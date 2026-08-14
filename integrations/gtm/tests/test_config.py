from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from performance_ads_gtm.config import ConfigurationError, Settings


class SettingsTests(TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.credentials_path = Path(self._tmp.name) / "client-secret.json"
        self.credentials_path.write_text("{}")

    def test_defaults_are_reporting_only_and_write_disabled(self) -> None:
        environment = {
            "PERFORMANCE_ADS_GTM_CREDENTIALS_PATH": str(self.credentials_path),
        }
        with patch.dict(os.environ, environment, clear=True):
            settings = Settings.from_environment()
        self.assertEqual(settings.declared_capabilities, frozenset({"reporting"}))
        self.assertEqual(settings.write_mode, "disabled")
        self.assertEqual(settings.allowed_container_ids, frozenset())

    def test_missing_credentials_path_fails_closed(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigurationError):
                Settings.from_environment()

    def test_nonexistent_credentials_file_fails_closed(self) -> None:
        environment = {
            "PERFORMANCE_ADS_GTM_CREDENTIALS_PATH": str(
                Path(self._tmp.name) / "does-not-exist.json"
            ),
        }
        with patch.dict(os.environ, environment, clear=True):
            with self.assertRaises(ConfigurationError):
                Settings.from_environment()

    def test_write_mode_requires_capability_and_allowlist(self) -> None:
        base_environment = {
            "PERFORMANCE_ADS_GTM_CREDENTIALS_PATH": str(self.credentials_path),
            "PERFORMANCE_ADS_GTM_WRITE_MODE": "execute",
        }
        with patch.dict(os.environ, base_environment, clear=True):
            with self.assertRaises(ConfigurationError):
                Settings.from_environment()

        with_capability = {
            **base_environment,
            "PERFORMANCE_ADS_GTM_DECLARED_CAPABILITIES": "reporting,tag_management",
        }
        with patch.dict(os.environ, with_capability, clear=True):
            with self.assertRaises(ConfigurationError):
                Settings.from_environment()

        fully_configured = {
            **with_capability,
            "PERFORMANCE_ADS_GTM_ALLOWED_CONTAINER_IDS": "123,456",
        }
        with patch.dict(os.environ, fully_configured, clear=True):
            settings = Settings.from_environment()
        self.assertEqual(settings.require_container("123"), "123")
        with self.assertRaises(ConfigurationError):
            settings.require_container("999")

    def test_capabilities_never_return_secret_values(self) -> None:
        environment = {
            "PERFORMANCE_ADS_GTM_CREDENTIALS_PATH": str(self.credentials_path),
        }
        with patch.dict(os.environ, environment, clear=True):
            payload = Settings.from_environment().public_capabilities()
        rendered = repr(payload)
        self.assertNotIn(str(self.credentials_path), rendered)
        self.assertTrue(payload["credentials_configured"])
