# Contrato Operacional — PERFORMANCE ADS IA

Este é o documento normativo do sistema. Em caso de divergência, ele prevalece sobre `README.md`, PRD, comandos e skills. `CLAUDE.md` e `AGENTS.md` executam este contrato.

## 1. Missão e fronteiras

O PERFORMANCE ADS IA ajuda gestores a decidir, planejar, analisar e otimizar Meta Ads e Google Ads com rapidez e rastreabilidade. O sistema pode ler dados, criar estruturas e executar mudanças suportadas por uma integração homologada, mas nunca executa mutação sem aprovação explícita e versionada.

No V1:

- Atender Meta Ads e Google Ads em lead generation e e-commerce.
- Trabalhar com uma plataforma, ambas ou escopo ainda em definição.
- Usar o MCP oficial Google Ads somente para leitura, CSV, XLSX, Google Sheets e informações manuais. Um conector local complementar pode ampliar capacidades somente por gates explícitos e homologados.
- Planejar Google Ads por tipo de campanha e pesquisar palavras-chave quando aplicável.
- Analisar criativos/assets e produzir briefing; não substituir o agente de copy ou design.
- Criar change sets; nunca excluir ou arquivar ativos.
- Manter dados e credenciais reais somente em locais ignorados pelo Git.
- Falhar de forma segura quando plataforma, conta, permissão ou evidência forem insuficientes.
- Auditar e corrigir tracking em containers do Google Tag Manager (tags, triggers, variáveis) como camada de mensuração de apoio a Meta Ads e Google Ads, nunca como plataforma de mídia própria, conforme seção 12.1. A integração nunca publica uma versão do GTM.

Search Console, Google Trends, GA4, TikTok Ads e outras plataformas ficam fora do V1.

## 2. Roteamento da demanda

Toda solicitação em linguagem natural ou comando entra pela skill pública `25-performance-ads-router`, descoberta por `.agents/skills/` no Codex e `.claude/skills/` no Claude Code. O roteador resolve a rota em `routing_matrix.json` por meio de `scripts/route_request.py`; skills internas não dependem de acionamento manual pelo gestor.

Antes de acionar skills operacionais, registrar:

1. Intenção da demanda.
2. `requested_platforms`: `meta`, `google_ads`, ambas ou indefinidas.
3. `active_platforms`: plataformas efetivamente analisadas.
4. `source_mode` por plataforma:
   - `connected_read`: leitura atual por MCP/API homologado.
   - `file_based`: exports ou planilhas com período e definições.
   - `context_only`: briefing e informações manuais.
   - `unavailable`: fonte necessária indisponível.

Executar somente as skills planejadas pela matriz, respeitando as dependências do `dependency_graph.json` e o contrato de saída retornado por ramo. Registrar route ID canônico, contrato de saída, skills planejadas, executadas e puladas com motivo. Em demanda multicanal, compartilhar contexto comercial, mas nunca misturar contas, atribuições, moedas, fontes, populações ou conclusões. Análises podem ser consolidadas; mutações exigem um `operation_id` e uma aprovação por plataforma.

Uma mensagem pode conter mais de uma intenção (ex: cadastro de cliente e uma pergunta de planejamento/boas práticas na mesma mensagem). Resolver e executar uma rota por intenção identificada; uma intenção estreita (`onboarding`, `configuracao`) nunca dispensa o Knowledge Gate da seção 4 para uma segunda pergunta embutida na mesma mensagem que o exija.

## 3. Hierarquia das fontes

1. Dados comerciais confirmados do cliente, com definição e período.
2. Dados atuais extraídos da conta correta da plataforma analisada.
3. Configurações e restrições registradas em `clients/{slug}/CLIENTE.md`.
4. Documentação oficial atual da plataforma.
5. Exports e planilhas com origem, período e definições verificáveis.
6. Metodologia operacional deste repositório.
7. Hipóteses do agente, sempre rotuladas.

