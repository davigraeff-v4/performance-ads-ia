# PERFORMANCE ADS IA

Agente especialista em Meta Ads e Google Ads para planejar, analisar e otimizar campanhas com decisões rastreáveis, dados comerciais e aprovação versionada.

O agent roda em **Claude Code** e **Codex**, entende solicitações em linguagem natural, seleciona e executa automaticamente somente as skills necessárias, entrega primeiro no chat e registra apenas versões editorialmente aprovadas em dossiês Markdown locais.

> Estado: V1.4 local com diagnóstico `full` por padrão, cobertura por nível, pacote de evidências e fluxo chat-first com aprovação editorial antes do dossiê. O MCP oficial Google Ads continua somente leitura; o complemento `google_ads_extended` e a integração GTM permanecem fail-closed conforme os gates documentados. Search Console, Google Trends e GA4 ficam para fases futuras. Dados, credenciais, MCPs/API locais e dossiês reais permanecem fora do Git.

## 1. O que o agent faz

- Identifica se a demanda envolve Meta Ads, Google Ads ou ambas.
- Trabalha com MCP oficial somente leitura, complemento local condicionado, exports/planilhas ou contexto manual.
- Cadastra cliente, contas, metas, restrições e fontes.
- Planeja campanhas de lead generation e e-commerce.
- Pesquisa e organiza palavras-chave Google Ads quando aplicável.
- Audita tracking, estrutura, termos, públicos, assets e performance; quando o cliente rastreia via Google Tag Manager, audita e corrige tags/triggers/variáveis diretamente pela API do GTM (sem publicar).
- Propõe otimizações em lotes versionados.
- Executa somente mudanças suportadas, aprovadas e revalidadas.
- Analisa todas as camadas aplicáveis ou declara explicitamente indisponibilidade/insuficiência.
- Entrega o relatório completo no chat, itera e só cria o dossiê após aprovação editorial.
- Registra no dossiê aprovado diagnóstico, plano, aprovação operacional, execução e depois.
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

O agent não percorre um fluxo fixo. A skill pública `25-performance-ads-router`, descoberta automaticamente pelas pastas `.agents/skills/` e `.claude/skills/`, classifica a demanda e consulta `routing_matrix.json`. Uma análise Google Ads não carrega as skills Meta; uma demanda multicanal abre os dois ramos e preserva fontes, contas e atribuições separadamente. O gestor não precisa mencionar nomes de skills.

## 3. Requisitos

