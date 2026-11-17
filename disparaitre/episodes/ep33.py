"""Épisode 33 — Mythe : la Terre qui arrête de tourner.
Sources :
- Science Notes (A. Helmenstine, mise à jour mai 2025), « What would happen if the Earth stopped rotating » :
  vitesse du sol à l'équateur ≈ 1 670 km/h ; en cas d'arrêt brutal, l'atmosphère continue à cette vitesse
  (vents jusqu'à 1 670 km/h) ; les océans se regroupent vers les pôles et l'équateur se découvre ;
  sans rotation, 6 mois de jour puis 6 mois de nuit ; « la Terre ne va pas s'arrêter de tourner »
  (il faudrait quelque chose comme un choc avec une autre planète).
- Live Science (7 déc. 2016) et Stephenson, Morrison & Hohenkerk, Proc. Royal Society A (2016) :
  d'après des éclipses notées depuis 720 av. J.-C. (tablettes babyloniennes), la journée s'allonge
  d'environ 1,8 milliseconde par siècle, surtout à cause des marées dues à la Lune.
- CORDIS (Commission européenne) : « les journées s'allongent d'environ deux millisecondes par siècle ».
- Ouragan de catégorie 5 : vents soutenus ≥ 252 km/h (échelle de Saffir-Simpson).
"""
from engine import *

EPISODE = 33
BOOM_SCENE = 7
LEGENDE = """Épisode 33 : et si la Terre arrêtait de tourner ? 🌍🛑

À l'équateur, le sol file à environ 1 670 km/h. Si la Terre freinait d'un coup, l'air, lui, continuerait sur sa lancée. Bonne nouvelle : c'est un mythe. La Terre ralentit bien… d'environ 2 millisecondes par siècle (Proceedings of the Royal Society A, 2016).

On va tous disparaître… mais pas aujourd'hui.

#findumonde #terre #mythe #astronomie #physique #science #vulgarisation #apocalypse"""

# ---------- fil rouge : la petite Terre qui tourne ----------
CONT = [(0.0, -0.35, 0.30, 0.22), (1.3, 0.25, 0.26, 0.30), (2.6, -0.05, 0.22, 0.18), (3.9, 0.40, 0.28, 0.16), (5.0, -0.45, 0.20, 0.14)]

def earth(d, cx, cy, R, rot, ocean='#339af0', land='#51cf66', poles=0.0):
    """rot : angle de rotation (rad). poles : 0 = normal, 1 = océans regroupés aux pôles."""
    if poles <= 0:
        circle(d, cx, cy, R, fill=hexc(ocean))
        for (ph, lat, w, h) in CONT:
            a = ph + rot
            c = math.cos(a)
            if c <= 0.05: continue
            x = cx + R * math.sin(a) * math.cos(lat)
            y = cy + R * math.sin(lat)
            ww = R * w * c; hh = R * h
            d.ellipse([s(x - ww), s(y - hh), s(x + ww), s(y + hh)], fill=hexc(land))
    else:
        circle(d, cx, cy, R, fill=hexc(ocean))
        h = R * (0.75 - 0.4 * poles)
        n = 40
        right = [(cx + math.sqrt(max(0, R * R - (y - cy) ** 2)), y) for y in [cy - h + 2 * h * i / n for i in range(n + 1)]]
        left = [(2 * cx - x, y) for (x, y) in reversed(right)]
        d.polygon([(s(x), s(y)) for (x, y) in right + left], fill=hexc('#d9a95b'))
        circle(d, cx, cy, R * 0.07, fill=hexc('#a8742f'))
    circle(d, cx, cy, R, outline=hexc('#ffffff', 90), width=4)

def spin_arrow(d, cx, cy, R, t, col='#ffffff', a=255):
    off = (t * 40) % 360
    d.arc([s(cx - R - 40), s(cy - R * 0.35), s(cx + R + 40), s(cy + R * 0.35)], 20, 160, fill=hexc(col, a), width=s(8))
    x, y = cx - (R + 40) * math.cos(math.radians(20)), cy + R * 0.35 * math.sin(math.radians(160))
    d.polygon([(s(x - 28), s(y - 10)), (s(x + 12), s(y - 30)), (s(x + 8), s(y + 18))], fill=hexc(col, a))

def wind(d, t, col, n=14, speed=900, a=200):
    for i in range(n):
        y = 360 + (i * 47) % 580
        x = (t * speed + i * 173) % 1400 - 200
        line(d, [(x, y), (x + 140 + 40 * (i % 3), y)], hexc(col, a), 8)

