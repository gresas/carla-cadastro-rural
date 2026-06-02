# CARla — Roadmap

**Versão:** 1.0.0  
**Data:** 2026-06-01

---

## Linha do Tempo

```
Semana 1-2         Mês 1-3              Mês 4-15
┌──────────────┐   ┌───────────────────┐   ┌────────────────────────┐
│  Fase 1      │   │     Fase 2        │   │       Fase 3           │
│  MVP         │──►│   MVP Produção    │──►│   Versão Escalável     │
│  Hackathon   │   │                   │   │                        │
│  (2 semanas) │   │  (12 semanas)     │   │  (12 meses)            │
└──────────────┘   └───────────────────┘   └────────────────────────┘
    Demo           Operação real           Produto governamental
    funcional      controlada              em escala
```

---

## Fase 1 — MVP Hackathon (2 semanas)

### Objetivo
Demonstrar o valor central da solução para os juízes: um produtor rural consegue iniciar um processo CAR com ajuda de IA, enviar documentos e receber orientação em tempo real.

### Arquitetura Simplificada

```
┌─────────────────────────────────────────────┐
│          MONOLITO MODULAR (FastAPI)          │
│                                              │
│  Módulos internos: auth, processos,          │
│  documentos, assistente                      │
│                                              │
│  ← Não microsserviços (complexidade          │
│    desnecessária para hackathon)             │
└────────────────────┬────────────────────────┘
                     │
     ┌───────────────┼──────────────────┐
     │               │                  │
     ▼               ▼                  ▼
PostgreSQL+      Redis              Claude API
PostGIS                           (Anthropic)
(local Docker)                    (via adapter)
```

**Decisão:** Mock do Gov.br para login (CPF + nome via formulário simples para demo)  
**Decisão:** Sem RabbitMQ — operações assíncronas via Celery + Redis simples  
**Decisão:** MinIO local para armazenamento de documentos  
**Decisão:** Docker Compose para orquestração local

### Funcionalidades Mínimas Demonstráveis

| # | Funcionalidade | Critério de Aceite |
|---|---|---|
| F01 | Login simulado (mock Gov.br) | Usuário entra com CPF e vê dashboard |
| F02 | Criar novo processo CAR | Formulário simples com dados do imóvel |
| F03 | Upload de documento (PDF/JPG) | Arquivo salvo no MinIO, status atualizado |
| F04 | OCR básico de documento | Texto extraído exibido na tela |
| F05 | Chat com assistente IA | Resposta streaming sobre dúvidas de CAR |
| F06 | Contexto do processo no chat | Assistente sabe qual processo o usuário tem |
| F07 | Status do processo | Dashboard mostra etapa atual e completude |
| F08 | Fila de processos (analista) | Analista vê lista de processos pendentes |
| F09 | Aprovar/rejeitar processo | Analista muda status com motivo |
| F10 | Notificação in-app | Cidadão recebe alerta de mudança de status |

### O que NÃO está no Hackathon

- Integração real com Gov.br (mock)
- Integração com SICAR, SIGEF, IBAMA
- Envio de email real
- Geração de dossiê PDF
- Valição geoespacial completa
- Autenticação em nível ouro
- Alta disponibilidade
- Kubernetes
- Análise antivírus de uploads
- Multi-analista / supervisão

### Critérios de Sucesso do Hackathon

1. Demo ao vivo sem travar por 5 minutos
2. Cidadão completa fluxo: login → criar processo → upload → chat → status (< 3 min)
3. Analista consegue ver processo e aprovar (< 1 min)
4. Assistente responde corretamente 3 perguntas sobre CAR
5. Score de completude reflete documentos enviados em tempo real
6. Interface responsiva e visualmente profissional

### Backlog Hackathon (MoSCoW)

| Feature | Prioridade | Estimativa | Entregável |
|---|---|---|---|
| Setup Docker Compose + FastAPI | Must | 4h | Ambiente rodando |
| Schema PostgreSQL inicial | Must | 3h | Banco de dados |
| Auth mock (CPF + nome) | Must | 2h | Login funcional |
| CRUD de Processo CAR | Must | 6h | API + frontend |
| Upload de documentos | Must | 4h | Multipart + MinIO |
| OCR básico (Tesseract) | Must | 4h | Texto extraído |
| Chat com Claude API | Must | 6h | Streaming SSE |
| RAG com normativos CAR | Must | 4h | Respostas embasadas |
| Frontend React + Tailwind | Must | 16h | Interface cidadão |
| Portal do analista (básico) | Must | 8h | Fila + aprovação |
| Dashboard de status | Should | 4h | Completude visual |
| Notificação in-app | Should | 3h | Badge no menu |
| Validação de geometria básica | Could | 4h | Shapefile upload |
| Geração de dossiê simples | Could | 4h | PDF texto |
| Modo demo com dados pré-carregados | Should | 2h | Seed de dados |

