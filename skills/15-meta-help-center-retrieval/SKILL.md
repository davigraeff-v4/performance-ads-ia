---
name: 15-meta-help-center-retrieval
description: Localiza e lê seletivamente artigos oficiais da Central de Ajuda da Meta armazenados em knowledge/meta-help-center. Use antes de responder dúvidas sobre funcionamento, configuração, políticas, faturamento, contas, campanhas, públicos, criativos, mensuração, catálogo, otimização ou solução de problemas do Meta Ads; também use quando o texto do usuário coincidir total ou parcialmente com o título de um artigo.
---

# Recuperação da Central de Ajuda Meta

## Objetivo

Dar ao agente acesso confiável à base local sem carregar os 151 artigos no contexto. Esta skill é transversal: ela complementa as skills operacionais, mas não substitui dados atuais da conta, metodologia nem validação online quando necessária.

## Dois modos de uso

1. **Dúvida:** o gestor pergunta como algo funciona. A consulta é a pergunta original.
2. **Checagem de premissas:** em diagnóstico, mudanças e relatório, a consulta é cada premissa de mecanismo que sustenta um achado ou mudança (ex.: "conjuntos com públicos sobrepostos competem no mesmo leilão"). Este modo roda em toda rota que planeja esta skill, mesmo sem pergunta do gestor.

Na checagem de premissas:

- buscar com `scripts/search_meta_help.py` usando a premissa como consulta e, também, `ads_get_help_article` do conector Meta (fonte oficial ao vivo, costuma achar o artigo certo quando a base local não tem);
- ler o artigo encontrado antes de julgar; resultado de busca não é leitura;
- dar o veredito: **sustenta**, **contradiz** ou **sem cobertura**, com título, URL e uma nota curta;
- se contradiz, corrigir o texto e o plano antes de apresentar e contar isso ao gestor na seção "Checagem com boas práticas";
- registrar cada checagem em `knowledge_checks` do spec do dossiê.

A busca local tem baixa precisão para premissas escritas como afirmação (costuma trazer artigos de política). Se os três primeiros resultados não tratarem do tema, reescreva a consulta com os termos do produto (ex.: "sobreposição de leilão") ou use o conector.

## Entrada

- Pergunta original do usuário, sem reescrever antes da busca.
- Contexto operacional, quando houver: conta, objetivo, recurso ou erro.
- Sensibilidade da decisão: informativa, operacional, financeira, política ou segurança.

## Regra if/else obrigatória

1. **Se** a pergunta for sobre Meta Ads, Business Suite, Gerenciador de Anúncios, Pixel, CAPI, públicos, catálogo, políticas, faturamento ou portfólio empresarial, **então** execute a busca seletiva.
2. **Se** houver correspondência exata ou forte com um título, **então** leia integralmente o artigo correspondente antes de responder.
3. **Se** houver apenas correspondência temática, **então** leia os 1–3 artigos mais aderentes; não leia a base inteira.
4. **Se** os resultados forem fracos ou ambíguos, **então** consulte primeiro `knowledge/meta-help-center/INDEX.md`, refine a busca e só depois abra candidatos.
5. **Se** nenhuma fonte local responder, **então** declare a lacuna e use a metodologia local ou pesquisa oficial ao vivo, conforme o caso.
6. **Se** a resposta orientar uma decisão sensível, tratar de política, elegibilidade, cobrança, restrição, segurança ou comportamento possivelmente alterado, **então** verificar também a URL oficial ao vivo.

## Busca

Execute a partir da raiz do projeto:

```bash
python3 scripts/search_meta_help.py "pergunta original do usuário" --platform meta --limit 3
```

Para inspecionar somente correspondências de título:

```bash
python3 scripts/search_meta_help.py "trecho do título" --platform meta --title-only --limit 5
```

