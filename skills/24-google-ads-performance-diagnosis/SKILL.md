---
name: 24-google-ads-performance-diagnosis
description: Analisa performance Google Ads por conta, campanha, grupo, keyword, termo, anúncio, asset, produto, conversão ou segmento. Use em /auditar-conta, /analisar-campanha, /otimizar-campanha, queda de resultado, desperdício ou oportunidade Google Ads.
---

# Diagnóstico de Performance Google Ads

## Leituras

1. `knowledge/google-ads/diagnostic-framework.md`.
2. `knowledge/methodology/windows-and-comparisons.md`.
3. Trilha de negócio e gate da skill `03`.
4. `quality/analysis-checklist.md`.

## Fontes

- MCP oficial: consultas GAQL e metadata somente leitura.
- Arquivos: exports com escopo, período, timezone e colunas definidas.
- Contexto manual: somente hipóteses e orientação de coleta.

## Processo

1. Confirmar customer, moeda, timezone, tipo, janela, comparação, atribuição e modo de fonte.
2. Registrar mudanças e eventos que afetam comparabilidade.
3. Decompor demanda/entrega → resposta → conversão → qualidade/receita.
4. Analisar campanhas, grupos, termos/keywords, ads/assets, conversões, dispositivos, rede, geografia e tempo somente quando relevantes.
5. Para Search, separar perda de impressão por budget de perda por ranking; revisar termos e negativas.
6. Para campanhas automatizadas, separar controles fornecidos, sinais e resultados observáveis sem inventar causalidade interna.
7. Cruzar dados comerciais sem forçar igualdade.
8. Consultar `change_event` quando disponível para testar hipóteses de queda.
9. Priorizar por impacto, confiança, esforço e reversibilidade.

## Saída

Para cada achado: `[F/C/H/R/I]`, plataforma, nível, evidência, impacto, confiança, limitação e próxima ação. Optimization Score e recomendações do Google ficam em bloco separado e nunca são aceitos automaticamente.

Análise pura termina `analysis_only`. Otimização segue para a skill `12` com itens Google Ads `manual_only`.
