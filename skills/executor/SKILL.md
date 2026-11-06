---
name: executor
description: Revalida e executa somente change set de plataforma explicitamente aprovado, registrando resultado por item e snapshot posterior. Use exclusivamente em /executar-operacao ou reversão aprovada; no Google Ads executa só pelo servidor googleAdsServer, validando cada item antes de gravar.
---

# Executor de Mudanças Aprovadas

## Pré-condições obrigatórias

1. Comando explícito `/executar-operacao <id>`.
2. Operação V2 (`clients/{slug}/operacoes/`) com status `approved`, conferida por `python3 scripts/dossier.py verify {operation_id}`. Operação legada aberta precisa ser migrada antes (roteador, seção 7).
3. Responsável, horário, versão e hash de aprovação.
4. Plataforma e conta `validated_write`. No Google Ads, vale o gate da seção 8.1 do contrato (servidor `googleAdsServer`, `write_mode` `execute`, conta na lista permitida); o MCP oficial `google_ads` e o complemento `google_ads_extended` não satisfazem este gate.
5. `quality/execution-checklist.md` aprovado.
6. `knowledge/platform-quirks/` lido para a plataforma do lote.

## Preflight

1. Rodar `dossier.py verify`; se o hash das mudanças não conferir, bloquear.
2. Reler cada alvo e comparar com o snapshot.
3. Invalidar aprovação diante de drift material.
4. Confirmar ferramenta, permissão, parâmetros e ordem.
5. Remover da fila itens `manual_only`, `blocked`, exclusão ou arquivamento. Se o lote for Google Ads e `list_allowed_accounts` não mostrar `write_mode` `execute` com a conta alvo na lista, bloquear toda chamada de escrita e tratar os itens como `manual_only`. Passando, repetir cada item Google Ads com `validate_only=true`: se a API recusar, o item fica `not_attempted` com o erro no detalhe, e a execução para quando os próximos dependerem dele. Se o lote incluir item originado em `mensuracao/gtm`, bloquear a chamada a menos que `write_mode` esteja `execute` e o `container_id` do alvo esteja na allowlist local (`PERFORMANCE_ADS_GTM_ALLOWED_CONTAINER_IDS`). Em `validate_only`, o script devolve o que seria enviado sem gravar nada: registrar o item como `not_attempted` com essa prévia no detalhe.

## Execução

1. Executar um item por vez na ordem aprovada. Depois de `ads_update_entity` no Meta, reativar e conferir o status da entidade (o conector força pausa). No Google Ads, gravar com `validate_only=false` exatamente a chamada validada, sem mudar parâmetros; depois reler o alvo por GAQL (`gaql_search`) e conferir em `get_change_history` que a alteração aparece.
2. Anotar para cada item: ferramenta, horário, resultado sanitizado e leitura de confirmação na plataforma.
3. Não improvisar alternativa se um item falhar.
4. Parar quando a falha tornar os próximos itens inseguros; os restantes ficam `not_attempted`.
5. Capturar o estado posterior por leitura.
6. Registrar tudo de uma vez: `python3 scripts/dossier.py record-execution {operation_id} --results '<lista>' --post-snapshot "<resumo>"`. Cada resultado tem `change_id`, `status` (`success`, `executed_manually`, `failed`, `not_attempted`), `via`, `detail`, `readback_confirmed` e `divergences`.
7. Itens `manual_only` e o que o gestor fizer à mão são registrados como `executed_manually` depois da confirmação por leitura, com toda diferença em relação ao aprovado em `divergences`.

## Status final

O `dossier.py` calcula o status a partir dos resultados:

- `executed`: todos os itens executáveis aplicados, pelo conector ou manualmente;
- `partial_failure`: pelo menos um aplicado e um `failed` ou `not_attempted`;
- `failed`: nada aplicado;
- `reverted`: quando o lote era uma reversão e tudo foi aplicado.

No chat, explicar o resultado item por item em linguagem simples, com as diferenças em destaque, e dizer quando o resultado será avaliado.

## Proibições

Não executar por frases genéricas. Não ampliar o lote. Não esconder falha. Não declarar sucesso antes do readback. Não usar browser como fallback. No Google Ads, não ligar `GOOGLE_ADS_ALLOW_REMOVE` e não mexer na lista de contas nem no modo de escrita para destravar uma execução. Não publicar versão do GTM sob nenhuma circunstância — a integração não suporta e não deve simular esse passo; itens que dependem de publicação terminam com instrução manual explícita.
