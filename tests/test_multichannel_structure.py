#!/usr/bin/env python3
"""Regressões estruturais do roteamento Meta e Google Ads."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MultichannelStructureTests(unittest.TestCase):
    def test_google_branch_is_complete(self) -> None:
        graph = json.loads((ROOT / "dependency_graph.json").read_text(encoding="utf-8"))
        google = {name for name in graph if "google-ads" in name}
        self.assertEqual(len(google), 9)
        self.assertIn("23-google-ads-campaign-build-plan", google)
        self.assertIn("24-google-ads-performance-diagnosis", google)

    def test_google_v1_is_read_only(self) -> None:
        contract = (ROOT / "CONTRATO-OPERACIONAL.md").read_text(encoding="utf-8")
        executor = (ROOT / "skills/13-approved-change-executor/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("toda mudança Google Ads é `manual_only`", contract)
        self.assertIn("bloquear toda chamada de escrita", executor)

    def test_file_based_mode_is_first_class(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("file_based", agents)
        self.assertIn("## 7. Usar sem MCP", readme)

    def test_multichannel_mutations_are_separate(self) -> None:
        contract = (ROOT / "CONTRATO-OPERACIONAL.md").read_text(encoding="utf-8")
        self.assertIn("um `operation_id` e uma aprovação por plataforma", contract)

    def test_keyword_research_does_not_invent_metrics(self) -> None:
        skill = (ROOT / "skills/18-google-ads-keyword-research/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Nunca apresentar estimativa do modelo como volume", skill)


if __name__ == "__main__":
    unittest.main()
