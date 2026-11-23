"""Épisode 44 — Mythe : Bételgeuse qui explose et nous grille.
Sources :
- ESO, communiqué eso2109 (16 juin 2021) ; Montargès et al., Nature 594, 2021 : la « Grande Baisse d'éclat » de fin
  2019 - début 2020 venait d'un voile de poussière (gaz éjecté qui s'est refroidi et condensé) ; ce n'était PAS un signe
  d'explosion imminente. Éclat revenu à la normale en avril 2020.
- NASA JPL (23 juil. 2025) ; Howell et al., ApJ Letters : compagne probable « Siwarha » imagée au télescope Gemini Nord.
- Live Science (P. Sutter, 22 nov. 2024) : Bételgeuse à ~650 années-lumière ; sa supernova sera « presque aussi
  brillante que la pleine Lune », visible en plein jour, pendant quelques mois ; danger seulement à quelques dizaines
  d'années-lumière (25-30 a.-l. pour détruire la moitié de l'ozone). Sky at Night (P. Moore) : Bételgeuse hors de portée.
- Distance selon les études : ~550 à 700 a.-l. (Joyce et al., ApJ 2020 : ~550 a.-l., explosion attendue d'ici
  ~100 000 ans). Rayon de plusieurs centaines de fois celui du Soleil : à la place du Soleil, elle dépasserait l'orbite
  de Mars.
"""
from engine import *

EPISODE = 44
BOOM_SCENE = 6
LEGENDE = """Épisode 44 : Bételgeuse va-t-elle exploser et nous griller ? ⭐💥

Fin 2019, l'étoile rouge d'Orion s'est assombrie d'un coup et internet a crié à l'explosion imminente. Verdict publié dans Nature en 2021 : un simple nuage de poussière lui faisait de l'ombre. Elle explosera bien un jour (sans doute d'ici 100 000 ans), mais à plus de 500 années-lumière, on aura juste droit à un spectacle presque aussi brillant que la pleine Lune.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #betelgeuse #mythe #astronomie #espace #supernova #science #vulgarisation #apocalypse"""

def xtext(d, txt, x, y, size, color, fpath=FB, alpha=1.0):
    f = font(fpath, size)
    d.text((s(x) - f.getlength(txt) / 2, s(y)), txt, font=f, fill=hexc(color)[:3] + (int(255 * alpha),))

# ---------- fil rouge : Bételgeuse, grosse étoile rouge qui ondule ----------
def betel(d, cx, cy, r, t, a=255, col='#ff5a2c', glow=False):
    if glow:
        circle(d, cx, cy, r * 1.12, outline=hexc('#ffb36b', int(a * 0.5)), width=6)
    pts = []
    for i in range(48):
        ang = i * math.pi * 2 / 48
        rr = r * (1 + 0.045 * math.sin(ang * 5 + t * 2.2) + 0.03 * math.sin(ang * 3 - t * 1.7))
        pts.append((s(cx + rr * math.cos(ang)), s(cy + rr * math.sin(ang))))
    d.polygon(pts, fill=hexc(col, a))
    rgb = [int(col[i:i + 2], 16) for i in (1, 3, 5)]
    hl = '#%02x%02x%02x' % tuple(min(255, int(v + (255 - v) * 0.45)) for v in rgb)
    circle(d, cx - r * 0.3, cy - r * 0.25, r * 0.28, fill=hexc(hl, a))

def twinkle(d, x, y, r, col='#ffffff', a=255):
    circle(d, x, y, r, fill=hexc(col, a))
    line(d, [(x - r * 2.2, y), (x + r * 2.2, y)], hexc(col, int(a * 0.6)), 3)
    line(d, [(x, y - r * 2.2), (x, y + r * 2.2)], hexc(col, int(a * 0.6)), 3)

ORION = [(400, 380), (690, 430), (500, 640), (560, 625), (620, 610), (430, 900), (700, 870)]

def earth(d, cx, cy, r, t):
    circle(d, cx, cy, r, fill=hexc('#2f7fd1'))
    for i, (dx, dy, rr) in enumerate([(-0.35, -0.25, 0.32), (0.3, 0.2, 0.38), (-0.1, 0.45, 0.22)]):
        circle(d, cx + dx * r + 3 * math.sin(t + i), cy + dy * r, rr * r, fill=hexc('#4caf63'))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b1026'); stars(d, t); header(d, hexc('#ffb38a'))
    for i, (x, y) in enumerate(ORION[1:]):
        twinkle(d, x, y, 11, '#cfe0ff', int(200 + 55 * math.sin(t * 3 + i)))
    line(d, [ORION[0], ORION[2]], hexc('#ffffff', 50), 3)
    line(d, [ORION[1], ORION[4]], hexc('#ffffff', 50), 3)
    line(d, [ORION[2], ORION[5]], hexc('#ffffff', 50), 3)
    line(d, [ORION[4], ORION[6]], hexc('#ffffff', 50), 3)
    pul = 26 + 8 * math.sin(t * 5)
    betel(d, ORION[0][0], ORION[0][1], pul, t)
    text_block(img, ["Et si l'étoile rouge d'Orion explosait… et nous grillait tous ?"], t, 1080, '#ffffff', size=76)

