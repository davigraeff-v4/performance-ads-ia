---
name: 25-performance-ads-router
description: Roteia e executa solicitações de Meta Ads ou Google Ads escolhendo automaticamente intenção, plataforma, modo de fonte, dossiê e sequência de skills. Use para configurar, cadastrar cliente, pesquisar palavras-chave, planejar, criar, auditar, analisar, otimizar, relatar, aprovar, executar ou reverter operações de mídia paga, inclusive quando o usuário não mencionar comandos ou skills. Não use para SEO, GA4, Search Console, Google Trends ou plataformas fora do contrato V1.
---

# Roteador PERFORMANCE ADS IA

Atuar como única entrada implícita do agent. Selecionar e executar as skills internas; não pedir que o gestor as acione manualmente.

## 1. Preparar o contexto

1. Ler `CONTRATO-OPERACIONAL.md` e `routing_matrix.json`.
2. Identificar a intenção normalizada: `configuracao`, `onboarding`, `pesquisa_palavras_chave`, `planejamento`, `criacao`, `auditoria`, `analise`, `otimizacao`, `relatorio`, `aprovacao`, `execucao` ou `reversao`.
3. Identificar `requested_platforms`, `active_platforms` e `source_mode` por plataforma.
4. Se houver cliente, ler `clients/{slug}/CLIENTE.md` antes de perguntar informação já registrada.
5. Localizar o dossiê por `operation_id`, cliente, plataforma, escopo, tipo, status e atualização. Nunca escolher apenas o arquivo mais recente quando houver mais de um candidato plausível.
6. Tratar dossiê sem `schema_version` ou `route` como legado: preservar o histórico e acrescentar os campos V1 ao atualizar.

Perguntar em uma única rodada somente quando cliente, plataforma, conta, objetivo ou operação permanecerem materialmente ambíguos.

## 2. Resolver a rota

Executar o roteador determinístico depois de classificar a demanda:

```bash
python3 scripts/route_request.py \
  --intent analise \
  --platform google_ads \
  --source-mode connected_read \
  --json
```

Para escopo multicanal, informar os modos separadamente:

```bash
python3 scripts/route_request.py \
  --intent otimizacao \
  --platform both \
  --meta-source-mode connected_read \
  --google-source-mode file_based \
  --json
```

Adicionar `--requires-keywords` somente quando Search, search themes ou validação de demanda exigirem a skill `18`.

Se a rota retornar `blocked`, parar antes das skills operacionais e apresentar o gate. Não improvisar plataforma, fonte, conta ou objetivo.

## 3. Executar as skills

1. Seguir `planned_skills` na ordem retornada e usar `output` como contrato do tipo de entrega esperado para cada ramo.
2. Ler integralmente cada `skills/{nome}/SKILL.md` antes de executá-la.
3. Não abrir skills de outra plataforma.
4. Não executar `00-configuracao-mcp` apenas porque a fonte é por arquivo ou contexto.
5. Em `connected_read`, validar a conta por `02` ou `16`; voltar à `00` somente se a conexão estiver ausente ou falhar.
6. Para otimização, exigir diagnóstico `11` no Meta ou `24` no Google Ads antes da `12`.
7. Atualizar o dossiê ao longo do fluxo, sem interromper o gestor entre skills que podem rodar silenciosamente.

## 4. Registrar a trilha

Salvar no dossiê:

- `router_version`, `route_id`/`route_ids` canônicos (`intencao:plataforma:source_mode`) e `output_contracts` por plataforma.
- Intenção, plataformas e modos de fonte.
- Skills planejadas, executadas e puladas com motivo.
- Gates encontrados e decisão tomada.
- Estado final correto.

O dossiê é a fonte estruturada e a trilha de auditoria. Ele não deve ser a única entrega ao gestor.

## 5. Entregar no chat

Depois de persistir o resultado, apresentar no chat um relatório autossuficiente contendo, conforme a demanda:

1. Veredito executivo e confiança.
2. Escopo, conta, fonte, janela, comparação e atribuição.
3. Resultado de negócio e KPIs com denominadores.
4. Achados com evidência, impacto, hipótese principal, alternativa e limitação.
5. Plano de ação com alvo, prioridade, responsável, prazo, janela e critérios de sucesso/parada.
6. Testes, riscos, indisponibilidades e próxima decisão.
7. Status, `operation_id` e caminho do dossiê apenas como referência final.

Não exigir que o gestor abra o arquivo para compreender o diagnóstico ou decidir. O chat não precisa reproduzir logs, JSON, GAQL ou respostas brutas.

## 6. Gates de mutação

- `planejamento`, `auditoria`, `analise` e `relatorio` terminam `analysis_only` quando não houver mudança proposta.
- `criacao`, `otimizacao` e `reversao` podem terminar `proposed`; nunca executar no mesmo comando.
- `aprovacao` registra a versão/hash e termina `approved`; não executa.
- `execucao` exige comando explícito, aprovação válida e skill `13`.
- Google Ads permanece `manual_only` enquanto `write_tools_registered` não estiver homologado.
- Nunca excluir, arquivar, ativar recomendações automáticas ou ampliar o lote.
