# CARla — Product Requirements Document

**Versão:** 1.0.0  
**Data:** 2026-06-01  
**Status:** Aprovado

---

## 1. Visão do Produto

O Cadastro Ambiental Rural (CAR) é um instrumento obrigatório da política ambiental brasileira, instituído pela Lei 12.651/2012 (Código Florestal). Sua correta execução é essencial para a regularização ambiental de imóveis rurais em todo o território nacional. Apesar de sua importância, o processo atual de registro e análise é marcado por fricção elevada: produtores rurais com baixo letramento digital enfrentam formulários complexos, exigências documentais pouco claras e nenhum suporte inteligente durante o preenchimento; analistas de órgãos ambientais recebem processos incompletos, dados inconsistentes e acumulam filas crescentes de pendências.

O **CARla** é uma camada de inteligência posicionada sobre o SICAR e os sistemas existentes — não os substituindo, mas potencializando-os. A plataforma oferece atendimento conversacional assistido por IA, validação documental automatizada, geração de dossiês e ferramentas de produtividade para analistas. O resultado esperado é uma experiência radicalmente melhor para o cidadão e uma redução substancial na carga operacional dos servidores públicos.

A arquitetura foi concebida para escalar de uma demonstração em hackathon até um produto real em produção governamental. As decisões técnicas — DDD, event-driven, LLM agnóstico, Anti-Corruption Layer para integrações externas — garantem que o sistema possa evoluir sem reescrita, incorporar novos sistemas (SIGEF, IBAMA, MapBiomas) progressivamente e se adaptar às mudanças regulatórias do CAR.

Do ponto de vista de impacto social, o CARla democratiza o acesso ao processo de regularização ambiental, reduzindo a dependência de intermediários pagos (consultores), acelerando a análise e contribuindo para os compromissos brasileiros de proteção da vegetação nativa e conformidade com o Código Florestal.

---

## 2. Objetivos de Negócio

| # | Objetivo | Métrica de Sucesso | Prazo |
|---|---|---|---|
| OB-01 | Reduzir retrabalho por documentação incompleta | Reduzir em 50% as pendências por documentação faltante | 6 meses pós-MVP |
| OB-02 | Reduzir tempo médio de análise | Reduzir de 30 para 15 dias úteis em média | 6 meses pós-MVP |
| OB-03 | Melhorar experiência do cidadão | NPS ≥ 70, taxa de conclusão de registro ≥ 75% | 3 meses pós-MVP |
| OB-04 | Melhorar qualidade dos dados enviados | Aumentar taxa de aprovação na 1ª tentativa de 40% para 70% | 6 meses pós-MVP |
| OB-05 | Aumentar produtividade dos analistas | Aumentar de 5 para 10 processos analisados/analista/dia | 6 meses pós-MVP |
| OB-06 | Automatizar tarefas repetitivas | 80% das validações documentais executadas sem intervenção humana | 12 meses pós-MVP |

---

## 3. Personas

### P1 — João Silva | Produtor Rural

**Perfil:** 52 anos, agricultor familiar, 3º grau incompleto, mora no interior do Maranhão. Possui propriedade de 50 hectares herdada do pai. Usa smartphone Android básico. Tem dificuldade com interfaces digitais complexas. Já tentou fazer o CAR duas vezes e desistiu.

**Objetivos:**
- Regularizar a propriedade para poder acessar crédito rural (exigência do banco)
- Entender o que precisa trazer sem precisar contratar consultor
- Concluir o processo sem precisar ir à cidade várias vezes

**Frustrações:**
- Formulários com jargão técnico incompreensível ("módulo fiscal", "área de preservação permanente")
- Não sabe quais documentos precisa reunir antes de começar
- Não recebe feedback quando algo está errado
- Atendimento presencial só disponível na capital

**Jobs-to-be-done:**
- Descobrir o que precisa antes de começar
- Ser guiado passo a passo durante o preenchimento
- Saber exatamente o que está faltando quando há pendência
- Acompanhar o status do processo de casa

**Critérios de satisfação:**
- Conseguir iniciar e completar o processo sem ajuda presencial
- Receber orientações claras em linguagem simples
- Ser notificado por WhatsApp ou SMS sobre mudanças de status