---

## Fase 2 — MVP Produção (12 semanas)

### Objetivo
Primeira versão operacional real, integrada com Gov.br, processando processos CAR reais em ambiente controlado de piloto.

### Épicos e Cronograma

```
Semana: 1  2  3  4  5  6  7  8  9  10  11  12
────────────────────────────────────────────────────
E1: Fundação ████████
E2: Auth Gov.br   ████████
E3: Portal Cidadão   ████████████████
E4: Assistente IA       ████████████████
E5: Motor Validação         ████████████████
E6: Portal Analista              ████████████████
E7: Integrações                      ████████████
E8: Observabilidade ████████████████████████████████
E9: Segurança LGPD  ████████████████████████████████
```

### Épico 1: Fundação de Plataforma (Semanas 1-3)

**F1.1 — Infraestrutura Docker/K8s**
- Docker Compose para desenvolvimento local completo
- Dockerfile otimizado por serviço (multi-stage build)
- Helm charts básicos para Kubernetes (staging)
- Secrets management com Vault

**F1.2 — CI/CD Pipeline (GitHub Actions)**
- CI: lint (ruff, mypy), testes unitários, testes de integração, SAST
- CD staging: deploy automático em cada push na `develop`
- CD production: deploy com aprovação manual
- Semantic versioning com conventional commits

**F1.3 — Observabilidade Base**
- Structured logging (JSON) com trace_id em todos os serviços
- Prometheus metrics endpoint em cada serviço
- Grafana dashboards: operacional, negócio, infraestrutura
- Alertas críticos configurados (PagerDuty ou equivalente)

**F1.4 — Segurança e LGPD Foundation**
- pgcrypto para CPF e email
- HashiCorp Vault para segredos
- Audit log trigger em tabelas críticas
- Política de retenção de dados configurada

### Épico 2: Identidade e Acesso Real (Semanas 2-4)

**F2.1 — Integração Gov.br**
- OAuth2 Authorization Code + PKCE com Gov.br
- Mapeamento de claims Gov.br para modelo de usuário
- Níveis de confiabilidade: bronze/prata/ouro
- Fallback para modo manutenção

**F2.2 — RBAC Completo**
- 5 roles implementados com matriz de permissões
- Ownership check em todos os recursos
- Middleware de autorização com cache de permissões no Redis

**F2.3 — Gestão de Sessões Segura**
- JWT RS256 com rotação de chaves via Vault
- Refresh token rotation
- Blacklist no Redis
- Rate limiting por IP + por CPF para autenticação

### Épico 3: Portal do Cidadão (Semanas 3-8)

**F3.1 — Registro e Perfil**
- Tela de boas-vindas pós-login Gov.br
- Visualização e edição de dados do perfil
- Central de privacidade (direitos LGPD)

**F3.2 — Formulário CAR Passo a Passo**
- Stepper com 5 etapas: dados básicos, dados do imóvel, documentos, geometria, revisão
- Validação em tempo real por etapa
- Salvamento automático de rascunho
- Indicador de completude dinâmico

**F3.3 — Upload e Validação Documental**
- Upload multipart com progress bar
- Feedback visual em tempo real (aguardando → processando → válido/inválido)
- Orientações claras para cada tipo de documento
- Reenvio de documento após rejeição

**F3.4 — Acompanhamento de Status**
- Dashboard com todos os processos do cidadão
- Linha do tempo visual do processo
- Lista de pendências com instruções de resolução
- Prazo de análise estimado

**F3.5 — Notificações Email**
- Templates de email para cada evento do processo
- Unsubscribe (respeito ao titular LGPD)
- Email transacional via SendGrid ou equivalente

### Épico 4: Assistente Inteligente (Semanas 4-9)

