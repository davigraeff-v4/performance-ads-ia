#!/usr/bin/env python3
"""Valida contratos acionáveis e fixtures sintéticas."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema

from scripts.validate_dossier import validate_dossier_payload


ROOT = Path(__file__).resolve().parents[1]


class SchemaContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.analysis_schema = json.loads((ROOT / "schemas/analysis.schema.json").read_text(encoding="utf-8"))
        cls.dossier_schema = json.loads((ROOT / "schemas/operation-dossier.schema.json").read_text(encoding="utf-8"))
        cls.analysis = json.loads((ROOT / "examples/synthetic/analysis-actionable.json").read_text(encoding="utf-8"))
        cls.dossier = json.loads((ROOT / "examples/synthetic/operation-approved.json").read_text(encoding="utf-8"))

    def test_schemas_and_fixtures_are_valid(self) -> None:
        for schema, fixture in [(self.analysis_schema, self.analysis), (self.dossier_schema, self.dossier)]:
            jsonschema.Draft7Validator.check_schema(schema)
            jsonschema.validate(fixture, schema, format_checker=jsonschema.FormatChecker())

    def test_shallow_finding_is_rejected(self) -> None:
        shallow = copy.deepcopy(self.analysis)
        del shallow["findings"][0]["evidence_ids"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(shallow, self.analysis_schema)

    def test_untraceable_change_is_rejected(self) -> None:
        untraceable = copy.deepcopy(self.dossier)
        del untraceable["changes"][0]["finding_ids"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(untraceable, self.dossier_schema)

    def test_route_trace_is_required(self) -> None:
        no_route = copy.deepcopy(self.dossier)
        del no_route["route"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(no_route, self.dossier_schema)

    def test_output_contract_is_required(self) -> None:
        no_output_contract = copy.deepcopy(self.dossier)
        del no_output_contract["route"]["output_contracts"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(no_output_contract, self.dossier_schema)

    def test_editorial_approval_is_required_before_dossier_exists(self) -> None:
        no_record_approval = copy.deepcopy(self.dossier)
        del no_record_approval["record_approval"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(no_record_approval, self.dossier_schema)

    def test_full_diagnostic_has_coverage_and_traceability(self) -> None:
        dossier = copy.deepcopy(self.dossier)
        dossier["analysis"] = copy.deepcopy(self.analysis)
        self.assertEqual(validate_dossier_payload(dossier), [])

    def test_missing_full_layer_is_rejected(self) -> None:
        dossier = copy.deepcopy(self.dossier)
        dossier["analysis"] = copy.deepcopy(self.analysis)
        dossier["analysis"]["coverage"] = [
            item for item in dossier["analysis"]["coverage"] if item["layer"] != "search_term"
        ]
        errors = validate_dossier_payload(dossier)
        self.assertTrue(any("cobertura full incompleta" in error and "search_term" in error for error in errors))

    def test_planned_skill_cannot_disappear_silently(self) -> None:
        dossier = copy.deepcopy(self.dossier)
        dossier["analysis"] = copy.deepcopy(self.analysis)
        dossier["route"]["planned_skills"].append("17-google-ads-official-retrieval")
        errors = validate_dossier_payload(dossier)
        self.assertTrue(any("skills planejadas sem execução" in error for error in errors))

    def test_change_must_reference_existing_action_finding_and_evidence(self) -> None:
        dossier = copy.deepcopy(self.dossier)
        dossier["analysis"] = copy.deepcopy(self.analysis)
        dossier["changes"][0]["action_ids"] = ["act-inexistente"]
        errors = validate_dossier_payload(dossier)
        self.assertTrue(any("referencia ação inexistente" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
