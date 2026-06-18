---
sidebar_position: 2
title: "ADR-001: FastAPI"
description: Por que escolhemos FastAPI como framework web Python para o CARla.
tags: [adr, fastapi, python, engenharia]
---

# ADR-001: FastAPI como Framework Web Python

**Status:** Aceito | **Data:** 2026-06-01

## Contexto

Precisamos de um framework Python para as APIs REST do CARla. Requisitos:
- Suporte nativo a `async/await` (I/O intensivo: banco, LLM, integrações)
- Validação de dados com tipagem forte (alinhado com DDD — Pydantic v2)
- Documentação OpenAPI automática
- Performance adequada para 500+ usuários simultâneos

## Decisão

**FastAPI 0.115+** com Pydantic v2, Uvicorn e Gunicorn em produção.

## Consequências

✅ ~3–5x mais rápido que Django DRF em workloads I/O-bound  
✅ OpenAPI/Swagger gerado automaticamente  
✅ Integração nativa com Pydantic v2 — VOs do domínio são schemas direto  
✅ SSE nativo (`StreamingResponse`) para o assistente IA  
❌ Sem admin embutido (não necessário para APIs)  
❌ Curva de aprendizado em async para times acostumados com Django

## Alternativas Rejeitadas

| Alternativa | Motivo da rejeição |
|---|---|
| Django REST Framework | Síncrono por padrão; overhead desnecessário para APIs puras |
| Flask + marshmallow | Muito manual; sem OpenAPI automático |
| Litestar | Menos maduro; menor comunidade para projeto governamental |
