# Naming e Arquitetura

> Metodologia interna.

## Convenção base

- Campanha: `{objetivo}_{mercado}_{oferta}_{funil}_{data}`
- Conjunto: `{publico}_{geo}_{evento}_{posicionamento}`
- Anúncio: `{formato}_{angulo}_{variacao}_{data}`

Adaptar ao padrão validado do cliente. Usar slugs/abreviações documentadas, sem dados pessoais.

## Arquitetura

Separar quando houver diferença real de objetivo, conversão, oferta, geografia, budget, controle, restrição ou hipótese. Consolidar redundância quando não houver justificativa e quando a transição for segura.

## Checklist de lançamento

- Conta, moeda e timezone confirmados.
- Objetivo/local/evento coerentes.
- Budget e datas aprovados.
- Públicos e exclusões validados.
- Identidade, URL, UTM e tracking conferidos.
- Criativos cobrem formatos/placements.
- Status inicial e plano de monitoramento definidos.
