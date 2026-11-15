# Plans propres à l'épisode 9 : le lac Vostok, sous la glace de l'Antarctique
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE...)

ICE = np.array([1.00, 0.92, 0.72])       # BGR : glace bleu pâle
WATER = np.array([1.00, 0.62, 0.22])     # bleu profond
DEEP = np.array([0.70, 0.38, 0.12])
GAS = np.array([1.00, 0.95, 0.60])
RED = np.array([0.20, 0.25, 1.00])
TH = 1.6                                 # épaisseur de glace (unités)
LX, LZ = 1.5, 0.3                        # demi-axes du lac (250 × 50 km)


def ice_block(sc, size=1.8, y0=0.0, y1=-TH, n=12, col=ICE):
    """Coupe de calotte : couches de glace (cadres) et arêtes verticales."""
    for k in range(n + 1):
        y = y0 + (y1 - y0) * k / n
        c = col * (0.55 if k % 3 == 0 else 0.22)
        sc.add([[-size, y, -size * 0.6], [size, y, -size * 0.6], [size, y, size * 0.6], [-size, y, size * 0.6]], c, 1, closed=True)
    for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        sc.seg([sx * size, y0, sz * size * 0.6], [sx * size, y1, sz * size * 0.6], col * 0.45, 1)


def lake(sc, y=-TH, col=WATER, t=0.0, rings=5, depth=0.35, amp=0.0):
    """Lac lenticulaire : contours elliptiques empilés vers le bas."""
    th = np.linspace(0, 2 * math.pi, 90)
    for k in range(rings):
        f = 1 - k / rings
        yy = y - depth * (k / rings) ** 0.7 + amp
        P = np.stack([LX * f * np.cos(th), np.full_like(th, yy), LZ * f * np.sin(th)], 1)
        sc.add(P, col * (1.0 if k == 0 else 0.5), 2 if k == 0 else 1, closed=True)
    for x in np.linspace(-LX * 0.9, LX * 0.9, 13):   # rides
        zz = LZ * math.sqrt(max(1 - (x / LX) ** 2, 0)) * 0.95
        zs = np.linspace(-zz, zz, 8)
        ys = y + amp + 0.012 * np.sin(6 * zs + 2 * t + 3 * x)
        sc.add(np.stack([np.full_like(zs, x), ys, zs], 1), col * 0.35, 1)


def station(sc, c=(0, 0, 0), s=1.0, col=GOLD):
    c = np.asarray(c, float)
    for dx, dz, w, h, d in ((0, 0, 0.6, 0.22, 0.3), (0.55, 0.2, 0.35, 0.16, 0.25), (-0.5, -0.15, 0.4, 0.3, 0.3)):
        sc.box(c + np.array([dx, h / 2, dz]) * s, [w * s, h * s, d * s], col, 1)
    sc.seg(c + [-0.1 * s, 0.22 * s, 0], c + [-0.1 * s, 0.9 * s, 0], col, 2)   # mât
    sc.circle(c + [-0.1 * s, 0.9 * s, 0], 0.05 * s, WHITE, 2, 12, axis="z")
    sc.box(c + [0.95 * s, 0.35 * s, -0.4 * s], [0.18 * s, 0.7 * s, 0.18 * s], col * 0.7, 1)  # tour de forage


def helix(sc, c, h, r, turns, rot, col, rungs=True):
    th = np.linspace(0, 2 * math.pi * turns, 140)
    y = c[1] - h / 2 + h * th / th[-1]
    for ph in (0, math.pi):
        P = np.stack([c[0] + r * np.cos(th + rot + ph), y, c[2] + r * np.sin(th + rot + ph)], 1)
        sc.add(P, col, 2)
    if rungs:
        for k in range(0, 140, 5):
            a = th[k] + rot
            sc.seg([c[0] + r * math.cos(a), y[k], c[2] + r * math.sin(a)],
                   [c[0] - r * math.cos(a), y[k], c[2] - r * math.sin(a)], col * 0.45, 1)


R9 = np.random.default_rng(9)
BUB = R9.uniform(0, 1, (160, 4))
DUST = R9.uniform(-1, 1, (40, 3))


# ------------------------------------------------------------------ plans
def sh_hook_ice(img, u, t, v, T):
    """La caméra descend à travers les couches de glace vers le noir."""
    sc = Scene()
    sc.grid_plane(1.8, 14, 0.0, WHITE * 0.25)
    ice_block(sc, 1.6, 0.0, -TH, 14)
    lake(sc, -TH, WATER * ease(u * 1.5), t)
    y = lerp(0.6, -TH * 0.7, ease(u))[()]
    cam = look_at(*orbit([0, y, 0], lerp(4.6, 3.6, ease(u)), 0.5 + 0.3 * u + 0.6 * v, lerp(0.45, 0.12, ease(u))))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 12))


