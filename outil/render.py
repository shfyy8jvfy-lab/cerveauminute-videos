"""Rendu d'une vidéo Cerveau Minute, style « tableau noir » (craie).
Usage : python3 render.py spec.json sortie.mp4  [--image t1,t2,...  : exporte seulement ces instants en PNG]

spec = {"audio": "...mp3", "segments": [{"key": "TEXTE", "dessin": "popcorn" | {"nom": "...", ...} | absent,
         "icon": "...", "hl": ["mot", ...], "chunks": [["texte dit", debut, fin], ...]}, ...]}
- "dessin" : illustration tracée à la craie (voir outil/dessins.py). Sans dessin, la clé est écrite en grand.
- "icon" (ancien format) est converti en dessin quand c'est possible (coin, ticket, question, plane…).
"""
import json, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dessins

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
F_TITLE = os.path.join(HERE, "polices", "CaveatBrush-Regular.ttf")
F_HAND = os.path.join(HERE, "polices", "PatrickHand-Regular.ttf")
_fcache = {}
def font(path, size):
    k = (path, int(size))
    if k not in _fcache:
        _fcache[k] = ImageFont.truetype(path, int(size))
    return _fcache[k]

CHALK = {"blanc": (244, 243, 236), "jaune": (255, 224, 110), "rose": (247, 160, 180), "bleu": (140, 200, 245),
         "orange": (252, 178, 96), "vert": (160, 225, 150), "rouge": (245, 118, 105), "gris": (175, 185, 180)}
ICON2DESSIN = {"coin": "euros", "ticket": "ticket", "question": "question", "plane": "fleche", "door": "question", "brain": "cerveau"}

DRAW_C = (540, 640)          # centre de la zone de dessin
KEY_Y_WITH_DRAW = 1035       # titre sous le dessin
SUB_Y = 1290                 # centre des sous-titres
SCALE = 1.1                  # agrandissement des dessins

# ---------------- tableau ----------------
rng = np.random.default_rng(7)

def make_board():
    base = np.zeros((H, W, 3), np.float32)
    base[:] = (34, 48, 42)
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.7)) ** 2)
    base *= (1.08 - 0.35 * d ** 2)[..., None]
    # traces d'effaçage (nuages de craie)
    smudge = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(smudge)
    r = random.Random(3)
    for _ in range(26):
        x, y = r.randint(0, W), r.randint(0, H); rx, ry = r.randint(120, 420), r.randint(40, 140)
        sd.ellipse([x - rx, y - ry, x + rx, y + ry], fill=r.randint(10, 26))
    for _ in range(40):  # vieilles écritures effacées
        x, y = r.randint(60, W - 60), r.randint(200, H - 200)
        pts = [(x + i * 18, y + r.randint(-14, 14)) for i in range(r.randint(4, 14))]
        sd.line(pts, fill=r.randint(14, 30), width=r.randint(5, 10))
    smudge = np.asarray(smudge.filter(ImageFilter.GaussianBlur(26)), np.float32) / 255
    base += smudge[..., None] * 160
    base += rng.normal(0, 4.5, (H, W, 1)).astype(np.float32)
    # cadre en bois
    fw = 26
    wood = np.zeros((H, W), bool); wood[:fw] = wood[-fw:] = True; wood[:, :fw] = wood[:, -fw:] = True
    grain = (np.sin(yy * 0.9 + np.sin(xx * 0.05) * 3) * 0.5 + 0.5) * 0.25 + 0.75
    wc = np.stack([150 * grain, 98 * grain, 58 * grain], -1)
    base[wood] = wc[wood]
    inner = np.zeros((H, W), bool); inner[fw:fw + 6, fw:-fw] = inner[-fw - 6:-fw, fw:-fw] = True
    inner[fw:-fw, fw:fw + 6] = inner[fw:-fw, -fw - 6:-fw] = True
    base[inner] *= 0.45
    return np.clip(base, 0, 255)

