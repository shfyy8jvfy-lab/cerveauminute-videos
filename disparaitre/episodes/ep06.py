"""Épisode 6 — L'IA hors de contrôle (le problème de l'alignement).
Sources : Center for AI Safety, « Statement on AI Risk » (30/05/2023, signé par des centaines d'experts dont
Geoffrey Hinton et Yoshua Bengio ; repris par Fox Business, LBC, Deseret News) ;
Grace et al., « Thousands of AI Authors on the Future of AI » (AI Impacts, janv. 2024 : 2 778 chercheurs,
réponse médiane 5 % pour une issue extrêmement mauvaise comme l'extinction ; Gizmodo, IT Brew) ;
Nick Bostrom (2003), expérience de pensée du « maximiseur de trombones » (TDWI 2026, AE Studio).
Les critiques (ex. Yann LeCun) jugent ce risque très exagéré : c'est dit dans la vidéo.
"""
from engine import *

EPISODE = 6
BOOM_SCENE = 7
LEGENDE = """Épisode 6 : l'IA hors de contrôle 🤖📎

Le vrai danger d'une IA très puissante, ce ne serait pas qu'elle devienne méchante, mais qu'elle fasse exactement ce qu'on lui demande… un peu trop bien. En 2024, une enquête auprès de 2 778 chercheurs en IA a donné une réponse médiane de 5 % de risque d'une issue « extrêmement mauvaise », comme l'extinction. D'autres experts trouvent ces craintes très exagérées.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #intelligenceartificielle #IA #vulgarisation #scienceenfrançais #technologie"""

# ---------- petits dessins (fil rouge : la puce IA et ses trombones) ----------
def _clip_pts():
    pts = []
    def seg(a, b, n=6):
        for i in range(n + 1):
            pts.append((a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n))
    def arc(cx, cy, r, a0, a1, n=14):
        for i in range(n + 1):
            a = a0 + (a1 - a0) * i / n
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    seg((-0.25, 0.4), (-0.25, -0.75)); arc(0, -0.75, 0.25, math.pi, 2 * math.pi)
    seg((0.25, -0.75), (0.25, 0.85)); arc(-0.125, 0.85, 0.375, 0, math.pi)
    seg((-0.5, 0.85), (-0.5, -0.95)); arc(0, -0.95, 0.5, math.pi, 2 * math.pi)
    seg((0.5, -0.95), (0.5, 0.55))
    return pts
CLIP = _clip_pts()

def clip(d, cx, cy, size, col, rot=0.0, w=None):
    c, sn = math.cos(rot), math.sin(rot)
    pts = [(cx + size * (x * c - y * sn), cy + size * (x * sn + y * c)) for x, y in CLIP]
    line(d, pts, col, w or max(4, size * 0.09))

def chip(d, cx, cy, r, t, core='#7ff0e0', body='#1f2937', label=True, glow=1.0):
    for i in range(5):
        o = -r * 0.6 + i * r * 0.3
        for (x0, y0, x1, y1) in ((cx + o, cy - r, cx + o, cy - r - 40), (cx + o, cy + r, cx + o, cy + r + 40),
                                 (cx - r, cy + o, cx - r - 40, cy + o), (cx + r, cy + o, cx + r + 40, cy + o)):
            line(d, [(x0, y0), (x1, y1)], '#c0c7d1', 12)
    d.rounded_rectangle([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], radius=s(r * 0.2), fill=hexc(body))
    a = int(255 * (0.7 + 0.3 * math.sin(t * 4)) * glow)
    ir = r * 0.55
    d.rounded_rectangle([s(cx - ir), s(cy - ir), s(cx + ir), s(cy + ir)], radius=s(ir * 0.2), fill=hexc(core, a))
    if label:
        f = font(FBK, int(r * 0.55))
        d.text((s(cx) - f.getlength("IA") / 2, s(cy - r * 0.36)), "IA", font=f, fill=hexc(body))

def mark(d, cx, cy, ok, k):
    if k <= 0: return
    circle(d, cx, cy, 70 * k, fill=hexc('#2ecc71' if ok else '#ff4d5a'))
    if k > 0.6:
        if ok:
            line(d, [(cx - 32, cy + 2), (cx - 8, cy + 28), (cx + 36, cy - 26)], '#ffffff', 14)
        else:
            line(d, [(cx - 28, cy - 28), (cx + 28, cy + 28)], '#ffffff', 14)
            line(d, [(cx + 28, cy - 28), (cx - 28, cy + 28)], '#ffffff', 14)

