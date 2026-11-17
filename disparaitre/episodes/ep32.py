"""Épisode 32 — La fin de l'oxygène : le Soleil qui chauffe et prive les plantes de CO2.
Sources :
- Ozaki & Reinhard, « The future lifespan of Earth's oxygenated atmosphere », Nature Geoscience 14 (2021),
  doi:10.1038/s41561-021-00693-5 (résumé repris par astrobiology.com) : durée de vie moyenne d'une atmosphère
  riche en oxygène (O2 > 1 % du niveau actuel) = 1,08 ± 0,14 milliard d'années ; la désoxygénation est une
  conséquence inévitable de l'augmentation du rayonnement solaire ; l'O2 chute brutalement à des niveaux
  rappelant la Terre de l'Archéen.
- IFLScience (3 mars 2021) : le Soleil plus brillant fera baisser le CO2, les plantes n'en auront plus assez pour
  produire de l'oxygène ; retour à une atmosphère pauvre en oxygène et riche en méthane, sans couche d'ozone
  (citation de K. Ozaki).
- ScienceAlert (janv. 2025, étude Graham et al., Planetary Science Journal) : le Soleil devient environ 10 % plus
  brillant tous les milliards d'années ; la chaleur accélère l'altération des roches, qui retire le CO2 de l'air.
- Air actuel ≈ 21 % d'oxygène ; Homo sapiens ≈ 300 000 ans (fossiles de Jebel Irhoud).
"""
from engine import *

EPISODE = 32
BOOM_SCENE = 8
LEGENDE = """Épisode 32 : le jour où l'air n'aura plus d'oxygène 🌱☀️

Le Soleil chauffe un tout petit peu plus chaque année. À la longue, les roches avalent le CO2 de l'air, les plantes n'ont plus de quoi fabriquer d'oxygène… et l'oxygène s'effondre. Une étude publiée dans Nature Geoscience (2021) estime que ça arrivera dans environ 1 milliard d'années.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #oxygene #soleil #climat #plantes #science #vulgarisation #apocalypse"""

# ---------- fil rouge : la petite pousse verte et le Soleil ----------
def sun(d, cx, cy, r, t, col='#ffd43b', rays=True, a=255):
    if rays:
        for i in range(12):
            ang = i * math.pi / 6 + t * 0.4
            r1, r2 = r + 18, r + 55 + 8 * math.sin(t * 4 + i)
            line(d, [(cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)), (cx + r2 * math.cos(ang), cy + r2 * math.sin(ang))], hexc(col, a), 10)
    circle(d, cx, cy, r, fill=hexc(col, a))

def plant(d, cx, base, h, t, wilt=0.0, col='#51cf66', pot='#c0703a'):
    d.rounded_rectangle([s(cx - 80), s(base), s(cx + 80), s(base + 120)], radius=s(18), fill=hexc(pot))
    d.rectangle([s(cx - 95), s(base - 10), s(cx + 95), s(base + 20)], fill=hexc(pot))
    sway = 6 * math.sin(t * 2) * (1 - wilt)
    pts = []
    for j in range(11):
        u = j / 10
        x = cx + sway * u + wilt * 120 * u ** 2
        y = base - h * u * (1 - 0.3 * wilt * u)
        pts.append((x, y))
    line(d, pts, col, 14)
    for (u, side) in [(0.45, -1), (0.7, 1), (1.0, -1)]:
        x, y = pts[int(u * 10)]
        droop = 40 * wilt
        lx = x + side * 75
        d.ellipse([s(min(x, lx)), s(y - 26 + droop), s(max(x, lx)), s(y + 10 + droop)], fill=hexc(col))

def bubble(d, x, y, r, a, col='#a5d8ff'):
    circle(d, x, y, r, outline=hexc(col, a), width=5)
    f = font(FB, int(r * 0.75)); lab = "O2"
    d.text((s(x) - f.getlength(lab) / 2, s(y - r * 0.5)), lab, font=f, fill=hexc(col, a))

