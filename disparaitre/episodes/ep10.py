"""Épisode 10 — La gelée grise (nanorobots auto-répliquants).
Sources : Wikipédia « Gray goo » ; K. E. Drexler, « Engines of Creation » (1986) ;
R. Freitas, « Some Limits to Global Ecophagy by Biovorous Nanoreplicators » (avril 2000) ;
C. Phoenix & K. E. Drexler, « Safe Exponential Manufacturing », Nanotechnology 15 (2004),
communiqué IOP repris par innovations-report (9 juin 2004) ; J. Giles, Nature 429, 591 (2004).
- Terme « grey goo » inventé par Eric Drexler dans Engines of Creation (1986), comme expérience de pensée.
- Freitas (2000) : une invasion rapide chaufferait et serait repérable tôt ; « tous les scénarios
  examinés semblent permettre une détection précoce par une surveillance vigilante ».
- Drexler (2004) : « J'aurais aimé ne jamais utiliser le terme » ; les machines auto-répliquantes
  ne sont pas nécessaires à la fabrication moléculaire et ne peuvent pas être construites avec les outils actuels.
- Royal Society (2004) : trop lointain pour préoccuper les régulateurs.
"""
from engine import *

EPISODE = 10
BOOM_SCENE = 7
LEGENDE = """Épisode 10 : la gelée grise 🤖🫠

Et si des robots minuscules se copiaient sans fin jusqu'à dévorer la planète ? L'idée vient d'Eric Drexler, en 1986… qui a lui-même regretté en 2004 d'avoir inventé le terme (Nature). Aucun robot de ce genre n'existe, et on n'en a pas besoin pour fabriquer des choses.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #nanotechnologie #robots #science #vulgarisation #scienceenfrançais #greygoo"""

# ---------- petits dessins ----------
def bot(d, cx, cy, r, t, col='#c9ced6', eye='#3ad6ff', a=255, phase=0.0):
    """Le fil rouge : un petit nanorobot hexagonal à pattes."""
    c = hexc(col, a)
    for i in range(6):
        ang = i * math.pi / 3 + math.pi / 6
        wig = 0.25 * math.sin(t * 9 + i + phase)
        x0, y0 = cx + r * 0.9 * math.cos(ang), cy + r * 0.9 * math.sin(ang)
        x1, y1 = cx + r * 1.55 * math.cos(ang + wig), cy + r * 1.55 * math.sin(ang + wig)
        line(d, [(x0, y0), (x1, y1)], c, max(3, r * 0.14))
    pts = [(s(cx + r * math.cos(i * math.pi / 3)), s(cy + r * math.sin(i * math.pi / 3))) for i in range(6)]
    d.polygon(pts, fill=c)
    circle(d, cx, cy, r * 0.38, fill=hexc(eye, a))

def cell(d, cx, cy, r, col):
    circle(d, cx, cy, r, fill=hexc(col, 120), outline=hexc(col), width=s(8))
    circle(d, cx + r * 0.2, cy - r * 0.15, r * 0.3, fill=hexc(col, 200))

def goo(d, cx, cy, R, t, col='#8a8f99', a=255):
    pts = []
    for i in range(48):
        ang = 2 * math.pi * i / 48
        rr = R * (1 + 0.07 * math.sin(ang * 5 + t * 3) + 0.04 * math.sin(ang * 9 - t * 4))
        pts.append((s(cx + rr * math.cos(ang)), s(cy + rr * math.sin(ang))))
    d.polygon(pts, fill=hexc(col, a))

def tree(d, x, y, k, col='#46c46a'):
    d.rectangle([s(x - 12), s(y - 60), s(x + 12), s(y)], fill=hexc('#8a5a3c'))
    circle(d, x, y - 110 * k - 20 * (1 - k), 70 * k, fill=hexc(col))

def car(d, x, y, col):
    d.rounded_rectangle([s(x - 90), s(y - 40), s(x + 90), s(y + 20)], radius=s(18), fill=hexc(col))
    d.rounded_rectangle([s(x - 50), s(y - 80), s(x + 45), s(y - 30)], radius=s(14), fill=hexc(col))
    for wx in (-50, 50): circle(d, x + wx, y + 25, 24, fill=hexc('#222222'))

def house(d, x, y, col):
    d.rectangle([s(x - 80), s(y - 110), s(x + 80), s(y)], fill=hexc(col))
    d.polygon([(s(x - 100), s(y - 110)), (s(x + 100), s(y - 110)), (s(x), s(y - 200))], fill=hexc('#c0392b'))
    d.rectangle([s(x - 20), s(y - 60), s(x + 20), s(y)], fill=hexc('#5a3a22'))

