"""Épisode 43 — La couche d'ozone qui disparaît (et comment on l'a sauvée).
Sources :
- EPA, « Basic Ozone Layer Science » (mise à jour mars 2026) : l'ozone de la stratosphère absorbe une grande partie des
  UV du Soleil ; les CFC servaient aux frigos, climatiseurs, mousses isolantes et bombes aérosol ; « un atome de chlore
  peut détruire plus de 100 000 molécules d'ozone ».
- NASA Ozone Watch, « What is a Dobson Unit? » : en moyenne ~300 unités Dobson, soit une couche de 3 mm si on la
  ramenait au sol (« l'épaisseur de 2 pièces empilées »).
- British Antarctic Survey / Discovering Antarctica ; NASA Earth Observatory : trou d'ozone au-dessus de l'Antarctique
  annoncé en 1985 (Farman, Gardiner & Shanklin, Nature) par des chercheurs britanniques de la station Halley.
- NASA Earth Observatory, « The World We Avoided by Protecting the Ozone Layer » (Newman et al., ACP, 2009) : sans le
  protocole de Montréal, près des deux tiers de l'ozone détruits vers 2065 ; indice UV ~30 l'été aux latitudes moyennes,
  coup de soleil en ~5 minutes.
- WMO / PNUE, évaluation scientifique 2022 (communiqué du 9 janv. 2023) : près de 99 % des substances interdites
  éliminées ; retour aux valeurs de 1980 vers 2040 (presque partout), 2045 (Arctique), 2066 (Antarctique).
  ONU : le protocole de Montréal (1987) est le premier traité ratifié par tous les pays membres (2009).
- NASA/NOAA (25 nov. 2025) : le trou d'ozone 2025 est le 5e plus petit depuis 1992.
"""
from engine import *

EPISODE = 43
BOOM_SCENE = 7
LEGENDE = """Épisode 43 : et si le ciel perdait sa crème solaire ? ☀️🕳️

Sans le protocole de Montréal (1987), les deux tiers de la couche d'ozone auraient disparu vers 2065 et un coup de soleil aurait pris 5 minutes (NASA, 2009). Mais le monde a interdit les CFC, près de 99 % ont été éliminés, et la couche devrait se réparer d'ici 2040 à 2066 (ONU/OMM). Pour une fois, on a sauvé la planète… et ça a marché.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #ozone #climat #environnement #vulgarisation #scienceenfrançais"""

def xtext(d, txt, x, y, size, color, fpath=FB, alpha=1.0):
    f = font(fpath, size)
    d.text((s(x) - f.getlength(txt) / 2, s(y)), txt, font=f, fill=hexc(color)[:3] + (int(255 * alpha),))

# ---------- fil rouge : la Terre et son bouclier bleu ----------
def earth(d, cx, cy, r, t):
    circle(d, cx, cy, r, fill=hexc('#2f7fd1'))
    for i, (dx, dy, rr) in enumerate([(-0.35, -0.25, 0.32), (0.3, 0.2, 0.38), (-0.1, 0.45, 0.22), (0.4, -0.4, 0.18)]):
        circle(d, cx + dx * r + 6 * math.sin(t + i), cy + dy * r, rr * r, fill=hexc('#4caf63'))

def shield(d, cx, cy, r, t, a=200, gap=0.0, col='#7fe8ff'):
    """Anneau bleu autour de la Terre. gap = taille (0..1) du trou en bas (pôle Sud)."""
    w = 18
    pul = 4 * math.sin(t * 3)
    if gap <= 0:
        circle(d, cx, cy, r + pul, outline=hexc(col, a), width=w)
    else:
        half = 90 * gap
        d.arc([s(cx - r - pul), s(cy - r - pul), s(cx + r + pul), s(cy + r + pul)], 90 + half, 90 - half + 360,
              fill=hexc(col, a), width=s(w))

def sun(d, cx, cy, r, t, col='#ffd23f'):
    for i in range(12):
        ang = i * math.pi / 6 + t * 0.4
        line(d, [(cx + math.cos(ang) * (r + 20), cy + math.sin(ang) * (r + 20)),
                 (cx + math.cos(ang) * (r + 60), cy + math.sin(ang) * (r + 60))], col, 10)
    circle(d, cx, cy, r, fill=hexc(col))

def rays(d, x0, y0, x1, y1, t, n=5, col='#c58bff', a=230, stop=None):
    """Petites flèches UV du Soleil vers la Terre ; stop = fraction où elles s'arrêtent."""
    for i in range(n):
        ph = (t * 0.9 + i / n) % 1.0
        if stop is not None: ph = min(ph, stop)
        off = (i - n / 2) * 30
        x = x0 + (x1 - x0) * ph; y = y0 + (y1 - y0) * ph + off
        line(d, [(x - 30, y - 12), (x, y), (x - 30, y + 12)], hexc(col, a), 7)

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#14213d'); header(d, hexc('#ffd23f'))
    sun(d, 230, 520, 80, t)
    rays(d, 340, 560, 640, 640, t, n=4)
    earth(d, 760, 660, 140, t); shield(d, 760, 660, 185, t)
    text_block(img, ["Et si le ciel perdait sa crème solaire ?"], t, 1100, '#ffffff', size=84)