def sc_giant(img, d, t, D):
    bg(d, '#3a0f1a'); header(d, hexc('#ffb3a8'))
    k = ease((t - 0.2) / 0.9)
    betel(d, 620, 640, 50 + 160 * k, t, glow=True)
    circle(d, 190, 640, 9, fill=hexc('#ffe36b'))
    xtext(d, "le Soleil", 190, 680, 34, '#ffe36b', FM, ease((t - 0.3) / 0.4))
    text_block(img, ["Bételgeuse est une géante rouge.", ("À la place du Soleil, elle dépasserait l'orbite de Mars.", 1.3)], t, 1040, '#ffffff', size=68)

def sc_old(img, d, t, D):
    bg(d, '#2b1640'); header(d, hexc('#e0c2ff'))
    flick = 1 + 0.05 * math.sin(t * 13) * math.sin(t * 3)
    betel(d, 540, 600, 210 * flick, t, glow=True)
    d.rounded_rectangle([s(330), s(890), s(750), s(930)], radius=s(20), outline=hexc('#e0c2ff'), width=s(5))
    d.rounded_rectangle([s(336), s(896), s(336 + 50), s(924)], radius=s(14), fill=hexc('#ff4d5a'))
    text_block(img, ["Elle est en fin de vie. Un jour, elle explosera : c'est une supernova."], t, 1060, '#ffffff', size=70)

def sc_dim(img, d, t, D):
    bg(d, '#141a2e'); stars(d, t); header(d, hexc('#a9c4ff'))
    k = ease((t - 0.6) / 1.4)
    c0, c1 = (0xff, 0x5a, 0x2c), (0x5e, 0x2e, 0x30)
    col = '#%02x%02x%02x' % tuple(int(a + (b - a) * k) for a, b in zip(c0, c1))
    betel(d, 540, 620, 220, t, col=col)
    xtext(d, "déc. 2019", 540, 890, 44, '#a9c4ff', FB, ease((t - 0.3) / 0.4))
    text_block(img, ["Fin 2019, patatras : elle perd d'un coup une grande partie de son éclat."], t, 1060, '#ffffff', size=70)

def phone(d, cx, cy, t, k):
    shake = 6 * math.sin(t * 35) if t > 1.0 else 0
    x = cx + shake
    d.rounded_rectangle([s(x - 170), s(cy - 300), s(x + 170), s(cy + 300)], radius=s(40), fill=hexc('#1b1b22'))
    d.rounded_rectangle([s(x - 150), s(cy - 270), s(x + 150), s(cy + 270)], radius=s(26), fill=hexc('#f4f4f8'))
    for i in range(4):
        kk = ease((t - 0.3 - i * 0.35) / 0.3)
        if kk <= 0: continue
        y = cy - 240 + i * 125
        d.rounded_rectangle([s(x - 135), s(y), s(x + 135), s(y + 105)], radius=s(18), fill=hexc('#ff4d5a', int(255 * kk)))
        circle(d, x - 95, y + 52, 26, fill=hexc('#ffffff', int(255 * kk)))
        d.rounded_rectangle([s(x - 55), s(y + 30), s(x + 115), s(y + 48)], radius=s(9), fill=hexc('#ffffff', int(220 * kk)))
        d.rounded_rectangle([s(x - 55), s(y + 60), s(x + 70), s(y + 76)], radius=s(8), fill=hexc('#ffffff', int(160 * kk)))

def sc_panic(img, d, t, D):
    bg(d, '#ffcf3f'); header(d, hexc('#6a3b00'))
    phone(d, 540, 630, t, 1)
    text_block(img, ["Sur internet, panique : « Elle va exploser ! On va tous y passer ! »"], t, 1060, '#2b1700', size=70)

def sc_boom(img, d, t, D):
    k = ease((t - 0.2) / 0.5)
    bg(d, '#05060f'); stars(d, t); header(d, hexc('#ffe9b0'))
    if t < 0.4:
        betel(d, 540, 600, 120, t)
    else:
        for i in range(4):
            rr = ((t - 0.4) * 200 - i * 80) % 320
            if rr > 0 and t - 0.4 > i * 0.4:
                circle(d, 540, 600, rr, outline=hexc('#ffe9b0', max(0, int(230 - rr * 0.7))), width=10)
        circle(d, 540, 600, 60 + 30 * k + 6 * math.sin(t * 20), fill=hexc('#ffffff'))
        circle(d, 540, 600, 40 + 20 * k, fill=hexc('#fff6d0'))
    text_block(img, ["Imaginons qu'elle explose ce soir…", ("Elle brillerait presque comme la pleine Lune. En plein jour, pendant des mois.", 1.5)], t, 1030, '#ffffff', size=64)