---

### P2 — Ana Costa | Consultora Ambiental

**Perfil:** 35 anos, engenheira florestal, Brasília-DF. Gerencia carteira de 200+ processos CAR de clientes (médios e grandes proprietários rurais). Usa notebook, tem bom domínio tecnológico. Precisa de eficiência — tempo é dinheiro.

**Objetivos:**
- Submeter processos corretos de primeira (evitar idas e vindas)
- Acompanhar status de todos os clientes de um único painel
- Receber alertas antecipados sobre possíveis inconsistências

**Frustrações:**
- Precisa checar status individualmente no SICAR para cada cliente
- Não tem visibilidade de qual documento específico está causando pendência
- Tempo perdido em pendências por questões documentais óbvias

**Jobs-to-be-done:**
- Pré-validar documentos antes de submeter
- Ter visibilidade consolidada dos processos dos clientes
- Receber alertas automáticos de pendências

**Critérios de satisfação:**
- Dashboard com status de todos os processos gerenciados
- Notificação automática por email ao surgir pendência
- Taxa de aprovação na 1ª tentativa > 90%

---

### P3 — Carlos Mendes | Analista de Órgão Ambiental

**Perfil:** 40 anos, técnico ambiental, servidor do SEMA-MT. Responsável por 300+ processos na fila. Trabalha com sistema legado lento. Acumula horas extras para dar conta do volume.

**Objetivos:**
- Analisar mais processos por dia sem aumentar carga de trabalho
- Identificar rapidamente quais processos têm problemas antes de abrir
- Focar tempo em análise técnica, não em conferência manual de documentos

**Frustrações:**
- Abre processo e descobre que falta documento básico que poderia ter sido verificado antes
- Não tem visão geoespacial integrada para verificar sobreposições
- Dossiê do processo precisa ser montado manualmente

**Jobs-to-be-done:**
- Triagem inteligente da fila por prioridade e completude
- Dossiê pré-montado com todos os dados do processo
- Integração com dados geoespaciais para verificação de sobreposições

**Critérios de satisfação:**
- Redução de 50% no tempo de análise por processo
- Dossiê completo gerado automaticamente em < 30 segundos
- Score de completude e risco visível antes de abrir o processo

---

### P4 — Maria Santos | Administradora do Sistema

**Perfil:** 38 anos, analista de TI, lotada na SEMAD estadual. Responsável pela operação da plataforma. Faz triagem de problemas, gerencia usuários e monitora disponibilidade.

**Objetivos:**
- Manter o sistema funcionando com alta disponibilidade
- Ter visibilidade de erros e gargalos antes que afetem usuários
- Gerenciar configurações sem precisar de deploy (ex: trocar provider de IA)

**Frustrações:**
- Não tem painéis de monitoramento em tempo real
- Configurações técnicas exigem deploy para alterar
- Dificuldade em rastrear causa de erros relatados por usuários

**Jobs-to-be-done:**
- Dashboard operacional em tempo real
- Gerenciamento de usuários e permissões via interface
- Logs de auditoria pesquisáveis

**Critérios de satisfação:**
- Uptime ≥ 99.5%
- Alertas automáticos para degradação de performance
- Capacidade de trocar configurações sem deploy

---

## 4. Casos de Uso Principais

### UC-001 — Iniciar Registro CAR com Assistência Inteligente

**Ator principal:** Produtor Rural, Consultor Ambiental  
**Pré-condições:** Usuário autenticado via Gov.br (nível mínimo: prata)  
**Fluxo principal:**
1. Usuário acessa "Novo Processo"
2. Sistema apresenta stepper com etapas do processo
3. Assistente IA inicia conversa de boas-vindas e solicita dados básicos do imóvel
4. Usuário preenche: nome do imóvel, município, estado
5. Sistema valida o município via código IBGE
6. Sistema cria processo no status "rascunho" e orienta próximos passos
7. Assistente apresenta lista de documentos necessários para o tipo de imóvel

**Fluxos alternativos:**
- 4a: Município não encontrado → assistente sugere municípios similares
- 4b: Usuário já tem processo em andamento → sistema alerta e oferece retomar

**Pós-condições:** Processo criado em status "rascunho", usuário orientado sobre próximos passos

