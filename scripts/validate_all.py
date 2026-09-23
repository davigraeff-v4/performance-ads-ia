#!/usr/bin/env python3
"""Executa a homologação local completa do V1 sem alterar contas externas."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTEGRATION_SRC = ROOT / "integrations" / "google_ads_extended" / "src"
GTM_SRC = ROOT / "integrations" / "gtm" / "src"


def run(label: str, command: list[str], *, env: dict[str, str] | None = None) -> None:
    print(f"[{label}]")
    result = subprocess.run(command, cwd=ROOT, env=env)
    if result.returncode:
        raise SystemExit(result.returncode)


def integration_runtime() -> str:
    installed_launcher = shutil.which("performance-ads-google-ads-extended")
    candidates: list[Path] = []
    if installed_launcher:
        first_line = Path(installed_launcher).read_text(encoding="utf-8").splitlines()[0]
        candidates.append(Path(first_line.removeprefix("#!")))
    pipx = shutil.which("pipx")
    if pipx:
        result = subprocess.run(
            [pipx, "environment", "--value", "PIPX_LOCAL_VENVS"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            candidates.append(
                Path(result.stdout.strip())
                / "performance-ads-google-ads-extended"
                / "bin"
                / "python"
            )
    # O launcher pode ser um script shell (README §15.8): só aceitar interpretadores Python.
    pythons = (candidate for candidate in candidates if candidate.is_file() and candidate.name.startswith("python"))
    return str(next(pythons, Path(sys.executable)))


def main() -> int:
    run("estrutura e contratos", [sys.executable, "scripts/validate_repository.py"])
    run("prompts CLAUDE.md e AGENTS.md sincronizados", [sys.executable, "scripts/build_agent_prompts.py", "--check"])
    run("rotas, RAG, schemas e dossiês V2", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    run("dossiês V2 dos clientes locais", [sys.executable, "scripts/dossier.py", "verify"])
    gtm_env = os.environ.copy()
    gtm_env["PYTHONPATH"] = str(GTM_SRC) + (os.pathsep + gtm_env["PYTHONPATH"] if gtm_env.get("PYTHONPATH") else "")
    run(
        "GTM: nunca publica, allowlist por caminho e validate_only",
        [sys.executable, "-m", "unittest", "discover", "-s", "integrations/gtm/tests", "-v"],
        env=gtm_env,
    )
    integration_env = os.environ.copy()
    integration_python = integration_runtime()
    if integration_python == sys.executable:
        current = integration_env.get("PYTHONPATH", "")
        integration_env["PYTHONPATH"] = str(INTEGRATION_SRC) + (os.pathsep + current if current else "")
    run(
        "conector Google Ads fail-closed",
        [integration_python, "-m", "unittest", "discover", "-s", "integrations/google_ads_extended/tests", "-v"],
        env=integration_env,
    )
    print("HOMOLOGATION OK: V2 local validado sem mutações externas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
