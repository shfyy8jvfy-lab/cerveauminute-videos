# Plans propres à l'épisode 4 : Göbekli Tepe
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

STONE = np.array([0.55, 0.80, 0.95])    # BGR : calcaire clair
EARTH = np.array([0.18, 0.38, 0.70])    # BGR : terre
FLINT = np.array([0.95, 0.85, 0.70])    # BGR : silex bleuté
RED = np.array([0.25, 0.30, 1.00])


def _rot(p, a):
    c, s = math.cos(a), math.sin(a)
    p = np.asarray(p, float)
    return np.stack([p[..., 0] * c + p[..., 2] * s, p[..., 1], -p[..., 0] * s + p[..., 2] * c], -1)


def obox(sc, c, size, a, col, w=2):
    """boîte orientée (rotation a autour de l'axe vertical)"""
    c = np.asarray(c, float); hx, hy, hz = np.asarray(size, float) / 2
    V = np.array([[x, y, z] for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)])
    V = _rot(V, a) + c
    for i, j in [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)]:
        sc.seg(V[i], V[j], col, w)


def face_pts(base, a, h, pts2, side=1):
    """points 2D (x le long du pilier, y en hauteur, en fraction de h) sur la face large du pilier"""
    P = np.array([[x * h, y * h, side * 0.045 * h] for x, y in pts2])
    return _rot(P, a) + np.asarray(base, float)


def tpillar(sc, base, h, a, col, w=2, arms=False, rise=1.0):
    """pilier en T : long axe local x (orienté selon a), face large vers ±z local"""
    base = np.asarray(base, float)
    hs = 0.78 * h * rise
    obox(sc, base + _rot([0, hs / 2, 0], a), [0.30 * h, hs, 0.08 * h], a, col, w)
    if rise > 0.75:
        obox(sc, base + _rot([0.07 * h, hs + 0.11 * h, 0], a), [0.50 * h, 0.22 * h, 0.10 * h], a, col, w)
    if arms and rise > 0.99:
        for side in (1, -1):
            # bras qui descendent le long de la face, mains jointes sur le ventre, ceinture
            sc.add(face_pts(base, a, h, [(-0.13, 0.74), (-0.10, 0.50), (-0.02, 0.36), (0.06, 0.34)], side), col * 0.8, max(1, w - 1))
            sc.add(face_pts(base, a, h, [(-0.15, 0.30), (0.15, 0.30)], side), col * 0.6, 1)
            sc.add(face_pts(base, a, h, [(-0.15, 0.26), (0.15, 0.26)], side), col * 0.6, 1)


def enclosure(sc, c, R, n, col, h=0.9, reveal=1.0, arms=False, wall=True):
    c = np.asarray(c, float)
    if wall:
        sc.circle(c, R + 0.18, col * 0.45, 1, 72)
        sc.circle(c + [0, 0.55 * h, 0], R + 0.18, col * 0.3, 1, 72)
        sc.circle(c, R - 0.12, col * 0.3, 1, 72)
    for k in range(n):
        th = 2 * math.pi * k / n
        f = min(max(reveal * (n + 2) - k, 0), 1)
        if f <= 0: continue
        p = c + [R * math.cos(th), 0, R * math.sin(th)]
        tpillar(sc, p, h, -th, col, 1, rise=ease(f))
    # deux piliers centraux, plus grands, face à face
    f = min(max(reveal * 1.4 - 0.2, 0), 1)
    if f > 0:
        for s in (-1, 1):
            tpillar(sc, c + [0, 0, s * 0.28 * R], 1.6 * h, 0.0, WHITE * 0.9, 2, arms=arms, rise=ease(f))


def hill(sc, c=(0, 0, 0), R=3.0, h=1.0, col=EARTH, rings=9, merid=16, cut=0.0):
    """colline en dôme (lignes de niveau + méridiens)"""
    c = np.asarray(c, float)
    for k in range(rings):
        y = h * k / rings
        r = R * math.sqrt(max(1 - y / h, 0)) if True else R
        if y < cut: continue
        sc.circle(c + [0, y, 0], r, col * (0.7 - 0.4 * k / rings), 1, 64)
    for m in range(merid):
        th = 2 * math.pi * m / merid
        ys = np.linspace(max(cut, 0), h * 0.96, 10)
        rs = R * np.sqrt(np.clip(1 - ys / h, 0, 1))
        P = np.stack([c[0] + rs * math.cos(th), c[1] + ys, c[2] + rs * math.sin(th)], 1)
        sc.add(P, col * 0.4, 1)


