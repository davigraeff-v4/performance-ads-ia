---
title: "Sobre os lances de ROAS desejado"
url: "https://support.google.com/google-ads/answer/6268637?hl=pt-BR"
answer_id: "6268637"
categoria: "03-otimizacao-desempenho"
topico: "Lances"
subtopico: "ROAS desejado"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Sobre os lances de ROAS desejado

> **Nomenclatura**: a partir de jun/2026, "Maximizar o Valor da Conversão com ROAS desejado" passa a se chamar apenas "ROAS desejado" — o comportamento de lances não muda.

Estratégia de Lances Inteligentes que usa IA para prever o valor de uma conversão em potencial a cada pesquisa do usuário e ajustar lances para maximizar o retorno. Pesquisas com alta probabilidade de conversão de valor recebem lances mais altos; pesquisas com baixa probabilidade recebem lances mais baixos. Disponível como estratégia padrão (campanha única) ou de portfólio (múltiplas campanhas) — **exceto** para campanhas Performance Max, de hotel e de viagens, onde a estratégia de portfólio não está disponível.

## Pré-requisitos

- Definir valores para as conversões acompanhadas (é possível usar regras de valor da conversão para multiplicar valores por tipo de cliente, dispositivo ou local).
- Volume mínimo de conversões nos últimos 30 dias (varia por tipo de campanha):
  - Pesquisa e Shopping: 15 conversões.
  - Display: 15 conversões com valor válido (campanhas novas de display não precisam de histórico).
  - Apps: 10 conversões/dia ou 300 em 30 dias.
  - Geração de Demanda: 50 conversões em 35 dias (10 nos últimos 7 dias) OU 100 conversões em 35 dias somando todas as campanhas de Geração de Demanda da conta.
  - Ação em vídeo: 30 conversões em 30 dias.
  - Hotel: 50 conversões/semana.
  - Viagens: 50 conversões em 7 dias.
- Valor de conversão deve ser maior que 0.
- Para campanhas para apps, o SDK do Google Analytics para Firebase precisa estar instalado, com eventos de conversão vindos do Firebase.
- Se o valor de conversão for novo ou tiver mudado, aguardar 4 semanas ou 3 ciclos de conversão antes de ativar.
- Recomenda-se rodar CPA desejado antes de ROAS desejado para ter uma referência de retorno ao definir a meta inicial.
- Orçamento: revisar se comporta gastar até o dobro da média diária (o teto do ciclo de faturamento mensal continua sendo o orçamento diário médio × 30,4 dias).

## Como funciona

O Google Ads estima conversões futuras e valores associados a partir dos dados de rastreamento de conversão, define lances máximos de CPC para maximizar o valor de conversão e buscar o ROAS médio desejado, usando indicadores em tempo real (dispositivo, navegador, local, hora do dia) e listas de remarketing. Campanhas de hotel só aceitam CPC manual, porcentagem do CPC e ROAS desejado, com rastreamento de conversão obrigatório.

**Exemplo de cálculo**: meta de R$ 5 em vendas por R$ 1 investido → ROAS desejado = (5 ÷ 1) × 100% = 500%.

## Quando usar lances com base em valor

Mais úteis quando conversões têm valores diferentes para o negócio ou há uma meta específica de ROAS.

| | Max. conversões | CPA desejado | Max. valor da conversão | ROAS desejado |
|---|---|---|---|---|
| Meta | Máximo de conversões dentro do orçamento | Conversões com meta de ROI | Máximo de valor de conversão dentro do orçamento | Valor de conversão com meta de ROI |
| Quando usar | Sem meta de ROI; conversões tratadas igualmente | Meta de ROI específica; conversões tratadas igualmente | Sem meta de ROI; conversões têm valores diferentes | Meta de ROI específica; conversões têm valores diferentes |

## Ajustes de lance

Como o ROAS desejado otimiza com dados em tempo real, ajustes de lance manuais **não são usados** — exceção: ajuste de lance por dispositivo de -100% continua válido. Não é necessário remover os ajustes existentes.

## Configuração do ROAS desejado

- Definir com base em metas de negócio e no ROAS histórico real (coluna "Valor conv./custo" × 100).
- Excluir da avaliação o intervalo mais recente de tempo até a conversão para não distorcer a leitura.
- Sugestões de meta disponíveis em Recomendações, Simulador de lances, ou ao criar a estratégia.
- **Limites de lance** não são recomendados (atrapalham a otimização por IA); quando definidos, valem só para leilões de rede de pesquisa e apenas em estratégias de portfólio de Pesquisa/Shopping. O CPC máximo real pode ficar abaixo do limite mínimo definido.
- Configuração "Incluir em Conversões" controla quais ações de conversão alimentam a otimização de CPA/ROAS desejado/ECPC.
- Metas por grupo de anúncios são possíveis mas não recomendadas — limitam a eficácia dos Lances Inteligentes; estratégias de portfólio tendem a performar melhor.

## Aviso de mudança nos sistemas de lances (17/08/2026)

O Google vai atualizar os sistemas de lances para campanhas limitadas por orçamento usando CPA/ROAS desejado, podendo causar flutuações temporárias. Uma ferramenta de ajuste de meta de lances estará disponível a partir de 06/07/2026 para preparação.

## Links relacionados

- [Sobre os Lances inteligentes](https://support.google.com/google-ads/answer/7065882?hl=pt-BR)
- [Sobre os lances de CPA desejado](https://support.google.com/google-ads/answer/6268632?hl=pt-BR)
