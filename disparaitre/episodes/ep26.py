"""Épisode 26 — La chute de fertilité mondiale (et si on arrêtait de faire des bébés ?).
Sources :
- GBD 2021 Fertility and Forecasting Collaborators, « Global fertility in 204 countries and territories,
  1950-2021, with forecasts to 2100 », The Lancet (mars 2024, IHME / HealthData.org) : fécondité mondiale
  4,84 enfants par femme en 1950, 2,23 en 2021 ; prévision 1,83 en 2050 et 1,59 en 2100 ; 97 % des pays
  (198 sur 204) sous le seuil de remplacement (≈ 2,1) en 2100. Repris par HealthDay, Drugs.com, TechTarget.
- ONU, World Population Prospects 2024 (Key Messages ; ONU Info, juillet 2024) : 8,2 milliards d'humains
  en 2024, pic vers 10,3 milliards au milieu des années 2080, puis légère baisse (10,2 milliards en 2100).
- Corée du Sud : indice de fécondité 0,72 en 2023, 0,75 en 2024, plus bas du monde (Statistics Korea,
  AP / Korea Times, février 2025).
- Consensus des démographes : défi de vieillissement (retraites, main-d'œuvre), pas une menace d'extinction ;
  les projections lointaines sont incertaines.
"""
from engine import *

EPISODE = 26
BOOM_SCENE = 8
LEGENDE = """Épisode 26 : et si on arrêtait de faire des bébés ? 👶📉

En 1950, il y avait près de 5 enfants par femme dans le monde. En 2021 : 2,2. D'après une étude publiée dans The Lancet en 2024, 97 % des pays passeront sous le seuil de remplacement d'ici 2100. Mais pour les démographes, c'est un défi de vieillissement, pas une extinction.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #demographie #natalite #population #science #vulgarisation #apocalypse #bebes"""

# ---------- fil rouge : une famille de petits ronds ----------
def person(d, cx, cy, r, col, a=255):
    circle(d, cx, cy - r * 1.25, r * 0.55, fill=hexc(col, a))
    d.rounded_rectangle([s(cx - r * 0.7), s(cy - r * 0.55), s(cx + r * 0.7), s(cy + r * 1.1)],
                        radius=s(r * 0.45), fill=hexc(col, a))

def family(d, t, kids, cy=640, adult='#ffffff', kid='#ffd166', start=0.4):
    person(d, 430, cy - 120, 60, adult); person(d, 650, cy - 120, 60, adult)
    n = len(kids)
    for i, frac in enumerate(kids):
        x = 540 + (i - (n - 1) / 2) * 120
        k = ease((t - start - 0.25 * i) / 0.4)
        if k <= 0: continue
        r = 36
        if frac < 1:
            person(d, x, cy + 150, r, kid, int(110 * k))
        else:
            person(d, x, cy + 150 + 20 * (1 - k), r, kid, int(255 * k))

def curve(d, t, pts, col, w=12):
    k = ease((t - 0.3) / 1.4)
    n = max(2, int(len(pts) * k))
    line(d, pts[:n], col, w)
    return pts[n - 1]

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#2b2d42'); header(d, hexc('#edf2f4'))
    # berceau qui se balance
    a = 0.25 * math.sin(t * 2.5)
    cx, cy = 540 + 60 * math.sin(a), 640
    d.chord([s(cx - 220), s(cy - 200), s(cx + 220), s(cy + 200)], 0, 180, fill=hexc('#ef8354'))
    line(d, [(cx - 240, cy), (cx + 240, cy)], '#ffffff', 12)
    ctext(d, "?", 420, 160, '#edf2f4', FBK)
    text_block(img, ["Et si l'humanité disparaissait sans explosion… juste parce qu'on arrête de faire des bébés ?"], t, 1060, '#ffffff', size=68)

def sc_rule(img, d, t, D):
    bg(d, '#14532d'); header(d, hexc('#bbf7d0'))
    family(d, t, [1, 1, 0.1])
    ctext(d, "2,1", 880, 70, '#bbf7d0', FBK, ease((t - 1.2) / 0.4))
    text_block(img, ["Pour qu'une population reste stable, il faut environ 2,1 enfants par femme (le seuil de remplacement)."], t, 1060, '#ffffff', size=62)

def sc_1950(img, d, t, D):
    bg(d, '#7c2d12'); header(d, hexc('#fed7aa'))
    family(d, t, [1, 1, 1, 1, 1], start=0.3)
    ctext(d, "1950", 300, 64, '#fed7aa', FBK)
    text_block(img, ["En 1950, la moyenne mondiale était de près de cinq enfants par femme."], t, 1060, '#ffffff', size=70)

