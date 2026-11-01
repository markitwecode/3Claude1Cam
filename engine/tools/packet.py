"""Everything a scene builder needs about one scene, in one compact printout:
where it sits in the chapter, the visual brief, and every narration line with the time
each sentence (and {mark}) starts, so animations can be planned against the voice.

    vk packet ch2_s4_why

Times are seconds from the clip's start (what c.until()/c.wait_until() measure against);
"⏸" marks a pause of ≥ 0.9 s in the voice. Any {mark} or any phrase shown can be a cue.
If the scene file already exists, its module docstring (design plan / STATUS) is printed too.
"""
import ast
import json
import re
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
from lib.paths import config, project  # noqa: E402
from lib.scene_status import implementation_state  # noqa: E402

ROOT = project()   # the project folder (script/, audio/, scenes/, media/, …)


def scenes_of(script):
    """[(stem, title, body_lines)] in script order."""
    out, cur = [], None
    for line in script.splitlines():
        m = re.match(r"^## Scene \d+ · (.+?) \((ch\d+_s\d+_\w+)\)\s*$", line)
        if m:
            cur = (m.group(2), m.group(1), [])
            out.append(cur)
        elif line.startswith("## "):
            cur = None
        elif cur is not None:
            cur[2].append(line)
    return out


def timed(entry):
    """Script words with their start times, cut into sentences, {marks} put back in."""
    words, marks = entry["words"], entry["marks"]
    at = {}
    for name, t in marks.items():   # a mark sits just before the word it cues (0.05 s lead)
        i = min(range(len(words)), key=lambda k: abs(words[k][1] - (t + 0.05)))
        at.setdefault(i, []).append(name)
    lines, cur, start = [], [], None
    for i, (w, t) in enumerate(words):
        if i in at and cur:
            lines.append((start, " ".join(cur)))
            cur = []
        if not cur:
            start = t
        cur += [f"{{{n}}}" for n in at.get(i, [])] + [w]
        nxt = words[i + 1][1] if i + 1 < len(words) else None
        if nxt is not None and nxt - t > 0.9 + 0.08 * len(w):
            cur.append("⏸")
        if re.search(r"[.?!]$", w):
            lines.append((start, " ".join(cur)))
            cur = []
    if cur:
        lines.append((start, " ".join(cur)))
    return lines


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    stem = sys.argv[1]
    n = re.match(r"ch(\d+)_", stem).group(1)
    script_path = next((ROOT / "script").glob(f"ch{n}_*.md"))
    script = script_path.read_text()
    chapter = script.splitlines()[0].lstrip("# ").strip()
    scenes = scenes_of(script)
    idx = [s[0] for s in scenes].index(stem)
    _, title, body = scenes[idx]
    manifest = json.loads((ROOT / "audio" / "manifest.json").read_text())

    path = ROOT / "scenes" / f"{stem}.py"
    if path.exists():
        src = path.read_text()
        cls = re.search(r"^class (\w+)\(NarratedScene\)", src, re.M)
        n_lines = len(src.splitlines())
        state = (f"exists, class {cls.group(1) if cls else '?'}, {n_lines} lines"
                 + (", has a STATUS block (resume it)" if "STATUS" in src else "")
                 + (" (a skeleton: empty or narration/timing only)"
                    if implementation_state(src) == "skeleton" else ""))
        doc = ast.get_docstring(ast.parse(src)) or ""
    else:
        state, doc = "missing: create it", ""

    cfg = config()
    print(f"PROJECT {cfg.get('title', '?')} ({cfg.get('course_line', '')}); code on screen: "
          f"{cfg.get('code_language') or 'none'}")
    print(f"SCENE {stem}: {title}\n{chapter} (script/{script_path.name}), scene {idx + 1} of {len(scenes)}")
    print(f"file: scenes/{stem}.py  ({state})")
    print(f"neighbours: {scenes[idx - 1][0] if idx else '(none: chapter start)'} | "
          f"{scenes[idx + 1][0] if idx + 1 < len(scenes) else '(none: chapter end)'}")
    if idx == 0:
        print("FIRST scene: open with title_card(...) as the brief says (lib/titles.py).")
    if idx == len(scenes) - 1:
        print("LAST scene: end on a ~8 s end card (the finished recap + 'Next: …'), music carries it, then fade.")

    brief = [l[1:].strip() for l in body if l.startswith(">")]
    ids = [m.group(1) for l in body for m in [re.match(r"^\[([\w.]+)\]", l)] if m]
    total = sum(manifest[c]["duration"] for c in ids)
    print(f"\nVISUAL BRIEF (a strong suggestion; keep every beat the narration names)")
    print("\n".join(f"  {l}" for l in brief))
    print(f"\nNARRATION: {len(ids)} clips, {total:.1f} s (+0.35 s gap after each)")
    for cid in ids:
        e = manifest[cid]
        print(f"[{cid}] {e['duration']:.1f} s")
        for t, text in timed(e):
            print(f"  {t:5.1f}  {text}")
    if doc:
        print(f"\nEXISTING FILE DOCSTRING (plan / status from earlier work)\n{doc}")


if __name__ == "__main__":
    main()
