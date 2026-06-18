---
sidebar_position: 7
title: "ADR-006: Estratégia de IA"
description: Por que adotamos LLM agnóstico com Adapter Pattern e Ollama para dados sensíveis.
tags: [adr, ia, llm, ollama, lgpd, rag]
---

# ADR-006: LLM Agnóstico com Adapter Pattern

**Status:** Aceito | **Data:** 2026-06-01

## Contexto

O assistente precisa de LLM para responder dúvidas, extrair dados e gerar dossiês. Restrições: LGPD (CPF e geometria não podem ir para nuvem sem mascaramento), mercado LLM evolui rápido (evitar lock-in), custo variável por volume.

## Decisão

**Interface abstrata `LLMProvider`** com adapters para Claude (Anthropic), GPT-4o (OpenAI) e Ollama (local).

- **Dados sem PII** → Claude ou GPT-4o (melhor qualidade em PT-BR)
- **Dados sensíveis** → Ollama local (zero risco LGPD)
- **Perguntas frequentes** → Cache semântico Redis (custo zero)
- **RAG** → pgvector no PostgreSQL (sem vector store externo)

## Consequências

✅ Sem vendor lock-in — troca de provider sem mudança de código  
✅ Conformidade LGPD com Ollama para dados sensíveis  
✅ Otimização de custo: cache + Ollama reduzem chamadas pagas  
✅ Fallback resiliente: se LLM externo cair, Ollama assume  
❌ Manutenção de múltiplos adapters  
❌ Ollama exige hardware com GPU ou CPU potente

## Alternativas Rejeitadas

| Alternativa | Motivo |
|---|---|
| LangChain | API instável; breaking changes frequentes; abstração excessiva |
| Apenas OpenAI | Vendor lock-in; custo imprevisível; risco LGPD |
| Apenas Ollama | Qualidade inferior em PT-BR para casos de uso conversacionais |
