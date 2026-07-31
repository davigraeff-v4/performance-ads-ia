# META PERFORMANCE IA

Agente especialista em Meta Ads para ajudar gestores a planejar, analisar e otimizar campanhas com mais assertividade, praticidade, velocidade e rastreabilidade.

O agente roda em **Claude Code** e **Codex**, usa o MCP oficial do Meta Ads quando disponível e registra cada auditoria, análise ou mudança em um dossiê Markdown dentro da pasta do cliente.

> Estado atual: versão pública inicial. Dados, configurações e dossiês reais de clientes continuam exclusivamente locais e ignorados pelo Git.

## 1. O que o agente faz

- Configura e diagnostica a conexão MCP.
- Cadastra contexto, metas e restrições por cliente.
- Planeja campanhas de lead generation e e-commerce.
- Audita tracking, estrutura e performance.
- Analisa campanhas com janelas e atribuição declaradas.
- Propõe otimizações em lotes versionados.
- Cria ou altera ativos suportados somente após aprovação.
- Registra antes, aprovação, execução e depois no mesmo dossiê.
- Produz relatórios e briefings criativos.
- Consulta seletivamente uma base local de 151 artigos oficiais da Central Meta.

Não exclui nem arquiva ativos, não executa mudanças silenciosas e não substitui uma análise causal.

## 2. Requisitos

- macOS, Linux ou ambiente compatível com Claude Code/Codex.
- Claude Code ou Codex instalado.
- Acesso autorizado ao Business/conta de anúncios Meta.
- Permissão adequada para leitura; permissão de escrita somente se for operar.
- Navegador para concluir OAuth quando solicitado pelo MCP.
- Dados comerciais em CSV, XLSX ou planilha quando a análise exigir qualidade do lead, vendas, receita ou margem.

## 3. Instalação local

### Via Git

```bash
git clone https://github.com/davigraeff-v4/meta-performance-ia.git
cd meta-performance-ia
```

Depois:

1. Abra exatamente a raiz `meta-performance-ia` no Claude Code ou Codex.
2. Confirme que a raiz contém `CLAUDE.md`, `AGENTS.md` e `CONTRATO-OPERACIONAL.md`.
3. Inicie uma conversa na raiz e execute `/configuracao-mcp`.

## 4. Abrir no Claude Code

No terminal:

```bash
cd "/caminho/onde-voce-clonou/meta-performance-ia"
claude
```

O Claude Code carrega `CLAUDE.md`. Os comandos em `.claude/commands/` ficam disponíveis como slash commands.

Teste inicial:

```text
/configuracao-mcp
```

## 5. Abrir no Codex

Abra a pasta clonada `meta-performance-ia` no Codex Desktop. O Codex carrega `AGENTS.md` como instrução do workspace.

No Codex, os slash commands do projeto são convenções textuais: digite `/configuracao-mcp`, `/auditar-conta` ou outro comando no chat.

## 6. Configurar o MCP no Claude Code

O endpoint usado pelo projeto é:

```text
https://mcp.facebook.com/ads
```

### Diagnóstico

```bash
claude mcp get facebook-ads
```

Se o servidor não existir, o comando validado na versão local do Claude Code é:

```bash
claude mcp add --transport http --scope user facebook-ads https://mcp.facebook.com/ads
```

Depois:

1. Execute `claude mcp get facebook-ads` novamente.
2. Abra/reinicie a sessão do Claude Code se as ferramentas não aparecerem.
3. Conclua o OAuth no navegador quando solicitado.
4. Autorize somente os ativos necessários.
5. Peça ao agente para listar contas acessíveis sem fazer alterações.

No ambiente usado para construir este modelo, `claude mcp get facebook-ads` retornou transporte HTTP conectado no escopo de usuário. Isso não comprova que outro computador esteja autenticado nem que tenha permissão de escrita.

## 7. Configurar o MCP no Codex

Execute `/configuracao-mcp` no Codex. A skill deve inspecionar apenas a seção Meta da configuração.

Configuração manual esperada em `~/.codex/config.toml`:

```toml
[mcp_servers.meta_ads]
url = "https://mcp.facebook.com/ads"
```

