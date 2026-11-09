"""Épisode 17 — L'effet de serre emballé (devenir comme Vénus).
Sources :
- Vénus : température de surface ~465 °C, atmosphère surtout de CO2, pression ~90 fois celle de la Terre
  (NASA ; Universe Today / Gizmodo « Why is Venus so horrible » ; StarDate). Le plomb fond à 327 °C.
- Effet de serre emballé : la chaleur fait évaporer l'eau, la vapeur d'eau (gaz à effet de serre) réchauffe
  davantage, jusqu'à l'évaporation des océans (Wikipedia « Runaway greenhouse effect », avec références).
- GIEC, AR5 GT1 ch. 12 : un effet de serre emballé comparable à Vénus « semble n'avoir pratiquement aucune chance »
  d'être provoqué par les activités humaines (cité par Science Feedback, revue de l'affirmation de S. Hawking).
- Le Soleil gagne ~10 % de luminosité par milliard d'années ; dans ~1 milliard d'années, la Terre perdra ses océans
  (Schröder & Smith 2008, « Distant future of the Sun and Earth revisited », arXiv:0801.4031).
"""
from engine import *

EPISODE = 17
BOOM_SCENE = 6
LEGENDE = """Épisode 17 : l'effet de serre emballé (devenir comme Vénus) 🔥🌍

Sur Vénus, il fait 465 °C : assez pour faire fondre du plomb. Si la chaleur faisait s'évaporer nos océans, la Terre pourrait finir pareil. Bonne nouvelle : selon le GIEC, cet emballement n'a pratiquement aucune chance d'être causé par nos activités. Le vrai coupable sera le Soleil… dans environ un milliard d'années.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #venus #climat #effetdeserre #espace #science #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def mix(c1, c2, k):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    k = max(0, min(1, k))
    return '#%02x%02x%02x' % tuple(int(b[j] + (a[j] - b[j]) * k) for j in range(3))

def earth(d, cx, cy, r, heat=0.0):
    """Fil rouge : la Terre, qui vire à l'orange quand elle chauffe (heat 0 → 1)."""
    if heat < 0.5:
        ocean = mix('#d8b26e', '#4fa3ff', heat * 2); land = mix('#a07a3a', '#6bd17a', heat * 2)
    else:
        ocean = mix('#d9480f', '#d8b26e', heat * 2 - 1); land = mix('#7a2e0e', '#a07a3a', heat * 2 - 1)
    circle(d, cx, cy, r, fill=hexc(ocean))
    circle(d, cx - r * 0.3, cy - r * 0.2, r * 0.35, fill=hexc(land))
    circle(d, cx + r * 0.35, cy + r * 0.3, r * 0.25, fill=hexc(land))

def venus(d, cx, cy, r, t):
    circle(d, cx, cy, r, fill=hexc('#e9b949'))
    for i in range(4):
        y = cy - r * 0.6 + i * r * 0.4
        w = math.sqrt(max(0, r * r - (y - cy) ** 2)) * 0.9
        off = 20 * math.sin(t * 1.5 + i)
        d.rounded_rectangle([s(cx - w + off), s(y - 12), s(cx + w * 0.7 + off), s(y + 12)], radius=s(12), fill=hexc('#f5d58a'))

def blanket(d, cx, cy, r, col, k=1.0):
    for i in range(3):
        rr = r + 40 + i * 30
        d.arc([s(cx - rr), s(cy - rr), s(cx + rr), s(cy + rr)], 200, 340, fill=hexc(mix(col, '#000000', k * (1 - i * 0.25))), width=s(14))

def sun(d, cx, cy, r, t, col='#ffb703'):
    for i in range(12):
        a = i * math.pi / 6 + t * 0.5
        line(d, [(cx + math.cos(a) * r * 1.2, cy + math.sin(a) * r * 1.2), (cx + math.cos(a) * r * 1.5, cy + math.sin(a) * r * 1.5)], '#ffd166', 8)
    circle(d, cx, cy, r, fill=hexc(col))

def steam(d, cx, cy, t, n=7, col='#ffffff', spread=260):
    for i in range(n):
        x = cx - spread / 2 + i * spread / (n - 1)
        ph = (t * 0.8 + i * 0.37) % 1.0
        y = cy - ph * 150
        pts = [(x + 14 * math.sin(j * 0.9 + t * 4 + i), y - j * 12) for j in range(8)]
        line(d, pts, col, 8)

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#1a0a05'); header(d, hexc('#ffb38a'))
    k = ease(t / 2.8)
    earth(d, 540, 640, 230, heat=k)
    text_block(img, ["Et si la Terre devenait un four… pour toujours ?"], t, 1090, '#ffffff', size=80)

