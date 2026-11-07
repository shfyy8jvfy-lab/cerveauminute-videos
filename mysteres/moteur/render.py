"""Rendu 'hologramme fil de fer doré' multi-plans à partir de timeline.json.
Usage : python render.py out.mp4 [--preview]   (--preview : 1 image par plan dans previews/)
"""
import sys, math, json, os, subprocess
import numpy as np
import cv2

W, H, FPS = 1080, 1920, 30
TL = json.load(open("timeline.json", encoding="utf-8"))
OUT = sys.argv[1] if len(sys.argv) > 1 else "visual.mp4"
PREVIEW = "--preview" in sys.argv

GOLD = np.array([0.30, 0.72, 1.00])     # BGR
AMBER = np.array([0.12, 0.42, 0.95])
WHITE = np.array([0.92, 0.97, 1.00])
DIM = GOLD * 0.28
RNG = np.random.default_rng(3)
STARS = RNG.uniform(-1, 1, (500, 3)); STARS /= np.linalg.norm(STARS, axis=1, keepdims=True); STARS *= 60


# ---------------------------------------------------------------- géométrie
class Scene:
    def __init__(self):
        self.segs, self.cols, self.wid = [], [], []

    def add(self, pts, col, w=2, closed=False):
        pts = np.asarray(pts, float)
        if closed:
            pts = np.vstack([pts, pts[:1]])
        s = np.stack([pts[:-1], pts[1:]], 1)
        self.segs.append(s); self.cols.append(np.repeat(np.asarray(col)[None], len(s), 0))
        self.wid.append(np.full(len(s), w))

    def seg(self, a, b, col, w=2):
        self.add([a, b], col, w)

    def box(self, c, size, col, w=2, grid=0):
        c = np.asarray(c, float); hx, hy, hz = np.asarray(size, float) / 2
        V = np.array([[x, y, z] for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]) + c
        for i, j in [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (1, 3), (4, 6), (5, 7), (0, 4), (1, 5), (2, 6), (3, 7)]:
            self.seg(V[i], V[j], col, w)
        if grid:
            for k in range(1, grid):
                f = -1 + 2 * k / grid
                for sz in (-hz, hz):
                    self.seg(c + [f * hx, -hy, sz], c + [f * hx, hy, sz], col * 0.45, 1)
                for sx in (-hx, hx):
                    self.seg(c + [sx, -hy, f * hz], c + [sx, hy, f * hz], col * 0.45, 1)
                for sy in (-hy, hy):
                    self.seg(c + [-hx, sy, f * hz], c + [hx, sy, f * hz], col * 0.35, 1)

    def circle(self, c, r, col, w=1, n=64, axis="y"):
        th = np.linspace(0, 2 * math.pi, n, endpoint=False)
        c = np.asarray(c, float)
        if axis == "y":
            P = np.stack([c[0] + r * np.cos(th), np.full(n, c[1]), c[2] + r * np.sin(th)], 1)
        elif axis == "z":
            P = np.stack([c[0] + r * np.cos(th), c[1] + r * np.sin(th), np.full(n, c[2])], 1)
        else:
            P = np.stack([np.full(n, c[0]), c[1] + r * np.cos(th), c[2] + r * np.sin(th)], 1)
        self.add(P, col, w, closed=True)

    def pyramid(self, half=1.15, h=1.465, courses=34, col=GOLD, top=1.0, joints=True, c=(0, 0, 0)):
        c = np.asarray(c, float)
        hmax = h * top
        corners = lambda y: [c + [s1 * half * (1 - y / h), y, s2 * half * (1 - y / h)]
                             for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        self.add(corners(0), col, 3, closed=True)
        topc = corners(hmax)
        for a, b in zip(corners(0), topc):
            self.seg(a, b, col, 3)
        if top < 0.999:
            self.add(topc, WHITE * 0.9, 2, closed=True)
        for k in range(1, courses):
            y = h * k / courses
            if y > hmax: break
            self.add(corners(y), col * 0.5, 1, closed=True)
            if joints and k % 2 == 0:
                cs = corners(y); cs2 = corners(min(y + h / courses, hmax))
                for f in range(4):
                    a, b = cs[f], cs[(f + 1) % 4]; a2, b2 = cs2[f], cs2[(f + 1) % 4]
                    nj = max(2, int(8 * (1 - y / h)))
                    for j in range(1, nj):
                        u = (j + 0.5 * (k // 2 % 2)) / nj
                        if u < 1:
                            self.seg(a + (b - a) * u, a2 + (b2 - a2) * u, col * 0.3, 1)

    def grid_plane(self, size, n, y, col, c=(0, 0)):
        for i in range(n + 1):
            f = -size + 2 * size * i / n
            self.seg([c[0] + f, y, c[1] - size], [c[0] + f, y, c[1] + size], col, 1)
            self.seg([c[0] - size, y, c[1] + f], [c[0] + size, y, c[1] + f], col, 1)

    def arrays(self):
        if not self.segs:
            return np.zeros((0, 2, 3)), np.zeros((0, 3)), np.zeros(0)
        return np.concatenate(self.segs), np.concatenate(self.cols), np.concatenate(self.wid)


# ---------------------------------------------------------------- caméra
def look_at(eye, target, roll=0.0):
    eye = np.asarray(eye, float); f = np.asarray(target, float) - eye; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r) + 1e-9; u = np.cross(r, f)
    if roll:
        cr, sr = math.cos(roll), math.sin(roll); r, u = r * cr + u * sr, -r * sr + u * cr
    return eye, np.stack([r, u, f])


def orbit(target, dist, az, el):
    target = np.asarray(target, float)
    eye = target + dist * np.array([math.cos(el) * math.sin(az), math.sin(el), math.cos(el) * math.cos(az)])
    return eye, target


def draw(img, scene, cam, fov=0.8, near=0.05, fade=(2, 30)):
    eye, M = cam
    S, C, Wd = scene.arrays()
    if not len(S): return
    P = (S - eye) @ M.T  # (n,2,3)
    z = P[..., 2]
    ok = (z[:, 0] > near) & (z[:, 1] > near)
    f = (W / 2) / math.tan(fov / 2)
    xy = np.empty(P.shape[:2] + (2,))
    zz = np.maximum(z, near)
    xy[..., 0] = W / 2 + f * P[..., 0] / zz
    xy[..., 1] = H / 2 - f * P[..., 1] / zz
    zm = z.mean(1)
    b = np.clip(1.25 - (zm - fade[0]) / (fade[1] - fade[0]), 0.22, 1.25)
    lim = 4000
    for i in np.nonzero(ok)[0]:
        p = xy[i]
        if np.abs(p).max() > 1e5: continue
        if (p[:, 0] < -lim).all() or (p[:, 0] > W + lim).all(): continue
        cv2.line(img, (int(p[0, 0]), int(p[0, 1])), (int(p[1, 0]), int(p[1, 1])),
                 (C[i] * b[i]).tolist(), int(Wd[i]), cv2.LINE_AA)


def stars(img, cam, t, amt=1.0, spin=0.0):
    eye, M = cam
    c, s = math.cos(spin), math.sin(spin)
    St = STARS @ np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]).T
    P = (St) @ M.T
    ok = P[:, 2] > 1
    f = (W / 2) / math.tan(0.8 / 2)
    for p in P[ok]:
        x, y = int(W / 2 + f * p[0] / p[2]), int(H / 2 - f * p[1] / p[2])
        if 0 <= x < W and 0 <= y < H:
            cv2.circle(img, (x, y), 1, (GOLD * 0.5 * amt).tolist(), -1)


