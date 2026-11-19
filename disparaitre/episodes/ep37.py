"""Épisode 37 — La mort thermique de l'univers (Big Freeze).
Sources :
- Astronomy.com, « The Big Freeze: How the universe will die » (5 sept. 2023, mis à jour 8 mai 2026) :
  univers né il y a 13,8 milliards d'années ; en 1998, deux équipes mesurent des supernovas et découvrent
  l'accélération de l'expansion ; énergie noire ~69 % ; « dans 100 000 milliards d'années, toute formation
  d'étoiles cessera » ; d'ici un gogol d'années (1 suivi de 100 zéros), le rayonnement de Hawking aura fait
  disparaître même les trous noirs supermassifs ; température finale juste au-dessus du zéro absolu ;
  nom scientifique : « mort thermique ».
- Space.com / LiveScience (4 oct. 2011) : prix Nobel de physique 2011 à Saul Perlmutter, Brian Schmidt et
  Adam Riess pour la découverte (annoncée en 1998) de l'accélération de l'expansion ; l'énergie noire
  n'a jamais été détectée directement ; l'univers deviendra froid et sombre.
- Big Think, entretien avec la cosmologiste Katie Mack : mort thermique = état d'entropie maximale,
  « la théorie la plus acceptée pour la fin de l'univers ».
- NPR / OPB (20 mars 2025) et National Geographic : les résultats du relevé DESI suggèrent que l'énergie
  noire pourrait faiblir avec le temps — pas encore confirmé, le scénario final reste ouvert.
"""
from engine import *

EPISODE = 37
BOOM_SCENE = 6
LEGENDE = """Épisode 37 : la mort thermique de l'univers 🥶🌌

Depuis 1998 (prix Nobel 2011), on sait que l'expansion de l'univers accélère. Si ça continue, plus aucune étoile ne naîtra dans environ 100 000 milliards d'années, et même les trous noirs finiront par s'évaporer. Il ne restera qu'un univers froid, sombre… et très, très calme. En 2025, le relevé DESI a toutefois suggéré que l'énergie noire pourrait faiblir : affaire à suivre.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #univers #cosmologie #bigfreeze #energienoire #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def mix(c1, c2, k):
    a, b = hexc(c1), hexc(c2)
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)) + (255,)

random.seed(37)
DOTS = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(6, 14),
         random.choice(['#ffd166', '#ff9a3d', '#9fc2ff', '#ffffff', '#ff6f91'])) for _ in range(60)]

def universe(d, cx, cy, spread, t, dim=0.0, bgcol='#000000', n=60, glow=True):
    """Le fil rouge : des galaxies (points) qui s'écartent et pâlissent."""
    for i, (x, y, r, c) in enumerate(DOTS[:n]):
        px = cx + x * 360 * spread
        py = cy + y * 300 * spread + 4 * math.sin(t * 1.5 + i)
        if px < 20 or px > 1060 or py < 260 or py > 980:
            continue
        col = mix(c, bgcol, dim)
        if glow and dim < 0.5:
            circle(d, px, py, r * 1.9, fill=mix(c, bgcol, 0.75 + 0.25 * dim))
        circle(d, px, py, r, fill=col)

def cup(d, cx, cy, t, steam=1.0, col='#f3ead6'):
    d.rounded_rectangle([s(cx - 130), s(cy - 120), s(cx + 130), s(cy + 120)], radius=s(30), fill=hexc(col))
    d.ellipse([s(cx + 100), s(cy - 60), s(cx + 200), s(cy + 50)], outline=hexc(col), width=s(22))
    d.ellipse([s(cx - 115), s(cy - 135), s(cx + 115), s(cy - 95)], fill=hexc('#6b3e1f'))
    for j in range(3):
        if steam <= 0: break
        x0 = cx - 60 + j * 60
        pts = [(x0 + 18 * math.sin(t * 3 + j + k * 0.6), cy - 160 - k * 30) for k in range(7)]
        line(d, pts, hexc('#ffffff', int(200 * steam)), 10)

