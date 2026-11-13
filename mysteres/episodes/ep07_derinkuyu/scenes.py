# Plans propres à l'épisode 7 : Derinkuyu, la ville souterraine de Cappadoce
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE...)

TUFF = np.array([0.55, 0.78, 0.92])      # BGR : tuf beige clair
SKY = np.array([1.00, 0.80, 0.45])       # bleu : air frais
WATER = np.array([1.00, 0.70, 0.30])
DARKT = TUFF * 0.22

NLEV = 18
DY = 0.26        # écart entre niveaux
R_CITY = np.random.default_rng(21)
ROOMS = []       # (niveau, centre, taille)
for k in range(NLEV):
    n = 3 + int(R_CITY.integers(0, 3))
    for j in range(n):
        a = 2 * math.pi * j / n + R_CITY.uniform(-0.4, 0.4) + k * 0.7
        r = R_CITY.uniform(0.45, 1.05)
        ROOMS.append((k, np.array([r * math.cos(a), -0.2 - k * DY, r * math.sin(a)]),
                      np.array([R_CITY.uniform(0.22, 0.42), 0.15, R_CITY.uniform(0.2, 0.36)])))


def lev_y(k):
    return -0.2 - k * DY


def city(sc, lit=NLEV, col=TUFF, dim_from=None, shafts=True, prog=1.0):
    """Ville souterraine : salles par niveau, galeries, rampes et puits central."""
    nshow = max(1, int(round(NLEV * prog)))
    for k in range(min(nshow, NLEV)):
        c = col if k < lit else col * 0.15
        if dim_from is not None and k >= dim_from:
            c = col * 0.13
        rs = [r for r in ROOMS if r[0] == k]
        for _, p, s in rs:
            sc.box(p, s, c, 1 if k >= lit else 2)
        for a, b in zip(rs, rs[1:] + rs[:1]):
            sc.seg(a[1], b[1], c * 0.6, 1)
        if k + 1 < nshow:
            nxt = [r for r in ROOMS if r[0] == k + 1]
            sc.seg(rs[0][1] - [0, 0.07, 0], nxt[-1][1] + [0, 0.07, 0], c * 0.5, 1)
    if shafts:
        bot = lev_y(nshow - 1) - 0.08
        for a in np.linspace(0, 2 * math.pi, 8, endpoint=False):
            sc.seg([0.07 * math.cos(a), 0, 0.07 * math.sin(a)], [0.07 * math.cos(a), bot, 0.07 * math.sin(a)], col * 0.35, 1)
        for y in np.arange(0, bot, -0.5):
            sc.circle([0, y, 0], 0.07, col * 0.5, 1, 12)


def surface(sc, size=1.8, col=GOLD * 0.18, n=12):
    sc.grid_plane(size, n, 0.0, col)


def house(sc, c=(0.6, 0, 0.3), col=GOLD, s=1.0):
    c = np.asarray(c, float)
    sc.box(c + [0, 0.18 * s, 0], [0.42 * s, 0.36 * s, 0.36 * s], col, 2)
    a, b = c + [-0.21 * s, 0.36 * s, -0.18 * s], c + [0.21 * s, 0.36 * s, -0.18 * s]
    a2, b2 = a + [0, 0, 0.36 * s], b + [0, 0, 0.36 * s]
    r1, r2 = c + [0, 0.52 * s, -0.18 * s], c + [0, 0.52 * s, 0.18 * s]
    sc.add([a, r1, b], col, 2); sc.add([a2, r2, b2], col, 2); sc.seg(r1, r2, col, 2)
    sc.box(c + [0, -0.12 * s, 0], [0.42 * s, 0.22 * s, 0.36 * s], col * 0.55, 1)   # cave


def cam_city(u, az0, az1, dist, el, y):
    return look_at(*orbit([0, y, 0], lerp(dist[0], dist[1], ease(u)), az0 + (az1 - az0) * u, lerp(el[0], el[1], u)))


