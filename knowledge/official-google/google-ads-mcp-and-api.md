# MCP Oficial e Google Ads API

- **verificado_em:** 2026-08-04
- **fontes:**
  - https://github.com/googleads/google-ads-mcp
  - https://developers.google.com/google-ads/api/docs/oauth/credential-management
  - https://developers.google.com/google-ads/api/docs/api-policy/developer-token

## Capacidades V1

O MCP oficial expõe listagem de customers, consultas GAQL e descoberta de metadata/resources. Ele exige developer token, Google Cloud, credencial OAuth/ADC e `login-customer-id` quando o acesso ocorre por manager account.

Neste projeto, o MCP oficial é somente leitura. Geração de ideias e forecasts do Keyword Planner não deve ser presumida como ferramenta do MCP oficial.

O complemento local `google_ads_extended` é um processo separado. Na V1.1 inicial ele expõe diagnóstico sanitizado de capacidades e um adapter de `KeywordPlanIdeaService`, bloqueado por padrão. Planner exige uso permitido compatível no API Center, flag local explícito e customer allowlisted. Não existem ferramentas de escrita registradas nesta etapa.

## Componentes da autenticação

- **Google Cloud project:** hospeda as credenciais OAuth e precisa ter a Google Ads API habilitada.
- **Developer token:** identifica o aplicativo e define o nível de acesso à API; não concede acesso às contas.
- **Identidade OAuth ou service account:** precisa ter acesso real às contas Google Ads consultadas.
- **ADC:** arquivo carregado por `GOOGLE_APPLICATION_CREDENTIALS`; pode representar usuário autorizado ou service account.
- **Login customer ID:** MCC usada no cabeçalho de acesso indireto, sem hífens; não é necessariamente a conta alvo.

## Rotas homologadas

1. ADC existente com escopo `https://www.googleapis.com/auth/adwords`.
2. OAuth Desktop e refresh token gerado pelo exemplo oficial, convertido localmente em ADC `authorized_user`.
3. ADC criado por `gcloud auth application-default login`.
4. Service account com acesso concedido na conta/MCC.

Google Workspace CLI não substitui o MCP Google Ads nem comprova o escopo `adwords`.

## Instalação compartilhada

Preferir `pipx install` e um launcher local fora do repositório. Claude Code e Codex podem apontar para o mesmo launcher, evitando duplicação de segredos. No Claude, usar escopo local do projeto; no Codex, inspecionar somente a entrada global `google_ads`.

## Segurança

- Manter tokens, JSONs, `google-ads.yaml` e configuração real fora do Git.
- Reutilizar o bundle local por launcher; nunca copiar o developer token para o código do complemento.
- Não usar uma chamada de Planner ou mutate como teste de permissão quando o uso permitido registrado for somente relatórios.
- Nunca pedir que o usuário envie credenciais em chat; trabalhar com caminhos locais e placeholders.
- Proteger diretório local com `0700` e arquivos secretos com `0600`.
- Copiar somente credenciais Google Ads quando a fonte local contiver segredos de outros serviços.
- Validar transporte, autenticação, customer e leitura separadamente.
- Não testar escrita.
- Não expor IDs integrais quando a apresentação puder usar máscara.
