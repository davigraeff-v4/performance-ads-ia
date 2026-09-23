# PERFORMANCE ADS IA

Agente especialista em Meta Ads e Google Ads para planejar, analisar e otimizar campanhas com decisões rastreáveis, dados comerciais e aprovação versionada.

O agent roda em **Claude Code** e **Codex**, entende solicitações em linguagem natural, seleciona e executa automaticamente somente as skills necessárias, entrega primeiro no chat e registra apenas versões editorialmente aprovadas em dossiês Markdown locais.

> Estado: V2.0 local. Respostas no chat explicativas e visuais (`templates/resposta-chat.md`), dossiê em dois arquivos (`.md` para ler e `.json` de registro) criado só por `scripts/dossier.py`, checagem obrigatória de boas práticas nas mudanças, histórico do cliente consultável (inclusive os dossiês legados) e profundidade `full` só em auditoria. O MCP oficial Google Ads continua somente leitura; o complemento `google_ads_extended` e a integração GTM permanecem fail-closed conforme os gates documentados. Search Console, Google Trends e GA4 ficam para fases futuras. Dados, credenciais, MCPs/API locais e dossiês reais permanecem fora do Git.

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
- Entrega no chat de forma explicativa e visual: todo número vem com leitura, sem IDs internos, hashes ou códigos.
- Confere as premissas do diagnóstico e das mudanças na base oficial (Central Meta, fontes Google Ads e `ads_get_help_article` do conector Meta).
- Só cria o dossiê depois da aprovação do conteúdo, e só pelo `scripts/dossier.py`.
- Registra aprovação, execução (inclusive o que o gestor fez à mão) e a avaliação do resultado ao fim da janela.
- Consulta o histórico do cliente, com os dossiês legados como base somente leitura.

Não exclui nem arquiva ativos, não ativa recomendações automáticas e não executa mudanças silenciosas.

## 2. Como o roteamento funciona

Cada demanda define:

1. Intenção: tirar dúvida, consulta rápida, histórico, configurar, cadastrar, pesquisar palavras-chave, planejar, criar, auditar, analisar, otimizar, ajuste pontual, relatar, aprovar, executar ou reverter. A tabela de decisão com exemplos está no CLAUDE.md/AGENTS.md (gerados de `prompt/agent-prompt.md` por `scripts/build_agent_prompts.py`).
2. Plataformas: `meta`, `google_ads`, ambas ou ainda indefinidas.
3. Fonte por plataforma:
   - `connected_read`: MCP/API somente leitura.
   - `file_based`: CSV, XLSX ou Google Sheets.
   - `context_only`: briefing e informações manuais.
   - `unavailable`: fonte necessária ausente.

O agent não percorre um fluxo fixo. A skill pública `performance-ads-roteador`, descoberta automaticamente pelas pastas `.agents/skills/` e `.claude/skills/`, classifica a demanda e consulta `routing_matrix.json`. Uma análise Google Ads não carrega as skills Meta; uma demanda multicanal abre os dois ramos e preserva fontes, contas e atribuições separadamente. O gestor não precisa mencionar nomes de skills.

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

O roteador público já está exposto em `.agents/skills/performance-ads-roteador` e `.claude/skills/performance-ads-roteador`. Depois de instalar ou atualizar esta estrutura, reinicie a sessão do Codex/Claude Code para renovar a descoberta de skills.

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

Execute `/configuracao-mcp`, informe `Meta Ads` e siga a skill `conexao/configuracao-mcp`. O procedimento exige confirmação antes de editar configuração local e termina com teste somente leitura.

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
| `/aprovar-operacao [id]` | Registra a aprovação de execução; sem id, lista as operações abertas e confirma pelo título. Não executa. |
| `/executar-operacao <id>` | Revalida e executa somente lote suportado. |
| `/reverter-operacao <id>` | Propõe restauração conhecida com nova aprovação. |

## 10. Catálogo dos 10 módulos

Desde a Sprint 2, as 27 skills antigas viraram 10 módulos em `skills/`. Só o roteador é público; os outros 9 são internos e o gestor nunca precisa acioná-los. Cada módulo tem um `SKILL.md` (índice com as regras comuns) e, quando cobre mais de um caso, referências em `references/`. As rotas (`routing_matrix.json`) planejam **etapas**: `modulo` lê `skills/modulo/SKILL.md`; `modulo/referencia` lê também `skills/modulo/references/referencia.md`. As dependências entre etapas ficam em `dependency_graph.json`.

