# ADR-006: Estratégia de IA — LLM Agnóstico com Adapter Pattern

**Status:** Aceito  
**Data:** 2026-06-01  
**Contexto:** BC Assistência Inteligente + geração de dossiês

---

## Contexto

O CARla usa IA generativa em três cenários:

1. **Assistente conversacional:** Responde dúvidas sobre CAR, orienta o preenchimento, explica pendências
2. **Extração de dados:** Estrutura informações do texto OCR de documentos
3. **Geração de dossiê:** Compila um resumo executivo do processo para o analista

Os requisitos conflitantes são:
- **LGPD:** CPF, coordenadas de imóvel e documentos pessoais são dados pessoais — não podem ir para LLMs externos na nuvem sem mascaramento e base legal adequada
- **Performance:** LLMs na nuvem têm latência de 1-3s (primeiro token) — aceitável para chat, inaceitável para validação em massa
- **Custo:** Em 50.000 usuários/mês, custo de LLM pode ser proibitivo sem otimização
- **Vendor lock-in:** Mercado de LLM evolui rapidamente — Claude hoje, algo melhor amanhã
- **Qualidade:** Alguns providers são melhores em contextos específicos (português, domínio legal)

---

## Decisão

**Arquitetura de Adapter Pattern com LLMProvider abstrato:**

```
                    ┌──────────────────────┐
                    │   AssistentService   │
                    │   (Application)      │
                    └──────────┬───────────┘
                               │ usa interface
                    ┌──────────▼───────────┐
                    │    LLMProvider       │
                    │    (Abstract)        │
                    └──────┬───────────────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
  ┌───────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
  │  Anthropic   │  │   OpenAI    │  │   Ollama    │
  │  Adapter     │  │   Adapter   │  │   Adapter   │
  │  (Claude)    │  │  (GPT-4o)   │  │  (local)    │
  └──────────────┘  └─────────────┘  └─────────────┘
```

### Seleção de Provider por Tipo de Dado

```python
class LLMProviderFactory:
    """Seleciona o provider adequado baseado no contexto."""

    def get_provider(self, contexto: 'ContextoLLM') -> LLMProvider:
        if contexto.contem_dados_sensiveis:
            # Dados sensíveis (CPF, coordenadas) → Ollama local
            return self._ollama
        if contexto.tipo == "chat_assistente":
            # Chat: Claude ou GPT-4o (melhor em português jurídico)
            return self._primary_provider
        if contexto.tipo == "extracao_dados":
            # Extração: modelo mais rápido e barato
            return self._fast_provider
        if contexto.tipo == "geracao_dossie":
            # Dossiê: modelo mais capaz (qualidade sobre custo)
            return self._premium_provider
        return self._primary_provider
```

### PII Masking antes de enviar para LLM externo

```python
class PIIMasker:
    """Remove informações pessoais antes de enviar para LLM na nuvem."""

    PATTERNS = [
        (r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}', '[CPF]'),          # CPF
        (r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', '[CNPJ]'),     # CNPJ
        (r'-?\d{1,3}\.\d{4,8},\s*-?\d{1,3}\.\d{4,8}', '[COORD]'),  # Lat/Lon
    ]

    def mascarar(self, texto: str) -> tuple[str, dict]:
        mapa_reverso = {}
        texto_mascarado = texto
        for pattern, placeholder in self.PATTERNS:
            import re
            matches = re.findall(pattern, texto_mascarado)
            for i, match in enumerate(matches):
                token = f"{placeholder}_{i+1}"
                mapa_reverso[token] = match
                texto_mascarado = texto_mascarado.replace(match, token, 1)
        return texto_mascarado, mapa_reverso
```

### RAG — Retrieval-Augmented Generation

```python
class BaseDeConhecimentoCAR:
    """
    Indexa documentos normativos do CAR para o assistente.
    Usa pgvector como vector store integrado ao PostgreSQL.
    """

    FONTES = [
        "Lei 12.651/2012 — Código Florestal",
        "Instrução Normativa MMA 2/2014 — SICAR",
        "Manual de Uso do SICAR v3.0",
        "FAQ CAR — Perguntas Frequentes",
        "Normas IBAMA para APP e Reserva Legal",
    ]

    CHUNK_SIZE = 500     # tokens por chunk
    CHUNK_OVERLAP = 50   # tokens de sobreposição
    TOP_K = 5            # chunks mais relevantes por consulta

    async def buscar(self, query: str, top_k: int = None) -> List[ChunkDocumento]:
        embedding = await self._embedder.embedar([query])
        # SQL com pgvector
        return await self._repo.buscar_por_similaridade(
            embedding=embedding[0],
            top_k=top_k or self.TOP_K,
            limite_distancia=0.8,
        )
```

