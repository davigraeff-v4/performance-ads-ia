# PRD — META PERFORMANCE IA

**Versão:** 1.0.0-local  
**Data:** 2026-07-31  
**Responsável:** Davi  
**Ambientes:** Claude Code e Codex  
**Estado:** versão pública inicial; homologação operacional em andamento

## 1. Visão geral

O META PERFORMANCE IA é um agente especialista em Meta Ads que ajuda gestores a tomar decisões e realizar otimizações de forma mais assertiva, prática, rápida e rastreável. Ele combina dados da plataforma, dados comerciais fornecidos pelo usuário, documentação oficial Meta e metodologia operacional.

O produto opera como um único agente com 14 skills de tráfego, uma skill de configuração e uma skill transversal de recuperação da Central Meta. O gestor interage com uma entidade; a modularidade existe por trás para garantir consistência, leitura seletiva e testes.

## 2. Problema

Gestores frequentemente precisam decidir sob pressão usando recortes incompletos, janelas incompatíveis ou métricas de plataforma sem resultado comercial. Isso cria riscos:

1. Otimizar CPL sem saber a qualidade do lead.
2. Tratar ROAS atribuído como lucro.
3. Alterar campanhas antes de haver dados suficientes.
4. Comparar períodos diferentes sem considerar sazonalidade ou atraso.
5. Fragmentar estrutura e aprendizado.
6. Aplicar heurísticas universais a contas diferentes.
7. Fazer mudanças sem documentar contexto, aprovação e resultado.
8. Misturar contas, IDs ou configurações.
9. Depender de memória de conversa para retomar uma operação.

## 3. Proposta de valor

O agente entrega uma linha auditável entre:

`objetivo de negócio → qualidade dos dados → diagnóstico → decisão → aprovação → execução → verificação → aprendizado`

Cada operação possui um dossiê Markdown persistente, permitindo revisar por que algo foi recomendado, quem aprovou, o que o MCP executou e qual foi o estado posterior.

## 4. Usuários

### Principal

Davi e gestores de tráfego com conhecimento intermediário ou avançado de Meta Ads.

### Secundários futuros

- Gestores de projeto que precisam interpretar performance.
- Analistas de dados e CRM.
- Lideranças de operação.
- Especialistas de e-commerce e vendas.

## 5. Objetivos do MVP

1. Configurar e diagnosticar o MCP do Meta em Claude Code e Codex.
2. Cadastrar cliente, conta, metas, restrições e fontes.
3. Planejar campanhas de lead generation e e-commerce.
4. Auditar estrutura, mensuração e performance.
5. Recomendar otimizações com evidência e confiança declaradas.
6. Criar change sets versionados.
7. Executar somente mudanças aprovadas e suportadas pelo MCP.
8. Produzir dossiê Markdown de toda operação.
9. Gerar relatórios executivos e operacionais.
10. Manter memória local por cliente.
11. Evoluir conhecimento somente por propostas sanitizadas e aprovadas.

## 6. Fora do escopo

- Google Ads, TikTok Ads ou outras plataformas.
- Produção final de copy ou design.
- Browser automation como fallback automático.
- Exclusão ou arquivamento de ativos.
- Otimização autônoma sem aprovação.
- Dashboard web, banco de dados ou RAG vetorial.
- Garantia de causalidade ou incrementalidade a partir de atribuição observacional.
- Upload de dados sensíveis de clientes ao Git.

## 7. Arquitetura

### Agente

`CLAUDE.md` e `AGENTS.md` representam a mesma persona e contrato, com instruções específicas de cada runtime.

### Skills

- 1 skill de instalação/configuração.
- 4 skills de contexto e mensuração.
- 6 skills de planejamento e construção.
- 4 skills de diagnóstico, otimização, execução e aprendizado.
- 1 skill transversal de recuperação seletiva da Central Meta.

### Estado

- `CLIENTE.md`: memória operacional durável.
- Dossiê `.md`: registro humano completo da operação.
- Bloco JSON no dossiê: estado estruturado validável.
- `dependency_graph.json`: dependências entre skills.
- Schemas: contratos de dados.

### Integração

Endpoint previsto: `https://mcp.facebook.com/ads`. A capacidade concreta é descoberta em runtime; transporte conectado não implica autenticação, acesso à conta ou escrita.

## 8. Requisitos funcionais

### RF-01 — Configuração