- macOS, Linux ou ambiente compatível com Claude Code/Codex.
- Python 3 e `pipx` somente para quem optar pelo MCP oficial Google Ads.
- Acesso autorizado à plataforma usada.
- Para a conexão opcional ao Google Ads: Google Cloud project, Google Ads API habilitada, developer token e OAuth/ADC.
- Para a conexão opcional ao Google Tag Manager: Google Cloud project com Tag Manager API habilitada e OAuth Client (Desktop app) — ver [apêndice de instalação](#16-apêndice-opcional--google-tag-manager-gtm).
- Para modo por arquivos: exports com período, timezone, definições e escopo.

## 4. Primeiro uso

### 4.1 Instalar (clonar o repositório)

Para outro gestor usar o agent, clone o repositório numa pasta local da máquina dele:

```bash
git clone https://github.com/davigraeff-v4/performance-ads-ia.git
cd performance-ads-ia
```

Pré-requisitos: `git` instalado e Claude Code ou Codex configurado na máquina. Não é necessário instalar nenhum pacote Python pra uso básico — `pip install -r requirements-dev.txt` só é necessário para quem for rodar a validação local (seção 13) ou reconstruir o índice vetorial (seção 12).

Cada gestor deve manter seu próprio clone local, já que `clients/`, dossiês e credenciais reais nunca são versionados (seção 14) — eles ficam só na máquina de quem os criou, nunca sincronizados automaticamente entre clones.

### 4.2 Abrir o projeto

Abra a raiz do projeto no Claude Code ou Codex e confirme a presença de:

- `AGENTS.md` ou `CLAUDE.md`.
- `CONTRATO-OPERACIONAL.md`.
- `dependency_graph.json`.
- `routing_matrix.json`.
- `skills/`.

O roteador público já está exposto em `.agents/skills/25-performance-ads-router` e `.claude/skills/25-performance-ads-router`. Depois de instalar ou atualizar esta estrutura, reinicie a sessão do Codex/Claude Code para renovar a descoberta de skills.

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

Comandos são atalhos. A mesma execução deve ocorrer com pedidos naturais como: “analise a campanha Search do cliente X usando o export e me diga o que fazer”.

## 5. Meta Ads MCP

Endpoint oficial usado pelo projeto:

```text
https://mcp.facebook.com/ads
```

Execute `/configuracao-mcp`, informe `Meta Ads` e siga a skill `00-configuracao-mcp`. O procedimento exige confirmação antes de editar configuração local e termina com teste somente leitura.

## 6. Google Ads MCP — opcional

O agent funciona normalmente sem MCP usando `file_based` ou `context_only`. O MCP oficial Google Ads serve para leitura atual da conta. O complemento local é opcional, separado e não amplia permissões automaticamente.

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

No complemento, `planner_connected` exige três evidências: uso permitido compatível no API Center, customer na allowlist local e chamada real bem-sucedida. Basic Access isoladamente não comprova Planner.

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

## 10. Catálogo das 27 skills

### Entrada pública

| Skill | Responsabilidade |
|---|---|
| `25-performance-ads-router` | Entender a demanda, resolver a rota, executar skills internas e entregar no chat |

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

O fluxo possui três gates distintos:

1. **Aprovação editorial:** autoriza registrar no dossiê a versão integral já mostrada no chat. Não aprova mídia.
2. **`/aprovar-operacao <id>`:** aprova a versão/hash do change set persistido. Não executa.
3. **`/executar-operacao <id>`:** executa somente quando a integração e as permissões foram homologadas.

Sem aprovação editorial, a entrega permanece `awaiting_record_approval` no chat e nenhum dossiê novo é criado.

Na V1.1 inicial:

- Meta pode ser executado somente se escrita tiver sido homologada.
- Google Ads permanece `manual_only`; o complemento ainda não registra ferramentas de escrita.
- Recomendações automáticas nunca são aplicadas por padrão.

## 12. Conhecimento

- Meta: snapshot seletivo de 151 artigos mais resumos operacionais.
- Google Ads: base seletiva da Central de Ajuda, fontes de API e consulta oficial ao vivo.
- Metodologia: regras internas separadas das afirmações das plataformas.
- Aprendizados: somente padrões sanitizados e aprovados.
- Busca híbrida (V1.2): a recuperação sobre as duas bases de Central de Ajuda combina busca lexical por título (padrão, determinística) com um sinal semântico local (embeddings via `fastembed`, sem PyTorch, sem chamada externa) que entra em ação só quando o título não bater — cobre perguntas parafraseadas sem perder a garantia de leitura integral em match forte. Índice em `knowledge/.vector-index/` (versionado no Git — ~2.6MB, o time recebe o RAG pronto no clone/pull — regenerável, isolado por plataforma, nunca indexa `clients/`; `scripts/validate_repository.py` detecta se ficou desatualizado em relação aos `.md` fonte).

Para (re)construir o índice vetorial localmente (só necessário depois de editar artigos, ou se `validate_repository.py` acusar desatualização):

```text
python3 scripts/build_knowledge_vector_index.py --platform all
```

Sem esse passo, a busca cai automaticamente para o modo lexical original — não é obrigatório para o agent funcionar.

## 13. Validação local

```text
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_all.py
```

O comando único verifica 26 módulos mais o roteador, descoberta nas duas plataformas, matriz e grafo, schemas acionáveis, cobertura diagnóstica, aprovação editorial, rastreabilidade evidência→achado→ação→mudança, isolamento do RAG e conectores fail-closed. Não realiza mutações externas.

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

### 15.12 Complemento local experimental

O diretório `integrations/google_ads_extended/` contém um segundo servidor MCP, separado do oficial. Ele reutiliza localmente o mesmo ADC, developer token e login customer ID, sem copiar valores para o repositório.

Instale em ambiente isolado:

```bash
pipx install --editable /CAMINHO/DO/REPOSITORIO/integrations/google_ads_extended
```

O launcher deve começar com esta política local:

```text
PERFORMANCE_ADS_GOOGLE_DECLARED_CAPABILITIES=reporting
PERFORMANCE_ADS_GOOGLE_PLANNER_ENABLED=false
PERFORMANCE_ADS_GOOGLE_WRITE_MODE=disabled
PERFORMANCE_ADS_GOOGLE_ALLOWED_CUSTOMER_IDS=
```

Registre o mesmo launcher nos dois clientes sob o namespace `google_ads_extended`. Reinicie as sessões e chame primeiro `get_extended_capabilities`. O retorno inicial esperado inclui `planner_enabled: false`, `write_mode: disabled` e `write_tools_registered: false`.

Somente depois da ampliação formal do uso permitido para pesquisa de keywords, configure localmente:

```text
PERFORMANCE_ADS_GOOGLE_DECLARED_CAPABILITIES=reporting,keyword_planning
PERFORMANCE_ADS_GOOGLE_PLANNER_ENABLED=true
PERFORMANCE_ADS_GOOGLE_ALLOWED_CUSTOMER_IDS=SEU_CUSTOMER_ID_SEM_HIFENS
```

Não habilite Planner para sondar autorização. Escrita não pode ser habilitada por variável nesta versão porque nenhuma ferramenta de mutação foi registrada.

### 15.13 Erros comuns

| Erro | Verificação segura |
|---|---|
| `GOOGLE_ADS_DEVELOPER_TOKEN environment variable not set` | Confirmar se o launcher carregou o arquivo local correto. |
| `DefaultCredentialsError` | Confirmar caminho, formato e permissão do ADC. |
| `invalid_grant` | Gerar nova autorização; o refresh token pode ter expirado ou sido revogado. |
| `USER_PERMISSION_DENIED` | Conferir usuário OAuth, customer alvo e login customer ID/MCC. |
| Token aprovado só para teste | Consultar o nível do developer token no API Center. |
| MCP conecta, mas não lista contas | Confirmar que o usuário/service account foi adicionado às contas corretas. |
| Processo desconecta | Confirmar Python 3.10+, `pipx list` e caminho absoluto do executável. |

### 15.14 Rotação ou remoção

Ao trocar credenciais, atualize somente os arquivos locais protegidos e reinicie as sessões. Para remover os registros:

```bash
claude mcp remove google_ads -s local
codex mcp remove google_ads
```

Não apague credenciais ou revogue acessos automaticamente. Confirme o alvo e a necessidade antes de qualquer ação destrutiva.

## 16. Apêndice opcional — Google Tag Manager (GTM)

### 16.1 Como funciona

Diferente do Google Ads, o GTM **não usa servidor MCP**. É um cliente Python local (`integrations/gtm/`) que fala diretamente com a API oficial (`tagmanager.googleapis.com`) via OAuth. A skill `26-gtm-tracking-audit-fix` chama dois scripts:

- `scripts/gtm_audit.py` — somente leitura: lista contas, containers e tira um snapshot de tags/triggers/variáveis de um workspace.
- `scripts/gtm_edit.py` — cria/edita tag, trigger ou variável **em rascunho de workspace**, só depois de um change set aprovado (`/aprovar-operacao` → `/executar-operacao`).

Garantias fixas no código, não apenas em configuração:

- **Nunca publica.** O escopo OAuth solicitado nunca inclui `tagmanager.publish` e não existe função de publish/versão em `integrations/gtm/src/performance_ads_gtm/` — testado em `integrations/gtm/tests/test_no_publish.py`. Levar uma mudança ao ar continua sendo um passo manual do gestor/responsável técnico na UI do GTM.
- **Leitura por padrão, escrita fail-closed.** `reporting` funciona sem nenhuma allowlist. Criar/editar exige três coisas ao mesmo tempo: `PERFORMANCE_ADS_GTM_WRITE_MODE != disabled`, a capability `tag_management` declarada e o `container_id` alvo na allowlist local. Faltando qualquer uma, o item vira `manual_only`.
- **Credenciais nunca no Git.** Client secret OAuth e token cacheado ficam em `credentials/` (ignorado pelo `.gitignore`); toda configuração fica em `.env` local (também ignorado). Só `.env.example`, sem valores, é versionado.

### 16.2 O que será necessário

| Item | Onde obter | Obrigatório |
|---|---|---|
| Google Cloud project | Google Cloud Console | Sim |
| Tag Manager API habilitada | API Library do projeto | Sim |
| OAuth Client (tipo Desktop app) | Google Cloud Console → Credentials | Sim |
| Acesso de usuário aos containers GTM do cliente | Admin do container/conta GTM | Sim |
| Python 3.11+ | Sistema operacional | Sim |

### 16.3 Criar o projeto, habilitar a API e o OAuth Client

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/) e crie ou selecione um projeto.
2. Na API Library, procure `Tag Manager API` e habilite.
3. Configure a tela de consentimento OAuth do projeto (modo de teste é suficiente para uso interno; adicione como test user o e-mail que acessa os containers GTM).
4. Em **Credentials → Create Credentials → OAuth client ID**, escolha o tipo **Desktop app**.
5. Baixe o JSON do client secret.

