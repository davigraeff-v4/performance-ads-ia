"""Ferramentas de escrita (mutate) e leitura com MCC automática para o google_ads_server.

Regras de segurança aplicadas aqui, independentes de quem chama:
- Só altera contas listadas em allowed_accounts.json (allowlist local).
- GOOGLE_ADS_WRITE_MODE: execute (grava quando validate_only=False),
  validate_only (nunca grava) ou disabled (recusa qualquer escrita).
- Toda ferramenta de escrita começa com validate_only=True: a API checa
  permissão e regras sem gravar. Para gravar, chame de novo com validate_only=False.
- Operações "remove" e status REMOVED são recusadas, a menos que
  GOOGLE_ADS_ALLOW_REMOVE=true.
- Cada chamada de escrita fica registrada em logs/mutations.jsonl.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import requests

BASE_DIR = Path(__file__).resolve().parent
ALLOWLIST_PATH = Path(
    os.environ.get("GOOGLE_ADS_ALLOWLIST_PATH", BASE_DIR / "allowed_accounts.json")
)
LOG_PATH = BASE_DIR / "logs" / "mutations.jsonl"

_RESOURCE = re.compile(r"^[a-zA-Z]+$")
_ID = re.compile(r"^[0-9]+$")
_COMPOSITE_ID = re.compile(r"^[0-9]+~[0-9]+$")
_MATCH_TYPES = {"EXACT", "PHRASE", "BROAD"}
_STATUSES = {"ENABLED", "PAUSED"}

_STATUS_RESOURCES = {
    "campaign": ("campaigns", _ID),
    "ad_group": ("adGroups", _ID),
    "ad": ("adGroupAds", _COMPOSITE_ID),  # "<ad_group_id>~<ad_id>"
    "keyword": ("adGroupCriteria", _COMPOSITE_ID),  # "<ad_group_id>~<criterion_id>"
    "asset_group": ("assetGroups", _ID),
}


def _write_mode() -> str:
    mode = os.environ.get("GOOGLE_ADS_WRITE_MODE", "validate_only").strip()
    if mode not in {"execute", "validate_only", "disabled"}:
        raise ValueError("GOOGLE_ADS_WRITE_MODE deve ser execute, validate_only ou disabled")
    return mode


def _allow_remove() -> bool:
    return os.environ.get("GOOGLE_ADS_ALLOW_REMOVE", "false").strip().lower() == "true"


def _load_allowlist() -> Dict[str, Any]:
    if not ALLOWLIST_PATH.is_file():
        return {"default_login_customer_id": "", "accounts": {}}
    with ALLOWLIST_PATH.open(encoding="utf-8") as handle:
        data = json.load(handle)
    data.setdefault("accounts", {})
    return data


def _log(entry: Dict[str, Any]) -> None:
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry = {"at": datetime.now(timezone.utc).isoformat(), **entry}
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _contains_remove(value: Any) -> bool:
    if isinstance(value, dict):
        if "remove" in value:
            return True
        if str(value.get("status", "")).upper() == "REMOVED":
            return True
        return any(_contains_remove(v) for v in value.values())
    if isinstance(value, list):
        return any(_contains_remove(v) for v in value)
    return False


def _summarize_error(response: requests.Response) -> Dict[str, Any]:
    try:
        body = response.json()
    except ValueError:
        return {"http_status": response.status_code, "message": response.text[:500]}
    error = body.get("error", body)
    out: Dict[str, Any] = {
        "http_status": response.status_code,
        "message": error.get("message"),
        "errors": [],
    }
    for detail in error.get("details", []) or []:
        for item in detail.get("errors", []) or []:
            out["errors"].append(
                {
                    "code": item.get("errorCode"),
                    "message": item.get("message"),
                    "trigger": item.get("trigger"),
                    "location": item.get("location"),
                }
            )
        if detail.get("requestId"):
            out["request_id"] = detail["requestId"]
    return out


def register(
    mcp,
    *,
    get_credentials: Callable[[], Any],
    get_headers: Callable[[Any], Dict[str, str]],
    format_customer_id: Callable[[str], str],
    api_version: str,
) -> None:
    """Registra as ferramentas no servidor FastMCP existente."""

    base_url = f"https://googleads.googleapis.com/{api_version}"

    def resolve_login(customer_id: str, login_customer_id: Optional[str]) -> Optional[str]:
        if login_customer_id:
            return format_customer_id(login_customer_id)
        allow = _load_allowlist()
        account = allow["accounts"].get(customer_id)
        if account and account.get("login_customer_id"):
            return format_customer_id(account["login_customer_id"])
        default = allow.get("default_login_customer_id") or os.environ.get(
            "GOOGLE_ADS_LOGIN_CUSTOMER_ID", ""
        )
        return format_customer_id(default) if default else None

    def headers_for(customer_id: str, login_customer_id: Optional[str] = None) -> Dict[str, str]:
        headers = dict(get_headers(get_credentials()))
        login = resolve_login(customer_id, login_customer_id)
        if login:
            headers["login-customer-id"] = login
        else:
            headers.pop("login-customer-id", None)
        return headers

    def search(customer_id: str, query: str, login_customer_id: Optional[str] = None) -> List[Dict[str, Any]]:
        headers = headers_for(customer_id, login_customer_id)
        rows: List[Dict[str, Any]] = []
        token = None
        while True:
            body: Dict[str, Any] = {"query": query}
            if token:
                body["pageToken"] = token
            response = requests.post(
                f"{base_url}/customers/{customer_id}/googleAds:search",
                headers=headers,
                json=body,
                timeout=120,
            )
            if response.status_code != 200:
                raise ValueError(json.dumps(_summarize_error(response), ensure_ascii=False))
            data = response.json()
            rows.extend(data.get("results", []))
            token = data.get("nextPageToken")
            if not token:
                return rows

    def check_write(customer_id: str, operations: Any, validate_only: bool) -> tuple[str, bool]:
        cid = format_customer_id(customer_id)
        mode = _write_mode()
        if mode == "disabled":
            raise ValueError("Escrita desligada (GOOGLE_ADS_WRITE_MODE=disabled).")
        allow = _load_allowlist()
        if cid not in allow["accounts"]:
            raise ValueError(
                f"Conta {cid} fora da lista de contas permitidas ({ALLOWLIST_PATH}). "
                "Adicione a conta à lista antes de alterar."
            )
        if _contains_remove(operations) and not _allow_remove():
            raise ValueError(
                "Operação de exclusão (remove/REMOVED) bloqueada. Pause em vez de excluir, "
                "ou ligue GOOGLE_ADS_ALLOW_REMOVE=true conscientemente."
            )
        effective_validate = True if mode == "validate_only" else bool(validate_only)
        return cid, effective_validate

    def post_mutate(
        cid: str,
        path: str,
        body: Dict[str, Any],
        validate_only: bool,
        label: str,
        login_customer_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = {**body, "validateOnly": validate_only}
        response = requests.post(
            f"{base_url}/customers/{cid}/{path}",
            headers=headers_for(cid, login_customer_id),
            json=body,
            timeout=120,
        )
        ok = response.status_code == 200
        result: Dict[str, Any] = {
            "customer_id": cid,
            "account_name": _load_allowlist()["accounts"].get(cid, {}).get("name"),
            "endpoint": path,
            "validate_only": validate_only,
            "write_mode": _write_mode(),
            "ok": ok,
        }
        if ok:
            data = response.json() if response.text.strip() else {}
            result["result"] = data
            result["summary"] = (
                "Validado pela API, nada foi gravado. Para gravar, repita com validate_only=false."
                if validate_only
                else "Gravado na conta. Confira com get_change_history ou uma consulta GAQL."
            )
            if data.get("partialFailureError"):
                result["partial_failure"] = data["partialFailureError"]
        else:
            result["error"] = _summarize_error(response)
        _log(
            {
                "tool": label,
                "customer_id": cid,
                "endpoint": path,
                "validate_only": validate_only,
                "ok": ok,
                "operations": body.get("operations") or body.get("mutateOperations"),
                "response": result.get("result") if ok else result.get("error"),
            }
        )
        return result

    # ------------------------------------------------------------------ leitura

    @mcp.tool()
    async def list_allowed_accounts() -> str:
        """Lista as contas que este servidor pode alterar, com a MCC usada para entrar em cada uma.

        Mostra também o modo de escrita atual e se exclusões estão liberadas.
        """
        allow = _load_allowlist()
        return json.dumps(
            {
                "write_mode": _write_mode(),
                "allow_remove": _allow_remove(),
                "api_version": api_version,
                "allowlist_file": str(ALLOWLIST_PATH),
                "accounts": allow["accounts"],
            },
            ensure_ascii=False,
            indent=2,
        )

    @mcp.tool()
    async def gaql_search(
        customer_id: str,
        query: str,
        login_customer_id: Optional[str] = None,
        max_rows: int = 1000,
    ) -> str:
        """Roda uma consulta GAQL e devolve JSON, escolhendo a MCC de entrada sozinho.

        Args:
            customer_id: conta (10 dígitos, com ou sem traços).
            query: consulta GAQL.
            login_customer_id: MCC de entrada. Se vazio, usa a MCC da conta em
                allowed_accounts.json ou a MCC padrão.
            max_rows: limite de linhas devolvidas (padrão 1000).
        """
        cid = format_customer_id(customer_id)
        try:
            rows = search(cid, query, login_customer_id)
        except ValueError as error:
            return f"Erro na consulta: {error}"
        return json.dumps(
            {"customer_id": cid, "row_count": len(rows), "rows": rows[: max(1, max_rows)]},
            ensure_ascii=False,
        )

    @mcp.tool()
    async def get_change_history(
        customer_id: str,
        start_date: str,
        end_date: str,
        limit: int = 50,
    ) -> str:
        """Histórico de alterações da conta (change_event), para conferir o que foi gravado.

        Args:
            customer_id: conta.
            start_date: AAAA-MM-DD (no máximo 30 dias atrás, regra da API).
            end_date: AAAA-MM-DD.
            limit: máximo de eventos (até 10000).
        """
        cid = format_customer_id(customer_id)
        query = f"""
            SELECT change_event.change_date_time, change_event.user_email,
                   change_event.client_type, change_event.change_resource_type,
                   change_event.change_resource_name, change_event.resource_change_operation,
                   change_event.changed_fields, change_event.campaign, change_event.ad_group
            FROM change_event
            WHERE change_event.change_date_time >= '{start_date}'
              AND change_event.change_date_time <= '{end_date} 23:59:59'
            ORDER BY change_event.change_date_time DESC
            LIMIT {int(limit)}
        """
        try:
            rows = search(cid, query)
        except ValueError as error:
            return f"Erro na consulta: {error}"
        return json.dumps({"customer_id": cid, "events": rows}, ensure_ascii=False)

    # ------------------------------------------------------------------ escrita

    @mcp.tool()
    async def mutate(
        customer_id: str,
        resource: str,
        operations: List[Dict[str, Any]],
        validate_only: bool = True,
        partial_failure: bool = False,
        login_customer_id: Optional[str] = None,
    ) -> str:
        """Altera qualquer recurso do Google Ads pela API REST (POST customers/{id}/{resource}:mutate).

        Começa SEMPRE em validate_only=True (só valida). Mostre o antes/depois ao usuário,
        espere a confirmação e só então repita com validate_only=False para gravar.

        Args:
            customer_id: conta (precisa estar em allowed_accounts.json).
            resource: nome REST no plural, em camelCase. Exemplos: campaigns,
                campaignBudgets, adGroups, adGroupCriteria, campaignCriteria,
                adGroupAds, assets, campaignAssets, adGroupAssets, assetGroups,
                assetGroupAssets, sharedSets, sharedCriteria, campaignSharedSets,
                biddingStrategies, conversionActions, customerNegativeCriteria.
            operations: lista de operações no formato da API. Exemplos:
                {"update": {"resourceName": "customers/1/campaigns/2", "status": "PAUSED"}, "updateMask": "status"}
                {"create": {"adGroup": "customers/1/adGroups/3", "status": "ENABLED",
                            "keyword": {"text": "oleo motul", "matchType": "PHRASE"}}}
                Valores em dinheiro vão em micros (R$ 1,00 = 1000000).
            validate_only: True só valida; False grava.
            partial_failure: True grava as operações válidas mesmo se outras falharem.
            login_customer_id: MCC de entrada (opcional; padrão vem da lista de contas).
        """
        try:
            if not _RESOURCE.fullmatch(resource or ""):
                raise ValueError("resource deve ser um nome REST como campaigns ou adGroupCriteria")
            if not operations:
                raise ValueError("operations está vazio")
            cid, effective = check_write(customer_id, operations, validate_only)
        except ValueError as error:
            return json.dumps({"ok": False, "blocked": str(error)}, ensure_ascii=False)
        body: Dict[str, Any] = {"operations": operations}
        if partial_failure:
            body["partialFailure"] = True
        result = post_mutate(cid, f"{resource}:mutate", body, effective, "mutate", login_customer_id)
        return json.dumps(result, ensure_ascii=False, indent=2)

    @mcp.tool()
    async def mutate_multi(
        customer_id: str,
        mutate_operations: List[Dict[str, Any]],
        validate_only: bool = True,
        partial_failure: bool = False,
        login_customer_id: Optional[str] = None,
    ) -> str:
        """Várias alterações de recursos diferentes numa chamada só (googleAds:mutate).

        Útil para criar campanha + orçamento + grupo + anúncio de uma vez usando
        resource names temporários (IDs negativos, ex.: customers/1/campaignBudgets/-1).

        Args:
            customer_id: conta (precisa estar em allowed_accounts.json).
            mutate_operations: lista no formato da API, ex.:
                [{"campaignBudgetOperation": {"create": {...}}},
                 {"campaignOperation": {"create": {...}}}]
            validate_only: True só valida; False grava.
            partial_failure: True grava as válidas mesmo se outras falharem.
            login_customer_id: MCC de entrada (opcional).
        """
        try:
            if not mutate_operations:
                raise ValueError("mutate_operations está vazio")
            cid, effective = check_write(customer_id, mutate_operations, validate_only)
        except ValueError as error:
            return json.dumps({"ok": False, "blocked": str(error)}, ensure_ascii=False)
        body: Dict[str, Any] = {"mutateOperations": mutate_operations}
        if partial_failure:
            body["partialFailure"] = True
        result = post_mutate(cid, "googleAds:mutate", body, effective, "mutate_multi", login_customer_id)
        return json.dumps(result, ensure_ascii=False, indent=2)

    @mcp.tool()
    async def set_status(
        customer_id: str,
        level: str,
        ids: List[str],
        status: str,
        validate_only: bool = True,
    ) -> str:
        """Pausa ou ativa campanhas, grupos, anúncios, palavras-chave ou grupos de recursos (PMax).

        Args:
            customer_id: conta.
            level: campaign, ad_group, ad, keyword ou asset_group.
            ids: IDs. Para ad use "<ad_group_id>~<ad_id>"; para keyword use
                "<ad_group_id>~<criterion_id>".
            status: ENABLED ou PAUSED (exclusão não é feita por aqui).
            validate_only: True só valida; False grava.
        """
        status = (status or "").upper()
        try:
            if level not in _STATUS_RESOURCES:
                raise ValueError("level deve ser campaign, ad_group, ad, keyword ou asset_group")
            if status not in _STATUSES:
                raise ValueError("status deve ser ENABLED ou PAUSED")
            resource, pattern = _STATUS_RESOURCES[level]
            bad = [i for i in ids if not pattern.fullmatch(str(i))]
            if bad or not ids:
                raise ValueError(f"IDs inválidos para {level}: {bad or 'lista vazia'}")
            cid = format_customer_id(customer_id)
            operations = [
                {
                    "update": {"resourceName": f"customers/{cid}/{resource}/{i}", "status": status},
                    "updateMask": "status",
                }
                for i in ids
            ]
            cid, effective = check_write(cid, operations, validate_only)
        except ValueError as error:
            return json.dumps({"ok": False, "blocked": str(error)}, ensure_ascii=False)
        result = post_mutate(cid, f"{resource}:mutate", {"operations": operations}, effective, "set_status")
        return json.dumps(result, ensure_ascii=False, indent=2)

    @mcp.tool()
    async def update_campaign_budget(
        customer_id: str,
        campaign_id: str,
        daily_amount: float,
        validate_only: bool = True,
        allow_shared_budget: bool = False,
    ) -> str:
        """Muda o orçamento diário de uma campanha (valor em reais, ex.: 70.0 = R$ 70,00/dia).

        Lê o orçamento atual antes e devolve antes → depois. Recusa orçamento
        compartilhado (afeta outras campanhas) a menos que allow_shared_budget=True.
        """
        cid = format_customer_id(customer_id)
        try:
            if not _ID.fullmatch(str(campaign_id)):
                raise ValueError("campaign_id inválido")
            if daily_amount <= 0:
                raise ValueError("daily_amount deve ser maior que zero")
            rows = search(
                cid,
                "SELECT campaign.name, campaign_budget.resource_name, campaign_budget.amount_micros, "
                "campaign_budget.explicitly_shared, campaign_budget.reference_count "
                f"FROM campaign WHERE campaign.id = {campaign_id}",
            )
            if not rows:
                raise ValueError("campanha não encontrada")
            budget = rows[0]["campaignBudget"]
            shared = bool(budget.get("explicitlyShared")) or int(budget.get("referenceCount", 1)) > 1
            if shared and not allow_shared_budget:
                raise ValueError(
                    "Orçamento compartilhado com outras campanhas; repita com allow_shared_budget=True se for intencional."
                )
            new_micros = int(round(daily_amount * 1_000_000 / 10_000)) * 10_000
            operations = [
                {
                    "update": {"resourceName": budget["resourceName"], "amountMicros": str(new_micros)},
                    "updateMask": "amount_micros",
                }
            ]
            cid, effective = check_write(cid, operations, validate_only)
        except ValueError as error:
            return json.dumps({"ok": False, "blocked": str(error)}, ensure_ascii=False)
        result = post_mutate(cid, "campaignBudgets:mutate", {"operations": operations}, effective, "update_campaign_budget")
        result["campaign"] = rows[0]["campaign"].get("name")
        result["before_daily"] = int(budget.get("amountMicros", 0)) / 1_000_000
        result["after_daily"] = new_micros / 1_000_000
        result["shared_budget"] = shared
        return json.dumps(result, ensure_ascii=False, indent=2)

    @mcp.tool()
    async def add_keywords(
        customer_id: str,
        ad_group_id: str,
        keywords: List[Dict[str, str]],
        cpc_bid: Optional[float] = None,
        status: str = "ENABLED",
        validate_only: bool = True,
    ) -> str:
        """Adiciona palavras-chave positivas a um grupo de anúncios.

        Args:
            keywords: [{"text": "oleo motul", "match_type": "PHRASE"}] — EXACT, PHRASE ou BROAD.
            cpc_bid: lance de CPC em reais (opcional; só vale para lance manual).
            status: ENABLED ou PAUSED.
        """
        cid = format_customer_id(customer_id)
        try:
            if not _ID.fullmatch(str(ad_group_id)):
                raise ValueError("ad_group_id inválido")
            status = status.upper()
            if status not in _STATUSES:
                raise ValueError("status deve ser ENABLED ou PAUSED")
            operations = []
            for kw in keywords:
                match = str(kw.get("match_type", "")).upper()
                if match not in _MATCH_TYPES or not kw.get("text"):
                    raise ValueError(f"palavra-chave inválida: {kw}")
                create: Dict[str, Any] = {
                    "adGroup": f"customers/{cid}/adGroups/{ad_group_id}",
                    "status": status,
                    "keyword": {"text": kw["text"], "matchType": match},
                }
                if cpc_bid:
                    create["cpcBidMicros"] = str(int(round(cpc_bid * 1_000_000 / 10_000)) * 10_000)
                operations.append({"create": create})
            if not operations:
                raise ValueError("keywords está vazio")
            cid, effective = check_write(cid, operations, validate_only)
        except ValueError as error:
            return json.dumps({"ok": False, "blocked": str(error)}, ensure_ascii=False)
        result = post_mutate(cid, "adGroupCriteria:mutate", {"operations": operations}, effective, "add_keywords")
        return json.dumps(result, ensure_ascii=False, indent=2)

    @mcp.tool()
    async def add_negative_keywords(
        customer_id: str,
        level: str,
        parent_id: str,
        keywords: List[Dict[str, str]],
        validate_only: bool = True,
    ) -> str:
        """Adiciona palavras-chave negativas na campanha ou no grupo de anúncios.

        Args:
            level: campaign ou ad_group.
            parent_id: ID da campanha ou do grupo.
            keywords: [{"text": "gratis", "match_type": "BROAD"}] — EXACT, PHRASE ou BROAD.
        """
        cid = format_customer_id(customer_id)
        try:
            if level not in {"campaign", "ad_group"}:
                raise ValueError("level deve ser campaign ou ad_group")
            if not _ID.fullmatch(str(parent_id)):
                raise ValueError("parent_id inválido")
            operations = []
            for kw in keywords:
                match = str(kw.get("match_type", "")).upper()
                if match not in _MATCH_TYPES or not kw.get("text"):
                    raise ValueError(f"negativa inválida: {kw}")
                create: Dict[str, Any] = {
                    "negative": True,
                    "keyword": {"text": kw["text"], "matchType": match},
                }
                if level == "campaign":
                    create["campaign"] = f"customers/{cid}/campaigns/{parent_id}"
                else:
                    create["adGroup"] = f"customers/{cid}/adGroups/{parent_id}"
                operations.append({"create": create})
            if not operations:
                raise ValueError("keywords está vazio")
            cid, effective = check_write(cid, operations, validate_only)
        except ValueError as error:
            return json.dumps({"ok": False, "blocked": str(error)}, ensure_ascii=False)
        resource = "campaignCriteria" if level == "campaign" else "adGroupCriteria"
        result = post_mutate(cid, f"{resource}:mutate", {"operations": operations}, effective, "add_negative_keywords")
        return json.dumps(result, ensure_ascii=False, indent=2)
