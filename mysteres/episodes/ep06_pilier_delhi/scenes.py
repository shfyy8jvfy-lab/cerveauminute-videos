# Plans propres à l'épisode 6 : le pilier de fer de Delhi
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

IRON = np.array([0.80, 0.78, 0.70])      # BGR : fer gris-bleuté clair
STONE = np.array([0.45, 0.65, 0.80])
HEAT = np.array([0.10, 0.35, 1.00])      # orange vif
RED = np.array([0.20, 0.25, 1.00])
FILM = np.array([1.00, 0.85, 0.40])      # bleu-cyan : pellicule protectrice
WATER = np.array([1.00, 0.75, 0.35])
PH = np.array([0.30, 0.95, 0.55])        # vert : phosphore

H_P = 3.6        # hauteur hors capital (échelle 1/2)
DENT_Y = 2.0     # impact du boulet (~4 m réels)


def pillar(sc, col=IRON, c=(0, 0, 0), rings=24, dent=0.0, base=True):
    c = np.asarray(c, float)
    n = 14
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    r = lambda y: 0.135 - 0.025 * y / H_P
    for a in th:
        sc.seg(c + [r(0) * math.cos(a), 0, r(0) * math.sin(a)], c + [r(H_P) * math.cos(a), H_P, r(H_P) * math.sin(a)], col * 0.55, 1)
    for k in range(rings + 1):
        y = H_P * k / rings
        sc.circle(c + [0, y, 0], r(y), col if k in (0, rings) else col * 0.6, 2 if k in (0, rings) else 1, 28)
    sc.add([c + [r(0), 0, 0], c + [r(H_P), H_P, 0]], col, 2)
    sc.add([c + [-r(0), 0, 0], c + [-r(H_P), H_P, 0]], col, 2)
    # capital en cloche + abaque carré
    prof = [(0.00, 0.12), (0.05, 0.16), (0.12, 0.20), (0.20, 0.19), (0.26, 0.14), (0.30, 0.15), (0.34, 0.12)]
    for dy, rr in prof:
        sc.circle(c + [0, H_P + dy, 0], rr, col, 2, 32)
    for a in th[::2]:
        P = [c + [rr * math.cos(a), H_P + dy, rr * math.sin(a)] for dy, rr in prof]
        sc.add(P, col * 0.6, 1)
    sc.box(c + [0, H_P + 0.43, 0], [0.30, 0.18, 0.30], col, 2)
    sc.box(c + [0, H_P + 0.56, 0], [0.18, 0.08, 0.18], col * 0.8, 1)
    if base:
        sc.box(c + [0, -0.04, 0], [0.9, 0.08, 0.9], STONE * 0.7, 1, grid=3)
        sc.box(c + [0, 0.03, 0], [0.6, 0.06, 0.6], STONE * 0.8, 1)
    if dent > 0:
        p = c + [0, DENT_Y, r(DENT_Y)]
        sc.circle(p + [0, 0, 0.005], 0.05 * dent, WHITE * 0.9, 2, 16, "z")
        sc.circle(p + [0, 0, 0.005], 0.025 * dent, AMBER, 1, 12, "z")


def ground(sc, size=3, n=18, col=GOLD * 0.10):
    sc.grid_plane(size, n, -0.08, col)


def _cam_full(u, az0, az1, dist=(6.2, 5.4), el=(0.10, 0.18), y=2.0):
    return look_at(*orbit([0, y, 0], lerp(dist[0], dist[1], ease(u)), az0 + (az1 - az0) * u, lerp(el[0], el[1], u)))


# ------------------------------------------------------------------ plans
def sh_hook_pillar(img, u, t, v, T):
    sc = Scene(); ground(sc)
    pillar(sc, IRON * (0.7 + 0.3 * ease(u * 2)))
    # pluie fine qui tombe autour
    R = np.random.default_rng(7).uniform(0, 1, (70, 3))
    for x, z, ph in R:
        y = 4.6 - ((t * 2.2 + ph * 5) % 5.0)
        p = np.array([(x - 0.5) * 3, y, (z - 0.5) * 3])
        sc.seg(p, p + [0, -0.18, 0], WATER * 0.45, 1)
    cam = _cam_full(u, 0.5, -0.1, (4.9, 4.2), (0.02, 0.12), 2.1) if v == 0 else _cam_full(u, -0.6, -0.2, (4.3, 3.9), (0.25, 0.15), 2.2)
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(2, 14))


