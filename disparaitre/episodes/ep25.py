"""Épisode 25 — Une supernova toute proche.
Sources :
- Brunton et al., « X-Ray-luminous Supernovae: Threats to Terrestrial Biospheres », ApJ 947:42 (2023) ;
  Universe Today (28/04/2023), Chandra/NASA, phys.org : les rayons X de certaines supernovae (SN 2006jd)
  pourraient dévaster une planète jusqu'à ~160 années-lumière ; aucune étoile proche ne menace la Terre, pas même Bételgeuse.
- Melott et al. / Universe Today (15/05/2017) : estimations classiques de la « zone mortelle » de 25 à 50 années-lumière ;
  mécanisme principal : destruction de la couche d'ozone, UV qui frappent plantes et plancton.
- Fer 60 (demi-vie 2,6 millions d'années) dans les sédiments océaniques : supernovae proches il y a ~2 et ~8 millions
  d'années, à quelques centaines d'années-lumière, sans extinction de masse (Universe Today, Wallner et al. Nature 2016).
- Bételgeuse : ~550-700 années-lumière, explosion attendue d'ici ~100 000 ans, sans danger ; brillante comme
  une demi-Lune et visible en plein jour (Astronomy.com, EarthSky, Joyce et al. 2020).
"""
from engine import *

EPISODE = 25
BOOM_SCENE = 8
LEGENDE = """Épisode 25 : une supernova toute proche 💥⭐

Quand une étoile géante explose, ses rayons peuvent arracher la couche d'ozone d'une planète voisine. Une étude de 2023 (Astrophysical Journal) estime la zone de danger jusqu'à 160 années-lumière pour les pires explosions. Bonne nouvelle : aucune étoile assez proche ne nous menace, et Bételgeuse est bien trop loin.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #supernova #espace #astronomie #betelgeuse #science #vulgarisation #apocalypse"""

# ---------- fil rouge : l'étoile géante et la petite Terre ----------
def star(d, cx, cy, r, col, t, a=255, glow=True):
    if glow:
        for i in range(4, 0, -1):
            rr = r * (1 + 0.12 * i) + 6 * math.sin(t * 3 + i)
            circle(d, cx, cy, rr, fill=hexc(col, int(a * 0.10)))
    circle(d, cx, cy, r, fill=hexc(col, a))
    circle(d, cx - r * 0.3, cy - r * 0.3, r * 0.25, fill=hexc('#ffffff', int(a * 0.25)))

def earth(d, cx, cy, r, ozone=1.0, t=0, burnt=0.0):
    if ozone > 0:
        d.ellipse([s(cx - r - 22), s(cy - r - 22), s(cx + r + 22), s(cy + r + 22)],
                  outline=hexc('#7fd3ff', int(200 * ozone)), width=s(10))
    sea = '#2f7fd8' if burnt < 0.5 else '#5a6b7a'
    land = '#46c26a' if burnt < 0.5 else '#9a7b4f'
    circle(d, cx, cy, r, fill=hexc(sea))
    d.ellipse([s(cx - r * 0.6), s(cy - r * 0.5), s(cx + r * 0.1), s(cy + r * 0.2)], fill=hexc(land))
    d.ellipse([s(cx + r * 0.05), s(cy + r * 0.1), s(cx + r * 0.6), s(cy + r * 0.6)], fill=hexc(land))

def burst(d, cx, cy, k, col='#fff3b0', n=16, rmax=420):
    if k <= 0: return
    for i in range(n):
        a = i * 2 * math.pi / n
        r0, r1 = 60 * k, rmax * k
        line(d, [(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))], hexc(col, int(255 * (1 - 0.5 * k))), 14)
    circle(d, cx, cy, 130 * k, fill=hexc('#ffffff', int(255 * (1 - 0.3 * k))))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b0c2a'); stars(d, t); header(d, hexc('#b8c0ff'))
    flash = 0.5 + 0.5 * math.sin(t * 8) if t > 1.0 else 0
    star(d, 760, 470, 70 + 30 * flash, '#ffb703', t)
    earth(d, 330, 780, 80, t=t)
    text_block(img, ["Et si la fin du monde venait d'une étoile qui explose… à des années-lumière d'ici ?"], t, 1060, '#ffffff', size=70)

def sc_giant(img, d, t, D):
    bg(d, '#3a0d12'); header(d, hexc('#ffb4a2'))
    star(d, 540, 640, 230 + 15 * math.sin(t * 2.5), '#e85d04', t)
    text_block(img, ["Une étoile géante, en fin de vie, finit par manquer de carburant."], t, 1060, '#ffffff', size=72)

