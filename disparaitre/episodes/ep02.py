"""Épisode 2 — Les bactéries miroir.
Sources : Science (déc. 2024, 38 chercheurs dont des Nobel) ; CNN 16/12/2024 ; Live Science ; Futura.
"""
from engine import *

EPISODE = 2
BOOM_SCENE = 8
LEGENDE = """Épisode 2 : les bactéries miroir 🪞🦠

En décembre 2024, 38 scientifiques (dont des prix Nobel) ont publié une alerte dans la revue Science : des bactéries « inversées » pourraient échapper à nos défenses immunitaires. Bonne nouvelle : personne n'en fabrique, et ce serait encore hors de portée pour au moins dix ans.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #biologie #bacteries #vulgarisation #scienceenfrançais #microbiologie"""

# ---------- petits dessins ----------
def mitten(d, cx, cy, flip, col, a=255):
    c = hexc(col, a); m = -1 if flip else 1
    d.rounded_rectangle([s(cx - 75), s(cy - 60), s(cx + 75), s(cy + 150)], radius=s(55), fill=c)
    for i in range(4):
        fx = cx - 55 + i * 37
        d.rounded_rectangle([s(fx - 17), s(cy - 150 + abs(i - 1.5) * 18), s(fx + 17), s(cy - 20)], radius=s(17), fill=c)
    tx = cx + m * 95
    d.ellipse([s(tx - 30), s(cy - 10), s(tx + 30), s(cy + 90)], fill=c)
    d.rectangle([s(min(cx + m * 60, tx)), s(cy + 10), s(max(cx + m * 60, tx)), s(cy + 80)], fill=c)

def bacterium(d, cx, cy, col, t, flip=False, a=255, scale=1.0):
    c = hexc(col, a); w, h = 130 * scale, 60 * scale
    d.rounded_rectangle([s(cx - w), s(cy - h), s(cx + w), s(cy + h)], radius=s(h), fill=c)
    m = -1 if flip else 1
    for k in (-1, 0, 1):
        pts = [(cx + m * (w + j * 9 * scale), cy + k * 25 * scale + 12 * scale * math.sin(j * 0.7 + t * 6)) for j in range(14)]
        line(d, pts, c, 6 * scale)
    circle(d, cx - m * 40 * scale, cy - 10 * scale, 16 * scale, fill=hexc('#ffffff', int(a * 0.5)))

def key(d, x, y, mirrored, col):
    c = hexc(col)
    d.ellipse([s(x - 150), s(y - 55), s(x - 40), s(y + 55)], outline=c, width=s(22))
    d.rectangle([s(x - 45), s(y - 14), s(x + 150), s(y + 14)], fill=c)
    sgn = -1 if mirrored else 1
    for tx in (95, 135):
        y0, y1 = sorted((y + sgn * 14, y + sgn * 55))
        d.rectangle([s(x + tx - 14), s(y0), s(x + tx + 14), s(y1)], fill=c)

def padlock(d, cx, cy, col, open_k=0.0):
    c = hexc(col)
    lift = 60 * open_k
    d.arc([s(cx - 95), s(cy - 210 - lift), s(cx + 95), s(cy - 20 - lift)], 180, 360, fill=c, width=s(30))
    d.line([(s(cx - 95 + 15), s(cy - 115 - lift)), (s(cx - 95 + 15), s(cy - 60 - lift))], fill=c, width=s(30))
    d.line([(s(cx + 95 - 15), s(cy - 115 - lift)), (s(cx + 95 - 15), s(cy - 60))], fill=c, width=s(30))
    d.rounded_rectangle([s(cx - 150), s(cy - 70), s(cx + 150), s(cy + 170)], radius=s(30), fill=c)
    circle(d, cx, cy + 30, 30, fill=hexc('#000000', 200))
    d.rectangle([s(cx - 8), s(cy + 30), s(cx + 8), s(cy + 110)], fill=hexc('#000000', 200))

