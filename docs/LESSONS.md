# Lessons learned

Everything that went wrong, or nearly did, while making FoCS Lecture 3 (Oct 2026), and what we
do now instead. Read this before changing the engine or the pipeline. Paths are as of the
2026-10-23 restructure (`engine/`, `projects/`).

## Token budget (measured 2026-10-23 from the session transcripts)

The first production run (ch1 v1 + v2, research, the ch2–5 scene wave) processed ~450M tokens of
context (439M cache reads + 13M cache writes) and hit the plan's limit with chapters 2–5 half
built. A turn re-reads the whole context, so **cost ≈ turns × context size**. Where it went:

- **The orchestrator session: 170M (38%).** One session did everything (research, voice
  experiments, ch1 reviews, 35 agent launches, 32 follow-ups) and grew to 854k context. The hour it
  spent supervising the ch2–5 agents cost 63M over 82 turns, ~0.8M per turn mostly to read a
  notification. Now: a fresh session per chapter, and the orchestrator never does hands-on scene
  work (CLAUDE.md, docs/PIPELINE.md).
- **Scene agents: ~170M for ~20 scenes (≈ 6–11M per scene).** Each started at ~31k and grew to
  200–460k:
  - ~15 turns of onboarding (STYLE, LESSONS, all 500 lines of PATTERNS, the whole chapter
    script, lib sources, 2–4 complete ch1 scenes, even tool *sources* and manifest dumps:
    60–80k);
  - then 20–60 turns of render → contact sheet → ffmpeg grab → image → heredoc patch;
  - plus ~85k of thinking that stays in context.

  Now:
  - the `scene-builder` agent type, whose cached system prompt is the distilled kit;
  - `vk packet` (engine/tools/packet.py), the scene's brief and sentence timings in ~1k tokens;
  - `vk check` (engine/tools/check.py), one command whose dry-run lint finds cut-off, overlapping or small text,
    ghosts, overruns and dwell problems without anyone looking at images, plus one beats image;
  - `engine/lib/kit.py`, the helpers that 2–5 scenes had each re-implemented.
- One-off research (3b1b patterns, GL→CE, music): ~90M. Done once; every future lecture reuses it.
- Images cost ~2–4k tokens each and stay in context for every later turn; ~300 were read.
  `check.py` makes one beats image per run, labelled with the narration cue.
- Polish passes sent hours later to a 300–400k agent re-wrote its whole cache before doing
  anything. Send fixes soon after a builder finishes, or start a fresh builder with the notes.
- **Result** (ch2 s4–s6, the first run of the new process): 2.3–3.8M per scene (avg 3.1M),
  each finished and check-clean in one pass with 2–3 check runs. Before it was 6–11M per scene,
  and those scenes were unfinished and unreviewed. A fix pass sent to a builder that had just
  finished cost ~0.4M. The biggest remaining item is thinking, ~80k of a ~200k peak.
- My own review from the downscaled holds tile was wrong once: I saw a "left-heavy" table that
  actually spanned the frame. The builder measured and pushed back. Verify before sending a
  composition note, or phrase it as a question.
