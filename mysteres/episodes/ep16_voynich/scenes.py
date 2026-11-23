# Plans propres à l'épisode 16 : le manuscrit de Voynich
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

VELLUM = np.array([0.62, 0.80, 0.92])    # BGR : parchemin clair
INK = np.array([0.55, 0.75, 1.00])
GREEN = np.array([0.45, 0.85, 0.35])
BLUE = np.array([1.00, 0.70, 0.30])
UVC = np.array([1.00, 0.35, 0.75])       # violet ultraviolet
RED = np.array([0.30, 0.30, 1.00])
R16 = np.random.default_rng(16)
RND = R16.uniform(-1, 1, (600, 6))


def _arc(cx, cy, r, a0, a1, n=10):
    return [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(a0, a1, n)]


# Glyphes inventés « à la Voynich » : traits 2D dans une cellule (x 0-1, y 0-1)
GLYPHS = [
    [_arc(0.5, 0.3, 0.25, 0, 2 * math.pi, 12)],                                         # o
    [_arc(0.5, 0.3, 0.22, 0.3, 2 * math.pi - 0.3, 10), [(0.7, 0.4), (0.75, 0.0), (0.6, -0.25)]],  # 9
    [[(0.2, 0.0), (0.2, 0.9)], [(0.7, 0.0), (0.7, 0.9)], _arc(0.45, 0.55, 0.25, math.pi, 0, 8), [(0.0, 0.4), (0.95, 0.4)]],  # potence
    [[(0.3, 0.0), (0.3, 0.6)], _arc(0.3, 0.6, 0.15, 0, math.pi, 6)],                     # i/e
    [_arc(0.5, 0.2, 0.2, 0, 2 * math.pi, 10), _arc(0.5, 0.55, 0.15, 0, 2 * math.pi, 10)],  # 8
    [[(0.1, 0.0), (0.5, 0.6), (0.9, 0.0)], [(0.5, 0.6), (0.5, 0.8)]],                    # a pointu
    [_arc(0.4, 0.3, 0.22, -2.6, 2.6, 10), [(0.6, 0.45), (0.9, 0.6)]],                     # c
    [[(0.2, 0.0), (0.2, 0.9)], _arc(0.45, 0.65, 0.25, math.pi, -0.3, 9), [(0.68, 0.55), (0.6, 0.0)]],  # potence 2
    [[(0.2, 0.5), (0.4, 0.0), (0.6, 0.5), (0.8, 0.0)]],                                   # m
    [_arc(0.5, 0.3, 0.22, math.pi * 0.5, math.pi * 2.3, 10), [(0.5, 0.52), (0.85, 0.85)]],
]
GL_RNG = np.random.default_rng(408)
LINES = [[GL_RNG.integers(0, len(GLYPHS), GL_RNG.integers(2, 7)) for _ in range(8)] for _ in range(30)]


def glyph_line(sc, origin, ex, ey, words, size=0.12, col=INK, w=1, upto=1e9):
    """Écrit une ligne de « mots » à partir de origin, axes ex (droite) et ey (haut)."""
    origin = np.asarray(origin, float); ex = np.asarray(ex, float); ey = np.asarray(ey, float)
    x = 0.0; n = 0
    for word in words:
        for g in word:
            if n >= upto: return x
            for stroke in GLYPHS[g]:
                sc.add([origin + ex * (x + px * size * 0.8) + ey * (py * size) for px, py in stroke], col, w)
            x += size * 0.85; n += 1
        x += size * 0.7
    return x


def page_text(sc, c, ex, ey, wdt, hgt, nlines=10, size=0.11, col=INK, seed=0, upto=1e9, w=1):
    c = np.asarray(c, float); ex = np.asarray(ex, float); ey = np.asarray(ey, float)
    cnt = 0
    for k in range(nlines):
        L = LINES[(k + seed) % len(LINES)]
        o = c - ex * (wdt / 2 - 0.08) + ey * (hgt / 2 - 0.15 - k * hgt * 0.9 / nlines)
        # tronque à la largeur
        words, x = [], 0
        for wd in L:
            if x + (len(wd) * 0.85 + 0.7) * size > wdt - 0.16: break
            words.append(wd); x += (len(wd) * 0.85 + 0.7) * size
        n_here = sum(len(wd) for wd in words)
        glyph_line(sc, o, ex, ey, words, size, col, w, upto=max(0, upto - cnt))
        cnt += n_here
        if cnt >= upto: return


