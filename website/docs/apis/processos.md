---
sidebar_position: 3
title: Processos CAR
description: Endpoints para criação, submissão, consulta e gerenciamento de processos CAR.
tags: [engenharia, api, processos]
---

# API — Processos CAR

:::info Para quem é esta página
Engenheiros back-end e front-end. Para o modelo de domínio, veja [Agregados](../dominio/agregados.md).
:::

## Endpoints

| Método | Path | Descrição | Auth |
|---|---|---|---|
| `GET` | `/api/v1/processos` | Listar processos (paginado) | JWT |
| `POST` | `/api/v1/processos` | Criar processo | JWT (prata+) |
| `GET` | `/api/v1/processos/{id}` | Buscar processo por ID | JWT |
| `PATCH` | `/api/v1/processos/{id}` | Atualizar rascunho | JWT |
| `POST` | `/api/v1/processos/{id}/submeter` | Submeter para análise | JWT (prata+) |
| `POST` | `/api/v1/processos/{id}/cancelar` | Cancelar processo | JWT |
| `GET` | `/api/v1/processos/{id}/historico` | Linha do tempo | JWT |
| `GET` | `/api/v1/processos/{id}/pendencias` | Listar pendências | JWT |
| `POST` | `/api/v1/processos/{id}/pendencias/{pid}/responder` | Responder pendência | JWT |

## Ciclo de Status

```
rascunho → em_preenchimento → submetido → em_analise
                                              ↓         ↓
                                          pendente   aprovado
                                              ↓
                                        em_correcao → em_analise
                                                          ↓
                                                      rejeitado → recurso
```

## Submeter Processo — Pré-condições

Para que `POST /api/v1/processos/{id}/submeter` funcione:
- Processo deve estar em `rascunho` ou `em_preenchimento`
- Deve haver ao menos um documento `matricula_imovel` com status `valido`
- Deve haver ao menos um documento `ccir` com status `valido`
- Geometria do imóvel deve estar definida

:::tip Idempotência na submissão
Use o header `Idempotency-Key` para evitar submissões duplicadas em caso de timeout de rede.
:::

## Filtros na Listagem

```
GET /api/v1/processos?status=submetido,em_analise&municipio_ibge=2111300&page_size=20
```

Produtores só veem seus próprios processos. Analistas e acima veem todos.
