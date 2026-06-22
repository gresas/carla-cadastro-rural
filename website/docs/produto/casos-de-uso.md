---
sidebar_position: 3
title: Casos de Uso
description: Os casos de uso da Carla — do registro guiado por IA ao acompanhamento de status pelo cidadão.
tags: [produto, casos-de-uso, gherkin]
---

# Casos de Uso

:::info Para quem é esta página
PMs e analistas de negócio. Para detalhes de implementação, veja os [endpoints de API](../apis/processos.md).
:::

## Mapa Geral

| ID | Caso de Uso | Ator Principal | Canal |
|---|---|---|---|
| UC-001 | Iniciar registro CAR com assistência da Carla | Produtor | Interface Web |
| UC-002 | Upload e validação automática de documentos | Produtor | Interface Web |
| UC-003 | Consulta conversacional de dúvidas | Qualquer usuário | Interface Web |
| UC-004 | Acompanhamento de status do processo | Produtor | Interface Web |
| UC-005 | Triagem automática de processos | Analista | Portal Analista |
| UC-006 | Geração automática de dossiê | Analista / Sistema | Portal Analista |
| UC-007 | Notificação de pendências ao cidadão | Sistema | Email / Interface Web |
| UC-008 | Análise e decisão pelo analista | Analista | Portal Analista |
| UC-009 | Correção de inconsistências guiada pela Carla | Produtor | Interface Web |
| UC-010 | Abertura da Carla via car.gov.br | Produtor | Interface Web |
| UC-011 | Primeira mensagem — identificação e login Gov.br | Produtor | Interface Web |
| UC-012 | Retomada de conversa — resumo de etapa e mensagens do analista | Produtor | Interface Web |
| UC-013 | *(Futuro)* Integração com apps de mensageria via webhook | Sistema | WhatsApp / Telegram |
| UC-014 | Relatório de conformidade e analytics | Admin / Supervisor | Portal Admin |

---

## UC-001 — Iniciar Registro CAR com Assistência da Carla

**Fluxo principal:**
1. Usuário acessa a Carla via `car.gov.br` e está autenticado com Gov.br (nível prata)
2. A Carla inicia o fluxo de criação do CAR confirmando o tipo de imóvel (rural comum)
3. Usuário percorre as 6 etapas guiadas: Cadastrante → Imóvel → Domínio → Documentação → Geo → Informações (PRA)
4. Cada etapa é fechada com confirmação em bloco — a Carla nunca pede dado já coletado
5. Processo criado no status `Em Andamento`; ao concluir, passa para `Cadastrado`

```gherkin
Cenário: Cidadão inicia processo com sucesso
  Dado que João está autenticado com Gov.br nível "prata"
  Quando confirmar que o imóvel é um imóvel rural comum
  Então a Carla inicia a Etapa 1 (Cadastrante)
  E apresenta os dados do Gov.br pré-preenchidos para confirmação

Cenário: Tipo de imóvel não elegível (povos tradicionais / assentamentos)
  Quando João indicar que não tem certeza sobre o tipo de imóvel
  Então a Carla explica que imóveis de povos tradicionais e assentamentos da reforma agrária seguem outro fluxo
  E orienta contato com entidade específica
```

---

## UC-002 — Upload e Validação Automática de Documentos

**Fluxo principal:**
1. Usuário envia imagem ou PDF de documento durante a Etapa 4 (Documentação) da Carla
2. Sistema armazena e retorna confirmação imediata (status `aguardando`)
3. Worker OCR processa assincronamente (< 60s)
4. Dados extraídos são comparados com dados declarados nas etapas anteriores
5. Usuário recebe resultado na conversa (válido / inconsistente + motivo)

:::tip Tipos aceitos
PDF, JPG, PNG, TIFF. Máximo 50MB por arquivo. Ver [API de Documentos](../apis/documentos.md).
:::

```gherkin
Cenário: Documento válido processado com sucesso
  Dado que João está na Etapa 4 (Documentação) da Carla
  Quando enviar CCIR em PDF válido
  Então status do documento muda para "aguardando_ocr"
  E em até 60 segundos muda para "validado"
  E dados extraídos são exibidos para conferência em bloco

Cenário: Área declarada diverge do documento
  Quando o OCR identificar área com diferença > 5% em relação ao declarado na Etapa 2
  Então documento recebe status "inconsistente"
  E a Carla indica o campo divergente e orienta correção
```

