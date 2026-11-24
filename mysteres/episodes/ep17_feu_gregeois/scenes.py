# Plans propres à l'épisode 17 : le feu grégeois
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE, COPPER...)

FIRE = np.array([0.18, 0.50, 1.00])     # BGR : orange vif
RED = np.array([0.15, 0.22, 1.00])
YEL = np.array([0.45, 0.90, 1.00])
SEA = np.array([0.95, 0.62, 0.25])      # bleu mer
SMOKE = np.array([0.55, 0.55, 0.58])
SAND = np.array([0.45, 0.75, 0.90])
R17 = np.random.default_rng(17)
FR = R17.uniform(0, 1, (400, 6))


def sea(sc, t, size=8.0, n=22, amp=0.08, col=SEA * 0.35, cx=0.0, cz=0.0):
    xs = np.linspace(-size, size, 40)
    for i in range(n + 1):
        z = cz - size + 2 * size * i / n
        y = amp * np.sin(xs * 0.9 + t * 1.3 + z * 0.7)
        sc.add(np.stack([cx + xs, y, np.full_like(xs, z)], 1), col, 1)


def flame(sc, base, h, t, k=0, b=1.0, w=2, nt=5):
    """Flamme : faisceau de langues qui ondulent."""
    base = np.asarray(base, float)
    for j in range(nt):
        r = FR[(k * 7 + j) % len(FR)]
        ph = r[0] * 6.28; hh = h * (0.55 + 0.45 * r[1]) * (0.85 + 0.15 * math.sin(t * 7 + ph))
        off = (r[2] - 0.5) * h * 0.5
        ys = np.linspace(0, 1, 9)
        x = off * (1 - ys) + 0.12 * h * np.sin(ys * 5 + t * 8 + ph) * ys
        z = (r[3] - 0.5) * h * 0.3 * (1 - ys)
        P = np.stack([base[0] + x, base[1] + ys * hh, base[2] + z], 1)
        col = YEL if j == 0 else (FIRE if j % 2 else RED)
        sc.add(P, col * b, w)


def ship(sc, c, L=3.0, col=GOLD, b=1.0, heading=0.0, mast=True, oars=True):
    """Galère (dromon) vue en fil de fer : coque, mât, rames. Proue vers +x local."""
    c = np.asarray(c, float); ch, sh = math.cos(heading), math.sin(heading)
    R = lambda p: c + np.array([p[0] * ch - p[2] * sh, p[1], p[0] * sh + p[2] * ch])
    hw = L * 0.13
    xs = np.linspace(-L / 2, L / 2, 14)
    prof = np.sqrt(np.clip(1 - (xs / (L / 2)) ** 2, 0, 1)) ** 0.6
    for side in (-1, 1):
        sc.add([R((x, 0.06 * L + 0.5 * (x / L) ** 2 * L * 0.5, side * hw * p)) for x, p in zip(xs, prof)], col * b, 2)
        sc.add([R((x, -0.06 * L, side * hw * p * 0.55)) for x, p in zip(xs, prof)], col * 0.6 * b, 1)
    sc.add([R((x, -0.09 * L + 0.4 * (x / L) ** 2 * L * 0.4, 0)) for x in xs], col * 0.8 * b, 2)
    sc.seg(R((-L / 2, 0.03 * L, 0)), R((L / 2, 0.03 * L, 0)), col * 0.5 * b, 1)
    for x, p in zip(xs[2:-2:2], prof[2:-2:2]):
        for side in (-1, 1):
            sc.add([R((x, 0.06 * L, side * hw * p)), R((x, -0.06 * L, side * hw * p * 0.55)), R((x, -0.09 * L, 0))], col * 0.45 * b, 1)
            if oars:
                sc.seg(R((x, 0.05 * L, side * hw * p)), R((x - 0.05 * L, -0.06 * L, side * (hw * p + 0.3 * L))), AMBER * 0.7 * b, 1)
    if mast:
        sc.seg(R((0, 0.03 * L, 0)), R((0, 0.55 * L, 0)), col * b, 2)
        sc.add([R((0, 0.5 * L, -0.25 * L)), R((0, 0.5 * L, 0.25 * L)), R((0.05 * L, 0.2 * L, 0.22 * L)), R((0.05 * L, 0.2 * L, -0.22 * L))], WHITE * 0.5 * b, 1, closed=True)
    return R


