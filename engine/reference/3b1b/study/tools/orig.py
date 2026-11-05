"""Reconstruct L10's ORIGINAL (pre-2026-11-03, fixed) pacing from audio/.pre-regap.

Assumes each scene was shorter by exactly the clips' duration change, i.e. the time between one
clip's end and the next clip's start (visual waits, scene joins) didn't change. Ground truth only
(clean wavs), REL 25 like ours.py.  usage: python -I orig.py <key>  (key: l10ch2, l10ch4, l10ch6)
"""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import speech as S

STUDY = Path(__file__).resolve().parent.parent

key = sys.argv[1]
o = json.loads((STUDY / f"data/ours_{key}.json").read_text())
proj = Path(o["final"]).parent.parent
pre = json.loads((proj / "audio/.pre-regap/manifest.json").read_text())
clips = o["clips"]
t, starts, durs = clips[0]["t0"], [], []
for i, c in enumerate(clips):
    starts.append(t)
    d0 = pre[c["id"]]["duration"]
    durs.append(d0)
    nxt = clips[i + 1]["t0"] if i + 1 < len(clips) else o["total"]
    t += d0 + (nxt - (c["t0"] + c["dur"]))
total = t
envs = [S.envelope(proj / "audio/.pre-regap" / Path(c["id"] + ".wav").name) for c in clips]
ref = S.ref_level(np.concatenate(envs))
a = np.zeros(int(total / S.HOP) + 1, bool)
for s, e in zip(starts, envs):
    i0 = int(s / S.HOP)
    seg = e > ref - 25
    j = min(len(a), i0 + len(seg))
    a[i0:j] |= seg[: j - i0]
m = S.metrics(S.clean(a), o["words"], total)
print(key, f"original {total/60:.2f} min vs now {o['total']/60:.2f}",
      {k: round(float(v), 3) for k, v in m.items()})
p = STUDY / "data/orig.json"
r = json.loads(p.read_text()) if p.exists() else {}
r[key] = m
p.write_text(json.dumps(r, indent=1, default=float))
