# CARla — Event Storming

**Versão:** 1.0.0  
**Data:** 2026-06-01  
**Método:** Big Picture Event Storming + Design-Level Event Storming

---

## 1. Legenda e Convenções

| Elemento | Cor | Notação neste doc | Descrição |
|---|---|---|---|
| Evento de Domínio | Laranja | **[EVENTO]** | Algo que aconteceu no passado; irreversível; nomeado no passado |
| Comando | Azul | `[Comando]` | Ação iniciada por ator ou sistema para causar algo |
| Ator | Amarelo-claro | **Ator →** | Pessoa ou sistema externo que inicia comandos |
| Agregado | Amarelo | {Agregado} | Entidade central afetada pelo comando/evento |
| Política | Lilás | ⇒ Política: | Regra que dispara quando evento ocorre ("quando X, então Y") |
| Sistema Externo | Rosa | [EXT: Sistema] | Sistema fora do bounded context |
| Read Model | Verde | 📊 View: | Modelo de leitura atualizado pelo evento |
| Hotspot | Vermelho | ⚠️ | Ponto de dúvida ou risco |

**Convenção de nomeação de eventos:** substantivo + particípio passado no domínio pt-BR  
Exemplos: `ProcessoSubmetido`, `DocumentoValidado`, `PendênciaIdentificada`

---

## 2. Atores do Sistema

| Ator | Tipo | Descrição | Nível de Acesso |
|---|---|---|---|
| **Produtor Rural** | Humano - Cidadão | Dono do imóvel rural que precisa registrar no CAR | Portal do Cidadão |
| **Consultor Ambiental** | Humano - Profissional | Engenheiro florestal ou técnico que representa proprietários | Portal do Cidadão (com autorização) |
| **Analista Ambiental** | Humano - Servidor | Servidor público que analisa e decide sobre os processos | Portal do Analista |
| **Supervisor Ambiental** | Humano - Servidor | Supervisiona analistas, decide sobre recursos | Portal do Analista (admin) |
| **Administrador do Sistema** | Humano - TI | Gerencia a plataforma técnica | Portal Admin |
| **Sistema de IA** | Sistema | LLM + RAG respondendo dúvidas e gerando dossiês | Interno |
| **Worker de Documentos** | Sistema | Processa OCR e validação de forma assíncrona | Interno |
| **Worker de Notificações** | Sistema | Envia notificações por email/in-app | Interno |
| **[EXT: Gov.br]** | Sistema Externo | Identity Provider do governo federal | OAuth2 OIDC |
| **[EXT: SICAR]** | Sistema Externo | Sistema oficial de Cadastro Ambiental Rural | REST/SOAP |
| **[EXT: SIGEF]** | Sistema Externo | Sistema de georreferenciamento INCRA | REST |
| **[EXT: IBAMA]** | Sistema Externo | Consulta de alertas e embargos | REST |

---

## 3. Bounded Contexts Identificados

### BC1 — Identidade e Acesso (IAM)
**Responsabilidade:** Autenticação, autorização, gestão de usuários e sessões  
**Atores:** Todos os usuários humanos, Gov.br  
**Sistemas externos:** Gov.br (IdP)  
**Modelo:** Usuário, Sessão, Role, Permissão

### BC2 — Gestão de Processos CAR
**Responsabilidade:** Ciclo de vida completo do processo CAR, máquina de estados, pendências, histórico  
**Atores:** Produtor, Consultor, Analista, Supervisor  
**Sistemas externos:** SICAR (consulta)  
**Modelo:** ProcessoCAR, ImóvelRural, Pendência, HistóricoStatus

### BC3 — Validação Documental
**Responsabilidade:** OCR, extração de dados, validação de consistência, cruzamento  
**Atores:** Worker de Documentos, Analista  
**Sistemas externos:** IBGE (municípios)  
**Modelo:** Documento, LoteValidação, ResultadoOCR

### BC4 — Canal WhatsApp
**Responsabilidade:** Recepção e envio de mensagens WhatsApp, vinculação de número ao Gov.br, roteamento para Assistência Inteligente  
**Atores:** Produtor Rural, Consultor, Sistema de IA, WhatsApp Business API  
**Sistemas externos:** WhatsApp Business API (Meta), Gov.br (para vinculação)  
**Modelo:** SessãoWhatsApp, VinculaçãoCanal, MensagemEntrada, MensagemSaída

### BC5 — Assistência Inteligente
**Responsabilidade:** Chat com IA, classificação de intenção, geração de dossiês  
**Atores:** Todos os usuários, Sistema de IA  
**Sistemas externos:** LLM (OpenAI/Claude/Ollama)  
**Modelo:** Conversa, Mensagem, Intenção, BaseConhecimento

