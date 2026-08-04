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
- Python 3 e `pipx` para o MCP oficial Google Ads.
- Acesso autorizado à plataforma usada.
- Para Google Ads conectado: Google Cloud project, Google Ads API habilitada, developer token e OAuth/ADC.
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

## 6. Google Ads MCP local

O V1 usa o servidor oficial open source:

```text
https://github.com/googleads/google-ads-mcp
```

Ele é tratado como **somente leitura**. As ferramentas esperadas são listagem de customers, consultas GAQL e descoberta de metadata. Não presumir escrita nem Keyword Planner.

### 6.1 Pré-requisitos Google

1. Criar ou selecionar um Google Cloud project.
2. Habilitar a Google Ads API.
3. Obter um developer token no API Center de uma manager account.
4. Criar OAuth client ou configurar Application Default Credentials.
5. Garantir que o usuário autenticado tenha acesso aos customers necessários.
6. Instalar `pipx`.

O developer token precisa de nível compatível com as contas consultadas. Acesso de teste não comprova leitura de contas de produção.

### 6.2 Credenciais

Guardar credenciais fora do repositório. Nunca copiar para `clients/`, `skills/`, `knowledge/`, exemplos ou dossiês.

Variáveis usadas pelo servidor:

```text
GOOGLE_APPLICATION_CREDENTIALS
GOOGLE_PROJECT_ID
GOOGLE_ADS_DEVELOPER_TOKEN
GOOGLE_ADS_LOGIN_CUSTOMER_ID
```

`GOOGLE_ADS_LOGIN_CUSTOMER_ID` é necessário quando o acesso ao customer ocorre por uma manager account. Os valores reais devem existir somente no ambiente/configuração local.

### 6.3 Comando local do servidor

O servidor pode ser iniciado por `pipx`:

```text
pipx run --spec git+https://github.com/googleads/google-ads-mcp.git google-ads-mcp
```

Antes de executar, configure as credenciais no ambiente local conforme a documentação oficial. Não coloque valores reais em scripts versionados.

### 6.4 Codex

Execute:

```text
/configuracao-mcp
Plataforma: Google Ads
```

A skill deve:

1. Inspecionar somente a seção Google Ads de `~/.codex/config.toml`.
2. Mostrar a configuração proposta com placeholders.
3. Pedir confirmação antes de editar o arquivo global local.
4. Apontar para credenciais armazenadas fora do projeto.
5. Reiniciar a sessão.
6. Testar somente listagem de customers, metadata e GAQL.

Exemplo estrutural com placeholders, para o arquivo global local:

```toml
[mcp_servers.google_ads]
command = "pipx"
args = ["run", "--spec", "git+https://github.com/googleads/google-ads-mcp.git", "google-ads-mcp"]

[mcp_servers.google_ads.env]
GOOGLE_APPLICATION_CREDENTIALS = "/CAMINHO/LOCAL/FORA/DO/REPOSITORIO/credentials.json"
GOOGLE_PROJECT_ID = "SEU_PROJECT_ID"
GOOGLE_ADS_DEVELOPER_TOKEN = "SEU_DEVELOPER_TOKEN"
GOOGLE_ADS_LOGIN_CUSTOMER_ID = "SEU_MANAGER_CUSTOMER_ID"
```

Este bloco é documentação com placeholders. Nunca criar um arquivo equivalente dentro do repositório.

### 6.5 Claude Code

Execute `/configuracao-mcp`, informe `Google Ads` e siga a configuração atual documentada pelo repositório oficial. O server command é o mesmo de `pipx`; variáveis e caminhos permanecem na configuração local do usuário.

### 6.6 Homologação

Validar nesta ordem:

1. Processo do servidor inicia.
2. Credencial OAuth/ADC funciona.
3. Developer token é aceito.
4. Customers acessíveis podem ser listados.
5. Customer correto é confirmado por nome, ID mascarado, moeda e timezone.
6. Consulta GAQL simples funciona.

Nenhum teste de escrita faz parte do V1.

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