Procedimento:

1. Feche sessões que possam sobrescrever a configuração.
2. Faça backup apenas do arquivo local de configuração.
3. Adicione a seção acima se ela não existir.
4. Reinicie o Codex.
5. Conclua a autenticação quando o aplicativo solicitar.
6. Verifique se as ferramentas Meta aparecem na nova sessão.
7. Faça teste somente de leitura.

O CLI global `codex mcp` pode variar ou estar quebrado por instalação incompleta. Por isso, este README documenta o formato de configuração local observado e exige validação na sessão, sem afirmar que um comando CLI não testado funciona.

## 8. Autenticação e contas

Conexão tem quatro gates separados:

1. **Transporte:** o servidor responde.
2. **Autenticação:** o usuário concluiu OAuth.
3. **Escopo:** a conta desejada aparece entre os ativos acessíveis.
4. **Capacidade:** leitura e escrita disponíveis para a operação pretendida.

Ao selecionar uma conta, confirme:

- Nome da conta.
- ID mascarado.
- Business associado.
- Moeda.
- Timezone.
- Pixel/dataset.
- Página e Instagram quando relevantes.
- Permissões de leitura e escrita.

Se duas contas tiverem nomes parecidos, o agente deve parar e pedir confirmação.

## 9. Primeiro uso

### 1. Configurar

```text
/configuracao-mcp
```

### 2. Cadastrar cliente

```text
/novo-cliente

Cliente: Exemplo Solar
Modelo: lead generation
Objetivo: gerar oportunidades qualificadas
Oferta: projeto de energia solar residencial
Meta: CPQL de até R$ 120
Ciclo de venda: 30 a 60 dias
```

O agente cria `clients/exemplo-solar/CLIENTE.md` e um dossiê de onboarding.

### 3. Planejar ou auditar

```text
/planejar-campanha
```

ou:

```text
/auditar-conta
```

### 4. Aprovar e executar

Quando houver mudanças, o agente gera um ID de operação:

```text
/aprovar-operacao op-20260801-1430-exemplo-solar-v1
```

Aprovar não executa. Para executar:

```text
/executar-operacao op-20260801-1430-exemplo-solar-v1
```

## 10. Fornecer arquivos e planilhas

Formatos aceitos no MVP:

- CSV.
- XLSX/XLS.
- Link de Google Sheets acessível no ambiente.
- Markdown com definição dos campos.

Informe junto:

- Período dos dados.
- Timezone.
- Definição de cada etapa.
- Chave de agregação: data, campanha, conjunto, anúncio ou UTM.
- Se receita é bruta, líquida ou aprovada.
- Se cancelamentos e reembolsos foram removidos.
- Se leads duplicados/inválidos foram tratados.

Não inclua dados pessoais quando bastarem dados agregados.

## 11. Comandos

| Comando | Resultado |
|---|---|
| `/configuracao-mcp` | Diagnostica/configura o MCP e gera dossiê sem segredos. |
| `/novo-cliente` | Cria ou atualiza a ficha operacional. |
| `/planejar-campanha` | Produz estratégia sem executar. |
| `/criar-campanha` | Produz plano completo e change set de criação. |
| `/auditar-conta` | Audita conexão, tracking, estrutura e riscos. |
| `/analisar-campanha` | Analisa performance de escopo e janela definidos. |
| `/otimizar-campanha` | Diagnostica e propõe lote priorizado. |
| `/relatorio-performance` | Gera resumo executivo e apêndice operacional. |
| `/aprovar-operacao <id>` | Registra aprovação da versão; não executa. |
| `/executar-operacao <id>` | Revalida e executa somente a versão aprovada. |
| `/reverter-operacao <id>` | Propõe restauração de valores conhecidos; exige nova aprovação. |

## 12. Catálogo das 16 skills

