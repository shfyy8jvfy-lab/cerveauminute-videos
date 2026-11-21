# Plans propres à l'épisode 14 : la pierre d'autel de Stonehenge, venue d'Écosse
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

GREEN = np.array([0.55, 0.95, 0.55])     # BGR : grès vert pâle
SEA = np.array([0.95, 0.55, 0.20])       # bleu
ICE = np.array([1.00, 0.90, 0.70])
RED = np.array([0.25, 0.25, 1.00])
R14 = np.random.default_rng(14)
GRN = R14.uniform(-1, 1, (70, 5))

# contour grossier de la Grande-Bretagne (lon, lat)
GB = [(-5.7, 50.06), (-5.2, 49.96), (-4.1, 50.35), (-3.4, 50.6), (-2.45, 50.55), (-1.3, 50.75), (-0.8, 50.75),
      (0.3, 50.8), (1.35, 51.13), (0.9, 51.45), (1.3, 51.95), (1.75, 52.48), (1.3, 52.93), (0.3, 52.85),
      (0.1, 53.6), (-0.1, 54.1), (-0.6, 54.5), (-1.4, 55.0), (-2.0, 55.77), (-2.6, 56.05), (-2.6, 56.28),
      (-2.08, 57.15), (-2.0, 57.69), (-3.0, 57.68), (-4.2, 57.5), (-3.8, 57.85), (-3.08, 58.44), (-3.03, 58.64),
      (-3.37, 58.67), (-5.0, 58.62), (-5.3, 57.9), (-5.8, 57.3), (-5.8, 56.95), (-6.0, 56.4), (-5.7, 55.3),
      (-4.6, 55.45), (-5.0, 54.9), (-3.5, 54.95), (-3.2, 54.1), (-3.0, 53.4), (-4.5, 53.3), (-4.7, 52.8),
      (-4.1, 52.4), (-5.3, 51.88), (-4.0, 51.6), (-2.7, 51.6), (-3.0, 51.35), (-3.5, 51.2), (-4.5, 51.0),
      (-5.1, 50.4)]
ORK = [(-3.4, 58.85), (-2.8, 58.85), (-2.6, 59.1), (-3.0, 59.3), (-3.4, 59.1)]
STH = (-1.83, 51.18)        # Stonehenge
PRE = (-4.7, 51.97)         # Preseli (pierres bleues)
CAI = (-3.4, 58.35)         # Caithness
MOR = (-3.6, 57.55)         # Moray


def mp(lon, lat, y=0.0):
    return np.array([(lon + 2.5) * 0.62, y, -(lat - 54.5)]) * 0.9


def britain(sc, col=GOLD, b=1.0):
    sc.add([mp(*p) for p in GB], col * b, 2, closed=True)
    sc.add([mp(*p) for p in ORK], col * b, 1, closed=True)
    sc.grid_plane(6, 24, -0.02, col * 0.07 * b)


def marker(sc, p, col, r=0.12, t=0.0):
    c = mp(*p)
    for k in range(3):
        sc.circle(c, r * (1 + 0.6 * k + 0.25 * math.sin(3 * t + k)), col * (1 - 0.3 * k), 2 if k == 0 else 1, 32)
    sc.seg(c, c + [0, 0.5, 0], col, 2)


def arc(sc, a, b, f, col, h=0.6, w=3):
    A, B = mp(*a), mp(*b)
    n = max(2, int(40 * f))
    P = [A + (B - A) * s + [0, h * 4 * s * (1 - s), 0] for s in np.linspace(0, f, n)]
    sc.add(P, col, w)


def altar(sc, c=(0, 0, 0), col=GREEN, broken=True, b=1.0):
    """Pierre d'autel : 4,9 x 0,5 x 1,0 m couchée, brisée en deux."""
    c = np.asarray(c, float)
    if broken:
        sc.box(c + [-1.25, 0.25, 0], [2.35, 0.5, 1.0], col * b, 2, grid=4)
        sc.box(c + [1.27, 0.24, 0.04], [2.35, 0.48, 1.0], col * b, 2, grid=4)
        for z in np.linspace(-0.5, 0.5, 6):
            sc.seg(c + [0.0, 0.5, z], c + [0.08, 0.0, z + 0.05], WHITE * 0.4 * b, 1)
    else:
        sc.box(c + [0, 0.25, 0], [4.9, 0.5, 1.0], col * b, 2, grid=6)


