# Plans propres à l'épisode 11 : 'Oumuamua, premier objet interstellaire (2017)
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE...)

RUST = np.array([0.25, 0.35, 0.95])      # BGR : rouge sombre de l'objet
CYAN = np.array([1.00, 0.85, 0.35])
SUNC = np.array([0.45, 0.85, 1.00])
HYD = np.array([1.00, 0.55, 0.75])
R11 = np.random.default_rng(11)
H2 = R11.normal(0, 1, (90, 3))


def rot(ax, ay, az):
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def cigar(sc, c, L=1.0, r=0.12, R=np.eye(3), col=RUST, w=2, nl=9, nr=10):
    """Objet très allongé (ellipsoïde ~ 8:1) en fil de fer, un peu irrégulier."""
    c = np.asarray(c, float)
    th = np.linspace(0, 2 * math.pi, nr + 1)
    xs = np.linspace(-1, 1, nl)
    for x in xs[1:-1]:
        rr = r * math.sqrt(max(1 - x * x, 0)) * (1 + 0.12 * math.sin(5 * x + 1))
        P = np.stack([np.full_like(th, x * L), rr * np.cos(th), rr * 0.8 * np.sin(th)], 1)
        sc.add(c + P @ R.T, col * 0.7, 1)
    xx = np.linspace(-1, 1, 30)
    for k in range(6):
        a = 2 * math.pi * k / 6
        rr = r * np.sqrt(np.maximum(1 - xx * xx, 0)) * (1 + 0.12 * np.sin(5 * xx + 1))
        P = np.stack([xx * L, rr * math.cos(a), rr * 0.8 * math.sin(a)], 1)
        sc.add(c + P @ R.T, col, w)


def sun(sc, c=(0, 0, 0), r=0.18, t=0.0):
    c = np.asarray(c, float)
    for ax in ("y", "z", "x"):
        sc.circle(c, r, SUNC, 2, 32, axis=ax)
    for k in range(12):
        a = 2 * math.pi * k / 12 + 0.2 * t
        d = np.array([math.cos(a), 0, math.sin(a)])
        sc.seg(c + d * r * 1.3, c + d * r * (1.7 + 0.15 * math.sin(3 * t + k)), SUNC * 0.6, 1)


def orbits(sc, radii=(0.5, 0.8, 1.1, 1.6), col=WHITE * 0.3):
    for rr in radii:
        sc.circle([0, 0, 0], rr, col, 1, 72)


def hyper(s, q=0.6, e=1.6):
    """Branche d'hyperbole (paramètre s), foyer à l'origine, dans le plan xz."""
    a = q / (e - 1); b = a * math.sqrt(e * e - 1)
    x = a * np.cosh(s) - a * e
    z = b * np.sinh(s)
    return np.stack([-x, np.zeros_like(s), z], 1)


def fv(x):
    return float(np.asarray(x))


# ------------------------------------------------------------------ plans
def sh_hook_flyby(img, u, t, v, T):
    """Le système solaire ; un objet allongé arrive d'en haut, frôle le Soleil et repart."""
    sc = Scene(); sun(sc, t=t); orbits(sc)
    s = np.linspace(-2.2, 2.2, 160)
    P = hyper(s)
    # inclinaison : il plonge par au-dessus du plan des planètes
    P = P @ rot(0.9, 0, 0).T
    k = int(lerp(20, 150, ease(u)))
    sc.add(P[:k], CYAN * 0.55, 1)
    p = P[k]; d = P[k + 1] - P[k - 1]
    ay = math.atan2(-d[2], d[0]); az = math.atan2(d[1], math.hypot(d[0], d[2]))
    cigar(sc, p, 0.38, 0.05, rot(0, ay, az) @ rot(1.7 * t, 0, 0), RUST, 2)
    cam = look_at(*orbit([0, 0, 0], lerp(5.4, 4.6, ease(u)), 0.5 + 0.25 * u, 0.55))
    stars(img, cam, T, 1.0, 0.02 * T); draw(img, sc, cam, fade=(2, 12))


