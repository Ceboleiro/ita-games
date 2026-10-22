Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.

import pygame
import math
import random

pygame.init()

# =====================================================
# ITA GAMES 2D - KAEL VS LORDE SOMBRIO - 5 FASES
# =====================================================

LARGURA, ALTURA = 1000, 650
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("ITA GAMES 2D - 5 FASES")

relogio = pygame.time.Clock()

BRANCO = (243, 248, 255)
ESCURO = (17, 26, 43)
PRATA = (197, 213, 229)
AZUL = (23, 100, 181)
CIANO = (66, 232, 255)
ROXO = (130, 57, 180)
VERMELHO = (238, 52, 70)
OURO = (255, 211, 56)

fonte = pygame.font.SysFont("arial", 23, bold=True)
pequena = pygame.font.SysFont("arial", 18, bold=True)
media = pygame.font.SysFont("arial", 30, bold=True)
grande = pygame.font.SysFont("arial", 55, bold=True)
logo = pygame.font.SysFont("arialblack", 72, bold=True)

# =====================================================
# CONFIGURACAO DAS 5 FASES
# =====================================================

FASES = [
    {
        "nome": "VALE VERDE",
        "buraco": (410, 540),
        "plataformas": [
            (250, 410, 150, 28),
            (440, 320, 150, 28),
            (650, 410, 150, 28)
        ],
        "moedas": [
            (175, 480),
            (300, 365),
            (490, 275),
            (705, 365),
            (840, 480)
        ],
        "inimigos": [
            (305, 255, 355, 1.4, 530),
            (690, 570, 810, 1.6, 530)
        ],
        "ceu": (
            (74, 159, 225),
            (190, 225, 244)
        )
    },

    {
        "nome": "FLORESTA MISTERIOSA",
        "buraco": (355, 505),
        "plataformas": [
            (200, 410, 145, 28),
            (385, 330, 155, 28),
            (590, 410, 155, 28),
            (770, 350, 130, 28)
        ],
        "moedas": [
            (145, 480),
            (245, 365),
            (440, 285),
            (635, 365),
            (815, 305)
        ],
        "inimigos": [
            (230, 110, 270, 1.9, 530),
            (650, 550, 750, 2.0, 530),
            (785, 780, 855, 1.2, 350)
        ],
        "ceu": (
            (74, 131, 158),
            (155, 205, 187)
        )
    },

    {
        "nome": "DESFILADEIRO",
        "buraco": (420, 610),
        "plataformas": [
            (230, 405, 145, 28),
            (415, 315, 155, 28),
            (635, 385, 150, 28),
            (790, 315, 130, 28)
        ],
        "moedas": [
            (145, 480),
            (270, 360),
            (460, 270),
            (680, 340),
            (830, 270)
        ],
        "inimigos": [
            (315, 215, 360, 2.0, 530),
            (690, 635, 785, 2.2, 385),
            (800, 720, 895, 1.7, 530)
        ],
        "ceu": (
            (172, 106, 123),
            (252, 187, 133)
        )
    },

    {
        "nome": "MONTANHA GELADA",
        "buraco": (300, 490),
        "plataformas": [
            (180, 400, 130, 28),
            (340, 320, 165, 28),
            (560, 400, 145, 28),
            (730, 310, 135, 28)
        ],
        "moedas": [
            (120, 480),
            (225, 355),
            (390, 275),
            (610, 355),
            (775, 265)
        ],
        "inimigos": [
            (185, 100, 245, 2.0, 530),
            (580, 510, 700, 2.2, 530),
            (765, 735, 840, 1.6, 310)
        ],
        "ceu": (
            (78, 143, 200),
            (206, 231, 251)
        )
    },

    {
        "nome": "FORTALEZA DAS SOMBRAS",
        "buraco": (400, 630),
        "plataformas": [
            (225, 395, 150, 28),
            (425, 310, 155, 28),
            (645, 385, 155, 28),
            (805, 305, 145, 28)
        ],
        "moedas": [
            (145, 480),
            (265, 350),
            (465, 265),
            (685, 340),
            (850, 260)
        ],
        "inimigos": [
            (295, 215, 365, 2.2, 530),
            (655, 645, 750, 2.1, 385),
            (770, 680, 880, 2.4, 530),
            (825, 810, 910, 1.8, 305)
        ],
        "ceu": (
            (35, 38, 85),
            (135, 105, 165)
        )
    }
]

# =====================================================
# CRIAR CENARIOS MONTANHOSOS
# =====================================================

def misturar(c1, c2, t):
    return tuple(
        int(a + (b - a) * t)
        for a, b in zip(c1, c2)
    )


