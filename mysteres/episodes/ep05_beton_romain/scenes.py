# Plans propres à l'épisode 5 : le béton romain qui se répare tout seul
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

STONE = np.array([0.55, 0.80, 0.95])    # BGR : béton clair
WATER = np.array([1.00, 0.75, 0.35])    # BGR : bleu eau
LIME = np.array([1.00, 1.00, 1.00])
HEAT = np.array([0.10, 0.35, 1.00])     # orange vif
SEA = np.array([0.85, 0.55, 0.20])


def rng_pts(seed, n, lo, hi):
    return np.random.default_rng(seed).uniform(lo, hi, (n, 3))


def crack_path(seed, a, b, n=9, amp=0.12):
    """ligne brisée de a vers b (fissure)"""
    r = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    P = [a + (b - a) * k / n for k in range(n + 1)]
    for k in range(1, n):
        P[k] = P[k] + [r.uniform(-amp, amp), 0, 0]
    return np.array(P)


def crack(sc, P, open_, col, z):
    """fissure dessinée sur la face z : deux lèvres écartées de open_ (0 = refermée)"""
    if open_ > 0.01:
        L = P + [-open_ / 2, 0, 0]; R = P + [open_ / 2, 0, 0]
        L[:, 2] = z; R[:, 2] = z
        sc.add(L, col, 2); sc.add(R, col, 2)
        for k in range(0, len(P), 2):
            sc.seg(L[k], R[k], col * 0.4, 1)
    else:
        Q = P.copy(); Q[:, 2] = z
        sc.add(Q, WHITE * 0.35, 1)


def arch(sc, c=(0, 0, 0), R=1.0, n=11, d=0.5, col=STONE, pier=1.2):
    """arc romain en voussoirs + piliers"""
    c = np.asarray(c, float); r2 = R + 0.32
    for k in range(n):
        a0, a1 = math.pi * k / n, math.pi * (k + 1) / n
        for z in (-d / 2, d / 2):
            P = [c + [R * math.cos(a0), pier + R * math.sin(a0), z], c + [r2 * math.cos(a0), pier + r2 * math.sin(a0), z],
                 c + [r2 * math.cos(a1), pier + r2 * math.sin(a1), z], c + [R * math.cos(a1), pier + R * math.sin(a1), z]]
            sc.add(P, col if k != n // 2 else col * 1.3, 2 if k == n // 2 else 1, closed=True)
        for rr in (R, r2):
            sc.seg(c + [rr * math.cos(a0), pier + rr * math.sin(a0), -d / 2], c + [rr * math.cos(a0), pier + rr * math.sin(a0), d / 2], col * 0.5, 1)
    for sx in (-1, 1):
        sc.box(c + [sx * (R + 0.16), pier / 2, 0], [0.32, pier, d], col, 2)
        sc.box(c + [sx * (R + 0.16), pier / 2, 0], [0.32, pier, d], col * 0.3, 1, grid=4)


def concrete_block(sc, c, s, col=STONE, grid=5, agg=40, seed=1, aggcol=None):
    c = np.asarray(c, float)
    sc.box(c, s, col, 2, grid=grid)
    P = rng_pts(seed, agg, -0.42, 0.42) * np.asarray(s, float) + c
    r = np.random.default_rng(seed + 9).uniform(0.03, 0.07, agg)
    for p, rr in zip(P, r):
        sc.circle(p, rr * min(s), (aggcol if aggcol is not None else col * 0.45), 1, 7, "z")


def clasts(sc, c, s, n, col, size=0.05, seed=4, pulse=None, t=0):
    P = rng_pts(seed, n, -0.38, 0.38) * np.asarray(s, float) + np.asarray(c, float)
    for i, p in enumerate(P):
        rr = size * (1 + (0.35 * math.sin(t * 4 + i) if pulse else 0))
        for ax in ("y", "z", "x"):
            sc.circle(p, rr, col, 2 if ax == "z" else 1, 14, ax)
    return P


def drops(sc, P, u, t, col, n=10, speed=1.0, stop=1.0):
    """gouttes qui coulent le long de la polyligne P (de P[0] à P[-1]) ; stop = fraction max atteinte"""
    L = len(P) - 1
    for k in range(n):
        f = ((t * speed * 0.35 + k / n) % 1.0) * stop
        x = f * L; i = min(int(x), L - 1); a = x - i
        p = P[i] + (P[i + 1] - P[i]) * a
        sc.add([p + [0, 0.035, 0], p + [0.02, 0, 0], p + [0, -0.035, 0], p + [-0.02, 0, 0]], col, 2, closed=True)


# ------------------------------------------------------------------ plans
def _arch_scene(u, t, heal):
    sc = Scene(); sc.grid_plane(5, 20, 0, GOLD * 0.10)
    arch(sc, (0, 0, 0), 1.0, 11, 0.6, STONE)
    P = crack_path(3, [0.05, 2.55, 0], [-0.15, 1.75, 0], 8, 0.08)
    crack(sc, P, 0.07 * (1 - heal), AMBER, 0.31)
    if heal > 0.01:
        Q = P.copy(); Q[:, 2] = 0.31
        n = int(1 + heal * (len(Q) - 1))
        sc.add(Q[:n + 1] if n < len(Q) else Q, WHITE, 3)
    return sc


def sh_hook_arch(img, u, t, v, T):
    heal = ease((u - 0.45) / 0.45)
    sc = _arch_scene(u, t, heal)
    cam = look_at(*orbit([0, 1.45, 0], lerp(4.4, 3.5, ease(u)), 0.35 - 0.5 * u, lerp(0.05, 0.12, u)))
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(2, 14))


