"""Épisode 19 — La disparition des pollinisateurs.
Sources :
- Citation « Si l'abeille disparaissait, l'homme n'aurait plus que quatre ans à vivre » : attribuée à Einstein
  sans aucune preuve ; plus ancienne trace connue en 1994, lors d'une manifestation d'apiculteurs à Bruxelles
  (Quote Investigator, 27 août 2013 ; Africa Check ; famousscientists.org). Einstein est mort en 1955.
- Environ 75 % des types de cultures alimentaires mondiales profitent de la pollinisation animale
  (Klein et al. 2007 ; rapport IPBES 2016 ; World Economic Forum 2019).
- Blé, riz, maïs : pollinisés par le vent ; seuls ~5 à 8 % de la production agricole mondiale sont directement
  attribuables aux pollinisateurs (IPBES 2016 ; Our World in Data, « pollinator dependence »).
- Smith et al., The Lancet, 2015 : une perte totale des pollinisateurs causerait environ 1,42 million de décès
  supplémentaires par an (carences en vitamine A et folates, maladies) (Harvard / The Lancet ; Pourquoi Docteur).
- Déclin réel : pesticides, maladies, perte d'habitat ; en Europe ~9 % des espèces d'abeilles sauvages menacées
  (Liste rouge européenne des abeilles, UICN 2014) ; IPBES 2016.
- Consensus : pas une menace d'extinction de l'humanité, mais un risque sérieux pour la nutrition et l'agriculture.
"""
from engine import *

