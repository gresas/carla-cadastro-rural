# CARla — Estratégia de Testes

**Versão:** 1.0.0  
**Data:** 2026-06-01

---

## 1. Filosofia e Pirâmide de Testes

```
                    ┌───────────────┐
                    │   Carga (k6)  │  2% — ~10 cenários
                    │  Segurança    │
                    └───────┬───────┘
                  ┌─────────┴──────────┐
                  │  E2E (Playwright)  │  3% — ~20 fluxos críticos
                  └─────────┬──────────┘
               ┌────────────┴──────────────┐
               │  Contrato (Pact)          │  5% — APIs entre serviços
               └────────────┬──────────────┘
          ┌──────────────────┴────────────────────┐
          │  Integração (pytest + TestContainers)  │  20% — com banco/infra real
          └──────────────────┬────────────────────┘
     ┌─────────────────────────────────────────────────┐
     │          Unitários (pytest)                      │  70% — isolados, sem I/O
     │  Domínio: entidades, VOs, serviços de domínio   │
     └─────────────────────────────────────────────────┘
```

**Princípios:**
- **FIRST:** Fast, Isolated, Repeatable, Self-validating, Timely
- **Arrange-Act-Assert** em todos os testes
- **Given-When-Then** (Gherkin) para cenários de negócio
- Testes documentam comportamento esperado — mais valor que comments
- Mocks apenas para dependências externas não controladas (LLM, SICAR)

---

## 2. Testes Unitários (pytest)

### Configuração

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = """
  --cov=src
  --cov-report=term-missing
  --cov-report=html:htmlcov
  --cov-fail-under=80
  -p no:warnings
"""

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "@abstractmethod",
]
```

### Cobertura Mínima por Camada

| Camada | Cobertura Mínima | Justificativa |
|---|---|---|
| Domain (entities, VOs, services) | 95% | Regras de negócio críticas |
| Application (use cases) | 85% | Orquestração de fluxos |
| Infrastructure (repositories) | 70% | I/O mockado; cobrir mapeamentos |
| Presentation (routes) | 80% | Validação de entrada e resposta |

### Exemplos — Domínio de Processos

```python
# tests/unit/processos/domain/test_value_objects.py
import pytest
from carla.modules.processos.domain.value_objects import (
    NumeroCAR, ÁreaTotalHectares, CPF, MunicípioIBGE
)

class TestNumeroCAR:
    def test_formato_valido_deve_ser_aceito(self):
        numero = NumeroCAR(valor="MA-0001234-20240115123456")
        assert numero.valor == "MA-0001234-20240115123456"
        assert numero.estado == "MA"

    @pytest.mark.parametrize("valor_invalido", [
        "MA-123-456",            # sequencial curto
        "123-0001234-00000000000000",  # sem UF
        "ma-0001234-20240115123456",   # UF minúscula
        "MA0001234-20240115123456",    # sem hífen
        "",
    ])
    def test_formato_invalido_deve_lancar_value_error(self, valor_invalido):
        with pytest.raises(ValueError, match="Número CAR inválido"):
            NumeroCAR(valor=valor_invalido)

    def test_igualdade_por_valor(self):
        a = NumeroCAR(valor="MA-0001234-20240115123456")
        b = NumeroCAR(valor="MA-0001234-20240115123456")
        assert a == b

    def test_numeros_diferentes_nao_sao_iguais(self):
        a = NumeroCAR(valor="MA-0001234-20240115123456")
        b = NumeroCAR(valor="PA-0009999-20240115999999")
        assert a != b


