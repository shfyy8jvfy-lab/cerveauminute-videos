# Plans propres à l'épisode 15 : le mortier au riz gluant (et la Grande Muraille)
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

RICE = np.array([0.85, 0.95, 1.00])      # BGR : blanc crème
LIME = np.array([0.80, 0.85, 0.80])      # chaux, gris clair
VIOLET = np.array([0.95, 0.30, 0.70])
RED = np.array([0.25, 0.25, 1.00])
R15 = np.random.default_rng(15)
GR = R15.uniform(-1, 1, (400, 6))


def grain(sc, c, a=0.0, L=0.32, col=RICE, w=2, tilt=0.0):
    """Grain de riz : ellipse allongée dans un plan vertical tourné de a."""
    c = np.asarray(c, float)
    th = np.linspace(0, 2 * math.pi, 14, endpoint=False)
    ca, sa = math.cos(a), math.sin(a)
    P = []
    for q in th:
        x, y = L / 2 * math.cos(q), L / 5 * math.sin(q)
        y2 = y + x * tilt
        P.append(c + [x * ca, y2, x * sa])
    sc.add(P, col, w, closed=True)


def wall(sc, x0, x1, h=3.0, th=1.6, z=0.0, col=GOLD, courses=10, b=1.0, mortar=None, crenel=True):
    """Rempart rectiligne le long de x : briques, joints, créneaux."""
    L = x1 - x0; cx = (x0 + x1) / 2
    sc.box([cx, h / 2, z], [L, h, th], col * b, 2)
    for k in range(1, courses):
        y = h * k / courses
        mc = (mortar if mortar is not None else col * 0.4) * b
        sc.seg([x0, y, z + th / 2], [x1, y, z + th / 2], mc, 1)
        nb = int(L / 0.8)
        for j in range(nb):
            x = x0 + (j + 0.5 * (k % 2)) * L / nb
            if x0 < x < x1:
                sc.seg([x, y, z + th / 2], [x, y + h / courses, z + th / 2], col * 0.3 * b, 1)
    if crenel:
        n = int(L / 0.9)
        for j in range(n):
            if j % 2 == 0:
                x = x0 + (j + 0.5) * L / n
                sc.box([x, h + 0.25, z + th / 2 - 0.15], [L / n, 0.5, 0.3], col * b, 2)


def tower(sc, c, s=2.6, h=4.2, col=GOLD, b=1.0):
    c = np.asarray(c, float)
    sc.box(c + [0, h / 2, 0], [s, h, s], col * b, 2, grid=3)
    for k in range(4):
        for sx in (-1, 1):
            sc.box(c + [sx * s / 2 * 0.75, h + 0.25, (k - 1.5) * s / 4], [0.25, 0.5, 0.4], col * b, 1)
    sc.box(c + [0, h * 0.6, s / 2], [0.5, 0.8, 0.02], WHITE * 0.5 * b, 1)


def brick_stack(sc, c=(0, 0, 0), nx=4, ny=5, bw=1.2, bh=0.45, bd=0.6, col=GOLD, mortar=RICE, glow_m=1.0, b=1.0):
    c = np.asarray(c, float)
    for j in range(ny):
        off = 0.5 * bw * (j % 2)
        for i in range(nx):
            x = (i - nx / 2 + 0.5) * (bw + 0.08) + off - bw / 4
            sc.box(c + [x, j * (bh + 0.08) + bh / 2, 0], [bw, bh, bd], col * b, 2)
        y = j * (bh + 0.08) - 0.04
        if j > 0:
            sc.seg(c + [-nx / 2 * bw, y, bd / 2 + 0.01], c + [nx / 2 * bw + bw / 2, y, bd / 2 + 0.01], mortar * glow_m * b, 2)


def pot(sc, c=(0, 0, 0), r=1.4, h=1.6, col=COPPER, b=1.0):
    c = np.asarray(c, float)
    for k in range(7):
        y = h * k / 6
        rr = r * (0.82 + 0.18 * math.sin(math.pi * k / 6))
        sc.circle(c + [0, y, 0], rr, col * (1.0 if k in (0, 6) else 0.5) * b, 2 if k in (0, 6) else 1, 48)
    for a in np.linspace(0, 2 * math.pi, 16, endpoint=False):
        sc.add([c + [r * (0.82 + 0.18 * math.sin(math.pi * k / 6)) * math.cos(a), h * k / 6,
                     r * (0.82 + 0.18 * math.sin(math.pi * k / 6)) * math.sin(a)] for k in range(7)], col * 0.45 * b, 1)


