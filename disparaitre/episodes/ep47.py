"""Épisode 47 — L'année sans été (Tambora, 1816) : quand un volcan éteint l'été.
Sources :
- Encyclopædia Britannica, « Mount Tambora » : éruption d'avril 1815 (nord de l'île de Sumbawa, Indonésie), la plus
  grande de l'histoire écrite ; volcan d'environ 4 300 m avant, 2 851 m aujourd'hui ; jusqu'à 150 km³ de matériaux
  dont ~60 mégatonnes de soufre ; au moins 10 000 morts immédiats, environ 80 000 morts de faim et de maladies ;
  1816 : neige et gel en juin, juillet, août en Europe de l'Ouest et dans l'est de l'Amérique du Nord, récoltes
  perdues, « année sans été ».
- AAAS (Science), « Year without summer » : indice d'explosivité 7 ; neige le 6 juin 1816 à New York (État) et dans
  le Maine, près de 30 cm à Québec ; pire famine du siècle en Irlande et Grande-Bretagne, famine en Chine ;
  baisse de la température mondiale de 0,4 à 0,7 °C ; Mary Shelley commence Frankenstein pendant cet été froid et
  pluvieux à Genève.
- Université de Cambridge (17 août 2022, Mani & Cassidy, commentaire dans Nature) : environ 1 chance sur 6 d'une
  éruption de magnitude 7 dans les 100 prochaines années ; le monde est « très mal préparé » ; refroidissement
  d'environ 1 °C en moyenne en 1816.
- NPR (13 août 2007) et National Geographic (2017) : lien entre l'été froid de 1816 et la naissance de Frankenstein.
Choix prudents : « moins d'un degré » (les sources donnent 0,4 à 1 °C en moyenne mondiale) ; « des dizaines de
milliers de morts » au total.
"""
from engine import *

EPISODE = 47
BOOM_SCENE = 7
LEGENDE = """Épisode 47 : le volcan qui a annulé l'été 🌋❄️

En avril 1815, le volcan Tambora, en Indonésie, explose : la plus grosse éruption de l'histoire écrite. Son soufre voile le Soleil, et 1816 devient « l'année sans été » : neige en juin en Amérique du Nord, récoltes perdues, famines en Europe et en Chine. Selon des chercheurs de Cambridge (2022), il y a environ 1 chance sur 6 qu'une éruption de cette taille se produise dans les 100 prochaines années. Grave pour les récoltes, mais pas la fin de l'humanité.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #volcan #tambora #climat #histoire #science #vulgarisation #apocalypse"""

def xtext(d, txt, x, y, size, color, fpath=FB, alpha=1.0):
    f = font(fpath, size)
    d.text((s(x) - f.getlength(txt) / 2, s(y)), txt, font=f, fill=hexc(color)[:3] + (int(255 * alpha),))

# ---------- fil rouge : le volcan ----------
def volcano(d, cx, base, t, w=320, h=330, col='#5a3d2b', cut=0.0, erupt=0.0, smoke=True):
    top = base - h * (1 - cut)
    half = w * (0.18 + 0.4 * cut)
    d.polygon([(s(cx - w), s(base)), (s(cx - half), s(top)), (s(cx + half), s(top)), (s(cx + w), s(base))], fill=hexc(col))
    d.polygon([(s(cx - half), s(top)), (s(cx + half), s(top)), (s(cx + half * 0.6), s(top + 26)), (s(cx - half * 0.6), s(top + 26))], fill=hexc('#c0392b'))
    if smoke and erupt <= 0:
        for i in range(3):
            k = (t * 0.5 + i / 3) % 1
            circle(d, cx + 20 * math.sin(k * 6), top - 30 - k * 140, 16 + 24 * k, fill=hexc('#d9d9d9', int(200 * (1 - k))))
    if erupt > 0:
        for i in range(14):
            k = ((t * 0.9 + i / 14) % 1)
            r = 28 + 55 * k * erupt
            y = top - 40 - k * 230 * erupt
            x = cx + (i % 5 - 2) * 30 * k + 25 * math.sin(i + t * 2)
            circle(d, x, y, r, fill=hexc('#8a8a8a', int(230 * (1 - k * 0.6))))
        for i in range(10):
            a = -math.pi / 2 + (i - 4.5) * 0.22
            k = ((t * 1.6 + i / 10) % 1) * erupt
            circle(d, cx + math.cos(a) * 260 * k, top + math.sin(a) * 300 * k + 260 * k * k, 10, fill=hexc('#ff7a2a'))

