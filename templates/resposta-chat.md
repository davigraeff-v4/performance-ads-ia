# Formato de resposta no chat

Este é o contrato de forma de toda entrega no chat. O corpo do dossiê é exatamente o mesmo texto aprovado no chat, então este formato também vale para ele.

**Princípio:** o gestor quer o máximo de explicação, de forma visual e organizada, para decidir sem dúvida. Números sempre vêm acompanhados de leitura: o que são, como foram calculados, com o que se comparam e o que significam para o negócio. Nunca um amontoado de números, códigos internos ou texto técnico.

## Estrutura padrão (análise, otimização, auditoria, relatório, criação)

1. **Cabeçalho**, uma linha em negrito: cliente · plataforma · o que foi analisado · período (e com o que foi comparado) · de onde vieram os dados · confiança em palavras.
2. **Resumo:** 3 a 6 frases diretas. O que aconteceu, por que acreditamos que aconteceu e o que proponho.
3. **Os números:** tabela com no máximo 5 colunas, seguida sempre de **Como ler esses números**, com um item para cada número que importa:
   - o que a métrica é (por extenso na primeira vez: "custo por lead (CPL)");
   - a conta com os valores reais na primeira vez ("R$ 323,83 ÷ 4 leads = R$ 80,96");
   - a comparação (período anterior, outro conjunto, meta ou referência) com seta e sinal: ▲ +12,4% / ▼ −8,1%; quando houver, até três referências com a origem de cada uma: a meta do cliente, a linha de base (período anterior equivalente) e a referência da plataforma (ex.: "a Meta classifica abaixo da média de anunciantes parecidos"). Plataforma sem referência para a conta: diga isso, não estime;
   - se isso é bom ou ruim para o negócio, e por quê;
   - quando o volume for pequeno, dizer isso e o quanto a conclusão pode mudar.
4. **O que está acontecendo:** um bloco por achado, com título em linguagem de negócio (`### 1. Os dois remarketings miram o mesmo público`):
   - **O que vimos:** fatos com números;
   - **Por que acreditamos que acontece:** explicação principal;
   - **Outra explicação possível:** alternativa, e o que vai diferenciar uma da outra;
   - **Confiança:** alta, média ou baixa, e o motivo (volume, janela, qualidade do rastreamento).
5. **O que proponho:** um bloco por mudança (`### Mudança 1 — Pausar o conjunto “Remarketing 60 dias”`):
   - **Onde:** plataforma, nível e nome como aparece na conta;
   - **Antes → depois:** o valor atual e o novo;
   - **Por quê:** a ligação com o achado, pelo nome do achado;
   - **Resultado esperado:** o que deve melhorar, e em quanto tempo;
   - **Efeito no orçamento:** diferença por dia, e o efeito líquido no fim da lista;
   - **Risco e como desfazer:** sempre com pausa, nunca com exclusão;
   - **Como será feito:** pelo conector depois da sua aprovação, ou manualmente por você no gerenciador.
6. **Checagem com boas práticas:** para cada premissa importante do diagnóstico ou das mudanças:
   - ✅ quando a documentação oficial sustenta;
   - ⚠️ quando contradiz, dizendo o que mudou no plano por causa disso;
   - ❔ quando não há cobertura oficial.

   Sempre com o nome do artigo e o link.
7. **Como vamos saber se funcionou:** a partir de quando avaliar, o sinal de sucesso (com número) e o sinal de parada.
8. **O que preciso de você:** lista de decisões, com as opções e a sua recomendação.
9. **Próximo passo:** uma frase. Por exemplo: "Se estiver de acordo, responda *pode registrar* e eu salvo o dossiê."

Numa auditoria completa, acrescente antes do próximo passo **O que foi analisado e o que ficou de fora**, em linguagem simples: cada parte da conta, se foi analisada e, se não foi, por quê.

## Regras de forma

- **Tabelas:** até 5 colunas, cabeçalhos em português por extenso e uma linha de total quando fizer sentido. Mais colunas? Divida em duas tabelas.
- **Números no padrão brasileiro:** R$ 1.234,56 · 12,5% · 2,7 vezes · 04/09/2026.
- **Siglas de mídia** (CPL, CPA, CPM, CTR, ROAS): por extenso na primeira vez em cada resposta.
- **Nomes** de campanhas, conjuntos e anúncios entre aspas, como aparecem na conta. ID numérico só quando ajudar a encontrar o item, entre parênteses.
- **Fato, cálculo e hipótese** se distinguem com palavras: "vimos que…" (fato), "calculamos…" (cálculo), "acreditamos que…" (hipótese), "recomendo…" (recomendação), "não temos esse dado porque…" (indisponível).
- **Indicadores visuais** permitidos com moderação e sempre acompanhados de texto: ✅ ⚠️ ❌ ❔ ▲ ▼.
- **Dado indisponível:** diga o que falta, por que importa e como conseguir. Nunca preencha com zero.

## Nunca no chat

- Códigos internos: `evd-…`, `fnd-…`, `act-…`, `chg-…`, `diag-…`, `op-…`, e abreviações próprias como "F1", "C2" ou "CS-03". Use "Achado 1", "Mudança 2".
- Hashes, nomes ou números de skills, rotas, JSON, GAQL, caminhos de arquivo, logs e respostas brutas de ferramentas.
- Tabelas com mais de 5 colunas ou matrizes técnicas de cobertura.

Duas exceções: o comando que o gestor precisa digitar no próximo passo (ex.: `/aprovar-operacao`) e o caminho do dossiê, numa única linha, depois de salvo.

## Variantes curtas

- **Dúvida:** resposta direta → explicação → o que a documentação oficial diz (com link) → como isso se aplica na prática ou à conta → cuidados.
- **Consulta rápida:** o número pedido em destaque → comparação curta → uma frase de leitura. Não gera dossiê.
- **Histórico do cliente:** o que já foi feito (data, o quê, situação), com as pendências e avaliações vencendo em destaque.
- **Ajuste pontual:** o que muda (antes → depois), risco e como desfazer, checagem rápida de boas práticas e pedido de registro.
- **Avaliação de operação:** cabeçalho (operação, data da execução, janela avaliada contra a linha de base) → veredito em uma frase (funcionou, não funcionou ou ainda não dá para dizer) → tabela "Critério · Combinado · Resultado · Situação" (✅ ⚠️ ❌ ❔) → por que deu esse resultado, separando o efeito da mudança de outras causas → o que a base oficial explica → o que fazer agora (manter, ajustar ou reverter com pausa) → pedido de aval para registrar a avaliação.

Exemplo completo: `examples/synthetic/v2/otimizacao-remarketing.body.md`.
