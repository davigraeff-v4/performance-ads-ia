# Servidor de escrita do Google Ads (googleAdsServer)

Servidor MCP que deixa o Claude ler **e alterar** contas do Google Ads, em qualquer projeto e no Claude Desktop. É o que a seção 8.1 do `CONTRATO-OPERACIONAL.md` chama de `googleAdsServer`: sem ele, o agent trata toda mudança no Google Ads como manual.

Base: o projeto aberto [cohnen/mcp-google-ads](https://github.com/cohnen/mcp-google-ads) (licença MIT), num commit fixo, mais os ajustes desta pasta. Nada aqui contém credencial, ID de conta ou dado de cliente.

## Como funciona

O Google não tem login de API só para leitura. O escopo OAuth do Google Ads (`adwords`) cobre ler e alterar, e quem decide se dá para alterar é o seu nível de acesso em cada conta:

| Nível na conta ou MCC | O que a API deixa fazer |
|---|---|
| Administrador | ler, alterar e gerenciar usuários |
| Padrão | ler e alterar |
| Somente leitura | só ler |
| Somente e-mail | nada |

Numa MCC, o nível vale para todas as contas ligadas a ela. Cada chamada leva quatro peças: o login OAuth (com `refresh_token`), o developer token, a MCC de entrada (`login-customer-id`) e a conta alvo. Se o seu usuário pode alterar aquela conta por aquela MCC, o Google aceita.

## O que você precisa antes

1. **Acesso às contas**, de preferência como Administrador ou Padrão numa MCC.
2. **Developer token** em nível Explorer, Básico ou Padrão, pego na Central de API da MCC (Ferramentas → Configuração → Central de API). O nível "Acesso de teste" só funciona em contas de teste. O token não precisa ser da mesma MCC das contas.
3. **Projeto no Google Cloud** com a Google Ads API ativada e um client OAuth. Pode ser "App para computador" (mais simples) ou "Aplicativo da Web", com o redirect `http://localhost:8085` cadastrado. Em modo "Teste", inclua o seu e-mail como testador.
4. **Na máquina:** Git e Python 3.11 ou mais novo.

Se você já usa o conector oficial `google_ads` deste projeto, as peças 2 e 3 já existem. O token de lá (`application_default_credentials.json`, tipo `authorized_user`) pode ser copiado como `google_ads_token.json` em vez de gerar um novo.

## Instalação

```bash
bash integrations/google_ads_write_server/install.sh
```

O script instala em `~/.mcp/google-ads`, fora do repositório, e faz o seguinte:

1. Baixa o servidor original no commit testado.
2. Aplica os ajustes descritos abaixo.
3. Cria o ambiente Python.
4. Cria `.env` e `allowed_accounts.json` vazios, com permissão 600.

Ele não pede nem lê credencial. Rodar de novo atualiza o código e preserva os seus arquivos.

Depois, em ordem:

1. **Token OAuth**, se ainda não tiver:
   ```bash
   ~/.mcp/google-ads/.venv/bin/python ~/.mcp/google-ads/gerar_token.py --client-secrets /caminho/credentials.json
   ```
   Para client do tipo Web, acrescente `--port 8085`. Logue com o usuário que tem acesso às contas.
2. **`.env`** em `~/.mcp/google-ads/.env`: developer token, MCC padrão e caminho absoluto do token. Deixe `GOOGLE_ADS_WRITE_MODE=validate_only` por enquanto.
3. **Registrar no Claude Code**, para todos os projetos:
   ```bash
   claude mcp add-json -s user googleAdsServer '{"type":"stdio","command":"/Users/SEU_USUARIO/.mcp/google-ads/.venv/bin/python","args":["/Users/SEU_USUARIO/.mcp/google-ads/google_ads_server.py"],"env":{}}'
   ```
   No Claude Desktop, o mesmo bloco, sem `"type"`, vai em `mcpServers` de `~/Library/Application Support/Claude/claude_desktop_config.json`. Use caminhos absolutos. Os segredos ficam só no `.env`, nunca nesses arquivos.
4. **Reiniciar o Claude** e conferir a conexão com `claude mcp get googleAdsServer`.
5. **Lista de contas.** Peça ao Claude `list_accounts` e, para cada MCC, uma consulta `SELECT customer_client.id, customer_client.descriptive_name FROM customer_client`. Preencha `~/.mcp/google-ads/allowed_accounts.json` com as contas que podem ser alteradas, cada uma com a MCC por onde se entra nela.
6. **Testar sem gravar.** Peça para validar, em uma conta da lista, a pausa de uma campanha que já está ativa. As ferramentas começam em `validate_only=true`, então nada muda. Resposta com `ok: true` prova que login, developer token, MCC e nível de acesso permitem alterar.
7. **Liberar a gravação.** Troque para `GOOGLE_ADS_WRITE_MODE=execute` no `.env`. O arquivo é lido quando o servidor inicia, então reinicie o Claude.

## Ferramentas

As 12 ferramentas de leitura do projeto original continuam lá: `list_accounts`, `run_gaql`, `get_campaign_performance` e as demais. Esta instalação acrescenta:

| Ferramenta | Para quê |
|---|---|
| `list_allowed_accounts` | modo de escrita, contas permitidas e MCC de cada uma |
| `gaql_search` | GAQL em JSON, escolhendo a MCC de entrada sozinho |
| `get_change_history` | histórico de alterações, para conferir o que foi gravado |
| `set_status` | pausar ou ativar campanha, grupo, anúncio, palavra-chave ou grupo de recursos |
| `update_campaign_budget` | orçamento diário em reais, mostrando antes → depois |
| `add_keywords`, `add_negative_keywords` | palavras-chave e negativas |
| `mutate` | qualquer recurso da API (`campaigns`, `adGroupAds`, `assets`...) |
| `mutate_multi` | várias operações numa chamada, como criar campanha inteira |

## Travas

- Toda ferramenta de escrita começa em `validate_only=true`. Gravar exige chamar de novo com `false`.
- `GOOGLE_ADS_WRITE_MODE`: `execute`, `validate_only` (nunca grava) ou `disabled`.
- Conta fora de `allowed_accounts.json` é lida, mas não alterada.
- Exclusão (`remove` ou status `REMOVED`) é bloqueada. O contrato do agent proíbe ligar `GOOGLE_ADS_ALLOW_REMOVE`.
- Orçamento compartilhado entre campanhas só muda com `allow_shared_budget=true`.
- Toda chamada de escrita fica em `~/.mcp/google-ads/logs/mutations.jsonl`.

No agent, a gravação só acontece dentro de `/executar-operacao`, depois de `/aprovar-operacao` (contrato, seção 8.1).

## Ajustes feitos no servidor original (`patch_server.py`)

| Problema | Ajuste |
|---|---|
| API v19 foi desligada (erro 404) | versão v26, configurável por `GOOGLE_ADS_API_VERSION` |
| `mcp` 2.x quebra o código (`FastMCP` foi renomeado) | `mcp>=1.27,<2` |
| token sem data de expiração nunca era renovado | renova sempre que houver `refresh_token` |
| login pelo navegador abria dentro do Claude e travava o servidor | bloqueado; use `gerar_token.py` |
| `.env` dependia da pasta de onde o Claude abre o processo | lido ao lado do servidor |
| sem ferramentas de escrita | `write_tools.py` |

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `USER_PERMISSION_DENIED` numa conta que você acessa | MCC de entrada errada | corrigir `login_customer_id` da conta em `allowed_accounts.json` |
| `DEVELOPER_TOKEN_NOT_APPROVED` | token em acesso de teste | pedir nível Explorer ou Básico na Central de API |
| `redirect_uri_mismatch` ao gerar token | client Web sem a porta cadastrada | `--port 8085` e o redirect cadastrado no Google Cloud |
| `invalid_grant` | token revogado ou expirado (app em modo Teste expira em 7 dias) | gerar o token de novo; publicar o app OAuth evita a expiração |
| custo com valores enormes | valores em micros | dividir por 1.000.000 |
| Performance Max "some" | não aparece em `FROM ad_group_ad` | consultar `FROM campaign` |

## Segurança

- `.env`, `google_ads_token.json` e `allowed_accounts.json` ficam com permissão 600, fora de qualquer repositório. Nunca envie por chat ou e-mail.
- Com o `refresh_token`, qualquer programa que rode com o seu usuário consegue ler e alterar as contas.
- Para revogar: remova o app em myaccount.google.com/permissions ou apague o token. Isso corta também a leitura.
