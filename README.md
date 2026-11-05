# 3Claude1Cam

A studio that turns study material (lecture notes, slides, a recording, or just a topic) into
narrated, 3Blue1Brown-style explainer videos. Claude Code produces them by directing a team of agents.
They plan the series, write the narration, voice it in your own cloned voice (Chatterbox Turbo, locally
on Apple Silicon), animate every scene in ManimCE, check the result and render the finished chapters.
You point it at a folder and say what you want.

**Start here: [docs/SETUP.md](docs/SETUP.md).** It covers the install, bringing your own voice and
material, and the styles (auto, deep, classic).

## What's in the repo
- **`engine/`:** the shared, topic-independent part.
  - `vk`: one CLI for every pipeline step.
  - `lib/`: the scene library (style, narration sync, transitions, the teaching widgets).
  - `tools/`: voice, Whisper QA, pacing, the load gate, render, music, checks, Gemini.
  - The pinned requirement and lock files.
  - `reference/3b1b/`: our notes on how 3b1b builds his videos
    ([NOTICE](engine/reference/3b1b/NOTICE.md)).
- **`.claude/agents/`:** the five agent types: series-planner, script-writer, load-auditor,
  chapter-director and scene-builder.
- **`CLAUDE.md`:** the producer's runbook, which Claude Code reads when you start it here.
- **`projects/`:** the example series, with their plans, scripts, scene code, music cue sheets and
  status notes. They cover Cambridge lectures in FoCS, Digital Electronics, NST Maths and Databases, a
  cross-product one-off, a tour of the studio itself, and the deep-style pilot
  (`nst-maths/l10-deep-oscillations`).
- **`docs/`:** how it works, what was measured, and what went wrong.

## What isn't
- **Lecture material:** every `source/` folder (course PDFs, recordings, their transcripts and
  digests).
- **Voice samples** (`engine/assets/voice/`), and narration audio (`audio/`), since that is the cloned
  voice. Bring your own: [SETUP §2](docs/SETUP.md#2-bring-your-own-voice).
- **Renders and finished videos** (`media/`, `out/`, `archive/`).
- **The music album.** The 3Blue1Brown soundtrack isn't ours to share
  ([SETUP §4](docs/SETUP.md#music)).
- **Third-party clones:** 3b1b's `videos` and `manim`, the ManimCE docs, `manim_skill`, and contact
  sheets of 3b1b's videos.
- Python environments, model weights and logs.

So the example projects are there to read: they have no audio or source material. With your own
voice they can be re-voiced (`vk voice`) and rendered, though nobody has tried that from a fresh clone.

## Docs
| Doc | What |
|---|---|
| [SETUP.md](docs/SETUP.md) | From a fresh Mac to your first video |
| [DEEP_STYLE.md](docs/DEEP_STYLE.md) | The teaching styles. §0 says what auto and deep each do; also the load gate (§13) and the reference rail (§15) |
| [3b1b-study.md](docs/3b1b-study.md) | Experiment: 8 of 3b1b's videos and 4 of ours, measured the same way. He isn't slower; he gives twice the words per idea, three times the motive, and a picture first |
| [load-calibration.md](docs/load-calibration.md) | Experiment: the measured load per minute (holds, questions) that separates "felt fine" from "too dense". Rubric: [load-rubric.md](docs/load-rubric.md) |
| [ROADMAP.md](docs/ROADMAP.md) | Findings so far, provisional numbers to recalibrate, what's next |
| [PIPELINE.md](docs/PIPELINE.md) | How it fits together: stages, file formats, every `vk` command, recovery |
| [LESSONS.md](docs/LESSONS.md) | Every pitfall paid for so far, with numbers |
| [STYLE.md](docs/STYLE.md) | The visual style, long form |

## Using it
After [setup](docs/SETUP.md), start `claude` in this folder and say what you need:
- "Make videos of lecture 3 from `~/Desktop/linear-algebra-l3/`."
- "Do lecture 5 in depth." (deep style; auto is the default)
- "I need a video on Dijkstra's algorithm, about 10 minutes."
- "Where are we?" / "Continue." / "In chapter 4, the trace is too small. Fix it."

Claude shows you the plan (chapters, minutes, rough cost) and goes straight on. It writes and checks
the scripts, voices them, has each chapter animated, reviewed and rendered, and reports when it's done.
The finished videos land in `projects/<…>/out/`. To check progress at any time, read
`projects/INDEX.md` or run `engine/vk -C <project folder> status`.

## Notes
- **Mac only:** Apple Silicon, macOS 14 or later. The voice and the Whisper checks run on MLX.
- **Voice:** Chatterbox Turbo (MLX), cloned from `engine/assets/voice/refs/ref_c.wav`. Only clone a
  voice you have permission to use.
- **Music:** "The Music of 3Blue1Brown" (Vincent Rubinetti) is optional and not included. Publishing a
  video with it needs his permission
  ([form](https://vincerubinetti.github.io/using-the-music-of-3blue1brown)).
- **Gemini** (through Google's Antigravity CLI `agy`) is optional. It digests lecture recordings and
  ear-checks the narration. Without it, a three-model Whisper vote is the ear.
- **Builders** are Claude (Opus). `vk build` can build a scene with Codex instead, as a fallback at a
  Claude usage limit.
- **Licence:** `engine/reference/3b1b/` is CC BY-NC-SA 4.0, as derived from 3b1b's video code
  ([NOTICE](engine/reference/3b1b/NOTICE.md)).
