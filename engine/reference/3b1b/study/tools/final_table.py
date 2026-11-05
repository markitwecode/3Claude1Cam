"""Merge all metrics into data/final.json and print the markdown table rows."""
import json, statistics as st
from pathlib import Path
import numpy as np
S = Path(__file__).resolve().parent.parent / "data"
M = json.loads((S / "metrics.json").read_text())
D = {**json.loads((S / "density_A.json").read_text()), **json.loads((S / "density_B.json").read_text())}
I = json.loads((S / "ideas.json").read_text())
O = json.loads((S / "orig.json").read_text())
keys = ["la3", "calc2", "calc3", "calc5", "eipi", "de1", "de4", "clt", "l10ch2", "l10ch4", "l10ch6", "l12ch1"]
rows = {}
for k in keys:
    m = M[k]; r = dict(m)
    if k in D:
        tl = D[k]["tiles"]
        r["fl"] = st.mean(t["fl"] for t in tl)
        r["fl_max"] = max(t["fl"] for t in tl)
        r["prose"] = st.mean(t["prose"] for t in tl)
        r["pics"] = st.mean(t["pics"] for t in tl)
        cats = [t["cat"] for t in tl]
        for c in ("maths", "picture", "both", "prose", "pi", "blank"):
            r["cat_" + c] = cats.count(c) / len(cats)
        r["pic_share"] = (cats.count("picture") + cats.count("both")) / len(cats)
        r["new_pm"] = sum(t["new"] for t in tl) / (len(tl) / 6)
        life = D[k]["life_tiles"]
        r["life_med_s"] = float(np.median(life)) * 10 if life else float("nan")
        r["life_mean_s"] = float(np.mean(life)) * 10 if life else float("nan")
        r["fl_ge4"] = sum(t["fl"] >= 4 for t in tl) / len(tl)
    if k in I:
        t = I[k]["totals"]; mins = m["runtime"]
        for c in "FDCRMQ":
            r[c + "_pm"] = t[c] / mins
        ideas = t["F"] + t["D"] + t["C"]
        r["ideas_pm"] = ideas / mins
        r["support_per_idea"] = (t["R"] + t["M"]) / ideas
        r["words_per_idea"] = m["wpm_run"] * mins / ideas
        r["sec_per_idea"] = mins * 60 / ideas
    rows[k] = r
(S / "final.json").write_text(json.dumps(rows, indent=1))
cols = [("runtime", "{:.1f}"), ("wpm_run", "{:.0f}"), ("nospeech", "{:.0%}"), ("g1", "{:.1f}"), ("g2", "{:.1f}"), ("g4", "{:.2f}"),
        ("resets_pm", "{:.1f}"), ("reset_gap", "{:.0f}"), ("still_speaking", "{:.0%}"), ("motion_share", "{:.0%}"),
        ("fl", "{:.1f}"), ("pic_share", "{:.0%}"), ("life_med_s", "{:.0f}"), ("F_pm", "{:.1f}"), ("ideas_pm", "{:.1f}"),
        ("support_per_idea", "{:.2f}"), ("words_per_idea", "{:.0f}"), ("Q_pm", "{:.2f}")]
def fmt(r):
    return " | ".join(f.format(r[c]) if c in r and r[c] == r[c] else "–" for c, f in cols)
print("| video | " + " | ".join(c for c, _ in cols) + " |")
for k in keys:
    print(f"| {k} | " + fmt(rows[k]) + " |")
for name, ks in [("3b1b 2016–17", keys[:4]), ("3b1b 2019+", keys[4:8]), ("3b1b all", keys[:8]), ("ours", keys[8:])]:
    avg = {c: float(np.nanmean([rows[k].get(c, np.nan) for k in ks])) for c, _ in cols}
    print(f"| **{name}** | " + fmt(avg) + " |")
for k in O:
    o = O[k]
    print(k, "orig", round(o["runtime_min"], 1), round(o["wpm_runtime"]), f"{o['nospeech_share']:.0%}", round(o["gaps_ge1_per_min"], 1), round(o["gaps_ge2_per_min"], 1), round(o["gaps_ge4_per_min"], 2))
extra = ["fl_max", "fl_ge4", "prose", "pics", "cat_maths", "cat_picture", "cat_both", "cat_prose", "cat_pi", "cat_blank", "new_pm", "life_mean_s", "D_pm", "C_pm", "R_pm", "M_pm", "sec_per_idea"]
for k in keys:
    print(k, {c: round(rows[k][c], 2) for c in extra if c in rows[k]})
