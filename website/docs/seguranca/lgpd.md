---
sidebar_position: 1
title: LGPD — Proteção de Dados
description: Dados pessoais tratados, direitos dos titulares, DPO e conformidade com a Lei 13.709/2018.
tags: [segurança, lgpd, privacidade, conformidade]
---

# LGPD — Proteção de Dados

:::caution Requisito legal inegociável
A Lei Geral de Proteção de Dados Pessoais (Lei 13.709/2018) impõe obrigações para todos os sistemas que tratam dados de brasileiros. O CARla é um serviço público — a conformidade é mandatória.
:::

## Dados Pessoais Tratados

| Dado | Finalidade | Base Legal | Retenção | Proteção |
|---|---|---|---|---|
| CPF | Autenticação, vinculação ao imóvel | Obrigação legal (Lei 12.651) | 5 anos pós-inatividade | pgcrypto + hash SHA-256 |
| E-mail | Notificações | Interesse legítimo | 5 anos | pgcrypto |
| Nome completo | Identificação em documentos | Obrigação legal | 10 anos | Armazenado em claro |
| Geometria do imóvel | Registro CAR | Obrigação legal | Indefinida | RBAC estrito — o dado de imóvel rural é público nos termos da Lei 12.651, mas a geometria precisa de imóvel de pessoa física pode revelar informações patrimoniais sensíveis quando combinada com outros dados. Acesso individual só via autenticação; exports agregados e anonimizados. |
| Número WhatsApp | Canal de atendimento | Consentimento | 30 dias (sessão) + revogação | Hash SHA-256 apenas |
| Documentos pessoais | Comprovação de propriedade | Obrigação legal | 10 anos pós-conclusão | AES-256 no MinIO |
| Conversas com IA | Atendimento | Consentimento | 90 dias → anonimização | PII masking para LLM externo |

## Direitos dos Titulares (Art. 18 LGPD)

| Direito | Como exercer | Prazo |
|---|---|---|
| **Acesso** | Portal → Minha Conta → Exportar Meus Dados | 15 dias úteis |
| **Retificação** | Portal → Minha Conta → Editar Dados | 15 dias úteis |
| **Eliminação** | Portal → Solicitar Exclusão da Conta | 15 dias úteis |
| **Portabilidade** | Portal → Exportar em JSON | 15 dias úteis |
| **Revogação de consentimento** | Portal → Privacidade → Revogar | Imediato |
| **Informação sobre compartilhamento** | Aviso de Privacidade (link no rodapé) | — |

## DPO — Encarregado de Proteção de Dados

Conforme Art. 41 da LGPD, o CARla deve indicar um DPO.

- **Canal de contato obrigatório:** `dpo@carcopilot.gov.br`
- **Prazo de resposta:** 15 dias úteis para todas as solicitações
- **Registro:** todas as solicitações registradas internamente

## Notificação de Incidentes (Art. 48)

Em caso de incidente de segurança que afete dados pessoais:

1. **Comunicar à ANPD** em até 72 horas via [portal ANPD](https://www.gov.br/anpd)
2. **Comunicar os titulares** afetados em prazo razoável
3. **Conteúdo mínimo:** natureza dos dados, titulares afetados, medidas adotadas, riscos

## Criptografia em Repouso

```sql
-- CPF criptografado com pgcrypto
INSERT INTO users (cpf_hash, cpf_encrypted)
VALUES (
    encode(digest('12345678901' || current_setting('app.cpf_salt'), 'sha256'), 'hex'),
    pgp_sym_encrypt('12345678901', current_setting('app.encryption_key'))
);
```

O hash SHA-256 permite buscas sem descriptografar. A chave de criptografia fica no Vault (HashiCorp), nunca em variável de ambiente plain text.

## Ver também

- [Autenticação e RBAC](./autenticacao.md) — controle de acesso por role
- [Auditoria](./auditoria.md) — trilha de eventos e retenção de logs
- [ADR-005 — Gov.br](../arquitetura/decisoes/adr-005-govbr.md) — por que Gov.br elimina responsabilidade de senha
