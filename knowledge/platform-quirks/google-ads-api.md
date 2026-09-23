# MCP oficial e API do Google Ads

- **Somente leitura.** O MCP oficial não escreve; toda mudança no Google Ads é `manual_only` e registrada depois com `dossier.py record-execution` como `executed_manually`.
- **Histórico de alterações de 30 dias.** `change_event` só expõe os últimos 30 dias. Quedas cuja causa pode estar antes disso exigem o Histórico de Alterações da interface, e o diagnóstico precisa declarar essa limitação.
- **Termos de pesquisa parciais.** O relatório de termos esconde parte do gasto por limite de privacidade. Informe a cobertura (quanto do gasto os termos visíveis representam) antes de concluir sobre desperdício.
- **Palavras-chave não competem entre si.** Palavras-chave e grupos do mesmo anunciante não disputam o mesmo leilão: o Google escolhe um, por prioridade de correspondência, relevância e classificação do anúncio ([priorização de grupos de anúncios e de recursos](https://support.google.com/google-ads/answer/2756257)). Consolidar campanhas duplicadas pode ter bons motivos, mas "leilão interno" não é um deles.
