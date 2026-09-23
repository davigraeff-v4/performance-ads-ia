#!/usr/bin/env python3
"""Migra a ficha de um cliente para a separação perfil / aprendizados / histórico.

Antes: `CLIENTE.md` mistura o perfil estável com uma seção longa de histórico
e aprendizados escrita à mão, em ordem variada.

Depois:

- `CLIENTE.md`: só o perfil (todas as seções, menos a de histórico), mais uma
  seção curta "Onde está o resto";
- `HISTORICO-ANTERIOR.md`: a seção de histórico antiga, **sem nenhuma
  alteração**, como registro somente leitura (pesquisável por
  `client_history.py search`);
- `APRENDIZADOS.md`: as regras duráveis. O script não decide o que é regra:
  o conteúdo vem de `--learnings` (um rascunho revisado e aprovado pelo
  gestor) ou, sem ele, do molde vazio.

Sem `--apply`, só mostra o que faria. Com `--apply`, grava uma cópia
`CLIENTE.md.bak-AAAAMMDDHHMM` antes de qualquer escrita e recusa sobrescrever
`APRENDIZADOS.md` ou `HISTORICO-ANTERIOR.md` existentes. Um cliente por vez.

Uso:
    python3 scripts/migrate_client_profile.py castelo-oleos
    python3 scripts/migrate_client_profile.py castelo-oleos --learnings .work/castelo-oleos-aprendizados.md --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import client_history  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLIENTS_DIR = ROOT / "clients"
LEARNINGS_TEMPLATE = ROOT / "templates" / "aprendizados-template.md"
HISTORY_HEADING = re.compile(r"^## +hist", re.I)
POINTER_TITLE = "## Onde está o resto"


def split_profile(markdown: str) -> tuple[str, str]:
    """Separa a seção de histórico (título '## Hist…' até o próximo '## ') do resto."""
    lines = markdown.splitlines()
    start = next((i for i, line in enumerate(lines) if HISTORY_HEADING.match(line)), None)
    if start is None:
        return markdown, ""
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    profile = lines[:start] + lines[end:]
    history = lines[start:end]
    return "\n".join(profile).rstrip() + "\n", "\n".join(history).rstrip() + "\n"


def pointer_section(slug: str, migrated_on: str) -> str:
    return (
        f"\n{POINTER_TITLE}\n\n"
        "Esta ficha guarda só o perfil estável. O resto:\n\n"
        "- **Regras duráveis:** `APRENDIZADOS.md`.\n"
        f"- **Histórico de operações:** nos dossiês, lido por `python3 scripts/client_brief.py {slug}`.\n"
        f"- **Histórico escrito à mão até {migrated_on}:** `HISTORICO-ANTERIOR.md` (somente leitura).\n"
    )


def learnings_text(name: str, learnings: Path | None) -> str:
    if learnings:
        return learnings.read_text(encoding="utf-8").rstrip() + "\n"
    return LEARNINGS_TEMPLATE.read_text(encoding="utf-8").replace("{nome}", name).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug")
    parser.add_argument("--clients-dir", default=str(DEFAULT_CLIENTS_DIR))
    parser.add_argument("--learnings", type=Path, help="rascunho aprovado de APRENDIZADOS.md")
    parser.add_argument("--apply", action="store_true", help="grava (sem isso, só simula)")
    parser.add_argument("--now", help="data e hora de referência (AAAA-MM-DDTHH:MM), para testes")
    args = parser.parse_args(argv)

    clients_dir = Path(args.clients_dir)
    base = client_history.client_dir(clients_dir, args.slug)
    profile_path = base / "CLIENTE.md"
    if not profile_path.is_file():
        raise SystemExit(f"ERRO: {args.slug} não tem CLIENTE.md")
    original = profile_path.read_text(encoding="utf-8")
    if POINTER_TITLE in original:
        print(f"{args.slug}: ficha já migrada; nada a fazer.")
        return 0
    if args.learnings and not args.learnings.is_file():
        raise SystemExit(f"ERRO: rascunho de aprendizados não encontrado: {args.learnings}")

    now = datetime.fromisoformat(args.now) if args.now else datetime.now()
    profile, history = split_profile(original)
    name = next((line[2:].strip() for line in original.splitlines() if line.startswith("# ")), args.slug)
    name = name.removeprefix("Cliente — ").strip()
    new_profile = profile.rstrip() + "\n" + pointer_section(args.slug, now.strftime("%d/%m/%Y"))
    learnings_path = base / "APRENDIZADOS.md"
    history_path = base / "HISTORICO-ANTERIOR.md"
    backup_path = base / f"CLIENTE.md.bak-{now:%Y%m%d%H%M}"

    conflicts = [path.name for path in (learnings_path, history_path, backup_path) if path.exists()]
    history_lines = len([line for line in history.splitlines() if line.strip()])
    print(f"Cliente: {name} ({args.slug})")
    print(f"- CLIENTE.md: {len(original.splitlines())} → {len(new_profile.splitlines())} linhas "
          f"({len(original.encode())} → {len(new_profile.encode())} bytes)")
    print(f"- HISTORICO-ANTERIOR.md: {history_lines} linhas da seção de histórico, copiadas sem alteração"
          if history else "- sem seção de histórico: HISTORICO-ANTERIOR.md não será criado")
    print(f"- APRENDIZADOS.md: {'rascunho ' + str(args.learnings) if args.learnings else 'molde vazio'}")
    print(f"- cópia de segurança: {backup_path.name}")

    if conflicts:
        print(f"RECUSADO: já existem {', '.join(conflicts)}; confira antes de migrar.")
        return 1
    if not args.apply:
        print("Simulação: nada foi gravado. Rode com --apply depois da aprovação do gestor.")
        return 0

    backup_path.write_text(original, encoding="utf-8")
    if history:
        header = (f"# Histórico anterior — {name}\n\n"
                  f"> Seção de histórico do CLIENTE.md até {now:%d/%m/%Y}, copiada sem alteração. "
                  "Somente leitura: o histórico novo vem dos dossiês.\n\n")
        history_path.write_text(header + history, encoding="utf-8")
    learnings_path.write_text(learnings_text(name, args.learnings), encoding="utf-8")
    profile_path.write_text(new_profile, encoding="utf-8")
    print("Gravado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
