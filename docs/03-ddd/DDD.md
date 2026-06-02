# CARla — Domain-Driven Design

**Versão:** 1.0.0  
**Data:** 2026-06-01

---

## 1. Visão Estratégica

### 1.1 Mapa de Contextos (Context Map)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CAR COPILOT — Context Map                     │
└─────────────────────────────────────────────────────────────────────┘

  ┌──────────────────┐   Partnership   ┌──────────────────────────┐
  │                  │◄───────────────►│                          │
  │  Identidade e    │                 │   Gestão de Processos    │
  │  Acesso (IAM)    │  Conformist     │   CAR  [CORE DOMAIN]     │
  │                  │────────────────►│                          │
  └──────────────────┘                 └──────────┬───────────────┘
                                                   │
                        Customer-Supplier          │ Customer-Supplier
                             ┌─────────────────────┤
                             │                     │
                ┌────────────▼──────┐   ┌──────────▼─────────────┐
                │                   │   │                         │
                │   Validação       │   │   Assistência           │
                │   Documental      │   │   Inteligente           │
                │   [SUPPORTING]    │   │   [SUPPORTING]          │
                │                   │   │                         │
                └───────────────────┘   └──────────┬─────────────┘
                                                    │  ACL
                                                    ▼
                                        ┌───────────────────────┐
                                        │  [EXT] LLM Providers  │
                                        │  OpenAI/Claude/Ollama  │
                                        └───────────────────────┘

  ┌───────────────────────────┐   Open Host Service
  │  Integrações Externas     │◄────────────────────── todos os BCs
  │  [GENERIC SUBDOMAIN]      │
  │                           │   ACL por sistema:
  │  SICAR / SIGEF / IBAMA    │   ┌──────────────────┐
  │  MapBiomas / PRODES       │──►│  Anti-Corruption │
  └───────────────────────────┘   │  Layer           │
                                  └──────────────────┘

  ┌───────────────────────────┐   Customer-Supplier
  │  Analytics e Reporting    │◄────────────────── BC Processos
  │  [GENERIC SUBDOMAIN]      │
  └───────────────────────────┘
```

**Tipos de relação:**
- **Partnership:** IAM e Processos evoluem juntos; mudanças coordenadas
- **Customer-Supplier:** Processos é cliente de Validação e Assistente (define o contrato)
- **Conformist:** IAM segue o modelo Gov.br sem questionar
- **Anti-Corruption Layer (ACL):** Assistente protege o domínio dos LLMs externos; Integrações protege dos sistemas externos
- **Open Host Service:** BC de Integrações expõe serviço padronizado para todos

---

### 1.2 Linguagem Ubíqua (Ubiquitous Language)

| Termo | Definição no Domínio |
|---|---|
| **CAR** | Registro eletrônico obrigatório de imóvel rural com dados geoespaciais e ambientais |
| **Processo CAR** | Fluxo de trabalho completo desde abertura até aprovação/rejeição do registro |
| **Imóvel Rural** | Entidade geoespacial representando a propriedade a ser registrada, com geometria |
| **Requerente** | Pessoa (produtor/consultor) que solicita o registro CAR |
| **Proprietário** | Titular legal do imóvel, identificado pelo CPF/CNPJ da matrícula |
| **Analista** | Servidor público que avalia e decide sobre o processo |
| **Pendência** | Inconsistência ou documentação faltante que impede aprovação |
| **Submissão** | Ato de enviar o processo para análise; gerador do número de protocolo |
| **Protocolo** | Número temporário gerado na submissão, antes do número CAR oficial |
| **Número CAR** | Identificador único oficial do registro. Formato: UF-NNNNNNN-NNNNNNNNNNNNNN |
| **Completude** | Score 0-100 indicando percentual de preenchimento do processo |
| **Score de Risco** | Pontuação de risco ambiental baseada em dados externos (DETER, IBAMA) |
| **Geometria** | Representação geoespacial (polígono/multipolígono) do imóvel em SIRGAS 2000 |
| **Dossiê** | Documento PDF compilado automaticamente com todos os dados do processo |
| **Validação Documental** | Processo de OCR, extração e verificação de consistência dos documentos |
| **Cruzamento de Dados** | Comparação de informações entre documentos e com bases externas |
| **Intenção** | Classificação da mensagem do usuário no assistente (dúvida, consulta, solicitação) |
| **Conversa** | Sessão de chat com o assistente inteligente, com contexto preservado |
| **Base de Conhecimento** | Conjunto de documentos normativos indexados para o RAG do assistente |
| **Embedding** | Representação vetorial de texto para busca semântica no RAG |
| **Bioma** | Região geográfica com características ecológicas (define % de Reserva Legal) |
| **APP** | Área de Preservação Permanente — faixa de vegetação obrigatoriamente preservada |
| **Reserva Legal** | Percentual mínimo de vegetação nativa que deve ser preservado por bioma |
| **Módulo Fiscal** | Unidade de medida agrária municipal (define categoria do imóvel) |
| **Embargo** | Restrição legal ao uso do imóvel por infração ambiental (IBAMA) |

---

## 2. BC: Gestão de Processos CAR — Core Domain

### 2.1 Máquina de Estados do ProcessoCAR

```
                    [rascunho]
                        │ SubmeterProcesso (completo)
                        ▼
                   [submetido]
                        │ AssumirProcesso (analista)
                        ▼
                  [em_analise]
                  │         │
    (pendências)  │         │ (sem pendências)
                  ▼         ▼
             [pendente]  [aprovado] ──────┐
                  │                       │
    CorrigirDados │                       │ (concluído)
                  ▼                       ▼
           [em_correcao]            [cancelado]
                  │
    (correção OK) │
                  ▼
             [em_analise]  ← ou [rejeitado]
                                      │
                         RecursoInterposto │
                                      ▼
                                  [recurso]
                                      │
                            ├── AcatarRecurso → [em_analise]
                            └── NegarRecurso  → [rejeitado definitivo]
