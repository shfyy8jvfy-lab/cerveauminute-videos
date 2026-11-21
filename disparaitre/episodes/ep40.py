"""Épisode 40 — Mythe : l'astéroïde Apophis qui nous percute en 2029.
Sources :
- NASA/JPL, « NASA Analysis: Earth Is Safe From Asteroid Apophis for 100-Plus Years » (25 mars 2021) :
  découvert en 2004, environ 340 m ; passage le vendredi 13 avril 2029 à moins de 32 000 km de la surface,
  plus près que les satellites géostationnaires, visible à l'œil nu dans l'hémisphère Est ; les radars de
  mars 2021 excluent l'impact de 2068 ; « aucun risque d'impact pendant au moins les 100 prochaines années »
  (D. Farnocchia, CNEOS) ; retiré de la table de risque Sentry.
- NASA Science, page Apophis (mise à jour mars 2026) : découvert le 19 juin 2004 à Kitt Peak ; ~32 000 km de
  la surface, plus près que de nombreux satellites géosynchrones (~36 000 km) ; aucun risque pendant au moins
  100 ans ; sonde OSIRIS-APEX redirigée vers Apophis.
- ESA, page Apophis (13 avr. 2024) : ~375 m ; risque d'impact en 2029 monté jusqu'à 2,7 % après sa découverte
  (record sur l'échelle de Turin), puis écarté par d'autres observations ; visible à l'œil nu depuis une
  partie de l'Europe, de l'Afrique et de l'Asie ; « le passage le plus proche d'un astéroïde de cette taille
  jamais connu à l'avance » ; mission Ramses de l'ESA pour l'accompagner.
- ESA, « Apophis impact ruled out for the first time » (26 mars 2021) : retiré de la liste des risques de l'ESA.
"""
from engine import *

