---
sidebar_position: 7
title: Roadmap
description: As três fases do CARla — do MVP do Hackathon à versão escalável nacional.
tags: [produto, roadmap, fases]
---

# Roadmap

:::info Para quem é esta página
Times de produto e liderança. Para detalhes de implementação por fase, veja o [Plano de Desenvolvimento](../contribuindo/setup.md).
:::

## Visão Geral

```
Semanas 1-2     │  Meses 1-3       │  Meses 4-15
────────────────┼──────────────────┼─────────────────────
FASE 1          │  FASE 2          │  FASE 3
MVP Hackathon   │  MVP Produção    │  Versão Escalável
Demo funcional  │  Piloto real     │  Produto governamental
```

---

## Fase 1 — MVP Hackathon (2 semanas)

**Objetivo:** Demonstrar o valor central para os juízes.

**O que está no escopo:**

| Funcionalidade | Critério de aceite |
|---|---|
| Login simulado (mock Gov.br) | Usuário entra com CPF e vê dashboard |
| Criar processo CAR | Formulário simples com dados do imóvel |
| Upload de documento | Arquivo salvo, status atualizado |
| OCR básico | Texto extraído e exibido |
| Chat com IA (Claude API + RAG) | Respostas streaming sobre dúvidas de CAR |
| Contexto do processo no chat | Assistente sabe qual processo o usuário tem |
| Fila do analista | Lista de processos pendentes |
| Aprovar/rejeitar | Analista muda status com motivo |

:::tip Arquitetura simplificada
Monolito modular FastAPI + Docker Compose. Sem RabbitMQ, sem Kubernetes — foco em demonstrar o valor, não a escala.
:::

**Critérios de sucesso:** Demo ao vivo sem falha por 5 minutos; juízes conseguem usar sem instrução prévia.

---

## Fase 2 — MVP Produção (12 semanas)

**Objetivo:** Primeira versão operacional integrada com Gov.br real.

**Épicos principais:**

| Épico | Semanas | Entregas-chave |
|---|---|---|
| E1: Fundação | 1–3 | Docker/K8s, CI/CD, observabilidade, Vault |
| E2: Auth Gov.br | 2–4 | OAuth2 PKCE real, RBAC 5 roles, sessões seguras |
| E3: Portal Cidadão | 3–8 | Stepper, upload, notificações, acompanhamento |
| E4: Assistente IA | 4–9 | Chat contextual, RAG, escalonamento humano |
| E5: Validação | 5–10 | OCR profissional, extração, cruzamento IBGE |
| E6: Portal Analista | 7–11 | Fila, dossiê automático, aprovação, dashboard |
| E7: Integrações | 8–12 | IBGE (municípios), stubs SIGEF/INCRA, **stub SICAR simulado** (integração real requer convênio — ver abaixo) |

**Meta:** 100 processos reais, NPS ≥ 60, uptime ≥ 99%.

:::warning Integração SICAR — pré-requisito institucional
O SICAR não possui API REST pública disponível. Acesso programático para consulta e submissão de dados requer **convênio formal com MAPA/IBAMA**. Esse processo é institucional, não técnico, e pode levar meses. Na Fase 2, o CARla opera com stub SICAR — o processo é gerenciado internamente e a sincronização com o SICAR ocorre manualmente ou via exportação. A integração real é pré-requisito para a Fase 3.
:::

---

## Fase 3 — Versão Escalável (meses 4–15)

**Objetivo:** Produto governamental robusto com integrações completas.

| Épico | Descrição |
|---|---|
| A: Microsserviços | Strangler Fig — extrair serviços do monolito gradualmente |
| B: Integrações completas | **Pré-requisito: convênio MAPA/IBAMA para API SICAR** — depois: SIGEF, IBAMA, MapBiomas, PRODES/DETER |
| C: IA Avançada | Análise geoespacial, scoring preditivo, fine-tuning |
| D: Analytics e BI | Dashboards estaduais, dados abertos anonimizados |
| E: Escalabilidade | Multi-tenancy, processamento em lote, CDN |
| E2: Canal WhatsApp | WhatsApp Business API + vinculação Gov.br |
| F: App Mobile | React Native, câmera OCR, push, offline |

**Meta:** 10.000 processos/mês em ≥ 1 estado; tempo de análise ≤ 15 dias úteis.

---

## Ver também

- [Métricas de Sucesso](./metricas.md) — como medimos cada fase
- [Arquitetura Fase 1](../arquitetura/visao-geral.md) — modelo simplificado do hackathon
- [Contribuindo](../contribuindo/setup.md) — como configurar o ambiente