```

### 2.2 Agregado: ProcessoCAR

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

class StatusProcesso(str, Enum):
    RASCUNHO = "rascunho"
    EM_PREENCHIMENTO = "em_preenchimento"
    AGUARDANDO_DOCUMENTOS = "aguardando_documentos"
    SUBMETIDO = "submetido"
    EM_ANALISE = "em_analise"
    PENDENTE = "pendente"
    EM_CORRECAO = "em_correcao"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"
    RECURSO = "recurso"
    CANCELADO = "cancelado"

class PrioridadeProcesso(str, Enum):
    BAIXA = "baixa"
    NORMAL = "normal"
    ALTA = "alta"
    URGENTE = "urgente"

@dataclass
class ProcessoCAR:
    id: UUID
    numero_car: Optional[str]          # None até aprovação
    status: StatusProcesso
    etapa: int                         # 1-10
    prioridade: PrioridadeProcesso
    requerente_id: UUID
    imovel_id: UUID
    analista_id: Optional[UUID]
    data_submissao: Optional[datetime]
    data_conclusao: Optional[datetime]
    score_completude: float            # 0.0 - 100.0
    score_risco: float                 # 0.0 - 10.0
    documentos: List['Documento']
    pendencias: List['Pendência']
    historico: List['HistóricoStatus']
    _domain_events: List = field(default_factory=list, repr=False)

    # === Invariantes do Agregado ===

    def submeter(self, requerente_id: UUID) -> None:
        """Invariante: só pode submeter se documentação mínima presente."""
        if requerente_id != self.requerente_id:
            raise PermissionDeniedError("Apenas o requerente pode submeter")
        if self.status not in (StatusProcesso.RASCUNHO, StatusProcesso.EM_PREENCHIMENTO):
            raise EstadoInvalidoError(f"Processo em {self.status} não pode ser submetido")
        if not self._tem_documentacao_minima():
            raise DocumentacaoInsuficienteError(self._documentos_faltantes())
        if self.imovel_geometria_definida is False:
            raise GeometriaFaltanteError("Geometria do imóvel é obrigatória")

        self.status = StatusProcesso.SUBMETIDO
        self.data_submissao = datetime.utcnow()
        self._emit(ProcessoSubmetido(
            processo_id=self.id,
            requerente_id=self.requerente_id,
            occurred_at=self.data_submissao
        ))

    def aprovar(self, analista_id: UUID, observacoes: Optional[str] = None) -> None:
        """Invariante: apenas o analista responsável pode aprovar."""
        if analista_id != self.analista_id:
            raise PermissionDeniedError("Apenas o analista responsável pode aprovar")
        if self.status != StatusProcesso.EM_ANALISE:
            raise EstadoInvalidoError("Apenas processos em análise podem ser aprovados")
        if self._tem_pendencias_abertas():
            raise PendênciasAbertasError("Resolva todas as pendências antes de aprovar")

        self.status = StatusProcesso.APROVADO
        self.data_conclusao = datetime.utcnow()
        self._emit(ProcessoAprovado(processo_id=self.id, analista_id=analista_id))

    def criar_pendencia(self, tipo: str, titulo: str, descricao: str,
                        analista_id: UUID, prazo=None) -> 'Pendência':
        """Invariante: pendência só pode ser criada em processos em análise."""
        if self.status not in (StatusProcesso.EM_ANALISE, StatusProcesso.SUBMETIDO):
            raise EstadoInvalidoError("Pendências só podem ser criadas durante análise")

        pendencia = Pendência(
            id=uuid4(), processo_id=self.id, tipo=tipo,
            titulo=titulo, descricao=descricao, prazo=prazo
        )
        self.pendencias.append(pendencia)
        self.status = StatusProcesso.PENDENTE
        self._emit(PendênciaIdentificada(processo_id=self.id, pendencia_id=pendencia.id))
        return pendencia

    def _tem_documentacao_minima(self) -> bool:
        tipos_obrigatorios = {"matricula_imovel", "ccir"}
        tipos_presentes = {d.tipo for d in self.documentos if d.status == "valido"}
        return tipos_obrigatorios.issubset(tipos_presentes)

    def _tem_pendencias_abertas(self) -> bool:
        return any(p.status == "aberta" for p in self.pendencias)

    def _emit(self, event) -> None:
        self._domain_events.append(event)

    @property
    def domain_events(self) -> List:
        return list(self._domain_events)

    def clear_events(self) -> None:
        self._domain_events.clear()
```

