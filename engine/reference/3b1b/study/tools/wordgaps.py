"""Second, music-independent pause measure: gaps between consecutive word START times.

3b1b: YouTube auto-caption word timings (json3 tOffsetMs, or vtt <hh:mm:ss.mmm><c> tags).
Ours: audio/manifest.json word starts placed on the video timeline (data/ours_<key>.json clips).
A pause of >= T s is counted when next_start - start >= T + 0.30 s (0.30 s ~ one word's
articulation at ~200 wpm), so this approximates silences, not exact ones.
usage: python -I wordgaps.py  -> data/wordgaps.json
"""
import json, re, sys
from pathlib import Path
import numpy as np

STUDY = Path(__file__).resolve().parent.parent
WD = 0.30


def auto_starts(key):
    j = STUDY / f"dl/{key}.auto.en.json3"
    if j.exists():
        d = json.loads(j.read_text())
        st = []
        for e in d["events"]:
            for s in e.get("segs", []):
                if s.get("utf8", "").strip():
                    st.append((e["tStartMs"] + s.get("tOffsetMs", 0)) / 1000)
        return sorted(set(st))
    txt = (STUDY / f"dl/{key}.auto.en.vtt").read_text()
    st = []
    ts = lambda h, m, s: int(h) * 3600 + int(m) * 60 + float(s)
    for block in txt.split("\n\n"):
        m = re.match(r"(\d+):(\d+):([\d.]+) --> ", block)
        if not m or "<c>" not in block:
            continue
        st.append(ts(*m.groups()))
        st += [ts(*t) for t in re.findall(r"<(\d+):(\d+):([\d.]+)><c>", block)]
    return sorted(set(st))


def our_starts(key, proj_root="/Users/markgolbraikh/Documents/3Claude1Cam/projects/nst-maths"):
    o = json.loads((STUDY / f"data/ours_{key}.json").read_text())
    proj = Path(o["final"]).parent.parent
    man = json.loads((proj / "audio/manifest.json").read_text())
    st = []
    for c in o["clips"]:
        st += [c["t0"] + w[1] for w in man[c["id"]]["words"]]
    return sorted(st)


def stats(st):
    st = np.array(st)
    g = np.diff(st)
    span = (st[-1] - st[0]) / 60
    out = {"words_timed": len(st), "span_min": span}
    for t in (1, 2, 4):
        out[f"pauses_ge{t}_per_min"] = float((g >= t + WD).sum() / span)
    out["pause_time_share"] = float(np.clip(g - WD, 0, None)[g >= 0.3 + WD].sum() / (span * 60))
    return out


if __name__ == "__main__":
    res = {}
    for k in ["la3", "calc2", "calc3", "calc5", "eipi", "de1", "de4", "clt"]:
        st = auto_starts(k)
        if len(st) > 100:
            res[k] = stats(st)
    for k in ["l10ch2", "l10ch4", "l10ch6", "l12ch1"]:
        res[k] = stats(our_starts(k))
    for k, v in res.items():
        print(f"{k:7s}", {a: round(b, 3) for a, b in v.items()})
    (STUDY / "data/wordgaps.json").write_text(json.dumps(res, indent=1))
