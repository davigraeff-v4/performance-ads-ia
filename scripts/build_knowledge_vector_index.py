#!/usr/bin/env python3
"""Constrói o índice vetorial local (numpy) de uma base de Central de Ajuda.

Lê os artigos via o mesmo INDEX.md usado pela busca lexical, corta cada
artigo em chunks por seção H2 (com overlap quando uma seção é longa), gera
embeddings locais com fastembed e persiste tudo em
knowledge/.vector-index/{plataforma}.npz + {plataforma}-meta.json.

Este índice é um artefato derivado, mas versionado no Git (pequeno, ~2.6MB,
só conhecimento público) para o time receber o RAG pronto no clone/pull.
Pode ser regenerado a qualquer momento; scripts/validate_repository.py
detecta desatualização comparando o hash do manifest com os .md fonte.
Não indexa nada em clients/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _help_index_common import Article, load_articles  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT / "knowledge" / ".vector-index"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Unidade usada para medir tamanho de chunk/overlap: contagem de palavras
# (proxy simples e auditável para tokens; evita depender do tokenizer
# específico do modelo só para o build).
WORDS_PER_CHUNK = 180
SECTION_SPLIT_THRESHOLD_WORDS = 300
OVERLAP_RATIO = 0.15
OVERLAP_WORDS = round(WORDS_PER_CHUNK * OVERLAP_RATIO)

FRONTMATTER_PATTERN = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
H1_PATTERN = re.compile(r"^#\s+.+\n+", re.MULTILINE)
H2_SPLIT_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

PLATFORM_CONFIGS = {
    "meta": {
        "base": ROOT / "knowledge" / "meta-help-center",
        "link_pattern": re.compile(
            r"^- \[(?P<title>.+?)\]\((?P<path>[^)]+\.md)\) — "
            r"\[fonte original\]\((?P<url>https://www\.facebook\.com/business/help/[^)]+)\)$"
        ),
        "date_pattern": re.compile(r"Gerado em (\d{4}-\d{2}-\d{2})"),
        "index_slug": "meta-help-center",
    },
    "google_ads": {
        "base": ROOT / "knowledge" / "official-google" / "help-center",
        "link_pattern": re.compile(
            r"^- \[(?P<title>.+?)\]\((?P<path>[^)]+\.md)\) — "
            r"\[fonte original\]\((?P<url>https://support\.google\.com/google-ads/answer/[^)]+)\)$"
        ),
        "date_pattern": re.compile(r"iniciado em (\d{4}-\d{2}-\d{2})"),
        "index_slug": "google-ads-help-center",
    },
}


def strip_frontmatter_and_title(text: str) -> str:
    without_frontmatter = FRONTMATTER_PATTERN.sub("", text, count=1)
    return H1_PATTERN.sub("", without_frontmatter, count=1)


def split_into_sections(body: str) -> list[tuple[str | None, str]]:
    """Divide o corpo em (título da seção ou None, texto) por H2."""
    matches = list(H2_SPLIT_PATTERN.finditer(body))
    if not matches:
        text = body.strip()
        return [(None, text)] if text else []

    sections: list[tuple[str | None, str]] = []
    intro = body[: matches[0].start()].strip()
    if intro:
        sections.append((None, intro))
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        text = body[start:end].strip()
        if text:
            sections.append((heading, text))
    return sections


def chunk_section_text(text: str) -> list[str]:
    """Janela deslizante por palavras com overlap, só quando a seção é longa."""
    words = text.split()
    if len(words) <= SECTION_SPLIT_THRESHOLD_WORDS:
        return [text]

    step = WORDS_PER_CHUNK - OVERLAP_WORDS
    chunks: list[str] = []
    position = 0
    while position < len(words):
        window = words[position : position + WORDS_PER_CHUNK]
        chunks.append(" ".join(window))
        if position + WORDS_PER_CHUNK >= len(words):
            break
        position += step
    return chunks


def build_chunks_for_article(article: Article, platform: str) -> list[dict]:
    raw_text = article.path.read_text(encoding="utf-8")
    body = strip_frontmatter_and_title(raw_text)
    sections = split_into_sections(body)

    chunks: list[dict] = []
    chunk_index = 0
    for heading, section_text in sections:
        for piece in chunk_section_text(section_text):
            embedded_text = (
                f"{article.title} — {heading}\n\n{piece}"
                if heading
                else f"{article.title}\n\n{piece}"
            )
            chunks.append(
                {
                    "text": embedded_text,
                    "title": article.title,
                    "section": heading,
                    "category": article.category,
                    "url": article.url,
                    "extracted_at": article.extracted_at,
                    "path": str(article.path.relative_to(ROOT)),
                    "platform": platform,
                    "chunk_index": chunk_index,
                }
            )
            chunk_index += 1
    return chunks


def source_hash(articles: list[Article]) -> str:
    digest = hashlib.sha256()
    for article in sorted(articles, key=lambda item: str(item.path)):
        digest.update(str(article.path).encode("utf-8"))
        digest.update(article.path.read_bytes())
    return digest.hexdigest()


def build_index(platform: str, *, force: bool) -> None:
    config = PLATFORM_CONFIGS[platform]
    articles = load_articles(
        root=ROOT,
        base=config["base"],
        link_pattern=config["link_pattern"],
        date_pattern=config["date_pattern"],
    )
    current_hash = source_hash(articles)

    slug = config["index_slug"]
    manifest_path = INDEX_DIR / f"{slug}-manifest.json"
    if manifest_path.is_file() and not force:
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        if existing.get("source_hash") == current_hash:
            print(f"[{platform}] índice já atualizado (hash inalterado); use --force para reconstruir.")
            return

    all_chunks: list[dict] = []
    for article in articles:
        all_chunks.extend(build_chunks_for_article(article, platform))

    if not all_chunks:
        raise ValueError(f"nenhum chunk gerado para a plataforma {platform}")

    print(f"[{platform}] {len(articles)} artigos → {len(all_chunks)} chunks. Carregando modelo de embedding...")

    import numpy as np
    from fastembed import TextEmbedding

    model = TextEmbedding(model_name=EMBEDDING_MODEL)
    texts = [chunk["text"] for chunk in all_chunks]
    vectors = np.array(list(model.embed(texts)), dtype=np.float32)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectors_path = INDEX_DIR / f"{slug}.npz"
    meta_path = INDEX_DIR / f"{slug}-meta.json"

    np.savez_compressed(vectors_path, vectors=vectors)
    meta_path.write_text(
        json.dumps([{k: v for k, v in chunk.items() if k != "text"} for chunk in all_chunks], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_path.write_text(
        json.dumps(
            {
                "platform": platform,
                "model": EMBEDDING_MODEL,
                "article_count": len(articles),
                "chunk_count": len(all_chunks),
                "source_hash": current_hash,
                "built_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "words_per_chunk": WORDS_PER_CHUNK,
                "overlap_words": OVERLAP_WORDS,
                "overlap_ratio": OVERLAP_RATIO,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[{platform}] índice salvo em {vectors_path.relative_to(ROOT)} ({vectors.shape[0]} vetores, dim={vectors.shape[1]}).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", required=True, choices=["meta", "google_ads", "all"])
    parser.add_argument("--force", action="store_true", help="reconstrói mesmo se o hash da fonte não mudou")
    args = parser.parse_args()

    platforms = ["meta", "google_ads"] if args.platform == "all" else [args.platform]
    for platform in platforms:
        build_index(platform, force=args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
