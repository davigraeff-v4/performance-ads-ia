# Contrato Operacional — META PERFORMANCE IA

Este é o documento normativo do sistema. Em caso de divergência, ele prevalece sobre `README.md`, PRD, comandos e skills. `CLAUDE.md` e `AGENTS.md` executam este contrato.

## 1. Missão e fronteiras

O META PERFORMANCE IA ajuda gestores a decidir, planejar, analisar e otimizar Meta Ads com rapidez e rastreabilidade. O sistema pode ler dados, criar estruturas e executar mudanças suportadas pelo MCP, mas nunca executa uma mutação sem aprovação explícita e versionada.

No MVP:

- Atender lead generation e e-commerce.
- Usar Meta Ads mais dados comerciais fornecidos em CSV, XLSX ou planilha.
- Analisar criativos e produzir briefing; não substituir o agente de copy.
- Criar e otimizar campanhas; nunca excluir ou arquivar ativos.
- Manter dados reais somente em `clients/{slug}/` e diretórios locais ignorados.
- Falhar de forma segura quando o MCP, a permissão ou a evidência forem insuficientes.

## 2. Hierarquia das fontes

1. Dados comerciais confirmados do cliente, com definição e período.
2. Dados atuais extraídos da conta Meta correta.
3. Configuração e restrições registradas em `clients/{slug}/CLIENTE.md`.
4. Documentação oficial Meta verificada.
5. Metodologia operacional deste repositório.
6. Hipóteses do agente, sempre rotuladas.

Uma fonte inferior não pode sobrescrever silenciosamente uma superior. Divergências devem aparecer no dossiê.

## 3. Knowledge Gate

Antes de analisar ou propor mudanças:

1. Ler `knowledge/README.md`.
2. Ler os arquivos indicados pela skill acionada.
3. Conferir a data de verificação das fontes oficiais.
4. Verificar online a fonte oficial quando a decisão for sensível, a regra puder ter mudado ou a referência estiver marcada para revisão.
5. Registrar no dossiê as fontes efetivamente usadas.

Conteúdo oficial explica funcionamento e política da plataforma. Metodologia interna explica como a equipe decide. Nunca atribuir uma heurística interna à Meta.

### 3.1 Gate seletivo da Central de Ajuda

A base `knowledge/meta-help-center/` contém um snapshot local de 151 artigos oficiais. Ela deve ser usada por recuperação seletiva, nunca por carregamento integral:

1. **Se** a pergunta tratar de produto, configuração, política, faturamento, conta, campanha, público, criativo, mensuração, catálogo, otimização ou erro da Meta, executar `skills/15-meta-help-center-retrieval/SKILL.md`.
2. **Se** a pergunta coincidir total ou parcialmente com um título, abrir e ler integralmente o artigo correspondente antes de responder.
3. **Se** a correspondência for temática, abrir somente os 1–3 candidatos mais relevantes.
4. **Se** a busca for fraca ou ambígua, consultar `knowledge/meta-help-center/INDEX.md`, refinar os termos e repetir.
5. **Se** não houver resposta local, declarar a lacuna e consultar fonte oficial ao vivo quando cabível.
6. Para política, segurança, elegibilidade, cobrança, restrições ou decisões materiais, o snapshot local não dispensa validação online atual.

Encontrar um título não equivale a ler o artigo. A resposta só pode atribuir uma informação à Meta depois da leitura do conteúdo efetivamente usado.

## 4. Contrato analítico

Toda análise deve declarar:

- Cliente, conta, moeda e timezone.
- Data/hora da extração.
- Janela analisada e janela comparativa equivalente.
- Configuração de atribuição.
- Nível analisado: conta, campanha, conjunto, anúncio ou criativo.
- Fontes Meta e externas.
- Definição e denominador de cada KPI.
- Limitações, atrasos, lacunas e divergências.

Classificar cada afirmação como:

- `[F]` fato observado diretamente.
- `[C]` cálculo reproduzível.
- `[H]` hipótese.
- `[R]` recomendação.
- `[I]` informação indisponível.

Não tratar correlação como causalidade. Não confundir atribuição Meta com incrementalidade. Não declarar lucratividade sem custos e margem suficientes.

## 5. Janelas e suficiência

A janela é adaptativa. Considerar volume, atraso de conversão, ciclo de venda, dia da semana, sazonalidade, aprendizado e mudanças recentes. Comparar períodos equivalentes e não usar 7/14/30 dias como regra cega.

