---
sidebar_position: 1
title: Estratégia de Testes
description: Pirâmide de testes do CARla — filosofia, cobertura mínima e quality gates de CI.
tags: [engenharia, testes, qualidade, ci]
---

# Estratégia de Testes

:::info Para quem é esta página
Engenheiros. Para exemplos concretos, veja [Testes Unitários](./unitarios.md) e [E2E](./e2e.md).
:::

## Pirâmide de Testes

```
                    ┌───────────┐
                    │  Carga    │  2%  (k6)
                    │ Segurança │
                    └─────┬─────┘
                 ┌────────┴────────┐
                 │  E2E (Playwright)│  3%
                 └────────┬────────┘
              ┌────────────┴──────────────┐
              │  Contrato (Pact)          │  5%
              └────────────┬──────────────┘
         ┌──────────────────┴──────────────────┐
         │  Integração (pytest + TestContainers) │  20%
         └──────────────────┬──────────────────┘
    ┌────────────────────────────────────────────────┐
    │              Unitários (pytest)                │  70%
    │  Domínio: entidades, VOs, serviços de domínio  │
    └────────────────────────────────────────────────┘
```

## Cobertura Mínima por Camada

| Camada | Mínimo | Justificativa |
|---|---|---|
| Domain (entities, VOs, services) | 95% | Regras de negócio críticas — zero tolerância |
| Application (use cases) | 85% | Orquestração de fluxos |
| Infrastructure (repositories) | 70% | I/O mockado; cobrir mapeamentos ORM |
| Presentation (routes) | 80% | Validação de entrada e formato de resposta |
| **Global** | **80%** | Quality gate — CI bloqueia se abaixo |

## Quality Gates do CI

| Gate | Condição de bloqueio |
|---|---|
| Cobertura | < 80% global |
| SAST (Bandit) | Qualquer finding HIGH ou CRITICAL |
| Dependências (Safety) | CVE CRITICAL em qualquer pacote |
| Secrets (Gitleaks) | Qualquer segredo detectado no código |
| Testes unitários | Qualquer falha |
| Testes de integração | Qualquer falha |
| p95 de latência (k6) | > 1000ms em endpoint crítico |

:::tip Princípio FIRST
**Fast** — testes unitários < 5s total  
**Isolated** — sem dependências entre testes  
**Repeatable** — mesmo resultado em qualquer ambiente  
**Self-validating** — passa ou falha, sem interpretação  
**Timely** — escrito junto com o código  
:::

## Configuração pytest

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = """
  --cov=src
  --cov-report=term-missing
  --cov-fail-under=80
"""
```

## Ver também

- [Testes Unitários](./unitarios.md) — exemplos de domínio com pytest
- [Testes de Integração](./integracao.md) — TestContainers
- [Testes E2E](./e2e.md) — Playwright
- [Testes de Carga](./carga.md) — k6
