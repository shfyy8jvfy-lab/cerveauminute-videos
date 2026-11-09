"""Épisode 16 — Mythe : l'inversion des pôles magnétiques qui nous tue.
Sources :
- NASA, « 2012: Magnetic Pole Reversal Happens All The (Geologic) Time » (2011) : les inversions sont fréquentes
  à l'échelle géologique, elles prennent des centaines à des milliers d'années, le champ ne disparaît pas, et
  aucune extinction de masse n'est associée aux inversions dans les fossiles (repris par Space Daily, Universe Today).
- Dernière inversion complète (Brunhes-Matuyama) : il y a environ 780 000 ans (NASA ; USGS).
- Le champ est produit par le fer liquide en mouvement dans le noyau externe (effet dynamo) et dévie les
  particules du vent solaire (ESA Swarm ; NASA).
- Le champ s'est affaibli d'environ 9 % en 200 ans (ESA Swarm).
- Excursion de Laschamp, il y a ~41 000 ans : le champ est tombé à quelques pourcents de sa force actuelle, les pôles
  se sont brièvement inversés ; Homo sapiens et Néandertal ont survécu (ESA / GFZ 2024 ; Space.com ; ScienceAlert).
- Risque réel : perturbations des satellites et des réseaux électriques, pas une extinction (NASA ; Universe Today).
"""
from engine import *

EPISODE = 16
BOOM_SCENE = 6
LEGENDE = """Épisode 16 : l'inversion des pôles magnétiques 🧭🌍

Le champ magnétique de la Terre s'est inversé des centaines de fois, la dernière il y a environ 780 000 ans. Selon la NASA, aucune extinction de masse n'a jamais coïncidé avec une inversion. Et il y a 41 000 ans, quand le champ est tombé à quelques pourcents de sa force, nos ancêtres ont très bien survécu.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #mythe #terre #champmagnetique #science #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def earth(d, cx, cy, r):
    circle(d, cx, cy, r, fill=hexc('#4fa3ff'))
    circle(d, cx - r * 0.3, cy - r * 0.2, r * 0.35, fill=hexc('#6bd17a'))
    circle(d, cx + r * 0.35, cy + r * 0.3, r * 0.25, fill=hexc('#6bd17a'))

def mix(c1, c2, k):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(int(b[j] + (a[j] - b[j]) * k) for j in range(3))

def field(d, cx, cy, r, col, alpha=1.0, t=0.0, bgc='#000000'):
    """Fil rouge : les boucles du champ magnétique autour de la Terre."""
    alpha = max(0, min(1, alpha))
    if alpha <= 0.02: return
    col = mix(col, bgc, alpha); a = 255
    for i, k in enumerate((1.6, 2.1, 2.6)):
        w = r * k * (1 + 0.03 * math.sin(t * 3 + i))
        for side in (-1, 1):
            x0 = cx + side * w * 0.55
            d.ellipse([s(x0 - w * 0.55), s(cy - w * 0.62), s(x0 + w * 0.55), s(cy + w * 0.62)], outline=hexc(col, a), width=s(6))

def magnet(d, cx, cy, flip_k, n_col='#ff4d5a', s_col='#4f8cff'):
    """Aimant vertical N/S ; flip_k de 0 à 1 fait tourner l'aimant de 180°."""
    ang = math.pi * flip_k
    L, Wd = 230, 70
    ux, uy = math.sin(ang), -math.cos(ang)
    px, py = -uy, ux
    def quad(t0, t1, col):
        pts = [(cx + ux * L * t0 + px * Wd, cy + uy * L * t0 + py * Wd),
               (cx + ux * L * t1 + px * Wd, cy + uy * L * t1 + py * Wd),
               (cx + ux * L * t1 - px * Wd, cy + uy * L * t1 - py * Wd),
               (cx + ux * L * t0 - px * Wd, cy + uy * L * t0 - py * Wd)]
        d.polygon([(s(x), s(y)) for x, y in pts], fill=hexc(col))
    quad(0, 1, n_col); quad(-1, 0, s_col)
    f = font(FBK, 70)
    d.text((s(cx + ux * L * 0.55), s(cy + uy * L * 0.55)), "N", font=f, fill=hexc('#ffffff'), anchor='mm')
    d.text((s(cx - ux * L * 0.55), s(cy - uy * L * 0.55)), "S", font=f, fill=hexc('#ffffff'), anchor='mm')

def compass(d, cx, cy, r, ang, ring='#ffffff', needle='#ff4d5a', face='#1d3354'):
    circle(d, cx, cy, r, fill=hexc(face), outline=hexc(ring), width=s(10))
    ux, uy = math.sin(ang), -math.cos(ang)
    px, py = -uy, ux
    tip = (cx + ux * r * 0.8, cy + uy * r * 0.8); tail = (cx - ux * r * 0.8, cy - uy * r * 0.8)
    l = (cx + px * r * 0.14, cy + py * r * 0.14); rr = (cx - px * r * 0.14, cy - py * r * 0.14)
    d.polygon([(s(tip[0]), s(tip[1])), (s(l[0]), s(l[1])), (s(rr[0]), s(rr[1]))], fill=hexc(needle))
    d.polygon([(s(tail[0]), s(tail[1])), (s(l[0]), s(l[1])), (s(rr[0]), s(rr[1]))], fill=hexc(ring))
    circle(d, cx, cy, r * 0.07, fill=hexc('#222222'))

