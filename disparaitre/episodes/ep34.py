"""Épisode 34 — Les trapps de Sibérie : la « Grande Mort » du Permien.
Sources :
- MIT News (J. Chu, 31 juil. 2017), sur Burgess, Muirhead & Bowring, Nature Communications (2017) :
  extinction il y a ~251,9 millions d'années ; 90 % des organismes marins et 75 % de la vie terrestre disparus ;
  le magma s'est étalé sous terre (sills) et a chauffé des sédiments riches en carbone, libérant CO2 et méthane ;
  réchauffement et acidification des océans ; volcanisme commencé ~300 000 ans avant l'extinction.
- Science News (T. Sumner, 28 août 2015), sur Burgess & Bowring, Science Advances (2015) :
  « plus de 3 millions de km³ de roche fondue » ; > 90 % des espèces marines, ~75 % des espèces terrestres ;
  rétablissement en environ 5 millions d'années.
- ScienceDaily / Univ. de Leeds (18 oct. 2012), sur Sun et al., Science (2012) : après l'extinction,
  surface de la mer ~40 °C sous les tropiques ; « zone morte » pendant ~5 millions d'années.
- Calcul : 3 000 000 km³ / 550 000 km² (France métropolitaine) ≈ 5,5 km d'épaisseur.
"""
from engine import *

EPISODE = 34
BOOM_SCENE = 7
LEGENDE = """Épisode 34 : la Grande Mort du Permien 🌋☠️

Il y a 252 millions d'années, des éruptions géantes en Sibérie ont vidé la planète : plus de 90 % des espèces marines et environ 75 % des espèces terrestres ont disparu. Le vrai coupable ? Le magma a chauffé des couches de charbon sous terre et libéré des montagnes de CO₂ et de méthane (MIT, Nature Communications 2017).

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #geologie #volcan #permien #extinction #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def volcano(d, cx, base, col, k, t, lava='#ff5a1f'):
    d.polygon([(s(cx - 260), s(base)), (s(cx - 70), s(base - 300)), (s(cx + 70), s(base - 300)), (s(cx + 260), s(base))], fill=hexc(col))
    if k > 0:
        for i in range(9):
            a = -math.pi / 2 + (i - 4) * 0.18
            r = 30 + (90 + 20 * math.sin(t * 6 + i)) * k
            circle(d, cx + r * math.cos(a) * 0.9, base - 300 + r * math.sin(a), 22 * k, fill=hexc(lava))
        d.polygon([(s(cx - 70), s(base - 300)), (s(cx + 70), s(base - 300)), (s(cx + 30 + 50 * k), s(base - 300 + 200 * k)), (s(cx - 30 - 50 * k), s(base - 300 + 200 * k))], fill=hexc(lava, 200))

def ground(d, t, heat=0.0, gas=0.0):
    """Coupe du sol : fil rouge de l'épisode."""
    d.rectangle([s(60), s(470), s(1020), s(540)], fill=hexc('#4a4a52'))          # lave en surface
    d.rectangle([s(60), s(540), s(1020), s(650)], fill=hexc('#a8845a'))          # roches
    coal = (0x1a + int(0x60 * heat), 0x1a, 0x1a)
    d.rectangle([s(60), s(650), s(1020), s(730)], fill=coal + (255,))            # charbon
    d.rectangle([s(60), s(730), s(1020), s(800)], fill=hexc('#a8845a'))
    w = 4 * math.sin(t * 3)
    d.rounded_rectangle([s(100), s(805 + w), s(980), s(860 + w)], radius=s(27), fill=hexc('#ff5a1f'))  # magma
    d.rectangle([s(500), s(860), s(580), s(950)], fill=hexc('#ff5a1f'))
    if heat > 0:
        for i in range(8):
            x = 150 + i * 110
            line(d, [(x, 800), (x + 12 * math.sin(t * 8 + i), 770), (x, 740)], hexc('#ffb347', int(220 * heat)), 8)
    if gas > 0:
        for i in range(14):
            x = 110 + (i * 67) % 880
            y = 640 - ((t * 120 + i * 47) % 330)
            circle(d, x, y, 18 + (i % 3) * 6, fill=hexc('#d9d9e3' if i % 2 else '#9fe3b0', int(200 * gas)))

def fish(d, cx, cy, col, dead=False, a=255):
    c = hexc(col, a)
    d.ellipse([s(cx - 50), s(cy - 26), s(cx + 40), s(cy + 26)], fill=c)
    d.polygon([(s(cx + 35), s(cy)), (s(cx + 70), s(cy - 26)), (s(cx + 70), s(cy + 26))], fill=c)
    if dead:
        line(d, [(cx - 32, cy - 10), (cx - 18, cy + 4)], hexc('#000000', a), 5)
        line(d, [(cx - 18, cy - 10), (cx - 32, cy + 4)], hexc('#000000', a), 5)
    else:
        circle(d, cx - 25, cy - 5, 6, fill=hexc('#000000', a))

