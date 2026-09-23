---
name: planejamento
description: Planeja campanhas Meta Ads e Google Ads — estratégia, arquitetura, públicos ou palavras-chave, orçamento e lances, criativos e o plano de construção aprovável. Use em /planejar-campanha, /criar-campanha e /pesquisar-palavras-chave.
---

# Planejamento

Módulo de planejamento. A rota planeja as etapas na ordem; cada uma aponta para uma referência. Leia só as da plataforma da rota.

## Meta Ads

| Etapa na rota | Leia |
|---|---|
| `planejamento/meta-estrategia` | `references/meta-estrategia.md` |
| `planejamento/meta-arquitetura` | `references/meta-arquitetura.md` |
| `planejamento/meta-publicos` | `references/meta-publicos.md` |
| `planejamento/meta-orcamento-e-lances` | `references/meta-orcamento-e-lances.md` |
| `planejamento/meta-briefing-criativo` | `references/meta-briefing-criativo.md` |
| `planejamento/meta-plano-de-construcao` | `references/meta-plano-de-construcao.md` |

## Google Ads

| Etapa na rota | Leia |
|---|---|
| `planejamento/google-ads-palavras-chave` | `references/google-ads-palavras-chave.md` |
| `planejamento/google-ads-estrategia` | `references/google-ads-estrategia.md` |
| `planejamento/google-ads-arquitetura` | `references/google-ads-arquitetura.md` |
| `planejamento/google-ads-orcamento-lances-e-conversoes` | `references/google-ads-orcamento-lances-e-conversoes.md` |
| `planejamento/google-ads-criativos-e-pagina` | `references/google-ads-criativos-e-pagina.md` |
| `planejamento/google-ads-plano-de-construcao` | `references/google-ads-plano-de-construcao.md` |

Regras comuns:

- Negócio antes da métrica: o objetivo da plataforma serve ao resultado comercial registrado no perfil e nos aprendizados do cliente.
- Toda escolha de mecanismo (objetivo, tipo de campanha, lance, público, correspondência) passa pelo módulo `revisor` antes de ir para o chat.
- Copy e variações de anúncio ficam com a skill `ad-variations-creator`, depois do briefing criativo; anúncios de concorrentes, com `meta-ads-competitor` ou `google-ads-competitor`.
- O plano de construção vira change set pelo módulo `change-set`; Google Ads é sempre `manual_only`.