def page(sc, c, ex, ey, wdt=1.6, hgt=2.2, col=VELLUM, w=2):
    c = np.asarray(c, float); ex = np.asarray(ex, float); ey = np.asarray(ey, float)
    P = [c + ex * sx * wdt / 2 + ey * sy * hgt / 2 for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    sc.add(P, col, w, closed=True)


def mini_plant(sc, c, ex, ey, s=0.5, col=GREEN, b=1.0):
    c = np.asarray(c, float); ex = np.asarray(ex, float); ey = np.asarray(ey, float)
    sc.add([c + ey * (y * s) + ex * 0.05 * math.sin(6 * y) for y in np.linspace(-0.6, 0.6, 8)], col * b, 1)
    for k, y in enumerate((-0.1, 0.2, 0.45)):
        for sd in (-1, 1):
            sc.add([c + ey * (y * s) + ex * sd * (q * s * 0.5) + ey * (0.25 * math.sin(math.pi * q) * s * 0.4) for q in np.linspace(0, 1, 7)], col * b, 1)
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * 0.4
        sc.seg(c - ey * 0.6 * s, c - ey * 0.6 * s + (ex * math.cos(a) + ey * math.sin(a)) * 0.35 * s, AMBER * 0.8 * b, 1)


def book(sc, c=(0, 0, 0), open_a=1.0, wdt=1.6, hgt=2.2, upto=1e9, ink=INK, b=1.0, pages=True, plant=True, seed=0):
    """Livre ouvert : deux pages inclinées d'un angle open_a (0 fermé, 1 à plat légèrement en V)."""
    c = np.asarray(c, float)
    ang = lerp(0.02, 1.38, open_a)[()]  # angle de chaque page par rapport au plan vertical
    ey = np.array([0, 0, -1.0])           # le haut de la page pointe vers -z (livre posé)
    out = []
    for sd in (-1, 1):
        ex = np.array([sd * math.sin(ang), math.cos(ang), 0.0])
        pc = c + ex * wdt / 2
        page(sc, pc, ex, ey, wdt, hgt, VELLUM * b, 2)
        # épaisseur (tranche)
        for k in range(1, 4):
            q = pc - [0, 0.025 * k, 0]
            sc.seg(q + ex * wdt / 2 - ey * hgt / 2, q + ex * wdt / 2 + ey * hgt / 2, VELLUM * 0.35 * b, 1)
        if pages:
            if sd == -1 and plant:
                mini_plant(sc, pc + ey * 0.3, ex * -1 * -1, ey, s=0.9, b=b)
                page_text(sc, pc - ey * 0.55, ex, ey, wdt, 0.9, nlines=3, size=0.09, col=ink * b, seed=seed, upto=upto)
            else:
                page_text(sc, pc, ex, ey, wdt, hgt, nlines=11, size=0.09, col=ink * b, seed=seed + 5, upto=upto)
        out.append((pc, ex))
    sc.seg(c + [0, 0, -hgt / 2], c + [0, 0, hgt / 2], AMBER * b, 2)  # reliure
    return out


def flat_page(sc, c=(0, 0, 0), wdt=2.2, hgt=3.0, b=1.0):
    """Page posée face caméra dans le plan xy."""
    c = np.asarray(c, float)
    page(sc, c, [1, 0, 0], [0, 1, 0], wdt, hgt, VELLUM * b, 2)
    return c


# ------------------------------------------------------------------ plans
def sh_hook_book(img, u, t, v, T):
    """Le livre s'ouvre, l'écriture inconnue s'allume."""
    sc = Scene()
    oa = ease(min(1, u * 1.8)) if v == 0 else 1.0
    book(sc, [0, 0, 0], oa, upto=int(40 + 900 * ease(u)) if v == 0 else 1e9)
    if v == 0:
        cam = look_at(*orbit([0, 0.4, 0], lerp(4.6, 3.4, ease(u)), 0.35 * math.sin(0.3 * T), lerp(0.9, 1.15, u)))
    else:
        cam = look_at(*orbit([0.8, 0.2, 0], lerp(3.6, 2.8, ease(u)), 0.5 - 0.3 * u, 1.0))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(2, 14))