class TestÁreaTotalHectares:
    def test_area_positiva_deve_ser_aceita(self):
        area = ÁreaTotalHectares(valor=150.5)
        assert area.valor == 150.5

    def test_area_zero_deve_ser_rejeitada(self):
        with pytest.raises(ValueError, match="maior que zero"):
            ÁreaTotalHectares(valor=0.0)

    def test_area_negativa_deve_ser_rejeitada(self):
        with pytest.raises(ValueError):
            ÁreaTotalHectares(valor=-10.0)

    def test_area_implausivel_deve_ser_rejeitada(self):
        with pytest.raises(ValueError, match="implausível"):
            ÁreaTotalHectares(valor=20_000_000.0)

    def test_area_arredondada_para_4_casas(self):
        area = ÁreaTotalHectares(valor=150.12345678)
        assert area.valor == 150.1235

    def test_conversao_para_modulos_fiscais(self):
        area = ÁreaTotalHectares(valor=100.0)
        assert area.em_modulos_fiscais(modulo_fiscal_ha=25.0) == 4.0


class TestCPF:
    def test_cpf_valido_deve_ser_aceito(self):
        # CPF de teste gerado por algoritmo (não real)
        cpf = CPF(valor="529.982.247-25")
        assert cpf.valor == "52998224725"

    def test_cpf_invalido_deve_ser_rejeitado(self):
        with pytest.raises(ValueError, match="CPF inválido"):
            CPF(valor="123.456.789-00")

    def test_cpf_com_todos_digitos_iguais_rejeitado(self):
        with pytest.raises(ValueError, match="todos os dígitos iguais"):
            CPF(valor="111.111.111-11")

    def test_formatacao(self):
        cpf = CPF(valor="52998224725")
        assert cpf.formatado == "529.982.247-25"

    def test_mascaramento_para_logs(self):
        cpf = CPF(valor="52998224725")
        assert cpf.mascarado == "***.***.247-**"
```

```python
# tests/unit/processos/domain/test_entities.py
import pytest
from datetime import datetime
from uuid import uuid4
from unittest.mock import patch
from carla.modules.processos.domain.entities import ProcessoCAR
from carla.modules.processos.domain.value_objects import StatusProcesso
from carla.modules.processos.domain.events import ProcessoSubmetido
from carla.modules.processos.domain.exceptions import (
    EstadoInvalidoError, DocumentacaoInsuficienteError, PermissionDeniedError
)

class TestProcessoCAR:
    @pytest.fixture
    def processo_em_preenchimento(self):
        """Processo com documentação mínima válida."""
        return ProcessoCAR(
            id=uuid4(),
            status=StatusProcesso.EM_PREENCHIMENTO,
            requerente_id=uuid4(),
            documentos=[
                # matricula válida
                make_documento("matricula_imovel", "valido"),
                # CCIR válido
                make_documento("ccir", "valido"),
            ],
            imovel_geometria_definida=True,
            # ... outros campos com defaults
        )

    def test_submeter_processo_completo_deve_mudar_status(self, processo_em_preenchimento):
        requerente_id = processo_em_preenchimento.requerente_id
        processo_em_preenchimento.submeter(requerente_id)
        assert processo_em_preenchimento.status == StatusProcesso.SUBMETIDO

    def test_submeter_processo_deve_emitir_evento(self, processo_em_preenchimento):
        requerente_id = processo_em_preenchimento.requerente_id
        processo_em_preenchimento.submeter(requerente_id)
        eventos = processo_em_preenchimento.domain_events
        assert len(eventos) == 1
        assert isinstance(eventos[0], ProcessoSubmetido)
        assert eventos[0].processo_id == processo_em_preenchimento.id

    def test_submeter_por_outro_usuario_deve_lancar_permissao(self, processo_em_preenchimento):
        outro_usuario_id = uuid4()
        with pytest.raises(PermissionDeniedError):
            processo_em_preenchimento.submeter(outro_usuario_id)

    def test_submeter_sem_matricula_deve_lancar_documentacao_insuficiente(self):
        processo = ProcessoCAR(
            id=uuid4(),
            status=StatusProcesso.EM_PREENCHIMENTO,
            requerente_id=(rid := uuid4()),
            documentos=[make_documento("ccir", "valido")],
            imovel_geometria_definida=True,
        )
        with pytest.raises(DocumentacaoInsuficienteError):
            processo.submeter(rid)

    def test_submeter_sem_geometria_deve_lancar_erro(self):
        processo = ProcessoCAR(
            id=uuid4(),
            status=StatusProcesso.EM_PREENCHIMENTO,
            requerente_id=(rid := uuid4()),
            documentos=[
                make_documento("matricula_imovel", "valido"),
                make_documento("ccir", "valido"),
            ],
            imovel_geometria_definida=False,
        )
        with pytest.raises(Exception, match="[Gg]eometria"):
            processo.submeter(rid)

    def test_resubmeter_processo_ja_submetido_deve_falhar(self, processo_em_preenchimento):
        rid = processo_em_preenchimento.requerente_id
        processo_em_preenchimento.submeter(rid)
        with pytest.raises(EstadoInvalidoError):
            processo_em_preenchimento.submeter(rid)

    def test_aprovar_sem_analista_atribuido_deve_falhar(self, processo_em_preenchimento):
        rid = processo_em_preenchimento.requerente_id
        processo_em_preenchimento.submeter(rid)
        # Processo em análise mas analista_id é None
        with pytest.raises(PermissionDeniedError):
            processo_em_preenchimento.aprovar(analista_id=uuid4())