def sh_final_arch(img, u, t, v, T):
    heal = ease(u / 0.6)
    sc = _arch_scene(u, t, heal)
    cam = look_at(*orbit([0, 1.4, 0], lerp(3.4, 4.8, ease(u)), -0.4 + 0.6 * u, lerp(0.15, 0.05, u)))
    stars(img, cam, T, 0.8, spin=0.1 * u); draw(img, sc, cam, fade=(2, 14))


def sh_lab_sample(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(3, 18, -0.75, GOLD * 0.10)
    concrete_block(sc, [0, 0, 0], [1.0, 1.4, 1.0], STONE, 4, 35, 2)
    y = -0.7 + 1.4 * ((u * 1.4) % 1.0)
    sc.add([[-0.75, y, -0.75], [0.75, y, -0.75], [0.75, y, 0.75], [-0.75, y, 0.75]], WATER, 2, closed=True)
    for k in range(4):  # socle de mesure
        a = k * math.pi / 2 + 0.3 * t
        sc.seg([0.9 * math.cos(a), -0.75, 0.9 * math.sin(a)], [1.2 * math.cos(a), -0.75, 1.2 * math.sin(a)], GOLD * 0.6, 2)
    sc.circle([0, -0.75, 0], 1.05, GOLD * 0.5, 1, 64)
    cam = look_at(*orbit([0, -0.05, 0], lerp(4.0, 3.3, ease(u)), 0.6 + 0.6 * u, 0.3))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 12))


def sh_lime_clasts(img, u, t, v, T):
    sc = Scene()
    concrete_block(sc, [0, 0, 0], [1.4, 1.4, 1.4], STONE * 0.7, 4, 50, 5)
    clasts(sc, [0, 0, 0], [1.4, 1.4, 1.4], 9, LIME * (0.5 + 0.5 * ease(u * 2)), 0.07, 4)
    cam = look_at(*orbit([0, 0, 0], lerp(4.6, 2.3, ease(u)), 0.3 + 0.7 * u, 0.25))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 10))


def sh_sloppy_mix(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(3, 18, -0.4, GOLD * 0.10)
    # auge de mélange
    sc.box([0, -0.1, 0], [2.0, 0.6, 1.2], GOLD * 0.8, 2)
    P = rng_pts(11, 40, -0.45, 0.45) * [2.0, 0.4, 1.2] + [0, -0.1, 0]
    for i, p in enumerate(P):
        a = t * 0.6 + i
        q = p + [0.05 * math.sin(a), 0, 0.05 * math.cos(a)]
        col = LIME * 0.8 if i % 6 == 0 else STONE * 0.5
        sc.circle(q, 0.05 if i % 6 == 0 else 0.035, col, 1, 8, "z")
    # point d'interrogation stylisé : marque rouge « erreur » qui clignote
    blink = 0.5 + 0.5 * math.sin(t * 5)
    for p in P[::6][:5]:
        sc.circle(p + [0, 0.18, 0], 0.07, np.array([0.25, 0.30, 1.0]) * blink, 1, 12, "z")
    # truelle
    a = 0.4 * math.sin(t * 1.5)
    tip = np.array([0.4 * math.sin(a), 0.1, 0.0])
    sc.add([tip + [-0.15, 0, -0.1], tip + [0.15, 0, -0.1], tip + [0, 0, 0.25]], COPPER, 2, closed=True)
    sc.seg(tip + [0, 0, -0.1], tip + [0, 0.5, -0.4], COPPER, 3)
    cam = look_at(*orbit([0, -0.05, 0], lerp(3.8, 3.2, u), -0.3 + 0.5 * u, 0.55))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 10))


