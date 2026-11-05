# Setup: from a fresh Mac to your first video

This guide is for a newcomer. It gets the studio running on your Mac, then shows how to use it.

## The short version
1. **Install the tools once** (§1): Claude Code, a few Homebrew packages, MacTeX, and two Python
   environments.
2. **Drop in a voice sample:** 12–15 s of clean speech, saved as
   `engine/assets/voice/refs/ref_c.wav` (§2). Every video is narrated in that voice.
3. **Put your material in a folder:** the lecture's PDFs, slides, notes, or a recording (§3).
4. **Start `claude` in the studio folder and ask** (§5): *"Make videos of lecture 3 from
   ~/Desktop/linear-algebra-l3/"*. Add *"in depth"* for the deep style.

From there, Claude plans the series, writes and voices the narration, animates and checks every
scene, and renders the finished chapters into the project's `out/` folder. It doesn't stop for
approval along the way; you can interrupt it at any time.

Every command below was checked against the code. Paths are relative to the studio folder (the clone)
unless they start with `/` or `~`.

## 1. Prerequisites

### The machine
- **An Apple Silicon Mac (M1 or later), macOS 14 or later. This is required.** The voice (Chatterbox
  Turbo), the Whisper voice checks and lecture transcripts all run on MLX, which runs only on Apple
  GPUs (`mlx-metal` ships wheels for macOS 14, 15 and 26 on arm64 only). The rendering half would run
  elsewhere, but nothing could be voiced.
- **Memory:** every number in this guide was measured on an M1 Max with 32 GB. A voice run holds ~7 GB,
  each scene being rendered holds 0.75–1.6 GB, and ~5 chapters are built at once. A memory budget in
  `engine/tools/slots.py` assumes 32 GB (`VK_JOB_GB=19`). On a 16 GB Mac, set `VK_JOB_GB` lower (§4)
  and ask Claude to build two chapters at a time. 16 GB is untested.
- **Disk:** about 15 GB for the tools (MacTeX ~8 GB, the models ~5.5 GB, the two environments ~1 GB),
  plus ~2 GB per finished lecture (renders, audio, videos).
- **A path without spaces.** The agents run commands with unquoted absolute paths.

### Claude Code
Install Claude Code, and sign in with an account that can use Opus. The planner, writers, directors and
scene builders run on Opus, and the load auditor runs on Sonnet. A lecture is a big job (cost in §5),
so plan for a Max subscription or API billing.
```sh
curl -fsSL https://claude.ai/install.sh | bash
claude --version        # tested with 2.1.318
```