```

```python
# tests/unit/processos/domain/test_services.py
from carla.modules.processos.domain.services import CalculadorAreaReservaLegal
from carla.modules.processos.domain.value_objects import ÁreaTotalHectares

class TestCalculadorAreaReservaLegal:
    @pytest.fixture
    def calculador(self):
        return CalculadorAreaReservaLegal()

    def test_amazonia_legal_exige_80_porcento(self, calculador):
        area_total = ÁreaTotalHectares(valor=100.0)
        area_minima = calculador.calcular_area_minima(area_total, "amazonia_legal")
        assert area_minima.valor == 80.0

    def test_cerrado_na_amazonia_exige_35_porcento(self, calculador):
        area_total = ÁreaTotalHectares(valor=200.0)
        area_minima = calculador.calcular_area_minima(area_total, "cerrado_amazonia_legal")
        assert area_minima.valor == 70.0

    def test_mata_atlantica_exige_20_porcento(self, calculador):
        area_total = ÁreaTotalHectares(valor=50.0)
        area_minima = calculador.calcular_area_minima(area_total, "mata_atlantica")
        assert area_minima.valor == 10.0

    def test_bioma_desconhecido_lanca_value_error(self, calculador):
        with pytest.raises(ValueError, match="Bioma desconhecido"):
            calculador.calcular_area_minima(ÁreaTotalHectares(valor=100.0), "bioma_invalido")

    def test_verificar_conformidade_aprovada(self, calculador):
        area_rl = ÁreaTotalHectares(valor=85.0)
        area_total = ÁreaTotalHectares(valor=100.0)
        conforme, mensagem = calculador.verificar_conformidade(area_rl, area_total, "amazonia_legal")
        assert conforme is True
        assert "Conforme" in mensagem

    def test_verificar_conformidade_reprovada(self, calculador):
        area_rl = ÁreaTotalHectares(valor=50.0)
        area_total = ÁreaTotalHectares(valor=100.0)
        conforme, mensagem = calculador.verificar_conformidade(area_rl, area_total, "amazonia_legal")
        assert conforme is False
        assert "Não conforme" in mensagem
```

---

## 3. Testes de Integração (TestContainers)

### Configuração de Fixtures

```python
# tests/conftest.py
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from httpx import AsyncClient, ASGITransport

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def postgres_container():
    with PostgresContainer("postgis/postgis:16-3.4") as pg:
        pg.start()
        yield pg

@pytest.fixture(scope="session")
async def db_engine(postgres_container):
    url = postgres_container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    async with AsyncSession(db_engine) as session:
        async with session.begin():
            yield session
            await session.rollback()  # Rollback após cada teste

