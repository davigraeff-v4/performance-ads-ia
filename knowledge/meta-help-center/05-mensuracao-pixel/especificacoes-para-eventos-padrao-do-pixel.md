---
title: "Especificações para eventos padrão do Pixel da Meta"
url: "https://www.facebook.com/business/help/402791146561655"
categoria: "05-mensuracao-pixel"
fonte: "Central de Ajuda da Meta para Empresas"
idioma: "pt-BR"
extraido_em: "2026-07-31"
---

# Especificações para eventos padrão do Pixel da Meta

Eventos são ações que as pessoas realizam no site. Os eventos padrão são predefinidos pela Meta para registrar conversões, otimizar campanhas e criar públicos.

## Lista de eventos padrão

| Ação no site | Descrição | Código do evento |
|---|---|---|
| Adicionar informações de pagamento | Adição de informações de pagamento durante o checkout | `fbq('track', 'AddPaymentInfo');` |
| Adicionar ao carrinho | Adição de um item ao carrinho | `fbq('track', 'AddToCart');` |
| Adicionar à lista de desejos | Adição de itens à lista de desejos | `fbq('track', 'AddToWishlist');` |
| Concluir registro | Envio de informações em troca de um serviço (ex.: assinatura de e-mail) | `fbq('track', 'CompleteRegistration');` |
| Entrar em contato | Contato entre cliente e empresa (telefone, SMS, e-mail, chat) | `fbq('track', 'Contact');` |
| Personalizar produto | Personalização de produtos via ferramenta de configuração | `fbq('track', 'CustomizeProduct');` |
| Doar | Doação de fundos para a organização | `fbq('track', 'Donate');` |
| Encontrar localização | Pessoa encontra uma localização com intenção de visitar | `fbq('track', 'FindLocation');` |
| Iniciar finalização da compra | Início do processo de checkout | `fbq('track', 'InitiateCheckout');` |
| Lead | Envio de informações pelo cliente para contato futuro | `fbq('track', 'Lead');` |
| Comprar | Conclusão de uma compra | `fbq('track', 'Purchase', {value: 0.00, currency: 'USD'});` |
| Programar | Marcação de horário para visitar uma localização | `fbq('track', 'Schedule');` |
| Pesquisar | Pesquisa realizada no site, app ou outra propriedade | `fbq('track', 'Search');` |
| Iniciar período de avaliação | Início de avaliação gratuita de produto/serviço | `fbq('track', 'StartTrial', {value: '0.00', currency: 'USD', predicted_ltv: '0.00'});` |
| Enviar inscrição | Envio de solicitação para produto/serviço/programa | `fbq('track', 'SubmitApplication');` |
| Assinar | Início de assinatura paga | `fbq('track', 'Subscribe', {value: '0.00', currency: 'USD', predicted_ltv: '0.00'});` |
| Ver conteúdo | Visita a uma página relevante (sem detalhar a ação na página) | `fbq('track', 'ViewContent');` |

Observação: o evento "Visualização da Página" já vem incluído no código base do pixel — informa quando alguém acessa uma página com o código base instalado.

## Exemplo de estrutura do código

1. Código original do site (o código do Pixel é colado entre as tags `<head>` e `</head>`).
2. Código base do Pixel da Meta (com o ID exclusivo do pixel).
3. Código do evento padrão correspondente à página (ex.: código de "Adicionar ao carrinho"), inserido acima da tag `</script>` — necessário em cada página a ser rastreada.

## Saiba mais

- Sobre o Pixel da Meta
- Como configurar e instalar o Pixel da Meta
- Boas práticas para a configuração de eventos padrão com o Pixel da Meta
