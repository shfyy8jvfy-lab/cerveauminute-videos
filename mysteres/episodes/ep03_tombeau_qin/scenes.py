# Plans propres à l'épisode 3 : le tombeau du premier empereur de Chine
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

MERC = np.array([0.98, 0.90, 0.78])     # BGR : argent bleuté du mercure
RED = np.array([0.25, 0.30, 1.00])
CLAY = np.array([0.30, 0.50, 0.85])


def mound(sc, col=GOLD, c=(0, 0, 0), half=1.6, courses=9):
    sc.pyramid(half=half, h=1.6, courses=courses, col=col, top=0.45, joints=False, c=c)


def rising(sc, t, n=60, r=1.6, h=2.6, col=MERC, seed=2, y0=0.2):
    rng = np.random.default_rng(seed)
    for k in range(n):
        x, z, ph = rng.uniform(-r, r) * 0.6, rng.uniform(-r, r) * 0.6, rng.uniform(0, h)
        y = y0 + ((t * 0.35 + ph) % h)
        a = 1 - (y - y0) / h
        sc.circle([x + 0.08 * math.sin(t + k), y, z], 0.025, col * (0.3 + 0.7 * a), 1, 8, axis="z")


def chamber(sc, col, c=(0, -1.2, 0), size=(1.6, 0.35, 1.0)):
    sc.box(c, size, col, 2, grid=4)


def figure(sc, p, s, col, w=1, arms=0.0):
    p = np.asarray(p, float)
    hip = p + [0, 0.45 * s, 0]; neck = p + [0, 0.85 * s, 0]
    sc.seg(p + [-0.12 * s, 0, 0], hip, col, w); sc.seg(p + [0.12 * s, 0, 0], hip, col, w)
    sc.seg(hip, neck, col, w)
    sc.seg(neck, neck + [-0.2 * s, -0.3 * s + arms * s, 0.05 * s], col, w)
    sc.seg(neck, neck + [0.2 * s, -0.3 * s, 0.05 * s], col, w)
    sc.circle(neck + [0, 0.11 * s, 0], 0.09 * s, col, w, 10, axis="z")


def river(sc, pts_xz, t, y, col, w=2, speed=0.5, dash=0.35):
    P = np.array(pts_xz, float)
    # interpolation lisse
    k = np.linspace(0, len(P) - 1, 120)
    X = np.interp(k, np.arange(len(P)), P[:, 0]); Z = np.interp(k, np.arange(len(P)), P[:, 1])
    L = np.concatenate([[0], np.cumsum(np.hypot(np.diff(X), np.diff(Z)))])
    sc.add(np.stack([X, np.full_like(X, y), Z], 1), col * 0.35, 1)
    ph = (L / dash - t * speed / dash * 3) % 1.0
    for i in range(len(X) - 1):
        if ph[i] < 0.55:
            sc.seg([X[i], y + 0.005, Z[i]], [X[i + 1], y + 0.005, Z[i + 1]], col, w)


YELLOW_R = [(-1.6, -0.2), (-1.0, -0.8), (-0.4, -0.95), (0.0, -0.5), (0.3, -0.7), (0.8, -0.6), (1.3, -0.35)]
YANGZI_R = [(-1.6, 0.6), (-1.0, 0.3), (-0.5, 0.55), (0.0, 0.4), (0.5, 0.7), (1.0, 0.55), (1.3, 0.6)]


def sh_hook_mound(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(4, 16, 0, GOLD * 0.15)
    mound(sc, GOLD * lerp(1.0, 0.6, ease(u))[()])
    chamber(sc, MERC * (0.25 + 0.6 * ease(u)))
    rising(sc, t, 50)
    if v == 0:
        cam = look_at(*orbit([0, 0.2, 0], lerp(6.2, 4.6, ease(u)), 0.6 + 0.3 * u, 0.22))
    else:
        cam = look_at(*orbit([0, -0.4, 0], lerp(4.6, 3.8, ease(u)), 1.2 + 0.3 * u, 0.12))
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(2, 14))