def sh_yale_vault(img, u, t, v, T):
    """Bibliothèque : façade à panneaux translucides, vitrine centrale avec le livre."""
    sc = Scene()
    if v % 2 == 0:
        sc.box([0, 3.0, 0], [8, 6, 8], GOLD, 2)
        for i in range(1, 6):
            for j in range(1, 5):
                x = -4 + i * 8 / 6; y = j * 6 / 5
                sc.box([x, y, 4.0], [1.2, 1.1, 0.02], AMBER * 0.5, 1)
        for sx in (-3.6, 3.6):
            for sz in (-3.6, 3.6):
                sc.seg([sx, -1.2, sz], [sx, 0, sz], GOLD, 3)
        sc.grid_plane(10, 20, -1.2, GOLD * 0.07)
        cam = look_at(*orbit([0, 2.5, 0], lerp(20, 17, ease(u)), 0.5 + 0.4 * u, 0.15))
    else:
        sc.box([0, 1.0, 0], [3.2, 0.2, 2.6], GOLD, 2)
        sc.box([0, 2.0, 0], [3.2, 2.0, 2.6], WHITE * 0.35, 1)
        for sx in (-1.5, 1.5):
            for sz in (-1.2, 1.2):
                sc.seg([sx, 0, sz], [sx, 1.0, sz], GOLD * 0.7, 2)
        book(sc, [0, 1.15, 0], 0.85, wdt=1.2, hgt=1.7)
        cam = look_at(*orbit([0, 1.3, 0], lerp(6.5, 5.4, ease(u)), -0.4 + 0.5 * u, 0.55))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 30))


def sh_villa(img, u, t, v, T):
    """Villa d'un collège jésuite sur une colline près de Rome."""
    sc = Scene()
    sc.box([0, 2.0, 0], [12, 4, 4], GOLD, 2)
    for i in range(9):
        x = -5.3 + i * 1.32
        for y in (1.0, 2.8):
            sc.add([[x - 0.3, y - 0.5, 2.01], [x + 0.3, y - 0.5, 2.01], [x + 0.3, y + 0.4, 2.01]] + [[x + 0.3 * math.cos(a), y + 0.4 + 0.3 * math.sin(a), 2.01] for a in np.linspace(0, math.pi, 7)] + [[x - 0.3, y - 0.5, 2.01]], AMBER * 0.7, 1)
    sc.add([[-6.4, 4.0, -2.2], [6.4, 4.0, -2.2], [6.4, 4.0, 2.2], [-6.4, 4.0, 2.2]], AMBER, 2, closed=True)
    sc.box([0, 5.0, 0], [3.0, 2.0, 2.4], GOLD, 2)
    sc.circle([0, 6.0, 0], 1.0, AMBER, 2, 32)
    sc.seg([0, 6.0, 0], [0, 7.2, 0], WHITE * 0.7, 2); sc.seg([-0.35, 6.85, 0], [0.35, 6.85, 0], WHITE * 0.7, 2)
    for k, z in enumerate((-6, -12, 9)):
        sc.add([[x, -0.3 + 0.8 * math.sin(0.25 * x + k) - 0.04 * abs(z), z] for x in np.linspace(-20, 20, 60)], GREEN * (0.5 - 0.1 * k), 1)
    for j in range(8):  # cyprès
        x = -9 + j * 2.6 if j < 4 else 1.2 + j * 1.6
        if abs(x) < 6.5: continue
        sc.add([[x - 0.35, 0, 3], [x, 2.6, 3], [x + 0.35, 0, 3]], GREEN * 0.7, 1, closed=True)
    sc.grid_plane(14, 20, 0, GOLD * 0.06)
    dist = [24, 17, 20][v % 3]
    cam = look_at(*orbit([0, 3.0, 0], lerp(dist, dist - 3, ease(u)), [-0.5, 0.5, 0.1][v % 3] + 0.3 * u, 0.12 + 0.05 * v))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(6, 40))


