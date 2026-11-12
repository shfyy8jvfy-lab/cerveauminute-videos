"""Épisode 22 — Un trou noir errant qui passe près de nous.
Sources :
- NASA / Hubble, communiqué du 10 juin 2022 « Hubble Determines Mass of Isolated Black Hole Roaming Our Milky Way
  Galaxy » : premier trou noir isolé détecté (OGLE-2011-BLG-0462) par microlentille gravitationnelle, environ 7 fois
  la masse du Soleil, à environ 5 000 années-lumière, vitesse ≈ 160 000 km/h ; on estime qu'environ 100 millions de
  trous noirs isolés errent dans la Voie lactée.
- Sahu et al., ApJ 933, 83 (2022) ; confirmation Sahu et al. 2025 (arXiv:2503.07820) : trou noir isolé de ~7 masses
  solaires confirmé avec de nouvelles données Hubble.
- Live Science, « Rogue black hole spotted on its own for the first time » ; Sci.News.
- MPIA / Max Planck (nov. 2022) et ESA : Gaia BH1, trou noir le plus proche connu, ≈ 1 560 années-lumière.
- Calcul : 5 000 années-lumière ≈ 4,7e16 km ; à 45 km/s → ≈ 33 millions d'années de trajet.
- Consensus : un passage assez proche pour perturber les orbites est extrêmement improbable (densité très faible
  des trous noirs dans le voisinage solaire) ; c'est un scénario possible en théorie, pas une menace connue.
"""
from engine import *

EPISODE = 22
BOOM_SCENE = 8
LEGENDE = """Épisode 22 : et si un trou noir invisible traversait le système solaire ? 🕳️🌍

En 2022, le télescope Hubble a repéré pour la première fois un trou noir qui voyage seul : environ 7 fois la masse du Soleil, à 5 000 années-lumière (NASA). Les astronomes estiment qu'il y en aurait environ 100 millions dans notre galaxie. Mais le plus proche connu est à 1 560 années-lumière : l'espace est vraiment, vraiment vide.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #trounoir #espace #astronomie #hubble #science #vulgarisation"""

# ---------- fil rouge : le trou noir (disque noir + anneau de lumière déviée) ----------
def black_hole(d, cx, cy, r, t, ring='#c77dff', alpha=255):
    for k in range(5, 0, -1):
        rr = r * (1 + 0.16 * k + 0.03 * math.sin(t * 3 + k))
        circle(d, cx, cy, rr, fill=hexc(ring, int(alpha * 0.10 * (6 - k) / 5)))
    circle(d, cx, cy, r * 1.12, outline=hexc('#ffffff', int(alpha * 0.85)), width=max(3, r * 0.05))
    circle(d, cx, cy, r, fill=hexc('#000000', alpha))

def earth(d, cx, cy, r, alpha=255):
    circle(d, cx, cy, r, fill=hexc('#4895ef', alpha))
    circle(d, cx - r * 0.3, cy - r * 0.2, r * 0.4, fill=hexc('#52b788', alpha))
    circle(d, cx + r * 0.35, cy + r * 0.3, r * 0.28, fill=hexc('#52b788', alpha))

def sun(d, cx, cy, r, t):
    circle(d, cx, cy, r * (1.25 + 0.05 * math.sin(t * 4)), fill=hexc('#ffd166', 90))
    circle(d, cx, cy, r, fill=hexc('#ffb703'))

def label(d, txt, x, y, col, size=40):
    d.text((s(x), s(y)), txt, font=font(FB, size), fill=hexc(col), anchor='mm')

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#10002b'); header(d, hexc('#e0aaff')); stars(d, t)
    x = 1000 - 460 * ease(t / D)
    black_hole(d, x, 600, 130, t)
    text_block(img, ["Et si un monstre invisible traversait le système solaire ?"], t, 1080, '#ffffff', size=78)

def sc_what(img, d, t, D):
    bg(d, '#14213d'); header(d, hexc('#a2d2ff'))
    black_hole(d, 540, 600, 170, t)
    for i in range(6):  # rayons de lumière aspirés
        a = i * math.pi / 3 + t * 0.6
        ph = (t * 0.8 + i * 0.17) % 1
        r0 = 420 - 200 * ph
        x0, y0 = 540 + r0 * math.cos(a), 600 + r0 * math.sin(a) * 0.75
        x1, y1 = 540 + (r0 - 60) * math.cos(a), 600 + (r0 - 60) * math.sin(a) * 0.75
        line(d, [(x0, y0), (x1, y1)], hexc('#ffd166', int(255 * (1 - ph))), 10)
    text_block(img, ["Un trou noir : tellement de masse au même endroit que même la lumière ne peut pas s'en échapper."], t, 1060, '#ffffff', size=62)

