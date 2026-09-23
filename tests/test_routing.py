#!/usr/bin/env python3
"""Regressões do roteamento determinístico e da separação de plataformas."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "scripts" / "route_request.py"


def route(*args: str, expected_code: int = 0) -> dict:
    result = subprocess.run(
        [sys.executable, str(ROUTER), *args, "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != expected_code:
        raise AssertionError(f"route exit={result.returncode}: {result.stderr}\n{result.stdout}")
    return json.loads(result.stdout)


class RoutingTests(unittest.TestCase):
    def test_every_route_respects_static_dependency_order(self) -> None:
        matrix = json.loads((ROOT / "routing_matrix.json").read_text(encoding="utf-8"))
        graph = json.loads((ROOT / "dependency_graph.json").read_text(encoding="utf-8"))
        for intent, platforms in matrix["intents"].items():
            for platform in platforms:
                for source_mode in ("connected_read", "file_based", "context_only"):
                    for requires_keywords in (False, True):
                        args = ["--intent", intent, "--platform", platform, "--source-mode", source_mode]
                        if requires_keywords:
                            args.append("--requires-keywords")
                        blocked = (platform == "google_ads" and intent == "execucao") or (
                            intent == "avaliacao" and source_mode == "context_only"
                        )
                        payload = route(*args, expected_code=3 if blocked else 0)
                        if payload["status"] == "blocked":
                            continue
                        seen: set[str] = set()
                        for skill in payload["branches"][0]["planned_skills"]:
                            missing = set(graph[skill]) - seen
                            self.assertFalse(missing, f"{intent}:{platform}:{source_mode} executa {skill} antes de {sorted(missing)}")
                            seen.add(skill)

    def test_route_id_and_output_contract_are_explicit(self) -> None:
        payload = route("--intent", "analise", "--platform", "meta", "--source-mode", "file_based")
        branch = payload["branches"][0]
        self.assertEqual(branch["route_id"], "analise:meta:file_based")
        self.assertEqual(branch["output"], "relatorio_analise")
        self.assertEqual(branch["delivery_state"], "awaiting_record_approval")
        self.assertEqual(branch["dossier_persistence"], "after_editorial_approval")
        self.assertEqual(branch["dossier_state_after_approval"], "analysis_only")

    def test_new_analysis_never_persists_before_editorial_approval(self) -> None:
        for intent in ("auditoria", "analise", "otimizacao", "relatorio"):
            for platform in ("meta", "google_ads"):
                with self.subTest(intent=intent, platform=platform):
                    payload = route(
                        "--intent", intent,
                        "--platform", platform,
                        "--source-mode", "file_based",
                    )
                    branch = payload["branches"][0]
                    self.assertEqual(branch["delivery_state"], "awaiting_record_approval")
                    self.assertEqual(branch["dossier_persistence"], "after_editorial_approval")

    def test_operational_approval_uses_existing_dossier(self) -> None:
        payload = route("--intent", "aprovacao", "--platform", "meta", "--source-mode", "connected_read")
        branch = payload["branches"][0]
        self.assertEqual(branch["delivery_state"], "approved")
        self.assertEqual(branch["dossier_persistence"], "existing_dossier_required")

    def test_meta_optimization_is_deep_and_never_loads_google(self) -> None:
        payload = route("--intent", "otimizacao", "--platform", "meta", "--source-mode", "connected_read")
        skills = payload["branches"][0]["planned_skills"]
        self.assertIn("conexao/meta", skills)
        self.assertLess(skills.index("diagnostico/meta"), skills.index("change-set"))
        self.assertFalse(any("google-ads" in skill for skill in skills))

    def test_google_optimization_is_deep_and_never_loads_meta(self) -> None:
        payload = route("--intent", "otimizacao", "--platform", "google_ads", "--source-mode", "connected_read")
        skills = payload["branches"][0]["planned_skills"]
        self.assertIn("conexao/google-ads", skills)
        self.assertLess(skills.index("diagnostico/google-ads"), skills.index("change-set"))
        self.assertNotIn("diagnostico/meta", skills)
        self.assertNotIn("revisor/meta", skills)

    def test_file_based_skips_account_connections_and_mcp_config(self) -> None:
        for platform, account_skill in [("meta", "conexao/meta"), ("google_ads", "conexao/google-ads")]:
            with self.subTest(platform=platform):
                payload = route("--intent", "analise", "--platform", platform, "--source-mode", "file_based")
                skills = payload["branches"][0]["planned_skills"]
                self.assertNotIn(account_skill, skills)
                self.assertNotIn("conexao/configuracao-mcp", skills)

    def test_multichannel_keeps_independent_sources_and_branches(self) -> None:
        payload = route(
            "--intent", "auditoria",
            "--platform", "both",
            "--meta-source-mode", "connected_read",
            "--google-source-mode", "file_based",
        )
        self.assertEqual([branch["platform"] for branch in payload["branches"]], ["meta", "google_ads"])
        self.assertIn("conexao/meta", payload["branches"][0]["planned_skills"])
        self.assertNotIn("conexao/google-ads", payload["branches"][1]["planned_skills"])

    def test_keywords_are_conditional(self) -> None:
        without = route("--intent", "planejamento", "--platform", "google_ads", "--source-mode", "context_only")
        with_keywords = route("--intent", "planejamento", "--platform", "google_ads", "--source-mode", "context_only", "--requires-keywords")
        self.assertNotIn("planejamento/google-ads-palavras-chave", without["branches"][0]["planned_skills"])
        self.assertIn("planejamento/google-ads-palavras-chave", with_keywords["branches"][0]["planned_skills"])

    def test_onboarding_alone_never_covers_platform_knowledge_questions(self) -> None:
        # Documenta a garantia por trás da regra de "mensagens compostas": a
        # rota onboarding é estreita de propósito e não inclui o gate de
        # conhecimento — por isso uma segunda intenção (ex: planejamento)
        # embutida na mesma mensagem do gestor precisa da própria rota,
        # nunca deve ser respondida usando só o que o onboarding carregou.
        for platform, knowledge_skill in [("meta", "revisor/meta"), ("google_ads", "revisor/google-ads")]:
            with self.subTest(platform=platform):
                payload = route("--intent", "onboarding", "--platform", platform, "--source-mode", "context_only")
                skills = payload["branches"][0]["planned_skills"]
                self.assertNotIn(knowledge_skill, skills)

    def test_planning_route_always_includes_platform_knowledge_gate(self) -> None:
        # Contraparte do teste acima: uma vez que a segunda intenção (ex:
        # planejamento) é corretamente identificada e roteada, o gate de
        # conhecimento vem garantido como passo "always" — não depende do
        # gestor lembrar de pedir explicitamente.
        for platform, knowledge_skill in [("meta", "revisor/meta"), ("google_ads", "revisor/google-ads")]:
            with self.subTest(platform=platform):
                payload = route("--intent", "planejamento", "--platform", platform, "--source-mode", "context_only")
                skills = payload["branches"][0]["planned_skills"]
                self.assertIn(knowledge_skill, skills)

    def test_google_execution_is_fail_closed(self) -> None:
        payload = route("--intent", "execucao", "--platform", "google_ads", "--source-mode", "connected_read", expected_code=3)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("google_ads_write_manual_only", payload["gates"])
        self.assertEqual(payload["branches"][0]["planned_skills"], [])

    def test_undefined_platform_is_blocked(self) -> None:
        payload = route("--intent", "analise", "--platform", "undefined", expected_code=3)
        self.assertEqual(payload["gates"], ["platform_undefined"])

    def test_meta_keyword_research_is_not_supported(self) -> None:
        payload = route("--intent", "pesquisa_palavras_chave", "--platform", "meta", "--source-mode", "context_only", expected_code=3)
        self.assertIn("intent_platform_not_supported", payload["gates"])

    def test_gtm_audit_is_conditional_and_never_auto_included(self) -> None:
        for intent in ("auditoria", "otimizacao"):
            for platform in ("meta", "google_ads"):
                with self.subTest(intent=intent, platform=platform):
                    without = route("--intent", intent, "--platform", platform, "--source-mode", "context_only")
                    self.assertNotIn("mensuracao/gtm", without["branches"][0]["planned_skills"])
                    with_audit = route(
                        "--intent", intent, "--platform", platform,
                        "--source-mode", "context_only", "--requires-gtm-audit",
                    )
                    skills = with_audit["branches"][0]["planned_skills"]
                    self.assertIn("mensuracao/gtm", skills)
                    self.assertLess(
                        skills.index("mensuracao"),
                        skills.index("mensuracao/gtm"),
                    )

    def test_gtm_audit_is_not_offered_outside_auditoria_and_otimizacao(self) -> None:
        payload = route(
            "--intent", "planejamento", "--platform", "meta",
            "--source-mode", "context_only", "--requires-gtm-audit",
        )
        self.assertNotIn("mensuracao/gtm", payload["branches"][0]["planned_skills"])

    def test_question_lookup_and_history_never_create_dossier(self) -> None:
        for intent in ("duvida", "consulta", "historico"):
            for platform in ("meta", "google_ads"):
                with self.subTest(intent=intent, platform=platform):
                    branch = route("--intent", intent, "--platform", platform, "--source-mode", "connected_read")["branches"][0]
                    self.assertEqual(branch["delivery_state"], "chat_only")
                    self.assertEqual(branch["dossier_persistence"], "none")

    def test_question_uses_official_base_even_without_account_source(self) -> None:
        payload = route("--intent", "duvida", "--platform", "meta", "--source-mode", "unavailable")
        self.assertEqual(payload["status"], "ready")
        self.assertEqual(payload["branches"][0]["planned_skills"], ["revisor/meta"])

    def test_default_depth_is_full_only_for_audit(self) -> None:
        expected = {"auditoria": "full", "analise": "focused", "otimizacao": "focused", "relatorio": "focused", "ajuste": "quick"}
        for intent, depth in expected.items():
            with self.subTest(intent=intent):
                branch = route("--intent", intent, "--platform", "meta", "--source-mode", "file_based")["branches"][0]
                self.assertEqual(branch["depth"], depth)
        forced = route("--intent", "analise", "--platform", "meta", "--source-mode", "file_based", "--depth", "full")
        self.assertEqual(forced["branches"][0]["depth"], "full")

    def test_adjustment_checks_official_base_but_skips_diagnosis(self) -> None:
        skills = route("--intent", "ajuste", "--platform", "meta", "--source-mode", "connected_read")["branches"][0]["planned_skills"]
        self.assertIn("revisor/meta", skills)
        self.assertIn("change-set", skills)
        self.assertNotIn("diagnostico/meta", skills)

    def test_report_checks_results_against_official_base(self) -> None:
        for platform, knowledge in (("meta", "revisor/meta"), ("google_ads", "revisor/google-ads")):
            with self.subTest(platform=platform):
                skills = route("--intent", "relatorio", "--platform", platform, "--source-mode", "connected_read")["branches"][0]["planned_skills"]
                self.assertEqual(skills[0], knowledge)

    def test_multichannel_keyword_research_skips_meta_instead_of_blocking(self) -> None:
        payload = route(
            "--intent", "pesquisa_palavras_chave", "--platform", "both",
            "--meta-source-mode", "context_only", "--google-source-mode", "context_only",
        )
        self.assertEqual(payload["status"], "ready")
        statuses = {branch["platform"]: branch["status"] for branch in payload["branches"]}
        self.assertEqual(statuses, {"google_ads": "ready", "meta": "not_applicable"})


    def test_evaluation_reads_data_checks_measurement_and_updates_existing_dossier(self) -> None:
        for platform, connection, knowledge, diagnosis in (
            ("meta", "conexao/meta", "revisor/meta", "diagnostico/meta"),
            ("google_ads", "conexao/google-ads", "revisor/google-ads", "diagnostico/google-ads"),
        ):
            payload = route("--intent", "avaliacao", "--platform", platform, "--source-mode", "connected_read")
            branch = payload["branches"][0]
            self.assertEqual(payload["status"], "ready")
            self.assertEqual(branch["depth"], "quick")
            self.assertEqual(branch["final_state"], "evaluated")
            self.assertEqual(branch["dossier_persistence"], "existing_dossier_required")
            for skill in (connection, knowledge, "mensuracao", "diagnostico/metas-e-linha-de-base", diagnosis):
                self.assertIn(skill, branch["planned_skills"])
            self.assertNotIn("change-set", branch["planned_skills"])

    def test_evaluation_is_blocked_without_account_or_file_data(self) -> None:
        payload = route("--intent", "avaliacao", "--platform", "meta", "--source-mode", "context_only", expected_code=3)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("evaluation_requires_account_or_file_data", payload["branches"][0]["gates"])
        file_based = route("--intent", "avaliacao", "--platform", "meta", "--source-mode", "file_based")
        self.assertEqual(file_based["status"], "ready")


if __name__ == "__main__":
    unittest.main()