A busca roda em modo híbrido por padrão (`--mode hybrid`): primeiro tenta correspondência de título; só quando o título ficar `related`/`weak` ela também considera um sinal semântico local (índice vetorial em `knowledge/.vector-index/`, gerado por `scripts/build_knowledge_vector_index.py`) para achar candidatos que uma pergunta parafraseada não bateu por título nenhum. Cada resultado vem marcado com `signal`: `lexical` (achou por título/corpo), `vector` (só achou pelo sentido) ou `hybrid` (os dois sinais concordaram). Se o índice vetorial não estiver construído localmente, o buscador cai automaticamente para o modo lexical de sempre, sem quebrar — use `--mode lexical` para forçar esse comportamento manualmente.

Interprete a classificação:

- `exact`: título normalizado idêntico à consulta.
- `strong`: correspondência forte; leitura obrigatória do primeiro resultado, independente do `signal`.
- `related`: candidato temático; valide o título e leia até três resultados.
- `weak`: não sustenta resposta sozinho; refine ou consulte o índice.

## Processo

1. Preservar a pergunta original como consulta inicial.
2. Rodar o buscador, que lê primeiro apenas o `INDEX.md`; somente se o índice produzir correspondências fracas ele varre o conteúdo como sinal de fallback, sem injetá-lo no contexto.
3. Registrar os candidatos retornados.
4. Abrir integralmente somente os artigos necessários.
5. Separar o que a fonte oficial informa do que a metodologia recomenda.
6. Verificar `extraido_em` e a URL original no frontmatter.
7. Quando a consulta fizer parte de uma operação, registrar na candidata título, caminho local, URL, data de extração e data da consulta; persistir no dossiê somente após aprovação editorial.
8. Responder por paráfrase; não reproduzir extensamente o artigo.

## Saída

- Artigos consultados, com título e URL.
- Resposta apoiada no conteúdo efetivamente lido.
- Data/frescor da fonte e necessidade ou não de validação ao vivo.
- Lacunas, conflitos ou limitações.
- Distinção explícita entre `Meta informa` e `metodologia recomenda`.

## Gates

- Não afirmar que leu um artigo apenas porque o buscador encontrou o título.
- Não carregar todos os arquivos como prevenção genérica.
- Não tratar o snapshot local como garantia de regra atual.
- Não inventar disponibilidade de recurso na conta; confirmar via MCP quando aplicável.
- Não usar a base para contornar o contrato de aprovação e execução.
- Não chamar sem `--platform meta`. O buscador falha fechado para `google_ads` e para consulta explicitamente conflitante; nesse caso, rotear para a skill `17`. O gate de plataforma vale igualmente para o sinal lexical e o vetorial — cada plataforma tem seu próprio índice vetorial, fisicamente separado, então não há como um sinal semântico vazar de uma base para a outra.
- Não afirmar que leu um artigo apenas porque o sinal vetorial encontrou similaridade; abrir e ler o arquivo indicado antes de responder, igual já vale para o sinal lexical.

## Exemplos

**Pergunta:** “Como funciona a meta de ROAS?”  
**Ação:** buscar a pergunta; abrir integralmente `sobre-a-meta-de-roas.md`; responder com a URL oficial e ressalvas de elegibilidade.

**Pergunta:** “Meu pixel está duplicando eventos.”  
**Ação:** buscar por título e tópico; ler os artigos mais aderentes de mensuração/deduplicação; cruzar com a skill `03-measurement-data-quality`.

**Pergunta (parafraseada, sem bater título nenhum):** “meu pixel está contando o mesmo evento duas vezes quando uso CAPI e o pixel do site juntos”  
**Ação:** o título não bate com nenhum artigo (`related`/`weak` no sinal lexical); o sinal vetorial complementa e traz “Sobre o Pixel da Meta” e “Sobre a API de Conversões” como candidatos por sentido. Ler os artigos indicados antes de responder, exatamente como faria com um match por título.

**Pergunta:** “Devo reduzir o orçamento desta campanha em 20%?”  
**Ação:** usar a base para funcionamento de orçamento/aprendizado, mas decidir com dados, baseline e metodologia; não converter documentação oficial em regra universal.
