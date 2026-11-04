"""Finish chapters without an agent: final render and format check, plus Gemini's transitions
review only when asked (--review); one short summary per chapter. Run by the producer once a chapter-director
reports "ready for final" (since 2026-11-01: finals and their reviews need no hot cache, so no
agent waits through them).

    vk finalize 3 4              # final render + format check, chapter after chapter (no Gemini)
    vk finalize 3 --review       # also Gemini's transitions pass (off by default since 2026-11-04:
                                 # a 5-chapter sample found 1 minor real finding; docs/LESSONS.md)
    vk finalize 3 --with-viewer  # the transitions pass and the viewer pass
    vk finalize 3 --no-review    # same as the default; kept for old notes and scripts

Renders run one chapter at a time (each already uses every core, at low CPU priority, see
render.py); a chapter's two reviews run while the next chapter renders. Writes
media/review/chN_finalize.md and prints it. The verdict is "clean" when no finding is a
pronunciation or a settled (not mid-transition) visual problem of medium or high severity;
(the ~0.7 s join hold at the start of s1 excepted);
otherwise "look", and a chapter-director fix pass gets chN_review.md and chN_transitions.md as notes.
"""
import argparse
import json
import subprocess
import sys
import threading
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
from lib.paths import final_quality, project  # noqa: E402

ROOT = project()
VK = ENGINE / "vk"
REVIEW = ROOT / "media" / "review"


def out_video(n):
    hits = [p for p in sorted((ROOT / "out").glob(f"ch{n}_*.mp4")) if not p.stem.endswith("_preview")]
    return hits[0] if hits else None


def probe(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(video)],
                       capture_output=True, text=True)
    try:
        j = json.loads(r.stdout)
        s, f = j["streams"][0], j["format"]
        num, den = s["r_frame_rate"].split("/")
        return int(s["width"]), int(s["height"]), round(int(num) / int(den)), float(f["duration"])
    except (KeyError, IndexError, ValueError, json.JSONDecodeError):
        return None


def tally(path):
    """(line for the summary, number of findings that need a look) for one review JSON."""
    if not path.exists():
        return f"{path.name}: missing (review failed?)", 1
    findings = json.loads(path.read_text()).get("findings", [])
    def join_hold(f):   # s1 opens on the previous chapter's end card for ~0.7 s, on purpose
        return "_s1_" in str(f.get("scene", "")) and float(f.get("scene_time") or 0) < 1.0
    look = [f for f in findings if not join_hold(f) and (f.get("kind") == "pronunciation"
            or (not f.get("moving") and f.get("severity") in ("medium", "high")))]
    moving = sum(bool(f.get("moving")) for f in findings)
    return (f"{path.name}: {len(findings)} findings ({moving} mid-transition); "
            f"{len(look)} to look at" + (": " + "; ".join(
                f"{f.get('scene')} @ {f.get('scene_time', 0):.1f} s [{f.get('kind')}] {f.get('observed', '')[:70]}"
                for f in look[:6]) if look else "")), len(look)


def render(n):
    log = ROOT / "media" / "logs" / f"ch{n}_finalize_render.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([str(VK), "final", str(n)], cwd=ROOT, capture_output=True, text=True)
    log.write_text(r.stdout + r.stderr)
    handovers = [ln for ln in r.stdout.splitlines() if ln.startswith("handover MISMATCH")]
    return r.returncode, handovers, log


def review(n, extra, sink):
    r = subprocess.run([str(VK), "review", str(n), *extra], cwd=ROOT, capture_output=True, text=True)
    sink[tuple(extra)] = r.returncode


def summarise(n, rc, handovers, log, reviews, transitions_only=False):
    video = out_video(n)
    lines = [f"# Chapter {n}: finalize"]
    if rc or not video:
        lines.append(f"FAILED: vk final {n} exited {rc}; log {log.relative_to(ROOT)}")
        return "\n".join(lines), "failed"
    fmt = probe(video)
    if fmt:
        w, h, fps, dur = fmt
        ew, eh, efps = final_quality()[2]
        ok = (w, h, fps) == (ew, eh, efps)
        lines.append(f"{video.relative_to(ROOT)}: {int(dur // 60)}:{dur % 60:04.1f}, {w}×{h} at {fps} fps"
                     + ("" if ok else f"  (NOT {ew}×{eh} at {efps} fps)"))
    else:
        ok = False
        lines.append(f"{video.relative_to(ROOT)}: ffprobe failed")
    lines += [f"{h}" for h in handovers] or ["handovers: all ok"]
    need = 0 if ok else 1
    if reviews is None:
        lines.append("reviews: skipped (--no-review, or Gemini is off)")
    else:
        passes = (((), f"ch{n}_review.json"), (("--transitions",), f"ch{n}_transitions.json"))
        for extra, name in (passes[1:] if transitions_only else passes):
            if reviews.get(extra):
                lines.append(f"{name}: vk review exited {reviews[extra]}")
                need += 1
                continue
            line, k = tally(REVIEW / name)
            lines.append(line)
            need += k
    verdict = "clean" if need == 0 else "look"
    lines.append(f"verdict: {verdict}")
    return "\n".join(lines), verdict


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("chapters", type=int, nargs="+")
    ap.add_argument("--review", action="store_true",
                    help="also Gemini's transitions pass (off by default since 2026-11-04)")
    ap.add_argument("--no-review", action="store_true", help="no Gemini review (the default; kept for old notes)")
    ap.add_argument("--with-viewer", action="store_true",
                    help="Gemini's transitions and viewer passes (the viewer pass rarely led to a fix in L10)")
    args = ap.parse_args()
    if not (args.review or args.with_viewer):
        args.no_review = True
    REVIEW.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(ENGINE / "tools"))
    import gemini
    off = gemini.off_reason()
    if off and not args.no_review:
        print(f"Gemini is off ({off}): rendering without the review", flush=True)
        args.no_review = True
    pending = []        # (n, rc, handovers, log, thread or None, sink)
    for n in args.chapters:
        print(f"ch{n}: final render…", flush=True)
        rc, handovers, log = render(n)
        if not rc and out_video(n):
            # the 480p review previews have done their job; `vk preview N` remakes one if needed
            for p in (ROOT / "out").glob(f"ch{n}_*_preview.*"):
                p.unlink()
        sink, threads = {}, []
        if not rc and not args.no_review and out_video(n):
            for extra in (((), ("--transitions",)) if args.with_viewer else (("--transitions",),)):
                t = threading.Thread(target=review, args=(n, list(extra), sink))
                t.start()
                threads.append(t)
        pending.append((n, rc, handovers, log, threads, sink))
    verdicts = {}
    for n, rc, handovers, log, threads, sink in pending:
        for t in threads:
            t.join()
        reviews = None if args.no_review else {tuple(k): v for k, v in sink.items()}
        text, verdicts[n] = summarise(n, rc, handovers, log, reviews, not args.with_viewer)
        (REVIEW / f"ch{n}_finalize.md").write_text(text + "\n")
        print(text + "\n", flush=True)
    print("verdicts: " + ", ".join(f"ch{n} {v}" for n, v in verdicts.items()))
    return 1 if "failed" in verdicts.values() else 0


if __name__ == "__main__":
    sys.exit(main())
