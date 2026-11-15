"""Épisode 29 — Le dégel du pergélisol et ses virus géants endormis.
Sources :
- Scientific American / Nature News, Science News (mars 2014) : Pithovirus sibericum, virus géant (~1,5 µm, visible
  au microscope optique) retrouvé dans un pergélisol sibérien vieux d'environ 30 000 ans, « réveillé » par l'équipe
  de Jean-Michel Claverie et Chantal Abergel (CNRS, Aix-Marseille) ; il n'infecte que des amibes.
- Smithsonian Magazine, Live Science, Euronews, Phys.org (mars 2023, revue Viruses) : 13 virus ranimés depuis le
  pergélisol, le plus vieux (Pandoravirus yedoma) âgé d'environ 48 500 ans, toujours infectieux pour des amibes ;
  les auteurs estiment qu'un virus capable d'infecter des humains pourrait en principe survivre aussi.
- NPR, PATH, EcoWatch, Scientific American (août 2016) : épidémie de charbon (anthrax, une bactérie) dans la
  péninsule de Yamal pendant une vague de chaleur, liée à une carcasse de renne dégelée ; un garçon de 12 ans
  est mort, des dizaines de personnes hospitalisées, environ 2 300 rennes morts.
- Consensus : risque réel mais jugé faible et mal connu ; à surveiller. Pas un scénario d'extinction probable.
"""
from engine import *

EPISODE = 29
BOOM_SCENE = 8
LEGENDE = """Épisode 29 : les virus endormis du pergélisol 🧊🦠

En 2023, des chercheurs ont réveillé un virus resté congelé environ 48 500 ans dans le sol de Sibérie… et il était encore capable d'infecter des amibes (revue Viruses). Avec le réchauffement, ce sol gelé fond. Bonne nouvelle : ces virus géants ne s'attaquent pas à nous, et le risque est jugé faible, mais il est surveillé.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #virus #pergelisol #siberie #climat #science #vulgarisation #apocalypse"""

# ---------- fil rouge : le virus « amphore » dans la glace ----------
def virus(d, cx, cy, sc, col, t, a=255):
    """Virus géant façon amphore (ovale + bouchon), avec petits points internes."""
    c = hexc(col, a)
    w, h = 70 * sc, 110 * sc
    d.ellipse([s(cx - w), s(cy - h), s(cx + w), s(cy + h)], fill=c)
    d.rounded_rectangle([s(cx - 26 * sc), s(cy - h - 26 * sc), s(cx + 26 * sc), s(cy - h + 10 * sc)],
                        radius=s(8 * sc), fill=hexc('#ffffff', int(a * 0.85)))
    for i in range(5):
        ang = t * 1.5 + i * 1.25
        circle(d, cx + 30 * sc * math.cos(ang), cy + 50 * sc * math.sin(ang), 9 * sc,
               fill=hexc('#000000', int(a * 0.25)))

def ice_block(d, cx, cy, w, h, a=200):
    d.rounded_rectangle([s(cx - w / 2), s(cy - h / 2), s(cx + w / 2), s(cy + h / 2)], radius=s(40),
                        fill=hexc('#bfe8ff', a), outline=hexc('#ffffff', 230), width=s(8))
    line(d, [(cx - w / 2 + 40, cy - h / 2 + 60), (cx - w / 2 + 110, cy - h / 2 + 30)], hexc('#ffffff', 200), 10)

def ground(d, top, t):
    d.rectangle([0, s(top), s(W), s(960)], fill=hexc('#5b3a29'))
    for i in range(14):
        x = 40 + i * 75; y = top + 40 + (i % 3) * 70
        circle(d, x, y, 10 + (i % 4) * 3, fill=hexc('#3e271b'))
    d.rectangle([0, s(top - 30), s(W), s(top)], fill=hexc('#7ccf6a'))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0f2433'); header(d, hexc('#9fd8ff'))
    ice_block(d, 540, 640, 460, 520, 170)
    virus(d, 540, 650 + 8 * math.sin(t * 2), 1.4, '#ff7a59', t)
    text_block(img, ["Et si un virus dormait sous la glace depuis 48 500 ans ?"], t, 1090, '#ffffff', size=80)

