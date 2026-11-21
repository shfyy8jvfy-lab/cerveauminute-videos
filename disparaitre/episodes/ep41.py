"""Épisode 41 — Mythe : le noyau de la Terre qui s'arrête.
Sources :
- Yang & Song, « Multidecadal variation of the Earth's inner-core rotation », Nature Geoscience (23 janv. 2023),
  Université de Pékin ; résumé par Science News (23 janv. 2023) : vers 2009 la graine (noyau interne) a presque
  cessé de tourner par rapport au manteau ; oscillation possible d'environ 70 ans, précédent changement au début
  des années 1970 ; « pas susceptible d'avoir des effets profonds sur la vie » ; résultat discuté par d'autres
  chercheurs.
- USC / Nature (12 juin 2024, Wang, Vidale et al.) : la graine, boule solide de fer et de nickel « à peu près de la
  taille de la Lune » (Science News : ~70 % de la largeur de la Lune), entourée de fer-nickel liquide, ralentit depuis
  environ 2010 ; effet sur la durée du jour « de l'ordre d'un millième de seconde » ; « très probablement sans
  importance pour la vie en surface » (J. Vidale).
- Anzellini et al., Science (2013, ESRF) via Smithsonian / NBC News : centre de la Terre vers 6 000 °C, autant que la
  surface du Soleil.
- National Geographic Education, « Core » : le champ magnétique terrestre est produit par les mouvements du fer
  liquide du noyau externe.
"""
from engine import *

EPISODE = 41
BOOM_SCENE = 7
LEGENDE = """Épisode 41 : le noyau de la Terre s'est arrêté de tourner ?! 🌍🛑

En 2023, des chercheurs ont estimé que la boule de fer au centre de la Terre avait presque cessé de tourner par rapport au reste de la planète, vers 2009. Panique dans les gros titres… alors qu'il s'agit sans doute d'un va-et-vient d'environ 70 ans, qui change la durée du jour d'à peu près un millième de seconde (Nature Geoscience 2023, Nature 2024). Aucun danger pour la vie.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #terre #geologie #noyau #mythe #vulgarisation #scienceenfrançais"""

# ---------- fil rouge : la Terre coupée en deux ----------
def earth_cut(d, cx, cy, r, t, spin=1.0, core_glow=1.0, show_arrow=True):
    """Terre vue en coupe : croûte, manteau, noyau liquide, graine solide qui tourne."""
    circle(d, cx, cy, r, fill=hexc('#2f7fd8'))
    circle(d, cx, cy, r * 0.94, fill=hexc('#c0522b'))          # manteau
    circle(d, cx, cy, r * 0.55, fill=hexc('#f08a24'))          # noyau externe liquide
    # petites vagues dans le fer liquide
    for i in range(10):
        a = t * 0.8 + i * 2 * math.pi / 10
        rr = r * (0.43 + 0.04 * math.sin(t * 3 + i))
        circle(d, cx + rr * math.cos(a), cy + rr * math.sin(a), r * 0.025, fill=hexc('#ffc266', 200))
    ri = r * 0.3
    circle(d, cx, cy, ri, fill=hexc('#ffe27a', int(255 * core_glow) if core_glow < 1 else 255))  # graine
    a0 = t * 1.4 * spin
    for k in range(3):                                          # rayures pour voir la rotation
        a = a0 + k * 2 * math.pi / 3
        line(d, [(cx + ri * 0.2 * math.cos(a), cy + ri * 0.2 * math.sin(a)),
                 (cx + ri * 0.85 * math.cos(a), cy + ri * 0.85 * math.sin(a))], '#d9a400', 7)
    if show_arrow and spin != 0:
        ra = ri + r * 0.07
        st = math.degrees(a0) % 360
        d.arc([s(cx - ra), s(cy - ra), s(cx + ra), s(cy + ra)], st, st + 110, fill=hexc('#ffffff'), width=s(6))

