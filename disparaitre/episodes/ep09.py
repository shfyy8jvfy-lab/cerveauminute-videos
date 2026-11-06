"""Épisode 9 — La tempête solaire géante (événement de Carrington, 1859).
Sources : Wikipédia « Carrington Event » ; NASA Science, « Near Miss: The Solar Superstorm of July 2012 »
(23/07/2014) ; PBS NewsHour (2014) ; Discover Magazine ; ScienceBlog / Silicon Canals (2025).
- 1er septembre 1859 : Richard Carrington (et Richard Hodgson) observent un flash blanc sur le Soleil.
- Le nuage de particules (éjection de masse coronale) atteint la Terre en ~17,6 h ; aurores visibles
  jusqu'à Cuba et aux Caraïbes ; télégraphes perturbés, opérateurs choqués, étincelles, papier enflammé.
- 23 juillet 2012 : une éjection aussi puissante croise l'orbite terrestre là où la Terre était
  une semaine plus tôt (NASA). Pete Riley (Space Weather, 2012) estime ~12 % de risque par décennie.
- Une répétition menacerait réseaux électriques (gros transformateurs), satellites, GPS ; ce serait
  une crise grave, pas une extinction. Des satellites (SOHO, etc.) surveillent le Soleil en continu.
"""
from engine import *

EPISODE = 9
BOOM_SCENE = 7
LEGENDE = """Épisode 9 : la tempête solaire géante ☀️⚡

En septembre 1859, une tempête solaire a fait briller des aurores jusqu'aux Caraïbes et mis le feu à du papier dans des bureaux de télégraphe. En juillet 2012, une tempête aussi forte a raté la Terre d'environ une semaine (NASA). Aujourd'hui, elle pourrait couper le courant longtemps… mais pas éteindre l'humanité.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #tempetesolaire #soleil #carrington #espace #astronomie #science #vulgarisation"""

# ---------- petits dessins ----------
def overlay(img, draw_fn):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    img.alpha_composite(layer)

def sun(d, cx, cy, r, t, col='#ffc23a', core='#fff1b0'):
    for i in range(12):
        a = i * math.pi / 6 + t * 0.4
        L = r * (1.25 + 0.12 * math.sin(t * 5 + i))
        line(d, [(cx + r * 1.05 * math.cos(a), cy + r * 1.05 * math.sin(a)), (cx + L * math.cos(a), cy + L * math.sin(a))], col, max(4, r * 0.09))
    circle(d, cx, cy, r, fill=hexc(col))
    circle(d, cx, cy, r * 0.72, fill=hexc(core))

def earth(d, cx, cy, r):
    circle(d, cx, cy, r, fill=hexc('#2f7de1'))
    d.ellipse([s(cx - r * 0.55), s(cy - r * 0.6), s(cx + r * 0.05), s(cy - r * 0.05)], fill=hexc('#46c46a'))
    d.ellipse([s(cx + r * 0.1), s(cy + r * 0.05), s(cx + r * 0.6), s(cy + r * 0.55)], fill=hexc('#46c46a'))

random.seed(19)
PARTS = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(5, 13)) for _ in range(90)]
def cme(d, cx, cy, spread, col='#ff8a3a'):
    for (u, v, r) in PARTS:
        if u * u + v * v > 1: continue
        circle(d, cx + u * spread * 0.8, cy + v * spread, r, fill=hexc(col))

def aurora(img, cx, cy, R, t, k):
    def f(dd):
        for j, col in enumerate(('#5dffa0', '#3ad6ff', '#c06bff')):
            pts = []
            for i in range(40):
                a = math.pi * (1.05 + 0.9 * i / 39)
                rr = R + 40 + j * 28 + 14 * math.sin(i * 0.6 + t * 4 + j)
                pts.append((s(cx + rr * math.cos(a)), s(cy + rr * math.sin(a))))
            dd.line(pts, fill=hexc(col, int(170 * k)), width=s(22), joint='curve')
    overlay(img, f)

def spark(d, x, y, t, col='#fff35a'):
    for i in range(6):
        a = i * math.pi / 3 + t * 7
        L = 22 + 14 * math.sin(t * 20 + i)
        line(d, [(x, y), (x + L * math.cos(a), y + L * math.sin(a))], col, 6)

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#160b2e'); stars(d, t); header(d, hexc('#ffc23a'))
    sun(d, 540, 640, 190 + 10 * math.sin(t * 3), t)
    text_block(img, ["Et si le Soleil nous coupait la lumière… sans même nous toucher ?"], t, 1080, '#ffffff', size=78)

def sc_flash(img, d, t, D):
    bg(d, '#3b1d0a'); header(d, hexc('#ffd28a'))
    sun(d, 540, 680, 190, t)
    k = ease((t - 0.9) / 0.3) * max(0.0, 1 - max(0, t - 1.6) / 1.6)
    if k > 0:
        circle(d, 590, 640, 50 * k + 10, fill=hexc('#ffffff'))
    ctext(d, "1859", 290, 70, '#ffd28a', FBK)
    text_block(img, ["Septembre 1859. L'astronome Richard Carrington voit un éclair blanc sur le Soleil."], t, 1060, '#ffffff', size=68)

