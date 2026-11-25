# Plans propres à l'épisode 18 : l'acier de Damas et ses nanotubes
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

STEEL = np.array([0.95, 0.85, 0.70])    # BGR : acier bleuté
CYAN = np.array([1.00, 0.85, 0.30])
FIRE = np.array([0.18, 0.50, 1.00])
RED = np.array([0.20, 0.25, 1.00])
VIOLET = np.array([0.95, 0.40, 0.75])
GREEN = np.array([0.55, 0.95, 0.45])
R18 = np.random.default_rng(18)
RR = R18.uniform(0, 1, (600, 6))


def blade_pts(L=5.0, curve=0.55, w0=0.32, n=40):
    """Lame courbe (shamshir) dans le plan xy, de la garde (x=-L/2) à la pointe."""
    s = np.linspace(0, 1, n)
    x = -L / 2 + L * s
    yb = curve * L * 0.18 * (s ** 2)            # dos courbé
    w = w0 * (1 - s ** 1.6) + 0.01
    return s, x, yb, w


def sabre(sc, c=(0, 0, 0), L=5.0, b=1.0, waves=1.0, T=0.0, col=STEEL, wav=GOLD, fadeout=1.0):
    c = np.asarray(c, float)
    s, x, yb, w = blade_pts(L)
    P = lambda xx, yy, zz=0.0: np.stack([c[0] + xx, c[1] + yy, c[2] + np.full_like(np.asarray(xx, float), zz)], -1)
    keep = s <= fadeout + 1e-9
    for zz in (-0.03, 0.03):
        sc.add(P(x[keep], yb[keep], zz), col * b, 2)                     # dos
        sc.add(P(x[keep], (yb - w)[keep], zz * 0.2), WHITE * 0.9 * b, 2)   # tranchant
    sc.add(P(x[keep], (yb - w * 0.35)[keep], 0.04), col * 0.5 * b, 1)     # gorge
    # vagues de Damas : lignes ondulées entre dos et fil
    if waves > 0:
        nl = 9
        for k in range(nl):
            f = (k + 0.5) / nl
            ph = k * 1.7
            off = 0.10 * np.sin(x * 4.2 + ph + 0.6 * np.sin(x * 1.3 + k)) * w / 0.32
            yy = yb - w * f + off * 0.5
            yy = np.minimum(np.maximum(yy, yb - w + 0.01), yb - 0.01)
            m = keep & (s < 0.97)
            sc.add(P(x[m], yy[m], 0.035), wav * waves * (0.35 + 0.25 * (k % 2)) * b, 1)
    # garde et poignée
    g = c + [-L / 2, 0, 0]
    sc.seg(g + [0, 0.45, 0], g + [0, -0.75, 0], GOLD * b, 3)
    sc.add([g + [0, 0.45, 0], g + [0.12, 0.55, 0]], GOLD * b, 2)
    sc.add([g + [0, -0.75, 0], g + [0.12, -0.85, 0]], GOLD * b, 2)
    hx = np.linspace(0, 1.3, 12)
    for o in (-0.09, 0.09):
        sc.add(np.stack([g[0] - hx, g[1] - 0.15 + o - 0.12 * hx ** 2, np.full(12, g[2])], 1), COPPER * b, 2)
    for k in range(1, 6):
        xx = g[0] - 1.3 * k / 6
        yy = g[1] - 0.15 - 0.12 * (1.3 * k / 6) ** 2
        sc.seg([xx, yy - 0.09, g[2]], [xx + 0.05, yy + 0.09, g[2]], COPPER * 0.6 * b, 1)
    sc.circle(g + [-1.38, -0.37, 0], 0.13, GOLD * b, 2, n=20, axis="z")


