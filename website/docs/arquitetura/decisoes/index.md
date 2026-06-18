---
sidebar_position: 1
title: Decisões Arquiteturais (ADRs)
description: Índice de Architecture Decision Records do CARla — por que cada escolha foi feita.
tags: [engenharia, adr, arquitetura, decisões]
---

# Decisões Arquiteturais (ADRs)

:::info Para quem é esta página
Engenheiros e arquitetos. ADRs registram o **porquê** das decisões — não apenas o **o quê**.
:::

## O que é um ADR?

Um Architecture Decision Record (ADR) é um documento curto que registra uma decisão arquitetural significativa: o contexto, a decisão tomada, as consequências e as alternativas rejeitadas.

> "O código diz o que foi feito. O ADR diz por que foi feito assim."

## ADRs do CARla

| ID | Decisão | Status |
|---|---|---|
| [ADR-001](./adr-001-fastapi.md) | FastAPI como framework web Python | Aceito |
| [ADR-002](./adr-002-postgresql.md) | PostgreSQL + PostGIS como banco principal | Aceito |
| [ADR-003](./adr-003-eda.md) | Arquitetura Orientada a Eventos (EDA) | Aceito |
| [ADR-004](./adr-004-rabbitmq.md) | RabbitMQ como message broker | Aceito |
| [ADR-005](./adr-005-govbr.md) | Autenticação via Gov.br (OAuth2/OIDC) | Aceito |
| [ADR-006](./adr-006-ia.md) | LLM agnóstico com Adapter Pattern | Aceito |

## Como criar um novo ADR

Veja o guia completo em [Contribuindo → Novo ADR](../../contribuindo/novo-adr.md).

**Regra de ouro:** Crie um ADR quando a decisão:
- Afeta múltiplos serviços ou camadas
- Tem implicações de segurança ou conformidade legal
- Tem trade-offs significativos que precisam ser documentados
- Pode ser questionada no futuro ("por que fizemos assim?")
