---
sidebar_position: 0
title: O que é o CARla
description: Visão geral do projeto CARla — assistente inteligente para o Cadastro Ambiental Rural.
---

# O que é o CARla?

O **CARla** é uma camada de inteligência posicionada sobre o SICAR (Sistema de Cadastro Ambiental Rural) — não o substitui, **potencializa**.

:::info Para quem é esta página
Para qualquer pessoa que chegou aqui pela primeira vez. Escolha depois a seção da sua área.
:::

## O problema que resolve

O Cadastro Ambiental Rural é obrigatório para qualquer imóvel rural no Brasil (Lei 12.651/2012). Sem ele, o produtor não acessa crédito rural nem pode comercializar produtos com regularidade ambiental.

Apesar da importância, o processo hoje é marcado por:

| Quem sofre | Problema |
|---|---|
| **Produtor rural** | Formulário técnico sem orientação, documentação confusa, sem feedback de pendências |
| **Analista ambiental** | Alto volume de processos incompletos, revisão manual repetitiva, sem triagem inteligente |

## O que o CARla faz

```
Cidadão → CARla → SICAR
```

O CARla se posiciona **entre** o cidadão e o SICAR, oferecendo:

- **Assistente IA conversacional** — responde dúvidas em linguagem simples, 24h
- **Validação documental automática** — OCR, extração de dados e verificação de consistência
- **Canal WhatsApp** — atendimento no canal que o brasileiro já usa, com autenticação segura via Gov.br
- **Portal do Analista** — fila priorizada, dossiê automático por IA, aprovação em um clique

## Por onde começar

Escolha a área mais próxima do seu papel:

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
