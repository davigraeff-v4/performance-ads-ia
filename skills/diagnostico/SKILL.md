---
name: diagnostico
description: Define metas e linha de base e diagnostica a performance Meta Ads ou Google Ads, do nível da conta ao anúncio, separando entrega, resposta, conversão, qualidade e mensuração. Use em análise, otimização, auditoria e avaliação de operação.
---

# Diagnóstico

Módulo de diagnóstico. Cada etapa da rota aponta para uma referência:

| Etapa na rota | Quando | Leia |
|---|---|---|
| `diagnostico/metas-e-linha-de-base` | sempre antes do diagnóstico, em qualquer plataforma | `references/metas-e-linha-de-base.md` |
| `diagnostico/meta` | ramo Meta | `references/meta.md` (inclui as referências oficiais da Meta e o modo avaliação) |
| `diagnostico/google-ads` | ramo Google Ads | `references/google-ads.md` (inclui o modo avaliação) |

Regras comuns:

- A profundidade vem da rota: `full` só em auditoria ou a pedido; `focused` declara o foco; `quick` em avaliação.
- Todo achado diz o que vimos (com números), por que acreditamos, outra explicação possível e a confiança.
- As premissas de mecanismo de cada achado e mudança passam pelo módulo `revisor` (`scripts/kb_check.py`) antes de ir para o chat.
- Não construa diagnóstico sobre desempenho individual de pessoas do cliente; foque no que a mídia controla.
- Nunca misture Meta e Google no mesmo ranking ou na mesma conclusão.
