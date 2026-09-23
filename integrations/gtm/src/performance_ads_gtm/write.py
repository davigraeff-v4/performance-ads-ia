"""Create/update operations over a GTM workspace (draft, never published).

Every function here writes to a *workspace* — GTM's draft area. Nothing
becomes live on the client's site until a human explicitly creates a
container version and publishes it from the GTM UI (or a future, separately
gated integration). This module intentionally has no publish/version
function: PERFORMANCE ADS IA does not publish GTM changes.

Gates applied to every call:

- write mode must not be ``disabled``;
- the declared ``container_id`` must be in the local allowlist, and the
  container embedded in the resource path must be that same container (a
  path from another container never slips through the allowlist);
- in ``validate_only`` mode nothing is written: the call returns what would
  be sent (reading the current resource is allowed, it is read-only);
- updates read the current resource, merge the requested fields over it and
  send the resource ``fingerprint``, so a partial body never wipes fields and
  a concurrent edit in the GTM UI is rejected instead of overwritten.
"""

from __future__ import annotations

import re
from typing import Any

from googleapiclient.discovery import Resource

from .config import ConfigurationError, Settings

_RESOURCE_PATH = re.compile(
    r"^accounts/(?P<account>\d+)/containers/(?P<container>\d+)/workspaces/(?P<workspace>\d+)(?:/.+)?$"
)


def _container_from_path(resource_path: str) -> str:
    match = _RESOURCE_PATH.match(resource_path.strip())
    if not match:
        raise ConfigurationError(
            "caminho GTM inválido; esperado accounts/{id}/containers/{id}/workspaces/{id}[/...]"
        )
    return match.group("container")


def _guard(settings: Settings, container_id: str, resource_path: str) -> None:
    settings.require_write_enabled()
    authorized = settings.require_container(container_id)
    in_path = _container_from_path(resource_path)
    if in_path != authorized:
        raise ConfigurationError(
            f"o caminho aponta para o container {in_path}, não para o container autorizado {authorized}"
        )


def _collection(gtm: Resource, kind: str) -> Any:
    workspaces = gtm.accounts().containers().workspaces()
    return getattr(workspaces, kind)()


def _create(
    gtm: Resource,
    settings: Settings,
    container_id: str,
    workspace_path: str,
    body: dict[str, Any],
    kind: str,
) -> dict[str, Any]:
    _guard(settings, container_id, workspace_path)
    if settings.write_mode == "validate_only":
        return {"validate_only": True, "operation": f"{kind}.create", "parent": workspace_path, "body": body}
    return _collection(gtm, kind).create(parent=workspace_path, body=body).execute()


def _update(
    gtm: Resource,
    settings: Settings,
    container_id: str,
    resource_path: str,
    body: dict[str, Any],
    kind: str,
) -> dict[str, Any]:
    _guard(settings, container_id, resource_path)
    collection = _collection(gtm, kind)
    current = collection.get(path=resource_path).execute()
    merged = {**current, **body}
    if settings.write_mode == "validate_only":
        return {
            "validate_only": True,
            "operation": f"{kind}.update",
            "path": resource_path,
            "current": current,
            "proposed": merged,
        }
    return collection.update(
        path=resource_path, body=merged, fingerprint=current.get("fingerprint")
    ).execute()


def create_tag(
    gtm: Resource, settings: Settings, container_id: str, workspace_path: str, tag_body: dict[str, Any]
) -> dict[str, Any]:
    return _create(gtm, settings, container_id, workspace_path, tag_body, "tags")


def update_tag(
    gtm: Resource, settings: Settings, container_id: str, tag_path: str, tag_body: dict[str, Any]
) -> dict[str, Any]:
    return _update(gtm, settings, container_id, tag_path, tag_body, "tags")


def create_trigger(
    gtm: Resource, settings: Settings, container_id: str, workspace_path: str, trigger_body: dict[str, Any]
) -> dict[str, Any]:
    return _create(gtm, settings, container_id, workspace_path, trigger_body, "triggers")


def update_trigger(
    gtm: Resource, settings: Settings, container_id: str, trigger_path: str, trigger_body: dict[str, Any]
) -> dict[str, Any]:
    return _update(gtm, settings, container_id, trigger_path, trigger_body, "triggers")


def create_variable(
    gtm: Resource, settings: Settings, container_id: str, workspace_path: str, variable_body: dict[str, Any]
) -> dict[str, Any]:
    return _create(gtm, settings, container_id, workspace_path, variable_body, "variables")


def update_variable(
    gtm: Resource, settings: Settings, container_id: str, variable_path: str, variable_body: dict[str, Any]
) -> dict[str, Any]:
    return _update(gtm, settings, container_id, variable_path, variable_body, "variables")
