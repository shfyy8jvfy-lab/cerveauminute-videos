"""Épisode 35 — Mythe : la queue de la comète de Halley en 1910 (les pilules anti-comète).
Sources :
- Science History Institute, Distillations (S. Kean, « The Comet Panic of 1910, Revisited », 16 janv. 2025) :
  l'observatoire Yerkes annonce le 7 févr. 1910 avoir détecté du cyanogène (C2N2, cousin du cyanure)
  dans la queue par analyse spectrale ; la Terre devait traverser la queue mi-mai 1910 ;
  Flammarion (interrogé par le New York Times) : le gaz pourrait « imprégner l'atmosphère et peut-être
  éteindre toute vie sur la planète » ; la plupart des autres astronomes réfutent ; Flammarion lui-même
  écrivait que la queue est « bien plus clairsemée qu'un nuage » ; « pilules anti-comète »,
  « assurance comète » ; gens qui bouchent portes et serrures ; retours de Halley espacés d'environ 76 ans.
- BBC Sky at Night Magazine (J. Powell, 11 nov. 2022) : pilules anti-comète, masques à gaz,
  papier autour des portes, parapluies anti-comète ; la Terre est sortie indemne.
- Space.com (J. Rao, 8 déc. 2023) : aphélie le 9 déc. 2023, prochain périhélie le 28 juillet 2061.
"""
from engine import *

EPISODE = 35
BOOM_SCENE = 5
LEGENDE = """Épisode 35 : la panique de la comète de Halley ☄️💊

En 1910, des astronomes détectent du cyanogène (un cousin du cyanure) dans la queue de la comète de Halley… juste avant que la Terre la traverse. Panique : on vend des pilules anti-comète, des masques à gaz et même des parapluies anti-comète. Résultat ? Rien du tout : la queue d'une comète est plus vide qu'un nuage (Science History Institute).

On va tous disparaître… mais pas aujourd'hui.

#findumonde #apocalypse #science #astronomie #comete #halley #histoire #vulgarisation #scienceenfrançais"""

# ---------- petits dessins ----------
def comet(d, cx, cy, t, scale=1.0, tail_a=200, tail_len=520):
    """La comète : fil rouge de l'épisode. Queue vers la gauche."""
    for i in range(6):
        k = i / 5
        y_off = (i - 2.5) * 34 * scale
        pts = [(cx - j * tail_len / 12 * scale, cy + y_off * (j / 12) + 6 * math.sin(j * 0.8 + t * 3 + i)) for j in range(13)]
        line(d, pts, hexc('#bfe3ff' if i % 2 else '#7fc8ff', int(tail_a * (1 - 0.5 * abs(k - 0.5)))), int(14 * scale))
    circle(d, cx, cy, 70 * scale, fill=hexc('#ffffff', 70))
    circle(d, cx, cy, 45 * scale, fill=hexc('#fff6c8'))

def earth(d, cx, cy, r):
    circle(d, cx, cy, r, fill=hexc('#2f7fd6'))
    circle(d, cx - r * 0.3, cy - r * 0.2, r * 0.38, fill=hexc('#3fbf6f'))
    circle(d, cx + r * 0.35, cy + r * 0.3, r * 0.28, fill=hexc('#3fbf6f'))

def pill(d, cx, cy, col1, col2, ang=0.0, L=90, R=34):
    dx, dy = math.cos(ang) * L / 2, math.sin(ang) * L / 2
    line(d, [(cx - dx, cy - dy), (cx, cy)], col1, R * 2)
    line(d, [(cx, cy), (cx + dx, cy + dy)], col2, R * 2)
    circle(d, cx - dx, cy - dy, R, fill=hexc(col1))
    circle(d, cx + dx, cy + dy, R, fill=hexc(col2))

def umbrella(d, cx, cy, col, w=1.0):
    d.pieslice([s(cx - 150 * w), s(cy - 120 * w), s(cx + 150 * w), s(cy + 120 * w)], 180, 360, fill=hexc(col))
    line(d, [(cx, cy), (cx, cy + 170 * w)], '#ffffff', 10)
    d.arc([s(cx - 40 * w), s(cy + 140 * w), s(cx), s(cy + 200 * w)], 0, 180, fill=hexc('#ffffff'), width=s(10))

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#101833'); stars(d, t); header(d, hexc('#9fc2ff'))
    k = ease((t - 0.5) / 0.6)
    pill(d, 540, 640, '#ff6fb5', '#ffffff', ang=0.3 * math.sin(t * 2), L=220 * k + 1, R=80 * k + 1)
    text_block(img, ["Et si un jour on vous vendait des pilules… contre une comète ?"], t, 1080, '#ffffff', size=76)

