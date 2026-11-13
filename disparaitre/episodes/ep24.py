"""Épisode 24 — Mythe : la fin du monde maya de 2012.
Sources :
- LiveScience, « 5 Mayan Apocalypse Myths Debunked » et « Why the World Won't End on Dec. 21, 2012 » ;
  The Week / ABC7, « NASA vs. doomsday theorists » ; NASA (science.gsfc.nasa.gov, Sun-Earth Day 2012, page hoax) :
  le 21 décembre 2012 marquait la fin du 13e b'ak'tun du « compte long » (13.0.0.0.0), un cycle d'environ
  5 125 ans ; les Mayas n'ont jamais annoncé de fin du monde ; la NASA a répété qu'aucune menace n'existait.
- AAAS « Myths: Mayan Long Count calendar » ; IBTimes : les inscriptions qui citent la date (Tortuguero, La Corona)
  ne parlent pas d'apocalypse ; les Mayas d'aujourd'hui n'y voyaient pas de fin du monde.
- Saturno et al., Science (mai 2012) ; ScienceDaily, EurekAlert, ABC News : peintures de Xultún (Guatemala),
  plus ancien calendrier maya connu, avec des tables qui couvrent environ 7 000 ans.
- Bugarach (Aude) : présenté comme refuge « épargné » ; la préfecture a fermé l'accès au pic et au village autour
  du 21 décembre 2012 (Slate.fr, VOA, Fox News, Bangkok Post).
- Un b'ak'tun = 144 000 jours ≈ 394 ans : le 14e b'ak'tun se termine en 2407.
"""
from engine import *

EPISODE = 24
BOOM_SCENE = 8
LEGENDE = """Épisode 24 : le mythe de la fin du monde maya de 2012 🗿📅

Le 21 décembre 2012, le « compte long » maya passait simplement à 13.0.0.0.0 : la fin d'un cycle d'environ 5 125 ans, comme un compteur kilométrique qui change de chiffre. Les Mayas n'ont jamais annoncé d'apocalypse, et leurs propres calculs, peints sur les murs de Xultún, vont des milliers d'années plus loin (Science, 2012). Il ne s'est rien passé.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #maya #2012 #apocalypse #mythe #histoire #science #vulgarisation"""

# ---------- fil rouge : le compteur du compte long ----------
def counter(d, t, digits, y=600, col='#f4a261', box='#264653', alpha=255, roll=None, sz=96):
    """5 cases : b'ak'tun . k'atun . tun . winal . k'in. roll = index de la case qui défile."""
    n = len(digits); w, gap = 170, 22
    x0 = 540 - (n * w + (n - 1) * gap) / 2
    f = font(FBK, sz)
    for i, v in enumerate(digits):
        x = x0 + i * (w + gap)
        d.rounded_rectangle([s(x), s(y - 110), s(x + w), s(y + 110)], radius=s(26), fill=hexc(box, alpha),
                            outline=hexc(col, alpha), width=s(6))
        txt = str(v)
        dy = 0
        if roll is not None and i == roll:
            dy = 18 * math.sin(t * 12)
        d.text((s(x + w / 2), s(y + dy)), txt, font=f, fill=hexc(col, alpha), anchor='mm')
        if i < n - 1:
            circle(d, x + w + gap / 2, y + 70, 7, fill=hexc(col, alpha))

def label(d, txt, x, y, col, size=40):
    d.text((s(x), s(y)), txt, font=font(FB, size), fill=hexc(col), anchor='mm')

