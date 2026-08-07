---
title: "Sobre os status da estratégia de lances"
url: "https://support.google.com/google-ads/answer/6263057?hl=pt-BR"
answer_id: "6263057"
categoria: "03-otimizacao-desempenho"
topico: "Orçamento e lances"
subtopico: "Lances"
fonte: "Central de Ajuda do Google Ads"
idioma: "pt-BR"
extraido_em: "2026-08-07"
traducao_por_ia: "possivel"
formato: "sintese-estruturada"
---

# Sobre os status da estratégia de lances

O status da estratégia de lances indica o estado da estratégia de lances automáticos em um determinado momento. Verificar esse status ao acompanhar a performance da campanha ajuda a identificar e resolver problemas.

Observação: os status da estratégia de lances não estão disponíveis para campanhas de hotel.

## Onde encontrar o status da estratégia de lances

1. Acesse "Estratégias de lances" no menu Ferramentas.
2. A coluna "Status" mostra o status da estratégia de lances de portfólio.
3. Passe o cursor sobre o texto para ver detalhes do status.
4. A coluna "Tipo de estratégia de lances" mostra a opção selecionada para cada campanha, mesmo quando não é uma estratégia de portfólio. Se essa coluna não aparecer, é preciso ativá-la clicando no ícone de colunas acima da tabela, em "Modificar colunas", categoria "Atributos".

## Status possíveis

### Inativa

A estratégia de lances não está ativa. Motivos possíveis:

- As campanhas estão pausadas ou não há campanhas associadas à estratégia.
- Todas as palavras-chave ou anúncios que usam essa estratégia estão pausados.
- Um orçamento pré-pago foi totalmente gasto.

### Ativa

A estratégia de lances está ativa e definindo lances para otimizar o desempenho. Nenhuma mudança é necessária.

### Aprendizado

Após uma mudança na estratégia de lances, pode haver pequenas variações de performance enquanto o Google Ads otimiza os lances. O cursor sobre o status revela qual dos quatro motivos originou o status "Aprendizado":

- **Nova estratégia:** a estratégia foi criada ou reativada recentemente.
- **Alteração na configuração:** uma configuração da estratégia foi modificada.
- **Alteração na composição:** campanhas, grupos de anúncios ou palavras-chave foram adicionados ou removidos da estratégia.

Próxima etapa: continuar usando a conta normalmente, sem avaliar o desempenho até o fim do período de aprendizado, já que as principais métricas podem variar nesse intervalo.

### Limitada

A estratégia de lances é limitada por um dos quatro fatores a seguir (visível ao passar o cursor sobre o status):

- **Inventário:** a estratégia é limitada pelo volume de pesquisas disponível — os anúncios só estão qualificados para um número restrito de leilões. Próxima etapa sugerida: considerar anúncios dinâmicos de pesquisa.
- **Limites de lance:** limites de lance máximo e/ou mínimo impedem a otimização total dos lances (exemplo citado: 95% dos gastos restritos pelo limite de lance máximo).
- **Limitada pelo orçamento:** muitas palavras-chave da estratégia estão limitadas pelo orçamento, impedindo que o Google Ads aumente os lances. Próxima etapa sugerida: otimizar o orçamento diário médio.
- **Estratégia de lances** (aplicável apenas no nível de campanha): a estratégia está limitada no momento; considerar lances mais eficientes ou upgrade para outra estratégia.

### Configuração incorreta (estratégia de lances "Maximizar" com orçamento compartilhado)

As estratégias Maximizar Cliques, Maximizar Conversões e Maximizar o Valor da Conversão otimizam desempenho (cliques, conversões, valor de conversão) sem ultrapassar o orçamento diário médio. Se compartilharem orçamento com outra estratégia de lances, o status pode aparecer como "Configuração incorreta". Para evitar isso, todas as campanhas com o mesmo orçamento compartilhado devem usar a mesma estratégia de lances de portfólio.

**Se a estratégia de lances padrão (nível de campanha) estiver configurada incorretamente:**

1. Acesse "Campanhas" no menu.
2. Acesse o Relatório de estratégia de lances.
3. Selecione "Corrigir" — isso filtra todas as campanhas do orçamento compartilhado na tabela "Campanhas".
4. Marque a caixa no topo da coluna "Campanha" para selecioná-las todas.
5. Selecione "Editar" e "Mudar estratégia de lances".
6. No menu suspenso, adicione as campanhas a uma única estratégia de portfólio (Maximizar cliques, Maximizar conversões ou Maximizar o valor da conversão).
7. Selecione "Usar uma estratégia de portfólio" e "Criar nova estratégia de portfólio", definindo nome e opções.
8. Selecione "Aplicar".

Observação: uma estratégia de portfólio pode conter vários orçamentos compartilhados, mas todas as campanhas de cada orçamento compartilhado precisam usar a mesma estratégia de portfólio. Alternativamente, é possível remover um orçamento compartilhado.

**Se a estratégia de lances de portfólio estiver configurada incorretamente**, o processo é semelhante: acessar Campanhas → Relatório de estratégia de lances → "Corrigir" → selecionar todas as campanhas filtradas → Editar → Mudar estratégia de lances → escolher "Usar estratégia de portfólio existente" e selecionar a estratégia original marcada como correta → Aplicar. Também é possível excluir o orçamento compartilhado da campanha.

### Configuração incorreta (configuração de conversão)

Estratégias automáticas baseadas em conversão (CPA desejado, ROAS desejado, Maximizar Conversões) usam o histórico de conversões para definir lances com precisão em cada leilão. Configurações incorretas das ações de conversão podem limitar a precisão dos lances e as conversões geradas.

Observação: em contas com acompanhamento de conversões de várias contas, esses problemas precisam ser resolvidos na conta de administrador do Google Ads.

Motivos e correções:

- **Não há ações de conversão de instalação do aplicativo:** configurar o acompanhamento de conversões para Android ou iOS; verificar se a ação de conversão está ativada (ponto verde = ativa, X vermelho = removida — reativar via "Editar" > "Ativar" em Metas); verificar se "Incluir em 'Conversões'" está marcado como "Sim".
- **Não há ações de conversão de chamada telefônica:** configurar o acompanhamento de chamadas a partir de anúncios; mesmas verificações de status e de "Incluir em 'Conversões'".
- **Não há ações de conversão no site:** configurar o acompanhamento de conversões no site; mesmas verificações de status e de "Incluir em 'Conversões'".

## Links relacionados

- [Sobre lances automáticos](https://support.google.com/google-ads/answer/2979071)
- [Criar uma estratégia de lances de portfólio](https://support.google.com/google-ads/answer/6263058)
- [Sobre o período de aprendizado das campanhas e o que o afeta](https://support.google.com/google-ads/answer/13020501)
- [Sobre a estratégia de lances Maximizar Cliques](https://support.google.com/google-ads/answer/6268626)
- [Sobre a estratégia de lances Maximizar Conversões](https://support.google.com/google-ads/answer/7381968)
- [Sobre a estratégia de lances Maximizar o Valor da Conversão](https://support.google.com/google-ads/answer/7684216)
- [Relatório de estratégia de lances](https://support.google.com/google-ads/answer/7074568)
