"""Bibliothèque de dessins à la craie pour Cerveau Minute.

Chaque dessin est une fonction qui renvoie une liste d'éléments, dans un repère centré
sur (0, 0), en pixels, y vers le bas, boîte utile d'environ 800 x 600 (x de -400 à 400, y de -300 à 300).
Éléments :
  {"pts": [(x, y), ...], "c": "blanc", "w": 10}            trait (polyligne) tracé progressivement
  {"text": "9,99 €", "x": 0, "y": 0, "size": 120, "c": "jaune"}   texte écrit à la craie (révélé de gauche à droite)
Couleurs : blanc, jaune, rose, bleu, orange, vert, rouge, gris.

Dans un script : "dessin": "popcorn"  ou  "dessin": {"nom": "etiquette", "texte": "9,99 €"}.
Lister les dessins : python3 outil/dessins.py
"""
import math

# ---------- primitives ----------

def L(pts, c="blanc", w=10):
    return {"pts": [tuple(map(float, p)) for p in pts], "c": c, "w": w}

def line(x0, y0, x1, y1, c="blanc", w=10):
    return L([(x0, y0), (x1, y1)], c, w)

def ellipse(cx, cy, rx, ry, c="blanc", w=10, a0=-100, a1=268, n=48):
    """Ellipse tracée comme à la main : légèrement plus d'un tour (dépassement)."""
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return L(pts, c, w)

def circle(cx, cy, r, c="blanc", w=10, **kw):
    return ellipse(cx, cy, r, r, c, w, **kw)

def arc(cx, cy, rx, ry, a0, a1, c="blanc", w=10, n=30):
    return ellipse(cx, cy, rx, ry, c, w, a0, a1, n)

def rect(x0, y0, x1, y1, c="blanc", w=10):
    return L([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0 - 4)], c, w)

def poly(pts, c="blanc", w=10, closed=True):
    pts = list(pts)
    if closed:
        pts = pts + [pts[0]]
    return L(pts, c, w)

def text(s, x, y, size=110, c="jaune"):
    return {"text": s, "x": float(x), "y": float(y), "size": size, "c": c}

