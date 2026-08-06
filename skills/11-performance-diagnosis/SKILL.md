---
name: 11-performance-diagnosis
description: Analisa performance Meta Ads por conta, campanha, conjunto, anúncio ou criativo. Use somente no ramo Meta de /auditar-conta, /analisar-campanha, /otimizar-campanha ou queda de resultado.
---

# Diagnóstico de Performance Meta Ads

## Leituras

1. `knowledge/methodology/diagnostic-framework.md`.
2. `knowledge/methodology/windows-and-comparisons.md`.
3. Trilha de negócio e gate da skill `03`.
4. `quality/analysis-checklist.md`.

## Processo

1. Confirmar escopo, conta, moeda, timezone, janela, comparação e atribuição.
2. Registrar mudanças e eventos que afetam comparabilidade.
3. Decompor entrega → resposta → conversão → qualidade/receita.
4. Analisar nos níveis necessários sem misturar denominadores.
5. Cruzar Meta e fonte comercial; preservar divergências.
6. Formular diagnósticos alternativos e evidência que os distingue.
7. Priorizar por impacto, confiança, esforço e reversibilidade.

## Saída

Para cada achado, registrar: `finding_id`, marcador `[F/C/H/R/I]`, plataforma, nível, evidência, impacto, confiança, limitação, hipótese principal, hipótese alternativa, verificação que distingue as hipóteses, ação exata, prioridade, responsável, prazo, janela de avaliação e critérios de sucesso e parada. Campo sem evidência deve ficar explicitamente `indisponível`, nunca omitido. Separar:

- Problema de entrega.
- Problema de resposta/criativo.
- Problema de conversão.
- Problema de qualidade/receita.
- Problema de mensuração.

Se a solicitação for apenas analítica, finalizar o dossiê como `analysis_only` depois da revisão, sem gerar mutação.