def sc_2021(img, d, t, D):
    bg(d, '#1e3a8a'); header(d, hexc('#bfdbfe'))
    d.line([s(150), s(880), s(950), s(880)], fill=hexc('#93c5fd'), width=s(6))
    d.line([s(150), s(880), s(150), s(330)], fill=hexc('#93c5fd'), width=s(6))
    pts = [(150 + i * 10, 380 + 440 * (1 - math.exp(-i / 45))) for i in range(81)]
    end = curve(d, t, pts, '#fbbf24')
    circle(d, end[0], end[1], 18, fill=hexc('#fbbf24'))
    ctext(d, "5  →  2,2", 300, 54, '#bfdbfe', FB, ease((t - 1.5) / 0.4))
    text_block(img, ["En 2021 : 2,2. Moitié moins en soixante-dix ans."], t, 1060, '#ffffff', size=72)

def sc_korea(img, d, t, D):
    bg(d, '#581c87'); header(d, hexc('#e9d5ff'))
    k = ease((t - 0.4) / 1.6)
    for g, sc in enumerate([1.0, 0.36, 0.13]):
        a = ease((t - 0.4 - g * 0.6) / 0.4)
        if a <= 0: continue
        cx = 230 + g * 300
        circle(d, cx, 640, 140 * sc, fill=hexc('#f0abfc', int(255 * a)))
    ctext(d, "0,75", 860, 70, '#e9d5ff', FBK, k)
    text_block(img, ["En Corée du Sud, c'est déjà moins de 0,8.", ("Chaque génération y est environ trois fois plus petite que la précédente.", 1.6)], t, 1040, '#ffffff', size=62)

def sc_why(img, d, t, D):
    bg(d, '#0f766e'); header(d, hexc('#ccfbf1'))
    items = [("ÉTUDES", '#fde68a'), ("LOYERS", '#fca5a5'), ("CONTRACEPTION", '#c4b5fd'), ("CHOIX", '#86efac')]
    for i, (w, col) in enumerate(items):
        a = ease((t - 0.3 - i * 0.35) / 0.3)
        if a <= 0: continue
        y = 360 + i * 140
        d.rounded_rectangle([s(220), s(y), s(860), s(y + 105)], radius=s(30), fill=hexc(col, int(255 * a)))
        ctext(d, w, y + 22, 54, '#1f2937', FB, a)
    text_block(img, ["Pourquoi ? Études plus longues, logements chers, contraception… et surtout des choix libres."], t, 1060, '#ffffff', size=64)

