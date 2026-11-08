"""Épisode 14 — Le Big Rip (l'univers qui se déchire).
Sources :
- Caldwell, Kamionkowski & Weinberg, « Phantom Energy and Cosmic Doomsday », Physical Review Letters 91 (2003) :
  si l'énergie noire se renforce avec le temps, l'univers finit déchiré. Exemple étudié : fin dans ~22 milliards
  d'années ; la Voie lactée dispersée ~60 millions d'années avant, la Terre détachée du Soleil ~3 mois avant,
  la Terre qui explose ~30 minutes avant, les atomes ~10^-19 s avant (PDF Rutgers ; NBC News ; Science News Explores).
- Expansion accélérée découverte en 1998 (supernovas, prix Nobel 2011).
- DESI (2024-2025) : indices que l'énergie noire faiblirait plutôt qu'elle ne se renforce, ce qui éloigne le Big Rip
  (Space.com, Physics World, Sky & Telescope, Smithsonian). Résultats encore à confirmer.
"""
from engine import *

EPISODE = 14
BOOM_SCENE = 8
LEGENDE = """Épisode 14 : le Big Rip, l'univers qui se déchire 🌌✂️

En 2003, trois physiciens ont calculé que si l'énergie noire se renforçait avec le temps, elle finirait par tout déchirer : galaxies, planètes et même atomes (Physical Review Letters). Bonne nouvelle : les mesures récentes du relevé DESI suggèrent plutôt une énergie noire qui faiblit, et même le pire scénario étudié se situait dans environ 22 milliards d'années.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #univers #cosmologie #astronomie #energienoire #science #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
random.seed(14)
DOTS = [(random.uniform(0, 2 * math.pi), random.uniform(0.15, 0.85)) for _ in range(16)]
COLS = ['#ffd166', '#7ff0e0', '#ff6fb5', '#9fc2ff']

def balloon(d, cx, cy, r, t, col='#3d5afe', dotc=None):
    """Fil rouge : l'univers comme un ballon couvert de galaxies (points)."""
    circle(d, cx, cy, r, fill=hexc(col))
    circle(d, cx - r * 0.35, cy - r * 0.4, r * 0.18, fill=hexc('#ffffff', 60))
    d.polygon([(s(cx - 18), s(cy + r + 22)), (s(cx + 18), s(cy + r + 22)), (s(cx), s(cy + r - 4))], fill=hexc(col))
    line(d, [(cx, cy + r + 22), (cx + 10 * math.sin(t * 3), cy + r + 120)], '#ffffff', 4)
    for i, (a, rr) in enumerate(DOTS):
        x, y = cx + math.cos(a) * rr * r, cy + math.sin(a) * rr * r
        circle(d, x, y, max(6, r * 0.05), fill=hexc(dotc or COLS[i % 4]))

def sc_hook(img, d, t, D):
    bg(d, '#14102a'); header(d, hexc('#c9b8ff'))
    k = ease((t - 0.5) / 1.6)
    gap = 90 * k
    for side in (-1, 1):
        pts = [(540 + side * (gap + 220), 360), (540 + side * gap, 360)]
        for j in range(9):
            pts.append((540 + side * gap + (25 if j % 2 else -25), 360 + (j + 1) * 62))
        pts.append((540 + side * (gap + 220), 918))
        d.polygon([(s(x), s(y)) for x, y in pts], fill=hexc('#f3efe6'))
    text_block(img, ["Et si l'univers finissait… déchiré comme une feuille de papier ?"], t, 1090, '#ffffff', size=80)

def sc_expand(img, d, t, D):
    bg(d, '#0b2545'); header(d, hexc('#9fc2ff'))
    r = 150 + 140 * ease(t / 3.5)
    balloon(d, 540, 600, r, t)
    text_block(img, ["L'univers grandit : les galaxies s'éloignent, comme des points sur un ballon qu'on gonfle."], t, 1080, '#ffffff', size=66)

