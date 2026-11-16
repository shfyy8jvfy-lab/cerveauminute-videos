"""Épisode 31 — Une civilisation extraterrestre hostile (l'hypothèse de la « forêt sombre »).
Sources :
- Universe Today, « Beyond Fermi's Paradox XVI: What is the Dark Forest Hypothesis? » : réponse au paradoxe de
  Fermi popularisée par le roman de Liu Cixin « La Forêt sombre » (2008) ; chaque civilisation se cache et élimine
  les autres par précaution, faute de pouvoir connaître leurs intentions.
- Big Think, « The Dark Forest theory: a terrifying explanation of why we haven't heard from aliens yet » ;
  Yu, « The Dark Forest Rule: One Solution to the Fermi Paradox », JBIS 68 (2015).
- Paradoxe de Fermi : question d'Enrico Fermi en 1950 (« Où sont-ils tous ? »).
- National Geographic / Universe Today, message d'Arecibo : envoyé le 16 novembre 1974 depuis le radiotélescope
  d'Arecibo (Porto Rico) vers l'amas d'étoiles M13, à environ 25 000 années-lumière ; arrivée dans ~25 000 ans.
  52 ans / 25 000 ≈ 0,2 % du trajet.
- Consensus : aucune trace confirmée de vie extraterrestre ; la forêt sombre est une hypothèse spéculative,
  sans données pour la tester.
"""
from engine import *

EPISODE = 31
BOOM_SCENE = 7
LEGENDE = """Épisode 31 : la forêt sombre, ou pourquoi l'univers se tait 🌲👽

Si l'univers est si grand, pourquoi personne ne nous parle ? Une réponse inquiétante, tirée d'un roman de science-fiction : tout le monde se cache, et on tire sur ce qui fait du bruit. Or il y a 52 ans jour pour jour (16 novembre 1974), on a envoyé un message radio vers l'amas M13… à 25 000 années-lumière. Il n'a fait que 0,2 % du trajet (source : National Geographic).

On va tous disparaître… mais pas aujourd'hui.

#findumonde #extraterrestres #espace #paradoxedefermi #astronomie #science #vulgarisation #apocalypse"""

random.seed(31)
SKY = [(random.uniform(80, 1000), random.uniform(300, 900), random.uniform(3, 7)) for _ in range(60)]
LIGHTS = [(200, 760), (420, 820), (640, 740), (880, 800), (320, 660), (780, 660)]

def tri(d, x, ybase, w, h, col):
    d.polygon([(s(x - w / 2), s(ybase)), (s(x + w / 2), s(ybase)), (s(x), s(ybase - h))], fill=col)

def forest(d, col='#0b1f14', base=950):
    for i, (x, h) in enumerate([(60, 420), (180, 520), (300, 380), (430, 560), (560, 440), (690, 540), (820, 400), (950, 500), (1060, 440)]):
        tri(d, x, base, 200, h, hexc(col))
        tri(d, x, base - h * 0.35, 160, h * 0.7, hexc(col))

# ---------- fil rouge : la petite Terre bleue qui "fait du bruit" ----------
def earth(d, cx, cy, r, waves=0.0, t=0.0, wcol='#7ee8fa'):
    if waves > 0:
        for i in range(4):
            p = (t * 0.6 + i / 4) % 1
            circle(d, cx, cy, r + p * 150 * waves, outline=hexc(wcol, int(220 * (1 - p))), width=6)
    circle(d, cx, cy, r, fill=hexc('#2f80ed'))
    for (dx, dy, rr) in [(-0.35, -0.2, 0.32), (0.3, 0.25, 0.28), (0.1, -0.45, 0.18)]:
        circle(d, cx + dx * r, cy + dy * r, rr * r, fill=hexc('#3fbf6f'))

def sc_hook(img, d, t, D):
    bg(d, '#0a0f24'); header(d, hexc('#9fb4ff'))
    stars(d, t)
    earth(d, 540, 640, 120 + 6 * math.sin(t * 2))
    text_block(img, ["Et si l'univers était silencieux… parce que tout le monde s'y cache ?"], t, 1090, '#ffffff', size=76)

