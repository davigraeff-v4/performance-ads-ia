---
name: 01-client-campaign-intake
description: Estrutura cliente, plataformas, contas e campanha a partir de briefing, conversa ou arquivos. Use em /novo-cliente, novo planejamento Meta/Google Ads ou quando faltarem objetivo, oferta, modelo de negócio, metas, restrições e fontes.
---

# Intake de Cliente e Campanha

## Dados necessários

1. `templates/cliente-template.md` e `templates/briefing-campanha.md`.
2. `clients/{slug}/CLIENTE.md`, se existir.
3. Briefing, planilhas e observações fornecidas.

## Processo

1. Normalizar nome e slug sem misturar clientes homônimos.
2. Extrair: modelo (`lead_generation` ou `ecommerce`), plataformas solicitadas, contas esperadas, modo de fonte por plataforma, oferta, objetivo comercial, funil, geografia, budget, prazo, ciclo de venda, margem, metas, restrições, ativos e fontes externas.
3. Separar valores confirmados, hipóteses e campos ausentes.
4. Perguntar em uma única rodada apenas pelos críticos: cliente, modelo, objetivo, oferta, plataforma, conta/escopo quando houver, budget ou limite, restrições e definição do resultado.
5. Criar/atualizar `CLIENTE.md` sem apagar histórico.
6. Iniciar a representação candidata em memória. Não criar dossiê antes de apresentar o conteúdo no chat e obter aprovação do conteúdo; o registro é sempre por `scripts/dossier.py`.

## Saída

Apresentar um resumo compacto:

```text
Cliente e modelo:
Objetivo de negócio:
Oferta e funil:
Plataformas, contas e modos de fonte:
Meta e baseline conhecidos:
Budget e prazo:
Fontes disponíveis:
Restrições:
Lacunas críticas:
Hipóteses permitidas:
```

## Histórico do cliente (intenção `historico` e consulta antes de agir)

1. `python3 scripts/client_history.py list {slug} --limit 10` para a linha do tempo, com legados e V2; `--open` só para o que está sem fechamento.
2. `python3 scripts/client_history.py search {slug} "termos"` para achar o que já foi analisado ou decidido sobre um tema; abrir o dossiê inteiro só quando o trecho for relevante.
3. Dossiês legados são somente leitura. Nunca editar; operação legada aberta que precise seguir adiante é migrada pelo `dossier.py migrate`.
4. Responder no chat: o que foi feito (data, o quê, situação), o que ficou pendente e o que vale revisar agora. Nunca cruzar clientes.

## Validação

- Não preencher ausência com zero.
- Não inferir permissão, conta, meta ou restrição.
- Não registrar dados pessoais desnecessários.
- Registrar origem e data de qualquer meta.