def ground(d, y, col):
    d.rectangle([0, s(y), s(1080), s(960)], fill=hexc(col))

def sun(d, cx, cy, r, t, col='#ffd23f', a=255):
    for i in range(12):
        ang = i * math.pi / 6 + t * 0.4
        line(d, [(cx + math.cos(ang) * (r + 18), cy + math.sin(ang) * (r + 18)),
                 (cx + math.cos(ang) * (r + 55), cy + math.sin(ang) * (r + 55))], hexc(col, a), 10)
    circle(d, cx, cy, r, fill=hexc(col, a))

def earth(d, cx, cy, r):
    circle(d, cx, cy, r, fill=hexc('#2f7fd1'))
    d.ellipse([s(cx - r * 0.55), s(cy - r * 0.5), s(cx + r * 0.05), s(cy + r * 0.1)], fill=hexc('#4caf50'))
    d.ellipse([s(cx + r * 0.1), s(cy + r * 0.05), s(cx + r * 0.6), s(cy + r * 0.6)], fill=hexc('#4caf50'))

def snowflakes(d, t, n=50, seed=3, y0=300, y1=950, col='#ffffff'):
    rnd = random.Random(seed)
    for i in range(n):
        x = rnd.uniform(60, 1020); sp = rnd.uniform(60, 140); ph = rnd.uniform(0, 1)
        y = y0 + ((ph * (y1 - y0) + t * sp) % (y1 - y0))
        circle(d, x + 12 * math.sin(t * 2 + i), y, rnd.uniform(5, 11), fill=hexc(col, 230))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#1d3557'); header(d, hexc('#a8d8ff'))
    k = ease((t - 0.6) / 1.2)
    sun(d, 540, 620, 130, t)
    for i in range(5):
        x = 140 + 1000 * (1 - k) + i * 170 - 300 * k
        circle(d, x, 560 + (i % 2) * 90, 120, fill=hexc('#6c7a89', int(235 * min(1, k * 1.5))))
    text_block(img, ["Et si un seul volcan pouvait annuler l'été… pour toute la planète ?"], t, 1080, '#ffffff', size=74)

def sc_calm(img, d, t, D):
    bg(d, '#1f6f6a'); header(d, hexc('#b8f0e0'))
    ground(d, 860, '#2a8fa8')
    k = ease((t - 0.1) / 0.8)
    volcano(d, 540, 860, t, w=260 + 80 * k, h=260 + 120 * k)
    xtext(d, "4 300 m", 820, 470, 54, '#ffffff', FB, ease((t - 0.9) / 0.4))
    text_block(img, ["Avril 1815, Indonésie. Sur l'île de Sumbawa, le volcan Tambora se réveille."], t, 1060, '#ffffff', size=68)

def sc_erupt(img, d, t, D):
    bg(d, '#4a1f1a'); header(d, hexc('#ffc2a8'))
    ground(d, 860, '#2a2a2a')
    cut = 0.33 * ease((t - 1.4) / 1.0)
    volcano(d, 540, 860, t, w=340, h=380, cut=cut, erupt=ease(t / 0.5))
    xtext(d, "– 1 400 m", 860, 760, 52, '#ffd166', FBK, ease((t - 1.8) / 0.4))
    text_block(img, ["Il crache jusqu'à 150 km³ de roches et de cendres.", ("Et perd environ 1 400 m de hauteur.", 1.5)], t, 1060, '#ffffff', size=66)

def sc_sulfur(img, d, t, D):
    bg(d, '#2b2a5a'); header(d, hexc('#d0c8ff'))
    ground(d, 900, '#3b3b6b')
    volcano(d, 540, 900, t, w=280, h=200, cut=0.33, smoke=False)
    y_lim = 380
    line(d, [(60, y_lim), (1020, y_lim)], hexc('#d0c8ff', 120), 4)
    xtext(d, "stratosphère", 880, 320, 40, '#d0c8ff', FM)
    for i in range(18):
        k = ((t * 0.5 + i / 18) % 1)
        y = 760 - k * 380
        circle(d, 540 + (i % 6 - 2.5) * 30 * (1 + k * 4), y, 14, fill=hexc('#ffe14d', int(240 * (1 - k * 0.3))))
    text_block(img, ["Surtout, il projette du soufre très haut, au-dessus des nuages (la stratosphère)."], t, 1060, '#ffffff', size=66)