EPISODE = 19
BOOM_SCENE = 6
LEGENDE = """Épisode 19 : et si toutes les abeilles disparaissaient ? 🐝🍽️

« Sans abeilles, l'humanité n'a plus que quatre ans » : Einstein n'a jamais dit ça (aucune trace avant 1994). Le blé, le riz et le maïs sont pollinisés par le vent. Mais sans pollinisateurs, adieu une bonne partie des fruits, légumes, café et chocolat : environ 1,4 million de morts en plus par an selon une étude du Lancet (2015).

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #abeilles #pollinisateurs #biodiversité #nature #science #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def bee(d, x, y, t, sc=1.0):
    """Abeille simple : corps rayé + ailes qui battent."""
    flap = 0.6 + 0.4 * abs(math.sin(t * 30))
    for side in (-1, 1):
        d.ellipse([s(x - 10 * sc + side * 4), s(y - 70 * sc * flap), s(x + 30 * sc + side * 4), s(y - 10)], fill=hexc('#e8f6ff', 200))
    d.ellipse([s(x - 50 * sc), s(y - 30 * sc), s(x + 50 * sc), s(y + 30 * sc)], fill=hexc('#ffc93c'))
    for k in (-18, 8):
        d.rectangle([s(x + k * sc), s(y - 28 * sc), s(x + (k + 12) * sc), s(y + 28 * sc)], fill=hexc('#2b1a10'))
    circle(d, x + 48 * sc, y, 16 * sc, fill=hexc('#2b1a10'))

def flower(d, x, y, col, r=46, center='#ffd166', stem=True):
    if stem:
        line(d, [(x, y + r), (x, y + r + 160)], '#3a7d44', 10)
    for k in range(6):
        a = k * math.pi / 3
        circle(d, x + math.cos(a) * r * 0.75, y + math.sin(a) * r * 0.75, r * 0.55, fill=hexc(col))
    circle(d, x, y, r * 0.45, fill=hexc(center))

# Fil rouge : l'assiette du monde
FOODS = [  # (dx, dy, r, couleur, dépend des pollinisateurs ?)
    (-130, -40, 52, '#e63946', True),   # pomme
    (-20, -95, 38, '#ff6b6b', True),    # fraise
    (110, -60, 48, '#f4a261', True),    # orange / abricot
    (130, 60, 40, '#6a4c93', True),     # myrtilles
    (-120, 80, 42, '#2a9d8f', True),    # légume vert
    (10, 90, 44, '#5c3a21', True),      # café / chocolat
    (0, 0, 46, '#e9d8a6', False),       # blé (pain)
]
def plate(d, cx, cy, t, keep=1.0, only_wind=False, beige=0.0, wobble=0.0):
    w = wobble * math.sin(t * 40)
    d.ellipse([s(cx - 300 + w), s(cy - 210), s(cx + 300 + w), s(cy + 210)], fill=hexc('#f7f7f2'))
    d.ellipse([s(cx - 240 + w), s(cy - 165), s(cx + 240 + w), s(cy + 165)], outline=hexc('#d9d9cf'), width=s(6))
    for (dx, dy, r, col, poll) in FOODS:
        if poll and only_wind:
            continue
        if poll and beige > 0:
            rr = r * (1 - beige)
            if rr < 3: continue
            circle(d, cx + dx + w, cy + dy, rr, fill=hexc(col, int(255 * (1 - beige))))
        else:
            circle(d, cx + dx + w, cy + dy, r * keep if poll else r, fill=hexc(col))
            if not poll:
                for k in range(-1, 2):
                    line(d, [(cx + dx + k * 14 + w, cy + dy - 30), (cx + dx + k * 14 + w, cy + dy + 30)], '#c9a86a', 5)

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#14361f'); header(d, hexc('#b8f0c0'))
    flower(d, 400, 620, '#ff8fab'); flower(d, 700, 680, '#c9b8ff')
    bx = 300 + 350 * ((t * 0.35) % 1.0); by = 470 + 40 * math.sin(t * 4)
    bee(d, bx, by, t, sc=1.8)
    text_block(img, ["Si les abeilles disparaissent… on meurt tous en quatre ans ?"], t, 1080, '#ffffff', size=76)

def sc_einstein(img, d, t, D):
    bg(d, '#3a2a0a'); header(d, hexc('#ffe08a'))
    bob = 8 * math.sin(t * 3)
    d.rounded_rectangle([s(220), s(420 + bob), s(860), s(700 + bob)], radius=s(40), fill=hexc('#fff3c4'))
    d.text((s(540), s(520 + bob)), "« 4 ans ! »", font=font(FBK, 80), fill=hexc('#3a2a0a'), anchor='mm')
    d.text((s(540), s(620 + bob)), "— soi-disant Einstein", font=font(FM, 38), fill=hexc('#7a5a1a'), anchor='mm')
    k = ease((t - 1.6) / 0.3)
    if k > 0:
        line(d, [(250, 760), (830, 380)], hexc('#e63946', int(255 * k)), 18)
    text_block(img, ["La phrase est attribuée à Einstein. Aucune trace avant 1994.", ("Il est mort en 1955.", 1.6)], t, 1060, '#ffffff', size=66)

def sc_pollen(img, d, t, D):
    bg(d, '#1d3557'); header(d, hexc('#a8dadc'))
    flower(d, 260, 600, '#ffb4a2'); flower(d, 820, 600, '#ffb4a2')
    p = (t * 0.45) % 1.0
    bx = 260 + 560 * p; by = 470 - 120 * math.sin(p * math.pi)
    bee(d, bx, by, t, sc=1.6)
    for k in range(4):
        circle(d, bx - 70 - k * 34, by + 50 + 6 * math.sin(t * 8 + k), 9, fill=hexc('#ffd166', 220 - k * 45))
    text_block(img, ["Les pollinisateurs (abeilles, mouches, papillons…) portent le pollen de fleur en fleur. Sans ça : pas de fruit."], t, 1050, '#ffffff', size=60)

def sc_plate_full(img, d, t, D):
    bg(d, '#5a189a'); header(d, hexc('#e0c3fc'))
    plate(d, 540, 640, t, keep=0.85 + 0.15 * ease(t / 0.6))
    text_block(img, ["Trois cultures alimentaires sur quatre en profitent : pommes, fraises, tomates, café, chocolat…"], t, 1060, '#ffffff', size=64)

def sc_wind(img, d, t, D):
    bg(d, '#0f4c5c'); header(d, hexc('#a8e6cf'))
    plate(d, 540, 730, t)
    for k in range(3):
        x0 = -200 + ((t * 420 + k * 380) % 1500)
        y0 = 360 + k * 60
        line(d, [(x0, y0), (x0 + 300, y0), (x0 + 360, y0 - 40)], '#e0f7fa', 14)
    text_block(img, ["Mais le blé, le riz et le maïs sont pollinisés par le vent.", ("Eux, ils s'en fichent.", 1.6)], t, 1060, '#ffffff', size=68)

def sc_boom(img, d, t, D):
    bg(d, '#6a040f'); header(d, hexc('#ffb3c1'))
    b = ease((t - 0.2) / 1.2)
    plate(d, 540, 640, t, beige=b, wobble=10 if t < 1.0 else 0)
    text_block(img, ["Plus aucun pollinisateur ? Adieu une grosse partie des fruits et légumes.", ("L'assiette devient beige.", 1.8)], t, 1060, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    d.rounded_rectangle([s(340), s(500), s(740), s(780)], radius=s(60), fill=hexc('#d4a373'))
    d.rounded_rectangle([s(370), s(530), s(710), s(750)], radius=s(48), fill=hexc('#f1dcb4'))
    k = ease((t - 0.8) / 0.4)
    y = 400 - 30 * k
    d.text((s(540), s(y)), "…et c'est tout.", font=font(FBK, 56), fill=hexc('#8a5a3c', int(255 * k)), anchor='mm')
    text_block(img, ["Le petit-déjeuner du futur : du pain sec.", ("Sans confiture. Sans café. Sans chocolat.", 1.4)], t, 1040, '#2b1a10', size=68)

def sc_lancet(img, d, t, D):
    bg(d, '#2b2d42'); header(d, hexc('#edf2f4'))
    n = int(1400000 * ease(t / 1.4))
    d.text((s(540), s(560)), f"{n:,}".replace(',', ' '), font=font(FBK, 130), fill=hexc('#ff8fa3'), anchor='mm')
    d.text((s(540), s(700)), "morts en plus par an", font=font(FB, 50), fill=hexc('#edf2f4'), anchor='mm')
    text_block(img, ["Une étude (The Lancet, 2015) : sans aucun pollinisateur, environ 1,4 million de morts en plus par an, surtout par carences."], t, 1040, '#ffffff', size=58)

def sc_ipbes(img, d, t, D):
    bg(d, '#283618'); header(d, hexc('#dde5b6'))
    cx, cy, r = 540, 620, 230
    k = ease(t / 1.0)
    d.pieslice([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], 0, 360, fill=hexc('#a3b18a'))
    d.pieslice([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], -90, -90 + 360 * 0.07 * k, fill=hexc('#e63946'))
    text_block(img, ["Au total, les récoltes mondiales baisseraient d'environ 5 à 8 %.", ("Pas zéro. Pas rien non plus.", 1.6)], t, 1060, '#ffffff', size=66)

def sc_decline(img, d, t, D):
    bg(d, '#7b2cbf'); header(d, hexc('#e0c3fc'))
    for i in range(10):
        x = 140 + i * 90
        poor = (i == 6)
        fade = ease((t - 1.0) / 0.6) if poor else 0
        bee(d, x + 20, 600 + 12 * math.sin(t * 3 + i), t + i, sc=0.75)
        if fade > 0:
            circle(d, x + 20, 600, 60, outline=hexc('#ff4d6d', int(255 * fade)), width=8)
    text_block(img, ["Et le déclin est réel : pesticides, maladies, champs sans fleurs. En Europe, près d'une abeille sauvage sur dix est menacée."], t, 1020, '#ffffff', size=58)

def sc_science(img, d, t, D):
    bg(d, '#0b2545'); header(d, hexc('#9fc2ff'))
    plate(d, 540, 640, t, beige=0.45)
    text_block(img, ["Ce que disent les scientifiques : ce n'est pas la fin de l'humanité. Mais une assiette plus triste, et des carences."], t, 1060, '#ffffff', size=60)

sc_title = scene_title(["SANS", "ABEILLES"], "Scénario d'extinction n°19", color='#9d6b00')
sc_end = scene_end("Bref : sans abeilles, on survit. Sans miel, sans café… mais toujours avec les impôts.", color='#9d6b00')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_einstein, 4.4), (sc_pollen, 4.6), (sc_plate_full, 4.2),
    (sc_wind, 4.2), (sc_boom, 4.0), (sc_joke, 4.0), (sc_lancet, 4.8), (sc_ipbes, 4.2),
    (sc_decline, 4.8), (sc_science, 4.4), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Si les abeilles disparaissent… on meurt tous en quatre ans ?",
    "Scénario d'extinction numéro dix-neuf : sans abeilles.",
    "La phrase est attribuée à Einstein. Aucune trace avant mille neuf cent quatre-vingt-quatorze. Il est mort en mille neuf cent cinquante-cinq.",
    "Les pollinisateurs, abeilles, mouches, papillons, portent le pollen de fleur en fleur. Sans ça : pas de fruit.",
    "Trois cultures alimentaires sur quatre en profitent : pommes, fraises, tomates, café, chocolat…",
    "Mais le blé, le riz et le maïs sont pollinisés par le vent. Eux, ils s'en fichent.",
    "Plus aucun pollinisateur ? Adieu une grosse partie des fruits et légumes. L'assiette devient beige.",
    "Le petit-déjeuner du futur : du pain sec. Sans confiture. Sans café. Sans chocolat.",
    "Une étude du Lancet estime : sans aucun pollinisateur, environ un million quatre cent mille morts en plus par an.",
    "Au total, les récoltes mondiales baisseraient d'environ cinq à huit pour cent. Pas zéro. Pas rien non plus.",
    "Et le déclin est réel. En Europe, près d'une abeille sauvage sur dix est menacée.",
    "Ce que disent les scientifiques : ce n'est pas la fin de l'humanité. Mais une assiette plus triste, et des carences.",
    "Bref : sans abeilles, on survit. Sans miel, sans café… mais toujours avec les impôts. Abonnez-vous. Tant qu'il y a un demain.",
]
