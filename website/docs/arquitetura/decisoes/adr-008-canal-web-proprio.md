---
sidebar_position: 9
title: "ADR-008: Canal Web Próprio"
description: Por que a Carla adota interface de chat web própria em vez de depender de WhatsApp/Telegram como canal core.
tags: [adr, canal, web, govbr, open-source, dpg]
---

# ADR-008: Interface de Chat Web Própria como Canal Core

**Status:** Aceito | **Data:** 2026-06-22

## Contexto

O projeto Carla nasceu como solução para o **Desafio 1 do haCARthon** — maratona de inovação aberta organizada por MGI, FBDS, Enap e Governo da Noruega, no contexto do projeto **CAR DPG (Digital Public Good)**. Para qualificar como bem público digital, o software precisa ser open source, sem dependências de fornecedores proprietários que possam restringir replicação ou uso soberano.

A versão inicial do projeto ([ADR-007](./adr-007-whatsapp.md)) planejava o WhatsApp (Meta Cloud API) como canal principal de atendimento ao cidadão. Essa decisão gerava as seguintes restrições:

- Custo operacional por conversa (~U$ 0,02–0,06), inviável em escala pública sem contrato
- Dependência de aprovação de templates pelo Meta — fila de aprovação de dias a semanas
- Aprovação de conta Business pelo Meta — processo externo ao controle do projeto
- Termos de serviço do Meta que podem ser alterados unilateralmente, afetando um sistema de governo
- Barreira para replicação em outros países (requisito DPG): cada instância precisaria de aprovação própria no Meta

Além disso, a análise do perfil dos usuários do CAR mostrou que 93,8% dos imóveis são de perfil "Pequeno" — produtores que acessam serviços digitais via navegador, não necessariamente via WhatsApp Business.

## Decisão

**Interface de chat web própria** como canal core, acessada via `car.gov.br`.

- O cidadão acessa `car.gov.br`, clica no banner/botão da Carla e abre uma nova aba com a interface de chat
- A primeira mensagem identifica a Carla e solicita (ou verifica) o login via Gov.br
- O histórico de conversa é persistido por usuário, vinculado ao `user_id` do Gov.br
- Ao retornar, a Carla resume a etapa atual, mensagens não lidas do analista e próximas ações
- Integração com apps de mensageria (WhatsApp, Telegram etc.) pode ser implementada **futuramente** como adapter desacoplado — nunca como dependência do core

## Justificativa

### Por que interface web própria

| Critério | Interface Web Própria | WhatsApp (Meta Cloud API) |
|---|---|---|
| Custo operacional | Zero (só infra própria) | ~U$ 0,02–0,06 por conversa |
| Dependência externa | Gov.br (já obrigatório) | Meta (adicional) |
| Qualificação DPG | Sim — open source puro | Não — depende de fornecedor proprietário |
| Aprovação externa necessária | Não | Sim (Meta, 1–3 semanas) |
| Persistência de histórico | Controlada internamente | Sujeita às políticas do Meta |
| Replicação por outros países | Simples (fork + deploy) | Requer nova aprovação Meta por país |
| Histórico de instabilidade | Sob controle do time | Meta incidentes históricos em 2021 e 2024 |

### Relação com Gov.br

Gov.br deixa de ser apenas uma "ponte" para vincular o número de telefone ao WhatsApp. Passa a ser:

- **Autenticação principal** da interface web da Carla
- **Âncora de identidade** para persistência do histórico de conversa por cidadão
- **Fonte de dados** para pré-preenchimento (nome, CPF verificado)

### Carla como canal alternativo, não substituto

O fluxo tradicional do CAR — incluindo plataformas estaduais como a do Acre — continua existindo. A Carla é um canal **adicional**, mais acessível. O cidadão escolhe.

## Consequências

✅ Zero custo de canal — apenas infraestrutura própria  
✅ Qualifica como Digital Public Good (sem dependências proprietárias)  
✅ Sem aprovação externa necessária para lançar ou escalar  
✅ Histórico de conversa sob controle total do sistema  
✅ Replicável por qualquer país com CAR equivalente  
✅ Pré-preenchimento via Gov.br (CPF verificado, nome)  
❌ Não aproveita a base instalada do WhatsApp (170M+ usuários no Brasil)  
❌ Exige desenvolvimento e manutenção de interface de chat própria  
❌ UX pode ser inferior a apps nativos de mensagem em dispositivos móveis antigos

## Arquitetura do Canal

```
car.gov.br
  └─→ Banner/botão "Fale com a Carla"
        └─→ Nova aba: interface web de chat (React)
              └─→ Verifica / solicita login Gov.br (OAuth2 PKCE)
                    └─→ Sessão persistente vinculada ao user_id Gov.br
                          └─→ Carla retoma etapa + mensagens não lidas + próximas ações
```

**Extensão futura (opcional):**

```
WhatsApp / Telegram
  └─→ Webhook Adapter (serviço desacoplado)
        └─→ Mesmo backend de conversas do canal web
```

## Alternativas Rejeitadas

| Alternativa | Motivo da rejeição |
|---|---|
| WhatsApp como canal core | Dependência proprietária; custo; barreira DPG; ver [ADR-007](./adr-007-whatsapp.md) |
| Telegram como canal core | Mesmo problema de dependência proprietária; menor adoção rural |
| WhatsApp + web em paralelo (MVP duplo) | Complexidade duplicada sem benefício claro no curto prazo |
