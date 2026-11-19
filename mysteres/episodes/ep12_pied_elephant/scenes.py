# Plans propres à l'épisode 12 : le « pied d'éléphant » de Tchernobyl
# (exécuté dans l'espace du moteur : Scene, look_at, orbit, draw, stars, ease, lerp, GOLD, AMBER, WHITE...)

LAVA = np.array([0.18, 0.40, 1.00])     # BGR : orange lave
HOT = np.array([0.55, 0.85, 1.00])
RAD = np.array([0.45, 1.00, 0.55])      # vert radiation
STEEL = np.array([0.95, 0.80, 0.60])
SAND = np.array([0.45, 0.80, 0.95])
URAN = np.array([0.30, 1.00, 0.40])
R12 = np.random.default_rng(12)
DUST = R12.uniform(-1, 1, (160, 3))
NEUT = R12.normal(0, 1, (220, 3))
EMB = R12.uniform(-1, 1, (60, 3))


def fv(x):
    return float(np.asarray(x))


def foot(sc, c=(0, 0, 0), s=1.0, col=LAVA, t=0.0, cracks=0.0, glow=1.0):
    """Coulée figée, ridée, en forme de patte : anneaux irréguliers empilés + plis verticaux."""
    c = np.asarray(c, float)
    th = np.linspace(0, 2 * math.pi, 49)
    nl = 14
    rings = []
    for k in range(nl):
        f = k / (nl - 1)
        y = 1.25 * s * f
        r = s * (0.95 - 0.38 * f + 0.22 * math.exp(-((f - 0.05) / 0.12) ** 2))
        wob = 1 + 0.10 * np.sin(5 * th + 1.7 * k) + 0.06 * np.sin(11 * th - k)
        P = np.stack([c[0] + r * wob * np.cos(th), np.full_like(th, c[1] + y), c[2] + r * wob * np.sin(th) * 0.85], 1)
        rings.append(P)
        b = 0.45 + 0.55 * (1 - f)
        sc.add(P, col * b * glow, 2 if k % 3 == 0 else 1)
    R = np.stack(rings)
    for j in range(0, 48, 3):
        sc.add(R[:, j], col * 0.6 * glow, 1)
    # dessus bombé
    top = R[-1]
    for j in range(0, 48, 8):
        sc.seg(top[j], top[(j + 24) % 48], col * 0.4 * glow, 1)
    # fissures
    if cracks > 0:
        for j in range(0, 48, 6):
            n = int(2 + 10 * cracks)
            pts = R[:n, j] * 1.0 + np.array([0.02, 0, 0.02])
            sc.add(pts, WHITE * 0.9, 2)
    return R


def waves(sc, c, t, col=RAD, n=4, rmax=2.4, axis="y"):
    for k in range(n):
        f = ((t * 0.5 + k / n) % 1.0)
        sc.circle(c, 0.4 + rmax * f, col * (1 - f) * 0.9, 1, 64, axis=axis)


def reactor(sc, c=(0, 0, 0), s=1.0, lid=0.0, col=GOLD):
    """Bâtiment (coupe) + cœur cylindrique + dalle supérieure (qui peut se soulever)."""
    c = np.asarray(c, float)
    sc.box(c + [0, 1.2 * s, 0], [3.2 * s, 2.4 * s, 2.4 * s], col * 0.45, 1)
    # cœur
    for k in range(7):
        y = 0.6 * s + 0.12 * s * k
        sc.circle(c + [0, y, 0], 0.75 * s, AMBER * 0.9, 2 if k in (0, 6) else 1, 40)
    for k in range(16):
        a = 2 * math.pi * k / 16
        p = c + [0.75 * s * math.cos(a), 0, 0.75 * s * math.sin(a)]
        sc.seg(p + [0, 0.6 * s, 0], p + [0, 1.32 * s, 0], AMBER * 0.6, 1)
    # dalle
    yl = 1.42 * s + 1.6 * s * lid
    tilt = 0.9 * lid
    th = np.linspace(0, 2 * math.pi, 41)
    P = np.stack([0.85 * s * np.cos(th), 0.85 * s * np.sin(th) * math.sin(tilt), 0.85 * s * np.sin(th) * math.cos(tilt)], 1)
    sc.add(c + [0, yl, 0] + P, WHITE * 0.9, 2)
    sc.add(c + [0, yl + 0.1 * s, 0] + P, WHITE * 0.5, 1)
    # niveaux inférieurs
    for y in (0.0, -0.8 * s, -1.6 * s):
        sc.add([c + [-1.6 * s, y, -1.2 * s], c + [1.6 * s, y, -1.2 * s], c + [1.6 * s, y, 1.2 * s], c + [-1.6 * s, y, 1.2 * s]], col * 0.35, 1, closed=True)


