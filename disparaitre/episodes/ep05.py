"""Épisode 5 — L'hiver nucléaire.
Sources : Xia, Robock et al., Nature Food (août 2022), via Rutgers / ScienceDaily 15/08/2022 ;
SIPRI Yearbook 2025 (communiqué du 16/06/2025 : 12 241 ogives, ~90 % à la Russie et aux États-Unis) ;
Robock & Toon (Scientific American / Physics Today) sur la fumée stratosphérique qui persiste des années ;
Reisner et al. (Los Alamos, JGR 2018) pour le débat sur la quantité de fumée.
"""
from engine import *

EPISODE = 5
BOOM_SCENE = 7
LEGENDE = """Épisode 5 : l'hiver nucléaire ❄️☢️

Le pire d'une grande guerre nucléaire ne serait peut-être pas les explosions, mais la fumée : elle cacherait le Soleil pendant des années. Une étude de 2022 (Nature Food) estime qu'une guerre totale entre les États-Unis et la Russie ferait chuter la production de nourriture d'environ 90 %. Bonne nouvelle : aucune bombe n'a été utilisée en guerre depuis 1945.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #hivernucleaire #climat #vulgarisation #scienceenfrançais #histoire"""

# ---------- petits dessins (fil rouge : la Terre, le Soleil et la couche de fumée) ----------
def earth(d, cx, cy, r, sea='#3b82c4', land='#4fae6a', ice=0.0):
    circle(d, cx, cy, r, fill=hexc(sea))
    for (dx, dy, rr) in ((-0.35, -0.2, 0.32), (0.3, 0.15, 0.36), (-0.1, 0.45, 0.22), (0.4, -0.45, 0.18)):
        circle(d, cx + dx * r, cy + dy * r, rr * r, fill=hexc(land))
    if ice > 0:
        h = r * 0.9 * ice
        d.chord([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], 270 - 90 * ice, 270 + 90 * ice, fill=hexc('#eaf4ff'))
        d.chord([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], 90 - 90 * ice, 90 + 90 * ice, fill=hexc('#eaf4ff'))

def sun(d, cx, cy, r, t, dim=0.0):
    a = int(255 * (1 - 0.75 * dim))
    for i in range(12):
        ang = i * math.pi / 6 + t * 0.4
        line(d, [(cx + (r + 18) * math.cos(ang), cy + (r + 18) * math.sin(ang)),
                 (cx + (r + 55) * math.cos(ang), cy + (r + 55) * math.sin(ang))], hexc('#ffd23f', a), 12)
    circle(d, cx, cy, r, fill=hexc('#ffd23f', a))

def smoke_band(d, cx, cy, r, k, t):
    """anneau de fumée autour de la Terre"""
    if k <= 0: return
    n = 26
    for i in range(int(n * k)):
        ang = i * 2 * math.pi / n + t * 0.3
        rr = r + 45 + 8 * math.sin(t * 3 + i)
        circle(d, cx + rr * math.cos(ang), cy + rr * math.sin(ang), 44, fill=hexc('#2b2b2b', 230))

def snowflake(d, cx, cy, r, col, rot=0):
    for i in range(6):
        a = rot + i * math.pi / 3
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        line(d, [(cx, cy), (x, y)], col, 12)
        for side in (-1, 1):
            bx, by = cx + 0.6 * r * math.cos(a), cy + 0.6 * r * math.sin(a)
            line(d, [(bx, by), (bx + 0.28 * r * math.cos(a + side * 0.8), by + 0.28 * r * math.sin(a + side * 0.8))], col, 10)