BOARD = make_board()
# grain de craie : fixe (la craie ne scintille pas)
_g = rng.random((H, W)).astype(np.float32)
_g = np.asarray(Image.fromarray((_g * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255
GRAIN = np.clip((_g - 0.18) / 0.45, 0, 1) * 0.78 + 0.18

def composite(base, layer):
    """Pose un calque RGBA de craie sur le tableau, avec le grain."""
    arr = np.asarray(layer, np.float32)
    a = (arr[..., 3] / 255 * GRAIN)[..., None]
    return base * (1 - a) + arr[..., :3] * a

# ---------------- traits ----------------

def wobble(pts, seed, amp=2.6, step=16):
    """Rééchantillonne une polyligne et lui donne un léger tremblé de main."""
    r = random.Random(seed)
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L / step))
        for i in range(n):
            t = i / n; out.append([x0 + (x1 - x0) * t, y0 + (y1 - y0) * t])
    out.append(list(pts[-1]))
    nx = ny = 0.0
    for p in out:
        nx = 0.7 * nx + 0.3 * r.uniform(-amp, amp) * 2; ny = 0.7 * ny + 0.3 * r.uniform(-amp, amp) * 2
        p[0] += nx; p[1] += ny
    return [tuple(p) for p in out]

def plen(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))

def cut(pts, length):
    out = [pts[0]]; acc = 0
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if acc + L >= length:
            t = (length - acc) / L if L else 0
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)); return out
        out.append(b); acc += L
    return out

