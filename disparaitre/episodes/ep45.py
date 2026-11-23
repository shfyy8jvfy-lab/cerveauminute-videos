"""Épisode 45 — La grippe aviaire H5N1 qui s'adapte à l'humain.
Sources :
- OMS, tableau cumulatif des cas humains de grippe A(H5N1), données au 31 mars 2026 : 997 cas confirmés en
  laboratoire depuis 2003, dont 478 décès (≈ 48 % des cas recensés ; les cas bénins passent souvent inaperçus).
- CDC, « A(H5) Bird Flu: Current Situation » (mise à jour 20 nov. 2026) : 75 cas humains aux États-Unis depuis 2024,
  surtout des employés de fermes laitières et avicoles ; « le risque actuel pour la santé publique est faible ».
  Épidémie chez les vaches laitières américaines détectée en mars 2024 (USDA).
- Lin et al., Science, 5 déc. 2024 (Scripps Research) ; communiqué NIH du 6 déc. 2024 : une seule mutation (Q226L)
  de l'hémagglutinine du virus bovin la fait passer des récepteurs « oiseau » aux récepteurs « humains ». Testé sur la
  protéine seule, pas sur un virus complet ; les auteurs précisent que cela ne veut pas dire qu'une pandémie est
  imminente.
- OMS, évaluations du risque à l'interface humain-animal (2026) : pas de transmission interhumaine durable observée ;
  risque pour la population générale jugé faible. Premiers cas humains connus : Hong Kong, 1997.
- Vaccins H5 : stocks constitués (achat conjoint UE de doses en 2024, réserve stratégique des États-Unis).
"""
from engine import *

EPISODE = 45
BOOM_SCENE = 6
LEGENDE = """Épisode 45 : et si la grippe aviaire apprenait à passer d'humain à humain ? 🐦🦠

Le virus H5N1 circule chez les oiseaux, et depuis 2024 chez des vaches laitières aux États-Unis. Chez l'humain, il reste rare (997 cas recensés par l'OMS depuis 2003) mais grave. Une étude parue dans Science en 2024 montre qu'une seule mutation pourrait l'aider à s'accrocher à nos cellules. Pour l'instant, pas de transmission durable entre humains : le risque pour le public reste faible, mais on le surveille de très près.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #grippeaviaire #h5n1 #pandemie #virus #science #vulgarisation #apocalypse"""

def xtext(d, txt, x, y, size, color, fpath=FB, alpha=1.0):
    f = font(fpath, size)
    d.text((s(x) - f.getlength(txt) / 2, s(y)), txt, font=f, fill=hexc(color)[:3] + (int(255 * alpha),))

# ---------- fil rouge : le virus (boule à « clés ») ----------
def virus(d, cx, cy, r, t, col='#e8455a', key='#ffd23f', a=255, nspk=12, hl=True):
    rot = t * 0.6
    for i in range(nspk):
        ang = rot + i * math.pi * 2 / nspk
        x0, y0 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        x1, y1 = cx + r * 1.35 * math.cos(ang), cy + r * 1.35 * math.sin(ang)
        line(d, [(x0, y0), (x1, y1)], hexc(key, a), max(4, int(r * 0.09)))
        circle(d, x1, y1, r * 0.13, fill=hexc(key, a))
    circle(d, cx, cy, r, fill=hexc(col, a))
    if not hl: return
    circle(d, cx - r * 0.3, cy - r * 0.3, r * 0.22, fill=hexc('#ffffff', int(a * 0.35)))
    circle(d, cx + r * 0.25, cy + r * 0.2, r * 0.15, fill=hexc('#ffffff', int(a * 0.2)))

