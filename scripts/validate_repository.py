#!/usr/bin/env python3
"""Structural validation for the local META PERFORMANCE IA model."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
META_HELP_BASE = ROOT / "knowledge" / "meta-help-center"
EXPECTED_META_HELP_ARTICLES = 151
EXPECTED_SKILLS = {
    "00-configuracao-mcp",
    "01-client-campaign-intake",
    "02-meta-account-connection",
    "03-measurement-data-quality",
    "04-goals-kpis-baseline",
    "05-campaign-strategy",
    "06-account-campaign-architecture",
    "07-audience-strategy",
    "08-budget-bidding-allocation",
    "09-creative-performance-brief",
    "10-campaign-build-plan",
    "11-performance-diagnosis",
    "12-optimization-change-set",
    "13-approved-change-executor",
    "14-reporting-memory-learning",
    "15-meta-help-center-retrieval",
}
EXPECTED_COMMANDS = {
    "configuracao-mcp.md",
    "novo-cliente.md",
    "planejar-campanha.md",
    "criar-campanha.md",
    "auditar-conta.md",
    "analisar-campanha.md",
    "otimizar-campanha.md",
    "relatorio-performance.md",
    "aprovar-operacao.md",
    "executar-operacao.md",
    "reverter-operacao.md",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_frontmatter(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return fail(errors, f"frontmatter ausente: {path.relative_to(ROOT)}")
    keys = [line.split(":", 1)[0].strip() for line in match.group(1).splitlines() if ":" in line]
    if keys != ["name", "description"]:
        fail(errors, f"frontmatter deve conter somente name/description: {path.relative_to(ROOT)}")
    expected = path.parent.name
    if f"name: {expected}" not in match.group(0):
        fail(errors, f"name não corresponde à pasta: {path.relative_to(ROOT)}")
    if "TODO" in text:
        fail(errors, f"TODO remanescente: {path.relative_to(ROOT)}")


def validate_meta_help_center(errors: list[str]) -> None:
    index = META_HELP_BASE / "INDEX.md"
    if not index.is_file():
        return fail(errors, "índice da Central Meta ausente")

    article_paths = sorted(META_HELP_BASE.glob("*/*.md"))
    if len(article_paths) != EXPECTED_META_HELP_ARTICLES:
        fail(
            errors,
            f"quantidade de artigos Meta divergente: {len(article_paths)} "
            f"(esperado {EXPECTED_META_HELP_ARTICLES})",
        )

    titles: set[str] = set()
    urls: set[str] = set()
    required_keys = {"title", "url", "categoria", "fonte", "idioma", "extraido_em"}
    for path in article_paths:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not match:
            fail(errors, f"frontmatter Meta ausente: {path.relative_to(ROOT)}")
            continue
        metadata: dict[str, str] = {}
        for line in match.group(1).splitlines():
            key, separator, value = line.partition(":")
            if separator:
                metadata[key.strip()] = value.strip().strip('"\'')
        missing = required_keys - set(metadata)
        if missing:
            fail(errors, f"metadados Meta ausentes em {path.relative_to(ROOT)}: {sorted(missing)}")
        title = metadata.get("title", "").casefold()
        url = metadata.get("url", "")
        if not title:
            fail(errors, f"título Meta vazio: {path.relative_to(ROOT)}")
        elif title in titles:
            fail(errors, f"título Meta duplicado: {metadata.get('title', '')}")
        titles.add(title)
        if not url.startswith("https://www.facebook.com/business/help/"):
            fail(errors, f"URL Meta inválida: {path.relative_to(ROOT)}")
        elif url in urls:
            fail(errors, f"URL Meta duplicada: {url}")
        urls.add(url)

    index_text = index.read_text(encoding="utf-8")
    if f"Total: {EXPECTED_META_HELP_ARTICLES} artigos" not in index_text:
        fail(errors, "total declarado no índice da Central Meta está divergente")


def main() -> int:
    errors: list[str] = []
    required = [
        "AGENTS.md",
        "CLAUDE.md",
        "README.md",
        "PRD-META-PERFORMANCE-IA.md",
        "CONTRATO-OPERACIONAL.md",
        "dependency_graph.json",
        ".gitignore",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            fail(errors, f"arquivo obrigatório ausente: {relative}")

    skill_dirs = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    if skill_dirs != EXPECTED_SKILLS:
        fail(errors, f"skills divergentes: {sorted(skill_dirs ^ EXPECTED_SKILLS)}")
    for name in sorted(EXPECTED_SKILLS):
        validate_frontmatter(ROOT / "skills" / name / "SKILL.md", errors)
        if not (ROOT / "skills" / name / "agents" / "openai.yaml").is_file():
            fail(errors, f"openai.yaml ausente: {name}")

    graph = json.loads((ROOT / "dependency_graph.json").read_text(encoding="utf-8"))
    if set(graph) != EXPECTED_SKILLS:
        fail(errors, "dependency_graph não cobre exatamente as skills")
    for name, deps in graph.items():
        unknown = set(deps) - EXPECTED_SKILLS
        if unknown:
            fail(errors, f"dependências desconhecidas em {name}: {sorted(unknown)}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visiting:
            fail(errors, f"ciclo detectado no dependency_graph em {name}")
            return
        if name in visited:
            return
        visiting.add(name)
        for dependency in graph[name]:
            visit(dependency)
        visiting.remove(name)
        visited.add(name)

    for name in graph:
        visit(name)

    command_names = {path.name for path in (ROOT / ".claude" / "commands").glob("*.md")}
    if command_names != EXPECTED_COMMANDS:
        fail(errors, f"comandos divergentes: {sorted(command_names ^ EXPECTED_COMMANDS)}")

    required_references = [
        "knowledge/README.md",
        "templates/dossie-operacao.md",
        "quality/analysis-checklist.md",
        "quality/execution-checklist.md",
        "examples/synthetic/operation-approved.json",
        "tests/test_meta_help_search.py",
    ]
    for relative in required_references:
        if not (ROOT / relative).is_file():
            fail(errors, f"referência obrigatória ausente: {relative}")

    validate_meta_help_center(errors)

    for schema in sorted((ROOT / "schemas").glob("*.json")):
        try:
            json.loads(schema.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"JSON inválido {schema.name}: {exc}")

    sensitive = re.compile(r"(?:access[_-]?token|client[_-]?secret|bearer\s+[A-Za-z0-9._-]{12,})", re.I)
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".yaml", ".toml", ".py"}:
            continue
        if path.is_relative_to(META_HELP_BASE):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if sensitive.search(text):
            fail(errors, f"possível segredo em {path.relative_to(ROOT)}")

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"VALIDATION OK: {len(EXPECTED_SKILLS)} skills, "
        f"{EXPECTED_META_HELP_ARTICLES} artigos Meta e schemas JSON válidos"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
