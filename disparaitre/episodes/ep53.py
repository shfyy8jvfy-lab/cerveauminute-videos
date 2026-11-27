"""Épisode 53 — Le flash d'un magnétar (SGR 1806-20, 27 décembre 2004).
Sources :
- NASA (Swift, fév. 2005) : flash du 27/12/2004 venu de SGR 1806-20, à environ 50 000 années-lumière ;
  un peu plus d'un dixième de seconde ; énergie totale supérieure à ce que le Soleil émet en 150 000 ans ;
  champ magnétique ~1 000 000 milliards de gauss (Terre : 0,5 gauss) ; « à moins de 10 années-lumière, il aurait
  sévèrement endommagé notre atmosphère » (B. Gaensler).
- Harvard-Smithsonian CfA (18/02/2005) : même à 50 000 années-lumière, le flash a perturbé l'ionosphère ;
  à moins de 10 années-lumière il détruirait une grande partie de la couche d'ozone, causant des extinctions ;
  « il n'y a aucun magnétar près de la Terre ».
- Space.com (18/02/2005) : « plus d'énergie en un dixième de seconde que le Soleil en 100 000 ans » (R. Fender) ;
  aucun magnétar connu à moins de ~4 000-5 000 années-lumière (Gaensler) ; effet sur Terre bien plus faible
  qu'une grosse éruption solaire (N. Gehrels) ; une vingtaine de km de diamètre.
- Scientific American (2024, « An Earth-Rocking Cosmic Explosion Turns 20 ») : ~20 km, plus massif que le Soleil ;
  champ jusqu'à un million de milliards de fois celui de la Terre ; cause probable : un « séisme d'étoile ».
Choix prudents : on garde le chiffre le plus bas (100 000 ans) ; on dit « des milliers d'années-lumière » pour
le plus proche connu ; « quelques dizaines » de magnétars connus.
"""
from engine import *

EPISODE = 53
BOOM_SCENE = 6
LEGENDE = """Épisode 53 : le flash du magnétar ⚡🧲

Le 27 décembre 2004, une étoile morte de 20 km, à 50 000 années-lumière, a lâché en un dixième de seconde plus d'énergie que le Soleil en 100 000 ans (NASA). Même de si loin, le flash a secoué le haut de notre atmosphère. À moins de 10 années-lumière, ce serait la fin de la couche d'ozone… mais aucun magnétar connu n'est aussi proche.

On va tous disparaître… mais pas aujourd'hui.

#findumonde #magnetar #astronomie #espace #etoile #science #vulgarisation #apocalypse"""

# ---------- fil rouge : le magnétar ----------
def magnetar(d, cx, cy, r, t, core='#e8f4ff', field='#7fd0ff', a=255, cracks=0.0, glow=0.0):
    # lignes de champ magnétique (boucles de chaque côté)
    for k in range(1, 4):
        w = r * (1.2 + 0.9 * k); h = r * (0.7 + 0.55 * k)
        pulse = 0.5 + 0.5 * math.sin(t * 3 - k)
        col = hexc(field, int(a * (0.35 + 0.4 * pulse)))
        d.arc([s(cx - w * 2 + r * 0.2), s(cy - h), s(cx + r * 0.2), s(cy + h)], 290, 430, fill=col, width=s(6))
        d.arc([s(cx - r * 0.2), s(cy - h), s(cx + w * 2 - r * 0.2), s(cy + h)], 110, 250, fill=col, width=s(6))
    if glow > 0:
        for g in range(5, 0, -1):
            circle(d, cx, cy, r * (1 + g * 0.35 * glow), fill=hexc('#ffffff', int(40 * glow)))
    circle(d, cx, cy, r, fill=hexc(core, a))
    circle(d, cx - r * 0.3, cy - r * 0.3, r * 0.25, fill=hexc('#ffffff', int(a * 0.6)))
    if cracks > 0:
        for i in range(4):
            ang = i * math.pi / 2 + 0.4
            pts = [(cx + r * 0.1 * math.cos(ang), cy + r * 0.1 * math.sin(ang))]
            for j in range(1, 4):
                rr = r * 0.95 * min(1, cracks) * j / 3
                pts.append((cx + rr * math.cos(ang + 0.25 * (-1) ** j), cy + rr * math.sin(ang + 0.25 * (-1) ** j)))
            line(d, pts, '#ff4d5a', max(3, r * 0.06))

def earth(d, cx, cy, r, a=255, ring=0.0):
    circle(d, cx, cy, r, fill=hexc('#2f7fd6', a))
    d.ellipse([s(cx - r * 0.6), s(cy - r * 0.5), s(cx - r * 0.05), s(cy + r * 0.1)], fill=hexc('#4cc27a', a))
    d.ellipse([s(cx + r * 0.1), s(cy - r * 0.1), s(cx + r * 0.6), s(cy + r * 0.55)], fill=hexc('#4cc27a', a))
    if ring > 0:
        circle(d, cx, cy, r * 1.18, outline=hexc('#ff9de2', int(255 * ring)), width=10)

