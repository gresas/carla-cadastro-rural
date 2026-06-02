---
sidebar_position: 2
title: Serviços
description: Responsabilidades, portas e estrutura interna de cada container do CARla.
tags: [engenharia, arquitetura, serviços, fastapi]
---

# Serviços

:::info Para quem é esta página
Engenheiros back-end. Para o mapa geral, veja [Visão Geral](./visao-geral.md).
:::

## Tabela de Serviços

| Serviço | Porta | BC | Responsabilidade |
|---|---|---|---|
| Auth Service | 8001 | IAM | OAuth2 Gov.br, JWT, RBAC |
| Process Service | 8002 | Processos CAR | CRUD, máquina de estados, pendências |
| Document Service | 8003 | Validação Documental | Upload, armazenamento, trigger de OCR |
| AI Assistant | 8004 | Assistência Inteligente | Chat, RAG, geração de dossiê |
| Analytics Service | 8005 | Analytics | Relatórios, KPIs, exportações |
| Integration Service | 8006 | Integrações Externas | ACL: SICAR, SIGEF, IBAMA |
| WhatsApp Service | 8007 | Canal WhatsApp | Webhook Meta, vinculação Gov.br |

## Estrutura Interna (padrão por serviço)

```
src/carla/modules/{nome}/
├── domain/
│   ├── entities.py       # Agregados e entidades
│   ├── value_objects.py  # VOs com validação
│   ├── services.py       # Serviços de domínio
│   ├── events.py         # Domain Events
│   └── repository.py     # Interface (ABC)
├── application/
│   └── use_cases/        # Um arquivo por caso de uso
├── infrastructure/
│   ├── models.py         # SQLAlchemy ORM
│   ├── repository.py     # Implementação concreta
│   └── (adapters)        # Clientes externos
└── presentation/
    ├── router.py         # FastAPI endpoints
    └── schemas.py        # Pydantic request/response
```

## Recursos Kubernetes (Produção)

| Serviço | Réplicas Min | CPU Req | Mem Req | HPA |
|---|---|---|---|---|
| Process Service | 2 | 500m | 512Mi | CPU > 70% |
| AI Assistant | 2 | 500m | 512Mi | Conexões > 100 |
| Document Worker | 2 | 1000m | 1Gi | Profundidade da fila |
| WhatsApp Service | 2 | 200m | 256Mi | CPU > 70% |

:::tip MVP Hackathon
Para o hackathon, todos os módulos rodam como um **monolito modular** em um único processo FastAPI. A separação em serviços acontece na Fase 3 via Strangler Fig Pattern.
:::
