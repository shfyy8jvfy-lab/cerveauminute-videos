# Plans propres à l'épisode 8 : le forage superprofond de Kola
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE...)

ROCK = np.array([0.45, 0.62, 0.80])      # BGR : granite gris-beige
HOT = np.array([0.15, 0.22, 1.00])       # rouge chaud
WATER = np.array([1.00, 0.70, 0.30])     # bleu
H2 = np.array([1.00, 0.95, 0.60])        # cyan pâle
STEEL = np.array([0.85, 0.85, 0.80])
KM = 0.33                                # unités par kilomètre
DEPTH = 12.262 * KM


def heat_col(f):
    """Couleur de la roche selon la profondeur relative f (0 surface, 1 fond)."""
    f = min(max(f, 0.0), 1.0)
    return ROCK * (1 - f) + HOT * f


def hole(sc, y0, y1, r, col=GOLD, n=40, w=1, hot=False):
    """Puits cylindrique de y0 (haut) à y1 (bas)."""
    for k in range(n + 1):
        y = y0 + (y1 - y0) * k / n
        c = heat_col(-y / DEPTH) if hot else col
        sc.circle([0, y, 0], r, c * (0.9 if k % 5 == 0 else 0.5), 2 if k % 5 == 0 else 1, 24)
    for a in np.linspace(0, 2 * math.pi, 8, endpoint=False):
        sc.seg([r * math.cos(a), y0, r * math.sin(a)], [r * math.cos(a), y1, r * math.sin(a)], col * 0.45, 1)


