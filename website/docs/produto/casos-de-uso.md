---
sidebar_position: 3
title: Casos de Uso
description: Os 13 casos de uso do CARla — do registro guiado por IA ao atendimento via WhatsApp.
tags: [produto, casos-de-uso, gherkin]
---

# Casos de Uso

:::info Para quem é esta página
PMs e analistas de negócio. Para detalhes de implementação, veja os [endpoints de API](../apis/processos.md).
:::

## Mapa Geral

| ID | Caso de Uso | Ator Principal | Canal |
|---|---|---|---|
| UC-001 | Iniciar registro CAR com assistência IA | Produtor / Consultor | Portal Web |
| UC-002 | Upload e validação automática de documentos | Produtor / Consultor | Portal Web |
| UC-003 | Consulta conversacional de dúvidas | Qualquer usuário | Portal Web / WhatsApp |
| UC-004 | Acompanhamento de status do processo | Produtor / Consultor | Portal Web / WhatsApp |
| UC-005 | Triagem automática de processos | Analista | Portal Analista |
| UC-006 | Geração automática de dossiê | Analista / Sistema | Portal Analista |
| UC-007 | Notificação de pendências ao cidadão | Sistema | Email / WhatsApp |
| UC-008 | Aprovação ou rejeição pelo analista | Analista | Portal Analista |
| UC-009 | Correção de inconsistências guiada por IA | Produtor / Consultor | Portal Web |
| UC-010 | Vinculação WhatsApp via Gov.br | Produtor / Consultor | WhatsApp + Browser |
| UC-011 | Consulta de status via WhatsApp | Produtor / Consultor | WhatsApp |
| UC-012 | Notificação proativa via WhatsApp | Sistema | WhatsApp |
| UC-013 | Relatório de conformidade e analytics | Admin / Supervisor | Portal Admin |

---

## UC-001 — Iniciar Registro CAR com Assistência IA

**Fluxo principal:**
1. Usuário acessa "Novo Processo" no portal
2. Assistente IA inicia conversa de boas-vindas e solicita dados básicos
3. Usuário preenche nome do imóvel, município e estado
4. Sistema valida o município via código IBGE
5. Processo criado no status `rascunho`; assistente orienta próximas etapas

```gherkin
Cenário: Cidadão inicia processo com sucesso
  Dado que João está autenticado com nível "prata"
  Quando acessar "Novo Processo" e preencher dados básicos
  Então processo no status "rascunho" deve ser criado
  E assistente deve apresentar lista de documentos necessários

Cenário: Município não encontrado
  Quando informar município inexistente
  Então deve ver sugestões de municípios similares
  E processo não deve ser criado
```

---

## UC-002 — Upload e Validação Automática

**Fluxo principal:**
1. Usuário faz upload de documento (PDF/JPG, até 50MB)
2. Sistema armazena e retorna confirmação imediata (status `aguardando`)
3. Worker OCR processa assincronamente (< 60s)
4. Dados extraídos são comparados com dados declarados
5. Usuário recebe notificação com resultado (✓ válido / ✗ inválido + motivo)

:::tip Tipos aceitos
PDF, JPG, PNG, TIFF. Máximo 50MB por arquivo. Ver [API de Documentos](../apis/documentos.md).
:::

---

## UC-010 — Vinculação WhatsApp via Gov.br

Este caso de uso resolve o desafio de autenticar um usuário do WhatsApp sem que o canal suporte OAuth2 diretamente.

**Fluxo:**
1. Usuário envia mensagem ao número oficial do CARla no WhatsApp
2. Bot detecta número não vinculado e envia link temporário (10 min): `carla.gov.br/auth/wpp?token=XYZ`
3. Usuário clica, abre no browser, autentica com Gov.br
4. Sistema vincula número WhatsApp ao CPF autenticado (válido por 30 dias)
5. Bot retoma atendimento já identificado

```gherkin
Cenário: Primeira mensagem de número não vinculado
  Dado que o número "+5511999998888" não está vinculado
  Quando enviar qualquer mensagem ao CARla
  Então bot envia link de vinculação com TTL de 10 minutos

Cenário: Token de vinculação expirado
  Dado que o usuário não acessou o link em 10 minutos
  Quando tentar acessar o link expirado
  Então deve ver mensagem de expiração
  E bot envia novo link automaticamente
```

:::caution Operações críticas permanecem no portal web
Submissão de processos e upload de documentos **não são feitos pelo WhatsApp** — exigem o portal web por serem atos jurídicos formais.
:::

## Ver também

- [Requisitos Funcionais](./requisitos.md) — RFs derivados destes UCs
- [Fluxo do Cidadão](../design/fluxos/cidadao.md) — jornada visual
- [API WhatsApp](../apis/whatsapp.md) — implementação técnica
