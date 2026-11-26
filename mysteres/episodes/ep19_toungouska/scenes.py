# Plans propres à l'épisode 19 : l'événement de la Toungouska (1908)
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

PINE = np.array([0.45, 0.85, 0.40])     # BGR : vert taïga
ICE = np.array([1.00, 0.85, 0.45])      # bleu glacé
FIRE = np.array([0.18, 0.50, 1.00])
RED = np.array([0.20, 0.25, 1.00])
R19 = np.random.default_rng(19)
# forêt : positions polaires (rayon, angle) + aléas
NT = 520
FR = np.sqrt(R19.uniform(0.02, 1.0, NT)) * 6.0
FA = R19.uniform(0, 2 * math.pi, NT)
FJ = R19.uniform(0, 1, (NT, 4))


def conifer(sc, x, z, h=0.55, b=1.0, col=PINE, y=0.0, tiers=3):
    sc.seg([x, y, z], [x, y + h, z], COPPER * 0.7 * b, 1)
    for k in range(tiers):
        yy = y + h * (0.35 + 0.22 * k)
        r = h * 0.32 * (1 - k / (tiers + 0.5))
        top = [x, yy + h * 0.25, z]
        for a in (0.3, 2.4, 4.5):
            sc.seg(top, [x + r * math.cos(a + k), yy, z + r * math.sin(a + k)], col * b, 1)


def fallen(sc, x, z, ang, L=0.55, b=1.0, col=AMBER, lift=0.0):
    """Arbre couché, cime vers l'extérieur (direction ang depuis le centre)."""
    d = np.array([math.cos(ang), 0, math.sin(ang)])
    p0 = np.array([x, 0.02, z]); p1 = p0 + d * L + [0, lift, 0]
    sc.seg(p0, p1, col * b, 2)
    n = np.array([-d[2], 0, d[0]])
    for f in (0.55, 0.8):
        q = p0 + (p1 - p0) * f
        sc.seg(q, q + d * 0.12 + n * 0.1, col * 0.6 * b, 1)
        sc.seg(q, q + d * 0.12 - n * 0.1, col * 0.6 * b, 1)


def forest(sc, down=1.0, b=1.0, rmax=6.0, core=0.9, poles=True):
    """down = proportion du rayon déjà balayée par l'onde (0 = tout debout)."""
    front = down * rmax
    for i in range(NT):
        r, a = FR[i], FA[i]
        if r > rmax: continue
        x, z = r * math.cos(a), r * math.sin(a)
        if r < core:
            if poles:
                h = 0.5 + 0.2 * FJ[i, 0]
                sc.seg([x, 0, z], [x, h, z], WHITE * 0.75 * b, 2)
            continue
        if r < front:
            fallen(sc, x, z, a + 0.15 * (FJ[i, 1] - 0.5), 0.45 + 0.25 * FJ[i, 2], b)
        else:
            conifer(sc, x, z, 0.45 + 0.2 * FJ[i, 0], b)


def shock_ring(sc, r, b=1.0, col=WHITE, y=0.05):
    if r <= 0: return
    sc.circle([0, y, 0], r, col * b, 3, n=96)
    sc.circle([0, y, 0], r * 0.93, col * 0.4 * b, 1, n=96)


def burst(sc, c, r, b=1.0, col=FIRE):
    c = np.asarray(c, float)
    for k in range(6):
        sc.circle(c, r * (0.55 + 0.09 * k), (col if k % 2 else WHITE) * b * (1 - k / 9), 2 if k < 2 else 1, n=48, axis="y")
    for k in range(5):
        sc.circle(c, r * (0.4 + 0.15 * k), col * 0.7 * b, 1, n=48, axis="z")
        sc.circle(c, r * (0.4 + 0.15 * k), col * 0.5 * b, 1, n=48, axis="x")
    for k in range(28):
        rr = RR19[k]
        d = np.array([rr[0] - 0.5, rr[1] - 0.5, rr[2] - 0.5]); d /= np.linalg.norm(d) + 1e-9
        sc.seg(c + d * r * 0.3, c + d * r * (1.0 + 0.5 * rr[3]), (WHITE if k % 3 == 0 else col) * b, 1)


RR19 = np.random.default_rng(91).uniform(0, 1, (300, 6))
RR19[230:244] = np.random.default_rng(92).uniform(0, 1, (14, 6))


