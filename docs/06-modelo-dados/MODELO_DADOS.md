# CARla — Modelo de Dados

**Versão:** 1.0.0  
**Data:** 2026-06-01  
**Stack:** PostgreSQL 16, PostGIS 3.4, pgvector, pgcrypto, SQLAlchemy 2.0, Alembic

---

## 1. Princípios do Modelo

- **UUIDs como PKs:** `gen_random_uuid()` gerado pelo banco — sem dependência do ORM
- **Auditoria universal:** `created_at`, `updated_at` em todas as tabelas; trigger automático para `updated_at`
- **Soft delete:** `deleted_at TIMESTAMPTZ nullable` — nunca deletar registros de negócio
- **SIRGAS 2000:** SRID 4674 para todos os dados geoespaciais (padrão brasileiro oficial)
- **pgcrypto:** CPF e email criptografados em repouso; hash SHA-256 do CPF para busca
- **pgvector:** Embeddings de 1536 dimensões para RAG do assistente IA
- **Particionamento:** Tabelas de alta escrita (audit_logs, historico_processos) particionadas por mês
- **Imutabilidade:** Tabelas de auditoria e histórico — apenas INSERT (sem UPDATE/DELETE)
- **Outbox Pattern:** Tabela `outbox` para garantia de entrega de eventos

---

## 2. Diagrama ER

```
┌──────────────┐  1     N  ┌──────────────────┐
│    users     │──────────►│  imoveis_rurais  │
│  (cidadão,   │           │  (geometria      │
│   analista,  │           │   PostGIS)       │
│   admin)     │           └────────┬─────────┘
└──────┬───────┘                    │ 1
       │ 1                          │
       │                            │ N
       │ N          ┌───────────────▼──────┐
       └───────────►│   processos_car      │
                    │  (máquina de estados)│
                    └─┬──────┬─────────┬───┘
                      │1     │1        │1
                      │      │         │
                      │N     │N        │N
              ┌───────▼┐  ┌──▼──────┐  ┌─▼──────────────┐
              │documen-│  │pendên-  │  │historico_       │
              │  tos   │  │  cias   │  │processos        │
              └────────┘  └─────────┘  └─────────────────┘

┌──────────────┐  1     N  ┌──────────────┐  1     N  ┌─────────────┐
│    users     │──────────►│  conversas   │──────────►│  mensagens  │
└──────────────┘           └──────────────┘           └─────────────┘

┌─────────────────────┐    ┌──────────────────┐    ┌─────────────┐
│  integracoes_       │    │  notificacoes    │    │  audit_logs │
│  externas           │    │                  │    │ (particiod) │
└─────────────────────┘    └──────────────────┘    └─────────────┘

┌──────────────────┐    ┌──────────────────┐
│  knowledge_base  │    │     outbox       │
│  (pgvector RAG)  │    │  (domain events) │
└──────────────────┘    └──────────────────┘
```

---

## 3. DDL Completo

### Extensões

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";
```

### ENUMs

```sql
CREATE TYPE tipo_usuario_enum AS ENUM (
    'produtor_rural', 'consultor_ambiental', 'analista_ambiental',
    'supervisor_ambiental', 'admin'
);

CREATE TYPE nivel_confiabilidade_enum AS ENUM ('bronze', 'prata', 'ouro');

CREATE TYPE tipo_imovel_enum AS ENUM (
    'minifundio', 'pequena_propriedade', 'media_propriedade', 'grande_propriedade'
);

CREATE TYPE status_processo_enum AS ENUM (
    'rascunho', 'em_preenchimento', 'aguardando_documentos',
    'submetido', 'em_analise', 'pendente', 'em_correcao',
    'aprovado', 'rejeitado', 'recurso', 'cancelado'
);

CREATE TYPE prioridade_enum AS ENUM ('baixa', 'normal', 'alta', 'urgente');

CREATE TYPE tipo_documento_enum AS ENUM (
    'matricula_imovel', 'ccir', 'planta_georeferenciada', 'memorial_descritivo',
    'car_anterior', 'declaracao_area', 'certidao_negativa', 'procuracao', 'outros'
);

