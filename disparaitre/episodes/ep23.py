"""Épisode 23 — L'effondrement de la circulation océanique (AMOC).
Sources :
- GIEC AR6 (WG1, 2021) : l'AMOC va très probablement s'affaiblir au XXIe siècle ; confiance moyenne qu'il n'y aura
  pas d'effondrement brutal avant 2100.
- Caesar et al. / Thornalley et al., Nature (2018) ; CBS News, phys.org (2021) : circulation au plus faible depuis
  plus de mille ans (environ 1 600 ans selon Thornalley).
- Drijfhout et al., Environmental Research Letters (2025) ; ScienceDaily 30/08/2025 : dans les modèles prolongés
  après 2100, l'arrêt se déclenche ce siècle dans ~25 % (faibles émissions) à ~70 % (fortes émissions) des cas
  — probabilités de modèles, pas du monde réel (climatetippingpoints.info, mai 2026).
- Met Office / Baker et al., Nature (fév. 2025) : l'AMOC devrait résister (affaiblie) au réchauffement de ce siècle.
- Conséquences discutées : hivers bien plus rigoureux en Europe du Nord-Ouest, hausse du niveau de la mer sur la
  côte est américaine, déplacement des ceintures de pluie tropicales. Arrêts passés pendant les périodes glaciaires.
- Consensus : catastrophe climatique régionale majeure possible, mais pas une extinction de l'humanité.
"""
from engine import *

EPISODE = 23
BOOM_SCENE = 8
LEGENDE = """Épisode 23 : et si l'océan tombait en panne ? 🌊🥶

Dans l'Atlantique, un immense « tapis roulant » d'eau (l'AMOC) apporte la chaleur des tropiques jusqu'à l'Europe. Il est au plus faible depuis plus de mille ans (Nature, 2018). Le GIEC prévoit qu'il ralentisse très probablement ce siècle ; un arrêt complet reste incertain, mais des études récentes jugent le risque sérieux. Catastrophe climatique : oui. Fin de l'humanité : non.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #climat #ocean #AMOC #gulfstream #science #vulgarisation"""

# ---------- fil rouge : le tapis roulant océanique (boucle d'eau) ----------
CX, CY, RX, RY = 540, 620, 330, 200

def loop_pt(a):
    return CX + RX * math.cos(a), CY + RY * math.sin(a)

def conveyor(d, t, speed=1.0, alpha=255, warm='#ff7b54', cold='#4cc9f0', n=18, dsz=16):
    """Boucle : en haut l'eau chaude va vers la droite (le nord), en bas l'eau froide revient."""
    pts = [loop_pt(i * 2 * math.pi / 120) for i in range(121)]
    line(d, pts, hexc('#ffffff', int(alpha * 0.25)), 40)
    for i in range(n):
        a = (i / n) * 2 * math.pi + t * 0.9 * speed
        x, y = loop_pt(-a)  # sens : haut vers la droite
        col = warm if y < CY else cold
        circle(d, x, y, dsz, fill=hexc(col, alpha))

def europe(d, x, y, sc=1.0, col='#80ed99'):
    d.rounded_rectangle([s(x - 70 * sc), s(y - 90 * sc), s(x + 70 * sc), s(y + 90 * sc)], radius=s(50 * sc), fill=hexc(col))
    circle(d, x - 60 * sc, y - 70 * sc, 40 * sc, fill=hexc(col))

def greenland(d, x, y, sc=1.0, col='#f8f9fa'):
    d.rounded_rectangle([s(x - 80 * sc), s(y - 60 * sc), s(x + 80 * sc), s(y + 70 * sc)], radius=s(55 * sc), fill=hexc(col))

def snowflake(d, x, y, r, col='#ffffff', a=255):
    for k in range(3):
        ang = k * math.pi / 3
        line(d, [(x - r * math.cos(ang), y - r * math.sin(ang)), (x + r * math.cos(ang), y + r * math.sin(ang))], hexc(col, a), 6)

def label(d, txt, x, y, col, size=40):
    d.text((s(x), s(y)), txt, font=font(FB, size), fill=hexc(col), anchor='mm')

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#03045e'); header(d, hexc('#90e0ef'))
    for i in range(5):
        y = 450 + i * 90
        pts = [(x, y + 20 * math.sin(x / 60 + t * 3 + i)) for x in range(80, 1001, 20)]
        line(d, pts, hexc('#48cae4', 200 - i * 30), 12)
    k = ease((t - 1.0) / 0.6)
    if k > 0:
        d.rounded_rectangle([s(420), s(560), s(660), s(680)], radius=s(20), fill=hexc('#ffffff', int(230 * k)))
        label(d, "EN PANNE", 540, 620, '#d00000', 46)
    text_block(img, ["Et si l'océan tombait… en panne ?"], t, 1090, '#ffffff', size=84)

