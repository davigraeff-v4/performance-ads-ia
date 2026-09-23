#!/usr/bin/env python3
"""Mede a qualidade da busca nas bases oficiais com consultas rotuladas.

Lê `tests/fixtures/retrieval_eval.json` e, para cada consulta, roda a mesma
busca que o agent usa (`help_search.search`, modo híbrido). Métricas:

- acerto no 1º e entre os 3 primeiros: só consultas com artigo esperado já
  presente na base;
- "forte" errado: o 1º resultado sai como exact/strong (o que obriga a ler o
  artigo inteiro) sem ser um dos esperados; em consulta sem cobertura, qualquer
  forte entre os 3 primeiros conta;
- intrusão de política: artigo de política entre os 3 primeiros numa consulta
  que não é sobre política;
- gate: consulta sobre a outra plataforma precisa ser recusada.

Uso:
    python3 scripts/eval_retrieval.py                 # tabela por consulta + resumo
    python3 scripts/eval_retrieval.py --json          # resultado completo
    python3 scripts/eval_retrieval.py --save-baseline # grava o resumo como linha de base
    python3 scripts/eval_retrieval.py --compare       # compara com a linha de base gravada
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from help_search import ROOT, is_policy_article, search  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "retrieval_eval.json"
BASELINE = ROOT / "tests" / "fixtures" / "retrieval_baseline.json"
STRONG_LABELS = {"exact", "strong"}


def evaluate_query(item: dict, pending: set[str], *, depth: int = 10) -> dict:
    payload = search(
        item["query"], base_platform=item["platform"], requested_platform=item["platform"],
        limit=depth, warn=lambda _message: None,
    )
    if item["type"] == "outra_plataforma":
        # O gate é testado pedindo à base da plataforma rotulada uma consulta
        # que menciona a outra: precisa sair fora de escopo.
        return {
            "id": item["id"], "type": item["type"], "platform": item["platform"],
            "holdout": bool(item.get("holdout")), "gate_ok": bool(payload["out_of_scope"]),
            "top": [],
        }

    results = payload["results"]
    paths = [result["path"] for result in results]
    expected = set(item["expected"])
    present_expected = expected - pending
    rank = next((index + 1 for index, path in enumerate(paths) if path in present_expected), None)
    top3 = results[:3]
    top1 = results[0] if results else None

    if item["type"] == "sem_cobertura":
        strong_wrong = any(result["match"] in STRONG_LABELS for result in top3)
    else:
        strong_wrong = bool(top1 and top1["match"] in STRONG_LABELS and top1["path"] not in expected)

    return {
        "id": item["id"],
        "type": item["type"],
        "platform": item["platform"],
        "holdout": bool(item.get("holdout")),
        "query": item["query"],
        "scored": bool(present_expected),
        "waiting_for_article": bool(expected) and not present_expected,
        "rank": rank,
        "hit1": rank == 1,
        "hit3": rank is not None and rank <= 3,
        "strong_wrong": strong_wrong,
        "policy_intrusion": item["type"] != "politica" and any(is_policy_article(r["path"]) for r in top3),
        "vector_used": payload.get("vector_used", False),
        "top": [
            {"title": r["title"], "match": r["match"], "score": r["score"], "expected": r["path"] in expected,
             "policy": is_policy_article(r["path"])}
            for r in top3
        ],
    }


def summarize(rows: list[dict]) -> dict:
    def ratio(numerator: int, denominator: int) -> float | None:
        return round(numerator / denominator, 3) if denominator else None

    summary: dict[str, dict] = {}
    groups = {
        "meta": lambda row: not row["holdout"] and row["platform"] == "meta",
        "google_ads": lambda row: not row["holdout"] and row["platform"] == "google_ads",
        "todas": lambda row: not row["holdout"],
        "controle": lambda row: row["holdout"],
    }
    for platform, belongs in groups.items():
        subset = [row for row in rows if belongs(row)]
        scored = [row for row in subset if row.get("scored")]
        on_scope = [row for row in subset if row["type"] != "outra_plataforma"]
        non_policy = [row for row in on_scope if row["type"] != "politica"]
        gates = [row for row in subset if row["type"] == "outra_plataforma"]
        summary[platform] = {
            "consultas": len(subset),
            "avaliadas_por_acerto": len(scored),
            "aguardando_artigo": sum(1 for row in subset if row.get("waiting_for_article")),
            "acerto_1": ratio(sum(row["hit1"] for row in scored), len(scored)),
            "acerto_3": ratio(sum(row["hit3"] for row in scored), len(scored)),
            "forte_errado": ratio(sum(row["strong_wrong"] for row in on_scope), len(on_scope)),
            "intrusao_politica": ratio(sum(row["policy_intrusion"] for row in non_policy), len(non_policy)),
            "gate_ok": ratio(sum(row["gate_ok"] for row in gates), len(gates)),
        }
    return summary


def pct(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.0f}%"


def print_report(rows: list[dict], summary: dict, baseline: dict | None) -> None:
    for row in rows:
        if row["holdout"] and not rows[rows.index(row) - 1]["holdout"]:
            print("\n-- controle --")
        if row["type"] == "outra_plataforma":
            print(f"{row['id']:<10} outra plataforma: {'recusada ✅' if row['gate_ok'] else 'NÃO recusada ❌'}")
            continue
        if row["waiting_for_article"]:
            verdict = "aguarda artigo"
        elif not row["scored"]:
            verdict = "sem cobertura ⚠️ forte" if row["strong_wrong"] else "sem cobertura ✅"
        else:
            verdict = f"posição {row['rank']}" if row["rank"] else "fora do top 10 ❌"
        flags = []
        if row["strong_wrong"] and row["scored"]:
            flags.append("forte errado")
        if row["policy_intrusion"]:
            flags.append("política intrusa")
        first = row["top"][0] if row["top"] else None
        first_text = f"{first['title'][:60]} [{first['match']}]" if first else "—"
        print(f"{row['id']:<10} {verdict:<22} {'; '.join(flags):<28} 1º: {first_text}")

    print("\nResumo")
    labels = {
        "acerto_1": "Acerto no 1º", "acerto_3": "Acerto nos 3 primeiros", "forte_errado": "Forte errado",
        "intrusao_politica": "Política intrusa", "gate_ok": "Outra plataforma recusada",
    }
    names = {"meta": "Meta", "google_ads": "Google Ads", "todas": "Todas as consultas de ajuste",
             "controle": "Controle (não usadas para ajustar)"}
    for platform, name in names.items():
        data = summary[platform]
        print(f"\n  {name}: {data['consultas']} consultas, {data['avaliadas_por_acerto']} avaliadas por acerto, "
              f"{data['aguardando_artigo']} aguardando artigo")
        for key, label in labels.items():
            line = f"    {label:<28} {pct(data[key]):>5}"
            if baseline and platform in baseline:
                before = baseline[platform].get(key)
                if None not in (before, data[key]) and before != data[key]:
                    delta = (data[key] - before) * 100
                    line += f"   (linha de base {pct(before)}, {'▲' if delta > 0 else '▼'} {abs(delta):.0f} pontos)"
            print(line)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--save-baseline", action="store_true")
    parser.add_argument("--compare", action="store_true")
    args = parser.parse_args(argv)

    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    pending = {path for path in fixture.get("pending", {}) if not (ROOT / path).is_file()}
    rows = [evaluate_query(item, pending) for item in fixture["queries"]]
    summary = summarize(rows)

    if args.save_baseline:
        BASELINE.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    baseline = json.loads(BASELINE.read_text(encoding="utf-8")) if args.compare and BASELINE.is_file() else None

    if args.as_json:
        print(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=2))
    else:
        print_report(rows, summary, baseline)
    return 0


if __name__ == "__main__":
    sys.exit(main())
