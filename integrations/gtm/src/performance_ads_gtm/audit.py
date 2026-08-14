"""Read-only inspection helpers over the Google Tag Manager API.

These calls only ever require tagmanager.readonly and never mutate state.
Tag/trigger/variable creation or publishing belongs in a separate module
gated by Settings.require_write_enabled().
"""

from __future__ import annotations

from typing import Any

from googleapiclient.discovery import Resource


def list_accounts(gtm: Resource) -> list[dict[str, Any]]:
    response = gtm.accounts().list().execute()
    return response.get("account", [])


def list_containers(gtm: Resource, account_path: str) -> list[dict[str, Any]]:
    response = gtm.accounts().containers().list(parent=account_path).execute()
    return response.get("container", [])


def list_workspaces(gtm: Resource, container_path: str) -> list[dict[str, Any]]:
    response = gtm.accounts().containers().workspaces().list(
        parent=container_path
    ).execute()
    return response.get("workspace", [])


def list_tags(gtm: Resource, workspace_path: str) -> list[dict[str, Any]]:
    response = gtm.accounts().containers().workspaces().tags().list(
        parent=workspace_path
    ).execute()
    return response.get("tag", [])


def list_triggers(gtm: Resource, workspace_path: str) -> list[dict[str, Any]]:
    response = gtm.accounts().containers().workspaces().triggers().list(
        parent=workspace_path
    ).execute()
    return response.get("trigger", [])


def list_variables(gtm: Resource, workspace_path: str) -> list[dict[str, Any]]:
    response = gtm.accounts().containers().workspaces().variables().list(
        parent=workspace_path
    ).execute()
    return response.get("variable", [])


def snapshot_container(gtm: Resource, container_path: str) -> dict[str, Any]:
    """Read-only snapshot of a container's default workspace for auditing."""

    workspaces = list_workspaces(gtm, container_path)
    default_workspace = next(
        (w for w in workspaces if w.get("name") == "Default Workspace"),
        workspaces[0] if workspaces else None,
    )
    if default_workspace is None:
        return {"workspaces": [], "tags": [], "triggers": [], "variables": []}

    workspace_path = default_workspace["path"]
    return {
        "workspace": default_workspace,
        "tags": list_tags(gtm, workspace_path),
        "triggers": list_triggers(gtm, workspace_path),
        "variables": list_variables(gtm, workspace_path),
    }
