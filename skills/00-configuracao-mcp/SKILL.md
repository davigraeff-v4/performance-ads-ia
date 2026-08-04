---
name: 00-configuracao-mcp
description: Configura, diagnostica e valida com segurança o MCP oficial do Meta Ads ou do Google Ads no Claude Code ou Codex. Use em /configuracao-mcp, instalação do agent, conexão de plataforma, autenticação ou verificação de permissões e ferramentas.
---

# Configuração de MCPs de Mídia

## Gate de plataforma

1. Identificar `meta` ou `google_ads` antes de inspecionar configuração.
2. Se o pedido for ambíguo, perguntar qual plataforma; não configurar ambas.
3. Ler `CONTRATO-OPERACIONAL.md`, seção 12.

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

O servidor oficial é executado localmente a partir de `googleads/google-ads-mcp`. No V1, tratá-lo como somente leitura.

1. Ler `knowledge/official-google/google-ads-mcp-and-api.md` e o README atual do servidor oficial.
2. Verificar Python/pipx, Google Cloud project, Google Ads API, developer token e OAuth/ADC.
3. Confirmar `login-customer-id` quando houver manager account.
4. Apresentar a configuração com placeholders e pedir confirmação antes de editar arquivo local.
5. Nunca inserir credenciais no repositório; apontar para caminho local fora do projeto.
6. Reiniciar a sessão e validar `list_accessible_customers`, metadata e consulta de leitura.
7. Não testar escrita nem presumir suporte a Keyword Planner.

## Validação comum

Verificar separadamente transporte, autenticação, contas acessíveis, conta correta, moeda/timezone, leitura e ferramentas expostas. "Conectado" não prova acesso operacional.

## Sem MCP

Registrar `file_based` ou `context_only` e orientar exports/planilhas adequados. Ausência de MCP não bloqueia planejamento consultivo.

## Dossiê

Registrar plataforma, ambiente, servidor, status, contas mascaradas, capacidades e horário. Omitir tokens, cookies, chaves, JSONs, cabeçalhos, OAuth e configurações de outros servidores.