def meteor(sc, head, d, L=4.0, b=1.0, r=0.25):
    head = np.asarray(head, float); d = np.asarray(d, float); d /= np.linalg.norm(d)
    for k in range(10):
        rr = RR19[40 + k]
        off = np.array([rr[0] - 0.5, rr[1] - 0.5, rr[2] - 0.5]) * r * 1.2
        sc.seg(head + off * 0.3, head - d * L * (0.5 + 0.5 * rr[3]) + off * 2.5, (FIRE if k % 2 else AMBER) * b, 2 if k < 4 else 1)
    for ax in ("x", "y", "z"):
        sc.circle(head, r, WHITE * b, 2, n=20, axis=ax)


# ---------------------------------------------------------------- plans
def sh_hook_blast(img, u, t, v, T):
    sc = Scene()
    forest(sc, down=ease(min(1, u * 1.6)), rmax=6.0)
    shock_ring(sc, 6.2 * ease(min(1, u * 1.6)), 1.0 - 0.5 * u)
    burst(sc, [0, 2.4, 0], 0.6 + 1.6 * ease(min(1, u * 2)), 1.2 - 0.6 * u)
    cam = look_at(*orbit([0, 0.8, 0], lerp(11.5, 9.5, ease(u)), 0.4 + 0.25 * u, 0.42))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 22))


def sh_hook_forest(img, u, t, v, T):
    sc = Scene(); forest(sc, 1.0, rmax=6.0)
    cam = look_at(*orbit([0, 0, 0], lerp(7.5, 10.5, ease(u)), 1.2 + 0.3 * u, lerp(1.25, 1.0, u)))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(3, 22))


def sh_siberia(img, u, t, v, T):
    sc = Scene()
    sc.grid_plane(5, 20, 0, GOLD * 0.12)
    # rivière sinueuse
    xs = np.linspace(-5, 5, 80)
    zs = 0.9 * np.sin(xs * 0.9) + 0.4 * np.sin(xs * 2.3 + 1)
    m = xs <= -5 + 10 * ease(min(1, u * 1.5))
    if m.sum() > 1:
        sc.add(np.stack([xs[m], np.full(m.sum(), 0.02), zs[m]], 1), ICE, 3)
        sc.add(np.stack([xs[m], np.full(m.sum(), 0.02), zs[m] + 0.12], 1), ICE * 0.4, 1)
    for i in range(0, NT, 3):
        x = (FJ[i, 0] - 0.5) * 9.5; z = (FJ[i, 1] - 0.5) * 9.5
        if abs(z - (0.9 * math.sin(x * 0.9) + 0.4 * math.sin(x * 2.3 + 1))) < 0.35: continue
        conifer(sc, x, z, 0.35 + 0.15 * FJ[i, 2], 0.8, tiers=2)
    # repère de l'épicentre
    p = np.array([0.8, 0, -1.6]); pul = 0.5 + 0.5 * math.sin(T * 5)
    sc.circle(p, 0.35 + 0.15 * pul, FIRE, 2, n=32)
    sc.circle(p, 0.7, FIRE * 0.5, 1, n=32)
    sc.seg(p, p + [0, 1.6, 0], FIRE, 2)
    cam = look_at(*orbit([0.4, 0, -0.6], lerp(9.0, 7.0, ease(u)), -0.3 + 0.35 * u, 0.85))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(3, 20))


def sh_fireball(img, u, t, v, T):
    sc = Scene(); forest(sc, 0.0, rmax=5.0, core=0.0)
    d = np.array([1.0, -0.45, 0.25])
    head = lerp([-5, 4.6, -1.2], [0.4, 2.2, 0.2], ease(u))
    meteor(sc, head, d, L=5.0, r=0.42)
    cam = look_at(*orbit([0, 2.0, 0], 9.0, 0.25 + 0.15 * u, 0.22))
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(3, 22))


def sh_airburst(img, u, t, v, T):
    sc = Scene(); forest(sc, 0.0, rmax=4.0, core=0.0)
    h = 3.0
    burst(sc, [0, h, 0], 0.4 + 1.3 * ease(u), 1.2)
    # règle d'altitude
    X = 2.6
    sc.seg([X, 0, 0], [X, h, 0], WHITE * 0.8, 2)
    for k in range(6):
        y = h * k / 5
        sc.seg([X - 0.15, y, 0], [X + 0.15, y, 0], WHITE * 0.7, 1)
    sc.seg([X - 0.35, h, 0], [X + 0.35, h, 0], FIRE, 2)
    sc.seg([0, 0.05, 0], [0, h, 0], FIRE * 0.35, 1)
    cam = look_at(*orbit([0.6, 1.5, 0], lerp(8.0, 7.0, ease(u)), 0.1 * math.sin(T * 0.3) + 0.15, 0.12))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 20))


