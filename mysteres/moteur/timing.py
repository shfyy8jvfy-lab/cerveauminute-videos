"""Construit timeline.json (mots, phrases, plans, annotations) à partir de plan.json.
Usage :
  python timing.py                -> estimation sans voix (débit de voix grave posée)
  python timing.py voice.mp3      -> calé sur la parole détectée dans la voix off
"""
import sys, re, json, subprocess

DELAY = 0.3          # décalage de la voix au mixage (s)
SYL_PER_S = 5.6      # débit estimé si pas encore de voix
plan = json.load(open("plan.json", encoding="utf-8"))


def syl(w):
    return (len(re.findall(r"[aeiouyéèêàâîïôûùœ]+", w.lower())) or 1) + 0.3


def pause(w):
    if re.search(r"[.…!?]$", w): return 2.4
    if re.search(r"[,:;]$", w): return 1.1
    return 0.0


words = []  # (mot, poids, pause, idx_phrase)
for i, s in enumerate(plan["sentences"]):
    for w in s["text"].split():
        words.append([w, syl(w), pause(w), i])
tot = sum(a + b for _, a, b, _ in words)

if len(sys.argv) > 1:
    voice = sys.argv[1]
    log = subprocess.run(["ffmpeg", "-i", voice, "-af", "silencedetect=n=-35dB:d=0.28", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "csv=p=0", voice]).strip())
    t0 = en[0] if st and st[0] < 0.05 and en else 0.0
    t1 = st[-1] if st and (not en or st[-1] > en[-1]) else total
else:
    t0, t1 = 0.0, tot / SYL_PER_S
    total = t1 + 0.2
t0 += DELAY; t1 += DELAY

k = (t1 - t0) / tot
t = t0
wt = []
for w, a, p, i in words:
    wt.append({"w": w, "s": round(t, 3), "e": round(t + a * k, 3), "i": i})
    t += (a + p) * k

# horodatages exacts issus de la transcription (words.json), si présents
import os
if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
    d = json.load(open(sys.argv[2], encoding="utf-8"))
    tw0 = [w for w in (d if isinstance(d, list) else d["words"]) if w.get("type", "word") == "word"]
    tw, inside = [], False  # retire les indications de jeu [....] éventuellement présentes
    for w in tw0:
        x = w["text"]
        if x.startswith("["): inside = True
        if not inside: tw.append(w)
        if x.endswith("]"): inside = False
    if len(tw) == len(wt):
        for x, y in zip(wt, tw):
            x["s"] = round(y["start"] + DELAY, 3); x["e"] = round(y["end"] + DELAY, 3)
        print("calage exact sur la transcription")
    else:
        # nombre de mots différent : on recale proportionnellement entre début et fin de parole
        a0, a1 = tw[0]["start"] + DELAY, tw[-1]["end"] + DELAY
        b0, b1 = wt[0]["s"], wt[-1]["e"]
        k2 = (a1 - a0) / max(b1 - b0, 1e-6)
        for x in wt:
            x["s"] = round(a0 + (x["s"] - b0) * k2, 3); x["e"] = round(a0 + (x["e"] - b0) * k2, 3)
        print("ATTENTION : transcription", len(tw), "mots vs script", len(wt), "-> calage approximatif")

sent = []
for i in range(len(plan["sentences"])):
    ws = [x for x in wt if x["i"] == i]
    sent.append([ws[0]["s"], ws[-1]["e"]])
# un plan commence au début de sa phrase (le premier dès 0)
bounds = [0.0] + [sent[i][0] for i in range(1, len(sent))] + [total + DELAY + 1.4]
shots, callouts = [], []
for i, s in enumerate(plan["sentences"]):
    a, b = bounds[i], bounds[i + 1]
    c = a
    for name, frac in s["shots"]:
        d = (b - a) * frac
        n = max(1, round(d / 4.6))  # coupe toutes les ~3 s, avec un nouvel angle de caméra
        for v in range(n):
            shots.append({"name": name, "v": v, "s": round(c + d * v / n, 3), "e": round(c + d * (v + 1) / n, 3)})
        c += (b - a) * frac
    for txt, f in s.get("callouts", []):
        ts = a + (b - a) * f
        callouts.append({"text": txt, "s": round(ts, 3), "e": round(min(b, ts + 2.6), 3)})
shots[-1]["e"] = bounds[-1]
out = {"duration": round(bounds[-1], 3), "words": wt, "shots": shots, "callouts": callouts}
json.dump(out, open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("durée", out["duration"], "s,", len(shots), "plans")
for s in shots:
    print(f'  {s["s"]:6.2f}-{s["e"]:6.2f}  {s["name"]}')
