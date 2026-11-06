"""Travas do servidor de escrita Google Ads (integrations/google_ads_write_server).

Nenhum teste chama a API: requests.post é substituído e as credenciais são falsas.
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "integrations" / "google_ads_write_server"


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"gaws_{name}", PACKAGE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeMCP:
    def __init__(self) -> None:
        self.tools: dict = {}

    def tool(self):
        def decorator(function):
            self.tools[function.__name__] = function
            return function

        return decorator


class FakeResponse:
    def __init__(self, status: int = 200, body: dict | None = None) -> None:
        self.status_code = status
        self._body = body if body is not None else {}
        self.text = json.dumps(self._body)

    def json(self) -> dict:
        return self._body


class WriteToolsGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.allowlist = base / "allowed_accounts.json"
        self.allowlist.write_text(
            json.dumps(
                {
                    "default_login_customer_id": "9999999999",
                    "accounts": {"1112223333": {"name": "Conta Teste", "login_customer_id": "4445556666"}},
                }
            ),
            encoding="utf-8",
        )
        self.module = load("write_tools")
        self.module.ALLOWLIST_PATH = self.allowlist
        self.module.LOG_PATH = base / "logs" / "mutations.jsonl"
        self.mcp = FakeMCP()
        self.module.register(
            self.mcp,
            get_credentials=lambda: object(),
            get_headers=lambda _creds: {"Authorization": "Bearer x", "developer-token": "y", "login-customer-id": "1"},
            format_customer_id=lambda value: str(value).replace("-", "").strip(),
            api_version="v26",
        )
        self.calls: list[dict] = []
        patcher = mock.patch.object(self.module.requests, "post", side_effect=self.fake_post)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.env = mock.patch.dict(os.environ, {"GOOGLE_ADS_WRITE_MODE": "execute", "GOOGLE_ADS_ALLOW_REMOVE": "false"})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.addCleanup(self.tmp.cleanup)

    def fake_post(self, url, headers=None, json=None, timeout=None):
        self.calls.append({"url": url, "headers": headers, "json": json})
        return FakeResponse(200, {"results": [{"resourceName": "ok"}]})

    def call(self, tool: str, **kwargs) -> dict:
        return json.loads(asyncio.run(self.mcp.tools[tool](**kwargs)))

    def pause_op(self, cid: str = "1112223333") -> list[dict]:
        return [{"update": {"resourceName": f"customers/{cid}/campaigns/1", "status": "PAUSED"}, "updateMask": "status"}]

    def test_write_tools_default_to_validate_only(self) -> None:
        result = self.call("mutate", customer_id="111-222-3333", resource="campaigns", operations=self.pause_op())
        self.assertTrue(result["ok"])
        self.assertTrue(self.calls[0]["json"]["validateOnly"])

    def test_execute_uses_account_manager_from_allowlist(self) -> None:
        result = self.call(
            "mutate", customer_id="1112223333", resource="campaigns", operations=self.pause_op(), validate_only=False
        )
        self.assertTrue(result["ok"])
        self.assertFalse(self.calls[0]["json"]["validateOnly"])
        self.assertEqual(self.calls[0]["headers"]["login-customer-id"], "4445556666")
        self.assertTrue(self.calls[0]["url"].endswith("/v26/customers/1112223333/campaigns:mutate"))

    def test_account_outside_allowlist_is_blocked(self) -> None:
        result = self.call(
            "mutate", customer_id="7778889999", resource="campaigns", operations=self.pause_op("7778889999"), validate_only=False
        )
        self.assertFalse(result["ok"])
        self.assertIn("fora da lista", result["blocked"])
        self.assertEqual(self.calls, [])

    def test_remove_and_removed_status_are_blocked(self) -> None:
        remove = [{"remove": "customers/1112223333/campaigns/1"}]
        removed = [{"update": {"resourceName": "customers/1112223333/campaigns/1", "status": "REMOVED"}, "updateMask": "status"}]
        for operations in (remove, removed):
            with self.subTest(operations=operations):
                result = self.call("mutate", customer_id="1112223333", resource="campaigns", operations=operations, validate_only=False)
                self.assertIn("exclusão", result["blocked"])
        multi = [{"campaignOperation": {"remove": "customers/1112223333/campaigns/1"}}]
        self.assertIn("exclusão", self.call("mutate_multi", customer_id="1112223333", mutate_operations=multi)["blocked"])
        self.assertEqual(self.calls, [])

    def test_validate_only_mode_never_writes(self) -> None:
        with mock.patch.dict(os.environ, {"GOOGLE_ADS_WRITE_MODE": "validate_only"}):
            result = self.call("mutate", customer_id="1112223333", resource="campaigns", operations=self.pause_op(), validate_only=False)
        self.assertTrue(result["validate_only"])
        self.assertTrue(self.calls[0]["json"]["validateOnly"])

    def test_disabled_mode_blocks_everything(self) -> None:
        with mock.patch.dict(os.environ, {"GOOGLE_ADS_WRITE_MODE": "disabled"}):
            result = self.call("set_status", customer_id="1112223333", level="campaign", ids=["1"], status="PAUSED")
        self.assertIn("desligada", result["blocked"])
        self.assertEqual(self.calls, [])

    def test_set_status_only_pauses_or_enables(self) -> None:
        self.assertIn("ENABLED ou PAUSED", self.call("set_status", customer_id="1112223333", level="campaign", ids=["1"], status="REMOVED")["blocked"])
        self.assertIn("IDs inválidos", self.call("set_status", customer_id="1112223333", level="ad", ids=["123"], status="PAUSED")["blocked"])
        result = self.call("set_status", customer_id="1112223333", level="keyword", ids=["10~20"], status="PAUSED")
        self.assertTrue(result["ok"])
        self.assertEqual(
            self.calls[0]["json"]["operations"][0]["update"]["resourceName"], "customers/1112223333/adGroupCriteria/10~20"
        )

    def test_invalid_resource_name_is_rejected(self) -> None:
        result = self.call("mutate", customer_id="1112223333", resource="campaigns/../x", operations=self.pause_op())
        self.assertFalse(result["ok"])
        self.assertEqual(self.calls, [])

    def test_every_write_call_is_logged(self) -> None:
        self.call("mutate", customer_id="1112223333", resource="campaigns", operations=self.pause_op())
        lines = self.module.LOG_PATH.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        self.assertTrue(json.loads(lines[0])["validate_only"])


class PatchServerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.patch = load("patch_server")

    def anchors(self) -> str:
        return "\n".join(old for old, _ in self.patch.SERVER_PATCHES) + "\n"

    def test_patch_is_idempotent(self) -> None:
        once = self.patch.apply(self.anchors(), self.patch.SERVER_PATCHES, "server")
        twice = self.patch.apply(once, self.patch.SERVER_PATCHES, "server")
        self.assertEqual(once, twice)
        self.assertIn('"v26"', once)
        self.assertIn("write_tools.register(", once)
        self.assertEqual(once.count("write_tools.register("), 1)

    def test_unknown_server_version_fails_without_writing(self) -> None:
        with self.assertRaises(SystemExit):
            self.patch.apply("codigo diferente\n", self.patch.SERVER_PATCHES, "server")

    def test_installer_pins_upstream_commit(self) -> None:
        installer = (PACKAGE / "install.sh").read_text(encoding="utf-8")
        self.assertIn('UPSTREAM_COMMIT="461a1d673cf1c369e8b95fc9b5b1d9cb7f3ebb4a"', installer)
        self.assertIn("patch_server.py", installer)


class PackageHasNoSecretsTests(unittest.TestCase):
    def test_examples_are_placeholders(self) -> None:
        env = (PACKAGE / ".env.example").read_text(encoding="utf-8")
        self.assertIn("GOOGLE_ADS_DEVELOPER_TOKEN=SEU_DEVELOPER_TOKEN", env)
        self.assertIn("GOOGLE_ADS_WRITE_MODE=validate_only", env)
        self.assertIn("GOOGLE_ADS_ALLOW_REMOVE=false", env)
        allow = json.loads((PACKAGE / "allowed_accounts.example.json").read_text(encoding="utf-8"))
        self.assertEqual(allow["accounts"], {})

    def test_package_has_no_real_customer_ids(self) -> None:
        import re

        allowed_fakes = {"0000000000", "1234567890"}
        for path in PACKAGE.iterdir():
            if path.is_file():
                found = set(re.findall(r"(?<![0-9a-f])\d{10}(?![0-9a-f])", path.read_text(encoding="utf-8")))
                with self.subTest(file=path.name):
                    self.assertTrue(found <= allowed_fakes, f"{path.name}: {sorted(found - allowed_fakes)}")


if __name__ == "__main__":
    unittest.main()
