# ADR-004: RabbitMQ como Message Broker

**Status:** Aceito  
**Data:** 2026-06-01  
**Contexto:** Infraestrutura de mensageria

---

## Contexto

Com a decisão pela EDA (ADR-003), precisamos escolher o message broker. Os requisitos específicos do CARla são:

- **Dead Letter Queues:** Retry automático com backoff exponencial — processos falhados não podem ser perdidos
- **Routing flexível:** Diferentes consumers precisam de diferentes subconjuntos de eventos (analista quer eventos de processo, worker OCR quer eventos de documento)
- **ACK/NACK explícito:** Consumer deve confirmar processamento antes de evento ser removido da fila
- **Management UI:** Analistas de plataforma precisam monitorar filas sem CLI
- **Persistência de mensagens:** Mensagens não podem ser perdidas se o broker reiniciar
- **Volume esperado:** 1.000-10.000 processos/dia → não é big data, é workflow management

---

## Decisão

**Adotar RabbitMQ 3.13+ com a seguinte configuração:**

### Exchange e Filas

```python
# Configuração do RabbitMQ via aio-pika (Python async)
import aio_pika

async def setup_topology(channel: aio_pika.Channel) -> None:
    # Exchange principal
    car_exchange = await channel.declare_exchange(
        "car.events",
        aio_pika.ExchangeType.TOPIC,
        durable=True,
    )
    
    # Dead Letter Exchange
    dlx = await channel.declare_exchange(
        "car.dlx",
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )
    
    # Filas com DLQ e retry policy
    filas_config = [
        ("processo.analista", "processo.*"),
        ("processo.notificacao", "processo.*"),
        ("documento.ocr", "documento.*"),
        ("integracao.sicar", "processo.aprovado.*"),
        ("analytics.metricas", "#"),
    ]
    
    for fila_nome, routing_key in filas_config:
        # DLQ para mensagens que falharam após todas as tentativas
        dlq = await channel.declare_queue(
            f"car.dlq.{fila_nome}",
            durable=True,
        )
        await dlq.bind(dlx, routing_key=fila_nome)
        
        # Fila principal com configuração de retry
        fila = await channel.declare_queue(
            fila_nome,
            durable=True,
            arguments={
                "x-dead-letter-exchange": "car.dlx",
                "x-dead-letter-routing-key": fila_nome,
                "x-message-ttl": 86400000,  # 24h max
                "x-max-priority": 10,
            }
        )
        await fila.bind(car_exchange, routing_key=routing_key)
```

### Publisher com Outbox Relay

```python
async def publicar_evento(event: DomainEvent, channel: aio_pika.Channel) -> None:
    car_exchange = await channel.get_exchange("car.events")
    
    message = aio_pika.Message(
        body=json.dumps({
            "event_id": str(event.id),
            "event_name": event.routing_key,
            "occurred_at": event.occurred_at.isoformat(),
            "payload": event.to_dict(),
        }).encode(),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,  # sobrevive a restart
        content_type="application/json",
        headers={"schema_version": "1"},
    )
    
    await car_exchange.publish(message, routing_key=event.routing_key)
```

### Consumer com Retry Exponencial

```python
async def consumer_com_retry(message: aio_pika.IncomingMessage, handler) -> None:
    tentativas = message.headers.get("x-retry-count", 0)
    
    async with message.process(requeue=False):
        try:
            await handler(message)
        except Exception as exc:
            if tentativas < 3:
                # Requeue com delay crescente
                delay_ms = [1000, 5000, 25000][tentativas]
                await republish_with_delay(message, delay_ms, tentativas + 1)
            else:
                # Após 3 tentativas vai para DLQ permanente
                await send_to_dlq(message, str(exc))
```

### Cluster em Produção

```yaml
# docker-compose snippet para dev (3 nós em prod)
rabbitmq:
  image: rabbitmq:3.13-management
  environment:
    RABBITMQ_DEFAULT_USER: carla
    RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
    RABBITMQ_DEFAULT_VHOST: carla
  volumes:
    - rabbitmq_data:/var/lib/rabbitmq
  ports:
    - "5672:5672"    # AMQP
    - "15672:15672"  # Management UI
  healthcheck:
    test: ["CMD", "rabbitmq-diagnostics", "ping"]
    interval: 30s
```

---

## Consequências

### Positivas
- **Routing flexível:** Topic exchange com wildcards (`processo.*`, `#`) atende todos os cenários de fan-out
- **DLQ robusta:** Mensagens falhas não são perdidas — monitoravelmente disponíveis para reprocessamento
- **Management UI:** `/api/v1/admin/metricas/sistema` pode consultar a API HTTP do RabbitMQ Management
- **ACK/NACK:** Garante que mensagem só é removida após processamento bem-sucedido
- **Quorum Queues:** Alta disponibilidade em cluster com replicação Raft (mais seguro que mirroring legacy)
- **Operacionalmente simples:** Mais fácil que Kafka para equipe sem expertise em streaming

### Negativas
- **Não é event log permanente:** Mensagens processadas são removidas — sem replay de histórico completo
- **Ordenação por consumer:** Ordenação global não garantida em múltiplos consumers
- **Escalabilidade limitada:** ~100k msg/s em cluster — suficiente para o volume do CAR mas não é Kafka

### Riscos
- Management UI exposta na rede interna pode ser vetor de ataque — proteger com autenticação forte
- Quorum queues exigem número ímpar de nós (3 ou 5) — garantir configuração correta do cluster

---

## Alternativas Consideradas

| Alternativa | Prós | Contras | Motivo da Rejeição |
|---|---|---|---|
| **Apache Kafka** | Event log permanente, replay, 1M+ msg/s | Complexidade operacional alta, DLQ manual, ZooKeeper/KRaft overhead | Over-engineering; volume CAR não justifica Kafka |
| **AWS SQS/SNS** | Gerenciado, sem ops | Vendor lock-in, custo, sem Management UI, latência maior | Filosofia cloud-agnostic; custo em produção governamental |
| **Redis Streams** | Simples, integrado ao Redis existente | DLQ fraca, sem management UI, sem persistent delivery nativo robusto | Ferramenta errada para o trabalho |
| **NATS** | Ultra-rápido, simples | Sem DLQ nativa (JetStream é mais novo), menor comunidade | RabbitMQ mais maduro para workflows |
| **ActiveMQ Artemis** | JMS-compliant, maduro | Performance inferior ao RabbitMQ, ecossistema Python menor | RabbitMQ tem melhor suporte Python (aio-pika) |

---

## Referências

- [RabbitMQ Quorum Queues](https://www.rabbitmq.com/docs/quorum-queues)
- [aio-pika — Python async RabbitMQ](https://aio-pika.readthedocs.io/)
- [Transactional Outbox com RabbitMQ](https://microservices.io/patterns/data/transactional-outbox.html)
- [RabbitMQ vs Kafka](https://www.rabbitmq.com/docs/rabbitmq-vs-kafka)
