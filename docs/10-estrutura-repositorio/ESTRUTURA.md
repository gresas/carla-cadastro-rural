# CARla — Estrutura do Repositório

**Versão:** 1.0.0  
**Data:** 2026-06-01

---

## Filosofia de Organização

**Monorepo** com separação clara entre backend, frontend e infraestrutura:
- Módulos backend organizados por **Bounded Context** (DDD) — não por tipo técnico
- Frontend organizado por **feature** — não por tipo de arquivo
- Infraestrutura como código no mesmo repositório
- Documentação versionada junto ao código

**Regras:**
- Cada módulo backend é auto-contido (domain, application, infrastructure, presentation)
- Sem importações entre módulos que violem as fronteiras de BC
- Testes espelham a estrutura de `src/`
- Configuração por ambiente via variáveis de ambiente (12-factor app)

---

## Árvore Completa do Repositório

```
carla/
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # CI: lint, tests, security scan
│   │   ├── cd-staging.yml            # Deploy automático p/ staging (branch develop)
│   │   ├── cd-production.yml         # Deploy com aprovação manual (branch main)
│   │   ├── security-scan.yml         # SAST (bandit, semgrep), trivy, gitleaks
│   │   └── release.yml               # Conventional commits → semver → changelog
│   ├── CODEOWNERS                    # Responsáveis por área do código
│   ├── PULL_REQUEST_TEMPLATE.md      # Checklist de PR obrigatório
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
│
├── backend/
│   ├── pyproject.toml                # uv/hatch config + dependências + ruff + mypy
│   ├── Makefile                      # make dev | test | lint | migrate | seed
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py                    # Configuração async do Alembic
│   │   └── versions/
│   │       └── 2024_01_15_0001_initial_schema.py
│   │
│   ├── src/
│   │   └── carla/
│   │       ├── __init__.py
│   │       ├── main.py               # FastAPI app factory (create_app())
│   │       ├── config.py             # Settings com Pydantic BaseSettings (env vars)
│   │       ├── dependencies.py       # FastAPI dependencies globais (db, redis, etc.)
│   │       │
│   │       ├── shared/               # Código compartilhado entre todos os módulos
│   │       │   ├── domain/
│   │       │   │   ├── base.py       # BaseEntity, BaseValueObject, DomainEvent
│   │       │   │   ├── exceptions.py # DomainException, NotFoundError, EstadoInvalidoError
│   │       │   │   └── types.py      # UUIDs tipados, tipos customizados
│   │       │   ├── infrastructure/
│   │       │   │   ├── database.py   # SQLAlchemy engine, AsyncSession factory
│   │       │   │   ├── redis.py      # Redis async client factory
│   │       │   │   ├── storage.py    # MinIO/S3 async client
│   │       │   │   ├── messaging.py  # RabbitMQ connection factory (aio-pika)
│   │       │   │   └── outbox.py     # Outbox relay worker
│   │       │   ├── presentation/
│   │       │   │   ├── middleware.py # Logging, tracing, error handling middleware
│   │       │   │   └── responses.py  # APIResponse, PaginatedResponse, ErrorResponse
│   │       │   └── utils/
│   │       │       ├── crypto.py     # hashing (SHA-256), pgcrypto helpers
│   │       │       ├── pagination.py # Cursor-based pagination
│   │       │       └── pii.py        # PII masking para LLM
│   │       │
│   │       ├── modules/
│   │       │   │
│   │       │   ├── auth/             # BC: Identidade e Acesso
│   │       │   │   ├── domain/
│   │       │   │   │   ├── entities.py       # Usuário, Sessão
│   │       │   │   │   ├── value_objects.py  # CPF, Email, Role, NivelConfiabilidade
│   │       │   │   │   ├── services.py       # AutenticadorGovBr, AutorizadorRBAC
│   │       │   │   │   └── events.py         # UsuárioCadastrado, SessãoIniciada
│   │       │   │   ├── application/
│   │       │   │   │   ├── use_cases/
│   │       │   │   │   │   ├── autenticar_govbr.py
│   │       │   │   │   │   ├── refresh_token.py
│   │       │   │   │   │   └── logout.py
│   │       │   │   │   └── dtos.py
│   │       │   │   ├── infrastructure/
│   │       │   │   │   ├── models.py          # SQLAlchemy UserModel, SessionModel
│   │       │   │   │   ├── repository.py      # UsuárioRepositoryImpl
│   │       │   │   │   └── govbr_adapter.py   # Anti-Corruption Layer Gov.br
│   │       │   │   └── presentation/
│   │       │   │       ├── router.py          # /api/v1/auth/*
│   │       │   │       └── schemas.py         # TokenResponse, UserResponse
│   │       │   │
│   │       │   ├── processos/        # BC: Gestão de Processos CAR [CORE DOMAIN]
│   │       │   │   ├── domain/
│   │       │   │   │   ├── entities.py       # ProcessoCAR, ImóvelRural, Documento, Pendência
│   │       │   │   │   ├── value_objects.py  # NumeroCAR, ÁreaTotalHectares, Geometria
│   │       │   │   │   ├── services.py       # CalculadorAreaRL, ValidadorGeometria
│   │       │   │   │   ├── events.py         # ProcessoSubmetido, ProcessoAprovado, ...
│   │       │   │   │   ├── exceptions.py     # EstadoInvalidoError, DocumentacaoInsuficiente
│   │       │   │   │   └── repository.py     # ProcessoCARRepository (ABC interface)
│   │       │   │   ├── application/
│   │       │   │   │   ├── use_cases/
│   │       │   │   │   │   ├── criar_processo.py
│   │       │   │   │   │   ├── submeter_processo.py
│   │       │   │   │   │   ├── aprovar_processo.py
│   │       │   │   │   │   ├── rejeitar_processo.py
│   │       │   │   │   │   └── criar_pendencia.py
│   │       │   │   │   └── dtos.py
│   │       │   │   ├── infrastructure/
│   │       │   │   │   ├── models.py          # SQLAlchemy ORM models
│   │       │   │   │   ├── repository.py      # ProcessoCARRepositoryImpl
│   │       │   │   │   ├── event_publisher.py # OutboxEventPublisher
│   │       │   │   │   └── sicar_adapter.py   # ACL para SICAR
│   │       │   │   └── presentation/
│   │       │   │       ├── router.py          # /api/v1/processos/*
│   │       │   │       └── schemas.py
│   │       │   │
│   │       │   ├── documentos/       # BC: Validação Documental
│   │       │   │   ├── domain/
│   │       │   │   │   ├── entities.py       # Documento, LoteValidação
│   │       │   │   │   ├── value_objects.py  # ResultadoOCR, DadosExtraídos, HashDocumento
│   │       │   │   │   ├── services.py       # ExtratordeDados, ValidadorDocumental
│   │       │   │   │   └── events.py         # DocumentoValidado, InconsistênciaDetectada
│   │       │   │   ├── application/
│   │       │   │   ├── infrastructure/
│   │       │   │   │   ├── models.py
│   │       │   │   │   ├── repository.py
│   │       │   │   │   ├── storage/
│   │       │   │   │   │   └── minio_adapter.py
│   │       │   │   │   └── ocr/
│   │       │   │   │       ├── base.py            # OCRProvider (ABC)
│   │       │   │   │       ├── tesseract_adapter.py
│   │       │   │   │       └── google_vision_adapter.py
│   │       │   │   └── presentation/
│   │       │   │       ├── router.py          # /api/v1/documentos/*
│   │       │   │       └── schemas.py
│   │       │   │
│   │       │   ├── assistente/       # BC: Assistência Inteligente
│   │       │   │   ├── domain/
│   │       │   │   │   ├── entities.py       # Conversa, Mensagem
│   │       │   │   │   ├── value_objects.py  # Intenção, ModeloIA, Embedding
│   │       │   │   │   ├── services.py       # ClassificadorIntenção, GeradorResposta
│   │       │   │   │   └── events.py         # ConversaçãoIniciada, RespostaGerada
│   │       │   │   ├── application/
│   │       │   │   │   ├── use_cases/
│   │       │   │   │   │   ├── iniciar_conversa.py
│   │       │   │   │   │   ├── enviar_mensagem.py    # retorna AsyncGenerator (SSE)
│   │       │   │   │   │   └── buscar_base_conhecimento.py
│   │       │   │   │   └── dtos.py
│   │       │   │   ├── infrastructure/
│   │       │   │   │   ├── models.py
│   │       │   │   │   ├── repository.py
│   │       │   │   │   └── llm/
│   │       │   │   │       ├── base.py            # LLMProvider (ABC — Anti-Corruption Layer)
│   │       │   │   │       ├── anthropic_adapter.py
│   │       │   │   │       ├── openai_adapter.py
│   │       │   │   │       └── ollama_adapter.py
│   │       │   │   └── presentation/
│   │       │   │       ├── router.py          # /api/v1/assistente/*
│   │       │   │       └── schemas.py
│   │       │   │
│   │       │   ├── analista/         # Portal do Analista (Application Service)
│   │       │   │   ├── application/
│   │       │   │   │   └── use_cases/
│   │       │   │   │       ├── listar_fila.py
│   │       │   │   │       ├── assumir_processo.py
│   │       │   │   │       └── gerar_dossie.py
│   │       │   │   └── presentation/
│   │       │   │       ├── router.py          # /api/v1/analista/*
│   │       │   │       └── schemas.py
│   │       │   │
│   │       │   ├── integracoes/      # BC: Integrações Externas
│   │       │   │   ├── domain/
│   │       │   │   │   └── services.py       # CircuitBreaker, RetryPolicy
│   │       │   │   └── adapters/
│   │       │   │       ├── base.py           # SistemaExternoAdapter (ABC)
│   │       │   │       ├── sicar_adapter.py
│   │       │   │       ├── sigef_adapter.py
│   │       │   │       ├── ibama_adapter.py
│   │       │   │       └── ibge_adapter.py
│   │       │   │
│   │       │   └── analytics/        # BC: Analytics e Reporting
│   │       │       ├── application/
│   │       │       │   └── queries/
│   │       │       │       ├── dashboard_analista.py
│   │       │       │       └── relatorio_gerencial.py
│   │       │       └── presentation/
│   │       │           ├── router.py          # /api/v1/admin/*
│   │       │           └── schemas.py
│   │       │
│   │       └── workers/              # Consumers RabbitMQ assíncronos
│   │           ├── __init__.py
│   │           ├── documento_worker.py    # Consome documento.*: OCR, validação
│   │           ├── notificacao_worker.py  # Consome *.notificacao: email, in-app
│   │           ├── integracao_worker.py   # Consome *.aprovado: SICAR sync
│   │           └── outbox_worker.py       # Relay: tabela outbox → RabbitMQ
│   │
│   └── tests/
│       ├── conftest.py               # Fixtures compartilhadas (db, redis, client)
│       ├── factories.py              # factory_boy factories
│       ├── unit/                     # Testes de domínio e use cases (sem I/O)
│       │   ├── processos/
│       │   │   ├── domain/
│       │   │   │   ├── test_entities.py
│       │   │   │   ├── test_value_objects.py
│       │   │   │   └── test_services.py
│       │   │   └── application/
│       │   │       └── test_use_cases.py
│       │   └── assistente/
│       ├── integration/              # Testes com banco e serviços reais (TestContainers)
│       │   ├── test_processos_api.py
│       │   ├── test_documentos_api.py
│       │   ├── test_auth_api.py
│       │   └── test_workers.py
│       ├── contract/                 # Pact — contratos entre serviços
│       │   └── test_documento_consumer.py
│       └── fixtures/                 # Fixtures de dados (PDFs de teste, shapefiles)
│           ├── sample_matricula.pdf
│           ├── sample_ccir.pdf
│           └── sample_geometria.geojson
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── playwright.config.ts
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── router.tsx                # React Router v6 — rotas por role
│   │   │
│   │   ├── features/                 # Organização por feature (não por tipo)
│   │   │   ├── auth/
│   │   │   │   ├── components/
│   │   │   │   │   └── LoginGovBr.tsx
│   │   │   │   ├── hooks/
│   │   │   │   │   └── useAuth.ts
│   │   │   │   └── store/
│   │   │   │       └── authStore.ts   # Zustand
│   │   │   │
│   │   │   ├── processos/
│   │   │   │   ├── components/
│   │   │   │   │   ├── ProcessoStepper.tsx
│   │   │   │   │   ├── ProcessoCard.tsx
│   │   │   │   │   ├── StatusBadge.tsx
│   │   │   │   │   └── LinhaDoTempo.tsx
│   │   │   │   ├── pages/
│   │   │   │   │   ├── DashboardCidadao.tsx
│   │   │   │   │   ├── NovoProcesso.tsx
│   │   │   │   │   └── DetalhesProcesso.tsx
│   │   │   │   ├── hooks/
│   │   │   │   │   └── useProcessos.ts  # react-query hooks
│   │   │   │   └── api/
│   │   │   │       └── processosApi.ts
│   │   │   │
│   │   │   ├── documentos/
│   │   │   │   ├── components/
│   │   │   │   │   ├── UploadZone.tsx
│   │   │   │   │   ├── DocumentoCard.tsx
│   │   │   │   │   └── ValidacaoStatus.tsx
│   │   │   │   └── hooks/
│   │   │   │       └── useUpload.ts
│   │   │   │
│   │   │   ├── assistente/
│   │   │   │   ├── components/
│   │   │   │   │   ├── ChatInterface.tsx
│   │   │   │   │   ├── MensagemBubble.tsx
│   │   │   │   │   └── StreamingText.tsx  # SSE rendering
│   │   │   │   └── hooks/
│   │   │   │       └── useChat.ts         # SSE connection management
│   │   │   │
│   │   │   └── analista/
│   │   │       ├── components/
│   │   │       │   ├── FilaProcessos.tsx
│   │   │       │   ├── DetalheProcessoAnalista.tsx
│   │   │       │   └── DashboardAnalista.tsx
│   │   │       └── pages/
│   │   │           ├── PortalAnalista.tsx
│   │   │           └── VisualizarProcesso.tsx
│   │   │
│   │   └── shared/
│   │       ├── components/            # Design System
│   │       │   ├── Button.tsx
│   │       │   ├── Input.tsx
│   │       │   ├── Modal.tsx
│   │       │   ├── Table.tsx
│   │       │   ├── Badge.tsx
│   │       │   └── Map.tsx            # Mapbox GL JS ou Leaflet
│   │       ├── hooks/
│   │       │   ├── useApi.ts          # React Query + axios wrapper
│   │       │   └── useNotifications.ts
│   │       ├── api/
│   │       │   ├── client.ts          # axios instance com interceptors
│   │       │   └── types.ts           # APIResponse<T>, PaginatedResponse<T>
│   │       └── utils/
│   │           ├── formatters.ts      # datas, CPF, área
│   │           └── validators.ts
│   │
│   └── tests/
│       ├── unit/                      # Vitest
│       └── e2e/                       # Playwright
│           └── fluxo-registro-car.spec.ts
│
├── infra/
│   ├── docker/
│   │   ├── backend.Dockerfile         # Multi-stage: builder + runtime (non-root)
│   │   ├── frontend.Dockerfile        # Nginx serving static build
│   │   └── worker.Dockerfile          # Para workers RabbitMQ
│   │
│   ├── docker-compose.yml             # Ambiente de desenvolvimento local completo
│   ├── docker-compose.test.yml        # Para testes de integração (CI)
│   │
│   ├── k8s/
│   │   ├── base/                      # Kustomize base
│   │   │   ├── namespace.yaml
│   │   │   ├── backend-deployment.yaml
│   │   │   ├── frontend-deployment.yaml
│   │   │   ├── worker-deployment.yaml
│   │   │   ├── services.yaml
│   │   │   ├── ingress.yaml
│   │   │   ├── hpa.yaml
│   │   │   ├── network-policies.yaml
│   │   │   └── external-secrets.yaml  # External Secrets Operator
│   │   │
│   │   └── overlays/
│   │       ├── staging/
│   │       │   ├── kustomization.yaml
│   │       │   └── patches/           # Réplicas menores, sem prod secrets
│   │       └── production/
│   │           ├── kustomization.yaml
│   │           └── patches/           # Réplicas completas, resources finais
│   │
│   └── terraform/                     # IaC para cloud (opcional)
│       ├── main.tf
│       ├── variables.tf
│       └── modules/
│           ├── postgresql/
│           └── kubernetes/
│
├── docs/                              # Esta pasta — documentação do projeto
│   ├── INDEX.md
│   ├── 01-prd/PRD.md
│   ├── 02-event-storming/EVENT_STORMING.md
│   ├── 03-ddd/DDD.md
│   ├── 04-arquitetura/ARQUITETURA.md
│   ├── 05-adrs/
│   ├── 06-modelo-dados/MODELO_DADOS.md
│   ├── 07-apis/API_DESIGN.md
│   ├── 08-seguranca/SEGURANCA.md
│   ├── 09-roadmap/ROADMAP.md
│   ├── 10-estrutura-repositorio/ESTRUTURA.md
│   ├── 11-plano-desenvolvimento/PLANO_DEV.md
│   └── 12-estrategia-testes/TESTES.md
│
├── scripts/
│   ├── seed_dev.py                    # Popular banco de desenvolvimento com dados sintéticos
│   ├── gen_migration.sh               # Helper: cria migration com nome padronizado
│   ├── check_deps.py                  # Verificar CVEs em dependências (Safety)
│   └── create_partitions.py           # Criar partições mensais futuras
│
├── .env.example                       # Template de variáveis de ambiente
├── .gitignore
├── .gitleaks.toml                     # Configuração do gitleaks (detect secrets)
├── .pre-commit-config.yaml            # Hooks: ruff, mypy, gitleaks, conventional commits
├── pyproject.toml                     # Root-level: ruff e mypy config compartilhada
└── README.md
```

