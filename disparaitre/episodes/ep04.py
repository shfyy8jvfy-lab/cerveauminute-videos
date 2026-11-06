"""Épisode 4 — Le super-volcan (Yellowstone, Toba).
Sources : USGS Yellowstone Volcano Observatory (probabilité annuelle d'une super-éruption ~1 sur 730 000 ;
3 super-éruptions il y a ~2,1 Ma, 1,3 Ma et ~631 000 ans ; réservoir de magma majoritairement solide ;
Yellowstone n'est pas « en retard ») ; Lead Stories fact-check 2022 ; Nature 2024 (Kappelman et al., site de
Shinfa-Metema, Éthiopie : des humains ont prospéré malgré Toba) ; Phys.org / Cosmos 2024 ; Nature 2018
(Pinnacle Point, Afrique du Sud) ; Tambora 1815 → « année sans été » 1816 (données historiques largement documentées).
Seuil d'une super-éruption : plus de 1 000 km³ de matériaux (indice d'explosivité 8). Mont St Helens 1980 : ~1 km³.
"""
from engine import *

EPISODE = 4
BOOM_SCENE = 6
LEGENDE = """Épisode 4 : le super-volcan 🌋❄️

Une super-éruption crache plus de 1 000 km³ de roches et de cendres, assez pour refroidir la planète pendant des années. Mais il y a 74 000 ans, nos ancêtres ont survécu à celle du Toba (Indonésie). Et pour Yellowstone, les géologues américains (USGS) estiment le risque à environ 1 sur 730 000 par an.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #volcan #yellowstone #géologie #science #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def volcano(d, cx, base, w, h, col, crater=0.22, a=255):
    """Cône simple : trapèze avec un cratère."""
    c = hexc(col, a)
    top = base - h; cw = w * crater
    d.polygon([(s(cx - w), s(base)), (s(cx - cw), s(top)), (s(cx + cw), s(top)), (s(cx + w), s(base))], fill=c)

def smoke(d, cx, top, t, col, n=4, big=1.0, a=200):
    for i in range(n):
        ph = (t * 0.6 + i / n) % 1
        r = (25 + 60 * ph) * big
        circle(d, cx + 30 * math.sin(i * 2 + t), top - 30 - ph * 260 * big, r, fill=hexc(col, int(a * (1 - ph))))

def lava(d, cx, top, t, k, col='#ff7a1a'):
    for i in range(9):
        ph = (t * 1.3 + i / 9) % 1
        ang = -math.pi / 2 + (i - 4) * 0.22
        x = cx + math.cos(ang) * 260 * ph * k
        y = top + math.sin(ang) * 300 * ph * k + 300 * ph * ph * k
        circle(d, x, y, 14 * k, fill=hexc(col, int(255 * (1 - ph))))

def cube(d, x, y, size, col):
    c = hexc(col); o = size * 0.3
    d.polygon([(s(x), s(y)), (s(x + o), s(y - o)), (s(x + size + o), s(y - o)), (s(x + size), s(y))], fill=hexc(col, 170))
    d.polygon([(s(x + size), s(y)), (s(x + size + o), s(y - o)), (s(x + size + o), s(y + size - o)), (s(x + size), s(y + size))], fill=hexc(col, 120))
    d.rectangle([s(x), s(y), s(x + size), s(y + size)], fill=c)

def sun(d, cx, cy, r, col, t, a=255):
    for i in range(12):
        an = i * math.pi / 6 + t * 0.4
        line(d, [(cx + (r + 20) * math.cos(an), cy + (r + 20) * math.sin(an)), (cx + (r + 55) * math.cos(an), cy + (r + 55) * math.sin(an))], hexc(col, a), 10)
    circle(d, cx, cy, r, fill=hexc(col, a))

def xtext(d, txt, x, y, size, color, fpath=FM, alpha=1.0):
    f = font(fpath, size)
    d.text((s(x) - f.getlength(txt) / 2, s(y)), txt, font=f, fill=hexc(color, int(255 * alpha)))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#1a1230'); header(d, hexc('#ffb38a'))
    stars(d, t)
    volcano(d, 540, 940, 420, 330, '#3d2a4f')
    smoke(d, 540, 610, t, '#9a8fb0', big=0.7)
    glow = 120 + 80 * math.sin(t * 4)
    d.ellipse([s(470), s(595), s(610), s(625)], fill=hexc('#ff7a1a', int(glow)))
    text_block(img, ["Et si la fin du monde dormait tranquillement… sous un parc naturel ?"], t, 1080, '#ffffff', size=78)

def sc_size(img, d, t, D):
    bg(d, '#123047'); header(d, hexc('#9fd3ff'))
    volcano(d, 250, 900, 150, 170, '#6b8aa3')
    smoke(d, 250, 730, t, '#cfe2f0', n=3, big=0.4)
    k = ease((t - 1.0) / 0.8)
    if k > 0:
        volcano(d, 720, 900, 300 * k + 10, 380 * k + 10, '#ff8a3d', crater=0.3)
        smoke(d, 720, 900 - 380 * k, t, '#ffd2b0', n=5, big=0.6 * k)
    xtext(d, "volcan normal", 250, 925, 40, '#9fd3ff')
    if k > 0.5: xtext(d, "super-volcan", 720, 925, 40, '#ffd2b0', alpha=k)
    text_block(img, ["Un super-volcan, c'est un volcan capable de cracher plus de 1 000 km³ de roches et de cendres d'un coup."], t, 1060, '#ffffff', size=64)

def sc_helens(img, d, t, D):
    bg(d, '#2b3a1a'); header(d, hexc('#d4f0a0'))
    cube(d, 170, 800, 40, '#d4f0a0')
    xtext(d, "St Helens : 1 km³", 205, 870, 36, '#d4f0a0')
    k = ease((t - 0.8) / 1.0)
    if k > 0:
        size = 420 * k
        cube(d, 470, 900 - size, size, '#ff8a3d')
    if k > 0.8: xtext(d, "super-éruption : 1 000 km³ et +", 680, 920, 40, '#ffd2b0', alpha=ease((t - 1.6) / 0.3))
    text_block(img, ["C'est au moins mille fois l'éruption du mont St Helens, aux États-Unis, en 1980."], t, 1090, '#ffffff', size=68)

def sc_yellow(img, d, t, D):
    bg(d, '#0f3a33'); header(d, hexc('#9ff0d8'))
    d.ellipse([s(140), s(560), s(940), s(900)], outline=hexc('#9ff0d8'), width=s(10))
    for i in range(18):
        x = 220 + i * 37; y = 760 + 20 * math.sin(i * 1.7)
        d.polygon([(s(x - 16), s(y + 30)), (s(x), s(y - 20)), (s(x + 16), s(y + 30))], fill=hexc('#2f6b5c'))
    for gx, ph in ((420, 0), (660, 1.3)):
        hh = 140 + 120 * abs(math.sin(t * 1.6 + ph))
        d.rounded_rectangle([s(gx - 14), s(780 - hh), s(gx + 14), s(780)], radius=s(14), fill=hexc('#e8fbff', 220))
        circle(d, gx, 780 - hh, 30, fill=hexc('#e8fbff', 200))
    text_block(img, ["Le plus célèbre dort sous le parc de Yellowstone, aux États-Unis. Ses geysers sont chauffés par son magma (de la roche fondue)."], t, 1040, '#ffffff', size=62)

def sc_history(img, d, t, D):
    bg(d, '#3a2210'); header(d, hexc('#ffcf99'))
    line(d, [(120, 650), (960, 650)], '#ffcf99', 8)
    marks = [(200, "2,1 Ma"), (480, "1,3 Ma"), (760, "630 000")]
    for i, (x, lbl) in enumerate(marks):
        k = ease((t - 0.3 - i * 0.6) / 0.4)
        if k <= 0: continue
        volcano(d, x, 640, 70 * k, 120 * k, '#ff8a3d')
        lava(d, x, 640 - 120 * k, t + i, 0.35 * k)
        f = font(FB, 40); d.text((s(x) - f.getlength(lbl) / 2, s(690)), lbl, font=f, fill=hexc('#ffcf99', int(255 * k)))
    k = ease((t - 2.2) / 0.4)
    if k > 0:
        f = font(FB, 40); d.text((s(940) - f.getlength("nous") / 2, s(690)), "nous", font=f, fill=hexc('#ffffff', int(255 * k)))
        circle(d, 940, 620, 22 * k, fill=hexc('#ffffff'))
    text_block(img, ["Il a déjà connu 3 super-éruptions : il y a 2,1 millions, 1,3 million et 630 000 ans."], t, 1060, '#ffffff', size=66)

def sc_boom(img, d, t, D):
    k = ease(t / 0.4)
    dark = int(150 * ease((t - 0.8) / 2.2))
    bg(d, '#5a1408'); header(d, hexc('#ffd0b0'))
    sun(d, 860, 360, 50, '#fff2a8', t)
    volcano(d, 540, 950, 380, 260, '#2a0a05', crater=0.35)
    grow = ease(t / 1.6)
    for i in range(10):  # colonne
        y = 690 - i * 32 * grow
        circle(d, 540 + 12 * math.sin(t * 3 + i), y, 50 + i * 4, fill=hexc('#6b5a55'))
    for j in range(9):  # champignon qui s'étale
        x = 540 + (j - 4) * 85 * grow
        circle(d, x, 400 + 15 * math.sin(t * 2 + j), 75 * grow + 10, fill=hexc('#7d6c66'))
    lava(d, 540, 690, t, 1.0 * k)
    if dark > 0:
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).rectangle([0, 0, W * S, H * S], fill=(0, 0, 0, dark))
        img.alpha_composite(layer)
    text_block(img, ["Le jour J\u00a0: des cendres sur tout un continent. Un voile de gaz cache le Soleil pendant des années.", ("Un «\u00a0hiver volcanique\u00a0».", 2.2)], t, 1040, '#ffffff', size=64)

def sc_joke(img, d, t, D):
    bg(d, '#e6f0f7'); header(d, hexc('#3a5a78'))
    # parasol + flocons
    line(d, [(540, 520), (540, 900)], '#3a5a78', 12)
    d.pieslice([s(340), s(400), s(740), s(640)], 180, 360, fill=hexc('#ff6f61'))
    d.line([(s(250), s(910)), (s(830), s(910))], fill=hexc('#e8c98a'), width=s(30))
    for i in range(26):
        x = (i * 97 + 30 * math.sin(t + i)) % 1000 + 40
        y = 320 + ((t * 120 + i * 53) % 600)
        circle(d, x, y, 8, fill=hexc('#ffffff'))
        circle(d, x, y, 8, outline=hexc('#9fb6c9'), width=2)
    text_block(img, ["En 1816, après un volcan bien plus petit, l'Europe a eu une « année sans été ».", ("Imaginez vos vacances d'août… en doudoune.", 2.0)], t, 1020, '#14283a', size=64)

def sc_toba(img, d, t, D):
    bg(d, '#1f3a14'); header(d, hexc('#c8f0a0'))
    volcano(d, 300, 900, 200, 170, '#4a5a3a', crater=0.35)
    k = ease((t - 0.8) / 0.6)
    for i in range(5):
        x = 600 + i * 80; y = 880 + 6 * math.sin(t * 6 + i)
        kk = ease((t - 0.9 - i * 0.15) / 0.3)
        if kk <= 0: continue
        d.rounded_rectangle([s(x - 18), s(y - 110 * kk), s(x + 18), s(y)], radius=s(18), fill=hexc('#ffd6a8'))
        circle(d, x, y - 110 * kk - 26, 26 * kk, fill=hexc('#ffd6a8'))
    ctext(d, "il y a 74 000 ans", 380, 52, '#c8f0a0', FB, ease(t / 0.4))
    text_block(img, ["Le dernier géant, le Toba en Indonésie, a explosé il y a 74 000 ans. Et nos ancêtres… ont survécu.", ("Des fouilles en Afrique le montrent.", 2.4)], t, 1040, '#ffffff', size=62)

def sc_odds(img, d, t, D):
    bg(d, '#000000'); stars(d, t)
    header(d, hexc('#9a9aa8'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "1 sur 730 000", 470, 130, '#ffb38a', FBK, k)
    ctext(d, "chaque année, pour Yellowstone", 660, 44, '#9a9aa8', FM, k)
    text_block(img, [("C'est le risque estimé par les géologues américains. Autrement dit : vous avez le temps de finir votre café.", 0.9)], t, 1040, '#ffffff', size=62)

def sc_solid(img, d, t, D):
    bg(d, '#2a1a3a'); header(d, hexc('#e0c8ff'))
    # coupe : réservoir de magma surtout solide
    d.rounded_rectangle([s(200), s(560), s(880), s(860)], radius=s(150), fill=hexc('#6b5a80'))
    for i in range(7):
        x = 300 + i * 80 + 15 * math.sin(t * 2 + i); y = 710 + 60 * math.sin(i * 2.1)
        circle(d, x, y, 18 + 4 * math.sin(t * 3 + i), fill=hexc('#ff7a1a'))
    volcano(d, 540, 520, 260, 140, '#4a3a5a', crater=0.3)
    ctext(d, "surtout de la roche solide", 890, 40, '#e0c8ff', FM)
    text_block(img, ["Et non, il n'est pas « en retard » : les volcans n'ont pas d'horaire, et son magma est surtout… solide."], t, 1040, '#ffffff', size=64)

sc_title = scene_title(["SUPER-", "VOLCAN"], "Scénario d'extinction n°4")
sc_end = scene_end("Bref : Yellowstone fait la sieste. Les impôts, eux, ne dorment jamais.")

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_size, 4.4), (sc_helens, 4.0), (sc_yellow, 4.6),
    (sc_history, 4.4), (sc_boom, 4.6), (sc_joke, 4.8), (sc_toba, 5.2),
    (sc_odds, 4.6), (sc_solid, 4.6), (sc_end, 4.8),
]
