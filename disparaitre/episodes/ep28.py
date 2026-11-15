"""Épisode 28 — Mythe : l'alignement des planètes qui détruit la Terre.
Sources :
- Wikipedia, « The Jupiter Effect » : livre de John Gribbin et Stephen Plagemann (1974), best-seller, prédisait
  pour le 10 mars 1982 des catastrophes dont un grand séisme sur la faille de San Andreas ; ce jour-là les planètes
  étaient du même côté du Soleil, réparties sur un arc d'environ 95° ; rien ne s'est produit. Gribbin a désavoué
  la théorie avant la date. Les forces de marée des autres planètes sur la croûte terrestre sont négligeables.
- Geophysical Institute, Univ. of Alaska Fairbanks (Alaska Science Forum, L. Gedney, 8 févr. 1982) : les grandes
  planètes ne s'aligneront pas « comme des soldats à la parade » (écart > 60°) ; Gribbin s'est rétracté dans
  New Scientist le 17 juillet 1980.
- BBC Science Focus (Dr Alastair Gunn, 2017) : les marées sont dues au Soleil et à la Lune ; Vénus, la plus
  influente des planètes, agit au maximum 10 000 fois moins que le Soleil et la Lune réunis ; Jupiter moins
  d'un dixième de Vénus ; effet « imperceptible ».
- BBC Science Focus, CBS News, Live Science (févr. 2025) : « parade » de sept planètes visibles fin février 2025.
- Consensus : aucun effet mesurable d'un alignement sur la Terre ; risque d'extinction nul.
"""
from engine import *

EPISODE = 28
BOOM_SCENE = 4
LEGENDE = """Épisode 28 : l'alignement des planètes 🪐🌍

Mythe ! En 1974, un livre à succès annonçait un séisme géant en Californie pour le 10 mars 1982, à cause des planètes « alignées ». Il ne s'est rien passé. Vénus, la planète qui tire le plus sur nous, agit environ 10 000 fois moins que la Lune et le Soleil réunis (BBC Science Focus).

On va tous disparaître… mais pas aujourd'hui.

#findumonde #planetes #astronomie #mythe #espace #science #vulgarisation #apocalypse"""

# ---------- fil rouge : le Soleil et une rangée de planètes ----------
PLANETS = [  # (rayon, couleur)
    (12, '#a8a29e'), (20, '#fde68a'), (22, '#60a5fa'), (16, '#f87171'),
    (46, '#fdba74'), (38, '#fcd34d'), (28, '#67e8f9'), (27, '#818cf8'),
]

def sun(d, cx, cy, r, a=255):
    circle(d, cx, cy, r + 26, fill=hexc('#fde047', int(a * 0.35)))
    circle(d, cx, cy, r, fill=hexc('#facc15', a))

def row(d, t, x0=150, y=640, spread=0.0, jitter=0.0, k=1.0):
    """Planètes en ligne à droite du Soleil ; spread = dispersion verticale (0 = alignées)."""
    x = x0 + 140
    for i, (r, col) in enumerate(PLANETS):
        x += r + 34
        dy = spread * (130 * math.sin(i * 2.3 + 1)) + jitter * math.sin(t * 30 + i)
        a = ease((k * 8 - i) / 1.0)
        if a > 0:
            circle(d, x, y + dy, r, fill=hexc(col, int(255 * a)))
        x += r

def earth(d, cx, cy, r, a=255):
    circle(d, cx, cy, r, fill=hexc('#3b82f6', a))
    d.ellipse([s(cx - r * 0.5), s(cy - r * 0.55), s(cx + r * 0.15), s(cy + r * 0.05)], fill=hexc('#22c55e', a))
    d.ellipse([s(cx + r * 0.1), s(cy + r * 0.1), s(cx + r * 0.6), s(cy + r * 0.55)], fill=hexc('#22c55e', a))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0f172a'); header(d, hexc('#cbd5e1')); stars(d, t)
    sun(d, 150, 640, 110)
    row(d, t, k=ease(t / 2.0))
    ctext(d, "?", 360, 160, '#fbbf24', FBK, ease((t - 1.6) / 0.4))
    text_block(img, ["Et si un jour, toutes les planètes s'alignaient… et tiraient la Terre en morceaux\u00a0?"], t, 1060, '#ffffff', size=68)

def sc_rumeur(img, d, t, D):
    bg(d, '#312e81'); header(d, hexc('#c7d2fe'))
    sun(d, 150, 560, 110)
    row(d, t, y=560)
    k = ease((t - 0.8) / 1.2)
    for i in range(3):
        x = 300 + i * 200 + 120 * k
        line(d, [(x, 760), (x + 90, 800), (x, 840)], '#fca5a5', 12)
    text_block(img, ["La rumeur\u00a0: en ligne, leurs forces s'additionnent et secouent la Terre."], t, 1060, '#ffffff', size=68)

