---
sidebar_position: 6
title: Plataformas Estaduais de Registro CAR
description: Alguns estados têm plataformas próprias para registro do CAR; os demais usam o SICAR federal. Como o CARla endereça essa diversidade.
tags: [domínio, sicar, estados, integração]
---

# Plataformas Estaduais de Registro CAR

## Contexto

O CAR é um registro federal obrigatório (Lei 12.651/2012), mas a **gestão é descentralizada**: cada estado é responsável pela análise dos processos. Isso criou uma fragmentação: alguns estados desenvolveram plataformas próprias para o cadastro; os demais continuam usando o SICAR federal.

---

## Cenários de plataforma

| Cenário | Descrição | Como o CARla atua |
|---|---|---|
| **SICAR federal** | Estado usa car.gov.br como plataforma de cadastro | Integração direta com o SICAR |
| **Plataforma estadual** | Estado tem sistema próprio integrado ao SICAR | CARla orienta o produtor e pode encaminhar para a plataforma estadual |

---

## Por que isso importa

Alguns estados criaram seus próprios sistemas de cadastro que:
- Apresentam interface local adaptada às exigências estaduais
- Integram-se com o SICAR federal via protocolo próprio
- Podem ter campos adicionais ou fluxos de análise distintos

O SICAR federal permanece como **repositório central** dos registros — qualquer cadastro, independente da plataforma de origem, termina centralizado no SICAR.

---

## Exemplo Mapeado: Acre

O fluxo de cadastro do CAR no Acre foi mapeado como referência para a implementação das 6 etapas guiadas da Carla. O Acre usa o SICAR federal como plataforma de cadastro, com as seguintes etapas:

| Etapa | Dados principais |
|---|---|
| **1. Cadastrante** | CPF, data de nascimento, nome completo, nome da mãe, representante legal |
| **2. Imóvel** | Nome do imóvel, município, CEP, zona (rural/urbana), acesso, correspondência |
| **3. Domínio** | Proprietário(s)/possuidor(es) — PF ou PJ — com documentos comprobatórios |
| **4. Documentação** | Tipo (Propriedade ou Posse), área (ha), matrícula/CCIR/SNCR/NIRF, Reserva Legal averbada |
| **5. Geo** | Demarcação do polígono do imóvel (a Carla sugere com base nos dados já informados) |
| **6. Informações (PRA)** | 12 perguntas sobre situação ambiental: adesão ao PRA, déficit de RL, TAC, PRAD, RPPN, CRF, multas etc. |

Este mapeamento é a base do fluxo conversacional da Carla e dos scripts de mensagem documentados em [Sequência de Mensagens](../design/fluxos/mensagens-simuladas.md).

---

## Posicionamento da Carla

A Carla integra diretamente com o **SICAR federal** — o repositório central que todos os estados alimentam. Para estados com plataformas próprias:

1. A Carla identifica o estado do imóvel a partir do município informado na Etapa 2
2. Orienta o produtor sobre o fluxo correto para aquele estado
3. Em uma evolução futura, adaptadores estaduais podem ser desenvolvidos conforme demanda

A Carla é um **canal alternativo** — o produtor pode continuar usando o SICAR ou a plataforma estadual diretamente, se preferir.

---

## Ver também

- [Glossário — SICAR, Recibo de Inscrição](./glossario.md)
- [Sequência de Mensagens — Etapas de Criação do CAR](../design/fluxos/mensagens-simuladas.md)
- [Visão do Produto](../produto/visao.md)
- [Roadmap — Fase 3](../produto/roadmap.md)
