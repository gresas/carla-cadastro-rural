# CARla — Arquitetura do Sistema

**Versão:** 1.0.0  
**Data:** 2026-06-01

---

## 1. Modelo C4

### Nível 1 — Contexto do Sistema

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CAR COPILOT — System Context                          │
└─────────────────────────────────────────────────────────────────────────────┘

  [Produtor Rural]          [Consultor Ambiental]      [Analista Ambiental]
       │                          │                           │
       └──────────────────────────┴───────────────────────────┘
                                  │ HTTPS (Browser/Mobile)
                                  ▼
                      ┌───────────────────────────┐
                      │                           │
                      │      CAR COPILOT          │
                      │                           │
                      │  • Portal do Cidadão      │
                      │  • Assistente IA          │
                      │  • Motor de Validação     │
                      │  • Portal do Analista     │
                      │                           │
                      └─────────────┬─────────────┘
                                    │
         ┌──────────────────────────┼───────────────────────────┐
         │                          │                           │
         ▼                          ▼                           ▼
  [Gov.br — IdP]         [SICAR — Sistema CAR]          [SIGEF — INCRA]
  OAuth2/OIDC            REST/SOAP (consulta)           REST (georef)
         │                          │                           │
         ▼                          ▼                           ▼
  [IBAMA/ICMBio]        [MapBiomas/TerraBrasilis]       [FUNAI]
  Alertas/embargos      Uso do solo / Satélite          Terras indígenas
```

---

### Nível 2 — Containers

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              CAR COPILOT — Containers                             │
└──────────────────────────────────────────────────────────────────────────────────┘

Browser/Mobile
     │ HTTPS :443
     ▼
┌────────────────────────────────────────────────────────┐
│  Nginx API Gateway   (rate limiting, TLS termination)  │
│  nginx:1.27-alpine   :80/:443                          │
└────────────────────────────────────────────────────────┘
     │                    │                    │
     ▼                    ▼                    ▼
┌──────────────┐  ┌──────────────┐  ┌───────────────────┐
│ Web App      │  │ Auth Service │  │ Process Service   │
│ React 18     │  │ FastAPI      │  │ FastAPI           │
│ Vite + TS    │  │ :8001        │  │ :8002             │
│ :3000        │  │ OAuth2/JWT   │  │ BC: Processos CAR │
│ Tailwind CSS │  │ Gov.br OIDC  │  │ DDD — Core Domain │
└──────────────┘  └──────────────┘  └───────────────────┘
                                            │
                ┌───────────────────────────┤
                │                           │
                ▼                           ▼
┌──────────────────────┐  ┌─────────────────────────────┐
│ Document Service     │  │ AI Assistant Service        │
│ FastAPI :8003        │  │ FastAPI :8004               │
│ BC: Validação        │  │ BC: Assistência Inteligente │
│ OCR + Extração       │  │ LLM + RAG + SSE Streaming   │
└──────────────────────┘  └─────────────────────────────┘
                │
                ▼
┌──────────────────────┐  ┌──────────────────────────────┐
│ Analytics Service    │  │ Integration Service          │
│ FastAPI :8005        │  │ FastAPI :8006                │
│ BC: Analytics        │  │ BC: Integrações Externas     │
│ Dossiês, relatórios  │  │ ACL: SICAR/SIGEF/IBAMA       │
└──────────────────────┘  └──────────────────────────────┘

Workers (Python Consumers RabbitMQ):
┌──────────────────┐  ┌──────────────────────┐  ┌────────────────────┐
│ Document Worker  │  │ Notification Worker  │  │ Integration Worker │
│ OCR assíncrono   │  │ Email/SMS/Push       │  │ SICAR/IBAMA sync   │
│ ClamAV scan      │  │                      │  │ Outbox relay       │
└──────────────────┘  └──────────────────────┘  └────────────────────┘

Infraestrutura:
┌─────────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL 16  │  │  Redis 7     │  │  RabbitMQ    │  │  MinIO       │
│  + PostGIS 3.4  │  │  :6379       │  │  3.13        │  │  (S3-compat) │
│  + pgvector     │  │  Cache/BL    │  │  :5672/15672 │  │  :9000       │
│  :5432          │  │  Sessions    │  │  Mensageria  │  │  Documentos  │
└─────────────────┘  └──────────────┘  └──────────────┘  └──────────────┘

Observabilidade:
┌────────────────────┐  ┌──────────────────┐  ┌──────────────┐
│ OTel Collector     │  │  Prometheus       │  │  Grafana     │
│ :4317 (gRPC)       │  │  :9090           │  │  :3001       │
│ Traces/Metrics/Log │  │  Métricas        │  │  Dashboards  │
└────────────────────┘  └──────────────────┘  └──────────────┘
```

