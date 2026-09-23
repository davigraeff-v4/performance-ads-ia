#!/usr/bin/env python3
"""Revisor de boas práticas (scripts/kb_check.py): casos de aceite da Sprint 2.

Os dois casos vêm de dossiês reais (anonimizados): uma otimização Meta que
justificou consolidar conjuntos por "disputa interna no leilão" e uma
auditoria Google Ads que afirmou "leilão interno" entre duas campanhas de
pesquisa. Nos dois, a documentação oficial contradiz a premissa; o revisor
precisa trazer o artigo certo, em primeiro, com a frase que contradiz.
"""

from __future__ import annotations

import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import kb_check  # noqa: E402


def run(*argv: str) -> dict:
    out = io.StringIO()
    with redirect_stdout(out):
        kb_check.main([*argv, "--json"])
    return json.loads(out.getvalue())


class KbCheckAcceptanceTests(unittest.TestCase):
    def test_meta_internal_auction_premise_finds_contradicting_article(self) -> None:
        payload = run("--platform", "meta",
                      "Os dois conjuntos de remarketing disputam internamente o leilão e isso encarece o CPM")
        check = payload["checks"][0]
        top = check["candidates"][0]
        self.assertEqual(top["url"], "https://www.facebook.com/business/help/537699989762051")
        self.assertIn(top["path"], check["read_in_full"])
        self.assertIn("sobreposicao-leilao", check["rewrites"])
        urls = [candidate["url"] for candidate in check["candidates"]]
        self.assertIn("https://www.facebook.com/business/help/1679591828938781", urls)
        self.assertEqual(payload["skeleton"][0]["source_url"], top["url"])
        self.assertIsNone(payload["skeleton"][0]["verdict"])
        self.assertIn("ads_get_help_article", check["live_query"])

    def test_google_internal_auction_premise_finds_contradicting_sentence(self) -> None:
        payload = run("--platform", "google_ads",
                      "As duas campanhas de pesquisa disputam os mesmos termos num leilão interno e desperdiçam verba")
        check = payload["checks"][0]
        top = check["candidates"][0]
        self.assertTrue(top["url"].startswith("https://support.google.com/google-ads/answer/2756257"))
        self.assertIn(top["path"], check["read_in_full"])
        self.assertTrue(any("não concorrem entre si no leilão" in excerpt for excerpt in top["excerpts"]))
        self.assertIsNone(check["live_query"])

    def test_uncovered_premise_is_flagged_without_strong_candidates(self) -> None:
        payload = run("--platform", "meta", "custo por lead médio do setor industrial no Brasil em 2026")
        check = payload["checks"][0]
        self.assertEqual(check["read_in_full"], [])

    def test_input_file_mixes_platforms_without_crossing_bases(self) -> None:
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump([
                {"premise": "reduzir orçamento reinicia a fase de aprendizado", "platform": "meta"},
                {"premise": "mudar a meta de CPA coloca a estratégia em aprendizado", "platform": "google_ads"},
            ], handle)
        self.addCleanup(Path(handle.name).unlink)
        payload = run("--input", handle.name)
        meta, google = payload["checks"]
        self.assertTrue(all(c["path"].startswith("knowledge/meta-help-center/") for c in meta["candidates"]))
        self.assertTrue(all(c["path"].startswith("knowledge/official-google/") for c in google["candidates"]))

    def test_missing_platform_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            kb_check.main(["reduzir orçamento reinicia o aprendizado"])


if __name__ == "__main__":
    unittest.main()
