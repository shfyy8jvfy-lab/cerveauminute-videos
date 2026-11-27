# Plans propres à l'épisode 20 : les géoglyphes de Nazca révélés par IA (PNAS 2024)
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

SAND = np.array([0.35, 0.55, 0.85])     # BGR : sable clair
RUST = np.array([0.15, 0.30, 0.70])     # roche rougeâtre
CYAN = np.array([1.00, 0.85, 0.30])     # couleur « IA »
RED = np.array([0.25, 0.25, 1.00])
R20 = np.random.default_rng(20)
RJ = R20.uniform(0, 1, (2000, 6))


# ---------------------------------------------------------------- formes 2D (x, z), taille ~1
def _arc(cx, cz, r, a0, a1, n=16, ry=None):
    ry = r if ry is None else ry
    a = np.linspace(a0, a1, n)
    return np.stack([cx + r * np.cos(a), cz + ry * np.sin(a)], 1)


def shape_hummingbird():
    P = []
    P.append(np.array([[0.0, -1.0], [0.0, -0.35]]))                      # long bec
    P.append(_arc(0, -0.2, 0.15, -math.pi / 2, 3 * math.pi / 2, 20))     # tête
    body = np.array([[0.1, -0.1], [0.16, 0.2], [0.12, 0.55], [0.0, 0.7], [-0.12, 0.55], [-0.16, 0.2], [-0.1, -0.1]])
    P.append(body)
    P.append(np.array([[0.16, 0.15], [0.9, -0.05], [0.95, 0.08], [0.18, 0.32]]))     # aile droite
    P.append(np.array([[-0.16, 0.15], [-0.9, -0.05], [-0.95, 0.08], [-0.18, 0.32]]))  # aile gauche
    for k in range(4):                                                    # plumes
        x = 0.35 + 0.15 * k
        P.append(np.array([[x, 0.02 - 0.02 * k], [x + 0.05, 0.25 - 0.03 * k]]))
        P.append(np.array([[-x, 0.02 - 0.02 * k], [-x - 0.05, 0.25 - 0.03 * k]]))
    P.append(np.array([[0.0, 0.7], [-0.15, 1.0], [-0.05, 1.0], [0.0, 0.8], [0.05, 1.0], [0.15, 1.0], [0.0, 0.7]]))  # queue
    return P


def shape_orca():
    P = []
    top = np.array([[-1.0, 0.0], [-0.8, -0.18], [-0.4, -0.25], [-0.1, -0.26], [0.05, -0.62], [0.18, -0.25],
                    [0.5, -0.18], [0.8, -0.08], [0.95, -0.25], [1.05, -0.3], [1.0, 0.0], [1.05, 0.3], [0.95, 0.25],
                    [0.8, 0.08], [0.5, 0.15], [0.0, 0.25], [-0.5, 0.22], [-0.85, 0.12], [-1.0, 0.0]])
    P.append(top)
    P.append(_arc(-0.7, -0.07, 0.05, 0, 2 * math.pi, 10))          # œil
    P.append(np.array([[-1.0, 0.0], [-0.75, 0.05]]))                # bouche
    P.append(np.array([[-0.3, 0.22], [-0.38, 0.5], [-0.15, 0.24]]))  # nageoire pectorale = « bras »
    # couteau tenu sous la nageoire
    P.append(np.array([[-0.37, 0.48], [-0.55, 0.62]]))
    P.append(np.array([[-0.55, 0.62], [-0.9, 0.78], [-0.98, 0.7], [-0.6, 0.55], [-0.55, 0.62]]))
    return P


def shape_llama():
    body = np.array([[-0.5, -0.1], [0.4, -0.1], [0.45, 0.15], [0.4, 0.2], [0.4, 0.55], [0.3, 0.55], [0.3, 0.22],
                     [-0.3, 0.22], [-0.3, 0.55], [-0.4, 0.55], [-0.4, 0.2], [-0.5, 0.1], [-0.5, -0.1]])
    neck = np.array([[0.3, -0.1], [0.35, -0.7], [0.55, -0.72], [0.55, -0.62], [0.45, -0.6], [0.45, -0.1]])
    ears = np.array([[0.38, -0.72], [0.36, -0.85], [0.44, -0.74]])
    return [body, neck, ears]