def mark(d, cx, cy, ok, k):
    if k <= 0: return
    r = 70 * k
    circle(d, cx, cy, r, fill=hexc('#2ecc71' if ok else '#ff4d5a'))
    if k > 0.6:
        if ok:
            line(d, [(cx - 32, cy + 2), (cx - 8, cy + 28), (cx + 36, cy - 26)], '#ffffff', 14)
        else:
            line(d, [(cx - 28, cy - 28), (cx + 28, cy + 28)], '#ffffff', 14)
            line(d, [(cx + 28, cy - 28), (cx - 28, cy + 28)], '#ffffff', 14)

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0d1b1e'); header(d, hexc('#7ff0e0'))
    d.rounded_rectangle([s(300), s(330), s(780), s(950)], radius=s(240), outline=hexc('#cfe9ec'), width=s(14))
    d.line([(s(540), s(370)), (s(540), s(910))], fill=hexc('#cfe9ec', 90), width=s(4))
    wob = 10 * math.sin(t * 3)
    bacterium(d, 440, 640 + wob, '#7ff0e0', t, flip=True, scale=0.42)
    k = ease((t - 0.8) / 0.6)
    bacterium(d, 640, 640 + wob, '#ff6fb5', t, flip=False, a=int(255 * k), scale=0.42)
    text_block(img, ["Et si le prochain grand danger venait… d'un reflet ?"], t, 1090, '#ffffff', size=80)

def sc_hands(img, d, t, D):
    bg(d, '#1b2a4a'); header(d, hexc('#9fc2ff'))
    k = ease((t - 0.2) / 0.6)
    mitten(d, 540 - 190 * k, 640, False, '#ffd6a8')
    mitten(d, 540 + 190 * k, 640, True, '#ffb37a')
    text_block(img, ["Vos deux mains se ressemblent…", ("…mais elles sont inversées. Impossible de les superposer.", 1.4)], t, 1030, '#ffffff', size=70)

def sc_molecules(img, d, t, D):
    bg(d, '#24163d'); header(d, hexc('#d2b8ff'))
    for row in range(4):
        for col in range(5):
            x = 170 + col * 185; y = 380 + row * 150 + 10 * math.sin(t * 4 + col + row)
            line(d, [(x - 45, y + 30), (x - 45, y - 30), (x + 40, y - 30)], '#d2b8ff', 16)
            circle(d, x + 40, y - 30, 16, fill=hexc('#ff6fb5'))
    text_block(img, ["Les molécules de la vie ont aussi un « sens ». Et chez tous les êtres vivants, c'est le même."], t, 1060, '#ffffff', size=66)

def sc_mirror(img, d, t, D):
    bg(d, '#0d1b1e'); header(d, hexc('#7ff0e0'))
    line(d, [(540, 380), (540, 900)], '#cfe9ec', 6)
    bacterium(d, 300, 640, '#7ff0e0', t, flip=True, scale=0.8)
    k = ease((t - 0.7) / 0.8)
    if k > 0:
        bacterium(d, 540 + 240 * k, 640, '#ff6fb5', t, flip=False, a=int(255 * k), scale=0.8)
    text_block(img, ["Des chercheurs pourraient un jour fabriquer une bactérie entièrement inversée : une bactérie miroir."], t, 1060, '#ffffff', size=66)

def sc_key_ok(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.3) / 1.0)
    open_k = ease((t - 1.4) / 0.4)
    key(d, 120 + 340 * k, 670, False, '#ffffff')
    padlock(d, 760, 640, '#a8f0c0', open_k)
    mark(d, 760, 380, True, ease((t - 1.5) / 0.3))
    text_block(img, ["Notre système immunitaire repère les microbes grâce à leur forme. Comme une clé dans une serrure."], t, 1060, '#ffffff', size=64)

def sc_key_fail(img, d, t, D):
    bg(d, '#3a1018'); header(d, hexc('#ffb3bd'))
    k = ease((t - 0.3) / 1.0)
    shake = 12 * math.sin(t * 40) * max(0, 1 - abs(t - 1.5) * 2) if t > 1.2 else 0
    key(d, 120 + 300 * k + shake, 670, True, '#ff6fb5')
    padlock(d, 760, 640, '#ffb3bd')
    mark(d, 760, 380, False, ease((t - 1.6) / 0.3))
    text_block(img, ["Une clé inversée ne rentre pas. La bactérie miroir passerait sans être vue."], t, 1060, '#ffffff', size=68)

