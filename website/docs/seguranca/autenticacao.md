---
sidebar_position: 2
title: Autenticação e RBAC
description: JWT RS256, RBAC, OWASP Top 10 e controle de acesso por role.
tags: [segurança, autenticação, rbac, jwt, owasp]
---

# Autenticação e Controle de Acesso

:::info Para quem é esta página
Engenheiros back-end e revisores de segurança. Para o fluxo OAuth2, veja [API — Autenticação](../apis/autenticacao.md).
:::

## JWT — Segurança

| Parâmetro | Valor |
|---|---|
| Algoritmo | RS256 (RSA 2048-bit) |
| Expiração do access token | 1 hora |
| Expiração do refresh token | 30 dias (com rotação) |
| Blacklist | Redis — SET `jwt:blacklist:{jti}` com TTL = expiração |
| Rotação de chaves | A cada 24h via HashiCorp Vault |

**Refresh Rotation:** A cada uso do refresh token, um novo é emitido e o anterior é invalidado. Isso detecta uso paralelo (indicativo de roubo).

## RBAC — Matriz de Permissões

| Operação | Produtor | Consultor | Analista | Supervisor | Admin |
|---|---|---|---|---|---|
| Criar processo | ✓ | ✓* | — | — | ✓ |
| Ver próprio processo | ✓ | ✓* | ✓ | ✓ | ✓ |
| Ver processo de terceiro | — | — | ✓ | ✓ | ✓ |
| Aprovar processo | — | — | ✓ | ✓ | ✓ |
| Rejeitar processo | — | — | ✓ | ✓ | ✓ |
| Criar pendência | — | — | ✓ | ✓ | ✓ |
| Acessar audit logs | — | — | — | ✓ | ✓ |
| Configurar sistema | — | — | — | — | ✓ |

\* Consultor acessa apenas processos com autorização explícita do proprietário.

## OWASP Top 10 — Principais Mitigações

| OWASP | Mitigação no CARla |
|---|---|
| A01 Broken Access Control | RBAC + ownership check + retorno 404 (não 403) + testes de autorização |
| A02 Cryptographic Failures | TLS 1.3, AES-256, RS256, pgcrypto, sem MD5/SHA-1 |
| A03 Injection | Pydantic v2 valida todos os inputs; ORM parametrizado; sem raw SQL com input do usuário |
| A07 Auth Failures | Gov.br cuida da senha; JWT RS256; lockout após 5 tentativas; blacklist Redis |
| A09 Logging Failures | Audit log imutável; logs estruturados JSON; SIEM integration |
| A10 SSRF | Whitelist de URLs externas; egress network policy no Kubernetes |

## Lockout de Autenticação

- **5 tentativas falhas** em 15 minutos por IP → bloqueio 15 minutos
- **5 tentativas falhas** em 15 minutos por CPF → bloqueio 15 minutos + e-mail de aviso
- Delay progressivo: 1s → 2s → 5s → 10s → bloqueio
