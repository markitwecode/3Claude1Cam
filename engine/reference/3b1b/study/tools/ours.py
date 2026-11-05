"""Our side: narration spans and a music-free ground truth from the clean clip wavs.

usage: python -I ours.py <project dir> <chapter N> <out json>
Read-only on the project. Scene order = sorted scenes/chN_*.py (as tools/render.py does);
scene offsets = cumulative durations of the rendered 1080p60 scene mp4s; clip start = cue start.
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import speech as S


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]))


def main(proj, n, out):
    proj = Path(proj)
    man = json.loads((proj / "audio/manifest.json").read_text())
    scenes = []
    for p in sorted((proj / "scenes").glob(f"ch{n}_*.py")):
        cls = re.search(r"^class (\w+)\(NarratedScene\)", p.read_text(), re.M).group(1)
        scenes.append((p.stem, cls))
    final = sorted((proj / "out").glob(f"ch{n}_*.mp4"))[0]
    total = dur(final)
    off, clips = 0.0, []
    for stem, cls in scenes:
        cue = json.loads((proj / f"media/cues/{stem}_1080p60.json").read_text())
        d = dur(proj / f"media/videos/{stem}/1080p60/{cls}.mp4")
        for c in cue["clips"]:
            m = man[c["id"]]
            clips.append(dict(id=c["id"], scene=stem, t0=off + c["start"], dur=m["duration"],
                              words=len(re.findall(S.WORD, m["text"])), file=str(proj / m["file"])))
        off += d
    nfr = int(total / S.HOP) + 1
    # ground truth: clean clip wavs, one reference level for the chapter
    envs = [S.envelope(c["file"]) for c in clips]
    ref = S.ref_level(np.concatenate(envs))
    gt = {}
    for rel in (20, 25, 30, 35):
        a = np.zeros(nfr, bool)
        for c, e in zip(clips, envs):
            i0 = int(c["t0"] / S.HOP)
            seg = e > ref - rel
            j = min(nfr, i0 + len(seg))
            a[i0:j] |= seg[: j - i0]
        gt[rel] = S.clean(a)
    words = sum(c["words"] for c in clips)
    spans = [(c["t0"], c["t0"] + c["dur"]) for c in clips]
    res = dict(final=str(final), total=total, scenes_sum=off, n_clips=len(clips), words=words,
               spans=spans, clips=[{k: c[k] for k in ("id", "scene", "t0", "dur", "words")} for c in clips],
               ground_truth={rel: S.metrics(a, words, total) for rel, a in gt.items()})
    np.save(Path(out).with_suffix(".gt25.npy"), gt[25])
    Path(out).write_text(json.dumps(res, indent=1))
    print(final.name, f"total {total:.1f} s, scenes {off:.1f} s, clips {len(clips)}, words {words}")
    for rel, m in res["ground_truth"].items():
        print(rel, {k: round(v, 3) for k, v in m.items()})


if __name__ == "__main__":
    main(*sys.argv[1:4])
