"""Épisode 46 — Mythe : le méga-tsunami de La Palma qui rase l'Atlantique.
Sources :
- Ward & Day, Geophysical Research Letters 28(17), 2001 : scénario d'un glissement d'environ 500 km³ du flanc ouest
  du Cumbre Vieja ; vagues de 400-600 m près des Canaries, 10-25 m sur les côtes américaines (Floride 20-25 m).
- Études suivantes (résumées sur la page Wikipédia « Cumbre Vieja tsunami hazard ») : Mader 2001 (≤ 3 m, voire < 1 m
  aux États-Unis), Gisler et al. 2006 (quelques centimètres), Løvholt et al. 2008 (Floride 2-3 fois moins touchée),
  Tehranirad et al. 2015 (1-5 m pour 450 km³, 0-2 m pour 80 km³). Effondrement en plusieurs étapes = vagues plus
  petites. Aucun mouvement actuel du flanc détecté par géodésie ; grands glissements aux Canaries : environ un tous
  les 100 000 ans.
- TU Delft, communiqué EurekAlert du 20 sept. 2006 : flanc « bien plus stable qu'on ne le pense », pas de rupture
  attendue avant au moins 10 000 ans, et il se briserait d'abord en morceaux. Faille de 1949 au sommet du volcan.
- Éruption 2021 (Tajogaite) : 19 sept. – 13 déc. 2021, 85 jours, la plus longue connue de l'île (NPR, CBS News,
  25 déc. 2021) ; pas d'effondrement (rumeurs démenties par les experts).
"""
from engine import *

EPISODE = 46
BOOM_SCENE = 5
LEGENDE = """Épisode 46 : une île des Canaries peut-elle noyer l'Amérique ? 🌋🌊

En 2001, une étude imagine la moitié du volcan Cumbre Vieja, sur l'île de La Palma, glissant d'un coup dans l'océan : une vague de 20 mètres jusqu'en Floride. Les simulations suivantes sont bien plus rassurantes : la vague s'étale et perd sa force, et le flanc se briserait plutôt en morceaux. Aucun mouvement du flanc n'est mesuré, même après l'éruption de 2021. Le vrai danger serait surtout local.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #tsunami #lapalma #canaries #volcan #mythe #science #vulgarisation"""

def xtext(d, txt, x, y, size, color, fpath=FB, alpha=1.0):
    f = font(fpath, size)
    d.text((s(x) - f.getlength(txt) / 2, s(y)), txt, font=f, fill=hexc(color)[:3] + (int(255 * alpha),))

# ---------- fil rouge : l'île-volcan ----------
def sea(d, y, t, col='#2f7fd1', amp=10):
    pts = [(x, y + amp * math.sin(x / 60 + t * 3)) for x in range(0, 1081, 20)]
    d.polygon([(s(x), s(yy)) for x, yy in pts] + [(s(1080), s(960)), (s(0), s(960))], fill=hexc(col))

def island(d, cx, base, t, w=300, h=240, col='#6b4a2f', slide=0.0, smoke=True, crack=False):
    # flanc est (fixe)
    d.polygon([(s(cx - w), s(base)), (s(cx), s(base - h)), (s(cx), s(base))], fill=hexc(col))
    # flanc ouest (peut glisser vers la gauche)
    dx, dy = -slide * 260, slide * 160
    d.polygon([(s(cx + dx), s(base - h + dy)), (s(cx + w + dx * 0.3), s(base + dy * 0.2)), (s(cx + dx), s(base + dy * 0.2))], fill=hexc('#7d5838'))
    d.polygon([(s(cx - 40), s(base - h + 34)), (s(cx), s(base - h)), (s(cx + 40), s(base - h + 34))], fill=hexc('#c0392b'))
    if smoke:
        for i in range(3):
            k = (t * 0.5 + i / 3) % 1
            circle(d, cx + 20 * math.sin(k * 6), base - h - 30 - k * 160, 18 + 26 * k, fill=hexc('#d9d9d9', int(200 * (1 - k))))
    if crack:
        line(d, [(cx + 8, base - h + 20), (cx - 6, base - h + 70), (cx + 10, base - h + 120)], '#1a1a1a', 7)

