# CARla — Índice de Documentação

**Projeto:** CARla — Plataforma Inteligente para o Cadastro Ambiental Rural  
**Versão:** 1.0.0  
**Data:** 2026-06-01

---

## Documentos

| # | Documento | Arquivo | Descrição |
|---|---|---|---|
| 01 | Product Requirements Document | [PRD.md](01-prd/PRD.md) | Visão, objetivos, personas, casos de uso, requisitos, métricas e riscos |
| 02 | Event Storming | [EVENT_STORMING.md](02-event-storming/EVENT_STORMING.md) | Atores, comandos, eventos, bounded contexts e fluxos críticos |
| 03 | Domain-Driven Design | [DDD.md](03-ddd/DDD.md) | Contextos, entidades, value objects, agregados e serviços de domínio |
| 04 | Arquitetura | [ARQUITETURA.md](04-arquitetura/ARQUITETURA.md) | Modelo C4, lógica, física, CQRS, EDA e observabilidade |
| 05 | ADRs | [INDEX.md](05-adrs/INDEX.md) | Decisões arquiteturais registradas (6 ADRs) |
| 06 | Modelo de Dados | [MODELO_DADOS.md](06-modelo-dados/MODELO_DADOS.md) | DDL completo, índices, triggers, views e política LGPD |
| 07 | Design de APIs | [API_DESIGN.md](07-apis/API_DESIGN.md) | Endpoints REST, schemas Pydantic, SSE, rate limiting, erros |
| 08 | Segurança | [SEGURANCA.md](08-seguranca/SEGURANCA.md) | LGPD, RBAC, criptografia, OWASP Top 10, auditoria |
| 09 | Roadmap | [ROADMAP.md](09-roadmap/ROADMAP.md) | MVP Hackathon (2 semanas), MVP Produção (3 meses), Versão Escalável (12 meses) |
| 10 | Estrutura do Repositório | [ESTRUTURA.md](10-estrutura-repositorio/ESTRUTURA.md) | Árvore completa do projeto, convenções e quick start |
| 11 | Plano de Desenvolvimento | [PLANO_DEV.md](11-plano-desenvolvimento/PLANO_DEV.md) | Épicos, features, histórias (Gherkin), estimativas e cronograma |
| 12 | Estratégia de Testes | [TESTES.md](12-estrategia-testes/TESTES.md) | Unitários (pytest), integração, contrato (Pact), E2E (Playwright), carga (k6) |

---

## Links Rápidos — ADRs

| ADR | Decisão |
|---|---|
| [ADR-001](05-adrs/ADR-001-fastapi.md) | FastAPI como framework Python |
| [ADR-002](05-adrs/ADR-002-postgresql-postgis.md) | PostgreSQL + PostGIS como banco principal |
| [ADR-003](05-adrs/ADR-003-event-driven.md) | Arquitetura orientada a eventos (EDA) |
| [ADR-004](05-adrs/ADR-004-mensageria-rabbitmq.md) | RabbitMQ como message broker |
| [ADR-005](05-adrs/ADR-005-autenticacao-govbr.md) | Autenticação via Gov.br OAuth2/OIDC |
| [ADR-006](05-adrs/ADR-006-estrategia-ia.md) | LLM agnóstico com Adapter Pattern |

---

## Stack Tecnológica

| Área | Tecnologia |
|---|---|
| Backend | Python 3.13+, FastAPI 0.115+, Pydantic v2 |
| ORM | SQLAlchemy 2.0 async, GeoAlchemy2, Alembic |
| Banco | PostgreSQL 16, PostGIS 3.4, pgvector, pgcrypto |
| Mensageria | RabbitMQ 3.13 (Quorum Queues) |
| Cache | Redis 7 |
| Object Storage | MinIO (S3-compatible) |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Autenticação | Gov.br OAuth2/OIDC, JWT RS256 |
| IA | Claude (Anthropic), GPT-4o (OpenAI), Ollama (local) |
| Infraestrutura | Docker, Kubernetes, Kustomize |
| Observabilidade | OpenTelemetry, Prometheus, Grafana |
| CI/CD | GitHub Actions |
| Testes | pytest, TestContainers, Playwright, k6, Pact |