def pagoda(sc, c=(0, 0, 0), levels=7, col=GOLD, b=1.0):
    c = np.asarray(c, float); y = 0.0
    for k in range(levels):
        s = 2.6 * (1 - 0.09 * k); hh = 1.1 * (1 - 0.05 * k)
        sc.box(c + [0, y + hh / 2, 0], [s, hh, s], col * b, 2)
        # toit débordant aux coins relevés
        e = s * 0.78
        corners = [c + [sx * e, y + hh + 0.05, sz * e] for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        tips = [p + [0, 0.25, 0] for p in corners]
        sc.add(tips, AMBER * b, 2, closed=True)
        for p in tips:
            sc.seg(p, c + [0, y + hh + 0.45, 0], AMBER * 0.6 * b, 1)
        y += hh + 0.45
    sc.seg(c + [0, y, 0], c + [0, y + 1.4, 0], WHITE * 0.8 * b, 2)
    for k in range(4):
        sc.circle(c + [0, y + 0.3 + 0.25 * k, 0], 0.18, WHITE * 0.6 * b, 1, 16)


def terrain(x):
    return 3.2 * math.sin(0.11 * x) + 1.8 * math.sin(0.27 * x + 1.0) + 0.8 * math.sin(0.6 * x)


def wall_path(s):
    return np.array([s, terrain(s) + 4.0, 6.0 * math.sin(0.08 * s)])


def great_wall(sc, s0=-40, s1=40, b=1.0, col=GOLD, ridges=True):
    ss = np.linspace(s0, s1, 160)
    P = np.array([wall_path(s) for s in ss])
    for dz in (-0.7, 0.7):
        sc.add(P + [0, 1.0, dz], col * b, 2)
        sc.add(P + [0, -1.2, dz], col * 0.45 * b, 1)
    for i in range(0, len(P), 4):
        for dz in (-0.7, 0.7):
            sc.seg(P[i] + [0, -1.2, dz], P[i] + [0, 1.0, dz], col * 0.35 * b, 1)
        sc.seg(P[i] + [0, 1.0, -0.7], P[i] + [0, 1.0, 0.7], col * 0.3 * b, 1)
        if i % 8 == 0:
            sc.box(P[i] + [0, 1.25, 0.75], [0.3, 0.5, 0.15], col * b, 1)
    for s in np.arange(s0 + 5, s1, 13):
        tower(sc, wall_path(s) + [0, -1.0, 0], s=2.0, h=3.0, col=col, b=b)
    if ridges:
        for zr, k in ((-9, 0.55), (-18, 0.35), (12, 0.3)):
            Q = [[x, 0.9 * terrain(x * 0.9 + zr) + 3.2 - 0.04 * abs(zr), zr + 3 * math.sin(0.05 * x)] for x in np.linspace(s0 - 10, s1 + 10, 90)]
            sc.add(Q, AMBER * k * b, 1)


def hexprism(sc, c, r, h, col, w=1, a=0.0):
    c = np.asarray(c, float)
    th = [a + k * math.pi / 3 for k in range(6)]
    B = [c + [r * math.cos(q), -h / 2, r * math.sin(q)] for q in th]
    T = [c + [r * math.cos(q), h / 2, r * math.sin(q)] for q in th]
    sc.add(B, col, w, closed=True); sc.add(T, col, w, closed=True)
    for p, q in zip(B, T): sc.seg(p, q, col * 0.7, 1)


def amylo(sc, c, s=1.0, depth=4, col=RICE, b=1.0, grow=1.0, seed=0):
    """Amylopectine stylisée : chaîne de glucoses (hexagones) très ramifiée."""
    rng = np.random.default_rng(seed)
    nodes = []

    def branch(p, d, lev):
        n = 6 - lev
        for k in range(n):
            if len(nodes) > 220 * grow: return
            q = p + d * 0.42 * s
            nodes.append((p.copy(), q.copy(), lev))
            p = q
            if lev < depth and k % 2 == 1:
                ang = rng.uniform(0.6, 1.1) * (1 if rng.random() < 0.5 else -1)
                ca, sa = math.cos(ang), math.sin(ang)
                d2 = np.array([d[0] * ca - d[1] * sa, d[0] * sa + d[1] * ca, rng.uniform(-0.4, 0.4)])
                branch(p.copy(), d2 / np.linalg.norm(d2), lev + 1)
            d = d + rng.uniform(-0.15, 0.15, 3) * [1, 1, 0.5]; d /= np.linalg.norm(d)

    branch(np.asarray(c, float), np.array([0, 1.0, 0]), 0)
    N = int(len(nodes) * min(1.0, grow))
    for p, q, lev in nodes[:N]:
        sc.seg(p, q, col * (1.0 - 0.12 * lev) * b, 2 if lev < 2 else 1)
        th = np.linspace(0, 2 * math.pi, 7)
        sc.add([q + [0.09 * s * math.cos(a), 0.09 * s * math.sin(a), 0] for a in th], AMBER * 0.9 * b, 1)


# ------------------------------------------------------------------ plans
def sh_hook_wall(img, u, t, v, T):
    """Rempart de briques en travelling ; les joints s'illuminent en blanc crème."""
    sc = Scene()
    m = RICE * (0.4 + 0.8 * ease(u * 1.4))
    wall(sc, -9, 9, h=4.0, th=2.0, courses=12, mortar=m)
    tower(sc, [-9, 0, 0], s=3.0, h=5.6); tower(sc, [9, 0, 0], s=3.0, h=5.6)
    sc.grid_plane(14, 20, 0, GOLD * 0.07)
    tgt = [lerp(-3, 2, u)[()], 2.4, 1.0]
    cam = look_at(*orbit(tgt, lerp(12, 8, ease(u)), 0.45 - 0.3 * u + 0.25 * v, 0.2))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(6, 40))


