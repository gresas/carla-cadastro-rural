---
sidebar_position: 1
title: Visão e Objetivos
description: Visão do produto CARla, posicionamento estratégico e objetivos de negócio mensuráveis.
tags: [produto, visão, objetivos]
---

# Visão e Objetivos

:::info Para quem é esta página
Times de produto, gestores e stakeholders. Para entender a implementação técnica, veja [Arquitetura Geral](../arquitetura/visao-geral.md).
:::

## Visão do Produto

O **CARla** é um sistema web que integra diretamente com o SICAR para simplificar o registro do CAR. A plataforma oferece assistência conversacional por IA, ferramenta de geometria por satélite, validação documental automatizada e ferramentas de produtividade para analistas de órgãos ambientais.

Do ponto de vista de impacto social, o CARla democratiza o acesso ao processo de regularização ambiental, reduzindo a dependência de intermediários pagos, acelerando a análise e contribuindo para os compromissos brasileiros de proteção da vegetação nativa e conformidade com o Código Florestal.

## Posicionamento

```
Produtor Rural ──→ [ CARla ] ──→ SICAR (integração direta)
```

O CARla **não é** um substituto ao SICAR. Usa o mesmo modelo de integração direta de outros sistemas que acessam o SICAR para efetivar o cadastro — resolvendo os problemas de experiência e eficiência sem exigir mudanças no sistema do governo.

:::note Realidade multi-plataforma
Alguns estados têm plataformas próprias de registro CAR; os demais usam o SICAR federal. Veja [Plataformas Estaduais](../dominio/plataformas-estaduais.md) para detalhes sobre como o CARla endereça essa diversidade.
:::

## Objetivos de Negócio

| # | Objetivo | Métrica | Prazo |
|---|---|---|---|
| OB-01 | Reduzir retrabalho por documentação incompleta | −50% de pendências por documentação faltante | 6 meses pós-MVP |
| OB-02 | Reduzir tempo médio de análise | De 30 → 15 dias úteis | 6 meses pós-MVP |
| OB-03 | Melhorar experiência do cidadão | NPS ≥ 70, taxa de conclusão ≥ 75% | 3 meses pós-MVP |
| OB-04 | Melhorar qualidade dos dados | Taxa de aprovação na 1ª tentativa: 40% → 70% | 6 meses pós-MVP |
| OB-05 | Aumentar produtividade dos analistas | 5 → 10 processos/analista/dia | 6 meses pós-MVP |
| OB-06 | Automatizar tarefas repetitivas | ≥ 80% das validações documentais automáticas | 12 meses pós-MVP |

## Contexto: Por que o CAR importa

O Cadastro Ambiental Rural é a porta de entrada para regularização ambiental de todo imóvel rural no Brasil. Sem ele, o produtor não acessa crédito rural, não pode vender madeira certificada e fica exposto a multas.

:::caution Obrigação legal
A Lei 12.651/2012 (Código Florestal) torna o CAR obrigatório. O prazo de regularização continua ativo para milhões de propriedades.
:::

Com **9,6 milhões de propriedades** no sistema nacional e tempo médio de análise de **30 dias úteis**, o gargalo operacional é evidente — e é exatamente onde o CARla atua.

## Próximos passos

- [Conheça as personas](./personas.md) — quem são os usuários
- [Casos de uso](./casos-de-uso.md) — o que cada persona consegue fazer
- [Roadmap](./roadmap.md) — quando cada parte será entregue