---

### UC-002 — Upload e Validação Automática de Documentos

**Ator principal:** Produtor Rural, Consultor Ambiental  
**Pré-condições:** Processo em status "em_preenchimento"  
**Fluxo principal:**
1. Usuário acessa aba "Documentos" do processo
2. Sistema exibe lista de documentos necessários com status (pendente/enviado/validado)
3. Usuário seleciona tipo de documento e faz upload do arquivo (PDF, JPG, PNG, até 50MB)
4. Sistema armazena no object storage e retorna confirmação imediata (202 Accepted)
5. Worker de OCR processa o documento assincronamente
6. Sistema extrai dados estruturados e valida consistência
7. Usuário recebe notificação (in-app + email) com resultado da validação
8. Documentos válidos aparecem marcados com ✓; inválidos com descrição do erro

**Fluxos alternativos:**
- 6a: OCR não consegue extrair dados (imagem com baixa qualidade) → notificação solicitando reenvio com foto/scan melhor
- 6b: Dados extraídos divergem dos informados no formulário → pendência automática com explicação

**Pós-condições:** Documento processado, status de completude do processo atualizado

---

### UC-003 — Consulta Conversacional de Dúvidas sobre CAR

**Ator principal:** Qualquer usuário autenticado  
**Pré-condições:** Usuário autenticado  
**Fluxo principal:**
1. Usuário acessa o Assistente CAR
2. Digita pergunta em linguagem natural: "O que é área de preservação permanente?"
3. Sistema classifica a intenção (dúvida conceitual, dúvida de processo, solicitação de documento)
4. Sistema busca resposta na base de conhecimento via RAG (normativos CAR, FAQ, manuais)
5. LLM gera resposta em linguagem simples com base nos documentos recuperados
6. Resposta é exibida via streaming (token a token) com indicação das fontes
7. Usuário pode fazer perguntas de acompanhamento no contexto da mesma conversa

**Fluxos alternativos:**
- 4a: Pergunta fora do domínio CAR → sistema informa que só responde sobre CAR e sugere canais
- 4b: LLM indisponível → mensagem de indisponibilidade temporária, sistema continua funcionando

**Pós-condições:** Dúvida respondida, feedback de utilidade coletado

---

### UC-004 — Acompanhamento de Status do Processo

**Ator principal:** Produtor Rural, Consultor Ambiental  
**Fluxo principal:**
1. Usuário acessa dashboard "Meus Processos"
2. Sistema exibe lista com: número CAR, status atual, última atualização, score de completude
3. Usuário clica em processo para ver detalhes
4. Sistema exibe: linha do tempo completa, documentos enviados, pendências abertas, prazo de análise

**Pós-condições:** Usuário informado sobre estado atual do processo

---

### UC-005 — Triagem Automática de Processos pelo Analista

**Ator principal:** Analista Ambiental  
**Fluxo principal:**
1. Analista acessa portal do analista
2. Sistema exibe fila de processos ordenada por: prioridade calculada, tempo na fila, score de completude
3. Para cada processo: exibe status, município, área total, tipo de imóvel, score de risco, pendências abertas
4. Analista filtra por: status, município, analista responsável, prioridade
5. Analista assume processo clicando em "Iniciar Análise"
6. Sistema gera dossiê automático com: dados do processo, documentos validados, cruzamentos externos, alertas

**Pós-condições:** Processo em análise, dossiê disponível para o analista

---

### UC-006 — Geração Automática de Dossiê do Processo

**Ator principal:** Sistema (trigger automático), Analista  
**Fluxo principal:**
1. Analista acessa processo e clica em "Gerar Dossiê"
2. Sistema inicia geração assíncrona (job em background)
3. LLM consolida: dados do imóvel, documentos validados e seus dados extraídos, pendências históricas, dados de integrações externas (SICAR, IBAMA), análise geoespacial
4. Sistema gera PDF estruturado com: resumo executivo, dados do requerente, dados do imóvel, análise documental, mapa com geometria, alertas e inconsistências identificadas
5. Analista recebe notificação e pode baixar o PDF

**Pós-condições:** Dossiê PDF disponível para download

---

### UC-007 — Notificação de Pendências ao Cidadão

