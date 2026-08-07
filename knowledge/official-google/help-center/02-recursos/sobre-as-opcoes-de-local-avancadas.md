---
title: "Sobre as opções de local avançadas"
url: "https://support.google.com/google-ads/answer/1722038?hl=pt-BR"
answer_id: "1722038"
categoria: "02-recursos"
topico: "Segmentação"
subtopico: "Locais"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Sobre as opções de local avançadas

Permitem incluir ou excluir pessoas com base em onde elas provavelmente estão/costumam estar e/ou nos lugares em que demonstraram interesse. Por padrão, a segmentação inclui localizações físicas e locais de interesse; anunciantes avançados podem restringir a um subconjunto. Aplicam-se a anúncios de Pesquisa, Display e Geração de Demanda (nesta última, o padrão recomendado também é presença + interesse).

## Segmentação por área geográfica ampla

Com **"Presença ou interesse"**, alcança-se quem está nas regiões segmentadas e quem demonstrou interesse nelas — mais regiões possíveis (países, cidades/territórios, raio) e mais conversões/cliques/impressões de interessados.

**Dado de referência do Google**: anunciantes de viagens, imóveis e educação que migraram de "Presença" para "Presença ou interesse" tiveram aumento de **5% nas conversões** em campanhas de pesquisa (dados internos globais do Google, 21/mai–1/jun de 2022).

É prática recomendada em campanhas de pesquisa e Geração de Demanda — mas "Presença" faz sentido quando: a empresa é de categoria sensível com limitações rígidas de segmentação, ou quando só interessa alcançar quem está fisicamente no local (não interessados de fora).

## Comparação das opções

- **Presença ou interesse** (padrão/recomendado): alcança quem frequenta, está ou demonstrou interesse (agora ou no passado) na região segmentada. A maioria das campanhas perde impressões ao sair desse padrão — mudar só para refinar tráfego deliberadamente.
- **Presença**: alcança apenas quem está ou costuma frequentar a região segmentada. **Campanhas de hotel só usam "Presença".**
- **Exclusão de local (Presença)**: por padrão, remove quem provavelmente está nas áreas excluídas; usuários fora dessas áreas continuam vendo os anúncios.

## Migração de segmentação por renda familiar

A segmentação por local baseada em renda familiar está sendo migrada automaticamente para ser tratada como segmentação demográfica. Ajustes: Campanhas → Públicos-alvo → Informações demográficas → aba "Renda familiar" → Editar informações demográficas → selecionar campanha/grupo de anúncios → marcar/desmarcar → Salvar.

## Perguntas frequentes (resumo)

- **A migração para segmentação ampla tem benefício?** Sim — ver o dado de 5% de aumento em conversões citado acima.
- **É possível recusar a migração para "Presença ou interesse"/exclusão "Presença"?** Não — mudança já ocorreu no Google Ads, na API e no Google Ads Editor; os campos `positive_geo_target_type` (Pesquisa/Display/Shopping) e `negative_geo_target_type` (Pesquisa/Display/PMax/Shopping) não aceitam mais os valores antigos, gerando `SettingError.SETTING_VALUE_NOT_COMPATIBLE_WITH_CAMPAIGN` se tentado via API.
- **Afeta todas as campanhas?** Não — só campanhas de pesquisa e tipos relacionados notam mudança na segmentação/exclusão por local.

## Links relacionados

- [Segmentar anúncios por localizações geográficas](https://support.google.com/google-ads/answer/1722043?hl=pt-BR)
- [Excluir anúncios de localizações geográficas](https://support.google.com/google-ads/answer/1722040?hl=pt-BR)
- [Refinar sua segmentação por local](https://support.google.com/google-ads/answer/2404184?hl=pt-BR)
- [Visão geral dos públicos-alvo da Geração de Demanda](https://support.google.com/google-ads/answer/15594567?hl=pt-BR)
- [Escolher o tipo certo de campanha](https://support.google.com/google-ads/answer/2567043?hl=pt-BR)
