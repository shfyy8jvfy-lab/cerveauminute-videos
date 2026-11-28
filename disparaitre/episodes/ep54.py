"""Épisode 54 — Mythe : le bug de 2038.
Sources :
- Wikipedia (« Year 2038 problem ») et Epoch Converter (simulation 32 bits) : le temps Unix compte les secondes
  depuis le 1er janvier 1970 (UTC) ; stocké sur 32 bits signés, le maximum est 2 147 483 647, atteint le
  19 janvier 2038 à 03:14:07 UTC ; la seconde suivante, la valeur devient négative et la date lue est le
  13 décembre 1901 (20:45:52 UTC) ; sur 64 bits, la limite recule d'environ 292 milliards d'années.
- TechTarget (« The Unix year 2038 problem ») et Hackaday (« The Epochalypse », juil. 2025) : risques surtout
  pour les systèmes embarqués anciens rarement mis à jour (automates, capteurs, appareils industriels) ;
  les systèmes modernes 64 bits ne sont pas concernés.
- LWN / glibc (« Y2038 Proofness Design ») : Linux (5.6, 2020) et la glibc permettent le temps sur 64 bits
  même sur les machines 32 bits ; The Register (25/07/2025) : Debian passe au temps 64 bits pour presque tout.
Choix prudents : « heure de Londres » = UTC en janvier ; on parle de pannes possibles sur de vieux appareils,
sans citer d'incident précis ; âge de l'univers ≈ 13,8 milliards d'années (292 milliards est bien plus grand).
"""
from engine import *

EPISODE = 54
BOOM_SCENE = 6
LEGENDE = """Épisode 54 : le bug de 2038 ⏱️💻

Beaucoup d'ordinateurs comptent le temps en secondes depuis le 1er janvier 1970. Sur les vieux systèmes 32 bits, ce compteur plafonne à 2 147 483 647 : le 19 janvier 2038 à 3 h 14 min 07 s (heure de Londres), il déborde et la date repart au 13 décembre 1901. Les systèmes modernes en 64 bits tiennent, eux, environ 292 milliards d'années. Le vrai risque : de vieux appareils jamais mis à jour.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #bug2038 #informatique #mythe #linux #science #vulgarisation #apocalypse"""

# ---------- fil rouge : le compteur à chiffres ----------
def counter(d, cx, cy, digits, col='#7dffb0', box='#0a0f14', frame='#d9e2ec', size=118, a=255, red_from=None):
    n = len(digits)
    f = font(FBK, size)
    cw = size * 0.74
    w = n * cw + 60
    h = size * 1.6
    d.rounded_rectangle([s(cx - w / 2 - 18), s(cy - h / 2 - 18), s(cx + w / 2 + 18), s(cy + h / 2 + 18)],
                        radius=s(34), fill=hexc(frame, a))
    d.rounded_rectangle([s(cx - w / 2), s(cy - h / 2), s(cx + w / 2), s(cy + h / 2)], radius=s(24), fill=hexc(box, a))
    x0 = cx - n * cw / 2
    for i, ch in enumerate(digits):
        x = x0 + i * cw
        if i > 0:
            d.line([(s(x), s(cy - h / 2 + 12)), (s(x), s(cy + h / 2 - 12))], fill=hexc('#ffffff', int(a * 0.12)), width=s(3))
        c = col if (red_from is None or i < red_from) else '#ff5c6a'
        tw = f.getlength(ch) / S
        d.text((s(x + cw / 2 - tw / 2), s(cy - size * 0.62)), ch, font=f, fill=hexc(c, a))

def clock(d, cx, cy, r, t, col='#ffffff', speed=1.0):
    circle(d, cx, cy, r, outline=hexc(col), width=s(12))
    for i in range(12):
        a = i * math.pi / 6
        line(d, [(cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a)), (cx + (r - 12) * math.cos(a), cy + (r - 12) * math.sin(a))], col, 8)
    a1 = -math.pi / 2 + t * 6 * speed
    a2 = -math.pi / 2 + t * 0.5 * speed
    line(d, [(cx, cy), (cx + (r - 45) * math.cos(a1), cy + (r - 45) * math.sin(a1))], col, 10)
    line(d, [(cx, cy), (cx + (r - 90) * math.cos(a2), cy + (r - 90) * math.sin(a2))], col, 16)
    circle(d, cx, cy, 16, fill=hexc(col))

