# PRD — PERFORMANCE ADS IA

**Versão:** 1.3.0-local
**Data:** 2026-08-06
**Responsável:** Davi
**Ambientes:** Claude Code e Codex
**Estado:** V1 de roteamento automático e entrega chat-first homologado localmente; MCP oficial validado e complemento local fail-closed instalado

## 1. Visão geral

O PERFORMANCE ADS IA é um único agente especialista em Meta Ads e Google Ads. Ele transforma dados de plataforma, arquivos e contexto comercial em planejamento, diagnóstico, change sets, aprovação e aprendizado rastreáveis.

O agent não segue um fluxo linear. Cada demanda seleciona intenção, plataformas e modos de fonte; somente as skills necessárias são executadas.

## 2. Problema

Gestores precisam decidir sob pressão usando fontes incompletas, atribuições incompatíveis e recomendações automáticas. Os principais riscos são:

1. Otimizar métrica de plataforma sem resultado comercial.
2. Misturar Meta, Google Ads e CRM como se fossem a mesma população.
3. Escolher campanha, lance ou targeting por costume.
4. Confundir palavra-chave com termo de pesquisa.
5. Tratar volume, forecast ou Optimization Score como garantia.
6. Alterar campanhas sem documentar estado, aprovação e resultado.
7. Depender de MCP para funcionar.
8. Misturar contas, plataformas, IDs ou credenciais.
9. Depender do acionamento manual de skills internas.
10. Entregar diagnóstico genérico ou exigir a abertura recorrente do dossiê.

## 3. Proposta de valor

`demanda → roteamento → fontes → qualidade → diagnóstico/estratégia → decisão → aprovação → execução suportada → verificação → aprendizado`

Cada operação possui uma representação estruturada persistida no dossiê e projetada como relatório completo no chat. Análises multicanal preservam ramos independentes; mutações usam operações e aprovações separadas.

## 4. Usuários

- Davi e gestores de tráfego intermediários/avançados.
- Gestores de projeto e lideranças que interpretam performance.
- Analistas de CRM, dados, vendas e e-commerce.

## 5. Objetivos do V1

1. Roteiar demandas Meta, Google Ads ou multicanal.
2. Funcionar com `connected_read`, `file_based` e `context_only`.
3. Configurar/diagnosticar MCP Meta, MCP oficial Google Ads e complemento local condicionado.
4. Cadastrar contas, metas, restrições e fontes por plataforma.
5. Planejar campanhas Meta e Google Ads por tipo.
6. Pesquisar e organizar palavras-chave Google Ads.
7. Auditar mensuração, estrutura e performance.
8. Recomendar otimizações com evidência e confiança.
9. Criar change sets versionados e aprovações por plataforma.
10. Produzir dossiês, relatórios e memória local.
11. Acionar skills automaticamente a partir da intenção, plataforma e fonte.
12. Produzir hipóteses e planos acionáveis com responsáveis e critérios verificáveis.

## 6. Fora do escopo

- Search Console, Google Trends e GA4.
- TikTok Ads ou outras plataformas.
- Produção final de copy ou design.
- Browser automation como fallback automático.
- Escrita Google Ads no V1.
- Aplicação automática de recomendações.
- Exclusão ou arquivamento de ativos.
- Otimização autônoma sem aprovação.
- Dashboard web, banco de dados ou RAG vetorial.
- Garantia causal a partir de atribuição observacional.

## 7. Arquitetura

### Agent

`CLAUDE.md` e `AGENTS.md` representam a mesma persona e contrato.

### Skills

- 1 skill de configuração multicanal.
- 6 skills compartilhadas de contexto, mensuração, metas, change set, execução e relatório.
- 9 skills operacionais/transversais Meta Ads.
- 9 skills Google Ads.
- 1 skill roteadora pública, descoberta automaticamente no Codex e Claude Code.
- Total: 26 skills (25 módulos + roteador).

### Estado

- `CLIENTE.md`: memória com plataformas, contas e modos de fonte.
- Dossiê `.md`: registro humano.
- JSON no dossiê: estado estruturado validável.
- `dependency_graph.json`: dependências condicionais.
- `routing_matrix.json`: rotas executáveis por intenção, plataforma e fonte.
- Schemas: contratos multicanal.

