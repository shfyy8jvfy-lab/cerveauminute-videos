# Plans propres à l'épisode 2 : le mécanisme d'Anticythère
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

TEAL = np.array([0.85, 0.72, 0.25])     # BGR : bleu-vert de la mer
BRONZE = np.array([0.22, 0.55, 0.95])


def gear(sc, c, r, n, ang, col, w=2, spokes=4, axis="z", tooth=0.08, hub=0.18):
    c = np.asarray(c, float)
    k = np.arange(n * 4)
    th = ang + 2 * math.pi * k / (n * 4)
    rr = np.where((k % 4) < 2, r * (1 + tooth), r)
    if axis == "z":
        P = np.stack([c[0] + rr * np.cos(th), c[1] + rr * np.sin(th), np.full_like(th, c[2])], 1)
    else:
        P = np.stack([c[0] + rr * np.cos(th), np.full_like(th, c[1]), c[2] + rr * np.sin(th)], 1)
    sc.add(P, col, w, closed=True)
    sc.circle(c, r * hub, col, 1, 32, axis=axis)
    for s in range(spokes):
        a = ang + 2 * math.pi * s / spokes
        d = np.array([math.cos(a), math.sin(a), 0]) if axis == "z" else np.array([math.cos(a), 0, math.sin(a)])
        sc.seg(c + d * r * hub, c + d * r * 0.9, col * 0.7, 1)
    sc.circle(c, r * 0.9, col * 0.5, 1, 64, axis=axis)


def gear_train(sc, t, z0=0.0, bright=1.0):
    specs = [([0, 0, z0], 1.0, 64, 0.25), ([1.36, 0.55, z0 + 0.15], 0.42, 27, -0.6),
             ([-1.05, 0.9, z0 - 0.1], 0.5, 32, -0.5), ([0.55, -1.25, z0 + 0.1], 0.6, 38, -0.42),
             ([-0.95, -0.85, z0 + 0.2], 0.35, 22, 0.73), ([0.2, 1.45, z0 + 0.25], 0.3, 18, 0.9)]
    for c, r, n, sp in specs:
        gear(sc, c, r, n, t * sp, BRONZE * bright if r < 1 else GOLD * bright, 2)


def sh_hook_mechanism(img, u, t, v, T):
    sc = Scene(); gear_train(sc, t)
    sc.box([0, 0, 0.1], [3.6, 3.6, 0.6], GOLD * 0.25, 1)
    cam = look_at(*orbit([0, 0, 0], lerp(7.5, 4.6, ease(u)), 0.5 - 0.3 * u, 0.35 - 0.15 * u))
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(2, 12))


def sh_sea_wreck(img, u, t, v, T):
    sc = Scene()
    for k in range(14):  # surface de la mer
        z = -5 + k * 0.75
        xs = np.linspace(-6, 6, 60)
        sc.add(np.stack([xs, 4.5 + 0.08 * np.sin(xs * 1.5 + t * 1.2 + k), np.full_like(xs, z)], 1), TEAL * 0.5, 1)
    sc.grid_plane(6, 24, 0, TEAL * 0.22)  # fond marin
    # épave : coque inclinée (quille, membrures, plats-bords)
    Rx = np.array([[1, 0, 0], [0, math.cos(0.4), -math.sin(0.4)], [0, math.sin(0.4), math.cos(0.4)]])
    L, Wd, D = 3.4, 1.0, 0.55
    xs = np.linspace(-1, 1, 30)
    keel = np.stack([xs * L / 2, 0.15 + 0.25 * xs ** 4, np.zeros_like(xs)], 1)
    sc.add(keel @ Rx.T + [0, 0.2, 0], GOLD, 3)
    for side in (-1, 1):
        gun = np.stack([xs * L / 2, 0.15 + D + 0.2 * xs ** 2, side * Wd / 2 * (1 - xs ** 2 * 0.85)], 1)
        sc.add(gun @ Rx.T + [0, 0.2, 0], GOLD, 2)
    for f in np.linspace(-0.85, 0.85, 9):
        w = Wd / 2 * (1 - f * f * 0.85); top = 0.15 + D + 0.2 * f * f
        th = np.linspace(-math.pi / 2, math.pi / 2, 12)
        rib = np.stack([np.full_like(th, f * L / 2), top - (top - 0.15 - 0.25 * f ** 4) * np.cos(th), w * np.sin(th)], 1)
        sc.add(rib @ Rx.T + [0, 0.2, 0], GOLD * 0.7, 1)
    # amphores
    for i in range(6):
        sc.circle([-1.2 + 0.45 * i, 0.12, 0.9 + 0.1 * (i % 2)], 0.1, AMBER, 1, 16)
    # bulles qui montent
    r = np.random.default_rng(4)
    for k in range(40):
        x, z, ph = r.uniform(-2, 2), r.uniform(-1.5, 1.5), r.uniform(0, 4)
        y = ((t * 0.6 + ph) % 4.5)
        sc.circle([x, y, z], 0.03, WHITE * 0.6, 1, 8)
    if v == 0:
        cam = look_at(*orbit([0, 2.0, 0], lerp(7.5, 6.5, u), 0.4 + 0.2 * u, lerp(0.35, 0.05, ease(u))))
    else:
        cam = look_at(*orbit([0, 0.4, 0], lerp(4.2, 3.5, u), 1.2 + 0.25 * u, 0.25))
    draw(img, sc, cam, fade=(2, 14))


