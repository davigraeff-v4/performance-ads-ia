#!/usr/bin/env python3
"""Gera o INDEX.md da base seletiva da Central de Ajuda do Google Ads."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "official-google" / "help-center"
INDEX = BASE / "INDEX.md"
CATEGORY_NAMES = {
    "00-comecar-a-anunciar": "Começar a anunciar",
    "01-campanhas": "Campanhas",
    "02-recursos": "Recursos",
    "03-otimizacao-desempenho": "Otimizar o desempenho",
    "04-conta-faturamento": "Conta e faturamento",
    "05-correcao-problemas": "Corrigir problemas",
    "06-google-partners": "Google Partners",
}


@dataclass(frozen=True)
class Article:
    title: str
    url: str
    category: str
    topic: str
    subtopic: str
    path: Path


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError(f"frontmatter ausente: {path.relative_to(ROOT)}")
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip().strip('"\'')
    return result


def load_articles() -> list[Article]:
    articles: list[Article] = []
    for path in sorted(BASE.glob("**/*.md")):
        if path.name == "INDEX.md":
            continue
        metadata = frontmatter(path)
        articles.append(
            Article(
                title=metadata["title"],
                url=metadata["url"],
                category=metadata["categoria"],
                topic=metadata["topico"],
                subtopic=metadata["subtopico"],
                path=path.relative_to(BASE),
            )
        )
    return articles


def render(articles: list[Article]) -> str:
    grouped: dict[str, dict[str, dict[str, list[Article]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))
    )
    for article in articles:
        grouped[article.category][article.topic][article.subtopic].append(article)

    category_label = "categoria" if len(grouped) == 1 else "categorias"
    lines = [
        "# Central de Ajuda do Google Ads — índice local",
        "",
        "Base seletiva em português do Brasil. Iniciada em 2026-08-07 e organizada conforme a navegação oficial da Central de Ajuda.",
        "",
        f"**Cobertura atual: {len(articles)} artigos em {len(grouped)} {category_label}.**",
        "",
    ]
    for category in sorted(grouped):
        lines.extend([f"## {CATEGORY_NAMES.get(category, category)}", ""])
        for topic in sorted(grouped[category], key=str.casefold):
            for subtopic in sorted(grouped[category][topic], key=str.casefold):
                heading = topic if topic == subtopic else f"{topic} → {subtopic}"
                lines.extend([f"### {heading}", ""])
                for article in sorted(
                    grouped[category][topic][subtopic],
                    key=lambda item: item.title.casefold(),
                ):
                    lines.append(
                        f"- [{article.title}]({article.path.as_posix()}) — "
                        f"[fonte original]({article.url})"
                    )
                lines.append("")

    lines.extend([
        "## Frescor e limites",
        "",
        "- Os conteúdos foram lidos na Central oficial usando o Chrome e sintetizados para recuperação seletiva.",
        "- Módulos personalizados pela conta, respostas de IA da página, feedback, anúncios e navegação foram excluídos.",
        "- As páginas podem conter tradução por IA. Confira o original em decisões sensíveis ou quando a redação local estiver ambígua.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="atualiza o INDEX.md")
    args = parser.parse_args()
    output = render(load_articles())
    if args.write:
        INDEX.write_text(output, encoding="utf-8")
        print(f"Índice atualizado: {INDEX.relative_to(ROOT)}")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
