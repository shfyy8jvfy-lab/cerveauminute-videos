"""Épisode 51 — Une comète géante venue du nuage d'Oort.
Sources :
- NASA Science, « Oort Cloud: Facts » (màj janv. 2025) : nuage d'Oort entre ~2 000-5 000 et 10 000-100 000 UA,
  région la plus lointaine du système solaire ; « des centaines de milliards, voire des milliers de milliards »
  de corps glacés ; parfois, quelque chose dérange l'orbite de l'un d'eux et il entame une longue chute vers le Soleil.
- NASA / Hubble, « Hubble Confirms Largest Comet Nucleus Ever Seen » (avril 2022, màj 2025) ; aussi NPR et Space.com
  (13/04/2022) : C/2014 UN271 (Bernardinelli-Bernstein), noyau d'environ 80 miles (~130 km), environ 50 fois plus
  gros que la plupart des comètes connues ; tombe vers le Soleil depuis plus d'un million d'années ;
  ne s'approchera pas à moins de 1 milliard de miles (~1,6 milliard de km) du Soleil, en 2031 ; aucun danger.
- ESA Gaia, « Close encounters of the stellar kind » (2017) : l'étoile Gliese 710 passera dans 1,3 million d'années
  à ~16 000 UA, dans le nuage d'Oort, et pourrait « potentiellement » envoyer des pluies de comètes.
- Aerospace America (AIAA), « The comet conundrum » (févr. 2023) : comètes à longue période ~65 km/s dans le système
  solaire interne ; quasi invisibles avant d'approcher du Soleil ; scénario d'alerte de ~22 mois ; NASA : la probabilité
  d'un impact de comète est inférieure à 1 % de celle d'un astéroïde ; des millions d'années entre deux impacts majeurs ;
  « dévastation globale » même pour une comète à longue période relativement petite.
Choix prudents : pas de taille minimale chiffrée pour la catastrophe ; « pourrait » pour Gliese 710.
"""
from engine import *

EPISODE = 51
BOOM_SCENE = 7
LEGENDE = """Épisode 51 : la comète géante venue du bout du système solaire ☄️

Très loin, le nuage d'Oort abrite peut-être des milliers de milliards de comètes. De temps en temps, l'une d'elles plonge vers nous à environ 65 km par seconde, et on ne la repère souvent que deux ans avant. La plus grosse jamais vue mesure ~130 km (NASA/Hubble)… mais elle restera loin, au-delà de Saturne. Et selon la NASA, un impact de comète est moins de 1 % aussi probable qu'un impact d'astéroïde.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #comete #espace #astronomie #nasa #science #vulgarisation #scienceenfrançais"""

# ---------- fil rouge : la comète ----------
ICE = '#e6f4ff'; ICE_D = '#a9c8e0'; TAIL = '#9fe3ff'

def comet(d, cx, cy, r, t, ang=0.0, tail=2.5, a=255):
    """Noyau glacé + queue qui part dans la direction ang (radians)."""
    if tail > 0:
        L = r * tail * (1 + 0.06 * math.sin(t * 5))
        px, py = -math.sin(ang), math.cos(ang)
        for k, (wf, al) in enumerate(((1.0, 70), (0.6, 120), (0.3, 180))):
            w = r * wf
            tip = (cx + math.cos(ang) * L * (1 - k * 0.12), cy + math.sin(ang) * L * (1 - k * 0.12))
            d.polygon([(s(cx + px * w), s(cy + py * w)), (s(cx - px * w), s(cy - py * w)), (s(tip[0]), s(tip[1]))],
                      fill=hexc(TAIL, int(al * a / 255)))
    circle(d, cx, cy, r, fill=hexc(ICE, a))
    for (dx, dy, rr) in ((-0.3, -0.25, 0.25), (0.3, 0.2, 0.2), (0.05, 0.45, 0.14)):
        circle(d, cx + dx * r, cy + dy * r, rr * r, fill=hexc(ICE_D, a))