def sh_hook_rice(img, u, t, v, T):
    """Plongée dans un joint : grains de riz entre deux briques."""
    sc = Scene()
    sc.box([0, 1.0, 0], [5.0, 1.6, 2.2], GOLD, 2, grid=4)
    sc.box([0, -1.0, 0], [5.0, 1.6, 2.2], GOLD, 2, grid=4)
    sc.add([[-2.5, 0.2, 1.1], [2.5, 0.2, 1.1], [2.5, -0.2, 1.1], [-2.5, -0.2, 1.1]], LIME * 0.6, 1, closed=True)
    for g in GR[:40]:
        grain(sc, [g[0] * 2.3, g[1] * 0.12, 1.1 + 0.05 * g[2]], a=g[3] * 0.5, L=0.3, col=RICE * (0.7 + 0.3 * abs(math.sin(2 * t + g[4] * 3))), tilt=g[5] * 0.3)
    cam = look_at(*orbit([0, 0, 1.0], lerp(8, 3.2, ease(u)), 0.25 * math.sin(0.5 * T), 0.08))
    draw(img, sc, cam, fade=(2, 14))


def sh_rice_pot(img, u, t, v, T):
    """Marmite : la soupe de riz gluant, versée vers un bac de chaux."""
    sc = Scene()
    if v % 2 == 0:
        pot(sc, [0, 0, 0], r=1.5, h=1.8)
        for k in range(3):
            sc.circle([0, 1.5 + 0.03 * math.sin(3 * t + k), 0], 1.2 - 0.35 * k, RICE * 0.5, 1, 40)
        for g in GR[:50]:
            rr = 1.1 * abs(g[0])
            grain(sc, [rr * math.cos(g[1] * 3 + 0.4 * t), 1.52 + 0.05 * g[2], rr * math.sin(g[1] * 3 + 0.4 * t)], a=g[3] * 3, L=0.22)
        for k in range(5):  # vapeur
            y0 = (t * 0.7 + k * 0.6) % 3.0
            sc.add([[0.3 * (k - 2) + 0.15 * math.sin(2 * y + k), 1.9 + y, 0] for y in np.linspace(y0, y0 + 0.8, 8)], WHITE * 0.35 * (1 - y0 / 3), 1)
        cam = look_at(*orbit([0, 1.2, 0], lerp(7.5, 6.0, ease(u)), 0.4 + 0.4 * u, 0.45))
    else:
        # bac de chaux qui reçoit le filet de soupe
        sc.box([0, 0.5, 0], [4.0, 1.0, 2.6], LIME, 2, grid=4)
        sc.grid_plane(3, 10, 0.98, LIME * 0.3)
        f = ease(u * 1.3)
        sc.add([[-1.8 + 0.6 * s, 3.4 - 2.4 * s * s, 0] for s in np.linspace(0, f, 12)], RICE, 3)
        pot(sc, [-2.6, 3.0, 0], r=0.8, h=0.9, col=COPPER)
        for k in range(int(30 * f)):
            g = GR[k]
            grain(sc, [g[0] * 1.6, 1.02, g[1] * 1.1], a=g[2] * 3, L=0.2, col=RICE * 0.9)
        cam = look_at(*orbit([-0.4, 1.4, 0], 9.0, 0.5 + 0.3 * u, 0.35))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 20))