### Homebrew packages
Install [Homebrew](https://brew.sh) first; it also installs Apple's command-line tools (git, a
compiler). Then:
```sh
brew install uv cairo pkg-config ffmpeg ffmpeg-full poppler
brew install --cask mactex-no-gui
```
| Package | Why |
|---|---|
| `uv` | Creates the two Python environments, and downloads Python 3.11 and 3.12 itself if they're missing |
| `cairo`, `pkg-config` | pycairo (Manim's renderer) has no macOS wheel and is built from source against them |
| `ffmpeg` | Stitching, music mixing, audio cuts. The tools call plain `ffmpeg` / `ffprobe` from your PATH |
| `ffmpeg-full` | The labelled review images (`vk check`, `vk holds`) need the `drawtext` filter, which Homebrew's plain `ffmpeg` dropped in 9.0.2. `ffmpeg-full` has it but is keg-only (not on PATH), so install both. `engine/lib/paths.py` finds it at `/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg`. It also pulls in `rubberband`, which `vk regap --speed` uses |
| `poppler` | `pdftotext` / `pdftoppm`, which Claude uses to read and render PDF pages |
| `mactex-no-gui` | Full TeX Live: LaTeX for every `MathTex` formula, and the CMU Serif font (Computer Modern, the 3b1b look) |

Open a **new terminal** after MacTeX, so `/Library/TeX/texbin` is on your PATH (`which latex dvisvgm`).
BasicTeX also works if you add the packages Manim lists, plus `cm-unicode` (`sudo tlmgr install …`).
The other fonts, Menlo (code) and Arial (labels on review images), ship with macOS.

### Get the studio
```sh
git clone https://github.com/markitwecode/3Claude1Cam.git ~/3Claude1Cam
cd ~/3Claude1Cam
```

### Two fixes you need on your machine (until the engine stops hard-coding them)
**1. Point the agents at your clone.** The agent files and `CLAUDE.md` name the author's studio path,
`/Users/markgolbraikh/Documents/3Claude1Cam`. Replace it with yours:
```sh
OLD=/Users/markgolbraikh/Documents/3Claude1Cam
grep -rl "$OLD" .claude/agents CLAUDE.md | xargs sed -i '' "s|$OLD|$PWD|g"
grep -rn "$OLD" .claude/agents CLAUDE.md      # prints nothing when done
```

**2. Make CMU Serif findable.** `engine/lib/style.py` loads the font from TeX Live 2023's folder,
`/usr/local/texlive/2023/texmf-dist/fonts/opentype/public/cm-unicode/`. If the folder is missing,
importing `lib.style` stops with `AssertionError: font doesn't exist`, and so does every scene. MacTeX
today installs TeX Live 2026, so link its font folder there:
```sh
kpsewhich cmunrm.otf        # where your TeX has the font, e.g. /usr/local/texlive/2026/…/cm-unicode/cmunrm.otf
CMU="$(dirname "$(kpsewhich cmunrm.otf)")"
sudo mkdir -p /usr/local/texlive/2023/texmf-dist/fonts/opentype/public
sudo ln -s "$CMU" /usr/local/texlive/2023/texmf-dist/fonts/opentype/public/cm-unicode
```
Skip this step if `kpsewhich` already prints a `/usr/local/texlive/2023/` path.

### The two Python environments
`engine/vk` runs the tools from two venvs inside `engine/`, which must have exactly these names and
Python versions:
- `.venv` is Python 3.11 with ManimCE 0.22.0, for rendering and checks. The agents' instructions name
  `.venv/lib/python3.11/`.
- `.venv-mlx` is Python 3.12 with mlx-audio, faster-whisper and soundfile, for voice, Whisper QA,
  transcripts, pacing and the load gate.

The `*.lock` files pin every package. The `requirements-*.txt` files list only the top-level ones.
```sh
cd engine
uv venv -p 3.11 .venv
uv pip install --python .venv/bin/python -r requirements-manim.lock
uv venv -p 3.12 .venv-mlx
uv pip install --python .venv-mlx/bin/python -r requirements-voice.lock
cd ..
```

### Models (downloaded on first use)
Nothing to do by hand. The weights go to the Hugging Face cache (`~/.cache/huggingface`, or
`$HF_HOME`) the first time a tool needs them:

| Model | Size | First needed by |
|---|---|---|
| `mlx-community/chatterbox-turbo-fp16` (the TTS) | ~3.0 GB | `vk audition`, `vk voice` |
| `mlx-community/S3TokenizerV2` (Chatterbox's speech tokenizer) | ~0.5 GB | the same, fetched with it |
| `Systran/faster-whisper-base` (CPU; word timings and the first QA vote) | ~0.15 GB | the same |
| `mlx-community/whisper-small-asr-fp16` (second QA vote) | ~0.5 GB | `vk voice` |
| `mlx-community/whisper-medium-asr-fp16` (third QA vote, lecture transcripts) | ~1.5 GB | `vk voice`, `vk lecture` |

## 2. Bring your own voice
**Consent first.** Only clone a voice you have the right to use: your own, or that of someone who has
explicitly agreed to it. Don't clone a public figure or anyone else without their permission, and don't
present the narration as a real person's speech.

**Where it goes.** The code reads one file, `engine/assets/voice/refs/ref_c.wav`, as set by
`VOICE["ref"]` in `engine/tools/voice.py` (relative to `engine/`). The folder isn't in the repo; create
it:
```sh
mkdir -p engine/assets/voice/refs
# trim to the first 15 s of speech, mono 24 kHz 16-bit WAV (the format of the original reference)
ffmpeg -i ~/Desktop/my-voice.m4a -ss 0.3 -t 15 -ac 1 -ar 24000 -c:a pcm_s16le engine/assets/voice/refs/ref_c.wav
```

**What makes a good sample** (from `docs/LESSONS.md`, "Voice"):
- **Length:** 12–15 s is ideal, and anything under 5 s is a hard error. Chatterbox Turbo uses only the
  first 10 s for the timbre and the first 15 s for the speaking style, so the opening matters most.
- **Start on speech:** trim any leading silence.
- **Clean:** one speaker, a quiet room, no music, no reverb, no clipping.
- **The pace you want:** the clone copies the reference's speaking rate. The original reference was a
  fast speaker (~270 wpm), so a calm, steady read gives calmer narration. To slow down a fast sample,
  stretch the *reference*, not the output: `rubberband --tempo 0.85 in.wav ref_c.wav`. Stretching the
  output sounded warbly.

**Hear it before you commit.** `vk audition` voices a sample paragraph exactly as the pipeline would.
The clip you test must be inside `engine/`, and the result is `engine/assets/voice/audition_<name>.wav`:
```sh
engine/vk audition engine/assets/voice/refs/ref_c.wav engine/assets/voice/refs/take2.wav
afplay engine/assets/voice/audition_ref_c.wav
```
Copy the take you like to `ref_c.wav`. The voice cache is keyed on the reference's *content*, so if you
swap it later, the next `vk voice` re-voices every line, and the scenes need re-rendering to match.

## 3. Bring your material
Put everything for one lecture (or topic) in a folder: PDFs of the notes, slide decks, handouts,
example sheets, images, a lecture recording. You can keep the folder anywhere and tell Claude where it
is. Or drop the files into the studio's root folder, and they'll be moved into place.

What Claude (the producer, following `CLAUDE.md`) does with it:
- **It picks the project folder:** `projects/<course>/lNN-<slug>/` for a course lecture (lectures of a
  course share `projects/<course>/source/`), or `projects/<slug>/` for a one-off topic.
- **It runs one command:**
  `engine/vk new <folder> "<Title>" "<Course · Lecture N>" --lang <lexer> --source <files…> [--style deep|classic]`.
  This creates the course (`COURSE.md`, `source/`) if it's new, and the project's `project.json`,
  `PLAN.md`, `STATUS.md` and its `script/ audio/ music/ scenes/ source/` folders.
  - Material from inside the studio is **moved** into `source/`, and material from elsewhere is
    **copied**.
  - It records the material in `project.json` `"sources"` and adds a line to `projects/INDEX.md`.
  - `--source` takes files, not a folder, so the producer passes the folder's files.
  - `--lang` is the Pygments lexer for code on screen (`ocaml`, `python`, `sql`, `verilog`, …). Leave it
    out for no code.
- **A lecture recording** goes into the course's `source/` and is processed in place:
  `engine/vk -C <project> lecture <video>`. It takes ~3 min per 20 min of lecture and writes three files
  next to the material:
  - `<stem>.transcript.md`: Whisper medium, local;
  - `<stem>.digest.md`: Gemini's notes on the board and slide content, diagrams, emphasis and student
    questions (it needs `agy`, §4);
  - `<stem>.captions.md`: the video's own subtitle track, if it has one.

  Recordings stay out of git (`**/source/*.mp4`).
- **No material at all** ("a 10-minute video on Dijkstra's algorithm") is fine: the planner researches
  the topic on the web.
- **Code or numbers on screen** are run for real. The writer verifies every example with the actual
  toolchain, which the planner records in `project.json` `"toolchain"`. Install what your material
  needs: OCaml via `opam`, DuckDB, `sympy` for maths, and so on.

## 4. Optional pieces

### Gemini, through the Antigravity CLI `agy`
Gemini watches and listens, which Claude can't. It's used at two points by default:
- `vk lecture`: the digest of a recording;
- `vk listen`: an ear-check of the voiced narration against the script, which catches mispronunciations
  that Whisper's text can't show.

`vk review` (Gemini watching rendered video) still works, but only when you ask for it.

To use it, install Google's Antigravity CLI and sign in once. It runs on your Google account's quota,
which is weekly. The old `gemini` CLI isn't used. The studio finds `agy` on your PATH, at
`~/.local/bin/agy`, or wherever `VK_AGY` points; it was tested with agy 1.4.7 and 1.5.0, and the default
model is `gemini-3.8-flash-medium` (`engine/tools/gemini.py`).

**Without it, set `VK_GEMINI=0`** (in your shell, or in `.claude/settings.local.json`, below). Then:
- `vk listen` and `vk review` print "skipped, Gemini is off" and exit 3, and the chapter directors
  switch to their "When Gemini is off" rules: the three-model Whisper vote (`vk qa`) is the ear, and
  `vk check`'s transition audits plus contact sheets cover motion.
- `vk lecture … --no-digest` still writes the transcript and captions. The planner works from those
  plus the slides or notes, and samples frames with ffmpeg where the board matters.
- If you don't set it and `agy` is missing, those commands fail with "agy not found" instead of
  skipping.

When the quota runs out, a circuit breaker writes `engine/logs/gemini-off`, and every Gemini call
skips for 24 h (`VK_GEMINI_OFF_HOURS`) or until you delete the file.

### Music
The 3Blue1Brown album ("The Music of 3Blue1Brown", Vincent Rubinetti) isn't included. For private
study, you can buy it ([Bandcamp](https://vincerubinetti.bandcamp.com)) and put the tracks in
`engine/assets/music/album/`. Any format ffmpeg reads works there, and other music you have the rights
to works the same way. **Publishing a video with his music needs the composer's permission:**
[request form](https://vincerubinetti.github.io/using-the-music-of-3blue1brown).

How it's used: each chapter director writes a cue sheet, `music/chN.json`, which places tracks by
narration line (`assets/music/album/<file>`, relative to `engine/`). The final render mixes them in,
ducked under the voice (`engine/tools/music.py`). Loudness is measured once per track and cached in
`engine/assets/music/.loudness.json`.

**Without an album, say "no music" when you start a project.** A chapter without `music/chN.json` is
rendered with narration only. A cue sheet that names missing tracks makes the final render fail.

### Settings for the agents' shells
Environment variables that every agent's commands should see go in `.claude/settings.local.json` (not
committed). For example:
```json
{ "env": { "VK_GEMINI": "0", "VK_JOB_GB": "8" } }
```
| Variable | Default | What |
|---|---|---|
| `VK_GEMINI` | `1` | `0` turns Gemini off everywhere |
| `VK_AGY` | PATH, then `~/.local/bin/agy` | Where `agy` is |
| `VK_FFMPEG_TEXT` | `ffmpeg-full`, then PATH | An ffmpeg with `drawtext`, for review images |
| `VK_JOB_GB` | `19` | Memory budget for heavy jobs (voice 7, lecture transcript 3, 1080p render 1.2, 480p preview 0.75, audit 0.6). `8` on a 16 GB Mac is a guess |
| `VK_GPU_SLOTS` · `VK_MANIM_SLOTS` | `2` · `10` | Upper bounds on GPU jobs and Manim processes |
| `VK_PRESSURE_GATE` | `1` | `0` stops new jobs from waiting while macOS reports memory pressure |

### Codex as a fallback builder
`vk build <stem>` builds one scene with OpenAI's Codex CLI (`codex`, signed in), off the Claude quota.
It's only for when Claude is at a usage limit: a whole lecture built this way came out clearly worse.

### Reference clones (for the curious; the agents don't need them)
`engine/reference/INDEX.md` and `engine/reference/3b1b/` cite sources that aren't redistributed (see
`engine/reference/3b1b/NOTICE.md`). To follow those citations:
```sh
cd engine/reference
git clone --branch v0.22.0 --depth 1 https://github.com/ManimCommunity/manim.git manim-v0.22.0
git clone https://github.com/adithya-s-k/manim_skill.git manim_skill                 # cited at cef0450
git clone https://github.com/3b1b/videos.git 3b1b/videos                             # cited at 306a134
mv 3b1b/videos/CLAUDE.md 3b1b/videos/GRANT_CLAUDE.md.txt    # or Claude Code loads it as instructions
git clone https://github.com/3b1b/manim.git 3b1b/manimgl                             # cited at fafa083
cd ../..
```
The scene builders look APIs up in the installed source (`engine/.venv/lib/python3.11/site-packages/manim/`),
which is always there.

## 5. Using it
Start Claude Code in the studio folder; it reads `CLAUDE.md` and acts as the producer:
```sh
cd ~/3Claude1Cam
claude
```
The agents run shell commands (`engine/vk`, python, ffmpeg) for hours. Choose a permission mode that
lets them do that without a prompt for every command (`claude --help`, `--permission-mode`), or be
ready to approve a lot.

### Example prompts
- "Make videos of lecture 3 from `~/Desktop/linear-algebra-l3/`."
- "Here are my notes on red-black trees (`~/Downloads/rb.pdf`): make a series. No music."
- "Do lecture 5 of databases in depth, from the slides and the recording in `inbox/`."
- "I need a video on Dijkstra's algorithm, about 10 minutes."
- "Where are we?" / "Continue." / "Finish lecture 3."
- "In lecture 3 chapter 4, the trace is too small. Fix it."
- "It says 'O-camel'. Make it say 'oh-camel'."

### The teaching styles
Set per project by `"style"` in `project.json`. The spec is `docs/DEEP_STYLE.md`, and its §0 says which
rules apply to which style.

| Style | Ask for | What you get |
|---|---|---|
| **auto** (default) | nothing special | The lecture, enhanced. Its coverage, order and examples are kept, and every gap is fixed in place: steps split until each is atomic, a motive for each move, missing prerequisites built from the ground up, an intuition picture |
| **deep** | "in depth", "deep style" | Rebuilt from first principles, restructured freely. The model is `projects/nst-maths/l10-deep-oscillations/` (4.5 min of lecture became 4 parts, 58 min) |
| **classic** | "classic style" | The style before 2026-11-04: 1080p, 2× pauses, no load gate |

auto and deep share the newer defaults:
- finals at 2560×1440, with one idea's picture and its derivation on screen together;
- a pinned legend and a reference rail;
- named key moves, and a recap built from them;
- 2–4 "pause and ponder" think stops per chapter;
- varied pauses at 1.5×;
- the load gate.

### What happens, stage by stage
1. **Plan.** A `series-planner` reads the material and writes `PLAN.md` and `project.json`: chapters of
   8–14 min, each with a goal, a scene list and an ending recap. Claude shows you the summary (chapters ×
   minutes, cost and time estimate, its judgment calls) and carries on without waiting.
2. **Scripts.** One `script-writer` per chapter, in parallel, writes `script/chN_<slug>.md`: the spoken
   narration (written for the ear), `{marks}` for animation cues, and a visual brief per scene. Every
   code example and number is checked with the real toolchain. The planner then reviews all scripts
   for continuity.
3. **Load gate** (auto and deep). One `load-auditor` per chapter (Sonnet) codes the script for holds
   (new formulas and terms), questions and ideas, and `vk load` checks the rates: holds per minute,
   holds minus questions, the peak in any 2 minutes, and words and motive per idea. A chapter that's
   "over" goes back to its writer. Details: `docs/PIPELINE.md`, "The load gate".
4. **Voice.** `vk voice` runs locally, with no tokens. Each sentence is voiced on its own, three Whisper
   models vote on what was said, and misheard sentences are retaken with new seeds. Word timings and
   the house pacing (varied pauses) are applied.
5. **Chapters.** One `chapter-director` per chapter, ~5 at once:
   - narration fixes, with Gemini as the ear when it's on;
   - the music cue sheet;
   - one `scene-builder` per scene in parallel, each writing one ManimCE file in `scenes/`;
   - audits (`vk check`), a review of one settled frame per narration line (`vk holds`), and at most two
     fix rounds.
6. **Finals.** `vk finalize N…` renders each chapter at full quality with the music mixed in, and checks
   its format and scene joins. Its summary goes to `media/review/chN_finalize.md`.

State lives in files, not in the conversation. If a session dies (a usage limit, a crash), start
`claude` again and say "continue <project>": it resumes at the first unfinished stage.

### Where things land
- **Videos:** `projects/<…>/out/chN_<slug>.mp4`, at 2560×1440 60 fps (auto, deep) or 1920×1080 60 fps
  (classic). Previews (`_preview.mp4`, 480p15) go in the same folder.
- **Progress:** `projects/INDEX.md`, the project's `STATUS.md`, or `engine/vk -C <project> status`.

### Time and cost
These are rough figures from the author's runs (M1 Max, 32 GB; `CLAUDE.md`, `docs/ROADMAP.md`):
- **Voice:** ~70 min per hour of narration.
- **Chapters:** ~3.5 chapters an hour with ~5 directors at once; a pair takes ~45–60 min.
- **Finals:** ~5 min per chapter.
- **A lecture recording:** ~3 min per 20 min of video.

A one-hour lecture is roughly an afternoon, mostly unattended.

**Claude tokens,** at API list prices:
- Digital Electronics L6 (6 chapters, 61 min, classic style) cost ~$195: builders 64%, directors 22%,
  writers 8%, producer and planner 7%.
- With the fixes since, a classic lecture is estimated at ~$115–125.
- The deep pilot (58 min) read ~158M context tokens over 47 agents.
- auto's length and cost aren't measured yet. The guess is 1.2–1.5× classic.

`engine/vk usage` prints the tokens per agent of the latest session.

## 6. Check the install
Run these from the studio folder, in order:
```sh
engine/vk help                                                   # the command list (needs no venv)
engine/.venv/bin/manim --version                                 # Manim Community v0.22.0
engine/.venv-mlx/bin/python -c "import mlx.core as mx; print(mx.default_device())"   # Device(gpu, 0)
/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg -hide_banner -filters | grep drawtext       # one line
ls /usr/local/texlive/2023/texmf-dist/fonts/opentype/public/cm-unicode/cmunrm.otf    # the font link
```
**A quick test render**, which exercises Manim, LaTeX, the CMU font and the scene library together
(~5 s at 480p):
```sh
cat > /tmp/vk_hello.py <<'EOF'
from manim import *
from lib.style import BLUE, T


class Hello(Scene):
    def construct(self):
        self.play(Write(T("Hello from 3Claude1Cam", size=48)))
        self.play(Write(MathTex(r"e^{i\pi} + 1 = 0", color=BLUE).shift(DOWN)))
        self.wait()
EOF
(cd engine && PYTHONPATH=. .venv/bin/manim -ql --media_dir /tmp/vk_hello --disable_caching /tmp/vk_hello.py Hello)
open /tmp/vk_hello/videos/vk_hello/480p15/Hello.mp4
```
**A one-line voice test.** The first run downloads Chatterbox and Whisper base (~3.7 GB):
```sh
engine/vk audition && afplay engine/assets/voice/audition_ref_c.wav
```
**End to end:** ask Claude for something small, such as *"a 3-minute video on why the sum of the first n
odd numbers is n squared, no music"*. It runs every stage on a single short chapter.

## 7. Troubleshooting
The full list, with the measurements behind each item, is `docs/LESSONS.md`.

| Symptom | Cause and fix |
|---|---|
| Every scene fails with `AssertionError: font doesn't exist at /usr/local/texlive/2023/…` | The CMU font link (§1, fix 2) |
| `no ffmpeg with the drawtext filter` from `vk check` / `vk holds` | `brew install ffmpeg-full` (keep plain `ffmpeg` too), or set `VK_FFMPEG_TEXT` to an ffmpeg that has it |
| `LaTeX compilation error` in a render log | TeX isn't on PATH (open a new terminal after MacTeX), or BasicTeX lacks a package |
| `pycairo` fails to build during `uv pip install` | `brew install cairo pkg-config`, then re-run the install |
| An agent type is "not found" | Claude Code watches only the agent folders that existed when it started: restart `claude` in the studio folder |
| An agent works in the wrong folder, or can't find `engine/vk` | The agent files still name the author's path (§1, fix 1) |
| A render fails | The error is in `projects/<…>/media/logs/<stem>.log`; `engine/vk -C <project> check <stem>` shows a short traceback. Render through `vk render` / `vk check`, never bare `manim` on a project's scenes: parallel renders need their own caches, and Manim's cache breaks sync, so the tools always pass `--disable_caching` |
| A narration line is flagged after several retakes | Change the text, not the seed. Write for the ear: spell single letters ("ex", "ell"), avoid bare letters at the start of a sentence, prefer plain words, and phrase things positively ("has at least one element", not "isn't empty"). Whisper false alarms on jargon ("OCaml" → "O-camel") are normal |
| The narration is too fast | The clone copies the reference's pace: use a calmer sample, or slow the reference (§2) |
| The Mac crawls, or swap grows | Too many heavy jobs at once. Lower `VK_JOB_GB`, ask for fewer chapters in parallel, and run one bulk `vk voice` at a time (slots.py enforces that) |
| `vk listen` fails with `agy not found` | Install `agy`, or set `VK_GEMINI=0` (§4) |
| Gemini says "skipped, Gemini is off" | The quota ran out. It switches back on after 24 h, or when you delete `engine/logs/gemini-off` |
| A session stopped halfway (usage limit) | Start `claude` and say "continue <project>" |
| Voicing is very slow after an install change | Keep Chatterbox on MLX (`mlx-audio`). The PyTorch `chatterbox-tts` ran 2.5–12× slower than real time on MPS |
