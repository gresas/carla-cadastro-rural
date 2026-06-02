# CARla

[![CI](https://github.com/org/carla/actions/workflows/ci.yml/badge.svg)](https://github.com/org/carla/actions)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

**Plataforma inteligente de atendimento e automação para o Cadastro Ambiental Rural (CAR).**

O CARla é uma camada de inteligência sobre o SICAR — não o substitui. Oferece assistência conversacional por IA, validação documental automatizada e ferramentas de produtividade para analistas de órgãos ambientais.

---

## Problema

Produtores rurais enfrentam um processo burocrático complexo sem orientação adequada. Analistas lidam com documentação incompleta e alto volume de processos repetitivos. O CARla resolve os dois lados.

## Solução

- **Portal do Cidadão:** Registro CAR guiado passo a passo com assistente IA
- **Assistente Inteligente:** Respostas em linguagem simples sobre o processo CAR
- **Motor de Validação:** OCR + extração de dados + verificação de consistência automática
- **Portal do Analista:** Fila priorizada, dossiê automático por IA, aprovação/rejeição em um clique

---

## Quick Start (5 comandos)

```bash
# 1. Clonar e entrar no projeto
git clone https://github.com/org/carla.git && cd carla

# 2. Subir infraestrutura
docker compose up -d

# 3. Instalar dependências e configurar banco
cd backend && uv sync && cp ../.env.example .env && make migrate && make seed-dev

# 4. Iniciar backend
make dev
# API docs: http://localhost:8000/api/docs

# 5. Em outro terminal: iniciar frontend
cd ../frontend && npm install && npm run dev
# App: http://localhost:3000
```

---

## Estrutura do Projeto

```
carla/
├── backend/         # Python 3.13 + FastAPI — API e workers
│   └── src/carla/
│       ├── modules/ # Bounded contexts (auth, processos, documentos, assistente...)
│       └── workers/ # Consumers RabbitMQ (OCR, notificações, integrações)
├── frontend/        # React 18 + TypeScript + Vite + Tailwind
├── infra/           # Docker Compose, Kubernetes (Kustomize), Terraform
├── docs/            # Documentação completa do projeto
└── scripts/         # Utilitários (seed, migrations, verificação de segurança)
```

---

## Documentação

| Documento | Descrição |
|---|---|
| [PRD](docs/01-prd/PRD.md) | Product Requirements Document — visão, personas, casos de uso |
| [Arquitetura](docs/04-arquitetura/ARQUITETURA.md) | C4, lógica, física, observabilidade |
| [ADRs](docs/05-adrs/INDEX.md) | Decisões arquiteturais justificadas |
| [Modelo de Dados](docs/06-modelo-dados/MODELO_DADOS.md) | DDL PostgreSQL + PostGIS completo |
| [API Design](docs/07-apis/API_DESIGN.md) | Endpoints REST, schemas, autenticação |
| [Roadmap](docs/09-roadmap/ROADMAP.md) | MVP Hackathon → MVP Produção → Escalável |
| [Índice completo](docs/INDEX.md) | Todos os documentos |

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.13+, FastAPI, Pydantic v2 |
| Banco | PostgreSQL 16 + PostGIS 3.4 + pgvector |
| Mensageria | RabbitMQ 3.13 |
| Cache | Redis 7 |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Auth | Gov.br OAuth2/OIDC, JWT RS256 |
| IA | Claude (Anthropic) / GPT-4o (OpenAI) / Ollama (local) |
| Infra | Docker, Kubernetes |
| Observabilidade | OpenTelemetry, Prometheus, Grafana |

---

## Contribuindo

1. Fork o repositório
2. Crie sua feature branch: `git checkout -b feat/CAR-123-descricao`
3. Siga os padrões de código (ruff, mypy, conventional commits)
4. Abra um Pull Request usando o template disponível

Veja [ESTRUTURA.md](docs/10-estrutura-repositorio/ESTRUTURA.md) para convenções de código e [TESTES.md](docs/12-estrategia-testes/TESTES.md) para a estratégia de testes.

---

## Licença

Apache 2.0 — veja [LICENSE](LICENSE) para detalhes.

---

**Desenvolvido para o Hackathon CAR/SICAR 2026**