def sc_cme(img, d, t, D):
    bg(d, '#0b2340'); stars(d, t); header(d, hexc('#9fd0ff'))
    sun(d, 150, 640, 170, t)
    earth(d, 900, 640, 70)
    k = ease((t - 0.3) / 3.2)
    cme(d, 330 + 450 * k, 640, 60 + 120 * k)
    text_block(img, ["Le Soleil vient de cracher un nuage géant de particules. Direction : la Terre."], t, 1060, '#ffffff', size=68)

def sc_aurora(img, d, t, D):
    bg(d, '#06231f'); stars(d, t); header(d, hexc('#8dffc4'))
    earth(d, 540, 700, 200)
    aurora(img, 540, 700, 200, t, ease((t - 0.3) / 0.8))
    text_block(img, ["Moins d'un jour plus tard, des aurores boréales illuminent le ciel… jusqu'aux Caraïbes."], t, 1060, '#ffffff', size=66)

def sc_telegraph(img, d, t, D):
    bg(d, '#2e2412'); header(d, hexc('#ffe08a'))
    sun(d, 920, 380, 70, t)
    for x in (200, 540, 880):
        d.rectangle([s(x - 12), s(520), s(x + 12), s(940)], fill=hexc('#a77b4f'))
        d.rectangle([s(x - 70), s(530), s(x + 70), s(550)], fill=hexc('#a77b4f'))
    for (x0, x1) in ((200, 540), (540, 880)):
        pts = [(x0 + (x1 - x0) * i / 20, 545 + 40 * math.sin(math.pi * i / 20)) for i in range(21)]
        line(d, pts, '#1a1206', 6)
    if t > 0.8:
        for i, (x, y) in enumerate(((370, 585), (710, 585), (200, 545), (880, 545))):
            if int(t * 8 + i * 3) % 3 != 0:
                spark(d, x, y, t + i)
    # papier qui brûle
    d.rectangle([s(620), s(780), s(760), s(930)], fill=hexc('#f4ead2'))
    if t > 1.6:
        fl = 30 + 12 * math.sin(t * 14)
        d.polygon([(s(650), s(790)), (s(690), s(790 - fl - 40)), (s(730), s(790))], fill=hexc('#ff7a1a'))
        d.polygon([(s(670), s(790)), (s(690), s(790 - fl)), (s(710), s(790))], fill=hexc('#ffd23a'))
    text_block(img, ["Les fils du télégraphe crépitent. Des opérateurs prennent des décharges, du papier prend feu."], t, 1060, '#ffffff', size=64)

def icon(d, kind, cx, cy, col):
    c = hexc(col)
    if kind == 'plug':
        d.rounded_rectangle([s(cx - 50), s(cy - 30), s(cx + 50), s(cy + 50)], radius=s(16), fill=c)
        for dx in (-22, 22): d.rectangle([s(cx + dx - 7), s(cy - 75), s(cx + dx + 7), s(cy - 30)], fill=c)
        d.rectangle([s(cx - 10), s(cy + 50), s(cx + 10), s(cy + 90)], fill=c)
    elif kind == 'phone':
        d.rounded_rectangle([s(cx - 45), s(cy - 80), s(cx + 45), s(cy + 80)], radius=s(16), fill=c)
        d.rounded_rectangle([s(cx - 33), s(cy - 62), s(cx + 33), s(cy + 55)], radius=s(6), fill=hexc('#14324a'))
    elif kind == 'pin':
        circle(d, cx, cy - 20, 48, fill=c)
        d.polygon([(s(cx - 40), s(cy)), (s(cx + 40), s(cy)), (s(cx), s(cy + 80))], fill=c)
        circle(d, cx, cy - 20, 18, fill=hexc('#14324a'))

def sat_icon(d, cx, cy, col):
    d.rectangle([s(cx - 25), s(cy - 25), s(cx + 25), s(cy + 25)], fill=hexc(col))
    d.rectangle([s(cx - 105), s(cy - 18), s(cx - 35), s(cy + 18)], fill=hexc('#7fc4ff'))
    d.rectangle([s(cx + 35), s(cy - 18), s(cx + 105), s(cy + 18)], fill=hexc('#7fc4ff'))

def sc_today(img, d, t, D):
    bg(d, '#14324a'); header(d, hexc('#a9e1ff'))
    items = [('plug', 300, 470), ('phone', 780, 470), ('sat', 300, 800), ('pin', 780, 800)]
    for i, (kind, x, y) in enumerate(items):
        k = ease((t - 0.4 - i * 0.35) / 0.3)
        if k <= 0: continue
        yy = y + 30 * (1 - k) + 6 * math.sin(t * 3 + i)
        if kind == 'sat': sat_icon(d, x, yy, '#ffffff')
        else: icon(d, kind, x, yy, '#ffffff')
    text_block(img, ["En 1859, il n'y avait que le télégraphe.", ("Aujourd'hui : électricité, téléphones, satellites, GPS…", 1.2)], t, 1060, '#ffffff', size=66)

