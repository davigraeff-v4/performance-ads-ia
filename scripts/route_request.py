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


def resolve_branch(
    matrix: dict[str, object],
    *,
    intent: str,
    platform: str,
    source_mode: str,
    requires_keywords: bool,
    requires_gtm_audit: bool = False,
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
    if source_mode == "unavailable" and intent not in {
        "configuracao",
        "onboarding",
        "planejamento",
        "criacao",
    }:
        status = "blocked"
        gates.append("required_source_unavailable")

    if platform == "google_ads" and intent == "execucao":
        status = "blocked"
        gates.append("google_ads_write_manual_only")

    dossier_policy = matrix.get("dossier_policy", {})
    candidate_intents = set(dossier_policy.get("candidate_intents", []))
    requires_editorial_approval = intent in candidate_intents

    return {
        "route_id": f"{intent}:{platform}:{source_mode}",
        "platform": platform,
        "source_mode": source_mode,
        "status": status,
        "planned_skills": planned if status == "ready" else [],
        "skipped_skills": skipped,
        "gates": gates,
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
                )
            )
        status = "ready" if all(branch["status"] == "ready" for branch in branches) else "blocked"
        payload = {
            "router_version": matrix["version"],
            "intent": args.intent,
            "status": status,
            "branches": branches,
            "gates": [gate for branch in branches for gate in branch["gates"]],
        }

    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Rota: {payload['intent']} | status: {payload['status']}")
        for branch in payload.get("branches", []):
            print(f"- {branch['route_id']}: {', '.join(branch['planned_skills']) or 'nenhuma skill'}")
        for gate in payload.get("gates", []):
            print(f"  gate: {gate}")
    return 0 if payload["status"] == "ready" else 3


if __name__ == "__main__":
    sys.exit(main())
