# Dossiê aprovado — {tipo} — {cliente} — {escopo}

> Criar este arquivo somente após o gestor aprovar editorialmente a versão completa apresentada no chat. Não usar como rascunho de trabalho.

O primeiro bloco JSON contém a mesma análise estruturada exibida abaixo. Substitua todos os placeholders, inclusive o objeto `analysis`, antes de validar em `schemas/operation-dossier.schema.json` e `scripts/validate_dossier.py`.

```json
{
  "schema_version": "1.1",
  "operation_id": "op-AAAAMMDD-HHMM-cliente-escopo",
  "version": 1,
  "status": "analysis_only",
  "type": "analise",
  "client_slug": "cliente",
  "platform": "meta",
  "active_platforms": ["meta"],
  "source_modes": {"meta": "connected_read"},
  "created_at": "AAAA-MM-DDTHH:MM:SS-03:00",
  "updated_at": "AAAA-MM-DDTHH:MM:SS-03:00",
  "scope": "escopo aprovado",
  "accounts": {"meta": "account-****0000"},
  "currencies": {"meta": "BRL"},
  "timezones": {"meta": "America/Sao_Paulo"},
  "sources": ["fonte efetivamente usada"],
  "route": {
    "router_version": "1.1.0",
    "intent": "analise",
    "route_ids": ["analise:meta:connected_read"],
    "output_contracts": {"meta": "relatorio_analise"},
    "planned_skills": [],
    "executed_skills": [],
    "skipped_skills": [],
    "gates": [],
    "dossier_persistence": "after_editorial_approval",
    "final_state": "analysis_only"
  },
  "record_approval": {
    "approved": true,
    "approved_by": "gestor",
    "approved_at": "AAAA-MM-DDTHH:MM:SS-03:00",
    "diagnostic_id": "diag-AAAAMMDD-cliente-escopo",
    "diagnostic_version": 1,
    "content_hash": "0000000000000000000000000000000000000000000000000000000000000000",
    "statement": "declaração literal de aprovação para registro"
  },
  "analysis": {},
  "changes": [],
  "approval": {"approved": false, "approved_by": null, "approved_at": null, "version": null, "hash": null, "statement": null},
  "execution": {"started_at": null, "finished_at": null, "results": [], "post_snapshot": null}
}
```

## Veredito aprovado

- Resultado observado:
- Causa/gargalo principal:
- Confiança:
- Decisão necessária:

## Escopo, fontes e confiabilidade

| Plataforma | Conta mascarada | Fonte/modo | Extraído em | Janela | Comparação | Atribuição | Moeda/timezone |
|---|---|---|---|---|---|---|---|

- Gate de mensuração:
- Divergências que afetam a leitura:
- Mudanças/eventos relevantes:

## Cobertura do diagnóstico

| Plataforma | Camada | Status | Entidades | Cobertura de investimento | Cobertura de conversões | Fonte | Motivo/limitação |
|---|---|---|---:|---:|---:|---|---|

Uma análise `full` não pode omitir camada aplicável. Use `analyzed`, `unavailable`, `insufficient` ou `not_applicable`.

## KPIs e comparação

| Plataforma/fonte | KPI | Definição/denominador | Unidade | Atual | Comparação | Delta absoluto | Delta % | Meta/limite |
|---|---|---|---|---:|---:|---:|---:|---:|

## Evidências

| Evidência | Plataforma/nível | Período | Fonte | Dados e comparação | Leitura | Limitação |
|---|---|---|---|---|---|---|

## Diagnóstico por plataforma e nível

Apresentar os níveis na ordem hierárquica e explicar contribuição, concentração, ganhadores, perdedores e outliers. Em multicanal, concluir cada plataforma separadamente antes da síntese comercial.

## Achados

| Achado | Classe | Plataforma/nível | Evidências | Impacto | Hipótese principal | Alternativa | Verificação discriminante | Confiança | Limitação |
|---|---|---|---|---|---|---|---|---|---|

## Plano de ação aprovado

| Ação | Tipo | Achados | Alvo exato | Baseline | Ação exata | Resultado esperado | Prioridade/confiança | Responsável/prazo | Janela | Sucesso | Parada | Dependência/risco |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Separar investigação, teste, recomendação e mudança candidata. Ação sem achado e evidência não entra.

## Decisões e limitações

- Aprovado no conteúdo:
- Rejeitado ou removido durante a iteração:
- Pendente de decisão:
- Dados indisponíveis e forma de obtê-los:

## Aprovação editorial para registro

- Diagnostic ID/versão:
- Responsável:
- Data/hora:
- Declaração literal:
- Hash do conteúdo aprovado:

## Change set — somente quando houver mutação proposta

| Ordem | ID | Ações | Achados | Evidências | Plataforma | Alvo/campo | Antes | Depois | Impacto esperado/financeiro | Confiança | Precondições/dependências | Risco | Reversão | Responsável/janela | Sucesso/parada | Modo |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Este bloco persistido continua não aprovado operacionalmente até `/aprovar-operacao <id>`.

## Apêndice técnico

- Intenção e rotas:
- Skills planejadas:
- Skills executadas:
- Skills puladas e motivo:
- Gates:

Acrescentar `Aprovação operacional`, `Preflight e execução`, `Snapshot posterior` e `Reversão` somente quando esses eventos realmente acontecerem. Nunca deixar seções vazias antecipadamente.
