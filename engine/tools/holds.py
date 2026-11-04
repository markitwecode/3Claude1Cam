"""One frame per narration clip at its last settled moment, tiled into one sheet per chapter.
Reviews composition at the moments viewers study.

    vk holds 1 [--quality 480p15]

Each tile is the last frame of the first still stretch (≥ 0.2 s with no visible change) that
reaches past the clip's last word, cut off before the next clip starts. So every cue of the
clip has played, nothing is mid-transform, and a transition between `say` blocks comes after
the tile, not in it. Timings are the render's own: clip starts from media/cues/<stem>_<q>.json
(written by every real render), clip lengths from audio/manifest.json, stillness from the video's
pixels. Label: "<clip id>  <scene time>s". "~" marks a clip that never holds still between its
last word and the next clip (its last still moment while speaking is shown, else the frame before
the next clip). A clip that ends on an empty frame shows its last still frame with something on
it. A scene without a usable cue file falls back to the old estimate (durations + gaps summed
from t=0, 0.4 s before each clip's end), marked "?", with a warning.
"""
import argparse
import json
import math
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
from lib.paths import ffmpeg_text, project  # noqa: E402

ROOT = project()   # the project folder (script/, audio/, scenes/, media/, …)
GAP = 0.35         # NarratedScene.gap (old estimate only)
W, H = 427, 240    # tile size: stillness is judged at the size the reviewer sees
BLOCK = 8          # ... on 8×8-pixel block means, which average out the codec's noise
STILL = 6          # grey levels a block mean may drift from a stretch's first frame and still
                   # count as unchanged (codec noise measured ≤ 5.1 on 268 known-still gaps)
MIN_STILL = 0.2    # s: a still stretch at least this long is a settled moment
EASE_IN = 0.25     # s to step back from the end of a stretch that motion ends
INK = 24           # grey levels away from the background that count as something on screen
EMPTY = 40         # a frame with fewer such pixels is empty


def profile(video):
    """Per frame: 8×8 block means (grey) and the number of pixels that aren't background."""
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(video), "-vf",
                          f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"],
                         stdout=subprocess.PIPE)
    hb, wb = H // BLOCK, W // BLOCK
    means, ink = [], []
    while buf := p.stdout.read(W * H * 120):
        fr = np.frombuffer(buf, np.uint8).reshape(-1, H, W)
        means.append(fr[:, :hb * BLOCK, :wb * BLOCK].reshape(len(fr), hb, BLOCK, wb, BLOCK)
                     .mean(axis=(2, 4), dtype=np.float32))
        bg = np.array([np.bincount(f.ravel(), minlength=256).argmax() for f in fr], np.int16)
        ink.append((np.abs(fr.astype(np.int16) - bg[:, None, None]) > INK).sum(axis=(1, 2)))
    if p.wait() or not means:
        raise RuntimeError(f"ffmpeg could not decode {video}")
    return np.concatenate(means), np.concatenate(ink)


def stretches(means):
    """first[k], last[k]: the still stretch holding frame k. A stretch runs on while every frame
    stays within STILL of its first frame, so a slow fade can't creep through as 'still'."""
    n = len(means)
    first, last = np.zeros(n, int), np.zeros(n, int)
    a = 0
    for k in range(1, n + 1):
        if k == n or np.abs(means[k] - means[a]).max() > STILL:
            first[a:k], last[a:k] = a, k - 1
            a = k
    return first, last


def settled(cues, manifest, fps, means, ink):
    """[(clip id, scene time, mark)] at each clip's last settled moment."""
    first, last = stretches(means)
    n, need = len(means), max(2, math.ceil(MIN_STILL * fps))
    back = math.ceil(EASE_IN * fps)

    def show(k, lo, hi):
        """The frame to show from the still stretch holding k, kept inside [lo, hi): its last
        one, or a little before it when motion ends it (STILL lets a stretch run on into the
        first frames of a slow ease-in)."""
        a, b = max(first[k], lo), last[k]
        return hi - 1 if b >= hi else max(b - back, a)

    def first_hold(lo, hi):
        """Frame to show from the first still stretch (≥ need) reaching into [lo, hi), or None."""
        k = lo
        while k < hi:
            if min(last[k], hi - 1) - first[k] + 1 >= need:
                return show(k, lo, hi)
            k = last[k] + 1
        return None

    def last_hold(lo, hi, min_ink=0):
        """Frame to show from the last still stretch (≥ need) inside [lo, hi) with enough ink."""
        k = hi - 1
        while k >= lo:
            if k - max(first[k], lo) + 1 >= need and ink[show(k, lo, hi)] >= min_ink:
                return show(k, lo, hi)
            k = first[k] - 1
        return None

    clips = cues["clips"]
    nexts = [c["start"] for c in clips[1:]] + [cues["duration"]]
    out = []
    for c, nxt in zip(clips, nexts):
        ks, kn = round(c["start"] * fps), min(round(nxt * fps), n)
        end = c["start"] + manifest.get(c["id"], {}).get("duration", 0.0)
        ke = min(max(ks, math.ceil(end * fps - 1e-6)), kn - 1)   # first frame after the last word
        pick, mark = first_hold(ke, kn), ""
        if pick is None:   # still moving when the next clip starts
            pick, mark = last_hold(ks, ke), " ~"
            pick = kn - 1 if pick is None else pick
        if ink[pick] < EMPTY:   # the clip clears the screen before it ends: show what it had up
            fuller = last_hold(ks, pick, EMPTY)
            pick = pick if fuller is None else fuller
        out.append((c["id"], int(pick) / fps, mark))
    return out


