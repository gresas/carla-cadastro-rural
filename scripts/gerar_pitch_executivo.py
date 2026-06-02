"""
Gerador do PDF de Pitch Executivo do CARla.
Versão não-técnica — para gestores, investidores e avaliadores.
Uso: python3 gerar_pitch_executivo.py
Saída: ../CARla_Pitch_Executivo.pdf
"""
from fpdf import FPDF
from fpdf.enums import XPos, YPos

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
F_REG  = FONT_DIR + "LiberationSans-Regular.ttf"
F_BOLD = FONT_DIR + "LiberationSans-Bold.ttf"
F_ITA  = FONT_DIR + "LiberationSans-Italic.ttf"
F_BITA = FONT_DIR + "LiberationSans-BoldItalic.ttf"

VERDE        = (27,  94,  32)
VERDE_MED    = (56, 142,  60)
VERDE_SOFT   = (200, 230, 201)
VERDE_FUNDO  = (241, 248, 241)
BRANCO       = (255, 255, 255)
PRETO        = (20,  20,  20)
CINZA        = (90,  90,  90)
CINZA_CLARO  = (245, 245, 245)
AMARELO      = (255, 214,   0)
AZUL         = (21, 101, 192)
VERMELHO     = (198,  40,  40)
LARANJA      = (230, 119,   0)


