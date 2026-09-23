#!/usr/bin/env python3
"""Resolve a PERFORMANCE ADS IA route from explicit normalized inputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "routing_matrix.json"


def load_matrix() -> dict[str, object]:
    return json.loads(MATRIX_PATH.read_text(encoding="utf-8"))


def condition_matches(
    condition: str,
    *,
    source_mode: str,
    requires_keywords: bool,
    requires_gtm_audit: bool,
) -> bool:
    if condition == "always":
        return True
    if condition.startswith("source_mode="):
        return source_mode == condition.partition("=")[2]
    if condition == "requires_keywords=true":
        return requires_keywords
    if condition == "requires_gtm_audit=true":
        return requires_gtm_audit
    raise ValueError(f"condicao de rota desconhecida: {condition}")


NO_SOURCE_INTENTS = {"duvida", "historico", "configuracao", "onboarding", "planejamento", "criacao"}
# Avaliar uma operação é afirmar se ela funcionou: exige dado da conta ou arquivo, nunca só contexto.
DATA_REQUIRED_INTENTS = {"avaliacao"}


def resolve_branch(
    matrix: dict[str, object],
    *,
    intent: str,
    platform: str,
    source_mode: str,
    requires_keywords: bool,
    requires_gtm_audit: bool = False,
    depth: str | None = None,
) -> dict[str, object]:
    intents = matrix["intents"]
    assert isinstance(intents, dict)
    intent_config = intents.get(intent)
    if not isinstance(intent_config, dict) or platform not in intent_config:
        return {
            "route_id": f"{intent}:{platform}:{source_mode}",
            "platform": platform,
            "source_mode": source_mode,
            "status": "blocked",
            "planned_skills": [],
            "skipped_skills": [],
            "gates": ["intent_platform_not_supported"],
            "final_state": "blocked",
            "output": None,
        }

    route = intent_config[platform]
    assert isinstance(route, dict)
    planned: list[str] = []
    skipped: list[dict[str, str]] = []
    for step in route.get("steps", []):
        skill = step["skill"]
        condition = step["when"]
        if condition_matches(
            condition,
            source_mode=source_mode,
            requires_keywords=requires_keywords,
            requires_gtm_audit=requires_gtm_audit,
        ):
            if skill not in planned:
                planned.append(skill)
        else:
            skipped.append({"skill": skill, "reason": f"condition_not_met:{condition}"})

    gates: list[str] = []
    status = "ready"
    if source_mode == "unavailable" and intent not in NO_SOURCE_INTENTS:
        status = "blocked"
        gates.append("required_source_unavailable")

    if intent in DATA_REQUIRED_INTENTS and source_mode == "context_only":
        status = "blocked"
        gates.append("evaluation_requires_account_or_file_data")

    if platform == "google_ads" and intent == "execucao":
        status = "blocked"
        gates.append("google_ads_write_manual_only")

    dossier_policy = matrix.get("dossier_policy", {})
    candidate_intents = set(dossier_policy.get("candidate_intents", []))
    no_dossier_intents = set(dossier_policy.get("no_dossier_intents", []))
    requires_editorial_approval = intent in candidate_intents
    default_depth = matrix.get("default_depth", {})
    assert isinstance(default_depth, dict)

    if intent in no_dossier_intents:
        return {
            "route_id": f"{intent}:{platform}:{source_mode}",
            "platform": platform,
            "source_mode": source_mode,
            "status": status,
            "planned_skills": planned if status == "ready" else [],
            "skipped_skills": skipped,
            "gates": gates,
            "depth": depth or default_depth.get(intent),
            "final_state": route.get("final_state"),
            "output": route.get("output"),
            "delivery_state": "chat_only",
            "dossier_persistence": "none",
            "dossier_state_after_approval": None,
        }

    return {
        "route_id": f"{intent}:{platform}:{source_mode}",
        "platform": platform,
        "source_mode": source_mode,
        "status": status,
        "planned_skills": planned if status == "ready" else [],
        "skipped_skills": skipped,
        "gates": gates,
        "depth": depth or default_depth.get(intent),
        "final_state": route.get("final_state"),
        "output": route.get("output"),
        "delivery_state": (
            dossier_policy.get("candidate_state")
            if requires_editorial_approval and status == "ready"
            else route.get("final_state")
        ),
        "dossier_persistence": (
            dossier_policy.get("persistence")
            if requires_editorial_approval
            else "existing_dossier_required"
        ),
        "dossier_state_after_approval": route.get("final_state"),
    }


def parser() -> argparse.ArgumentParser:
    route_parser = argparse.ArgumentParser(description=__doc__)
    route_parser.add_argument("--intent", required=True)
    route_parser.add_argument(
        "--platform",
        required=True,
        choices=["meta", "google_ads", "both", "undefined"],
    )
    route_parser.add_argument("--source-mode")
    route_parser.add_argument("--meta-source-mode")
    route_parser.add_argument("--google-source-mode")
    route_parser.add_argument("--requires-keywords", action="store_true")
    route_parser.add_argument("--requires-gtm-audit", action="store_true")
    route_parser.add_argument(
        "--depth",
        choices=["quick", "focused", "full"],
        help="sobrescreve a profundidade padrão (use full só em auditoria ou quando o gestor pedir análise completa)",
    )
    route_parser.add_argument("--json", action="store_true", dest="as_json")
    return route_parser


def main() -> int:
    args = parser().parse_args()
    matrix = load_matrix()
    intents = matrix.get("intents", {})
    if args.intent not in intents:
        print(f"ERRO: intencao desconhecida: {args.intent}", file=sys.stderr)
        return 2

    if args.platform == "undefined":
        payload = {
            "router_version": matrix["version"],
            "intent": args.intent,
            "status": "blocked",
            "branches": [],
            "gates": ["platform_undefined"],
        }
    else:
        platforms = ["meta", "google_ads"] if args.platform == "both" else [args.platform]
        branches: list[dict[str, object]] = []
        for platform in platforms:
            if args.platform == "both":
                source_mode = (
                    args.meta_source_mode if platform == "meta" else args.google_source_mode
                )
            else:
                source_mode = args.source_mode
            if source_mode not in matrix["source_modes"]:
                print(
                    f"ERRO: informe source_mode valido para {platform}",
                    file=sys.stderr,
                )
                return 2
            branches.append(
                resolve_branch(
                    matrix,
                    intent=args.intent,
                    platform=platform,
                    source_mode=source_mode,
                    requires_keywords=args.requires_keywords,
                    requires_gtm_audit=args.requires_gtm_audit,
                    depth=args.depth,
                )
            )
        if args.platform == "both":
            # Em pedido multicanal, uma intenção que só existe numa plataforma
            # (ex: pesquisa de palavras-chave) não bloqueia a outra.
            supported = [b for b in branches if "intent_platform_not_supported" not in b["gates"]]
            if supported and len(supported) < len(branches):
                for branch in branches:
                    if branch not in supported:
                        branch["status"] = "not_applicable"
                branches = supported + [b for b in branches if b not in supported]
        active = [branch for branch in branches if branch["status"] != "not_applicable"]
        status = "ready" if active and all(branch["status"] == "ready" for branch in active) else "blocked"
        payload = {
            "router_version": matrix["version"],
            "intent": args.intent,
            "status": status,
            "branches": branches,
            "gates": [gate for branch in active for gate in branch["gates"]],
        }

    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Rota: {payload['intent']} | status: {payload['status']}")
        for branch in payload.get("branches", []):
            if branch["status"] == "not_applicable":
                print(f"- {branch['route_id']}: não se aplica a esta plataforma")
                continue
            depth = f" | profundidade: {branch['depth']}" if branch.get("depth") else ""
            print(f"- {branch['route_id']}: {', '.join(branch['planned_skills']) or 'nenhuma skill'}{depth}")
        for gate in payload.get("gates", []):
            print(f"  gate: {gate}")
    return 0 if payload["status"] == "ready" else 3


if __name__ == "__main__":
    sys.exit(main())