EPISODE = 40
BOOM_SCENE = 7
LEGENDE = """Épisode 40 : Apophis, l'astéroïde du vendredi 13 ☄️🌍

Le 13 avril 2029, l'astéroïde Apophis (environ 350 m) passera à moins de 32 000 km de la Terre : plus près que certains satellites, et visible à l'œil nu depuis une partie de l'Europe. En 2004, on lui donnait 2,7 % de chances de nous toucher… mais les mesures ont tout écarté : aucun risque pendant au moins 100 ans (NASA, ESA).

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #asteroide #apophis #espace #astronomie #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
ROCK = [(math.cos(a), math.sin(a), 0.78 + 0.22 * math.sin(a * 3 + 1.3) * math.cos(a * 2)) for a in
        [i * 2 * math.pi / 14 for i in range(14)]]

def apophis(d, cx, cy, r, t, col='#9c8b7a', spin=0.4):
    """Le fil rouge : un caillou cabossé qui tourne doucement."""
    rot = t * spin
    pts = []
    for (ca, sa, k) in ROCK:
        a = math.atan2(sa, ca) + rot
        pts.append((s(cx + r * k * math.cos(a)), s(cy + r * k * math.sin(a))))
    d.polygon(pts, fill=hexc(col))
    for (dx, dy, rr) in ((-0.3, -0.2, 0.18), (0.25, 0.15, 0.14), (-0.05, 0.35, 0.1)):
        a = math.atan2(dy, dx) + rot; L = math.hypot(dx, dy) * r
        circle(d, cx + L * math.cos(a), cy + L * math.sin(a), rr * r, fill=hexc('#000000', 60))

def earth(d, cx, cy, r, t):
    circle(d, cx, cy, r, fill=hexc('#2f7fd8'))
    for (dx, dy, rr) in ((-0.35, -0.25, 0.32), (0.3, 0.2, 0.26), (0.05, -0.5, 0.18)):
        x = cx + (dx + 0.04 * math.sin(t)) * r
        circle(d, x, cy + dy * r, rr * r, fill=hexc('#4fbf6a'))

def ring(d, cx, cy, r, col, w=4, a=160):
    d.ellipse([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], outline=hexc(col, a), width=s(w))

def sat(d, x, y, col='#ffffff'):
    d.rectangle([s(x - 10), s(y - 10), s(x + 10), s(y + 10)], fill=hexc(col))
    d.rectangle([s(x - 38), s(y - 6), s(x - 14), s(y + 6)], fill=hexc('#6ab0ff'))
    d.rectangle([s(x + 14), s(y - 6), s(x + 38), s(y + 6)], fill=hexc('#6ab0ff'))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b0f24'); stars(d, t); header(d, hexc('#c9b8ff'))
    earth(d, 540, 700, 150, t)
    k = ease(t / 3.0)
    apophis(d, 920 - 220 * k, 360 + 120 * k, 60, t)
    text_block(img, ["Un astéroïde va frôler la Terre… un vendredi 13. C'est la fin ?"], t, 1080, '#ffffff', size=74)

def sc_who(img, d, t, D):
    bg(d, '#2a1f3d'); header(d, hexc('#e0c8ff'))
    apophis(d, 540, 620, 230 * (0.6 + 0.4 * ease(t / 1.0)), t)
    text_block(img, ["Il s'appelle Apophis. Découvert en 2004.", ("Environ 350 mètres : plus de trois terrains de foot.", 1.4)], t, 1040, '#ffffff', size=64)

def sc_panic(img, d, t, D):
    bg(d, '#4a1414'); header(d, hexc('#ffb3b3'))
    apophis(d, 540, 620, 160, t, col='#a8907a')
    k = ease((t - 0.3) / 0.5)
    if k > 0:
        d.rounded_rectangle([s(330), s(330), s(750), s(450)], radius=s(30), fill=hexc('#ffd166', int(255 * k)))
        ctext(d, "2,7 %", 342, 90, '#4a1414', FBK, k)
    text_block(img, ["Juste après sa découverte, les calculs donnaient 2,7 % de chances qu'il nous touche en 2029.", ("Un record !", 2.0)], t, 1040, '#ffffff', size=60)

def sc_measure(img, d, t, D):
    bg(d, '#123a4a'); header(d, hexc('#a6e6f2'))
    apophis(d, 700, 600, 110, t)
    # antenne radar
    d.pieslice([s(150), s(720), s(390), s(960)], 200, 340, fill=hexc('#dfe8ee'))
    line(d, [(270, 840), (270, 940)], '#dfe8ee', 18)
    for i in range(3):
        ph = ((t * 1.2 + i / 3) % 1)
        r = 60 + ph * 380
        d.arc([s(270 - r), s(780 - r), s(270 + r), s(780 + r)], 300, 340, fill=hexc('#ffd166', int(255 * (1 - ph))), width=s(8))
    text_block(img, ["Puis les télescopes et les radars l'ont suivi pendant des années.", ("Plus on mesure, plus on sait où il va.", 1.6)], t, 1040, '#ffffff', size=62)

def sc_orbit(img, d, t, D):
    bg(d, '#0f2a1c'); header(d, hexc('#a8f0c0'))
    earth(d, 540, 640, 110, t)
    ring(d, 540, 640, 230, '#a8f0c0', w=4, a=120)
    for i in range(5):
        a = t * 0.5 + i * 2 * math.pi / 5
        sat(d, 540 + 230 * math.cos(a), 640 + 230 * math.sin(a))
    k = ease((t - 0.6) / 2.6)
    apophis(d, 1000 - 900 * k, 300 + 120 * k, 40, t)
    text_block(img, ["Le 13 avril 2029, il passera à 32 000 km de nous.", ("Plus près que certains satellites !", 1.5)], t, 1040, '#ffffff', size=64)

def sc_naked(img, d, t, D):
    bg(d, '#14183f'); stars(d, t); header(d, hexc('#c2c8ff'))
    # silhouette de collines
    d.polygon([(0, s(950)), (s(250), s(840)), (s(520), s(900)), (s(800), s(820)), (s(1080), s(880)), (s(1080), s(960)), (0, s(960))], fill=hexc('#0a0c20'))
    k = ease(t / 3.6)
    x = 150 + 780 * k; y = 520 - 140 * math.sin(k * math.pi)
    circle(d, x, y, 12, fill=hexc('#ffffff'))
    line(d, [(x - 60, y + 14), (x - 4, y + 2)], '#ffffff', 4)
    text_block(img, ["On pourra le voir à l'œil nu, depuis l'Europe, l'Afrique et l'Asie.", ("Un point lumineux qui file dans le ciel.", 1.5)], t, 1040, '#ffffff', size=62)

def sc_boom(img, d, t, D):
    bg(d, '#5c1a08'); header(d, hexc('#ffc8a6'))
    earth(d, 360, 760, 130, t)
    ring(d, 360, 760, 210, '#ffc8a6', w=3, a=90)
    k = ease(t / 2.6)
    x = 1000 - 760 * k; y = 330 + 60 * math.sin(k * math.pi)
    for j in range(1, 6):
        circle(d, x + j * 34, y - j * 4, 10 - j, fill=hexc('#ffd166', 200 - j * 30))
    apophis(d, x, y, 60, t, col='#b39a80')
    kk = ease((t - 1.6) / 0.3)
    if kk > 0:
        d.text((s(620), s(590)), "RATÉ !", font=font(FBK, 100), fill=hexc('#ffd166', int(255 * kk)))
        d.text((s(700), s(730)), "ouf.", font=font(FB, 60), fill=hexc('#ffffff', int(255 * kk)))
    text_block(img, ["Le moment fatidique arrive… et il passe à côté.", ("Il ne fait que nous frôler.", 1.6)], t, 1040, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#fbe9d0'); header(d, hexc('#8a4a00'))
    # un parapluie ouvert
    d.pieslice([s(300), s(380), s(780), s(860)], 180, 360, fill=hexc('#e2453c'))
    line(d, [(540, 620), (540, 900)], '#5a3a1e', 14)
    d.arc([s(490), s(870), s(540), s(930)], 0, 180, fill=hexc('#5a3a1e'), width=s(14))
    for i in range(4):
        x = 360 + i * 120; y = 340 + ((t * 300 + i * 70) % 260)
        line(d, [(x, y), (x - 6, y + 30)], '#6ab0ff', 8)
    text_block(img, ["Pas besoin de parapluie anti-astéroïde.", ("Gardez-le pour le vendredi 13… au cas où il pleuve.", 1.6)], t, 1040, '#3a2200', size=62)

def sc_100(img, d, t, D):
    bg(d, '#14324f'); header(d, hexc('#a6d4ff'))
    k = ease((t - 0.2) / 0.4)
    n = int(min(100, 100 * ease(t / 1.2)))
    ctext(d, f"{n} ANS", 430, 200, '#ffd166', FBK, k)
    ctext(d, "sans aucun risque d'impact", 690, 46, '#a6d4ff', FM, k)
    text_block(img, ["Verdict de la NASA et de l'ESA : aucun risque pendant au moins 100 ans.", ("Ni en 2029, ni en 2036, ni en 2068.", 1.7)], t, 1040, '#ffffff', size=60)

def sc_visit(img, d, t, D):
    bg(d, '#2d1a4a'); stars(d, t); header(d, hexc('#e0c2ff'))
    apophis(d, 600, 640, 170, t)
    k = ease(t / 2.0)
    x = 180 + 180 * k; y = 420 + 40 * math.sin(t * 2)
    d.rectangle([s(x - 30), s(y - 30), s(x + 30), s(y + 30)], fill=hexc('#ffd166'))
    d.rectangle([s(x - 90), s(y - 12), s(x - 34), s(y + 12)], fill=hexc('#6ab0ff'))
    d.rectangle([s(x + 34), s(y - 12), s(x + 90), s(y + 12)], fill=hexc('#6ab0ff'))
    text_block(img, ["Mieux : des sondes iront l'étudier de près (OSIRIS-APEX, Ramses).", ("Une occasion rare, pas une menace.", 1.7)], t, 1040, '#ffffff', size=60)

sc_title = scene_title(["APOPHIS", "2029"], "Scénario d'extinction n°40 · mythe")
sc_end = scene_end("Bref : l'astéroïde nous rate. Votre déclaration d'impôts, elle, ne vous ratera pas.")

SCENES = [
    (sc_hook, 3.6), (sc_title, 2.4), (sc_who, 4.2), (sc_panic, 4.6), (sc_measure, 4.4),
    (sc_orbit, 4.6), (sc_naked, 4.4), (sc_boom, 4.2), (sc_joke, 4.4),
    (sc_100, 4.8), (sc_visit, 4.8), (sc_end, 4.8),
]