**Ator principal:** Sistema (automático), Analista  
**Fluxo principal:**
1. Analista identifica pendência e cria registro com: tipo, título, descrição detalhada, prazo
2. Sistema salva a pendência e publica evento PendênciaIdentificada
3. Worker de notificação processa o evento
4. Sistema envia: notificação in-app, email com descrição da pendência e link direto para correção
5. Cidadão acessa o processo e vê pendência destacada com instruções claras
6. Assistente IA pode explicar a pendência se o cidadão não entender

**Pós-condições:** Cidadão notificado, pendência visível no portal

---

### UC-008 — Aprovação/Rejeição pelo Analista

**Ator principal:** Analista Ambiental  
**Pré-condições:** Processo em status "em_analise"  
**Fluxo principal (aprovação):**
1. Analista conclui análise e clica em "Aprovar"
2. Sistema valida: processo em status correto, analista é o responsável
3. Analista confirma com observações opcionais
4. Sistema muda status para "aprovado", registra no histórico, gera número CAR oficial
5. Sistema notifica o cidadão por email e in-app
6. Cidadão pode baixar o comprovante de registro CAR

**Fluxo alternativo (rejeição):**
1. Analista clica em "Rejeitar"
2. Sistema exige: motivo obrigatório + código de motivo padronizado
3. Sistema muda status para "rejeitado", registra, notifica cidadão
4. Cidadão pode interpor recurso em até 30 dias

**Pós-condições:** Processo concluído, cidadão notificado, registro no histórico imutável

---

### UC-009 — Correção de Inconsistências Guiada por IA

**Ator principal:** Produtor Rural, Consultor  
**Pré-condições:** Processo em status "pendente" com pendências abertas  
**Fluxo principal:**
1. Cidadão acessa pendência no portal
2. Sistema exibe descrição da pendência com linguagem clara
3. Cidadão pode perguntar ao assistente: "O que devo fazer para resolver a pendência X?"
4. Assistente analisa o contexto da pendência e orienta: qual documento enviar, como fotografar, o que o documento deve conter
5. Cidadão envia novo documento ou complementação
6. Sistema revalida automaticamente
7. Se válido: pendência marcada como resolvida, analista notificado

**Pós-condições:** Pendência resolvida, processo retorna para análise

---

### UC-010 — Atendimento via WhatsApp com Vinculação Gov.br

**Ator principal:** Produtor Rural, Consultor Ambiental  
**Pré-condições:** Usuário possui conta ativa no WhatsApp  
**Fluxo principal:**
1. Cidadão envia mensagem para o número oficial do CARla no WhatsApp
2. Bot identifica que o número não está vinculado a uma conta Gov.br
3. Bot envia link curto de vinculação com token temporário (TTL 10 min): `carla.gov.br/auth/wpp?token=XYZ`
4. Cidadão clica no link, abre no browser do celular
5. Sistema redireciona para Gov.br (OAuth2 Authorization Code + PKCE)
6. Cidadão autentica com CPF e senha Gov.br
7. Gov.br retorna callback com token e claims (CPF, nome, nível de confiabilidade)
8. Sistema cria ou recupera o usuário, vincula o número WhatsApp ao `user_id`
9. Browser exibe confirmação: "Número vinculado com sucesso. Volte ao WhatsApp."
10. Bot no WhatsApp detecta a vinculação e continua o atendimento identificado

**Fluxos alternativos:**
- 3a: Usuário já vinculado → bot segue direto para o atendimento
- 6a: Token expirado → bot envia novo link automaticamente
- 8a: Gov.br indisponível → bot informa indisponibilidade e oferece acesso pelo portal web

**Pós-condições:** Número WhatsApp vinculado ao user_id por 30 dias; usuário atendido com contexto personalizado

---

### UC-011 — Consulta de Status do Processo via WhatsApp

**Ator principal:** Produtor Rural  
**Pré-condições:** Número WhatsApp vinculado ao Gov.br  
**Fluxo principal:**
1. Cidadão envia "qual o status do meu processo?" no WhatsApp
2. Bot identifica intenção de consulta de status
3. Bot busca processos ativos do usuário
4. Bot responde com resumo: status atual, etapa, pendências abertas e próximo passo

