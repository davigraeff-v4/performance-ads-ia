# PERFORMANCE ADS IA

Agente especialista em Meta Ads e Google Ads para planejar, analisar e otimizar campanhas com decisões rastreáveis, dados comerciais e aprovação versionada.

O agent roda em **Claude Code** e **Codex**, seleciona somente as plataformas e skills necessárias para cada demanda e registra auditorias, análises e mudanças em dossiês Markdown locais.

> Estado: V1 multicanal inicial. Meta Ads e Google Ads estão no escopo. Search Console, Google Trends e GA4 ficam para fases futuras. Dados, credenciais, MCPs locais e dossiês reais permanecem fora do Git.

## 1. O que o agent faz

- Identifica se a demanda envolve Meta Ads, Google Ads ou ambas.
- Trabalha com MCP somente leitura, exports/planilhas ou contexto manual.
- Cadastra cliente, contas, metas, restrições e fontes.
- Planeja campanhas de lead generation e e-commerce.
- Pesquisa e organiza palavras-chave Google Ads quando aplicável.
- Audita tracking, estrutura, termos, públicos, assets e performance.
- Propõe otimizações em lotes versionados.
- Executa somente mudanças suportadas, aprovadas e revalidadas.
- Registra antes, aprovação, execução e depois no mesmo dossiê.
- Consulta seletivamente a Central Meta e fontes oficiais Google Ads.

Não exclui nem arquiva ativos, não ativa recomendações automáticas e não executa mudanças silenciosas.

## 2. Como o roteamento funciona

Cada demanda define:

1. Intenção: configurar, planejar, criar, auditar, analisar, otimizar, relatar, aprovar, executar ou reverter.
2. Plataformas: `meta`, `google_ads`, ambas ou ainda indefinidas.
3. Fonte por plataforma:
   - `connected_read`: MCP/API somente leitura.
   - `file_based`: CSV, XLSX ou Google Sheets.
   - `context_only`: briefing e informações manuais.
   - `unavailable`: fonte necessária ausente.

O agent não percorre um fluxo fixo. Uma análise Google Ads não carrega as skills Meta; uma demanda multicanal abre os dois ramos e preserva fontes, contas e atribuições separadamente.

## 3. Requisitos

- macOS, Linux ou ambiente compatível com Claude Code/Codex.
- Python 3 e `pipx` somente para quem optar pelo MCP oficial Google Ads.
- Acesso autorizado à plataforma usada.
- Para a conexão opcional ao Google Ads: Google Cloud project, Google Ads API habilitada, developer token e OAuth/ADC.
- Para modo por arquivos: exports com período, timezone, definições e escopo.

## 4. Primeiro uso

Abra a raiz do projeto no Claude Code ou Codex e confirme a presença de:

- `AGENTS.md` ou `CLAUDE.md`.
- `CONTRATO-OPERACIONAL.md`.
- `dependency_graph.json`.
- `skills/`.

Depois escolha uma rota:

```text
/novo-cliente
```

```text
/planejar-campanha
Plataforma: Google Ads
```

```text
/analisar-campanha
Plataformas: Meta e Google Ads
```

## 5. Meta Ads MCP

Endpoint oficial usado pelo projeto:

```text
https://mcp.facebook.com/ads
```

Execute `/configuracao-mcp`, informe `Meta Ads` e siga a skill `00-configuracao-mcp`. O procedimento exige confirmação antes de editar configuração local e termina com teste somente leitura.

## 6. Google Ads MCP — opcional

O agent funciona normalmente sem MCP usando `file_based` ou `context_only`. A conexão ao Google Ads é opcional e serve apenas para leitura atual da conta.

