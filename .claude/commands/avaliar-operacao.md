---
description: "Avalia se uma operação executada funcionou, comparando com os critérios registrados"
argument-hint: "[operação ou deixe vazio para ver as avaliações vencidas]"
---

Execute `skills/performance-ads-roteador/SKILL.md` com intenção fixa `avaliacao`. Se a operação não foi informada, rode `python3 scripts/client_brief.py {slug}` (ou `scripts/dossier.py list --open` sem cliente) e mostre as avaliações vencidas pelo título. Leia os dados da janela depois da execução, compare com os critérios de sucesso e de parada registrados e explique no chat se funcionou e por quê, à luz da base oficial. Só registre com `dossier.py evaluate` depois do aval do gestor. Não execute nem reverta nada.
