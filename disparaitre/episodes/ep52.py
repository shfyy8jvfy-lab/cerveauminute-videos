"""Épisode 52 — Mythe : la fin du monde de l'an 1000.
Sources :
- Richard Landes, « The Fear of an Apocalyptic Year 1000: Augustinian Historiography, Medieval and Modern »,
  Speculum 75.1 (2000) (repris par Medievalists.net) : Jules Michelet, au milieu du XIXe siècle, a dessiné un
  tableau spectaculaire d'attentes apocalyptiques de masse culminant en l'an 1000 ; à la fin du XIXe siècle,
  les historiens professionnels l'ont rejeté comme une légende romantique (G. L. Burr, American Historical
  Review, 1901) ; arguments des critiques : peu de contemporains connaissaient même la date, les documents
  cités concernent souvent 1010 ou 1033. Landes, lui, défend que des attentes de la fin des temps ont existé.
- Smithsonian Magazine, « Terror in A.D. 1000? » : l'image d'églises bondées, de champs abandonnés et de biens
  donnés à l'Église est, pour la plupart des médiévistes, « plus légende que réalité » ; débat toujours vif (Landes).
- Raoul Glaber, Histoires (chronique achevée vers 1044 à Cluny), trad. Coulton (Fordham Medieval Sourcebook) et
  livre III (Columbia, Medieval Architecture) : famines autour de l'an mil ; « environ deux ou trois ans » après
  l'an mil, le monde se revêt « d'un blanc manteau d'églises » ; des gens attendaient des prodiges à l'approche du
  millénaire de la Passion (1033). L'introduction de Coulton met en garde contre l'exagération de l'importance
  de l'an 1000 (J. Roy, L'An mille, 1885).
Choix prudents : on parle d'une « légende » amplifiée au XIXe siècle, on reconnaît que des inquiétudes ont existé
(surtout vers 1033) et que le débat entre historiens continue ; aucune anecdote non vérifiée (ex. la messe de
minuit du pape Sylvestre II) n'est citée.
"""
from engine import *

EPISODE = 52
BOOM_SCENE = 5
LEGENDE = """Épisode 52 : la fin du monde de l'an 1000 🕯️📜

La légende raconte qu'en 999, toute l'Europe attendait l'Apocalypse : églises bondées, champs abandonnés. Pour la plupart des historiens, cette grande panique a surtout été racontée au XIXe siècle (Michelet). Un moine de l'époque, Raoul Glaber, décrit plutôt un monde qui se couvre ensuite « d'un blanc manteau d'églises ».

On va tous disparaître… mais pas aujourd'hui.

#findumonde #anmil #moyenage #histoire #mythe #apocalypse #vulgarisation #histoiredefrance"""

# ---------- fil rouge : la page de calendrier ----------
def calendar(d, cx, cy, txt, txt_col='#2b1a10', scale=1.0, a=255, band='#b3121b', page='#fbf3e2', tilt=0, sub=None):
    w, h = 230 * scale, 270 * scale
    cy = cy + tilt
    d.rounded_rectangle([s(cx - w), s(cy - h), s(cx + w), s(cy + h)], radius=s(26 * scale), fill=hexc(page, a))
    d.rounded_rectangle([s(cx - w), s(cy - h), s(cx + w), s(cy - h + 110 * scale)], radius=s(26 * scale), fill=hexc(band, a))
    d.rectangle([s(cx - w), s(cy - h + 70 * scale), s(cx + w), s(cy - h + 110 * scale)], fill=hexc(band, a))
    for rx in (-120, 0, 120):
        d.rounded_rectangle([s(cx + rx * scale - 12 * scale), s(cy - h - 40 * scale), s(cx + rx * scale + 12 * scale),
                             s(cy - h + 30 * scale)], radius=s(12 * scale), fill=hexc('#6b6b78', a))
    if txt:
        size = int(170 * scale)
        f = font(FBK, size)
        tw = f.getlength(txt) / S
        d.text((s(cx - tw / 2), s(cy + 20 * scale - size * 0.62)), txt, font=f, fill=hexc(txt_col, a))
    if sub:
        f2 = font(FB, int(44 * scale))
        tw = f2.getlength(sub) / S
        d.text((s(cx - tw / 2), s(cy + 150 * scale)), sub, font=f2, fill=hexc(txt_col, int(a * 0.75)))

