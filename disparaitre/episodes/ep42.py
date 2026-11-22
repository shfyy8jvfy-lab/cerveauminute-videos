"""Épisode 42 — Les océans sans oxygène (anoxie océanique et zones mortes).
Sources :
- Schmidtko, Stramma & Visbeck, « Decline in global oceanic oxygen content during the past five decades »,
  Nature 542 (2017) ; Carbon Brief (guest post Oschlies, Brandt, Stramma, Schmidtko, 15 juin 2018) : baisse moyenne
  d'environ 2 % de l'oxygène de l'océan depuis 1960 ; les modèles prévoient que ça continue et s'accélère.
- Breitburg et al., « Declining oxygen in the global ocean and coastal waters », Science (janv. 2018) ;
  ScienceDaily (4 janv. 2018) et PBS NOVA (5 janv. 2018) : le volume d'eau sans aucun oxygène en haute mer a plus que
  quadruplé ; zones côtières pauvres en oxygène : moins de 50 en 1950, au moins 500 aujourd'hui (x10) ; causes :
  réchauffement (l'eau chaude garde moins d'oxygène) et engrais / eaux usées qui font proliférer des algues dont la
  décomposition consomme l'oxygène ; « environ la moitié de l'oxygène de la Terre vient de l'océan » (V. Ryabinin, UNESCO).
- Penn et al., Science (déc. 2018) ; UW News (6 déc. 2018) ; Smithsonian : il y a ~252 millions d'années (fin du
  Permien), ~96 % des espèces marines ont disparu ; le réchauffement et le manque d'oxygène expliquent plus de la
  moitié des pertes ; d'ici 2100, le réchauffement de l'océan de surface atteindrait ~20 % de celui du Permien.
"""
from engine import *

EPISODE = 42
BOOM_SCENE = 8
LEGENDE = """Épisode 42 : et si l'océan manquait d'air ? 🐟🫧

Depuis 1960, l'océan a perdu environ 2 % de son oxygène (Nature, 2017) et les « zones mortes » côtières sont passées de moins de 50 à plus de 500 (Science, 2018). Il y a 252 millions d'années, un océan chaud et privé d'oxygène a participé à la plus grande extinction de l'histoire. Pas de quoi nous faire disparaître, nous… mais les poissons, eux, commencent à suffoquer. Et on sait quoi faire : moins d'engrais, moins de réchauffement.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #ocean #climat #zonesmortes #vulgarisation #scienceenfrançais"""

# ---------- fil rouge : un petit poisson et ses bulles ----------
def fish(d, cx, cy, t, col='#ffb347', a=255, scale=1.0, sad=False):
    c = hexc(col, a); w, h = 150 * scale, 85 * scale
    wig = 12 * scale * math.sin(t * 5)
    d.polygon([(s(cx + w * 0.8), s(cy)), (s(cx + w * 1.5), s(cy - h * 0.9 + wig)), (s(cx + w * 1.5), s(cy + h * 0.9 + wig))], fill=c)
    d.ellipse([s(cx - w), s(cy - h), s(cx + w), s(cy + h)], fill=c)
    d.polygon([(s(cx - w * 0.1), s(cy - h * 0.9)), (s(cx + w * 0.4), s(cy - h * 1.45)), (s(cx + w * 0.5), s(cy - h * 0.8))], fill=c)
    circle(d, cx - w * 0.55, cy - h * 0.2, 16 * scale, fill=hexc('#ffffff', a))
    circle(d, cx - w * 0.58, cy - h * 0.2, 8 * scale, fill=hexc('#1a1a1a', a))
    if sad:
        d.arc([s(cx - w * 0.95), s(cy + h * 0.15), s(cx - w * 0.6), s(cy + h * 0.5)], 200, 340, fill=hexc('#1a1a1a', a), width=s(5 * scale))
    else:
        d.arc([s(cx - w * 0.95), s(cy - h * 0.05), s(cx - w * 0.6), s(cy + h * 0.3)], 20, 160, fill=hexc('#1a1a1a', a), width=s(5 * scale))

def bubbles(d, x, y, t, n=6, col='#e8fbff', a=200, spread=1.0):
    for i in range(n):
        ph = (t * 0.8 + i / n) % 1.0
        bx = x + 18 * math.sin(t * 3 + i) * spread
        by = y - ph * 320 * spread
        circle(d, bx, by, (8 + 10 * ph) * spread, outline=hexc(col, int(a * (1 - ph))), width=4)

def waves(d, y, col, t, a=255):
    pts = [(x, y + 14 * math.sin(x / 70 + t * 2)) for x in range(0, W + 20, 20)]
    line(d, pts, hexc(col, a), 8)

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b2a3f'); header(d, hexc('#8fd8ff'))
    waves(d, 360, '#8fd8ff', t)
    fish(d, 520, 660, t)
    bubbles(d, 380, 610, t, n=5)
    text_block(img, ["Et si la mer… arrêtait de respirer ?"], t, 1100, '#ffffff', size=84)