def dome(sc, c, r, col=GOLD, b=1.0, n=7):
    c = np.asarray(c, float)
    for k in range(n):
        a = k * math.pi / n
        th = np.linspace(0, math.pi, 12)
        sc.add(np.stack([c[0] + r * np.cos(th) * math.cos(a), c[1] + r * np.sin(th), c[2] + r * np.cos(th) * math.sin(a)], 1), col * b, 1)
    sc.circle(c, r, col * b, 2)
    sc.circle(c + [0, r * 0.7, 0], r * 0.71, col * 0.5 * b, 1)


def amphora(sc, c, s=1.0, col=COPPER, b=1.0, fill=0.0, t=0.0):
    c = np.asarray(c, float)
    prof = [(0.0, -1.0), (0.18, -0.9), (0.5, -0.3), (0.55, 0.1), (0.42, 0.45), (0.18, 0.65), (0.14, 0.95), (0.2, 1.0)]
    for k in range(10):
        a = k * math.pi * 2 / 10
        sc.add([c + s * np.array([r * math.cos(a), y, r * math.sin(a)]) for r, y in prof], col * b, 1)
    for r, y in prof[1:]:
        sc.circle(c + [0, s * y, 0], s * r, col * 0.7 * b, 1, n=28)
    for sd in (-1, 1):
        sc.add([c + s * np.array([sd * 0.15, 0.8, 0]), c + s * np.array([sd * 0.45, 0.85, 0]), c + s * np.array([sd * 0.48, 0.4, 0])], col * b, 2)
    if fill > 0:  # liquide qui luit
        lv = -0.9 + 1.2 * fill
        rr = np.interp(lv, [p[1] for p in prof], [p[0] for p in prof])
        sc.circle(c + [0, s * lv, 0], s * rr * 0.97, FIRE * b, 2, n=32)
        for k in range(6):
            y = -0.85 + (lv + 0.85) * k / 6
            rr2 = np.interp(y, [p[1] for p in prof], [p[0] for p in prof]) * 0.9
            sc.circle(c + [0, s * y, 0], s * rr2, FIRE * 0.35 * b, 1, n=24)


# ------------------------------------------------------------------ plans
def sh_hook_fire(img, u, t, v, T):
    """La mer en feu : des flammes qui brûlent sur l'eau autour d'une galère."""
    sc = Scene(); sea(sc, T)
    ship(sc, [0, 0.05, 0], 4.0, GOLD, 1.0, heading=0.4)
    nf = int(6 + 22 * ease(min(1, u * 1.4)))
    for k in range(nf):
        r = FR[k]
        a = r[4] * 6.28; d = 1.2 + 3.0 * r[5]
        flame(sc, [d * math.cos(a), 0, d * math.sin(a)], 0.5 + 0.7 * r[1], T, k, 1.0, 2)
    cam = look_at(*orbit([0, 0.7, 0], lerp(8.0, 6.0, ease(u)), 0.6 + 0.25 * u + 0.5 * v, lerp(0.38, 0.28, u)))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 18))