def nanotube(sc, c=(0, 0, 0), r=0.6, L=4.0, b=1.0, n=14, rows=20, col=CYAN, axis="x", grow=1.0, rot=0.0):
    """Nanotube : réseau hexagonal (motif 'nid d'abeille') enroulé en cylindre."""
    c = np.asarray(c, float)
    def p(a, z):
        a = a + rot
        if axis == "x":
            return c + [z, r * math.cos(a), r * math.sin(a)]
        return c + [r * math.cos(a), z, r * math.sin(a)]
    da = 2 * math.pi / n; dz = L / rows
    zmax = -L / 2 + L * grow
    for i in range(rows):
        z = -L / 2 + i * dz
        if z > zmax: break
        for j in range(n):
            a = j * da + (i % 2) * da / 2
            # zigzag hexagonal
            A = p(a, z); B = p(a + da / 2, z + dz * 0.33); C = p(a + da / 2, z + dz)
            sc.seg(A, B, col * b, 1); sc.seg(B, C, col * b, 1)
            sc.seg(B, p(a + da, z), col * 0.8 * b, 1)
    for z in (-L / 2, zmax):
        P = [p(j * da, z) for j in range(n)]
        sc.add(P, WHITE * 0.8 * b, 2, closed=True)


def atom(sc, c, r, col, b=1.0, w=1):
    sc.circle(c, r, col * b, w, n=14, axis="z"); sc.circle(c, r, col * 0.6 * b, 1, n=14, axis="x")


def rotz(sc, ang, c=(0, 0, 0)):
    """Tourne toute la scène autour de l'axe z (pour dresser la lame à la verticale)."""
    ca, sa = math.cos(ang), math.sin(ang); c = np.asarray(c, float)
    M = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    sc.segs = [(S - c) @ M.T + c for S in sc.segs]
    return lambda p: (np.asarray(p, float) - c) @ M.T + c


UP = 1.35  # angle : lame dressée, légèrement inclinée


# ------------------------------------------------------------------ plans
def sh_hook_blade(img, u, t, v, T):
    """Le sabre courbe, la caméra plonge vers un point lumineux au milieu de la lame."""
    sc = Scene(); sabre(sc, [0.6, 0.3, 0], 5.2, 1.0, 1.0, T)
    pt = np.array([1.2, 0.3 + 0.55 * 5.2 * 0.18 * 0.6 ** 2 - 0.15, 0])
    for k in range(3):
        rr = 0.05 + ((t * 0.7 + k / 3) % 1) * 0.6
        sc.circle(pt, rr, CYAN * (1 - rr / 0.7), 2, n=32, axis="z")
    R = rotz(sc, UP); pt = R(pt)
    tgt = lerp([0.0, 0.3, 0], pt, ease(u))
    cam = look_at(*orbit(tgt, lerp(8.5, 2.4, ease(u)), 0.25 + 0.2 * u, 0.1))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 16))


def sh_nanotube(img, u, t, v, T):
    """Un nanotube de carbone qui tourne lentement, vu de biais."""
    sc = Scene()
    nanotube(sc, [0, 0, 0], 0.75, 5.0, 1.0, 14, 24, CYAN, "y", grow=min(1, 0.35 + u * 1.3), rot=T * 0.4)
    if v == 1:  # nanofils de cémentite autour
        for k in range(5):
            a = k * 1.25
            sc.seg([2.0 * math.cos(a), -2.6, 2.0 * math.sin(a)], [2.0 * math.cos(a) + 0.3, 2.6, 2.0 * math.sin(a)], AMBER * 0.8, 2)
    cam = look_at(*orbit([0, 0, 0], lerp(7.5, 6.3, ease(u)), 0.4 + 0.3 * u + v, 0.35))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(3, 14))


def sh_sabre(img, u, t, v, T):
    """Le sabre de Damas en entier, qui tourne."""
    sc = Scene(); sabre(sc, [0.5, 0, 0], 5.4, 1.0, 1.0, T)
    for k in range(5):
        sc.circle([0, -4.2, 0], 1.0 + 0.7 * k, GOLD * (0.3 - 0.05 * k), 1)
    rotz(sc, UP)
    cam = look_at(*orbit([0.0, 0.3, 0], lerp(7.6, 6.8, ease(u)), -0.6 + 1.2 * u, 0.1))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 18))