def sc_shield(img, d, t, D):
    bg(d, '#1d3b6e'); header(d, hexc('#a6e3ff'))
    sun(d, 200, 500, 70, t)
    rays(d, 300, 540, 520, 640, t, n=5, stop=0.95)
    earth(d, 760, 650, 150, t); shield(d, 760, 650, 200, t, a=240)
    text_block(img, ["Tout là-haut, un gaz, l'ozone, bloque une grande partie des UV du Soleil.", ("Notre parasol géant.", 1.5)], t, 1040, '#ffffff', size=66)

def sc_thin(img, d, t, D):
    bg(d, '#2b4a2e'); header(d, hexc('#c8f0b0'))
    k = ease((t - 0.3) / 0.8)
    for i in range(2):
        y = 760 - i * 70 * k
        d.ellipse([s(390), s(y - 30), s(690), s(y + 30)], fill=hexc('#d9a441'), outline=hexc('#8a6420'), width=s(6))
    ctext(d, "3 mm", 380, 160, '#c8f0b0', FBK, ease((t - 0.8) / 0.4))
    text_block(img, ["Ramenée au sol, cette couche ferait 3 mm.", ("L'épaisseur de deux pièces empilées.", 1.3)], t, 1060, '#ffffff', size=70)

def sc_cfc(img, d, t, D):
    bg(d, '#4a2c5e'); header(d, hexc('#e8c8ff'))
    # frigo
    d.rounded_rectangle([s(170), s(380), s(430), s(900)], radius=s(30), fill=hexc('#f2f2f2'))
    d.line([(s(170), s(560)), (s(430), s(560))], fill=hexc('#9a9a9a'), width=s(6))
    d.rounded_rectangle([s(390), s(440), s(405), s(520)], radius=s(6), fill=hexc('#9a9a9a'))
    # bombe aérosol
    d.rounded_rectangle([s(640), s(520), s(800), s(900)], radius=s(30), fill=hexc('#ff7a59'))
    d.rounded_rectangle([s(690), s(470), s(750), s(525)], radius=s(10), fill=hexc('#cccccc'))
    for i in range(8):
        ph = (t * 0.8 + i / 8) % 1.0
        circle(d, 760 + ph * 200 + 20 * math.sin(i), 480 - ph * 140 + (i % 3) * 15, 10 + 14 * ph, fill=hexc('#ffffff', int(180 * (1 - ph))))
    text_block(img, ["Dans les années 1970-80, frigos et bombes aérosol utilisent des gaz très pratiques : les CFC."], t, 1050, '#ffffff', size=64)