def sc_fermi(img, d, t, D):
    bg(d, '#1c2a5a'); header(d, hexc('#c5d0ff'))
    k = ease((t - 0.2) / 1.5)
    for i, (x, y, r) in enumerate(SKY):
        if i / len(SKY) < k:
            circle(d, x, y, r + 1.5 * math.sin(t * 3 + i), fill=hexc('#fff3bf'))
    k2 = ease((t - 1.6) / 0.4)
    ctext(d, "?", 480, 300, '#ffd43b', FBK, k2)
    text_block(img, ["1950 : le physicien Enrico Fermi se demande : avec autant d'étoiles…", ("…où sont les extraterrestres ?", 2.0)], t, 1060, '#ffffff', size=66)

def sc_roman(img, d, t, D):
    bg(d, '#14361f'); header(d, hexc('#b2f2bb'))
    k = ease((t - 0.2) / 0.8)
    d.rounded_rectangle([s(380), s(360 + 40 * (1 - k)), s(700), s(860)], radius=s(18), fill=hexc('#2b8a3e', int(255 * k)))
    d.rounded_rectangle([s(380), s(360 + 40 * (1 - k)), s(420), s(860)], radius=s(10), fill=hexc('#1b5e2a', int(255 * k)))
    for j, (x, h) in enumerate([(480, 180), (560, 240), (640, 170)]):
        tri(d, x, 760, 90, h, hexc('#0b1f14', int(255 * k)))
    text_block(img, ["Une réponse inquiétante vient d'un roman de science-fiction chinois de 2008 :", ("« la forêt sombre ».", 2.2)], t, 1040, '#ffffff', size=66)

def sc_foret(img, d, t, D):
    bg(d, '#05140c'); header(d, hexc('#8ce99a'))
    stars(d, t)
    forest(d)
    for i, (x, y) in enumerate(LIGHTS):
        a = 0.5 + 0.5 * math.sin(t * 2.5 + i * 1.3)
        circle(d, x, y, 10 + 4 * a, fill=hexc('#ffe066', int(80 + 170 * a)))
    text_block(img, ["L'idée : l'univers est une forêt, la nuit. Chaque civilisation s'y cache, en silence."], t, 1060, '#ffffff', size=66)

def sc_tirer(img, d, t, D):
    bg(d, '#2a0f12'); header(d, hexc('#ffc9c9'))
    forest(d, '#160608')
    k = ease((t - 1.6) / 0.3)
    for i, (x, y) in enumerate(LIGHTS):
        on = i != 2 or k < 0.5
        if on:
            circle(d, x, y, 12, fill=hexc('#ffe066', 140))
    if k > 0:
        circle(d, 640, 740, 20 + 80 * k, outline=hexc('#ff6b6b', int(255 * (1 - k))), width=10)
    text_block(img, ["Personne ne sait si l'autre est gentil. Alors, au moindre bruit…", ("…on tire en premier.", 2.0)], t, 1060, '#ffffff', size=68)

def sc_arecibo(img, d, t, D):
    bg(d, '#103a4a'); header(d, hexc('#a5f3fc'))
    earth(d, 300, 640, 100, waves=1.0, t=t)
    k = ease((t - 0.4) / 0.5)
    ctext(d, "16 NOV. 1974", 330, 64, '#ffffff', FB, k)
    for i in range(7):
        circle(d, 860 + 25 * math.cos(i), 640 + 25 * math.sin(i * 1.7), 6, fill=hexc('#fff3bf'))
    f = font(FM, 44); lab = "amas M13"
    d.text((s(860) - f.getlength(lab) / 2, s(700)), lab, font=f, fill=hexc('#a5f3fc', int(255 * ease((t - 1.2) / 0.4))))
    text_block(img, ["Et nous ? Il y a 52 ans jour pour jour, on a envoyé un message radio vers un amas d'étoiles.", ("Exprès.", 2.6)], t, 1030, '#ffffff', size=62)

