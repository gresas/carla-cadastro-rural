---
sidebar_position: 6
title: Riscos e Mitigações
description: Principais riscos do projeto CARla com probabilidade, impacto e estratégias de mitigação.
tags: [produto, riscos, gestão]
---

# Riscos e Mitigações

:::info Para quem é esta página
PMs, gestores e tech leads. Riscos técnicos específicos estão documentados nos [ADRs](../arquitetura/decisoes/index.md).
:::

| ID | Risco | Prob. | Impacto | Mitigação | Contingência |
|---|---|---|---|---|---|
| R-01 | Indisponibilidade do Gov.br | Média | Alta | Circuit breaker + monitoramento de SLA | Modo manutenção com auth temporária para servidores |
| R-02 | Mudança na API do SICAR | Média | Alta | Anti-Corruption Layer isola impacto | Stub configurável para operação desacoplada |
| R-03 | Qualidade ruim de documentos enviados | Alta | Média | OCR com múltiplos engines + instruções de upload | Revisão manual para docs com baixa confiança |
| R-04 | Adoção baixa por baixo letramento digital | Média | Alta | UX simples + assistente IA + tutoriais | Parceria com extensão rural (EMATER) |
| R-05 | Custo elevado de LLM em escala | Média | Média | Cache semântico + Ollama local | Limitar tokens por sessão |
| R-06 | Violação de LGPD | Baixa | Alta | PII masking, criptografia, auditoria, DPO | Plano de resposta a incidentes + ANPD |
| R-07 | Escalabilidade insuficiente | Baixa | Alta | Kubernetes + auto-scaling + testes de carga | Horizontal scaling na nuvem |
| R-08 | Resistência dos analistas à mudança | Média | Média | Envolvimento no design + treinamento | Adoção gradual com champions |
| R-09 | Alteração na legislação do CAR | Baixa | Média | Regras via base de conhecimento (RAG) | Atualização da knowledge base |
| R-10 | Vazamento de dados geoespaciais | Baixa | Alta | RBAC estrito + sem export público individual | Auditoria imediata + notificação ANPD |

:::warning Riscos de maior atenção
R-01 (Gov.br) e R-06 (LGPD) têm impacto alto e dependência de terceiros — monitorar ativamente.
:::