def sc_veil(img, d, t, D):
    bg(d, '#0b1026'); stars(d, t); header(d, hexc('#ffe9a8'))
    sun(d, 150, 620, 70, t)
    earth(d, 700, 620, 170)
    k = ease((t - 0.3) / 1.4)
    d.arc([s(700 - 215), s(620 - 215), s(700 + 215), s(620 + 215)], -90, -90 + 360 * k, fill=hexc('#ffe14d', 170), width=s(22))
    for i in range(3):
        y = 560 + i * 60
        kk = ((t * 0.8 + i / 3) % 1)
        x = 240 + kk * 240
        line(d, [(x, y), (x + 50, y)], '#ffd23f', 8)
        if kk > 0.75 and k > 0.6:
            line(d, [(470, y), (470 - (kk - 0.75) * 400, y - 40)], hexc('#ffd23f', 150), 6)
    text_block(img, ["Le soufre forme un voile autour de la Terre.", ("Il renvoie une partie de la lumière du Soleil.", 1.4)], t, 1060, '#ffffff', size=68)

def sc_thermo(img, d, t, D):
    bg(d, '#14506b'); header(d, hexc('#bfe8ff'))
    d.rounded_rectangle([s(500), s(330), s(580), s(820)], radius=s(40), outline=hexc('#ffffff'), width=s(10))
    circle(d, 540, 860, 80, fill=hexc('#ff4d5a'))
    lvl = 470 + 90 * ease((t - 0.5) / 1.5)
    d.rounded_rectangle([s(518), s(lvl), s(562), s(850)], radius=s(22), fill=hexc('#ff4d5a'))
    xtext(d, "< 1 °C", 790, 560, 70, '#bfe8ff', FBK, ease((t - 1.3) / 0.4))
    text_block(img, ["La planète perd en moyenne moins d'un degré.", ("Ça paraît peu… c'est énorme pour les récoltes.", 1.5)], t, 1060, '#ffffff', size=66)

def sc_boom(img, d, t, D):
    bg(d, '#8fa3b8'); header(d, hexc('#1d2b3a'))
    ground(d, 820, '#eef4fa')
    for i in range(7):
        x = 140 + i * 135; bend = ease(t / 0.8)
        line(d, [(x, 820), (x + 10 * bend, 700 + 40 * bend), (x + 40 * bend, 690 + 70 * bend)], '#7a8a5a', 9)
    snowflakes(d, t, n=60, y0=300, y1=820)
    d.rounded_rectangle([s(290), s(340), s(790), s(470)], radius=s(30), fill=hexc('#eef4fa'))
    xtext(d, "JUIN 1816", 540, 355, 88, '#1d2b3a', FBK, ease(t / 0.3))
    text_block(img, ["1816 : neige en juin en Amérique du Nord. Gel en plein été. Récoltes perdues."], t, 1060, '#1d2b3a', size=68)

def sc_famine(img, d, t, D):
    bg(d, '#3a2a14'); header(d, hexc('#f0d8a8'))
    for i in range(3):
        x = 300 + i * 240; k = ease((t - 0.3 - i * 0.4) / 0.4)
        d.rounded_rectangle([s(x - 80), s(520), s(x + 80), s(800)], radius=s(30), outline=hexc('#f0d8a8'), width=s(10))
        d.rectangle([s(x - 60), s(min(770, 545 + 225 * k)), s(x + 60), s(785)], fill=hexc('#d9a441'))
    xtext(d, "Europe   ·   Chine", 540, 400, 52, '#f0d8a8', FB, ease((t - 0.2) / 0.4))
    text_block(img, ["Les greniers se vident. Famines en Europe et en Chine.", ("Au total : des dizaines de milliers de morts.", 1.5)], t, 1060, '#ffffff', size=66)