def calendar(d, cx, cy, top, big, col='#c0392b', a=255, wob=0):
    d.rounded_rectangle([s(cx - 210), s(cy - 220 + wob), s(cx + 210), s(cy + 220 + wob)], radius=s(36), fill=hexc('#ffffff', a))
    d.rounded_rectangle([s(cx - 210), s(cy - 220 + wob), s(cx + 210), s(cy - 90 + wob)], radius=s(36), fill=hexc(col, a))
    d.rectangle([s(cx - 210), s(cy - 130 + wob), s(cx + 210), s(cy - 90 + wob)], fill=hexc(col, a))
    ctext(d, top, cy - 186 + wob, 44, '#ffffff', FB, a / 255)
    ctext(d, big, cy - 50 + wob, 170, '#1d1d1d', FBK, a / 255)

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0e1a26'); header(d, hexc('#8fd3ff'))
    clock(d, 540, 620, 260, t, '#8fd3ff', speed=1.4)
    text_block(img, ["Et si la fin du monde était… une simple erreur de calcul ?"], t, 1090, '#ffffff', size=78)

def sc_count(img, d, t, D):
    bg(d, '#1f2a4d'); header(d, hexc('#a9c4ff'))
    n = int(t * 7)
    counter(d, 540, 520, f"{n:010d}")
    ctext(d, "secondes depuis le 1er janvier 1970", 700, 42, '#a9c4ff', FM, ease((t - 0.3) / 0.4))
    text_block(img, ["Beaucoup d'ordinateurs comptent le temps…",
                     ("…en secondes, depuis le 1er janvier 1970.", 1.5)], t, 1030, '#ffffff', size=70)

def sc_box(img, d, t, D):
    bg(d, '#2d1f47'); header(d, hexc('#d2b8ff'))
    counter(d, 540, 520, "2147483647", col='#ffd36b')
    k = ease((t - 1.2) / 0.4)
    ctext(d, "LE MAXIMUM", 700, 50, '#ffd36b', FB, k)
    text_block(img, ["Ce nombre est rangé dans une boîte de taille fixe (32 bits).",
                     ("Sur les vieux systèmes, elle ne va pas plus loin que ça.", 1.6)], t, 1030, '#ffffff', size=64)

def sc_date(img, d, t, D):
    bg(d, '#123329'); header(d, hexc('#a8f0c0'))
    calendar(d, 540, 610, "JANVIER 2038", "19", col='#1f7a52', wob=6 * math.sin(t * 3))
    text_block(img, ["Ce plafond sera atteint le 19 janvier 2038…",
                     ("…à 3 h 14 min 07 s, heure de Londres.", 1.4)], t, 1060, '#ffffff', size=70)

def sc_tick(img, d, t, D):
    bg(d, '#3a2a10'); header(d, hexc('#ffd98a'))
    shake = 6 * math.sin(t * 45) * ease((t - 1.0) / 1.5)
    counter(d, 540 + shake, 560, "2147483647", col='#ffd36b', red_from=0 if t > 2.0 and int(t * 5) % 2 == 0 else None)
    text_block(img, [("Et une seconde plus tard…", 0.2), ("…le compteur déborde.", 1.6)], t, 1080, '#ffffff', size=80)

def sc_boom(img, d, t, D):
    bg(d, '#4a0f16'); header(d, hexc('#ffb3bd'))
    k = ease((t - 0.2) / 0.5)
    if k < 0.5:
        counter(d, 540, 390, "2147483647", col='#ff5c6a', size=80)
    else:
        counter(d, 540, 390, "-2147483648", col='#ff5c6a', size=74)
    k2 = ease((t - 0.9) / 0.5)
    if k2 > 0:
        calendar(d, 540, 730 - 30 * (1 - k2), "DÉCEMBRE 1901", "13", col='#7a1f2b', a=int(255 * k2))
    text_block(img, [("Il devient négatif, et l'ordinateur croit qu'on est le 13 décembre 1901.", 1.0)], t, 1080, '#ffffff', size=66)

def sc_fears(img, d, t, D):
    bg(d, '#24163d'); header(d, hexc('#f0b8ff'))
    labels = ["avions cloués au sol", "banques en panne", "plus d'électricité"]
    for i, l in enumerate(labels):
        y = 400 + i * 150; k = ease((t - 0.3 - i * 0.5) / 0.3)
        if k <= 0: continue
        ctext(d, l, y, 56, '#ffffff', FB, k)
    k = ease((t - 2.3) / 0.3)
    if k > 0:
        ctext(d, "Vraiment ?", 860, 64, '#ffd36b', FBK, k)
    text_block(img, ["Sur internet, on lit que tout va s'arrêter d'un coup."], t, 1080, '#ffffff', size=70)