def sc_boom(img, d, t, D):
    bg(d, '#3d0c0c'); header(d, hexc('#ffa8a8'))
    stars(d, t, col='#ffc9c9')
    k = ease((t - 0.3) / 1.2)
    earth(d, 260, 660, 100, waves=1.0, t=t, wcol='#ffd8a8')
    circle(d, 860, 420, 16 + 14 * k, fill=hexc('#ff6b6b'))
    k2 = ease((t - 1.6) / 1.0)
    if k2 > 0:
        x = 860 + (260 - 860) * k2; y = 420 + (660 - 420) * k2
        line(d, [(860, 420), (x, y)], hexc('#ff8787'), 12)
    k3 = ease((t - 2.6) / 0.5)
    if k3 > 0:
        circle(d, 260, 660, 100 + 160 * k3, fill=hexc('#ffffff', int(230 * (1 - k3 * 0.6))))
    text_block(img, ["Si quelqu'un d'hostile l'entend… la Terre devient une cible."], t, 1080, '#ffffff', size=72)

def sc_delai(img, d, t, D):
    bg(d, '#1e3a2f'); header(d, hexc('#c3fae8'))
    d.rounded_rectangle([s(140), s(600), s(940), s(660)], radius=s(30), fill=hexc('#0b2a20'))
    k = ease((t - 0.4) / 1.0)
    d.rounded_rectangle([s(140), s(600), s(140 + 30 * k + 1), s(660)], radius=s(30), fill=hexc('#63e6be'))
    earth(d, 140, 630, 50)
    for i in range(5):
        circle(d, 940 + 20 * math.cos(i * 1.3), 630 + 20 * math.sin(i * 2.1), 6, fill=hexc('#fff3bf'))
    ctext(d, "0,2 %", 440, 110, '#ffffff', FBK, k)
    ctext(d, "25 000 années-lumière", 760, 46, '#c3fae8', FM, ease((t - 0.9) / 0.4))
    text_block(img, ["Bonne nouvelle : cet amas est à 25 000 années-lumière.", ("Le message n'a fait que 0,2 % du trajet.", 2.0)], t, 1040, '#ffffff', size=66)

def sc_joke(img, d, t, D):
    bg(d, '#fff0f6'); header(d, hexc('#a61e4d'))
    d.rounded_rectangle([s(380), s(380), s(700), s(900)], radius=s(30), fill=hexc('#343a40'))
    pulse = 1 + 0.08 * math.sin(t * 12)
    circle(d, 540, 520, 70 * pulse, fill=hexc('#868e96'))
    circle(d, 540, 520, 30, fill=hexc('#212529'))
    circle(d, 540, 740, 110 * pulse, fill=hexc('#868e96'))
    circle(d, 540, 740, 45, fill=hexc('#212529'))
    for i in range(3):
        p = (t * 0.8 + i / 3) % 1
        for side in (-1, 1):
            x = 540 + side * (220 + 120 * p)
            line(d, [(x, 600 - 60 * p), (x + side * 20, 640), (x, 680 + 60 * p)], hexc('#e64980', int(255 * (1 - p))), 8)
    text_block(img, ["C'est comme mettre la musique à fond dans un immeuble…", ("…en espérant que les voisins soient sympas.", 2.0)], t, 1030, '#3b0a1e', size=64)

def sc_science(img, d, t, D):
    bg(d, '#1f3d1a'); header(d, hexc('#c0eb75'))
    k = ease((t - 0.3) / 0.5)
    ctext(d, "SIGNAUX EXTRATERRESTRES", 380, 50, '#c0eb75', FB, k)
    ctext(d, "CONFIRMÉS", 440, 50, '#c0eb75', FB, k)
    ctext(d, "0", 520, 220, '#ffffff', FBK, k)
    ctext(d, "une hypothèse, pas une preuve", 820, 48, '#c0eb75', FM, ease((t - 0.9) / 0.4))
    text_block(img, [("Ce que disent les scientifiques : aucune trace de vie ailleurs pour l'instant. La forêt sombre reste une idée… impossible à vérifier.", 0.8)], t, 1010, '#ffffff', size=58)

sc_title = scene_title(["FORÊT", "SOMBRE"], "Scénario d'extinction n°31", color='#1b5e20')
sc_end = scene_end("Bref : aucun chasseur à l'horizon. Le fisc, lui, vous a déjà repéré.", color='#1b5e20')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_fermi, 4.4), (sc_roman, 4.4), (sc_foret, 4.6),
    (sc_tirer, 4.4), (sc_arecibo, 4.6), (sc_boom, 4.4), (sc_delai, 4.6), (sc_joke, 4.6),
    (sc_science, 5.0), (sc_end, 4.6),
]