random.seed(29)
WINDOWS = [(bx, random.uniform(0, 1)) for bx in range(8)]
def sc_blackout(img, d, t, D):
    bg(d, '#05050a'); header(d, hexc('#ff8a8a'))
    off = t > 1.4
    for i in range(8):
        x0 = 70 + i * 120; h = 220 + (i * 97) % 260
        d.rectangle([s(x0), s(950 - h), s(x0 + 105), s(950)], fill=hexc('#1c1c2a'))
        for wy in range(int(950 - h + 25), 930, 50):
            for wx in (x0 + 18, x0 + 62):
                lit = (not off) or (t < 1.4 + (i / 8) * 0.8 and (wx + wy) % 3 == 0)
                d.rectangle([s(wx), s(wy), s(wx + 25), s(wy + 25)], fill=hexc('#ffd86a' if lit else '#2a2a38'))
    if 1.3 < t < 1.6:
        bg(d, '#ffffff')
    text_block(img, [("Une tempête pareille aujourd'hui pourrait griller d'énormes transformateurs. Et couper le courant pendant des mois.", 1.5)], t, 1040, '#ffffff', size=64)

def sc_joke(img, d, t, D):
    bg(d, '#ffe4ec'); header(d, hexc('#a03050'))
    d.rounded_rectangle([s(400), s(340), s(680), s(900)], radius=s(40), fill=hexc('#2b1a22'))
    d.rounded_rectangle([s(425), s(380), s(655), s(860)], radius=s(14), fill=hexc('#fff6f8'))
    d.rounded_rectangle([s(470), s(560), s(590), s(640)], radius=s(10), outline=hexc('#2b1a22'), width=s(8))
    d.rectangle([s(590), s(585), s(604), s(615)], fill=hexc('#2b1a22'))
    if int(t * 2.5) % 2 == 0:
        d.rectangle([s(480), s(570), s(490), s(630)], fill=hexc('#ff3b5c'))
    ctext(d, "3 %", 670, 54, '#ff3b5c', FBK)
    text_block(img, ["Le vrai cauchemar : téléphone à 3 %…", ("…et plus une seule prise qui marche.", 1.5)], t, 1030, '#2b1a22', size=70)

def sc_near_miss(img, d, t, D):
    bg(d, '#1d0f33'); stars(d, t); header(d, hexc('#d7b8ff'))
    sun(d, 540, 640, 80, t)
    d.ellipse([s(240), s(340), s(840), s(940)], outline=hexc('#6a5a8a'), width=s(4))
    ang = -0.5 + 0.35 * ease(t / 2.0)
    earth(d, 540 + 300 * math.cos(ang), 640 + 300 * math.sin(ang), 38)
    k = ease((t - 0.6) / 2.4)
    a0 = 0.25
    cme(d, 540 + (110 + 230 * k) * math.cos(a0), 640 + (110 + 230 * k) * math.sin(a0), 25 + 55 * k)
    ctext(d, "JUILLET 2012", 300, 56, '#d7b8ff', FBK)
    text_block(img, ["En 2012, une tempête aussi forte est passée sur l'orbite de la Terre…", ("…là où on était une semaine plus tôt.", 2.0)], t, 1060, '#ffffff', size=64)

def sc_proba(img, d, t, D):
    bg(d, '#0f2a1c'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.4)
    n = int(min(12, 12 * ease(t / 1.0)))
    ctext(d, f"{n} %", 440, 220, '#a8f0c0', FBK, k)
    ctext(d, "de risque par décennie (estimation de 2012)", 720, 40, '#a8f0c0', FM, k)
    text_block(img, [("Ce serait une crise énorme. Mais elle couperait le courant… pas l'humanité.", 1.0)], t, 1040, '#ffffff', size=68)

def sc_watch(img, d, t, D):
    bg(d, '#2a1a3d'); stars(d, t); header(d, hexc('#ffd28a'))
    sun(d, 220, 640, 120, t)
    sat_icon(d, 760, 600 + 15 * math.sin(t * 2), '#ffffff')
    for i in range(3):
        r = 60 + ((t * 120 + i * 60) % 180)
        d.arc([s(760 - r), s(600 - r), s(760 + r), s(600 + r)], 150, 210, fill=hexc('#ffd28a'), width=s(6))
    text_block(img, ["Bonne nouvelle : des satellites surveillent le Soleil jour et nuit. On verrait le nuage partir."], t, 1060, '#ffffff', size=64)

sc_title = scene_title(["TEMPÊTE", "SOLAIRE"], "Scénario d'extinction n°9")
sc_end = scene_end("Bref : le Soleil peut couper Internet. Pas votre avis d'impôt.")

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_flash, 4.4), (sc_cme, 4.2), (sc_aurora, 4.2),
    (sc_telegraph, 4.4), (sc_today, 4.2), (sc_blackout, 4.6), (sc_joke, 4.4),
    (sc_near_miss, 5.0), (sc_proba, 5.0), (sc_watch, 4.4), (sc_end, 4.6),
]