---

## Convenções de Nomenclatura

### Python (PEP 8 + Ruff)
| Elemento | Convenção | Exemplo |
|---|---|---|
| Módulos/arquivos | snake_case | `valor_objects.py` |
| Classes | PascalCase | `ProcessoCAR`, `NumeroCAR` |
| Funções/métodos | snake_case | `calcular_area_rl()` |
| Constantes | UPPER_SNAKE_CASE | `MAX_TAMANHO_ARQUIVO` |
| Variáveis privadas | _snake_case | `_domain_events` |
| Type vars | PascalCase | `T = TypeVar('T')` |

### TypeScript/React
| Elemento | Convenção | Exemplo |
|---|---|---|
| Componentes | PascalCase.tsx | `ProcessoStepper.tsx` |
| Hooks | usePascalCase.ts | `useProcessos.ts` |
| Utils | camelCase.ts | `formatters.ts` |
| Tipos/Interfaces | PascalCase | `ProcessoCARResponse` |
| Stores (Zustand) | camelCase + Store | `authStore.ts` |

### Git
| Elemento | Convenção | Exemplo |
|---|---|---|
| Branches | feat/TICKET-desc ou fix/TICKET-desc | `feat/CAR-123-upload-documentos` |
| Commits | Conventional Commits | `feat(processos): adicionar submissão com validação` |
| Tags | v{semver} | `v1.2.3` |
| PRs | Título do commit principal | `feat(auth): integrar Gov.br OAuth2 PKCE` |

