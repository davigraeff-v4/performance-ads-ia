---
name: 17-google-ads-official-retrieval
description: Localiza e lê seletivamente a base local da Central de Ajuda, a documentação oficial do Google Ads e a Google Ads API. Use antes de responder sobre funcionamento, configuração, política, faturamento, campanhas, palavras-chave, lances, conversões, anúncios, assets, mensuração, otimização, MCP ou erros Google Ads.
---

# Recuperação Oficial Google Ads

## Fontes permitidas

1. Pesquisar `knowledge/official-google/help-center/INDEX.md` pela busca seletiva.
2. Ler integralmente somente os 1–3 documentos locais relevantes.
3. Para temas fora da cobertura local, ler `knowledge/official-google/source-catalog.md` e os resumos ainda vigentes.
4. Para informação atual, pesquisar e abrir páginas em:
   - `support.google.com/google-ads/`
   - `developers.google.com/google-ads/api/`
   - `github.com/googleads/google-ads-mcp`
   - `console.cloud.google.com/` somente para orientar a ação interativa do usuário no projeto correto.

## Processo

1. Preservar a pergunta original.
2. Identificar se o tema é interface/produto, API/MCP, política ou metodologia.
3. Para interface/produto, executar a partir da raiz:

```bash
python3 scripts/search_google_ads_help.py "pergunta original" --platform google_ads --limit 3
```

4. O buscador roda em modo híbrido por padrão: primeiro tenta correspondência de título; só quando o título for `related`/`weak` ele também considera um sinal semântico local (índice vetorial em `knowledge/.vector-index/`) para achar candidatos que a pergunta parafraseada não bateu por título. Correspondência `exact` ou `strong` exige leitura integral do primeiro documento, seja o sinal `lexical`, `vector` ou `hybrid`. Correspondência `related` permite abrir até três candidatos. Resultado `weak` não sustenta resposta sozinho. Se o índice vetorial não estiver construído localmente, o buscador cai automaticamente para o modo lexical de sempre, sem quebrar.
5. Abrir somente as 1–3 fontes mais aderentes e ler integralmente a seção necessária; não responder por snippet.
6. Verificar data, versão da API, elegibilidade e limitações por tipo de campanha.
7. Separar `Google informa` de `metodologia recomenda`.
8. Registrar título, caminho local, URL, data de extração e data de consulta no dossiê.

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
- O snapshot local é seletivo e não representa cobertura integral da Central.
- Não carregar todos os artigos como prevenção genérica.
- Não chamar o buscador sem `--platform google_ads`; consultas Meta devem falhar fechadas — o gate de plataforma vale igualmente para o sinal lexical e o vetorial, cada um com índice fisicamente separado por plataforma.
- Não afirmar que leu um artigo apenas porque o sinal vetorial encontrou similaridade; abrir e ler o arquivo indicado antes de responder.
- Não usar blog, fórum, fornecedor ou MCP comunitário como fonte normativa quando houver fonte oficial.
- Não afirmar disponibilidade de recurso na conta sem verificar via MCP/interface.
- Não transformar recomendação do Google em regra universal ou autorização de execução.