def sh_ratio(img, u, t, v, T):
    """1 cube de riz face à 20 cubes de chaux."""
    sc = Scene(); n = int(20 * ease(u * 1.5))
    sc.box([-3.0, 0.5, 0], [1, 1, 1], RICE * 1.2, 3, grid=2)
    for k in range(12):
        g = GR[k]; grain(sc, [-3.0 + g[0] * 0.35, 1.05, g[1] * 0.35], a=g[2] * 3, L=0.2)
    for k in range(n):
        i, j = k % 5, k // 5
        sc.box([0.2 + i * 1.15, 0.5 + j * 1.15, 0], [1, 1, 1], LIME * 0.9, 2)
    sc.grid_plane(8, 16, 0, GOLD * 0.08)
    cam = look_at(*orbit([1.4, 2.2, 0], lerp(13, 11, ease(u)), 0.45 - 0.25 * u, 0.25))
    draw(img, sc, cam, fade=(4, 26))


def sh_composite(img, u, t, v, T):
    """Coupe : briques + joint mêlant grains (organique) et cristaux (minéral)."""
    sc = Scene()
    brick_stack(sc, c=(0, -1.6, 0), nx=4, ny=6, mortar=RICE, glow_m=0.6 + 0.6 * abs(math.sin(2 * t)))
    # zoom inséré : cercle loupe
    c = np.array([0.6, 0.9, 1.2])
    sc.circle(c, 1.5, WHITE * 0.7, 2, 60, axis="z")
    for g in GR[50:80]:
        if g[0] ** 2 + g[1] ** 2 < 0.8:
            if g[2] > 0:
                grain(sc, c + [g[0] * 1.3, g[1] * 1.3, 0.01], a=0, L=0.28, tilt=g[3])
            else:
                sc.add([c + [g[0] * 1.3 + 0.12 * math.cos(q), g[1] * 1.3 + 0.12 * math.sin(q), 0.01] for q in np.arange(6) * math.pi / 3], LIME, 1, closed=True)
    cam = look_at(*orbit([0.3, 0.3, 0], lerp(10, 8.5, ease(u)), 0.25 * math.sin(0.4 * T) + 0.15 * v, 0.12))
    draw(img, sc, cam, fade=(4, 24))


def sh_pagoda(img, u, t, v, T):
    sc = Scene(); pagoda(sc); sc.grid_plane(8, 16, 0, GOLD * 0.08)
    cam = look_at(*orbit([0, 4.5, 0], lerp(17, 15, ease(u)), 0.6 + 0.6 * u, lerp(0.05, 0.22, u)))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(8, 36))


def sh_nanjing(img, u, t, v, T):
    """Rempart de Nankin : porte voûtée et longue enceinte."""
    sc = Scene()
    wall(sc, -18, -3, h=5.0, th=3.0, courses=12)
    wall(sc, 3, 18, h=5.0, th=3.0, courses=12)
    sc.box([0, 3.0, 0], [6, 6.0, 4.0], GOLD, 2, grid=3)
    sc.add([[-1.4, 0, 2.01]] + [[1.4 * math.cos(a), 2.4 + 1.4 * math.sin(a), 2.01] for a in np.linspace(math.pi, 0, 14)] + [[1.4, 0, 2.01]], AMBER, 2)
    sc.box([0, 7.0, 0], [5.0, 2.0, 3.0], AMBER * 0.9, 2)
    sc.add([[-3.2, 8.0, -2.0], [3.2, 8.0, -2.0], [3.2, 8.0, 2.0], [-3.2, 8.0, 2.0]], AMBER, 2, closed=True)
    sc.seg([-3.2, 8.0, 0], [3.2, 8.0, 0], AMBER * 0.5, 1); sc.seg([-2.0, 8.7, 0], [2.0, 8.7, 0], AMBER, 2)
    for sx in (-1, 1):
        for sz in (-1, 1): sc.seg([sx * 3.2, 8.0, sz * 2.0], [sx * 2.0, 8.7, 0], AMBER * 0.8, 1)
    sc.grid_plane(22, 22, 0, GOLD * 0.07)
    cam = look_at(*orbit([0, 3.5, 0], lerp(19, 15, ease(u)), -0.4 + 0.4 * u + 0.3 * v, 0.18))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(10, 50))


