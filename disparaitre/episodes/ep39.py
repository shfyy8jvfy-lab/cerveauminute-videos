"""Épisode 39 — Mythe : le champignon zombie (Cordyceps) qui contamine les humains.
Sources :
- Library of Congress, « What's up with zombie ants? » (Everyday Mysteries, 2024) : une spore se fixe sur la
  fourmi et perce sa carapace (enzymes + pression) ; le champignon se nourrit de l'intérieur et se répand ;
  la fourmi quitte les pistes de la colonie, erre, grimpe sur une tige ou une brindille et s'y accroche avec
  ses mâchoires ; elle meurt peu après ; quelques jours plus tard une tige sort de sa tête et libère des
  spores ; le champignon semble agir directement sur les muscles plutôt que via le cerveau (présent partout
  sauf dans le cerveau) ; 35 espèces d'Ophiocordyceps connues (2023) capables de contrôler des fourmis ;
  la plupart ne peuvent même pas passer à une autre espèce de fourmi ; « le corps humain est trop chaud pour
  la plupart des champignons ».
- NPR, « The zombie fungus from 'The Last Of Us' is real — but not nearly as deadly » (30 janv. 2023,
  B. Dentinger, Field Museum) : le champignon ne peut pas infecter les humains ; notre température corporelle
  est trop élevée ; traits très spécifiques à l'insecte ; le réchauffement aide certains champignons à
  supporter la chaleur, mais « aucun n'est un cordyceps ».
- Scientific American, interview de Tom Chiller (CDC), 2023 : aucune espèce d'Ophiocordyceps n'envahit
  poissons, amphibiens ou mammifères ; « pour Ophiocordyceps, aucune chance » ; vraie inquiétude : des
  champignons émergents résistants aux médicaments (ex. Candida auris).
"""
from engine import *

