<!-- Referência do módulo `revisor`; etapa `revisor/meta` nas rotas. -->

# Recuperação da Central de Ajuda Meta

## Objetivo

Dar ao agente acesso confiável à base local sem carregar os 153 artigos no contexto. Esta skill é transversal: ela complementa as skills operacionais, mas não substitui dados atuais da conta, metodologia nem validação online quando necessária.

## Dois modos de uso

1. **Dúvida:** o gestor pergunta como algo funciona. A consulta é a pergunta original.
2. **Checagem de premissas:** em diagnóstico, mudanças e relatório, a consulta é cada premissa de mecanismo que sustenta um achado ou mudança (ex.: "conjuntos com públicos sobrepostos competem no mesmo leilão"). Este modo roda em toda rota que planeja esta skill, mesmo sem pergunta do gestor.

Na checagem de premissas:

- rodar o revisor com todas as premissas de uma vez:

  ```bash
  python3 scripts/kb_check.py --platform meta "premissa 1" "premissa 2"
  ```

  ele devolve, por premissa, os artigos candidatos (com os trechos mais ligados à premissa), quais precisam ser lidos por inteiro e um esqueleto de `knowledge_checks` com o veredito em branco;
- consultar também `ads_get_help_article` do conector Meta (fonte oficial ao vivo). Ela acerta melhor com o nome do produto em inglês ("auction overlap") e devolve um resumo em inglês: use para confirmar e para achar artigos que a base local não tem, citando a URL oficial;
- ler o artigo antes de julgar; resultado de busca e trecho não são leitura;
- dar o veredito: **sustenta**, **contradiz** ou **sem cobertura**, com título, URL e uma nota curta. `sustenta` e `contradiz` sem URL oficial são recusados pelo `dossier.py`;
- se contradiz, corrigir o texto e o plano antes de apresentar e contar isso ao gestor na seção "Checagem com boas práticas";
- registrar cada checagem em `knowledge_checks` do spec do dossiê.

Premissas escritas como afirmação ("os conjuntos disputam o leilão entre si") passam por um dicionário controlado de reescrita (`knowledge/retrieval-rewrites.json`) que as traduz para o termo do produto ("sobreposição no leilão"). Se a premissa não achar nada relevante, reescreva com o termo do produto e, se fizer sentido, proponha a regra nova no dicionário com uma consulta rotulada em `tests/fixtures/retrieval_eval.json`.

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

A busca roda em modo híbrido por padrão (`--mode hybrid`): primeiro tenta correspondência de título; só quando o título ficar abaixo de `strong` ela também considera um sinal semântico local (índice vetorial em `knowledge/.vector-index/`, gerado por `scripts/build_knowledge_vector_index.py`). Cada resultado vem marcado com `signal`: `lexical` (título/corpo), `vector` (só pelo sentido), `hybrid` (os dois) ou `rewrite` (achado pelo termo do dicionário de reescrita). Artigos de política só sobem quando a consulta é sobre política. Se o índice vetorial não estiver construído, o buscador cai para o modo lexical sem quebrar; `--mode lexical` força esse comportamento e `--no-rewrite` desliga o dicionário.

Interprete a classificação:

- `exact`: título normalizado idêntico à consulta.
- `strong`: o título bate com a consulta ou com o termo do dicionário; leitura integral obrigatória. O sinal semântico e o conteúdo sozinhos nunca dão `strong`.
- `related`: candidato temático; valide o título e leia até três resultados.
- `weak`: não sustenta resposta sozinho; refine ou consulte o índice.

A qualidade da busca é medida por `python3 scripts/eval_retrieval.py --compare` (consultas rotuladas em `tests/fixtures/retrieval_eval.json`); rode antes e depois de mexer em pesos, no dicionário ou na base.

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
- Não chamar sem `--platform meta`. O buscador falha fechado para `google_ads` e para consulta explicitamente conflitante; nesse caso, rotear para a etapa `revisor/google-ads`. O gate de plataforma vale igualmente para o sinal lexical e o vetorial — cada plataforma tem seu próprio índice vetorial, fisicamente separado, então não há como um sinal semântico vazar de uma base para a outra.
- Não afirmar que leu um artigo apenas porque o sinal vetorial encontrou similaridade; abrir e ler o arquivo indicado antes de responder, igual já vale para o sinal lexical.

## Exemplos

**Pergunta:** “Como funciona a meta de ROAS?”  
**Ação:** buscar a pergunta; abrir integralmente `sobre-a-meta-de-roas.md`; responder com a URL oficial e ressalvas de elegibilidade.

**Pergunta:** “Meu pixel está duplicando eventos.”  
**Ação:** buscar por título e tópico; ler os artigos mais aderentes de mensuração/deduplicação; cruzar com a etapa `mensuracao`.

**Pergunta (parafraseada, sem bater título nenhum):** “meu pixel está contando o mesmo evento duas vezes quando uso CAPI e o pixel do site juntos”  
**Ação:** o título não bate com nenhum artigo (`related`/`weak` no sinal lexical); o sinal vetorial complementa e traz “Sobre o Pixel da Meta” e “Sobre a API de Conversões” como candidatos por sentido. Ler os artigos indicados antes de responder, exatamente como faria com um match por título.

**Pergunta:** “Devo reduzir o orçamento desta campanha em 20%?”  
**Ação:** usar a base para funcionamento de orçamento/aprendizado, mas decidir com dados, baseline e metodologia; não converter documentação oficial em regra universal.