---

## UC-003 — Consulta Conversacional de Dúvidas

**Fluxo principal:**
1. Usuário digita dúvida no chat da Carla (interface web)
2. Sistema busca chunks relevantes na base de conhecimento (RAG com pgvector)
3. LLM gera resposta embasada nos normativos indexados, com indicação de fonte
4. Resposta exibida em streaming; usuário pode fazer perguntas de acompanhamento
5. Se confiança do RAG for baixa, a Carla oferece encaminhar a pergunta ao analista ambiental

:::tip Cache semântico
Perguntas frequentes (≥ 95% de similaridade) retornam resposta em cache (Redis TTL 1h) sem chamar o LLM.
:::

```gherkin
Cenário: Dúvida com resposta na base de conhecimento
  Dado que Maria está na interface da Carla
  Quando perguntar "Qual a área mínima de Reserva Legal para pequenas propriedades?"
  Então deve receber resposta com citação do Código Florestal
  E deve ver a fonte: "Lei 12.651/2012, Art. 12"

Cenário: Dúvida técnica sem resposta segura
  Quando Maria perguntar algo fora do escopo ou que exige análise técnica específica
  Então a Carla oferece encaminhar a pergunta ao analista ambiental
  E pergunta se Maria confirma o encaminhamento
```

---

## UC-004 — Acompanhamento de Status do Processo

**Fluxo principal:**
1. Usuário acessa a Carla ou a seção "Meus Processos" na interface web
2. A Carla exibe status atual usando a terminologia oficial do SICAR
3. Ao selecionar um processo, exibe timeline completo de eventos
4. Se houver pendência (`Pendente de Regularização`), exibe a mensagem do analista e o prazo
5. Se estiver `Regular`, exibe o Recibo de Inscrição do Imóvel Rural no CAR

```gherkin
Cenário: Processo Pendente de Regularização
  Dado que o cadastro de João está "Pendente de Regularização"
  Quando acessar o status na Carla
  Então deve ver a mensagem do analista com o motivo da pendência
  E botão "Responder agora" deve estar visível
  E deve ver opção "Saber mais sobre o PRA"

Cenário: Processo Regular
  Dado que o processo de João foi aprovado pelo analista
  Quando acessar o status na Carla
  Então deve ver status "Regular" com a data
  E deve ver o Recibo de Inscrição do Imóvel Rural no CAR
  E deve poder baixar o recibo
```

---

## UC-005 — Triagem Automática de Processos

**Fluxo principal:**
1. Analista acessa fila de processos no portal analista
2. Sistema exibe processos ordenados por: (1) prioridade urgente, (2) score de risco, (3) tempo na fila
3. Analista pode filtrar por município, estado, tipo de imóvel ou score
4. Analista seleciona processo e clica "Assumir" — status interno muda para `Em Análise`
5. Sistema registra o analista responsável e hora de início

```gherkin
Cenário: Analista assume processo de alta prioridade
  Dado que existem 15 processos na fila com diferentes scores de risco
  Quando a analista Ana acessar a fila
  Então processos com score de risco > 7 devem aparecer no topo
  E ao clicar "Assumir", status muda para "Em Análise"
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
O dossiê gerado por IA é suporte à decisão. A motivação do ato administrativo deve ser do próprio servidor. Ver [Fluxo do Analista](../design/fluxos/analista.md).
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
3. Notificação enviada por email; na Carla, aparece como mensagem não lida com destaque
4. Cidadão recebe: o que precisa corrigir, prazo e botão direto para responder
5. Sistema registra envio e atualiza status do cadastro para `Pendente de Regularização`

```gherkin
Cenário: Notificação de pendência recebida na Carla
  Dado que João tem processo e o analista criou pendência "Planta de localização ausente"
  Quando João acessar a Carla
  Então deve ver banner "Tenho uma novidade importante"
  E a Carla deve exibir a mensagem do analista com motivo e prazo
  E botão "Responder agora" deve estar visível

