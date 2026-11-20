# Plans propres à l'épisode 13 : le tunnel sous le temple du Serpent à plumes (Teotihuacan)
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

MERC = np.array([1.00, 0.92, 0.80])     # BGR : argent bleuté
JADE = np.array([0.55, 0.95, 0.35])
PYR = np.array([0.35, 0.90, 1.00])      # éclat doré pâle
SPH = np.array([0.15, 0.80, 0.95])      # jaune
EARTH = np.array([0.20, 0.38, 0.60])
R13 = np.random.default_rng(13)
PYRPTS = R13.uniform(0, 1, (260, 3))
SPHPTS = R13.uniform(-1, 1, (140, 3))
RAIN = R13.uniform(0, 1, (160, 3))
OBJ = R13.uniform(-1, 1, (36, 4))

DEPTH = -1.5      # niveau du tunnel
ZENT = 3.4        # entrée (sur la place, devant le temple)


def fv(x):
    return float(np.asarray(x))


def temple(sc, c=(0, 0, 0), base=1.6, tiers=7, th=0.2, col=GOLD, b=1.0):
    """Pyramide à degrés (talud-tablero) + escalier frontal."""
    c = np.asarray(c, float)
    for k in range(tiers):
        h = base * (1 - k * 0.1)
        y = k * th
        # talud (pente) puis tablero (panneau vertical)
        lo = [c + [sx * h, y, sz * h] for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        mid = [c + [sx * (h - 0.06), y + th * 0.4, sz * (h - 0.06)] for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        hi = [c + [sx * (h - 0.06), y + th, sz * (h - 0.06)] for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        sc.add(lo, col * 0.9 * b, 2, closed=True)
        sc.add(mid, col * 0.6 * b, 1, closed=True)
        sc.add(hi, col * 0.6 * b, 1, closed=True)
        for a, m, e in zip(lo, mid, hi):
            sc.seg(a, m, col * 0.7 * b, 1); sc.seg(m, e, col * 0.7 * b, 1)
        # têtes de serpent stylisées sur le tablero (petits carrés)
        for j in range(-3, 4):
            x = j * (h - 0.06) / 3.6
            p = c + [x, y + th * 0.7, h - 0.06]
            sc.add([p + [-0.04, -0.04, 0.001], p + [0.04, -0.04, 0.001], p + [0.04, 0.04, 0.001], p + [-0.04, 0.04, 0.001]],
                   WHITE * 0.5 * b, 1, closed=True)
    # escalier frontal
    top = tiers * th
    for k in range(15):
        f = k / 14
        y = top * f; z = c[2] + base + 0.35 - (base * 0.62 + 0.35) * f
        sc.seg(c + [-0.28, y, z], c + [0.28, y, z], col * 0.8 * b, 1)
    sc.seg(c + [-0.28, 0, base + 0.35], c + [-0.28, top, base * 0.38], col * b, 2)
    sc.seg(c + [0.28, 0, base + 0.35], c + [0.28, top, base * 0.38], col * b, 2)


def ground(sc, y=0.0, size=4.5, col=GOLD):
    sc.grid_plane(size, 18, y, col * 0.12)


def tunnel(sc, z0=ZENT, z1=0.0, y=DEPTH, w=0.32, hgt=0.42, col=GOLD, b=1.0, n=26, fill=0.0):
    """Tunnel horizontal (section voûtée) de z0 à z1 ; fill = part comblée depuis le fond."""
    for k in range(n):
        f = k / (n - 1)
        z = z0 + (z1 - z0) * f
        arch = [[-w, y, z], [-w, y + hgt * 0.7, z], [-w * 0.6, y + hgt * 0.95, z], [0, y + hgt, z],
                [w * 0.6, y + hgt * 0.95, z], [w, y + hgt * 0.7, z], [w, y, z]]
        sc.add(arch, col * (0.9 if k % 5 == 0 else 0.5) * b, 2 if k % 5 == 0 else 1)
        if fill > 0 and f > 1 - fill:
            for yy in np.linspace(y + 0.05, y + hgt * 0.85, 4):
                sc.seg([-w * 0.95, yy, z], [w * 0.95, yy, z], EARTH * 0.8 * b, 1)
    for x, yy in ((-w, y), (w, y), (-w, y + hgt * 0.7), (w, y + hgt * 0.7), (0, y + hgt)):
        sc.seg([x, yy, z0], [x, yy, z1], col * 0.7 * b, 1)


def shaft(sc, z=ZENT, y0=0.0, y1=DEPTH, r=0.18, col=GOLD, b=1.0):
    for k in range(8):
        sc.circle([0, y0 + (y1 - y0) * k / 7, z], r, col * 0.6 * b, 1, 24)
    for a in range(0, 360, 60):
        q = math.radians(a)
        sc.seg([r * math.cos(q), y0, z + r * math.sin(q)], [r * math.cos(q), y1, z + r * math.sin(q)], col * 0.5 * b, 1)


def pool(sc, c, r, t, col=MERC, n=5):
    """Flaque de mercure : ellipses concentriques ondulantes."""
    c = np.asarray(c, float)
    th = np.linspace(0, 2 * math.pi, 64)
    for k in range(n):
        rr = r * (1 - k / n) * (1 + 0.04 * math.sin(2.5 * t + k))
        P = np.stack([c[0] + rr * np.cos(th), np.full_like(th, c[1] + 0.005 * k), c[2] + rr * 0.8 * np.sin(th)], 1)
        sc.add(P, col * (1.0 - 0.12 * k), 2 if k == 0 else 1)
    # reflets
    for k in range(6):
        a = 2 * math.pi * k / 6 + 0.4 * t
        sc.seg(c + [0.2 * r * math.cos(a), 0.01, 0.2 * r * math.sin(a)],
               c + [0.7 * r * math.cos(a), 0.01, 0.56 * r * math.sin(a)], WHITE * 0.5, 1)


def sphere(sc, c, r, col, n=10):
    sc.circle(c, r, col, 1, n, "y"); sc.circle(c, r, col, 1, n, "z"); sc.circle(c, r, col * 0.7, 1, n, "x")


def statue(sc, c, s=0.25, col=JADE):
    """Figurine stylisée (blocs) — pas de visage."""
    c = np.asarray(c, float)
    sc.box(c + [0, 0.5 * s, 0], [0.7 * s, 1.0 * s, 0.4 * s], col, 1)
    sc.box(c + [0, 1.25 * s, 0], [0.55 * s, 0.5 * s, 0.42 * s], col, 2)
    sc.box(c + [0, 1.55 * s, 0], [0.8 * s, 0.1 * s, 0.5 * s], col * 0.7, 1)


def ptext(img, txt, org, sc_, col, th=2):
    tmp = np.zeros(img.shape, np.uint8)
    cv2.putText(tmp, txt, org, cv2.FONT_HERSHEY_SIMPLEX, sc_, (np.clip(np.asarray(col), 0, 1) * 255).tolist(), th, cv2.LINE_AA)
    np.add(img, tmp.astype(np.float32) / 255, out=img)


def label3d(img, cam, p, txt, col=WHITE, sc_=1.1):
    eye, M = cam
    q = (np.asarray(p, float) - eye) @ M.T
    if q[2] <= 0.1: return
    f = (W / 2) / math.tan(0.4)
    x, y = int(W / 2 + f * q[0] / q[2]), int(H / 2 - f * q[1] / q[2])
    ptext(img, txt, (x - int(11 * sc_ * len(txt)), y), sc_, col)


# ------------------------------------------------------------------ plans
def sh_hook_temple(img, u, t, v, T):
    """Le temple, et sous lui le tunnel qui s'allume."""
    sc = Scene(); temple(sc); ground(sc)
    tunnel(sc, b=0.4 + 0.6 * ease(u * 1.5))
    shaft(sc, b=0.6)
    pool(sc, [0, DEPTH + 0.01, 0.0], 0.25, t, MERC * ease(u * 1.6))
    cam = look_at(*orbit([0, -0.4, 0.7], lerp(10.5, 9.0, ease(u)), 1.75 + 0.25 * u, 0.24))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(3, 14))


def sh_hook_mercury(img, u, t, v, T):
    """Gros plan : la flaque argentée au fond de la chambre."""
    sc = Scene()
    pool(sc, [0, 0, 0], 1.1, t, MERC, 7)
    sc.grid_plane(1.6, 8, -0.01, GOLD * 0.15)
    cam = look_at(*orbit([0, 0.0, 0], lerp(3.6, 2.6, ease(u)), 0.3 + 0.5 * u, 0.55))
    draw(img, sc, cam, fade=(1.5, 8))


def sh_city_map(img, u, t, v, T):
    """Plan de Teotihuacan : l'allée des Morts, Soleil, Lune, la Ciudadelle."""
    sc = Scene(); sc.grid_plane(6, 24, 0, GOLD * 0.1)
    sc.seg([-0.25, 0, -5.5], [-0.25, 0, 4.5], GOLD * 0.8, 2); sc.seg([0.25, 0, -5.5], [0.25, 0, 4.5], GOLD * 0.8, 2)
    sc.pyramid(half=1.1, h=1.2, courses=8, col=GOLD * 0.8, c=(-1.8, 0, -1.2), joints=False)    # Soleil
    sc.pyramid(half=0.8, h=0.9, courses=6, col=GOLD * 0.7, c=(0, 0, -5.8), joints=False)       # Lune
    # Ciudadelle : enceinte carrée et temple du Serpent à plumes
    sc.add([[0.6, 0, 2.2], [3.6, 0, 2.2], [3.6, 0, 5.2], [0.6, 0, 5.2]], GOLD * 0.7, 2, closed=True)
    sc.add([[0.8, 0.12, 2.4], [3.4, 0.12, 2.4], [3.4, 0.12, 5.0], [0.8, 0.12, 5.0]], GOLD * 0.4, 1, closed=True)
    temple(sc, c=(2.1, 0, 3.0), base=0.55, tiers=6, th=0.08, col=AMBER, b=1.2)
    a = 0.5 + 0.5 * math.sin(4 * t)
    sc.circle([2.1, 0.02, 3.0], 0.75 + 0.15 * a, WHITE * (0.4 + 0.5 * a), 2)
    cam = look_at(*orbit([lerp(0, 2.1, ease(u)), 0, lerp(0, 3.0, ease(u))], lerp(11, 5.5, ease(u)), 0.4, 1.0))
    draw(img, sc, cam, fade=(3, 18))
    if u > 0.55:
        label3d(img, cam, [2.1, 0.9, 3.0], "SERPENT A PLUMES", WHITE * min(1, (u - 0.55) * 4), 1.0)


def sh_sinkhole(img, u, t, v, T):
    """Pluie, puis le sol qui cède au pied du temple."""
    sc = Scene(); temple(sc, c=(0, 0, -1.2), b=0.7); ground(sc)
    open_ = ease(min(1, u * 1.6))
    c = np.array([0, 0, 1.4])
    for k in range(4):
        sc.circle(c + [0, -0.05 * k, 0], 0.08 + 0.32 * open_ * (1 - 0.15 * k), WHITE * (0.9 - 0.2 * k), 2, 40)
    for k in range(10):
        a = 2 * math.pi * k / 10
        r = 0.4 * open_
        sc.seg(c + [r * math.cos(a), 0, r * math.sin(a)], c + [(r + 0.25) * math.cos(a + 0.2), 0, (r + 0.25) * math.sin(a + 0.2)], GOLD * 0.6, 1)
    for p in RAIN:
        x, z = -3 + 6 * p[0], -3 + 6 * p[2]
        y = 4 - ((p[1] * 4 + t * 6) % 4)
        sc.seg([x, y, z], [x - 0.02, y - 0.22, z], MERC * 0.45, 1)
    cam = look_at(*orbit([0, 0.2, 0.6], 5.2 - 0.8 * u, 0.5 - 0.2 * u, 0.42))
    draw(img, sc, cam, fade=(2, 12))


def sh_rope_descent(img, u, t, v, T):
    """Coupe du sol : la corde descend dans le puits jusqu'au tunnel."""
    sc = Scene(); ground(sc, 0, 3)
    shaft(sc, z=0.0, y0=0.0, y1=DEPTH, r=0.25)
    tunnel(sc, z0=-0.3, z1=-4.0, y=DEPTH - 0.45, w=0.4, hgt=0.5, b=0.9)
    yb = lerp(0.0, DEPTH - 0.1, ease(u))
    sc.seg([0, 0.8, 0], [0, fv(yb), 0], WHITE, 2)               # corde
    p = np.array([0, fv(yb) - 0.12, 0])
    sc.circle(p, 0.07, WHITE, 2, 16, "z"); sc.seg(p + [0, -0.07, 0], p + [0, -0.3, 0], WHITE, 2)
    # lampe : cône lumineux vers le bas
    for a in range(0, 360, 45):
        q = math.radians(a)
        sc.seg(p, p + [0.35 * math.cos(q), -0.9, 0.35 * math.sin(q)], PYR * 0.35, 1)
    # échelle de profondeur
    for k in range(5):
        y = DEPTH * k / 4
        sc.seg([0.9, y, 0], [1.05, y, 0], GOLD * 0.7, 1)
    sc.seg([0.95, 0, 0], [0.95, DEPTH, 0], GOLD * 0.6, 1)
    cam = look_at(*orbit([0, fv(yb) * 0.7 - 0.2, -0.6], 3.6, 0.9 + (0.25 * v), 0.15))
    draw(img, sc, cam, fade=(1.5, 10))


def sh_tunnel_cutaway(img, u, t, v, T):
    """Le temple en transparence, le tunnel qui court jusqu'en son centre."""
    sc = Scene(); temple(sc, b=0.55); ground(sc)
    shaft(sc)
    L = ease(min(1, u * 1.3))
    tunnel(sc, z0=ZENT, z1=ZENT - ZENT * L, b=1.0)
    zf = ZENT - ZENT * L
    sc.circle([0, DEPTH + 0.2, zf], 0.15 + 0.05 * math.sin(6 * t), WHITE, 2, 24, "z")
    # cote ≈ 100 m
    sc.seg([0.7, DEPTH, ZENT], [0.7, DEPTH, 0], WHITE * 0.6, 1)
    for z in (ZENT, 0):
        sc.seg([0.62, DEPTH, z], [0.78, DEPTH, z], WHITE * 0.6, 1)
    cam = look_at(*orbit([0, -0.4, 0.9], 10.0 - 0.8 * u, 1.5 + 0.2 * u, 0.14))
    draw(img, sc, cam, fade=(3, 13))


def sh_sealing(img, u, t, v, T):
    """Le tunnel comblé de terre, puis l'entrée fermée de gros blocs."""
    sc = Scene()
    tunnel(sc, z0=1.0, z1=-6.0, y=0, w=0.7, hgt=1.0, n=20, fill=ease(min(1, u * 1.5)))
    nb = int(9 * ease(max(0, (u - 0.35) / 0.65)))
    for k in range(nb):
        i, j = k % 3, k // 3
        x = -0.46 + 0.46 * i; y = 0.17 + 0.33 * j
        sc.box([x, y, 1.0], [0.42, 0.3, 0.4], WHITE * 0.85, 2)
    cam = look_at([0.15 * math.sin(0.3 * t), 0.55, 3.6 - 0.6 * u], [0, 0.45, -1.5])
    draw(img, sc, cam, fade=(2, 10))


def sh_dig(img, u, t, v, T):
    """Fouille : le front de terre recule, centimètre par centimètre."""
    sc = Scene()
    zf = lerp(-0.5, -4.0, ease(u))
    tunnel(sc, z0=1.0, z1=-6.0, y=0, w=0.7, hgt=1.0, n=22, b=0.8)
    for k in range(10):
        z = fv(zf) - 0.12 * k
        for yy in np.linspace(0.08, 0.9, 6):
            sc.seg([-0.65, yy, z], [0.65, yy, z], EARTH * (0.9 - 0.06 * k), 1)
    # pelle
    s = 0.3 * math.sin(5 * t)
    hnd = np.array([0.15, 0.85, fv(zf) + 1.3 + 0.1 * s]); bl = np.array([0.05, 0.25, fv(zf) + 0.35 + 0.15 * s])
    sc.seg(hnd, bl, COPPER, 2)
    sc.add([bl + [-0.12, 0, 0], bl + [0.12, 0, 0], bl + [0.1, -0.12, -0.18], bl + [-0.1, -0.12, -0.18]], WHITE * 0.9, 2, closed=True)
    cam = look_at([0.25, 0.55, fv(zf) + 3.2], [0, 0.4, fv(zf) - 1])
    draw(img, sc, cam, fade=(1.5, 9))


def rover(sc, c, s=0.25, col=WHITE, t=0.0):
    c = np.asarray(c, float)
    sc.box(c + [0, 0.35 * s, 0], [1.0 * s, 0.4 * s, 1.6 * s], col, 2)
    for x in (-0.55 * s, 0.55 * s):
        for z in (-0.55 * s, 0.55 * s):
            sc.circle(c + [x, 0.18 * s, z], 0.18 * s, col * 0.8, 1, 14, "x")
    cam_ = c + [0, 0.75 * s, -0.7 * s]
    sc.seg(c + [0, 0.55 * s, -0.5 * s], cam_, col, 1)
    sc.circle(cam_, 0.08 * s, PYR, 2, 12, "z")
    for a in (-0.25, 0, 0.25):
        sc.seg(cam_, cam_ + [math.sin(a) * 1.4, -0.15, -1.4], PYR * (0.25 + 0.15 * math.sin(4 * t)), 1)


def sh_robots(img, u, t, v, T):
    sc = Scene()
    tunnel(sc, z0=2.0, z1=-6.0, y=0, w=0.7, hgt=1.0, n=22, b=0.7)
    z = lerp(1.0, -1.8, u)
    rover(sc, [0, 0, fv(z)], 0.42, WHITE, t)
    rover(sc, [0.0, 0, fv(z) + 1.4], 0.26, GOLD, t)
    cam = look_at([0.25 * math.sin(0.4 * t), 0.75, fv(z) + 2.0], [0, 0.15, fv(z) - 0.2])
    draw(img, sc, cam, fade=(1, 8))


def shell(sc, c, s, col):
    c = np.asarray(c, float)
    th = np.linspace(0, 5 * math.pi, 60)
    r = s * np.exp(0.12 * th) / np.exp(0.12 * th[-1])
    P = np.stack([c[0] + r * np.cos(th), c[1] + r * np.sin(th), np.full_like(th, c[2])], 1)
    sc.add(P, col, 2)


def sh_offerings(img, u, t, v, T):
    """Offrandes en orbite : coquillages, statues de jade, boules d'ambre, os."""
    sc = Scene()
    for k, o in enumerate(OBJ):
        a = 2 * math.pi * k / len(OBJ) + 0.25 * t
        r = 1.3 + 0.9 * (o[0] * 0.5 + 0.5)
        y = 0.9 * o[1] + 0.1 * math.sin(t + k)
        p = np.array([r * math.cos(a), y, r * math.sin(a)])
        kind = k % 4
        if kind == 0: shell(sc, p, 0.22, WHITE * 0.9)
        elif kind == 1: statue(sc, p - [0, 0.2, 0], 0.22, JADE)
        elif kind == 2: sphere(sc, p, 0.12, AMBER * 1.1, 14)
        else:
            sc.seg(p - [0.2, 0, 0], p + [0.2, 0, 0], WHITE * 0.7, 2)
            for d in (-0.2, 0.2):
                sc.circle(p + [d, 0, 0], 0.05, WHITE * 0.7, 1, 10, "z")
    statue(sc, [0, -0.8, 0], 0.8, JADE)
    sc.grid_plane(2.6, 12, -0.85, GOLD * 0.15)
    cam = look_at(*orbit([0, -0.1, 0], lerp(5.6, 4.6, ease(u)), 0.4 * u + 0.25 * v, 0.25))
    draw(img, sc, cam, fade=(2, 10))


def sh_pyrite_stars(img, u, t, v, T):
    """Vue à l'intérieur du tunnel : parois constellées d'éclats qui scintillent."""
    sc = Scene()
    tunnel(sc, z0=2.0, z1=-10.0, y=-0.6, w=0.8, hgt=1.25, n=24, b=0.35)
    lamp = ease(min(1, u * 2))
    for k, p in enumerate(PYRPTS):
        z = 1.5 - 11 * p[2]
        side = k % 3
        if side == 0: q = np.array([-0.79, -0.55 + 0.85 * p[1], z])
        elif side == 1: q = np.array([0.79, -0.55 + 0.85 * p[1], z])
        else: q = np.array([-0.5 + p[0], 0.62, z])
        tw = 0.5 + 0.5 * math.sin(7 * t + 13 * p[0] + 7 * k)
        col = PYR * (0.35 + 0.9 * tw) * lamp
        d = 0.025 + 0.02 * tw
        sc.seg(q - [d, 0, 0], q + [d, 0, 0], col, 2); sc.seg(q - [0, d, 0], q + [0, d, 0], col, 2)
    cam = look_at([0.05 * math.sin(0.5 * t), 0.0, 2.0 - 1.2 * u], [0.1 * math.sin(0.3 * t), 0.05, -8], roll=0.04 * math.sin(0.4 * t))
    draw(img, sc, cam, fov=1.15, fade=(1, 12))


def sh_spheres(img, u, t, v, T):
    """Des centaines de sphères jaunes posées dans une salle."""
    sc = Scene(); sc.grid_plane(2.5, 12, -0.6, GOLD * 0.15)
    sc.box([0, 0.3, 0], [5, 1.8, 5], GOLD * 0.25, 1)
    n = int(len(SPHPTS) * ease(min(1, 0.3 + u * 1.2)))
    for k, p in enumerate(SPHPTS[:n]):
        r = 0.06 + 0.06 * (p[2] * 0.5 + 0.5)
        c = [2.2 * p[0], -0.6 + r + 0.15 * (k % 3) * (abs(p[1]) > 0.7), 2.2 * p[1]]
        sphere(sc, c, r, SPH * (0.8 + 0.3 * math.sin(3 * t + k)), 10)
    big = [0, -0.1, 0]
    sphere(sc, big, 0.5, SPH, 28)
    sc.circle(big, 0.18, EARTH * 1.4, 2, 20, "z")         # cœur d'argile
    sc.circle(big, 0.18, EARTH * 1.4, 2, 20, "x")
    cam = look_at(*orbit([0, -0.2, 0], lerp(4.6, 3.4, ease(u)), 0.5 + 0.6 * u, 0.4))
    draw(img, sc, cam, fade=(1.5, 9))


def sh_mercury_reveal(img, u, t, v, T):
    """Fin du tunnel : chambre en croix, la flaque de mercure s'allume."""
    sc = Scene()
    tunnel(sc, z0=6.0, z1=1.2, y=0, w=0.6, hgt=0.9, n=16, b=0.6)
    # chambre en croix
    for c, s in (([0, 0.55, 0], [3.2, 1.1, 1.3]), ([0, 0.55, 0], [1.3, 1.1, 2.6])):
        sc.box(c, s, GOLD * 0.7, 1)
    on = ease(min(1, max(0, (u - 0.25) * 2.2)))
    pool(sc, [0, 0.01, 0], 0.55, t, MERC * on, 6)
    pool(sc, [1.15, 0.01, 0], 0.3, t + 1, MERC * on, 4)
    pool(sc, [-1.15, 0.01, 0], 0.3, t + 2, MERC * on, 4)
    cam = look_at(*orbit([0, 0.2, 0.2], lerp(5.0, 3.2, ease(u)), 0.15 + 0.4 * u, lerp(0.15, 0.6, ease(u))))
    draw(img, sc, cam, fade=(1.5, 10))


def sh_underworld(img, u, t, v, T):
    """Paysage miniature : lacs et rivières argentés d'un monde souterrain."""
    sc = Scene(); sc.grid_plane(3, 16, 0, GOLD * 0.12)
    th = np.linspace(-3, 3, 70)
    for k, ph in enumerate((0.0, 1.7)):
        x = th; z = 0.8 * np.sin(1.1 * th + ph + 0.3 * t) + (k - 0.5) * 1.4
        P = np.stack([x, np.full_like(x, 0.01), z], 1)
        sc.add(P, MERC * 0.9, 2); sc.add(P + [0, 0, 0.12], MERC * 0.5, 1)
    for c, r in (([-1.2, 0, 0.0], 0.45), ([1.4, 0, -0.6], 0.35), ([0.2, 0, 1.2], 0.3)):
        pool(sc, c, r, t, MERC, 4)
    for c in ([-2.2, 0, -1.6], [2.3, 0, 1.4], [0.9, 0, -2.0]):
        sc.pyramid(half=0.35, h=0.5, courses=5, col=GOLD * 0.5, c=c, joints=False)
    cam = look_at(*orbit([0, 0, 0], lerp(6.0, 4.8, ease(u)), 0.2 + 0.5 * u, 0.62))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 11))