def sc_loop(img, d, t, D):
    bg(d, '#023e8a'); header(d, hexc('#ade8f4'))
    conveyor(d, t)
    text_block(img, ["Dans l'Atlantique, un immense tapis roulant d'eau tourne en boucle (l'AMOC)."], t, 1060, '#ffffff', size=66)

def sc_heat(img, d, t, D):
    bg(d, '#9d0208'); header(d, hexc('#ffccd5'))
    conveyor(d, t)
    europe(d, 930, 420, 0.8)
    circle(d, 150, 830, 60 + 6 * math.sin(t * 4), fill=hexc('#ffd166'))
    label(d, "TROPIQUES", 200, 930, '#ffd166', 38)
    label(d, "EUROPE", 780, 330, '#80ed99', 38)
    text_block(img, ["L'eau chaude des tropiques remonte vers le nord… et réchauffe l'Europe."], t, 1060, '#ffffff', size=68)

def sc_dive(img, d, t, D):
    bg(d, '#0b525b'); header(d, hexc('#99e2b4'))
    conveyor(d, t)
    k = (t * 0.6) % 1
    x = CX + RX - 10
    circle(d, x, CY - RY + 2 * RY * k, 30, fill=hexc('#4cc9f0'))
    line(d, [(x + 60, CY - 80), (x + 60, CY + 80)], '#ffffff', 8)
    line(d, [(x + 40, CY + 55), (x + 60, CY + 80), (x + 80, CY + 55)], '#ffffff', 8)
    text_block(img, ["Au nord, elle refroidit, devient plus lourde et plonge au fond.", ("Puis elle repart vers le sud.", 1.6)], t, 1060, '#ffffff', size=66)

def sc_melt(img, d, t, D):
    bg(d, '#5a189a'); header(d, hexc('#e0aaff'))
    conveyor(d, t, speed=0.6, n=14)
    greenland(d, 820, 360, 0.9)
    for i in range(5):
        ph = (t * 0.7 + i * 0.2) % 1
        circle(d, 760 + i * 30, 430 + 180 * ph, 12, fill=hexc('#caf0f8', int(255 * (1 - ph))))
    label(d, "GROENLAND", 820, 290, '#ffffff', 36)
    text_block(img, ["Mais le Groenland fond. Son eau douce est plus légère :", ("elle ne plonge plus.", 1.5)], t, 1060, '#ffffff', size=66)

def sc_slow(img, d, t, D):
    bg(d, '#3d405b'); header(d, hexc('#f2cc8f'))
    conveyor(d, t, speed=0.25)
    k = ease((t - 0.5) / 1.5)
    d.rounded_rectangle([s(290), s(870), s(790), s(920)], radius=s(25), outline=hexc('#ffffff'), width=s(4))
    d.rounded_rectangle([s(295), s(875), s(295 + 490 * (1 - 0.6 * k)), s(915)], radius=s(20), fill=hexc('#f2cc8f'))
    text_block(img, ["Résultat : le tapis ralentit.", ("Il serait déjà au plus faible depuis plus de mille ans.", 1.3)], t, 1060, '#ffffff', size=66)

def sc_past(img, d, t, D):
    bg(d, '#264653'); header(d, hexc('#a8dadc'))
    conveyor(d, 0, speed=0, alpha=150, warm='#a8dadc', cold='#a8dadc')
    for i in range(12):
        x = 120 + (i * 83) % 860; y = 330 + ((t * 80 + i * 57) % 600)
        snowflake(d, x, y, 18)
    label(d, "PÉRIODES GLACIAIRES", 540, 620, '#ffffff', 50)
    text_block(img, ["Pas de la science-fiction : il s'est déjà effondré pendant les périodes glaciaires."], t, 1060, '#ffffff', size=64)