def criar_cenario(numero):

    config = FASES[numero - 1]
    r = random.Random(2026 + numero)

    s = pygame.Surface(
        (LARGURA, ALTURA)
    ).convert()

    # CEU COM DEGRADE
    for y in range(ALTURA):

        cor = misturar(
            config["ceu"][0],
            config["ceu"][1],
            y / ALTURA
        )

        pygame.draw.line(
            s, cor,
            (0, y),
            (LARGURA, y)
        )

    # SOL OU LUA
    if numero == 5:
        sol = (219, 222, 242)
    else:
        sol = (245, 238, 214)

    pygame.draw.circle(
        s, sol,
        (815, 122),
        54
    )

    # MONTANHAS DISTANTES
    montanhas_distantes = [
        (-160, 175, 460),
        (130, 145, 460),
        (410, 200, 430),
        (730, 153, 480)
    ]

    for x, topo, largura in montanhas_distantes:

        pico = x + largura // 2

        if numero == 5:
            cor_montanha = (72, 70, 112)
        else:
            cor_montanha = (114, 145, 165)

        pygame.draw.polygon(
            s,
            cor_montanha,
            [
                (x, 535),
                (pico, topo),
                (x + largura, 535)
            ]
        )

        # NEVE
        pygame.draw.polygon(
            s,
            (226, 239, 247),
            [
                (pico - 44, topo + 66),
                (pico, topo),
                (pico + 55, topo + 72),
                (pico + 20, topo + 61),
                (pico, topo + 83),
                (pico - 17, topo + 57)
            ]
        )

    # MONTANHAS PRINCIPAIS
    montanhas = [
        (-220, 224, 580),
        (80, 178, 610),
        (455, 205, 555),
        (745, 215, 460)
    ]

    for x, topo, largura in montanhas:

        pico = x + largura // 2

        pygame.draw.polygon(
            s,
            (96, 106, 117),
            [
                (x, 545),
                (pico, topo),
                (x + largura, 545)
            ]
        )

        # SOMBRA
        pygame.draw.polygon(
            s,
            (62, 76, 91),
            [
                (pico, topo),
                (x + largura, 545),
                (pico + 50, 545)
            ]
        )

        # NEVE NO PICO
        pygame.draw.polygon(
            s,
            (235, 243, 248),
            [
                (pico - 70, topo + 92),
                (pico, topo),
                (pico + 70, topo + 98),
                (pico + 27, topo + 69),
                (pico, topo + 104),
                (pico - 23, topo + 69)
            ]
        )

        # TEXTURA DE ROCHAS
        for i in range(65):

            y = r.randint(
                topo + 112,
                530
            )

            alcance = int(
                (y - topo) * largura /
                (2 * (545 - topo))
            )

            xx = r.randint(
                pico - alcance,
                pico + alcance
            )

            cor = r.choice([
                (62, 73, 85),
                (136, 143, 151),
                (99, 108, 118)
            ])

            pygame.draw.line(
                s, cor,
                (xx, y),
                (xx + r.randint(5, 18), y + 5),
                2
            )

    # COLINAS
    pygame.draw.ellipse(
        s,
        (56, 107, 84),
        (-200, 455, 850, 300)
    )

    pygame.draw.ellipse(
        s,
        (38, 87, 69),
        (350, 460, 850, 280)
    )

    # SOLO
    pygame.draw.rect(
        s,
        (71, 116, 71),
        (0, 548, LARGURA, 102)
    )

    # ARVORES
    arvores = [
        (55, 555, 105),
        (130, 552, 90),
        (215, 568, 115),
        (760, 554, 105),
        (870, 550, 120),
        (965, 560, 100)
    ]

    for x, base, tamanho in arvores:

        pygame.draw.rect(
            s,
            (84, 58, 44),
            (x - 5, base - 29, 10, 29)
        )

        for camada in range(3):

            topo = base - tamanho + camada * 21
            largura = tamanho // 2 - camada * 6

            pygame.draw.polygon(
                s,
                (
                    28 + camada * 8,
                    72 + camada * 11,
                    50 + camada * 5
                ),
                [
                    (x, topo),
                    (x - largura, topo + 53),
                    (x + largura, topo + 53)
                ]
            )

    # GRAMA TEXTURIZADA
    for i in range(250):

        x = r.randrange(1000)
        y = r.randrange(558, 650)

        cor = r.choice([
            (46, 91, 53),
            (96, 141, 80),
            (133, 151, 95)
        ])

        pygame.draw.line(
            s, cor,
            (x, y),
            (x + 2, y - 5),
            1
        )

    # ATMOSFERA DA FASE 4
    if numero == 4:

        camada = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        camada.fill(
            (197, 219, 250, 37)
        )

        s.blit(camada, (0, 0))

    # ATMOSFERA DA FASE 5
    elif numero == 5:

        camada = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        camada.fill(
            (22, 13, 51, 65)
        )

        s.blit(camada, (0, 0))

    return s


cenarios = [
    criar_cenario(i)
    for i in range(1, 6)
]

# ==========================================
# NUVENS ANIMADAS
# ==========================================

nuvens = pygame.Surface(
    (LARGURA, 250),
    pygame.SRCALPHA
)

