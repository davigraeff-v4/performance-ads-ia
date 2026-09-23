---
name: 25-performance-ads-router
description: Porta de entrada do PERFORMANCE ADS IA para qualquer pedido sobre Meta Ads, Google Ads ou rastreamento de mídia (GTM, pixel, conversões, UTM de campanha) — dúvidas, consultas rápidas, histórico do cliente, cadastro, palavras-chave, planejamento, criação, auditoria, análise, otimização, ajustes, relatórios, aprovação, execução e reversão. Tem precedência sobre skills genéricas de mídia paga e de analytics neste projeto. Não use para SEO, GA4, Search Console, Google Trends ou plataformas fora do contrato.
---

# Roteador PERFORMANCE ADS IA

Única entrada do agent. Classifica o pedido, executa as skills internas na ordem certa, entrega no chat no formato de `templates/resposta-chat.md` e, depois da aprovação do gestor, registra pelo `scripts/dossier.py`. O gestor nunca precisa acionar skills internas.

## 1. Preparar o contexto

1. Ler `CONTRATO-OPERACIONAL.md` uma vez por sessão. A matriz de rotas é lida pelo `route_request.py`; não é preciso abri-la.
2. Identificar **todas** as intenções da mensagem: `duvida`, `consulta`, `historico`, `configuracao`, `onboarding`, `pesquisa_palavras_chave`, `planejamento`, `criacao`, `auditoria`, `analise`, `otimizacao`, `ajuste`, `relatorio`, `aprovacao`, `execucao` ou `reversao`. A tabela de decisão e os exemplos estão no CLAUDE.md/AGENTS.md.
3. Identificar plataformas pedidas e o modo de fonte de cada uma: `connected_read`, `file_based`, `context_only` ou `unavailable`.
4. Com cliente identificado:
   - ler `clients/{slug}/CLIENTE.md`;
   - rodar `python3 scripts/client_history.py list {slug} --limit 8`;
   - mencionar no início da resposta operações abertas, decisões pendentes e avaliações vencidas que tenham relação com o pedido.
5. Histórico legado: os dossiês antigos na raiz da pasta do cliente são base de consulta somente leitura. Use `python3 scripts/client_history.py search {slug} "termos"` quando o gestor pedir para verificar o que já foi feito, quando a análise depender de uma decisão anterior ou antes de repetir uma recomendação. Abra o arquivo inteiro só quando o trecho encontrado for relevante.

Perguntar numa única rodada, e só quando cliente, plataforma, conta, objetivo ou operação continuarem materialmente ambíguos.

### Mensagens com mais de um pedido

`onboarding` e `configuracao` são rotas estreitas e não incluem a base oficial. Se a mesma mensagem também pergunta sobre funcionamento, estratégia ou otimização, essa segunda parte é outra intenção, com a sua própria chamada ao `route_request.py` e a sua própria execução.

Exemplo real: "tenho um novo cliente X, aqui está a conta… qual a melhor forma de rodar campanha de visitas ao local e quais as boas práticas?" são duas intenções, `onboarding:meta` e `planejamento:meta`. Resolva e execute as duas rotas.

### Aprovação do conteúdo versus aprovação de execução

- Se há uma versão apresentada no chat aguardando registro e o gestor diz "aprovado", "pode registrar" ou equivalente, sem `/aprovar-operacao`, isso é **aprovação do conteúdo**: registre com `dossier.py new` (ou `revise`, se a operação já existia).
- Só `/aprovar-operacao` ou uma autorização explícita de execução entra na intenção `aprovacao`. Se o gestor digitar `/aprovar-operacao` sem identificar a operação, rode `python3 scripts/dossier.py list --client {slug} --open`, mostre o título, a versão e o número de mudanças da operação candidata e peça confirmação antes de aprovar. Se houver mais de uma candidata, pergunte qual.
- Aprovar o conteúdo não aprova a execução. Aprovar a execução não executa.

## 2. Resolver a rota

```bash
python3 scripts/route_request.py --intent otimizacao --platform meta --source-mode connected_read --json
```

Multicanal, com modos separados:

```bash
python3 scripts/route_request.py --intent auditoria --platform both \
  --meta-source-mode connected_read --google-source-mode file_based --json
```

- `--depth full` fora de `auditoria` só quando o gestor pedir análise completa; a profundidade padrão de cada intenção vem na resposta.
- `--requires-keywords` quando Search, temas de pesquisa ou validação de demanda exigirem a skill `18`.
- `--requires-gtm-audit` quando o rastreamento passa por um container GTM, em auditoria ou otimização.
- Rota `blocked`: parar antes das skills operacionais e explicar o bloqueio. Não improvisar plataforma, fonte, conta ou objetivo.
- Ramo `not_applicable` (ex.: palavras-chave no Meta): seguir só com o outro ramo e dizer isso ao gestor.

## 3. Executar as skills