def calendar_page(d, x, y, sc, top, bottom, col='#ffffff', red='#e63946', a=255):
    d.rounded_rectangle([s(x - 160 * sc), s(y - 180 * sc), s(x + 160 * sc), s(y + 180 * sc)], radius=s(30 * sc), fill=hexc(col, a))
    d.rounded_rectangle([s(x - 160 * sc), s(y - 180 * sc), s(x + 160 * sc), s(y - 90 * sc)], radius=s(30 * sc), fill=hexc(red, a))
    d.rectangle([s(x - 160 * sc), s(y - 120 * sc), s(x + 160 * sc), s(y - 90 * sc)], fill=hexc(red, a))
    d.text((s(x), s(y - 135 * sc)), top, font=font(FB, int(48 * sc)), fill=hexc('#ffffff', a), anchor='mm')
    d.text((s(x), s(y + 40 * sc)), bottom, font=font(FBK, int(130 * sc)), fill=hexc('#1d3557', a), anchor='mm')

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#1d3557'); header(d, hexc('#a8dadc'))
    sh = 6 * math.sin(t * 20) if t > 1.2 else 0
    calendar_page(d, 540 + sh, 620, 1.2, "DÉC. 2012", "21")
    k = ease((t - 1.2) / 0.3)
    if k > 0:
        line(d, [(470, 470), (520, 560), (490, 640), (560, 760)], hexc('#000000', int(220 * k)), 8)
    text_block(img, ["Et si les Mayas avaient prévu la fin du monde… pour le 21 décembre 2012 ?"], t, 1080, '#ffffff', size=72)

def sc_counter(img, d, t, D):
    bg(d, '#2a9d8f'); header(d, hexc('#e9f5db'))
    k = int(t * 6) % 20
    counter(d, t, [12, 19, 19, 17, k], roll=4, box='#264653')
    label(d, "LE « COMPTE LONG »", 540, 420, '#ffffff', 44)
    text_block(img, ["Les Mayas comptaient les jours avec un compteur géant : le « compte long »."], t, 1060, '#ffffff', size=68)

def sc_cycle(img, d, t, D):
    bg(d, '#6d597a'); header(d, hexc('#ffd6ff'))
    k = ease((t - 1.0) / 0.5)
    digs = [12, 19, 19, 17, 19] if k < 0.5 else [13, 0, 0, 0, 0]
    counter(d, t, digs, box='#355070', col='#ffd166')
    if k > 0.5:
        label(d, "21 / 12 / 2012", 540, 820, '#ffd166', 54)
    text_block(img, ["Le 21 décembre 2012, il affichait 13.0.0.0.0 : la fin d'un cycle de plus de 5 000 ans."], t, 1060, '#ffffff', size=66)

def sc_panic(img, d, t, D):
    bg(d, '#9d0208'); header(d, hexc('#ffccd5'))
    counter(d, t, [13, 0, 0, 0, 0], box='#370617', col='#ffba08', alpha=170)
    for i, (x, y) in enumerate(((180, 380), (900, 420), (220, 860), (880, 840))):
        sc = 1 + 0.15 * math.sin(t * 5 + i)
        label(d, "!", x, y, '#ffba08', int(90 * sc))
    text_block(img, ["Des auteurs en concluent : fin du cycle = fin du monde.", ("Ajoutez Nibiru et des planètes alignées : panique.", 1.6)], t, 1060, '#ffffff', size=64)

def sc_car(img, d, t, D):
    bg(d, '#ffb703'); header(d, hexc('#5a3e00'))
    # tableau de bord : compteur kilométrique qui repasse à zéro
    d.rounded_rectangle([s(190), s(480), s(890), s(760)], radius=s(40), fill=hexc('#023047'))
    k = ease((t - 1.0) / 0.4)
    txt = "999 999" if k < 0.5 else "000 000"
    d.text((s(540), s(600)), txt, font=font(FBK, 120), fill=hexc('#ffffff'), anchor='mm')
    label(d, "km", 540, 710, '#8ecae6', 40)
    for i in range(3):
        x = 300 + ((t * 160 + i * 240) % 520)
        line(d, [(x, 860), (x + 90, 860)], '#023047', 12)
    text_block(img, ["Comme le compteur d'une vieille voiture qui repasse à zéro :", ("la voiture, elle, continue de rouler.", 1.5)], t, 1060, '#023047', size=66)