def sh_bulldozer(img, u, t, v, T):
    """Un bulldozer pousse contre un tombeau : rien ne bouge."""
    sc = Scene()
    sc.box([2.5, 1.5, 0], [4.0, 3.0, 4.0], GOLD, 2, grid=5)  # tombeau
    for k in range(4):
        sc.circle([2.5, 3.0 + 0.3 * k, 0], 2.3 - 0.55 * k, GOLD * 0.7, 1, 40)
    j = 0.08 * math.sin(40 * t) * (u > 0.3)
    x0 = lerp(-6.5, -2.3, ease(u * 2.5))[()] + j
    # lame
    sc.box([x0 + 2.0, 0.9, 0], [0.2, 1.8, 3.6], COPPER, 2)
    # corps et cabine
    sc.box([x0, 1.1, 0], [3.0, 1.4, 2.2], AMBER, 2)
    sc.box([x0 - 0.5, 2.5, 0], [1.6, 1.4, 1.8], AMBER, 2)
    for dz in (-1.3, 1.3):  # chenilles
        sc.add([[x0 - 1.6, 0.0, dz], [x0 + 1.5, 0.0, dz], [x0 + 1.8, 0.45, dz], [x0 + 1.5, 0.9, dz], [x0 - 1.6, 0.9, dz], [x0 - 1.9, 0.45, dz]], GOLD * 0.8, 2, closed=True)
        for k in range(6):
            sc.circle([x0 - 1.3 + 0.55 * k, 0.45, dz], 0.25, GOLD * 0.4, 1, 10, axis="z")
    sc.seg([x0 + 1.0, 1.4, 1.2], [x0 + 2.0, 0.8, 1.6], COPPER * 0.7, 2); sc.seg([x0 + 1.0, 1.4, -1.2], [x0 + 2.0, 0.8, -1.6], COPPER * 0.7, 2)
    if u > 0.35:  # étincelles d'impact
        for k in range(8):
            a = 2 * math.pi * k / 8 + 3 * t
            p = np.array([0.4, 1.2, 0])
            sc.seg(p, p + [-0.4 * abs(math.cos(a)), 0.6 * math.sin(a), 0.6 * math.cos(a)], WHITE * 0.7, 1)
    sc.grid_plane(9, 18, 0, GOLD * 0.08)
    cam = look_at(*orbit([0, 1.4, 0], lerp(12.0, 10.5, ease(u)), 0.15 + 0.2 * u + 0.35 * (v % 2), 0.25))
    draw(img, sc, cam, fade=(5, 30))


def sh_quake(img, u, t, v, T):
    """Ondes sismiques ; la pagode et le rempart vibrent mais tiennent."""
    sc = Scene()
    sh = 0.12 * math.sin(25 * t) * (0.5 + 0.5 * math.sin(3 * t))
    pagoda(sc, c=(sh, 0, -1.0))
    wall(sc, -9 + sh, -3 + sh, h=3.0, th=1.6, z=2.0, courses=8)
    wall(sc, 3 + sh, 9 + sh, h=3.0, th=1.6, z=2.0, courses=8)
    for k in range(5):
        r = ((t * 4 + k * 3) % 16)
        sc.circle([0, 0.02, 0], r, RED * 0.8 * (1 - r / 16), 2, 72)
    for k in range(-10, 11):
        x = k * 1.0
        sc.seg([x, 0, -10 + 0.0], [x, 0, 10], GOLD * 0.06, 1)
    cam = look_at(*orbit([0, 3.5, 0], 21, 0.5 + 0.35 * u, 0.28 + 0.1 * v))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(8, 40))


def sh_molecule(img, u, t, v, T):
    sc = Scene()
    amylo(sc, [0, -2.2, 0], s=1.0, depth=4, grow=ease(u * 1.4) * 1.0 + 0.05)
    cam = look_at(*orbit([0, 0.2, 0], lerp(8.0, 6.5, ease(u)), 0.5 * math.sin(0.4 * T), 0.05))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(4, 20))