### 2.3 Entidade: Documento

```python
class TipoDocumento(str, Enum):
    MATRICULA_IMOVEL = "matricula_imovel"
    CCIR = "ccir"
    PLANTA_GEOREFERENCIADA = "planta_georeferenciada"
    MEMORIAL_DESCRITIVO = "memorial_descritivo"
    CAR_ANTERIOR = "car_anterior"
    DECLARACAO_AREA = "declaracao_area"
    OUTROS = "outros"

class StatusDocumento(str, Enum):
    AGUARDANDO = "aguardando"
    PROCESSANDO = "processando"
    VALIDO = "valido"
    INVALIDO = "invalido"
    REJEITADO = "rejeitado"

@dataclass
class Documento:
    id: UUID
    processo_id: UUID
    tipo: TipoDocumento
    nome_arquivo: str
    tamanho_bytes: int
    hash_sha256: str
    storage_path: str
    status: StatusDocumento
    dados_ocr: Optional[dict]
    dados_extraidos: Optional[dict]
    erros_validacao: Optional[List[dict]]
    tentativas_ocr: int = 0

    def marcar_valido(self, dados_extraidos: dict) -> None:
        self.status = StatusDocumento.VALIDO
        self.dados_extraidos = dados_extraidos

    def marcar_invalido(self, erros: List[dict]) -> None:
        self.status = StatusDocumento.INVALIDO
        self.erros_validacao = erros
```

### 2.4 Entidade: Pendência

```python
class TipoPendência(str, Enum):
    DOCUMENTACAO_FALTANTE = "documentacao_faltante"
    DOCUMENTO_INVALIDO = "documento_invalido"
    GEOMETRIA_INCONSISTENTE = "geometria_inconsistente"
    DADO_CONFLITANTE = "dado_conflitante"
    AREA_DIVERGENTE = "area_divergente"
    OUTRO = "outro"

class StatusPendência(str, Enum):
    ABERTA = "aberta"
    EM_CORRECAO = "em_correcao"
    RESOLVIDA = "resolvida"
    CANCELADA = "cancelada"

@dataclass
class Pendência:
    id: UUID
    processo_id: UUID
    tipo: TipoPendência
    titulo: str
    descricao: str
    status: StatusPendência = StatusPendência.ABERTA
    prazo: Optional[datetime] = None
    resolvida_em: Optional[datetime] = None

    def resolver(self, descricao_resolucao: str) -> None:
        if self.status == StatusPendência.RESOLVIDA:
            raise EstadoInvalidoError("Pendência já resolvida")
        self.status = StatusPendência.RESOLVIDA
        self.resolvida_em = datetime.utcnow()
```

### 2.5 Value Objects do BC Processos

