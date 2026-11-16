# Plans propres à l'épisode 10 : le signal « Wow! » (Big Ear, 15 août 1977)
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE...)

CYAN = np.array([1.00, 0.85, 0.35])      # BGR : onde radio
RED = np.array([0.20, 0.25, 1.00])       # encre rouge
PAPER = np.array([0.80, 0.88, 0.92])
HYD = np.array([1.00, 0.55, 0.75])       # violet hydrogène
INT = [6, 14, 26, 30, 19, 5]             # 6 E Q U J 5 (échelle d'intensité)
R10 = np.random.default_rng(10)
CLOUD = R10.normal(0, 1, (260, 3)) * [0.9, 0.55, 0.7]
PRINT = R10.integers(0, 4, (18, 8))


def fv(x):
    return float(np.asarray(x))


def big_ear(sc, s=1.0, col=GOLD, drop=0.0):
    """Big Ear : réflecteur plan inclinable, plan de sol, réflecteur parabolique fixe."""
    W = 1.7 * s
    # plan de sol (grille)
    for x in np.linspace(-W, W, 13):
        sc.seg([x, 0, -1.4 * s], [x, 0, 1.3 * s], col * 0.25, 1)
    for z in np.linspace(-1.4 * s, 1.3 * s, 11):
        sc.seg([-W, 0, z], [W, 0, z], col * 0.25, 1)
    # réflecteur plan incliné (côté sud)
    tilt = 0.55
    base = np.array([0, 0, -1.4 * s])
    for k in range(9):
        f = k / 8
        y = 1.0 * s * f * math.cos(tilt)
        z = -1.4 * s - 1.0 * s * f * math.sin(tilt)
        yy = y - drop * f * 1.2
        sc.seg([-W, max(yy, 0), z], [W, max(yy, 0), z], col * (0.9 if k in (0, 8) else 0.45), 2 if k in (0, 8) else 1)
    for x in np.linspace(-W, W, 11):
        sc.seg([x, 0, -1.4 * s], [x, max(1.0 * s * math.cos(tilt) - drop * 1.2, 0), -1.4 * s - 1.0 * s * math.sin(tilt)], col * 0.45, 1)
    # réflecteur parabolique (côté nord)
    ys = np.linspace(0, 1.25 * s, 14)
    zp = 1.3 * s + 0.45 * s * (ys / (1.25 * s)) ** 2
    yd = np.maximum(ys - drop * 1.5 * (ys / ys[-1]), 0)
    for x in np.linspace(-W, W, 11):
        sc.add(np.stack([np.full_like(ys, x), yd, zp], 1), col * 0.6, 1)
    for k in range(0, 14, 3):
        sc.seg([-W, yd[k], zp[k]], [W, yd[k], zp[k]], col * (0.9 if k == 12 else 0.5), 2 if k == 12 else 1)
    sc.seg([-W, yd[-1], zp[-1]], [W, yd[-1], zp[-1]], col, 2)
    # cornets d'alimentation au foyer
    for dx in (-0.12, 0.12):
        sc.box([dx * s, 0.12 * s, 0.75 * s], [0.12 * s, 0.14 * s, 0.22 * s], WHITE * 0.8, 1)


def wave(sc, a, b, amp, cycles, col, w=2, n=120, prog=1.0, phase=0.0):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a; L = np.linalg.norm(d); d = d / L
    perp = np.cross(d, [0, 0, 1]); perp = perp / (np.linalg.norm(perp) + 1e-9)
    if np.linalg.norm(np.cross(d, [0, 0, 1])) < 1e-3: perp = np.array([0, 1, 0])
    s = np.linspace(0, prog, max(2, int(n * prog)))
    P = a[None] + np.outer(s * L, d) + np.outer(amp * np.sin(2 * math.pi * cycles * s + phase), perp)
    sc.add(P, col, w)