GLY = np.random.default_rng(12).integers(0, 6, (7, 9))


def sh_inscription(img, u, t, v, T):
    sc = Scene(); ground(sc)
    pillar(sc, IRON)
    # panneau d'inscription sur le fût (face +z), lignes de « glyphes » qui s'allument
    y0, y1 = 1.05, 1.45
    rz = 0.135 - 0.025 * 1.25 / H_P + 0.004
    sc.add([[-0.09, y0, rz], [0.09, y0, rz], [0.09, y1, rz], [-0.09, y1, rz]], GOLD * 0.6, 1, closed=True)
    nlit = int(ease(u * 1.3) * GLY.size)
    k = 0
    for i in range(GLY.shape[0]):
        y = y1 - 0.03 - i * 0.052
        for j in range(GLY.shape[1]):
            x = -0.08 + j * 0.019
            col = AMBER if k < nlit else GOLD * 0.15
            g = GLY[i, j]
            p = np.array([x, y, rz])
            if g == 0: sc.add([p, p + [0.012, 0, 0], p + [0.012, -0.02, 0]], col, 1)
            elif g == 1: sc.add([p + [0.006, 0, 0], p + [0.006, -0.025, 0], p + [0.014, -0.025, 0]], col, 1)
            elif g == 2: sc.circle(p + [0.007, -0.012, 0], 0.007, col, 1, 8, "z")
            elif g == 3: sc.add([p, p + [0.014, 0, 0], p + [0.002, -0.022, 0]], col, 1)
            elif g == 4: sc.add([p + [0, -0.02, 0], p + [0.007, 0, 0], p + [0.014, -0.02, 0]], col, 1)
            else: sc.add([p, p + [0.014, 0, 0], p + [0.007, -0.006, 0], p + [0.007, -0.024, 0]], col, 1)
            k += 1
    if v == 0:
        cam = look_at(*orbit([0, 1.6, 0], lerp(5.2, 2.6, ease(u)), 0.4 - 0.3 * u, lerp(0.05, 0.0, u)))
    else:
        cam = look_at(*orbit([0, 1.25, 0], lerp(1.6, 1.1, ease(u)), 0.15 - 0.25 * u, 0.02))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(1, 12))


def sh_pillar_measure(img, u, t, v, T):
    sc = Scene(); ground(sc)
    pillar(sc, IRON)
    top = H_P + 0.6
    h = top * ease(u * 1.6)
    x = 0.55
    sc.seg([x, 0, 0], [x, h, 0], AMBER, 2)
    for k in range(int(h / 0.25) + 1):
        y = k * 0.25
        sc.seg([x - 0.06, y, 0], [x + 0.06 if k % 4 == 0 else x, y, 0], AMBER * 0.8, 1)
    if u > 0.6:
        sc.seg([x - 0.12, top, 0], [x + 0.12, top, 0], WHITE, 2)
    # poids : ondes de pression au sol
    w = ease((u - 0.45) / 0.4)
    for k in range(3):
        rr = 0.5 + 0.35 * k + 0.25 * ((t * 0.8) % 1.0)
        sc.circle([0, -0.07, 0], rr, AMBER * w * (0.7 - 0.2 * k), 1, 48)
    cam = _cam_full(u, -0.5, -0.1, (4.6, 4.2), (0.06, 0.12), 2.2)
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(2, 14))