def derrick(sc, c=(0, 0, 0), s=1.0, col=GOLD):
    c = np.asarray(c, float)
    h, b, tp = 1.6 * s, 0.35 * s, 0.08 * s
    lv = 7
    pts = lambda y: [c + [sx * lerp(b, tp, y / h)[()], y, sz * lerp(b, tp, y / h)[()]] for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for k in range(lv + 1):
        y = h * k / lv
        sc.add(pts(y), col * (0.9 if k in (0, lv) else 0.55), 2 if k in (0, lv) else 1, closed=True)
        if k < lv:
            A, B = pts(y), pts(h * (k + 1) / lv)
            for f in range(4):
                sc.seg(A[f], B[(f + 1) % 4], col * 0.4, 1)
                sc.seg(A[f], B[f], col, 2)
    sc.box(c + [0, h + 0.06 * s, 0], [0.22 * s, 0.12 * s, 0.22 * s], col, 2)
    sc.seg(c + [0, h, 0], c + [0, 0, 0], WHITE * 0.7, 1)       # train de tiges


def building(sc, c, size, col):
    c = np.asarray(c, float); sx, sy, sz = size
    sc.box(c + [0, sy / 2, 0], size, col, 1)
    sc.seg(c + [-sx / 2, sy, 0], c + [sx / 2, sy, 0], col * 0.5, 1)


def strata(sc, size=1.2, ymin=-DEPTH - 0.3, col=ROCK, n=14, hot=False):
    """Coupe de croûte : couches horizontales (cadres carrés) et arêtes verticales."""
    for k in range(n + 1):
        y = ymin * k / n
        c = (heat_col(k / n) if hot else col) * (0.55 if k % 3 == 0 else 0.28)
        sc.add([[-size, y, -size], [size, y, -size], [size, y, size], [-size, y, size]], c, 1, closed=True)
    for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        sc.seg([sx * size, 0, sz * size], [sx * size, ymin, sz * size], col * 0.4, 1)


def km_marks(sc, depth_km=12, x=0.0, col=GOLD, every=1):
    for k in range(0, depth_km + 1, every):
        y = -k * KM
        L = 0.16 if k % 3 == 0 else 0.08
        sc.seg([x - L, y, 0], [x + L, y, 0], col * (0.9 if k % 3 == 0 else 0.5), 2 if k % 3 == 0 else 1)


R8 = np.random.default_rng(8)
CRACKS = []
for i in range(70):
    p = np.array([R8.uniform(-1, 1), -7 * KM + R8.uniform(-0.55, 0.55), R8.uniform(-1, 1)])
    pts = [p]
    for j in range(3):
        pts.append(pts[-1] + R8.normal(0, 0.09, 3))
    CRACKS.append(np.array(pts))
DROPS = R8.uniform(0, 1, (120, 4))
BUB = R8.uniform(0, 1, (60, 3))


def fossil(sc, c, s, kind, rot, col):
    c = np.asarray(c, float)
    if kind == 0:   # foraminifère en spirale
        th = np.linspace(0, 5 * math.pi, 90)
        r = s * 0.12 * np.exp(0.16 * th)
        P = np.stack([r * np.cos(th + rot), r * np.sin(th + rot), np.zeros_like(th)], 1) + c
        sc.add(P, col, 2)
        for k in range(0, 90, 9):
            sc.seg(c, P[k], col * 0.35, 1)
    elif kind == 1:  # radiolaire : sphère et épines
        sc.circle(c, s * 0.5, col, 2, 32, axis="z"); sc.circle(c, s * 0.5, col * 0.5, 1, 32, axis="y")
        sc.circle(c, s * 0.5, col * 0.5, 1, 32, axis="x")
        for a in np.linspace(0, 2 * math.pi, 12, endpoint=False):
            d = np.array([math.cos(a + rot), math.sin(a + rot), 0.3 * math.sin(3 * a)])
            sc.seg(c + d * s * 0.5, c + d * s * 0.95, col * 0.8, 1)
    else:            # diatomée : disque à rayons
        sc.circle(c, s * 0.55, col, 2, 40, axis="z"); sc.circle(c, s * 0.3, col * 0.6, 1, 28, axis="z")
        for a in np.linspace(0, 2 * math.pi, 16, endpoint=False):
            sc.seg(c + [s * 0.3 * math.cos(a + rot), s * 0.3 * math.sin(a + rot), 0],
                   c + [s * 0.55 * math.cos(a + rot), s * 0.55 * math.sin(a + rot), 0], col * 0.5, 1)


R_F = np.random.default_rng(24)
FOSS = [(R_F.uniform(-0.9, 0.9), R_F.uniform(-1.5, 1.5), R_F.uniform(-0.4, 0.4), R_F.uniform(0.18, 0.32), i % 3, R_F.uniform(0, 6))
        for i in range(24)]


# ------------------------------------------------------------------ plans
def sh_hook_hole(img, u, t, v, T):
    """Gros plan : l'ouverture de 23 cm et sa règle, la caméra plonge dans le puits."""
    sc = Scene()
    sc.grid_plane(1.4, 14, 0.0, ROCK * 0.22)
    hole(sc, 0.0, -6.0, 0.23, GOLD, n=60)
    sc.circle([0, 0.002, 0], 0.23, WHITE, 3, 48)
    # règle de 23 cm
    sc.seg([-0.23, 0.01, 0.32], [0.23, 0.01, 0.32], AMBER, 3)
    for x in (-0.23, 0.23):
        sc.seg([x, 0.01, 0.27], [x, 0.01, 0.37], AMBER, 3)
    if v == 0:
        cam = look_at(*orbit([0, -0.3, 0], lerp(2.4, 1.3, ease(u)), 0.3 * u, lerp(1.0, 1.25, ease(u))))
    else:
        cam = look_at(lerp([0.05, 1.3, 0.55], [0.0, 0.3, 0.08], ease(u)), [0, -3, 0])
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(1, 9))


def sh_hook_depth(img, u, t, v, T):
    """Recul : le puits file vers le bas jusqu'à 12 km, repères tous les km."""
    sc = Scene()
    sc.grid_plane(1.0, 10, 0.0, ROCK * 0.3)
    prog = ease(u * 1.4)
    hole(sc, 0.0, -DEPTH * prog, 0.05, GOLD, n=48)
    km_marks(sc, int(12 * prog), 0.0, AMBER)
    sc.circle([0, -DEPTH * prog, 0], 0.09, WHITE, 2, 20)
    derrick(sc, (0, 0, 0), 0.45, GOLD * 0.8)
    cam = look_at(*orbit([0, lerp(-0.6, -DEPTH / 2, ease(u)), 0], lerp(2.0, 6.2, ease(u)), 0.5 - 0.3 * u, lerp(0.3, 0.05, u)))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 14))


