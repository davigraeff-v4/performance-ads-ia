---
description: "Executa uma operação aprovada, item por item, e registra o resultado"
argument-hint: "[operação]"
---

Execute `skills/performance-ads-roteador/SKILL.md` com intenção fixa `execucao` e a operação informada. Exija aprovação válida (`dossier.py verify`), preflight e leitura de confirmação; registre cada item com `dossier.py record-execution` e nunca amplie o lote. No Google Ads, executar só pelo `googleAdsServer`, validando cada item com `validate_only=true` antes de gravar e conferindo depois por leitura e pelo histórico de alterações; o que for `manual_only` fica com o gestor.
