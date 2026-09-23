# Conector Meta Ads (`facebook-ads`)

## Edição força pausa

`ads_update_entity` devolve `status_forced_to_paused: true` e **pausa de verdade** o conjunto ou anúncio editado, mesmo quando a mudança é só de orçamento ou segmentação.

- Depois de qualquer `ads_update_entity` numa entidade que deve continuar ativa, chame `ads_activate_entity` na mesma entidade e confira `effective_status` antes de dar o item por concluído.
- Logo após a edição, `effective_status: IN_PROCESS` é reprocessamento normal, não falha; `status` volta a `ACTIVE`.

## Segmentação

- Ao mudar um subcampo de `targeting`, envie a especificação **completa** (interesses, públicos personalizados, `age_range`). Campos omitidos voltam ao padrão; por exemplo, `age_range` retorna silenciosamente para 18-65.
- Para desligar o Advantage+ Audience (`targeting_automation.advantage_audience: 0`), **não** inclua a chave legada `targeting_optimization`: a API rejeita a chamada inteira (VALIDATION, subcódigo 1870197).
- O conector não tem busca de localizações. As chaves de estados brasileiros em `geo_locations.regions[].key`, confirmadas por escrita e leitura, estão na tabela abaixo. Fontes públicas erram (por exemplo, dão 458 para o Rio de Janeiro, que é Roraima). Confira sempre por leitura: a resposta traz o `name` de cada chave.

| Estado | Chave | Estado | Chave |
|---|---|---|---|
| Amapá | 440 | Rondônia | 457 |
| Amazonas | 441 | Roraima | 458 |
| Bahia | 442 | Santa Catarina | 459 |
| Ceará | 443 | São Paulo | 460 |
| Distrito Federal | 444 | Sergipe | 461 |
| Espírito Santo | 445 | Goiás | 462 |
| Mato Grosso do Sul | 446 | Minas Gerais | 449 |
| Maranhão | 447 | Pará | 450 |
| Mato Grosso | 448 | Paraíba | 451 |
| Paraná | 452 | Piauí | 453 |
| Rio de Janeiro | 454 | Rio Grande do Norte | 455 |
| Rio Grande do Sul | 456 | | |

Ainda não confirmados: Acre, Alagoas, Pernambuco, Tocantins.

## Criação

- **Conjuntos de formulário nativo não podem ser criados pelo conector.** `ads_create_ad_set` com `optimization_goal=LEAD_GENERATION` falha com erro 100, subcódigo 1815089 (`is_retryable=false`). A conexão não tem `pages_manage_ads` para ler o aceite dos Termos de Cadastro da Página. Planeje esse item como `manual_only` desde o início: duplicar um conjunto de formulário existente no Gerenciador e trocar geografia e orçamento. As campanhas "casca" (`OUTCOME_LEADS`) podem ser criadas pelo conector e nascem pausadas.
- Se um lote realoca verba para conjuntos de formulário que ainda não existem, **não corte o orçamento de origem** antes de o destino existir: marque esses cortes como `not_attempted`.
- **Anúncio de vídeo com WhatsApp:** precisa de miniatura (`image_url` ou `image_hash`; o campo `picture` de `ads_get_ad_videos` funciona, mas tem 160 px), e `call_to_action` deve ser `{type: WHATSAPP_MESSAGE}` **sem** `value.link` (erros 100/1443226 e 105/1815630). Em anúncio de imagem é o contrário: `link_data.link` é obrigatório (use a URL da Página).
- **Limite de 50 anúncios por conjunto, pausados incluídos** (erro 100/1487809). Ao planejar lotes de criativos em conjuntos existentes, conte os anúncios atuais, inclusive os pausados, ainda no planejamento.
- Ao espelhar um conjunto existente, a Meta pode acrescentar `frequently_in` em `location_types` e posicionamentos automáticos novos podem perder Messenger Stories. Leia o conjunto criado e registre as diferenças.

## Leitura

- `ads_get_ad_entities` sem filtro é **paginado** (`pagination.next_cursor`). Uma entidade que não aparece na primeira página não está necessariamente pausada. Para afirmar status, leia por `object_ids` com `status`/`effective_status` ou esgote a paginação. Nunca registre status por ausência.

## Base oficial ao vivo

`ads_get_help_article` busca artigos da Central de Ajuda da Meta e costuma achar o artigo certo para premissas de mecanismo (por exemplo, sobreposição de leilão) que a base local não cobre. Use na checagem de boas práticas.

- **Idioma da consulta:** em 2026-09-23, a consulta em português ("sobreposição de leilão conjuntos de anúncios") trouxe artigos sem relação (impostos no Brasil, LGPD); a mesma ideia em inglês ("auction overlap ad sets overlapping audiences") trouxe os 3 artigos certos. Consulte com o nome do produto em inglês.
- **Formato da resposta:** um resumo do artigo em inglês, em minúsculas, com a URL. Serve para confirmar a regra e citar a URL oficial; não serve como cópia fiel para a base local.
- **Cópia em português:** a página `https://www.facebook.com/business/help/{id}?locale=pt_BR` monta o texto por JavaScript; leitura simples por HTTP devolve só o título. Para acrescentar um artigo à base, é preciso um navegador. Páginas de glossário de métrica (ex.: 957407462768373, "campaign auction overlap") devolveram erro na Central com e sem `locale`.

## Referências oficiais (benchmarks, ranking, oportunidade, anomalias, tendência)

Observado numa conta real de conversas no WhatsApp em 2026-09-23 (todas só de leitura):

- `ads_insights_industry_benchmark` pode devolver apenas "No industry benchmark data available for the given criteria." Isso é resultado, não erro: registre "sem referência do setor" e não estime. Na leitura, "acima da referência" significa sempre **melhor** posição, inclusive em métricas de custo (custo menor que os pares).
- `ads_insights_auction_ranking_benchmarks` agrupa os anúncios por objetivo de otimização, evento otimizado e tipo de público (remarketing ou prospecção). Anúncios novos ou com pouca entrega vêm com os três rankings "Not Yet Available": não conclua nada sobre qualidade nesse caso.
- `ads_get_opportunity_score` devolve a nota (0 a 100) **da conta** e recomendações em português, cada uma com `opportunity_score_lift` (pontos) e `lift_estimate`. Recomendações como "aumente o orçamento" (`budget_limited`) são da plataforma, não decisão do gestor; nunca ative recomendação automática.
- `ads_insights_anomaly_signal` não aceita período; avalia a entrega atual. Exemplo de alerta: `active_delivery_narrow_audience`, com a faixa estimada do público de cada conjunto.
- `ads_insights_performance_trend` não aceita período (usa todo o histórico disponível), só `analysis_level` ADSET ou AD. Devolve a variação em % **sem sinal** e o rótulo GOOD/BAD; a direção vem do rótulo. A métrica principal padrão é a taxa de cliques; `CPCL` aparece entre as métricas secundárias. Use `hide_ui: true` quando for só apoio ao diagnóstico. Não use o % como comparação do período analisado.