def printout(sc, t, circ=1.0, hl=1.0):
    """Feuille de listing : colonnes de caractères (traits), une colonne entourée."""
    w, h = 1.1, 1.7
    sc.add([[-w, -h, 0], [w, -h, 0], [w, h, 0], [-w, h, 0]], PAPER * 0.7, 2, closed=True)
    for y in np.linspace(-h + 0.1, h - 0.1, 18):    # trous d'entraînement
        for x in (-w + 0.07, w - 0.07):
            sc.circle([x, y, 0], 0.025, PAPER * 0.35, 1, 8, axis="z")
    rows = np.linspace(h - 0.2, -h + 0.2, 18)
    cols = np.linspace(-w + 0.3, w - 0.3, 8)
    for i, y in enumerate(rows):
        for j, x in enumerate(cols):
            hit = (j == 4 and 6 <= i <= 11)
            v = PRINT[i, j]
            if hit: v = 1 + INT[i - 6] // 6
            c = (GOLD * (0.5 + 0.5 * hl)) if hit else PAPER * 0.45
            if v == 0 and not hit:
                sc.seg([x - 0.02, y, 0], [x + 0.02, y, 0], c * 0.6, 1)
            else:
                sc.seg([x - 0.06, y, 0], [x + 0.06, y, 0], c, 2 if hit else 1)
                sc.seg([x, y - 0.04, 0], [x, y + 0.04, 0], c, 2 if hit else 1)
    if circ > 0:   # ellipse à l'encre rouge, tracée progressivement
        th = np.linspace(0.3, 0.3 + 2 * math.pi * 1.08 * circ, max(2, int(100 * circ)))
        cx, cy = cols[4], (rows[6] + rows[11]) / 2
        P = np.stack([cx + 0.2 * np.cos(th) + 0.01 * np.sin(5 * th), cy + 0.62 * np.sin(th), np.full_like(th, 0.02)], 1)
        sc.add(P, RED, 3)


# ------------------------------------------------------------------ plans
def sh_hook_sky(img, u, t, v, T):
    """Une onde radio traverse le ciel étoilé et arrive sur la Grande Oreille."""
    sc = Scene()
    big_ear(sc, 0.8, GOLD * 0.8)
    pr = ease(u * 1.3)
    wave(sc, [0, 3.5, -6], [0, 0.4, 0.6], 0.06, 14, CYAN, 2, 200, pr, -6 * t)
    if pr > 0.95:
        sc.circle([0, 0.15, 0.6], 0.2 + 0.4 * ((t * 1.5) % 1), CYAN * (1 - (t * 1.5) % 1), 2, 40)
    cam = look_at(*orbit([0, 1.2, -0.4], lerp(6.8, 5.8, ease(u)), 2.6 + 0.2 * u, 0.35))
    stars(img, cam, T, 1.2, 0.03 * T); draw(img, sc, cam, fade=(2, 14))


def sh_hook_print(img, u, t, v, T):
    """Le listing ; l'encre rouge entoure la colonne."""
    sc = Scene()
    printout(sc, t, circ=ease((u - 0.15) * 1.6))
    cam = look_at(*orbit([0, -0.1, 0], lerp(3.6, 2.9, ease(u)), -0.25 + 0.3 * u, 0.12))
    draw(img, sc, cam, fade=(1, 9))


def sh_big_ear(img, u, t, v, T):
    """Le radiotélescope Big Ear, grand comme trois terrains de football."""
    sc = Scene()
    big_ear(sc, 1.0)
    az = [2.4, 0.9, -1.0][v % 3]
    cam = look_at(*orbit([0, 0.35, 0], lerp(6.2, 5.4, ease(u)), az + 0.3 * u, lerp(0.6, 0.42, u)))
    stars(img, cam, T, 0.8, 0.04 * T); draw(img, sc, cam, fade=(2, 14))


