"""Épisode 20 — La collision avec Andromède (spoiler : pas dangereuse).
Sources :
- Andromède (M31) : à environ 2,5 millions d'années-lumière, se rapproche de la Voie lactée à environ 110 km/s
  (≈ 400 000 km/h) ; mesures Hubble 2012 (van der Marel et al.) prévoyant un choc frontal dans ~4 milliards d'années ;
  les étoiles sont si espacées qu'elles ne se percuteraient pratiquement pas, le Soleil serait seulement déplacé
  (NASA, « NASA's Hubble Shows Milky Way is Destined for Head-On Collision », 31 mai 2012 ; UC Santa Cruz ; Phys.org).
- Sawala et al., Nature Astronomy, 2 juin 2025 (données Hubble + Gaia, ~100 000 simulations) : environ 50 % de chances
  de fusion dans les 10 prochains milliards d'années, ~2 % seulement dans les 4-5 prochains milliards d'années
  (AP / Washington Times 2 juin 2025 ; EarthSky ; Sci.News ; Universe Today).
- Surnom « Milkomeda » / « Lactomède » pour la galaxie fusionnée (Cox & Loeb, 2008).
- Le Soleil, de plus en plus lumineux, rendra la Terre inhabitable (évaporation des océans) dans environ un milliard
  d'années (NASA ; consensus en astrophysique), bien avant toute collision.
- Consensus : aucune menace pour l'humanité.
"""
from engine import *

EPISODE = 20
BOOM_SCENE = 6
LEGENDE = """Épisode 20 : la galaxie d'Andromède fonce sur nous. Faut-il paniquer ? 🌌💥

Andromède se rapproche à environ 110 km par seconde. En 2012, la NASA annonçait un choc dans 4 milliards d'années. Mais une étude de 2025 (Nature Astronomy, données Hubble + Gaia) ne donne plus qu'environ une chance sur deux en 10 milliards d'années. Et même en cas de choc, les étoiles ne se cogneraient presque jamais.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #andromede #voielactee #galaxie #astronomie #espace #science #vulgarisation"""

# ---------- fil rouge : deux galaxies spirales ----------
random.seed(20)
ARM = [(random.uniform(0.08, 1.0), random.uniform(-0.25, 0.25), random.uniform(2.5, 6), random.random()) for _ in range(150)]

def galaxy(d, cx, cy, R, t, col='#bde0fe', core='#fff3b0', tilt=0.45, spin=0.25, alpha=255):
    """Galaxie spirale vue en biais : deux bras de points + bulbe lumineux."""
    for i, (rr, jit, sz, ph) in enumerate(ARM):
        arm = i % 2
        a = rr * 5.0 + arm * math.pi + t * spin + jit
        x = cx + math.cos(a) * rr * R
        y = cy + math.sin(a) * rr * R * tilt
        tw = 0.65 + 0.35 * math.sin(t * 3 + ph * 6)
        circle(d, x, y, 1.6 * sz * (R / 260) ** 0.5, fill=hexc(col, int(alpha * tw * (1.05 - rr * 0.5))))
    for k, rk in enumerate((0.16, 0.10, 0.05)):
        d.ellipse([s(cx - R * rk), s(cy - R * rk * tilt * 1.4), s(cx + R * rk), s(cy + R * rk * tilt * 1.4)],
                  fill=hexc(core, int(alpha * (0.25 + 0.3 * k))))

def milky(d, cx, cy, R, t, alpha=255):
    galaxy(d, cx, cy, R, t, col='#caf0f8', core='#fff3b0', tilt=0.42, spin=0.25, alpha=alpha)

def andro(d, cx, cy, R, t, alpha=255):
    galaxy(d, cx, cy, R, t, col='#ffc8dd', core='#ffe5ec', tilt=0.55, spin=-0.22, alpha=alpha)

def label(d, txt, x, y, col, size=40):
    d.text((s(x), s(y)), txt, font=font(FB, size), fill=hexc(col), anchor='mm')

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b0c2a'); header(d, hexc('#b8c0ff')); stars(d, t)
    k = ease(t / D)
    milky(d, 300, 640, 210, t)
    andro(d, 860 - 120 * k, 520 + 40 * k, 160 + 40 * k, t)
    text_block(img, ["Une galaxie géante fonce droit sur nous.", ("Faut-il paniquer ?", 1.4)], t, 1080, '#ffffff', size=76)