random.seed(16)
PART = [(random.uniform(0, 1), random.uniform(-260, 260)) for _ in range(26)]
def particles(d, t, cx, cy, r, shield, col='#ffd166'):
    for (ph, dy) in PART:
        u = (t * 0.45 + ph) % 1.0
        x = -40 + u * 1200
        y = cy + dy
        stop = cx - r * 2.0
        if shield > 0.5 and x > stop:
            # déviées : elles glissent autour du bouclier
            off = (x - stop) * 0.9
            y = cy + dy + (off if dy >= 0 else -off)
            if abs(y - cy) > 420: continue
        elif shield <= 0.5 and x > cx - r:
            continue
        circle(d, x, y, 9, fill=hexc(col))
        line(d, [(x - 40, y), (x, y)], hexc(col, 120), 4)

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0a1626'); header(d, hexc('#9fc2ff'))
    ang = t * 7 + 2 * math.sin(t * 5)
    compass(d, 540, 630, 260, ang)
    text_block(img, ["Et si le nord devenait le sud… et que ça nous tuait tous ?"], t, 1090, '#ffffff', size=80)

def sc_shield(img, d, t, D):
    bg(d, '#14244a'); stars(d, t); header(d, hexc('#9fe0ff'))
    k = ease((t - 0.5) / 1.2)
    field(d, 540, 630, 110, '#7ff0e0', k, t, '#14244a')
    earth(d, 540, 630, 110)
    circle(d, 540, 630, 45, fill=hexc('#ff9f43', int(255 * (0.7 + 0.3 * math.sin(t * 6)))))
    text_block(img, ["Au cœur de la Terre, du fer liquide tourne. Il crée un champ magnétique : un bouclier invisible."], t, 1060, '#ffffff', size=64)

def sc_deflect(img, d, t, D):
    bg(d, '#102a2e'); header(d, hexc('#7ff0e0'))
    particles(d, t, 700, 630, 90, shield=1.0)
    field(d, 700, 630, 90, '#7ff0e0', 1.0, t)
    earth(d, 700, 630, 90)
    text_block(img, ["Ce bouclier dévie les particules envoyées par le Soleil."], t, 1080, '#ffffff', size=72)

def sc_flip(img, d, t, D):
    bg(d, '#2a1040'); header(d, hexc('#f0b8ff'))
    k = ease((t - 1.0) / 1.4)
    magnet(d, 540, 620, k)
    text_block(img, ["Parfois, ce champ s'inverse : le nord magnétique devient le sud. C'est arrivé des centaines de fois."], t, 1060, '#ffffff', size=64)

def sc_weak(img, d, t, D):
    bg(d, '#2e2a0e'); stars(d, t); header(d, hexc('#ffe08a'))
    k = ease((t - 0.3) / 2.5)
    field(d, 540, 620, 110, '#7ff0e0', 1.0 - 0.75 * k, t, '#2e2a0e')
    earth(d, 540, 620, 110)
    ctext(d, f"-{int(9 * k)} %", 900, 64, '#ffe08a', FBK, ease((t - 0.3) / 0.4))
    text_block(img, ["Pendant une inversion, le bouclier faiblit. Et il a déjà perdu environ 9 % de sa force en 200 ans."], t, 1060, '#ffffff', size=62)

def sc_boom(img, d, t, D):
    bg(d, '#3a0b10'); header(d, hexc('#ffb3bd'))
    shake = 8 * math.sin(t * 45) * (1 if t < 1.0 else 0.2)
    particles(d, t, 540 + shake, 620, 140, shield=0.0, col='#ff9f43')
    earth(d, 540 + shake, 620, 140)
    glow = 0.5 + 0.5 * math.sin(t * 8)
    circle(d, 540 + shake, 620, 150 + 12 * glow, outline=hexc('#ff4d5a'), width=s(10))
    text_block(img, ["La rumeur : sans bouclier, on serait tous grillés.", ("Fin de la partie ?", 1.8)], t, 1060, '#ffffff', size=74)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    compass(d, 540, 620, 240, math.pi + 0.15 * math.sin(t * 3), ring='#8a5a3c', needle='#d94a3a', face='#fff8ee')
    d.text((s(540), s(330)), "N", font=font(FBK, 56), fill=hexc('#8a5a3c'), anchor='mm')
    text_block(img, ["Le seul vrai drame : votre boussole indiquerait le sud…", ("…comme votre sens de l'orientation depuis toujours.", 1.6)], t, 1010, '#2b1a10', size=66)

