# Base de Conhecimento — PERFORMANCE ADS IA

Use este índice no início de toda auditoria, análise, criação ou otimização. Leia apenas os arquivos relevantes, mas cumpra as leituras obrigatórias da skill.

## Precedência

1. Fonte oficial atual da plataforma para funcionamento, produto e política.
2. Dados confirmados do cliente para resultado comercial.
3. Metodologia interna para tomada de decisão.
4. Aprendizados sanitizados aprovados.

## Oficial Meta

### Central de Ajuda completa — recuperação seletiva

- `meta-help-center/INDEX.md` — índice de 151 artigos em 12 categorias.
- `meta-help-center/{categoria}/{artigo}.md` — snapshot integral com título, URL e data de extração.
- `skills/15-meta-help-center-retrieval/SKILL.md` — regra if/else e gates de leitura.
- `scripts/search_meta_help.py` — busca por título e tópico sem carregar a base inteira.

Para qualquer dúvida sobre funcionamento do Meta Ads, rode primeiro:

```bash
python3 scripts/search_meta_help.py "pergunta original" --platform meta --limit 3
```

Correspondência exata ou forte de título exige leitura integral do primeiro artigo. Correspondência temática permite abrir até três candidatos. Resultado fraco exige refinar pelo índice; não autoriza responder como se a fonte tivesse sido consultada.

Este snapshot foi extraído em 2026-07-31. Em políticas, cobrança, segurança, elegibilidade, restrições ou decisões sensíveis, valide a URL oficial ao vivo.

### Resumos operacionais

- `official-meta/objectives-and-delivery.md` — objetivos e entrega.
- `official-meta/account-structure-and-learning.md` — simplificação e aprendizado.
- `official-meta/budgets-bidding-advantage.md` — budget, lances e Advantage+.
- `official-meta/audiences-and-placements.md` — controles, sugestões e posicionamentos.
- `official-meta/creative-and-review.md` — diversificação, formato e revisão.
- `official-meta/measurement-and-capi.md` — Pixel, CAPI e qualidade de dados.
- `official-meta/source-catalog.md` — rotas oficiais para consulta ao vivo e temas não congelados.

Cada arquivo inclui `verificado_em`. Verifique a fonte ao vivo se a decisão for sensível, houver indício de mudança ou o arquivo estiver marcado para revisão. Registre a URL consultada no dossiê.

## Oficial Google Ads

O Google Ads usa uma base seletiva em expansão, sem alegar snapshot integral:

- `official-google/help-center/INDEX.md` — índice local da Central de Ajuda.
- `official-google/help-center/{categoria}/{artigo}.md` — sínteses estruturadas com URL e data de extração.
- `scripts/build_google_ads_help_index.py --write` — regenera o índice a partir dos frontmatters.
- `scripts/search_google_ads_help.py` — recuperação seletiva com gate de plataforma.
- `official-google/source-catalog.md` — rotas oficiais ainda dependentes de leitura ao vivo.
- `official-google/google-ads-mcp-and-api.md` — API e MCP.
- Os demais resumos em `official-google/` são legados em revisão durante a expansão da base.
- `skills/17-google-ads-official-retrieval/SKILL.md` — gate seletivo Google Ads.

Para dúvidas de interface/produto, execute primeiro:

```bash
python3 scripts/search_google_ads_help.py "pergunta original" --platform google_ads --limit 3
```

Para comportamento atual, elegibilidade, política, cobrança, campos da API ou decisão material, abrir também a fonte oficial ao vivo. Não atribuir metodologia interna ao Google.

## Metodologia

- `methodology/diagnostic-framework.md`
- `methodology/kpis-baseline-breakeven.md`
- `methodology/windows-and-comparisons.md`
- `methodology/testing-and-prioritization.md`
- `methodology/budget-and-scaling.md`
- `methodology/naming-and-architecture.md`
- `google-ads/keyword-research-methodology.md`
- `google-ads/account-architecture.md`
- `google-ads/diagnostic-framework.md`

Metodologia é regra operacional interna, não recomendação oficial da Meta.

## Trilhas

- `lead-generation/decision-tree.md`
- `ecommerce/decision-tree.md`
- `measurement/measurement-quality.md`
- `creative-performance/creative-diagnosis.md`

## Aprendizados

`sanitized-learnings/` recebe somente propostas anônimas aprovadas por Davi. Um caso isolado deve permanecer rotulado como evidência limitada.

## Regra de citação

No dossiê, registre título, URL e data de consulta. Parafraseie; não copie páginas extensas. Diferencie claramente `Meta informa`, `Google informa` e `metodologia recomenda`.
