# Checklist de Qualidade de Mensuração

## Identidade e escopo

- Conta, pixel/dataset, domínio e timezone corretos.
- Evento e valor com definição conhecida.
- Janela e atribuição registradas.

## Coleta

- Browser/Pixel presente quando aplicável.
- Server/CAPI presente quando aplicável.
- Event ID/deduplicação verificáveis.
- Qualidade de correspondência e diagnósticos consultados quando acessíveis.
- UTMs consistentes e preservadas.

## Reconciliação

- Mesma janela e timezone.
- Mesma definição de lead/receita.
- Duplicados, inválidos, cancelamentos e reembolsos tratados.
- Atraso do CRM/ciclo considerado.
- Escopo de campanha versus total distinguido.

## Gate

- `confiavel`: sustenta a decisão declarada.
- `utilizavel_com_ressalvas`: sustenta somente parte da leitura.
- `insuficiente`: bloquear mudança dependente e priorizar correção.

O gate é relativo à decisão: dados podem ser suficientes para entrega e insuficientes para lucratividade.