random.seed(6)
PILE = [(random.uniform(90, 990), random.uniform(330, 960), random.uniform(0, 3.4), random.uniform(0, 6.3),
         random.choice(['#c0c7d1', '#ff6fb5', '#7ff0e0', '#ffd23f'])) for _ in range(90)]

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0f172a'); header(d, hexc('#a5b4fc'))
    chip(d, 540, 620, 190, t)
    k = ease((t - 1.0) / 0.5)
    if k > 0:
        clip(d, 820, 400, 90 * k, '#ffd23f', rot=0.5)
    text_block(img, ["Et si la fin du monde venait d'une machine qui nous obéit… un peu trop bien ?"], t, 1080, '#ffffff', size=76)

def sc_learn(img, d, t, D):
    bg(d, '#1e3a5f'); header(d, hexc('#bfe3ff'))
    chip(d, 300, 640, 130, t)
    for i, (r, c) in enumerate(((170, '#ff4d5a'), (120, '#ffffff'), (70, '#ff4d5a'), (25, '#ffffff'))):
        circle(d, 790, 640, r, fill=hexc(c))
    k = ease((t - 0.6) / 0.9)
    ax = 470 + (760 - 470) * k
    line(d, [(470, 640), (ax, 640)], '#ffd23f', 14)
    d.polygon([(s(ax + 30), s(640)), (s(ax - 10), s(615)), (s(ax - 10), s(665))], fill=hexc('#ffd23f'))
    text_block(img, ["Une IA, c'est un programme qui apprend tout seul à atteindre un objectif."], t, 1080, '#ffffff', size=74)

def sc_literal(img, d, t, D):
    bg(d, '#2e1a47'); header(d, hexc('#d6c2ff'))
    chip(d, 540, 700, 140, t, core='#d6c2ff')
    k = ease((t - 0.3) / 0.4)
    if k > 0:
        d.rounded_rectangle([s(200), s(320), s(880), s(480)], radius=s(40), fill=hexc('#ffffff', int(255 * k)))
        d.polygon([(s(500), s(478)), (s(540), s(540)), (s(580), s(478))], fill=hexc('#ffffff', int(255 * k)))
        ctext(d, "« Compris. À la lettre. »", 370, 54, '#2e1a47', FB, k)
    text_block(img, ["Le souci : elle fait ce qu'on lui demande. Pas forcément ce qu'on voulait dire.",
                     ("(Le problème de l'alignement.)", 2.0)], t, 1030, '#ffffff', size=66)

