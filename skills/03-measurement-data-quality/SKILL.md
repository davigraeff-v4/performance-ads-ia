---
name: 03-measurement-data-quality
description: Audita a confiabilidade de mensuração Meta Ads ou Google Ads, eventos/conversões, Pixel/CAPI/tags/imports, UTMs, atribuição e dados comerciais. Use antes de metas ou quando plataforma e CRM divergem.
---

# Qualidade de Mensuração

## Leituras

1. `knowledge/measurement/measurement-quality.md`.
2. Para Meta: `knowledge/official-meta/measurement-and-capi.md`.
3. Para Google Ads: `knowledge/official-google/conversions-bidding-and-budget.md`.
4. Ficha do cliente, dossiê e fontes externas.

## Processo

1. Inventariar fonte, evento, conversão, timezone, janela e atribuição.
2. Verificar o mecanismo da plataforma: Pixel/dataset/CAPI no Meta; tag, imports e ações de conversão no Google Ads.
3. Conferir evento de otimização versus resultado comercial desejado.
4. Conferir UTMs e chave de reconciliação.
5. Comparar cada plataforma e dados externos sem forçar igualdade.
6. Explicar diferenças plausíveis: atribuição, atraso, timezone, cancelamento, duplicidade, definição ou escopo.

## Classificação

- `confiavel`: suficiente para a decisão declarada.
- `utilizavel_com_ressalvas`: permite leitura parcial com limitação explícita.
- `insuficiente`: não sustenta a decisão; bloquear mutação dependente.

## Saída

Registrar sinais verificados, lacunas, divergências, impacto analítico, correções propostas e gate. Não declarar tracking "correto" sem evidência observada.