def ease(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)


def lerp(a, b, x):
    return np.asarray(a, float) + (np.asarray(b, float) - np.asarray(a, float)) * x


# ---------------------------------------------------------------- plans
# chaque fonction : (img, u in [0,1], t local s, v variante, T abs) -> dessine
def sh_pyramid_reveal(img, u, t, v, T):
    sc = Scene(); sc.pyramid(); sc.grid_plane(6, 24, 0, DIM * 0.6)
    if v == 0:
        cam = look_at(*orbit([0, 0.55, 0], lerp(7.5, 4.6, ease(u)), 0.6 + 0.35 * u, lerp(0.02, 0.22, ease(u))))
    else:
        cam = look_at(*orbit([0, 0.9, 0], 3.2 - 0.6 * u, 2.4 + 0.5 * u, 0.05 + 0.1 * u))
    stars(img, cam, T); draw(img, sc, cam)


def sh_blocks_fill(img, u, t, v, T):
    sc = Scene(); L = 7; s = 0.33
    shown = u * (L + 1.5)
    for i in range(L):
        a = min(max(shown - i, 0), 1)
        if a <= 0: break
        n = 2 * (L - i) - 1
        y = i * s + (1 - ease(a)) * 2.5
        half = n * s / 2
        col = GOLD * (0.4 + 0.6 * a)
        for k in range(n + 1):
            f = -half + k * s
            sc.seg([f, y + s, -half], [f, y + s, half], col * 0.55, 1)
            sc.seg([-half, y + s, f], [half, y + s, f], col * 0.55, 1)
            for sx in (-half, half):
                sc.seg([sx, y, f], [sx, y + s, f], col * 0.7, 1); sc.seg([f, y, sx], [f, y + s, sx], col * 0.7, 1)
        sc.box([0, y + s / 2, 0], [2 * half, s, 2 * half], col, 2)
    cam = look_at(*orbit([0, 0.9, 0], 6.3, 0.75 + 0.4 * u, 0.42))
    stars(img, cam, T, 0.6); draw(img, sc, cam)


def sh_scan(img, u, t, v, T):
    sc = Scene(); sc.pyramid(courses=40)
    if v == 0:
        y = lerp(0.05, 1.3, u)[()] if False else 0.05 + 1.3 * u
        k = 1 - y / 1.465; hh = 1.15 * k * 1.25
        sc.add([[-hh, y, -hh], [hh, y, -hh], [hh, y, hh], [-hh, y, hh]], WHITE, 3, closed=True)
        cam = look_at(*orbit([0, 0.6, 0], 3.6, -0.5 + 0.3 * u, 0.25))
    else:
        x = -1.2 + 2.4 * u
        sc.add([[x, 0, 1.0], [x, 1.5, 1.0], [x, 1.5, -1.0], [x, 0, -1.0]], WHITE * 0.8, 2, closed=True)
        cam = look_at([0.3 + 0.4 * u, 0.5, 3.6], [0, 0.55, 0])
    stars(img, cam, T, 0.5); draw(img, sc, cam)


