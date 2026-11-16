"""Épisode 30 — Les étrangelets (strangelets) qui transformeraient la Terre.
Sources :
- CERN, page « La sûreté du LHC » (archive public-archive.web.cern.ch) : un étrangelet est un morceau hypothétique
  de « matière étrange » contenant à peu près autant de quarks up, down et strange ; la plupart des travaux
  théoriques prévoient qu'il redeviendrait de la matière ordinaire en un milliardième de seconde ; la crainte :
  qu'il s'unisse à la matière ordinaire et la change en matière étrange. Plus d'énergie au LHC rend leur formation
  encore moins probable : « comme la glace ne se forme pas dans l'eau chaude ». RHIC a cherché des étrangelets
  pendant des années sans en détecter. La nature a déjà produit sur Terre autant de collisions qu'environ un
  million d'expériences LHC. Rapport LSAG (2008) : aucun danger.
- Brookhaven National Laboratory (bnl.gov/RHIC/black-holes.php) : en juillet 1999, le directeur John Marburger
  réunit un comité de physiciens (présidé par Robert Jaffe, MIT) avant le démarrage de RHIC en 2000 ; conclusion :
  « aucun mécanisme crédible de scénario catastrophe ». E. Kolb : des rayons cosmiques plus énergétiques ont
  frappé la Lune sans la détruire.
- Jaffe, Busza, Sandweiss, Wilczek, « Review of speculative disaster scenarios at RHIC », Rev. Mod. Phys. 72 (2000),
  arXiv:hep-ph/9910333.
- Consensus : hypothèse théorique ; aucun étrangelet jamais observé ; risque lié aux collisionneurs jugé nul en pratique.
"""
from engine import *

EPISODE = 30
BOOM_SCENE = 7
LEGENDE = """Épisode 30 : les étrangelets, la matière qui transforme tout 🟣⚛️

En 1999, avant le démarrage d'un grand accélérateur américain (RHIC), des physiciens ont dû vérifier qu'il ne fabriquerait pas une « matière étrange » capable de transformer la Terre. Verdict : aucun scénario crédible. Les rayons cosmiques, bien plus puissants, frappent la Lune depuis des milliards d'années… et elle est toujours là (sources : CERN, Brookhaven).

On va tous disparaître… mais pas aujourd'hui.

#findumonde #physique #quarks #cern #espace #science #vulgarisation #apocalypse"""

QC = {'u': '#ff5c7a', 'd': '#4dabf7', 's': '#b197fc'}

# ---------- fil rouge : la petite boule de quarks ----------
def blob(d, cx, cy, r, kinds, t, ring='#ffffff', a=255, glow=None):
    """Une particule = une bulle avec des quarks (points colorés) qui tournent dedans."""
    if glow:
        circle(d, cx, cy, r * 1.25 + 6 * math.sin(t * 4), fill=hexc(glow, int(a * 0.35)))
    circle(d, cx, cy, r, fill=hexc('#ffffff', int(a * 0.12)), outline=hexc(ring, a), width=max(4, int(r / 14)))
    n = len(kinds)
    for i, k in enumerate(kinds):
        ang = t * 1.6 + i * 2 * math.pi / n
        rr = r * 0.45
        circle(d, cx + rr * math.cos(ang), cy + rr * math.sin(ang), r * 0.2, fill=hexc(QC[k], a))

def earth(d, cx, cy, r, k_strange=0.0):
    circle(d, cx, cy, r, fill=hexc('#2f80ed'))
    for (dx, dy, rr) in [(-0.35, -0.2, 0.32), (0.3, 0.25, 0.28), (0.1, -0.45, 0.18), (-0.2, 0.45, 0.2)]:
        circle(d, cx + dx * r, cy + dy * r, rr * r, fill=hexc('#3fbf6f'))
    if k_strange > 0:
        circle(d, cx, cy, r, fill=hexc('#9b5de5', int(235 * k_strange)))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#1b1036'); header(d, hexc('#d0bfff'))
    earth(d, 540, 640, 230)
    k = ease((t - 0.5) / 1.2)
    circle(d, 540 + 160, 640 - 160, 14 + 4 * math.sin(t * 6), fill=hexc('#b197fc'))
    circle(d, 540 + 160, 640 - 160, 40 * k + 14, outline=hexc('#b197fc', int(200 * (1 - k))), width=6)
    text_block(img, ["Et si une poussière invisible pouvait transformer la Terre entière ?"], t, 1090, '#ffffff', size=78)