def sc_far(img, d, t, D):
    bg(d, '#0e3b2e'); header(d, hexc('#a8f0c0'))
    earth(d, 150, 620, 55, t)
    k = ease((t - 0.3) / 1.2)
    bx = 150 + 780 * k
    betel(d, bx, 620, 50, t, glow=False)
    circle(d, bx, 620, 120, outline=hexc('#ff4d5a', 200), width=6)
    line(d, [(150, 760), (150 + 780 * k, 760)], '#a8f0c0', 8)
    if k > 0.95:
        xtext(d, "plus de 500 années-lumière", 540, 790, 44, '#a8f0c0', FB, ease((t - 1.5) / 0.4))
    xtext(d, "zone de danger", bx, 470, 34, '#ffb3bd', FM, ease((t - 1.0) / 0.4))
    text_block(img, ["Mais une supernova ne nous menace qu'à quelques dizaines d'années-lumière.", ("Bételgeuse est dix fois plus loin.", 2.0)], t, 1030, '#ffffff', size=64)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    # télescope pointé vers une étoile qui brille
    ang = -0.6 + 0.05 * math.sin(t * 2)
    x0, y0 = 380, 820
    x1, y1 = x0 + 420 * math.cos(ang), y0 + 420 * math.sin(ang)
    line(d, [(x0, y0), (x1, y1)], '#8a5a3c', 60)
    line(d, [(x0 + 40, y0 + 10), (x0 - 20, y0 + 130)], '#4a2c1d', 14)
    line(d, [(x0 + 40, y0 + 10), (x0 + 110, y0 + 130)], '#4a2c1d', 14)
    twinkle(d, 820, 380, 30 + 6 * math.sin(t * 4), '#ff9a3c')
    text_block(img, ["Le seul vrai risque :", ("un torticolis, à force de la regarder.", 1.1)], t, 1060, '#2b1a10', size=72)

def sc_dust(img, d, t, D):
    bg(d, '#1f2a44'); header(d, hexc('#c8d6ff'))
    betel(d, 540, 620, 220, t)
    k = ease((t - 0.3) / 1.2)
    for i in range(9):
        cx = 330 + 60 * (i % 3) + 140 * k
        cy = 700 + 50 * (i // 3) + 6 * math.sin(t * 2 + i)
        circle(d, cx, cy, 70, fill=hexc('#5b5f6e', int(200 * k)))
    xtext(d, "poussière", 470 + 140 * k, 880, 40, '#c8d6ff', FB, k)
    text_block(img, ["L'explication (revue Nature, 2021) : un nuage de poussière, recraché par l'étoile, lui faisait de l'ombre."], t, 1030, '#ffffff', size=62)

def sc_buddy(img, d, t, D):
    bg(d, '#123a4a'); header(d, hexc('#a6e3ff'))
    betel(d, 540, 620, 190, t)
    ang = t * 1.4
    bx, by = 540 + 300 * math.cos(ang), 620 + 110 * math.sin(ang)
    circle(d, bx, by, 22, fill=hexc('#bfe6ff'))
    circle(d, bx, by, 34, outline=hexc('#bfe6ff', 120), width=4)
    text_block(img, ["Et en 2025, on a sans doute photographié sa petite étoile compagne : Siwarha."], t, 1060, '#ffffff', size=66)

def sc_verdict(img, d, t, D):
    bg(d, '#3b2a0a'); header(d, hexc('#ffe0a0'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "~100 000 ANS", 480, 140, '#ffe0a0', FBK, k)
    ctext(d, "avant l'explosion, sans doute", 680, 44, '#ffe0a0', FM, k)
    text_block(img, [("Les astronomes : elle explosera bien un jour. Mais sans aucun danger pour nous.", 0.8)], t, 1050, '#ffffff', size=66)

sc_title = scene_title(["BÉTEL-", "GEUSE"], "Mythe à démonter · n°44", color='#8f1d14')
sc_end = scene_end("Bref : Bételgeuse explosera un jour. Votre avis d'impôts, lui, arrivera bien avant.", color='#8f1d14')

SCENES = [
    (sc_hook, 3.0), (sc_title, 2.4), (sc_giant, 4.2), (sc_old, 4.0), (sc_dim, 4.4),
    (sc_panic, 4.2), (sc_boom, 4.6), (sc_far, 4.4), (sc_joke, 3.8), (sc_dust, 4.6),
    (sc_buddy, 4.0), (sc_verdict, 4.4), (sc_end, 4.8),
]
