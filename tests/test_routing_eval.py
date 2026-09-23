#!/usr/bin/env python3
"""As rotas esperadas do teste de roteamento existem e resolvem (a classificação em si é do modelo e fica fora do CI)."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import eval_routing  # noqa: E402


class RoutingEvalFixtureTests(unittest.TestCase):
    def test_every_expected_route_exists_and_resolves(self) -> None:
        self.assertEqual(eval_routing.check(eval_routing.load()), [])

    def test_fixture_is_anonymized(self) -> None:
        text = eval_routing.FIXTURE.read_text(encoding="utf-8")
        for forbidden in ("power test", "castelo", "prado", "alientech", "movimak", "scann", "boutique", "centro sul",
                          "cadeira e cia", "vanzella", "dmf", "http", "gtm-"):
            self.assertNotIn(forbidden, text.lower())
        self.assertNotRegex(text, r"\d{3}-\d{3}-\d{4}|\d{10,}")

    def test_scoring_does_not_let_an_extra_intent_hide_a_missing_one(self) -> None:
        fixture = {"frases": [{"id": "x", "frase": "compara com a última otimização",
                               "esperado": [{"intent": "avaliacao", "plataformas": ["meta"]}, {"intent": "otimizacao", "plataformas": ["meta"]}],
                               "extras_ok": ["historico"]}]}
        answers = [{"id": "x", "intents": [{"intent": "historico", "plataformas": []}, {"intent": "otimizacao", "plataformas": ["meta"]}]}]
        result = eval_routing.score(fixture, answers)
        self.assertEqual(result["acerto"], 0.0)
        answers[0]["intents"].append({"intent": "avaliacao", "plataformas": ["meta"]})
        self.assertEqual(eval_routing.score(fixture, answers)["acerto"], 1.0)


if __name__ == "__main__":
    unittest.main()
