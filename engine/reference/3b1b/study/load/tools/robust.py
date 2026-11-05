"""Robustness of candidate measures: all 2^9 one-coder-per-chapter picks, leave-one-out, and 2-min peaks."""
import json, re, itertools, statistics as st
from pathlib import Path
import importlib.util
L = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("an", L / "tools/analyse.py")
GROUP = {"de10ch2": "ok", "de10ch4": "ok", "pil1": "ok", "pil2": "ok",
         "l10ch2": "dense", "l10ch4": "dense", "l10ch6": "dense", "l11ch1": "dense", "l12ch1": "?"}
W = lambda s: len(re.findall(r"[A-Za-z0-9']+", s))
def rows(k, f):
    tx = json.loads((L / f"tx/{k}.json").read_text()); c = json.loads(f.read_text())
    byi = {s["i"]: s for s in c["sentences"]}; out = []
    for s in tx["sentences"]:
        u = byi[s["i"]].get("u", []); j = byi[s["i"]].get("J", "") or ""
        r = dict(t=s["t"], w=W(s["text"]), F=0, Fp=0, Dp=0, Cp=0, Q=0, R=0, M=0, J=int(bool(j)))
        for t in u:
            t = t.strip()
            if not t: continue
            if t[0] == "F": r["F"] += 1; r["Fp"] += t.endswith("+")
            if t[0] == "D": r["Dp"] += t.endswith("+")
            if t[0] == "C": r["Cp"] += t.endswith("+")
            if t[0] in "QRM": r[t[0]] += 1
        out.append(r)
    return tx["total"], out
data = {k: [rows(k, f) for f in sorted((L / "codes").glob(f"{k}.c*.json"))] for k in GROUP}
MEAS = {
  "F": lambda r: r["F"], "F+": lambda r: r["Fp"], "F+ +D+": lambda r: r["Fp"] + r["Dp"],
  "F+ -Q": lambda r: r["Fp"] - r["Q"], "F+ -0.5Q": lambda r: r["Fp"] - 0.5 * r["Q"],
  "F+ +J -Q": lambda r: r["Fp"] + r["J"] - r["Q"], "F -Q": lambda r: r["F"] - r["Q"],
  "F+ +D+ -Q": lambda r: r["Fp"] + r["Dp"] - r["Q"], "new": lambda r: r["Fp"] + r["Dp"] + r["Cp"],
  "Q": lambda r: -r["Q"],
}
def rate(k, ci, m):
    T, rs = data[k][ci]; return sum(MEAS[m](r) for r in rs) / (T / 60)
def auc(v):
    ok = [v[k] for k in v if GROUP[k] == "ok"]; dn = [v[k] for k in v if GROUP[k] == "dense"]
    return sum((y > x) + 0.5 * (y == x) for x in ok for y in dn) / 16, min(dn) - max(ok)
lab = [k for k in GROUP if GROUP[k] != "?"]
print("measure      AUC(mean) gap | share of 256 coder picks with AUC=1 | min AUC over picks | LOO thresholds")
for m in MEAS:
    mean = {k: st.mean(rate(k, c, m) for c in (0, 1)) for k in lab}
    a, g = auc(mean)
    picks = [auc({k: rate(k, c, m) for k, c in zip(lab, combo)}) for combo in itertools.product((0, 1), repeat=len(lab))]
    full = sum(p[0] == 1 for p in picks) / len(picks); mn = min(p[0] for p in picks)
    # leave one out: threshold = midpoint of the gap on the remaining 7, does the left-out one fall on its side?
    hits = 0
    for out in lab:
        rest = {k: mean[k] for k in lab if k != out}
        ok = [rest[k] for k in rest if GROUP[k] == "ok"]; dn = [rest[k] for k in rest if GROUP[k] == "dense"]
        thr = (max(ok) + min(dn)) / 2
        hits += (mean[out] > thr) == (GROUP[out] == "dense")
    l12 = st.mean(rate("l12ch1", c, m) for c in (0, 1))
    print(f"{m:11s} {a:.2f} {g:+.2f} | {full:.0%} | {mn:.2f} | LOO {hits}/8 | l12ch1 {l12:.2f}")
# per chapter values and 2-min peaks for the chosen measures (mean of coders, windows on sentence starts)
print()
for m in ["F", "F+", "F+ -Q", "Q"]:
    line = []
    for k in GROUP:
        T = data[k][0][0]; starts = [i * 5.0 for i in range(int((T - 120) / 5) + 1)]
        wv = [st.mean(sum(MEAS[m](r) for r in data[k][c][1] if a <= r["t"] < a + 120) for c in (0, 1)) / 2 for a in starts]
        i = max(range(len(wv)), key=lambda j: wv[j]) if m != "Q" else min(range(len(wv)), key=lambda j: wv[j])
        line.append(f"{k} {st.mean(rate(k, c, m) for c in (0, 1)):.2f}/pk {wv[i]:.2f}@{int(starts[i])//60}:{int(starts[i])%60:02d}")
    print(m, " | ".join(line))
