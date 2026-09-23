"""Gates de escrita GTM: container do caminho, validate_only e fingerprint."""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock

from performance_ads_gtm import write
from performance_ads_gtm.config import ConfigurationError, Settings

WORKSPACE = "accounts/1/containers/456/workspaces/7"
TAG_PATH = f"{WORKSPACE}/tags/9"


def settings(mode: str = "execute", allowed: frozenset[str] = frozenset({"456"})) -> Settings:
    return Settings(
        declared_capabilities=frozenset({"reporting", "tag_management"}),
        allowed_container_ids=allowed,
        write_mode=mode,
        credentials_path=Path("/nao/usado.json"),
        token_cache_path=Path("/nao/usado-token.json"),
    )


def fake_gtm(current: dict | None = None) -> tuple[MagicMock, MagicMock]:
    gtm = MagicMock()
    tags = gtm.accounts.return_value.containers.return_value.workspaces.return_value.tags.return_value
    tags.get.return_value.execute.return_value = current or {}
    tags.create.return_value.execute.return_value = {"created": True}
    tags.update.return_value.execute.return_value = {"updated": True}
    return gtm, tags


class WriteGuardTests(TestCase):
    def test_path_from_another_container_is_rejected(self) -> None:
        gtm, tags = fake_gtm()
        with self.assertRaises(ConfigurationError):
            write.create_tag(gtm, settings(), "456", "accounts/1/containers/999/workspaces/7", {"name": "x"})
        tags.create.assert_not_called()

    def test_malformed_path_is_rejected(self) -> None:
        gtm, tags = fake_gtm()
        with self.assertRaises(ConfigurationError):
            write.update_tag(gtm, settings(), "456", "tags/9", {"name": "x"})
        tags.update.assert_not_called()

    def test_container_outside_allowlist_is_rejected(self) -> None:
        gtm, tags = fake_gtm()
        with self.assertRaises(ConfigurationError):
            write.create_tag(gtm, settings(allowed=frozenset({"123"})), "456", WORKSPACE, {"name": "x"})
        tags.create.assert_not_called()

    def test_disabled_mode_never_writes(self) -> None:
        gtm, tags = fake_gtm()
        with self.assertRaises(ConfigurationError):
            write.create_tag(gtm, settings(mode="disabled"), "456", WORKSPACE, {"name": "x"})
        tags.create.assert_not_called()

    def test_validate_only_create_does_not_call_api(self) -> None:
        gtm, tags = fake_gtm()
        result = write.create_tag(gtm, settings(mode="validate_only"), "456", WORKSPACE, {"name": "x"})
        self.assertTrue(result["validate_only"])
        tags.create.assert_not_called()

    def test_validate_only_update_reads_but_does_not_write(self) -> None:
        gtm, tags = fake_gtm({"name": "antiga", "type": "html", "fingerprint": "42"})
        result = write.update_tag(gtm, settings(mode="validate_only"), "456", TAG_PATH, {"name": "nova"})
        self.assertEqual(result["proposed"], {"name": "nova", "type": "html", "fingerprint": "42"})
        tags.update.assert_not_called()

    def test_update_merges_partial_body_and_sends_fingerprint(self) -> None:
        gtm, tags = fake_gtm({"name": "antiga", "type": "html", "parameter": [{"key": "a"}], "fingerprint": "42"})
        write.update_tag(gtm, settings(), "456", TAG_PATH, {"name": "nova"})
        kwargs = tags.update.call_args.kwargs
        self.assertEqual(kwargs["fingerprint"], "42")
        self.assertEqual(kwargs["body"]["parameter"], [{"key": "a"}])
        self.assertEqual(kwargs["body"]["name"], "nova")