def hatch(polygon, c="blanc", w=5, step=22, angle=-35):
    """Hachures à la craie à l'intérieur d'un polygone (remplissage)."""
    a = math.radians(angle); ca, sa = math.cos(a), math.sin(a)
    rot = [(x * ca + y * sa, -x * sa + y * ca) for x, y in polygon]
    ys = [p[1] for p in rot]
    out, flip = [], False
    yy = min(ys) + step / 2
    while yy < max(ys):
        xs = []
        for (x0, y0), (x1, y1) in zip(rot, rot[1:] + rot[:1]):
            if (y0 <= yy < y1) or (y1 <= yy < y0):
                xs.append(x0 + (yy - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            p0, p1 = (xs[i] + 3, yy), (xs[i + 1] - 3, yy)
            if flip:
                p0, p1 = p1, p0
            seg = [(px * ca - py * sa, px * sa + py * ca) for px, py in (p0, p1)]
            out.append(L(seg, c, w))
        flip = not flip
        yy += step
    return out

def circle_pts(cx, cy, r, n=24):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]

def shift(items, dx=0, dy=0, s=1.0):
    out = []
    for it in items:
        it = dict(it)
        if "pts" in it:
            it["pts"] = [(x * s + dx, y * s + dy) for x, y in it["pts"]]
            it["w"] = max(4, it["w"] * (s if s < 1 else 1))
        else:
            it["x"] = it["x"] * s + dx; it["y"] = it["y"] * s + dy; it["size"] = int(it["size"] * s)
        out.append(it)
    return out

def stick(x, y, s=1.0, c="blanc"):
    """Bonhomme bâton (pas de visage réaliste)."""
    r = 26 * s
    return [circle(x, y - 120 * s, r, c, 8),
            line(x, y - 94 * s, x, y - 20 * s, c, 8),
            L([(x - 40 * s, y - 70 * s), (x, y - 80 * s), (x + 40 * s, y - 70 * s)], c, 8),
            L([(x - 32 * s, y + 30 * s), (x, y - 20 * s), (x + 32 * s, y + 30 * s)], c, 8)]

# ---------- dessins génériques ----------

def d_question(**k):
    return [circle(0, 0, 230, "jaune", 12),
            L([(-70, -60), (-60, -110), (-10, -135), (50, -120), (75, -75), (60, -30), (10, 0), (0, 40), (0, 70)], "jaune", 16),
            circle(0, 130, 10, "jaune", 16)]

def d_ampoule(**k):
    out = [L([(-60, 90), (-75, 30), (-120, -20), (-130, -90), (-100, -160), (-40, -200), (40, -200), (100, -160), (130, -90),
              (120, -20), (75, 30), (60, 90)], "jaune", 11),
           line(-60, 90, 60, 90), line(-55, 120, 55, 120), line(-45, 150, 45, 150), line(-25, 180, 25, 180),
           L([(-30, 85), (-30, -40), (-10, -70), (10, -40), (30, -70), (30, 85)], "orange", 7)]
    for a in (-160, -125, -90, -55, -20):
        r = math.radians(a)
        out.append(line(220 * math.cos(r), -60 + 220 * math.sin(r), 280 * math.cos(r), -60 + 280 * math.sin(r), "jaune", 9))
    return out

def d_cerveau(**k):
    out = [L([(-40, 150), (-120, 140), (-200, 90), (-230, 10), (-210, -70), (-150, -130), (-70, -160), (10, -165), (90, -150),
              (170, -110), (220, -40), (225, 40), (190, 100), (120, 130), (40, 135)], "rose", 12),
           L([(40, 135), (55, 200), (90, 240)], "rose", 12),
           L([(0, -160), (-20, -100), (10, -50), (-15, 0), (10, 60), (-5, 130)], "rose", 8),
           L([(-160, -80), (-110, -60), (-120, -10), (-70, 10)], "rose", 7),
           L([(-190, 40), (-140, 30), (-110, 80), (-60, 70)], "rose", 7),
           L([(80, -110), (110, -60), (170, -60)], "rose", 7),
           L([(60, -10), (110, 0), (130, 50), (180, 40)], "rose", 7)]
    return out

def d_oeil(**k):
    return [L([(-280, 0), (-180, -110), (0, -150), (180, -110), (280, 0)], "blanc", 11),
            L([(-280, 0), (-180, 110), (0, 150), (180, 110), (280, 0)], "blanc", 11),
            circle(0, 0, 95, "bleu", 11), *hatch(circle_pts(0, 0, 45), "bleu", 6, 16),
            circle(35, -35, 12, "blanc", 8)]

def d_loupe(**k):
    return [circle(-50, -50, 170, "blanc", 13), arc(-50, -50, 120, 120, 200, 260, "blanc", 7),
            L([(70, 70), (230, 230)], "orange", 26)]

def d_coeur(**k):
    pts = []
    for i in range(61):
        t = math.pi * 2 * i / 60 - math.pi
        pts.append((14 * 16 * math.sin(t) ** 3 / 1.0 * 0.9, -14 * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) * 0.9 + 20))
    return [L(pts, "rose", 13), *hatch(pts[::2], "rose", 5, 24)]

def d_balance(**k):
    out = [line(0, -220, 0, 200, "blanc", 11), line(-120, 200, 120, 200, "blanc", 11), line(-280, -150, 280, -190, "blanc", 11),
           circle(0, -225, 14, "blanc", 9),
           line(-280, -150, -330, 0, "blanc", 6), line(-280, -150, -230, 0, "blanc", 6), arc(-280, 0, 70, 35, 0, 180, "jaune", 9),
           line(280, -190, 230, -40, "blanc", 6), line(280, -190, 330, -40, "blanc", 6), arc(280, -40, 70, 35, 0, 180, "jaune", 9)]
    return out

def d_horloge(**k):
    out = [circle(0, 0, 230, "blanc", 12)]
    for i in range(12):
        a = 2 * math.pi * i / 12
        out.append(line(195 * math.cos(a), 195 * math.sin(a), 215 * math.cos(a), 215 * math.sin(a), "blanc", 8))
    out += [line(0, 0, 0, -150, "jaune", 12), line(0, 0, 110, 40, "jaune", 12)]
    return out

def d_sablier(**k):
    return [line(-160, -230, 160, -230, "orange", 14), line(-160, 230, 160, 230, "orange", 14),
            L([(-130, -230), (-120, -120), (-20, 0), (-120, 120), (-130, 230)], "blanc", 10),
            L([(130, -230), (120, -120), (20, 0), (120, 120), (130, 230)], "blanc", 10),
            *hatch([(-90, -100), (90, -100), (10, -10), (-10, -10)], "jaune", 5, 18),
            line(0, 0, 0, 150, "jaune", 5), *hatch([(-110, 225), (110, 225), (60, 160), (-60, 160)], "jaune", 5, 18)]