def sh_carbon(img, u, t, v, T):
    """Bande de parchemin et atome de carbone 14 : 6 protons, 8 neutrons."""
    sc = Scene()
    if v % 2 == 0:
        c = np.array([0, 1.2, 0])
        nuc = [(GOLD if k < 6 else WHITE * 0.7) for k in range(14)]
        for k in range(14):
            phi = math.acos(1 - 2 * (k + 0.5) / 14); th = math.pi * (1 + 5 ** 0.5) * k
            p = c + 0.42 * np.array([math.sin(phi) * math.cos(th), math.cos(phi), math.sin(phi) * math.sin(th)])
            sc.circle(p, 0.17, nuc[k], 2, 16, axis="z"); sc.circle(p, 0.17, nuc[k] * 0.6, 1, 16, axis="x")
        for k in range(3):
            a = 0.7 * k
            R = np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]])
            tilt = np.array([[1, 0, 0], [0, math.cos(1.1), -math.sin(1.1)], [0, math.sin(1.1), math.cos(1.1)]])
            P = [c + R @ tilt @ np.array([2.0 * math.cos(q), 0, 2.0 * math.sin(q)]) for q in np.linspace(0, 2 * math.pi, 60)]
            sc.add(P, AMBER * 0.6, 1, closed=True)
            q = 2 * t * (1 + 0.3 * k) + k
            e = c + R @ tilt @ np.array([2.0 * math.cos(q), 0, 2.0 * math.sin(q)])
            sc.circle(e, 0.09, WHITE, 2, 10, axis="z")
        cam = look_at(*orbit(c, lerp(5.6, 4.6, ease(u)), 0.4 * T, 0.3))
    else:
        # bande de parchemin et frise du temps 1400-1450
        flat_page(sc, [-1.0, 1.0, 0], 2.0, 2.8)
        page_text(sc, [-1.0, 1.0, 0.01], [1, 0, 0], [0, 1, 0], 2.0, 2.8, nlines=12, size=0.1)
        sc.box([1.6, 1.0, 0], [0.35, 2.2, 0.02], WHITE, 2)
        sc.seg([-3, -1.4, 0], [3, -1.4, 0], GOLD, 2)
        for k in range(6):
            x = -3 + k * 1.2; sc.seg([x, -1.5, 0], [x, -1.3, 0], GOLD, 1)
        f = ease(u * 1.4)
        xa, xb = -3 + 6 * 4 / 50, -3 + 6 * 38 / 50
        sc.add([[xa, -1.4, 0.02], [lerp(xa, xb, f)[()] + 0.01, -1.4, 0.02]], WHITE, 5)
        cam = look_at(*orbit([0, 0.2, 0], lerp(6.6, 5.8, ease(u)), 0.3 - 0.3 * u, 0.1))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(3, 16))


def sh_glyphs(img, u, t, v, T):
    """Gros plan : les glyphes inconnus s'écrivent ligne après ligne."""
    sc = Scene()
    flat_page(sc, [0, 0, 0], 3.2, 4.4)
    n = int(20 + 400 * ease(min(1, (u + v) / 2 * 1.2)))
    page_text(sc, [0, 0, 0.01], [1, 0, 0], [0, 1, 0], 3.2, 4.4, nlines=12, size=0.2, upto=n, w=2, seed=3 * v)
    cams = [(4.2, -0.25, 0.1), (2.8, 0.3, -0.1), (3.5, 0.0, 0.25)]
    d, az, el = cams[v % 3]
    tgt = [lerp(-0.6, 0.6, u)[()] * (v % 2 * 2 - 1), 0.8 - 0.8 * v * 0.5, 0]
    cam = look_at(*orbit(tgt, d - 0.4 * u, az + 0.15 * u, el))
    draw(img, sc, cam, fade=(1, 10))