def sh_hot_mix(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(3, 18, -0.4, GOLD * 0.10)
    sc.box([0, -0.1, 0], [2.0, 0.6, 1.2], GOLD * 0.8, 2)
    heat = ease(u * 1.6)
    # chaux vive qui tombe dans l'auge
    for k in range(14):
        f = (t * 0.8 + k / 14) % 1.0
        x = -0.3 + 0.6 * ((k * 0.37) % 1)
        y = 1.3 - 1.5 * f
        sc.box([x, y, 0.1 * math.sin(k)], [0.06, 0.06, 0.06], LIME, 1)
    # ondes de chaleur
    for k in range(7):
        x = -0.8 + 1.6 * k / 6
        ys = np.linspace(0.25, 0.25 + 1.1 * heat, 14)
        P = np.stack([x + 0.05 * np.sin(ys * 9 - t * 6 + k), ys, np.zeros_like(ys)], 1)
        sc.add(P, HEAT * (0.4 + 0.6 * heat), 2)
    P = rng_pts(11, 30, -0.45, 0.45) * [2.0, 0.4, 1.2] + [0, -0.1, 0]
    for i, p in enumerate(P):
        sc.circle(p, 0.04, (HEAT * heat + STONE * (1 - heat)) * 0.7, 1, 8, "z")
    cam = look_at(*orbit([0, 0.25, 0], lerp(4.2, 3.6, u), 0.2 + 0.4 * u, 0.32))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 10))


def sh_calcium_reserve(img, u, t, v, T):
    sc = Scene()
    s = [1.3, 1.9, 1.3]
    concrete_block(sc, [0, 0, 0], s, STONE * 0.45, 3, 40, 6)
    P = clasts(sc, [0, 0, 0], s, 11, LIME, 0.08, 8, pulse=True, t=t)
    for i, p in enumerate(P):  # halos de calcium
        sc.circle(p, 0.15 + 0.05 * math.sin(t * 3 + i), GOLD * 0.6, 1, 16, "z")
    cam = look_at(*orbit([0, 0, 0], lerp(4.4, 3.6, ease(u)), 1.0 + 0.6 * u, 0.15 + 0.1 * u))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 10))


def sh_crack_fill(img, u, t, v, T):
    sc = Scene()
    s = [1.6, 2.2, 0.8]
    concrete_block(sc, [0, 0, 0], s, STONE * 0.55, 4, 30, 7)
    P = crack_path(5, [0.1, 1.1, 0], [-0.1, -1.1, 0], 10, 0.14)
    heal = ease((u - 0.35) / 0.55)
    crack(sc, P, 0.12 * (1 - heal), AMBER, 0.41)
    Q = P.copy(); Q[:, 2] = 0.41
    drops(sc, Q, u, t, WATER, 7, 1.2, 1.0 - 0.6 * heal)
    # clastes de chaux le long de la fissure qui libèrent le calcium
    for k in (2, 5, 8):
        sc.circle(Q[k] + [0.18, 0, 0], 0.07 * (1 - 0.5 * heal), LIME, 2, 14, "z")
    if heal > 0:
        n = int(1 + heal * (len(Q) - 1))
        sc.add(Q[:n + 1], WHITE, 4)  # carbonate de calcium qui rebouche
        for k in range(n):
            sc.add([Q[k] + [-0.05, 0.03, 0], Q[k] + [0.05, 0.08, 0], Q[k] + [0.05, -0.02, 0]], WHITE * 0.6, 1, closed=True)
    cam = look_at(*orbit([0, 0, 0], lerp(4.6, 3.6, ease(u)), 0.15 + 0.25 * u, 0.05))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(1, 10))


def _cyl(sc, c, r, h, col, n=24):
    c = np.asarray(c, float)
    sc.circle(c + [0, -h / 2, 0], r, col, 2, n); sc.circle(c + [0, h / 2, 0], r, col, 2, n)
    for k in range(8):
        a = 2 * math.pi * k / 8
        sc.seg(c + [r * math.cos(a), -h / 2, r * math.sin(a)], c + [r * math.cos(a), h / 2, r * math.sin(a)], col * 0.6, 1)