def paper(d, x, y, w, h, title, k, col='#fffaf0', tcol='#b3121b', size=50):
    if k <= 0: return
    d.rounded_rectangle([s(x), s(y), s(x + w), s(y + h)], radius=s(16), fill=hexc(col, int(255 * k)))
    for i in range(2):
        line(d, [(x + 30, y + h - 36 - i * 30), (x + w - 30 - i * 40, y + h - 36 - i * 30)], '#bbbbbb', 8)
    f = font(FBK, size)
    d.text((s(x + 30), s(y + 24)), title, font=f, fill=hexc(tcol, int(255 * k)))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#14102e'); stars(d, t); header(d, hexc('#c9b8ff'))
    earth_cut(d, 540, 640, 260, t, spin=max(0, 1 - t / 2.5))
    ctext(d, "?!", 255, 90, '#ffd166', FBK, ease((t - 2.2) / 0.3))
    text_block(img, ["Le cœur de la Terre se serait arrêté de tourner. On est fichus ?"], t, 1080, '#ffffff', size=72)

def sc_ball(img, d, t, D):
    bg(d, '#3a1d12'); header(d, hexc('#ffc8a6'))
    k = ease(t / 1.2)
    earth_cut(d, 380, 640, 240 + 20 * k, t)
    # comparaison : la Lune
    circle(d, 860, 640, 95 * k, fill=hexc('#cfcfcf'))
    for (dx, dy, rr) in ((-30, -20, 18), (25, 30, 14), (20, -35, 10)):
        circle(d, 860 + dx * k, 640 + dy * k, rr * k, fill=hexc('#a8a8a8'))
    text_block(img, ["Au centre : une boule de fer et de nickel.", ("Un peu plus petite que la Lune.", 1.5)], t, 1040, '#ffffff', size=66)

def sc_hot(img, d, t, D):
    bg(d, '#5a1630'); header(d, hexc('#ffb3c8'))
    earth_cut(d, 380, 640, 240, t)
    # le Soleil à droite
    pulse = 1 + 0.05 * math.sin(t * 4)
    for i in range(12):
        a = i * math.pi / 6 + t * 0.5
        line(d, [(850 + 110 * math.cos(a), 640 + 110 * math.sin(a)), (850 + 150 * math.cos(a), 640 + 150 * math.sin(a))], '#ffd166', 10)
    circle(d, 850, 640, 90 * pulse, fill=hexc('#ffb020'))
    ctext(d, "=", 640 - 40, 90, '#ffffff', FBK, ease((t - 0.8) / 0.4))
    text_block(img, ["Elle est solide, et chauffée à environ 6 000 °C.", ("Autant que la surface du Soleil.", 1.5)], t, 1040, '#ffffff', size=64)

def sc_spin(img, d, t, D):
    bg(d, '#123a4a'); header(d, hexc('#a6e6f2'))
    earth_cut(d, 540, 640, 290, t, spin=1.6)
    text_block(img, ["Elle flotte dans un océan de fer liquide…", ("…et tourne un peu à son rythme, pas tout à fait comme le reste.", 1.5)], t, 1040, '#ffffff', size=62)

def sc_magnet(img, d, t, D):
    bg(d, '#0f2a1c'); header(d, hexc('#a8f0c0'))
    cx, cy = 540, 640
    k = ease(t / 1.5)
    for i in range(4):  # lignes du champ magnétique
        w = 260 + i * 70
        d.ellipse([s(cx - w * k), s(cy - 300), s(cx), s(cy + 300)], outline=hexc('#a8f0c0', 150 - i * 25), width=s(4))
        d.ellipse([s(cx), s(cy - 300), s(cx + w * k), s(cy + 300)], outline=hexc('#a8f0c0', 150 - i * 25), width=s(4))
    earth_cut(d, cx, cy, 190, t)
    text_block(img, ["C'est ce fer liquide qui fabrique notre champ magnétique.", ("Notre bouclier contre les particules du Soleil.", 1.6)], t, 1040, '#ffffff', size=62)

def sc_2023(img, d, t, D):
    bg(d, '#2a2f6a'); header(d, hexc('#c2c8ff'))
    earth_cut(d, 540, 660, 250, t, spin=max(0, 1 - t / 2.0))
    k = ease((t - 2.2) / 0.4)
    if k > 0:
        d.rounded_rectangle([s(340), s(280), s(740), s(380)], radius=s(26), fill=hexc('#ffd166', int(255 * k)))
        ctext(d, "≈ 2009", 292, 70, '#2a2f6a', FBK, k)
    text_block(img, ["En 2023, des chercheurs annoncent : vers 2009, la boule a presque arrêté de tourner.", ("Par rapport au reste de la planète.", 2.0)], t, 1040, '#ffffff', size=58)

