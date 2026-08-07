from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "search_google_ads_help.py"


class GoogleAdsHelpSearchTests(unittest.TestCase):
    def run_search(self, *args: str) -> dict[str, object]:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), *args, "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    def test_exact_title_match(self) -> None:
        payload = self.run_search(
            "Usar o Planejador de palavras-chave",
            "--platform", "google_ads",
        )
        expected_count = len([
            path for path in
            (ROOT / "knowledge" / "official-google" / "help-center").glob("**/*.md")
            if path.name != "INDEX.md"
        ])
        self.assertEqual(payload["article_count"], expected_count)
        first = payload["results"][0]
        self.assertEqual(first["match"], "exact")
        self.assertEqual(first["title"], "Usar o Planejador de palavras-chave")

    def test_accent_insensitive_title_match(self) -> None:
        payload = self.run_search(
            "organizacao de palavras chave",
            "--platform", "google_ads",
            "--title-only",
        )
        self.assertIn("organização", payload["results"][0]["title"].lower())

    def test_body_fallback_finds_forecast_limitations(self) -> None:
        payload = self.run_search(
            "previsão diferente do tráfego real",
            "--platform", "google_ads",
        )
        self.assertTrue(payload["body_fallback"])
        self.assertIn("previsões", payload["results"][0]["title"].lower())

    def test_meta_query_never_returns_google_articles(self) -> None:
        payload = self.run_search(
            "meta ads orçamento",
            "--platform", "google_ads",
        )
        self.assertTrue(payload["out_of_scope"])
        self.assertEqual(payload["results"], [])

    def test_platform_gate_rejects_meta_branch(self) -> None:
        payload = self.run_search(
            "planejador de palavras-chave",
            "--platform", "meta",
        )
        self.assertTrue(payload["out_of_scope"])
        self.assertEqual(payload["reason"], "platform_not_google_ads")


if __name__ == "__main__":
    unittest.main()
