"""Épisode 18 — Le grand filtre de Fermi (pourquoi l'univers semble vide).
Sources :
- Paradoxe de Fermi : en 1950, à Los Alamos, lors d'un déjeuner, Enrico Fermi demande « Where is everybody? »
  (Universe Today, « The Great Filter Part 1: The Legacy of Fermi's Paradox » ; Ars Technica, mars 2025).
- Grand Filtre : idée proposée par l'économiste Robin Hanson en 1996 ; une étape très improbable entre la matière
  inerte et une civilisation qui colonise l'espace, qui peut être derrière nous ou devant nous
  (Universe Today, « Beyond Fermi's Paradox III: What is the Great Filter? » ; Ars Technica 2025).
- Nick Bostrom, « Where are they? Why I hope the search for extraterrestrial life finds nothing »,
  MIT Technology Review, 2008 (nickbostrom.com) : trouver de la vie indépendante sur Mars serait une mauvaise nouvelle.
- Voie lactée : de l'ordre de 100 à 400 milliards d'étoiles (Astronomy.com ; NASA).
- Écoute radio SETI depuis 1960 (projet Ozma de Frank Drake).
- Consensus : aucune réponse établie ; aucune preuve de civilisation extraterrestre ; le silence observé ne permet
  pas de conclure.
"""
from engine import *

EPISODE = 18
BOOM_SCENE = 7
LEGENDE = """Épisode 18 : le Grand Filtre de Fermi 👽🧱

Plus de 100 milliards d'étoiles dans notre galaxie… et pas un seul message extraterrestre. Et s'il existait une étape presque impossible à franchir pour toute civilisation ? Si elle est derrière nous, ouf. Si elle est devant… aïe. Le philosophe Nick Bostrom espère même qu'on ne trouvera aucune vie sur Mars (MIT Technology Review, 2008).

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #fermi #extraterrestres #espace #astronomie #science #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
STEP_W, STEP_H = 150, 85
def stair_xy(x0, y0, i):
    """Coin haut-gauche de la marche i (escalier qui monte vers la droite)."""
    return x0 + i * STEP_W, y0 - i * STEP_H

def stairs(d, x0, y0, n, col, labels=None, lab_col='#ffffff'):
    """Fil rouge : l'escalier des civilisations."""
    for i in range(n):
        x, y = stair_xy(x0, y0, i)
        d.rounded_rectangle([s(x), s(y), s(x + STEP_W - 8), s(y0 + STEP_H)], radius=s(12), fill=hexc(col))
        if labels and i < len(labels):
            f = font(FB, 30)
            d.text((s(x + (STEP_W - 8) / 2), s(y + 30)), labels[i], font=f, fill=hexc(lab_col), anchor='mm')

def ball_on(d, x0, y0, pos, col='#ffd166', r=34, hop=0.0):
    """Petite boule (une civilisation) posée sur la marche pos (peut être fractionnaire)."""
    i = int(pos); fr = pos - i
    x = x0 + pos * STEP_W + (STEP_W - 8) / 2
    y = y0 - pos * STEP_H - r - 4 - abs(math.sin(fr * math.pi)) * 60 - hop
    circle(d, x, y, r, fill=hexc(col))
    return x, y

def wall(d, x, ytop, ybot, col='#e63946'):
    d.rounded_rectangle([s(x - 22), s(ytop), s(x + 22), s(ybot)], radius=s(10), fill=hexc(col))
    for j in range(int((ybot - ytop) / 60)):
        yy = ytop + 30 + j * 60
        line(d, [(x - 22, yy), (x + 22, yy)], '#00000055' if False else '#7a1b22', 4)

def galaxy(d, cx, cy, t, R=300, col='#c9b8ff'):
    for arm in range(2):
        for j in range(60):
            a = j * 0.13 + arm * math.pi + t * 0.25
            r = 20 + j * R / 60
            circle(d, cx + math.cos(a) * r, cy + math.sin(a) * r * 0.55, 3 + (60 - j) / 20, fill=hexc(col, 120 + j * 2))
    circle(d, cx, cy, 40, fill=hexc('#fff1c1'))