def sh_context_map(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(4, 20, 0, GOLD * 0.12)
    mound(sc, GOLD, half=0.55, courses=5, c=(0, 0, 0.3))
    # enceintes intérieure et extérieure
    sc.box([0, 0.05, 0.2], [1.6, 0.1, 2.6], AMBER * 0.8, 2)
    sc.box([0, 0.05, 0.0], [2.2, 0.1, 4.6], AMBER * 0.5, 2)
    # repère « 13 ans » : marqueur pulsant
    r = 0.8 + 0.25 * math.sin(t * 3)
    sc.circle([0, 0.02, 0.3], r, WHITE * 0.7, 2, 64)
    if v == 0:
        cam = look_at(*orbit([0, 0, 0.1], lerp(7.0, 5.6, ease(u)), 0.2 + 0.4 * u, lerp(1.25, 0.95, ease(u))))
    else:
        cam = look_at(*orbit([0, 0.2, 0.2], lerp(5.0, 4.2, u), -0.5 + 0.4 * u, 0.45))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 14))


def sh_workers(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(4, 16, 0, GOLD * 0.12)
    mound(sc, GOLD * 0.8, c=(0, 0, -2.2), half=1.2, courses=7)
    n = int(lerp(40, 260, ease((u + v) / 1.5)))
    rng = np.random.default_rng(11)
    for k in range(n):
        x = rng.uniform(-2.4, 2.4); z = rng.uniform(-0.6, 2.4)
        z = z - ((t * 0.15 + k * 0.01) % 0.5)
        figure(sc, [x, 0, z], 0.28, AMBER * rng.uniform(0.6, 1.0), 1, arms=0.5 * math.sin(t * 4 + k))
    cam = look_at(*orbit([0, 0.4, -0.2], lerp(5.0, 4.3, u), 0.3 * (v - 0.5) + 0.2 * u, 0.32 + 0.1 * v))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 12))


def sh_army_pit(img, u, t, v, T):
    sc = Scene()
    reveal = ease(u * 1.4 + 0.15 * v)
    for row in range(5):
        x = -1.6 + row * 0.8
        sc.box([x, -0.25, 0], [0.62, 0.5, 8.0], GOLD * 0.35, 1)
        for k in range(16):
            z = -3.6 + k * 0.48
            if (k / 16) > reveal + 0.05: continue
            for col_ in (-0.15, 0.15):
                figure(sc, [x + col_, -0.5, z], 0.42, CLAY if (row + k) % 3 else GOLD, 2)
    if v == 0:
        cam = look_at(*orbit([0, -0.2, 0], 6.5 - 0.8 * u, 0.15 + 0.15 * u, 0.45))
    elif v == 1:
        eye = [lerp(-1.2, -0.6, u)[()], 1.3, lerp(3.2, 1.6, u)[()]]
        cam = look_at(eye, [-0.4, -0.4, -1.2])
    else:
        cam = look_at(*orbit([0.0, -0.3, 0], 4.2, 0.9 + 0.3 * u, 0.35))
    draw(img, sc, cam, fade=(1, 12))


