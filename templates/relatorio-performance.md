# Relatório de performance

Contrato do relatório no chat. Segue `templates/resposta-chat.md` (explicativo, com todo número interpretado, tabelas de até 5 colunas e sem códigos internos) e acrescenta o que é próprio de um fechamento de período. O dossiê só nasce depois da aprovação do conteúdo, por `scripts/dossier.py`.

## Estrutura

1. **Cabeçalho:** cliente · plataformas · período (comparado com) · fonte dos dados · confiança.
2. **Resumo do período:** o resultado de negócio, o que melhorou, o que piorou e a decisão principal, em até 6 frases.
3. **Resultado de negócio:** leads válidos, oportunidades, vendas e receita quando existirem. Em lead generation, custo por lead sozinho não prova qualidade; em e-commerce, ROAS não é lucro.
4. **Os números por plataforma:** uma tabela por plataforma (Meta Ads, Google Ads e comercial separados), seguida de "Como ler esses números". Atribuições diferentes não são somadas.
5. **O que foi bem e o que foi mal, e por quê:** para cada ponto, o número, a comparação e a explicação. Conferir as explicações de mecanismo na base oficial (módulo `revisor`, com `scripts/kb_check.py`) e citar a fonte.
6. **O que fizemos no período:** operações executadas, com a situação de cada uma e o resultado da avaliação quando a janela já venceu (`scripts/client_history.py list {slug}`).
7. **Avaliações pendentes:** operações cuja janela de avaliação venceu, com a proposta de avaliação.
8. **Próximas decisões:** o que o gestor precisa decidir, com opções e recomendação.
9. **Limitações:** dados indisponíveis, por que importam e como conseguir.

## Regras

- Separar Meta Ads, Google Ads e comercial antes de qualquer síntese.
- Ausência de dado não é zero.
- Janelas comparáveis e atribuição declarada.
- Resultado observado não é impacto causal: diga quando é só correlação.
- Aprendizado reutilizável vira proposta sanitizada, sem nomes, IDs ou valores, e só entra na base com aprovação de Davi.
