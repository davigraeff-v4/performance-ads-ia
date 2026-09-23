# API do Google Tag Manager (`scripts/gtm_edit.py`)

## Negação em filtros de acionador

"Não contém" / "não corresponde" é expresso como parâmetro booleano **dentro** de `parameter` da condição:

```json
{"type": "contains", "parameter": [
  {"type": "template", "key": "arg0", "value": "{{Page URL}}"},
  {"type": "template", "key": "arg1", "value": "/obrigado"},
  {"type": "boolean", "key": "negate", "value": "true"}
]}
```

Um campo `"negate": true` solto na condição é **ignorado sem erro**, e o filtro passa a significar o oposto. Sempre leia o acionador depois de criar ou editar.

## Escrita segura

- A escrita só acontece em rascunho de workspace; publicar é sempre manual, na interface do GTM.
- O container do caminho (`accounts/{id}/containers/{id}/…`) precisa ser o mesmo `--container-id` autorizado na allowlist; caminhos de outro container são recusados.
- Atualizações leem o recurso atual, mesclam os campos enviados e mandam o `fingerprint`: um corpo parcial não apaga campos, e uma edição feita ao mesmo tempo na interface gera erro em vez de ser sobrescrita.
- Em `PERFORMANCE_ADS_GTM_WRITE_MODE=validate_only`, nada é gravado: o script devolve o que seria enviado.
