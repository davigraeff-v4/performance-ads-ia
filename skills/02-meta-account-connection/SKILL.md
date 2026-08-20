---
name: 02-meta-account-connection
description: Confirma de forma não destrutiva a conta Meta correta, ativos, moeda, timezone, permissões e capacidades do MCP. Use antes de qualquer leitura de performance, planejamento operacional ou execução.
---

# Conexão e Escopo da Conta Meta

## Pré-requisitos

1. Skill `01` com cliente e conta esperada.
2. `CLIENTE.md` e representação candidata; usar dossiê somente em continuação de operação já persistida.
3. Em `connected_read`, conexão Meta já disponível; executar a skill `00` somente quando estiver ausente ou falhar. Em `file_based` ou `context_only`, esta skill é pulada.

## Processo

1. Listar contas acessíveis sem fazer mutação.
2. Comparar nome, ID mascarado, business, moeda e timezone com a ficha.
3. Confirmar pixel/dataset, página, Instagram, catálogo e domínio quando aplicáveis.
4. Inventariar ferramentas de leitura e escrita realmente expostas.
5. Registrar permissões insuficientes e ativos indisponíveis.
6. Pedir confirmação se houver qualquer ambiguidade.

## Gate

- `validated_read`: conta inequívoca e leitura testada.
- `validated_write`: leitura validada mais ferramenta/permissão de escrita detectada.
- `ambiguous`: mais de uma conta plausível; bloquear.
- `unavailable`: conta ou ferramenta ausente; modo consultivo/local.

## Registro

Acrescentar à candidata data da consulta, nome, ID mascarado, moeda, timezone, ativos e capacidades. Persistir isso no dossiê somente após aprovação editorial. ID integral só pode existir em estado local estritamente necessário; nunca em conhecimento ou exemplo.

## Proibição

Não usar uma conta "parecida" para continuar. Não testar escrita criando objeto descartável.