def sun(d, cx, cy, r, t):
    for i in range(10):
        an = i * math.pi / 5 + t * 0.4
        line(d, [(cx + (r + 15) * math.cos(an), cy + (r + 15) * math.sin(an)),
                 (cx + (r + 45) * math.cos(an), cy + (r + 45) * math.sin(an))], '#ffd23f', 10)
    circle(d, cx, cy, r, fill=hexc('#ffb703'))

def earth(d, cx, cy, r, t, a=255):
    circle(d, cx, cy, r, fill=hexc('#2f7fc1', a))
    for (dx, dy, rr) in ((-0.35, -0.25, 0.32), (0.3, 0.2, 0.26), (-0.2, 0.45, 0.2)):
        circle(d, cx + (dx + 0.06 * math.sin(t)) * r, cy + dy * r, rr * r, fill=hexc('#4fbf6a', a))

random.seed(51)
CLOUD = [(random.uniform(0, 2 * math.pi), random.uniform(230, 320), random.uniform(5, 11)) for _ in range(140)]

DOTS = [(random.uniform(100, 980), random.choice([random.uniform(330, 540), random.uniform(710, 940)]), random.uniform(6, 16)) for _ in range(60)]

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0a0f26'); stars(d, t); header(d, hexc('#9fe3ff'))
    earth(d, 300, 800, 110, t)
    k = ease(t / 3.0)
    ang = math.atan2(-400, 600)  # queue vers le haut à droite
    comet(d, 960 - 560 * k, 360 + 340 * k, 30 + 25 * k, t, ang=ang, tail=3.0)
    text_block(img, ["Et si une comète géante fonçait sur nous… sans prévenir ?"], t, 1090, '#ffffff', size=80)

def sc_oort(img, d, t, D):
    bg(d, '#14204a'); stars(d, t); header(d, hexc('#b8d0ff'))
    cx, cy = 540, 630
    sun(d, cx, cy, 22, t)
    k = ease((t - 0.2) / 1.2)
    for i, (a0, r, sz) in enumerate(CLOUD):
        if i / len(CLOUD) > k: break
        a = a0 + t * 0.05
        circle(d, cx + r * math.cos(a), cy + r * 0.95 * math.sin(a), sz * 0.5, fill=hexc(ICE, 200))
    text_block(img, ["Tout au bord du système solaire flotte un immense nuage de boules de glace : le nuage d'Oort."],
               t, 1040, '#ffffff', size=64)

def sc_count(img, d, t, D):
    bg(d, '#22164a'); stars(d, t); header(d, hexc('#d2b8ff'))
    n = int(60 * ease(t / 2.0))
    for i, (x, y, r) in enumerate(DOTS[:n]):
        circle(d, x, y + 6 * math.sin(t * 2 + i), r, fill=hexc(ICE, 220))
    ctext(d, "1 000 000 000 000 ?", 570, 84, '#ffe066', FBK, ease((t - 0.6) / 0.4))
    text_block(img, ["Il y aurait là des milliards de comètes. Peut-être même des milliers de milliards.",
                     ("Elles dorment, très loin du Soleil.", 1.6)], t, 1040, '#ffffff', size=62)

def sc_nudge(img, d, t, D):
    bg(d, '#2e1438'); stars(d, t); header(d, hexc('#ffc2e8'))
    k = ease(t / 2.0)
    sx = 120 + 600 * k
    for i in range(8):
        an = i * math.pi / 4
        line(d, [(sx + 50 * math.cos(an), 470 + 50 * math.sin(an)), (sx + 75 * math.cos(an), 470 + 75 * math.sin(an))], '#ffd6a8', 8)
    circle(d, sx, 470, 42, fill=hexc('#ffd6a8'))
    kk = ease((t - 1.0) / 2.0)
    comet(d, 600 - 80 * kk, 760 + 120 * kk, 40, t, ang=-math.pi / 2 - 0.4 * kk, tail=1.5 * kk)
    text_block(img, ["Parfois, une étoile qui passe les bouscule.",
                     ("Une comète commence alors à tomber vers le Soleil. Une chute de plus d'un million d'années.", 1.4)],
               t, 1030, '#ffffff', size=60)