def sc_sol(img, d, t, D):
    bg(d, '#1f3b2c'); header(d, hexc('#b7f0c8'))
    ground(d, 560, t)
    k = ease((t - 0.3) / 0.6)
    d.rectangle([0, s(700), s(W), s(700 + 260 * k)], fill=hexc('#bfe8ff', 170))
    ctext(d, "toujours gelé", 790, 48, '#0f2433', FB, k)
    for i in range(6):
        x = 120 + i * 170; y = 360 + 25 * math.sin(t * 2 + i)
        line(d, [(x, y), (x + 30, y + 40), (x - 30, y + 40), (x, y)], '#ffffff', 6)
    text_block(img, ["Le pergélisol, c'est un sol gelé toute l'année. En Sibérie, au Canada, en Alaska…"], t, 1060, '#ffffff', size=68)

def sc_congel(img, d, t, D):
    bg(d, '#26334d'); header(d, hexc('#c7d6ff'))
    d.rounded_rectangle([s(290), s(330), s(790), s(950)], radius=s(36), fill=hexc('#e8eef7'))
    line(d, [(290, 520), (790, 520)], '#9fb1cc', 8)
    d.rounded_rectangle([s(720), s(390), s(745), s(480)], radius=s(10), fill=hexc('#9fb1cc'))
    ice_block(d, 540, 740, 360, 300, 220)
    virus(d, 540, 745, 0.9, '#ff7a59', t)
    text_block(img, ["Un congélateur géant, qui garde intacts des microbes très anciens."], t, 1060, '#ffffff', size=70)

def sc_degel(img, d, t, D):
    bg(d, '#4a2a12'); header(d, hexc('#ffd3a3'))
    circle(d, 860, 400, 70 + 6 * math.sin(t * 3), fill=hexc('#ffc93c'))
    k = ease((t - 0.3) / 2.6)
    w, h = 480 - 260 * k, 460 - 260 * k
    ice_block(d, 480, 680 + (460 - h) / 2, w, h, int(200 - 80 * k))
    for i in range(4):
        y = 700 + ((t * 220 + i * 70) % 250)
        circle(d, 300 + i * 120, y, 12, fill=hexc('#9fd8ff', 200))
    virus(d, 480, 760, 0.6 + 0.4 * k, '#ff7a59', t)
    text_block(img, ["Avec le réchauffement, ce sol dégèle. Et ce qu'il cachait refait surface."], t, 1060, '#ffffff', size=68)