def thermo(d, cx, cy, level, col='#ff4d4d'):
    d.rounded_rectangle([s(cx - 26), s(cy - 260), s(cx + 26), s(cy + 150)], radius=s(26), fill=hexc('#f3ead6'))
    circle(d, cx, cy + 170, 52, fill=hexc(col))
    top = cy + 150 - 380 * level
    d.rounded_rectangle([s(cx - 12), s(top), s(cx + 12), s(cy + 160)], radius=s(12), fill=hexc(col))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#3b2416'); header(d, hexc('#ffd59e'))
    cup(d, 520, 640, t, steam=max(0, 1 - t / (D - 0.4)))
    text_block(img, ["Et si l'univers finissait… comme un café oublié sur la table ?"], t, 1080, '#ffffff', size=72)

def sc_age(img, d, t, D):
    bg(d, '#0d1730'); header(d, hexc('#9fc2ff'))
    k = ease(t / 3.0)
    universe(d, 540, 620, 0.25 + 0.65 * k, t, bgcol='#0d1730')
    text_block(img, ["L'univers a 13,8 milliards d'années.", ("Depuis le Big Bang, il ne fait que gonfler.", 1.3)], t, 1060, '#ffffff', size=66)

def sc_accel(img, d, t, D):
    bg(d, '#2b1a47'); header(d, hexc('#d6c2ff'))
    k = ((t / D) ** 2)
    universe(d, 540, 620, 0.6 + 0.9 * k, t, bgcol='#2b1a47')
    kk = ease((t - 0.3) / 0.4)
    d.rounded_rectangle([s(390), s(320), s(690), s(450)], radius=s(30), fill=hexc('#2b1a47'))
    ctext(d, "1998", 330, 100, '#ffd166', FBK, kk)
    text_block(img, ["1998 : surprise ! Ce gonflement accélère au lieu de ralentir.", ("Découverte récompensée par le prix Nobel 2011.", 1.6)], t, 1040, '#ffffff', size=62)

def sc_dark(img, d, t, D):
    bg(d, '#111111'); header(d, hexc('#bbbbbb'))
    universe(d, 540, 620, 0.9 + 0.25 * math.sin(t), t, bgcol='#111111', n=40)
    kk = ease((t - 0.5) / 0.4)
    if kk > 0:
        ctext(d, "?", 470, 260, '#8a5cff', FBK, kk)
    text_block(img, ["Le coupable : l'« énergie noire ».", ("Elle ferait 69 % de l'univers… et personne ne l'a jamais vue.", 1.3)], t, 1060, '#ffffff', size=62)

def sc_far(img, d, t, D):
    bg(d, '#0e3b3b'); header(d, hexc('#9fe3d8'))
    k = ease(t / 3.2)
    universe(d, 540, 620, 1.0 + 1.6 * k, t, bgcol='#0e3b3b')
    circle(d, 540, 620, 22, fill=hexc('#ffd166'))
    text_block(img, ["Les galaxies s'éloignent de plus en plus vite…", ("…jusqu'à disparaître de notre ciel.", 1.4)], t, 1060, '#ffffff', size=64)

def sc_stars_out(img, d, t, D):
    bg(d, '#1a0f24'); header(d, hexc('#e0b8ff'))
    dim = ease((t - 0.8) / 3.0)
    universe(d, 540, 620, 0.85, t, dim=dim, bgcol='#1a0f24')
    kk = ease((t - 0.2) / 0.4)
    ctext(d, "100 000 MILLIARDS D'ANNÉES", 300, 48, '#ffd166', FBK, kk)
    text_block(img, ["Dans 100 000 milliards d'années : plus aucune étoile ne naît.", ("Les dernières s'éteignent, une par une.", 1.8)], t, 1040, '#ffffff', size=62)

def sc_blackholes(img, d, t, D):
    bg(d, '#05050a'); header(d, hexc('#9f9fbf'))
    k = ease((t - 1.0) / 3.0)
    r = 150 * (1 - k) + 4
    circle(d, 540, 620, r + 18, fill=hexc('#ff9a3d'))
    circle(d, 540, 620, r, fill=hexc('#000000'))
    random.seed(int(t * 20))
    for _ in range(18):
        a = random.uniform(0, 6.283); dist = r + 40 + random.uniform(0, 200)
        circle(d, 540 + math.cos(a) * dist, 620 + math.sin(a) * dist, 4, fill=hexc('#ffd166'))
    text_block(img, ["Même les trous noirs s'évaporent, tout doucement.", ("Délai : un 1 suivi de 100 zéros d'années.", 1.6)], t, 1040, '#ffffff', size=62)

