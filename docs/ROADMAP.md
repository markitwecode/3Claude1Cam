# Roadmap: findings, provisional numbers, tightenings, tasks

One place for what we've learned and what's still open (started 2026-11-04). The rules themselves live in
`docs/DEEP_STYLE.md`; pitfalls already paid for live in `docs/LESSONS.md`.

## Findings (where they're written down)
- **3b1b vs us, measured** (`docs/3b1b-study.md`). 3b1b isn't slower: he speaks 174 words per minute of
  video against our 132, and is silent 23% of the time against our 40%. We packed in 1.5× the ideas and
  2.2× the new formulas per minute, at half the words per idea (28 vs 58). He gives 3× the motive sentences
  and 2× the questions per idea. He shows the picture first and the formula as its caption; only 8% of his
  frames are maths-only, against our 23%. His "pause and ponder" holds last 1–5 s, because the viewer
  presses pause. The doc ends with 13 rules (now `DEEP_STYLE.md` §11).
- **The load equalizer** (`docs/load-calibration.md`, rubric `docs/load-rubric.md`). Holds per minute
  separate "felt fine" from "too dense": H counts new formulas and terms the viewer must hold. Comfortable
  chapters run at 1.35–1.87, dense at 2.05–3.57. Questions offset load: H − Q separates the groups about 3×
  more cleanly. Ideas per minute, words per idea, voice speed and "jumps" didn't separate them.
- **The deep pilot** (`projects/nst-maths/l10-deep-oscillations`). L10 §2.6 (4.5 min of lecture) became 4
  parts, 58 min, at ~158M tokens of context reads. The user: "yeah i love it … the questions are quite
  nice". It is the model for both styles.
- **Gemini's visual reviews dropped** (`docs/LESSONS.md`, "Scheduling study: the sample"). Frame-checked
  on 5 chapters: 1 minor real finding, 2 false, 1 transient. The ear (`vk listen`) stays: it caught 9 real
  mishearings in the same run.
- **GPU** (memory, not a repo doc). Middle.app held ~40% of the GPU. The baseline is the 4K monitor at
  "looks like 2560×1440" and 120 Hz.

## Provisional numbers to recalibrate
Each needs the user's ratings of the first auto lecture, and more over time.
1. **Load thresholds** (H 1.3–1.8, max 1.9; H − Q ≤ 1.4; peak 9 in 2 min). They come from 8 chapters, and
   subject is tangled with rating: the comfortable ones are DE plus the pilot, the dense ones all maths.
   Grow the set: after each watched chapter, record "comfortable / dense / too slow" in its STATUS.md, and
   re-fit when there are ~20.
2. **Substance floor** (≥ 32 words and ≥ 0.20 motive sentences per idea). This is a producer's guess,
   meant to be ~30% more explanation than the pilot. Every existing chapter fails it, the loved pilot
   included. Check that chapters which pass don't feel padded; if they do, lower the floor.
3. **Pacing 1.5×** for styled projects. The thresholds were measured at 2×, and 1.5× makes the same script
   ~8% denser per minute. The gate compensates, but confirm it by ear.
4. **Auditor reliability.** It's a single Sonnet coder. On L12 ch1 the two calibration coders gave 1.25
   and 1.64. Consider a second coder whenever a chapter lands within ±0.15 of a limit.
5. **auto's length and cost**: unmeasured. My guess is 1.2–1.5× the classic length. Measure them with
   `vk usage` on the first auto lecture.

## Tightenings (not built yet)
- **Check the remaining 3b1b rules automatically.** "You" ≥ 1.5 per 100 words, and no lecture references
  aloud ("the notes say", "equation seventy-seven"), as regex checks in `vk load`. After the render:
  frame motion ≥ 5%, still-while-speaking ≤ 50%, picture frames ≥ 75%, using the study's frame tools
  (`engine/reference/3b1b/study/tools`), as advice in `vk finalize`.
- **Move-card length.** Over ~70 characters a card still wraps onto 3 lines and touches the column's
  first line. Lint it in `vk check`, or have the writer keep under 70.
- **Rail capacity.** About 10 entries fit, and past that `rail` raises an error. The planner should plan
  removals; `vk load --rail` lists the candidates.
- **`derive_step` and the rail haven't been used in a real chapter yet.** Watch the first auto lecture for
  them.
- **A missing lib helper:** live readouts (a number that updates beside a sweep). Every pilot scene
  built its own.
- **Pilot leftovers** (small, in its STATUS.md): ch2 runs 17 min, over the 14 cap; two move cards wrap a
  word; a "not to scale" label crosses the spring in ch3; a 9 s silent build in ch4 s3.
- **Older projects:** databases L4 c8.text.1 and c9.pairs.3 still say "semijoin" unhyphenated; a label in
  L4 ch3 s6 appears 2 s early; FoCS L5 ch5's "Part 5" label.

## Portability blockers (fix before packaging as a skill; found writing docs/SETUP.md, 2026-11-05)
SETUP.md gives a workaround for each, but a newcomer shouldn't need any of them.
1. **This machine's path is hard-coded:** `/Users/markgolbraikh/Documents/3Claude1Cam` appears in all five
   `.claude/agents/*.md` files and in CLAUDE.md. Make it relative, or resolve it at start.
2. **`engine/lib/style.py:17` loads the CMU fonts from `/usr/local/texlive/2023/…`.** Any other TeX Live
   year fails with an AssertionError. Look the font up with `kpsewhich cmunrm.otf`.
3. **`engine/tools/gemini.py`:** without `agy` installed, `vk listen` crashes instead of exiting 3
   ("skipped").
4. **No album:** the director can write a music cue sheet naming tracks that don't exist, and `music.py`
   then crashes the final render. Skip the music when there's no album.
5. Smaller ones:
   - `slots.py` assumes a 32 GB Mac.
   - `vk new --source` can't copy a folder from outside the studio.
   - `paths.py` has anaconda fallbacks.
   - LICENSE: MIT since 2026-11-05; `engine/reference/3b1b/` stays CC BY-NC-SA (NOTICE.md) and covers the
     3b1b-derived files (CC BY-NC-SA 4.0).

## Tasks for later
- **Package the studio as a skill** (the user, 2026-11-04: "we should really format it as a skill").
  Someone drops in a voice sample and a folder of material, picks auto or deep, and gets videos. The
  setup guide (`docs/SETUP.md`) is the first step. A skill would bundle the producer runbook (CLAUDE.md),
  the five agent definitions, `vk` and the bootstrap (venvs, models, ffmpeg-full, LaTeX), with the
  user-specific bits (paths, the Gemini CLI, the music album) made optional or configurable.
- **Study companions** (`DEEP_STYLE.md` §10): an Anki deck of each chapter's moves, hint ladders for
  example sheets, a one-page moves sheet per lecture, interleaved review questions, mp4 chapter markers
  at each scene and think stop, and a learner profile in COURSE.md.
- **Re-pace or restyle older lectures** on request. The classic projects stay at 1080p and 2× pauses.