def sh_city(img, u, t, v, T):
    """Constantinople : murailles crénelées, tours, grande coupole, port."""
    sc = Scene(); sea(sc, T, size=12, n=26, cz=6, amp=0.05, col=SEA * 0.25)
    # muraille le long du rivage
    for i in range(-6, 7):
        x = i * 1.0
        sc.box([x, 0.6, 0], [1.0, 1.2, 0.4], GOLD * 0.8, 1)
        sc.box([x - 0.25, 1.32, 0], [0.25, 0.24, 0.4], GOLD * 0.6, 1)
        if i % 3 == 0:
            sc.box([x, 0.9, 0], [0.7, 1.8, 0.7], GOLD, 2)
    # ville derrière
    for k in range(40):
        r = FR[100 + k]
        sc.box([-6 + 12 * r[0], 0.4 + r[1] * 0.5, -1.5 - 5 * r[2]], [0.6, 0.8 + r[1], 0.6], AMBER * 0.5, 1)
    sc.box([0, 1.2, -3.5], [3.0, 2.4, 3.0], GOLD, 2)
    dome(sc, [0, 2.4, -3.5], 1.4, WHITE * 0.9)
    for sx in (-1.8, 1.8):
        sc.seg([sx, 0, -1.8], [sx, 3.8, -1.8], GOLD * 0.8, 2)
    if v % 2 == 0:
        cam = look_at(*orbit([0, 1.6, -2], lerp(12, 9.5, ease(u)), 0.15 + 0.35 * u, 0.3))
    else:
        cam = look_at(*orbit([0, 2.0, -3.5], lerp(8, 6.5, ease(u)), -0.4 + 0.4 * u, 0.25))
    stars(img, cam, T, 0.6); draw(img, sc, cam, fade=(3, 30))


def sh_amphora(img, u, t, v, T):
    """Une amphore dont le liquide s'allume : le feu liquide."""
    sc = Scene()
    amphora(sc, [0, 0, 0], 1.3, COPPER, 1.0, fill=ease(min(1, u * 1.5)) if v == 0 else 1.0, t=T)
    if v == 1 or u > 0.6:
        flame(sc, [0, 1.35, 0], 0.9 * (ease((u - 0.6) / 0.3) if v == 0 else 1.0) + 0.01, T, 3, 1.0, 2, 6)
    for k in range(4):
        sc.circle([0, -1.3, 0], 1.0 + 0.5 * k, GOLD * (0.35 - 0.07 * k), 1)
    cam = look_at(*orbit([0, 0.2, 0], lerp(5.2, 4.4, ease(u)), 0.6 * T * 0.3 + v, 0.2))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 12))


def sh_sea_fire(img, u, t, v, T):
    """Une nappe de feu qui s'étale sur la mer."""
    sc = Scene(); sea(sc, T, size=7, amp=0.06)
    rad = lerp(0.6, 4.0, ease(u))[()]
    for k in range(60):
        r = FR[k + 30]
        a = r[0] * 6.28; d = rad * math.sqrt(r[1])
        flame(sc, [d * math.cos(a), 0, d * math.sin(a)], 0.25 + 0.35 * r[2], T, k + 30, 1.0, 1 + (k % 3 == 0), 3)
    th = np.linspace(0, 6.28, 50)
    sc.add(np.stack([rad * np.cos(th) * (1 + 0.08 * np.sin(5 * th + T)), np.full(50, 0.02), rad * np.sin(th)], 1), FIRE, 2, closed=True)
    cam = look_at(*orbit([0, 0, 0], lerp(10, 8.5, u), 0.3 * T * 0.2 + v * 1.3, lerp(0.75, 0.6, u)))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(3, 18))


def sh_siphon(img, u, t, v, T):
    """Dromon : tube de bronze à la proue qui projette un jet de feu, fumée."""
    sc = Scene(); sea(sc, T, size=9, amp=0.05)
    R = ship(sc, [0, 0.05, 0], 4.0, GOLD, 1.0, heading=0.0)
    tip = R((2.0, 0.35, 0)); end = R((2.6, 0.45, 0))
    for k in range(8):  # tube
        a = k * math.pi / 4
        o = np.array([0, 0.07 * math.cos(a), 0.07 * math.sin(a)])
        sc.seg(tip + o * 1.4, end + o, COPPER, 2)
    sc.circle(end, 0.07, COPPER, 2, n=16, axis="x")
    # jet en arc
    L = 5.0 * ease(min(1, u * 2.0 + 0.2))
    for k in range(70):
        q = (k / 70 + t * 0.9) % 1.0
        if q * 5 > L: continue
        x = 2.6 + q * 5; y = 0.45 + q * 1.0 - q * q * 1.6
        r = FR[k]; sp = 0.05 + q * 0.5
        p = np.array([x, y + (r[1] - 0.5) * sp, (r[2] - 0.5) * sp])
        sc.seg(p, p + [0.18, 0.02, 0], (YEL if q < 0.3 else FIRE if q < 0.7 else RED), 2 + (q < 0.4))
    for k in range(5):  # fumée
        q = (t * 0.25 + k / 5) % 1
        sc.circle([2.4 - q * 1.2, 0.8 + q * 1.8, 0], 0.15 + q * 0.6, SMOKE * (0.6 * (1 - q)), 1, n=20, axis="x")
    if v == 0:
        cam = look_at(*orbit([2.6, 0.7, 0], lerp(6.5, 5.6, ease(u)), 1.1 + 0.3 * u, 0.22))
    else:
        cam = look_at(*orbit([3.4, 0.7, 0], lerp(4.6, 4.0, ease(u)), 2.2 - 0.3 * u, 0.15))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 18))


