---
sidebar_position: 1
title: Princípios das APIs
description: Convenções REST, envelope de resposta, paginação cursor-based e códigos de erro.
tags: [engenharia, api, rest, paginação]
---

# Princípios das APIs

:::info Para quem é esta página
Engenheiros back-end e front-end. Para endpoints específicos, use o menu lateral.
:::

## Convenções Gerais

- **Versioning:** prefixo `/api/v1/`
- **Autenticação:** `Authorization: Bearer {JWT}` em todas as rotas protegidas
- **Content-Type:** `application/json`
- **Datas:** ISO 8601 com timezone UTC (`2026-01-15T10:30:00Z`)
- **IDs:** UUIDs v4 em todos os recursos

## Envelope de Resposta

### Recurso único
```json
{
  "data": { "id": "...", "status": "rascunho" },
  "meta": { "request_id": "uuid", "timestamp": "2026-01-15T10:30:00Z" }
}
```

### Lista paginada
```json
{
  "data": [...],
  "meta": {
    "cursor_next": "opaque-cursor",
    "cursor_prev": null,
    "total_count": 150,
    "has_more": true,
    "page_size": 20
  }
}
```

### Erro
```json
{
  "error": {
    "code": "CAR-004",
    "message": "Dados de entrada inválidos",
    "details": [
      { "field": "municipio_ibge", "code": "invalid_format", "message": "Deve ter 7 dígitos" }
    ]
  }
}
```

## Paginação Cursor-Based

:::tip Por que cursor em vez de offset?
Paginação com `OFFSET` é instável — novos registros mudam a posição dos itens. Cursor-based é estável e mais performática para tabelas grandes.
:::

```
GET /api/v1/processos?page_size=20
→ meta.cursor_next = "eyJpZCI6IjU1MGU4..."

GET /api/v1/processos?page_size=20&cursor=eyJpZCI6IjU1MGU4...
→ próxima página
```

## Rate Limiting

| Role | Geral | Upload | Assistente |
|---|---|---|---|
| Produtor Rural | 60 req/min | 5 req/min | 20 req/min |
| Consultor | 120 req/min | 15 req/min | 20 req/min |
| Analista | 200 req/min | 30 req/min | 20 req/min |
| Admin | sem limite | sem limite | sem limite |

Headers de resposta: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Idempotência

Operações críticas e irreversíveis aceitam o header `Idempotency-Key`:

```
POST /api/v1/processos/{id}/submeter
Idempotency-Key: meu-key-unico-123
```

Mesma key com mesma requisição retorna o mesmo resultado sem executar duas vezes.

## Ver também

- [Autenticação e JWT](./autenticacao.md)
- [Erros — Tabela completa](./erros.md)
- [ADR-001 — FastAPI](../arquitetura/decisoes/adr-001-fastapi.md)