def sh_spike(img, u, t, v, T):
    """Bruit de fond en barres 3D… puis un pic trente fois plus haut."""
    sc = Scene()
    n = 40
    sc.seg([-2, 0, 0], [2, 0, 0], WHITE * 0.5, 1)
    for k in range(n):
        x = -1.9 + 3.8 * k / (n - 1)
        hgt = 0.05 + 0.04 * abs(math.sin(7.3 * k + 3 * t))
        if k == 26:
            hgt = 0.05 + 2.2 * ease((u - 0.25) * 2.5)
        col = CYAN if k == 26 else WHITE * 0.45
        sc.box([x, hgt / 2, 0], [0.05, hgt, 0.05], col, 2 if k == 26 else 1)
    cam = look_at(*orbit([0, 1.0, 0], lerp(3.6, 3.1, ease(u)), -0.35 + 0.25 * u, 0.15))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 10))


def sh_scan(img, u, t, v, T):
    """La Terre tourne : le faisceau fixe balaye une bande du ciel, une source passe."""
    sc = Scene()
    rot = 0.6 * u
    th = np.linspace(0, 2 * math.pi, 64)
    for lat in np.linspace(-1.2, 1.2, 7):
        r = math.cos(lat)
        sc.add(np.stack([r * np.cos(th), np.full_like(th, math.sin(lat)), r * np.sin(th)], 1), WHITE * 0.3, 1, closed=True)
    for k in range(10):
        a = rot + k * math.pi / 5
        ph = np.linspace(-math.pi / 2, math.pi / 2, 40)
        sc.add(np.stack([np.cos(ph) * math.cos(a), np.sin(ph), np.cos(ph) * math.sin(a)], 1), WHITE * 0.3, 1)
    lat0, a0 = 0.7, rot + 0.4
    p = np.array([math.cos(lat0) * math.cos(a0), math.sin(lat0), math.cos(lat0) * math.sin(a0)])
    sc.circle(p, 0.04, GOLD, 2, 12, axis="z")
    up = p / np.linalg.norm(p)
    tip = p + up * 1.3
    sc.seg(p, tip, GOLD * 0.8, 2)
    # bande balayée dans le ciel
    band = np.stack([2.2 * math.cos(lat0) * np.cos(th), np.full_like(th, 2.2 * math.sin(lat0)), 2.2 * math.cos(lat0) * np.sin(th)], 1)
    sc.add(band, AMBER * 0.35, 1, closed=True)
    src_a = 0.4 + 0.6 * 0.55
    src = 2.2 * np.array([math.cos(lat0) * math.cos(src_a), math.sin(lat0), math.cos(lat0) * math.sin(src_a)])
    hit = abs(a0 - src_a) < 0.06
    sc.circle(src, 0.08, CYAN if hit else WHITE * 0.7, 3 if hit else 1, 16, axis="z")
    if hit:
        sc.seg(p, src, CYAN, 2)
    cam = look_at(*orbit([0, 0.6, 0], 5.0, 1.1 + 0.15 * u, 0.3))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(3, 14))


def sh_printout(img, u, t, v, T):
    """Gros plan sur le listing : la colonne s'illumine puis l'encre rouge l'entoure."""
    sc = Scene()
    printout(sc, t, circ=ease((u - 0.45) * 2.2), hl=ease(u * 2))
    cx = lerp(0.0, 0.25, ease(u))
    cam = look_at(*orbit([fv(cx), -0.05, 0], lerp(3.4, 2.1, ease(u)), 0.35 - 0.4 * u + 0.2 * v, 0.1))
    draw(img, sc, cam, fade=(1, 8))


def sh_intensity(img, u, t, v, T):
    """Six barres : 6, E, Q, U, J, 5 — l'intensité monte, culmine, retombe."""
    sc = Scene()
    sc.grid_plane(1.8, 12, 0.0, WHITE * 0.18)
    for k, val in enumerate(INT):
        g = ease(u * 2.2 - k * 0.18)
        hgt = 0.02 + 2.0 * val / 30 * g
        x = -1.25 + k * 0.5
        sc.box([x, hgt / 2, 0], [0.3, hgt, 0.3], CYAN if val == 30 else GOLD, 2, grid=3 if hgt > 0.4 else 0)
    xs = np.linspace(-1.5, 1.5, 80)
    ys = 2.0 * np.exp(-((xs - 0.25) / 0.75) ** 2)
    sc.add(np.stack([xs, ys * ease(u * 1.6 - 0.8), np.full_like(xs, -0.3)], 1), WHITE * 0.6, 1)
    cam = look_at(*orbit([0, 0.9, 0], lerp(4.6, 4.0, ease(u)), 0.55 - 0.5 * u, 0.25))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 10))