Cenário: Email de notificação enviado
  Quando analista criar pendência
  Então João recebe email com detalhes da pendência
  E link direto para a Carla para responder
```

---

## UC-008 — Análise e Decisão pelo Analista

**Fluxo principal:**
1. Analista revisa dossiê e documentos do processo (UC-006)
2. Analista clica em "Encaminhar como Regular", "Encaminhar com pendência (PRA)" ou "Criar pendência"
3. Para qualquer decisão, campo de observações é obrigatório
4. Sistema registra decisão e notifica o cidadão via Carla e email
5. Status do cadastro reflete a terminologia oficial do SICAR

:::warning Recibo de Inscrição
O Recibo de Inscrição do Imóvel Rural no CAR é o comprovante oficial emitido pelo SICAR após a análise.
:::

```gherkin
Cenário: Cadastro encaminhado como Regular
  Dado que Ana revisou o processo e está dentro das conformidades
  Quando clicar "Encaminhar como Regular" e preencher observações
  Então status do cadastro muda para "Regular"
  E cidadão recebe notificação na Carla com Recibo de Inscrição disponível para download
  E registro de auditoria é criado com ID do analista e timestamp

Cenário: Pendência de regularização ambiental identificada
  Dado que o processo tem déficit de Reserva Legal declarado
  Quando Ana criar pendência com motivo e prazo
  Então status muda para "Pendente de Regularização"
  E cidadão recebe notificação na Carla com a mensagem do analista
  E aba "Regularização Ambiental" é liberada no Demonstrativo da Situação do CAR
```

---

## UC-009 — Correção de Inconsistências Guiada pela Carla

**Fluxo principal:**
1. Cidadão acessa processo com status `Pendente de Regularização` na Carla
2. A Carla exibe a mensagem do analista em linguagem acessível e orienta o que corrigir
3. Cidadão faz as correções (reedita dados ou faz novo upload de documento)
4. Sistema revalida automaticamente os documentos corrigidos
5. Processo retorna para fila do analista

```gherkin
Cenário: Cidadão corrige dado divergente
  Dado que João tem cadastro "Pendente de Regularização" com motivo "Área total diverge do CCIR em 8%"
  Quando acessar a mensagem na Carla
  Então a Carla deve explicar qual campo está divergente e como corrigir
  E João deve poder editar a área declarada ou fazer novo upload do CCIR

Cenário: Documento resubmetido dentro do prazo
  Quando João enviar documento corrigido dentro do prazo
  Então a Carla confirma o recebimento
  E analista recebe notificação de que correção foi submetida

Cenário: Prazo de correção vencido sem resposta
  Dado que prazo da pendência venceu sem ação do cidadão
  Então a Carla envia lembrete ao cidadão
  E analista é notificado para decisão sobre o processo
```

---

## UC-010 — Abertura da Carla via car.gov.br

**Fluxo principal:**
1. Cidadão acessa `car.gov.br` e clica no banner ou botão "Fale com a Carla"
2. Nova aba é aberta com a interface de chat da Carla
3. A Carla se apresenta e exibe as três coisas que pode fazer (criação do CAR, dúvidas, acompanhamento)
4. Se o cidadão não estiver logado, exibe o botão "Entrar com Gov.br"
5. Se o cidadão já estiver logado, segue para UC-011 ou UC-012 conforme o contexto

```gherkin
Cenário: Primeiro acesso sem login (Cenário A)
  Dado que o cidadão não está autenticado com Gov.br
  Quando abrir a Carla via car.gov.br
  Então a Carla se apresenta e exibe o botão "Entrar com Gov.br"
  E lista as três capacidades (criação do CAR, dúvidas, acompanhamento)

Cenário: Acesso com login ativo redirecionado para contexto
  Dado que o cidadão já está autenticado com Gov.br
  Quando abrir a Carla via car.gov.br
  Então a Carla verifica se há CAR em andamento ou mensagens do analista
  E segue para UC-012 (retomada) ou UC-011 (primeiro contato)
