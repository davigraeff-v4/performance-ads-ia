<!-- Referência do módulo `diagnostico`; etapa `diagnostico/google-ads` nas rotas. -->

# Diagnóstico de Performance Google Ads

## Leituras

1. `knowledge/google-ads/diagnostic-framework.md`.
2. `knowledge/methodology/windows-and-comparisons.md`.
3. `knowledge/methodology/diagnostic-coverage-contract.md`.
4. Trilha de negócio e gate da etapa `mensuracao`.
5. `quality/analysis-checklist.md`.
6. Quando uma hipótese ou ação depender de entender um mecanismo específico do Google Ads que os arquivos acima não cobrem (ex: como um tipo de campanha, estratégia de lance, correspondência ou elegibilidade funciona), consultar `skills/revisor/references/google-ads.md` — não assumir funcionamento de memória.

## Fontes

- MCP oficial: consultas GAQL e metadata somente leitura.
- Arquivos: exports com escopo, período, timezone e colunas definidas.
- Contexto manual: somente hipóteses e orientação de coleta.

## Processo

1. Usar `depth_mode=full` por padrão. Usar `focused` somente quando o gestor restringir explicitamente o escopo e registrar o foco.
2. Confirmar customer, moeda, timezone, tipo, janela, comparação, atribuição e modo de fonte.
3. Registrar mudanças e eventos que afetam comparabilidade.
4. Em `full`, cobrir conta, campanha, grupo, anúncio/asset, conversão, dispositivo, geografia, tempo, mensuração, negócio, mudanças e budget/rank, mais as camadas do tipo de campanha do contrato de cobertura, registrando para cada uma se foi analisada, ficou indisponível, insuficiente ou não se aplica. Em `focused`, declarar o foco.
5. Reunir as evidências comparativas: unidade, definição, denominador, valores, variações e cobertura de investimento e conversões.
6. Decompor demanda/entrega → resposta → conversão → qualidade/receita e aprofundar entidades materiais e outliers.
7. Para Search, separar perda por budget de perda por ranking; revisar grupos, keywords, termos, negativas, anúncios/assets e rede na mesma rodada.
8. Para campanhas automatizadas, separar controles fornecidos, sinais e resultados observáveis sem inventar causalidade interna.
9. Cruzar dados comerciais sem forçar igualdade.
10. Consultar `change_event` quando disponível para testar hipóteses de queda; a API só expõe 30 dias (ver `knowledge/platform-quirks/google-ads-api.md`).
11. Listar as premissas de mecanismo de cada achado e ação (ex.: "duas campanhas com as mesmas palavras-chave competem no leilão") e conferir cada uma pela etapa `revisor/google-ads` (`python3 scripts/kb_check.py --platform google_ads "premissa 1" "premissa 2"`) antes de apresentar. Premissa contradita pela fonte muda o texto e o plano; registrar a checagem com fonte.
12. Priorizar por impacto, confiança, esforço e reversibilidade.

## Saída

Entregar no chat, antes de qualquer dossiê, no formato de `templates/resposta-chat.md`: resumo, números com a leitura de cada um, achados (o que vimos, por que acreditamos, outra explicação possível, confiança), plano de ação com alvo, antes e depois, resultado esperado, janela, sucesso e parada, e a checagem com boas práticas. Campo sem evidência fica explicitamente indisponível. Optimization Score e recomendações do Google ficam separados e nunca são aceitos automaticamente.

Uma camada aplicável ausente bloqueia o rótulo de diagnóstico completo. Análise pura é registrada como `analysis_only` por `scripts/dossier.py new` depois da aprovação do conteúdo. Otimização segue para a etapa `change-set` no chat; itens Google Ads permanecem `manual_only`.

## Modo avaliação (`avaliacao`, profundidade `quick`)

Quando a rota é de avaliação, o diagnóstico é curto e fechado na operação: ler só os alvos da operação e o que os cerca (a campanha e os conjuntos ou grupos vizinhos que podem ter absorvido o efeito), na janela depois da execução contra a linha de base registrada. Para cada critério de sucesso e de parada, dizer o número combinado, o número observado e a situação. Separar o efeito da mudança de outras mudanças no período, sazonalidade e atraso de conversão; se não der para separar, o resultado é `inconclusive`. As premissas da explicação passam pela etapa `revisor/google-ads` (`kb_check.py`).