```python
from pydantic import BaseModel, field_validator
import re

class NumeroCAR(BaseModel):
    """Formato oficial SICAR: UF-NNNNNNN-NNNNNNNNNNNNNN"""
    valor: str

    @field_validator('valor')
    @classmethod
    def validar_formato(cls, v: str) -> str:
        # Formato: 2 letras UF + hífen + 7 dígitos + hífen + 14 dígitos
        pattern = r'^[A-Z]{2}-\d{7}-\d{14}$'
        if not re.match(pattern, v):
            raise ValueError(
                f'Número CAR inválido: "{v}". '
                f'Formato esperado: UF-NNNNNNN-NNNNNNNNNNNNNN '
                f'(ex: MA-0001234-20240115123456)'
            )
        return v

    @property
    def estado(self) -> str:
        return self.valor[:2]

    @property
    def sequencial(self) -> str:
        return self.valor[3:10]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NumeroCAR):
            return False
        return self.valor == other.valor

    def __hash__(self) -> int:
        return hash(self.valor)


class ÁreaTotalHectares(BaseModel):
    """Área em hectares com 4 casas decimais de precisão."""
    valor: float

    @field_validator('valor')
    @classmethod
    def deve_ser_positivo(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Área deve ser maior que zero')
        if v > 10_000_000:  # 10 milhões de hectares — maior fazenda do Brasil tem ~4M ha
            raise ValueError('Área implausível — verifique a unidade (hectares)')
        return round(v, 4)

    def em_modulos_fiscais(self, modulo_fiscal_ha: float) -> float:
        return round(self.valor / modulo_fiscal_ha, 2)


class MunicípioIBGE(BaseModel):
    """Município identificado pelo código IBGE de 7 dígitos."""
    codigo: str
    nome: str
    estado: str

    @field_validator('codigo')
    @classmethod
    def validar_codigo(cls, v: str) -> str:
        if not re.match(r'^\d{7}$', v):
            raise ValueError('Código IBGE deve ter exatamente 7 dígitos numéricos')
        return v

    @field_validator('estado')
    @classmethod
    def validar_estado(cls, v: str) -> str:
        ufs_validas = {
            'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA',
            'MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN',
            'RS','RO','RR','SC','SP','SE','TO'
        }
        v = v.upper()
        if v not in ufs_validas:
            raise ValueError(f'UF inválida: {v}')
        return v


class CPF(BaseModel):
    """CPF validado com dígitos verificadores."""
    valor: str  # apenas dígitos, 11 chars

    @field_validator('valor')
    @classmethod
    def validar_cpf(cls, v: str) -> str:
        v = re.sub(r'\D', '', v)
        if len(v) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        if len(set(v)) == 1:
            raise ValueError('CPF com todos os dígitos iguais é inválido')
        # Validação dos dígitos verificadores
        for i in range(9, 11):
            soma = sum(int(v[j]) * (i + 1 - j) for j in range(i))
            digito = (soma * 10 % 11) % 10
            if digito != int(v[i]):
                raise ValueError('CPF inválido — dígitos verificadores incorretos')
        return v

    @property
    def formatado(self) -> str:
        return f'{self.valor[:3]}.{self.valor[3:6]}.{self.valor[6:9]}-{self.valor[9:]}'

    @property
    def mascarado(self) -> str:
        return f'***.***.{self.valor[6:9]}-**'


class Geometria(BaseModel):
    """Geometria geoespacial em WKT com SRID 4674 (SIRGAS 2000)."""
    wkt: str
    srid: int = 4674  # SIRGAS 2000 — padrão brasileiro

    @field_validator('wkt')
    @classmethod
    def validar_wkt(cls, v: str) -> str:
        tipos_permitidos = ('POLYGON', 'MULTIPOLYGON')
        v_upper = v.strip().upper()
        if not any(v_upper.startswith(t) for t in tipos_permitidos):
            raise ValueError('Geometria deve ser POLYGON ou MULTIPOLYGON')
        return v

    def as_geojson(self) -> dict:
        """Converte WKT para GeoJSON (requer shapely)."""
        from shapely import wkt, to_geojson
        import json
        return json.loads(to_geojson(wkt.loads(self.wkt)))
```

### 2.6 Serviços de Domínio