---

### Nível 3 — Componentes do Process Service

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PROCESS SERVICE — Components                      │
└─────────────────────────────────────────────────────────────────────┘

HTTP Request
     │
     ▼
┌─────────────────────────────────┐
│        ProcessRouter            │
│  (FastAPI APIRouter)            │
│  /api/v1/processos              │
└────────────────┬────────────────┘
                 │ Depends()
                 ▼
┌─────────────────────────────────┐
│   Auth Middleware               │
│   (JWT validation + RBAC)       │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│   ProcessController             │
│   (FastAPI Dependencies)        │
│   Injeta: use_case, user        │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│   CriarProcessoUseCase          │
│   (Application Layer)           │
│   Orquestra: domain + repo      │
└───┬────────────────────┬────────┘
    │                    │
    ▼                    ▼
┌──────────────┐  ┌─────────────────────────────────┐
│ ProcessoCAR  │  │  ProcessoCARRepository          │
│ (Aggregate)  │  │  (SQLAlchemy 2.0 + GeoAlchemy2) │
│ Domain Model │  │  + UnitOfWork                   │
└──────────────┘  └──────────────────────┬────────────┘
                                         │
                          ┌──────────────┴──────────────┐
                          │                             │
                          ▼                             ▼
               ┌─────────────────────┐  ┌──────────────────────────┐
               │  PostgreSQL          │  │  OutboxEventPublisher    │
               │  (write model)       │  │  (tabela outbox)         │
               └─────────────────────┘  └──────────────────────────┘
                                                    │
                                                    ▼ (async worker)
                                        ┌───────────────────────────┐
                                        │  RabbitMQ Exchange        │
                                        │  car.events (topic)       │
                                        └───────────────────────────┘
```

---

### Nível 4 — Estrutura de Pacotes Python

```
src/carla/modules/processos/
├── domain/
│   ├── __init__.py
│   ├── entities.py         # ProcessoCAR, ImóvelRural, Documento, Pendência
│   ├── value_objects.py    # NumeroCAR, ÁreaTotalHectares, MunicípioIBGE, Geometria
│   ├── services.py         # CalculadorAreaRL, ValidadorGeometria, ClassificadorProcesso
│   ├── events.py           # ProcessoIniciado, ProcessoSubmetido, PendênciaIdentificada
│   ├── exceptions.py       # EstadoInvalidoError, DocumentacaoInsuficienteError
│   └── repository.py       # ProcessoCARRepository (ABC), ImóvelRuralRepository (ABC)
├── application/
│   ├── __init__.py
│   ├── use_cases/
│   │   ├── criar_processo.py       # CriarProcessoUseCase
│   │   ├── submeter_processo.py    # SubmeterProcessoUseCase
│   │   ├── aprovar_processo.py     # AprovarProcessoUseCase
│   │   ├── rejeitar_processo.py    # RejeitarProcessoUseCase
│   │   └── criar_pendencia.py      # CriarPendênciaUseCase
│   └── dtos.py             # CriarProcessoDTO, SubmeterProcessoDTO
├── infrastructure/
│   ├── __init__.py
│   ├── models.py           # SQLAlchemy ORM Models (ProcessoCARModel, etc.)
│   ├── repository.py       # ProcessoCARRepositoryImpl (implementação concreta)
│   ├── event_publisher.py  # OutboxEventPublisher
│   └── external/
│       └── sicar_adapter.py  # SICARAdapter (Anti-Corruption Layer)
└── presentation/
    ├── __init__.py
    ├── router.py           # FastAPI APIRouter com todos os endpoints
    └── schemas.py          # Pydantic v2 request/response schemas
