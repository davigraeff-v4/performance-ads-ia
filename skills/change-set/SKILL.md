---
name: change-set
description: Transforma diagnóstico Meta Ads ou Google Ads em lote versionado de otimizações com antes/depois, impacto, risco e reversão. Use em /otimizar-campanha ou quando recomendações virarem alterações aprováveis.
---

# Change Set de Otimização

## Pré-requisitos

1. Etapa `diagnostico/meta` para Meta Ads ou `diagnostico/google-ads` para Google Ads, com diagnóstico e evidências. Em um build plan, `planejamento/meta-plano-de-construcao` ou `planejamento/google-ads-plano-de-construcao` pode originar o lote, mantendo os mesmos gates. Em `ajuste`, a origem é a decisão do gestor: registrar a motivação dele como justificativa e ler o estado atual do alvo. Em reversão, o dossiê executado e o snapshot anterior substituem o diagnóstico somente para restaurar valores conhecidos.
2. Candidato final no chat com uma única plataforma de mutação; o dossiê ainda não deve existir, salvo continuação de uma operação já registrada.
3. Estado atual dos alvos.
4. Checagem de boas práticas das premissas de cada item pela etapa `revisor/meta` (Meta, mais `ads_get_help_article`) ou `revisor/google-ads` (Google Ads), começando por `python3 scripts/kb_check.py --platform {meta|google_ads} "premissa…"`. É obrigatória: o `dossier.py` recusa operação com mudanças sem `knowledge_checks`, e recusa veredito sustenta ou contradiz sem o link oficial.
5. `knowledge/platform-quirks/` para saber o que o conector consegue ou não fazer. Por exemplo, o conector Meta não cria conjuntos de formulário nativo, então esse item é `manual_only`.

## Processo

1. Rejeitar diagnóstico `full` com camada aplicável ausente e ação cujo nível-alvo não esteja `analyzed`.
2. Selecionar somente recomendações que sustentem ação.
3. Ordenar dependências e separar itens independentes.
4. Para cada item, definir no formato do spec (`examples/synthetic/v2/otimizacao-remarketing.spec.json`): título em linguagem de ação, plataforma, conta, alvo (tipo, ID e nome), campo, antes, depois, tipo de ação (`create`, `update`, `pause`, `activate`), modo de execução (`mcp`, `api_script`, `manual_only`, `blocked`), por quê (citando o achado pelo nome), resultado esperado, efeito no orçamento diário, risco, como desfazer, ordem e dependências.
5. Definir a avaliação da operação: data a partir da qual avaliar, critérios de sucesso com número e critérios de parada.
6. Quantificar o efeito no orçamento quando houver budget.
7. Marcar como `manual_only` o que o conector não suporta; Google Ads permanece assim enquanto não houver escrita homologada.
8. Proibir exclusão e arquivamento, inclusive na reversão (reverter é pausar ou restaurar valor).
9. Apresentar as mudanças no chat em blocos, no formato de `templates/resposta-chat.md`.
10. Depois da aprovação do conteúdo, registrar com `scripts/dossier.py new`: o status nasce `proposed` e o script calcula os hashes.

## Checkpoint

Primeiro pedir aprovação do conteúdo para registrar diagnóstico, plano e mudanças. Depois do registro, explicar que `/aprovar-operacao` é uma aprovação de execução separada. Não executar nesta skill.

## Validação

- Nenhum alvo fora da plataforma e conta confirmadas.
- Nenhuma mudança implícita.
- Todo budget tem atual, proposto e impacto.
- Toda reversão usa valor conhecido.
- Todo item diz de qual achado vem e a operação tem critérios de avaliação verificáveis.
- Itens bloqueados não entram como executáveis.
