"""Épisode 15 — Une planète errante qui traverse le système solaire.
Sources :
- Sumi et al. & Koshimoto et al., The Astronomical Journal (2023), relevé MOA (microlentilles, 9 ans) :
  environ 20 fois plus de planètes errantes que d'étoiles dans la Voie lactée (communiqué NASA Goddard, juil. 2023 ;
  Universe Today ; Earth.com ; Phys.org).
- Détection par microlentille gravitationnelle : la gravité de la planète amplifie un instant la lumière d'une
  étoile lointaine (NASA ; Universe Today).
- Raymond et al., MNRAS (2023), « Future Trajectories of the Solar System » : 12 000 simulations d'une étoile
  passant à moins de 100 ua du Soleil ; plus de 95 % de chances qu'aucune planète ne soit perdue ; ce genre de
  passage arrive environ une fois tous les 100 milliards d'années ; la Terre peut, rarement, tomber sur le Soleil,
  heurter une planète ou être éjectée (ScienceAlert / Universe Today, nov. 2023).
- Étude Icarus (2025) : les passages d'étoiles rendent le système solaire moins stable que prévu, mais
  les risques pour la Terre restent faibles sur 5 milliards d'années (Gizmodo, mai 2025).
- Une planète est bien plus légère qu'une étoile : elle devrait passer encore plus près pour perturber les orbites.
"""
from engine import *

