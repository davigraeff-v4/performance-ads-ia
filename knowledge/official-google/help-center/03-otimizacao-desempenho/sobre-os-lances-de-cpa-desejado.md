---
title: "Sobre os lances de CPA desejado"
url: "https://support.google.com/google-ads/answer/6268632?hl=pt-BR"
answer_id: "6268632"
categoria: "03-otimizacao-desempenho"
topico: "Lances"
subtopico: "CPA desejado"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Sobre os lances de CPA desejado

> **Nomenclatura**: a partir de jun/2026, "Maximizar Conversões com CPA desejado" passa a se chamar apenas "CPA desejado" — o comportamento de lances não muda.

Estratégia de lances automática que define lances para gerar o máximo de conversões possível a um custo médio por ação (CPA) definido pelo anunciante. Em campanhas para apps, o CPA desejado equivale ao custo por instalação ou custo por ação no app. Disponível como estratégia padrão (campanha única) ou de portfólio (várias campanhas).

## Pré-requisitos

- Configurar acompanhamento de conversões antes de ativar.
- Revisar configurações de orçamento: é possível gastar até o dobro do orçamento diário médio em um dia sem exceder o limite de cobrança mensal.

## Como funciona

O Google Ads identifica automaticamente um lance ideal a cada leilão qualificado, usando dados históricos da campanha e indicadores de contexto em tempo real (dispositivo, navegador, local, horário, listas de remarketing). Pode ser ativado sem histórico de conversões e funciona para campanhas de qualquer porte.

Algumas conversões custam mais que o CPA desejado, outras menos — o sistema busca manter a média igual ao valor definido. O CPA real varia por fatores fora do controle do Google (mudanças no site/anúncios, concorrência no leilão, variação na taxa de conversão real vs. estimada).

**Exemplo**: CPA desejado de US$ 10 → o sistema tenta gerar o máximo de conversões a uma média de US$ 10, dentro do orçamento.

> **Aviso**: a partir de 17/08/2026, mudanças nos sistemas de lances para campanhas limitadas por orçamento (usando CPA/ROAS desejado) podem causar flutuações temporárias — ferramenta de ajuste de meta de lances disponível a partir de 06/07/2026.

## Configurações principais

- **Metas de grupos de anúncios**: aplicáveis a estratégias padrão e de portfólio, mas não recomendadas — podem limitar a eficácia dos Lances Inteligentes. Em Geração de Demanda, limites de CPA desejado por grupo de anúncios substituem o limite da campanha.
- **CPA desejado**: valor médio que se deseja pagar por conversão. Um valor muito baixo pode reduzir o volume total de conversões. Quando há histórico, o Google recomenda um CPA desejado baseado na média dos últimos 30 dias (ajustada por atraso de conversão); sem histórico, usa dados de simulação. Avaliar performance com pelo menos 30 conversões nos últimos 30 dias.
- **Incluir em "Conversões"**: controla quais ações de conversão alimentam a otimização de CPA desejado, ROAS desejado e ECPC.
- **CPA desejado médio**: métrica que reflete o CPA médio real que a estratégia mirou (inclui ajustes por dispositivo, por grupo de anúncios e mudanças ao longo do tempo) — comparar com esse valor, não com o CPA desejado definido, para avaliar performance.
- **Limites de lance**: não recomendados (restringem a otimização automática); disponíveis apenas para estratégias de portfólio de CPA desejado, válidos só na rede de pesquisa. O CPC máx. real pode ficar abaixo do limite mínimo definido.
- **Ajustes de lance por dispositivo**: modificam o valor do CPA desejado (não o lance em si) — ex.: CPA desejado de R$ 10 + ajuste de +40% para mobile = CPA desejado de R$ 14 em mobile. Ajuste de -100% impede exibição no dispositivo. Recomenda-se remover ajustes de CPC manual ao migrar para CPA desejado. Ajustes que não são por dispositivo são ignorados em Pesquisa e Display.
- **Pagamento por conversões** (só Display): alternativa ao pagamento por clique/visualização engajada, configurável em Lances → "Pagar por" → "Conversões".

## Onde encontrar as métricas

- Coluna "CPA méd. desejado" (ou "Custo méd. desejado por instalação/ação no app") na tabela de performance da página "Campanhas" ou no gráfico de performance.
- Relatório de estratégia de lances, ao lado do "CPA real" alcançado.
- Recomenda-se medir períodos com pelo menos 30 conversões para maior precisão.

## Links relacionados

- [Sobre os lances de ROAS desejado](https://support.google.com/google-ads/answer/6268637?hl=pt-BR)
- [Sobre os lances automáticos](https://support.google.com/google-ads/answer/2979071?hl=pt-BR)