def earth(d, cx, cy, r):
    circle(d, cx, cy, r, fill=hexc('#2f7de1'))
    d.ellipse([s(cx - r * 0.55), s(cy - r * 0.6), s(cx + r * 0.05), s(cy - r * 0.05)], fill=hexc('#46c46a'))
    d.ellipse([s(cx + r * 0.1), s(cy + r * 0.05), s(cx + r * 0.6), s(cy + r * 0.55)], fill=hexc('#46c46a'))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#15171c'); header(d, hexc('#b8bec9'))
    goo(d, 540, 650, 200 + 15 * math.sin(t * 2), t)
    for i, (x, y) in enumerate(((470, 610), (610, 600))):
        circle(d, x, y, 22, fill=hexc('#ffffff')); circle(d, x + 4 * math.sin(t * 2), y + 4, 10, fill=hexc('#15171c'))
    text_block(img, ["Et si la fin du monde ressemblait… à une grosse flaque grise ?"], t, 1080, '#ffffff', size=78)

def sc_tiny(img, d, t, D):
    bg(d, '#123a3a'); header(d, hexc('#8ff0dc'))
    cell(d, 540, 690, 230, '#8ff0dc')
    k = ease((t - 0.6) / 0.6)
    if k > 0:
        bot(d, 440 + 30 * math.sin(t * 2), 770, 34 * k, t)
    ctext(d, "une cellule", 345, 44, '#8ff0dc', FM)
    text_block(img, ["Imaginez des robots minuscules. Plus petits qu'une seule de vos cellules."], t, 1060, '#ffffff', size=70)