| Módulo | Responsabilidade | Etapas |
|---|---|---|
| `performance-ads-roteador` | Entrada pública: entende o pedido, resolve a rota, executa as etapas e entrega no chat | — |
| `contexto-cliente` | Cadastro, ficha, histórico e aprendizados do cliente | `contexto-cliente` |
| `conexao` | Conta certa e capacidade real dos conectores; configuração do MCP | `conexao/meta`, `conexao/google-ads`, `conexao/configuracao-mcp` |
| `mensuracao` | Qualidade da mensuração; auditoria de GTM quando pedida | `mensuracao`, `mensuracao/gtm` |
| `diagnostico` | Metas e linha de base; diagnóstico por plataforma; modo avaliação | `diagnostico/metas-e-linha-de-base`, `diagnostico/meta`, `diagnostico/google-ads` |

| Módulo | Responsabilidade | Etapas |
|---|---|---|
| `planejamento` | Estratégia, arquitetura, públicos ou palavras-chave, verba e lances, criativos e plano de construção | 6 etapas `planejamento/meta-…` e 6 `planejamento/google-ads-…` |
| `change-set` | Transforma diagnóstico ou decisão do gestor em mudanças aprováveis | `change-set` |
| `revisor` | Base oficial: dúvidas e checagem de premissas (`kb_check.py`) | `revisor/meta`, `revisor/google-ads` |
| `entrega` | Relatório e fechamento; exportação na Sprint 3 | `entrega` |
| `executor` | Executa só o que foi aprovado e registra o resultado | `executor` |

Dossiês antigos citam os nomes antigos das skills (ex.: `11-performance-diagnosis`); isso é esperado, porque eles são registro histórico somente leitura.

## 11. Dossiês, aprovação e execução

Cada operação registrada vive em `clients/{slug}/operacoes/`, em dois arquivos com o mesmo nome:

- `.md`: o dossiê para ler, com o texto aprovado no chat, as mudanças em blocos, o andamento (aprovação, execução, diferenças, avaliação) e, recolhidos no fim, os dados técnicos;
- `.json`: o registro de máquina (`schemas/operation-v2.schema.json`).

Os dois são criados e atualizados só pelo `scripts/dossier.py`:

| Momento | Comando |
|---|---|
| Gestor aprova o conteúdo mostrado no chat | `dossier.py new --client {slug} --spec … --body …` |
| Conteúdo muda antes da execução | `dossier.py revise {operação} …` (nova versão, aprovação anterior invalidada) |
| `/aprovar-operacao` | `dossier.py approve {operação} --statement "…"` |
| Execução pelo conector ou manual | `dossier.py record-execution {operação} --results …` |
| `/avaliar-operacao`, no fim da janela e com o aval do gestor | `dossier.py evaluate {operação} --result success\|failure\|inconclusive --notes "…"` |
| Conferir | `dossier.py verify --client {slug}` · `dossier.py list --open` |

No Claude Code, um hook (`.claude/settings.json`) bloqueia escrita direta em `operacoes/`, edição de dossiê legado e dossiê novo escrito à mão.

Análises multicanal podem compartilhar um dossiê, mas mutações usam um `operation_id` por plataforma. Aprovar Meta não aprova Google Ads e vice-versa. O fluxo possui três gates distintos:

1. **Aprovação do conteúdo:** autoriza registrar a versão mostrada no chat. Não aprova mídia.
2. **`/aprovar-operacao`:** aprova a versão e o hash das mudanças registradas. Não executa.
3. **`/executar-operacao`:** executa somente quando a integração e as permissões foram homologadas.
4. **`/avaliar-operacao`** (intenção `avaliacao`, profundidade rápida): no fim da janela, compara o resultado com os critérios de sucesso e de parada registrados e explica no chat se funcionou e por quê; só registra com o aval do gestor. Exige dado da conta ou de arquivo. O resumo do cliente e `dossier.py list --open` destacam as avaliações vencidas.

**Dossiês legados** (Markdown com bloco JSON, na raiz da pasta do cliente) ficam como base de consulta somente leitura: `python3 scripts/client_history.py list {slug}` e `search {slug} "termos"`. Uma operação legada ainda aberta é migrada com `dossier.py migrate` antes de ser aprovada ou executada.

