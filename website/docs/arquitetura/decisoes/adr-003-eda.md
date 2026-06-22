---
sidebar_position: 4
title: "ADR-003: Event-Driven Architecture"
description: Por que adotamos EDA com Domain Events e Outbox Pattern.
tags: [adr, eda, eventos, outbox, rabbitmq]
---

# ADR-003: Arquitetura Orientada a Eventos (EDA)

**Status:** Aceito | **Data:** 2026-06-01

## Contexto

O sistema tem workflows longos (processo CAR pode demorar dias), operações assíncronas (OCR, LLM, integrações externas) e múltiplos consumidores para o mesmo evento (notificação email + Carla + analytics).

## Decisão

**EDA com Domain Events + Outbox Pattern + RabbitMQ.**

Cada operação de negócio emite Domain Events. O Outbox Pattern garante entrega atômica com a transação de banco. Workers independentes consumem os eventos.

## Consequências

✅ Desacoplamento temporal — OCR não bloqueia a resposta ao usuário  
✅ Resiliência — falha em notificações não afeta o processo em si  
✅ Auditoria natural — cada evento é um registro histórico imutável  
✅ Escalabilidade independente por consumer  
❌ Eventual consistency — leitura imediata após escrita pode retornar dado desatualizado  
❌ Debugging distribuído exige correlação de logs por `trace_id`

## Alternativas Rejeitadas

| Alternativa | Motivo |
|---|---|
| REST síncrono | Acoplamento temporal; timeouts em operações longas |
| Kafka | Over-engineering para o volume esperado; operacionalmente complexo |