def sc_2014(img, d, t, D):
    bg(d, '#103a3a'); header(d, hexc('#a8f0e0'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "2014", 360, 150, '#a8f0e0', FBK, k)
    ctext(d, "30 000 ans au frais", 540, 52, '#ffffff', FM, k)
    virus(d, 540, 790, 0.9 * ease((t - 0.6) / 0.5) + 0.01, '#ff7a59', t)
    text_block(img, ["Des chercheurs français réveillent un virus géant congelé depuis 30 000 ans."], t, 1060, '#ffffff', size=68)

def sc_geant(img, d, t, D):
    bg(d, '#2d1b4e'); header(d, hexc('#d8c4ff'))
    circle(d, 540, 640, 280, outline=hexc('#ffffff'), width=12)
    circle(d, 540, 640, 268, fill=hexc('#3f2a66'))
    line(d, [(735, 840), (860, 960)], '#ffffff', 26)
    virus(d, 480, 650, 1.3, '#ff7a59', t)
    k = ease((t - 1.2) / 0.4)
    for i in range(3):
        circle(d, 640 + 10 * math.sin(t * 3 + i), 520 + i * 110, 30 * k, fill=hexc('#ffd166'))
    text_block(img, ["Si gros qu'on le voit au microscope ordinaire.", ("Et il est encore contagieux… pour des amibes.", 1.4)], t, 1040, '#ffffff', size=66)

def sc_2023(img, d, t, D):
    bg(d, '#0d2a4a'); header(d, hexc('#9fd8ff'))
    k = ease((t - 0.2) / 0.5)
    n = int(48500 * ease(t / 1.4))
    ctext(d, f"{n:,}".replace(',', ' '), 380, 170, '#ffd166', FBK, k)
    ctext(d, "ans", 580, 60, '#ffffff', FM, k)
    for i in range(5):
        virus(d, 220 + i * 160, 820 + 15 * math.sin(t * 3 + i), 0.45, '#ff7a59', t + i, a=int(255 * ease((t - 0.8 - i * 0.2) / 0.3)))
    text_block(img, [("2023, nouveau record : 13 virus réveillés, dont un de 48 500 ans.", 0.6)], t, 1060, '#ffffff', size=68)

random.seed(29)
SPREAD = [(random.uniform(90, 990), random.uniform(330, 950), random.uniform(0, 2.6)) for _ in range(40)]
def sc_boom(img, d, t, D):
    bg(d, '#3a0d12'); header(d, hexc('#ffb3bd'))
    ground(d, 860, t)
    for (x, y, b) in SPREAD:
        if t > b:
            k = ease((t - b) / 0.4)
            virus(d, x, 860 - (860 - y) * k, 0.32, '#ff4d5a', t + b, a=int(255 * k))
    text_block(img, ["Le cauchemar : un microbe oublié, que notre corps ne connaît plus, sort du sol."], t, 1080, '#ffffff', size=68)

def sc_yamal(img, d, t, D):
    bg(d, '#2b3a1a'); header(d, hexc('#d9f0a8'))
    d.rounded_rectangle([s(160), s(520), s(920), s(900)], radius=s(30), fill=hexc('#e9f2ff'))
    k = ease((t - 0.3) / 0.6)
    ctext(d, "SIBÉRIE · 2016", 360, 60, '#d9f0a8', FB, k)
    for i in range(20):
        x = 230 + (i % 10) * 70; y = 640 + (i // 10) * 130
        kk = ease((t - 0.6 - i * 0.05) / 0.3)
        circle(d, x, y, 22 * kk, fill=hexc('#8a5a3c'))
        line(d, [(x - 14, y - 22 * kk), (x - 24, y - 50 * kk)], '#8a5a3c', 5)
        line(d, [(x + 14, y - 22 * kk), (x + 24, y - 50 * kk)], '#8a5a3c', 5)
    text_block(img, ["Déjà vu en 2016 : un renne mort, dégelé, libère une maladie (l'anthrax).", ("Un enfant meurt. 2 300 rennes aussi.", 2.0)], t, 1020, '#ffffff', size=62)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    d.rounded_rectangle([s(300), s(330), s(780), s(940)], radius=s(30), fill=hexc('#ffffff'), outline=hexc('#8a5a3c'), width=s(12))
    d.rounded_rectangle([s(390), s(620), s(690), s(820)], radius=s(20), fill=hexc('#cfe9ff'))
    ctext(d, "? ? ?", 680, 56, '#4a6a8a', FB)
    k = ease((t - 0.4) / 0.4)
    d.rounded_rectangle([s(370), s(395), s(710), s(470)], radius=s(12), fill=hexc('#ffd166', int(255 * k)))
    ctext(d, "-46 500 av. J.-C.", 412, 34, '#4a2c1d', FB, k)
    text_block(img, ["Morale : ne jamais décongeler la boîte oubliée au fond du congélo…", ("…surtout si elle date de la préhistoire.", 1.8)], t, 1000, '#2b1a10', size=64)

def sc_science(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#b7e4c7'))
    k = ease((t - 0.3) / 0.5)
    ctext(d, "RISQUE POUR NOUS", 420, 56, '#b7e4c7', FB, k)
    ctext(d, "FAIBLE", 510, 150, '#ffffff', FBK, k)
    ctext(d, "mais surveillé", 700, 52, '#b7e4c7', FM, ease((t - 0.9) / 0.4))
    text_block(img, [("Ce que disent les scientifiques : les virus réveillés n'attaquent que des amibes. Le danger existe, mais il reste mal connu.", 0.8)], t, 1020, '#ffffff', size=60)

sc_title = scene_title(["VIRUS", "ENDORMIS"], "Scénario d'extinction n°29", color='#0e7490')
sc_end = scene_end("Bref : même un virus se réveille après 48 500 ans. Vos impôts, eux, ne dorment jamais.", color='#0e7490')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_sol, 4.2), (sc_congel, 4.0), (sc_degel, 4.2),
    (sc_2014, 4.2), (sc_geant, 4.6), (sc_2023, 4.4), (sc_boom, 4.2), (sc_yamal, 5.0),
    (sc_joke, 4.6), (sc_science, 5.0), (sc_end, 4.8),
]
