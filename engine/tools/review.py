"""A viewer's review by Gemini, which watches and hears the video: mispronunciations, picture vs
narration mismatches, visual glitches and confusing moments, each mapped back to its scene,
scene-local time and narration clip.

    vk review 4 [--model M] [--file out/ch4_x.mp4]   the finished chapter (out/chN_<slug>.mp4)
    vk review ch4_s3_trace ch4_s5_nrev [--model M]    scenes: each one's latest 480p check render

Chapter mode: the final video (or --file), downscaled to 720p30 and split into equal pieces of at
most --chunk s (default 600), 2 in flight. `vk final` concatenates the scene renders
(media/videos/<stem>/<res>/<Class>.mp4, filename order, video stream copied, no gaps or separate
cards: the title card is part of scene 1), so a scene starts where the previous render ends.
Scene mode: media/videos/<stem>/480p15/<Class>.mp4 (what `vk check` renders), one request per
scene, 3 in flight. Either way clip starts come from the render's own cue file
(media/cues/<stem>_<res>.json) and clip lengths from audio/manifest.json.

Calibration: a pronunciation finding is snapped to the nearest narration word (±12 s) matching
what Gemini says was expected ("≈" when none matched). A visual finding (glitch, mismatch) is
tagged "mid-transition" when the picture is moving within ±0.6 s of it (Gemini samples about one
frame a second): measured 2026-10-28 on l03 ch4, its "collisions" and "duplicates" were frames
inside a transform that resolved ~0.5 s later. Untagged visual findings are on a still frame and
worth a look; findings are claims either way.

--transitions: a prompt for visual problems only, *including* brief ones during animations (letters
scrambling mid-morph, doubled copies, old text ghosting under new, half-written words, elements
early or late), which the stock prompt tells Gemini to ignore. It found 51 glitches on l03 ch4 where
the stock prompt found 1 (glitch study 2026-10-28). Output goes to *_transitions.{json,md} instead
of *_review.*. Directors run it on the final review and record its findings under "Glitches".

Output: media/review/chN_review.{json,md} or media/review/<stem>_review.{json,md}; the .md is
printed: one line per finding,
    <scene> @ <scene s> (<clip id>) [<kind>] "expected" → "observed"  (<severity>, conf <c>)  [mm:ss.s]
Writes nothing outside media/review/.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(ENGINE / "tools"))
from lib.paths import config, project, rel  # noqa: E402
from gemini import (DEFAULT_MODEL, add_usage, cut, ffprobe_duration, fmt_usage, mss,  # noqa: E402
                    parse_time, watch)
from holds import BLOCK, STILL, H, W  # noqa: E402  (same stillness test as vk holds)
from music import probe_duration  # noqa: E402
from render import chapter_name, chapter_scenes  # noqa: E402
from voiceqa import qa_token  # noqa: E402

ROOT = project()
SNAP = 12.0          # s: how far from Gemini's time a pronunciation finding may be snapped
NEAR = 0.6           # s: motion this close to a visual finding makes it "mid-transition"
SCENE_RES = "480p15"
KINDS = ["pronunciation", "mismatch", "glitch", "confusing"]
VISUAL = {"mismatch", "glitch"}
LEVELS = ["high", "medium", "low"]

SCHEMA = {
    "type": "object",
    "properties": {
        "findings": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "time": {"type": "string", "description": "mm:ss.s from the start of this clip, where the problem starts"},
                "kind": {"type": "string", "enum": KINDS},
                "expected": {"type": "string", "description": "pronunciation: the word(s) as they should be said, plain spelling, no IPA; otherwise what should be seen or heard. Under 15 words."},
                "observed": {"type": "string", "description": "pronunciation: what it actually sounds like, plain spelling, no IPA; otherwise what is seen or heard. Under 15 words."},
                "severity": {"type": "string", "enum": LEVELS},
                "confidence": {"type": "string", "enum": LEVELS},
            },
            "required": ["time", "kind", "expected", "observed", "severity", "confidence"],
        }},
        "overall": {"type": "string", "description": "one sentence on the clip as a whole"},
    },
    "required": ["findings"],
}

PROMPT = """This is {what} of a narrated, animated explainer video in the style of 3Blue1Brown: "{title}", {course}, chapter {n} ("{chapter}"). The voice is text-to-speech. Watch and listen to all of it as a careful, attentive viewer and report every problem of these four kinds:

1. pronunciation: every mispronounced word, letter or symbol. Code names and single letters are read out by their letter names, and these readings are correct: n = "en", x = "ex", xs = "exes", ys = "whys" (sounds like "wise"), l = "ell", k = "kay"; so nrev is "en-rev". Report only deviations, e.g. expected "en-rev", observed "on-rev". Report EVERY occurrence separately, even when the same word is mispronounced again.
2. mismatch: moments where the picture doesn't match what is being said (wrong thing highlighted, a value, count or code on screen that contradicts the narration, an animation far too early or too late).
3. glitch: visual glitches that stay on screen: stray or duplicate objects, flicker, overlapping or colliding objects, text cut off at the frame edge, wrong counts, objects left behind after they should be gone. Judge the picture once it has settled: shapes morphing, fading or sliding during an animation are not glitches unless the animation ends wrong.
4. confusing: anything confusing, unclear or too fast to follow.

Times are mm:ss.s from the start of this clip, as a video player shows them, at the moment the problem starts (for pronunciation, the moment the word is spoken). Keep "expected" and "observed" short. If there are no problems of a kind, report none; don't invent any."""


# ── what was stitched: scene offsets and clip starts ───────────────────────────
def quality_of(video):
    """The render quality a video was made at: '1080p60', '480p15', …"""
    h, rate = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                       "stream=height,r_frame_rate", "-of", "csv=p=0:s=,",
                                       str(video)], text=True).strip().split(",")[:2]
    num, _, den = rate.partition("/")
    return f"{h}p{round(int(num) / int(den or 1))}"


def scene_class(stem):
    path = ROOT / "scenes" / f"{stem}.py"
    if not path.exists():
        sys.exit(f"no scene file scenes/{stem}.py")
    m = re.search(r"^class (\w+)\(NarratedScene\)", path.read_text(), re.M)
    if not m:
        sys.exit(f"scenes/{stem}.py: no NarratedScene subclass")
    return m.group(1)


def clips_of(stem, cls, res, part, offset, manifest, warn):
    """The render's clips in output time: [{id, start, end, words: [(word, time)]}]."""
    cue_file = ROOT / "media" / "cues" / f"{stem}_{res}.json"
    cues = json.loads(cue_file.read_text()) if cue_file.exists() else None
    if not cues or cues.get("scene") != cls:
        warn.append(f"{stem}: no usable cue file {rel(cue_file)}; its findings map to the scene only")
        return []
    if abs(cue_file.stat().st_mtime - part.stat().st_mtime) > 300:
        warn.append(f"{stem}: {rel(cue_file)} is from another render than {rel(part)}; clip times may be off")
    out = []
    for c in cues["clips"]:
        info = manifest.get(c["id"], {})
        s = offset + c["start"]
        out.append({"id": c["id"], "start": s, "end": s + info.get("duration", 0.0),
                    "words": [(w, s + t) for w, t in info.get("words", [])]})
    return out


def chapter_timeline(n, res, video):
    """[{stem, start, end, clips}] in chapter time, and warnings."""
    manifest = json.loads((ROOT / "audio" / "manifest.json").read_text())
    scenes, warn, offset = [], [], 0.0
    for stem, cls in chapter_scenes(n):
        part = ROOT / "media" / "videos" / stem / res / f"{cls}.mp4"
        if not part.exists():
            sys.exit(f"{rel(part)} missing: can't map times (was the chapter stitched at {res}?)")
        dur = probe_duration(part)
        if part.stat().st_mtime > video.stat().st_mtime + 60:
            warn.append(f"{stem}: re-rendered after {video.name} was stitched; its times may be off")
        scenes.append({"stem": stem, "start": offset, "end": offset + dur,
                       "clips": clips_of(stem, cls, res, part, offset, manifest, warn)})
        offset += dur
    total = ffprobe_duration(video)
    if abs(total - offset) > 0.5:
        warn.append(f"the scene renders add up to {offset:.2f} s but {video.name} is {total:.2f} s: "
                    "it isn't a stitch of the current renders, so times may be off")
    return scenes, warn


def scene_timeline(stem):
    """(video, [one scene], warnings) for a scene's 480p check render."""
    cls = scene_class(stem)
    video = ROOT / "media" / "videos" / stem / SCENE_RES / f"{cls}.mp4"
    if not video.exists():
        sys.exit(f"{rel(video)} missing: render it first (vk check {stem})")
    warn = []
    if (ROOT / "scenes" / f"{stem}.py").stat().st_mtime > video.stat().st_mtime + 5:
        warn.append(f"{stem}: scenes/{stem}.py changed after this render; reviewing the older render")
    manifest = json.loads((ROOT / "audio" / "manifest.json").read_text())
    dur = probe_duration(video)
    return video, [{"stem": stem, "start": 0.0, "end": dur,
                    "clips": clips_of(stem, cls, SCENE_RES, video, 0.0, manifest, warn)}], warn


