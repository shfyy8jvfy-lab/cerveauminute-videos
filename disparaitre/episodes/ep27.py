"""Épisode 27 — Les bactéries résistantes à tous les antibiotiques.
Sources :
- GBD 2021 Antimicrobial Resistance Collaborators (projet GRAM), The Lancet, 16 sept. 2024
  (communiqués Université d'Oxford, IHME/HealthData.org, Wellcome ; repris par ITV, News-Medical) :
  au moins un million de morts par an directement dus à la résistance depuis 1990 (1,14 million en 2021,
  4,71 millions de décès associés) ; prévision 1,91 million par an en 2050 et 39 millions de morts
  cumulés entre 2025 et 2050.
- Prix Nobel / nobelprize.org (FAQ Fleming) et ReAct : Fleming découvre la pénicilline en 1928 et met en
  garde dès 1945 contre la résistance liée aux doses insuffisantes.
- CDC, MMWR janv. 2017 (CIDRAP, CBS News, PBS NewsHour, The Scientist) : en 2016, une patiente au Nevada
  meurt d'une infection à Klebsiella pneumoniae résistante aux 26 antibiotiques disponibles aux États-Unis.
- E. coli peut se diviser environ toutes les 20 minutes en conditions idéales (manuels de microbiologie).
- Consensus : menace sanitaire majeure (retour partiel à l'ère pré-antibiotique), mais pas une menace
  d'extinction ; solutions : usage raisonné, hygiène, vaccins, nouveaux antibiotiques.
"""
from engine import *

EPISODE = 27
BOOM_SCENE = 8
LEGENDE = """Épisode 27 : les superbactéries 🦠💊

Depuis 1990, la résistance aux antibiotiques tue au moins un million de personnes par an. Selon une étude publiée dans The Lancet en 2024, elle pourrait causer 39 millions de morts entre 2025 et 2050. Grave, oui. Extinction, non : hygiène, vaccins et nouveaux médicaments peuvent changer la donne.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #antibiotiques #bacteries #superbacteries #sante #science #vulgarisation #apocalypse"""

# ---------- fil rouge : des bactéries (bâtonnets) et une gélule ----------
def bact(d, cx, cy, col, a=255, ang=0.0, L=70, R=26, shield=False):
    dx, dy = L * math.cos(ang), L * math.sin(ang)
    d.line([s(cx - dx), s(cy - dy), s(cx + dx), s(cy + dy)], fill=hexc(col, a), width=s(R * 2))
    circle(d, cx - dx, cy - dy, R, fill=hexc(col, a)); circle(d, cx + dx, cy + dy, R, fill=hexc(col, a))
    if shield:
        circle(d, cx, cy, L + R + 18, outline=hexc('#ffffff', a), width=s(7))

def pill(d, cx, cy, w=300, h=110, a=255, c1='#ef4444', c2='#f8fafc'):
    d.rounded_rectangle([s(cx - w / 2), s(cy - h / 2), s(cx), s(cy + h / 2)], radius=s(h / 2), fill=hexc(c1, a))
    d.rounded_rectangle([s(cx), s(cy - h / 2), s(cx + w / 2), s(cy + h / 2)], radius=s(h / 2), fill=hexc(c2, a))
    d.rectangle([s(cx - h / 2), s(cy - h / 2), s(cx), s(cy + h / 2)], fill=hexc(c1, a))
    d.rectangle([s(cx), s(cy - h / 2), s(cx + h / 2), s(cy + h / 2)], fill=hexc(c2, a))

def colony(d, t, n, col='#4ade80', shields=0, cy=630, start=0.3, seed=7, spread=1.0):
    import random
    rnd = random.Random(seed)
    for i in range(n):
        x = 540 + (rnd.random() - 0.5) * 640 * spread; y = cy + (rnd.random() - 0.5) * 520 * spread
        k = ease((t - start - 0.08 * i) / 0.3)
        if k <= 0: continue
        ang = rnd.random() * 3 + 0.3 * math.sin(t * 2 + i)
        bact(d, x, y, col, int(255 * k), ang, L=40, R=20)
        if i < shields:
            circle(d, x, y, 72, outline=hexc('#ffffff', int(255 * k)), width=s(5))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#1e293b'); header(d, hexc('#e2e8f0'))
    pill(d, 540, 560 + 20 * math.sin(t * 2), a=255)
    k = ease((t - 1.0) / 0.4)
    ctext(d, "?", 720, 160, '#fbbf24', FBK, k)
    text_block(img, ["Et si un jour, plus aucun médicament ne marchait contre les infections ?"], t, 1060, '#ffffff', size=70)

