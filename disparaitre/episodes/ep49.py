"""Épisode 49 — La fonte de l'Antarctique de l'Ouest (Thwaites, le « glacier de l'Apocalypse »).
Sources :
- International Thwaites Glacier Collaboration (ITGC / NSF / BAS), synthèse « Findings », sept. 2025 :
  surface égale à la Grande-Bretagne ou à la Floride, jusqu'à près de 4 000 m d'épaisseur ; effondrement complet =
  +65 cm de niveau des mers ; la partie de l'inlandsis qu'il retient = plus de 3 m ; les marées poussent l'eau de mer
  tiède sous la glace jusqu'à 10 km en amont ; le débit de glace de Thwaites et voisins a plus que doublé des
  années 1990 aux années 2010 ; les plateformes de glace freinent la glace qui pousse derrière ;
  « un effondrement complet est peu probable dans les prochaines décennies », recul plus rapide aux XXIe et XXIIe
  siècles ; réduire les émissions peut retarder la perte de glace.
- Britannica (« Thwaites Glacier ») : ~192 000 km², taille de la Floride ; jusqu'à 65 cm ; surnom « Doomsday
  Glacier » ; environ 4 % de la montée actuelle des mers ; eaux profondes de la mer d'Amundsen qui se réchauffent.
- NPR (21 mai 2024) : glacier le plus large du monde, taille de la Floride ; plus de deux pieds de montée
  possible ; ~4 % de la montée des mers selon l'ITGC ; eau de mer poussée sous la glace par les marées.
Choix prudents : pas de date d'effondrement (la date « années 2040 » de Britannica est contredite par l'ITGC 2025) ;
« environ 4 % » pour Thwaites seul ; on précise que ce n'est pas une extinction de l'humanité.
"""
from engine import *

EPISODE = 49
BOOM_SCENE = 7
LEGENDE = """Épisode 49 : Thwaites, le « glacier de l'Apocalypse » 🧊🌊

En Antarctique, un glacier grand comme la Floride fond par en dessous, rongé par de l'eau de mer tiède que les marées poussent jusqu'à 10 km sous la glace. S'il s'effondrait entièrement, les océans monteraient d'environ 65 cm (ITGC, Britannica). Bonne nouvelle : les chercheurs jugent un effondrement complet peu probable dans les prochaines décennies, et réduire nos émissions peut le retarder.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #antarctique #glacier #climat #oceans #science #vulgarisation #scienceenfrançais"""

# ---------- fil rouge : le glacier vu en coupe ----------
SEA_Y = 560
ICE = '#eaf6ff'; ICE_D = '#b9dcf2'; ROCK = '#6b4a3a'; SEA = '#2f7fc1'; WARM = '#ff8a3d'

def glacier(d, t, sea_y=SEA_Y, warm=0.0, melt=0.0, shelf=1.0, crack=0.0, flow=0.0, sea_col=SEA):
    # mer
    d.rectangle([s(0), s(sea_y), s(1080), s(950)], fill=hexc(sea_col))
    for i in range(6):  # vaguelettes
        x = (i * 200 + t * 60) % 1200 - 60
        line(d, [(x, sea_y + 6), (x + 50, sea_y - 4), (x + 100, sea_y + 6)], '#ffffff', 5)
    # glace posée sur le sol (fond légèrement si melt)
    gx = 640 - 120 * melt
    top = [(40, 360), (300, 380), (500, 430), (gx, 500 + 10 * melt)]
    poly = top + [(gx, 785 - 0.2 * (640 - gx)), (40, 905)]
    d.polygon([(s(x), s(y)) for x, y in poly], fill=hexc(ICE))
    for i in range(3):  # couches dans la glace
        y = 520 + i * 100
        line(d, [(60, y + 40), (gx - 20, y - 20 + 10 * i)], ICE_D, 4)
    # plateforme flottante (le "bouchon")
    if shelf > 0:
        a = int(255 * shelf)
        dx = 220 * (1 - shelf)
        pts = [(gx, 500 + 10 * melt), (gx + 280 + dx, 535), (gx + 280 + dx, 620), (gx, 660)]
        d.polygon([(s(x + dx * 0.4), s(y)) for x, y in pts], fill=hexc(ICE, a))
        if crack > 0:
            cx = gx + 140
            line(d, [(cx, 520), (cx - 15, 560), (cx + 10, 600), (cx - 5, 640 * 1)], '#1b3a57', 6 * crack)
    # flèches d'écoulement de la glace
    if flow > 0:
        for i in range(3):
            x = 120 + ((t * 120 * flow + i * 160) % 420)
            y = 450 + i * 70
            line(d, [(x, y), (x + 50, y)], '#2f7fc1', 8)
            line(d, [(x + 32, y - 16), (x + 52, y), (x + 32, y + 16)], '#2f7fc1', 8)
    # eau tiède qui se glisse dessous
    if warm > 0:
        for i in range(7):
            ph = (t * 0.6 + i / 7) % 1
            x = 1000 - ph * (380 + 140 * warm)
            y = 700 + 40 * math.sin(i * 1.7) + (ph * 60 if x < gx else 0)
            circle(d, x, y, 16 * warm, fill=hexc(WARM, int(230 * warm * min(1, (1 - ph) * 4))))
    # le sol (sous le niveau de la mer)
    rock = [(0, 950), (0, 905), (40, 905), (gx, 785 - 0.2 * (640 - gx)), (640, 785), (760, 800), (1080, 880), (1080, 950)]
    d.polygon([(s(x), s(y)) for x, y in rock], fill=hexc(ROCK))