def sh_forge_weld(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(3, 18, -0.6, GOLD * 0.10)
    # enclume
    sc.box([0, -0.45, 0], [1.6, 0.3, 0.7], IRON * 0.6, 2)
    sc.box([0, -0.25, 0], [2.0, 0.1, 0.8], IRON * 0.8, 2)
    # barre horizontale qui s'allonge, morceau par morceau
    n = 8
    built = 2 + ease(u * 1.2) * (n - 2)
    for k in range(n):
        if k > built: break
        x = -1.4 + k * 0.35
        hot = max(0.0, 1.0 - (built - k) * 0.6)
        col = IRON * (1 - hot) + HEAT * hot
        rr = np.random.default_rng(k).uniform(0.85, 1.05, 2)
        sc.box([x, 0.0, 0], [0.34, 0.36 * rr[0], 0.36 * rr[1]], col, 2)
        sc.box([x, 0.0, 0], [0.34, 0.36 * rr[0], 0.36 * rr[1]], col * 0.3, 1, grid=2)
    xe = -1.4 + min(int(built), n - 1) * 0.35
    # marteau qui frappe la soudure
    ph = (t * 1.6) % 1.0
    lift = 0.9 * (1 - abs(math.sin(ph * math.pi))) if ph > 0.5 else 0.9 * ph * 2
    hy = 0.22 + (0.9 - lift if ph > 0.5 else lift) * 0.8
    hx = xe - 0.17
    sc.box([hx, hy + 0.12, 0], [0.22, 0.24, 0.4], COPPER, 2)
    sc.seg([hx, hy + 0.12, 0.2], [hx + 0.2, hy + 0.5, 1.0], COPPER * 0.8, 3)
    # étincelles à l'impact
    if hy < 0.35:
        R = np.random.default_rng(int(t * 10)).uniform(-1, 1, (16, 3))
        for d in R:
            p = np.array([hx, 0.2, 0]); sc.seg(p, p + d * [0.5, 0.4, 0.5] + [0, 0.3, 0], HEAT, 1)
    az = 0.5 + 0.4 * u if v == 0 else -0.5 + 0.3 * u
    cam = look_at(*orbit([-0.15, 0.15, 0], lerp(3.4, 2.9, ease(u)), az, 0.35))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 12))


def hill(sc, c, R, h, col):
    c = np.asarray(c, float)
    for k in range(6):
        f = k / 6
        sc.circle(c + [0, h * (1 - (1 - f) ** 2) * 0 + h * f, 0], R * (1 - f) ** 0.8, col * (0.6 + 0.4 * f), 1, 40)
    for a in np.linspace(0, 2 * math.pi, 12, endpoint=False):
        P = [c + [R * (1 - k / 6) ** 0.8 * math.cos(a), h * k / 6, R * (1 - k / 6) ** 0.8 * math.sin(a)] for k in range(7)]
        sc.add(P, col * 0.5, 1)


def sh_journey(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(6, 24, 0, GOLD * 0.10)
    A = np.array([0.3, 0, 2.6]); B = np.array([-0.3, 0, -2.6])
    hill(sc, A, 1.0, 0.8, STONE)
    # Delhi : petit complexe (enceinte + tour)
    sc.box(B + [0, 0.15, 0], [1.4, 0.3, 1.0], STONE * 0.7, 1, grid=3)
    for k in range(5):
        sc.circle(B + [0.45, 0.3 + k * 0.35, 0.25], 0.16 - 0.02 * k, STONE, 1, 16)
    sc.seg(B + [0.45, 0.3, 0.25], B + [0.45, 2.0, 0.25], STONE * 0.5, 1)
    # trajet en pointillés
    m = ease((u - 0.2) / 0.6)
    N = 40
    for k in range(N):
        f0, f1 = k / N, (k + 0.5) / N
        if f0 > m: break
        p0 = lerp(A + [0, 0.8, 0], B + [0, 0.3, 0], f0) + [0, 1.2 * math.sin(math.pi * f0), 0]
        p1 = lerp(A + [0, 0.8, 0], B + [0, 0.3, 0], f1) + [0, 1.2 * math.sin(math.pi * f1), 0]
        sc.seg(p0, p1, AMBER, 2)
    # le pilier (miniature) voyage
    pos = lerp(A + [0, 0.8, 0], B + [0, 0.3, 0], m) + [0, 1.2 * math.sin(math.pi * m), 0]
    s = Scene(); pillar(s, IRON, base=False, rings=8)
    for seg_, col, w in zip(s.segs, s.cols, s.wid):
        sc.segs.append(seg_ * 0.5 + pos); sc.cols.append(col); sc.wid.append(w)
    sc.circle(A + [0, 0.8, 0], 0.25, GOLD * 0.8, 2, 24)
    cam = look_at(*orbit([0, 0.6, 0], lerp(7.0, 6.2, ease(u)), 0.25 - 0.3 * u, 0.75))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 16))


