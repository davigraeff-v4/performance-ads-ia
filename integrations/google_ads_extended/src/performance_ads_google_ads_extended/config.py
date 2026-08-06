"""Runtime capability gates without exposing credential values."""

from __future__ import annotations

from dataclasses import dataclass
import os
import re
from pathlib import Path


_CUSTOMER_ID = re.compile(r"^[0-9]{6,12}$")
_KNOWN_CAPABILITIES = frozenset({"reporting", "keyword_planning", "ad_management"})
_KNOWN_WRITE_MODES = frozenset({"disabled", "validate_only", "execute"})


class ConfigurationError(ValueError):
    """Raised when local capability configuration is unsafe or inconsistent."""


def normalize_customer_id(value: str) -> str:
    """Return a digits-only Google Ads customer ID or fail closed."""

    normalized = value.replace("-", "").strip()
    if not _CUSTOMER_ID.fullmatch(normalized):
        raise ConfigurationError("customer_id deve conter somente 6 a 12 digitos")
    return normalized


def _enabled(name: str) -> bool:
    value = os.environ.get(name, "false").strip().casefold()
    if value not in {"true", "false"}:
        raise ConfigurationError(f"{name} deve ser true ou false")
    return value == "true"


def _csv(name: str) -> frozenset[str]:
    return frozenset(
        item.strip() for item in os.environ.get(name, "").split(",") if item.strip()
    )


@dataclass(frozen=True)
class Settings:
    """Local runtime policy; credentials remain in environment/ADC."""

    declared_capabilities: frozenset[str]
    allowed_customer_ids: frozenset[str]
    planner_enabled: bool
    write_mode: str

    @classmethod
    def from_environment(cls) -> "Settings":
        declared = _csv("PERFORMANCE_ADS_GOOGLE_DECLARED_CAPABILITIES") or frozenset(
            {"reporting"}
        )
        unknown = declared - _KNOWN_CAPABILITIES
        if unknown:
            raise ConfigurationError(
                "capabilities desconhecidas: " + ", ".join(sorted(unknown))
            )

        allowed = frozenset(
            normalize_customer_id(item)
            for item in _csv("PERFORMANCE_ADS_GOOGLE_ALLOWED_CUSTOMER_IDS")
        )
        write_mode = os.environ.get(
            "PERFORMANCE_ADS_GOOGLE_WRITE_MODE", "disabled"
        ).strip()
        if write_mode not in _KNOWN_WRITE_MODES:
            raise ConfigurationError(
                "PERFORMANCE_ADS_GOOGLE_WRITE_MODE deve ser disabled, "
                "validate_only ou execute"
            )

        planner_enabled = _enabled("PERFORMANCE_ADS_GOOGLE_PLANNER_ENABLED")
        if planner_enabled and "keyword_planning" not in declared:
            raise ConfigurationError(
                "Keyword Planner requer capability declarada keyword_planning"
            )
        if write_mode != "disabled" and "ad_management" not in declared:
            raise ConfigurationError(
                "escrita requer capability declarada ad_management"
            )

        return cls(
            declared_capabilities=declared,
            allowed_customer_ids=allowed,
            planner_enabled=planner_enabled,
            write_mode=write_mode,
        )

    def require_customer(self, customer_id: str) -> str:
        normalized = normalize_customer_id(customer_id)
        if not self.allowed_customer_ids:
            raise ConfigurationError(
                "nenhum customer autorizado localmente; configure a allowlist"
            )
        if normalized not in self.allowed_customer_ids:
            raise ConfigurationError("customer_id fora da allowlist local")
        return normalized

    def require_planner(self, customer_id: str) -> str:
        if not self.planner_enabled:
            raise ConfigurationError(
                "Keyword Planner bloqueado localmente; uso permitido ainda nao homologado"
            )
        if "keyword_planning" not in self.declared_capabilities:
            raise ConfigurationError("capability keyword_planning nao declarada")
        return self.require_customer(customer_id)

    def public_capabilities(self) -> dict[str, object]:
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        credentials_present = bool(
            credentials_path and Path(credentials_path).expanduser().is_file()
        )
        return {
            "declared_capabilities": sorted(self.declared_capabilities),
            "planner_enabled": self.planner_enabled,
            "write_mode": self.write_mode,
            "write_tools_registered": False,
            "allowed_customer_count": len(self.allowed_customer_ids),
            "developer_token_present": bool(
                os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN")
            ),
            "credentials_file_present": credentials_present,
            "login_customer_present": bool(
                os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
            ),
        }
