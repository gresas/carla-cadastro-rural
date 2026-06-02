# CARla — Plano de Desenvolvimento

**Versão:** 1.0.0  
**Data:** 2026-06-01

---

## 1. Metodologia

**Scrum adaptado:**
- Hackathon: sprint único de 14 dias com reunião diária de 15min
- MVP Produção: sprints de 2 semanas, planning + retro + review
- Ferramentas: GitHub Issues + Projects, GitHub Actions CI/CD

### Definition of Ready (DoR)
Uma história está pronta para desenvolvimento quando:
- Critérios de aceite escritos e revisados
- Dependências técnicas identificadas
- Estimativa em story points acordada
- Mocks/wireframes disponíveis (se frontend)

### Definition of Done (DoD)
Uma história está concluída quando:
- Código revisado em PR com 2 aprovações
- Cobertura de testes ≥ 80% para novos arquivos
- Testes de integração cobrindo happy path
- SAST sem findings HIGH/CRITICAL
- API documentada (OpenAPI schema atualizado)
- Testado manualmente em staging
- Métricas Prometheus adicionadas
- Zero regressões nos testes existentes

---

## 2. Épicos — MVP Hackathon (2 semanas)

### EPIC-01: Fundação Técnica

**Objetivo:** Repositório configurado, ambiente rodando, banco com schema inicial.

**FEAT-01-01: Setup do Projeto Python**
- US-001: Como dev, quero projeto Python com linting automático para manter qualidade de código
  - Tarefa: Inicializar pyproject.toml com uv + dependências base (FastAPI, SQLAlchemy, Pydantic v2)
  - Tarefa: Configurar Ruff (E, F, I, N, UP, S, B rules)
  - Tarefa: Configurar mypy strict mode
  - Tarefa: Configurar pre-commit hooks (ruff, mypy, gitleaks)
  - Tarefa: GitHub Actions CI básico (lint + test)
  - Estimativa: 4h

**FEAT-01-02: Docker Compose Completo**
- US-002: Como dev, quero subir todos os serviços de infraestrutura com um comando
  - Tarefa: docker-compose.yml com PostgreSQL+PostGIS, Redis, MinIO
  - Tarefa: Configurar extensões PostGIS, pgvector no init script
  - Tarefa: Healthchecks para todos os serviços
  - Tarefa: Volumes persistentes para dados de desenvolvimento
  - Estimativa: 3h

**FEAT-01-03: FastAPI App Factory**
- US-003: Como dev, quero estrutura modular do FastAPI
  - Tarefa: `create_app()` com configuração por ambiente
  - Tarefa: Pydantic BaseSettings com .env
  - Tarefa: Middleware de logging estruturado (JSON)
  - Tarefa: Health endpoint `/health` com status dos serviços
  - Estimativa: 3h

**FEAT-01-04: SQLAlchemy + Alembic**
- US-004: Como dev, quero migrações de banco versionadas
  - Tarefa: Configurar SQLAlchemy 2.0 async + GeoAlchemy2
  - Tarefa: Configurar Alembic com suporte a postgis
  - Tarefa: Migration inicial: ENUMs + tabelas base (users, imoveis_rurais, processos_car, documentos, pendencias)
  - Estimativa: 4h

---

### EPIC-02: Autenticação (Mock para Hackathon)

**Objetivo:** Login simplificado + JWT + RBAC básico para demo.

**FEAT-02-01: Auth Simplificado**
- US-005: Como cidadão, quero fazer login com CPF para acessar o sistema
  - Tarefa: Endpoint POST /api/v1/auth/mock-login (CPF + nome → JWT)
  - Tarefa: JWT RS256 com chave gerada localmente
  - Tarefa: Middleware de validação JWT
  - Tarefa: Roles básicos: produtor_rural, analista_ambiental
  - Estimativa: 5h