def sc_book(img, d, t, D):
    bg(d, '#2a1f3d'); header(d, hexc('#e0c8ff'))
    for i in range(30):
        x = (i * 73) % 1000 + 40; y = 330 + ((i * 131 + t * 500) % 600)
        line(d, [(x, y), (x - 8, y + 30)], hexc('#9fb8ff', 160), 4)
    k = ease((t - 0.2) / 0.6)
    d.rounded_rectangle([s(380), s(450), s(700), s(880)], radius=s(18), fill=hexc('#3d6b4a', int(255 * k)))
    d.rectangle([s(380), s(450), s(410), s(880)], fill=hexc('#2a4a33', int(255 * k)))
    if int(t * 3) % 4 == 0 and t > 1.0:
        line(d, [(560, 520), (510, 640), (580, 640), (530, 780)], '#ffe14d', 14)
    text_block(img, ["Bloquée par la pluie en Suisse, une jeune autrice commence un roman : Frankenstein."], t, 1060, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#cfe8d8'); header(d, hexc('#2d5a3d'))
    ground(d, 860, '#7fbf8f')
    d.polygon([(s(330), s(860)), (s(540), s(560)), (s(750), s(860))], fill=hexc('#e76f51'))
    d.polygon([(s(500), s(860)), (s(540), s(700)), (s(580), s(860))], fill=hexc('#7a2e1f'))
    circle(d, 760, 400, 90, fill=hexc('#7d8a96'))
    circle(d, 650, 420, 70, fill=hexc('#7d8a96'))
    for i in range(10):
        x = 600 + (i * 37) % 220; y = 480 + ((i * 59 + t * 400) % 260)
        line(d, [(x, y), (x - 6, y + 26)], '#4a7ab0', 5)
    text_block(img, ["La prochaine fois qu'il pleut au camping…", ("…dites-vous qu'en 1816, il neigeait en juin.", 1.4)], t, 1060, '#1d3a28', size=68)

def sc_odds(img, d, t, D):
    bg(d, '#000000'); stars(d, t); header(d, hexc('#9a9aa8'))
    k = ease((t - 0.2) / 0.4)
    for i in range(6):
        x = 190 + i * 140
        hit = i == 2 and t > 1.2
        d.rounded_rectangle([s(x - 55), s(420), s(x + 55), s(530)], radius=s(18), fill=hexc('#ff4d5a' if hit else '#2c2c3a', int(255 * k)))
    ctext(d, "1 sur 6", 600, 120, '#ffd166', FBK, k)
    text_block(img, [("Selon des chercheurs de Cambridge (2022) : environ 1 chance sur 6 d'une éruption de cette taille d'ici 100 ans.", 0.6)], t, 1010, '#ffffff', size=62)

def sc_verdict(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    ground(d, 860, '#1e4a30')
    volcano(d, 540, 860, t, w=260, h=260, col='#3d5a45')
    k = ease((t - 0.8) / 0.4)
    d.rounded_rectangle([s(690), s(440), s(990), s(620)], radius=s(20), fill=hexc('#a8f0c0', int(255 * k)))
    if k > 0:
        pts = [(710 + i * 7, 530 + (38 * math.sin(i * 1.3 + t * 8) * math.exp(-((i - 20) / 8) ** 2) + 4 * math.sin(i)) ) for i in range(40)]
        line(d, pts, '#12301f', 6)
    xtext(d, "surveillance", 840, 640, 40, '#a8f0c0', FM, k)
    text_block(img, ["Des récoltes ratées, oui. La fin de l'humanité, non.", ("Mais les experts demandent de mieux surveiller les volcans.", 1.5)], t, 1060, '#ffffff', size=64)

sc_title = scene_title(["L'ANNÉE", "SANS ÉTÉ"], "Scénario d'extinction n°47", color='#5a2a1a')
sc_end = scene_end("Bref : un volcan peut annuler l'été. Pas votre déclaration d'impôts.", color='#5a2a1a')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_calm, 3.8), (sc_erupt, 4.2), (sc_sulfur, 3.8),
    (sc_veil, 4.0), (sc_thermo, 4.0), (sc_boom, 4.0), (sc_famine, 4.0), (sc_book, 3.8),
    (sc_joke, 3.8), (sc_odds, 4.4), (sc_verdict, 4.2), (sc_end, 4.6),
]