def sh_casing_join(img, u, t, v, T):
    sc = Scene()
    u = (v + u) / 2  # progression continue sur les deux plans
    gap = lerp(1.2, 0.012, ease(min(u * 2.0, 1)))[()]
    sc.box([-(0.9 + gap / 2), 0, 0], [1.8, 1.2, 1.4], GOLD, 2, grid=4)
    sc.box([(0.9 + gap / 2), 0, 0], [1.8, 1.2, 1.4], GOLD, 2, grid=4)
    if u > 0.5:
        a = ease((u - 0.5) / 0.15)
        for yy in (0.75, -0.75):
            sc.seg([-gap / 2, yy * a, 0.71], [gap / 2, yy * a, 0.71], WHITE, 2)
        sc.seg([0, -0.9 * a, 0.72], [0, 0.9 * a, 0.72], WHITE, 3)
    if v == 0:
        cam = look_at(*orbit([0, 0, 0], lerp(5.2, 3.6, u), 0.35, 0.3))
    else:
        cam = look_at(*orbit([0, 0.1, 0.5], lerp(1.9, 1.3, u), 0.15 - 0.2 * u, 0.12))
    draw(img, sc, cam, fade=(1, 10))


def interior(sc):
    sc.pyramid(courses=18, col=GOLD * 0.55, joints=False)
    e = np.array([0, 0.17, 1.15 * (1 - 0.17 / 1.465) * 0.98]); ang = math.radians(26.5)
    d = np.array([0, -math.sin(ang), -math.cos(ang)])
    bottom = e + d * 0.6
    for off in (0.015, -0.015):
        sc.seg(e + [off, 0.02, 0], bottom + [off, 0.02, 0], WHITE, 2)
    sc.box(bottom + [0, -0.03, -0.12], [0.14, 0.06, 0.08], WHITE, 2)
    a0 = e + d * 0.2
    up = np.array([0, math.sin(ang), -math.cos(ang)])
    a1 = a0 + up * 0.36
    g1 = a1 + up * 0.48
    sc.seg(a0, a1, WHITE * 0.9, 2)
    for off in (0.03, -0.03):
        sc.seg(a1 + [off, 0, 0], g1 + [off, 0, 0], WHITE * 0.9, 2)
        sc.seg(a1 + [off, 0.08, 0], g1 + [off, 0.08, 0], WHITE * 0.6, 1)
    sc.box(g1 + [0, 0.03, -0.1], [0.2, 0.06, 0.1], WHITE, 2)  # chambre du roi
    for k in range(5):
        sc.box(g1 + [0, 0.08 + 0.03 * k, -0.1], [0.2, 0.012, 0.1], AMBER, 1)
    sc.seg(a1, a1 + [0, 0, -0.2], WHITE * 0.8, 2)
    sc.box(a1 + [0, 0.02, -0.24], [0.1, 0.05, 0.08], WHITE * 0.8, 2)
    return e, d


def sh_cutaway(img, u, t, v, T):
    sc = Scene(); interior(sc)
    cam = look_at(*orbit([0, 0.35, 0], lerp(3.4, 2.6, u), 1.45 + 0.25 * u, 0.12))
    stars(img, cam, T, 0.5); draw(img, sc, cam)


def sh_tunnel(img, u, t, v, T):
    sc = Scene(); step = 0.5; zoff = (t * 2.2) % step
    for k in range(40):
        z = -k * step + zoff
        b = 1.0 if k % 6 == 0 else 0.55
        sc.add([[-0.5, -0.6, z], [0.5, -0.6, z], [0.5, 0.6, z], [-0.5, 0.6, z]], GOLD * b, 2 if k % 6 == 0 else 1, closed=True)
    for x, y in ((-0.5, -0.6), (0.5, -0.6), (0.5, 0.6), (-0.5, 0.6)):
        sc.seg([x, y, 2], [x, y, -20], GOLD, 2)
    for x in np.linspace(-0.5, 0.5, 6):
        sc.seg([x, -0.6, 2], [x, -0.6, -20], GOLD * 0.35, 1)
    sc.seg([0, 0, -1], [0, 0, -20], WHITE * 0.9, 1)  # faisceau laser d'axe
    cam = look_at([0.05 * math.sin(t), 0.02, 1.2], [0, -0.05, -10], roll=0.03 * math.sin(t * 0.7))
    draw(img, sc, cam, fade=(1, 16), fov=1.2)