**FEAT-02-02: RBAC Básico**
- US-006: Como sistema, quero garantir que cidadão não acessa rotas de analista
  - Tarefa: Decorator/Depends para verificação de role
  - Tarefa: Ownership check para processos
  - Tarefa: Retorno 404 (não 403) para recursos não autorizados
  - Estimativa: 3h

---

### EPIC-03: Gestão de Processos CAR

**Objetivo:** CRUD completo com máquina de estados e upload de documentos.

**FEAT-03-01: Domínio ProcessoCAR**
- US-007: Como sistema, preciso do modelo de domínio ProcessoCAR com invariantes
  - Tarefa: Entidade ProcessoCAR com máquina de estados
  - Tarefa: Value Objects: NumeroCAR, ÁreaTotalHectares, StatusProcesso
  - Tarefa: Testes unitários do domínio (100% cobertura das regras de negócio)
  - Estimativa: 6h

**FEAT-03-02: API de Processos**
- US-008: Como cidadão, quero criar e gerenciar meu processo CAR
  - Tarefa: GET /api/v1/processos (lista paginada)
  - Tarefa: POST /api/v1/processos (criar)
  - Tarefa: GET /api/v1/processos/{id}
  - Tarefa: PATCH /api/v1/processos/{id} (atualizar rascunho)
  - Tarefa: POST /api/v1/processos/{id}/submeter
  - Estimativa: 8h

**FEAT-03-03: Upload de Documentos**
- US-009: Como cidadão, quero fazer upload de documentos do meu imóvel
  - Tarefa: POST /api/v1/documentos/upload (multipart/form-data)
  - Tarefa: Validação de tipo (PDF, JPG, PNG) e tamanho (50MB)
  - Tarefa: Cálculo de hash SHA-256
  - Tarefa: Armazenamento no MinIO
  - Tarefa: Status assíncrono do processamento
  - Estimativa: 6h

**FEAT-03-04: OCR Básico**
- US-010: Como sistema, quero extrair texto de documentos enviados
  - Tarefa: Worker Celery para processamento assíncrono
  - Tarefa: Integração com Tesseract OCR
  - Tarefa: Armazenar texto extraído no banco
  - Tarefa: Atualizar status do documento
  - Estimativa: 5h

---

### EPIC-04: Assistente Inteligente

**Objetivo:** Chat com IA respondendo dúvidas sobre CAR com contexto do processo.

**FEAT-04-01: Adapter LLM**
- US-011: Como sistema, quero abstrair o provider de LLM
  - Tarefa: Interface LLMProvider (ABC)
  - Tarefa: AnthropicAdapter (claude-sonnet-4-6)
  - Tarefa: OllamaAdapter (fallback local)
  - Tarefa: Factory com seleção por configuração
  - Estimativa: 4h

**FEAT-04-02: Base de Conhecimento RAG**
- US-012: Como assistente, quero responder baseado nos normativos do CAR
  - Tarefa: Script para indexar documentos (Lei 12.651, manuais CAR)
  - Tarefa: pgvector: chunking + embedding + armazenamento
  - Tarefa: Busca por similaridade coseno
  - Tarefa: Formatar contexto para prompt do LLM
  - Estimativa: 6h

**FEAT-04-03: API de Conversas com SSE**
- US-013: Como cidadão, quero fazer perguntas sobre CAR e receber respostas em tempo real
  - Tarefa: POST /api/v1/assistente/conversas (criar)
  - Tarefa: POST /api/v1/assistente/conversas/{id}/mensagens (SSE streaming)
  - Tarefa: StreamingResponse com generator assíncrono
  - Tarefa: Salvar mensagens no banco
  - Estimativa: 6h

**FEAT-04-04: Contexto do Processo**
- US-014: Como cidadão, quero que o assistente saiba do meu processo
  - Tarefa: Injetar dados do processo no system prompt
  - Tarefa: Classificação básica de intenção (dúvida, status, documento)
  - Tarefa: Resposta contextualizada com dados do processo
  - Estimativa: 4h

