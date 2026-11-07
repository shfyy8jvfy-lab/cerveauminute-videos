"""Épisode 12 — Mythe : le LHC qui crée un trou noir.
Sources : CERN, « The safety of the LHC » (public-archive.web.cern.ch) ; rapport LSAG 2008 (arXiv:0806.3414),
repris par ScienceDaily / Institute of Physics (5 sept. 2008) ; Scientific American et NBC News (plainte
déposée à Hawaï en 2008, rejetée par le juge) ; Universe Today.
- LHC : anneau de 27 km sous la frontière franco-suisse, protons accélérés presque à la vitesse de la lumière.
- Énergie d'une collision ≈ celle de deux moustiques qui se cognent (Institute of Physics / LSAG).
- La nature a déjà fait l'équivalent d'environ 100 000 programmes LHC sur Terre via les rayons cosmiques
  (LSAG ; le CERN dit même « environ un million ») — et la Terre existe toujours. On garde le chiffre le plus prudent.
- Un éventuel mini trou noir se désintégrerait immédiatement selon la théorie (rayonnement de Hawking) ;
  la survie des étoiles à neutrons et naines blanches exclut tout trou noir dangereux.
"""
from engine import *

EPISODE = 12
BOOM_SCENE = 5
LEGENDE = """Épisode 12 : le LHC va-t-il créer un trou noir ? 🕳️⚛️

C'est un mythe. En 2008, on a eu peur que l'accélérateur du CERN fabrique un trou noir qui avalerait la Terre. Mais la nature fait des chocs bien plus violents depuis des milliards d'années : l'équivalent d'environ 100 000 programmes LHC déjà réalisés sur Terre (rapport de sécurité du CERN, 2008). Et la planète est toujours là.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #cern #trounoir #physique #science #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def ring(d, cx, cy, r, t, col='#7fd8ff', w=22, dots=True, a=255):
    """Le fil rouge : l'anneau du LHC, avec deux particules qui tournent en sens inverse."""
    d.ellipse([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], outline=hexc(col, a), width=s(w))
    if dots:
        for sgn, c in ((1, '#ffffff'), (-1, '#ffd23f')):
            ang = sgn * t * 3.2
            for k in range(5):
                aa = ang - sgn * k * 0.09
                circle(d, cx + r * math.cos(aa), cy + r * math.sin(aa), (16 - k * 3), fill=hexc(c, int(a * (1 - k * 0.18))))

def earth(d, cx, cy, r, a=255):
    circle(d, cx, cy, r, fill=hexc('#2f7de1', a))
    for (dx, dy, rr) in ((-0.35, -0.25, 0.32), (0.3, 0.2, 0.28), (0.05, -0.5, 0.18), (-0.15, 0.45, 0.2)):
        circle(d, cx + dx * r, cy + dy * r, rr * r, fill=hexc('#3fbf6a', a))

def blackhole(d, cx, cy, r, t, a=255):
    for i in range(3):
        rr = r * (1.9 - i * 0.25)
        d.ellipse([s(cx - rr), s(cy - rr * 0.32), s(cx + rr), s(cy + rr * 0.32)], outline=hexc(['#ff7a1a', '#ffb347', '#ffe08a'][i], a), width=s(max(3, r * 0.08)))
    circle(d, cx, cy, r * 1.08, fill=hexc('#ff9a3c', int(a * 0.6)))
    circle(d, cx, cy, r, fill=hexc('#000000', a))

def mosquito(d, cx, cy, flip, t, col='#3a2a1a'):
    m = -1 if flip else 1
    flap = 18 * math.sin(t * 40)
    d.ellipse([s(cx - 40), s(cy - 60 - flap), s(cx + 10), s(cy - 5)], fill=hexc('#ffffff', 150))
    d.ellipse([s(cx - 10), s(cy - 60 + flap), s(cx + 40), s(cy - 5)], fill=hexc('#ffffff', 150))
    d.ellipse([s(cx - 70), s(cy - 14), s(cx + 50), s(cy + 14)], fill=hexc(col))
    circle(d, cx + m * 62, cy - 4, 18, fill=hexc(col))
    line(d, [(cx + m * 76, cy - 2), (cx + m * 120, cy + 8)], col, 4)
    for k in (-40, -10, 20):
        line(d, [(cx + k, cy + 10), (cx + k - 15, cy + 55), (cx + k - 25, cy + 75)], col, 4)

def gavel(d, cx, cy, lift, col='#8a5a3c'):
    """Marteau de juge : tête horizontale + manche, qui monte et retombe."""
    y = cy - lift
    line(d, [(cx + 40, y - 10), (cx + 230, y - 150)], col, 26)
    d.rounded_rectangle([s(cx - 120), s(y - 55), s(cx + 120), s(y + 45)], radius=s(18), fill=hexc('#a0704c'))
    d.rectangle([s(cx - 80), s(y - 55), s(cx - 60), s(y + 45)], fill=hexc('#5a3824'))
    d.rectangle([s(cx + 60), s(y - 55), s(cx + 80), s(y + 45)], fill=hexc('#5a3824'))