def sh_water_fail(img, u, t, v, T):
    """Un seau d'eau versé sur la flamme : la flamme reste."""
    sc = Scene(); sea(sc, T, size=4, n=14, amp=0.04)
    hh = 1.4 * (1 + 0.15 * math.sin(T * 3))
    flame(sc, [0, 0, 0], hh, T, 5, 1.0, 3, 7)
    for k in range(40):  # gouttes qui tombent
        r = FR[k + 200]
        q = (t * 0.9 + r[0]) % 1
        p = np.array([(r[1] - 0.5) * 1.2, 3.5 - q * 3.6, (r[2] - 0.5) * 0.8])
        sc.seg(p, p + [0, 0.22, 0], SEA * 0.9, 2)
    sc.box([0, 3.8, 0], [0.8, 0.4, 0.6], COPPER * 0.8, 1)
    cam = look_at(*orbit([0, 1.4, 0], lerp(6.0, 5.0, ease(u)), 0.4 + 0.3 * u, 0.12))
    stars(img, cam, T, 0.3); draw(img, sc, cam, fade=(2, 12))


def sh_sand(img, u, t, v, T):
    """Tas de sable et deux jarres ; la flamme se réduit."""
    sc = Scene(); sc.grid_plane(5, 16, 0, GOLD * 0.06)
    for k in range(9):  # tas de sable (cône)
        y = k * 0.12; r = 1.3 * (1 - k / 9)
        sc.circle([0, y, 0], r, SAND * (0.9 - 0.05 * k), 1, n=40)
    for k in range(12):
        a = k * math.pi / 6
        sc.seg([1.3 * math.cos(a), 0, 1.3 * math.sin(a)], [0, 1.08, 0], SAND * 0.45, 1)
    amphora(sc, [-2.3, 0.9, 0.3], 0.9, COPPER, 0.9)
    amphora(sc, [2.3, 0.75, 0.3], 0.75, GOLD, 0.8)
    hf = 0.9 * (1 - ease(u)) + 0.05
    flame(sc, [0, 1.1, 0], hf, T, 9, 1.0, 2, 5)
    cam = look_at(*orbit([0, 0.9, 0], lerp(8.0, 6.8, ease(u)), -0.3 + 0.4 * u, 0.32))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 16))


def _fleet(sc, T, burn, enemies=9):
    sea(sc, T, size=14, n=26, amp=0.06, col=SEA * 0.28)
    for k in range(enemies):
        r = FR[300 + k]
        x = -6 + 12 * (k + 0.5) / enemies; z = -4 - 4 * r[0]
        ship(sc, [x, 0.05, z], 2.4, AMBER * 0.9, 0.9, heading=math.pi / 2 + (r[1] - 0.5) * 0.4, oars=False)
        if burn > r[2] * 0.8:
            for j in range(3):
                flame(sc, [x + (j - 1) * 0.4, 0.2, z], 0.6 + 0.4 * r[3], T, k * 3 + j, 1.0, 2, 4)
    for k in range(3):  # dromons byzantins
        x = -4 + 4 * k
        R = ship(sc, [x, 0.05, 1.5], 3.0, GOLD, 1.0, heading=-math.pi / 2, oars=True)


