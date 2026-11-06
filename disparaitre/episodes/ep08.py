"""Épisode 8 — Mythe : la planète Nibiru.
Sources : Space.com, « Nibiru: The Nonexistent Planet » ; NASA Astrobiology, « Nibiru and Doomsday 2012:
Questions and Answers » (David Morrison) ; Popular Science (2009) ; Skeptic ; IFLScience.
- L'idée vient de Zecharia Sitchin, « The 12th Planet » (1976), qui prétendait la lire dans des textes
  sumériens ; les spécialistes de l'assyriologie rejettent ses traductions.
- Dates de fin du monde annoncées : 2003 (Nancy Lieder), puis 2012, puis 2017 (David Meade).
- NASA / D. Morrison : une planète en approche serait parmi les objets les plus brillants du ciel,
  visible à l'œil nu des années à l'avance ; elle ne peut pas rester « cachée derrière le Soleil »
  puisque la Terre en fait le tour. Nibiru n'existe pas.
"""
from engine import *

EPISODE = 8
BOOM_SCENE = 6
LEGENDE = """Épisode 8 : le mythe de la planète Nibiru 🪐🙄

Selon une rumeur qui tourne depuis les années 1990, une planète géante cachée viendrait percuter la Terre. Elle était annoncée pour 2003, puis 2012, puis 2017… Pour la NASA, c'est simple : une planète qui foncerait vers nous serait visible à l'œil nu depuis des années. Nibiru n'existe pas.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #nibiru #apocalypse #mythe #astronomie #espace #science #vulgarisation"""

# ---------- petits dessins ----------
def glow(img, cx, cy, r, col, a):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(layer)
    for k in range(6, 0, -1):
        rr = r * (1 + k * 0.25)
        dd.ellipse([s(cx - rr), s(cy - rr), s(cx + rr), s(cy + rr)], fill=hexc(col, int(a * 0.12)))
    img.alpha_composite(layer)

def nibiru(img, d, cx, cy, r, t=0, a=255):
    glow(img, cx, cy, r, '#ff4a3d', 160 * a / 255)
    circle(d, cx, cy, r, fill=hexc('#d8342a', a))
    for i, (oy, w) in enumerate(((-0.35, 0.8), (0.05, 0.95), (0.4, 0.7))):
        hw = r * w
        d.line([(s(cx - hw), s(cy + oy * r + 4 * math.sin(t * 2 + i))), (s(cx + hw), s(cy + oy * r - 4 * math.sin(t * 2 + i)))],
               fill=hexc('#8a1a14', a), width=s(max(4, r * 0.12)))

def earth(d, cx, cy, r, t=0):
    circle(d, cx, cy, r, fill=hexc('#2f7fd8'))
    for (ox, oy, rr) in ((-0.35, -0.2, 0.33), (0.3, 0.25, 0.28), (0.1, -0.45, 0.18)):
        circle(d, cx + ox * r + 5 * math.sin(t), cy + oy * r, rr * r, fill=hexc('#3fae5a'))

def sun(img, d, cx, cy, r):
    glow(img, cx, cy, r, '#ffd23f', 200)
    circle(d, cx, cy, r, fill=hexc('#ffd23f'))

def ctx(d, txt, x, y, sz, col, fp=FB):
    f = font(fp, sz); d.text((s(x) - f.getlength(txt) / 2, s(y)), txt, font=f, fill=hexc(col))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#07060f'); stars(d, t); header(d, hexc('#ffb3a8'))
    k = 0.5 + 0.5 * math.sin(t * 4)
    nibiru(img, d, 540, 620, 24 + 70 * ease(t / D) + 4 * k, t)
    text_block(img, ["Et si une planète cachée fonçait droit sur la Terre ?"], t, 1090, '#ffffff', size=80)