def sc_venus(img, d, t, D):
    bg(d, '#2b1a3a'); stars(d, t); header(d, hexc('#f5d58a'))
    venus(d, 400, 620, 190, t)
    k = ease((t - 0.6) / 0.5)
    d.text((s(800), s(620)), "465 °C", font=font(FBK, 100), fill=hexc('#ff9f43', int(255 * k)), anchor='mm')
    text_block(img, ["Vénus est presque la jumelle de la Terre. À sa surface : 465 °C. De quoi faire fondre du plomb."], t, 1060, '#ffffff', size=64)

def sc_blanket(img, d, t, D):
    bg(d, '#0d2a3a'); stars(d, t); header(d, hexc('#9fe0ff'))
    k = ease((t - 0.4) / 1.0)
    earth(d, 540, 680, 170, heat=0.0)
    blanket(d, 540, 680, 170, '#9fe0ff', k)
    text_block(img, ["L'effet de serre, c'est une couverture : des gaz retiennent la chaleur. Sans elle, on gèlerait."], t, 1060, '#ffffff', size=64)

def sc_loop(img, d, t, D):
    bg(d, '#123a2a'); header(d, hexc('#a8f0c0'))
    cx, cy, R = 540, 630, 230
    d.arc([s(cx - R), s(cy - R), s(cx + R), s(cy + R)], 0, 360, fill=hexc('#a8f0c0'), width=s(10))
    for j in range(3):
        a = t * 1.6 + j * 2 * math.pi / 3
        x, y = cx + math.cos(a) * R, cy + math.sin(a) * R
        circle(d, x, y, 22, fill=hexc('#ffd166'))
    k1, k2 = ease((t - 0.3) / 0.4), ease((t - 1.0) / 0.4)
    ctext(d, "chaleur", cy - 60, 58, '#ff9f43', FB, k1)
    ctext(d, "vapeur d'eau", cy + 20, 58, '#9fe0ff', FB, k2)
    text_block(img, ["Le piège : plus il fait chaud, plus l'eau s'évapore. Et la vapeur d'eau réchauffe encore plus."], t, 1060, '#ffffff', size=64)

def sc_runaway(img, d, t, D):
    bg(d, '#3a2a0a'); header(d, hexc('#ffe08a'))
    k = ease(t / 3.5)
    earth(d, 540, 700, 180, heat=0.5 * k)
    steam(d, 540, 560, t, n=7 + int(6 * k), spread=260 + 200 * k)
    text_block(img, ["Si cette boucle s'emballe, les océans finissent par s'évaporer complètement."], t, 1080, '#ffffff', size=68)

random.seed(17)
CRACKS = [(random.uniform(0, 2 * math.pi), random.uniform(0.4, 1.0)) for _ in range(14)]
def sc_boom(img, d, t, D):
    bg(d, '#3a0b10'); header(d, hexc('#ffb3bd'))
    shake = 7 * math.sin(t * 45) * (1 if t < 1.0 else 0.15)
    k = ease((t - 0.2) / 1.5)
    earth(d, 540 + shake, 640, 220, heat=0.5 + 0.5 * k)
    if k > 0.3:
        for (a, l) in CRACKS:
            line(d, [(540 + shake + math.cos(a) * 50, 640 + math.sin(a) * 50), (540 + shake + math.cos(a) * 215 * l, 640 + math.sin(a) * 215 * l)], '#3a0b10', 6)
    text_block(img, ["Plus d'océans, plus de pluie. Une planète-four.", ("Fin de la partie.", 1.8)], t, 1060, '#ffffff', size=74)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    d.rounded_rectangle([s(220), s(420), s(860), s(860)], radius=s(40), outline=hexc('#8a5a3c'), width=s(14))
    for i in range(4):
        x = 270 + i * 150
        d.rounded_rectangle([s(x), s(470), s(x + 110), s(600)], radius=s(16), fill=hexc('#cfe9ec'))
    for i in range(9):
        x = 270 + i * 66 + 6 * math.sin(t * 3 + i)
        circle(d, x, 690, 26, fill=hexc('#8a5a3c'))
        d.rounded_rectangle([s(x - 26), s(718), s(x + 26), s(820)], radius=s(14), fill=hexc('#8a5a3c'))
    text_block(img, ["Un endroit étouffant d'où personne ne peut sortir…", ("…c'est le métro à 18 h en plein mois d'août.", 1.6)], t, 1010, '#2b1a10', size=66)