**F4.1 — Chat com Base de Conhecimento CAR**
- Interface de chat com streaming SSE
- RAG com Lei 12.651, manuais SICAR, FAQ
- Respostas com indicação de fonte
- Feedback de utilidade por resposta

**F4.2 — Classificação de Intenção**
- 6 classes de intenção identificadas e roteadas
- Confiança mínima para resposta automática
- Escalonamento quando confiança baixa

**F4.3 — Contexto do Processo**
- Assistente acessa status, documentos e pendências do processo ativo
- Respostas personalizadas com dados do processo do usuário
- Solicitação de documento específico com link de upload

**F4.4 — Escalonamento Humano**
- Detecção de frustração/reclamação
- Notificação para analista disponível
- Contexto da conversa enviado ao analista

### Épico 5: Motor de Validação (Semanas 5-10)

**F5.1 — OCR de Documentos**
- Tesseract para fallback local
- Google Vision API ou Azure Form Recognizer como primário
- Pré-processamento de imagem (deskew, enhance)
- Retry com engine diferente se confiança < 70%

**F5.2 — Extração de Dados Estruturados**
- Extração por tipo de documento (matrícula, CCIR, planta)
- Validação de formato dos campos extraídos
- Score de confiança por campo

**F5.3 — Validação de Consistência**
- Comparação de área entre documentos (tolerância 5%)
- Verificação de proprietário vs. CPF cadastrado
- Cruzamento com dados IBGE (município existe?)

**F5.4 — Cruzamento com IBGE**
- Validar municípios via tabela IBGE (shapefile público)
- Verificar se geometria está no município declarado

### Épico 6: Portal do Analista (Semanas 7-11)

**F6.1 — Fila de Processos com Filtros**
- Lista com filtros: status, município, prioridade, analista, data
- Ordenação por prioridade e tempo na fila
- Busca por número CAR ou nome do requerente

**F6.2 — Visualização Completa do Processo**
- Todos os dados em uma tela: dados do imóvel, documentos, pendências, histórico
- Visualização de mapa com geometria do imóvel
- Score de completude e risco com justificativa

**F6.3 — Geração de Dossiê Automático**
- Trigger automático quando analista assume processo
- LLM gera resumo executivo em linguagem técnica
- PDF com: dados, documentos validados, mapa, alertas, análise

**F6.4 — Aprovação/Rejeição**
- Fluxo de aprovação com confirmação e observações opcionais
- Rejeição exige motivo + código padronizado
- Registro imutável no histórico

**F6.5 — Dashboard de Produtividade**
- Processos analisados por dia/semana/mês
- Tempo médio de análise
- Comparativo entre analistas (supervisor)

### Épico 7: Integrações Externas (Semanas 8-12)

**F7.1 — Consulta SICAR**
- Verificação de registros CAR anteriores pelo CPF
- Verificação de sobreposição geográfica
- Circuit breaker + cache 24h

**F7.2 — Verificação IBGE**
- Validação de código de município
- Download e indexação do shapefile de municípios

**F7.3 — Abstração para SIGEF/INCRA**
- Interface SistemaFundiárioAdapter implementada com mock
- Stub configurável para ambientes de teste
- Documentação para integração real futura

### Definição de Pronto (DoD)

Uma feature está pronta quando:
1. Código revisado em PR com aprovação de 2 reviewers
2. Testes unitários: cobertura ≥ 80% dos novos arquivos
3. Testes de integração cobrindo caminho feliz e erros comuns
4. SAST sem findings HIGH/CRITICAL
5. Documentação de API atualizada (OpenAPI)
6. Testado manualmente em staging
7. Métricas Prometheus adicionadas para a feature
8. Logs estruturados com trace_id
9. Revisão de segurança (ownership check, validações de entrada)
10. Nenhuma regressão nos testes existentes

---

## Fase 3 — Versão Escalável (Meses 4-15)

### Objetivo
Plataforma robusta e escalável, com integrações completas, capacidade para processamento em escala estadual/nacional e qualidade de produto governamental.

### Épico A: Migração para Microsserviços (Meses 4-7)

Decomposição do monolito modular em serviços independentes usando **Strangler Fig Pattern**:
1. Extrair Auth Service (primeiro — menor dependência)
2. Extrair Document Service (worker de OCR independente)
3. Extrair AI Assistant Service
4. Extrair Analytics Service
5. Process Service permanece como core — extrair por último

