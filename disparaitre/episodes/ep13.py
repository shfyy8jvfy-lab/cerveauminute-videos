"""Épisode 13 — La pandémie de laboratoire.
Sources :
- Laboratoires de sécurité maximale : Global BioLabs Report 2023 (King's College London / George Mason Univ.),
  repris par Medical Xpress et KCL News (mars 2023) : 69 laboratoires BSL-4 dans 27 pays, et la régulation
  de la biosécurité ne suit pas ce boom.
- Variole, Birmingham 1978 : Janet Parker, photographe médicale de l'université, contaminée par un virus
  venu d'un labo de l'étage inférieur ; dernière personne morte de la variole (Wikipedia « 1978 smallpox
  outbreak in the United Kingdom », WHYY, NZ Herald).
- « Gain de fonction » : expériences rendant un virus plus transmissible (ex. grippe H5N1 chez le furet, 2011-2012).
- Risque : Toby Ord (Oxford), The Precipice (2020), estime à ~1 sur 30 le risque existentiel lié à une
  pandémie fabriquée au cours de ce siècle — estimation jugée exagérée par d'autres chercheurs
  (ex. série « Exaggerating the risks », EA Forum). On le présente comme une estimation pessimiste.
- Une maladie qui tuerait absolument tout le monde est jugée très improbable (variabilité immunitaire,
  populations isolées) : formulation prudente.
"""
from engine import *

