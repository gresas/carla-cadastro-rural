---
sidebar_position: 5
title: PRA — Programa de Regularização Ambiental
description: O que é o PRA, quando é exigido e como se relaciona com o CAR no ciclo do CARla.
tags: [domínio, pra, regularização, código-florestal]
---

# PRA — Programa de Regularização Ambiental

:::info Para quem é esta página
Engenheiros, PMs e analistas. O PRA define um estado de processo que o CARla precisa modelar — imóveis com déficit ambiental não são apenas "aprovados" ou "rejeitados".
:::

## O que é o PRA

O **Programa de Regularização Ambiental** é o instrumento pelo qual proprietários rurais com déficit de Área de Preservação Permanente (APP) ou Reserva Legal (RL) se comprometem a recuperar as áreas degradadas.

**Base legal:** art. 59 da Lei 12.651/2012 (Código Florestal).

## Quando é exigido

O PRA é obrigatório quando a propriedade tem **déficit ambiental** — ou seja, quando a área de APP ou RL existente é menor que o mínimo exigido pelo Código Florestal:

| Situação | Exige PRA? |
|---|---|
| APP intacta + RL atendida | Não — aprovação direta |
| APP ou RL com déficit (mesmo que pequeno) | Sim — aprovação com obrigação de PRA |
| Imóvel em área de uso consolidado (art. 61-A) | Pode ter regime especial de recuperação |

:::tip Imóveis consolidados
Imóveis que tinham intervenção em APP ou RL antes de 22/07/2008 podem ter área de recuperação reduzida conforme módulos fiscais — a regra varia por bioma e tamanho do imóvel. O assistente IA deve ser capaz de orientar o cidadão sobre essa regra.
:::

## Relação com o CAR no CARla

```
CAR (submissão) → Análise → Resultado
                               ├── Aprovado        → Certificado CAR
                               ├── Aprovado com PRA → Certificado CAR + obrigação de adesão ao PRA
                               └── Rejeitado        → Motivo + prazo de recurso
```

O estado `aprovado_com_pra` no CARla significa:

- O imóvel está **regularmente cadastrado** no CAR
- O proprietário **deve aderir ao PRA** junto ao órgão ambiental estadual
- O Certificado CAR é emitido, mas inclui a observação sobre a obrigação de regularização

## O que o CARla faz (e não faz)

| Funcionalidade | CARla |
|---|---|
| Identificar que o imóvel tem déficit | ✅ Via cálculo de área de APP/RL nos dados do processo |
| Notificar cidadão sobre obrigação de PRA | ✅ Na notificação de aprovação com PRA |
| Orientar sobre o processo de adesão ao PRA | ✅ Assistente IA com RAG sobre o PRA estadual |
| Gerir o PRA (prazos, planos de recuperação, monitoramento) | ❌ Fora do escopo — sistema separado do órgão estadual |

:::caution Escopo do CARla
O CARla não substitui o sistema de gestão do PRA. Ele apenas identifica a necessidade, notifica o cidadão e orienta os próximos passos. A adesão e o acompanhamento do PRA ocorrem nos sistemas do órgão ambiental estadual.
:::

## Mensagem ao Cidadão — Aprovado com PRA

```
✅ Seu CAR foi aprovado!
Número de protocolo: MA-1234567-12345678901234

⚠️ Atenção: sua propriedade precisa de regularização ambiental.
A análise identificou que sua área de Reserva Legal está
abaixo do mínimo exigido pelo Código Florestal.

Próximo passo obrigatório: aderir ao Programa de Regularização
Ambiental (PRA) junto à SEMA-MA.

O que fazer agora:
1. Acesse o portal da SEMA-MA
2. Informe seu número de protocolo CAR
3. Solicite a adesão ao PRA

Dúvidas? Pergunte ao assistente do CARla.
```

## Ver também

- [Glossário — PRA, Déficit Ambiental](./glossario.md)
- [Event Storming — ProcessoAprovadoComPRA](./event-storming.md)
- [Fluxo do Analista — Aprovado com PRA](../design/fluxos/analista.md)
