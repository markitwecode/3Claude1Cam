"""Timestamped per-sentence transcript of one chapter, from manifest word timings + cue starts.
usage: python3 -I tx.py <project dir> <N> <key> <outdir>   (read-only on the project)"""
import json, re, subprocess, sys
from pathlib import Path
proj, n, key, outd = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
def dur(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]))
man = json.loads((proj/"audio/manifest.json").read_text())
cues = proj/"media/cues"
res = "1440p60" if any(cues.glob(f"ch{n}_*_1440p60.json")) else "1080p60"
off, sents, clips, scen = 0.0, [], [], []
for p in sorted((proj/"scenes").glob(f"ch{n}_*.py")):
    stem = p.stem
    cls = re.search(r"^class (\w+)\(NarratedScene\)", p.read_text(), re.M).group(1)
    cue = json.loads((cues/f"{stem}_{res}.json").read_text())
    vid = proj/f"media/videos/{stem}/{res}/{cls}.mp4"
    d = dur(vid) if vid.exists() else cue["duration"]
    scen.append(dict(stem=stem, t0=off, dur=d, cue_dur=cue["duration"]))
    for c in cue["clips"]:
        m = man[c["id"]]; t0c = off + c["start"]
        clips.append(dict(id=c["id"], scene=stem, t0=t0c, dur=m["duration"]))
        cur, ts0 = [], None
        for w, ts in m["words"]:
            if ts0 is None: ts0 = t0c + ts
            cur.append(w)
            if re.search(r"[.?!][\"'”)]*$", w):
                sents.append(dict(t=round(ts0,2), clip=c["id"], text=" ".join(cur))); cur, ts0 = [], None
        if cur: sents.append(dict(t=round(ts0,2), clip=c["id"], text=" ".join(cur)))
    off += d
final = sorted((proj/"out").glob(f"ch{n}_*.mp4"))
final = [f for f in final if "preview" not in f.name][0]
total = dur(final)
for i, s in enumerate(sents): s["i"] = i + 1
words = sum(len(re.findall(r"[A-Za-z0-9']+", s["text"])) for s in sents)
out = dict(key=key, project=str(proj), chapter=int(n), final=str(final), total=total, scenes_sum=off,
           words=words, scenes=scen, clips=clips, sentences=sents)
(outd/f"{key}.json").write_text(json.dumps(out, indent=1))
fmt = lambda t: f"{int(t)//60:02d}:{int(t)%60:02d}"
lines = [f"S{s['i']:03d} [{fmt(s['t'])}] ({s['clip']}) {s['text']}" for s in sents]
(outd/f"{key}.txt").write_text("\n".join(lines) + "\n")
print(f"{key}: total {total:.1f}s scenes {off:.1f}s sentences {len(sents)} words {words} wpm {words/total*60:.0f}")
