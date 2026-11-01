# Scene-writing guide

The long form of the scene-builder's kit (`.claude/agents/scene-builder.md` wins where they
differ). How every scene is built, so the video reads as one piece. Also read
`LESSONS.md` (known pitfalls). `projects/focs/l03-lists/archive/v1/scenes/` holds v1's eight finished scenes. They're
good visual references, but **v1 was paced far too fast**. Don't copy its density.

**Don't write manim from memory.** Before using a class or animation you haven't used here,
look up a real example: `engine/reference/INDEX.md` lists the official v0.22.0 example gallery,
tutorials and guides, plus the `manimce-best-practices` rules. The installed source in
`engine/.venv/lib/python3.11/site-packages/manim/` is the final word.

**Learn the style from the source.** `engine/reference/3b1b/PATTERNS.md` distils how Grant
actually paces and reveals ideas, from his own video code. `engine/reference/3b1b/GL_TO_CE.md`
translates his ManimGL idioms into our ManimCE. Read PATTERNS.md before designing a scene.

## Files

- `script/chN_name.md`: the chapter's narration. Each `[id]` line is one audio clip; `{mark}`
  is a cue point; `{pause=1.5}` is a deliberate hold. The `>` notes under each scene heading
  are the visual brief.
- `audio/manifest.json`: per clip `duration`, `marks` and `words` (start time of every spoken
  word), all in seconds from the clip's start.
- `engine/lib/narration.py`: `NarratedScene`, `self.say(id)` and the cue helpers.
- `engine/lib/style.py`: palette, fonts, `T` (prose), `Mono`, `Code` (project.json's language), `ConsCell`, `Nil`,
  `ConsChain`, `link`, `label_pointer`, `CELL`/`PTR_W`/`LINK` sizes.
- `engine/lib/titles.py`: `title_card("Part N · …")`, the chapter title card, identical in every chapter.
- `engine/lib/effects.py`: 3b1b's moves ported to CE: `FlashAround`, `FlashUnder`,
  `set_backstroke`, `TransformMatchingStrings` (glyph-matching rewrite, no `{{ }}`),
  `time_span`, `select`. Prefer these over hand-rolled pulses. More ports and the full GL→CE
  translation table are in `engine/reference/3b1b/` (`ce_ports.py`, `GL_TO_CE.md`).
- `scenes/chN_sK_name.py`: one `NarratedScene` subclass per file, rendered in filename order.

## Pacing: give the viewer time (measured from 3b1b's own code; see PATTERNS.md §1)

- **One change, then hold.** About one visual change per ~8 spoken words (his median beat is
  3 s), and the screen is still for ~40% of each beat. Never chain more than two plays without
  a hold. In practice: `run_time` ≈ 60% of `c.until(next cue)`, then `c.wait_until(next cue)`.
- If the narration pauses (`{pause}`), the screen is still too, so the viewer can look.
- Animations that carry meaning (`TransformFromCopy`, `ReplacementTransform`, a cell being built,
  an arrow redirected, a trace step): **1.5–2 s**. Incidental fades: 1 s. Never 0.3 s for
  something the viewer must follow. "Feel how long this takes" sweeps: 5+ s, linear.
- At most 2–3 animations per `play`. A group enters with `lag_ratio` 0.1–0.25; items meant to
  be read one by one get 0.5+.
- Repeated steps: the first one slow with narration, the next faster, the rest quick.
- **Screen time (viewer feedback on ch1 v2: things vanished before they could be read).**
  Text stays fully visible for at least **4 s + 1 s per 12 characters** after it finishes
  appearing; results and facts the viewer should absorb, longer. Check every scene with
  `vk dwell --chapter N` (or `vk check`), which lists text faded out too soon.
- **Don't clear just because a new narration line started.** Clear only when the space is
  actually needed, or the topic really changes. If the next idea fits in the free space, keep
  the previous content on screen (shift it aside, shrink it, or dim it to ~0.4 if it would
  distract). A result the narration just landed stays up at least through the next sentence.

## 3b1b moves to use (PATTERNS.md §2 has the evidence and his code)

- **New things come out of old things:** `fly(source, result)` (lib.moves; a raw TransformFromCopy
  doubles and morphs text). The head value flies from `x :: xs` into the cell; each trace line is
  born from the line above with `derive`.
- **Emphasis = a flash that removes itself + a colour change that stays** (P6/P7), or **one
  highlight box that slides from term to term** (P8). Never `Indicate`.
- **Spotlight by dimming the rest** to opacity ~0.25 with explicit `set_opacity` (CE `fade()`
  multiplies), then restore to 1.
- **Show the whole shape first, then walk it** (P2/P4): build the full layout, then reveal.
- **Ask on screen, hold, then the answer takes the question's place** (P23): `swap(q, answer)`.
  Never morph one text into another; the transition moves are listed in scene-builder.md.
- **Clear the board in a lagged sweep that keeps what the next idea builds on** (P18).
- **Counters move with what they count; cost is felt as screen time** (P19–P21).
- Labels drop toward what they name: `FadeIn(label, shift=0.3 * DOWN)`; braces `GrowFromCenter`;
  arrows `GrowArrow`, in the colour of their label.

## Composition

- **The hero object, i.e. what the narration is about right now, is big: 40–70% of the frame
  width** (≈ 6–10 of 14.2 units), placed at the visual centre. Don't leave a 2-unit-wide
  diagram floating in an empty frame. Scale cells, boxes and code up to fill the space.
- Text sizes already match 3b1b's. Our `T`/`Mono` size 36 ≈ his default 48 (his size units differ
  from ours). Labels ≥ 30, titles 44–56, code 32–40, hero code/expressions up to 48–56.
