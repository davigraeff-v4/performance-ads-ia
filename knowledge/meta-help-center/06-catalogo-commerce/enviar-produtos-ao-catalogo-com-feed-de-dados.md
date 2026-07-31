---
title: "Como carregar produtos no catálogo com um feed de dados no Gerenciador de Comércio"
url: "https://www.facebook.com/business/help/125074381480892"
categoria: "06-catalogo-commerce"
fonte: "Central de Ajuda da Meta para Empresas"
idioma: "pt-BR"
extraido_em: "2026-07-31"
---

# Como carregar produtos no catálogo com um feed de dados no Gerenciador de Comércio

Um feed de dados é um arquivo que contém dados de produtos que você carrega no catálogo no Gerenciador de Comércio. É possível carregar um arquivo uma vez ou configurar carregamentos programados para manter os produtos atualizados.

Observação: essas etapas mostram como carregar um novo feed de dados no seu catálogo. Também é possível atualizar um feed existente.

## Antes de começar

- Você precisa de controle total do catálogo.
- Crie um feed de dados no formato XLSC, CSV, TSV ou XML (RSS/ATOM) ou Planilhas Google e inclua os campos obrigatórios para cada produto. O tamanho máximo do arquivo é de 4 GB. Caso o arquivo seja maior ou contenha mais de um milhão de produtos, divida os produtos em vários feeds de dados e carregue-os separadamente.
- (Opcional) Para configurar uma programação de carregamento, salve o arquivo no servidor, em um site de hospedagem ou no Planilhas Google e tenha o link pronto.

## Carregar um feed de dados em um catálogo

Para carregar um novo arquivo de feed de dados:

1. Acesse o Gerenciador de Comércio e selecione seu catálogo.
2. Na aba Catálogo, acesse Produtos ou Fontes de dados.
3. Clique em **+ Adicionar** e selecione **Arquivo de dados** no menu suspenso.
4. Em "Seu arquivo está formatado para qual plataforma?", o Gerenciador de Comércio está selecionado por padrão. Isso significa que seu arquivo está formatado de acordo com as especificações de dados de produtos da Meta. No entanto, se estiver carregando um arquivo formatado para publicidade no Google, selecione **Google Merchant Center**.
5. Escolha como deseja carregar o arquivo:
   - **Use um URL ou o Planilhas Google**: forneça o link para o arquivo salvo no servidor, em um site de hospedagem ou no Planilhas Google. O link deve começar com http://, https://, ftp:// ou sftp:// e direcionar para seu arquivo, não para uma página no site ou em outro local. Teste o link no navegador antes para ter certeza de que ele abre ou baixa o arquivo.
     - Se o arquivo estiver no Planilhas Google, os dados devem estar na primeira aba e a opção de compartilhamento deve ser configurada como "Qualquer pessoa com o link", e não "Restrito".
     - Se o link começa com ftp:// ou sftp:// e é protegido por senha, insira o nome de usuário e a senha. Não insira detalhes de login a menos que o link os exija.
   - **Carregar do seu computador**: arraste e solte o arquivo do seu computador ou clique em Escolher arquivo no seu dispositivo.
6. Clique em **Avançar**.
7. Se os campos no seu feed de dados não corresponderem aos campos aos quais a Meta oferece suporte, o sistema tentará ajudar você a correspondê-los. Em "Campo do seu feed de dados", analise ou selecione qual campo no feed você deseja corresponder a cada um dos campos suportados. Por exemplo, se você forneceu títulos de produto em um campo chamado "nome", poderia correspondê-los ao campo "título". Para corresponder a mais campos, clique em **Adicionar ou remover campos** e repita o processo. Em seguida, clique em **Avançar**. Regras de dados são criadas para corresponder automaticamente esses campos em futuros carregamentos do feed.
8. Na janela pop-up, dê um nome ao seu feed de dados e selecione a moeda padrão a ser usada se algum preço não tiver um código de moeda.
9. Se você tiver fornecido um link para o arquivo na etapa 5, escolha uma programação de carregamento por hora, dia ou semana. Programe os carregamentos para acontecerem depois de você atualizar o arquivo. Dessa forma, o catálogo receberá os dados mais recentes de forma rápida. Por exemplo, se você atualizar o arquivo no seu site diariamente às 9h, poderá configurar um carregamento programado para 9h15.
10. Clique em **Carregar**.

O feed de dados aparece em Fontes de dados no Gerenciador de Comércio. Quando o carregamento for concluído, você verá um resumo com:

- O número de produtos adicionados ou atualizados durante o carregamento.
- Erros que impediram que os produtos ou o arquivo inteiro fossem carregados.
- Qualquer problema que impeça produtos de aparecerem nos seus anúncios ou lojas.

Volte para Fontes de dados e clique no feed de dados a qualquer momento para ter uma visão geral ou gerenciar as configurações. É possível editar ou adicionar programações, atualizar o feed, adicionar regras de dados ou excluir o feed.