# ------------------------------------------------------------------ plans
def sh_hook_wall(img, u, t, v, T):
    sc = Scene()
    hc = np.array([0, 0, 0])
    house(sc, hc, GOLD, 2.2)
    # mur de la cave (face +z) qui se fissure puis s'ouvre
    z = 0.4; y0, y1 = -0.5, 0.0
    br = ease((u - 0.3) / 0.5)
    R = np.random.default_rng(4)
    for i in range(6):
        for j in range(4):
            x0 = -0.45 + i * 0.15; yy = y0 + j * 0.125
            off = np.array([0, -br * R.uniform(0.1, 0.5), br * R.uniform(0.3, 0.9)]) if abs(i - 2.5) < 2 and j < 3 else np.zeros(3)
            sc.add([[x0, yy, z], [x0 + 0.15, yy, z], [x0 + 0.15, yy + 0.125, z], [x0, yy + 0.125, z]] + off,
                   TUFF * (1 - 0.4 * br), 1, closed=True)
    # lueur derrière le mur
    if br > 0:
        for k in range(4):
            sc.box([0, -0.3, -0.4 - 0.25 * k], [0.4 - 0.05 * k, 0.3, 0.02], AMBER * br * (0.9 - 0.2 * k), 1)
    cam = look_at(*orbit([0, -0.25, 0], lerp(3.0, 1.7, ease(u)), 0.15 - 0.2 * u, lerp(0.15, 0.02, u)))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 12))


def sh_hook_reveal(img, u, t, v, T):
    sc = Scene(); surface(sc)
    house(sc, (0.6, 0, 0.3), GOLD * 0.8)
    city(sc, prog=0.25 + 0.75 * ease(u * 1.3))
    cam = cam_city(u, 0.6, 0.2, (4.2, 5.4), (0.25, 0.12), lerp(-0.6, -2.2, ease(u)))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 14))


def fairy(sc, c, h, r, col):
    c = np.asarray(c, float)
    n = 10
    for a in np.linspace(0, 2 * math.pi, n, endpoint=False):
        sc.seg(c + [r * math.cos(a), 0, r * math.sin(a)], c + [0, h, 0], col * 0.6, 1)
    for f in (0, 0.35, 0.65):
        sc.circle(c + [0, h * f, 0], r * (1 - f), col, 1, 18)


def sh_cappadoce(img, u, t, v, T):
    sc = Scene(); surface(sc, 2.2, GOLD * 0.15, 14)
    R = np.random.default_rng(9)
    for i in range(14):
        x, z = R.uniform(-2, 2, 2)
        if abs(x) < 0.5 and abs(z) < 0.5: continue
        fairy(sc, [x, 0, z], R.uniform(0.4, 0.9), R.uniform(0.15, 0.25), TUFF * 0.8)
    for i in range(6):
        house(sc, (R.uniform(-1, 1), 0, R.uniform(-1, 1)), GOLD * 0.6, 0.6)
    city(sc, prog=0.6 + 0.4 * ease(u), col=TUFF * 0.9)
    if v == 0:
        cam = cam_city(u, -0.6, 0.2, (5.6, 4.8), (0.45, 0.2), lerp(-0.4, -1.4, ease(u)))
    else:
        cam = cam_city(u, 0.4, 1.0, (4.4, 4.8), (0.1, -0.05), -1.8)
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 14))


def sh_levels(img, u, t, v, T):
    sc = Scene(); surface(sc, 1.6, GOLD * 0.12, 10)
    nl = int(1 + ease(u * 1.3) * (NLEV - 1))
    city(sc, prog=nl / NLEV)
    x = 1.45
    sc.seg([x, 0, 0], [x, lev_y(nl - 1), 0], AMBER, 2)
    for k in range(nl):
        sc.seg([x - 0.08, lev_y(k), 0], [x + 0.08, lev_y(k), 0], AMBER * (1.0 if k % 5 == 4 else 0.6), 1)
    sc.seg([x - 0.15, lev_y(nl - 1) - 0.05, 0], [x + 0.15, lev_y(nl - 1) - 0.05, 0], WHITE, 2)
    cam = cam_city(u, -0.35, 0.05, (5.4, 5.2), (0.08, 0.0), lerp(-1.0, -2.4, ease(u)))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 16))