def sc_1928(img, d, t, D):
    bg(d, '#14532d'); header(d, hexc('#bbf7d0'))
    circle(d, 540, 690, 250, fill=hexc('#dcfce7'))
    circle(d, 540, 690, 250, outline=hexc('#86efac'), width=s(10))
    colony(d, t, 9, '#16a34a', cy=690, seed=3, spread=0.6)
    k = ease((t - 1.2) / 0.6)
    circle(d, 540, 690, 40 + 130 * k, fill=hexc('#fde68a'))
    circle(d, 540, 690, 40 * (0.6 + k), fill=hexc('#a3e635'))
    ctext(d, "1928", 300, 64, '#bbf7d0', FBK)
    text_block(img, ["En 1928, Alexander Fleming découvre la pénicilline : une moisissure qui tue les bactéries."], t, 1060, '#ffffff', size=64)

def sc_miracle(img, d, t, D):
    bg(d, '#1e3a8a'); header(d, hexc('#bfdbfe'))
    pill(d, 540, 420, 260, 96)
    labels = ["PNEUMONIE", "PLAIE", "OPÉRATION"]
    for i, w in enumerate(labels):
        a = ease((t - 0.5 - i * 0.4) / 0.3)
        if a <= 0: continue
        y = 560 + i * 130
        d.rounded_rectangle([s(250), s(y), s(830), s(y + 100)], radius=s(30), fill=hexc('#93c5fd', int(255 * a)))
        ctext(d, w + "  ✓", y + 20, 52, '#0f172a', FB, a)
    text_block(img, ["Les antibiotiques ont rendu banal ce qui tuait avant : une pneumonie, une plaie, une opération."], t, 1060, '#ffffff', size=62)