def sc_myth(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.35)
    sc = 1.6 - 0.6 * k
    if k > 0:
        w, h = 330 * sc, 120 * sc
        d.rounded_rectangle([s(540 - w), s(600 - h), s(540 + w), s(600 + h)], radius=s(30), outline=hexc('#ff4d5a', int(255 * k)), width=s(16))
        d.text((s(540), s(600)), "MYTHE", font=font(FBK, int(150 * sc)), fill=hexc('#ff4d5a', int(255 * k)), anchor='mm')
    text_block(img, [("En vrai : aucune extinction de masse n'a jamais coïncidé avec une inversion des pôles (NASA).", 0.6)], t, 1060, '#ffffff', size=64)

def sc_laschamp(img, d, t, D):
    bg(d, '#24163d'); header(d, hexc('#d2b8ff'))
    k = ease((t - 0.2) / 0.4)
    n = int(min(41000, 41000 * ease(t / 1.2)))
    ctext(d, f"{n:,}".replace(",", " "), 450, 190, '#d2b8ff', FBK, k)
    ctext(d, "ans : le bouclier tombe à quelques %", 700, 46, '#d2b8ff', FM, k)
    text_block(img, [("Il y a 41 000 ans, le champ a presque disparu. Nos ancêtres ont survécu sans problème.", 0.8)], t, 1040, '#ffffff', size=64)

def sc_real(img, d, t, D):
    bg(d, '#1d3a3a'); stars(d, t); header(d, hexc('#a8f0e0'))
    earth(d, 400, 650, 110)
    ang = t * 0.9
    sx, sy = 400 + math.cos(ang) * 260, 650 + math.sin(ang) * 150
    d.rectangle([s(sx - 20), s(sy - 16), s(sx + 20), s(sy + 16)], fill=hexc('#dddddd'))
    d.rectangle([s(sx - 70), s(sy - 10), s(sx - 26), s(sy + 10)], fill=hexc('#4f8cff'))
    d.rectangle([s(sx + 26), s(sy - 10), s(sx + 70), s(sy + 10)], fill=hexc('#4f8cff'))
    blink = int(t * 3) % 2 == 0
    circle(d, 830, 560, 50, fill=hexc('#ffd166' if blink else '#5a5030'))
    d.rectangle([s(812), s(610), s(848), s(660)], fill=hexc('#888888'))
    text_block(img, ["Le vrai risque ? Des satellites et des réseaux électriques un peu perturbés. Gênant. Pas mortel."], t, 1060, '#ffffff', size=62)

def sc_last(img, d, t, D):
    bg(d, '#3a1a08'); header(d, hexc('#ffd166'))
    k = ease((t - 0.2) / 0.4)
    n = int(min(780000, 780000 * ease(t / 1.2)))
    ctext(d, f"{n:,}".replace(",", " "), 450, 170, '#ffd166', FBK, k)
    ctext(d, "ans depuis la dernière inversion", 700, 46, '#ffd166', FM, k)
    text_block(img, [("Personne ne sait quand viendra la prochaine. Mais elle prendrait des siècles, voire des milliers d'années.", 0.8)], t, 1030, '#ffffff', size=60)

sc_title = scene_title(["PÔLES", "INVERSÉS"], "Scénario d'extinction n°16", color='#1f4e8c')
sc_end = scene_end("Bref : le nord peut bien changer de place. Votre avis d'imposition, lui, trouvera toujours votre adresse.", color='#1f4e8c')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_shield, 4.2), (sc_deflect, 3.8), (sc_flip, 4.2),
    (sc_weak, 4.4), (sc_boom, 3.8), (sc_joke, 4.6), (sc_myth, 4.4),
    (sc_laschamp, 4.6), (sc_real, 4.4), (sc_last, 5.0), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Et si le nord devenait le sud… et que ça nous tuait tous ?",
    "Scénario d'extinction numéro seize : les pôles inversés.",
    "Au cœur de la Terre, du fer liquide tourne. Il crée un champ magnétique : un bouclier invisible.",
    "Ce bouclier dévie les particules envoyées par le Soleil.",
    "Parfois, ce champ s'inverse. Le nord magnétique devient le sud. C'est arrivé des centaines de fois.",
    "Pendant une inversion, le bouclier faiblit. Et il a déjà perdu environ neuf pour cent de sa force en deux cents ans.",
    "La rumeur : sans bouclier, on serait tous grillés. Fin de la partie ?",
    "Le seul vrai drame : votre boussole indiquerait le sud… comme votre sens de l'orientation depuis toujours.",
    "En vrai : aucune extinction de masse n'a jamais coïncidé avec une inversion des pôles. C'est la NASA qui le dit.",
    "Il y a quarante et un mille ans, le champ a presque disparu. Nos ancêtres ont survécu sans problème.",
    "Le vrai risque ? Des satellites et des réseaux électriques un peu perturbés. Gênant. Pas mortel.",
    "Sept cent quatre-vingt mille ans depuis la dernière inversion. Personne ne sait quand viendra la prochaine. Mais elle prendrait des siècles.",
    "Bref : le nord peut bien changer de place. Votre avis d'imposition, lui, trouvera toujours votre adresse. Abonnez-vous. Tant qu'il y a un demain.",
]
