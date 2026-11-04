# The pipeline

How a request becomes finished videos, what each stage reads and writes, and how to recover when
something stops halfway. The producer's short version is the root `CLAUDE.md`. Each agent's own
rules are in `.claude/agents/<name>.md`, which is the authority for that role.

```
request + material
   │  vk lecture (if a recording) ─▶ source/<stem>.transcript.md, .digest.md  (Whisper + Gemini)
   │  series-planner ──────────────▶ PLAN.md, project.json              (≈ 2–5M tokens)
   │  (user approves the plan: the one checkpoint)
   │  script-writer × chapters ────▶ script/chN_<slug>.md              (≈ 2–4M each, parallel)
   │  series-planner (review) ─────▶ small edits to the scripts
   │  load-auditor × chapters ─────▶ script/chN_load.json            (Sonnet, ~70k tokens each, parallel)
   │  vk load N… ──────────────────▶ media/review/chN_load.md         (the load gate; "over" → back to the writer)
   │  vk voice ────────────────────▶ audio/*.wav + audio/manifest.json (local GPU, ~20–30 min/hour)
   │  chapter-director × chapters  (one at a time by default)
   │     ├─ music/chN.json
   │     ├─ scene-builder × scenes ──▶ scenes/chN_sK_<slug>.py   (Opus, medium effort; Codex `vk build` only at a Claude usage limit)
   │     ├─ vk qa + vk listen (Gemini ear-check) → narration fixes
   │     ├─ vk check / vk review <stems> (Gemini) / vk holds → fix passes
   │     ├─ vk review N (Gemini, after vk final) → at most one more round
   │     └─ vk final N ────────────▶ out/chN_<slug>.mp4                (1080p60, music mixed)
   ▼
STATUS.md (per project) and projects/INDEX.md, kept current at every stage
```

## Granularity
- **Project:** one series, e.g. one lecture or one topic. It's a folder with a `project.json`. A
  course is a folder of projects plus a `COURSE.md`.
