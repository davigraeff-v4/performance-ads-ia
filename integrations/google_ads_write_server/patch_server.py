#!/usr/bin/env python3
"""Aplica os ajustes do PERFORMANCE ADS IA ao servidor cohnen/mcp-google-ads.

Uso: python3 patch_server.py <pasta do servidor>

Idempotente: pode rodar de novo sem duplicar nada. Falha (sem gravar) se o
código do servidor não tiver os trechos esperados, o que indica outra versão
do projeto original; nesse caso use o commit fixado em install.sh.
"""

from __future__ import annotations

import sys
from pathlib import Path

SERVER_PATCHES = [
    (
        'API_VERSION = "v19"  # Google Ads API version',
        'API_VERSION = os.environ.get("GOOGLE_ADS_API_VERSION", "v26")  # Google Ads API version',
    ),
    (
        "    load_dotenv()\n",
        '    load_dotenv(Path(__file__).resolve().parent / ".env")\n',
    ),
    (
        "        if creds and creds.expired and creds.refresh_token:",
        "        if creds and creds.refresh_token:",
    ),
    (
        "            # Run the OAuth flow\n",
        "            # Run the OAuth flow (só fora do MCP: dentro do Claude o navegador travaria o servidor)\n"
        '            if os.environ.get("GOOGLE_ADS_ALLOW_INTERACTIVE_LOGIN", "false").lower() != "true":\n'
        "                raise ValueError(\n"
        '                    "Token OAuth ausente ou revogado. Gere de novo fora do Claude "\n'
        '                    "com gerar_token.py (veja LEIA-ME-INSTALACAO.md)."\n'
        "                )\n",
    ),
    (
        "            if creds.expired and creds.refresh_token:\n"
        "                try:\n"
        '                    logger.info("Refreshing expired OAuth token in get_headers")',
        "            if creds.refresh_token:\n"
        "                try:\n"
        '                    logger.info("Refreshing expired OAuth token in get_headers")',
    ),
    (
        'if __name__ == "__main__":\n    # Start the MCP server on stdio transport',
        "# Ferramentas de escrita e leitura com MCC automática (write_tools.py)\n"
        "import write_tools  # noqa: E402\n"
        "\n"
        "write_tools.register(\n"
        "    mcp,\n"
        "    get_credentials=get_credentials,\n"
        "    get_headers=get_headers,\n"
        "    format_customer_id=format_customer_id,\n"
        "    api_version=API_VERSION,\n"
        ")\n"
        "\n"
        'if __name__ == "__main__":\n    # Start the MCP server on stdio transport',
    ),
]

REQUIREMENTS_PATCHES = [("mcp>=0.0.11", "mcp>=1.27,<2")]


def apply(text: str, patches: list[tuple[str, str]], name: str) -> str:
    for old, new in patches:
        if new in text:
            continue
        if text.count(old) != 1:
            raise SystemExit(
                f"{name}: trecho esperado não encontrado ({old.strip()[:60]!r}). "
                "O servidor original mudou; use o commit fixado em install.sh."
            )
        text = text.replace(old, new)
    return text


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    base = Path(sys.argv[1]).expanduser()
    server = base / "google_ads_server.py"
    requirements = base / "requirements.txt"
    patched_server = apply(server.read_text(encoding="utf-8"), SERVER_PATCHES, server.name)
    patched_requirements = apply(
        requirements.read_text(encoding="utf-8"), REQUIREMENTS_PATCHES, requirements.name
    )
    server.write_text(patched_server, encoding="utf-8")
    requirements.write_text(patched_requirements, encoding="utf-8")
    print("servidor ajustado: API v26, mcp<2, renovação de token, login interativo bloqueado, write_tools")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
