---
name: 13-approved-change-executor
description: Revalida e executa somente change set de plataforma explicitamente aprovado, registrando resultado por item e snapshot posterior. Use exclusivamente em /executar-operacao ou reversão aprovada; Google Ads permanece manual_only enquanto não houver escrita homologada.
---

# Executor de Mudanças Aprovadas

## Pré-condições obrigatórias

1. Comando explícito `/executar-operacao <id>`.
2. Dossiê com status `approved`.
3. Responsável, horário, versão e hash de aprovação.
4. Plataforma e conta `validated_write`; o conector Google Ads V1.1 inicial não satisfaz este gate.
5. `quality/execution-checklist.md` aprovado.

## Preflight

1. Recalcular hash; bloquear se divergir.
2. Reler cada alvo e comparar com o snapshot.
3. Invalidar aprovação diante de drift material.
4. Confirmar ferramenta, permissão, parâmetros e ordem.
5. Remover da fila itens `manual_only`, `blocked`, exclusão ou arquivamento. Se o lote for Google Ads e `write_tools_registered` não estiver homologado como verdadeiro, bloquear toda chamada de escrita.

## Execução

1. Alterar status para `executing`.
2. Executar um item por vez na ordem aprovada.
3. Registrar ferramenta/operação, alvo, timestamp e resultado sanitizado.
4. Não improvisar alternativa se um item falhar.
5. Parar quando a falha tornar os próximos itens inseguros; marcar os restantes `not_attempted`.
6. Capturar snapshot posterior.

## Status final

- `executed`: todos os itens aplicáveis confirmados.
- `partial_failure`: pelo menos um sucesso e um failed/not_attempted.
- `failed`: nada aplicado ou preflight bloqueou.
- `reverted`: somente quando o lote era uma reversão aprovada e o estado foi confirmado.

## Proibições

Não executar por frases genéricas. Não ampliar o lote. Não esconder falha. Não declarar sucesso antes do readback. Não usar browser como fallback.
