# MCP oficial, servidor de escrita e API do Google Ads

- **Dois servidores.** O MCP oficial (`google_ads`) só lê. A escrita é do servidor local `googleAdsServer` (escopo de usuário, `~/.mcp/google-ads`), que também lê. O que não cabe nele é `manual_only` e é registrado depois como `executed_manually`.
- **Validar não grava.** Toda ferramenta de escrita começa com `validate_only=true`: a API confere permissão, developer token e regras, e nada muda. Só `validate_only=false` grava. A resposta de validação aceita é `ok: true` com resultado vazio.
- **Lista de contas e MCC.** O servidor só altera contas de `allowed_accounts.json` e entra em cada uma pela MCC registrada ali. Conta fora da lista é lida, mas a escrita volta bloqueada. `USER_PERMISSION_DENIED` costuma ser MCC de entrada errada, não falta de acesso.
- **Exclusão bloqueada no servidor.** Operação `remove` ou status `REMOVED` volta bloqueada; pausar é o máximo.
- **Dinheiro em micros.** Orçamento e lance vão em micros (R$ 1,00 = 1.000.000) e múltiplos de 10.000. `update_campaign_budget` recebe reais e converte; recusa orçamento compartilhado sem `allow_shared_budget=true`.
- **IDs compostos.** Anúncio é `<grupo>~<anúncio>` e palavra-chave é `<grupo>~<critério>` em `set_status` e nos resource names de `mutate`.
- **Confirmação.** Depois de gravar, reler o alvo por GAQL e conferir `get_change_history`; o evento sai com o e-mail do login OAuth e cliente API. Cada chamada de escrita também fica em `~/.mcp/google-ads/logs/mutations.jsonl`.
- **Performance Max.** Não aparece em consultas `FROM ad_group_ad`; conferir em `FROM campaign` e mexer em grupos de recursos por `assetGroups`.
- **Histórico de alterações de 30 dias.** `change_event` só expõe os últimos 30 dias. Quedas cuja causa pode estar antes disso exigem o Histórico de Alterações da interface, e o diagnóstico precisa declarar essa limitação.
- **Termos de pesquisa parciais.** O relatório de termos esconde parte do gasto por limite de privacidade. Informe a cobertura (quanto do gasto os termos visíveis representam) antes de concluir sobre desperdício.
- **Palavras-chave não competem entre si.** Palavras-chave e grupos do mesmo anunciante não disputam o mesmo leilão: o Google escolhe um, por prioridade de correspondência, relevância e classificação do anúncio ([priorização de grupos de anúncios e de recursos](https://support.google.com/google-ads/answer/2756257)). Consolidar campanhas duplicadas pode ter bons motivos, mas "leilão interno" não é um deles.
