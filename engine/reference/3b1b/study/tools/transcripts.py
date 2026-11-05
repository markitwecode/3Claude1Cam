"""Timestamped transcripts (one line per caption cue / per sentence) into dl/transcripts/ (deleted with dl/)."""
import json, re
from pathlib import Path
STUDY = Path(__file__).resolve().parent.parent
OUT = STUDY / "dl/transcripts"
fmt = lambda t: f"{int(t)//60:02d}:{int(t)%60:02d}"
for k in ["la3", "calc2", "calc3", "calc5", "eipi", "de1", "de4", "clt"]:
    d = json.loads((STUDY / f"dl/{k}.en.json3").read_text())
    lines = []
    for e in d["events"]:
        t = "".join(s.get("utf8", "") for s in e.get("segs", [])).replace("\n", " ").strip()
        if t and "criblate" not in t:
            lines.append(f"[{fmt(e['tStartMs']/1000)}] {t}")
    (OUT / f"{k}.txt").write_text("\n".join(lines) + "\n")
for k in ["l10ch2", "l10ch4", "l10ch6", "l12ch1"]:
    o = json.loads((STUDY / f"data/ours_{k}.json").read_text())
    proj = Path(o["final"]).parent.parent
    man = json.loads((proj / "audio/manifest.json").read_text())
    lines = []
    for c in o["clips"]:
        words = man[c["id"]]["words"]
        cur, t0 = [], None
        for w, ts in words:
            if t0 is None:
                t0 = c["t0"] + ts
            cur.append(w)
            if re.search(r"[.?!]$", w):
                lines.append(f"[{fmt(t0)}] {' '.join(cur)}"); cur, t0 = [], None
        if cur:
            lines.append(f"[{fmt(t0)}] {' '.join(cur)}")
    (OUT / f"{k}.txt").write_text("\n".join(lines) + "\n")
print(sorted(p.name for p in OUT.iterdir()))
