"""Busca seletiva nas bases locais da Central de Ajuda (Meta e Google Ads).

Módulo único de ranqueamento, usado pelas interfaces de linha de comando
(`search_meta_help.py`, `search_google_ads_help.py`), pela medição
(`eval_retrieval.py`) e pelo revisor de boas práticas (`kb_check.py`).

Etapas, na ordem:

1. gate de plataforma, fail-closed (a base de uma plataforma nunca responde
   pela outra);
2. pontuação lexical pelo título do `INDEX.md`;
3. fallback de conteúdo, só quando o melhor título fica abaixo de `strong`;
4. sinal vetorial local, só quando o título puro fica abaixo de `strong`.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable, Pattern

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _help_index_common import (  # noqa: E402
    Article,
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
REWRITES_PATH = ROOT / "knowledge" / "retrieval-rewrites.json"
STRONG = 75.0
# Termo do dicionário precisa bater quase por inteiro com o título. O artigo
# apontado fica acima de qualquer resultado só vetorial (teto 95), mas abaixo
# de um título idêntico à consulta original: nunca vira "exact".
REWRITE_MIN_TITLE = 90.0
REWRITE_SCORE = 96.0
POLICY_PENALTY = 0.6


def _expand_meta_dedup(query_tokens: set[str]) -> set[str]:
    expanded = set(query_tokens)
    if any(token.startswith("duplic") or token.startswith("deduplic") for token in query_tokens):
        expanded.update({"duplicacao", "desduplicacao", "deduplicacao"})
    return expanded


@dataclass(frozen=True)
class PlatformConfig:
    key: str
    label: str
    base: Path
    stopwords: frozenset[str]
    link_pattern: Pattern[str]
    date_pattern: Pattern[str]
    category_bonus: bool
    body_expand: Callable[[set[str]], set[str]] | None
    # Consulta que menciona explicitamente a outra plataforma é recusada.
    conflict_tokens: frozenset[str]
    # Meta confere o conflito depois das stopwords; Google, nos tokens brutos.
    conflict_uses_raw_tokens: bool

    @property
    def tokens(self) -> Callable[[str], set[str]]:
        return make_tokenizer(self.stopwords)


PLATFORMS: dict[str, PlatformConfig] = {
    "meta": PlatformConfig(
        key="meta",
        label="Meta",
        base=ROOT / "knowledge" / "meta-help-center",
        stopwords=frozenset({
            "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
            "e", "em", "na", "nas", "no", "nos", "o", "os", "para", "por", "que",
            "esta", "estou", "meta", "meu", "minha", "qual", "quais", "se", "seu",
            "sua", "sobre", "um", "uma",
        }),
        link_pattern=re.compile(
            r"^- \[(?P<title>.+?)\]\((?P<path>[^)]+\.md)\) — "
            r"\[fonte original\]\((?P<url>https://www\.facebook\.com/business/help/[^)]+)\)$"
        ),
        date_pattern=re.compile(r"Gerado em (\d{4}-\d{2}-\d{2})"),
        category_bonus=True,
        body_expand=_expand_meta_dedup,
        conflict_tokens=frozenset({"google", "ads"}),
        conflict_uses_raw_tokens=False,
    ),
    "google_ads": PlatformConfig(
        key="google_ads",
        label="Google Ads",
        base=ROOT / "knowledge" / "official-google" / "help-center",
        stopwords=frozenset({
            "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
            "e", "em", "google", "ads", "na", "nas", "no", "nos", "o", "os", "para",
            "planejador", "por", "que", "se", "seu", "sua", "sobre", "um", "uma",
        }),
        link_pattern=re.compile(
            r"^- \[(?P<title>.+?)\]\((?P<path>[^)]+\.md)\) — "
            r"\[fonte original\]\((?P<url>https://support\.google\.com/google-ads/answer/[^)]+)\)$"
        ),
        date_pattern=re.compile(r"iniciado em (\d{4}-\d{2}-\d{2})"),
        category_bonus=False,
        body_expand=None,
        conflict_tokens=frozenset({"meta", "ads"}),
        conflict_uses_raw_tokens=True,
    ),
}


# Artigos de política, restrição e revisão: úteis quando a consulta é sobre
# política, intrusos quando a consulta é sobre mecanismo de entrega ou lance.
POLICY_PATH_PATTERNS = (
    re.compile(r"meta-help-center/07-politicas-anuncios/"),
    re.compile(
        r"meta-help-center/10-solucao-problemas/(exemplos-comuns-de-violacoes|sobre-as-restricoes|"
        r"como-solucionar-anuncio-rejeitado|como-pedir-analise-para-conta-restrita|"
        r"como-solucionar-problemas-de-conta-desativada)"
    ),
    re.compile(r"official-google/help-center/02-recursos/sobre-o-processo-de-revisao-de-anuncios"),
    re.compile(r"official-google/help-center/04-conta-faturamento/suspensoes-"),
)


def is_policy_article(path: str | Path) -> bool:
    text = str(path)
    return any(pattern.search(text) for pattern in POLICY_PATH_PATTERNS)


@lru_cache(maxsize=1)
def load_rewrites() -> dict:
    if not REWRITES_PATH.is_file():
        return {}
    return json.loads(REWRITES_PATH.read_text(encoding="utf-8"))


def matching_rewrites(query: str, platform: str) -> list[dict]:
    normalized = normalize(query)
    return [
        rule for rule in load_rewrites().get(platform, [])
        if any(re.search(pattern, normalized) for pattern in rule["padroes"])
    ]


def is_policy_query(query: str) -> bool:
    normalized = normalize(query)
    patterns = load_rewrites().get("politica", {}).get("padroes", [])
    return any(re.search(pattern, normalized) for pattern in patterns)


def match_label(score: float, title_score: float) -> str:
    """Rótulo de leitura. "exact"/"strong" exigem evidência de título (da
    consulta original ou de um termo do dicionário de reescrita); sinal
    vetorial e fallback de conteúdo ordenam, mas sozinhos não obrigam a ler
    um artigo inteiro."""
    if score == 100 and title_score == 100:
        return "exact"
    if score >= STRONG and title_score >= STRONG:
        return "strong"
    return label_for(min(score, STRONG - 0.01)) if score >= STRONG else label_for(score)


def load_articles(platform: str) -> list[Article]:
    config = PLATFORMS[platform]
    return _load_articles(
        root=ROOT, base=config.base, link_pattern=config.link_pattern, date_pattern=config.date_pattern,
    )


def score_article(query: str, article: Article, platform: str) -> float:
    config = PLATFORMS[platform]
    return _score_article(query, article, tokens=config.tokens, category_bonus=config.category_bonus)


def body_signal(query: str, article: Article, platform: str) -> float:
    config = PLATFORMS[platform]
    return _body_signal(query, article, tokens=config.tokens, expand=config.body_expand)


def platform_conflict(query: str, platform: str) -> bool:
    config = PLATFORMS[platform]
    query_tokens = set(normalize(query).split()) if config.conflict_uses_raw_tokens else config.tokens(query)
    return config.conflict_tokens.issubset(query_tokens)


def _warn(message: str) -> None:
    print(message, file=sys.stderr)


def search(
    query: str,
    *,
    base_platform: str,
    requested_platform: str,
    limit: int = 3,
    mode: str = "hybrid",
    title_only: bool = False,
    rewrite: bool = True,
    warn: Callable[[str], None] = _warn,
) -> dict:
    """Busca na base de `base_platform`, com o gate contra `requested_platform`.

    Devolve o mesmo payload que a interface `--json` imprime. Levanta
    FileNotFoundError/ValueError se o índice da base estiver ausente.
    """
    if requested_platform != base_platform or platform_conflict(query, base_platform):
        reason = f"platform_not_{base_platform}" if requested_platform != base_platform else "query_platform_conflict"
        return {
            "query": query,
            "platform": requested_platform,
            "out_of_scope": True,
            "reason": reason,
            "article_count": 0,
            "body_fallback": False,
            "results": [],
        }

    articles = load_articles(base_platform)
    title_scores = {article.path: score_article(query, article, base_platform) for article in articles}
    ranked = [(title_scores[article.path], article) for article in articles]
    ranked.sort(key=lambda item: (-item[0], normalize(item[1].title)))
    # O gate do vetor decide pelo score de título puro, capturado antes do
    # fallback de corpo (heurística de substring mais fraca que o semântico).
    top_title_score = ranked[0][0] if ranked else 0.0

    used_body_fallback = False
    if not title_only and ranked and ranked[0][0] < STRONG:
        used_body_fallback = True
        ranked = [
            (round(min(99.0, score + body_signal(query, article, base_platform)), 2), article)
            for score, article in ranked
        ]
        ranked.sort(key=lambda item: (-item[0], normalize(item[1].title)))

    vector_used = False
    combined: list[list] = [[score, article, "lexical", None] for score, article in ranked]
    if not title_only and mode != "lexical" and (mode == "vector" or top_title_score < STRONG):
        candidates = vector_candidates(query, base_platform)
        if candidates is None:
            warn(f"aviso: índice vetorial indisponível para {base_platform}; usando busca lexical apenas.")
        else:
            vector_used = True
            combined = []
            for score, article in ranked:
                match = candidates.get(str(article.path.relative_to(ROOT)))
                vector_score = match["score"] if match else 0.0
                if vector_score <= 0:
                    signal = "lexical"
                elif score < 35:
                    signal = "vector"
                else:
                    signal = "hybrid"
                combined.append([max(score, vector_score), article, signal, match["section"] if match else None])

    # Reescrita controlada: a premissa vira o termo de produto do título.
    # Só correspondência forte de título pelo termo reescrito conta.
    rules = matching_rewrites(query, base_platform) if rewrite else []
    rewritten_by: dict[Path, str] = {}
    for rule in rules:
        for term in rule["termos"]:
            for entry in combined:
                article = entry[1]
                term_score = score_article(term, article, base_platform)
                if term_score >= REWRITE_MIN_TITLE and term_score > title_scores[article.path]:
                    title_scores[article.path] = term_score
                    rewritten_by[article.path] = rule["id"]
                    entry[0] = max(entry[0], REWRITE_SCORE)

    # Artigo de política só sobe quando a consulta é sobre política.
    policy_query = is_policy_query(query)
    for entry in combined:
        if not policy_query and is_policy_article(entry[1].path):
            entry[0] = round(entry[0] * POLICY_PENALTY, 2)

    combined.sort(key=lambda item: (-item[0], normalize(item[1].title)))

    results = []
    for score, article, signal, section in combined[:limit]:
        results.append({
            "score": score,
            "match": match_label(score, title_scores[article.path]),
            "title": article.title,
            "category": article.category,
            "path": str(article.path.relative_to(ROOT)),
            "url": article.url,
            "extracted_at": read_frontmatter_field(article.path, "extraido_em") or article.extracted_at,
            "signal": "rewrite" if article.path in rewritten_by else signal,
            "matched_section": section,
            "rewrite_rule": rewritten_by.get(article.path),
        })
    return {
        "query": query,
        "platform": base_platform,
        "out_of_scope": False,
        "article_count": len(articles),
        "body_fallback": used_body_fallback,
        "vector_used": vector_used,
        "rewrites": [rule["id"] for rule in rules],
        "results": results,
    }


def print_human(payload: dict, label: str) -> None:
    stage_parts = ["índice"]
    if payload["body_fallback"]:
        stage_parts.append("fallback de conteúdo")
    if payload["vector_used"]:
        stage_parts.append("sinal vetorial")
    stage = " + ".join(stage_parts) if len(stage_parts) > 1 else "somente índice"
    print(f"Consulta {label}: {payload['query']}")
    print(f"Base: {payload['article_count']} artigos | Busca: {stage} | Resultados: {len(payload['results'])}")
    for index, item in enumerate(payload["results"], start=1):
        print(f"\n{index}. [{item['match']}|{item['signal']}] {item['score']:.2f} — {item['title']}")
        print(f"   Caminho: {item['path']}")
        print(f"   Categoria: {item['category']} | Extraído em: {item['extracted_at']}")
        if item["matched_section"]:
            print(f"   Seção correspondente: {item['matched_section']}")
        print(f"   URL: {item['url']}")


def cli(base_platform: str, argv: list[str] | None = None, doc: str | None = None) -> int:
    import argparse
    import json

    config = PLATFORMS[base_platform]
    parser = argparse.ArgumentParser(description=doc)
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
    parser.add_argument("--no-rewrite", action="store_true", help="desliga o dicionário de reescrita (knowledge/retrieval-rewrites.json)")
    parser.add_argument("--json", action="store_true", dest="as_json", help="retorna JSON")
    args = parser.parse_args(argv)

    query = " ".join(args.query).strip()
    if not query or args.limit < 1:
        parser.error("informe uma consulta e um limite maior que zero")

    try:
        payload = search(
            query, base_platform=base_platform, requested_platform=args.platform,
            limit=args.limit, mode=args.mode, title_only=args.title_only, rewrite=not args.no_rewrite,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif payload["out_of_scope"]:
        print(f"Consulta fora do escopo da base {config.label}: {payload['reason']}")
    else:
        print_human(payload, config.label)
    return 0
