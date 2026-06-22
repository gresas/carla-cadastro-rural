---
sidebar_position: 2
title: Personas
description: Os quatro perfis de usuário do CARla com objetivos, frustrações e critérios de satisfação.
tags: [produto, ux, personas]
---

# Personas

:::info Para quem é esta página
Times de produto, design e pesquisa de UX. Para a versão focada em jornadas e fluxos de tela, veja [Personas UX](../design/personas.md).
:::

## P1 — João Silva | Produtor Rural

**52 anos · Agricultor familiar · Interior do Maranhão · Propriedade de 50 ha**

João herdou a terra do pai. Usa smartphone Android básico, tem dificuldade com interfaces digitais e já tentou fazer o CAR duas vezes — desistiu nas duas.

| Dimensão | Detalhe |
|---|---|
| **Objetivo principal** | Regularizar a propriedade para acessar crédito rural (exigência do banco) |
| **Letramento digital** | Baixo — usa apps de mensageria no celular, pouco além |
| **Canais preferidos** | Celular (chat, voz), atendimento presencial |
| **Maior frustração** | "Não entendo o que estão pedindo e não tenho com quem tirar dúvida" |

:::tip Job-to-be-done
João quer regularizar o imóvel **sem contratar consultor** — ele precisa de orientação em linguagem simples, não de formulário técnico.
:::

**Critérios de satisfação:**
- Conseguir iniciar e completar o processo sem ajuda presencial, via `car.gov.br`
- Receber notificação de pendência explicando o que falta em linguagem clara
- Acompanhar o status pela Carla (abre no celular, sem instalar app)

---

## P2 — Ana Costa | Responsável Técnica (RT)

**35 anos · Engenheira florestal · Brasília-DF · Registro CREA ativo**

Ana é contratada pontualmente por produtores rurais com imóveis acima de 4 módulos fiscais, onde a legislação exige assinatura de profissional habilitado. Ela assina digitalmente o processo e co-responde legalmente pelos dados prestados.

| Dimensão | Detalhe |
|---|---|
| **Objetivo principal** | Assinar processos tecnicamente corretos — um dado errado é risco de responsabilização no CREA |
| **Letramento digital** | Alto — usa planilhas, sistemas GIS |
| **Maior frustração** | "Descubro problemas no processo só depois que o produtor já ficou sem resposta por semanas" |
| **Diferencial do papel** | Como RT, Ana co-assina o processo e tem acesso específico aos processos autorizados pelo proprietário |

:::note Responsável Técnico no RBAC
O CARla diferencia o RT dos demais usuários: toda submissão assinada por RT gera registro de assinatura em `historico_processos` com o `ator_id` do RT e indicação de responsabilidade técnica — necessário para eventual fiscalização do conselho profissional (CREA/CONFEA/CFBio).
:::

:::tip Job-to-be-done
Ana quer **pré-validar documentos antes de submeter** e ser notificada automaticamente de pendências nos processos que assina.
:::

---

## P3 — Carlos Mendes | Analista Ambiental

**40 anos · Técnico ambiental · Servidor SEMA-MT · 300+ processos na fila**

Carlos trabalha com sistema legado lento e acumula horas extras para dar conta do volume. Abre processos e frequentemente descobre que falta documento básico — retrabalho evitável.

| Dimensão | Detalhe |
|---|---|
| **Objetivo principal** | Analisar mais processos por dia sem aumentar carga de trabalho |
| **Maior frustração** | "Gasto horas conferindo documentos que deveriam ter sido validados antes de chegar pra mim" |
| **O que mais valoriza** | Triagem inteligente e dossiê já pronto ao abrir um processo |

:::tip Job-to-be-done
Carlos quer **focar no julgamento técnico**, não na conferência manual de documentos.
:::

---

## P4 — Maria Santos | Administradora do Sistema

**38 anos · Analista de TI · SEMAD estadual · Responsável pela plataforma**

Maria mantém o sistema no ar, gerencia usuários e resolve incidentes. Não quer ser surpreendida — quer visibilidade antecipada de problemas.

| Dimensão | Detalhe |
|---|---|
| **Objetivo principal** | Uptime ≥ 99,5%, zero surpresas em produção |
| **Maior frustração** | "Fico sabendo do erro pelo usuário, não pelo sistema" |
| **O que mais valoriza** | Dashboard operacional em tempo real e configurações sem deploy |

---

## Relação entre Personas

```mermaid
graph LR
    J[João — Produtor] -->|submete processo| C[CARla]
    A[Ana — RT] -->|co-assina processo autorizado| C
    C -->|fila organizada| K[Carlos — Analista]
    K -->|aprova / rejeita| C
    C -->|notifica| J
    C -->|notifica| A
    M[Maria — Admin] -->|monitora| C
```

## Ver também

- [Casos de Uso](./casos-de-uso.md) — o que cada persona consegue fazer
- [Fluxo do Cidadão](../design/fluxos/cidadao.md) — jornada do João
- [Fluxo do Analista](../design/fluxos/analista.md) — jornada do Carlos
