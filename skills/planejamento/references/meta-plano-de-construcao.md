<!-- Referência do módulo `planejamento`; etapa `planejamento/meta-plano-de-construcao` nas rotas. -->

# Plano de Construção Meta Ads

## Pré-requisitos

1. Etapas `conexao/meta` e `planejamento/meta-estrategia` a `planejamento/meta-briefing-criativo` concluídas conforme `dependency_graph.json`.
2. Conta e mensuração validadas.
3. Versão candidata no chat; dossiê ainda inexistente em demanda nova.

## Processo

1. Consolidar todos os parâmetros nos níveis campanha, conjunto e anúncio.
2. Marcar campos confirmados, hipóteses e indisponíveis.
3. Verificar compatibilidade entre objetivo, conversion location, performance goal, evento, público, posicionamento, budget, lance e criativo.
4. Definir status inicial seguro; preferir criação pausada quando a ferramenta permitir.
5. Gerar change set versionado com ordem, antes/depois, risco e reversão.
6. Apresentar tudo no chat no formato de `templates/resposta-chat.md`. Depois da aprovação do conteúdo, registrar com `scripts/dossier.py new` (nasce `proposed`); só então orientar `/aprovar-operacao`. Consultar `knowledge/platform-quirks/meta-ads-mcp.md`: conjuntos de formulário nativo e vídeo com WhatsApp têm limitações no conector.

## Gate

Não chamar ferramenta de escrita nesta skill. Plano completo não é aprovação. Se um criativo/URL/identidade estiver ausente, marcar item `blocked` em vez de improvisar.

## Saída

Resumo executivo, mapa hierárquico, tabela de configuração, checklist pré-lançamento, change set e impacto financeiro.
