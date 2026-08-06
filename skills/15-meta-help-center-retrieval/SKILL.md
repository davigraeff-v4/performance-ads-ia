---
name: 15-meta-help-center-retrieval
description: Localiza e lê seletivamente artigos oficiais da Central de Ajuda da Meta armazenados em knowledge/meta-help-center. Use antes de responder dúvidas sobre funcionamento, configuração, políticas, faturamento, contas, campanhas, públicos, criativos, mensuração, catálogo, otimização ou solução de problemas do Meta Ads; também use quando o texto do usuário coincidir total ou parcialmente com o título de um artigo.
---

# Recuperação da Central de Ajuda Meta

## Objetivo

Dar ao agente acesso confiável à base local sem carregar os 151 artigos no contexto. Esta skill é transversal: ela complementa as skills operacionais, mas não substitui dados atuais da conta, metodologia nem validação online quando necessária.

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

Interprete a classificação:

- `exact`: título normalizado idêntico à consulta.
- `strong`: correspondência forte; leitura obrigatória do primeiro resultado.
- `related`: candidato temático; valide o título e leia até três resultados.
- `weak`: não sustenta resposta sozinho; refine ou consulte o índice.

## Processo

1. Preservar a pergunta original como consulta inicial.
2. Rodar o buscador, que lê primeiro apenas o `INDEX.md`; somente se o índice produzir correspondências fracas ele varre o conteúdo como sinal de fallback, sem injetá-lo no contexto.
3. Registrar os candidatos retornados.
4. Abrir integralmente somente os artigos necessários.
5. Separar o que a fonte oficial informa do que a metodologia recomenda.
6. Verificar `extraido_em` e a URL original no frontmatter.
7. Quando a consulta fizer parte de uma operação, registrar no dossiê título, caminho local, URL, data de extração e data da consulta.
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
- Não chamar sem `--platform meta`. O buscador falha fechado para `google_ads` e para consulta explicitamente conflitante; nesse caso, rotear para a skill `17`.

## Exemplos

**Pergunta:** “Como funciona a meta de ROAS?”  
**Ação:** buscar a pergunta; abrir integralmente `sobre-a-meta-de-roas.md`; responder com a URL oficial e ressalvas de elegibilidade.

**Pergunta:** “Meu pixel está duplicando eventos.”  
**Ação:** buscar por título e tópico; ler os artigos mais aderentes de mensuração/deduplicação; cruzar com a skill `03-measurement-data-quality`.

**Pergunta:** “Devo reduzir o orçamento desta campanha em 20%?”  
**Ação:** usar a base para funcionamento de orçamento/aprendizado, mas decidir com dados, baseline e metodologia; não converter documentação oficial em regra universal.