def sh_tuff(img, u, t, v, T):
    sc = Scene()
    sc.box([0, 0, 0], [2.0, 1.4, 1.2], TUFF * 0.7, 1, grid=6)
    # cavité creusée progressivement (arche)
    d = 0.1 + 0.9 * ease(u)
    for k in range(7):
        zz = 0.6 - d * k / 6
        pts = [[-0.35, -0.7, zz], [-0.35, 0.05, zz]] + [[0.35 * math.cos(a), 0.05 + 0.35 * math.sin(a), zz] for a in np.linspace(math.pi, 0, 12)] + [[0.35, -0.7, zz]]
        sc.add(pts, AMBER if k == 6 else TUFF * 0.8, 2 if k in (0, 6) else 1)
    # outil (pic) qui frappe
    ph = (t * 1.6) % 1.0
    hit = 0.6 - d + 0.05
    a = 0.9 * (1 - abs(ph * 2 - 1))
    tip = np.array([0.1, -0.1, hit + 0.02])
    hdl = tip + [0.45 * math.cos(a), 0.45 * math.sin(a) + 0.2, 0.25]
    sc.seg(tip, hdl, WHITE, 2); sc.seg(tip + [-0.08, 0.1, 0], tip + [0.08, -0.06, 0.0], WHITE, 3)
    # éclats
    R = np.random.default_rng(int(t * 1.6))
    if ph < 0.35:
        for i in range(10):
            dv = R.uniform(-1, 1, 3) * [0.4, 0.3, 0.1] + [0, 0.15, 0.3]
            sc.seg(tip, tip + dv * ph * 2.5, GOLD, 1)
    cam = look_at(*orbit([0, -0.1, 0.2], lerp(2.6, 1.9, ease(u)), 0.5 - 0.4 * u if v == 0 else -0.4 + 0.3 * u, 0.15))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(1, 10))


def sh_crowd(img, u, t, v, T):
    sc = Scene(); surface(sc, 1.6, GOLD * 0.10, 10)
    city(sc, col=TUFF * 0.5)
    R = np.random.default_rng(5)
    n = int(40 + 360 * ease(u * 1.2))
    idx = R.integers(0, len(ROOMS), 400)
    off = R.uniform(-0.5, 0.5, (400, 3)) * [0.6, 0, 0.5]
    for i in range(n):
        _, p, s = ROOMS[idx[i]]
        q = p + off[i] * s * 2 + [0, -0.07, 0]
        sc.seg(q, q + [0, 0.05, 0], AMBER if i % 7 else WHITE, 2)
    cam = cam_city(u, 0.9, 0.4, (5.0, 4.4), (0.2, 0.12), lerp(-1.6, -2.4, ease(u)))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 14))


SHAFTS = np.random.default_rng(31).uniform(-1.2, 1.2, (16, 2))


def sh_shafts(img, u, t, v, T):
    sc = Scene(); surface(sc, 1.6, GOLD * 0.15, 10)
    city(sc, col=TUFF * 0.45, shafts=True)
    for i, (x, z) in enumerate(SHAFTS):
        bot = -1.5 - (i % 5) * 0.6
        sc.seg([x, 0.05, z], [x, bot, z], SKY * 0.5, 1)
        sc.circle([x, 0.0, z], 0.05, SKY, 1, 10)
        for k in range(3):
            y = 0.05 - ((t * 1.2 + k / 3 + i * 0.13) % 1.0) * (0.05 - bot)
            sc.seg([x, y, z], [x, y - 0.12, z], SKY, 2)
    cam = cam_city(u, -0.8, -0.3, (4.8, 4.4), (0.35, 0.18), lerp(-1.0, -2.0, ease(u)))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 14))


