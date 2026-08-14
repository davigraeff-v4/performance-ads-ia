#!/usr/bin/env python3
"""Auditoria somente-leitura de containers do Google Tag Manager.

Uso:
  python3 scripts/gtm_audit.py --list-accounts
  python3 scripts/gtm_audit.py --account-path accounts/123 --list-containers
  python3 scripts/gtm_audit.py --container-path accounts/123/containers/456 --snapshot

Requer as variaveis de ambiente descritas em .env.example (nenhuma credencial
e lida deste script; tudo vem de PERFORMANCE_ADS_GTM_* apontando para
arquivos locais fora do Git).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "integrations" / "gtm" / "src"))

from performance_ads_gtm import audit  # noqa: E402
from performance_ads_gtm.client import get_gtm_client  # noqa: E402
from performance_ads_gtm.config import ConfigurationError, Settings  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-accounts", action="store_true")
    parser.add_argument("--account-path", help="ex: accounts/123")
    parser.add_argument("--list-containers", action="store_true")
    parser.add_argument("--container-path", help="ex: accounts/123/containers/456")
    parser.add_argument("--snapshot", action="store_true")
    args = parser.parse_args()

    try:
        settings = Settings.from_environment()
    except ConfigurationError as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1

    gtm = get_gtm_client(settings)

    if args.list_accounts:
        result = audit.list_accounts(gtm)
    elif args.list_containers:
        if not args.account_path:
            parser.error("--list-containers requer --account-path")
        result = audit.list_containers(gtm, args.account_path)
    elif args.snapshot:
        if not args.container_path:
            parser.error("--snapshot requer --container-path")
        if settings.allowed_container_ids:
            container_id = args.container_path.rsplit("/", 1)[-1]
            settings.require_container(container_id)
        result = audit.snapshot_container(gtm, args.container_path)
    else:
        parser.error("informe --list-accounts, --list-containers ou --snapshot")
        return 2

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
