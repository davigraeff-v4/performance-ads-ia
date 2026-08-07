---
title: "Atualizar seus scripts para criar anúncios em vídeo"
url: "https://support.google.com/google-ads/answer/11587128?hl=pt-BR"
answer_id: "11587128"
categoria: "02-recursos"
topico: "Recursos"
subtopico: "Configurações da campanha"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Atualizar seus scripts para criar anúncios em vídeo

Desde 28 de fevereiro de 2022, vídeos usados por scripts do Google Ads são representados por recursos, como `AdVideoAsset` e `AdImageAsset`, em vez de arquivos de mídia. Scripts antigos que criam anúncios em vídeo precisam trocar as referências à mídia pelas APIs de recursos correspondentes.

## Procedimento

1. Na conta do Google Ads, abra o menu de ferramentas.
2. Em **Ações em massa**, selecione **Scripts**.
3. Abra o script que precisa ser atualizado.
4. Localize as partes do código que usam mídia de vídeo.
5. Substitua essas referências por recursos de vídeo compatíveis com o modelo atual.
6. Salve o script.

## Referências técnicas

- [Recursos em Google Ads Scripts](https://developers.google.com/google-ads/scripts/docs/reference/adsapp/adsapp_asset)
- [`AdVideoAsset`](https://developers.google.com/google-ads/api/reference/rpc/latest/AdVideoAsset)
- [`AdImageAsset`](https://developers.google.com/google-ads/api/reference/rpc/latest/AdImageAsset)
- [Mídia em Google Ads Scripts](https://developers.google.com/google-ads/scripts/docs/reference/adsapp/adsapp_media)
- [Scripts do Google Ads](https://support.google.com/google-ads/answer/188712?hl=pt-BR)