### BC5 — Integração com Sistemas Externos
**Responsabilidade:** Anti-Corruption Layer para sistemas externos, circuit breakers, cache  
**Atores:** Todos os BCs que precisam de dados externos  
**Sistemas externos:** SICAR, SIGEF, IBAMA, MapBiomas, PRODES/DETER  
**Modelo:** Integração, ConsultaExterna, ResultadoExterno

### BC6 — Analytics e Reporting
**Responsabilidade:** Métricas, relatórios gerenciais, dashboards, dossiês PDF  
**Atores:** Administrador, Supervisor, Analista  
**Sistemas externos:** Nenhum  
**Modelo:** MétricaDiária, RelatórioGerencial, DossiêProcesso

---

## 4. Event Storming Detalhado por Bounded Context

### BC1 — Identidade e Acesso (IAM)

**Fluxo: Autenticação via Gov.br**

```
Produtor Rural → `[IniciarLoginGovBr]` → {Sessão}
  → [UsuárioRedirecionadoGovBr]
  ⇒ Política: AguardarCallbackGovBr
  📊 View: —

[EXT: Gov.br] → `[RetornarCallbackAutenticação]` → {Usuário}
  → [CallbackGovBrRecebido]
  ⇒ Política: ValidarStateCSRF → se inválido → [TentativaAutenticaçãoFraudulenta]
  ⇒ Política: TrocarCodePorToken → [TokenGovBrObtido]

Sistema → `[CriarOuAtualiarUsuário]` → {Usuário}
  → [UsuárioCadastrado] (novo) ou [UsuárioAtualizado] (retorno)
  ⇒ Política: MapearNívelConfiabilidadeParaRole

Sistema → `[EmitirJWT]` → {Sessão}
  → [SessãoIniciada]
  ⇒ Política: RegistrarÚltimoAcesso
  📊 View: Dashboard do usuário carregado
```

**Fluxo: Gerenciamento de Sessão**

```
Sistema → `[ExpirarSessão]` → {Sessão}
  → [SessãoExpirada]
  ⇒ Política: RemoverDaBlacklist (não aplicável - apenas revogação antecipada vai para blacklist)

Usuário → `[SolicitarRefreshToken]` → {Sessão}
  → [TokenRefrescado] ou [RefreshTokenInválido]
  ⇒ Política: RotacionarRefreshToken (refresh rotation)

Usuário → `[Logout]` → {Sessão}
  → [SessãoEncerrada]
  ⇒ Política: AdicionarJTINaBlacklist (Redis, TTL = expiração do token)
```

**Fluxo: Administração de Usuários**

```
Admin → `[DesativarUsuário]` → {Usuário}
  → [UsuárioDesativado]
  ⇒ Política: RevogarTodasAsSessõesAtivas
  ⇒ Política: NotificarUsuário

Admin → `[AlterarRoleUsuário]` → {Usuário}
  → [RoleAlterada]
  ⇒ Política: InvalidarCachePermissões
```

---

### BC2 — Gestão de Processos CAR

**Fluxo: Criação do Processo**

```
Produtor → `[IniciarNovoProcessoCAR]` → {ProcessoCAR}
  → [ProcessoIniciado] (status: rascunho)
  ⇒ Política: CriarImóvelRuralAssociado
  ⇒ Política: IniciarAssistenteBemVindo
  📊 View: Dashboard atualizado com novo processo

Produtor → `[PreencherDadosImóvel]` → {ImóvelRural}
  → [DadosImóvelSalvos]
  ⇒ Política: AtualizarScoreCompletude

Produtor → `[DefinirGeometriaImóvel]` → {ImóvelRural}
  → [GeometriaDefinida]
  ⇒ Política: ValidarGeometriaAssíncrono → [GeometriaVálida] ou [GeometriaInválida]
  ⇒ Política (GeometriaInválida): CriarPendênciaGeometria
  ⇒ Política: CalcularÁreaAutomática
```

⚠️ **Hotspot:** Quem valida a geometria? O Motor de Validação ou um serviço dedicado? Decidido: ValidadorGeometria como serviço de domínio no BC de Processos, com chamada assíncrona.

**Fluxo: Submissão do Processo**