def sc_return(img, d, t, D):
    bg(d, '#0b1f3a'); stars(d, t); header(d, hexc('#a9d6ff'))
    k = ease((t - 0.2) / 2.8)
    comet(d, 1000 - 380 * k, 480 + 120 * k, t, scale=0.8)
    earth(d, 260, 820, 90)
    text_block(img, ["1910 : la comète de Halley revient, comme environ tous les 76 ans.", ("Et cette fois, la Terre va passer dans sa queue.", 1.5)], t, 1030, '#ffffff', size=64)

def sc_spectro(img, d, t, D):
    bg(d, '#2a1840'); header(d, hexc('#d6c2ff'))
    comet(d, 260, 520, t, scale=0.55, tail_len=300)
    k = ease((t - 0.3) / 0.8)
    d.polygon([(s(330), s(520)), (s(560), s(440)), (s(560), s(600))], fill=hexc('#ffffff', int(60 * k)))
    d.polygon([(s(560), s(440)), (s(660), s(600)), (s(460), s(600))], fill=hexc('#e8e8ff'))
    cols = ['#ff4d5a', '#ff9a3d', '#ffd166', '#3fbf6f', '#3fa0ff', '#8a5cff']
    for i, c in enumerate(cols):
        kk = ease((t - 0.8 - i * 0.1) / 0.3)
        if kk > 0:
            d.rectangle([s(700 + i * 50), s(420), s(700 + i * 50 + 44), s(420 + 200 * kk)], fill=hexc(c))
    kk = ease((t - 1.8) / 0.3)
    if kk > 0:
        d.rectangle([s(842), s(400), s(852), s(640)], fill=hexc('#000000'))
        ctext(d, "CYANOGÈNE !", 760, 60, '#ff6fb5', FBK, kk)
    text_block(img, ["Des astronomes analysent sa lumière (spectroscopie)…", ("…et y trouvent du cyanogène, un gaz cousin du cyanure.", 1.4)], t, 1030, '#ffffff', size=62)