## 8. Roteamento

Toda solicitação registra:

- `requested_platforms`.
- `active_platforms`.
- `source_mode` por plataforma.
- Intenção operacional.
- Route ID canônico, contrato de saída e skills planejadas, executadas e puladas com motivo.

Regras:

- Uma demanda Meta não abre Google Ads.
- Uma demanda Google Ads não abre Meta.
- Escopo indefinido pode usar diagnóstico de canal antes do planejamento.
- Escopo multicanal compartilha contexto de negócio, mas separa evidência e conclusões.
- Mutação multicanal gera um `operation_id` por plataforma.
- Linguagem natural e comandos entram pela mesma skill roteadora pública.
- Fonte por arquivo/contexto não aciona configuração ou conexão de conta desnecessariamente.

## 9. Modos de fonte

### Connected read

Dados atuais consultados via MCP/API homologado. Exige conta inequívoca e timestamp.

### File based

CSV, XLSX ou Sheets com plataforma, conta, período, timezone, nível, atribuição e definições.

### Context only

Briefing e informações manuais. Sustenta planejamento e hipóteses; não sustenta diagnóstico factual da conta.

### Unavailable

Fonte necessária ausente. O agent registra a limitação e orienta a coleta.

## 10. Requisitos funcionais

### RF-01 — Configuração

Selecionar a plataforma antes de inspecionar configuração. Pedir confirmação para qualquer edição local e nunca exibir segredos.

### RF-02 — Onboarding

Criar `CLIENTE.md` com modelo, plataformas, contas, metas, funil, restrições, fontes, ciclo, margem e preferências.

### RF-03 — Seleção de conta

Confirmar nome, ID mascarado, moeda, timezone e manager/business conforme a plataforma. Bloquear ambiguidade.

### RF-04 — Mensuração

Avaliar Pixel/CAPI no Meta e tags/imports/ações de conversão no Google Ads, além de UTMs, atribuição e dados comerciais.

### RF-05 — Metas

Definir KPI principal, indicadores de saúde, meta, baseline, fonte, denominador e breakeven quando calculável.

### RF-06 — Planejamento Meta

Objetivo, performance goal, arquitetura, públicos, budget, lances e criativos.

### RF-07 — Planejamento Google Ads

Tipo/subtipo, metas de conversão, demanda, arquitetura correta, targeting, budget, lances, ads/assets, feed e landing pages conforme aplicável.

### RF-08 — Palavras-chave

Gerar seeds, intenções, clusters, marca/não marca, match types, negativas, grupos e destinos. Não inventar volume, CPC ou forecast.

### RF-09 — Diagnóstico

Analisar níveis e segmentos relevantes, comparar janelas equivalentes, detectar mudanças e decompor entrega, resposta, conversão e qualidade. Cada achado liga evidência, impacto, hipótese principal/alternativa, verificação discriminante e ação exata com responsável, prazo, janela e critérios de sucesso/parada.

### RF-10 — Change set

Registrar plataforma, conta, achados de origem, alvo, antes/depois, justificativa, impacto, risco, reversão, precondições, dependências, responsável, janela, critérios e modo de execução.

### RF-11 — Aprovação

Registrar ID, versão e hash por plataforma. Drift invalida a aprovação.

### RF-12 — Execução

Executar somente ferramentas homologadas. Na V1.1 inicial, Google Ads continua `manual_only` porque o complemento não registra ferramentas de escrita.

### RF-13 — Relatório

Gerar no chat um relatório completo e autossuficiente preservando fontes, atribuições e denominadores por plataforma. Persistir o mesmo resultado no dossiê sem exigir sua abertura.

### RF-14 — Conhecimento oficial

Meta usa snapshot seletivo; Google Ads usa catálogo leve, resumos próprios e consulta oficial ao vivo.

## 11. Google Ads MCP

Servidor oficial: `googleads/google-ads-mcp`, executado localmente com `pipx`.

Capacidades V1:

- Listar customers acessíveis.
- Consultar dados via GAQL.
- Descobrir metadata, métricas e segmentos.

Não presumir:

- Escrita.
- Keyword Planner.
- Customer correto.
- Produção liberada pelo developer token.

Configuração e credenciais ficam fora do Git. Ausência do MCP direciona para arquivos ou contexto manual.