def sc_breathe(img, d, t, D):
    bg(d, '#123a5c'); header(d, hexc('#a6e3ff'))
    fish(d, 560, 640, t)
    for i in range(14):
        x = 140 + (i * 67) % 800; y = 400 + (i * 131) % 480
        circle(d, x, y + 8 * math.sin(t * 2 + i), 7, fill=hexc('#dff6ff', 160))
    text_block(img, ["Les poissons respirent l'oxygène dissous dans l'eau.", ("Invisible… mais vital.", 1.4)], t, 1060, '#ffffff', size=70)

def sc_half(img, d, t, D):
    bg(d, '#0f4a45'); header(d, hexc('#a8f0d8'))
    k = ease((t - 0.2) / 0.6)
    circle(d, 540, 640, 260, fill=hexc('#2c8fd6'))
    d.pieslice([s(280), s(380), s(800), s(900)], -90, -90 + 180 * k, fill=hexc('#7fe0a8'))
    ctext(d, "50 %", 590, 90, '#ffffff', FBK, k)
    text_block(img, ["Et environ la moitié de l'oxygène de la planète vient de l'océan."], t, 1060, '#ffffff', size=70)

def sc_warm(img, d, t, D):
    bg(d, '#5c2a12'); header(d, hexc('#ffc8a0'))
    k = ease((t - 0.3) / 1.2)
    d.rounded_rectangle([s(220), s(360), s(300), s(860)], radius=s(40), outline=hexc('#ffffff'), width=s(10))
    circle(d, 260, 880, 60, fill=hexc('#ff4d3a'))
    d.rounded_rectangle([s(245), s(800 - 380 * k), s(275), s(870)], radius=s(15), fill=hexc('#ff4d3a'))
    d.rounded_rectangle([s(520), s(430), s(820), s(900)], radius=s(50), outline=hexc('#ffe0c8'), width=s(10))
    d.rounded_rectangle([s(600), s(360), s(740), s(440)], radius=s(20), outline=hexc('#ffe0c8'), width=s(10))
    for i in range(int(10 * (1 - k)) + 1):
        ph = (t * 0.6 + i / 10) % 1.0
        circle(d, 560 + (i * 53) % 230, 870 - ph * 400, 10, outline=hexc('#ffffff', 200), width=4)
    text_block(img, ["Problème : une eau plus chaude garde moins d'oxygène.", ("Comme un soda tiède qui perd ses bulles.", 1.5)], t, 1040, '#ffffff', size=66)

def sc_algae(img, d, t, D):
    bg(d, '#2f4a14'); header(d, hexc('#d8f5a0'))
    for i in range(6):
        d.rounded_rectangle([s(90 + i * 60), s(380), s(130 + i * 60), s(470)], radius=s(18), fill=hexc('#ffe27a'))
    xtext(d, "engrais", 255, 300, 40, '#ffe27a', FB)
    line(d, [(150, 520), (330, 600), (520, 640), (700, 700), (980, 760)], '#6fc3ff', 34)
    k = ease((t - 0.8) / 1.5)
    for i in range(int(40 * k)):
        x = 560 + (i * 97) % 440; y = 780 + (i * 53) % 150
        circle(d, x, y + 5 * math.sin(t * 3 + i), 18 + (i % 3) * 6, fill=hexc('#5fd35f', 220))
    text_block(img, ["Sur les côtes, les engrais nourrissent des algues. En pourrissant, elles avalent l'oxygène."], t, 1060, '#ffffff', size=64)

