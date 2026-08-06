---
name: 23-google-ads-campaign-build-plan
description: Consolida estratégia, arquitetura, targeting, palavras-chave quando aplicável, budget, lances, conversões, anúncios, assets e landing pages em um plano Google Ads aprovável. Use em /criar-campanha para Google Ads antes de qualquer configuração manual.
---

# Plano de Construção Google Ads

## Pré-requisitos

1. Skills `01`, `03`, `04`, `17`, `19`, `20`, `21` e `22` concluídas conforme o escopo.
2. Skill `18` concluída quando houver keywords, search themes ou validação de demanda.
3. Dossiê em `draft` e conta/modo de fonte registrados.

## Processo

1. Consolidar parâmetros no modelo estrutural correto do tipo de campanha.
2. Marcar campos confirmados, hipóteses, indisponíveis e dependentes de interface.
3. Verificar compatibilidade entre tipo, rede, budget, lance, conversões, targeting, ads/assets, feed e destino.
4. Definir status inicial seguro e checklist de publicação manual.
5. Gerar change set versionado com itens Google Ads marcados `manual_only` enquanto `write_tools_registered` for falso.
6. Atualizar dossiê para `proposed` somente quando houver mutação proposta; planejamento puro termina `analysis_only`.

## Gate

Não chamar ferramenta de escrita. A presença do namespace complementar não é autorização operacional. Plano completo não é aprovação. Campo ausente fica `blocked`; configuração cuja disponibilidade não foi validada exige instrução para conferência manual.

## Saída

Resumo executivo, mapa hierárquico, tabela de configuração, checklist, change set manual, impacto financeiro, riscos e critério da primeira leitura.