API Gateway (Kong ou NGINX Plus) para roteamento.  
Service Mesh (Linkerd ou Istio) para mTLS automático.

### Épico B: Integrações Completas (Meses 5-9)

| Sistema | Funcionalidade | Complexidade |
|---|---|---|
| SIGEF | Verificação de georreferenciamento certificado | Alta — API não pública |
| INCRA | Consulta de módulos fiscais por município | Média — CSV público |
| MapBiomas | Classificação de uso do solo do imóvel | Média — API REST disponível |
| PRODES/DETER | Score de risco de desmatamento no histórico | Média — API INPE disponível |
| ICMBio | Verificação de sobreposição com Unidades de Conservação | Alta — shapefile complexo |
| FUNAI | Verificação de sobreposição com Terras Indígenas | Alta — shapefile complexo |

### Épico C: IA Avançada (Meses 6-12)

**C1 — Análise Geoespacial Automatizada**
- Verificação de sobreposição com APPs (cursos d'água, encostas) via PostGIS
- Cálculo automático de área de Reserva Legal por bioma
- Integração com base do MapBiomas para uso do solo em 2008 (Lei 12.651, Art. 29)

**C2 — LLM Fine-tuning para Domínio CAR**
- Dataset de Q&A especializado em CAR
- Fine-tuning de modelo open-source (Llama) para português jurídico ambiental
- Redução de custo com LLM externo em 70%

**C3 — Scoring Preditivo**
- Modelo ML para prever probabilidade de aprovação
- Identificação antecipada de processos de alto risco
- Priorização inteligente da fila do analista

**C4 — Assistente para Analista**
- Sugestão de motivos de pendência baseado em casos similares
- Análise comparativa com processos da mesma região aprovados
- Checklist de análise gerado automaticamente por tipo de imóvel

### Épico D: Analytics e BI (Meses 7-10)

- Dashboard gerencial para órgãos estaduais com KPIs por município/região
- Relatórios de conformidade exportáveis (CSV, Excel, PDF)
- API de dados abertos (anonimizados) para pesquisadores
- Integração com BI governamental (Power BI, Metabase)

### Épico E: Escalabilidade (Meses 8-12)

- **Multi-tenancy:** Um deployment para múltiplos estados (namespace isolation no K8s)
- **Processamento em lote:** Import de shapefiles ZIP com múltiplos imóveis
- **CDN:** Assets geoespaciais (mapas, imagens de satélite) via CDN
- **Caching avançado:** Cache geoespacial de consultas IBGE/INCRA
- **Read replicas:** Queries de dashboard apontam para réplica PostgreSQL

### Épico F: App Mobile (Meses 10-15)

- React Native para iOS e Android
- Câmera para captura de documentos com OCR on-device
- Notificações push nativas
- Funcionalidade offline para preenchimento sem conexão

---

## Riscos do Roadmap

| Risco | Fase | Prob. | Impacto | Mitigação | Contingência |
|---|---|---|---|---|---|
| Gov.br API sem SLA adequado | F2 | M | A | Sessions longas, monitoramento | Modo degradado para servidores |
| SICAR sem API pública estável | F2, F3 | A | M | ACL + mock + cache agressivo | Processo sem dados SICAR com flag |
| Custo LLM em escala | F2, F3 | M | M | Cache semântico + Ollama local | Limite de tokens por sessão |
| Resistência de servidores à mudança | F2 | M | M | Champions program, treinamento | Adoção gradual opcional |
| Mudança legislativa no CAR | F3 | B | A | Regras no RAG (configurável) | Atualização da base de conhecimento |
| Equipe insuficiente para escala | F3 | M | A | Documentação técnica robusta | Contratação ou parceria |

---

## KPIs de Aceitação por Fase

### Hackathon
- Demo ao vivo sem falha crítica
- 3 juízes conseguem usar o sistema sem instrução prévia

### MVP Produção (após 3 meses)
- 100 processos criados por usuários reais
- NPS ≥ 60
- Uptime ≥ 99% em 30 dias
- Zero incidentes de segurança P0/P1

### Versão Escalável (após 12 meses)
- 10.000 processos/mês em pelo menos 1 estado
- NPS ≥ 70
- Taxa de aprovação na 1ª tentativa ≥ 70%
- Tempo médio de análise ≤ 15 dias úteis
