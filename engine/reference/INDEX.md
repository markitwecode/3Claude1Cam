# Manim reference: look things up, don't write from memory

(Paths here are relative to `engine/`, where this folder now lives.)

Before using a manim class or animation you haven't used in this project, find a real
example of it here. If sources disagree, **the installed source wins**:
`.venv/lib/python3.11/site-packages/manim/` is exactly what renders our videos (0.22.0).

| Source | What | Version |
|---|---|---|
| `manim-v0.22.0/docs/source/examples.rst` | The official Example Gallery: 27 complete, runnable scenes (text, LaTeX, graphs, updaters, camera, boolean ops, …); 48 more are embedded in the tutorials and guides below | exactly ours |
| `manim-v0.22.0/docs/source/tutorials/` | `quickstart`, `building_blocks` (mobjects / animations / scenes), `output_and_config` | exactly ours |
| `manim-v0.22.0/docs/source/guides/` | `using_text` (Text vs MarkupText vs Tex, fonts, t2c), `deep_dive` (how the renderer, caching and play() actually work), `configuration`, `add_voiceovers` | exactly ours |
| `manim-v0.22.0/example_scenes/` | The repo's own example scenes (`basic.py`, `customtex.py`, …) | exactly ours |
| `manim_skill/skills/manimce-best-practices/` | 23 rule files (animations, transforms, text, latex, positioning, grouping, timing, updaters, axes, graphing, lines, styling, cli, config…) + tested examples (`examples/`). Also installed as the project skill `manimce-best-practices`. | Jan 2026 (pre-0.22). No deprecated API found in a scan, but check the installed source if anything fails. |

Searching tips:

```sh
grep -n "TransformMatchingTex\|LaggedStart" reference/manim-v0.22.0/docs/source/examples.rst
grep -rln "ValueTracker" reference/manim_skill/skills/manimce-best-practices/
grep -n "def __init__" -A 25 .venv/lib/python3.11/site-packages/manim/mobject/text/code_mobject.py
```

## 3Blue1Brown's own code: the style reference

Grant renders his videos with **ManimGL** (`from manimlib import *`), his own branch of manim.
It forked from ours (ManimCE) in 2020, and code for one doesn't run on the other. **Read it for
how he builds, paces and reveals ideas; port the idea, never paste the code.**

| Path | What |
|---|---|
| `3b1b/PATTERNS.md` | **Start here.** His pacing measured from 2023–2026 code, plus concrete patterns with file:line citations |
| `3b1b/GL_TO_CE.md` | His most-used ManimGL APIs → our ManimCE 0.22 equivalents, verified against the installed source |
| `3b1b/ce_ports.py` | Tested ManimCE ports of GL helpers he relies on that CE lacks |
| `3b1b/videos/_20XX/` | His actual video code (2015 – Sept 2026, shallow clone of 3b1b/videos @ 306a134) |
| `3b1b/videos/custom/` | His reusable components |
| `3b1b/manimgl/manimlib/` | ManimGL itself (3b1b/manim @ fafa083), to see what a GL helper actually does |
| `3b1b/videos/GRANT_CLAUDE.md.txt` | His notes for Claude, renamed from CLAUDE.md so they don't auto-load as instructions |

His video code is CC BY-NC-SA 4.0. Fine for personal study, not for redistribution.

For project-specific patterns (narration sync, cons cells, OCaml code), see `STYLE.md`,
`LESSONS.md` and `lib/`. Those beat any generic reference here.
