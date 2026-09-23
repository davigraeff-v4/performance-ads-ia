---
name: conexao
description: Confirma, sem alterar nada, a conta certa e a capacidade real do conector Meta Ads ou Google Ads, e configura ou diagnostica os conectores quando faltam. Use antes de qualquer leitura ao vivo, em /configuracao-mcp e quando a conexão falhar.
---

# Conexão com as plataformas

Módulo de conexão. Cada etapa da rota aponta para uma referência:

| Etapa na rota | Quando | Leia |
|---|---|---|
| `conexao/meta` | leitura ao vivo do Meta (`connected_read`) | `references/meta.md` |
| `conexao/google-ads` | leitura ao vivo do Google Ads (`connected_read`) | `references/google-ads.md` |
| `conexao/configuracao-mcp` | /configuracao-mcp, conector ausente ou falhando | `references/configuracao-mcp.md` |

Regras comuns:

- "Conectado" não prova conta certa, leitura nem escrita: confirme cada uma.
- Nunca peça, mostre ou grave token, secret, JSON de credencial ou resposta OAuth.
- Em `file_based` ou `context_only`, este módulo não roda: não abra a configuração do conector só porque a fonte é arquivo.
- Antes de ler entidades pelo conector Meta, leia `knowledge/platform-quirks/meta-ads-mcp.md` (paginação, status).
