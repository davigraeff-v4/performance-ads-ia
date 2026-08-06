# Dossiê — {tipo} — {cliente} — {escopo}

```json
{
  "schema_version": "1.0",
  "operation_id": "op-AAAAMMDD-HHMM-cliente-escopo",
  "version": 1,
  "status": "draft",
  "type": "analise",
  "client_slug": "cliente",
  "platform": "meta",
  "active_platforms": ["meta"],
  "source_modes": {"meta": "context_only"},
  "created_at": "AAAA-MM-DDTHH:MM:SS-03:00",
  "updated_at": "AAAA-MM-DDTHH:MM:SS-03:00",
  "scope": "escopo confirmado",
  "accounts": {"meta": null},
  "currencies": {"meta": null},
  "timezones": {"meta": null},
  "sources": [],
  "route": {
    "router_version": "1.0.0",
    "intent": "analise",
    "route_ids": ["analise:meta:context_only"],
    "output_contracts": {"meta": "relatorio_analise"},
    "planned_skills": [],
    "executed_skills": [],
    "skipped_skills": [],
    "gates": [],
    "final_state": "analysis_only"
  },
  "changes": [],
  "approval": {
    "approved": false,
    "approved_by": null,
    "approved_at": null,
    "version": null,
    "hash": null,
    "statement": null
  },
  "execution": {
    "started_at": null,
    "finished_at": null,
    "results": [],
    "post_snapshot": null
  }
}
```

## Solicitação, objetivo e escopo

- Solicitação:
- Resultado comercial esperado:
- Responsável:
- Plataformas solicitadas/ativas:
- Modo de fonte por plataforma:
- Conta/ID mascarado por plataforma:
- Campanha/objeto:

## Rota executada

- Intenção e rota por plataforma:
- Skills planejadas:
- Skills executadas:
- Skills puladas e motivo:
- Gates e decisão:
- Estado final:

## Fontes e janela

- Extraído em:
- Timezone/moeda por plataforma:
- Janela:
- Comparação:
- Atribuição:
- Fontes Meta Ads:
- Fontes Google Ads:
- Fontes comerciais/externas:
- URLs oficiais verificadas:

## Qualidade dos dados

- Gate: confiavel | utilizavel_com_ressalvas | insuficiente
- Divergências:
- Limitações:

## Diagnóstico acionável

| Achado | Classe | Plataforma/nível | Evidência | Impacto | Hipótese principal | Alternativa | Verificação | Confiança | Limitação |
|---|---|---|---|---|---|---|---|---|---|

## Plano de ação

| Prioridade | Achado | Ação exata/alvo | Responsável | Prazo | Janela | Sucesso | Parada |
|---|---|---|---|---|---|---|---|

## Snapshot anterior

Registre somente campos necessários à decisão e reversão.

## Change set

| Ordem | ID | Achados | Plataforma | Alvo/campo | Antes | Depois | Evidência | Impacto esperado/financeiro | Confiança | Precondições/dependências | Risco | Reversão | Responsável/janela | Sucesso/parada | Modo |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Aprovação

- Status:
- Responsável:
- Data/hora:
- Versão:
- Hash:
- Declaração literal:

## Preflight e execução

- Hash, estado, conta e permissão conferem:
- Itens bloqueados/manuais:
- Resultado por change ID:
- Falha parcial e estado final:

## Conclusão e relatório no chat

- Resumo entregue no chat em:
- Próxima decisão:
- O gestor recebeu conteúdo suficiente para decidir sem abrir este arquivo: sim | não

Em dossiê multicanal, concluir cada plataforma separadamente antes da síntese. Mutações usam `operation_id` e aprovação independentes por plataforma.

## Aprendizados locais e proposta sanitizada

Não promover à base versionável antes da aprovação de Davi.