for x, y, escala in [
    (150, 85, 1.1),
    (490, 55, 0.8),
    (810, 135, 1.0)
]:

    partes = [
        (-50, 8, 90, 36),
        (-12, -13, 90, 56),
        (36, 5, 92, 38)
    ]

    for dx, dy, w, h in partes:

        pygame.draw.ellipse(
            nuvens,
            (255, 255, 255, 155),
            (
                int(x + dx * escala),
                int(y + dy * escala),
                int(w * escala),
                int(h * escala)
            )
        )

# ==========================================
# TEXTURA DAS PLATAFORMAS
# ==========================================

def textura_plataforma(w, h, semente):

    s = pygame.Surface(
        (w, h),
        pygame.SRCALPHA
    )

    r = random.Random(semente)

    pygame.draw.rect(
        s,
        (105, 76, 58),
        (0, 0, w, h),
        border_radius=6
    )

    for i in range(min(250, w)):

        cor = r.choice([
            (74, 57, 51),
            (147, 104, 73),
            (171, 131, 89)
        ])

        pygame.draw.circle(
            s,
            cor,
            (
                r.randrange(w),
                r.randrange(12, h)
            ),
            r.randint(1, 3)
        )

    pygame.draw.rect(
        s,
        (39, 112, 56),
        (0, 0, w, 17),
        border_radius=5
    )

    pygame.draw.rect(
        s,
        (88, 184, 80),
        (0, 0, w, 11),
        border_radius=5
    )

    pygame.draw.line(
        s,
        (155, 225, 101),
        (4, 3),
        (w - 4, 3),
        3
    )

    for x in range(5, w - 5, 14):

        pygame.draw.polygon(
            s,
            (51, 139, 61),
            [
                (x, 11),
                (x + 10, 11),
                (x + 5, 19)
            ]
        )

    return s.convert_alpha()

# ==========================================
# KAEL E LORDE SOMBRIO
# ==========================================

def criar_personagem(sombrio=False):

    s = pygame.Surface(
        (100, 135),
        pygame.SRCALPHA
    )

    if sombrio:
        capa = (77, 32, 112)
        capa_clara = (142, 64, 187)
        armadura = (52, 54, 72)
        brilho = (178, 89, 232)
    else:
        capa = (20, 45, 100)
        capa_clara = (37, 88, 166)
        armadura = AZUL
        brilho = CIANO

    # CAPA
    pygame.draw.polygon(
        s, capa,
        [
            (33, 46),
            (67, 46),
            (86, 123),
            (12, 123)
        ]
    )

    pygame.draw.polygon(
        s, capa_clara,
        [
            (35, 51),
            (43, 57),
            (21, 119),
            (16, 119)
        ]
    )

    # BOTAS
    for x in (30, 54):

        pygame.draw.rect(
            s, ESCURO,
            (x, 104, 17, 25),
            border_radius=4
        )

        cor = (
            (53, 47, 68)
            if sombrio
            else PRATA
        )

        pygame.draw.rect(
            s, cor,
            (x - 1, 120, 20, 7),
            border_radius=3
        )

    # BRACOS
    for x in (21, 63):

        pygame.draw.rect(
            s, ESCURO,
            (x, 53, 17, 43),
            border_radius=5
        )

        pygame.draw.rect(
            s, armadura,
            (x + 2, 58, 13, 31),
            border_radius=4
        )

    # PEITORAL
    pygame.draw.rect(
        s, ESCURO,
        (32, 47, 39, 64),
        border_radius=9
    )

    pygame.draw.rect(
        s, armadura,
        (36, 52, 31, 52),
        border_radius=7
    )

    cor_peito = (
        (119, 120, 139)
        if sombrio
        else PRATA
    )

    pygame.draw.polygon(
        s,
        cor_peito,
        [
            (36, 55),
            (51, 65),
            (66, 55),
            (62, 81),
            (51, 90),
            (40, 81)
        ]
    )

    pygame.draw.polygon(
        s,
        brilho,
        [
            (51, 66),
            (59, 76),
            (51, 85),
            (44, 76)
        ]
    )

    # OMBREIRAS
    for x in (30, 71):

        cor_ombro = (
            ESCURO if sombrio else PRATA
        )

        pygame.draw.circle(
            s,
            cor_ombro,
            (x, 56),
            13
        )

        pygame.draw.circle(
            s,
            ROXO if sombrio else AZUL,
            (x, 56),
            8
        )

    # ROSTO
    cor_pele = (
        (192, 147, 127)
        if sombrio
        else (204, 156, 120)
    )

    pygame.draw.ellipse(
        s,
        cor_pele,
        (33, 15, 37, 41)
    )

    # CABELO ESPETADO
    cor_cabelo = (
        (17, 17, 28)
        if sombrio
        else (53, 37, 28)
    )

    pygame.draw.polygon(
        s,
        cor_cabelo,
        [
            (29, 36),
            (25, 15),
            (36, 18),
            (39, 3),
            (48, 14),
            (57, 1),
            (61, 16),
            (72, 10),
            (70, 36),
            (62, 25),
            (48, 29),
            (37, 24)
        ]
    )

    # OLHOS
    for x in (38, 55):

        cor_olhos = (
            VERMELHO
            if sombrio
            else (24, 191, 255)
        )

        pygame.draw.ellipse(
            s,
            cor_olhos,
            (x, 33, 9, 7)
        )

        pygame.draw.circle(
            s,
            ESCURO,
            (x + 5, 36),
            2
        )

    pygame.draw.line(
        s,
        (92, 46, 47),
        (45, 47),
        (58, 47),
        2
    )

    # ESPADA DO KAEL
    if not sombrio:

        pygame.draw.line(
            s,
            (28, 44, 68),
            (79, 92),
            (89, 77),
            6
        )

        pygame.draw.line(
            s,
            (165, 243, 255),
            (89, 77),
            (94, 12),
            10
        )

        pygame.draw.line(
            s,
            CIANO,
            (89, 77),
            (94, 12),
            5
        )

    return pygame.transform.smoothscale(
        s,
        (63, 85)
    ).convert_alpha()


