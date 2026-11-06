"""Épisode 7 — Le sursaut gamma (hypothèse de l'extinction de l'Ordovicien).
Sources : Melott et al., « Did a gamma-ray burst initiate the late Ordovician mass extinction? »,
International Journal of Astrobiology (2004) ; communiqué NASA/Université du Kansas (phys.org, 2005 ;
NBC News) : un sursaut à moins de ~6 000 années-lumière pourrait détruire jusqu'à la moitié de la couche
d'ozone ; l'Ordovicien (~440-450 millions d'années) a vu disparaître ~85 % des espèces marines.
GRB 221009A (« BOAT », 9 oct. 2022), à ~2 milliards d'années-lumière, a perturbé l'ionosphère terrestre
(Nature Communications 2023 ; Live Science ; Scientific American).
Piran & Jimenez, Physical Review Letters (2014) : sursauts mortels rares, de l'ordre d'un tous les
centaines de millions d'années pour la Terre (phys.org, Universe Today).
La cause principale admise de l'extinction de l'Ordovicien reste une glaciation : le sursaut gamma est
présenté comme une hypothèse non prouvée.
"""
from engine import *

EPISODE = 7
BOOM_SCENE = 7
LEGENDE = """Épisode 7 : le sursaut gamma 🌟💥

Quand certaines étoiles géantes meurent, elles projettent deux jets d'énergie si puissants qu'ils pourraient arracher une grande partie de la couche d'ozone d'une planète située à quelques milliers d'années-lumière. Des chercheurs de la NASA et de l'Université du Kansas se sont demandé si ce n'était pas arrivé à la Terre il y a environ 440 millions d'années. Mais ça reste une hypothèse, et ces événements sont rarissimes.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #astronomie #espace #sursautgamma #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def glow(img, cx, cy, r, col, a):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(layer)
    for k in range(6, 0, -1):
        rr = r * (1 + k * 0.25)
        dd.ellipse([s(cx - rr), s(cy - rr), s(cx + rr), s(cy + rr)], fill=hexc(col, int(a * 0.12)))
    img.alpha_composite(layer)

def jets(img, cx, cy, ang, length, width, col, a=230):
    """Deux faisceaux opposés en forme de cône étroit."""
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(layer)
    for sgn in (1, -1):
        ux, uy = sgn * math.cos(ang), sgn * math.sin(ang)
        px, py = -uy, ux
        tip = (cx + ux * length, cy + uy * length)
        pts = [(cx + px * 8, cy + py * 8), (tip[0] + px * width, tip[1] + py * width),
               (tip[0] - px * width, tip[1] - py * width), (cx - px * 8, cy - py * 8)]
        dd.polygon([(s(x), s(y)) for x, y in pts], fill=hexc(col, a))
        pts2 = [(cx, cy), (tip[0] + px * width * 0.35, tip[1] + py * width * 0.35),
                (tip[0] - px * width * 0.35, tip[1] - py * width * 0.35)]
        dd.polygon([(s(x), s(y)) for x, y in pts2], fill=hexc('#ffffff', a))
    img.alpha_composite(layer)

def earth(d, cx, cy, r, ozone_k=1.0, t=0, hole=0.0):
    if ozone_k > 0:
        # couche d'ozone : anneau, avec un trou qui s'ouvre côté gauche
        if hole > 0:
            gap = 70 * hole
            d.arc([s(cx - r - 28), s(cy - r - 28), s(cx + r + 28), s(cy + r + 28)], 180 + gap, 180 - gap + 360,
                  fill=hexc('#7fd3ff', int(255 * ozone_k)), width=s(16))
        else:
            circle(d, cx, cy, r + 28, outline=hexc('#7fd3ff', int(255 * ozone_k)), width=16)
    circle(d, cx, cy, r, fill=hexc('#2f7fd8'))
    for (ox, oy, rr) in ((-0.35, -0.2, 0.33), (0.3, 0.25, 0.28), (0.1, -0.45, 0.18)):
        circle(d, cx + ox * r + 6 * math.sin(t), cy + oy * r, rr * r, fill=hexc('#3fae5a'))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#05060f'); stars(d, t); header(d, hexc('#c9b8ff'))
    k = 0.5 + 0.5 * math.sin(t * 5)
    glow(img, 540, 620, 40, '#fff2b0', 180 + 70 * k)
    circle(d, 540, 620, 30 + 6 * k, fill=hexc('#fff7d6'))
    text_block(img, ["Et si l'humanité disparaissait… à cause d'un flash de lumière ?"], t, 1090, '#ffffff', size=80)

def sc_star(img, d, t, D):
    bg(d, '#1a0b2e'); header(d, hexc('#ffb36b'))
    k = ease((t - 0.8) / 1.4)
    r = 230 - 200 * k
    glow(img, 540, 630, r, '#ff8a3d', 200)
    circle(d, 540, 630, r, fill=hexc('#ff9a4a'))
    if k > 0.8:
        circle(d, 540, 630, 28, fill=hexc('#000000'), outline=hexc('#ffd28a'), width=6)
    text_block(img, ["Quand une étoile géante meurt, son cœur peut s'effondrer en trou noir."], t, 1070, '#ffffff', size=70)

def sc_jets(img, d, t, D):
    bg(d, '#0b1c3a'); header(d, hexc('#9fd8ff'))
    k = ease((t - 0.4) / 1.0)
    ang = -1.2 + 0.05 * math.sin(t * 2)
    jets(img, 540, 630, ang, 330 * k + 5, 50 * k + 2, '#9fd8ff')
    glow(img, 540, 630, 40, '#ffffff', 220)
    circle(d, 540, 630, 30, fill=hexc('#ffffff'))
    text_block(img, ["Elle crache alors deux jets d'énergie, comme deux lampes torches géantes."], t, 1070, '#ffffff', size=70)

def sc_name(img, d, t, D):
    bg(d, '#2b0f3d'); header(d, hexc('#f0b8ff'))
    flash = max(0, 1 - abs(t - 1.0) * 2.5)
    jets(img, 540, 630, -1.2, 340, 55 + 30 * flash, '#f0b8ff')
    glow(img, 540, 630, 50 + 60 * flash, '#ffffff', 230)
    circle(d, 540, 630, 32 + 30 * flash, fill=hexc('#ffffff'))
    text_block(img, ["C'est un sursaut gamma : l'explosion la plus puissante connue dans l'univers."], t, 1070, '#ffffff', size=70)

def sc_energy(img, d, t, D):
    bg(d, '#3a2a05'); header(d, hexc('#ffe08a'))
    # petit soleil à gauche, sursaut à droite
    circle(d, 290, 600, 70, fill=hexc('#ffd23f'))
    ctext_x = lambda txt, x, y, sz, col: d.text((s(x) - font(FB, sz).getlength(txt) / 2, s(y)), txt, font=font(FB, sz), fill=hexc(col))
    ctext_x("Soleil", 290, 810, 40, '#ffe08a')
    ctext_x("10 milliards d'années", 290, 865, 34, '#ffe08a')
    k = ease((t - 0.6) / 0.5)
    jets(img, 790, 600, -1.35, 150 * k + 4, 30 * k + 2, '#ffe08a')
    circle(d, 790, 600, 28, fill=hexc('#ffffff'))
    ctext_x("Sursaut", 790, 810, 40, '#ffe08a')
    ctext_x("quelques secondes", 790, 865, 34, '#ffe08a')
    ctext(d, "=", 590, 90, '#ffffff', FBK, k)
    text_block(img, [("En quelques secondes, il libère autant d'énergie que le Soleil pendant toute sa vie.", 0.4)], t, 1060, '#ffffff', size=66)

def sc_aim(img, d, t, D):
    bg(d, '#0d2a2a'); header(d, hexc('#8af0e0'))
    earth(d, 820, 640, 120, 1.0, t)
    k = ease((t - 0.4) / 1.6)
    jets(img, 170, 640, 0.0, 120 + 380 * k, 30 + 30 * k, '#8af0e0', 200)
    circle(d, 170, 640, 26, fill=hexc('#ffffff'))
    text_block(img, ["Le danger : qu'un de ces jets vise la Terre depuis notre galaxie, à quelques milliers d'années-lumière."], t, 1050, '#ffffff', size=64)

def sc_boom(img, d, t, D):
    hit = ease((t - 0.3) / 0.4)
    bg(d, '#4a0a12'); header(d, hexc('#ffb3bd'))
    hole = ease((t - 0.7) / 0.9)
    shake = 10 * math.sin(t * 45) * max(0, 1 - abs(t - 0.9) * 1.5)
    earth(d, 700 + shake, 640, 150, 1.0, t, hole)
    jets(img, 60, 640, 0.0, 520 * hit + 4, 70 * hit + 2, '#ffd0d6', 210)
    if 0.5 < t < 1.3:
        layer = Image.new('RGBA', img.size, (255, 255, 255, int(160 * max(0, 1 - abs(t - 0.7) * 2.5))))
        img.alpha_composite(layer)
    text_block(img, ["Il détruirait jusqu'à la moitié de la couche d'ozone.", ("Les UV du Soleil frapperaient la vie de plein fouet.", 1.6)], t, 1030, '#ffffff', size=68)

def sc_ordo(img, d, t, D):
    bg(d, '#0a2a4a'); header(d, hexc('#9fd0ff'))
    # mer et petites créatures marines (ovales segmentés) qui s'effacent
    for i in range(5):
        y = 380 + i * 40
        line(d, [(80 + x * 46, y + 10 * math.sin(x * 0.8 + t * 3 + i)) for x in range(21)], hexc('#5aa8e8', 140), 6)
    random.seed(3)
    for j in range(12):
        x = 130 + (j % 6) * 165; y = 680 + (j // 6) * 170
        fade = 0.15 if j in (2, 9) else 1 - ease((t - 1.2 - j * 0.12) / 0.4)
        a = int(255 * max(0.15, fade))
        d.ellipse([s(x - 55), s(y - 35), s(x + 55), s(y + 35)], fill=hexc('#e8c28a', a))
        for kx in (-25, 0, 25):
            d.line([(s(x + kx), s(y - 33)), (s(x + kx), s(y + 33))], fill=hexc('#8a6a3a', a), width=s(5))
    text_block(img, ["Certains chercheurs se demandent si c'est arrivé il y a 440 millions d'années.", ("Ce jour-là, environ 85 % des espèces marines ont disparu.", 1.8)], t, 1030, '#ffffff', size=60)

def sc_joke(img, d, t, D):
    bg(d, '#ffe9c7'); header(d, hexc('#a0521d'))
    wob = 6 * math.sin(t * 3)
    d.rounded_rectangle([s(420), s(400 + wob), s(660), s(880 + wob)], radius=s(50), fill=hexc('#ff8a3d'))
    d.rounded_rectangle([s(480), s(330 + wob), s(600), s(410 + wob)], radius=s(16), fill=hexc('#ffffff'))
    d.rounded_rectangle([s(445), s(560 + wob), s(635), s(740 + wob)], radius=s(20), fill=hexc('#ffffff'))
    ctext(d, "SPF", 585 + wob, 46, '#a0521d', FBK)
    k = ease((t - 1.6) / 0.4)
    ctext(d, "50" if t < 1.6 else "1 000 000", 655 + wob, 50 if t < 1.6 else 34, '#a0521d', FBK, 1)
    text_block(img, ["Bonne nouvelle : contre les UV, on a la crème solaire.", ("Mauvaise nouvelle : il faudrait de l'indice un million.", 1.6)], t, 1010, '#3a1a08', size=66)

def sc_boat(img, d, t, D):
    bg(d, '#000000'); stars(d, t); header(d, hexc('#9a9aa8'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "2 MILLIARDS", 450, 130, '#c9b8ff', FBK, k)
    ctext(d, "d'années-lumière", 610, 50, '#c9b8ff', FM, k)
    ctext(d, "le plus puissant jamais vu (2022)", 690, 42, '#9a9aa8', FM, k)
    text_block(img, [("Le plus puissant jamais observé était à 2 milliards d'années-lumière. Il a juste chatouillé notre atmosphère.", 0.9)], t, 1010, '#ffffff', size=62)

def sc_rare(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "RARISSIME", 470, 140, '#a8f0c0', FBK, k)
    ctext(d, "≈ 1 fois en plusieurs centaines de millions d'années", 670, 36, '#a8f0c0', FM, k)
    text_block(img, [("Et pour l'Ordovicien, c'est une hypothèse : la piste principale reste une grande glaciation.", 0.8)], t, 1040, '#ffffff', size=64)

sc_title = scene_title(["SURSAUT", "GAMMA"], "Scénario d'extinction n°7")
sc_end = scene_end("Bref : le ciel ne devrait pas nous griller demain. Votre feuille d'impôts, si.")

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_star, 3.8), (sc_jets, 4.0), (sc_name, 3.8),
    (sc_energy, 4.4), (sc_aim, 4.6), (sc_boom, 4.6), (sc_ordo, 5.0),
    (sc_joke, 4.6), (sc_boat, 5.0), (sc_rare, 4.6), (sc_end, 4.8),
]