def corridor(sc, z0=0.0, n=12, col=GOLD):
    for k in range(n):
        z = z0 - k * 0.9
        sc.add([[-0.8, -0.8, z], [0.8, -0.8, z], [0.8, 0.9, z], [-0.8, 0.9, z]], col * (0.7 - 0.04 * k), 1, closed=True)
    for x, y in ((-0.8, -0.8), (0.8, -0.8), (0.8, 0.9), (-0.8, 0.9)):
        sc.seg([x, y, z0], [x, y, z0 - (n - 1) * 0.9], col * 0.5, 1)
    # câbles le long du mur
    for k in range(3):
        sc.seg([-0.75, 0.6 - 0.12 * k, z0], [-0.75, 0.6 - 0.12 * k, z0 - (n - 1) * 0.9], COPPER * 0.6, 1)


def ptext(img, txt, org, sc_, col, th=2):
    tmp = np.zeros(img.shape, np.uint8)
    cv2.putText(tmp, txt, org, cv2.FONT_HERSHEY_SIMPLEX, sc_, (np.clip(np.asarray(col), 0, 1) * 255).tolist(), th, cv2.LINE_AA)
    np.add(img, tmp.astype(np.float32) / 255, out=img)


def label3d(img, cam, p, txt, col=WHITE, sc_=1.2):
    eye, M = cam
    q = (np.asarray(p, float) - eye) @ M.T
    if q[2] <= 0.1: return
    f = (W / 2) / math.tan(0.4)
    x, y = int(W / 2 + f * q[0] / q[2]), int(H / 2 - f * q[1] / q[2])
    ptext(img, txt, (x - int(12 * sc_ * len(txt)), y), sc_, col)


# ------------------------------------------------------------------ plans
def sh_hook_reactor(img, u, t, v, T):
    """Le réacteur en coupe ; une lueur sous le plancher."""
    sc = Scene(); reactor(sc, [0, 0, 0], 1.0)
    foot(sc, [0.6, -1.6, 0.3], 0.42, LAVA, t)
    waves(sc, [0.6, -1.4, 0.3], t, RAD, 3, 1.2)
    cam = look_at(*orbit([0, 0.0, 0], lerp(7.2, 6.0, ease(u)), 0.6 + 0.35 * u, 0.25))
    draw(img, sc, cam, fade=(3, 14))


def sh_hook_foot(img, u, t, v, T):
    sc = Scene(); foot(sc, [0, 0, 0], 1.0, LAVA, t)
    waves(sc, [0, 0.2, 0], t, RAD, 4, 2.4)
    sc.grid_plane(2.6, 10, 0, GOLD * 0.2)
    cam = look_at(*orbit([0, 0.6, 0], lerp(4.6, 3.8, ease(u)), 0.4 * u - 0.3, 0.35))
    draw(img, sc, cam, fade=(2, 10))