### Estratégia de Cache de Respostas

```python
# Cache semântico: perguntas similares retornam resposta em cache
# Evita LLM para perguntas frequentes como "O que é CAR?"
class CacheSemanticoLLM:
    SIMILARIDADE_MINIMA = 0.95  # 95% de similaridade para hit de cache
    TTL = 3600  # 1 hora

    async def get_or_generate(self, query: str, generator) -> str:
        # Busca no cache Redis por embedding da query
        embedding = await self._embedder.embedar([query])
        cached = await self._redis.buscar_similar(embedding[0], self.SIMILARIDADE_MINIMA)
        if cached:
            return cached.resposta
        resposta = await generator(query)
        await self._redis.salvar(query, embedding[0], resposta, ttl=self.TTL)
        return resposta
```

---

## Configuração por Ambiente

```python
# settings.py
class LLMSettings(BaseSettings):
    LLM_PRIMARY_PROVIDER: str = "anthropic"  # "openai", "anthropic", "ollama"
    LLM_FAST_PROVIDER: str = "anthropic"
    LLM_LOCAL_MODEL: str = "llama3.2"        # Modelo Ollama para dados sensíveis

    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-4-6"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    OLLAMA_BASE_URL: str = "http://ollama:11434"

    LLM_MAX_TOKENS_CHAT: int = 2000
    LLM_MAX_TOKENS_DOSSIE: int = 4000
    LLM_TEMPERATURA_CHAT: float = 0.3
    LLM_TEMPERATURA_EXTRACAO: float = 0.0  # Determinístico para extração
```

---

## Consequências

### Positivas
- **Sem vendor lock-in:** Troca de provider sem mudança no código de negócio
- **LGPD-compliant:** Dados sensíveis processados localmente com Ollama
- **Otimização de custo:** Ollama para consultas frequentes, LLM premium apenas quando necessário
- **Fallback resiliente:** Se LLM externo cair, Ollama local assume
- **Testabilidade:** Interface abstrata facilita mocks em testes

### Negativas
- **Manutenção de múltiplos adapters:** Cada provider tem suas peculiaridades de API
- **Qualidade variável:** Ollama local pode ter qualidade inferior para português jurídico
- **Infraestrutura local:** Ollama precisa de GPU ou CPU potente para performance aceitável

### Riscos
- Modelos Ollama precisam de RAM significativa (Llama 3.2 7B: ~8GB RAM)
- **Mitigação:** Dimensionar nó dedicado para Ollama; fallback para LLM externo com mascaramento se Ollama indisponível

---

## Alternativas Consideradas

| Alternativa | Prós | Contras | Motivo da Rejeição |
|---|---|---|---|
| **LangChain** | Abstração pronta, muitos integradores | API instável (breaking changes frequentes), abstração excessiva, dificulta debug | Overhead sem benefício claro; atualizações frequentes são risco |
| **LlamaIndex** | Bom para RAG, mais estável | Foca em RAG, não tem abstrações de chat tão boas | Pode ser usado como biblioteca RAG sem ser o framework principal |
| **Framework próprio** | Controle total | Alto custo de manutenção para algo não-core | Reinventar a roda; nosso adapter pattern é suficiente |
| **Apenas OpenAI** | Simplicidade | Vendor lock-in; custo; LGPD com dados sensíveis | Risco de dependência única e custo imprevisível |
| **Apenas Ollama** | Zero custo, LGPD nativo | Qualidade inferior em PT-BR; hardware custoso | Qualidade insuficiente para assistente conversacional de qualidade |

---

## Referências

- [Anthropic API — Claude](https://docs.anthropic.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Ollama — Local LLMs](https://ollama.com/)
- [pgvector — Vector similarity search](https://github.com/pgvector/pgvector)
- [LGPD Art. 7 — Bases legais para tratamento](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