def sc_chlore(img, d, t, D):
    bg(d, '#5e1f2c'); header(d, hexc('#ffc0c8'))
    k = ease((t - 0.3) / 3.0)
    eaten = int(15 * k)
    for i in range(24):
        if i < eaten: continue
        x = 180 + (i % 6) * 145; y = 420 + (i // 6) * 120
        circle(d, x, y, 28, fill=hexc('#7fe8ff'))
    hx = 180 + (eaten % 6) * 145; hy = 420 + (min(eaten, 23) // 6) * 120
    circle(d, hx - 60, hy + 8 * math.sin(t * 8), 40, fill=hexc('#7dff6a'))
    xtext(d, "chlore", hx - 60, hy - 95, 34, '#7dff6a', FB)
    text_block(img, ["Là-haut, ils libèrent du chlore.", ("Un seul atome peut détruire plus de 100 000 molécules d'ozone.", 1.2)], t, 1040, '#ffffff', size=64)

def sc_hole(img, d, t, D):
    bg(d, '#0d2b3a'); header(d, hexc('#8fd8ff'))
    k = ease((t - 0.3) / 1.6)
    earth(d, 540, 620, 170, t); shield(d, 540, 620, 225, t, a=230, gap=0.08 + 0.32 * k)
    ctext(d, "1985", 880, 70, '#ffd23f', FBK, ease((t - 0.2) / 0.4))
    text_block(img, ["Des chercheurs britanniques annoncent un trou au-dessus de l'Antarctique."], t, 1080, '#ffffff', size=68)

def sc_boom(img, d, t, D):
    bg(d, '#6b1010'); header(d, hexc('#ffc0c0'))
    k = ease((t - 0.3) / 2.2)
    sun(d, 200, 470, 80 + 30 * k, t, col='#ffb020')
    rays(d, 320, 520, 640, 640, t * 1.6, n=7, col='#e27bff')
    earth(d, 760, 660, 140, t); shield(d, 760, 660, 185, t, a=int(230 * (1 - 0.85 * k)), gap=0.2 + 0.5 * k)
    ctext(d, "2065 : -2/3", 860, 64, '#ffffff', FBK, ease((t - 1.0) / 0.4))
    text_block(img, ["Sans réaction, la NASA a calculé : deux tiers de l'ozone détruits et un coup de soleil en 5 minutes."], t, 1040, '#ffffff', size=62)

def sc_joke(img, d, t, D):
    bg(d, '#efe4cf'); header(d, hexc('#6a4a2a'))
    d.rounded_rectangle([s(260), s(420), s(820), s(780)], radius=s(26), fill=hexc('#2b2b3a'))
    g = 150 + 60 * math.sin(t * 4)
    d.rounded_rectangle([s(290), s(450), s(790), s(750)], radius=s(16), fill=hexc('#5fd3ff', int(g)))
    d.rounded_rectangle([s(470), s(780), s(610), s(840)], radius=s(10), fill=hexc('#2b2b3a'))
    d.rounded_rectangle([s(380), s(840), s(700), s(870)], radius=s(12), fill=hexc('#2b2b3a'))
    text_block(img, ["Le seul gagnant :", ("votre cousin qui ne sort jamais de sa chambre.", 1.2)], t, 1040, '#2b1a10', size=68)

def sc_montreal(img, d, t, D):
    bg(d, '#14532d'); header(d, hexc('#b8f5c8'))
    d.rounded_rectangle([s(300), s(360), s(780), s(900)], radius=s(24), fill=hexc('#fdfaf0'))
    for i in range(6):
        d.rounded_rectangle([s(350), s(420 + i * 60), s(730 - (i % 2) * 80), s(440 + i * 60)], radius=s(8), fill=hexc('#c9c2ad'))
    k = ease((t - 0.8) / 1.0)
    pts = [(380 + 300 * x / 20, 820 - 30 * math.sin(x * 0.8)) for x in range(int(20 * k) + 1)]
    if len(pts) > 1: line(d, pts, '#1a4dbf', 7)
    text_block(img, ["Alors en 1987, le monde signe le protocole de Montréal : on interdit les CFC.", ("Aujourd'hui, tous les pays l'ont ratifié.", 1.6)], t, 1010, '#ffffff', size=60)

def sc_99(img, d, t, D):
    bg(d, '#1f3b73'); header(d, hexc('#b8d0ff'))
    k = ease((t - 0.2) / 1.2)
    d.rounded_rectangle([s(140), s(600), s(940), s(680)], radius=s(40), outline=hexc('#ffffff'), width=s(6))
    d.rounded_rectangle([s(150), s(610), s(150 + 780 * 0.99 * k), s(670)], radius=s(32), fill=hexc('#7fe8ff'))
    ctext(d, f"{int(99 * k)} %", 400, 150, '#ffffff', FBK, ease(t / 0.3))
    text_block(img, ["Près de 99 % des gaz interdits ont disparu.", ("Le bouclier se recolle, doucement.", 1.3)], t, 1060, '#ffffff', size=68)

def sc_verdict(img, d, t, D):
    bg(d, '#0f3a3a'); header(d, hexc('#a8f0e0'))
    for i, (yr, lab) in enumerate([("2040", "presque partout"), ("2045", "Arctique"), ("2066", "Antarctique")]):
        k = ease((t - 0.3 - i * 0.4) / 0.4)
        xtext(d, yr, 220 + i * 320, 470, 96, '#ffffff', FBK, k)
        xtext(d, lab, 220 + i * 320, 600, 38, '#a8f0e0', FM, k)
    text_block(img, [("Les scientifiques : retour à la normale de 1980 d'ici quelques décennies. Aucune menace d'extinction.", 1.0)], t, 1030, '#ffffff', size=62)

def sc_2025(img, d, t, D):
    bg(d, '#1d3b6e'); header(d, hexc('#a6e3ff'))
    earth(d, 540, 640, 170, t); shield(d, 540, 640, 225, t, a=240, gap=0.1)
    text_block(img, ["En 2025, le trou était le 5e plus petit depuis 1992.", ("La preuve qu'on peut réparer le ciel.", 1.4)], t, 1060, '#ffffff', size=66)

sc_title = scene_title(["LE TROU", "D'OZONE"], "Scénario d'extinction n°43")
sc_end = scene_end("Bref : le ciel se recoud. Le trou dans votre budget après les impôts, beaucoup moins.")

SCENES = [
    (sc_hook, 3.0), (sc_title, 2.4), (sc_shield, 4.2), (sc_thin, 3.4), (sc_cfc, 4.2),
    (sc_chlore, 4.4), (sc_hole, 3.6), (sc_boom, 4.8), (sc_joke, 3.4), (sc_montreal, 4.6),
    (sc_99, 3.6), (sc_verdict, 4.6), (sc_2025, 3.6), (sc_end, 4.8),
]
