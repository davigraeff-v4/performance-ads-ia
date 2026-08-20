#!/usr/bin/env python3
"""Structural validation for the local PERFORMANCE ADS IA model."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
META_HELP_BASE = ROOT / "knowledge" / "meta-help-center"
EXPECTED_META_HELP_ARTICLES = 151
GOOGLE_HELP_BASE = ROOT / "knowledge" / "official-google" / "help-center"
VECTOR_INDEX_DIR = ROOT / "knowledge" / ".vector-index"
VECTOR_INDEX_PLATFORMS = {
    "meta": ("meta-help-center", META_HELP_BASE),
    "google_ads": ("google-ads-help-center", GOOGLE_HELP_BASE),
}
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
    "16-google-ads-account-connection",
    "17-google-ads-official-retrieval",
    "18-google-ads-keyword-research",
    "19-google-ads-campaign-strategy",
    "20-google-ads-campaign-architecture",
    "21-google-ads-budget-bidding-conversions",
    "22-google-ads-creative-assets-landing-page",
    "23-google-ads-campaign-build-plan",
    "24-google-ads-performance-diagnosis",
    "25-performance-ads-router",
    "26-gtm-tracking-audit-fix",
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
    "pesquisar-palavras-chave.md",
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


def validate_openai_yaml(path: Path, skill_name: str, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    required = ["display_name:", "short_description:", "default_prompt:"]
    for key in required:
        if key not in text:
            fail(errors, f"{key[:-1]} ausente: {path.relative_to(ROOT)}")
    if f"${skill_name}" not in text:
        fail(errors, f"default_prompt não menciona ${skill_name}: {path.relative_to(ROOT)}")
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


def validate_google_help_center(errors: list[str]) -> None:
    index = GOOGLE_HELP_BASE / "INDEX.md"
    if not index.is_file():
        return fail(errors, "índice da Central Google Ads ausente")

    article_paths = sorted(
        path for path in GOOGLE_HELP_BASE.glob("**/*.md") if path.name != "INDEX.md"
    )
    titles: set[str] = set()
    urls: set[str] = set()
    answer_ids: set[str] = set()
    required_keys = {
        "title", "url", "answer_id", "categoria", "topico", "subtopico",
        "fonte", "idioma", "extraido_em", "traducao_por_ia", "formato",
    }
    for path in article_paths:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not match:
            fail(errors, f"frontmatter Google Ads ausente: {path.relative_to(ROOT)}")
            continue
        metadata: dict[str, str] = {}
        for line in match.group(1).splitlines():
            key, separator, value = line.partition(":")
            if separator:
                metadata[key.strip()] = value.strip().strip('"\'')
        missing = required_keys - set(metadata)
        if missing:
            fail(
                errors,
                f"metadados Google Ads ausentes em {path.relative_to(ROOT)}: {sorted(missing)}",
            )

        title = metadata.get("title", "").casefold()
        url = metadata.get("url", "")
        answer_id = metadata.get("answer_id", "")
        if not title:
            fail(errors, f"título Google Ads vazio: {path.relative_to(ROOT)}")
        elif title in titles:
            fail(errors, f"título Google Ads duplicado: {metadata.get('title', '')}")
        titles.add(title)

        expected_url_prefix = f"https://support.google.com/google-ads/answer/{answer_id}"
        if not answer_id.isdigit() or not url.startswith(expected_url_prefix):
            fail(errors, f"URL/answer_id Google Ads inválido: {path.relative_to(ROOT)}")
        elif url in urls or answer_id in answer_ids:
            fail(errors, f"URL ou answer_id Google Ads duplicado: {url}")
        urls.add(url)
        answer_ids.add(answer_id)

    index_text = index.read_text(encoding="utf-8")
    declared_match = re.search(r"Cobertura atual: (\d+) artigos", index_text)
    if not declared_match:
        fail(errors, "total ausente no índice da Central Google Ads")
    elif int(declared_match.group(1)) != len(article_paths):
        fail(
            errors,
            "total declarado no índice da Central Google Ads está divergente: "
            f"{declared_match.group(1)} declarado, {len(article_paths)} arquivos",
        )


def validate_vector_index(errors: list[str]) -> None:
    """Índice vetorial é versionado (artefato pequeno, ~2.6MB) para o time
    já receber o RAG pronto no clone/pull. Ausência total não é falha (o
    repositório funciona em modo lexical-only via fallback gracioso). Se
    existir, precisa ser consistente: sem chunk órfão, sem artigo esquecido,
    sem vazamento de plataforma, sem indexar clients/, e sem desatualização
    silenciosa em relação aos .md fonte (hash do manifest)."""
    if not VECTOR_INDEX_DIR.is_dir():
        return

    sys.path.insert(0, str(ROOT / "scripts"))
    from _help_index_common import load_articles as _load_articles  # noqa: PLC0415
    from build_knowledge_vector_index import (  # noqa: PLC0415
        EMBEDDING_MODEL,
        PLATFORM_CONFIGS,
        source_hash,
    )

    for platform, (slug, base) in VECTOR_INDEX_PLATFORMS.items():
        meta_path = VECTOR_INDEX_DIR / f"{slug}-meta.json"
        vectors_path = VECTOR_INDEX_DIR / f"{slug}.npz"
        manifest_path = VECTOR_INDEX_DIR / f"{slug}-manifest.json"
        if not meta_path.is_file() and not vectors_path.is_file():
            continue
        if meta_path.is_file() != vectors_path.is_file():
            fail(errors, f"índice vetorial incompleto para {platform}: vetores e metadados devem existir juntos")
            continue

        manifest: dict[str, object] = {}
        if manifest_path.is_file():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            config = PLATFORM_CONFIGS[platform]
            current_articles = _load_articles(
                root=ROOT,
                base=config["base"],
                link_pattern=config["link_pattern"],
                date_pattern=config["date_pattern"],
            )
            if source_hash(current_articles) != manifest.get("source_hash"):
                fail(
                    errors,
                    f"índice vetorial {platform} desatualizado em relação aos artigos fonte "
                    f"(rode: python3 scripts/build_knowledge_vector_index.py --platform {platform} --force)",
                )
            if manifest.get("model") != EMBEDDING_MODEL:
                fail(
                    errors,
                    f"índice vetorial {platform} foi gerado com um modelo diferente do configurado "
                    f"({manifest.get('model')!r} vs {EMBEDDING_MODEL!r})",
                )
            manifest_fastembed_version = manifest.get("fastembed_version")
            if manifest_fastembed_version:
                try:
                    import fastembed  # noqa: PLC0415

                    installed_version = fastembed.__version__
                except ImportError:
                    installed_version = None
                if installed_version and installed_version != manifest_fastembed_version:
                    fail(
                        errors,
                        f"fastembed instalado ({installed_version}) diverge da versão que gerou o índice "
                        f"{platform} ({manifest_fastembed_version}); reinstale a versão fixada em "
                        "requirements-dev.txt ou reconstrua o índice com --force",
                    )
        else:
            fail(errors, f"manifest ausente para o índice vetorial {platform}")

        chunks = json.loads(meta_path.read_text(encoding="utf-8"))
        if not chunks:
            fail(errors, f"índice vetorial vazio para {platform}")
            continue

        articles_on_disk = {
            str(path.relative_to(ROOT)) for path in base.glob("**/*.md") if path.name != "INDEX.md"
        }
        chunk_paths: set[str] = set()
        for chunk in chunks:
            if chunk.get("platform") != platform:
                fail(errors, f"chunk com plataforma divergente no índice {platform}: {chunk.get('path')}")
            path = chunk.get("path", "")
            if not path.startswith(f"knowledge/{'meta-help-center' if platform == 'meta' else 'official-google/help-center'}/"):
                fail(errors, f"chunk fora da base esperada de {platform}: {path}")
            if path.startswith("clients/"):
                fail(errors, f"índice vetorial indexou dado de cliente (proibido): {path}")
            if path not in articles_on_disk:
                fail(errors, f"chunk órfão no índice vetorial {platform} (artigo inexistente): {path}")
            chunk_paths.add(path)

        missing_articles = sorted(articles_on_disk - chunk_paths)
        if missing_articles:
            shown = missing_articles[:5]
            extra = len(missing_articles) - len(shown)
            suffix = f" (+{extra} outros)" if extra > 0 else ""
            fail(errors, f"artigos sem nenhum chunk no índice vetorial {platform}: {shown}{suffix}")

        try:
            import numpy as np

            vectors = np.load(vectors_path)["vectors"]
        except Exception as exc:  # noqa: BLE001
            fail(errors, f"índice vetorial {platform} corrompido: {exc}")
            continue
        if vectors.shape[0] != len(chunks):
            fail(
                errors,
                f"contagem de vetores ({vectors.shape[0]}) diverge da contagem de metadados "
                f"({len(chunks)}) para {platform}",
            )
        manifest_dim = manifest.get("embedding_dim")
        if manifest_dim is not None and vectors.shape[1] != manifest_dim:
            fail(
                errors,
                f"dimensão dos vetores ({vectors.shape[1]}) diverge da dimensão declarada no "
                f"manifest ({manifest_dim}) para {platform}",
            )


def main() -> int:
    errors: list[str] = []
    required = [
        "AGENTS.md",
        "CLAUDE.md",
        "README.md",
        "PRD-PERFORMANCE-ADS-IA.md",
        "CONTRATO-OPERACIONAL.md",
        "dependency_graph.json",
        "routing_matrix.json",
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
        openai_yaml = ROOT / "skills" / name / "agents" / "openai.yaml"
        if not openai_yaml.is_file():
            fail(errors, f"openai.yaml ausente: {name}")
        else:
            validate_openai_yaml(openai_yaml, name, errors)

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

    matrix = json.loads((ROOT / "routing_matrix.json").read_text(encoding="utf-8"))
    if matrix.get("version") != "1.1.0":
        fail(errors, "versão inesperada da matriz de roteamento")
    declared_platforms = set(matrix.get("platforms", []))
    if declared_platforms != {"meta", "google_ads"}:
        fail(errors, f"plataformas declaradas na matriz são inválidas: {sorted(declared_platforms)}")
    policy = matrix.get("dossier_policy", {})
    if policy.get("candidate_state") != "awaiting_record_approval" or policy.get("persistence") != "after_editorial_approval":
        fail(errors, "política chat-first/dossiê aprovado ausente ou inválida")
    supported_conditions = {"always", "source_mode=connected_read", "requires_keywords=true", "requires_gtm_audit=true"}
    for intent, platforms in matrix.get("intents", {}).items():
        for platform, route in platforms.items():
            if platform not in declared_platforms:
                fail(errors, f"plataforma não declarada na rota {intent}:{platform}")
            if not isinstance(route.get("output"), str) or not route["output"]:
                fail(errors, f"contrato de saída ausente na rota {intent}:{platform}")
            for step in route.get("steps", []):
                if step.get("skill") not in EXPECTED_SKILLS:
                    fail(errors, f"skill desconhecida na rota {intent}:{platform}: {step.get('skill')}")
                if step.get("when") not in supported_conditions:
                    fail(errors, f"condição desconhecida na rota {intent}:{platform}: {step.get('when')}")

    for discovery_root in [ROOT / ".agents" / "skills", ROOT / ".claude" / "skills"]:
        router_link = discovery_root / "25-performance-ads-router"
        if not router_link.is_dir() or not (router_link / "SKILL.md").is_file():
            fail(errors, f"roteador não descobrível em {discovery_root.relative_to(ROOT)}")

    command_names = {path.name for path in (ROOT / ".claude" / "commands").glob("*.md")}
    if command_names != EXPECTED_COMMANDS:
        fail(errors, f"comandos divergentes: {sorted(command_names ^ EXPECTED_COMMANDS)}")

    required_references = [
        "knowledge/README.md",
        "knowledge/methodology/diagnostic-coverage-contract.md",
        "templates/dossie-operacao.md",
        "quality/analysis-checklist.md",
        "quality/execution-checklist.md",
        "examples/synthetic/operation-approved.json",
        "examples/synthetic/analysis-actionable.json",
        "scripts/route_request.py",
        "scripts/validate_dossier.py",
        "scripts/validate_all.py",
        "tests/test_meta_help_search.py",
        "tests/test_google_ads_help_search.py",
        "tests/test_multichannel_structure.py",
        "tests/test_routing.py",
        "tests/test_schema_contracts.py",
        "knowledge/official-google/source-catalog.md",
        "knowledge/official-google/google-ads-mcp-and-api.md",
        "knowledge/official-google/help-center/INDEX.md",
        "scripts/build_google_ads_help_index.py",
        "scripts/search_google_ads_help.py",
        "scripts/_help_index_common.py",
        "scripts/_vector_search.py",
        "scripts/build_knowledge_vector_index.py",
        "tests/test_vector_search_isolation.py",
        "knowledge/google-ads/keyword-research-methodology.md",
        "templates/pesquisa-palavras-chave.md",
        "integrations/google_ads_extended/pyproject.toml",
        "integrations/google_ads_extended/src/performance_ads_google_ads_extended/config.py",
        "integrations/google_ads_extended/src/performance_ads_google_ads_extended/server.py",
        "integrations/google_ads_extended/tests/test_config.py",
        "integrations/google_ads_extended/tests/test_server_registration.py",
    ]
    for relative in required_references:
        if not (ROOT / relative).is_file():
            fail(errors, f"referência obrigatória ausente: {relative}")

    validate_meta_help_center(errors)
    validate_google_help_center(errors)
    validate_vector_index(errors)

    schemas: dict[str, dict[str, object]] = {}
    for schema in sorted((ROOT / "schemas").glob("*.json")):
        try:
            schemas[schema.name] = json.loads(schema.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"JSON inválido {schema.name}: {exc}")

    try:
        import jsonschema
    except ImportError:
        fail(errors, "dependência jsonschema ausente; instale requirements-dev.txt")
    else:
        fixture_pairs = [
            ("analysis.schema.json", "examples/synthetic/analysis-actionable.json"),
            ("operation-dossier.schema.json", "examples/synthetic/operation-approved.json"),
        ]
        for schema_name, fixture_path in fixture_pairs:
            try:
                jsonschema.Draft7Validator.check_schema(schemas[schema_name])
                fixture = json.loads((ROOT / fixture_path).read_text(encoding="utf-8"))
                jsonschema.validate(fixture, schemas[schema_name], format_checker=jsonschema.FormatChecker())
            except (KeyError, jsonschema.SchemaError, jsonschema.ValidationError) as exc:
                fail(errors, f"contrato inválido {schema_name} / {fixture_path}: {exc.message if hasattr(exc, 'message') else exc}")

    sensitive = re.compile(
        r"(?:access[_-]?token|client[_-]?secret|developer[_-]?token)\s*[:=]\s*[\"']?(?!SEU_|YOUR_|\$\{|<)[A-Za-z0-9._-]{12,}"
        r"|bearer\s+[A-Za-z0-9._-]{12,}",
        re.I,
    )
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
        f"VALIDATION OK: {len(EXPECTED_SKILLS)} skills (26 módulos + roteador), "
        f"{EXPECTED_META_HELP_ARTICLES} artigos Meta, base Google Ads e schemas JSON válidos"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
