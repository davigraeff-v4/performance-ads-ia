---
name: 12-optimization-change-set
description: Transforma diagnóstico Meta Ads ou Google Ads em lote versionado de otimizações com antes/depois, impacto, risco e reversão. Use em /otimizar-campanha ou quando recomendações virarem alterações aprováveis.
---

# Change Set de Otimização

## Pré-requisitos

1. Skill `11` para Meta Ads ou `24` para Google Ads, com diagnóstico, cobertura e evidências identificadas. Em um build plan, `10` ou `23` pode originar o lote, mantendo os mesmos gates. Em reversão, o dossiê executado e o snapshot anterior substituem o diagnóstico somente para restaurar valores conhecidos.
2. Candidato final no chat com uma única plataforma de mutação; o dossiê ainda não deve existir, salvo continuação de uma operação já registrada.
3. Estado atual dos alvos.
4. Se algum item do lote depender de entender um mecanismo específico da plataforma (ex: como um tipo de orçamento, lance ou elegibilidade de recurso funciona) que o diagnóstico de origem ainda não esclareceu, consultar a skill `15` (Meta) ou `17` (Google Ads) antes de escrever a justificativa do item — não assumir funcionamento de memória.

## Processo

1. Rejeitar diagnóstico `full` com camada aplicável ausente e ação cujo nível-alvo não esteja `analyzed`.
2. Selecionar somente recomendações que sustentem ação.
3. Ordenar dependências e separar itens independentes.
4. Para cada item, registrar `action_ids`, `finding_ids`, `evidence_ids`, alvo, campo, antes, depois, justificativa, impacto esperado, impacto financeiro, confiança, risco, reversão, precondições, dependências, ordem, responsável, janela e critérios de sucesso e parada.
5. Quantificar impacto financeiro quando houver budget.
6. Marcar ações não suportadas como `manual_only`; Google Ads permanece assim enquanto não houver escrita homologada.
7. Proibir itens de exclusão/arquivamento.
8. Apresentar o change set completo como parte da versão final candidata no chat.
9. Após aprovação editorial, criar o dossiê como `proposed` e calcular o hash operacional do change set.

## Checkpoint

Primeiro pedir aprovação editorial para registrar o diagnóstico, plano e change set no dossiê. Depois da persistência, explicar que `/aprovar-operacao <id>` é uma aprovação operacional separada. Não executar nesta skill.

## Validação

- Nenhum alvo fora da plataforma e conta confirmadas.
- Nenhuma mudança implícita.
- Todo budget tem atual, proposto e impacto.
- Toda reversão usa valor conhecido.
- Todo item aponta para ação, achado e evidência identificados e possui responsável, janela e critérios verificáveis.
- Itens bloqueados não entram como executáveis.
