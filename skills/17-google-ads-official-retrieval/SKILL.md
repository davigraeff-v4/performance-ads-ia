---
name: 17-google-ads-official-retrieval
description: Localiza e lê seletivamente documentação oficial do Google Ads e da Google Ads API. Use antes de responder sobre funcionamento, configuração, política, faturamento, campanhas, palavras-chave, lances, conversões, anúncios, assets, mensuração, otimização, MCP ou erros Google Ads.
---

# Recuperação Oficial Google Ads

## Fontes permitidas

1. Ler `knowledge/official-google/source-catalog.md`.
2. Ler somente os resumos locais diretamente relevantes.
3. Para informação atual, pesquisar e abrir páginas em:
   - `support.google.com/google-ads/`
   - `developers.google.com/google-ads/api/`
   - `github.com/googleads/google-ads-mcp`
   - `console.cloud.google.com/` somente para orientar a ação interativa do usuário no projeto correto.

## Processo

1. Preservar a pergunta original.
2. Identificar se o tema é interface/produto, API/MCP, política ou metodologia.
3. Abrir somente as 1–3 fontes oficiais mais aderentes.
4. Ler integralmente a seção necessária; não responder por snippet.
5. Verificar data, versão da API, elegibilidade e limitações por tipo de campanha.
6. Separar `Google informa` de `metodologia recomenda`.
7. Registrar título, URL e data de consulta no dossiê.

## Rotas de configuração

- Projeto e API habilitada: `oauth/cloud-project`.
- Credenciais e armazenamento seguro: `oauth/credential-management`.
- OAuth de usuário/ADC: `oauth/single-user-authentication`.
- Refresh token sem `gcloud`: exemplo oficial `generate-user-credentials`.
- Service account: `oauth/service-accounts`.
- Developer token e nível de acesso: `api-policy/developer-token` e `api-policy/access-levels`.
- MCC/login customer ID: `concepts/call-structure`.
- Instalação e ferramentas MCP: README atual de `googleads/google-ads-mcp`.

Ao orientar obtenção de credenciais, nunca pedir valores no chat. Explicar onde o usuário encontra cada item e trabalhar somente com caminhos locais e placeholders.

## Gates

- Política, cobrança, elegibilidade, campos de API e comportamento mutável exigem fonte ao vivo.
- Não usar blog, fórum, fornecedor ou MCP comunitário como fonte normativa quando houver fonte oficial.
- Não afirmar disponibilidade de recurso na conta sem verificar via MCP/interface.
- Não transformar recomendação do Google em regra universal ou autorização de execução.