---

### EPIC-05: Portal do Cidadão (Frontend)

**Objetivo:** Interface React funcional para demo.

**FEAT-05-01: Setup Frontend**
- Tarefa: Vite + React 18 + TypeScript + Tailwind CSS + shadcn/ui
- Tarefa: React Query para estado servidor
- Tarefa: Zustand para estado cliente
- Tarefa: axios com interceptors (auth token, error handling)
- Estimativa: 4h

**FEAT-05-02: Auth e Layout**
- US-015: Como cidadão, quero fazer login e ver dashboard
  - Tarefa: Tela de login com "Entrar com Gov.br" (mock)
  - Tarefa: Layout principal (sidebar, header, notificações)
  - Tarefa: Rota protegida com redirect para login
  - Estimativa: 4h

**FEAT-05-03: Novo Processo (Stepper)**
- US-016: Como cidadão, quero criar meu processo passo a passo
  - Tarefa: Componente Stepper com 4 etapas
  - Tarefa: Formulário de dados do imóvel (Etapa 1)
  - Tarefa: Área de upload de documentos (Etapa 2)
  - Tarefa: Revisão e submissão (Etapa 3)
  - Estimativa: 10h

**FEAT-05-04: Upload com Feedback Visual**
- US-017: Como cidadão, quero ver o progresso do upload e validação
  - Tarefa: DropZone com drag-and-drop
  - Tarefa: Progress bar durante upload
  - Tarefa: Polling do status de validação
  - Tarefa: Exibição de erro com instrução de correção
  - Estimativa: 6h

**FEAT-05-05: Chat com Assistente**
- US-018: Como cidadão, quero conversar com o assistente IA
  - Tarefa: Interface de chat com histórico
  - Tarefa: Streaming de texto (SSE → tokens na tela)
  - Tarefa: Botões de pergunta rápida frequente
  - Estimativa: 6h

**FEAT-05-06: Dashboard do Cidadão**
- US-019: Como cidadão, quero ver o status dos meus processos
  - Tarefa: Cards de processos com status colorido
  - Tarefa: Barra de completude animada
  - Tarefa: Lista de pendências em destaque
  - Estimativa: 4h

---

### EPIC-06: Portal do Analista (Frontend)

**FEAT-06-01: Fila de Processos**
- US-020: Como analista, quero ver fila de processos ordenada por prioridade
  - Tarefa: Tabela com filtros (status, prioridade, data)
  - Tarefa: Score de completude e risco visíveis
  - Tarefa: Botão "Assumir" processo
  - Estimativa: 6h

**FEAT-06-02: Visualização Detalhada**
- US-021: Como analista, quero ver todos os dados do processo em uma tela
  - Tarefa: Layout two-column: dados + documentos/histórico
  - Tarefa: Visualização de documentos (preview de PDF/imagem)
  - Tarefa: Timeline do histórico do processo
  - Tarefa: Botões de ação (aprovar, rejeitar, criar pendência)
  - Estimativa: 8h

**FEAT-06-03: Aprovação e Rejeição**
- US-022: Como analista, quero aprovar ou rejeitar processos
  - Tarefa: Modal de aprovação com campo observações
  - Tarefa: Modal de rejeição com motivo obrigatório
  - Tarefa: Confirmação antes de ação irreversível
  - Estimativa: 4h

---

## 3. Histórias de Usuário Completas (Gherkin)

### US-CAR-001: Cidadão inicia novo processo CAR

**Como** produtor rural autenticado,  
**Quero** iniciar um novo processo de registro CAR,  
**Para** cadastrar meu imóvel rural no sistema.

