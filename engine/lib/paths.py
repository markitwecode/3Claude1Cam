"""Where things live: the shared engine (code, venvs, assets) vs the project being produced.

ENGINE is this folder's parent (3Claude1Cam/engine). A project is any folder holding a
project.json (e.g. projects/focs/l03-lists); its script/, audio/, scenes/, music/, media/ and
out/ are what the tools read and write. The project is $VK_PROJECT if set (engine/vk sets it),
else the nearest folder at or above the working directory that holds project.json.
"""
import json
import os
from functools import cache
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
STUDIO = ENGINE.parent
MARKER = "project.json"


@cache
def ffmpeg_text() -> tuple[str, str]:
    """An ffmpeg that has the drawtext filter (for labelled check images), and the drawtext
    option prefix it needs. Homebrew's plain `ffmpeg` formula dropped drawtext (9.0.2,
    2026-11-03); `brew install ffmpeg-full` (keg-only) has it. $VK_FFMPEG_TEXT overrides.
    A font file is always passed, so builds without fontconfig work too."""
    import glob
    import shutil
    import subprocess
    cands = [os.environ.get("VK_FFMPEG_TEXT"), "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg",
             shutil.which("ffmpeg"), *sorted(glob.glob(str(Path.home() / "anaconda3/envs/*/bin/ffmpeg"))),
             str(Path.home() / "anaconda3/bin/ffmpeg")]
    font = "/System/Library/Fonts/Supplemental/Arial.ttf"
    for c in cands:
        if c and Path(c).exists():
            try:
                out = subprocess.run([c, "-hide_banner", "-filters"], capture_output=True,
                                     text=True, timeout=20).stdout
            except (OSError, subprocess.SubprocessError):
                continue
            if " drawtext " in out:
                return c, f"drawtext=fontfile={font}:"
    raise SystemExit("no ffmpeg with the drawtext filter: `brew install ffmpeg-full`, "
                     "or set VK_FFMPEG_TEXT to one that has it")


@cache
def project() -> Path:
    env = os.environ.get("VK_PROJECT")
    if env:
        return Path(env).resolve()
    cwd = Path.cwd().resolve()
    for d in (cwd, *cwd.parents):
        if (d / MARKER).exists():
            return d
    raise SystemExit(f"not inside a project: no {MARKER} at or above {cwd} "
                     "(cd into a project folder, or set VK_PROJECT)")


@cache
def config() -> dict:
    """project.json: title, course_line, code_language, sources, … (see docs/PIPELINE.md)."""
    return json.loads((project() / MARKER).read_text())


FINAL_QUALITY = {   # project.json "resolution" → manim flag, media folder, (width, height, fps)
    "1080p": ("-qh", "1080p60", (1920, 1080, 60)),
    "1440p": ("-qp", "1440p60", (2560, 1440, 60)),   # deep-style projects (docs/DEEP_STYLE.md §6)
}


def final_quality() -> tuple[str, str, tuple[int, int, int]]:
    """The final render's manim flag, media folder and (w, h, fps), from project.json
    "resolution" (default 1080p). Previews stay 480p15 for every project."""
    res = config().get("resolution", "1080p")
    if res not in FINAL_QUALITY:
        raise SystemExit(f"project.json resolution {res!r}: use one of {', '.join(FINAL_QUALITY)}")
    return FINAL_QUALITY[res]


@cache
def load_scene(stem):
    """Another scene file of this project as a module, for its helpers: e.g. the shot a
    "# handover: next" scene ends on, load_scene("ch2_s3_shiftreg").handover_shot().
    Loading a scene file doesn't render it."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"_scene_{stem}", project() / "scenes" / f"{stem}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def subprocess_env() -> dict:
    """Environment for child processes (manim renders): same project, and `import lib` works."""
    path = os.pathsep.join(p for p in (str(ENGINE), os.environ.get("PYTHONPATH")) if p)
    return {**os.environ, "VK_PROJECT": str(project()), "PYTHONPATH": path}


def rel(path) -> str:
    """A path for messages: relative to the project or the studio when possible."""
    path = Path(path)
    for base in (project(), STUDIO):
        try:
            return str(path.relative_to(base))
        except ValueError:
            pass
    return str(path)
