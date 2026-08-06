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

1. Confirmar período, comparação, atribuição e status dos dossiês.
2. Consolidar fatos sem misturar plataformas, atribuições, populações ou denominadores.
3. Gerar uma única representação estruturada do resultado e projetá-la em dois destinos: dossiê local e relatório completo no chat.
4. Apresentar no chat sumário executivo, escopo/fontes, resultado de negócio, diagnóstico, hipóteses, plano de ação, decisões, mudanças, impacto, riscos, limitações e próximo passo.
5. Separar resultado observado de impacto causal.
6. Atualizar `CLIENTE.md` acrescentando histórico; nunca apagar aprendizado anterior.
7. Gerar proposta de aprendizado sanitizado quando houver padrão reutilizável.

## Governança do aprendizado

Remover nome, ID, valores, oferta, criativo e qualquer identificador. Declarar número de casos, fonte, escopo e limitação. Um caso isolado é evidência limitada. Pedir aprovação de Davi antes de escrever em `knowledge/sanitized-learnings/`.

## Saída

- Relatório completo e autossuficiente no chat; o gestor não precisa abrir o dossiê para compreender ou decidir.
- Dossiê encerrado ou atualizado.
- Ficha do cliente atualizada.
- Proposta sanitizada separada, se aplicável.

Informar `operation_id`, status e caminho do dossiê somente como referência ao final. Não despejar JSON, logs ou respostas brutas no chat.

Não confundir aprovação do gestor com melhora medida de performance.
