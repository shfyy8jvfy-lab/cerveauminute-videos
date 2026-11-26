"""Épisode 50 — Mythe : la Lune qui tombe sur la Terre (elle s'éloigne en fait).
Sources :
- NASA JPL, « The Apollo Experiment That Keeps on Giving » (24 juil. 2019) : distance moyenne ~385 000 km ;
  la distance augmente de 3,8 cm par an ; les bourrelets de marée freinent la rotation de la Terre et tirent la Lune
  vers l'avant, ce qui la fait s'éloigner ; réflecteurs laissés par Apollo 11, 14 et 15.
- NASA Goddard, « Measuring the Moon's Distance » (Apollo Laser Ranging) : la Lune s'éloigne d'environ 3,8 cm/an ;
  premier réflecteur posé par Apollo 11 en 1969 ; les marées océaniques influencent l'orbite de la Lune.
- University of Texas Marine Science Institute, « Coral Moon » : il y a 300 millions d'années, l'année comptait
  environ 390 jours d'environ 22 heures (cernes de coraux fossiles) ; la cause, ce sont les marées.
Choix prudents : vitesse orbitale arrondie (« plus de 3 600 km/h », ~1 km/s) ; pas de date de « verrouillage »
Terre-Lune ; on dit clairement que c'est un mythe.
"""
from engine import *

EPISODE = 50
BOOM_SCENE = 8
LEGENDE = """Épisode 50 : et si la Lune nous tombait dessus ? 🌕😱

Mythe ! La Lune « tombe » en permanence, mais elle file de côté si vite qu'elle rate la Terre à chaque tour. Mieux : grâce aux miroirs laissés par les missions Apollo, on mesure au laser qu'elle s'éloigne de 3,8 cm par an (NASA). La faute aux marées, qui rallongent aussi nos journées.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #lune #mythe #espace #astronomie #science #vulgarisation #scienceenfrançais"""

# ---------- fil rouge : la Terre et la Lune ----------
EARTH_B = '#2f7fc1'; EARTH_G = '#4fbf6a'; MOON = '#e9e4d8'; MOON_D = '#bdb6a6'

def earth(d, cx, cy, r, t, a=255):
    circle(d, cx, cy, r, fill=hexc(EARTH_B, a))
    for (dx, dy, rr) in ((-0.35, -0.25, 0.32), (0.3, 0.2, 0.26), (0.05, -0.5, 0.18), (-0.2, 0.45, 0.2)):
        ox = dx + 0.08 * math.sin(t * 0.8)
        if abs(ox) + rr < 0.98:
            circle(d, cx + ox * r, cy + dy * r, rr * r, fill=hexc(EARTH_G, a))

def moon(d, cx, cy, r, a=255):
    circle(d, cx, cy, r, fill=hexc(MOON, a))
    for (dx, dy, rr) in ((-0.3, -0.2, 0.22), (0.35, 0.1, 0.16), (0.0, 0.45, 0.14), (0.2, -0.45, 0.1)):
        circle(d, cx + dx * r, cy + dy * r, rr * r, fill=hexc(MOON_D, a))

def arrow(d, x0, y0, x1, y1, col, w=10):
    line(d, [(x0, y0), (x1, y1)], col, w)
    ang = math.atan2(y1 - y0, x1 - x0)
    for da in (2.6, -2.6):
        line(d, [(x1, y1), (x1 + 36 * math.cos(ang + da), y1 + 36 * math.sin(ang + da))], col, w)

def dashed_circle(d, cx, cy, r, col, n=40):
    for i in range(n):
        a0 = i * 2 * math.pi / n; a1 = a0 + math.pi / n
        line(d, [(cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))], col, 5)

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b0f24'); stars(d, t); header(d, hexc('#ffe9a8'))
    earth(d, 540, 820, 150, t)
    k = ease(t / 3.0)
    shake = 6 * math.sin(t * 25) * k
    moon(d, 540 + shake, 340 + 260 * k, 70 + 50 * k)
    text_block(img, ["Et si, un beau matin, la Lune nous tombait dessus ?"], t, 1090, '#ffffff', size=80)

def sc_orbit(img, d, t, D):
    bg(d, '#16234a'); stars(d, t); header(d, hexc('#9fc2ff'))
    cx, cy, R = 540, 630, 260
    dashed_circle(d, cx, cy, R, '#5f78b8')
    earth(d, cx, cy, 110, t)
    a = -math.pi / 2 + t * 0.6
    mx, my = cx + R * math.cos(a), cy + R * math.sin(a)
    moon(d, mx, my, 48)
    k = ease((t - 0.8) / 0.5)
    if k > 0:
        arrow(d, mx, my, mx + (cx - mx) * 0.45 * k, my + (cy - my) * 0.45 * k, '#ff6f7a', 9)
    text_block(img, ["Surprise : la Lune tombe déjà vers nous.", ("Tout le temps.", 1.4)], t, 1060, '#ffffff', size=74)