| Skill | Use para | Entrada principal | Saída |
|---|---|---|---|
| `00-configuracao-mcp` | Instalar/diagnosticar MCP | Ambiente e endpoint | Dossiê de configuração |
| `01-client-campaign-intake` | Cadastrar contexto | Briefing e ficha | Cliente/campanha estruturados |
| `02-meta-account-connection` | Confirmar conta | MCP e cliente | Snapshot de conta/permissões |
| `03-measurement-data-quality` | Auditar tracking | Eventos e fontes | Gate de confiabilidade |
| `04-goals-kpis-baseline` | Definir sucesso | Metas e histórico | KPIs e baseline |
| `05-campaign-strategy` | Planejar campanha | Objetivo e oferta | Estratégia Meta |
| `06-account-campaign-architecture` | Estruturar ativos | Estratégia | Campanhas/conjuntos/anúncios |
| `07-audience-strategy` | Planejar públicos | Mercado e dados | Públicos, exclusões e testes |
| `08-budget-bidding-allocation` | Planejar verba | Meta e arquitetura | Alocação/lances |
| `09-creative-performance-brief` | Melhorar criativos | Breakdown e peças | Diagnóstico/briefing |
| `10-campaign-build-plan` | Consolidar criação | Skills 05–09 | Plano e change set |
| `11-performance-diagnosis` | Encontrar gargalos | Insights + comercial | Diagnóstico priorizado |
| `12-optimization-change-set` | Propor otimização | Diagnóstico | Lote versionado |
| `13-approved-change-executor` | Executar lote | Aprovação válida | Resultado por item |
| `14-reporting-memory-learning` | Relatar/aprender | Dossiês e resultados | Relatório e memória |
| `15-meta-help-center-retrieval` | Consultar Central Meta | Pergunta ou trecho de título | Artigos relevantes lidos e fontes |

Leia o `SKILL.md` correspondente para o fluxo e gates completos.

### Validar o modelo local

Execute:

```bash
python3 scripts/validate_repository.py
python3 -m unittest tests/test_meta_help_search.py
```

Para calcular o hash canônico de um dossiê JSON estruturado:

```bash
python3 scripts/hash_change_set.py examples/synthetic/operation-approved.json
```

## 13. Interpretar uma análise

O agente usa marcadores:

- `[F]`: fato observado.
- `[C]`: cálculo reproduzível.
- `[H]`: hipótese ainda não comprovada.
- `[R]`: recomendação.
- `[I]`: informação indisponível.

Confiança:

- **Alta:** fonte confiável, volume e comparação adequados, sem contradição relevante.
- **Média:** evidência útil, mas com ressalva de volume, tracking ou contexto.
- **Baixa:** hipótese exploratória; não sustenta mudança irreversível.

## 14. Dossiês

Local:

```text
clients/{cliente}/AAAA-MM-DD-HHMM-{tipo}-{escopo}.md
```

O mesmo arquivo acompanha proposta, aprovação, execução e snapshot posterior. Nunca altere manualmente uma versão aprovada sem invalidar a aprovação.

Estados: `draft`, `proposed`, `approved`, `executing`, `executed`, `partial_failure`, `failed`, `reverted`, `analysis_only`.

## 15. Reversão

`/reverter-operacao <id>` não desfaz magicamente uma operação. Ele:

1. Lê o snapshot anterior.
2. Identifica somente campos restauráveis.
3. Cria um novo change set.
4. Expõe riscos e efeitos colaterais.
5. Exige aprovação e execução separadas.

Não reverte criativos, aprendizado, revisão ou efeitos históricos que a plataforma não permita restaurar.

## 16. Base de conhecimento

Comece por `knowledge/README.md`. A base separa:

- Snapshot local de 151 artigos da Central de Ajuda Meta, com URL e data.
- Resumos operacionais de documentação oficial Meta.
- Metodologia operacional interna.
- Trilhas lead generation e e-commerce.
- Mensuração.
- Performance criativa.
- Aprendizados sanitizados aprovados.

### Como a recuperação seletiva funciona

O agente não “memoriza” nem carrega os 151 artigos em toda conversa. Ele usa recuperação progressiva:

