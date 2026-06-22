---
sidebar_position: 1
title: Fluxo do Cidadão
description: Jornada completa do produtor rural — da abertura no car.gov.br às 6 etapas do CAR até o status Regular.
tags: [design, ux, fluxo, cidadão]
---

# Fluxo do Cidadão

:::info Para quem é esta página
Designers e front-end engineers. Para os casos de uso formais, veja [UC-001 a UC-012](../../produto/casos-de-uso.md). Para os scripts de conversa, veja [Sequência de Mensagens](./mensagens-simuladas.md).
:::

## Fluxo de Abertura e Identificação

```mermaid
flowchart TD
    A([Cidadão acessa car.gov.br]) --> B["Banner: 'Fale com a Carla'"]
    B --> C[Nova aba — interface de chat]
    C --> D{Autenticado com Gov.br?}

    D -- Não --> E["Cenário A\nCarla se apresenta\nbotão 'Entrar com Gov.br'"]
    E --> F[Login com CPF + senha Gov.br]
    F --> G[Retorna à Carla autenticado]

    D -- Sim --> G
    G --> H{CAR em andamento\nou mensagem do analista?}
    H -- Mensagem não lida --> I["Cenário D\nDestaque de mensagem urgente"]
    H -- CAR em andamento --> J["Cenário C\nRetomada de cadastro"]
    H -- Sem processos --> K["Cenário B\nOferta de iniciar CAR"]

    K --> L[Usuário clica 'Iniciar meu CAR']
    L --> M[Início do fluxo de criação\n6 etapas guiadas pela Carla]
```

---

## Fluxo de Criação do CAR — 6 Etapas

```mermaid
flowchart TD
    M([Início do CAR]) --> E1

    E1["Etapa 1 — Cadastrante\nCPF, nascimento, nome, nome da mãe\nRepresentante legal"]
    E1 --> E1C[Confirmação em bloco\nCarla não repete dados já coletados]
    E1C --> E2

    E2["Etapa 2 — Imóvel\nNome, município, CEP, zona\nAcesso, correspondência"]
    E2 --> E2C[Confirmação em bloco]
    E2C --> E3

    E3["Etapa 3 — Domínio\nProprietário / possuidor\nPessoa Física ou Jurídica\nDocumento comprobatório"]
    E3 --> E3R{Mais proprietários?}
    E3R -- Sim --> E3
    E3R -- Não --> E3C[Confirmação em bloco]
    E3C --> E4

    E4["Etapa 4 — Documentação\nPropriedade ou Posse\nMatrícula, CCIR, SNCR, NIRF\nReserva Legal averbada\nUpload de imagens"]
    E4 --> E4V{Validação automática\nOCR}
    E4V -- Consistente --> E4C[Confirmação em bloco]
    E4V -- Inconsistente --> E4X[Carla indica divergência\ne orienta correção]
    E4X --> E4
    E4C --> E5

    E5["Etapa 5 — Geo\nDemarcação de polígonos sugerida\nbaseada em área + município declarados\nUsuário ajusta e confirma\n(não desenha do zero)"]
    E5 --> E5V{Validações em tempo real}
    E5V -- Fora do município --> E5A[Alerta de área divergente\nUsuário ajusta]
    E5V -- Self-intersection --> E5B[Alerta de cruzamento\nUsuário corrige]
    E5V -- OK --> E5C[Confirmação da demarcação]
    E5A --> E5V
    E5B --> E5V
    E5C --> E6

    E6["Etapa 6 — Informações (PRA)\n12 perguntas sobre situação ambiental\nPRA, TAC, PRAD, RPPN, CRF, multas\nCarla pré-marca campos com dados já conhecidos"]
    E6 --> FINAL

    FINAL["Resumo geral de todas as etapas\nBotão 'Finalizar cadastro'"]
    FINAL --> OK["Status: Cadastrado\nRecibo de Inscrição gerado\nCarla avisa quando analista responder"]
```