def blob(sc, c, r, col, t, seed=1):
    rng = np.random.default_rng(seed)
    bumps = rng.uniform(-0.18, 0.18, (6, 6))
    for lat in np.linspace(-1.2, 1.2, 9):
        th = np.linspace(0, 2 * math.pi, 48)
        rr = r * (1 + 0.15 * np.sin(th * 3 + lat * 2) + 0.08 * np.cos(th * 5 - lat))
        P = np.stack([c[0] + rr * np.cos(th) * math.cos(lat), np.full_like(th, c[1] + r * 0.8 * math.sin(lat)),
                      c[2] + rr * np.sin(th) * math.cos(lat) * 0.6], 1)
        sc.add(P, col, 1, closed=True)


def sh_bronze_lump(img, u, t, v, T):
    sc = Scene()
    reveal = ease((u + v) / 1.6) if True else 0
    blob(sc, [0, 0, 0], 1.3, BRONZE * (0.9 - 0.5 * reveal), t)
    gear(sc, [0.25, 0.1, 0.05], 0.6, 40, t * 0.15, WHITE * (0.2 + 0.9 * reveal), 2)
    if reveal > 0.5:
        sc.circle([0.25, 0.1, 0.05], 0.85, WHITE * (reveal - 0.5) * 1.6, 2, 64, axis="z")
    cam = look_at(*orbit([0, 0, 0], lerp(4.6, 3.6, u) - 0.4 * v, 0.2 + 0.3 * u + 0.4 * v, 0.15))
    draw(img, sc, cam, fade=(1, 9))


def sh_xray_scan(img, u, t, v, T):
    sc = Scene(); uu = (u + v) / 2
    x = -2.2 + 4.4 * ((uu * 1.2) % 1.0)
    blob(sc, [0, 0, 0], 2.1, BRONZE * 0.35, t)
    gear_train(sc, t * 0.2, 0.0, bright=0.35)
    # partie déjà balayée : engrenages en blanc
    sc2 = Scene(); gear_train(sc2, t * 0.2, 0.0, bright=1.0)
    S, C, Wd = sc2.arrays()
    keep = S[:, :, 0].max(1) < x
    sc.segs.append(S[keep]); sc.cols.append(np.repeat(WHITE[None], keep.sum(), 0) * 0.9); sc.wid.append(Wd[keep])
    sc.add([[x, -2.6, -1.2], [x, 2.6, -1.2], [x, 2.6, 1.2], [x, -2.6, 1.2]], WHITE, 3, closed=True)
    sc.box([0, 0, 0], [5.6, 6.2, 3.0], GOLD * 0.3, 1)  # cadre du scanner
    cam = look_at(*orbit([0, 0, 0], 8.0 - 0.8 * u, 0.35 + 0.5 * v + 0.15 * u, 0.2))
    draw(img, sc, cam, fade=(3, 14))


def sh_inscriptions(img, u, t, v, T):
    sc = Scene(); uu = (u + v) / 2
    sc.box([0, 0, 0], [3.0, 2.2, 0.08], BRONZE * 0.8, 2)
    r = np.random.default_rng(7)
    nl = int(14 * ease(min(1, uu * 1.3 + 0.1)))
    for k in range(nl):
        y = 0.9 - k * 0.13
        x = -1.35
        while x < 1.3:
            g = r.integers(0, 4)
            if g == 0: sc.seg([x, y - 0.04, 0.05], [x, y + 0.04, 0.05], WHITE * 0.85, 1)
            elif g == 1: sc.add([[x, y - 0.04, 0.05], [x + 0.03, y + 0.04, 0.05], [x + 0.06, y - 0.04, 0.05]], WHITE * 0.85, 1)
            elif g == 2: sc.circle([x + 0.03, y, 0.05], 0.035, WHITE * 0.85, 1, 10, axis="z")
            else: sc.add([[x, y + 0.04, 0.05], [x + 0.06, y + 0.04, 0.05], [x + 0.03, y - 0.04, 0.05]], WHITE * 0.85, 1)
            x += 0.09 + (0.07 if r.random() < 0.15 else 0)
    cam = look_at(*orbit([0.2 * (v - 0.5), 0.1, 0], lerp(4.0, 3.2, u), -0.3 + 0.6 * v + 0.15 * u, 0.15))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 9))


