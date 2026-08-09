"""Lógica compartilhada de leitura e pontuação para as bases de Central de
Ajuda (Meta e Google Ads). Usado por search_meta_help.py,
search_google_ads_help.py e, futuramente, pelo pipeline de índice vetorial.

Não contém nenhuma regra de gate de plataforma — isso permanece em cada
script, que é o dono da decisão de qual base é a sua.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Callable, Pattern


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


def make_tokenizer(stopwords: frozenset[str]) -> Callable[[str], set[str]]:
    def tokens(value: str) -> set[str]:
        return {
            token for token in normalize(value).split()
            if len(token) > 1 and token not in stopwords
        }

    return tokens


def load_articles(
    *,
    root: Path,
    base: Path,
    link_pattern: Pattern[str],
    date_pattern: Pattern[str],
    index_filename: str = "INDEX.md",
) -> list[Article]:
    """Carrega somente o INDEX.md; os corpos permanecem fechados nesta etapa."""
    index_path = base / index_filename
    if not index_path.is_file():
        raise FileNotFoundError(f"índice ausente: {index_path.relative_to(root)}")

    text = index_path.read_text(encoding="utf-8")
    date_match = date_pattern.search(text)
    extracted_at = date_match.group(1) if date_match else ""

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
                path=base / relative_path,
            )
        )
    if not articles:
        raise ValueError(f"nenhum artigo encontrado em {index_path.relative_to(root)}")
    return articles


def score_article(
    query: str,
    article: Article,
    *,
    tokens: Callable[[str], set[str]],
    category_bonus: bool = False,
) -> float:
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

    if category_bonus:
        category_overlap = query_tokens & tokens(article.category)
        score += min(6.0, 3.0 * len(category_overlap))

    return min(round(score, 2), 99.0)


def body_signal(
    query: str,
    article: Article,
    *,
    tokens: Callable[[str], set[str]],
    expand: Callable[[set[str]], set[str]] | None = None,
) -> float:
    """Sinal secundário usado somente quando o índice não dá resultado forte."""
    query_tokens = tokens(query)
    if not query_tokens:
        return 0.0
    expanded = expand(query_tokens) if expand else query_tokens
    text = normalize(article.path.read_text(encoding="utf-8", errors="ignore"))
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
