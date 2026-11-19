"""Épisode 36 — Le syndrome de Kessler (débris spatiaux en cascade).
Sources :
- ESA Space Environment Report 2025 (1er avr. 2025, données fin 2024) : ~40 000 objets suivis,
  dont ~11 000 satellites actifs ; plus de 1,2 million d'objets > 1 cm ; plus de 50 000 > 10 cm ;
  « même sans aucun lancement supplémentaire, le nombre de débris continuerait d'augmenter »
  (syndrome de Kessler), consensus scientifique.
- Aerospace America / AIAA (J. Kelvey, « Understanding the misunderstood Kessler Syndrome », 1er mars 2024) :
  article de D. Kessler et B. Cour-Palais (NASA Johnson) en 1978 dans le Journal of Geophysical Research ;
  collision Iridium–Cosmos 2009 : ~2 000 débris d'au moins 10 cm ; la cascade se jouerait sur des
  décennies voire des siècles (pas comme le film Gravity) ; pas une menace pour la vie sur Terre,
  plutôt une dégradation progressive qui coûte cher.
- D. J. Kessler, « The Kessler Syndrome » (page personnelle, 8 mars 2009) : collision du 10 févr. 2009
  à 790 km d'altitude et ~11,6 km/s (≈ 42 000 km/h) ; solutions : ne plus laisser d'objets en orbite
  après usage, et retirer les débris existants.
"""
from engine import *

EPISODE = 36
BOOM_SCENE = 6
LEGENDE = """Épisode 36 : le syndrome de Kessler 🛰️💥

Autour de la Terre, plus d'1,2 million de débris de plus d'1 cm tournent à toute vitesse (ESA). Le risque : une collision crée des débris, qui causent d'autres collisions… une réaction en chaîne imaginée par Donald Kessler, de la NASA, en 1978. Bonne nouvelle : ça prendrait des décennies, et ça ne menace pas la vie sur Terre.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #espace #debrisspatiaux #satellites #kessler #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def earth(d, cx, cy, r):
    circle(d, cx, cy, r, fill=hexc('#2f7fd6'))
    circle(d, cx - r * 0.3, cy - r * 0.2, r * 0.38, fill=hexc('#3fbf6f'))
    circle(d, cx + r * 0.35, cy + r * 0.3, r * 0.28, fill=hexc('#3fbf6f'))

def satellite(d, cx, cy, sc=1.0, col='#e8e8f0', panel='#3fa0ff'):
    d.rectangle([s(cx - 70 * sc), s(cy - 14 * sc), s(cx - 22 * sc), s(cy + 14 * sc)], fill=hexc(panel))
    d.rectangle([s(cx + 22 * sc), s(cy - 14 * sc), s(cx + 70 * sc), s(cy + 14 * sc)], fill=hexc(panel))
    d.rounded_rectangle([s(cx - 22 * sc), s(cy - 22 * sc), s(cx + 22 * sc), s(cy + 22 * sc)], radius=s(6 * sc), fill=hexc(col))

random.seed(36)
DEBRIS = [(random.uniform(0, 6.283), random.uniform(1.25, 1.9), random.uniform(0.25, 0.6), random.uniform(3, 8),
           random.choice(['#ffffff', '#ffd166', '#ff9a3d', '#c8c8d8'])) for _ in range(160)]

def orbit_cloud(d, cx, cy, r, t, n, speed=1.0, size=1.0):
    """Le fil rouge : la Terre et son nuage d'objets en orbite."""
    for i, (a, rr, w, sz, c) in enumerate(DEBRIS[:n]):
        ang = a + t * w * speed
        x = cx + math.cos(ang) * r * rr
        y = cy + math.sin(ang) * r * rr * 0.55
        circle(d, x, y, sz * size, fill=hexc(c))

def chair(d, cx, cy, col):
    d.rectangle([s(cx - 130), s(cy - 260), s(cx - 105), s(cy + 200)], fill=hexc(col))
    d.rectangle([s(cx - 130), s(cy), s(cx + 130), s(cy + 30)], fill=hexc(col))
    d.rectangle([s(cx + 105), s(cy), s(cx + 130), s(cy + 200)], fill=hexc(col))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0d1730'); stars(d, t); header(d, hexc('#9fc2ff'))
    k = ease((t - 0.3) / 0.8)
    earth(d, 540, 620, 150 * k + 1)
    orbit_cloud(d, 540, 620, 150, t, int(60 * k))
    text_block(img, ["Et si nos poubelles de l'espace nous coupaient… du ciel ?"], t, 1080, '#ffffff', size=76)

