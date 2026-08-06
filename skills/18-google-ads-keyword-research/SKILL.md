---
name: 18-google-ads-keyword-research
description: Pesquisa, classifica e prioriza palavras-chave, intenções, termos, negativas e temas para Google Ads. Use em /pesquisar-palavras-chave, campanhas Search, validação de demanda, revisão de termos de pesquisa ou quando o gestor fornecer Keyword Planner, CSV, XLSX ou seeds.
---

# Pesquisa de Palavras-chave Google Ads

## Leituras e entradas

1. `knowledge/official-google/keywords-and-search-terms.md`.
2. `knowledge/google-ads/keyword-research-methodology.md`.
3. Objetivo, oferta, geografia, idioma, URLs e restrições do cliente.
4. Keyword Planner/API, termos da conta ou arquivos fornecidos.

## Modos

- `planner_connected`: `google_ads_extended` homologado, Planner habilitado, customer allowlisted e chamada oficial bem-sucedida.
- `file_based`: export do Keyword Planner ou planilha.
- `account_terms`: termos e keywords atuais via MCP/export.
- `context_only`: seeds e hipóteses sem volume oficial.

Nunca apresentar estimativa do modelo como volume do Keyword Planner.

Antes de usar o conector complementar, chamar `get_extended_capabilities`. Se `planner_enabled` for falso ou o customer estiver fora da allowlist, não chamar `generate_keyword_ideas`; usar `file_based`, `account_terms` ou `context_only`.

## Processo

1. Confirmar produto, mercado, localização, idioma, rede e período.
2. Gerar seeds por oferta, problema, solução, categoria, marca e linguagem do cliente.
3. Normalizar sem apagar variações semanticamente relevantes.
4. Classificar intenção: navegacional, informacional, comercial ou transacional.
5. Separar marca, não marca e concorrentes.
6. Agrupar por tema e landing page, evitando grupos semanticamente misturados.
7. Avaliar volume, sazonalidade, concorrência, faixas de lance e forecast somente quando fornecidos pela fonte.
8. Propor match type como hipótese condicionada a conversões, Smart Bidding, budget e controle de termos.
9. Propor negativas por irrelevância, intenção incompatível, localização ou oferta indisponível.

## Saída

Tabela com `keyword`, `tema`, `intencao`, `marca`, `fonte`, `volume`, `concorrencia`, `faixa_lance`, `match_type`, `grupo`, `landing_page`, `negativas_relacionadas`, `prioridade` e `limitacao`.

Separar palavra-chave planejada de termo de pesquisa observado. Volume, CPC e forecast não garantem tráfego qualificado ou conversão.