def locate(scenes, t):
    """Output time -> (scene, clip or None, where: 'in' | 'after' | 'before')."""
    sc = next((s for s in scenes if s["start"] <= t < s["end"]), None)
    sc = sc or (scenes[-1] if t >= scenes[-1]["start"] else scenes[0])
    started = [c for c in sc["clips"] if c["start"] <= t + 1e-6]
    if not started:
        return sc, (sc["clips"][0] if sc["clips"] else None), "before"
    c = started[-1]
    return sc, c, "in" if t <= c["end"] + 0.05 else "after"


def said_around(clip, t, k=4):
    """The narration words around time t in this clip."""
    if not clip or not clip["words"]:
        return ""
    i = max([j for j, (_, wt) in enumerate(clip["words"]) if wt <= t] or [0])
    return " ".join(w for w, _ in clip["words"][max(0, i - k):i + k + 1])


def phrases(text):
    """Candidate script phrases (compared tokens) from Gemini's 'expected' text: quoted parts,
    then the text outside parentheses split on ' or ', '/', ',' and ';'."""
    out = re.findall(r"[\"“']([^\"”']+)[\"”']", text)
    out += re.split(r"\s+or\s+|/|;|,", re.sub(r"\(.*?\)|\[.*?\]", " ", text))
    seen, keep = set(), []
    for p in out:
        toks = [x for x in (qa_token(w) for w in p.split()) if x]
        if toks and tuple(toks) not in seen and len(toks) <= 6:
            seen.add(tuple(toks))
            keep.append(toks)
    return keep


def snap(clips, t, expected, within=SNAP):
    """The narration word nearest t (within `within` s) matching `expected` -> (time, clip, word
    index) or None."""
    best = None
    for toks in phrases(expected):
        want, k = "".join(toks), len(toks)
        for c in clips:
            if c["end"] < t - within or c["start"] > t + within:
                continue
            ws = c["words"]
            for i in range(len(ws) - k + 1):
                if abs(ws[i][1] - t) > within:
                    continue
                got = "".join(qa_token(w) for w, _ in ws[i:i + k])
                if got and (got == want or (len(want) > 3 and SequenceMatcher(None, want, got).ratio() >= 0.8)):
                    if best is None or abs(ws[i][1] - t) < best[0]:
                        best = (abs(ws[i][1] - t), ws[i][1], c, i)
    return best[1:] if best else None


