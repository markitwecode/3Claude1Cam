"""Load per minute: chapter rates, 2-min sliding windows, coder agreement, group separation.
usage: python3 -I tools/analyse.py   (run from the load/ folder)"""
import json, re, itertools, statistics as st
from pathlib import Path
L = Path(__file__).resolve().parent.parent
TX, CO = L / "tx", L / "codes"
GROUP = {"de10ch2": "ok", "de10ch4": "ok", "pil1": "ok", "pil2": "ok",
         "l10ch2": "dense", "l10ch4": "dense", "l10ch6": "dense", "l11ch1": "dense", "l12ch1": "?"}
KEYS = list(GROUP)
ORIG = json.loads((L / "tx/orig.json").read_text())
IDEAS0 = json.loads(Path("/Users/markgolbraikh/Documents/3Claude1Cam/engine/reference/3b1b/study/data/ideas.json").read_text())
WIN, STEP = 120.0, 5.0
W = lambda s: len(re.findall(r"[A-Za-z0-9']+", s))

def per_sentence(sents, code):
    """-> list of dicts of unit counts per sentence for one coder."""
    rows = []
    byi = {c["i"]: c for c in code["sentences"]}
    for s in sents:
        c = byi.get(s["i"], {"u": [], "J": ""})
        u = c.get("u", []); j = c.get("J", "") or ""
        r = {k: 0 for k in ["F", "D", "C", "R", "M", "Q", "F+", "D+", "C+", "J", "Js", "Jm", "Jf"]}
        for t in u:
            t = t.strip()
            if not t: continue
            r[t[0]] = r.get(t[0], 0) + 1
            if t[0] in "FDC" and t.endswith("+"): r[t[0] + "+"] += 1
        if j:
            r["J"] = 1; r["Js"] = int("s" in j); r["Jm"] = int("m" in j); r["Jf"] = int("f" in j)
        r["ideas"] = r["F"] + r["D"] + r["C"]; r["new"] = r["F+"] + r["D+"] + r["C+"]
        r["t"] = s["t"]; r["w"] = W(s["text"])
        rows.append(r)
    return rows

MEAS = ["ideas", "new", "F", "F+", "J", "Js", "Jm", "R", "M", "Q"]
out, agree = {}, {}
for k in KEYS:
    tx = json.loads((TX / f"{k}.json").read_text())
    files = sorted(CO.glob(f"{k}.c*.json"))
    if not files: continue
    codes = [json.loads(f.read_text()) for f in files]
    ps = [per_sentence(tx["sentences"], c) for c in codes]
    mins = tx["total"] / 60
    words = sum(W(s["text"]) for s in tx["sentences"])
    tot = [{m: sum(r[m] for r in p) for m in MEAS + ["D", "C", "D+", "C+", "Jf"]} for p in ps]
    mean = {m: st.mean(t[m] for t in tot) for m in tot[0]}
    rec = dict(group=GROUP[k], mins=mins, orig_mins=ORIG[k]["orig"] / 60, words=words, wpm=words / mins,
               n_coders=len(ps), coders=[c["coder"] for c in codes], totals=mean, per_coder=tot)
    for m in MEAS: rec[m + "_pm"] = mean[m] / mins
    rec["words_per_idea"] = words / mean["ideas"]
    rec["words_per_new"] = words / mean["new"] if mean["new"] else float("nan")
    rec["new_share"] = mean["new"] / mean["ideas"]
    # sliding 2-min windows on the mean of the coders
    T = tx["total"]; starts = [i * STEP for i in range(int((T - WIN) / STEP) + 1)]
    win = {m: [] for m in MEAS + ["wpi"]}
    for a in starts:
        sel = [[r for r in p if a <= r["t"] < a + WIN] for p in ps]
        for m in MEAS:
            win[m].append(st.mean(sum(r[m] for r in s) for s in sel) / (WIN / 60))
        wsum = sum(r["w"] for r in sel[0]); idm = st.mean(sum(r["ideas"] for r in s) for s in sel)
        win["wpi"].append(wsum / idm if idm else float("inf"))
    for m in MEAS:
        i = max(range(len(starts)), key=lambda j: win[m][j])
        rec[m + "_peak"] = win[m][i]; rec[m + "_peak_at"] = starts[i]
    rec["wpi_peak"] = min(win["wpi"])
    rec["windows"] = {m: win[m] for m in ["new", "J", "ideas", "F+"]}; rec["win_starts"] = starts
    # agreement between the two coders
    if len(ps) == 2:
        a, b = ps
        ja = [r["J"] for r in a]; jb = [r["J"] for r in b]
        n = len(ja); po = sum(x == y for x, y in zip(ja, jb)) / n
        pa, pb = sum(ja) / n, sum(jb) / n; pe = pa * pb + (1 - pa) * (1 - pb)
        # +-1 sentence tolerance: a jump of one coder matched by a jump of the other within 1 sentence
        hits = sum(1 for i, x in enumerate(ja) if x and any(jb[j] for j in range(max(0, i - 1), min(n, i + 2))))
        hitsb = sum(1 for i, x in enumerate(jb) if x and any(ja[j] for j in range(max(0, i - 1), min(n, i + 2))))
        agree[k] = dict(J=(tot[0]["J"], tot[1]["J"]), kappa=(po - pe) / (1 - pe) if pe < 1 else float("nan"),
                        J_match_pm1=(hits, hitsb), ideas=(tot[0]["ideas"], tot[1]["ideas"]),
                        new=(tot[0]["new"], tot[1]["new"]), F=(tot[0]["F"], tot[1]["F"]))
    out[k] = rec

