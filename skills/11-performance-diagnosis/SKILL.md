---
name: 11-performance-diagnosis
description: Analisa performance Meta Ads por conta, campanha, conjunto, anúncio ou criativo. Use somente no ramo Meta de /auditar-conta, /analisar-campanha, /otimizar-campanha ou queda de resultado.
---

# Diagnóstico de Performance Meta Ads

## Leituras

1. `knowledge/methodology/diagnostic-framework.md`.
2. `knowledge/methodology/windows-and-comparisons.md`.
3. `knowledge/methodology/diagnostic-coverage-contract.md`.
4. Trilha de negócio e gate da skill `03`.
5. `quality/analysis-checklist.md`.
6. Quando uma hipótese ou ação depender de entender um mecanismo específico do Meta Ads que os arquivos acima não cobrem (ex: como um recurso, orçamento, lance ou elegibilidade funciona), consultar `skills/15-meta-help-center-retrieval/SKILL.md` — não assumir funcionamento de memória.

## Processo

1. Usar `depth_mode=full` por padrão. Usar `focused` somente quando o gestor restringir explicitamente o escopo e registrar o foco.
2. Confirmar escopo, conta, moeda, timezone, janela, comparação e atribuição.
3. Registrar mudanças e eventos que afetam comparabilidade.
4. Montar a matriz de cobertura Meta antes de concluir: conta, campanha, conjunto, anúncio/criativo, placement/dispositivo, público/geografia/demografia, conversão, mensuração, negócio e mudanças. Toda camada deve ficar `analyzed`, `unavailable`, `insufficient` ou `not_applicable`.
5. Produzir o pacote de evidências comparativas com IDs, unidades, denominadores, variações e cobertura de investimento/conversões.
6. Decompor entrega → resposta → conversão → qualidade/receita e aprofundar entidades materiais e outliers.
7. Cruzar Meta e fonte comercial; preservar divergências.
8. Formular diagnósticos alternativos e a evidência que os distingue.
9. Para cada hipótese ou ação recomendada que dependa de um mecanismo específico da plataforma, consultar a skill `15` antes de registrar o achado; citar título e URL da fonte usada.
10. Priorizar por impacto, confiança, esforço e reversibilidade.

## Saída

Entregar no chat, antes de criar qualquer dossiê: veredito, matriz de cobertura, tabela de KPIs, pacote de evidências, diagnóstico e plano de ação. Para cada achado, registrar `finding_id` e `evidence_ids`; para cada ação, `action_id` e `finding_ids`, alvo, baseline, resultado esperado, prioridade, confiança, responsável, prazo, janela, sucesso, parada, dependências e risco. Campo sem evidência fica explicitamente indisponível. Separar:

- Problema de entrega.
- Problema de resposta/criativo.
- Problema de conversão.
- Problema de qualidade/receita.
- Problema de mensuração.

Uma camada aplicável ausente bloqueia o rótulo de diagnóstico completo. Iterar no chat e solicitar aprovação editorial da versão final. Somente após essa aprovação criar o dossiê como `analysis_only`; nenhuma mutação é gerada em análise pura.
