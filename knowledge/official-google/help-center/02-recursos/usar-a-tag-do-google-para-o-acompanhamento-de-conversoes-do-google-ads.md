---
title: "Usar a tag do Google para o acompanhamento de conversões do Google Ads"
url: "https://support.google.com/google-ads/answer/7548399?hl=pt-BR"
answer_id: "7548399"
categoria: "02-recursos"
topico: "Medir resultados"
subtopico: "Tags de conversão"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Usar a tag do Google para o acompanhamento de conversões do Google Ads

## Contexto: unificação de tags

A tag global do site (gtag.js) passou a ser chamada de **tag do Google**. Instalações novas e antigas de gtag.js ganham novos recursos, melhor qualidade de dados e novas funcionalidades sem necessidade de código extra.

A tag do Google funciona sempre em conjunto com outro código: um **snippet de evento** ou um **snippet de telefone**. Ao criar uma ação de conversão no site na experiência atual do Google Ads, a tag do Google substitui a antiga tag de acompanhamento de conversões. Precisa ser instalada em **todas as páginas do site**.

Quem usa o Gerenciador de Tags do Google (GTM) deve verificar se a tag do Google está configurada no contêiner do GTM e vinculada à conta correta do Google Ads. Após implementar ou corrigir tags, o status da conversão pode levar até **48 horas** para atualizar no Google Ads.

**Dica**: tags de acompanhamento de conversões anteriores continuam funcionando, mas o uso da tag do Google é recomendado para maior precisão.

## Benefícios

- **Integração mais rápida com outros produtos do Google**: a mesma tag é usada por Google Ads, Google Analytics e outros produtos, unificando a implementação no site.
- **Acompanhamento de conversões mais preciso**: permite definir novos cookies no domínio para armazenar um identificador exclusivo do usuário/clique que trouxe o cliente ao site, permitindo especificar quais interações contam como conversão do Google Ads.
- **Cobertura completa de conversões**: ao contrário da tag antiga modificada para implementação "apenas um pixel" (que não acompanha todas as conversões), a tag do Google garante contabilização completa.

Quando um usuário chega ao site após clicar no anúncio, a tag do Google lê as informações do clique e as envia ao Google Ads; em páginas subsequentes, as tags reutilizam esses dados via os cookies definidos no domínio.

## Como funciona

### A Tag do Google
O snippet deve ser inserido em todas as páginas do site, normalmente na seção `<head>` do HTML.

```html
<!-- Google tag (gtag.js) - Google Ads: TAG_ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id=TAG_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config','TAG_ID');
</script>
```

Se a tag do Google já foi instalada por outra ação de conversão da mesma conta (ou por uma conta de administrador), não adicionar o snippet novamente. Se a tag já foi adicionada via outro produto (ex.: Analytics) ou outra conta do Google Ads, é preciso **adaptá-la** (ver seção abaixo).

### Snippet de evento (para conversões no site)
Deve ser instalado na própria página de conversão, após o snippet da Tag do Google (idealmente no `<head>` para maior precisão). É necessário verificar se o ID de conversão e o rótulo estão corretos, e — para conversões baseadas em URL — se o URL exato bate com o configurado no Google Ads.

```html
<!-- Event snippet for example conversion page -->
<script>
gtag('event', 'conversion', {
  'send_to': 'AW-CONVERSION_ID/CONVERSION_LABEL',
  'value': 0.0,
  'currency': 'USD',
  'transaction_id': ''
  // 'new_customer': true, /* opcional — melhora a precisão do relatório de aquisição de novos clientes */
});
</script>
```

### Snippet de telefone (para conversões de chamada)
Deve ser adicionado às páginas que exibem o número de telefone a acompanhar, posicionado **antes** do comando `config` da tag do Google. Substitui o número corporativo por um número de encaminhamento de chamadas do Google.

```html
<script>
gtag('set', {
  'phone_conversion_number': '1-650-555-5555',
  'phone_conversion_ids': ['AW-CONVERSION_ID/CONVERSION_LABEL']
});
gtag('config', 'AW_CONVERSION_ID');
</script>
```

## Como adaptar uma tag do Google já instalada para a conta do Google Ads

Se a tag do Google já está em todas as páginas (por exemplo, vinda de uma conta do Analytics), é possível configurá-la para enviar dados a múltiplas contas adicionando um novo comando `config` com o ID da conta do Google Ads:

```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'TAG_ID_ANALYTICS');
  gtag('config', 'TAG_ID_GOOGLE_ADS');
</script>
```

Para desativar o uso dos dados na personalização de publicidade, adicionar o comando:

```javascript
gtag('set', 'allow_ad_personalization_signals', false);
```

Após adaptar a tag dessa forma, não é preciso adicionar novamente o snippet da tag do Google do Google Ads — basta incluir o snippet de evento ou de telefone. Para cada conta adicional (Google Ads ou Analytics), adicionar um novo comando `config` com o respectivo ID.

**Observação**: é possível usar um único snippet global (gtag.js) para atender várias contas de Google Ads ou Google Analytics simultaneamente.

## Diagnóstico e segurança/privacidade

- Usar o Assistente de tags para verificar a implementação e depurar problemas.
- Se houver múltiplos métodos simultâneos (gtag.js + GTM), verificar conflitos e considerar consolidar em um único método (de preferência GTM).
- Status da tag pode levar até 48 horas para atualizar após correções.
- O Google Ads só coleta dados em sites/apps com acompanhamento configurado; é necessário fornecer informações claras sobre coleta de dados e obter consentimento quando exigido por lei ou pelas políticas do Google, incluindo a Política de consentimento de usuários da União Europeia.

## Links relacionados

- [Sobre a tag do Google](https://support.google.com/google-ads/answer/11994839)
- [Adicionar uma tag do Google ao seu site](https://support.google.com/google-ads/answer/6331314)
- [Sobre implementação "apenas um pixel"](https://support.google.com/tagassistant/answer/2947038#pixel_only)
