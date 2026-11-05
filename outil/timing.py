"""Cale les sous-titres d'un script Cerveau Minute sur sa voix off, sans modèle de transcription.

Usage : python3 timing.py script.json voix.mp3 spec_sortie.json

script.json = {"segments": [{"key": "...", "icon": "...", "hl": [...], "chunks": ["phrase dite", ...]}, ...]}
Chaque "chunk" est un morceau de phrase séparé par une pause audible (point, virgule forte, deux-points...).
On détecte les silences de la voix off avec ffmpeg, on garde les N-1 plus longs comme frontières
entre les N chunks, et on obtient le début et la fin de chaque chunk. Si l'audio ne contient pas
assez de pauses, on répartit le temps au prorata du nombre de caractères.
"""
import json, re, subprocess, sys

script_path, audio, out = sys.argv[1], sys.argv[2], sys.argv[3]
script = json.load(open(script_path))
chunks = [c for s in script["segments"] for c in s["chunks"]]
n = len(chunks)


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def silences(path, noise="-35dB", d=0.12):
    r = subprocess.run(["ffmpeg", "-i", path, "-af", f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"],
                       capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(starts, ends))


total = duration(audio)
sil = silences(audio)
# début et fin de la parole
speech_start = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
speech_end = sil[-1][0] if sil and sil[-1][1] >= total - 0.05 else total
inner = [s for s in sil if s[0] > speech_start + 0.1 and s[1] < speech_end - 0.1]

times = None
if n == 1:
    times = [(speech_start, speech_end)]
elif len(inner) >= n - 1:
    # position attendue de chaque frontière, au prorata des caractères
    tot = sum(len(c) for c in chunks)
    span = speech_end - speech_start
    exp, acc = [], 0
    for c in chunks[:-1]:
        acc += len(c)
        exp.append(speech_start + span * acc / tot)
    m = len(inner)
    mids = [(a + b) / 2 for a, b in inner]
    lens = [b - a for a, b in inner]
    # programmation dynamique : associer chaque frontière à une pause, dans l'ordre,
    # en minimisant l'écart à la position attendue et en favorisant les pauses longues
    INF = float("inf")
    cost = [[INF] * m for _ in range(n - 1)]
    prev = [[-1] * m for _ in range(n - 1)]
    for j in range(m):
        cost[0][j] = (mids[j] - exp[0]) ** 2 - 2.0 * lens[j]
    for i in range(1, n - 1):
        best, bj = INF, -1
        for j in range(m):
            if j > 0 and cost[i - 1][j - 1] < best:
                best, bj = cost[i - 1][j - 1], j - 1
            if bj >= 0:
                cost[i][j] = best + (mids[j] - exp[i]) ** 2 - 2.0 * lens[j]
                prev[i][j] = bj
    j = min(range(m), key=lambda k: cost[n - 2][k])
    if cost[n - 2][j] < INF:
        picks = [0] * (n - 1)
        for i in range(n - 2, -1, -1):
            picks[i] = j
            j = prev[i][j]
        bounds = [speech_start] + [x for k in picks for x in inner[k]] + [speech_end]
        times = [(bounds[2 * i], bounds[2 * i + 1]) for i in range(n)]

if times is None:
    span = speech_end - speech_start
    tot = sum(len(c) for c in chunks)
    t, times = speech_start, []
    for c in chunks:
        d = span * len(c) / tot
        times.append((t, t + d * 0.92))
        t += d
    print("répartition proportionnelle (pauses insuffisantes)", file=sys.stderr)

i = 0
spec = {"audio": audio, "segments": []}
for s in script["segments"]:
    seg = {k: s[k] for k in ("key", "icon", "hl")}
    seg["chunks"] = []
    for c in s["chunks"]:
        a, b = times[i]
        seg["chunks"].append([c, round(a, 2), round(b, 2)])
        i += 1
    spec["segments"].append(seg)
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print(out, "chunks:", n, "pauses:", len(inner), "durée:", round(total, 2))