def shape_human():
    P = [_arc(0, -0.65, 0.22, 0, 2 * math.pi, 20)]
    P.append(_arc(-0.08, -0.68, 0.03, 0, 2 * math.pi, 6)); P.append(_arc(0.08, -0.68, 0.03, 0, 2 * math.pi, 6))
    P.append(np.array([[-0.18, -0.4], [-0.25, 0.3], [0.25, 0.3], [0.18, -0.4]]))
    P.append(np.array([[-0.2, -0.3], [-0.55, -0.6]])); P.append(np.array([[0.2, -0.3], [0.55, -0.6]]))
    P.append(np.array([[-0.12, 0.3], [-0.2, 0.75]])); P.append(np.array([[0.12, 0.3], [0.2, 0.75]]))
    return P


def shape_head():
    P = [_arc(0, 0, 0.5, 0, 2 * math.pi, 28)]
    P.append(_arc(-0.18, -0.1, 0.08, 0, 2 * math.pi, 8)); P.append(_arc(0.18, -0.1, 0.08, 0, 2 * math.pi, 8))
    P.append(np.array([[-0.18, 0.22], [0.18, 0.22]]))
    for k in range(5):  # rayons / coiffe
        a = -math.pi / 2 + (k - 2) * 0.35
        P.append(np.array([[0.5 * math.cos(a), 0.5 * math.sin(a)], [0.8 * math.cos(a), 0.8 * math.sin(a)]]))
    return P


def shape_bird():  # grand oiseau (type linéaire)
    P = [np.array([[0, -1.0], [0, 0.4]])]
    P.append(np.array([[0, -0.3], [-1.0, -0.6], [-0.95, -0.45], [0, -0.05]]))
    P.append(np.array([[0, -0.3], [1.0, -0.6], [0.95, -0.45], [0, -0.05]]))
    zz = np.linspace(0.4, 1.0, 9)
    P.append(np.stack([0.12 * np.sin(zz * 30), zz], 1))
    return P


def shape_monkey():
    P = []
    th = np.linspace(0, 5 * math.pi, 80)
    r = 0.45 * (1 - th / (5.6 * math.pi))
    P.append(np.stack([0.55 + r * np.cos(th), 0.45 + r * np.sin(th)], 1))  # queue en spirale
    P.append(np.array([[0.1, 0.45], [-0.3, 0.3], [-0.45, -0.1], [-0.3, -0.45], [0.05, -0.4], [0.1, 0.0], [0.55, 0.45]]))
    P.append(_arc(-0.45, -0.6, 0.18, 0, 2 * math.pi, 16))
    return P


SHAPES = {"hummingbird": shape_hummingbird(), "orca": shape_orca(), "llama": shape_llama(),
          "human": shape_human(), "head": shape_head(), "bird": shape_bird(), "monkey": shape_monkey()}


def glyph(sc, name, c=(0, 0), s=1.0, rot=0.0, col=SAND, w=2, prog=1.0, y=0.02, lift=0.0):
    """Dessine une figure au sol ; prog = fraction tracée (effet de tracé progressif)."""
    polys = SHAPES[name]
    tot = sum(len(p) - 1 for p in polys)
    budget = prog * tot
    cr, sr = math.cos(rot), math.sin(rot)
    for p in polys:
        n = len(p) - 1
        if budget <= 0: break
        m = min(n, budget); budget -= n
        k = int(math.floor(m)); fr = m - k
        q = p[:k + 1]
        if fr > 0 and k < n:
            q = np.vstack([q, p[k] + (p[k + 1] - p[k]) * fr])
        if len(q) < 2: continue
        X = c[0] + s * (q[:, 0] * cr - q[:, 1] * sr)
        Z = c[1] + s * (q[:, 0] * sr + q[:, 1] * cr)
        sc.add(np.stack([X, np.full(len(X), y + lift), Z], 1), col, w)


