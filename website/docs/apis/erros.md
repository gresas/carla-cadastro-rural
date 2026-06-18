---
sidebar_position: 8
title: Tratamento de Erros
description: Tabela completa de códigos de erro CAR-XXX com status HTTP e contexto.
tags: [engenharia, api, erros]
---

# Tratamento de Erros

:::info Para quem é esta página
Engenheiros front-end e back-end. Use esta tabela para implementar mensagens de erro na UI.
:::

## Tabela de Códigos de Erro

| Código | HTTP | Mensagem | Quando ocorre |
|---|---|---|---|
| `CAR-001` | 401 | Não autenticado | Token ausente ou inválido |
| `CAR-002` | 403 | Acesso negado | Sem permissão de role para o endpoint |
| `CAR-003` | 404 | Recurso não encontrado | ID inválido ou sem acesso (inclui 403 disfarçado) |
| `CAR-004` | 422 | Dados inválidos | Falha de validação Pydantic |
| `CAR-005` | 413 | Arquivo muito grande | Acima de 50MB |
| `CAR-006` | 415 | Tipo não suportado | MIME type não aceito |
| `CAR-007` | 409 | Documento duplicado | Hash SHA-256 já existe |
| `CAR-008` | 409 | Conflito de estado | Ex: submeter processo já submetido |
| `CAR-010` | 400 | CPF inválido | Formato ou dígitos verificadores inválidos |
| `CAR-011` | 400 | Authorization code expirado | Callback OAuth2 tardio |
| `CAR-012` | 503 | Gov.br indisponível | Timeout na integração |
| `CAR-020` | 422 | Geometria inválida | Polígono não fecha ou auto-intersecção |
| `CAR-021` | 422 | Município não encontrado | Código IBGE inválido |
| `CAR-030` | 503 | Assistente indisponível | LLM offline |
| `CAR-040` | 503 | Sistema externo indisponível | SICAR/SIGEF timeout |
| `CAR-050` | 429 | Rate limit excedido | Muitas requisições |
| `CAR-060` | 409 | Processo não pode ser submetido | Documentação incompleta |
| `CAR-070` | 500 | Erro interno | Exceção não tratada |

## Formato do Erro

```json
{
  "error": {
    "code": "CAR-004",
    "message": "Dados de entrada inválidos",
    "details": [
      {
        "field": "municipio_ibge",
        "code": "invalid_format",
        "message": "Deve ter exatamente 7 dígitos numéricos"
      }
    ]
  }
}
```

:::tip Para front-end
Use `error.code` (não `error.message`) para lógica condicional. A mensagem pode ser traduzida ou personalizada para o usuário — o código é estável.
:::

## Erros Comuns no Fluxo de Upload

| Situação | Código | O que mostrar ao usuário |
|---|---|---|
| Arquivo > 50MB | `CAR-005` | "O arquivo é muito grande. Limite: 50MB." |
| PDF corrompido | `CAR-006` | "Este arquivo não pode ser lido. Tente enviar novamente." |
| Mesmo doc duas vezes | `CAR-007` | "Este documento já foi enviado anteriormente." |
| Conexão perdida | Timeout | "Conexão interrompida. O upload será reiniciado." |
