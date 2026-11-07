"""Monte le reel à partir de timeline.json.
Usage : python assemble.py visual.mp4 out.mp4 voice.mp3 [music.wav]
Sans voix : nappe sonore + sous-titres seuls (aperçu du rythme).
"""
import sys, json, re, subprocess

visual, out = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else None
TL = json.load(open("timeline.json", encoding="utf-8"))
D = TL["duration"]


def ts(x):
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


# blocs de 1 à 3 mots, coupés à la ponctuation
chunks, cur = [], []
for w in TL["words"]:
    cur.append(w)
    if len(cur) == 3 or re.search(r"[,.…!?:]$", w["w"]):
        chunks.append(cur); cur = []
if cur: chunks.append(cur)

L = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 0", "",
     "[V4+ Styles]",
     "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
     "Style: Sub,Inter,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,6,0,5,70,70,0,1",
     "Style: Call,Inter,100,&H0045C8FF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,4,0,1,4,0,5,60,60,0,1",
     "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for i, ch in enumerate(chunks):
    end = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else ch[-1]["e"] + 0.5
    end = min(end, ch[-1]["e"] + 0.6)
    for k, w in enumerate(ch):
        we = ch[k + 1]["s"] if k + 1 < len(ch) else end
        parts = [("{\\c&H45C8FF&}" + x["w"].rstrip(",.:") + "{\\c&HFFFFFF&}") if j == k else x["w"].rstrip(",.:")
                 for j, x in enumerate(ch)]
        L.append(f"Dialogue: 0,{ts(w['s'])},{ts(we)},Sub,,0,0,0,,{{\\pos(540,1340)}}" + " ".join(parts).upper())
for c in TL["callouts"]:
    L.append(f"Dialogue: 1,{ts(c['s'])},{ts(c['e'])},Call,,0,0,0,,{{\\pos(540,330)\\fad(150,200)\\t(0,250,\\fscx100\\fscy100)\\fscx70\\fscy70}}{c['text']}")
open("subs.ass", "w", encoding="utf-8").write("\n".join(L) + "\n")

music = sys.argv[4] if len(sys.argv) > 4 else None
inputs = ["-i", visual, "-i", voice]
if music:
    inputs += ["-i", music]
    # musique baissée automatiquement quand la voix parle (sidechain)
    fc = ("[1]adelay=300|300,highpass=f=60,acompressor=threshold=-18dB:ratio=3,volume=1.4,asplit=2[v][vk];"
          "[2]volume=0.55[m];"
          "[m][vk]sidechaincompress=threshold=0.03:ratio=5:attack=40:release=600:makeup=1[md];"
          "[v][md]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a];")
else:
    fc = ("[1]adelay=300|300,highpass=f=60,acompressor=threshold=-18dB:ratio=3,volume=1.4,"
          "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a];")
fc += f"[0]trim=0:{D},setpts=PTS-STARTPTS,ass=subs.ass[vid]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fc,
                "-map", "[vid]", "-map", "[a]", "-t", str(D), "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out],
               check=True)
print("ok", out)