def candle(d, x, y, t, ph=0, col='#fbf3e2'):
    d.rounded_rectangle([s(x - 18), s(y), s(x + 18), s(y + 120)], radius=s(8), fill=hexc(col))
    fl = 6 * math.sin(t * 9 + ph)
    d.ellipse([s(x - 13 + fl * 0.3), s(y - 52), s(x + 13 + fl * 0.3), s(y - 4)], fill=hexc('#ffb03b'))
    d.ellipse([s(x - 6), s(y - 30), s(x + 6), s(y - 8)], fill=hexc('#fff1b8'))

def church(d, x, y, sc, col, a=255):
    c = hexc(col, a)
    d.rectangle([s(x - 60 * sc), s(y - 70 * sc), s(x + 60 * sc), s(y + 70 * sc)], fill=c)
    d.polygon([(s(x - 75 * sc), s(y - 70 * sc)), (s(x), s(y - 140 * sc)), (s(x + 75 * sc), s(y - 70 * sc))], fill=c)
    d.rectangle([s(x - 14 * sc), s(y - 230 * sc), s(x + 14 * sc), s(y - 120 * sc)], fill=c)
    d.polygon([(s(x - 28 * sc), s(y - 225 * sc)), (s(x), s(y - 285 * sc)), (s(x + 28 * sc), s(y - 225 * sc))], fill=c)
    d.rounded_rectangle([s(x - 20 * sc), s(y + 10 * sc), s(x + 20 * sc), s(y + 70 * sc)], radius=s(20 * sc), fill=hexc('#2b3a55', a))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#1d1430'); stars(d, t); header(d, hexc('#d2b8ff'))
    calendar(d, 540, 640, "999", tilt=6 * math.sin(t * 2))
    text_block(img, ["Et si le monde avait failli finir… il y a mille ans ?"], t, 1100, '#ffffff', size=80)

def sc_legend(img, d, t, D):
    bg(d, '#2a1a0e'); header(d, hexc('#ffd98a'))
    calendar(d, 540, 600, "999", sub="31 décembre", scale=0.9)
    for i, x in enumerate((180, 300, 780, 900)):
        candle(d, x, 800, t, ph=i)
    text_block(img, ["La légende : fin 999, toute l'Europe attend la fin du monde."], t, 1080, '#ffffff', size=72)

def sc_panic(img, d, t, D):
    bg(d, '#123047'); header(d, hexc('#9fd3ff'))
    items = ["églises bondées", "champs abandonnés", "terres données à l'Église"]
    for i, l in enumerate(items):
        k = ease((t - 0.3 - i * 0.7) / 0.35)
        if k <= 0: continue
        y = 420 + i * 160
        d.rounded_rectangle([s(170), s(y - 10), s(910), s(y + 100)], radius=s(50), fill=hexc('#2c5878'))
        ctext(d, l, y + 15, 58, '#ffffff', FB, k)
    text_block(img, [("Dans les vieux récits, on se confesse, on prie… et on lâche tout.", 2.4)], t, 1080, '#ffffff', size=68)

def sc_clock(img, d, t, D):
    bg(d, '#0e0e1a'); stars(d, t); header(d, hexc('#c8ccff'))
    cx, cy, r = 540, 630, 260
    circle(d, cx, cy, r, fill=hexc('#fbf3e2'))
    circle(d, cx, cy, r - 20, outline=hexc('#2b1a10'), width=6)
    for i in range(12):
        a = i * math.pi / 6
        line(d, [(cx + (r - 50) * math.sin(a), cy - (r - 50) * math.cos(a)), (cx + (r - 30) * math.sin(a), cy - (r - 30) * math.cos(a))], '#2b1a10', 10)
    m = -0.5 + 0.5 * ease(t / (D - 0.4))   # l'aiguille des minutes monte vers 12
    am = m * math.pi * 2 / 12 * 2
    line(d, [(cx, cy), (cx + 200 * math.sin(am), cy - 200 * math.cos(am))], '#2b1a10', 14)
    line(d, [(cx, cy), (cx + 130 * math.sin(am / 12), cy - 130 * math.cos(am / 12))], '#2b1a10', 22)
    circle(d, cx, cy, 20, fill=hexc('#b3121b'))
    text_block(img, ["Minuit approche.", ("Tout le monde retient son souffle…", 1.2)], t, 1080, '#ffffff', size=78)

