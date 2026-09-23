#!/usr/bin/env python3
"""Histórico do cliente: legado + V2, sem cruzar clientes."""

from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from scripts import client_history


def run(*argv: str) -> str:
    out = io.StringIO()
    with redirect_stdout(out):
        client_history.main(list(argv))
    return out.getvalue()


class ClientHistoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        base = self.tmp / "cliente-a"
        (base / "operacoes").mkdir(parents=True)
        legacy = {"status": "proposed", "platform": "meta", "type": "otimizacao"}
        (base / "2026-08-13-1000-meta-otimizacao-raio.md").write_text(
            "# Dossiê — raio das unidades\n\n```json\n" + json.dumps(legacy) + "\n```\n\n"
            "## Veredito\n\nA sobreposição de raio entre as unidades Norte e Sul chega a 4 km e encarece o alcance.\n",
            encoding="utf-8",
        )
        (base / "operacoes" / "2026-09-21-1500-meta-otimizacao-remarketing.json").write_text(
            json.dumps({"status": "executed", "platform": "meta", "type": "otimizacao",
                        "title": "Unificação do remarketing", "created_at": "2026-09-21T15:00:00-03:00"}),
            encoding="utf-8",
        )
        (base / "operacoes" / "2026-09-21-1500-meta-otimizacao-remarketing.md").write_text(
            "# Unificação do remarketing\n\nOs dois conjuntos de remarketing miram o mesmo público.\n", encoding="utf-8",
        )
        other = self.tmp / "cliente-b"
        other.mkdir()
        (other / "2026-08-01-1000-meta-analise-raio.md").write_text("# Outro cliente\n\nraio raio raio sobreposição\n", encoding="utf-8")

    def test_list_merges_legacy_and_v2_newest_first(self) -> None:
        output = run("--clients-dir", str(self.tmp), "list", "cliente-a")
        self.assertLess(output.index("Unificação do remarketing"), output.index("raio das unidades"))
        self.assertIn("(legado)", output)
        self.assertIn("(v2)", output)

    def test_open_filter_shows_only_unfinished(self) -> None:
        output = run("--clients-dir", str(self.tmp), "list", "cliente-a", "--open")
        self.assertIn("aguardando aprovação", output)
        self.assertNotIn("Unificação do remarketing", output)

    def test_search_finds_snippet_and_never_crosses_clients(self) -> None:
        output = run("--clients-dir", str(self.tmp), "search", "cliente-a", "sobreposição raio unidades")
        self.assertIn("4 km", output)
        self.assertNotIn("Outro cliente", output)

    def test_invalid_slug_is_rejected(self) -> None:
        with self.assertRaises(SystemExit):
            run("--clients-dir", str(self.tmp), "list", "../cliente-b")


if __name__ == "__main__":
    unittest.main()