def sarsen(sc, c, h=4.1, w=2.1, d=1.1, col=GOLD, yaw=0.0, lying=False, b=1.0):
    c = np.asarray(c, float)
    cy, sy = math.cos(yaw), math.sin(yaw)
    R = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    hx, hy, hz = (h / 2, d / 2, w / 2) if lying else (w / 2, h / 2, d / 2)
    V = np.array([[x, y, z] for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]) @ R.T + c
    for i, j in [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)]:
        sc.seg(V[i], V[j], col * b, 2)
    for k in range(1, 4):
        f = -1 + k / 2
        a, bb = (np.array([f * hx, -hy, hz]), np.array([f * hx, hy, hz])) if lying else (np.array([-hx, f * hy, hz]), np.array([hx, f * hy, hz]))
        sc.seg(a @ R.T + c, bb @ R.T + c, col * 0.4 * b, 1)


def henge(sc, b=1.0, fallen=True):
    """Cercle de sarsens + linteaux, fer à cheval de trilithes, pierres bleues, pierre d'autel."""
    R = 15.0
    for k in range(30):
        a = 2 * math.pi * k / 30
        if k in (8, 9, 21): continue  # quelques manquantes
        sarsen(sc, [R * math.sin(a), 2.05, R * math.cos(a)], h=4.1, w=2.0, d=1.0, yaw=a, b=0.8 * b)
    for k in range(30):
        if k in (7, 8, 9, 20, 21, 22, 23): continue
        a0, a1 = 2 * math.pi * (k - 0.45) / 30, 2 * math.pi * (k + 0.45) / 30
        sc.seg([R * math.sin(a0), 4.4, R * math.cos(a0)], [R * math.sin(a1), 4.4, R * math.cos(a1)], GOLD * 0.8 * b, 2)
        sc.seg([R * math.sin(a0), 4.1, R * math.cos(a0)], [R * math.sin(a1), 4.1, R * math.cos(a1)], GOLD * 0.5 * b, 1)
    # bluestones
    for k in range(40):
        a = 2 * math.pi * k / 40
        sc.box([11.5 * math.sin(a), 0.9, 11.5 * math.cos(a)], [0.6, 1.8, 0.4], AMBER * 0.6 * b, 1)
    # trilithes en fer à cheval (ouvert vers le nord-est, ici +z)
    tri = [(-7.5, 3.0, 6.0), (-6.5, -2.5, 6.6), (0.0, -6.0, 7.3), (6.5, -2.5, 6.6), (7.5, 3.0, 6.0)]
    for i, (x, z, h) in enumerate(tri):
        yaw = math.atan2(x, z)
        if fallen and i == 2:
            continue
        for s in (-1, 1):
            off = np.array([math.cos(yaw), 0, -math.sin(yaw)]) * 1.2 * s
            sarsen(sc, np.array([x, h / 2, z]) + off, h=h, w=1.9, d=1.1, yaw=yaw, b=b)
        sarsen(sc, [x, h + 0.5, z], h=4.6, w=1.0, d=1.0, yaw=yaw + math.pi / 2, lying=True, b=b)
    if fallen:
        # grand trilithe : un montant debout, un montant et le linteau couchés sur la pierre d'autel
        sarsen(sc, [-1.2, 3.65, -6.0], h=7.3, w=1.9, d=1.1, b=b)
        sarsen(sc, [0.6, 0.55, -3.2], h=7.3, w=1.9, d=1.1, yaw=1.25, lying=True, col=GOLD, b=b)
        sarsen(sc, [-0.8, 0.5, -2.2], h=4.6, w=1.0, d=1.0, yaw=0.2, lying=True, col=GOLD, b=b)
    altar(sc, c=(0, 0, -3.0), b=1.3 * b)