@pytest.fixture
async def client(db_session):
    from carla.main import create_app
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

@pytest.fixture
async def token_produtor(client, db_session):
    """JWT válido para usuário produtor."""
    usuario = await criar_usuario_test(db_session, tipo="produtor_rural")
    return gerar_jwt_test(usuario)

@pytest.fixture
async def token_analista(client, db_session):
    usuario = await criar_usuario_test(db_session, tipo="analista_ambiental")
    return gerar_jwt_test(usuario)

@pytest.fixture
async def processo_rascunho(db_session, token_produtor):
    """Processo no status rascunho com usuário produtor."""
    return await criar_processo_test(db_session, status="rascunho")
```

### Testes de API

```python
# tests/integration/test_processos_api.py
import pytest
from httpx import AsyncClient

class TestProcessosAPI:
    async def test_criar_processo_autenticado_retorna_201(self, client, token_produtor, imovel_criado):
        response = await client.post(
            "/api/v1/processos",
            json={"imovel_id": str(imovel_criado.id)},
            headers={"Authorization": f"Bearer {token_produtor}"},
        )
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["status"] == "rascunho"
        assert data["score_completude"] == 0.0

    async def test_criar_processo_sem_autenticacao_retorna_401(self, client):
        response = await client.post("/api/v1/processos", json={"imovel_id": "uuid"})
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "CAR-001"

    async def test_submeter_processo_com_docs_validos(
        self, client, token_produtor, processo_com_docs_validos
    ):
        response = await client.post(
            f"/api/v1/processos/{processo_com_docs_validos.id}/submeter",
            headers={
                "Authorization": f"Bearer {token_produtor}",
                "Idempotency-Key": "test-key-001",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "submetido"

    async def test_submeter_processo_incompleto_retorna_422(
        self, client, token_produtor, processo_rascunho
    ):
        response = await client.post(
            f"/api/v1/processos/{processo_rascunho.id}/submeter",
            headers={"Authorization": f"Bearer {token_produtor}"},
        )
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "CAR-060"

    async def test_produtor_nao_ve_processo_de_outro_retorna_404(
        self, client, token_produtor, processo_outro_usuario
    ):
        response = await client.get(
            f"/api/v1/processos/{processo_outro_usuario.id}",
            headers={"Authorization": f"Bearer {token_produtor}"},
        )
        # 404, não 403 — segurança por obscuridade
        assert response.status_code == 404

    async def test_paginacao_cursor_based(self, client, token_analista, multiplos_processos):
        # Primeira página
        r1 = await client.get(
            "/api/v1/analista/processos?page_size=5",
            headers={"Authorization": f"Bearer {token_analista}"},
        )
        assert r1.status_code == 200
        meta1 = r1.json()["meta"]
        assert len(r1.json()["data"]) == 5
        assert meta1["has_more"] is True

        # Segunda página com cursor
        r2 = await client.get(
            f"/api/v1/analista/processos?page_size=5&cursor={meta1['cursor_next']}",
            headers={"Authorization": f"Bearer {token_analista}"},
        )
        assert r2.status_code == 200
        # Sem sobreposição de itens
        ids1 = {p["id"] for p in r1.json()["data"]}
        ids2 = {p["id"] for p in r2.json()["data"]}
        assert ids1.isdisjoint(ids2)
```

### Testes Geoespaciais

```python
# tests/integration/test_geometria.py
class TestValidacaoGeometria:
    async def test_geometria_valida_aceita(self, client, token_produtor, imovel_sem_geometria):
        geojson_valido = {
            "type": "MultiPolygon",
            "coordinates": [[[[-44.0, -5.0], [-43.0, -5.0], [-43.0, -4.0], [-44.0, -4.0], [-44.0, -5.0]]]]
        }
        response = await client.post(
            f"/api/v1/imoveis/{imovel_sem_geometria.id}/validar-geometria",
            json={"geometria_geojson": geojson_valido},
            headers={"Authorization": f"Bearer {token_produtor}"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["valida"] is True

    async def test_geometria_auto_interseccao_rejeitada(self, client, token_produtor, imovel_sem_geometria):
        geojson_invalido = {
            "type": "MultiPolygon",
            "coordinates": [[[[0, 0], [1, 1], [0, 1], [1, 0], [0, 0]]]]  # borboleta
        }
        response = await client.post(
            f"/api/v1/imoveis/{imovel_sem_geometria.id}/validar-geometria",
            json={"geometria_geojson": geojson_invalido},
            headers={"Authorization": f"Bearer {token_produtor}"},
        )
        assert response.status_code == 200
        assert response.json()["data"]["valida"] is False
        assert "auto-intersecção" in response.json()["data"]["erros"][0].lower()
```

---

## 4. Testes de Contrato (Pact)

```python
# tests/contract/test_documento_consumer.py
# O Process Service (consumer) espera este contrato do Document Service (provider)
import pytest
from pact import Consumer, Provider

@pytest.fixture(scope="module")
def pact():
    pact = Consumer("process-service").has_pact_with(
        Provider("document-service"),
        pact_dir="./pacts",
        publish_verification_results=True,
    )
    pact.start_service()
    yield pact
    pact.stop_service()

def test_consultar_status_documento(pact):
    expected = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "status": "valido",
        "dados_extraidos": {
            "numero_matricula": "123456",
            "area_ha": 150.0
        }
    }
    (
        pact.given("documento 550e8400 existe e está válido")
        .upon_receiving("uma consulta de status de documento")
        .with_request("GET", "/api/v1/documentos/550e8400-e29b-41d4-a716-446655440000/status")
        .will_respond_with(200, body={"data": expected})
    )
    with pact:
        from carla.modules.integracoes.adapters.documento_client import DocumentoClient
        client = DocumentoClient(base_url=pact.uri)
        resultado = client.consultar_status("550e8400-e29b-41d4-a716-446655440000")
        assert resultado["status"] == "valido"
```

---

## 5. Testes E2E (Playwright)

```typescript
// tests/e2e/fluxo-registro-car.spec.ts
import { test, expect, Page } from '@playwright/test';

test.describe('Fluxo completo de registro CAR', () => {
  test.beforeEach(async ({ page }) => {
    // Login mock
    await page.goto('/login');
    await page.fill('[data-testid="cpf-input"]', '529.982.247-25');
    await page.fill('[data-testid="nome-input"]', 'João Silva');
    await page.click('[data-testid="btn-login"]');
    await expect(page).toHaveURL('/dashboard');
  });

  test('cidadão completa registro CAR em happy path', async ({ page }) => {
    // Iniciar novo processo
    await page.click('[data-testid="btn-novo-processo"]');
    await page.fill('[data-testid="nome-imovel"]', 'Fazenda Boa Vista');
    await page.selectOption('[data-testid="estado-select"]', 'MA');
    await page.selectOption('[data-testid="municipio-select"]', 'São Luís');
    await page.fill('[data-testid="area-total"]', '50');
    await page.click('[data-testid="btn-proximo"]');

    // Upload de matrícula
    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser'),
      page.click('[data-testid="upload-matricula"]'),
    ]);
    await fileChooser.setFiles('./tests/fixtures/sample_matricula.pdf');

    // Aguardar validação (polling até 60s)
    await expect(page.locator('[data-testid="status-matricula"]'))
      .toHaveText('Válido', { timeout: 60000 });

    // Submeter processo
    await page.click('[data-testid="btn-submeter"]');
    await expect(page.locator('[data-testid="status-processo"]'))
      .toHaveText('Submetido');
    await expect(page.locator('[data-testid="numero-protocolo"]'))
      .not.toBeEmpty();
  });

  test('assistente IA responde pergunta sobre CAR', async ({ page }) => {
    await page.click('[data-testid="btn-assistente"]');
    await page.fill('[data-testid="chat-input"]', 'O que é reserva legal?');
    await page.click('[data-testid="btn-enviar"]');

    // Aguardar resposta (streaming)
    await expect(page.locator('[data-testid="ultima-resposta"]'))
      .toContainText('reserva legal', { timeout: 30000 });
    await expect(page.locator('[data-testid="ultima-resposta"]'))
      .toContainText('12.651', { timeout: 30000 });
  });

  test('analista aprova processo', async ({ page, browser }) => {
    // Segundo contexto para o analista
    const contextoAnalista = await browser.newContext();
    const pageAnalista = await contextoAnalista.newPage();

    await pageAnalista.goto('/login');
    await pageAnalista.fill('[data-testid="cpf-input"]', '111.111.111-11');
    await pageAnalista.selectOption('[data-testid="role-select"]', 'analista');
    await pageAnalista.click('[data-testid="btn-login"]');

    await pageAnalista.click('[data-testid="menu-analista"]');
    await pageAnalista.click('[data-testid="primeiro-processo"]');
    await pageAnalista.click('[data-testid="btn-assumir"]');
    await pageAnalista.click('[data-testid="btn-aprovar"]');
    await pageAnalista.click('[data-testid="btn-confirmar-aprovacao"]');

    await expect(pageAnalista.locator('[data-testid="status-processo"]'))
      .toHaveText('Aprovado');

    await contextoAnalista.close();
  });
});
```

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false,          // E2E sequencial para evitar conflitos de dados
  retries: 1,
  timeout: 120000,
  use: {
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  ],
  reporter: [['html', { outputFolder: 'playwright-report' }]],
});
```

---

## 6. Testes de Carga (k6)

```javascript
// tests/load/normal_load.js
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up para 50 usuários
    { duration: '5m', target: 50 },   // Sustain
    { duration: '2m', target: 100 },  // Pico
    { duration: '5m', target: 100 },  // Sustain no pico
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(50)<200', 'p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],    // < 1% de erros
    errors: ['rate<0.05'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export function setup() {
  // Autenticar e obter token
  const loginRes = http.post(`${BASE_URL}/api/v1/auth/mock-login`, JSON.stringify({
    cpf: '52998224725', nome: 'Load Test User'
  }), { headers: { 'Content-Type': 'application/json' } });
  return { token: loginRes.json('data.access_token') };
}

export default function(data) {
  const headers = {
    'Authorization': `Bearer ${data.token}`,
    'Content-Type': 'application/json',
  };

  group('dashboard do cidadão', () => {
    const r = http.get(`${BASE_URL}/api/v1/processos`, { headers });
    check(r, { 'status 200': (r) => r.status === 200 }) || errorRate.add(1);
    sleep(1);
  });

  group('conversa com assistente', () => {
    // Criar conversa
    const criarR = http.post(`${BASE_URL}/api/v1/assistente/conversas`,
      JSON.stringify({}), { headers });
    if (criarR.status !== 201) { errorRate.add(1); return; }
    const conversaId = criarR.json('data.id');

    // Enviar mensagem (sem SSE para load test — usar endpoint síncrono)
    const msgR = http.post(
      `${BASE_URL}/api/v1/assistente/conversas/${conversaId}/mensagens/sync`,
      JSON.stringify({ conteudo: 'O que é CAR?' }),
      { headers, timeout: '30s' }
    );
    check(msgR, { 'resposta recebida': (r) => r.status === 200 }) || errorRate.add(1);
    sleep(2);
  });
}
```

### Thresholds de Aceitação por Endpoint

| Endpoint | p50 | p95 | p99 | Max Erros |
|---|---|---|---|---|
| GET /api/v1/processos | 100ms | 300ms | 500ms | 0.1% |
| POST /api/v1/processos | 200ms | 500ms | 1000ms | 0.1% |
| POST /api/v1/processos/{id}/submeter | 300ms | 800ms | 1500ms | 0.1% |
| POST /api/v1/documentos/upload | 500ms | 2000ms | 5000ms | 1% |
| POST /api/v1/assistente/mensagens | 2000ms | 5000ms | 10000ms | 2% |
| GET /api/v1/analista/processos | 150ms | 400ms | 800ms | 0.1% |

---

## 7. Testes de Segurança

```bash
# SAST — executar no CI em cada PR
bandit -r src/ -ll -i --format json > bandit-report.json

# Dependency scan
safety check --json --output safety-report.json

# Container scan
trivy image carla-backend:latest --format json --exit-code 1 --severity HIGH,CRITICAL

# Secret detection (pre-commit + CI)
gitleaks detect --source . --report-format json --report-path gitleaks-report.json

# DAST (apenas staging)
docker run -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t https://staging-api.carcopilot.gov.br \
  -J zap-report.json \
  -I  # Ignorar alertas INFO
```

### Testes de Autorização

```python
# tests/integration/test_autorizacao.py
class TestMatrizDeAutorizacao:
    @pytest.mark.parametrize("rota,metodo,token_fixture,status_esperado", [
        # Produtor não acessa rota de analista
        ("/api/v1/analista/processos", "GET", "token_produtor", 403),
        # Analista não acessa rota de admin
        ("/api/v1/admin/usuarios", "GET", "token_analista", 403),
        # Sem token → 401
        ("/api/v1/processos", "GET", None, 401),
        # Analista acessa dashboard
        ("/api/v1/analista/processos", "GET", "token_analista", 200),
    ])
    async def test_controle_de_acesso(
        self, client, rota, metodo, token_fixture, status_esperado, request
    ):
        token = request.getfixturevalue(token_fixture) if token_fixture else None
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = await getattr(client, metodo.lower())(rota, headers=headers)
        assert response.status_code == status_esperado

    async def test_processo_de_outro_usuario_retorna_404_nao_403(
        self, client, token_produtor_a, processo_produtor_b
    ):
        response = await client.get(
            f"/api/v1/processos/{processo_produtor_b.id}",
            headers={"Authorization": f"Bearer {token_produtor_a}"},
        )
        assert response.status_code == 404  # segurança por obscuridade

    async def test_token_expirado_retorna_401(self, client, token_expirado):
        response = await client.get(
            "/api/v1/processos",
            headers={"Authorization": f"Bearer {token_expirado}"},
        )
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "CAR-001"

    async def test_token_na_blacklist_retorna_401(self, client, token_revogado):
        response = await client.get(
            "/api/v1/processos",
            headers={"Authorization": f"Bearer {token_revogado}"},
        )
        assert response.status_code == 401
```

---

## 8. Pipeline CI/CD de Testes

```yaml
# .github/workflows/ci.yml (trecho de testes)
jobs:
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv run ruff check src/
      - run: uv run mypy src/

  unit-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv run pytest tests/unit/ -x --tb=short

  integration-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    services:
      docker:
        image: docker:dind
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv run pytest tests/integration/ -x --tb=short

  security-scan:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv run bandit -r src/ -ll -i
      - run: uv run safety check
      - uses: gitleaks/gitleaks-action@v2
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          exit-code: 1
          severity: HIGH,CRITICAL

  e2e-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    if: github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/compose-action@v1
        with:
          compose-file: docker-compose.test.yml
          up-flags: --wait
      - run: npx playwright install chromium
      - run: npx playwright test --project=chromium
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

### Quality Gates

| Gate | Condição de Bloqueio |
|---|---|
| Cobertura de testes | < 80% de cobertura global |
| SAST (bandit) | Qualquer finding HIGH ou CRITICAL |
| Dependency scan | CVE CRITICAL em dependência |
| Secret detection | Qualquer segredo detectado no código |
| Testes unitários | Qualquer falha |
| Testes de integração | Qualquer falha |
| Contrato (Pact) | Breaking change detectado |
| p95 de latência (load test) | > 1000ms em qualquer endpoint crítico |
