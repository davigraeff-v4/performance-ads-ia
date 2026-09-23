---
name: revisor
description: Confere premissas e responde dúvidas com a base oficial da Meta e do Google Ads — Central de Ajuda local, fonte ao vivo e revisor kb_check.py — e registra as checagens de boas práticas. Use em toda rota que o planeja, em dúvidas de funcionamento e na checagem de premissas de diagnóstico, mudanças, relatório e avaliação.
---

# Revisor de boas práticas

Módulo da base oficial. Cada etapa da rota aponta para a referência da plataforma:

| Etapa na rota | Leia |
|---|---|
| `revisor/meta` | `references/meta.md` |
| `revisor/google-ads` | `references/google-ads.md` |

Dois modos, nas duas plataformas:

1. **Dúvida:** o gestor pergunta como algo funciona; a consulta é a pergunta original (`scripts/search_meta_help.py` ou `scripts/search_google_ads_help.py`).
2. **Checagem de premissas:** em diagnóstico, mudanças, relatório e avaliação, rode `python3 scripts/kb_check.py --platform {meta|google_ads} "premissa 1" "premissa 2"`, leia os artigos que ele indicar e registre cada checagem em `knowledge_checks`: veredito sustenta, contradiz ou sem cobertura, com título, URL oficial e nota. Sustenta e contradiz sem URL oficial são recusados pelo `dossier.py`. Se contradiz, corrija o texto e o plano antes de mostrar.

Regras comuns:

- Resultado de busca e trecho não são leitura: `exact` e `strong` exigem ler o artigo inteiro.
- Cada plataforma tem a sua base e o seu índice; a busca recusa consulta da outra plataforma.
- Nunca atribua uma heurística interna à Meta ou ao Google. Política, cobrança, elegibilidade e regras que mudam exigem fonte ao vivo.
- Qualidade da busca: `python3 scripts/eval_retrieval.py --compare` antes e depois de mexer em pesos, no dicionário (`knowledge/retrieval-rewrites.json`) ou na base.
