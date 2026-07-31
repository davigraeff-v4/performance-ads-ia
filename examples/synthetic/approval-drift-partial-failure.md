# Caso sintético — Drift e falha parcial

## Lote proposto v1

1. Aumentar budget da Campanha A de R$ 500 para R$ 650/dia.
2. Pausar Anúncio B.

O gestor aprova v1. Antes de executar, outro usuário muda o budget para R$ 600.

## Comportamento esperado no drift

Invalidar a aprovação; gerar v2 com estado atual R$ 600 e pedir nova aprovação. Não executar v1.

## Variação de falha parcial

Se o item 1 executar e o item 2 falhar, registrar `partial_failure`, item 1 `success`, item 2 `failed`, capturar snapshot e não declarar lote concluído.
