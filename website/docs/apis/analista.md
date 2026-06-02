---
sidebar_position: 6
title: Portal do Analista
description: Endpoints da fila de processos, dossiê automático, aprovação e rejeição.
tags: [engenharia, api, analista]
---

# API — Portal do Analista

:::info Para quem é esta página
Engenheiros back-end. Para o fluxo UX, veja [Fluxo do Analista](../design/fluxos/analista.md).
:::

## Endpoints

| Método | Path | Descrição | Auth mínima |
|---|---|---|---|
| `GET` | `/api/v1/analista/processos` | Fila de processos com filtros e ordenação | Analista |
| `POST` | `/api/v1/analista/processos/{id}/assumir` | Assumir processo para análise | Analista |
| `POST` | `/api/v1/analista/processos/{id}/aprovar` | Aprovar processo | Analista |
| `POST` | `/api/v1/analista/processos/{id}/rejeitar` | Rejeitar processo com motivo obrigatório | Analista |
| `POST` | `/api/v1/analista/processos/{id}/criar-pendencia` | Criar pendência manual | Analista |
| `POST` | `/api/v1/analista/processos/{id}/gerar-dossie` | Iniciar geração de dossiê PDF (async) | Analista |
| `GET` | `/api/v1/analista/dossies/{job_id}` | Status do dossiê em geração | Analista |
| `GET` | `/api/v1/analista/dossies/{job_id}/download` | Download do PDF gerado | Analista |
| `GET` | `/api/v1/analista/dashboard` | Métricas de produtividade | Analista |

## Fila de Processos

```
GET /api/v1/analista/processos?status=submetido,em_analise&prioridade=alta&page_size=20
```

Cada item da fila inclui: `score_completude`, `score_risco`, `tempo_em_analise`, `total_documentos`, `pendencias_abertas`.

## Rejeição — Campos Obrigatórios

```json
POST /api/v1/analista/processos/{id}/rejeitar
{
  "motivo": "Área declarada diverge em 15% da matrícula apresentada.",
  "codigo_motivo": "AREA_DIVERGENTE"
}
```

Códigos de motivo padronizados: `DOCUMENTACAO_INSUFICIENTE`, `AREA_DIVERGENTE`, `GEOMETRIA_INVALIDA`, `DADO_INCONSISTENTE`, `OUTRO`.

## Dossiê PDF (Assíncrono)

```
POST /api/v1/analista/processos/{id}/gerar-dossie
→ 202: { "job_id": "uuid", "status": "processando" }

GET /api/v1/analista/dossies/{job_id}
→ { "status": "processando" | "pronto" | "falhou" }

GET /api/v1/analista/dossies/{job_id}/download
→ Binary PDF (quando status = "pronto")
```

:::note Geração automática
O dossiê é gerado automaticamente quando o analista assume o processo (`POST /assumir`). O endpoint `/gerar-dossie` é para regenerar manualmente quando necessário.
:::