def sh_mercury_rivers(img, u, t, v, T):
    sc = Scene()
    sc.box([0, 0.35, 0], [3.4, 0.9, 2.4], GOLD * 0.35, 1)
    river(sc, YELLOW_R, t, -0.1, MERC, 3)
    river(sc, YANGZI_R, t, -0.1, MERC, 3, speed=0.4)
    for z in np.linspace(-0.9, 0.9, 7):   # affluents
        river(sc, [(-1.5, z), (-0.8, z * 0.7 + 0.1), (-0.2, z * 0.5)], t, -0.1, MERC * 0.6, 1, speed=0.3)
    for k in range(8):  # la mer, à l'est
        xs = np.linspace(-1.2, 1.2, 30)
        sc.add(np.stack([np.full_like(xs, 1.35 + 0.04 * np.sin(xs * 6 + t * 2 + k)) + k * 0.03,
                         np.full_like(xs, -0.1), xs], 1), MERC * 0.7, 1)
    sc.grid_plane(1.7, 10, -0.1, GOLD * 0.1)
    if v == 0:
        cam = look_at(*orbit([0, -0.1, 0], lerp(5.2, 4.2, u), 0.3 + 0.3 * u, 0.85))
    elif v == 1:
        cam = look_at(*orbit([-0.3, -0.1, 0], lerp(3.4, 2.8, u), -0.6 + 0.3 * u, 0.5))
    else:
        cam = look_at(*orbit([0.6, -0.1, 0], lerp(3.6, 3.0, u), 1.2 + 0.2 * u, 0.6))
    draw(img, sc, cam, fade=(1, 9))


def crossbow(sc, p, aim, col):
    p = np.asarray(p, float); d = np.asarray(aim, float) - p; d /= np.linalg.norm(d)
    side = np.cross(d, [0, 1, 0]); side /= np.linalg.norm(side) + 1e-9
    sc.seg(p - d * 0.25, p + d * 0.25, col, 2)
    tip = p + d * 0.18
    arc = [tip + side * 0.28 * s - d * 0.1 * s * s for s in np.linspace(-1, 1, 9)]
    sc.add(arc, col, 2)
    sc.seg(arc[0], p - d * 0.05, col * 0.6, 1); sc.seg(arc[-1], p - d * 0.05, col * 0.6, 1)


def sh_ceiling_crossbows(img, u, t, v, T):
    sc = Scene()
    rng = np.random.default_rng(5)
    pts = []
    for k in range(70):  # voûte étoilée
        a, e = rng.uniform(0, 2 * math.pi), rng.uniform(0.25, 1.3)
        p = np.array([1.9 * math.cos(e) * math.cos(a), 1.9 * math.sin(e), 1.9 * math.cos(e) * math.sin(a)])
        pts.append(p); sc.circle(p, 0.025, WHITE, 1, 6, axis="z")
    for k in range(0, 60, 3):
        sc.seg(pts[k], pts[k + 1], GOLD * 0.6, 1); sc.seg(pts[k + 1], pts[k + 2], GOLD * 0.6, 1)
    for e in (0.0, 0.5, 1.0):
        sc.circle([0, 1.9 * math.sin(e), 0], 1.9 * math.cos(e), GOLD * 0.18, 1, 64)
    door = np.array([0, -0.4, 1.9])
    sc.box(door + [0, 0.3, 0], [0.7, 1.0, 0.05], AMBER, 2)
    for k, p in enumerate([[-1.3, -0.3, -0.6], [1.3, -0.3, -0.6], [-1.5, 0.2, 0.3], [1.5, 0.2, 0.3]]):
        crossbow(sc, p, door, RED * 0.9)
        f = ((t * 0.9 + k * 0.27) % 1.0)
        a = lerp(p, door, f); d = (door - np.array(p)); d /= np.linalg.norm(d)
        sc.seg(a, a + d * 0.3, WHITE, 2)
    sc.grid_plane(1.9, 12, -0.8, GOLD * 0.12)
    if v == 0:
        cam = look_at(*orbit([0, 0.2, 0], lerp(4.4, 3.8, u), -0.4 + 0.3 * u, 0.35))
    else:
        cam = look_at(*orbit([0, 0.1, 0], lerp(4.4, 3.8, u), 0.5 + 0.3 * u, 0.1))
    draw(img, sc, cam, fade=(1, 8))