def sh_crucible(img, u, t, v, T):
    """Un creuset d'argile fermé dans le feu, le métal luit à l'intérieur."""
    sc = Scene()
    prof = [(0.55, -1.4), (0.62, -0.8), (0.6, 0.4), (0.5, 1.2), (0.45, 1.4)]
    for k in range(12):
        a = k * math.pi / 6
        sc.add([[r * math.cos(a), y, r * math.sin(a)] for r, y in prof], COPPER, 1)
    for r, y in prof:
        sc.circle([0, y, 0], r, COPPER * 0.8, 2 if y in (-1.4, 1.4) else 1)
    # couvercle "poivrière"
    for k in range(8):
        a = k * math.pi / 4
        sc.seg([0.45 * math.cos(a), 1.4, 0.45 * math.sin(a)], [0, 1.75, 0], COPPER * 0.8, 1)
    glow_l = 0.4 + 0.6 * ease(u)
    for k in range(6):
        y = -1.3 + 0.18 * k
        sc.circle([0, y, 0], 0.5, FIRE * glow_l * (1 - k / 7), 2 if k == 5 else 1)
    # flammes en dessous
    for k in range(18):
        r = RR[k]; a = r[0] * 6.28; d = 0.3 + 0.7 * r[1]
        h = 0.6 + 0.6 * r[2] * (0.8 + 0.2 * math.sin(T * 7 + k))
        ys = np.linspace(0, 1, 7)
        P = np.stack([d * math.cos(a) + 0.1 * np.sin(ys * 5 + T * 8 + k) * ys, -2.2 + ys * h, d * math.sin(a) + 0 * ys], 1)
        sc.add(P, (FIRE if k % 2 else RED), 2)
    sc.grid_plane(3, 10, -2.2, GOLD * 0.15)
    cam = look_at(*orbit([0, -0.2, 0], lerp(7.0, 6.0, ease(u)), 0.3 * T * 0.3, 0.25))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 14))


def sh_cake(img, u, t, v, T):
    """Une galette de wootz : disque bombé couvert de dendrites."""
    sc = Scene(); R0 = 1.6
    for k in range(7):
        rr = R0 * (1 - k / 7)
        sc.circle([0, 0.35 * (1 - (rr / R0) ** 2), 0], rr, STEEL * (0.9 - 0.08 * k), 2 if k == 0 else 1)
    sc.circle([0, -0.25, 0], R0, STEEL * 0.6, 2)
    for k in range(16):
        a = k * math.pi / 8
        sc.seg([R0 * math.cos(a), -0.25, R0 * math.sin(a)], [R0 * math.cos(a), 0, R0 * math.sin(a)], STEEL * 0.5, 1)
    # dendrites
    for k in range(22):
        r = RR[50 + k]; a = r[0] * 6.28; d = 0.2 + 1.2 * r[1]
        c0 = np.array([d * math.cos(a), 0.0, d * math.sin(a)])
        c0[1] = 0.36 * (1 - (d / R0) ** 2) + 0.01
        L = 0.25 + 0.2 * r[2]; ang = r[3] * 6.28
        dd = np.array([math.cos(ang), 0, math.sin(ang)])
        sc.seg(c0 - dd * L / 2, c0 + dd * L / 2, GOLD * 0.7, 1)
        pp = np.array([-dd[2], 0, dd[0]])
        for f in (-0.25, 0.0, 0.25):
            q = c0 + dd * L * f
            sc.seg(q, q + (pp + dd * 0.3) * L * 0.25, GOLD * 0.45, 1)
    cam = look_at(*orbit([0, 0, 0], lerp(5.6, 4.6, ease(u)), 0.4 * T * 0.3, lerp(0.75, 0.55, u)))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 12))