CREATE TYPE status_documento_enum AS ENUM (
    'aguardando', 'processando', 'valido', 'invalido', 'rejeitado'
);

CREATE TYPE tipo_pendencia_enum AS ENUM (
    'documentacao_faltante', 'documento_invalido', 'geometria_inconsistente',
    'dado_conflitante', 'area_divergente', 'complementacao_necessaria', 'outro'
);

CREATE TYPE status_pendencia_enum AS ENUM ('aberta', 'em_correcao', 'resolvida', 'cancelada');

CREATE TYPE role_mensagem_enum AS ENUM ('user', 'assistant', 'system');

CREATE TYPE status_conversa_enum AS ENUM ('ativa', 'encerrada', 'escalonada');

CREATE TYPE sistema_externo_enum AS ENUM (
    'sicar', 'sigef', 'incra', 'ibama', 'mapbiomas', 'govbr', 'prodes', 'deter', 'icmbio', 'funai'
);

CREATE TYPE status_integracao_enum AS ENUM ('pendente', 'sucesso', 'falha', 'timeout', 'circuit_aberto');

CREATE TYPE canal_notificacao_enum AS ENUM ('email', 'sms', 'push', 'inapp');

CREATE TYPE status_notificacao_enum AS ENUM ('pendente', 'enviada', 'falha', 'lida');

CREATE TYPE operacao_audit_enum AS ENUM ('INSERT', 'UPDATE', 'DELETE');

CREATE TYPE status_outbox_enum AS ENUM ('pendente', 'publicado', 'falhou');
```

### Tabela: users

```sql
CREATE TABLE users (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- CPF armazenado criptografado (pgcrypto) e como hash para busca
    cpf_hash              CHAR(64) NOT NULL UNIQUE,  -- SHA256(cpf || salt)
    cpf_encrypted         BYTEA NOT NULL,            -- pgp_sym_encrypt(cpf, key)
    email_hash            CHAR(64),                  -- SHA256(email || salt)
    email_encrypted       BYTEA,                     -- pgp_sym_encrypt(email, key)
    nome_completo         VARCHAR(255) NOT NULL,
    tipo_usuario          tipo_usuario_enum NOT NULL,
    govbr_sub             VARCHAR(255) UNIQUE,       -- Subject do JWT Gov.br
    nivel_confiabilidade  nivel_confiabilidade_enum,
    ativo                 BOOLEAN NOT NULL DEFAULT true,
    ultimo_acesso_at      TIMESTAMPTZ,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at            TIMESTAMPTZ
);

COMMENT ON TABLE users IS 'Usuários do sistema. CPF e email criptografados com pgcrypto (LGPD).';
COMMENT ON COLUMN users.cpf_hash IS 'SHA256(cpf_digits || app_salt) — permite busca sem descriptografar';
COMMENT ON COLUMN users.govbr_sub IS 'Subject do token OIDC do Gov.br — identificador único do cidadão';
```

### Tabela: sessions

```sql
CREATE TABLE sessions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id),
    token_hash  CHAR(64) NOT NULL UNIQUE,  -- SHA256(jti) para blacklist
    ip_address  INET,
    user_agent  TEXT,
    expires_at  TIMESTAMPTZ NOT NULL,
    revogada_em TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Tabela: imoveis_rurais

