#!/usr/bin/env python3
"""Prompt de fonte única e hook de proteção de clients/."""

from __future__ import annotations

import json
import subprocess
import sys
import unicodedata
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "scripts" / "hooks" / "check_client_write.py"


def hook(file_path: str) -> int:
    payload = json.dumps({"tool_name": "Write", "tool_input": {"file_path": file_path}})
    return subprocess.run([sys.executable, str(HOOK)], input=payload, text=True, capture_output=True).returncode


class PromptAndHookTests(unittest.TestCase):
    def test_generated_prompts_match_single_source(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_agent_prompts.py"), "--check"], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_prompts_keep_router_precedence_and_chat_contract(self) -> None:
        for name in ("CLAUDE.md", "AGENTS.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(file=name):
                self.assertIn("25-performance-ads-router", text)
                self.assertIn("templates/resposta-chat.md", text)
                self.assertIn("scripts/dossier.py", text)
                self.assertIn("file_based", text)
                self.assertNotIn("somente:", text)

    def test_hook_blocks_operations_legacy_and_handwritten_dossiers(self) -> None:
        base = unicodedata.normalize("NFC", str(ROOT / "clients" / "cliente-teste"))
        self.assertEqual(hook(f"{base}/operacoes/2026-09-21-1500-meta-otimizacao-x.json"), 2)
        self.assertEqual(hook(f"{base}/2026-10-01-1000-meta-otimizacao-x.md"), 2)

    def test_hook_allows_profile_and_code(self) -> None:
        self.assertEqual(hook(str(ROOT / "clients" / "cliente-teste" / "CLIENTE.md")), 0)
        self.assertEqual(hook(str(ROOT / "scripts" / "dossier.py")), 0)

    def test_hook_handles_decomposed_accents(self) -> None:
        decomposed = unicodedata.normalize("NFD", str(ROOT / "clients" / "cliente-teste" / "operacoes" / "x.json"))
        self.assertEqual(hook(decomposed), 2)


if __name__ == "__main__":
    unittest.main()