def sc_story(img, d, t, D):
    bg(d, '#14213d'); header(d, hexc('#ffd23f'))
    earth(d, 170, 620, 80, t)
    sun(img, d, 560, 620, 120)
    x = 880 - 40 * ease((t - 1.0) / 2.0)
    nibiru(img, d, x, 620 - 20 * math.sin(t), 70, t)
    text_block(img, ["La rumeur : une planète géante, Nibiru, se cacherait derrière le Soleil…", ("… avant de venir nous percuter.", 1.8)], t, 1050, '#ffffff', size=68)

def sc_book(img, d, t, D):
    bg(d, '#3d2b14'); header(d, hexc('#ffd8a0'))
    wob = 5 * math.sin(t * 2)
    d.rounded_rectangle([s(170), s(430 + wob), s(470), s(860 + wob)], radius=s(18), fill=hexc('#a0522d'))
    d.rounded_rectangle([s(195), s(455 + wob), s(445), s(835 + wob)], radius=s(10), outline=hexc('#ffd8a0'), width=s(5))
    ctx(d, "1976", 320, 610 + wob, 64, '#ffd8a0', FBK)
    # tablette d'argile avec petits signes
    d.rounded_rectangle([s(600), s(450 - wob), s(910), s(850 - wob)], radius=s(40), fill=hexc('#c9a26b'))
    random.seed(8)
    for j in range(5):
        for i in range(4):
            if random.random() < 0.8:
                x, y = 645 + i * 70, 500 + j * 70 - wob
                d.polygon([(s(x), s(y)), (s(x + 40), s(y + 12)), (s(x), s(y + 24))], fill=hexc('#7a5a30'))
    text_block(img, ["Elle vient d'un livre de 1976, qui prétendait l'avoir lue dans de vieilles tablettes sumériennes."], t, 1050, '#ffffff', size=66)

def sc_translation(img, d, t, D):
    bg(d, '#1f3d2b'); header(d, hexc('#b8f0c8'))
    d.rounded_rectangle([s(385), s(420), s(695), s(820)], radius=s(40), fill=hexc('#c9a26b'))
    k = ease((t - 0.8) / 0.4)
    if k > 0:
        a = int(255 * k)
        line(d, [(380, 410), (700, 830)], hexc('#ff4a3d', a), 26)
        line(d, [(700, 410), (380, 830)], hexc('#ff4a3d', a), 26)
    text_block(img, ["Problème : les spécialistes de ces textes disent que c'est une traduction fantaisiste."], t, 1050, '#ffffff', size=68)

def sc_dates(img, d, t, D):
    bg(d, '#2b1a3d'); header(d, hexc('#e0c0ff'))
    for i, yr in enumerate(("2003", "2012", "2017")):
        x = 210 + i * 330
        appear = 0.3 + i * 0.9
        k = ease((t - appear) / 0.3)
        if k <= 0: continue
        a = int(255 * k)
        d.rounded_rectangle([s(x - 130), s(470), s(x + 130), s(780)], radius=s(26), fill=hexc('#ffffff', a))
        d.rounded_rectangle([s(x - 130), s(470), s(x + 130), s(560)], radius=s(26), fill=hexc('#d8342a', a))
        ctx(d, yr, x, 620, 70, '#2b1a3d', FBK)
        kk = ease((t - appear - 0.5) / 0.3)
        if kk > 0:
            line(d, [(x - 110, 500), (x + 110, 760)], hexc('#d8342a', int(255 * kk)), 16)
    text_block(img, [("Fin du monde annoncée pour 2003.", 0.3), ("Puis 2012.", 1.2), ("Puis 2017…", 2.1)], t, 1050, '#ffffff', size=72)

def sc_boom(img, d, t, D):
    bg(d, '#4a0a12'); header(d, hexc('#ffb3bd'))
    k = ease((t - 0.2) / 1.0)
    shake = 12 * math.sin(t * 45) * max(0, 1 - abs(t - 1.3) * 1.5)
    earth(d, 680 + shake, 640, 150, t)
    nibiru(img, d, 120 + 320 * k, 600, 120 + 40 * k, t)
    if 1.0 < t < 1.8:
        layer = Image.new('RGBA', img.size, (255, 255, 255, int(170 * max(0, 1 - abs(t - 1.2) * 2.5))))
        img.alpha_composite(layer)
    text_block(img, ["Dans le scénario, elle frôle la Terre.", ("Séismes, raz-de-marée… rideau.", 1.5)], t, 1050, '#ffffff', size=72)