def sc_livre(img, d, t, D):
    bg(d, '#7c2d12'); header(d, hexc('#fed7aa'))
    w = 360 * ease(t / 0.5) + 1
    d.rounded_rectangle([s(540 - w / 2), s(380), s(540 + w / 2), s(880)], radius=s(24), fill=hexc('#fef3c7'))
    if t > 0.5:
        d.rectangle([s(370), s(380), s(395), s(880)], fill=hexc('#b45309'))
        circle(d, 560, 520, 50, fill=hexc('#facc15'))
        for i in range(4):
            circle(d, 450 + i * 60, 650, 14 + 4 * i, fill=hexc('#ea580c'))
        ctext(d, "10/03/1982", 760, 48, '#7c2d12', FBK)
    ctext(d, "1974", 300, 60, '#fed7aa', FBK)
    text_block(img, ["En 1974, un livre à succès prédit un grand séisme en Californie pour le 10 mars 1982."], t, 1060, '#ffffff', size=64)

def sc_boom(img, d, t, D):
    bg(d, '#111111'); header(d, hexc('#a3a3a3'))
    sh = 14 * math.sin(t * 40) if 1.0 < t < 3.0 else 0
    earth(d, 540 + sh, 620, 230)
    k = ease((t - 1.0) / 1.0)
    if k > 0:
        line(d, [(470 + sh, 400), (560 + sh, 540), (500 + sh, 650), (600 + sh, 760), (560 + sh, 850)], '#ef4444', int(4 + 12 * k))
    text_block(img, ["Le jour J\u00a0: séisme géant, la Terre qui se fissure…", ("…du moins sur le papier.", 2.2)], t, 1060, '#ffffff', size=68)

def sc_rien(img, d, t, D):
    bg(d, '#14532d'); header(d, hexc('#bbf7d0'))
    earth(d, 540, 600, 200 + 6 * math.sin(t * 2))
    ctext(d, "RIEN.", 860, 110, '#ffffff', FBK, ease((t - 0.6) / 0.4))
    text_block(img, ["Résultat\u00a0: rien. Même l'un des auteurs avait renié sa théorie avant la date."], t, 1060, '#ffffff', size=66)

def sc_marees(img, d, t, D):
    bg(d, '#0c4a6e'); header(d, hexc('#bae6fd'))
    b = 30 + 12 * math.sin(t * 2)
    d.ellipse([s(400 - b), s(480), s(680 + b), s(760)], fill=hexc('#38bdf8'))
    earth(d, 540, 620, 120)
    circle(d, 900, 620, 50, fill=hexc('#e5e7eb'))
    sun(d, 120, 620, 70)
    text_block(img, ["Ce qui tire vraiment sur la Terre, ce sont la Lune et le Soleil\u00a0: ce sont eux qui font les marées."], t, 1060, '#ffffff', size=62)

def bars(d, t, vals, labels, cols, y_base=880):
    k = ease((t - 0.3) / 1.2)
    for i, (v, lab, col) in enumerate(zip(vals, labels, cols)):
        x = 340 + i * 400
        hh = max(4, v * k)
        d.rounded_rectangle([s(x - 80), s(y_base - hh), s(x + 80), s(y_base)], radius=s(16), fill=hexc(col))
        f = font(FB, 42); w = d.textlength(lab, font=f)
        d.text((s(x) - w / 2, s(y_base + 20)), lab, font=f, fill=hexc('#ffffff'))

def sc_venus(img, d, t, D):
    bg(d, '#581c87'); header(d, hexc('#e9d5ff'))
    bars(d, t, [420, 1], ["LUNE+SOLEIL", "VÉNUS"], ['#38bdf8', '#fde68a'])
    ctext(d, "÷ 10 000", 290, 80, '#fde68a', FBK, ease((t - 1.5) / 0.4))
    text_block(img, ["Vénus, la planète qui tire le plus sur nous, agit dix mille fois moins que la Lune et le Soleil réunis."], t, 1060, '#ffffff', size=60)

def sc_jupiter(img, d, t, D):
    bg(d, '#9a3412'); header(d, hexc('#ffedd5'))
    circle(d, 540, 620, 230, fill=hexc('#fdba74'))
    for i, yy in enumerate([520, 590, 660, 720]):
        d.rectangle([s(320), s(yy), s(760), s(yy + 22)], fill=hexc('#c2410c' if i % 2 else '#fed7aa'))
    d.ellipse([s(600), s(650), s(690), s(700)], fill=hexc('#b91c1c'))
    circle(d, 540, 620, 230, outline=hexc('#9a3412'), width=12)
    ctext(d, "÷ 10", 900, 80, '#ffffff', FBK, ease((t - 1.0) / 0.4))
    text_block(img, ["Et Jupiter, la géante\u00a0? Encore dix fois moins que Vénus. Une plume."], t, 1060, '#ffffff', size=66)