def dish(d, cx, cy, t, col='#e0e0e0', waves=True):
    d.pieslice([s(cx - 150), s(cy - 220), s(cx + 150), s(cy + 40)], 10, 170, fill=hexc(col))
    line(d, [(cx, cy - 90), (cx, cy - 170)], col, 8); circle(d, cx, cy - 175, 14, fill=hexc(col))
    d.rounded_rectangle([s(cx - 18), s(cy + 20), s(cx + 18), s(cy + 140)], radius=s(8), fill=hexc(col))
    d.rounded_rectangle([s(cx - 90), s(cy + 130), s(cx + 90), s(cy + 160)], radius=s(12), fill=hexc(col))
    if waves:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1.0
            rr = 60 + ph * 220
            d.arc([s(cx - rr), s(cy - 175 - rr), s(cx + rr), s(cy - 175 + rr)], 240, 300, fill=hexc(col, int(255 * (1 - ph))), width=s(8))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b0b26'); stars(d, t); header(d, hexc('#c9b8ff'))
    galaxy(d, 540, 620, t)
    k = ease((t - 0.8) / 0.4)
    d.text((s(860), s(380)), "?", font=font(FBK, 160), fill=hexc('#ffd166', int(255 * k)), anchor='mm')
    text_block(img, ["L'univers est immense. Alors… où sont les extraterrestres ?"], t, 1090, '#ffffff', size=76)

def sc_fermi(img, d, t, D):
    bg(d, '#2a1b0e'); header(d, hexc('#ffcf99'))
    d.rounded_rectangle([s(200), s(760), s(880), s(800)], radius=s(16), fill=hexc('#8a5a3c'))
    for x in (260, 820):
        d.rounded_rectangle([s(x - 12), s(800), s(x + 12), s(940)], radius=s(6), fill=hexc('#8a5a3c'))
    circle(d, 400, 735, 60, fill=hexc('#f3e6d3')); circle(d, 400, 735, 38, fill=hexc('#e0cdb0'))
    d.rounded_rectangle([s(600), s(640), s(680), s(758)], radius=s(14), fill=hexc('#cfe9ec'))
    k = ease((t - 0.5) / 0.4)
    bob = 10 * math.sin(t * 3)
    d.rounded_rectangle([s(330), s(390 + bob), s(750), s(560 + bob)], radius=s(40), fill=hexc('#ffffff', int(255 * k)))
    d.text((s(540), s(475 + bob)), "Où sont-ils ?", font=font(FBK, 58), fill=hexc('#2a1b0e', int(255 * k)), anchor='mm')
    text_block(img, ["En 1950, le physicien Enrico Fermi lance à table : « Mais où sont-ils tous ? »"], t, 1060, '#ffffff', size=66)

def sc_silence(img, d, t, D):
    bg(d, '#0d2238'); stars(d, t); header(d, hexc('#9fd3ff'))
    dish(d, 540, 700, t, waves=False)
    k = ease((t - 0.6) / 0.4)
    d.text((s(540), s(420)), "…", font=font(FBK, 140), fill=hexc('#9fd3ff', int(255 * k)), anchor='mm')
    text_block(img, ["Notre galaxie compte plus de cent milliards d'étoiles. Et pourtant : silence radio."], t, 1080, '#ffffff', size=66)

def sc_filter(img, d, t, D):
    bg(d, '#1f3a2a'); header(d, hexc('#a8f0c0'))
    stairs(d, 200, 820, 5, '#a8f0c0')
    ball_on(d, 200, 820, min(2.0, t * 0.9))
    wall(d, 200 + 3 * STEP_W - 4, 820 - 4 * STEP_H - 40, 820 - 2 * STEP_H)
    text_block(img, ["L'idée du Grand Filtre : il existe une marche presque impossible à franchir."], t, 1080, '#ffffff', size=68)

