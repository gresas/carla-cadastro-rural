# CARla — Design de APIs REST

> **Versão:** 1.0.0  
> **Stack:** FastAPI 0.115+, Pydantic v2, OAuth2/JWT, PostgreSQL  
> **Última atualização:** 2026-06-01  
> **Status:** Aprovado

---

## Sumário

1. [Princípios de Design da API](#1-princípios-de-design-da-api)
2. [Autenticação e Autorização](#2-autenticação-e-autorização)
3. [Schemas Pydantic v2 Principais](#3-schemas-pydantic-v2-principais)
4. [Endpoints Detalhados por Módulo](#4-endpoints-detalhados-por-módulo)
5. [Tratamento de Erros](#5-tratamento-de-erros)
6. [Rate Limiting](#6-rate-limiting)
7. [SSE — Server-Sent Events para o Assistente](#7-sse--server-sent-events-para-o-assistente)
8. [OpenAPI — Contrato e Especificação](#8-openapi--contrato-e-especificação)
9. [Versionamento da API](#9-versionamento-da-api)

---

## 1. Princípios de Design da API

### 1.1 Convenções Gerais

A API do CARla segue os princípios REST com orientação a recursos. Todas as URLs são substantivos no plural, em português sem acentuação, com separadores em hífen.

| Princípio | Decisão |
|---|---|
| Estilo arquitetural | REST resource-based |
| Prefixo de versão | `/api/v1/` |
| Codificação | UTF-8 em todas as requisições e respostas |
| Content-Type padrão | `application/json` |
| Datas e horários | ISO 8601 com timezone UTC (ex: `2024-01-15T14:30:00Z`) |
| Identificadores | UUIDs v4 (nunca IDs sequenciais expostos) |
| Tamanho máximo de payload | 10 MB (exceto upload de documentos, 50 MB) |

### 1.2 Estrutura de URLs

```
https://api.carcopilot.gov.br/api/v1/{recurso}
https://api.carcopilot.gov.br/api/v1/{recurso}/{id}
https://api.carcopilot.gov.br/api/v1/{recurso}/{id}/{sub-recurso}
https://api.carcopilot.gov.br/api/v1/{recurso}/{id}/acoes
```

Exemplos válidos:
```
GET  /api/v1/processos
GET  /api/v1/processos/550e8400-e29b-41d4-a716-446655440000
GET  /api/v1/processos/550e8400-e29b-41d4-a716-446655440000/documentos
POST /api/v1/processos/550e8400-e29b-41d4-a716-446655440000/submeter
```

### 1.3 Envelope de Resposta

Todas as respostas seguem um envelope padronizado que facilita o tratamento uniforme no cliente.

**Resposta de recurso único — sucesso:**
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "numero_car": "MG-3106200-ABCD1234567890",
    "status": "submetido"
  },
  "meta": {
    "request_id": "req_01HN5X7M3K4WQJZB9YDVP6T8E",
    "timestamp": "2024-01-15T14:30:00Z"
  }
}
```

**Resposta de lista paginada — sucesso:**
```json
{
  "data": [
    { "id": "...", "status": "em_analise" },
    { "id": "...", "status": "rascunho" }
  ],
  "meta": {
    "request_id": "req_01HN5X7M3K4WQJZB9YDVP6T8E",
    "timestamp": "2024-01-15T14:30:00Z",
    "cursor_next": "eyJpZCI6IjU1MGU4NDAwIiwiY3JlYXRlZF9hdCI6IjIwMjQtMDEtMTVUMTQ6MzA6MDBaIn0=",
    "cursor_prev": null,
    "total_count": 847,
    "has_more": true,
    "page_size": 20
  }
}
```

**Resposta de erro:**
```json
{
  "error": {
    "code": "CAR-004",
    "message": "Dados de entrada inválidos",
    "details": [
      {
        "field": "municipio_ibge",
        "code": "invalid_format",
        "message": "Deve ter exatamente 7 dígitos numéricos"
      }
    ]
  }
}
```

### 1.4 Paginação Cursor-Based

A paginação usa cursores opacos (base64) em vez de OFFSET/LIMIT para evitar inconsistências em conjuntos de dados mutáveis.

**Como funciona:**
- O cursor codifica o último item retornado (id + created_at) em base64
- O cliente passa `?cursor=<valor>` na próxima requisição
- O servidor decodifica e executa `WHERE (created_at, id) < (cursor_ts, cursor_id) ORDER BY created_at DESC, id DESC`
- Cursores expiram após 1 hora de inatividade

**Query params de paginação:**
| Parâmetro | Tipo | Padrão | Máximo | Descrição |
|---|---|---|---|---|
| `cursor` | string | null | — | Cursor para a próxima página |
| `page_size` | integer | 20 | 100 | Itens por página |

### 1.5 Headers Obrigatórios e Opcionais

**Headers de requisição:**
| Header | Obrigatório | Descrição |
|---|---|---|
| `Authorization: Bearer <token>` | Sim (rotas protegidas) | JWT de acesso |
| `Content-Type: application/json` | Sim (POST/PATCH) | Tipo do corpo |
| `Accept: application/json` | Recomendado | Tipo aceito na resposta |
| `X-Request-ID` | Opcional | ID para rastreabilidade (gerado pelo servidor se ausente) |
| `Idempotency-Key` | Obrigatório em operações críticas | UUID para idempotência |

**Headers de resposta:**
| Header | Descrição |
|---|---|
| `X-Request-ID` | ID único da requisição para debugging |
| `X-RateLimit-Limit` | Limite de requisições no período |
| `X-RateLimit-Remaining` | Requisições restantes no período atual |
| `X-RateLimit-Reset` | Unix timestamp de reset do contador |
| `Deprecation` | Data de deprecação do endpoint (quando aplicável) |
| `Sunset` | Data de remoção do endpoint (quando aplicável) |

### 1.6 Idempotência

Operações críticas aceitam o header `Idempotency-Key` (UUID v4). O servidor armazena o resultado da primeira execução por 24 horas e retorna o mesmo resultado para requisições com a mesma chave, evitando duplo processamento em caso de retry.

```
POST /api/v1/processos/550e8400.../submeter
Idempotency-Key: 7f4e1c2b-3a8d-4f9e-b6c5-1234567890ab
```

Se a operação já foi processada com essa chave, o servidor retorna HTTP 200 com o resultado original e o header `X-Idempotency-Replayed: true`.

### 1.7 CORS

Configurado por ambiente via variável de ambiente `ALLOWED_ORIGINS`:

| Ambiente | Origins Permitidas |
|---|---|
| Produção | `https://carcopilot.gov.br`, `https://www.carcopilot.gov.br` |
| Staging | `https://staging.carcopilot.gov.br` |
| Desenvolvimento | `http://localhost:3000`, `http://localhost:5173` |

---

## 2. Autenticação e Autorização

### 2.1 Fluxo OAuth2 Gov.br — Authorization Code + PKCE

O CARla utiliza o Gov.br como provedor de identidade único. O fluxo Authorization Code com PKCE (Proof Key for Code Exchange) elimina a necessidade de client_secret no frontend.

```
┌─────────┐          ┌──────────────┐          ┌─────────┐
│ Browser │          │ CARla  │          │ Gov.br  │
└────┬────┘          └──────┬───────┘          └────┬────┘
     │                      │                       │
     │ 1. GET /auth/govbr/  │                       │
     │    authorize?        │                       │
     │    redirect_uri=...  │                       │
     │    state=<random>    │                       │
     │    code_challenge=.. │                       │
     │─────────────────────>│                       │
     │                      │                       │
     │ 2. 302 → Gov.br URL  │                       │
     │<─────────────────────│                       │
     │                      │                       │
     │ 3. Usuário autentica no Gov.br               │
     │─────────────────────────────────────────────>│
     │                      │                       │
     │ 4. Gov.br redireciona com ?code=...&state=.. │
     │<─────────────────────────────────────────────│
     │                      │                       │
     │ 5. GET /auth/govbr/  │                       │
     │    callback?code=... │                       │
     │    &state=...        │                       │
     │─────────────────────>│                       │
     │                      │ 6. POST token_endpoint│
     │                      │    code + verifier    │
     │                      │──────────────────────>│
     │                      │                       │
     │                      │ 7. access_token +     │
     │                      │    userinfo           │
     │                      │<──────────────────────│
     │                      │                       │
     │ 8. JWT CARla   │                       │
     │<─────────────────────│                       │
└────┴────┘          └──────┴───────┘          └────┴────┘
```

**Passo 1 — Iniciar fluxo:**
```
GET /api/v1/auth/govbr/authorize
  ?redirect_uri=https://carcopilot.gov.br/auth/callback
  &state=xK9mP2nQ7rL4sT1u
  &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
  &code_challenge_method=S256
```

O `state` deve ser gerado aleatoriamente pelo cliente e armazenado em sessão para validação anti-CSRF. O `code_challenge` é derivado do `code_verifier` via SHA-256 + base64url.

**Passo 5 — Callback:**
```
GET /api/v1/auth/govbr/callback
  ?code=SplxlOBeZQQYbYS6WxSbIA
  &state=xK9mP2nQ7rL4sT1u
```

**Passo 8 — Resposta com tokens CARla:**
```json
{
  "data": {
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
    "expires_in": 3600,
    "token_type": "Bearer"
  },
  "meta": {
    "request_id": "req_01HN5X7M3K4WQJZB9YDVP6T8E",
    "timestamp": "2024-01-15T14:30:00Z"
  }
}
```

### 2.2 JWT — Estrutura do Payload

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email_hash": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
  "nome": "João Silva",
  "cpf_hash": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
  "tipo_usuario": "produtor_rural",
  "nivel_confiabilidade": "prata",
  "roles": ["processos:read", "processos:write", "documentos:write"],
  "jti": "01HN5X7M3K4WQJZB9YDVP6T8E",
  "iss": "https://api.carcopilot.gov.br",
  "aud": "carcopilot-web",
  "iat": 1705312200,
  "exp": 1705315800
}
```

| Campo | Descrição |
|---|---|
| `sub` | UUID interno do usuário no CARla |
| `email_hash` | SHA-256 do email (nunca o email em texto puro) |
| `cpf_hash` | SHA-256 do CPF (LGPD compliance) |
| `tipo_usuario` | `produtor_rural`, `consultor_ambiental`, `analista`, `supervisor`, `admin` |
| `nivel_confiabilidade` | Nível de confiabilidade Gov.br: `bronze`, `prata`, `ouro` |
| `roles` | Lista de permissões finas (resource:action) |
| `jti` | JWT ID único — permite revogação individual |
| `iss` | Issuer — URL da API |
| `aud` | Audience — identifica o cliente |
| `iat` | Issued At (Unix timestamp) |
| `exp` | Expiration (Unix timestamp) — 1 hora após emissão |

**Algoritmo de assinatura:** RS256 (RSA 2048-bit). A chave pública é disponibilizada em `GET /api/v1/auth/.well-known/jwks.json`.

**Refresh token:** opaco (não JWT), armazenado no banco com validade de 30 dias. Rotacionado a cada uso (refresh token rotation).

### 2.3 Endpoints de Autenticação

**GET /api/v1/auth/govbr/authorize**

Inicia o fluxo OAuth2. Retorna a URL de autorização do Gov.br.

| Parâmetro | Obrigatório | Descrição |
|---|---|---|
| `redirect_uri` | Sim | URI de callback registrada no Gov.br |
| `state` | Sim | String aleatória para proteção CSRF |
| `code_challenge` | Sim | Hash do code_verifier (base64url SHA-256) |
| `code_challenge_method` | Sim | Deve ser `S256` |

Resposta 200:
```json
{
  "data": {
    "authorization_url": "https://sso.acesso.gov.br/authorize?client_id=carcopilot&response_type=code&scope=openid+email+profile&redirect_uri=...&state=...&code_challenge=...&code_challenge_method=S256",
    "state": "xK9mP2nQ7rL4sT1u",
    "expires_in": 300
  }
}
```

**GET /api/v1/auth/govbr/callback**

Processa o retorno do Gov.br. Troca o authorization code por tokens.

| Parâmetro | Descrição |
|---|---|
| `code` | Authorization code retornado pelo Gov.br |
| `state` | Deve coincidir com o state enviado no passo 1 |

Resposta 200: tokens de acesso (ver seção 2.1).

Erros possíveis:
- `CAR-010` (400) — state inválido ou expirado
- `CAR-011` (400) — authorization code expirado
- `CAR-012` (503) — Gov.br indisponível

**GET /api/v1/auth/me**

Retorna os dados do usuário autenticado.

Auth: Bearer JWT obrigatório.

Resposta 200:
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "nome": "João Silva",
    "tipo_usuario": "produtor_rural",
    "nivel_confiabilidade": "prata",
    "status": "ativo",
    "ultimo_acesso_at": "2024-01-15T14:00:00Z",
    "created_at": "2023-06-01T09:00:00Z"
  }
}
```

**POST /api/v1/auth/refresh**

Renova o access token usando o refresh token.

Body:
```json
{ "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..." }
```

Resposta 200: novos tokens (ver seção 2.1). O refresh token anterior é invalidado imediatamente (rotation).

Erros: `CAR-001` (401) se o refresh token for inválido, expirado ou já utilizado.

**POST /api/v1/auth/logout**

Invalida o access token e o refresh token associado.

Auth: Bearer JWT obrigatório.

Resposta 204: sem corpo. O JTI do token é adicionado à blocklist no Redis com TTL igual ao tempo restante de expiração.

**GET /api/v1/auth/.well-known/jwks.json**

Endpoint público que expõe as chaves públicas RSA para validação de tokens por terceiros.

Auth: pública.

### 2.4 RBAC — Matriz de Permissões

| Endpoint | Produtor Rural | Consultor Ambiental | Analista | Supervisor | Admin |
|---|:---:|:---:|:---:|:---:|:---:|
| `GET /imoveis` (próprios) | ✓ | ✓ | — | — | ✓ |
| `GET /imoveis/{id}` | ✓ (próprio) | ✓ (associado) | ✓ | ✓ | ✓ |
| `POST /imoveis` | ✓ | ✓ | — | — | ✓ |
| `PATCH /imoveis/{id}` | ✓ (próprio) | ✓ (associado) | — | — | ✓ |
| `GET /processos` (próprios) | ✓ | ✓ | ✓ (todos) | ✓ (todos) | ✓ |
| `POST /processos` | ✓ | ✓ | — | — | ✓ |
| `POST /processos/{id}/submeter` | ✓ (próprio) | ✓ (associado) | — | — | ✓ |
| `POST /processos/{id}/cancelar` | ✓ (próprio) | — | — | ✓ | ✓ |
| `POST /documentos/upload` | ✓ | ✓ | — | — | ✓ |
| `DELETE /documentos/{id}` | ✓ (próprio) | ✓ (associado) | — | — | ✓ |
| `POST /assistente/conversas` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `GET /analista/processos` | — | — | ✓ | ✓ | ✓ |
| `POST /analista/processos/{id}/assumir` | — | — | ✓ | ✓ | ✓ |
| `POST /analista/processos/{id}/aprovar` | — | — | ✓ | ✓ | ✓ |
| `POST /analista/processos/{id}/rejeitar` | — | — | ✓ | ✓ | ✓ |
| `GET /analista/dashboard` | — | — | ✓ | ✓ | ✓ |
| `GET /admin/usuarios` | — | — | — | — | ✓ |
| `GET /admin/audit-logs` | — | — | — | ✓ | ✓ |
| `POST /admin/configuracoes/llm` | — | — | — | — | ✓ |
| `GET /admin/metricas/sistema` | — | — | — | ✓ | ✓ |

> Regra geral: produtores e consultores só acessam recursos associados ao seu CPF/CNPJ. Analistas veem todos os processos mas não podem criar novos. Supervisores podem cancelar qualquer processo e acessar logs de auditoria.

---

## 3. Schemas Pydantic v2 Principais

### 3.1 Estruturas Base de Resposta

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic import AnyHttpUrl, EmailStr
from typing import Optional, List, Generic, TypeVar, Annotated
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
import re
import hashlib

T = TypeVar("T")


class Meta(BaseModel):
    """Metadados presentes em todas as respostas."""
    request_id: str = Field(
        description="ID único da requisição para rastreabilidade",
        example="req_01HN5X7M3K4WQJZB9YDVP6T8E"
    )
    timestamp: datetime = Field(
        description="Timestamp UTC da resposta em ISO 8601"
    )


class PaginationMeta(Meta):
    """Metadados de paginação cursor-based."""
    cursor_next: Optional[str] = Field(
        default=None,
        description="Cursor opaco para a próxima página. Null se não houver."
    )
    cursor_prev: Optional[str] = Field(
        default=None,
        description="Cursor opaco para a página anterior. Null se for a primeira."
    )
    total_count: int = Field(
        description="Total de registros que satisfazem os filtros aplicados",
        ge=0
    )
    has_more: bool = Field(
        description="Indica se existem mais registros após o cursor atual"
    )
    page_size: int = Field(
        description="Quantidade de itens retornados nesta página",
        ge=1,
        le=100
    )


class APIResponse(BaseModel, Generic[T]):
    """Envelope padrão para resposta de recurso único."""
    data: T
    meta: Meta


class PaginatedResponse(BaseModel, Generic[T]):
    """Envelope padrão para resposta de lista paginada."""
    data: List[T]
    meta: PaginationMeta


class ErrorDetail(BaseModel):
    """Detalhe de um item de erro, geralmente associado a um campo específico."""
    field: Optional[str] = Field(
        default=None,
        description="Caminho do campo com erro (dot notation). Null para erros gerais.",
        example="imovel.municipio_ibge"
    )
    code: str = Field(
        description="Código de erro semântico para tratamento programático",
        example="invalid_format"
    )
    message: str = Field(
        description="Mensagem legível por humanos em português",
        example="Deve ter exatamente 7 dígitos numéricos"
    )


class ErrorBody(BaseModel):
    """Corpo do erro."""
    code: str = Field(example="CAR-004")
    message: str = Field(example="Dados de entrada inválidos")
    details: List[ErrorDetail] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    """Envelope de resposta de erro."""
    error: ErrorBody
```

### 3.2 Enumerações de Domínio

```python
class StatusProcesso(str, Enum):
    RASCUNHO = "rascunho"
    SUBMETIDO = "submetido"
    EM_ANALISE = "em_analise"
    PENDENTE_DOCUMENTACAO = "pendente_documentacao"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"
    CANCELADO = "cancelado"
    SUSPENSO = "suspenso"


class PrioridadeProcesso(str, Enum):
    BAIXA = "baixa"
    NORMAL = "normal"
    ALTA = "alta"
    URGENTE = "urgente"


class TipoDocumento(str, Enum):
    DOCUMENTO_PROPRIEDADE = "documento_propriedade"
    CCIR = "ccir"
    ITR = "itr"
    PLANTA_GEOREFERENCIADA = "planta_georeferenciada"
    ART_RRT = "art_rrt"
    DOCUMENTO_IDENTIDADE = "documento_identidade"
    COMPROVANTE_RESIDENCIA = "comprovante_residencia"
    LICENCA_AMBIENTAL = "licenca_ambiental"
    OUTORGA_AGUA = "outorga_agua"
    OUTROS = "outros"


class StatusDocumento(str, Enum):
    AGUARDANDO = "aguardando"
    PROCESSANDO = "processando"
    VALIDADO = "validado"
    REJEITADO = "rejeitado"
    ERRO_PROCESSAMENTO = "erro_processamento"


class TipoUsuario(str, Enum):
    PRODUTOR_RURAL = "produtor_rural"
    CONSULTOR_AMBIENTAL = "consultor_ambiental"
    ANALISTA = "analista"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"


class NivelConfiabilidade(str, Enum):
    BRONZE = "bronze"
    PRATA = "prata"
    OURO = "ouro"


class TipoPendencia(str, Enum):
    DOCUMENTACAO_FALTANTE = "documentacao_faltante"
    DADO_INCORRETO = "dado_incorreto"
    GEOMETRIA_INVALIDA = "geometria_invalida"
    INFORMACAO_COMPLEMENTAR = "informacao_complementar"


class StatusPendencia(str, Enum):
    ABERTA = "aberta"
    RESPONDIDA = "respondida"
    ENCERRADA = "encerrada"
    VENCIDA = "vencida"
```

### 3.3 Schemas de Imóvel

```python
class CoordenadasGPS(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class GeoJSONPolygon(BaseModel):
    """Representação simplificada de polígono GeoJSON."""
    type: str = Field(default="Polygon", pattern="^Polygon$")
    coordinates: List[List[List[float]]] = Field(
        description="Array de anéis: [[longitude, latitude], ...]. Primeiro anel é o exterior."
    )

    @field_validator("coordinates")
    @classmethod
    def validate_polygon_closed(cls, v: List[List[List[float]]]) -> List[List[List[float]]]:
        """Valida que cada anel está fechado (primeiro ponto = último ponto)."""
        for ring in v:
            if len(ring) < 4:
                raise ValueError("Anel deve ter no mínimo 4 pontos (incluindo fechamento)")
            if ring[0] != ring[-1]:
                raise ValueError("Anel não está fechado: primeiro e último ponto devem ser iguais")
        return v


class ImóvelCreate(BaseModel):
    nome_imovel: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Nome da propriedade rural",
        example="Fazenda São João"
    )
    municipio_ibge: str = Field(
        ...,
        pattern=r"^\d{7}$",
        description="Código IBGE do município com 7 dígitos",
        example="3106200"
    )
    area_total_ha: float = Field(
        ...,
        gt=0,
        description="Área total em hectares",
        example=125.75
    )
    numero_incra: Optional[str] = Field(
        default=None,
        pattern=r"^\d{13}$",
        description="Número de matrícula INCRA com 13 dígitos"
    )
    geometria_geojson: Optional[GeoJSONPolygon] = Field(
        default=None,
        description="Polígono da propriedade em GeoJSON WGS84"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "nome_imovel": "Fazenda São João",
                "municipio_ibge": "3106200",
                "area_total_ha": 125.75,
                "geometria_geojson": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-44.123456, -19.123456],
                        [-44.123456, -19.234567],
                        [-44.234567, -19.234567],
                        [-44.234567, -19.123456],
                        [-44.123456, -19.123456]
                    ]]
                }
            }
        }
    }