def sc_boom(img, d, t, D):
    bg(d, '#000000'); header(d, hexc('#888888'))
    conveyor(d, 0, speed=0, alpha=110, warm='#555555', cold='#555555')
    k = ease(t / 1.5)
    europe(d, 540, 600, 1.4, col='#caf0f8')
    for i in range(9):
        snowflake(d, 380 + (i % 3) * 160, 460 + (i // 3) * 140, 26 * k, a=int(255 * k))
    text_block(img, ["S'il s'arrête : hivers glaciaux en Europe, mer qui monte en Amérique, pluies tropicales déréglées."], t, 1060, '#ffffff', size=62)

def sc_joke(img, d, t, D):
    bg(d, '#ffddd2'); header(d, hexc('#83c5be'))
    # plaid : grand rectangle à carreaux avec un mug
    x0, y0 = 260, 520
    for i in range(6):
        for j in range(4):
            c = '#e29578' if (i + j) % 2 == 0 else '#006d77'
            d.rectangle([s(x0 + i * 95), s(y0 + j * 95), s(x0 + i * 95 + 95), s(y0 + j * 95 + 95)], fill=hexc(c))
    d.rounded_rectangle([s(470), s(400), s(610), s(520)], radius=s(18), fill=hexc('#ffffff'))
    d.arc([s(590), s(420), s(660), s(500)], 270, 90, fill=hexc('#ffffff'), width=s(14))
    for i in range(3):
        y = 385 - 30 * ((t + i * 0.3) % 1)
        line(d, [(500 + i * 40, y), (510 + i * 40, y - 30)], hexc('#9a9a9a', 180), 6)
    text_block(img, ["Point positif : vous auriez enfin une excuse officielle pour ne plus quitter votre plaid."], t, 1060, '#2b2d42', size=64)

def sc_science(img, d, t, D):
    bg(d, '#2d6a4f'); header(d, hexc('#b7e4c7'))
    conveyor(d, t, speed=0.6)
    k = ease((t - 0.8) / 0.4)
    d.rounded_rectangle([s(300), s(890), s(780), s(970)], radius=s(24), fill=hexc('#40916c', int(255 * k)))
    if k > 0.5:
        label(d, "RALENTISSEMENT : TRÈS PROBABLE", 540, 930, '#ffffff', 30)
    text_block(img, ["Ce que disent les scientifiques : le tapis va très probablement ralentir ce siècle."], t, 1060, '#ffffff', size=64)

def sc_collapse(img, d, t, D):
    bg(d, '#6a4c93'); header(d, hexc('#e9d8fd'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "ARRÊT COMPLET ?", 430, 90, '#ffffff', FBK, k)
    ctext(d, "incertain… mais pris au sérieux", 570, 46, '#e9d8fd', FM, k)
    k2 = ease((t - 2.2) / 0.4)
    ctext(d, "Fin de l'humanité : non.", 760, 58, '#ffd166', FB, k2)
    text_block(img, ["Un arrêt complet ? Le GIEC ne l'attend pas avant 2100. Des études récentes jugent le risque bien réel."], t, 1060, '#ffffff', size=60)

sc_title = scene_title(["L'OCÉAN", "EN PANNE"], "Scénario d'extinction n°23", color='#0077b6')
sc_end = scene_end("Bref : l'océan peut geler, votre avis d'impôt arrivera quand même.", color='#0077b6')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_loop, 4.2), (sc_heat, 4.2), (sc_dive, 4.4),
    (sc_melt, 4.4), (sc_slow, 4.2), (sc_past, 4.2), (sc_boom, 4.4), (sc_joke, 4.2),
    (sc_science, 4.2), (sc_collapse, 4.8), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Et si l'océan tombait… en panne ?",
    "Scénario d'extinction numéro vingt-trois : l'océan en panne.",
    "Dans l'Atlantique, un immense tapis roulant d'eau tourne en boucle. On l'appelle l'AMOC.",
    "L'eau chaude des tropiques remonte vers le nord… et réchauffe l'Europe.",
    "Au nord, elle refroidit, devient plus lourde et plonge au fond. Puis elle repart vers le sud.",
    "Mais le Groenland fond. Son eau douce est plus légère : elle ne plonge plus.",
    "Résultat : le tapis ralentit. Il serait déjà au plus faible depuis plus de mille ans.",
    "Pas de la science-fiction : il s'est déjà effondré pendant les périodes glaciaires.",
    "S'il s'arrête : hivers glaciaux en Europe, mer qui monte en Amérique, pluies tropicales déréglées.",
    "Point positif : vous auriez enfin une excuse officielle pour ne plus quitter votre plaid.",
    "Ce que disent les scientifiques : le tapis va très probablement ralentir ce siècle.",
    "Un arrêt complet ? Le GIEC ne l'attend pas avant deux mille cent. Des études récentes jugent le risque bien réel. Mais la fin de l'humanité : non.",
    "Bref : l'océan peut geler, votre avis d'impôt arrivera quand même. Abonnez-vous. Tant qu'il y a un demain.",
]
