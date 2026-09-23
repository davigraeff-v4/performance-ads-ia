#!/usr/bin/env python3
"""Resumo do cliente para o começo de qualquer conversa.

Gerado na hora (nada é gravado), a partir de:

- `clients/{slug}/CLIENTE.md`: o perfil, compacto (algumas linhas por seção);
- dossiês legados e V2: operações em aberto, avaliações vencidas, decisões
  pendentes e as últimas operações;
- `clients/{slug}/APRENDIZADOS.md`: as regras duráveis do cliente, inteiras.

Enquanto a ficha não é migrada, o histórico ainda mora no CLIENTE.md: o resumo
mostra as primeiras linhas dele e avisa.

Uso:
    python3 scripts/client_brief.py castelo-oleos
    python3 scripts/client_brief.py castelo-oleos --today 2026-10-02 --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import client_history  # noqa: E402
import dossier  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLIENTS_DIR = ROOT / "clients"
PROFILE_LINES_PER_SECTION = 6
LEGACY_HISTORY_LINES = 8
RECENT_OPERATIONS = 5
HISTORY_HEADING = re.compile(r"^hist", re.I)


@dataclass
class Section:
    title: str
    lines: list[str] = field(default_factory=list)


def parse_sections(markdown: str) -> tuple[str, list[Section]]:
    """Divide o Markdown pelos títulos de nível 2; subtítulos ficam no corpo."""
    title = ""
    sections: list[Section] = []
    for line in markdown.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## "):
            sections.append(Section(line[3:].strip()))
        elif sections and line.strip() and not line.startswith(">"):
            sections[-1].lines.append(line.rstrip())
    return title, sections


def compact(section: Section, limit: int) -> list[str]:
    shown = section.lines[:limit]
    hidden = len(section.lines) - len(shown)
    if hidden > 0:
        shown = shown + [f"  (+{hidden} linhas no arquivo)"]
    return shown


def drop_empty_sections(markdown: str) -> str:
    """Remove subtítulos sem conteúdo (seções do molde ainda não preenchidas)."""
    blocks = re.split(r"(?m)^(?=## )", markdown)
    kept = [block for block in blocks if not block.startswith("## ") or block.split("\n", 1)[1:] and block.split("\n", 1)[1].strip()]
    return "".join(kept).strip()


def brief(clients_dir: Path, slug: str, today: date) -> dict:
    base = client_history.client_dir(clients_dir, slug)
    profile_path = base / "CLIENTE.md"
    if not profile_path.is_file():
        raise SystemExit(f"ERRO: {slug} não tem CLIENTE.md; cadastre o cliente antes (/novo-cliente)")
    title, sections = parse_sections(profile_path.read_text(encoding="utf-8"))
    profile = [s for s in sections if not HISTORY_HEADING.match(s.title)]
    legacy_history = next((s for s in sections if HISTORY_HEADING.match(s.title)), None)

    entries = client_history.collect(clients_dir, slug)
    v2_rows = dossier.list_rows(clients_dir, slug, open_only=False, today=today)
    v2_by_path = {Path(row["path"]).name: row for row in v2_rows}

    open_ops, overdue, decisions = [], [], []
    for entry in entries:
        row = v2_by_path.get(entry.path.name) if entry.kind == "v2" else None
        pending_eval = bool(row and row["note"])
        if entry.status in client_history.OPEN_STATUSES or pending_eval:
            open_ops.append({"entry": entry, "note": row["note"] if row else ""})
        if row and row["evaluation_overdue"]:
            overdue.append(entry)
        if row:
            decisions += [(entry, decision) for decision in row["pending_decisions"]]

    learnings_path = base / "APRENDIZADOS.md"
    learnings = learnings_path.read_text(encoding="utf-8").strip() if learnings_path.is_file() else None

    return {
        "slug": slug,
        "title": title or slug,
        "today": today.isoformat(),
        "profile": [{"title": s.title, "lines": compact(s, PROFILE_LINES_PER_SECTION)} for s in profile],
        "open": [
            {"line": client_history.format_entry(item["entry"], clients_dir).splitlines()[0], "note": item["note"],
             "kind": item["entry"].kind}
            for item in open_ops
        ],
        "overdue_evaluations": [client_history.format_entry(e, clients_dir).splitlines()[0] for e in overdue],
        "pending_decisions": [{"operation": e.title, "decision": d} for e, d in decisions],
        "recent": [client_history.format_entry(e, clients_dir).splitlines()[0] for e in entries[:RECENT_OPERATIONS]],
        "operation_count": len(entries),
        "learnings": learnings,
        "legacy_history": compact(legacy_history, LEGACY_HISTORY_LINES) if legacy_history and legacy_history.lines else [],
    }


def print_brief(data: dict) -> None:
    today = date.fromisoformat(data["today"])
    print(f"# Resumo — {data['title'].removeprefix('Cliente — ')} (gerado em {today:%d/%m/%Y})")

    print("\n## Perfil (CLIENTE.md, compacto)")
    for section in data["profile"]:
        print(f"\n### {section['title']}")
        for line in section["lines"]:
            print(line)

    print("\n## Em aberto")
    if not data["open"] and not data["pending_decisions"]:
        print("Nada em aberto.")
    for item in data["open"]:
        note = f" — {item['note']}" if item["note"] else ""
        legacy = " (dossiê antigo: para seguir com ela, migrar antes)" if item["kind"] == "legado" else ""
        print(f"- {item['line']}{note}{legacy}")
    if data["overdue_evaluations"]:
        print("\nAvaliações vencidas (propor a avaliação ao gestor):")
        for line in data["overdue_evaluations"]:
            print(f"- {line}")
    if data["pending_decisions"]:
        print("\nDecisões pendentes do gestor:")
        for item in data["pending_decisions"]:
            print(f"- {item['decision']} (em “{item['operation']}”)")

    print(f"\n## Últimas operações ({min(RECENT_OPERATIONS, data['operation_count'])} de {data['operation_count']})")
    for line in data["recent"] or ["Nenhuma operação registrada."]:
        print(f"- {line}")

    print("\n## Aprendizados")
    if data["learnings"]:
        body = data["learnings"].split("\n", 1)[1].strip() if data["learnings"].startswith("# ") else data["learnings"]
        print(drop_empty_sections(body))
    else:
        print("Sem APRENDIZADOS.md ainda.")
        if data["legacy_history"]:
            print("O histórico ainda está no CLIENTE.md (seção de histórico); as linhas mais recentes:")
            for line in data["legacy_history"]:
                print(line)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug")
    parser.add_argument("--clients-dir", default=str(DEFAULT_CLIENTS_DIR))
    parser.add_argument("--today", help="data de referência (AAAA-MM-DD) para avaliações vencidas")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    today = date.fromisoformat(args.today) if args.today else datetime.now(dossier.TZ).date()
    data = brief(Path(args.clients_dir), args.slug, today)
    if args.as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_brief(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