def sh_cannonball(img, u, t, v, T):
    sc = Scene(); ground(sc)
    hit = 0.45
    pillar(sc, IRON, dent=1.0 if u > hit else 0.0)
    target = np.array([0, DENT_Y, 0.13])
    start = np.array([2.5, 2.9, 5.0])
    if u < hit:
        f = u / hit
        p = lerp(start, target, f) + [0, 0.6 * math.sin(math.pi * f), 0]
        sc.circle(p, 0.07, RED, 2, 16, "z"); sc.circle(p, 0.07, RED, 2, 16, "x")
        for k in range(1, 6):
            g = max(0, f - k * 0.03)
            q = lerp(start, target, g) + [0, 0.6 * math.sin(math.pi * g), 0]
            sc.circle(q, 0.03, RED * (0.5 - 0.08 * k), 1, 8, "z")
    else:
        f = ease((u - hit) / 0.15)
        fl = max(0.0, 1 - (u - hit) / 0.25)
        for k in range(10):
            a = 2 * math.pi * k / 10
            sc.seg(target, target + np.array([math.cos(a), math.sin(a), 0.3]) * 0.4 * f, HEAT * fl, 2)
        # fissures horizontales sur la face opposée
        for dy in (-0.05, 0.0, 0.05):
            sc.seg([-0.08, DENT_Y + dy, -0.12], [0.08, DENT_Y + dy, -0.12], AMBER * 0.7 * f, 1)
        p = lerp(target, target + [1.2, -2.0, 1.5], ease((u - hit) / 0.5))
        sc.circle(p, 0.07, RED * 0.6, 2, 16, "z")
    if v == 0:
        cam = look_at(*orbit([0, 2.0, 0], lerp(5.2, 3.0, ease(u)), 0.9 - 0.5 * u, 0.08))
    else:
        cam = look_at(*orbit([0, DENT_Y, 0], lerp(1.6, 1.2, ease(u)), 0.4 - 0.4 * u, 0.1))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(1, 12))


def lattice(sc, c, n, a, col, pfrac=0.0, seed=3, pcol=PH, rot=0.0):
    c = np.asarray(c, float)
    R = np.random.default_rng(seed).uniform(0, 1, (n, n, n))
    cr, sr = math.cos(rot), math.sin(rot)
    def P(i, j, k):
        x, y, z = (np.array([i, j, k]) - (n - 1) / 2) * a
        return c + [x * cr + z * sr, y, -x * sr + z * cr]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                p = P(i, j, k)
                if i < n - 1: sc.seg(p, P(i + 1, j, k), col * 0.25, 1)
                if j < n - 1: sc.seg(p, P(i, j + 1, k), col * 0.25, 1)
                if k < n - 1: sc.seg(p, P(i, j, k + 1), col * 0.25, 1)
                isp = R[i, j, k] < pfrac
                sc.circle(p, a * (0.22 if isp else 0.15), pcol if isp else col, 2 if isp else 1, 12, "z")


def sh_microscope(img, u, t, v, T):
    sc = Scene()
    # zoom à travers des anneaux de lentille jusqu'au réseau du métal
    lattice(sc, [0, 0, 0], 5, 0.45, IRON, 0.06, 3, rot=0.3 * t)
    for k in range(5):
        z = 3.5 - k * 1.6
        sc.circle([0, 0, z], 1.6 + 0.1 * k, GOLD * (0.6 - 0.08 * k), 2, 64, "z")
        sc.circle([0, 0, z], 1.45 + 0.1 * k, GOLD * (0.3 - 0.04 * k), 1, 64, "z")
    d = lerp(9.0, 3.6, ease(u))
    cam = look_at(*orbit([0, 0, 0], float(d), 0.25 * math.sin(t * 0.4) + 0.15 * v, 0.12))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(1, 14))


def sh_phosphorus(img, u, t, v, T):
    sc = Scene()
    w = ease(u * 1.5)
    lattice(sc, [0, 1.15, 0], 4, 0.42, IRON * 0.6, 0.02, 5, rot=0.2 * t)      # fer moderne
    lattice(sc, [0, -1.15, 0], 4, 0.42, IRON, 0.02 + 0.14 * w, 8, rot=-0.2 * t)  # fer du pilier
    sc.seg([-1.0, 0, 0], [1.0, 0, 0], GOLD * 0.3, 1)
    cam = look_at(*orbit([0, 0, 0], lerp(5.2, 4.6, ease(u)), 0.4 + 0.15 * math.sin(t * 0.5), 0.2))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 12))


