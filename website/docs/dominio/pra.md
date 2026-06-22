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

O **Programa de Regularização Ambiental** é o instrumento pelo qual proprietários rurais com déficit de Área de Preservação Permanente (APP) ou Reserva Legal (RL) se comprometem a recuperar as áreas degradadas dentro de um prazo estabelecido em Termo de Compromisso firmado com o órgão ambiental.

**Base legal:**
- **Lei nº 12.651/2012** (Código Florestal), art. 59 — institui o PRA nos estados e Distrito Federal
- **Decreto nº 7.830/2012** — regulamenta o SICAR, define a natureza declaratória do CAR e estabelece os instrumentos do PRA

### Instrumentos do PRA (Decreto 7.830/2012)

| Instrumento | Descrição |
|---|---|
| **Termo de Compromisso** | Documento firmado entre o proprietário e o órgão ambiental estadual, estabelecendo o prazo e o plano de regularização |
| **PRAD** | Projeto de Recuperação de Áreas Degradadas — plano técnico detalhado de recomposição vegetal |
| **CRA** | Cota de Reserva Ambiental — permite compensar déficit de Reserva Legal em outra propriedade |

### Natureza declaratória do CAR

O CAR tem **natureza declaratória** — o cidadão declara os dados, o órgão analisa. A análise resulta em:
- **Regular** — dados declarados consistentes e limites atendidos
- **Pendente de Regularização** — déficit identificado; notificação única é enviada ao proprietário (art. 7º do Decreto 7.830/2012); prazo para adesão ao PRA começa a partir da notificação

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

## Relação com o CAR na Carla

```
CAR (submissão) → Em Análise → Resultado SICAR
                                  ├── Regular                    → Recibo de Inscrição
                                  └── Pendente de Regularização  → Recibo + aba Regularização Ambiental + prazo PRA
```

O status `Pendente de Regularização` significa:

- O imóvel está **regularmente inscrito** no CAR (Recibo de Inscrição emitido)
- O proprietário **deve aderir ao PRA** junto ao órgão ambiental estadual
- A **aba Regularização Ambiental** é liberada no Demonstrativo da Situação do CAR
- A Carla notifica o cidadão e orienta os próximos passos

## O que o CARla faz (e não faz)

| Funcionalidade | CARla |
|---|---|
| Identificar que o imóvel tem déficit | ⚠️ Com base nas **áreas declaradas pelo requerente/RT** no processo. Cálculo geoespacial automatizado (cruzamento com topografia e cobertura vegetal via MapBiomas/MDE) é funcionalidade de Fase 3 — não está disponível no MVP. |
| Notificar cidadão sobre obrigação de PRA | ✅ Na notificação de aprovação com PRA |
| Orientar sobre o processo de adesão ao PRA | ✅ Assistente IA com RAG sobre o PRA estadual |
| Gerir o PRA (prazos, planos de recuperação, monitoramento) | ❌ Fora do escopo — sistema separado do órgão estadual |

:::note Prazo de adesão ao PRA
Ao aprovar com PRA, o analista deve registrar o **prazo para adesão** (definido pela normativa estadual — geralmente 1 ano a partir da aprovação). O CARla agenda uma notificação automática ao cidadão quando o prazo estiver a 30 dias do vencimento. Mesmo sem gerir o PRA, o lembrete é parte do atendimento e evita que o produtor perca o prazo por falta de informação.
:::

:::caution Escopo do CARla
O CARla não substitui o sistema de gestão do PRA. Ele apenas identifica a necessidade, notifica o cidadão e orienta os próximos passos. A adesão e o acompanhamento do PRA ocorrem nos sistemas do órgão ambiental estadual.
:::

## Mensagem ao Cidadão — Pendente de Regularização

```
⚠️ Seu CAR foi analisado e está Pendente de Regularização.

O analista identificou que sua propriedade possui déficit de Reserva Legal
abaixo do mínimo exigido pelo Código Florestal.

Seu Recibo de Inscrição do Imóvel Rural no CAR está disponível:
Recibo: MA-1234567-12345678901234

Próximo passo obrigatório: aderir ao Programa de Regularização
Ambiental (PRA) junto à SEMA-MA.

O que fazer agora:
1. Acesse a aba "Regularização Ambiental" no Demonstrativo da Situação do CAR
2. Leia a mensagem completa do analista
3. Formalize a adesão ao PRA junto à SEMA-MA

Dúvidas? Pergunte à Carla.

[ 📬 Ver mensagem completa ] [ 🌿 Saber mais sobre o PRA ]
```

## Ver também

- [Fundamentação Legal](./fundamentacao-legal.md) — Lei 12.651/2012 e Decreto 7.830/2012
- [Glossário — PRA, Termo de Compromisso, CRA, PRAD](./glossario.md)
- [Event Storming — ProcessoPendenteDeRegularização](./event-storming.md)
- [Fluxo do Analista — Pendência de Regularização](../design/fluxos/analista.md)
- [Sequência de Mensagens — Seção de Dúvidas sobre PRA](../design/fluxos/mensagens-simuladas.md)