- Agent types (`.claude/agents/*.md`) are hot-reloaded, but only from folders that existed when
  `claude` started. The `agents/` folder was created mid-session, so the type was invisible until
  a restart (`/clear` doesn't restart). The general-purpose fallback worked as well (ch3).

## Pacing and depth (the big one)

- **v1 was too fast and too shallow.** It compressed an hour-long lecture into 8 minutes at
  about 195 words/min. The verdict was "comprehending even at 1x is damn near impossible".
- Now: **chapters of ~8–10 min, ~45 min per lecture**, covering *everything* in the notes
  (pitfalls, worked examples, exact cost derivations), each chapter ending in a recap.
- Narration pace: **~160 wpm**, from voicing each sentence separately and joining them
  with a 0.55 s breath (`VOICE["sentence_gap"]`). The user picked this ("B") by ear.
- Use `{pause}` / `{pause=1.5}` in the script for deliberate holds after key reveals and
  before answers ("pause and think").

## Voice (TTS)

- **Use Chatterbox Turbo via `mlx-audio` (MLX), not the PyTorch `chatterbox-tts`.**
  PyTorch on MPS ran 2.5–12× *slower* than real time; MLX runs 2.5–3.5× *faster* than
  real time on an M1 Max. The PyTorch package also pins torch 2.6 and numpy<2, and its
  watermarker needs `setuptools<81` (`pkg_resources`).
- **The clone copies the reference's speaking rate.** `ref_c` is a fast speaker (~270 wpm),
  which is why raw output runs ~200 wpm.
  - Rejected: time-stretching the *output* (`rubberband` at 0.9) sounded warbly to the user.
  - Works: time-stretching the *reference* (fresh synthesis at a slower pace, no
    artifacts). 0.85 → ~154 wpm, 0.75 → ~138 wpm. The user still preferred plain ref + breaths.
- Reference clip: at least 5 s (hard error below). Turbo uses only the first **10 s** for timbre and the
  first **15 s** for speaking style. Start on speech, with no leading silence. 12–15 s is ideal.
- **Write for the ear.** Lines that broke in v1:
  - Bare single letters as variable names ("x", "l") came out stuttered or garbled across 3+
    seeds. Spell them: "ex", "ell", and give them commas: "some head, ex, consed onto…".
  - "Here's one: three, five, nine" was heard as the list 1, 3, 5, 9. Say "Here's an example:".
  - "caret" came out like "character". Say "the caret symbol".
  - "flatly refuses" was mumbled. Prefer plain, common words.
  - Spell numbers and identifiers as spoken: "add-len", "rev-app", "big O of n".
  - A colon ends a voiced chunk, so the text after it is voiced on its own. A fragment like
    "a list of any type…" came out as "O-wist of any type". After a colon, start with a strong
    word, or use a comma ("…alpha list, which means a list of…").
  - "en" (for n) next to a word starting with a vowel sound merges: "exactly en conses" was
    heard as "exactly unconscious". Say the idea instead: "one cons per element".
  - Avoid negative contractions where a slip flips the meaning: "lists that aren't empty" came
    back as "lists that are empty". Phrase it positively ("has at least one element").
  - QA maps "ex"/"ell"/"why" back to x/l/y (`SPELLED` in voice.py), because Whisper writes letters.
    Vector names too: "ay"/"bee"/"see"/"eye"/"jay"/"kay" (both sides go through `norm`, so a real
    "see" still matches; an "ay" voiced as "eye" still gets flagged).
  - Vector-letter words are fragile: "Ay" opening a sentence comes out "aye"/"eye", and "ay"/"kay"
    can turn into "AI"/"chi". Put a word before them ("In other words, ay cross bee…", "First, ay
    one…"). Subscripts ("ay one") still get flagged because Whisper writes "a1"; that one's a false
    positive (cross-product, 2026-10-25).
- **If a line fails across several seeds, change the text, not the seed.**
- Seeds must change per retry; the same seed reproduces the same glitch.
- Loudness across clips is very consistent (±0.6 dB). The stitch step still runs `loudnorm`.

## Running voice jobs safely

- **Two voice runs at once used to corrupt the manifest.** Each loaded `manifest.json` at
  start and rewrote the whole file after every line, so a long chapter-2 run silently reverted
  the chapter-5 lines another run had just re-voiced. The new audio was left with the old
  timings. Writes now go through `update_manifest()` (file lock, re-read, merge one entry,
  atomic replace). Still, prefer one sequential run (`voice.py` with no `--chapter` does
  everything) because they share one GPU anyway.
- Editing narration with search-and-replace can hit `{mark}` names too. `{id}` became
  `{eye-dee}`, which is no longer a valid mark (hyphen), so it would have been *spoken*. Only
  replace inside the narration text, and grep for `{[a-z]*-` afterwards.

## Automatic QA (Whisper)

- `faster-whisper`'s own file decoder breaks with newer PyAV (`metadata_errors` kwarg).
  Always pass a 16 kHz numpy array.
- Word error rate (WER) gives **false alarms on jargon**: "OCaml" → "O-camel",
  "A, B, C" → "ABC", "three, five, nine" → "359", "add-len" → "Adlin". Don't chase them.
- WER **misses repeated phrases**: "Tail hands back the X. Tail hands back the L." was only
  7% WER. Hence the separate **stutter** metric (3 or more inserted words = bad).
- QA is per sentence: only the failing sentence is re-voiced. The best take is kept.
- **Whisper base misses real mishearings** (FoCS L4, 2026-10-26). Directors that re-checked
  every line with base, small and medium, and fixed what two of the three agreed on, found 4–13
  bad lines per chapter that `vk voice` had passed: "nil" → "no", "append and zip" → "a pendant
  zip", "type error" → "tie bearer", "halve" → "have", a doubled "one" in a list of numbers. Fix
  the text, not the seed. Since 2026-10-27 `vk voice` runs this consensus itself (see
  "2026-10-27 engine changes").
- Don't pipe `vk voice` through `tail`: the per-sentence "still flagged" lines exist only in its
  output, and the manifest keeps only line-level WER and stutter.
- **We can't hear the audio, and the user doesn't check by ear** (2026-10-28): `vk listen` (Gemini)
  is the ear. A Gemini-only finding gets a slight rewrite, a re-voice and `vk listen --only` again.

## Sync between animation and narration

- **Never hard-code seconds** (`c.start + 4.2`). v1's agents wrote 157 of them, and every
  re-voiced line silently desynced. Cue on `{marks}` or on any spoken phrase:
  `c.wait_until("hands back the ell")`. The manifest stores every word's time.
- The first-pass alignment can be off. One v1 mark was 0.7 s early until re-timed.
  `voice.py --retime` redoes the timings without re-voicing.

## Manim

- **The cache also breaks sync.** A cached `play()` advances the scene clock by its exact
  `run_time`, but its stored segment has a whole number of frames, while a fresh play advances
  by the frames it writes. Cached plays add up to a frame each that the narration doesn't know
  about: Hook went from 708 to 710 frames and WhatIsAList from 1304 to 1309, so by the end of
  the scene the picture was ~0.33 s behind the voice. **`engine/tools/render.py` always passes
  `--disable_caching`.** Previews are fast enough fresh, and every scene renders in parallel.
- **The cache drops sounds.** A `play()` served from the cache leaves the renderer in
  "skipping" mode until the next `play()`, and `add_sound` is silently ignored while skipping.
  Re-renders came out with missing narration. Fixed in `NarratedScene.say` (it restores the
  skip state first). Don't remove that.
- **Parallel renders race on the shared `media/texts` and `media/Tex` caches** (FileNotFoundError
  on an SVG). `engine/tools/render.py` gives each scene its own via a per-scene config file, in
  `media/cache/<stem>/`. They must NOT be nested inside `media/Tex`: manim's cleanup of the
  shared folder tries to delete nested folders and crashes (PermissionError). Always render
  via `vk render --chapter N --only <stem> --no-stitch` or `vk check`, never bare `manim` with hand-made configs.
- `Indicate()` floods opaque-filled boxes (cons cells, cards) with solid colour and hides the
  label. Use a stroke-only pulse instead.
- `TransformMatchingShapes` on multi-line code can fling glyphs across lines. Swap single
  tokens in place instead.
- **Never wrap on-screen sub-objects in an `AnimationGroup`/`Group` to animate them.**
  `play()` adds the wrapper to the scene as a new top-level object. That (1) pulls the parts out
  of their parent, so a later `remove(parent)` leaves ghosts behind (seen with `Code` glyphs),
  and (2) re-layers them on top, so opaque cell boxes covered their own values and dots
  (ch1 cells scene). Pass the animations to `play()` directly, one per part.
- `Text` has no glyphs for whitespace, so glyph indices ≠ character indices. `lib.style.Code`
  handles the mapping (`code.find(...)`, `code.line(i)`).
- The Pygments OCaml lexer splits `'a` and `::` oddly. `Code` re-colours them with a regex pass.
- Arrows built with `link(..., follow=True)` are redrawn every frame and ignore colour animations.
- Manim's logs are wrapped by `rich`, so `grep` misses phrases split across lines.
  Use `COLUMNS=400` when grepping logs.

## Rendering and assembly

- One manim process per scene, all in parallel: 8 scenes at 480p15 take ~15–20 s, and at
  1080p60 ~90 s, on the M1 Max.
- Stitch with `-c:v copy` and re-encode only the audio. Use `aresample=async=1` so the gaps
  between scenes stay as silence; otherwise narration can drift. Verified within 5 ms.
- Contact sheets (`tools/sheet.sh`) select frames by real timestamp, with the label at the
  bottom. The earlier version used the `fps` filter, mislabelled frames by up to ~1 s, and
  covered the top margin.
- **Stay on Cairo + libx264. GPU options were benchmarked and lost** (2026-10-24, ch4_s3_trace,
  1080p60, M1 Max; full write-up in `docs/bench/2026-10-24-renderers.md`):
  - **Where the time goes.** About 76% of CPU time is encoding (x264 plus the colour conversion).
    By wall time, Cairo drawing is about 45%, and the main thread waits on the encoder about 37%.
  - **OpenGL renderer: 0.54× (slower).** It makes ~29k draw calls through macOS's deprecated GL.
    Porting it means:
    - `set_z_index` doesn't exist, and nothing else controls layering;
    - plain `VMobject()` crashes when mixed with OpenGL objects;
    - `set_cap_style` doesn't exist;
    - text renders heavier;
    - the picture drifts ahead of the narration by 7 frames per minute.
  - **`h264_videotoolbox`: 0.88× on one scene and 17% slower for 8 scenes at once,** though it
    uses half the CPU. The Mac's hardware encoder is a single engine shared by every process.
    It needs quality mode (`flags=+qscale`, `global_quality≈7670`); in bitrate mode the first
    frames of each segment come out blurry.
  - **`--max-inflight-encoders 4`: 1.3–1.5× on a single-scene render, bit-identical output,
    ~2.6 GB RAM per scene.** It gives nothing when 7–8 scenes render at once, so it's only
    worth using for fix passes.

## Don't write manim from memory

- The user insisted on this, rightly. `engine/reference/INDEX.md` indexes the official v0.22.0
  example gallery, tutorials and guides, plus the `manimce-best-practices` rules and examples
  (also installed as a project skill). Look things up there or in the installed source.
- Context7 (live docs) is available once its OAuth login is done
  (`mcp__plugin_context7_context7__authenticate`).
- Searched in Oct 2026: no public manim skill covers voiceover sync, pacing, caching or
  parallel rendering. That knowledge lives only in this file and STYLE.md.
- Grant uses ManimGL; we use ManimCE (better docs, pinned releases, per-animation cache,
  headless parallel renders). His video code in `engine/reference/3b1b/` is still essential for
  *style*. Port ideas through `GL_TO_CE.md`, never paste.
- Downloaded repos can ship a `CLAUDE.md` (3b1b/videos does), which Claude Code would
  auto-load as instructions when working in that folder. Rename such files on download.

## Look (calibrated against 3b1b)

- **Size units differ.** ManimGL makes a "0" 1 unit tall at font_size 144, so 48 → 0.33 units.
  In CE, `MathTex` matches (0.34 at 48) but `Text` renders ~35% bigger (0.45 at 48), so our
  `T(…, 36)` ≈ his default `Text` 48. Ch1 v2's "everything looks small" was about
  **composition** (the hero diagrams spanned ~15% of the frame width), not font size.
- His 1.5× saturation boost (`eq=saturation=1.5` in his ffmpeg pipe) barely changes our
  palette and tints our background slightly green. Tested; not adopted.
- Measured pacing: median beat 3 s, ~40% of it still; meaningful transforms ~2 s; no `Indicate`.
  Details in `engine/reference/3b1b/PATTERNS.md`.

## Screen time

- Viewer feedback on ch1 v2: "keep the onscreen stuff for a bit longer… you preemptively remove
  stuff even where there is free space". The worst case was OCaml's reply `- : int list = [3; 5; 9]`,
  readable for ~1 s. The cause was our own STYLE.md rule "do transitions at the start of the
  next block": every agent cleared the board on the first word of each new line.
- `vk dwell` (also part of `vk check`) audits it in seconds (a dry run, no rendering). It found 65 pieces of text
  in ch1 removed before they could be read twice. Run it before every render you show anyone.

## Music (see engine/reference/3b1b/MUSIC.md for the evidence)

- 3b1b: no music-only intro (he speaks from frame 0 over a quiet bed); beds come and go under the
  narration; dense explanation stays dry; no stings or interludes; music carries ~18 s of end
  screen. We use: a hook bed, at most one mid-chapter bed under a *visual* stretch, and a bed
  over the recap and an ~8 s end card. Beds sit ~20–25 dB under the voice.
- Our first ducking settings (threshold 0.02, ratio 6, release 600 ms) *pumped*: −19 dB under speech,
  springing back to −5 dB in every 0.55 s sentence breath. Use ratio 2, release 2000 ms.
- `music/chN.json` cues name narration lines (`"c1.ht.4:end"`), never seconds, and each chapter gets
  its own tracks. Avoid tracks with lots of energy in the speech band (300–3400 Hz) under speech:
  the solo piano Etudes, Trinkets, Wading.
- The end-card music at the under-speech level (−27 LUFS) sounded thin once the voice stopped.
  Cue option `swell_after` (+6 dB over 1.5 s after the last line) lifts it to ≈ −21 LUFS.
- **Licence:** private study only. Publishing with this music needs the composer's form.

## Working with agents

- Brief: `STYLE.md` plus a finished reference scene, then a render → contact sheet → fix loop.
  Each agent took ~15–25 min per pair of scenes.
- Agents report confidently. Review their contact sheets and exact frames yourself before
  trusting a report.
- Agents hard-coded Whisper timings when bookmarks felt too coarse. That's now forbidden in
  STYLE.md, and phrase cues remove the reason for it.
- Review a chapter with `vk holds N` (one settled frame per line) rather than fixed-interval
  contact sheets. Those mostly catch mid-transform frames once transforms take 1.5–2 s.
- Polish passes go back to the agent that built the scene (SendMessage). It already knows the
  scene, so a pass takes ~8–12 min instead of a rebuild.
- Never let two agents edit `engine/lib/` at once. Agents put helpers in their own scene files.
- (ch3, 2026-10-23) A holds frame can be sampled just before a clip's last cue, so an element
  "missing" there may appear a moment later. Ask the builder to confirm from its frames first.
- (ch3) `vk check` requires every scene to end on an empty frame. When one scene flowed into the
  next, the earlier one used to fade the shared shot out and the next faded it back in. In DE L8
  (2026-10-31) that gave ~1.5 s of near-black mid-thought at 7 of 42 joins (ch2, ch5, ch7). It
  reads as a blink, and Gemini flagged it. Now such a scene is marked `# handover: next`, ends on
  the shot without fading, and the next opens with it already on screen
  (`load_scene(stem).handover_shot()`, lib/paths.py). `vk check` and `vk final` compare the join's
  two frames (tools/handover.py: at 480x270, a pixel differs past 32/255, and a join fails past
  0.2% of pixels or on an empty frame). The same frame encoded two ways measures 0.00%, and a
  30-pixel shift measures 1.8%. A topic change keeps the fade to empty: that break is wanted. L8's
  videos were left with their dips (the user's call).
- (ch3) A whole chapter took 16M context tokens: 4 builds, 2 small fixes, 3 fix passes; the
  orchestrator 2.3M. Builders read 1.1–3.9M each, peaking at 75–195k.

## Layout (2026-10-23 restructure)
- One studio, two kinds of folder: `engine/` (code, venvs, assets, reference; topic-independent)
  and `projects/<…>/` (everything specific to one series). Tools find the project by walking up to
  `project.json` (`engine/lib/paths.py`). Moving the venvs only broke their console-script
  shebangs, which were rewritten in place. The voice cache key hashes the reference *content*, so
  moving `ref_c.wav` re-voiced nothing.
- The title card text and the code lexer come from `project.json`, so a non-FoCS topic needs no
  engine change.

## 2026-10-27 engine changes (from a pipeline review, checked against the transcripts)
- **Consensus voice QA.** `vk voice` now has Whisper small and medium (MLX, GPU) vote alongside
  base. A sentence two of the three mishear the same way is retried; what's still flagged is
  stored in manifest `qa` and listed by `vk qa N` (counted in `vk status`), so piping the output
  through `tail` no longer loses it. Jargon, homophones, numbers and spoken punctuation are
  normalised away; swaps of only "a"/"the"-type words are `minor` (`--all`). Timings still come
  from base alone. Cost: ~+20% voice time, zero tokens.
- mlx-audio's Whisper transcription loop invents sentences after the speech ends, and its fallback
  writes gibberish. voiceqa decodes each window once, greedily, and stops at the end of speech.
- **`vk holds` sampled the wrong moments.** It summed durations from t=0, so animation outside
  `say` blocks threw it off by up to 5.1 s (l04 c7.types.5). It now uses the real clip starts in
  `media/cues/` and takes the last still frame after each clip's last word, before the next clip.
  `~` = never settles, `?` = no cue file (old guess).
- **`vk check` renders only once overrun, sync and layout flags are fixed.** Builds averaged ~5
  check runs and ~5 beats images, many made while flags were still open. Dwell doesn't block (6 of
  7 finished l04 ch1 scenes carry an accepted one). `--render-anyway` is for accepted flags.
- **Builder lookups.** Builders grepped engine/lib ~2.7× per build, mostly for return types and
  behaviour of helpers the prompt already named, so scene-builder.md now carries the full library
  API with exact signatures (+1.3k tokens, cached).
- **Where a builder's cost is:** thinking is ~80k of a ~132k peak and ~half its dollars (output);
  images are ~10% of context. Effort level (xhigh by default here) is the untested lever; the
  studio-tour build is the first A/B (Opus xhigh / Opus medium / Sonnet).
- To wait for a running voice run, `pgrep -f 'tools/voice.py'` matches its own `zsh -c` wrapper and
  never reports done (a director's wait loop spun forever); use `pgrep -fl 'python.*[t]ools/voice'`.
  voice.py's manifest lock only makes overlapping *writes* safe; since 2026-10-28 the GPU slot
  (engine/tools/slots.py) makes a second voice run wait instead.
- **The letter n.** Spelled "en", Chatterbox sometimes says "on"/"un" (the user heard it in l03;
  Whisper heard "an item's", "own steps"). Capital "N" came back as "n" in 6 of 6 test places.
  Confirmed blind by Gemini (2026-10-28): it ranked "N" best of en / enn / N / ehn / "the letter en"
  (all six clean), with "en" heard as "an" and "own". A single Gemini flag on "N-rev" did not repeat.
- **More letter words (digital-electronics l06, 2026-10-28).** "ar-ess latch" was heard as "hours" /
  "areas": say "reset-set latch". "bistable" came out "bis-table": write "bye-stable". "ay" is
  still read as "eye" mid-sentence, so ch1 said "top input" / "bottom input" instead of a / b.
  "cue", "dee", "ess", "ar", "tee" are in the QA letter maps; Whisper's "Q0" splits into "cue zero".
  Also heard wrong in l06: "clock" → "quack" / "cock" (say "every edge of the clock", or just "every
  edge"), "flip-flops" → "flit-flops", "halve" → "have", "kay-map" → "chi-map", "state" → "stage".
  "ex-or" → "axer" / "exer", but only by Gemini (Whisper fine), so it was accepted; prefer
  "exclusive-or" where it first appears.
- **More voice fixes (digital-electronics l08, 2026-10-31).** "kay" came out "chi"/"kai" even after
  rewording; a capital "K" fixed it (like "N"). Gemini heard "clock-to-cue" as "cock-to-Q": say
  "clock-to-output". Also misheard: "a slower clock" → "quack", "launches" → "wauches", "flip-flop" →
  "foot flop"/"flip-plop", "invalid" with the noun's stress, "Harris and Harris" (say "David and Sarah
  Harris"), and a sentence opening on a bare noun ("Throughput asks" needed an "And").
- **Directors re-voice before building.** l06 ch1 took ~74 min, ~20–30 of them with its short
  re-voice queued behind the bulk ch3–6 run (then one GPU slot), and its scenes then re-rendered
  against the new audio. Since then slots.py allows 2 GPU jobs (`VK_GPU_SLOTS`) and 10 Manim
  processes, so a `vk voice N --only …` runs beside a bulk run. Narration fixes still come first.

## Scheduling study (2026-11-01, in progress)
- Question: how many chapter-directors at once, and does the scheduler need priorities? The old cap
  of two assumed builders render constantly; they render in short bursts and mostly think in the
  cloud (3 directors: CPU ~49% idle, pressure normal).
- Data: `engine/logs/jobs.jsonl` (slots.py: every heavy job's wait, the reason it waited, run time
  and the slots held at its start), `engine/logs/gemini.jsonl` (every agy attempt: duration,
  outcome, error, tokens) and `engine/logs/system.tsv` (CPU idle, load, memory pressure, swap and
  job counts every ~15 s). joblog.py swallows its own errors, so logging can't break a job.
- First look at 5 directors: started together, their narration re-voices coincided (two 7 GB voice
  runs) and memory pressure went to warning, which held L7 ch2's renders. (Staggering starts was
  considered and dropped: the GPU work is the same either way, and no builders exist yet while
  directors re-voice.)
- Applied 2026-11-01 ~11:25 (safe without data): low CPU priority (`nice 10`) for finals
  (render.py, any quality but -ql), bulk voice runs (> 25 lines, voice.py `BULK_LINES`) and lecture
  transcripts (lecture.py). Previews and audits, which block a builder, keep normal priority.
  Gemini waits before a retry (10–30 s; quota or rate errors 2–4 min with up to two extra
  attempts; `VK_GEMINI_BACKOFF` scales it), where it used to retry instantly, once.
  "agy denied" (Gemini tried a shell command in plan mode instead of opening the file) also gets up
  to two extra attempts after 5–15 s: on 2026-11-01 it failed 5 of 9 lecture-digest calls and lost
  two 10-min pieces with only one retry. No quota errors at all in ~76 calls with 6 directors.
- Gemini quota is finite too (the user had 20% left for two days on 2026-11-01). Tokens by stage that
  day (engine/logs/gemini.jsonl, ~80 calls): scene reviews 59% (mostly Gemini's thinking), listens
  15%, lecture digests 15%, final reviews 12%. Round 1 of the scene reviews is the only pre-final
  check that sees motion and caught real glitches (mid-animation jumbles, morphs, LEDs reading as
  bubbles); round 2 mostly re-checks fixes (L7 ch1: 1 of 7 scenes still wrong). Under a tight quota:
  one round, fixes confirmed on frames and holds, re-listens only where Whisper agrees. Final
  reviews: the transitions pass led to real fixes in ~3 of 7 finished chapters (L10 ch2, ch3, ch5) and
  is the only check of the joins; the viewer pass flagged one item across L10's six, a false alarm.
  So `vk finalize` runs only the transitions pass by default (`--with-viewer` adds the other). Listens: one pass per chapter is still
  worth it (Gemini hears stress and sound, Whisper only text: most voice rules came from it).
- When the quota ran out (2026-11-01, ~16:00): the quota backoff would have made every Gemini call
  wait ~10 min before failing. gemini.py now has a circuit breaker: the first call that fails on quota
  writes engine/logs/gemini-off, and every later call in any session fails at once (delete the file to
  turn it back on; it expires after 24 h, and the next call is then a single-attempt probe that re-arms it if the quota is still out; VK_GEMINI=0 by hand). `vk review` and `vk listen` then print
  "skipped" and exit 3, and `vk finalize` renders without a review. The quota ran out with a message
  the pattern didn't know ("invalid model selection" / "status ERROR", 11 failures in a row from
  16:15), so a failure streak also trips it: 6 failed attempts in a row studio-wide, spanning ≥ 2 min,
  switch Gemini off for 1 h (a blip costs an hour; the hourly single-attempt probe re-arms it while
  the quota is out). Antigravity's real message, once it came (17:20): "RESOURCE_EXHAUSTED (code
  429): Individual quota reached … Resets in 55h4m54s"; `_trip` now reads "Resets in XhYm" and stays
  off exactly that long (24 h when no time is given). Fallbacks for directors are in
  chapter-director.md, "When Gemini is off".
- Applied 2026-11-01 ~11:35, with the user: (1) finals split off the director. A director ends at
  "ready for final" after its scene-review rounds and a `vk preview N` handover check;
  `vk finalize N…` (tools/finalize.py, no agent) renders the final, checks the format, runs both
  Gemini reviews (a chapter's reviews overlap the next chapter's render) and writes
  `media/review/chN_finalize.md` with a verdict: "clean", or "look" when a finding is a
  pronunciation or a settled medium/high visual problem (the s1 join hold excepted). "look" gets a
  short chapter-director fix pass; then `vk finalize N --no-review`. Run on L10's six reviews it
  gave ch1 and ch4 clean and one finding each for ch2, ch3, ch5 and ch6, the ones their directors
  had checked by hand. (2) Re-voices ahead of bulk runs: a bulk voice run (label "(bulk)") pauses
  between sentences while a short re-voice holds the other GPU slot (`slots.holders`), up to 15 min
  per sentence. It keeps its own slot and memory. (3) One bulk voice run at a time, enforced in
  slots.acquire (inside the admission lock): a second "(bulk)" run waits, so one GPU slot always
  stays free for short re-voices. Tested: a short re-voice beside a bulk run starts at once.
- First run of the split (L11 ch1, 2026-11-01): `vk finalize 1` (render + transitions pass) gave one
  "look"; a fresh fix-pass director checked it on 5–10 fps frames (a fade-in Gemini misread) in
  ~35k tokens and 44 s, with no re-final. Final scene renders that day: median 163 s, max 330 s at
  nice 10 under 5–6 directors' load, slot wait median 0 s.
- Candidate changes, waiting on the data: CPU priority by job type (previews and short re-voices
  high; finals, bulk voice and audits low: short jobs that block an agent go first), a Gemini slot
  with backoff on quota errors, re-voices ahead of bulk voice runs.
- Proposal (with the user, 2026-11-01): three lanes by who waits. Fast lane, high priority (a
  cached agent is blocked): previews, audits, short re-voices, scene reviews. Slow lane, low
  priority (nobody waits): finals and final reviews, the next lecture's voicing and transcription.
  Cloud lane: the next lecture's plan and scripts, any time. Split finalising off the director: it
  ends after its last scene-review round, a script queue runs `vk final N` + the final reviews in
  the slow lane, and a short fix agent is spawned only for real findings. Rules: stagger director
  starts; no agent waits more than ~5 min on local work (prompt cache); one bulk GPU job at a time.
  Decide with the day's logs: director idle time on finals and reviews, fast-lane waits, CPU idle.

## Engine to-dos (found 2026-11-01, not done)
- `load_scene` reaches only the current project: L10 ch4 and L11 ch1 loaded other lectures' helpers
  by file path or by pointing `lib.paths.project` elsewhere. Give it a project argument.
- FIXED 2026-11-01 (reported by the math session's L10 ch2 builders): `fly()`/`derive()` showed a
  full-opacity copy over its source. Cause: `_clear_alpha` tested one axis and was capped at 0.6, so
  a line dropping to a close row (0.45 below) went opaque at 60% while still on its source. Now it
  tests both axes with the size interpolated, capped at 0.9 for `_FlyCopy` (0.6 kept for `_Carry`,
  which fades out at 55–80%). `derive()`'s run-aligned copy is kept inside the frame (`_on_screen`;
  it had dropped 1.6 units past the left edge). End frames unchanged, so handovers are unaffected.
  Second pass the same day (math L10 ch3's builders: `vk check` still flagged close rows): the
  opacity ramp began at half the clearing point, so the copy was ~0.5 opaque while still on its
  source. `_FlyCopy` now uses `_fly_ramp`: a ghost of at most 0.25 (under the audit's 0.3 line)
  until clear, then full over half the remaining way. Simulated at 121 steps: 21 / 16 / 10 doubled
  frames (close row / next row / diagonal) → 0.
- FIXED 2026-11-01 (math L11 ch3 s4, a wrong-maths transient): `edit()` fades dropped glyphs out
  (0–35%) before new ones fade in (65–100%), so mid-play only the shared glyphs show; with lone
  glyphs reused from a changed term, that read as a wrong formula (e^{2y} → (e^y)^2 showed
  "e² − 2x e^y − 1 = 0" for ~0.5 s). For MathTex/Tex, `_term_pairs` now treats a lone matched glyph
  next to a changed one as part of the changed term (repeated until stable), so the term swaps whole
  and runs of 2+ glyphs still slide. Text and code edits unchanged.
- FIXED 2026-11-01: `set_alpha(mobs, 1)` / `restyle(op=1)` in lib/kit.py couldn't bring back text
  faded to 0 (L7 ch2 s2): a leaf counted as "filled" only if its fill opacity was > 0, so a faded
  glyph was treated as an outline and only its (absent) stroke restored. Text glyphs
  (VMobjectFromSVGPath) now always count as filled; invisible spacers stay invisible.
- The near-black dip between scenes that hand over their picture (L8 ch2) comes from the "end on an
  empty frame" rule.
- FIXED 2026-11-01: `vk check`'s flash-box audit (tools/transitions.py) crashed on a ValueTracker
  left in the scene (math L10 ch7 s4): a ValueTracker keeps its value as a point but has no stroke;
  the loop now skips non-VMobjects, as the other call sites already did.
- FIXED 2026-11-01 (Databases L5 ch1 s1): a scene that rendered at 15 fps (preview) raised at 60 fps
  (final), in `at(own_word=label)` with no fallback cue. An entrance ran 0.07 s past the start of the
  label's word, so "none of its words are spoken from here on". Frame rounding decided which side of
  the word the scene time fell. `Clip.at` now lands the label at once when its word began ≤ 0.5 s ago.
  It changes only cases that used to raise.
- `vk holds` can show a flash's fading tail as a false "stub" (Databases L5 ch2 s2, 2026-11-01).
  `FlashAround`/`Circumscribe` leave no residue in the video: every frame after the flash is
  pixel-identical to a no-flash render. But holds.py judges stillness on 8×8 block means, so the
  last 2–3 frames of a 1-px stroke fading out count as a "still stretch". When that stretch is just
  the 0.2 s minimum (too short for the 0.25 s step back), `show()` returns its first frame, where
  the sliver is brightest. It happens only when a clip's last word lands during the flash and the
  flash is its last motion. Until fixed, treat a thin outline fragment beside a just-flashed element
  on a holds sheet as this, not a glitch. Proposed fix (scratch-tested on the s2 case): in
  `first_hold`, prefer a stretch of `need + back` frames before falling back to `need`. It changes the
  pick in ~20% of windows, so compare a chapter's holds sheet before and after first. Not applied
  mid-production.
- Whisper base runs on the CPU, 14 min per hour of narration; an MLX port would save ~10 min per
  lecture but changes the QA flags (A/B first).

- Math L10 + L11 (2026-11-01, 15 chapters, up to 5 directors, `vk finalize` per chapter): 12
  transitions reviews ran: 5 clean, 7 "look". Of the 7, 2 led to real fixes (L11 ch1: highlight rings
  half a letter off, next to a false claim; L11 ch3: `edit()` dropped the y of e^{2y} for 0.5 s,
  fixed in moves.py) and 5 were false on frames. A "look" cost a 1–4 min frame check by the
  director that built the chapter, resumed with SendMessage (warm context): keep that, not a fresh
  fix-pass director. 3 more reviews failed on the Gemini quota (429) and were accepted on the render
  and handover checks. Session total: 240 agents, 375M context read; the producer 71M (19%), mostly
  notification turns.

## Scheduling study: results (2026-11-01, 11:18–19:45 logs; script in the session scratchpad)
- Throughput: 28 chapters built (DE L7 ×2, L11 ×6, math L10 ×8, L11 ×7, FoCS L5 ×5), first to last
  render 11:18 → 19:28: ~3.5 chapters/h with 3–7 chapters active at once (2 directors on 10-31: ~1.2/h).
- The Mac's knee is ~5 busy directors. At 6–7 all building at once (12:00–12:30) the CPU was
  saturated in 64% of samples and memory pressure at warning in 42%: preview p90 wait 47 s, audit p90
  89 s. At ≤ 5 the fast lane waited ~0–10 s at p90. Waits were for "all 10 manim slots busy" (174),
  memory pressure (146) and the memory budget (61). Keep ~5; a 6th only while others are in
  narration or handed off.
- The GPU was the real bottleneck: 88 GPU jobs (76 short re-voices, 12 bulk), 7.1 h of slot-time.
  Short re-voices waited p90 up to 26 min (13:00) and 5–14 min (13:30–15:30) while the math
  session's chapter-by-chapter bulk voicing held one slot for hours and several directors queued on
  the other. Fix to build: a bulk run should hand its slot over (not just pause) while a short
  re-voice waits, or bulk voicing should run when few directors are in their narration phase.
- Gemini cost ≈ 0.8–1.0M tokens per chapter with one review round (DE L11 6.1M/6, math L10 6.6M/8,
  math L11 5.8M/7), and the weekly quota is ~80M tokens (13.2M used 11:55–15:40 = 16% of the week by
  the user's numbers; rough, and only if the quota counts tokens): ~12 lectures a week at most.
- Chapters without Gemini (FoCS L5 ch3–7) took 26–55 min of director time, against 69–104 min for DE
  L11's with Gemini reviews: the reviews cost wall time too (waiting for them and the fix rounds they
  trigger). Whether they also cost quality is the A/B in projects/INDEX.md "Pending" (Wednesday).
- Working hypothesis (with the user, 2026-11-01), still to be tested: Gemini earns its quota in two
  jobs only. (1) The ear: it hears sound, stress and tone where Whisper returns text ("quack", "A"
  as "uh", "ess ess zero", "Gal" spelled out; most course voice rules came from it), though its value
  falls as the rules pile up. (2) The lecture digest: the only source for what's on the board in a
  recording, though Claude reading sampled frames plus the slides may match it (Gemini's digest was
  wrong in places in L8 and L10). Its visual checks (scene reviews, the final transitions pass) are
  on trial: they cost ~80% of its tokens and doubled director time, and frame sheets caught real
  glitches without them. Test: Wednesday's pass (projects/INDEX.md "Pending"). Few real findings in
  the nine chapters → drop both visual checks; keep the ear and the digest.

## Gemini in the pipeline (2026-10-28, measured)
- Reached through the Antigravity CLI `agy` headless, plan mode, from a scratch dir holding only the
  media; the prompt must say "open it with your file viewing tool, no shell commands" or it tries a
  shell command and returns nothing (engine/tools/gemini.py does this).
- **Hearing:** on l03 ch4, the Whisper vote (base + small + medium) heard 8–9 of Gemini's 10
  pronunciation findings, including "on-rev" and "on wide". l03's "en" lines got through because it
  was voiced with base-only QA. Gemini alone: ~4 false flags per 10 min on a clean chapter, and run
  to run it varies ("on wide" once, "n wide" twice). So the Whisper vote stays; Gemini is the second
  opinion that separates real flags (both hear it) from homophones and number formats.
- **Seeing:** most "glitches" are brief jumbles during a transition (a doubled "append", a scrambled
  trace, `[[3;; 2;; 11]]` mid-transform), visible ~0.6 s; the settled frames were clean (3 of 3
  checked). Its timestamps run ~0.5 s early. A prompt that judges only the settled picture cut 40
  glitch findings to 1, but those transition jumbles are what a viewer sees and what the glitch
  study should fix at the source.
- **Lecture digest:** slides came out exactly (SQL and result table); small scrolling terminal text
  did not (wrong names, 38303 for 30303). ~72k Gemini tokens per 10 min of lecture. Embedded
  Panopto captions agree with Whisper on 95% of words; Whisper is better on code terms.
- **Builder model/effort test (studio-tour, 16 scenes, 2026-10-28):** cost per finished scene
  (median) Opus xhigh $2.86, Opus medium $1.63, Sonnet $0.64; director quality notes per scene 0.5,
  2.2, 3.8. All ended check-clean; Sonnet had the only real bug and the only brief not followed.
  Thinking (output) roughly halves at medium, and so does working time: first build 16.7 → 7.0 min
  (Sonnet 4.6), with fixes 17.1 → 9.6 (5.7). Details: projects/studio-tour/STATUS.md.
- **RAM overload (2026-10-28).** Three sessions at once (two re-voice runs at ~6.4 GB of MLX models
  each, a lecture transcription, `vk check` pools of one Manim process per core, Gemini cuts) filled
  the 32 GB and 18 GB of swap; macOS paused apps. engine/tools/slots.py now runs a measured memory
  budget: each heavy job declares its size (voice run 7 GB, lecture transcript 3, 1080p render 1.2,
  480p preview 0.75, audit 0.6) and starts only if everything running plus itself fits in 19 GB
  (32 minus ~4.5 wired and ~8 apps + sessions; VK_JOB_GB), or if nothing else is running. Count caps
  stay as upper bounds (GPU 2, Manim 10). A first version allowed ONE GPU job: a director's 2-minute `--only`
  re-voice then waited 20–30 min behind a bulk voice run, and the chapter got built on stale
  narration and re-rendered (DE L6). One slot is right for throughput, wrong for latency.
- **Memory pressure gate (2026-10-30).** The declared budget can't see other apps. Codex's DE L6 run
  started with 6.7 GB of swap and a pressure *warning* before any studio job ran. It ran on tighter
  caps (12 GB, GPU 1, Manim 6), checked `kern.memorystatus_vm_pressure_level` by hand and held
  new work at warning. Pressure stayed normal and swap shrank through the whole lecture. slots.py
  now does that check itself: a job waits while pressure is ≥ 2 and studio jobs are running, so
  something can always start. The measured 19/2/10 stay as upper bounds. Its static cuts weren't
  ported: GPU 1 brings back the re-voice queue above, and 12 GB slows every lecture to cover the
  rare tight case that the gate now catches.
- **Digital Electronics letters (2026-10-28).** Scripts say "cue", "dee", "ess", "ar", "tee"; both
  letter maps (voice.py SPELLED, voiceqa.py LETTERS) map them to letters. Whisper writes subscripts
  as one token ("Q0" for "cue zero"); voice.py's `heard_tokens` splits letter+number tokens for
  alignment, as voiceqa's vote already did, so those lines aren't re-voiced for nothing.
  DE L10 (2026-10-31): "ee" (the input E) is in both maps too, and voiceqa's homophones have
  "sight site cite" and "sync sink" (L10's Hunt / Sight / Sync states).
  DE L11: voice.py's SPELLED is now `dict(voiceqa.LETTERS)`, one list instead of two hand-kept
  copies, after "ee", "eff", "gee", "aitch", "em", "pee" and "vee" turned out missing from it.

## Transitions (glitch study, 2026-10-28; docs/glitch-study-2026-10-28.md)
- 81% of 187 Gemini glitch findings were five transition mechanisms: a text morphed into a different text, a copy starting opaque on its source, `sweep_clear`'s fade-out running under the incoming content, matching transforms crossing glyphs, `Write`/lag_ratio half-words. Fixed by `lib.moves` (appear, disappear, swap, edit, fly, derive, during) and a `sweep_clear` that clears before it fills.
- `vk check` now audits every play: morph and partial are read off the animations (exact); overlap samples 25/50/75% and fires where two texts overlap mid-play only. It hit 6 of 7 frame-confirmed copy-overlap cases, and 8 of 8 sampled flags Gemini hadn't reported were real jumbles, so it blocks too. All block only in `# style: 2` scenes.
- Labels: 46% of 648 spoken prose labels came up 1–4 s before their word, mostly one play revealing several labels, or a cue on the sentence start. `c.wait_until(own_word=label)`; the check flags > 2 s.
- CMU Serif draws ASCII `~` as a raised accent: `T()` now writes `∼`. Glyphs of one text at two font sizes differ by ≤ 0.001 in normalised outline, so `_shape_key`'s exact rounding misses them; `lib.moves.glyph_classes` matches within 0.02.
- The stock `vk review` prompt hides transition jumbles (1 found on l03 ch4 vs 51 with `--transitions`).
- **Codex test (GPT-6.1 Sol, medium effort, 2026-10-28):** `codex exec` rebuilt 6 studio-tour scenes in a
  scratch copy with the same builder prompt (stdin must be closed: `< /dev/null`, or it waits forever;
  `--add-dir engine/.locks` for the slots). Fast and lean: 2–5 min and 7–11 commands per scene, all
  check-clean under `# style: 2`, ~1–3k reasoning tokens, no Claude tokens. But a blind Gemini judge
  preferred the finished Opus versions 5 of 6 (mean 7.5 vs 5.3 out of 10). Codex's typical faults: text
  from the previous beat left on screen for 8–10 s, brief deviations, cluttered layouts. Transition
  reviews flagged fewer glitches on Codex (32 vs 49; the new moves help). Not like for like: the Opus
  scenes had had a director's review rounds, Codex one unreviewed pass. Scratch copy and logs:
  scratchpad codex-test/ (session 84c988cb).
- `FlashAround` on one letter or digit flashed its box's top edge first, which read as an overbar (NOT): 3 times in DE L6. It now rings one-glyph targets with a whole circle that fades in and out (a travelling arc beside a digit read as a comma or prime, DE ch3 re-final), and any flash path under 1 unit fades whole; `vk check` advises (`flashbox`) on hand-built boxes round one glyph.
- The overlap check sampled at 25/50/75% and missed a copy crossing a table partway along its path (DE L6 ch3 s3). It now samples every 10%, interpolates moving glyphs between samples, and tests only the movers: 28 more overlaps on the 4 calibration chapters (8 of 8 sampled were real), same check time.
- Not flagged: earlier-beat text left up while new content builds (a blind judge's complaint). A timer can't tell it from the context STYLE.md asks builders to keep, dimmed.
- **Stale holds image (DE L6 ch6, 2026-10-28):** a director judged round 2 from a holds image made 3 h
  before the scene's fix render; `vk holds` hadn't been re-run. Now `vk holds` deletes the old image at
  start, stamps each tile with its scene's render time (`@23h13`), and warns when a scene file is newer
  than its render (an edit after the last check, e.g. while blocking flags skipped the render).
- **Cache expiry was 28% of DE L6's Claude cost (2026-10-28).** A sub-agent's prompt cache expires after
  5 idle minutes; its next turn re-writes the whole context. Builders resumed for fix notes 16 min (median)
  after finishing re-wrote ~87k each: 68% of builder cache writes ($42 of $63). Directors woke once per
  background builder (489 wakes over 6 chapters) and 69% of their writes were rewrites ($12). Now: fix
  passes go to fresh builders unless the original finished < 5 min ago; directors launch builders in the
  foreground, all in one message (one wake per batch); long tool waits are chained into one command.
  Lecture 6 total ~$195 at list prices: builders 64%, directors 22%, writers 8%, producer + planner 7%.
- **Codex builders with a director round (2026-10-28):** a chapter-director reviewed the 6 Codex-built
  test scenes and sent one round of fixes through `vk build --notes`. Codex applied all 41 notes
  accurately in 1.3–5.3 min each (all six in parallel: 5.3 min of wall time). The director judged 4 of 6
  at Opus level, 1 close and 1 needing another pass; a blind Gemini judge then preferred the fixed Codex
  scenes 5 of 6 over the finished Opus ones (mean 8.2 vs 4.5; its absolute scores drift between runs,
  but its preference flipped from Opus 5 of 6 before the round). The director's Claude cost was $2.88
  for 6 scenes. So builders now default to Codex, with Claude scene-builders as the fallback.
  Codex's habits: rough first builds; it doesn't trade off dwell against clearing on its own; it can
  miss a collision its own fix creates. So plan on two rounds.
- **Codex full lecture vs Opus (DE L6, 2026-10-30):** Codex produced the whole lecture, planning and
  scripts included, on a newer engine than the Opus original. A blind Gemini Flash judge was mixed:
  Opus won hooks, recaps and derivations, Codex won traces and table scenes. The user watched both
  and found Codex clearly worse ("the ripple counter visuals were just elite", of the Opus one).
  Builders went back to Opus at medium effort. A Gemini judge's preference doesn't stand in for the
  user's eye on overall quality.