def sc_2100(img, d, t, D):
    bg(d, '#9a3412'); header(d, hexc('#ffedd5'))
    k = ease((t - 0.3) / 1.4)
    for i in range(100):
        x, y = 210 + (i % 10) * 66, 330 + (i // 10) * 60
        red = i < int(97 * k)
        circle(d, x, y, 22, fill=hexc('#fb923c' if red else '#fff7ed'))
    text_block(img, ["D'ici 2100, 97 % des pays seraient sous ce seuil, selon une étude de 2024 (The Lancet)."], t, 1060, '#ffffff', size=64)

def sc_boom(img, d, t, D):
    bg(d, '#111111'); header(d, hexc('#a3a3a3'))
    n = 6
    for g in range(n):
        a = ease((t - 0.2 - g * 0.35) / 0.3)
        if a <= 0: continue
        r = 150 * (0.55 ** g)
        circle(d, 160 + g * 160, 640, max(r, 5), fill=hexc('#e5e5e5', int(255 * a)))
    if t > 2.6:
        light = 0 if int(t * 6) % 2 else 1
        circle(d, 540, 380, 50, fill=hexc('#fde047' if light and t < 3.4 else '#404040'))
    text_block(img, ["Si ça ne remonte jamais, chaque génération rétrécit…", ("…jusqu'au dernier humain, qui éteint la lumière.", 2.2)], t, 1060, '#ffffff', size=68)

def sc_joke(img, d, t, D):
    bg(d, '#fef3c7'); header(d, hexc('#92400e'))
    # baguette + comptoir vide
    d.rounded_rectangle([s(200), s(760), s(880), s(900)], radius=s(20), fill=hexc('#b45309'))
    a = 0.15 * math.sin(t * 3)
    cx, cy = 540, 600
    pts = [(cx - 260 * math.cos(a), cy - 260 * math.sin(a) * 0.3 - 40), (cx + 260 * math.cos(a), cy + 260 * math.sin(a) * 0.3 + 40)]
    line(d, pts, '#f59e0b', 70)
    text_block(img, ["Bonne nouvelle : plus de file d'attente à la boulangerie.", ("Mauvaise nouvelle : plus de boulanger non plus.", 2.0)], t, 1040, '#3b2105', size=64)

def sc_peak(img, d, t, D):
    bg(d, '#0c4a6e'); stars(d, t); header(d, hexc('#bae6fd'))
    pts = [(150 + i * 10, 880 - 480 * math.sin(min(math.pi, i / 80 * math.pi * 0.85))) for i in range(81)]
    curve(d, t, pts, '#38bdf8', 14)
    ctext(d, "PIC ≈ 2085", 330, 56, '#ffffff', FB, ease((t - 1.6) / 0.4))
    text_block(img, ["Mais pour l'instant, on est 8,2 milliards.", ("L'ONU prévoit un pic à 10,3 milliards vers 2085.", 1.6)], t, 1060, '#ffffff', size=66)

def sc_old(img, d, t, D):
    bg(d, '#4c1d95'); header(d, hexc('#ddd6fe'))
    for i in range(4):
        person(d, 260 + i * 185, 560, 58, '#e5e7eb')
        line(d, [(300 + i * 185, 600), (310 + i * 185, 700)], '#a78bfa', 8)  # cannes
    a = ease((t - 1.0) / 0.4)
    person(d, 540, 860, 34, '#ffd166', int(255 * a))
    text_block(img, ["Le vrai risque : des sociétés très âgées, avec plus de grands-parents que de petits-enfants."], t, 1060, '#ffffff', size=64)

def sc_science(img, d, t, D):
    bg(d, '#1b4332'); header(d, hexc('#b7e4c7'))
    k = ease((t - 0.3) / 0.5)
    ctext(d, "RISQUE D'EXTINCTION", 470, 52, '#b7e4c7', FB, k)
    ctext(d, "TRÈS FAIBLE", 560, 120, '#ffffff', FBK, k)
    text_block(img, ["Ce que disent les démographes : un gros défi (retraites, travail), mais pas une extinction. Les taux peuvent remonter."], t, 1040, '#ffffff', size=60)

sc_title = scene_title(["BÉBÉS", "EN GRÈVE"], "Scénario d'extinction n°26", color='#c2410c')
sc_end = scene_end("Bref : même sans bébés, il restera toujours quelqu'un pour vous envoyer votre avis d'impôt.", color='#c2410c')

SCENES = [
    (sc_hook, 3.6), (sc_title, 2.4), (sc_rule, 4.4), (sc_1950, 3.8), (sc_2021, 3.6),
    (sc_korea, 4.6), (sc_why, 4.4), (sc_2100, 4.4), (sc_boom, 4.6), (sc_joke, 4.2),
    (sc_peak, 4.2), (sc_old, 4.2), (sc_science, 4.6), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Et si l'humanité disparaissait sans explosion… juste parce qu'on arrête de faire des bébés ?",
    "Scénario d'extinction numéro vingt-six : la grève des bébés.",
    "Pour qu'une population reste stable, il faut environ deux virgule un enfants par femme. C'est le seuil de remplacement.",
    "En mille neuf cent cinquante, la moyenne mondiale était de près de cinq enfants par femme.",
    "En deux mille vingt et un : deux virgule deux. Moitié moins en soixante-dix ans.",
    "En Corée du Sud, c'est déjà moins de zéro virgule huit. Chaque génération y est environ trois fois plus petite que la précédente.",
    "Pourquoi ? Études plus longues, logements chers, contraception… et surtout des choix libres.",
    "D'ici deux mille cent, quatre-vingt-dix-sept pour cent des pays seraient sous ce seuil, selon une étude publiée dans The Lancet.",
    "Si ça ne remonte jamais, chaque génération rétrécit… jusqu'au dernier humain, qui éteint la lumière.",
    "Bonne nouvelle : plus de file d'attente à la boulangerie. Mauvaise nouvelle : plus de boulanger non plus.",
    "Mais pour l'instant, on est huit milliards deux cents millions. L'ONU prévoit un pic à dix milliards trois cents millions vers deux mille quatre-vingt-cinq.",
    "Le vrai risque : des sociétés très âgées, avec plus de grands-parents que de petits-enfants.",
    "Ce que disent les démographes : un gros défi pour les retraites et le travail, mais pas une extinction. Et les taux peuvent remonter.",
    "Bref : même sans bébés, il restera toujours quelqu'un pour vous envoyer votre avis d'impôt. Abonnez-vous. Tant qu'il y a un demain.",
]
