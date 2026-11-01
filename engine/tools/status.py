"""Where a project stands, from its files alone (seconds, no rendering). Read this before
STATUS.md when resuming: it can't go stale.

    vk status

Per chapter: script (lines), narration (voiced / fresh), voice QA (sentences the Whisper
consensus still flags; `vk qa N` lists them), music cue sheet, scenes (built / skeleton /
missing, from the script's scene list), and the rendered video (stale if a scene or the cue
sheet changed after it). Chapters listed in PLAN.md without a script show as
"planned". Judgements (reviewed? accepted flags?) live in STATUS.md, not here.
"""
import json
import re
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
from lib.paths import config, project  # noqa: E402
from lib.scene_status import implementation_state  # noqa: E402
from voiceqa import line_state  # noqa: E402  (tools/, next to this file)

ROOT = project()
LINE_RE = re.compile(r"^\[([\w.]+)\]\s*(.*)$")
SCENE_RE = re.compile(r"^## Scene \d+ · (.+?) \((ch\d+_s\d+_\w+)\)\s*$")
PLAN_RE = re.compile(r"^## Chapter (\d+) · (.+?)\s*$")


def script_lines(path):
    """{id: raw} exactly as tools/voice.py parses them."""
    lines, cur = {}, None
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if m := LINE_RE.match(line):
            cur = m.group(1)
            lines[cur] = m.group(2)
        elif cur and line and not line.startswith(("#", ">", "---")):
            lines[cur] += " " + line
        else:
            cur = None
    return lines


def scene_state(path):
    if not path.exists():
        return "missing"
    src = path.read_text()
    return implementation_state(src)


def main():
    cfg = config()
    manifest_path = ROOT / "audio" / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    scripts = {int(re.match(r"ch(\d+)_", p.name).group(1)): p
               for p in sorted((ROOT / "script").glob("ch*_*.md"))}
    planned = {}
    if (ROOT / "PLAN.md").exists():
        for line in (ROOT / "PLAN.md").read_text().splitlines():
            if m := PLAN_RE.match(line):
                planned[int(m.group(1))] = m.group(2)

    print(f"{cfg.get('title', ROOT.name)} · {cfg.get('course_line', '')}  ({ROOT})")
    total_min = 0.0
    for n in sorted(set(scripts) | set(planned)):
        if n not in scripts:
            print(f"ch{n}  planned: {planned[n]}  (no script yet)")
            continue
        path = scripts[n]
        lines = script_lines(path)
        voiced = [c for c in lines if c in manifest and (ROOT / manifest[c]["file"]).exists()]
        stale = [c for c in voiced if manifest[c].get("raw") != lines[c]]
        minutes = sum(manifest[c]["duration"] for c in voiced) / 60
        total_min += minutes
        scenes = [m.group(2) for l in path.read_text().splitlines() if (m := SCENE_RE.match(l))]
        states = {s: scene_state(ROOT / "scenes" / f"{s}.py") for s in scenes}
        music = ROOT / "music" / f"ch{n}.json"
        outs = [p for p in (ROOT / "out").glob(f"ch{n}_*.mp4") if not p.stem.endswith("_preview")]
        inputs = [ROOT / "scenes" / f"{s}.py" for s in scenes if states[s] != "missing"]
        inputs += [music] if music.exists() else []
        newest = max((p.stat().st_mtime for p in inputs), default=0)

        built = sum(st == "built" for st in states.values())
        print(f"ch{n}  {path.stem}")
        qa = [line_state(manifest[c]) for c in voiced]
        flagged, unchecked = qa.count("flagged"), qa.count("unchecked")
        qa_note = ", ".join(x for x in (f"{flagged} line(s) flagged (vk qa {n})" if flagged else "",
                                        f"{unchecked} unchecked (vk voice {n} --qa-only)" if unchecked else "")
                            if x) or "clean"
        if unchecked and unchecked == len(qa):
            qa_note = f"not run (vk voice {n} --qa-only)"
        print(f"     script {len(lines)} lines · narration {len(voiced)}/{len(lines)} voiced"
              f"{f' ({len(stale)} changed since voicing: run vk voice {n})' if stale else ''}"
              f", {minutes:.1f} min" + (f", QA {qa_note}" if voiced else "")
              + f" · music {'yes' if music.exists() else 'NO'}")
        others = [f"{s} {st}" for s, st in states.items() if st != "built"]
        print(f"     scenes {built}/{len(scenes)} built" + (f": {', '.join(others)}" if others else ""))
        if outs:
            out = max(outs, key=lambda p: p.stat().st_mtime)
            fresh = out.stat().st_mtime >= newest
            print(f"     video  {out.relative_to(ROOT)}" + ("" if fresh else
                  "  (STALE: scenes or music changed after it; run vk final " + str(n) + ")"))
        else:
            print("     video  none")
    print(f"narration total {total_min:.1f} min")


if __name__ == "__main__":
    main()
