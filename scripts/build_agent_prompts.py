#!/usr/bin/env python3
"""Gera CLAUDE.md e AGENTS.md a partir da fonte única prompt/agent-prompt.md.

Blocos `<!-- somente:claude -->…<!-- /somente -->` e
`<!-- somente:codex -->…<!-- /somente -->` entram só no arquivo do cliente
correspondente. Use --check na homologação para falhar se alguém editar os
arquivos gerados diretamente.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "prompt" / "agent-prompt.md"
TARGETS = {"claude": ROOT / "CLAUDE.md", "codex": ROOT / "AGENTS.md"}
BLOCK = re.compile(r"<!-- somente:(?P<who>[a-z]+) -->\n(?P<body>.*?)<!-- /somente -->\n?", re.S)
HEADER = (
    "<!-- Gerado por scripts/build_agent_prompts.py a partir de prompt/agent-prompt.md. "
    "Edite a fonte e rode o script; não edite este arquivo. -->\n\n"
)


def render(source: str, who: str) -> str:
    def keep(match: re.Match[str]) -> str:
        return match.group("body") if match.group("who") == who else ""

    return HEADER + BLOCK.sub(keep, source)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="só confere se os arquivos estão atualizados")
    args = parser.parse_args()
    source = SOURCE.read_text(encoding="utf-8")
    stale = []
    for who, target in TARGETS.items():
        expected = render(source, who)
        current = target.read_text(encoding="utf-8") if target.is_file() else ""
        if current == expected:
            continue
        if args.check:
            stale.append(target.name)
        else:
            target.write_text(expected, encoding="utf-8")
            print(f"gerado: {target.name}")
    if stale:
        print(f"DESATUALIZADO: {', '.join(stale)} (rode python3 scripts/build_agent_prompts.py)")
        return 1
    if args.check:
        print("PROMPTS OK: CLAUDE.md e AGENTS.md batem com prompt/agent-prompt.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
