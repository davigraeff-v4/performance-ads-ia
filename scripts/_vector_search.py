"""Busca vetorial local (numpy) sobre o índice gerado por
build_knowledge_vector_index.py. Usado como segundo sinal pelos scripts de
busca lexical (search_meta_help.py, search_google_ads_help.py) — nunca
sozinho, e nunca carregado quando o sinal lexical já é exact/strong.

Falha graciosamente: se o índice ou o fastembed não estiverem disponíveis,
retorna None e quem chamou cai de volta para o modo lexical puro.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_knowledge_vector_index import EMBEDDING_MODEL, INDEX_DIR, PLATFORM_CONFIGS  # noqa: E402

# Faixa de calibração: similaridade de cosseno desse modelo não vai a zero
# nem para frases sem relação (viés conhecido de embeddings de frase). Testado
# empiricamente contra a base local: consultas sem relação nenhuma ficam
# abaixo de ~0.45; consultas de fato relacionadas passam de ~0.5.
SIMILARITY_FLOOR = 0.45
SIMILARITY_CEILING = 0.85
SCORE_CEILING = 95.0

_MODEL_CACHE: dict[str, object] = {}


def _map_similarity(cosine: float) -> float:
    if cosine <= SIMILARITY_FLOOR:
        return 0.0
    scaled = (min(cosine, SIMILARITY_CEILING) - SIMILARITY_FLOOR) / (SIMILARITY_CEILING - SIMILARITY_FLOOR)
    return round(scaled * SCORE_CEILING, 2)


def _load_index(platform: str):
    slug = PLATFORM_CONFIGS[platform]["index_slug"]
    vectors_path = INDEX_DIR / f"{slug}.npz"
    meta_path = INDEX_DIR / f"{slug}-meta.json"
    if not vectors_path.is_file() or not meta_path.is_file():
        return None
    try:
        import numpy as np

        raw = np.load(vectors_path)["vectors"]
        norms = np.linalg.norm(raw, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        vectors = raw / norms
        metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        return vectors, metadata
    except Exception:
        return None


def _embed_query(text: str):
    import numpy as np

    if "model" not in _MODEL_CACHE:
        from fastembed import TextEmbedding

        _MODEL_CACHE["model"] = TextEmbedding(model_name=EMBEDDING_MODEL)
    model = _MODEL_CACHE["model"]
    vector = np.array(next(iter(model.embed([text]))), dtype=np.float32)
    norm = np.linalg.norm(vector)
    return vector / norm if norm else vector


def vector_candidates(query: str, platform: str, *, top_chunks: int = 15) -> dict[str, dict] | None:
    """Retorna {path_relativo: {"score", "similarity", "section"}} ou None
    se o índice/motor não estiverem disponíveis (chamador cai para lexical)."""
    loaded = _load_index(platform)
    if loaded is None:
        return None
    vectors, metadata = loaded
    try:
        import numpy as np

        query_vector = _embed_query(query)
        similarities = vectors @ query_vector
        top_indices = np.argsort(-similarities)[:top_chunks]
    except Exception:
        return None

    candidates: dict[str, dict] = {}
    for index in top_indices:
        similarity = float(similarities[index])
        score = _map_similarity(similarity)
        if score <= 0:
            continue
        chunk = metadata[index]
        path = chunk["path"]
        if path not in candidates or score > candidates[path]["score"]:
            candidates[path] = {
                "score": score,
                "similarity": round(similarity, 3),
                "section": chunk.get("section"),
            }
    return candidates