def desert(sc, size=6, n=24, b=1.0, pebbles=260):
    sc.grid_plane(size, n, 0, RUST * 0.22 * b)
    for i in range(pebbles):
        x = (RJ[i, 0] - 0.5) * 2 * size; z = (RJ[i, 1] - 0.5) * 2 * size
        r = 0.03 + 0.04 * RJ[i, 2]
        sc.seg([x - r, 0.01, z], [x + r, 0.01, z + r * 0.5], RUST * 0.5 * b, 1)


def lines_net(sc, b=1.0, size=6):
    for i in range(7):
        a = RJ[300 + i, 0] * math.pi
        x0, z0 = (RJ[300 + i, 1] - 0.5) * size, (RJ[300 + i, 2] - 0.5) * size
        d = np.array([math.cos(a), math.sin(a)]) * size * 1.2
        sc.seg([x0 - d[0], 0.015, z0 - d[1]], [x0 + d[0], 0.015, z0 + d[1]], SAND * 0.55 * b, 1)
    # trapèze
    sc.add([[-4.5, 0.015, 2.5], [1.5, 0.015, 3.4], [1.5, 0.015, 4.2], [-4.5, 0.015, 3.0]], SAND * 0.6 * b, 2, closed=True)


def bbox(sc, c, s, col=CYAN, w=2, y=0.03):
    x, z = c
    sc.add([[x - s, y, z - s], [x + s, y, z - s], [x + s, y, z + s], [x - s, y, z + s]], col, w, closed=True)
    L = s * 0.35
    for sx in (-1, 1):
        for sz in (-1, 1):
            p = np.array([x + sx * s, y + 0.01, z + sz * s])
            sc.seg(p, p - [sx * L, 0, 0], WHITE * 0.9, w)
            sc.seg(p, p - [0, 0, sz * L], WHITE * 0.9, w)


SMALL = ["human", "llama", "head", "orca", "human", "llama", "head", "monkey"]
SITES = [((RJ[500 + i, 0] - 0.5) * 9, (RJ[500 + i, 1] - 0.5) * 9) for i in range(40)]


def faint_glyphs(sc, b=0.35, n=40, s=0.35):
    for i in range(n):
        glyph(sc, SMALL[i % len(SMALL)], SITES[i], s, RJ[500 + i, 2] * 6, SAND * b, 1)


# ---------------------------------------------------------------- plans
def sh_hook_desert(img, u, t, v, T):
    sc = Scene(); desert(sc, 6, 24); lines_net(sc, 0.8)
    glyph(sc, "hummingbird", (0, 0), 1.6, 0.3, SAND, 3)
    faint_glyphs(sc, 0.18)
    cam = look_at(*orbit([0, 0, 0], lerp(7.0, 5.2, ease(u)), 0.3 + 0.3 * u, lerp(1.0, 1.2, ease(u))))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(3, 22))


def sh_hook_ai(img, u, t, v, T):
    sc = Scene(); desert(sc, 6, 24); lines_net(sc, 0.5)
    n = int(40 * ease(min(1, u * 1.3)))
    for i in range(40):
        on = i < n
        glyph(sc, SMALL[i % len(SMALL)], SITES[i], 0.35, RJ[500 + i, 2] * 6, SAND * (1.0 if on else 0.15), 2 if on else 1)
        if on: bbox(sc, SITES[i], 0.48, CYAN * 0.9, 1)
    # ligne de balayage
    zs = -5 + 10 * min(1, u * 1.3)
    sc.seg([-5.5, 0.05, zs], [5.5, 0.05, zs], CYAN, 3)
    cam = look_at(*orbit([0, 0, 0], 11.5, 0.4 + 0.2 * u, 1.25))
    draw(img, sc, cam, fade=(3, 24))


