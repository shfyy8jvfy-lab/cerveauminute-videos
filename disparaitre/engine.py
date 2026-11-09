"""Moteur de rendu des Reels @on.va.tous.disparaitre.

Usage :
  python3 engine.py episodes/ep02.py videos/ep02.mp4            # rendu complet (vidéo + son)
  python3 engine.py episodes/ep02.py --preview 0:1.5 4:2.0      # PNG d'aperçu dans preview/
  python3 engine.py episodes/ep02.py --durees                    # durées finales (avec voix) + thumb_offset

Un épisode est un fichier Python qui fait `from engine import *`, définit des fonctions
de scène `f(img, d, t, D)` et les variables : EPISODE (int), SCENES = [(fonction, durée_s), ...],
BOOM_SCENE (index de la scène où tombe le « boum » sonore, ou None), LEGENDE (str),
et VOIX = ["texte lu pendant la scène 0", ...] (un texte par scène) pour la voix off.

Voix off : si le dossier voix/epNN/ contient s00.mp3, s01.mp3… (générés avec ElevenLabs à partir de VOIX),
chaque scène est allongée si besoin pour que sa voix tienne dedans (début à VOICE_DELAY, marge VOICE_TAIL),
et la voix est mixée par-dessus la nappe sonore (baissée) et la musique originale de musique.py
(orgue spatial « slowed ») — DÉSACTIVÉE par défaut, à activer avec MUSIQUE = True dans l'épisode.
"""
import math, random, subprocess, sys, os, wave, importlib.util, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, S = 1080, 1920, 30, 2
FD = "/usr/share/fonts/opentype/inter/"
FB, FM, FBK = FD + "InterDisplay-Bold.otf", FD + "Inter-Medium.otf", FD + "InterDisplay-Black.otf"
HANDLE = "@on.va.tous.disparaitre"
LABEL = "FIN DE L'HUMANITÉ"

_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, int(size * S))
    return _fc[k]

def s(v): return int(round(v * S))
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def hexc(h, a=255):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)

def bg(d, color):
    d.rectangle([0, 0, W * S, H * S], fill=hexc(color))

def wrap(text, f, maxw):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= maxw * S: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def text_block(img, paras, t, y0, color, size=74, fpath=FB, gap=1.18, start=0.15, stagger=0.28):
    """paras : liste de str ou de (str, instant_d_apparition). Fondu + glissement vers le haut."""
    y = y0
    f = font(fpath, size)
    col = hexc(color) if isinstance(color, str) else color
    for i, para in enumerate(paras):
        txt, appear = (para if isinstance(para, tuple) else (para, start + i * stagger))
        k = ease((t - appear) / 0.35)
        for ln in wrap(txt, f, 900):
            if k > 0:
                layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
                dd = ImageDraw.Draw(layer)
                dd.text(((W * S - f.getlength(ln)) / 2, s(y + 28 * (1 - k))), ln, font=f, fill=col[:3] + (int(255 * k),))
                img.alpha_composite(layer)
            y += size * gap
        y += size * 0.35
    return y

def ctext(d, txt, y, size, color, fpath=FB, alpha=1.0):
    f = font(fpath, size)
    col = hexc(color) if isinstance(color, str) else color
    d.text(((W * S - f.getlength(txt)) / 2, s(y)), txt, font=f, fill=col[:3] + (int(255 * alpha),))

def header(d, accent):
    f = font(FM, 34)
    label = f"{LABEL} · ÉPISODE {EPISODE_NUM}"
    col = hexc(accent) if isinstance(accent, str) else accent
    d.text(((W * S - f.getlength(label)) / 2, s(190)), label, font=f, fill=col)

def circle(d, cx, cy, r, fill=None, outline=None, width=0):
    d.ellipse([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], fill=fill, outline=outline, width=s(width) if width else 0)

def line(d, pts, color, width):
    d.line([(s(x), s(y)) for x, y in pts], fill=hexc(color) if isinstance(color, str) else color, width=s(width), joint='curve')

random.seed(4)
STARS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(1, 3.2), random.random()) for _ in range(160)]
def stars(d, t, fade_from=None, D=1, col='#ffffff'):
    for i, (x, y, r, ph) in enumerate(STARS):
        a = 140 + 115 * math.sin(t * 2 + ph * 6)
        if fade_from is not None and t > fade_from + (i / len(STARS)) * (D - fade_from - 0.6):
            continue
        circle(d, x, y, r, fill=hexc(col, int(a)))