def zodiac_dial(sc, c, r, col):
    sc.circle(c, r, col, 2, 128, axis="z"); sc.circle(c, r * 0.86, col * 0.7, 1, 128, axis="z")
    for k in range(72):
        a = 2 * math.pi * k / 72; l = 0.14 if k % 6 == 0 else 0.06
        sc.seg([c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]],
               [c[0] + (r - l * r) * math.cos(a), c[1] + (r - l * r) * math.sin(a), c[2]], col * 0.8, 1)


def sh_crank_dials(img, u, t, v, T):
    sc = Scene()
    sc.box([0, 0, -0.25], [3.2, 4.0, 0.5], GOLD * 0.35, 1)
    zodiac_dial(sc, [0, 0.2, 0.02], 1.35, GOLD)
    a_sun = t * 0.6; a_moon = t * 0.6 * 13.37 / 4
    sc.seg([0, 0.2, 0.04], [1.1 * math.cos(a_sun), 0.2 + 1.1 * math.sin(a_sun), 0.04], AMBER, 3)
    sc.circle([1.1 * math.cos(a_sun), 0.2 + 1.1 * math.sin(a_sun), 0.04], 0.09, AMBER, 2, 16, axis="z")
    sc.seg([0, 0.2, 0.06], [0.85 * math.cos(a_moon), 0.2 + 0.85 * math.sin(a_moon), 0.06], WHITE, 2)
    mc = [0.85 * math.cos(a_moon), 0.2 + 0.85 * math.sin(a_moon), 0.07]
    sc.circle(mc, 0.1, WHITE, 2, 24, axis="z")
    ph = (math.sin(t * 1.3) + 1) / 2  # phase de la Lune
    sc.add([[mc[0] + 0.1 * math.cos(a) * (2 * ph - 1), mc[1] + 0.1 * math.sin(a), mc[2]] for a in np.linspace(-math.pi / 2, math.pi / 2, 12)], WHITE, 1)
    # manivelle sur le côté
    ca = t * 2.0
    sc.seg([1.6, -1.3, 0], [1.95, -1.3, 0], GOLD, 3)
    sc.seg([1.95, -1.3, 0], [1.95, -1.3 + 0.45 * math.cos(ca), 0.45 * math.sin(ca)], GOLD, 3)
    sc.seg([1.95, -1.3 + 0.45 * math.cos(ca), 0.45 * math.sin(ca)], [2.25, -1.3 + 0.45 * math.cos(ca), 0.45 * math.sin(ca)], WHITE, 3)
    cam = look_at(*orbit([0.2, 0, 0], lerp(5.8, 5.0, u), 0.45 + 0.3 * v + 0.1 * u, 0.12))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 12))


def sh_gear_223(img, u, t, v, T):
    sc = Scene()
    gear(sc, [0, 0, 0], 1.6, 223, t * 0.12, GOLD, 2, spokes=6, tooth=0.025, hub=0.12)
    cnt = int(223 * ease(min(1, u * 1.2)))
    for k in range(0, cnt, 1):  # dents comptées, surlignées
        a = t * 0.12 + 2 * math.pi * (k + 0.25) / 223
        sc.seg([1.6 * math.cos(a), 1.6 * math.sin(a), 0.01], [1.68 * math.cos(a), 1.68 * math.sin(a), 0.01], WHITE, 1)
    cam = look_at(*orbit([0, 0, 0], lerp(6.0, 4.6, ease(u)), 0.15 + 0.2 * u, 0.25 - 0.1 * u))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(2, 12))