def sh_crystals_big(img, u, t, v, T):
    """Chaux seule : quelques gros cristaux désordonnés, avec des vides."""
    sc = Scene()
    for k in range(14):
        g = GR[100 + k]
        h = 1.5 + 2.0 * abs(g[0]) * ease(u * 1.5 + 0.2)
        hexprism(sc, [g[1] * 3.0, h / 2 - 2.0, g[2] * 2.0], 0.4 + 0.3 * abs(g[3]), h, LIME, 2, a=g[4])
    sc.box([0, 0, 0], [7, 4.2, 4.6], WHITE * 0.25, 1)
    cam = look_at(*orbit([0, 0, 0], 11, 0.4 + 0.5 * u, 0.25))
    draw(img, sc, cam, fade=(4, 22))


def sh_crystals_small(img, u, t, v, T):
    """Avec l'amylopectine : une multitude de petits cristaux serrés."""
    sc = Scene()
    n = int(lerp(60, 260, ease(u * 1.6))[()])
    for k in range(n):
        g = GR[k]
        hexprism(sc, [g[0] * 3.3, g[1] * 1.9, g[2] * 2.1], 0.12, 0.3, LIME * 0.9, 1, a=g[3])
    for k in range(10):
        g = GR[300 + k]
        P = [[g[0] * 3 + 0.4 * s, g[1] * 1.8 + 0.25 * math.sin(4 * s + k), g[2] * 2] for s in np.linspace(-1.2, 1.2, 12)]
        sc.add(P, RICE * 0.8, 1)
    sc.box([0, 0, 0], [7, 4.2, 4.6], WHITE * (0.35 + 0.35 * ease(u)), 2)
    cam = look_at(*orbit([0, 0, 0], lerp(11, 9.5, ease(u)), 0.8 + 0.4 * u + 0.4 * v, 0.25))
    draw(img, sc, cam, fade=(4, 22))


def sh_iodine(img, u, t, v, T):
    """Goutte d'iode sur un fragment de mortier : la tache vire au violet."""
    sc = Scene()
    P = [[-1.8, 0, -1.0], [-0.6, 0, -1.6], [1.4, 0, -1.3], [2.0, 0, 0.2], [1.0, 0, 1.4], [-1.2, 0, 1.2], [-2.1, 0, 0.1]]
    sc.add(P, LIME, 2, closed=True)
    sc.add([np.array(p) + [0, 0.8, 0] for p in P], LIME, 2, closed=True)
    for p in P: sc.seg(p, np.array(p) + [0, 0.8, 0], LIME * 0.6, 1)
    for g in GR[200:230]:
        grain(sc, [g[0] * 1.4, 0.81, g[1] * 0.9], a=g[2] * 3, L=0.18, col=RICE * 0.6)
    fall = ease(u * 2.2)
    yd = lerp(4.5, 0.85, fall)[()]
    if fall < 0.999:
        sc.add([[0.25 * math.sin(a) * (1 - 0.6 * (a > math.pi)), yd + 0.35 * math.cos(a), 0] for a in np.linspace(0, 2 * math.pi, 20)], COPPER, 2, closed=True)
    sc.seg([0, 5.6, 0], [0, 4.9, 0], WHITE * 0.5, 2)
    sc.box([0, 6.3, 0], [0.4, 1.4, 0.4], WHITE * 0.5, 1)
    sp = ease((u - 0.42) * 2.2)
    if sp > 0:
        col = lerp(COPPER, VIOLET, ease((u - 0.5) * 2.5))
        for k in range(4):
            sc.circle([0, 0.82, 0], (0.25 + 0.35 * k) * sp, col * (1.3 - 0.25 * k), 2, 40)
    cam = look_at(*orbit([0, 1.2, 0], lerp(6.0, 4.8, ease(u)), 0.4 + 0.3 * u, 0.5))
    draw(img, sc, cam, fade=(3, 16))