# ---------- scènes génériques réutilisables ----------
def scene_title(title_lines, subtitle, color='#b3121b'):
    def f(img, d, t, D):
        bg(d, color); header(d, hexc('#ffd6d6'))
        k = ease(t / 0.4)
        ctext(d, subtitle, 760, 40, '#ffd6d6', FM, k)
        size = int(150 + 30 * (1 - k))
        for i, l in enumerate(title_lines):
            ctext(d, l, 840 + i * size, size, '#ffffff', FBK, k)
    return f

def scene_end(punchline, color='#b3121b'):
    def f(img, d, t, D):
        bg(d, color); header(d, hexc('#ffd6d6'))
        text_block(img, [(punchline, 0.15)], t, 560, '#ffffff', size=82)
        k = ease((t - 1.9) / 0.4)
        if k > 0:
            y = 1080
            d.rounded_rectangle([s(140), s(y), s(940), s(y + 250)], radius=s(36), fill=hexc('#ffffff', int(255 * k)))
            ctext(d, "Abonnez-vous.", y + 55, 60, '#b3121b', FB, k)
            ctext(d, "Tant qu'il y a un demain.", y + 140, 46, '#4a0a0e', FM, k)
            ctext(d, HANDLE, y + 310, 50, '#ffffff', FB, k)
    return f

# ---------- rendu ----------
EPISODE_NUM = 0

def load_episode(path):
    global EPISODE_NUM
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    spec = importlib.util.spec_from_file_location("episode", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    EPISODE_NUM = mod.EPISODE
    import engine as _E
    _E.EPISODE_NUM = mod.EPISODE
    attach_voice(mod, path)
    return mod

VOICE_DELAY, VOICE_TAIL, VOICE_SPEED = 0.25, 0.45, 1.12  # voix légèrement accélérée (plus nerveuse)

def audio_duration(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())

def attach_voice(mod, path):
    """Si voix/epNN/sNN.mp3 existent pour toutes les scènes, allonge les scènes trop courtes."""
    here = os.path.dirname(os.path.abspath(__file__))
    vdir = os.path.join(here, 'voix', f'ep{mod.EPISODE:02d}')
    files = [os.path.join(vdir, f's{i:02d}.mp3') for i in range(len(mod.SCENES))]
    mod.VOIX_FILES = None
    if not os.path.isdir(vdir):
        return
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        raise SystemExit(f'voix incomplète : {len(missing)} fichier(s) manquant(s), ex. {missing[0]}')
    new = []
    for (fn, D), f in zip(mod.SCENES, files):
        need = VOICE_DELAY + audio_duration(f) / VOICE_SPEED + VOICE_TAIL
        new.append((fn, round(max(D, need), 2)))
    mod.SCENES = new
    mod.VOIX_FILES = files

def read_voice(f, sr=44100):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-af', f'atempo={VOICE_SPEED}', '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.int16).astype(np.float64) / 32768

def frame(fn, t, D):
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 255))
    fn(img, ImageDraw.Draw(img), t, D)
    return img.convert('RGB').reduce(S)