```
Produtor → `[VerificarCompletude]` → {ProcessoCAR}
  → [CompletudaVerificada]
  ⇒ Política: ExibirDocumentosFaltantes (se incompleto)

Produtor → `[SubmeterProcesso]` → {ProcessoCAR}
  → [ValidaçãoPréSubmissãoIniciada]
  ⇒ Política: VerificarDocumentosObrigatórios
    → [DocumentaçãoInsuficiente] → Rejeitar submissão com lista do que falta
    → [DocumentaçãoSuficiente] → continuar

Sistema → `[GerarNumeroProtocolo]` → {ProcessoCAR}
  → [ProcessoSubmetido] (status: submetido)
  ⇒ Política: PublicarEventoParaFilaDeAnalistas
  ⇒ Política: NotificarCidadãoSubmissãoBemSucedida
  📊 View: Dashboard analista atualizado com novo processo na fila
```

**Fluxo: Análise pelo Analista**

```
Analista → `[AssumirProcesso]` → {ProcessoCAR}
  → [ProcessoEmAnálise] (status: em_analise, analista_id preenchido)
  ⇒ Política: RemoverDaFilaGeral
  ⇒ Política: GerarDossiêAutomático (background)
  📊 View: Fila de outros analistas atualizada

Analista → `[IdentificarPendência]` → {Pendência}
  → [PendênciaIdentificada]
  ⇒ Política: MudarStatusProcessoParaPendente
  ⇒ Política: NotificarCidadãoComDetalhes (email + in-app)
  ⇒ Política: IniciarContadorDePrazo
  📊 View: Processo mostra pendência em destaque para o cidadão

Analista → `[AprovarProcesso]` → {ProcessoCAR}
  → [ProcessoAprovado] (status: aprovado)
  ⇒ Política: GerarNúmeroCAROoficial (integração SICAR)
  ⇒ Política: NotificarCidadãoAprovação
  ⇒ Política: GerarComprovanteRegistro
  📊 View: Dashboard cidadão mostra status "Aprovado" com download do comprovante

Analista → `[RejeitarProcesso]` → {ProcessoCAR}
  → [ProcessoRejeitado] (status: rejeitado)
  ⇒ Política: ObrigarPreenchimentoDeMotivo
  ⇒ Política: NotificarCidadãoComMotivo
  ⇒ Política: IniciarPrazoParaRecurso (30 dias)
  📊 View: Dashboard cidadão mostra status "Rejeitado" com motivo e opção de recurso
```

**Fluxo: Pendência e Correção**

```
Produtor → `[ResponderPendência]` → {Pendência}
  → [RespostaAPendênciaEnviada]
  ⇒ Política: AnalisarSeRequereNovoDocumento
  ⇒ Política: NotificarAnalista
  ⇒ Política: MudarStatusParaEmCorreção (processo)

Sistema → `[ValidarCorreção]` → {Pendência}
  → [PendênciaResolvida] ou [CorreçãoInsuficiente]
  ⇒ Política (resolvida): VerificarSePendênciasRestantes
    → Se sem pendências: [ProcessoRetornadoParaAnálise]
```

**Fluxo: Recurso**

```
Produtor → `[InterpорRecurso]` → {ProcessoCAR}
  → [RecursoInterposto] (status: recurso)
  ⇒ Política: EscalonarParaSupervisor
  ⇒ Política: NotificarSupervisor
  ⇒ Política: ValidarPrazoDe30Dias (se fora do prazo: [RecursoForaDoPrazo])

Supervisor → `[AnalisarRecurso]` → {ProcessoCAR}
  → [RecursoAnalisado]
  ⇒ Política: [RecursoAcatado] → voltar para em_analise com analista diferente
  ⇒ Política: [RecursoNegado] → [ProcessoConcluídoDefinitivamente]
```

---

### BC3 — Validação Documental

**Fluxo: Recebimento e Processamento**

```
Usuário → `[FazerUploadDocumento]` → {Documento}
  → [DocumentoRecebido] (status: aguardando)
  ⇒ Política: ArmazenarNoObjectStorage
  ⇒ Política: PublicarNaFilaOCR
  📊 View: Lista de documentos mostra "Aguardando processamento"

Worker → `[ProcessarOCR]` → {Documento}
  → [OCRIniciado] (status: processando)
  
Worker → `[FinalizarOCR]` → {Documento}
  → [OCRConcluído]
  ⇒ Política: ExtrairDadosEstruturados → [DadosExtraídos]
  ⇒ Política: AvaliarConfiançaOCR
    → Se confiança < 70%: [OCRComBaixaConfiança]
    ⇒ Política (baixa confiança): NotificarReenvio ou FallbackParaRevisãoManual
```

**Fluxo: Validação e Cruzamento**

