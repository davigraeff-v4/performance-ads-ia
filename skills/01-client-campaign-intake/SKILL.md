---
name: 01-client-campaign-intake
description: Estrutura cliente, conta e campanha a partir de briefing, conversa ou arquivos. Use em /novo-cliente, novo planejamento, nova campanha ou quando faltarem objetivo, oferta, modelo de negócio, metas, restrições e fontes.
---

# Intake de Cliente e Campanha

## Dados necessários

1. `templates/cliente-template.md` e `templates/briefing-campanha.md`.
2. `clients/{slug}/CLIENTE.md`, se existir.
3. Briefing, planilhas e observações fornecidas.

## Processo

1. Normalizar nome e slug sem misturar clientes homônimos.
2. Extrair: modelo (`lead_generation` ou `ecommerce`), conta esperada, oferta, objetivo comercial, funil, geografia, budget, prazo, ciclo de venda, margem, metas, restrições, ativos e fontes externas.
3. Separar valores confirmados, hipóteses e campos ausentes.
4. Perguntar em uma única rodada apenas pelos críticos: cliente, modelo, objetivo, oferta, conta/escopo, budget ou limite, restrições e definição do resultado.
5. Criar/atualizar `CLIENTE.md` sem apagar histórico.
6. Iniciar dossiê da demanda.

## Saída

Apresentar um resumo compacto:

```text
Cliente e modelo:
Objetivo de negócio:
Oferta e funil:
Conta/escopo esperado:
Meta e baseline conhecidos:
Budget e prazo:
Fontes disponíveis:
Restrições:
Lacunas críticas:
Hipóteses permitidas:
```

## Validação

- Não preencher ausência com zero.
- Não inferir permissão, conta, meta ou restrição.
- Não registrar dados pessoais desnecessários.
- Registrar origem e data de qualquer meta.

