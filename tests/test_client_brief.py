#!/usr/bin/env python3
"""Memória do cliente: resumo gerado na hora e migração da ficha, em clientes sintéticos."""

from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from scripts import client_brief, dossier, migrate_client_profile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "synthetic" / "v2"
SLUG = "cliente-exemplo"
OP_ID = "op-20260921-1500-cliente-exemplo-meta-remarketing-curitiba"

PROFILE = """# Cliente — Cliente Exemplo

## Identificação

- Slug: cliente-exemplo
- Modelo: lead_generation

## Negócio

- Produto/serviço: troca de óleo
- Linha 2
- Linha 3
- Linha 4
- Linha 5
- Linha 6
- Linha 7
- Linha 8

## Histórico e aprendizados

- **2026-09-18**: remarketing unificado; avaliação até 02/10.
- **2026-08-05**: nesta conta o custo por mil impressões domina o custo por lead.

## Preferências operacionais

- Relatório mensal.
"""


def run(module, *argv: str) -> tuple[int, str]:
    out = io.StringIO()
    with redirect_stdout(out):
        code = module.main(list(argv))
    return code, out.getvalue()


class ClientBriefTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.clients = self.tmp / "clients"
        self.base = self.clients / SLUG
        self.base.mkdir(parents=True)
        (self.base / "CLIENTE.md").write_text(PROFILE, encoding="utf-8")

    def register_operation(self) -> None:
        code, output = run(
            dossier, "--clients-dir", str(self.clients), "new", "--client", SLUG,
            "--spec", str(EXAMPLES / "otimizacao-remarketing.spec.json"),
            "--body", str(EXAMPLES / "otimizacao-remarketing.body.md"),
            "--now", "2026-09-21T15:00:00-03:00",
        )
        self.assertEqual(code, 0, output)

    def execute_operation(self) -> None:
        self.assertEqual(run(dossier, "--clients-dir", str(self.clients), "approve", OP_ID, "--statement", "/aprovar-operacao")[0], 0)
        results = json.dumps([{"change_id": c, "status": "success", "via": "MCP", "readback_confirmed": True} for c in ("c1", "c2", "c3")])
        code, output = run(dossier, "--clients-dir", str(self.clients), "record-execution", OP_ID, "--results", results)
        self.assertEqual(code, 0, output)

    def brief(self, today: str) -> str:
        return run(client_brief, SLUG, "--clients-dir", str(self.clients), "--today", today)[1]

    def test_profile_is_compact_and_history_stays_out_of_the_profile(self) -> None:
        output = self.brief("2026-09-22")
        self.assertIn("### Negócio", output)
        self.assertIn("(+2 linhas no arquivo)", output)
        profile_part = output.split("## Em aberto")[0]
        self.assertNotIn("remarketing unificado", profile_part)
        self.assertIn("### Preferências operacionais", profile_part)
        self.assertIn("Sem APRENDIZADOS.md ainda", output)
        self.assertIn("custo por mil impressões domina", output)

    def test_open_operation_and_pending_decisions_are_highlighted(self) -> None:
        self.register_operation()
        output = self.brief("2026-09-22")
        open_part = output.split("## Em aberto")[1].split("## Últimas operações")[0]
        self.assertIn("aguardando aprovação", open_part)
        self.assertIn("Decisões pendentes do gestor", open_part)

    def test_overdue_evaluation_appears_only_after_due_date(self) -> None:
        self.register_operation()
        self.execute_operation()
        self.assertNotIn("Avaliações vencidas", self.brief("2026-10-01"))
        output = self.brief("2026-10-12")
        self.assertIn("Avaliações vencidas", output)
        self.assertIn("avaliação vencida desde 12/10", output)

    def test_learnings_file_replaces_legacy_history_excerpt(self) -> None:
        (self.base / "APRENDIZADOS.md").write_text(
            "# Aprendizados — Cliente Exemplo\n\n## Mídia e plataformas\n\n- **Decompor o custo por lead.** Por quê: teste.\n\n## Mensuração e rastreamento\n",
            encoding="utf-8",
        )
        output = self.brief("2026-09-22")
        self.assertIn("Decompor o custo por lead", output)
        self.assertNotIn("Sem APRENDIZADOS.md", output)
        self.assertNotIn("## Mensuração e rastreamento", output)

    def test_brief_never_crosses_clients(self) -> None:
        with self.assertRaises(SystemExit):
            run(client_brief, "../outro", "--clients-dir", str(self.clients))


class MigrateClientProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.clients = self.tmp / "clients"
        self.base = self.clients / SLUG
        self.base.mkdir(parents=True)
        (self.base / "CLIENTE.md").write_text(PROFILE, encoding="utf-8")

    def migrate(self, *extra: str) -> tuple[int, str]:
        return run(migrate_client_profile, SLUG, "--clients-dir", str(self.clients), "--now", "2026-09-23T12:00", *extra)

    def test_dry_run_writes_nothing(self) -> None:
        code, output = self.migrate()
        self.assertEqual(code, 0)
        self.assertIn("Simulação", output)
        self.assertEqual(sorted(p.name for p in self.base.iterdir()), ["CLIENTE.md"])
        self.assertEqual((self.base / "CLIENTE.md").read_text(encoding="utf-8"), PROFILE)

    def test_apply_splits_profile_keeps_history_verbatim_and_backs_up(self) -> None:
        draft = self.tmp / "aprendizados.md"
        draft.write_text("# Aprendizados — Cliente Exemplo\n\n## Mídia e plataformas\n\n- **Regra aprovada.**\n", encoding="utf-8")
        code, output = self.migrate("--learnings", str(draft), "--apply")
        self.assertEqual(code, 0, output)
        backup = self.base / "CLIENTE.md.bak-202609231200"
        self.assertEqual(backup.read_text(encoding="utf-8"), PROFILE)
        profile = (self.base / "CLIENTE.md").read_text(encoding="utf-8")
        self.assertNotIn("remarketing unificado", profile)
        self.assertIn("## Preferências operacionais", profile)
        self.assertIn("## Onde está o resto", profile)
        history = (self.base / "HISTORICO-ANTERIOR.md").read_text(encoding="utf-8")
        self.assertIn("- **2026-09-18**: remarketing unificado; avaliação até 02/10.", history)
        self.assertIn("Regra aprovada", (self.base / "APRENDIZADOS.md").read_text(encoding="utf-8"))

    def test_second_run_is_a_no_op_and_existing_files_are_never_overwritten(self) -> None:
        self.assertEqual(self.migrate("--apply")[0], 0)
        code, output = self.migrate("--apply")
        self.assertEqual(code, 0)
        self.assertIn("já migrada", output)
        (self.base / "CLIENTE.md").write_text(PROFILE, encoding="utf-8")
        code, output = run(migrate_client_profile, SLUG, "--clients-dir", str(self.clients), "--now", "2026-09-24T12:00", "--apply")
        self.assertEqual(code, 1)
        self.assertIn("RECUSADO", output)


if __name__ == "__main__":
    unittest.main()