**Pós-condições:** Cidadão informado sem precisar acessar o portal web

---

### UC-012 — Notificação Proativa de Pendência via WhatsApp

**Ator principal:** Sistema (automático)  
**Pré-condições:** Usuário com número WhatsApp vinculado e processo com nova pendência  
**Fluxo principal:**
1. Analista cria pendência ou sistema detecta inconsistência documental
2. Worker de notificações verifica canais preferidos do usuário
3. Sistema envia mensagem WhatsApp com: descrição da pendência, prazo e link direto para correção no portal

**Pós-condições:** Cidadão notificado em tempo real no canal que já usa no dia a dia

---

### UC-013 — Relatório de Conformidade e Analytics

**Ator principal:** Administrador, Supervisor  
**Fluxo principal:**
1. Admin acessa área de relatórios
2. Seleciona período, estado, tipo de relatório
3. Sistema gera relatório com: processos por status, tempo médio de análise, taxa de aprovação, produtividade por analista, documentos mais problemáticos, municípios com maior volume

**Pós-condições:** Relatório disponível para download (PDF/Excel)

---

## 5. Requisitos Funcionais

### Portal do Cidadão

| ID | Título | Descrição | Prioridade |
|---|---|---|---|
| RF-001 | Autenticação Gov.br | Login via OAuth2/OIDC com Gov.br, suporte a níveis bronze/prata/ouro | Must |
| RF-002 | Perfil do usuário | Visualizar e atualizar dados pessoais, vincular CPF validado | Must |
| RF-003 | Criar processo CAR | Iniciar novo processo com dados básicos do imóvel | Must |
| RF-004 | Stepper de preenchimento | Formulário dividido em etapas com progresso visual | Must |
| RF-005 | Upload de documentos | Upload de PDF/imagem com validação de tipo e tamanho | Must |
| RF-006 | Acompanhamento de status | Dashboard com lista de processos e status em tempo real | Must |
| RF-007 | Linha do tempo do processo | Histórico cronológico de todas as mudanças de status | Should |
| RF-008 | Visualização de pendências | Lista de pendências com descrição clara e prazo | Must |
| RF-009 | Resposta a pendências | Envio de documentos complementares para resolver pendências | Must |
| RF-010 | Notificações | Notificações in-app e email para eventos do processo | Should |
| RF-010a | Canal WhatsApp | Atendimento conversacional via WhatsApp Business API com autenticação vinculada | Should |
| RF-010b | Vinculação WhatsApp-Gov.br | Fluxo de link temporário para autenticar número WhatsApp via OAuth2 Gov.br | Should |
| RF-010c | Notificação WhatsApp proativa | Envio de alertas de pendência e status por WhatsApp para usuários vinculados | Should |

### Assistente Inteligente

| ID | Título | Descrição | Prioridade |
|---|---|---|---|
| RF-011 | Chat conversacional | Interface de chat com streaming de respostas do LLM | Must |
| RF-012 | Base de conhecimento CAR | RAG com normativos, manuais e FAQ do CAR/SICAR | Must |
| RF-013 | Classificação de intenção | Identificar se é dúvida, solicitação de doc, consulta de status | Should |
| RF-014 | Contexto do processo | Assistente acessa dados do processo do usuário para respostas personalizadas | Should |
| RF-015 | Solicitação de documentos | Assistente pode iniciar fluxo de upload de documento específico | Could |
| RF-016 | Escalonamento humano | Detectar quando não consegue responder e encaminhar para analista | Should |
| RF-017 | Histórico de conversas | Usuário pode acessar conversas anteriores | Could |
| RF-017a | Sessão WhatsApp contextual | Bot mantém contexto da conversa e do processo ativo durante a sessão | Should |
| RF-017b | Escalona para portal | Bot direciona operações críticas (submissão, correção) para o portal web com link direto | Must |

### Motor de Validação