```
Worker → `[ValidarDocumento]` → {Documento}
  → [ValidaçãoExecutada]
  
  Se consistente:
  → [DocumentoValidado] (status: valido)
  ⇒ Política: AtualizarScoreCompletudeDoProceso
  📊 View: Checklist de documentos atualizado (✓)

  Se inconsistente:
  → [InconsistênciaDetectada] (status: invalido)
  ⇒ Política: CriarPendênciaAutomática no BC Processos
  ⇒ Política: ExplicarInconsistênciaNaPendência
  📊 View: Documento marcado com ✗ e motivo

Worker → `[CruzarDadosEntreDocumentos]` → {LoteValidação}
  → [CruzamentoConcluído]
  ⇒ Política: IdentificarDivergências (área declarada vs. área na matrícula)
  ⇒ Política: CriarPendênciaSeHouverDivergência
```

⚠️ **Hotspot:** OCR de shapefiles ZIP — como validar dados geoespaciais? Decidido: usar PyGEOS/Shapely para validação geométrica após extração.

---

### BC4 — Canal WhatsApp

**Fluxo: Primeira Mensagem — Número Não Vinculado**

```
Cidadão → `[EnviarMensagemWhatsApp]` → {SessãoWhatsApp}
  → [MensagemWhatsAppRecebida]
  ⇒ Política: VerificarVinculaçãoDoNúmero
    → Não vinculado: [SessãoNãoAutenticada]
    ⇒ Política: GerarTokenVinculação (Redis TTL 10min)
    ⇒ Política: EnviarLinkVinculação → [LinkVinculaçãoEnviado]

Cidadão → `[AcessarLinkVinculação]` → {VinculaçãoCanal}
  → [LinkVinculaçãoAcessado]
  ⇒ Política: ValidarTokenNãoExpirado
    → Expirado: [LinkVinculaçãoExpirado] → bot envia novo link
    → Válido: [RedirecionarParaGovBr]

[EXT: Gov.br] → `[RetornarCallbackAutenticação]` → {VinculaçãoCanal}
  → [AutenticaçãoGovBrConfirmada]
  ⇒ Política: VincularNúmeroAoUserId
  → [NúmeroWhatsAppVinculado] (TTL 30 dias no Redis)
  ⇒ Política: NotificarBotWhatsApp → [BotInformadoDaVinculação]
  ⇒ Política: ContinuarAtendimento
```

**Fluxo: Mensagem de Usuário Já Vinculado**

```
Cidadão → `[EnviarMensagemWhatsApp]` → {SessãoWhatsApp}
  → [MensagemWhatsAppRecebida]
  ⇒ Política: VerificarVinculação → Vinculado: [SessãoAutenticada]
  ⇒ Política: ClassificarIntenção
    → duvida/consulta: [RoteadoParaAssistenteIA] → BC Assistência Inteligente
    → operacao_critica (submeter, corrigir): [RedirecionadoParaPortalWeb]
    ⇒ Política: EnviarLinkDiretoAoPortal → [LinkPortalEnviado]
```

**Fluxo: Notificação Proativa**

```
Sistema → `[EnviarNotificaçãoWhatsApp]` → {MensagemSaída}
  (triggerado por: PendênciaIdentificada, ProcessoAprovado, ProcessoRejeitado)
  → [NotificaçãoWhatsAppEnviada] ou [FalhaEnvioWhatsApp]
  ⇒ Política (falha): FallbackParaEmail
```

⚠️ **Hotspot H-09:** Revinculação — se o usuário troca de número de WhatsApp, a vinculação anterior fica órfã. Precisamos de fluxo de desvinculação e revinculação no portal.

⚠️ **Hotspot H-10:** LGPD — o número de WhatsApp é dado pessoal. Deve ser armazenado com criptografia e o usuário deve poder desvincular a qualquer momento.

---

### BC5 — Assistência Inteligente

**Fluxo: Conversa e Resposta**

```
Usuário → `[IniciarConversa]` → {Conversa}
  → [ConversaçãoIniciada]
  ⇒ Política: CarregarContextoDoProcesso (se processo_id fornecido)
  ⇒ Política: SelecionarModeloIA (baseado em configuração + tipo de dados)

Usuário → `[EnviarMensagem]` → {Mensagem}
  → [MensagemRecebida]
  ⇒ Política: ClassificarIntenção → [IntençãoClassificada]

Sistema → `[ProcessarIntenção]` → {Conversa}
  Intenção = dúvida_conceitual:
    ⇒ Política: BuscarNaBaseDeConhecimento (RAG)
    → [DocumentosRelevantesRecuperados]
    ⇒ Política: GerarRespostaComLLM → [RespostaGerada] (via streaming)
    ⇒ Política: ColetarTokensELatência → [MétricaLLMRegistrada]

  Intenção = consultar_status:
    ⇒ Política: ConsultarStatusDoProcesso → [StatusRetornado]
    ⇒ Política: FormatarRespostaDeStatus

  Intenção = solicitar_documento:
    ⇒ Política: IdentificarDocumentoFaltante
    ⇒ Política: GerarLinkUpload → [DocumentoSolicitado]
    ⇒ Política: RegistrarSolicitaçãoNoProcesso

Usuário → `[AvaliarResposta]` → {Mensagem}
  → [FeedbackRegistrado]
  ⇒ Política: AtualizarMétricasDeQualidade
```