def sh_carbon(img, u, t, v, T):
    """Réseau cristallin de fer (cubes) avec des atomes de carbone qui s'allument."""
    sc = Scene(); n = 4; a = 0.9
    off = -(n - 1) * a / 2
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c = np.array([off + i * a, off + j * a, off + k * a])
                atom(sc, c, 0.12, STEEL * 0.8)
                if i < n - 1: sc.seg(c, c + [a, 0, 0], STEEL * 0.25, 1)
                if j < n - 1: sc.seg(c, c + [0, a, 0], STEEL * 0.25, 1)
                if k < n - 1: sc.seg(c, c + [0, 0, a], STEEL * 0.25, 1)
    nc = int(1 + 6 * ease(u * 1.3))
    for q in range(nc):
        r = RR[100 + q]
        c = np.array([off + a * (0.5 + int(r[0] * (n - 1))), off + a * (0.5 + int(r[1] * (n - 1))), off + a * (0.5 + int(r[2] * (n - 1)))])
        atom(sc, c, 0.18, GOLD, 1.2, 2)
    cam = look_at(*orbit([0, 0, 0], lerp(6.8, 5.8, ease(u)), 0.5 + 0.4 * u, 0.45))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 12))


def sh_forge(img, u, t, v, T):
    """Une enclume, un marteau qui frappe une lame incandescente."""
    sc = Scene()
    # enclume
    sc.box([0, -0.9, 0], [1.2, 0.8, 1.0], GOLD * 0.7, 2)
    sc.box([0, -0.35, 0], [2.6, 0.35, 1.0], GOLD, 2)
    sc.add([[1.3, -0.18, -0.5], [2.1, -0.3, 0], [1.3, -0.18, 0.5]], GOLD, 2)
    sc.add([[1.3, -0.52, -0.5], [1.6, -0.45, 0], [1.3, -0.52, 0.5]], GOLD * 0.6, 1)
    sc.box([0, -1.5, 0], [1.8, 0.4, 1.3], GOLD * 0.5, 1)
    # barre chaude
    sc.box([0.2, -0.1, 0], [2.4, 0.08, 0.3], FIRE, 2)
    # marteau
    ph = (t * 1.6) % 1; lift = 0.2 + 1.6 * (abs(math.sin(ph * math.pi)))
    hc = np.array([0.3, lift, 0])
    sc.box(hc + [0, 0.2, 0], [0.5, 0.4, 0.4], STEEL, 2)
    sc.seg(hc + [0, 0.2, 0], hc + [-1.6, 0.6, 0], COPPER, 3)
    if ph < 0.15 or ph > 0.9:
        for k in range(12):
            r = RR[200 + k]; a = r[0] * 6.28
            d = np.array([math.cos(a), 0.5 + r[1], math.sin(a)]) * (0.4 + 0.8 * r[2])
            sc.seg([0.3, -0.05, 0], np.array([0.3, -0.05, 0]) + d, np.array([0.45, 0.9, 1.0]), 1)
    cam = look_at(*orbit([0.2, -0.2, 0], lerp(6.5, 5.6, ease(u)), 0.6 + 0.3 * u, 0.25))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 14))


def sh_bands(img, u, t, v, T):
    """Gros plan sur les vagues de la lame : les bandes qui ondulent."""
    sc = Scene()
    xs = np.linspace(-3.5, 3.5, 90)
    for k in range(22):
        y = -1.6 + 3.2 * k / 21
        off = 0.18 * np.sin(xs * 2.1 + k * 0.9 + 0.8 * np.sin(xs * 0.7 + k * 0.3) + T * 0.4)
        col = GOLD if k % 2 else STEEL
        sc.add(np.stack([xs, y + off, np.zeros_like(xs)], 1), col * (0.5 + 0.5 * (k % 3 == 0)), 1 + (k % 3 == 0))
    sc.add([[-3.5, 1.8, 0], [3.5, 1.8, 0]], STEEL, 2)
    sc.add([[-3.5, -1.8, 0], [3.5, -1.8, 0]], WHITE * 0.9, 2)
    cam = look_at(*orbit([lerp(-0.8, 0.8, u), 0, 0], lerp(5.2, 4.6, ease(u)), 0.35 * math.sin(0.3 * T) + 0.2 * v, 0.1))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 12))


