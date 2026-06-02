# ADR-002: PostgreSQL com PostGIS como Banco de Dados Principal

**Status:** Aceito  
**Data:** 2026-06-01  
**Contexto:** Persistência — todos os serviços

---

## Contexto

O CARla precisa armazenar e consultar dados de naturezas distintas:

1. **Dados geoespaciais:** Geometrias de imóveis rurais (polígonos/multipolígonos), APPs, Reserva Legal — precisamos de funções espaciais como `ST_Intersects`, `ST_Area`, `ST_Distance`, `ST_Contains`, `ST_Buffer`.
2. **Dados relacionais:** Processos, usuários, documentos, pendências — com ACID, FKs, transações.
3. **Dados vetoriais:** Embeddings do RAG do assistente IA (dimensão 1536) para busca semântica.
4. **Dados JSON dinâmicos:** Metadados de integração, dados extraídos de OCR, configurações.
5. **Dados criptografados:** CPF, email — conformidade LGPD.

O padrão brasileiro para georreferenciamento é SIRGAS 2000 (SRID 4674). O SICAR e SIGEF utilizam esse SRID. O QGIS (ferramenta dos analistas) tem integração nativa com PostGIS.

---

## Decisão

**Adotar PostgreSQL 16+ com as extensões:**
- `postgis` 3.4+ — tipos e funções geoespaciais
- `pgvector` — embeddings para RAG (1536 dimensões)
- `pgcrypto` — criptografia de dados pessoais (CPF, email)
- `uuid-ossp` — geração de UUIDs

**ORM:** SQLAlchemy 2.0 com `async` + GeoAlchemy2 para tipos geoespaciais  
**Migrations:** Alembic com suporte a DDL geoespacial  
**SRID padrão:** 4674 (SIRGAS 2000)

```sql
-- Exemplo de uso de funções espaciais
SELECT p.id, p.numero_car, ST_Area(ir.geometria::geography) / 10000 AS area_ha
FROM processos_car p
JOIN imoveis_rurais ir ON ir.id = p.imovel_id
WHERE ST_Intersects(
    ir.geometria,
    ST_GeomFromText('POLYGON((-44.0 -5.0, -43.0 -5.0, -43.0 -4.0, -44.0 -4.0, -44.0 -5.0))', 4674)
);

-- Índice GIST para performance em consultas espaciais
CREATE INDEX idx_imoveis_geometria ON imoveis_rurais USING GIST(geometria);

-- pgvector para busca semântica no RAG
CREATE INDEX idx_kb_embedding ON knowledge_base
USING ivfflat(embedding vector_cosine_ops) WITH (lists = 100);
```

---

## Consequências

### Positivas
- **Padrão da indústria para geodados governamentais brasileiros** — compatível com QGIS, SICAR, SIGEF
- **ACID completo** — garantias transacionais para processos CAR (crítico para auditoria)
- **PostGIS maturo** — 20+ anos de desenvolvimento, funções espaciais abrangentes
- **pgvector integrado** — RAG sem sistema externo de vector store
- **pgcrypto** — conformidade LGPD sem infraestrutura adicional
- **JSONB** — campos dinâmicos (metadados OCR, configurações) sem schema rígido
- **Particionamento nativo** — tabelas de auditoria e histórico particionadas por mês

### Negativas
- **Complexidade operacional:** PostGIS requer expertise especializada para tuning e backup
- **Escala horizontal limitada:** PostgreSQL escala melhor verticalmente; sharding é complexo
- **DBA geoespacial necessário:** Em produção real, requer profissional com expertise em PostGIS

### Riscos
- Versões de PostGIS podem ter bugs em funções espaciais específicas — manter atualizado
- pgvector em produção com alta concorrência requer tuning de `maintenance_work_mem` e `max_parallel_workers`

---

## Alternativas Consideradas

| Alternativa | Prós | Contras | Motivo da Rejeição |
|---|---|---|---|
| **MongoDB + GeoJSON** | Schema flexível, escala horizontal | Sem ACID completo, suporte espacial inferior ao PostGIS, sem pgvector | Conformidade ACID obrigatória para processos CAR |
| **MySQL Spatial** | Mais simples operacionalmente | Funções espaciais muito limitadas vs. PostGIS; sem pgvector | PostGIS muito superior em funcionalidade geoespacial |
| **CockroachDB** | Escala horizontal nativa, PostgreSQL-compatible | Suporte PostGIS incipiente e instável, latência maior | Compatibilidade PostGIS insuficiente |
| **Oracle Spatial** | Maduro, padrão em alguns órgãos | Custo de licença inviável para projeto open-source; vendor lock-in | Custo e filosofia open-source incompatíveis |
| **Neo4j (graph)** | Relações complexas entre entidades | Não é adequado como banco principal; sem suporte geoespacial nativo | Caso de uso principal não é graph |

---

## Referências

- [PostGIS Documentation](https://postgis.net/documentation/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/)
- [SIRGAS 2000 — IBGE](https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/sirgas)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
