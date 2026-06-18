---
sidebar_position: 3
title: "ADR-002: PostgreSQL + PostGIS"
description: Por que escolhemos PostgreSQL com PostGIS para armazenar dados geoespaciais do CAR.
tags: [adr, postgresql, postgis, banco-de-dados]
---

# ADR-002: PostgreSQL + PostGIS como Banco Principal

**Status:** Aceito | **Data:** 2026-06-01

## Contexto

O CAR envolve dados geoespaciais (polígonos de imóveis rurais, APPs, Reserva Legal). Precisamos de:
- ACID completo para processos jurídicos
- Funções espaciais nativas (`ST_Intersects`, `ST_Area`, `ST_Distance`)
- Busca vetorial para RAG do assistente (embeddings)
- Criptografia em repouso para conformidade LGPD

## Decisão

**PostgreSQL 16** com extensões: PostGIS 3.4, pgvector, pgcrypto, uuid-ossp.

**SRID padrão:** 4674 (SIRGAS 2000) — padrão brasileiro oficial.

## Consequências

✅ Padrão da indústria para geodados governamentais brasileiros  
✅ QGIS integra nativamente — analistas podem visualizar geometrias  
✅ pgvector elimina a necessidade de um vector store externo  
✅ pgcrypto para conformidade LGPD sem infraestrutura adicional  
❌ Escalabilidade horizontal limitada (escala melhor verticalmente)  
❌ DBA especializado em PostGIS necessário em produção

## Alternativas Rejeitadas

| Alternativa | Motivo |
|---|---|
| MongoDB + GeoJSON | Sem ACID; suporte espacial inferior ao PostGIS |
| MySQL Spatial | Funções geoespaciais muito limitadas |
| CockroachDB | Suporte PostGIS incipiente e instável |