def d_chrono(texte="25 min", **k):
    return [circle(0, 20, 210, "blanc", 12), rect(-35, -250, 35, -215, "blanc", 10), line(0, -215, 0, -190, "blanc", 10),
            line(150, -150, 185, -185, "blanc", 10),
            line(0, 20, 0, -140, "rouge", 12), arc(0, 20, 160, 160, -90, 60, "rouge", 7),
            text(texte, 0, 110, 80, "jaune")]

def d_calendrier(texte="7 jours", **k):
    out = [rect(-250, -200, 250, 220, "blanc", 11), line(-250, -120, 250, -120, "blanc", 11),
           *hatch([(-250, -200), (250, -200), (250, -120), (-250, -120)], "rouge", 6, 18),
           line(-150, -235, -150, -170, "blanc", 12), line(150, -235, 150, -170, "blanc", 12)]
    for r in range(3):
        for col in range(5):
            x, y = -190 + col * 95, -60 + r * 90
            out.append(rect(x, y, x + 55, y + 50, "gris", 5))
    out.append(L([(-195, -70), (-125, 0)], "jaune", 9))
    out.append(text(texte, 0, 290, 70, "jaune")) if texte else None
    return out

def d_fleche(texte="", **k):
    return [L([(-320, 0), (300, 0)], "jaune", 16), L([(220, -80), (310, 0), (220, 80)], "jaune", 16)] + \
           ([text(texte, 0, -120, 90, "blanc")] if texte else [])

def d_graphique(**k):
    return [L([(-300, -240), (-300, 220), (320, 220)], "blanc", 10),
            L([(-280, 190), (-200, 170), (-120, 120), (-40, 20), (40, -80), (120, -140), (200, -170), (300, -185)], "jaune", 12)]

def d_check(**k):
    return [circle(0, 0, 220, "vert", 12), L([(-110, 0), (-30, 90), (130, -100)], "vert", 20)]

def d_croix(**k):
    return [circle(0, 0, 220, "rouge", 12), line(-100, -100, 100, 100, "rouge", 20), line(100, -100, -100, 100, "rouge", 20)]

def d_texte(texte="?", c="jaune", **k):
    size = 220 if len(texte) <= 6 else (170 if len(texte) <= 10 else 120)
    return [text(texte, 0, -10, size, c), L([(-260, 120), (0, 130), (260, 115)], "blanc", 8)]

def d_bulle(texte="Encore !", **k):
    return [L([(-60, 150), (-120, 230), (10, 160)], "blanc", 10),
            ellipse(0, 0, 300, 170, "blanc", 11), text(texte, 0, -5, 110, "jaune")]

def d_enveloppe(**k):
    return [rect(-250, -160, 250, 160, "blanc", 11), L([(-250, -160), (0, 40), (250, -160)], "blanc", 10),
            L([(-250, 160), (-60, 0)], "blanc", 7), L([(250, 160), (60, 0)], "blanc", 7)]

def d_groupe(n=7, **k):
    out = []
    n = int(n)
    for i in range(n):
        x = -330 + 660 * i / max(1, n - 1)
        y = 120 + (40 if i % 2 else 0)
        out += stick(x, y, 0.85, "blanc")
    return out

def d_paires(**k):
    pos = [(-280, -40), (-120, -180), (110, -180), (280, -40), (190, 170), (-190, 170)]
    out = []
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            out.append(line(*pos[i], *pos[j], "jaune", 5))
    for x, y in pos:
        out += stick(x, y + 70, 0.55, "blanc")
    return out

def d_euros(texte="€", **k):
    out = []
    for i, dx in enumerate((-190, 0, 190)):
        out += [circle(dx, 20 - (40 if dx == 0 else 0), 120, "jaune", 11), circle(dx, 20 - (40 if dx == 0 else 0), 92, "jaune", 6)]
    out.append(text(texte, 0, -20, 110, "blanc"))
    return out

def d_etiquette(texte="9,99 €", **k):
    pts = [(-300, -130), (200, -130), (320, 0), (200, 130), (-300, 130)]
    return [poly(pts, "blanc", 11), circle(220, 0, 22, "blanc", 8), L([(240, -10), (300, -90), (340, -160)], "gris", 6),
            text(texte, -40, -10, 130, "jaune")]