kael = criar_personagem()
lorde = criar_personagem(True)

kael_esquerda = pygame.transform.flip(
    kael, True, False
)

lorde_esquerda = pygame.transform.flip(
    lorde, True, False
)

# ==========================================
# MOEDA
# ==========================================

moeda_img = pygame.Surface(
    (35, 35),
    pygame.SRCALPHA
)

for raio, cor in [
    (16, (145, 90, 26)),
    (14, OURO),
    (10, (255, 242, 134)),
    (7, (255, 201, 35))
]:

    pygame.draw.circle(
        moeda_img,
        cor,
        (17, 17),
        raio
    )

pygame.draw.line(
    moeda_img,
    BRANCO,
    (12, 8),
    (16, 6),
    3
)

moeda_img = moeda_img.convert_alpha()

# ==========================================
# PORTA
# ==========================================

porta_img = pygame.Surface(
    (110, 145),
    pygame.SRCALPHA
)

camadas_porta = [
    ((9, 34, 87, 109), ESCURO, 21),
    ((15, 40, 75, 101), (157, 171, 192), 19),
    ((23, 49, 59, 92), (128, 78, 56), 14),
    ((29, 56, 46, 85), (166, 103, 70), 10)
]

for ret, cor, arred in camadas_porta:

    pygame.draw.rect(
        porta_img,
        cor,
        ret,
        border_radius=arred
    )

pygame.draw.line(
    porta_img,
    (80, 44, 39),
    (53, 61),
    (53, 138),
    3
)

pygame.draw.circle(
    porta_img,
    OURO,
    (65, 103),
    5
)

pygame.draw.line(
    porta_img,
    ESCURO,
    (98, 9),
    (98, 140),
    4
)

pygame.draw.polygon(
    porta_img,
    (45, 204, 111),
    [
        (99, 17),
        (109, 28),
        (99, 45)
    ]
)

porta_img = porta_img.convert_alpha()

porta_rect = pygame.Rect(
    875, 445, 55, 85
)

# ==========================================
# MENU INICIAL
# ==========================================

botoes_menu = [
    pygame.Rect(
        354,
        325 + 81 * i,
        292,
        60
    )
    for i in range(3)
]

nomes_botoes = [
    "JOGAR",
    "COMO JOGAR",
    "SAIR"
]

retrato_kael = pygame.transform.smoothscale(
    kael,
    (151, 207)
)

retrato_lorde = pygame.transform.smoothscale(
    lorde_esquerda,
    (151, 207)
)

voltar_rect = pygame.Rect(
    390, 550, 220, 57
)

sombra_menu = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

sombra_menu.fill(
    (11, 20, 44, 140)
)

sombra_ajuda = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

sombra_ajuda.fill(
    (8, 15, 35, 205)
)

sombra_fim = pygame.Surface(
    (LARGURA, ALTURA),
    pygame.SRCALPHA
)

sombra_fim.fill(
    (8, 15, 35, 205)
)

# ==========================================
# FUNCOES DO MENU
# ==========================================

def escrever(
    txt, f, cor, x, y, centro=False
):

    imagem = f.render(
        str(txt),
        True,
        cor
    )

    if centro:
        pos = imagem.get_rect(
            center=(x, y)
        )
    else:
        pos = (x, y)

    tela.blit(imagem, pos)


def botao(rect, texto, ativo):

    pygame.draw.rect(
        tela,
        (7, 18, 38),
        rect.move(0, 5),
        border_radius=15
    )

    if ativo:
        cor = (13, 153, 194)
        borda = (155, 242, 255)
    else:
        cor = (19, 49, 82)
        borda = (104, 171, 217)

    pygame.draw.rect(
        tela,
        cor,
        rect,
        border_radius=15
    )

    pygame.draw.rect(
        tela,
        borda,
        rect,
        2,
        border_radius=15
    )

    escrever(
        texto,
        media,
        BRANCO,
        *rect.center,
        centro=True
    )


