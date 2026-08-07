---
title: "Sobre os segmentos de público-alvo do Gerenciador de públicos-alvo"
url: "https://support.google.com/google-ads/answer/7558048?hl=pt-BR"
answer_id: "7558048"
categoria: "02-recursos"
topico: "Segmentação"
subtopico: "Públicos-alvo"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Sobre os segmentos de público-alvo do Gerenciador de públicos-alvo

O Google Ads consolidou a visão de públicos-alvo com um novo relatório de público-alvo (acessível em Campanhas → Públicos-alvo), que reúne informações demográficas, segmentos e exclusões, além de permitir gerenciar os públicos diretamente ali. A nomenclatura também mudou: "tipos de públicos-alvo" (personalizados, no mercado, de afinidade) agora se chamam "segmentos de público-alvo", e "remarketing" agora é "seus dados".

O Gerenciador de públicos-alvo tem uma seção "Segmentos de público-alvo" para criar e gerenciar segmentos dos dados do anunciante. Com campanhas de dados do site, é possível controlar quais segmentos veem os anúncios no YouTube, Gmail, Pesquisa Google e Rede de Display, depois de configurar uma origem de público-alvo.

## Vantagens

- Ver todos os segmentos de dados em um só lugar.
- Ver tipo, status e tamanho (alcance) de cada segmento em cada rede ativa.
- Adicionar rapidamente segmentos a grupos de anúncios e campanhas.
- Ajustar onde e para quem os anúncios são exibidos, otimizando a exposição.
- Aplicar rótulos aos segmentos para filtrar e gerar relatórios.

## Como funciona

Quando a tag do Google é adicionada ao site/app, ela coleta dados e inclui pessoas nos segmentos relevantes conforme o critério definido. Exemplo: uma lanchonete pode criar o segmento "Clientes do almoço" com quem acessa o site no horário do almoço, e usá-lo em uma campanha "Promoção de almoço" para aumentar pedidos.

### Como acessar

Ícone de ferramentas → menu "Biblioteca compartilhada" → "Gerenciador de públicos-alvo" (abre por padrão a página "Segmentos dos seus dados").

## Como os dados são organizados

A tabela de segmentos de público-alvo mostra até **50 segmentos por vez**, com colunas:

| Coluna | O que mostra |
|---|---|
| Tipo | Quem está incluído e como o segmento foi criado |
| Status da associação | Se o segmento ainda está adicionando usuários |
| Tamanho | Quantas pessoas podem ser alcançadas em cada rede (pesquisa, YouTube, Display, Gmail) |
| Rótulos | Organização/filtragem de segmentos, palavras-chave, anúncios, grupos e campanhas |

A tabela pode ser ordenada por qualquer coluna. Selecionar segmentos abre uma barra de ferramentas para adicioná-los a grupo de anúncios/campanha, editar ou rotular; é possível adicionar colunas opcionais.

## Requisitos mínimos de tamanho do segmento

| Rede | Requisito mínimo |
|---|---|
| Rede de Display do Google | 100 visitantes/usuários ativos nos últimos 30 dias |
| Rede de Pesquisa do Google | 100 visitantes/usuários ativos nos últimos 30 dias (listas de clientes têm a mesma exigência) |
| YouTube | 100 visitantes/usuários ativos nos últimos 30 dias (listas de clientes têm a mesma exigência) |

**Observação sobre listas de clientes**: o requisito de 100 usuários ativos vale para listas enviadas/atualizadas **após 1º de fevereiro de 2024**. Listas enviadas antes dessa data ainda seguem o requisito anterior de mínimo de **1.000 usuários correspondentes**.

"Usuários ativos" (ou "Usuários") é o número de pessoas que interagiram com o site/app e é diferente do total do Google Analytics/Firebase — o Google Ads considera apenas interações recentes com anúncios e Serviços do Google. Para comparar com o GA4, usar o segmento "Publicidade" do GA4, que reflete os usuários qualificados para remarketing do Google Ads.

## Resolver discrepâncias no tamanho e preenchimento

- **Indicadores do Google**: precisam estar ativados no Google Analytics para o público ser preenchido corretamente no Google Ads.
- **Cookies**: verificar se cookies necessários (SNID, NID, ID, IDE) estão implementados corretamente.
- **Tempo de preenchimento**: uma lista recém-criada pode levar de **48 a 72 horas** para ser totalmente preenchida.
- **Limites mínimos de usuários ativos**: se não atingidos, os anúncios não são veiculados para a lista.

## Tipos de segmento de dados

- **Visitantes do site**: tipo padrão para campanhas baseadas em site; acompanha comportamento via critérios definidos pelo anunciante ou gerados automaticamente (visitas, origem do clique, destino do clique, etapas de conversão). Alguns segmentos são criados automaticamente, como "Todos os visitantes" e "Todos os conversores".
- **Segmentos de clientes**: baseados na Segmentação por lista de clientes — upload de dados de contato (e-mail, CEP) para alcançar clientes nos Serviços do Google. Se "Ativar listas com base em conversões" estiver marcado, o Google gera automaticamente listas por meta de conversão (ex.: compras), atualizadas em tempo real com dados hash conforme novas conversões.
- **Usuários do YouTube**: usuários que veem/interagem com anúncios em vídeo; exige vincular o canal do YouTube à conta do Google Ads.
- **Usuários do aplicativo**: usuários que instalaram o app, qualificados para ver anúncios em outros apps da Rede de Display.
- **Combinação personalizada**: criado ao combinar manualmente dois ou mais segmentos de dados (ex.: compradores de alto valor + compradores de eletrônicos).
- **Autores de chamadas**: monitora quem já ligou para a empresa; gerado automaticamente (não é possível adicionar/remover membros manualmente), aparece como segmento de visitantes do site. Pode ser usado para remarketing ou exclusão de leads já convertidos.

## O que é possível fazer com os segmentos

- **Criar**: manualmente (ícone de adição) ou automaticamente pelo Google Ads a partir das origens de público-alvo.
- **Adicionar a**: grupos de anúncios (um ou mais) ou campanhas (uma ou mais).
- **Remover**: o segmento recebe o rótulo "Removido" e some da tabela principal enquanto mantiver esse rótulo.
- **Pausar**: suspende o segmento do grupo de anúncios/campanha associada, mas ele continua adicionando usuários.
- **Rotular**: usando rótulos padrão do Google Ads ou rótulos próprios.

## Por que melhorar os segmentos

É necessário ter no mínimo 100 visitantes/usuários ativos nos últimos 30 dias (Display e Pesquisa; listas de clientes seguem a mesma regra) para que os anúncios sejam veiculados. Segmentos com pelo menos 100 usuários também passam a aparecer nos insights sobre público-alvo, ajudando a identificar novos públicos.

## Links relacionados

- [Sobre o Gerenciador de públicos-alvo](https://support.google.com/google-ads/answer/7538811)
- [Usar modelos de segmentos de dados do site](https://support.google.com/google-ads/answer/6297549)
- [Como corrigir problemas com anúncios, tags e segmentos de dados do Google Ads](https://support.google.com/google-ads/answer/2472738)
- [Sobre a compatibilidade do segmento dos seus dados](https://support.google.com/google-ads/answer/7476585)
- [Saiba mais sobre a Segmentação por lista de clientes](https://support.google.com/google-ads/answer/6379332)
- [Sobre a combinação personalizada](https://support.google.com/google-ads/answer/2549111)
