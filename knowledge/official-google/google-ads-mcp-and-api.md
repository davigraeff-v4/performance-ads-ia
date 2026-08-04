# MCP Oficial e Google Ads API

- **verificado_em:** 2026-08-04
- **fontes:**
  - https://github.com/googleads/google-ads-mcp
  - https://developers.google.com/google-ads/api/docs/oauth/credential-management
  - https://developers.google.com/google-ads/api/docs/api-policy/developer-token

## Capacidades V1

O MCP oficial expõe listagem de customers, consultas GAQL e descoberta de metadata/resources. Ele exige developer token, Google Cloud, credencial OAuth/ADC e `login-customer-id` quando o acesso ocorre por manager account.

Neste projeto, o MCP é somente leitura. Geração de ideias e forecasts do Keyword Planner não deve ser presumida como ferramenta do MCP; usar export fornecido ou integração futura homologada.

## Segurança

- Manter tokens, JSONs, `google-ads.yaml` e configuração real fora do Git.
- Validar transporte, autenticação, customer e leitura separadamente.
- Não testar escrita.
- Não expor IDs integrais quando a apresentação puder usar máscara.
