---
sidebar_position: 4
title: Requisitos
description: Requisitos funcionais e não-funcionais do CARla organizados por módulo.
tags: [produto, requisitos, rf, rnf]
---

# Requisitos

:::info Para quem é esta página
PMs e tech leads. Os RNFs de performance e segurança têm detalhes em [Arquitetura](../arquitetura/visao-geral.md) e [Segurança](../seguranca/lgpd.md).
:::

## Requisitos Funcionais

### Portal do Cidadão

| ID | Requisito | Prioridade |
|---|---|---|
| RF-001 | Autenticação via Gov.br (OAuth2/OIDC, níveis bronze/prata/ouro) | Must |
| RF-002 | Perfil do usuário com dados básicos e central de privacidade LGPD | Must |
| RF-003 | Criar processo CAR com dados básicos do imóvel | Must |
| RF-004 | Formulário em etapas (stepper) com progresso visual | Must |
| RF-005 | Upload de documentos (PDF/JPG/PNG/TIFF, até 50MB) | Must |
| RF-006 | Dashboard com lista de processos e status em tempo real | Must |
| RF-007 | Linha do tempo do processo (histórico imutável) | Should |
| RF-008 | Visualização de pendências com prazo e instrução de resolução | Must |
| RF-009 | Resposta a pendências com envio de documentos complementares | Must |
| RF-010 | Notificações in-app e e-mail | Should |
| RF-010a | Canal WhatsApp com autenticação vinculada ao Gov.br | Should |
| RF-010b | Fluxo de vinculação WhatsApp via link temporário | Should |
| RF-010c | Notificação proativa de pendências via WhatsApp | Should |

### Assistente Inteligente

| ID | Requisito | Prioridade |
|---|---|---|
| RF-011 | Chat conversacional com streaming de respostas (SSE) | Must |
| RF-012 | Base de conhecimento RAG (normativos CAR, manuais SICAR) | Must |
| RF-013 | Classificação de intenção (dúvida, status, documento) | Should |
| RF-014 | Contexto do processo ativo nas respostas | Should |
| RF-015 | Solicitação de documento com link direto ao upload | Could |
| RF-016 | Escalonamento para analista humano quando necessário | Should |
| RF-017 | Histórico de conversas acessível pelo usuário | Could |
| RF-017a | Sessão WhatsApp com contexto do processo preservado | Should |
| RF-017b | Direcionamento para portal web em operações críticas | Must |
| RF-017c | Transcrição de mensagens de voz recebidas pelo WhatsApp (Whisper local) | Should |

### Motor de Validação

| ID | Requisito | Prioridade |
|---|---|---|
| RF-018 | OCR de documentos (PDF e imagens) | Must |
| RF-019 | Extração de campos estruturados por tipo de documento | Must |
| RF-020 | Validação de consistência entre campos extraídos e declarados | Must |
| RF-021 | Cruzamento com bases externas (IBGE) | Should |
| RF-022 | Geração automática de pendência quando inconsistência detectada | Must |
| RF-023 | Retry de OCR após reenvio de documento com melhor qualidade | Should |

### Ferramenta de Geometria

| ID | Requisito | Prioridade |
|---|---|---|
| RF-031 | Exibir mapa Leaflet com camada de imagem de satélite (tile layer) centrado no município declarado na Etapa 1 | Must |
| RF-032 | Permitir marcação de vértices por toque/clique sobre a imagem de satélite, com cálculo de área em tempo real | Must |
| RF-033 | Aceitar upload de KML ou SHP como alternativa ao desenho manual | Should |

### Portal do Analista

| ID | Requisito | Prioridade |
|---|---|---|
| RF-024 | Fila de processos com filtros e ordenação por prioridade/risco | Must |
| RF-025 | Tela unificada com dados, documentos validados e histórico | Must |
| RF-026 | Geração automática de dossiê PDF por IA | Should |
| RF-027 | Aprovar ou rejeitar processo com motivo obrigatório | Must |
| RF-028 | Criar pendência manual com descrição e prazo | Must |
| RF-029 | Dashboard de produtividade por analista | Should |
| RF-030 | Canal de comunicação com cidadão vinculado ao processo | Could |

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
| RNF-010 | Segurança | Autenticação | OAuth2/OIDC + JWT RS256 |
| RNF-013 | Conformidade | LGPD | 100% conforme |
| RNF-014 | Acessibilidade | Padrão | WCAG 2.1 nível AA |
| RNF-017 | Manutenibilidade | Cobertura de testes | ≥ 80% |

:::caution LGPD — requisito inegociável
Todos os dados pessoais (CPF, e-mail, geometria do imóvel) devem ser tratados conforme a Lei 13.709/2018. Ver [LGPD](../seguranca/lgpd.md).
:::