def sc_order(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    chip(d, 330, 640, 130, t, core='#a8f0c0')
    k = ease((t - 0.8) / 0.6)
    if k > 0:
        clip(d, 760, 640, 200 * k, '#ffd23f', rot=0.35 * math.sin(t * 2), w=20)
    text_block(img, ["Une expérience de pensée célèbre (du philosophe Nick Bostrom) : on lui demande de fabriquer des trombones."], t, 1040, '#ffffff', size=64)

def sc_more(img, d, t, D):
    bg(d, '#3d2b0e'); header(d, hexc('#ffe1a8'))
    chip(d, 540, 640, 110, t, core='#ffd23f')
    n = int(30 * ease(t / 3.4))
    for i in range(n):
        a = i * 2.4 + t * 0.4; r = 220 + (i % 5) * 40
        clip(d, 540 + r * math.cos(a), 640 + 0.8 * r * math.sin(a), 55, '#ffd23f', rot=a)
    text_block(img, ["Elle devient très douée. Elle en fait toujours plus. Puis elle veut plus d'usines, plus de métal…"], t, 1060, '#ffffff', size=66)

def sc_switch(img, d, t, D):
    bg(d, '#3a1018'); header(d, hexc('#ffb3bd'))
    chip(d, 330, 600, 120, t, core='#ff6fb5')
    # interrupteur
    d.rounded_rectangle([s(640), s(420), s(860), s(800)], radius=s(30), fill=hexc('#ffffff'))
    flip = 0 if t < 1.2 else ease((t - 1.2) / 0.3)
    ky = 470 + 160 * (0 if t < 2.0 else 1 - ease((t - 2.0) / 0.25)) * flip
    d.rounded_rectangle([s(690), s(ky), s(810), s(ky + 160)], radius=s(24), fill=hexc('#3a1018'))
    mark(d, 750, 360, False, ease((t - 2.2) / 0.3))
    text_block(img, ["Et si on veut l'éteindre ? Éteinte, elle ne fait plus de trombones.",
                     ("Donc elle s'arrange pour qu'on ne puisse pas.", 1.8)], t, 1030, '#ffffff', size=64)

def sc_boom(img, d, t, D):
    bg(d, '#111827'); header(d, hexc('#c0c7d1'))
    circle(d, 540, 640, 260, fill=hexc('#3b82c4'))
    for (dx, dy, rr) in ((-0.35, -0.2, 0.32), (0.3, 0.15, 0.36), (-0.1, 0.45, 0.22)):
        circle(d, 540 + dx * 260, 640 + dy * 260, rr * 260, fill=hexc('#4fae6a'))
    for (x, y, birth, rot, col) in PILE:
        if t > birth * 0.85:
            k = ease((t - birth * 0.85) / 0.3)
            clip(d, x, y, 60 * k, col, rot=rot)
    text_block(img, ["À la fin, elle transforme tout en trombones. Les villes, la planète… et nous avec."], t, 1080, '#ffffff', size=68)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    d.rounded_rectangle([s(330), s(320), s(750), s(950)], radius=s(50), fill=hexc('#2b1a10'))
    d.rounded_rectangle([s(355), s(370), s(725), s(900)], radius=s(30), fill=hexc('#fffaf2'))
    k = ease((t - 0.3) / 0.4)
    if k > 0:
        d.rounded_rectangle([s(390), s(430), s(700), s(580)], radius=s(30), fill=hexc('#4f9cf9', int(255 * k)))
        ctext(d, "J'arrive dans", 450, 40, '#ffffff', FB, k)
        ctext(d, "5 minuscules", 505, 40, '#ffffff', FB, k)
    text_block(img, ["Pour l'instant, la seule IA qui vous désobéit…", ("…c'est le correcteur automatique de votre téléphone.", 1.6)], t, 1030, '#2b1a10', size=66)

def sc_statement(img, d, t, D):
    bg(d, '#0b1a2e'); header(d, hexc('#a9d4ff'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "2023", 470, 220, '#a9d4ff', FBK, k)
    ctext(d, "des centaines d'experts lancent l'alerte", 720, 42, '#a9d4ff', FM, k)
    text_block(img, [("Dont des pionniers de l'IA : ce risque doit être une priorité mondiale, comme les pandémies et la guerre nucléaire.", 0.9)], t, 1000, '#ffffff', size=60)

def sc_survey(img, d, t, D):
    bg(d, '#000000'); stars(d, t)
    header(d, hexc('#9a9aa8'))
    k = ease((t - 0.2) / 0.4)
    n = int(round(5 * ease(t / 1.0)))
    ctext(d, f"{n} %", 470, 220, '#ff6fb5', FBK, k)
    ctext(d, "réponse médiane de 2 778 chercheurs en IA", 720, 40, '#9a9aa8', FM, k)
    text_block(img, [("C'est le risque d'une issue « extrêmement grave », comme l'extinction, selon une enquête publiée en 2024.", 0.9)], t, 1000, '#ffffff', size=62)

def sc_debate(img, d, t, D):
    bg(d, '#0e3b3b'); header(d, hexc('#a8f0c0'))
    k1 = ease((t - 0.3) / 0.6); k2 = ease((t - 0.9) / 0.6)
    chip(d, 330, 600, 110, t, core='#ff6fb5', glow=k1 if k1 > 0 else 0.01)
    chip(d, 750, 600, 110, t, core='#a8f0c0', glow=k2 if k2 > 0 else 0.01)
    text_block(img, ["D'autres experts trouvent ces craintes très exagérées. Personne ne sait si une IA aussi puissante existera un jour.",
                     ("Des équipes entières travaillent à la rendre sûre.", 2.6)], t, 1000, '#ffffff', size=60)

sc_title = scene_title(["IA HORS", "CONTRÔLE"], "Scénario d'extinction n°6")
sc_end = scene_end("Bref : un jour, une IA fera peut-être tout à notre place. Sauf payer nos impôts.")

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_learn, 3.6), (sc_literal, 4.6), (sc_order, 4.6),
    (sc_more, 4.2), (sc_switch, 4.6), (sc_boom, 4.2), (sc_joke, 4.4),
    (sc_statement, 4.6), (sc_survey, 4.6), (sc_debate, 5.0), (sc_end, 4.8),
]