```python
from abc import ABC, abstractmethod

class CalculadorAreaReservaLegal:
    """Calcula área mínima de Reserva Legal por bioma (Lei 12.651/2012, Art. 12)."""

    PERCENTUAIS = {
        'amazonia_legal': 0.80,       # 80% — Art. 12, I, a
        'cerrado_amazonia_legal': 0.35,  # 35% — Art. 12, I, b
        'campos_gerais_amazonia': 0.20,  # 20% — Art. 12, I, c
        'mata_atlantica': 0.20,       # 20% — Art. 12, II
        'cerrado': 0.20,              # 20% — Art. 12, II
        'pantanal': 0.20,             # 20% — Art. 12, II
        'pampa': 0.20,                # 20% — Art. 12, II
    }

    def calcular_area_minima(
        self,
        area_total: ÁreaTotalHectares,
        bioma: str
    ) -> ÁreaTotalHectares:
        percentual = self.PERCENTUAIS.get(bioma)
        if percentual is None:
            raise ValueError(f'Bioma desconhecido: {bioma}')
        area_minima = area_total.valor * percentual
        return ÁreaTotalHectares(valor=area_minima)

    def verificar_conformidade(
        self,
        area_rl_declarada: ÁreaTotalHectares,
        area_total: ÁreaTotalHectares,
        bioma: str
    ) -> tuple[bool, str]:
        area_minima = self.calcular_area_minima(area_total, bioma)
        conforme = area_rl_declarada.valor >= area_minima.valor
        mensagem = (
            f"Conforme: {area_rl_declarada.valor:.2f} ha ≥ {area_minima.valor:.2f} ha ({self.PERCENTUAIS[bioma]*100:.0f}%)"
            if conforme else
            f"Não conforme: {area_rl_declarada.valor:.2f} ha < mínimo de {area_minima.valor:.2f} ha"
        )
        return conforme, mensagem


class ValidadorGeometria:
    """Valida geometria do imóvel: fechamento, auto-intersecção, SRID, área."""

    def validar(self, geometria: Geometria) -> 'ResultadoValidaçãoGeometria':
        try:
            from shapely import wkt
            from shapely.validation import explain_validity
            geom = wkt.loads(geometria.wkt)
        except Exception as e:
            return ResultadoValidaçãoGeometria(valido=False, erros=[f"WKT inválido: {e}"])

        erros = []
        if not geom.is_valid:
            erros.append(f"Geometria inválida: {explain_validity(geom)}")
        if geom.area == 0:
            erros.append("Geometria com área zero")
        if geometria.srid != 4674:
            erros.append(f"SRID {geometria.srid} incorreto. Use 4674 (SIRGAS 2000)")

        return ResultadoValidaçãoGeometria(valido=len(erros) == 0, erros=erros)


class ClassificadorProcesso:
    """Classifica prioridade e score de risco de um processo."""

    def calcular_score_risco(
        self,
        alertas_ibama: List[dict],
        alertas_deter: List[dict],
        area_ha: float,
        bioma: str
    ) -> float:
        score = 0.0
        # Alertas IBAMA pesam 40%
        score += min(len(alertas_ibama) * 2.0, 4.0)
        # Alertas DETER pesam 40%
        score += min(len(alertas_deter) * 2.0, 4.0)
        # Amazônia Legal tem peso maior
        if bioma == 'amazonia_legal':
            score *= 1.25
        # Área grande tem mais impacto
        if area_ha > 10_000:
            score += 1.0
        return min(round(score, 2), 10.0)
```

### 2.7 Eventos de Domínio

```python
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class ProcessoIniciado:
    processo_id: UUID
    requerente_id: UUID
    municipio_ibge: str
    occurred_at: datetime

    @property
    def routing_key(self) -> str:
        return "processo.iniciado.v1"

@dataclass(frozen=True)
class ProcessoSubmetido:
    processo_id: UUID
    requerente_id: UUID
    municipio_ibge: str
    area_total_ha: float
    total_documentos: int
    occurred_at: datetime

    @property
    def routing_key(self) -> str:
        return "processo.submetido.v1"

@dataclass(frozen=True)
class PendênciaIdentificada:
    processo_id: UUID
    pendencia_id: UUID
    tipo: str
    titulo: str
    prazo: Optional[datetime]
    criado_por_analista_id: Optional[UUID]
    criado_por_sistema: bool
    occurred_at: datetime

    @property
    def routing_key(self) -> str:
        return "processo.pendencia_identificada.v1"

@dataclass(frozen=True)
class ProcessoAprovado:
    processo_id: UUID
    analista_id: UUID
    numero_car: str
    occurred_at: datetime

    @property
    def routing_key(self) -> str:
        return "processo.aprovado.v1"

@dataclass(frozen=True)
class ProcessoRejeitado:
    processo_id: UUID
    analista_id: UUID
    motivo: str
    codigo_motivo: str
    occurred_at: datetime

    @property
    def routing_key(self) -> str:
        return "processo.rejeitado.v1"
```

### 2.8 Interface do Repositório

```python
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

class ProcessoCARRepository(ABC):

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[ProcessoCAR]: ...

    @abstractmethod
    async def find_by_requerente(
        self,
        requerente_id: UUID,
        status: Optional[StatusProcesso] = None,
        limit: int = 20,
        cursor: Optional[str] = None
    ) -> tuple[List[ProcessoCAR], Optional[str]]: ...

    @abstractmethod
    async def find_pending_analysis(
        self,
        analista_id: Optional[UUID] = None,
        limit: int = 50
    ) -> List[ProcessoCAR]: ...

    @abstractmethod
    async def save(self, processo: ProcessoCAR) -> ProcessoCAR: ...

    @abstractmethod
    async def find_by_municipio(
        self,
        municipio_ibge: str,
        status: Optional[StatusProcesso] = None
    ) -> List[ProcessoCAR]: ...

    @abstractmethod
    async def find_by_geometria_intersects(
        self,
        geometria_wkt: str,
        srid: int = 4674
    ) -> List[ProcessoCAR]: ...
```

