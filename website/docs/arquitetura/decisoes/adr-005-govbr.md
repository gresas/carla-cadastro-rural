---
sidebar_position: 6
title: "ADR-005: Autenticação Gov.br"
description: Por que usamos Gov.br como Identity Provider com OAuth2/OIDC.
tags: [adr, govbr, autenticação, oauth2, oidc]
---

# ADR-005: Autenticação via Gov.br com OAuth2/OIDC

**Status:** Aceito | **Data:** 2026-06-01

## Contexto

O CARla é uma plataforma pública brasileira. Cidadãos precisam de autenticação com CPF verificado. Criar uma senha própria aumenta abandono e responsabilidade de segurança.

## Decisão

**Gov.br como Identity Provider** via OAuth2 Authorization Code Flow + PKCE.

- Nível mínimo para consulta: bronze
- Nível mínimo para submissão: **prata** (ato jurídico)
- Tokens internos: JWT RS256 com rotação de chaves via Vault
- Anti-Corruption Layer: `GovBrAdapter` isola o protocolo do domínio

**Fluxo WhatsApp:** Link temporário (TTL 10min) → Gov.br no browser → número vinculado ao user_id no Redis (30 dias).

## Consequências

✅ CPF verificado de graça — Gov.br já fez a verificação  
✅ Sem nova senha para o cidadão — menor abandono  
✅ 150M+ contas disponíveis — base de usuários imediata  
✅ Conformidade com Decreto 10.900/2021  
❌ Dependência externa crítica — Gov.br fora do ar = cidadãos bloqueados  
❌ SLA do Gov.br não é público — histórico de instabilidades em picos

## Mitigação

Modo degradado para servidores públicos (auth simplificada de emergência, desabilitada por padrão).

## Alternativas Rejeitadas

| Alternativa | Motivo |
|---|---|
| Identity Provider próprio | Alta responsabilidade de segurança; sem CPF verificado |
| Keycloak | Complexidade operacional sem benefício extra |
| AWS Cognito | Vendor lock-in; não integra nativamente com Gov.br |
