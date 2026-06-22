---
sidebar_position: 5
title: Integração com Mensageria (Futuro)
description: Documentação do fluxo de integração com apps de mensageria — escopo futuro, não faz parte do MVP.
tags: [design, ux, fluxo, mensageria, futuro]
---

# Integração com Apps de Mensageria

:::caution Escopo Futuro — Fora do MVP
Esta documentação descreve uma integração prevista para versões posteriores ao MVP. A Carla não depende de WhatsApp, Telegram ou qualquer app de mensageria para funcionar. O canal core é a **interface web própria**, acessível via `car.gov.br`.

Para o fluxo atual de abertura da Carla, veja [Abertura da Carla](./abertura-carla.md).
Para a decisão arquitetural, veja [ADR-008: Canal Web Próprio](../../arquitetura/decisoes/adr-008-canal-web-proprio.md).
:::

## Conceito

A integração com apps de mensageria (WhatsApp, Telegram etc.) será implementada futuramente como um **adapter desacoplado** — um serviço independente que recebe webhooks do app de mensageria, traduz as mensagens para o protocolo interno da Carla e repassa para o mesmo backend de conversas do canal web.

O backend de conversas **não muda** — apenas ganha uma nova entrada de canal.

```
WhatsApp / Telegram
  └─→ Webhook Adapter (serviço desacoplado)
        └─→ Mesmo backend de conversas do canal web
              └─→ Resposta traduzida de volta para o canal de origem
```

## O que será possível via mensageria (quando implementado)

| Funcionalidade | Via mensageria | Motivo |
|---|---|---|
| Tirar dúvidas sobre CAR | ✅ Sim | Canal de baixa barreira |
| Consultar status do processo | ✅ Sim | Leitura, sem risco |
| Receber notificações de pendência | ✅ Sim | Canal de conveniência |
| Criar processo CAR completo | ❌ Não | Exige confirmação em tela cheia |
| Upload de documentos (formal) | ❌ Não | Ato jurídico — exige interface web |
| Submeter processo | ❌ Não | Exige revisão e confirmação formal |

## Referências

- [ADR-007: Provider WhatsApp (Superada)](../../arquitetura/decisoes/adr-007-whatsapp.md) — decisão anterior, já superada
- [ADR-008: Canal Web Próprio](../../arquitetura/decisoes/adr-008-canal-web-proprio.md) — decisão vigente
- [UC-013: Integração com Mensageria (Futuro)](../../produto/casos-de-uso.md) — caso de uso formal