def d_ticket(**k):
    return [L([(-300, -140), (300, -140), (300, -50), (260, -20), (260, 20), (300, 50), (300, 140), (-300, 140), (-300, 50),
               (-260, 20), (-260, -20), (-300, -50), (-300, -140)], "jaune", 11),
            L([(150, -120), (150, 125)], "jaune", 5), text("CINÉ", -60, -10, 120, "blanc")]

# ---------- dessins par sujet ----------

def d_soleil(**k):
    out = [circle(0, 0, 120, "jaune", 13), *hatch(circle_pts(0, 0, 100), "jaune", 5, 20)]
    for i in range(12):
        a = 2 * math.pi * i / 12
        out.append(line(160 * math.cos(a), 160 * math.sin(a), 240 * math.cos(a), 240 * math.sin(a), "jaune", 11))
    return out

def d_molecules(**k):
    out = []
    for x, y, r in ((-200, -120, 50), (60, -170, 40), (220, 20, 55), (-80, 120, 45), (120, 190, 35), (-260, 160, 30)):
        out += [circle(x, y, r, "blanc", 9), circle(x + 0.7 * r, y, r * 0.6, "blanc", 7)]
    out += [L([(-380, -20), (-260, -40), (-160, 10)], "jaune", 8),
            L([(-160, 10), (-60, -60), (20, -120)], "bleu", 7), L([(-160, 10), (-40, 30), (40, 60)], "bleu", 7),
            L([(-160, 10), (-90, 80), (-60, 170)], "bleu", 7)]
    return out

def d_popcorn(taille="trois", **k):
    def cornet(x, w, h, c="rouge"):
        top = 200 - h
        o = [L([(x - w / 2, top), (x - w * 0.38, 200), (x + w * 0.38, 200), (x + w / 2, top)], "blanc", 10)]
        for f in (-0.25, 0, 0.25):
            o.append(line(x + w * f, top + 8, x + w * f * 0.78, 196, c, 7))
        for i in range(int(w / 40) + 1):
            cx = x - w / 2 + 20 + i * (w - 40) / max(1, int(w / 40))
            o.append(circle(cx, top - 18 - (i % 2) * 20, 26, "jaune", 7, a0=150, a1=420))
        return o
    if taille == "un":
        return cornet(0, 300, 380)
    if taille == "deux":
        return cornet(-170, 170, 200) + cornet(170, 260, 360) + [text("3 €", -170, 260, 80, "jaune"), text("7 €", 170, 260, 80, "jaune")]
    return cornet(-260, 150, 180) + cornet(0, 200, 300) + cornet(260, 250, 370) + \
        [text("3 €", -260, 260, 70, "jaune"), text("6,50 €", 0, 260, 70, "orange"), text("7 €", 260, 260, 70, "jaune")]

def d_voiture(c="rouge", **k):
    return [L([(-330, 80), (-330, 10), (-260, -10), (-170, -110), (110, -110), (200, -10), (320, 10), (330, 80), (-330, 80)], c, 12),
            *hatch([(-320, 75), (-320, 15), (-255, -5), (-170, -100), (105, -100), (195, -5), (315, 15), (320, 75)], c, 5, 26),
            L([(-150, -10), (-100, -85), (-10, -85), (-10, -10), (-150, -10)], "blanc", 8),
            L([(20, -10), (20, -85), (95, -85), (160, -10), (20, -10)], "blanc", 8),
            circle(-190, 85, 60, "blanc", 12), circle(190, 85, 60, "blanc", 12)]

def d_compteur(texte="79 900", **k):
    return [arc(0, 100, 290, 290, 180, 360, "blanc", 12), line(0, 100, -170, -110, "rouge", 12), circle(0, 100, 18, "blanc", 10),
            rect(-170, 140, 170, 240, "blanc", 9), text(texte, 0, 185, 80, "jaune")]

def d_entonnoir(**k):
    out = [L([(-300, -200), (300, -200), (60, 60), (60, 230), (-60, 230), (-60, 60), (-300, -200)], "blanc", 11)]
    for x, y, c in ((-250, -290, "bleu"), (-150, -270, "gris"), (-40, -300, "gris"), (60, -265, "vert"), (170, -295, "gris"), (260, -270, "gris")):
        out.append(circle(x, y, 22, c, 8))
    out += [circle(0, 290, 26, "rouge", 10)]
    return out

