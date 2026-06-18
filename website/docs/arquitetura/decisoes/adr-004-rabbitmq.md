---
sidebar_position: 5
title: "ADR-004: RabbitMQ"
description: Por que escolhemos RabbitMQ como message broker para o CARla.
tags: [adr, rabbitmq, mensageria]
---

# ADR-004: RabbitMQ como Message Broker

**Status:** Aceito | **Data:** 2026-06-01

## Contexto

Com a decisão pela EDA ([ADR-003](./adr-003-eda.md)), precisamos de um broker. Requisitos: DLQ robusta, routing flexível, ACK/NACK explícito, Management UI, persistência de mensagens.

## Decisão

**RabbitMQ 3.13+** com Topic Exchange `car.events`, Quorum Queues, DLX/DLQ por fila, mensagens persistentes (`delivery_mode=2`), cluster de 3 nós em produção.

## Consequências

✅ Topic exchange com wildcards atende todos os cenários de fan-out  
✅ DLQ robusta — mensagens falhas monitoravelmente disponíveis  
✅ Management UI para operações sem CLI  
✅ Mais simples de operar que Kafka para o volume do CAR  
❌ Não é event log permanente — mensagens processadas são removidas  
❌ Ordenação global não garantida com múltiplos consumers

## Alternativas Rejeitadas

| Alternativa | Motivo |
|---|---|
| Apache Kafka | Over-engineering; DLQ manual complexa; operacionalmente pesado |
| Redis Streams | DLQ fraca; sem Management UI |
| AWS SQS/SNS | Vendor lock-in; sem Management UI |
