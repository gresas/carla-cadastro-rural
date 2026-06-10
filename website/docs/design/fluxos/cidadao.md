---
sidebar_position: 1
title: Fluxo do Cidadão
description: Jornada completa do produtor rural — do primeiro acesso à aprovação do CAR.
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

    L --> N[Etapa 3: Geometria\nLeaflet + satélite: toca vértices sobre foto aérea\nou importa KML/SHP]
    N --> NA{Validação de geometria\nem tempo real}
    NA -- Geometria fora do município --> NB[Alerta: 'Sua geometria está fora\ndo município declarado'\nUsuário ajusta]
    NB --> NA
    NA -- Self-intersection detectada --> NC[Alerta: 'Geometria com cruzamento\nde bordas — corrija no mapa'\nUsuário ajusta]
    NC --> NA
    NA -- Área diverge > 5% da declarada --> ND[Alerta: 'Área calculada diverge\nda declarada. Revise.']
    ND --> NA
    NA -- Validações OK --> O[Etapa 4: Revisão\ntodos os dados]
    O --> P[Clica 'Submeter']
    P --> Q[Número de protocolo CAR gerado pelo SICAR\nStatus: Submetido]
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
| `aprovado` | ✅ "Aprovado! Baixe seu Certificado CAR" | Baixar Certificado CAR oficial |
| `aprovado_com_pra` | ✅⚠️ "CAR aprovado — mas sua propriedade precisa de regularização ambiental. Veja os próximos passos." | Acessar orientações sobre o PRA |
| `rejeitado` | ❌ "Rejeitado — veja o motivo" | Opção de recurso |

---

## Pontos de Atenção para Design

:::note Por que satélite, não GPS?
GPS de smartphone tem precisão de 10–30m, o que representa erro inaceitável em propriedades pequenas (1–5 ha). O produtor traça os vértices sobre a imagem aérea da sua própria terra — cercas, estradas e cursos d'água visíveis na foto servem de referência precisa. Leaflet com tile layer de satélite (ex: Esri World Imagery) funciona em mobile via touch nativo.
:::

:::warning Geometria é o maior gargalo real do CAR
A geometria incorreta é a principal causa de retrabalho e rejeição no CAR brasileiro. Validações em tempo real (município, área, self-intersection) reduzem erros antes da submissão. Sobreposição com outras propriedades, TIs e UCs é verificada **assincronamente** — não bloqueia a submissão mas gera alerta para o analista e notificação ao cidadão se confirmada.
:::

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
