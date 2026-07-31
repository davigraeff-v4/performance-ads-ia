# Checklist de Execução

- [ ] Comando `/executar-operacao <id>` recebido.
- [ ] Dossiê está `approved`.
- [ ] Versão e hash conferem.
- [ ] Aprovação tem responsável, timestamp e declaração.
- [ ] Conta, moeda e timezone conferem.
- [ ] MCP e permissão de escrita foram validados.
- [ ] Estado atual dos alvos confere com snapshot.
- [ ] Não há exclusão ou arquivamento.
- [ ] Todos os budgets mostram impacto financeiro.
- [ ] A ordem e as dependências estão definidas.
- [ ] Valores anteriores permitem reversão quando prometida.
- [ ] Itens manuais/bloqueados foram removidos da fila MCP.
- [ ] Resultado será registrado por item.
- [ ] Snapshot posterior será lido antes do encerramento.

Falha em qualquer item crítico bloqueia a execução.