def sh_fallen(img, u, t, v, T):
    sc = Scene(); forest(sc, 1.0, rmax=6.0)
    for k in range(8):
        a = k * math.pi / 4 + 0.2
        sc.seg([0.9 * math.cos(a), 0.05, 0.9 * math.sin(a)], [6.3 * math.cos(a), 0.05, 6.3 * math.sin(a)], WHITE * 0.25, 1)
    cam = look_at(*orbit([0, 0, 0], lerp(10.5, 8.0, ease(u)), 0.6 * T * 0.12, 1.35))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(3, 22))


def hut(sc, c, b=1.0, col=GOLD):
    c = np.asarray(c, float)
    sc.box(c + [0, 0.5, 0], [1.6, 1.0, 1.2], col * b, 2, grid=4)
    A = c + [-0.85, 1.0, -0.65]; B = c + [0.85, 1.0, -0.65]; C = c + [0.85, 1.0, 0.65]; D = c + [-0.85, 1.0, 0.65]
    ra = c + [-0.85, 1.6, 0]; rb = c + [0.85, 1.6, 0]
    for p, q in ((A, ra), (D, ra), (B, rb), (C, rb), (ra, rb)):
        sc.seg(p, q, col * b, 2)
    sc.box(c + [0.3, 0.4, 0.61], [0.4, 0.8, 0.02], col * 0.7 * b, 1)


def chair(sc, c, tilt=0.0, b=1.0):
    c = np.asarray(c, float)
    ca, sa = math.cos(tilt), math.sin(tilt)
    R = lambda p: c + [p[0] * ca - p[1] * sa, p[0] * sa + p[1] * ca, p[2]]
    for px in (-0.2, 0.2):
        for pz in (-0.2, 0.2):
            sc.seg(R([px, 0, pz]), R([px, 0.45, pz]), COPPER * b, 2)
    sc.add([R([-0.22, 0.45, -0.22]), R([0.22, 0.45, -0.22]), R([0.22, 0.45, 0.22]), R([-0.22, 0.45, 0.22])], COPPER * b, 2, closed=True)
    sc.seg(R([-0.2, 0.45, -0.2]), R([-0.2, 1.0, -0.2]), COPPER * b, 2)
    sc.seg(R([-0.2, 0.45, 0.2]), R([-0.2, 1.0, 0.2]), COPPER * b, 2)
    sc.seg(R([-0.2, 1.0, -0.2]), R([-0.2, 1.0, 0.2]), COPPER * b, 2)


def sh_farm(img, u, t, v, T):
    sc = Scene(); hut(sc, [-0.6, 0, -0.8])
    chair(sc, [0.9, 0, 0.6])
    sc.box([1.6, 0.35, 0.6], [0.7, 0.04, 0.7], GOLD * 0.7, 1)
    for k in range(4):
        sc.seg([1.3 + 0.2 * k, 0, 0.3], [1.3 + 0.2 * k, 0.35, 0.3], GOLD * 0.4, 1)
    sc.grid_plane(4, 12, 0, GOLD * 0.1)
    for i in range(0, 60):
        a = FA[i]; r = 3.0 + FR[i] * 0.3
        conifer(sc, r * math.cos(a), r * math.sin(a), 0.6, 0.7)
    cam = look_at(*orbit([0.3, 0.6, 0], lerp(6.0, 5.0, ease(u)), 0.5 + 0.25 * u, 0.3))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 16))