def stroke(d, pts, col, w, alpha=255):
    if len(pts) < 2:
        return
    c = col + (alpha,)
    d.line(pts, fill=c, width=int(w), joint="curve")
    r = w / 2
    for x, y in (pts[0], pts[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)

def write_text(layer, s, x, y, size, col, prog=1.0, alpha=255, path=F_TITLE):
    """Texte à la craie centré sur (x, y), révélé de gauche à droite selon prog. Renvoie la position de la craie."""
    f = font(path, size)
    tmp = Image.new("RGBA", layer.size, (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
    td.text((x, y), s, font=f, fill=col + (alpha,), anchor="mm")
    x0, y0, x1, y1 = td.textbbox((x, y), s, font=f, anchor="mm")
    if prog < 1:
        cx = int(x0 + (x1 - x0) * max(0, prog))
        ImageDraw.Draw(tmp).rectangle([cx, 0, W, H], fill=(0, 0, 0, 0))
        layer.alpha_composite(tmp)
        return (cx, (y0 + y1) / 2)
    layer.alpha_composite(tmp)
    return None

# ---------------- préparation des segments ----------------
spec = json.load(open(sys.argv[1]))
SEG = spec["segments"]
last_end = max(c[2] for s in SEG for c in s["chunks"])
TOTAL = round(last_end + 1.6, 2)
STARTS = [0.0] + [s["chunks"][0][1] - 0.15 for s in SEG[1:]]

def prep(i, seg):
    dspec = seg.get("dessin")
    if not dspec and seg.get("icon") in ICON2DESSIN:
        dspec = ICON2DESSIN[seg["icon"]]
    items = dessins.get(dspec) or []
    cx, cy = DRAW_C
    out, total = [], 0.0
    for j, it in enumerate(items):
        if "pts" in it:
            pts = wobble([(x * SCALE + cx, y * SCALE + cy) for x, y in it["pts"]], seed=i * 1000 + j)
            L = plen(pts)
            out.append({"pts": pts, "len": L, "c": CHALK.get(it["c"], CHALK["blanc"]), "w": it["w"]})
        else:
            f = font(F_TITLE, it["size"])
            L = f.getlength(it["text"]) * 1.4
            out.append({"text": it["text"], "x": it["x"] * SCALE + cx, "y": it["y"] * SCALE + cy, "size": int(it["size"] * SCALE), "len": L,
                        "c": CHALK.get(it["c"], CHALK["jaune"])})
        total += out[-1]["len"]
    seg["_items"], seg["_len"] = out, total
    # durée de tracé : vitesse de craie constante, bornée
    seg["_draw_dur"] = min(1.7, max(0.6, total / 2600)) if out else 0

for i, s in enumerate(SEG):
    prep(i, s)

def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def draw_items(layer, seg, prog, alpha=255):
    """Trace les éléments du dessin jusqu'à la fraction prog. Renvoie la position de la craie."""
    d = ImageDraw.Draw(layer)
    budget = seg["_len"] * prog; tip = None
    for it in seg["_items"]:
        if budget <= 0:
            break
        part = min(1.0, budget / it["len"]) if it["len"] else 1
        if "pts" in it:
            pts = it["pts"] if part >= 1 else cut(it["pts"], it["len"] * part)
            stroke(d, pts, it["c"], it["w"], alpha)
            if part < 1: tip = pts[-1]
        else:
            t = write_text(layer, it["text"], it["x"], it["y"], it["size"], it["c"], part, alpha)
            if part < 1: tip = t
        budget -= it["len"]
    return tip

def chalk_stick(layer, tip):
    """Petit bâton de craie au bout du trait pendant qu'on dessine."""
    if not tip: return
    x, y = tip
    st = Image.new("RGBA", (120, 120), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle([50, 10, 74, 100], 8, fill=(250, 250, 244, 255))
    sd.rectangle([50, 70, 74, 100], fill=(225, 225, 215, 255))
    st = st.rotate(-28, resample=Image.BICUBIC)
    layer.alpha_composite(st, (int(x - 62 + 20), int(y - 105 + 40)))

def wrap(words, f, maxw):
    lines, cur = [], []
    for w in words:
        if cur and f.getlength(" ".join(cur + [w])) > maxw:
            lines.append(cur); cur = [w]
        else:
            cur.append(w)
    if cur: lines.append(cur)
    return lines

def draw_key(layer, seg, lt, alpha=255):
    key = seg.get("key") or ""
    if not key: return None
    if seg["_items"]:
        size = 92; f = font(F_TITLE, size)
        while f.getlength(key) > W - 160: size -= 4; f = font(F_TITLE, size)
        start = seg["_draw_dur"] * 0.85 + 0.05
        prog = ease((lt - start) / 0.45)
        return write_text(layer, key, W // 2, KEY_Y_WITH_DRAW, size, CHALK["jaune"], prog, alpha)
    size = 150; f = font(F_TITLE, size)
    while f.getlength(key) > W - 170: size -= 6; f = font(F_TITLE, size)
    prog = ease(lt / 0.55)
    tip = write_text(layer, key, W // 2, DRAW_C[1], size, CHALK["jaune"], prog, alpha)
    # soulignement à la main
    u = ease((lt - 0.45) / 0.35)
    if u > 0:
        hw = min(f.getlength(key) / 2 + 30, W / 2 - 90)
        pts = wobble([(W / 2 - hw, DRAW_C[1] + size * 0.62), (W / 2 + hw, DRAW_C[1] + size * 0.55)], seed=hash(key) % 999)
        stroke(ImageDraw.Draw(layer), cut(pts, plen(pts) * u), CHALK["blanc"], 9, alpha)
    return tip

def spoken_count(seg, t):
    n = 0
    for ctext, cs, ce in seg["chunks"]:
        wts = [len(w) + 2 for w in ctext.split()]; tot, c = sum(wts), 0
        for wgt in wts:
            if t >= cs + (ce - cs) * c / tot: n += 1
            c += wgt
    return n

F_SUBS = font(F_HAND, 88)
def draw_subs(layer, seg, t):
    d = ImageDraw.Draw(layer)
    words = " ".join(c[0] for c in seg["chunks"]).split()
    spoken = spoken_count(seg, t)
    hl = set(seg.get("hl", []))
    lines = wrap(words, F_SUBS, W - 190)
    lh = 104
    y = SUB_Y - (len(lines) * lh) // 2 + lh // 2; idx = 0
    for line in lines:
        x = (W - F_SUBS.getlength(" ".join(line))) / 2
        for w in line:
            idx += 1
            bare = w.strip(".,;:!?«»…\"'")
            ww = F_SUBS.getlength(w)
            if idx <= spoken:
                is_hl = w in hl or bare in hl
                col = CHALK["jaune"] if is_hl else CHALK["blanc"]
                d.text((x, y), w, font=F_SUBS, fill=col + (255,), anchor="lm")
                if is_hl:
                    pts = wobble([(x, y + 44), (x + ww, y + 40)], seed=idx * 7)
                    stroke(d, pts, CHALK["jaune"], 6)
            else:
                d.text((x, y), w, font=F_SUBS, fill=CHALK["blanc"] + (80,), anchor="lm")
            x += ww + F_SUBS.getlength(" ")
        y += lh

HEADER = Image.new("RGBA", (W, H), (0, 0, 0, 0))
write_text(HEADER, "Cerveau Minute", W // 2, 130, 66, CHALK["blanc"], alpha=170)
_hd = ImageDraw.Draw(HEADER)
for x0 in (W // 2 - 250, W // 2 + 220):  # petits traits décoratifs
    stroke(_hd, wobble([(x0, 132), (x0 + 30, 132)], seed=x0), CHALK["jaune"], 6, 170)

def frame(t):
    i = max(j for j in range(len(SEG)) if t >= STARTS[j])
    seg = SEG[i]; lt = t - STARTS[i]
    layer = HEADER.copy(); d = ImageDraw.Draw(layer)
    # barre de progression : trait de craie en haut
    pw = int((W - 120) * min(1, t / TOTAL))
    if pw > 4:
        stroke(d, [(60, 200), (60 + pw, 200)], CHALK["jaune"], 7, 200)
    # l'ancien dessin s'efface au début du segment
    if i > 0 and lt < 0.3:
        prev = SEG[i - 1]; a = int(255 * (1 - lt / 0.3) * 0.6)
        ghost = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_items(ghost, prev, 1.0, a); draw_key(ghost, prev, 99, a)
        layer.alpha_composite(ghost.filter(ImageFilter.GaussianBlur(3 + 10 * lt / 0.3)))
    tip = None
    if seg["_items"]:
        prog = (lt - 0.05) / seg["_draw_dur"]
        if prog > 0:
            tip = draw_items(layer, seg, min(1.0, prog))
    ktip = draw_key(layer, seg, lt)
    tip = tip or ktip
    draw_subs(layer, seg, t)
    if i == len(SEG) - 1:
        e = ease((t - (seg["chunks"][-1][2] - 0.2)) / 0.6)
        if e > 0:
            write_text(layer, "Abonne-toi : 1 concept par jour", W // 2, 1610, 64, CHALK["blanc"], e, 220)
    out = composite(BOARD, layer)
    if tip:
        st = Image.new("RGBA", (W, H), (0, 0, 0, 0)); chalk_stick(st, tip)
        a = np.asarray(st, np.float32); al = a[..., 3:4] / 255
        out = out * (1 - al) + a[..., :3] * al
    return Image.fromarray(out.astype(np.uint8))

if __name__ == "__main__":
    out = sys.argv[2]
    if "--image" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--image") + 1].split(",")]
        for tt in ts:
            frame(tt).save(f"{out}_{tt:05.2f}.png")
        sys.exit(0)
    n = int(TOTAL * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", spec["audio"], "-af", "apad", "-t", str(TOTAL),
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                          "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(n):
        p.stdin.write(frame(f / FPS).tobytes())
    p.stdin.close(); p.wait()
    print(out, TOTAL)
