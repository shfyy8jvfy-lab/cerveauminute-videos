"""Épisode 1 — Le faux vide."""
from engine import *

EPISODE = 1
BOOM_SCENE = 8
LEGENDE = """Épisode 1 : le faux vide 🫧

Et si l'univers tenait sur un réglage pas tout à fait stable ? C'est une vraie hypothèse de physique, proposée dès les années 70. Rassurez-vous : très, très improbable avant des milliards d'années.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #physique #univers #espace #vulgarisation #astrophysique #scienceenfrançais"""

# ---------- scenes ----------
def sc_bulb(img, d, t, D):
    d.rectangle([0, 0, W*S, H*S], fill=hexc('#0b0b10'))
    header(d, hexc('#f5c84c'))
    on = True
    if t > 1.3:
        on = int(t * 14) % 3 != 0 if t < 2.0 else False
    if on:
        for r, a in ((300, 18), (250, 30), (210, 50)):
            circle(d, 540, 640, r, fill=hexc('#f5c84c', a))
    circle(d, 540, 640, 170, fill=hexc('#f5c84c') if on else hexc('#2a2a30'))
    d.rectangle([s(470), s(800), s(610), s(900)], fill=hexc('#55555f'))
    for yy in (830, 865):
        d.rectangle([s(470), s(yy), s(610), s(yy + 8)], fill=hexc('#0b0b10'))
    text_block(img, ["Et si l'univers pouvait tomber en panne, d'un coup ?"], t, 1090, hexc('#ffffff'), size=82)

def valley_y(x):
    return 520 + 120 * math.exp(-((x - 330) / 110) ** 2) + 320 * math.exp(-((x - 760) / 130) ** 2) - 0.0003 * (x - 540) ** 2

def draw_valley(d, line_col, deep_hl=0.0):
    pts = [(s(x), s(valley_y(x))) for x in range(60, 1021, 6)]
    if deep_hl > 0:
        lvl = valley_y(560)
        poly = [(s(x), s(max(lvl, valley_y(x)))) for x in range(560, 961, 6)]
        d.polygon(poly, fill=hexc('#7cf2c8', int(70 * deep_hl)))
    d.line(pts, fill=line_col, width=s(10), joint='curve')

def sc_valley1(img, d, t, D):
    d.rectangle([0, 0, W*S, H*S], fill=hexc('#10233f'))
    header(d, hexc('#8fb8ff'))
    draw_valley(d, hexc('#8fb8ff'))
    bx = 330 + 18 * math.sin(t * 3.2) * math.exp(-t * 0.4)
    circle(d, bx, valley_y(bx) - 42, 36, fill=hexc('#ffffff'))
    text_block(img, ["Imaginez ce réglage comme une bille dans un petit creux. Ça a l'air stable…"], t, 1060, hexc('#ffffff'), size=74)

def sc_valley2(img, d, t, D):
    d.rectangle([0, 0, W*S, H*S], fill=hexc('#10233f'))
    header(d, hexc('#8fb8ff'))
    pulse = 0.55 + 0.45 * math.sin(t * 5)
    draw_valley(d, hexc('#8fb8ff'), deep_hl=ease(t / 0.6) * pulse)
    bx = 330 + 4 * math.sin(t * 9)
    circle(d, bx, valley_y(bx) - 42, 36, fill=hexc('#ffffff'))
    f = font(FB, 44)
    k = ease((t - 0.5) / 0.4)
    l = "le vrai fond"
    d.text((s(760) - f.getlength(l) / 2, s(valley_y(760) + 30)), l, font=f, fill=hexc('#7cf2c8', int(255 * k)))
    text_block(img, ["…mais il existe peut-être un creux bien plus profond juste à côté."], t, 1100, hexc('#ffffff'), size=74)

def sc_tip(img, d, t, D):
    d.rectangle([0, 0, W*S, H*S], fill=hexc('#10233f'))
    header(d, hexc('#8fb8ff'))
    k = ease((t - 0.6) / 1.3)
    bx = 330 + (760 - 330) * k
    landed = t > 1.9
    draw_valley(d, hexc('#8fb8ff'), deep_hl=1.0 if landed else 0.0)
    if landed:
        fl = max(0, 1 - (t - 1.9) / 0.5)
        circle(d, 760, valley_y(760) - 42, 36 + 200 * (1 - fl), fill=hexc('#ffffff', int(120 * fl)))
    hop = 90 * math.sin(math.pi * k) if 0 < k < 1 else 0
    circle(d, bx, valley_y(bx) - 42 - hop, 36, fill=hexc('#ffffff'))
    text_block(img, ["Si un jour la bille bascule, même à un seul endroit de l'univers…"], t, 1100, hexc('#ffffff'), size=74)