**Fluxo: Escalonamento Humano**

```
Sistema → `[DetectarNecessidadeEscalonamento]` → {Conversa}
  (triggers: 3 tentativas sem satisfação, intenção = reclamação, pergunta jurídica complexa)
  → [EscalonamentoTriggered]
  ⇒ Política: NotificarAnalista
  ⇒ Política: EnviarContextoDaConversa
  ⇒ Política: InformarUsuárioSobreEscalonamento
  → [ConversaEscalonada] (status: escalonada)
```

**Fluxo: Geração de Dossiê**

```
Analista → `[SolicitarGeraçãoDeDossiê]` → {DossiêJob}
  → [DossiêSolicitado]
  ⇒ Política: ConsolidarDadosDoProcesso (documentos + integrações + histórico)
  ⇒ Política: GerarTextoComLLM
  ⇒ Política: ComporPDF → [DossiêGerado]
  ⇒ Política: NotificarAnalistaDowloadDisponível
  📊 View: Link de download disponível na tela do processo
```

---

### BC5 — Integração com Sistemas Externos

**Fluxo: Consulta SICAR**

```
BC Processos → `[ConsultarRegistroSICAR]` → {IntegracaoExterna}
  → [ConsultaSICARIniciada]
  ⇒ Política: VerificarCircuitBreaker
    → Circuito Aberto: [FalhaComunicaçãoSICAR] → usar cache ou prosseguir sem dados
    → Circuito Fechado: executar consulta

  Sucesso:
  → [DadosSICARRetornados]
  ⇒ Política: CachearResultado (Redis, TTL 24h)
  ⇒ Política: EnriqueserDadosDoProcesso

  Falha/Timeout:
  → [FalhaComunicaçãoSICAR]
  ⇒ Política: IncrementarContadorCircuitBreaker
  ⇒ Política: RetornarDadosEmCache (se disponível)
  ⇒ Política: AgendarRetry (background, após 30min)
```

**Fluxo: Verificação IBAMA**

```
BC Processos → `[VerificarAlertsIBAMA]` → {IntegracaoExterna}
  → [ConsultaIBAMAIniciada]
  
  Com resultado:
  → [AlertaIBAMAChecado]
  ⇒ Política: SeHouverEmbargo: CriarAlertaNoDossiê + [EmbargoIdentificado]
  ⇒ Política: AtualizarScoreRisco
```

**Fluxo: Resiliência**

```
Sistema → `[DetectarFalhaSistêmica]` → {CircuitBreaker}
  → [CircuitoAberto] (após 5 falhas em 60s)
  ⇒ Política: RegistrarIndisponibilidade
  ⇒ Política: NotificarAdministrador
  ⇒ Política: AgendarVerificação (após 30s → half-open)

Sistema → `[VerificarRecuperação]` → {CircuitBreaker}
  → [CircuitoHalfOpen]
  ⇒ Política: TestePingSistema
  → Sucesso: [CircuitoFechado]
  → Falha: [CircuitoAberto] (continua aberto)
```

---

### BC6 — Analytics e Reporting

**Fluxo: Coleta de Métricas**

```
Sistema (event consumer) → `[ProcessarEventoParaMétrica]` → {MétricaDiária}
  → [MétricaColetada]
  ⇒ Política: AgregrarPorDia+Analista+Município
  📊 View: Dashboard gerencial atualizado

Admin → `[GerarRelatórioGerencial]` → {Relatório}
  → [RelatórioSolicitado]
  ⇒ Política: AgregarDadosDoBanco → [RelatórioGerado]
  ⇒ Política: DisponibilizarParaDownload
```

---

## 5. Mapa Consolidado de Comandos e Eventos