def weird_plant(sc, c=(0, 0, 0), grow=1.0, b=1.0):
    c = np.asarray(c, float)
    h = 4.2 * grow
    stem = [c + [0.25 * math.sin(2.2 * y), y, 0.15 * math.cos(1.7 * y)] for y in np.linspace(0, h, 30)]
    sc.add(stem, GREEN * b, 3)
    for k in range(6):  # feuilles
        y = 0.8 + k * 0.55
        if y > h: break
        a = k * 2.1
        base = c + [0.25 * math.sin(2.2 * y), y, 0.15 * math.cos(1.7 * y)]
        d = np.array([math.cos(a), 0.35, math.sin(a)])
        L = 1.4 * (1 - 0.08 * k) * min(1, (h - y) / 0.8)
        perp = np.cross(d, [0, 1, 0]); perp /= np.linalg.norm(perp) + 1e-9
        P = [base + d * L * q + perp * 0.4 * L * math.sin(math.pi * q) for q in np.linspace(0, 1, 9)]
        Q = [base + d * L * q - perp * 0.4 * L * math.sin(math.pi * q) for q in np.linspace(0, 1, 9)]
        sc.add(P + Q[::-1], GREEN * 0.8 * b, 1)
        sc.seg(base, base + d * L, GREEN * 0.5 * b, 1)
    if grow > 0.95:  # fleur étrange
        top = stem[-1]
        for k in range(7):
            a = k * 2 * math.pi / 7
            sc.add([top + [0.7 * q * math.cos(a), 0.5 * q + 0.3 * math.sin(math.pi * q), 0.7 * q * math.sin(a)] for q in np.linspace(0, 1, 7)], BLUE * b, 2)
        sc.circle(top + [0, 0.15, 0], 0.25, RED * b, 2, 16)
    # racines tentaculaires, très voynichiennes
    for k in range(7):
        a = k * 2 * math.pi / 7 + 0.3
        R = [c + [0.9 * q * math.cos(a + 0.6 * q), -1.4 * q * q - 0.1 * q, 0.9 * q * math.sin(a + 0.6 * q)] for q in np.linspace(0, min(1, grow * 1.3), 10)]
        sc.add(R, AMBER * 0.85 * b, 2)
    sc.add([c + [0.55 * math.cos(a), -0.05, 0.55 * math.sin(a)] for a in np.linspace(0, 2 * math.pi, 20)], AMBER * 0.6 * b, 1)


def sh_plant(img, u, t, v, T):
    sc = Scene()
    weird_plant(sc, [0, -0.6, 0], grow=ease(min(1, u * 1.5 + 0.15)) if v == 0 else 1.0)
    d = [9.0, 6.5, 7.5][v % 3]
    cam = look_at(*orbit([0, 1.5 - 0.3 * v, 0], lerp(d, d - 1.0, ease(u)), 0.5 * T * 0.3 + v, 0.15 + 0.1 * (v % 2)))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(3, 16))


def sh_zodiac(img, u, t, v, T):
    """Roue du ciel : anneaux concentriques, 12 secteurs, étoiles, soleil central."""
    sc = Scene()
    for r, col in ((3.2, GOLD), (2.6, AMBER), (1.6, GOLD * 0.7), (0.6, WHITE)):
        sc.circle([0, 0, 0], r, col, 2, 96, axis="z")
    rot = 0.15 * T
    for k in range(12):
        a = rot + k * math.pi / 6
        sc.seg([1.6 * math.cos(a), 1.6 * math.sin(a), 0], [3.2 * math.cos(a), 3.2 * math.sin(a), 0], AMBER * 0.6, 1)
        b = a + math.pi / 12
        for j in range(4):  # petites étoiles
            rr = 2.75 + 0.3 * ((j * 7 + k) % 3) / 2
            p = np.array([rr * math.cos(b + 0.1 * (j - 1.5)), rr * math.sin(b + 0.1 * (j - 1.5)), 0])
            for q in range(4):
                s = q * math.pi / 4
                sc.seg(p - 0.06 * np.array([math.cos(s), math.sin(s), 0]), p + 0.06 * np.array([math.cos(s), math.sin(s), 0]), WHITE * 0.8, 1)
        glyph_line(sc, np.array([2.0 * math.cos(b), 2.0 * math.sin(b), 0]), [math.cos(b + math.pi / 2), math.sin(b + math.pi / 2), 0], [math.cos(b), math.sin(b), 0], [LINES[k][0][:3]], size=0.14, col=INK)
    for k in range(16):
        a = -rot * 2 + k * math.pi / 8
        sc.seg([0.6 * math.cos(a), 0.6 * math.sin(a), 0], [1.1 * math.cos(a), 1.1 * math.sin(a), 0], GOLD, 2)
    cam = look_at(*orbit([0, 0, 0], lerp(10.5, 9.0, ease(u)), 0.35 * math.sin(0.4 * T), 0.15 + 0.15 * u))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(4, 20))


def bather(sc, c, s=0.5, col=VELLUM):
    """Silhouette stylisée et minimaliste (cercle + traits), sans visage."""
    c = np.asarray(c, float)
    sc.circle(c + [0, 1.5 * s, 0], 0.22 * s, col, 1, 12, axis="z")
    sc.seg(c + [0, 1.28 * s, 0], c + [0, 0.4 * s, 0], col, 1)
    sc.seg(c + [0, 1.1 * s, 0], c + [-0.4 * s, 1.5 * s, 0], col, 1)
    sc.seg(c + [0, 1.1 * s, 0], c + [0.4 * s, 1.5 * s, 0], col, 1)


