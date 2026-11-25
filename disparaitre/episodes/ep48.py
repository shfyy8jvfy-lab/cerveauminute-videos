"""Épisode 48 — Mythe : le bug de l'an 2000.
Sources :
- The Conversation, « If you think the millennium bug was a hoax, here comes a history lesson » (déc. 2019) :
  années stockées sur deux chiffres pour économiser une mémoire chère (années 1970 à début 1990) ; préparation
  estimée à environ 300 milliards de dollars ; le 1er janvier 2000, « guère plus que des problèmes mineurs » ;
  ce n'était pas un canular : les correctifs ont protégé tout le monde ; problème de 2038 (compteur de secondes
  Unix sur 32 bits depuis 1970), la plupart des systèmes concernés devraient être remplacés avant.
- TIME (F. Uenuma, 30 déc. 2019) : deux chiffres « pour économiser la mémoire, alors très chère » ; « 00 » lu comme
  1900 ; environ 100 milliards de dollars dépensés aux États-Unis ; un vidéoclub a facturé à un client un siècle
  de frais de retard ; après coup, beaucoup ont parlé de canular, alors que les experts disent que rien ne s'est
  passé précisément parce qu'on s'est préparé.
- Computerworld (2000/2010), Britannica (notice « Y2K bug ») : mêmes ordres de grandeur, incidents mineurs.
Choix prudents : « environ 300 milliards de dollars » dans le monde ; pas d'incident précis non vérifié deux fois
(seul l'exemple du vidéoclub, rapporté par TIME, est cité, sans chiffre).
"""
from engine import *

EPISODE = 48
BOOM_SCENE = 7
LEGENDE = """Épisode 48 : le bug de l'an 2000 💻🎆

Pour économiser une mémoire très chère, les vieux ordinateurs écrivaient l'année avec deux chiffres : après 99 venait 00… soit 1900. Le monde a dépensé environ 300 milliards de dollars pour corriger le code, et le 1er janvier 2000, il ne s'est presque rien passé. Pas un canular : un problème réel, réglé à temps (The Conversation, TIME).

On va tous disparaître… mais pas aujourd'hui.

#findumonde #an2000 #bug #informatique #histoire #mythe #science #vulgarisation"""

# ---------- fil rouge : le vieil ordinateur ----------
def monitor(d, cx, cy, txt, txt_col='#5cff8a', scale=1.0, screen='#0b1a0f', body='#e8dcc0', a=255, txt_size=None):
    w, h = 300 * scale, 230 * scale
    d.rounded_rectangle([s(cx - w), s(cy - h), s(cx + w), s(cy + h)], radius=s(40 * scale), fill=hexc(body, a))
    d.rounded_rectangle([s(cx - w + 40 * scale), s(cy - h + 40 * scale), s(cx + w - 40 * scale), s(cy + h - 70 * scale)],
                        radius=s(30 * scale), fill=hexc(screen, a))
    circle(d, cx + w - 70 * scale, cy + h - 36 * scale, 12 * scale, fill=hexc('#2ecc71', a))
    d.rounded_rectangle([s(cx - 70 * scale), s(cy + h), s(cx + 70 * scale), s(cy + h + 40 * scale)], fill=hexc(body, a))
    d.rounded_rectangle([s(cx - 180 * scale), s(cy + h + 35 * scale), s(cx + 180 * scale), s(cy + h + 65 * scale)],
                        radius=s(14 * scale), fill=hexc(body, a))
    if txt:
        size = txt_size or int(150 * scale)
        f = font(FBK, size)
        tw = f.getlength(txt) / S
        d.text((s(cx - tw / 2), s(cy - 15 * scale - size * 0.62)), txt, font=f, fill=hexc(txt_col, a))

def cursor_on(t): return int(t * 2.5) % 2 == 0

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#101820'); header(d, hexc('#8fd3ff'))
    monitor(d, 540, 600, "00" + ("_" if cursor_on(t) else " "))
    text_block(img, ["Et si deux petits zéros suffisaient à tout arrêter ?"], t, 1100, '#ffffff', size=80)

def sc_memory(img, d, t, D):
    bg(d, '#2d1f47'); header(d, hexc('#d2b8ff'))
    k = ease((t - 0.8) / 0.6)
    monitor(d, 540, 600, None)
    f = font(FBK, 150)
    txt = "1975" if k < 0.5 else "75"
    tw = f.getlength(txt) / S
    d.text((s(540 - tw / 2), s(492)), txt, font=f, fill=hexc('#5cff8a'))
    text_block(img, ["Dans les années 1970, la mémoire des ordinateurs coûtait une fortune.",
                     ("Alors on écrivait l'année avec deux chiffres : 75, 86, 99…", 1.6)], t, 1040, '#ffffff', size=64)