def d_poils(**k):
    """Coupe de peau : poils couchés puis dressés, petits muscles."""
    out = [L([(-380, 40), (-200, 30), (0, 45), (200, 30), (380, 40)], "rose", 12)]
    for i, x in enumerate((-280, -100, 80, 260)):
        out += [L([(x, 40), (x - 10, 140)], "rose", 6),
                L([(x, 40), (x + 40, -90), (x + 55, -200)], "blanc", 7),
                L([(x - 5, 110), (x - 60, 60)], "rouge", 9),
                arc(x, 30, 30, 22, 180, 360, "rose", 7)]
    return out

def d_frisson(**k):
    out = [L([(-330, -60), (330, -90)], "rose", 11), L([(-330, 90), (330, 60)], "rose", 11)]
    for x in range(-280, 300, 70):
        y = -75 + (x + 330) * (-30 / 660)
        out.append(arc(x, y, 18, 14, 180, 360, "rose", 7))
        out.append(line(x, y - 14, x + 8, y - 70, "blanc", 5))
    return out

def d_flocon(**k):
    out = []
    for i in range(6):
        a = math.pi * i / 3
        out.append(line(0, 0, 220 * math.cos(a), 220 * math.sin(a), "bleu", 11))
        for f in (0.5, 0.75):
            bx, by = 220 * f * math.cos(a), 220 * f * math.sin(a)
            for s in (-1, 1):
                b = a + s * math.radians(40)
                out.append(line(bx, by, bx + 60 * math.cos(b), by + 60 * math.sin(b), "bleu", 8))
    return out

def d_chat(**k):
    """Chat stylisé au dos rond et poils hérissés (dessin original, silhouette simple)."""
    out = [arc(40, 120, 230, 210, 180, 360, "blanc", 12), line(-190, 120, 270, 120, "blanc", 9)]
    for a in range(195, 350, 14):
        r = math.radians(a)
        x, y = 40 + 230 * math.cos(r), 120 + 210 * math.sin(r)
        out.append(line(x, y, x + 45 * math.cos(r), y + 45 * math.sin(r), "blanc", 6))
    out += [line(-170, 120, -175, 230), line(-110, 120, -110, 230), line(190, 120, 195, 230), line(250, 120, 255, 230),
            L([(270, 60), (330, -40), (310, -150), (350, -230)], "blanc", 11),
            circle(-250, -10, 75, "blanc", 11),
            L([(-305, -55), (-300, -135), (-255, -85)], "blanc", 10), L([(-235, -85), (-195, -130), (-195, -50)], "blanc", 10),
            circle(-280, -15, 10, "jaune", 12), circle(-220, -15, 10, "jaune", 12),
            L([(-260, 25), (-250, 35), (-240, 25)], "blanc", 6)]
    return out

def d_note(**k):
    return [L([(-80, 160), (-80, -160), (140, -200), (140, 110)], "blanc", 11),
            ellipse(-130, 160, 55, 40, "blanc", 11), *hatch(circle_pts(-130, 160, 35, 16), "blanc", 5, 14),
            ellipse(90, 110, 55, 40, "blanc", 11), *hatch(circle_pts(90, 110, 35, 16), "blanc", 5, 14),
            line(-80, -110, 140, -150, "blanc", 11)]

def d_verre(**k):
    """Le travail s'étale : un liquide qui remplit tout le récipient."""
    return [L([(-200, -230), (-160, 230), (160, 230), (200, -230)], "blanc", 12),
            *hatch([(-178, -60), (178, -60), (158, 220), (-158, 220)], "bleu", 6, 20),
            L([(-178, -60), (-90, -80), (0, -55), (90, -80), (178, -60)], "bleu", 9),
            L([(-30, -290), (-30, -200)], "jaune", 8), L([(-60, -230), (-30, -190), (0, -230)], "jaune", 8)]

def d_brouillard(**k):
    out = [line(-330, 200, 330, 200, "blanc", 8), text("?", -200, 0, 140, "gris"), text("?", 30, -100, 110, "gris"), text("?", 220, 30, 130, "gris")]
    for y in (-200, -40, 120):
        out.append(L([(-340, y), (-220, y - 30), (-100, y), (20, y - 30), (140, y), (260, y - 30), (340, y)], "gris", 7))
    return out

