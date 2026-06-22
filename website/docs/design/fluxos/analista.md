---
sidebar_position: 2
title: Fluxo do Analista
description: Jornada do analista ambiental — da fila de processos à decisão usando a terminologia oficial do SICAR.
tags: [design, ux, fluxo, analista]
---

# Fluxo do Analista

:::info Para quem é esta página
Designers e front-end engineers. Para os casos de uso formais, veja [UC-005 a UC-008](../../produto/casos-de-uso.md).
:::

## Fluxo de Análise e Decisão

```mermaid
flowchart TD
    A([Analista acessa portal]) --> B[Fila de Processos\nordenada por prioridade + risco]
    B --> C{Filtrar fila}
    C --> D[Seleciona processo]
    D --> E[Dossiê gerado automaticamente\npelo assistente IA]

    E --> F{Análise do dossiê}
    F --> G[Verificar documentos\nvalidados automaticamente]
    G --> H[Consultar mapa\ngeometria do imóvel]
    H --> I{Decisão}

    I -- Regular --> J["Encaminha como Regular\nobservações obrigatórias"]
    J --> K["Status: Regular\nRecibo de Inscrição disponível\nNotificação ao cidadão na Carla + email"]

    I -- Pendência --> L["Cria pendência de Regularização\ncom motivo + prazo"]
    L --> M["Status: Pendente de Regularização\nNotificação ao cidadão na Carla + email\naba Regularização Ambiental liberada"]
    M --> N[Aguarda resposta do cidadão]
    N --> F
```

---

:::warning Recibo de Inscrição do Imóvel Rural no CAR
Ao encaminhar um cadastro como Regular, o sistema disponibiliza o **Recibo de Inscrição do Imóvel Rural no CAR** — comprovante oficial gerado pelo SICAR. Este é o documento com validade jurídica para transações rurais (crédito, comercialização). O comprovante interno do CARla complementa, mas não substitui o Recibo de Inscrição.
:::

:::caution Decisão — responsabilidade do servidor
O dossiê gerado por IA é **apoio à decisão**, não substituto. Atos administrativos precisam ter **motivação própria do servidor** para ter validade jurídica. O campo de observações deve ser preenchido pelo analista — mesmo que brevemente. A IA resume; o analista decide e fundamenta.
:::

---

## O que o Analista vê na Fila

Cada processo na fila exibe:

| Campo | O que significa |
|---|---|
| **Status SICAR** | `Em Andamento`, `Em Análise`, `Pendente de Regularização`, `Regular` |
| **Score de completude** | 0–100% — quanto dos dados está preenchido e validado |
| **Score de risco** | 0–10 — baseado em alertas IBAMA/DETER |
| **Tempo na fila** | Quanto tempo desde o envio |
| **Município / Estado** | Para filtros regionais |
| **Tipo do imóvel** | Minifúndio, pequena, média, grande |

:::tip Ordenação padrão
A fila é ordenada por: (1) prioridade urgente primeiro, (2) maior score de risco, (3) mais tempo na fila. O analista pode reordenar por qualquer coluna.
:::

:::note Score de risco e isonomia
Qualquer critério de priorização algorítmica em serviço público precisa de **fundamentação legal explícita** (portaria, instrução normativa do órgão) para não ser questionado por CGU/TCU ou em ação judicial por isonomia. O score de risco é ferramenta de apoio ao analista — não deve ser o único critério de ordenação sem respaldo normativo.
:::

---

## O Dossiê Automático

Ao assumir um processo, a Carla gera um dossiê em PDF com:

1. **Resumo executivo** — gerado por IA em linguagem técnica
2. **Dados do requerente** — nome, CPF (mascarado), contato
3. **Dados do imóvel** — área, município, bioma, tipo
4. **Análise documental** — status de cada documento com campos extraídos
5. **Mapa** — geometria do imóvel com camadas de APP e Reserva Legal
6. **Alertas externos** — IBAMA, DETER (quando disponível)
7. **Pendências anteriores** — histórico de interações

:::note Tempo de geração
O dossiê leva até 30 segundos para ser gerado. O analista pode começar a revisar os dados enquanto ele é montado.
:::

---

## Criar Pendência de Regularização — Padrões de UX

Para criar pendência de forma eficiente:

- **Templates pré-definidos** por tipo de problema (documentação faltante, geometria inválida, área divergente)
- **Campo de descrição livre** para detalhar além do template
- **Sugestão de prazo** baseada no tipo de pendência (padrão: 15 dias)
- **Preview** da mensagem que o cidadão vai receber na Carla antes de confirmar

Ao confirmar a pendência:
- Status muda para `Pendente de Regularização`
- Cidadão recebe notificação na Carla (Cenário D — destaque imediato) + email
- Aba **Regularização Ambiental** é liberada no Demonstrativo da Situação do CAR

:::warning Clareza na mensagem ao cidadão
O texto da pendência vai direto para o chat da Carla do cidadão. Evite termos técnicos e linguagem de servidor. Use o [guia de linguagem](../principios.md#linguagem-e-tom). O cidadão precisa entender exatamente o que fazer.
:::

---

## Comunicação com o Cidadão

O analista pode enviar mensagens diretamente pelo processo — o cidadão as recebe na Carla como mensagens do analista. Quando há mensagens não lidas com retorno necessário, a Carla prioriza e exibe o Cenário D na próxima abertura do cidadão.

---

## Ver também

- [Fluxo do Cidadão](./cidadao.md) — o que acontece do lado de quem submete
- [Sequência de Mensagens](./mensagens-simuladas.md) — mensagens de notificação de pendência que o cidadão recebe
- [API do Analista](../../apis/analista.md) — endpoints de encaminhamento e pendência
- [Segurança & RBAC](../../seguranca/autenticacao.md) — permissões do analista
