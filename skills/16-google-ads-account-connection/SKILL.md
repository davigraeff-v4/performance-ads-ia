---
name: 16-google-ads-account-connection
description: Confirma de forma não destrutiva a conta Google Ads correta, manager account, customer ID, moeda, timezone e capacidade real do MCP. Use antes de ler performance Google Ads, auditar conta conectada ou depender de dados atuais da plataforma.
---

# Conexão da Conta Google Ads

## Pré-requisitos

1. Skill `00-configuracao-mcp` concluída para Google Ads, quando houver MCP.
2. Skill `01-client-campaign-intake` com cliente e conta esperada.
3. `CLIENTE.md` e dossiê atual.

## Processo

1. Inventariar as ferramentas realmente expostas pelo MCP oficial.
2. Listar customers diretamente acessíveis sem mutação.
3. Confirmar customer ID mascarado, nome, moeda e timezone.
4. Confirmar `login-customer-id`/manager account quando o acesso for indireto.
5. Testar consulta GAQL simples e somente leitura.
6. Registrar recursos ou campos indisponíveis sem improvisar alternativa.
7. Pedir confirmação diante de qualquer ambiguidade.

## Gates

- `validated_read`: customer inequívoco e consulta testada.
- `ambiguous`: mais de um customer plausível; bloquear.
- `unavailable`: MCP, credencial, developer token ou customer indisponível.
- `file_based`: sem conexão, mas exports utilizáveis.
- `context_only`: planejamento sem dados atuais da conta.

No V1 não existe `validated_write` para Google Ads. Não testar escrita criando objeto descartável.

## Registro

Salvar no dossiê data, customer mascarado, manager mascarado, moeda, timezone, modo de fonte, ferramentas e limitações. Nunca registrar developer token, OAuth, ADC, JSON de credencial ou configuração completa.