EPISODE = 39
BOOM_SCENE = 5
LEGENDE = """Épisode 39 : le champignon zombie 🍄🐜

Le champignon « zombie » existe vraiment : il pousse dans les fourmis, les fait grimper sur une tige, puis fait sortir une tige de leur tête pour pleuvoir des spores. Mais chaque espèce vise en général une seule espèce de fourmi, et notre corps à 37 °C est bien trop chaud pour lui. Aucun ne s'attaque aux mammifères (Library of Congress, CDC). Le vrai sujet : d'autres champignons résistants aux médicaments.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #champignon #zombie #fourmis #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def ant(d, cx, cy, sc, t, col='#2b1b12', walk=1.0, angle=0.0, stalk=0.0, spots=0.0):
    """Le fil rouge : une fourmi simple (3 boules, 6 pattes, 2 antennes)."""
    ca, sa = math.cos(angle), math.sin(angle)
    def P(x, y):
        return (cx + (x * ca - y * sa) * sc, cy + (x * sa + y * ca) * sc)
    c = hexc(col)
    # pattes
    for i, x in enumerate((-12, 8, 28)):
        ph = math.sin(t * 10 * walk + i * 2.1) * 10 * walk
        for side in (-1, 1):
            a, b, e = P(x, 0), P(x + ph * side, 34 * side), P(x + ph * side - 10, 52 * side)
            line(d, [a, b, e], col, max(3, int(6 * sc)))
    # corps
    for x, r in ((-42, 26), (8, 16), (50, 20)):
        px, py = P(x, 0)
        circle(d, px, py, r * sc, fill=c)
    # antennes
    for side in (-1, 1):
        wob = 4 * math.sin(t * 6 + side)
        line(d, [P(64, 6 * side), P(84, (18 + wob) * side), P(98, (12 + wob) * side)], col, max(3, int(5 * sc)))
    # taches de champignon
    if spots > 0:
        for j, (x, y) in enumerate(((-48, -8), (-34, 10), (4, 4), (-56, 6))):
            if j < spots * 4:
                px, py = P(x, y)
                circle(d, px, py, 6 * sc, fill=hexc('#ffb347'))
    # tige qui sort de la tête
    if stalk > 0:
        hx, hy = P(50, 0)
        L = 120 * stalk * sc
        tip = (hx + 6 * math.sin(t * 2), hy - L)
        line(d, [(hx, hy), tip], '#e8a33a', max(4, int(9 * sc)))
        circle(d, tip[0], tip[1], 18 * sc * stalk, fill=hexc('#ffb347'))

def twig(d, x, y0, y1, col='#5a3a1e'):
    line(d, [(x, y0), (x + 10, (y0 + y1) / 2), (x, y1)], col, 16)
    d.ellipse([s(x + 4), s(y1 + 40), s(x + 120), s(y1 + 90)], fill=hexc('#4f9a4a'))

def spores(d, x0, y0, t, n=24, col='#ffe08a', fall=420):
    for i in range(n):
        ph = (t * 160 + i * 37) % fall
        x = x0 + (i % 8 - 3.5) * 46 + 14 * math.sin(t * 3 + i)
        circle(d, x, y0 + ph, 6 + (i % 3) * 2, fill=hexc(col))

def thermo(d, cx, cy, level, col='#ff4d4d'):
    d.rounded_rectangle([s(cx - 26), s(cy - 260), s(cx + 26), s(cy + 150)], radius=s(26), fill=hexc('#f3ead6'))
    circle(d, cx, cy + 170, 52, fill=hexc(col))
    top = cy + 150 - 380 * level
    d.rounded_rectangle([s(cx - 12), s(top), s(cx + 12), s(cy + 160)], radius=s(12), fill=hexc(col))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#1f3a2a'); header(d, hexc('#a8e0b5'))
    for i in range(3):
        ant(d, 200 + i * 330 + 30 * math.sin(t + i), 620 + 90 * (i % 2), 1.6, t + i)
    text_block(img, ["Et si un champignon transformait l'humanité en zombies ?"], t, 1080, '#ffffff', size=74)

def sc_real(img, d, t, D):
    bg(d, '#2d2a4a'); header(d, hexc('#cfc8ff'))
    k = ease(t / 1.2)
    ant(d, 520, 640, 1.6 + 0.8 * k, t, walk=0.6)
    text_block(img, ["Le champignon « zombie » existe vraiment (Ophiocordyceps).", ("Sa cible préférée ? Les fourmis.", 1.4)], t, 1040, '#ffffff', size=64)

def sc_spore(img, d, t, D):
    bg(d, '#4a3a14'); header(d, hexc('#ffe3a3'))
    ant(d, 500, 680, 2.4, t, walk=0.3, spots=ease((t - 1.6) / 1.6))
    k = ease((t - 0.2) / 1.2)
    circle(d, 900 - 300 * k, 360 + 280 * k, 16, fill=hexc('#ffb347'))
    text_block(img, ["Une spore se colle sur une fourmi et perce sa carapace.", ("Puis le champignon grandit à l'intérieur.", 1.5)], t, 1040, '#ffffff', size=64)

def sc_climb(img, d, t, D):
    bg(d, '#123f4a'); header(d, hexc('#a6e6f2'))
    twig(d, 600, 940, 380)
    k = ease((t - 0.3) / 2.6)
    ant(d, 600, 860 - 400 * k, 1.2, t, walk=1.0, angle=-math.pi / 2, spots=1)
    text_block(img, ["La fourmi quitte les copines, erre, puis grimpe sur une tige…", ("…et s'y accroche avec ses mâchoires. Pour de bon.", 1.7)], t, 1040, '#ffffff', size=62)

def sc_boom(img, d, t, D):
    bg(d, '#5c1020'); header(d, hexc('#ffb3c0'))
    twig(d, 780, 940, 380, col='#3d2414')
    st = ease((t - 0.4) / 1.4)
    ant(d, 780, 560, 1.2, t, walk=0.0, angle=-math.pi / 2, spots=1, stalk=st)
    if t > 1.6:
        spores(d, 740, 300, t - 1.6, fall=650)
    kk = ease((t - 1.6) / 0.3)
    if kk > 0:
        d.text((s(110), s(560)), "POUF !", font=font(FBK, 110), fill=hexc('#ffd166', int(255 * kk)))
    text_block(img, ["Quelques jours après, une tige lui sort de la tête…", ("…et fait pleuvoir des spores sur toute la colonie.", 1.9)], t, 1040, '#ffffff', size=64)

def sc_muscles(img, d, t, D):
    bg(d, '#3a1f4f'); header(d, hexc('#e0c2ff'))
    ant(d, 540, 640, 3.0, t, walk=0.4, spots=1)
    # fils du champignon autour, sauf la tête
    for i in range(6):
        x = 300 + i * 50
        line(d, [(x, 560 + 20 * math.sin(t * 2 + i)), (x + 30, 720 + 20 * math.cos(t * 2 + i))], '#ffb347', 5)
    text_block(img, ["Le plus fou : il laisse le cerveau intact.", ("Il semble piloter surtout… les muscles.", 1.4)], t, 1040, '#ffffff', size=64)

def sc_joke(img, d, t, D):
    bg(d, '#ffe9d1'); header(d, hexc('#8a4a00'))
    # tasse de café qui fume
    d.rounded_rectangle([s(400), s(520), s(640), s(820)], radius=s(36), fill=hexc('#7a4a2a'))
    d.arc([s(610), s(580), s(730), s(740)], 270, 90, fill=hexc('#7a4a2a'), width=s(22))
    for i in range(3):
        y = 480 - ((t * 60 + i * 40) % 140)
        line(d, [(460 + i * 60, 500), (470 + i * 60 + 15 * math.sin(t * 3 + i), y)], '#b08a6a', 8)
    kk = ease((t - 0.3) / 0.4)
    ctext(d, "LUNDI 7 H", 340, 64, '#8a4a00', FBK, kk)
    text_block(img, ["Un peu comme vous le lundi matin : le corps avance…", ("…mais ce n'est pas vraiment vous aux commandes.", 1.6)], t, 1040, '#3a2200', size=60)

def sc_specific(img, d, t, D):
    bg(d, '#14402e'); header(d, hexc('#a8f0c8'))
    cols = ['#2b1b12', '#7a2b1b', '#1b2b4a']
    for i, c in enumerate(cols):
        ant(d, 260 + i * 280, 560, 1.0, t + i, col=c, spots=1 if i == 0 else 0)
    k = ease((t - 1.2) / 0.4)
    if k > 0:
        for x in (540, 820):
            line(d, [(x - 60, 700), (x + 60, 820)], '#ff4d4d', 14)
            line(d, [(x + 60, 700), (x - 60, 820)], '#ff4d4d', 14)
    text_block(img, ["Mais en général, chaque espèce vise une seule espèce de fourmi.", ("Elle n'arrive même pas à changer de fourmi !", 1.5)], t, 1040, '#ffffff', size=60)

def sc_heat(img, d, t, D):
    bg(d, '#4f2a10'); header(d, hexc('#ffd0a6'))
    thermo(d, 260, 600, 0.3 + 0.5 * ease((t - 0.3) / 1.6))
    kk = ease((t - 0.6) / 0.4)
    ctext(d, "37 °C", 560, 120, '#ffd166', FBK, kk)
    text_block(img, ["Et nous sommes bien trop chauds pour lui.", ("Aucun ne s'attaque aux mammifères. Ni aux poissons.", 1.5)], t, 1040, '#ffffff', size=62)

def sc_science(img, d, t, D):
    bg(d, '#14324f'); header(d, hexc('#a6d4ff'))
    ant(d, 540, 640, 1.8, t, walk=0.5)
    kk = ease((t - 0.4) / 0.4)
    if kk > 0:
        d.rounded_rectangle([s(290), s(320), s(790), s(420)], radius=s(30), fill=hexc('#ffd166', int(255 * kk)))
        ctext(d, "ZÉRO CHANCE", 338, 58, '#14324f', FBK, kk)
    text_block(img, ["Verdict des experts (dont le CDC américain) : aucun risque.", ("Le vrai souci : d'autres champignons, résistants aux médicaments.", 1.8)], t, 1030, '#ffffff', size=58)

sc_title = scene_title(["LE CHAMPI", "ZOMBIE"], "Scénario d'extinction n°39 · mythe")
sc_end = scene_end("Bref : pas de zombies. Mais le fisc, lui, ne lâche jamais prise.")

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_real, 4.4), (sc_spore, 4.4), (sc_climb, 4.6),
    (sc_boom, 4.8), (sc_muscles, 4.4), (sc_joke, 4.2), (sc_specific, 4.6),
    (sc_heat, 4.4), (sc_science, 4.8), (sc_end, 4.8),
]