def sh_sealed_gate(img, u, t, v, T):
    sc = Scene()
    for z in np.linspace(-3, 1, 9):  # couloir
        sc.add([[-0.7, -0.8, z], [-0.7, 0.6, z], [0.7, 0.6, z], [0.7, -0.8, z]], GOLD * 0.45, 1)
    for x in (-0.7, 0.7):
        for y in (-0.8, 0.6):
            sc.seg([x, y, -3], [x, y, 1], GOLD * 0.6, 1)
    fall = ease(min(1, (u + v) * 1.3))
    y0 = lerp(1.8, -0.1, fall)[()]
    sc.box([0, y0, 0.2], [1.5, 1.4, 0.12], AMBER, 3, grid=3)
    for k, x in enumerate([-0.35, 0.0, 0.35]):
        figure(sc, [x, -0.8, -1.0 - 0.3 * k], 0.7, CLAY * (1 - 0.6 * fall), 2, arms=0.4)
    cam = look_at([0.25 * (v - 0.5), 0.0, 3.2 - 0.5 * u], [0, -0.2, -1.0])
    draw(img, sc, cam, fade=(1, 9))


def sh_soil_probe(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(3.5, 14, 0, GOLD * 0.12)
    mound(sc, GOLD * 0.55)
    rng = np.random.default_rng(9)
    n = int(40 * ease(u * 1.3 + 0.2 * v))
    for k in range(n):
        x, z = rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)
        hgt = 1.6 * (1 - max(abs(x), abs(z)) / 1.6)
        hgt = min(hgt, 0.72)
        conc = math.exp(-((x * x + z * z) / 1.2))
        col = lerp(GOLD * 0.6, MERC * 1.1, conc)
        sc.seg([x, hgt, z], [x, hgt + 0.15 + 0.9 * conc, z], col, 2)
        sc.circle([x, hgt + 0.15 + 0.9 * conc, z], 0.04, col, 1, 8, axis="z")
    cam = look_at(*orbit([0, 0.5, 0], lerp(5.0, 4.2, u), 0.5 + 0.6 * v + 0.2 * u, 0.35))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 12))


def sh_lidar(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(4, 16, 0, GOLD * 0.12)
    mound(sc, GOLD * 0.6)
    van = np.array([3.2, 0.25, 1.6])
    sc.box(van, [0.8, 0.45, 0.45], AMBER, 2)
    sc.box(van + [0, 0.32, 0], [0.25, 0.2, 0.25], AMBER, 1)
    ang = math.sin(t * 0.8) * 0.6
    tgt = np.array([0.3 * math.cos(ang * 2), 1.0 + 0.4 * math.sin(ang), 0.8 * math.sin(ang * 1.5)])
    sc.seg(van + [0, 0.42, 0], tgt + (tgt - van) * 0.4, RED, 3)
    rising(sc, t, 70, r=1.4, h=2.4, y0=0.75)
    if v == 0:
        cam = look_at(*orbit([1.0, 0.7, 0.4], lerp(6.4, 5.6, u), 0.9 + 0.2 * u, 0.22))
    else:
        cam = look_at(*orbit([0.3, 1.2, 0], lerp(5.0, 4.4, u), 0.2 + 0.3 * u, 0.12))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(2, 13))


def sh_chamber_scan(img, u, t, v, T):
    sc = Scene()
    # coupe du tertre (profil) + sol + chambre
    half, h = 1.6, 1.6
    prof = [[-half, 0, 0], [-half * 0.55, 0.72, 0], [half * 0.55, 0.72, 0], [half, 0, 0]]
    sc.add(prof, GOLD, 3)
    sc.seg([-3, 0, 0], [3, 0, 0], GOLD * 0.7, 2)
    for k in range(1, 6):
        sc.seg([-3, -0.35 * k, 0], [3, -0.35 * k, 0], GOLD * 0.12, 1)
    reveal = ease(u * 1.5 + 0.3 * v)
    sc.box([0, -1.35, 0], [1.6, 0.3, 1.0], MERC * reveal, 2, grid=4)
    # cotes
    if reveal > 0.3:
        sc.seg([-0.8, -1.65, 0.6], [0.8, -1.65, 0.6], WHITE * 0.8, 1)
        sc.seg([1.25, 0, 0], [1.25, -1.2, 0], WHITE * 0.8, 1)
        sc.seg([1.15, -1.2, 0], [1.35, -1.2, 0], WHITE * 0.8, 1)
    sy = 0.7 - 2.6 * ((t * 0.4) % 1.0)
    sc.seg([-2.2, sy, 0.02], [2.2, sy, 0.02], MERC * 0.5, 2)
    cam = look_at(*orbit([0, -0.55, 0], lerp(4.2, 3.6, u), 0.25 + 0.5 * v + 0.1 * u, 0.18))
    draw(img, sc, cam, fade=(2, 12))