- Balance the frame vertically: don't park content in the top third with the bottom 60% empty.
- When a scene moves on to a genuinely new idea and space is needed, clear the old one rather
  than squeezing both on screen. Keep it (dimmed) whenever there's room.

## Timing pattern

```python
with self.say("c1.cons.3") as c:                         # audio starts now
    self.play(FadeIn(a), run_time=c.until("shuffle"))     # animate right up to the bookmark
    c.wait_until("nope")                                  # idle until the word after {nope}
    self.play(Create(b), run_time=1.0)
    c.wait_until("the list that was")                     # ...or until any spoken phrase
# leaving the block waits out the clip, plus a 0.35 s gap
```

- Say every clip of your section, in script order, one `with` block each.
- Visual changes land on the word they illustrate. Cue on `{marks}` or **any phrase spoken
  in the clip**: `c.wait_until("hands back the ell")`, `c.until("one more than", floor=0.5)`,
  `c.at("alpha", nth=1)` for a second occurrence. Case and punctuation are ignored.
- **Never hard-code seconds** (`c.start + 4.2`, `wait(1.3)` to reach a word). They silently
  drift out of sync the next time that line is re-voiced. Animation `run_time`s are fine.
- Don't overrun a clip. If a block's animations outlast its audio, the next clip starts late
  and leaves dead air.
- When something *must* be cleared, do it at the moment the new content needs the space,
  usually on the cue that introduces the new content, not on the first word of the next line.
- A scene starts from an empty screen and ends with everything faded out, so scenes join cleanly
  and a new idea gets a visual break. The exception is a handover (`# handover: next`): when the
  next scene continues the same picture, this scene ends on it and the next opens on it, so the
  join is an invisible cut. A fade to black between two identical pictures reads as a blink.

## Look

- 3Blue1Brown feel: dark background, few elements on screen, smooth motion, colour carries
  meaning, text is minimal and never a wall. Show, don't caption.
- Colours (from `lib.style`): BLUE structure/cells/keywords · TEAL nil, `::`, list syntax,
  "shared" · YELLOW attention, new things, function names · GOLD numbers & costs · GREEN types,
  good · RED errors/bad · PINK type variables · DIM secondary labels · FG normal text.
- Fonts: prose and labels use `T(...)` (CMU Serif). Code uses `Code(...)` (Menlo, highlighted),
  short snippets use `Mono`. Maths uses `MathTex` (LaTeX, matches CMU). Never use a bare `Text`
  with the default font.
- Sizes: see Composition above. Nothing smaller than 28.
- Keep 0.5 units of margin from the frame edge (frame is 14.2 × 8 units). Check that nothing
  overlaps and nothing is cut off.
- `Code.find("x :: xs", line=2)` and `Code.line(i)` return the glyphs to highlight.
- Gotchas, with the details in LESSONS.md:
  - `Indicate()` floods filled boxes; use a stroke-only pulse.
  - `TransformMatchingShapes` on multi-line code scatters glyphs; swap tokens in place.
  - `link(..., follow=True)` arrows ignore colour animations.
- OCaml on screen must be exactly right (it's study material). If unsure, check it with
  `ocaml` (installed) rather than guessing.

## Render & review

```sh
vk render --chapter N --only chN_sK_name --no-stitch   # 480p15 preview
tools/sheet.sh media/videos/chN_sK_name/480p15/ClassName.mp4 3               # contact sheet PNG
```

Always render through `vk render` / `vk check`. It gives each scene a private text/LaTeX cache, which
is safe when other scenes render in parallel. Don't run bare `manim` with a hand-made config.
A failed render's log is in `media/logs/<stem>.log`.

For the whole chapter, `vk holds N` tiles one settled frame per narration line (taken
just before each line ends). It's the best single view of composition across scenes.

Open the sheet PNG and look at it. Check layout, overlaps, off-screen bits, legibility, and
whether each visual matches what's being said at that timestamp. The manifest's `words` tell
you what's being said when. Iterate until it's clean. To look closer at one moment:
`ffmpeg -ss 12.5 -i in.mp4 -frames:v 1 out.png`.
