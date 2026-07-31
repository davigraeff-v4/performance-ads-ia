#!/usr/bin/env python3
"""Busca seletiva na base local da Central de Ajuda Meta Ads."""

from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "meta-help-center"
STOPWORDS = {
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "na", "nas", "no", "nos", "o", "os", "para", "por", "que",
    "esta", "estou", "meta", "meu", "minha", "qual", "quais", "se", "seu",
    "sua", "sobre", "um", "uma",
}


@dataclass(frozen=True)
class Article:
    title: str
    url: str
    category: str
    extracted_at: str
    path: Path


def normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    ascii_text = "".join(char for char in decomposed if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", ascii_text.lower()).strip()


def tokens(value: str) -> set[str]:
    return {token for token in normalize(value).split() if len(token) > 1 and token not in STOPWORDS}


def load_articles() -> list[Article]:
    """Carrega somente o INDEX.md; os corpos permanecem fechados nesta etapa."""
    index_path = BASE / "INDEX.md"
    if not index_path.is_file():
        raise FileNotFoundError(f"índice ausente: {index_path.relative_to(ROOT)}")
    text = index_path.read_text(encoding="utf-8")
    date_match = re.search(r"Gerado em (\d{4}-\d{2}-\d{2})", text)
    extracted_at = date_match.group(1) if date_match else ""
    link_pattern = re.compile(
        r"^- \[(?P<title>.+?)\]\((?P<path>[^)]+\.md)\) — "
        r"\[fonte original\]\((?P<url>https://www\.facebook\.com/business/help/[^)]+)\)$"
    )
    articles: list[Article] = []
    for line in text.splitlines():
        match = link_pattern.match(line)
        if not match:
            continue
        relative_path = Path(match.group("path"))
        articles.append(
            Article(
                title=match.group("title"),
                url=match.group("url"),
                category=relative_path.parent.name,
                extracted_at=extracted_at,
                path=BASE / relative_path,
            )
        )
    if not articles:
        raise ValueError(f"nenhum artigo encontrado em {index_path.relative_to(ROOT)}")
    return articles


def score_article(query: str, article: Article) -> float:
    normalized_query = normalize(query)
    normalized_title = normalize(article.title)
    query_tokens = tokens(query)
    title_tokens = tokens(article.title)

    if normalized_query == normalized_title:
        return 100.0

    intersection = query_tokens & title_tokens
    query_coverage = len(intersection) / max(len(query_tokens), 1)
    title_coverage = len(intersection) / max(len(title_tokens), 1)
    union = query_tokens | title_tokens
    jaccard = len(intersection) / max(len(union), 1)
    score = 55 * query_coverage + 20 * title_coverage + 15 * jaccard
    score += 18 * SequenceMatcher(None, normalized_query, normalized_title).ratio()

    if normalized_query and normalized_query in normalized_title:
        score = max(score, 84 + 10 * query_coverage)
    elif normalized_title and normalized_title in normalized_query:
        score = max(score, 78 + 10 * title_coverage)

    category_overlap = query_tokens & tokens(article.category)
    score += min(6.0, 3.0 * len(category_overlap))

    return min(round(score, 2), 99.0)


def body_signal(query: str, article: Article) -> float:
    """Sinal secundário usado somente quando o índice não dá resultado forte."""
    query_tokens = tokens(query)
    if not query_tokens:
        return 0.0
    text = normalize(article.path.read_text(encoding="utf-8", errors="ignore"))
    expanded = set(query_tokens)
    if any(token.startswith("duplic") or token.startswith("deduplic") for token in query_tokens):
        expanded.update({"duplicacao", "desduplicacao", "deduplicacao"})
    hits = sum(1 for token in expanded if token in text)
    return min(32.0, 32.0 * hits / max(len(expanded), 1))


def label_for(score: float) -> str:
    if score == 100:
        return "exact"
    if score >= 75:
        return "strong"
    if score >= 35:
        return "related"
    return "weak"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="pergunta ou trecho de título")
    parser.add_argument("--limit", type=int, default=3, help="quantidade de resultados (padrão: 3)")
    parser.add_argument("--title-only", action="store_true", help="não usa o corpo como sinal secundário")
    parser.add_argument("--json", action="store_true", dest="as_json", help="retorna JSON")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    if not query or args.limit < 1:
        parser.error("informe uma consulta e um limite maior que zero")

    try:
        articles = load_articles()
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    ranked = [(score_article(query, article), article) for article in articles]
    ranked.sort(key=lambda item: (-item[0], normalize(item[1].title)))
    used_body_fallback = False
    if not args.title_only and ranked and ranked[0][0] < 75:
        used_body_fallback = True
        ranked = [
            (round(min(99.0, score + body_signal(query, article)), 2), article)
            for score, article in ranked
        ]
        ranked.sort(key=lambda item: (-item[0], normalize(item[1].title)))
    selected = ranked[: args.limit]

    payload = [
        {
            "score": score,
            "match": label_for(score),
            "title": article.title,
            "category": article.category,
            "path": str(article.path.relative_to(ROOT)),
            "url": article.url,
            "extracted_at": article.extracted_at,
        }
        for score, article in selected
    ]

    if args.as_json:
        print(json.dumps({"query": query, "article_count": len(articles), "body_fallback": used_body_fallback, "results": payload}, ensure_ascii=False, indent=2))
        return 0

    print(f"Consulta: {query}")
    stage = "índice + fallback de conteúdo" if used_body_fallback else "somente índice"
    print(f"Base: {len(articles)} artigos | Busca: {stage} | Resultados: {len(payload)}")
    for index, item in enumerate(payload, start=1):
        print(f"\n{index}. [{item['match']}] {item['score']:.2f} — {item['title']}")
        print(f"   Caminho: {item['path']}")
        print(f"   Categoria: {item['category']} | Extraído em: {item['extracted_at']}")
        print(f"   URL: {item['url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