def sh_hook_lake(img, u, t, v, T):
    """Le lac apparaît sous la glace, isolé, la glace au-dessus en fantôme."""
    sc = Scene()
    ice_block(sc, 1.7, -0.2, -TH, 8, ICE * 0.6)
    lake(sc, -TH, WATER, t, rings=6)
    cam = look_at(*orbit([0, -TH - 0.05, 0], lerp(3.6, 2.9, ease(u)), 0.9 + 0.4 * u, lerp(0.35, 0.25, u)))
    draw(img, sc, cam, fade=(1.5, 9))


def sh_base(img, u, t, v, T):
    """La station Vostok sur le plateau glacé."""
    sc = Scene()
    sc.grid_plane(3.0, 20, 0.0, ICE * 0.22)
    station(sc, (0, 0, 0), 1.3, GOLD)
    R = np.random.default_rng(83)
    for i in range(26):   # congères
        x, z = R.uniform(-3, 3, 2)
        if abs(x) < 1.6 and abs(z) < 1.2: continue
        r = R.uniform(0.2, 0.5)
        sc.add([[x - r, 0, z], [x, R.uniform(0.04, 0.12), z], [x + r, 0, z]], ICE * 0.4, 1)
    az = [0.5, 2.2, -1.0][v % 3]
    cam = look_at(*orbit([0, 0.35, 0], lerp(2.6, 2.1, ease(u)), az + 0.35 * u, lerp(0.3, 0.18, u)))
    stars(img, cam, T, 1.0, 0.05 * T); draw(img, sc, cam, fade=(2, 12))


def sh_thermo(img, u, t, v, T):
    """Thermomètre géant : la colonne chute jusqu'à −89 °C."""
    sc = Scene()
    x0, top, bot = 0.0, 1.4, -1.4
    sc.add([[-0.12, bot, 0], [0.12, bot, 0], [0.12, top, 0], [-0.12, top, 0]], WHITE * 0.8, 2, closed=True)
    sc.circle([0, bot - 0.2, 0], 0.22, WHITE * 0.8, 2, 32, axis="z")
    lvl = lambda c: bot + (top - bot) * (c + 100) / 140     # échelle −100 … +40 °C
    for c in range(-100, 41, 10):
        L = 0.22 if c % 50 == 0 else 0.12
        sc.seg([0.12, lvl(c), 0], [0.12 + L, lvl(c), 0], WHITE * (0.8 if c % 50 == 0 else 0.4), 2 if c == 0 else 1)
    cur = lerp(20, -89, ease(u * 1.3))[()]
    for y in np.linspace(bot, lvl(cur), 40):
        sc.seg([-0.07, y, 0], [0.07, y, 0], lerp(RED, ICE, (20 - cur) / 109), 2)
    sc.circle([0, bot - 0.2, 0], 0.15, lerp(RED, ICE, (20 - cur) / 109), 3, 24, axis="z")
    sc.seg([-0.5, lvl(-89), 0], [0.6, lvl(-89), 0], ICE, 2)
    for p in DUST:   # cristaux
        q = np.array([p[0] * 1.4, p[1] * 1.8, p[2] * 0.6])
        sc.seg(q - [0.03, 0, 0], q + [0.03, 0, 0], ICE * 0.5, 1); sc.seg(q - [0, 0.03, 0], q + [0, 0.03, 0], ICE * 0.5, 1)
    cam = look_at(*orbit([0.1, -0.1, 0], lerp(3.9, 3.5, ease(u)), 0.25 * math.sin(0.5 * t) + 0.3 * v, 0.05))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 12))


def sh_liquid(img, u, t, v, T):
    """Sous le plafond de glace, la surface de l'eau ondule."""
    sc = Scene()
    for k in range(5):   # plafond
        sc.grid_plane(1.6, 10, 0.55 + 0.12 * k, ICE * (0.35 - 0.05 * k))
    xs = np.linspace(-1.6, 1.6, 40)
    for z in np.linspace(-1.4, 1.4, 16):
        ys = 0.06 * np.sin(3 * xs + 1.6 * t + 2 * z) + 0.03 * np.sin(5 * z - t)
        sc.add(np.stack([xs, ys, np.full_like(xs, z)], 1), WATER * (0.9 if abs(z) < 0.5 else 0.5), 2 if abs(z) < 0.5 else 1)
    cam = look_at(*orbit([0, 0.1, 0], lerp(2.8, 2.2, ease(u)), 0.3 + 0.5 * u, 0.12))
    draw(img, sc, cam, fade=(1, 7))


