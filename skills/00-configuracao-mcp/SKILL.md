---
name: 00-configuracao-mcp
description: Configura, diagnostica e valida com segurança o MCP oficial do Meta Ads no Claude Code ou Codex. Use quando o usuário disser /configuracao-mcp, instalar o agent, conectar Meta Ads, autenticar, corrigir MCP ou verificar permissões e ferramentas disponíveis.
---

# Configuração do MCP Meta Ads

## Objetivo

Separar transporte, autenticação, acesso à conta, leitura e escrita. Nunca tratar "conectado" como prova de capacidade operacional.

## Dados necessários

1. Ambiente: Claude Code ou Codex Desktop/CLI.
2. `CONTRATO-OPERACIONAL.md`, seções 10 e 11.
3. Endpoint `https://mcp.facebook.com/ads`.
4. Nome da conta desejada, se já conhecido.

## Fluxo Claude Code

1. Detectar `claude` sem alterar nada.
2. Executar `claude mcp get facebook-ads` ou `claude mcp list` sem expor configurações sensíveis.
3. Se ausente, explicar o comando a aplicar e pedir confirmação.
4. Após confirmação, usar `claude mcp add --transport http --scope user facebook-ads https://mcp.facebook.com/ads`.
5. Orientar OAuth e reinício da sessão quando necessário.

## Fluxo Codex

1. Identificar Desktop ou CLI.
2. Inspecionar somente `[mcp_servers.meta_ads]` em `~/.codex/config.toml`; nunca imprimir o arquivo completo.
3. Se ausente, apresentar exatamente a seção TOML e pedir confirmação antes de editar.
4. Reiniciar a sessão e verificar exposição real das ferramentas.
5. Se o CLI falhar, registrar a falha do binário separadamente do status do MCP.

## Validação

Verificar em ordem:

- Servidor responde.
- OAuth concluído.
- Contas acessíveis podem ser listadas.
- Conta correta pode ser lida.
- Moeda/timezone/ativos podem ser consultados.
- Ferramentas de escrita existem e a permissão do usuário é suficiente.

O teste deve ser somente leitura. Não criar, editar, pausar, publicar ou excluir nada.

## Dossiê

Criar dossiê de configuração local com ambiente, servidor, status, contas mascaradas, capacidades e horário. Omitir tokens, cookies, cabeçalhos, respostas OAuth e configurações de outros servidores.

## Gate final

- Leitura validada → modo consultivo liberado.
- Escrita detectada e autorizada → modo operacional elegível, ainda sujeito a change set e aprovação.
- Qualquer gate falhou → registrar limitação e não prometer execução.