def sh_level(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(4, 32, 0, DIM)
    sc.add([[-1.15, 0, -1.15], [1.15, 0, -1.15], [1.15, 0, 1.15], [-1.15, 0, 1.15]], GOLD, 3, closed=True)
    sc.pyramid(courses=12, col=GOLD * 0.35, joints=False)
    z = -1.4 + 2.8 * ((u * 1.3) % 1)
    sc.seg([-3.5, 0.01, z], [3.5, 0.01, z], WHITE, 3)
    for x in (-1.15, 1.15):
        sc.seg([x, 0, 1.45], [x, 0.12, 1.45], WHITE * 0.8, 2)
    sc.seg([-1.15, 0.06, 1.45], [1.15, 0.06, 1.45], WHITE * 0.8, 2)
    if v == 0:
        cam = look_at([lerp(-2.5, -1.2, u)[()], 0.12, 3.2], [0.3, 0.05, 0])
    else:
        cam = look_at(*orbit([0, 0, 0], 4.2, 0.9 + 0.3 * u, 0.55))
    stars(img, cam, T, 0.4); draw(img, sc, cam)


def sh_north(img, u, t, v, T):
    sc = Scene(); sc.pyramid(courses=20, joints=False)
    for r in (1.9, 2.05):
        sc.circle([0, 0, 0], r, GOLD * 0.7, 1, 128)
    for k in range(72):
        a = 2 * math.pi * k / 72; l = 0.18 if k % 18 == 0 else (0.1 if k % 6 == 0 else 0.05)
        sc.seg([1.9 * math.sin(a), 0, -1.9 * math.cos(a)], [(1.9 - l) * math.sin(a), 0, -(1.9 - l) * math.cos(a)], GOLD, 1)
    sc.add([[-0.12, 0, -2.0], [0, 0, -2.45], [0.12, 0, -2.0]], WHITE, 3)
    sc.seg([0, 0, 0], [0, 0, -2.45], WHITE * 0.7, 1)
    if v == 0:
        cam = look_at([0, 5.2, 0.01], [0, 0, 0], roll=0.25 * u)
        stars(img, cam, T, 1.0, spin=t * 0.05)
    else:
        cam = look_at(*orbit([0, 0.3, -0.6], 4.6, 0.2 + 0.25 * u, 0.5))
        # traînées d'étoiles autour du pôle céleste
        sc2 = Scene()
        for r in np.linspace(0.6, 4, 12):
            th = np.linspace(0, 0.6 + u * 1.4, 30) + r
            P = np.stack([r * np.cos(th), 2.5 + r * np.sin(th), np.full_like(th, -6)], 1)
            sc2.add(P, GOLD * 0.45, 1)
        draw(img, sc2, cam)
    draw(img, sc, cam)


def chamber(sc):
    sc.box([0, 0.29, 0], [1.05, 0.58, 0.52], GOLD, 2, grid=3)
    y = 0.62
    for layer in range(5):
        for k in range(9):
            sc.box([-0.47 + k * 0.1175, y, 0], [0.105, 0.1, 0.6], AMBER if layer % 2 else GOLD * 0.8, 1)
        y += 0.24 if layer < 4 else 0
    sc.seg([-0.6, y + 0.06, 0], [0, y + 0.45, 0], WHITE * 0.8, 2)
    sc.seg([0.6, y + 0.06, 0], [0, y + 0.45, 0], WHITE * 0.8, 2)
    sc.box([0.25, 0.08, 0], [0.23, 0.1, 0.1], WHITE, 2)  # sarcophage


def sh_kings_chamber(img, u, t, v, T):
    sc = Scene(); chamber(sc)
    cam = look_at(*orbit([0, 1.0, 0], lerp(2.7, 2.1, u), 0.7 + 0.5 * u, lerp(-0.05, 0.15, u)))
    draw(img, sc, cam, fade=(1.5, 8))


def sh_beam_close(img, u, t, v, T):
    sc = Scene(); sc.box([0, 0, 0], [3.2, 0.55, 0.55], GOLD, 3, grid=8)
    a = ease(u * 1.5)
    sc.seg([-1.6, -0.5, 0.3], [-1.6 + 3.2 * a, -0.5, 0.3], WHITE, 2)
    for x in (-1.6, -1.6 + 3.2 * a):
        sc.seg([x, -0.6, 0.3], [x, -0.4, 0.3], WHITE, 2)
    cam = look_at(*orbit([0, 0, 0], lerp(3.0, 2.3, u), -0.5 + 0.6 * u, 0.25 - 0.2 * u))
    draw(img, sc, cam, fade=(1, 8))


def sh_boat(img, u, t, v, T):
    sc = Scene(); x0 = -1 + 2 * u
    for k in range(18):
        z = -6 + k * 0.7
        xs = np.linspace(-8, 8, 80)
        P = np.stack([xs, 0.04 * np.sin(xs * 2 + t * 2 + k), np.full_like(xs, z)], 1)
        sc.add(P, AMBER * 0.45, 1)
    L, Wd = 2.6, 0.5
    for f in np.linspace(-1, 1, 9):
        x = x0 + f * L / 2; w = Wd * (1 - f * f * 0.85); d = 0.28 * (1 - f * f * 0.6)
        sc.add([[x, 0.25 + 0.15 * f * f, -w / 2], [x, -d + 0.15, 0], [x, 0.25 + 0.15 * f * f, w / 2]], GOLD * 0.8, 1)
    xs = np.linspace(-1, 1, 30)
    for side in (-1, 1):
        sc.add(np.stack([x0 + xs * L / 2, 0.25 + 0.15 * xs ** 2, side * Wd / 2 * (1 - xs ** 2 * 0.85)], 1), GOLD, 2)
    sc.box([x0, 0.4, 0], [1.4, 0.28, 0.28], WHITE, 2, grid=4)
    sc.seg([x0 - 0.4, 0.25, 0], [x0 - 0.4, 1.9, 0], GOLD, 2)
    sc.add([[x0 - 0.4, 1.85, 0], [x0 + 0.5, 1.0, 0], [x0 - 0.4, 0.55, 0]], GOLD * 0.7, 1)
    cam = look_at(*orbit([x0 * 0.8, 0.5, 0], 4.6, 0.55, 0.2))
    stars(img, cam, T, 0.6); draw(img, sc, cam)


def sh_ramp_build(img, u, t, v, T):
    sc = Scene(); top = lerp(0.25, 0.9, ease(u))[()]
    sc.pyramid(top=top, courses=30)
    hy = 1.465 * top; zf = 1.15 * (1 - top)
    sc.add([[-0.12, hy, zf], [0.12, hy, zf], [0.12, 0, 3.2], [-0.12, 0, 3.2]], WHITE * 0.85, 2, closed=True)
    for k in range(1, 14):
        f = k / 14
        sc.seg([-0.12, hy * (1 - f), zf + (3.2 - zf) * f], [0.12, hy * (1 - f), zf + (3.2 - zf) * f], WHITE * 0.4, 1)
    sc.grid_plane(5, 20, 0, DIM * 0.6)
    cam = look_at(*orbit([0, 0.6, 0.6], 5.2, 0.95 + 0.25 * u, 0.3))
    stars(img, cam, T, 0.5); draw(img, sc, cam)


def sh_sledge(img, u, t, v, T):
    sc = Scene(); ang = 0.12
    for k in range(-10, 11):
        z = k * 0.4
        sc.seg([-0.8, z * math.sin(ang) * 0 + (-z) * ang, z], [0.8, (-z) * ang, z], DIM * 1.4, 1)
    for x in np.linspace(-0.8, 0.8, 9):
        sc.seg([x, 4 * ang, -4], [x, -4 * ang, 4], DIM * 1.4, 1)
    zc = lerp(1.5, -1.0, u)[()]
    yc = -zc * ang
    sc.box([0, yc + 0.32, zc], [0.6, 0.5, 0.7], GOLD, 2, grid=3)
    for x in (-0.25, 0.25):
        P = np.stack([np.full(12, x), yc + 0.04 + 0.06 * np.maximum(0, (np.linspace(-0.45, 0.45, 12) + 0.3) * -1) * 0,
                      zc + np.linspace(0.45, -0.5, 12)], 1)
        P[-3:, 1] += np.array([0.02, 0.05, 0.1])
        sc.add(P, WHITE, 2)
    for k in range(6):  # cordes vers l'avant
        x = -0.5 + 0.2 * k
        sc.seg([x * 0.5, yc + 0.2, zc - 0.5], [x * 1.6, yc + 0.3 + 2.5 * ang, zc - 3], AMBER, 1)
    for k in range(25):  # eau versée sur le sable
        dz = ((k * 0.37 + t * 1.5) % 1.0)
        sc.seg([-0.3 + 0.025 * k, yc + 0.02 + (zc - 0.7 + dz * 0.1) * -ang * 0, zc - 0.6 - dz * 0.2],
               [-0.3 + 0.025 * k, yc + 0.03, zc - 0.62 - dz * 0.2], WHITE * 0.6, 1)
    if v == 0:
        cam = look_at(*orbit([0, yc + 0.25, zc - 0.3], 2.3, 0.9 + 0.3 * u, 0.35))
    else:
        cam = look_at(*orbit([0, yc + 0.3, zc], 1.6, -2.4 + 0.3 * u, 0.15))
    draw(img, sc, cam, fade=(1.5, 10))


def sh_village(img, u, t, v, T):
    sc = Scene()
    if v == 0:
        rng = np.random.default_rng(5)
        for i in range(-5, 6):
            for j in range(-3, 4):
                if rng.random() < 0.25: continue
                w, d = 0.32, 0.22 + 0.1 * rng.random()
                sc.box([i * 0.42, 0.08, j * 0.42], [w, 0.16, d], GOLD * (0.55 + 0.45 * rng.random()), 1)
        sc.add([[-2.4, 0, -1.6], [2.4, 0, -1.6], [2.4, 0, 1.6], [-2.4, 0, 1.6]], WHITE * 0.7, 2, closed=True)
        sc.pyramid(c=(0, 0, -6), courses=16, joints=False, col=GOLD * 0.6)
        cam = look_at(*orbit([0, 0, -0.5], lerp(4.6, 3.6, u), 0.25 + 0.3 * u, 0.6))
    else:
        # papyrus de Merer : feuille ondulée + lignes de texte qui apparaissent
        xs = np.linspace(-1.2, 1.2, 50)
        for y in (-0.7, 0.7):
            sc.add(np.stack([xs, np.full(50, y), 0.06 * np.sin(xs * 3)], 1), GOLD, 2)
        for x in (-1.2, 1.2):
            sc.seg([x, -0.7, 0.06 * math.sin(x * 3)], [x, 0.7, 0.06 * math.sin(x * 3)], GOLD, 2)
        nl = int(14 * ease(u * 1.3))
        r2 = np.random.default_rng(9)
        for k in range(nl):
            col_x = 1.05 - (k // 7) * 1.1
            y = 0.55 - (k % 7) * 0.18
            for g in range(r2.integers(4, 9)):
                x = col_x - g * 0.12
                sc.seg([x, y, 0.06 * math.sin(x * 3) + 0.01], [x - 0.07, y + 0.03 * r2.uniform(-1, 1), 0.06 * math.sin(x * 3) + 0.01], WHITE * 0.8, 1)
        cam = look_at(*orbit([0, 0, 0], lerp(3.0, 2.5, u), -0.3 + 0.3 * u, 0.1))
    stars(img, cam, T, 0.5); draw(img, sc, cam)


def sh_final(img, u, t, v, T):
    sc = Scene()
    sc.pyramid(c=(0, 0, 0))
    sc.pyramid(c=(-2.2, 0, -2.0), half=1.07, h=1.36, courses=26, col=GOLD * 0.8)
    sc.pyramid(c=(-3.9, 0, -3.8), half=0.52, h=0.65, courses=14, col=GOLD * 0.6)
    sc.grid_plane(8, 30, 0, DIM * 0.5)
    if v == 0:
        cam = look_at(*orbit([-1.4, 0.4, -1.4], lerp(4.2, 6.5, ease(u)), 0.9 + 0.2 * u, lerp(0.1, 0.25, u)))
    else:
        cam = look_at(*orbit([-1.4, 0.6, -1.4], lerp(6.5, 8.5, ease(u)), 1.1 + 0.15 * u, 0.12))
    stars(img, cam, T, 1.0, spin=T * 0.01); draw(img, sc, cam, fade=(3, 18))



# ---------------------------------------------------------------- plans v2
COPPER = np.array([0.25, 0.50, 0.95])


def granite_block(sc, c, size, col=GOLD):
    sc.box(c, size, col, 2, grid=6)
    r = np.random.default_rng(11)
    hx, hy, hz = np.asarray(size) / 2
    for _ in range(140):  # grain du granit
        p = np.asarray(c) + [r.uniform(-hx, hx), r.uniform(-hy, hy), hz + 0.002]
        sc.seg(p, p + [0.02, 0.0, 0], WHITE * r.uniform(0.2, 0.6), 1)


def chisel(sc, tip, d=np.array([0, 0, 1.0]), L=1.6, col=COPPER):
    tip = np.asarray(tip, float); d = d / np.linalg.norm(d)
    back = tip + d * L
    w = 0.06
    for ox, oy in ((-w, -w), (w, -w), (w, w), (-w, w)):
        sc.seg(tip + [ox * 0.3, oy, 0], back + [ox, oy, 0], col, 2)
    sc.add([back + [-w, -w, 0], back + [w, -w, 0], back + [w, w, 0], back + [-w, w, 0]], col, 2, closed=True)
    sc.seg(tip + [-w * 0.3, -w, 0], tip + [w * 0.3, -w, 0], WHITE, 3)
    sc.seg(tip + [-w * 0.3, w, 0], tip + [w * 0.3, w, 0], WHITE, 3)


def sh_chisel_granite(img, u, t, v, T):
    sc = Scene(); granite_block(sc, [0, 0, 0], [2.0, 1.4, 1.2], GOLD * 0.9)
    hit = abs(math.sin(t * 5.0)) ** 3
    tip = np.array([0.15, 0.1, 0.6 + 0.08 + 0.25 * hit])
    chisel(sc, tip, np.array([0.15, 0.25, 1.0]))
    if hit < 0.15:
        for k in range(8):
            a = k * 0.8 + t
            sc.seg(tip + [0, 0, -0.06], tip + [0.15 * math.cos(a), 0.15 * math.sin(a), 0.05], WHITE * 0.8, 1)
    if v == 0:
        cam = look_at(*orbit([0, 0.1, 0.3], lerp(4.2, 3.4, u), 0.55 + 0.2 * u, 0.25))
    else:
        cam = look_at(*orbit(tip * 0.8, lerp(1.6, 1.3, u), 0.9 - 0.3 * u, 0.15))
    draw(img, sc, cam, fade=(1, 9))


def sh_saw_cut(img, u, t, v, T):
    sc = Scene(); uu = (v + u) / 2
    granite_block(sc, [0, 0, 0], [2.2, 1.2, 1.2], GOLD * 0.85)
    depth = 1.0 * uu
    sc.add([[-0.012, 0.6, -0.61], [-0.012, 0.6 - depth, -0.61], [-0.012, 0.6 - depth, 0.61], [-0.012, 0.6, 0.61]], WHITE, 2)
    sx = 0.5 * math.sin(t * 3.0)
    hb = lerp(0.45, 0.28, uu)[()]  # la lame s'use
    y0 = 0.6 - depth
    sc.add([[0, y0, -1.4 + sx], [0, y0 + hb, -1.4 + sx], [0, y0 + hb, 1.4 + sx], [0, y0, 1.4 + sx]], COPPER, 2, closed=True)
    sc.seg([0, y0 + hb + 0.06, -1.2 + sx], [0, y0 + hb + 0.06, 1.2 + sx], COPPER * 0.6, 4)
    r = np.random.default_rng(int(T * 12))
    for _ in range(60):  # sable abrasif
        p = np.array([r.uniform(-0.25, 0.25), 0.62 + r.uniform(0, 0.15), r.uniform(-0.65, 0.65)])
        sc.seg(p, p + [0.01, -0.01, 0.01], WHITE * 0.9, 2)
    if v == 0:
        cam = look_at(*orbit([0, 0.3, 0], lerp(4.0, 3.3, u), 1.1 + 0.2 * u, 0.35))
    else:
        cam = look_at(*orbit([0, 0.3, 0], lerp(2.4, 2.0, u), 0.25 + 0.2 * u, 0.25))
    draw(img, sc, cam, fade=(1, 9))


def sh_harbor_core(img, u, t, v, T):
    sc = Scene()
    if v == 0:
        for k in range(14):  # couches de sédiments
            y = -k * 0.18
            col = COPPER * 1.2 if k in (6, 7) else GOLD * (0.25 + 0.03 * k)
            sc.circle([0, y, 0], 0.35, col, 2 if k in (6, 7) else 1, 48)
        for a in np.linspace(0, 2 * math.pi, 12, endpoint=False):
            sc.seg([0.35 * math.cos(a), 0, 0.35 * math.sin(a)], [0.35 * math.cos(a), -2.4, 0.35 * math.sin(a)], GOLD * 0.35, 1)
        pulse = 0.7 + 0.3 * math.sin(t * 4)
        for k in (6, 7):
            y = -k * 0.18
            for rr in (0.38, 0.42):
                sc.circle([0, y, 0], rr, COPPER * pulse, 1, 48)
        cam = look_at(*orbit([0, -1.1, 0], lerp(3.6, 3.0, u), 0.5 + 0.4 * u, 0.15))
    else:
        for k in range(16):
            z = -5 + k * 0.6
            xs = np.linspace(-6, 3, 60)
            sc.add(np.stack([xs, 0.03 * np.sin(xs * 2 + t * 1.5 + k), np.full_like(xs, z)], 1), AMBER * 0.4, 1)
        sc.pyramid(c=(3.5, 0, -2.5), courses=20, joints=False)
        sc.circle([0, 0.01, 0], 0.4 + 0.15 * math.sin(t * 3), COPPER, 2, 48)
        sc.seg([0, 0, 0], [0, -1.5, 0], COPPER, 3)
        cam = look_at(*orbit([1.6, 0.3, -1.2], 5.2, 0.35 + 0.2 * u, 0.25))
    stars(img, cam, T, 0.5); draw(img, sc, cam)


MUON = np.random.default_rng(21).uniform(0, 1, (90, 4))


def sh_muons(img, u, t, v, T):
    sc = Scene(); sc.pyramid(courses=28)
    for a, b, c0, ph in MUON:
        x0, z0 = -2.5 + 5 * a, -2.5 + 5 * b
        dirv = np.array([0.35 * (c0 - 0.5), -1, 0.25 * (ph - 0.5)])
        k = ((t * 1.6 + ph * 4) % 4.0)
        p0 = np.array([x0, 4.5, z0]) + dirv * k
        sc.seg(p0, p0 + dirv * 0.45, WHITE * 0.85, 1)
    sc.box([0, 0.24, 0], [0.12, 0.08, 0.12], COPPER, 2)  # détecteurs (chambre de la Reine)
    if v == 0:
        cam = look_at(*orbit([0, 1.0, 0], lerp(6.5, 5.2, u), 0.6 + 0.3 * u, 0.25))
    else:
        cam = look_at(*orbit([0, 0.5, 0], 3.6, 2.2 + 0.3 * u, 0.1))
    stars(img, cam, T); draw(img, sc, cam)


def void_box(sc, t, amp=1.0):
    ang = math.radians(26.5); up = np.array([0, math.sin(ang), -math.cos(ang)])
    a1 = np.array([0, 0.17, 1.15 * (1 - 0.17 / 1.465) * 0.98]) + np.array([0, -math.sin(ang), -math.cos(ang)]) * 0.2 + up * 0.36
    c = a1 + up * 0.24 + np.array([0, 0.22, 0])
    pulse = (0.7 + 0.3 * math.sin(t * 3)) * amp
    for s in (1.0, 1.15):
        sc.box(c, [0.08 * s, 0.09 * s, 0.32 * s], WHITE * pulse / s, 2 if s == 1 else 1)
    return c


def sh_big_void(img, u, t, v, T):
    sc = Scene(); interior(sc); c = void_box(sc, t)
    if v == 0:
        cam = look_at(*orbit([0, 0.4, 0], lerp(3.4, 2.4, u), 1.4 + 0.2 * u, 0.15))
    else:
        cam = look_at(*orbit(c, lerp(1.4, 0.9, u), 1.0 + 0.5 * u, 0.25))
    stars(img, cam, T, 0.4); draw(img, sc, cam, fade=(1, 10))


def sh_corridor(img, u, t, v, T):
    sc = Scene()
    for k in range(-6, 7):  # assises de la face nord
        y = k * 0.25
        sc.seg([-3, y, 0], [3, y, 0], GOLD * 0.35, 1)
        for j in range(-6, 7):
            x = j * 0.5 + (0.25 if k % 2 else 0)
            sc.seg([x, y, 0], [x, y + 0.25, 0], GOLD * 0.25, 1)
    for s, col in ((0.6, GOLD), (0.9, GOLD * 0.8)):  # chevrons
        sc.add([[-s, -0.6, 0.01], [0, -0.6 + s * 0.9, 0.01], [s, -0.6, 0.01]], col, 3)
    sc.add([[-0.25, -1.0, 0.01], [0.25, -1.0, 0.01], [0.25, -1.5, 0.01], [-0.25, -1.5, 0.01]], WHITE * 0.8, 2, closed=True)
    reveal = ease((u + v) / 1.5)
    sc.box([0, 0.0, -1.2], [0.45, 0.45, 2.2], WHITE * (0.3 + 0.7 * reveal), 2, grid=4)
    ln = 0.9 * ease(min(1, (u + v) * 1.2))
    sc.seg([0.1, -0.22, 0.6], [0.1, -0.22, 0.6 - ln], COPPER, 2)
    sc.seg([0.1, -0.22, 0.6], [0.6, -0.9, 1.6], COPPER * 0.6, 1)
    cam = look_at(*orbit([0, -0.2, -0.6], lerp(4.0, 3.2, u), 0.45 + (0.5 if v else 0) + 0.15 * u, 0.12 + 0.1 * v))
    draw(img, sc, cam, fade=(1, 10))


def sh_papyrus(img, u, t, v, T):
    sc = Scene(); uu = (u + v) / 3
    xs = np.linspace(-1.2, 1.2, 50)
    for y in (-0.7, 0.7):
        sc.add(np.stack([xs, np.full(50, y), 0.06 * np.sin(xs * 3)], 1), GOLD, 2)
    for x in (-1.2, 1.2):
        sc.seg([x, -0.7, 0.06 * math.sin(x * 3)], [x, 0.7, 0.06 * math.sin(x * 3)], GOLD, 2)
    nl = int(21 * ease(min(1, uu * 1.4 + 0.1)))
    r2 = np.random.default_rng(9)
    for k in range(nl):
        col_x = 1.05 - (k // 7) * 0.8
        y = 0.55 - (k % 7) * 0.18
        for g in range(r2.integers(4, 7)):
            x = col_x - g * 0.11
            z = 0.06 * math.sin(x * 3) + 0.01
            sc.seg([x, y, z], [x - 0.07, y + 0.03 * r2.uniform(-1, 1), z], WHITE * 0.8, 1)
    cams = [(3.0, -0.4, 0.1), (2.0, 0.35, 0.25), (2.6, 0.0, -0.15)]
    dist, az, el = cams[v % 3]
    cam = look_at(*orbit([0.2 * (v - 1), 0, 0], dist - 0.3 * u, az + 0.2 * u, el))
    stars(img, cam, T, 0.5); draw(img, sc, cam)


def sh_river_map(img, u, t, v, T):
    sc = Scene(); sc.grid_plane(5, 20, 0, DIM * 0.6)
    zs = np.linspace(-5, 5, 80)
    sc.add(np.stack([2.2 + 0.4 * np.sin(zs * 0.6), np.zeros(80), zs], 1), AMBER * 0.6, 2)  # Nil actuel
    n = int(80 * ease(min(1, (u + v) * 0.9 + 0.1)))
    br = np.stack([-0.6 + 0.35 * np.sin(zs * 0.9 + 1), np.full(80, 0.01), zs], 1)
    if n > 1:
        sc.add(br[:n], WHITE, 3)
        sc.add(br[:n] + [0.12, 0, 0], GOLD, 1); sc.add(br[:n] - [0.12, 0, 0], GOLD, 1)
    for zz in np.linspace(-4, 4, 9):  # pyramides le long du bras
        x = -0.6 + 0.35 * math.sin(zz * 0.9 + 1) - 0.55
        sc.pyramid(half=0.12, h=0.15, courses=2, joints=False, c=(x, 0, zz), col=GOLD)
    sy = 3.0; sz = -5 + 10 * ((u + v) / 2)
    sc.box([0, sy, sz], [0.2, 0.15, 0.3], WHITE * 0.8, 1)
    sc.box([-0.4, sy, sz], [0.5, 0.02, 0.2], AMBER, 1); sc.box([0.4, sy, sz], [0.5, 0.02, 0.2], AMBER, 1)
    sc.seg([0, sy, sz], [-0.6, 0.01, sz], WHITE * 0.4, 1); sc.seg([0, sy, sz], [0.6, 0.01, sz], WHITE * 0.4, 1)
    cam = look_at(*orbit([0, 0, 0], lerp(8.5, 7.5, u), 0.3 + 0.2 * v, lerp(1.1, 1.0, u)))
    draw(img, sc, cam, fade=(3, 14))


def sh_final_void(img, u, t, v, T):
    sc = Scene(); sc.pyramid(courses=30, col=GOLD * 0.7)
    void_box(sc, t, 1.3)
    cam = look_at(*orbit([0, 0.5, 0], lerp(2.6, 5.5, ease((u + v) / 2)), 1.2 + 0.3 * u, 0.12))
    stars(img, cam, T); draw(img, sc, cam)



def sh_hook_void(img, u, t, v, T):
    sc = Scene(); sc.pyramid(courses=30, col=GOLD * lerp(0.9, 0.45, ease(u))[()])
    c = void_box(sc, t, 1.0 + 0.6 * ease(u))
    cam = look_at(*orbit(lerp([0, 0.6, 0], c, ease(u)), lerp(6.0, 1.6, ease(u)), 0.9 + 0.4 * u, lerp(0.25, 0.12, u)))
    stars(img, cam, T); draw(img, sc, cam, fade=(1, 14))


if os.path.exists("scenes.py"):  # plans propres à l'épisode
    exec(open("scenes.py", encoding="utf-8").read(), globals())

SHOTS = {k[3:]: v for k, v in globals().items() if k.startswith("sh_")}


# ---------------------------------------------------------------- post
def hud(img, T):
    sy = int((T * 300) % (H + 300)) - 150
    cv2.line(img, (0, sy), (W, sy), (GOLD * 0.12).tolist(), 2)


def glow(img):
    small = cv2.resize(img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    g1 = cv2.resize(cv2.GaussianBlur(small, (0, 0), 2), (W, H))
    g2 = cv2.resize(cv2.GaussianBlur(small, (0, 0), 7), (W, H))
    return img + 0.9 * g1 + 0.9 * g2


yy, xx = np.mgrid[0:H, 0:W]
VIGN = (1 - 0.6 * (((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2)).clip(0.25, 1)[..., None].astype(np.float32)


XF = 0.6  # durée du fondu enchaîné (s)


def shot_layer(i, T):
    s = TL["shots"][i]
    d = s["e"] - s["s"]; t = T - s["s"]; u = min(max(t / d, 0.0), 1.08)
    img = np.zeros((H, W, 3), np.float32)
    SHOTS[s["name"]](img, u, t, s.get("v", 0), T)
    return img


def frame(T):
    shots = TL["shots"]
    i = max(k for k, s in enumerate(shots) if s["s"] <= T + 1e-6) if T >= 0 else 0
    t = T - shots[i]["s"]
    img = shot_layer(i, T)
    if i > 0 and t < XF:
        a = ease(t / XF)
        img = img * a + shot_layer(i - 1, T) * (1 - a)
    hud(img, T)
    img = glow(img) * VIGN
    k = ease(T / 0.6) * ease((TL["duration"] - T) / 1.0)
    return np.clip(img * k, 0, 1)


if PREVIEW:
    os.makedirs("previews", exist_ok=True)
    for j, s in enumerate(TL["shots"]):
        T = s["s"] + 0.6 * (s["e"] - s["s"])
        cv2.imwrite(f"previews/{j:02d}_{s['name']}.png", (frame(T) * 255).astype(np.uint8))
    print("previews ok")
    sys.exit()

ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
                       "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                       "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
N = int(TL["duration"] * FPS)
for fi in range(N):
    ff.stdin.write((frame(fi / FPS) * 255).astype(np.uint8).tobytes())
    if fi % 300 == 0: print(f"frame {fi}/{N}", flush=True)
ff.stdin.close(); ff.wait(); print("ok", OUT)