def sc_arc(img, d, t, D):
    bg(d, '#1e3a8a'); header(d, hexc('#bfdbfe'))
    cx, cy = 540, 640
    sun(d, cx, cy, 60)
    for i, (r, col) in enumerate(PLANETS):
        rr = 110 + i * 32
        circle(d, cx, cy, rr, outline=hexc('#3b5bb5'), width=2)
        ang = -math.pi / 2 + (i / 7) * (95 / 180 * math.pi) * ease((t - 0.3) / 1.2)
        circle(d, cx + rr * math.cos(ang), cy + rr * math.sin(ang), max(8, r * 0.45), fill=hexc(col))
    text_block(img, ["Et elles ne font jamais une vraie ligne\u00a0: en 1982, elles étaient étalées sur un quart de cercle."], t, 1060, '#ffffff', size=62)

def sc_2025(img, d, t, D):
    bg(d, '#134e4a'); header(d, hexc('#ccfbf1')); stars(d, t, col='#ccfbf1')
    for i, (r, col) in enumerate(PLANETS[:2] + PLANETS[3:]):
        a = ease((t - 0.2 - i * 0.2) / 0.3)
        x = 160 + i * 127; y = 540 - 160 * math.sin(i / 6 * math.pi)
        if a > 0: circle(d, x, y, max(12, r * 0.6), fill=hexc(col, int(255 * a)))
    d.rectangle([s(0), s(820), s(W), s(960)], fill=hexc('#042f2e'))
    earth(d, 540, 880, 70, int(255 * ease((t - 2.0) / 0.4)))
    text_block(img, ["Fin février 2025\u00a0: sept planètes visibles le même soir. La Terre\u00a0? Toujours là."], t, 1060, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#fef3c7'); header(d, hexc('#92400e'))
    a = 0.25 + 0.08 * math.sin(t * 3)
    cx, cy = 540, 760
    # silhouette simple : cou tendu vers le ciel
    d.rounded_rectangle([s(cx - 120), s(cy), s(cx + 120), s(cy + 200)], radius=s(60), fill=hexc('#fdba74'))
    hx, hy = cx + 140 * math.sin(a), cy - 120
    line(d, [(cx, cy + 20), (hx, hy)], '#fdba74', 70)
    circle(d, hx, hy - 40, 80, fill=hexc('#fdba74'))
    for i in range(4):
        circle(d, 250 + i * 190, 360 + 30 * math.sin(i + t), 18, fill=hexc('#f59e0b'))
    text_block(img, ["Le seul vrai danger d'un alignement\u00a0: le torticolis, à force de regarder le ciel."], t, 1060, '#3b2105', size=66)

def sc_science(img, d, t, D):
    bg(d, '#1b4332'); header(d, hexc('#b7e4c7'))
    k = ease((t - 0.3) / 0.5)
    ctext(d, "RISQUE D'EXTINCTION", 470, 52, '#b7e4c7', FB, k)
    ctext(d, "ZÉRO", 560, 150, '#ffffff', FBK, k)
    text_block(img, ["Ce que disent les scientifiques\u00a0: effet sur la Terre quasi nul. C'est un mythe."], t, 1060, '#ffffff', size=64)

sc_title = scene_title(["PLANÈTES", "ALIGNÉES"], "Scénario d'extinction n°28", color='#6d28d9')
sc_end = scene_end("Bref\u00a0: planètes alignées ou pas, vos impôts, eux, tomberont pile à l'heure.", color='#6d28d9')

SCENES = [
    (sc_hook, 3.6), (sc_title, 2.4), (sc_rumeur, 4.0), (sc_livre, 4.4), (sc_boom, 4.6),
    (sc_rien, 4.0), (sc_marees, 4.4), (sc_venus, 4.6), (sc_jupiter, 3.8), (sc_arc, 4.4),
    (sc_2025, 4.2), (sc_joke, 3.8), (sc_science, 4.0), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Et si un jour, toutes les planètes s'alignaient… et tiraient la Terre en morceaux ?",
    "Scénario d'extinction numéro vingt-huit : l'alignement des planètes.",
    "La rumeur : en ligne, leurs forces s'additionnent et secouent la Terre.",
    "En mille neuf cent soixante-quatorze, un livre à succès prédit un grand séisme en Californie pour le dix mars mille neuf cent quatre-vingt-deux.",
    "Le jour J : séisme géant, la Terre qui se fissure… du moins sur le papier.",
    "Résultat : rien. Même l'un des auteurs avait renié sa théorie avant la date.",
    "Ce qui tire vraiment sur la Terre, ce sont la Lune et le Soleil : ce sont eux qui font les marées.",
    "Vénus, la planète qui tire le plus sur nous, agit dix mille fois moins que la Lune et le Soleil réunis.",
    "Et Jupiter, la géante ? Encore dix fois moins que Vénus. Une plume.",
    "Et elles ne font jamais une vraie ligne : en mille neuf cent quatre-vingt-deux, elles étaient étalées sur un quart de cercle.",
    "Fin février deux mille vingt-cinq : sept planètes visibles le même soir. La Terre ? Toujours là.",
    "Le seul vrai danger d'un alignement : le torticolis, à force de regarder le ciel.",
    "Ce que disent les scientifiques : effet sur la Terre quasi nul. C'est un mythe.",
    "Bref : planètes alignées ou pas, vos impôts, eux, tomberont pile à l'heure. Abonnez-vous. Tant qu'il y a un demain.",
]
