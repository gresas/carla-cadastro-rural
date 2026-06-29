---
sidebar_position: 5
title: Métricas de Sucesso
description: KPIs do CARla — adoção, qualidade, eficiência, satisfação e técnico.
tags: [produto, kpis, métricas]
---

# Métricas de Sucesso

:::info Para quem é esta página
PMs e gestores. As métricas técnicas têm alertas configurados em [Observabilidade](../arquitetura/visao-geral.md#observabilidade).
:::

## KPIs por Dimensão

### Adoção
| Métrica | Meta 3 meses | Meta 12 meses |
|---|---|---|
| MAU (Usuários Ativos Mensais) | ≥ 500 | ≥ 10.000 |
| Taxa de conclusão de registro | ≥ 75% | ≥ 85% |
| Taxa de retenção pós-pendência | ≥ 60% | ≥ 75% |

### Qualidade dos Dados
| Métrica | Situação Atual | Meta |
|---|---|---|
| **Taxa de retificação** (KPI norte) | **77% (2026, SICAR/MMA)** | **< 40%** |
| Taxa de aprovação na 1ª tentativa | ~23% (inverso da retificação) | ≥ 60% |
| Redução de pendências por doc. incompleta | — | −50% |
| Precisão do OCR (extração de campos) | — | ≥ 90% |

### Eficiência Operacional
| Métrica | Situação Atual (est.) | Meta |
|---|---|---|
| Tempo médio de análise | ~30 dias úteis | ≤ 15 dias úteis |
| Processos/analista/dia | ~5 | ≥ 10 |
| % de validações documentais automáticas | ~0% | ≥ 80% |

### Satisfação
| Métrica | Meta |
|---|---|
| NPS do cidadão | ≥ 70 |
| CSAT do analista | ≥ 4,0/5,0 (**piloto Acre: 4,5/5,0**) |
| Taxa de uso do assistente IA | ≥ 40% dos MAU |

### Técnico (SLAs)
| Métrica | Meta |
|---|---|
| Uptime | ≥ 99,5% |
| Latência p99 da API | < 2s |
| Taxa de erro HTTP 5xx | < 0,1% |
| Cobertura de testes | ≥ 80% |

## Resultados do Piloto — Acre (Jan–Jun 2026)

:::tip Dados reais do painel administrativo
Os números abaixo são do piloto em produção no estado do Acre. Base: painel do analista, jun/2026.
:::

### KPIs do piloto

| Métrica | Resultado |
|---|---|
| **Atendimentos realizados** | 1.284 (desde o lançamento) |
| **Imóveis cadastrados via Carla** | 847 (de 1.284 iniciados — 66% de conclusão) |
| **Tempo médio por CAR** | 28 min (redução de **−41%** vs. fluxo tradicional) |
| **Horas de servidor poupadas** | 312 h (equivalente a 39 dias de trabalho) |
| **Satisfação** | **4,5/5** — 280 avaliações; 82% satisfeitos, 11% neutros, 7% insatisfeitos |

### Evolução do tempo médio de atendimento (min)

| Jan | Fev | Mar | Abr | Mai | Jun |
|---|---|---|---|---|---|
| 48 | 43 | 39 | 36 | 31 | 28 |

### Atendimentos por mês (2026)

| Mês | Iniciados | Cadastrados | Pendentes |
|---|---|---|---|
| Jan | 18 | 12 | 6 |
| Fev | 24 | 19 | 8 |
| Mar | 31 | 22 | 11 |
| Abr | 28 | 25 | 9 |
| Mai | 36 | 28 | 14 |
| Jun | 22 | 15 | 12 |

### Distribuição por município (Acre)

| Município | CARs no sistema |
|---|---|
| Rio Branco | 47 |
| Cruzeiro do Sul | 28 |
| Sena Madureira | 19 |
| Tarauacá | 14 |
| Feijó | 11 |
| Brasileia | 9 |
| Xapuri | 8 |
| Outros | 22 |

---

## Critérios de Aceitação por Fase

| Fase | Critério mínimo |
|---|---|
| **Hackathon** | Demo ao vivo sem falha; juízes usam sem instrução prévia |
| **MVP Produção** | 100 processos reais; NPS ≥ 60; uptime ≥ 99% por 30 dias |
| **Versão Escalável** | 10.000 processos/mês; NPS ≥ 70; tempo análise ≤ 15 dias |
