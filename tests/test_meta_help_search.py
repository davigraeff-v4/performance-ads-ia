#!/usr/bin/env python3
"""Regressões da recuperação seletiva da Central Meta."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEARCH = ROOT / "scripts" / "search_meta_help.py"


def search(query: str, *options: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(SEARCH), query, "--platform", "meta", *options, "--json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


class MetaHelpSearchTests(unittest.TestCase):
    def test_exact_title(self) -> None:
        payload = search("Sobre a meta de ROAS", "--title-only", "--limit", "1")
        self.assertEqual(payload["platform"], "meta")
        self.assertFalse(payload["out_of_scope"])
        self.assertEqual(payload["article_count"], 153)
        self.assertEqual(payload["results"][0]["match"], "exact")
        self.assertTrue(payload["results"][0]["path"].endswith("sobre-a-meta-de-roas.md"))

    def test_accent_insensitive_title(self) -> None:
        payload = search("publico semelhante", "--title-only", "--limit", "3")
        self.assertEqual(payload["results"][0]["match"], "strong")
        self.assertIn("público semelhante", payload["results"][0]["title"].lower())

    def test_topic_fallback_finds_deduplication_article(self) -> None:
        payload = search("meu pixel está duplicando eventos", "--limit", "3")
        paths = {result["path"] for result in payload["results"]}
        self.assertTrue(payload["body_fallback"])
        self.assertTrue(any("como-monitorar-a-configuracao-da-api" in path for path in paths))

    def test_unrelated_query_remains_weak(self) -> None:
        payload = search("qual a capital da frança", "--limit", "1")
        self.assertEqual(payload["results"][0]["match"], "weak")

    def test_google_ads_query_never_returns_meta_articles(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SEARCH), "como configurar conversões no Google Ads", "--platform", "google_ads", "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["out_of_scope"])
        self.assertEqual(payload["reason"], "platform_not_meta")
        self.assertEqual(payload["results"], [])

    def test_conflicting_query_is_fail_closed(self) -> None:
        payload = search("como configurar conversões no Google Ads")
        self.assertTrue(payload["out_of_scope"])
        self.assertEqual(payload["reason"], "query_platform_conflict")
        self.assertEqual(payload["results"], [])


if __name__ == "__main__":
    unittest.main()
