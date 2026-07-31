---
title: "Como solucionar problemas de taxa de correspondência do catálogo"
url: "https://www.facebook.com/business/help/644889989181423"
categoria: "06-catalogo-commerce"
fonte: "Central de Ajuda da Meta para Empresas"
idioma: "pt-BR"
extraido_em: "2026-07-31"
---

# Como solucionar problemas de taxa de correspondência do catálogo

A taxa de correspondência do catálogo mostra a porcentagem de identificações de conteúdo recebidas pela Meta dos eventos do seu site ou app que podem ser combinadas com produtos no seu catálogo. Recomenda-se mantê-la em 90% ou mais. Você pode visualizar sua taxa de correspondência no Gerenciador de Comércio, verificar se há problemas e baixar um relatório de problemas.

Experimente estas etapas se a taxa de correspondência do seu catálogo for baixa, zero ou se você tiver problemas para visualizá-la.

Observação: a taxa de correspondência é exibida para os últimos 28 dias, com um atraso de 48 horas. Isso significa que pode levar até 48 horas para refletir as alterações ou correções que você fizer.

## Se você encontrar problemas sobre identificações de conteúdo ausentes, inválidas ou excluídas

- **Verifique as identificações de conteúdo nos parâmetros de evento**: confira se `content_ids` ou `contents` estão corretos nos eventos do pixel ou do app e correspondem exatamente às identificações (ou identificações de grupo) do seu catálogo. Se uma página exibir vários produtos (por exemplo, uma página de finalização da compra), verifique se ela está configurada para enviar vários IDs.
- **Verifique se as identificações de conteúdo estão no seu catálogo**: confira se as identificações de conteúdo enviadas nos seus eventos de pixel ou do app realmente existem no seu catálogo. Produtos com essas identificações podem ter sido excluídos do seu catálogo, nunca adicionados ou adicionados com uma identificação diferente. Pesquise seu catálogo e adicione os produtos que estão faltando para que sejam correspondidos.
- **Verifique a ortografia de `content_ids`**: o nome do parâmetro deve estar escrito como `content_ids`, com um "s", e não `content_id`, mesmo quando você estiver enviando apenas uma identificação.
- **Verifique a formatação da identificação do conteúdo**: verifique se as identificações do conteúdo nos parâmetros do evento estão formatadas corretamente, sem números ou símbolos extras. Para um produto, formate como `'12345'`. Para vários produtos em uma página, formate-os como `['12345','67890']`. Observação: esses exemplos usam aspas simples (') para incluir o ID do conteúdo, mas aspas duplas (") também são aceitas. Exemplos comuns de erro de formatação:
  - `['12345,67890']`: interpretado como um único produto com a identificação de conteúdo `12345,67890`.
  - `'[\'12345\']'`: interpretado como um produto com a identificação de conteúdo `['12345']`.
  - `'[\'12345\', \'67890\']'`: interpretado como um único produto com a identificação de conteúdo `['12345', '67890']`.
  - `'[12345,67890]'`: interpretado como um único produto com a identificação de conteúdo `[12345,67890]`.
  - `['[12345,67890]']`: interpretado como um único produto com a identificação de conteúdo `[12345,67890]`.

## Se os eventos tiverem baixo volume ou não estiverem sendo rastreados

- **Verifique a configuração do pixel**: confirme se o pixel está instalado corretamente e inclui os eventos e parâmetros necessários para produtos e serviços, hotéis, voos, destinos, automóveis ou imóveis. Use o Auxiliar de Pixel da Meta para verificar se o pixel está sendo acionado corretamente em eventos do site, como ViewContent, AddToCart e Purchase.
- **Verifique a configuração do SDK do app**: confirme se o SDK do app está configurado e enviando os eventos do app necessários. Use a ferramenta de eventos de teste no Gerenciador de Eventos para confirmar se a Meta está recebendo eventos relevantes do seu app.
- **Entenda as contagens de eventos**: é normal que o número total de eventos no Gerenciador de Eventos seja maior do que no Gerenciador de Comércio. O Gerenciador de Eventos mostra todos os eventos recebidos pela Meta, enquanto o Gerenciador de Comércio mostra apenas eventos que podem ser associados a produtos no catálogo que você está visualizando.
- **Verifique se o seu site ou app tem atividade suficiente**: se o tráfego for muito baixo no seu site ou app, a Meta pode não receber eventos suficientes para calcular uma taxa de correspondência estável. Use a ferramenta de eventos de teste no Gerenciador de Eventos para confirmar se a Meta está recebendo eventos relevantes do seu conjunto de dados, aguarde mais tráfego e verifique novamente mais tarde.

## Se você encontrar problemas sobre tipo de conteúdo inválido

O parâmetro de evento `content_type` não é obrigatório. Porém, se o seu pixel incluí-lo, verifique se o `content_type` corresponde ao que você está enviando:

- `product` se o seu pixel estiver enviando identificações individuais.
- `product_group` se o pixel estiver enviando identificações de grupo (`item_group_id` no catálogo).
- Outros valores compatíveis são `hotel`, `destination`, `flight`, `vehicle`, `vehicle_offer` ou `home_listing`.

## Se a taxa de correspondência do catálogo for pausada

A taxa de correspondência poderá ser pausada se você não usar um catálogo para anunciar em 28 dias. Se isso acontecer, você verá uma notificação na aba Eventos do Gerenciador de Comércio. Para retomar a taxa de correspondência, clique em **Retomar** na notificação ou comece a veicular anúncios novamente a partir do catálogo.

## Se você não conseguir ver seu pixel ou app em Catálogo > Eventos

- **Verifique a conexão do pixel ou do app**: confira se o pixel ou o SDK do app está realmente conectado ao seu catálogo.
- **Verifique suas permissões**: você precisa ter ao menos acesso parcial ao catálogo e ao pixel ou SDK para visualizar a taxa de correspondência.