class ImóvelUpdate(BaseModel):
    nome_imovel: Optional[str] = Field(default=None, min_length=3, max_length=255)
    area_total_ha: Optional[float] = Field(default=None, gt=0)
    geometria_geojson: Optional[GeoJSONPolygon] = None


class ImóvelResponse(BaseModel):
    id: UUID
    nome_imovel: str
    municipio_ibge: str
    municipio_nome: str
    estado_sigla: str
    area_total_ha: float
    numero_incra: Optional[str]
    tem_geometria: bool
    area_geometria_ha: Optional[float]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

### 3.4 Schemas de Processo CAR

```python
class ProcessoCARCreate(BaseModel):
    imovel_id: UUID = Field(
        ...,
        description="UUID do imóvel para o qual o processo CAR será aberto"
    )

    model_config = {
        "json_schema_extra": {
            "example": {"imovel_id": "550e8400-e29b-41d4-a716-446655440000"}
        }
    }


class ProcessoCARUpdate(BaseModel):
    """Campos atualizáveis enquanto o processo está em rascunho."""
    prioridade: Optional[PrioridadeProcesso] = None
    observacoes_internas: Optional[str] = Field(default=None, max_length=5000)


class PendenciaResponse(BaseModel):
    id: UUID
    tipo: TipoPendencia
    titulo: str
    descricao: str
    prazo: Optional[datetime]
    status: StatusPendencia
    resposta: Optional[str]
    respondido_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class EventoHistoricoResponse(BaseModel):
    id: UUID
    tipo_evento: str
    descricao: str
    usuario_nome: str
    dados_adicionais: Optional[dict]
    created_at: datetime

    model_config = {"from_attributes": True}


class ProcessoCARResponse(BaseModel):
    id: UUID
    numero_car: Optional[str] = Field(
        description="Número oficial CAR. Gerado apenas após submissão aprovada."
    )
    status: StatusProcesso
    etapa: int = Field(ge=1, le=5, description="Etapa atual do fluxo (1-5)")
    prioridade: PrioridadeProcesso
    data_submissao_at: Optional[datetime]
    data_aprovacao_at: Optional[datetime]
    score_completude: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
        description="Percentual de completude da documentação (0-100)"
    )
    score_risco: Optional[float] = Field(
        default=None,
        ge=0,
        le=10,
        description="Score de risco calculado pela IA (0-10)"
    )
    imovel: ImóvelResponse
    total_documentos: int = Field(ge=0)
    documentos_validados: int = Field(ge=0)
    pendencias_abertas: int = Field(ge=0)
    analista_responsavel: Optional[str] = Field(
        default=None,
        description="Nome do analista responsável pela análise atual"
    )
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

### 3.5 Schemas de Documento

```python
class DocumentoUploadResponse(BaseModel):
    id: UUID
    processo_id: UUID
    tipo_documento: TipoDocumento
    nome_arquivo: str
    tamanho_bytes: int = Field(ge=1)
    hash_sha256: str = Field(
        pattern=r"^[a-f0-9]{64}$",
        description="Hash SHA-256 do conteúdo do arquivo em hexadecimal"
    )
    status: StatusDocumento
    mime_type: str
    created_at: datetime

    model_config = {"from_attributes": True}


