"""Rendu d'une vidéo Cerveau Minute à partir d'une spec JSON.
Usage : python3 render.py spec.json sortie.mp4
spec = {"audio": "...mp3", "segments": [{"key": "TEXTE", "icon": "door|coin|ticket|plane|question|brain|none",
         "hl": ["mot", ...], "chunks": [["texte dit", debut, fin], ...]}, ...]}
"""
import json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BG1, BG2 = (12, 22, 52), (24, 40, 92)
YEL, WHITE, DIM, NAVY = (255, 210, 63), (255, 255, 255), (150, 165, 200), (14, 25, 58)
BOLD = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
F_CAP = ImageFont.truetype(BOLD, 78)
F_TAG = ImageFont.truetype(BOLD, 40)
F_SUB = ImageFont.truetype(BOLD, 52)

spec = json.load(open(sys.argv[1]))
SEG = spec["segments"]
last_end = max(c[2] for s in SEG for c in s["chunks"])
TOTAL = round(last_end + 1.5, 2)
STARTS = [0.0] + [s["chunks"][0][1] - 0.15 for s in SEG[1:]]

def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

BG = Image.new("RGB", (W, H)); _d = ImageDraw.Draw(BG)
for y in range(H):
    k = y / H; _d.line([(0, y), (W, y)], fill=tuple(int(BG1[i] + (BG2[i] - BG1[i]) * k) for i in range(3)))

CY = 640
def icon_door(d, k, lt):
    w, h = 300, 520; cx = W // 2; x0, y0 = cx - w // 2, CY - h // 2
    openk = ease((lt - 0.3) / 1.0)
    d.rectangle([x0 - 22, y0 - 22, x0 + w + 22, y0 + h], outline=WHITE, width=10)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(255, 245, 200))
    pw = int(w * (1 - 0.75 * openk))
    d.polygon([(x0, y0), (x0 + pw, y0 + int(40 * openk)), (x0 + pw, y0 + h - int(40 * openk)), (x0, y0 + h)], fill=YEL, outline=WHITE)
    d.ellipse([x0 + pw - 50, CY - 12, x0 + pw - 26, CY + 12], fill=BG1)