# ------------------------------------------------------------------ plans
def sh_hook_altar(img, u, t, v, T):
    """Le monument vu de haut, puis plongée sur la pierre verte au centre."""
    sc = Scene(); henge(sc, b=lerp(1.0, 0.55, ease(u))[()])
    sc.grid_plane(24, 24, 0, GOLD * 0.07)
    cam = look_at(*orbit(lerp([0, 0, 0], [0, 0.3, -3.0], ease(u)), lerp(44, 15, ease(u)), 0.6 + 0.35 * u, lerp(0.75, 0.55, u)))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(8, 70))


def sh_hook_map(img, u, t, v, T):
    sc = Scene(); britain(sc)
    marker(sc, STH, GREEN, t=t)
    arc(sc, CAI, STH, ease(u * 1.3), GREEN, h=1.2)
    marker(sc, CAI, RED * (0.4 + 0.6 * abs(math.sin(4 * t))), r=0.3, t=t)
    for k in range(5):
        a = 2 * math.pi * k / 5 + t
        sc.seg(mp(*CAI, 0.6) + [0.5 * math.cos(a), 0, 0.5 * math.sin(a)], mp(*CAI, 0.6), WHITE * 0.3, 1)
    cam = look_at(*orbit(mp(-2.6, 54.5), lerp(8.0, 7.2, ease(u)), 0.08 * math.sin(0.3 * T), 1.3))
    draw(img, sc, cam, fade=(4, 16))


def sh_circle_overview(img, u, t, v, T):
    sc = Scene(); henge(sc); sc.grid_plane(30, 30, 0, GOLD * 0.08)
    cam = look_at(*orbit([0, 2, 0], 38, 2.3 + 0.5 * u, 0.32))
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(10, 70))


def sh_altar_close(img, u, t, v, T):
    sc = Scene(); altar(sc, broken=False, b=1.2); sc.grid_plane(4, 16, 0, GOLD * 0.12)
    # échelle : 4,9 m
    sc.seg([-2.45, 0, 0.9], [2.45, 0, 0.9], WHITE * 0.8, 2)
    for x in (-2.45, 2.45): sc.seg([x, 0, 0.8], [x, 0, 1.0], WHITE * 0.8, 2)
    # silhouette humaine stylisée (1,7 m) pour l'échelle
    sc.box([3.3, 0.85, 0], [0.45, 1.7, 0.25], WHITE * 0.35, 1)
    cam = look_at(*orbit([0.5, 0.4, 0], lerp(9.0, 7.8, ease(u)), 0.35 + 0.3 * u, 0.42))
    draw(img, sc, cam, fade=(3, 16))


def sh_trilithon_fall(img, u, t, v, T):
    sc = Scene(); f = ease(u * 1.4)
    altar(sc, c=(0, 0, 0), b=1.3)
    sc.grid_plane(8, 16, 0, GOLD * 0.1)
    sarsen(sc, [-1.2, 3.65, -2.8], h=7.3, w=1.9, d=1.1, b=0.9)
    # montant qui bascule puis linteau qui tombe
    ang = lerp(0, 1.45, f)[()]
    piv = np.array([1.2, 0, -2.8])
    ctr = piv + np.array([0, 3.65 * math.cos(ang), 3.65 * math.sin(ang)])
    sc_up = Scene()
    hx, hy, hz = 0.95, 3.65, 0.55
    Rx = np.array([[1, 0, 0], [0, math.cos(ang), -math.sin(ang)], [0, math.sin(ang), math.cos(ang)]])
    V = np.array([[x, y, z] for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]) @ Rx.T + ctr
    for i, j in [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)]:
        sc.seg(V[i], V[j], GOLD, 2)
    ly = lerp(7.8, 0.9, ease(u * 1.6 - 0.2))[()]
    sarsen(sc, [0.0, ly, lerp(-2.8, 0.6, ease(u * 1.6 - 0.2))[()]], h=4.6, w=1.0, d=1.0, yaw=0.15, lying=True, b=1.0)
    cam = look_at(*orbit([0, 1.8, -0.6], 15.5, 0.95 + 0.25 * u, 0.3))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(5, 30))


