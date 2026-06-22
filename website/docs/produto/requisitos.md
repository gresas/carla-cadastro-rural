---
sidebar_position: 4
title: Requisitos
description: Requisitos funcionais e não-funcionais da Carla organizados por módulo.
tags: [produto, requisitos, rf, rnf]
---

# Requisitos

:::info Para quem é esta página
PMs e tech leads. Os RNFs de performance e segurança têm detalhes em [Arquitetura](../arquitetura/visao-geral.md) e [Segurança](../seguranca/lgpd.md).
:::

## Requisitos Funcionais

### Interface de Chat (Canal Web)

| ID | Requisito | Prioridade |
|---|---|---|
| RF-001 | Autenticação via Gov.br (OAuth2/OIDC, níveis bronze/prata/ouro) | Must |
| RF-002 | Sessão web persistente vinculada ao `user_id` do Gov.br | Must |
| RF-003 | Ao retornar, a Carla resume etapa atual, mensagens não lidas do analista e próximas ações | Must |
| RF-004 | Histórico de conversa acessível pelo usuário em sessões futuras | Should |
| RF-005 | Perfil do usuário com dados básicos e central de privacidade LGPD | Must |
| RF-006 | Sem dependência de APIs de mensageria proprietárias (WhatsApp, Telegram) no canal core | Must |
| RF-007 | Integração com apps de mensageria implementável futuramente como adapter desacoplado | Could |

### Fluxo de Criação do CAR (6 etapas)

| ID | Requisito | Prioridade |
|---|---|---|
| RF-010 | Criar processo CAR guiado pelas 6 etapas: Cadastrante → Imóvel → Domínio → Documentação → Geo → Informações | Must |
| RF-011 | Reaproveitamento de dados entre etapas: dado já coletado nunca é solicitado novamente | Must |
| RF-012 | Confirmação em bloco ao final de cada etapa (não campo a campo) | Must |
| RF-013 | Progresso salvo automaticamente — usuário pode parar e retomar em qualquer etapa | Must |
| RF-014 | Etapa Geo com sugestão de demarcação de polígonos pré-carregada com base nos dados já informados (área, município) — o usuário ajusta e confirma; não é necessário desenhar do zero | Must |
| RF-015 | Aceitar upload de KML ou SHP como alternativa ao ajuste manual de polígono | Should |

### Assistente Conversacional (Carla)

| ID | Requisito | Prioridade |
|---|---|---|
| RF-020 | Chat conversacional com streaming de respostas (SSE) | Must |
| RF-021 | Base de conhecimento RAG (normativos CAR, manuais SICAR) | Must |
| RF-022 | Classificação de intenção (dúvida, status, documento, retomada de etapa) | Should |
| RF-023 | Contexto do processo ativo nas respostas | Should |
| RF-024 | Escalonamento para analista humano quando necessário — Carla encaminha a pergunta | Should |

### Upload e Validação Documental

| ID | Requisito | Prioridade |
|---|---|---|
| RF-030 | Upload de documentos (PDF/JPG/PNG/TIFF, até 50MB) via interface de chat | Must |
| RF-031 | OCR de documentos assíncrono (< 60s) | Must |
| RF-032 | Extração de campos estruturados por tipo de documento | Must |
| RF-033 | Validação de consistência entre dados extraídos e dados declarados nas etapas anteriores | Must |
| RF-034 | Geração automática de pendência quando inconsistência detectada | Must |

### Acompanhamento de Status

| ID | Requisito | Prioridade |
|---|---|---|
| RF-040 | Status do CAR exibido com a terminologia oficial do SICAR (Em Andamento → Cadastrado → Gravado/Enviado → Em Análise → Regular / Pendente de Regularização) | Must |
| RF-041 | Notificação in-app e e-mail quando analista criar pendência | Must |
| RF-042 | Recibo de Inscrição do Imóvel Rural no CAR disponível para download quando status for "Regular" | Must |
| RF-043 | Demonstrativo da Situação do CAR com aba Regularização Ambiental quando aplicável | Should |

### Portal do Analista

| ID | Requisito | Prioridade |
|---|---|---|
| RF-050 | Fila de processos com filtros e ordenação por prioridade/risco | Must |
| RF-051 | Tela unificada com dados, documentos validados e histórico | Must |
| RF-052 | Geração automática de dossiê PDF por IA | Should |
| RF-053 | Encaminhar processo como Regular ou criar pendência de regularização, com motivo obrigatório | Must |
| RF-054 | Criar pendência manual com descrição e prazo | Must |
| RF-055 | Dashboard de produtividade por analista | Should |
| RF-056 | Canal de comunicação com cidadão vinculado ao processo | Could |

---

## Requisitos Não-Funcionais

| ID | Categoria | Requisito | Meta |
|---|---|---|---|
| RNF-001 | Performance | Latência p95 da API | < 500ms |
| RNF-002 | Performance | Primeiro token do assistente IA | < 2s |
| RNF-003 | Performance | Processamento OCR por documento | < 60s |
| RNF-004 | Performance | Geração de dossiê PDF | < 30s |
| RNF-005 | Disponibilidade | SLA do sistema | ≥ 99,5% |
| RNF-006 | Disponibilidade | RTO (Recovery Time Objective) | < 4h |
| RNF-007 | Disponibilidade | RPO (Recovery Point Objective) | < 1h |
| RNF-008 | Portabilidade | Open source, sem dependências de fornecedores proprietários no core | Must |
| RNF-010 | Segurança | Autenticação | OAuth2/OIDC + JWT RS256 |
| RNF-013 | Conformidade | LGPD | 100% conforme |
| RNF-014 | Acessibilidade | Padrão | WCAG 2.1 nível AA |
| RNF-017 | Manutenibilidade | Cobertura de testes | ≥ 80% |

:::caution LGPD — requisito inegociável
Todos os dados pessoais (CPF, e-mail, geometria do imóvel, histórico de conversa) devem ser tratados conforme a Lei 13.709/2018. Ver [LGPD](../seguranca/lgpd.md).
:::