def thermometer(d, cx, top, k, col='#ff4d5a'):
    d.rounded_rectangle([s(cx - 40), s(top), s(cx + 40), s(top + 480)], radius=s(40), fill=hexc('#ffffff'))
    circle(d, cx, top + 500, 75, fill=hexc('#ffffff'))
    circle(d, cx, top + 500, 55, fill=hexc(col))
    h = 60 + 380 * k
    d.rounded_rectangle([s(cx - 20), s(top + 470 - h), s(cx + 20), s(top + 500)], radius=s(20), fill=hexc(col))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#1a1220'); header(d, hexc('#ffb38a'))
    volcano(d, 540, 900, '#3b2a40', ease((t - 0.6) / 0.8), t)
    k = ease((t - 1.2) / 0.4)
    ctext(d, "?", 250, 130, '#ffb38a', FBK, k)
    text_block(img, ["La pire catastrophe de l'histoire de la vie n'est pas venue de l'espace…"], t, 1060, '#ffffff', size=72)

def sc_siberia(img, d, t, D):
    bg(d, '#13324a'); header(d, hexc('#a9d6ff'))
    d.rectangle([s(60), s(540), s(1020), s(950)], fill=hexc('#2f5a3a'))
    k = ease((t - 0.2) / 2.5)
    for i, x in enumerate((220, 540, 860)):
        kk = ease((t - 0.2 - i * 0.4) / 1.0)
        d.polygon([(s(x - 60), s(540)), (s(x - 15), s(470)), (s(x + 15), s(470)), (s(x + 60), s(540))], fill=hexc('#3b2a40'))
        if kk > 0:
            d.ellipse([s(x - 130 * kk), s(530), s(x + 130 * kk), s(560 + 200 * k)], fill=hexc('#ff5a1f', 230))
    text_block(img, ["Il y a 252 millions d'années, en Sibérie, la Terre s'est ouverte.", ("Et la lave a coulé pendant des centaines de milliers d'années.", 1.5)], t, 1030, '#ffffff', size=64)