---

## 3. BC: Validação Documental — Supporting Domain

### 3.1 Agregado: LoteValidação

```python
@dataclass
class LoteValidação:
    """Agrupa validação de múltiplos documentos de um processo."""
    id: UUID
    processo_id: UUID
    documentos: List[ItemValidação]
    status: str  # aguardando, processando, concluido, falhou
    iniciado_em: Optional[datetime]
    concluido_em: Optional[datetime]

@dataclass
class ItemValidação:
    documento_id: UUID
    tipo_documento: TipoDocumento
    resultado_ocr: Optional['ResultadoOCR']
    dados_extraidos: Optional[dict]
    erros: List[str]
    status: str
```

### 3.2 Value Objects de Validação

```python
class ResultadoOCR(BaseModel):
    texto_extraido: str
    confianca: float           # 0.0 a 1.0
    paginas: int
    engine_utilizada: str      # "tesseract", "google_vision", "azure_form"
    duracao_segundos: float
    idioma_detectado: str = "pt"

    @property
    def confianca_aceitavel(self) -> bool:
        return self.confianca >= 0.70

class DadosExtraídosMatrícula(BaseModel):
    numero_matricula: str
    cartorio: Optional[str]
    municipio: Optional[str]
    area_ha: Optional[float]
    proprietario_nome: Optional[str]
    proprietario_cpf: Optional[str]
    data_registro: Optional[datetime]
    numero_livro: Optional[str]
    numero_folha: Optional[str]
```

### 3.3 Serviços de Domínio

```python
class ExtratordeDados:
    """Extrai campos estruturados do texto OCR baseado no tipo de documento."""

    def extrair(self, resultado_ocr: ResultadoOCR, tipo: TipoDocumento) -> dict:
        extratores = {
            TipoDocumento.MATRICULA_IMOVEL: self._extrair_matricula,
            TipoDocumento.CCIR: self._extrair_ccir,
            TipoDocumento.PLANTA_GEOREFERENCIADA: self._extrair_planta,
        }
        extrator = extratores.get(tipo, self._extrair_generico)
        return extrator(resultado_ocr.texto_extraido)

class ValidadorDocumental:
    """Verifica completude e consistência dos dados extraídos."""

    CAMPOS_OBRIGATORIOS = {
        TipoDocumento.MATRICULA_IMOVEL: ["numero_matricula", "area_ha", "proprietario_cpf"],
        TipoDocumento.CCIR: ["numero_ccir", "municipio", "area_ha"],
    }

    def validar(self, tipo: TipoDocumento, dados: dict) -> List[str]:
        erros = []
        for campo in self.CAMPOS_OBRIGATORIOS.get(tipo, []):
            if campo not in dados or dados[campo] is None:
                erros.append(f"Campo obrigatório ausente: {campo}")
        return erros

class ComparadorCruzado:
    """Compara dados entre documentos para detectar divergências."""

    TOLERANCIA_AREA_PERCENTUAL = 0.05  # 5% de tolerância

    def comparar_areas(self, area_declarada: float, area_documento: float) -> Optional[str]:
        if area_documento is None:
            return None
        divergencia = abs(area_declarada - area_documento) / max(area_declarada, area_documento)
        if divergencia > self.TOLERANCIA_AREA_PERCENTUAL:
            return (
                f"Área divergente: declarado={area_declarada:.2f}ha, "
                f"documento={area_documento:.2f}ha ({divergencia*100:.1f}% de diferença)"
            )
        return None
```

---

## 4. BC: Assistência Inteligente — Supporting Domain

### 4.1 Agregado: Conversa