class DadosExtratosDocumento(BaseModel):
    """Dados estruturados extraídos via OCR e IA."""
    tipo_documento: TipoDocumento
    confianca_extracao: float = Field(ge=0, le=1)
    campos_extraidos: dict = Field(
        description="Dicionário chave-valor com campos identificados no documento"
    )
    alertas: List[str] = Field(
        default_factory=list,
        description="Alertas sobre inconsistências ou dados ausentes"
    )
    processado_at: datetime
```

### 3.6 Schemas do Assistente

```python
class ConversaCreate(BaseModel):
    processo_id: Optional[UUID] = Field(
        default=None,
        description="Vincular a conversa a um processo específico (opcional)"
    )
    titulo: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Título da conversa (gerado automaticamente se não informado)"
    )


class ConversaResponse(BaseModel):
    id: UUID
    titulo: str
    processo_id: Optional[UUID]
    total_mensagens: int
    tokens_utilizados: int
    status: str = Field(description="ativa | encerrada")
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MensagemCreate(BaseModel):
    conteudo: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Texto da mensagem do usuário",
        example="Como faço para registrar a Reserva Legal no CAR?"
    )
    processo_id: Optional[UUID] = Field(
        default=None,
        description="Contexto de processo para respostas mais precisas"
    )


class MensagemResponse(BaseModel):
    id: UUID
    conversa_id: UUID
    role: str = Field(description="user | assistant")
    conteudo: str
    tokens_prompt: Optional[int]
    tokens_completion: Optional[int]
    latencia_ms: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}
```

### 3.7 Schemas Analista e Admin

```python
class ProcessoFilaAnalista(BaseModel):
    """Visão estendida do processo para a fila do analista."""
    id: UUID
    numero_car: Optional[str]
    status: StatusProcesso
    prioridade: PrioridadeProcesso
    score_completude: Optional[float]
    score_risco: Optional[float]
    tempo_na_fila_horas: float
    total_documentos: int
    documentos_validados: int
    pendencias_abertas: int
    imovel_nome: str
    municipio_nome: str
    estado_sigla: str
    area_total_ha: float
    produtor_nome: str
    analista_responsavel: Optional[str]
    data_submissao_at: Optional[datetime]
    prazo_analise_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class AprovarProcessoBody(BaseModel):
    observacoes: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Observações do analista sobre a aprovação"
    )