def sc_field(img, d, t, D):
    d.rectangle([0, 0, W*S, H*S], fill=hexc('#1d1236'))
    header(d, hexc('#c9a7ff'))
    for gx in range(9):
        for gy in range(7):
            x = 140 + gx * 100; y = 330 + gy * 100
            j = 6 * math.sin(t * 7 + gx * 1.3 + gy * 2.1)
            circle(d, x + j, y - j * 0.6, 11, fill=hexc('#c9a7ff'))
    text_block(img, ["Tout ce qui existe dépend d'un réglage invisible de l'univers.", "(les physiciens l'appellent le champ de Higgs)"], t, 1080, hexc('#ffffff'), size=70, stagger=1.4)

def sc_seed(img, d, t, D):
    d.rectangle([0, 0, W*S, H*S], fill=hexc('#000000'))
    stars(d, t)
    header(d, hexc('#9a9aa8'))
    if t > 0.3:
        k = ease((t - 0.3) / 0.3)
        p = 1 + 0.35 * math.sin(t * 10)
        circle(d, 540, 640, 60 * k * p, fill=hexc('#7a3cff', 60))
        circle(d, 540, 640, 16 * k, fill=hexc('#ffffff'))
    text_block(img, ["…une minuscule bulle apparaît, où les lois de la physique sont différentes."], t, 1060, hexc('#ffffff'), size=68)

def sc_bubble(img, d, t, D):
    d.rectangle([0, 0, W*S, H*S], fill=hexc('#000000'))
    stars(d, t + 4)
    r = 16 * math.exp(t / D * math.log(2400 / 16))
    circle(d, 540, 640, r + 30, fill=hexc('#ffffff', 40))
    circle(d, 540, 640, r, fill=hexc('#2a0b5e'), outline=hexc('#ffffff'), width=8)
    header(d, hexc('#d6c4ff'))
    text_block(img, ["Et elle grandit à la vitesse de la lumière. Elle avale tout."], t, 1150, hexc('#ffffff'), size=86)

def sc_alarm(img, d, t, D):
    d.rectangle([0, 0, W*S, H*S], fill=hexc('#2a0b5e'))
    header(d, hexc('#d6c4ff'))
    f = font(FBK, 150)
    l = "00:00"
    blink = int(t * 3) % 2 == 0
    d.text(((W*S - f.getlength(l)) / 2, s(520)), l, font=f, fill=hexc('#ff4d5a') if blink else hexc('#5a2a7a'))
    f2 = font(FM, 38); l2 = "temps de préavis"
    d.text(((W*S - f2.getlength(l2)) / 2, s(720)), l2, font=f2, fill=hexc('#d6c4ff'))
    text_block(img, ["On ne la verrait pas venir : rien ne va plus vite qu'elle pour nous prévenir."], t, 1050, hexc('#ffffff'), size=70)

def icon_atom(d, cx, cy, t, a):
    c = hexc('#7cf2c8', a)
    circle(d, cx, cy, 90, outline=c, width=5)
    circle(d, cx, cy, 20, fill=c)
    ang = t * 4
    circle(d, cx + 90 * math.cos(ang), cy + 90 * math.sin(ang), 12, fill=c)
    circle(d, cx + 90 * math.cos(ang + math.pi), cy + 90 * math.sin(ang + math.pi), 12, fill=c)

def icon_flask(d, cx, cy, t, a):
    c = hexc('#ffd166', a)
    d.rectangle([s(cx - 22), s(cy - 95), s(cx + 22), s(cy - 20)], outline=c, width=s(5))
    d.polygon([(s(cx - 22), s(cy - 20)), (s(cx + 22), s(cy - 20)), (s(cx + 85), s(cy + 85)), (s(cx - 85), s(cy + 85))], outline=c, width=s(5))
    for i in range(3):
        by = cy + 50 - ((t * 60 + i * 40) % 120)
        circle(d, cx - 20 + i * 20, by, 8, fill=c)

