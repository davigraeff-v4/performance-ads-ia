#!/usr/bin/env python3
"""Regressões do índice vetorial: isolamento por plataforma e fallback gracioso.

Estes testes exigem que o índice vetorial já tenha sido construído
(scripts/build_knowledge_vector_index.py --platform all). Se o índice não
existir, os testes de isolamento são pulados — a suíde lexical continua
cobrindo o comportamento sem índice vetorial via search_meta_help.py /
search_google_ads_help.py em --mode lexical.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT / "knowledge" / ".vector-index"
META_SEARCH = ROOT / "scripts" / "search_meta_help.py"
GOOGLE_SEARCH = ROOT / "scripts" / "search_google_ads_help.py"


def _index_files_present() -> bool:
    return (
        (INDEX_DIR / "meta-help-center.npz").is_file()
        and (INDEX_DIR / "meta-help-center-meta.json").is_file()
        and (INDEX_DIR / "google-ads-help-center.npz").is_file()
        and (INDEX_DIR / "google-ads-help-center-meta.json").is_file()
    )


def run_search(script: Path, query: str, *options: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(script), query, *options, "--json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


@unittest.skipUnless(_index_files_present(), "índice vetorial não construído localmente")
class VectorIndexIsolationTests(unittest.TestCase):
    def test_meta_index_metadata_never_tags_google_ads(self) -> None:
        metadata = json.loads((INDEX_DIR / "meta-help-center-meta.json").read_text(encoding="utf-8"))
        self.assertTrue(metadata)
        for chunk in metadata:
            self.assertEqual(chunk["platform"], "meta")
            self.assertTrue(chunk["path"].startswith("knowledge/meta-help-center/"))

    def test_google_ads_index_metadata_never_tags_meta(self) -> None:
        metadata = json.loads((INDEX_DIR / "google-ads-help-center-meta.json").read_text(encoding="utf-8"))
        self.assertTrue(metadata)
        for chunk in metadata:
            self.assertEqual(chunk["platform"], "google_ads")
            self.assertTrue(chunk["path"].startswith("knowledge/official-google/help-center/"))

    def test_no_client_data_indexed(self) -> None:
        for manifest_name in ("meta-help-center-meta.json", "google-ads-help-center-meta.json"):
            metadata = json.loads((INDEX_DIR / manifest_name).read_text(encoding="utf-8"))
            for chunk in metadata:
                self.assertFalse(chunk["path"].startswith("clients/"))

    def test_hybrid_search_never_crosses_platform_at_runtime(self) -> None:
        # A pergunta é sobre Meta, mas pedida explicitamente na plataforma
        # google_ads: o gate de plataforma já bloqueia antes de tocar no
        # índice vetorial (mesmo comportamento do lexical puro).
        payload = run_search(
            META_SEARCH,
            "sobre o pixel da meta e eventos duplicados",
            "--platform",
            "google_ads",
        )
        self.assertTrue(payload["out_of_scope"])
        self.assertEqual(payload["results"], [])

    def test_hybrid_mode_enriches_a_paraphrased_query(self) -> None:
        lexical_only = run_search(
            META_SEARCH,
            "meu pixel esta contando o mesmo evento duas vezes quando uso capi e o pixel do site juntos",
            "--platform",
            "meta",
            "--mode",
            "lexical",
            "--limit",
            "3",
        )
        hybrid = run_search(
            META_SEARCH,
            "meu pixel esta contando o mesmo evento duas vezes quando uso capi e o pixel do site juntos",
            "--platform",
            "meta",
            "--mode",
            "hybrid",
            "--limit",
            "3",
        )
        self.assertFalse(lexical_only["vector_used"])
        self.assertTrue(hybrid["vector_used"])
        self.assertGreaterEqual(hybrid["results"][0]["score"], lexical_only["results"][0]["score"])


class VectorFallbackTests(unittest.TestCase):
    @unittest.skipUnless(_index_files_present(), "índice vetorial não construído localmente")
    def test_missing_index_falls_back_to_lexical_without_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            backup = Path(tmp) / "vector-index-backup"
            shutil.move(str(INDEX_DIR), str(backup))
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(META_SEARCH),
                        "meu pixel esta contando o mesmo evento duas vezes quando uso capi e o pixel do site juntos",
                        "--platform",
                        "meta",
                        "--limit",
                        "3",
                        "--json",
                    ],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                )
            finally:
                shutil.move(str(backup), str(INDEX_DIR))
        payload = json.loads(result.stdout)
        self.assertFalse(payload["out_of_scope"])
        self.assertFalse(payload["vector_used"])
        self.assertTrue(payload["results"])

    def test_lexical_mode_never_imports_vector_engine(self) -> None:
        # Garante que --mode lexical não paga o custo (nem o risco) de carregar
        # fastembed/numpy para casos exact/strong, mesmo com índice presente.
        result = subprocess.run(
            [
                sys.executable,
                str(META_SEARCH),
                "Sobre a meta de ROAS",
                "--platform",
                "meta",
                "--mode",
                "lexical",
                "--json",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertFalse(payload["vector_used"])
        self.assertEqual(payload["results"][0]["signal"], "lexical")


if __name__ == "__main__":
    unittest.main()
