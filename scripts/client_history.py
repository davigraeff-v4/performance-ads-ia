#!/usr/bin/env python3
"""Consulta o histórico de um cliente: dossiês legados (Markdown com JSON
embutido na raiz da pasta) e operações V2 (`operacoes/`).

Os dossiês legados são base de consulta somente leitura. Este script nunca
cruza clientes: toda consulta exige o slug e fica dentro de `clients/{slug}/`.

Uso:
  python3 scripts/client_history.py list cliente-exemplo --limit 10
  python3 scripts/client_history.py list cliente-exemplo --open
  python3 scripts/client_history.py search cliente-exemplo "remarketing orçamento unidade" --limit 5
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _help_index_common import normalize  # noqa: E402

DEFAULT_CLIENTS_DIR = ROOT / "clients"
LEGACY_NAME = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(\d{4})?-?(.*)\.md$")
LEGACY_JSON = re.compile(r"```json\s*(\{.*?\})\s*```", re.S)
OPEN_STATUSES = {"proposed", "approved", "partial_failure", "draft"}
STOPWORDS = frozenset(
    "a o as os de da do das dos e em no na nos nas para por com sem um uma que se ao aos como mais "
    "foi ser ter sobre entre ou ja nao sim cliente campanha".split()
)
STATUS_LABELS = {
    "analysis_only": "análise registrada",
    "proposed": "aguardando aprovação",
    "approved": "aprovado, sem execução registrada",
    "executed": "executado",
    "partial_failure": "executado parcialmente",
    "failed": "falhou",
    "reverted": "revertido",
    "blocked": "bloqueado",
    "evaluated": "avaliado",
    "draft": "rascunho legado",
}
# Os legados usaram vários nomes para a mesma coisa; normalizamos na leitura.
PLATFORM_ALIASES = {
    "meta": "meta",
    "google_ads": "google_ads",
    "google": "google_ads",
    "both": "multicanal",
    "cross_channel": "multicanal",
    "multicanal": "multicanal",
    "multiplataforma": "multicanal",
}
PLATFORM_LABELS = {"meta": "Meta Ads", "google_ads": "Google Ads", "multicanal": "Multicanal"}


@dataclass
class Entry:
    path: Path
    date: str
    kind: str  # "legado" ou "v2"
    status: str | None
    title: str
    platform: str | None
    type: str | None
    text: str = field(repr=False, default="")


def client_dir(clients_dir: Path, slug: str) -> Path:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        raise SystemExit("slug inválido")
    path = (clients_dir / slug).resolve()
    if not path.is_dir() or path.parent != clients_dir.resolve():
        raise SystemExit(f"cliente não encontrado: {slug}")
    return path


def human_text(markdown: str) -> str:
    """Texto legível do dossiê, sem blocos JSON e sem os dados técnicos gerados."""
    text = LEGACY_JSON.sub("", markdown)
    return re.sub(r"<details>.*?</details>", "", text, flags=re.S)


def legacy_entry(path: Path) -> Entry | None:
    match = LEGACY_NAME.match(path.name)
    if not match:
        return None
    markdown = path.read_text(encoding="utf-8", errors="ignore")
    payload: dict = {}
    json_match = LEGACY_JSON.search(markdown)
    if json_match:
        try:
            payload = json.loads(json_match.group(1))
        except json.JSONDecodeError:
            payload = {}
    heading = next((line[2:].strip() for line in markdown.splitlines() if line.startswith("# ")), path.stem)
    return Entry(
        path=path,
        date=f"{match.group(1)}-{match.group(2)}-{match.group(3)}",
        kind="legado",
        status=payload.get("status") if isinstance(payload, dict) else None,
        title=heading,
        platform=legacy_platform(payload if isinstance(payload, dict) else {}, path.name),
        type=payload.get("type") if isinstance(payload, dict) else None,
        text=human_text(markdown),
    )


def legacy_platform(payload: dict, filename: str) -> str | None:
    """Plataforma de um legado: campo do topo, depois fontes e mudanças, depois o nome do arquivo."""
    if (top := PLATFORM_ALIASES.get(str(payload.get("platform") or ""))):
        return top
    found = {
        PLATFORM_ALIASES.get(str(item.get("platform") or ""))
        for key in ("sources", "changes")
        for item in (payload.get(key) or [])
        if isinstance(item, dict)
    } - {None}
    if len(found) == 1:
        return found.pop()
    if found:
        return "multicanal"
    name_tokens = set(re.split(r"[-.]", filename))
    from_name = {PLATFORM_ALIASES[token] for token in name_tokens if token in PLATFORM_ALIASES}
    if len(from_name) == 1:
        return from_name.pop()
    return None


def v2_entry(json_path: Path) -> Entry | None:
    try:
        operation = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    md_path = json_path.with_suffix(".md")
    markdown = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""
    return Entry(
        path=md_path,
        date=operation.get("created_at", "")[:10],
        kind="v2",
        status=operation.get("status"),
        title=operation.get("title", json_path.stem),
        platform=PLATFORM_ALIASES.get(operation.get("platform") or ""),
        type=operation.get("type"),
        text=human_text(markdown),
    )


def collect(clients_dir: Path, slug: str) -> list[Entry]:
    base = client_dir(clients_dir, slug)
    entries = [entry for path in sorted(base.glob("20*.md")) if (entry := legacy_entry(path))]
    entries += [entry for path in sorted((base / "operacoes").glob("*.json")) if (entry := v2_entry(path))]
    return sorted(entries, key=lambda entry: (entry.date, entry.path.name), reverse=True)


def format_entry(entry: Entry, clients_dir: Path) -> str:
    day = "/".join(reversed(entry.date.split("-"))) if entry.date else "—"
    status = STATUS_LABELS.get(entry.status or "", entry.status or "sem status")
    platform = PLATFORM_LABELS.get(entry.platform or "", "plataforma não registrada")
    relative = entry.path.relative_to(clients_dir.resolve()) if entry.path.is_relative_to(clients_dir.resolve()) else entry.path
    return f"{day} · {platform} · {status} · {entry.title}\n    {relative} ({entry.kind})"


def tokens(value: str) -> list[str]:
    return [token for token in normalize(value).split() if len(token) > 2 and token not in STOPWORDS]


def best_snippets(text: str, query_tokens: set[str], limit: int = 2) -> list[str]:
    scored: list[tuple[int, str]] = []
    for line in text.splitlines():
        clean = line.strip(" -*#>|")
        if len(clean) < 25:
            continue
        hits = len(query_tokens & set(tokens(clean)))
        if hits:
            scored.append((hits, clean))
    scored.sort(key=lambda item: -item[0])
    return [snippet[:240] + ("…" if len(snippet) > 240 else "") for _, snippet in scored[:limit]]


def cmd_list(args: argparse.Namespace) -> int:
    clients_dir = Path(args.clients_dir)
    entries = collect(clients_dir, args.client)
    if args.open:
        entries = [entry for entry in entries if entry.status in OPEN_STATUSES]
    if not entries:
        print("Nenhum registro encontrado.")
        return 0
    for entry in entries[: args.limit]:
        print(format_entry(entry, clients_dir))
    if len(entries) > args.limit:
        print(f"… e mais {len(entries) - args.limit} registro(s). Use --limit para ver mais.")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    clients_dir = Path(args.clients_dir)
    query_tokens = set(tokens(args.query))
    if not query_tokens:
        print("Consulta vazia depois de remover palavras comuns; use termos mais específicos.")
        return 1
    ranked = []
    for entry in collect(clients_dir, args.client):
        title_tokens = set(tokens(entry.title))
        body_tokens = tokens(entry.text)
        body_set = set(body_tokens)
        matched = query_tokens & (body_set | title_tokens)
        if not matched:
            continue
        frequency = sum(1 for token in body_tokens if token in query_tokens)
        score = 10 * len(matched) + 5 * len(query_tokens & title_tokens) + min(frequency, 30)
        ranked.append((score, len(matched), entry))
    ranked.sort(key=lambda item: (-item[0], item[2].date))
    if not ranked:
        print("Nada encontrado no histórico deste cliente para esses termos.")
        return 0
    for score, matched, entry in ranked[: args.limit]:
        print(format_entry(entry, clients_dir))
        print(f"    termos encontrados: {matched}/{len(query_tokens)}")
        for snippet in best_snippets(entry.text, query_tokens):
            print(f"    › {snippet}")
    return 0


def parser() -> argparse.ArgumentParser:
    main_parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    main_parser.add_argument("--clients-dir", default=str(DEFAULT_CLIENTS_DIR))
    sub = main_parser.add_subparsers(dest="command", required=True)
    list_cmd = sub.add_parser("list", help="linha do tempo das operações do cliente (legado + V2)")
    list_cmd.add_argument("client")
    list_cmd.add_argument("--limit", type=int, default=10)
    list_cmd.add_argument("--open", action="store_true", help="só operações sem fechamento")
    list_cmd.set_defaults(func=cmd_list)
    search = sub.add_parser("search", help="busca por termos no texto dos dossiês do cliente")
    search.add_argument("client")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=5)
    search.set_defaults(func=cmd_search)
    return main_parser


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
