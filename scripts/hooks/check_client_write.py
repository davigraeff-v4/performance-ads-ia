#!/usr/bin/env python3
"""Hook PreToolUse (Write/Edit/MultiEdit) do Claude Code para `clients/`.

Bloqueia, antes da gravação:
- qualquer escrita direta em `clients/{slug}/operacoes/`: esses arquivos só
  são criados e atualizados por `scripts/dossier.py`, que calcula hashes e
  status e regenera a narrativa;
- edição de dossiês legados (`clients/{slug}/AAAA-MM-DD-*.md`): são base de
  consulta somente leitura;
- criação de dossiê novo na raiz da pasta do cliente, fora do fluxo V2.

`CLIENTE.md` e os demais arquivos do cliente continuam livres. Saída 2 bloqueia
a ferramenta e devolve a mensagem ao agent.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLIENTS = ROOT / "clients"
DOSSIER_NAME = re.compile(r"^20\d{2}-\d{2}-\d{2}.*\.md$")


def nfc(path: Path) -> str:
    return unicodedata.normalize("NFC", str(path))


def block(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(2)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    tool_input = payload.get("tool_input") or {}
    raw_path = tool_input.get("file_path")
    if not raw_path:
        return 0
    path = Path(raw_path)
    if not path.is_absolute():
        path = Path(payload.get("cwd") or ROOT) / path
    # macOS devolve caminhos com acento ora compostos (NFC), ora decompostos
    # (NFD) — a pasta do projeto tem "Tráfego" no nome. Comparar sempre em NFC.
    try:
        relative = Path(nfc(path.resolve())).relative_to(nfc(CLIENTS.resolve()))
    except ValueError:
        return 0
    parts = relative.parts
    if len(parts) >= 3 and parts[1] == "operacoes":
        block(
            "Bloqueado: arquivos em clients/*/operacoes/ só podem ser criados ou alterados por "
            "scripts/dossier.py (new, revise, approve, record-execution, evaluate, render). "
            "Prepare spec e corpo em .work/ e rode o comando correspondente."
        )
    if len(parts) == 2 and DOSSIER_NAME.match(parts[1]):
        if path.exists():
            block(
                "Bloqueado: dossiês legados são base de consulta somente leitura. Para seguir com uma "
                "operação legada aberta, use `python3 scripts/dossier.py migrate <arquivo>` e registre a "
                "versão nova com `dossier.py new`."
            )
        block(
            "Bloqueado: dossiê novo não é escrito à mão na raiz do cliente. Registre com "
            "`python3 scripts/dossier.py new --client <slug> --spec .work/<nome>.spec.json --body .work/<nome>.body.md`."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