def icon_human(d, cx, cy, t, a):
    c = hexc('#ff8fa3', a)
    circle(d, cx, cy - 65, 28, fill=c)
    d.line([(s(cx), s(cy - 35)), (s(cx), s(cy + 35))], fill=c, width=s(9))
    wave_ = 25 * math.sin(t * 8)
    d.line([(s(cx), s(cy - 15)), (s(cx - 50), s(cy + 15))], fill=c, width=s(9))
    d.line([(s(cx), s(cy - 15)), (s(cx + 50), s(cy - 40 - wave_))], fill=c, width=s(9))
    d.line([(s(cx), s(cy + 35)), (s(cx - 35), s(cy + 95))], fill=c, width=s(9))
    d.line([(s(cx), s(cy + 35)), (s(cx + 35), s(cy + 95))], fill=c, width=s(9))

def sc_inside(img, d, t, D):
    d.rectangle([0, 0, W*S, H*S], fill=hexc('#14141c'))
    header(d, hexc('#9a9aa8'))
    times = [1.4, 2.4, 3.4]
    for i, (fn, x) in enumerate(zip((icon_atom, icon_flask, icon_human), (230, 540, 850))):
        k = ease((t - times[i] - 0.1) / 0.5)
        a = int(255 * (1 - k))
        if a > 0: fn(d, x, 620, t, a)
        if k > 0:
            c = hexc('#ff4d5a', int(255 * min(1, k * 2)) if k < 0.5 else int(255 * (1 - (k - 0.5) * 2)))
            d.line([(s(x - 100), s(520)), (s(x + 100), s(720))], fill=c, width=s(12))
    text_block(img, [("Dans la bulle :", 0.15), ("Plus d'atomes.", 1.4), ("Plus de chimie.", 2.4), ("Plus de nous.", 3.4)], t, 980, hexc('#ffffff'), size=70, gap=1.1)

def sc_coffee(img, d, t, D):
    bg = hexc('#f3e6d3')
    d.rectangle([0, 0, W*S, H*S], fill=bg)
    header(d, hexc('#8a5a3c'))
    c = hexc('#4a2c1d')
    d.rounded_rectangle([s(400), s(520), s(640), s(780)], radius=s(30), fill=c)
    d.ellipse([s(610), s(570), s(720), s(700)], outline=c, width=s(22))
    d.rectangle([s(360), s(780), s(680), s(800)], fill=c)
    for i in range(3):
        x0 = 450 + i * 70
        pts = []
        for j in range(30):
            yy = 490 - j * 6
            pts.append((s(x0 + 14 * math.sin(j * 0.35 + t * 5 + i)), s(yy)))
        d.line(pts, fill=hexc('#8a5a3c', 160), width=s(8))
    text_block(img, ["Le bon côté ? Ce serait instantané.", "Même pas le temps de finir votre café."], t, 1000, hexc('#2b1a10'), size=70, stagger=1.3)

def sc_proba(img, d, t, D):
    d.rectangle([0, 0, W*S, H*S], fill=hexc('#000000'))
    stars(d, t, fade_from=0.9, D=D)
    header(d, hexc('#9a9aa8'))
    f = font(FBK, 120); l = "INFIME"
    k = ease((t - 0.2) / 0.4)
    d.text(((W*S - f.getlength(l)) / 2, s(560)), l, font=f, fill=hexc('#7cf2c8', int(255 * k)))
    f2 = font(FM, 40); l2 = "probabilité que ça arrive"
    d.text(((W*S - f2.getlength(l2)) / 2, s(500)), l2, font=f2, fill=hexc('#9a9aa8', int(255 * k)))
    text_block(img, [("C'est une vraie hypothèse de physique. Mais sûrement pas avant que toutes les étoiles se soient éteintes.", 0.9)], t, 1060, hexc('#ffffff'), size=68)


sc_title = scene_title(["LE FAUX", "VIDE"], "Scénario d'extinction n°1")
sc_end = scene_end("Donc oui : vous devrez quand même payer vos impôts.")

SCENES = [
    (sc_bulb, 3.0), (sc_title, 2.2), (sc_field, 4.4), (sc_valley1, 3.6), (sc_valley2, 3.4),
    (sc_tip, 3.4), (sc_seed, 3.6), (sc_bubble, 3.4), (sc_alarm, 3.6),
    (sc_inside, 4.8), (sc_coffee, 4.4), (sc_proba, 5.2), (sc_end, 4.6),
]