def sh_lake_map(img, u, t, v, T):
    """Vue du dessus : le contour du lac, règles de 250 km et 50 km."""
    sc = Scene()
    sc.grid_plane(2.2, 16, -0.05, ICE * 0.15)
    th = np.linspace(0, 2 * math.pi, 120)
    wob = 1 + 0.06 * np.sin(3 * th) + 0.04 * np.cos(5 * th)
    prog = ease(u * 1.4)
    n = max(2, int(120 * prog))
    P = np.stack([LX * wob * np.cos(th), np.zeros_like(th), 1.6 * LZ * wob * np.sin(th)], 1)
    sc.add(P[:n], WATER, 3)
    if prog > 0.6:
        sc.seg([-LX, 0.01, 0.75], [LX, 0.01, 0.75], AMBER, 3)
        for x in (-LX, LX): sc.seg([x, 0.01, 0.68], [x, 0.01, 0.82], AMBER, 3)
        sc.seg([LX + 0.25, 0.01, -1.6 * LZ], [LX + 0.25, 0.01, 1.6 * LZ], GOLD, 3)
    cam = look_at(*orbit([0, 0, 0.1], lerp(4.6, 4.0, ease(u)), 0.15 * math.sin(0.3 * t) + 0.2 * v, lerp(1.35, 1.2, u)))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 12))


def sh_pressure(img, u, t, v, T):
    """La glace écrase l'eau : flèches de pression, manomètre."""
    sc = Scene()
    ice_block(sc, 1.0, 0.9, -0.2, 8)
    lake(sc, -0.25, WATER, t, rings=4, depth=0.3)
    off = (0.25 * t) % 0.3
    for x in np.linspace(-0.8, 0.8, 5):
        for k in range(2):
            y = 0.8 - off - 0.4 * k
            sc.seg([x, y, 0.65], [x, y - 0.25, 0.65], AMBER, 2)
            sc.seg([x, y - 0.25, 0.65], [x - 0.06, y - 0.17, 0.65], AMBER, 2)
            sc.seg([x, y - 0.25, 0.65], [x + 0.06, y - 0.17, 0.65], AMBER, 2)
    g = np.array([0.0, -1.0, 0.7])
    sc.circle(g, 0.35, WHITE * 0.8, 2, 40, axis="z")
    for a in np.linspace(-2.3, 2.3, 11):
        sc.seg(g + [0.3 * math.sin(a), 0.3 * math.cos(a), 0], g + [0.35 * math.sin(a), 0.35 * math.cos(a), 0], WHITE * 0.5, 1)
    a = lerp(-2.3, 2.0, ease(u * 1.3))[()]
    sc.seg(g, g + [0.3 * math.sin(a), 0.3 * math.cos(a), 0], AMBER, 3)
    cam = look_at(*orbit([0, -0.05, 0], lerp(3.8, 3.3, ease(u)), 0.35 + 0.25 * u + 0.4 * v, 0.15))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 12))


def sh_gas(img, u, t, v, T):
    """Deux cuves : un lac ordinaire (quelques bulles) et Vostok (saturé)."""
    sc = Scene()
    for cx, nb in ((-0.62, 4), (0.62, 160)):
        sc.box([cx, 0, 0], [0.95, 2.6, 0.95], WATER * 0.7, 1)
        k = nb if cx < 0 else int(4 + 156 * ease(u * 1.3))
        for a, b, c, s in BUB[:k]:
            y = -1.25 + ((a + 0.08 * t * (0.5 + s)) % 1.0) * 2.5
            sc.circle([cx + (b - 0.5) * 0.85, y, (c - 0.5) * 0.85], 0.015 + 0.025 * s, GAS, 1, 10, axis="z")
    cam = look_at(*orbit([0, 0, 0], lerp(4.1, 3.7, ease(u)), 0.15 * math.sin(0.4 * t) + 0.3 * v, 0.12))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 12))