def sc_speed(img, d, t, D):
    bg(d, '#0f3446'); stars(d, t); header(d, hexc('#a8e6ff'))
    x = -150 + ((t * 700) % 1400)
    for j in range(6):
        line(d, [(x - 120 - j * 90, 620 + (j % 3 - 1) * 40), (x - 60 - j * 90, 620 + (j % 3 - 1) * 40)], '#5fb0d0', 6)
    comet(d, x, 620, 55, t, ang=math.pi, tail=3.2)
    ctext(d, "65 km/s", 400, 110, '#ffe066', FBK, ease((t - 0.4) / 0.4))
    text_block(img, ["En arrivant, elle peut foncer à environ 65 km par seconde.",
                     ("Paris-Marseille en 10 secondes.", 1.6)], t, 1040, '#ffffff', size=66)

def sc_late(img, d, t, D):
    bg(d, '#3b2a0c'); stars(d, t); header(d, hexc('#ffe0a8'))
    # un télescope simple
    d.polygon([(s(250), s(820)), (s(560), s(560)), (s(600), s(610)), (s(290), s(870))], fill=hexc('#d9c7a0'))
    line(d, [(420, 740), (360, 920)], '#d9c7a0', 12); line(d, [(420, 740), (500, 920)], '#d9c7a0', 12)
    k = ease((t - 1.0) / 0.5)
    comet(d, 800, 420, 30, t, ang=-0.6, tail=2.0, a=int(255 * k))
    if k > 0.5:
        ctext(d, "!", 300, 120, '#ff6f7a', FBK, k)
    text_block(img, ["Le hic : une comète est presque invisible tant qu'elle est loin du Soleil.",
                     ("On peut ne la repérer que deux ans avant. Voire moins.", 1.8)], t, 1030, '#ffffff', size=60)

def sc_boom(img, d, t, D):
    bg(d, '#4a0d12'); stars(d, t); header(d, hexc('#ffb3bd'))
    k = ease(t / 0.9)
    ex, ey = 540, 680
    earth(d, ex, ey, 170, t)
    if t < 0.9:
        comet(d, 1000 - (1000 - ex - 120) * k, 300 + (ey - 120 - 300) * k, 40, t, ang=math.atan2(-380, 460), tail=3.0)
    else:
        kk = ease((t - 0.9) / 0.8)
        for i in range(14):
            an = i * 2 * math.pi / 14
            r0, r1 = 40 + 60 * kk, 80 + 220 * kk
            line(d, [(ex + 110 + r0 * math.cos(an), ey - 110 + r0 * math.sin(an)),
                     (ex + 110 + r1 * math.cos(an), ey - 110 + r1 * math.sin(an))], '#ffd23f', 14)
        circle(d, ex + 110, ey - 110, 90 * kk, fill=hexc('#ff7b00', 220))
    text_block(img, ["Même une comète de quelques kilomètres pourrait causer une catastrophe mondiale."],
               t, 1060, '#ffffff', size=70)

def sc_record(img, d, t, D):
    bg(d, '#123a2a'); stars(d, t); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.8)
    comet(d, 330, 620, 40, t, tail=0)
    comet(d, 680, 620, 40 + 150 * k, t, tail=0)
    f = font(FM, 38)
    d.text((s(330) - f.getlength("normale") / 2, s(690)), "normale", font=f, fill=hexc('#a8f0c0'))
    ctext(d, "≈ 130 km", 330, 80, '#ffe066', FBK, ease((t - 1.0) / 0.4))
    text_block(img, ["La plus grosse jamais vue, Bernardinelli-Bernstein, fait environ 130 km.",
                     ("50 fois plus qu'une comète ordinaire.", 1.6)], t, 1040, '#ffffff', size=60)