def city(d, base, col, t, fire=0.0):
    xs = [(130, 120, 260), (270, 110, 380), (400, 140, 300), (560, 120, 430), (700, 130, 330), (850, 110, 260)]
    for (x, w, h) in xs:
        d.rounded_rectangle([s(x), s(base - h), s(x + w), s(base)], radius=s(10), fill=hexc(col))
        for wy in range(int(base - h + 30), int(base - 30), 60):
            for wx in (x + 25, x + w - 45):
                d.rectangle([s(wx), s(wy), s(wx + 20), s(wy + 26)], fill=hexc('#ffe9a8', 180))
        if fire > 0:
            for j in range(3):
                fx = x + w * (0.25 + 0.25 * j)
                fh = (60 + 30 * math.sin(t * 9 + j + x)) * fire
                fy = base - h
                d.polygon([(s(fx - 22), s(fy)), (s(fx), s(fy - fh)), (s(fx + 22), s(fy))], fill=hexc('#ff7a1a'))
                d.polygon([(s(fx - 11), s(fy)), (s(fx), s(fy - fh * 0.55)), (s(fx + 11), s(fy))], fill=hexc('#ffd23f'))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b1a2e'); header(d, hexc('#a9d4ff'))
    earth(d, 540, 640, 230, ice=ease((t - 0.8) / 1.4) * 0.45)
    snowflake(d, 790, 420, 70, '#ffffff', rot=t * 0.8)
    text_block(img, ["Et si la fin du monde ne venait pas d'un grand boum… mais d'un grand froid ?"], t, 1080, '#ffffff', size=76)

def sc_stock(img, d, t, D):
    bg(d, '#2d1b0e'); header(d, hexc('#ffcf99'))
    k = ease((t - 0.2) / 0.4)
    n = int(12241 * ease(t / 1.4))
    ctext(d, f"{n:,}".replace(',', ' '), 470, 190, '#ffcf99', FBK, k)
    ctext(d, "bombes nucléaires dans le monde (2025)", 720, 42, '#ffcf99', FM, k)
    text_block(img, [("Environ 9 sur 10 appartiennent à deux pays : les États-Unis et la Russie.", 0.9)], t, 1060, '#ffffff', size=70)

def sc_fire(img, d, t, D):
    bg(d, '#3a0f12'); header(d, hexc('#ffb3a8'))
    city(d, 900, '#1a0608', t, fire=ease((t - 0.5) / 0.8))
    text_block(img, ["Dans une grande guerre, des villes entières prendraient feu."], t, 1080, '#ffffff', size=76)

def sc_rise(img, d, t, D):
    bg(d, '#4b5563'); header(d, hexc('#e5e7eb'))
    random.seed(5)
    for i in range(16):
        x0 = 150 + (i % 8) * 110
        ph = random.random()
        prog = ((t * 0.35 + ph) % 1.0)
        y = 930 - prog * 560
        circle(d, x0 + 20 * math.sin(t * 2 + i), y, 35 + 25 * prog, fill=hexc('#111111', 220))
    for (cx, cy) in ((230, 640), (560, 610), (880, 650)):
        for (dx, dy, r) in ((-60, 10, 50), (0, -15, 65), (60, 10, 50)):
            circle(d, cx + dx + 10 * math.sin(t), cy + dy, r, fill=hexc('#ffffff', 235))
    text_block(img, ["Leur fumée noire monterait plus haut que les nuages (la stratosphère)."], t, 1080, '#ffffff', size=72)

def sc_blanket(img, d, t, D):
    bg(d, '#14213d'); header(d, hexc('#a9c4ff'))
    sun(d, 180, 380, 70, t)
    earth(d, 600, 680, 200)
    smoke_band(d, 600, 680, 200, ease(t / 2.2), t)
    text_block(img, ["Là-haut, pas de pluie pour la laver. Elle ferait le tour de la Terre et resterait des années."], t, 1060, '#ffffff', size=66)

def sc_cold(img, d, t, D):
    bg(d, '#1e3a5f'); header(d, hexc('#bfe3ff'))
    sun(d, 230, 400, 70, t, dim=ease((t - 0.3) / 1.0))
    # thermomètre
    d.rounded_rectangle([s(690), s(340), s(770), s(820)], radius=s(40), outline=hexc('#ffffff'), width=s(10))
    circle(d, 730, 860, 70, fill=hexc('#ff4d5a'))
    lvl = 420 + 330 * ease((t - 0.5) / 1.8)
    d.rounded_rectangle([s(712), s(lvl), s(748), s(830)], radius=s(18), fill=hexc('#ff4d5a'))
    snowflake(d, 330, 760, 60, '#ffffff', rot=t)
    text_block(img, ["Moins de soleil, donc beaucoup plus froid. Même en plein été."], t, 1080, '#ffffff', size=74)

