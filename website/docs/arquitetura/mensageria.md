---
sidebar_position: 4
title: Mensageria
description: RabbitMQ — exchanges, filas, DLQ, retry policy e Outbox Pattern.
tags: [engenharia, arquitetura, rabbitmq, mensageria, outbox]
---

# Mensageria

:::info Para quem é esta página
Engenheiros back-end. Decisão de usar RabbitMQ: [ADR-004](./decisoes/adr-004-rabbitmq.md).
:::

## Topologia

```
Exchange: car.events (type: topic)
│
├── processo.*     → fila: processos.analista
├── processo.*     → fila: processos.notificacao
├── documento.*    → fila: documentos.ocr
├── canal.whatsapp.* → fila: whatsapp.mensagens
├── *.aprovado     → fila: integracao.sicar
└── #              → fila: analytics.metricas

Dead Letter Exchange: car.dlx
└── car.dlq.{nome_da_fila}  (após 3 tentativas)
```

## Retry Policy

Após falha no processamento de uma mensagem:

| Tentativa | Delay |
|---|---|
| 1ª | 1 segundo |
| 2ª | 5 segundos |
| 3ª | 25 segundos |
| 4ª (falhou) | → Dead Letter Queue permanente |

:::warning Consumers devem ser idempotentes
Como mensagens podem ser entregues mais de uma vez (falha antes do ACK), sempre verifique se o evento já foi processado via `event_id` antes de executar a lógica.
:::

## Outbox Pattern

Garante que um evento nunca é publicado sem o dado correspondente estar no banco:

```python
# Na mesma transação ACID:
async with db.begin():
    processo_salvo = await repo.save(processo)
    for event in processo.domain_events:
        await outbox_repo.save(OutboxMessage(
            event_name=event.routing_key,
            payload=event.to_dict(),
            status="pendente",
        ))
    processo.clear_events()

# Worker separado (Outbox Relay) lê e publica:
# SELECT * FROM outbox WHERE status='pendente' ORDER BY created_at LIMIT 100
# → Publica no RabbitMQ
# → UPDATE outbox SET status='publicado'
```

## Schema de Mensagem

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_name": "processo.submetido.v1",
  "occurred_at": "2026-01-15T10:30:00Z",
  "correlation_id": "req-uuid",
  "payload": {
    "processo_id": "...",
    "requerente_id": "...",
    "municipio_ibge": "2111300"
  }
}
```

## Ver também

- [ADR-003 — Event-Driven Architecture](./decisoes/adr-003-eda.md)
- [ADR-004 — RabbitMQ](./decisoes/adr-004-rabbitmq.md)
- [Event Storming — Routing Keys](../dominio/event-storming.md#tabela-consolidada-de-eventos)