# ---------- scènes ----------
def sc_hook(img, d, t, D):
    bg(d, '#0b0f24'); stars(d, t); header(d, hexc('#9fc2ff'))
    magnetar(d, 540, 640, 70 + 6 * math.sin(t * 4), t)
    text_block(img, ["Et si une étoile morte, grosse comme une ville, pouvait nous griller ?"], t, 1080, '#ffffff', size=76)

def sc_dying(img, d, t, D):
    bg(d, '#3a1020'); stars(d, t); header(d, hexc('#ffb3bd'))
    k = ease((t - 0.8) / 1.4)
    r = 280 * (1 - k) + 60 * k
    circle(d, 540, 640, r + 30 * (1 - k), fill=hexc('#ff6a3d', int(120 * (1 - k))))
    circle(d, 540, 640, r, fill=hexc('#ff8a4d') if k < 0.7 else hexc('#e8f4ff'))
    text_block(img, ["Quand une étoile géante meurt, son cœur s'effondre sur lui-même."], t, 1080, '#ffffff', size=72)

def sc_tiny(img, d, t, D):
    bg(d, '#0e3b3b'); header(d, hexc('#9fd3ff'))
    # balance : la petite boule pèse plus lourd que le Soleil
    tilt = 60 * ease((t - 0.6) / 0.8)
    line(d, [(540, 900), (540, 640)], '#cfe9ec', 14)
    lx, ly, rx, ry = 260, 640 + tilt, 820, 640 - tilt
    line(d, [(lx, ly), (rx, ry)], '#cfe9ec', 14)
    circle(d, lx, ly - 50, 45, fill=hexc('#e8f4ff'))
    circle(d, rx, ry - 130, 120, fill=hexc('#ffd84a'))
    f20 = font(FB, 40); d.text((s(lx - f20.getlength("20 km") / S / 2), s(ly + 30)), "20 km", font=f20, fill=hexc('#cfe9ec'))
    text_block(img, ["Il reste une boule d'une vingtaine de kilomètres…",
                     ("…plus lourde que tout le Soleil.", 1.4)], t, 1060, '#ffffff', size=68)

def sc_magnet(img, d, t, D):
    bg(d, '#1d1430'); header(d, hexc('#d2b8ff'))
    magnetar(d, 540, 640, 90, t, field='#ff8af0')
    k = ease((t - 0.3) / 0.4)
    ctext(d, "× 1 000 000 000 000 000", 340, 50, '#ff8af0', FBK, k)
    text_block(img, ["Certaines sont des aimants monstres : un million de milliards de fois plus fort que la Terre.",
                     ("Leur nom : magnétar.", 2.6)], t, 1010, '#ffffff', size=60)

def sc_crack(img, d, t, D):
    bg(d, '#2a1a0e'); stars(d, t); header(d, hexc('#ffd98a'))
    sh = 6 * math.sin(t * 45) if t > 1.0 else 0
    magnetar(d, 540 + sh, 640, 110, t, field='#ffd98a', cracks=ease((t - 0.8) / 1.2))
    text_block(img, ["Parfois, sa croûte craque.",
                     ("Un tremblement de terre… mais d'étoile.", 1.2)], t, 1080, '#ffffff', size=74)

def sc_boom(img, d, t, D):
    flash = max(0, 1 - t / 0.7)
    bg(d, '#ffffff' if flash > 0.6 else '#6b2a00'); header(d, hexc('#ffe0a8'))
    magnetar(d, 540, 640, 80, t, field='#ffe0a8', glow=max(0.25, flash))
    for i in range(12):
        a = i * math.pi / 6 + t * 0.5
        r0 = 140 + 200 * ease(t / 0.8)
        line(d, [(540 + r0 * math.cos(a), 640 + r0 * math.sin(a)), (540 + (r0 + 90) * math.cos(a), 640 + (r0 + 90) * math.sin(a))], '#ffe0a8', 12)
    text_block(img, [("27 décembre 2004 : FLASH !", 0.5),
                     ("En un dixième de seconde : plus d'énergie que le Soleil en 100 000 ans.", 1.2)], t, 1060, '#ffffff', size=64)