def d_cible(**k):
    return [circle(0, 0, 230, "blanc", 11), circle(0, 0, 150, "rouge", 11), circle(0, 0, 70, "blanc", 11),
            *hatch(circle_pts(0, 0, 40, 16), "rouge", 6, 14), L([(330, -300), (10, -10)], "jaune", 12),
            L([(330, -300), (300, -240)], "jaune", 8), L([(330, -300), (270, -270)], "jaune", 8)]

def d_gateau(**k):
    out = [L([(-260, 0), (-260, 200), (260, 200), (260, 0)], "blanc", 12), ellipse(0, 0, 260, 50, "blanc", 11),
           L([(-260, 80), (-180, 110), (-90, 80), (0, 110), (90, 80), (180, 110), (260, 80)], "rose", 9),
           line(-320, 210, 320, 210, "gris", 8)]
    for x in (-150, -50, 50, 150):
        out += [rect(x - 12, -110, x + 12, -10, "bleu", 7), L([(x, -125), (x - 14, -150), (x, -185), (x + 12, -150), (x, -125)], "orange", 7)]
    return out

def d_de(**k):
    return [rect(-170, -170, 170, 170, "blanc", 12)] + [circle(x, y, 22, "jaune", 12) for x, y in ((-90, -90), (90, 90), (0, 0), (-90, 90), (90, -90))]

def d_pourcent(texte="99,9 %", **k):
    return [L([(-320, 200), (-320, -220)], "blanc", 9), L([(-320, 200), (330, 200)], "blanc", 9),
            L([(-300, 190), (-200, 160), (-100, 60), (0, -60), (100, -150), (200, -185), (310, -195)], "jaune", 12),
            L([(-320, 0), (330, 0)], "gris", 5),
            text(texte, 140, 80, 90, "blanc")]

def d_meuble(**k):
    """Petite étagère un peu bancale."""
    return [L([(-220, -230), (-230, 230)], "orange", 13), L([(210, -240), (230, 225)], "orange", 13),
            L([(-225, -230), (210, -245)], "orange", 11), L([(-226, -70), (215, -95)], "orange", 11),
            L([(-228, 80), (220, 70)], "orange", 11), L([(-230, 225), (232, 228)], "orange", 11),
            rect(-170, -170, -90, -78, "bleu", 8), rect(-60, -185, 10, -82, "rose", 8), circle(120, -125, 40, "vert", 8),
            text("?", 300, -120, 90, "jaune")]

def d_outils(**k):
    """Marteau et clé Allen."""
    return [L([(-280, 230), (-20, -40)], "orange", 18),
            poly([(-110, -120), (-20, -210), (90, -100), (0, -10)], "gris", 12),
            L([(60, 240), (60, -20), (250, -20)], "blanc", 16)]

def d_boite(**k):
    return [poly([(-240, -60), (0, -150), (240, -60), (0, 30)], "orange", 11),
            L([(-240, -60), (-240, 150), (0, 250), (240, 150), (240, -60)], "orange", 11), line(0, 30, 0, 250, "orange", 11),
            L([(-240, -60), (-320, -150)], "orange", 9), L([(240, -60), (320, -150)], "orange", 9)]

def d_origami(**k):
    return [poly([(-250, 120), (0, -220), (250, 120)], "bleu", 11), line(0, -220, 0, 180, "bleu", 8),
            L([(-250, 120), (0, 180), (250, 120)], "bleu", 11), line(-120, 30, 0, 180, "blanc", 5), line(120, 30, 0, 180, "blanc", 5)]

def d_moitie(**k):
    """Objet abandonné à moitié : planches éparpillées."""
    return [L([(-220, 200), (-230, -40)], "orange", 13), L([(-225, -40), (60, -60)], "orange", 11),
            L([(80, 170), (300, 120)], "orange", 11), L([(40, 230), (330, 200)], "orange", 11),
            circle(-120, 220, 6, "gris", 8), circle(-60, 230, 6, "gris", 8), circle(160, 240, 6, "gris", 8),
            text("50 %", 160, -160, 100, "rouge")]


DESSINS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("d_")}


def get(spec):
    if not spec:
        return None
    if isinstance(spec, str):
        spec = {"nom": spec}
    spec = dict(spec)
    nom = spec.pop("nom")
    if nom not in DESSINS:
        raise SystemExit(f"Dessin inconnu : {nom}. Dessins disponibles : {', '.join(sorted(DESSINS))}")
    return DESSINS[nom](**spec)


if __name__ == "__main__":
    print("\n".join(sorted(DESSINS)))