def fundo_animado(t):

    tela.blit(
        cenarios[fase - 1],
        (0, 0)
    )

    desloc = int(t * 12) % LARGURA

    tela.blit(
        nuvens,
        (desloc - LARGURA, 0)
    )

    tela.blit(
        nuvens,
        (desloc, 0)
    )


def desenhar_menu(t):

    tela.blit(
        cenarios[0],
        (0, 0)
    )

    desloc = int(t * 12) % LARGURA

    tela.blit(
        nuvens,
        (desloc - LARGURA, 0)
    )

    tela.blit(
        nuvens,
        (desloc, 0)
    )

    tela.blit(
        sombra_menu,
        (0, 0)
    )

    escrever(
        "ITA GAMES 2D",
        logo,
        BRANCO,
        500, 119,
        True
    )

    escrever(
        "KAEL VS LORDE SOMBRIO",
        media,
        CIANO,
        500, 213,
        True
    )

    escrever(
        "AVENTURA EM 5 FASES",
        pequena,
        BRANCO,
        500, 267,
        True
    )

    tela.blit(
        retrato_kael,
        (105, 335)
    )

    tela.blit(
        retrato_lorde,
        (741, 335)
    )

    mouse = pygame.mouse.get_pos()

    for i, rect in enumerate(botoes_menu):

        ativo = (
            rect.collidepoint(mouse)
            or escolha == i
        )

        botao(
            rect,
            nomes_botoes[i],
            ativo
        )

    escrever(
        "Mouse ou setas + ENTER",
        pequena,
        BRANCO,
        500, 611,
        True
    )


def desenhar_ajuda(t):

    tela.blit(
        cenarios[0],
        (0, 0)
    )

    tela.blit(
        sombra_ajuda,
        (0, 0)
    )

    painel = pygame.Rect(
        135, 62, 730, 565
    )

    pygame.draw.rect(
        tela,
        (20, 41, 67),
        painel,
        border_radius=22
    )

    pygame.draw.rect(
        tela,
        CIANO,
        painel,
        2,
        border_radius=22
    )

    escrever(
        "COMO JOGAR",
        grande,
        CIANO,
        500, 130,
        True
    )

    instrucoes = [
        "A / D ou SETAS: andar",
        "ESPACO, W ou SETA CIMA: pulo duplo",
        "SHIFT: correr | J: atacar com a espada",
        "R: reiniciar | ESC: voltar ao menu",
        "Colete as 5 moedas de cada fase.",
        "Chegue a porta para avancar.",
        "Complete as 5 fases para vencer!"
    ]

    for i, linha in enumerate(instrucoes):

        escrever(
            linha,
            pequena,
            BRANCO,
            500,
            218 + 42 * i,
            True
        )

    botao(
        voltar_rect,
        "VOLTAR",
        voltar_rect.collidepoint(
            pygame.mouse.get_pos()
        )
    )

# ==========================================
# CARREGAR UMA FASE
# ==========================================

def carregar_fase(numero):

    global fase, config
    global plataformas, texturas
    global agua_x, agua_largura, espinhos
    global moedas, coletadas_fase, inimigos
    global jogador, jogador_y, vy, pulos
    global direcao, invencivel
    global ataque_tempo, ataque_cooldown
    global atingidos

    fase = numero
    config = FASES[fase - 1]

    inicio, fim = config["buraco"]

    # AGUA DO BURACO
    agua_x = inicio
    agua_largura = fim - inicio

    # ESPINHOS BAIXOS
    espinhos = pygame.Rect(
        inicio + 5,
        518,
        fim - inicio - 10,
        12
    )

    # TERRENO ESQUERDO E DIREITO
    plataformas = [
        pygame.Rect(
            0, 530,
            inicio, 120
        ),

        pygame.Rect(
            fim, 530,
            LARGURA - fim, 120
        )
    ]

    # PLATAFORMAS ELEVADAS
    plataformas += [
        pygame.Rect(*p)
        for p in config["plataformas"]
    ]

    # TEXTURA DAS PLATAFORMAS
    texturas = [
        textura_plataforma(
            p.width,
            p.height,
            fase * 100 + i
        )
        for i, p in enumerate(plataformas)
    ]

    # 5 MOEDAS DESTA FASE
    moedas = [
        pygame.Rect(x, y, 30, 30)
        for x, y in config["moedas"]
    ]

    coletadas_fase = 0

    # CRIAR LORDES SOMBRIOS
    inimigos = []

    for i, dados in enumerate(config["inimigos"]):

        x, xmin, xmax, rapidez, chao = dados

        inimigos.append({
            "id": i,
            "rect": pygame.Rect(
                x,
                chao - 65,
                42,
                65
            ),
            "x": float(x),
            "min": xmin,
            "max": xmax,
            "vel": rapidez,
            "direcao": 1,
            "vida": 100
        })

    # REPOSICIONAR KAEL
    jogador = pygame.Rect(
        70, 465, 40, 65
    )

    jogador_y = float(jogador.y)

    vy = 0
    pulos = 0
    direcao = 1
    invencivel = 65

    ataque_tempo = 0
    ataque_cooldown = 0

    atingidos = set()