```

---

## 2. Arquitetura Lógica

### Camadas da Aplicação

```
┌─────────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                              │
│  FastAPI Routers + Pydantic Schemas                             │
│  • Controllers (recebem HTTP, delegam para Application)         │
│  • Schemas (validação de request, serialização de response)     │
│  • Middleware (auth, logging, tracing, rate limit)              │
└─────────────────────────────────────────────────────────────────┘
                              │ DTOs
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  APPLICATION LAYER                                               │
│  Use Cases (orquestração)                                       │
│  • Use Cases: coordenam domain + infra                          │
│  • Application Services: agrupam use cases relacionados         │
│  • Event Handlers: reagem a domain events de outros BCs         │
└─────────────────────────────────────────────────────────────────┘
                              │ Domain Objects
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  DOMAIN LAYER  (núcleo — sem dependências externas)             │
│  • Entities: Processoo CAR, ImóvelRural, Documento              │
│  • Value Objects: NumeroCAR, CPF, Geometria                     │
│  • Domain Services: CalculadorAreaRL, ValidadorGeometria        │
│  • Domain Events: ProcessoSubmetido, PendênciaIdentificada      │
│  • Repository Interfaces: ProcessoCARRepository (ABC)           │
│  • Domain Exceptions: EstadoInvalidoError, InvarianteViolada    │
└─────────────────────────────────────────────────────────────────┘
                              │ Interfaces
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  INFRASTRUCTURE LAYER                                            │
│  • Repository Implementations: SQLAlchemy 2.0 + GeoAlchemy2    │
│  • ORM Models: Mapeamento SQLAlchemy                            │
│  • Message Bus: RabbitMQ Publisher via Outbox                   │
│  • External Adapters: SICARAdapter, GovBrAdapter, LLMAdapter   │
│  • Cache: Redis Client                                          │
│  • Storage: MinIO/S3 Client                                     │
└─────────────────────────────────────────────────────────────────┘
```

### Fluxo Completo — "Submeter Processo CAR"

```
1. POST /api/v1/processos/{id}/submeter
   │
   ▼
2. Nginx (TLS termination, rate limit check: 10/min para produtor)
   │
   ▼
3. Auth Middleware (JWT validation: RS256, exp, jti blacklist, nivel_confiabilidade >= prata)
   │
   ▼
4. ProcessController.submeter_processo()
   → Extrai: processo_id, current_user do JWT
   → Verifica ownership do processo
   │
   ▼
5. SubmeterProcessoUseCase.execute(processo_id, user_id)
   → await processo_repo.find_by_id(processo_id)
   → processo.submeter(user_id)  ← DOMÍNIO VALIDA INVARIANTES
     → Verifica documentação mínima
     → Verifica geometria definida
     → Muda status para SUBMETIDO
     → Emite ProcessoSubmetido (domain event)
   │
   ▼
6. async with unit_of_work:
   → await processo_repo.save(processo)        ← PERSISTE NO POSTGRESQL
   → await outbox_repo.save(ProcessoSubmetido) ← OUTBOX (mesma transação)
   ← COMMIT
   │
   ▼
7. Response 200: ProcessoCARResponse(status=submetido, numero_car=None)
   │
   ▼ (assíncrono — worker separado)
8. Outbox Relay Worker:
   → Lê tabela outbox WHERE status='pendente'
   → Publica no RabbitMQ: car.events / processo.submetido.v1
   → UPDATE outbox SET status='publicado'
   │
   ▼ (consumers em paralelo)
