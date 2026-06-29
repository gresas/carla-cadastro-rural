---
sidebar_position: 1
title: Visão e Objetivos
description: Visão do produto Carla, posicionamento estratégico, diferenciais e objetivos de negócio mensuráveis.
tags: [produto, visão, objetivos]
---

# Visão e Objetivos

:::info Para quem é esta página
Times de produto, gestores e stakeholders. Para a implementação técnica, veja [Arquitetura Geral](../arquitetura/visao-geral.md).
:::

## Visão do Produto

A **Carla** é uma interface de chat web própria para o Cadastro Ambiental Rural, open source, sem dependência de plataformas de mensageria proprietárias. O cidadão acessa via `car.gov.br`, autentica com Gov.br e recebe orientação conversacional ao longo de todo o processo do CAR.

Do ponto de vista de impacto, a Carla democratiza o acesso à regularização ambiental — reduzindo a dependência de intermediários pagos, diminuindo a taxa de retificação e contribuindo com os compromissos brasileiros de proteção da vegetação nativa e conformidade com o Código Florestal.

## Posicionamento

```
car.gov.br → [ Carla — chat web ] → cidadão guiado → cadastro no SICAR
                                                   ↓
                              fluxo estadual (ex: Acre) continua disponível
```

A Carla **não substitui** o SICAR nem os fluxos estaduais existentes. É um **canal alternativo**, mais acessível — o cidadão escolhe.

:::note Realidade multi-plataforma
Alguns estados têm plataformas próprias de registro CAR; os demais usam o SICAR federal. Veja [Plataformas Estaduais](../dominio/plataformas-estaduais.md) para detalhes.
:::

## Origem: haCARthon e CAR DPG

A Carla foi desenvolvida como solução para o **Desafio 1 do haCARthon**, maratona de inovação aberta realizada com parceria de MGI, FBDS, Enap e Impact Hub Brasil. Integra o projeto **CAR DPG (Digital Public Good)** — o que exige que o software seja open source e livre de dependências de fornecedores proprietários, para permitir replicação soberana por outros países.

## Diferenciais Centrais

### 1. Orientação guiada anti-retificação
A Carla nunca pede um dado que já recebeu. Reaproveita, pré-preenche e pede confirmação. Fecha cada etapa com um resumo em bloco — não campo a campo. O objetivo é que o cadastro chegue ao analista completo e correto desde a primeira tentativa.

### 2. Etapa Geo assistida (demarcação sugerida)
Em vez de pedir que o cidadão desenhe o polígono do imóvel do zero, a Carla sugere uma demarcação com base nos dados já informados (área, município, nome). O cidadão ajusta e confirma. Reservas Legais e APPs são destacadas automaticamente como referência.

### 3. Ponte direta com o analista ambiental
A Carla notifica o cidadão quando há mensagens do analista, exibe o status oficial do SICAR e permite responder diretamente pela interface, sem precisar navegar pelo portal do SICAR.

## Evidências do Problema

Os dados oficiais do SICAR justificam a necessidade de uma solução como a Carla:

| Dado | Valor | Implicação |
|---|---|---|
| Taxa de retificação (2014) | 5,7% | Baseline — quase nenhum cadastro era revisado |
| Taxa de retificação (2026) | **77%** | Três em cada quatro cadastros precisam de correção |
| Imóveis de perfil "Pequeno" | **93,8%** | Maioria são pequenos produtores, com menos suporte técnico |
| Imóveis com PRA informado sem adesão | **~34%** | Produtores não completam a regularização ambiental |

*Fonte: planilha oficial de dados do CAR — SICAR/MMA.*

## Objetivos de Negócio

| # | Objetivo | Métrica | Prazo |
|---|---|---|---|
| OB-01 | Reduzir retrabalho por documentação incompleta | −50% de pendências por documentação faltante | 6 meses pós-MVP |
| OB-02 | Reduzir tempo médio de análise | De 30 → 15 dias úteis | 6 meses pós-MVP |
| OB-03 | Melhorar experiência do cidadão | NPS ≥ 70, taxa de conclusão ≥ 75% | 3 meses pós-MVP |
| OB-04 | Reduzir taxa de retificação | De 77% → abaixo de 40% | 12 meses pós-MVP |
| OB-05 | Aumentar produtividade dos analistas | 5 → 10 processos/analista/dia | 6 meses pós-MVP |
| OB-06 | Automatizar validações documentais | ≥ 80% das validações automáticas | 12 meses pós-MVP |

## Contexto: Por que o CAR importa

O Cadastro Ambiental Rural é a porta de entrada para a regularização ambiental de todo imóvel rural no Brasil. Sem ele, o produtor não acessa crédito rural, programas de Pagamento por Serviços Ambientais (PSA), Cotas de Reserva Ambiental (CRA), descontos tributários nem pode vender madeira certificada — e fica exposto a multas e embargos.

:::caution Obrigação legal
A Lei 12.651/2012 (Código Florestal) torna o CAR obrigatório. O Decreto 7.830/2012 regulamenta o SICAR e define os instrumentos do PRA. Veja [Fundamentação Legal](../dominio/fundamentacao-legal.md).
:::

Com **9,6 milhões de propriedades** no sistema nacional e taxa de retificação de 77%, o problema de qualidade dos cadastros é o gargalo central — e é exatamente onde a Carla atua.

## Próximos passos

- [Conheça as personas](./personas.md) — quem são os usuários
- [Casos de uso](./casos-de-uso.md) — o que cada persona consegue fazer
- [Roadmap](./roadmap.md) — quando cada parte será entregue
