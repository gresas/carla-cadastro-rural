---
sidebar_position: 2
title: Testes Unitários
description: pytest — exemplos de testes de domínio para entidades, value objects e serviços.
tags: [engenharia, testes, pytest, domínio]
---

# Testes Unitários

:::info Para quem é esta página
Engenheiros back-end. Filosofia de testes: [Estratégia](./estrategia.md).
:::

## Testando Value Objects

```python
# tests/unit/processos/domain/test_value_objects.py
import pytest
from carla.modules.processos.domain.value_objects import NumeroCAR, CPF, ÁreaTotalHectares

class TestNumeroCAR:
    def test_formato_valido_aceito(self):
        numero = NumeroCAR(valor="MA-0001234-20240115123456")
        assert numero.estado == "MA"

    @pytest.mark.parametrize("invalido", [
        "MA-123-456",            # sequencial curto
        "ma-0001234-20240115123456",  # UF minúscula
        "",
    ])
    def test_formato_invalido_rejeita(self, invalido):
        with pytest.raises(ValueError, match="inválido"):
            NumeroCAR(valor=invalido)

    def test_igualdade_por_valor(self):
        a = NumeroCAR(valor="MA-0001234-20240115123456")
        b = NumeroCAR(valor="MA-0001234-20240115123456")
        assert a == b


class TestCPF:
    def test_cpf_valido_aceito(self):
        cpf = CPF(valor="529.982.247-25")
        assert cpf.valor == "52998224725"

    def test_todos_digitos_iguais_rejeitado(self):
        with pytest.raises(ValueError, match="todos os dígitos iguais"):
            CPF(valor="111.111.111-11")

    def test_mascarado_protege_cpf(self):
        cpf = CPF(valor="52998224725")
        assert cpf.mascarado == "***.***.247-**"
```

## Testando Invariantes do Agregado

```python
# tests/unit/processos/domain/test_entities.py
from uuid import uuid4
from carla.modules.processos.domain.entities import ProcessoCAR
from carla.modules.processos.domain.events import ProcessoSubmetido
from carla.modules.processos.domain.exceptions import (
    EstadoInvalidoError, DocumentacaoInsuficienteError, PermissionDeniedError
)

class TestProcessoCAR:
    def test_submeter_completo_muda_status(self, processo_completo):
        rid = processo_completo.requerente_id
        processo_completo.submeter(rid)
        assert processo_completo.status.value == "submetido"

    def test_submeter_emite_evento(self, processo_completo):
        rid = processo_completo.requerente_id
        processo_completo.submeter(rid)
        assert any(isinstance(e, ProcessoSubmetido) for e in processo_completo.domain_events)

    def test_submeter_por_outro_usuario_falha(self, processo_completo):
        with pytest.raises(PermissionDeniedError):
            processo_completo.submeter(uuid4())  # ID diferente

    def test_submeter_sem_matricula_falha(self, processo_sem_matricula):
        rid = processo_sem_matricula.requerente_id
        with pytest.raises(DocumentacaoInsuficienteError):
            processo_sem_matricula.submeter(rid)

    def test_resubmeter_processo_falha(self, processo_completo):
        rid = processo_completo.requerente_id
        processo_completo.submeter(rid)
        with pytest.raises(EstadoInvalidoError):
            processo_completo.submeter(rid)  # já está submetido
```

## Testando Serviços de Domínio

```python
class TestCalculadorAreaReservaLegal:
    @pytest.fixture
    def calc(self):
        return CalculadorAreaReservaLegal()

    def test_amazonia_exige_80_porcento(self, calc):
        area = ÁreaTotalHectares(valor=100.0)
        minima = calc.calcular_area_minima(area, "amazonia_legal")
        assert minima.valor == 80.0

    def test_mata_atlantica_exige_20_porcento(self, calc):
        area = ÁreaTotalHectares(valor=50.0)
        minima = calc.calcular_area_minima(area, "mata_atlantica")
        assert minima.valor == 10.0

    def test_bioma_desconhecido_lanca_erro(self, calc):
        with pytest.raises(ValueError, match="Bioma desconhecido"):
            calc.calcular_area_minima(ÁreaTotalHectares(valor=100.0), "bioma_xyz")
```

:::tip Fixtures para agregados complexos
Crie `conftest.py` com fixtures que retornam agregados em estados específicos:
```python
@pytest.fixture
def processo_completo():
    return ProcessoCAR(
        id=uuid4(), status=StatusProcesso.EM_PREENCHIMENTO,
        requerente_id=(rid := uuid4()),
        documentos=[
            make_documento("matricula_imovel", "valido"),
            make_documento("ccir", "valido"),
        ],
        imovel_geometria_definida=True,
    )
```
:::