def sh_wales_map(img, u, t, v, T):
    sc = Scene(); britain(sc)
    marker(sc, STH, GREEN, t=t)
    marker(sc, PRE, AMBER, r=0.2, t=t)
    arc(sc, PRE, STH, ease(u * 1.5), AMBER, h=0.5)
    # point d'interrogation clignotant
    q = 0.4 + 0.6 * abs(math.sin(3 * t))
    c = mp(*PRE, 0.9)
    sc.add([c + [0.25 * math.cos(a), 0.25 * math.sin(a) + 0.25, 0] for a in np.linspace(2.6, -1.2, 14)] + [c + [0, 0.12, 0], c + [0, -0.05, 0]], WHITE * q, 3)
    sc.seg(c + [0, -0.18, 0], c + [0, -0.24, 0], WHITE * q, 4)
    cam = look_at(*orbit(mp(-3.2, 51.8), lerp(5.2, 4.4, ease(u)), 0.2, 0.95))
    draw(img, sc, cam, fade=(3, 12))


def sh_microscope(img, u, t, v, T):
    """Lame mince : un fragment de la pierre, et la mise au point."""
    sc = Scene()
    sc.box([0, 0, 0], [3.0, 0.05, 1.4], WHITE * 0.6, 2)
    # fragment
    P = [[-0.7, 0.04, -0.3], [-0.2, 0.04, -0.55], [0.6, 0.04, -0.4], [0.8, 0.04, 0.2], [0.2, 0.04, 0.5], [-0.6, 0.04, 0.35]]
    sc.add(P, GREEN, 2, closed=True)
    for g in GRN[:30]:
        c = [g[0] * 0.6, 0.05, g[1] * 0.35]
        sc.circle(c, 0.03 + 0.02 * abs(g[2]), AMBER, 1, 8)
    # objectif
    y0 = lerp(2.6, 1.2, ease(u))[()]
    for k in range(6):
        sc.circle([0, y0 + 0.3 * k, 0], 0.35 + 0.05 * (k > 2), GOLD * 0.8, 2 if k in (0, 5) else 1, 40)
    for a in range(0, 360, 45):
        q = math.radians(a)
        sc.seg([0.35 * math.cos(q), y0, 0.35 * math.sin(q)], [0.4 * math.cos(q), y0 + 1.5, 0.4 * math.sin(q)], GOLD * 0.5, 1)
    sc.circle([0, 0.05, 0], 0.9 * ease(u), WHITE * 0.5, 1, 64)
    cam = look_at(*orbit([0, 0.7, 0], 4.6, 0.6 + 0.3 * u, 0.45))
    draw(img, sc, cam, fade=(2, 12))


def crystal(sc, c, s, col, rot):
    """Prisme bipyramidé (zircon stylisé)."""
    c = np.asarray(c, float)
    ring = lambda y: [c + [s * 0.4 * math.cos(rot + k * math.pi / 2), y, s * 0.4 * math.sin(rot + k * math.pi / 2)] for k in range(4)]
    lo, hi = ring(-s * 0.5), ring(s * 0.5)
    sc.add(lo, col, 2, closed=True); sc.add(hi, col, 2, closed=True)
    for a, b in zip(lo, hi):
        sc.seg(a, b, col, 2); sc.seg(a, c + [0, -s, 0], col * 0.8, 1); sc.seg(b, c + [0, s, 0], col * 0.8, 1)


def sh_grains(img, u, t, v, T):
    _grains(img, u, t, 0, T)


def sh_grain_clock(img, u, t, v, T):
    _grains(img, u, t, 1, T)


def _grains(img, u, t, v, T):
    sc = Scene()
    cols = [GOLD, AMBER, WHITE * 0.8]
    if v == 0:
        for i, (x, col) in enumerate(zip((-1.3, 0, 1.3), cols)):
            crystal(sc, [x * 0.9, 1.3 * (1 - i) + 0.15 * math.sin(t + i), 0], 0.75, col, 0.6 * t + i)
        cam = look_at(*orbit([0, 0, 0], lerp(5.6, 4.8, ease(u)), 0.25 * u, 0.12))
    else:
        # un grain-horloge : cadran et aiguille qui remonte le temps
        crystal(sc, [0, 0, 0], 1.0, GOLD, 0.4 * t)
        sc.circle([0, 0, 0], 1.7, WHITE * 0.6, 2, 72, "z")
        for k in range(12):
            a = 2 * math.pi * k / 12
            sc.seg([1.55 * math.cos(a), 1.55 * math.sin(a), 0], [1.7 * math.cos(a), 1.7 * math.sin(a), 0], WHITE * 0.7, 2)
        a = math.pi / 2 + 12 * ease(u)
        sc.seg([0, 0, 0.1], [1.4 * math.cos(a), 1.4 * math.sin(a), 0.1], AMBER, 3)
        a2 = math.pi / 2 + 1.5 * ease(u)
        sc.seg([0, 0, 0.1], [0.9 * math.cos(a2), 0.9 * math.sin(a2), 0.1], WHITE, 3)
        cam = look_at(*orbit([0, 0, 0], 5.0, 0.15 * math.sin(0.5 * T), 0.08))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 14))


