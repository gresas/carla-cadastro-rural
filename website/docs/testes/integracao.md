---
sidebar_position: 3
title: Testes de Integração
description: pytest + TestContainers — banco real, API completa e workers RabbitMQ.
tags: [engenharia, testes, integração, testcontainers]
---

# Testes de Integração

:::info Para quem é esta página
Engenheiros back-end.
:::

## Setup com TestContainers

```python
# tests/conftest.py
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture(scope="session")
async def postgres_container():
    with PostgresContainer("postgis/postgis:16-3.4") as pg:
        yield pg

@pytest.fixture(scope="session")
async def db_engine(postgres_container):
    url = postgres_container.get_connection_url().replace(
        "postgresql://", "postgresql+asyncpg://"
    )
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine

@pytest.fixture
async def db_session(db_engine):
    async with AsyncSession(db_engine) as session:
        async with session.begin():
            yield session
            await session.rollback()  # cleanup após cada teste
```

## Testando a API

```python
# tests/integration/test_processos_api.py
from httpx import AsyncClient, ASGITransport
from carla.main import create_app

@pytest.fixture
async def client(db_session):
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

class TestProcessosAPI:
    async def test_criar_processo_retorna_201(self, client, token_produtor, imovel):
        response = await client.post(
            "/api/v1/processos",
            json={"imovel_id": str(imovel.id)},
            headers={"Authorization": f"Bearer {token_produtor}"},
        )
        assert response.status_code == 201
        assert response.json()["data"]["status"] == "rascunho"

    async def test_sem_autenticacao_retorna_401(self, client):
        response = await client.post("/api/v1/processos", json={})
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "CAR-001"

    async def test_processo_de_outro_usuario_retorna_404(
        self, client, token_produtor_a, processo_de_b
    ):
        response = await client.get(
            f"/api/v1/processos/{processo_de_b.id}",
            headers={"Authorization": f"Bearer {token_produtor_a}"},
        )
        assert response.status_code == 404  # 404, não 403
```

:::tip Rollback após cada teste
A fixture `db_session` faz rollback ao final de cada teste — o banco volta ao estado inicial sem precisar recriar tabelas. Isso é ~10x mais rápido que truncate.
:::
