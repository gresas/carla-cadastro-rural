---
sidebar_position: 0
title: O que é o CARla
description: Visão geral do projeto CARla — assistente inteligente para o Cadastro Ambiental Rural.
---

# O que é o CARla?

O **CARla** é um sistema web que integra diretamente com o SICAR (Sistema de Cadastro Ambiental Rural) para simplificar o registro do CAR — com IA, validação documental, geometria por satélite e atendimento via WhatsApp.

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
Produtor Rural → CARla (web + WhatsApp) → SICAR (integração direta)
```

O CARla faz o que o produtor rural não consegue fazer sozinho no SICAR:

- **Assistente IA conversacional** — responde dúvidas em linguagem simples, 24h
- **Geometria por satélite** — o produtor traça o polígono do imóvel sobre foto aérea real (Leaflet + tile de satélite), sem GPS impreciso
- **Validação documental automática** — OCR, extração de dados e verificação de consistência
- **Canal WhatsApp** — atendimento no canal que o brasileiro já usa, com autenticação segura via Gov.br
- **Portal do Analista** — fila priorizada, dossiê automático por IA, aprovação em um clique

:::note Realidade multi-plataforma
Alguns estados têm plataformas próprias de registro do CAR; os demais usam o SICAR federal. O CARla se integra com o SICAR federal e endereça essa diversidade — veja [Plataformas Estaduais](./dominio/plataformas-estaduais.md).
:::

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