def sh_kola_site(img, u, t, v, T):
    """La toundra de Kola : tour de forage et bâtiments."""
    sc = Scene()
    sc.grid_plane(3.0, 18, 0.0, ROCK * 0.18)
    derrick(sc, (0, 0, 0), 1.0, GOLD)
    building(sc, (0.9, 0, 0.3), (0.7, 0.35, 0.45), GOLD * 0.6)
    building(sc, (-0.9, 0, -0.2), (0.5, 0.5, 0.6), GOLD * 0.6)
    building(sc, (-0.4, 0, 1.0), (1.0, 0.25, 0.35), GOLD * 0.5)
    R = np.random.default_rng(70)
    for i in range(30):   # collines basses
        x, z = R.uniform(-3, 3, 2)
        if abs(x) < 1.4 and abs(z) < 1.4: continue
        h = R.uniform(0.1, 0.35); r = R.uniform(0.3, 0.6)
        sc.add([[x - r, 0, z], [x, h, z], [x + r, 0, z]], ROCK * 0.35, 1)
    az = [0.4, 2.0, -1.2][v % 3]
    cam = look_at(*orbit([0, 0.7, 0], lerp(3.6, 3.0, ease(u)), az + 0.35 * u, lerp(0.22, 0.12, u)))
    stars(img, cam, T, 0.9, 0.05 * T); draw(img, sc, cam, fade=(2, 12))


def sh_crust(img, u, t, v, T):
    """Coupe de la croûte : la tige descend couche après couche."""
    sc = Scene()
    strata(sc, 0.9, -DEPTH - 0.4, ROCK, 16)
    d = DEPTH * (ease(u) * 0.6 + (0.4 if v else 0.0))
    d = min(d, DEPTH)
    sc.seg([0, 0.6, 0], [0, -d, 0], WHITE * 0.9, 3)
    sc.circle([0, -d, 0], 0.07, AMBER, 2, 16)
    km_marks(sc, int(d / KM), 1.0, AMBER)
    derrick(sc, (0, 0, 0), 0.4, GOLD)
    cam = look_at(*orbit([0, -d * 0.6 - 0.3, 0], lerp(4.2, 5.2, ease(u)) + DEPTH * 0.15, 0.6 + 0.4 * u + v, 0.18))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 16))


def sh_mariana(img, u, t, v, T):
    """Comparaison : la fosse des Mariannes (≈ 11 km) et le puits (12,262 km)."""
    sc = Scene()
    xs = np.linspace(-1.6, 0.2, 40)
    prof = -11.0 * KM * np.exp(-((xs + 0.7) / 0.32) ** 2)
    sc.add(np.stack([xs, prof, np.zeros_like(xs)], 1), WATER, 2)
    for y in np.linspace(-0.05, -11 * KM + 0.2, 10):  # eau
        m = prof < y
        if m.any():
            sc.seg([xs[m][0], y, 0], [xs[m][-1], y, 0], WATER * 0.25, 1)
    sc.seg([-1.7, 0, 0], [1.4, 0, 0], GOLD * 0.6, 1)
    prog = ease(u * 1.3)
    sc.seg([0.8, 0, 0], [0.8, -DEPTH * prog, 0], WHITE, 3)
    derrick(sc, (0.8, 0, 0), 0.35, GOLD)
    for y, c in ((-11 * KM, WATER), (-DEPTH, AMBER)):
        for x in np.arange(-1.6, 1.3, 0.12):
            sc.seg([x, y, 0], [x + 0.06, y, 0], c * 0.6, 1)
    cam = look_at(*orbit([-0.1, -DEPTH / 2, 0], 5.6, 0.15 * math.sin(u * 2) + 0.1 * v, 0.05))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 16))


def sh_descent(img, u, t, v, T):
    """Plongée dans le puits : les anneaux défilent, l'obscurité gagne."""
    sc = Scene()
    y = -0.5 - 3.0 * u
    hole(sc, y + 0.2, y - 6, 0.23, GOLD * lerp(0.9, 0.5, u)[()], n=70, hot=False)
    cam = look_at([0.0, y + 0.3, 0.0], [0.03, y - 3.0, 0.06], roll=0.4 * u)
    draw(img, sc, cam, fade=(0.3, 5))


def sh_basalt(img, u, t, v, T):
    """Vers 7 km : la couche de basalte attendue (pointillés) se dissout."""
    sc = Scene()
    yb = -7 * KM
    for k in range(9):
        y = yb + 0.9 - k * 0.225
        sc.add([[-1, y, -1], [1, y, -1], [1, y, 1], [-1, y, 1]], ROCK * (0.5 if k % 2 == 0 else 0.25), 1, closed=True)
    for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        sc.seg([sx, yb + 0.9, sz], [sx, yb - 0.9, sz], ROCK * 0.5, 1)
    fade = 1 - ease((u - 0.35) / 0.4)
    for x in np.arange(-1.0, 1.0, 0.1):
        for z in (-1.0, 1.0):
            sc.seg([x, yb, z], [x + 0.05, yb, z], HOT * fade, 3)
        sc.seg([x, yb, -1.0], [x, yb, 1.0], HOT * 0.6 * fade, 1)
    sc.seg([0, yb + 0.9, 0], [0, yb - 0.9, 0], WHITE * 0.8, 3)
    if fade < 0.2:
        sc.circle([0, yb, 0], 0.15, WHITE, 2, 24)
    cam = look_at(*orbit([0, yb, 0], lerp(4.2, 3.2, ease(u)), 0.5 + 0.5 * u, lerp(0.3, 0.18, u)))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 12))