def sh_water_test(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(3, 18, -1.1, GOLD * 0.10)
    tt = u if v == 0 else 1.0  # avancement du test (2e angle : résultat final)
    for sx, healing, lab in ((-0.75, True, GOLD), (0.75, False, np.array([0.25, 0.30, 1.0]))):
        c = np.array([sx, 0, 0])
        _cyl(sc, c, 0.45, 1.6, STONE * 0.8)
        P = crack_path(9 if healing else 13, c + [0, 0.8, 0.46], c + [0, -0.8, 0.46], 8, 0.08)
        heal = ease(tt / 0.8) if healing else 0.0
        crack(sc, P, 0.08 * (1 - heal), AMBER, 0.46)
        if heal > 0:
            Q = P.copy(); Q[:, 2] = 0.46
            sc.add(Q[:int(1 + heal * (len(Q) - 1)) + 1], WHITE, 3)
        # eau : entonnoir au-dessus, gouttes qui traversent (s'arrêtent si réparé)
        sc.add([c + [-0.3, 1.25, 0], c + [0, 0.95, 0], c + [0.3, 1.25, 0]], WATER * 0.8, 2)
        Q = np.vstack([c + [0, 0.95, 0.46], P[1:], c + [0, -1.1, 0.46]]); Q[:, 2] = 0.46
        if healing and heal > 0.95:
            for k in range(3):
                sc.circle(c + [0, 0.98 + 0.05 * k, 0.2], 0.2 - 0.04 * k, WATER * 0.6, 1, 16)
        else:
            drops(sc, Q, u, t, WATER, 8, 1.6, 1.0 - 0.9 * heal if healing else 1.0)
        if not healing:
            sc.circle(c + [0, -1.1, 0.3], 0.25 + 0.05 * math.sin(t * 4), WATER * 0.7, 1, 24)
        sc.circle(c + [0, -1.1, 0], 0.6, lab * 0.6, 2, 32)
    if v == 0:
        cam = look_at(*orbit([0, 0, 0], lerp(4.8, 4.2, u), 0.1 * math.sin(u * 2), 0.12))
    else:
        cam = look_at(*orbit([-0.4, 0, 0], lerp(3.9, 3.4, u), -0.25 + 0.2 * u, 0.2))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 10))


def sh_harbor(img, u, t, v, T):
    sc = Scene()
    # mer : grille ondulante
    N = 22
    for i in range(N + 1):
        x = -4 + 8 * i / N
        zs = np.linspace(-4, 4, 40)
        sc.add(np.stack([np.full_like(zs, x), 0.06 * np.sin(zs * 2 + t * 2 + x), zs], 1), SEA * 0.45, 1)
        sc.add(np.stack([zs, 0.06 * np.sin(x * 2 + t * 2 + zs), np.full_like(zs, x)], 1), SEA * 0.3, 1)
    # jetée courbe en blocs de béton
    for k in range(10):
        a = -0.9 + 1.8 * k / 9
        p = np.array([2.6 * math.sin(a), 0.1, 2.6 * math.cos(a) - 2.4])
        sc.box(p, [0.55, 0.9, 0.55], STONE, 2, grid=2)
    # quai et colonnes
    sc.box([0, 0.15, -2.6], [2.4, 1.0, 0.8], STONE * 0.8, 2, grid=3)
    cam = look_at(*orbit([0, 0.2, -1.4], lerp(7.0, 5.2, ease(u)), 0.5 + 0.4 * u, lerp(0.55, 0.35, u)))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(2, 16))