def sc_glyph(img, d, t, D):
    bg(d, '#606c38'); header(d, hexc('#fefae0'))
    # stèle de pierre avec des glyphes (formes simples)
    d.rounded_rectangle([s(370), s(340), s(710), s(940)], radius=s(50), fill=hexc('#dda15e'))
    for j in range(4):
        for i in range(2):
            x, y = 450 + i * 180, 420 + j * 130
            k = ease((t - 0.3 - (j * 2 + i) * 0.12) / 0.3)
            d.rounded_rectangle([s(x - 60), s(y - 45), s(x + 60), s(y + 45)], radius=s(18), outline=hexc('#5a3e1b', int(255 * k)), width=s(6))
            circle(d, x - 20 + 6 * math.sin(t * 2 + i + j), y, 12, fill=hexc('#5a3e1b', int(255 * k)))
    text_block(img, ["Mais les Mayas n'ont jamais prédit de fin du monde.", ("Les rares inscriptions qui citent 2012 n'en parlent pas.", 1.5)], t, 1060, '#ffffff', size=64)

def sc_xultun(img, d, t, D):
    bg(d, '#bc6c25'); header(d, hexc('#fefae0'))
    # mur peint avec des colonnes de chiffres (barres et points mayas)
    d.rounded_rectangle([s(160), s(360), s(920), s(920)], radius=s(30), fill=hexc('#fefae0'))
    for c in range(6):
        for r in range(4):
            k = ease((t - 0.3 - (c + r) * 0.08) / 0.3)
            x, y = 230 + c * 125, 430 + r * 125
            d.rounded_rectangle([s(x - 40), s(y + 10), s(x + 40), s(y + 24)], radius=s(6), fill=hexc('#9b2226', int(255 * k)))
            for p in range((c + r) % 4):
                circle(d, x - 30 + p * 20, y - 10, 7, fill=hexc('#9b2226', int(255 * k)))
    label(d, "+ 7 000 ANS", 540, 870, '#9b2226', 48)
    text_block(img, ["Mieux : au Guatemala, des calculs mayas peints sur un mur vont environ 7 000 ans plus loin."], t, 1060, '#ffffff', size=64)

def sc_boom(img, d, t, D):
    bg(d, '#000000'); header(d, hexc('#888888'))
    n = max(0, 3 - int(t / 0.6))
    if t < 1.8:
        ctext(d, str(n if n else 0), 520, 200, '#ffffff', FBK)
    else:
        counter(d, t, [13, 0, 0, 0, 1], box='#111111', col='#ffffff')
        k = ease((t - 2.0) / 0.4)
        label(d, "…", 540, 850, '#888888', 80)
    text_block(img, [("21 décembre 2012. 3, 2, 1…", 0.15), ("Il ne s'est rien passé. Le compteur a juste ajouté un jour.", 1.9)], t, 1060, '#ffffff', size=66)

def sc_bugarach(img, d, t, D):
    bg(d, '#457b9d'); header(d, hexc('#f1faee'))
    d.polygon([(s(220), s(900)), (s(540), s(420)), (s(860), s(900))], fill=hexc('#1d3557'))
    d.polygon([(s(470), s(525)), (s(540), s(420)), (s(610), s(525))], fill=hexc('#f1faee'))
    # barrière qui descend
    k = ease((t - 1.0) / 0.5)
    d.rounded_rectangle([s(260), s(870 - 20), s(260 + 560 * k), s(870 + 20)], radius=s(10), fill=hexc('#e63946'))
    for i in range(int(6 * k)):
        d.rectangle([s(290 + i * 90), s(852), s(330 + i * 90), s(888)], fill=hexc('#ffffff'))
    label(d, "BUGARACH", 540, 350, '#f1faee', 44)
    text_block(img, ["En France, le pic de Bugarach devait être « épargné ».", ("Résultat : les autorités ont fermé l'accès.", 1.5)], t, 1060, '#ffffff', size=64)

def sc_joke(img, d, t, D):
    bg(d, '#ffddd2'); header(d, hexc('#e76f51'))
    calendar_page(d, 540, 620, 1.1, "DÉCEMBRE", "31", red='#e76f51')
    k = ease((t - 1.6) / 0.5)
    if k > 0:
        d.rounded_rectangle([s(640), s(780), s(900), s(880)], radius=s(20), fill=hexc('#2a9d8f', int(255 * k)))
        label(d, "2,99 €", 770, 830, '#ffffff', 48)
    text_block(img, ["Leçon du jour : si votre calendrier s'arrête au 31 décembre, ce n'est pas l'apocalypse.", ("Rachetez-en un.", 1.8)], t, 1060, '#2b2d42', size=60)