def estimated(src, manifest):
    """The old guess: clip durations + gaps summed from t=0, 0.4 s before each clip's end."""
    out, t = [], 0.0
    for cid in re.findall(r'self\.say\("([\w.]+)"', src):
        end = t + manifest[cid]["duration"]
        out.append((cid, max(0.0, end - 0.4), " ?"))
        t = end + GAP
    return out


def scene_holds(path, quality, manifest):
    """(video, [(clip id, scene time, mark)], warnings) for one scene file."""
    src = path.read_text()
    cls = re.search(r"^class (\w+)\(NarratedScene\)", src, re.M).group(1)
    video = ROOT / "media" / "videos" / path.stem / quality / f"{cls}.mp4"
    if not video.exists():
        return video, [], [f"warning: {path.stem}: no {quality} render, skipped"]
    stale = [f"warning: {path.stem}: scene file edited after its {quality} render "
             f"({time.strftime('%H:%M', time.localtime(path.stat().st_mtime))} > "
             f"{time.strftime('%H:%M', time.localtime(video.stat().st_mtime))}): its tiles show the old version; "
             f"re-render it (vk check) and run vk holds again"] \
        if path.stat().st_mtime > video.stat().st_mtime + 2 else []
    fps = int(quality.split("p")[1])
    cue_file = ROOT / "media" / "cues" / f"{path.stem}_{quality}.json"
    cues = json.loads(cue_file.read_text()) if cue_file.exists() else None
    warn, why = [], "is missing"
    if cues and abs(cue_file.stat().st_mtime - video.stat().st_mtime) > 300:
        why = "is from another render than the video"
    elif cues and cues.get("scene") != cls:
        why = f"is for {cues.get('scene')}, not {cls}"
    elif cues:
        means, ink = profile(video)
        if abs(len(means) - cues["duration"] * fps) <= 2:
            redone = [c["id"] for c in cues["clips"] if (ROOT / "audio" / f"{c['id']}.wav").exists()
                      and (ROOT / "audio" / f"{c['id']}.wav").stat().st_mtime > cue_file.stat().st_mtime]
            if redone:
                warn.append(f"warning: {path.stem}: rendered before {', '.join(redone)} was "
                            "re-voiced; re-render for exact holds")
            return video, settled(cues, manifest, fps, means, ink), stale + warn
        why = f"says {cues['duration']:.2f} s but the video is {len(means) / fps:.2f} s"
    warn.append(f"warning: {path.stem}: cue file {cue_file.relative_to(ROOT)} {why}; "
                "tiles estimated from summed durations, marked ?")
    return video, estimated(src, manifest), stale + warn


def grab(video, t, fps, label, out):
    # ffmpeg takes the first frame at or after -ss: aim half a frame early to get frame t*fps
    ff, dt = ffmpeg_text()   # an ffmpeg with drawtext (lib/paths.py)
    subprocess.run([ff, "-v", "error", "-y", "-ss", f"{max(0.0, t - 0.5 / fps):.4f}",
                    "-i", str(video), "-frames:v", "1", "-vf",
                    f"scale={W}:-1,{dt}text='{label}':x=6:y=h-22:fontcolor=white:"
                    "fontsize=14:box=1:boxcolor=black@0.6", str(out)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--quality", default="480p15")
    args = ap.parse_args()
    fps = int(args.quality.split("p")[1])
    manifest = json.loads((ROOT / "audio" / "manifest.json").read_text())
    paths = sorted((ROOT / "scenes").glob(f"ch{args.chapter}_*.py"))
    # never leave an old sheet behind: a failed or skipped run must not be misread as current
    (ROOT / "media" / f"ch{args.chapter}_holds.png").unlink(missing_ok=True)
    with ThreadPoolExecutor() as pool:
        scenes = list(pool.map(lambda p: scene_holds(p, args.quality, manifest), paths))
        jobs = [(video, t, f"{cid}  {t:.1f}s{mark}  @{time.strftime('%Hh%M', time.localtime(video.stat().st_mtime))}")
                for video, holds, _ in scenes for cid, t, mark in holds]
        if not jobs:
            sys.exit(f"no renders at {args.quality} for chapter {args.chapter}")
        with tempfile.TemporaryDirectory() as tmp:
            tiles = [Path(tmp) / f"{i:03d}.png" for i in range(len(jobs))]
            list(pool.map(lambda j: grab(j[0], j[1], fps, j[2], tiles[j[3]]),
                          [(*job, i) for i, job in enumerate(jobs)]))
            sheet = ROOT / "media" / f"ch{args.chapter}_holds.png"
            rows = (len(tiles) + 3) // 4
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i",
                            f"{tmp}/%03d.png", "-vf", f"tile=4x{rows}:padding=4:color=white",
                            "-frames:v", "1", str(sheet)], check=True)
    for line in (w for _, _, warn in scenes for w in warn):
        print(line)
    print(f"{sheet.relative_to(ROOT)}  ({len(tiles)} clips)")
    rough = [label.split()[0] for _, _, label in jobs if label.split()[1].endswith("~")]
    if rough:
        print(f"~ never still between its last word and the next clip: {', '.join(rough)}")


if __name__ == "__main__":
    main()