```

---

## UC-011 — Primeira Mensagem — Identificação e Login Gov.br

**Fluxo principal:**
1. Cidadão recém-autenticado chega à Carla (ou conclui login via Gov.br)
2. A Carla o saúda pelo nome e verifica se há CAR iniciado
3. Se não houver CAR iniciado (Cenário B): oferece iniciar o cadastro ou tirar dúvidas
4. A Carla já usa nome e CPF do Gov.br para pré-preencher a Etapa 1, se o cidadão iniciar

```gherkin
Cenário: Logado, sem nenhum CAR iniciado (Cenário B)
  Dado que João acaba de se autenticar com Gov.br e não tem nenhum CAR iniciado
  Quando a Carla carregar sua sessão
  Então deve ser saudado pelo nome e informado que não há cadastros iniciados
  E deve ver botões "Iniciar meu CAR" e "Tenho dúvidas antes"

Cenário: Cidadão opta por iniciar o CAR
  Quando João clicar "Iniciar meu CAR"
  Então a Carla inicia o fluxo de criação (UC-001)
  E pré-preenche os dados da Etapa 1 com as informações do Gov.br
```

---

## UC-012 — Retomada de Conversa

**Fluxo principal:**
1. Cidadão retorna à Carla e está autenticado com Gov.br
2. A Carla verifica o estado da última sessão
3. Se houver mensagens não lidas do analista com retorno pendente (Cenário D): destaca imediatamente
4. Se houver CAR em andamento sem pendências (Cenário C): oferece continuar de onde parou
5. Carla resume etapa atual, mensagens não lidas e próximas ações

```gherkin
Cenário: Retomada com CAR em andamento, sem pendências (Cenário C)
  Dado que João tem um CAR na etapa "Geo" sem mensagens novas do analista
  Quando abrir a Carla
  Então deve ser saudado e ver o resumo: imóvel + etapa atual
  E deve ver botões "Continuar cadastro" e "Ver status completo"

Cenário: Retomada com mensagens não lidas do analista (Cenário D)
  Dado que João tem mensagens do analista sobre o CAR que precisam de retorno
  Quando abrir a Carla
  Então a Carla deve destacar "Tenho uma novidade importante"
  E exibir a quantidade de mensagens e o nome do imóvel
  E oferecer "Ver mensagens" antes de qualquer outro fluxo
```

---

## UC-013 — *(Futuro)* Integração com Apps de Mensageria via Webhook

:::note Escopo futuro
Este caso de uso descreve uma integração prevista para versões posteriores ao MVP. A Carla não depende de WhatsApp ou Telegram para funcionar — a interface web própria é o canal core. A integração com mensageria será implementada como adapter desacoplado, sem alterar o core da plataforma. Ver [ADR-008](../arquitetura/decisoes/adr-008-canal-web-proprio.md).
:::

**Fluxo planejado:**
1. Cidadão envia mensagem ao número/bot oficial da Carla no WhatsApp ou Telegram
2. Webhook adapter recebe a mensagem e identifica o cidadão via CPF vinculado ao Gov.br
3. Adapter repassa a mensagem para o mesmo backend de conversas do canal web
4. Cidadão pode consultar status e receber notificações; operações formais (criação de CAR, envio de documentos) exigem a interface web

```gherkin
Cenário: Consulta de status via app de mensageria
  Dado que Maria tem CAR em andamento e está vinculada via Gov.br
  Quando enviar mensagem ao bot da Carla pelo WhatsApp
  Então deve receber o status atual do seu CAR com terminologia oficial do SICAR
  E link para a interface web para retomar o cadastro se necessário
```

---

## UC-014 — Relatório de Conformidade e Analytics

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
  Então deve ver: total de processos submetidos, regulares, pendentes de regularização e em andamento
  E tempo médio de análise e taxa de retificação do período

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
- [Sequência de Mensagens da Carla](../design/fluxos/mensagens-simuladas.md) — scripts completos de conversa
- [Fluxo de Abertura da Carla](../design/fluxos/abertura-carla.md) — jornada de entrada pelo car.gov.br
- [Fluxo do Cidadão](../design/fluxos/cidadao.md) — jornada visual das 6 etapas do CAR
- [Fluxo do Analista](../design/fluxos/analista.md) — jornada do analista
- [ADR-008: Canal Web Próprio](../arquitetura/decisoes/adr-008-canal-web-proprio.md) — decisão arquitetural do canal
