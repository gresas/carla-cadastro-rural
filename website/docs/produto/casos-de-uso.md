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

```gherkin
Cenário: Documento válido processado com sucesso
  Dado que João tem processo no status "em_preenchimento"
  Quando fizer upload de CCIR em PDF válido
  Então status do documento muda para "aguardando_ocr"
  E em até 60 segundos muda para "validado"
  E dados extraídos são exibidos para conferência

Cenário: Área declarada diverge do documento
  Quando o OCR identificar área com diferença > 5% em relação ao declarado
  Então documento recebe status "inconsistente"
  E assistente IA indica o campo divergente e orienta correção
```

---

## UC-003 — Consulta Conversacional de Dúvidas

**Fluxo principal:**
1. Usuário digita dúvida no chat (portal ou WhatsApp)
2. Sistema busca chunks relevantes na base de conhecimento (RAG com pgvector)
3. LLM gera resposta embasada nos normativos indexados, com indicação de fonte
4. Resposta exibida em streaming; usuário pode fazer perguntas de acompanhamento
5. Se confiança do RAG for baixa, sistema indica canal de atendimento humano

:::tip Cache semântico
Perguntas frequentes (≥ 95% de similaridade) retornam resposta em cache (Redis TTL 1h) sem chamar o LLM.
:::

```gherkin
Cenário: Dúvida com resposta na base de conhecimento
  Dado que Maria está autenticada no portal
  Quando perguntar "Qual a área mínima de Reserva Legal para pequenas propriedades?"
  Então deve receber resposta com citação do Código Florestal
  E deve ver a fonte: "Lei 12.651/2012, Art. 12"

Cenário: Dúvida fora do escopo do CARla
  Quando perguntar sobre tema não relacionado ao CAR
  Então assistente informa que só pode ajudar com questões do CAR
  E sugere canais oficiais do IBAMA/órgão estadual
```

---

## UC-004 — Acompanhamento de Status do Processo

**Fluxo principal:**
1. Usuário acessa "Meus Processos" no portal ou envia mensagem ao bot do WhatsApp
2. Sistema retorna lista de processos com status atual e data da última atualização
3. Ao selecionar um processo, exibe timeline completo de eventos
4. Se houver pendência aberta, exibe o motivo e o prazo para correção
5. Se aprovado, exibe comprovante e orientações sobre o Certificado CAR oficial no SICAR

```gherkin
Cenário: Processo com pendência aberta
  Dado que João tem processo no status "pendente"
  Quando acessar "Meus Processos"
  Então deve ver status "pendente" com motivo e prazo
  E botão "Responder Pendência" deve estar visível

Cenário: Processo aprovado com PRA
  Dado que processo de João foi aprovado com PRA
  Quando acessar detalhes do processo
  Então deve ver status "aprovado_com_pra"
  E deve ver orientação sobre obrigação de adesão ao PRA
  E deve ver prazo para adesão e link para o órgão ambiental estadual
```

---

## UC-005 — Triagem Automática de Processos

**Fluxo principal:**
1. Analista acessa fila de processos no portal analista
2. Sistema exibe processos ordenados por: (1) prioridade urgente, (2) score de risco, (3) tempo na fila
3. Analista pode filtrar por município, estado, tipo de imóvel ou score
4. Analista seleciona processo e clica "Assumir" — status muda para `em_analise`
5. Sistema registra o analista responsável e hora de início

```gherkin
Cenário: Analista assume processo de alta prioridade
  Dado que existem 15 processos na fila com diferentes scores de risco
  Quando o analista Ana acessar a fila
  Então processos com score de risco > 7 devem aparecer no topo
  E ao clicar "Assumir", status muda para "em_analise"
  E processo some da fila disponível de outros analistas

Cenário: Filtro por município
  Quando Ana filtrar a fila pelo município "Santarém/PA"
  Então deve ver apenas processos daquele município
  E contador de resultados deve refletir o filtro aplicado
```

---

## UC-006 — Geração Automática de Dossiê

**Fluxo principal:**
1. Analista assume o processo (UC-005); geração de dossiê inicia automaticamente
2. Sistema coleta: dados do imóvel, documentos validados, alertas IBAMA/DETER, histórico de pendências
3. LLM (Claude) gera resumo executivo em linguagem técnica
4. Dossiê PDF é montado e disponibilizado em até 30 segundos
5. Analista revisa dossiê antes de tomar decisão

:::caution Dossiê é apoio, não substituto
O dossiê gerado por IA é suporte à decisão. A motivação do ato administrativo (aprovação/rejeição) deve ser do próprio servidor. Ver [Fluxo do Analista](../design/fluxos/analista.md).
:::