### 16.4 Instalar o cliente local

Peça ao agent para instalar, ou rode manualmente:

```bash
python3 -m venv .venv-gtm
.venv-gtm/bin/pip install -e integrations/gtm
```

### 16.5 Configurar as credenciais (nunca no repositório)

1. Salve o JSON baixado em `credentials/gtm-oauth-client-secret.json` (a pasta `credentials/` já está no `.gitignore`).
2. Copie `.env.example` para `.env` e preencha:

```text
PERFORMANCE_ADS_GTM_CREDENTIALS_PATH=credentials/gtm-oauth-client-secret.json
PERFORMANCE_ADS_GTM_TOKEN_CACHE_PATH=credentials/gtm-oauth-token.json
PERFORMANCE_ADS_GTM_DECLARED_CAPABILITIES=reporting
PERFORMANCE_ADS_GTM_WRITE_MODE=disabled
PERFORMANCE_ADS_GTM_ALLOWED_CONTAINER_IDS=
```

Nunca cole client secret, JSON de credencial ou token em chats, issues ou commits. Se o agent ajudar na instalação, ele deve informar somente caminhos e nomes de variável, sem imprimir valores.

### 16.6 Primeiro teste (leitura)

```bash
set -a && source .env && set +a
.venv-gtm/bin/python scripts/gtm_audit.py --list-accounts
```