def sc_steps(img, d, t, D):
    bg(d, '#3a2a0a'); header(d, hexc('#ffe08a'))
    stairs(d, 170, 860, 5, '#ffe08a', labels=["vie", "cellule", "animal", "cerveau", "fusée"], lab_col='#3a2a0a')
    ball_on(d, 170, 860, min(4.0, t * 1.2))
    text_block(img, ["La vie, les cellules, l'intelligence, les fusées… Une de ces étapes bloque presque tout le monde."], t, 1060, '#ffffff', size=62)

def sc_where(img, d, t, D):
    bg(d, '#2b1a3a'); header(d, hexc('#d2b8ff'))
    stairs(d, 200, 820, 5, '#d2b8ff')
    ball_on(d, 200, 820, 2.0, hop=12 * abs(math.sin(t * 4)))
    k = ease((t - 0.3) / 0.4); k2 = ease((t - 1.6) / 0.4)
    if k > 0:
        wall(d, 200 + STEP_W - 4, 820 - 2 * STEP_H - 40, 820)
        d.text((s(260), s(420)), "ouf", font=font(FBK, 60), fill=hexc('#a8f0c0', int(255 * k)), anchor='mm')
    if k2 > 0:
        wall(d, 200 + 4 * STEP_W - 4, 820 - 5 * STEP_H - 40, 820 - 3 * STEP_H)
        d.text((s(830), s(320)), "aïe", font=font(FBK, 60), fill=hexc('#ff8fa3', int(255 * k2)), anchor='mm')
    text_block(img, ["Si ce filtre est derrière nous : ouf.", ("S'il est devant nous : aïe.", 1.6)], t, 1080, '#ffffff', size=72)

random.seed(18)
SHARDS = [(random.uniform(0, 2 * math.pi), random.uniform(80, 260)) for _ in range(12)]
def sc_boom(img, d, t, D):
    bg(d, '#3a0b10'); header(d, hexc('#ffb3bd'))
    shake = 7 * math.sin(t * 45) * (1 if t < 1.0 else 0.15)
    stairs(d, 200 + shake, 820, 5, '#ffb3bd')
    wx = 200 + 4 * STEP_W - 4
    wall(d, wx + shake, 820 - 5 * STEP_H - 40, 820 - 3 * STEP_H)
    p = min(1.0, t / 0.8)
    if p < 1.0:
        ball_on(d, 200 + shake, 820, 2.0 + 1.4 * p)
    else:
        cx, cy = wx - 40, 820 - 3 * STEP_H - 40
        k = ease((t - 0.8) / 0.8)
        for (a, r) in SHARDS:
            circle(d, cx + math.cos(a) * r * k, cy + math.sin(a) * r * k + 120 * k * k, 12, fill=hexc('#ffd166'))
    text_block(img, ["Alors toutes les civilisations s'écrasent contre le mur. Nous compris.", ("Fin de la partie.", 1.8)], t, 1060, '#ffffff', size=70)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    cols = ['#e63946', '#457b9d', '#2a9d8f', '#e9c46a', '#8a5a3c']
    for i in range(5):
        x = 170 + i * 150
        d.rounded_rectangle([s(x), s(560), s(x + 130), s(800)], radius=s(26), fill=hexc(cols[i]))
    a = t * 1.8
    x = 540 + 360 * math.cos(a); y = 470 + 40 * math.sin(a)
    d.rounded_rectangle([s(x - 70), s(y - 40), s(x + 70), s(y + 40)], radius=s(24), fill=hexc('#2b1a10'))
    text_block(img, ["Une épreuve que presque personne ne franchit…", ("…se garer à Paris un samedi.", 1.6)], t, 1020, '#2b1a10', size=68)