def sc_joke(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    d.rounded_rectangle([s(230), s(420), s(850), s(860)], radius=s(40), fill=hexc('#d9d2c5'))
    d.rounded_rectangle([s(280), s(470), s(640), s(810)], radius=s(26), fill=hexc('#3b3b3b'))
    d.rounded_rectangle([s(670), s(480), s(810), s(560)], radius=s(14), fill=hexc('#10261a'))
    if int(t * 2) % 2 == 0:
        ctext(d, "00:00", 506, 44, '#5cff8a', FBK, 1)
    for i in range(3):
        circle(d, 740, 620 + i * 70, 22, fill=hexc('#8a5a3c'))
    text_block(img, ["Au pire, votre vieux micro-ondes affichera 1901…",
                     ("…comme votre four affiche 00:00 depuis trois ans.", 1.8)], t, 1010, '#2b1a10', size=66)

def sc_fix(img, d, t, D):
    bg(d, '#0f3b3a'); header(d, hexc('#9ff0e0'))
    k = ease((t - 0.6) / 0.8)
    n = 10 + int(9 * k)
    counter(d, 540, 560, "9" * n if k < 1 else "9" * 19, col='#7dffb0', size=int(118 - 58 * k))
    ctext(d, "64 bits", 760, 56, '#9ff0e0', FB, ease((t - 1.2) / 0.4))
    text_block(img, ["La solution existe : une boîte beaucoup plus grande (64 bits).",
                     ("Les ordinateurs et téléphones récents l'utilisent déjà.", 1.8)], t, 1040, '#ffffff', size=62)

def sc_years(img, d, t, D):
    bg(d, '#000000'); stars(d, t)
    header(d, hexc('#9a9aa8'))
    k = ease((t - 0.2) / 0.4)
    n = int(292 * ease(t / 1.3))
    ctext(d, f"{n} milliards", 470, 130, '#ffd36b', FBK, k)
    ctext(d, "d'années avant le prochain débordement", 690, 42, '#9a9aa8', FM, k)
    text_block(img, [("Bien plus que l'âge de l'univers. On a de la marge.", 1.0)], t, 1060, '#ffffff', size=70)

def sc_risk(img, d, t, D):
    bg(d, '#1b2a4a'); header(d, hexc('#9fc2ff'))
    for i in range(3):
        x = 260 + i * 280; y = 600 + 8 * math.sin(t * 3 + i)
        d.rounded_rectangle([s(x - 100), s(y - 120), s(x + 100), s(y + 120)], radius=s(26), fill=hexc('#9fc2ff'))
        d.rounded_rectangle([s(x - 70), s(y - 90), s(x + 70), s(y - 10)], radius=s(12), fill=hexc('#10261a'))
        circle(d, x, y + 60, 22, fill=hexc('#1b2a4a'))
        if ease((t - 1.5 - i * 0.3) / 0.3) > 0:
            circle(d, x + 85, y - 105, 34, fill=hexc('#ff9f43'))
            f = font(FBK, 48); tw = f.getlength("!") / S
            d.text((s(x + 85 - tw / 2), s(y - 105 - 30)), "!", font=f, fill=hexc('#ffffff'))
    text_block(img, ["Le vrai risque : de vieux appareils jamais mis à jour (machines, capteurs).",
                     ("Des pannes possibles. Une extinction : non.", 2.0)], t, 1030, '#ffffff', size=60)

sc_title = scene_title(["BUG DE", "2038"], "Mythe à démonter · n°54", color='#1f3f6b')
sc_end = scene_end("Bref : les ordinateurs survivront à 2038. Et votre avis d'imposition aussi.", color='#1f3f6b')

SCENES = [
    (sc_hook, 3.2), (sc_title, 2.4), (sc_count, 4.2), (sc_box, 4.4), (sc_date, 4.0),
    (sc_tick, 3.6), (sc_boom, 4.4), (sc_fears, 3.8), (sc_joke, 4.6),
    (sc_fix, 4.6), (sc_years, 4.0), (sc_risk, 5.0), (sc_end, 4.8),
]