def sh_tomb_question(img, u, t, v, T):
    """Une cuve vide, deux statues tournées vers le mur : où est le souverain ?"""
    sc = Scene(); sc.grid_plane(2.4, 12, 0, GOLD * 0.15)
    sc.box([0, 0.3, 0], [1.6, 0.6, 0.8], GOLD, 2, grid=4)
    a = 0.5 + 0.5 * math.sin(3 * t)
    sc.box([0, 0.62, 0], [1.4, 0.04, 0.6], WHITE * (0.3 + 0.4 * a), 1)
    statue(sc, [-1.4, 0, -0.9], 0.6, JADE * 0.8)
    statue(sc, [1.4, 0, -0.9], 0.6, JADE * 0.8)
    # point d'interrogation lumineux
    q = np.linspace(math.pi, -0.6 * math.pi, 30)
    P = np.stack([0.25 * np.cos(q), 1.6 + 0.25 * np.sin(q), np.zeros_like(q)], 1)
    sc.add(P, WHITE * (0.4 + 0.5 * a), 2); sc.seg([0.1, 1.38, 0], [0, 1.2, 0], WHITE * (0.4 + 0.5 * a), 2)
    sc.circle([0, 1.05, 0], 0.04, WHITE * (0.4 + 0.5 * a), 2, 10, "z")
    cam = look_at(*orbit([0, 0.75, -0.2], lerp(4.2, 3.4, ease(u)), -0.4 + 0.8 * u, 0.22))
    draw(img, sc, cam, fade=(2, 10))


def sh_final_temple(img, u, t, v, T):
    """Retour sur le temple : le tunnel s'éteint, le mercure brille seul."""
    sc = Scene(); temple(sc); ground(sc)
    tunnel(sc, b=lerp(0.9, 0.25, ease(u)))
    shaft(sc, b=0.4)
    pool(sc, [0, DEPTH + 0.01, 0.0], 0.3, t, MERC)
    cam = look_at(*orbit([0, -0.2, 0.8], lerp(5.4, 7.6, ease(u)), 2.2 + 0.4 * u, lerp(0.18, 0.32, ease(u))))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(3, 15))