- **Chapter:** ≈ 1300–1800 spoken words (8–11 min at ~160 wpm; with the house pacing's pauses the video runs ~20% longer), one question
  answered, ending in a recap. A one-hour lecture becomes 4–6 chapters (~45–60 min).
- **Scene:** one idea or visual setting, 45–150 s, one ManimCE file. A chapter has 6–8 scenes.
- **Clip:** one narration line `[cN.key.k]`, 15–40 s. It's the unit of voicing, and of syncing
  (a `with self.say(id)` block).
- **Mark:** `{word}` inside a clip, a cue point animations land on.

The planner decides the counts within these ranges (sizing rules in `series-planner.md`).

## A project folder
| Path | Written by | What |
|---|---|---|
| `project.json` | `vk new`, planner | `title` and `course_line` (title card), `code_language` (Pygments lexer for `Code`), `toolchain` (how to run code to verify it), `sources` |
| `PLAN.md` | planner | Chapters (`## Chapter N · Title`), each with slug, minutes, source pages, goal, scene list and continuity; then "Decisions" |
| `STATUS.md` | directors, producer | Judgements the files can't show: reviewed or not, accepted check flags and why, lines to check by ear, open issues |
| `script/chN_<slug>.md` | script-writer | Narration + marks + visual briefs; format in `script-writer.md` |
| `script/chN_load.json` | load-auditor | The load coding: per narration line, its holds (new formulas and terms), questions, ideas and motive sentences (`docs/load-rubric.md`) |
| `audio/` | `vk voice` | `<id>.wav` per clip; `manifest.json`: per clip `duration`, `marks`, `words` (word → start time), `raw` text, cache `key` |
| `music/chN.json` | director | Cue sheet: tracks placed by narration line, never by seconds (`engine/tools/music.py`) |
| `scenes/chN_sK_<slug>.py` | scene-builder | One `NarratedScene` subclass each; module docstring = design notes |
| `media/` | tools | `videos/` renders; `check/<stem>_beats.png` per-scene review image; `chN_holds.png`; `cues/` real clip times per render (music uses them); `logs/`; per-scene caches |
| `out/` | `vk final` / `vk preview` | `chN_<slug>.mp4` (1080p60), `chN_<slug>_preview.mp4` (480p15) |
| `source/` | you | The material, or the course's `../source/` |
| `archive/` | anyone | Superseded versions kept for reference |

## The `vk` command
`engine/vk` runs every step. Run it from inside a project folder, or pass `-C <project folder>`
from anywhere. Agents always use the absolute path plus `-C`.

| Command | Does |
|---|---|
| `vk new <folder> "<Title>" "<course line>" [--lang L] [--source files…]` | Scaffold a project (and its course if new), move/copy the material in, list it in projects/INDEX.md |
| `vk status` | Per chapter: script lines, narration voiced/changed, music, scenes built/skeleton/missing, video fresh/stale |
| `vk voice [N]` · `vk retime [N]` | Voice new/changed lines (all chapters, or N); redo timings only |
| `vk voice [N] --qa-only` · `vk qa [N] [-v] [--all]` | Consensus voice QA (Whisper base + small + medium; 2 of 3 must agree) on cached clips; list flagged sentences, expected → heard |
| `vk regap N [--scale X] [--speed V] [--fixed] [--seed S] [--only ID …] [--revert]` | Pace voiced chapter N without re-voicing (no TTS, no AI, ~10 s): sentence gaps get seeded random lengths, the silence after each line varies, everything × `--scale` ({pause}s too). Defaults = the house pacing (varied, scale 2; `tools/regap.py` HOUSE), which `vk voice` already applies to every line it voices, so this is for projects voiced before 2026-11-03 or other values; `--speed 0.8` slows the speech itself (Rubber Band R3, pitch kept); `--fixed` keeps the original gaps. Shifts the word timings to match. Always starts from the originals in `audio/.pre-regap/`, so re-running with other values is safe; `--revert` restores them. Then `vk finalize N --no-review` |
| `vk packet <stem>` | One scene's brief + narration with sentence start times (a builder's input) |
| `vk build <stem> [--context "…"] [--notes "…"]` | Build (or, with `--notes`, fix) one scene with Codex (GPT-6.1 Sol, medium effort) using the scene-builder instructions; prints its report, minutes and tokens; logs in media/codex/ |
| `vk check <stems…> \| --chapter N [--no-render] [--frames t…] [--render-anyway]` | Dry-run audit (errors, overruns, dwell, layout lint, and a transition audit of every play: text morphed into other text, text revealed in pieces, texts drawn over each other mid-transition, raised `~`, labels > 2 s before their word), then 480p render + beats image only once no overrun/sync/layout/transition flag is left (`--render-anyway` overrides). Transition flags block only in scenes marked `# style: 2`; older scenes get them as advice. A scene marked `# handover: next` must end on the shot the next scene opens on, and once both have 480p renders the join's two frames are compared (`vk final` repeats it at 1080p) |
| `vk holds N` | Each line's last still frame after its final word, from the render's `media/cues/` timings → `media/chN_holds.png` |
| `vk lecture <video> [--chunk S] [--until T] [--name N]` | Lecture recording → source/<stem>.transcript.md (Whisper medium, local), .digest.md (Gemini: screen verbatim, diagrams, Q&A, demos), .captions.md (embedded subtitles); recorded in project.json |
| `vk review N [--file F] [--transitions]` · `vk review <stem…>` | Gemini watches the final chapter, or scenes' 480p renders → media/review/*_review.md: scene @ time (clip) [kind] expected → observed; visual findings near motion tagged mid-transition. `--transitions`: visual problems only, including brief jumbles during animations (the stock prompt ignores those) → *_transitions.md |
| `vk listen N [--only id…]` | Gemini ear-checks the voiced narration against the script → media/review/chN_listen.md (`clip:sentence "script" → "heard"`, +qa = the Whisper vote agrees) |
| `vk load N… [--rail] [--wpm W] [--timing …]` · `vk load N --list` · `--check` | The load gate (below) on `script/chN_load.json` → media/review/chN_load.md; exit 1 if any chapter is "over". `--list` prints the lines sentence by sentence (the auditor's keys), `--check` validates a coding without the verdict, `--rail` prints the holds in order as rail candidates (DEEP_STYLE §15) |
| `vk preview N` · `vk final N` | Render all scenes in parallel and stitch (480p15 / 1080p60 with music) |
| `vk render --chapter N --only <stem>` | Re-render some scenes and re-stitch |
| `vk audition <ref.wav>` · `vk usage` | Try a voice reference · tokens per agent of the latest session |

The tools resolve two roots (`engine/lib/paths.py`): ENGINE (code, venvs, assets) and the
PROJECT (the nearest `project.json` at or above the working directory, or `$VK_PROJECT`).

## The load gate (DEEP_STYLE §13, §0; thresholds from `docs/load-calibration.md`)
After the continuity review and before voicing, one `load-auditor` per chapter (Sonnet, in parallel)
codes the script with the fixed rubric in `docs/load-rubric.md`. It is independent: it never edits
the script and never sees the writer's counts. Then `vk load N…` places every hold and question in
time and checks the chapter:

| check | pass | kind |
|---|---|---|
| holds per minute H (new formulas + new terms) | mean ≤ 1.9 (target 1.3–1.8) | load |
| H − Q (questions to the viewer per minute) | mean ≤ 1.4 (target 0.7–1.2) | load |
| holds in any 2-minute window | ≤ 8 (lines of one stated `pattern` count once) | load |
| words per idea · motive sentences per idea | ≥ 45 · ≥ 0.25, chapter means | substance ("thin explanation") |
| a question in every 2-minute window | listed as advice, not a fail | questions |

The report lists every flagged window with its lines and holds, and keeps load flags apart from
"thin explanation". A chapter that's "over" goes back to its writer with `media/review/chN_load.md`,
and is re-audited after the rewrite. Timing is the best available:
- the rendered scenes' `media/cues/`;
- else the voiced lines (`audio/manifest.json`, + 3.7 s of visuals per scene);
- else the script, at the voice's 190 wpm with the project's own pacing (`regap.pacing()`).

The script estimate was within ±3% of the finished videos on the nine calibration chapters.
`--wpm W` swaps in §13's rule of thumb (W per minute of video, plus `{pause}`s), which ran 3–13% long.
After voicing, `vk load` runs again as a check; log H in STATUS.md so the band can be re-fitted.

## Review standard (what directors check)
- `vk check --chapter N --no-render` is clean, or each remaining flag is accepted for a reason
  the brief gives, and recorded in STATUS.md.
- The holds image, seen once per round, shows:
  - frames that match the narration;
  - consistent sizes, colours and placement across scenes;
  - exact code;
  - nothing cramped, cut off or half-empty.
- A holds tile is the clip's last still frame after its final word (from the render's
  `media/cues/` timings), so a missing element is a real bug. `~` = never held still, `?` = no
  cue file (rough guess): confirm those with the builder first.