def pen(d, x, y, col):
    d.rounded_rectangle([s(x - 12), s(y - 80), s(x + 12), s(y + 60)], radius=s(10), fill=hexc(col))
    d.polygon([(s(x - 12), s(y + 60)), (s(x + 12), s(y + 60)), (s(x), s(y + 90))], fill=hexc('#2b1a10'))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b1230'); stars(d, t); header(d, hexc('#7fd8ff'))
    earth(d, 540, 640, 150)
    ring(d, 540, 640, 260, t)
    text_block(img, ["Et si une machine de scientifiques avalait la Terre ?"], t, 1090, '#ffffff', size=80)

def sc_ring(img, d, t, D):
    bg(d, '#123a2a'); header(d, hexc('#a8f0c0'))
    # sol vu du dessus : petites maisons, et l'anneau qui se dessine
    for (x, y) in ((200, 420), (860, 470), (300, 860), (820, 850), (540, 380), (150, 700), (930, 690)):
        d.rounded_rectangle([s(x - 30), s(y - 22), s(x + 30), s(y + 22)], radius=s(6), fill=hexc('#2c5e46'))
    k = ease((t - 0.2) / 1.2)
    d.arc([s(540 - 280), s(640 - 280), s(540 + 280), s(640 + 280)], -90, -90 + 360 * k, fill=hexc('#7fd8ff'), width=s(22))
    if k > 0.98:
        ring(d, 540, 640, 280, t, dots=True)
    ctext(d, "27 km", 600, 70, '#ffffff', FBK, ease((t - 1.3) / 0.4))
    text_block(img, ["Sous la frontière franco-suisse, au CERN : un anneau géant, le LHC."], t, 1070, '#ffffff', size=70)

def sc_collide(img, d, t, D):
    bg(d, '#1b2a4a'); header(d, hexc('#9fc2ff'))
    ring(d, 540, 640, 280, t, col='#3a5a8a', dots=False)
    k = ease((t - 0.3) / 1.3)
    x1, x2 = 220 + 320 * k, 860 - 320 * k
    for x, c in ((x1, '#ffffff'), (x2, '#ffd23f')):
        line(d, [(x - (40 if c == '#ffffff' else -40), 640), (x, 640)], c, 6)
        circle(d, x, 640, 26, fill=hexc(c))
    f = ease((t - 1.6) / 0.5)
    if f > 0:
        for i in range(14):
            a = i * math.pi / 7
            r0, r1 = 40 * f, 40 + 170 * f
            line(d, [(540 + r0 * math.cos(a), 640 + r0 * math.sin(a)), (540 + r1 * math.cos(a), 640 + r1 * math.sin(a))], '#ffd23f', 6)
        circle(d, 540, 640, 40 * (1 - f) + 10, fill=hexc('#ffffff'))
    text_block(img, ["On y lance des grains de matière minuscules (protons) presque à la vitesse de la lumière…", ("…et on les fait se percuter.", 2.0)], t, 1030, '#ffffff', size=64)

def sc_rumor(img, d, t, D):
    bg(d, '#3a1f08'); header(d, hexc('#ffd37a'))
    ring(d, 540, 640, 280, t, col='#a8742a')
    r = 20 + 25 * ease((t - 0.8) / 1.5)
    blackhole(d, 540, 640, r, t)
    for i, (x, y) in enumerate(((250, 420), (830, 430), (820, 880))):
        k = ease((t - 0.5 - i * 0.4) / 0.3)
        if k > 0:
            d.text((s(x - 25), s(y - 50)), "?", font=font(FBK, 100), fill=hexc('#ffd37a', int(255 * k)))
    text_block(img, ["En 2008, une rumeur affole la planète : ces chocs pourraient créer un mini trou noir."], t, 1060, '#ffffff', size=68)

def sc_boom(img, d, t, D):
    bg(d, '#14060a'); stars(d, t, col='#ffb0a0'); header(d, hexc('#ffb0a0'))
    k = ease(t / 2.6)
    er = 170 * (1 - 0.85 * k)
    ex = 540 + 120 * (1 - k) * math.cos(t * 3); ey = 640 + 60 * (1 - k) * math.sin(t * 3)
    if t < 3.0:
        earth(d, ex, ey, er, a=int(255 * (1 - ease((t - 2.4) / 0.5))))
    blackhole(d, 540, 640, 40 + 90 * k, t)
    text_block(img, ["Un trou noir qui grossirait, grossirait…", ("…et finirait par avaler la Terre.", 1.5)], t, 1060, '#ffffff', size=72)

