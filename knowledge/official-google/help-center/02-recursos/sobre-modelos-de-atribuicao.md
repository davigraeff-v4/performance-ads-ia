---
title: "Sobre modelos de atribuição"
url: "https://support.google.com/google-ads/answer/6259715?hl=pt-BR"
answer_id: "6259715"
categoria: "02-recursos"
topico: "Medir resultados"
subtopico: "Atribuição"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Sobre modelos de atribuição

## Aviso de descontinuação

O Google **não oferece mais suporte** aos modelos de atribuição linear, baseada na posição, de primeiro clique e de iminência da conversão. As ações de conversão que usavam esses modelos descontinuados foram automaticamente atualizadas para a **atribuição baseada em dados**. Ainda é possível migrar para o modelo de **último clique**, que continua sendo aceito.

## O que são modelos de atribuição

No caminho de conversão, os clientes podem interagir com vários anúncios do mesmo anunciante. Os modelos de atribuição determinam quanto crédito cada interação recebe pelas conversões, ajudando a entender melhor o desempenho dos anúncios e a otimizar as jornadas de conversão.

## Por que usar

A maioria dos anunciantes mede sucesso pelo "último clique" — atribuindo todo o crédito ao último anúncio/palavra-chave clicado, o que ignora as demais interações do caminho. Com modelos de atribuição é possível:

- **Alcançar clientes no início do ciclo de compra**: identificar oportunidades de influenciar clientes cedo no caminho de conversão.
- **Estabelecer correspondência com o negócio**: escolher o modelo mais alinhado à forma como as pessoas pesquisam a oferta.
- **Aprimorar os lances**: otimizar lances com base em uma compreensão mais completa da performance dos anúncios.

## Os modelos disponíveis atualmente

- **Último clique**: atribui 100% do crédito da conversão ao último anúncio clicado e à palavra-chave correspondente.
- **Baseada em dados**: distribui o crédito de acordo com o histórico real dessa ação de conversão, calculando a contribuição de cada interação a partir dos dados da própria conta. É o modelo **padrão para a maioria das ações de conversão**.

**Observação**: conversões realizadas no app podem ser atribuídas às campanhas para apps para fins de geração de relatórios.

### Exemplo ilustrativo

Uma cliente pesquisa "restaurante toscana", "restaurante florença", "restaurante 3 estrelas florença" e "restaurante 3 estrelas abigaille florença", clicando em anúncios em cada pesquisa, e reserva mesa após clicar no anúncio da última pesquisa.

- **Último clique**: a palavra-chave "restaurante 3 estrelas abigaille florença" recebe 100% do crédito.
- **Baseada em dados**: cada palavra-chave recebe uma fração do crédito, proporcional à sua contribuição real para a conversão.

## Canais que podem receber crédito

- Canais pagos do Google (Google Ads)
- Canais pagos (mídia paga em geral)
- Canais pagos e orgânicos
- Canais de [editor] (apenas canais do editor)
- Canais desconhecidos (crédito atribuído pela fonte de dados)

Os canais elegíveis para crédito variam conforme a outra atividade medida na conta e nos demais produtos do Google configurados (Google Ads, Google Analytics, Search Ads 360, Display & Video 360, Campaign Manager).

## Modelo de atribuição e impacto em conversões e lances

- A configuração "Modelo de atribuição" no acompanhamento de conversões pode ser aplicada a ações de conversão no site e do Google Analytics.
- Afeta como conversões são registradas nas colunas **"Conversões"** e **"Todas as conversões"** — a coluna "Conversões" só reflete ações marcadas como conversões principais.
- O modelo escolhido afeta **somente** a ação de conversão à qual foi aplicado.
- Afeta diretamente estratégias de lances automáticas que otimizam conversões: **CPA desejado**, **ECPC (custo por clique otimizado)** e **ROAS desejado**. Em estratégias manuais, é possível alterar o modelo para ajudar na definição de lances.
- Recomendação: ao adotar um novo modelo diferente de "último clique", testar primeiro e acompanhar o impacto no ROI.

