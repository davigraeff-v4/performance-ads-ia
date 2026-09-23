---
name: entrega
description: Gera relatórios Meta Ads, Google Ads ou multicanal, explicando o que foi bem, o que foi mal e por quê, e fecha análises e operações. Na Sprint 3 também exporta a entrega aprovada. Use em /relatorio-performance ou fechamento de análise/operação.
---

# Entrega: relatório e fechamento

## Leituras

1. `templates/relatorio-performance.md` e `templates/resposta-chat.md`.
2. `quality/reporting-scorecard.md`.
3. `python3 scripts/client_brief.py {slug}`, `python3 scripts/client_history.py list {slug}` e os dossiês relevantes (legados e V2).
4. Trilha de negócio aplicável.

## Processo

1. Confirmar período, comparação, atribuição e status das candidatas/dossiês existentes.
2. Consolidar fatos sem misturar plataformas, atribuições, populações ou denominadores.
3. Gerar uma única representação estruturada e projetá-la primeiro no chat.
4. Apresentar no chat sumário executivo, cobertura, escopo/fontes, KPIs comparativos, evidências, diagnóstico, hipóteses, plano de ação, decisões, mudanças, impacto, riscos, limitações e próximo passo.
5. Com Meta em `connected_read`, usar as referências oficiais da Meta como na etapa `diagnostico/meta` (seção "Referências oficiais da Meta"): cada número importante comparado com a meta do cliente, a linha de base e a referência da Meta, com a origem de cada uma; resposta vazia da ferramenta vira "sem referência da Meta", nunca estimativa.
6. Separar resultado observado de impacto causal. Explicar por que cada resultado está bom ou ruim à luz da base oficial (módulo `revisor`, com `scripts/kb_check.py` para as premissas da explicação) e registrar essas checagens. Relatório é o único tipo em que a checagem pode ser dispensada, e só quando a leitura não depende de nenhum mecanismo de plataforma.
7. Para operações executadas cuja janela de avaliação venceu, propor a avaliação: comparar com os critérios registrados e, com o aval do gestor, registrar com `dossier.py evaluate`.
8. Iterar até existir versão final e pedir aprovação do conteúdo.
9. Depois da aprovação, registrar com `scripts/dossier.py new`, com o mesmo texto.
10. Atualizar a memória do cliente como manda o módulo `contexto-cliente` (seção "Memória do cliente").
11. Gerar proposta de aprendizado sanitizado quando houver padrão reutilizável.

## Saída

- Relatório completo e autossuficiente no chat; o gestor não precisa abrir o dossiê para compreender ou decidir.
- Dossiê criado/atualizado somente após aprovação editorial.
- Ficha do cliente atualizada.
- Proposta sanitizada separada, se aplicável.

Depois do registro, informar numa linha o caminho do dossiê e o próximo passo. Não despejar IDs, JSON, logs ou respostas brutas no chat.

Não confundir aprovação do gestor com melhora medida de performance.