def sh_fleet(img, u, t, v, T):
    sc = Scene(); _fleet(sc, T, 0.15 if v == 0 else 0.0, 9 if v == 0 else 12)
    cam = look_at(*orbit([0, 0.5, -2.0], lerp(12, 10, ease(u)), 0.15 + 0.3 * u + 0.5 * v, 0.3))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 30))


def sh_fleet_burn(img, u, t, v, T):
    sc = Scene(); _fleet(sc, T, 0.3 + ease(u), 12)
    for k in range(30):  # flammèches sur l'eau entre les navires
        r = FR[350 + k % 50]
        flame(sc, [-7 + 14 * r[0], 0, -2 - 6 * r[1]], 0.3 + 0.3 * r[2], T, 350 + k, 0.8, 1, 3)
    cam = look_at(*orbit([0, 0.6, -5.5], lerp(8, 6.8, ease(u)), -0.3 + 0.4 * u, 0.25))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(3, 24))


def sh_secret(img, u, t, v, T):
    """Le système découpé en éléments séparés : réservoir, brasier, pompe, tube. Un seul allumé à la fois."""
    sc = Scene()
    act = int(T * 1.2) % 4
    sp = lerp(0.0, 1.0, ease(min(1, u * 2)))[()]
    parts = [(-0.9 - 0.4 * sp, 1.2 + 0.4 * sp, 0), (0.9 + 0.4 * sp, 1.2 + 0.4 * sp, 1), (-0.9 - 0.4 * sp, -1.4 - 0.4 * sp, 2), (0.9 + 0.4 * sp, -1.4 - 0.4 * sp, 3)]
    for x, yo, k in parts:
        sc0 = sc; sc = Scene()
        b = 1.0 if k == act else 0.3
        col = (GOLD, FIRE, COPPER, WHITE)[k]
        if k == 0:  # réservoir
            sc.box([x, 0, 0], [0.9, 1.4, 0.9], col * b, 2, grid=3)
        elif k == 1:  # brasier
            sc.box([x, -0.4, 0], [0.8, 0.5, 0.8], col * b, 2)
            if k == act: flame(sc, [x, -0.15, 0], 0.7, T, 40, 1.0, 2, 5)
        elif k == 2:  # pompe
            sc.circle([x, -0.6, 0], 0.4, col * b, 2, n=24)
            sc.circle([x, 0.6, 0], 0.4, col * b, 2, n=24)
            for a in range(8):
                aa = a * math.pi / 4
                sc.seg([x + 0.4 * math.cos(aa), -0.6, 0.4 * math.sin(aa)], [x + 0.4 * math.cos(aa), 0.6, 0.4 * math.sin(aa)], col * 0.6 * b, 1)
            sc.seg([x, 0.6, 0], [x, 1.2 + 0.2 * math.sin(T * 4), 0], col * b, 2)
        else:  # tube
            for a in range(6):
                aa = a * math.pi / 3
                sc.seg([x - 0.6, 0.12 * math.cos(aa), 0.12 * math.sin(aa)], [x + 0.6, 0.08 * math.cos(aa), 0.08 * math.sin(aa)], col * b, 2)
        # cadenas sous chaque pièce
        sc.box([x, -1.2, 0], [0.35, 0.28, 0.12], AMBER * b, 1)
        sc.add([[x - 0.12, -1.06, 0], [x - 0.12, -0.92, 0], [x + 0.12, -0.92, 0], [x + 0.12, -1.06, 0]], AMBER * b, 1)
        S_, C_, W_ = sc.arrays(); sc = sc0
        if len(S_): sc.segs.append(S_ + [0, yo, 0]); sc.cols.append(C_); sc.wid.append(W_)
    cam = look_at(*orbit([0, 0, 0], lerp(9.0, 8.0, ease(u)), 0.35 * math.sin(0.4 * T), 0.15))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 16))