def sc_briques(img, d, t, D):
    bg(d, '#0f3b44'); header(d, hexc('#a5f3fc'))
    blob(d, 540, 640, 230 + 8 * math.sin(t * 2), 'uud', t)
    k = ease((t - 0.8) / 0.5)
    ctext(d, "un proton", 330, 50, '#a5f3fc', FM, k)
    text_block(img, ["Tout ce qui existe est fait de minuscules briques : les quarks."], t, 1060, '#ffffff', size=70)

def sc_deux(img, d, t, D):
    bg(d, '#2b2d6e'); header(d, hexc('#c5cbff'))
    for i, (k_, lab) in enumerate([('u', 'UP'), ('d', 'DOWN')]):
        x = 340 + i * 400
        kk = ease((t - 0.3 - i * 0.4) / 0.4)
        circle(d, x, 620 + 12 * math.sin(t * 3 + i), 120 * kk + 1, fill=hexc(QC[k_]))
        f = font(FB, 60)
        d.text((s(x) - f.getlength(lab) / 2, s(800)), lab, font=f, fill=hexc('#ffffff', int(255 * kk)))
    text_block(img, ["Dans la matière normale, il n'en existe que deux sortes : « up » et « down »."], t, 1060, '#ffffff', size=68)

def sc_strange(img, d, t, D):
    bg(d, '#4a1d5e'); header(d, hexc('#f0c4ff'))
    k = ease((t - 0.3) / 0.5)
    r = 130 * k + 1
    x = 540 + 30 * math.sin(t * 7) * k
    circle(d, x, 620, r, fill=hexc(QC['s']))
    ctext(d, "STRANGE", 880, 64, '#ffffff', FB, k)
    for i in range(6):
        a = t * 2 + i
        line(d, [(540 + 190 * math.cos(a), 620 + 190 * math.sin(a)), (540 + 230 * math.cos(a), 620 + 230 * math.sin(a))], hexc('#f0c4ff', int(200 * k)), 8)
    text_block(img, ["Il en existe une troisième, qu'on ne voit qu'un instant : le quark « étrange »."], t, 1060, '#ffffff', size=68)

def sc_strangelet(img, d, t, D):
    bg(d, '#14213d'); header(d, hexc('#ffd166'))
    k = ease((t - 0.3) / 0.8)
    blob(d, 540, 640, 60 + 170 * k, 'udsudsuds', t, ring='#b197fc', glow='#9b5de5')
    ctext(d, "hypothétique", 285, 46, '#ffd166', FM, ease((t - 1.2) / 0.4))
    text_block(img, ["Une idée de physiciens : un mélange des trois pourrait former une boule stable.", ("Un étrangelet.", 2.2)], t, 1040, '#ffffff', size=66)

def sc_contact(img, d, t, D):
    bg(d, '#123d2a'); header(d, hexc('#b7f0c8'))
    k = ease((t - 0.5) / 1.0)
    x = 280 + 200 * k
    blob(d, x, 640, 120, 'udsuds', t, ring='#b197fc', glow='#9b5de5')
    k2 = ease((t - 1.6) / 0.8)
    kinds = 'uud' if k2 < 0.5 else 'uds'
    ring = '#ffffff' if k2 < 0.5 else '#b197fc'
    blob(d, 780, 640, 110, kinds, t, ring=ring)
    text_block(img, ["Le cauchemar : il touche un noyau d'atome normal…", ("…et le change en matière étrange.", 1.8)], t, 1060, '#ffffff', size=68)

random.seed(30)
DOTS = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(140)]
def sc_boom(img, d, t, D):
    bg(d, '#3a0d2e'); header(d, hexc('#ffb3e0'))
    k = ease((t - 0.3) / 3.2)
    earth(d, 540, 640, 260, 0)
    for (dx, dy) in DOTS:
        if dx * dx + dy * dy <= 1 and math.hypot(dx - 0.5, dy + 0.5) < k * 2.2:
            circle(d, 540 + dx * 250, 640 + dy * 250, 22, fill=hexc('#9b5de5'))
    text_block(img, ["Puis le suivant. Et le suivant… jusqu'à transformer la Terre en boule étrange."], t, 1060, '#ffffff', size=68)