# ---------- autres petits dessins ----------
def antarctica(d, t, k):
    pts = []
    for i in range(36):
        a = i / 36 * 2 * math.pi
        r = 270 + 40 * math.sin(3 * a) + 25 * math.cos(5 * a + 1)
        pts.append((540 + r * math.cos(a), 640 + r * 0.8 * math.sin(a)))
    d.polygon([(s(x), s(y)) for x, y in pts], fill=hexc(ICE))
    # Thwaites, côté ouest, qui clignote
    pulse = 0.6 + 0.4 * math.sin(t * 5)
    circle(d, 330, 680, 55 * k, fill=hexc('#ff4d5a', int(230 * pulse * k)))

def glass(d, cx, cy, cube_out, t):
    d.rounded_rectangle([s(cx - 110), s(cy - 170), s(cx + 110), s(cy + 170)], radius=s(26), outline=hexc('#5a3e2b'), width=s(10))
    d.rectangle([s(cx - 100), s(cy - 40), s(cx + 100), s(cy + 160)], fill=hexc('#9fd3f5'))
    if not cube_out:
        wob = 6 * math.sin(t * 3)
        d.rounded_rectangle([s(cx - 50), s(cy - 70 + wob), s(cx + 40), s(cy + 10 + wob)], radius=s(14), fill=hexc('#ffffff'))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0e2233'); header(d, hexc('#9fd3ff'))
    glacier(d, t)
    text_block(img, ["Et si un seul glaçon géant faisait monter toutes les mers du monde ?"], t, 1080, '#ffffff', size=76)

def sc_where(img, d, t, D):
    bg(d, '#16324f'); header(d, hexc('#bfe3ff'))
    antarctica(d, t, ease((t - 0.6) / 0.5))
    text_block(img, ["En Antarctique de l'Ouest, il y a un glacier grand comme la Floride.",
                     ("Son nom : Thwaites.", 1.6)], t, 1060, '#ffffff', size=68)

def sc_thick(img, d, t, D):
    bg(d, '#1d2b45'); header(d, hexc('#c8d6ff'))
    glacier(d, t)
    k = ease((t - 0.4) / 0.6)
    line(d, [(250, 380), (250, 380 + 480 * k)], '#ffe066', 8)
    if k > 0.9:
        ctext(d, "≈ 4 km", 300, 50, '#ffe066', FBK)
    text_block(img, ["Par endroits, sa glace fait presque 4 km d'épaisseur.",
                     ("Et elle repose sur un sol… sous le niveau de la mer.", 1.5)], t, 1060, '#ffffff', size=66)

def sc_cork(img, d, t, D):
    bg(d, '#123b3a'); header(d, hexc('#a8f0e0'))
    glacier(d, t, flow=1.0)
    k = ease((t - 1.0) / 0.4)
    if k > 0:
        d.rounded_rectangle([s(650), s(400), s(1010), s(480)], radius=s(20), fill=hexc('#ffe066', int(255 * k)))
        f = font(FB, 44); tw = f.getlength("LE BOUCHON") / S
        d.text((s(830 - tw / 2), s(414)), "LE BOUCHON", font=f, fill=hexc('#123b3a', int(255 * k)))
        line(d, [(830, 480), (790, 530)], hexc('#ffe066', int(255 * k)), 6)
    text_block(img, ["Son bord flotte sur l'océan (la plateforme de glace).",
                     ("Il freine la glace qui pousse derrière. Comme un bouchon.", 1.6)], t, 1060, '#ffffff', size=66)