def car(d, cx, cy, col='#ff6b6b'):
    d.rounded_rectangle([s(cx - 220), s(cy - 50), s(cx + 220), s(cy + 60)], radius=s(30), fill=hexc(col))
    d.rounded_rectangle([s(cx - 130), s(cy - 130), s(cx + 110), s(cy - 30)], radius=s(30), fill=hexc(col))
    d.rounded_rectangle([s(cx - 105), s(cy - 112), s(cx - 15), s(cy - 50)], radius=s(12), fill=hexc('#d0ebff'))
    d.rounded_rectangle([s(cx + 5), s(cy - 112), s(cx + 90), s(cy - 50)], radius=s(12), fill=hexc('#d0ebff'))
    for wx in (-130, 130):
        circle(d, cx + wx, cy + 65, 48, fill=hexc('#212529'))
        circle(d, cx + wx, cy + 65, 18, fill=hexc('#adb5bd'))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b1d3a'); stars(d, t); header(d, hexc('#a5d8ff'))
    u = min(t, 2.6)
    rot = 2.2 * u - 0.423 * u * u
    earth(d, 540, 640, 250, rot)
    text_block(img, ["Et si la Terre arrêtait de tourner… d'un coup ?"], t, 1090, '#ffffff', size=80)

def sc_speed(img, d, t, D):
    bg(d, '#123d5c'); header(d, hexc('#d0ebff'))
    earth(d, 540, 560, 210, t * 1.2)
    spin_arrow(d, 540, 560, 210, t)
    k = ease((t - 0.4) / 0.5)
    ctext(d, "1 670 km/h", 830, 92, '#ffd43b', FBK, k)
    text_block(img, [("En ce moment, la Terre tourne sur elle-même. À l'équateur, le sol file à environ 1 670 km/h.", 0.9)], t, 1040, '#ffffff', size=64)

def sc_feel(img, d, t, D):
    bg(d, '#2b2d42'); header(d, hexc('#edf2f4'))
    earth(d, 540, 600, 200, t * 1.2)
    # petite maison posée sur le globe, immobile pour nous
    d.rounded_rectangle([s(490), s(330), s(590), s(410)], radius=s(8), fill=hexc('#ffd8a8'))
    d.polygon([(s(475), s(335)), (s(540), s(280)), (s(605), s(335))], fill=hexc('#e8590c'))
    d.rectangle([s(527), s(365), s(553), s(410)], fill=hexc('#8a5a3c'))
    text_block(img, ["Et vous ne sentez rien, parce que tout tourne avec vous : le sol, l'air, la mer."], t, 1060, '#ffffff', size=66)

def sc_car(img, d, t, D):
    bg(d, '#3d1e4a'); header(d, hexc('#e5dbff'))
    stop = 1.4
    x = 140 + 300 * ease(t / stop) if t < stop else 440
    line(d, [(60, 900), (1020, 900)], '#9775fa', 8)
    car(d, x, 780)
    bx = x + 40 + (420 * ease((t - stop) / 0.5) if t > stop else 0)
    by = 600 - (90 * math.sin(min(1, max(0, (t - stop) / 0.5)) * math.pi) if t > stop else 0)
    d.rounded_rectangle([s(bx - 45), s(by - 45), s(bx + 45), s(by + 45)], radius=s(12), fill=hexc('#ffd43b'))
    text_block(img, ["C'est comme en voiture : quand on pile, tout ce qui n'est pas attaché continue tout droit."], t, 1060, '#ffffff', size=64)

def sc_oceans(img, d, t, D):
    bg(d, '#0c4a3e'); header(d, hexc('#c3fae8'))
    k = ease((t - 0.6) / 2.4)
    earth(d, 540, 620, 260, 0, poles=max(0.001, k))
    text_block(img, ["Même en freinant tout doucement, les océans glisseraient vers les pôles.", ("L'équateur deviendrait un immense désert.", 2.2)], t, 1030, '#ffffff', size=62)

def sc_day(img, d, t, D):
    bg(d, '#4a3412'); header(d, hexc('#ffec99'))
    circle(d, 540, 620, 250, fill=hexc('#1c2541'))
    d.pieslice([s(290), s(370), s(790), s(870)], 270, 90, fill=hexc('#ffd43b'))
    k = ease((t - 0.3) / 0.4)
    f = font(FBK, 60)
    d.text((s(665) - f.getlength("JOUR") / 2, s(590)), "JOUR", font=f, fill=hexc('#4a3412', int(255 * k)))
    d.text((s(415) - f.getlength("NUIT") / 2, s(590)), "NUIT", font=f, fill=hexc('#ffec99', int(255 * k)))
    text_block(img, ["Et une journée durerait un an : 6 mois de soleil, puis 6 mois de nuit."], t, 1060, '#ffffff', size=68)

