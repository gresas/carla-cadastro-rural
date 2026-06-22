---
sidebar_position: 7
title: Fundamentação Legal
description: Base legal do CAR e do PRA — Lei nº 12.651/2012 (Código Florestal) e Decreto nº 7.830/2012.
tags: [domínio, legal, car, pra, código-florestal, sicar]
---

# Fundamentação Legal

:::info Para quem é esta página
Engenheiros, PMs e analistas que precisam entender os dispositivos legais que determinam comportamento do sistema. O CARla modela regras de negócio derivadas diretamente desta legislação.
:::

---

## Lei nº 12.651/2012 — Código Florestal

A Lei nº 12.651/2012, conhecida como Código Florestal, é o principal diploma legal que institui e regulamenta o **Cadastro Ambiental Rural (CAR)** e o **Programa de Regularização Ambiental (PRA)**.

### Art. 29 — Instituição do CAR

> "É criado o Cadastro Ambiental Rural - CAR, no âmbito do Sistema Nacional de Informação sobre Meio Ambiente - SINIMA, registro público eletrônico de âmbito nacional, obrigatório para todos os imóveis rurais, com a finalidade de integrar as informações ambientais das propriedades e posses rurais, compondo base de dados para controle, monitoramento, planejamento ambiental e econômico e combate ao desmatamento."

**Implicações para o CARla:**
- O cadastro é **obrigatório** para todos os imóveis rurais
- É um **registro público** — os dados declarados fazem parte do SICAR nacional
- A finalidade é controle e monitoramento, não licenciamento

### Art. 29, § 1º — Conteúdo obrigatório

O CAR deve conter, no mínimo:
1. Identificação do proprietário ou possuidor rural
2. Comprovação da propriedade ou posse
3. Identificação do imóvel por meio de planta e memorial descritivo
4. Remanescentes de vegetação nativa, nascentes e cursos d'água
5. Servidões ambientais, Áreas de Uso Restrito e Áreas de Preservação Permanente
6. Áreas de Reserva Legal, inclusive as já constituídas

**Implicações para o CARla:**
- As 6 etapas do fluxo de cadastro (Cadastrante → Imóvel → Domínio → Documentação → Geo → Informações/PRA) mapeiam diretamente esses requisitos legais mínimos

### Art. 59 — PRA

> "A União, os Estados e o Distrito Federal deverão implantar Programas de Regularização Ambiental - PRAs de posses e propriedades rurais, com o objetivo de adequar e promover a regularização ambiental..."

> "§ 2º Para fins do disposto no caput, o proprietário ou possuidor rural deverá ser inscrito no CAR."

**Implicações para o CARla:**
- O CAR é **pré-requisito** para adesão ao PRA
- A identificação do passivo ambiental no cadastro aciona o fluxo de notificação sobre o PRA

---

## Decreto nº 7.830/2012 — Regulamentação do SICAR

O Decreto nº 7.830/2012 regulamenta o SICAR (Sistema de Cadastro Ambiental Rural) e define regras operacionais que o CARla deve modelar.

### Art. 2º — Natureza declaratória

> "O CAR é de natureza declaratória e permanente, não podendo o órgão competente exigir documentos além dos previstos neste Decreto."

**Implicação central:** o cidadão *declara* os dados; o órgão *analisa*. A Carla facilita a declaração correta — não garante aprovação. Documentos além dos exigidos em decreto não podem ser exigidos pelos analistas.

### Art. 3º — Status dos cadastros

O decreto define o ciclo de vida oficial dos cadastros:

| Status | Significado |
|---|---|
| **Em Andamento** | Registro iniciado, não finalizado |
| **Cadastrado** | Todas as etapas preenchidas, aguardando envio |
| **Gravado/Enviado** | Enviado ao SICAR, aguardando análise |
| **Em Análise** | Analista ambiental está avaliando o processo |
| **Regular** | Análise concluída; dados consistentes e limites atendidos |
| **Pendente de Regularização** | Déficit ambiental identificado; obrigação de adesão ao PRA |

:::caution Terminologia obrigatória
Use **sempre** esses termos nos artefatos da Carla — código, mensagens ao usuário, logs, métricas. Nunca "aprovado", "reprovado", "rejeitado" ou "cancelado".
:::

### Art. 7º — Notificação única de pendência

> "O órgão estadual competente emitirá notificação única ao proprietário ou possuidor rural inscrito no CAR com passivo ambiental, para que este adira ao PRA, no prazo estabelecido pelo Estado."

**Implicações para o CARla:**
- Uma única notificação formal é emitida ao proprietário com passivo ambiental
- A Carla deve modelar esse evento como `ProcessoPendenteDeRegularização` com `NotificaçãoEmitida`
- O prazo para adesão ao PRA começa a contar a partir da notificação — a Carla agenda lembrete a 30 dias do vencimento

### Art. 8º — Inscrição no SICAR

> "A inscrição no CAR deverá ser feita, preferencialmente, por meio eletrônico no SICAR, de forma individualizada pelo proprietário ou possuidor rural ou por representante devidamente habilitado."

**Implicação:** a Carla é um *facilitador* da inscrição via SICAR — não substitui o SICAR, apenas guia o processo pelo chat.

---

## Instrumentos do PRA (Decreto 7.830/2012, Art. 9º)

| Instrumento | Quando se aplica | Implicação para o CARla |
|---|---|---|
| **Termo de Compromisso** | Todos os imóveis com passivo ambiental | A Carla informa sobre a necessidade de assinatura; a formalização ocorre no órgão estadual |
| **PRAD** (Projeto de Recuperação de Áreas Degradadas) | Passivo com necessidade de recuperação ativa | A Carla orienta sobre o que é o PRAD; elaboração é responsabilidade do RT |
| **CRA** (Cota de Reserva Ambiental) | Compensação de déficit de RL por título de vegetação nativa em outra área | A Carla pode informar sobre a possibilidade de compensação via CRA como alternativa ao PRAD |

---

## Tabela de Dispositivos × Funcionalidades da Carla

| Dispositivo legal | Funcionalidade da Carla |
|---|---|
| Lei 12.651/2012, art. 29 — obrigatoriedade | Onboarding: explicar ao produtor que o CAR é obrigatório e o que acontece sem ele |
| Lei 12.651/2012, art. 29, §1º — conteúdo mínimo | As 6 etapas do fluxo de criação do CAR |
| Lei 12.651/2012, art. 59 — PRA | Notificação de pendência, orientação sobre adesão ao PRA |
| Decreto 7.830/2012, art. 2º — natureza declaratória | Mensagens: "você declara, o analista avalia" |
| Decreto 7.830/2012, art. 3º — status oficiais | Terminologia obrigatória em toda a interface e notificações |
| Decreto 7.830/2012, art. 7º — notificação única | Evento `ProcessoPendenteDeRegularização`, lembrete de prazo PRA |
| Decreto 7.830/2012, art. 9º — instrumentos do PRA | Conteúdo RAG sobre Termo de Compromisso, PRAD e CRA |

---

## Ver também

- [PRA — Programa de Regularização Ambiental](./pra.md) — detalhe operacional do PRA na Carla
- [Glossário — terminologia oficial SICAR](./glossario.md)
- [ADR-005 — Gov.br como autenticação](../arquitetura/decisoes/adr-005-govbr.md)
- [Fluxo do Cidadão — Criação do CAR](../design/fluxos/cidadao.md)