def sh_warrior_paint(img, u, t, v, T):
    sc = Scene()
    s = 1.0
    sc.box([0, 0.75, 0], [0.7, 0.9, 0.38], CLAY, 2, grid=3)       # torse / armure
    sc.box([0, 0.2, 0], [0.62, 0.25, 0.36], CLAY * 0.8, 2)       # jupe
    for x in (-0.16, 0.16):
        sc.box([x, -0.3, 0], [0.18, 0.75, 0.2], CLAY * 0.7, 2)   # jambes
    for x in (-0.45, 0.45):
        sc.box([x, 0.75, 0.08], [0.16, 0.7, 0.18], CLAY * 0.8, 2) # bras
    for lat in np.linspace(-1.2, 1.2, 6):                         # tête
        sc.circle([0, 1.48 + 0.2 * math.sin(lat), 0], 0.2 * math.cos(lat), CLAY, 1, 24)
    sc.box([0, 1.73, -0.05], [0.18, 0.12, 0.18], CLAY, 1)         # chignon
    # écailles de peinture qui se détachent
    rng = np.random.default_rng(3)
    prog = ease(u * 1.1 + 0.4 * v)
    for k in range(70):
        p0 = np.array([rng.uniform(-0.38, 0.38), rng.uniform(0.1, 1.3), 0.21])
        st = rng.uniform(0, 0.8)
        f = max(0.0, prog - st) / 0.4
        col = [RED, GOLD, np.array([0.7, 0.55, 0.2])][k % 3]
        if f <= 0:
            sc.circle(p0, 0.035, col, 1, 6, axis="z")
        else:
            p = p0 + [0.25 * f * math.sin(k), -1.4 * f * f, 0.3 * f]
            if p[1] > -0.8:
                sc.add([p, p + [0.05, 0.02 * math.sin(t * 5 + k), 0.02], p + [0.02, -0.04, 0]], col * 0.9, 1, closed=True)
    sc.grid_plane(2, 8, -0.68, GOLD * 0.12)
    cam = look_at(*orbit([0, 0.5, 0], lerp(3.4, 2.8, u) - 0.3 * v, 0.35 * (v - 0.5) + 0.15 * u, 0.12))
    draw(img, sc, cam, fade=(1, 9))


def sh_final_mound(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(4.5, 18, 0, GOLD * 0.12)
    mound(sc, GOLD * 0.75)
    sc.box([0, -1.2, 0], [1.8, 0.4, 1.2], GOLD * 0.25, 1)
    sx = lambda P: [(x * 0.55, z * 0.5) for x, z in P]
    river(sc, sx(YELLOW_R), t, -1.38, MERC, 2)
    river(sc, sx(YANGZI_R), t, -1.38, MERC, 2, speed=0.4)
    rising(sc, t, 30, y0=0.75, h=2.0)
    if v == 0:
        cam = look_at(*orbit([0, -0.4, 0], lerp(3.8, 5.0, ease(u)), 0.8 + 0.25 * u, 0.1))
    else:
        cam = look_at(*orbit([0, 0.0, 0], lerp(5.0, 7.5, ease(u)), 1.1 + 0.25 * u, lerp(0.15, 0.4, u)))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(2, 15))