def sc_court(img, d, t, D):
    bg(d, '#2d2d2d'); header(d, hexc('#d0d0d0'))
    d.rounded_rectangle([s(320), s(820), s(760), s(900)], radius=s(16), fill=hexc('#5a3824'))
    hit = t % 1.4
    lift = 160 * (1 - ease(hit / 0.25)) if hit < 0.25 else 160 * ease((hit - 0.25) / 0.8)
    gavel(d, 540, 760, lift)
    if 0.2 < hit < 0.5:
        for i in range(5):
            a = math.pi + i * math.pi / 4
            line(d, [(540 + 150 * math.cos(a), 820 + 40 * math.sin(a)), (540 + 210 * math.cos(a), 820 + 70 * math.sin(a))], '#ffffff', 6)
    ctext(d, "PLAINTE REJETÉE", 400, 64, '#ff6f6f', FBK, ease((t - 1.6) / 0.4))
    text_block(img, ["Des gens ont même porté plainte à Hawaï pour arrêter la machine.", ("Le juge a dit non.", 1.8)], t, 1040, '#ffffff', size=68)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    # un bureau avec un tiroir ouvert, des stylos qui tombent dedans
    d.rounded_rectangle([s(230), s(560), s(850), s(900)], radius=s(20), fill=hexc('#c99a6b'))
    d.rounded_rectangle([s(300), s(620), s(780), s(760)], radius=s(16), fill=hexc('#000000'))
    circle(d, 540, 820, 18, fill=hexc('#8a5a3c'))
    cols = ['#2f7de1', '#e14b4b', '#2b2b2b', '#3fbf6a']
    for i in range(4):
        tt = (t - 0.3 - i * 0.9)
        if tt < 0: continue
        y = 330 + 420 * min(1, tt / 0.8) ** 2
        if y < 680:
            pen(d, 380 + i * 105, y, cols[i])
    text_block(img, ["Le seul vrai trou noir du CERN ?", ("Le tiroir où disparaissent tous les stylos.", 1.4)], t, 1020, '#2b1a10', size=70)

def sc_mosquito(img, d, t, D):
    bg(d, '#cfe9d8'); header(d, hexc('#2c5e46'))
    k = ease((t - 0.2) / 1.2)
    mosquito(d, 200 + 230 * k, 620 + 10 * math.sin(t * 5), False, t)
    mosquito(d, 880 - 230 * k, 620 + 10 * math.cos(t * 5), True, t)
    if t > 1.4:
        ctext(d, "toc.", 470, 60, '#2c5e46', FB, ease((t - 1.4) / 0.3))
    text_block(img, ["En vrai, chaque choc du LHC libère à peu près l'énergie de deux moustiques qui se cognent."], t, 1060, '#10301f', size=66)

random.seed(12)
RAYS = [(random.uniform(0, 1080), random.uniform(-0.6, 0.6), random.uniform(0, 3.5)) for _ in range(26)]
def sc_cosmic(img, d, t, D):
    bg(d, '#101a3a'); stars(d, t); header(d, hexc('#c8d6ff'))
    earth(d, 540, 820, 170)
    for (x0, sl, ph) in RAYS:
        p = ((t + ph) % 1.2) / 1.2
        x = x0 + sl * 500 * p; y = 300 + 520 * p
        if math.hypot(x - 540, y - 820) > 175:
            line(d, [(x - sl * 90, y - 90), (x, y)], '#ffe08a', 5)
    text_block(img, ["Et l'espace bombarde la Terre de chocs bien plus violents depuis des milliards d'années (rayons cosmiques)."], t, 1060, '#ffffff', size=62)

def sc_number(img, d, t, D):
    bg(d, '#0f2e1c'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.4)
    n = int(100000 * ease(t / 1.4))
    ctext(d, f"{n:,}".replace(',', ' '), 470, 190, '#a8f0c0', FBK, k)
    ctext(d, "expériences du LHC déjà « faites »", 720, 44, '#a8f0c0', FM, k)
    ctext(d, "par la nature, sur Terre", 780, 44, '#a8f0c0', FM, k)
    text_block(img, [("C'est l'estimation du rapport de sécurité du CERN.", 0.6), ("Et la Terre est toujours là.", 2.0)], t, 1040, '#ffffff', size=66)

def sc_evaporate(img, d, t, D):
    bg(d, '#2a1a4a'); header(d, hexc('#d2b8ff'))
    k = ease((t - 0.6) / 1.4)
    if k < 1:
        blackhole(d, 540, 640, 70 * (1 - k) + 1, t, a=int(255 * (1 - k)))
    random.seed(3)
    for i in range(24):
        a = random.uniform(0, 2 * math.pi); sp = random.uniform(120, 300)
        r = sp * k
        if k > 0:
            circle(d, 540 + r * math.cos(a), 640 + r * math.sin(a), 8 * (1 - k * 0.6), fill=hexc('#ffe08a', int(255 * (1 - k * 0.7))))
    text_block(img, ["Et même si un mini trou noir apparaissait, la théorie prédit qu'il s'évaporerait aussitôt."], t, 1060, '#ffffff', size=66)

sc_title = scene_title(["TROU NOIR", "AU CERN"], "Scénario d'extinction n°12 · mythe")
sc_end = scene_end("Bref : aucun trou noir ne vous avalera. Mais vous devrez quand même payer vos impôts.", color='#7a1030')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_ring, 4.0), (sc_collide, 4.4), (sc_rumor, 4.2),
    (sc_boom, 4.0), (sc_court, 4.2), (sc_joke, 4.6), (sc_mosquito, 4.2), (sc_cosmic, 4.4),
    (sc_number, 4.8), (sc_evaporate, 4.2), (sc_end, 4.8),
]