def slab(sc, film_th, u, t, rain=True, sun=0.0):
    # coupe : métal en bas, pellicule au-dessus
    sc.box([0, -0.5, 0], [2.4, 1.0, 1.4], IRON, 2, grid=6)
    if film_th > 0.001:
        sc.box([0, film_th / 2, 0], [2.4, film_th, 1.4], FILM, 2)
        for k in range(12):
            x = -1.1 + k * 0.2
            sc.seg([x, 0, 0.7], [x + 0.1, film_th, 0.7], FILM * 0.6, 1)
    if rain:
        R = np.random.default_rng(4).uniform(0, 1, (40, 3))
        for x, z, ph in R:
            y = 2.2 - ((t * 1.8 + ph * 2.2) % 2.2)
            p = np.array([(x - 0.5) * 2.2, y + film_th, (z - 0.5) * 1.2])
            sc.seg(p, p + [0, -0.12, 0], WATER * 0.7, 1)
    if sun > 0:
        c = np.array([0.6, 1.5, -0.5])
        sc.circle(c, 0.25, AMBER * sun, 2, 32, "z")
        for k in range(10):
            a = 2 * math.pi * k / 10 + t * 0.3
            sc.seg(c + [0.35 * math.cos(a), 0.35 * math.sin(a), 0], c + [0.5 * math.cos(a), 0.5 * math.sin(a), 0], AMBER * sun, 1)


def sh_film(img, u, t, v, T):
    sc = Scene()
    cyc = (t * 0.5) % 2.0
    wet = cyc < 1.0
    slab(sc, 0.03 + 0.10 * ease(u), u, t, rain=wet, sun=0.0 if wet else 1.0)
    # atomes de phosphore qui migrent vers la surface
    R = np.random.default_rng(9).uniform(0, 1, (18, 3))
    for x, z, ph in R:
        y = -0.9 + ((t * 0.25 + ph) % 1.0) * 0.9
        sc.circle([(x - 0.5) * 2.0, y, (z - 0.5) * 1.2], 0.04, PH, 1, 10, "z")
    cam = look_at(*orbit([0, 0.3, 0], lerp(3.8, 3.1, ease(u)), 0.55 - 0.3 * u + 0.4 * v, 0.35))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 12))


def sh_film_grow(img, u, t, v, T):
    sc = Scene()
    th = 0.02 + 0.16 * ease(u)
    slab(sc, th, u, t, rain=False, sun=0.0)
    # jauge d'épaisseur
    x = 1.45
    sc.seg([x, 0, 0.7], [x, th, 0.7], WHITE, 2)
    sc.seg([x - 0.08, 0, 0.7], [x + 0.08, 0, 0.7], WHITE, 2)
    sc.seg([x - 0.08, th, 0.7], [x + 0.08, th, 0.7], WHITE, 2)
    # horloge des siècles qui tourne
    c = np.array([-0.2, 1.2, 0])
    sc.circle(c, 0.5, GOLD * 0.7, 2, 64, "z")
    for k in range(16):
        a = 2 * math.pi * k / 16
        sc.seg(c + [0.43 * math.cos(a), 0.43 * math.sin(a), 0], c + [0.5 * math.cos(a), 0.5 * math.sin(a), 0], GOLD * 0.6, 1)
    a = math.pi / 2 - 2 * math.pi * 3 * u
    sc.seg(c, c + [0.42 * math.cos(a), 0.42 * math.sin(a), 0], AMBER, 2)
    cam = look_at(*orbit([0, 0.35, 0], lerp(4.6, 4.0, ease(u)), 0.35 - 0.2 * u - 0.5 * v, 0.2))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 12))


def sh_final_pillar(img, u, t, v, T):
    sc = Scene(); ground(sc, 4, 24)
    pillar(sc, IRON, dent=1.0)
    # halo de la pellicule protectrice
    g = 0.5 + 0.5 * math.sin(t * 2)
    for k in range(6):
        sc.circle([0, 0.3 + k * 0.65, 0], 0.2, FILM * (0.3 + 0.3 * g), 1, 28)
    cam = _cam_full(u, -0.3, 0.6, (3.9, 5.0), (0.15, 0.05), 2.1)
    stars(img, cam, T, 0.9, spin=0.1 * u); draw(img, sc, cam, fade=(2, 16))