Detectar Claude Code ou Codex, verificar o servidor Meta, explicar a mudança, pedir confirmação, configurar, autenticar, testar leitura e detectar escrita. Nunca imprimir segredos.

### RF-02 — Onboarding

Criar `clients/{slug}/CLIENTE.md` com modelo de negócio, conta, metas, funil, restrições, fontes, ciclo de venda, margem e preferências.

### RF-03 — Seleção segura de conta

Confirmar nome, ID mascarado, moeda, timezone, business, pixel/dataset e permissões. Bloquear diante de ambiguidade.

### RF-04 — Mensuração

Avaliar disponibilidade e coerência de Pixel, CAPI, eventos, deduplicação, UTMs, atribuição e dados comerciais. Produzir classificação `confiável`, `utilizável_com_ressalvas` ou `insuficiente`.

### RF-05 — Metas e baseline

Definir KPI principal, indicadores de saúde, meta, baseline, período, fonte, denominador e breakeven quando calculável.

### RF-06 — Planejamento

Converter objetivo comercial em objetivo de campanha, conversão, performance goal, funil, arquitetura, públicos, verba, lances e plano criativo.

### RF-07 — Auditoria e análise

Extrair dados no nível necessário, comparar janelas equivalentes, detectar mudanças recentes, decompor o funil e priorizar diagnósticos.

### RF-08 — Change set

Converter recomendações em uma lista ordenada de mudanças com alvo, antes/depois, justificativa, impacto, risco e reversão.

### RF-09 — Aprovação

Registrar aprovação por ID, versão e hash, separada da execução. Invalidar se o lote ou estado material mudar.

### RF-10 — Execução

Revalidar precondições, chamar somente ferramentas suportadas, registrar resposta por item e capturar snapshot posterior. Sem escrita, fornecer procedimento manual e manter status correto.

### RF-11 — Reversão

Criar novo lote que restaura valores anteriores conhecidos. Exigir nova aprovação; nunca usar reversão para excluir ou arquivar.

### RF-12 — Relatório

Entregar sumário executivo, diagnóstico, fatos, limitações, decisões, mudanças, próximo ponto de leitura e apêndice operacional.

### RF-13 — Memória e conhecimento

Atualizar a ficha do cliente sem apagar histórico. Propor aprendizado sanitizado separado, com aprovação antes de entrar na base versionável.

### RF-14 — Recuperação da Central Meta

Indexar localmente os artigos oficiais por título, categoria e conteúdo. Diante de uma pergunta sobre funcionamento da plataforma, buscar primeiro; ler integralmente o artigo quando houver correspondência exata ou forte; limitar correspondências temáticas aos 1–3 melhores candidatos; e verificar a fonte ao vivo em decisões sensíveis ou potencialmente desatualizadas.

## 9. Requisitos não funcionais

- **Segurança:** fail closed, menor privilégio e nenhuma credencial no projeto.
- **Rastreabilidade:** toda decisão relevante possui fonte e dossiê.
- **Idempotência:** reexecutar verificação não deve duplicar mutação concluída.
- **Portabilidade:** comportamento equivalente em Claude Code e Codex.
- **Legibilidade:** arquivos em português operacional, IDs e campos técnicos preservados quando necessários.
- **Atualidade:** conhecimento oficial com URL e data de verificação.
- **Privacidade:** cliente isolado por pasta; sem dados reais nos exemplos versionáveis.
- **Velocidade:** perguntas críticas consolidadas e skills silenciosas entre checkpoints.

## 10. Dados e métricas

### Campos universais

Conta, moeda, timezone, objeto, janela, comparação, atribuição, extração, spend, impressions, reach, frequency, clicks, link clicks, landing page views, CPM, CTR, CPC e resultados do objetivo.

### Lead generation

Leads Meta, leads válidos, qualificados, oportunidades, agendamentos, vendas, CPL, CPVL, CPQL, CAC, receita e taxas entre etapas. Campos indisponíveis permanecem `null` com motivo; não usar zero.

### E-commerce

View content, add to cart, initiate checkout, purchases, revenue atribuída, CPA, ROAS, ticket, margem, ROAS de equilíbrio e MER quando houver escopo completo.

## 11. Fluxos

### Configurar

`/configuracao-mcp` → detectar → diagnosticar → explicar → confirmar → configurar → autenticar → validar → dossiê.

### Planejar/criar

`/planejar-campanha` ou `/criar-campanha` → intake → conta → mensuração → metas → estratégia → arquitetura → públicos → verba → criativos → plano/change set → aprovação → execução separada.

