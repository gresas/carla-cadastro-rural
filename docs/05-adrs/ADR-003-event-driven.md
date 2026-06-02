# ADR-003: Arquitetura Orientada a Eventos (Event-Driven Architecture)

**Status:** Aceito  
**Data:** 2026-06-01  
**Contexto:** Arquitetura de comunicação entre serviços

---

## Contexto

O sistema CARla tem características que favorecem fortemente uma arquitetura orientada a eventos:

1. **Workflows longos:** Um processo CAR pode levar dias ou semanas — comunicação síncrona causaria timeouts e acoplamento temporal
2. **Operações assíncronas:** OCR (30-60s), geração de dossiê (20-30s), consultas a sistemas externos lentos (SICAR, IBAMA) não devem bloquear o usuário
3. **Múltiplos consumidores:** Uma pendência criada deve notificar o cidadão (email), atualizar o dashboard (in-app), registrar no audit log — sem acoplamento entre esses sistemas
4. **Auditabilidade:** Cada evento é um registro imutável da evolução do processo — requisito legal do CAR
5. **Resiliência:** Falha no serviço de notificações não deve afetar o serviço de processos

---

## Decisão

**Adotar EDA com:**

1. **Domain Events** no núcleo do domínio — eventos imutáveis emitidos pelos agregados
2. **Outbox Pattern** para garantia de entrega atômica com a transação de banco
3. **RabbitMQ** como message broker
4. **Eventos versionados** (v1, v2) para evolução sem breaking changes

### Outbox Pattern

```python
# Na transação de banco: persiste o processo E o evento atomicamente
async with db.begin():
    processo_salvo = await repo.save(processo)
    for event in processo.domain_events:
        await outbox_repo.save(OutboxMessage(
            event_name=event.routing_key,
            payload=event.__dict__,
            status="pendente",
        ))
    processo.clear_events()

# Worker separado (Outbox Relay) publica para RabbitMQ
# Garante: evento nunca é perdido e nunca é publicado sem o dado no banco
```

### Schema de Evento

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_name": "processo.submetido.v1",
  "occurred_at": "2024-01-15T10:30:00Z",
  "correlation_id": "req-uuid",
  "payload": {
    "processo_id": "...",
    "requerente_id": "...",
    "municipio_ibge": "2111300",
    "area_total_ha": 150.0
  },
  "metadata": {
    "schema_version": "1",
    "service": "process-service"
  }
}
```

### Topologia RabbitMQ

```
Exchange: car.events (type: topic)
  ├── processo.*    → fila: processos.analista (consumer: portal analista)
  ├── processo.*    → fila: processos.notif (consumer: notificacao_worker)
  ├── documento.*   → fila: documentos.ocr (consumer: document_worker)
  ├── assistente.*  → fila: assistente.metrics (consumer: analytics)
  └── *.aprovado    → fila: integracao.sicar (consumer: integracao_worker)

Dead Letter Exchange: car.dlx
  └── car.dlq.{queue_name} (retry após 1s, 5s, 25s → DLQ permanente)
```

---

## Consequências

### Positivas
- **Desacoplamento temporal:** OCR pode demorar sem bloquear a resposta ao usuário
- **Resiliência:** Falha em um consumer não afeta outros
- **Auditoria natural:** Cada evento é um registro histórico do que aconteceu
- **Escalabilidade independente:** Consumer de OCR pode ter mais réplicas que consumer de notificação
- **Facilidade de novos integradores:** Novo sistema só precisa fazer subscribe, sem mudança nos produtores

### Negativas
- **Eventual consistency:** Estado do sistema não é imediatamente consistente — leitura logo após escrita pode retornar dado desatualizado
- **Debugging distribuído:** Rastrear um fluxo completo requer correlação de logs por `correlation_id` e trace_id (OpenTelemetry)
- **Ordenação de mensagens:** RabbitMQ não garante ordenação global — usar `correlation_id` + timestamps para reconstruir sequência
- **Duplicatas:** Consumers devem ser idempotentes (verificar se evento já foi processado via `event_id`)

### Riscos
- Equipe sem experiência em EDA pode introduzir acoplamento temporal escondido (ex: publicar evento antes do commit)
- **Mitigação:** Outbox Pattern obrigatório + review de código focado em ordem de operações

---

## Alternativas Consideradas

| Alternativa | Prós | Contras | Motivo da Rejeição |
|---|---|---|---|
| **REST síncrono** | Simples, fácil debug | Acoplamento temporal, timeouts em ops longas, cascata de falhas | Incompatível com OCR e dossiê assíncronos |
| **gRPC** | Performance, contrato forte, streaming | Ainda síncrono por natureza (streaming não é messgeria) | Não resolve o desacoplamento temporal |
| **GraphQL Subscriptions** | Bom para real-time no frontend | Não é solução de mensageria inter-serviços | Escopo é comunicação frontend, não backend |
| **Apache Kafka** | Event log permanente, replay, alta vazão | Operacionalmente complexo, não tem DLQ nativa simples, over-engineering para o volume esperado | RabbitMQ é suficiente e mais simples de operar |
| **Redis Streams** | Simples, integrado ao Redis existente | Sem DLQ robusta, sem management UI, persistência limitada | RabbitMQ mais maduro para mensageria |

---

## Referências

- [Martin Fowler — Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Outbox Pattern](https://microservices.io/patterns/data/transactional-outbox.html)
- [CloudEvents Specification](https://cloudevents.io/)
- [RabbitMQ Topic Exchange](https://www.rabbitmq.com/tutorials/tutorial-five-python.html)
