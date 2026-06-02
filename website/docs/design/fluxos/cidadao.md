---
sidebar_position: 1
title: Fluxo do Cidadão
description: Jornada completa do produtor rural e do consultor — do primeiro acesso à aprovação do CAR.
tags: [design, ux, fluxo, cidadão]
---

# Fluxo do Cidadão

:::info Para quem é esta página
Designers e front-end engineers. Para os casos de uso formais, veja [UC-001 a UC-009](../../produto/casos-de-uso.md).
:::

## Fluxo Feliz — Registro CAR Completo

```mermaid
flowchart TD
    A([Cidadão acessa CARla]) --> B{Autenticado?}
    B -- Não --> C[Clica 'Entrar com Gov.br']
    C --> D[Redireciona para Gov.br]
    D --> E[Login com CPF + senha]
    E --> F[Retorna ao CARla autenticado]
    B -- Sim --> G
    F --> G[Dashboard — Meus Processos]

    G --> H[Clica 'Novo Processo']
    H --> I[Etapa 1: Dados do Imóvel\nnome, município, área]
    I --> J[Etapa 2: Upload de Documentos\nmatrícula, CCIR]
    J --> K{OCR automático}
    K -- Válido --> L[Documento marcado ✓]
    K -- Inválido --> M[Pendência automática\ncom instrução de correção]
    M --> J

    L --> N[Etapa 3: Geometria\nshapefile ou desenho manual]
    N --> O[Etapa 4: Revisão\ntodos os dados]
    O --> P[Clica 'Submeter']
    P --> Q[Protocolo gerado\nStatus: Submetido]
    Q --> R[Notificação: e-mail + WhatsApp]
    R --> S([Aguarda análise])
```

---

## Fluxo de Pendência e Correção

```mermaid
sequenceDiagram
    participant C as Cidadão
    participant P as Portal CARla
    participant A as Analista
    participant W as WhatsApp

    A->>P: Cria pendência com descrição
    P->>W: Envia notificação WhatsApp
    P->>C: Envia e-mail com link direto
    C->>W: Recebe mensagem
    C->>P: Acessa pendência pelo link
    C->>P: Pergunta ao assistente IA
    P->>C: Assistente explica o que falta
    C->>P: Faz upload do documento correto
    P->>P: Revalida automaticamente
    P->>A: Notifica: pendência resolvida
    A->>P: Retoma análise
```

---

## Estados do Processo

| Status | O que o cidadão vê | Próxima ação |
|---|---|---|
| `rascunho` | "Em preenchimento" | Continuar preenchendo |
| `submetido` | "Enviado — aguardando analista" | Aguardar |
| `em_analise` | "Em análise" | Aguardar |
| `pendente` | ⚠️ "Pendência — ação necessária" | Responder pendência |
| `aprovado` | ✅ "Aprovado! Baixe seu comprovante" | Baixar certificado CAR |
| `rejeitado` | ❌ "Rejeitado — veja o motivo" | Opção de recurso |

---

## Pontos de Atenção para Design

:::warning Upload em conexão ruim
João pode ter 3G instável. O upload deve:
- Mostrar progresso incremental
- Suportar retomada em caso de falha
- Limitar tamanho a 50MB com mensagem clara antes do envio
:::

:::tip Stepper sempre visível
Em mobile, o stepper deve permanecer fixo no topo durante o preenchimento — o cidadão precisa saber em qual das 4 etapas está a qualquer momento.
:::

## Ver também

- [Fluxo do Analista](./analista.md) — o que acontece depois da submissão
- [Fluxo WhatsApp](./whatsapp.md) — jornada pelo canal WhatsApp
- [Princípios UX](../principios.md) — diretrizes de linguagem e acessibilidade