def sh_water(img, u, t, v, T):
    """Granite fracturé, eau chaude et salée qui circule dans les fissures."""
    sc = Scene()
    yb = -7 * KM
    sc.box([0, yb, 0], [2.0, 1.2, 2.0], ROCK * 0.45, 1, grid=4)
    n = int(len(CRACKS) * (0.3 + 0.7 * ease(u * 1.5)))
    for P in CRACKS[:n]:
        sc.add(P, ROCK * 0.9, 1)
    for i, (a, b, c, ph) in enumerate(DROPS):
        P = CRACKS[i % len(CRACKS)]
        f = (ph + 0.25 * t) % 1.0
        k = min(int(f * 3), 2); g = f * 3 - k
        p = P[k] + (P[k + 1] - P[k]) * g
        sc.circle(p, 0.018, WATER, 2, 8, axis="z")
    hole(sc, yb + 0.6, yb - 0.6, 0.06, WHITE * 0.7, n=10)
    cam = look_at(*orbit([0, yb, 0], lerp(2.9, 2.2, ease(u)), 0.9 + 0.6 * u + 0.8 * v, 0.2))
    draw(img, sc, cam, fade=(1, 7))


def sh_fossils(img, u, t, v, T):
    """24 microfossiles de plancton apparaissent un à un."""
    sc = Scene()
    n = 1 + int(23 * ease(u * 1.25))
    for i, (x, y, z, s, kind, rot) in enumerate(FOSS[:n]):
        col = GOLD if i % 2 == 0 else WHITE * 0.85
        fossil(sc, [x, y, z], s, kind, rot + 0.3 * t, col)
    cam = look_at(*orbit([0, 0, 0], lerp(4.6, 3.8, ease(u)), 0.25 * math.sin(0.4 * t) + 0.3 * v, 0.05))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(1, 10))


def sh_hydrogen(img, u, t, v, T):
    """Bulles d'hydrogène qui remontent le long du puits."""
    sc = Scene()
    strata(sc, 0.7, -2.2, ROCK, 8)
    hole(sc, 0.0, -2.2, 0.16, GOLD * 0.7, n=30)
    for a, b, c in BUB:
        y = -2.2 + ((a + 0.22 * t) % 1.0) * 2.4
        x, z = 0.1 * math.cos(6.28 * b), 0.1 * math.sin(6.28 * b)
        sc.circle([x, y, z], 0.02 + 0.03 * c, H2, 2, 12, axis="z")
    cam = look_at(*orbit([0, -0.9, 0], lerp(3.2, 2.6, ease(u)), 0.4 + 0.4 * u, 0.25))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 9))


def sh_heat(img, u, t, v, T):
    """La chaleur monte : roche qui rougit avec la profondeur, jauge 100 °C / 180 °C."""
    sc = Scene()
    strata(sc, 0.8, -DEPTH, ROCK, 14, hot=True)
    hole(sc, 0.0, -DEPTH, 0.06, GOLD, n=40, hot=True)
    gx, g0, g1 = 1.25, -DEPTH, 0.0                     # jauge 0-200 °C
    sc.add([[gx - 0.08, g0, 0], [gx + 0.08, g0, 0], [gx + 0.08, g1, 0], [gx - 0.08, g1, 0]], WHITE * 0.7, 2, closed=True)
    lvl = lambda c: g0 + (g1 - g0) * c / 200
    for c in range(0, 201, 20):
        sc.seg([gx + 0.08, lvl(c), 0], [gx + 0.16, lvl(c), 0], WHITE * 0.4, 1)
    sc.seg([gx - 0.3, lvl(100), 0], [gx + 0.3, lvl(100), 0], WATER, 2)    # prévu
    cur = 180 * ease(u * 1.3)
    for y in np.linspace(g0, lvl(cur), 30):
        sc.seg([gx - 0.06, y, 0], [gx + 0.06, y, 0], heat_col((y - g0) / max(g1 - g0, 1e-6) * 1.1), 2)
    cam = look_at(*orbit([0.4, -DEPTH / 2, 0], 6.0, 0.2 * math.sin(u * 2) + 0.2 * v, 0.05))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 16))