```sql
CREATE TABLE imoveis_rurais (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id),
    nome_imovel             VARCHAR(255) NOT NULL,
    codigo_incra            VARCHAR(20),
    municipio_ibge          CHAR(7) NOT NULL,  -- Código IBGE 7 dígitos
    estado                  CHAR(2) NOT NULL,
    area_total_ha           NUMERIC(15, 4) NOT NULL CHECK (area_total_ha > 0),
    area_app_ha             NUMERIC(15, 4) CHECK (area_app_ha >= 0),
    area_reserva_legal_ha   NUMERIC(15, 4) CHECK (area_reserva_legal_ha >= 0),
    area_uso_restrito_ha    NUMERIC(15, 4) CHECK (area_uso_restrito_ha >= 0),
    area_consolidada_ha     NUMERIC(15, 4) CHECK (area_consolidada_ha >= 0),
    geometria               GEOMETRY(MULTIPOLYGON, 4674),  -- SIRGAS 2000
    modulo_fiscal_ha        NUMERIC(6, 2),
    bioma                   VARCHAR(50),
    tipo_imovel             tipo_imovel_enum,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at              TIMESTAMPTZ,

    CONSTRAINT chk_rl_menor_total CHECK (
        area_reserva_legal_ha IS NULL OR area_reserva_legal_ha <= area_total_ha
    )
);
```

### Tabela: processos_car

```sql
CREATE TABLE processos_car (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_car          VARCHAR(50) UNIQUE,  -- NULL até aprovação; formato: UF-NNNNNNN-NNNNNNNNNNNNNN
    imovel_id           UUID NOT NULL REFERENCES imoveis_rurais(id),
    requerente_id       UUID NOT NULL REFERENCES users(id),
    analista_id         UUID REFERENCES users(id),
    status              status_processo_enum NOT NULL DEFAULT 'rascunho',
    etapa               INTEGER NOT NULL DEFAULT 1 CHECK (etapa BETWEEN 1 AND 10),
    prioridade          prioridade_enum NOT NULL DEFAULT 'normal',
    prazo_analise       DATE,
    data_submissao_at   TIMESTAMPTZ,
    data_conclusao_at   TIMESTAMPTZ,
    observacoes_analista TEXT,
    score_completude    NUMERIC(5, 2) DEFAULT 0.0 CHECK (score_completude BETWEEN 0 AND 100),
    score_risco         NUMERIC(4, 2) DEFAULT 0.0 CHECK (score_risco BETWEEN 0 AND 10),
    metadata            JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ,

    CONSTRAINT chk_analista_em_analise CHECK (
        status NOT IN ('em_analise', 'aprovado', 'rejeitado') OR analista_id IS NOT NULL
    ),
    CONSTRAINT chk_numero_car_aprovado CHECK (
        status != 'aprovado' OR numero_car IS NOT NULL
    )
);
```

### Tabela: documentos

```sql
CREATE TABLE documentos (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    processo_id         UUID NOT NULL REFERENCES processos_car(id),
    tipo_documento      tipo_documento_enum NOT NULL,
    nome_arquivo        VARCHAR(500) NOT NULL,
    tamanho_bytes       BIGINT NOT NULL CHECK (tamanho_bytes > 0),
    mime_type           VARCHAR(100) NOT NULL,
    hash_sha256         CHAR(64) NOT NULL,     -- integridade do arquivo
    storage_path        VARCHAR(1000) NOT NULL, -- path no MinIO/S3
    status              status_documento_enum NOT NULL DEFAULT 'aguardando',
    dados_ocr           JSONB,   -- {texto, confianca, paginas, engine}
    dados_extraidos     JSONB,   -- campos estruturados extraídos
    erros_validacao     JSONB,   -- [{codigo, campo, mensagem}]
    tentativas_ocr      INTEGER NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_tamanho_maximo CHECK (tamanho_bytes <= 52428800)  -- 50MB
);
```

### Tabela: pendencias

