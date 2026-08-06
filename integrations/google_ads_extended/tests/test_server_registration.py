from __future__ import annotations

import asyncio
import os
import re
from unittest import TestCase
from unittest.mock import patch

from fastmcp.exceptions import ToolError
import fastmcp

from performance_ads_google_ads_extended.server import (
    generate_keyword_ideas,
    get_extended_capabilities,
    mcp,
)


class ServerRegistrationTests(TestCase):
    def test_supported_fastmcp_major_is_installed(self) -> None:
        major_match = re.match(r"^(\d+)", fastmcp.__version__)
        self.assertIsNotNone(major_match)
        self.assertEqual(int(major_match.group(1)), 3)

    def test_only_expected_read_tools_are_registered(self) -> None:
        listed = asyncio.run(mcp.list_tools())
        tools = {tool.name: tool for tool in listed}
        self.assertEqual(set(tools), {"get_extended_capabilities", "generate_keyword_ideas"})
        self.assertTrue(all(tool.annotations.readOnlyHint for tool in tools.values()))
        self.assertFalse(any(token in name for name in tools for token in ("create", "update", "delete", "mutate", "execute")))

    def test_default_capability_report_is_fail_closed_and_sanitized(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            payload = get_extended_capabilities()
        self.assertEqual(payload["declared_capabilities"], ["reporting"])
        self.assertFalse(payload["planner_enabled"])
        self.assertEqual(payload["write_mode"], "disabled")
        self.assertFalse(payload["write_tools_registered"])
        self.assertEqual(payload["allowed_customer_count"], 0)

    def test_planner_gate_blocks_before_client_access(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ToolError) as context:
                generate_keyword_ideas("1234567890", keywords=["exemplo"])
        self.assertIn("Keyword Planner bloqueado localmente", str(context.exception))
