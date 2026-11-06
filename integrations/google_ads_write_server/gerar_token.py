#!/usr/bin/env python3
"""Gera o token OAuth (refresh_token) do Google Ads, uma vez, fora do Claude.

Rode com o Python do ambiente do servidor:
    ~/.mcp/google-ads/.venv/bin/python gerar_token.py --client-secrets ~/Downloads/credentials.json

- Client OAuth "App para computador" (Desktop): use o padrão (--port 0, porta livre).
- Client OAuth "Aplicativo da Web": cadastre o redirect http://localhost:8085 no Google
  Cloud e rode com --port 8085, senão o Google responde redirect_uri_mismatch.

Logue com o usuário Google que tem acesso às contas (de preferência na MCC).
O arquivo sai com permissão 600. Nunca envie o conteúdo dele por chat ou e-mail.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/adwords"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--client-secrets", required=True, help="credentials.json baixado do Google Cloud")
    parser.add_argument("--port", type=int, default=0, help="0 para Desktop; a porta cadastrada para Web")
    parser.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parent / "google_ads_token.json"),
        help="onde salvar o token (padrão: ao lado deste script)",
    )
    args = parser.parse_args()

    flow = InstalledAppFlow.from_client_secrets_file(os.path.expanduser(args.client_secrets), SCOPES)
    creds = flow.run_local_server(port=args.port, redirect_uri_trailing_slash=False)
    if not creds.refresh_token:
        raise SystemExit("O Google não devolveu refresh_token. Remova o acesso do app em myaccount.google.com/permissions e tente de novo.")

    out = Path(args.out).expanduser()
    fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(creds.to_json())
    print(f"token salvo em {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