def sh_plateau(img, u, t, v, T):
    sc = Scene(); desert(sc, 6, 24)
    lines_net(sc, 1.0)
    # relief : montagnes (Andes) en fond
    xs = np.linspace(-7, 7, 60)
    sc.add(np.stack([xs, 0.9 + 0.6 * np.abs(np.sin(xs * 0.9)) + 0.4 * np.sin(xs * 2.1), np.full(60, -6.5)], 1), GOLD * 0.5, 2)
    glyph(sc, "monkey", (1.5, -0.5), 1.3, 0.0, SAND, 2)
    glyph(sc, "bird", (-2.2, 0.6), 1.2, 0.8, SAND, 2)
    # repère
    p = np.array([0.0, 0, 0.5]); pul = 0.5 + 0.5 * math.sin(T * 4)
    sc.circle(p, 0.3 + 0.1 * pul, CYAN, 2, n=32); sc.seg(p, p + [0, 1.8, 0], CYAN, 2)
    cam = look_at(*orbit([0, 0.3, 0], lerp(10.5, 8.0, ease(u)), -0.4 + 0.4 * u, lerp(0.7, 0.55, u)))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 22))


def sh_stones(img, u, t, v, T):
    sc = Scene()
    sc.grid_plane(2.5, 10, 0, RUST * 0.2)
    L = 4.0; front = -2 + L * ease(u)
    for i in range(420):
        x = (RJ[i, 0] - 0.5) * 5; z = (RJ[i, 1] - 0.5) * 5
        s = 0.06 + 0.06 * RJ[i, 2]
        inpath = abs(z) < 0.35 and x < front
        if inpath:  # pierre écartée sur le bord
            z = math.copysign(0.42 + 0.25 * RJ[i, 3], z if z != 0 else 1)
        sc.box([x, s / 2, z], [s, s * 0.7, s * 1.2], RUST * (0.9 if not inpath else 0.6), 1)
    if front > -2:
        sc.add([[-2.5, 0.01, -0.35], [front, 0.01, -0.35], [front, 0.01, 0.35], [-2.5, 0.01, 0.35]], SAND, 3, closed=True)
        for k in range(8):
            xx = -2.5 + (front + 2.5) * (k + 0.5) / 8
            sc.seg([xx, 0.01, -0.3], [xx + 0.15, 0.01, 0.3], SAND * 0.5, 1)
    cam = look_at(*orbit([front * 0.4, 0, 0], lerp(4.2, 3.4, ease(u)), 0.6 + 0.3 * u, 0.6))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(1, 12))


def sh_dry(img, u, t, v, T):
    sc = Scene(); desert(sc, 5, 20)
    glyph(sc, "monkey", (0, 0), 2.0, 0.2, SAND, 3)
    # soleil
    c = np.array([0, 4.2, -3.0])
    sc.circle(c, 0.6, GOLD, 3, n=40, axis="z")
    for k in range(16):
        a = k * math.pi / 8 + T * 0.2
        sc.seg(c + [0.8 * math.cos(a), 0.8 * math.sin(a), 0], c + [1.15 * math.cos(a), 1.15 * math.sin(a), 0], GOLD * 0.8, 2)
    # compteur des siècles qui défile
    for k in range(20):
        x = -4 + 8 * k / 19
        on = k / 19 < ease(u)
        sc.seg([x, 0.02, 3.2], [x, 0.25 if k % 5 == 0 else 0.12, 3.2], (WHITE if on else WHITE * 0.25), 2)
    cam = look_at(*orbit([0, 0.8, 0], lerp(8.5, 7.5, ease(u)), 0.2 * math.sin(T * 0.3), 0.75))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(3, 20))


def sh_hummingbird(img, u, t, v, T):
    sc = Scene(); desert(sc, 5, 20, 0.8)
    glyph(sc, "hummingbird", (0, 0), 2.3, 0.0, SAND, 3, prog=ease(min(1, u * 1.6)))
    # règle d'échelle : 93 m (bec -> queue)
    k = ease(min(1, max(0, u * 2 - 0.6)))
    X = 2.7
    if k > 0:
        z0, z1 = -2.3, -2.3 + 4.6 * k
        sc.seg([X, 0.05, z0], [X, 0.05, z1], CYAN, 3)
        for j in range(11):
            z = -2.3 + 4.6 * j / 10
            if z <= z1: sc.seg([X - 0.12, 0.05, z], [X + 0.12, 0.05, z], CYAN * 0.8, 1)
    cam = look_at(*orbit([0.3, 0, 0], lerp(8.0, 7.0, ease(u)), 0.2 + 0.25 * u, 1.2))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(3, 20))


