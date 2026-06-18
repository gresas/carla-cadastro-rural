---
sidebar_position: 7
title: WhatsApp
description: Webhook Meta, fluxo de vinculação Gov.br e envio de mensagens ativas.
tags: [engenharia, api, whatsapp, webhook]
---

# API — Canal WhatsApp

:::info Para quem é esta página
Engenheiros back-end. Para o fluxo UX, veja [Fluxo WhatsApp](../design/fluxos/whatsapp.md). Para contexto arquitetural, veja [ADR-005](../arquitetura/decisoes/adr-005-govbr.md).
:::

## Fluxo de Vinculação

O WhatsApp não suporta OAuth2. A autenticação usa um link temporário como "ponte":

```mermaid
sequenceDiagram
    participant B as Bot (WhatsApp)
    participant A as CARla API
    participant R as Redis
    participant G as Gov.br

    B->>A: POST /vincular/solicitar {number_hash}
    A->>R: SET wpp:token:{token} → number_hash (TTL 10min)
    A-->>B: { link: "carla.gov.br/auth/wpp?token=XYZ" }
    B->>B: Envia link ao usuário

    Note over B,G: Usuário abre no browser
    G-->>A: GET /vincular/callback?token=XYZ&code=...
    A->>G: Troca code por claims Gov.br
    A->>R: SET wpp:session:{number_hash} → user_id (TTL 30d)
    A->>A: Salva em canal_vinculos
    A-->>B: 302 → página de confirmação
```

## Endpoints

| Método | Path | Descrição | Auth |
|---|---|---|---|
| `POST` | `/api/v1/whatsapp/vincular/solicitar` | Gera token de vinculação | API Key interna |
| `GET` | `/api/v1/whatsapp/vincular/callback` | Callback Gov.br — vincula número | Pública (redirect_uri) |
| `POST` | `/api/v1/whatsapp/webhook` | Recebe mensagens da Meta | HMAC-SHA256 |
| `GET` | `/api/v1/whatsapp/webhook` | Challenge de verificação Meta | Pública |
| `POST` | `/api/v1/whatsapp/mensagem` | Envia mensagem ativa | API Key interna |
| `DELETE` | `/api/v1/whatsapp/vincular` | Desvincula número (LGPD) | JWT |

## Webhook Meta — Validação de Assinatura

```python
import hmac, hashlib

def validar_assinatura(body: bytes, signature: str, app_secret: str) -> bool:
    expected = hmac.new(app_secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

:::warning Responda em < 20 segundos
A Meta considera o webhook como falha se não receber resposta em 20s. Toda a lógica de negócio deve ser assíncrona (publicar em fila e retornar `{}` imediatamente).
:::

## Provider Recomendado — Meta Cloud API

:::danger Não use APIs não oficiais
O CARla deve usar a **Meta Cloud API (WhatsApp Business Platform oficial)**. Z-API, UltraMsg e similares violam os ToS do Meta — contas são banidas sem aviso, o que interromperia toda a comunicação com cidadãos.

**Custo estimado (América Latina):**
- Conversa iniciada pelo negócio (proativa): ~U$ 0,05–0,06 / conversa de 24h
- Conversa iniciada pelo usuário: ~U$ 0,02–0,03 / conversa de 24h
- Para 10.000 processos ativos/mês com ~3 interações cada: estimar ~U$ 600–900/mês

**Configuração necessária:**
1. Conta Meta Business verificada
2. Número dedicado registrado no Meta
3. Templates de mensagem aprovados pelo Meta (obrigatório para mensagens proativas)
4. Credenciais: `WHATSAPP_PHONE_NUMBER_ID` e `WHATSAPP_ACCESS_TOKEN`
:::

## Privacidade — Número como Hash

O número de telefone **nunca é armazenado em claro**. Apenas o hash SHA-256:

```python
number_hash = hashlib.sha256(f"+5511999998888{APP_SALT}".encode()).hexdigest()
```

Isso atende ao princípio de **minimização de dados** da LGPD.

## Operações NÃO disponíveis pelo WhatsApp

Por serem atos jurídicos formais, estas operações exigem o portal web:

- Submissão de processo
- Upload de documentos
- Correção de pendências
- Aprovação/rejeição pelo analista
