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
| R-11 | API SICAR sem acesso público — integração pode ser inviável sem convênio | Alta | Alta | Negociação institucional com MAPA/IBAMA + stub simulado para MVP | Operar sem sincronização SICAR na Fase 2; iniciar processo de convênio em paralelo |
| R-12 | Provider WhatsApp não oficial (Z-API ou similar) | Alta se não migrado | Alta | Usar exclusivamente Meta Cloud API oficial | Substituição de provider em emergência (número precisa ser remigrado) |
| R-13 | Qualidade de geometrias enviadas — principal causa de retrabalho no CAR | Alta | Alta | Validações em tempo real (área, município, self-intersection) + assistente IA guiando a etapa | Revisão manual para geometrias com alertas de sobreposição |
| R-14 | Responsabilidade administrativa em decisão baseada em IA | Média | Alta | Dossiê IA como apoio, não substituto; campo de observações obrigatório para analista | Revisão jurídica do fluxo de aprovação antes do piloto em órgão público |
| R-15 | Custo WhatsApp Business API em escala | Média | Média | Cache de conversas, limitar mensagens proativas, revisar volume | Capped budget mensal por órgão; negociar tarifas corporativas com Meta |

:::warning Riscos de maior atenção
R-01 (Gov.br), R-06 (LGPD), R-11 (API SICAR) e R-12 (provider WhatsApp) têm impacto alto — monitorar ativamente. R-11 e R-12 são riscos operacionais críticos que precisam ser mitigados antes do piloto.
:::