---

## Fluxo de Pendência e Correção

```mermaid
sequenceDiagram
    participant C as Cidadão
    participant K as Carla (chat web)
    participant A as Analista

    A->>K: Cria pendência com descrição e prazo
    K->>C: Notificação na Carla (Cenário D) + email
    C->>K: Acessa a Carla — vê destaque "Tenho uma novidade importante"
    C->>K: Lê mensagem do analista
    C->>K: Pergunta à Carla o que precisa corrigir
    K->>C: Explica em linguagem simples e orienta a correção
    C->>K: Envia documento ou corrige dado
    K->>K: Revalida automaticamente
    K->>A: Notifica: correção submetida
    A->>K: Retoma análise
```

---

## Status do CAR — Terminologia Oficial do SICAR

| Status SICAR | O que o cidadão vê na Carla | Próxima ação |
|---|---|---|
| `Em Andamento` | "Cadastro em andamento — etapa \{etapa_atual\}" | Continuar preenchendo |
| `Cadastrado` | "Cadastro preenchido — pronto para envio" | Confirmar envio |
| `Gravado/Enviado` | "Cadastro enviado ao SICAR" | Aguardar processamento |
| `Em Análise` | "Em análise pelo analista ambiental" | Aguardar |
| `Pendente de Regularização` | ⚠️ "Pendência — você tem uma mensagem do analista" | Responder à mensagem |
| `Regular` | ✅ "CAR Regular! Recibo de Inscrição disponível" | Baixar Recibo de Inscrição |

:::note Demonstrativo da Situação do CAR
Quando o status é `Pendente de Regularização`, a aba **Regularização Ambiental** é liberada no Demonstrativo da Situação do CAR, onde o cidadão pode aderir ao PRA e acompanhar o Termo de Compromisso.
:::

---

## Pontos de Atenção para Design

:::note Por que demarcação sugerida, não desenho do zero?
A geometria incorreta é a principal causa de retrabalho no CAR. Pedir que o cidadão desenhe o polígono sem referência é uma barreira especialmente para pequenos produtores. A Carla pré-carrega uma sugestão com base nos dados já informados (área declarada + município), que o usuário ajusta — como confirmar a localização de uma encomenda, não como fazer um mapa do zero.
:::

:::warning Geometria — validações em tempo real
Validar enquanto o usuário ancora os vértices (não só ao finalizar) reduz o retrabalho:
- Área calculada diverge da declarada (> 5%): alerta imediato
- Polígono sai do município: alerta imediato
- Self-intersection (bordas que se cruzam): alerta imediato
- Sobreposição com TIs/UCs/outras propriedades: verificação assíncrona — não bloqueia, mas gera alerta para o analista
:::

:::warning Upload em conexão ruim
A etapa 4 (Documentação) envolve envio de imagens. Em conexões 3G instáveis o upload deve:
- Mostrar progresso incremental
- Suportar retomada em caso de falha de rede
- Limitar tamanho a 50MB com mensagem clara antes do envio
:::

:::tip Stepper de etapas sempre visível
Em mobile, o indicador de etapa atual (1 de 6, 2 de 6...) deve permanecer fixo no topo da conversa. O cidadão precisa saber onde está na jornada a qualquer momento.
:::

:::tip Confirmação em bloco — não campo a campo
Ao final de cada etapa, a Carla exibe um resumo de todos os dados daquela etapa para o cidadão revisar de uma só vez. Isso é mais eficiente e menos cansativo do que confirmar cada campo individualmente.
:::

---

## Ver também

- [Sequência de Mensagens](./mensagens-simuladas.md) — scripts completos de conversa
- [Abertura da Carla](./abertura-carla.md) — os 4 cenários de entrada pelo car.gov.br
- [Fluxo do Analista](./analista.md) — o que acontece depois do envio
- [Princípios UX](../principios.md) — diretrizes de linguagem e acessibilidade