def sh_hook_push(img, u, t, v, T):
    """Gros plan : l'objet s'éloigne et une flèche de poussée apparaît."""
    sc = Scene()
    R = rot(0.9 * t, 0.4, 0.25 * math.sin(t))
    c = np.array([0, 0, -0.6 * u])
    cigar(sc, c, 1.0, 0.13, R, RUST, 2)
    a = ease((u - 0.2) * 2)
    if a > 0:
        tip = c + np.array([0, 0, -1.6 * a])
        sc.seg(c + [0, 0, -0.2], tip, WHITE, 3)
        for s_ in (-1, 1):
            sc.seg(tip, tip + [0.12 * s_, 0, 0.18], WHITE, 3)
    cam = look_at(*orbit([0, 0, -0.5], lerp(3.6, 3.2, ease(u)), 1.0 + 0.3 * u, 0.3))
    stars(img, cam, T, 1.0); draw(img, sc, cam, fade=(1, 8))


def telescope(sc, s=1.0, pitch=0.9, col=GOLD):
    """Monture, tube en treillis, coupole ouverte."""
    # coupole
    for k in range(7):
        lat = (k / 6) * math.pi / 2
        r = 1.15 * s * math.cos(lat); y = 0.9 * s + 1.15 * s * math.sin(lat)
        th = np.linspace(0.6, 2 * math.pi - 0.6, 50)
        sc.add(np.stack([r * np.cos(th), np.full_like(th, y), r * np.sin(th)], 1), col * 0.35, 1)
    th = np.linspace(0, 2 * math.pi, 50)
    for y in (0, 0.9 * s):
        sc.add(np.stack([1.15 * s * np.cos(th), np.full_like(th, y), 1.15 * s * np.sin(th)], 1), col * 0.5, 1)
    for k in range(10):
        a = 2 * math.pi * k / 10
        sc.seg([1.15 * s * math.cos(a), 0, 1.15 * s * math.sin(a)], [1.15 * s * math.cos(a), 0.9 * s, 1.15 * s * math.sin(a)], col * 0.35, 1)
    # pilier + fourche
    sc.box([0, 0.45 * s, 0], [0.3 * s, 0.9 * s, 0.3 * s], col * 0.8, 1)
    piv = np.array([0, 1.1 * s, 0])
    d = np.array([math.cos(pitch), math.sin(pitch), 0.0])
    n = np.array([0, 0, 1.0])
    up = np.cross(n, d)
    for f0, f1 in ((-0.55, 1.1),):
        for a in range(8):
            ang = 2 * math.pi * a / 8
            off = (up * math.cos(ang) + n * math.sin(ang)) * 0.28 * s
            sc.seg(piv + d * f0 * s + off, piv + d * f1 * s + off, col, 2 if a % 2 == 0 else 1)
        for f in (f0, 0.2, f1):
            P = [piv + d * f * s + (up * math.cos(2 * math.pi * a / 16) + n * math.sin(2 * math.pi * a / 16)) * 0.28 * s for a in range(16)]
            sc.add(P, col, 2, closed=True)
    return piv + d * 1.1 * s, d


def sh_telescope(img, u, t, v, T):
    """Le télescope sur la montagne ; un point de lumière file dans le ciel."""
    sc = Scene()
    tip, d = telescope(sc, 0.9, 0.95)
    sc.grid_plane(4, 16, 0, DIM * 0.5)
    tgt = tip + d * 2.6 + np.array([lerp(-1.0, 1.0, u), 0, 0])
    sc.seg(tip, tgt, CYAN * 0.25, 1)
    sc.circle(tgt, 0.04 + 0.01 * math.sin(8 * t), WHITE, 2, 12, axis="z")
    sc.seg(tgt - [0.35, 0, 0], tgt, CYAN * 0.5, 1)
    az = [0.6, -0.5, 1.4][v % 3]
    cam = look_at(*orbit([0, 1.5, 0], lerp(5.6, 4.8, ease(u)), az + 0.25 * u, 0.32))
    stars(img, cam, T, 1.0, 0.02 * T); draw(img, sc, cam, fade=(2, 12))