def sh_hydrogen(img, u, t, v, T):
    """Atome d'hydrogène : proton, électron, et l'onde de 21 cm qui s'échappe."""
    sc = Scene()
    sc.circle([0, 0, 0], 0.12, GOLD, 3, 20, axis="z"); sc.circle([0, 0, 0], 0.12, GOLD, 2, 20, axis="x")
    for k, (ax, tl) in enumerate((("y", 0), ("z", 0), ("x", 0))):
        sc.circle([0, 0, 0], 0.9, HYD * 0.45, 1, 80, axis=ax)
    a = 2.2 * t
    e = np.array([0.9 * math.cos(a), 0.9 * math.sin(a) * 0.4, 0.9 * math.sin(a)])
    sc.circle(e, 0.06, WHITE, 2, 12, axis="z")
    # flèches de spin
    flip = 1 if (t % 2.4) < 1.2 else -1
    sc.seg([0, -0.25, 0], [0, 0.25, 0], GOLD, 2)
    sc.seg(e + [0, -0.15 * flip, 0], e + [0, 0.15 * flip, 0], WHITE, 2)
    for ph in range(3):
        d = ((t * 0.8 + ph / 3) % 1)
        wave(sc, [1.1 + 2.5 * d, 0, 0], [1.6 + 2.5 * d, 0, 0], 0.08 * (1 - d), 2, CYAN * (1 - d), 2, 40)
    cam = look_at(*orbit([0.5, 0, 0], lerp(3.6, 3.0, ease(u)), 0.3 + 0.4 * u + 0.4 * v, 0.2))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 10))


TEAPOT = np.array([[0, 0], [0.5, 0.1], [0.9, 0.0], [0.8, -0.5], [0.3, -0.6], [0, -0.3], [-0.4, -0.1], [-0.6, 0.35], [0.5, 0.1]]) * 1.4


def sh_sagittarius(img, u, t, v, T):
    """La constellation du Sagittaire, la cible du signal encerclée."""
    sc = Scene()
    P = np.c_[TEAPOT[:, 0], TEAPOT[:, 1], np.zeros(len(TEAPOT))]
    n = max(2, int(len(P) * ease(u * 1.5)))
    sc.add(P[:n], WHITE * 0.55, 1)
    for p in P:
        sc.circle(p, 0.04, WHITE, 2, 10, axis="z")
    tgt = np.array([0.15, 0.75, 0])
    r = lerp(0.9, 0.18, ease((u - 0.3) * 2))
    sc.circle(tgt, fv(r), CYAN, 2, 40, axis="z")
    for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        sc.seg(tgt + np.array([d[0], d[1], 0]) * fv(r) * 1.2, tgt + np.array([d[0], d[1], 0]) * fv(r) * 1.6, CYAN, 2)
    cam = look_at(*orbit([0.1, 0.1, 0], lerp(4.0, 3.4, ease(u)), 0.15 * math.sin(0.4 * t), 0.05))
    stars(img, cam, T, 1.4, 0.02 * T); draw(img, sc, cam, fade=(2, 10))


def dish(sc, c, r, aim, col):
    c = np.asarray(c, float)
    for k in range(1, 4):
        rr = r * k / 3
        sc.circle(c + aim * (0.25 * r * (k / 3) ** 2), rr, col * (1 if k == 3 else 0.5), 1 if k < 3 else 2, 24)
    sc.seg(c - [0, 0.5 * r, 0], c, col * 0.7, 2)
    sc.seg(c, c + aim * 0.6 * r, col * 0.7, 1)


