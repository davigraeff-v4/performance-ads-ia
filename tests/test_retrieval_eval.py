#!/usr/bin/env python3
"""Regressão da busca nas bases oficiais (Sprint 2, etapa 2B).

O patamar foi medido por `scripts/eval_retrieval.py` depois do ajuste; a
linha de base anterior ao ajuste está em `tests/fixtures/retrieval_baseline.json`.
Se um teste cair, rode `python3 scripts/eval_retrieval.py --compare` para ver
qual consulta piorou antes de mexer em pesos ou no dicionário.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import eval_retrieval  # noqa: E402
import help_search  # noqa: E402

VECTOR_INDEX_READY = all(
    (ROOT / "knowledge" / ".vector-index" / name).is_file()
    for name in ("meta-help-center.npz", "google-ads-help-center.npz")
)


@unittest.skipUnless(VECTOR_INDEX_READY, "índice vetorial não construído localmente")
class RetrievalRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = json.loads(eval_retrieval.FIXTURE.read_text(encoding="utf-8"))
        cls.rows = [eval_retrieval.evaluate_query(item, set()) for item in fixture["queries"]]
        cls.summary = eval_retrieval.summarize(cls.rows)

    def test_tuning_queries_keep_the_measured_level(self) -> None:
        data = self.summary["todas"]
        self.assertGreaterEqual(data["acerto_1"], 0.90)
        self.assertEqual(data["acerto_3"], 1.0)
        self.assertEqual(data["forte_errado"], 0.0)
        self.assertEqual(data["intrusao_politica"], 0.0)
        self.assertEqual(data["gate_ok"], 1.0)

    def test_control_queries_keep_the_measured_level(self) -> None:
        data = self.summary["controle"]
        self.assertGreaterEqual(data["acerto_1"], 0.80)
        self.assertGreaterEqual(data["acerto_3"], 0.90)
        self.assertEqual(data["forte_errado"], 0.0)

    def test_real_premises_from_legacy_dossiers_find_the_contradicting_article(self) -> None:
        # Casos de aceite da Sprint 2: a premissa errada precisa trazer, em
        # primeiro lugar, o artigo oficial que a contradiz.
        by_id = {row["id"]: row for row in self.rows}
        for query_id in ("meta-05", "google-02"):
            self.assertEqual(by_id[query_id]["rank"], 1, query_id)


class RankingRuleTests(unittest.TestCase):
    def search(self, query: str, platform: str, **kwargs) -> dict:
        return help_search.search(query, base_platform=platform, requested_platform=platform,
                                  warn=lambda _m: None, **kwargs)

    def test_vector_or_body_alone_never_labels_strong(self) -> None:
        self.assertEqual(help_search.match_label(95.0, 30.0), "related")
        self.assertEqual(help_search.match_label(80.0, 74.9), "related")
        self.assertEqual(help_search.match_label(80.0, 75.0), "strong")
        self.assertEqual(help_search.match_label(100.0, 100.0), "exact")

    def test_rewrite_rules_are_platform_scoped(self) -> None:
        meta_rules = {rule["id"] for rule in help_search.matching_rewrites("mesmas palavras-chave competem entre si", "meta")}
        google_rules = {rule["id"] for rule in help_search.matching_rewrites("mesmas palavras-chave competem entre si", "google_ads")}
        self.assertIn("priorizacao-palavras-chave", google_rules)
        self.assertNotIn("priorizacao-palavras-chave", meta_rules)

    def test_rewrite_can_be_disabled_and_is_reported(self) -> None:
        query = "palavras-chave duplicadas em campanhas diferentes"
        with_rewrite = self.search(query, "google_ads", mode="lexical")
        without = self.search(query, "google_ads", mode="lexical", rewrite=False)
        self.assertEqual(with_rewrite["rewrites"], ["priorizacao-palavras-chave"])
        self.assertEqual(with_rewrite["results"][0]["signal"], "rewrite")
        self.assertEqual(without["rewrites"], [])
        self.assertNotEqual(without["results"][0]["path"], with_rewrite["results"][0]["path"])

    def test_policy_articles_only_rise_for_policy_queries(self) -> None:
        self.assertTrue(help_search.is_policy_query("anúncio reprovado por política"))
        self.assertFalse(help_search.is_policy_query("sobreposição de público entre conjuntos"))
        policy = self.search("anúncio reprovado por política de práticas discriminatórias", "meta", mode="lexical")
        self.assertTrue(help_search.is_policy_article(policy["results"][0]["path"]))

    def test_rewrite_never_crosses_the_platform_gate(self) -> None:
        payload = help_search.search("palavras-chave duplicadas no Google Ads", base_platform="meta",
                                     requested_platform="meta", warn=lambda _m: None)
        self.assertTrue(payload["out_of_scope"])


if __name__ == "__main__":
    unittest.main()
