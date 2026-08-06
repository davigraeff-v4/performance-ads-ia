#!/usr/bin/env python3
"""Valida contratos acionáveis e fixtures sintéticas."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema


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
        del shallow["findings"][0]["next_action"]
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


if __name__ == "__main__":
    unittest.main()