### Banco de Dados
| Elemento | Convenção | Exemplo |
|---|---|---|
| Tabelas | snake_case, plural | `processos_car`, `imoveis_rurais` |
| Colunas | snake_case | `data_submissao_at`, `score_completude` |
| Índices | `idx_{tabela}_{coluna(s)}` | `idx_processos_status` |
| Constraints FK | `fk_{tabela}_{coluna}_ref` | `fk_processos_requerente_id_ref` |
| Constraints check | `chk_{tabela}_{regra}` | `chk_processos_area_positiva` |
| Triggers | `trg_{tabela}_{evento}` | `trg_processos_updated_at` |
| Functions | `fn_{descricao}` | `fn_calcular_score_completude` |
| Views | `vw_{descricao}` | `vw_processos_dashboard` |
| Migrations | `YYYY_MM_DD_NNNN_{descricao}.py` | `2024_01_15_0001_initial_schema.py` |

---

## Configuração do Ambiente Local

### Pré-requisitos
- Python 3.13+
- Node.js 20+
- Docker + Docker Compose
- uv (gerenciador de pacotes Python)

### Quick Start

```bash
# 1. Clonar repositório
git clone https://github.com/org/carla.git
cd carla

# 2. Iniciar serviços de infraestrutura
docker compose up -d postgres redis rabbitmq minio

# 3. Instalar dependências Python e configurar ambiente
cd backend
uv sync
cp ../.env.example .env
# Editar .env com suas configurações locais

# 4. Executar migrations e seed
make migrate
make seed-dev

# 5. Iniciar o backend
make dev

# 6. Em outro terminal: iniciar o frontend
cd ../frontend
npm install
npm run dev

# Backend: http://localhost:8000/api/docs
# Frontend: http://localhost:3000
# RabbitMQ UI: http://localhost:15672 (guest/guest)
# MinIO UI: http://localhost:9001 (minioadmin/minioadmin)
```

### Variáveis de Ambiente Principais

```bash
# .env.example
# Database
DATABASE_URL=postgresql+asyncpg://carla:password@localhost:5432/carla_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# RabbitMQ
RABBITMQ_URL=amqp://carla:password@localhost:5672/carla

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_DOCUMENTOS=carla-docs

# LLM
LLM_PRIMARY_PROVIDER=anthropic         # openai | anthropic | ollama
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
OLLAMA_BASE_URL=http://localhost:11434

# Gov.br (mock para dev)
GOVBR_CLIENT_ID=carla-dev
GOVBR_CLIENT_SECRET=dev-secret
GOVBR_MOCK_ENABLED=true               # true para dev, false para prod

# Segurança
JWT_PRIVATE_KEY_PATH=./keys/private.pem
JWT_PUBLIC_KEY_PATH=./keys/public.pem
ENCRYPTION_KEY=dev-encryption-key-32chars  # NÃO usar em produção
CPF_SALT=dev-cpf-salt

# Ambiente
ENVIRONMENT=development               # development | staging | production
LOG_LEVEL=DEBUG
```
