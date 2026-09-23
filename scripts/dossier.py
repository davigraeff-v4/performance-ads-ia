#!/usr/bin/env python3
"""Ciclo de vida dos dossiês V2: criar, revisar, aprovar, registrar execução,
avaliar, renderizar e verificar.

Cada operação vive em dois arquivos dentro de `clients/{slug}/operacoes/`:

- `{nome}.md`: o dossiê para ler. O texto aprovado no chat fica entre os
  marcadores `corpo-aprovado`; o resto (mudanças, andamento, dados técnicos) é
  gerado a partir do JSON e regenerado a cada mudança de estado.
- `{nome}.json`: o registro de máquina, validado por
  `schemas/operation-v2.schema.json`.

O agent nunca escreve esses arquivos à mão: ele prepara um spec (JSON) e um
corpo (Markdown) em `.work/` e chama este script. Hashes, status e narrativa
de andamento são calculados aqui, nunca pelo modelo.

Dossiês legados (Markdown com bloco JSON embutido, na raiz da pasta do
cliente) permanecem somente leitura; `migrate` extrai um rascunho V2 deles.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from hash_change_set import canonical_payload  # noqa: E402

SCHEMA_PATH = ROOT / "schemas" / "operation-v2.schema.json"
MATRIX_PATH = ROOT / "routing_matrix.json"
DEFAULT_CLIENTS_DIR = ROOT / "clients"
WORK_DIR = ROOT / ".work"
OPERATIONS_DIRNAME = "operacoes"
TZ = ZoneInfo("America/Sao_Paulo")

BODY_START = "<!-- corpo-aprovado:inicio -->"
BODY_END = "<!-- corpo-aprovado:fim -->"
CHANGES_MARKER = "<!-- mudancas -->"
CHANGES_START = "<!-- mudancas:inicio -->"
CHANGES_END = "<!-- mudancas:fim -->"

KNOWLEDGE_SKILLS = {"15-meta-help-center-retrieval", "17-google-ads-official-retrieval"}
# Verbos de exclusão/arquivamento de ativo. "Excluir compradores do público" é
# segmentação legítima, por isso a regra dura vale só para a reversão e para
# valores de status; no título e na justificativa vira alerta.
DELETION_VERBS = re.compile(
    r"\b(excluir|exclua|excluindo|deletar|delete|apagar|apague|arquivar|arquive|arquivamento)\b", re.I
)
SOFT_DELETION_VERBS = re.compile(r"\b(remover|remova|removendo|remoção)\b", re.I)
DELETED_STATES = {"DELETED", "REMOVED", "ARCHIVED"}
FORBIDDEN_CODE_BLOCK = re.compile(r"```json", re.I)
APPLIED = {"success", "executed_manually"}
OPEN_STATUSES = {"proposed", "approved", "partial_failure", "failed"}
GTM_TARGETS = {"gtm_tag", "gtm_trigger", "gtm_variable"}

SPEC_KEYS = {
    "title", "type", "platform", "depth", "scope", "scope_slug", "window", "accounts", "sources",
    "route", "record_statement", "knowledge_checks", "pending_decisions", "changes", "evaluation",
    "legacy_source",
}
SPEC_REQUIRED = {"title", "type", "platform", "depth", "scope", "sources", "route", "record_statement"}

STATUS_LABELS = {
    "analysis_only": "Registrado — análise sem mudanças na conta",
    "proposed": "Aguardando sua aprovação para executar",
    "approved": "Aprovado — aguardando execução",
    "executed": "Executado",
    "partial_failure": "Executado parcialmente",
    "failed": "Não executado (falhou)",
    "reverted": "Revertido",
    "blocked": "Bloqueado",
    "evaluated": "Avaliado",
}
TYPE_LABELS = {
    "configuracao": "Configuração", "onboarding": "Cadastro de cliente",
    "pesquisa_palavras_chave": "Pesquisa de palavras-chave", "planejamento": "Planejamento",
    "criacao": "Criação de campanha", "auditoria": "Auditoria", "analise": "Análise",
    "otimizacao": "Otimização", "ajuste": "Ajuste pontual", "relatorio": "Relatório",
    "reversao": "Reversão",
}
PLATFORM_LABELS = {"meta": "Meta Ads", "google_ads": "Google Ads", "multicanal": "Meta Ads + Google Ads"}
TARGET_LABELS = {
    "account": "conta", "campaign": "campanha", "adset": "conjunto de anúncios", "ad": "anúncio",
    "creative": "criativo", "ad_group": "grupo de anúncios", "keyword": "palavra-chave",
    "negative_keyword": "palavra-chave negativa", "asset": "recurso", "asset_group": "grupo de recursos",
    "audience": "público", "conversion_action": "ação de conversão", "gtm_tag": "tag do GTM",
    "gtm_trigger": "acionador do GTM", "gtm_variable": "variável do GTM", "other": "item",
}
MODE_LABELS = {
    "mcp": "pelo conector da plataforma (MCP), depois da sua aprovação de execução",
    "api_script": "por script de API, em rascunho (nunca publicado automaticamente)",
    "manual_only": "manualmente, por você, no gerenciador da plataforma",
    "blocked": "bloqueada — não será executada",
}
RESULT_LABELS = {
    "success": "aplicada",
    "executed_manually": "aplicada manualmente",
    "failed": "falhou",
    "not_attempted": "não tentada",
}
EVALUATION_LABELS = {"success": "funcionou", "failure": "não funcionou", "inconclusive": "inconclusivo"}
VERDICT_LABELS = {"sustenta": "✅ sustenta", "contradiz": "⚠️ contradiz", "sem_cobertura": "❔ sem cobertura"}
REASON_LABELS = {
    "condition_not_met": "condição da rota não se aplica",
    "source_unavailable": "fonte indisponível",
    "account_not_enabled": "conta não habilitada no conector",
    "platform_not_applicable": "não se aplica a esta plataforma",
    "user_restricted_scope": "escopo restringido por você",
    "no_platform_mechanism": "nenhum mecanismo de plataforma em jogo",
}
VALUE_LABELS = {
    "ACTIVE": "Ativo", "PAUSED": "Pausado", "ENABLED": "Ativo", "REMOVED": "Removido",
    "ARCHIVED": "Arquivado", True: "sim", False: "não",
}


class DossierError(Exception):
    """Erro de uso ou de integridade que impede a operação."""


# --------------------------------------------------------------------------- utilidades


def now_iso(override: str | None = None) -> str:
    if override:
        return datetime.fromisoformat(override).isoformat(timespec="seconds")
    return datetime.now(TZ).isoformat(timespec="seconds")


def slugify(value: str, limit: int = 48) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    ascii_text = "".join(char for char in decomposed if not unicodedata.combining(char))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug[:limit].rstrip("-") or "operacao"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def changes_hash(operation: dict) -> str:
    encoded = json.dumps(
        canonical_payload(operation), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return sha256_text(encoded)


def normalize_body(body: str) -> str:
    return body.replace("\r\n", "\n").strip("\n") + "\n"


def content_hash(body: str) -> str:
    return sha256_text(normalize_body(body))


def format_brl(value: float | None, *, signed: bool = False) -> str:
    if value is None:
        return "—"
    text = f"{abs(value):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    sign = ("+" if value > 0 else "−" if value < 0 else "") if signed else ("−" if value < 0 else "")
    return f"{sign}R$ {text}"


def format_date(value: str | None) -> str:
    if not value:
        return "—"
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return value
    if len(value) <= 10:
        return parsed.strftime("%d/%m/%Y")
    return parsed.strftime("%d/%m/%Y %H:%M")


def format_value(value: object) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool) or (isinstance(value, str) and value in VALUE_LABELS):
        return VALUE_LABELS[value]
    if isinstance(value, dict):
        return "; ".join(f"{key}: {format_value(item)}" for key, item in value.items())
    if isinstance(value, list):
        return ", ".join(format_value(item) for item in value) or "—"
    return str(value)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DossierError(f"JSON inválido em {path}: {exc}") from exc


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def client_display_name(clients_dir: Path, slug: str) -> str:
    profile = clients_dir / slug / "CLIENTE.md"
    if profile.is_file():
        for line in profile.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                heading = line[2:].strip()
                return heading.split("—", 1)[-1].strip() if "—" in heading else heading
    return slug


# --------------------------------------------------------------------------- localização


def operation_files(clients_dir: Path, client: str | None = None) -> list[Path]:
    pattern = f"{client}/{OPERATIONS_DIRNAME}/*.json" if client else f"*/{OPERATIONS_DIRNAME}/*.json"
    return sorted(clients_dir.glob(pattern))


def find_operation(clients_dir: Path, operation_id: str) -> Path:
    for path in operation_files(clients_dir):
        try:
            if load_json(path).get("operation_id") == operation_id:
                return path
        except DossierError:
            continue
    raise DossierError(f"operação não encontrada: {operation_id}")


def markdown_path(json_path: Path, operation: dict) -> Path:
    return json_path.with_name(operation["files"]["markdown"])


# --------------------------------------------------------------------------- corpo e renderização


def extract_body(markdown: str) -> str:
    start = markdown.find(BODY_START)
    end = markdown.find(BODY_END)
    if start < 0 or end < 0 or end < start:
        raise DossierError("marcadores do corpo aprovado ausentes no dossiê")
    inner = markdown[start + len(BODY_START):end]
    inner = re.sub(
        re.escape(CHANGES_START) + r".*?" + re.escape(CHANGES_END),
        CHANGES_MARKER,
        inner,
        flags=re.S,
    )
    return normalize_body(inner)


def prepare_body(body: str, has_changes: bool) -> str:
    body = normalize_body(body)
    if CHANGES_START in body or CHANGES_END in body or BODY_START in body or BODY_END in body:
        raise DossierError("o corpo não pode conter marcadores gerados pelo script")
    if FORBIDDEN_CODE_BLOCK.search(body):
        raise DossierError("o corpo não pode conter bloco JSON; o registro de máquina fica no .json")
    if has_changes and CHANGES_MARKER not in body:
        body = body.rstrip("\n") + "\n\n## O que vai mudar\n\n" + CHANGES_MARKER + "\n"
    return body


def render_change(change: dict, index_by_id: dict[str, int], results: dict[str, dict]) -> str:
    number = index_by_id[change["change_id"]]
    target = change["target"]
    where = f"{PLATFORM_LABELS[change['platform']]} · {TARGET_LABELS[target['type']]} “{target['name']}”"
    if target.get("id"):
        where += f" (ID {target['id']})"
    where += f" · conta {change['account']}"
    if change["action_kind"] == "create":
        what = f"Criar {TARGET_LABELS[target['type']]}: {format_value(change['after'])}"
    else:
        what = f"{change['field']}: {format_value(change['before'])} → {format_value(change['after'])}"
    lines = [
        f"### Mudança {number} — {change['title']}",
        "",
        f"- **Onde:** {where}",
        f"- **O que muda:** {what}",
        f"- **Por quê:** {change['why']}",
        f"- **Resultado esperado:** {change['expected_impact']}",
    ]
    if change.get("daily_budget_delta") is not None:
        lines.append(f"- **Efeito no orçamento diário:** {format_brl(change['daily_budget_delta'], signed=True)}")
    lines += [
        f"- **Risco:** {change['risk']}",
        f"- **Como desfazer:** {change['rollback']}",
        f"- **Como será executada:** {MODE_LABELS[change['execution_mode']]}",
    ]
    if change["depends_on"]:
        deps = ", ".join(f"Mudança {index_by_id[dep]}" for dep in change["depends_on"] if dep in index_by_id)
        lines.append(f"- **Depende de:** {deps}")
    result = results.get(change["change_id"])
    if result:
        situation = RESULT_LABELS[result["status"]]
        if result["divergences"]:
            situation += f", com {len(result['divergences'])} diferença(s) em relação ao aprovado"
        lines.append(f"- **Situação:** {situation} em {format_date(result['at'])}")
    return "\n".join(lines)


def latest_results(operation: dict) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    for result in (operation.get("execution") or {}).get("results", []):
        latest[result["change_id"]] = result
    return latest


def change_numbers(operation: dict) -> dict[str, int]:
    ordered = sorted(operation["changes"], key=lambda item: (item["order"], item["change_id"]))
    return {change["change_id"]: position for position, change in enumerate(ordered, start=1)}


def render_changes(operation: dict) -> str:
    if not operation["changes"]:
        return ""
    numbers = change_numbers(operation)
    results = latest_results(operation)
    ordered = sorted(operation["changes"], key=lambda item: numbers[item["change_id"]])
    blocks = [render_change(change, numbers, results) for change in ordered]
    total = sum(change["daily_budget_delta"] or 0 for change in operation["changes"])
    if any(change["daily_budget_delta"] is not None for change in operation["changes"]):
        blocks.append(f"**Efeito líquido no orçamento diário:** {format_brl(total, signed=True)}")
    return "\n\n".join(blocks)


def next_step(operation: dict) -> str:
    status = operation["status"]
    op_id = operation["operation_id"]
    if status == "analysis_only":
        return "Nenhuma mudança para executar."
    if status == "proposed":
        return f"Para executar, aprove com `/aprovar-operacao {op_id}`."
    if status == "approved":
        modes = {change["execution_mode"] for change in operation["changes"]} - {"blocked"}
        if modes == {"manual_only"}:
            return "Aplique as mudanças no gerenciador e me avise para registrar o que foi feito."
        if "manual_only" in modes:
            return (
                f"Use `/executar-operacao {op_id}` para as mudanças pelo conector; "
                "as manuais você aplica no gerenciador e me avisa para registrar."
            )
        return f"Para executar, use `/executar-operacao {op_id}`."
    if status in {"partial_failure", "failed"}:
        return "Há mudanças pendentes ou com falha; veja o andamento abaixo."
    evaluation = operation.get("evaluation")
    if status in {"executed", "reverted"} and evaluation and not evaluation.get("result"):
        return f"Avaliar o resultado a partir de {format_date(evaluation['due_date'])}."
    return "Operação encerrada."


def render_timeline(operation: dict) -> str:
    numbers = change_numbers(operation)
    titles = {change["change_id"]: change["title"] for change in operation["changes"]}
    events: list[tuple[str, str]] = []
    record = operation["record_approval"]
    events.append((record["approved_at"], f"Registrado após sua aprovação do conteúdo: “{record['statement']}”."))
    for previous in operation["previous_versions"]:
        events.append((previous["replaced_at"], f"Versão {previous['version']} substituída: {previous['reason']}."))
    approval = operation.get("approval")
    if approval:
        events.append((
            approval["approved_at"],
            f"Execução aprovada (versão {approval['version']}, {len(operation['changes'])} mudança(s)): “{approval['statement']}”.",
        ))
    for result in (operation.get("execution") or {}).get("results", []):
        label = RESULT_LABELS[result["status"]]
        text = f"Mudança {numbers.get(result['change_id'], '?')} ({titles.get(result['change_id'], result['change_id'])}): {label} via {result['via']}."
        if result["detail"]:
            text += f" {result['detail']}"
        if result["readback_confirmed"]:
            text += " Conferido por leitura na plataforma."
        events.append((result["at"], text))
    evaluation = operation.get("evaluation")
    if evaluation and evaluation.get("result"):
        text = f"Avaliação: {EVALUATION_LABELS[evaluation['result']]}."
        if evaluation.get("notes"):
            text += f" {evaluation['notes']}"
        events.append((evaluation["evaluated_at"], text))
    events.sort(key=lambda item: item[0])
    lines = [f"- **{format_date(moment)}** — {text}" for moment, text in events]
    divergences = [
        (numbers.get(result["change_id"], "?"), item)
        for result in latest_results(operation).values()
        for item in result["divergences"]
    ]
    if divergences:
        lines += ["", "### Diferenças entre o aprovado e o executado", ""]
        lines += [f"- Mudança {number}: {item}" for number, item in divergences]
    if evaluation:
        lines += [
            "",
            "### Como o resultado será avaliado",
            "",
            f"- **Quando:** a partir de {format_date(evaluation['due_date'])}",
        ]
        lines += [f"- **Funcionou se:** {item}" for item in evaluation["success_criteria"]]
        lines += [f"- **Parar ou reverter se:** {item}" for item in evaluation["stop_criteria"]]
    return "\n".join(lines)


def render_technical(operation: dict, json_name: str) -> str:
    route = operation["route"]
    lines = [
        f"- Operação: `{operation['operation_id']}` · versão {operation['version']}",
        f"- Registro de máquina: `{json_name}`",
        f"- Conferência do texto aprovado: `{operation['record_approval']['content_hash'][:16]}`",
    ]
    if operation.get("approval"):
        lines.append(f"- Conferência das mudanças aprovadas: `{operation['approval']['hash'][:16]}`")
    lines.append(f"- Profundidade: {operation['depth']}")
    lines.append(f"- Rota: {', '.join(f'`{item}`' for item in route['route_ids'])}")
    if route["executed_skills"]:
        lines.append(f"- Etapas executadas: {', '.join(route['executed_skills'])}")
    for skipped in route["skipped_skills"]:
        lines.append(f"- Etapa não executada: {skipped['skill']} — {REASON_LABELS[skipped['reason_code']]}: {skipped['detail']}")
    checks = operation["knowledge_checks"]
    if checks:
        counts = {verdict: sum(1 for item in checks if item["verdict"] == verdict) for verdict in VERDICT_LABELS}
        summary = " · ".join(f"{VERDICT_LABELS[key]}: {value}" for key, value in counts.items() if value)
        lines.append(f"- Checagens de boas práticas: {summary}")
        for item in checks:
            source = f"[{item['source_title']}]({item['source_url']})" if item.get("source_url") else (item.get("source_title") or "sem fonte")
            lines.append(f"  - {VERDICT_LABELS[item['verdict']]} — {item['premise']} — {source}")
    lines.append("- Fontes:")
    lines += [f"  - {source}" for source in operation["sources"]]
    if operation.get("legacy_source"):
        lines.append(f"- Migrado do dossiê legado: `{operation['legacy_source']}`")
    return "\n".join(lines)


def render_markdown(operation: dict, body: str, clients_dir: Path, json_name: str) -> str:
    client = client_display_name(clients_dir, operation["client_slug"])
    header = f"{client} · {PLATFORM_LABELS[operation['platform']]} · {TYPE_LABELS[operation['type']]}"
    status = STATUS_LABELS[operation["status"]]
    evaluation = operation.get("evaluation")
    if operation["status"] == "evaluated" and evaluation and evaluation.get("result"):
        status += f": {EVALUATION_LABELS[evaluation['result']]}"
    changes_block = render_changes(operation)
    body_rendered = body.replace(
        CHANGES_MARKER, f"{CHANGES_START}\n{changes_block}\n{CHANGES_END}" if changes_block else f"{CHANGES_START}\n{CHANGES_END}"
    )
    parts = [
        f"# {operation['title']}",
        "",
        f"> {header}  ",
        f"> **Situação:** {status}. {next_step(operation)}",
        "",
        BODY_START,
        body_rendered.rstrip("\n"),
        BODY_END,
        "",
        "## Andamento",
        "",
        render_timeline(operation),
        "",
        "---",
        "",
        "<details>",
        "<summary>Dados técnicos (para auditoria)</summary>",
        "",
        render_technical(operation, json_name),
        "",
        "</details>",
        "",
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------- verificação


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_matrix() -> dict:
    return json.loads(MATRIX_PATH.read_text(encoding="utf-8"))


def derive_execution_status(operation: dict) -> str:
    latest = latest_results(operation)
    executable = [change for change in operation["changes"] if change["execution_mode"] != "blocked"]
    states = [latest.get(change["change_id"], {}).get("status", "not_attempted") for change in executable]
    if states and all(state in APPLIED for state in states):
        return "reverted" if operation["type"] == "reversao" else "executed"
    if any(state in APPLIED for state in states):
        return "partial_failure"
    return "failed"


def check_route(operation: dict, matrix: dict, errors: list[str], warnings: list[str]) -> None:
    route = operation["route"]
    executed = set(route["executed_skills"])
    skipped = {item["skill"]: item for item in route["skipped_skills"]}
    has_changes = bool(operation["changes"])
    legacy = bool(operation.get("legacy_source"))
    sink = warnings if legacy else errors
    intents: set[str] = set()
    platforms: set[str] = set()
    for route_id in route["route_ids"]:
        intent, platform, source_mode = route_id.split(":")
        intents.add(intent)
        platforms.add(platform)
        steps = matrix.get("intents", {}).get(intent, {}).get(platform)
        if steps is None:
            errors.append(f"rota inexistente na matriz: {route_id}")
            continue
        for step in steps.get("steps", []):
            skill, condition = step["skill"], step["when"]
            required = condition == "always" or condition == f"source_mode={source_mode}"
            known_unmet = condition.startswith("source_mode=") and condition != f"source_mode={source_mode}"
            reason = skipped.get(skill)
            if skill in executed:
                continue
            if reason is None:
                if required:
                    sink.append(f"etapa obrigatória {skill} ({route_id}) não foi executada nem justificada")
                continue
            if reason["reason_code"] == "condition_not_met" and required:
                sink.append(
                    f"{skill} marcada como 'condição não atendida', mas a condição da rota {route_id} é '{condition}'"
                )
            if reason["reason_code"] == "no_platform_mechanism":
                if skill not in KNOWLEDGE_SKILLS:
                    errors.append(f"motivo 'nenhum mecanismo de plataforma' só vale para as skills 15/17, não para {skill}")
                elif has_changes:
                    sink.append(
                        f"{skill} não pode ser pulada numa operação com mudanças: toda mudança passa pela checagem de boas práticas"
                    )
                else:
                    warnings.append(f"{skill} pulada sem checagem de boas práticas: {reason['detail']}")
            if known_unmet and reason["reason_code"] != "condition_not_met":
                warnings.append(f"{skill} pulada com motivo '{reason['reason_code']}', mas a condição já não se aplicava")
    if operation["type"] not in intents:
        warnings.append(f"tipo '{operation['type']}' não aparece nas rotas {sorted(intents)}")
    expected = {"meta": {"meta"}, "google_ads": {"google_ads"}, "multicanal": {"meta", "google_ads"}}[operation["platform"]]
    if platforms != expected:
        errors.append(f"plataforma '{operation['platform']}' não bate com as rotas {sorted(platforms)}")


def check_changes(operation: dict, errors: list[str], warnings: list[str]) -> None:
    changes = operation["changes"]
    ids = [change["change_id"] for change in changes]
    if len(ids) != len(set(ids)):
        errors.append("IDs de mudança duplicados")
    orders = [change["order"] for change in changes]
    if len(orders) != len(set(orders)):
        errors.append("ordens de execução duplicadas entre mudanças")
    known = set(ids)
    if changes and operation["platform"] == "multicanal":
        errors.append("mudanças exigem uma operação por plataforma; separe Meta e Google Ads")
    for change in changes:
        label = f"mudança {change['change_id']}"
        if operation["platform"] != "multicanal" and change["platform"] != operation["platform"]:
            errors.append(f"{label}: plataforma diferente da operação")
        for dependency in change["depends_on"]:
            if dependency not in known or dependency == change["change_id"]:
                errors.append(f"{label}: dependência inválida {dependency}")
        if DELETION_VERBS.search(change["rollback"]):
            errors.append(f"{label}: a reversão fala em excluir/apagar/arquivar; o contrato só permite pausar")
        if isinstance(change["after"], str) and change["after"].upper() in DELETED_STATES:
            errors.append(f"{label}: mudar para '{change['after']}' é exclusão/arquivamento, proibido pelo contrato")
        descriptive = " ".join([change["title"], change["field"], change["why"]])
        if DELETION_VERBS.search(descriptive) or SOFT_DELETION_VERBS.search(descriptive + " " + change["rollback"]):
            warnings.append(f"{label}: menciona excluir/remover; confirme que é segmentação, não exclusão de ativo")
        if change["platform"] == "google_ads" and change["execution_mode"] == "mcp":
            errors.append(f"{label}: Google Ads não tem escrita homologada; use manual_only")
        if change["target"]["type"] in GTM_TARGETS and change["execution_mode"] == "mcp":
            errors.append(f"{label}: mudanças de GTM usam api_script ou manual_only")
        if change["action_kind"] == "create" and change["before"] not in (None, "", {}):
            warnings.append(f"{label}: criação com valor 'antes' preenchido")
    if changes and not operation["knowledge_checks"] and not operation.get("legacy_source"):
        errors.append("operação com mudanças sem nenhuma checagem de boas práticas (knowledge_checks)")
    if changes and operation.get("evaluation") is None:
        errors.append("operação com mudanças sem critério de avaliação (evaluation)")


def check_state(operation: dict, errors: list[str]) -> None:
    status = operation["status"]
    changes = operation["changes"]
    approval = operation.get("approval")
    execution = operation.get("execution")
    evaluation = operation.get("evaluation")
    if not changes and status not in {"analysis_only", "blocked"}:
        errors.append(f"status '{status}' exige mudanças; análise sem mudança é 'analysis_only'")
    if changes and status == "analysis_only":
        errors.append("operação com mudanças não pode ser 'analysis_only'")
    if status == "proposed" and (approval or execution):
        errors.append("status 'proposed' não pode ter aprovação ou execução registradas")
    if status == "approved" and (not approval or execution):
        errors.append("status 'approved' exige aprovação e nenhuma execução")
    if status in {"executed", "partial_failure", "failed", "reverted", "evaluated"} and changes:
        if not approval:
            errors.append(f"status '{status}' sem aprovação operacional registrada")
        if not execution:
            errors.append(f"status '{status}' sem execução registrada")
    if approval:
        if approval["version"] != operation["version"]:
            errors.append("aprovação é de outra versão da operação")
        if approval["hash"] != changes_hash(operation):
            errors.append("as mudanças foram alteradas depois da aprovação (hash não confere)")
    if execution:
        known = {change["change_id"] for change in changes}
        for result in execution["results"]:
            if result["change_id"] not in known:
                errors.append(f"resultado de execução para mudança inexistente: {result['change_id']}")
        derived = derive_execution_status(operation)
        if status in {"executed", "partial_failure", "failed", "reverted"} and status != derived:
            errors.append(f"status '{status}' não bate com os resultados de execução (esperado '{derived}')")
    if status == "evaluated" and not (evaluation and evaluation.get("result")):
        errors.append("status 'evaluated' sem resultado de avaliação")
    if evaluation and evaluation.get("result") and status != "evaluated":
        errors.append("avaliação registrada, mas status não é 'evaluated'")


def verify_operation(json_path: Path, clients_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        operation = load_json(json_path)
    except DossierError as exc:
        return [str(exc)], warnings
    validator = jsonschema.Draft7Validator(load_schema(), format_checker=jsonschema.FormatChecker())
    for error in validator.iter_errors(operation):
        location = "/".join(str(part) for part in error.absolute_path) or "(raiz)"
        errors.append(f"formato: {location}: {error.message}")
    if errors:
        return errors, warnings
    if json_path.parent.name != OPERATIONS_DIRNAME or json_path.parent.parent.name != operation["client_slug"]:
        errors.append("arquivo fora de clients/{cliente}/operacoes/ do cliente declarado")
    md_path = markdown_path(json_path, operation)
    if md_path.stem != json_path.stem:
        errors.append("o .md e o .json devem ter o mesmo nome")
    if not md_path.is_file():
        errors.append(f"dossiê .md ausente: {md_path.name}")
        return errors, warnings
    markdown = md_path.read_text(encoding="utf-8")
    try:
        body = extract_body(markdown)
    except DossierError as exc:
        errors.append(str(exc))
        return errors, warnings
    if content_hash(body) != operation["record_approval"]["content_hash"]:
        errors.append("o texto aprovado do .md foi alterado depois do registro (hash não confere)")
    if operation["changes"] and CHANGES_MARKER not in body:
        errors.append("corpo sem o marcador de mudanças")
    check_route(operation, load_matrix(), errors, warnings)
    check_changes(operation, errors, warnings)
    check_state(operation, errors)
    if not errors and render_markdown(operation, body, clients_dir, json_path.name) != markdown:
        warnings.append("o .md está fora de sincronia com o .json; rode `dossier.py render`")
    return errors, warnings


# --------------------------------------------------------------------------- comandos


def read_spec(path: Path) -> dict:
    spec = load_json(path)
    unknown = set(spec) - SPEC_KEYS
    missing = SPEC_REQUIRED - set(spec)
    if unknown:
        raise DossierError(f"campos desconhecidos no spec: {sorted(unknown)}")
    if missing:
        raise DossierError(f"campos obrigatórios ausentes no spec: {sorted(missing)}")
    return spec


def build_evaluation(raw: dict | None) -> dict | None:
    if raw is None:
        return None
    return {
        "due_date": raw.get("due_date"),
        "success_criteria": raw.get("success_criteria", []),
        "stop_criteria": raw.get("stop_criteria", []),
        "result": None,
        "evaluated_at": None,
        "notes": None,
    }


def apply_spec(operation: dict, spec: dict) -> None:
    operation.update({
        "title": spec["title"],
        "type": spec["type"],
        "platform": spec["platform"],
        "depth": spec["depth"],
        "scope": spec["scope"],
        "window": spec.get("window"),
        "accounts": spec.get("accounts", {}),
        "sources": spec["sources"],
        "route": spec["route"],
        "knowledge_checks": spec.get("knowledge_checks", []),
        "pending_decisions": spec.get("pending_decisions", []),
        "changes": spec.get("changes", []),
        "evaluation": build_evaluation(spec.get("evaluation")),
    })
    if spec.get("legacy_source"):
        operation["legacy_source"] = spec["legacy_source"]
    operation["status"] = "proposed" if operation["changes"] else "analysis_only"


def persist(operation: dict, body: str, json_path: Path, clients_dir: Path, *, dry_run: bool) -> tuple[list[str], list[str]]:
    """Valida numa pasta temporária e só grava no cliente se não houver erro."""
    md_name = operation["files"]["markdown"]
    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp) / operation["client_slug"] / OPERATIONS_DIRNAME
        staging.mkdir(parents=True)
        staged_json = staging / json_path.name
        staged_md = staging / md_name
        write_json(staged_json, operation)
        staged_md.write_text(render_markdown(operation, body, clients_dir, json_path.name), encoding="utf-8")
        errors, warnings = verify_operation(staged_json, clients_dir)
        if not errors and not dry_run:
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(staged_json.read_text(encoding="utf-8"), encoding="utf-8")
            json_path.with_name(md_name).write_text(staged_md.read_text(encoding="utf-8"), encoding="utf-8")
    return errors, warnings


def remind_contradictions(operation: dict) -> None:
    for check in operation["knowledge_checks"]:
        if check["verdict"] == "contradiz":
            print(f"  lembrete: a checagem contradiz “{check['premise']}”; o texto aprovado precisa refletir a correção")


def report(errors: list[str], warnings: list[str]) -> None:
    for warning in warnings:
        print(f"  atenção: {warning}")
    if errors:
        print("NÃO GRAVADO — corrija e rode de novo:")
        for error in errors:
            print(f"  - {error}")


def cmd_new(args: argparse.Namespace) -> int:
    clients_dir = Path(args.clients_dir)
    slug = args.client
    if not (clients_dir / slug / "CLIENTE.md").is_file():
        raise DossierError(f"cliente '{slug}' sem CLIENTE.md; cadastre o cliente antes de registrar operações")
    spec = read_spec(Path(args.spec))
    moment = now_iso(args.now)
    stamp = datetime.fromisoformat(moment)
    scope_slug = slugify(spec.get("scope_slug") or spec["title"])
    platform_slug = spec["platform"]
    operation_id = f"op-{stamp:%Y%m%d}-{stamp:%H%M}-{slug}-{platform_slug.replace('_', '-')}-{scope_slug}"
    base_name = f"{stamp:%Y-%m-%d-%H%M}-{platform_slug}-{spec['type']}-{scope_slug}"
    json_path = clients_dir / slug / OPERATIONS_DIRNAME / f"{base_name}.json"
    if json_path.exists() or json_path.with_suffix(".md").exists():
        raise DossierError(f"já existe um dossiê com este nome: {json_path.name}")
    operation: dict = {
        "schema_version": "2.0",
        "operation_id": operation_id,
        "version": 1,
        "client_slug": slug,
        "created_at": moment,
        "updated_at": moment,
        "approval": None,
        "execution": None,
        "previous_versions": [],
        "files": {"markdown": f"{base_name}.md"},
    }
    apply_spec(operation, spec)
    body = prepare_body(Path(args.body).read_text(encoding="utf-8"), bool(operation["changes"]))
    operation["record_approval"] = {
        "approved_at": moment,
        "statement": spec["record_statement"],
        "content_hash": content_hash(body),
    }
    operation = order_keys(operation)
    errors, warnings = persist(operation, body, json_path, clients_dir, dry_run=args.dry_run)
    report(errors, warnings)
    if errors:
        return 1
    remind_contradictions(operation)
    verb = "Validado (nada gravado)" if args.dry_run else "Registrado"
    print(f"{verb}: {operation['title']}")
    print(f"  situação: {STATUS_LABELS[operation['status']]}")
    print(f"  dossiê: {json_path.with_suffix('.md').relative_to(ROOT) if json_path.is_relative_to(ROOT) else json_path.with_suffix('.md')}")
    print(f"  operação: {operation_id}")
    return 0


def order_keys(operation: dict) -> dict:
    order = [
        "schema_version", "operation_id", "version", "client_slug", "type", "platform", "status", "title",
        "created_at", "updated_at", "depth", "scope", "window", "accounts", "sources", "route",
        "record_approval", "knowledge_checks", "pending_decisions", "changes", "approval", "execution",
        "evaluation", "previous_versions", "legacy_source", "files",
    ]
    return {key: operation[key] for key in order if key in operation}


def load_for_update(args: argparse.Namespace) -> tuple[Path, dict, str, Path]:
    clients_dir = Path(args.clients_dir)
    json_path = find_operation(clients_dir, args.operation_id)
    errors, _ = verify_operation(json_path, clients_dir)
    if errors:
        raise DossierError("o dossiê atual não passa na verificação; corrija antes de alterá-lo:\n  - " + "\n  - ".join(errors))
    operation = load_json(json_path)
    body = extract_body(markdown_path(json_path, operation).read_text(encoding="utf-8"))
    return json_path, operation, body, clients_dir


def save_update(json_path: Path, operation: dict, body: str, clients_dir: Path, moment: str) -> int:
    operation["updated_at"] = moment
    errors, warnings = persist(order_keys(operation), body, json_path, clients_dir, dry_run=False)
    report(errors, warnings)
    if errors:
        return 1
    print(f"Atualizado: {operation['title']}")
    print(f"  situação: {STATUS_LABELS[operation['status']]}")
    print(f"  próximo passo: {next_step(operation)}")
    return 0


def cmd_revise(args: argparse.Namespace) -> int:
    json_path, operation, old_body, clients_dir = load_for_update(args)
    if operation["execution"]:
        raise DossierError("operação já executada não pode ser revisada; registre uma nova operação ou uma reversão")
    spec = read_spec(Path(args.spec))
    for fixed in ("type", "platform"):
        if spec[fixed] != operation[fixed]:
            raise DossierError(f"'{fixed}' não pode mudar numa revisão; registre uma nova operação")
    moment = now_iso(args.now)
    operation["previous_versions"].append({
        "version": operation["version"],
        "replaced_at": moment,
        "content_hash": operation["record_approval"]["content_hash"],
        "changes_hash": changes_hash(operation),
        "reason": args.reason,
    })
    operation["version"] += 1
    apply_spec(operation, spec)
    operation["approval"] = None
    body = prepare_body(Path(args.body).read_text(encoding="utf-8"), bool(operation["changes"]))
    operation["record_approval"] = {
        "approved_at": moment,
        "statement": spec["record_statement"],
        "content_hash": content_hash(body),
    }
    remind_contradictions(operation)
    return save_update(json_path, operation, body, clients_dir, moment)


def cmd_approve(args: argparse.Namespace) -> int:
    json_path, operation, body, clients_dir = load_for_update(args)
    if operation["status"] != "proposed":
        raise DossierError(f"só é possível aprovar operação 'proposed' (atual: {operation['status']})")
    if all(change["execution_mode"] == "blocked" for change in operation["changes"]):
        raise DossierError("todas as mudanças estão bloqueadas; não há o que aprovar")
    moment = now_iso(args.now)
    operation["approval"] = {
        "approved_at": moment,
        "statement": args.statement,
        "version": operation["version"],
        "hash": changes_hash(operation),
    }
    operation["status"] = "approved"
    return save_update(json_path, operation, body, clients_dir, moment)


def cmd_record_execution(args: argparse.Namespace) -> int:
    json_path, operation, body, clients_dir = load_for_update(args)
    if operation["status"] not in {"approved", "partial_failure", "failed"}:
        raise DossierError(f"execução só pode ser registrada em operação aprovada (atual: {operation['status']})")
    moment = now_iso(args.now)
    if args.results.lstrip().startswith(("[", "{")):
        try:
            raw_results = json.loads(args.results)
        except json.JSONDecodeError as exc:
            raise DossierError(f"resultados em JSON inválido: {exc}") from exc
    else:
        raw_results = load_json(Path(args.results))
    if isinstance(raw_results, dict):
        raw_results = [raw_results]
    results = []
    for raw in raw_results:
        if "change_id" not in raw or "status" not in raw:
            raise DossierError("cada resultado precisa de change_id e status")
        results.append({
            "change_id": raw["change_id"],
            "status": raw["status"],
            "via": raw.get("via", "não informado"),
            "at": raw.get("at", moment),
            "detail": raw.get("detail", ""),
            "readback_confirmed": bool(raw.get("readback_confirmed", False)),
            "divergences": raw.get("divergences", []),
        })
    execution = operation["execution"] or {"started_at": moment, "finished_at": moment, "results": [], "post_snapshot": None}
    execution["results"].extend(results)
    execution["finished_at"] = moment
    if args.post_snapshot:
        execution["post_snapshot"] = args.post_snapshot
    operation["execution"] = execution
    operation["status"] = derive_execution_status(operation)
    return save_update(json_path, operation, body, clients_dir, moment)


def cmd_evaluate(args: argparse.Namespace) -> int:
    json_path, operation, body, clients_dir = load_for_update(args)
    if operation["status"] not in {"executed", "partial_failure", "reverted"}:
        raise DossierError(f"só é possível avaliar operação executada (atual: {operation['status']})")
    if not operation["evaluation"]:
        raise DossierError("operação sem critério de avaliação registrado")
    moment = now_iso(args.now)
    operation["evaluation"].update({"result": args.result, "evaluated_at": moment, "notes": args.notes})
    operation["status"] = "evaluated"
    return save_update(json_path, operation, body, clients_dir, moment)


def cmd_render(args: argparse.Namespace) -> int:
    clients_dir = Path(args.clients_dir)
    json_path = find_operation(clients_dir, args.operation_id)
    operation = load_json(json_path)
    md_path = markdown_path(json_path, operation)
    body = extract_body(md_path.read_text(encoding="utf-8"))
    md_path.write_text(render_markdown(operation, body, clients_dir, json_path.name), encoding="utf-8")
    print(f"Renderizado: {md_path.name}")
    return 0


def cmd_hash(args: argparse.Namespace) -> int:
    operation = load_json(find_operation(Path(args.clients_dir), args.operation_id))
    print(changes_hash(operation))
    return 0


def resolve_verify_targets(args: argparse.Namespace, clients_dir: Path) -> list[Path]:
    if args.path:
        path = Path(args.path).resolve()
        if path.suffix == ".md":
            path = path.with_suffix(".json")
        return [path]
    if args.operation_ids:
        return [find_operation(clients_dir, op_id) for op_id in args.operation_ids]
    return operation_files(clients_dir, args.client)


def cmd_verify(args: argparse.Namespace) -> int:
    clients_dir = Path(args.clients_dir)
    targets = resolve_verify_targets(args, clients_dir)
    if not targets:
        print("Nenhum dossiê V2 encontrado.")
        return 0
    failures = 0
    for path in targets:
        # Com --path, a pasta de clientes é a do próprio arquivo (clients/{slug}/operacoes/x.json).
        base = path.parents[2] if args.path and len(path.parents) > 2 else clients_dir
        errors, warnings = verify_operation(path, base)
        label = path.relative_to(clients_dir) if path.is_relative_to(clients_dir) else path
        if errors:
            failures += 1
            print(f"INVÁLIDO {label}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {label}")
        for warning in warnings:
            print(f"  atenção: {warning}")
    return 1 if failures else 0


def cmd_list(args: argparse.Namespace) -> int:
    clients_dir = Path(args.clients_dir)
    today = date.fromisoformat(args.today) if args.today else datetime.now(TZ).date()
    rows = []
    for path in operation_files(clients_dir, args.client):
        try:
            operation = load_json(path)
        except DossierError:
            continue
        evaluation = operation.get("evaluation") or {}
        pending_evaluation = operation["status"] in {"executed", "partial_failure", "reverted"} and not evaluation.get("result")
        is_open = operation["status"] in OPEN_STATUSES or pending_evaluation
        if args.open and not is_open:
            continue
        note = ""
        if pending_evaluation and evaluation.get("due_date"):
            due = date.fromisoformat(evaluation["due_date"])
            note = f"avaliação vencida desde {due:%d/%m}" if due <= today else f"avaliar a partir de {due:%d/%m}"
        rows.append({
            "operation_id": operation["operation_id"],
            "client": operation["client_slug"],
            "date": operation["created_at"][:10],
            "platform": PLATFORM_LABELS[operation["platform"]],
            "type": TYPE_LABELS[operation["type"]],
            "status": STATUS_LABELS[operation["status"]],
            "title": operation["title"],
            "note": note,
            "pending_decisions": operation.get("pending_decisions", []),
            "path": str(path.with_suffix(".md")),
        })
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    if not rows:
        print("Nenhuma operação V2 encontrada com esses filtros.")
        return 0
    for row in rows:
        suffix = f" — {row['note']}" if row["note"] else ""
        print(f"{format_date(row['date'])} · {row['client']} · {row['platform']} · {row['type']} · {row['status']}{suffix}")
        print(f"    {row['title']}  [{row['operation_id']}]")
        for decision in row["pending_decisions"]:
            print(f"    decisão pendente: {decision}")
    return 0


LEGACY_JSON = re.compile(r"```json\s*(\{.*?\})\s*```", re.S)


def cmd_migrate(args: argparse.Namespace) -> int:
    legacy_path = Path(args.legacy).resolve()
    text = legacy_path.read_text(encoding="utf-8")
    match = LEGACY_JSON.search(text)
    if not match:
        raise DossierError("dossiê legado sem bloco JSON; não há mudanças estruturadas para migrar")
    legacy = json.loads(match.group(1))
    if legacy.get("status") not in {"proposed", "approved"}:
        raise DossierError(f"só operações legadas abertas (proposed/approved) são migradas; status atual: {legacy.get('status')}")
    platform = legacy.get("platform")
    if platform not in {"meta", "google_ads"}:
        raise DossierError(f"plataforma legada não suportada para migração: {platform}")
    human = text[match.end():].lstrip("\n")
    clients_dir = Path(args.clients_dir)
    relative_legacy = str(legacy_path.relative_to(clients_dir.resolve())) if legacy_path.is_relative_to(clients_dir.resolve()) else str(legacy_path)
    body = (
        f"> Migrado do dossiê legado `{legacy_path.name}`. O texto original aprovado está preservado abaixo.\n"
        f"> Aprovações operacionais legadas não são transportadas: a execução exige nova aprovação.\n\n"
        f"{human}\n\n## O que vai mudar\n\n{CHANGES_MARKER}\n"
    )
    changes = []
    for position, raw in enumerate(sorted(legacy.get("changes", []), key=lambda item: item.get("order", 0)), start=1):
        field = str(raw.get("field", "campo"))
        after = raw.get("after")
        kind = "update"
        if field == "entity_creation":
            kind = "create"
        elif field == "status" and after in {"PAUSED", "ACTIVE", "ENABLED"}:
            kind = "pause" if after == "PAUSED" else "activate"
        target_ref = str(raw.get("target_ref", ""))
        target_id = re.search(r"\d{6,}", target_ref)
        mode = raw.get("execution_mode", "manual_only")
        if mode not in {"mcp", "api_script", "manual_only", "blocked"} or (platform == "google_ads" and mode == "mcp"):
            mode = "manual_only"
        target_type = raw.get("target_type", "other")
        if target_type not in TARGET_LABELS:
            target_type = "other"
        changes.append({
            "change_id": f"c{position}",
            "title": f"{field} — {target_ref}"[:160] or f"Mudança {position}",
            "platform": platform,
            "account": next(iter((legacy.get("accounts") or {}).values()), "não informada"),
            "target": {"type": target_type, "id": target_id.group(0) if target_id else None, "name": target_ref or "não informado"},
            "field": field,
            "before": raw.get("before"),
            "after": after,
            "action_kind": kind,
            "execution_mode": mode,
            "why": str(raw.get("rationale") or "revisar justificativa"),
            "expected_impact": str(raw.get("expected_impact") or "revisar impacto esperado"),
            "daily_budget_delta": raw.get("financial_impact") if isinstance(raw.get("financial_impact"), (int, float)) else None,
            "risk": str(raw.get("risk") or "revisar risco"),
            "rollback": str(raw.get("rollback") or "revisar reversão"),
            "order": position,
            "depends_on": [],
        })
    route = legacy.get("route") or {}
    success = sorted({item for raw in legacy.get("changes", []) for item in raw.get("success_criteria", [])})
    stop = sorted({item for raw in legacy.get("changes", []) for item in raw.get("stop_criteria", [])})
    today = datetime.now(TZ).date()
    spec = {
        "title": str(legacy.get("scope") or legacy_path.stem)[:140],
        "type": legacy.get("type") if legacy.get("type") in TYPE_LABELS else "otimizacao",
        "platform": platform,
        "depth": (legacy.get("analysis") or {}).get("depth_mode") or "focused",
        "scope": str(legacy.get("scope") or "revisar escopo"),
        "scope_slug": slugify(legacy_path.stem.split("-", 4)[-1]),
        "window": None,
        "accounts": legacy.get("accounts") or {},
        "sources": legacy.get("sources") or [f"dossiê legado {legacy_path.name}"],
        "route": {
            "router_version": route.get("router_version", "1.1.0"),
            "route_ids": route.get("route_ids") or [f"{legacy.get('type', 'otimizacao')}:{platform}:{(legacy.get('source_modes') or {}).get(platform, 'context_only')}"],
            "executed_skills": route.get("executed_skills", []),
            "skipped_skills": [],
        },
        "record_statement": "REVISAR: migração de operação legada aprovada pelo gestor em <data>",
        "knowledge_checks": [],
        "pending_decisions": [],
        "changes": changes,
        "evaluation": {
            "due_date": (today + timedelta(days=14)).isoformat(),
            "success_criteria": success or ["REVISAR: critério de sucesso"],
            "stop_criteria": stop,
        },
        "legacy_source": relative_legacy,
    }
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    spec_path = out_dir / f"migracao-{legacy_path.stem}.spec.json"
    body_path = out_dir / f"migracao-{legacy_path.stem}.body.md"
    write_json(spec_path, spec)
    body_path.write_text(body, encoding="utf-8")
    print("Rascunho de migração gerado (nada foi registrado ainda):")
    print(f"  spec: {spec_path}")
    print(f"  corpo: {body_path}")
    print("Revise títulos das mudanças, prazo de avaliação e a declaração de registro; depois rode `dossier.py new`.")
    return 0


# --------------------------------------------------------------------------- CLI


def parser() -> argparse.ArgumentParser:
    main_parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    main_parser.add_argument("--clients-dir", default=str(DEFAULT_CLIENTS_DIR))
    sub = main_parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="registra uma operação aprovada editorialmente")
    new.add_argument("--client", required=True)
    new.add_argument("--spec", required=True)
    new.add_argument("--body", required=True)
    new.add_argument("--now")
    new.add_argument("--dry-run", action="store_true")
    new.set_defaults(func=cmd_new)

    revise = sub.add_parser("revise", help="nova versão de uma operação ainda não executada")
    revise.add_argument("operation_id")
    revise.add_argument("--spec", required=True)
    revise.add_argument("--body", required=True)
    revise.add_argument("--reason", required=True)
    revise.add_argument("--now")
    revise.set_defaults(func=cmd_revise)

    approve = sub.add_parser("approve", help="registra a aprovação operacional (não executa)")
    approve.add_argument("operation_id")
    approve.add_argument("--statement", required=True)
    approve.add_argument("--now")
    approve.set_defaults(func=cmd_approve)

    record = sub.add_parser("record-execution", help="registra resultados de execução (MCP ou manual)")
    record.add_argument("operation_id")
    record.add_argument("--results", required=True, help="arquivo JSON ou JSON inline com a lista de resultados")
    record.add_argument("--post-snapshot")
    record.add_argument("--now")
    record.set_defaults(func=cmd_record_execution)

    evaluate = sub.add_parser("evaluate", help="registra a avaliação do resultado ao fim da janela")
    evaluate.add_argument("operation_id")
    evaluate.add_argument("--result", required=True, choices=["success", "failure", "inconclusive"])
    evaluate.add_argument("--notes", required=True)
    evaluate.add_argument("--now")
    evaluate.set_defaults(func=cmd_evaluate)

    render = sub.add_parser("render", help="regenera o .md a partir do .json")
    render.add_argument("operation_id")
    render.set_defaults(func=cmd_render)

    hash_cmd = sub.add_parser("hash", help="mostra o hash canônico das mudanças")
    hash_cmd.add_argument("operation_id")
    hash_cmd.set_defaults(func=cmd_hash)

    verify = sub.add_parser("verify", help="verifica formato, hashes, rota e estado")
    verify.add_argument("operation_ids", nargs="*")
    verify.add_argument("--client")
    verify.add_argument("--path")
    verify.set_defaults(func=cmd_verify)

    list_cmd = sub.add_parser("list", help="lista operações V2")
    list_cmd.add_argument("--client")
    list_cmd.add_argument("--open", action="store_true", help="só operações abertas ou com avaliação pendente")
    list_cmd.add_argument("--today")
    list_cmd.add_argument("--json", action="store_true")
    list_cmd.set_defaults(func=cmd_list)

    migrate = sub.add_parser("migrate", help="gera rascunho V2 a partir de um dossiê legado aberto")
    migrate.add_argument("legacy")
    migrate.add_argument("--out-dir", default=str(WORK_DIR))
    migrate.set_defaults(func=cmd_migrate)
    return main_parser


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.func(args)
    except DossierError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
