#!/usr/bin/env python3
"""Valida dossiês legados (Markdown com bloco JSON embutido, schema 1.1).

Dossiês V2 em `clients/{slug}/operacoes/` são delegados para `scripts/dossier.py verify`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
OPERATION_SCHEMA = json.loads((ROOT / "schemas" / "operation-dossier.schema.json").read_text(encoding="utf-8"))
ANALYSIS_SCHEMA = json.loads((ROOT / "schemas" / "analysis.schema.json").read_text(encoding="utf-8"))
ANALYTIC_TYPES = {"auditoria", "analise", "otimizacao", "relatorio"}

META_FULL_LAYERS = {
    "account", "campaign", "adset", "ad_or_creative", "placement_and_device",
    "audience_geo_demographic", "conversion", "measurement", "business", "change_history",
}
GOOGLE_FULL_LAYERS = {
    "account", "campaign", "ad_group", "ad_or_asset", "conversion", "device", "geography",
    "time", "measurement", "business", "change_history", "budget_and_rank",
}
GOOGLE_TYPE_LAYERS = {
    "search": {"keyword", "search_term", "network"},
    "performance_max": {"asset_group", "asset", "product_or_listing_group", "audience_signal_or_insight"},
    "display": {"placement_or_inventory", "audience", "creative_or_asset"},
    "video": {"placement_or_inventory", "audience", "creative_or_asset"},
    "demand_gen": {"placement_or_inventory", "audience", "creative_or_asset"},
    "shopping": {"product_or_listing_group", "feed", "search_term_or_insight"},
}


def extract_payload(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)
    if not match:
        raise ValueError("primeiro bloco JSON do dossiê não encontrado")
    return json.loads(match.group(1))


def expected_layers(analysis: dict) -> dict[str, set[str]]:
    expected: dict[str, set[str]] = {}
    for platform in analysis["active_platforms"]:
        if platform == "meta":
            expected[platform] = set(META_FULL_LAYERS)
            continue
        layers = set(GOOGLE_FULL_LAYERS)
        for campaign_type in analysis["campaign_types"].get("google_ads", []):
            normalized = campaign_type.lower().replace(" ", "_").replace("-", "_")
            if normalized == "pmax":
                normalized = "performance_max"
            layers.update(GOOGLE_TYPE_LAYERS.get(normalized, set()))
        expected[platform] = layers
    return expected


def validate_dossier_payload(payload: dict) -> list[str]:
    errors: list[str] = []
    validator = jsonschema.Draft7Validator(OPERATION_SCHEMA, format_checker=jsonschema.FormatChecker())
    errors.extend(f"schema dossier: {error.message}" for error in validator.iter_errors(payload))
    if errors:
        return errors

    route = payload["route"]
    planned = set(route["planned_skills"])
    executed = set(route["executed_skills"])
    skipped = {item["skill"] for item in route["skipped_skills"]}
    missing_skills = planned - executed - skipped
    if missing_skills:
        errors.append(f"skills planejadas sem execução ou justificativa: {sorted(missing_skills)}")

    analysis = payload.get("analysis")
    if payload["type"] in ANALYTIC_TYPES and analysis is None:
        errors.append("dossiê analítico sem objeto analysis")
        return errors
    if analysis is None:
        return errors

    analysis_validator = jsonschema.Draft7Validator(ANALYSIS_SCHEMA, format_checker=jsonschema.FormatChecker())
    errors.extend(f"schema analysis: {error.message}" for error in analysis_validator.iter_errors(analysis))
    if errors:
        return errors

    record = payload["record_approval"]
    if record["diagnostic_id"] != analysis["diagnostic_id"] or record["diagnostic_version"] != analysis["diagnostic_version"]:
        errors.append("aprovação editorial não corresponde ao diagnóstico persistido")

    if analysis["depth_mode"] == "focused" and not analysis["focus"]:
        errors.append("diagnóstico focused sem foco explícito")

    coverage_keys = {(item["platform"], item["layer"]) for item in analysis["coverage"]}
    if analysis["depth_mode"] == "full":
        for platform, layers in expected_layers(analysis).items():
            missing = sorted(layer for layer in layers if (platform, layer) not in coverage_keys)
            if missing:
                errors.append(f"cobertura full incompleta em {platform}: {missing}")

    evidence_ids = [item["evidence_id"] for item in analysis["evidence"]]
    finding_ids = [item["finding_id"] for item in analysis["findings"]]
    action_ids = [item["action_id"] for item in analysis["actions"]]
    for label, values in (("evidence", evidence_ids), ("finding", finding_ids), ("action", action_ids)):
        if len(values) != len(set(values)):
            errors.append(f"IDs duplicados em {label}")

    evidence_set, finding_set, action_set = set(evidence_ids), set(finding_ids), set(action_ids)
    for finding in analysis["findings"]:
        missing = set(finding["evidence_ids"]) - evidence_set
        if missing:
            errors.append(f"{finding['finding_id']} referencia evidências inexistentes: {sorted(missing)}")
    for action in analysis["actions"]:
        missing = set(action["finding_ids"]) - finding_set
        if missing:
            errors.append(f"{action['action_id']} referencia achados inexistentes: {sorted(missing)}")
    for change in payload["changes"]:
        if set(change["evidence_ids"]) - evidence_set:
            errors.append(f"{change['change_id']} referencia evidência inexistente")
        if set(change["finding_ids"]) - finding_set:
            errors.append(f"{change['change_id']} referencia achado inexistente")
        if set(change["action_ids"]) - action_set:
            errors.append(f"{change['change_id']} referencia ação inexistente")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    if args.path.parent.name == "operacoes":
        # Dossiês V2 (.md + .json em operacoes/) são verificados pelo dossier.py.
        from dossier import main as dossier_main  # noqa: PLC0415

        return dossier_main(["verify", "--path", str(args.path)])
    try:
        payload = extract_payload(args.path)
        errors = validate_dossier_payload(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"DOSSIER INVALID: {exc}")
        return 1
    if errors:
        print("DOSSIER INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("DOSSIER OK: aprovação editorial, cobertura, evidências e rastreabilidade válidas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
