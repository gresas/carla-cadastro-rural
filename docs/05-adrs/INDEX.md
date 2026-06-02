# ADRs — Architecture Decision Records

**Projeto:** CARla  
**Última atualização:** 2026-06-01

---

## Índice de Decisões

| ID | Título | Status | Data | Área Afetada |
|---|---|---|---|---|
| [ADR-001](ADR-001-fastapi.md) | Uso de FastAPI como Framework Web Python | Aceito | 2026-06-01 | Backend — todos os serviços |
| [ADR-002](ADR-002-postgresql-postgis.md) | PostgreSQL com PostGIS como Banco de Dados Principal | Aceito | 2026-06-01 | Persistência |
| [ADR-003](ADR-003-event-driven.md) | Arquitetura Orientada a Eventos (EDA) | Aceito | 2026-06-01 | Arquitetura de comunicação |
| [ADR-004](ADR-004-mensageria-rabbitmq.md) | RabbitMQ como Message Broker | Aceito | 2026-06-01 | Infraestrutura de mensageria |
| [ADR-005](ADR-005-autenticacao-govbr.md) | Autenticação via Gov.br com OAuth2/OIDC | Aceito | 2026-06-01 | Identidade e acesso |
| [ADR-006](ADR-006-estrategia-ia.md) | Estratégia de IA — LLM Agnóstico com Adapter Pattern | Aceito | 2026-06-01 | BC Assistência Inteligente |

---

## Como Criar um Novo ADR

### Template

```markdown
# ADR-XXX: Título Descritivo

**Status:** Proposto | Em Discussão | Aceito | Substituído por ADR-YYY | Obsoleto
**Data:** YYYY-MM-DD
**Contexto:** [Área do sistema afetada]

---

## Contexto

[Descreva o problema, forças em conflito, requisitos e restrições que levaram à necessidade desta decisão]

## Decisão

[Descreva a decisão tomada, com exemplos de código quando relevante]

## Consequências

### Positivas
- [...]

### Negativas
- [...]

### Riscos
- [...]

## Alternativas Consideradas

| Alternativa | Prós | Contras | Motivo da Rejeição |

## Referências

- [...]
```

### Processo de Decisão

1. **Propor:** Crie o arquivo ADR-XXX-titulo.md com status "Proposto"
2. **Discutir:** Abra PR para review da equipe. Use o PR para debater
3. **Decidir:** Tech Lead ou arquiteto aprova com status "Aceito" ou "Rejeitado"
4. **Registrar:** Merge do PR. ADR é imutável após aceito
5. **Substituir:** Se a decisão mudar, crie novo ADR e marque o antigo como "Substituído por ADR-XXX"

### Quando Criar um ADR

Crie um ADR quando a decisão:
- Envolve tecnologia ou framework que afeta múltiplos serviços
- Tem implicações de segurança ou conformidade
- Tem trade-offs significativos que precisam ser documentados
- Pode ser questionada no futuro ("por que fizemos assim?")
- Envolve rejeitar uma alternativa popular

**Não** crie ADR para decisões triviais (ex: qual biblioteca de logging usar internamente em um serviço).

---

## Sumário de Decisões Técnicas

| Área | Decisão | ADR |
|---|---|---|
| Framework API | FastAPI 0.115+ | ADR-001 |
| Banco de dados principal | PostgreSQL 16 + PostGIS 3.4 | ADR-002 |
| Vector store | pgvector (extensão PostgreSQL) | ADR-002 |
| ORM | SQLAlchemy 2.0 async + GeoAlchemy2 | ADR-002 |
| Padrão de comunicação | Event-Driven Architecture | ADR-003 |
| Garantia de entrega de eventos | Outbox Pattern | ADR-003 |
| Message broker | RabbitMQ 3.13 | ADR-004 |
| Autenticação cidadão | Gov.br OAuth2 OIDC + PKCE | ADR-005 |
| Token interno | JWT RS256 | ADR-005 |
| LLM principal | Anthropic Claude (configurável) | ADR-006 |
| LLM para dados sensíveis | Ollama (local) | ADR-006 |
| RAG knowledge base | pgvector + normativos CAR | ADR-006 |
| Migrations | Alembic | — |
| Cache | Redis 7 | — |
| Object storage | MinIO (S3-compatible) | — |
| Containerização | Docker + Kubernetes | — |
| Observabilidade | OpenTelemetry + Prometheus + Grafana | — |