def sh_crystals(img, u, t, v, T):
    sc = Scene()
    s = [1.6, 1.6, 1.6]
    sc.box([0, 0, 0], s, STONE * 0.35, 1, grid=3)
    # grains de cendre volcanique (polyèdres) dissous par l'eau de mer
    P = rng_pts(31, 12, -0.6, 0.6)
    g = ease(u * 1.3)
    for i, p in enumerate(P):
        r = 0.13 * (1 - 0.4 * g)
        sc.add([p + [r, 0, 0], p + [0, r, 0], p + [-r, 0, 0], p + [0, -r, 0]], AMBER * 0.7, 1, closed=True)
        # plaquettes de cristaux qui poussent autour
        for k in range(6):
            a = k * math.pi / 3 + i
            L = 0.32 * g
            d = np.array([math.cos(a), math.sin(a), 0.5 * math.sin(a + i)])
            q = p + d * 0.12
            w = np.array([-d[1], d[0], 0]) * 0.04
            sc.add([q - w, q + w, q + w + d * L, q - w + d * L], WHITE * (0.4 + 0.6 * g), 1, closed=True)
    # eau qui percole
    for k in range(10):
        f = (t * 0.4 + k / 10) % 1
        x = -0.7 + 1.4 * ((k * 0.61) % 1)
        sc.circle([x, 0.8 - 1.6 * f, 0.3 * math.sin(k)], 0.03, WATER, 2, 8, "z")
    cam = look_at(*orbit([0, 0, 0], lerp(4.0, 2.8, ease(u)), 0.4 + 0.7 * u, 0.25))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(1, 10))


def sh_one_stone(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(4, 20, -1.0, SEA * 0.25)
    g = ease(u / 0.75)
    r = np.random.default_rng(17)
    for i in range(18):
        p = np.array([(i % 3 - 1) * 0.55, (i // 3 % 3 - 1) * 0.55, (i // 9 - 0.5) * 0.55])
        off = r.uniform(-1, 1, 3) * 0.6
        sc.box(p + off * (1 - g), [0.5, 0.5, 0.5], STONE * (0.5 + 0.2 * (1 - g)), 1)
    if g > 0.4:
        sc.box([0, 0, 0], [1.65, 1.65, 1.1], WHITE * ease((g - 0.4) / 0.6), 3)
    # vagues qui viennent frapper
    for k in range(3):
        f = (t * 0.5 + k / 3) % 1
        sc.circle([0, -0.95, 0], 2.8 - 1.6 * f, SEA * (0.2 + 0.6 * f), 1, 64)
    cam = look_at(*orbit([0, -0.1, 0], lerp(5.2, 4.2, ease(u)), 0.6 + 0.5 * u, 0.3))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(2, 12))


def sh_pantheon(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(4, 20, 0, GOLD * 0.10)
    R = 1.4; base = 1.3
    # tambour cylindrique
    sc.circle([0, 0, 0], R, STONE, 2, 64); sc.circle([0, base, 0], R, STONE, 2, 64)
    for k in range(16):
        a = 2 * math.pi * k / 16
        sc.seg([R * math.cos(a), 0, R * math.sin(a)], [R * math.cos(a), base, R * math.sin(a)], STONE * 0.5, 1)
    # coupole : parallèles + méridiens (caissons) ; s'affiche du bas vers l'oculus
    rise = ease(u * 1.5)
    for k in range(1, 9):
        e = (math.pi / 2) * k / 9
        if k / 9 > rise: break
        sc.circle([0, base + R * math.sin(e), 0], R * math.cos(e), GOLD * (0.9 - 0.05 * k), 1, 64)
    oc = math.asin(0.2)
    for k in range(28):
        a = 2 * math.pi * k / 28
        es = np.linspace(0, (math.pi / 2 - oc) * rise, 12)
        P = np.stack([R * np.cos(es) * math.cos(a), base + R * np.sin(es), R * np.cos(es) * math.sin(a)], 1)
        sc.add(P, GOLD * 0.55, 1)
    if rise > 0.97:
        sc.circle([0, base + R * math.cos(oc), 0], R * 0.2, WHITE, 3, 32)  # oculus
        # rayon de lumière par l'oculus
        sc.seg([0, base + R, 0], [0.3, 0.0, 0.3], WHITE * 0.4, 1)
    # portique
    for k in range(8):
        x = -0.9 + 1.8 * k / 7
        sc.seg([x, 0, R + 0.6], [x, base * 0.9, R + 0.6], STONE, 2)
    sc.add([[-1.05, base * 0.9, R + 0.6], [1.05, base * 0.9, R + 0.6], [0, base * 1.25, R + 0.6]], STONE, 2, closed=True)
    sc.box([0, base * 0.45, R + 0.3], [2.0, base * 0.9, 0.6], STONE * 0.4, 1)
    cam = look_at(*orbit([0, 1.2, 0.3], lerp(6.4, 5.0, ease(u)), -0.5 + 0.5 * u, lerp(0.15, 0.4, ease(u))))
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(2, 16))