def sh_scotland_route(img, u, t, v, T):
    sc = Scene(); britain(sc)
    # bassin des Orcades : zone hachurée autour du Caithness / Moray / Orcades
    c = mp(-3.2, 58.4)
    for k in range(4):
        sc.circle(c, 0.6 + 0.25 * k, RED * (0.9 - 0.18 * k), 2 if k == 0 else 1, 48)
    marker(sc, STH, GREEN, t=t)
    arc(sc, STH, (-3.2, 58.4), ease(u * 1.4), GREEN, h=1.6)
    cam = look_at(*orbit(lerp(mp(-2.4, 54.0), mp(-2.8, 55.5), ease(u)), lerp(8.0, 7.0, ease(u)), 0.05, 1.3))
    draw(img, sc, cam, fade=(3, 15))


def sh_glacier(img, u, t, v, T):
    """Calotte glaciaire : flèches qui partent vers le nord, à l'inverse du trajet."""
    sc = Scene(); britain(sc, b=0.6)
    ice = [(-6.5, 54.5), (-3.0, 53.8), (0.5, 54.5), (0.8, 59.0), (-3.0, 59.8), (-6.8, 58.5)]
    sc.add([mp(*p, 0.15) for p in ice], ICE * 0.8, 2, closed=True)
    for k in range(5):
        x = -5 + 1.2 * k; f = ease(u * 1.3)
        a, b = mp(x, 55.2, 0.2), mp(x + 0.2, 55.2 + 3.0 * f, 0.2)
        sc.seg(a, b, ICE, 3)
        d = b - a; n = np.linalg.norm(d) + 1e-6; d /= n; pz = np.array([-d[2], 0, d[0]])
        sc.seg(b, b - 0.25 * d + 0.15 * pz, ICE, 3); sc.seg(b, b - 0.25 * d - 0.15 * pz, ICE, 3)
    marker(sc, STH, GREEN, t=t)
    # croix rouge
    c = mp(-2.5, 54.0, 0.4); q = ease(u * 2 - 0.8)
    sc.seg(c + [-0.8 * q, 0, -0.8 * q], c + [0.8 * q, 0, 0.8 * q], RED, 5)
    sc.seg(c + [-0.8 * q, 0, 0.8 * q], c + [0.8 * q, 0, -0.8 * q], RED, 5)
    cam = look_at(*orbit(mp(-2.6, 55.0), 7.8, 0.08 * math.sin(0.3 * T), 1.3))
    draw(img, sc, cam, fade=(3, 15))


def sh_sea_boat(img, u, t, v, T):
    """Grand radeau / embarcation de planches portant la pierre, sur la houle."""
    sc = Scene()
    for k in range(22):
        z = -7 + k * 0.7
        xs = np.linspace(-9, 9, 90)
        sc.add(np.stack([xs, 0.06 * np.sin(xs * 1.6 + t * 1.8 + k), np.full_like(xs, z)], 1), SEA * 0.5, 1)
    x0 = lerp(-1.2, 1.2, u)[()]; bob = 0.05 * math.sin(1.5 * t)
    L, Wd = 6.0, 1.8
    for f in np.linspace(-1, 1, 11):
        x = x0 + f * L / 2; w = Wd * (1 - f * f * 0.6)
        sc.add([[x, 0.35 + bob, -w / 2], [x, -0.1 + bob, 0], [x, 0.35 + bob, w / 2]], GOLD * 0.8, 1)
    xs = np.linspace(-1, 1, 30)
    for side in (-1, 1):
        sc.add(np.stack([x0 + xs * L / 2, 0.35 + bob + 0.1 * xs ** 2, side * Wd / 2 * (1 - xs ** 2 * 0.6)], 1), GOLD, 2)
    altar(sc, c=(x0, 0.35 + bob, 0), broken=False, col=GREEN, b=1.2)
    cam = look_at(*orbit([x0 * 0.7, 0.4, 0], 10.0, 0.6, 0.25))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(4, 25))