```python
class TipoIntenção(str, Enum):
    DUVIDA_CONCEITUAL = "duvida_conceitual"
    CONSULTA_STATUS = "consulta_status"
    SOLICITAR_DOCUMENTO = "solicitar_documento"
    EXPLICAR_PENDENCIA = "explicar_pendencia"
    RECLAMACAO = "reclamacao"
    OUTRO = "outro"

@dataclass
class Intenção(BaseModel):
    tipo: TipoIntenção
    confianca: float           # 0.0 a 1.0
    entidades_extraidas: dict  # ex: {"numero_processo": "...", "tipo_doc": "matricula"}

@dataclass
class ModeloIA(BaseModel):
    provider: str      # "openai", "anthropic", "ollama"
    modelo: str        # "gpt-4o", "claude-3-5-sonnet-20241022", "llama3.2"
    temperatura: float = 0.3
    max_tokens: int = 2000

@dataclass
class Conversa:
    id: UUID
    user_id: UUID
    processo_id: Optional[UUID]
    mensagens: List['Mensagem']
    intencao_atual: Optional[Intenção]
    modelo_ia: ModeloIA
    status: str  # ativa, encerrada, escalonada
    total_tokens: int

    def adicionar_mensagem(self, role: str, conteudo: str) -> 'Mensagem':
        msg = Mensagem(id=uuid4(), conversa_id=self.id, role=role, conteudo=conteudo)
        self.mensagens.append(msg)
        return msg

    def encerrar(self) -> None:
        if self.status != "ativa":
            raise EstadoInvalidoError("Conversa não está ativa")
        self.status = "encerrada"

    def escalonar(self) -> None:
        self.status = "escalonada"
```

### 4.2 Anti-Corruption Layer para LLM

```python
from abc import ABC, abstractmethod
from typing import AsyncGenerator

class MensagemLLM(BaseModel):
    role: str   # "system", "user", "assistant"
    conteudo: str

class RespostaLLM(BaseModel):
    conteudo: str
    tokens_prompt: int
    tokens_completion: int
    latencia_ms: int
    modelo_utilizado: str

class LLMProvider(ABC):
    """Interface abstrata que isola o domínio dos providers externos de LLM.
    Anti-Corruption Layer: os adaptadores traduzem entre o modelo do domínio
    e o formato específico de cada provider."""

    @abstractmethod
    async def completar(
        self,
        mensagens: List[MensagemLLM],
        modelo: ModeloIA
    ) -> RespostaLLM: ...

    @abstractmethod
    async def completar_stream(
        self,
        mensagens: List[MensagemLLM],
        modelo: ModeloIA
    ) -> AsyncGenerator[str, None]: ...

    @abstractmethod
    async def embedar(self, textos: List[str]) -> List[List[float]]: ...

    @abstractmethod
    def mascarar_pii(self, texto: str) -> tuple[str, dict]: ...


class AnthropicAdapter(LLMProvider):
    """Adapter para Claude (Anthropic). Traduz MensagemLLM para Messages API."""

    def __init__(self, api_key: str):
        import anthropic
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    async def completar(self, mensagens: List[MensagemLLM], modelo: ModeloIA) -> RespostaLLM:
        import time
        start = time.monotonic()
        messages = [{"role": m.role, "content": m.conteudo} for m in mensagens if m.role != "system"]
        system = next((m.conteudo for m in mensagens if m.role == "system"), "")

        response = await self._client.messages.create(
            model=modelo.modelo,
            max_tokens=modelo.max_tokens,
            temperature=modelo.temperatura,
            system=system,
            messages=messages,
        )
        latencia_ms = int((time.monotonic() - start) * 1000)
        return RespostaLLM(
            conteudo=response.content[0].text,
            tokens_prompt=response.usage.input_tokens,
            tokens_completion=response.usage.output_tokens,
            latencia_ms=latencia_ms,
            modelo_utilizado=response.model,
        )

    async def completar_stream(self, mensagens: List[MensagemLLM], modelo: ModeloIA):
        messages = [{"role": m.role, "content": m.conteudo} for m in mensagens if m.role != "system"]
        system = next((m.conteudo for m in mensagens if m.role == "system"), "")
        async with self._client.messages.stream(
            model=modelo.modelo, max_tokens=modelo.max_tokens,
            temperature=modelo.temperatura, system=system, messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    def mascarar_pii(self, texto: str) -> tuple[str, dict]:
        """Substitui CPF e coordenadas por tokens antes de enviar ao LLM."""
        import re
        mapa = {}
        def substituir_cpf(match):
            token = f"[CPF_{len(mapa)+1:03d}]"
            mapa[token] = match.group(0)
            return token
        texto_mascarado = re.sub(r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}', substituir_cpf, texto)
        return texto_mascarado, mapa

    async def embedar(self, textos: List[str]) -> List[List[float]]:
        raise NotImplementedError("Use OpenAI para embeddings")


class OllamaAdapter(LLMProvider):
    """Adapter para Ollama (local). Para dados sensíveis que não podem sair da infra."""

    def __init__(self, base_url: str = "http://ollama:11434"):
        self._base_url = base_url

    async def completar(self, mensagens, modelo):
        import httpx, time
        start = time.monotonic()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/chat",
                json={
                    "model": modelo.modelo,
                    "messages": [{"role": m.role, "content": m.conteudo} for m in mensagens],
                    "stream": False,
                },
                timeout=120.0,
            )
        data = response.json()
        return RespostaLLM(
            conteudo=data["message"]["content"],
            tokens_prompt=data.get("prompt_eval_count", 0),
            tokens_completion=data.get("eval_count", 0),
            latencia_ms=int((time.monotonic() - start) * 1000),
            modelo_utilizado=modelo.modelo,
        )

    def mascarar_pii(self, texto: str) -> tuple[str, dict]:
        # Ollama roda localmente — dados sensíveis permitidos sem mascaramento
        return texto, {}
```

