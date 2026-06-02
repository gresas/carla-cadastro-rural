---
sidebar_position: 3
title: Auditoria e Rastreabilidade
description: Audit logs imutáveis, eventos de segurança auditados e trilha do processo.
tags: [segurança, auditoria, rastreabilidade, lgpd]
---

# Auditoria e Rastreabilidade

:::info Para quem é esta página
Engenheiros, compliance e auditores. Para contexto LGPD, veja [LGPD](./lgpd.md).
:::

## Audit Log de Banco

Um trigger PL/pgSQL captura automaticamente toda operação de escrita em tabelas críticas:

```sql
CREATE OR REPLACE FUNCTION fn_audit_log() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_logs (tabela_nome, registro_id, operacao, dados_antes, dados_depois)
    VALUES (
        TG_TABLE_NAME,
        CASE TG_OP WHEN 'DELETE' THEN OLD.id ELSE NEW.id END,
        TG_OP::operacao_audit_enum,
        CASE TG_OP WHEN 'INSERT' THEN NULL ELSE to_jsonb(OLD) END,
        CASE TG_OP WHEN 'DELETE' THEN NULL ELSE to_jsonb(NEW) END
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

**Características:**
- Particionado por mês (performance em queries históricas)
- **Imutável** — política de banco: sem UPDATE/DELETE em `audit_logs`
- Retenção: 5 anos (requisito legal do CAR)

## Histórico Imutável do Processo

Cada mudança de status do processo gera um registro em `historico_processos`:

| Campo | Descrição |
|---|---|
| `status_anterior` | Status antes da mudança |
| `status_novo` | Status após a mudança |
| `motivo` | Justificativa do analista (obrigatória em rejeição) |
| `ator_id` | UUID do usuário humano responsável |
| `ator_sistema` | Nome do serviço se ação automática |
| `created_at` | Timestamp imutável |

## Eventos de Segurança Auditados

| Evento | Campos registrados |
|---|---|
| Login bem-sucedido | user_id, ip, user_agent, timestamp |
| Falha de login | ip, cpf_hash (sem CPF), motivo, timestamp |
| Logout | user_id, session_id, timestamp |
| Acesso negado | user_id, recurso tentado, timestamp |
| Download de dossiê | user_id, processo_id, timestamp |
| Aprovação de processo | analista_id, processo_id, observações |
| Rejeição de processo | analista_id, processo_id, motivo, código |
| Mudança de role | admin_id, user_id, role_anterior, role_nova |
| Tentativa OAuth2 fraudulenta | ip, state_tentado, timestamp |

:::caution CPF não aparece nos logs
Logs de segurança usam `cpf_hash` (SHA-256), nunca o CPF em claro. Isso garante rastreabilidade sem expor dados pessoais em arquivos de log.
:::

## Pipeline de Segurança CI/CD

```bash
# Executado em cada PR
bandit -r src/ -ll -i            # SAST Python
safety check --json               # CVEs em dependências
gitleaks detect --source .        # Segredos no código
trivy image carla-backend:latest  # Vulnerabilidades na imagem
```

**Quality gate:** zero findings HIGH/CRITICAL para merge na branch `main`.
