"""Épisode 38 — Le fusil à clathrates (le méthane des fonds marins).
Sources :
- USGS, communiqué « Gas hydrate breakdown unlikely to cause massive greenhouse gas release » (9 fév. 2017),
  sur la revue de C. Ruppel (USGS) et J. Kessler (Univ. de Rochester), Reviews of Geophysics, 2017 :
  l'hydrate de méthane est une forme « semblable à de la glace » de méthane et d'eau, stable seulement
  dans une plage étroite de pression et de température ; on le trouve sous le fond des océans (au-delà de
  300 à 500 m d'eau environ) et dans / sous le pergélisol ; « la plupart du méthane libéré par les hydrates
  n'atteint jamais l'atmosphère » : il reste dans les sédiments, se dissout dans l'océan ou est transformé
  en CO2 par des microbes ; pas de preuve concluante que ce méthane atteigne l'air aujourd'hui ; l'étude
  remet en cause l'idée d'un relâchement catastrophique. (Repris à l'identique par ScienceDaily.)
- Wikipédia (en), « Clathrate gun hypothesis », citant : Kennett, Cannariato, Hendy et Behl (2003),
  « Methane Hydrates in Quaternary Climate Change: The Clathrate Gun Hypothesis » ; GIEC AR6 (GT1, ch. 5) :
  stock estimé entre 1 500 et 2 000 Gt de carbone ; il est « très improbable » que les clathrates
  provoquent un écart détectable de la trajectoire des émissions au cours de ce siècle ; Archer (2007) : il
  faut environ mille ans ou plus pour que le réchauffement atteigne les hydrates ; Maximum thermique du
  Paléocène-Éocène (~56 millions d'années, +5 à 8 °C) : le rôle des hydrates y est discuté, non prouvé ;
  méthane : pouvoir de réchauffement ~72 fois celui du CO2 sur 20 ans, durée de vie ~12 ans.
"""
from engine import *