class Pitch(FPDF):

    def setup_fonts(self):
        self.add_font("s",  "",   F_REG)
        self.add_font("s",  "B",  F_BOLD)
        self.add_font("s",  "I",  F_ITA)
        self.add_font("s",  "BI", F_BITA)

    def f(self, style="", size=10):
        self.set_font("s", style, size)

    def fc(self, c): self.set_fill_color(*c)
    def tc(self, c): self.set_text_color(*c)
    def dc(self, c): self.set_draw_color(*c)

    def header(self): pass

    def footer(self):
        self.set_y(-11)
        self.f("I", 7.5)
        self.tc(CINZA)
        self.cell(0, 6,
            f"CARla  —  Assistente Inteligente do CAR  |  Hackathon GovTech 2026  |  pág. {self.page_no()}",
            align="C")

    # ── helpers visuais ──────────────────────────────────────────────────────

    def faixa(self, y, h, cor):
        self.fc(cor)
        self.rect(0, y, self.w, h, "F")

    def card(self, x, y, w, h, cor_fundo=CINZA_CLARO, cor_borda=None):
        self.fc(cor_fundo)
        self.rect(x, y, w, h, "F")
        if cor_borda:
            self.dc(cor_borda)
            self.set_line_width(0.4)
            self.rect(x, y, w, h)

    def tag(self, x, y, texto, cor=VERDE, fg=BRANCO, w=None):
        self.f("B", 7.5)
        tw = w or (self.get_string_width(texto) + 8)
        self.fc(cor)
        self.rect(x, y, tw, 7, "F")
        self.tc(fg)
        self.set_xy(x, y + 0.3)
        self.cell(tw, 6.5, texto, align="C")
        return tw

    def titulo_secao(self, txt, cor_linha=VERDE_MED):
        self.ln(5)
        self.f("B", 13)
        self.tc(VERDE)
        self.set_x(14)
        self.cell(0, 7, txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.dc(cor_linha)
        self.set_line_width(0.8)
        self.line(14, self.get_y(), 80, self.get_y())
        self.ln(4)

    def paragrafo(self, txt, size=10, cor=PRETO, indent=14):
        self.f("", size)
        self.tc(cor)
        self.set_x(indent)
        self.multi_cell(self.w - indent - 12, 6, txt)
        self.ln(1)

    def bullet(self, txt, size=10, cor=PRETO, indent=18):
        self.f("", size)
        self.tc(VERDE_MED)
        self.set_x(indent)
        self.cell(5, 6, "•")
        self.tc(cor)
        self.multi_cell(self.w - indent - 15, 6, txt)

    def numero_destaque(self, numero, descricao, x, y, w=42, h=26, cor=VERDE):
        self.card(x, y, w, h, cor_fundo=cor)
        self.set_xy(x, y + 3)
        self.tc(BRANCO)
        self.f("B", 18)
        self.cell(w, 10, numero, align="C", new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.set_xy(x, y + 14)
        self.f("", 7.5)
        for linha in descricao.split("\n"):
            self.set_x(x)
            self.cell(w, 5, linha, align="C", new_x=XPos.LEFT, new_y=YPos.NEXT)

    def icone_texto(self, icone, titulo, corpo, x, y, w, cor=VERDE):
        self.set_xy(x, y)
        self.f("B", 20)
        self.tc(cor)
        self.cell(12, 10, icone)
        self.set_xy(x + 14, y + 1)
        self.f("B", 10)
        self.tc(PRETO)
        self.cell(w - 14, 6, titulo, new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.set_xy(x + 14, self.get_y())
        self.f("", 8.5)
        self.tc(CINZA)
        self.multi_cell(w - 15, 5, corpo)


# ─────────────────────────────────────────────────────────────────────────────
def gerar(saida: str):
    pdf = Pitch()
    pdf.set_auto_page_break(auto=True, margin=13)
    pdf.set_margins(12, 12, 12)
    pdf.setup_fonts()

    # ══════════════════════════════════════════════════════════════════════════
    # PÁGINA 1 — CAPA
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()

    # Bloco verde superior
    pdf.faixa(0, 70, VERDE)

    # Detalhe decorativo lateral
    pdf.fc(VERDE_MED)
    pdf.rect(0, 0, 6, 70, "F")

    # Nome do projeto
    pdf.set_xy(0, 16)
    pdf.tc(BRANCO)
    pdf.f("B", 52)
    pdf.cell(0, 18, "CARla", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.f("", 12)
    pdf.tc(VERDE_SOFT)
    pdf.cell(0, 7, "Assistente Inteligente do Cadastro Ambiental Rural",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(1)
    pdf.f("I", 9.5)
    pdf.tc((180, 220, 182))
    pdf.cell(0, 5, "Hackathon GovTech 2026", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Faixa amarela fina de destaque
    pdf.fc(AMARELO)
    pdf.rect(0, 68, pdf.w, 4, "F")

    # Subtítulo / tagline
    pdf.set_xy(0, 78)
    pdf.f("BI", 13)
    pdf.tc(VERDE)
    pdf.cell(0, 8,
             "\"Porque regularizar o imóvel rural não deveria ser um pesadelo.\"",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Números de impacto (3 grandes)
    pdf.ln(6)
    nums = [
        ("9,6 mi", "propriedades rurais\nno CAR nacional"),
        ("30 dias", "tempo médio de\nanálise de um processo"),
        ("40%", "aprovados na\nprimeira tentativa"),
    ]
    bw = (pdf.w - 32) / 3
    bx = 14
    by = pdf.get_y()
    cores = [VERDE, LARANJA, VERMELHO]
    for i, (n, d) in enumerate(nums):
        pdf.numero_destaque(n, d, bx + i * (bw + 2), by, w=bw - 2, h=28, cor=cores[i])

    # Problema em destaque visual
    pdf.set_y(by + 36)
    pdf.faixa(pdf.get_y(), 42, VERDE_FUNDO)
    pdf.ln(4)

    pdf.set_x(14)
    pdf.f("B", 11)
    pdf.tc(VERDE)
    pdf.cell(0, 7, "O que acontece hoje?", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    col_w = (pdf.w - 30) / 2
    problemas = [
        [
            "Produtor rural sem orientação alguma no preenchimento",
            "Documentação exigida confusa — depende de consultor pago",
            "Sem notificação clara quando há pendência",
            "Processo abandouado na metade por dificuldade",
        ],
        [
            "Analista afogado em processos incompletos",
            "Revisão manual e repetitiva de documentos",
            "Sem triagem — tudo chega como prioridade igual",
            "Meses de espera para um registro simples",
        ],
    ]
    titulos = ["Para o produtor rural", "Para o analista ambiental"]
    cores_prob = [VERDE, AZUL]

    y_p = pdf.get_y()
    for i, (titulo, itens, cor) in enumerate(zip(titulos, problemas, cores_prob)):
        x = 14 + i * (col_w + 2)
        pdf.set_xy(x, y_p)
        pdf.f("B", 8.5)
        pdf.tc(cor)
        pdf.cell(col_w, 6, titulo, new_x=XPos.LEFT, new_y=YPos.NEXT)
        yy = pdf.get_y()
        for item in itens:
            pdf.set_xy(x + 2, yy)
            pdf.tc(cor)
            pdf.f("", 8)
            pdf.cell(4, 5.5, "•")
            pdf.tc(PRETO)
            pdf.multi_cell(col_w - 7, 5.5, item)
            yy = pdf.get_y()

    # ══════════════════════════════════════════════════════════════════════════
    # PÁGINA 2 — A SOLUÇÃO
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()

    pdf.faixa(0, 18, VERDE)
    pdf.set_xy(0, 3)
    pdf.tc(BRANCO)
    pdf.f("B", 14)
    pdf.cell(0, 12, "A SOLUCAO", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)
    pdf.paragrafo(
        "O CARla é um assistente digital que acompanha o produtor rural "
        "do início ao fim do registro no CAR — explicando cada passo, "
        "pedindo os documentos certos, avisando sobre pendências e "
        "agilizando a vida do analista com informações já organizadas.",
        size=11
    )
    pdf.ln(2)

    # Os 4 pilares — cards grandes
    pilares = [
        ("Guia o cidadão",
         "O produtor entra, responde perguntas simples e o sistema "
         "faz o registro junto com ele. Nada de formulário confuso sozinho.",
         VERDE, "PORTAL DO CIDADAO"),
        ("Responde na hora",
         "Um assistente de IA tira dúvidas em linguagem simples, "
         "24 horas por dia. Sem precisar ligar para ninguém.",
         AZUL, "ASSISTENTE IA"),
        ("Confere os documentos",
         "A plataforma lê, interpreta e valida os documentos enviados "
         "automaticamente. Erros são apontados antes mesmo de chegar ao analista.",
         LARANJA, "VALIDACAO AUTOMATICA"),
        ("Libera o analista",
         "O analista recebe um resumo pronto, já organizado. "
         "Aprova ou solicita correção em minutos, não em horas.",
         VERDE_MED, "PORTAL DO ANALISTA"),
    ]

    pw = (pdf.w - 30) / 2
    ph = 46
    py0 = pdf.get_y()
    for i, (titulo, corpo, cor, tag_txt) in enumerate(pilares):
        row, col = divmod(i, 2)
        px = 14 + col * (pw + 2)
        py = py0 + row * (ph + 4)

        pdf.card(px, py, pw, ph, cor_fundo=VERDE_FUNDO, cor_borda=cor)

        # faixa de cor no topo do card
        pdf.fc(cor)
        pdf.rect(px, py, pw, 8, "F")
        pdf.set_xy(px, py + 0.5)
        pdf.tc(BRANCO)
        pdf.f("B", 7.5)
        pdf.cell(pw, 7, tag_txt, align="C")

        pdf.set_xy(px + 4, py + 10)
        pdf.tc(PRETO)
        pdf.f("B", 10.5)
        pdf.multi_cell(pw - 8, 6, titulo)

        pdf.set_xy(px + 4, pdf.get_y() + 1)
        pdf.tc(CINZA)
        pdf.f("", 8.5)
        pdf.multi_cell(pw - 8, 5.5, corpo)

    pdf.set_y(py0 + 2 * (ph + 4) + 4)

    # Como funciona — fluxo simples
    pdf.titulo_secao("COMO FUNCIONA NA PRATICA")

    etapas = [
        ("1", "Cidadão entra\ncom Gov.br",    VERDE),
        ("2", "Preenche com\napoio da IA",    VERDE_MED),
        ("3", "Envia documentos\npela tela",   AZUL),
        ("4", "Sistema valida\nautomaticamente", LARANJA),
        ("5", "Analista revisa\no resumo",     VERDE_MED),
        ("6", "CAR aprovado\ne emitido",       VERDE),
    ]

    ew = (pdf.w - 28) / len(etapas)
    ey = pdf.get_y()
    for i, (num, txt, cor) in enumerate(etapas):
        ex = 14 + i * ew

        # círculo numerado
        pdf.fc(cor)
        pdf.rect(ex + ew/2 - 6, ey, 12, 12, "F")
        pdf.set_xy(ex, ey)
        pdf.tc(BRANCO)
        pdf.f("B", 10)
        pdf.cell(ew, 12, num, align="C")

        # seta (exceto último)
        if i < len(etapas) - 1:
            pdf.tc(CINZA)
            pdf.f("", 9)
            pdf.set_xy(ex + ew - 4, ey + 2)
            pdf.cell(8, 8, ">")

        # texto
        pdf.set_xy(ex, ey + 14)
        pdf.tc(PRETO)
        pdf.f("", 7.5)
        for linha in txt.split("\n"):
            pdf.set_x(ex)
            pdf.cell(ew, 4.5, linha, align="C", new_x=XPos.LEFT, new_y=YPos.NEXT)

    # ══════════════════════════════════════════════════════════════════════════
    # PÁGINA 3 — IMPACTO + PARA QUEM + DIFERENCIAIS
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()

    pdf.faixa(0, 18, VERDE)
    pdf.set_xy(0, 3)
    pdf.tc(BRANCO)
    pdf.f("B", 14)
    pdf.cell(0, 12, "IMPACTO ESPERADO", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)

    # 6 números grandes de impacto
    impactos = [
        ("-50%",    "pendências por\ndocumentacao",    VERMELHO),
        ("-50%",    "tempo médio\nde análise",          LARANJA),
        ("+75%",    "processos concluídos\nna 1a vez",  VERDE),
        ("NPS 70+", "satisfacao\ndo cidadao",          AZUL),
        ("10x/dia", "processos por\nanalista",         VERDE_MED),
        ("99,5%",   "disponibilidade\nda plataforma",  CINZA),
    ]

    iw = (pdf.w - 32) / 3
    ix0 = 14
    iy = pdf.get_y()
    for i, (num, desc, cor) in enumerate(impactos):
        row, col = divmod(i, 3)
        ix = ix0 + col * (iw + 2)
        iy2 = iy + row * 32
        pdf.numero_destaque(num, desc, ix, iy2, w=iw - 2, h=28, cor=cor)

    pdf.set_y(iy + 2 * 32 + 6)

    # Para quem é o CARla
    pdf.titulo_secao("PARA QUEM E O CARla")

    perfis = [
        ("Produtor Rural",
         "Agricultor familiar ou grande proprietário que precisa regularizar "
         "o imóvel sem entender de burocracia ambiental.",
         VERDE),
        ("Consultor Ambiental",
         "Profissional que gerencia dezenas de processos ao mesmo tempo e "
         "precisa de mais agilidade e menos retrabalho.",
         AZUL),
        ("Analista do Orgao Ambiental",
         "Servidor público sobrecarregado que quer analisar mais processos "
         "com mais qualidade e menos esforço repetitivo.",
         LARANJA),
        ("Gestores Publicos",
         "Secretários e diretores que precisam de dados e dashboards "
         "para tomar decisões sobre o CAR no seu estado.",
         VERDE_MED),
    ]

    pw2 = (pdf.w - 30) / 2
    py2 = pdf.get_y()
    for i, (nome, desc, cor) in enumerate(perfis):
        row, col = divmod(i, 2)
        px2 = 14 + col * (pw2 + 2)
        py2_card = py2 + row * 28

        pdf.card(px2, py2_card, pw2, 25, cor_fundo=VERDE_FUNDO)
        pdf.fc(cor)
        pdf.rect(px2, py2_card, 5, 25, "F")

        pdf.set_xy(px2 + 8, py2_card + 3)
        pdf.f("B", 9.5)
        pdf.tc(cor)
        pdf.cell(pw2 - 12, 6, nome, new_x=XPos.LEFT, new_y=YPos.NEXT)
        pdf.set_xy(px2 + 8, pdf.get_y())
        pdf.f("", 8)
        pdf.tc(CINZA)
        pdf.multi_cell(pw2 - 14, 5, desc)

    pdf.set_y(py2 + 2 * 28 + 6)

    # Diferenciais
    pdf.titulo_secao("POR QUE O CARla E DIFERENTE")

    diferenciais = [
        ("Nao substitui o SICAR",
         "Funciona junto com o sistema oficial. O governo não precisa "
         "abandonar o que já tem — o CARla potencializa."),
        ("Linguagem simples",
         "Tudo explicado em português direto. "
         "Um agricultor sem letramento digital consegue usar."),
        ("IA com responsabilidade",
         "Dados pessoais e documentos são tratados com total segurança "
         "e em conformidade com a LGPD."),
        ("Pronto para crescer",
         "Começa como demonstração no hackathon e pode virar produto "
         "nacional com o mesmo código-base."),
        ("Sem fila, sem papel",
         "100% digital, 100% rastreável. Qualquer pendência é "
         "comunicada na hora, com instrução clara de como resolver."),
    ]

    for titulo, corpo in diferenciais:
        pdf.set_x(14)
        pdf.f("B", 9.5)
        pdf.tc(VERDE)
        pdf.cell(5, 6, "•")
        pdf.cell(0, 6, titulo, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.paragrafo(corpo, size=9, cor=CINZA, indent=20)

    # ══════════════════════════════════════════════════════════════════════════
    # PÁGINA 4 — ROADMAP VISUAL + CHAMADA FINAL
    # ══════════════════════════════════════════════════════════════════════════
    pdf.add_page()

    pdf.faixa(0, 18, VERDE)
    pdf.set_xy(0, 3)
    pdf.tc(BRANCO)
    pdf.f("B", 14)
    pdf.cell(0, 12, "O CAMINHO", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(6)

    fases = [
        (
            "FASE 1  —  HACKATHON",
            "2 semanas",
            VERDE,
            "Demonstração funcional ao vivo",
            [
                "Cidadao cria processo com ajuda da IA",
                "Faz upload e recebe validacao automatica",
                "Conversa com assistente sobre suas duvidas",
                "Analista ve o processo pronto para avaliar",
                "Aprova ou solicita correcao com um clique",
            ],
            "Meta: juizes conseguem usar sem explicacao previa"
        ),
        (
            "FASE 2  —  PILOTO REAL",
            "3 meses",
            AZUL,
            "Operacao controlada com usuarios reais",
            [
                "Integracao oficial com Gov.br",
                "Validacao real de documentos",
                "Notificacoes por e-mail",
                "Portal do analista completo",
                "Monitoramento e seguranca em producao",
            ],
            "Meta: 100 processos reais, NPS acima de 60"
        ),
        (
            "FASE 3  —  ESCALA NACIONAL",
            "12 meses",
            LARANJA,
            "Produto governamental em producao",
            [
                "Todos os estados brasileiros",
                "Integracao com IBAMA, SIGEF e MapBiomas",
                "App mobile para o campo",
                "Dashboard para secretarias estaduais",
                "IA avancada com dados de satelite",
            ],
            "Meta: 1 milhao de processos facilitados"
        ),
    ]

    fw = (pdf.w - 30) / 3
    fy0 = pdf.get_y()
    for i, (nome, tempo, cor, subtitulo, itens, meta) in enumerate(fases):
        fx = 14 + i * (fw + 2)

        # header do card
        pdf.fc(cor)
        pdf.rect(fx, fy0, fw, 20, "F")
        pdf.set_xy(fx, fy0 + 2)
        pdf.tc(BRANCO)
        pdf.f("B", 8)
        pdf.cell(fw, 6, nome, align="C", new_x=XPos.LEFT, new_y=YPos.NEXT)
        pdf.set_xy(fx, pdf.get_y())
        pdf.f("I", 8)
        pdf.cell(fw, 5, tempo, align="C", new_x=XPos.LEFT, new_y=YPos.NEXT)
        pdf.set_xy(fx, pdf.get_y())
        pdf.f("BI", 7.5)
        pdf.tc((220, 240, 220))
        pdf.cell(fw, 6, subtitulo, align="C")

        # corpo
        pdf.card(fx, fy0 + 20, fw, 68, cor_fundo=VERDE_FUNDO)
        yi = fy0 + 23
        for item in itens:
            pdf.set_xy(fx + 3, yi)
            pdf.tc(cor)
            pdf.f("", 8)
            pdf.cell(4, 5, "•")
            pdf.tc(PRETO)
            pdf.multi_cell(fw - 9, 5, item)
            yi = pdf.get_y() + 0.5

        # badge de meta
        pdf.fc(cor)
        pdf.rect(fx, fy0 + 88, fw, 10, "F")
        pdf.set_xy(fx, fy0 + 89)
        pdf.tc(BRANCO)
        pdf.f("I", 7)
        pdf.multi_cell(fw, 4.5, meta, align="C")

    pdf.set_y(fy0 + 102)

    # O que o CAR representa — contexto
    pdf.titulo_secao("O CONTEXTO: POR QUE ISSO IMPORTA")

    pdf.paragrafo(
        "O Cadastro Ambiental Rural é a porta de entrada para regularização "
        "ambiental de todo imóvel rural no Brasil. Sem ele, o produtor não "
        "acessa crédito rural, não pode vender madeira certificada e fica "
        "exposto a multas. Hoje, burocracia e falta de orientação travam "
        "milhões de pequenos agricultores — especialmente os mais vulneráveis.",
        size=10
    )
    pdf.ln(2)
    pdf.paragrafo(
        "O CARla não é mais um sistema de governo. É um assistente que "
        "fala a língua do cidadão, entende o trabalho do analista e usa "
        "tecnologia de ponta — de forma responsável — para destravar esse gargalo.",
        size=10, cor=VERDE
    )

    # Chamada final
    pdf.ln(6)
    pdf.fc(VERDE)
    pdf.rect(12, pdf.get_y(), pdf.w - 24, 30, "F")

    pdf.fc(AMARELO)
    pdf.rect(12, pdf.get_y(), 5, 30, "F")

    pdf.set_xy(20, pdf.get_y() + 5)
    pdf.tc(BRANCO)
    pdf.f("B", 13)
    pdf.cell(0, 8,
             "CARla — o CAR que finalmente funciona para quem mais precisa.",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_xy(20, pdf.get_y())
    pdf.f("", 9.5)
    pdf.tc(VERDE_SOFT)
    pdf.multi_cell(pdf.w - 32, 6,
        "Um projeto nascido no hackathon com potencial de impacto nacional. "
        "Tecnologia a servico da regularizacao ambiental e da cidadania.")

    pdf.output(saida)
    print(f"PDF gerado: {saida}")


if __name__ == "__main__":
    import os
    saida = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "CARla_Pitch_Executivo.pdf")
    )
    gerar(saida)