| # | Comando | Ator | BC | Agregado | Evento Resultante | Políticas Disparadas |
|---|---|---|---|---|---|---|
| 01 | IniciarLoginGovBr | Cidadão | IAM | Sessão | UsuárioRedirecionadoGovBr | AguardarCallback |
| 02 | RetornarCallbackAutenticação | Gov.br | IAM | Usuário | TokenGovBrObtido | CriarOuAtualiarUsuário |
| 03 | EmitirJWT | Sistema | IAM | Sessão | SessãoIniciada | RegistrarAcesso |
| 04 | Logout | Usuário | IAM | Sessão | SessãoEncerrada | BlacklistJTI |
| 05 | SolicitarRefreshToken | Usuário | IAM | Sessão | TokenRefrescado | RotacionarRefreshToken |
| 06 | DesativarUsuário | Admin | IAM | Usuário | UsuárioDesativado | RevogarSessões |
| 07 | IniciarNovoProcessoCAR | Cidadão/Consultor | Processos | ProcessoCAR | ProcessoIniciado | CriarImóvel |
| 08 | PreencherDadosImóvel | Cidadão | Processos | ImóvelRural | DadosImóvelSalvos | AtualizarScore |
| 09 | DefinirGeometriaImóvel | Cidadão | Processos | ImóvelRural | GeometriaDefinida | ValidarGeometria |
| 10 | SubmeterProcesso | Cidadão | Processos | ProcessoCAR | ProcessoSubmetido | NotificarAnalistas |
| 11 | AssumirProcesso | Analista | Processos | ProcessoCAR | ProcessoEmAnálise | GerarDossiê |
| 12 | IdentificarPendência | Analista | Processos | Pendência | PendênciaIdentificada | NotificarCidadão |
| 13 | AprovarProcesso | Analista | Processos | ProcessoCAR | ProcessoAprovado | GerarNúmeroCAR |
| 14 | RejeitarProcesso | Analista | Processos | ProcessoCAR | ProcessoRejeitado | NotificarCidadão |
| 15 | ResponderPendência | Cidadão | Processos | Pendência | RespostaEnviada | NotificarAnalista |
| 16 | InterpорRecurso | Cidadão | Processos | ProcessoCAR | RecursoInterposto | EscalonarSupervisor |
| 17 | AnalisarRecurso | Supervisor | Processos | ProcessoCAR | RecursoAnalisado | AcatarOuNegar |
| 18 | FazerUploadDocumento | Cidadão | Documentos | Documento | DocumentoRecebido | PublicarNaFilaOCR |
| 19 | ProcessarOCR | Worker | Documentos | Documento | OCRConcluído | ExtrairDados |
| 20 | ValidarDocumento | Worker | Documentos | Documento | DocumentoValidado / Inválido | AtualizarScore |
| 21 | CruzarDadosEntreDocumentos | Worker | Documentos | LoteValidação | CruzamentoConcluído | CriarPendência |
| 22 | IniciarConversa | Usuário | Assistente | Conversa | ConversaçãoIniciada | CarregarContexto |
| 23 | EnviarMensagem | Usuário | Assistente | Mensagem | MensagemRecebida | ClassificarIntenção |
| 24 | GerarResposta | Sistema IA | Assistente | Mensagem | RespostaGerada | StreamingParaCliente |
| 25 | SolicitarGeraçãoDeDossiê | Analista | Assistente | DossiêJob | DossiêSolicitado | ConsolidarDados |
| 26 | ConsultarRegistroSICAR | BC Processos | Integrações | IntegracaoExterna | DadosSICARRetornados | CachearResultado |
| 27 | VerificarAlertsIBAMA | BC Processos | Integrações | IntegracaoExterna | AlertaIBAMAChecado | AtualizarRisco |
| 28 | SincronizarStatusSICAR | Worker | Integrações | IntegracaoExterna | SincronizaçãoConcluída | AtualizarProcesso |
| 29 | ProcessarEventoParaMétrica | Sistema | Analytics | MétricaDiária | MétricaColetada | AgregarDashboard |
| 30 | GerarRelatórioGerencial | Admin | Analytics | Relatório | RelatórioGerado | DisponibilizarDownload |

---

## 6. Fluxos Críticos Detalhados

### Fluxo 1 — Happy Path: Registro CAR Completo

1. **Autenticação:** João Silva acessa o portal e clica em "Entrar com Gov.br". Gov.br valida CPF e retorna token nível prata. Sistema cria sessão e redireciona para dashboard.

2. **Início do processo:** João clica em "Novo Processo". Assistente IA inicia: "Olá João! Vou te ajudar a registrar seu imóvel no CAR. Qual o nome da sua propriedade?"

3. **Preenchimento guiado:** João preenche nome do imóvel, município (sistema valida via IBGE), área estimada. Assistente explica cada campo em linguagem simples.

