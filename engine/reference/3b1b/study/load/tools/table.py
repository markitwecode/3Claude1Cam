"""Final per-chapter table (mean of 2 coders; peaks = max 2-min window, step 5 s) incl. audited jumps."""
import json, re, statistics as st
from pathlib import Path
L = Path(__file__).resolve().parent.parent
GROUP = {"de10ch2": "ok", "de10ch4": "ok", "pil1": "ok", "pil2": "ok",
         "l10ch2": "dense", "l10ch4": "dense", "l10ch6": "dense", "l11ch1": "dense", "l12ch1": "?"}
W = lambda s: len(re.findall(r"[A-Za-z0-9']+", s))
def load(k):
    tx = json.loads((L / f"tx/{k}.json").read_text()); cs = []
    for f in sorted((L / "codes").glob(f"{k}.c*.json")):
        c = {s["i"]: s for s in json.loads(f.read_text())["sentences"]}; rs = []
        for s in tx["sentences"]:
            r = dict(t=s["t"], w=W(s["text"]), ideas=0, new=0, F=0, Fp=0, Dp=0, Q=0, Jc=int(bool(c[s["i"]].get("J"))))
            for u in c[s["i"]].get("u", []):
                u = u.strip()
                if not u: continue
                if u[0] in "FDC": r["ideas"] += 1; r["new"] += u.endswith("+")
                if u[0] == "F": r["F"] += 1; r["Fp"] += u.endswith("+")
                if u[0] == "D": r["Dp"] += u.endswith("+")
                if u[0] == "Q": r["Q"] += 1
            r["H"] = r["Fp"] + r["Dp"]; r["HQ"] = r["H"] - r["Q"]
            rs.append(r)
        cs.append(rs)
    ja = L / f"codes/{k}.jumps.json"
    aud = {j["i"]: j["J"] for j in json.loads(ja.read_text())["jumps"]} if ja.exists() else None
    for rs in cs:
        for r, s in zip(rs, tx["sentences"]):
            r["J"] = int(s["i"] in aud) if aud is not None else float("nan")
    return tx["total"], cs, aud
M = ["ideas", "new", "F", "Fp", "Dp", "H", "J", "Q", "HQ", "Jc"]
res = {}
for k in GROUP:
    T, cs, aud = load(k); mins = T / 60
    starts = [i * 5.0 for i in range(int((T - 120) / 5) + 1)]
    r = dict(group=GROUP[k], mins=mins, words=sum(x["w"] for x in cs[0]))
    for m in M:
        r[m] = st.mean(sum(x[m] for x in rs) for rs in cs) / mins
        wv = [st.mean(sum(x[m] for x in rs if a <= x["t"] < a + 120) for rs in cs) / 2 for a in starts]
        i = max(range(len(wv)), key=lambda j: wv[j]); r[m + "_pk"] = wv[i]; r[m + "_at"] = starts[i]
    ideas_tot = st.mean(sum(x["ideas"] for x in rs) for rs in cs)
    r["wpi"] = r["words"] / ideas_tot
    wp = []
    for a in starts:
        w = sum(x["w"] for x in cs[0] if a <= x["t"] < a + 120); n = st.mean(sum(x["ideas"] for x in rs if a <= x["t"] < a + 120) for rs in cs)
        wp.append(w / n if n else 999)
    r["wpi_pk"] = min(wp)
    r["J_n"] = len(aud) if aud is not None else None
    r["J_types"] = "".join(sorted(aud.values())) if aud else ""
    res[k] = r
(L / "table.json").write_text(json.dumps(res, indent=1))
f = lambda r, m, p=2: f"{r[m]:.{p}f} ({r[m + '_pk']:.1f})"
print("| ch | grp | min | ideas | new ideas | F | F+ | D+ | H=F+ +D+ | jumps | Q | H−Q | words/idea |")
for k, r in res.items():
    print(f"| {k} | {r['group']} | {r['mins']:.1f} | {f(r,'ideas',1)} | {f(r,'new',1)} | {f(r,'F')} | {f(r,'Fp')} | {f(r,'Dp')} | {f(r,'H')} @{int(r['H_at'])//60}:{int(r['H_at'])%60:02d} | {f(r,'J')} n={r['J_n']} | {f(r,'Q')} | {f(r,'HQ')} | {r['wpi']:.0f} ({r['wpi_pk']:.0f}) |")
ok = [k for k in res if GROUP[k] == "ok"]; dn = [k for k in res if GROUP[k] == "dense"]
for m in M + ["wpi"]:
    for suf in ("", "_pk"):
        if m == "wpi" and suf: continue
        key = m + suf
        a = [res[k][key] for k in ok]; b = [res[k][key] for k in dn]
        if any(x != x for x in a + b): continue
        auc = sum((y > x) + 0.5 * (y == x) for x in a for y in b) / 16
        print(f"{key:7s} ok {min(a):.2f}-{max(a):.2f} dense {min(b):.2f}-{max(b):.2f} AUC {auc:.2f} l12 {res['l12ch1'][key]:.2f}")
