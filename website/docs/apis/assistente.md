---
sidebar_position: 5
title: Assistente IA
description: Chat conversacional com SSE streaming, histórico de conversas e escalonamento humano.
tags: [engenharia, api, assistente, sse, streaming]
---

# API — Assistente IA

:::info Para quem é esta página
Engenheiros front-end e back-end. Para estratégia de IA, veja [Arquitetura — IA](../arquitetura/ia.md).
:::

## Endpoints

| Método | Path | Descrição |
|---|---|---|
| `POST` | `/api/v1/assistente/conversas` | Iniciar conversa (com ou sem contexto de processo) |
| `POST` | `/api/v1/assistente/conversas/{id}/mensagens` | Enviar mensagem — **resposta via SSE** |
| `GET` | `/api/v1/assistente/conversas/{id}` | Buscar conversa |
| `GET` | `/api/v1/assistente/conversas/{id}/mensagens` | Histórico |
| `POST` | `/api/v1/assistente/conversas/{id}/encerrar` | Encerrar conversa |
| `GET` | `/api/v1/assistente/conversas` | Histórico do usuário |

## SSE — Server-Sent Events

A resposta do assistente é transmitida token a token via SSE:

```javascript
// Cliente JavaScript
const source = new EventSource('/api/v1/assistente/conversas/{id}/mensagens', {
  headers: { Authorization: `Bearer ${token}` }
});

source.addEventListener('token', (e) => {
  const { content } = JSON.parse(e.data);
  appendToChat(content);  // adiciona token a token na UI
});

source.addEventListener('done', (e) => {
  const { message_id, tokens_prompt, latencia_ms } = JSON.parse(e.data);
  source.close();
});

source.addEventListener('error', (e) => {
  const { code, message } = JSON.parse(e.data);
  showError(message);
  source.close();
});
```

**Eventos SSE:**

| Evento | Dados | Quando |
|---|---|---|
| `token` | `{ "content": "texto parcial" }` | A cada token gerado |
| `done` | `{ "message_id", "tokens_prompt", "tokens_completion", "latencia_ms" }` | Geração concluída |
| `error` | `{ "code": "CAR-030", "message": "..." }` | Erro durante geração |
| `heartbeat` | `{}` | A cada 15s para manter conexão |

:::tip Configuração de servidor
Ao usar SSE, configure o Nginx para não fazer buffer da resposta:
```nginx
proxy_buffering off;
X-Accel-Buffering: no;
```
:::

## Iniciar Conversa com Contexto do Processo

```json
POST /api/v1/assistente/conversas
{
  "processo_id": "uuid-do-processo-ativo"
}
```

Com `processo_id`, o assistente tem acesso ao status, documentos e pendências do processo e pode dar respostas personalizadas como _"Seu documento de matrícula foi validado, mas ainda falta o CCIR."_

## Escalonamento Humano

Quando o assistente detecta frustração ou pergunta fora do domínio, publica evento `EscalonamentoTriggered` que notifica o analista responsável. O usuário recebe: _"Vou conectar você com um analista. Aguarde."_
