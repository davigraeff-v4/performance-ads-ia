"""Google Tag Manager API client using a local OAuth installed-app flow.

Credentials never live in this repo: the OAuth client secret path and the
cached user token path are read from environment variables (see config.py),
and both are expected to point outside version control (see .gitignore).
"""

from __future__ import annotations

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build

from .config import Settings

_READONLY_SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.readonly",
]
# Draft-only editing of tags/triggers/variables inside a workspace. This
# scope alone cannot create a container version or make anything live.
_EDIT_SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
]
# Deliberately never requested or referenced anywhere else in this package.
# Publishing a GTM version pushes changes live on the client's site, and this
# integration does not support that yet: it requires its own capability,
# allowlist, and CONTRATO-OPERACIONAL.md gate before it can exist.
_PUBLISH_SCOPE = "https://www.googleapis.com/auth/tagmanager.publish"


def _scopes_for(settings: Settings) -> list[str]:
    if settings.write_mode == "disabled":
        return _READONLY_SCOPES
    return _READONLY_SCOPES + _EDIT_SCOPES


def _load_credentials(settings: Settings, scopes: list[str]) -> Credentials:
    token_path = settings.token_cache_path
    credentials: Credentials | None = None

    if token_path.is_file():
        credentials = Credentials.from_authorized_user_file(str(token_path), scopes)
        granted = set(credentials.scopes or [])
        if not set(scopes).issubset(granted):
            # Cached token predates a scope change (e.g. edit was just
            # enabled) — force a fresh consent instead of failing later
            # with an opaque 403 from the API.
            credentials = None

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials or not credentials.valid:
        assert _PUBLISH_SCOPE not in scopes, "publish scope must never be requested"
        flow = InstalledAppFlow.from_client_secrets_file(
            str(settings.credentials_path), scopes
        )
        credentials = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(credentials.to_json())

    return credentials


def get_gtm_client(settings: Settings | None = None) -> Resource:
    settings = settings or Settings.from_environment()
    scopes = _scopes_for(settings)
    credentials = _load_credentials(settings, scopes)
    return build("tagmanager", "v2", credentials=credentials, cache_discovery=False)
