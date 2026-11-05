"""Join speech (REL 20), word-gap and visual metrics into data/metrics.json and print a table."""
import json
from pathlib import Path
import numpy as np
STUDY = Path(__file__).resolve().parent.parent
SP = json.loads((STUDY / "data/speech.json").read_text())
WG = json.loads((STUDY / "data/wordgaps.json").read_text())
OR = json.loads((STUDY / "data/orig.json").read_text())
keys = ["la3", "calc2", "calc3", "calc5", "eipi", "de1", "de4", "clt", "l10ch2", "l10ch4", "l10ch6", "l12ch1"]
rows = {}
for k in keys:
    s = SP[k]["20"]
    v = np.load(STUDY / f"data/{k}.visual.npz")
    sp = np.load(STUDY / f"data/{k}.speech.npy")          # 20 ms frames
    n = len(v["ch1"])
    # speech per 0.5 s sample: voiced in >= half of the 25 frames
    m = min(n, len(sp) // 25)
    voiced = sp[: m * 25].reshape(m, 25).mean(1) >= 0.5
    still = v["ch1"][:m] < 0.002
    r = v["resets"]
    mins = n / 2 / 60
    row = dict(runtime=s["runtime_min"], wpm_speech=s["wpm_speech"], wpm_run=s["wpm_runtime"],
               nospeech=s["nospeech_share"], g1=s["gaps_ge1_per_min"], g2=s["gaps_ge2_per_min"],
               g4=s["gaps_ge4_per_min"], resets_pm=len(r) / mins,
               reset_gap=float(np.diff(r).mean() / 2) if len(r) > 1 else float("nan"),
               reset_gap_med=float(np.median(np.diff(r)) / 2) if len(r) > 1 else float("nan"),
               still_all=float(still.mean()), still_speaking=float(still[voiced].mean()),
               motion_share=float((v["ch1"][:m] > 0.05).mean()), ink=float(v["ink"].mean()))
    if k in WG:
        row.update(wg1=WG[k]["pauses_ge1_per_min"], wg2=WG[k]["pauses_ge2_per_min"])
    if k in OR:
        o = OR[k]
        row.update(orig_runtime=o["runtime_min"], orig_wpm_run=o["wpm_runtime"], orig_nospeech=o["nospeech_share"],
                   orig_g1=o["gaps_ge1_per_min"], orig_g2=o["gaps_ge2_per_min"], orig_g4=o["gaps_ge4_per_min"])
    rows[k] = row
(STUDY / "data/metrics.json").write_text(json.dumps(rows, indent=1))
cols = ["runtime", "wpm_speech", "wpm_run", "nospeech", "g1", "g2", "g4", "wg1", "wg2", "resets_pm", "reset_gap", "reset_gap_med", "still_all", "still_speaking", "motion_share", "ink"]
print("key     " + " ".join(f"{c[:9]:>9s}" for c in cols))
def pr(name, d):
    print(f"{name:8s}" + " ".join(f"{d.get(c, float('nan')):9.3f}" for c in cols))
for k in keys:
    pr(k, rows[k])
for name, ks in [("3b1b avg", keys[:8]), ("3b1b old", keys[:4]), ("3b1b 19+", keys[4:8]), ("ours avg", keys[8:])]:
    pr(name, {c: float(np.nanmean([rows[k].get(c, np.nan) for k in ks])) for c in cols})
for k in ["l10ch2", "l10ch4", "l10ch6"]:
    print(k, "orig", {c: round(v, 3) for c, v in rows[k].items() if c.startswith("orig")})