```gherkin
Cenário: Cidadão inicia processo com sucesso
  Dado que João está autenticado com nível de confiabilidade "prata"
  E não possui processo CAR em aberto para o imóvel X
  Quando acessar "Novo Processo" e preencher os dados básicos
    | campo       | valor            |
    | nome_imovel | Fazenda Boa Vista|
    | municipio   | São Luís - MA    |
    | area_ha     | 50.0             |
  Então um processo no status "rascunho" deve ser criado
  E o processo deve aparecer no dashboard de João
  E o assistente IA deve apresentar os próximos passos

Cenário: Cidadão tenta iniciar segundo processo simultâneo
  Dado que João já possui processo no status "em_preenchimento"
  Quando tentar criar novo processo para o mesmo imóvel
  Então deve ver mensagem informando que já tem processo em andamento
  E deve ser direcionado para o processo existente

Cenário: Município informado não encontrado no IBGE
  Dado que João está preenchendo o formulário
  Quando informar "Municipio Inexistente - XX"
  Então deve ver mensagem de erro com sugestões de municípios similares
  E o processo não deve ser criado
```

---

### US-CAR-002: Cidadão faz upload de documento

```gherkin
Cenário: Upload de PDF válido bem-sucedido
  Dado que João tem processo no status "em_preenchimento"
  Quando fazer upload de "matricula.pdf" do tipo "matricula_imovel"
    | propriedade | valor |
    | tamanho     | 2MB   |
    | tipo_mime   | application/pdf |
  Então o documento deve aparecer com status "Aguardando validação"
  E após até 60 segundos o status deve mudar para "Válido" ou "Inválido"
  E o score de completude do processo deve aumentar se válido

Cenário: Upload de arquivo muito grande
  Quando tentar fazer upload de arquivo com 60MB
  Então deve ver erro "Arquivo muito grande. Limite: 50MB"
  E o arquivo não deve ser armazenado

Cenário: Upload de tipo de arquivo não suportado
  Quando tentar fazer upload de arquivo .docx
  Então deve ver erro com lista de tipos aceitos
```

---

### US-CAR-003: Cidadão conversa com assistente IA

```gherkin
Cenário: Pergunta sobre CAR respondida com base de conhecimento
  Dado que Ana está autenticada
  Quando perguntar "O que é área de preservação permanente?"
  Então deve receber resposta em streaming (tokens aparecem progressivamente)
  E a resposta deve citar a Lei 12.651/2012
  E deve ter link para a fonte do conhecimento

Cenário: Assistente responde com contexto do processo
  Dado que João tem processo com pendência de geometria
  Quando perguntar "O que está faltando no meu processo?"
  Então o assistente deve citar a pendência específica de João
  E oferecer orientação para resolver aquela pendência específica

Cenário: Pergunta fora do domínio CAR
  Quando perguntar "Qual o resultado da Copa do Mundo?"
  Então o assistente deve explicar educadamente que responde apenas sobre CAR
  E sugerir perguntas relevantes sobre o processo do usuário
```

---

### US-CAR-004: Analista aprova processo

```gherkin
Cenário: Analista aprova processo completo
  Dado que Carlos (analista) está autenticado
  E o processo "PR-2024-001" está no status "em_analise"
  E Carlos é o analista responsável
  E o processo tem todos os documentos válidos e sem pendências abertas
  Quando Carlos clicar em "Aprovar" e confirmar
  Então o processo deve mudar para status "aprovado"
  E um número CAR deve ser gerado
  E o cidadão deve receber notificação de aprovação
  E o histórico deve registrar a aprovação com o ID de Carlos

Cenário: Analista tenta aprovar processo com pendências
  Dado que o processo tem 2 pendências abertas
  Quando Carlos tentar aprovar
  Então deve ver mensagem indicando as pendências em aberto
  E o botão de aprovação deve estar desabilitado

Cenário: Analista tenta aprovar processo de outro analista
  Dado que o processo está atribuído ao analista Maria
  Quando Carlos tentar aprovar
  Então deve ver erro "Apenas o analista responsável pode aprovar este processo"
```

---

## 4. Tarefas Técnicas Transversais