def sh_count430(img, u, t, v, T):
    n = int(43 * ease(u)); cur = -2.6 + 5.2 * ease(u)
    sc3 = Scene(); sc3.seg([-2.6, 0, 0], [2.6, 0, 0], WHITE * 0.6, 2)
    for k in range(11):
        x = -2.6 + 5.2 * k / 10; sc3.seg([x, -0.1, 0], [x, 0.1, 0], WHITE * 0.5, 1)
    sc3.seg([cur, -0.3, 0], [cur, 0.3, 0], CYAN, 3)
    for i in range(n):
        col = i % 6; row = i // 6
        cx, cy = -2.2 + col * 0.88, 0.8 + row * 0.88
        for p in SHAPES[SMALL[i % 8]]:
            sc3.add(np.stack([cx + 0.33 * p[:, 0], cy - 0.33 * p[:, 1], np.zeros(len(p))], 1), GOLD * 0.9, 2)
    cam = look_at(*orbit([0, 2.6, 0], lerp(7.6, 7.0, ease(u)), 0.25 * math.sin(T * 0.3), 0.05))
    stars(img, cam, T, 0.4); draw(img, sc3, cam, fade=(3, 16))


def sh_neural(img, u, t, v, T):
    sc = Scene()
    # tuiles d'images aériennes au sol
    for i in range(-2, 3):
        for j in range(-2, 3):
            c = (i * 1.1, j * 1.1)
            sc.add([[c[0] - 0.5, 0, c[1] - 0.5], [c[0] + 0.5, 0, c[1] - 0.5], [c[0] + 0.5, 0, c[1] + 0.5], [c[0] - 0.5, 0, c[1] + 0.5]], RUST * 0.6, 1, closed=True)
            k = (i + 2) * 5 + j + 2
            glyph(sc, SMALL[k % 8], c, 0.25, RJ[k, 0] * 6, SAND * 0.5, 1)
    # réseau de neurones au-dessus
    layers = [(1.6, 7), (2.6, 5), (3.5, 3)]
    nodes = []
    for y, n in layers:
        row = [np.array([(k - (n - 1) / 2) * 0.75, y, 0.0]) for k in range(n)]
        nodes.append(row)
        for p in row: sc.circle(p, 0.12, CYAN, 2, n=14, axis="z")
    for a, b in zip(nodes[:-1], nodes[1:]):
        for p in a:
            for q in b:
                sc.seg(p, q, CYAN * 0.25, 1)
    # signaux qui montent
    ph = (T * 0.8) % 1
    for k in range(7):
        p0 = np.array([((k % 5) - 2) * 1.1, 0, ((k * 3) % 5 - 2) * 1.1]); p1 = nodes[0][k]
        q = p0 + (p1 - p0) * ph
        sc.seg(p0, p1, CYAN * 0.15, 1); sc.circle(q, 0.05, WHITE, 2, n=8, axis="z")
    cam = look_at(*orbit([0, 1.6, 0], lerp(7.5, 6.5, ease(u)), 0.5 + 0.4 * u, 0.35))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 16))


def sh_candidates(img, u, t, v, T):
    sc = Scene(); desert(sc, 6, 24, 0.8)
    faint_glyphs(sc, 0.3)
    for i in range(40):
        p = SITES[i]
        keep = RJ[700 + i, 0] < 0.6
        if not keep and u > 0.35:
            continue
        bbox(sc, p, 0.45, CYAN * (1.0 if keep else 0.5), 1)
    # archéologue (piste pointillée) vers un site
    tgt = SITES[3]; k = ease(max(0, u * 1.6 - 0.5))
    for j in range(int(20 * k)):
        f0, f1 = j / 20, (j + 0.5) / 20
        sc.seg([lerp(-5, tgt[0], f0)[()], 0.03, lerp(5, tgt[1], f0)[()]], [lerp(-5, tgt[0], f1)[()], 0.03, lerp(5, tgt[1], f1)[()]], WHITE, 2)
    cam = look_at(*orbit([0, 0, 0], lerp(11.5, 10.0, ease(u)), 0.6 + 0.2 * u, 1.15))
    draw(img, sc, cam, fade=(3, 24))