def sh_bridge(img, u, t, v, T):
    """Pont de pierre en arc, au-dessus de l'eau."""
    sc = Scene()
    R = 5.0
    for dz in (-1.5, 1.5):
        sc.add([[R * math.cos(a), R * math.sin(a) - 1.0, dz] for a in np.linspace(0, math.pi, 30)], GOLD, 2)
        sc.add([[(R + 0.9) * math.cos(a), (R + 0.9) * math.sin(a) - 1.0, dz] for a in np.linspace(0, math.pi, 30)], GOLD * 0.6, 1)
        for a in np.linspace(0, math.pi, 17):
            sc.seg([R * math.cos(a), R * math.sin(a) - 1.0, dz], [(R + 0.9) * math.cos(a), (R + 0.9) * math.sin(a) - 1.0, dz], GOLD * 0.45, 1)
        sc.add([[-9, 0.2, dz], [-5.5, 0.2, dz], [-2, 4.9, dz], [2, 4.9, dz], [5.5, 0.2, dz], [9, 0.2, dz]], AMBER, 2)
        for x in np.linspace(-8, 8, 17):
            yy = 4.9 if abs(x) < 2 else max(0.2, 4.9 - (abs(x) - 2) * 4.7 / 3.5)
            sc.seg([x, yy, dz], [x, yy + 0.7, dz], AMBER * 0.6, 1)
        sc.add([[-9, 0.9, dz], [-5.5, 0.9, dz], [-2, 5.6, dz], [2, 5.6, dz], [5.5, 0.9, dz], [9, 0.9, dz]], AMBER * 0.8, 1)
    sc.add([[-2, 4.9, -1.5], [2, 4.9, -1.5], [2, 4.9, 1.5], [-2, 4.9, 1.5]], AMBER * 0.5, 1, closed=True)
    for k in range(9):  # eau
        z = -6 + 1.5 * k
        sc.add([[x, -1.0 + 0.08 * math.sin(0.8 * x + 2 * t + k), z] for x in np.linspace(-12, 12, 40)], np.array([0.95, 0.55, 0.2]) * 0.35, 1)
    cam = look_at(*orbit([0, 2.0, 0], lerp(16, 13, ease(u)), 0.45 + 0.35 * u, 0.12))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(8, 40))


def sh_great_wall(img, u, t, v, T):
    sc = Scene(); great_wall(sc)
    s = lerp(-30, -5, ease(u))[()] + 12 * v
    p = wall_path(s)
    cam = look_at(p + [-4, 5.5 + 2 * v, 12], p + [9, 0, 0])
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(6, 50))


def sh_wall_scan(img, u, t, v, T):
    """Un tronçon de la muraille passé au scanner ; points d'échantillons et point d'interrogation."""
    sc = Scene(); great_wall(sc, -14, 14, b=0.8, ridges=False)
    y = lerp(-1, 9, (u * 1.5) % 1.0)[()]
    sc.add([[-14, y, -3], [14, y, -3], [14, y, 3], [-14, y, 3]], WHITE * 0.5, 1, closed=True)
    for k in range(8):
        s = -12 + 3.4 * k
        p = wall_path(s) + [0, 0.2, 0.8]
        on = (u * 8 > k)
        if on:
            sc.circle(p, 0.35 + 0.08 * math.sin(4 * t + k), RED, 2, 20, axis="z")
    q = 0.4 + 0.6 * abs(math.sin(2.5 * t))
    c = wall_path(0) + [0, 5.0, 1.0]
    sc.add([c + [1.0 * math.cos(a), 1.0 * math.sin(a) + 1.0, 0] for a in np.linspace(2.6, -1.2, 16)] + [c + [0, 0.5, 0], c + [0, -0.2, 0]], WHITE * q, 4)
    sc.seg(c + [0, -0.7, 0], c + [0, -0.95, 0], WHITE * q, 6)
    cam = look_at(*orbit(wall_path(0) + [0, 1.5, 0], lerp(20, 16, ease(u)), 0.15 * math.sin(0.3 * T), 0.22))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(10, 50))


def sh_final_wall(img, u, t, v, T):
    """Retour au rempart, les joints de riz qui luisent ; la caméra s'éloigne sur la muraille."""
    sc = Scene(); great_wall(sc, -45, 45, b=lerp(1.0, 0.6, ease(u))[()])
    m = 0.5 + 0.5 * abs(math.sin(1.5 * t))
    ss = np.linspace(-45, 45, 160)
    P = np.array([wall_path(s) for s in ss])
    sc.add(P + [0, -0.1, 0.72], RICE * m, 1)
    cam = look_at(*orbit(wall_path(0), lerp(22, 60, ease(u)), 0.3 + 0.3 * u, lerp(0.25, 0.45, u)))
    stars(img, cam, T, 1.0); draw(img, sc, cam, fade=(10, 90))