def sc_mars(img, d, t, D):
    bg(d, '#12301f'); stars(d, t); header(d, hexc('#a8f0c0'))
    circle(d, 540, 640, 200, fill=hexc('#c1440e'))
    circle(d, 470, 590, 40, fill=hexc('#9a3509')); circle(d, 610, 700, 28, fill=hexc('#9a3509'))
    k = ease((t - 0.8) / 0.4)
    d.rounded_rectangle([s(640), s(380), s(900), s(500)], radius=s(30), fill=hexc('#ffffff', int(255 * k)))
    d.text((s(770), s(440)), "0 microbe", font=font(FBK, 44), fill=hexc('#12301f', int(255 * k)), anchor='mm')
    text_block(img, ["Le philosophe Nick Bostrom espère qu'on ne trouvera aucune vie sur Mars. Si la vie est rare, le filtre est derrière nous."], t, 1040, '#ffffff', size=58)

def sc_science(img, d, t, D):
    bg(d, '#0b2545'); header(d, hexc('#9fc2ff'))
    k = ease((t - 0.2) / 0.35)
    sc = 1.5 - 0.5 * k
    if k > 0:
        d.text((s(540), s(620)), "?", font=font(FBK, int(300 * sc)), fill=hexc('#9fc2ff', int(255 * k)), anchor='mm')
    text_block(img, [("Ce que disent les scientifiques : personne ne sait où est ce filtre. Ni même s'il existe.", 0.6)], t, 1060, '#ffffff', size=64)

def sc_listen(img, d, t, D):
    bg(d, '#24163d'); stars(d, t); header(d, hexc('#d2b8ff'))
    dish(d, 540, 700, t, col='#d2b8ff')
    text_block(img, ["On n'écoute le ciel que depuis 1960. Pour l'univers, c'est un clin d'œil. Le silence ne prouve rien."], t, 1060, '#ffffff', size=62)

sc_title = scene_title(["GRAND", "FILTRE"], "Scénario d'extinction n°18", color='#3d1a78')
sc_end = scene_end("Bref : le filtre est peut-être derrière nous. La date limite des impôts, elle, est toujours devant.", color='#3d1a78')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_fermi, 4.2), (sc_silence, 4.2), (sc_filter, 4.0),
    (sc_steps, 4.4), (sc_where, 4.0), (sc_boom, 3.8), (sc_joke, 4.4), (sc_mars, 5.0),
    (sc_science, 4.2), (sc_listen, 4.4), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "L'univers est immense. Alors… où sont les extraterrestres ?",
    "Scénario d'extinction numéro dix-huit : le Grand Filtre.",
    "En mille neuf cent cinquante, le physicien Enrico Fermi lance à table : « Mais où sont-ils tous ? »",
    "Notre galaxie compte plus de cent milliards d'étoiles. Et pourtant : silence radio.",
    "L'idée du Grand Filtre : il existe une marche presque impossible à franchir.",
    "La vie, les cellules, l'intelligence, les fusées… Une de ces étapes bloque presque tout le monde.",
    "Si ce filtre est derrière nous : ouf. S'il est devant nous : aïe.",
    "Alors toutes les civilisations s'écrasent contre le mur. Nous compris. Fin de la partie.",
    "Une épreuve que presque personne ne franchit… se garer à Paris un samedi.",
    "Le philosophe Nick Bostrom espère qu'on ne trouvera aucune vie sur Mars. Si la vie est rare, le filtre est derrière nous.",
    "Ce que disent les scientifiques : personne ne sait où est ce filtre. Ni même s'il existe.",
    "On n'écoute le ciel que depuis mille neuf cent soixante. Pour l'univers, c'est un clin d'œil. Le silence ne prouve rien.",
    "Bref : le filtre est peut-être derrière nous. La date limite des impôts, elle, est toujours devant. Abonnez-vous. Tant qu'il y a un demain.",
]