def sh_double(img, u, t, v, T):
    sc = Scene()
    k = ease(min(1, u * 1.4))
    h1 = 4.3 * 0.75; h2 = h1 + 3.03 * 0.75 * k
    sc.box([-1.0, h1 / 2, 0], [1.2, h1, 1.2], GOLD, 2, grid=4)
    sc.box([1.0, h1 / 2, 0], [1.2, h1, 1.2], GOLD * 0.6, 1, grid=4)
    if h2 > h1 + 0.01:
        sc.box([1.0, (h1 + h2) / 2, 0], [1.2, h2 - h1, 1.2], CYAN, 3, grid=3)
    sc.grid_plane(3, 12, 0, DIM * 0.6)
    cam = look_at(*orbit([0, 2.6, 0], lerp(8.5, 7.8, ease(u)), 0.5 + 0.3 * u, 0.2))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 18))


def sh_small_big(img, u, t, v, T):
    sc = Scene(); desert(sc, 5, 20, 0.7)
    glyph(sc, "bird", (0, 0), 3.0, 0.0, SAND * 0.8, 2)
    glyph(sc, "human", (2.6, 2.4), 0.32, 0.0, SAND, 2)
    bbox(sc, (2.6, 2.4), 0.35 + 0.05 * math.sin(T * 4), CYAN, 2)
    # deux règles
    sc.seg([-3.4, 0.05, -3.0], [-3.4, 0.05, 3.0], WHITE * 0.7, 2)
    sc.seg([3.2, 0.05, 2.1], [3.2, 0.05, 2.7], CYAN, 3)
    tgt = lerp([0, 0, 0], [2.6, 0, 2.4], ease(u))
    cam = look_at(*orbit(tgt, lerp(9.5, 3.0, ease(u)), 0.4, lerp(1.1, 0.9, u)))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(1, 18))


TRAIL = np.array([[(-6 + 12 * f), 0.02, 1.4 * math.sin(f * 7) + 0.4 * math.sin(f * 17)] for f in np.linspace(0, 1, 120)])
TRAIL_G = [(10, "human", 1), (30, "llama", -1), (52, "head", 1), (72, "human", -1), (92, "llama", 1), (110, "head", -1)]


def trail_scene(sc, b=1.0):
    desert(sc, 6, 24, 0.7)
    sc.add(TRAIL, WHITE * 0.7 * b, 2)
    for i, name, side in TRAIL_G:
        p = TRAIL[i]
        glyph(sc, name, (p[0], p[2] + side * 0.75), 0.4, 0.0, SAND * b, 2)


def sh_trail(img, u, t, v, T):
    sc = Scene(); trail_scene(sc)
    cam = look_at(*orbit([lerp(-2.0, 2.0, u)[()], 0, 0.3], 4.6, 0.3, 1.0))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(2, 16))


def sh_walker(img, u, t, v, T):
    sc = Scene(); trail_scene(sc)
    f = lerp(20, 80, ease(u))[()]
    i = int(f); a = TRAIL[i]
    sc.circle(a + [0, 0.05, 0], 0.08, WHITE, 2, n=10)
    sc.seg(a, a + [0, 0.35, 0], WHITE, 2)
    cam = look_at(*orbit(a + [0.6, 0, 0], 3.2, -1.2 + 0.3 * u, 0.42))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(1, 10))


