---
name: 26-gtm-tracking-audit-fix
description: Audita containers do Google Tag Manager (tags, triggers, variáveis) via API direta, aponta rastreamento errado ou ausente e propõe correção como change set aprovável. Use quando o cliente rastreia via GTM e a skill 03 identificar necessidade de inspeção direta do container, ou quando o gestor pedir explicitamente revisão/ajuste de tracking no GTM.
---

# Auditoria e Correção de Tracking via GTM

## Quando usar

Esta skill complementa `03-measurement-data-quality`: a 03 audita o que a plataforma de mídia (Meta ou Google Ads) reporta sobre a própria mensuração; esta skill inspeciona a fonte real do rastreamento quando ele passa por um container GTM — tags GA4, conversion linker, tags de conversão Google Ads, Pixel/CAPI via parceiro, consent mode, triggers e variáveis. Acionar quando:

- A skill 03 apontar divergência que só se explica olhando o container (tag duplicada, disparo errado, tag ausente).
- O gestor pedir explicitamente "revisar/auditar/corrigir tracking no GTM" ou equivalente.
- Uma otimização (`12-optimization-change-set`) depender de corrigir uma tag antes de a mudança de mídia fazer sentido.

Não é uma plataforma de mídia paga: a mesma auditoria pode servir tanto ao ramo Meta quanto ao Google Ads de um mesmo dossiê.

## Instalação

Se o gestor perguntar como instalar ou configurar a API do Google Tag Manager, siga e explique o passo a passo de `README.md §16` (apêndice "Google Tag Manager (GTM)"): criar projeto e OAuth Client no Google Cloud Console, habilitar a Tag Manager API, instalar `integrations/gtm/` em ambiente Python isolado, salvar o client secret em `credentials/` e preencher `.env` a partir de `.env.example`. Nunca peça para o gestor colar client secret, JSON de credencial ou token no chat — oriente a salvar o arquivo localmente e apenas confirmar o caminho.

## Pré-requisitos técnicos

- `integrations/gtm/` instalado (`pip install -e integrations/gtm`) e `.env` preenchido conforme `.env.example` (`PERFORMANCE_ADS_GTM_CREDENTIALS_PATH` obrigatório). Ver `README.md §16` para o passo a passo completo.
- Leitura sempre disponível com `PERFORMANCE_ADS_GTM_DECLARED_CAPABILITIES` incluindo `reporting` (padrão).
- Escrita (criar/editar tag, trigger, variável) só ocorre quando `PERFORMANCE_ADS_GTM_WRITE_MODE != disabled`, a capability `tag_management` está declarada, e o container está em `PERFORMANCE_ADS_GTM_ALLOWED_CONTAINER_IDS`. Sem isso, tratar como `manual_only` — igual à regra que já vale para escrita Google Ads.
- **Esta integração nunca publica.** O escopo OAuth não inclui `tagmanager.publish` e não existe função de publish no código (`integrations/gtm/src/performance_ads_gtm/`). Uma vez aprovada e criada/editada em rascunho (workspace), a publicação da versão no GTM permanece manual, feita pelo gestor ou responsável técnico do cliente na UI do GTM.

## Leituras

1. `knowledge/measurement/measurement-quality.md`.
2. Para Meta: `knowledge/official-meta/measurement-and-capi.md` (o que a tag GTM precisa alimentar).
3. Para Google Ads: `knowledge/official-google/conversions-bidding-and-budget.md`.

## Processo

1. **Identificar o container.** Usar `python3 scripts/gtm_audit.py --list-accounts` e `--list-containers --account-path accounts/{id}` para localizar a conta/container do cliente. Registrar `account_path` e `container_path` na candidata; persistir só após aprovação editorial.
2. **Snapshot somente leitura.** `python3 scripts/gtm_audit.py --snapshot --container-path {path}` retorna tags, triggers e variáveis do workspace padrão. Nunca afirmar o que está configurado sem esse retorno.
3. **Cruzar com o esperado.** Para cada mecanismo de mensuração relevante (GA4 config, conversion linker, tag de conversão Google Ads, Pixel/CAPI via parceiro, consent mode), verificar se existe, se dispara no trigger certo e se não há duplicidade ou conflito (ex: gtag.js e GTM rastreando o mesmo evento).
4. **Classificar cada achado** com o mesmo vocabulário da skill 03: `confiavel`, `utilizavel_com_ressalvas`, `insuficiente`. Rotular claramente `GTM informa` (fato observado no container) versus `Meta informa`/`Google informa` (o que a plataforma de mídia espera) versus `metodologia recomenda`.
5. **Se houver correção acionável**, gerar mudança no formato de `12-optimization-change-set`: alvo `gtm_tag`, `gtm_trigger` ou `gtm_variable`, com o path do recurso como ID; antes e depois; por quê; risco; como desfazer; modo `api_script` (ou `manual_only` sem allowlist). Marcar `platform` como a plataforma de mídia que a tag serve (`meta` ou `google_ads`), nunca "gtm": GTM não é plataforma de mutação no dossiê. Filtros de acionador seguem `knowledge/platform-quirks/gtm-api.md`: negação é parâmetro `negate` dentro de `parameter`, e todo filtro é conferido por leitura depois de gravado.
6. **Nunca criar/editar diretamente nesta etapa.** Esta skill só propõe. A execução real (`scripts/gtm_edit.py`) só roda dentro de `13-approved-change-executor`, depois de `/aprovar-operacao`.

## Gate de escrita (preflight, espelha o Google Ads)

Antes de qualquer item GTM entrar como executável em `13-approved-change-executor`:

1. Confirmar `write_mode` != `disabled` e capability `tag_management` declarada.
2. Confirmar `container_id` do alvo está na allowlist local.
3. Se qualquer uma falhar, marcar o item `manual_only` — mesma tratativa que change sets Google Ads recebem enquanto não houver escrita homologada.
4. Publicação nunca é um item de change set: não existe caminho de execução para publish nesta integração. Se o resultado esperado exige a mudança ir ao ar, o item termina com a instrução explícita "publicar manualmente no GTM" como passo humano fora do escopo de `/executar-operacao`.

## Saída

Entregar no chat e manter na candidata: containers inspecionados, snapshot resumido, achados classificados com rótulo de fonte, itens de correção propostos prontos para o change set da plataforma e limitações. Criar/atualizar dossiê somente após aprovação editorial.

## Proibições

- Não declarar tag "correta" sem ter lido o snapshot.
- Não publicar, nem sugerir automação de publish.
- Não misturar containers/contas de clientes diferentes.
- Não tratar recomendação automática do GTM/Google como aprovação do gestor.