### Diagnóstico de problemas após mudar o modelo
Se as conversões pararem de ser registradas ou a ação aparecer como "Inativo": verificar se as tags do Google estão implementadas corretamente (especialmente páginas de agradecimento/confirmação), usar o Assistente de Tags do Google, confirmar que a tag do Vinculador de Conversões está ativa (se usar o Gerenciador de Tags do Google) e fazer conversões de teste.

## Relatório "Comparação de modelos"

Permite comparar dois modelos de atribuição lado a lado (por palavra-chave, grupo de anúncios, campanha ou dispositivo). Útil para identificar elementos subvalorizados no modelo "Último clique" ao compará-los com "Baseada em dados".

**Observação**: pode exibir aviso de que dados históricos estão disponíveis apenas parcialmente para o período selecionado — isso ocorre quando a conta se qualificou recentemente para atribuição de várias redes; contas nesse caso devem escolher um período mais recente para ver dados completos.

**Dica**: usar as colunas "Custo / conv." e "Valor da conv. / custo" no relatório para comparar CPA e ROAS entre modelos e identificar campanhas/palavras-chave subvalorizadas.

## Como definir/alterar o modelo de atribuição

### Comparar modelos
1. Acessar Atribuição no menu Metas.
2. No menu de páginas à esquerda, selecionar Comparação de modelos.
3. Escolher uma opção no menu suspenso "Dimensão".
4. Usar os menus "Comparar" e "Com" para selecionar os modelos a comparar.

### Mudar o modelo de uma ação de conversão
1. Acessar Resumo no menu Metas.
2. Na tabela, clicar no nome da conversão a editar.
3. Selecionar Editar configurações.
4. Escolher o Modelo de atribuição no menu suspenso.
5. Selecionar Salvar e Concluído.

Contas que usam acompanhamento de conversões de várias contas (nível de conta de administrador) precisam selecionar o modelo de atribuição na conta de administrador.

## Colunas de relatório "modelo atual"

Ao alterar o modelo de atribuição, a mudança só afeta o registro **a partir daquele momento** nas colunas "Conversões" e "Todas as conversões". Para ver como os dados históricos ficariam com o modelo escolhido, é possível adicionar colunas específicas (seção "Atribuição" do menu Colunas):

- Conversões (modelo atual)
- Custo / conv. (modelo atual)
- Taxa conv. (modelo atual)
- Valor da conv. (modelo atual)
- Valor da conv. / custo (modelo atual)
- Valor da conv. / clique (modelo atual)
- Valor / conv. (modelo atual)

Essas colunas, como as colunas "Conversões" padrão, não incluem ações não marcadas como conversões principais (mas incluem conversões em dispositivos diferentes por padrão), e não são afetadas por dados que independem do modelo de atribuição, como campanhas de display com faturamento por pagamento por conversões.

## Links relacionados

- [Sobre a atribuição baseada em dados](https://support.google.com/google-ads/answer/6394265)
- [Sobre os Relatórios de atribuição](https://support.google.com/google-ads/answer/1722023)
- [Sobre modelos de atribuição descontinuados](https://support.google.com/google-ads/answer/13427716)
- [Práticas recomendadas para gerenciar alterações no modelo de atribuição](https://support.google.com/google-ads/answer/9203352)
- [Sobre conversões principais](https://support.google.com/google-ads/answer/11461796)
- [Sobre estratégias de lances automáticas](https://support.google.com/google-ads/answer/2472725)
- [Sobre CPA desejado](https://support.google.com/google-ads/answer/6268632)
- [Sobre ECPC](https://support.google.com/google-ads/answer/2464964)
- [Sobre ROAS desejado](https://support.google.com/google-ads/answer/6268637)
- [Sobre atribuição de várias redes](https://support.google.com/google-ads/answer/9296311)
- [Sobre acompanhamento de conversões de várias contas](https://support.google.com/google-ads/answer/3030657)
- [Usar o pagamento por conversões em campanhas de display](https://support.google.com/google-ads/answer/7528254)