def sh_heatwave(img, u, t, v, T):
    sc = Scene(); hut(sc, [-0.6, 0, -0.8], 1.0)
    tilt = 1.3 * ease(min(1, max(0, (u - 0.35) * 2.5)))
    dx = 1.2 * ease(min(1, max(0, (u - 0.35) * 2.5)))
    chair(sc, [0.9 + dx, 0, 0.6], -tilt)
    sc.grid_plane(4, 12, 0, GOLD * 0.1)
    # front de chaleur venant de gauche
    fx = lerp(-6, 4, ease(u))[()]
    for k in range(7):
        x = fx - k * 0.35
        ys = np.linspace(0, 2.6, 20)
        P = np.stack([x + 0.12 * np.sin(ys * 4 + T * 9 + k), ys, np.zeros_like(ys) + 0.6], 1)
        sc.add(P, (FIRE if k % 2 else RED) * (1 - k / 8), 2)
        P2 = np.stack([x + 0.12 * np.sin(ys * 4 + T * 9 + k + 1), ys, np.zeros_like(ys) - 1.6], 1)
        sc.add(P2, FIRE * 0.5 * (1 - k / 8), 1)
    cam = look_at(*orbit([0.5, 0.8, 0], 6.2, 0.35, 0.22))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(2, 16))


def sh_seismo(img, u, t, v, T):
    sc = Scene()
    # tambour enregistreur
    for k in range(9):
        a = k * math.pi / 4 + T * 0.4
        sc.seg([-2.2, 0.8 * math.cos(a), 0.8 * math.sin(a)], [2.2, 0.8 * math.cos(a), 0.8 * math.sin(a)], GOLD * 0.35, 1)
    sc.circle([-2.2, 0, 0], 0.8, GOLD, 2, axis="x"); sc.circle([2.2, 0, 0], 0.8, GOLD, 2, axis="x")
    sc.seg([-2.8, 0, 0], [2.8, 0, 0], GOLD * 0.6, 2)
    # tracé
    xs = np.linspace(-2.2, 2.2, 260)
    pos = -2.2 + 4.4 * ease(min(1, u * 1.15))
    m = xs <= pos
    q = 1.0 - xs * 0 + 0
    env = np.exp(-((xs - 0.0) / 0.55) ** 2) + 0.05
    amp = 0.55 * env * np.sin(xs * 38) * (0.6 + 0.4 * np.sin(xs * 7))
    if m.sum() > 1:
        sc.add(np.stack([xs[m], amp[m], np.full(m.sum(), 0.82)], 1), FIRE, 2)
    sc.seg([pos, 1.6, 0.85], [pos, amp[m][-1] if m.any() else 0, 0.85], WHITE, 2)
    sc.box([pos, 1.9, 0.85], [0.3, 0.6, 0.3], WHITE * 0.7, 1)
    cam = look_at(*orbit([0, 0.2, 0], 6.0, 0.2 + 0.1 * math.sin(T * 0.4), 0.15))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(2, 14))


CITY = np.random.default_rng(7).uniform(0, 1, (26, 3))


def sh_night_city(img, u, t, v, T):
    sc = Scene()
    for i, (a, bb, c) in enumerate(CITY):
        x = -4 + 8 * i / 25; h = 0.5 + 1.8 * a; w = 0.25 + 0.15 * bb
        sc.box([x, h / 2, -0.5 + c], [w, h, 0.4], GOLD * 0.8, 1)
    # horloge (tour)
    sc.box([0.5, 1.8, 0.0], [0.6, 3.6, 0.6], GOLD, 2)
    sc.circle([0.5, 3.1, 0.31], 0.22, WHITE, 2, n=32, axis="z")
    sc.seg([0.5, 3.1, 0.32], [0.5, 3.3, 0.32], WHITE, 2)
    sc.seg([0.5, 3.1, 0.32], [0.5, 3.28, 0.32], WHITE, 2)
    sc.add([[0.2, 3.6, -0.3], [0.5, 4.3, 0], [0.8, 3.6, -0.3]], GOLD, 2)
    # ciel lumineux : bandes ondulantes
    gl = 0.5 + 0.5 * ease(u)
    for k in range(9):
        xs = np.linspace(-6, 6, 60)
        ys = 4.6 + 0.4 * k + 0.15 * np.sin(xs * 0.8 + T * 0.6 + k)
        sc.add(np.stack([xs, ys, np.full(60, -3.0 - 0.3 * k)], 1), (AMBER if k % 2 else GOLD) * gl * (0.7 - 0.05 * k), 2)
    cam = look_at(*orbit([0, 2.6, 0], lerp(9.0, 8.0, ease(u)), 0.15 * math.sin(T * 0.3), 0.05))
    stars(img, cam, T, 0.15); draw(img, sc, cam, fade=(3, 20))


