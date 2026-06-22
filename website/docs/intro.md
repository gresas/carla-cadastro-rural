---
sidebar_position: 0
title: O que é a Carla
description: Visão geral do projeto Carla — assistente virtual do CAR (Cadastro Ambiental Rural), desenvolvida no haCARthon como parte do projeto CAR DPG.
---

# O que é a Carla?

A **Carla** é uma assistente virtual de chat para o Cadastro Ambiental Rural (CAR), desenvolvida como solução para o **Desafio 1 do haCARthon** — maratona de inovação aberta organizada por MGI, FBDS, Enap e Governo da Noruega, no contexto do projeto **CAR DPG (Digital Public Good)**.

:::info Para quem é esta página
Para qualquer pessoa que chegou aqui pela primeira vez. Escolha depois a seção mais próxima da sua área.
:::

A Carla é uma **interface web de chat própria**, acessada via `car.gov.br`. Ela orienta o cidadão ao longo de todo o processo de criação e acompanhamento do CAR, com autenticação segura pelo Gov.br — sem depender de WhatsApp, Telegram ou qualquer plataforma de mensageria proprietária.

## O problema que resolve

O Cadastro Ambiental Rural é obrigatório para qualquer imóvel rural no Brasil (Lei 12.651/2012). Sem ele, o produtor não acessa crédito rural nem pode comercializar produtos com regularidade ambiental.

Apesar da importância, o processo é marcado por dificuldades:

| Quem sofre | Problema |
|---|---|
| **Produtor rural** | Formulário técnico sem orientação, documentação confusa, sem feedback claro de pendências |
| **Analista ambiental** | Alto volume de processos incompletos, revisão manual repetitiva, sem triagem inteligente |

Os dados oficiais do sistema revelam o impacto dessas dificuldades:

- **Taxa de retificação** subiu de 5,7% (2014) para **77% em 2026** — a grande maioria dos cadastros precisa ser corrigida após a primeira tentativa
- **93,8% dos imóveis** cadastrados são de perfil "Pequeno" — produtores com menos recursos e menor familiaridade com sistemas técnicos
- **~34% dos imóveis** com situação de PRA informada **não aderiram** ao Programa de Regularização Ambiental

*Fonte: planilha oficial de dados do CAR — SICAR/MMA.*

## O que a Carla faz

```
car.gov.br → banner "Fale com a Carla" → chat web → Gov.br (login) → Carla orienta o cadastro
```

A Carla não substitui o fluxo tradicional do CAR — o cidadão continua podendo usar as plataformas estaduais (como a do Acre) ou o SICAR diretamente. A Carla é um **canal alternativo**, mais acessível:

- **Assistente conversacional** — orienta em linguagem simples, passo a passo, 24h
- **Reaproveitamento de dados** — nunca pede a mesma informação duas vezes; confirma em bloco ao final de cada etapa
- **Etapa Geo assistida** — sugere a demarcação de polígonos com base nos dados já informados; o usuário ajusta e confirma (sem desenhar do zero)
- **Validação documental automática** — OCR, extração de dados e verificação de consistência
- **Acompanhamento de status** — usa a terminologia oficial do SICAR e notifica sobre mensagens do analista
- **Portal do Analista** — fila priorizada, dossiê automático por IA, gestão de pendências

## Por onde começar

| Sou de... | Comece por... |
|---|---|
| **Produto** | [Visão e Objetivos](./produto/visao.md) |
| **Design / UX** | [Princípios de UX](./design/principios.md) |
| **Engenharia** | [Glossário do Domínio](./dominio/glossario.md) |
| **Qualquer área** | [Roadmap](./produto/roadmap.md) |

## Stack rápida

- **Backend:** Python 3.13 + FastAPI + PostgreSQL/PostGIS
- **Frontend:** React 18 + TypeScript + Tailwind CSS
- **IA:** Claude (Anthropic) / GPT-4o / Ollama — agnóstico via Adapter Pattern
- **Auth:** Gov.br OAuth2/OIDC + JWT RS256
- **Infra:** Docker + Kubernetes

:::tip Decisões explicadas
Todas as escolhas técnicas têm justificativa documentada nas [ADRs](./arquitetura/decisoes/index.md).
:::