### Auditar/analisar

`/auditar-conta` ou `/analisar-campanha` → escopo → fontes → qualidade → janela → diagnóstico → recomendações → dossiê `analysis_only`.

### Otimizar

`/otimizar-campanha` → diagnóstico → change set → aprovação → revalidação → execução → snapshot posterior → aprendizado.

## 12. Regras de decisão

- Não inferir conta, moeda, objetivo, oferta, restrição ou aprovação.
- Pode inferir hipóteses de público, funil e criativo se rotuladas.
- Dados insuficientes reduzem confiança ou bloqueiam ação; não justificam chute.
- Uma boa métrica de plataforma não supera evidência comercial contrária.
- Mudança que pode afetar aprendizado ou revisão deve aparecer como risco.

## 13. Estados do dossiê

- `draft`: escopo ainda em construção.
- `proposed`: análise/change set apresentado.
- `approved`: versão aprovada, ainda não executada.
- `executing`: preflight passou e execução iniciou.
- `executed`: todos os itens aplicáveis confirmados.
- `partial_failure`: parte executada, parte falhou.
- `failed`: nenhuma mudança concluída ou preflight bloqueado.
- `reverted`: lote de reversão confirmado.
- `analysis_only`: análise revisada sem mutação.

## 14. Segurança e privacidade

- Configuração MCP fora do repositório.
- Tokens e cookies nunca registrados.
- IDs mascarados em apresentações; IDs integrais somente no estado local estritamente necessário.
- Dados pessoais de leads não são necessários para análise agregada.
- Exportações reais ficam ignoradas.
- Nenhum dado real de cliente, exportação ou segredo no Git.

## 15. Base de conhecimento

Quatro camadas:

1. `meta-help-center/`: snapshot local de 151 artigos oficiais, com índice, URL e data de extração.
2. `official-meta/`: resumos operacionais de fontes oficiais, URL e revisão.
3. Metodologia: decisões internas para diagnóstico, planejamento e teste.
4. `sanitized-learnings/`: somente padrões aprovados e anônimos.

Fontes oficiais prevalecem sobre metodologia em funcionamento e política. A metodologia prevalece sobre palpite não sustentado.

A camada integral usa recuperação seletiva por título e tópico, nunca carregamento total. O snapshot não equivale a retreinamento e não substitui verificação ao vivo para política, cobrança, segurança, elegibilidade, restrições ou mudanças de produto. A publicação preserva atribuição e URLs originais; conteúdo de terceiros permanece sujeito aos direitos e termos de seus titulares.

## 16. Critérios de sucesso

- Reduzir tempo até um diagnóstico utilizável.
- Evitar perguntas repetidas sobre cliente conhecido.
- Zero mutação sem aprovação válida.
- Zero exclusão/arquivamento.
- 100% das operações com dossiê.
- 100% das recomendações com evidência e limitação.
- 100% das execuções com snapshot posterior e resultado por item.
- Nenhum segredo ou dado real incluído no Git.

## 17. Testes de aceite

1. Validar 16 skills e metadados.
2. Validar schemas e grafo.
3. Comparar regras de Claude e Codex.
4. Executar casos sintéticos de lead e e-commerce.
5. Simular drift após aprovação.
6. Simular falha parcial.
7. Bloquear exclusão.
8. Bloquear conta ambígua.
9. Detectar tracking insuficiente.
10. Verificar ausência de segredos e dados reais no repositório.
11. Validar 151 artigos, metadados, títulos e URLs únicos.
12. Testar busca exata, temática, sem acento e resultado fraco.

## 18. Roadmap

### V1 — Modelo local

Documentação, skills, base inicial, templates, schemas, exemplos sintéticos e testes estruturais.

### V1.1 — Homologação

MCP nos dois ambientes, leitura real autorizada, um dossiê real e uma operação controlada aprovada.

### V1.2 — Publicação sanitizada

Auditoria de segredos concluída e publicação pública do motor, base atribuída e exemplos sintéticos, sem clientes reais.

### V2

Calibração com mais casos, integrações comerciais, relatórios recorrentes e testes de impacto mais robustos.

## 19. Critério final do MVP

O MVP público está pronto quando PRD, README, contrato, 16 skills, comandos, schemas, templates, os 151 artigos, a recuperação seletiva e as regressões estiverem consistentes; Claude e Codex conseguirem seguir os mesmos fluxos; e nenhum dado real ou segredo estiver versionado.