def sc_count(img, d, t, D):
    bg(d, '#3c096c'); header(d, hexc('#e0aaff'))
    # galaxie : spirale de points
    for i in range(120):
        a = i * 0.35 + t * 0.2
        r = 20 + i * 2.6
        circle(d, 540 + r * math.cos(a), 600 + r * math.sin(a) * 0.55, 4, fill=hexc('#ffffff', 170))
    n = int(1 + 9 * ease((t - 0.5) / 2))
    for i in range(n):
        a = i * 2.4 + t * 0.2
        r = 60 + i * 30
        black_hole(d, 540 + r * math.cos(a), 600 + r * math.sin(a) * 0.55, 18, t, alpha=255)
    text_block(img, ["Certains voyagent seuls dans la galaxie.", ("On estime qu'il y en a environ 100 millions.", 1.4)], t, 1060, '#ffffff', size=66)

def sc_hubble(img, d, t, D):
    bg(d, '#023e8a'); header(d, hexc('#90e0ef')); stars(d, t)
    # télescope (rectangles) qui vise
    d.rounded_rectangle([s(130), s(700), s(400), s(800)], radius=s(20), fill=hexc('#ced4da'))
    d.rectangle([s(400), s(720), s(440), s(780)], fill=hexc('#adb5bd'))
    d.rectangle([s(180), s(620), s(350), s(690)], fill=hexc('#ffd166'))
    k = ease((t - 0.4) / 1.0)
    line(d, [(440, 750), (440 + 300 * k, 750 - 260 * k)], hexc('#90e0ef', 200), 6)
    black_hole(d, 780, 450, 80, t)
    label(d, "x7 SOLEIL", 780, 660, '#ffd166', 46)
    text_block(img, ["En 2022, Hubble en repère un pour la première fois : sept fois la masse du Soleil, à 5 000 années-lumière."], t, 1060, '#ffffff', size=60)

def sc_lens(img, d, t, D):
    bg(d, '#2b2d42'); header(d, hexc('#edf2f4'))
    # étoile derrière qui s'éclaire quand le trou noir passe devant
    bx = 240 + 600 * (t / D)
    dist = abs(bx - 540)
    glow = max(0, 1 - dist / 260)
    circle(d, 540, 600, 40 + 70 * glow, fill=hexc('#fff3b0', int(120 + 135 * glow)))
    circle(d, 540, 600, 30, fill=hexc('#ffffff'))
    black_hole(d, bx, 640, 70, t, alpha=230)
    text_block(img, ["Problème : il ne brille pas.", ("On le repère seulement quand il déforme la lumière des étoiles (microlentille).", 1.3)], t, 1060, '#ffffff', size=62)

def sc_speed(img, d, t, D):
    bg(d, '#006d77'); header(d, hexc('#83c5bc'))
    x = 200 + 700 * ((t * 0.35) % 1)
    for i in range(5):
        line(d, [(x - 120 - i * 40, 560 + i * 20), (x - 220 - i * 60, 560 + i * 20)], hexc('#83c5bc', 200 - i * 35), 8)
    black_hole(d, x, 600, 80, t)
    label(d, "160 000 KM/H", 540, 820, '#ffffff', 56)
    text_block(img, ["Il file à 160 000 km/h. Même lancé droit sur nous, il mettrait plus de 30 millions d'années à arriver."], t, 1060, '#ffffff', size=60)

def sc_pull(img, d, t, D):
    bg(d, '#540b0e'); header(d, hexc('#ffb4a2'))
    sun(d, 400, 620, 60, t)
    k = ease(t / D)
    for i, (r, col) in enumerate([(130, '#e5e5e5'), (200, '#4895ef'), (270, '#e76f51')]):
        a = t * (1.2 - i * 0.3) + i
        px = 400 + r * math.cos(a) + 60 * k * (i + 1) / 3
        py = 620 + r * math.sin(a) * 0.6
        d.ellipse([s(400 - r), s(620 - r * 0.6), s(400 + r), s(620 + r * 0.6)], outline=hexc('#ffffff', 60), width=s(2))
        if col == '#4895ef':
            earth(d, px, py, 20)
        else:
            circle(d, px, py, 14, fill=hexc(col))
    black_hole(d, 900 - 60 * k, 480, 70, t)
    text_block(img, ["S'il passait près de chez nous, sa gravité tirerait sur toutes les planètes."], t, 1060, '#ffffff', size=64)