def sh_baths(img, u, t, v, T):
    """Bassins reliés par des conduits, silhouettes immergées."""
    sc = Scene()
    pools = [(-3.0, 0.0, 0), (0.0, -0.8, 0), (3.0, 0.4, 0)]
    for i, (x, y, z) in enumerate(pools):
        sc.add([[x - 1.2, y + 0.6, 0], [x - 1.0, y - 0.6, 0], [x + 1.0, y - 0.6, 0], [x + 1.2, y + 0.6, 0]], GOLD, 2)
        sc.add([[x + q, y + 0.3 + 0.05 * math.sin(4 * q + 3 * t + i), 0.01] for q in np.linspace(-1.1, 1.1, 24)], BLUE, 2)
        for k in range(2):
            bather(sc, [x - 0.45 + 0.9 * k, y - 0.55, 0.02], 0.75, col=WHITE)
    for a, b in ((0, 1), (1, 2)):
        xa, ya, _ = pools[a]; xb, yb, _ = pools[b]
        P = [[lerp(xa + 1.1, xb - 1.1, q)[()], lerp(ya + 0.4, yb + 0.4, q)[()] + 0.9 * math.sin(math.pi * q), 0] for q in np.linspace(0, 1, 16)]
        sc.add(P, AMBER, 2); sc.add([[p[0], p[1] + 0.12, 0] for p in P], AMBER * 0.6, 1)
        q = (t * 0.5 + a * 0.4) % 1
        sc.circle([lerp(xa + 1.1, xb - 1.1, q)[()], lerp(ya + 0.4, yb + 0.4, q)[()] + 0.9 * math.sin(math.pi * q) + 0.06, 0], 0.06, BLUE, 2, 8, axis="z")
    # tuyau vertical venant du haut
    sc.add([[-3.0 + 0.4 * math.sin(y), 1.0 + y, 0] for y in np.linspace(0, 3, 14)], AMBER, 2)
    cam = look_at(*orbit([0, 0.3, 0], lerp(7.6, 6.8, ease(u)), 0.3 * math.sin(0.3 * T) + 0.2 * v, 0.1))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(4, 20))


def coin(sc, c, r=0.6, h=0.12, col=GOLD, b=1.0):
    c = np.asarray(c, float)
    sc.circle(c, r, col * b, 2, 32); sc.circle(c + [0, h, 0], r, col * b, 2, 32)
    sc.circle(c + [0, h + 0.001, 0], r * 0.7, col * 0.5 * b, 1, 24)
    for a in np.linspace(0, 2 * math.pi, 12, endpoint=False):
        sc.seg(c + [r * math.cos(a), 0, r * math.sin(a)], c + [r * math.cos(a), h, r * math.sin(a)], col * 0.5 * b, 1)


def crown(sc, c, r=1.2, col=AMBER):
    c = np.asarray(c, float)
    sc.circle(c, r, col, 2, 40)
    pts = []
    for k in range(17):
        a = k * 2 * math.pi / 16
        hh = 0.9 if k % 2 == 0 else 0.35
        pts.append(c + [r * math.cos(a), hh, r * math.sin(a)])
    sc.add(pts, col, 2)
    for k in range(0, 16, 2):
        a = k * 2 * math.pi / 16
        sc.circle(c + [r * math.cos(a), 1.0, r * math.sin(a)], 0.08, WHITE, 1, 8, axis="z")


def sh_ducats(img, u, t, v, T):
    sc = Scene()
    n = int(3 + 27 * ease(min(1, u * 1.4))) if v == 0 else 30
    for k in range(n):
        st = k % 3; lvl = k // 3
        coin(sc, [(st - 1) * 1.4, lvl * 0.14, 0.3 * (st % 2)], 0.6)
    crown(sc, [0, 2.4 + 0.1 * math.sin(T), -1.0], 1.0)
    sc.grid_plane(6, 16, 0, GOLD * 0.07)
    cam = look_at(*orbit([0, 1.4, 0], lerp(8.0, 6.5, ease(u)), 0.4 * T * 0.4 + v, 0.35))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(3, 18))