Quem quiser instalar pode ignorar esta etapa no primeiro uso e consultar depois o [apêndice completo de instalação](#15-apêndice-opcional--google-ads-mcp-local), no final deste README.

Nenhuma credencial deve ser enviada em chats ou armazenada no repositório.

## 7. Usar sem MCP

O MCP é opcional. Sem conexão, informe `file_based` ou `context_only`.

### Google Ads — pacote mínimo

Exportar, quando a análise exigir:

- Campanhas.
- Grupos de anúncios.
- Investimento, impressões, cliques e conversões.
- Budget e estratégia de lance.
- Ações de conversão relevantes.

### Google Ads — pacote completo

- Palavras-chave.
- Termos de pesquisa.
- Negativas.
- Anúncios e assets.
- Landing pages.
- Parcela de impressões e perdas por budget/ranking.
- Dispositivo, rede, localização, data e horário.
- Histórico de alterações.
- Export do Keyword Planner.
- Dados comerciais/CRM.

### Contrato do arquivo

Informar junto:

- Plataforma e conta.
- Período e timezone.
- Nível do export.
- Modelo de atribuição.
- Definição das conversões.
- Se receita é bruta, líquida ou aprovada.
- Se duplicados, inválidos, cancelamentos ou reembolsos foram tratados.

Campo ausente permanece `null`; nunca vira zero.

## 8. Pesquisa de palavras-chave

Use:

```text
/pesquisar-palavras-chave
```

Informe oferta, geografia, idioma, rede, URLs/seeds e fonte. Modos aceitos:

- Keyword Planner/API disponível.
- Export do Keyword Planner.
- Termos/keywords atuais da conta.
- Apenas contexto e seeds.

Sem fonte oficial, o agent pode estruturar intenções, clusters, negativas, grupos e landing pages, mas deixa volume, CPC, concorrência e forecast indisponíveis.

## 9. Comandos

| Comando | Resultado |
|---|---|
| `/configuracao-mcp` | Diagnostica/configura o MCP da plataforma escolhida. |
| `/novo-cliente` | Cria ou atualiza a ficha operacional multicanal. |
| `/planejar-campanha` | Produz estratégia sem executar. |
| `/criar-campanha` | Produz plano e change set por plataforma. |
| `/pesquisar-palavras-chave` | Pesquisa intenção, clusters, match types e negativas. |
| `/auditar-conta` | Audita conta, mensuração, estrutura e riscos. |
| `/analisar-campanha` | Analisa performance do escopo. |
| `/otimizar-campanha` | Gera lote priorizado por plataforma. |
| `/relatorio-performance` | Gera relatório mono ou multicanal. |
| `/aprovar-operacao <id>` | Registra aprovação; não executa. |
| `/executar-operacao <id>` | Revalida e executa somente lote suportado. |
| `/reverter-operacao <id>` | Propõe restauração conhecida com nova aprovação. |

## 10. Catálogo das 25 skills

### Núcleo e Meta Ads

| Skill | Responsabilidade |
|---|---|
| `00-configuracao-mcp` | Configurar MCP da plataforma escolhida |
| `01-client-campaign-intake` | Cliente, plataformas, contas e briefing |
| `02-meta-account-connection` | Conta Meta |
| `03-measurement-data-quality` | Mensuração compartilhada |
| `04-goals-kpis-baseline` | Metas e baseline |
| `05-campaign-strategy` | Estratégia Meta |
| `06-account-campaign-architecture` | Arquitetura Meta |
| `07-audience-strategy` | Públicos Meta |
| `08-budget-bidding-allocation` | Budget e lances Meta |
| `09-creative-performance-brief` | Criativos Meta |
| `10-campaign-build-plan` | Construção Meta |
| `11-performance-diagnosis` | Diagnóstico Meta |
| `12-optimization-change-set` | Change set compartilhado |
| `13-approved-change-executor` | Executor aprovado |
| `14-reporting-memory-learning` | Relatório e memória |
| `15-meta-help-center-retrieval` | Fontes oficiais Meta |

### Google Ads

| Skill | Responsabilidade |
|---|---|
| `16-google-ads-account-connection` | Customer, manager e leitura |
| `17-google-ads-official-retrieval` | Fontes oficiais Google |
| `18-google-ads-keyword-research` | Keywords, intenções e negativas |
| `19-google-ads-campaign-strategy` | Tipo e estratégia da campanha |
| `20-google-ads-campaign-architecture` | Arquitetura por tipo |
| `21-google-ads-budget-bidding-conversions` | Budget, lances e conversões |
| `22-google-ads-creative-assets-landing-page` | Ads, assets e landing pages |
| `23-google-ads-campaign-build-plan` | Plano de construção Google |
| `24-google-ads-performance-diagnosis` | Diagnóstico Google |

## 11. Aprovação e execução

Análises multicanal podem compartilhar um dossiê, mas mutações usam um `operation_id` por plataforma. Aprovar Meta não aprova Google Ads e vice-versa.

No V1:

- Meta pode ser executado somente se escrita tiver sido homologada.
- Google Ads é sempre `manual_only`.
- Recomendações automáticas nunca são aplicadas por padrão.

## 12. Conhecimento

- Meta: snapshot seletivo de 151 artigos mais resumos operacionais.
- Google Ads: catálogo leve, resumos próprios e consulta oficial ao vivo.
- Metodologia: regras internas separadas das afirmações das plataformas.
- Aprendizados: somente padrões sanitizados e aprovados.

## 13. Validação local

```text
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests
```

O validador verifica 25 skills, grafo, comandos, schemas, base Meta e arquivos obrigatórios Google Ads.

## 14. Segurança e Git

Nunca versionar:

- Clientes e dossiês reais.
- CSV/XLSX/exports reais.
- `google-ads.yaml`.
- JSONs OAuth, ADC ou service account.
- Developer tokens e refresh tokens.
- Configuração local de MCP.
- Respostas de autenticação.

Antes de publicar, revisar `git status`, `git diff`, testes e auditoria de segredos. Push continua exigindo autorização explícita.

## 15. Apêndice opcional — Google Ads MCP local

O V1 usa o servidor oficial open source:

```text
https://github.com/googleads/google-ads-mcp
```

Ele é tratado como **somente leitura**. As ferramentas esperadas são listagem de customers, consultas GAQL e descoberta de metadata. Não presumir escrita nem Keyword Planner.

### 15.1 Regra de segurança antes de começar

Nunca cole developer token, client secret, refresh token, conteúdo de JSON OAuth ou configuração completa em chats, issues ou commits. Quando o agent ajudar na instalação, informe somente caminhos locais; ele deve inspecionar nomes de variáveis e presença dos arquivos, sem imprimir valores.

Use uma pasta fora do clone, por exemplo:

```text
~/.config/performance-ads-ia/google-ads/
```

Proteja a pasta e os arquivos:

```bash
chmod 700 ~/.config/performance-ads-ia/google-ads
chmod 600 ~/.config/performance-ads-ia/google-ads/*.json
chmod 600 ~/.config/performance-ads-ia/google-ads/*.env
```

Não use `clients/`, `skills/`, `knowledge/`, exemplos ou dossiês para armazenar credenciais. O `.gitignore` é uma segunda barreira, não um cofre.

### 15.2 O que será necessário

| Item | Onde obter | Obrigatório |
|---|---|---|
| Google Cloud project ID | Google Cloud Console | Sim |
| Google Ads API habilitada | API Library do projeto | Sim |
| Developer token | API Center de uma conta administradora Google Ads | Sim |
| OAuth Client ID e Client Secret, ADC ou service account | Google Cloud Console | Sim, conforme a rota |
| Refresh token | Fluxo OAuth de usuário | Somente na rota OAuth de usuário |
| Login customer ID | ID da MCC, sem hífens | Quando o acesso passa por MCC |
| `pipx` e Python 3.10+ | Sistema operacional | Sim |

O e-mail autorizado precisa ter acesso às contas Google Ads que serão consultadas. Ter um developer token não concede acesso às contas.

### 15.3 Criar o projeto e habilitar a API

1. Acesse a [configuração oficial do Google API Console](https://developers.google.com/google-ads/api/docs/oauth/cloud-project).
2. Crie ou selecione um projeto exclusivo ou já compatível com o developer token usado.
3. Abra a API Library, procure `Google Ads API` e clique em habilitar.
4. Anote o **Project ID**, não apenas o nome nem o número do projeto.
5. Não habilite billing apenas por causa da Google Ads API; a documentação oficial informa que billing é opcional para esse uso.

### 15.4 Obter o developer token

1. Entre em uma conta administradora Google Ads — MCC.
2. Abra o [API Center](https://ads.google.com/aw/apicenter).
3. Aceite os termos e preencha os dados solicitados, caso ainda não exista token.
4. Copie o developer token para o armazenamento local seguro.
5. Confira o nível de acesso: `Test Account`, `Explorer`, `Basic` ou `Standard`.

`Test Account Access` consulta somente contas de teste. Acesso a produção exige nível compatível. O Google normalmente associa o token a uma organização/projeto e pode exigir revisão. Consulte sempre as páginas atuais de [developer token](https://developers.google.com/google-ads/api/docs/api-policy/developer-token) e [níveis de acesso](https://developers.google.com/google-ads/api/docs/api-policy/access-levels).

### 15.5 Identificar MCC e customer

- O **customer ID** é a conta que será consultada.
- O **login customer ID** é a MCC usada como ponto de entrada quando o acesso é indireto.
- Grave ambos sem hífens: `1234567890`, nunca `123-456-7890`.
- Se o usuário OAuth acessa diretamente a conta, `GOOGLE_ADS_LOGIN_CUSTOMER_ID` pode ser omitido.
- Se o acesso passa por MCC, omitir ou usar a MCC errada pode causar `USER_PERMISSION_DENIED`.

Veja a explicação oficial de [`login-customer-id`](https://developers.google.com/google-ads/api/docs/concepts/call-structure#login-customer-id).

### 15.6 Escolher a autenticação

Use uma destas rotas:

#### Rota A — ADC já existente

Use quando você já possui um `application_default_credentials.json` válido e autorizado com o escopo:

```text
https://www.googleapis.com/auth/adwords
```

Copie o arquivo para a pasta local segura e avance para a instalação.

#### Rota B — OAuth de usuário sem Google Cloud CLI

Use quando você possui ou consegue criar um OAuth Client e prefere não instalar `gcloud`.

1. Configure a tela de consentimento OAuth do projeto.
2. Adicione o escopo `https://www.googleapis.com/auth/adwords`.
3. Se a aplicação estiver em modo de teste, adicione como test user o e-mail que acessa as contas Google Ads.
4. Crie uma credencial OAuth do tipo **Desktop app** e baixe o JSON.
5. Salve como `oauth-client.json` na pasta local segura.
6. Baixe o [arquivo Python oficial `generate_user_credentials.py`](https://github.com/googleads/google-ads-python/blob/main/examples/authentication/generate_user_credentials.py) e salve fora do repositório.
7. Prepare um ambiente isolado:

```bash
python3 -m venv ~/.config/performance-ads-ia/google-ads/oauth-venv
~/.config/performance-ads-ia/google-ads/oauth-venv/bin/pip \
  install google-auth-oauthlib
```

8. Execute o exemplo para abrir o consentimento no navegador:

```bash
~/.config/performance-ads-ia/google-ads/oauth-venv/bin/python \
  /CAMINHO/LOCAL/generate_user_credentials.py \
  --client_secrets_path \
  ~/.config/performance-ads-ia/google-ads/oauth-client.json
```

O script oficial usa o escopo Google Ads e devolve um refresh token após o consentimento. Consulte também a página [Generate user credentials](https://developers.google.com/google-ads/api/samples/generate-user-credentials). Se você usar OAuth Client do tipo Web, configure o redirect URI solicitado pelo exemplo; Desktop app é a rota mais simples para uso local.

9. Crie localmente `application_default_credentials.json` com esta estrutura:

```json
{
  "type": "authorized_user",
  "client_id": "SEU_OAUTH_CLIENT_ID",
  "client_secret": "SEU_OAUTH_CLIENT_SECRET",
  "refresh_token": "SEU_REFRESH_TOKEN"
}
```

Não publique nem envie esse arquivo. O refresh token pode ser revogado e deve ser gerado novamente quando aparecer `invalid_grant`.

#### Rota C — ADC com Google Cloud CLI

Use quando `gcloud` estiver disponível:

```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/adwords,https://www.googleapis.com/auth/cloud-platform \
  --client-id-file=/CAMINHO/LOCAL/oauth-client.json
```

O comando abre o navegador e informa o caminho do `application_default_credentials.json` gerado. Mantenha esse arquivo fora do repositório.

#### Rota D — service account

Use para automação institucional quando a organização preferir identidade não vinculada a uma pessoa. Crie a service account e o JSON no projeto, conceda o acesso necessário ao e-mail da service account na conta/MCC Google Ads e use o JSON como `GOOGLE_APPLICATION_CREDENTIALS`. Siga o [fluxo oficial de service account](https://developers.google.com/google-ads/api/docs/oauth/service-accounts) e aplique o menor nível de acesso possível.

### 15.7 Instalar o servidor oficial

Instale `pipx` conforme o sistema. Em macOS com Homebrew:

```bash
brew install pipx
```

Instale o pacote oficial uma vez:

```bash
pipx install git+https://github.com/googleads/google-ads-mcp.git
```

Confirme o executável:

```bash
pipx list
```

Para produção interna, registre a revisão Git homologada e faça upgrades somente após revisar as mudanças. Não execute atualização automática do MCP.

### 15.8 Criar um launcher compartilhado e sem segredos

O Claude e o Codex podem apontar para o mesmo launcher. Isso evita duplicar tokens nas configurações dos dois clientes.

Crie `~/.config/performance-ads-ia/google-ads/google-ads.env`:

```bash
GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/performance-ads-ia/google-ads/application_default_credentials.json"
GOOGLE_PROJECT_ID="SEU_PROJECT_ID"
GOOGLE_ADS_DEVELOPER_TOKEN="SEU_DEVELOPER_TOKEN"
GOOGLE_ADS_LOGIN_CUSTOMER_ID="SEU_MANAGER_CUSTOMER_ID_SEM_HIFENS"
```

Se não houver MCC, remova a última linha. Depois crie `~/.config/performance-ads-ia/google-ads/run-google-ads-mcp`:

```sh
#!/bin/sh
set -a
. "$HOME/.config/performance-ads-ia/google-ads/google-ads.env"
set +a
exec "$HOME/.local/bin/google-ads-mcp"
```

Proteja o launcher:

```bash
chmod 700 ~/.config/performance-ads-ia/google-ads/run-google-ads-mcp
```

Em instalações nas quais `pipx` publica o executável em outro local, substitua `~/.local/bin/google-ads-mcp` pelo caminho retornado por `pipx list` ou `command -v google-ads-mcp`.

### 15.9 Registrar no Claude Code

Abra o terminal na raiz deste repositório e registre com escopo local:

```bash
claude mcp add --scope local google_ads -- \
  "$HOME/.config/performance-ads-ia/google-ads/run-google-ads-mcp"
```

Verifique sem exibir credenciais:

```bash
claude mcp get google_ads
```

O resultado esperado é `Scope: Local`, transporte `stdio` e status conectado. O escopo local fica na configuração privada do Claude associada a este projeto, não no Git.

### 15.10 Registrar no Codex

Registre o launcher no Codex:

```bash
codex mcp add google_ads -- \
  "$HOME/.config/performance-ads-ia/google-ads/run-google-ads-mcp"
```

Verifique:

```bash
codex mcp get google_ads --json
```

O Codex registra MCPs em `~/.codex/config.toml`. Não mostre o arquivo completo: inspecione somente a entrada `google_ads`. Se o comando `codex` do shell não estiver disponível no macOS, use o binário fornecido pelo aplicativo instalado ou execute a configuração pela interface do Codex.

### 15.11 Reiniciar e homologar

Abra uma nova sessão no Claude Code e uma nova tarefa no Codex. Valide nesta ordem:

1. O processo do servidor inicia.
2. `customers_list_accessible_customers` lista customers sem mutação.
3. O customer correto é confirmado por nome, ID mascarado, moeda e timezone.
4. `metadata_get_resource_metadata` funciona para `customer` ou `campaign`.
5. `search_search` executa uma consulta GAQL pequena, com período e `limit`.
6. O dossiê registra horário, ferramentas, contas mascaradas e limitações.

Nunca faça uma mutação como teste. No V1, `connected_read` comprova somente leitura; mudanças Google Ads continuam `manual_only`.

### 15.12 Erros comuns

| Erro | Verificação segura |
|---|---|
| `GOOGLE_ADS_DEVELOPER_TOKEN environment variable not set` | Confirmar se o launcher carregou o arquivo local correto. |
| `DefaultCredentialsError` | Confirmar caminho, formato e permissão do ADC. |
| `invalid_grant` | Gerar nova autorização; o refresh token pode ter expirado ou sido revogado. |
| `USER_PERMISSION_DENIED` | Conferir usuário OAuth, customer alvo e login customer ID/MCC. |
| Token aprovado só para teste | Consultar o nível do developer token no API Center. |
| MCP conecta, mas não lista contas | Confirmar que o usuário/service account foi adicionado às contas corretas. |
| Processo desconecta | Confirmar Python 3.10+, `pipx list` e caminho absoluto do executável. |

### 15.13 Rotação ou remoção

Ao trocar credenciais, atualize somente os arquivos locais protegidos e reinicie as sessões. Para remover os registros:

```bash
claude mcp remove google_ads -s local
codex mcp remove google_ads
```

Não apague credenciais ou revogue acessos automaticamente. Confirme o alvo e a necessidade antes de qualquer ação destrutiva.