1. Recebe a pergunta original.
2. Busca lexical leve por título e categoria usando primeiro apenas o índice.
3. Se houver correspondência exata ou forte de título, lê o artigo inteiro.
4. Se houver correspondência temática, lê somente os 1–3 melhores candidatos.
5. Se o índice produzir resultado fraco, usa uma varredura local de conteúdo apenas como fallback e refina a busca; os arquivos não são carregados no contexto do agente.
6. Em decisões sensíveis ou regras mutáveis, valida também a URL oficial ao vivo.

Busca manual:

```bash
python3 scripts/search_meta_help.py "como funciona a meta de ROAS" --limit 3
```

Busca apenas em títulos:

```bash
python3 scripts/search_meta_help.py "público semelhante" --title-only --limit 5
```

Cada resultado informa força da correspondência, título, caminho, categoria, data de extração e URL. A regra completa está em `skills/15-meta-help-center-retrieval/SKILL.md`.

### Atualidade e atribuição

O snapshot contém 151 artigos extraídos em 2026-07-31. Quando uma regra oficial puder ter mudado, o agente deve verificar a fonte ao vivo e registrar a consulta no dossiê.

O repositório inclui o snapshot para que clones públicos preservem a recuperação local. Os textos mantêm título, fonte e URL original. Consulte `NOTICE-META-CONTENT.md`: o projeto não é afiliado, endossado ou mantido pela Meta, e o conteúdo de terceiros continua sujeito aos direitos e termos de seus titulares.

## 17. Atualizar conhecimento

1. Registre o aprendizado real em `clients/{cliente}/CLIENTE.md`.
2. Peça ao agente uma proposta sanitizada.
3. Confirme que não há nome, ID, valor, oferta ou criativo identificável.
4. Revise evidência, escopo e limitação.
5. Aprove explicitamente.
6. Somente então adicione em `knowledge/sanitized-learnings/`.

## 18. Solução de problemas

### MCP conectado, mas ferramentas não aparecem

- Reinicie a sessão.
- Confirme o endpoint e o ambiente.
- Refaça OAuth.
- Verifique se o host suporta o transporte HTTP.

### Conta não aparece

- Confirme o usuário autenticado.
- Verifique permissões no Business.
- Confirme se a conta pertence ao Business esperado.
- Não tente contornar permissão com outro cliente/conta.

### Leitura funciona, escrita não

- Verifique a lista real de ferramentas e permissões.
- Mantenha modo consultivo.
- Gere change set e instrução manual.
- Não use navegador automaticamente.

### Codex CLI retorna erro de instalação

- Use o Codex Desktop e a configuração TOML validada.
- Corrija o CLI separadamente; não confunda falha do binário com falha do servidor MCP.

### Dados Meta e planilha divergem

- Confira timezone, janela, atribuição, chaves, cancelamentos, duplicidade e definição de receita/lead.
- Mantenha ambos os valores e explique a incompatibilidade.
- Não force reconciliação sem evidência.

## 19. Segurança do repositório

Nunca publicar:

- `clients/` reais.
- CSV/XLSX/exportações.
- Tokens, cookies, OAuth ou configurações locais.
- Dossiês reais.
- IDs completos de conta, pixel, página ou catálogo.
- Criativos, ofertas ou resultados identificáveis.
Antes de qualquer push:

1. Auditar `.gitignore`.
2. Buscar padrões de segredo e IDs.
3. Conferir que exemplos são sintéticos.
4. Revisar a lista completa de arquivos staged.

## 20. Checklist de homologação

- [ ] PRD, README e contrato revisados.
- [ ] 16 skills válidas.
- [ ] 151 artigos validados, sem títulos ou URLs duplicados.
- [ ] Busca seletiva testada com correspondência exata, temática e fraca.
- [ ] Grafo e schemas válidos.
- [ ] Claude e Codex coerentes.
- [ ] MCP validado nos dois ambientes.
- [ ] Smoke test somente leitura concluído.
- [ ] Casos sintéticos aprovados.
- [ ] Um dossiê real revisado.
- [ ] Uma operação controlada aprovada separadamente, se desejada.
- [ ] Nenhum segredo ou dado real fora de `clients/`.
- [ ] Nenhum cliente, segredo ou exportação real staged.
- [ ] Publicação ou atualização aprovada por Davi.