def sc_heatdeath(img, d, t, D):
    bg(d, '#1c2a3a'); header(d, hexc('#a6e6ff'))
    lvl = 0.9 - 0.85 * ease((t - 0.3) / 2.8)
    thermo(d, 540, 640, lvl, col='#3fa0ff' if lvl < 0.4 else '#ff4d4d')
    text_block(img, ["À la fin : tout est à peine au-dessus du zéro absolu.", ("Plus rien ne peut se passer. C'est la « mort thermique ».", 1.6)], t, 1040, '#ffffff', size=60)

def sc_joke(img, d, t, D):
    bg(d, '#e6f2f5'); header(d, hexc('#2e5a7a'))
    # baignoire qui refroidit pendant qu'on scrolle
    d.rounded_rectangle([s(220), s(580), s(860), s(840)], radius=s(80), fill=hexc('#ffffff'), outline=hexc('#2e5a7a'), width=s(10))
    k = ease((t - 0.4) / 3.0)
    d.rounded_rectangle([s(250), s(610), s(830), s(700)], radius=s(40), fill=mix('#ff9a3d', '#9fd3ff', k))
    for j in range(3):
        a = int(200 * (1 - k))
        if a > 10:
            x0 = 400 + j * 140
            line(d, [(x0 + 15 * math.sin(t * 3 + q), 560 - q * 30) for q in range(6)], hexc('#9fb5c5', a), 9)
    d.rounded_rectangle([s(760), s(330), s(880), s(530)], radius=s(18), fill=hexc('#2b2b3a'))
    d.rounded_rectangle([s(772), s(350 - (t * 60) % 40), s(868), s(380 - (t * 60) % 40)], radius=s(6), fill=hexc('#ff6fb5'))
    text_block(img, ["Comme le bain qu'on a fait couler… puis oublié en scrollant.", ("Tiède. Puis froid. Pour toujours.", 1.7)], t, 1040, '#1d2b38', size=60)

def sc_science(img, d, t, D):
    bg(d, '#0f3d2e'); header(d, hexc('#9fe3b0'))
    universe(d, 540, 590, 0.85, t, dim=0.3, bgcol='#0f3d2e')
    kk = ease((t - 1.6) / 0.4)
    if kk > 0:
        d.rounded_rectangle([s(330), s(890), s(750), s(970)], radius=s(30), fill=hexc('#0f3d2e'))
        ctext(d, "DESI 2025 : ?", 895, 56, '#ffd166', FB, kk)
    text_block(img, ["Pour la plupart des cosmologistes, c'est le scénario le plus probable.", ("Mais en 2025, le relevé DESI suggère que l'énergie noire pourrait faiblir.", 1.7)], t, 1010, '#ffffff', size=56)

def sc_zeros(img, d, t, D):
    bg(d, '#3a2a12'); header(d, hexc('#ffd59e'))
    n = int(1 + 60 * ease(t / 3.0))
    txt = "1" + "0" * n
    f = font(FBK, 70)
    rows = [txt[i:i + 18] for i in range(0, len(txt), 18)][:6]
    for i, r in enumerate(rows):
        ctext(d, r, 380 + i * 90, 70, '#ffd166', FBK)
    text_block(img, ["Bonne nouvelle : c'est si loin que le nombre d'années ne tient pas sur l'écran.", ("Le Soleil, lui, aura fini sa vie bien avant.", 1.8)], t, 1020, '#ffffff', size=58)

sc_title = scene_title(["LE GRAND", "FROID"], "Scénario d'extinction n°37")
sc_end = scene_end("Bref : l'univers va geler, mais vos impôts, eux, resteront brûlants.")

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_age, 4.2), (sc_accel, 4.4), (sc_dark, 4.4),
    (sc_far, 4.0), (sc_stars_out, 4.8), (sc_blackholes, 4.6), (sc_heatdeath, 4.6),
    (sc_joke, 4.4), (sc_science, 4.6), (sc_zeros, 4.2), (sc_end, 4.8),
]