def sh_hyperbola(img, u, t, v, T):
    """Orbites fermées des planètes contre la branche ouverte de l'intrus."""
    sc = Scene(); sun(sc, t=t)
    for rr, ee in ((0.6, 0.0), (1.0, 0.1), (1.5, 0.3)):
        th = np.linspace(0, 2 * math.pi, 90)
        r_ = rr * (1 - ee * ee) / (1 + ee * np.cos(th))
        sc.add(np.stack([r_ * np.cos(th), np.zeros_like(th), r_ * np.sin(th)], 1), WHITE * 0.4, 1, closed=True)
    s = np.linspace(-2.4, 2.4, 160)
    P = hyper(s, 0.5, 1.9)
    k = int(lerp(10, 159, ease(u * 1.2)))
    sc.add(P[:k + 1], CYAN, 3)
    sc.add(np.stack([np.linspace(-3.5, 3.5, 2), [0, 0], [0, 0]], 1), WHITE * 0.12, 1)
    cigar(sc, P[k], 0.15, 0.025, rot(2 * t, 0, 0), RUST, 2)
    cam = look_at(*orbit([-0.3, 0, 0], lerp(6.0, 5.2, ease(u)), 0.2 * u, 1.15))
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(2, 12))


LYRA = np.array([[0, 0.9, 0], [-0.25, 0.45, 0], [0.12, 0.42, 0], [-0.32, -0.25, 0], [0.05, -0.3, 0]]) * 1.6


def sh_vega(img, u, t, v, T):
    """La constellation de la Lyre ; une trajectoire part de Véga vers nous."""
    sc = Scene()
    for a, b in ((0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)):
        sc.seg(LYRA[a], LYRA[b], GOLD * 0.6, 1)
    for i, p in enumerate(LYRA):
        r = 0.09 if i == 0 else 0.04
        sc.circle(p, r * (1 + 0.15 * math.sin(4 * t)), WHITE if i == 0 else GOLD, 2, 20, axis="z")
        if i == 0:
            for k in range(4):
                a = k * math.pi / 4
                sc.seg(p + [0.16 * math.cos(a), 0.16 * math.sin(a), 0], p - [0.16 * math.cos(a), 0.16 * math.sin(a), 0], WHITE * 0.7, 1)
    a = ease(u * 1.1)
    start = LYRA[0]; end = np.array([0.0, -1.6, 3.0])
    p = start + (end - start) * a
    sc.seg(start, p, CYAN * 0.6, 1)
    cigar(sc, p, 0.25, 0.04, rot(2.2 * t, 0.6, 0.4), RUST, 2)
    cam = look_at(*orbit([0, 0.0, 0.6], 4.4 - 0.6 * ease(u), 0.25 * math.sin(0.3 * t), 0.08))
    stars(img, cam, T, 1.1, 0.01 * T); draw(img, sc, cam, fade=(2, 12))


def sh_name(img, u, t, v, T):
    """Gros plan de l'éclaireur, lent tour d'horizon."""
    sc = Scene()
    cigar(sc, [0, 0, 0], 1.1, 0.14, rot(0.5 * t, 0, 0.2), RUST, 2, 13, 14)
    cam = look_at(*orbit([0, 0, 0], lerp(3.4, 2.8, ease(u)), 0.6 + 0.6 * u, 0.25))
    stars(img, cam, T, 1.0); draw(img, sc, cam, fade=(1, 8))


def sh_leaving(img, u, t, v, T):
    """Il a déjà contourné le Soleil et file vers l'extérieur."""
    sc = Scene(); sun(sc, t=t); orbits(sc, (0.5, 0.8, 1.1))
    s = np.linspace(-1.6, 1.6, 160)
    P = hyper(s, 0.4, 1.3)
    k0 = 80
    k = int(lerp(k0 + 5, 158, ease(u)))
    sc.add(P[:k0], CYAN * 0.3, 1)
    sc.add(P[k0:k + 1], CYAN, 2)
    sc.circle(P[k0], 0.05, WHITE, 2, 12, axis="z")
    cigar(sc, P[k], 0.3, 0.05, rot(2 * t, 0, 0), RUST, 2)
    cam = look_at(*orbit(lerp([0, 0, 0], P[k] * 0.6, ease(u)), lerp(4.4, 5.6, ease(u)), 1.0 + 0.2 * u, 0.7))
    stars(img, cam, T, 1.0, 0.02 * T); draw(img, sc, cam, fade=(2, 12))


