---
sidebar_position: 6
title: Riscos e Mitigações
description: Principais riscos do projeto Carla com probabilidade, impacto e estratégias de mitigação.
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
| R-03 | Qualidade ruim de documentos enviados | Alta | Média | OCR com múltiplos engines + instruções de upload na Carla | Revisão manual para docs com baixa confiança |
| R-04 | Adoção baixa por baixo letramento digital | Média | Alta | UX conversacional simples + assistente IA + tutoriais integrados à Carla | Parceria com extensão rural (EMATER) |
| R-05 | Custo elevado de LLM em escala | Média | Média | Cache semântico + Ollama local | Limitar tokens por sessão |
| R-06 | Violação de LGPD | Baixa | Alta | PII masking, criptografia, auditoria, DPO | Plano de resposta a incidentes + ANPD |
| R-07 | Escalabilidade insuficiente | Baixa | Alta | Kubernetes + auto-scaling + testes de carga | Horizontal scaling na nuvem |
| R-08 | Resistência dos analistas à mudança | Média | Média | Envolvimento no design + treinamento | Adoção gradual com champions |
| R-09 | Alteração na legislação do CAR | Baixa | Média | Regras via base de conhecimento (RAG) | Atualização da knowledge base |
| R-10 | Vazamento de dados geoespaciais | Baixa | Alta | RBAC estrito + sem export público individual | Auditoria imediata + notificação ANPD |
| R-11 | API SICAR sem acesso público — integração pode ser inviável sem convênio | Alta | Alta | Negociação institucional com MAPA/IBAMA + stub simulado para MVP | Operar sem sincronização SICAR na Fase 2; iniciar processo de convênio em paralelo |
| R-12 | Manutenção de interface de chat própria | Média | Média | Componentes de chat open source bem mantidos (ex: react-chat-ui, Botpress UI) + testes de regressão | Simplificação de UX de chat em caso de sobrecarga do time |
| R-13 | Qualidade de geometrias enviadas — principal causa de retrabalho no CAR | Alta | Alta | Demarcação sugerida pré-carregada + validações em tempo real (área, município, self-intersection) + Carla guiando a etapa Geo | Revisão manual para geometrias com alertas de sobreposição |
| R-14 | Responsabilidade administrativa em decisão baseada em IA | Média | Alta | Dossiê IA como apoio, não substituto; campo de observações obrigatório para analista | Revisão jurídica do fluxo de aprovação antes do piloto em órgão público |
| R-15 | Falso-positivo geoespacial na sugestão de polígono | Média | Média | Sugestão baseada em dados de imóvel já declarados + o usuário sempre confirma ou ajusta antes de salvar | Usuário pode redesenhar manualmente o polígono |
| R-16 | Segurança do histórico de conversa vinculado ao Gov.br | Baixa | Alta | Histórico armazenado sob o mesmo escopo de dados pessoais do cidadão (LGPD); acesso restrito ao próprio usuário | Auditoria de acesso ao histórico + DPO notificado em caso de incidente |

:::warning Riscos de maior atenção
R-01 (Gov.br), R-06 (LGPD), R-11 (API SICAR) e R-13 (geometria) têm impacto alto — monitorar ativamente. R-11 é risco operacional crítico que precisa ser mitigado antes do piloto.
:::