def sh_uv_sign(img, u, t, v, T):
    """Une lampe UV balaie la page : une signature effacée apparaît."""
    sc = Scene()
    flat_page(sc, [0, 0, 0], 3.0, 4.0)
    mini_plant(sc, [0, 0.6, 0.01], [1, 0, 0], [0, 1, 0], s=2.0)
    page_text(sc, [0, -1.3, 0.01], [1, 0, 0], [0, 1, 0], 3.0, 1.0, nlines=3, size=0.14)
    sx = lerp(-1.8, 1.8, ease(min(1, (u + v) / 2 * 1.5)))[()]
    sc.seg([sx, -2.0, 0.02], [sx, 2.0, 0.02], UVC, 3)
    sc.box([sx, 2.4, 0.4], [0.5, 0.3, 0.3], UVC * 0.8, 2)
    # signature en cursive dans la marge du bas, révélée derrière le faisceau
    xs = np.linspace(-1.3, 1.1, 120)
    sig = [[x, -1.85 + 0.09 * math.sin(14 * x) + 0.05 * math.sin(31 * x + 1), 0.015] for x in xs if x < sx]
    if len(sig) > 1:
        sc.add(sig, UVC * 1.2, 2)
        for x0 in (-1.2, -0.4, 0.5):
            if x0 < sx:
                sc.add([[x0 + 0.08 * math.cos(a), -1.75 + 0.18 * math.sin(a), 0.015] for a in np.linspace(0, 2 * math.pi, 12)], UVC, 1)
    cams = [(5.8, -0.2, 0.05, 0.0), (3.0, 0.15, -0.05, -1.4), (4.0, 0.3, 0.1, -0.6)]
    d, az, el, ty = cams[v % 3]
    cam = look_at(*orbit([0, ty, 0], d - 0.4 * u, az + 0.1 * u, el))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(2, 12))


def punch_card(sc, c, w=3.2, h=1.4, b=1.0, seed=0, col=AMBER):
    c = np.asarray(c, float)
    sc.add([c + [-w / 2, -h / 2, 0], c + [w / 2 - 0.2, -h / 2, 0], c + [w / 2, -h / 2 + 0.2, 0], c + [w / 2, h / 2, 0], c + [-w / 2, h / 2, 0]], col * b, 2, closed=True)
    rr = np.random.default_rng(seed)
    for i in range(24):
        for j in range(8):
            if rr.random() < 0.18:
                x = -w / 2 + 0.2 + i * (w - 0.4) / 23; y = -h / 2 + 0.2 + j * (h - 0.4) / 7
                sc.add([c + [x - 0.03, y - 0.05, 0], c + [x + 0.03, y - 0.05, 0], c + [x + 0.03, y + 0.05, 0], c + [x - 0.03, y + 0.05, 0]], WHITE * 0.8 * b, 1, closed=True)


def sh_codebreak(img, u, t, v, T):
    """Cartes perforées et grille d'analyse qui défilent autour du manuscrit."""
    sc = Scene()
    flat_page(sc, [0, 0, 0], 2.4, 3.2)
    page_text(sc, [0, 0, 0.01], [1, 0, 0], [0, 1, 0], 2.4, 3.2, nlines=12, size=0.12)
    for k in range(6):
        a = 0.4 * t + k * math.pi / 3
        punch_card(sc, [3.6 * math.cos(a), 1.6 * math.sin(a * 0.7 + k) * 0.8, 1.5 * math.sin(a) - 1.0], 2.0, 0.9, seed=k)
    sy = -1.6 + 3.2 * ((t * 0.45) % 1)
    sc.seg([-1.3, sy, 0.05], [1.3, sy, 0.05], WHITE, 2)
    for k in range(9):
        x = -1.2 + 0.3 * k
        sc.seg([x, -1.7, 0.03], [x, 1.7, 0.03], GREEN * 0.25, 1)
    cam = look_at(*orbit([0, 0, 0], lerp(6.8, 5.8, ease(u)), 0.4 * math.sin(0.25 * T) + 0.3 * v, 0.12))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(3, 18))


