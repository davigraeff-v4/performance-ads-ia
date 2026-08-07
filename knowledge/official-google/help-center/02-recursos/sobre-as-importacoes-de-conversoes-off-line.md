---
title: "Sobre as importações de conversões off-line"
url: "https://support.google.com/google-ads/answer/2998031?hl=pt-BR"
answer_id: "2998031"
categoria: "02-recursos"
topico: "Medir resultados"
subtopico: "Conversões off-line"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Sobre as importações de conversões off-line

## Avisos de migração (relevantes para 2026)

- A partir de **15 de junho de 2026**, a importação de conversões off-line e os uploads de conversões otimizadas para leads serão migrados para a **API Data Manager** e bloqueados na API Google Ads. Tokens de desenvolvedor que não solicitarem entre janeiro e junho de 2026 ficarão fora da lista de permissões de acesso legado.
- **Importante**: as conversões otimizadas para a Web e para leads serão combinadas em uma **única configuração de ativação/desativação**. A partir de abril de 2026, o Google Ads passará a aceitar simultaneamente dados fornecidos pelo usuário vindos de tags de sites, da Central de Dados e de conexões de API — não será mais necessário escolher um único método. Contas existentes serão migradas automaticamente para essa configuração unificada.
- Quem ainda não adotou a importação de conversões off-line deve começar diretamente pelas **conversões otimizadas para leads** (mais fáceis de configurar e com relatórios mais duráveis e precisos). Quem já usa a importação padrão deve considerar o upgrade para aproveitar esses benefícios.

## O que são conversões off-line

Um anúncio nem sempre leva a uma venda on-line — às vezes conduz o cliente a uma venda off-line (na loja física ou por telefone). A importação de conversões off-line permite analisar o que acontece no mundo off-line depois que o anúncio gera um clique ou uma chamada.

## Conversões otimizadas para leads (versão recomendada/atual)

São uma versão atualizada da importação de conversões off-line que usa **dados fornecidos pelo usuário com hash** (ex.: e-mail) para complementar os dados de conversão importados, melhorando precisão e performance dos lances. Ao importar, os dados com hash são usados para atribuir a conversão de volta à campanha do Google Ads, cruzando com os dados coletados no site (ex.: formulário de lead) e com Contas do Google conectadas que interagiram com o anúncio.

Quem já usa conversões off-line pode fazer upgrade e importar dados fornecidos pelo usuário além do GCLID já importado.

### Vantagens

| Vantagem | Descrição |
|---|---|
| Durável | Resultados mais confiáveis; obedece a regulamentos de privacidade mais rígidos |
| Fácil de configurar | Ajuste feito direto na conta do Google Ads |
| Performance otimizada | Relatórios de conversão mais precisos que a importação off-line padrão; ativa conversões de visualização engajada e entre dispositivos |
| Configuração simplificada | Inclusão de tags e compartilhamento de dados pessoais simplificados pela Central de Dados |
| Flexível | Implementação via tag do Google ou Gerenciador de tags do Google |

**Dado de impacto**: anunciantes que usaram dados próprios (e-mails, telefones) combinados com GCLIDs da importação off-line tiveram um **aumento médio de 10% nas conversões** em comparação com quem usa apenas a importação de conversões off-line padrão.

A forma mais rápida de configurar/fazer upgrade é pela **Central de Dados**, onde o GCLID e os dados fornecidos pelo usuário servem como chaves de correspondência para as importações.

Após configurar (via Gerenciador de Tags do Google ou Tag do Google), é possível verificar a eficiência no **relatório de diagnóstico de conversões otimizadas** — que ajuda a identificar problemas comuns como dados do usuário ausentes/mal formatados ou implementação incorreta do código in-page. Também existe uma **lista de verificação de implementação das conversões otimizadas para leads** e é possível configurar via API do Google Ads.

## Como funcionam as importações (mecanismos por origem)

As importações de conversões off-line funcionam de forma diferente dependendo se a conversão se origina de um **clique** ou de uma **chamada**.

### [Recomendado] Conversões originadas de cliques — conversões otimizadas para leads
Usam uma tag para capturar dados próprios, garantindo medição durável, precisa e de alta qualidade, com upload de dados mais detalhados dos leads de volta ao Google para mais relatórios e insights de otimização.

### Conversões originadas de cliques — usando GCLID
O Google Ads atribui um **ID de clique do Google (GCLID)** exclusivo a cada clique em anúncio que leva ao site. Para acompanhar conversões off-line originadas de cliques: salvar o GCLID junto às informações de lead coletadas da pessoa; quando ela realizar a conversão off-line (ex.: assinar um contrato), enviar o GCLID de volta ao Google Ads com detalhes do tipo de conversão e a data em que ocorreu. O Google Ads então registra essa conversão junto aos demais dados de acompanhamento.

### Conversões originadas de chamadas
Importar informações de conversões de chamada permite identificar quais anúncios e palavras-chave geram mais chamadas de vendas.

## Complementar medição on-line com dados off-line

É possível combinar as medições on-line do site com dados próprios off-line (de sistemas de gerenciamento de pedidos ou plataformas de dados) diretamente na interface do Google Ads, sem apoio de desenvolvedores, para otimizar a performance da campanha usando mais fontes de dados.

## Segurança e privacidade

O Google Ads só coleta dados em sites e apps com acompanhamento configurado. É necessário fornecer informações claras sobre a coleta de dados e obter consentimento quando exigido por lei ou pelas políticas do Google, incluindo a Política de consentimento de usuários da União Europeia.

## Links relacionados

- [Faça upgrade da importação de conversões off-line para conversões otimizadas para leads](https://support.google.com/google-ads/answer/14274408)
- [Configurar as conversões otimizadas para leads com a tag do Google](https://support.google.com/google-ads/answer/11021502)
- [Configurar conversões otimizadas para leads com o Gerenciador de tags do Google](https://support.google.com/google-ads/answer/11347292)
- [Seu guia para a estimativa de conversão (em inglês)](https://support.google.com/google-ads/answer/12284070)
- [Sobre a importação de conversões de chamada](https://support.google.com/google-ads/answer/6301373)
- [Melhorar a medição do seu site com mais fontes de dados (Beta)](https://support.google.com/google-ads-data-manager/answer/16542291)
- [Sobre as conversões otimizadas para leads](https://support.google.com/google-ads/answer/15713840)
- [Sobre a Central de Dados](https://support.google.com/google-ads/answer/14639041)
- [Relatório de diagnóstico de conversões otimizadas](https://support.google.com/google-ads/answer/15249267)
- [Lista de verificação para implementação das conversões otimizadas para leads](https://support.google.com/google-ads/answer/16782203)
- [Sobre a importação de conversões off-line: como o Google usa dados de leads](https://support.google.com/adspolicy/answer/9755941#leads)