def sh_ritual(img, u, t, v, T):
    sc = Scene(); desert(sc, 6, 24, 0.7); lines_net(sc, 1.0)
    glyph(sc, "bird", (-0.6, -0.2), 2.6, 0.5, SAND, 3)
    # procession : points lumineux le long d'une ligne droite
    for k in range(14):
        f = (k / 14 + T * 0.05) % 1
        p = lerp([-5, 0.06, -2.5], [5, 0.06, 1.8], f)
        sc.circle(p, 0.06, WHITE, 2, n=8)
    cam = look_at(*orbit([0, 0, 0], lerp(10.0, 8.5, ease(u)), -0.3 + 0.4 * u, lerp(0.9, 1.1, u)))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(3, 22))


def sh_orca(img, u, t, v, T):
    sc = Scene(); desert(sc, 4, 16, 0.7)
    glyph(sc, "orca", (0, 0), 1.9, 0.0, SAND, 3, prog=ease(min(1, u * 1.4)))
    if u > 0.6:
        bbox(sc, (-1.4, 1.2), 0.5 + 0.05 * math.sin(T * 5), RED, 2)
    cam = look_at(*orbit([-0.2, 0, 0.2], lerp(6.5, 5.5, ease(u)), 0.15 * math.sin(T * 0.4), 1.2))
    stars(img, cam, T, 0.2); draw(img, sc, cam, fade=(2, 16))


def sh_pottery(img, u, t, v, T):
    sc = Scene()
    prof = [(0.0, 0.5), (0.3, 0.75), (0.8, 0.95), (1.3, 0.9), (1.7, 0.6), (1.9, 0.45), (2.1, 0.5)]
    rot = T * 0.4
    for y, r in prof:
        sc.circle([0, y, 0], r, COPPER if 'COPPER' in globals() else AMBER, 2, n=48)
    for k in range(16):
        a = k * math.pi / 8 + rot
        P = [[r * math.cos(a), y, r * math.sin(a)] for y, r in prof]
        sc.add(P, AMBER * 0.5, 1)
    # frise : orques peintes autour du vase (face caméra)
    for k in range(3):
        a = rot + k * 2 * math.pi / 3
        if math.cos(a) < -0.2: continue
        for p in SHAPES["orca"]:
            ang = a + p[:, 0] * 0.35
            yy = 1.05 - p[:, 1] * 0.3
            R = 0.97
            sc.add(np.stack([R * np.sin(ang), yy, R * np.cos(ang)], 1), WHITE * 0.9, 2)
    cam = look_at(*orbit([0, 1.05, 0], lerp(4.6, 4.0, ease(u)), 0.0, 0.25))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 10))


def sh_pending(img, u, t, v, T):
    sc = Scene(); desert(sc, 6, 24, 0.8); lines_net(sc, 0.4)
    for i in range(40):
        p = SITES[i]
        blink = 0.5 + 0.5 * math.sin(T * 3 + i)
        bbox(sc, p, 0.4, CYAN * (0.35 + 0.65 * blink), 1)
        # point d'interrogation stylisé
        q = np.array([p[0], 0.05, p[1]])
        sc.add([q + [-0.1, 0, -0.12], q + [0, 0, -0.2], q + [0.1, 0, -0.12], q + [0, 0, 0.0], q + [0, 0, 0.08]], WHITE * 0.7 * blink, 1)
        sc.circle(q + [0, 0, 0.17], 0.02, WHITE * blink, 1, n=6)
    cam = look_at(*orbit([0, 0, 0], lerp(9.0, 11.0, ease(u)), 0.9 + 0.3 * u, 1.15))
    draw(img, sc, cam, fade=(3, 24))


def sh_final(img, u, t, v, T):
    sc = Scene(); desert(sc, 7, 28); lines_net(sc, 0.8, 7)
    glyph(sc, "hummingbird", (0, 0), 1.6, 0.3, SAND, 3)
    faint_glyphs(sc, lerp(0.05, 0.45, ease(u))[()])
    cam = look_at(*orbit([0, 0, 0], lerp(8.0, 13.0, ease(u)), 0.6 + 0.4 * u, lerp(1.2, 1.0, ease(u))))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 26))
