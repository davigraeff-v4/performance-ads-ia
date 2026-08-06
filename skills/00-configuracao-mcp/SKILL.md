---
name: 00-configuracao-mcp
description: Configura, diagnostica e valida com segurança o MCP oficial do Meta Ads ou do Google Ads no Claude Code ou Codex. Use em /configuracao-mcp, instalação do agent, conexão de plataforma, autenticação ou verificação de permissões e ferramentas.
---

# Configuração de MCPs de Mídia

## Gate de plataforma

1. Identificar `meta` ou `google_ads` antes de inspecionar configuração.
2. Se o pedido for ambíguo, perguntar qual plataforma; não configurar ambas.
3. Ler `CONTRATO-OPERACIONAL.md`, seção 12.

## Gate de credenciais

1. Nunca pedir que o usuário cole segredo, token ou conteúdo de JSON no chat.
2. Aceitar somente caminhos locais e, quando necessário, inspecionar nomes de variáveis, existência, formato e permissões sem imprimir valores.
3. Se a fonte contiver credenciais de outras plataformas, copiar somente as chaves necessárias ao MCP solicitado.
4. Manter credenciais fora do repositório e proteger diretórios com `0700` e arquivos secretos com `0600`.
5. Mostrar comandos e configurações somente com placeholders.
6. Pedir confirmação antes de instalar pacote, editar configuração local ou iniciar OAuth.

## Meta Ads

### Claude Code

1. Executar `claude mcp get facebook-ads` ou `claude mcp list` sem expor segredos.
2. Se ausente, explicar o comando e pedir confirmação.
3. Após confirmação, usar o endpoint oficial `https://mcp.facebook.com/ads`.
4. Orientar OAuth e reinício quando necessário.

### Codex

1. Inspecionar somente `[mcp_servers.meta_ads]` em `~/.codex/config.toml`.
2. Se ausente, apresentar a seção TOML e pedir confirmação antes de editar.
3. Reiniciar a sessão e verificar ferramentas.

## Google Ads

O servidor oficial é executado localmente a partir de `googleads/google-ads-mcp` e permanece somente leitura. O conector `google_ads_extended` roda em processo separado e nunca amplia capacidade apenas porque está instalado.

### Fontes obrigatórias

1. Ler `knowledge/official-google/google-ads-mcp-and-api.md` e `knowledge/official-google/source-catalog.md`.
2. Abrir o README atual do servidor oficial.
3. Para criação de credencial, developer token, nível de acesso ou `login-customer-id`, abrir a página oficial específica no momento da instalação.

### Diagnóstico inicial

1. Verificar Python 3.10+, `pipx`, Claude Code e Codex sem instalar nada.
2. Inspecionar somente as entradas `google_ads` e, quando fizer parte do pedido, `google_ads_extended` em cada cliente.
3. Identificar o material disponível sem ler ou imprimir valores:
   - ADC `authorized_user`;
   - OAuth Client JSON e refresh token;
   - service account JSON;
   - developer token;
   - Google Cloud project ID;
   - MCC/login customer ID, quando aplicável.
4. Confirmar que a Google Ads API está habilitada e que a identidade OAuth/service account tem acesso às contas.
5. Se faltar uma credencial, orientar o apêndice opcional da seção 15 do `README.md` antes de editar configurações.
6. Para o conector complementar, chamar primeiro `get_extended_capabilities`; nunca inferir Planner ou escrita pelo nível Basic isolado.

### Obtenção das credenciais

1. Orientar criar/selecionar o Google Cloud project e habilitar `Google Ads API`.
2. Orientar obter o developer token no API Center de uma MCC e conferir se o nível permite contas de produção.
3. Orientar identificar customer e MCC; normalizar IDs removendo hífens.
4. Selecionar uma rota:
   - ADC existente com escopo `https://www.googleapis.com/auth/adwords`;
   - OAuth Desktop + exemplo oficial `Generate user credentials`, sem `gcloud`;
   - `gcloud auth application-default login` com o escopo Google Ads;
   - service account com acesso concedido na conta/MCC.
