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
                        payload = route(*args, expected_code=3 if platform == "google_ads" and intent == "execucao" else 0)
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
        self.assertIn("02-meta-account-connection", skills)
        self.assertLess(skills.index("11-performance-diagnosis"), skills.index("12-optimization-change-set"))
        self.assertFalse(any("google-ads" in skill for skill in skills))

    def test_google_optimization_is_deep_and_never_loads_meta(self) -> None:
        payload = route("--intent", "otimizacao", "--platform", "google_ads", "--source-mode", "connected_read")
        skills = payload["branches"][0]["planned_skills"]
        self.assertIn("16-google-ads-account-connection", skills)
        self.assertLess(skills.index("24-google-ads-performance-diagnosis"), skills.index("12-optimization-change-set"))
        self.assertNotIn("11-performance-diagnosis", skills)
        self.assertNotIn("15-meta-help-center-retrieval", skills)

    def test_file_based_skips_account_connections_and_mcp_config(self) -> None:
        for platform, account_skill in [("meta", "02-meta-account-connection"), ("google_ads", "16-google-ads-account-connection")]:
            with self.subTest(platform=platform):
                payload = route("--intent", "analise", "--platform", platform, "--source-mode", "file_based")
                skills = payload["branches"][0]["planned_skills"]
                self.assertNotIn(account_skill, skills)
                self.assertNotIn("00-configuracao-mcp", skills)

    def test_multichannel_keeps_independent_sources_and_branches(self) -> None:
        payload = route(
            "--intent", "auditoria",
            "--platform", "both",
            "--meta-source-mode", "connected_read",
            "--google-source-mode", "file_based",
        )
        self.assertEqual([branch["platform"] for branch in payload["branches"]], ["meta", "google_ads"])
        self.assertIn("02-meta-account-connection", payload["branches"][0]["planned_skills"])
        self.assertNotIn("16-google-ads-account-connection", payload["branches"][1]["planned_skills"])

    def test_keywords_are_conditional(self) -> None:
        without = route("--intent", "planejamento", "--platform", "google_ads", "--source-mode", "context_only")
        with_keywords = route("--intent", "planejamento", "--platform", "google_ads", "--source-mode", "context_only", "--requires-keywords")
        self.assertNotIn("18-google-ads-keyword-research", without["branches"][0]["planned_skills"])
        self.assertIn("18-google-ads-keyword-research", with_keywords["branches"][0]["planned_skills"])

    def test_onboarding_alone_never_covers_platform_knowledge_questions(self) -> None:
        # Documenta a garantia por trás da regra de "mensagens compostas": a
        # rota onboarding é estreita de propósito e não inclui o gate de
        # conhecimento — por isso uma segunda intenção (ex: planejamento)
        # embutida na mesma mensagem do gestor precisa da própria rota,
        # nunca deve ser respondida usando só o que o onboarding carregou.
        for platform, knowledge_skill in [("meta", "15-meta-help-center-retrieval"), ("google_ads", "17-google-ads-official-retrieval")]:
            with self.subTest(platform=platform):
                payload = route("--intent", "onboarding", "--platform", platform, "--source-mode", "context_only")
                skills = payload["branches"][0]["planned_skills"]
                self.assertNotIn(knowledge_skill, skills)

    def test_planning_route_always_includes_platform_knowledge_gate(self) -> None:
        # Contraparte do teste acima: uma vez que a segunda intenção (ex:
        # planejamento) é corretamente identificada e roteada, o gate de
        # conhecimento vem garantido como passo "always" — não depende do
        # gestor lembrar de pedir explicitamente.
        for platform, knowledge_skill in [("meta", "15-meta-help-center-retrieval"), ("google_ads", "17-google-ads-official-retrieval")]:
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
                    self.assertNotIn("26-gtm-tracking-audit-fix", without["branches"][0]["planned_skills"])
                    with_audit = route(
                        "--intent", intent, "--platform", platform,
                        "--source-mode", "context_only", "--requires-gtm-audit",
                    )
                    skills = with_audit["branches"][0]["planned_skills"]
                    self.assertIn("26-gtm-tracking-audit-fix", skills)
                    self.assertLess(
                        skills.index("03-measurement-data-quality"),
                        skills.index("26-gtm-tracking-audit-fix"),
                    )

    def test_gtm_audit_is_not_offered_outside_auditoria_and_otimizacao(self) -> None:
        payload = route(
            "--intent", "planejamento", "--platform", "meta",
            "--source-mode", "context_only", "--requires-gtm-audit",
        )
        self.assertNotIn("26-gtm-tracking-audit-fix", payload["branches"][0]["planned_skills"])


if __name__ == "__main__":
    unittest.main()
