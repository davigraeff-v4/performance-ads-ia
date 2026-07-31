---
name: 03-measurement-data-quality
description: Audita a confiabilidade de Pixel, CAPI, eventos, deduplicação, UTMs, atribuição e dados comerciais. Use em auditorias, antes de definir metas, quando Meta e CRM divergem ou quando uma decisão depende de conversão e receita.
---

# Qualidade de Mensuração

## Leituras

1. `knowledge/measurement/measurement-quality.md`.
2. `knowledge/official-meta/measurement-and-capi.md`.
3. Ficha do cliente, dossiê e fontes externas.

## Processo

1. Inventariar fonte, evento, conversão, timezone, janela e atribuição.
2. Verificar disponibilidade de Pixel/dataset, CAPI, browser/server, event ID e sinais de duplicidade.
3. Conferir evento de otimização versus resultado comercial desejado.
4. Conferir UTMs e chave de reconciliação.
5. Comparar Meta e dados externos sem forçar igualdade.
6. Explicar diferenças plausíveis: atribuição, atraso, timezone, cancelamento, duplicidade, definição ou escopo.

## Classificação

- `confiavel`: suficiente para a decisão declarada.
- `utilizavel_com_ressalvas`: permite leitura parcial com limitação explícita.
- `insuficiente`: não sustenta a decisão; bloquear mutação dependente.

## Saída

Registrar sinais verificados, lacunas, divergências, impacto analítico, correções propostas e gate. Não declarar tracking "correto" sem evidência observada.