9a. NotificaçãoWorker consume processo.submetido:
    → Envia email de confirmação para o cidadão
    → Cria notificação in-app

9b. Analytics Consumer consume processo.submetido:
    → Incrementa métricas diárias

9c. IntegracaoWorker consume processo.submetido:
    → Consulta SICAR por registros anteriores do CPF (circuit breaker)
    → Enriquece o processo com dados retornados
```

---

## 3. Padrões Arquiteturais

### CQRS (Command Query Responsibility Segregation)

```python
# COMMANDS — passam pelo domínio, garantem invariantes
class CriarProcessoUseCase:
    async def execute(self, dto: CriarProcessoDTO, user_id: UUID) -> ProcessoCAR:
        processo = ProcessoCAR.criar(requerente_id=user_id, imovel_id=dto.imovel_id)
        return await self.repo.save(processo)

class SubmeterProcessoUseCase:
    async def execute(self, processo_id: UUID, user_id: UUID) -> ProcessoCAR:
        processo = await self.repo.find_by_id(processo_id)
        processo.submeter(user_id)  # Domínio valida
        return await self.repo.save(processo)

# QUERIES — direto no banco, sem passar pelo domínio
class ProcessosQueryService:
    async def listar_para_analista(
        self, filtros: FiltrosAnalista, cursor: Optional[str] = None
    ) -> tuple[List[ProcessoDashboardDTO], Optional[str]]:
        # Query SQL otimizada diretamente na view vw_processos_dashboard
        # Sem carregar agregados completos — apenas DTOs de leitura
        query = """
            SELECT * FROM vw_processos_dashboard
            WHERE status = ANY(:statuses) AND deleted_at IS NULL
            ORDER BY prioridade DESC, data_submissao_at ASC
            LIMIT :limit
        """
        rows = await self.db.execute(query, {"statuses": filtros.statuses, "limit": 21})
        # ...
```

### Event-Driven Architecture

```
Exchange: car.events (topic)
│
├── routing: "processo.submetido.v1"
│   ├── Queue: processos.notificacao  → NotificaçãoWorker
│   ├── Queue: processos.analytics   → AnalyticsConsumer
│   └── Queue: processos.integracao  → IntegracaoWorker
│
├── routing: "documento.validado.v1"
│   ├── Queue: documentos.score      → ScoreCompletudeUpdater
│   └── Queue: documentos.notif      → NotificaçãoWorker
│
└── routing: "processo.aprovado.v1"
    ├── Queue: processos.sicar        → SICARIntegrationWorker
    └── Queue: processos.notif        → NotificaçãoWorker (email congratulations)
```

---

## 4. Arquitetura Física

### Kubernetes — Recursos em Produção

| Serviço | Réplicas Min | Réplicas Max | CPU Request | CPU Limit | Mem Request | Mem Limit | HPA |
|---|---|---|---|---|---|---|---|
| web-app | 2 | 10 | 100m | 500m | 128Mi | 512Mi | CPU > 70% |
| auth-service | 2 | 6 | 200m | 500m | 256Mi | 512Mi | CPU > 70% |
| process-service | 2 | 8 | 500m | 1000m | 512Mi | 1Gi | CPU > 70% |
| document-service | 2 | 6 | 500m | 2000m | 512Mi | 2Gi | Queue depth |
| ai-assistant | 2 | 8 | 500m | 2000m | 512Mi | 2Gi | Conn > 100 |
| document-worker | 2 | 10 | 1000m | 2000m | 1Gi | 4Gi | Queue depth |
| notification-worker | 2 | 4 | 200m | 500m | 256Mi | 512Mi | Queue depth |
| integration-worker | 2 | 4 | 200m | 500m | 256Mi | 512Mi | Queue depth |
| postgresql | 1 (primary) + 2 (replicas) | — | 2000m | 4000m | 4Gi | 8Gi | Manual |
| redis | 1 (master) + 2 (replicas) | — | 200m | 500m | 256Mi | 1Gi | Manual |
| rabbitmq | 3 nós (quorum) | — | 500m | 1000m | 512Mi | 2Gi | Manual |
| minio | 1 (dev) / 4 (prod erasure) | — | 500m | 1000m | 512Mi | 2Gi | Manual |

### Alta Disponibilidade

```
PostgreSQL (Patroni + pgBouncer):
  ┌─────────────────┐     Streaming Replication
  │  Primary (RW)   │──────────────────────────────┐
  └─────────────────┘                               │
           │                          ┌─────────────▼────────────┐
           │ Failover automático      │  Replica 1 (RO)          │
           │ (Patroni + etcd)         └──────────────────────────┘
           │                          ┌──────────────────────────┐
           │                          │  Replica 2 (RO)          │
           └──────────────────────────► pgBouncer (load balancer)│
                                      └──────────────────────────┘