def sc_tracked(img, d, t, D):
    bg(d, '#102a43'); stars(d, t); header(d, hexc('#a9d6ff'))
    earth(d, 540, 620, 150)
    n = int(20 + 100 * ease((t - 0.2) / 2.5))
    orbit_cloud(d, 540, 620, 150, t, n)
    for i in range(3):
        satellite(d, 540 + 260 * math.cos(t * 0.5 + i * 2.1), 620 + 140 * math.sin(t * 0.5 + i * 2.1), sc=0.6)
    text_block(img, ["Autour de la Terre, environ 40 000 objets sont surveillés.", ("Seulement 11 000 sont des satellites qui marchent.", 1.5)], t, 1040, '#ffffff', size=64)

def sc_small(img, d, t, D):
    bg(d, '#2b1a47'); stars(d, t); header(d, hexc('#d6c2ff'))
    earth(d, 540, 620, 120)
    n = int(40 + 120 * ease((t - 0.5) / 2.0))
    orbit_cloud(d, 540, 620, 150, t, n, size=0.6)
    kk = ease((t - 1.2) / 0.4)
    if kk > 0:
        ctext(d, "1 200 000", 860, 70, '#ffd166', FBK, kk)
    text_block(img, ["Et plus d'1,2 million de débris de plus d'1 cm…", ("…des bouts de fusées et de satellites cassés.", 1.5)], t, 1060, '#ffffff', size=64)

def sc_speed(img, d, t, D):
    bg(d, '#0e3b3b'); header(d, hexc('#9fe3d8'))
    x = -100 + ((t * 600) % 1300)
    for j in range(6):
        line(d, [(x - 60 - j * 70, 560 + (j % 3 - 1) * 30), (x - 30 - j * 70, 560 + (j % 3 - 1) * 30)], hexc('#9fe3d8', 200 - j * 30), 16)
    circle(d, x, 560, 38, fill=hexc('#ffd166'))
    k = ease((t - 0.6) / 0.4)
    ctext(d, "40 000 km/h", 720, 96, '#ffffff', FBK, k)
    text_block(img, ["Ça file à une vitesse folle.", ("Lors d'une collision, le choc peut dépasser 40 000 km/h.", 1.2)], t, 1060, '#ffffff', size=64)

def sc_kessler(img, d, t, D):
    bg(d, '#3a2a12'); header(d, hexc('#ffd59e'))
    # dominos qui tombent
    for i in range(6):
        fall = ease((t - 1.0 - i * 0.25) / 0.3)
        ang = fall * 1.2
        bx, by = 200 + i * 130, 860
        h = 260
        tx, ty = bx + math.sin(ang) * h, by - math.cos(ang) * h
        line(d, [(bx, by), (tx, ty)], '#f3ead6', 46)
    ctext(d, "1978", 380, 110, '#ffd166', FBK, ease((t - 0.2) / 0.4))
    text_block(img, ["1978 : Donald Kessler, de la NASA, imagine une réaction en chaîne.", ("Une collision fait des débris… qui font d'autres collisions… qui font plus de débris.", 1.6)], t, 1010, '#ffffff', size=58)

def sc_boom(img, d, t, D):
    bg(d, '#5a0f1e'); header(d, hexc('#ffb3bd'))
    k = min(1, t / 1.2)
    if t < 1.2:
        satellite(d, 140 + 400 * k, 560, sc=1.0)
        satellite(d, 940 - 400 * k, 560, sc=1.0, panel='#c8c8d8', col='#9a8f78')
    else:
        kk = ease((t - 1.2) / 1.5)
        circle(d, 540, 560, 120 * (1 - kk) + 1, fill=hexc('#ffd166', int(255 * (1 - kk))))
        for i, (a, rr, w, sz, c) in enumerate(DEBRIS[:80]):
            dist = 40 + 420 * kk * rr / 1.9
            circle(d, 540 + math.cos(a) * dist, 560 + math.sin(a) * dist * 0.8, sz * 0.8, fill=hexc(c))
    text_block(img, ["2009 : boum ! Un satellite Iridium percute un vieux satellite russe.", ("Environ 2 000 nouveaux débris de plus de 10 cm.", 1.8)], t, 1030, '#ffffff', size=62)

