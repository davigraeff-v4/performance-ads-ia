---
title: "Como configurar e instalar o Pixel da Meta"
url: "https://www.facebook.com/business/help/952192354843755"
categoria: "05-mensuracao-pixel"
fonte: "Central de Ajuda da Meta para Empresas"
idioma: "pt-BR"
extraido_em: "2026-07-31"
---

# Como configurar e instalar o Pixel da Meta

O Pixel da Meta é um trecho de código colocado no site para entender as ações que as pessoas realizam nele e mensurar a eficácia da publicidade na Meta.

A configuração de um pixel envolve duas etapas:

1. Criar o pixel no Gerenciador de Eventos e configurar o código base no site (por integração de parceiro ou manualmente).
2. Configurar eventos no site para mensurar ações, como compras (por integração de parceiro, pela ferramenta de configuração "apontar e clicar", ou manualmente por código).

Se eventos são compartilhados com a Meta usando o pixel, é recomendado usar também a API de Conversões, que trabalha junto ao Pixel para melhorar o desempenho e a mensuração das campanhas.

## Antes de começar

- É necessário ter um site ou app da empresa.
- Para configuração manual por código, pode ser necessária ajuda de um desenvolvedor para atualizar o código do site ou do gerenciador de tags.

## Passo a passo

1. Acesse o Gerenciador de Eventos da Meta.
2. Clique em Conectar dados e selecione Web, depois Conectar.
3. Digite um nome para o pixel e clique em Criar pixel (gera um novo ID, visível no Gerenciador de Eventos).
4. Se houver um site, insira a URL para verificar opções de integração de parceiro; se não houver, marque "Eu não tenho um site" e continue.
5. Escolha como conectar os dados: "Obter orientação" (recomendado, com recomendações de configuração) ou "Faça você mesmo".
6. Selecione a opção de configuração: "API de Conversões e Pixel da Meta" ou "Pixel da Meta somente".
   - Para API de Conversões e Pixel: escolha entre integração de parceiro, API de Conversões habilitada pela Meta (somente web) ou configuração manual.
   - Para Pixel somente: escolha instalar o código manualmente, procurar um parceiro, ou enviar instruções por e-mail a um desenvolvedor.

## Como adicionar o código do Pixel manualmente ao site

1. Copie o código base do pixel.
2. Localize o cabeçalho do site ou o modelo de cabeçalho no CMS ou na plataforma web.
3. Cole o código base na parte inferior da seção de cabeçalho, logo acima da tag de fechamento `</head>`, em todas as páginas do site. O ID do pixel já vem incluído no código base, e é possível usar o mesmo ID em todo o site.
4. Clique em Continuar.
5. (Opcional, se elegível) Ative "Incluir automaticamente informações mais detalhadas de página e produto" para permitir que o Pixel da Meta use IA para identificar e compartilhar detalhes relevantes do site (como nome do produto, preço e disponibilidade) com a Meta.
6. (Opcional, se elegível) Ative a "Correspondência avançada automática" e verifique as informações de cliente que deseja enviar.
7. Clique em Continuar.
8. Adicione eventos usando a ferramenta de configuração de eventos ou inserindo código manualmente no site:
   - Para usar a ferramenta de configuração de eventos: clique em "Abrir ferramenta de configuração de eventos" e siga as instruções na tela para adicionar eventos e parâmetros sem necessidade de codificação adicional.
   - Para configuração manual: clique em "Instalar eventos usando código" para configurar o Pixel da Meta por código.

Após configurar o pixel no site, é importante verificar se ele está funcionando corretamente e, em seguida, aprender a adicionar pessoas ao pixel.

## Saiba mais

- Sobre o Pixel da Meta
- Sobre o Auxiliar de Pixel da Meta
- Sobre a API de Conversões