4. **Upload de documentos:** Sistema exibe lista de 4 documentos necessários para imóvel < 4 módulos fiscais. João fotografa a matrícula e faz upload. Worker processa OCR (45 segundos), extrai número de matrícula, área, proprietário. Dados conferem com o declarado. Documento marcado como ✓.

5. **Geometria:** João importa shapefile. Sistema valida geometria (polígono fechado, sem auto-interseções, SRID correto). Geometria aceita.

6. **Submissão:** João clica "Submeter processo". Sistema verifica completude (score 100%). Processo submetido. Protocolo gerado. João recebe email de confirmação.

7. **Análise:** Analista Carlos vê processo na fila (prioridade normal, completude 100%). Assume processo. Dossiê gerado automaticamente em 20 segundos.

8. **Aprovação:** Carlos revisa dossiê, verifica no mapa que não há sobreposição com UC. Aprova o processo. Sistema gera número CAR oficial via integração SICAR.

9. **Conclusão:** João recebe email e notificação in-app: "Seu CAR foi aprovado! Número: MA-0001234-XXXXXXXXXX". Pode baixar comprovante.

**Tempo total:** 2-3 dias (tempo de análise do analista)

---

### Fluxo 2 — Pendência e Correção

1. Analista abre processo de Ana Costa (consultora) e identifica divergência: área informada = 150ha, mas matrícula diz 120ha.

2. Analista cria pendência: tipo=dado_conflitante, título="Divergência na área do imóvel", prazo=15 dias.

3. Sistema publica evento PendênciaIdentificada. Worker de notificações envia email para Ana com o detalhe da pendência e link direto.

4. Ana acessa o portal. Vê pendência destacada. Não entende exatamente o que está errado e pergunta ao assistente: "O que significa 'divergência de área'?"

5. Assistente explica: "Identificamos que na matrícula do imóvel consta 120 hectares, mas você declarou 150 hectares. Você precisa atualizar a área declarada ou enviar uma nova matrícula mais recente que comprove os 150 hectares."

6. Ana envia nova matrícula (com área atualizada de 150ha após desmembramento). Worker processa OCR: 150ha confirmado.

7. Sistema valida cruzamento: dados consistentes. Pendência marcada como resolvida automaticamente.

8. Analista notificado: "Pendência resolvida. Processo pronto para revisão."

---

### Fluxo 3 — Análise e Aprovação pelo Analista

1. Carlos acessa portal do analista. Vê fila com 15 processos. Filtra por "prioridade alta" (processos com score de risco elevado).

2. Abre processo de fazenda no Mato Grosso. Score de risco: 8.5/10 (alto). Dossiê mostra: alerta DETER de desmatamento de 2022 a 800m do imóvel.

3. Carlos consulta o dossiê gerado por IA: resumo do processo, mapas de cobertura do solo (MapBiomas), alertas IBAMA, documentação completa.

4. Carlos verifica mapa: imóvel não sobrepõe área de alerta. Documentação completa e consistente. Área de reserva legal > 80% (Amazônia Legal). Tudo conforme.

5. Carlos aprova processo com observação: "Verificado sobreposição com alerta DETER. Imóvel fora da área de desmatamento. APPs identificadas e declaradas. RL suficiente."

6. Proprietário notificado. CAR emitido.

---

### Fluxo 4 — Falha de Integração Externa (Resiliência)

1. Processo submetido aciona consulta ao SICAR para verificar registros anteriores.

2. SICAR está em manutenção. Timeout após 5s.

3. Sistema registra falha. Circuit breaker incrementa contador (3/5).

4. Sistema verifica cache Redis: consulta anterior para o mesmo CPF há 6 horas. Retorna dados em cache.

5. Se sem cache: processo continua sem dados do SICAR. Flag no dossiê: "Consulta SICAR indisponível no momento da análise. Verificar manualmente se necessário."

6. Worker agenda retry para daqui 30 minutos.

7. Analista vê aviso no dossiê e, se necessário, acessa o SICAR diretamente para verificação.

8. Quando SICAR volta: retry automático enriquece o processo com dados atualizados.

---

## 7. Hotspots Identificados

### H-01 — Validação de Geometria Complexa
**Descrição:** Geometrias inválidas (auto-interseções, pontos duplicados, polígonos abertos) são comuns em shapefiles criados por leigos.  
**Complexidade:** Alta — muitos casos edge, comportamento inconsistente entre bibliotecas geoespaciais.  
**Resolução proposta:** PyGEOS + Shapely para validação; simplificação automática com alerta; guia visual de como criar geometria válida.  
**ADR relacionado:** ADR-002 (PostGIS)

