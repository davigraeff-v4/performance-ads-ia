---
title: "Conhecer melhor os URLs finais e modelos de acompanhamento"
url: "https://support.google.com/google-ads/answer/6273460?hl=pt-BR"
answer_id: "6273460"
categoria: "02-recursos"
topico: "Anúncios, recursos e páginas de destino"
subtopico: "URLs finais"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Conhecer melhor os URLs finais e modelos de acompanhamento

## URL final

O URL final é a página do site para onde a pessoa é levada ao clicar no anúncio. Não precisa ser idêntico ao URL de visualização, mas o domínio (ex.: "example.com" em "www.example.com") precisa ser o mesmo em ambos.

Com os URLs atualizados (que usam modelos de acompanhamento), o URL da página de destino fica separado da parte que contém informações de acompanhamento — ou seja, não é preciso inserir dados de rastreamento dentro do URL final.

## Modelo de acompanhamento

É o campo onde se inserem as informações de rastreamento de URL, por exemplo para acompanhar cliques de uma campanha ou grupo de anúncios específico. Os modelos de acompanhamento usam parâmetros de URL para personalizar o URL de rastreamento ou o URL final.

### Redirecionamentos entre domínios e parâmetros

- Se o URL incluir redirecionamento entre domínios, a pessoa passa por um site com domínio diferente antes ou depois de chegar à página de destino.
- É possível usar parâmetros como `source=google` e `ad={creative}` para registrar detalhes do anúncio no momento do clique.
- Nos URLs atualizados, essas informações de rastreamento migram do URL de destino para o campo "Modelo de acompanhamento".
- Recomenda-se usar a macro `{unescapedlpurl}` nos modelos de acompanhamento, para manter os URLs finais consistentes e precisos mesmo que a página de destino mude.

### Exemplo prático

Página de destino: `http://www.examplebusiness.com/comprar`

Para acompanhar o tráfego vindo da campanha A, o modelo de acompanhamento seria escrito como:

```
{lpurl}?source_campaign={_campaignA}
```

## Qual URL o cliente vê

| Situação | Comportamento |
|---|---|
| Modelo de acompanhamento presente + acompanhamento paralelo ativado | A pessoa é direcionada ao URL final imediatamente, enquanto o URL do modelo de acompanhamento carrega em segundo plano. |
| Modelo de acompanhamento presente + acompanhamento paralelo desativado | A pessoa é direcionada ao URL do modelo, que pode passar por servidores de acompanhamento intermediários antes de chegar ao URL final. |
| Modelo de acompanhamento ausente | A pessoa é direcionada diretamente ao URL final. |

## Requisitos técnicos

- O URL do modelo de acompanhamento e todos os URLs de redirecionamento precisam ser HTTPS para funcionar.
- Os redirecionamentos precisam ser do lado do servidor.
- O Google Ads sempre usa HTTPS para a primeira chamada de acompanhamento, mesmo que ela não tenha sido inserida como tal (o Google não controla redirecionamentos subsequentes).
- Acompanhamento paralelo é **obrigatório** para campanhas de Pesquisa, Shopping, Display, Vídeo e Performance Max.
- Em campanhas de Hotel, o acompanhamento paralelo é **opcional**.
- Algumas contas ainda podem exibir o botão de acompanhamento paralelo nas configurações, mas essa opção só se aplica a campanhas de Hotel.

## Alerta de versão do Google Ads Editor

Use o Google Ads Editor versão 12.4 ou superior. Versões mais antigas podem excluir alterações anteriores de acompanhamento paralelo e de URL.

## Links relacionados

- [URL final](https://support.google.com/google-ads/answer/6080568)
- [URL de visualização](https://support.google.com/google-ads/answer/2616010)
