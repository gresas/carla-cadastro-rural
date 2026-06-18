---
sidebar_position: 5
title: Testes de Carga
description: k6 — cenários de carga, thresholds e interpretação de resultados.
tags: [engenharia, testes, carga, k6, performance]
---

# Testes de Carga com k6

:::info Para quem é esta página
Engenheiros de plataforma e QA de performance.
:::

## Cenário de Carga Normal

```javascript
// tests/load/normal_load.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // ramp up para 50 usuários
    { duration: '5m', target: 50 },   // sustain
    { duration: '2m', target: 100 },  // pico
    { duration: '5m', target: 100 },  // sustain no pico
    { duration: '2m', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(50)<200', 'p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
  },
};
```

## Thresholds de Aceitação

| Endpoint | p50 | p95 | p99 | Max erros |
|---|---|---|---|---|
| `GET /api/v1/processos` | 100ms | 300ms | 500ms | 0,1% |
| `POST /api/v1/processos` | 200ms | 500ms | 1000ms | 0,1% |
| `POST /upload` | 500ms | 2000ms | 5000ms | 1% |
| Assistente IA (1º token) | 1000ms | 3000ms | 6000ms | 2% |

:::warning Assistente IA tem limites mais altos
O LLM introduz latência intrínseca de 1–3s para o primeiro token. Testes de carga do assistente medem separadamente e com thresholds adaptados.
:::

## Outros Cenários

| Cenário | Objetivo |
|---|---|
| **Spike test** | 0 → 300 usuários em 30s — como o sistema reage a picos súbitos |
| **Soak test** | 50 usuários por 1h — detectar memory leaks e degradação progressiva |
| **Stress test** | Escalar até encontrar ponto de ruptura |

Executar testes de carga **apenas em staging** — nunca em produção.