def sc_sideways(img, d, t, D):
    bg(d, '#1f1240'); stars(d, t); header(d, hexc('#d2b8ff'))
    cx, cy, R = 540, 640, 260
    earth(d, cx, cy, 110, t)
    pts = []
    a0 = -math.pi / 2
    span = 2.6 * ease(t / 3.2)
    for i in range(40):
        a = a0 + span * i / 39
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    if len(pts) > 1:
        line(d, pts, '#8f7ad6', 6)
    mx, my = pts[-1]
    moon(d, mx, my, 48)
    a = a0 + span
    arrow(d, mx, my, mx - 120 * math.sin(a), my + 120 * math.cos(a), '#ffe066', 9)
    text_block(img, ["Mais elle file de côté à plus de 3 600 km/h. Elle tombe… et rate la Terre. À chaque tour."],
               t, 1060, '#ffffff', size=64)

def sc_mirror(img, d, t, D):
    bg(d, '#2a2a2a'); header(d, hexc('#dddddd'))
    d.rectangle([s(0), s(780), s(1080), s(950)], fill=hexc(MOON_D))
    for (x, r) in ((180, 40), (820, 55), (980, 25)):
        d.ellipse([s(x - r), s(820), s(x + r), s(850)], fill=hexc('#a59e8e'))
    k = ease((t - 0.3) / 0.6)
    y = 780 - 0 * k
    d.line([(s(470), s(780)), (s(500), s(700))], fill=hexc('#888888'), width=s(10))
    d.line([(s(610), s(780)), (s(580), s(700))], fill=hexc('#888888'), width=s(10))
    d.rounded_rectangle([s(420), s(560), s(660), s(710)], radius=s(12), fill=hexc('#555a66', int(255 * k)))
    for i in range(4):
        for j in range(3):
            glint = 0.5 + 0.5 * math.sin(t * 4 + i + j)
            d.rectangle([s(438 + i * 56), s(576 + j * 44), s(482 + i * 56), s(612 + j * 44)],
                        fill=hexc('#bfe3ff', int((120 + 135 * glint) * k)))
    text_block(img, ["En 1969, les astronautes d'Apollo 11 ont posé des miroirs sur la Lune."], t, 1060, '#ffffff', size=70)

def sc_laser(img, d, t, D):
    bg(d, '#2a0f3a'); stars(d, t); header(d, hexc('#7ff0e0'))
    earth(d, 220, 640, 120, t)
    moon(d, 880, 640, 70)
    k = (t * 0.9) % 1.0
    for back in (False, True):
        x0, x1 = (340, 810) if not back else (810, 340)
        kk = k * 2 if not back else (k - 0.5) * 2
        if 0 <= kk <= 1:
            x = x0 + (x1 - x0) * kk
            line(d, [(x - 60 if not back else x + 60, 640), (x, 640)], '#ff4d5a', 12)
    text_block(img, ["Depuis, on y tire des lasers pour mesurer la distance.", ("Au centimètre près.", 1.6)],
               t, 1060, '#ffffff', size=70)

def sc_away(img, d, t, D):
    bg(d, '#123040'); stars(d, t); header(d, hexc('#a8e6ff'))
    earth(d, 220, 640, 120, t)
    k = ease((t - 0.5) / 2.0)
    mx = 760 + 120 * k
    moon(d, mx, 640, 70)
    arrow(d, mx + 90, 640, mx + 90 + 80 * ease((t - 0.3) / 0.4), 640, '#ffe066', 10)
    ctext(d, "+3,8 cm par an", 450, 64, '#ffe066', FBK, ease((t - 0.8) / 0.4))
    text_block(img, ["Verdict : la Lune ne se rapproche pas. Elle s'éloigne !"], t, 1080, '#ffffff', size=74)

def sc_tides(img, d, t, D):
    bg(d, '#3a2a10'); stars(d, t); header(d, hexc('#ffe0a8'))
    cx, cy = 400, 640
    rot = t * 0.5
    bx = [(cx + 175 * math.cos(rot + q) * (1 if i % 2 == 0 else 0.86), cy + 145 * math.sin(rot + q))
          for i, q in enumerate([j * 2 * math.pi / 60 for j in range(60)])]
    d.ellipse([s(cx - 170), s(cy - 130), s(cx + 170), s(cy + 130)], fill=hexc('#5aa9e6', 140))
    earth(d, cx, cy, 120, t)
    moon(d, 880, 560, 60)
    k = ease((t - 1.2) / 0.5)
    if k > 0:
        arrow(d, 880, 560, 880 + 20 * k, 560 - 110 * k, '#ffe066', 9)
    text_block(img, ["Le coupable : les marées. Elles freinent la Terre…",
                     ("…et poussent la Lune vers l'avant, donc plus loin.", 1.8)], t, 1040, '#ffffff', size=64)