def sh_water(img, u, t, v, T):
    sc = Scene()
    city(sc, col=TUFF * 0.35)
    wy = lev_y(NLEV - 1) - 0.5
    sc.grid_plane(1.4, 14, wy, WATER * 0.45)
    for k in range(3):
        rr = 0.1 + ((t * 0.6 + k / 3) % 1.0) * 0.6
        sc.circle([0.8, wy + 0.01, 0.2], rr, WATER * (1 - rr / 0.7), 1, 32)
    sc.seg([0.8, 0, 0.2], [0.8, wy, 0.2], WATER, 2)
    sc.circle([0.8, 0, 0.2], 0.08, WATER, 2, 16)
    # seau qui descend
    by = lerp(-0.3, wy + 0.1, ease(u))
    sc.box([0.8, by, 0.2], [0.08, 0.08, 0.08], WHITE, 2)
    cam = cam_city(u, 0.3, 0.6, (4.6, 3.8), (-0.05, -0.15), lerp(-3.0, -4.2, ease(u)))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(1, 12))


def sh_rooms(img, u, t, v, T):
    sc = Scene()
    # trois salles côte à côte : étable, cave à jarres, église en croix
    sc.box([-1.1, 0, 0], [0.9, 0.6, 0.8], TUFF, 2)
    for i in range(3):
        sc.box([-1.4 + i * 0.3, -0.18, -0.25], [0.04, 0.24, 0.3], TUFF * 0.6, 1)    # stalles
    sc.box([0, 0, 0], [0.9, 0.6, 0.8], TUFF, 2)
    for i in range(3):
        for j in range(2):
            c = np.array([-0.25 + i * 0.25, -0.15, -0.15 + j * 0.3])
            for f, r in ((0, 0.05), (0.08, 0.09), (0.16, 0.08), (0.24, 0.04)):
                sc.circle(c + [0, f - 0.12, 0], r, AMBER * 0.8, 1, 12)
    lit = ease((u - 0.45) / 0.35)
    cc = np.array([1.2, 0, 0])
    col = TUFF * (0.5 + 0.5 * lit)
    sc.box(cc, [0.35, 0.6, 1.0], col, 2)
    sc.box(cc, [1.0, 0.6, 0.35], col, 2)
    for k in range(9):
        a = math.pi * k / 8
        sc.seg(cc + [-0.17, 0.3 + 0.15 * math.sin(a), -0.5 + 1.0 * k / 8], cc + [0.17, 0.3 + 0.15 * math.sin(a), -0.5 + 1.0 * k / 8], col * 0.5, 1)
    sc.seg(cc + [0, 0.02, -0.48], cc + [0, 0.22, -0.48], AMBER * lit + WHITE * 0.2, 2)
    sc.seg(cc + [-0.07, 0.15, -0.48], cc + [0.07, 0.15, -0.48], AMBER * lit + WHITE * 0.2, 2)
    sc.seg([-0.65, -0.2, 0], [-0.45, -0.2, 0], TUFF * 0.6, 1); sc.seg([0.45, -0.2, 0], [0.7, -0.2, 0], TUFF * 0.6, 1)
    target = lerp([-1.0, 0, 0], [1.1, 0, 0], ease(u))
    cam = look_at(*orbit(target, 3.3, 0.5 - 0.2 * u, 0.35))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(1, 10))