def sc_warm(img, d, t, D):
    bg(d, '#3a1f12'); header(d, hexc('#ffc9a3'))
    glacier(d, t, warm=ease((t - 0.3) / 0.8))
    text_block(img, ["Mais l'eau de mer se réchauffe.",
                     ("Les marées la poussent jusqu'à 10 km sous la glace.", 1.4)], t, 1060, '#ffffff', size=70)

def sc_melt(img, d, t, D):
    bg(d, '#2b1a3d'); header(d, hexc('#e0c8ff'))
    m = ease((t - 0.3) / 2.5)
    glacier(d, t, warm=1.0, melt=m, crack=ease((t - 1.5) / 0.6), flow=1.0 + m)
    text_block(img, ["Le glacier fond par en dessous. Et sa glace file vers la mer deux fois plus vite que dans les années 1990."],
               t, 1060, '#ffffff', size=62)

def sc_boom(img, d, t, D):
    bg(d, '#4a0d12'); header(d, hexc('#ffb3bd'))
    k = ease((t - 0.3) / 2.0)
    glacier(d, t, sea_y=SEA_Y - 90 * k, warm=1.0, melt=1.0, shelf=1 - k, sea_col='#3b8fd6')
    shake = 8 * math.sin(t * 30) * max(0, 1 - t / 2)
    ctext(d, "+65 cm", 300 + shake, 90, '#ffe066', FBK, ease((t - 1.2) / 0.4))
    text_block(img, ["S'il s'effondrait en entier : environ 65 cm de mer en plus. Partout sur Terre."], t, 1080, '#ffffff', size=70)

def sc_domino(img, d, t, D):
    bg(d, '#14304a'); header(d, hexc('#bfe3ff'))
    for i in range(6):
        k = ease((t - 0.4 - i * 0.25) / 0.3)
        x = 150 + i * 120
        ang = 1.1 * k
        cx, cy = x, 900
        hx, hy = cx + 230 * math.sin(ang), cy - 230 * math.cos(ang)
        line(d, [(cx, cy), (hx, hy)], ICE if i else '#ff4d5a', 60)
    text_block(img, ["Pire : il retient une partie de la glace voisine.",
                     ("Si tout partait, ce serait plus de 3 mètres.", 1.6)], t, 1060, '#ffffff', size=68)

def sc_joke(img, d, t, D):
    bg(d, '#f6ead8'); header(d, hexc('#8a5a3c'))
    glass(d, 380, 620, False, t)
    k = ease((t - 1.6) / 0.5)
    d.rounded_rectangle([s(640), s(700 - 20 * k), s(820), s(790 - 20 * k)], radius=s(18), fill=hexc('#ffffff', int(255 * k)), outline=hexc('#5a3e2b', int(255 * k)), width=s(4))
    d.rectangle([s(600), s(790), s(900), s(805)], fill=hexc('#5a3e2b', int(255 * k)))
    text_block(img, ["Un glaçon qui fond dans votre verre ne le fait pas déborder…",
                     ("…sauf que Thwaites, lui, est posé à côté du verre.", 1.6)], t, 1010, '#2b1a10', size=64)

def sc_now(img, d, t, D):
    bg(d, '#0f2f24'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.5)
    n = int(round(4 * ease(t / 1.0)))
    ctext(d, f"{n} %", 440, 220, '#a8f0c0', FBK, k)
    ctext(d, "de la montée actuelle des mers", 720, 44, '#a8f0c0', FM, k)
    text_block(img, [("Aujourd'hui déjà, il cause environ 4 % de la montée des océans. Et ça accélère.", 0.9)], t, 1040, '#ffffff', size=64)

def sc_science(img, d, t, D):
    bg(d, '#22264d'); header(d, hexc('#c8ccff'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "DES SIÈCLES", 470, 120, '#c8ccff', FBK, k)
    ctext(d, "pour reculer, pas un jour", 640, 44, '#c8ccff', FM, k)
    text_block(img, ["Les scientifiques jugent un effondrement complet peu probable dans les prochaines décennies.",
                     ("Pas une extinction : un gros problème de côtes. Et moins d'émissions peut le ralentir.", 2.0)],
               t, 960, '#ffffff', size=56)

sc_title = scene_title(["GLACIER", "THWAITES"], "Scénario d'extinction n°49", color='#1b5a8a')
sc_end = scene_end("Bref : la mer monte lentement. Vos impôts, eux, montent à l'heure.", color='#1b5a8a')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_where, 4.2), (sc_thick, 4.4), (sc_cork, 4.6),
    (sc_warm, 4.2), (sc_melt, 4.6), (sc_boom, 4.4), (sc_domino, 4.2),
    (sc_joke, 4.6), (sc_now, 4.4), (sc_science, 5.4), (sc_end, 4.8),
]