def sh_newspaper(img, u, t, v, T):
    sc = Scene()
    c = np.array([0, 0, 0])
    W2, H2 = 1.4, 1.9
    sc.add([[-W2, -H2, 0], [W2, -H2, 0], [W2, H2, 0], [-W2, H2, 0]], WHITE, 2, closed=True)
    sc.seg([0, -H2, 0.0], [0, H2, 0.0], WHITE * 0.4, 1)
    sc.box([0, H2 - 0.3, 0], [2.4, 0.3, 0.01], GOLD, 2)
    for col in (-1, 1):
        for k in range(13):
            y = H2 - 0.75 - k * 0.22
            L = 1.05 * (0.6 + 0.4 * RR19[100 + k + (col > 0) * 20, 0])
            x0 = col * 0.15 if col > 0 else -1.25
            sc.seg([x0, y, 0.01], [x0 + L, y, 0.01], GOLD * 0.6, 1)
    # horloge minuit
    cc = np.array([0, -2.7, 0.3])
    sc.circle(cc, 0.45, AMBER, 2, n=40, axis="z")
    sc.seg(cc, cc + [0, 0.38, 0], WHITE, 2); sc.seg(cc, cc + [0, 0.3, 0], WHITE, 2)
    for k in range(12):
        a = k * math.pi / 6
        sc.seg(cc + [0.38 * math.cos(a), 0.38 * math.sin(a), 0], cc + [0.45 * math.cos(a), 0.45 * math.sin(a), 0], AMBER, 1)
    cam = look_at(*orbit([0, -0.3, 0], lerp(7.2, 6.2, ease(u)), 0.25 * math.sin(T * 0.5), 0.1))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(2, 14))


def sh_energy(img, u, t, v, T):
    sc = Scene()
    sc.grid_plane(5, 14, 0, GOLD * 0.12)
    burst(sc, [0, 2.6, 0], 1.0 + 0.4 * math.sin(T * 3) * 0.2 + 0.6 * ease(u), 1.2)
    # petites "unités" alignées : comparaison d'échelle
    n = int(6 + 40 * ease(u))
    for k in range(n):
        x = -3.6 + (k % 12) * 0.65; z = 2.0 + (k // 12) * 0.6
        sc.circle([x, 0.15, z], 0.12, AMBER, 1, n=12)
        sc.seg([x, 0.0, z], [x, 0.3, z], AMBER * 0.7, 1)
    for k in range(4):
        shock_ring(sc, 1.5 + k * 1.1 + (T * 0.8 % 1.1), 0.5)
    cam = look_at(*orbit([0, 1.4, 1.0], 9.5, 0.2 * math.sin(T * 0.3), 0.32))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(3, 20))


def sh_expedition(img, u, t, v, T):
    sc = Scene(); forest(sc, 1.0, rmax=6.0, poles=False)
    # piste et tente
    path = np.array([[6.5 - 5.0 * f, 0.03, 1.5 * math.sin(f * 3)] for f in np.linspace(0, 1, 40)])
    k = max(2, int(40 * ease(u)))
    sc.add(path[:k], WHITE, 2)
    p = path[k - 1]
    sc.add([p + [-0.35, 0, -0.3], p + [0, 0.5, -0.3], p + [0.35, 0, -0.3]], GOLD, 2)
    sc.add([p + [-0.35, 0, 0.3], p + [0, 0.5, 0.3], p + [0.35, 0, 0.3]], GOLD, 2)
    sc.seg(p + [0, 0.5, -0.3], p + [0, 0.5, 0.3], GOLD, 2)
    sc.circle(p + [0.6, 0.1, 0], 0.08 + 0.03 * math.sin(T * 9), FIRE, 2, n=12)
    cam = look_at(*orbit(lerp([5.0, 0, 1.0], [2.5, 0, 0.6], ease(u)), 6.0, 1.3 + 0.2 * u, 0.6))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 18))


def sh_crater_search(img, u, t, v, T):
    sc = Scene(); forest(sc, 1.0, rmax=4.5)
    # cratère "attendu" en pointillés
    for k in range(24):
        if k % 2: continue
        a0, a1 = k * math.pi / 12, (k + 1) * math.pi / 12
        sc.seg([1.6 * math.cos(a0), 0.05, 1.6 * math.sin(a0)], [1.6 * math.cos(a1), 0.05, 1.6 * math.sin(a1)], ICE, 2)
    # faisceau de recherche qui balaie
    a = T * 1.3
    sc.seg([0, 2.5, 0], [2.0 * math.cos(a), 0.05, 2.0 * math.sin(a)], ICE * 0.7, 1)
    sc.circle([2.0 * math.cos(a), 0.05, 2.0 * math.sin(a)], 0.3, ICE, 2, n=20)
    cam = look_at(*orbit([0, 0, 0], lerp(8.0, 6.5, ease(u)), 0.5 + 0.3 * u, 0.9))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(2, 18))