def sc_nothing(img, d, t, D):
    bg(d, '#2a0b30'); header(d, hexc('#f0b8ff'))
    labels = ["défenses immunitaires", "virus prédateurs", "la plupart des antibiotiques"]
    for i, l in enumerate(labels):
        y = 400 + i * 150; k = ease((t - 0.3 - i * 0.6) / 0.3)
        if k <= 0: continue
        ctext(d, l, y, 54, '#ffffff', FB, k)
        if t > 0.6 + i * 0.6:
            w = font(FB, 54).getlength(l) / S
            kk = ease((t - 0.6 - i * 0.6) / 0.25)
            line(d, [(540 - w / 2 - 20, y + 35), (540 - w / 2 - 20 + (w + 40) * kk, y + 35)], '#ff4d5a', 10)
    text_block(img, [("Rien de tout ça ne serait conçu pour l'arrêter.", 2.4)], t, 1060, '#ffffff', size=74)

random.seed(9)
SPREAD = [(random.uniform(80, 1000), random.uniform(320, 980), random.uniform(0, 3.2), random.random() < 0.5) for _ in range(70)]
def sc_spread(img, d, t, D):
    bg(d, '#0d1b1e'); header(d, hexc('#7ff0e0'))
    for (x, y, birth, f) in SPREAD:
        if t > birth * 0.9:
            k = ease((t - birth * 0.9) / 0.3)
            bacterium(d, x, y, '#ff6fb5', t + birth, flip=f, a=int(230 * k), scale=0.28 * k)
    text_block(img, ["Elle pourrait se répandre partout : chez les humains, les animaux… et les plantes."], t, 1080, '#ffffff', size=68)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    d.rounded_rectangle([s(340), s(340), s(740), s(880)], radius=s(30), outline=hexc('#8a5a3c'), width=s(16))
    circle(d, 540, 600, 120, fill=hexc('#ffd6a8'))
    for i in range(7):
        a = math.pi + i * math.pi / 6
        line(d, [(540 + 110 * math.cos(a), 600 + 110 * math.sin(a)), (540 + 160 * math.cos(a + 0.2 * math.sin(t * 3 + i)), 600 + 160 * math.sin(a))], '#4a2c1d', 12)
    blink = 4 if int(t * 1.5) % 3 == 0 else 14
    for ex in (495, 585):
        d.ellipse([s(ex - 16), s(585 - blink / 2), s(ex + 16), s(585 + blink / 2)], fill=hexc('#4a2c1d'))
    line(d, [(510, 660), (570, 650)], '#4a2c1d', 8)
    text_block(img, ["Jusqu'ici, le miroir le plus effrayant…", ("…c'était celui de la salle de bain à 7 h du matin.", 1.6)], t, 1010, '#2b1a10', size=68)

def sc_good(img, d, t, D):
    bg(d, '#000000'); stars(d, t)
    header(d, hexc('#9a9aa8'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "scientifiques ont lancé l'alerte", 720, 42, '#9a9aa8', FM, k)
    n = int(min(38, 38 * ease(t / 1.2)))
    ctext(d, str(n), 470, 220, '#7ff0e0', FBK, k)
    text_block(img, [("En 2024, des chercheurs, dont des prix Nobel, ont demandé que personne n'en fabrique. Et pour l'instant, personne n'essaie.", 1.0)], t, 1000, '#ffffff', size=62)

def sc_delay(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "10 ANS+", 520, 170, '#a8f0c0', FBK, k)
    ctext(d, "avant que ce soit seulement possible", 730, 42, '#a8f0c0', FM, k)
    text_block(img, [("Et la technique est encore très loin d'être prête.", 0.8)], t, 1060, '#ffffff', size=72)

sc_title = scene_title(["BACTÉRIES", "MIROIR"], "Scénario d'extinction n°2")
sc_end = scene_end("Bref : vous pouvez continuer à vous regarder dans le miroir. Pour l'instant.")

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_hands, 4.0), (sc_molecules, 4.2), (sc_mirror, 4.4),
    (sc_key_ok, 4.2), (sc_key_fail, 4.0), (sc_nothing, 4.2), (sc_spread, 4.0),
    (sc_joke, 4.6), (sc_good, 5.4), (sc_delay, 3.8), (sc_end, 4.8),
]