random.seed(10)
ATOMS = [(random.uniform(120, 960), random.uniform(360, 940), random.choice(('#ff6f6f', '#ffd23a', '#6fb6ff'))) for _ in range(26)]
def sc_build(img, d, t, D):
    bg(d, '#2a1d4a'); header(d, hexc('#d2b8ff'))
    k = ease((t - 0.4) / 2.6)
    for i, (x, y, col) in enumerate(ATOMS):
        gx = 380 + (i % 6) * 64; gy = 520 + (i // 6) * 64
        circle(d, x + (gx - x) * k, y + (gy - y) * k, 24, fill=hexc(col))
    bot(d, 540 + 260 * math.cos(t * 1.5), 640 + 230 * math.sin(t * 1.5), 40, t)
    text_block(img, ["Ils assemblent la matière atome par atome (nanotechnologie). Comme des Lego… mais en tout petit."], t, 1060, '#ffffff', size=64)

def sc_copy(img, d, t, D):
    bg(d, '#0e2a4a'); header(d, hexc('#9fd0ff'))
    k = ease((t - 0.8) / 1.0)
    bot(d, 540 - 170 * k, 640, 90, t)
    if k > 0:
        bot(d, 540 + 170 * k, 640, 90 * k, t, a=int(255 * k), phase=1.0)
    text_block(img, ["Mais imaginez qu'on leur apprenne un truc de plus : fabriquer une copie d'eux-mêmes."], t, 1060, '#ffffff', size=66)

def sc_double(img, d, t, D):
    bg(d, '#3a2410'); header(d, hexc('#ffd28a'))
    steps = min(6, int(t / 0.55))
    n = 2 ** steps
    cols = int(math.ceil(math.sqrt(n * 1.4)))
    rows = int(math.ceil(n / cols))
    r = min(70, 470 / (3.2 * rows), 880 / (3.2 * cols))
    for i in range(n):
        x = 540 + (i % cols - (cols - 1) / 2) * r * 3.2
        y = 700 + (i // cols - (rows - 1) / 2) * r * 3.2
        bot(d, x, y, r, t, phase=i)
    big = int(min(1e9, 2 ** (t * 7.2)))
    ctext(d, f"{big:,}".replace(",", " "), 330, 60, '#ffd28a', FBK)
    text_block(img, ["Chaque copie se copie à son tour. 2, 4, 8, 16… Très vite : des milliards."], t, 1060, '#ffffff', size=68)

def sc_eat(img, d, t, D):
    bg(d, '#16361f'); header(d, hexc('#a8f0c0'))
    k = max(0.0, min(1.0, (t - 0.4) / 3.6))
    gx = 20 + 1000 * k
    items = [('tree', 220), ('car', 540), ('house', 860)]
    for i, (kind, x) in enumerate(items):
        if gx < x:
            if kind == 'tree': tree(d, x, 880, 1)
            elif kind == 'car': car(d, x, 860, '#ff6f6f')
            else: house(d, x, 880, '#f4ead2')
    goo(d, gx - 60, 830, 70 + 90 * k, t)
    for j in range(4):
        bot(d, gx - 120 + j * 45, 620 + 25 * math.sin(t * 4 + j), 22, t, phase=j)
    text_block(img, ["Pour se copier, il leur faut de la matière. Alors ils mangent tout : arbres, voitures, maisons…"], t, 1060, '#ffffff', size=64)

def sc_boom(img, d, t, D):
    bg(d, '#05060a'); stars(d, t); header(d, hexc('#b8bec9'))
    earth(d, 540, 650, 260)
    k = ease((t - 0.3) / 2.2)
    if k > 0:
        goo(d, 540, 650, 270 * k + 10, t, a=int(255 * min(1, k * 1.3)))
    text_block(img, ["Résultat : toute la planète transformée en gelée grise. Fin.",
                     ("L'idée vient de l'ingénieur Eric Drexler, en 1986.", 2.2)], t, 1040, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#e9f6ff'); header(d, hexc('#2f5f8a'))
    d.rounded_rectangle([s(330), s(330), s(750), s(930)], radius=s(30), fill=hexc('#ffffff'), outline=hexc('#2f5f8a'), width=s(12))
    for y in (520, 720): d.line([(s(345), s(y)), (s(735), s(y))], fill=hexc('#2f5f8a'), width=s(8))
    d.rounded_rectangle([s(390), s(780), s(520), s(900)], radius=s(18), fill=hexc('#d9e6ef'))
    goo(d, 455, 800, 55 + 5 * math.sin(t * 3), t, col='#7d8a6a')
    for i, (x, y) in enumerate(((440, 795), (472, 790))):
        circle(d, x, y, 9, fill=hexc('#ffffff')); circle(d, x, y + 2, 4, fill=hexc('#222222'))
    text_block(img, ["Une gelée grise qui grossit toute seule ?", ("On a tous ça au fond du frigo après les vacances.", 1.5)], t, 1030, '#16324a', size=68)

def sc_regret(img, d, t, D):
    bg(d, '#3a1030'); header(d, hexc('#ffb3e0'))
    ctext(d, "2004", 420, 150, '#ffb3e0', FBK)
    k = ease((t - 0.6) / 0.5)
    if k > 0:
        d.rounded_rectangle([s(160), s(600), s(920), s(860)], radius=s(40), fill=hexc('#ffffff', int(235 * k)))
        ctext(d, "« J'aurais aimé ne jamais", 680, 50, '#3a1030', FB, k)
        ctext(d, "utiliser ce terme. »", 760, 50, '#3a1030', FB, k)
    text_block(img, [("Mais en 2004, Drexler lui-même a regretté d'avoir inventé cette expression.", 1.0)], t, 1060, '#ffffff', size=66)

def sc_none(img, d, t, D):
    bg(d, '#102a3a'); header(d, hexc('#a9e1ff'))
    bot(d, 540, 640, 130, t, col='#7f8a99', eye='#55606e')
    k = ease((t - 0.6) / 0.4)
    if k > 0:
        circle(d, 540, 640, 260, outline=hexc('#ff4d5a'), width=s(22))
        a = math.pi / 4; R = 250 * k
        line(d, [(540 - R * math.cos(a), 640 - R * math.sin(a)), (540 + R * math.cos(a), 640 + R * math.sin(a))], '#ff4d5a', 22)
    text_block(img, ["Aucun robot capable de se copier tout seul n'existe.",
                     ("Et on n'en a même pas besoin pour fabriquer des objets.", 1.6)], t, 1060, '#ffffff', size=64)

def sc_detect(img, d, t, D):
    bg(d, '#3a1a0a'); header(d, hexc('#ffc58a'))
    goo(d, 540, 680, 150, t, col='#8a8f99')
    for i in range(3):
        r = 170 + ((t * 70 + i * 30) % 90)
        d.arc([s(540 - r), s(680 - r), s(540 + r), s(680 + r)], 200, 340, fill=hexc('#ff7a1a', 200), width=s(10))
    ctext(d, "ÇA CHAUFFE !", 330, 64, '#ffc58a', FBK)
    text_block(img, ["Un calcul publié en 2000 le montre : une telle invasion chaufferait très vite. On la repérerait tôt."], t, 1060, '#ffffff', size=62)

sc_title = scene_title(["GELÉE", "GRISE"], "Scénario d'extinction n°10")
sc_end = scene_end("Bref : rien ne va vous dévorer. Sauf peut-être votre déclaration d'impôts.")

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_tiny, 4.2), (sc_build, 4.4), (sc_copy, 4.2),
    (sc_double, 4.2), (sc_eat, 4.4), (sc_boom, 4.8), (sc_joke, 4.4),
    (sc_regret, 4.6), (sc_none, 4.8), (sc_detect, 4.6), (sc_end, 4.6),
]