def sc_two(img, d, t, D):
    bg(d, '#1b2550'); header(d, hexc('#b8c6ff'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "-2 %", 400, 220, '#8fd8ff', FBK, k)
    ctext(d, "d'oxygène dans l'océan depuis 1960", 700, 44, '#b8c6ff', FM, k)
    fish(d, 540, 880, t, scale=0.45)
    text_block(img, [("Ça paraît peu. Mais c'est à l'échelle de toute la planète.", 0.9)], t, 1060, '#ffffff', size=70)

def xtext(d, txt, x, y, size, color, fpath=FB, alpha=1.0):
    f = font(fpath, size)
    d.text((s(x) - f.getlength(txt) / 2, s(y)), txt, font=f, fill=hexc(color)[:3] + (int(255 * alpha),))

def sc_dead(img, d, t, D):
    bg(d, '#3b1d3f'); header(d, hexc('#f0c0f5'))
    k = ease((t - 0.2) / 1.2)
    n = int(min(500, 50 + 450 * k))
    d.rounded_rectangle([s(190), s(780), s(430), s(840)], radius=s(16), fill=hexc('#f0c0f5'))
    xtext(d, "1950", 310, 860, 46, '#f0c0f5', FB, ease(t / 0.4))
    xtext(d, "moins de 50", 310, 915, 36, '#f0c0f5', FM, ease(t / 0.4))
    hgt = 60 + 400 * k
    d.rounded_rectangle([s(650), s(840 - hgt), s(890), s(840)], radius=s(16), fill=hexc('#ff6fb5'))
    xtext(d, "aujourd'hui", 770, 860, 46, '#ff9ccf', FB, ease((t - 0.3) / 0.4))
    xtext(d, f"{n} et plus", 770, 915, 36, '#ff9ccf', FM, ease((t - 0.3) / 0.4))
    text_block(img, [("Les « zones mortes » au bord des côtes : multipliées par 10.", 0.8)], t, 1080, '#ffffff', size=68)

def sc_zero(img, d, t, D):
    bg(d, '#0a1f2e'); header(d, hexc('#8fd8ff'))
    waves(d, 360, '#8fd8ff', t)
    for i in range(4):
        k = ease((t - 0.3 - i * 0.4) / 0.3)
        if k > 0:
            d.rounded_rectangle([s(150 + i * 200), s(620 - 90 * k), s(330 + i * 200), s(620 + 90 * k)], radius=s(24), fill=hexc('#2a2a3a'), outline=hexc('#5a6a8a'), width=s(6))
    ctext(d, "x 4", 800, 110, '#ffffff', FBK, ease((t - 1.8) / 0.3))
    text_block(img, ["En haute mer, l'eau sans aucun oxygène a plus que quadruplé."], t, 1080, '#ffffff', size=68)

def sc_boom(img, d, t, D):
    bg(d, '#5a0d0d'); header(d, hexc('#ffc0c0'))
    for i in range(10):
        k = ease((t - 0.3 - i * 0.15) / 0.3)
        x = 180 + (i % 5) * 180; y = 470 + (i // 5) * 250
        sad = k > 0.5
        fish(d, x, y + 30 * k, t + i, col='#ff9a6b' if i == 9 else '#8a5a5a', a=int(255 * (1 - 0.75 * k)) if i < 9 else 255, scale=0.38, sad=sad)
    text_block(img, ["Il y a 252 millions d'années, un océan chaud et sans oxygène a tué 96 % des espèces marines."], t, 1060, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#f2e6c9'); header(d, hexc('#7a5a2a'))
    d.rounded_rectangle([s(220), s(380), s(860), s(860)], radius=s(30), fill=hexc('#d9c9a3'), outline=hexc('#7a5a2a'), width=s(10))
    d.rectangle([s(260), s(780), s(820), s(830)], fill=hexc('#7a5a2a'))
    for i, x in enumerate((340, 540, 740)):
        sway = 6 * math.sin(t * 2 + i)
        circle(d, x + sway, 640, 55, fill=hexc('#4a3a2a'))
        d.rounded_rectangle([s(x - 70 + sway), s(700), s(x + 70 + sway), s(790)], radius=s(30), fill=hexc('#4a3a2a'))
    text_block(img, ["Un endroit qui manque d'oxygène, vous connaissez :", ("la salle de réunion du lundi, fenêtres fermées.", 1.6)], t, 1010, '#2b1a10', size=66)

def sc_verdict(img, d, t, D):
    bg(d, '#102a1a'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "~20 %", 400, 200, '#a8f0c0', FBK, k)
    ctext(d, "du réchauffement du Permien, d'ici 2100", 680, 42, '#a8f0c0', FM, k)
    text_block(img, [("Les scientifiques ne prévoient pas notre disparition. Mais pour la vie marine et la pêche, c'est un vrai danger.", 0.8)], t, 1000, '#ffffff', size=62)

def sc_fix(img, d, t, D):
    bg(d, '#0e3d5c'); header(d, hexc('#8fd8ff'))
    waves(d, 360, '#8fd8ff', t)
    fish(d, 540, 660, t)
    bubbles(d, 400, 610, t, n=8)
    text_block(img, ["La bonne nouvelle : on sait quoi faire.", ("Moins d'engrais, moins de réchauffement.", 1.4)], t, 1060, '#ffffff', size=70)

sc_title = scene_title(["OCÉANS", "ASPHYXIÉS"], "Scénario d'extinction n°42")
sc_end = scene_end("Bref : la mer manque d'air. Le fisc, lui, ne manque jamais de souffle.")

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_breathe, 4.2), (sc_half, 4.2), (sc_warm, 4.6),
    (sc_algae, 4.6), (sc_two, 4.2), (sc_dead, 4.6), (sc_boom, 4.6), (sc_joke, 4.6),
    (sc_verdict, 4.8), (sc_fix, 4.2), (sc_end, 4.8),
]