class RejeitarProcessoBody(BaseModel):
    motivo: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Descrição detalhada do motivo de rejeição"
    )
    codigo_motivo: str = Field(
        ...,
        description="Código padronizado do motivo",
        examples=["DOC_INSUFICIENTE", "GEOMETRIA_INVALIDA", "DADOS_INCORRETOS"]
    )


class CriarPendenciaBody(BaseModel):
    tipo: TipoPendencia
    titulo: str = Field(..., min_length=5, max_length=255)
    descricao: str = Field(..., min_length=10, max_length=5000)
    prazo: Optional[datetime] = Field(
        default=None,
        description="Prazo para o cidadão responder. Null = sem prazo definido."
    )


class ResponderPendenciaBody(BaseModel):
    resposta: str = Field(..., min_length=1, max_length=5000)
    documentos_ids: Optional[List[UUID]] = Field(
        default=None,
        description="IDs de documentos anexados como resposta"
    )


class DashboardAnalista(BaseModel):
    processos_por_status: dict = Field(
        description="Mapa status -> quantidade"
    )
    tempo_medio_analise_horas: float
    processos_na_fila: int
    processos_atribuidos_a_mim: int
    aprovados_esta_semana: int
    rejeitados_esta_semana: int
    pendencias_abertas_total: int
    analistas_ativos: int
    produtividade_por_analista: List[dict]