def sc_boom(img, d, t, D):
    bg(d, '#000000'); header(d, hexc('#777777')); stars(d, t)
    black_hole(d, 700, 560, 150, t)
    k = ease(t / 2.0)
    a = k * 5
    r = 380 * (1 - 0.6 * k)
    ex, ey = 700 + r * math.cos(a + 2.5), 560 + r * math.sin(a + 2.5) * 0.7
    earth(d, ex, ey, 40 * (1 - 0.7 * k) + 4, alpha=int(255 * (1 - 0.6 * k)))
    text_block(img, ["La Terre serait éjectée de son orbite… ou avalée.", ("Bonsoir.", 1.8)], t, 1080, '#ffffff', size=76)

def sc_socks(img, d, t, D):
    bg(d, '#f4a261'); header(d, hexc('#fff1e6'))
    black_hole(d, 540, 600, 120, t, ring='#ffffff')
    for i in range(4):
        a = i * math.pi / 2 + t * 1.5
        r = 300 - 120 * ((t * 0.5 + i * 0.25) % 1)
        x, y = 540 + r * math.cos(a), 600 + r * math.sin(a) * 0.8
        col = ['#e63946', '#457b9d', '#2a9d8f', '#ffffff'][i]
        d.rounded_rectangle([s(x - 18), s(y - 50), s(x + 18), s(y + 20)], radius=s(12), fill=hexc(col))
        d.rounded_rectangle([s(x - 18), s(y + 5), s(x + 40), s(y + 35)], radius=s(14), fill=hexc(col))
    text_block(img, ["Point positif : on saurait enfin où partent les chaussettes perdues."], t, 1060, '#ffffff', size=68)

def sc_nearest(img, d, t, D):
    bg(d, '#283618'); header(d, hexc('#dde5b6'))
    earth(d, 150, 620, 40)
    k = ease((t - 0.3) / 1.6)
    line(d, [(200, 620), (200 + 560 * k, 620)], hexc('#dde5b6', 200), 6)
    black_hole(d, 880, 620, 70, t)
    label(d, "1 560 ANNÉES-LUMIÈRE", 520, 520, '#ffffff', 46)
    text_block(img, ["Le plus proche qu'on connaisse (Gaia BH1) est à 1 560 années-lumière.", ("Très, très loin.", 1.6)], t, 1060, '#ffffff', size=62)

def sc_science(img, d, t, D):
    bg(d, '#1b4332'); header(d, hexc('#b7e4c7'))
    stars(d, t)
    earth(d, 380, 600, 50)
    black_hole(d, 760, 560, 40, t)
    k = ease((t - 1.0) / 0.4)
    d.rounded_rectangle([s(300), s(760), s(780), s(850)], radius=s(24), fill=hexc('#40916c', int(255 * k)))
    if k > 0.5:
        label(d, "RISQUE : QUASI NUL", 540, 805, '#ffffff', 44)
    text_block(img, ["Ce que disent les scientifiques : l'espace est immense et presque vide.", ("Le risque d'un tel passage : quasi nul.", 1.7)], t, 1060, '#ffffff', size=62)

sc_title = scene_title(["TROU NOIR", "ERRANT"], "Scénario d'extinction n°22", color='#5a189a')
sc_end = scene_end("Bref : même un trou noir ne pourra pas avaler votre feuille d'impôts.", color='#5a189a')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_what, 4.6), (sc_count, 4.2), (sc_hubble, 4.6),
    (sc_lens, 4.6), (sc_speed, 4.6), (sc_pull, 4.0), (sc_boom, 3.6), (sc_socks, 4.0),
    (sc_nearest, 4.2), (sc_science, 4.4), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Et si un monstre invisible traversait le système solaire ?",
    "Scénario d'extinction numéro vingt-deux : le trou noir errant.",
    "Un trou noir : tellement de masse au même endroit que même la lumière ne peut pas s'en échapper.",
    "Certains voyagent seuls dans la galaxie. On estime qu'il y en a environ cent millions.",
    "En deux mille vingt-deux, Hubble en repère un pour la première fois : sept fois la masse du Soleil, à cinq mille années-lumière.",
    "Problème : il ne brille pas. On le repère seulement quand il déforme la lumière des étoiles.",
    "Il file à cent soixante mille kilomètres heure. Même lancé droit sur nous, il mettrait plus de trente millions d'années à arriver.",
    "S'il passait près de chez nous, sa gravité tirerait sur toutes les planètes.",
    "La Terre serait éjectée de son orbite… ou avalée. Bonsoir.",
    "Point positif : on saurait enfin où partent les chaussettes perdues.",
    "Le plus proche qu'on connaisse est à mille cinq cent soixante années-lumière. Très, très loin.",
    "Ce que disent les scientifiques : l'espace est immense et presque vide. Le risque d'un tel passage : quasi nul.",
    "Bref : même un trou noir ne pourra pas avaler votre feuille d'impôts. Abonnez-vous. Tant qu'il y a un demain.",
]