def bird(d, cx, cy, sc, t, col='#3d7bd9'):
    flap = 18 * math.sin(t * 8) * sc
    d.ellipse([s(cx - 90 * sc), s(cy - 50 * sc), s(cx + 90 * sc), s(cy + 50 * sc)], fill=hexc(col))
    circle(d, cx + 85 * sc, cy - 45 * sc, 42 * sc, fill=hexc(col))
    d.polygon([(s(cx + 122 * sc), s(cy - 52 * sc)), (s(cx + 165 * sc), s(cy - 40 * sc)), (s(cx + 120 * sc), s(cy - 30 * sc))], fill=hexc('#ffb02e'))
    circle(d, cx + 98 * sc, cy - 55 * sc, 7 * sc, fill=hexc('#ffffff'))
    d.polygon([(s(cx - 20 * sc), s(cy - 10 * sc)), (s(cx + 40 * sc), s(cy - 10 * sc)), (s(cx - 40 * sc), s(cy - 110 * sc - flap))], fill=hexc('#2a5fb0'))

def cow(d, cx, cy, t):
    chew = 4 * math.sin(t * 6)
    d.rounded_rectangle([s(cx - 210), s(cy - 90), s(cx + 150), s(cy + 90)], radius=s(60), fill=hexc('#ffffff'))
    for (dx, dy, rr) in [(-120, -20, 42), (0, 30, 34), (70, -40, 28)]:
        circle(d, cx + dx, cy + dy, rr, fill=hexc('#2b2b2b'))
    for lx in (-170, -90, 40, 110):
        d.rounded_rectangle([s(cx + lx), s(cy + 70), s(cx + lx + 34), s(cy + 190)], radius=s(12), fill=hexc('#ffffff'))
    d.rounded_rectangle([s(cx + 120), s(cy - 140 + chew), s(cx + 280), s(cy + 10 + chew)], radius=s(50), fill=hexc('#ffffff'))
    d.rounded_rectangle([s(cx + 190), s(cy - 50 + chew), s(cx + 290), s(cy + 20 + chew)], radius=s(30), fill=hexc('#f7a8b8'))
    circle(d, cx + 175, cy - 90 + chew, 9, fill=hexc('#2b2b2b'))
    d.ellipse([s(cx + 110), s(cy - 150 + chew), s(cx + 150), s(cy - 120 + chew)], fill=hexc('#2b2b2b'))

# serrure : rectangle arrondi avec une encoche ronde (oiseau) ou carrée (humain)
def lock(d, cx, cy, shape, col, a=255):
    d.rounded_rectangle([s(cx - 90), s(cy - 70), s(cx + 90), s(cy + 110)], radius=s(26), fill=hexc(col, a))
    if shape == 'round':
        circle(d, cx, cy - 66, 34, fill=hexc('#1c1c2b', a))
    else:
        d.rectangle([s(cx - 30), s(cy - 70), s(cx + 30), s(cy - 16)], fill=hexc('#1c1c2b', a))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0f2a3d'); header(d, hexc('#9fd8ff'))
    bird(d, 400, 640, 1.3, t)
    virus(d, 770, 470 + 12 * math.sin(t * 3), 55, t)
    text_block(img, ["Et si la grippe des oiseaux apprenait à passer d'humain à humain ?"], t, 1080, '#ffffff', size=74)

def sc_virus(img, d, t, D):
    bg(d, '#3a1340'); header(d, hexc('#f0b8ff'))
    k = ease((t - 0.1) / 0.8)
    virus(d, 540, 620, 60 + 130 * k, t, hl=False)
    xtext(d, "H5N1", 540, 620 - (30 + 50 * k) * 0.62, int(30 + 50 * k), '#ffffff', FBK, k)
    text_block(img, ["H5N1, c'est un virus de grippe des oiseaux.", ("Premiers cas humains connus : 1997.", 1.3)], t, 1040, '#ffffff', size=68)

def sc_cows(img, d, t, D):
    bg(d, '#2f6b3a'); header(d, hexc('#c8f5b0'))
    cow(d, 470, 640, t)
    virus(d, 820, 420 + 10 * math.sin(t * 3), 45, t, a=int(255 * ease((t - 0.8) / 0.5)))
    text_block(img, ["Depuis 2024, aux États-Unis, il infecte même des vaches laitières."], t, 1060, '#ffffff', size=70)