def wave(d, x, base, hgt, col='#e8f4ff', a=255):
    d.polygon([(s(x - 160), s(base)), (s(x - 40), s(base - hgt)), (s(x + 30), s(base - hgt * 0.8)), (s(x + 60), s(base))], fill=hexc(col, a))
    circle(d, x - 20, base - hgt + 12, 26, fill=hexc('#ffffff', a))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0f2f4f'); header(d, hexc('#9fd8ff'))
    sea(d, 800, t)
    island(d, 680, 800, t)
    wave(d, 330 - 40 * t, 800, 120 + 30 * math.sin(t * 2))
    text_block(img, ["Et si une île des Canaries noyait l'Amérique ?"], t, 1080, '#ffffff', size=76)

def sc_island(img, d, t, D):
    bg(d, '#1f5a5a'); header(d, hexc('#b8f0e0'))
    k = ease((t - 0.1) / 0.8)
    sea(d, 820, t, col='#2a8fa8')
    island(d, 540, 820, t, w=200 + 120 * k, h=170 + 110 * k)
    xtext(d, "La Palma", 540, 860, 48, '#ffffff', FB, k)
    text_block(img, ["Sur l'île de La Palma, il y a un volcan : le Cumbre Vieja.", ("En 2021, il a craché de la lave pendant 85 jours.", 1.4)], t, 1040, '#ffffff', size=64)

def sc_crack(img, d, t, D):
    bg(d, '#4a2a3a'); header(d, hexc('#ffc8e0'))
    sea(d, 840, t, col='#3a6fb0')
    island(d, 540, 840, t, w=320, h=300, crack=t > 0.6)
    xtext(d, "1949", 760, 430, 60, '#ffc8e0', FBK, ease((t - 0.6) / 0.4))
    text_block(img, ["En 1949, une faille s'ouvre au sommet.", ("Certains y voient un flanc prêt à lâcher.", 1.3)], t, 1060, '#ffffff', size=68)

def sc_theory(img, d, t, D):
    bg(d, '#2b2a5a'); header(d, hexc('#d0c8ff'))
    sea(d, 840, t, col='#4a6fd0')
    k = ease((t - 0.8) / 1.6) * 0.5
    island(d, 600, 840, t, w=320, h=300, slide=k, crack=True)
    # flèche
    line(d, [(560, 420), (380, 520)], '#ffd23f', 12)
    d.polygon([(s(360), s(532)), (s(395), s(495)), (s(410), s(535))], fill=hexc('#ffd23f'))
    text_block(img, ["2001 : une étude imagine la moitié du volcan glissant d'un coup dans l'océan.", ("(500 km³ de roche !)", 1.8)], t, 1030, '#ffffff', size=62)

