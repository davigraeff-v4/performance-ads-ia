---
title: "Sobre a API de Conversões"
url: "https://www.facebook.com/business/help/2041148702652965"
categoria: "05-mensuracao-pixel"
fonte: "Central de Ajuda da Meta para Empresas"
idioma: "pt-BR"
extraido_em: "2026-07-31"
---

# Sobre a API de Conversões

A API de Conversões (CAPI) foi desenvolvida para criar uma conexão direta entre os dados de marketing e os sistemas de otimização de anúncios da Meta, ajudando a otimizar o direcionamento, reduzir o custo por resultado e mensurar resultados nas tecnologias da Meta.

## Como a API de Conversões funciona

A API de Conversões cria uma conexão direta e mais confiável entre dados de marketing (do servidor, plataforma do site, app ou CRM) e a Meta. Os dados de marketing incluem eventos do site, eventos do app, conversões offline e eventos de mensagens. Esses dados ajudam a otimizar, mensurar e personalizar anúncios, exibindo-os para pessoas com maior probabilidade de achá-los relevantes.

As conversões offline podem ser usadas para otimização de anúncios em campanhas com objetivo de Vendas ao selecionar "Site e loja física".

É possível configurar a API de Conversões de várias maneiras — muitas integrações não exigem desenvolvedor.

## Gerenciamento de dados de eventos

A API de Conversões é compatível com eventos de várias fontes: sites, estabelecimentos físicos, e-mail, chat comercial, telefone, app para celular e eventos offline. Ela pode substituir a API de Eventos do App e a API de Conversões Offline.

Observação: a API de Conversões Offline foi descontinuada em maio de 2025 — recomenda-se carregar eventos em conjuntos de dados e converter integrações antigas para a API de Conversões.

## Benefícios adicionais

Usar a API de Conversões junto ao Pixel da Meta (evento redundante) ajuda a:

- Melhorar a conectividade e reduzir o custo por resultado, já que os dados da API são menos afetados por erros de carregamento, problemas de conectividade e bloqueadores de anúncios.
- Otimizar anúncios para ações posteriores na jornada do cliente (ex.: assinaturas pós-compra, ações em loja física).
- Melhorar a mensuração e a atribuição ao longo da jornada do cliente.
- Aumentar os eventos correspondidos, reduzindo o custo por resultado, ao incluir mais parâmetros de informações do cliente.

## Integração da API de Conversões com o Pixel da Meta

Ao usar a API de Conversões para enviar eventos do site, é recomendável também usar o Pixel. Os eventos do site enviados pela API de Conversões ficam vinculados ao Pixel e se comportam como eventos enviados pelo Pixel nos seguintes aspectos:

- São usados para os mesmos tipos de otimização de anúncios, incluindo maximizar o número de conversões e maximizar o valor das conversões.
- Aparecem na maioria das mesmas superfícies, incluindo o Gerenciador de Anúncios e o Gerenciador de Eventos da Meta.
- Seguem a ferramenta de atividade fora do Facebook e o controle de personalização de anúncios com dados de terceiros, além de outras restrições dos Termos das Ferramentas Comerciais da Meta.
- Assim como o Pixel, a API de Conversões não foi projetada como forma de contornar políticas de compartilhamento de dados, como o framework de transparência de rastreamento de apps (ATT) da Apple ou regras de privacidade europeias, como a Diretiva de Privacidade Eletrônica.

## Benefícios para eventos de app

Ao usar a API de Conversões para enviar eventos de app, é possível:

- Depender menos de atualizações do SDK e de versões do app: usar a API de Conversões para enviar novos dados de eventos sem precisar manter o SDK do Facebook para iOS ou Android, nem depender de atualizações de versão do app.

## Benefícios para eventos offline

Ao usar a API de Conversões para enviar eventos offline, é possível:

- Mensurar resultados em loja física impulsionados pelos anúncios da Meta.
- Criar públicos personalizados e semelhantes com base nos eventos offline.
- Realizar estudos de lift para entender o impacto dos anúncios da Meta nas compras em loja física.

## Benefícios para eventos de mensagens

Ao usar a API de Conversões para enviar eventos de mensagens, é possível:

- Conectar dados valiosos de conversas comerciais: compartilhar eventos pode ajudar a entender as ações que as pessoas realizam em chats comerciais no Messenger, Instagram ou WhatsApp.
- Otimizar anúncios de clique para o Messenger com foco em compras, para melhorar o desempenho (a otimização está disponível atualmente apenas para eventos de compra no Messenger).
- Melhorar a mensuração: a API de Conversões ajuda a entender e mensurar melhor ações que ocorrem mais tarde na jornada do cliente, como realizar uma compra.

## Saiba mais

- Como preparar sua empresa para usar a API de Conversões
- Boas práticas para a API de Conversões
- Comparar os métodos de configuração
- Sobre a Mensuração de Eventos Agregados da Meta