def sc_volume(img, d, t, D):
    bg(d, '#2b1d3d'); header(d, hexc('#d6c2ff'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "3 000 000 km³", 400, 120, '#ffb38a', FBK, k)
    ctext(d, "de roche fondue", 560, 46, '#d6c2ff', FM, k)
    kk = ease((t - 1.2) / 1.2)
    d.rectangle([s(240), s(900 - 220 * kk), s(840), s(900)], fill=hexc('#ff5a1f'))
    d.rectangle([s(240), s(900), s(840), s(950)], fill=hexc('#6c8cff'))
    ctext(d, "FRANCE", 903, 36, '#ffffff', FB)
    if kk > 0.5: ctext(d, "5 km", 900 - 220 * kk + 70, 60, '#ffffff', FBK, ease((kk - 0.5) * 2))
    text_block(img, [("De quoi recouvrir toute la France sous 5 km de lave.", 1.3)], t, 1080, '#ffffff', size=72)

def sc_under(img, d, t, D):
    bg(d, '#2a2016'); header(d, hexc('#ffd59e'))
    ground(d, t, heat=ease((t - 1.0) / 1.2))
    text_block(img, ["Mais le pire se passait sous terre.", ("Le magma s'est glissé sous des couches de charbon… et les a fait cuire.", 1.2)], t, 1020, '#ffffff', size=64)

def sc_gas(img, d, t, D):
    bg(d, '#16302a'); header(d, hexc('#9fe3b0'))
    ground(d, t, heat=1.0, gas=ease((t - 0.2) / 0.8))
    text_block(img, ["Résultat : des montagnes de CO₂ et de méthane relâchées dans l'air."], t, 1060, '#ffffff', size=68)

def sc_heat(img, d, t, D):
    bg(d, '#3d2410'); header(d, hexc('#ffc28a'))
    thermometer(d, 360, 330, ease((t - 0.2) / 2.2))
    for i in range(3):
        y = 480 + i * 140
        ww = 8 * math.sin(t * 5 + i)
        line(d, [(540, y), (620, y - 20 + ww), (700, y), (780, y - 20 - ww), (860, y)], '#ff8a3d', 12)
    text_block(img, ["Effet de serre géant : la planète chauffe.", ("Et l'océan absorbe tellement de CO₂ qu'il devient plus acide.", 1.4)], t, 1030, '#ffffff', size=64)

random.seed(34)
FISH = [(random.uniform(150, 930), random.uniform(360, 900), random.random()) for _ in range(20)]
def sc_boom(img, d, t, D):
    bg(d, '#0e2a3a'); header(d, hexc('#8fd3ff'))
    for i, (x, y, r) in enumerate(FISH):
        dead = i < 18 and t > 0.5 + r * 2.0
        fish(d, x, y + (0 if dead else 8 * math.sin(t * 3 + i)), '#7a8a96' if dead else '#ffd166', dead=dead)
    n = int(min(90, 90 * ease((t - 0.3) / 2.2)))
    if t > 0.3:
        d.rounded_rectangle([s(320), s(560), s(760), s(720)], radius=s(30), fill=hexc('#0e2a3a', 220))
        ctext(d, f"{n} %", 565, 130, '#ff4d5a', FBK)
    text_block(img, ["Plus de 90 % des espèces marines disparaissent.", ("Et environ 3 espèces terrestres sur 4.", 1.6)], t, 1040, '#ffffff', size=66)

def sc_sea(img, d, t, D):
    bg(d, '#0f4c5c'); header(d, hexc('#a6f0ff'))
    for i in range(4):
        y = 620 + i * 70
        pts = [(80 + j * 46, y + 14 * math.sin(j * 0.6 + t * 3 + i)) for j in range(21)]
        line(d, pts, '#ff9a5a' if i == 0 else '#5fc4d8', 12)
    k = ease((t - 0.3) / 0.5)
    ctext(d, "≈ 40 °C", 380, 140, '#ffb38a', FBK, k)
    text_block(img, ["Après la catastrophe, la surface de la mer a atteint environ 40 °C sous les tropiques."], t, 1060, '#ffffff', size=64)

def sc_joke(img, d, t, D):
    bg(d, '#f2e8cf'); header(d, hexc('#7a5c2e'))
    d.rounded_rectangle([s(290), s(380), s(790), s(820)], radius=s(30), outline=hexc('#7a5c2e'), width=s(14))
    for i in range(7):
        x = 330 + i * 64
        d.rectangle([s(x), s(420), s(x + 54), s(470)], fill=hexc('#7a5c2e', 120))
    for r in range(5):
        for c in range(7):
            x = 330 + c * 64; y = 490 + r * 62
            if r * 7 + c < 22 + int(t * 3) % 6:
                line(d, [(x + 8, y + 8), (x + 46, y + 46)], '#c0392b', 7)
    text_block(img, ["La vie a mis environ 5 millions d'années à s'en remettre.", ("Et vous, vous trouvez que le lundi est long.", 1.6)], t, 1020, '#2b1a10', size=64)

def sc_rare(img, d, t, D):
    bg(d, '#14213d'); header(d, hexc('#b8c8ff'))
    volcano(d, 540, 900, '#3a4a6e', 0, t)
    for i in range(3):
        ph = (t * 0.6 + i / 3) % 1
        f = font(FBK, int(50 + 40 * i))
        d.text((s(650 + i * 70 + 20 * ph), s(560 - i * 90 - 60 * ph)), "z", font=f, fill=hexc('#b8c8ff', int(255 * (1 - ph))))
    text_block(img, ["Bonne nouvelle : ces éruptions géantes sont rarissimes.", ("Aucune n'a eu lieu depuis des millions d'années. Et rien n'en annonce une.", 1.4)], t, 1020, '#ffffff', size=62)

def sc_lesson(img, d, t, D):
    bg(d, '#1d3b1f'); header(d, hexc('#b6f0b0'))
    k = ease((t - 0.2) / 0.5)
    circle(d, 540, 620, 220 * k, fill=hexc('#2f8f5a'))
    for (x, y, r) in ((480, 560, 60), (610, 650, 70), (520, 700, 40)):
        circle(d, x, y, r * k, fill=hexc('#3fbf6f'))
    ctext(d, "CO₂", 360, 70, '#ffd166', FBK, ease((t - 0.8) / 0.4))
    text_block(img, ["La leçon des géologues : trop de CO₂, trop vite…", ("…c'est très mauvais pour la santé de la planète.", 1.5)], t, 1030, '#ffffff', size=64)

sc_title = scene_title(["LA GRANDE", "MORT"], "Scénario d'extinction n°34")
sc_end = scene_end("Bref : la vie a survécu à la Grande Mort. Vos impôts aussi, évidemment.")

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_siberia, 4.4), (sc_volume, 4.2), (sc_under, 4.4),
    (sc_gas, 3.8), (sc_heat, 4.4), (sc_boom, 4.6), (sc_sea, 4.0),
    (sc_joke, 4.6), (sc_rare, 4.8), (sc_lesson, 4.2), (sc_end, 4.8),
]