def sc_cases(img, d, t, D):
    bg(d, '#1d2b55'); header(d, hexc('#b8c8ff'))
    k = ease((t - 0.2) / 1.6)
    n = 100
    for i in range(n):
        x = 230 + (i % 10) * 69
        y = 330 + (i // 10) * 62
        dead = i % 2 == 0 and i < 96
        col = '#ff5a6e' if (dead and k * n > i) else '#dbe3ff'
        circle(d, x, y, 22, fill=hexc(col))
    text_block(img, ["Chez l'humain : 997 cas recensés par l'OMS depuis 2003.", ("Presque la moitié en sont morts.", 1.6)], t, 1040, '#ffffff', size=66)

def sc_lock(img, d, t, D):
    bg(d, '#f4e3c4'); header(d, hexc('#8a5a2c'))
    lock(d, 300, 700, 'round', '#3d7bd9')
    lock(d, 780, 700, 'square', '#e07a3c')
    xtext(d, "oiseau", 300, 830, 40, '#2b1a10', FB)
    xtext(d, "humain", 780, 830, 40, '#2b1a10', FB)
    k = ease((t - 0.4) / 1.0)
    vx = 540 - 240 * k
    virus(d, vx, 450, 55, t)
    if t > 1.5:
        circle(d, 420, 470, 26, fill=hexc('#2a9a4a'))
    if t > 2.2:
        line(d, [(760, 500), (800, 540)], '#c22a2a', 10); line(d, [(800, 500), (760, 540)], '#c22a2a', 10)
    text_block(img, ["Ses « clés » ouvrent surtout les cellules des oiseaux. Pas bien les nôtres."], t, 1060, '#2b1a10', size=68)

def sc_boom(img, d, t, D):
    bg(d, '#5a0a14'); header(d, hexc('#ffc2c8'))
    if t < 1.4:
        virus(d, 540, 620, 120, t, key='#ffd23f')
        if t > 0.7:
            circle(d, 540 + 160, 620 - 160, 30 + 8 * math.sin(t * 20), fill=hexc('#ffffff'))
    else:
        tt = t - 1.4
        rnd = random.Random(45)
        pts = [(540, 620)] + [(540 + rnd.uniform(-430, 430), 620 + rnd.uniform(-290, 290)) for _ in range(30)]
        nshow = min(len(pts), 1 + int(tt * 10))
        for (x, y) in pts[:nshow]:
            virus(d, x, y, 34, t, key='#ff9ab0', nspk=8)
    text_block(img, ["Le cauchemar : une mutation change ses clés…", ("…et le virus passe d'humain à humain.", 1.4)], t, 1040, '#ffffff', size=68)

def sc_study(img, d, t, D):
    bg(d, '#0e4a4a'); header(d, hexc('#a8f0e8'))
    # éprouvette
    d.rounded_rectangle([s(470), s(320), s(610), s(860)], radius=s(70), outline=hexc('#ffffff'), width=s(8))
    lvl = 600 + 20 * math.sin(t * 2)
    d.rounded_rectangle([s(482), s(lvl), s(598), s(848)], radius=s(58), fill=hexc('#4fd1b8'))
    for i in range(4):
        by = 820 - ((t * 120 + i * 60) % 220)
        circle(d, 520 + 30 * (i % 2), by, 10, fill=hexc('#ffffff', 170))
    virus(d, 790, 470, 50, t)
    xtext(d, "1 mutation", 790, 570, 38, '#a8f0e8', FB, ease((t - 0.5) / 0.4))
    text_block(img, ["2024, revue Science : une seule mutation pourrait l'aider à s'accrocher à nos cellules.", ("(Testé sur une protéine, pas sur le virus entier.)", 1.8)], t, 1010, '#ffffff', size=60)

def sc_joke(img, d, t, D):
    bg(d, '#ffd6e0'); header(d, hexc('#a0304a'))
    bird(d, 540, 680, 1.4, t, col='#8a8f9e')
    k = ease((t - 0.5) / 0.4)
    if k > 0:
        line(d, [(380, 420), (700, 920)], hexc('#c22a2a', int(255 * k)), 16)
        circle(d, 540, 670, 260, outline=hexc('#c22a2a', int(255 * k)), width=16)
    text_block(img, ["Conseil du jour :", ("ne faites pas la bise aux pigeons.", 1.0)], t, 1080, '#3a0f1a', size=74)

def sc_now(img, d, t, D):
    bg(d, '#2a2350'); header(d, hexc('#cfc4ff'))
    for i, x in enumerate([300, 540, 780]):
        y = 620 + 8 * math.sin(t * 2 + i)
        circle(d, x, y - 90, 50, fill=hexc('#cfc4ff'))
        d.rounded_rectangle([s(x - 70), s(y - 30), s(x + 70), s(y + 140)], radius=s(40), fill=hexc('#cfc4ff'))
    k = ease((t - 0.6) / 0.6)
    for x in (420, 660):
        line(d, [(x - 25, 560), (x + 25, 610)], hexc('#ff5a6e', int(255 * k)), 10)
        line(d, [(x + 25, 560), (x - 25, 610)], hexc('#ff5a6e', int(255 * k)), 10)
    text_block(img, ["Aujourd'hui : aucune transmission durable entre humains.", ("Les malades ont attrapé le virus au contact d'animaux.", 1.6)], t, 1020, '#ffffff', size=62)

def sc_watch(img, d, t, D):
    bg(d, '#0d3b66'); header(d, hexc('#a8d4ff'))
    virus(d, 470, 600, 90, t)
    k = 0.5 + 0.5 * math.sin(t * 1.5)
    lx, ly = 420 + 140 * k, 560
    circle(d, lx, ly, 110, outline=hexc('#ffffff'), width=14)
    line(d, [(lx + 78, ly + 78), (lx + 190, ly + 190)], '#ffffff', 26)
    for i in range(3):
        d.rounded_rectangle([s(760 + i * 70), s(780), s(800 + i * 70), s(900)], radius=s(12), fill=hexc('#8fe3a0'))
        d.rectangle([s(770 + i * 70), s(760), s(790 + i * 70), s(782)], fill=hexc('#ffffff'))
    text_block(img, ["Chaque mutation est surveillée. Et des vaccins contre H5 sont déjà en stock."], t, 1060, '#ffffff', size=66)

def sc_verdict(img, d, t, D):
    bg(d, '#3b2a0a'); header(d, hexc('#ffe0a0'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "RISQUE FAIBLE", 470, 120, '#ffe0a0', FBK, k)
    ctext(d, "pour le public, aujourd'hui (OMS, CDC)", 650, 42, '#ffe0a0', FM, k)
    text_block(img, [("Mais c'est l'un des virus que les experts surveillent le plus pour la prochaine pandémie.", 0.8)], t, 1040, '#ffffff', size=64)

sc_title = scene_title(["GRIPPE", "AVIAIRE"], "Risque sérieux · n°45", color='#8f1d3a')
sc_end = scene_end("Bref : la grippe aviaire ne nous aura pas cette année. Les impôts, si.", color='#8f1d3a')

SCENES = [
    (sc_hook, 3.0), (sc_title, 2.4), (sc_virus, 4.2), (sc_cows, 4.4), (sc_cases, 4.4),
    (sc_lock, 4.6), (sc_boom, 4.6), (sc_study, 4.4), (sc_joke, 3.8), (sc_now, 4.4),
    (sc_watch, 4.2), (sc_verdict, 4.4), (sc_end, 4.8),
]
