---
name: 24-google-ads-performance-diagnosis
description: Analisa performance Google Ads por conta, campanha, grupo, keyword, termo, anúncio, asset, produto, conversão ou segmento. Use em /auditar-conta, /analisar-campanha, /otimizar-campanha, queda de resultado, desperdício ou oportunidade Google Ads.
---

# Diagnóstico de Performance Google Ads

## Leituras

1. `knowledge/google-ads/diagnostic-framework.md`.
2. `knowledge/methodology/windows-and-comparisons.md`.
3. `knowledge/methodology/diagnostic-coverage-contract.md`.
4. Trilha de negócio e gate da skill `03`.
5. `quality/analysis-checklist.md`.
6. Quando uma hipótese ou ação depender de entender um mecanismo específico do Google Ads que os arquivos acima não cobrem (ex: como um tipo de campanha, estratégia de lance, correspondência ou elegibilidade funciona), consultar `skills/17-google-ads-official-retrieval/SKILL.md` — não assumir funcionamento de memória.

## Fontes

- MCP oficial: consultas GAQL e metadata somente leitura.
- Arquivos: exports com escopo, período, timezone e colunas definidas.
- Contexto manual: somente hipóteses e orientação de coleta.

## Processo

1. Usar `depth_mode=full` por padrão. Usar `focused` somente quando o gestor restringir explicitamente o escopo e registrar o foco.
2. Confirmar customer, moeda, timezone, tipo, janela, comparação, atribuição e modo de fonte.
3. Registrar mudanças e eventos que afetam comparabilidade.
4. Montar a matriz de cobertura antes de concluir. Cobrir conta, campanha, grupo, anúncio/asset, conversão, dispositivo, geografia, tempo, mensuração, negócio, mudanças e budget/rank; acrescentar as camadas específicas do tipo de campanha definidas no contrato de cobertura.
5. Produzir o pacote de evidências comparativas com IDs, unidades, denominadores, variações e cobertura de investimento/conversões.
6. Decompor demanda/entrega → resposta → conversão → qualidade/receita e aprofundar entidades materiais e outliers.
7. Para Search, separar perda por budget de perda por ranking; revisar grupos, keywords, termos, negativas, anúncios/assets e rede na mesma rodada.
8. Para campanhas automatizadas, separar controles fornecidos, sinais e resultados observáveis sem inventar causalidade interna.
9. Cruzar dados comerciais sem forçar igualdade.
10. Consultar `change_event` quando disponível para testar hipóteses de queda.
11. Para mecanismos específicos da plataforma, consultar a skill `17` antes de registrar o achado; citar título e URL da fonte usada.
12. Priorizar por impacto, confiança, esforço e reversibilidade.

## Saída

Entregar no chat, antes de criar qualquer dossiê: veredito, matriz de cobertura, tabela de KPIs, pacote de evidências, diagnóstico e plano de ação. Cada achado referencia `evidence_ids`; cada ação referencia `finding_ids` e informa alvo, baseline, resultado esperado, prioridade, confiança, responsável, prazo, janela, sucesso, parada, dependências e risco. Campo sem evidência fica explicitamente indisponível. Optimization Score e recomendações do Google ficam separados e nunca são aceitos automaticamente.

Uma camada aplicável ausente bloqueia o rótulo de diagnóstico completo. Análise pura só cria dossiê `analysis_only` após aprovação editorial. Otimização segue para a skill `12` no chat; itens Google Ads permanecem `manual_only`.
