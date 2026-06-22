---
sidebar_position: 2
title: Convenções de Código
description: Padrões de Git, Python, TypeScript e banco de dados do projeto CARla.
tags: [contribuindo, convenções, git, python, typescript]
---

# Convenções de Código

## Git — Conventional Commits

```
feat(processos): adicionar submissão com validação de geometria
fix(auth): corrigir expiração de refresh token em fuso horário
docs(api): atualizar exemplo de paginação cursor-based
test(dominio): adicionar casos de borda para CPF inválido
chore(deps): atualizar fastapi para 0.116
```

**Branches:**
```
feat/CAR-123-abertura-carla
fix/CAR-456-timeout-govbr
chore/atualizar-dependencias
```

## Python

| Elemento | Convenção | Exemplo |
|---|---|---|
| Módulos/arquivos | snake_case | `value_objects.py` |
| Classes | PascalCase | `ProcessoCAR`, `NumeroCAR` |
| Funções/métodos | snake_case | `calcular_area_rl()` |
| Constantes | UPPER_SNAKE_CASE | `MAX_TAMANHO_ARQUIVO` |
| Variáveis privadas | _snake_case | `_domain_events` |

**Linting:** Ruff com regras E, F, I, N, UP, S, B  
**Types:** mypy strict mode — sem `Any` sem justificativa

```bash
# Checar antes de commitar
uv run ruff check src/
uv run mypy src/
```

## TypeScript / React

| Elemento | Convenção | Exemplo |
|---|---|---|
| Componentes | PascalCase.tsx | `ProcessoStepper.tsx` |
| Hooks | usePascalCase.ts | `useProcessos.ts` |
| Utils | camelCase.ts | `formatters.ts` |
| Types/Interfaces | PascalCase | `ProcessoCARResponse` |
| Stores (Zustand) | camelCase + Store | `authStore.ts` |

## Banco de Dados

| Elemento | Convenção | Exemplo |
|---|---|---|
| Tabelas | snake_case, plural | `processos_car` |
| Colunas | snake_case | `data_submissao_at` |
| Índices | `idx_{tabela}_{coluna}` | `idx_processos_status` |
| Triggers | `trg_{tabela}_{evento}` | `trg_processos_updated_at` |
| Functions | `fn_{descricao}` | `fn_calcular_score_completude` |
| Migrations | `YYYY_MM_DD_NNNN_{descricao}.py` | `2026_01_15_0001_initial_schema.py` |

## Pull Requests

Checklist antes de abrir PR:
- [ ] Testes passando (`make test`)
- [ ] Sem lint errors (`make lint`)
- [ ] Cobertura ≥ 80% nos arquivos alterados
- [ ] SAST sem findings HIGH/CRITICAL
- [ ] Descrição do PR explica o **porquê**, não o **o quê**
- [ ] Se ADR necessária: criada e linkada