### H-02 — Disponibilidade do Gov.br
**Descrição:** Todo o sistema depende do Gov.br para autenticação. Indisponibilidade = usuários bloqueados.  
**Complexidade:** Alta — não temos controle sobre o SLA do Gov.br.  
**Resolução proposta:** Modo degradado com autenticação de emergência para servidores. Monitoramento de SLA do Gov.br. Sessões longas para cidadãos (30 dias refresh token).  
**ADR relacionado:** ADR-005 (Gov.br)

### H-03 — OCR em Documentos de Baixa Qualidade
**Descrição:** Produtores rurais frequentemente enviam fotos escuras, tortas ou com reflexo.  
**Complexidade:** Média — qualidade do OCR degrada muito com imagens ruins.  
**Resolução proposta:** Pré-processamento de imagem (deskew, enhance contrast). Se confiança < 70%: solicitar reenvio com instruções claras e exemplo. Fallback para revisão manual.  
**ADR relacionado:** Nenhum específico

### H-04 — Consistência Entre Documentos
**Descrição:** Área declarada vs. matrícula vs. CCIR vs. georreferenciamento SIGEF podem divergir.  
**Complexidade:** Alta — cada documento tem formato diferente e tolerâncias de área distintas.  
**Resolução proposta:** Tolerância configurável por tipo de divergência (ex: ±5% na área). Pendência automática para divergências > tolerância com explicação clara.

### H-05 — Custo de LLM em Escala
**Descrição:** Cada mensagem do assistente gera chamada LLM. Em 50.000 usuários isso pode ser muito caro.  
**Complexidade:** Média — balancear custo vs. qualidade.  
**Resolução proposta:** Cache semântico de respostas (perguntas similares retornam resposta em cache). Ollama para perguntas frequentes. Limite de tokens por sessão. Relatório mensal de custo.  
**ADR relacionado:** ADR-006 (IA)

### H-06 — LGPD e Dados Geoespaciais
**Descrição:** Geometria do imóvel rural pode revelar localização precisa de residência. Dado pessoal com nível de proteção especial.  
**Complexidade:** Média — dado público (CAR é público) mas individual.  
**Resolução proposta:** Acesso à geometria de terceiros restrito a analistas com role adequada. Exportações públicas agregadas por município, não por imóvel individual.

### H-07 — Idempotência na Submissão
**Descrição:** Usuário clica duas vezes em "Submeter" ou perde conexão. Risco de duplicação de processo.  
**Complexidade:** Baixa — padrão conhecido.  
**Resolução proposta:** Idempotency-Key header obrigatório. Constraint UNIQUE no banco para (requerente_id, imovel_id) em status != rascunho.

### H-08 — Integração com SICAR para Número CAR
**Descrição:** O número CAR oficial deve ser gerado pelo SICAR. Não temos controle sobre a disponibilidade ou API deles.  
**Complexidade:** Alta — dependência crítica no caminho de aprovação.  
**Resolução proposta:** Gerar número CAR interno temporário no formato compatível. Sincronizar com SICAR quando disponível. Se SICAR indisponível: processo marcado como "aprovado_pendente_SICAR", número gerado posteriormente.

---

## 8. Read Models Identificados

| Read Model | Dados Exibidos | Eventos que Atualizam | Performance |
|---|---|---|---|
| 📊 Dashboard do Cidadão | Lista de processos com status, data, progresso | ProcessoIniciado, StatusAlterado, PendênciaIdentificada | Cache 5 min |
| 📊 Detalhes do Processo (Cidadão) | Status, documentos, pendências, histórico | Qualquer evento do processo | Tempo real |
| 📊 Fila do Analista | Processos pendentes com score, prioridade, tempo | ProcessoSubmetido, AnalistaAssumiu, ProcessoConcluído | Cache 1 min |
| 📊 Visão do Analista do Processo | Tudo: dados, docs validados, integrações, dossiê | Qualquer evento | Tempo real |
| 📊 Dashboard Gerencial | KPIs por período, analista, município, bioma | MétricaColetada (diariamente) | Cache 1h |
| 📊 Status de Documentos | Lista com ícone de validação por tipo | DocumentoValidado, DocumentoInválido | Cache 5 min |
| 📊 Histórico do Processo | Linha do tempo de todas as mudanças | HistóricoStatusInserido | Somente leitura |
| 📊 Notificações do Usuário | Lista de notificações não lidas | NotificaçãoCriada, NotificaçãoLida | Tempo real (WebSocket) |
