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

    def test_google_write_remains_fail_closed(self) -> None:
        contract = (ROOT / "CONTRATO-OPERACIONAL.md").read_text(encoding="utf-8")
        executor = (ROOT / "skills/13-approved-change-executor/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("nenhuma ferramenta de escrita Google Ads é registrada", contract)
        self.assertIn("bloquear toda chamada de escrita", executor)

    def test_google_ads_extended_is_fail_closed(self) -> None:
        base = ROOT / "integrations" / "google_ads_extended"
        self.assertTrue((base / "pyproject.toml").is_file())
        server = (base / "src" / "performance_ads_google_ads_extended" / "server.py").read_text(encoding="utf-8")
        config = (base / "src" / "performance_ads_google_ads_extended" / "config.py").read_text(encoding="utf-8")
        self.assertIn("get_extended_capabilities", server)
        self.assertIn('"write_tools_registered": False', config)
        self.assertIn('"PERFORMANCE_ADS_GOOGLE_WRITE_MODE", "disabled"', config)

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

    def test_google_ads_mcp_installation_is_documented_for_both_clients(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        required = [
            "## 6. Google Ads MCP — opcional",
            "## 15. Apêndice opcional — Google Ads MCP local",
            "Rota B — OAuth de usuário sem Google Cloud CLI",
            "claude mcp add --scope local google_ads",
            "codex mcp add google_ads",
            "customers_list_accessible_customers",
            "Nunca cole developer token",
            "Complemento local experimental",
            "write_tools_registered: false",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, readme)

    def test_gtm_api_installation_is_documented_and_never_publishes(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        contract = (ROOT / "CONTRATO-OPERACIONAL.md").read_text(encoding="utf-8")
        skill = (ROOT / "skills/26-gtm-tracking-audit-fix/SKILL.md").read_text(encoding="utf-8")
        required_in_readme = [
            "## 16. Apêndice opcional — Google Tag Manager (GTM)",
            "Tag Manager API",
            "OAuth Client (tipo Desktop app)",
            "credentials/gtm-oauth-client-secret.json",
            "PERFORMANCE_ADS_GTM_ALLOWED_CONTAINER_IDS",
            "Nunca cole client secret",
            "Nunca publica",
        ]
        for marker in required_in_readme:
            with self.subTest(marker=marker):
                self.assertIn(marker, readme)
        self.assertIn("A integração nunca publica uma versão do GTM", contract)
        self.assertIn("README.md §16", skill)

    def test_google_ads_mcp_skill_protects_credentials_and_validates_reads(self) -> None:
        skill = (ROOT / "skills/00-configuracao-mcp/SKILL.md").read_text(encoding="utf-8")
        required = [
            "Nunca pedir que o usuário cole segredo",
            "Google Workspace CLI e Google Ads API são superfícies diferentes",
            "customers_list_accessible_customers",
            "metadata_get_resource_metadata",
            "search_search",
            "Nunca testar escrita",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, skill)


if __name__ == "__main__":
    unittest.main()
