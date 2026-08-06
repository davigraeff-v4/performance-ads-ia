from __future__ import annotations

import os
from unittest import TestCase
from unittest.mock import patch

from performance_ads_google_ads_extended.config import (
    ConfigurationError,
    Settings,
    normalize_customer_id,
)


class SettingsTests(TestCase):
    def test_defaults_are_reporting_only_and_write_disabled(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings.from_environment()
        self.assertEqual(settings.declared_capabilities, frozenset({"reporting"}))
        self.assertFalse(settings.planner_enabled)
        self.assertEqual(settings.write_mode, "disabled")

    def test_planner_requires_declared_capability(self) -> None:
        environment = {"PERFORMANCE_ADS_GOOGLE_PLANNER_ENABLED": "true"}
        with patch.dict(os.environ, environment, clear=True):
            with self.assertRaises(ConfigurationError):
                Settings.from_environment()

    def test_customer_must_be_allowlisted(self) -> None:
        environment = {
            "PERFORMANCE_ADS_GOOGLE_DECLARED_CAPABILITIES": "reporting,keyword_planning",
            "PERFORMANCE_ADS_GOOGLE_PLANNER_ENABLED": "true",
            "PERFORMANCE_ADS_GOOGLE_ALLOWED_CUSTOMER_IDS": "123-456-7890",
        }
        with patch.dict(os.environ, environment, clear=True):
            settings = Settings.from_environment()
        self.assertEqual(settings.require_planner("1234567890"), "1234567890")
        with self.assertRaises(ConfigurationError):
            settings.require_planner("9999999999")

    def test_capabilities_never_return_secret_values(self) -> None:
        environment = {
            "GOOGLE_ADS_DEVELOPER_TOKEN": "YOUR_DEVELOPER_TOKEN",
            "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "1234567890",
        }
        with patch.dict(os.environ, environment, clear=True):
            payload = Settings.from_environment().public_capabilities()
        rendered = repr(payload)
        self.assertNotIn("YOUR_DEVELOPER_TOKEN", rendered)
        self.assertNotIn("1234567890", rendered)
        self.assertTrue(payload["developer_token_present"])
        self.assertTrue(payload["login_customer_present"])

    def test_customer_id_normalization(self) -> None:
        self.assertEqual(normalize_customer_id("123-456-7890"), "1234567890")
        with self.assertRaises(ConfigurationError):
            normalize_customer_id("customer-one")