RabbitMQ (3 nós — Quorum Queues):
  Node1 ←──── Raft Consensus ────► Node2 ←──────► Node3
  (quorum queues: replicadas em todos os 3 nós)

Redis (Sentinel — 1 master + 2 replicas):
  Sentinel1, Sentinel2, Sentinel3 monitoram
  Master → Replica1, Replica2 (replicação assíncrona)
  Failover automático em caso de falha do master
```

---

## 5. Observabilidade

### Métricas Prometheus (15 customizadas)

```python
from prometheus_client import Counter, Histogram, Gauge

# Processos
car_processos_criados_total = Counter(
    'car_processos_criados_total', 'Processos CAR criados')
car_processos_submetidos_total = Counter(
    'car_processos_submetidos_total', 'Processos CAR submetidos',
    labelnames=['municipio_uf', 'tipo_imovel'])
car_tempo_analise_horas = Histogram(
    'car_tempo_analise_horas', 'Tempo de análise em horas',
    buckets=[1, 8, 24, 48, 120, 240, 720])

# Documentos
car_ocr_duracao_segundos = Histogram(
    'car_ocr_duracao_segundos', 'Duração do OCR',
    labelnames=['engine', 'tipo_documento'],
    buckets=[1, 5, 15, 30, 60, 120])
car_documentos_por_status = Gauge(
    'car_documentos_por_status', 'Documentos por status',
    labelnames=['status'])

# LLM
car_llm_latencia_segundos = Histogram(
    'car_llm_latencia_segundos', 'Latência do LLM (primeiro token)',
    labelnames=['provider', 'modelo'],
    buckets=[0.5, 1, 2, 3, 5, 10])
car_llm_tokens_total = Counter(
    'car_llm_tokens_total', 'Tokens LLM consumidos',
    labelnames=['provider', 'tipo'])  # prompt / completion

# Integrações externas
car_integracao_latencia = Histogram(
    'car_integracao_latencia_segundos', 'Latência de integração externa',
    labelnames=['sistema'])
car_integracao_erros_total = Counter(
    'car_integracao_erros_total', 'Erros de integração externa',
    labelnames=['sistema', 'tipo_erro'])

# Sistema
car_fila_tamanho = Gauge(
    'car_fila_tamanho', 'Mensagens na fila RabbitMQ',
    labelnames=['fila'])
car_sessoes_ativas = Gauge('car_sessoes_ativas', 'Sessões JWT ativas')
car_processos_por_status = Gauge(
    'car_processos_por_status', 'Processos por status atual',
    labelnames=['status'])