def sc_far(img, d, t, D):
    bg(d, '#1c1c3a'); stars(d, t); header(d, hexc('#c8ccff'))
    sun(d, 160, 640, 50, t)
    earth(d, 300, 640, 22, t)
    # Saturne
    d.ellipse([s(620), s(615), s(800), s(665)], outline=hexc('#e8d6a0'), width=s(8))
    circle(d, 710, 640, 42, fill=hexc('#e8c78a'))
    k = ease(t / 3.0)
    comet(d, 900, 400 + 300 * k, 28, t, ang=-math.pi / 2 + 0.3, tail=2.2)
    text_block(img, ["Bonne nouvelle : elle restera au-delà de l'orbite de Saturne, à 1,6 milliard de km du Soleil.",
                     ("Son passage le plus proche : 2031.", 1.8)], t, 1030, '#ffffff', size=58)

def sc_joke(img, d, t, D):
    bg(d, '#eef4f8'); header(d, hexc('#4a6a80'))
    # congélateur ouvert
    d.rounded_rectangle([s(330), s(330), s(750), s(930)], radius=s(30), fill=hexc('#ffffff'), outline=hexc('#7a95a8'), width=s(10))
    d.rectangle([s(360), s(620), s(720), s(630)], fill=hexc('#7a95a8'))
    bob = 6 * math.sin(t * 3)
    for (x, y, r) in ((450, 520, 55), (610, 540, 40), (530, 780, 70)):
        circle(d, x, y + bob, r, fill=hexc('#c9dbe8'))
        circle(d, x - r * 0.3, y - r * 0.3 + bob, r * 0.25, fill=hexc('#9db7c9'))
    text_block(img, ["Une boule de glace sale, venue de très loin, qu'on découvre trop tard…",
                     ("…c'est aussi le fond de votre congélateur.", 1.8)], t, 1030, '#1d2b36', size=62)

def sc_science(img, d, t, D):
    bg(d, '#0d2b3e'); stars(d, t); header(d, hexc('#a8e6ff'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "< 1 %", 430, 170, '#a8e6ff', FBK, k)
    ctext(d, "du risque d'un astéroïde (NASA)", 640, 44, '#a8e6ff', FM, k)
    text_block(img, ["Les gros impacts de comètes sont rarissimes : des millions d'années les séparent.",
                     ("Et on construit de meilleurs télescopes pour les voir plus tôt.", 1.8)], t, 1000, '#ffffff', size=58)

def sc_next(img, d, t, D):
    bg(d, '#24361a'); stars(d, t); header(d, hexc('#d0f0a8'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "1,3 MILLION", 440, 120, '#d0f0a8', FBK, k)
    ctext(d, "d'années avant le passage de l'étoile Gliese 710", 620, 40, '#d0f0a8', FM, k)
    text_block(img, [("Prochaine grosse bousculade possible du nuage d'Oort. On a le temps de finir le café.", 0.8)],
               t, 1040, '#ffffff', size=64)

sc_title = scene_title(["COMÈTE", "GÉANTE"], "Scénario d'extinction n°51", color='#1f4f8a')
sc_end = scene_end("Bref : une comète géante ne vous dispensera pas de vos impôts. Désolé.", color='#1f4f8a')

SCENES = [
    (sc_hook, 3.0), (sc_title, 2.4), (sc_oort, 4.0), (sc_count, 4.0), (sc_nudge, 4.4),
    (sc_speed, 3.8), (sc_late, 4.4), (sc_boom, 3.6), (sc_record, 4.2),
    (sc_far, 4.4), (sc_joke, 4.2), (sc_science, 4.4), (sc_next, 4.0), (sc_end, 4.6),
]