def nova_partida():

    global vidas, pontuacao, tela_atual

    vidas = 3
    pontuacao = 0

    carregar_fase(1)

    tela_atual = "jogo"


def perder_vida():

    global vidas, jogador_y, vy
    global pulos, invencivel, tela_atual

    if invencivel > 0:
        return

    if tela_atual != "jogo":
        return

    vidas -= 1

    if vidas <= 0:

        tela_atual = "perdeu"

    else:

        jogador.topleft = (70, 465)
        jogador_y = float(jogador.y)

        vy = 0
        pulos = 0
        invencivel = 90

# ==========================================
# DESENHAR A FASE
# ==========================================

def desenhar_fase(tempo):

    fundo_animado(tempo)

    # ======================================
    # AGUA ANIMADA
    # ======================================

    pygame.draw.rect(
        tela,
        (20, 125, 215),
        (
            agua_x,
            545,
            agua_largura,
            105
        )
    )

    for i in range(5):

        y = 545 + 12 + i * 20

        pontos_onda = []

        for x in range(
            agua_x,
            agua_x + agua_largura + 1,
            3
        ):

            onda = math.sin(
                x * 0.08 + tempo * 3
            ) * 4

            pontos_onda.append(
                (x, int(y + onda))
            )

        if len(pontos_onda) > 1:

            pygame.draw.lines(
                tela,
                (95, 215, 255),
                False,
                pontos_onda,
                2
            )

    # ======================================
    # PLATAFORMAS
    # ======================================

    for plataforma, imagem in zip(
        plataformas,
        texturas
    ):

        tela.blit(
            imagem,
            plataforma.topleft
        )

    # ======================================
    # ESPINHOS BAIXOS
    # ======================================

    for x in range(
        agua_x + 5,
        agua_x + agua_largura - 14,
        19
    ):

        pygame.draw.polygon(
            tela,
            (55, 67, 83),
            [
                (x, 530),
                (x + 9, 518),
                (x + 19, 530)
            ]
        )

        pygame.draw.polygon(
            tela,
            PRATA,
            [
                (x + 4, 528),
                (x + 9, 521),
                (x + 15, 528)
            ]
        )

    # ======================================
    # MOEDAS
    # ======================================

    for moeda in moedas:

        flutuar = int(
            math.sin(
                tempo * 5 + moeda.x * 0.02
            ) * 4
        )

        tela.blit(
            moeda_img,
            (
                moeda.x,
                moeda.y + flutuar
            )
        )

    # ======================================
    # INIMIGOS SEM BARRA DE VIDA
    # ======================================

    for inimigo in inimigos:

        if inimigo["direcao"] < 0:
            imagem = lorde_esquerda
        else:
            imagem = lorde

        tela.blit(
            imagem,
            (
                inimigo["rect"].x - 10,
                inimigo["rect"].y - 20
            )
        )

    # ======================================
    # PORTA
    # ======================================

    tela.blit(
        porta_img,
        (855, 390)
    )

    # ======================================
    # KAEL
    # ======================================

    if (
        invencivel <= 0
        or int(tempo * 13) % 2 == 0
    ):

        if direcao < 0:
            imagem = kael_esquerda
        else:
            imagem = kael

        tela.blit(
            imagem,
            (
                jogador.x - 12,
                jogador.y - 18
            )
        )

    # ======================================
    # EFEITO DA ESPADA
    # ======================================

    if (
        tela_atual == "jogo"
        and ataque_tempo > 0
    ):

        if direcao > 0:
            cx = jogador.right + 27
        else:
            cx = jogador.left - 27

        centro = (
            cx,
            jogador.centery
        )

        pygame.draw.circle(
            tela,
            CIANO,
            centro,
            34,
            4
        )

        pygame.draw.arc(
            tela,
            BRANCO,
            (
                cx - 40,
                jogador.centery - 40,
                80,
                80
            ),
            -1.2,
            1.2,
            5
        )

    # ======================================
    # PLACAR
    # ======================================

    pygame.draw.rect(
        tela,
        (25, 42, 72),
        (10, 10, 980, 58),
        border_radius=14
    )

    escrever(
        f"FASE {fase}/5",
        fonte,
        CIANO,
        23, 25
    )

    escrever(
        f"VIDAS: {vidas}",
        fonte,
        BRANCO,
        175, 25
    )

    escrever(
        f"MOEDAS: {coletadas_fase}/5",
        fonte,
        BRANCO,
        340, 25
    )

    escrever(
        f"PONTOS: {pontuacao}",
        fonte,
        OURO,
        570, 25
    )

    escrever(
        config["nome"],
        pequena,
        BRANCO,
        790, 29
    )

