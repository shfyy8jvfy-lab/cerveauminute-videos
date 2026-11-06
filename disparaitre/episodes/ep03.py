"""Épisode 3 — L'astéroïde tueur (et la mission DART).
Sources : NASA (communiqué 11/10/2022 : DART a raccourci l'orbite de Dimorphos de 32 min, 11 h 55 → 11 h 23) ;
Space.com, ScienceDaily (oct. 2022) ; NASA/JPL CNEOS (plus de 90 % des géocroiseurs > 1 km repérés,
aucun ne menace la Terre au cours du prochain siècle) ; Sky at Night Magazine, Phys.org (Chicxulub, ~10 km, il y a 66 Ma,
environ 3 espèces sur 4 disparues).
"""
from engine import *

EPISODE = 3
BOOM_SCENE = 5
LEGENDE = """Épisode 3 : l'astéroïde tueur ☄️🦖

Il y a 66 millions d'années, un caillou d'environ 10 km a mis fin au règne des dinosaures. Bonne nouvelle : en 2022, la sonde DART de la NASA a foncé exprès dans l'astéroïde Dimorphos et a raccourci son orbite de 32 minutes. Et aucun gros astéroïde connu ne menace la Terre pour les 100 prochaines années.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #astéroïde #espace #nasa #dinosaures #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
ROCK = [(1.00, 0.0), (0.85, 0.7), (0.95, 1.4), (0.80, 2.1), (1.05, 2.8), (0.9, 3.5), (1.0, 4.2), (0.82, 4.9), (0.95, 5.6)]
def rock(d, cx, cy, r, col='#8c8a96', rot=0.0, a=255):
    pts = [(cx + r * k * math.cos(ang + rot), cy + r * k * math.sin(ang + rot)) for k, ang in ROCK]
    d.polygon([(s(x), s(y)) for x, y in pts], fill=hexc(col, a))
    for (dx, dy, rr) in ((-0.3, -0.2, 0.18), (0.35, 0.25, 0.14), (0.05, 0.45, 0.1)):
        ox = dx * math.cos(rot) - dy * math.sin(rot); oy = dx * math.sin(rot) + dy * math.cos(rot)
        circle(d, cx + ox * r, cy + oy * r, rr * r, fill=hexc('#000000', int(a * 0.25)))

def earth(d, cx, cy, r, t=0, a=255):
    circle(d, cx, cy, r, fill=hexc('#2f7fd6', a))
    for (ox, oy, rr) in ((-0.35, -0.25, 0.32), (0.3, 0.2, 0.28), (0.1, -0.5, 0.18)):
        x = cx + (ox + 0.05 * math.sin(t)) * r
        circle(d, x, cy + oy * r, rr * r, fill=hexc('#49b36b', a))

def trail(d, x, y, dx, dy, n=6, col='#ffb347'):
    for i in range(1, n + 1):
        circle(d, x - dx * i * 18, y - dy * i * 18, max(3, 26 - i * 4), fill=hexc(col, int(200 - i * 30)))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b0f24'); stars(d, t); header(d, hexc('#ffb347'))
    k = ease(t / 2.8)
    x, y = 860 - 420 * k, 360 + 360 * k
    trail(d, x, y, -0.76, 0.65)
    rock(d, x, y, 60, rot=t * 2)
    text_block(img, ["Et si la fin du monde… nous tombait littéralement sur la tête ?"], t, 1090, '#ffffff', size=80)

def sc_dinos(img, d, t, D):
    bg(d, '#1d3a2a'); header(d, hexc('#b6f0c8'))
    earth(d, 600, 700, 220, t)
    k = ease((t - 0.2) / 2.6)
    x, y = 180 + 220 * k, 380 + 150 * k
    trail(d, x, y, 0.82, 0.56)
    rock(d, x, y, 45, rot=t * 2)
    text_block(img, ["Il y a 66 millions d'années, un caillou d'environ 10 km a frappé l'actuel Mexique."], t, 1060, '#ffffff', size=68)

def sc_species(img, d, t, D):
    bg(d, '#4a2a12'); header(d, hexc('#ffd9a8'))
    for i in range(4):
        x = 225 + i * 210; y = 640 + 8 * math.sin(t * 4 + i)
        circle(d, x, y, 80, fill=hexc('#f2a65a'))
        circle(d, x + 28, y - 20, 12, fill=hexc('#3a1e08'))
        if i < 3:
            kk = ease((t - 0.8 - i * 0.45) / 0.3)
            if kk > 0:
                line(d, [(x - 95, y - 95), (x - 95 + 190 * kk, y - 95 + 190 * kk)], '#ff4d5a', 16)
    text_block(img, ["Bilan : fin des dinosaures. Environ 3 espèces sur 4 ont disparu."], t, 1060, '#ffffff', size=72)

random.seed(3)
NEO = [(random.uniform(0, 6.28), random.uniform(0.25, 0.6), random.uniform(250, 380)) for _ in range(26)]
def sc_many(img, d, t, D):
    bg(d, '#14143a'); stars(d, t); header(d, hexc('#c8c8ff'))
    circle(d, 540, 640, 60, fill=hexc('#ffcf4a'))
    d.ellipse([s(540 - 220), s(640 - 220), s(540 + 220), s(640 + 220)], outline=hexc('#5a6aff', 140), width=s(4))
    ea = t * 0.9
    earth(d, 540 + 220 * math.cos(ea), 640 + 220 * math.sin(ea), 26)
    for i, (ph, sp, rr) in enumerate(NEO):
        if t > 0.3 + i * 0.07:
            a = ph + t * sp
            rock(d, 540 + rr * math.cos(a), 640 + rr * 0.85 * math.sin(a), 11, rot=a)
    text_block(img, ["Et il en reste plein : des milliers de cailloux croisent la route de la Terre."], t, 1060, '#ffffff', size=68)

def sc_boom(img, d, t, D):
    dark = ease((t - 0.6) / 2.0)
    base = (int(120 - 90 * dark), int(30 + 0 * dark), int(20 + 10 * dark))
    d.rectangle([0, 0, s(W), s(H)], fill=base + (255,))
    header(d, hexc('#ffc2a8'))
    earth(d, 540, 680, 230)
    fl = max(0, 1 - t / 0.6)
    if fl > 0:
        circle(d, 470, 560, 120 + 300 * (1 - fl), fill=hexc('#fff3c4', int(255 * fl)))
    for i in range(18):
        ang = i * 0.35 + t * 0.4
        r = 120 + 140 * dark
        circle(d, 540 + r * math.cos(ang), 680 + r * 0.8 * math.sin(ang), 70 + 30 * dark, fill=hexc('#3b302c', int(200 * dark)))
    text_block(img, ["Un tel impact, c'est de la poussière partout, le Soleil caché… et plus aucune récolte."], t, 1060, '#ffffff', size=68)

def sc_joke(img, d, t, D):
    bg(d, '#f6e7c8'); header(d, hexc('#8a5a3c'))
    y = 380 + 300 * ease(t / 2.5) + 10 * math.sin(t * 3)
    d.pieslice([s(380), s(y - 170), s(700), s(y + 150)], 180, 360, fill=hexc('#ff7a59'))
    for x0 in (395, 540, 685):
        line(d, [(x0, y - 10), (540, y + 140)], '#8a5a3c', 5)
    d.rounded_rectangle([s(470), s(y + 130), s(610), s(y + 250)], radius=s(12), fill=hexc('#c98b4f'))
    line(d, [(470, y + 175), (610, y + 175)], '#8a5a3c', 8)
    text_block(img, ["Pour l'instant, la seule chose qu'on attend vraiment du ciel…",
                     ("…c'est le colis « livré entre 8 h et 18 h ».", 1.7)], t, 1040, '#2b1a10', size=66)

def sc_dart(img, d, t, D):
    bg(d, '#0a2a3a'); stars(d, t); header(d, hexc('#9fe3ff'))
    rock(d, 640, 640, 130, rot=0.3)
    k = ease(t / 1.6)
    px, py = 80 + 450 * k, 400 + 180 * k
    if t < 1.6:
        d.rectangle([s(px - 22), s(py - 16), s(px + 22), s(py + 16)], fill=hexc('#ffffff'))
        line(d, [(px - 70, py), (px - 22, py)], '#9fe3ff', 12)
        line(d, [(px + 22, py), (px + 70, py)], '#9fe3ff', 12)
    else:
        fl = ease((t - 1.6) / 0.6)
        for i in range(12):
            a = i * 0.52
            circle(d, 530 + 120 * fl * math.cos(a), 580 + 120 * fl * math.sin(a), 14 * (1 - fl * 0.5), fill=hexc('#ffd27a', int(255 * (1 - fl * 0.6))))
    text_block(img, ["Bonne nouvelle : en 2022, la NASA a foncé exprès dans un astéroïde avec une sonde."], t, 1060, '#ffffff', size=68)

def sc_32(img, d, t, D):
    bg(d, '#2a1a4a'); header(d, hexc('#d9c2ff'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "11 h 55", 420, 90, '#9a88c0', FB, k)
    if k > 0:
        w = font(FB, 90).getlength("11 h 55") / S
        kk = ease((t - 0.8) / 0.3)
        line(d, [(540 - w / 2 - 15, 470), (540 - w / 2 - 15 + (w + 30) * kk, 470)], '#ff4d5a', 10)
    ctext(d, "11 h 23", 600, 150, '#ffffff', FBK, ease((t - 1.0) / 0.4))
    ctext(d, "– 32 minutes par tour", 820, 48, '#d9c2ff', FM, ease((t - 1.3) / 0.4))
    text_block(img, [("Mission DART : le petit astéroïde tourne désormais plus vite autour du grand. Ça marche !", 0.4)], t, 1050, '#ffffff', size=64)

def sc_90(img, d, t, D):
    bg(d, '#103a30'); header(d, hexc('#a8f0d0'))
    k = ease((t - 0.2) / 0.4)
    n = int(min(90, 90 * ease(t / 1.2)))
    ctext(d, f"{n} %", 500, 220, '#a8f0d0', FBK, k)
    ctext(d, "des géocroiseurs de plus de 1 km", 760, 44, '#a8f0d0', FM, k)
    text_block(img, [("Plus de 90 % des gros astéroïdes proches de nous (les géocroiseurs) sont déjà repérés.", 0.8)], t, 1040, '#ffffff', size=64)

def sc_100(img, d, t, D):
    bg(d, '#000000'); stars(d, t); header(d, hexc('#9a9aa8'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "100 ANS", 520, 170, '#ffd27a', FBK, k)
    ctext(d, "sans menace connue", 730, 46, '#9a9aa8', FM, k)
    text_block(img, [("Et aucun d'eux ne menace la Terre au cours du prochain siècle.", 0.8)], t, 1060, '#ffffff', size=72)

def sc_rare(img, d, t, D):
    bg(d, '#3a0f2e'); header(d, hexc('#ffb8e0'))
    for i in range(10):
        x = 120 + i * 93
        kk = ease((t - 0.2 - i * 0.12) / 0.3)
        d.rounded_rectangle([s(x - 30), s(700 - 220 * kk), s(x + 30), s(700)], radius=s(12), fill=hexc('#ffb8e0', 120))
    rock(d, 120 + 9 * 93, 440 + 6 * math.sin(t * 4), 40, col='#ff6fb5', rot=t)
    ctext(d, "1 fois / 100 millions d'années", 800, 50, '#ffb8e0', FB, ease((t - 1.0) / 0.4))
    text_block(img, [("Un géant comme celui des dinosaures, c'est en gros une fois tous les 100 millions d'années.", 0.6)], t, 1040, '#ffffff', size=64)

sc_title = scene_title(["ASTÉROÏDE", "TUEUR"], "Scénario d'extinction n°3")
sc_end = scene_end("Bref : pas besoin de sortir avec un casque. Les impôts, eux, tombent quand même chaque année.")

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_dinos, 4.2), (sc_species, 4.0), (sc_many, 4.2),
    (sc_boom, 4.0), (sc_joke, 4.4), (sc_dart, 4.2), (sc_32, 4.2),
    (sc_90, 4.4), (sc_100, 4.0), (sc_rare, 4.2), (sc_end, 4.8),
]