def sh_lightcurve(img, u, t, v, T):
    """L'objet tourne ; sa luminosité trace une courbe qui varie d'un facteur dix."""
    sc = Scene()
    ph = 2.2 * t
    cigar(sc, [0, 0.9, 0], 0.7, 0.09, rot(0, ph, 0), RUST, 2)
    # axes du graphe
    x0, x1, y0 = -1.3, 1.3, -0.9
    sc.seg([x0, y0, 0], [x1, y0, 0], WHITE * 0.5, 1); sc.seg([x0, y0, 0], [x0, y0 + 1.1, 0], WHITE * 0.5, 1)
    xs = np.linspace(x0, x1, 120)
    k = max(2, int(120 * ease(u * 1.2)))
    ys = y0 + 0.08 + 0.95 * (0.5 + 0.5 * np.cos(2 * (xs - x0) * 2.4)) ** 2
    sc.add(np.stack([xs[:k], ys[:k], np.zeros(k)], 1), GOLD, 2)
    cam = look_at(*orbit([0, 0.1, 0], lerp(4.4, 4.0, ease(u)), 0.15 * math.sin(0.4 * t), 0.08))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(1, 10))


def sh_cigar(img, u, t, v, T):
    """Proportions : environ dix fois plus long que large."""
    sc = Scene()
    R = rot(0.3 * t, 0, 0)
    cigar(sc, [0, 0, 0], 1.25, 0.13, R, RUST, 2, 13, 12)
    a = ease(u * 1.6)
    sc.seg([-1.25, -0.4, 0], [-1.25 + 2.5 * a, -0.4, 0], WHITE * 0.8, 2)
    for x in (-1.25, -1.25 + 2.5 * a):
        sc.seg([x, -0.47, 0], [x, -0.33, 0], WHITE * 0.8, 2)
    sc.seg([1.45, -0.13, 0], [1.45, 0.13, 0], WHITE * 0.8, 2)
    cam = look_at(*orbit([0, -0.05, 0], lerp(3.9, 3.5, ease(u)), 0.1 * u, 0.15))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(1, 9))


def sh_tumble(img, u, t, v, T):
    """Culbute : rotation sur plusieurs axes à la fois, trace lumineuse des extrémités."""
    sc = Scene()
    def Rt(tt): return rot(0.9 * tt, 0.55 * tt, 0.3 * tt)
    R = Rt(t)
    cigar(sc, [0, 0, 0], 1.0, 0.12, R, RUST, 2, 11, 12)
    trail = np.array([Rt(t - 0.05 * k) @ np.array([1.0, 0, 0]) for k in range(40)])
    sc.add(trail, GOLD * 0.6, 1); sc.add(-trail, GOLD * 0.6, 1)
    az = [0.4, 2.0, -1.0][v % 3]
    cam = look_at(*orbit([0, 0, 0], lerp(3.6, 3.2, ease(u)), az + 0.3 * u, 0.3))
    stars(img, cam, T, 1.0); draw(img, sc, cam, fade=(1, 8))


def sh_accel(img, u, t, v, T):
    """Trajectoire prévue (gravité seule) en pointillés ; la vraie s'en écarte."""
    sc = Scene(); sun(sc, [-1.6, 0, 0], 0.14, t)
    s = np.linspace(0, 1, 100)
    pred = np.stack([-1.2 + 3.0 * s, np.zeros_like(s), -0.2 - 1.2 * s ** 1.2], 1)
    real = pred + np.stack([0.0 * s, 0.0 * s, -0.9 * s ** 2], 1) + np.stack([0.25 * s ** 2, 0.0 * s, 0 * s], 1)
    for i in range(0, 98, 4):
        sc.seg(pred[i], pred[i + 2], WHITE * 0.55, 1)
    k = max(2, int(100 * ease(u * 1.1)))
    sc.add(real[:k], CYAN, 3)
    p = real[min(k, 99)]
    cigar(sc, p, 0.18, 0.03, rot(2 * t, 0, 0), RUST, 2)
    if u > 0.5:
        gap = ease((u - 0.5) * 3)
        sc.seg(pred[min(k, 99)], pred[min(k, 99)] + (p - pred[min(k, 99)]) * gap, GOLD, 2)
    cam = look_at(*orbit([0.6, 0, -1.2], lerp(4.6, 4.2, ease(u)), -0.1 + 0.15 * u, 1.0))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(2, 10))


