"""Épisode 21 — L'hypothèse de la simulation qu'on éteint.
Sources :
- Nick Bostrom, « Are You Living in a Computer Simulation? », Philosophical Quarterly, vol. 53, 2003
  (simulation-argument.com) : trilemme — soit les civilisations disparaissent avant de savoir simuler des mondes,
  soit elles ne le font pas, soit nous vivons presque certainement dans une simulation.
- Nick Bostrom, « Existential Risks », Journal of Evolution and Technology, 2002 : « nous vivons dans une simulation
  et elle est arrêtée » figure parmi les risques existentiels envisagés.
- Robin Hanson (économiste), « How to Live in a Simulation », Journal of Evolution and Technology, 2001 :
  conseil (en partie ironique) d'être intéressant pour que la simulation continue.
- Beane, Davoudi & Savage, « Constraints on the Universe as a Numerical Simulation », 2012 (arXiv:1210.1847) :
  propose de chercher une « grille » via les rayons cosmiques ; aucune signature détectée à ce jour.
- Franco Vazza (Univ. Bologne), Frontiers in Physics, 2025 (doi 10.3389/fphy.2025.1561873) : simuler l'univers,
  ou même la Terre en haute résolution, demanderait une énergie colossale, hors de portée physique.
- Consensus (Live Science, Wikipedia « Simulation hypothesis ») : hypothèse philosophique, non testable à ce jour,
  aucun risque mesurable.
"""
from engine import *

EPISODE = 21
BOOM_SCENE = 6
LEGENDE = """Épisode 21 : et si notre univers était une simulation… qu'on pourrait éteindre ? 🖥️⏻

En 2003, le philosophe Nick Bostrom a proposé un raisonnement célèbre : si une civilisation sait simuler des mondes, il pourrait y avoir bien plus de copies que d'originaux. Mais en 2025, un astrophysicien (Frontiers in Physics) a calculé que simuler l'univers demanderait une énergie délirante. Et personne n'a jamais trouvé le moindre « pixel ».

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #simulation #matrice #philosophie #physique #science #vulgarisation"""

# ---------- fil rouge : un écran avec une petite Terre dedans ----------
def monitor(d, cx, cy, w, t, power=1.0, frame_col='#e9ecef', glitch=0.0):
    h = w * 0.66
    d.rounded_rectangle([s(cx - w / 2), s(cy - h / 2), s(cx + w / 2), s(cy + h / 2)], radius=s(w * 0.06), fill=hexc(frame_col))
    m = w * 0.05
    sx0, sy0, sx1, sy1 = cx - w / 2 + m, cy - h / 2 + m, cx + w / 2 - m, cy + h / 2 - m
    d.rounded_rectangle([s(sx0), s(sy0), s(sx1), s(sy1)], radius=s(w * 0.03), fill=hexc('#0b132b'))
    # pied
    d.rectangle([s(cx - w * 0.06), s(cy + h / 2), s(cx + w * 0.06), s(cy + h / 2 + w * 0.1)], fill=hexc(frame_col))
    d.rounded_rectangle([s(cx - w * 0.2), s(cy + h / 2 + w * 0.09), s(cx + w * 0.2), s(cy + h / 2 + w * 0.13)], radius=s(8), fill=hexc(frame_col))
    if power <= 0:
        return
    a = int(255 * power)
    # petites étoiles
    for i in range(14):
        x = sx0 + (sx1 - sx0) * ((i * 0.37) % 1)
        y = sy0 + (sy1 - sy0) * ((i * 0.61 + 0.1) % 1)
        circle(d, x, y, max(1.5, w * 0.006), fill=hexc('#ffffff', int(a * (0.5 + 0.5 * math.sin(t * 3 + i)))))
    # Terre en pixels
    ex, ey, R = cx, cy, h * 0.3
    px = max(6, w * 0.03)
    n = int(R / px) + 1
    for ix in range(-n, n + 1):
        for iy in range(-n, n + 1):
            x, y = ex + ix * px, ey + iy * px
            if (ix * px) ** 2 + (iy * px) ** 2 > R * R:
                continue
            land = math.sin(ix * 0.7 + t * 1.5) + math.cos(iy * 0.9) > 0.6
            col = '#52b788' if land else '#4895ef'
            off = glitch * 40 * math.sin(iy * 3 + t * 20) if glitch else 0
            d.rectangle([s(x + off), s(y), s(x + off + px - 1), s(y + px - 1)], fill=hexc(col, a))

def power_button(d, cx, cy, r, col, alpha=255, lit=True):
    circle(d, cx, cy, r, fill=hexc(col, alpha))
    c = '#ffffff' if lit else '#999999'
    d.arc([s(cx - r * 0.5), s(cy - r * 0.5), s(cx + r * 0.5), s(cy + r * 0.5)], start=-60, end=240, fill=hexc(c, alpha), width=s(r * 0.12))
    line(d, [(cx, cy - r * 0.62), (cx, cy - r * 0.12)], hexc(c, alpha), r * 0.12)