def sc_boom(img, d, t, D):
    k = ease((t - 0.3) / 1.0)
    r = int(0x12 + (0x6b - 0x12) * k); g = int(0x3d + (0x1a - 0x3d) * k); b = int(0x5c + (0x1a - 0x5c) * k)
    bg(d, '#%02x%02x%02x' % (r, g, b)); header(d, hexc('#ffc9c9'))
    shake = 10 * math.sin(t * 50) * k
    earth(d, 540 + shake, 640, 220, 0.4)
    wind(d, t, '#ffffff', a=int(220 * k), speed=1300)
    text_block(img, ["Mais si l'arrêt était brutal, l'air continuerait, lui, à 1 670 km/h.", ("Des vents 6 fois plus forts que le pire ouragan. Tout serait rasé.", 2.0)], t, 1030, '#ffffff', size=62)

def sc_joke(img, d, t, D):
    bg(d, '#f8f9fa'); header(d, hexc('#495057'))
    d.rounded_rectangle([s(290), s(360), s(790), s(900)], radius=s(30), fill=hexc('#ffffff'), outline=hexc('#343a40'), width=s(10))
    d.rectangle([s(290), s(360), s(790), s(480)], fill=hexc('#e03131'))
    ctext(d, "LUNDI", 385, 70, '#ffffff', FBK)
    k = ease((t - 0.4) / 0.6)
    ctext(d, "1", 520, 200, '#212529', FBK)
    ctext(d, "→ 182 jours", 790, 52, '#e03131', FB, k)
    text_block(img, ["Petit détail : un jour qui dure 6 mois…", ("…ça veut dire un lundi de 6 mois.", 1.5)], t, 1030, '#212529', size=68)

def sc_myth(img, d, t, D):
    bg(d, '#0f3d3e'); header(d, hexc('#96f2d7'))
    earth(d, 540, 560, 190, t * 1.2)
    k = ease((t - 0.3) / 0.4)
    w, h = 300, 110
    d.rounded_rectangle([s(540 - w / 2), s(780), s(540 + w / 2), s(780 + h)], radius=s(20), outline=hexc('#ff6b6b', int(255 * k)), width=s(10))
    ctext(d, "MYTHE", 795, 70, '#ff6b6b', FBK, k)
    text_block(img, [("Bonne nouvelle : c'est un mythe. Rien, dans notre coin de l'espace, ne peut freiner la Terre comme ça.", 0.8)], t, 1030, '#ffffff', size=62)

def sc_moon(img, d, t, D):
    bg(d, '#1b1f3b'); stars(d, t); header(d, hexc('#bac8ff'))
    earth(d, 430, 620, 190, t * 1.2)
    a = t * 0.5
    circle(d, 430 + 360 * math.cos(a), 620 + 120 * math.sin(a), 55, fill=hexc('#ced4da'))
    text_block(img, ["La Terre ralentit quand même un tout petit peu, freinée par les marées que provoque la Lune."], t, 1060, '#ffffff', size=64)

def sc_ms(img, d, t, D):
    bg(d, '#24163d'); header(d, hexc('#d0bfff'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "≈ 2 ms", 400, 170, '#ffffff', FBK, k)
    ctext(d, "par siècle, sur la durée d'une journée", 620, 44, '#d0bfff', FM, ease((t - 0.6) / 0.4))
    text_block(img, [("Des éclipses notées depuis 2 700 ans le confirment : la journée s'allonge d'environ 2 millisecondes par siècle.", 1.0)], t, 1000, '#ffffff', size=60)

def sc_science(img, d, t, D):
    bg(d, '#16402a'); header(d, hexc('#b2f2bb'))
    k = ease((t - 0.3) / 0.5)
    ctext(d, "Dans 5 milliards d'années", 420, 62, '#ffffff', FBK, k)
    ctext(d, "le Soleil gonflera…", 520, 46, '#b2f2bb', FM, k)
    earth(d, 540, 760, 110, t * 1.2)
    text_block(img, [("Verdict des scientifiques : la Terre tournera encore bien après la fin du Soleil tel qu'on le connaît.", 1.0)], t, 1030, '#ffffff', size=60)

sc_title = scene_title(["LA TERRE", "S'ARRÊTE"], "Scénario d'extinction n°33", color='#1864ab')
sc_end = scene_end("Bref : la Terre continuera de tourner. Et vos impôts de tomber.", color='#1864ab')

SCENES = [
    (sc_hook, 3.0), (sc_title, 2.4), (sc_speed, 4.2), (sc_feel, 3.4), (sc_car, 4.0),
    (sc_oceans, 4.4), (sc_day, 3.6), (sc_boom, 4.8), (sc_joke, 3.8), (sc_myth, 4.2),
    (sc_moon, 3.4), (sc_ms, 4.6), (sc_science, 4.6), (sc_end, 4.6),
]
