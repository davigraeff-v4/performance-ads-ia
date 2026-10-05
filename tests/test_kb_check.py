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
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import help_search  # noqa: E402
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


class SearchStatusTests(unittest.TestCase):
    """O agent precisa saber quando a busca semântica (fastembed) não está ativa."""

    PREMISE = "Os dois conjuntos de remarketing disputam internamente o leilão e isso encarece o CPM"

    def test_engine_missing_reports_lexical_only_with_action(self) -> None:
        with mock.patch.object(kb_check, "engine_status", return_value=(False, "pacote fastembed não instalado")):
            payload = run("--platform", "meta", self.PREMISE)
        status = payload["search_status"]
        self.assertEqual(status["status"], "lexical_only")
        self.assertIn("pacote fastembed não instalado", status["reasons"])
        self.assertIn("pip install -r requirements-dev.txt", status["action"])

    def test_engine_missing_prints_warning_before_results(self) -> None:
        out = io.StringIO()
        with mock.patch.object(kb_check, "engine_status", return_value=(False, "pacote fastembed não instalado")):
            with redirect_stdout(out):
                kb_check.main(["--platform", "meta", self.PREMISE])
        text = out.getvalue()
        self.assertTrue(text.startswith("ATENÇÃO: a busca semântica não está ativa"))
        self.assertLess(text.index("ATENÇÃO"), text.index("Premissa 1"))

    def test_engine_ready_reports_hybrid_without_warning(self) -> None:
        out = io.StringIO()
        with mock.patch.object(kb_check, "engine_status", return_value=(True, None)):
            with redirect_stdout(out):
                kb_check.main(["--platform", "meta", self.PREMISE])
            payload = run("--platform", "meta", self.PREMISE)
        self.assertNotIn("ATENÇÃO", out.getvalue())
        self.assertEqual(payload["search_status"], {"status": "hybrid", "reasons": [], "action": None})

    def test_vector_failure_during_search_is_reported_with_reason(self) -> None:
        weak = "quando eu mexo muito na verba o sistema volta a aprender do zero"
        with mock.patch.object(kb_check, "engine_status", return_value=(True, None)), \
             mock.patch.object(help_search, "vector_candidates", return_value=None), \
             mock.patch.object(help_search, "unavailable_reason", return_value="falha ao gerar o vetor da consulta (OSError)"):
            payload = run("--platform", "meta", weak)
        self.assertEqual(payload["checks"][0]["search_mode"], "lexical_fallback")
        self.assertEqual(payload["search_status"]["status"], "lexical_only")
        self.assertIn("falha ao gerar o vetor da consulta (OSError)", payload["search_status"]["reasons"])

    def test_help_search_payload_names_the_mode(self) -> None:
        with mock.patch.object(help_search, "vector_candidates", return_value=None), \
             mock.patch.object(help_search, "unavailable_reason", return_value="pacote fastembed não instalado"):
            payload = help_search.search("quando eu mexo muito na verba o sistema volta a aprender do zero",
                                         base_platform="meta", requested_platform="meta", warn=lambda _m: None)
        self.assertEqual(payload["search_mode"], "lexical_fallback")
        self.assertEqual(payload["vector_unavailable_reason"], "pacote fastembed não instalado")
        lexical = help_search.search("quando eu mexo muito na verba o sistema volta a aprender do zero",
                                     base_platform="meta", requested_platform="meta", mode="lexical")
        self.assertEqual(lexical["search_mode"], "lexical")
        self.assertIsNone(lexical["vector_unavailable_reason"])


if __name__ == "__main__":
    unittest.main()