def rock(d, cx, cy, w, h, col='#868e96'):
    d.rounded_rectangle([s(cx - w), s(cy - h), s(cx + w), s(cy + h)], radius=s(h * 0.8), fill=hexc(col))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b2239'); header(d, hexc('#a5d8ff'))
    sun(d, 800, 430, 70 + 6 * math.sin(t * 2), t)
    plant(d, 420, 800, 300, t)
    for i in range(4):
        p = (t * 0.5 + i / 4) % 1
        bubble(d, 420 + 60 * math.sin(i * 2 + t), 470 - 140 * p, 30, int(220 * (1 - p)))
    text_block(img, ["Et si un jour, on manquait d'air… à cause du Soleil ?"], t, 1090, '#ffffff', size=78)

def sc_breath(img, d, t, D):
    bg(d, '#123d5c'); header(d, hexc('#d0ebff'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "21 %", 420, 230, '#ffffff', FBK, k)
    ctext(d, "de l'air qu'on respire = oxygène", 720, 46, '#d0ebff', FM, ease((t - 0.7) / 0.4))
    br = 1 + 0.12 * math.sin(t * 2.5)
    circle(d, 160, 520, 40 * br, outline=hexc('#d0ebff', 160), width=6)
    circle(d, 920, 520, 40 * br, outline=hexc('#d0ebff', 160), width=6)
    text_block(img, ["À chaque inspiration, un cinquième de ce qui entre dans vos poumons, c'est de l'oxygène."], t, 1060, '#ffffff', size=66)

def sc_plants(img, d, t, D):
    bg(d, '#16402a'); header(d, hexc('#b2f2bb'))
    sun(d, 820, 400, 60, t)
    plant(d, 400, 820, 320, t)
    for i in range(6):
        p = (t * 0.45 + i / 6) % 1
        bubble(d, 400 + 140 * math.sin(i * 1.7) * p, 480 - 140 * p, 26, int(230 * (1 - p)), '#d3f9d8')
    text_block(img, ["Cet oxygène, ce sont les plantes et les algues qui le fabriquent, avec la lumière…", ("…et le CO2 de l'air (le gaz carbonique).", 1.8)], t, 1030, '#ffffff', size=64)

def sc_sun(img, d, t, D):
    bg(d, '#5c2b00'); header(d, hexc('#ffe8cc'))
    k = ease((t - 0.3) / 2.2)
    sun(d, 540, 600, 120 + 90 * k, t, col='#ffa94d' if k > 0.5 else '#ffd43b')
    text_block(img, ["Problème : le Soleil brille de plus en plus fort.", ("Environ 10 % de plus tous les milliards d'années.", 1.6)], t, 1060, '#ffffff', size=68)

def sc_rocks(img, d, t, D):
    bg(d, '#3b3b52'); header(d, hexc('#dee2e6'))
    for i in range(14):
        x = 120 + (i * 67) % 860
        y = 340 + ((t * 420 + i * 97) % 380)
        line(d, [(x, y), (x - 8, y + 35)], hexc('#74c0fc', 200), 6)
    rock(d, 330, 820, 170, 80); rock(d, 700, 800, 210, 100, '#adb5bd')
    for i in range(5):
        p = ease(((t * 0.6 + i / 5) % 1))
        x = 520 + 300 * math.cos(i * 1.3) * (1 - p)
        y = 420 + 380 * p
        f = font(FB, 40); lab = "CO2"
        d.text((s(x) - f.getlength(lab) / 2, s(y)), lab, font=f, fill=hexc('#ffe066', int(255 * (1 - p))))
    text_block(img, ["Plus il fait chaud, plus la pluie use les roches.", ("Et en s'usant, les roches avalent le CO2 de l'air.", 1.6)], t, 1060, '#ffffff', size=66)

def sc_starve(img, d, t, D):
    bg(d, '#4a3a12'); header(d, hexc('#fff3bf'))
    sun(d, 820, 400, 95, t, col='#ffa94d')
    w = ease((t - 0.5) / 2.5)
    plant(d, 400, 820, 320, t, wilt=w, col='#94d82d' if w < 0.5 else '#c9a227')
    for i in range(3):
        p = (t * 0.45 + i / 3) % 1
        a = int(230 * (1 - p) * (1 - w))
        if a > 5: bubble(d, 400, 480 - 120 * p, 24, a, '#d3f9d8')
    text_block(img, ["Moins de CO2, et les plantes n'ont plus de quoi fabriquer leur oxygène."], t, 1060, '#ffffff', size=68)

def sc_study(img, d, t, D):
    bg(d, '#24163d'); header(d, hexc('#d0bfff'))
    d.rounded_rectangle([s(140), s(600), s(940), s(660)], radius=s(30), fill=hexc('#120a22'))
    k = ease((t - 0.4) / 1.6)
    d.rounded_rectangle([s(140), s(600), s(140 + 800 * k + 1), s(660)], radius=s(30), fill=hexc('#b197fc'))
    ctext(d, "1 MILLIARD", 380, 120, '#ffffff', FBK, ease((t - 0.2) / 0.4))
    ctext(d, "d'années environ", 510, 50, '#d0bfff', FM, ease((t - 0.4) / 0.4))
    text_block(img, ["Une étude de 2021, dans la revue Nature Geoscience, a fait le calcul.", ("Verdict : ça arrive dans environ 1 milliard d'années.", 2.0)], t, 1020, '#ffffff', size=62)

def sc_boom(img, d, t, D):
    k = ease((t - 0.6) / 2.0)
    r = int(0x16 + (0x7a - 0x16) * k); g = int(0x40 + (0x3a - 0x40) * k); b = int(0x2a + (0x10 - 0x2a) * k)
    bg(d, '#%02x%02x%02x' % (r, g, b)); header(d, hexc('#ffd8a8'))
    sun(d, 820, 400, 110, t, col='#ff922b')
    plant(d, 400, 820, 320, t, wilt=1.0, col='#a07e3a')
    for i in range(10):
        bx = 150 + (i * 83) % 780; by = 380 + (i * 131) % 380
        a = int(230 * (1 - ease((t - 0.3 - i * 0.12) / 0.4)))
        if a > 5: bubble(d, bx, by, 26, a)
    text_block(img, ["Et là, l'oxygène s'effondre. L'air redevient celui de la Terre des débuts : plein de méthane, sans couche d'ozone."], t, 1030, '#ffffff', size=60)

def sc_joke(img, d, t, D):
    bg(d, '#f1f3f5'); header(d, hexc('#495057'))
    d.rounded_rectangle([s(160), s(760), s(920), s(800)], radius=s(10), fill=hexc('#868e96'))
    d.rounded_rectangle([s(600), s(560), s(860), s(740)], radius=s(16), fill=hexc('#343a40'))
    d.rectangle([s(705), s(740), s(755), s(760)], fill=hexc('#343a40'))
    plant(d, 340, 640, 240, t, wilt=ease((t - 0.3) / 1.5), col='#8f7a3a')
    text_block(img, ["Bref, la Terre finira comme la plante verte du bureau au retour des vacances…", ("…sauf que personne ne pourra l'arroser.", 2.2)], t, 1020, '#212529', size=62)

def sc_science(img, d, t, D):
    bg(d, '#0f3d3e'); header(d, hexc('#96f2d7'))
    k = ease((t - 0.3) / 0.5)
    ctext(d, "1 000 000 000 ans", 400, 84, '#ffffff', FBK, k)
    ctext(d, "avant le manque d'oxygène", 510, 44, '#96f2d7', FM, k)
    ctext(d, "300 000 ans", 650, 84, '#ffd43b', FBK, ease((t - 1.0) / 0.4))
    ctext(d, "l'âge de notre espèce", 760, 44, '#ffd43b', FM, ease((t - 1.0) / 0.4))
    text_block(img, [("Ce que disent les scientifiques : c'est quasi inévitable… mais il nous reste plus de 3 000 fois l'âge de notre espèce.", 1.6)], t, 1020, '#ffffff', size=58)

sc_title = scene_title(["FIN DE L'", "OXYGÈNE"], "Scénario d'extinction n°32", color='#2b8a3e')
sc_end = scene_end("Bref : un jour, l'air viendra à manquer. Les impôts, eux, jamais.", color='#2b8a3e')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_breath, 4.2), (sc_plants, 4.8), (sc_sun, 4.2),
    (sc_rocks, 4.6), (sc_starve, 4.2), (sc_study, 4.8), (sc_boom, 5.2), (sc_joke, 4.8),
    (sc_science, 5.4), (sc_end, 4.8),
]