| ID | Título | Descrição | Prioridade |
|---|---|---|---|
| RF-018 | OCR de documentos | Extração de texto de PDFs e imagens via OCR | Must |
| RF-019 | Extração estruturada | Identificar campos específicos por tipo de documento (matrícula, CCIR, etc.) | Must |
| RF-020 | Validação de consistência | Comparar dados extraídos com dados declarados no formulário | Must |
| RF-021 | Cruzamento de dados | Verificar dados contra bases externas (IBGE, SICAR) | Should |
| RF-022 | Geração de pendência automática | Criar pendência automaticamente quando inconsistência detectada | Must |
| RF-023 | Retry de OCR | Reprocessar documento com qualidade inadequada após reenvio | Should |

### Portal do Analista

| ID | Título | Descrição | Prioridade |
|---|---|---|---|
| RF-024 | Fila de processos | Lista de processos com filtros avançados e ordenação por prioridade | Must |
| RF-025 | Visão completa do processo | Tela unificada com todos os dados, documentos e histórico | Must |
| RF-026 | Geração de dossiê | Geração automática de PDF com resumo do processo via IA | Should |
| RF-027 | Aprovação/rejeição | Aprovar ou rejeitar processo com motivo obrigatório | Must |
| RF-028 | Criar pendência | Criar pendência manual com descrição e prazo | Must |
| RF-029 | Dashboard de produtividade | Métricas de processos analisados, tempo médio, por período | Should |
| RF-030 | Comunicação com cidadão | Canal de mensagens vinculado ao processo | Could |

---

## 6. Requisitos Não Funcionais

| ID | Categoria | Requisito | Métrica |
|---|---|---|---|
| RNF-001 | Performance | Tempo de resposta da API (p95) | < 500ms para endpoints síncronos |
| RNF-002 | Performance | Tempo de resposta do assistente IA (1º token) | < 2 segundos |
| RNF-003 | Performance | Tempo de processamento OCR | < 60 segundos por documento |
| RNF-004 | Performance | Geração de dossiê PDF | < 30 segundos |
| RNF-005 | Disponibilidade | SLA do sistema | 99.5% (excluindo janelas de manutenção) |
| RNF-006 | Disponibilidade | RTO (Recovery Time Objective) | < 4 horas |
| RNF-007 | Disponibilidade | RPO (Recovery Point Objective) | < 1 hora |
| RNF-008 | Escalabilidade | Usuários simultâneos suportados | 500 (MVP), 5.000 (v1), 50.000 (v2) |
| RNF-009 | Escalabilidade | Processos processados por dia | 1.000 (MVP), 10.000 (v2) |
| RNF-010 | Segurança | Autenticação | OAuth2/OIDC + JWT RS256 |
| RNF-011 | Segurança | Criptografia em repouso | AES-256 para documentos, pgcrypto para CPF/email |
| RNF-012 | Segurança | Criptografia em trânsito | TLS 1.3 obrigatório |
| RNF-013 | Conformidade | LGPD | 100% conforme — dados pessoais protegidos, direitos dos titulares suportados |
| RNF-014 | Acessibilidade | Padrão | WCAG 2.1 nível AA |
| RNF-015 | Compatibilidade | Browsers suportados | Chrome 90+, Firefox 90+, Safari 14+, Edge 90+ |
| RNF-016 | Auditabilidade | Logs de auditoria | 100% das operações de escrita registradas, retenção 5 anos |
| RNF-017 | Manutenibilidade | Cobertura de testes | ≥ 80% (unitários + integração) |
| RNF-018 | Internacionalização | Idioma padrão | Português brasileiro (pt-BR) |
| RNF-019 | Observabilidade | Instrumentação | OpenTelemetry, Prometheus, Grafana |
| RNF-020 | Portabilidade | Containerização | Docker + Kubernetes, sem vendor lock-in de cloud |

---

## 7. Premissas e Restrições

### Premissas
1. O SICAR continuará existindo como sistema oficial e o CARla se integra a ele, não o substitui
2. O Gov.br estará disponível como Identity Provider com SLA adequado
3. Os usuários terão acesso a smartphone ou computador com internet
4. Os documentos enviados estarão em formatos digitalizáveis (PDF, JPG, PNG)
5. A legislação do CAR (Lei 12.651/2012 e normativas SICAR) permanecerá estável durante o desenvolvimento
6. O sistema será implantado em infraestrutura gerenciada pelo órgão ambiental ou cloud pública
7. Haverá equipe técnica para operar e manter o sistema em produção
8. As integrações com SIGEF, INCRA, IBAMA serão desenvolvidas progressivamente