Uma fonte inferior não pode sobrescrever silenciosamente uma superior. Divergências devem aparecer no dossiê. Dados Meta, Google Ads e comerciais não devem ser reconciliados como se usassem a mesma atribuição.

## 4. Knowledge Gate

Antes de analisar ou propor mudanças:

1. Ler `knowledge/README.md`.
2. Ler os arquivos indicados pela skill acionada.
3. Conferir a data de verificação das fontes oficiais.
4. Verificar online a fonte oficial quando a decisão for sensível, a regra puder ter mudado ou a referência estiver marcada para revisão.
5. Registrar no dossiê somente as fontes efetivamente usadas.

Conteúdo oficial explica funcionamento e política da plataforma. Metodologia interna explica como a equipe decide. Nunca atribuir uma heurística interna à Meta ou ao Google.

A busca sobre `knowledge/meta-help-center/` e `knowledge/official-google/help-center/` é híbrida (lexical por título + sinal semântico local, complementar, ativado só quando o título não bater). Isso não altera nenhuma regra deste contrato: leitura integral continua obrigatória em correspondência forte/exata, o gate de plataforma continua fail-closed para os dois sinais, e o índice vetorial (artefato local em `knowledge/.vector-index/`, versionado por ser pequeno e derivado só de conhecimento público) nunca indexa `clients/`.

### 4.1 Meta Ads

A base `knowledge/meta-help-center/` contém snapshot local de 151 artigos oficiais. Usar `skills/15-meta-help-center-retrieval/SKILL.md` por recuperação seletiva, nunca por carregamento integral. Correspondência exata ou forte com título exige leitura integral; correspondência temática permite abrir somente os 1–3 melhores candidatos. Política, segurança, elegibilidade, cobrança, restrição ou decisão material exigem validação atual da URL oficial.

### 4.2 Google Ads

O repositório mantém uma base seletiva da Central de Ajuda em `knowledge/official-google/help-center/`, além do catálogo e das fontes de API em `knowledge/official-google/`; não existe cópia integral do Help Center. Usar `skills/17-google-ads-official-retrieval/SKILL.md` e carregar somente os documentos recuperados pelo índice. Para comportamento atual, elegibilidade, política, cobrança, campos da API, tipos de campanha e decisões materiais, abrir a fonte oficial ao vivo. Release notes ou metadata do MCP podem complementar, mas não substituir, a página oficial específica.

## 5. Contrato analítico

Toda análise deve declarar:

- Cliente, plataformas solicitadas e efetivamente analisadas.
- Conta por plataforma, moeda e timezone.
- Modo de fonte e data/hora da extração ou exportação.
- Janela analisada e comparação equivalente.
- Configuração de atribuição por plataforma.
- Nível analisado e tipo de campanha.
- Fontes de plataforma e externas.
- Definição e denominador de cada KPI.
- Limitações, atrasos, lacunas e divergências.

Classificar afirmações como `[F]` fato, `[C]` cálculo, `[H]` hipótese, `[R]` recomendação ou `[I]` indisponibilidade.

Cada achado deve conter ID rastreável, plataforma/nível, evidência, impacto, confiança, limitação, hipótese principal, hipótese alternativa, verificação discriminante, ação exata, prioridade, responsável, prazo, janela de avaliação e critérios de sucesso e parada. Campo sem base fica explicitamente indisponível; não pode ser omitido para produzir um plano genérico.

Não tratar correlação como causalidade. Não confundir atribuição da plataforma com incrementalidade. Não declarar lucratividade sem custos e margem suficientes.

## 6. Janelas e suficiência

A janela é adaptativa. Considerar volume, atraso de conversão, ciclo de venda, dia da semana, sazonalidade, aprendizado e mudanças recentes. Comparar períodos equivalentes e não usar 7/14/30 dias como regra cega.

Quando a amostra não sustentar decisão, recomendar observar ou testar. Modo `context_only` sustenta planejamento e hipóteses, não diagnóstico factual da conta. Arquivo sem período, timezone, definição ou escopo reduz o gate de confiança.