def sc_accel(img, d, t, D):
    bg(d, '#1d3a2a'); header(d, hexc('#a8f0c0'))
    r = 150 + 150 * (t / D) ** 2
    balloon(d, 540, 600, r, t, col='#2e7d5b')
    for i in range(3):
        k = ease((t - 0.8 - i * 0.4) / 0.4)
        if k > 0:
            y = 400 + i * 60
            line(d, [(880, y + 40), (950, y - 30 * k)], '#a8f0c0', 12)
    text_block(img, ["Depuis 1998, on sait que ça accélère. Le moteur mystérieux s'appelle l'« énergie noire »."], t, 1080, '#ffffff', size=66)

def sc_stronger(img, d, t, D):
    bg(d, '#3a1430'); header(d, hexc('#ffb3e0'))
    k = ease(t / 3.5)
    balloon(d, 380, 600, 150 + 90 * k, t, col='#8e2a6e')
    d.rounded_rectangle([s(800), s(360), s(900), s(880)], radius=s(30), outline=hexc('#ffb3e0'), width=s(8))
    h = 480 * k
    d.rounded_rectangle([s(816), s(864 - h), s(884), s(864)], radius=s(22), fill=hexc('#ff4d8a'))
    text_block(img, ["Le scénario du Big Rip : l'énergie noire devient de plus en plus forte. Et rien ne lui résiste."], t, 1080, '#ffffff', size=66)

random.seed(5)
ARMS = [(random.uniform(0, 1), random.choice((0, math.pi)), random.uniform(-0.3, 0.3)) for _ in range(90)]
def sc_galaxy(img, d, t, D):
    bg(d, '#060818'); stars(d, t)
    header(d, hexc('#c9b8ff'))
    k = ease((t - 0.8) / 2.8)
    for (u, arm, j) in ARMS:
        a = arm + u * 4.2 + t * 0.4 + j
        rr = 30 + u * 230
        rr *= 1 + 1.6 * k * (0.5 + u)
        x, y = 540 + math.cos(a) * rr, 620 + math.sin(a) * rr * 0.55
        if 300 < y < 950:
            circle(d, x, y, 7, fill=hexc('#ffe9a8', int(255 * (1 - 0.5 * k))))
    circle(d, 540, 620, 40 * (1 - 0.6 * k), fill=hexc('#fff3c4'))
    text_block(img, [("60 millions d'années avant la fin :", 0.15), ("notre galaxie est éparpillée.", 0.8)], t, 1080, '#ffffff', size=72)

def sc_solar(img, d, t, D):
    bg(d, '#2a1a05'); header(d, hexc('#ffd166'))
    circle(d, 300, 620, 110, fill=hexc('#ffb703'))
    k = ease((t - 1.0) / 2.2)
    a = t * 1.6
    R = 230 + 600 * k
    ex, ey = 300 + math.cos(a * (1 - k)) * R, 620 + math.sin(a * (1 - k)) * R * 0.45
    if k < 0.3:
        d.ellipse([s(300 - 230), s(620 - 104), s(300 + 230), s(620 + 104)], outline=hexc('#ffd166', int(150 * (1 - k / 0.3))), width=s(3))
    if ex < 1040 and 320 < ey < 940:
        circle(d, ex, ey, 34, fill=hexc('#4fa3ff'))
        circle(d, ex - 8, ey - 6, 12, fill=hexc('#6bd17a'))
    text_block(img, [("3 mois avant :", 0.15), ("la Terre se détache du Soleil et part à la dérive.", 0.8)], t, 1080, '#ffffff', size=72)

