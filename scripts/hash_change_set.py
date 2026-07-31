#!/usr/bin/env python3
"""Calculate the approval hash for a structured operation dossier JSON."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def canonical_payload(dossier: dict) -> dict:
    return {
        "operation_id": dossier["operation_id"],
        "version": dossier["version"],
        "changes": sorted(dossier.get("changes", []), key=lambda item: item["change_id"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", type=Path)
    args = parser.parse_args()
    dossier = json.loads(args.json_file.read_text(encoding="utf-8"))
    encoded = json.dumps(
        canonical_payload(dossier), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    print(hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()