def sc_andromeda(img, d, t, D):
    bg(d, '#1a0b2e'); header(d, hexc('#e0aaff')); stars(d, t)
    andro(d, 540, 620, 300, t)
    label(d, "ANDROMÈDE", 540, 860, '#ffc8dd', 44)
    text_block(img, ["Andromède : notre grande voisine. Des centaines de milliards d'étoiles, à 2,5 millions d'années-lumière."], t, 1060, '#ffffff', size=62)

def sc_speed(img, d, t, D):
    bg(d, '#002a32'); header(d, hexc('#90e0ef')); stars(d, t)
    milky(d, 250, 620, 160, t)
    x = 860 - 60 * ease(t / D)
    andro(d, x, 620, 150, t)
    for k in range(3):
        xx = x + 170 + k * 50 + 20 * math.sin(t * 10 + k)
        line(d, [(xx, 580 + k * 40), (xx + 90, 580 + k * 40)], hexc('#ffc8dd', 160 - k * 40), 8)
    n = int(110 * ease(t / 1.2))
    d.text((s(540), s(380)), f"{n} km/s", font=font(FBK, 96), fill=hexc('#ffd166'), anchor='mm')
    text_block(img, ["Elle se rapproche à environ 110 kilomètres… par seconde.", ("Paris-Marseille en 6 secondes.", 1.6)], t, 1060, '#ffffff', size=66)

def sc_2012(img, d, t, D):
    bg(d, '#3d0e61'); header(d, hexc('#e0aaff')); stars(d, t)
    milky(d, 400, 620, 190, t); andro(d, 690, 600, 170, t)
    k = ease((t - 0.6) / 0.4)
    d.rounded_rectangle([s(330), s(330), s(750), s(430)], radius=s(24), fill=hexc('#ff4d6d', int(255 * k)))
    label(d, "CHOC : 100 %", 540, 380, '#ffffff', 52) if k > 0.5 else None
    text_block(img, ["En 2012, les mesures du télescope Hubble semblaient formelles : choc frontal dans 4 milliards d'années."], t, 1060, '#ffffff', size=62)

def sc_2025(img, d, t, D):
    bg(d, '#1b4332'); header(d, hexc('#b7e4c7')); stars(d, t)
    milky(d, 400, 640, 190, t); andro(d, 690, 620, 170, t)
    # pièce qui tourne : pile ou face
    w = abs(math.cos(t * 5)) * 90 + 6
    d.ellipse([s(540 - w), s(300), s(540 + w), s(480)], fill=hexc('#ffd166'), outline=hexc('#b08900'), width=s(6))
    text_block(img, ["En 2025, nouveau calcul avec plus de données : seulement une chance sur deux… en 10 milliards d'années."], t, 1060, '#ffffff', size=62)

def sc_boom(img, d, t, D):
    bg(d, '#370617'); header(d, hexc('#ffb3c1')); stars(d, t)
    k = ease(t / 1.6)
    milky(d, 300 + 200 * k, 640, 200, t * 2, alpha=int(255 - 80 * k))
    andro(d, 780 - 200 * k, 600 + 30 * k, 180, t * 2, alpha=int(255 - 80 * k))
    if t > 1.4:
        g = ease((t - 1.4) / 0.8)
        for j in range(3):
            rg = g * (180 + 70 * j)
            d.ellipse([s(540 - rg), s(620 - rg * 0.5), s(540 + rg), s(620 + rg * 0.5)], outline=hexc('#ffd6a5', int(200 * (1 - j * 0.3))), width=s(6))
    text_block(img, ["Et si ça arrive ? Les deux galaxies se traversent…", ("…puis fusionnent en une seule.", 1.5)], t, 1060, '#ffffff', size=68)

def sc_empty(img, d, t, D):
    bg(d, '#03045e'); header(d, hexc('#90e0ef'))
    for i in range(5):
        x = 180 + i * 180
        circle(d, x, 500 + 30 * math.sin(t * 2 + i), 10, fill=hexc('#caf0f8'))
        circle(d, x + 90, 760 - 30 * math.sin(t * 2 + i), 10, fill=hexc('#ffc8dd'))
    k = ease((t - 0.8) / 0.5)
    d.text((s(540), s(380)), "beaucoup de vide", font=font(FB, 52), fill=hexc('#ffd166', int(255 * k)), anchor='mm')
    text_block(img, ["Mais les étoiles sont si espacées qu'elles ne se cognent presque jamais.", ("Le Soleil serait juste déplacé.", 1.6)], t, 1060, '#ffffff', size=64)