```gherkin
Cenário: Dossiê gerado com sucesso
  Dado que Ana assumiu o processo de João
  Quando o sistema iniciar a geração do dossiê
  Então em até 30 segundos deve estar disponível para download
  E deve conter: resumo executivo, mapa do imóvel, alertas externos e análise documental

Cenário: Falha na geração do dossiê
  Quando o serviço de IA estiver indisponível
  Então Ana deve ver aviso de que o dossiê não pôde ser gerado
  E deve poder prosseguir a análise sem o dossiê
```

---

## UC-007 — Notificação de Pendências ao Cidadão

**Fluxo principal:**
1. Analista cria pendência com motivo e prazo (padrão: 15 dias úteis)
2. Sistema gera notificação em linguagem acessível a partir do template selecionado
3. Notificação enviada por email e WhatsApp (se número vinculado)
4. Cidadão recebe mensagem com: o que precisa corrigir, prazo e link direto ao processo
5. Sistema registra envio e atualiza status do processo para `pendente`

```gherkin
Cenário: Notificação enviada por ambos os canais
  Dado que João tem email e WhatsApp vinculados
  Quando analista criar pendência "Planta de localização ausente"
  Então João deve receber email com detalhes da pendência
  E deve receber mensagem WhatsApp com link direto ao processo
  E prazo de 15 dias úteis deve aparecer em ambos os canais

Cenário: Usuário sem WhatsApp vinculado
  Dado que João não vinculou WhatsApp
  Quando analista criar pendência
  Então João recebe apenas email
  E sistema registra tentativa de WhatsApp como "não enviado — número não vinculado"
```

---

## UC-008 — Aprovação ou Rejeição pelo Analista

**Fluxo principal:**
1. Analista revisa dossiê e documentos do processo (UC-006)
2. Analista clica em "Aprovar", "Aprovar com PRA" ou "Rejeitar"
3. Para qualquer decisão, campo de observações é obrigatório
4. Sistema registra decisão, gera comprovante interno e notifica o cidadão
5. Status do processo muda para `aprovado`, `aprovado_com_pra` ou `rejeitado`

:::warning Certificado CAR oficial
O comprovante gerado pelo CARla é interno. O Certificado CAR com validade jurídica plena é emitido pelo SICAR. Até a integração SICAR (Fase 3), orientar o cidadão a acessar o SICAR diretamente.
:::

```gherkin
Cenário: Aprovação direta
  Dado que Ana revisou o processo e está dentro das conformidades
  Quando clicar "Aprovar" e preencher observações
  Então status muda para "aprovado"
  E cidadão recebe notificação com comprovante interno
  E registro de auditoria é criado com ID do analista e timestamp

Cenário: Aprovação com PRA
  Dado que o processo tem déficit de Reserva Legal declarado
  Quando Ana clicar "Aprovar com PRA" e descrever a obrigação de recuperação
  Então status muda para "aprovado_com_pra"
  E cidadão recebe notificação com orientação sobre adesão ao PRA
  E sistema agenda lembrete automático 30 dias antes do prazo de adesão

Cenário: Rejeição com motivo
  Quando Ana clicar "Rejeitar" com motivo obrigatório preenchido
  Então status muda para "rejeitado"
  E cidadão recebe notificação com motivo e prazo de recurso
```

---

## UC-009 — Correção de Inconsistências Guiada por IA

**Fluxo principal:**
1. Cidadão acessa processo com pendência e lê o motivo
2. Assistente IA explica a inconsistência em linguagem acessível e orienta o que corrigir
3. Cidadão faz as correções (reedita dados ou faz novo upload de documento)
4. Sistema revalida automaticamente os documentos corrigidos
5. Processo retorna para fila do analista com status `em_correcao` → `em_analise`

```gherkin
Cenário: Cidadão corrige dado divergente
  Dado que João recebeu pendência "Área total diverge do CCIR em 8%"
  Quando acessar a pendência no portal
  Então assistente deve explicar qual campo está divergente e como corrigir
  E João deve poder editar a área declarada ou fazer novo upload do CCIR

Cenário: Documento resubmetido dentro do prazo
  Quando João fizer upload de documento corrigido dentro do prazo
  Então status muda para "em_correcao"
  E analista recebe notificação de que correção foi submetida
  E processo volta para fila de análise

Cenário: Prazo de correção vencido sem resposta
  Dado que prazo da pendência venceu sem ação do cidadão
  Então sistema marca pendência como "vencida"
  E notifica analista responsável para decisão (arquivar ou estender prazo)
```

---

## UC-010 — Vinculação WhatsApp via Gov.br

Este caso de uso resolve o desafio de autenticar um usuário do WhatsApp sem que o canal suporte OAuth2 diretamente.

**Fluxo:**
1. Usuário envia mensagem ao número oficial do CARla no WhatsApp
2. Bot detecta número não vinculado e envia link temporário (30 min): `carla.gov.br/auth/wpp?token=XYZ`
3. Usuário clica, abre no browser, autentica com Gov.br
4. Sistema vincula número WhatsApp ao CPF autenticado (válido por 30 dias)
5. Bot retoma atendimento já identificado