def sc_earth(img, d, t, D):
    bg(d, '#0d2b3a'); header(d, hexc('#9fe0ff'))
    k = ease((t - 1.2) / 2.0)
    shake = 8 * math.sin(t * 50) * (1 if 0.6 < t < 1.3 else 0)
    for q, (dx, dy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        ox, oy = 540 + shake + dx * 120 * k, 620 + dy * 90 * k
        st = [180, 270, 90, 0][q]
        d.pieslice([s(ox - 200), s(oy - 200), s(ox + 200), s(oy + 200)], st, st + 90, fill=hexc('#4fa3ff'))
        circle(d, ox + dx * 70, oy + dy * 70, 30, fill=hexc('#6bd17a'))
    text_block(img, [("30 minutes avant :", 0.15), ("la Terre éclate en morceaux.", 0.8)], t, 1080, '#ffffff', size=72)

def sc_atoms(img, d, t, D):
    bg(d, '#4a0a12'); header(d, hexc('#ffb3bd'))
    k = ease((t - 0.3) / 2.0)
    circle(d, 540, 620, 60, fill=hexc('#ff8a5c'))
    for i in range(3):
        rot = i * math.pi / 3
        R = 210 * (1 + 2.5 * k)
        a = t * 4 + i * 2
        x = 540 + math.cos(rot) * math.cos(a) * R - math.sin(rot) * math.sin(a) * R * 0.35
        y = 620 + math.sin(rot) * math.cos(a) * R + math.cos(rot) * math.sin(a) * R * 0.35
        if k < 0.25:
            pts = []
            for j in range(41):
                b = j / 40 * 2 * math.pi
                pts.append((540 + math.cos(rot) * math.cos(b) * 210 - math.sin(rot) * math.sin(b) * 74,
                            620 + math.sin(rot) * math.cos(b) * 210 + math.cos(rot) * math.sin(b) * 74))
            line(d, pts, hexc('#ffb3bd', int(200 * (1 - k / 0.25))), 4)
        if 320 < y < 940 and 20 < x < 1060:
            circle(d, x, y, 22, fill=hexc('#7ff0e0'))
    text_block(img, ["Un milliardième de milliardième de seconde avant : même les atomes sont déchirés.", ("Fin de tout.", 2.0)], t, 1060, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    k = 0.5 + 0.5 * math.sin(t * 2.5)
    w = 170 + 120 * k
    d.rounded_rectangle([s(540 - w), s(470), s(540 + w), s(800)], radius=s(40), fill=hexc('#8a5a3c'))
    d.rounded_rectangle([s(540 - w + 30), s(520), s(540 + w - 30), s(600)], radius=s(20), fill=hexc('#6b4029'))
    circle(d, 540 + w - 60, 680, 26, fill=hexc('#ffd166'))
    for side in (-1, 1):
        line(d, [(540 + side * (w + 20), 635), (540 + side * (w + 90), 635)], '#4a2c1d', 10)
    text_block(img, ["Être écartelé jusqu'au moindre atome…", ("…c'est à peu près ce que vit votre compte en banque le 25 du mois.", 1.6)], t, 1010, '#2b1a10', size=66)

def sc_science(img, d, t, D):
    bg(d, '#102a43'); header(d, hexc('#9fc2ff'))
    d.rounded_rectangle([s(490), s(360), s(590), s(880)], radius=s(30), outline=hexc('#9fc2ff'), width=s(8))
    k = ease((t - 0.6) / 2.0)
    h = 480 * (0.55 - 0.25 * k)
    d.rounded_rectangle([s(506), s(864 - h), s(574), s(864)], radius=s(22), fill=hexc('#7ff0e0'))
    if k > 0.3:
        line(d, [(660, 520), (660, 700)], '#7ff0e0', 14)
        line(d, [(620, 650), (660, 700), (700, 650)], '#7ff0e0', 14)
    text_block(img, ["Les mesures récentes (relevé DESI, 2024-2025) suggèrent plutôt l'inverse : l'énergie noire faiblirait.", ("À confirmer, mais mauvais signe pour le Big Rip.", 2.4)], t, 1020, '#ffffff', size=60)

def sc_delay(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.4)
    n = int(min(22, 22 * ease(t / 1.2)))
    ctext(d, str(n), 400, 240, '#a8f0c0', FBK, k)
    ctext(d, "milliards d'années", 700, 56, '#a8f0c0', FB, k)
    text_block(img, [("Et même dans le pire scénario calculé en 2003, la fin tombait dans environ 22 milliards d'années.", 0.8)], t, 1040, '#ffffff', size=62)

sc_title = scene_title(["LE BIG", "RIP"], "Scénario d'extinction n°14", color='#3b1a7a')
sc_end = scene_end("Bref : l'univers ne se déchirera pas demain. Vos impôts, eux, tomberont quand même.", color='#3b1a7a')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_expand, 4.4), (sc_accel, 4.4), (sc_stronger, 4.4),
    (sc_galaxy, 4.2), (sc_solar, 4.2), (sc_earth, 4.0), (sc_atoms, 4.4),
    (sc_joke, 4.6), (sc_science, 5.4), (sc_delay, 4.2), (sc_end, 4.8),
]