5. Na rota OAuth sem `gcloud`, orientar ambiente virtual isolado, `google-auth-oauthlib` e o exemplo oficial `generate_user_credentials.py`; gerar localmente um ADC `authorized_user` contendo apenas `type`, `client_id`, `client_secret` e `refresh_token`, sem imprimir o arquivo.
6. Não reutilizar silenciosamente token do Google Workspace: Google Workspace CLI e Google Ads API são superfícies diferentes e podem usar escopos diferentes.

### Instalação local

1. Apresentar o plano com placeholders e pedir confirmação.
2. Instalar `pipx` somente após confirmação.
3. Instalar `googleads/google-ads-mcp` com `pipx install`; registrar a revisão Git homologada e não configurar atualização automática.
4. Criar o bundle em `~/.config/performance-ads-ia/google-ads/` ou caminho equivalente fora do clone.
5. Preferir um launcher local compartilhado que carregue `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_PROJECT_ID`, `GOOGLE_ADS_DEVELOPER_TOKEN` e, se necessário, `GOOGLE_ADS_LOGIN_CUSTOMER_ID`.
6. Fazer Claude e Codex apontarem para o launcher; não duplicar tokens nas configurações quando isso puder ser evitado.
7. Instalar o complemento em namespace separado, com capabilities `reporting`, Planner `false`, escrita `disabled` e allowlist vazia por padrão.

### Claude Code

1. Executar na raiz do projeto:

```text
claude mcp add --scope local google_ads -- /CAMINHO/LOCAL/run-google-ads-mcp
```

2. Verificar com `claude mcp get google_ads` sem exibir ambientes completos.
3. Confirmar escopo `local`, transporte `stdio` e processo conectado.

### Codex

1. Registrar:

```text
codex mcp add google_ads -- /CAMINHO/LOCAL/run-google-ads-mcp
```

2. Inspecionar somente `google_ads` com `codex mcp get google_ads --json`.
3. Se o shim `codex` falhar no macOS, localizar o binário do aplicativo instalado; não alterar outras entradas MCP.
4. Explicar que o registro atual do Codex é local ao usuário e pode ficar disponível em outros diretórios, enquanto o roteamento especializado pertence a este agent.

### Homologação

1. Abrir nova sessão/tarefa depois de alterar configuração.
2. Validar, nesta ordem:
   - transporte;
   - autenticação;
   - `customers_list_accessible_customers`;
   - customer correto, ID mascarado, moeda e timezone;
   - `metadata_get_resource_metadata`;
   - `search_search` com GAQL pequena e limitada.
3. Se houver mais de uma conta plausível, marcar `ambiguous` e pedir confirmação.
4. Nunca testar escrita, criar objeto descartável ou presumir suporte ao Keyword Planner.
5. No complemento, validar somente transporte e `get_extended_capabilities` enquanto o uso permitido for relatórios. Não chamar Planner para sondar autorização.

### Falhas e reversão de configuração

- `DefaultCredentialsError`: revisar caminho/formato do ADC.
- `invalid_grant`: renovar a autorização OAuth.
- `USER_PERMISSION_DENIED`: revisar usuário, customer e MCC/login customer ID.
- Token limitado a teste: revisar o nível no API Center.
- Processo desconectado: revisar Python, instalação `pipx` e caminho absoluto do executável.
- Para remover registros, usar `claude mcp remove google_ads -s local` e `codex mcp remove google_ads` somente após confirmação.
- Nunca apagar credenciais ou revogar acesso como parte implícita da remoção do MCP.

## Validação comum

Verificar separadamente transporte, autenticação, contas acessíveis, conta correta, moeda/timezone, leitura e ferramentas expostas. "Conectado" não prova acesso operacional.

## Sem MCP

Registrar `file_based` ou `context_only` e orientar exports/planilhas adequados. Ausência de MCP não bloqueia planejamento consultivo.

## Dossiê

Registrar plataforma, ambiente, servidor/revisão, status por cliente MCP, contas mascaradas, capacidades, fonte oficial e horário. Omitir tokens, cookies, chaves, JSONs, cabeçalhos, OAuth e configurações de outros servidores.
