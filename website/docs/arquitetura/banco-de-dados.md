---
sidebar_position: 3
title: Banco de Dados
description: PostgreSQL 16 + PostGIS + pgvector — schema, extensões e decisões de modelo.
tags: [engenharia, banco-de-dados, postgresql, postgis, pgvector]
---

# Banco de Dados

:::info Para quem é esta página
Engenheiros back-end e DBAs. Para a decisão de escolher PostgreSQL, veja [ADR-002](./decisoes/adr-002-postgresql.md).
:::

## Stack

| Extensão | Uso |
|---|---|
| **PostGIS 3.4** | Geometrias de imóveis rurais (SRID 4674 — SIRGAS 2000) |
| **pgvector** | Embeddings do RAG (1536 dimensões — OpenAI text-embedding-3-small) |
| **pgcrypto** | Criptografia de CPF e e-mail em repouso (conformidade LGPD) |
| **uuid-ossp** | Geração de UUIDs no banco (`gen_random_uuid()`) |

## Principais Tabelas

| Tabela | Descrição |
|---|---|
| `users` | Usuários — CPF e e-mail criptografados com pgcrypto |
| `imoveis_rurais` | Imóveis com geometria GEOMETRY(MULTIPOLYGON, 4674) |
| `processos_car` | Ciclo de vida do processo — índice por status + prioridade |
| `documentos` | Metadados dos arquivos + resultado do OCR em JSONB |
| `pendencias` | Pendências por processo |
| `historico_processos` | Auditoria imutável — particionado por mês |
| `canal_vinculos` | Vinculação de canal de mensageria (futuro/opcional) — identificador como hash SHA-256 |
| `knowledge_base` | Chunks de documentos normativos + embedding (pgvector) |
| `outbox` | Fila de eventos de domínio a publicar no RabbitMQ |
| `audit_logs` | Audit log genérico — particionado por mês |

## Princípios do Modelo

- **UUIDs como PKs** — gerados pelo banco (`gen_random_uuid()`)
- **Soft delete** — `deleted_at TIMESTAMPTZ` nullable em tabelas de negócio
- **Auditoria universal** — `created_at` + `updated_at` em todas as tabelas
- **Tabelas imutáveis** — `historico_processos` e `audit_logs` só aceitam INSERT
- **Particionamento** — `historico_processos` e `audit_logs` particionados por `RANGE(created_at)` mensal

## Consultas Geoespaciais

```sql
-- Processos cujo imóvel intersecta uma área de alerta
SELECT p.id, p.numero_car
FROM processos_car p
JOIN imoveis_rurais ir ON ir.id = p.imovel_id
WHERE ST_Intersects(
    ir.geometria,
    ST_GeomFromText('POLYGON((-44.0 -5.0, ...))', 4674)
);

-- Índice GiST obrigatório para performance
CREATE INDEX idx_imoveis_geometria ON imoveis_rurais USING GIST(geometria);
```

## Busca Semântica (pgvector)

```sql
-- Buscar chunks mais similares à query do usuário
SELECT conteudo, fonte, 1 - (embedding <=> $1) AS similaridade
FROM knowledge_base
ORDER BY embedding <=> $1
LIMIT 5;

-- Índice IVFFlat para performance
CREATE INDEX idx_kb_embedding ON knowledge_base
USING ivfflat(embedding vector_cosine_ops) WITH (lists = 100);
```

:::tip SRID 4674 — SIRGAS 2000
Sempre use SRID 4674 para dados geoespaciais brasileiros. É o padrão oficial do IBGE, SICAR e SIGEF. Usar SRID 4326 (WGS84) causa pequenas divergências nas medições de área.
:::

## Ver também

- [ADR-002 — PostgreSQL/PostGIS](./decisoes/adr-002-postgresql.md) — por que PostgreSQL
- [ADR-006 — IA](./decisoes/adr-006-ia.md) — por que pgvector em vez de Pinecone/Weaviate
- [Segurança — LGPD](../seguranca/lgpd.md) — como CPF e e-mail são protegidos