# ---- animaux en traits (coordonnées 2D sur la face, fraction de la hauteur du pilier)
FOX = [(-0.12, 0.55), (-0.04, 0.58), (0.04, 0.58), (0.09, 0.62), (0.12, 0.60), (0.10, 0.56), (0.05, 0.54),
       (0.05, 0.47), (0.03, 0.54), (-0.08, 0.53), (-0.09, 0.47), (-0.11, 0.53), (-0.15, 0.50)]
BOAR = [(-0.13, 0.36), (-0.06, 0.40), (0.06, 0.40), (0.12, 0.36), (0.14, 0.33), (0.10, 0.31), (0.08, 0.27),
        (0.06, 0.31), (-0.06, 0.31), (-0.08, 0.27), (-0.10, 0.31), (-0.13, 0.36)]
SNAKE = [(-0.13 + 0.26 * k / 20, 0.18 + 0.025 * math.sin(k * 1.1)) for k in range(21)]
CRANE = [(-0.06, 0.66), (-0.02, 0.70), (0.04, 0.70), (0.07, 0.74), (0.07, 0.78), (0.10, 0.80), (0.07, 0.78),
         (0.04, 0.70), (0.06, 0.62), (0.04, 0.70), (-0.02, 0.70), (-0.06, 0.66)]
VULTURE = [(-0.14, 0.62), (-0.09, 0.66), (-0.04, 0.66), (0.0, 0.70), (0.03, 0.68), (0.04, 0.66), (0.09, 0.66),
           (0.14, 0.62), (0.06, 0.62), (0.03, 0.60), (0.03, 0.54), (-0.03, 0.54), (-0.03, 0.60), (-0.06, 0.62),
           (-0.14, 0.62)]


def partial(pts, f):
    n = max(2, int(len(pts) * f + 0.999))
    return pts[:n] if f < 1 else pts


def sh_hook_hill(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(5, 20, 0, GOLD * 0.12)
    hill(sc, (0, 0, 0), 3.0, 1.1, EARTH * lerp(1.0, 0.35, ease(u))[()])
    enclosure(sc, (0, -0.95, 0), 1.0, 10, GOLD * (0.35 + 0.65 * ease(u)), 0.75)
    if v == 0:
        cam = look_at(*orbit([0, -0.3, 0], lerp(5.2, 3.8, ease(u)), 0.4 + 0.3 * u, lerp(0.40, 0.28, ease(u))))
    else:
        cam = look_at(*orbit([0, -0.6, 0], lerp(4.2, 3.2, ease(u)), 1.1 + 0.3 * u, 0.42))
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(2, 16))


def sh_context_plain(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(8, 32, -0.6, GOLD * 0.10)
    # chaîne de collines (crête) et la colline au sommet
    for k in range(-4, 5):
        if k == 0: continue
        hill(sc, (k * 1.7, -0.6, -1.4 + 0.3 * math.sin(k)), 1.3, 0.55, EARTH * 0.6, 5, 10)
    hill(sc, (0, -0.6, -1.2), 1.8, 1.0, GOLD, 8, 16)
    r = 2.1 + 0.25 * math.sin(t * 3)
    sc.circle([0, -0.58, -1.2], r, WHITE * 0.7, 2, 64)
    # plaine de Harran : champ de points au premier plan
    if v == 0:
        cam = look_at(*orbit([0, -0.4, -0.6], lerp(9.0, 7.0, ease(u)), 0.2 + 0.3 * u, lerp(1.0, 0.6, ease(u))))
    else:
        cam = look_at(*orbit([0, 0.0, -1.2], lerp(6.0, 5.0, u), -0.4 + 0.4 * u, 0.35))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 18))


def sh_gravestones(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(3, 18, 0, EARTH * 0.35)
    rng = np.random.default_rng(7)
    for k in range(9):
        x, z, a = rng.uniform(-1.1, 1.1), rng.uniform(-1.3, 0.9), rng.uniform(0, math.pi)
        # seules les têtes des piliers affleurent : prises pour des stèles
        obox(sc, [x, 0.08, z], [0.42, 0.16, 0.1], a, STONE * 0.8, 2)
        sc.seg([x, 0.16, z], [x, 0.36, z], AMBER * 0.6 * (1 - ease(u)), 1)
        sc.seg([x - 0.07, 0.30, z], [x + 0.07, 0.30, z], AMBER * 0.6 * (1 - ease(u)), 1)
    cam = look_at(*orbit([0, 0.1, -0.2], lerp(3.6, 3.0, u), 0.5 + 0.4 * u + v, 0.6))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 12))