def sh_silk(img, u, t, v, T):
    """Un foulard qui tombe sur le fil de la lame et se sépare en deux."""
    sc = Scene()
    tmp = Scene(); sabre(tmp, [0.6, 0, 0], 5.0, 0.9, 0.7, T)
    for S in tmp.segs:          # retourné : le fil vers le haut
        S = S.copy(); S[..., 1] = -S[..., 1] - 1.3; sc.segs.append(S)
    sc.cols += tmp.cols; sc.wid += tmp.wid
    fy = lerp(2.0, -0.95, ease(min(1, u * 1.6)))[()]
    cut = u > 0.62
    nx, nz = 14, 9
    for half in ((-1.6, -0.02), (0.02, 1.6)) if cut else ((-1.6, 1.6),):
        sep = (u - 0.62) * 2.0 if cut else 0.0
        x0, x1 = half; sh = -sep if x1 < 0.5 else sep
        for i in range(nz):
            z = -1.0 + 2.0 * i / (nz - 1)
            xs = np.linspace(x0, x1, nx)
            ys = fy + 0.15 * np.sin(xs * 2 + T * 2 + z) + (np.abs(xs) * 0.6 * sep if cut else 0) * -1
            sc.add(np.stack([xs + sh, ys, np.full(nx, z)], 1), VIOLET * 0.8, 1)
        for xx in np.linspace(x0, x1, 7):
            zs = np.linspace(-1, 1, nz)
            ys = fy + 0.15 * np.sin(xx * 2 + T * 2 + zs) - (abs(xx) * 0.6 * sep if cut else 0)
            sc.add(np.stack([np.full(nz, xx + sh), ys, zs], 1), VIOLET * 0.5, 1)
    cam = look_at(*orbit([0.3, -0.4, 0], 5.0, 0.35 + 0.15 * u, 0.25))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 16))


def sh_lost(img, u, t, v, T):
    """La lame se dissout en poussière d'étoiles, de la pointe vers la garde."""
    sc = Scene()
    fo = 1.0 - 0.85 * ease(u) if v == 0 else 0.15 + 0.1 * (1 - u)
    sabre(sc, [0.5, 0, 0], 5.2, 0.9, 0.8, T, fadeout=fo)
    s, x, yb, w = blade_pts(5.2)
    for k in range(120):
        r = RR[300 + k]
        if r[0] < fo: continue
        si = int(r[0] * 39)
        drift = (r[0] - fo) * 3.0 * (0.5 + r[1])
        p = np.array([0.5 + x[si] + drift * 0.6, yb[si] - w[si] * r[2] + drift * (r[3] - 0.3), (r[4] - 0.5) * drift])
        sc.seg(p, p + [0.04, 0.04, 0], GOLD * (1 - min(1, drift / 3)), 2)
    rotz(sc, UP)
    cam = look_at(*orbit([0.0, 0.4, 0], 8.6, 0.2 + 0.2 * u, 0.08))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(3, 16))


