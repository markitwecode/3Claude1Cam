# 3Claude1Cam

A studio that turns study material into 3Blue1Brown-style videos: narrated by a cloned voice,
animated in ManimCE, with the 3b1b soundtrack underneath. Claude produces them by directing a team
of agents. You tell it what you want.

## Using it

Codex can also produce videos from this folder: its entry point is `AGENTS.md`, with
adapted roles in `.codex/agents/`. See [the Codex workflow](docs/CODEX.md) for production,
resource limits, recovery and comparison checks. The Claude workflow below remains available.

Start `claude` in this folder and say what you need:

- "Make videos for FoCS lecture 5 from `projects/focs/source/focs-202627-v1.8.pdf`."
- "I need a video on Dijkstra's algorithm, about 10 minutes."
- "Here are my notes on red-black trees (`~/Downloads/rb.pdf`): make a series."
- "Finish lecture 3." / "Continue." / "Where are we?"
- "In lecture 3 chapter 4, the trace is too small. Fix it."

Claude plans the series and shows you the plan: how many chapters, how long, what each covers,
and roughly what it costs. Once you say go, it writes the scripts, voices them, and has each
chapter animated, reviewed and rendered without further input. Finished videos land in
`projects/<…>/out/`. It tells you which lines to listen to, because TTS mistakes can only be
caught by ear.

To see progress at any time: `projects/INDEX.md`, or `engine/vk -C <project folder> status`.

## Layout
- **`engine/`:** shared and topic-independent. The `vk` command, scene library, tools, venvs,
  music, voice reference, and the manim / 3b1b reference.
- **`projects/`:** one folder per video series: plan, status, scripts, audio, scenes, renders,
  finished videos.
- **`.claude/agents/`:** the planner, script-writer, chapter-director and scene-builder.
- **`docs/`:** `PIPELINE.md` (how it works; setup), `LESSONS.md` (pitfalls), `STYLE.md` (look).
- **`CLAUDE.md`:** the producer's runbook, which Claude reads automatically.

## Notes
- **Voice:** Chatterbox Turbo (MLX) cloned from `engine/assets/voice/refs/ref_c.wav`, ~160 wpm.
  Try another reference with `engine/vk audition <clip.wav>`.
- **Music:** "The Music of 3Blue1Brown" (Vincent Rubinetti). Private study use only; publishing
  needs his permission (form at vincerubinetti.github.io/using-the-music-of-3blue1brown).
- The folder is a git repo for the text (scripts, scenes, docs, engine code). Renders, audio,
  venvs and the album are ignored.
