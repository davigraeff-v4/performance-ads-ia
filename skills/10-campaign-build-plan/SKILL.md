---
name: 10-campaign-build-plan
description: Consolida estratégia, arquitetura, públicos, budget, lances, tracking e criativos em um plano completo de campanha e change set aprovável. Use em /criar-campanha antes de qualquer criação no Meta.
---

# Plano de Construção de Campanha

## Pré-requisitos

1. Skills `02`–`09` concluídas conforme `dependency_graph.json`.
2. Conta e mensuração validadas.
3. Dossiê em `draft`.

## Processo

1. Consolidar todos os parâmetros nos níveis campanha, conjunto e anúncio.
2. Marcar campos confirmados, hipóteses e indisponíveis.
3. Verificar compatibilidade entre objetivo, conversion location, performance goal, evento, público, posicionamento, budget, lance e criativo.
4. Definir status inicial seguro; preferir criação pausada quando a ferramenta permitir.
5. Gerar change set versionado com ordem, antes/depois, risco e reversão.
6. Atualizar dossiê para `proposed` e solicitar `/aprovar-operacao <id>`.

## Gate

Não chamar ferramenta de escrita nesta skill. Plano completo não é aprovação. Se um criativo/URL/identidade estiver ausente, marcar item `blocked` em vez de improvisar.

## Saída

Resumo executivo, mapa hierárquico, tabela de configuração, checklist pré-lançamento, change set e impacto financeiro.
