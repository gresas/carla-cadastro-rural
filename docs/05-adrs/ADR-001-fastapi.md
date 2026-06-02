# ADR-001: Uso de FastAPI como Framework Web Python

**Status:** Aceito  
**Data:** 2026-06-01  
**Contexto:** Backend — todos os serviços de API REST

---

## Contexto

Precisamos de um framework Python para construir APIs REST para o CARla. A equipe tem experiência em Python. Os requisitos são:

- Suporte nativo a `async/await` (operações de I/O intensivo: banco, LLM, integrações externas)
- Validação de dados com tipagem forte (alinhado com DDD — Value Objects com Pydantic)
- Documentação OpenAPI automática (essencial para hackathon e equipes externas)
- Performance adequada para 500+ usuários simultâneos no MVP
- Ecossistema maduro com suporte para injeção de dependências

O contexto é um hackathon com deadline apertado que pode evoluir para produto governamental real.

---

## Decisão

**Adotar FastAPI 0.115+ com:**
- Pydantic v2 para validação de dados e schemas
- Uvicorn como ASGI server (dev)
- Gunicorn + workers Uvicorn em produção
- `async def` em todos os endpoints e serviços com I/O
- Dependency Injection via `Depends()` para serviços, repositórios e autenticação

```python
# Exemplo do padrão adotado
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

app = FastAPI(
    title="CARla API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

@app.post("/api/v1/processos", response_model=ProcessoCARResponse, status_code=201)
async def criar_processo(
    dados: ProcessoCARCreate,
    current_user: Annotated[UsuárioAutenticado, Depends(get_current_user)],
    use_case: Annotated[CriarProcessoUseCase, Depends(get_criar_processo_use_case)],
) -> ProcessoCARResponse:
    result = await use_case.execute(dados, current_user.id)
    return ProcessoCARResponse.from_domain(result)
```

---

## Consequências

### Positivas
- **Performance:** FastAPI + Uvicorn processa ~50.000 req/s em benchmarks sintéticos (TechEmpower Framework Benchmarks Round 22); ~3-5x mais rápido que Django DRF em I/O-bound workloads
- **Documentação automática:** Swagger UI e ReDoc gerados automaticamente via OpenAPI — crítico para hackathon
- **Type safety end-to-end:** Pydantic v2 valida requests, responses e configurações com type hints Python nativos
- **DDD-friendly:** Pydantic v2 BaseModel perfeito para Value Objects do domínio com validadores customizados
- **Startup rápido:** Ideal para Kubernetes — readiness probe em < 2s
- **SSE nativo:** `StreamingResponse` com generators assíncronos — necessário para o assistente IA

### Negativas
- **Ecossistema menor que Django:** Menos pacotes de "batteries included" (admin, ORM integrado)
- **Async mindset obrigatório:** Erros sutis ao misturar código síncrono com async (ex: drivers síncronos bloqueiam o event loop)
- **Sem ORM embutido:** Requer escolha e configuração separada do SQLAlchemy 2.0

### Riscos
- Desenvolvedores acostumados com Django/Flask precisam de curva de aprendizado em async Python
- Dependency Injection do FastAPI tem limitações em cenários de teste complexos (mitigado com fixtures pytest)

---

## Alternativas Consideradas

| Alternativa | Prós | Contras | Motivo da Rejeição |
|---|---|---|---|
| **Django REST Framework** | Maduro, admin integrado, ORM robusto | Síncrono por padrão, mais verboso, overhead para APIs puras | Performance insuficiente para async workloads; overhead desnecessário |
| **Flask + marshmallow** | Simples, flexível | Muito manual (sem docs automáticas, sem DI, sem async nativo) | Produtividade baixa para hackathon; sem OpenAPI automático |
| **Litestar (ex-Starlite)** | Moderno, async nativo, DI mais robusto que FastAPI | Menos maduro, comunidade menor, documentação em evolução | Risco de bugs em produção governamental; suporte menor |
| **gRPC (Protobuf)** | Performance, contrato forte | Complexidade para web clients, sem browser-friendly out of the box | Frontend React precisa de REST; gRPC para comunicação interna futura |

---

## Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TechEmpower Benchmarks](https://www.techempower.com/benchmarks/)
- [Pydantic v2 Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [Uvicorn ASGI server](https://www.uvicorn.org/)