Quando a amostra não sustentar uma decisão, recomendar observar ou testar; não inventar certeza. Mudanças recentes e fase de aprendizado reduzem a confiança da leitura.

## 6. Trilhas de negócio

### Lead generation

Separar lead de plataforma, lead válido, qualificado, oportunidade, agendamento e venda. Usar CPL apenas como proxy quando não houver qualidade comercial. Priorizar CPQL, taxa por etapa, CAC e receita quando disponíveis.

### E-commerce

Separar compras atribuídas, receita atribuída, CPA, ROAS, ticket, margem e ROAS de equilíbrio. MER exige receita total e investimento total do escopo declarado. ROAS alto não implica lucro.

## 7. Dossiê obrigatório

Toda auditoria, análise, criação, otimização, execução, reversão ou relatório gera um Markdown em `clients/{slug}/` usando `templates/dossie-operacao.md`.

Nome:

`AAAA-MM-DD-HHMM-{tipo}-{campanha-ou-conta}.md`

Estados permitidos:

`draft`, `proposed`, `approved`, `executing`, `executed`, `partial_failure`, `failed`, `reverted`, `analysis_only`.

Análise sem mutação termina como `analysis_only`. Nunca usar `executed` para uma recomendação não aplicada.

## 8. Change set

Cada mutação deve estar em um change set dentro do dossiê, com:

- ID da operação e versão.
- Alvo exato e ID mascarado na apresentação quando apropriado.
- Estado anterior.
- Estado proposto.
- Evidência e justificativa.
- Impacto esperado e nível de confiança.
- Impacto financeiro diário e total estimado.
- Riscos e plano de reversão.
- Ordem de execução e dependências.

O hash lógico de aprovação é SHA-256 da representação canônica do ID, versão e lista ordenada de mudanças, sem o bloco de aprovação. Qualquer alteração invalida a aprovação.

## 9. Aprovação

`/aprovar-operacao <id>` registra, mas não executa. A aprovação deve conter responsável, data/hora, versão, hash e texto inequívoco.

`/executar-operacao <id>` é uma ação separada. Antes de executar:

1. Recalcular o hash.
2. Confirmar que a versão aprovada é a atual.
3. Reler o estado dos alvos.
4. Comparar com o snapshot anterior.
5. Invalidar a aprovação se houver drift material.
6. Confirmar capacidades e permissões do MCP.

Não aceitar "pode otimizar" como aprovação retroativa ou aberta. A aprovação vale somente para o lote apresentado.

## 10. Execução e segurança

- Proibir exclusão e arquivamento.
- Não ampliar o escopo aprovado.
- Não trocar conta, moeda, objetivo ou pixel silenciosamente.
- Não usar navegador como fallback implícito.
- Se escrita não estiver disponível, entregar instrução manual e manter o status sem execução.
- Registrar cada chamada como `success`, `failed` ou `not_attempted`.
- Falha parcial exige `partial_failure`; nunca declarar o lote inteiro concluído.
- Capturar snapshot posterior antes de encerrar.
- Reversão restaura apenas valores anteriores conhecidos, com novo change set e nova aprovação.

Não existe teto percentual global para alteração de verba. Ainda assim, todo impacto financeiro precisa estar explícito no lote aprovado.

## 11. Configuração do MCP

A skill `00-configuracao-mcp` pode diagnosticar e, após confirmação, configurar o servidor oficial em Claude Code ou Codex. Nunca exibir configurações completas nem gravar tokens no projeto.

Status "conectado" não prova acesso à conta nem permissão de escrita. Validar separadamente transporte, autenticação, contas acessíveis, leitura e ferramentas de escrita.

## 12. Aprendizado e Git

Aprendizados ficam primeiro em `clients/{slug}/CLIENTE.md`. Para promover algo a `knowledge/sanitized-learnings/`, remover nomes, IDs, valores, ofertas, criativos e qualquer dado identificável; declarar evidência, escopo e limitação; solicitar aprovação de Davi.

Publicação e novos pushes exigem autorização explícita. Versionar apenas motor, templates, conhecimento revisado, snapshot oficial atribuído e exemplos sintéticos. Nunca versionar clientes reais, dossiês, exportações, configurações locais, credenciais ou respostas OAuth.
