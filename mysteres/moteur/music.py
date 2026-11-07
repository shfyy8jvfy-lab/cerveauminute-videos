"""Musique originale : orgue lent et planant (ambiance « slowed »), arpège montant,
montée sur la révélation. Calée sur timeline.json.
Usage : python music.py music.wav
"""
import sys, json
import numpy as np
from scipy.signal import fftconvolve

SR = 44100
OUT = sys.argv[1] if len(sys.argv) > 1 else "music.wav"
TL = json.load(open("timeline.json", encoding="utf-8"))
DUR = TL["duration"] + 1.5
# repères : début de la révélation (« apparu ») et début de la conclusion
words = TL["words"]
T_REVEAL = next((w["s"] for w in words if w["w"].startswith("apparu")), DUR * 0.45)
T_OUTRO = next((w["s"] for w in reversed(words) if w["w"] == "Mais"), DUR - 6)

N = int(DUR * SR)
t = np.arange(N) / SR


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


# grille harmonique originale en la mineur (accords de 4,5 s, tempo très lent)
A, F, C, G, D, E = 57, 53, 48, 55, 50, 52
PROG = [
    (A, [57, 60, 64]), (F, [53, 57, 60]), (C, [55, 60, 64]), (G, [55, 59, 62]),
    (A, [57, 60, 64]), (F, [53, 57, 60]), (D, [53, 57, 62]), (E, [52, 56, 59]),
]
CH = 4.5


def organ(freq, n, att=1.4, rel=1.8):
    tt = np.arange(n) / SR
    out = np.zeros(n)
    for h, a in zip([1, 2, 3, 4, 6, 8], [1, .45, .3, .18, .1, .06]):
        for det in (-0.0012, 0.0012):
            out += a * np.sin(2 * np.pi * freq * h * (1 + det) * tt + h)
    env = np.minimum(1, tt / att) * np.minimum(1, (n / SR - tt) / rel)
    trem = 1 + 0.04 * np.sin(2 * np.pi * 0.25 * tt)
    return out * np.clip(env, 0, 1) * trem


mix = np.zeros(N)
pad = np.zeros(N)
arp = np.zeros(N)
k = 0
pos = 0.0
while pos < DUR:
    root, notes = PROG[k % len(PROG)]
    s0 = int(pos * SR); n = int((CH + 1.8) * SR)
    n = min(n, N - s0)
    if n <= 0: break
    seg = organ(midi(root - 24), n) * 0.9 + organ(midi(root - 12), n) * 0.6
    for m in notes:
        seg += organ(midi(m), n) * 0.35
    pad[s0:s0 + n] += seg
    # arpège : notes de l'accord, une demi-octave au-dessus, croches très lentes
    if pos >= 5.0:
        cyc = [notes[0] + 12, notes[1] + 12, notes[2] + 12, notes[1] + 24, notes[2] + 12, notes[1] + 12]
        step = 0.5625
        for j in range(int(CH / step)):
            ts = pos + j * step
            a0 = int(ts * SR); ln = int(1.6 * SR)
            if a0 + ln > N: break
            tt = np.arange(ln) / SR
            f = midi(cyc[j % len(cyc)])
            tone = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 2.6)
            tone *= np.minimum(1, tt / 0.01)
            arp[a0:a0 + ln] += tone
    pos += CH; k += 1

# sub-basse : souffle grave qui enfle à la révélation
sub = np.sin(2 * np.pi * 36.7 * t) * 0.6


def ramp(x0, x1):
    return np.clip((t - x0) / max(x1 - x0, 1e-3), 0, 1)


# dynamique : intro calme -> montée jusqu'à la révélation -> plateau -> outro dépouillée
pad_env = 0.55 + 0.45 * ramp(0, T_REVEAL)
pad_env *= 1 - 0.45 * ramp(T_OUTRO - 1, T_OUTRO + 2)
arp_env = 0.25 + 0.75 * ramp(5, T_REVEAL)
arp_env *= 1 - ramp(T_OUTRO - 2, T_OUTRO + 1)
sub_env = 0.3 + 0.7 * np.exp(-((t - T_REVEAL) / 3.0) ** 2) + 0.4 * ramp(T_OUTRO, DUR)
mix = pad * pad_env * 0.11 + arp * arp_env * 0.10 + sub * sub_env * 0.18

# réverbération de grande salle (réponse impulsionnelle synthétique, 4 s)
rng = np.random.default_rng(1)
irl = int(4.0 * SR)
ir = rng.standard_normal(irl) * np.exp(-np.arange(irl) / SR * 1.6)
ir[:int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
ir /= np.sqrt((ir ** 2).sum())
wetL = fftconvolve(mix, ir)[:N]
ir2 = np.roll(ir, 347)
wetR = fftconvolve(mix, ir2)[:N]
L = 0.55 * mix + 0.8 * wetL
R = 0.55 * mix + 0.8 * wetR
st = np.stack([L, R], 1)
# fondus d'entrée et de sortie
fade = np.minimum(1, t / 2.0) * np.clip((DUR - t) / 3.0, 0, 1)
st *= fade[:, None]
st /= np.abs(st).max() + 1e-9
st *= 0.8
import wave
with wave.open(OUT, "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((st * 32767).astype("<i2").tobytes())
print("ok", OUT, round(DUR, 1), "s | révélation", round(T_REVEAL, 1), "| outro", round(T_OUTRO, 1))