def moving(video, t, near=NEAR):
    """Does the picture change within ±near s of t? (holds.py's test: 8×8 block means of a
    427×240 grey frame drifting more than STILL from the first frame.) None if undecodable."""
    a = max(0.0, t - near)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{t + near - a:.3f}", "-i",
                          str(video), "-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8)
    if len(fr) < 2 * W * H:
        return None
    fr = fr[:len(fr) // (W * H) * W * H].reshape(-1, H, W)
    hb, wb = H // BLOCK, W // BLOCK
    means = fr[:, :hb * BLOCK, :wb * BLOCK].reshape(len(fr), hb, BLOCK, wb, BLOCK).mean(axis=(2, 4))
    return bool(np.abs(means - means[0]).max() > STILL)


# ── Gemini, and turning its answers into mapped findings ───────────────────────
TRANSITION_KINDS = ["glitch", "timing", "mismatch"]
TRANSITION_PROMPT = """This is {what} of a narrated, animated explainer video in the style of 3Blue1Brown: "{title}", {course}, chapter {n} ("{chapter}"). Watch it closely, as a sharp-eyed viewer stepping through it, and report every VISUAL problem, including brief ones that last only a fraction of a second while something animates. Three kinds:

1. glitch: anything that looks wrong at any moment, INCLUDING DURING ANIMATIONS: letters of a text scrambling, jumbling, doubling or flying to wrong places while the text changes; a word, symbol or object briefly shown twice; a shape or text morphing through a garbled intermediate state; objects that pop, flicker or jump; stray or leftover objects, including ones that linger from the previous shot for a moment before vanishing; objects overlapping or colliding; rotated, mirrored or upside-down text; a wrong or misplaced glyph (e.g. a symbol sitting too high or too low); text cut off at the frame edge. A smooth, sensible motion (a slide, a fade, a clean morph between similar shapes) is NOT a glitch; a morph that passes through a garbled, doubled or scrambled state IS.
2. timing: an element that appears clearly (more than about a second) before or after the narration mentions it.
3. mismatch: the picture contradicts what is being said (a wrong value, highlight, count or code).

Times are mm:ss.s from the start of this clip, as a video player shows them, at the moment the problem becomes visible, as precisely as you can (to 0.1 s). Report each occurrence separately. Do not report pronunciation or other audio problems. If there are no problems of a kind, report none; don't invent any."""
SUFFIX = "review"   # media/review/<chN|stem>_<SUFFIX>.{json,md}


def use_transitions():
    """Switch this run to the transition-aware prompt (vk review --transitions)."""
    global PROMPT, KINDS, VISUAL, SUFFIX
    PROMPT, KINDS, VISUAL, SUFFIX = TRANSITION_PROMPT, TRANSITION_KINDS, set(TRANSITION_KINDS), "transitions"
    item = SCHEMA["properties"]["findings"]["items"]["properties"]
    item["kind"]["enum"] = TRANSITION_KINDS
    item["expected"]["description"] = "what should be seen at that moment. Under 15 words."
    item["observed"]["description"] = "exactly what is seen: which text or object, what it looks like. Under 20 words."


def ask(clip, what, n, model):
    cfg = config()
    chapter = re.sub(r"^ch\d+_", "", chapter_name(n)).replace("_", " ")
    return watch(clip, PROMPT.format(what=what, title=cfg.get("title", ""), course=cfg.get("course_line", ""),
                                     n=n, chapter=chapter), SCHEMA, model=model)


def mapped(results, scenes, video, total, warnings):
    """[(offset, Result)] -> findings sorted by time, each mapped to scene/clip and calibrated."""
    findings = []
    clips = [c for sc in scenes for c in sc["clips"]]
    for start, r in results:
        for f in r.data.get("findings", []):
            local = parse_time(f.get("time", ""))
            if local is None:
                warnings.append(f"unreadable time {f.get('time')!r}: {f}")
                continue
            t = min(start + local, total)
            item = {"time": round(t, 2), "mmss": mss(t), "gemini_time": round(t, 2),
                    **{k: str(f.get(k, "")).strip() for k in ("kind", "expected", "observed", "severity", "confidence")}}
            if item["kind"] == "pronunciation":
                hit = snap(clips, t, item["expected"])
                item["snapped"] = bool(hit)
                if hit:
                    t = hit[0]
                    item.update(time=round(t, 2), mmss=mss(t))
            elif item["kind"] in VISUAL:
                item["moving"] = moving(video, t)
            sc, c, where = locate(scenes, t)
            item.update(scene=sc["stem"], scene_time=round(t - sc["start"], 2),
                        clip=c["id"] if c else None, where=where,
                        clip_time=round(t - c["start"], 2) if c and where == "in" else None,
                        said=said_around(c, t) if where == "in" else "")
            findings.append(item)
    return sorted(findings, key=lambda f: f["time"])


def line(f):
    tag = f["clip"] if f["where"] == "in" else (f"{f['where']} {f['clip']}" if f["clip"] else "no clip")
    kind = f["kind"] + (", mid-transition" if f.get("moving") else "")
    approx = " ≈" if f["kind"] == "pronunciation" and not f.get("snapped") else ""
    return (f"{f['scene']} @ {f['scene_time']:.1f} s ({tag}) [{kind}] \"{f['expected']}\" → "
            f"\"{f['observed']}\"  ({f['severity']}, conf {f['confidence']}){approx}  [{f['mmss']}]")


def report(out_base, title, video, total, model, results, seconds, findings, warnings):
    usage = {}
    for _, r in results:
        add_usage(usage, r.usage)
    overall = [r.data["overall"] for _, r in results if r.data.get("overall")]
    data = {"title": title, "video": rel(video), "duration": round(total, 2), "model": model,
            "generated": datetime.now().isoformat(timespec="seconds"), "seconds": round(seconds, 1),
            "usage": usage, "overall": overall, "warnings": warnings,
            "chunks": [{"start": round(s, 2), "seconds": round(r.seconds, 1), "attempts": r.attempts,
                        "usage": r.usage, "raw": r.data} for s, r in results],
            "findings": findings}
    out_base.parent.mkdir(parents=True, exist_ok=True)
    out_base.with_suffix(".json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    vis = [f for f in findings if f["kind"] in VISUAL]
    counts = ", ".join(f"{sum(f['kind'] == k for f in findings)} {k}" for k in KINDS)
    md = [f"# {title} ({model})",
          f"{rel(video)}, {mss(total)}; {seconds:.0f} s, {fmt_usage(usage)}. {counts}; "
          f"{sum(bool(f.get('moving')) for f in vis)} of {len(vis)} visual findings mid-transition. "
          "Claims: check a frame before fixing.", "",
          *(line(f) for f in findings),
          *([""] + [f"warning: {w}" for w in warnings] if warnings else [])]
    out_base.with_suffix(".md").write_text("\n".join(md) + "\n")
    return "\n".join(md)


# ── the two modes ──────────────────────────────────────────────────────────────
def review_chapter(n, model, file, chunk):
    if file:
        video = Path(os.environ.get("VK_CALLER_PWD") or os.getcwd(), file).expanduser().resolve()
    else:
        outs = [p for p in (ROOT / "out").glob(f"ch{n}_*.mp4") if not p.stem.endswith("_preview")]
        if not outs:
            sys.exit(f"no final video out/ch{n}_*.mp4 (vk final {n}), or pass --file")
        named = ROOT / "out" / f"{chapter_name(n)}.mp4"
        video = named if named.exists() else max(outs, key=lambda p: p.stat().st_mtime)
    if not video.exists():
        sys.exit(f"no such file: {video}")
    res = quality_of(video)
    scenes, warnings = chapter_timeline(n, res, video)
    total = ffprobe_duration(video)
    k = int(max(1, -(-total // chunk)))
    step = total / k
    pieces = [(i * step, min(step, total - i * step)) for i in range(k)]
    print(f"reviewing {rel(video)} ({mss(total)}, {res}) in {k} piece(s) with {model}", flush=True)
    t0 = time.time()
    with tempfile.TemporaryDirectory(prefix="vk-review-") as tmp:
        def one(i):
            start, dur = pieces[i]
            clip = cut(video, Path(tmp) / f"ch{n}_part{i + 1}.mp4", start, dur)
            what = (f"part {i + 1} of {k} (from {mss(start)} to {mss(start + dur)} of the chapter; give times "
                    "from the start of THIS clip)") if k > 1 else "one whole chapter"
            r = ask(clip, what, n, model)
            print(f"  piece {i + 1}/{k} [{mss(start)}–{mss(start + dur)}]: {len(r.data.get('findings', []))} "
                  f"finding(s), {r.seconds:.0f}s, {fmt_usage(r.usage)}", flush=True)
            return start, r
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(one, range(k)))
    findings = mapped(results, scenes, video, total, warnings)
    md = report(ROOT / "media" / "review" / f"ch{n}_{SUFFIX}", f"Chapter {n} {SUFFIX}", video, total, model,
                results, time.time() - t0, findings, warnings)
    print(md)


def review_scenes(stems, model):
    def one(stem):
        video, scenes, warnings = scene_timeline(stem)
        total = probe_duration(video)
        n = int(re.match(r"ch(\d+)_", stem).group(1))
        t0 = time.time()
        r = ask(video, f"one scene ({mss(total)} long, a 480p check render)", n, model)
        findings = mapped([(0.0, r)], scenes, video, total, warnings)
        md = report(ROOT / "media" / "review" / f"{stem}_{SUFFIX}", f"{stem} {SUFFIX}", video, total, model,
                    [(0.0, r)], time.time() - t0, findings, warnings)
        return md
    print(f"reviewing {len(stems)} scene render(s) ({SCENE_RES}) with {model}", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        for md in pool.map(one, stems):
            print(md + "\n", flush=True)


def main():
    import gemini as _g
    if _g.off_reason():   # Gemini's quota is out: say so plainly, exit 3 (agents treat it as "skipped")
        print(f"vk review: skipped, Gemini is off ({_g.off_reason()}). Use vk qa / vk check / vk holds / "
              "builder frames instead (chapter-director.md, \"When Gemini is off\").", flush=True)
        sys.exit(3)
    ap = argparse.ArgumentParser(description="Gemini reviews a finished chapter or scene renders as a viewer.")
    ap.add_argument("targets", nargs="+", help="a chapter number, or scene stems (ch4_s3_trace …)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--file", help="chapter mode: the video (default out/chN_<slug>.mp4)")
    ap.add_argument("--chunk", type=float, default=600, help="chapter mode: max seconds per request")
    ap.add_argument("--transitions", action="store_true",
                    help="visual problems only, including brief ones during animations -> *_transitions.md")
    args = ap.parse_args()
    if args.transitions:
        use_transitions()
    if len(args.targets) == 1 and args.targets[0].isdigit():
        review_chapter(int(args.targets[0]), args.model, args.file, args.chunk)
    elif all(re.match(r"ch\d+_s\d+_\w+$", t) for t in args.targets):
        review_scenes(args.targets, args.model)
    else:
        sys.exit("vk review: give one chapter number, or scene stems like ch4_s3_trace")


if __name__ == "__main__":
    main()
