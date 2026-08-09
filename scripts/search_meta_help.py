#!/usr/bin/env python3
"""Busca seletiva na base local da Central de Ajuda Meta Ads."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _help_index_common import (  # noqa: E402
    body_signal as _body_signal,
    label_for,
    load_articles as _load_articles,
    make_tokenizer,
    normalize,
    read_frontmatter_field,
    score_article as _score_article,
)
from _vector_search import vector_candidates  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "meta-help-center"
STOPWORDS = frozenset({
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "na", "nas", "no", "nos", "o", "os", "para", "por", "que",
    "esta", "estou", "meta", "meu", "minha", "qual", "quais", "se", "seu",
    "sua", "sobre", "um", "uma",
})
tokens = make_tokenizer(STOPWORDS)

LINK_PATTERN = re.compile(
    r"^- \[(?P<title>.+?)\]\((?P<path>[^)]+\.md)\) — "
    r"\[fonte original\]\((?P<url>https://www\.facebook\.com/business/help/[^)]+)\)$"
)
DATE_PATTERN = re.compile(r"Gerado em (\d{4}-\d{2}-\d{2})")


def load_articles():
    return _load_articles(
        root=ROOT,
        base=BASE,
        link_pattern=LINK_PATTERN,
        date_pattern=DATE_PATTERN,
    )


def score_article(query, article):
    return _score_article(query, article, tokens=tokens, category_bonus=True)


def _expand_dedup(query_tokens: set[str]) -> set[str]:
    expanded = set(query_tokens)
    if any(token.startswith("duplic") or token.startswith("deduplic") for token in query_tokens):
        expanded.update({"duplicacao", "desduplicacao", "deduplicacao"})
    return expanded


def body_signal(query, article):
    return _body_signal(query, article, tokens=tokens, expand=_expand_dedup)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="pergunta ou trecho de título")
    parser.add_argument("--platform", required=True, choices=["meta", "google_ads"], help="plataforma já resolvida pelo roteador")
    parser.add_argument("--limit", type=int, default=3, help="quantidade de resultados (padrão: 3)")
    parser.add_argument("--title-only", action="store_true", help="não usa o corpo como sinal secundário")
    parser.add_argument(
        "--mode",
        choices=["lexical", "vector", "hybrid"],
        default="hybrid",
        help="lexical: só título/corpo (comportamento original). vector: força o sinal semântico. hybrid (padrão): lexical primeiro, vetorial só quando o título for fraco.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="retorna JSON")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    if not query or args.limit < 1:
        parser.error("informe uma consulta e um limite maior que zero")

    query_tokens = tokens(query)
    platform_conflict = args.platform == "meta" and {"google", "ads"}.issubset(query_tokens)
    if args.platform != "meta" or platform_conflict:
        reason = "platform_not_meta" if args.platform != "meta" else "query_platform_conflict"
        result = {
            "query": query,
            "platform": args.platform,
            "out_of_scope": True,
            "reason": reason,
            "article_count": 0,
            "body_fallback": False,
            "results": [],
        }
        if args.as_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Consulta fora do escopo da base Meta: {reason}")
        return 0

    try:
        articles = load_articles()
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    ranked = [(score_article(query, article), article) for article in articles]
    ranked.sort(key=lambda item: (-item[0], normalize(item[1].title)))
    # Score de título puro, capturado ANTES do fallback de corpo — é isso
    # que decide se o vetor é consultado, não o score já inflado pelo
    # fallback (que é uma heurística de substring mais fraca que o
    # semântico e pode mascarar um caso que o vetor acertaria melhor).
    top_title_score = ranked[0][0] if ranked else 0.0

    used_body_fallback = False
    if not args.title_only and ranked and ranked[0][0] < 75:
        used_body_fallback = True
        ranked = [
            (round(min(99.0, score + body_signal(query, article)), 2), article)
            for score, article in ranked
        ]
        ranked.sort(key=lambda item: (-item[0], normalize(item[1].title)))

    vector_used = False
    combined: list[tuple[float, object, str, str | None]] = [
        (score, article, "lexical", None) for score, article in ranked
    ]
    if not args.title_only and args.mode != "lexical" and (args.mode == "vector" or top_title_score < 75):
        candidates = vector_candidates(query, "meta")
        if candidates is None:
            print("aviso: índice vetorial indisponível para meta; usando busca lexical apenas.", file=sys.stderr)
        else:
            vector_used = True
            combined = []
            for score, article in ranked:
                path_key = str(article.path.relative_to(ROOT))
                match = candidates.get(path_key)
                vector_score = match["score"] if match else 0.0
                final_score = max(score, vector_score)
                if vector_score <= 0:
                    signal = "lexical"
                elif score < 35:
                    signal = "vector"
                else:
                    signal = "hybrid"
                combined.append((final_score, article, signal, match["section"] if match else None))
            combined.sort(key=lambda item: (-item[0], normalize(item[1].title)))

    selected = combined[: args.limit]

    payload = [
        {
            "score": score,
            "match": label_for(score),
            "title": article.title,
            "category": article.category,
            "path": str(article.path.relative_to(ROOT)),
            "url": article.url,
            "extracted_at": read_frontmatter_field(article.path, "extraido_em") or article.extracted_at,
            "signal": signal,
            "matched_section": section,
        }
        for score, article, signal, section in selected
    ]

    if args.as_json:
        print(json.dumps({"query": query, "platform": "meta", "out_of_scope": False, "article_count": len(articles), "body_fallback": used_body_fallback, "vector_used": vector_used, "results": payload}, ensure_ascii=False, indent=2))
        return 0

    print(f"Consulta Meta: {query}")
    stage_parts = ["índice"]
    if used_body_fallback:
        stage_parts.append("fallback de conteúdo")
    if vector_used:
        stage_parts.append("sinal vetorial")
    stage = " + ".join(stage_parts) if len(stage_parts) > 1 else "somente índice"
    print(f"Base: {len(articles)} artigos | Busca: {stage} | Resultados: {len(payload)}")
    for index, item in enumerate(payload, start=1):
        print(f"\n{index}. [{item['match']}|{item['signal']}] {item['score']:.2f} — {item['title']}")
        print(f"   Caminho: {item['path']}")
        print(f"   Categoria: {item['category']} | Extraído em: {item['extracted_at']}")
        if item["matched_section"]:
            print(f"   Seção correspondente: {item['matched_section']}")
        print(f"   URL: {item['url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