def sc_mutation(img, d, t, D):
    bg(d, '#7c2d12'); header(d, hexc('#fed7aa'))
    n = 8
    for i in range(n):
        x = 200 + (i % 4) * 225; y = 470 + (i // 4) * 260
        if i == 5:
            bact(d, x, y, '#facc15', 255, 0.4, L=50, R=24, shield=t > 1.2)
        else:
            bact(d, x, y, '#fdba74', 255, 0.4 + 0.2 * math.sin(t * 2 + i), L=50, R=24)
    text_block(img, ["Mais les bactéries se multiplient vite : toutes les vingt minutes, parfois.", ("Et à chaque copie, une petite erreur peut les rendre résistantes.", 1.8)], t, 1040, '#ffffff', size=60)

def sc_select(img, d, t, D):
    bg(d, '#581c87'); header(d, hexc('#e9d5ff'))
    k = ease((t - 0.6) / 0.8)
    for i in range(8):
        x = 200 + (i % 4) * 225; y = 470 + (i // 4) * 260
        if i == 5:
            bact(d, x, y, '#facc15', 255, 0.4, L=50, R=24, shield=True)
        else:
            a = int(255 * (1 - k))
            if a > 5: bact(d, x, y, '#d8b4fe', a, 0.4, L=50, R=24)
    if t < 1.4:
        pill(d, 540 - 400 + 600 * ease(t / 1.2), 340, 180, 64)
    text_block(img, ["L'antibiotique tue les fragiles. Les résistantes survivent… et prennent toute la place."], t, 1060, '#ffffff', size=64)

def sc_fleming(img, d, t, D):
    bg(d, '#0f766e'); header(d, hexc('#ccfbf1'))
    # bulle de dialogue
    d.rounded_rectangle([s(200), s(380), s(880), s(760)], radius=s(60), fill=hexc('#f0fdfa'))
    d.polygon([(s(330), s(760)), (s(420), s(760)), (s(300), s(860))], fill=hexc('#f0fdfa'))
    ctext(d, "1945", 440, 70, '#0f766e', FBK)
    ctext(d, "« ATTENTION ! »", 560, 72, '#0f172a', FB, ease((t - 0.8) / 0.4))
    text_block(img, ["Fleming l'avait prédit dès 1945 : mal utiliser son médicament allait créer des bactéries résistantes."], t, 1060, '#ffffff', size=62)

def sc_now(img, d, t, D):
    bg(d, '#9a3412'); header(d, hexc('#ffedd5'))
    k = ease((t - 0.3) / 1.4)
    for i in range(100):
        x, y = 210 + (i % 10) * 66, 330 + (i // 10) * 60
        circle(d, x, y, 22, fill=hexc('#fdba74' if i < int(100 * k) else '#7c2d12'))
    ctext(d, "≥ 1 000 000 / AN", 960, 54, '#ffedd5', FB, ease((t - 1.6) / 0.4))
    text_block(img, ["Aujourd'hui, ces superbactéries tuent déjà au moins un million de personnes par an."], t, 1060, '#ffffff', size=64)

def sc_nevada(img, d, t, D):
    bg(d, '#312e81'); header(d, hexc('#c7d2fe'))
    for i in range(26):
        x = 180 + (i % 7) * 120; y = 340 + (i // 7) * 140
        a = ease((t - 0.2 - i * 0.05) / 0.2)
        if a <= 0: continue
        pill(d, x, y, 90, 36, int(255 * a), '#a5b4fc', '#e0e7ff')
        if t > 0.4 + i * 0.05 + 0.4:
            line(d, [(x - 40, y - 30), (x + 40, y + 30)], '#f87171', 8)
    text_block(img, ["En 2016, aux États-Unis, une patiente meurt d'une bactérie qui résistait aux vingt-six antibiotiques disponibles."], t, 1050, '#ffffff', size=58)

def sc_boom(img, d, t, D):
    bg(d, '#111111'); header(d, hexc('#a3a3a3'))
    colony(d, t, 22, '#22c55e', shields=22, cy=620, start=0.1, seed=11)
    if t > 2.4:
        pill(d, 540, 640, 300, 110, 255, '#525252', '#737373')
        line(d, [(380, 520), (700, 760)], '#ef4444', 18)
    text_block(img, ["Le pire scénario : toutes les bactéries deviennent invincibles…", ("…et une simple égratignure redevient mortelle.", 2.2)], t, 1060, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#fef3c7'); header(d, hexc('#92400e'))
    # pansement géant
    a = 0.12 * math.sin(t * 2.5)
    cx, cy = 540, 620
    d.rounded_rectangle([s(cx - 330), s(cy - 90), s(cx + 330), s(cy + 90)], radius=s(90), fill=hexc('#fdba74'))
    d.rounded_rectangle([s(cx - 110), s(cy - 70), s(cx + 110), s(cy + 70)], radius=s(30), fill=hexc('#fff7ed'))
    for i in range(3):
        circle(d, cx - 230 + 0 * a, cy - 40 + i * 40, 7, fill=hexc('#c2410c'))
        circle(d, cx + 230, cy - 40 + i * 40, 7, fill=hexc('#c2410c'))
    text_block(img, ["Dans ce monde-là, se couper avec une feuille de papier devient un sport extrême."], t, 1060, '#3b2105', size=66)

def sc_2050(img, d, t, D):
    bg(d, '#0c4a6e'); header(d, hexc('#bae6fd'))
    d.line([s(150), s(880), s(950), s(880)], fill=hexc('#7dd3fc'), width=s(6))
    k = ease((t - 0.3) / 1.4)
    for i, (lab, h) in enumerate([("2021", 230), ("2050", 390)]):
        x = 330 + i * 380
        hh = h * k
        d.rounded_rectangle([s(x - 90), s(880 - hh), s(x + 90), s(880)], radius=s(20), fill=hexc('#38bdf8' if i == 0 else '#f97316'))
        f = font(FB, 46); w = d.textlength(lab, font=f)
        d.text((s(x) - w / 2, s(900)), lab, font=f, fill=hexc('#bae6fd'))
    ctext(d, "39 MILLIONS", 340, 72, '#ffffff', FBK, ease((t - 1.6) / 0.4))
    text_block(img, ["Une étude publiée dans The Lancet en 2024 prévoit 39 millions de morts entre 2025 et 2050."], t, 1080, '#ffffff', size=62)

def sc_fix(img, d, t, D):
    bg(d, '#4c1d95'); header(d, hexc('#ddd6fe'))
    items = [("HYGIÈNE", '#fde68a'), ("VACCINS", '#86efac'), ("BON USAGE", '#fca5a5'), ("NOUVEAUX MÉDICAMENTS", '#93c5fd')]
    for i, (w, col) in enumerate(items):
        a = ease((t - 0.3 - i * 0.35) / 0.3)
        if a <= 0: continue
        y = 360 + i * 140
        d.rounded_rectangle([s(160), s(y), s(920), s(y + 105)], radius=s(30), fill=hexc(col, int(255 * a)))
        ctext(d, w, y + 24, 50, '#1f2937', FB, a)
    text_block(img, ["Les parades existent : se laver les mains, se vacciner, ne prendre d'antibiotiques que quand il faut, en inventer de nouveaux."], t, 1050, '#ffffff', size=56)

def sc_science(img, d, t, D):
    bg(d, '#1b4332'); header(d, hexc('#b7e4c7'))
    k = ease((t - 0.3) / 0.5)
    ctext(d, "RISQUE D'EXTINCTION", 470, 52, '#b7e4c7', FB, k)
    ctext(d, "TRÈS FAIBLE", 560, 120, '#ffffff', FBK, k)
    text_block(img, ["Ce que disent les scientifiques : une menace sanitaire majeure, pas une extinction. Mais il faut agir maintenant."], t, 1040, '#ffffff', size=60)

sc_title = scene_title(["SUPER", "BACTÉRIES"], "Scénario d'extinction n°27", color='#15803d')
sc_end = scene_end("Bref : même une bactérie invincible ne vous dispensera pas de payer vos impôts.", color='#15803d')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_1928, 4.2), (sc_mutation, 4.6), (sc_select, 4.2),
    (sc_fleming, 4.2), (sc_now, 4.0), (sc_nevada, 4.6), (sc_boom, 4.6), (sc_joke, 3.8),
    (sc_2050, 4.2), (sc_fix, 4.6), (sc_science, 4.6), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Et si un jour, plus aucun médicament ne marchait contre les infections ?",
    "Scénario d'extinction numéro vingt-sept : les superbactéries.",
    "En mille neuf cent vingt-huit, Alexander Fleming découvre la pénicilline : une moisissure qui tue les bactéries.",
    "Mais les bactéries se multiplient vite : toutes les vingt minutes, parfois. Et à chaque copie, une petite erreur peut les rendre résistantes.",
    "L'antibiotique tue les fragiles. Les résistantes survivent… et prennent toute la place.",
    "Fleming l'avait prédit dès mille neuf cent quarante-cinq : mal utiliser son médicament allait créer des bactéries résistantes.",
    "Aujourd'hui, ces superbactéries tuent déjà au moins un million de personnes par an.",
    "En deux mille seize, aux États-Unis, une patiente meurt d'une bactérie qui résistait aux vingt-six antibiotiques disponibles.",
    "Le pire scénario : toutes les bactéries deviennent invincibles… et une simple égratignure redevient mortelle.",
    "Dans ce monde-là, se couper avec une feuille de papier devient un sport extrême.",
    "Une étude publiée dans The Lancet en deux mille vingt-quatre prévoit trente-neuf millions de morts entre deux mille vingt-cinq et deux mille cinquante.",
    "Les parades existent : se laver les mains, se vacciner, ne prendre d'antibiotiques que quand il faut, et en inventer de nouveaux.",
    "Ce que disent les scientifiques : une menace sanitaire majeure, pas une extinction. Mais il faut agir maintenant.",
    "Bref : même une bactérie invincible ne vous dispensera pas de payer vos impôts. Abonnez-vous. Tant qu'il y a un demain.",
]