def sc_boom(img, d, t, D):
    flash = max(0, 1 - t / 0.6)
    bg(d, '#f2c14e' if flash > 0.5 else '#5a1220'); header(d, hexc('#ffe0a8'))
    k = ease((t - 0.3) / 0.5)
    sh = 18 * math.sin(t * 50) * max(0, 1 - t)
    calendar(d, 540 + sh, 620, "999" if k < 0.5 else "1000", scale=1.0)
    for i in range(10):
        a = i * math.pi / 5 + t
        rr = 330 + 30 * math.sin(t * 6 + i)
        line(d, [(540 + 300 * math.cos(a), 620 + 300 * math.sin(a) * 0.95), (540 + rr * math.cos(a), 620 + rr * math.sin(a) * 0.95)], '#ffe0a8', 10)
    text_block(img, [("DONG ! Minuit. L'an 1000 commence…", 0.4)], t, 1100, '#ffffff', size=78)

def sc_nothing(img, d, t, D):
    bg(d, '#8fd0ff'); header(d, hexc('#1d3a5a'))
    k = ease(t / 1.6)
    sy = 620 - 120 * k
    circle(d, 860, sy - 120, 90, fill=hexc('#ffd84a'))
    for i in range(8):
        a = i * math.pi / 4 + t * 0.6
        line(d, [(860 + 110 * math.cos(a), sy - 120 + 110 * math.sin(a)), (860 + 150 * math.cos(a), sy - 120 + 150 * math.sin(a))], '#ffd84a', 10)
    calendar(d, 470, 650, "1000", scale=0.85)
    text_block(img, ["…et il ne se passe rien.", ("Le soleil se lève. Les vaches ont faim. On retourne au travail.", 1.2)], t, 1060, '#10253d', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#f6ead8'); header(d, hexc('#8a5a3c'))
    d.rounded_rectangle([s(260), s(420), s(820), s(860)], radius=s(20), fill=hexc('#fffaf0'), outline=hexc('#c9a97a'), width=s(6))
    for i in range(4):
        line(d, [(320, 520 + i * 80), (760, 520 + i * 80)], '#e3d2b4', 4)
    f = font(FBK, 110)
    tw = f.getlength("999") / S
    d.text((s(540 - tw / 2), s(450)), "999", font=f, fill=hexc('#2b1a10'))
    k = ease((t - 1.2) / 0.4)
    if k > 0:
        line(d, [(540 - tw / 2 - 20, 525), (540 - tw / 2 - 20 + (tw + 40) * k, 525)], '#b3121b', 14)
        tw2 = f.getlength("1000") / S
        d.text((s(540 - tw2 / 2), s(640)), "1000", font=f, fill=hexc('#b3121b', int(255 * k)))
    text_block(img, ["Le vrai drame du 1er janvier 1000 ?",
                     ("Écrire la date sans se tromper. Comme nous, chaque année.", 1.4)], t, 1010, '#2b1a10', size=64)

def sc_date(img, d, t, D):
    bg(d, '#24163d'); header(d, hexc('#d2b8ff'))
    calendar(d, 540, 630, "?", scale=0.95, txt_col='#7a5cff', tilt=10 * math.sin(t * 3))
    text_block(img, ["En réalité, peu de gens savaient même qu'on était en l'an 1000.",
                     ("Ils ne comptaient pas les années comme nous.", 1.8)], t, 1040, '#ffffff', size=62)

def sc_michelet(img, d, t, D):
    bg(d, '#3a2a10'); header(d, hexc('#ffd98a'))
    # un livre ouvert
    k = ease((t - 0.2) / 0.6)
    d.polygon([(s(540), s(500)), (s(220), s(450 + 30 * (1 - k))), (s(220), s(820)), (s(540), s(860))], fill=hexc('#fbf3e2'))
    d.polygon([(s(540), s(500)), (s(860), s(450 + 30 * (1 - k))), (s(860), s(820)), (s(540), s(860))], fill=hexc('#efe2c6'))
    line(d, [(540, 500), (540, 860)], '#c9a97a', 6)
    for i in range(5):
        line(d, [(270, 540 + i * 55), (500, 560 + i * 55)], '#c9a97a', 6)
        line(d, [(580, 560 + i * 55), (810, 540 + i * 55)], '#c9a97a', 6)
    ctext(d, "XIXe SIÈCLE", 360, 60, '#ffd98a', FBK, ease((t - 0.8) / 0.4))
    text_block(img, ["La grande panique a surtout été racontée 800 ans plus tard…",
                     ("…au XIXe siècle, par des historiens romantiques comme Michelet.", 1.8)], t, 1010, '#ffffff', size=60)

CHURCHES = [(170, 870, 0.55), (330, 840, 0.75), (540, 860, 0.95), (750, 840, 0.75), (910, 870, 0.55)]
def sc_glaber(img, d, t, D):
    bg(d, '#2f5d4a'); header(d, hexc('#c8f0d8'))
    order = [2, 1, 3, 0, 4]
    for n, idx in enumerate(order):
        x, y, sc = CHURCHES[idx]
        k = ease((t - 0.3 - n * 0.35) / 0.4)
        if k > 0:
            church(d, x, y + 40 * (1 - k), sc, '#ffffff', int(255 * k))
    text_block(img, ["Un moine de l'époque, Raoul Glaber, parle de famines…",
                     ("…puis d'un monde qui se couvre « d'un blanc manteau d'églises ».", 2.0)], t, 1010, '#ffffff', size=60)

def sc_science(img, d, t, D):
    bg(d, '#22264d'); stars(d, t); header(d, hexc('#c8ccff'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "LÉGENDE", 450, 150, '#c8ccff', FBK, k)
    ctext(d, "pour la plupart des historiens", 630, 44, '#c8ccff', FM, k)
    text_block(img, ["Des inquiétudes ont existé, surtout vers 1033, mille ans après la mort de Jésus.",
                     ("Mais pas de panique générale. Et le débat continue.", 2.0)], t, 1000, '#ffffff', size=58)

def sc_since(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    years = ["1000", "1033", "2000", "2012"]
    for i, y in enumerate(years):
        k = ease((t - 0.2 - i * 0.45) / 0.3)
        if k <= 0: continue
        x = 180 + i * 240
        d.rounded_rectangle([s(x - 100), s(520), s(x + 100), s(700)], radius=s(20), fill=hexc('#fbf3e2', int(255 * k)))
        f = font(FBK, 64); tw = f.getlength(y) / S
        d.text((s(x - tw / 2), s(570)), y, font=f, fill=hexc('#2b1a10', int(255 * k)))
        if t > 0.5 + i * 0.45:
            kk = ease((t - 0.5 - i * 0.45) / 0.25)
            line(d, [(x - 80, 540), (x - 80 + 160 * kk, 680)], '#b3121b', 12)
    text_block(img, ["Depuis, la fin du monde a été annoncée encore et encore.",
                     ("Taux de réussite : 0 %.", 2.4)], t, 1040, '#ffffff', size=66)

sc_title = scene_title(["MYTHE DE", "L'AN 1000"], "Scénario d'extinction n°52", color='#6b3a1f')
sc_end = scene_end("Bref : le monde n'a pas fini en l'an 1000. Les impôts non plus.", color='#6b3a1f')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_legend, 3.4), (sc_panic, 4.4), (sc_clock, 2.8),
    (sc_boom, 3.0), (sc_nothing, 4.2), (sc_joke, 4.4), (sc_date, 4.0),
    (sc_michelet, 4.8), (sc_glaber, 4.8), (sc_science, 5.0), (sc_since, 3.8), (sc_end, 4.8),
]
