"""Musique originale pour @on.va.tous.disparaitre — ambiance « orgue spatial, slowed + reverb ».

Composition générée par code (aucun extrait d'œuvre existante) : grille originale en ré mineur,
orgue d'église très lent, ostinato de deux notes qui tic-tac comme une horloge, pouls grave,
le tout ralenti, assombri (filtre passe-bas) et noyé dans une grande réverbération.
Montée progressive jusqu'au « boum », silence d'une demi-seconde, puis reprise plus ample.

make_music(total_s, boom_t=None, sr=44100) -> tableau numpy (n, 2) normalisé à 1.
"""
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SLOW = 0.87  # facteur « slowed » : tout est joué plus grave et plus lent


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12) * SLOW


# grille originale (ré mineur) : Dm – B♭ – Gm – A(sus4→A) / Dm – F – C – A
PROG = [
    (38, [62, 65, 69]), (34, [62, 65, 70]), (31, [62, 67, 70]), (33, [61, 64, 69]),
    (38, [62, 65, 69]), (41, [60, 65, 69]), (36, [60, 64, 67]), (33, [61, 64, 69]),
]
CH = 4.6 / SLOW  # durée d'un accord (s)


def organ(freq, n, sr, att=1.6, rel=2.2):
    tt = np.arange(n) / sr
    out = np.zeros(n)
    for h, a in zip([1, 2, 3, 4, 6, 8], [1, .5, .28, .2, .09, .05]):
        for det in (-0.0015, 0.0015):
            out += a * np.sin(2 * np.pi * freq * h * (1 + det) * tt + h)
    env = np.clip(np.minimum(tt / att, (n / sr - tt) / rel), 0, 1)
    return out * env * (1 + 0.05 * np.sin(2 * np.pi * 0.2 * tt))


def make_music(total_s, boom_t=None, sr=44100):
    N = int(total_s * sr); t = np.arange(N) / sr
    pad = np.zeros(N); ost = np.zeros(N); tick = np.zeros(N)
    pos, k = 0.0, 0
    while pos < total_s:
        root, notes = PROG[k % len(PROG)]
        s0 = int(pos * sr); n = min(int((CH + 2.2) * sr), N - s0)
        if n <= 0: break
        seg = organ(midi(root), n, sr) * 0.8 + organ(midi(root + 12), n, sr) * 0.5
        for m in notes:
            seg += organ(midi(m - 12), n, sr) * 0.3
        pad[s0:s0 + n] += seg
        # ostinato : deux notes de l'accord en alternance, comme un balancier
        step = 0.42 / SLOW
        hi = [notes[2] + 12, notes[1] + 12]
        for j in range(int(CH / step)):
            a0 = int((pos + j * step) * sr); ln = int(1.2 * sr)
            if a0 + ln > N: break
            tt = np.arange(ln) / sr; f = midi(hi[j % 2])
            tone = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt + 1)) * np.exp(-tt * 3.2)
            ost[a0:a0 + ln] += tone * np.minimum(1, tt / 0.008)
            # petit « tic » boisé sur chaque temps
            lt = int(0.03 * sr); nz = np.random.default_rng(a0).standard_normal(lt)
            tick[a0:a0 + lt] += nz * np.exp(-np.arange(lt) / (0.004 * sr)) * (1.0 if j % 2 == 0 else 0.6)
        pos += CH; k += 1

    def ramp(x0, x1):
        return np.clip((t - x0) / max(x1 - x0, 1e-3), 0, 1)

    bt = boom_t if boom_t else total_s * 0.45
    build = ramp(0, bt)                       # montée jusqu'au boum
    after = ramp(bt + 0.6, bt + 3.0)          # reprise après le silence
    gap = 1 - np.clip((t - (bt - 0.05)) / 0.05, 0, 1) * np.clip(((bt + 0.55) - t) / 0.05, 0, 1)
    sub = np.sin(2 * np.pi * 36.7 * SLOW * t) * (0.4 + 0.6 * build)
    pad_env = (0.45 + 0.4 * build) * (1 - after) + 0.95 * after
    ost_env = (0.2 + 0.8 * build) * (1 - after) + 0.7 * after
    mix = pad * pad_env * 0.10 + ost * ost_env * 0.11 + tick * 0.035 + sub * 0.12
    mix *= gap

    # « slowed » : on assombrit (passe-bas) puis grande réverbération stéréo (5 s)
    mix = sosfilt(butter(4, 2600, 'low', fs=sr, output='sos'), mix)
    rng = np.random.default_rng(7)
    irl = int(5.0 * sr)
    ir = rng.standard_normal(irl) * np.exp(-np.arange(irl) / sr * 1.3)
    ir[:int(0.03 * sr)] *= np.linspace(0, 1, int(0.03 * sr))
    ir /= np.sqrt((ir ** 2).sum())
    wl = fftconvolve(mix, ir)[:N]; wr = fftconvolve(mix, np.roll(ir, 911))[:N]
    st = np.stack([0.5 * mix + 0.85 * wl, 0.5 * mix + 0.85 * wr], 1)
    fade = np.minimum(1, t / 1.5) * np.clip((total_s - t) / 3.0, 0, 1)
    st *= fade[:, None]
    return st / (np.abs(st).max() + 1e-9)


def load_music_file(path, total_s, boom_t=None, sr=44100, start_s=0.0):
    """Morceau fourni (sous licence) : bouclé si trop court, volume lissé, coupure d'une demi-seconde
    au « boum », fondus d'entrée/sortie. Renvoie (n, 2) avec un niveau moyen (RMS) d'environ 0,25."""
    import subprocess
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(start_s), '-i', path, '-ac', '2', '-ar', str(sr),
                        '-f', 's16le', '-'], capture_output=True, check=True)
    m = np.frombuffer(r.stdout, dtype=np.int16).astype(np.float64).reshape(-1, 2) / 32768
    N = int(total_s * sr)
    if len(m) < N:  # boucle avec fondu enchaîné de 2 s
        xf = int(2 * sr); out = m.copy()
        while len(out) < N:
            k = np.linspace(0, 1, xf)[:, None]
            out = np.concatenate([out[:-xf], out[-xf:] * (1 - k) + m[:xf] * k, m[xf:]])
        m = out
    m = m[:N]
    # lissage du volume : on rapproche chaque passage d'un niveau cible (gain borné)
    mono = np.abs(m).mean(1)
    w = int(1.5 * sr)
    rms = np.sqrt(np.convolve(mono ** 2, np.ones(w) / w, mode='same')) + 1e-6
    gain = np.clip(0.12 / rms, 0.5, 2.0)
    m = m * gain[:, None]
    t = np.arange(N) / sr
    if boom_t:
        gap = 1 - np.clip((t - (boom_t - 0.05)) / 0.05, 0, 1) * np.clip(((boom_t + 0.5) - t) / 0.08, 0, 1)
        m *= gap[:, None]
    fade = np.minimum(1, t / 1.0) * np.clip((total_s - t) / 2.5, 0, 1)
    m *= fade[:, None]
    return m / (np.sqrt((m ** 2).mean()) + 1e-9) * 0.25


if __name__ == '__main__':
    import sys, wave
    out = sys.argv[1] if len(sys.argv) > 1 else 'musique_test.wav'
    m = make_music(float(sys.argv[2]) if len(sys.argv) > 2 else 60, 25)
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100)
        w.writeframes((m * 0.8 * 32767).astype('<i2').tobytes())
    print(out)
