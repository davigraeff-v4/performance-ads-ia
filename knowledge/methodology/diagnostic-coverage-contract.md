# Contrato de Cobertura Diagnóstica

> Metodologia interna. Define quando uma análise pode ser chamada de completa.

## Modos

- `full`: padrão para `auditoria`, `analise` e `otimizacao`. Verifica todas as camadas aplicáveis à plataforma e ao tipo de campanha.
- `focused`: permitido somente quando o gestor restringir explicitamente a pergunta a um objeto, dimensão ou hipótese. Registrar o foco e não chamar a entrega de diagnóstico completo da conta.

Completo não significa listar toda entidade no chat. Significa cobrir 100% do agregado da conta ou escopo e aprofundar as entidades materiais, cobrindo preferencialmente pelo menos 90% do investimento e 90% das conversões, além de todo outlier com gasto material, conversão anômala ou risco de mensuração. Quando isso não for possível, declarar a cobertura obtida e a limitação.

## Estados de cobertura

Cada camada aplicável deve aparecer na matriz de cobertura com um dos estados:

- `analyzed`: fonte lida e evidência suficiente para a conclusão declarada.
- `unavailable`: fonte ou campo não acessível; informar motivo e como obter.
- `insufficient`: dado acessível, mas amostra, definição ou qualidade não sustenta decisão.
- `not_applicable`: camada não existe para o tipo de campanha ou escopo; justificar.

Não existe estado implícito. Uma camada ausente é `not_checked` e bloqueia a conclusão como diagnóstico completo.

## Camadas Meta Ads

Em modo `full`, registrar: conta, campanha, conjunto de anúncios, anúncio/criativo, placement/dispositivo, público/geografia/demografia, conversão, mensuração, resultado comercial e histórico de mudanças.

## Camadas Google Ads

Em modo `full`, registrar: conta, campanha, grupo de anúncios, anúncio/asset, conversão, dispositivo, geografia, tempo, mensuração, resultado comercial, histórico de mudanças e orçamento/classificação.

Adicionar conforme o tipo:

- Search: keyword, termo de pesquisa e rede.
- Performance Max: asset group, assets, produtos/listing groups quando aplicável e sinais/insights observáveis.
- Display/Video/Demand Gen: placement/inventário, público, criativo/asset e ações de conversão.
- Shopping: produto/listing group, feed, termos/insights disponíveis e margem/receita.

## Pacote de evidências

Antes de formular achados, produzir evidências identificadas. Cada evidência registra:

- fonte e data de extração;
- plataforma e nível;
- janela e comparação;
- métricas com unidade, definição e denominador;
- valor atual, comparativo, variação absoluta e percentual;
- escopo e cobertura;
- indisponibilidade ou ressalva, quando houver.

O chat mostra as tabelas necessárias para o gestor compreender a decisão. Respostas brutas, GAQL e logs ficam resumidos; números decisórios não podem ser escondidos.

## Rastreabilidade

Usar a cadeia:

`evidence_id -> finding_id -> action_id -> change_id`

- Achado sem evidência identificada é inválido.
- Ação sem achado de origem é inválida.
- Change set sem ação, achado e evidência no nível do alvo é inválido.
- Investigação, teste, recomendação e mudança candidata são tipos de ação distintos.

## Entrega e persistência

1. Montar a representação estruturada em memória.
2. Entregar integralmente no chat: veredito, cobertura, KPIs, evidências, diagnóstico, ações, limitações e decisões.
3. Iterar no chat até existir uma versão final candidata.
4. Solicitar aprovação editorial para registrar exatamente essa versão.
5. Somente depois da aprovação criar o dossiê Markdown e gravar o hash do conteúdo aprovado.

Aprovação editorial permite registrar o dossiê. Não aprova nem executa mudança de mídia. Change set persistido ainda exige `/aprovar-operacao <id>` e, quando suportado, `/executar-operacao <id>`.
