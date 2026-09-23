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
6. `knowledge/platform-quirks/meta-ads-mcp.md` antes de ler entidades pelo conector (paginação, status).
7. `templates/resposta-chat.md` para a forma da entrega.

## Processo

1. Usar a profundidade devolvida pela rota: `full` em auditoria ou quando o gestor pedir análise completa; `focused` nos demais casos, com o foco declarado.
2. Confirmar escopo, conta, moeda, timezone, janela, comparação e atribuição.
3. Registrar mudanças e eventos que afetam comparabilidade.
4. Em `full`, cobrir todas as camadas Meta (conta, campanha, conjunto, anúncio/criativo, posicionamento/dispositivo, público/geografia/demografia, conversão, mensuração, negócio e mudanças) e registrar para cada uma se foi analisada, ficou indisponível, insuficiente ou não se aplica.
5. Reunir as evidências comparativas: unidade, definição, denominador, valores, variações e quanto do investimento e das conversões cada leitura cobre. Para status de entidades, ler por IDs; nunca inferir pausa pela ausência numa listagem paginada.
6. Decompor entrega → resposta → conversão → qualidade/receita e aprofundar entidades materiais e outliers.
7. Cruzar Meta e fonte comercial; preservar divergências.
8. Formular diagnósticos alternativos e a evidência que os distingue.
9. Listar as premissas de mecanismo de cada achado e ação (ex.: "conjuntos sobrepostos competem no leilão") e conferir cada uma pela skill `15` e por `ads_get_help_article`, antes de apresentar. Premissa contradita pela fonte muda o texto e o plano; registrar a checagem com fonte.
10. Priorizar por impacto, confiança, esforço e reversibilidade.

## Saída

Entregar no chat, antes de qualquer dossiê, no formato de `templates/resposta-chat.md`: resumo, números com a leitura de cada um, achados (o que vimos, por que acreditamos, outra explicação possível, confiança), plano de ação com alvo, antes e depois, resultado esperado, janela, sucesso e parada, e a checagem com boas práticas. Campo sem evidência fica explicitamente indisponível. Separar:

- Problema de entrega.
- Problema de resposta/criativo.
- Problema de conversão.
- Problema de qualidade/receita.
- Problema de mensuração.

Uma camada aplicável ausente bloqueia o rótulo de diagnóstico completo. Iterar no chat e pedir aprovação do conteúdo. Só depois registrar com `scripts/dossier.py new` (análise pura fica `analysis_only`); nenhuma mutação é gerada em análise pura.
