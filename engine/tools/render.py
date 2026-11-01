"""Render a chapter's scenes in parallel (one manim process per scene), then stitch them.

    vk preview 1                       # 480p15 preview -> out/ch1_<name>_preview.mp4
    vk final 1                         # 1080p60        -> out/ch1_<name>.mp4
    vk render --chapter 1 --only ch1_s3_vs   # re-render some scenes (480p), re-stitch

Scenes are scenes/ch<N>_*.py in filename order, one NarratedScene subclass each.
Manim's Cairo renderer is single-threaded, so the speed-up comes from running all
scenes at once across the cores. Caching is off on purpose (see LESSONS.md).
Stitching copies the video stream (no re-encode), pads audio gaps with silence
so the narration can't drift, and loudness-normalises the audio. Before it, each join after a
scene marked "# handover: next" is compared frame to frame (tools/handover.py) and printed.
"""
import argparse
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
import music  # noqa: E402
from lib.paths import project, subprocess_env  # noqa: E402

ROOT = project()   # the project folder (script/, scenes/, media/, out/, …)
MANIM = ENGINE / ".venv" / "bin" / "manim"
QUALITY = {False: ("-ql", "480p15", "_preview"), True: ("-qh", "1080p60", "")}


def chapter_scenes(n):
    out = []
    for path in sorted((ROOT / "scenes").glob(f"ch{n}_*.py")):
        m = re.search(r"^class (\w+)\(NarratedScene\)", path.read_text(), re.M)
        if not m:
            sys.exit(f"{path.name}: no NarratedScene subclass")
        out.append((path.stem, m.group(1)))
    return out


def chapter_name(n):
    scripts = sorted((ROOT / "script").glob(f"ch{n}_*.md"))
    return scripts[0].stem if scripts else f"ch{n}"


def render(stem, cls, flag):
    t0 = time.time()
    log = ROOT / "media" / "logs" / f"{stem}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    # Parallel manim processes race on the shared text/LaTeX caches (one deletes an
    # SVG another is about to read), so each scene gets its own. They must live OUTSIDE
    # media/texts and media/Tex: manim's cache cleanup deletes whatever is inside those
    # folders, nested per-scene folders included (PermissionError).
    cfg = ROOT / "media" / "cfg" / f"{stem}.cfg"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(f"[CLI]\ntext_dir = {{media_dir}}/cache/{stem}/texts\n"
                   f"tex_dir = {{media_dir}}/cache/{stem}/Tex\n")
    with open(log, "w") as fh:
        # --disable_caching: a cached play advances the clock by its exact run_time but its
        # stored segment has a whole number of frames, so cached renders drift out of sync
        # with the narration (~0.3 s per scene measured). Fresh renders are cheap enough.
        import slots
        with slots.manim(f"render {stem}", gb=0.75 if flag == "-ql" else 1.2):
            cmd = [str(MANIM), flag, "--media_dir", "media", "--config_file", str(cfg),
                   "--disable_caching", f"scenes/{stem}.py", cls]
            if flag != "-ql":   # finals: nobody's loop waits on them, so builders' previews get the CPU first
                cmd = ["nice", "-n", "10"] + cmd
            rc = subprocess.run(cmd,
                                cwd=ROOT, env=subprocess_env(), stdout=fh,
                                stderr=subprocess.STDOUT).returncode
    return stem, rc, time.time() - t0, log


def stitch(parts, out, chapter, stems, res):
    listing = out.with_suffix(".txt")
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    head = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing)]
    tail = ["-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
    mix = music.build(chapter, list(zip(stems, parts)), res)
    if mix is None:     # narration only
        cmd = head + ["-c:v", "copy", "-af",
                      "aresample=async=1:first_pts=0,loudnorm=I=-16:TP=-1.5:LRA=11"] + tail
    else:               # narration + music cues from music/chN.json, ducked under the voice
        inputs, graph, label = mix
        cmd = head + inputs + ["-filter_complex", graph, "-map", "0:v", "-map", label,
                               "-c:v", "copy"] + tail
        print(f"music: {len(inputs) // 2} cue(s) from music/ch{chapter}.json")
    subprocess.run(cmd, check=True)
    listing.unlink()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--final", action="store_true", help="1080p60 instead of the 480p preview")
    ap.add_argument("--only", nargs="*", help="scene file stems to (re)render")
    ap.add_argument("--no-stitch", action="store_true")
    args = ap.parse_args()

    flag, res, suffix = QUALITY[args.final]
    scenes = chapter_scenes(args.chapter)
    if not scenes:
        sys.exit(f"no scenes/ch{args.chapter}_*.py files")
    todo = [(s, c) for s, c in scenes if not args.only or s in args.only]

    t0 = time.time()
    failed = []
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
        for stem, rc, took, log in pool.map(lambda sc: render(*sc, flag), todo):
            print(f"{stem:<22} {'ok' if rc == 0 else 'FAILED'}  {took:5.1f}s"
                  + ("" if rc == 0 else f"  (see {log.relative_to(ROOT)})"), flush=True)
            if rc:
                failed.append(stem)
    print(f"rendered {len(todo)} scene(s) in {time.time() - t0:.0f}s")
    if failed:
        sys.exit(1)
    if args.no_stitch:
        return

    parts = [ROOT / "media" / "videos" / s / res / f"{c}.mp4" for s, c in scenes]
    absent = [p for p in parts if not p.exists()]
    if absent:
        sys.exit("not stitching, some scenes have never been rendered at this quality:\n  "
                 + "\n  ".join(str(p.relative_to(ROOT)) for p in absent))
    import handover
    for (a, _), (b, _), pa, pb in zip(scenes, scenes[1:], parts, parts[1:]):
        if handover.marked(ROOT / "scenes" / f"{a}.py"):
            ok, msg = handover.check_join(a, pa, b, pb)
            print(f"handover {'ok' if ok else 'MISMATCH'}: {msg}")
    if handover.marked(ROOT / "scenes" / f"{scenes[-1][0]}.py"):
        print(f"handover MISMATCH: {scenes[-1][0]} is marked '# handover: next' but ends the chapter")
    out = ROOT / "out" / f"{chapter_name(args.chapter)}{suffix}.mp4"
    out.parent.mkdir(exist_ok=True)
    stitch(parts, out, args.chapter, [s for s, _ in scenes], res)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", str(out)]))
    print(f"-> {out.relative_to(ROOT)}  ({dur / 60:.1f} min)")


if __name__ == "__main__":
    main()
