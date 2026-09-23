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
