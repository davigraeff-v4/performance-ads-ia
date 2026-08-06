---
name: 12-optimization-change-set
description: Transforma diagnóstico Meta Ads ou Google Ads em lote versionado de otimizações com antes/depois, impacto, risco e reversão. Use em /otimizar-campanha ou quando recomendações virarem alterações aprováveis.
---

# Change Set de Otimização

## Pré-requisitos

1. Skill `11` para Meta Ads ou `24` para Google Ads, com diagnóstico e fontes. Em um build plan, `10` ou `23` pode originar o lote, mantendo a mesma evidência e os mesmos gates. Em reversão, o dossiê executado e o snapshot anterior substituem o diagnóstico somente para restaurar valores conhecidos.
2. Dossiê atual com uma única plataforma de mutação.
3. Estado atual dos alvos.

## Processo

1. Selecionar somente recomendações que sustentem ação.
2. Ordenar dependências e separar itens independentes.
3. Para cada item, registrar `finding_ids`, alvo, campo, antes, depois, justificativa, evidência, impacto esperado, impacto financeiro quando aplicável, confiança, risco, reversão, precondições, dependências, ordem, responsável, janela de avaliação e critérios de sucesso e parada.
4. Quantificar impacto financeiro quando houver budget.
5. Marcar ações não suportadas como `manual_only`; enquanto o conector Google Ads não registrar escrita homologada, todas as mudanças Google Ads usam esse modo.
6. Proibir itens de exclusão/arquivamento.
7. Calcular versão/hash conforme contrato.
8. Mudar dossiê para `proposed`.

## Checkpoint

Apresentar lote completo e perguntar se o gestor aprova exatamente aquela versão. Orientar `/aprovar-operacao <id>`. Não executar nesta skill.

## Validação

- Nenhum alvo fora da plataforma e conta confirmadas.
- Nenhuma mudança implícita.
- Todo budget tem atual, proposto e impacto.
- Toda reversão usa valor conhecido.
- Todo item aponta para achado/evidência e possui responsável, janela e critérios verificáveis.
- Itens bloqueados não entram como executáveis.
