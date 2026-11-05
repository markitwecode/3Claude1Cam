"""Dry-run a music cue sheet against a rendered chapter: where does each cue land?

    .venv/bin/python -I reference/3b1b/tools/cue_check.py SHEET.json CHAPTER [480p15|1080p60]

Uses tools/music.py's own line_times()/resolve() (same rules as the stitch step) on the
media/cues/*.json files of the last render, and prints each cue's window, its fade
points and the narration lines under it. Touches nothing (no loudness cache, no mix).
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("music", ROOT / "tools" / "music.py")
music = importlib.util.module_from_spec(spec)
spec.loader.exec_module(music)


def scenes(n, res):
    out = []
    for path in sorted((ROOT / "scenes").glob(f"ch{n}_*.py")):
        cls = re.search(r"^class (\w+)\(NarratedScene\)", path.read_text(), re.M).group(1)
        out.append((path.stem, ROOT / "media" / "videos" / path.stem / res / f"{cls}.mp4"))
    return out


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def main():
    sheet = json.loads(Path(sys.argv[1]).read_text())
    chapter, res = int(sys.argv[2]), (sys.argv[3] if len(sys.argv) > 3 else "480p15")
    manifest = json.loads((ROOT / "audio" / "manifest.json").read_text())
    times, total = music.line_times(scenes(chapter, res), res, manifest)
    last_end = max(e for _, e in times.values())
    print(f"chapter {chapter} ({res}): {mmss(total)} total, last line ends {mmss(last_end)} "
          f"-> end-card hold {total - last_end:.1f} s")
    for cue in sheet["cues"]:
        a = max(0.0, music.resolve(cue["from"], times, total) + cue.get("from_offset", 0))
        b = min(total, music.resolve(cue["until"], times, total) + cue.get("until_offset", 0))
        fi, fo = cue.get("fade_in", 2), min(cue.get("fade_out", 3), (b - a) / 2)
        under = [cid for cid, (s, e) in sorted(times.items(), key=lambda kv: kv[1][0]) if s < b and e > a]
        print(f"\n{Path(cue['track']).stem.split(' - ')[-1]}: {mmss(a)} -> {mmss(b)} ({b - a:.1f} s), "
              f"full level {mmss(a + fi)}..{mmss(b - fo)}, level_db {cue.get('level_db', -14)}, "
              f"track_start {cue.get('track_start', 0)}")
        print("   lines under it:", ", ".join(under) or "none")
        if not (ROOT / cue["track"]).exists():
            print("   !! track file missing:", cue["track"])


if __name__ == "__main__":
    main()