def sh_codebreak_fail(img, u, t, v, T):
    """Les cartes tombent et s'éteignent ; la page reste intacte."""
    sc = Scene()
    flat_page(sc, [0, 0, 0], 2.4, 3.2)
    page_text(sc, [0, 0, 0.01], [1, 0, 0], [0, 1, 0], 2.4, 3.2, nlines=12, size=0.12)
    f = ease(u)
    for k in range(6):
        a = k * math.pi / 3
        punch_card(sc, [3.6 * math.cos(a), 1.0 - 4.0 * f * f - 0.3 * k * f, 1.5 * math.sin(a) - 1.0], 2.0, 0.9, b=1 - 0.8 * f, seed=k)
    m = 0.4 + 0.6 * abs(math.sin(5 * t)) * (1 - f)
    sc.seg([-1.6, -2.0, 0.05], [1.6, 2.0, 0.05], RED * m, 4)
    sc.seg([1.6, -2.0, 0.05], [-1.6, 2.0, 0.05], RED * m, 4)
    cam = look_at(*orbit([0, 0, 0], lerp(5.4, 6.4, ease(u)), 0.1, 0.1))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 18))


def zipf_scene(sc, u, bars=True):
    sc.seg([-3, -2.5, 0], [3.2, -2.5, 0], GOLD, 2); sc.seg([-3, -2.5, 0], [-3, 3.2, 0], GOLD, 2)
    n = 20
    f = ease(min(1, u * 1.5))
    for k in range(n):
        h = 5.2 / (k + 1)
        x = -2.7 + k * 0.29
        hh = h * f
        col = WHITE if k < 2 else AMBER
        if bars:
            sc.box([x, -2.5 + hh / 2, 0], [0.22, max(hh, 0.01), 0.22], col * (1.0 if k < 2 else 0.8), 2 if k < 2 else 1)
    xs = np.linspace(0, n - 1, 60)
    curve = [[-2.7 + q * 0.29, -2.5 + 5.2 / (q + 1) * f + 0.15, 0.2] for q in xs]
    sc.add(curve, GREEN, 2)


def sh_zipf(img, u, t, v, T):
    sc = Scene(); zipf_scene(sc, (u + v) / 2 if v else u)
    page_text(sc, [0.5, 1.6, -1.5], [1, 0, 0], [0, 1, 0], 3.6, 2.0, nlines=6, size=0.12, col=INK * 0.5)
    cam = look_at(*orbit([-0.6, 0.4, 0], lerp(8.0, 7.2, ease(u)), -0.35 + 0.4 * u + 0.3 * v, 0.15))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 18))


def sh_zipf_bars(img, u, t, v, T):
    """Gros plan sur les deux premières barres : rapport 2 pour 1."""
    sc = Scene(); zipf_scene(sc, 1.0)
    p = 0.5 + 0.5 * math.sin(4 * t)
    sc.seg([-2.95, 2.7, 0.15], [-2.25, 2.7, 0.15], WHITE * (0.6 + 0.4 * p), 2)
    sc.seg([-2.65, 0.1, 0.15], [-2.25, 0.1, 0.15], WHITE * (0.6 + 0.4 * p), 2)
    cam = look_at(*orbit([-2.2, 0.4, 0], lerp(6.0, 5.0, ease(u)), 0.35 - 0.2 * u, 0.15))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 14))


def sh_final_book(img, u, t, v, T):
    """Le livre flotte, des glyphes s'en échappent en spirale."""
    sc = Scene()
    book(sc, [0, 0, 0], 0.9)
    for k in range(40):
        g = RND[k]
        a = 0.6 * t + k * 0.5; r = 1.0 + 0.08 * k
        y = 0.3 + (0.12 * k + 0.4 * t) % 5
        o = np.array([r * math.cos(a), y, r * math.sin(a)])
        ex = np.array([-math.sin(a), 0, math.cos(a)])
        for stroke in GLYPHS[k % len(GLYPHS)]:
            sc.add([o + ex * px * 0.25 + np.array([0, 1, 0]) * py * 0.25 for px, py in stroke], INK * max(0.2, 1 - y / 5), 1)
    cam = look_at(*orbit([0, 1.2, 0], lerp(5.0, 6.0, ease(u)), 0.3 * T, 0.45))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(3, 18))


def sh_final_close(img, u, t, v, T):
    """Retour à l'accroche : le livre se referme, la caméra recule dans le noir."""
    sc = Scene()
    oa = 1.0 - ease(min(1, u * 1.3))
    book(sc, [0, 0, 0], max(0.02, oa), b=lerp(1.0, 0.7, u)[()])
    cam = look_at(*orbit([0, 0.4, 0], lerp(3.6, 6.0, ease(u)), 0.35 * math.sin(0.3 * T), lerp(1.15, 0.6, u)))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(2, 16))