def sc_worst(img, d, t, D):
    bg(d, '#1d1d2e'); stars(d, t); header(d, hexc('#c8c8ff'))
    earth(d, 540, 620, 130)
    orbit_cloud(d, 540, 620, 150, t, 160, size=0.9)
    k = ease((t - 1.4) / 0.4)
    if k > 0:
        ctext(d, "GPS ?  MÉTÉO ?", 870, 54, '#ff9a3d', FB, k)
    text_block(img, ["Le pire scénario : certaines orbites deviennent trop risquées.", ("Adieu une partie des satellites (GPS, météo, internet).", 1.6)], t, 1040, '#ffffff', size=60)

random.seed(361)
CLOTHES = [(random.uniform(-110, 110), random.choice(['#ff6fb5', '#3fa0ff', '#ffd166', '#3fbf6f', '#8a5cff'])) for _ in range(9)]
def sc_joke(img, d, t, D):
    bg(d, '#f2e8cf'); header(d, hexc('#7a5c2e'))
    n = int(1 + 8 * ease((t - 0.3) / 2.2))
    if n < 6:
        chair(d, 540, 700, '#7a5c2e')
    for i in range(n):
        dx, c = CLOTHES[i]
        y = 680 - i * 38
        d.rounded_rectangle([s(540 + dx - 120), s(y), s(540 + dx + 120), s(y + 40)], radius=s(14), fill=hexc(c))
    text_block(img, ["C'est la chaise de votre chambre : un t-shirt, puis un autre…", ("…et un jour, plus personne ne sait où est la chaise.", 1.7)], t, 1040, '#2b1a10', size=60)

def sc_slow(img, d, t, D):
    bg(d, '#14365a'); header(d, hexc('#a6e6ff'))
    # sablier
    d.polygon([(s(400), s(380)), (s(680), s(380)), (s(540), s(620))], fill=hexc('#f3ead6'))
    d.polygon([(s(400), s(860)), (s(680), s(860)), (s(540), s(620))], fill=hexc('#f3ead6'))
    k = (t / D)
    d.polygon([(s(430 + 80 * k), s(400 + 120 * k)), (s(650 - 80 * k), s(400 + 120 * k)), (s(540), s(600))], fill=hexc('#ffd166'))
    d.polygon([(s(540 - 120 * k), s(840)), (s(540 + 120 * k), s(840)), (s(540), s(840 - 120 * k))], fill=hexc('#ffd166'))
    text_block(img, ["Bonne nouvelle : ce n'est pas un film catastrophe.", ("Selon les experts, la cascade prendrait des décennies, voire des siècles.", 1.5)], t, 1040, '#ffffff', size=60)

def sc_science(img, d, t, D):
    bg(d, '#0f3d2e'); header(d, hexc('#9fe3b0'))
    earth(d, 540, 620, 170)
    kk = ease((t - 0.6) / 0.4)
    if kk > 0:
        ctext(d, "LA VIE CONTINUE", 840, 52, '#9fe3b0', FB, kk)
    text_block(img, ["Et ça ne tuerait pas l'humanité : en bas, la vie continue.", ("Mais d'après l'ESA, les débris augmenteraient même sans aucun nouveau lancement.", 1.6)], t, 1020, '#ffffff', size=58)

def sc_fix(img, d, t, D):
    bg(d, '#24163d'); stars(d, t); header(d, hexc('#d2b8ff'))
    k = ease((t - 0.3) / 2.5)
    # un « camion-poubelle » spatial attrape un débris
    satellite(d, 230 + 180 * k, 600, sc=1.8, panel='#3fbf6f')
    line(d, [(360 + 180 * k, 600), (600 + 110 * k, 600)], '#ffffff', 10)
    circle(d, 780, 600 + 10 * math.sin(t * 3), 48, fill=hexc('#ff9a3d'))
    text_block(img, ["La solution : ne plus abandonner nos vieux satellites là-haut…", ("…et aller chercher les débris.", 1.5)], t, 1040, '#ffffff', size=62)

sc_title = scene_title(["DÉBRIS", "EN CHAÎNE"], "Scénario d'extinction n°36")
sc_end = scene_end("Bref : même sans GPS, les impôts sauront toujours vous retrouver.")

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_tracked, 4.4), (sc_small, 4.2), (sc_speed, 3.8),
    (sc_kessler, 4.8), (sc_boom, 4.6), (sc_worst, 4.4), (sc_joke, 4.6),
    (sc_slow, 4.4), (sc_science, 4.8), (sc_fix, 4.2), (sc_end, 4.8),
]