- Fix notes are observable and tied to a beat label. They go to the original builder via
  SendMessage when it finished less than ~1 h ago, otherwise to a fresh builder. At most two rounds.

## Recovery
- **A usage limit or crash mid-run:** start `claude` in the studio and say "continue <project>".
  The producer runs `vk status`, reads STATUS.md and picks up at the first unfinished stage.
  Half-written scenes keep a `STATUS` block in their docstring, which `vk packet` shows the next
  builder.
- **A voice line fails QA across seeds:** change the text, not the seed (ear rules in
  `chapter-director.md`). False alarms on jargon are normal.
- **A render fails:** the error is in `media/logs/<stem>.log`, and `vk check <stem>` shows a short
  traceback.
- **An agent type is missing:** restart `claude` in the studio (agent folders are watched only
  if they existed at startup), or use the general-purpose fallback in `CLAUDE.md`.
- **A video is stale** (scenes or cue sheet changed after it): `vk final N`.

## Design notes
- **Nested agents, not one big session.** Cost is roughly turns × context size, and the first
  lecture's main session grew to 854k context. Each level now holds only its own concerns: the
  producer sees plans and reports, a director one chapter, a builder one scene. Nesting depth is 2
  (producer → director → builder), within Claude Code's default limit of 3.
- **Agents skip CLAUDE.md** (`omitClaudeMd: true`) and carry their whole kit in their system prompt,
  which is cached and identical across builders. Builders read a ~1k-token packet instead of
  docs, sources and other scenes.
- **One director at a time** keeps CPU contention (each builder renders) and usage bursts in check.
  Two at once roughly halves wall time.
- **Why not a Workflow script:** the director's loop (review → judge → fix → re-review) and the plan
  checkpoint need judgment and occasional user input. A saved workflow could later run the
  mechanical parts (all builders of a chapter) deterministically.

## Setup (once per machine)
macOS on Apple Silicon, [uv](https://docs.astral.sh/uv/), Homebrew `ffmpeg`, `poppler`
(`pdftotext`), a TeX install (MacTeX/TeX Live, for `MathTex` and CMU Serif), and the toolchain for
the code on screen (e.g. OCaml 5.4 via opam).
```sh
cd engine
uv venv -p 3.11 .venv     && uv pip install --python .venv/bin/python -r requirements-manim.lock
uv venv -p 3.12 .venv-mlx && uv pip install --python .venv-mlx/bin/python -r requirements-voice.lock
```
Model weights download on first use (Chatterbox Turbo fp16 ≈ 2.8 GB, Whisper base, and Whisper
small + medium for MLX voice QA ≈ 2 GB in the Hugging Face cache). The
`*.lock` files pin exact versions. `requirements-*.txt` are the loose top-level lists.