def sh_acid(img, u, t, v, T):
    """Un bécher : un fragment de lame se dissout, des bulles montent."""
    sc = Scene()
    for y in (-1.6, 1.4):
        sc.circle([0, y, 0], 1.1, WHITE * 0.7, 2)
    for k in range(10):
        a = k * math.pi / 5
        sc.seg([1.1 * math.cos(a), -1.6, 1.1 * math.sin(a)], [1.1 * math.cos(a), 1.4, 1.1 * math.sin(a)], WHITE * 0.35, 1)
    sc.circle([0, 0.6, 0], 1.08, GREEN, 2)
    for k in range(3):
        sc.circle([0, 0.6 - 0.55 * (k + 1), 0], 1.06, GREEN * 0.3, 1)
    sz = lerp(1.0, 0.35, ease(u))[()]
    sc.box([0, -1.2, 0], [0.9 * sz, 0.12 * sz, 0.35 * sz], STEEL, 2)
    for k in range(30):
        r = RR[450 + k]
        yy = -1.1 + ((t * (0.4 + 0.5 * r[0]) + r[1]) % 1) * 1.65
        c = [(r[2] - 0.5) * 1.4, yy, (r[3] - 0.5) * 1.4]
        sc.circle(c, 0.04 + 0.04 * r[4], GREEN * 0.9, 1, n=10, axis="z")
    cam = look_at(*orbit([0, -0.2, 0], lerp(6.0, 5.0, ease(u)), 0.3 + 0.3 * u, 0.3))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 12))


def sh_microscope(img, u, t, v, T):
    """Colonne de microscope électronique : faisceau qui descend sur l'échantillon."""
    sc = Scene()
    for y in np.linspace(-0.6, 3.0, 7):
        sc.circle([0, y, 0], 0.55 if y > -0.5 else 0.8, WHITE * 0.7, 2)
    for k in range(8):
        a = k * math.pi / 4
        sc.seg([0.55 * math.cos(a), -0.6, 0.55 * math.sin(a)], [0.55 * math.cos(a), 3.0, 0.55 * math.sin(a)], WHITE * 0.3, 1)
    for k in range(3):  # lentilles
        y = 0.4 + k * 0.9
        sc.circle([0, y, 0], 0.75, CYAN, 2)
    sc.box([0, -1.4, 0], [2.4, 0.1, 1.6], GOLD * 0.6, 1)
    sc.box([0, -1.3, 0], [0.5, 0.06, 0.5], STEEL, 2)
    hb = ease(min(1, u * 1.5))
    for k in range(6):
        a = k * math.pi / 3
        sc.seg([0.1 * math.cos(a), 2.8, 0.1 * math.sin(a)], [0.02 * math.cos(a), lerp(2.8, -1.27, hb)[()], 0.02 * math.sin(a)], CYAN, 1)
    if hb > 0.95:
        for k in range(3):
            rr = 0.05 + ((t * 0.8 + k / 3) % 1) * 0.6
            sc.circle([0, -1.26, 0], rr, CYAN * (1 - rr / 0.7), 2, n=24)
    cam = look_at(*orbit([0, 0.6, 0], lerp(8.5, 7.5, ease(u)), 0.5 + 0.3 * u, 0.18))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 16))


def sh_vanadium(img, u, t, v, T):
    """Le réseau de fer, quelques atomes de vanadium (rouges), et des bandes qui s'alignent."""
    sc = Scene(); n = 5; a = 0.8
    off = -(n - 1) * a / 2
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c = np.array([off + i * a, off + j * a, off + k * a])
                atom(sc, c, 0.09, STEEL * 0.55)
    hot = [(1, 2, 3), (3, 1, 1)] if v == 0 else [(1, 2, 3), (3, 1, 1), (2, 4, 0)]
    for (i, j, k) in hot:
        c = np.array([off + i * a, off + j * a, off + k * a])
        atom(sc, c, 0.2 + 0.03 * math.sin(T * 4), RED, 1.3, 2)
    if v == 1:  # bandes de carbures qui naissent
        xs = np.linspace(-2, 2, 40)
        for q in range(5):
            y = -1.6 + q * 0.8
            yy = y + 0.12 * np.sin(xs * 2 + q) * ease(u)
            sc.add(np.stack([xs, yy, np.full(40, 2.0)], 1), GOLD * ease(u), 2)
    cam = look_at(*orbit([0, 0, 0.3 * v], lerp(7.0, 6.0, ease(u)), 0.4 + 0.4 * u - 0.6 * v, 0.35 - 0.25 * v))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 13))


