---
name: 25-performance-ads-router
description: Roteia solicitações de Meta Ads ou Google Ads, executa as skills necessárias e entrega uma versão completa no chat antes de persistir um dossiê aprovado. Use para configurar, cadastrar cliente, pesquisar palavras-chave, planejar, criar, auditar, analisar, otimizar, relatar, aprovar, executar ou reverter operações de mídia paga. Não use para SEO, GA4, Search Console, Google Trends ou plataformas fora do contrato V1.
---

# Roteador PERFORMANCE ADS IA

Atuar como única entrada implícita do agent. Selecionar e executar as skills internas; não pedir que o gestor as acione manualmente.

## 1. Preparar o contexto

1. Ler `CONTRATO-OPERACIONAL.md` e `routing_matrix.json`.
2. Identificar **todas** as intenções normalizadas presentes na mensagem — pode haver mais de uma: `configuracao`, `onboarding`, `pesquisa_palavras_chave`, `planejamento`, `criacao`, `auditoria`, `analise`, `otimizacao`, `relatorio`, `aprovacao`, `execucao` ou `reversao`.
3. Identificar `requested_platforms`, `active_platforms` e `source_mode` por plataforma.
4. Se houver cliente, ler `clients/{slug}/CLIENTE.md` antes de perguntar informação já registrada.
5. Localizar no contexto uma versão candidata ainda não persistida. Localizar dossiê somente quando já houve aprovação editorial ou a demanda continua uma operação registrada.
6. Em dossiê existente, buscar por `operation_id`, cliente, plataforma, escopo, tipo, status e atualização. Tratar arquivo sem `schema_version` ou `route` como legado.

### Aprovação editorial versus operacional

- Se existe candidata `awaiting_record_approval` e o gestor diz “aprovado”, “pode registrar” ou equivalente sem `/aprovar-operacao <id>`, interpretar como aprovação editorial e criar o dossiê exato daquela versão.
- Somente `/aprovar-operacao <id>` ou autorização operacional explícita com operação, versão e hash entra na intenção `aprovacao`.
- Aprovação editorial não aprova nem executa change set.

Perguntar em uma única rodada somente quando cliente, plataforma, conta, objetivo ou operação permanecerem materialmente ambíguos.

### Mensagens compostas (mais de uma intenção)

`onboarding` e `configuracao` são intenções estreitas — planejam pouquíssimas skills (ex: `onboarding` só planeja `01-client-campaign-intake`) e **não** incluem a skill 15/17 de recuperação de conhecimento. Se a mesma mensagem também contiver uma pergunta de funcionamento, boas práticas, estratégia ou otimização, essa segunda parte é uma intenção separada (tipicamente `planejamento`, `analise` ou `otimizacao`) que **tem** a skill 15/17 como passo `always` — e precisa da sua própria chamada ao `route_request.py` e da sua própria execução de skills. Nunca responder a segunda pergunta usando só o que a primeira intenção carregou.

Exemplo real que já aconteceu: gestor manda "tenho um novo cliente X, aqui está a conta... qual a melhor forma de rodar campanha de visitas ao local e quais as boas práticas?" numa mensagem só. Isso é `onboarding:meta` **e** `planejamento:meta` — resolver e executar as duas rotas, não só a primeira.

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
7. Para `auditoria`, `analise` e `otimizacao`, usar `depth_mode=full` salvo restrição explícita do gestor.
8. Manter a representação estruturada em memória; não criar ou atualizar dossiê novo antes da aprovação editorial.

## 4. Montar a versão candidata

Manter na candidata:

- `router_version`, `route_id`/`route_ids` canônicos (`intencao:plataforma:source_mode`) e `output_contracts` por plataforma.
- Intenção, plataformas e modos de fonte.
- Skills planejadas, executadas e puladas com motivo.
- Gates encontrados e decisão tomada.
- Matriz de cobertura, pacote de evidências, achados, ações e estado persistido esperado.

Skill planejada deve aparecer como executada ou pulada com motivo. Uma skill obrigatória silenciosamente ausente bloqueia a candidata final.

## 5. Entregar no chat

Antes de persistir, apresentar no chat um relatório autossuficiente contendo, conforme a demanda:

1. Veredito executivo e confiança.
2. Escopo, conta, fonte, janela, comparação e atribuição.
3. Matriz de cobertura por nível e cobertura de investimento/conversões.
4. Resultado de negócio, KPIs, comparações, unidades e denominadores.
5. Pacote de evidências identificadas.
6. Achados com evidência, impacto, hipótese principal, alternativa e limitação.
7. Plano de ação ligado aos achados, com baseline, alvo, prioridade, responsável, prazo, janela, sucesso/parada, dependência e risco.
8. Testes, riscos, indisponibilidades e próxima decisão.

Marcar a entrega como candidata e solicitar aprovação editorial para registrar. Após aprovação, persistir exatamente a mesma versão e informar status, `operation_id` e caminho. O chat não precisa reproduzir logs, JSON, GAQL ou respostas brutas, mas deve mostrar todos os dados decisórios.

## 6. Gates de mutação

- Antes da aprovação editorial, demandas novas terminam `awaiting_record_approval` no chat e não têm dossiê.
- Após aprovação editorial, `planejamento`, `auditoria`, `analise` e `relatorio` persistem `analysis_only` quando não houver mutação.
- Após aprovação editorial, `criacao`, `otimizacao` e `reversao` podem persistir `proposed`; nunca executar no mesmo comando.
- `aprovacao` registra a versão/hash e termina `approved`; não executa.
- `execucao` exige comando explícito, aprovação válida e skill `13`.
- Google Ads permanece `manual_only` enquanto `write_tools_registered` não estiver homologado.
- Nunca excluir, arquivar, ativar recomendações automáticas ou ampliar o lote.
