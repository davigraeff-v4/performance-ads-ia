#!/usr/bin/env python3
"""Cria ou atualiza tags/triggers/variaveis em um workspace GTM (rascunho).

NUNCA publica. Nao existe flag de publicacao neste script nem em
integrations/gtm: a mudanca fica no workspace ate um humano publicar
manualmente pela UI do GTM.

Uso:
  python3 scripts/gtm_edit.py --container-id 456 \
    --resource tag --action create \
    --workspace-path accounts/123/containers/456/workspaces/1 \
    --body-file change.json

  python3 scripts/gtm_edit.py --container-id 456 \
    --resource trigger --action update \
    --path accounts/123/containers/456/workspaces/1/triggers/9 \
    --body-file change.json

Requer PERFORMANCE_ADS_GTM_WRITE_MODE != disabled, capability
tag_management declarada e o container na allowlist local (ver
.env.example). Pensado para ser chamado pela skill so depois de
/aprovar-operacao, com o change set ja registrado no dossie.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "integrations" / "gtm" / "src"))

from performance_ads_gtm import write  # noqa: E402
from performance_ads_gtm.client import get_gtm_client  # noqa: E402
from performance_ads_gtm.config import ConfigurationError, Settings  # noqa: E402

_ACTIONS = {
    ("tag", "create"): lambda gtm, settings, cid, args, body: write.create_tag(
        gtm, settings, cid, args.workspace_path, body
    ),
    ("tag", "update"): lambda gtm, settings, cid, args, body: write.update_tag(
        gtm, settings, cid, args.path, body
    ),
    ("trigger", "create"): lambda gtm, settings, cid, args, body: write.create_trigger(
        gtm, settings, cid, args.workspace_path, body
    ),
    ("trigger", "update"): lambda gtm, settings, cid, args, body: write.update_trigger(
        gtm, settings, cid, args.path, body
    ),
    ("variable", "create"): lambda gtm, settings, cid, args, body: write.create_variable(
        gtm, settings, cid, args.workspace_path, body
    ),
    ("variable", "update"): lambda gtm, settings, cid, args, body: write.update_variable(
        gtm, settings, cid, args.path, body
    ),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--container-id", required=True)
    parser.add_argument("--resource", choices=["tag", "trigger", "variable"], required=True)
    parser.add_argument("--action", choices=["create", "update"], required=True)
    parser.add_argument("--workspace-path", help="obrigatorio para --action create")
    parser.add_argument("--path", help="obrigatorio para --action update")
    parser.add_argument("--body-file", required=True, help="JSON do recurso GTM")
    args = parser.parse_args()

    if args.action == "create" and not args.workspace_path:
        parser.error("--action create requer --workspace-path")
    if args.action == "update" and not args.path:
        parser.error("--action update requer --path")

    try:
        settings = Settings.from_environment(base_dir=ROOT)
    except ConfigurationError as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1

    body = json.loads(Path(args.body_file).read_text())
    gtm = get_gtm_client(settings)

    handler = _ACTIONS[(args.resource, args.action)]
    try:
        result = handler(gtm, settings, args.container_id, args, body)
    except ConfigurationError as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
