"""Create/update operations over a GTM workspace (draft, never published).

Every function here writes to a *workspace* — GTM's draft area. Nothing
becomes live on the client's site until a human explicitly creates a
container version and publishes it from the GTM UI (or a future, separately
gated integration). This module intentionally has no publish/version
function: PERFORMANCE ADS IA does not publish GTM changes.

Every call requires Settings.require_write_enabled() and
Settings.require_container() to have already passed — callers (scripts,
skills) must resolve those before invoking anything below.
"""

from __future__ import annotations

from typing import Any

from googleapiclient.discovery import Resource

from .config import Settings


def _guard(settings: Settings, container_id: str) -> None:
    settings.require_write_enabled()
    settings.require_container(container_id)


def create_tag(
    gtm: Resource,
    settings: Settings,
    container_id: str,
    workspace_path: str,
    tag_body: dict[str, Any],
) -> dict[str, Any]:
    _guard(settings, container_id)
    return gtm.accounts().containers().workspaces().tags().create(
        parent=workspace_path, body=tag_body
    ).execute()


def update_tag(
    gtm: Resource,
    settings: Settings,
    container_id: str,
    tag_path: str,
    tag_body: dict[str, Any],
) -> dict[str, Any]:
    _guard(settings, container_id)
    return gtm.accounts().containers().workspaces().tags().update(
        path=tag_path, body=tag_body
    ).execute()


def create_trigger(
    gtm: Resource,
    settings: Settings,
    container_id: str,
    workspace_path: str,
    trigger_body: dict[str, Any],
) -> dict[str, Any]:
    _guard(settings, container_id)
    return gtm.accounts().containers().workspaces().triggers().create(
        parent=workspace_path, body=trigger_body
    ).execute()


def update_trigger(
    gtm: Resource,
    settings: Settings,
    container_id: str,
    trigger_path: str,
    trigger_body: dict[str, Any],
) -> dict[str, Any]:
    _guard(settings, container_id)
    return gtm.accounts().containers().workspaces().triggers().update(
        path=trigger_path, body=trigger_body
    ).execute()


def create_variable(
    gtm: Resource,
    settings: Settings,
    container_id: str,
    workspace_path: str,
    variable_body: dict[str, Any],
) -> dict[str, Any]:
    _guard(settings, container_id)
    return gtm.accounts().containers().workspaces().variables().create(
        parent=workspace_path, body=variable_body
    ).execute()


def update_variable(
    gtm: Resource,
    settings: Settings,
    container_id: str,
    variable_path: str,
    variable_body: dict[str, Any],
) -> dict[str, Any]:
    _guard(settings, container_id)
    return gtm.accounts().containers().workspaces().variables().update(
        path=variable_path, body=variable_body
    ).execute()