def sh_search(img, u, t, v, T):
    """D'autres antennes (réseau en Y) pointent la même zone : rien."""
    sc = Scene()
    sc.grid_plane(2.6, 16, 0.0, WHITE * 0.15)
    aim = np.array([0, 1, 0])
    for arm in range(3):
        a = arm * 2 * math.pi / 3 + 0.3
        for k in range(1, 5):
            d = 0.55 * k
            dish(sc, [d * math.cos(a), 0.35, d * math.sin(a)], 0.22, aim, GOLD)
    for k in range(5):   # cercles d'écoute qui montent dans le vide
        d = ((t * 0.5 + k / 5) % 1)
        sc.circle([0, 0.6 + 2.5 * d, 0], 0.3 + 1.2 * d, CYAN * 0.5 * (1 - d), 1, 48)
    cam = look_at(*orbit([0, 0.6, 0], lerp(6.5, 5.8, ease(u)), 0.4 + 0.4 * u, lerp(0.75, 0.6, u)))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(2, 12))


def sh_magnetar(img, u, t, v, T):
    """Un nuage d'hydrogène froid, illuminé par l'éclair d'un magnétar lointain."""
    sc = Scene()
    flash = max(0.0, math.sin(math.pi * min(max((u - 0.3) / 0.35, 0), 1)))
    for p in CLOUD:
        q = p
        c = lerp(HYD * 0.35, CYAN * 1.1, flash)
        sc.seg(q - [0.02, 0, 0], q + [0.02, 0, 0], c, 1); sc.seg(q - [0, 0.02, 0], q + [0, 0.02, 0], c, 1)
    m = np.array([0.0, 2.3, -0.6])
    sc.circle(m, 0.08, WHITE, 3, 16, axis="z")
    for k in range(6):   # lignes de champ
        a = k * math.pi / 3 + 0.4 * t
        th = np.linspace(0.2, math.pi - 0.2, 30)
        R = 0.45
        P = np.stack([m[0] + R * np.sin(th) ** 2 * np.cos(a) * np.sin(th) * 2, m[1] + R * np.cos(th) * np.sin(th) * 2, m[2] + R * np.sin(th) ** 2 * np.sin(a) * 2 * np.sin(th)], 1)
        sc.add(P, AMBER * 0.6, 1)
    if flash > 0:
        for k in range(12):
            a = k * math.pi / 6
            d = np.array([math.cos(a), math.sin(a) * 0.5, math.sin(a)])
            sc.seg(m, m + d * (0.3 + 3.5 * flash), WHITE * flash, 2)
    if u > 0.55:   # l'onde part vers la Terre
        wave(sc, [0, -0.9, 0], [0, -3.2, 0], 0.06, 8, CYAN, 2, 80, ease((u - 0.55) * 2.5), -6 * t)
    cam = look_at(*orbit([0, 0.2, 0], lerp(6.0, 5.2, ease(u)), 0.3 + 0.25 * u, 0.15))
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(2, 14))


def sh_demolish(img, u, t, v, T):
    """La Grande Oreille s'efface et s'affaisse."""
    sc = Scene()
    big_ear(sc, 1.0, GOLD * lerp(1.0, 0.25, ease(u)), drop=ease((u - 0.2) * 1.4))
    cam = look_at(*orbit([0, 0.3, 0], lerp(5.6, 6.6, ease(u)), 2.2 - 0.3 * u, 0.55))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(2, 14))


def sh_final(img, u, t, v, T):
    """Le listing entouré de rouge s'éloigne dans le ciel étoilé."""
    sc = Scene()
    printout(sc, t, circ=1.0)
    cam = look_at(*orbit([0, 0, 0], lerp(2.6, 6.5, ease(u)), 0.2 * math.sin(0.3 * t), 0.08))
    stars(img, cam, T, 1.4, 0.02 * T); draw(img, sc, cam, fade=(2, 20))