1. Seguir `planned_skills` na ordem, lendo cada `skills/{nome}/SKILL.md` antes de agir. Não abrir skills de outra plataforma.
2. Não executar `00-configuracao-mcp` só porque a fonte é arquivo ou contexto. Em `connected_read`, validar a conta pela `02` ou `16`; voltar à `00` só se a conexão faltar ou falhar.
3. Skills `15` e `17` rodam em toda rota que as planeja. Fora de `duvida`, elas **checam premissas**: liste as afirmações de mecanismo do diagnóstico, das mudanças ou da leitura de resultados e confira cada uma. No Meta, use também `ads_get_help_article` do conector. Registre cada checagem com veredito (sustenta, contradiz, sem cobertura), fonte e nota. Se contradiz, corrija o texto e o plano antes de mostrar.
4. `otimizacao` exige o diagnóstico `11` (Meta) ou `24` (Google Ads) antes da `12`. `ajuste` não exige diagnóstico: a decisão é do gestor; leia o estado atual do alvo e registre a motivação dele.
5. Antes de executar pelo conector Meta ou pela API do GTM, ler `knowledge/platform-quirks/`.
6. Guardar em memória, para o registro: rotas, skills executadas, skills não executadas com motivo, checagens de boas práticas, mudanças, critérios de avaliação e decisões pendentes.

Uma skill planejada não executada precisa de motivo de uma lista fechada: `condition_not_met` (só quando a condição da rota não é `always` e não se aplica), `source_unavailable`, `account_not_enabled`, `platform_not_applicable`, `user_restricted_scope` ou `no_platform_mechanism` (só para 15/17, e só em operação sem mudanças). O `dossier.py` rejeita outros casos.

## 4. Entregar no chat

Seguir `templates/resposta-chat.md` à risca: cabeçalho, resumo, números com a seção "Como ler esses números", achados, mudanças em blocos, checagem com boas práticas, como vamos avaliar, o que preciso de você e próximo passo. O exemplo completo está em `examples/synthetic/v2/otimizacao-remarketing.body.md`.

Nunca mostrar no chat IDs internos, hashes, nomes ou números de skills, rotas, JSON, GAQL, caminhos de arquivo ou logs de ferramenta. As exceções são o comando que o gestor precisa digitar e o caminho do dossiê depois de salvo.

`duvida`, `consulta` e `historico` terminam no chat, sem dossiê.

## 5. Registrar depois da aprovação do conteúdo

1. Escrever em `.work/`:
   - o **corpo**: o texto aprovado no chat, sem alterações de conteúdo, com `<!-- mudancas -->` no lugar dos blocos de mudança (o script renderiza as mudanças a partir do spec);
   - o **spec**: JSON no formato de `examples/synthetic/v2/otimizacao-remarketing.spec.json`.
2. Rodar `python3 scripts/dossier.py new --client {slug} --spec .work/{nome}.spec.json --body .work/{nome}.body.md`.
3. Se o script recusar, corrigir o spec ou o corpo e rodar de novo; nunca contornar escrevendo os arquivos à mão.
4. Informar ao gestor, numa linha, o caminho do dossiê e o próximo passo que o script devolve.

Regras do spec: `changes` vazio gera `analysis_only`. Com mudanças, são obrigatórios `knowledge_checks` e `evaluation` (data, critérios de sucesso e de parada). Uma operação com mudanças é de uma plataforma só; em multicanal, registre uma operação por plataforma.

## 6. Aprovar, executar, avaliar, reverter

- **Aprovar a execução** (`/aprovar-operacao`): `python3 scripts/dossier.py approve {operation_id} --statement "<frase literal do gestor>"`. O script calcula o hash e muda o status para aprovado.
- **Executar** (`/executar-operacao`): skill `13`. Ao terminar, registrar tudo com `dossier.py record-execution {operation_id} --results '<lista>'`. Isso inclui o que o gestor fez à mão (`executed_manually`, com as diferenças em relação ao aprovado). O status (executado, parcial, falhou) é calculado pelo script.
- **Mudanças manuais** (Google Ads, criação de conjunto de formulário no Meta, publicação no GTM): depois de aprovadas, o gestor aplica no gerenciador. Quando ele avisar, confirmar por leitura na plataforma sempre que possível e registrar com `record-execution`.
- **Avaliar** ao fim da janela: comparar com os critérios registrados, explicar no chat se funcionou e por quê (à luz da base oficial) e registrar com `dossier.py evaluate {operation_id} --result success|failure|inconclusive --notes "…"`.
- **Reverter**: nova operação `reversao` com os valores anteriores conhecidos, sempre com pausa, nunca com exclusão.
- **Mudar o conteúdo depois de registrado** e antes de executar: `dossier.py revise`, que cria uma nova versão e invalida a aprovação anterior.

## 7. Operações legadas abertas

Para aprovar ou executar uma operação legada ainda aberta (`proposed` ou `approved` num dossiê antigo):

1. `python3 scripts/dossier.py migrate clients/{slug}/{arquivo-legado}.md`;
2. revisar o rascunho gerado em `.work/` (títulos das mudanças, prazo de avaliação, checagens de boas práticas);
3. apresentar a versão migrada no chat;
4. registrar com `dossier.py new` depois da aprovação do conteúdo.

A aprovação operacional antiga não é transportada. O arquivo legado nunca é editado.

## 8. Gates

- Nunca excluir ou arquivar, nem na reversão; nunca ativar recomendações automáticas; nunca ampliar o lote aprovado.
- Google Ads permanece `manual_only` enquanto `write_tools_registered` não estiver homologado.
- GTM: escrita só em rascunho de workspace, com o container na allowlist local; publicação sempre manual.
- Qualquer mutação exige o dossiê registrado, `/aprovar-operacao` e `/executar-operacao`, nessa ordem.