def sc_flammarion(img, d, t, D):
    bg(d, '#3a2a12'); header(d, hexc('#ffd59e'))
    d.rounded_rectangle([s(250), s(340), s(830), s(920)], radius=s(20), fill=hexc('#f3ead6'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "LA FIN", 400, 96, '#1a1a1a', FBK, k)
    ctext(d, "DU MONDE ?", 500, 72, '#b3121b', FBK, k)
    for i in range(6):
        w = 460 if i % 3 else 300
        d.rectangle([s(310), s(600 + i * 48), s(310 + w), s(620 + i * 48)], fill=hexc('#9a8f78'))
    text_block(img, ["Un astronome célèbre, Camille Flammarion, imagine que ce gaz pourrait…", ("…« peut-être éteindre toute vie sur la planète ».", 1.6)], t, 1020, '#ffffff', size=62)

random.seed(35)
PILLS = [(random.uniform(120, 960), random.uniform(-200, 200), random.uniform(0, 3.2), random.random() * 6,
          random.choice([('#ff6fb5', '#ffffff'), ('#ffd166', '#ff4d5a'), ('#7ff0e0', '#3fa0ff')])) for _ in range(28)]
def sc_boom(img, d, t, D):
    bg(d, '#5a0f1e'); header(d, hexc('#ffb3bd'))
    for (x, y0, birth, a, (c1, c2)) in PILLS:
        if t > birth * 0.8:
            y = 320 + y0 * 0.2 + (t - birth * 0.8) * 420
            if y < 960:
                pill(d, x, y, c1, c2, ang=a + t * 2, L=60, R=22)
    k = ease((t - 1.0) / 0.4)
    if k > 0:
        umbrella(d, 540, 560, '#ffd166', w=k)
    text_block(img, ["Panique ! On vend des pilules anti-comète, des masques à gaz…", ("…et même des parapluies anti-comète.", 1.6)], t, 1030, '#ffffff', size=64)

def sc_door(img, d, t, D):
    bg(d, '#1d3b4a'); header(d, hexc('#a6e6ff'))
    d.rounded_rectangle([s(360), s(330), s(720), s(940)], radius=s(16), fill=hexc('#8a5a3c'))
    circle(d, 670, 640, 18, fill=hexc('#ffd166'))
    for i in range(5):
        kk = ease((t - 0.3 - i * 0.35) / 0.3)
        if kk > 0:
            y = 360 + i * 130
            d.rectangle([s(330), s(y), s(330 + 60 * kk), s(y + 90)], fill=hexc('#ffffff'))
            d.rectangle([s(750 - 60 * kk), s(y + 40), s(750), s(y + 130)], fill=hexc('#ffffff'))
    text_block(img, ["Certains bouchent portes et serrures avec du papier.", ("Un malin vend même une « assurance comète ».", 1.5)], t, 1030, '#ffffff', size=64)

def sc_empty(img, d, t, D):
    bg(d, '#0f3d2e'); header(d, hexc('#9fe3b0'))
    # une boîte = un morceau de queue de comète : presque vide
    d.rounded_rectangle([s(240), s(360), s(840), s(900)], radius=s(30), outline=hexc('#9fe3b0'), width=s(10))
    for i in range(4):
        x = 330 + (i * 157) % 420 + 30 * math.sin(t * 1.5 + i)
        y = 450 + (i * 113) % 350 + 25 * math.cos(t * 1.3 + i)
        circle(d, x, y, 7, fill=hexc('#ffffff'))
    ctext(d, "(presque) RIEN", 960, 44, '#9fe3b0', FB, ease((t - 0.6) / 0.4))
    text_block(img, ["Le hic : la queue d'une comète est incroyablement vide.", ("Flammarion lui-même l'écrivait : bien plus légère qu'un nuage.", 1.5)], t, 1060, '#ffffff', size=60)

def sc_result(img, d, t, D):
    bg(d, '#14213d'); stars(d, t); header(d, hexc('#b8c8ff'))
    k = ease((t - 0.2) / 2.0)
    comet(d, 880 - 200 * k, 520, t, scale=0.9, tail_a=140, tail_len=700)
    earth(d, 380, 560, 110)
    kk = ease((t - 1.8) / 0.3)
    if kk > 0:
        ctext(d, "RIEN.", 800, 110, '#ffd166', FBK, kk)
    text_block(img, ["Mai 1910 : la Terre traverse la queue. Résultat…", ("…rien. Absolument rien.", 1.8)], t, 1060, '#ffffff', size=68)

def sc_joke(img, d, t, D):
    bg(d, '#f2e8cf'); header(d, hexc('#7a5c2e'))
    d.rounded_rectangle([s(370), s(380), s(710), s(900)], radius=s(40), fill=hexc('#ffffff'), outline=hexc('#7a5c2e'), width=s(10))
    d.rectangle([s(370), s(380), s(710), s(470)], fill=hexc('#7a5c2e'))
    ctext(d, "100 %", 620, 90, '#2f8f5a', FBK, ease((t - 0.4) / 0.4))
    ctext(d, "efficace", 720, 44, '#7a5c2e', FB, ease((t - 0.6) / 0.4))
    for i in range(3):
        pill(d, 450 + i * 90, 820 + 6 * math.sin(t * 4 + i), '#ff6fb5', '#ffffff', ang=0.6, L=40, R=16)
    text_block(img, ["Les pilules anti-comète ont donc marché à 100 %.", ("Comme votre spray anti-dinosaures : aucun dinosaure dans le jardin.", 1.6)], t, 1020, '#2b1a10', size=60)

def sc_myth(img, d, t, D):
    bg(d, '#24163d'); header(d, hexc('#d2b8ff'))
    k = ease((t - 0.2) / 0.4)
    ctext(d, "MYTHE", 520, 170, '#ff6fb5', FBK, k)
    kk = ease((t - 0.7) / 0.4)
    if kk > 0:
        line(d, [(220, 520), (220 + 640 * kk, 520)], '#ffffff', 14)
    text_block(img, ["Déjà en 1910, la plupart des astronomes le disaient : ce gaz est bien trop dilué pour nous faire du mal."], t, 1040, '#ffffff', size=62)

def sc_2061(img, d, t, D):
    bg(d, '#0b2a3a'); stars(d, t); header(d, hexc('#8fd3ff'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "2061", 430, 220, '#ffd166', FBK, k)
    comet(d, 760 + 20 * math.sin(t), 780, t, scale=0.6, tail_len=420)
    text_block(img, [("Prochain passage de Halley : l'été 2061.", 0.6), ("Inutile de stocker des pilules d'ici là.", 1.6)], t, 1060, '#ffffff', size=66)

sc_title = scene_title(["LA COMÈTE", "DE HALLEY"], "Scénario d'extinction n°35")
sc_end = scene_end("Bref : la comète n'a tué personne. Vos impôts, eux, repassent tous les ans.")

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_return, 4.4), (sc_spectro, 4.6), (sc_flammarion, 4.6),
    (sc_boom, 4.6), (sc_door, 4.2), (sc_empty, 4.4), (sc_result, 4.0),
    (sc_joke, 4.6), (sc_myth, 4.4), (sc_2061, 4.0), (sc_end, 4.8),
]