def sc_hit(img, d, t, D):
    bg(d, '#14304a'); stars(d, t); header(d, hexc('#9fc2ff'))
    magnetar(d, 150, 520, 30, t)
    k = ease((t - 0.3) / 1.4)
    x = 190 + (720 - 190) * k
    line(d, [(190, 520), (x, 520 + 150 * k)], '#fff1b8', 10)
    earth(d, 820, 690, 110, ring=ease((t - 1.6) / 0.4) * (0.6 + 0.4 * math.sin(t * 12)))
    text_block(img, ["Il venait de 50 000 années-lumière.",
                     ("Et pourtant, il a secoué le haut de notre atmosphère.", 1.4)], t, 1060, '#ffffff', size=68)

def sc_joke(img, d, t, D):
    bg(d, '#f6ead8'); header(d, hexc('#8a5a3c'))
    # la bûche de Noël et un flash d'appareil photo
    d.rounded_rectangle([s(240), s(700), s(840), s(860)], radius=s(80), fill=hexc('#7a4a2a'))
    circle(d, 840, 780, 80, fill=hexc('#a8754f'))
    circle(d, 840, 780, 40, outline=hexc('#7a4a2a'), width=8)
    for x in (360, 520, 680):
        line(d, [(x, 700), (x + 15, 660)], '#ffffff', 14)
    d.rounded_rectangle([s(400), s(380), s(680), s(560)], radius=s(24), fill=hexc('#2b2b38'))
    circle(d, 540, 470, 55, fill=hexc('#6b6b78'))
    circle(d, 540, 470, 30, fill=hexc('#111118'))
    fl = 1 if 1.6 < t < 1.9 else 0
    if fl:
        circle(d, 640, 410, 60, fill=hexc('#fff6c8'))
    else:
        d.rectangle([s(615), s(395), s(665), s(425)], fill=hexc('#e8e8f0'))
    text_block(img, ["Pendant ce temps, sur Terre, le flash le plus aveuglant…",
                     ("…c'était tonton qui photographiait la bûche.", 1.6)], t, 1010, '#2b1a10', size=66)

def sc_close(img, d, t, D):
    bg(d, '#4a0d2e'); stars(d, t); header(d, hexc('#ffb3bd'))
    k = ease((t - 0.3) / 1.0)
    magnetar(d, 300, 620, 70, t, field='#ffb3bd')
    earth(d, 790 - 60 * k, 640, 110)
    if t > 1.6:
        kk = ease((t - 1.6) / 0.6)
        circle(d, 730, 640, 140, outline=hexc('#ff4d5a', int(255 * kk)), width=10)
        line(d, [(640, 550), (820, 730)], '#ff4d5a', 12)
    ctext(d, "< 10 années-lumière", 360, 52, '#ffb3bd', FBK, k)
    text_block(img, ["Si ça arrivait tout près de nous, la couche d'ozone serait en grande partie détruite.",
                     ("Là, oui : extinctions en série.", 2.4)], t, 1020, '#ffffff', size=62)

def sc_science(img, d, t, D):
    bg(d, '#12301f'); header(d, hexc('#a8f0c0'))
    k = ease((t - 0.2) / 0.5)
    ctext(d, "0", 390, 260, '#a8f0c0', FBK, k)
    ctext(d, "magnétar connu à moins de", 700, 44, '#a8f0c0', FM, k)
    ctext(d, "10 années-lumière", 760, 44, '#a8f0c0', FM, k)
    text_block(img, [("Bonne nouvelle : le plus proche connu est à des milliers d'années-lumière.", 1.0)], t, 1040, '#ffffff', size=64)

def sc_rare(img, d, t, D):
    bg(d, '#22264d'); stars(d, t); header(d, hexc('#c8ccff'))
    random.seed(53)
    pts = [(random.uniform(120, 960), random.uniform(380, 900)) for _ in range(28)]
    for i, (x, y) in enumerate(pts):
        if t > 0.3 + i * 0.06:
            circle(d, x, y, 10 + 3 * math.sin(t * 5 + i), fill=hexc('#7fd0ff'))
    text_block(img, ["On n'en connaît que quelques dizaines dans toute notre galaxie.",
                     ("Et un flash pareil, c'est rarissime.", 1.6)], t, 1040, '#ffffff', size=64)

sc_title = scene_title(["LE FLASH", "MAGNÉTAR"], "Scénario d'extinction n°53", color='#3d1a7a')
sc_end = scene_end("Bref : aucun magnétar ne vous grillera ce soir. Vos impôts, eux, arrivent quand même.", color='#3d1a7a')

SCENES = [
    (sc_hook, 3.4), (sc_title, 2.4), (sc_dying, 4.0), (sc_tiny, 4.2), (sc_magnet, 4.8),
    (sc_crack, 3.8), (sc_boom, 4.2), (sc_hit, 4.6), (sc_joke, 4.6),
    (sc_close, 5.0), (sc_science, 4.6), (sc_rare, 4.0), (sc_end, 4.8),
]