def sc_count(img, d, t, D):
    bg(d, '#0f3b3a'); header(d, hexc('#9ff0e0'))
    seq = ["97", "98", "99", "00"]
    i = min(3, int(t / 0.7))
    col = '#ff5c6a' if i == 3 else '#5cff8a'
    monitor(d, 540, 600, seq[i], txt_col=col)
    text_block(img, [("Problème : après 99…", 0.2), ("…il y a 00.", 2.1)], t, 1100, '#ffffff', size=82)

def sc_1900(img, d, t, D):
    bg(d, '#3a2a10'); header(d, hexc('#ffd98a'))
    k = ease((t - 1.0) / 0.5)
    txt = "1900" if k > 0.5 else "00"
    monitor(d, 540, 600, txt, txt_col='#ff5c6a')
    if k > 0.5:
        ctext(d, "?!", 250, 90, '#ffd98a', FBK, k)
    text_block(img, ["Pour l'ordinateur, 00, ce n'était pas 2000.", ("C'était 1900.", 1.4)], t, 1080, '#ffffff', size=72)

def sc_calc(img, d, t, D):
    bg(d, '#123a1e'); header(d, hexc('#a8f0c0'))
    monitor(d, 540, 600, None)
    lines_ = ["NÉ EN : 75", "ANNÉE : 00", "ÂGE : -75 ANS"]
    for i, l in enumerate(lines_):
        k = ease((t - 0.3 - i * 0.6) / 0.3)
        if k <= 0: continue
        f = font(FB, 56); tw = f.getlength(l) / S
        d.text((s(540 - tw / 2), s(450 + i * 85)), l, font=f, fill=hexc('#ff5c6a' if i == 2 else '#5cff8a', int(255 * k)))
    text_block(img, [("Âges, intérêts, échéances, factures : tous les calculs de dates risquaient de devenir absurdes.", 1.9)],
               t, 1060, '#ffffff', size=62)

def plane(d, x, y, col, a=255):
    c = hexc(col, a)
    d.rounded_rectangle([s(x - 90), s(y - 16), s(x + 90), s(y + 16)], radius=s(16), fill=c)
    d.polygon([(s(x - 10), s(y)), (s(x + 30), s(y)), (s(x - 30), s(y + 80)), (s(x - 60), s(y + 80))], fill=c)
    d.polygon([(s(x - 10), s(y)), (s(x + 30), s(y)), (s(x - 30), s(y - 80)), (s(x - 60), s(y - 80))], fill=c)
    d.polygon([(s(x - 90), s(y)), (s(x - 70), s(y)), (s(x - 95), s(y - 45)), (s(x - 110), s(y - 45))], fill=c)

def bulb(d, x, y, on, a=255):
    circle(d, x, y, 55, fill=hexc('#ffe066' if on else '#555566', a))
    d.rounded_rectangle([s(x - 28), s(y + 45), s(x + 28), s(y + 95)], radius=s(8), fill=hexc('#9a9aa8', a))

def can(d, x, y, a=255):
    d.rounded_rectangle([s(x - 50), s(y - 70), s(x + 50), s(y + 70)], radius=s(14), fill=hexc('#c8ccd6', a))
    d.rectangle([s(x - 50), s(y - 30), s(x + 50), s(y + 30)], fill=hexc('#e84d3d', a))

def sc_rumor(img, d, t, D):
    bg(d, '#3d1020'); header(d, hexc('#ffb3c6'))
    k1 = ease((t - 0.2) / 0.4); k2 = ease((t - 0.8) / 0.4); k3 = ease((t - 1.4) / 0.4)
    if k1 > 0:
        ang = 0.25 * math.sin(t * 3)
        plane(d, 230, 520 + 60 * ease((t - 0.2) / 3), '#ffffff', int(255 * k1))
    if k2 > 0:
        bulb(d, 540, 560, int(t * 4) % 3 != 0, int(255 * k2))
    if k3 > 0:
        for j, (cx, cy) in enumerate([(790, 650), (900, 650), (845, 510)]):
            can(d, cx, cy, int(255 * k3))
    text_block(img, ["La rumeur : avions en panne, électricité coupée, banques vides…",
                     ("Certains ont même fait des stocks de conserves.", 1.8)], t, 1040, '#ffffff', size=64)