def sh_olympiad_dial(img, u, t, v, T):
    sc = Scene(); c = [0, 0, 0]
    sc.circle(c, 1.3, GOLD, 3, 128, axis="z"); sc.circle(c, 0.4, GOLD * 0.7, 1, 64, axis="z")
    for k in range(4):
        a = math.pi / 2 + k * math.pi / 2
        sc.seg([0.4 * math.cos(a), 0.4 * math.sin(a), 0], [1.3 * math.cos(a), 1.3 * math.sin(a), 0], GOLD * 0.8, 2)
    step = int((T * 0.8) % 4)
    a0 = math.pi / 2 + step * math.pi / 2 + math.pi / 4
    sc.seg([0, 0, 0.02], [1.15 * math.cos(a0), 1.15 * math.sin(a0), 0.02], WHITE, 3)
    # quart actif surligné
    th = np.linspace(a0 - math.pi / 4, a0 + math.pi / 4, 24)
    sc.add(np.stack([1.38 * np.cos(th), 1.38 * np.sin(th), np.zeros_like(th)], 1), WHITE, 3)
    # anneaux olympiques stylisés (5 cercles) au centre
    for (x, y) in [(-0.2, 0.05), (0, 0.05), (0.2, 0.05), (-0.1, -0.07), (0.1, -0.07)]:
        sc.circle([x, y, 0.01], 0.09, AMBER, 1, 24, axis="z")
    cam = look_at(*orbit([0, 0, 0], lerp(4.4, 3.8, u), 0.3 - 0.3 * u, 0.3))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(1, 10))


def sh_cosmos(img, u, t, v, T):
    sc = Scene()
    sc.circle([0, 0, 0], 0.18, TEAL, 2, 24); sc.circle([0, 0, 0], 0.18, TEAL, 2, 24, axis="z")  # Terre
    radii = [0.45, 0.7, 0.95, 1.2, 1.45, 1.7, 1.95]  # Lune, Mercure, Vénus, Soleil, Mars, Jupiter, Saturne
    speeds = [2.0, 1.2, 0.9, 0.6, 0.45, 0.3, 0.2]
    for i, (r, s) in enumerate(zip(radii, speeds)):
        col = AMBER if i == 3 else (WHITE if i == 0 else GOLD)
        sc.circle([0, 0, 0], r, col * 0.55, 1, 96)
        a = t * s + i
        sc.circle([r * math.cos(a), 0, r * math.sin(a)], 0.07 if i != 3 else 0.12, col, 2, 16)
        sc.circle([r * math.cos(a), 0, r * math.sin(a)], 0.07 if i != 3 else 0.12, col, 2, 16, axis="x")
    cam = look_at(*orbit([0, 0, 0], lerp(4.2, 3.4, u), 0.3 + 0.4 * u + 0.6 * v, 0.55 - 0.15 * v))
    stars(img, cam, T, 1.0, spin=t * 0.02); draw(img, sc, cam, fade=(2, 10))


def sh_timeline_gap(img, u, t, v, T):
    # frise verticale : en bas Anticythère (~ -100), en haut les horloges astronomiques (~ 1350)
    sc = Scene(); y0, y1 = -2.6, 2.9
    sc.seg([0, y0, 0], [0, y1, 0], GOLD * 0.5, 2)
    for k in range(16):  # un trait par siècle
        y = y0 + (y1 - y0) * k / 15
        sc.seg([-0.12, y, 0], [0.12, y, 0], GOLD * 0.6, 1)
    sc.box([0, y0 - 0.45, 0], [0.7, 0.7, 0.7], BRONZE, 2, grid=2)
    gear(sc, [0, y0 - 0.45, 0.36], 0.28, 18, t * 0.5, WHITE, 1, spokes=3)
    ye = y0 + (y1 - y0) * ease(min(1, u * 1.15))
    sc.seg([0.03, y0, 0.02], [0.03, ye, 0.02], WHITE, 3)
    sc.circle([0, ye, 0.02], 0.1, WHITE, 2, 16, axis="z")
    a = ease((u - 0.7) / 0.3) if u > 0.7 else 0.0
    if a > 0:
        yc = y1 + 0.2
        sc.add([[-0.45, yc, 0], [-0.45, yc + 1.2, 0], [0, yc + 1.65, 0], [0.45, yc + 1.2, 0], [0.45, yc, 0]], GOLD * a, 2)
        zodiac_dial(sc, [0, yc + 0.75, 0.01], 0.33, WHITE * a)
    cam = look_at(*orbit([0, lerp(-0.6, 0.9, ease(u)), 0], 7.6, 0.35, 0.08))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(2, 14))


def sh_final_mechanism(img, u, t, v, T):
    sc = Scene()
    sc.grid_plane(7, 28, -2.2, TEAL * 0.25)
    for k in range(10):
        z = -6 + k * 1.2
        xs = np.linspace(-7, 7, 60)
        sc.add(np.stack([xs, 5.0 + 0.1 * np.sin(xs + t + k), np.full_like(xs, z)], 1), TEAL * 0.35, 1)
    gear_train(sc, t * 0.5)
    sc.box([0, 0, 0.1], [3.6, 3.6, 0.6], GOLD * 0.3, 1)
    cam = look_at(*orbit([0, lerp(0, 1.5, ease(u)), 0], lerp(4.8, 11.0, ease(u)), 0.6 + 0.3 * u, lerp(0.15, 0.45, u)))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 16))