```

---

## 4. Endpoints Detalhados por Módulo

### 4.1 Auth — `/api/v1/auth`

---

**GET /api/v1/auth/govbr/authorize**

Inicia o fluxo OAuth2 Authorization Code + PKCE com o Gov.br.

- **Auth:** Pública
- **Query params:**

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|:---:|---|
| `redirect_uri` | string (URI) | Sim | URI registrada no Gov.br para receber o callback |
| `state` | string | Sim | String aleatória para proteção CSRF (mín. 16 chars) |
| `code_challenge` | string | Sim | SHA-256 do code_verifier em base64url |
| `code_challenge_method` | string | Sim | Deve ser `S256` |

- **Response 200:**
```json
{
  "data": {
    "authorization_url": "https://sso.acesso.gov.br/authorize?...",
    "state": "xK9mP2nQ7rL4sT1u",
    "expires_in": 300
  }
}
```

- **Erros:** nenhum esperado (validação básica de redirect_uri)

---

**GET /api/v1/auth/govbr/callback**

Processa o retorno do Gov.br e emite tokens CARla.

- **Auth:** Pública
- **Query params:** `code` (string), `state` (string)
- **Response 200:** `APIResponse[TokenResponse]` com `access_token`, `refresh_token`, `expires_in`, `token_type`
- **Erros:**

| Código | Status | Quando |
|---|---|---|
| CAR-010 | 400 | `state` não coincide com o gerado ou já utilizado |
| CAR-011 | 400 | Authorization code expirado (Gov.br permite apenas 1 uso em até 60s) |
| CAR-012 | 503 | Gov.br indisponível ou timeout |

---

**GET /api/v1/auth/me**

Retorna perfil do usuário autenticado.

- **Auth:** Bearer JWT
- **Response 200:** `APIResponse[UsuarioResponse]`

---

**GET /api/v1/auth/.well-known/jwks.json**

Chaves públicas RSA para validação de JWTs.

- **Auth:** Pública
- **Cache:** `Cache-Control: public, max-age=3600`
- **Response 200:** JWK Set

---

**POST /api/v1/auth/refresh**

- **Auth:** Pública (usa refresh token no body)
- **Body:** `{"refresh_token": "..."}`
- **Response 200:** novos tokens + invalidação do refresh token anterior
- **Erros:** CAR-001 (401) se token inválido ou expirado

---

**POST /api/v1/auth/logout**

- **Auth:** Bearer JWT
- **Response 204:** sem corpo
- **Comportamento:** adiciona JTI à blocklist Redis; invalida refresh token associado

---

### 4.2 Imóveis — `/api/v1/imoveis`

---

**POST /api/v1/imoveis**

Cadastra um novo imóvel rural.

- **Auth:** Bearer JWT (produtor, consultor, admin)
- **Request body:** `ImóvelCreate`
- **Response 201:** `APIResponse[ImóvelResponse]`
- **Erros:**

| Código | Status | Quando |
|---|---|---|
| CAR-004 | 422 | Falha de validação (nome muito curto, área negativa, etc.) |
| CAR-020 | 422 | Geometria inválida (polígono não fecha, auto-intersecção) |
| CAR-021 | 422 | Código IBGE de município não encontrado na base de dados |

---

**GET /api/v1/imoveis**

Lista imóveis do usuário autenticado (produtor/consultor) ou todos (admin).

- **Auth:** Bearer JWT
- **Query params:** `cursor`, `page_size` (padrão 20, máx 100), `municipio_ibge`, `estado`
- **Response 200:** `PaginatedResponse[ImóvelResponse]`

---

**GET /api/v1/imoveis/{id}**

Busca imóvel por UUID.

- **Auth:** Bearer JWT (próprio ou admin)
- **Path params:** `id` (UUID)
- **Response 200:** `APIResponse[ImóvelResponse]`
- **Erros:** CAR-003 (404) se não encontrado ou sem acesso

---

**PATCH /api/v1/imoveis/{id}**

Atualiza dados do imóvel. Bloqueado se houver processo em status diferente de `rascunho` ou `cancelado`.

- **Auth:** Bearer JWT (próprio ou admin)
- **Request body:** `ImóvelUpdate` (todos os campos opcionais)
- **Response 200:** `APIResponse[ImóvelResponse]`
- **Erros:** CAR-008 (409) se imóvel tem processo em andamento; CAR-020, CAR-021 em atualizações de geometria e município

---

**GET /api/v1/imoveis/{id}/geometria**

Retorna a geometria em GeoJSON completo.

- **Auth:** Bearer JWT
- **Response 200:** `{"data": {"type": "Feature", "geometry": {...}, "properties": {...}}}`
- **Erros:** CAR-003 (404) se imóvel sem geometria cadastrada

---

**POST /api/v1/imoveis/{id}/validar-geometria**

Valida uma geometria sem persistir. Útil para feedback em tempo real no formulário.

- **Auth:** Bearer JWT
- **Request body:** `{"geometria_geojson": GeoJSONPolygon}`
- **Response 200:**
```json
{
  "data": {
    "valida": true,
    "area_calculada_ha": 125.75,
    "alertas": [],
    "sobreposicoes": []
  }
}
```
- **Response 200 (com problemas):**
```json
{
  "data": {
    "valida": false,
    "area_calculada_ha": null,
    "alertas": ["Polígono possui auto-intersecção no vértice 7"],
    "sobreposicoes": []
  }
}
```

---

### 4.3 Processos — `/api/v1/processos`

---

**GET /api/v1/processos**

Lista processos CAR com paginação e filtros.

- **Auth:** Bearer JWT
  - Produtor/consultor: vê apenas os seus
  - Analista/supervisor/admin: vê todos com filtros completos
- **Query params:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `status` | string (multi-value) | Filtrar por status. Ex: `?status=submetido&status=em_analise` |
| `municipio_ibge` | string | Filtrar por código IBGE do município |
| `estado` | string | Filtrar por UF. Ex: `MG`, `SP` |
| `data_inicio` | date (ISO 8601) | Filtrar por data de criação (início) |
| `data_fim` | date (ISO 8601) | Filtrar por data de criação (fim) |
| `prioridade` | string | `baixa`, `normal`, `alta`, `urgente` |
| `page_size` | integer | Padrão 20, máximo 100 |
| `cursor` | string | Cursor opaco para paginação |

- **Response 200:** `PaginatedResponse[ProcessoCARResponse]`

---

**POST /api/v1/processos**

Cria um novo processo CAR em rascunho.

- **Auth:** Bearer JWT (produtor, consultor, admin)
- **Request body:** `ProcessoCARCreate`
- **Response 201:** `APIResponse[ProcessoCARResponse]`
- **Erros:** CAR-003 (404) se `imovel_id` não encontrado; CAR-002 (403) se imóvel de terceiro

---

**GET /api/v1/processos/{id}**

Busca processo por UUID com todos os detalhes.

- **Auth:** Bearer JWT
- **Response 200:** `APIResponse[ProcessoCARResponse]`
- **Erros:** CAR-003 (404)

---

**PATCH /api/v1/processos/{id}**

Atualiza processo em rascunho.

- **Auth:** Bearer JWT (próprio ou admin)
- **Request body:** `ProcessoCARUpdate`
- **Response 200:** `APIResponse[ProcessoCARResponse]`
- **Erros:** CAR-008 (409) se processo não está em rascunho

---

**POST /api/v1/processos/{id}/submeter**

Submete o processo para análise. Operação crítica com idempotência.

- **Auth:** Bearer JWT (produtor, consultor)
- **Headers obrigatórios:** `Idempotency-Key: <UUID v4>`
- **Request body:** vazio `{}`
- **Validações antes de submeter:**
  - Imóvel possui geometria cadastrada
  - Score de completude de documentação >= 70%
  - Todos os campos obrigatórios preenchidos
  - Não possui pendências abertas de submissões anteriores
- **Response 200:**
```json
{
  "data": {
    "id": "550e8400-...",
    "numero_car": "MG-3106200-ABCD1234567890",
    "status": "submetido",
    "data_submissao_at": "2024-01-15T14:30:00Z"
  }
}
```
- **Erros:** CAR-008 (409) se já submetido; CAR-060 (409) se documentação incompleta

---

**POST /api/v1/processos/{id}/cancelar**

Cancela o processo. Apenas processos em `rascunho`, `submetido` ou `pendente_documentacao`.

- **Auth:** Bearer JWT (próprio) ou supervisor/admin
- **Request body:** `{"motivo": "Descrição do motivo"}`
- **Response 200:** `APIResponse[ProcessoCARResponse]` com `status: "cancelado"`
- **Erros:** CAR-008 (409) se status não permite cancelamento

---

**GET /api/v1/processos/{id}/historico**

Linha do tempo de eventos do processo.

- **Auth:** Bearer JWT
- **Query params:** `cursor`, `page_size`
- **Response 200:** `PaginatedResponse[EventoHistoricoResponse]` (ordem cronológica decrescente)

---

**GET /api/v1/processos/{id}/pendencias**

Lista pendências do processo.

- **Auth:** Bearer JWT
- **Query params:** `status` (aberta | respondida | encerrada | todas), `cursor`, `page_size`
- **Response 200:** `PaginatedResponse[PendenciaResponse]`

---

**POST /api/v1/processos/{id}/pendencias/{pendencia_id}/responder**

Cidadão responde uma pendência aberta.

- **Auth:** Bearer JWT (dono do processo)
- **Request body:** `ResponderPendenciaBody`
- **Response 200:** `APIResponse[PendenciaResponse]` com `status: "respondida"`
- **Erros:** CAR-003 (404) se pendência não encontrada; CAR-008 (409) se pendência já respondida ou encerrada

---

### 4.4 Documentos — `/api/v1/documentos`

---

**POST /api/v1/documentos/upload**

Faz upload de um documento vinculado a um processo. Processamento é assíncrono.

- **Auth:** Bearer JWT
- **Content-Type:** `multipart/form-data`
- **Form fields:**

| Campo | Tipo | Obrigatório | Descrição |
|---|---|:---:|---|
| `processo_id` | UUID | Sim | Processo ao qual o documento será associado |
| `tipo_documento` | TipoDocumento | Sim | Tipo do documento (ver enum TipoDocumento) |
| `arquivo` | file | Sim | Arquivo binário. Máx 50 MB. |

- **Tipos MIME aceitos:** `application/pdf`, `image/jpeg`, `image/png`, `image/tiff`
- **Response 202 (Accepted):** `APIResponse[DocumentoUploadResponse]` com `status: "aguardando"`
  - O documento é enfileirado para OCR e validação assíncrona
- **Erros:**

| Código | Status | Quando |
|---|---|---|
| CAR-005 | 413 | Arquivo acima de 50 MB |
| CAR-006 | 415 | MIME type não suportado |
| CAR-007 | 409 | Hash SHA-256 já existe para esse processo (documento duplicado) |
| CAR-008 | 409 | Processo não está em estado que aceita documentos |

---

**GET /api/v1/documentos/{id}**

Retorna metadados do documento.

- **Auth:** Bearer JWT
- **Response 200:** `APIResponse[DocumentoUploadResponse]`

---

**GET /api/v1/documentos/{id}/status**

Retorna o status de validação assíncrona.

- **Auth:** Bearer JWT
- **Response 200:**
```json
{
  "data": {
    "id": "uuid",
    "status": "processando",
    "progresso_percentual": 45,
    "etapa_atual": "ocr_extracao",
    "erros": []
  }
}
```

---

**GET /api/v1/documentos/{id}/dados-extraidos**

Retorna os dados estruturados extraídos via OCR e IA. Disponível apenas quando `status = "validado"`.

- **Auth:** Bearer JWT
- **Response 200:** `APIResponse[DadosExtratosDocumento]`
- **Erros:** CAR-008 (409) se documento não foi validado ainda

---

**DELETE /api/v1/documentos/{id}**

Remove um documento. Permitido apenas quando `status = "aguardando"` ou `"erro_processamento"`.

- **Auth:** Bearer JWT (próprio ou admin)
- **Response 204:** sem corpo
- **Erros:** CAR-008 (409) se documento está `validado` ou `processando`

---

### 4.5 Assistente — `/api/v1/assistente`

---

**POST /api/v1/assistente/conversas**

Inicia uma nova conversa com o assistente de IA.

- **Auth:** Bearer JWT
- **Request body:** `ConversaCreate`
- **Response 201:** `APIResponse[ConversaResponse]`

---

**POST /api/v1/assistente/conversas/{id}/mensagens**

Envia uma mensagem e recebe a resposta via SSE (Server-Sent Events) com streaming.

- **Auth:** Bearer JWT
- **Request body:** `MensagemCreate`
- **Content-Type da resposta:** `text/event-stream`
- **Response:** stream de eventos SSE (ver seção 7)
- **Erros:** CAR-030 (503) se o LLM estiver indisponível; CAR-003 (404) se conversa não encontrada

---

**GET /api/v1/assistente/conversas/{id}**

Retorna metadados de uma conversa específica.

- **Auth:** Bearer JWT
- **Response 200:** `APIResponse[ConversaResponse]`

---

**GET /api/v1/assistente/conversas/{id}/mensagens**

Histórico de mensagens de uma conversa com paginação.

- **Auth:** Bearer JWT
- **Query params:** `cursor`, `page_size`
- **Response 200:** `PaginatedResponse[MensagemResponse]` (ordem cronológica crescente)

---

**POST /api/v1/assistente/conversas/{id}/encerrar**

Encerra uma conversa ativa. Conversas encerradas não aceitam novas mensagens.

- **Auth:** Bearer JWT
- **Response 200:** `APIResponse[ConversaResponse]` com `status: "encerrada"`

---

**GET /api/v1/assistente/conversas**

Lista o histórico de conversas do usuário autenticado.

- **Auth:** Bearer JWT
- **Query params:** `cursor`, `page_size`, `status` (`ativa` | `encerrada` | `todas`)
- **Response 200:** `PaginatedResponse[ConversaResponse]` (mais recente primeiro)

---

### 4.6 Portal do Analista — `/api/v1/analista`

Todos os endpoints deste módulo exigem `tipo_usuario` = `analista`, `supervisor` ou `admin`.

---

**GET /api/v1/analista/processos**

Fila de processos pendentes de análise, com visão enriquecida.

- **Auth:** Bearer JWT (analista, supervisor, admin)
- **Query params:**

| Parâmetro | Descrição |
|---|---|
| `status` | Status do processo (padrão: `submetido,em_analise,pendente_documentacao`) |
| `prioridade` | Filtrar por prioridade |
| `municipio_ibge` | Filtrar por município |
| `estado` | Filtrar por UF |
| `analista_id` | Filtrar por analista responsável. `null` = sem analista |
| `cursor`, `page_size` | Paginação padrão |

- **Response 200:** `PaginatedResponse[ProcessoFilaAnalista]`
  - Inclui: `score_completude`, `score_risco`, `tempo_na_fila_horas`, `documentos_validados`, `pendencias_abertas`, `prazo_analise_at`

---

**POST /api/v1/analista/processos/{id}/assumir**

Atribui o processo ao analista autenticado.

- **Auth:** Bearer JWT (analista, supervisor, admin)
- **Request body:** vazio `{}`
- **Response 200:** `APIResponse[ProcessoCARResponse]` com `analista_responsavel` preenchido
- **Erros:** CAR-008 (409) se processo já assumido por outro analista (supervisor pode forçar reassignação)

---

**POST /api/v1/analista/processos/{id}/aprovar**

Aprova o processo e gera o número CAR oficial.

- **Auth:** Bearer JWT (analista, supervisor, admin)
- **Request body:** `AprovarProcessoBody`
- **Response 200:** `APIResponse[ProcessoCARResponse]` com `status: "aprovado"` e `numero_car` preenchido
- **Erros:** CAR-008 (409) se processo não está em `em_analise`

---

**POST /api/v1/analista/processos/{id}/rejeitar**

Rejeita o processo com motivo obrigatório.

- **Auth:** Bearer JWT (analista, supervisor, admin)
- **Request body:** `RejeitarProcessoBody`
- **Response 200:** `APIResponse[ProcessoCARResponse]` com `status: "rejeitado"`
- **Erros:** CAR-008 (409) se processo não está em `em_analise`

---

**POST /api/v1/analista/processos/{id}/criar-pendencia**

Cria uma pendência que o cidadão deve responder antes de retomar a análise.

- **Auth:** Bearer JWT (analista, supervisor, admin)
- **Request body:** `CriarPendenciaBody`
- **Response 201:** `APIResponse[PendenciaResponse]`
  - Processo é movido automaticamente para `pendente_documentacao`

---

**POST /api/v1/analista/processos/{id}/gerar-dossie**

Solicita geração assíncrona de dossiê PDF com resumo de IA.

- **Auth:** Bearer JWT (analista, supervisor, admin)
- **Request body:** `{"incluir_mapa": true, "incluir_historico": true}`
- **Response 202:** `{"data": {"job_id": "uuid", "status": "processando", "estimativa_segundos": 30}}`

---

**GET /api/v1/analista/dossies/{job_id}**

Verifica o status de geração do dossiê.

- **Auth:** Bearer JWT (analista, supervisor, admin)
- **Response 200:**
```json
{
  "data": {
    "job_id": "uuid",
    "status": "concluido",
    "download_url": "/api/v1/analista/dossies/uuid/download",
    "expires_at": "2024-01-15T18:00:00Z",
    "tamanho_bytes": 2457600
  }
}
```

---

**GET /api/v1/analista/dossies/{job_id}/download**

Faz download do PDF do dossiê gerado.

- **Auth:** Bearer JWT (analista, supervisor, admin)
- **Response 200:** arquivo PDF com headers `Content-Type: application/pdf` e `Content-Disposition: attachment; filename="dossie-{numero_car}.pdf"`
- **Erros:** CAR-003 (404) se job não encontrado; CAR-008 (409) se job ainda processando

---

**GET /api/v1/analista/dashboard**

Métricas consolidadas para o painel do analista.

- **Auth:** Bearer JWT (analista, supervisor, admin)
- **Query params:** `periodo` (7d | 30d | 90d, padrão 7d)
- **Response 200:** `APIResponse[DashboardAnalista]`

---

### 4.7 Admin — `/api/v1/admin`

Todos os endpoints deste módulo exigem `tipo_usuario` = `admin`.

---

**GET /api/v1/admin/usuarios**

Lista todos os usuários do sistema.

- **Auth:** Bearer JWT (admin)
- **Query params:** `tipo_usuario`, `status` (ativo | inativo), `busca` (nome ou email hash), `cursor`, `page_size`
- **Response 200:** `PaginatedResponse[UsuarioAdminResponse]`

---

**PATCH /api/v1/admin/usuarios/{id}/status**

Ativa ou desativa um usuário.

- **Auth:** Bearer JWT (admin)
- **Request body:** `{"status": "inativo", "motivo": "Conta duplicada"}`
- **Response 200:** `APIResponse[UsuarioAdminResponse]`
- **Erros:** não é possível desativar o próprio usuário admin

---

**GET /api/v1/admin/audit-logs**

Logs de auditoria com todos os eventos de modificação do sistema.

- **Auth:** Bearer JWT (supervisor, admin)
- **Query params:** `usuario_id`, `recurso`, `acao`, `data_inicio`, `data_fim`, `cursor`, `page_size`
- **Response 200:** `PaginatedResponse[AuditLogResponse]`

---

**POST /api/v1/admin/configuracoes/llm**

Atualiza configurações do provider de IA em runtime, sem necessidade de redeploy.

- **Auth:** Bearer JWT (admin)
- **Request body:**
```json
{
  "provider": "anthropic",
  "modelo": "claude-3-5-sonnet-20241022",
  "temperatura": 0.3,
  "max_tokens": 4096,
  "timeout_segundos": 30
}
```
- **Response 200:** configurações atualizadas
- **Erros:** CAR-004 (422) se provider/modelo inválido

---

**GET /api/v1/admin/metricas/sistema**

Métricas técnicas em tempo real do sistema.

- **Auth:** Bearer JWT (supervisor, admin)
- **Response 200:**
```json
{
  "data": {
    "filas": {
      "documentos_pendentes": 47,
      "dossies_pendentes": 3,
      "latencia_media_ms": 1200
    },
    "banco_de_dados": {
      "conexoes_ativas": 12,
      "conexoes_disponiveis": 88,
      "queries_lentas_ultima_hora": 2
    },
    "api": {
      "requisicoes_ultimo_minuto": 340,
      "taxa_erro_5xx_pct": 0.02,
      "p50_latencia_ms": 45,
      "p99_latencia_ms": 320
    },
    "llm": {
      "status": "operacional",
      "requisicoes_ultima_hora": 128,
      "tokens_ultima_hora": 987654,
      "taxa_erro_pct": 0.0
    }
  }
}
```

---

**POST /api/v1/admin/processos/{id}/reprocessar-documentos**

Reencaminha todos os documentos de um processo para reprocessamento OCR.

- **Auth:** Bearer JWT (admin)
- **Request body:** `{"documentos_ids": ["uuid1", "uuid2"]}` ou `{}` para todos
- **Response 202:** `{"data": {"jobs_enfileirados": 5, "job_ids": ["..."]}}`

---

### 4.8 Canal WhatsApp — `/api/v1/whatsapp`

#### Fluxo de Vinculação Gov.br

O WhatsApp não suporta redirecionamento OAuth2. A solução é um token temporário como "ponte":

```
1. Bot detecta número não vinculado
2. Solicita token: POST /api/v1/whatsapp/vincular/solicitar
3. Bot envia link: https://carla.gov.br/auth/wpp?token={token}
4. Usuário abre no browser do celular → Gov.br OAuth2 flow
5. Callback: GET /api/v1/whatsapp/vincular/callback?token=...&code=...
6. Sistema vincula number_hash ↔ user_id no Redis (TTL 30 dias)
7. Bot retoma a conversa já com o usuário identificado
```

---

**POST /api/v1/whatsapp/vincular/solicitar**

Gera token temporário de vinculação para um número WhatsApp.

- **Auth:** API Key interna (entre serviços)
- **Body:** `{"whatsapp_number_hash": "sha256_do_numero"}`
- **Response 200:**
```json
{
  "data": {
    "token": "abc123xyz",
    "link": "https://carla.gov.br/auth/wpp?token=abc123xyz",
    "expires_in_seconds": 600
  }
}
```

---

**GET /api/v1/whatsapp/vincular/callback**

Endpoint de retorno após autenticação Gov.br. Vincula número ao user_id.

- **Auth:** Pública (é o `redirect_uri` registrado no Gov.br)
- **Query:** `token`, `code` (authorization code Gov.br), `state`
- **Fluxo interno:**
  1. Valida token no Redis (TTL 10min) → se expirado: `CAR-011`
  2. Troca `code` por claims Gov.br (CPF, nome, nível)
  3. Cria ou recupera usuário no banco
  4. Salva `wpp:session:{number_hash}` → `user_id` no Redis (TTL 30 dias)
  5. Persiste em `canal_vinculos` (tabela de auditoria)
  6. Publica evento `canal.whatsapp.vinculado` no RabbitMQ
- **Response:** `HTTP 302` → `/auth/wpp/sucesso` (página de confirmação para fechar o browser)
- **Erros:** `CAR-011` (token expirado), `CAR-012` (Gov.br indisponível)

---

**POST /api/v1/whatsapp/webhook**

Recebe mensagens e eventos da Meta (WhatsApp Business API).

- **Auth:** Validação de assinatura HMAC-SHA256 via header `X-Hub-Signature-256`
- **Body:** Payload padrão Meta Webhook
- **Response 200:** `{}` — deve responder em < 20s (Meta considera timeout após isso)
- Processamento assíncrono: publica em fila `canal.whatsapp.mensagem_recebida`

**GET /api/v1/whatsapp/webhook**

Verificação de challenge pelo Meta ao cadastrar o webhook.

- **Auth:** Pública
- **Query:** `hub.mode`, `hub.challenge`, `hub.verify_token`
- **Response 200:** retorna `hub.challenge` como texto puro

---

**POST /api/v1/whatsapp/mensagem** *(uso interno)*

Envia mensagem ativa para um número (workers de notificação).

- **Auth:** API Key interna
- **Body:**
```json
{
  "whatsapp_number_hash": "sha256_do_numero",
  "tipo": "texto",
  "conteudo": "Seu processo foi aprovado!",
  "link_opcional": "https://carla.gov.br/processos/uuid"
}
```
- **Response 202:** mensagem enfileirada para envio

---

**DELETE /api/v1/whatsapp/vincular**

Remove a vinculação do número WhatsApp (direito de exclusão — LGPD Art. 18, IV).

- **Auth:** Bearer JWT (usuário autenticado no portal web)
- **Response 200:** vinculação removida do Redis e de `canal_vinculos`

---

### 4.9 Webhooks e Notificações — `/api/v1`

---

**GET /api/v1/notificacoes**

Lista notificações do usuário autenticado.

- **Auth:** Bearer JWT
- **Query params:** `lida` (true | false | todas), `cursor`, `page_size`
- **Response 200:** `PaginatedResponse[NotificacaoResponse]`

---

**PATCH /api/v1/notificacoes/{id}/lida**

Marca uma notificação como lida.

- **Auth:** Bearer JWT
- **Response 200:** `APIResponse[NotificacaoResponse]` com `lida: true`

---

**PATCH /api/v1/notificacoes/marcar-todas-lidas**

Marca todas as notificações do usuário como lidas.

- **Auth:** Bearer JWT
- **Response 200:** `{"data": {"total_marcadas": 12}}`

---

**POST /api/v1/webhooks/sicar**

Recebe atualizações de status do SICAR (Sistema Nacional de Cadastro Ambiental Rural).

- **Auth:** HMAC-SHA256 via header `X-SICAR-Signature`
  - Calculado como: `HMAC-SHA256(secret, request_body_bytes)`
  - Validado em tempo constante para evitar timing attacks
- **Request body:**
```json
{
  "evento": "status_atualizado",
  "numero_car": "MG-3106200-ABCD1234567890",
  "novo_status": "ativo",
  "data_evento": "2024-01-15T14:30:00Z"
}
```
- **Response 200:** `{"data": {"processado": true}}`
- **Response 400:** se assinatura inválida

---

## 5. Tratamento de Erros

### 5.1 Códigos de Erro Padronizados

| Código | HTTP Status | Mensagem Padrão | Quando Ocorre |
|---|---|---|---|
| CAR-001 | 401 | Não autenticado | Token ausente, malformado, expirado ou revogado |
| CAR-002 | 403 | Acesso negado | Usuário não tem permissão para o recurso ou ação |
| CAR-003 | 404 | Recurso não encontrado | UUID inexistente ou sem acesso (por segurança, retorna 404 em vez de 403) |
| CAR-004 | 422 | Dados de entrada inválidos | Falha de validação Pydantic (campos obrigatórios, formatos, ranges) |
| CAR-005 | 413 | Arquivo muito grande | Arquivo acima de 50 MB |
| CAR-006 | 415 | Tipo de arquivo não suportado | MIME type não está na lista de aceitos |
| CAR-007 | 409 | Documento duplicado | Hash SHA-256 já existe para o processo informado |
| CAR-008 | 409 | Conflito de estado | Ação não permitida no estado atual do recurso |
| CAR-009 | 429 | Idempotency key já em uso | Requisição com mesma chave já está em processamento |
| CAR-010 | 400 | State OAuth inválido | State não coincide ou já foi utilizado (CSRF protection) |
| CAR-011 | 400 | Authorization code expirado | Código OAuth2 expirado ou já utilizado |
| CAR-012 | 503 | Gov.br indisponível | Timeout ou erro na comunicação com Gov.br |
| CAR-020 | 422 | Geometria inválida | Polígono não fecha, auto-intersecção ou coordenadas fora do Brasil |
| CAR-021 | 422 | Município não encontrado | Código IBGE inválido ou inexistente |
| CAR-022 | 422 | Área inconsistente | Área declarada difere mais de 20% da área calculada pela geometria |
| CAR-030 | 503 | Assistente temporariamente indisponível | LLM offline ou timeout |
| CAR-031 | 400 | Conversa encerrada | Tentativa de enviar mensagem para conversa encerrada |
| CAR-040 | 503 | Sistema externo indisponível | SICAR ou SIGEF com timeout ou erro |
| CAR-050 | 429 | Rate limit excedido | Número de requisições acima do limite permitido |
| CAR-060 | 409 | Processo não pode ser submetido | Documentação incompleta, geometria ausente ou dados obrigatórios faltando |
| CAR-061 | 409 | Processo já está sendo analisado | Tentativa de outro analista assumir processo já atribuído |
| CAR-070 | 500 | Erro interno | Exceção não tratada — registrada com request_id para debugging |

### 5.2 Exemplo de Resposta de Erro Simples

```json
{
  "error": {
    "code": "CAR-003",
    "message": "Recurso não encontrado",
    "details": []
  }
}
```

### 5.3 Exemplo de Resposta de Erro de Validação (CAR-004)

```json
{
  "error": {
    "code": "CAR-004",
    "message": "Dados de entrada inválidos",
    "details": [
      {
        "field": "municipio_ibge",
        "code": "invalid_format",
        "message": "Deve ter exatamente 7 dígitos numéricos"
      },
      {
        "field": "area_total_ha",
        "code": "must_be_positive",
        "message": "Área deve ser maior que zero"
      },
      {
        "field": "geometria_geojson.coordinates",
        "code": "polygon_not_closed",
        "message": "O anel exterior do polígono deve ter o primeiro ponto igual ao último"
      }
    ]
  }
}
```

### 5.4 Implementação FastAPI — Exception Handler Global

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import uuid


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
            details.append({
                "field": field or None,
                "code": error["type"],
                "message": error["msg"]
            })
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "CAR-004",
                    "message": "Dados de entrada inválidos",
                    "details": details
                }
            }
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        # Log estruturado com request_id para correlação
        import logging
        logging.error(f"Unhandled exception [{request_id}]: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "CAR-070",
                    "message": "Erro interno do servidor",
                    "details": [
                        {
                            "field": None,
                            "code": "internal_error",
                            "message": f"Contate o suporte com o ID: {request_id}"
                        }
                    ]
                }
            }
        )
```

