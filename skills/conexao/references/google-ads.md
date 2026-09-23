<!-- Referência do módulo `conexao`; etapa `conexao/google-ads` nas rotas. -->

# Conexão da Conta Google Ads

## Pré-requisitos

1. Etapa `conexao/configuracao-mcp` concluída para Google Ads, quando houver MCP.
2. Etapa `contexto-cliente` com cliente e conta esperada.
3. `CLIENTE.md` e representação candidata; usar dossiê somente em continuação de operação persistida.
4. Se o MCP ainda não estiver configurado, seguir o apêndice opcional da seção 15 do `README.md`; nunca pedir segredos no chat.

## Processo

1. Inventariar as ferramentas realmente expostas pelo MCP oficial.
2. Chamar `customers_list_accessible_customers` sem mutação. Lembrar que a resposta lista customers diretamente acessíveis e pode retornar MCCs, não toda a hierarquia abaixo delas.
3. Se houver mais de um customer plausível, mascarar os IDs, apresentar as opções mínimas e pedir confirmação antes de consultar performance.
4. Confirmar `login-customer-id`/MCC quando o acesso for indireto; remover hífens antes da chamada.
5. Chamar `metadata_get_resource_metadata` para o recurso que será consultado; não adivinhar campos GAQL.
6. Testar `search_search` no customer confirmado com consulta pequena, `limit` e somente os campos necessários.
7. Confirmar ID mascarado, nome, moeda e timezone contra `CLIENTE.md` ou confirmação do gestor.
8. Registrar recursos ou campos indisponíveis sem improvisar alternativa.
9. Pedir confirmação diante de qualquer ambiguidade.
10. Quando `google_ads_extended` estiver instalado, chamar `get_extended_capabilities` e registrar separadamente `planner_enabled`, `write_mode`, presença de credenciais e quantidade de customers permitidos, sem revelar valores.

## Preflight seguro

- Nunca mostrar developer token, OAuth, ADC, refresh token ou configuração completa.
- Nunca selecionar automaticamente o primeiro customer quando existirem várias contas plausíveis.
- Não inferir que a MCC do developer token é a mesma MCC usada como `login-customer-id`.
- Não chamar `search_search` antes de descobrir os campos com metadata.
- Não consultar períodos ou níveis além do escopo pedido.

## Diagnóstico de falhas

- Transporte falha: voltar à etapa `conexao/configuracao-mcp` e revisar launcher/executável.
- `DefaultCredentialsError` ou `invalid_grant`: marcar autenticação indisponível; não pedir o segredo no chat.
- `USER_PERMISSION_DENIED`: conferir identidade autenticada, customer alvo e cadeia da MCC.
- Lista vazia: conferir se o usuário/service account recebeu acesso no Google Ads.
- Token limitado a teste: não alegar acesso a produção.
- Metadata funciona e GAQL falha: revisar compatibilidade dos campos e condições antes de culpar a autenticação.

## Gates

- `validated_read`: customer inequívoco e consulta testada.
- `ambiguous`: mais de um customer plausível; bloquear.
- `unavailable`: MCP, credencial, developer token ou customer indisponível.
- `file_based`: sem conexão, mas exports utilizáveis.
- `context_only`: planejamento sem dados atuais da conta.

Na etapa V1.1 inicial não existe `validated_write` para Google Ads. O complemento instalado com `write_tools_registered: false` não satisfaz esse gate. Não testar escrita criando objeto descartável.

Planner é uma capability separada: somente registrar `planner_connected` depois de `planner_enabled: true`, customer allowlisted e uma chamada real bem-sucedida. Basic Access ou transporte conectado isoladamente não bastam.

## Registro

Acrescentar à candidata data, customer/manager mascarados, moeda, timezone, modo de fonte, ferramentas, revisão e limitações. Persistir no dossiê somente após aprovação editorial. Nunca registrar developer token, OAuth, ADC, JSON de credencial ou configuração completa.