def sc_collapse(img, d, t, D):
    bg(d, '#14213d'); header(d, hexc('#a2d2ff'))
    k = ease((t - 0.3) / 1.0)
    if t < 1.5:
        star(d, 540, 640, 230 * (1 - 0.85 * k), '#e85d04', t)
    else:
        burst(d, 540, 640, ease((t - 1.5) / 0.6))
    text_block(img, ["Son cœur s'effondre en une fraction de seconde.", ("Puis tout explose : c'est une supernova.", 1.5)], t, 1060, '#ffffff', size=70)

random.seed(25)
GAL = [(random.gauss(0, 1), random.gauss(0, 0.35), random.random()) for _ in range(160)]
def sc_bright(img, d, t, D):
    bg(d, '#240046'); header(d, hexc('#e0aaff'))
    for (x, y, p) in GAL:
        circle(d, 380 + 120 * x, 640 + 120 * y, 4, fill=hexc('#e0aaff', int(120 + 100 * math.sin(t * 2 + p * 6))))
    k = ease((t - 0.8) / 0.6)
    star(d, 820, 560, 40 + 70 * k, '#fff3b0', t)
    text_block(img, ["Pendant quelques semaines, elle peut briller autant qu'une galaxie entière."], t, 1060, '#ffffff', size=70)

def sc_ozone(img, d, t, D):
    bg(d, '#03314b'); header(d, hexc('#90e0ef'))
    k = ease((t - 0.8) / 1.2)
    for i in range(6):
        x = 120 + ((t * 300 + i * 90) % 360)
        line(d, [(x, 620 + (i - 2.5) * 40), (x + 60, 620 + (i - 2.5) * 40)], '#fff3b0', 8)
    earth(d, 700, 640, 160, ozone=1 - k, t=t)
    text_block(img, ["Si elle est trop proche, ses rayons (rayons X et gamma) arrachent notre couche d'ozone."], t, 1060, '#ffffff', size=66)

def sc_uv(img, d, t, D):
    bg(d, '#2d3a1f'); header(d, hexc('#d8f3dc'))
    circle(d, 540, 400, 70, fill=hexc('#ffd60a'))
    for i in range(5):
        x = 260 + i * 140
        wilt = ease((t - 0.8 - i * 0.15) / 0.6)
        line(d, [(x, 900), (x + 30 * wilt, 760 + 60 * wilt)], '#52b788', 12)
        circle(d, x + 30 * wilt, 750 + 60 * wilt, 28, fill=hexc('#95d5b2' if wilt < 0.5 else '#9c6644'))
        if i < 4:
            line(d, [(470 + i * 45, 480), (300 + i * 140, 700)], hexc('#c77dff', 160), 6)
    text_block(img, ["Sans ozone, les UV du Soleil brûlent les plantes et le plancton. La chaîne alimentaire s'écroule."], t, 1060, '#ffffff', size=64)

def sc_zone(img, d, t, D):
    bg(d, '#370617'); header(d, hexc('#ffb3c1'))
    k = ease((t - 0.3) / 1.0)
    for i, (r, col) in enumerate([(330, '#9d0208'), (220, '#d00000'), (110, '#ff4d6d')]):
        circle(d, 540, 640, r * k, outline=hexc(col), width=10)
    star(d, 540, 640, 40, '#fff3b0', t)
    ctext(d, "DANGER", 360, 44, '#ffb3c1', FB, k)
    text_block(img, ["Zone de danger : quelques dizaines d'années-lumière.", ("Jusqu'à 160 pour les pires explosions.", 1.4)], t, 1060, '#ffffff', size=68)

def sc_boom(img, d, t, D):
    k = ease((t - 0.4) / 0.8)
    bg(d, '#ffffff' if 0.4 < t < 0.7 else '#1b0b00'); header(d, hexc('#ffd6a5'))
    burst(d, 540, 560, k, rmax=310)
    earth(d, 860, 860, 60, ozone=max(0, 1 - ease((t - 1.6) / 1.0)), t=t, burnt=ease((t - 2.4) / 0.4))
    text_block(img, ["Une étoile voisine explose. Le ciel s'illumine…", ("…et notre bouclier d'ozone fond.", 1.8)], t, 1060, '#ffffff', size=70)

def sc_joke(img, d, t, D):
    bg(d, '#fef3c7'); header(d, hexc('#92400e'))
    on = int(t * 2) % 2 == 0 and t < 2.0
    circle(d, 540, 500, 110, fill=hexc('#fde047' if on else '#d6d3d1'))
    d.rounded_rectangle([s(480), s(600), s(600), s(680)], radius=s(14), fill=hexc('#78716c'))
    line(d, [(540, 680), (540, 900)], '#44403c', 10)
    if t > 2.0:
        line(d, [(460, 420), (620, 580)], '#dc2626', 18); line(d, [(620, 420), (460, 580)], '#dc2626', 18)
    text_block(img, ["Point positif : pendant des semaines, plus besoin d'allumer la lumière la nuit.", ("Point négatif : tout le reste.", 2.0)], t, 1030, '#3b2105', size=64)