def sh_explosion(img, u, t, v, T):
    sc = Scene()
    a = ease(min(u * 1.8, 1))
    reactor(sc, [0, 0, 0], 1.0, lid=a)
    for k in range(40):
        d = NEUT[k] / (np.linalg.norm(NEUT[k]) + 1e-6)
        d[1] = abs(d[1]) + 0.3
        p0 = np.array([0, 1.5, 0]); p1 = p0 + d * (0.3 + 2.8 * a)
        sc.seg(p0 + d * 2.2 * a, p1, HOT * (1 - 0.6 * a), 2)
    cam = look_at(*orbit([0, 0.8, 0], 7.0, 0.9 - 0.3 * u, 0.25 + 0.1 * u))
    draw(img, sc, cam, fade=(3, 14))


def sh_meltdown(img, u, t, v, T):
    sc = Scene(); reactor(sc, [0, 0, 0], 1.0, lid=1.0)
    a = ease(u)
    for k in range(9):
        x = -0.6 + 0.15 * k; z = 0.2 * math.sin(k * 1.3)
        y1 = lerp(0.6, -1.6 + 0.2 * math.sin(k), a)
        ys = np.linspace(0.6, fv(y1), 12)
        P = np.stack([x + 0.05 * np.sin(ys * 7 + k), ys, np.full_like(ys, z)], 1)
        sc.add(P, LAVA, 3)
    if a > 0.6:
        foot(sc, [0.6, -1.6, 0.3], 0.42 * (a - 0.6) / 0.4 + 0.01, LAVA, t)
    cam = look_at(*orbit([0, -0.3, 0], 6.4, 0.3 + 0.3 * u, 0.15))
    draw(img, sc, cam, fade=(3, 14))