def sh_nocoma(img, u, t, v, T):
    """Une comète fantôme (avec queue) s'efface ; l'objet nu, sans queue."""
    sc = Scene()
    R = rot(0.7 * t, 0.3, 0)
    cigar(sc, [0, 0, 0], 0.9, 0.11, R, RUST, 2)
    g = 1 - ease((u - 0.2) * 2.5)
    if g > 0.02:
        for k in range(14):
            a = 2 * math.pi * k / 14
            P = [[0.1 * math.cos(a) * (1 + 3 * f), 0.1 * math.sin(a) * (1 + 3 * f), 0.3 + 3.2 * f] for f in np.linspace(0, 1, 12)]
            sc.add(P, CYAN * 0.5 * g, 1)
        for r in (0.4, 0.6):
            sc.circle([0, 0, 0], r, CYAN * 0.4 * g, 1, 40, axis="z")
    if u > 0.55:
        a = ease((u - 0.55) * 3)
        c = np.array([0, 0, 0.6])
        sc.seg(c + [-0.45, -0.45, 0], c + [-0.45 + 0.9 * a, -0.45 + 0.9 * a, 0], WHITE, 3)
        sc.seg(c + [0.45, -0.45, 0], c + [0.45 - 0.9 * a, -0.45 + 0.9 * a, 0], WHITE, 3)
    cam = look_at(*orbit([0, 0, 0.8], lerp(4.4, 3.9, ease(u)), 0.35 + 0.2 * u, 0.25))
    stars(img, cam, T, 1.0); draw(img, sc, cam, fade=(1, 10))


def sh_hydrogen(img, u, t, v, T):
    """Coupe de l'objet : glace, molécules de H2 qui s'échappent côté Soleil."""
    sc = Scene()
    R = rot(0.25 * t, 0, 0)
    cigar(sc, [0, 0, 0], 1.1, 0.16, R, RUST * 0.8, 2, 11, 12)
    # cristaux de glace à l'intérieur
    for k in range(9):
        x = -0.8 + 1.6 * k / 8
        sc.box(R @ np.array([x, 0, 0]), [0.08, 0.08, 0.08], WHITE * 0.45, 1)
    # molécules H2 (deux petits cercles) qui s'échappent
    for i in range(26):
        ph = ((t * 0.35 + i / 26) % 1)
        base = R @ np.array([-1.0 + 2.0 * (i % 13) / 12, 0.0, 0.0])
        d = H2[i] * 0.15 + np.array([0, 0.25, 0])
        p = base + np.array([0, 0.14, 0]) + d * ph * 4 * ease(u * 2)
        c = HYD * (1 - ph)
        sc.circle(p, 0.025, c, 1, 10, axis="z")
        sc.circle(p + [0.05, 0, 0], 0.025, c, 1, 10, axis="z")
        sc.seg(p, p + [0.05, 0, 0], c, 1)
    sun(sc, [0, 2.6, -1.0], 0.2, t)
    cam = look_at(*orbit([0, 0.4, 0], lerp(4.0, 3.4, ease(u)), 0.2 + 0.25 * u, 0.2))
    stars(img, cam, T, 0.7); draw(img, sc, cam, fade=(1, 10))


def sh_fading(img, u, t, v, T):
    """Le télescope pointe ; l'objet s'éloigne et s'éteint."""
    sc = Scene()
    tip, d = telescope(sc, 0.7, 1.0, GOLD * 0.8)
    far = tip + d * lerp(2.0, 8.0, ease(u))
    b = 1 - ease(u * 1.1)
    sc.seg(tip, far, CYAN * 0.2, 1)
    cigar(sc, far, 0.3, 0.05, rot(2 * t, 0.3, 0), RUST * max(b, 0.05), 2)
    cam = look_at(*orbit([0, 1.6, 0], lerp(5.0, 5.6, ease(u)), 0.9 - 0.2 * u, 0.15))
    stars(img, cam, T, 0.8, 0.02 * T); draw(img, sc, cam, fade=(2, 14))


def sh_final(img, u, t, v, T):
    """L'éclaireur s'enfonce dans le noir, entre les étoiles."""
    sc = Scene()
    z = lerp(0.0, -6.0, ease(u))
    b = 1 - 0.85 * ease(u)
    cigar(sc, [0, 0, fv(z)], 0.9, 0.11, rot(0.6 * t, 0.4, 0.2), RUST * b, 2, 11, 12)
    s = np.linspace(0, 1, 40)
    sc.add(np.stack([np.zeros_like(s), np.zeros_like(s), fv(z) + 3.0 * s], 1), CYAN * 0.25 * b, 1)
    cam = look_at(*orbit([0, 0, fv(z)], lerp(3.2, 5.5, ease(u)), 0.5 + 0.3 * u, 0.2))
    stars(img, cam, T, 1.2, 0.01 * T); draw(img, sc, cam, fade=(1, 12))
