---
sidebar_position: 1
title: Setup do Ambiente
description: Pré-requisitos e quick start para rodar o CARla localmente.
tags: [contribuindo, setup, docker]
---

# Setup do Ambiente

:::info Para quem é esta página
Qualquer pessoa que quer rodar o CARla localmente — dev, QA ou PM técnico.
:::

## Pré-requisitos

| Ferramenta | Versão mínima | Instalação |
|---|---|---|
| Python | 3.13+ | [python.org](https://python.org) ou `pyenv` |
| Node.js | 20+ | [nvm](https://github.com/nvm-sh/nvm) |
| Docker | 24+ | [docker.com](https://docker.com) |
| Docker Compose | 2.20+ | Incluído no Docker Desktop |
| uv | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| git | 2.40+ | — |

## Quick Start (5 comandos)

```bash
# 1. Clonar e entrar no projeto
git clone git@github.com:gresas/carla-cadastro-rural.git && cd carla-cadastro-rural

# 2. Subir infraestrutura (PostgreSQL+PostGIS, Redis, RabbitMQ, MinIO)
docker compose up -d

# 3. Backend: instalar deps, criar .env e aplicar migrations
cd backend && uv sync && cp ../.env.example .env && make migrate && make seed-dev

# 4. Iniciar o backend
make dev
# API docs: http://localhost:8000/api/docs

# 5. Frontend (em outro terminal)
cd ../frontend && npm install && npm run dev
# App: http://localhost:3000
```

## Documentação (este site)

```bash
cd website && npm install && npm run start
# Docusaurus: http://localhost:3001
```

## Variáveis de Ambiente

Copie `.env.example` e edite conforme necessário:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://carla:password@localhost:5432/carla_dev

# LLM (apenas uma é necessária para dev)
ANTHROPIC_API_KEY=sk-ant-...
LLM_PRIMARY_PROVIDER=anthropic

# Gov.br (mock habilitado por padrão em dev)
GOVBR_MOCK_ENABLED=true
```

:::tip Gov.br em desenvolvimento
`GOVBR_MOCK_ENABLED=true` ativa um login simplificado (CPF + nome) sem necessidade de integração real com o Gov.br. Ideal para desenvolvimento local.
:::

## Comandos úteis

```bash
# Backend
make dev          # Iniciar com hot-reload
make test         # Rodar testes unitários + integração
make lint         # ruff + mypy
make migrate      # Aplicar migrations pendentes
make seed-dev     # Popular banco com dados de teste

# Frontend
npm run dev       # Dev server com HMR
npm run build     # Build de produção
npm run test      # Vitest

# Docusaurus
npm run start     # Dev server
npm run build     # Build estático
```

## Ver também

- [Convenções de código](./convencoes.md) — Git, Python, TypeScript, banco
- [Como escrever documentação](./como-escrever-docs.md) — guia deste Docusaurus
- [Novo ADR](./novo-adr.md) — quando e como criar uma decisão arquitetural