def sh_empty(img, u, t, v, T):
    sc = Scene()
    sc.grid_plane(3, 12, 0, ICE * 0.4)
    # tourbière vide : ondulations
    for k in range(5):
        sc.circle([0, 0.02, 0], 0.4 + k * 0.5 + (T * 0.3 % 0.5), ICE * (0.9 - 0.12 * k), 2, n=64)
    s = 1.0 - 0.6 * ease(u)
    sc.box([0, 0.6, 0], [0.9 * s, 0.9 * s, 0.9 * s], WHITE * (1 - ease(u)), 1)
    cam = look_at(*orbit([0, 0.3, 0], lerp(3.6, 4.4, ease(u)), 0.4 + 0.2 * u, 0.5))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 14))


def sh_poles(img, u, t, v, T):
    sc = Scene(); forest(sc, 1.0, rmax=3.5, core=1.3)
    for i in range(NT):
        if FR[i] < 1.3:
            x, z = FR[i] * math.cos(FA[i]), FR[i] * math.sin(FA[i])
            h = 0.6 + 0.3 * FJ[i, 0]
            for k in range(2):
                y = h * (0.5 + 0.2 * k)
                a = FJ[i, 3] * 6 + k * 2
                sc.seg([x, y, z], [x + 0.06 * math.cos(a), y + 0.02, z + 0.06 * math.sin(a)], WHITE * 0.6, 1)
    cam = look_at(*orbit([0, 0.3, 0], lerp(5.0, 4.0, ease(u)), 0.4 + 0.5 * u, 0.45))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 10))


def sh_rock_or_comet(img, u, t, v, T):
    sc = Scene()
    # astéroïde : polyèdre irrégulier
    c = np.array([-1.3, 1.0, 0]); rot = T * 0.5
    V = []
    for k in range(30):
        rr = RR19[200 + k]
        th = math.acos(2 * rr[0] - 1); ph = 2 * math.pi * rr[1] + rot
        r = 1.0 + 0.3 * rr[2]
        V.append(c + r * np.array([math.sin(th) * math.cos(ph), math.cos(th), math.sin(th) * math.sin(ph)]))
    V = np.array(V)
    for i in range(30):
        dd = np.linalg.norm(V - V[i], axis=1)
        for j in np.argsort(dd)[1:5]:
            if j > i: sc.seg(V[i], V[j], AMBER, 2)
    # comète : noyau + queue
    h = np.array([1.4, -1.2, 0])
    for ax in ("x", "y", "z"):
        sc.circle(h, 0.3, ICE, 2, n=20, axis=ax)
    for k in range(14):
        rr = RR19[230 + k]
        a = (rr[0] - 0.5) * 0.7
        L = 2.5 + 1.5 * rr[1]
        d = np.array([math.cos(1.1 + a), math.sin(1.1 + a), (rr[2] - 0.5) * 0.4])
        ys = np.linspace(0, 1, 12)
        P = h + np.outer(ys * L, d) + np.outer(np.sin(ys * 3 + T * 2 + k) * 0.08 * ys, [1, 0, 0])
        sc.add(P, ICE * (0.9 - 0.04 * k), 1 if k > 3 else 2)
    sc.seg([0, -2.8, 0], [0, 2.8, 0], WHITE * 0.15, 1)
    cam = look_at(*orbit([0, 0, 0], lerp(8.5, 7.8, ease(u)), 0.15 * math.sin(T * 0.4), 0.1))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(3, 16))


def sh_final(img, u, t, v, T):
    sc = Scene(); forest(sc, 1.0, rmax=6.0)
    burst(sc, [0, 2.4, 0], 1.2 + 0.2 * math.sin(T * 2), 1.0 - 0.7 * ease(u))
    cam = look_at(*orbit([0, 0.6, 0], lerp(8.5, 12.0, ease(u)), 0.9 + 0.4 * u, lerp(0.5, 0.9, ease(u))))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 24))