def sh_corridor_217(img, u, t, v, T):
    sc = Scene(); corridor(sc, 0.0, 12)
    zf = -9.5
    foot(sc, [0.1, -0.8, zf], 0.55, LAVA, t)
    waves(sc, [0.1, -0.2, zf + 0.5], t, RAD, 4, 1.6, axis="z")
    z = lerp(3.0, -1.0, ease(u)) if v == 0 else lerp(-1.0, -5.0, ease(u))
    cam = look_at([0.1 * math.sin(t) + [0, 0.4][v % 2], 0.2 - 0.25 * (v % 2), fv(z)], [0, -0.1, fv(z) - 5], 0.05 * (v % 2))
    draw(img, sc, cam, fade=(1, 12))
    # dosimètre
    val = int(50 + 9950 * ease((u + v) / 2) ** 3)
    ptext(img, f"{val:>5} R/H", (W // 2 - 190, int(H * 0.73)), 2.0, RAD * 0.9, 3)


def sh_foot_reveal(img, u, t, v, T):
    sc = Scene(); foot(sc, [0, 0, 0], 1.0, LAVA, t)
    sc.grid_plane(2.4, 8, 0, GOLD * 0.18)
    # murs du coin
    sc.add([[-2.2, 0, -1.4], [2.2, 0, -1.4], [2.2, 2.6, -1.4], [-2.2, 2.6, -1.4]], GOLD * 0.3, 1, closed=True)
    sc.add([[-2.2, 0, -1.4], [-2.2, 0, 2.2], [-2.2, 2.6, 2.2], [-2.2, 2.6, -1.4]], GOLD * 0.3, 1, closed=True)
    az = [0.5, -0.6][v % 2] + 0.5 * u
    cam = look_at(*orbit([0, 0.6, 0], lerp(4.4, 3.4, ease(u)), az, 0.3))
    draw(img, sc, cam, fade=(2, 10))


def sh_dosimeter(img, u, t, v, T):
    sc = Scene(); foot(sc, [0, -0.8, 0], 0.8, LAVA, t)
    waves(sc, [0, -0.3, 0], t * 1.6, RAD, 6, 2.6)
    for k in range(14):
        a = 2 * math.pi * k / 14 + 0.3 * t
        d = np.array([math.cos(a), 0.4, math.sin(a)])
        sc.seg([0, 0, 0] + d * 0.9, d * (1.6 + 0.4 * math.sin(4 * t + k)), RAD * 0.7, 2)
    cam = look_at(*orbit([0, -0.1, 0], 4.2, 0.4 * t, 0.45))
    draw(img, sc, cam, fade=(2, 10))
    # cadran
    cx, cy, r = W // 2, int(H * 0.22), 190
    cv2.ellipse(img, (cx, cy), (r, r), 0, 180, 360, (GOLD * 0.8).tolist(), 3, cv2.LINE_AA)
    for k in range(11):
        a = math.pi + math.pi * k / 10
        cv2.line(img, (int(cx + r * math.cos(a)), int(cy + r * math.sin(a))), (int(cx + 0.85 * r * math.cos(a)), int(cy + 0.85 * r * math.sin(a))), (GOLD * 0.8).tolist(), 2, cv2.LINE_AA)
    a = math.pi + math.pi * min(0.2 + 1.2 * ease(u), 0.99) + 0.03 * math.sin(30 * t)
    cv2.line(img, (cx, cy), (int(cx + 0.9 * r * math.cos(a)), int(cy + 0.9 * r * math.sin(a))), (RAD).tolist(), 4, cv2.LINE_AA)


def sh_composition(img, u, t, v, T):
    """Anneau de composition : sable/béton, acier, uranium (~10 %)."""
    sc = Scene()
    parts = [(0.62, SAND, "SABLE FONDU"), (0.18, GOLD * 0.8, "BETON"), (0.10, STEEL, "ACIER"), (0.10, URAN, "URANIUM")]
    a0 = 0.0; R = 1.1
    rot_ = 0.3 * t
    k_show = ease(u * 1.8)
    labels = []
    for i, (f, col, name) in enumerate(parts):
        a1 = a0 + f * 2 * math.pi * k_show
        th = np.linspace(a0, a1, max(4, int(60 * f)))
        lift = 0.35 if name == "URANIUM" and u > 0.75 else 0.0
        mid = (a0 + a1) / 2
        off = np.array([math.cos(mid + rot_), 0, math.sin(mid + rot_)]) * lift
        for y in (0.0, 0.3):
            for rr in (0.6, R):
                P = np.stack([rr * np.cos(th + rot_), np.full_like(th, y), rr * np.sin(th + rot_)], 1) + off
                sc.add(P, col, 2)
        for a in np.linspace(a0, a1, max(2, int(10 * f))):
            for rr in (0.6, R):
                p = np.array([rr * math.cos(a + rot_), 0, rr * math.sin(a + rot_)]) + off
                sc.seg(p, p + [0, 0.3, 0], col * 0.6, 1)
        labels.append((np.array([1.45 * math.cos(mid + rot_), 0.55, 1.45 * math.sin(mid + rot_)]) + off, name, col))
        a0 = a0 + f * 2 * math.pi * k_show
    cam = look_at(*orbit([0, 0.1, 0], 4.3, 0.2 + 0.5 * v, 0.7))
    draw(img, sc, cam, fade=(2, 10))
    if u > 0.3:
        for p, name, col in labels:
            label3d(img, cam, p, name, col, 1.1)


def sh_drill(img, u, t, v, T):
    sc = Scene(); foot(sc, [0, 0, 0], 0.9, LAVA, t)
    # chariot + foret
    x = fv(lerp(-3.2, -1.05, ease(u * 1.4)))
    sc.box([x - 0.6, 0.25, 0], [0.9, 0.3, 0.6], STEEL, 2)
    for dz in (-0.3, 0.3):
        for dx in (-0.35, 0.35):
            sc.circle([x - 0.6 + dx, 0.08, dz], 0.08, STEEL * 0.8, 1, 16, axis="z")
    sc.box([x - 0.2, 0.55, 0], [0.5, 0.15, 0.15], STEEL, 2)
    spin = 8 * t
    for k in range(10):
        a0 = spin + k * 0.9
        p = np.array([x + 0.05 + 0.04 * k, 0.55 + 0.05 * math.cos(a0), 0.05 * math.sin(a0)])
        q = np.array([x + 0.09 + 0.04 * k, 0.55 + 0.05 * math.cos(a0 + 0.9), 0.05 * math.sin(a0 + 0.9)])
        sc.seg(p, q, WHITE, 2)
    if u > 0.6:
        for k in range(6):
            a = 2 * math.pi * k / 6 + 5 * t
            sc.seg([x + 0.45, 0.55, 0], [x + 0.45 + 0.15 * math.cos(a), 0.55 + 0.15 * math.sin(a), 0], HOT, 1)
    cam = look_at(*orbit([-0.6, 0.5, 0], 4.8, 0.5 + 0.2 * u, 0.25))
    draw(img, sc, cam, fade=(2, 10))


def sh_bullets(img, u, t, v, T):
    sc = Scene(); foot(sc, [0, 0, 0], 0.9, LAVA, t)
    for b in range(3):
        ph = (u * 3 - b * 0.7)
        if ph < 0: continue
        y = 0.4 + 0.25 * b; z = 0.2 * (b - 1)
        if ph < 1:
            x = fv(lerp(-4.0, -0.85, ph))
            sc.seg([x - 0.5, y, z], [x, y, z], WHITE * 0.35, 1)
            sc.circle([x, y, z], 0.04, WHITE, 2, 12, axis="x")
            sc.seg([x, y, z], [x + 0.14, y, z], WHITE, 3)
        else:
            k = min(ph - 1, 1.5)
            for j in range(10):
                d = NEUT[j + 10 * b]; d = d / (np.linalg.norm(d) + 1e-6)
                d[0] = -abs(d[0])
                p = np.array([-0.85, y, z]) + d * 0.9 * k + np.array([0, -0.6 * k * k, 0])
                sc.box(p, [0.06, 0.06, 0.06], LAVA if j % 2 else HOT, 1)
            sc.circle([-0.85, y, z], 0.08 + 0.3 * k, HOT * max(0, 1 - k), 1, 20, axis="x")
    cam = look_at(*orbit([-0.4, 0.5, 0], 3.8, -0.9 + 0.3 * u, 0.2))
    draw(img, sc, cam, fade=(2, 10))


def sh_decay(img, u, t, v, T):
    """Barres : 1986 ≈ 10 000 R/h, 1989 ≈ 1 100 R/h ; l'aiguille de danger reste allumée."""
    sc = Scene()
    a = ease(u * 1.4)
    h86 = 3.0; h89 = fv(lerp(3.0, 0.33, a))
    sc.box([-0.8, h86 / 2, 0], [0.8, h86, 0.8], LAVA, 2, grid=4)
    sc.box([0.8, h89 / 2, 0], [0.8, h89, 0.8], LAVA * 0.9, 2)
    sc.grid_plane(2.4, 8, 0, GOLD * 0.2)
    # ligne de danger
    sc.seg([-2.0, 0.12, 0.6], [2.0, 0.12, 0.6], RAD * (0.6 + 0.4 * math.sin(6 * t)), 2)
    cam = look_at(*orbit([0, 1.4, 0], 6.0, [0.25, -0.35][v % 2] + 0.2 * u, [0.15, 0.3][v % 2]))
    draw(img, sc, cam, fade=(2, 12))
    label3d(img, cam, [-1.25, -0.35, 0.4], "1986", GOLD, 1.4)
    label3d(img, cam, [0.35, -0.35, 0.4], "1989", GOLD, 1.4)


def sh_dust(img, u, t, v, T):
    sc = Scene()
    foot(sc, [0, 0, 0], 1.0, LAVA * (1 - 0.3 * u), t, cracks=ease(u * 1.5))
    for k in range(len(DUST)):
        ph = (k / len(DUST) + 0.25 * t) % 1.0
        a = 2 * math.pi * DUST[k, 0]
        r = 0.6 + 0.5 * abs(DUST[k, 2])
        y = 1.2 * (1 - ph) + 0.1
        p = np.array([r * math.cos(a) * (1 + 0.4 * ph), y, r * math.sin(a) * (1 + 0.4 * ph)])
        sc.seg(p, p + [0.01, 0.02, 0], (RAD if k % 3 == 0 else SAND) * (0.3 + 0.7 * ease(u * 2)), 2)
    cam = look_at(*orbit([0, 0.6, 0], lerp(4.2, 3.2, ease(u)), [1.2, -0.4][v % 2] + 0.4 * u, [0.25, 0.5][v % 2]))
    draw(img, sc, cam, fade=(2, 10))


def sh_neutrons(img, u, t, v, T):
    """Coupe : salle 305/2 au-dessus de la coulée ; les neutrons se multiplient."""
    sc = Scene()
    sc.box([0, 1.4, 0], [3.0, 1.4, 2.2], GOLD * 0.6, 1)
    sc.box([0, -0.4, 0], [3.0, 1.4, 2.2], GOLD * 0.3, 1)
    foot(sc, [0.7, -1.1, 0.2], 0.45, LAVA * 0.7, t)
    # débris de combustible
    for k in range(9):
        p = np.array([-1.0 + 0.25 * k, 0.8 + 0.05 * math.sin(k), 0.3 * math.cos(2 * k)])
        sc.box(p, [0.2, 0.12, 0.2], AMBER, 1)
    n = int(lerp(15, 200, ease(u)))
    for k in range(n):
        d = NEUT[k] / (np.linalg.norm(NEUT[k]) + 1e-6)
        ph = (0.6 * t + k * 0.137) % 1.0
        p = np.array([-1.0 + 2.0 * ((k * 0.37) % 1.0), 0.9, 0.3 * math.cos(k)]) + d * (0.1 + 0.6 * ph)
        sc.seg(p, p + d * 0.06, RAD * (1 - ph), 2)
    cam = look_at(*orbit([0, 0.6, 0] if v == 0 else [0, 0.9, 0], lerp(6.4, 5.4, ease(u)) - 1.2 * (v % 2), [0.5, -0.5][v % 2] - 0.3 * u, 0.25))
    draw(img, sc, cam, fade=(3, 12))
    # compteur


def sh_embers(img, u, t, v, T):
    sc = Scene()
    for k in range(len(EMB)):
        p = EMB[k] * np.array([1.6, 0.25, 1.0])
        s_ = 0.12 + 0.08 * abs(math.sin(k))
        b = 0.5 + 0.5 * math.sin(2.5 * t + 3 * k)
        col = LAVA * (0.4 + 0.6 * b) if k % 4 else HOT * b
        sc.box(p, [s_, s_ * 0.6, s_], col, 2 if b > 0.6 else 1)
    for k in range(30):
        ph = (0.4 * t + k / 30) % 1.0
        p = EMB[k] * np.array([1.4, 0.2, 0.9]) + [0, 0.2 + 1.6 * ph, 0]
        sc.seg(p, p + [0, 0.05, 0], HOT * (1 - ph), 2)
    sc.grid_plane(2.2, 8, -0.35, GOLD * 0.15)
    cam = look_at(*orbit([0, 0.1, 0], lerp(4.0, 3.2, ease(u)), 0.3 + 0.4 * u, 0.45))
    draw(img, sc, cam, fade=(2, 10))


def sh_final_foot(img, u, t, v, T):
    sc = Scene()
    b = 1 - 0.5 * ease(u)
    foot(sc, [0, 0, 0], 1.0, LAVA * b, t)
    sc.box([0, 3.0, 0], [3.0, 1.4, 2.2], GOLD * 0.35, 1)
    for k in range(40):
        d = NEUT[k] / (np.linalg.norm(NEUT[k]) + 1e-6)
        ph = (0.5 * t + k * 0.21) % 1.0
        p = np.array([0, 2.6, 0]) + d * (0.2 + 0.8 * ph) * np.array([1.2, 0.4, 0.8])
        sc.seg(p, p + d * 0.06, RAD * (1 - ph) * ease(u * 2), 2)
    cam = look_at(*orbit([0, lerp(0.6, 1.6, ease(u)), 0], lerp(3.8, 7.0, ease(u)), [0.8, -0.6][v % 2] + 0.4 * u, 0.2))
    draw(img, sc, cam, fade=(2, 14))
