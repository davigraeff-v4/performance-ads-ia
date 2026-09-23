"""Runtime capability gates without exposing credential values."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


_KNOWN_CAPABILITIES = frozenset({"reporting", "tag_management"})
_KNOWN_WRITE_MODES = frozenset({"disabled", "validate_only", "execute"})


class ConfigurationError(ValueError):
    """Raised when local capability configuration is unsafe or inconsistent."""


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
    """Local runtime policy; credentials remain in environment/local files."""

    declared_capabilities: frozenset[str]
    allowed_container_ids: frozenset[str]
    write_mode: str
    credentials_path: Path
    token_cache_path: Path

    @classmethod
    def from_environment(cls, base_dir: Path | None = None) -> "Settings":
        """Lê a política local. Caminhos relativos resolvem a partir de
        ``base_dir`` (os scripts passam a raiz do projeto), nunca do diretório
        de onde o comando foi chamado."""
        base = base_dir or Path.cwd()

        def resolve(value: str) -> Path:
            path = Path(value).expanduser()
            return path if path.is_absolute() else base / path

        declared = _csv("PERFORMANCE_ADS_GTM_DECLARED_CAPABILITIES") or frozenset(
            {"reporting"}
        )
        unknown = declared - _KNOWN_CAPABILITIES
        if unknown:
            raise ConfigurationError(
                "capabilities desconhecidas: " + ", ".join(sorted(unknown))
            )

        allowed_containers = _csv("PERFORMANCE_ADS_GTM_ALLOWED_CONTAINER_IDS")

        write_mode = os.environ.get("PERFORMANCE_ADS_GTM_WRITE_MODE", "disabled").strip()
        if write_mode not in _KNOWN_WRITE_MODES:
            raise ConfigurationError(
                "PERFORMANCE_ADS_GTM_WRITE_MODE deve ser disabled, "
                "validate_only ou execute"
            )
        if write_mode != "disabled" and "tag_management" not in declared:
            raise ConfigurationError(
                "escrita requer capability declarada tag_management"
            )
        if write_mode != "disabled" and not allowed_containers:
            raise ConfigurationError(
                "escrita requer allowlist de containers configurada"
            )

        credentials_value = os.environ.get("PERFORMANCE_ADS_GTM_CREDENTIALS_PATH")
        if not credentials_value:
            raise ConfigurationError(
                "PERFORMANCE_ADS_GTM_CREDENTIALS_PATH nao configurado"
            )
        credentials_path = resolve(credentials_value)
        if not credentials_path.is_file():
            raise ConfigurationError(
                f"arquivo de credencial OAuth nao encontrado: {credentials_path}"
            )

        token_cache_value = os.environ.get(
            "PERFORMANCE_ADS_GTM_TOKEN_CACHE_PATH",
            str(Path("credentials") / "gtm-oauth-token.json"),
        )
        token_cache_path = resolve(token_cache_value)

        return cls(
            declared_capabilities=declared,
            allowed_container_ids=allowed_containers,
            write_mode=write_mode,
            credentials_path=credentials_path,
            token_cache_path=token_cache_path,
        )

    def require_container(self, container_id: str) -> str:
        normalized = container_id.strip()
        if not normalized:
            raise ConfigurationError("container_id vazio")
        if not self.allowed_container_ids:
            raise ConfigurationError(
                "nenhum container autorizado localmente; configure a allowlist"
            )
        if normalized not in self.allowed_container_ids:
            raise ConfigurationError("container_id fora da allowlist local")
        return normalized

    def require_write_enabled(self) -> None:
        """Bloqueia escrita quando desabilitada. Em ``validate_only`` a
        chamada segue até write.py, que devolve o que seria enviado sem
        gravar nada."""
        if self.write_mode == "disabled":
            raise ConfigurationError(
                "escrita GTM desabilitada localmente "
                "(PERFORMANCE_ADS_GTM_WRITE_MODE=disabled)"
            )

    def public_capabilities(self) -> dict[str, object]:
        """Non-secret summary safe to print or log."""

        return {
            "declared_capabilities": sorted(self.declared_capabilities),
            "write_mode": self.write_mode,
            "allowed_container_count": len(self.allowed_container_ids),
            "credentials_configured": self.credentials_path.is_file(),
        }