A primeira chamada abre o navegador para o consentimento OAuth e cacheia o token em `PERFORMANCE_ADS_GTM_TOKEN_CACHE_PATH`. O resultado esperado é a lista de contas GTM às quais o e-mail autorizado tem acesso — sem nenhuma mutação.

Para inspecionar um container específico:

```bash
.venv-gtm/bin/python scripts/gtm_audit.py --list-containers --account-path accounts/SEU_ACCOUNT_ID
.venv-gtm/bin/python scripts/gtm_audit.py --snapshot --container-path accounts/SEU_ACCOUNT_ID/containers/SEU_CONTAINER_ID
```

### 16.7 Habilitar criação/edição

Escrita continua bloqueada até você preencher a allowlist local. No `.env`:

```text
PERFORMANCE_ADS_GTM_DECLARED_CAPABILITIES=reporting,tag_management
PERFORMANCE_ADS_GTM_WRITE_MODE=execute
PERFORMANCE_ADS_GTM_ALLOWED_CONTAINER_IDS=SEU_CONTAINER_ID,OUTRO_CONTAINER_ID
```

Com isso, um change set aprovado envolvendo tag/trigger/variável desses containers pode ser aplicado por `/executar-operacao` via `scripts/gtm_edit.py` — sempre em rascunho de workspace, nunca publicado.

### 16.8 Erros comuns

| Erro | Verificação segura |
|---|---|
| `PERFORMANCE_ADS_GTM_CREDENTIALS_PATH nao configurado` | Confirmar se `.env` foi carregado no shell atual. |
| `arquivo de credencial OAuth nao encontrado` | Conferir o caminho do JSON salvo em `credentials/`. |
| `escrita requer allowlist de containers configurada` | Preencher `PERFORMANCE_ADS_GTM_ALLOWED_CONTAINER_IDS` com o `container_id` numérico. |
| `container_id fora da allowlist local` | O container do alvo não está na lista; adicionar ou confirmar o ID correto. |
| Pedido de novo login no navegador após mudar `WRITE_MODE` | Esperado — o token antigo não tinha o escopo de edição; o cache é renovado automaticamente. |

### 16.9 Rotação ou remoção

Para trocar de client secret (ex: após um valor ter sido exposto), gere um novo em Google Cloud Console → Credentials, revogue o antigo, substitua o arquivo em `credentials/` e apague `credentials/gtm-oauth-token.json` para forçar novo consentimento. Para remover a integração, apague `.env`, a pasta `credentials/` e desinstale o pacote do ambiente local — nada disso afeta o restante do agent.