def sc_science(img, d, t, D):
    bg(d, '#2d6a4f'); header(d, hexc('#b7e4c7'))
    k = ease((t - 0.6) / 0.5)
    ctext(d, "RISQUE EN 2012", 470, 60, '#b7e4c7', FB, k)
    ctext(d, "ZÉRO", 560, 180, '#ffffff', FBK, k)
    text_block(img, ["Ce que disaient les scientifiques, NASA en tête : aucune menace en 2012. Ni planète, ni astéroïde, ni rien."], t, 1060, '#ffffff', size=60)

def sc_next(img, d, t, D):
    bg(d, '#5a189a'); header(d, hexc('#e0aaff'))
    counter(d, t, [13, 0, 14, 1, (int(t * 6) % 20)], roll=4, box='#3c096c', col='#e0aaff')
    k = ease((t - 1.2) / 0.4)
    ctext(d, "PROCHAIN CHIFFRE ROND : 2407", 790, 44, '#ffd166', FB, k)
    text_block(img, ["Et le compteur tourne toujours. Le prochain grand cycle se termine en 2407.", ("On a le temps.", 1.8)], t, 1060, '#ffffff', size=64)

sc_title = scene_title(["MYTHE :", "MAYA 2012"], "Scénario d'extinction n°24", color='#bc4749')
sc_end = scene_end("Bref : le calendrier maya n'a pas arrêté le monde. Le calendrier des impôts, lui, ne s'arrête jamais.", color='#bc4749')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_counter, 4.0), (sc_cycle, 4.4), (sc_panic, 4.4),
    (sc_car, 4.2), (sc_glyph, 4.4), (sc_xultun, 4.4), (sc_boom, 4.6), (sc_bugarach, 4.2),
    (sc_joke, 4.4), (sc_science, 4.2), (sc_next, 4.4), (sc_end, 4.8),
]

# ---------- voix off (une entrée par scène, même ordre que SCENES) ----------
VOIX = [
    "Et si les Mayas avaient prévu la fin du monde… pour le vingt et un décembre deux mille douze ?",
    "Scénario d'extinction numéro vingt-quatre : le mythe maya de deux mille douze.",
    "Les Mayas comptaient les jours avec un compteur géant : le compte long.",
    "Le vingt et un décembre deux mille douze, il passait à treize, zéro, zéro, zéro, zéro : la fin d'un cycle de plus de cinq mille ans.",
    "Des auteurs en concluent : fin du cycle égale fin du monde. Ajoutez Nibiru et des planètes alignées : panique.",
    "Comme le compteur d'une vieille voiture qui repasse à zéro : la voiture, elle, continue de rouler.",
    "Mais les Mayas n'ont jamais prédit de fin du monde. Les rares inscriptions qui citent deux mille douze n'en parlent pas.",
    "Mieux : au Guatemala, des calculs mayas peints sur un mur vont environ sept mille ans plus loin.",
    "Vingt et un décembre deux mille douze. Trois, deux, un… Il ne s'est rien passé. Le compteur a juste ajouté un jour.",
    "En France, le pic de Bugarach devait être épargné. Résultat : les autorités ont fermé l'accès.",
    "Leçon du jour : si votre calendrier s'arrête au trente et un décembre, ce n'est pas l'apocalypse. Rachetez-en un.",
    "Ce que disaient les scientifiques, NASA en tête : aucune menace en deux mille douze. Ni planète, ni astéroïde, ni rien.",
    "Et le compteur tourne toujours. Le prochain grand cycle se termine en deux mille quatre cent sept. On a le temps.",
    "Bref : le calendrier maya n'a pas arrêté le monde. Le calendrier des impôts, lui, ne s'arrête jamais. Abonnez-vous. Tant qu'il y a un demain.",
]
