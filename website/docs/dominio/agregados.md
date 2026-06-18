---
sidebar_position: 4
title: Agregados e Value Objects
description: Entidades de domínio, value objects e invariantes com exemplos em Python.
tags: [engenharia, ddd, agregados, python]
---

# Agregados e Value Objects

:::info Para quem é esta página
Engenheiros back-end. Contexto de design: [Bounded Contexts](./bounded-contexts.md).
:::

## Agregado Principal: ProcessoCAR

O `ProcessoCAR` é a **raiz do agregado** do Core Domain. Ele garante todas as invariantes de negócio do processo.

### Invariantes (regras que o agregado garante)

1. Processo não pode ser submetido sem matrícula do imóvel válida
2. Status só avança seguindo a máquina de estados definida
3. Apenas o requerente (ou RT autorizado) pode submeter o processo
4. Apenas o analista responsável pode aprovar, aprovar com PRA ou rejeitar
5. Aprovação exige zero pendências abertas
6. **Número de protocolo é gerado na submissão** — não na aprovação. O analista não cria o número CAR; ele analisa um cadastro que já possui número. A aprovação resulta na emissão do Certificado CAR.

### Estrutura

```python
@dataclass
class ProcessoCAR:
    id: UUID
    numero_protocolo: Optional[str]     # Gerado pelo SICAR na submissão (formato UF-NNNNNNN-...)
    numero_car_sicar: Optional[str]     # Confirmado pelo SICAR após análise concluída (pode ser o mesmo)
    status: StatusProcesso
    requerente_id: UUID
    imovel_id: UUID
    analista_id: Optional[UUID]
    documentos: List[Documento]
    pendencias: List[Pendência]
    historico: List[HistóricoStatus]
    score_completude: float             # 0.0 – 100.0
    score_risco: float                  # 0.0 – 10.0
    _domain_events: List = field(default_factory=list)

    def submeter(self, requerente_id: UUID) -> None:
        if requerente_id != self.requerente_id:
            raise PermissionDeniedError("Apenas o requerente pode submeter")
        if self.status not in (StatusProcesso.RASCUNHO, StatusProcesso.EM_PREENCHIMENTO):
            raise EstadoInvalidoError(f"Processo em {self.status} não pode ser submetido")
        if not self._tem_documentacao_minima():
            raise DocumentacaoInsuficienteError(self._documentos_faltantes())
        self.status = StatusProcesso.SUBMETIDO
        self._emit(ProcessoSubmetido(processo_id=self.id, ...))
```

---

## Value Objects Principais

Value Objects são **imutáveis** e têm **igualdade por valor**, não por identidade.

### NumeroCAR

```python
class NumeroCAR(BaseModel):
    """Formato oficial SICAR: UF-NNNNNNN-NNNNNNNNNNNNNN"""
    valor: str

    @field_validator('valor')
    @classmethod
    def validar_formato(cls, v: str) -> str:
        import re
        if not re.match(r'^[A-Z]{2}-\d{7}-\d{14}$', v):
            raise ValueError(f'Número CAR inválido: "{v}"')
        return v

    @property
    def estado(self) -> str:
        return self.valor[:2]
```

### CPF (com validação de dígitos verificadores)

```python
class CPF(BaseModel):
    valor: str  # 11 dígitos, sem formatação

    @field_validator('valor')
    @classmethod
    def validar_cpf(cls, v: str) -> str:
        v = re.sub(r'\D', '', v)
        if len(v) != 11 or len(set(v)) == 1:
            raise ValueError('CPF inválido')
        for i in range(9, 11):
            soma = sum(int(v[j]) * (i + 1 - j) for j in range(i))
            if (soma * 10 % 11) % 10 != int(v[i]):
                raise ValueError('CPF inválido — dígitos verificadores incorretos')
        return v

    @property
    def mascarado(self) -> str:
        return f'***.***.{self.valor[6:9]}-**'
```

### ÁreaTotalHectares

```python
class ÁreaTotalHectares(BaseModel):
    valor: float

    @field_validator('valor')
    @classmethod
    def validar(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Área deve ser maior que zero')
        if v > 10_000_000:
            raise ValueError('Área implausível — verifique a unidade')
        return round(v, 4)

    def em_modulos_fiscais(self, modulo_ha: float) -> float:
        return round(self.valor / modulo_ha, 2)
```

---

## Interface do Repositório

```python
class ProcessoCARRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[ProcessoCAR]: ...

    @abstractmethod
    async def find_pending_analysis(self, limit: int = 50) -> List[ProcessoCAR]: ...

    @abstractmethod
    async def save(self, processo: ProcessoCAR) -> ProcessoCAR: ...

    @abstractmethod
    async def find_by_geometria_intersects(
        self, geometria_wkt: str, srid: int = 4674
    ) -> List[ProcessoCAR]: ...
```

:::note Sem dependência de SQLAlchemy no domínio
O domínio define **interfaces** (`ABC`). A implementação concreta com SQLAlchemy fica na camada de infraestrutura. Isso permite testar o domínio sem banco de dados.
:::

## Ver também

- [Banco de Dados](../arquitetura/banco-de-dados.md) — mapeamento ORM dos agregados
- [Testes Unitários](../testes/unitarios.md) — como testar invariantes do domínio