def sc_giec(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.35)
    sc = 1.5 - 0.5 * k
    if k > 0:
        d.text((s(540), s(600)), "≈ 0 %", font=font(FBK, int(190 * sc)), fill=hexc('#a8f0c0', int(255 * k)), anchor='mm')
    text_block(img, [("Bonne nouvelle : selon le GIEC, nos activités n'ont pratiquement aucune chance de déclencher cet emballement.", 0.6)], t, 1040, '#ffffff', size=60)

def sc_but(img, d, t, D):
    bg(d, '#0b2545'); header(d, hexc('#9fc2ff'))
    h = 260 + 40 * ease(t / 2.5)
    d.rounded_rectangle([s(500), s(820 - h - 120), s(580), s(820)], radius=s(40), outline=hexc('#ffffff'), width=s(10))
    d.rounded_rectangle([s(518), s(820 - h), s(562), s(810)], radius=s(22), fill=hexc('#ff6b6b'))
    circle(d, 540, 860, 70, fill=hexc('#ff6b6b'))
    text_block(img, ["Attention : le réchauffement actuel reste un vrai problème. Juste pas celui-là."], t, 1060, '#ffffff', size=66)

def sc_sun(img, d, t, D):
    bg(d, '#3a1a08'); header(d, hexc('#ffd166'))
    k = ease(t / 3.0)
    sun(d, 330, 620, 110 + 40 * k, t)
    earth(d, 820, 640, 70, heat=0.3 * k)
    text_block(img, ["Le vrai coupable, ce sera le Soleil : il brille un peu plus fort chaque milliard d'années."], t, 1060, '#ffffff', size=64)

def sc_billion(img, d, t, D):
    bg(d, '#24163d'); header(d, hexc('#d2b8ff'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "1 MILLIARD", 470, 150, '#d2b8ff', FBK, k)
    ctext(d, "d'années, environ", 690, 52, '#d2b8ff', FM, k)
    text_block(img, [("C'est le temps qu'il faudra avant qu'il fasse bouillir nos océans.", 0.8)], t, 1060, '#ffffff', size=70)

sc_title = scene_title(["SERRE", "EMBALLÉE"], "Scénario d'extinction n°17", color='#9a2a0e')
sc_end = scene_end("Bref : la Terre ne deviendra pas Vénus de sitôt. Votre déclaration d'impôts, elle, chauffe déjà.", color='#9a2a0e')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_venus, 4.2), (sc_blanket, 4.2), (sc_loop, 4.2),
    (sc_runaway, 4.0), (sc_boom, 3.8), (sc_joke, 4.6), (sc_giec, 4.6), (sc_but, 4.0),
    (sc_sun, 4.2), (sc_billion, 4.0), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Et si la Terre devenait un four… pour toujours ?",
    "Scénario d'extinction numéro dix-sept : l'effet de serre emballé.",
    "Vénus est presque la jumelle de la Terre. À sa surface : quatre cent soixante-cinq degrés. De quoi faire fondre du plomb.",
    "L'effet de serre, c'est une couverture : des gaz retiennent la chaleur. Sans elle, on gèlerait.",
    "Le piège : plus il fait chaud, plus l'eau s'évapore. Et la vapeur d'eau réchauffe encore plus.",
    "Si cette boucle s'emballe, les océans finissent par s'évaporer complètement.",
    "Plus d'océans, plus de pluie. Une planète-four. Fin de la partie.",
    "Un endroit étouffant d'où personne ne peut sortir… c'est le métro à dix-huit heures en plein mois d'août.",
    "Bonne nouvelle : selon le GIEC, nos activités n'ont pratiquement aucune chance de déclencher cet emballement.",
    "Attention : le réchauffement actuel reste un vrai problème. Juste pas celui-là.",
    "Le vrai coupable, ce sera le Soleil : il brille un peu plus fort chaque milliard d'années.",
    "Dans environ un milliard d'années, il fera bouillir nos océans.",
    "Bref : la Terre ne deviendra pas Vénus de sitôt. Votre déclaration d'impôts, elle, chauffe déjà. Abonnez-vous. Tant qu'il y a un demain.",
]
