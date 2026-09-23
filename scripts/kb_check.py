#!/usr/bin/env python3
"""Revisor de boas práticas: confere premissas contra a base oficial.

Recebe as premissas de mecanismo de um diagnóstico, change set ou leitura de
resultados ("reduzir o orçamento reinicia o aprendizado", "as duas campanhas
competem no leilão") e, para cada uma, devolve:

- os artigos candidatos da plataforma certa (título, caminho, URL, rótulo e o
  trecho que mais se relaciona com a premissa);
- quais precisam ser lidos por inteiro (rótulo exact/strong);
- para Meta, a sugestão de consulta ao vivo em `ads_get_help_article`;
- um esqueleto de `knowledge_checks` com o veredito em branco.

O script NÃO decide o veredito. O agent lê os artigos e preenche
sustenta / contradiz / sem_cobertura, com a nota e a fonte que usou. Um
veredito sustenta ou contradiz sem URL oficial é recusado por
`dossier.py verify`.

Uso:
    python3 scripts/kb_check.py --platform meta "premissa 1" "premissa 2"
    python3 scripts/kb_check.py --input .work/premissas.json [--json]

Formato de --input: lista de strings ou de objetos {"premise", "platform"};
`platform` do objeto vale mais que --platform.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from help_search import PLATFORMS, ROOT, load_rewrites, search  # noqa: E402

READ_IN_FULL = {"exact", "strong"}
EXCERPT_CHARS = 420
FRONTMATTER = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


def load_premises(args: argparse.Namespace) -> list[dict]:
    items: list[dict] = []
    if args.input:
        raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
        for entry in raw:
            if isinstance(entry, str):
                items.append({"premise": entry, "platform": args.platform})
            else:
                items.append({"premise": entry["premise"], "platform": entry.get("platform") or args.platform})
    items += [{"premise": premise, "platform": args.platform} for premise in args.premises]
    for item in items:
        if item["platform"] not in PLATFORMS:
            raise SystemExit(f"ERRO: plataforma ausente ou inválida para a premissa “{item['premise']}” (use meta ou google_ads)")
        if len(item["premise"].strip()) < 10:
            raise SystemExit(f"ERRO: premissa curta demais para conferir: “{item['premise']}”")
    if not items:
        raise SystemExit("ERRO: informe ao menos uma premissa")
    return items


# Verbos que a premissa e o artigo usam para a mesma ideia de concorrência.
EQUIVALENT_STEMS = {"disput": "concor", "compet": "concor", "concor": "concor"}


def _stems(words: set[str]) -> set[str]:
    stems = set()
    for word in words:
        stem = word[:6]
        stems.add(EQUIVALENT_STEMS.get(stem, stem))
    return stems


def best_excerpts(article_path: Path, premise_terms: set[str], rewrite_terms: set[str], tokens,
                  count: int = 2) -> list[str]:
    """Os parágrafos do artigo que mais se relacionam com a premissa.

    Palavras da premissa pesam o dobro das do termo reescrito; a comparação é
    pelo radical (6 letras), com os verbos de concorrência tratados como um só.
    """
    text = FRONTMATTER.sub("", article_path.read_text(encoding="utf-8", errors="ignore"))
    premise_stems, rewrite_stems = _stems(premise_terms), _stems(rewrite_terms)
    scored: list[tuple[int, int, str]] = []
    for position, block in enumerate(re.split(r"\n\s*\n", text)):
        if block.lstrip().startswith("#"):
            continue
        clean = " ".join(line.strip(" -*>") for line in block.splitlines()).strip()
        if len(clean) < 40:
            continue
        block_stems = _stems(tokens(clean))
        score = 2 * len(premise_stems & block_stems) + len(rewrite_stems & block_stems)
        if score:
            scored.append((score, position, clean))
    # Os melhores parágrafos, na ordem em que aparecem no artigo.
    chosen = sorted(sorted(scored, key=lambda item: (-item[0], item[1]))[:count], key=lambda item: item[1])
    return [clean if len(clean) <= EXCERPT_CHARS else clean[:EXCERPT_CHARS].rsplit(" ", 1)[0] + "…"
            for _score, _position, clean in chosen]


def live_query_hint(payload: dict, platform: str) -> str | None:
    if platform != "meta":
        return None
    # A ferramenta ao vivo da Meta acerta melhor com o nome do produto em inglês;
    # o título do melhor candidato é um bom ponto de partida.
    if payload["results"] and payload["results"][0]["match"] in READ_IN_FULL:
        return f"ads_get_help_article: “{payload['results'][0]['title']}” (tente também o termo em inglês)"
    return "ads_get_help_article: descreva o mecanismo com o nome do produto (em inglês costuma funcionar melhor)"


def check_premise(item: dict, limit: int) -> dict:
    platform = item["platform"]
    config = PLATFORMS[platform]
    payload = search(item["premise"], base_platform=platform, requested_platform=platform,
                     limit=limit, warn=lambda _message: None)
    if payload["out_of_scope"]:
        return {"premise": item["premise"], "platform": platform, "out_of_scope": True,
                "reason": payload["reason"], "candidates": [], "read_in_full": [], "live_query": None,
                "skeleton": skeleton(item["premise"], None)}

    premise_terms = set(config.tokens(item["premise"]))
    rewrite_terms: set[str] = set()
    for rule in load_rewrites().get(platform, []):
        if rule["id"] in payload.get("rewrites", []):
            for term in rule["termos"]:
                rewrite_terms |= config.tokens(term)

    candidates = []
    for result in payload["results"]:
        candidates.append({
            "title": result["title"],
            "path": result["path"],
            "url": result["url"],
            "match": result["match"],
            "signal": result["signal"],
            "extracted_at": result["extracted_at"],
            "excerpts": best_excerpts(ROOT / result["path"], premise_terms, rewrite_terms, config.tokens),
        })
    relevant = [c for c in candidates if c["match"] != "weak"]
    return {
        "premise": item["premise"],
        "platform": platform,
        "out_of_scope": False,
        "rewrites": payload.get("rewrites", []),
        "candidates": candidates,
        "read_in_full": [c["path"] for c in candidates if c["match"] in READ_IN_FULL],
        "no_local_coverage": not relevant,
        "live_query": live_query_hint(payload, platform),
        "skeleton": skeleton(item["premise"], relevant[0] if relevant else None),
    }


def skeleton(premise: str, top: dict | None) -> dict:
    return {
        "premise": premise,
        "verdict": None,
        "source_title": top["title"] if top else None,
        "source_url": top["url"] if top else None,
        "note": "",
    }


def print_human(results: list[dict]) -> None:
    for index, result in enumerate(results, start=1):
        label = "Meta" if result["platform"] == "meta" else "Google Ads"
        print(f"\nPremissa {index} ({label}): {result['premise']}")
        if result["out_of_scope"]:
            print(f"  fora da base desta plataforma ({result['reason']}); confira na plataforma certa")
            continue
        if result["no_local_coverage"]:
            print("  nenhum candidato relevante na base local: provável 'sem_cobertura', a menos que a fonte ao vivo cubra")
        for position, candidate in enumerate(result["candidates"], start=1):
            must = " — LER INTEIRO" if candidate["match"] in READ_IN_FULL else ""
            print(f"  {position}. [{candidate['match']}] {candidate['title']}{must}")
            print(f"     {candidate['path']}")
            print(f"     {candidate['url']} (extraído em {candidate['extracted_at']})")
            for excerpt in candidate["excerpts"]:
                print(f"     trecho: {excerpt}")
        if result["live_query"]:
            print(f"  fonte ao vivo: {result['live_query']}")
    print("\nEsqueleto de knowledge_checks (preencha verdict e note depois de ler os artigos):")
    print(json.dumps([r["skeleton"] for r in results], ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("premises", nargs="*", help="premissas, uma por argumento")
    parser.add_argument("--platform", choices=sorted(PLATFORMS), help="plataforma das premissas passadas como argumento")
    parser.add_argument("--input", help="arquivo JSON com a lista de premissas")
    parser.add_argument("--limit", type=int, default=3, help="candidatos por premissa (padrão: 3)")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    results = [check_premise(item, args.limit) for item in load_premises(args)]
    if args.as_json:
        print(json.dumps({"checks": results, "skeleton": [r["skeleton"] for r in results]}, ensure_ascii=False, indent=2))
    else:
        print_human(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