def arrowhead(sc, p, s, a, col):
    P = np.array([[0, 0, -0.5], [0.22, 0, 0.15], [0.08, 0, 0.5], [-0.08, 0, 0.5], [-0.22, 0, 0.15]]) * s
    sc.add(_rot(P, a) + p, col, 2, closed=True)
    sc.seg(_rot(np.array([0, 0, -0.5]) * s, a) + p, _rot(np.array([0, 0, 0.5]) * s, a) + p, col * 0.5, 1)


def sh_flint_dig(img, u, t, v, T):
    sc = Scene()
    uu = (u + v) / 2 if v < 2 else u
    rng = np.random.default_rng(4)
    if v == 0:
        sc.grid_plane(2, 12, 0, EARTH * 0.4)
        for k in range(7):
            p = np.array([rng.uniform(-0.9, 0.9), 0.01, rng.uniform(-0.9, 0.9)])
            arrowhead(sc, p, 0.45, rng.uniform(0, 6) + 0.2 * t, FLINT)
        cam = look_at(*orbit([0, 0, 0], lerp(3.4, 2.6, u), 0.3 + 0.3 * u, 0.9))
        draw(img, sc, cam, fade=(1, 10)); return
    # la fouille : la terre s'abaisse et révèle le cercle
    d = ease(u)
    sc.grid_plane(4, 16, 0, EARTH * 0.3)
    sc.box([0, -0.5, 0], [3.0, 1.0, 3.0], EARTH * 0.6, 1)
    enclosure(sc, (0, -1.0, 0), 1.1, 10, GOLD, 0.8, reveal=0.15 + 0.85 * d)
    cam = look_at(*orbit([0, -0.6, 0], lerp(5.0, 4.0, u), 0.8 + 0.4 * u, 0.6))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 12))


def sh_giant_pillars(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(3, 16, 0, GOLD * 0.15)
    for s in (-1, 1):
        tpillar(sc, [s * 0.95, 0, 0], 2.4, 0.0 if s < 0 else math.pi, GOLD if s < 0 else WHITE * 0.9, 3, arms=True)
    # silhouette humaine à l'échelle (≈ 1/3 de la hauteur)
    p = np.array([0.0, 0, 0.7]); s = 0.75
    hip = p + [0, 0.45 * s, 0]; neck = p + [0, 0.85 * s, 0]
    sc.seg(p + [-0.08, 0, 0], hip, AMBER, 2); sc.seg(p + [0.08, 0, 0], hip, AMBER, 2); sc.seg(hip, neck, AMBER, 2)
    sc.seg(neck, neck + [-0.12, -0.3 * s, 0], AMBER, 2); sc.seg(neck, neck + [0.12, -0.3 * s, 0], AMBER, 2)
    sc.circle(neck + [0, 0.08, 0], 0.07, AMBER, 2, 12, axis="z")
    if v == 0:
        cam = look_at(*orbit([0, 1.2, 0], lerp(5.6, 4.6, ease(u)), 0.35 - 0.3 * u, lerp(-0.05, 0.12, u)))
    else:
        cam = look_at(*orbit([0, 1.4, 0], 4.4 - 0.4 * u, -0.5 + 0.3 * u, -0.1))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 12))


def sh_bestiary(img, u, t, v, T):
    sc = Scene(); h = 3.0
    tpillar(sc, [0, -1.4, 0], h, 0.0, STONE * 0.7, 2)
    for k, (pts, col) in enumerate([(FOX, GOLD), (CRANE, WHITE), (BOAR, AMBER), (SNAKE, GOLD)]):
        f = min(max(u * 4.5 - k * 0.9, 0), 1)
        if f > 0:
            sc.add(face_pts([0, -1.4, 0], 0.0, h, partial(pts, f), 1), col, 3)
    cam = look_at(*orbit([0, 0.0, 0], lerp(3.6, 3.0, u), 0.25 - 0.4 * u, 0.05))
    draw(img, sc, cam, fade=(1, 10))


