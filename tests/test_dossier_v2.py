#!/usr/bin/env python3
"""Ciclo de vida dos dossiês V2 (scripts/dossier.py) sobre clientes sintéticos."""

from __future__ import annotations

import copy
import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from scripts import dossier


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "synthetic" / "v2"
SLUG = "cliente-exemplo"
OP_ID = "op-20260921-1500-cliente-exemplo-meta-remarketing-curitiba"


def run(*argv: str) -> tuple[int, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = dossier.main(list(argv))
    return code, out.getvalue() + err.getvalue()


class DossierV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.clients = self.tmp / "clients"
        (self.clients / SLUG).mkdir(parents=True)
        (self.clients / SLUG / "CLIENTE.md").write_text("# Cliente — Cliente Exemplo\n", encoding="utf-8")
        self.spec = json.loads((EXAMPLES / "otimizacao-remarketing.spec.json").read_text(encoding="utf-8"))
        self.body = (EXAMPLES / "otimizacao-remarketing.body.md").read_text(encoding="utf-8")

    # ------------------------------------------------------------------ apoio

    def write_inputs(self, spec: dict | None = None, body: str | None = None) -> tuple[Path, Path]:
        spec_path = self.tmp / "spec.json"
        body_path = self.tmp / "body.md"
        spec_path.write_text(json.dumps(spec or self.spec, ensure_ascii=False), encoding="utf-8")
        body_path.write_text(body if body is not None else self.body, encoding="utf-8")
        return spec_path, body_path

    def cli(self, *argv: str) -> tuple[int, str]:
        return run("--clients-dir", str(self.clients), *argv)

    def create(self, spec: dict | None = None, body: str | None = None) -> tuple[int, str]:
        spec_path, body_path = self.write_inputs(spec, body)
        return self.cli(
            "new", "--client", SLUG, "--spec", str(spec_path), "--body", str(body_path),
            "--now", "2026-09-21T15:00:00-03:00",
        )

    def files(self) -> tuple[Path, Path]:
        ops = self.clients / SLUG / "operacoes"
        return next(ops.glob("*.json")), next(ops.glob("*.md"))

    def operation(self) -> dict:
        return json.loads(self.files()[0].read_text(encoding="utf-8"))

    def verify(self) -> tuple[int, str]:
        return self.cli("verify", "--client", SLUG)

    # ------------------------------------------------------------------ criação

    def test_new_creates_readable_pair_without_json_in_markdown(self) -> None:
        code, output = self.create()
        self.assertEqual(code, 0, output)
        json_path, md_path = self.files()
        self.assertEqual(json_path.stem, md_path.stem)
        operation = self.operation()
        self.assertEqual(operation["operation_id"], OP_ID)
        self.assertEqual(operation["status"], "proposed")
        markdown = md_path.read_text(encoding="utf-8")
        self.assertNotIn("```json", markdown)
        self.assertIn("### Mudança 1 — Criar o conjunto", markdown)
        self.assertIn("**Efeito líquido no orçamento diário:** R$ 0,00", markdown)
        self.assertLess(markdown.index("## Resumo"), markdown.index("<details>"))
        self.assertEqual(self.verify()[0], 0)

    def test_analysis_without_changes_is_analysis_only(self) -> None:
        spec = copy.deepcopy(self.spec)
        spec.update({"type": "analise", "changes": [], "evaluation": None, "knowledge_checks": []})
        spec["route"]["route_ids"] = ["analise:meta:connected_read"]
        spec["route"]["executed_skills"] = [
            "01-client-campaign-intake", "02-meta-account-connection", "15-meta-help-center-retrieval",
            "03-measurement-data-quality", "04-goals-kpis-baseline", "11-performance-diagnosis",
        ]
        body = self.body.replace("<!-- mudancas -->", "Nenhuma mudança nesta rodada.")
        code, output = self.create(spec, body)
        self.assertEqual(code, 0, output)
        self.assertEqual(self.operation()["status"], "analysis_only")

    def test_json_block_in_body_is_rejected(self) -> None:
        code, output = self.create(body=self.body + "\n```json\n{}\n```\n")
        self.assertNotEqual(code, 0)
        self.assertIn("bloco JSON", output)

    def test_missing_client_profile_is_rejected(self) -> None:
        (self.clients / SLUG / "CLIENTE.md").unlink()
        code, output = self.create()
        self.assertNotEqual(code, 0)
        self.assertIn("CLIENTE.md", output)

    # ------------------------------------------------------------------ regras de rota e conteúdo

    def test_always_skill_cannot_be_skipped_as_condition_not_met(self) -> None:
        spec = copy.deepcopy(self.spec)
        spec["route"]["executed_skills"].remove("15-meta-help-center-retrieval")
        spec["route"]["skipped_skills"] = [{
            "skill": "15-meta-help-center-retrieval",
            "reason_code": "condition_not_met",
            "detail": "sem pergunta de funcionamento",
        }]
        code, output = self.create(spec)
        self.assertNotEqual(code, 0)
        self.assertIn("condição da rota", output)
        self.assertFalse((self.clients / SLUG / "operacoes").exists() and any((self.clients / SLUG / "operacoes").iterdir()))

    def test_knowledge_check_is_mandatory_for_changes(self) -> None:
        spec = copy.deepcopy(self.spec)
        spec["route"]["executed_skills"].remove("15-meta-help-center-retrieval")
        spec["route"]["skipped_skills"] = [{
            "skill": "15-meta-help-center-retrieval",
            "reason_code": "no_platform_mechanism",
            "detail": "mudança operacional simples",
        }]
        spec["knowledge_checks"] = []
        code, output = self.create(spec)
        self.assertNotEqual(code, 0)
        self.assertIn("checagem de boas práticas", output)

    def test_deletion_in_rollback_is_rejected(self) -> None:
        spec = copy.deepcopy(self.spec)
        spec["changes"][0]["rollback"] = "Pausar ou excluir o conjunto criado."
        code, output = self.create(spec)
        self.assertNotEqual(code, 0)
        self.assertIn("só permite pausar", output)

    def test_audience_exclusion_wording_is_only_a_warning(self) -> None:
        spec = copy.deepcopy(self.spec)
        spec["changes"][0]["why"] = "Achado 1: excluir compradores recentes do público do conjunto novo."
        code, output = self.create(spec)
        self.assertEqual(code, 0, output)
        self.assertIn("confirme que é segmentação", output)

    def test_google_ads_cannot_execute_via_mcp(self) -> None:
        spec = copy.deepcopy(self.spec)
        spec["platform"] = "google_ads"
        spec["route"]["route_ids"] = ["otimizacao:google_ads:connected_read"]
        spec["route"]["executed_skills"] = [
            "01-client-campaign-intake", "16-google-ads-account-connection", "17-google-ads-official-retrieval",
            "03-measurement-data-quality", "04-goals-kpis-baseline", "24-google-ads-performance-diagnosis",
            "12-optimization-change-set",
        ]
        for change in spec["changes"]:
            change["platform"] = "google_ads"
        code, output = self.create(spec)
        self.assertNotEqual(code, 0)
        self.assertIn("use manual_only", output)

    def test_mutations_require_evaluation_criteria(self) -> None:
        spec = copy.deepcopy(self.spec)
        spec["evaluation"] = None
        code, output = self.create(spec)
        self.assertNotEqual(code, 0)
        self.assertIn("critério de avaliação", output)

    # ------------------------------------------------------------------ integridade

    def test_editing_approved_text_is_detected(self) -> None:
        self.assertEqual(self.create()[0], 0)
        _, md_path = self.files()
        md_path.write_text(md_path.read_text(encoding="utf-8").replace("5 a 7 vezes", "10 vezes"), encoding="utf-8")
        code, output = self.verify()
        self.assertNotEqual(code, 0)
        self.assertIn("texto aprovado", output)

    def test_editing_changes_after_approval_is_detected(self) -> None:
        self.assertEqual(self.create()[0], 0)
        self.assertEqual(self.cli("approve", OP_ID, "--statement", "/aprovar-operacao")[0], 0)
        json_path, _ = self.files()
        operation = self.operation()
        operation["changes"][1]["daily_budget_delta"] = -70.0
        json_path.write_text(json.dumps(operation, ensure_ascii=False), encoding="utf-8")
        code, output = self.verify()
        self.assertNotEqual(code, 0)
        self.assertIn("alteradas depois da aprovação", output)

    def test_hash_matches_legacy_canonical_script(self) -> None:
        self.assertEqual(self.create()[0], 0)
        self.assertEqual(self.cli("approve", OP_ID, "--statement", "/aprovar-operacao")[0], 0)
        from scripts.hash_change_set import canonical_payload
        import hashlib
        operation = self.operation()
        expected = hashlib.sha256(
            json.dumps(canonical_payload(operation), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertEqual(operation["approval"]["hash"], expected)

    # ------------------------------------------------------------------ ciclo de vida

    def test_manual_execution_with_divergences_and_evaluation(self) -> None:
        self.assertEqual(self.create()[0], 0)
        self.assertEqual(self.cli("approve", OP_ID, "--statement", "/aprovar-operacao")[0], 0)
        results = json.dumps([
            {"change_id": "c1", "status": "executed_manually", "via": "Gerenciador", "divergences": ["Orçamento R$ 90,00"]},
            {"change_id": "c2", "status": "success", "via": "MCP", "readback_confirmed": True},
            {"change_id": "c3", "status": "success", "via": "MCP", "readback_confirmed": True},
        ])
        code, output = self.cli("record-execution", OP_ID, "--results", results)
        self.assertEqual(code, 0, output)
        self.assertEqual(self.operation()["status"], "executed")
        markdown = self.files()[1].read_text(encoding="utf-8")
        self.assertIn("Diferenças entre o aprovado e o executado", markdown)
        self.assertIn("aplicada manualmente", markdown)
        code, output = self.cli("evaluate", OP_ID, "--result", "success", "--notes", "Custo por lead caiu para R$ 41,20.")
        self.assertEqual(code, 0, output)
        self.assertEqual(self.operation()["status"], "evaluated")
        self.assertEqual(self.verify()[0], 0)

    def test_failure_on_one_change_is_partial_failure(self) -> None:
        self.assertEqual(self.create()[0], 0)
        self.assertEqual(self.cli("approve", OP_ID, "--statement", "/aprovar-operacao")[0], 0)
        results = json.dumps([
            {"change_id": "c1", "status": "failed", "via": "MCP", "detail": "erro 1815089"},
            {"change_id": "c2", "status": "success", "via": "MCP"},
        ])
        self.assertEqual(self.cli("record-execution", OP_ID, "--results", results)[0], 0)
        self.assertEqual(self.operation()["status"], "partial_failure")

    def test_revision_bumps_version_and_resets_approval(self) -> None:
        self.assertEqual(self.create()[0], 0)
        self.assertEqual(self.cli("approve", OP_ID, "--statement", "/aprovar-operacao")[0], 0)
        spec = copy.deepcopy(self.spec)
        spec["changes"][1]["daily_budget_delta"] = -70.0
        spec_path, body_path = self.write_inputs(spec)
        code, output = self.cli(
            "revise", OP_ID, "--spec", str(spec_path), "--body", str(body_path), "--reason", "orçamento ajustado",
        )
        self.assertEqual(code, 0, output)
        operation = self.operation()
        self.assertEqual(operation["version"], 2)
        self.assertIsNone(operation["approval"])
        self.assertEqual(operation["status"], "proposed")
        self.assertEqual(operation["previous_versions"][0]["version"], 1)

    def test_list_shows_open_operations_and_due_evaluations(self) -> None:
        self.assertEqual(self.create()[0], 0)
        code, output = self.cli("list", "--open", "--today", "2026-09-22")
        self.assertEqual(code, 0)
        self.assertIn("Aguardando sua aprovação", output)
        self.assertIn("decisão pendente", output)

    def test_migrate_legacy_generates_reviewable_draft(self) -> None:
        legacy = json.loads((ROOT / "examples/synthetic/operation-approved.json").read_text(encoding="utf-8"))
        legacy_path = self.clients / SLUG / "2026-08-01-1000-google_ads-otimizacao-termos.md"
        legacy_path.write_text(
            "# Dossiê legado\n\n```json\n" + json.dumps(legacy, ensure_ascii=False) + "\n```\n\n## Veredito aprovado\n\nTexto.\n",
            encoding="utf-8",
        )
        out_dir = self.tmp / "work"
        code, output = self.cli("migrate", str(legacy_path), "--out-dir", str(out_dir))
        self.assertEqual(code, 0, output)
        spec = json.loads(next(out_dir.glob("*.spec.json")).read_text(encoding="utf-8"))
        self.assertEqual(spec["platform"], "google_ads")
        self.assertTrue(all(change["execution_mode"] != "mcp" for change in spec["changes"]))
        self.assertIn("legacy_source", spec)


if __name__ == "__main__":
    unittest.main()