def sh_stone_door(img, u, t, v, T):
    sc = Scene()
    # couloir le long de z
    for x in (-0.35, 0.35):
        sc.seg([x, -0.5, -2.5], [x, -0.5, 1.5], TUFF, 2); sc.seg([x, 0.5, -2.5], [x, 0.5, 1.5], TUFF * 0.7, 1)
        for z in np.arange(-2.5, 1.6, 0.5):
            sc.seg([x, -0.5, z], [x, 0.5, z], TUFF * 0.35, 1)
    for z in np.arange(-2.5, 1.6, 0.5):
        sc.seg([-0.35, 0.5, z], [0.35, 0.5, z], TUFF * 0.35, 1)
    # niche latérale + meule qui roule
    sc.box([0.75, 0, 0], [0.8, 1.1, 0.25], TUFF * 0.6, 1)
    x = lerp(0.85, 0.0, ease((u - 0.15) / 0.65))
    rot = (0.85 - x) / 0.5
    c = np.array([x, 0, 0])
    for dz in (-0.09, 0.09):
        sc.circle(c + [0, 0, dz], 0.5, WHITE * 0.9, 2, 40, "z")
        sc.circle(c + [0, 0, dz], 0.1, AMBER, 1, 16, "z")
    for a in np.linspace(0, 2 * math.pi, 12, endpoint=False):
        p = c + [0.5 * math.cos(a + rot), 0.5 * math.sin(a + rot), 0]
        sc.seg(p + [0, 0, -0.09], p + [0, 0, 0.09], WHITE * 0.6, 1)
        if a < 1: sc.seg(c + [0.1 * math.cos(a + rot), 0.1 * math.sin(a + rot), 0.09], p + [0, 0, 0.09], AMBER, 1)
    if v == 0:
        cam = look_at([0.05, 0.05, -2.0 + 0.4 * u], [0.1, -0.05, 0.5])
    else:
        cam = look_at(*orbit([0.3, 0, 0], 2.6, 0.9 - 0.3 * u, 0.2))
    draw(img, sc, cam, fade=(1, 8))


def sh_history(img, u, t, v, T):
    sc = Scene(); surface(sc, 1.6, GOLD * 0.10, 10)
    # niveaux anciens d'abord (haut), puis agrandissements byzantins (bas) en or
    k1 = int(4 + 4 * ease(u * 2))
    k2 = int(ease((u - 0.45) / 0.45) * (NLEV - 8))
    city(sc, prog=(k1 + k2) / NLEV, col=TUFF, dim_from=None)
    for k in range(k1, k1 + k2):
        for _, p, s in [r for r in ROOMS if r[0] == k]:
            sc.box(p, s * 1.04, AMBER, 1)
    cam = cam_city(u, -0.2, 0.4, (4.6, 5.0), (0.15, 0.08), lerp(-0.8, -2.2, ease(u)))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 16))


def sh_closed(img, u, t, v, T):
    sc = Scene(); surface(sc, 1.6, GOLD * 0.12, 10)
    city(sc, col=TUFF, dim_from=8 if u > 0.2 else None)
    # barrière au niveau 8
    y = (lev_y(7) + lev_y(8)) / 2
    w = ease((u - 0.2) / 0.3)
    if w > 0:
        sc.add([[-1.3, y, -1.3], [1.3, y, -1.3], [1.3, y, 1.3], [-1.3, y, 1.3]], AMBER * w, 2, closed=True)
        for f in np.linspace(-1.3, 1.3, 9):
            sc.seg([f, y, -1.3], [f + 0.3 if f < 1.0 else 1.3, y, 1.3], AMBER * w * 0.4, 1)
    cam = cam_city(u, 0.5, 0.0, (5.2, 4.8), (0.18, 0.1), lerp(-1.6, -2.2, ease(u)))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 16))


SITES = np.random.default_rng(77).normal(0, 0.9, (360, 2)).clip(-2.0, 2.0)


def sh_sites(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(2.2, 16, 0.0, GOLD * 0.13)
    n = int(ease(u * 1.2) * len(SITES))
    for i, (x, z) in enumerate(SITES[:n]):
        a = 1.0 if i > n - 15 else 0.65
        sc.seg([x, 0, z], [x, -0.12 - 0.1 * (i % 3), z], AMBER * a, 1)
        sc.circle([x, 0.0, z], 0.025, AMBER * a, 1, 6)
    sc.circle([0, 0, 0], 0.12, WHITE, 2, 16)
    cam = look_at(*orbit([0, 0, 0], lerp(3.2, 4.2, ease(u)), 0.3 + 0.5 * u, lerp(0.9, 0.75, u)))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 14))


def sh_final(img, u, t, v, T):
    sc = Scene(); surface(sc)
    house(sc, (0.6, 0, 0.3), GOLD * 0.8)
    city(sc, col=TUFF * lerp(1.0, 0.6, ease(u))[()])
    cam = cam_city(u, 0.2, 0.9, (5.2, 3.8), (0.08, 0.25), lerp(-2.2, -0.6, ease(u)))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(2, 14))
