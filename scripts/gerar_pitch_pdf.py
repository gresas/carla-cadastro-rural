"""
Gerador do PDF de Pitch do CARla.
Uso: python3 gerar_pitch_pdf.py
Saída: ../CARla_Pitch.pdf
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Fontes TTF com suporte Unicode
FONT_DIR = "/usr/share/fonts/truetype/liberation/"
F_REG  = FONT_DIR + "LiberationSans-Regular.ttf"
F_BOLD = FONT_DIR + "LiberationSans-Bold.ttf"
F_ITA  = FONT_DIR + "LiberationSans-Italic.ttf"
F_BITA = FONT_DIR + "LiberationSans-BoldItalic.ttf"

# ─── Paleta ───────────────────────────────────────────────────────────────────
VERDE_ESCURO  = (27,  94,  32)
VERDE_MEDIO   = (46, 125,  50)
VERDE_CLARO   = (200, 230, 201)
VERDE_FUNDO   = (232, 245, 233)
BRANCO        = (255, 255, 255)
CINZA_ESCURO  = (33,  33,  33)
CINZA_MEDIO   = (97,  97,  97)
CINZA_CLARO   = (245, 245, 245)
AZUL_GOV      = (21, 101, 192)
ROXO          = (106, 27, 154)
VERMELHO      = (183, 28,  28)
LARANJA       = (230, 119,   0)


class PitchPDF(FPDF):

    def setup_fonts(self):
        self.add_font("sans",      "", F_REG)
        self.add_font("sans",      "B", F_BOLD)
        self.add_font("sans",      "I", F_ITA)
        self.add_font("sans",      "BI", F_BITA)

    # ── shortcuts ────────────────────────────────────────────────────────────

    def fc(self, color):
        self.set_fill_color(*color)

    def tc(self, color):
        self.set_text_color(*color)

    def dc(self, color):
        self.set_draw_color(*color)

    def font(self, style="", size=10):
        self.set_font("sans", style, size)

    # ── componentes ──────────────────────────────────────────────────────────

    def section_title(self, title):
        self.ln(4)
        self.fc(VERDE_FUNDO)
        self.dc(VERDE_MEDIO)
        self.set_line_width(0.3)
        y = self.get_y()
        self.rect(12, y, self.w - 24, 10)
        self.set_xy(16, y + 1.5)
        self.font("B", 11)
        self.tc(VERDE_ESCURO)
        self.cell(0, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def body_text(self, txt, size=9.5, color=CINZA_ESCURO, indent=14):
        self.font("", size)
        self.tc(color)
        self.set_x(indent)
        self.multi_cell(self.w - indent - 12, 5.5, txt)
        self.ln(1)

    def bullet(self, txt, size=9.5, color=CINZA_ESCURO, indent=18):
        self.font("", size)
        self.tc(VERDE_MEDIO)
        self.set_x(indent)
        self.cell(5, 5.5, "•")
        self.tc(color)
        self.multi_cell(self.w - indent - 17, 5.5, txt)

    def kpi_box(self, value, label, x, y, w=42, h=22):
        self.fc(VERDE_ESCURO)
        self.rect(x, y, w, h, "F")
        self.set_xy(x, y + 2)
        self.tc(BRANCO)
        self.font("B", 14)
        self.cell(w, 8, value, align="C", new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.set_xy(x, y + 12)
        self.font("", 7.5)
        lines = label.split("\n")
        for line in lines:
            self.set_xy(x, self.get_y())
            self.cell(w, 4.5, line, align="C", new_x=XPos.LEFT, new_y=YPos.NEXT)

    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.font("I", 7.5)
        self.tc(CINZA_MEDIO)
        self.cell(0, 8,
                  f"CARla  ·  Hackathon GovTech 2026  ·  Pág. {self.page_no()}",
                  align="C")


# ─────────────────────────────────────────────────────────────────────────────
def build_pdf(output_path: str):
    pdf = PitchPDF()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(12, 12, 12)
    pdf.setup_fonts()

    # ══════════════════════════════════════════════════════════════════════════
    # PÁGINA 1 — CAPA
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()

    # Fundo verde no topo
    pdf.fc(VERDE_ESCURO)
    pdf.rect(0, 0, pdf.w, 80, "F")
    pdf.fc(VERDE_MEDIO)
    pdf.rect(0, 75, pdf.w, 6, "F")

    # Título
    pdf.set_xy(0, 20)
    pdf.tc(BRANCO)
    pdf.font("B", 42)
    pdf.cell(0, 12, "CARla", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.font("", 13)
    pdf.tc(VERDE_CLARO)
    pdf.cell(0, 7, "Plataforma Inteligente para o Cadastro Ambiental Rural",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    pdf.font("I", 10)
    pdf.tc((200, 230, 201))
    pdf.cell(0, 6, "Hackathon GovTech 2026", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Faixa de KPIs
    pdf.set_y(86)
    pdf.fc(VERDE_FUNDO)
    pdf.rect(0, 84, pdf.w, 38, "F")
    pdf.set_xy(0, 88)
    pdf.tc(VERDE_ESCURO)
    pdf.font("B", 10)
    pdf.cell(0, 6, "IMPACTO ESPERADO", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    kpis = [
        ("-50%", "pendências por\ndoc. incompleta"),
        ("-50%", "tempo médio\nde análise"),
        ("+75%", "taxa de conclusão\nde registro"),
        ("NPS 70+", "satisfação\ndo cidadão"),
    ]
    box_w, gap = 44, 4
    total = len(kpis) * (box_w + gap) - gap
    sx = (pdf.w - total) / 2
    base_y = pdf.get_y()
    for i, (val, lab) in enumerate(kpis):
        pdf.kpi_box(val, lab, sx + i * (box_w + gap), base_y, w=box_w, h=22)

    # Problema (duas colunas)
    pdf.set_y(128)
    pdf.tc(CINZA_ESCURO)
    pdf.font("B", 12)
    pdf.set_x(12)
    pdf.cell(0, 7, "O PROBLEMA", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.dc(VERDE_MEDIO)
    pdf.set_line_width(0.5)
    pdf.line(15, pdf.get_y(), pdf.w - 15, pdf.get_y())
    pdf.ln(4)

    cols_prob = [
        ("Para o CIDADAO", VERDE_MEDIO, [
            "Processo burocático sem orientação",
            "Documentação exigida é confusa",
            "Sem feedback sobre pendências",
            "Depende de consultores pagos",
        ]),
        ("Para o ANALISTA", AZUL_GOV, [
            "Alta carga de processos repetitivos",
            "Documentação incompleta e inconsistente",
            "Sem triagem automatizada",
            "Dosiê montado manualmente",
        ]),
    ]

    col_w = (pdf.w - 30) / 2
    y_cols = pdf.get_y()
    for i, (title, color, items) in enumerate(cols_prob):
        x = 14 + i * (col_w + 4)
        pdf.fc(color)
        pdf.rect(x, y_cols, col_w, 8, "F")
        pdf.set_xy(x, y_cols + 0.5)
        pdf.tc(BRANCO)
        pdf.font("B", 9)
        pdf.cell(col_w, 7, title, align="C")
        yi = y_cols + 10
        for item in items:
            pdf.set_xy(x + 2, yi)
            pdf.tc(color)
            pdf.font("", 8)
            pdf.cell(4, 5, "•")
            pdf.tc(CINZA_ESCURO)
            pdf.multi_cell(col_w - 7, 5, item)
            yi = pdf.get_y()

    # ══════════════════════════════════════════════════════════════════════════
    # PÁGINA 2 — SOLUÇÃO E STACK
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("A SOLUCAO")

    pdf.body_text(
        "O CARla é uma camada inteligente sobre o SICAR — não o substitui, "
        "potencializa. Combina Inteligência Artificial, automação documental e UX "
        "centrada no cidadão para transformar um processo burocrático em uma "
        "experiência guiada, eficiente e confiável.",
        size=10,
    )
    pdf.ln(2)

    # 4 módulos em grid 2×2
    modulos = [
        ("PORTAL DO CIDADAO", VERDE_ESCURO, [
            "Login via Gov.br (sem nova senha)",
            "Registro CAR passo a passo",
            "Upload e acompanhamento",
            "Notificações de pendências",
        ]),
        ("ASSISTENTE IA", AZUL_GOV, [
            "Respostas em linguagem simples",
            "Base de conhecimento CAR/SICAR",
            "Explica pendências e orienta",
            "Chat contextual do processo",
        ]),
        ("MOTOR DE VALIDACAO", ROXO, [
            "OCR de documentos automático",
            "Extração de dados estruturados",
            "Cruzamento e consistência",
            "Pendências geradas por IA",
        ]),
        ("PORTAL DO ANALISTA", VERMELHO, [
            "Fila priorizada com score de risco",
            "Dosiê automático por IA",
            "Aprovação/rejeição em 1 clique",
            "Dashboard de produtividade",
        ]),
    ]

    mod_col_w = (pdf.w - 30) / 2
    mod_h = 40
    gap_m = 4
    y_mod = pdf.get_y()
    for i, (title, color, items) in enumerate(modulos):
        row, col = divmod(i, 2)
        x = 14 + col * (mod_col_w + gap_m)
        y = y_mod + row * (mod_h + gap_m)
        pdf.fc(color)
        pdf.rect(x, y, mod_col_w, 9, "F")
        pdf.set_xy(x, y + 1)
        pdf.tc(BRANCO)
        pdf.font("B", 9)
        pdf.cell(mod_col_w, 7, title, align="C")
        pdf.fc(CINZA_CLARO)
        pdf.rect(x, y + 9, mod_col_w, mod_h - 9, "F")
        yi = y + 11
        for item in items:
            pdf.set_xy(x + 3, yi)
            pdf.tc(color)
            pdf.font("", 7.5)
            pdf.cell(4, 5, "•")
            pdf.tc(CINZA_ESCURO)
            pdf.multi_cell(mod_col_w - 9, 5, item)
            yi = pdf.get_y() + 0.5

    pdf.set_y(y_mod + 2 * (mod_h + gap_m) + 4)
    pdf.section_title("STACK TECNOLOGICA")

    tech_rows = [
        ("Backend",       "Python 3.13+  ·  FastAPI  ·  Pydantic v2  ·  SQLAlchemy 2.0  ·  Alembic"),
        ("Banco",         "PostgreSQL 16  +  PostGIS 3.4  +  pgvector  +  pgcrypto"),
        ("Mensageria",    "RabbitMQ 3.13  (Quorum Queues, Outbox Pattern)  ·  Redis 7"),
        ("Frontend",      "React 18  ·  TypeScript  ·  Vite  ·  Tailwind CSS"),
        ("Autenticacao",  "Gov.br OAuth2/OIDC  ·  JWT RS256  ·  PKCE"),
        ("IA",            "Claude (Anthropic)  ·  GPT-4o (OpenAI)  ·  Ollama (local)  ·  RAG + pgvector"),
        ("Infra",         "Docker  ·  Kubernetes  ·  OpenTelemetry  ·  Prometheus  ·  Grafana"),
    ]
    for label, tech in tech_rows:
        pdf.set_x(14)
        pdf.font("B", 8.5)
        pdf.tc(VERDE_ESCURO)
        pdf.cell(34, 6, label)
        pdf.font("", 8.5)
        pdf.tc(CINZA_ESCURO)
        pdf.cell(0, 6, tech, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ══════════════════════════════════════════════════════════════════════════
    # PÁGINA 3 — ARQUITETURA + DDD + ADRs
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("ARQUITETURA — VISAO GERAL (C4)")

    # Caixas de arquitetura
    pdf.fc(CINZA_CLARO)
    pdf.rect(14, pdf.get_y(), pdf.w - 28, 36, "F")

    arch_lines = [
        ("CIDADAO / CONSULTOR / ANALISTA / ADMIN", VERDE_ESCURO, "B"),
        ("↓  HTTPS  ↓", CINZA_MEDIO, ""),
        ("Nginx API Gateway  ·  TLS 1.3  ·  Rate Limiting  ·  CORS", AZUL_GOV, ""),
        ("↓", CINZA_MEDIO, ""),
    ]
    for text, color, style in arch_lines:
        pdf.set_x(14)
        pdf.font(style, 8.5)
        pdf.tc(color)
        pdf.cell(pdf.w - 28, 5, text, align="C",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    services = [
        ("Auth\nService", VERDE_ESCURO),
        ("Process\nService", VERDE_MEDIO),
        ("Document\nService", AZUL_GOV),
        ("AI Assistant\nService", ROXO),
        ("Analytics\nService", VERMELHO),
    ]
    svc_w = (pdf.w - 30) / len(services)
    sy = pdf.get_y()
    for i, (name, color) in enumerate(services):
        sx = 14 + i * (svc_w + 1)
        pdf.fc(color)
        pdf.rect(sx, sy, svc_w, 14, "F")
        pdf.set_xy(sx, sy + 1)
        pdf.tc(BRANCO)
        pdf.font("B", 7)
        for line in name.split("\n"):
            pdf.set_x(sx)
            pdf.cell(svc_w, 5.5, line, align="C",
                     new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.set_y(sy + 16)
    pdf.set_x(14)
    pdf.tc(CINZA_MEDIO)
    pdf.font("", 7.5)
    pdf.cell(0, 4,
             "↑  Workers Assíncronos (RabbitMQ)  ·  PostgreSQL+PostGIS  ·  Redis  ·  MinIO  ↑",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    pdf.section_title("DOMINIO (DDD) — BOUNDED CONTEXTS")

    bcs = [
        ("IAM",     "Identidade e Acesso",         "Gov.br OAuth2, JWT RS256, RBAC 5 roles",              AZUL_GOV),
        ("CORE",    "Gestao de Processos CAR",      "Agregado ProcessoCAR, máquina de estados, Domain Events", VERDE_ESCURO),
        ("SUP-1",   "Validacao Documental",         "OCR, extração estruturada, cruzamento de dados",       VERDE_MEDIO),
        ("SUP-2",   "Assistencia Inteligente",      "LLM agnóstico, RAG, classificação de intenção, SSE",    ROXO),
        ("GEN-1",   "Integracoes Externas",         "ACL: SICAR, SIGEF, IBAMA, MapBiomas, PRODES/DETER",   VERMELHO),
        ("GEN-2",   "Analytics e Reporting",        "Dosiê PDF automático, KPIs, relatórios gerenciais",  LARANJA),
    ]
    for tag, name, desc, color in bcs:
        pdf.set_x(14)
        pdf.fc(color)
        pdf.tc(BRANCO)
        pdf.font("B", 8)
        pdf.cell(16, 6, tag, fill=True, align="C")
        pdf.tc(CINZA_ESCURO)
        pdf.font("B", 8.5)
        pdf.cell(54, 6, f"  {name}")
        pdf.font("", 8)
        pdf.tc(CINZA_MEDIO)
        pdf.cell(0, 6, desc, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(2)
    pdf.section_title("DECISOES ARQUITETURAIS (ADRs)")

    adrs = [
        ("ADR-001", "FastAPI",              "Performance async, OpenAPI automático, sinergia com Pydantic v2"),
        ("ADR-002", "PostgreSQL+PostGIS",   "ACID + funções geoespaciais + pgvector para RAG do assistente"),
        ("ADR-003", "Event-Driven (EDA)",   "Desacoplamento temporal, auditoria natural, resiliência"),
        ("ADR-004", "RabbitMQ",             "Routing flexível, DLQ, ACK/NACK, simples de operar"),
        ("ADR-005", "Gov.br OAuth2/OIDC",   "CPF verificado, UX cidadão, conformidade e-gov (Decreto 10.900)"),
        ("ADR-006", "LLM Agnostico",        "Sem vendor lock-in, LGPD com Ollama local, custo otimizável"),
    ]
    for num, title, reason in adrs:
        pdf.set_x(14)
        pdf.tc(VERDE_ESCURO)
        pdf.font("B", 8)
        pdf.cell(22, 5.5, num)
        pdf.font("B", 8.5)
        pdf.tc(CINZA_ESCURO)
        pdf.cell(46, 5.5, title)
        pdf.font("", 8)
        pdf.tc(CINZA_MEDIO)
        pdf.cell(0, 5.5, reason, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ══════════════════════════════════════════════════════════════════════════
    # PÁGINA 4 — ROADMAP + MÉTRICAS + SEGURANÇA
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("ROADMAP — 3 FASES")

    fases = [
        ("FASE 1\nMVP Hackathon", "2 semanas", VERDE_ESCURO, [
            "Login mock Gov.br + JWT + RBAC",
            "CRUD de Processo CAR completo",
            "Upload + OCR básico (Tesseract)",
            "Chat com Claude API + RAG CAR",
            "Portal do Analista: fila + aprovação",
            "Monolito modular + Docker Compose",
        ]),
        ("FASE 2\nMVP Producao", "12 semanas", AZUL_GOV, [
            "Integração real Gov.br (PKCE)",
            "Validação documental completa",
            "OCR profissional (Google Vision)",
            "Portal analista + dosiê automático",
            "Notificações email + in-app",
            "Kubernetes + CI/CD + Observabilidade",
        ]),
        ("FASE 3\nVersao Escalavel", "12 meses", ROXO, [
            "Migração para microsserviços",
            "Integrações: SIGEF, IBAMA, MapBiomas",
            "IA avançada: análise geoespacial",
            "Multi-tenancy (múltiplos estados)",
            "App Mobile (React Native)",
            "Analytics e BI para órgãos",
        ]),
    ]

    f_col_w = (pdf.w - 30) / 3
    f_h = 62
    y_f = pdf.get_y()
    for i, (title, duration, color, items) in enumerate(fases):
        x = 14 + i * (f_col_w + 1)
        pdf.fc(color)
        pdf.rect(x, y_f, f_col_w, 18, "F")
        pdf.set_xy(x, y_f + 2)
        pdf.tc(BRANCO)
        pdf.font("B", 9)
        for line in title.split("\n"):
            pdf.set_x(x)
            pdf.cell(f_col_w, 5.5, line, align="C",
                     new_x=XPos.LEFT, new_y=YPos.NEXT)
        pdf.set_xy(x, y_f + 13.5)
        pdf.font("I", 7.5)
        pdf.cell(f_col_w, 4, duration, align="C")

        pdf.fc(CINZA_CLARO)
        pdf.rect(x, y_f + 18, f_col_w, f_h - 18, "F")
        yi = y_f + 20
        for item in items:
            pdf.set_xy(x + 3, yi)
            pdf.tc(color)
            pdf.font("", 7.5)
            pdf.cell(4, 5, "•")
            pdf.tc(CINZA_ESCURO)
            pdf.multi_cell(f_col_w - 9, 5, item)
            yi = pdf.get_y() + 0.5

    pdf.set_y(y_f + f_h + 6)

    # Métricas
    pdf.section_title("METRICAS DE SUCESSO (KPIs)")

    kpi_rows = [
        [("Adoção",    "MAU mes 3",           "≥ 500 usuarios"),
         ("Adoção",    "Taxa conclusao",        "≥ 75%"),
         ("Qualidade",    "Aprovacao 1a tent.",    "≥ 70%"),
         ("Qualidade",    "Reduçao pend.",    "-50%")],
        [("Eficiencia",   "Tempo analise",         "≤ 15 dias uteis"),
         ("Eficiencia",   "Processos/analista/dia", "≥ 10"),
         ("Satisfação", "NPS Cidadao",   "≥ 70"),
         ("Tecnico",      "Uptime SLA",            "≥ 99,5%")],
    ]
    for row in kpi_rows:
        x0 = 14
        kw = (pdf.w - 28) / len(row)
        yk = pdf.get_y()
        for cat, label, val in row:
            pdf.fc(VERDE_ESCURO)
            pdf.rect(x0, yk, kw - 2, 6, "F")
            pdf.set_xy(x0, yk + 0.5)
            pdf.tc(BRANCO)
            pdf.font("B", 7)
            pdf.cell(kw - 2, 5, cat, align="C")
            pdf.set_xy(x0, yk + 7)
            pdf.tc(CINZA_ESCURO)
            pdf.font("", 7)
            pdf.cell(kw - 2, 4.5, label, align="C",
                     new_x=XPos.LEFT, new_y=YPos.NEXT)
            pdf.set_xy(x0, pdf.get_y())
            pdf.tc(VERDE_MEDIO)
            pdf.font("B", 9)
            pdf.cell(kw - 2, 5, val, align="C")
            x0 += kw
        pdf.set_y(yk + 22)

    # Segurança
    pdf.section_title("SEGURANCA E CONFORMIDADE (LGPD)")

    sec_items = [
        "LGPD (Lei 13.709/2018): CPF e email criptografados com pgcrypto; direitos dos titulares implementados; DPO definido",
        "Autenticacao Gov.br: OAuth2 PKCE + JWT RS256 + blacklist Redis + refresh rotation + lockout após 5 tentativas",
        "OWASP Top 10: mitigações documentadas (A01–A10); RBAC com ownership check; SQL via ORM parametrizado",
        "Auditoria imutável: trigger PL/pgSQL captura INSERT/UPDATE/DELETE; retencao 5 anos; audit_logs particionado",
        "Infra K8s: Pod Security Admission (restricted); Network Policies deny-all; Vault para segredos; mTLS entre servicos",
        "Pipeline CI/CD: Bandit (SAST) + Safety (CVEs) + Trivy (container) + Gitleaks (secrets) + OWASP ZAP (DAST)",
    ]
    for item in sec_items:
        pdf.bullet(item, size=8.5)

    # ══════════════════════════════════════════════════════════════════════════
    # PÁGINA 5 — DIFERENCIAIS + INTEGRAÇÕES + ENTREGÁVEIS
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("POR QUE O CARla?")

    diferenciais = [
        ("Nao reinventa a roda",
         "O SICAR continua sendo o sistema oficial. O CARla é uma camada de valor "
         "que potencializa o que já existe, sem risco de ruptura ou incompatibilidade."),
        ("IA aplicada com responsabilidade",
         "LLM agnóstico via Adapter Pattern: troca de provider sem mudar código. "
         "Ollama local para dados sensíveis (LGPD). PII masking antes de qualquer LLM na nuvem."),
        ("DDD + Event-Driven: pronto para escalar",
         "Bounded Contexts isolados permitem crescer de monolito (hackathon) para "
         "microsserviços (produção) sem reescrita. Cada serviço escala independentemente."),
        ("Hackathon para produto governamental",
         "Decisões arquiteturais foram tomadas pensando nos dois cenários. "
         "Documentação, ADRs e testes garantem continuidade após o hackathon."),
        ("Open Source e cloud-agnostico",
         "Stack 100% open source (PostgreSQL, FastAPI, RabbitMQ, Redis). "
         "Sem vendor lock-in. Pode rodar on-premises em infraestrutura governamental."),
    ]
    for title, desc in diferenciais:
        pdf.set_x(14)
        pdf.tc(VERDE_ESCURO)
        pdf.font("B", 9.5)
        pdf.cell(5, 6, "•")
        pdf.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.body_text(desc, size=9, indent=20)
        pdf.ln(1)

    pdf.section_title("INTEGRACOES PLANEJADAS")

    integracoes = [
        ("Gov.br",     "Autenticação OIDC",           "MVP Prod.", VERDE_ESCURO),
        ("SICAR",      "Consulta registros",       "MVP Prod.", VERDE_ESCURO),
        ("IBGE",       "Validação municípios",  "MVP Prod.", VERDE_ESCURO),
        ("SIGEF/INCRA","Georrefer.",               "Fase 3",    AZUL_GOV),
        ("IBAMA",      "Alertas/embargos",         "Fase 3",    AZUL_GOV),
        ("MapBiomas",  "Uso do solo/satélite", "Fase 3",   AZUL_GOV),
        ("PRODES/DETER","Score desmat.",           "Fase 3",    AZUL_GOV),
        ("FUNAI",      "Terras indígenas",    "Fase 3",    ROXO),
    ]

    iw = (pdf.w - 28) / 4
    y_int = pdf.get_y()
    for i, (name, use, phase, color) in enumerate(integracoes):
        row, col = divmod(i, 4)
        x = 14 + col * iw
        y = y_int + row * 14
        pdf.fc(color)
        pdf.rect(x, y, iw - 2, 6, "F")
        pdf.set_xy(x, y + 0.5)
        pdf.tc(BRANCO)
        pdf.font("B", 8)
        pdf.cell(iw - 2, 5, name, align="C")
        pdf.set_xy(x, y + 7)
        pdf.tc(CINZA_ESCURO)
        pdf.font("", 7)
        pdf.cell(iw - 2, 3.5, use, align="C")
        pdf.set_xy(x, y + 10.5)
        pdf.tc(CINZA_MEDIO)
        pdf.font("I", 6.5)
        pdf.cell(iw - 2, 3, phase, align="C")

    pdf.set_y(y_int + 32)
    pdf.section_title("ENTREGAVEIS DO HACKATHON")

    entregaveis = [
        "Repositório com documentação completa: PRD, DDD, ADRs, Arquitetura, Roadmap, Plano de Testes",
        "Backend: FastAPI + PostgreSQL/PostGIS + Redis + RabbitMQ (Docker Compose pronto)",
        "Motor de validação documental: upload, OCR (Tesseract), extração e validação automática",
        "Assistente IA: Claude API + RAG com normativos CAR + streaming SSE em tempo real",
        "Portal do Cidadão: React 18 + Tailwind — login, processo, upload, chat, status",
        "Portal do Analista: fila de processos, dosiê automático, aprovação/rejeição",
        "Demo ao vivo com dados sintéticos: fluxo completo cidadão → analista",
        "Estratégia de testes: unitários (pytest), integração, E2E (Playwright), carga (k6)",
    ]
    for item in entregaveis:
        pdf.bullet(item, size=9)

    # Rodapé de destaque
    pdf.ln(4)
    pdf.fc(VERDE_ESCURO)
    pdf.rect(12, pdf.get_y(), pdf.w - 24, 24, "F")
    pdf.set_xy(14, pdf.get_y() + 3)
    pdf.tc(BRANCO)
    pdf.font("B", 11)
    pdf.cell(0, 7,
             "CARla — Porque o Código Florestal não pode esperar.",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.font("", 9)
    pdf.tc(VERDE_CLARO)
    pdf.cell(0, 6,
             "Uma plataforma que respeita o que existe, potencializa o que falta e escala para o que vem.",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.font("I", 8.5)
    pdf.tc((200, 230, 201))
    pdf.cell(0, 6, "Hackathon GovTech 2026", align="C")

    pdf.output(output_path)
    print(f"PDF gerado: {output_path}")


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(__file__), "..", "CARla_Pitch.pdf")
    build_pdf(os.path.abspath(out))