### Restrições
1. O sistema NÃO pode substituir o número CAR oficial — este deve ser gerado pelo SICAR
2. O sistema DEVE estar em conformidade com a LGPD (Lei 13.709/2018)
3. Todo dado de caráter geoespacial deve usar SRID 4674 (SIRGAS 2000), padrão brasileiro
4. O sistema deve operar sem depender de APIs externas indisponíveis (resiliência com fallback)
5. O budget de tokens de LLM deve ser controlado (dados sensíveis não podem ir para LLMs na nuvem sem mascaramento)
6. A interface deve ser acessível por usuários com baixo letramento digital

---

## 8. Dependências Externas

| Sistema | Propósito | Disponibilidade de API | Estratégia |
|---|---|---|---|
| Gov.br | Autenticação e identificação do cidadão | API pública OIDC disponível | Integração direta; fallback de emergência para manutenção |
| SICAR | Consulta de registros CAR existentes, submissão final | API parcialmente disponível (consulta pública) | Adapter com cache agressivo; mock para dev |
| SIGEF | Verificação de georreferenciamento INCRA | API REST disponível (dados públicos) | Anti-Corruption Layer; opcional no MVP |
| INCRA | Consulta de módulos fiscais e CCIR | Dados públicos, API limitada | CSV/shapefile público como fallback |
| IBAMA | Alertas de embargo e infrações ambientais | API pública limitada | Consulta por CPF/CNPJ; cache 24h |
| MapBiomas | Dados de uso e cobertura do solo | API REST disponível | Enrichment do processo; opcional no MVP |
| TerraBrasilis | Dados PRODES/DETER de desmatamento | API REST INPE disponível | Score de risco do imóvel; fase 2 |
| DETER | Alertas de desmatamento em tempo real | API INPE pública | Score de risco; fase 2 |
| PRODES | Dados anuais de desmatamento | API INPE pública | Histórico do imóvel; fase 2 |
| ICMBio | Unidades de Conservação | API REST disponível | Verificação de sobreposição; fase 2 |
| FUNAI | Terras indígenas | Shapefile público | Verificação de sobreposição; fase 2 |

---

## 9. Métricas de Sucesso (KPIs)

### Adoção
- MAU (Usuários Ativos Mensais): ≥ 500 no mês 3, ≥ 5.000 no mês 12
- Taxa de conclusão de registro: ≥ 75% dos processos iniciados são submetidos
- Taxa de retenção: ≥ 60% dos usuários retornam após pendência

### Qualidade dos Dados
- Taxa de aprovação na 1ª tentativa: ≥ 70% (vs ~40% atual estimado)
- Redução de pendências por documentação: ≥ 50%
- Precisão do OCR: ≥ 90% de acurácia na extração de campos obrigatórios

### Eficiência Operacional
- Tempo médio de análise: ≤ 15 dias úteis (vs ~30 dias estimados atualmente)
- Processos analisados por analista/dia: ≥ 10 (vs ~5 atualmente)
- % de validações documentais automáticas: ≥ 80%

### Satisfação
- NPS do cidadão: ≥ 70
- CSAT do analista: ≥ 4.0/5.0
- Taxa de uso do assistente IA: ≥ 40% dos usuários por mês

### Técnico
- Uptime: ≥ 99.5%
- Latência p99 da API: < 2 segundos
- Taxa de erro HTTP 5xx: < 0.1%
- Cobertura de testes: ≥ 80%

---

## 10. Riscos e Mitigações