```gherkin
Cenário: Primeira mensagem de número não vinculado
  Dado que o número "+5511999998888" não está vinculado
  Quando enviar qualquer mensagem ao CARla
  Então bot envia link de vinculação com TTL de 30 minutos

Cenário: Token de vinculação expirado
  Dado que o usuário não acessou o link em 30 minutos
  Quando tentar acessar o link expirado
  Então deve ver mensagem de expiração
  E bot envia novo link automaticamente
```

:::caution Operações críticas permanecem no portal web
Submissão de processos e upload de documentos **não são feitos pelo WhatsApp** — exigem o portal web por serem atos jurídicos formais.
:::

---

## UC-011 — Consulta de Status via WhatsApp

**Fluxo principal:**
1. Usuário vinculado envia mensagem perguntando sobre o status do processo
2. Bot identifica CPF vinculado ao número e recupera processo(s) ativo(s)
3. Bot responde com status atual em linguagem natural, com emoji de status
4. Se houver pendência, exibe motivo resumido e prazo
5. Se houver mais de um processo, lista todos e aguarda o usuário escolher

```gherkin
Cenário: Consulta de processo único
  Dado que João está vinculado e tem um processo ativo
  Quando enviar "Qual o status do meu CAR?"
  Então bot responde com: número de protocolo, status atual e data da última atualização

Cenário: Processo com pendência ativa
  Dado que o processo de João está "pendente"
  Quando consultar o status
  Então bot deve informar o motivo resumido da pendência e o prazo restante
  E deve enviar link direto para o portal para responder a pendência

Cenário: Usuário com múltiplos processos
  Dado que Maria tem dois processos ativos
  Quando perguntar sobre o status
  Então bot lista os dois processos com seus protocolos e status
  E pergunta qual deles Maria quer mais detalhes
```

---

## UC-012 — Notificação Proativa via WhatsApp

**Fluxo principal:**
1. Sistema detecta evento relevante (pendência criada, aprovação, lembrete de prazo)
2. Sistema verifica se o cidadão tem WhatsApp vinculado e sessão ativa
3. Mensagem proativa enviada via Meta Cloud API com Template Message aprovado
4. Cidadão recebe notificação sem precisar iniciar conversa

:::note Template Messages
Notificações proativas no WhatsApp exigem Template Messages pré-aprovados pelo Meta. Mensagens livres só são permitidas dentro de janela de 24h após o usuário enviar a última mensagem.
:::

```gherkin
Cenário: Notificação de aprovação
  Dado que processo de João foi aprovado
  E João tem WhatsApp vinculado
  Quando sistema processar evento "ProcessoAprovado"
  Então João deve receber mensagem WhatsApp com: número de protocolo, status "✅ Aprovado" e link ao portal

Cenário: Lembrete de prazo PRA
  Dado que prazo de adesão ao PRA vence em 30 dias
  Quando job agendado executar
  Então cidadão recebe mensagem alertando sobre o prazo
  E orientação de como aderir ao PRA junto ao órgão estadual

Cenário: Número não vinculado
  Dado que o cidadão não tem WhatsApp vinculado
  Quando sistema tentar enviar notificação proativa
  Então notificação é enviada apenas por email
  E registro de "WhatsApp não enviado" é criado para auditoria
```

---

## UC-013 — Relatório de Conformidade e Analytics

**Fluxo principal:**
1. Admin ou supervisor acessa o portal administrativo
2. Seleciona período, estado/município e tipo de relatório
3. Sistema agrega dados anonimizados do período selecionado
4. Dashboard exibe: volume de processos, tempo médio de análise, taxa de aprovação, top pendências
5. Relatório pode ser exportado em CSV ou PDF

```gherkin
Cenário: Dashboard mensal por estado
  Dado que supervisor estadual está autenticado
  Quando acessar "Analytics" e selecionar o mês atual
  Então deve ver: total de processos submetidos, aprovados, rejeitados e pendentes
  E tempo médio de análise e NPS do período

Cenário: Exportação de dados
  Quando clicar "Exportar CSV"
  Então deve baixar arquivo com dados anonimizados do período
  E nenhum CPF ou dado pessoal identificável deve constar no arquivo

Cenário: Acesso negado a analista comum
  Dado que usuário com role "analista" tenta acessar Analytics
  Então deve receber erro 403
  E ser redirecionado ao portal de processos
```

---

## Ver também

- [Requisitos Funcionais](./requisitos.md) — RFs derivados destes UCs
- [Fluxo do Cidadão](../design/fluxos/cidadao.md) — jornada visual
- [Fluxo do Analista](../design/fluxos/analista.md) — jornada do analista
- [API WhatsApp](../apis/whatsapp.md) — implementação técnica do canal