(L / "results.json").write_text(json.dumps(dict(chapters=out, agree=agree), indent=1))

def row(k, r):
    return (f"{k:8s} {r['group']:5s} {r['mins']:5.1f} {r['wpm']:4.0f} | ideas {r['ideas_pm']:4.2f} new {r['new_pm']:4.2f} "
            f"F {r['F_pm']:4.2f} F+ {r['F+_pm']:4.2f} J {r['J_pm']:4.2f} (s {r['Js_pm']:.2f} m {r['Jm_pm']:.2f}) "
            f"w/idea {r['words_per_idea']:3.0f} w/new {r['words_per_new']:3.0f} new% {r['new_share']:.0%} M {r['M_pm']:.2f} Q {r['Q_pm']:.2f} "
            f"| peak ideas {r['ideas_peak']:.1f} new {r['new_peak']:.1f} F+ {r['F+_peak']:.1f} J {r['J_peak']:.1f} wpi {r['wpi_peak']:.0f} n={r['n_coders']}")
for k, r in out.items(): print(row(k, r))
print("\nagreement:")
for k, a in agree.items(): print(k, a)
print("\nvs original coder (totals F D C R M Q; new coders' mean):")
for k in ["l10ch2", "l10ch4", "l10ch6", "l12ch1"]:
    if k in out:
        o = IDEAS0[k]["totals"]; n = out[k]["totals"]
        print(k, "orig", [o[c] for c in "FDCRMQ"], "ideas", o["F"] + o["D"] + o["C"], "| new", [round(n[c], 1) for c in "FDCRMQ"], "ideas", round(n["ideas"], 1))

# separation: AUC (ok < dense) and margin, per measure (chapter and peak); LOO not needed for AUC
ok = [k for k in out if GROUP[k] == "ok"]; dn = [k for k in out if GROUP[k] == "dense"]
def sep(vals):
    a = [vals[k] for k in ok]; b = [vals[k] for k in dn]
    auc = sum((y > x) + 0.5 * (y == x) for x in a for y in b) / (len(a) * len(b))
    gap = min(b) - max(a)
    mid = (min(b) + max(a)) / 2
    sd = st.pstdev(a + b) or 1
    return auc, gap, gap / sd, mid, (min(a), max(a)), (min(b), max(b))
cands = {}
for m in MEAS:
    cands[m + "_pm"] = {k: out[k][m + "_pm"] for k in out}
    cands[m + "_peak"] = {k: out[k][m + "_peak"] for k in out}
cands["ideas_per100w"] = {k: 100 / out[k]["words_per_idea"] for k in out}
cands["new_per100w"] = {k: 100 / out[k]["words_per_new"] for k in out}
cands["J_per100w"] = {k: out[k]["totals"]["J"] / out[k]["words"] * 100 for k in out}
cands["new_share"] = {k: out[k]["new_share"] for k in out}
for w in (0.5, 1, 2, 3):
    cands[f"new+{w}J_pm"] = {k: out[k]["new_pm"] + w * out[k]["J_pm"] for k in out}
    cands[f"new+{w}J_peak"] = {}
    for k in out:
        nw, jw = out[k]["windows"]["new"], out[k]["windows"]["J"]
        cands[f"new+{w}J_peak"][k] = max(x + w * y for x, y in zip(nw, jw))
    cands[f"F+ +{w}J_pm"] = {k: out[k]["F+_pm"] + w * out[k]["J_pm"] for k in out}
cands["neg_wpi_peak"] = {k: -out[k]["wpi_peak"] for k in out}
cands["neg_M_per_idea"] = {k: -out[k]["totals"]["M"] / out[k]["totals"]["ideas"] for k in out}
if ok and dn:
    print("\nseparation (AUC, gap, gap/sd, threshold, ok range, dense range, l12ch1):")
    res = []
    for name, v in cands.items():
        auc, gap, gsd, mid, ra, rb = sep(v)
        res.append((auc, gsd, name, gap, mid, ra, rb, v.get("l12ch1")))
    for auc, gsd, name, gap, mid, ra, rb, l12 in sorted(res, key=lambda x: (-x[0], -x[1])):
        print(f"{name:16s} AUC {auc:.2f} gap {gap:+.2f} gap/sd {gsd:+.2f} thr {mid:.2f} ok {ra[0]:.2f}-{ra[1]:.2f} dense {rb[0]:.2f}-{rb[1]:.2f} l12 {l12 if l12 is None else round(l12, 2)}")
    (L / "separation.json").write_text(json.dumps({n: v for n, v in cands.items()}, indent=1))