def _codex(sc, c, b=1.0, lines=1.0):
    c = np.asarray(c, float)
    for sd in (-1, 1):
        ex = np.array([sd * 1.0, 0.0, 0.0]); ang = 0.15
        P = [c + [sd * x, abs(x) * ang, z] for x, z in ((0, -1.4), (2.0, -1.4), (2.0, 1.4), (0, 1.4))]
        sc.add(P, WHITE * 0.8 * b, 2, closed=True)
        nl = int(14 * lines)
        for k in range(nl):
            z = -1.2 + k * 0.18
            ln = 1.6 * (0.6 + 0.4 * FR[k + sd * 20 + 40][0])
            sc.seg(c + [sd * 0.2, 0.2 * ang * 0.5 + 0.03, z], c + [sd * (0.2 + ln), (0.2 + ln) * ang + 0.03, z], GOLD * 0.7 * b, 1)
    sc.seg(c + [0, 0, -1.4], c + [0, 0, 1.4], AMBER * b, 2)


def sh_codex(img, u, t, v, T):
    """Livre impérial ouvert, couronne au-dessus, sceau."""
    sc = Scene()
    _codex(sc, [0, 0, 0], 1.0, ease(min(1, 0.2 + u * 1.3)))
    # couronne stylisée
    cy = 1.8 + 0.08 * math.sin(T * 1.5)
    sc.circle([0, cy, 0], 0.55, GOLD, 2, n=40)
    sc.circle([0, cy + 0.3, 0], 0.55, GOLD * 0.7, 1, n=40)
    for k in range(8):
        a = k * math.pi / 4
        sc.seg([0.55 * math.cos(a), cy, 0.55 * math.sin(a)], [0.55 * math.cos(a), cy + 0.5, 0.55 * math.sin(a)], GOLD, 1)
    sc.seg([0, cy + 0.3, 0], [0, cy + 0.9, 0], WHITE, 2); sc.seg([-0.18, cy + 0.72, 0], [0.18, cy + 0.72, 0], WHITE, 2)
    sc.circle([1.3, 0.25, 0.9], 0.25, RED, 2, n=24)
    cam = look_at(*orbit([0, 0.8, 0], lerp(6.5, 5.5, ease(u)), 0.2 + 0.3 * u, 0.85))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 14))


def sh_angel(img, u, t, v, T):
    """Rayons de lumière et deux grandes ailes abstraites au-dessus du livre."""
    sc = Scene()
    _codex(sc, [0, 0, 0], 0.7, 1.0)
    top = np.array([0, 4.5, 0])
    for k in range(18):  # rayons
        a = k * math.pi * 2 / 18 + T * 0.1
        q = ease(min(1, u * 2))
        sc.seg(top, [1.8 * math.cos(a) * q, 0.1, 1.2 * math.sin(a) * q], WHITE * 0.35, 1)
    op = ease(min(1, u * 1.5))
    for sd in (-1, 1):  # ailes : plumes en éventail
        for k in range(11):
            a = 0.15 + k * 0.12 * op
            Lk = 2.6 - 0.12 * k
            base = top + [sd * 0.2, 0, 0]
            P = [base + [sd * Lk * q * math.cos(a), Lk * q * math.sin(a) * 0.6 - k * 0.12 * q, 0] for q in np.linspace(0, 1, 8)]
            sc.add(P, (GOLD if k % 2 else WHITE) * (0.9 - 0.04 * k), 2 if k < 4 else 1)
    sc.circle(top + [0, 0.6, 0], 0.4, WHITE, 2, n=36, axis="z")
    cam = look_at(*orbit([0, 2.6, 0], lerp(10, 8.5, ease(u)), 0.15 * math.sin(0.5 * T), 0.12))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(3, 18))