Complemento V1.1: `integrations/google_ads_extended/`, instalado em ambiente local separado. Expõe capability report sanitizado e adapter de Keyword Planner bloqueado por padrão. Exige uso permitido compatível, allowlist local e flag explícito. Não registra escrita.

## 12. Conhecimento Google Ads

Camada intencionalmente leve:

1. Catálogo de URLs oficiais.
2. Resumos de tipos/estrutura, keywords/termos, conversões/lances, ads/assets e MCP/API.
3. Metodologia interna de keywords, arquitetura e diagnóstico.
4. Consulta ao vivo obrigatória para informação mutável ou sensível.

## 13. Dados e métricas

### Universais

Plataforma, conta, moeda, timezone, tipo, janela, comparação, atribuição, fonte, spend, impressions, clicks, CPC, CTR e resultado definido.

### Lead generation

Leads de plataforma, válidos, qualificados, oportunidades, agendamentos, vendas, CPL, CPVL, CPQL, CAC, receita e taxas por etapa.

### E-commerce

Compras, receita atribuída, CPA, ROAS, ticket, margem, ROAS de equilíbrio e MER somente com escopo total compatível.

### Google Ads

Quando aplicável: termos, keywords, match type, negativas, parcela de impressões, perdas por budget/ranking, conversões/valor, ads/assets, dispositivos, rede, geografia e change events.

## 14. Segurança e privacidade

- Configuração MCP fora do repositório.
- Tokens, OAuth, ADC, developer tokens e JSONs nunca registrados.
- IDs mascarados em apresentações.
- Dados reais e exports ignorados.
- Sem aplicação automática de recomendações.
- Sem exclusão ou arquivamento.

## 15. Critérios de sucesso

- Roteamento correto da plataforma em 100% dos casos sintéticos.
- Funcionamento sem MCP.
- Zero mistura silenciosa de contas/plataformas.
- Zero mutação sem aprovação válida.
- Google Ads permanece `manual_only` enquanto `write_tools_registered` não estiver homologado.
- 100% das operações com dossiê.
- 100% das entregas analíticas compreensíveis e decidíveis diretamente no chat.
- 100% dos achados sintéticos com ação, responsável, janela e critérios de sucesso/parada.
- Nenhum segredo ou dado real no Git.

## 16. Testes de aceite

1. Validar 25 módulos, roteador público, metadados e descoberta Codex/Claude Code.
2. Validar schemas e grafo sem ciclos.
3. Comparar regras de Claude e Codex.
4. Rotear Meta, Google Ads e multicanal.
5. Validar modos connected/file/context.
6. Pesquisar keywords sem inventar métricas ausentes.
7. Diagnosticar Google Ads por MCP/export sintético.
8. Gerar dois change sets em demanda multicanal.
9. Bloquear escrita Google Ads e Planner sem capability/allowlist.
10. Bloquear conta/plataforma ambígua.
11. Simular drift e falha parcial Meta.
12. Verificar ausência de segredos e dados reais.
13. Preservar 151 artigos Meta e regressões existentes.
14. Bloquear recuperação Meta para consultas Google Ads e impedir vazamento entre ramos.
15. Rejeitar por schema achados rasos, mudanças sem evidência e dossiês sem trilha de rota.
16. Executar uma homologação única incluindo os testes do complemento Google Ads com `PYTHONPATH` correto.

## 17. Roadmap

### V1.1 atual

Motor multicanal, roteador público automático, Google Ads consultivo, MCP oficial validado, complemento local fail-closed, modo por arquivos, keywords, schemas acionáveis, entrega chat-first e regressões de rota/RAG.

### Homologação seguinte

Ampliar formalmente o uso permitido, homologar Keyword Planner por customer allowlisted e manter escrita ausente.

### Futuro

Adapter de escrita Google Ads com `validate_only`, conta de teste, aprovação versionada e readback; depois Search Console, Trends e GA4.

## 18. Critério final do V1

O V1 está pronto quando nome, contrato, agents, README, PRD, 25 módulos mais roteador, comandos, schemas, templates, conhecimento, matriz, grafo e validações estiverem consistentes; o fluxo funcionar com ou sem MCP; o relatório completo chegar ao chat; e nenhum dado real ou segredo estiver versionado.
