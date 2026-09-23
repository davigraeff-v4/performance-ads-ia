# Corpo do dossiê (V2)

Este é o molde do **corpo** que o agent escreve em `.work/` depois da aprovação do conteúdo. O corpo é o mesmo texto aprovado no chat, no formato de `templates/resposta-chat.md`. Quem monta o dossiê final (título, situação, mudanças, andamento e dados técnicos) é o `scripts/dossier.py`. Nunca crie o arquivo do dossiê à mão.

Regras do corpo:

- nada de bloco JSON, IDs internos, hashes ou nomes de skills: o registro de máquina vai no spec;
- onde as mudanças aparecem no chat, deixe só o marcador `<!-- mudancas -->`: o script renderiza cada mudança a partir do spec, com os mesmos dados que serão aprovados e executados;
- em análise sem mudança, não use o marcador.

Exemplo completo: `examples/synthetic/v2/otimizacao-remarketing.body.md` (corpo) e `examples/synthetic/v2/otimizacao-remarketing.spec.json` (spec).

---

**{Cliente}** · {Plataforma} · {o que foi analisado} · {período} (comparado com {período anterior}) · {fonte dos dados} · confiança {alta|média|baixa}

## Resumo

{3 a 6 frases: o que aconteceu, por que acreditamos que aconteceu, o que proponho.}

## Os números

| {Recorte} | {Métrica} | {Métrica} | {Métrica} | {Comparação} |
|---|---:|---:|---:|---:|

**Como ler esses números**

- **{Métrica por extenso (sigla)}:** o que é, a conta com os valores reais, a comparação com ▲/▼ e o que isso significa para o negócio.
- **Atenção ao volume:** {quando a amostra for pequena}.

## O que está acontecendo

### 1. {Achado em linguagem de negócio}

- **O que vimos:** {fatos com números}
- **Por que acreditamos que acontece:** {explicação principal}
- **Outra explicação possível:** {alternativa e o que vai diferenciar}
- **Confiança:** {alta|média|baixa}, porque {motivo}

## O que proponho

<!-- mudancas -->

## Checagem com boas práticas

- ✅ **{premissa}:** {o que a fonte oficial diz}. [{título do artigo}]({url})
- ⚠️ **{premissa contradita}:** {o que a fonte diz e o que mudou no plano}. [{título}]({url})
- ❔ **{premissa sem cobertura}:** {como vamos acompanhar}.

## Como vamos saber se funcionou

- **Quando avaliar:** a partir de {data}.
- **Funcionou se:** {critério com número}.
- **Parar ou rever se:** {critério com número}.

## O que preciso de você

- [ ] {decisão, com opções e a sua recomendação}