EPISODE = 38
BOOM_SCENE = 6
LEGENDE = """Épisode 38 : le fusil à clathrates 🧊💨

Sous le fond des océans dort une glace étrange qui emprisonne du méthane, un gaz qui réchauffe des dizaines de fois plus que le CO2. En 2003, des chercheurs ont imaginé un « coup de fusil » : la mer chauffe, la glace fond, le méthane jaillit et réchauffe encore plus. Bonne nouvelle : selon l'USGS (2017), la plupart de ce méthane n'atteint jamais l'air, et le GIEC juge un effet visible ce siècle « très improbable ».

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #climat #methane #ocean #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def mix(c1, c2, k):
    a, b = hexc(c1), hexc(c2)
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)) + (255,)

random.seed(38)
BUB = [(random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8), random.uniform(7, 14)) for _ in range(5)]

def hydrate(d, cx, cy, size, t, melt=0.0, col='#e8f6ff'):
    """Le fil rouge : un bloc de glace avec des bulles de méthane prisonnières."""
    h = size * (1 - 0.6 * melt)
    d.rounded_rectangle([s(cx - size), s(cy + size - 2 * h), s(cx + size), s(cy + size)], radius=s(size * 0.25),
                        fill=hexc(col), outline=hexc('#9fd3ff'), width=s(6))
    for i, (x, y, r) in enumerate(BUB):
        py = cy + size - h + y * h * 0.75 + 3 * math.sin(t * 2 + i)
        circle(d, cx + x * size * 0.75, py, r * size / 90, fill=hexc('#ffb347'))

def seafloor(d, t, top='#0b4f7a', bottom='#06263d', ground='#5a4632', gy=820):
    d.rectangle([0, s(260), s(W), s(gy)], fill=hexc(top))
    d.rectangle([0, s(gy - 220), s(W), s(gy)], fill=hexc(bottom))
    pts = [(x, gy + 12 * math.sin(x / 90 + 1)) for x in range(0, W + 40, 40)]
    d.polygon([(s(x), s(y)) for x, y in pts] + [(s(W), s(980)), (0, s(980))], fill=hexc(ground))

def bubbles_up(d, cx, y0, y1, t, n=10, col='#ffb347', speed=180, spread=120):
    for i in range(n):
        ph = (t * speed + i * (y0 - y1) / n) % (y0 - y1)
        x = cx + spread * math.sin(i * 2.3) + 10 * math.sin(t * 4 + i)
        circle(d, x, y0 - ph, 10 + (i % 3) * 4, fill=hexc(col))

def thermo(d, cx, cy, level, col='#ff4d4d'):
    d.rounded_rectangle([s(cx - 26), s(cy - 260), s(cx + 26), s(cy + 150)], radius=s(26), fill=hexc('#f3ead6'))
    circle(d, cx, cy + 170, 52, fill=hexc(col))
    top = cy + 150 - 380 * level
    d.rounded_rectangle([s(cx - 12), s(top), s(cx + 12), s(cy + 160)], radius=s(12), fill=hexc(col))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0a3550'); header(d, hexc('#9fd3ff'))
    seafloor(d, t, top='#0e5a86', bottom='#0a3550')
    hydrate(d, 540, 760, 90, t)
    for i in range(3):
        circle(d, 300 + i * 240, 420 + 20 * math.sin(t * 2 + i), 8, fill=hexc('#cfefff'))
    text_block(img, ["Et si la fin du monde dormait… dans un glaçon au fond de la mer ?"], t, 1080, '#ffffff', size=72)

def sc_what(img, d, t, D):
    bg(d, '#123b5c'); header(d, hexc('#bfe6ff'))
    k = ease(t / 1.2)
    hydrate(d, 540, 620, 120 + 60 * k, t)
    text_block(img, ["Sous le fond des océans, il y a une glace bizarre.", ("De l'eau qui emprisonne du méthane (un « hydrate »).", 1.3)], t, 1040, '#ffffff', size=64)

def sc_where(img, d, t, D):
    bg(d, '#1d2f4a'); header(d, hexc('#a6c8ff'))
    # pression = flèches qui appuient, froid = flocons
    hydrate(d, 540, 680, 120, t)
    for i in range(4):
        x = 330 + i * 140; y = 330 + 14 * math.sin(t * 3 + i)
        line(d, [(x, y), (x, y + 90)], '#ffd166', 12)
        d.polygon([(s(x - 22), s(y + 80)), (s(x + 22), s(y + 80)), (s(x), s(y + 115))], fill=hexc('#ffd166'))
    for i in range(6):
        a = t * 0.8 + i
        cx, cy = 540 + 280 * math.cos(a), 690 + 220 * math.sin(a)
        for j in range(3):
            ang = j * math.pi / 3
            line(d, [(cx - 18 * math.cos(ang), cy - 18 * math.sin(ang)), (cx + 18 * math.cos(ang), cy + 18 * math.sin(ang))], '#ffffff', 5)
    text_block(img, ["Elle ne tient que grâce au froid et à la pression.", ("Sous des centaines de mètres d'eau… ou dans le sol gelé de l'Arctique.", 1.3)], t, 1040, '#ffffff', size=60)

def sc_stock(img, d, t, D):
    bg(d, '#2a2350'); header(d, hexc('#cdbfff'))
    n = int(1 + 14 * ease(t / 2.6))
    for i in range(n):
        r, c = divmod(i, 5)
        hydrate(d, 300 + c * 120, 420 + r * 150, 48, t + i)
    kk = ease((t - 0.3) / 0.4)
    text_block(img, ["Et il y en a beaucoup : entre 1 500 et 2 000 milliards de tonnes de carbone.", ("Estimation du GIEC (les experts climat de l'ONU).", 1.6)], t, 1020, '#ffffff', size=60)

def sc_potent(img, d, t, D):
    bg(d, '#4a2a12'); header(d, hexc('#ffd59e'))
    # balance : 1 bulle de méthane contre une pile de bulles de CO2
    tilt = 40 * ease((t - 0.6) / 1.0)
    line(d, [(540, 520), (540, 860)], '#f3ead6', 14)
    line(d, [(300, 520 + tilt), (780, 520 - tilt)], '#f3ead6', 12)
    circle(d, 300, 470 + tilt, 46, fill=hexc('#ffb347'))
    for i in range(6):
        circle(d, 720 + (i % 3) * 40 - 40, 500 - tilt - (i // 3) * 38, 18, fill=hexc('#bbbbbb'))
    text_block(img, ["Or le méthane réchauffe la planète des dizaines de fois plus que le CO2…", ("…du moins pendant ses 20 premières années dans l'air.", 1.5)], t, 1030, '#ffffff', size=60)

def sc_gun(img, d, t, D):
    bg(d, '#5c0f14'); header(d, hexc('#ffb3b3'))
    seafloor(d, t, top='#8a1f1f', bottom='#5c0f14', ground='#3d2a1c')
    melt = ease((t - 0.4) / 1.8)
    hydrate(d, 540, 760, 90, t, melt=melt)
    if t > 1.0:
        bubbles_up(d, 540, 700, 330, t, n=14, speed=320, spread=160)
    kk = ease((t - 2.0) / 0.3)
    if kk > 0:
        ctext(d, "PAN !", 330, 120, '#ffd166', FBK, kk)
    text_block(img, ["L'idée (2003) : la mer chauffe, la glace fond, le méthane jaillit…", ("…et réchauffe encore plus. Le « fusil » est parti.", 1.9)], t, 1040, '#ffffff', size=62)

def sc_past(img, d, t, D):
    bg(d, '#2f4a1e'); header(d, hexc('#cfe8a8'))
    lvl = 0.25 + 0.45 * ease((t - 0.4) / 2.4)
    thermo(d, 540, 620, lvl)
    kk = ease((t - 0.2) / 0.4)
    ctext(d, "-56 000 000 ANS", 300, 50, '#ffd166', FBK, kk)
    text_block(img, ["Il y a 56 millions d'années, la Terre a pris 5 à 8 °C.", ("Le méthane des fonds marins est un suspect… jamais prouvé.", 1.5)], t, 1040, '#ffffff', size=62)

def sc_joke(img, d, t, D):
    bg(d, '#fff1c9'); header(d, hexc('#8a5a00'))
    # canette au soleil
    circle(d, 860, 380, 70, fill=hexc('#ffb000'))
    for i in range(8):
        a = i * math.pi / 4 + t
        line(d, [(860 + 90 * math.cos(a), 380 + 90 * math.sin(a)), (860 + 120 * math.cos(a), 380 + 120 * math.sin(a))], '#ffb000', 8)
    sw = 6 * math.sin(t * 20) * ease((t - 1.5) / 0.5)
    d.rounded_rectangle([s(430 + sw), s(480), s(650 + sw), s(880)], radius=s(40), fill=hexc('#d7263d'))
    d.rounded_rectangle([s(450 + sw), s(470), s(630 + sw), s(500)], radius=s(12), fill=hexc('#c0c0c0'))
    if t > 2.4:
        for i in range(10):
            ph = ((t - 2.4) * 400 + i * 30) % 150
            circle(d, 540 + 70 * math.sin(i * 1.7), 460 - ph, 12, fill=hexc('#ffffff'))
    text_block(img, ["Un peu comme la canette oubliée au soleil sur la plage arrière.", ("Ça chauffe, ça gonfle… pschitt.", 1.6)], t, 1040, '#3a2a00', size=60)

def sc_microbes(img, d, t, D):
    bg(d, '#0f3d2e'); header(d, hexc('#9fe3b0'))
    seafloor(d, t, top='#13604a', bottom='#0f3d2e', ground='#4a3a26')
    hydrate(d, 540, 760, 80, t, melt=0.3)
    for i in range(8):
        ph = (t * 150 + i * 50) % 400
        y = 680 - ph
        x = 540 + 120 * math.sin(i * 2.1)
        if y > 420:
            circle(d, x, y, 12, fill=hexc('#ffb347'))
        else:
            circle(d, x, y, 10, fill=hexc('#bbbbbb'))
    for i in range(4):
        x = 330 + i * 140 + 20 * math.sin(t * 2 + i); y = 450 + 15 * math.cos(t * 3 + i)
        d.rounded_rectangle([s(x - 26), s(y - 13), s(x + 26), s(y + 13)], radius=s(13), fill=hexc('#7ee081'))
    text_block(img, ["Mais ce méthane atteint rarement l'air : il se dissout dans l'eau…", ("…ou des microbes le mangent et le changent en CO2.", 1.6)], t, 1030, '#ffffff', size=60)

def sc_slow(img, d, t, D):
    bg(d, '#3a2a4a'); header(d, hexc('#e0c8ff'))
    seafloor(d, t, top='#4f3a66', bottom='#3a2a4a', ground='#5a4632', gy=560)
    hydrate(d, 540, 860, 70, t)
    k = ease(t / D) * 0.35
    y = 560 + 280 * k
    line(d, [(540, 580), (540, y)], '#ff6f61', 16)
    d.polygon([(s(515), s(y)), (s(565), s(y)), (s(540), s(y + 34))], fill=hexc('#ff6f61'))
    text_block(img, ["Et la chaleur met très longtemps à descendre jusqu'aux glaces profondes.", ("De l'ordre de mille ans, voire plus.", 1.6)], t, 1040, '#ffffff', size=60)

def sc_science(img, d, t, D):
    bg(d, '#14324f'); header(d, hexc('#a6d4ff'))
    hydrate(d, 540, 620, 110, t)
    kk = ease((t - 0.4) / 0.4)
    if kk > 0:
        d.rounded_rectangle([s(260), s(320), s(820), s(420)], radius=s(30), fill=hexc('#ffd166', int(255 * kk)))
        ctext(d, "TRÈS IMPROBABLE", 340, 56, '#14324f', FBK, kk)
    text_block(img, ["Le GIEC juge « très improbable » un effet visible d'ici 2100.", ("Le vrai souci reste le méthane et le CO2… que nous émettons.", 1.7)], t, 1030, '#ffffff', size=58)

sc_title = scene_title(["LE FUSIL", "À MÉTHANE"], "Scénario d'extinction n°38")
sc_end = scene_end("Bref : le fusil est enrayé, mais votre avis d'impôt, lui, part toujours à l'heure.")

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_what, 4.4), (sc_where, 4.4), (sc_stock, 4.4),
    (sc_potent, 4.2), (sc_gun, 4.8), (sc_past, 4.6), (sc_joke, 4.2),
    (sc_microbes, 4.6), (sc_slow, 4.2), (sc_science, 4.6), (sc_end, 4.8),
]