def sc_joke(img, d, t, D):
    bg(d, '#3c1642'); header(d, hexc('#ffc8dd'))
    milky(d, 540, 560, 230, t)
    d.rounded_rectangle([s(270), s(780), s(810), s(890)], radius=s(30), fill=hexc('#ff4d6d'))
    k = ease((t - 1.2) / 0.4)
    label(d, "LACTOMÈDE ?", 540, 835, '#ffffff', 56) if k > 0.3 else label(d, "VOIE LACTÉE", 540, 835, '#ffffff', 56)
    text_block(img, ["Le seul vrai drame : la galaxie fusionnée a déjà un surnom.", ("« Lactomède ». Courage.", 1.6)], t, 1040, '#ffffff', size=68)

def sc_sky(img, d, t, D):
    bg(d, '#10002b'); header(d, hexc('#c77dff')); stars(d, t)
    andro(d, 540, 520, 400, t * 0.5)
    d.rectangle([s(0), s(860), s(W), s(960)], fill=hexc('#05001a'))
    for x in (200, 760):
        d.polygon([(s(x), s(860)), (s(x + 60), s(760)), (s(x + 120), s(860))], fill=hexc('#05001a'))
    text_block(img, ["En prime : un ciel de nuit spectaculaire, avec une galaxie géante au-dessus de nos têtes."], t, 1060, '#ffffff', size=64)

def sc_sun(img, d, t, D):
    bg(d, '#9d0208'); header(d, hexc('#ffd6a5'))
    r = 150 + 25 * ease(t / D) + 6 * math.sin(t * 4)
    circle(d, 700, 560, r, fill=hexc('#ffba08'))
    circle(d, 700, 560, r * 0.7, fill=hexc('#ffd166'))
    circle(d, 300, 640, 55, fill=hexc('#4ea8de'))
    circle(d, 300, 640, 55 * (1 - 0.6 * ease(t / D)), fill=hexc('#2a9d8f'))
    text_block(img, ["Le vrai problème arrive bien avant : dans environ un milliard d'années, le Soleil sera trop chaud pour nos océans."], t, 1040, '#ffffff', size=60)

def sc_science(img, d, t, D):
    bg(d, '#023047'); header(d, hexc('#8ecae6')); stars(d, t)
    milky(d, 400, 620, 170, t); andro(d, 700, 600, 150, t)
    text_block(img, ["Ce que disent les scientifiques : risque pour l'humanité ? Zéro.", ("Et le choc n'est même plus certain.", 1.6)], t, 1060, '#ffffff', size=64)

sc_title = scene_title(["CHOC DES", "GALAXIES"], "Scénario d'extinction n°20", color='#5a189a')
sc_end = scene_end("Bref : la galaxie fusionnera peut-être. Vos impôts, eux, c'est certain.", color='#5a189a')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_andromeda, 4.6), (sc_speed, 4.2), (sc_2012, 4.4),
    (sc_2025, 4.6), (sc_boom, 3.8), (sc_empty, 4.4), (sc_joke, 4.0), (sc_sky, 4.0),
    (sc_sun, 4.6), (sc_science, 4.0), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Une galaxie géante fonce droit sur nous. Faut-il paniquer ?",
    "Scénario d'extinction numéro vingt : le choc des galaxies.",
    "Andromède : notre grande voisine. Des centaines de milliards d'étoiles, à deux millions et demi d'années-lumière.",
    "Elle se rapproche à environ cent dix kilomètres… par seconde. Paris-Marseille en six secondes.",
    "En deux mille douze, le télescope Hubble semblait formel : choc frontal dans quatre milliards d'années.",
    "En deux mille vingt-cinq, nouveau calcul : seulement une chance sur deux… en dix milliards d'années.",
    "Et si ça arrive ? Les deux galaxies se traversent… puis fusionnent en une seule.",
    "Mais les étoiles sont si espacées qu'elles ne se cognent presque jamais. Le Soleil serait juste déplacé.",
    "Le seul vrai drame : la galaxie fusionnée a déjà un surnom. Lactomède. Courage.",
    "En prime : un ciel de nuit spectaculaire, avec une galaxie géante au-dessus de nos têtes.",
    "Le vrai problème arrive bien avant : dans environ un milliard d'années, le Soleil sera trop chaud pour nos océans.",
    "Ce que disent les scientifiques : risque pour l'humanité ? Zéro. Et le choc n'est même plus certain.",
    "Bref : la galaxie fusionnera peut-être. Vos impôts, eux, c'est certain. Abonnez-vous. Tant qu'il y a un demain.",
]