def sh_ore(img, u, t, v, T):
    """Une colline de minerai dont les filons s'éteignent un à un."""
    sc = Scene()
    xs = np.linspace(-4, 4, 41)
    for i in range(12):
        z = -3 + 6 * i / 11
        y = 1.8 * np.exp(-(xs ** 2 + z ** 2) / 6) - 1.2
        sc.add(np.stack([xs, y, np.full_like(xs, z)], 1), COPPER * 0.6, 1)
    for i in range(12):
        x = -4 + 8 * i / 11
        zs = np.linspace(-3, 3, 31)
        y = 1.8 * np.exp(-(x ** 2 + zs ** 2) / 6) - 1.2
        sc.add(np.stack([np.full_like(zs, x), y, zs], 1), COPPER * 0.35, 1)
    for k in range(10):
        r = RR[520 + k]
        alive = r[0] > ease(u)
        a = r[1] * 6.28; d = 0.3 + 1.6 * r[2]
        p0 = np.array([d * math.cos(a), 0, d * math.sin(a)])
        p0[1] = 1.8 * math.exp(-(p0[0] ** 2 + p0[2] ** 2) / 6) - 1.2 + 0.02
        p1 = p0 + [0.5 * math.cos(a + 1), -0.05, 0.5 * math.sin(a + 1)]
        sc.seg(p0, p1, (RED if alive else STEEL * 0.2), 4 if alive else 1)
        if alive:
            sc.circle(p0, 0.15, RED * 0.8, 2, n=12)
    cam = look_at(*orbit([0, -0.4, 0], lerp(7.0, 6.0, ease(u)), 0.3 * T * 0.2, 0.75))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 16))


def sh_doubt(img, u, t, v, T):
    """Le nanotube vacille : il apparaît puis se brouille."""
    sc = Scene()
    flick = 0.55 + 0.45 * math.sin(T * 5) * math.sin(T * 1.7)
    nanotube(sc, [0, 0, 0], 0.7, 4.5, flick, 12, 20, CYAN, "y", rot=T * 0.3)
    # point d'interrogation en fil de fer
    th = np.linspace(math.pi, -math.pi / 2, 20)
    q = np.stack([2.1 + 0.45 * np.cos(th), 1.0 + 0.45 * np.sin(th), np.zeros(20)], 1)
    sc.add(q, GOLD, 3); sc.seg(q[-1], q[-1] + [0, -0.5, 0], GOLD, 3)
    sc.circle([2.1, -0.25, 0], 0.07, GOLD, 3, n=10, axis="z")
    cam = look_at(*orbit([0.8, 0, 0], lerp(7.5, 6.6, ease(u)), 0.15 * math.sin(0.4 * T), 0.15))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 14))


def sh_final(img, u, t, v, T):
    """Le sabre seul ; un nanotube lumineux en son cœur ; la caméra recule."""
    sc = Scene(); sabre(sc, [0.5, 0, 0], 5.2, 1.0, 1.0, T)
    nanotube(sc, [1.1, 0.12, 0], 0.08, 0.9, 1.2, 8, 8, CYAN, "x", rot=T)
    for k in range(3):
        rr = 0.1 + ((t * 0.5 + k / 3) % 1) * 0.9
        sc.circle([1.1, 0.12, 0], rr, CYAN * 0.7 * (1 - rr / 1.0), 1, n=32, axis="z")
    R = rotz(sc, UP); c0 = R([1.1, 0.12, 0])
    cam = look_at(*orbit(lerp(c0, [0, 0.3, 0], ease(u)), lerp(2.6, 8.8, ease(u)), 0.3 + 0.2 * u, 0.1))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(2, 18))
