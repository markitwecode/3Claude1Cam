"""Original-pacing runtime per chapter: total minus the summed change in clip length vs audio/.pre-regap."""
import json, subprocess, sys
from pathlib import Path
def dur(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]))
res = {}
for f in sorted(Path("tx").glob("*.json")):
    d = json.loads(f.read_text()); proj = Path(d["project"]); pre = proj/"audio/.pre-regap"
    delta, n = 0.0, 0
    for c in d["clips"]:
        w = pre/f"{c['id']}.wav"
        if w.exists():
            delta += c["dur"] - dur(w); n += 1
    res[d["key"]] = dict(total=d["total"], orig=d["total"]-delta, n_pre=n, n_clips=len(d["clips"]))
    print(d["key"], f"now {d['total']/60:.1f} min, pre-regap {(d['total']-delta)/60:.1f} min ({n}/{len(d['clips'])} clips)")
Path("tx/orig.json").write_text(json.dumps(res, indent=1))