def sc_boom(img, d, t, D):
    bg(d, '#7a1010'); header(d, hexc('#ffc0c0'))
    titles = ["LE NOYAU S'ARRÊTE !", "PANIQUE !", "LA FIN ?!"]
    for i, ti in enumerate(titles):
        k = ease((t - 0.2 - i * 0.45) / 0.3)
        wob = 8 * math.sin(t * 9 + i)
        paper(d, 90 + i * 70, 300 + i * 190 + wob, 760, 170, ti, k, size=58)
    text_block(img, ["Les gros titres s'affolent…", ("…et il ne se passe rien. Strictement rien.", 1.6)], t, 1040, '#ffffff', size=66)

def sc_swing(img, d, t, D):
    bg(d, '#3d2a5c'); header(d, hexc('#e0c8ff'))
    sp = math.sin(t * 1.6)
    earth_cut(d, 540, 600, 250, t, spin=sp, show_arrow=False)
    ctext(d, "≈ 70 ans", 900, 52, '#ffd166', FBK, ease((t - 0.6) / 0.4))
    text_block(img, ["En fait, elle ralentit puis accélère, comme un va-et-vient.", ("Peut-être tous les 70 ans. Dernier virage : les années 1970.", 1.7)], t, 1040, '#ffffff', size=58)

def sc_joke(img, d, t, D):
    bg(d, '#fbe9d0'); header(d, hexc('#8a4a00'))
    # une tasse de café
    d.rounded_rectangle([s(380), s(520), s(660), s(820)], radius=s(30), fill=hexc('#ffffff'))
    d.rectangle([s(395), s(535), s(645), s(580)], fill=hexc('#6b3e1e'))
    d.arc([s(620), s(590), s(760), s(740)], 270, 90, fill=hexc('#ffffff'), width=s(26))
    for i in range(3):
        y = 470 - ((t * 60 + i * 30) % 120)
        x = 440 + i * 80 + 12 * math.sin(t * 3 + i)
        line(d, [(x, y + 40), (x + 10, y)], '#c9a27a', 8)
    text_block(img, ["Effet sur vos journées : environ un millième de seconde.", ("Toujours pas assez pour finir votre café.", 1.7)], t, 1040, '#3a2200', size=60)

def sc_verdict(img, d, t, D):
    bg(d, '#14324f'); header(d, hexc('#a6d4ff'))
    earth_cut(d, 540, 600, 220, t)
    k = ease((t - 0.4) / 0.4)
    d.rounded_rectangle([s(300), s(860), s(780), s(940)], radius=s(24), fill=hexc('#4fbf6a', int(255 * k)))
    ctext(d, "AUCUN DANGER", 872, 52, '#ffffff', FBK, k)
    text_block(img, ["Verdict des scientifiques : aucun danger pour la vie.", ("Et l'idée fait encore débat entre chercheurs.", 1.7)], t, 1040, '#ffffff', size=60)

def sc_still(img, d, t, D):
    bg(d, '#1d3d2e'); header(d, hexc('#b8f0d0'))
    earth_cut(d, 540, 620, 280, t, spin=1.2)
    text_block(img, ["Le fer liquide continue de bouger, et notre bouclier magnétique avec.", ("La Terre tourne toujours, promis.", 1.7)], t, 1040, '#ffffff', size=60)

sc_title = scene_title(["LE NOYAU", "S'ARRÊTE"], "Scénario d'extinction n°41 · mythe")
sc_end = scene_end("Bref : le noyau fait une pause. Vos impôts, eux, n'en font jamais.")

SCENES = [
    (sc_hook, 3.6), (sc_title, 2.4), (sc_ball, 4.2), (sc_hot, 4.4), (sc_spin, 4.0),
    (sc_magnet, 4.6), (sc_2023, 4.6), (sc_boom, 4.2), (sc_swing, 4.8), (sc_joke, 4.6),
    (sc_verdict, 4.6), (sc_still, 4.2), (sc_end, 4.8),
]
