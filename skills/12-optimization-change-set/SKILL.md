---
name: 12-optimization-change-set
description: Transforma um diagnóstico aprovado em um lote versionado de otimizações com antes/depois, impacto, risco e reversão. Use em /otimizar-campanha ou sempre que recomendações precisarem virar alterações aprováveis.
---

# Change Set de Otimização

## Pré-requisitos

1. Skill `11` com diagnóstico e fontes.
2. Dossiê atual.
3. Estado atual dos alvos.

## Processo

1. Selecionar somente recomendações que sustentem ação.
2. Ordenar dependências e separar itens independentes.
3. Para cada item, registrar alvo, campo, antes, depois, justificativa, evidência, impacto, risco, reversão e precondição.
4. Quantificar impacto financeiro quando houver budget.
5. Marcar ações não suportadas como `manual_only`.
6. Proibir itens de exclusão/arquivamento.
7. Calcular versão/hash conforme contrato.
8. Mudar dossiê para `proposed`.

## Checkpoint

Apresentar lote completo e perguntar se o gestor aprova exatamente aquela versão. Orientar `/aprovar-operacao <id>`. Não executar nesta skill.

## Validação

- Nenhum alvo fora da conta confirmada.
- Nenhuma mudança implícita.
- Todo budget tem atual, proposto e impacto.
- Toda reversão usa valor conhecido.
- Itens bloqueados não entram como executáveis.