def sc_boom(img, d, t, D):
    bg(d, '#4a0d12'); stars(d, t); header(d, hexc('#ffb3bd'))
    earth(d, 220, 640, 120, t)
    k = ease((t - 0.3) / 2.5)
    shake = 6 * math.sin(t * 30) * max(0, 1 - t / 2)
    moon(d, 820 + 200 * k + shake, 640 - 120 * k, 70 - 30 * k)
    # petit mouchoir qui s'agite
    hx, hy = 330, 520
    wave = 20 * math.sin(t * 8)
    d.polygon([(s(hx), s(hy)), (s(hx + 70), s(hy - 30 + wave)), (s(hx + 60), s(hy + 40 + wave)), (s(hx + 5), s(hy + 50))],
              fill=hexc('#ffffff'))
    text_block(img, ["Le vrai scénario catastrophe ? La Lune nous quitte.",
                     ("Lentement. Sans même dire au revoir.", 1.6)], t, 1060, '#ffffff', size=70)

def sc_coral(img, d, t, D):
    bg(d, '#0d3b3a'); header(d, hexc('#a8f0e0'))
    k = ease((t - 0.2) / 0.6)
    for i in range(9):
        r = 40 + i * 30
        d.ellipse([s(540 - r * 1.3), s(640 - r * 0.85), s(540 + r * 1.3), s(640 + r * 0.85)],
                  outline=hexc('#ffb38a' if i % 2 else '#ffd9c2', int(255 * ease((t - 0.2 - i * 0.12) / 0.3))),
                  width=s(10))
    ctext(d, "390 jours", 310, 64, '#ffe066', FBK, ease((t - 1.4) / 0.4))
    text_block(img, ["La preuve : il y a 300 millions d'années, une année comptait 390 jours de 22 heures.",
                     ("Les coraux fossiles l'ont noté dans leurs cernes.", 2.2)], t, 1010, '#ffffff', size=58)

def sc_joke(img, d, t, D):
    bg(d, '#f6ead8'); header(d, hexc('#8a5a3c'))
    # une main simplifiée avec ongles qui poussent
    d.rounded_rectangle([s(360), s(620), s(720), s(900)], radius=s(60), fill=hexc('#ffd6a8'))
    g = ease(t / 3.5)
    for i in range(4):
        fx = 390 + i * 85
        d.rounded_rectangle([s(fx), s(400), s(fx + 70), s(680)], radius=s(35), fill=hexc('#ffd6a8'))
        d.rounded_rectangle([s(fx + 10), s(400 - 30 * g), s(fx + 60), s(470)], radius=s(22), fill=hexc('#ffffff'),
                            outline=hexc('#e0b48a'), width=s(4))
    text_block(img, ["3,8 cm par an, c'est à peu près la vitesse de vos ongles.",
                     ("Personne n'a jamais fait de film catastrophe sur une manucure.", 1.8)], t, 1010, '#2b1a10', size=62)

def sc_science(img, d, t, D):
    bg(d, '#22264d'); stars(d, t); header(d, hexc('#c8ccff'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "0 RISQUE", 470, 150, '#c8ccff', FBK, k)
    ctext(d, "qu'elle tombe sur la Terre", 640, 44, '#c8ccff', FM, k)
    text_block(img, ["Les astronomes sont formels : rien ne peut faire tomber la Lune sur nous.",
                     ("Ce qui l'éloigne, ce sont nos marées. Doucement.", 1.8)], t, 1000, '#ffffff', size=60)

def sc_later(img, d, t, D):
    bg(d, '#12301f'); stars(d, t); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "385 000 km", 470, 140, '#a8f0c0', FBK, k)
    ctext(d, "et quelques centimètres de plus chaque année", 640, 40, '#a8f0c0', FM, k)
    text_block(img, [("Elle restera dans notre ciel bien, bien plus longtemps que nous.", 0.8)], t, 1060, '#ffffff', size=68)

sc_title = scene_title(["LA LUNE", "TOMBE ?"], "Scénario d'extinction n°50", color='#3a3f8f')
sc_end = scene_end("Bref : la Lune ne vous tombera pas dessus. Votre avis d'imposition, si.", color='#3a3f8f')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_orbit, 4.2), (sc_sideways, 4.4), (sc_mirror, 4.0),
    (sc_laser, 4.4), (sc_away, 4.2), (sc_tides, 4.6), (sc_boom, 4.4),
    (sc_coral, 4.8), (sc_joke, 4.6), (sc_science, 4.6), (sc_end, 4.8),
]