def sh_ingredients(img, u, t, v, T):
    """Goutte de pétrole et pin résineux, points d'interrogation entre eux."""
    sc = Scene()
    # goutte
    c = np.array([-1.3, 0.2, 0])
    for k in range(10):
        a = k * math.pi / 10
        P = []
        for th in np.linspace(0, 2 * math.pi, 30):
            r = 0.6 * (1 - math.sin(th)) ** 0.9 * 0.55 + 0.05
            y = 0.9 * math.sin(th) * -0.8
            P.append(c + [r * math.cos(th) * math.cos(a) * 1.2, -math.cos(th + math.pi / 2) * 0.9 + 0.0, r * math.cos(th) * math.sin(a) * 1.2])
        sc.add(P, AMBER * 0.9, 1)
    sc.circle(c + [0, -0.4, 0], 0.62, AMBER, 2, n=32)
    # pin
    p = np.array([1.4, -1.2, 0])
    sc.seg(p, p + [0, 3.0, 0], COPPER, 3)
    for k in range(6):
        y = 0.6 + k * 0.4; r = 1.1 * (1 - k / 7)
        sc.circle(p + [0, y, 0], r, GOLD * 0.8, 1, n=24)
        for j in range(8):
            a = j * math.pi / 4 + k * 0.3
            sc.seg(p + [0, y + 0.4, 0], p + [r * math.cos(a), y, r * math.sin(a)], GOLD * 0.5, 1)
    # gouttes de résine
    for k in range(3):
        q = (t * 0.4 + k / 3) % 1
        sc.circle(p + [0.12, 1.4 - q * 1.5, 0.1], 0.06, YEL, 2, n=10)
    # point d'interrogation
    qc = np.array([0.05, 1.8, 0])
    th = np.linspace(math.pi, -0.6, 16)
    sc.add([qc + [0.3 * math.cos(a), 0.3 * math.sin(a), 0] for a in th] + [qc + [0, -0.45, 0]], WHITE, 3)
    sc.circle(qc + [0, -0.7, 0], 0.05, WHITE, 3, n=10, axis="z")
    cam = look_at(*orbit([0, 0.4, 0], lerp(7.5, 6.6, ease(u)), 0.3 * math.sin(0.5 * T), 0.15))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(3, 14))


def sh_lost(img, u, t, v, T):
    """Le parchemin de la recette se défait en poussière."""
    sc = Scene()
    q = ease(u)
    for k in range(14):
        r = FR[k + 60]
        z = -1.3 + k * 0.2
        ln = 2.4 * (0.6 + 0.4 * r[0])
        lift = max(0.0, q * 1.6 - r[1] * 0.6) * 2.0
        off = np.array([(r[2] - 0.5) * lift, lift, (r[3] - 0.5) * lift])
        b = max(0.0, 1 - lift / 2.5)
        sc.seg(np.array([-1.2, 0.02, z]) + off, np.array([-1.2 + ln, 0.02, z]) + off, GOLD * b, 1)
    fr = max(0.0, 1 - q * 0.8)
    sc.add([[-1.5, 0, -1.5], [1.5, 0, -1.5], [1.5, 0, 1.5], [-1.5, 0, 1.5]], WHITE * 0.7 * fr, 2, closed=True)
    for sd in (-1, 1):
        sc.circle([0, 0.15, sd * 1.6], 0.15, WHITE * 0.6 * fr, 2, n=16, axis="x")
    for k in range(120):  # poussière
        r = FR[k + 150]
        h = (q * 3.5 * r[0] + t * 0.1) % 4
        if r[1] < q:
            p = np.array([(r[2] - 0.5) * 3 + 0.3 * h, h, (r[3] - 0.5) * 3])
            sc.seg(p, p + [0.03, 0.03, 0], GOLD * (1 - h / 4), 2)
    cam = look_at(*orbit([0, 0.8, 0], lerp(6.8, 6.0, ease(u)), 0.2 + 0.2 * u, 0.7))
    stars(img, cam, T, 0.5); draw(img, sc, cam, fade=(2, 14))


def sh_final(img, u, t, v, T):
    """Une seule flamme sur la mer noire, la caméra s'éloigne."""
    sc = Scene(); sea(sc, T, size=12, n=28, amp=0.07, col=SEA * 0.3)
    flame(sc, [0, 0, 0], 1.9, T, 2, 1.0, 3, 7)
    for k in range(3):
        rr = 0.5 + ((t * 0.5 + k / 3) % 1) * 3
        sc.circle([0, 0.03, 0], rr, FIRE * 0.6 * (1 - rr / 3.5), 1, n=48)
    cam = look_at(*orbit([0, 0.8, 0], lerp(5.0, 11.0, ease(u)), 0.5 + 0.3 * u, lerp(0.2, 0.45, u)))
    stars(img, cam, T, 0.8); draw(img, sc, cam, fade=(3, 24))