```

### Alertas Críticos

| Alerta | Condição | Severidade | Canal |
|---|---|---|---|
| ProcessoServiceDown | up{job="process-service"} == 0 por 2min | Critical | PagerDuty + Slack |
| APILatencyHigh | histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2 | Warning | Slack |
| ErrorRateHigh | rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01 | Critical | PagerDuty |
| QueueBacklogHigh | car_fila_tamanho{fila="documento.ocr"} > 100 | Warning | Slack |
| OCRLatencyHigh | histogram_quantile(0.95, car_ocr_duracao_segundos_bucket) > 60 | Warning | Slack |
| LLMProviderDown | rate(car_llm_latencia_segundos_count[5m]) == 0 AND car_sessoes_ativas > 10 | Critical | Slack |
| DBConnectionPoolExhausted | pg_stat_activity_count > 90 | Critical | PagerDuty |
| DiskSpaceMinIO | minio_disk_storage_free_bytes / minio_disk_storage_total_bytes < 0.1 | Warning | Slack |
| DeadLetterQueueGrowing | rate(rabbitmq_queue_messages_total{queue=~"car.dlq.*"}[15m]) > 0 | Warning | Slack |
| CertificateExpiringSoon | probe_ssl_earliest_cert_expiry - time() < 604800 | Warning | Slack |

---

## 6. Diagrama de Sequência — Fluxo Principal

```
Cidadão    WebApp    Nginx     Auth     Process   AI       Document   PostgreSQL  RabbitMQ
   │          │        │        │        Service  Service  Service       │           │
   │ clica    │        │        │           │        │         │          │           │
   │ "Enviar  │        │        │           │        │         │          │           │
   │  Mensagem│        │        │           │        │         │          │           │
   │  ao IA"  │        │        │           │        │         │          │           │
   │─────────►│        │        │           │        │         │          │           │
   │          │─POST──►│        │           │        │         │          │           │
   │          │/api/v1 │        │           │        │         │          │           │
   │          │/assist.│        │           │        │         │          │           │
   │          │/mensag.│ rate   │           │        │         │          │           │
   │          │        │ limit  │           │        │         │          │           │
   │          │        │ check  │           │        │         │          │           │
   │          │        │───────►│ JWT       │        │         │          │           │
   │          │        │        │ validate  │        │         │          │           │
   │          │        │        │ RS256     │        │         │          │           │
   │          │        │        │ blacklist │        │         │          │           │
   │          │        │        │───────────────────►│         │          │           │
   │          │        │        │           │        │ classify│          │           │
   │          │        │        │           │        │ intenção│          │           │
   │          │        │        │           │        │ PII mask│          │           │
   │ SSE      │        │        │           │        │────────►LLM Cloud  │           │
   │ streaming│        │        │           │        │◄────────tokens     │           │
   │◄─────────│◄──text/│        │           │        │         │          │           │
   │ token a  │event-  │        │           │        │ save    │          │           │
   │ token    │stream  │        │           │        │ mensagem│──INSERT──►           │
   │          │        │        │           │        │◄────────│          │           │
   │          │        │        │           │        │ emit    │          │           │
   │          │        │        │           │        │ FeedbackColetado   │           │
   │          │        │        │           │        │─────────────────────────────PUBLISH
   │          │        │        │           │        │         │          │    mensagem│
   │          │        │        │           │        │         │          │    .regist │
   │ [done]   │        │        │           │        │         │          │           │
   │◄─────────│        │        │           │        │         │          │           │
```

---

## 7. Decisões de Integração por Sistema Externo

| Sistema | Protocolo | Fallback | Circuit Breaker | Cache TTL |
|---|---|---|---|---|
| Gov.br | OAuth2 OIDC | Modo manutenção (servidores) | Não aplicável (auth crítica) | JWT 1h (refresh 30d) |
| SICAR | REST (consulta) | Dados em cache + flag "sem SICAR" | 5 falhas/60s → 30s open | 24 horas |
| SIGEF | REST | Processo avança sem dados SIGEF | 3 falhas/30s → 60s open | 24 horas |
| IBAMA | REST | Score de risco marcado como "não verificado" | 3 falhas/30s → 60s open | 6 horas |
| MapBiomas | REST | Bioma não preenchido automaticamente | 3 falhas/60s → 120s open | 7 dias |
| LLM (OpenAI/Claude) | HTTPS REST | Fallback para Ollama local | 3 timeouts/60s → 30s open | Semântico Redis |
| Ollama (local) | HTTP REST | Mensagem de indisponibilidade + retry | N/A (local) | Sem cache |
