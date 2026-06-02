---
sidebar_position: 5
title: Estratégia de IA
description: LLM agnóstico com Adapter Pattern, RAG com pgvector e conformidade LGPD.
tags: [engenharia, ia, llm, rag, lgpd]
---

# Estratégia de IA

:::info Para quem é esta página
Engenheiros back-end e ML engineers. Decisão arquitetural: [ADR-006](./decisoes/adr-006-ia.md).
:::

## Arquitetura LLM Agnóstico

```mermaid
graph LR
    AS[AssistentService] --> LP[LLMProvider\ninterface ABC]
    LP --> AA[AnthropicAdapter\nClaude Sonnet]
    LP --> OA[OpenAIAdapter\nGPT-4o]
    LP --> OL[OllamaAdapter\nLocal — dados sensíveis]
```

**Seleção por configuração:**
```bash
LLM_PRIMARY_PROVIDER=anthropic  # ou openai, ollama
```

A troca de provider **não exige mudança de código** — apenas variável de ambiente.

## PII Masking (conformidade LGPD)

Antes de enviar qualquer texto para um LLM externo na nuvem, o sistema substitui dados pessoais por tokens:

```python
class PIIMasker:
    PATTERNS = [
        (r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}', '[CPF]'),          # CPF
        (r'-?\d{1,3}\.\d{4,8},\s*-?\d{1,3}\.\d{4,8}', '[COORD]'),  # Lat/Lon
    ]

    def mascarar(self, texto: str) -> tuple[str, dict]:
        # Retorna texto mascarado + mapeamento reverso
        ...
```

:::caution Regra de ouro
Dados sensíveis (CPF, coordenadas do imóvel) → **Ollama local** sempre.
Dúvidas genéricas sobre CAR → Claude ou GPT-4o (sem PII).
:::

## RAG — Retrieval-Augmented Generation

O assistente responde com base na **base de conhecimento indexada**, não apenas no treinamento do LLM.

**Fontes indexadas:**
- Lei 12.651/2012 (Código Florestal)
- Instruções Normativas do SICAR
- Manual de Uso do SICAR v3.0
- FAQ CAR — Perguntas Frequentes

**Pipeline:**
```
Query do usuário
   → Embedding (text-embedding-3-small)
   → Busca vetorial no pgvector (top-5 chunks)
   → Monta prompt com chunks como contexto
   → LLM gera resposta embasada
   → Resposta com indicação de fonte
```

**Cache semântico:** Perguntas com ≥ 95% de similaridade retornam resposta em cache (Redis, TTL 1h) — evita chamada desnecessária ao LLM.

## Custos e Limites

| Cenário | Provider | Motivo |
|---|---|---|
| Dúvida sobre CAR (sem PII) | Claude / GPT-4o | Melhor qualidade em PT-BR |
| Dados do processo (com PII) | Ollama local | LGPD |
| Perguntas frequentes | Cache Redis | Custo zero |
| Geração de dossiê | Claude (premium) | Qualidade exige modelo maior |

## Ver também

- [ADR-006 — Estratégia de IA](./decisoes/adr-006-ia.md)
- [API do Assistente](../apis/assistente.md) — endpoints de chat e SSE
- [Banco de Dados — pgvector](./banco-de-dados.md#busca-semântica-pgvector)
