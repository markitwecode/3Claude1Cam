"""Handover joins: a scene marked "# handover: next" ends on the shot the next scene opens on, with
no fade-out, and the next scene starts with that shot already on screen. The stitched video then
cuts between two identical frames, so the join can't be seen.

Every other scene ends on an empty frame (a topic change gets its visual break). Before 2026-10-31
a continuing picture faded out and the next scene faded the same picture back in: ~1.5 s of
near-black mid-thought, which reads as a blink (Gemini flagged it in DE L8 ch2 and ch7).

vk check compares scene K's last frame with scene K+1's first (480p renders, once both exist) and
vk final repeats it on the 1080p parts. Both frames are scaled to 480x270; a pixel differs when a
channel is off by more than TOL, and a join fails when more than MAX_SHARE of pixels differ or
the shared frame is empty (the fade was left in).
"""
import re
import subprocess
from pathlib import Path

import numpy as np

MARK_RE = re.compile(r"^\s*#\s*handover:\s*next\b", re.M)
W, H = 480, 270
TOL = 32          # of 255, per channel: anti-aliasing noise stays under it, a moved edge doesn't
MAX_SHARE = 0.002 # 0.2% of pixels (~260): a stray label or a shifted line is well over it
EMPTY = 0.001     # a frame with fewer non-background pixels than this counts as empty


def marked(scene_file):
    return bool(MARK_RE.search(Path(scene_file).read_text()))


def _frame(video, last):
    cmd = ["ffmpeg", "-v", "error"] + (["-sseof", "-1"] if last else []) + ["-i", str(video)]
    cmd += ([] if last else ["-frames:v", "1"]) + ["-vf", f"scale={W}:{H}", "-f", "rawvideo",
                                                     "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = W * H * 3
    if len(raw) < n:
        raise ValueError(f"no frame decoded from {video}")
    return np.frombuffer(raw[-n:] if last else raw[:n], np.uint8).reshape(H, W, 3).astype(np.int16)


def _box(mask):
    ys, xs = np.nonzero(mask)
    return (f"x {xs.min() / W:.2f}–{(xs.max() + 1) / W:.2f}, "
            f"y {ys.min() / H:.2f}–{(ys.max() + 1) / H:.2f} of the frame from top left")


def check_join(a_stem, a_video, b_stem, b_video):
    """(ok, message) for the join a → b, where a is marked "# handover: next"."""
    a, b = _frame(a_video, last=True), _frame(b_video, last=False)
    background = a[0, 0]
    if (np.abs(a - background).max(axis=2) > TOL).mean() < EMPTY:
        return False, (f"{a_stem} → {b_stem}: {a_stem} ends on an empty frame, so the join still dips "
                       f"to black: end on the shared shot without fading it")
    diff = np.abs(a - b).max(axis=2) > TOL
    share = float(diff.mean())
    if share > MAX_SHARE:
        return False, (f"{a_stem} → {b_stem}: {a_stem}'s last frame and {b_stem}'s first differ in "
                       f"{100 * share:.1f}% of pixels ({_box(diff)}): the cut will jump. Build the "
                       f"shot from one function both scenes call")
    return True, f"{a_stem} → {b_stem}: frames match ({100 * share:.2f}% of pixels differ)"


def stale(stem, video, root):
    """True when a scene's file is newer than its render (the comparison may be out of date)."""
    return (root / "scenes" / f"{stem}.py").stat().st_mtime > Path(video).stat().st_mtime