---

## 6. Rate Limiting

### 6.1 Limites por Role e Tipo de Endpoint

| Endpoint / Categoria | Produtor Rural | Consultor Ambiental | Analista | Supervisor | Admin |
|---|:---:|:---:|:---:|:---:|:---:|
| `GET` — leitura geral | 60/min | 120/min | 200/min | 200/min | sem limite |
| `POST /processos` | 10/min | 30/min | 50/min | 50/min | sem limite |
| `PATCH` — atualizações | 30/min | 60/min | 100/min | 100/min | sem limite |
| `POST /documentos/upload` | 5/min | 15/min | 30/min | 30/min | sem limite |
| `POST /assistente/conversas` | 5/hora | 5/hora | 10/hora | 10/hora | sem limite |
| `POST /assistente/mensagens` | 20/min | 20/min | 20/min | 20/min | sem limite |
| `POST /processos/{id}/submeter` | 3/hora | 10/hora | N/A | N/A | sem limite |
| `GET /auth/*` | 10/min | 10/min | 10/min | 10/min | sem limite |

### 6.2 Implementação de Headers

Todas as respostas incluem:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 47
X-RateLimit-Reset: 1705312260
```

Quando o limite é excedido (HTTP 429):
```json
{
  "error": {
    "code": "CAR-050",
    "message": "Rate limit excedido",
    "details": [
      {
        "field": null,
        "code": "rate_limit_exceeded",
        "message": "Aguarde 45 segundos antes de realizar nova requisição"
      }
    ]
  }
}
```

Headers adicionais no 429:
```
Retry-After: 45
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705312260
```

### 6.3 Estratégia de Implementação

- **Algoritmo:** Token Bucket com janela deslizante de 60 segundos
- **Storage:** Redis com chave `ratelimit:{user_id}:{endpoint_category}`
- **IP fallback:** para endpoints públicos (auth), limitar por IP: 20 req/min
- **Burst:** permitir burst de até 2x o limite por no máximo 5 segundos

---

## 7. SSE — Server-Sent Events para o Assistente

### 7.1 Protocolo de Eventos

O assistente utiliza SSE (Server-Sent Events) para streaming de respostas da IA, evitando timeouts em respostas longas e melhorando a experiência percebida.

**Eventos disponíveis:**

| Evento | Quando emitido | Dados |
|---|---|---|
| `token` | A cada chunk de texto gerado pelo LLM | `{"content": "texto parcial"}` |
| `done` | Quando a geração completa | metadados completos da mensagem |
| `error` | Em caso de falha durante geração | código e mensagem de erro |
| `heartbeat` | A cada 15s se nenhum token foi emitido | `{}` (keepalive) |

**Fluxo completo de eventos:**
```
event: token
data: {"content": "O Cadastro"}

