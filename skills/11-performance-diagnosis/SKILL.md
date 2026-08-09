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
5. Quando uma hipótese ou ação depender de entender um mecanismo específico do Meta Ads que os arquivos acima não cobrem (ex: como um recurso, orçamento, lance ou elegibilidade funciona), consultar `skills/15-meta-help-center-retrieval/SKILL.md` — não assumir funcionamento de memória.

## Processo

1. Confirmar escopo, conta, moeda, timezone, janela, comparação e atribuição.
2. Registrar mudanças e eventos que afetam comparabilidade.
3. Decompor entrega → resposta → conversão → qualidade/receita.
4. Analisar nos níveis necessários sem misturar denominadores.
5. Cruzar Meta e fonte comercial; preservar divergências.
6. Formular diagnósticos alternativos e evidência que os distingue.
7. Para cada hipótese ou ação recomendada que dependa de um mecanismo específico da plataforma (não de dado da conta), consultar a skill `15` (busca híbrida sobre a Central de Ajuda) antes de registrar o achado; citar título e URL da fonte usada no achado.
8. Priorizar por impacto, confiança, esforço e reversibilidade.

## Saída

Para cada achado, registrar: `finding_id`, marcador `[F/C/H/R/I]`, plataforma, nível, evidência, impacto, confiança, limitação, hipótese principal, hipótese alternativa, verificação que distingue as hipóteses, ação exata, prioridade, responsável, prazo, janela de avaliação e critérios de sucesso e parada. Campo sem evidência deve ficar explicitamente `indisponível`, nunca omitido. Separar:

- Problema de entrega.
- Problema de resposta/criativo.
- Problema de conversão.
- Problema de qualidade/receita.
- Problema de mensuração.

Se a solicitação for apenas analítica, finalizar o dossiê como `analysis_only` depois da revisão, sem gerar mutação.