def sh_vulture_pillar(img, u, t, v, T):
    sc = Scene(); h = 3.0
    tpillar(sc, [0, -1.4, 0], h, 0.0, STONE * 0.7, 2)
    f = ease(min(u * 1.8, 1))
    sc.add(face_pts([0, -1.4, 0], 0.0, h, partial(VULTURE, f), 1), WHITE, 3)
    sc.add(face_pts([0, -1.4, 0], 0.0, h, [(-0.10, 0.44), (-0.06, 0.47), (-0.02, 0.44), (-0.06, 0.41), (-0.10, 0.44)], 1), GOLD * 0.8, 2)  # disque
    sc.add(face_pts([0, -1.4, 0], 0.0, h, [(0.02, 0.40), (0.05, 0.44), (0.08, 0.40), (0.13, 0.42)], 1), GOLD * 0.6, 2)   # scorpion stylisé
    for k, pts in enumerate([FOX, SNAKE]):
        sc.add(face_pts([0, -1.4, 0], 0.0, h, pts, 1), GOLD * 0.25, 1)
    cam = look_at(*orbit([0, 0.35, 0], lerp(3.2, 2.4, ease(u)), -0.3 + 0.35 * u, 0.1))
    draw(img, sc, cam, fade=(1, 10))


def sh_empty_site(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(4, 20, 0, GOLD * 0.12)
    enclosure(sc, (0, 0, 0), 1.0, 10, GOLD, 0.7)
    # maisons, foyers, fosses « fantômes » qui s'effacent
    fade_ = 1 - ease(u * 1.3)
    for k, (x, z) in enumerate([(-2.4, 1.0), (2.3, 0.6), (-1.6, -2.2), (1.8, -2.0), (0.3, 2.5)]):
        a = max(fade_ - 0.12 * k, 0)
        if a <= 0: continue
        sc.box([x, 0.25, z], [0.7, 0.5, 0.6], AMBER * a, 1)
        sc.add([[x - 0.35, 0.5, z - 0.3], [x, 0.8, z - 0.3], [x + 0.35, 0.5, z - 0.3]], AMBER * a, 1)
        sc.circle([x + 0.7, 0.01, z], 0.18, RED * a, 1, 16)
    cam = look_at(*orbit([0, 0.3, 0], lerp(5.0, 4.0, u), 0.3 + 0.35 * u + 0.8 * v, 0.5))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 14))


def sh_quarry(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(3, 14, 0, STONE * 0.25)
    # banc de calcaire et pilier couché à demi dégagé
    sc.box([0, -0.25, 0], [4.0, 0.5, 2.6], STONE * 0.4, 1, grid=4)
    cut = ease(u)
    L = 3.2
    obox(sc, [0, -0.1, 0], [L, 0.2, 0.8], 0.0, GOLD, 2)
    obox(sc, [-L / 2 + 0.3, -0.1, 0], [0.6, 0.2, 1.3], 0.0, GOLD, 2)  # tête du T
    # tranchée creusée autour
    sc.add([[-L / 2 - 0.15, 0.0, -0.8], [L / 2 + 0.15, 0.0, -0.8], [L / 2 + 0.15, 0.0, 0.8], [-L / 2 - 0.15, 0.0, 0.8]], AMBER, 2, closed=True)
    # éclats de silex qui sautent le long de la tranchée
    x = lerp(-L / 2, L / 2, cut)[()]
    rng = np.random.default_rng(int(t * 8))
    for k in range(6):
        d = np.array([rng.uniform(-0.3, 0.3), rng.uniform(0.1, 0.4), rng.uniform(-0.2, 0.2)])
        p = np.array([x, 0.02, 0.8 if k % 2 else -0.8])
        sc.seg(p, p + d, FLINT, 1)
    if v == 0:
        cam = look_at(*orbit([0, -0.1, 0], lerp(4.2, 3.6, u), 0.5 + 0.3 * u, 0.75))
    else:
        cam = look_at(*orbit([0.3, -0.1, 0], 3.4, -0.6 + 0.3 * u, 0.4))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 12))


def trilithon(sc, p, s, col):
    for dx in (-0.25, 0.25):
        sc.box(p + [dx * s, 0.4 * s, 0], [0.18 * s, 0.8 * s, 0.14 * s], col, 1)
    sc.box(p + [0, 0.86 * s, 0], [0.75 * s, 0.12 * s, 0.14 * s], col, 1)


