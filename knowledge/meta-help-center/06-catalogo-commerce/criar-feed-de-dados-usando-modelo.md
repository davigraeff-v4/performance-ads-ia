---
title: "Como criar um feed de dados para seu catálogo usando um modelo"
url: "https://www.facebook.com/business/help/1898524300466211"
categoria: "06-catalogo-commerce"
fonte: "Central de Ajuda da Meta para Empresas"
idioma: "pt-BR"
extraido_em: "2026-07-31"
---

# Como criar um feed de dados para seu catálogo usando um modelo

Um feed de dados é um arquivo usado para carregar informações de produtos do seu catálogo no Gerenciador de Comércio. Para criar seu feed, baixe e preencha um modelo do Gerenciador de Comércio.

## Antes de começar

Você precisa de controle total do catálogo.

## Como baixar um modelo de feed de dados para seu catálogo

Para baixar um modelo de feed:

1. Acesse o Gerenciador de Comércio e selecione o catálogo.
2. Na aba Catálogo, acesse Produtos ou Fontes de dados.
3. Clique em **+ Adicionar** no canto superior direito. Selecione **Arquivo de dados** no menu suspenso.
4. Clique em **Baixar modelo**.
5. Escolha seu modelo:
   - Para baixar um modelo padrão, selecione o formato de arquivo de sua preferência: Excel (XLSX) ou CSV.
   - (Apenas produtos) Para criar um modelo personalizado com campos específicos de categorias, clique em **Modelo personalizado**. Selecione uma ou mais categorias de produto que você vende. Quando terminar, clique em Baixar modelo .xlsx ou abra o menu suspenso e clique em Baixar modelo .csv.

Você baixou um modelo de feed. Agora pode preenchê-lo com os dados dos seus produtos.

## Como preencher o modelo de feed de dados

Para preencher seu modelo de feed com os dados dos seus produtos:

1. Abra o arquivo XLSX ou CSV que você acabou de baixar em um programa de planilha, como o Microsoft Excel, ou importe-o para o Planilhas Google.

   Observação: se você usar o Planilhas Google, seu feed precisa estar na primeira aba. Todas as outras abas são ignoradas. Use uma conta pessoal do Google, não do Google Workspace, pois sua organização pode não permitir o compartilhamento externo de arquivos. Defina sua opção de compartilhamento de links como "Quem tiver o link" (não Restrito) para permitir o compartilhamento de arquivos com a Meta.

2. Abra as especificações de dados para o tipo de produto ou serviço do seu catálogo em uma nova aba ou janela. Será necessário consultá-las para preencher o modelo. As categorias incluem: Produtos, Transmissão de mídia, Apps e software, Artigos e publicações, Serviços profissionais, Hotéis/voos/destinos, Inventário e ofertas de automóveis, Imóveis, e Outros produtos ou serviços.
3. Analise seu modelo. A linha de cabeçalho contém uma série de colunas, cada uma representando um atributo de produto no próprio campo. Não altere os nomes dos campos — eles devem continuar em inglês e corresponder exatamente às especificações. As linhas abaixo conterão os dados dos seus produtos, com um item por linha. Você deve inserir os dados em todos os campos obrigatórios. É possível manter os campos identificados como opcionais ou excluí-los.
4. No modelo, exclua as linhas de exemplo e substitua-as por dados de produtos reais para cada atributo. Alguns campos são compatíveis com texto livre, enquanto outros aceitam somente determinados valores. Siga com atenção as especificações para evitar erros. Exemplo de estrutura do feed:

   | id | title | description | availability | condition | price | link | image_link | brand |
   |----|-------|--------------|--------------|-----------|-------|------|------------|-------|
   | 1234 | Tapete listrado | Preto e branco... | in stock | new | 24.99 USD | http://www... | http://www... | Jasper's Market |
   | 5678 | Manta felpuda | Para dias frios... | in stock | new | 14.99 USD | http://www... | http://www... | Jasper's Market |
   | 9123 | Almofada | Veludo vermelho... | in stock | new | 9.99 USD | http://www... | http://www... | Jasper's Market |

5. (Apenas produtos) Para adicionar variantes de um produto, como cores e tamanhos diferentes, adicione cada variante à própria linha e preencha os seguintes campos:
   - No campo `item_group_id`, insira a mesma identificação de grupo para todas as variantes do mesmo produto. Isso indica que elas pertencem a um grupo.
   - Adicione os atributos da variante que desejar para diferenciar cada variante: `color`, `size`, `material`, `pattern`, `gender` ou `additional_variant_attribute`. Preencha os mesmos atributos para todas as variantes do grupo.
6. Depois de inserir todos os dados dos seus produtos, salve o arquivo.

Você concluiu o modelo de feed de dados. Agora pode carregá-lo no seu catálogo.