event: token
data: {"content": " Ambiental"}

event: token
data: {"content": " Rural (CAR)"}

event: token
data: {"content": " é um instrumento"}

[... demais tokens ...]

event: done
data: {
  "message_id": "550e8400-e29b-41d4-a716-446655440001",
  "conversa_id": "550e8400-e29b-41d4-a716-446655440000",
  "role": "assistant",
  "tokens_prompt": 150,
  "tokens_completion": 312,
  "latencia_ms": 1847,
  "modelo_utilizado": "claude-3-5-sonnet-20241022",
  "created_at": "2024-01-15T14:30:00Z"
}
```

**Em caso de erro durante geração:**
```
event: error
data: {"code": "CAR-030", "message": "Assistente temporariamente indisponível. Tente novamente em instantes."}
```

**Heartbeat (keepalive):**
```
event: heartbeat
data: {}
```

### 7.2 Implementação FastAPI

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from uuid import UUID, uuid4
from datetime import datetime, timezone
import json
import asyncio

router = APIRouter(prefix="/assistente", tags=["Assistente"])


async def chat_stream_generator(
    conversa_id: UUID,
    mensagem: str,
    ai_service: AIService,
) -> AsyncIterator[str]:
    """
    Gerador assíncrono de eventos SSE para o streaming do assistente.
    Emite eventos no formato: "event: <tipo>\\ndata: <json>\\n\\n"
    """
    message_id = uuid4()
    tokens_completion = 0
    inicio = datetime.now(timezone.utc)

    try:
        async for chunk in ai_service.completar_stream(conversa_id, mensagem):
            tokens_completion += 1
            payload = json.dumps({"content": chunk}, ensure_ascii=False)
            yield f"event: token\ndata: {payload}\n\n"

        latencia_ms = int(
            (datetime.now(timezone.utc) - inicio).total_seconds() * 1000
        )
        done_payload = json.dumps({
            "message_id": str(message_id),
            "conversa_id": str(conversa_id),
            "role": "assistant",
            "tokens_completion": tokens_completion,
            "latencia_ms": latencia_ms,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
        yield f"event: done\ndata: {done_payload}\n\n"

    except LLMUnavailableError:
        error_payload = json.dumps({
            "code": "CAR-030",
            "message": "Assistente temporariamente indisponível"
        })
        yield f"event: error\ndata: {error_payload}\n\n"

    except Exception as exc:
        error_payload = json.dumps({
            "code": "CAR-070",
            "message": "Erro interno durante geração da resposta"
        })
        yield f"event: error\ndata: {error_payload}\n\n"


@router.post(
    "/conversas/{id}/mensagens",
    summary="Enviar mensagem ao assistente com streaming SSE",
    response_description="Stream de eventos SSE com a resposta do assistente",
)
async def enviar_mensagem(
    id: UUID,
    body: MensagemCreate,
    current_user: UsuarioAutenticado = Depends(get_current_user),
    ai_service: AIService = Depends(get_ai_service),
) -> StreamingResponse:
    # Valida existência e acesso à conversa
    conversa = await conversa_service.get_or_404(id, current_user.id)
    if conversa.status == "encerrada":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "CAR-031", "message": "Conversa está encerrada"}
        )

    return StreamingResponse(
        chat_stream_generator(id, body.conteudo, ai_service),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",     # Desativa buffer do Nginx
            "Access-Control-Allow-Origin": "*",
        }
    )
```