def label(d, txt, x, y, col, size=40):
    d.text((s(x), s(y)), txt, font=font(FB, size), fill=hexc(col), anchor='mm')

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#14213d'); header(d, hexc('#a2d2ff')); stars(d, t)
    w = 520 + 60 * ease(t / D)
    monitor(d, 540, 600, w, t)
    text_block(img, ["Et si tout ça n'était qu'un programme ?", ("Et si quelqu'un l'éteignait ?", 1.4)], t, 1080, '#ffffff', size=76)

def sc_idea(img, d, t, D):
    bg(d, '#1d3557'); header(d, hexc('#a8dadc'))
    monitor(d, 540, 590, 620, t)
    for i in range(6):  # lignes de code qui défilent
        y = 330 + ((i * 40 + t * 60) % 240)
        line(d, [(120, y), (120 + 60 + 30 * (i % 3), y)], hexc('#80ffdb', 160), 8)
        line(d, [(900, y), (900 + 40 + 20 * (i % 2), y)], hexc('#80ffdb', 160), 8)
    text_block(img, ["L'idée : notre univers serait un programme, sur l'ordinateur d'une civilisation bien plus avancée."], t, 1060, '#ffffff', size=62)

def sc_bostrom(img, d, t, D):
    bg(d, '#3a0ca3'); header(d, hexc('#cdb4db'))
    k = ease((t - 0.6) / 1.8)
    nmax = 1 + int(11 * k)
    pos = [(540, 600, 360)] + [(160 + (i % 4) * 253, 380 + (i // 4) * 200, 150) for i in range(12)]
    if nmax <= 1:
        monitor(d, *pos[0], t)
    else:
        for (x, y, w) in pos[1:nmax + 1]:
            monitor(d, x, y, w, t)
    text_block(img, ["En 2003, le philosophe Nick Bostrom raisonne : si on sait simuler des mondes, on en simulera des milliards."], t, 1060, '#ffffff', size=62)

def sc_odds(img, d, t, D):
    bg(d, '#240046'); header(d, hexc('#e0aaff'))
    monitor(d, 220, 600, 240, t, frame_col='#ffd166')
    label(d, "1 ORIGINAL", 220, 790, '#ffd166', 38)
    for i in range(9):
        x = 520 + (i % 3) * 170; y = 440 + (i // 3) * 130
        monitor(d, x, y, 120, t + i)
    label(d, "DES MILLIARDS DE COPIES", 690, 850, '#e0aaff', 38)
    text_block(img, ["Alors, côté probabilités, on serait plus sûrement dans une copie que dans l'original."], t, 1060, '#ffffff', size=64)

def sc_risk(img, d, t, D):
    bg(d, '#5f0f40'); header(d, hexc('#ffb3c6'))
    monitor(d, 400, 600, 440, t)
    pulse = 1 + 0.08 * math.sin(t * 6)
    power_button(d, 820, 640, 90 * pulse, '#e63946')
    label(d, "OFF", 820, 770, '#ffb3c6', 44)
    text_block(img, ["Le danger : une simulation, ça coûte cher.", ("Un jour, quelqu'un pourrait appuyer sur OFF.", 1.5)], t, 1060, '#ffffff', size=68)

def sc_boom(img, d, t, D):
    bg(d, '#000000'); header(d, hexc('#555555'))
    if t < 1.2:
        monitor(d, 540, 600, 600, t, power=1.0, glitch=ease(t / 1.2))
    elif t < 1.6:
        k = (t - 1.2) / 0.4
        monitor(d, 540, 600, 600, t, power=0)
        d.rectangle([s(270), s(600 - 3 * (1 - k)), s(810), s(600 + 3 * (1 - k))], fill=hexc('#ffffff', int(255 * (1 - k))))
    else:
        monitor(d, 540, 600, 600, t, power=0, frame_col='#2b2d42')
    text_block(img, ["Pas d'explosion. Pas de douleur.", ("Juste… plus rien.", 1.8)], t, 1080, '#ffffff', size=78)

def sc_bugs(img, d, t, D):
    bg(d, '#e76f51'); header(d, hexc('#ffe8d6'))
    # imprimante qui clignote
    d.rounded_rectangle([s(330), s(520), s(750), s(760)], radius=s(30), fill=hexc('#f1faee'))
    d.rectangle([s(400), s(440), s(680), s(520)], fill=hexc('#dee2e6'))
    blink = int(t * 3) % 2 == 0
    circle(d, 690, 580, 20, fill=hexc('#e63946' if blink else '#6c757d'))
    label(d, "ERREUR", 520, 650, '#e63946', 52)
    text_block(img, ["Avantage : ça expliquerait enfin pourquoi l'imprimante plante toujours le jour où vous en avez besoin."], t, 1040, '#ffffff', size=62)

def sc_hanson(img, d, t, D):
    bg(d, '#2a9d8f'); header(d, hexc('#e9f5db'))
    monitor(d, 540, 560, 520, t)
    for i in range(5):  # petites étoiles de « note »
        x = 260 + i * 140
        circle(d, x, 860 + 10 * math.sin(t * 4 + i), 22, fill=hexc('#ffd166' if i < 4 else '#ffffff', 230))
    text_block(img, ["Un économiste a même écrit un conseil, en 2001 : soyez intéressants…", ("…pour qu'on ne vous éteigne pas.", 1.6)], t, 1060, '#ffffff', size=64)

def sc_pixels(img, d, t, D):
    bg(d, '#003049'); header(d, hexc('#8ecae6')); stars(d, t)
    # loupe sur une grille
    for i in range(7):
        line(d, [(260 + i * 90, 340), (260 + i * 90, 880)], hexc('#8ecae6', 70), 3)
        line(d, [(260, 340 + i * 90), (800, 340 + i * 90)], hexc('#8ecae6', 70), 3)
    lx = 530 + 140 * math.sin(t * 1.4); ly = 600 + 90 * math.cos(t * 1.1)
    circle(d, lx, ly, 120, outline=hexc('#ffd166'), width=14)
    line(d, [(lx + 85, ly + 85), (lx + 170, ly + 170)], '#ffd166', 26)
    label(d, "?", lx, ly, '#ffffff', 90)
    text_block(img, ["Des physiciens ont cherché des « pixels » dans l'univers, grâce aux rayons cosmiques.", ("Rien trouvé.", 1.8)], t, 1060, '#ffffff', size=62)

def sc_energy(img, d, t, D):
    bg(d, '#6a040f'); header(d, hexc('#ffccd5'))
    monitor(d, 400, 600, 400, t)
    # prise électrique + éclairs
    d.rounded_rectangle([s(720), s(520), s(900), s(700)], radius=s(30), fill=hexc('#f8f9fa'))
    d.rounded_rectangle([s(772), s(580), s(788), s(640)], radius=s(6), fill=hexc('#343a40')); d.rounded_rectangle([s(832), s(580), s(848), s(640)], radius=s(6), fill=hexc('#343a40'))
    for k in range(3):
        x = 640 + k * 30; ph = (t * 4 + k) % 1
        line(d, [(x, 470 + ph * 40), (x + 20, 520), (x - 10, 560), (x + 15, 610)], hexc('#ffd60a', int(255 * (1 - ph))), 8)
    n = int(99 * ease(t / 1.5))
    label(d, f"{n} 000 000 000 000…", 540, 380, '#ffd60a', 60)
    text_block(img, ["En 2025, un astrophysicien fait les comptes : simuler l'univers demanderait une énergie complètement délirante."], t, 1060, '#ffffff', size=62)

def sc_science(img, d, t, D):
    bg(d, '#283618'); header(d, hexc('#dde5b6'))
    monitor(d, 540, 590, 480, t)
    k = ease((t - 1.0) / 0.4)
    d.rounded_rectangle([s(300), s(330), s(780), s(420)], radius=s(24), fill=hexc('#606c38', int(255 * k)))
    if k > 0.5:
        label(d, "NON TESTABLE", 540, 375, '#ffffff', 46)
    text_block(img, ["Ce que disent les scientifiques : une idée de philosophe, impossible à tester.", ("Risque mesurable : aucun.", 1.7)], t, 1060, '#ffffff', size=64)

sc_title = scene_title(["ON NOUS", "ÉTEINT ?"], "Scénario d'extinction n°21", color='#0077b6')
sc_end = scene_end("Bref : si l'univers s'éteint, vous serez peut-être dispensé d'impôts. Peut-être.", color='#0077b6')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_idea, 4.4), (sc_bostrom, 4.6), (sc_odds, 4.2),
    (sc_risk, 4.2), (sc_boom, 3.6), (sc_bugs, 4.4), (sc_hanson, 4.2), (sc_pixels, 4.4),
    (sc_energy, 4.4), (sc_science, 4.2), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Et si tout ça n'était qu'un programme ? Et si quelqu'un l'éteignait ?",
    "Scénario d'extinction numéro vingt et un : on nous éteint ?",
    "L'idée : notre univers serait un programme, sur l'ordinateur d'une civilisation bien plus avancée.",
    "En deux mille trois, le philosophe Nick Bostrom raisonne : si on sait simuler des mondes, on en simulera des milliards.",
    "Alors, côté probabilités, on serait plus sûrement dans une copie que dans l'original.",
    "Le danger : une simulation, ça coûte cher. Un jour, quelqu'un pourrait appuyer sur OFF.",
    "Pas d'explosion. Pas de douleur. Juste… plus rien.",
    "Avantage : ça expliquerait enfin pourquoi l'imprimante plante toujours le jour où vous en avez besoin.",
    "Un économiste a même écrit un conseil, en deux mille un : soyez intéressants… pour qu'on ne vous éteigne pas.",
    "Des physiciens ont cherché des pixels dans l'univers, grâce aux rayons cosmiques. Rien trouvé.",
    "En deux mille vingt-cinq, un astrophysicien fait les comptes : simuler l'univers demanderait une énergie complètement délirante.",
    "Ce que disent les scientifiques : une idée de philosophe, impossible à tester. Risque mesurable : aucun.",
    "Bref : si l'univers s'éteint, vous serez peut-être dispensé d'impôts. Peut-être. Abonnez-vous. Tant qu'il y a un demain.",
]
