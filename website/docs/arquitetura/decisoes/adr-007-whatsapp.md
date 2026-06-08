---
sidebar_position: 8
title: "ADR-007: Provider WhatsApp"
description: Por que escolhemos a Meta Cloud API em vez de Z-API ou Twilio para o canal WhatsApp.
tags: [adr, whatsapp, meta, integração]
---

# ADR-007: Meta Cloud API como Provider WhatsApp

**Status:** Aceito | **Data:** 2026-06-01

## Contexto

O canal WhatsApp é um diferencial central do CARla para alcançar cidadãos rurais. Para enviar e receber mensagens via WhatsApp, o sistema precisa de um provider. Existem três categorias de opções:

1. **Meta Cloud API** — a API oficial do Meta para WhatsApp Business
2. **APIs não oficiais** (Z-API, UltraMsg, Evolution API) — replicam o WhatsApp Web via engenharia reversa
3. **Intermediários oficiais (BSP)** (Twilio, Vonage, Infobip) — revendem acesso à Meta Cloud API

O projeto precisa de uma decisão explícita porque a escolha afeta conformidade jurídica, custo, estabilidade e aprovação para uso governamental.

## Decisão

**Meta Cloud API diretamente** via WhatsApp Business Platform.

- Acesso direto à API oficial do Meta via Facebook Developers
- Número de telefone dedicado registrado no Meta
- Templates de mensagem aprovados previamente pelo Meta (obrigatório para mensagens proativas)

## Justificativa

### Por que não usar APIs não oficiais (Z-API, UltraMsg)

APIs não oficiais funcionam simulando o WhatsApp Web — uma abordagem que:

- **Viola os Termos de Serviço do Meta** explicitamente
- Pode resultar em **banimento do número sem aviso** — todas as vinculações de cidadãos são perdidas imediatamente
- É **juridicamente questionável** para uso por órgão público: o governo estaria usando uma ferramenta que viola um contrato privado
- Não oferece SLA nem suporte formal

Para um sistema governamental que pode ter 10.000+ cidadãos dependendo do canal, o risco de banimento não é aceitável.

### Por que não usar Twilio (ou outro BSP)

Twilio e outros Business Solution Providers (BSPs) são intermediários que revendem acesso à Meta Cloud API. Isso implica:

- **Custo adicional** (markup sobre o preço Meta + taxa mensal da plataforma)
- **Camada extra de dependência** sem benefício técnico direto
- Para o volume esperado (< 1M mensagens/mês), o acesso direto à Meta Cloud API é suficiente

BSPs são justificados para empresas que precisam de suporte premium, múltiplos canais de mensagem (SMS, WhatsApp, RCS) ou integração com CRM proprietário — nenhum desses casos se aplica ao CARla.

## Consequências

✅ Conformidade total com os ToS do Meta — sem risco de banimento  
✅ SLA e suporte oficial do Meta  
✅ Aceitável juridicamente para uso governamental  
✅ Custo mais baixo vs. BSPs  
❌ Processo de aprovação do Meta (1–3 semanas para conta verificada)  
❌ Custo por conversa (~U$ 0,02–0,06 na América Latina) — precisa constar no modelo de sustentabilidade  
❌ Templates de mensagens proativas precisam de aprovação prévia (lead time de dias)

## Modelo de Custo Estimado

| Cenário | Volume/mês | Custo estimado |
|---|---|---|
| MVP Piloto | 500 conversas | ~U$ 25–30 |
| MVP Produção (100 processos/mês) | 5.000 conversas | ~U$ 250–300 |
| Escala (10.000 processos/mês) | 50.000 conversas | ~U$ 2.500–3.000 |

O custo em escala nacional deve ser previsto no contrato com o órgão público contratante.

## Configuração Necessária

```bash
# Variáveis de ambiente obrigatórias
WHATSAPP_PHONE_NUMBER_ID=<ID do número no Meta>
WHATSAPP_ACCESS_TOKEN=<token permanente de sistema>
WHATSAPP_WEBHOOK_VERIFY_TOKEN=<token aleatório para verificação do webhook>
WHATSAPP_APP_SECRET=<para validação de assinatura HMAC do webhook>
```

## Alternativas Rejeitadas

| Alternativa | Motivo da rejeição |
|---|---|
| Z-API / UltraMsg / Evolution | Viola ToS do Meta; risco de banimento; inaceitável para governo |
| Twilio | Custo adicional sem benefício técnico no volume esperado |
| Telegram | Menor adoção que WhatsApp no Brasil rural (WhatsApp: 170M+ usuários) |
| SMS | Sem capacidade de bot conversacional; custo similar sem riqueza de canal |