# ==========================================
# TELAS DE RESULTADO
# ==========================================

def sobreposicao(
    titulo,
    subtitulo,
    extra=""
):

    tela.blit(
        sombra_fim,
        (0, 0)
    )

    escrever(
        titulo,
        grande,
        BRANCO,
        500, 265,
        True
    )

    escrever(
        subtitulo,
        media,
        CIANO,
        500, 345,
        True
    )

    if extra:

        escrever(
            extra,
            pequena,
            BRANCO,
            500, 406,
            True
        )

# ==========================================
# INICIAR O JOGO NO MENU
# ==========================================

fase = 1
vidas = 3
pontuacao = 0

carregar_fase(1)

tela_atual = "menu"
escolha = 0

rodando = True
tempo = 0.0

# ==========================================
# LOOP PRINCIPAL DO JOGO
# ==========================================

while rodando:

    dt = relogio.tick(FPS) / 1000

    tempo += dt

    # ======================================
    # EVENTOS
    # ======================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            rodando = False

        # MOVER MOUSE NO MENU
        elif (
            evento.type == pygame.MOUSEMOTION
            and tela_atual == "menu"
        ):

            escolha = -1

            for i, b in enumerate(botoes_menu):

                if b.collidepoint(evento.pos):

                    escolha = i
                    break

        # CLICAR COM O MOUSE
        elif (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):

            if tela_atual == "menu":

                for i, b in enumerate(botoes_menu):

                    if b.collidepoint(evento.pos):

                        if i == 0:

                            nova_partida()

                        elif i == 1:

                            tela_atual = "ajuda"

                        else:

                            rodando = False

                        break

            elif tela_atual == "ajuda":

                if voltar_rect.collidepoint(
                    evento.pos
                ):

                    tela_atual = "menu"
                    escolha = 0

        # TECLADO
        elif evento.type == pygame.KEYDOWN:

            # MENU PRINCIPAL
            if tela_atual == "menu":

                if evento.key == pygame.K_ESCAPE:

                    rodando = False

                elif evento.key in (
                    pygame.K_UP,
                    pygame.K_w
                ):

                    escolha = (escolha - 1) % 3

                elif evento.key in (
                    pygame.K_DOWN,
                    pygame.K_s
                ):

                    escolha = (escolha + 1) % 3

                elif evento.key in (
                    pygame.K_RETURN,
                    pygame.K_KP_ENTER,
                    pygame.K_SPACE
                ):

                    if escolha in (-1, 0):

                        nova_partida()

                    elif escolha == 1:

                        tela_atual = "ajuda"

                    elif escolha == 2:

                        rodando = False

            # COMO JOGAR
            elif tela_atual == "ajuda":

                if evento.key in (
                    pygame.K_ESCAPE,
                    pygame.K_RETURN,
                    pygame.K_BACKSPACE
                ):

                    tela_atual = "menu"
                    escolha = 0

            # DURANTE O JOGO
            elif tela_atual in (
                "jogo",
                "proxima",
                "venceu",
                "perdeu"
            ):

                if evento.key == pygame.K_ESCAPE:

                    tela_atual = "menu"
                    escolha = 0

                elif evento.key == pygame.K_r:

                    nova_partida()

                # PROXIMA FASE
                elif (
                    tela_atual == "proxima"
                    and evento.key in (
                        pygame.K_RETURN,
                        pygame.K_SPACE
                    )
                ):

                    carregar_fase(fase + 1)
                    tela_atual = "jogo"

                # RECOMECAR DEPOIS DO FIM
                elif (
                    tela_atual in (
                        "venceu",
                        "perdeu"
                    )
                    and evento.key == pygame.K_RETURN
                ):

                    nova_partida()

                # CONTROLES DO KAEL
                elif tela_atual == "jogo":

                    # PULO DUPLO
                    if (
                        evento.key in (
                            pygame.K_SPACE,
                            pygame.K_w,
                            pygame.K_UP
                        )
                        and pulos < 2
                    ):

                        vy = -14
                        pulos += 1

                    # ESPADA
                    if (
                        evento.key == pygame.K_j
                        and ataque_cooldown <= 0
                    ):

                        ataque_tempo = 12
                        ataque_cooldown = 24

                        atingidos.clear()

    # ======================================
    # ATUALIZAR JOGO
    # ======================================

    if tela_atual == "jogo":

        teclas = pygame.key.get_pressed()

        direita = (
            teclas[pygame.K_d]
            or teclas[pygame.K_RIGHT]
        )

        esquerda = (
            teclas[pygame.K_a]
            or teclas[pygame.K_LEFT]
        )

        movimento = (
            int(bool(direita))
            - int(bool(esquerda))
        )

        if movimento:
            direcao = movimento

        velocidade = 5

        if (
            teclas[pygame.K_LSHIFT]
            or teclas[pygame.K_RSHIFT]
        ):

            velocidade = 8

        # ANDAR
        jogador.x += movimento * velocidade

        jogador.x = max(
            0,
            min(
                LARGURA - jogador.width,
                jogador.x
            )
        )

        # ==================================
        # GRAVIDADE E PLATAFORMAS
        # ==================================

        antes = jogador.copy()

        vy = min(vy + 0.7, 16)

        jogador_y += vy
        jogador.y = round(jogador_y)

        for p in plataformas:

            if jogador.colliderect(p):

                # POUSAR NA PLATAFORMA
                if (
                    vy >= 0
                    and antes.bottom <= p.top
                ):

                    jogador.bottom = p.top
                    jogador_y = float(jogador.y)

                    vy = 0
                    pulos = 0

                # BATER A CABECA
                elif (
                    vy < 0
                    and antes.top >= p.bottom
                ):

                    jogador.top = p.bottom
                    jogador_y = float(jogador.y)

                    vy = 0

        # ==================================
        # COLETAR MOEDAS SEM TRAVAR
        # ==================================

        for i in range(
            len(moedas) - 1,
            -1,
            -1
        ):

            if jogador.colliderect(moedas[i]):

                moedas.pop(i)

                coletadas_fase += 1
                pontuacao += 10

        # ==================================
        # TEMPO DA ESPADA
        # ==================================

        if ataque_tempo > 0:
            ataque_tempo -= 1

        if ataque_cooldown > 0:
            ataque_cooldown -= 1

        ataque = None

        if ataque_tempo > 0:

            if direcao > 0:

                x_ataque = jogador.right

            else:

                x_ataque = jogador.left - 55

            ataque = pygame.Rect(
                x_ataque,
                jogador.y + 10,
                55,
                45
            )

        # ==================================
        # INIMIGOS
        # ==================================

        for inimigo in inimigos[:]:

            inimigo["x"] += inimigo["vel"]

            # VIRAR NA ESQUERDA
            if inimigo["x"] <= inimigo["min"]:

                inimigo["x"] = float(
                    inimigo["min"]
                )

                inimigo["vel"] = abs(
                    inimigo["vel"]
                )

                inimigo["direcao"] = 1

            # VIRAR NA DIREITA
            elif inimigo["x"] >= inimigo["max"]:

                inimigo["x"] = float(
                    inimigo["max"]
                )

                inimigo["vel"] = -abs(
                    inimigo["vel"]
                )

                inimigo["direcao"] = -1

            inimigo["rect"].x = round(
                inimigo["x"]
            )

            # KAEL ACERTA O INIMIGO
            if (
                ataque is not None
                and ataque.colliderect(
                    inimigo["rect"]
                )
                and inimigo["id"] not in atingidos
            ):

                atingidos.add(
                    inimigo["id"]
                )

                inimigo["vida"] -= 25

                # INIMIGO DERROTADO
                if inimigo["vida"] <= 0:

                    inimigos.remove(inimigo)

                    pontuacao += 50

                    continue

            # KAEL ENCOSTA NO INIMIGO
            if jogador.colliderect(
                inimigo["rect"]
            ):

                perder_vida()
                break

        # ==================================
        # ESPINHOS E QUEDAS
        # ==================================

        if (
            jogador.colliderect(espinhos)
            or jogador.top > ALTURA
        ):

            perder_vida()

        if invencivel > 0:

            invencivel -= 1

        # ==================================
        # PASSAR DE FASE
        # ==================================

        if (
            tela_atual == "jogo"
            and jogador.colliderect(porta_rect)
            and coletadas_fase == 5
        ):

            # BONUS POR COMPLETAR UMA FASE
            pontuacao += 100

            if fase == 5:

                tela_atual = "venceu"

            else:

                tela_atual = "proxima"

    # ======================================
    # DESENHAR AS TELAS
    # ======================================

    if tela_atual == "menu":

        desenhar_menu(tempo)
... 
...     elif tela_atual == "ajuda":
... 
...         desenhar_ajuda(tempo)
... 
...     else:
... 
...         desenhar_fase(tempo)
... 
...         # FASE CONCLUIDA
...         if tela_atual == "proxima":
... 
...             sobreposicao(
...                 f"FASE {fase} CONCLUIDA!",
...                 "ENTER: PROXIMA FASE",
...                 "+100 pontos de bonus | ESC: menu"
...             )
... 
...         # TODAS AS FASES CONCLUIDAS
...         elif tela_atual == "venceu":
... 
...             sobreposicao(
...                 "VOCE VENCEU!",
...                 "CONCLUIU AS 5 FASES!",
...                 f"PONTUACAO FINAL: {pontuacao}"
...             )
... 
...         # GAME OVER
...         elif tela_atual == "perdeu":
... 
...             sobreposicao(
...                 "GAME OVER",
...                 "ENTER: TENTAR NOVAMENTE",
...                 "R: reiniciar | ESC: menu"
...             )
... 
...     pygame.display.flip()
... 
... pygame.quit()