def sh_search_orkney(img, u, t, v, T):
    _search(img, u, t, 0, T)


def sh_search_caithness(img, u, t, v, T):
    _search(img, u, t, 1, T)


def _search(img, u, t, v, T):
    sc = Scene(); britain(sc)
    sites = [(-3.2, 59.0), (-3.3, 58.45)] if v == 0 else [(-3.3, 58.45), (-3.6, 57.6)]
    for i, p in enumerate(sites):
        marker(sc, p, AMBER, r=0.15, t=t + i)
    p = sites[0] if v == 0 else sites[0]
    c = mp(*p, 0.3); q = ease(u * 2 - 0.5)
    sc.seg(c + [-0.4 * q, 0, -0.4 * q], c + [0.4 * q, 0, 0.4 * q], RED, 5)
    sc.seg(c + [-0.4 * q, 0, 0.4 * q], c + [0.4 * q, 0, -0.4 * q], RED, 5)
    if v == 1:
        c = mp(-3.2, 59.0, 0.3)
        sc.seg(c + [-0.4, 0, -0.4], c + [0.4, 0, 0.4], RED, 5); sc.seg(c + [-0.4, 0, 0.4], c + [0.4, 0, -0.4], RED, 5)
    # faisceau de recherche
    a = 1.5 * t
    sc.seg(mp(-3.2, 58.2, 2.5), mp(-3.2, 58.2) + [0.9 * math.cos(a), 0, 0.9 * math.sin(a)], WHITE * 0.4, 1)
    cam = look_at(*orbit(mp(-3.3, 58.0), lerp(6.5, 5.5, ease(u)), 0.1 + 0.15 * v, 1.3))
    draw(img, sc, cam, fade=(2, 10))


def sh_no_match(img, u, t, v, T):
    sc = Scene(); britain(sc, b=0.7)
    for i, p in enumerate([(-3.2, 59.0), (-3.3, 58.45), (-3.6, 57.6), (-4.0, 56.3), (-3.2, 55.4), (-4.8, 51.9)]):
        c = mp(*p, 0.25)
        k = ease(u * 3 - i * 0.3)
        sc.seg(c + [-0.3 * k, 0, -0.3 * k], c + [0.3 * k, 0, 0.3 * k], RED, 4)
        sc.seg(c + [-0.3 * k, 0, 0.3 * k], c + [0.3 * k, 0, -0.3 * k], RED, 4)
    # point d'interrogation au-dessus de l'Écosse
    c = mp(0.6, 57.0, 1.4); q = 0.5 + 0.5 * abs(math.sin(2 * t))
    sc.add([c + [0.5 * math.cos(a), 0, -(0.5 * math.sin(a) + 0.5)] for a in np.linspace(2.6, -1.2, 16)] + [c + [0, 0, -0.25], c + [0, 0, 0.1]], WHITE * q, 3)
    sc.seg(c + [0, 0, 0.35], c + [0, 0, 0.45], WHITE * q, 5)
    cam = look_at(*orbit(mp(-2.8, 55.6), lerp(7.6, 7.0, ease(u)), 0.0, 1.35))
    draw(img, sc, cam, fade=(3, 15))


def sh_final_altar(img, u, t, v, T):
    sc = Scene(); henge(sc, b=0.55); sc.grid_plane(24, 24, 0, GOLD * 0.06)
    altar(sc, c=(0, 0, -3.0), b=1.6 + 0.4 * math.sin(2 * t))
    cam = look_at(*orbit([0, 0.3, -3.0], lerp(14, 30, ease(u)), 3.6 - 0.5 * u, lerp(0.5, 0.9, ease(u))))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(6, 60))