random.seed(48)
SPARKS = [(random.uniform(150, 930), random.uniform(420, 640), random.uniform(0, 6.3), random.choice(['#ffe066', '#ff6fb5', '#7ff0e0', '#ffffff'])) for _ in range(6)]
def sc_boom(img, d, t, D):
    bg(d, '#05051a'); stars(d, t); header(d, hexc('#9a9aa8'))
    n = max(0, 3 - int(t / 0.5))
    if t < 1.5:
        ctext(d, str(n) if n > 0 else "0", 470, 260, '#ffffff', FBK, 1.0)
    else:
        tt = t - 1.5
        for (x, y, ph, col) in SPARKS:
            r = 160 * ease(tt / 0.9)
            a = int(255 * max(0, 1 - tt / 2.6))
            for k in range(12):
                ang = ph + k * math.pi / 6
                line(d, [(x + r * 0.6 * math.cos(ang), y + r * 0.6 * math.sin(ang)),
                         (x + r * math.cos(ang), y + r * math.sin(ang))], hexc(col, a), 8)
        monitor(d, 540, 780, "2000", txt_col='#5cff8a', scale=0.55, a=int(255 * ease(tt / 0.4)))
    text_block(img, [("31 décembre 1999, minuit…", 0.1), ("…et presque rien. Quelques petits bugs.", 2.0)],
               t, 1120, '#ffffff', size=70)

def tape(d, cx, cy, a=255):
    d.rounded_rectangle([s(cx - 170), s(cy - 100), s(cx + 170), s(cy + 100)], radius=s(18), fill=hexc('#2b2b33', a))
    d.rounded_rectangle([s(cx - 120), s(cy - 60), s(cx + 120), s(cy + 10)], radius=s(10), fill=hexc('#f3e6d3', a))
    for ox in (-70, 70):
        circle(d, cx + ox, cy + 50, 28, fill=hexc('#f3e6d3', a))

def sc_video(img, d, t, D):
    bg(d, '#f3e6d3'); header(d, hexc('#8a5a3c'))
    tape(d, 330, 560)
    k = ease((t - 1.2) / 0.4)
    if k > 0:
        d.rounded_rectangle([s(560), s(400), s(940), s(760)], radius=s(20), fill=hexc('#ffffff', int(255 * k)), outline=hexc('#8a5a3c', int(255 * k)), width=s(6))
        ctext_x = 750
        for i, (l, sz, col) in enumerate([("RETARD", 50, '#8a5a3c'), ("100 ANS", 84, '#e84d3d'), ("à payer", 42, '#8a5a3c')]):
            f = font(FBK if i == 1 else FB, sz); tw = f.getlength(l) / S
            d.text((s(ctext_x - tw / 2), s(440 + i * 100)), l, font=f, fill=hexc(col, int(255 * k)))
    text_block(img, ["Le plus célèbre : un vidéoclub qui réclame à un client un siècle de retard.",
                     ("Pour une cassette. Il fallait vraiment rembobiner.", 2.0)], t, 1030, '#2b1a10', size=62)

def sc_fix(img, d, t, D):
    bg(d, '#0c2b4a'); header(d, hexc('#9fc2ff'))
    for i in range(3):
        x = 230 + i * 310
        monitor(d, x, 560, "00" if t < 1.0 + i * 0.4 else "2000", txt_col='#5cff8a', scale=0.42, txt_size=56)
    k = ease((t - 2.0) / 0.4)
    ctext(d, "≈ 300 MILLIARDS $", 790, 64, '#ffe066', FBK, k)
    text_block(img, ["Ce n'était pas de la chance : pendant des années, des informaticiens ont corrigé le code.",
                     ], t, 1060, '#ffffff', size=62)

def sc_verdict(img, d, t, D):
    bg(d, '#1e4020'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.5)
    monitor(d, 540, 600, "OK", txt_col='#5cff8a')
    circle(d, 790, 380, 70 * k, fill=hexc('#2ecc71'))
    if k > 0.6:
        line(d, [(758, 382), (782, 408), (826, 354)], '#ffffff', 14)
    text_block(img, ["Verdict : pas une fin du monde, ni un canular.",
                     ("Un vrai problème… réglé à temps.", 1.6)], t, 1080, '#ffffff', size=70)

def sc_2038(img, d, t, D):
    bg(d, '#2a1640'); header(d, hexc('#f0b8ff'))
    monitor(d, 540, 600, "2038" + ("_" if cursor_on(t) else " "), txt_col='#ffe066', txt_size=130)
    text_block(img, ["Prochain rendez-vous : 2038, quand un autre compteur arrive au bout.",
                     ("Même remède : corriger avant. On a le temps.", 1.9)], t, 1060, '#ffffff', size=62)

sc_title = scene_title(["BUG DE", "L'AN 2000"], "Mythe à démonter · n°48", color='#1f5c3a')
sc_end = scene_end("Bref : les ordinateurs ont survécu à l'an 2000. Votre déclaration d'impôts aussi.", color='#1f5c3a')

SCENES = [
    (sc_hook, 3.0), (sc_title, 2.4), (sc_memory, 4.6), (sc_count, 3.4), (sc_1900, 4.0),
    (sc_calc, 4.4), (sc_rumor, 4.6), (sc_boom, 4.4), (sc_video, 4.8), (sc_fix, 4.6),
    (sc_verdict, 4.2), (sc_2038, 4.6), (sc_end, 4.8),
]