def icon_coin(d, k, lt):
    for i, dx in enumerate((-150, 0, 150)):
        kk = ease((lt - i * 0.12) / 0.4); y = CY + int(120 * (1 - kk)) - (40 if dx == 0 else 0)
        if kk <= 0: continue
        d.ellipse([W // 2 + dx - 120, y - 120, W // 2 + dx + 120, y + 120], fill=YEL, outline=WHITE, width=8)
        d.ellipse([W // 2 + dx - 92, y - 92, W // 2 + dx + 92, y + 92], outline=(230, 180, 40), width=6)
        d.text((W // 2 + dx, y + 4), "€", font=ImageFont.truetype(BOLD, 130), fill=NAVY, anchor="mm")

def icon_ticket(d, k, lt):
    s = 0.85 + 0.15 * k; w, h = int(620 * s), int(300 * s); x0, y0 = W // 2 - w // 2, CY - h // 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 30, fill=YEL)
    for yy in (y0 + h // 2,):
        d.ellipse([x0 - 40, yy - 40, x0 + 40, yy + 40], fill=BG1); d.ellipse([x0 + w - 40, yy - 40, x0 + w + 40, yy + 40], fill=BG1)
    for yy in range(y0 + 30, y0 + h - 20, 36):
        d.line([(x0 + int(w * 0.72), yy), (x0 + int(w * 0.72), yy + 18)], fill=NAVY, width=6)
    d.text((x0 + int(w * 0.36), CY), "CINÉ", font=ImageFont.truetype(BOLD, int(110 * s)), fill=NAVY, anchor="mm")

def icon_plane(d, k, lt):
    x = -300 + (W + 300) * ease(lt / 1.6) * 0.75; y = CY
    pts = [(x + 330, y), (x + 230, y - 18), (x + 40, y - 22), (x - 120, y - 150), (x - 170, y - 150), (x - 90, y - 24),
           (x - 210, y - 20), (x - 250, y - 70), (x - 280, y - 70), (x - 260, y), (x - 280, y + 30), (x - 90, y + 26), (x + 230, y + 18)]
    d.polygon(pts, fill=WHITE)
    for i in range(3):
        d.line([(x - 300 - i * 70, y + 4), (x - 340 - i * 70, y + 4)], fill=DIM, width=6)

def icon_question(d, k, lt):
    r = int(200 * (0.7 + 0.3 * k))
    d.ellipse([W // 2 - r, CY - r, W // 2 + r, CY + r], outline=YEL, width=16)
    d.text((W // 2, CY + 10), "?", font=ImageFont.truetype(BOLD, int(r * 1.5)), fill=YEL, anchor="mm")

ICONS = {"door": icon_door, "coin": icon_coin, "ticket": icon_ticket, "plane": icon_plane, "question": icon_question}

def wrap(words, font, maxw, d):
    lines, cur = [], []
    for w in words:
        if cur and d.textlength(" ".join(cur + [w]), font=font) > maxw:
            lines.append(cur); cur = [w]
        else:
            cur.append(w)
    if cur: lines.append(cur)
    return lines

def frame(t):
    img = BG.copy(); d = ImageDraw.Draw(img)
    i = max(j for j in range(len(SEG)) if t >= STARTS[j])
    seg = SEG[i]; lt = t - STARTS[i]; k = ease(lt / 0.35)
    d.rectangle([0, 0, int(W * min(1, t / TOTAL)), 14], fill=YEL)
    d.text((W // 2, 110), "CERVEAU MINUTE", font=F_TAG, fill=DIM, anchor="mm")
    icon = seg.get("icon", "none")
    if icon in ICONS:
        ICONS[icon](d, k, lt)
        if seg.get("key") and icon not in ("question",):
            d.text((W // 2, CY + 330), seg["key"], font=ImageFont.truetype(BOLD, 64), fill=YEL, anchor="mm")
    else:
        key = seg["key"]; size = int(120 * (0.7 + 0.3 * k)); f = ImageFont.truetype(BOLD, size)
        while d.textlength(key, font=f) > W - 140:
            size -= 6; f = ImageFont.truetype(BOLD, size)
        d.text((W // 2, CY + int(60 * (1 - k))), key, font=f, fill=YEL, anchor="mm")
        d.rounded_rectangle([W // 2 - 70, CY + 110, W // 2 + 70, CY + 122], 6, fill=WHITE)
    words = " ".join(c[0] for c in seg["chunks"]).split()
    spoken = 0
    for ctext, cs, ce in seg["chunks"]:
        wts = [len(w) + 2 for w in ctext.split()]; tot, c = sum(wts), 0
        for wgt in wts:
            if t >= cs + (ce - cs) * c / tot: spoken += 1
            c += wgt
    hl = set(seg.get("hl", []))
    lines = wrap(words, F_CAP, W - 160, d)
    y = 1260 - (len(lines) * 100) // 2; idx = 0
    for line in lines:
        x = (W - d.textlength(" ".join(line), font=F_CAP)) / 2
        for w in line:
            idx += 1
            bare = w.strip(".,;:!?«»…\"'")
            col = (YEL if (w in hl or bare in hl) else WHITE) if idx <= spoken else (70, 85, 125)
            d.text((x + 4, y + 5), w, font=F_CAP, fill=(5, 10, 25)); d.text((x, y), w, font=F_CAP, fill=col)
            x += d.textlength(w + " ", font=F_CAP)
        y += 100
    if i == len(SEG) - 1:
        d.text((W // 2, 1700), "Abonne-toi pour 1 concept / jour", font=F_SUB, fill=DIM, anchor="mm")
    return img

out = sys.argv[2]
n = int(TOTAL * FPS)
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-i", spec["audio"], "-af", "apad", "-t", str(TOTAL),
                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                      "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for f in range(n):
    p.stdin.write(frame(f / FPS).tobytes())
p.stdin.close(); p.wait()
print(out, TOTAL)
