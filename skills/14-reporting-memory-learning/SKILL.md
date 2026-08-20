---
name: 14-reporting-memory-learning
description: Gera relatórios Meta Ads, Google Ads ou multicanal, atualiza a memória local do cliente e propõe aprendizados sanitizados. Use em /relatorio-performance ou fechamento de análise/operação.
---

# Relatório, Memória e Aprendizado

## Leituras

1. `templates/relatorio-performance.md`.
2. `quality/reporting-scorecard.md`.
3. Dossiês e `CLIENTE.md`.
4. Trilha de negócio aplicável.

## Processo

1. Confirmar período, comparação, atribuição e status das candidatas/dossiês existentes.
2. Consolidar fatos sem misturar plataformas, atribuições, populações ou denominadores.
3. Gerar uma única representação estruturada e projetá-la primeiro no chat.
4. Apresentar no chat sumário executivo, cobertura, escopo/fontes, KPIs comparativos, evidências, diagnóstico, hipóteses, plano de ação, decisões, mudanças, impacto, riscos, limitações e próximo passo.
5. Separar resultado observado de impacto causal.
6. Iterar até existir versão final candidata e pedir aprovação editorial.
7. Somente depois da aprovação criar/atualizar o dossiê com o conteúdo idêntico.
8. Atualizar `CLIENTE.md` acrescentando histórico; nunca apagar aprendizado anterior.
9. Gerar proposta de aprendizado sanitizado quando houver padrão reutilizável.

## Governança do aprendizado

Remover nome, ID, valores, oferta, criativo e qualquer identificador. Declarar número de casos, fonte, escopo e limitação. Um caso isolado é evidência limitada. Pedir aprovação de Davi antes de escrever em `knowledge/sanitized-learnings/`.

## Saída

- Relatório completo e autossuficiente no chat; o gestor não precisa abrir o dossiê para compreender ou decidir.
- Dossiê criado/atualizado somente após aprovação editorial.
- Ficha do cliente atualizada.
- Proposta sanitizada separada, se aplicável.

Antes da aprovação, informar `diagnostic_id` e versão candidata. Depois da persistência, informar `operation_id`, status e caminho como referência. Não despejar JSON, logs ou respostas brutas no chat.

Não confundir aprovação do gestor com melhora medida de performance.