### 7.3 Consumo no Cliente (JavaScript)

```javascript
const response = await fetch('/api/v1/assistente/conversas/{id}/mensagens', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`,
  },
  body: JSON.stringify({ conteudo: 'Como registro o CAR?' }),
});

const reader = response.body.getReader();
const decoder = new TextDecoder();
let buffer = '';

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  buffer += decoder.decode(value, { stream: true });
  const lines = buffer.split('\n');
  buffer = lines.pop(); // linha incompleta fica no buffer

  for (const line of lines) {
    if (line.startsWith('event: ')) {
      currentEvent = line.slice(7).trim();
    } else if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      if (currentEvent === 'token') {
        appendToChat(data.content);
      } else if (currentEvent === 'done') {
        finalizeMessage(data);
      } else if (currentEvent === 'error') {
        showError(data.message);
      }
    }
  }
}
```

---

## 8. OpenAPI — Contrato e Especificação

### 8.1 Header do Contrato YAML

```yaml
openapi: "3.1.0"

info:
  title: "CARla API"
  description: |
    API do CARla — Plataforma Inteligente para o Cadastro Ambiental Rural.

    ## Autenticação
    Todas as rotas protegidas requerem um Bearer JWT obtido via fluxo OAuth2 com Gov.br.
    Para testar: use `GET /api/v1/auth/govbr/authorize` para iniciar o fluxo.

    ## Paginação
    Listas utilizam paginação cursor-based. Passe o valor de `meta.cursor_next`
    como `?cursor=<valor>` na próxima requisição.

    ## Rate Limiting
    Respostas incluem headers `X-RateLimit-*`. Ao atingir o limite, retorna HTTP 429
    com header `Retry-After`.

    ## Ambiente de Sandbox
    Para testes de integração, use `https://sandbox-api.carcopilot.gov.br/api/v1`.
    Autenticação no sandbox aceita usuários de teste criados via
    `POST /api/v1/sandbox/usuarios`.
  version: "1.0.0"
  contact:
    name: "Equipe CARla"
    email: "suporte@carcopilot.gov.br"
    url: "https://carcopilot.gov.br/suporte"
  license:
    name: "Apache 2.0"
    url: "https://www.apache.org/licenses/LICENSE-2.0"
  x-logo:
    url: "https://carcopilot.gov.br/assets/logo.png"

servers:
  - url: "https://api.carcopilot.gov.br/api/v1"
    description: "Produção"
  - url: "https://staging-api.carcopilot.gov.br/api/v1"
    description: "Staging"
  - url: "https://sandbox-api.carcopilot.gov.br/api/v1"
    description: "Sandbox (testes de integração)"
  - url: "http://localhost:8000/api/v1"
    description: "Desenvolvimento local"

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT gerado após autenticação via Gov.br. Válido por 1 hora.
        Para renovar, use `POST /auth/refresh`.

  parameters:
    cursor:
      name: cursor
      in: query
      required: false
      schema:
        type: string
      description: "Cursor opaco para paginação. Obter de `meta.cursor_next`."

    page_size:
      name: page_size
      in: query
      required: false
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20
      description: "Número de itens por página."

    idempotency_key:
      name: Idempotency-Key
      in: header
      required: true
      schema:
        type: string
        format: uuid
      description: "UUID v4 para garantir idempotência em operações críticas."

  responses:
    Unauthorized:
      description: "Token ausente, inválido ou expirado."
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            error:
              code: "CAR-001"
              message: "Não autenticado"
              details: []

    Forbidden:
      description: "Usuário autenticado mas sem permissão para o recurso."
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

    NotFound:
      description: "Recurso não encontrado."
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

    UnprocessableEntity:
      description: "Dados de entrada inválidos."
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

    TooManyRequests:
      description: "Rate limit excedido."
      headers:
        Retry-After:
          schema:
            type: integer
          description: "Segundos para aguardar antes de nova tentativa."
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

security:
  - BearerAuth: []

tags:
  - name: "Auth"
    description: "Autenticação via Gov.br, emissão e renovação de tokens"
  - name: "Imóveis"
    description: "Gestão de imóveis rurais e geometrias"
  - name: "Processos"
    description: "Processos CAR — criação, submissão e acompanhamento"
  - name: "Documentos"
    description: "Upload, validação OCR e consulta de documentos"
  - name: "Assistente"
    description: "Chatbot de IA com streaming SSE"
  - name: "Analista"
    description: "Portal do analista — fila, aprovação, rejeição e dossiês"
  - name: "Admin"
    description: "Administração de usuários, logs e configurações"
  - name: "Notificações"
    description: "Notificações do usuário"
  - name: "Webhooks"
    description: "Recebimento de eventos externos (SICAR)"
```

### 8.2 Exposição via FastAPI

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI) -> dict:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="CARla API",
        version="1.0.0",
        description="API do CARla — Plataforma Inteligente para o Cadastro Ambiental Rural",
        routes=app.routes,
    )

    # Adicionar componentes de segurança
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Aplicar segurança global
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(
    title="CARla API",
    version="1.0.0",
    docs_url="/api/v1/docs",         # Swagger UI
    redoc_url="/api/v1/redoc",       # ReDoc
    openapi_url="/api/v1/openapi.json",
)
app.openapi = lambda: custom_openapi(app)
```

---

## 9. Versionamento da API

### 9.1 Política de Versões

| Conceito | Decisão |
|---|---|
| Versão atual | `/api/v1/` |
| Próxima versão (quando necessário) | `/api/v2/` |
| Formato de versão | Inteiro incremental no prefixo da URL |
| Coexistência de versões | Mínimo 12 meses após início da deprecação |
| Aviso prévio de deprecação | Mínimo 6 meses antes do Sunset |

### 9.2 O que Exige Nova Versão (Breaking Change)

- Remoção de um campo obrigatório da resposta
- Alteração do tipo de um campo existente
- Mudança no comportamento de um endpoint existente
- Remoção de um endpoint
- Alteração nos códigos de erro existentes (renomeação de `CAR-XXX`)
- Mudança na estrutura do envelope de resposta

### 9.3 O que Não Exige Nova Versão (Non-Breaking Change)

- Adição de novos campos opcionais na resposta
- Adição de novos endpoints
- Adição de novos query params opcionais
- Adição de novos valores a enums existentes (com backward compat)
- Novos códigos de erro (novos `CAR-XXX`)
- Melhorias de performance sem mudança de contrato

### 9.4 Ciclo de Vida de Deprecação

Quando uma funcionalidade é marcada para deprecação:

1. **Mês 0** — Anúncio público e adição dos headers nas respostas:
   ```
   Deprecation: Mon, 15 Jul 2024 00:00:00 GMT
   Sunset: Mon, 15 Jan 2025 00:00:00 GMT
   Link: <https://docs.carcopilot.gov.br/migration/v1-to-v2>; rel="successor-version"
   ```

2. **Meses 1-6** — Período de migração com ambas as versões funcionando. Logs de uso da versão deprecated são monitorados.

3. **Mês 6** — Resposta passa a incluir warning no campo `meta`:
   ```json
   {
     "data": {...},
     "meta": {
       "request_id": "...",
       "timestamp": "...",
       "deprecation_warning": "Este endpoint será removido em 2025-01-15. Migre para /api/v2/processos."
     }
   }
   ```

4. **Mês 12 (Sunset)** — Endpoint retorna HTTP 410 Gone com link para documentação de migração.

### 9.5 Canais de Comunicação de Breaking Changes

- Email para todos os usuários de API cadastrados (via chave de API)
- Post no portal de desenvolvedores `https://docs.carcopilot.gov.br`
- Changelog versionado disponível em `GET /api/v1/changelog`
- Header `Deprecation` + `Sunset` em todas as respostas do endpoint afetado

---

*Documento mantido pela equipe de Plataforma do CARla.*  
*Para contribuições ou dúvidas: suporte@carcopilot.gov.br*