EPISODE = 15
BOOM_SCENE = 7
LEGENDE = """Épisode 15 : la planète errante qui traverse le système solaire 🪐🌑

Il existerait environ 20 fois plus de planètes « errantes », sans étoile, que d'étoiles dans notre galaxie (études 2023, relevé MOA / NASA). Si l'une d'elles passait tout près, elle pourrait dérégler l'orbite de la Terre. Bonne nouvelle : même pour une étoile, un passage aussi proche n'arrive qu'environ une fois tous les 100 milliards d'années, et dans plus de 95 % des simulations, toutes les planètes s'en sortent.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #espace #astronomie #planete #systemesolaire #science #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def rogue(d, cx, cy, r, glow=0.0):
    """Fil rouge : la planète errante, sombre et violacée, avec un liseré."""
    if glow > 0:
        circle(d, cx, cy, r * 1.25, fill=hexc('#b48cff', int(60 * glow)))
    circle(d, cx, cy, r, fill=hexc('#3b2a5c'))
    circle(d, cx + r * 0.15, cy + r * 0.1, r * 0.82, fill=hexc('#2a1d45'))
    d.arc([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], 200, 320, fill=hexc('#b48cff'), width=s(max(4, r * 0.06)))
    for (dx, dy, rr) in ((-0.3, 0.25, 0.14), (0.35, -0.2, 0.1), (0.1, 0.45, 0.08)):
        circle(d, cx + dx * r, cy + dy * r, rr * r, fill=hexc('#1f1535'))

def earth(d, cx, cy, r, frost=0.0):
    circle(d, cx, cy, r, fill=hexc('#4fa3ff'))
    circle(d, cx - r * 0.3, cy - r * 0.2, r * 0.35, fill=hexc('#6bd17a'))
    circle(d, cx + r * 0.35, cy + r * 0.3, r * 0.25, fill=hexc('#6bd17a'))
    if frost > 0:
        circle(d, cx, cy, r, fill=hexc('#e8f6ff', int(235 * frost)))

def sun(d, cx, cy, r, t):
    for i in range(12):
        a = i * math.pi / 6 + t * 0.5
        line(d, [(cx + math.cos(a) * r * 1.2, cy + math.sin(a) * r * 1.2), (cx + math.cos(a) * r * 1.5, cy + math.sin(a) * r * 1.5)], '#ffd166', 8)
    circle(d, cx, cy, r, fill=hexc('#ffb703'))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0a0716'); stars(d, t); header(d, hexc('#b48cff'))
    x = 1180 - 640 * ease(t / 2.6)
    rogue(d, x, 620, 160)
    text_block(img, ["Et si une planète sans soleil fonçait droit sur nous ?"], t, 1090, '#ffffff', size=80)

def sc_alone(img, d, t, D):
    bg(d, '#1b1440'); header(d, hexc('#c9b8ff'))
    sun(d, 260, 620, 80, t)
    k = ease((t - 1.0) / 2.6)
    a = t * 2.2
    if k < 0.05:
        x, y = 260 + math.cos(a) * 220, 620 + math.sin(a) * 120
    else:
        x0, y0 = 260 + math.cos(1.0 * 2.2) * 220, 620 + math.sin(1.0 * 2.2) * 120
        x, y = x0 + 700 * k, y0 - 150 * k
    d.ellipse([s(40), s(500), s(480), s(740)], outline=hexc('#c9b8ff', int(120 * (1 - k))), width=s(3))
    rogue(d, x, y, 60)
    text_block(img, ["Certaines planètes ont été éjectées de leur système. Elles dérivent seules, dans le noir."], t, 1080, '#ffffff', size=66)

def sc_lens(img, d, t, D):
    bg(d, '#0d1b2e'); stars(d, t); header(d, hexc('#9fc2ff'))
    x = 120 + 840 * (t / D)
    close = max(0, 1 - abs(x - 540) / 260)
    circle(d, 540, 560, 30 + 50 * close, fill=hexc('#ffffff', int(120 + 135 * close)))
    circle(d, 540, 560, 18, fill=hexc('#ffffff'))
    rogue(d, x, 780, 70)
    text_block(img, ["On les repère quand elles passent devant une étoile lointaine : celle-ci brille plus fort un instant (microlentille)."], t, 1060, '#ffffff', size=62)

def sc_count(img, d, t, D):
    bg(d, '#2a1040'); header(d, hexc('#f0b8ff'))
    k = ease((t - 0.2) / 0.4)
    n = int(min(20, 20 * ease(t / 1.2)))
    ctext(d, f"×{n}", 470, 230, '#f0b8ff', FBK, k)
    ctext(d, "plus de planètes errantes que d'étoiles", 720, 44, '#f0b8ff', FM, k)
    text_block(img, [("Selon des études de 2023, notre galaxie en compterait des milliers de milliards.", 0.8)], t, 1060, '#ffffff', size=68)

def solar_system(d, t, wobble=0.0):
    cx, cy = 540, 640
    sun(d, cx, cy, 55, t)
    for i, (R, col, sp) in enumerate(((140, '#c0c0c0', 3), (230, '#4fa3ff', 2), (320, '#ff7f50', 1.4))):
        d.ellipse([s(cx - R), s(cy - R * 0.5), s(cx + R), s(cy + R * 0.5)], outline=hexc('#ffffff', 70), width=s(3))
        a = t * sp + i
        j = wobble * 40 * math.sin(t * 7 + i)
        circle(d, cx + math.cos(a) * (R + j), cy + math.sin(a) * (R + j) * 0.5, 18 + 4 * i, fill=hexc(col))

def sc_cross(img, d, t, D):
    bg(d, '#102a43'); header(d, hexc('#9fe0ff'))
    k = t / D
    w = max(0, 1 - abs(k - 0.55) * 3)
    solar_system(d, t, wobble=w)
    rogue(d, 1100 - 1160 * k, 360 + 300 * k, 70, glow=w)
    text_block(img, ["Si l'une d'elles traversait le système solaire, sa gravité pourrait dérégler les orbites."], t, 1080, '#ffffff', size=66)

def sc_push(img, d, t, D):
    bg(d, '#3a1a08'); header(d, hexc('#ffd166'))
    sun(d, 300, 620, 90, t)
    k = ease((t - 0.8) / 2.6)
    ex, ey = 520 + 480 * k, 620 - 200 * k
    pts = [(520 + 480 * ease((u / 20) * 1.0) * k, 620 - 200 * ease((u / 20)) * k) for u in range(21)]
    if k > 0.02:
        line(d, pts, hexc('#ffd166', 120), 4)
    earth(d, ex, ey, 40, frost=0)
    text_block(img, ["La Terre pourrait être poussée vers le Soleil… ou éjectée loin, dans le froid."], t, 1080, '#ffffff', size=68)

random.seed(15)
CRACKS = [(random.uniform(0, 2 * math.pi), random.uniform(0.4, 1.0)) for _ in range(14)]
def sc_freeze(img, d, t, D):
    bg(d, '#061a2a'); stars(d, t); header(d, hexc('#cfefff'))
    k = ease((t - 0.4) / 2.6)
    shake = 6 * math.sin(t * 40) * (1 if 0.2 < t < 0.8 else 0)
    earth(d, 540 + shake, 620, 230, frost=k)
    if k > 0.4:
        for (a, l) in CRACKS:
            line(d, [(540 + math.cos(a) * 60, 620 + math.sin(a) * 60), (540 + math.cos(a) * 225 * l, 620 + math.sin(a) * 225 * l)], hexc('#9fd8ff', int(255 * (k - 0.4) / 0.6)), 5)
    text_block(img, ["Loin du Soleil, la surface gèle et le jour ne se lève plus.", ("Fin de la partie.", 2.2)], t, 1080, '#ffffff', size=72)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    d.rounded_rectangle([s(360), s(360), s(720), s(900)], radius=s(20), outline=hexc('#8a5a3c'), width=s(14))
    circle(d, 680, 640, 16, fill=hexc('#8a5a3c'))
    bx = 540 + 120 * math.sin(t * 1.6)
    d.polygon([(s(bx), s(900)), (s(bx - 120), s(420)), (s(bx + 120), s(420))], fill=hexc('#ffd166', 140))
    d.rounded_rectangle([s(bx - 30), s(880), s(bx + 30), s(940)], radius=s(10), fill=hexc('#4a2c1d'))
    text_block(img, ["Errer seul dans le noir, sans savoir où l'on va…", ("…c'est vous à 3 h du matin, en cherchant les toilettes sans allumer.", 1.6)], t, 1010, '#2b1a10', size=64)

def sc_light(img, d, t, D):
    bg(d, '#1d3a2a'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.3) / 1.2)
    sun(d, 330, 600, 110 + 10 * math.sin(t * 2), t)
    rogue(d, 790, 640, 60 * (1 - 0.4 * k))
    d.text((s(330), s(820)), "étoile", font=font(FB, 44), fill=hexc('#a8f0c0', int(255 * k)), anchor='mm')
    d.text((s(790), s(820)), "planète", font=font(FB, 44), fill=hexc('#a8f0c0', int(255 * k)), anchor='mm')
    text_block(img, ["Bonne nouvelle : une planète est bien plus légère qu'une étoile. Il faudrait qu'elle passe vraiment tout près."], t, 1060, '#ffffff', size=62)

def sc_rare(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.4)
    n = int(min(100, 100 * ease(t / 1.2)))
    ctext(d, str(n), 410, 240, '#a8f0c0', FBK, k)
    ctext(d, "milliards d'années", 700, 56, '#a8f0c0', FB, k)
    text_block(img, [("Même pour une étoile, un passage aussi proche n'arrive qu'environ une fois tous les 100 milliards d'années (étude 2023).", 0.8)], t, 1020, '#ffffff', size=60)

def sc_survive(img, d, t, D):
    bg(d, '#0b2545'); header(d, hexc('#9fc2ff'))
    k = ease((t - 0.2) / 0.4)
    n = int(min(95, 95 * ease(t / 1.2)))
    ctext(d, f"{n} %", 470, 220, '#7ff0e0', FBK, k)
    ctext(d, "des simulations : aucune planète perdue", 720, 44, '#9fc2ff', FM, k)
    text_block(img, [("Et même dans ce cas rarissime, toutes les planètes s'en sortent dans plus de 95 % des simulations.", 0.8)], t, 1040, '#ffffff', size=62)

sc_title = scene_title(["PLANÈTE", "ERRANTE"], "Scénario d'extinction n°15", color='#3b2a5c')
sc_end = scene_end("Bref : aucune planète ne vient nous percuter. Les impôts, eux, arrivent toujours pile à l'heure.", color='#3b2a5c')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_alone, 4.4), (sc_lens, 4.6), (sc_count, 4.2),
    (sc_cross, 4.4), (sc_push, 4.0), (sc_freeze, 4.2),
    (sc_joke, 4.6), (sc_light, 4.8), (sc_rare, 5.2), (sc_survive, 4.6), (sc_end, 4.8),
]
