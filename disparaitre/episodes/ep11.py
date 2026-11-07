"""Épisode 11 — Le Soleil qui devient une géante rouge.
Sources : The Conversation / phys.org, « The Sun won't die for 5 billion years, so why do humans have
only 1 billion years left on Earth? » (fév. 2015) ; Futura-Sciences (X. Demeersman, « Quand aura lieu
la mort du Soleil ? ») ; Slate.fr, « On sait désormais quand et comment le Soleil va mourir » (2021) ;
Astronomy.com, « How life on Earth will end ».
- Soleil âgé d'environ 4,6 milliards d'années, à peu près à la moitié de sa vie « normale ».
- Il brille d'environ 10 % de plus par milliard d'années : Terre trop chaude pour les océans dans ~1 milliard d'années.
- Dans ~5 milliards d'années : géante rouge, des centaines de fois plus grande ; Mercure et Vénus avalées,
  le sort de la Terre reste débattu.
- Puis naine blanche, à peu près de la taille de la Terre.
- Homo sapiens : environ 300 000 ans.
"""
from engine import *

EPISODE = 11
BOOM_SCENE = 6
LEGENDE = """Épisode 11 : le Soleil qui devient une géante rouge ☀️🔴

Celui-là, il est (presque) certain : dans environ 5 milliards d'années, le Soleil va gonfler et avaler Mercure et Vénus. Mais bien avant, d'ici environ 1 milliard d'années, il brillera assez fort pour faire bouillir nos océans. Ça laisse un peu de marge.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #soleil #astronomie #espace #science #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def sun(d, cx, cy, r, t, col='#ffcc33', rays=True, a=255):
    """Le fil rouge : le Soleil, un disque qui respire, avec des rayons."""
    if rays:
        for i in range(12):
            ang = i * math.pi / 6 + t * 0.4
            r0, r1 = r * 1.15, r * (1.38 + 0.06 * math.sin(t * 5 + i))
            line(d, [(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))], hexc(col, a), max(4, r * 0.08))
    circle(d, cx, cy, r * 1.06, fill=hexc(col, int(a * 0.35)))
    circle(d, cx, cy, r, fill=hexc(col, a))

def earth(d, cx, cy, r, col='#3a8dff', land='#3fbf6a', a=255):
    circle(d, cx, cy, r, fill=hexc(col, a))
    circle(d, cx - r * 0.3, cy - r * 0.2, r * 0.35, fill=hexc(land, a))
    circle(d, cx + r * 0.35, cy + r * 0.3, r * 0.25, fill=hexc(land, a))

def gauge(d, cx, cy, level, col):
    d.rounded_rectangle([s(cx - 70), s(cy - 220), s(cx + 70), s(cy + 220)], radius=s(30), outline=hexc('#ffffff'), width=s(10))
    h = 420 * level
    d.rounded_rectangle([s(cx - 52), s(cy + 202 - h), s(cx + 52), s(cy + 202)], radius=s(18), fill=hexc(col))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b1230'); stars(d, t); header(d, hexc('#ffd37a'))
    sun(d, 400, 620, 150, t)
    earth(d, 760 + 20 * math.sin(t * 1.5), 620, 45)
    text_block(img, ["Et si la date de notre fin était déjà écrite… dans le ciel ?"], t, 1090, '#ffffff', size=78)

def sc_fuel(img, d, t, D):
    bg(d, '#3a2208'); header(d, hexc('#ffd37a'))
    sun(d, 390, 620, 190, t)
    lvl = 1.0 - 0.5 * ease((t - 0.3) / 1.6)
    gauge(d, 810, 620, lvl, '#ffcc33')
    ctext(d, "50 %", 880, 46, '#ffd37a', FB, ease((t - 1.6) / 0.4))
    text_block(img, ["Le Soleil brille en brûlant son carburant : de l'hydrogène.",
                     ("Il a 4,6 milliards d'années. Il a fait la moitié du chemin.", 1.5)], t, 1030, '#ffffff', size=64)

def sc_brighter(img, d, t, D):
    bg(d, '#4a1f3a'); header(d, hexc('#ffc0e0'))
    k = ease((t - 0.3) / 2.5)
    for i in range(3):
        circle(d, 540, 620, 180 + k * 60 + i * 40, fill=hexc('#ffe27a', int(40 * k)))
    sun(d, 540, 620, 180 + 30 * k, t, col='#ffe27a')
    ctext(d, "+10 %", 360, 70, '#ffffff', FBK, ease((t - 0.8) / 0.4))
    text_block(img, ["En vieillissant, il brille de plus en plus fort : environ 10 % de plus par milliard d'années."], t, 1060, '#ffffff', size=64)

def sc_oceans(img, d, t, D):
    bg(d, '#0e3b4a'); header(d, hexc('#9fe6ff'))
    dry = ease((t - 0.8) / 2.6)
    earth(d, 540, 680, 210, col='#3a8dff' if dry < 0.5 else '#9a7f55', land='#3fbf6a' if dry < 0.5 else '#c9a46a')
    for i in range(7):
        x = 380 + i * 54
        y = 450 - ((t * 120 + i * 40) % 160)
        if dry > 0.05:
            circle(d, x, y, 18, fill=hexc('#e6f7ff', int(200 * min(1, dry * 2))))
    text_block(img, ["Résultat : dans environ 1 milliard d'années, il fera trop chaud. Les océans vont s'évaporer."], t, 1060, '#ffffff', size=64)

def sc_empty(img, d, t, D):
    bg(d, '#2d2d2d'); header(d, hexc('#d0d0d0'))
    lvl = 0.5 * (1 - ease((t - 0.2) / 2.0))
    gauge(d, 540, 620, max(0.02, lvl), '#ff8a3a')
    ctext(d, "RÉSERVE", 880, 46, '#ff8a3a', FB, ease((t - 1.8) / 0.3) * (0.5 + 0.5 * math.sin(t * 10)))
    text_block(img, ["Puis, dans 5 milliards d'années, le carburant au centre s'épuise…"], t, 1080, '#ffffff', size=70)

def sc_boom(img, d, t, D):
    bg(d, '#14060a'); stars(d, t, col='#ffb0a0'); header(d, hexc('#ffb0a0'))
    k = ease((t - 0.2) / 2.2)
    r = 50 + 270 * k
    planets = [(110, 18, '#b0a090'), (190, 30, '#f0c070'), (300, 34, '#3a8dff')]
    for dx, pr, pc in planets:
        x = 540 + dx
        if x - 540 > r * 0.95:
            circle(d, x, 640, pr, fill=hexc(pc))
    col = '#ffcc33' if k < 0.3 else '#ff5a2a'
    circle(d, 540, 640, r * 1.12, fill=hexc(col, 70))
    circle(d, 540, 640, r, fill=hexc(col))
    text_block(img, ["…et il gonfle : il devient une géante rouge, des centaines de fois plus grande !"], t, 1090, '#ffffff', size=68)

def sc_earth(img, d, t, D):
    bg(d, '#5a1408'); header(d, hexc('#ffc2a8'))
    d.ellipse([s(-900), s(240), s(560), s(1040)], fill=hexc('#ff5a2a'))
    for i, (lbl, x) in enumerate([("Mercure", 300), ("Vénus", 470)]):
        k = ease((t - 0.4 - i * 0.6) / 0.3)
        ctext_x = x
        f = font(FB, 40)
        d.text((s(ctext_x) - f.getlength(lbl) / 2, s(340 + i * 0)), lbl, font=f, fill=hexc('#ffffff', int(255 * k)))
        if k > 0:
            line(d, [(x - 40, 400), (x + 40, 450)], '#ffffff', 8)
            line(d, [(x + 40, 400), (x - 40, 450)], '#ffffff', 8)
    wob = 6 * math.sin(t * 8)
    earth(d, 780 + wob, 640, 70)
    f = font(FBK, 90)
    d.text((s(780) - f.getlength("?") / 2, s(480)), "?", font=f, fill=hexc('#ffffff', int(255 * ease((t - 1.6) / 0.3))))
    text_block(img, ["Mercure et Vénus seront avalées.", ("La Terre ? Peut-être aussi. Les astronomes hésitent encore.", 1.5)], t, 1060, '#ffffff', size=64)

def sc_joke(img, d, t, D):
    bg(d, '#fff1c9'); header(d, hexc('#a0661a'))
    # un ventilateur de bureau qui tourne
    cx, cy = 540, 580
    d.rounded_rectangle([s(cx - 20), s(cy + 60), s(cx + 20), s(cy + 300)], radius=s(10), fill=hexc('#6b4a2a'))
    d.rounded_rectangle([s(cx - 150), s(cy + 280), s(cx + 150), s(cy + 330)], radius=s(25), fill=hexc('#6b4a2a'))
    circle(d, cx, cy, 200, outline=hexc('#6b4a2a'), width=10)
    for i in range(3):
        a = t * 14 + i * 2 * math.pi / 3
        d.ellipse([s(cx + 100 * math.cos(a) - 80), s(cy + 100 * math.sin(a) - 45), s(cx + 100 * math.cos(a) + 80), s(cy + 100 * math.sin(a) + 45)], fill=hexc('#7ab8ff'))
    circle(d, cx, cy, 34, fill=hexc('#6b4a2a'))
    text_block(img, ["Et dire qu'on se plaint déjà de la canicule au bureau…"], t, 1060, '#2b1a08', size=72)

def sc_dwarf(img, d, t, D):
    bg(d, '#101a3a'); stars(d, t); header(d, hexc('#c8d6ff'))
    k = ease((t - 0.2) / 1.6)
    r = 300 - 250 * k
    circle(d, 540, 620, r, fill=hexc('#ff5a2a' if k < 0.6 else '#e8f0ff'))
    earth(d, 820, 620, 50, a=int(255 * ease((t - 1.6) / 0.4)))
    text_block(img, ["Ensuite, il se tasse en naine blanche : une braise à peu près de la taille de la Terre."], t, 1060, '#ffffff', size=64)

def sc_certain(img, d, t, D):
    bg(d, '#0f2e1c'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "≈ 100 %", 450, 190, '#a8f0c0', FBK, k)
    ctext(d, "de chances que ça arrive un jour", 700, 44, '#a8f0c0', FM, k)
    text_block(img, [("Pour une fois, les scientifiques sont d'accord : ce scénario-là est quasi certain.", 0.8)], t, 1060, '#ffffff', size=64)

def sc_delay(img, d, t, D):
    bg(d, '#2a1a4a'); header(d, hexc('#d2b8ff'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "× 3 000", 450, 190, '#d2b8ff', FBK, k)
    ctext(d, "l'âge de notre espèce", 700, 44, '#d2b8ff', FM, k)
    text_block(img, [("Mais 1 milliard d'années, c'est plus de 3 000 fois l'âge d'Homo sapiens. On a le temps.", 0.8)], t, 1060, '#ffffff', size=64)

sc_title = scene_title(["GÉANTE", "ROUGE"], "Scénario d'extinction n°11")
sc_end = scene_end("Bref : le Soleil a encore des milliards d'années. Vos impôts, eux, c'est le mois prochain.", color='#8a1f10')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_fuel, 4.4), (sc_brighter, 4.2), (sc_oceans, 4.4),
    (sc_empty, 3.6), (sc_boom, 4.6), (sc_earth, 4.6), (sc_joke, 4.0),
    (sc_dwarf, 4.4), (sc_certain, 4.4), (sc_delay, 4.6), (sc_end, 4.8),
]