def sc_iron(img, d, t, D):
    bg(d, '#023e8a'); header(d, hexc('#caf0f8'))
    d.rectangle([s(120), s(820), s(960), s(950)], fill=hexc('#6c584c'))
    for i in range(12):
        x = 160 + i * 68
        y = 340 + ((t * 160 + i * 47) % 470)
        circle(d, x, min(y, 810), 14, fill=hexc('#ff7b00'))
    ctext(d, "FER 60", 860, 50, '#ffe8d6', FBK)
    text_block(img, ["Et c'est déjà arrivé ! Il y a environ deux millions d'années, une supernova a semé du fer radioactif au fond des océans."], t, 1030, '#ffffff', size=60)

def sc_betel(img, d, t, D):
    bg(d, '#1d1145'); stars(d, t); header(d, hexc('#c8b6ff'))
    star(d, 760, 470, 120 + 8 * math.sin(t * 2), '#f3722c', t)
    earth(d, 220, 830, 30, t=t)
    k = ease((t - 0.6) / 1.4)
    line(d, [(260, 810), (260 + 380 * k, 810 - 260 * k)], hexc('#ffffff', 140), 4)
    ctext(d, "≈ 550 ANNÉES-LUMIÈRE", 880, 42, '#ffd166', FB, ease((t - 1.6) / 0.4))
    text_block(img, ["La plus célèbre candidate, Bételgeuse, explosera d'ici cent mille ans.", ("Mais elle est bien trop loin pour nous faire du mal.", 1.8)], t, 1040, '#ffffff', size=62)

def sc_science(img, d, t, D):
    bg(d, '#1b4332'); header(d, hexc('#b7e4c7'))
    k = ease((t - 0.3) / 0.5)
    ctext(d, "ÉTOILE MENAÇANTE CONNUE", 470, 48, '#b7e4c7', FB, k)
    ctext(d, "AUCUNE", 560, 160, '#ffffff', FBK, k)
    text_block(img, ["Ce que disent les astronomes : aucune étoile assez proche pour nous menacer aujourd'hui."], t, 1060, '#ffffff', size=66)

sc_title = scene_title(["SUPERNOVA", "PROCHE"], "Scénario d'extinction n°25", color='#9d0208')
sc_end = scene_end("Bref : une supernova n'annulera pas vos impôts. Elle éclairera juste votre déclaration.", color='#9d0208')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_giant, 3.6), (sc_collapse, 4.2), (sc_bright, 4.0),
    (sc_ozone, 4.4), (sc_uv, 4.4), (sc_zone, 4.2), (sc_boom, 4.6), (sc_joke, 4.4),
    (sc_iron, 4.6), (sc_betel, 4.8), (sc_science, 4.0), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Et si la fin du monde venait d'une étoile qui explose… à des années-lumière d'ici ?",
    "Scénario d'extinction numéro vingt-cinq : une supernova toute proche.",
    "Une étoile géante, en fin de vie, finit par manquer de carburant.",
    "Son cœur s'effondre en une fraction de seconde. Puis tout explose : c'est une supernova.",
    "Pendant quelques semaines, elle peut briller autant qu'une galaxie entière.",
    "Si elle est trop proche, ses rayons X et gamma arrachent notre couche d'ozone.",
    "Sans ozone, les UV du Soleil brûlent les plantes et le plancton. La chaîne alimentaire s'écroule.",
    "Zone de danger : quelques dizaines d'années-lumière. Jusqu'à cent soixante pour les pires explosions.",
    "Une étoile voisine explose. Le ciel s'illumine… et notre bouclier d'ozone fond.",
    "Point positif : pendant des semaines, plus besoin d'allumer la lumière la nuit. Point négatif : tout le reste.",
    "Et c'est déjà arrivé ! Il y a environ deux millions d'années, une supernova a semé du fer radioactif au fond des océans.",
    "La plus célèbre candidate, Bételgeuse, explosera d'ici cent mille ans. Mais à cinq cent cinquante années-lumière, elle est bien trop loin.",
    "Ce que disent les astronomes : aucune étoile assez proche pour nous menacer aujourd'hui.",
    "Bref : une supernova n'annulera pas vos impôts. Elle éclairera juste votre déclaration. Abonnez-vous. Tant qu'il y a un demain.",
]
