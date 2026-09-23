#!/usr/bin/env python3
"""Teste de roteamento com frases reais (anonimizadas) do gestor.

A classificação de intenção é feita pelo modelo, então este teste tem duas
partes:

- `--check` (determinístico, roda no CI): toda rota esperada em
  `tests/fixtures/routing_eval.json` existe na matriz e resolve sem bloqueio
  para a fonte indicada.
- `--prompt` e `--score` (semiautomático, fora do CI): `--prompt` imprime o
  pedido de classificação para o modelo (ex.: `claude -p "$(python3
  scripts/eval_routing.py --prompt)" > .work/rotas.json`, numa sessão sem
  permissão de escrita); `--score .work/rotas.json` compara as respostas com o
  gabarito. Rode a cada mudança no prompt do agent ou no roteador.

Formato esperado das respostas: lista de objetos
{"id": "r01", "intents": [{"intent": "duvida", "plataformas": ["meta"]}], "fora_do_escopo": false}.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from route_request import load_matrix, resolve_branch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "routing_eval.json"


def load(path: Path = FIXTURE) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check(fixture: dict) -> list[str]:
    matrix = load_matrix()
    intents = matrix["intents"]
    errors: list[str] = []
    for item in fixture["frases"]:
        if item.get("fora_do_escopo"):
            if item["esperado"]:
                errors.append(f"{item['id']}: fora do escopo não pode ter rota esperada")
            continue
        if not item["esperado"]:
            errors.append(f"{item['id']}: sem rota esperada")
        source = item.get("fonte", "connected_read")
        for expected in item["esperado"]:
            intent = expected["intent"]
            if intent not in intents:
                errors.append(f"{item['id']}: intenção inexistente na matriz: {intent}")
                continue
            for alternative in item.get("aceitas", []) + item.get("extras_ok", []):
                if alternative not in intents:
                    errors.append(f"{item['id']}: intenção aceita inexistente: {alternative}")
            for platform in expected["plataformas"]:
                branch = resolve_branch(
                    matrix, intent=intent, platform=platform, source_mode=source,
                    requires_keywords=False, requires_gtm_audit=bool(item.get("requires_gtm_audit")),
                    depth=item.get("profundidade"),
                )
                if branch["status"] != "ready":
                    errors.append(f"{item['id']}: rota {branch['route_id']} bloqueada: {branch['gates']}")
                if item.get("requires_gtm_audit") and intent in {"auditoria", "otimizacao"} and "mensuracao/gtm" not in branch["planned_skills"]:
                    errors.append(f"{item['id']}: rota {branch['route_id']} não planeja a auditoria de GTM")
    return errors


PROMPT = """Você é o roteador do PERFORMANCE ADS IA. Classifique cada pedido abaixo, sem executar nada.

Para cada pedido, devolva as intenções (uma mensagem pode ter mais de uma) e as plataformas de cada uma.
Intenções válidas: {intents}.
Plataformas: "meta", "google_ads" (as duas quando o pedido cobre as duas). Se a frase não disser a plataforma, use a mais provável pelo pedido.
"historico" não tem plataforma (lista vazia). Pedido fora do escopo do agent (SEO, GA4, eKyte, outras plataformas de anúncio, pesquisa geral na internet) tem "fora_do_escopo": true e intents vazio.

Responda somente com JSON válido, uma lista no formato:
[{{"id": "r01", "intents": [{{"intent": "duvida", "plataformas": ["meta"]}}], "fora_do_escopo": false}}]

Pedidos:
{items}
"""


def prompt(fixture: dict) -> str:
    intents = ", ".join(load_matrix()["intents"])
    items = "\n".join(f'{item["id"]}: "{item["frase"]}"' for item in fixture["frases"])
    return PROMPT.format(intents=intents, items=items)


def score(fixture: dict, answers: list[dict]) -> dict:
    by_id = {answer["id"]: answer for answer in answers}
    rows = []
    for item in fixture["frases"]:
        answer = by_id.get(item["id"])
        if answer is None:
            rows.append({"id": item["id"], "ok": False, "motivo": "sem resposta"})
            continue
        if item.get("fora_do_escopo"):
            ok = bool(answer.get("fora_do_escopo"))
            rows.append({"id": item["id"], "ok": ok, "motivo": "" if ok else "deveria ser fora do escopo"})
            continue
        got = {entry["intent"]: set(entry.get("plataformas", [])) for entry in answer.get("intents", [])}
        allowed = {e["intent"] for e in item["esperado"]} | set(item.get("aceitas", [])) | set(item.get("extras_ok", []))
        expected_intents = {e["intent"] for e in item["esperado"]}
        # Uma intenção aceita presente cobre uma esperada ausente (mas não duas).
        spare = [intent for intent in got if intent in set(item.get("aceitas", [])) - expected_intents]
        missing = []
        for e in item["esperado"]:
            if e["intent"] not in got:
                if spare:
                    spare.pop(0)
                else:
                    missing.append(e["intent"])
        extra = [intent for intent in got if intent not in allowed]
        platform_errors = [
            e["intent"] for e in item["esperado"]
            if e["intent"] in got and e["plataformas"] and got[e["intent"]] != set(e["plataformas"])
            and not item.get("plataforma_pela_ficha")
        ]
        multi = len(item["esperado"]) > 1
        multi_ok = not multi or not missing
        ok = not missing and not extra and not platform_errors and multi_ok
        reason = "; ".join(filter(None, [
            f"faltou {missing}" if missing else "",
            f"sobrou {extra}" if extra else "",
            f"plataforma errada em {platform_errors}" if platform_errors else "",
            "pedido com mais de uma intenção não foi separado" if not multi_ok else "",
        ]))
        rows.append({"id": item["id"], "ok": ok, "motivo": reason, "multi": multi})
    total = len(rows)
    multi_rows = [row for row in rows if row.get("multi")]
    return {
        "acerto": round(sum(row["ok"] for row in rows) / total, 3) if total else None,
        "acerto_multi_intencao": round(sum(row["ok"] for row in multi_rows) / len(multi_rows), 3) if multi_rows else None,
        "frases": total,
        "erros": [row for row in rows if not row["ok"]],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="confere se toda rota esperada existe e resolve")
    group.add_argument("--prompt", action="store_true", help="imprime o pedido de classificação para o modelo")
    group.add_argument("--score", type=Path, help="arquivo JSON com as respostas do modelo")
    args = parser.parse_args(argv)

    fixture = load()
    if args.check:
        errors = check(fixture)
        for error in errors:
            print(f"ERRO: {error}")
        if not errors:
            print(f"ROTEAMENTO OK: {len(fixture['frases'])} frases com rota esperada válida")
        return 1 if errors else 0
    if args.prompt:
        print(prompt(fixture))
        return 0
    raw = args.score.read_text(encoding="utf-8")
    # O modelo pode cercar o JSON com texto ou cercas de código: lê a primeira lista válida.
    answers, _ = json.JSONDecoder().raw_decode(raw[raw.index("["):])
    result = score(fixture, answers)
    print(f"Acerto: {result['acerto'] * 100:.0f}% de {result['frases']} frases")
    if result["acerto_multi_intencao"] is not None:
        print(f"Pedidos com mais de uma intenção: {result['acerto_multi_intencao'] * 100:.0f}%")
    for row in result["erros"]:
        print(f"- {row['id']}: {row['motivo']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