def sc_crops(img, d, t, D):
    bg(d, '#5a3d1a'); header(d, hexc('#ffe1a8'))
    k = ease((t - 0.4) / 1.2)
    for i in range(7):
        x = 170 + i * 125
        bend = 0.55 * k * (1 if i % 2 else 0.8)
        top = (x + 170 * math.sin(bend), 900 - 420 * math.cos(bend))
        line(d, [(x, 920), top], '#c9a227' if k < 0.5 else '#7a5c22', 12)
        circle(d, top[0], top[1], 30, fill=hexc('#e8c547' if k < 0.5 else '#8a6a2a'))
    line(d, [(80, 920), (1000, 920)], '#2e1f0c', 14)
    text_block(img, ["Les récoltes s'effondreraient. Environ 90 % de nourriture en moins dans le monde."], t, 1060, '#ffffff', size=68)

def sc_famine(img, d, t, D):
    bg(d, '#000000'); stars(d, t)
    header(d, hexc('#9a9aa8'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "5 MILLIARDS", 480, 140, '#ff6b6b', FBK, k)
    ctext(d, "de personnes menacées par la faim", 680, 42, '#9a9aa8', FM, k)
    text_block(img, [("C'est l'estimation d'une étude de 2022 (revue Nature Food) pour une guerre totale États-Unis – Russie.", 0.9)], t, 1020, '#ffffff', size=62)

def sc_joke(img, d, t, D):
    bg(d, '#e6f0f7'); header(d, hexc('#3b6e91'))
    # climatiseur au mur
    d.rounded_rectangle([s(260), s(380), s(820), s(560)], radius=s(30), fill=hexc('#ffffff'), outline=hexc('#3b6e91'), width=s(8))
    for j in range(4):
        line(d, [(320, 510 + j * 0), (760, 510)], '#3b6e91', 6)
    ctext(d, "16 °C", 410, 70, '#3b6e91', FBK)
    for j in range(5):
        x = 320 + j * 110; y = 600 + ((t * 120 + j * 50) % 320)
        snowflake(d, x, y, 30, '#7fb3d5', rot=t + j)
    text_block(img, ["Le seul hiver nucléaire que vous ayez connu…", ("…c'est la clim du bureau réglée sur 16 °C.", 1.6)], t, 1040, '#13293d', size=70)

def sc_debate(img, d, t, D):
    bg(d, '#2e1a47'); header(d, hexc('#d6c2ff'))
    k1 = ease((t - 0.3) / 0.8); k2 = ease((t - 0.9) / 0.8)
    base = 900
    d.rounded_rectangle([s(260), s(base - 480 * k1), s(460), s(base)], radius=s(20), fill=hexc('#ff6fb5'))
    d.rounded_rectangle([s(620), s(base - 140 * k2), s(820), s(base)], radius=s(20), fill=hexc('#7ff0e0'))
    ctext(d, "fumée selon les études", 330, 40, '#d6c2ff', FM, k1)
    line(d, [(200, base), (880, base)], '#ffffff', 6)
    text_block(img, ["Le vrai chiffre fait débat : certaines études trouvent beaucoup moins de fumée, donc moins de froid.",
                     ("Mais toutes disent : ce serait très grave.", 2.4)], t, 1000, '#ffffff', size=60)

def sc_good(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "1945", 480, 200, '#a8f0c0', FBK, k)
    ctext(d, "dernière bombe utilisée en guerre", 720, 42, '#a8f0c0', FM, k)
    text_block(img, [("Bonne nouvelle : l'hiver nucléaire n'arrive que si quelqu'un appuie sur le bouton.", 0.8)], t, 1060, '#ffffff', size=68)

sc_title = scene_title(["HIVER", "NUCLÉAIRE"], "Scénario d'extinction n°5")
sc_end = scene_end("Bref : l'hiver nucléaire n'est pas une fatalité. Les impôts, si.")

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_stock, 4.2), (sc_fire, 3.8), (sc_rise, 4.2),
    (sc_blanket, 4.6), (sc_cold, 4.0), (sc_crops, 4.4), (sc_famine, 4.8),
    (sc_joke, 4.6), (sc_debate, 5.4), (sc_good, 4.2), (sc_end, 4.8),
]