| # | Tarefa | Área | Estimativa | Sprint |
|---|---|---|---|---|
| TT-01 | Configurar structured logging JSON com trace_id | Infra | 3h | 1 |
| TT-02 | Health checks (liveness, readiness) em todos os serviços | Infra | 2h | 1 |
| TT-03 | Configurar Prometheus metrics endpoint | Observabilidade | 3h | 1 |
| TT-04 | Instrumentação OpenTelemetry (traces) | Observabilidade | 4h | 2 |
| TT-05 | Grafana dashboards: operacional + negócio | Observabilidade | 4h | 2 |
| TT-06 | Rate limiting Nginx por IP e por role | Segurança | 2h | 1 |
| TT-07 | CORS configurado por ambiente | Segurança | 1h | 1 |
| TT-08 | Security headers HTTP (CSP, HSTS, etc.) | Segurança | 2h | 1 |
| TT-09 | Swagger/OpenAPI customizado com exemplos | Docs | 3h | 2 |
| TT-10 | Seed de dados de desenvolvimento (factory_boy) | Testes | 4h | 1 |
| TT-11 | Configurar TestContainers para testes de integração | Testes | 3h | 2 |
| TT-12 | Pipeline CI completo (lint, test, security scan) | CI/CD | 4h | 1 |
| TT-13 | Audit log trigger automático no banco | Auditoria | 3h | 2 |
| TT-14 | Partições mensais automáticas (cron script) | Banco | 2h | 2 |
| TT-15 | Configurar pgvector índice IVFFLAT | Banco | 2h | 1 |

---

## 5. Estimativas e Cronograma

### Hackathon (14 dias — equipe de 4 pessoas)

| Dia | Backend | Frontend | DevOps/Infra |
|---|---|---|---|
| 1-2 | EPIC-01 Fundação + EPIC-02 Auth | Setup frontend + Auth UI | Docker Compose + CI |
| 3-4 | EPIC-03 Domínio + API Processos | Dashboard cidadão | Banco + migrations |
| 5-6 | EPIC-03 Upload + OCR básico | Stepper Novo Processo | MinIO setup |
| 7-8 | EPIC-04 LLM Adapter + RAG | Chat Interface + SSE | — |
| 9-10 | EPIC-04 Contexto + Classificação | Upload com feedback visual | Seed de dados |
| 11-12 | EPIC-06 API Analista + Aprovação | Portal do Analista | — |
| 13 | Integração backend-frontend + bugs | Refinamentos UX | Observabilidade básica |
| 14 | Buffer + demo preparation | Demo data + polimento | Deploy Docker Compose demo |

### MVP Produção (12 semanas — equipe de 6 pessoas)

| Semanas | Épicos em Paralelo | Marco |
|---|---|---|
| 1-2 | E1 (Fundação) + E2 (Gov.br) | Ambiente staging operacional |
| 3-4 | E3 (Portal Cidadão início) + E2 finalização | Login Gov.br real funcionando |
| 5-6 | E3 (Portal continuação) + E4 (Assistente) | Upload e validação funcionando |
| 7-8 | E4 (Assistente finalização) + E5 (Validação) + E6 início | Chat IA em produção |
| 9-10 | E5 (Validação finalização) + E6 (Analista) + E7 início | Portal analista operacional |
| 11-12 | E7 (Integrações) + Hardening + Testes de carga | Piloto com usuários reais |

---

## 6. Métricas de Progresso

| Métrica | Target Hackathon | Target MVP |
|---|---|---|
| Cobertura de testes | 60% | 80% |
| Story points/sprint | N/A (hackathon) | 40 SP/sprint |
| Bugs críticos abertos | 0 | 0 |
| Security findings HIGH/CRITICAL | 0 | 0 |
| Uptime (staging) | N/A | ≥ 99% |
| Tempo de build CI | < 10min | < 15min |
| Latência p95 API | < 1s | < 500ms |
