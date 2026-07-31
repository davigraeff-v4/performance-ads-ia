---
title: "Sobre carregamentos de feed de dados programados para catálogos"
url: "https://www.facebook.com/business/help/2284463181837648"
categoria: "06-catalogo-commerce"
fonte: "Central de Ajuda da Meta para Empresas"
idioma: "pt-BR"
extraido_em: "2026-07-31"
---

# Sobre carregamentos de feed de dados programados para catálogos

É possível configurar e gerenciar carregamentos de feed de dados programados para atualizar o catálogo por hora, dia ou semana. Salve o arquivo de dados em um site de hospedagem e forneça o link. A Meta busca o arquivo e atualiza o catálogo nos horários programados.

## Especificações para feeds programados

- **Formatos de arquivo compatíveis**: CSV, TSV, Excel (XLSX), XML (RSS/ATOM) ou Planilhas Google. O URL deve começar com http, https, ftp ou sftp e direcionar para o arquivo, e não para seu site, sua Página do Facebook ou outro local.
- **Tamanho máximo do arquivo**: 4 GB. Caso o arquivo seja maior ou contenha mais de um milhão de produtos, divida os produtos em vários feeds de dados e carregue-os separadamente. Para que o processamento de arquivos grandes seja mais rápido, também é recomendável usar a configuração de atualização para carregamentos de feed (veja abaixo) em vez da configuração de substituição.
- **Compartilhamento de arquivos**: se o arquivo for protegido por senha, adicione o nome de usuário e a senha no seu feed. Para as Planilhas Google, altere a opção de compartilhamento de link para "Qualquer pessoa com o link" e não "Restrito".

## Como adicionar ou alterar uma programação de carregamento de feed

Quando você carregar um novo feed de dados no Gerenciador de Comércio, será possível escolher uma programação. É possível adicionar ou alterar programações a qualquer momento em Fontes de dados. Selecione seu feed de dados, acesse Configurações e edite os cronogramas em Cronogramas.

## Diferença entre a configuração de substituir e atualizar carregamento de feed

Há duas configurações de programação de carregamento. Você pode substituir o feed anterior durante cada carregamento ou apenas atualizá-lo.

- **Programação de substituição**: o novo feed substitui completamente todos os dados de produtos do feed anterior. Ele adiciona novos produtos ao catálogo, atualiza produtos existentes e exclui qualquer produto que você removeu do novo arquivo. Essa é a configuração padrão quando você carrega um novo feed de dados com uma programação. O tempo de processamento do carregamento é maior.
- **Programação de atualização**: seu novo feed é rapidamente lido. Os produtos existentes são atualizados e os novos são adicionados ao seu catálogo. O tempo de processamento do carregamento é mais rápido. No entanto, quaisquer produtos ou campos que você excluir do arquivo serão ignorados. Para excluir produtos ou dados usando a configuração de atualização, você deve realizar certas ações:
  - Para excluir produtos, adicione um campo `delete` no seu feed e insira `true` para cada produto. Carregue o feed uma vez para excluir os produtos. Você pode remover os produtos do arquivo posteriormente.
  - Para excluir os dados de produto de um determinado campo, deixe o campo no feed, mas vazio. Por exemplo, para remover o preço de venda de um produto, defina o campo `sale_price` como 0 ou deixe-o em branco. Carregue o feed uma vez para excluir os dados desse campo. Você pode remover o campo depois se quiser.

## Dicas para programar carregamentos de feed

- Programe os carregamentos para acontecerem depois de você atualizar o feed. Dessa forma, o catálogo poderá receber os dados de produtos mais recentes de forma rápida. Por exemplo, se você atualizar o feed no seu site diariamente às 9h, poderá configurar um carregamento programado para 9h15.
- Se você usar apenas a configuração de atualização, o número de produtos no catálogo pode continuar crescendo, porque essa configuração não exclui nenhum produto (a menos que você use o campo `delete`). Você pode configurar uma combinação de horários de carregamento para manter seus dados de produtos atualizados. Por exemplo, você pode configurar:
  - Uma programação de atualização por hora para atualizar dados de produtos, como preços e disponibilidade.
  - Uma programação de substituição semanal ou mensal para limpar o catálogo, excluindo produtos antigos ou desatualizados.
- As programações de substituição e atualização para o mesmo feed devem ter pelo menos dez minutos de diferença.