EPISODE = 13
BOOM_SCENE = 6
LEGENDE = """Épisode 13 : la pandémie de laboratoire 🧪🦠

Les accidents de labo, ça existe : en 1978 à Birmingham, la variole s'est échappée d'un laboratoire et a tué une photographe de l'université, la dernière victime de cette maladie. Il existe aujourd'hui 69 labos de sécurité maximale dans le monde (Global BioLabs, 2023), et les experts réclament surtout des règles plus strictes.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #pandemie #virus #biologie #science #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def virus(d, cx, cy, r, t, col='#ff5a7a', a=255, spikes=12, spike_len=0.45):
    c = hexc(col, a)
    for i in range(spikes):
        ang = i * 2 * math.pi / spikes + t * 0.6
        x1, y1 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        x2, y2 = cx + r * (1 + spike_len) * math.cos(ang), cy + r * (1 + spike_len) * math.sin(ang)
        line(d, [(x1, y1), (x2, y2)], c, max(3, r * 0.12))
        circle(d, x2, y2, max(4, r * 0.16), fill=c)
    circle(d, cx, cy, r, fill=c)
    circle(d, cx - r * 0.3, cy - r * 0.3, r * 0.22, fill=hexc('#ffffff', int(a * 0.45)))

def flask(d, cx, cy, t, liquid='#7ff0e0', glass='#e8f4ff', crack=0.0):
    """Le fil rouge : une fiole de labo (col étroit + ventre rond) avec du liquide qui bulle."""
    g = hexc(glass)
    # liquide
    circle(d, cx, cy + 60, 175, fill=hexc(liquid, 200))
    # contour
    circle(d, cx, cy + 60, 190, outline=g, width=16)
    d.rectangle([s(cx - 50), s(cy - 260), s(cx + 50), s(cy - 115)], fill=hexc(liquid, 120))
    line(d, [(cx - 55, cy - 120), (cx - 55, cy - 270)], g, 16)
    line(d, [(cx + 55, cy - 120), (cx + 55, cy - 270)], g, 16)
    d.rounded_rectangle([s(cx - 80), s(cy - 300), s(cx + 80), s(cy - 260)], radius=s(12), fill=g)
    # bulles
    for i in range(5):
        p = ((t * 0.7 + i * 0.21) % 1)
        circle(d, cx - 80 + i * 40, cy + 180 - 320 * p, 10 + 4 * (i % 2), fill=hexc('#ffffff', int(170 * (1 - p))))
    if crack > 0:
        pts = [(cx + 120, cy - 60), (cx + 150, cy - 10), (cx + 125, cy + 30), (cx + 165, cy + 80)]
        n = 1 + int(3 * min(1, crack))
        line(d, pts[:n + 1], '#ffffff', 8)

def globe(d, cx, cy, r, a=255):
    circle(d, cx, cy, r, fill=hexc('#2f7de1', a))
    for (dx, dy, rr) in ((-0.35, -0.25, 0.32), (0.3, 0.2, 0.28), (0.05, -0.5, 0.18), (-0.15, 0.45, 0.2), (0.55, -0.3, 0.15)):
        circle(d, cx + dx * r, cy + dy * r, rr * r, fill=hexc('#3fbf6a', a))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0d1b2a'); header(d, hexc('#7ff0e0'))
    flask(d, 540, 640, t)
    virus(d, 540, 700 + 12 * math.sin(t * 3), 55, t)
    text_block(img, ["Et si la prochaine grande épidémie sortait… d'un laboratoire ?"], t, 1090, '#ffffff', size=78)

def sc_lab(img, d, t, D):
    bg(d, '#123a2a'); header(d, hexc('#a8f0c0'))
    for i, (x, col) in enumerate(((250, '#ffd23f'), (540, '#7ff0e0'), (830, '#d2b8ff'))):
        k = ease((t - 0.2 - i * 0.35) / 0.4)
        if k <= 0: continue
        y = 700 + 30 * (1 - k)
        d.rounded_rectangle([s(x - 45), s(y - 260), s(x + 45), s(y + 110)], radius=s(45), outline=hexc('#e8f4ff', int(255 * k)), width=s(12))
        d.rounded_rectangle([s(x - 33), s(y - 90 + 8 * math.sin(t * 3 + i)), s(x + 33), s(y + 98)], radius=s(33), fill=hexc(col, int(200 * k)))
        virus(d, x, y + 20, 18, t + i, col='#ff5a7a', a=int(255 * k), spikes=9)
    text_block(img, ["Partout dans le monde, des labos étudient des virus dangereux… pour apprendre à les combattre."], t, 1070, '#ffffff', size=66)

def sc_bsl4(img, d, t, D):
    bg(d, '#1b2a4a'); header(d, hexc('#9fc2ff'))
    for i in range(4):
        k = ease((t - 0.2 - i * 0.3) / 0.4)
        m = 60 + i * 70
        d.rounded_rectangle([s(540 - 430 + m), s(330 + m * 0.75), s(540 + 430 - m), s(960 - m * 0.75)], radius=s(30), outline=hexc('#9fc2ff', int(255 * k)), width=s(10))
    flask_k = ease((t - 1.3) / 0.4)
    if flask_k > 0:
        virus(d, 540, 645, 50 * flask_k, t)
    text_block(img, ["Les plus protégés (niveau 4) sont de vraies boîtes dans des boîtes.", ("On en comptait 69 dans le monde en 2023.", 1.8)], t, 1040, '#ffffff', size=66)

def sc_leak(img, d, t, D):
    bg(d, '#3a1018'); header(d, hexc('#ffb3bd'))
    flask(d, 540, 660, t, liquid='#ff9aa8', crack=ease((t - 0.5) / 0.8) * 1.2)
    k = ease((t - 1.2) / 1.5)
    if k > 0:
        virus(d, 700 + 180 * k, 600 - 200 * k, 34, t, col='#ffd23f')
    d.text((s(90), s(330)), "1978", font=font(FBK, 100), fill=hexc('#ffb3bd', int(255 * ease((t - 0.1) / 0.4))))
    text_block(img, ["Mais les accidents existent. En 1978, à Birmingham, la variole s'échappe d'un labo.", ("Une photographe de l'université en meurt : la toute dernière victime de cette maladie.", 2.4)], t, 1020, '#ffffff', size=58)

def sc_gof(img, d, t, D):
    bg(d, '#24163d'); header(d, hexc('#d2b8ff'))
    flask(d, 540, 660, t, liquid='#b48cff')
    g = ease((t - 0.6) / 1.8)
    virus(d, 540, 720, 45 + 35 * g, t, spikes=int(8 + 10 * g), spike_len=0.4 + 0.3 * g)
    for i in range(3):
        kk = ease((t - 1.2 - i * 0.4) / 0.3)
        if kk > 0:
            d.text((s(800), s(350 + i * 90)), "+", font=font(FBK, 90), fill=hexc('#ffd23f', int(255 * kk)))
    text_block(img, ["Certains vont plus loin : ils rendent un virus plus contagieux, pour voir comment il pourrait évoluer (« gain de fonction »)."], t, 1050, '#ffffff', size=60)

random.seed(13)
DOTS = [(random.uniform(0, 2 * math.pi), random.uniform(0, 0.95), random.uniform(0.2, 3.0)) for _ in range(60)]
def sc_boom(img, d, t, D):
    bg(d, '#14060a'); stars(d, t, col='#ffb0a0'); header(d, hexc('#ffb0a0'))
    globe(d, 540, 660, 260)
    # le virus part d'un point et se répand
    for (ang, rr, birth) in DOTS:
        if t > birth:
            k = ease((t - birth) / 0.4)
            x = 540 + 230 * rr * math.cos(ang); y = 660 + 230 * rr * math.sin(ang)
            circle(d, x, y, 18 * k, fill=hexc('#ff4d5a', 220))
    p = ease(t / 0.8)
    if p < 1:
        virus(d, 160 + 380 * p, 330 + 330 * p, 40, t, col='#ff4d5a')
    text_block(img, ["Le cauchemar : un virus modifié s'échappe…", ("…et fait le tour du monde en quelques semaines.", 1.4)], t, 1060, '#ffffff', size=70)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    # frigo ouvert, un bocal oublié tout au fond
    d.rounded_rectangle([s(300), s(320), s(780), s(940)], radius=s(30), fill=hexc('#ffffff'), outline=hexc('#8a5a3c'), width=s(10))
    for y in (500, 680):
        line(d, [(320, y), (760, y)], '#c9b8a6', 8)
    d.rounded_rectangle([s(470), s(560), s(610), s(680)], radius=s(18), outline=hexc('#6a8a4a'), width=s(8))
    for i in range(6):
        circle(d, 495 + i * 22, 640 - 15 * math.sin(t * 2 + i), 16 + 4 * math.sin(t * 3 + i), fill=hexc('#7dbf4a'))
    d.rounded_rectangle([s(460), s(540), s(620), s(565)], radius=s(6), fill=hexc('#c0392b'))
    for i in range(3):
        p = ((t * 0.6 + i * 0.33) % 1)
        circle(d, 540 + 40 * math.sin(i * 2 + t), 520 - 120 * p, 8, fill=hexc('#7dbf4a', int(200 * (1 - p))))
    text_block(img, ["Pendant ce temps, chez vous…", ("…le bocal oublié au fond du frigo mène ses propres expériences.", 1.4)], t, 1010, '#2b1a10', size=66)

random.seed(7)
PEOPLE = [(150 + (i % 8) * 112, 400 + (i // 8) * 110, random.random()) for i in range(40)]
def sc_survive(img, d, t, D):
    bg(d, '#0f2e3a'); header(d, hexc('#9fe0ff'))
    k = ease((t - 0.8) / 1.0)
    for (x, y, r) in PEOPLE:
        col = '#ff6f7a' if r < 0.45 else '#7ff0a0'
        mix = col if k > 0.5 else '#c8d6e0'
        circle(d, x, y + 6 * math.sin(t * 3 + x), 34, fill=hexc(mix))
    text_block(img, ["Mais une maladie qui tue absolument tout le monde, c'est très improbable.", ("Nos corps ne réagissent pas tous pareil.", 1.8)], t, 1030, '#ffffff', size=64)

def sc_number(img, d, t, D):
    bg(d, '#000000'); stars(d, t); header(d, hexc('#9a9aa8'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "1 sur 30", 470, 190, '#ffd23f', FBK, k)
    ctext(d, "risque estimé sur ce siècle", 720, 44, '#9a9aa8', FM, k)
    text_block(img, [("C'est l'estimation, plutôt pessimiste, du chercheur d'Oxford Toby Ord, pour une pandémie fabriquée.", 0.6), ("D'autres la jugent bien plus faible.", 2.8)], t, 1000, '#ffffff', size=58)

def sc_rules(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    flask(d, 540, 660, t)
    # un cadenas / bouchon qui se visse
    k = ease((t - 0.4) / 0.8)
    d.rounded_rectangle([s(540 - 95), s(330 - 200 * (1 - k)), s(540 + 95), s(390 - 200 * (1 - k))], radius=s(14), fill=hexc('#2ecc71'))
    if k > 0.95:
        circle(d, 760, 420, 60, fill=hexc('#2ecc71'))
        line(d, [(732, 422), (754, 446), (792, 398)], '#ffffff', 12)
    text_block(img, ["Ce que demandent surtout les experts : des règles plus strictes.", ("Car le nombre de labos augmente plus vite que les contrôles.", 1.8)], t, 1040, '#ffffff', size=62)

sc_title = scene_title(["PANDÉMIE", "DE LABO"], "Scénario d'extinction n°13")
sc_end = scene_end("Bref : lavez-vous les mains, videz votre frigo… et payez quand même vos impôts.", color='#7a1030')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_lab, 4.2), (sc_bsl4, 4.4), (sc_leak, 5.2),
    (sc_gof, 4.6), (sc_boom, 4.2), (sc_joke, 4.6), (sc_survive, 4.6), (sc_number, 5.2),
    (sc_rules, 4.6), (sc_end, 4.8),
]