def render_scene(fn, D, out):
    tmp = out[:-4] + '.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                          '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for k in range(int(round(D * FPS))):
        p.stdin.write(frame(fn, k / FPS, D).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit(f'échec rendu {out}')
    os.replace(tmp, out)

MUSIC_LEVEL = 0.32  # volume de la musique sous la voix
# Musique de fond : fichier sous licence (Artlist « Frozen Lake », slowed & reverb) ; si absent,
# repli sur la musique originale générée par musique.py.
MUSIC_FILE = None

def make_audio(scenes, boom_scene, path, voice_files=None, music=True):
    sr = 44100
    total = sum(D for _, D in scenes)
    n = int(total * sr); t = np.arange(n) / sr
    out = (0.18 * np.sin(2*np.pi*55*t) + 0.10 * np.sin(2*np.pi*82.4*t) + 0.05 * np.sin(2*np.pi*110.3*t))
    out *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t)
    starts = np.cumsum([0] + [D for _, D in scenes])[:-1]
    for st in starts:
        a = int(st * sr); L = int(0.12 * sr)
        if a + L < n:
            out[a:a+L] += 0.25 * np.exp(-np.arange(L) / (0.02*sr)) * np.sin(2*np.pi*880*np.arange(L)/sr)
    if boom_scene is not None and 0 < boom_scene < len(scenes):
        a, b = int(starts[boom_scene - 1] * sr), int(starts[boom_scene] * sr)
        noise = np.convolve(np.random.default_rng(1).standard_normal(b - a), np.ones(40) / 40, mode='same')
        out[a:b] += 0.9 * noise * np.linspace(0, 1, b - a) ** 2
        L = min(int(1.6 * sr), n - b); tt = np.arange(L) / sr
        out[b:b+L] += 0.8 * np.sin(2*np.pi*(60 - 25*tt)*tt) * np.exp(-tt*2.5)
    fo, fi = int(1.5*sr), int(0.3*sr)
    out[-fo:] *= np.linspace(1, 0, fo); out[:fi] *= np.linspace(0, 1, fi)
    if voice_files:
        out = out / np.max(np.abs(out)) * 0.30
        vo = np.zeros(n)
        for st, f in zip(starts, voice_files):
            v = read_voice(f, sr)
            v = v / max(1e-6, np.max(np.abs(v))) * 0.92
            a = int((st + VOICE_DELAY) * sr); L = min(len(v), n - a)
            if L > 0: vo[a:a+L] += v[:L]
        env = np.convolve(np.abs(vo) > 0.02, np.ones(int(0.25 * sr)) / int(0.25 * sr), mode='same')
        duck = 1 - 0.45 * np.clip(env * 3, 0, 1)
        if music:
            from musique import make_music, load_music_file
            bt = starts[boom_scene] if boom_scene is not None and 0 < boom_scene < len(scenes) else None
            mfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), MUSIC_FILE) if MUSIC_FILE else None
            if mfile and os.path.exists(mfile):
                mus = load_music_file(mfile, total, bt, sr)[:n]
            else:
                mus = make_music(total, bt, sr)[:n]
            out = out * 0.6  # la nappe s'efface un peu derrière la musique
            mono = out * duck + vo
            st = np.stack([mono, mono], 1) + MUSIC_LEVEL * mus * duck[:, None]
        else:
            mono = out * duck + vo
            st = np.stack([mono, mono], 1)
        st = np.clip(np.tanh(st * 1.1) / np.tanh(1.1), -0.98, 0.98)  # limiteur doux
        stereo = (st * 32767).astype(np.int16)
    else:
        pcm = (out / np.max(np.abs(out)) * 0.85 * 32767).astype(np.int16)
        stereo = np.stack([pcm, pcm], axis=1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(stereo.tobytes())

def _render_one(args):
    path, i, out = args
    mod = load_episode(path)
    fn, D = mod.SCENES[i]
    render_scene(fn, D, out)

def main():
    path = sys.argv[1]
    mod = load_episode(path)
    here = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) > 2 and sys.argv[2] == '--durees':
        ds = [D for _, D in mod.SCENES]
        print('voix :', 'oui' if mod.VOIX_FILES else 'non')
        print('durées :', ds, '| total : %.1f s' % sum(ds))
        print('thumb_offset (milieu scène titre, ms) :', int((ds[0] + ds[1] / 2) * 1000))
        return
    if len(sys.argv) > 2 and sys.argv[2] == '--preview':
        os.makedirs(os.path.join(here, 'preview'), exist_ok=True)
        for a in sys.argv[3:]:
            i, tt = a.split(':'); fn, D = mod.SCENES[int(i)]
            frame(fn, float(tt), D).save(os.path.join(here, 'preview', f'ep{mod.EPISODE:02d}_s{int(i):02d}.png'))
        return
    out = sys.argv[2]
    work = f'/tmp/disparaitre_ep{mod.EPISODE:02d}'
    shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
    from multiprocessing import Pool
    jobs = [(path, i, f'{work}/s{i:02d}.mp4') for i in range(len(mod.SCENES))]
    with Pool(min(8, os.cpu_count() or 2)) as pool:
        pool.map(_render_one, jobs)
    with open(f'{work}/list.txt', 'w') as fl:
        for _, _, o in jobs: fl.write(f"file '{o}'\n")
    make_audio(mod.SCENES, getattr(mod, 'BOOM_SCENE', None), f'{work}/audio.wav', getattr(mod, 'VOIX_FILES', None), getattr(mod, 'MUSIQUE', False))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{work}/list.txt', '-c', 'copy', f'{work}/video.mp4'], check=True)
    tmp = out[:-4] + '.tmp.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{work}/video.mp4', '-i', f'{work}/audio.wav', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', tmp], check=True)
    os.replace(tmp, out)
    print(out)

if __name__ == '__main__':
    main()
