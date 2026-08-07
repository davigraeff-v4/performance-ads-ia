---
title: "Como o Google Ads acompanha conversões no site"
url: "https://support.google.com/google-ads/answer/7521212?hl=pt-BR"
answer_id: "7521212"
categoria: "02-recursos"
topico: "Medir resultados"
subtopico: "Conversões no site"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Como o Google Ads acompanha conversões no site

## Mecanismo básico

Quando alguém interage com um anúncio (clica em um anúncio de texto ou visualiza um anúncio em vídeo), o Google Ads armazena cookies contendo dados da interação e um identificador exclusivo do usuário ou do clique que levou a pessoa ao site. Se essa pessoa converter no site, a tag de acompanhamento instalada lê o cookie e o envia de volta ao Google Ads junto com os dados da conversão.

Em alguns casos (por exemplo, configurações de navegador), os cookies com detalhes da interação não ficam disponíveis. Para esses casos, o Google Ads oferece métodos alternativos de acompanhamento mais preciso.

## Antes de começar (pré-requisitos para máxima precisão)

- Ativar a codificação automática em todas as contas do Google Ads.
- Se usar rastreadores de cliques em URLs de rastreamento ou redirecionamentos do lado do servidor, garantir que transmitam o GCLID (identificador de clique do Google) para as páginas de destino.
- Se a página de conversão estiver em domínio diferente da página de destino, usar o vinculador de domínio da gtag.js para transmitir o GCLID.
- Não acionar as tags a partir de um iframe (por exemplo, dentro de outra tag de acompanhamento como o Floodlight).

## Opções de acompanhamento (tag em todo o site)

Todas as opções abaixo implementam uma tag em todo o site que define novos cookies no domínio, armazenando o identificador do usuário/clique.

### Opção 1 — Tag de acompanhamento atualizada do Google Ads (tag do Google)
A tag do Google (composta por snippet de evento + tag do Google) define os novos cookies usando o parâmetro GCLID incluído na tag de acompanhamento. É a opção recomendada para garantir avaliação de todas as conversões independentemente do navegador. Os snippets de código são fornecidos ao configurar o acompanhamento na nova experiência do Google Ads.

**Como desativar** (não recomendado — reduz a precisão): adicionar `{'conversion_linker': false}` ao comando `config` da tag: `gtag('config', 'TAG_ID', {'conversion_linker': false});`

### Opção 2 — Gerenciador de tags do Google com a tag do Vinculador de conversões
Passos:
1. Configurar e instalar o Gerenciador de tags do Google.
2. No contêiner, adicionar uma Nova tag.
3. Em Configuração da tag, selecionar o tipo "Vinculador de conversões".
4. Em Acionamento, selecionar um acionador que dispare a tag em Todas as páginas.

A tag do Vinculador de conversões detecta as informações do clique no anúncio nos URLs das páginas de destino e as armazena nos novos cookies do domínio.

### Opção 3 — Google Analytics (apenas Universal Analytics)
Se a tag do Google Analytics já estiver instalada, o GCLID do clique fica armazenado em um cookie do Analytics no domínio do site, desde que:
- o código JavaScript da tag de acompanhamento de conversões não seja removido manualmente (evitar implementação "apenas pixel");
- a propriedade ativa do Analytics esteja vinculada à conta do Google Ads que contém as ações de conversão no site.

Seguindo essas condições, o GCLID do cookie do Analytics é lido automaticamente pela tag de acompanhamento de conversões do Google Ads.

**Observação importante**: o Universal Analytics preserva o GCLID em cookie; a tag do **Google Analytics 4 não preserva mais o GCLID em cookie** para eventos de acompanhamento de conversões do Google Ads — para usar o GA4 nesse fluxo é necessário exportar as conversões para o Google Ads.

**Como desativar**: é possível atualizar a tag do Google Analytics para não armazenar o GCLID no cookie (reduz a precisão da medição).

## Acompanhamento em vários domínios

Quando a página de destino e a página de conversão estão em domínios diferentes, é preciso ativar o acompanhamento entre domínios, por exemplo:

```
gtag('set', 'linker', {
  'domains': ['landing-destination.com', 'conversion-destination.com']
});
```

## Diagnóstico

- Usar o Assistente de tags para verificar a implementação e depurar problemas.
- Se houver vários métodos de rastreamento simultâneos (ex.: gtag.js e GTM ao mesmo tempo), verificar conflitos e considerar consolidar em um único método — de preferência o GTM.
- Após correções, o status da tag pode levar até **48 horas** para ser atualizado no Google Ads.

## Quando o Google Ads não consegue acompanhar todas as conversões

Mesmo com as soluções implementadas, há casos que escapam ao rastreamento — por exemplo, um usuário sem login nos serviços do Google que vê um anúncio em vídeo no app do YouTube (mobile) e depois converte no navegador do smartphone. Nesses casos, o Google inclui **conversões estimadas** na coluna "Conversões" dos relatórios, geradas a partir de dados de usuários logados e com proteção de privacidade, para produzir um relatório mais completo.

## Impacto nos lances

Recomenda-se monitorar os relatórios de conversão nos meses seguintes e ajustar os lances conforme necessário:
- Em estratégias de Lances inteligentes (CPA desejado, ROAS desejado), se houver queda de tráfego aparente, ajustar as metas para compensar conversões não acompanhadas.
- Em lances manuais, considerar que parte das conversões pode não estar sendo contabilizada ao avaliar performance.

## Tag de remarketing legada

Como alternativa às opções acima, a tag de remarketing legada do Google Ads também pode definir cookies com informações de clique (via GCLID) no domínio, seguindo as mesmas instruções de "Antes de começar" e implantando a tag em todas as páginas do site.

**Como desativar**: adicionar `var google_conversion_linker = false;` antes de carregar a tag de script; para `conversion_async.js`, incluir `{ google_conversion_linker : false }` na chamada `google_trackConversion`. Não recomendado — reduz a precisão.

## Segurança e privacidade

O Google Ads só coleta dados em sites e apps com acompanhamento configurado. É necessário fornecer informações claras sobre a coleta de dados e obter consentimento quando exigido por lei ou pelas políticas do Google, incluindo a Política de consentimento de usuários da União Europeia.

## Links relacionados

- [Sobre a codificação automática](https://support.google.com/google-ads/answer/3095550)
- [Sobre o GCLID (identificador de clique do Google)](https://support.google.com/google-ads/answer/9744275)
- [Vinculador de domínio da gtag.js](https://developers.google.com/gtagjs/devguide/linker)
- [Usar a tag do Google para o acompanhamento de conversões do Google Ads](https://support.google.com/google-ads/answer/7548399)
- [Configurar e instalar o Gerenciador de tags do Google](https://support.google.com/tagmanager/answer/6103696)
- [Sobre a tag do Vinculador de conversões](https://support.google.com/tagmanager/answer/7549390)
- [Vincular a propriedade do Analytics à conta do Google Ads](https://support.google.com/google-ads/answer/1704341)
- [Atualizar a tag do Google Analytics para não armazenar o GCLID](https://support.google.com/analytics/answer/7519794)
- [Assistente de tags](https://support.google.com/tagassistant/answer/10039345)
- [Resolver problemas de inclusão de tag em todo o site](https://support.google.com/google-ads/answer/9148089)
- [Usar o Assistente de Tags para resolver problemas com ações de conversão não verificadas ou inativas](https://support.google.com/google-ads/answer/10989978)
- [Sobre as conversões estimadas](https://support.google.com/google-ads/answer/10081327)
- [Sobre as estratégias de Lances inteligentes](https://support.google.com/google-ads/answer/7065882)
