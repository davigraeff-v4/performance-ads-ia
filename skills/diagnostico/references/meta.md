<!-- Referência do módulo `diagnostico`; etapa `diagnostico/meta` nas rotas. -->

# Diagnóstico de Performance Meta Ads

## Leituras

1. `knowledge/methodology/diagnostic-framework.md`.
2. `knowledge/methodology/windows-and-comparisons.md`.
3. `knowledge/methodology/diagnostic-coverage-contract.md`.
4. Trilha de negócio e gate da etapa `mensuracao`.
5. `quality/analysis-checklist.md`.
6. `knowledge/platform-quirks/meta-ads-mcp.md` antes de ler entidades pelo conector (paginação, status).
7. `templates/resposta-chat.md` para a forma da entrega.

## Processo

1. Usar a profundidade devolvida pela rota: `full` em auditoria ou quando o gestor pedir análise completa; `focused` nos demais casos, com o foco declarado.
2. Confirmar escopo, conta, moeda, timezone, janela, comparação e atribuição.
3. Registrar mudanças e eventos que afetam comparabilidade.
4. Em `full`, cobrir todas as camadas Meta (conta, campanha, conjunto, anúncio/criativo, posicionamento/dispositivo, público/geografia/demografia, conversão, mensuração, negócio e mudanças) e registrar para cada uma se foi analisada, ficou indisponível, insuficiente ou não se aplica.
5. Reunir as evidências comparativas: unidade, definição, denominador, valores, variações e quanto do investimento e das conversões cada leitura cobre. Para status de entidades, ler por IDs; nunca inferir pausa pela ausência numa listagem paginada.
6. Decompor entrega → resposta → conversão → qualidade/receita e aprofundar entidades materiais e outliers.
7. Cruzar Meta e fonte comercial; preservar divergências.
8. Formular diagnósticos alternativos e a evidência que os distingue.
9. Listar as premissas de mecanismo de cada achado e ação (ex.: "conjuntos sobrepostos competem no leilão") e conferir cada uma pela etapa `revisor/meta` (`python3 scripts/kb_check.py --platform meta "premissa 1" "premissa 2"`) e por `ads_get_help_article`, antes de apresentar. Premissa contradita pela fonte muda o texto e o plano; registrar a checagem com fonte.
10. Priorizar por impacto, confiança, esforço e reversibilidade.

## Referências oficiais da Meta (padrão em `connected_read`)

Em toda análise, otimização e auditoria com leitura ao vivo, consultar as ferramentas de referência do conector, todas só de leitura, antes de fechar os achados:

| Ferramenta | Para que serve no diagnóstico |
|---|---|
| `ads_insights_performance_trend` (com `hide_ui: true`) | direção de cada métrica por conjunto ou anúncio, dentro do grupo de otimização |
| `ads_insights_anomaly_signal` | alertas da própria Meta: público estreito, quedas, picos |
| `ads_insights_auction_ranking_benchmarks` | ranking de qualidade, engajamento e conversão do anúncio contra anúncios do mesmo leilão |
| `ads_insights_industry_benchmark` | custo por resultado, taxa de cliques, custo por mil impressões e conversão contra anunciantes parecidos |
| `ads_get_opportunity_score` | pontuação da conta e recomendações da Meta, com o ganho estimado |

Regras de leitura (detalhes em `knowledge/platform-quirks/meta-ads-mcp.md`):

- **Três referências, sempre nomeadas.** No chat, cada número importante é comparado com até três referências, dizendo de onde vem cada uma: **meta do cliente** (do `CLIENTE.md`), **linha de base** (o período anterior equivalente, calculado por nós) e **referência da Meta** (a ferramenta que devolveu). Ex.: "custo por conversa de R$ 9,09 · meta do cliente R$ 10,00 · mês anterior R$ 8,76 · a Meta classifica abaixo da média de anunciantes parecidos".
- **Resposta vazia é resposta.** Se a ferramenta disser que não há dados ("No industry benchmark data available") ou devolver rankings "Not Yet Available", escreva "a Meta não tem referência para esta conta neste período" e siga. Nunca estime o valor que faltou.
- **Comparação justa.** Referência do setor e ranking valem dentro do mesmo objetivo de otimização e do mesmo tipo de público (a ferramenta agrupa por isso). Não compare um conjunto de conversas com referência de compras.
- **Tendência não é comparação de período.** `performance_trend` usa todo o histórico disponível, sem janela declarada, e traz a variação em % sem sinal, com o rótulo GOOD/BAD. Use como indicação de direção ("a Meta vê piora no custo por resultado deste conjunto"), nunca como o número da comparação do período, que vem da leitura das entidades na janela escolhida.
- **Pontuação de oportunidade é da conta.** Nunca atribua a nota a uma campanha. As recomendações são da plataforma, não decisão do gestor: cada uma entra no chat como "a Meta recomenda…", com a nossa leitura (concordamos, discordamos ou depende), e só vira mudança pelo caminho normal do change set.
- **Alerta é pista, não causa.** Um alerta de anomalia abre uma pergunta a investigar; a causa vem dos dados.
- Em `file_based` ou `context_only`, estas ferramentas não se aplicam: dizer que a comparação com a Meta ficou indisponível e por quê.

## Saída

Entregar no chat, antes de qualquer dossiê, no formato de `templates/resposta-chat.md`: resumo, números com a leitura de cada um, achados (o que vimos, por que acreditamos, outra explicação possível, confiança), plano de ação com alvo, antes e depois, resultado esperado, janela, sucesso e parada, e a checagem com boas práticas. Campo sem evidência fica explicitamente indisponível. Separar:

- Problema de entrega.
- Problema de resposta/criativo.
- Problema de conversão.
- Problema de qualidade/receita.
- Problema de mensuração.

Uma camada aplicável ausente bloqueia o rótulo de diagnóstico completo. Iterar no chat e pedir aprovação do conteúdo. Só depois registrar com `scripts/dossier.py new` (análise pura fica `analysis_only`); nenhuma mutação é gerada em análise pura.

## Modo avaliação (`avaliacao`, profundidade `quick`)

Quando a rota é de avaliação, o diagnóstico é curto e fechado na operação: ler só os alvos da operação e o que os cerca (a campanha e os conjuntos ou grupos vizinhos que podem ter absorvido o efeito), na janela depois da execução contra a linha de base registrada. Para cada critério de sucesso e de parada, dizer o número combinado, o número observado e a situação. Separar o efeito da mudança de outras mudanças no período, sazonalidade e atraso de conversão; se não der para separar, o resultado é `inconclusive`. As premissas da explicação passam pela etapa `revisor/meta` (`kb_check.py`).