def sh_timeline(img, u, t, v, T):
    sc = Scene()
    # axe du temps : -10 000 (gauche) -> aujourd'hui (droite)
    X = lambda yr: -1.5 + 3.0 * (yr + 10000) / 12000
    sc.seg([X(-10000), 0, 0], [X(2000), 0, 0], GOLD * 0.5, 2)
    for yr in range(-10000, 2001, 1000):
        sc.seg([X(yr), -0.08, 0], [X(yr), 0.08, 0], GOLD * 0.4, 1)
    g = np.array([X(-9500), 0.0, 0.0])
    sc.circle(g + [0, 0.02, 0], 0.32, WHITE, 2, 40)
    for k in range(8):
        th = 2 * math.pi * k / 8
        tpillar(sc, g + [0.32 * math.cos(th), 0, 0.32 * math.sin(th)], 0.35, -th, WHITE, 1)
    a = ease(min(u * 1.6, 1))
    st = np.array([X(-3000), 0, 0])
    if a > 0.4:
        trilithon(sc, st, 0.6, AMBER)
    py = np.array([X(-2560), 0, 0.6])
    if a > 0.75:
        sc.pyramid(half=0.25, h=0.32, courses=6, col=GOLD * 0.7, c=py)
    # barre de « 6 000 ans » qui s'étend
    e = lerp(g, st, a)
    sc.seg(g + [0, 0.9, 0], e + [0, 0.9, 0], WHITE, 3)
    sc.seg(g + [0, 0.8, 0], g + [0, 1.0, 0], WHITE, 2)
    if a > 0.98:
        sc.seg(st + [0, 0.8, 0], st + [0, 1.0, 0], WHITE, 2)
    cam = look_at(*orbit([-0.5, 0.35, 0], lerp(3.6, 3.2, u), 0.12 * math.sin(t * 0.3), 0.32))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 12))


ENC = [(0.0, 0.0), (1.4, 0.4), (-1.3, 0.6), (0.5, -1.4), (-0.8, -1.2), (2.0, -0.7), (-2.0, -0.6),
       (0.9, 1.7), (-0.6, 1.9), (1.9, 1.3), (-1.9, 1.6), (2.3, 0.3), (-2.5, 0.4), (0.2, 2.6),
       (1.5, -1.9), (-1.5, -2.0), (0.0, -2.5), (2.6, -1.6), (-2.6, -1.6), (1.1, 2.6)]


def sh_geo_scan(img, u, t, v, T):
    sc = Scene()
    hill(sc, (0, 0, 0), 3.4, 0.8, EARTH * 0.5, 7, 16)
    sc.grid_plane(3.4, 24, -0.6, GOLD * 0.08)
    uu = (u + v) / 2 if T > 0 else u
    zs = lerp(-3.2, 3.2, ease(min(uu * 1.25, 1)))[()]
    sc.add([[-3.4, -0.55, zs], [3.4, -0.55, zs], [3.4, 0.9, zs], [-3.4, 0.9, zs]], WHITE * 0.7, 2, closed=True)
    for k, (x, z) in enumerate(ENC):
        if z > zs: continue
        col = GOLD if k < 4 else AMBER * 0.85
        R = 0.42 if k < 4 else 0.34
        sc.circle([x, -0.6, z], R, col, 2, 40)
        for j in range(8):
            th = 2 * math.pi * j / 8
            sc.seg([x + R * math.cos(th), -0.6, z + R * math.sin(th)], [x + R * math.cos(th), -0.45, z + R * math.sin(th)], col * 0.8, 1)
    cam = look_at(*orbit([0, -0.4, 0], lerp(8.2, 7.2, u), 0.3 + 0.3 * u + 0.6 * v, lerp(1.05, 0.9, u)))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 18))


def sh_final_ring(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(4, 18, 0, GOLD * 0.10)
    enclosure(sc, (0, 0, 0), 1.3, 12, GOLD, 0.9, arms=True)
    if v == 0:
        cam = look_at(*orbit([0, 0.6, 0], lerp(5.5, 4.4, ease(u)), 0.3 + 0.5 * u, 0.2))
    else:
        cam = look_at(*orbit([0, 0.7, 0], 3.0, 2.0 + 0.6 * u, 0.12))
    stars(img, cam, T, 1.0, spin=0.02 * T); draw(img, sc, cam, fade=(1, 14))


def sh_final_hill(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(6, 24, 0, GOLD * 0.10)
    a = ease(min(u * 1.5, 1))
    hill(sc, (0, 0, 0), 3.4, 1.2, EARTH * (0.2 + 0.8 * a))
    for k, (x, z) in enumerate(ENC[:12]):
        sc.circle([x * 0.85, -0.7, z * 0.85], 0.32, GOLD * (1.0 - 0.75 * a) if k else WHITE * (1 - 0.5 * a), 2, 32)
    cam = look_at(*orbit([0, 0.0, 0], lerp(5.2, 7.5, ease(u)), 0.9 + 0.4 * u, lerp(0.35, 0.5, u)))
    stars(img, cam, T, 1.0); draw(img, sc, cam, fade=(2, 20))