---

## 5. BC: Identidade e Acesso — Supporting Domain

### 5.1 Agregado: Usuário

```python
class TipoUsuário(str, Enum):
    PRODUTOR_RURAL = "produtor_rural"
    CONSULTOR_AMBIENTAL = "consultor_ambiental"
    ANALISTA_AMBIENTAL = "analista_ambiental"
    SUPERVISOR_AMBIENTAL = "supervisor_ambiental"
    ADMIN = "admin"

class NivelConfiabilidade(str, Enum):
    BRONZE = "bronze"    # Cadastro básico (email verificado)
    PRATA = "prata"      # Biometria ou validação bancária
    OURO = "ouro"        # Biometria facial (reconhecimento facial)

@dataclass
class Usuário:
    id: UUID
    cpf: CPF
    email: str
    nome_completo: str
    tipo: TipoUsuário
    nivel_confiabilidade: NivelConfiabilidade
    govbr_sub: str      # Subject do ID token Gov.br
    ativo: bool = True
    ultimo_acesso: Optional[datetime] = None

    def pode_submeter_processo(self) -> bool:
        """Invariante: submissão exige nível prata ou acima."""
        return self.nivel_confiabilidade in (
            NivelConfiabilidade.PRATA, NivelConfiabilidade.OURO
        ) and self.ativo

    def pode_aprovar_processo(self) -> bool:
        return self.tipo in (
            TipoUsuário.ANALISTA_AMBIENTAL,
            TipoUsuário.SUPERVISOR_AMBIENTAL,
            TipoUsuário.ADMIN,
        ) and self.ativo
```

---

## 6. Padrões DDD Aplicados

| Padrão | Onde Aplicado | Justificativa |
|---|---|---|
| **Aggregate Root** | ProcessoCAR, ImóvelRural, Conversa, Usuário | Garante consistência transacional e invariantes de negócio |
| **Value Object** | NumeroCAR, CPF, ÁreaTotalHectares, Geometria, ModeloIA | Imutabilidade + validação no construtor + igualdade por valor |
| **Domain Event** | ProcessoSubmetido, PendênciaIdentificada, ProcessoAprovado | Desacoplamento entre BCs via RabbitMQ |
| **Repository** | ProcessoCARRepository, ImóvelRuralRepository | Abstração da persistência — domínio não conhece SQLAlchemy |
| **Domain Service** | CalculadorAreaReservaLegal, ValidadorGeometria, ComparadorCruzado | Lógica que não pertence a uma entidade específica |
| **Factory** | ProcessoCAR.criar() (factory method) | Garante estado inicial válido com defaults corretos |
| **Anti-Corruption Layer** | LLMProvider, SICARAdapter, GovBrAdapter | Isola o domínio de APIs externas voláteis |
| **Specification** | ProcessosPendentesSpec, DocumentosObrigatóriosSpec | Encapsula regras de seleção reutilizáveis |
| **Outbox Pattern** | EventPublisher + tabela outbox | Garante entrega de eventos junto com a transação de negócio |
| **CQRS** | Commands (agregados DDD), Queries (views SQL otimizadas) | Separação de leitura e escrita para performance e clareza |

---

## 7. Sumário de Decisões de Design

| Decisão | Padrão | Justificativa | Trade-off |
|---|---|---|---|
| Geometria fora do agregado ProcessoCAR | ImóvelRural é agregado separado | Imóvel pode ter múltiplos processos ao longo do tempo | Relação 1:N entre imóvel e processos |
| Histórico de status imutável | Append-only (apenas INSERT) | Auditoria legal exige trilha imutável | Sem possibilidade de correção — erro exige evento de correção |
| Score de completude calculado por trigger | Function PL/pgSQL | Performance — calculado no banco onde os dados estão | Lógica de negócio no banco (aceitável para cálculo simples) |
| Pendência como entidade filha de ProcessoCAR | Dentro do agregado | Pendência não existe sem processo; consistência transacional | Agregado cresce — limitar a 50 pendências por processo |
| LLM selecionado por configuração em runtime | Strategy Pattern | Zero downtime ao trocar de provider | Testes de regressão necessários para cada provider |