| ID | Risco | Prob. | Impacto | Mitigação | Contingência |
|---|---|---|---|---|---|
| R-01 | Indisponibilidade do Gov.br | M | A | Circuit breaker + monitoramento de SLA | Modo de manutenção com autenticação temporária |
| R-02 | Mudança na API do SICAR | M | A | Anti-Corruption Layer isola impacto | Stub configurável para operação desacoplada |
| R-03 | Qualidade ruim de documentos enviados (fotos escuras) | A | M | OCR com múltiplos engines + instruções de upload | Revisão manual para documentos com baixa confiança |
| R-04 | Adoção baixa por baixo letramento digital | M | A | UX simples + assistente IA + tutoriais em vídeo | Parceria com extensão rural (EMATER) para onboarding |
| R-05 | Custo elevado de LLM em escala | M | M | Cache de respostas + Ollama local para consultas frequentes | Limitar tokens por sessão + plano de custos |
| R-06 | Violação de LGPD | B | A | PII masking, criptografia, auditoria, DPO | Plano de resposta a incidentes, comunicação ANPD |
| R-07 | Escalabilidade insuficiente | B | A | Kubernetes + auto-scaling + testes de carga | Horizontal scaling na nuvem |
| R-08 | Resistência dos analistas à mudança | M | M | Envolvimento dos analistas no design + treinamento | Programa de adoção gradual com champions |
| R-09 | Legislação CAR sofre alteração | B | M | Arquitetura desacoplada de regras de negócio | Configuração das regras via base de conhecimento (RAG) |
| R-10 | Vazamento de dados geoespaciais sensíveis | B | A | RBAC estrito, sem export público de geometrias individuais | Auditoria imediata, notificação ANPD |

---

## 11. Glossário

| Termo | Definição |
|---|---|
| CAR | Cadastro Ambiental Rural — registro eletrônico obrigatório para imóveis rurais, contendo informações geoespaciais da propriedade e das áreas de vegetação nativa |
| SICAR | Sistema de Cadastro Ambiental Rural — sistema federal que centraliza todos os registros CAR do Brasil |
| SIGEF | Sistema de Gestão Fundiária — sistema INCRA para georreferenciamento de imóveis rurais |
| INCRA | Instituto Nacional de Colonização e Reforma Agrária |
| IBAMA | Instituto Brasileiro do Meio Ambiente e dos Recursos Naturais Renováveis |
| APP | Área de Preservação Permanente — área protegida coberta ou não por vegetação nativa, com função ambiental de preservar recursos hídricos, paisagem, estabilidade geológica e biodiversidade |
| Reserva Legal | Área localizada no interior de uma propriedade rural com cobertura de vegetação nativa. Percentual mínimo varia por bioma: 80% na Amazônia Legal, 35% no Cerrado (Amazônia Legal), 20% nos demais biomas |
| Área Rural Consolidada | Área de imóvel rural com ocupação antrópica preexistente a 22 de julho de 2008 |
| Módulo Fiscal | Unidade de medida agrária que representa a área mínima necessária à subsistência de uma família rural. Varia por município (de 5 a 110 ha) |
| Imóvel Rural | Prédio rústico de área contínua, qualquer que seja a sua localização, que se destine à exploração agrícola, pecuária, extrativa vegetal, florestal ou agroindustrial |
| Número CAR | Código único de identificação do registro no SICAR. Formato: UF-NNNNNNN-NNNNNNNNNNNNNN |
| Protocolo | Número de protocolamento da solicitação, gerado antes do número CAR definitivo |
| Geocodificação | Processo de converter endereço ou coordenadas em representação geoespacial |
| Shapefile | Formato de arquivo geoespacial da ESRI (conjunto de arquivos .shp, .dbf, .shx) para armazenar geometrias e atributos |
| WKT | Well-Known Text — representação textual padronizada de geometrias geoespaciais (ex: POLYGON((lon lat, ...))) |
| GeoJSON | Formato JSON para representação de feições geoespaciais, padrão aberto RFC 7946 |
| SRID | Spatial Reference Identifier — código que identifica o sistema de referência espacial. SRID 4674 = SIRGAS 2000 (padrão brasileiro) |
| PRODES | Projeto de Monitoramento do Desmatamento na Amazônia Legal — dados anuais do INPE |
| DETER | Sistema de Detecção do Desmatamento em Tempo Real — alertas do INPE |
| Embedding | Representação numérica vetorial de texto, usada em busca semântica (RAG) |
| RAG | Retrieval-Augmented Generation — técnica de IA que combina busca em base de conhecimento com geração de texto pelo LLM |
| LGPD | Lei Geral de Proteção de Dados Pessoais (Lei 13.709/2018) |
| DDD | Domain-Driven Design — abordagem de desenvolvimento de software centrada no domínio do negócio |