def sc_boom(img, d, t, D):
    bg(d, '#0a1a3a'); header(d, hexc('#a8c8ff'))
    sea(d, 820, t, col='#1d4fa0', amp=16)
    island(d, 900, 820, t, w=150, h=140, slide=0.5, smoke=False, crack=True)
    k = ease(t / 2.5)
    wave(d, 800 - 520 * k, 820, 120 + 260 * k)
    # côte américaine à gauche : petits immeubles
    for i, hh in enumerate([90, 140, 70]):
        d.rounded_rectangle([s(30 + i * 60), s(820 - hh), s(80 + i * 60), s(830)], radius=s(8), fill=hexc('#f0c040'))
    text_block(img, ["Selon cette étude : une vague qui traverse l'Atlantique…", ("…20 à 25 mètres en Floride !", 1.5)], t, 1040, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#ffe9b8'); header(d, hexc('#8a5a10'))
    sea(d, 760, t, col='#3aa0d8')
    # planche de surf
    y = 700 + 14 * math.sin(t * 3)
    d.rounded_rectangle([s(360), s(y - 22), s(720), s(y + 22)], radius=s(22), fill=hexc('#e8455a'))
    line(d, [(380, y), (700, y)], '#ffffff', 6)
    text_block(img, ["Les surfeurs du monde entier ont noté la date.", ("(Il n'y en a pas.)", 1.4)], t, 1080, '#3a2a0a', size=70)

def sc_spread(img, d, t, D):
    bg(d, '#14506b'); header(d, hexc('#a8e8ff'))
    k = ease((t - 0.3) / 2.2)
    for i in range(5):
        r = 60 + k * 270 * (i + 1) / 5
        circle(d, 540, 620, r, outline=hexc('#ffffff', int(230 * (1 - i / 6) * (1 - 0.6 * k))), width=max(3, int(16 * (1 - k * 0.8))))
    island(d, 540, 660, t, w=80, h=70, smoke=False)
    text_block(img, ["Les simulations suivantes : la vague s'étale et perd sa force.", ("De l'autre côté : quelques mètres, souvent moins.", 1.6)], t, 1030, '#ffffff', size=62)

def sc_pieces(img, d, t, D):
    bg(d, '#5a3a1a'); header(d, hexc('#ffd8a8'))
    sea(d, 840, t, col='#2f7fd1')
    island(d, 500, 840, t, w=280, h=280, smoke=False)
    for i in range(4):
        tt = max(0, t - 0.6 - i * 0.5)
        y = 640 + i * 40 + min(150, tt * 120)
        d.rounded_rectangle([s(640 + i * 50), s(y), s(700 + i * 50), s(y + 50)], radius=s(12), fill=hexc('#7d5838'))
    text_block(img, ["Et le flanc tomberait plutôt en plusieurs morceaux.", ("Petits morceaux = petites vagues.", 1.5)], t, 1060, '#ffffff', size=66)

def sc_stable(img, d, t, D):
    bg(d, '#2a4a2a'); header(d, hexc('#c8f5b0'))
    sea(d, 840, t, col='#2f8f7f')
    island(d, 540, 840, t, w=320, h=290)
    k = ease((t - 0.5) / 0.4)
    circle(d, 850, 420, 70, fill=hexc('#2a9a4a', int(255 * k)))
    line(d, [(815, 420), (842, 450), (890, 392)], hexc('#ffffff', int(255 * k)), 14)
    text_block(img, ["Les mesures : le flanc ne bouge pas.", ("Même l'éruption de 2021 ne l'a pas fait glisser.", 1.3)], t, 1060, '#ffffff', size=66)

def sc_verdict(img, d, t, D):
    bg(d, '#3b0f2a'); header(d, hexc('#ffc0e0'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "EXAGÉRÉ", 470, 140, '#ffc0e0', FBK, k)
    ctext(d, "grands effondrements aux Canaries : ~1 tous les 100 000 ans", 660, 34, '#ffc0e0', FM, k)
    text_block(img, [("Le vrai danger serait surtout local : aux Canaries et sur les côtes proches.", 0.9)], t, 1040, '#ffffff', size=62)

sc_title = scene_title(["LA PALMA", "TSUNAMI"], "Mythe à démonter · n°46", color='#0f5a8a')
sc_end = scene_end("Bref : la vague géante ne viendra pas. Votre avis d'imposition, si.", color='#0f5a8a')

SCENES = [
    (sc_hook, 3.0), (sc_title, 2.4), (sc_island, 4.4), (sc_crack, 4.0), (sc_theory, 4.6),
    (sc_boom, 4.6), (sc_joke, 3.6), (sc_spread, 4.6), (sc_pieces, 4.2), (sc_stable, 4.2),
    (sc_verdict, 4.4), (sc_end, 4.8),
]
