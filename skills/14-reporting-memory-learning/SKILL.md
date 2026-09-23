---
name: 14-reporting-memory-learning
description: Gera relatórios Meta Ads, Google Ads ou multicanal, atualiza a memória local do cliente e propõe aprendizados sanitizados. Use em /relatorio-performance ou fechamento de análise/operação.
---

# Relatório, Memória e Aprendizado

## Leituras

1. `templates/relatorio-performance.md` e `templates/resposta-chat.md`.
2. `quality/reporting-scorecard.md`.
3. `CLIENTE.md`, `python3 scripts/client_history.py list {slug}` e os dossiês relevantes (legados e V2).
4. Trilha de negócio aplicável.

## Processo

1. Confirmar período, comparação, atribuição e status das candidatas/dossiês existentes.
2. Consolidar fatos sem misturar plataformas, atribuições, populações ou denominadores.
3. Gerar uma única representação estruturada e projetá-la primeiro no chat.
4. Apresentar no chat sumário executivo, cobertura, escopo/fontes, KPIs comparativos, evidências, diagnóstico, hipóteses, plano de ação, decisões, mudanças, impacto, riscos, limitações e próximo passo.
5. Separar resultado observado de impacto causal. Explicar por que cada resultado está bom ou ruim à luz da base oficial (skill 15 ou 17) e registrar essas checagens.
6. Para operações executadas cuja janela de avaliação venceu, propor a avaliação: comparar com os critérios registrados e, com o aval do gestor, registrar com `dossier.py evaluate`.
7. Iterar até existir versão final e pedir aprovação do conteúdo.
8. Depois da aprovação, registrar com `scripts/dossier.py new`, com o mesmo texto.
9. Atualizar `CLIENTE.md` acrescentando histórico em uma linha por operação, do mais recente para o mais antigo; regras duráveis sobre o cliente vão para a seção de aprendizados. Nunca apagar aprendizado anterior.
10. Gerar proposta de aprendizado sanitizado quando houver padrão reutilizável.

## Governança do aprendizado

Remover nome, ID, valores, oferta, criativo e qualquer identificador. Declarar número de casos, fonte, escopo e limitação. Um caso isolado é evidência limitada. Pedir aprovação de Davi antes de escrever em `knowledge/sanitized-learnings/`.

## Saída

- Relatório completo e autossuficiente no chat; o gestor não precisa abrir o dossiê para compreender ou decidir.
- Dossiê criado/atualizado somente após aprovação editorial.
- Ficha do cliente atualizada.
- Proposta sanitizada separada, se aplicável.

Depois do registro, informar numa linha o caminho do dossiê e o próximo passo. Não despejar IDs, JSON, logs ou respostas brutas no chat.

Não confundir aprovação do gestor com melhora medida de performance.
