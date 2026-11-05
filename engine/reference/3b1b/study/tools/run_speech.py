"""Mixed-track speech metrics, the same detector on both sides.

usage: python -I run_speech.py  (writes data/speech.json and data/<key>.speech.npy at REL = MAIN)
"""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import speech as S

STUDY = Path(__file__).resolve().parent.parent
THREE = ["la3", "calc2", "calc3", "calc5", "eipi", "de1", "de4", "clt"]
OURS = ["l10ch2", "l10ch4", "l10ch6", "l12ch1"]
RELS = (20, 25, 30)
MAIN = 20   # calibrated: on ours, REL 20 on the mixed track matches the clean-wav ground truth best


def run(key):
    if key in OURS:
        o = json.loads((STUDY / f"data/ours_{key}.json").read_text())
        media, spans, words, total = o["final"], o["spans"], o["words"], o["total"]
    else:
        media = STUDY / f"dl/{key}.mp4"
        spans, words = S.caption_spans(STUDY / f"dl/{key}.en.json3")
        total = None
    db = S.envelope(media)
    total = total or len(db) * S.HOP
    ref = S.ref_level(db)
    sm = S.span_mask(len(db), spans)
    out = {"ref_db": ref}
    for rel in RELS:
        a = S.clean((db > ref - rel) & sm)
        out[rel] = S.metrics(a, words, total)
        if rel == MAIN:
            np.save(STUDY / f"data/{key}.speech.npy", a)
    # unmasked, to show what the caption/clip mask removes
    out["nomask25"] = S.metrics(S.clean(db > ref - 25), words, total)
    return out


if __name__ == "__main__":
    keys = sys.argv[1:] or THREE + OURS
    res = {}
    p = STUDY / "data/speech.json"
    if p.exists():
        res = json.loads(p.read_text())
    for k in keys:
        res[k] = run(k)
        m = res[k][str(MAIN)] if str(MAIN) in res[k] else res[k][MAIN]
        print(k, {a: round(float(b), 3) for a, b in m.items()}, flush=True)
        p.write_text(json.dumps(res, indent=1, default=float))