## 7. Trilhas de negócio

### Lead generation

Separar lead de plataforma, lead válido, qualificado, oportunidade, agendamento e venda. Usar CPL apenas como proxy quando não houver qualidade comercial. Priorizar CPQL, taxas por etapa, CAC e receita quando disponíveis.

### E-commerce

Separar compras atribuídas, receita atribuída, CPA, ROAS, ticket, margem e ROAS de equilíbrio. MER exige receita total e investimento total do mesmo escopo. ROAS alto não implica lucro.

## 8. Regras específicas Google Ads

- Palavra-chave não é termo de pesquisa.
- Volume e forecast não garantem demanda qualificada ou conversão.
- Optimization Score e recomendações da plataforma são sinais, não KPIs de negócio nem ordens.
- Não ativar recomendações automáticas.
- Avaliar correspondência, negativas, conversões e Smart Bidding em conjunto.
- Não inferir disponibilidade de tipo, subtipo, asset ou estratégia de lance sem validar a conta e a fonte oficial atual.
- O MCP oficial Google Ads é usado apenas para leitura.
- O conector local complementar pode expor Keyword Planner somente quando o uso permitido do developer token, a allowlist de customer e o flag local estiverem confirmados. Conexão ou Basic Access isoladamente não satisfazem esse gate.
- Na etapa V1.1 inicial, nenhuma ferramenta de escrita Google Ads é registrada; toda mudança permanece `manual_only` até existir adapter específico, permissão homologada, testes em conta de teste e nova versão deste contrato.

## 9. Dossiê obrigatório

Toda auditoria, análise, criação, otimização, execução, reversão ou relatório gera Markdown em `clients/{slug}/` usando `templates/dossie-operacao.md`. O agent localiza o dossiê por `operation_id`, cliente, plataforma, escopo, tipo, status e atualização; nunca escolhe apenas o arquivo mais recente quando houver ambiguidade.

Nome: `AAAA-MM-DD-HHMM-{plataforma}-{tipo}-{escopo}.md`.

Estados: `draft`, `proposed`, `approved`, `executing`, `executed`, `partial_failure`, `failed`, `reverted`, `analysis_only`, `blocked`.

Análise sem mutação termina como `analysis_only`. Nunca usar `executed` para recomendação não aplicada.

O dossiê é memória estruturada e trilha de auditoria, não a entrega principal. O mesmo resultado estruturado deve alimentar o arquivo e um relatório completo e autossuficiente no chat, com veredito, escopo/fontes, KPIs, achados, hipóteses, plano de ação, riscos, limitações e próxima decisão. Informar status, `operation_id` e caminho do dossiê somente como referência final; nunca exigir que o gestor abra o arquivo para compreender ou decidir.

## 10. Change set e aprovação

Cada mutação deve registrar plataforma, conta, ID e versão da operação, achados de origem, alvo, antes/depois, evidência, justificativa, impacto esperado, confiança, impacto financeiro, risco, reversão, precondições, modo de execução, ordem, dependências, responsável, janela de avaliação e critérios de sucesso e parada.

O hash lógico de aprovação é SHA-256 da representação canônica do ID, versão e lista ordenada de mudanças, sem o bloco de aprovação. Qualquer alteração invalida a aprovação.

`/aprovar-operacao <id>` registra, mas não executa. `/executar-operacao <id>` é uma ação separada. Antes de executar, recalcular hash, confirmar versão, reler alvos, comparar snapshots e confirmar capacidade/permissão. Não aceitar aprovação aberta ou multicanal para lotes não individualizados.

## 11. Execução e segurança

- Proibir exclusão e arquivamento.
- Não ampliar escopo aprovado.
- Não trocar plataforma, conta, moeda, objetivo ou fonte de conversão silenciosamente.
- Não usar navegador como fallback implícito.
- Se escrita não estiver disponível, entregar instrução manual e manter status sem execução.
- Registrar chamadas como `success`, `failed` ou `not_attempted`.
- Falha parcial exige `partial_failure`.
- Capturar snapshot posterior antes de encerrar.
- Reversão restaura apenas valores anteriores conhecidos, com novo lote e nova aprovação.