def sh_tides(img, u, t, v, T):
    """La Lune tourne, la surface du lac se soulève et redescend."""
    sc = Scene()
    ice_block(sc, 1.7, 0.4, -0.6, 6, ICE * 0.6)
    amp = 0.08 * math.sin(1.6 * t)
    lake(sc, -0.65, WATER, t, rings=5, amp=amp)
    sc.seg([1.8, -0.65, 0], [2.0, -0.65, 0], WHITE * 0.5, 1)
    sc.seg([1.9, -0.65, 0], [1.9, -0.65 + amp, 0], AMBER, 3)
    a = 0.5 * t
    m = np.array([1.2 * math.cos(a), 1.25, 0.6 * math.sin(a) - 0.4])
    sc.circle(m, 0.28, WHITE, 2, 32, axis="z"); sc.circle(m, 0.28, WHITE * 0.4, 1, 32, axis="x")
    sc.circle(m, 0.28, WHITE * 0.4, 1, 32, axis="y")
    cam = look_at(*orbit([0, 0.2, 0], lerp(4.0, 3.5, ease(u)), 0.4 + 0.3 * u, 0.18))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(2, 14))


def sh_drill(img, u, t, v, T):
    """Le forage traverse la glace jusqu'au lac, repères de profondeur."""
    sc = Scene()
    ice_block(sc, 1.2, 0.0, -TH, 14)
    lake(sc, -TH, WATER, t, rings=4)
    station(sc, (0.0, 0, -0.5), 0.5, GOLD * 0.8)
    d = TH * ease(u * 1.25)
    sc.seg([0, 0.3, 0], [0, -d, 0], WHITE, 3)
    sc.circle([0, -d, 0], 0.06, AMBER, 2, 16)
    for k in range(9):
        y = -TH * k / 8
        if -y <= d + 1e-6:
            sc.seg([-0.12, y, 0], [0.12, y, 0], AMBER * 0.8, 2)
    cam = look_at(*orbit([0, -d * 0.6 - 0.2, 0], lerp(4.4, 3.6, ease(u)), 0.6 + 0.4 * u + v, 0.2))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 14))


def sh_gush(img, u, t, v, T):
    """L'eau remonte dans le trou, puis se fige en cristaux."""
    sc = Scene()
    ice_block(sc, 0.9, 0.6, -1.4, 10, ICE * 0.7)
    for k in range(4):
        sc.circle([0, -1.45 - 0.05 * k, 0], 0.9 - 0.15 * k, WATER * 0.6, 1, 48)
    for y in np.linspace(0.6, -1.4, 20):
        sc.circle([0, y, 0], 0.09, WHITE * 0.35, 1, 16)
    top = lerp(-1.4, 0.2, ease(u * 1.6))[()]
    frz = ease((u - 0.55) / 0.35)
    col = lerp(WATER, WHITE, frz)
    for y in np.linspace(-1.4, top, 26):
        sc.circle([0, y, 0], 0.07, col, 2, 14)
    if frz > 0.05:
        for y in np.linspace(-1.2, top, 9):
            for a in range(3):
                ang = a * math.pi / 3 + 0.3 * t
                d = np.array([math.cos(ang), 0, math.sin(ang)]) * 0.16 * frz
                sc.seg([0, y, 0] - d, [0, y, 0] + d, WHITE, 2)
    cam = look_at(*orbit([0, -0.5, 0], lerp(3.2, 2.7, ease(u)), 0.5 + 0.5 * u, 0.15))
    draw(img, sc, cam, fade=(1, 8))


def sh_dna(img, u, t, v, T):
    """Double hélice dans un cube de glace, des particules suspectes autour."""
    sc = Scene()
    sc.box([0, 0, 0], [1.4, 2.4, 1.4], ICE * 0.5, 1)
    helix(sc, [0, 0, 0], 2.0, 0.35, 2.5, 0.6 * t, GOLD)
    if u > 0.55:
        k = int(40 * ease((u - 0.55) / 0.3))
        for p in DUST[:k]:
            q = p * np.array([1.1, 1.3, 1.1])
            sc.circle(q, 0.03, RED, 2, 10, axis="z")
    cam = look_at(*orbit([0, 0, 0], lerp(4.2, 3.6, ease(u)), 0.3 * u + 0.4 * v, 0.1))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 10))


def sh_final(img, u, t, v, T):
    """Retour : on remonte du lac à travers la glace jusqu'à la surface étoilée."""
    sc = Scene()
    sc.grid_plane(1.8, 14, 0.0, WHITE * 0.25)
    ice_block(sc, 1.6, 0.0, -TH, 14)
    lake(sc, -TH, WATER * lerp(1.0, 0.6, u)[()], t, rings=6)
    y = lerp(-TH * 0.8, 0.8, ease(u))[()]
    cam = look_at(*orbit([0, y, 0], lerp(3.0, 4.6, ease(u)), 1.2 - 0.6 * u, lerp(0.12, 0.45, ease(u))))
    stars(img, cam, T, lerp(0.3, 1.0, u)[()]); draw(img, sc, cam, fade=(2, 13))