def sh_cap(img, u, t, v, T):
    """Site abandonné : ruines et couvercle d'acier boulonné sur le puits."""
    sc = Scene()
    sc.grid_plane(2.0, 16, 0.0, ROCK * 0.18)
    R = np.random.default_rng(92)
    for i in range(9):   # ruines : murs penchés
        x, z = R.uniform(-1.8, 1.8, 2)
        if abs(x) < 0.7 and abs(z) < 0.7: continue
        w, h = R.uniform(0.3, 0.7), R.uniform(0.2, 0.6)
        tilt = R.uniform(-0.3, 0.3)
        sc.add([[x - w / 2, 0, z], [x + w / 2, 0, z], [x + w / 2 + tilt, h, z], [x - w / 2 + tilt * 0.5, h * 0.7, z]], ROCK * 0.5, 1, closed=True)
    sc.circle([0, 0.03, 0], 0.23, STEEL, 3, 48)
    sc.circle([0, 0.03, 0], 0.18, STEEL * 0.6, 1, 40)
    for a in np.linspace(0, 2 * math.pi, 8, endpoint=False):
        sc.circle([0.205 * math.cos(a), 0.035, 0.205 * math.sin(a)], 0.012, WHITE, 2, 8)
    hole(sc, -0.02, -3.0, 0.23, GOLD * 0.25, n=24)
    cam = look_at(*orbit([0, 0, 0], lerp(3.4, 1.3, ease(u)), 0.8 - 0.5 * u, lerp(0.45, 0.95, ease(u))))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(1, 10))


def sh_earth(img, u, t, v, T):
    """La Terre en coupe : le puits n'est qu'une égratignure au pôle."""
    sc = Scene()
    R = 1.2
    for la in np.linspace(-1.2, 1.2, 7):
        sc.circle([0, R * math.sin(la), 0], R * math.cos(la), GOLD * 0.45, 1, 64)
    for lo in np.linspace(0, math.pi, 6, endpoint=False):
        th = np.linspace(0, 2 * math.pi, 80)
        sc.add(np.stack([R * np.cos(th) * math.cos(lo), R * np.sin(th), R * np.cos(th) * math.sin(lo)], 1), GOLD * 0.3, 1)
    for rr, c in ((R * 0.99, ROCK * 0.6), (R * 0.55, AMBER * 0.7), (R * 0.19, HOT)):   # croûte, noyau externe, graine
        sc.circle([0, 0, 0], rr, c, 2, 80, axis="z")
    d = R * 0.0019 * 6       # exagéré ×6 pour rester visible
    sc.seg([0, R, 0], [0, R - d, 0], WHITE, 3)
    sc.circle([0, R, 0], 0.03, WHITE, 2, 16, axis="z")
    sc.seg([0, R - d, 0.01], [0, 0, 0.01], WHITE * 0.15, 1)
    tgt = lerp([0, R, 0], [0, 0, 0], ease(u))
    cam = look_at(*orbit(tgt, lerp(0.45, 4.6, ease(u)), 0.2 * u, 0.05))
    stars(img, cam, T, 0.8, 0.03 * T); draw(img, sc, cam, fade=(1, 10))


def sh_final(img, u, t, v, T):
    """Retour au puits : on s'élève au-dessus de l'ouverture, en dessous l'inconnu."""
    sc = Scene()
    sc.grid_plane(1.4, 14, 0.0, ROCK * 0.2)
    hole(sc, 0.0, -DEPTH, 0.23, GOLD * lerp(0.8, 0.5, u)[()], n=80)
    sc.circle([0, 0.002, 0], 0.23, WHITE, 3, 48)
    sc.seg([-0.23, 0.01, 0.32], [0.23, 0.01, 0.32], AMBER, 3)
    for x in (-0.23, 0.23):
        sc.seg([x, 0.01, 0.27], [x, 0.01, 0.37], AMBER, 3)
    cam = look_at(*orbit([0, -0.3, 0], lerp(1.4, 2.4, ease(u)), 0.3 - 0.3 * u, lerp(1.2, 1.0, ease(u))))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(1, 9))