```sql
CREATE TABLE pendencias (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    processo_id             UUID NOT NULL REFERENCES processos_car(id),
    tipo                    tipo_pendencia_enum NOT NULL,
    titulo                  VARCHAR(255) NOT NULL,
    descricao               TEXT NOT NULL,
    prazo                   DATE,
    status                  status_pendencia_enum NOT NULL DEFAULT 'aberta',
    criada_por_sistema      BOOLEAN NOT NULL DEFAULT false,
    criada_por_analista_id  UUID REFERENCES users(id),
    resolvida_em            TIMESTAMPTZ,
    resolucao_descricao     TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Tabela: historico_processos (particionada, imutável)

```sql
CREATE TABLE historico_processos (
    id              UUID NOT NULL DEFAULT gen_random_uuid(),
    processo_id     UUID NOT NULL REFERENCES processos_car(id),
    status_anterior VARCHAR(50),
    status_novo     VARCHAR(50) NOT NULL,
    etapa_anterior  INTEGER,
    etapa_nova      INTEGER,
    motivo          TEXT,
    ator_id         UUID REFERENCES users(id),
    ator_sistema    VARCHAR(100),  -- ex: 'document_worker', 'ai_assistant'
    metadata        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT historico_processos_pkey PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Partições (criar via script automatizado no deploy)
CREATE TABLE historico_processos_2024_01
    PARTITION OF historico_processos
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE historico_processos_2024_02
    PARTITION OF historico_processos
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
-- ... continuar mensalmente

COMMENT ON TABLE historico_processos IS 'Imutável — apenas INSERT permitido. Auditoria legal do processo CAR.';
```

### Tabela: conversas

```sql
CREATE TABLE conversas (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id),
    processo_id UUID REFERENCES processos_car(id),
    titulo      VARCHAR(255),
    modelo_ia   VARCHAR(100) NOT NULL,   -- ex: 'claude-sonnet-4-6'
    provider_ia VARCHAR(50) NOT NULL,    -- ex: 'anthropic', 'openai', 'ollama'
    status      status_conversa_enum NOT NULL DEFAULT 'ativa',
    total_tokens INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Tabela: mensagens

```sql
CREATE TABLE mensagens (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversa_id         UUID NOT NULL REFERENCES conversas(id),
    role                role_mensagem_enum NOT NULL,
    conteudo            TEXT NOT NULL,
    tokens_prompt       INTEGER,
    tokens_completion   INTEGER,
    latencia_ms         INTEGER,
    feedback            SMALLINT CHECK (feedback BETWEEN -1 AND 1),
    metadata            JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Tabela: audit_logs (particionada, imutável)

```sql
CREATE TABLE audit_logs (
    id          UUID NOT NULL DEFAULT gen_random_uuid(),
    tabela_nome VARCHAR(100) NOT NULL,
    registro_id UUID,
    operacao    operacao_audit_enum NOT NULL,
    dados_antes JSONB,
    dados_depois JSONB,
    user_id     UUID,
    ip_address  INET,
    user_agent  TEXT,
    trace_id    VARCHAR(64),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT audit_logs_pkey PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE audit_logs_2024_01
    PARTITION OF audit_logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### Tabela: integracoes_externas

```sql
CREATE TABLE integracoes_externas (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sistema          sistema_externo_enum NOT NULL,
    processo_id      UUID REFERENCES processos_car(id),
    tipo_consulta    VARCHAR(100) NOT NULL,
    request_payload  JSONB,
    response_payload JSONB,
    status           status_integracao_enum NOT NULL,
    codigo_http      INTEGER,
    latencia_ms      INTEGER,
    tentativas       INTEGER NOT NULL DEFAULT 1,
    erro_mensagem    TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Tabela: notificacoes

```sql
CREATE TABLE notificacoes (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id),
    processo_id UUID REFERENCES processos_car(id),
    canal       canal_notificacao_enum NOT NULL,
    titulo      VARCHAR(255) NOT NULL,
    conteudo    TEXT NOT NULL,
    status      status_notificacao_enum NOT NULL DEFAULT 'pendente',
    tentativas  INTEGER NOT NULL DEFAULT 0,
    enviada_em  TIMESTAMPTZ,
    lida_em     TIMESTAMPTZ,
    metadata    JSONB,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Tabela: knowledge_base (RAG com pgvector)

```sql
CREATE TABLE knowledge_base (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fonte       VARCHAR(255) NOT NULL,   -- ex: 'lei_12651_2012', 'manual_sicar_v3'
    titulo      VARCHAR(500),
    conteudo    TEXT NOT NULL,           -- texto do chunk
    chunk_index INTEGER NOT NULL,        -- posição no documento original
    embedding   vector(1536),            -- text-embedding-3-small (OpenAI) ou equivalente
    metadata    JSONB NOT NULL DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Tabela: outbox (Outbox Pattern para eventos de domínio)

```sql
CREATE TABLE outbox (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id     UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    event_name   VARCHAR(200) NOT NULL,    -- ex: 'processo.submetido.v1'
    routing_key  VARCHAR(200) NOT NULL,
    payload      JSONB NOT NULL,
    status       status_outbox_enum NOT NULL DEFAULT 'pendente',
    tentativas   INTEGER NOT NULL DEFAULT 0,
    publicado_em TIMESTAMPTZ,
    erro         TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 4. Índices

```sql
-- users
CREATE INDEX idx_users_cpf_hash ON users(cpf_hash) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_govbr_sub ON users(govbr_sub) WHERE govbr_sub IS NOT NULL;
CREATE INDEX idx_users_tipo ON users(tipo_usuario) WHERE deleted_at IS NULL AND ativo = true;

-- sessions
CREATE INDEX idx_sessions_user ON sessions(user_id, expires_at);
CREATE INDEX idx_sessions_expires ON sessions(expires_at) WHERE revogada_em IS NULL;

-- imoveis_rurais
CREATE INDEX idx_imoveis_user ON imoveis_rurais(user_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_imoveis_municipio ON imoveis_rurais(municipio_ibge) WHERE deleted_at IS NULL;
CREATE INDEX idx_imoveis_geometria ON imoveis_rurais USING GIST(geometria);  -- consultas espaciais

-- processos_car
CREATE INDEX idx_processos_requerente ON processos_car(requerente_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_processos_analista ON processos_car(analista_id) WHERE analista_id IS NOT NULL AND deleted_at IS NULL;
CREATE INDEX idx_processos_status ON processos_car(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_processos_status_prioridade ON processos_car(status, prioridade, created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_processos_submetidos ON processos_car(data_submissao_at DESC) WHERE status = 'submetido';
CREATE INDEX idx_processos_metadata ON processos_car USING GIN(metadata);

-- documentos
CREATE INDEX idx_documentos_processo ON documentos(processo_id);
CREATE INDEX idx_documentos_processo_tipo ON documentos(processo_id, tipo_documento);
CREATE INDEX idx_documentos_processo_status ON documentos(processo_id, status);
CREATE UNIQUE INDEX idx_documentos_hash ON documentos(hash_sha256);  -- deduplicação
CREATE INDEX idx_documentos_aguardando ON documentos(created_at) WHERE status = 'aguardando';

-- pendencias
CREATE INDEX idx_pendencias_processo ON pendencias(processo_id) WHERE status != 'resolvida';
CREATE INDEX idx_pendencias_abertas ON pendencias(prazo ASC) WHERE status = 'aberta';

-- historico_processos (por partição)
CREATE INDEX idx_historico_processo ON historico_processos(processo_id, created_at DESC);

-- conversas e mensagens
CREATE INDEX idx_conversas_user ON conversas(user_id, created_at DESC);
CREATE INDEX idx_conversas_processo ON conversas(processo_id) WHERE processo_id IS NOT NULL;
CREATE INDEX idx_mensagens_conversa ON mensagens(conversa_id, created_at ASC);

-- audit_logs (por partição)
CREATE INDEX idx_audit_tabela_registro ON audit_logs(tabela_nome, registro_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at DESC) WHERE user_id IS NOT NULL;

-- knowledge_base
CREATE INDEX idx_kb_embedding ON knowledge_base
    USING ivfflat(embedding vector_cosine_ops)
    WITH (lists = 100);  -- sqrt(nrows) como regra geral
CREATE INDEX idx_kb_fonte ON knowledge_base(fonte);

-- outbox
CREATE INDEX idx_outbox_pendente ON outbox(created_at ASC) WHERE status = 'pendente';

-- integracoes_externas
CREATE INDEX idx_integracoes_processo ON integracoes_externas(processo_id, created_at DESC);
CREATE INDEX idx_integracoes_sistema ON integracoes_externas(sistema, status, created_at DESC);

-- notificacoes
CREATE INDEX idx_notificacoes_user ON notificacoes(user_id, status, created_at DESC);
CREATE INDEX idx_notificacoes_pendentes ON notificacoes(created_at) WHERE status = 'pendente';
```

---

## 5. Triggers e Functions PL/pgSQL

```sql
-- Trigger para updated_at automático
CREATE OR REPLACE FUNCTION fn_update_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

-- Aplicar em todas as tabelas relevantes
DO $$
DECLARE t TEXT;
BEGIN
    FOREACH t IN ARRAY ARRAY[
        'users', 'imoveis_rurais', 'processos_car', 'documentos',
        'pendencias', 'conversas'
    ] LOOP
        EXECUTE format('CREATE TRIGGER trg_%s_updated_at
            BEFORE UPDATE ON %s
            FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at()', t, t);
    END LOOP;
END;
$$;

-- Trigger de audit log genérico
CREATE OR REPLACE FUNCTION fn_audit_log()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO audit_logs (tabela_nome, registro_id, operacao, dados_antes, dados_depois)
    VALUES (
        TG_TABLE_NAME,
        CASE TG_OP WHEN 'DELETE' THEN OLD.id ELSE NEW.id END,
        TG_OP::operacao_audit_enum,
        CASE TG_OP WHEN 'INSERT' THEN NULL ELSE to_jsonb(OLD) END,
        CASE TG_OP WHEN 'DELETE' THEN NULL ELSE to_jsonb(NEW) END
    );
    RETURN COALESCE(NEW, OLD);
END;
$$;

-- Aplicar auditoria em tabelas críticas
CREATE TRIGGER trg_audit_processos_car
    AFTER INSERT OR UPDATE OR DELETE ON processos_car
    FOR EACH ROW EXECUTE FUNCTION fn_audit_log();

CREATE TRIGGER trg_audit_users
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION fn_audit_log();

-- Function para calcular score de completude
CREATE OR REPLACE FUNCTION fn_calcular_score_completude(p_processo_id UUID)
RETURNS NUMERIC LANGUAGE plpgsql AS $$
DECLARE
    v_total_docs     INTEGER;
    v_docs_validos   INTEGER;
    v_tem_geometria  BOOLEAN;
    v_tem_matricula  BOOLEAN;
    v_tem_ccir       BOOLEAN;
    v_score          NUMERIC := 0;
BEGIN
    SELECT COUNT(*) INTO v_total_docs
    FROM documentos WHERE processo_id = p_processo_id;

    SELECT COUNT(*) INTO v_docs_validos
    FROM documentos WHERE processo_id = p_processo_id AND status = 'valido';

    SELECT EXISTS(
        SELECT 1 FROM documentos
        WHERE processo_id = p_processo_id
          AND tipo_documento = 'matricula_imovel' AND status = 'valido'
    ) INTO v_tem_matricula;

    SELECT EXISTS(
        SELECT 1 FROM documentos
        WHERE processo_id = p_processo_id
          AND tipo_documento = 'ccir' AND status = 'valido'
    ) INTO v_tem_ccir;

    SELECT (ir.geometria IS NOT NULL) INTO v_tem_geometria
    FROM processos_car p JOIN imoveis_rurais ir ON ir.id = p.imovel_id
    WHERE p.id = p_processo_id;

    -- Score: 30% geometria + 30% matrícula + 20% CCIR + 20% outros docs
    v_score := 0;
    IF v_tem_geometria THEN v_score := v_score + 30; END IF;
    IF v_tem_matricula THEN v_score := v_score + 30; END IF;
    IF v_tem_ccir      THEN v_score := v_score + 20; END IF;
    IF v_total_docs > 2 THEN
        v_score := v_score + LEAST(20, (v_docs_validos - 2) * 5);
    END IF;

    RETURN LEAST(100, ROUND(v_score, 2));
END;
$$;
```

---

## 6. Views

```sql
-- Dashboard do analista — processos com todos os KPIs em uma consulta
CREATE OR REPLACE VIEW vw_processos_dashboard AS
SELECT
    p.id,
    p.numero_car,
    p.status,
    p.prioridade,
    p.etapa,
    p.score_completude,
    p.score_risco,
    p.data_submissao_at,
    p.data_conclusao_at,
    NOW() - p.data_submissao_at AS tempo_em_analise,
    u_req.nome_completo         AS requerente_nome,
    u_ana.nome_completo         AS analista_nome,
    ir.municipio_ibge,
    ir.estado,
    ir.area_total_ha,
    ir.tipo_imovel,
    ir.bioma,
    COUNT(d.id)                 AS total_documentos,
    COUNT(d.id) FILTER (WHERE d.status = 'valido')      AS docs_validos,
    COUNT(d.id) FILTER (WHERE d.status = 'invalido')    AS docs_invalidos,
    COUNT(pend.id) FILTER (WHERE pend.status = 'aberta') AS pendencias_abertas
FROM processos_car p
    JOIN users u_req ON p.requerente_id = u_req.id
    LEFT JOIN users u_ana ON p.analista_id = u_ana.id
    JOIN imoveis_rurais ir ON p.imovel_id = ir.id
    LEFT JOIN documentos d ON d.processo_id = p.id
    LEFT JOIN pendencias pend ON pend.processo_id = p.id
WHERE p.deleted_at IS NULL
GROUP BY p.id, u_req.nome_completo, u_ana.nome_completo,
         ir.municipio_ibge, ir.estado, ir.area_total_ha, ir.tipo_imovel, ir.bioma;
```

---

## 7. Estratégia de Migração com Alembic

### Nomenclatura de Migrations
`YYYY_MM_DD_NNNN_descricao_curta.py`  
Exemplo: `2024_01_15_0001_initial_schema.py`

### Template de Migration

```python
"""initial_schema

Revision ID: 0001
Revises:
Create Date: 2024-01-15 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
from pgvector.sqlalchemy import Vector

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Extensões
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # ENUMs primeiro
    op.execute("""
        CREATE TYPE tipo_usuario_enum AS ENUM (
            'produtor_rural', 'consultor_ambiental', 'analista_ambiental',
            'supervisor_ambiental', 'admin'
        )
    """)

    # Tabelas
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('cpf_hash', sa.CHAR(64), nullable=False, unique=True),
        # ...
        sa.PrimaryKeyConstraint('id'),
    )

def downgrade() -> None:
    op.drop_table('users')
    op.execute("DROP TYPE IF EXISTS tipo_usuario_enum CASCADE")
```

---

## 8. Política de Retenção e LGPD

| Dado | Tabela | Retenção | Base Legal | Proteção | Anonimização |
|---|---|---|---|---|---|
| CPF | users | 5 anos pós-inatividade | Art. 7, V LGPD (contrato) | pgcrypto AES-256 | Hash SHA-256 para analytics |
| Email | users | 5 anos pós-inatividade | Art. 7, IX (interesse legítimo) | pgcrypto AES-256 | Removido de exports |
| Geometria do imóvel | imoveis_rurais | Indefinida (dado de registro público) | Art. 7, II (obrigação legal) | RBAC — sem export individual público | Agregado por município em relatórios |
| Documentos pessoais | MinIO + documentos | 10 anos pós-conclusão | Art. 7, II (obrigação legal CAR) | AES-256 no object storage | — |
| Histórico de status | historico_processos | 10 anos (prazo legal CAR) | Art. 7, II (obrigação legal) | Tabela imutável particionada | — |
| Audit logs | audit_logs | 5 anos | Art. 37 LGPD (segurança) | Write-once particionado | — |
| Conversas com IA | conversas + mensagens | 90 dias + anonimização | Consentimento | CPF mascarado no prompt | CPF→token após 90 dias |
| Logs de acesso | sessions | 6 meses | Interesse legítimo (segurança) | Particionado | IP truncado em analytics |