def sc_rhic(img, d, t, D):
    bg(d, '#1d3557'); header(d, hexc('#a8dadc'))
    circle(d, 540, 640, 250, outline=hexc('#a8dadc'), width=26)
    for i in range(2):
        a = t * 3 * (1 if i == 0 else -1)
        circle(d, 540 + 250 * math.cos(a), 640 + 250 * math.sin(a), 22, fill=hexc('#ffd166'))
    k = ease((t - 0.3) / 0.5)
    ctext(d, "1999", 590, 100, '#ffffff', FBK, k)
    text_block(img, ["1999 : avant d'allumer un nouvel accélérateur américain, des physiciens vérifient.", ("Verdict : aucun scénario crédible.", 2.4)], t, 1020, '#ffffff', size=62)

def sc_lune(img, d, t, D):
    bg(d, '#0b0b1e'); header(d, hexc('#cdd6ff'))
    stars(d, t)
    circle(d, 540, 680, 210, fill=hexc('#d9d9e3'))
    for (dx, dy, r) in [(-60, -50, 40), (70, 40, 30), (-20, 90, 22)]:
        circle(d, 540 + dx, 680 + dy, r, fill=hexc('#b5b5c8'))
    for i in range(6):
        p = ((t * 0.9 + i / 6) % 1)
        x0, y0 = 120 + i * 170, 300
        x1, y1 = 540 + (i - 2.5) * 40, 520
        x, y = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
        line(d, [(x, y), (x - (x1 - x0) * 0.12, y - (y1 - y0) * 0.12)], '#ffd166', 6)
    text_block(img, ["Des rayons cosmiques bien plus puissants frappent la Lune depuis des milliards d'années.", ("Elle est toujours là.", 2.6)], t, 1040, '#ffffff', size=62)

def sc_joke(img, d, t, D):
    bg(d, '#ffe8cc'); header(d, hexc('#a0522d'))
    d.rounded_rectangle([s(230), s(330), s(850), s(930)], radius=s(36), fill=hexc('#495057'))
    d.rounded_rectangle([s(290), s(430), s(790), s(870)], radius=s(24), fill=hexc('#ff922b', 210 + int(30 * math.sin(t * 5))))
    for i in range(4):
        circle(d, 300 + i * 160, 380, 18, fill=hexc('#ced4da'))
    k = ease((t - 0.4) / 0.4)
    d.rounded_rectangle([s(370), s(620), s(710), s(700)], radius=s(12), fill=hexc('#dee2e6', int(255 * k)))
    for i in range(4):
        y = 640 - 30 * ((t * 1.2 + i * 0.25) % 1)
        circle(d, 410 + i * 85, y, 18 * k, fill=hexc('#74c0fc', int(200 * k)))
    text_block(img, ["En plus, une collision, c'est brûlant. Fabriquer un étrangelet là-dedans…", ("…c'est comme faire des glaçons au four.", 2.0)], t, 1010, '#3b1f0e', size=62)

def sc_science(img, d, t, D):
    bg(d, '#1f3d1a'); header(d, hexc('#c0eb75'))
    k = ease((t - 0.3) / 0.5)
    ctext(d, "ÉTRANGELETS OBSERVÉS", 400, 52, '#c0eb75', FB, k)
    ctext(d, "0", 480, 220, '#ffffff', FBK, k)
    ctext(d, "risque jugé quasi nul", 780, 52, '#c0eb75', FM, ease((t - 0.9) / 0.4))
    text_block(img, [("Ce que disent les scientifiques : c'est une hypothèse. Personne n'en a jamais vu un seul, et aucun accélérateur ne peut en fabriquer de dangereux.", 0.8)], t, 1010, '#ffffff', size=58)

sc_title = scene_title(["MATIÈRE", "ÉTRANGE"], "Scénario d'extinction n°30", color='#7b2cbf')
sc_end = scene_end("Bref : la Terre ne deviendra pas étrange. Vos impôts, eux, le sont déjà.", color='#7b2cbf')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_briques, 4.0), (sc_deux, 4.2), (sc_strange, 4.2),
    (sc_strangelet, 4.6), (sc_contact, 4.4), (sc_boom, 4.4), (sc_rhic, 4.6), (sc_lune, 4.6),
    (sc_joke, 4.6), (sc_science, 5.0), (sc_end, 4.6),
]