def sc_bright(img, d, t, D):
    bg(d, '#0a1630'); stars(d, t); header(d, hexc('#9fd0ff'))
    # silhouette de collines
    d.polygon([(0, s(950)), (s(250), s(840)), (s(520), s(910)), (s(800), s(820)), (s(1080), s(900)), (s(1080), s(960)), (0, s(960))], fill=hexc('#050a18'))
    k = 0.5 + 0.5 * math.sin(t * 3)
    glow(img, 540, 560, 110, '#ffffff', 200)
    nibiru(img, d, 540, 560, 70 + 6 * k, t)
    text_block(img, ["Sauf qu'une planète qui foncerait vers nous serait l'un des objets les plus brillants du ciel."], t, 1050, '#ffffff', size=66)

def sc_scopes(img, d, t, D):
    bg(d, '#123a3a'); header(d, hexc('#8af0e0'))
    nibiru(img, d, 540, 400, 44, t)
    for i, x in enumerate((220, 540, 860)):
        tx, ty = x + (540 - x) * 0.45 + 6 * math.sin(t * 2 + i), 900 - (900 - 400) * 0.45
        line(d, [(x, 900), (tx, ty)], '#e0fff8', 34)
        line(d, [(x, 900), (x - 50, 960)], '#8af0e0', 8)
        line(d, [(x, 900), (x + 50, 960)], '#8af0e0', 8)
    text_block(img, ["Visible à l'œil nu depuis des années. Des milliers d'astronomes amateurs l'auraient repérée."], t, 1050, '#ffffff', size=66)

def sc_orbit(img, d, t, D):
    bg(d, '#2a2a05'); header(d, hexc('#ffe08a'))
    sun(img, d, 540, 640, 70)
    circle(d, 540, 640, 260, outline=hexc('#ffe08a', 120), width=4)
    ang = math.pi + t / D * math.pi
    earth(d, 540 + 260 * math.cos(ang), 640 + 260 * math.sin(ang), 40, t)
    text_block(img, ["Et impossible de se cacher derrière le Soleil : la Terre en fait le tour chaque année."], t, 1050, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#ffe9c7'); header(d, hexc('#a0521d'))
    wob = 6 * math.sin(t * 3)
    d.rounded_rectangle([s(330), s(470 + wob), s(750), s(860 + wob)], radius=s(24), fill=hexc('#c98a4a'))
    d.rectangle([s(510), s(470 + wob), s(570), s(860 + wob)], fill=hexc('#e8c28a'))
    d.rounded_rectangle([s(600), s(760 + wob), s(730), s(830 + wob)], radius=s(8), fill=hexc('#ffffff'))
    ctx(d, "ENVOI EN COURS…", 540, 380 + wob, 44, '#a0521d', FBK)
    text_block(img, ["Une planète annoncée chaque année et qui n'arrive jamais ?", ("Ça s'appelle un colis en point relais.", 1.8)], t, 1010, '#3a1a08', size=66)

def sc_zero(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "0 %", 440, 220, '#a8f0c0', FBK, k)
    ctext(d, "de risque", 720, 48, '#a8f0c0', FM, k)
    text_block(img, [("Pour la NASA, c'est clair : Nibiru n'existe pas.", 0.7)], t, 1060, '#ffffff', size=72)

sc_title = scene_title(["MYTHE :", "NIBIRU"], "Scénario d'extinction n°8")
sc_end = scene_end("Bref : aucune planète ne viendra nous écraser. Votre avis d'impôt, lui, arrive toujours.")

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_story, 4.4), (sc_book, 4.6), (sc_translation, 4.2),
    (sc_dates, 4.0), (sc_boom, 4.2), (sc_bright, 4.6), (sc_scopes, 4.6),
    (sc_orbit, 4.4), (sc_joke, 4.6), (sc_zero, 3.6), (sc_end, 4.8),
]