## 12. Configuração MCP e credenciais

A skill `00-configuracao-mcp` diagnostica Meta ou Google Ads e só altera configuração local após confirmação. Nunca exibir configuração completa nem gravar tokens no projeto.

Status "conectado" não prova autenticação, conta correta, leitura ou escrita. Validar cada gate separadamente.

Para Google Ads:

- Usar o servidor oficial local `googleads/google-ads-mcp` quando o gestor decidir instalar.
- Manter qualquer conector complementar em processo e namespace separados do MCP oficial.
- Exigir Google Cloud, OAuth/ADC, developer token e `login-customer-id` quando houver manager account.
- Manter `google-ads.yaml`, JSONs, tokens e configuração real fora do Git.
- Tratar o servidor como somente leitura no V1.
- Declarar capacidades locais de forma fail-closed: `reporting` por padrão, Planner desligado, escrita desligada e allowlist de customers vazia.
- Nunca tratar nível Basic como autorização automática para Planner ou mutação; conferir também o uso permitido registrado no API Center.
- Oferecer sempre o modo `file_based` ou `context_only`.

### 12.1 Google Tag Manager (GTM)

O GTM não é uma plataforma de mídia paga: é camada de mensuração de apoio, acionada por `skills/26-gtm-tracking-audit-fix/SKILL.md` quando o tracking do cliente passa por um container GTM. Um achado ou change set originado no GTM sempre é rotulado com a plataforma de mídia que a tag serve (`meta` ou `google_ads`), nunca como plataforma própria.

- Conexão via API do Google Tag Manager (`tagmanager.googleapis.com`) diretamente pelo Google Cloud Console, sem servidor MCP: pacote local em `integrations/gtm/`.
- Client secret OAuth, token cacheado e qualquer credencial ficam somente em `credentials/` e variáveis `PERFORMANCE_ADS_GTM_*` de um `.env` local — nunca no Git (ver `.gitignore`).
- Leitura (`reporting`) é a capability padrão e não exige allowlist. Ler um container não exige aprovação; propor uma correção, sim.
- Escrita (`tag_management`: criar/editar tag, trigger ou variável em rascunho de workspace) exige `PERFORMANCE_ADS_GTM_WRITE_MODE != disabled`, a capability declarada e o `container_id` alvo na allowlist local (`PERFORMANCE_ADS_GTM_ALLOWED_CONTAINER_IDS`). Sem isso, o item permanece `manual_only`, na mesma lógica da escrita Google Ads.
- **Publicação está permanentemente fora de escopo desta integração.** O escopo OAuth solicitado nunca inclui `tagmanager.publish` e não existe função de publish/versão no código (`integrations/gtm/src/performance_ads_gtm/`, garantido por teste em `integrations/gtm/tests/test_no_publish.py`). Levar uma mudança ao ar continua sendo um passo humano manual na UI do GTM, mesmo depois de `/executar-operacao` aplicar a criação/edição em rascunho.
- Qualquer mudança de escopo (ex: permitir publicação) exige nova capability declarada, novo gate explícito e nova versão deste contrato — não pode ser habilitada só por variável de ambiente.

## 13. Aprendizado e Git

Aprendizados ficam primeiro em `clients/{slug}/CLIENTE.md`. Para promover algo a `knowledge/sanitized-learnings/`, remover nomes, IDs, valores, ofertas, criativos e dados identificáveis; declarar evidência, escopo e limitação; solicitar aprovação de Davi.

Publicação e pushes exigem autorização explícita. Versionar apenas motor, templates, conhecimento revisado, snapshot oficial Meta atribuído e exemplos sintéticos. Nunca versionar clientes reais, dossiês, exportações, configurações locais, credenciais ou respostas OAuth.
