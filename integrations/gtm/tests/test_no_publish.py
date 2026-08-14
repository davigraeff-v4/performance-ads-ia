"""Structural guarantee: this integration can never request publish scope
or call a publish/version-creation endpoint, regardless of configuration."""

from __future__ import annotations

import inspect
from unittest import TestCase

from performance_ads_gtm import client, write

_PUBLISH_SCOPE = "https://www.googleapis.com/auth/tagmanager.publish"


class NoPublishTests(TestCase):
    def test_edit_scopes_exclude_publish(self) -> None:
        self.assertNotIn(_PUBLISH_SCOPE, client._EDIT_SCOPES)
        self.assertNotIn(_PUBLISH_SCOPE, client._READONLY_SCOPES)

    def test_client_module_has_no_publish_function(self) -> None:
        names = [name for name, _ in inspect.getmembers(client, inspect.isfunction)]
        self.assertFalse(any("publish" in name.lower() for name in names))

    def test_write_module_has_no_publish_or_version_function(self) -> None:
        names = [name for name, _ in inspect.getmembers(write, inspect.isfunction)]
        self.assertFalse(
            any("publish" in name.lower() or "version" in name.lower() for name in names)
        )
