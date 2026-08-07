---
title: "Sobre a medição de conversões"
url: "https://support.google.com/google-ads/answer/1722022?hl=pt-BR"
answer_id: "1722022"
categoria: "02-recursos"
topico: "Medir resultados"
subtopico: "Conversões — Primeiros passos"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Sobre a medição de conversões

## Aviso de migração (relevante para 2026)

A partir de **15 de junho de 2026**, a importação de conversões off-line e os uploads de conversões otimizadas para leads serão migrados para a **API Data Manager** e bloqueados na API Google Ads. Tokens de desenvolvedor que não enviarem solicitação entre janeiro e junho de 2026 não entrarão na lista de permissões de acesso legado. Para evitar interrupções, é preciso usar a API Data Manager para uploads de conversões off-line (atuais e futuras) e de conversões otimizadas para leads.

## O que são conversões

Conversões medem ações que o gestor considera valiosas para o negócio — compra, inscrição, chamada etc. O Google Ads usa essa medição para ajudar a otimizar campanhas.

## Por que usar a medição de conversões

- Identificar quais palavras-chave, anúncios, grupos de anúncios e campanhas geram mais atividades valiosas.
- Entender o ROI e tomar decisões melhores sobre investimento em anúncios.
- Usar estratégias de Lances inteligentes (Maximizar conversões, CPA desejado, ROAS desejado) que otimizam automaticamente as campanhas conforme as metas do negócio.
- Visualizar conversões entre dispositivos/navegadores diferentes (coluna "Todas as conversões" nos relatórios).

## Como as conversões funcionam

### 1. Selecionar as plataformas de acompanhamento

| Fonte | O que mede | Observação |
|---|---|---|
| Conversão no site | Ações específicas realizadas no site após interação com o anúncio (compras, inscrições e outras ações) | Requer configuração de conversões na Web |
| Conversões de app | Instalações de app (Android/iOS) e ações dentro do app | Se houver site + app, usar App Connect para experiência integrada web-para-app |
| Conversões de chamada telefônica | Chamadas diretas do anúncio, ligações para número exibido no site, cliques em telefone no site mobile | — |
| Conversões off-line | Impacto dos anúncios em vendas físicas/fora do site | Funciona de forma diferente dependendo se o rastreamento começa por clique ou por chamada |

### 2. Selecionar uma fonte de dados

Após escolher as plataformas, é preciso adicionar uma fonte de dados para os locais de conversão selecionados. As preferências de origem de dados ficam salvas para próximos usos do fluxo de configuração.

### 3. Criar ações de conversão

Uma ação de conversão é uma atividade específica e valiosa do cliente que será medida; a medição serve para refinar campanhas e alcançar objetivos publicitários.

### 4. Concluir a configuração

Após criar as conversões, é necessário revisar as próximas etapas para garantir que a medição funcione corretamente.

## Mecanismo técnico

O processo varia por origem, mas — exceto para conversões off-line — normalmente se enquadra em uma destas categorias:

- **Tag/snippet no código**: uma tag do Google (ou snippet) é inserida no site ou app. Quando o cliente clica no anúncio de Pesquisa, em determinados sites da Rede de Display, ou visualiza um anúncio em vídeo, um cookie temporário é gravado no dispositivo. Quando a ação definida ocorre, o sistema reconhece o cookie (via o snippet) e registra a conversão.
- **Sem necessidade de tag**: para certos tipos de medição não é preciso configurar tags. Exemplo: ligações de recursos de chamada ou anúncios só para chamadas usam um número de encaminhamento do Google, permitindo saber se a ligação veio de um anúncio e monitorar duração, horários e código de área. Downloads e compras no app via Google Play são registrados automaticamente como conversões, sem necessidade de código de rastreamento.

## Diagnóstico quando as conversões não aparecem (ou ficam abaixo do esperado)

- Verificar se as tags de acompanhamento foram implementadas corretamente (usar o Assistente de tags do Google).
- Se a ação de conversão não aparecer como "Ativa", resolver problemas de status do acompanhamento.
- Para quem usa o Gerenciador de Tags do Google, confirmar se a Tag do Vinculador de Conversões está configurada corretamente.

## Segurança e privacidade

- O Google segue padrões de segurança rigorosos; o Google Ads só coleta dados em sites e apps onde o acompanhamento foi configurado.
- É necessário fornecer aos usuários informações claras e abrangentes sobre os dados coletados em sites, apps e outras propriedades, e obter consentimento quando exigido por lei ou por políticas do Google (incluindo a Política de consentimento de usuários da União Europeia).
- **Observação**: se os usuários não autorizarem coleta, compartilhamento e uso de dados pessoais para personalização de anúncios conforme exigido por lei, é preciso desativar a coleta de informações de remarketing para esses usuários específicos.

## Links relacionados

- [Diversas opções de acompanhamento de conversões](https://support.google.com/google-ads/answer/1722054)
- [Entender os dados de rastreamento de conversões](https://support.google.com/google-ads/answer/6270625)
- [Como o Google Ads rastreia conversões no site](https://support.google.com/google-ads/answer/7521212)
- [Sobre a importação de conversões off-line](https://support.google.com/google-ads/answer/2998031)
- [Assistente de tags do Google](https://support.google.com/tagassistant/answer/10039345)