**Memória do cliente (Sprint 2).** Toda conversa começa por `python3 scripts/client_brief.py {slug}`, gerado na hora, sem arquivo intermediário: perfil compacto do `CLIENTE.md`, operações em aberto (legado e V2), avaliações vencidas, decisões pendentes, últimas operações e as regras duráveis de `APRENDIZADOS.md`. A ficha passa a ter três partes: `CLIENTE.md` (perfil estável), `APRENDIZADOS.md` (regras duráveis, molde em `templates/aprendizados-template.md`) e, para fichas antigas, `HISTORICO-ANTERIOR.md` (a seção de histórico escrita à mão, copiada sem alteração). A separação de uma ficha antiga é feita por `python3 scripts/migrate_client_profile.py {slug} [--learnings rascunho.md] [--apply]`: sem `--apply` só simula; com `--apply` grava cópia de segurança e nunca sobrescreve arquivos existentes. Um cliente por vez, com aprovação do gestor.

Na V1.1 inicial:

- Meta pode ser executado somente se escrita tiver sido homologada.
- Google Ads permanece `manual_only`; o complemento ainda não registra ferramentas de escrita.
- Recomendações automáticas nunca são aplicadas por padrão.

## 12. Conhecimento

- Meta: snapshot seletivo de 153 artigos mais resumos operacionais.
- Google Ads: base seletiva da Central de Ajuda, fontes de API e consulta oficial ao vivo.
- Metodologia: regras internas separadas das afirmações das plataformas.
- Aprendizados: somente padrões sanitizados e aprovados.
- Busca híbrida (V1.2): a recuperação sobre as duas bases de Central de Ajuda combina busca lexical por título (padrão, determinística) com um sinal semântico local (embeddings via `fastembed`, sem PyTorch, sem chamada externa) que entra em ação só quando o título não bater — cobre perguntas parafraseadas sem perder a garantia de leitura integral em match forte. Índice em `knowledge/.vector-index/` (versionado no Git — ~2.6MB, o time recebe o RAG pronto no clone/pull — regenerável, isolado por plataforma, nunca indexa `clients/`; `scripts/validate_repository.py` detecta se ficou desatualizado em relação aos `.md` fonte).

Para (re)construir o índice vetorial localmente (só necessário depois de editar artigos, ou se `validate_repository.py` acusar desatualização):

```text
python3 scripts/build_knowledge_vector_index.py --platform all
```

Sem esse passo, a busca cai automaticamente para o modo lexical original — não é obrigatório para o agent funcionar.

- Revisor de boas práticas (V2, Sprint 2): `scripts/kb_check.py` recebe as premissas de mecanismo de um diagnóstico ou change set e devolve, por plataforma, os artigos a ler, os trechos mais ligados a cada premissa e o esqueleto de `knowledge_checks`. O ranqueamento vive em `scripts/help_search.py` (as duas interfaces `search_*_help.py` são finas). Premissas passam por um dicionário controlado de reescrita (`knowledge/retrieval-rewrites.json`); `strong` só com evidência de título; artigos de política só sobem em consulta sobre política. Medição: `python3 scripts/eval_retrieval.py --compare` (51 consultas rotuladas, 11 delas de controle). Em 2026-09-23, o acerto no 1º resultado foi de 58% para 97% nas consultas de ajuste e de 60% para 91% nas de controle, com zero "forte" errado.

## 13. Validação local

```text
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_all.py
```

O comando único verifica os 10 módulos e as 27 etapas de rota, descoberta nas duas plataformas, matriz e grafo, sincronia entre `prompt/agent-prompt.md`, CLAUDE.md e AGENTS.md, schemas, ciclo de vida dos dossiês V2 (hash, rota, estado), dossiês V2 dos clientes locais, isolamento do RAG, garantias do GTM (nunca publica, allowlist pelo caminho, `validate_only` sem escrita) e conectores fail-closed. Não realiza mutações externas. `python3 -m pytest` na raiz roda o motor e o GTM.

Medições que acompanham mudanças no agent (Sprint 2):

- **Busca na base oficial:** `python3 scripts/eval_retrieval.py --compare` (51 consultas rotuladas, 11 de controle). Rode antes e depois de mexer em pesos, no dicionário de reescrita ou na base; o patamar mínimo está em `tests/test_retrieval_eval.py`.
- **Roteamento:** `python3 scripts/eval_routing.py --check` (no CI: toda rota esperada existe) e, a cada mudança no prompt ou no roteador, a classificação independente das 33 frases reais anonimizadas: `claude -p "$(python3 scripts/eval_routing.py --prompt)" --permission-mode plan > .work/rotas.txt` e `python3 scripts/eval_routing.py --score .work/rotas.txt`. As medições ficam em `historico_de_medicoes` de `tests/fixtures/routing_eval.json`.

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

Diferente do Google Ads, o GTM **não usa servidor MCP**. É um cliente Python local (`integrations/gtm/`) que fala diretamente com a API oficial (`tagmanager.googleapis.com`) via OAuth. A skill `mensuracao/gtm` chama dois scripts:

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
