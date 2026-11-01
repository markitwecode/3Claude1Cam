# Glitch study, 2026-10-28

Goal: trace every visual glitch to the call that made it, group the calls by root cause, and fix each
cause at the source (lib helpers that make the safe move the default, lint rules, builder rules), so a
kind of glitch can't come back. Phase 1 (this document) is analysis and design; nothing in engine/,
.claude/ or any project's scenes/script/audio/out was changed.

## What was run
- **Gemini reviews with a transition prompt.** The stock `vk review` prompt tells Gemini to judge
  only settled frames, which hides exactly the transition jumbles under study (on l03 ch4 it reports
  1 glitch). A scratch wrapper around tools/review.py (same chunking, mapping and calibration) asked
  for every visual problem *including mid-animation* ones and wrote `media/review/chN_glitch_review.*`:
  l03 ch4 (52 visual findings), l04 ch2 (29), l05 ch1 (40), cross-product ch1 (49). Plus the existing
  stock reviews: studio-tour ch1/ch2 (10; the originals of 01:33/01:40, since overwritten by its
  running fix round) and l03 ch4's chapter and scene reviews (7). **187 visual findings.**
- **Finding → call, deterministically.** A dry-run play logger (scratch `playlog.py`) runs each scene
  with `Scene.play` hooked and records, per play: clip, clip-relative start/end, the scene-file line
  (and lib helper) that called it, and every animation with its source and target, marked `=`
  (identical glyph shapes: a pure move), `~`/`#` (different glyphs: a morph) or `s` (plain shapes).
  Each finding is aligned on its clip's real start (media/cues) and joined to the plays active in
  [t − 0.2, t + 1.2] s (Gemini runs ~0.5 s early; jumbles last ~0.6 s). 47 scenes logged.
- **Frames.** 42 findings were checked on ffmpeg grabs of out/*.mp4 at +0/+0.3/+0.6/+0.9/+1.2 s
  (10 contact sheets): 32 confirmed, covering every class, 10 not visible or not a glitch; the other
  145 are classed by the call active at the moment ("mechanism": the same call pattern as a
  frame-confirmed case).
- **Early labels, measured over every finished scene** (132 scenes in 5 projects; scratch `early.py`):
  for each prose label (`T` text), when it starts to appear (time_span-aware) vs when its first
  distinctive word (≥ 4 letters) is spoken.

184 of the 187 findings fall on moving frames; settled frames were clean. Gemini's descriptions of
*what* is wrong are often off ("rotated", "Fraktur", "e^-x", "mirrored k" are all glyphs caught
mid-morph or mid-stroke), but its *when* is reliable to ~0.5 s, and that is all the mapping needs.

## Root causes and counts

| Class | What the viewer sees | Root cause (the call) | Findings | Frame-confirmed |
|---|---|---|---|---|
| **A** unlike morph | letter salad for ~0.6 s: `$2.5ʋ`, `Lectur04: inary`, "Fraktur" digits, `?` → squiggle | `TransformFromCopy` (26) / `ReplacementTransform` (14) / `Transform` (3) between texts whose glyphs differ (other string, other font, or shapes → glyphs). CE pairs sub-objects by index and interpolates their outlines. | 43 | 7 |
| **B** copy overlaps its source | doubled text: `appepend`, `[[33;; 22;; 11]]`, `$$0.2020`, `rr FF`, a cell "duplicated" | same-glyph `TransformFromCopy` (35) / `ReplacementTransform` (4) of text to a nearby spot: the copy starts fully opaque on top of its source and slides through it and its neighbours; trace "birth" helpers move many pieces by different offsets, so they cross. | 40 | 8 |
| **C** matching transform | glyphs fly across the line: `append 1; 2; 3] 4[ ]`, a stray `4` | `TransformMatchingShapes` / `TransformMatchingStrings` on text whose tokens reorder or repeat: matches may cross, unmatched glyphs fly to/from the other object's centre at scale 0. | 8 | 2 |
| **D** clear/fill overlap | old text ghosting under new text, "lingers from the previous shot" | outgoing content still visible while incoming content fades or moves into the same space: `sweep_clear` (its lagged FadeOut runs to the end of the play, the incoming FadeIn starts at 50%) (20), `FadeOut(old)` + `FadeIn`/move of new in one play (23), `FadeTransform` between unlike cards (2). | 45 | 9 |
| **E** partial reveal | half-words (`larg`ᵉ, `extr`, `co`, `Cle`, `Torque, an`), stroke scribbles read as mirrored/stray glyphs | `Write()` on MathTex/Text (9), `FadeIn(text, lag_ratio>0)` = letter by letter, later letters still shifted (4), `Create()` of a box starting as a stray line (3). | 16 | 4 |
| **T** label before its object | `a × b` label waiting at an arrow's tip before the arrow grows | label FadeIn in the same play as the GrowArrow it names | 1 | 1 |
| **K** stale content kept | a caveat stays into an unrelated shot | `sweep_clear(..., keep=[cav])` keeping something the next shot doesn't use | 1 | 1 |
| **N** no transition cause | flashes read as stray bars/boxes, `Create` of shapes, Gemini miscounts and misreads, still frames | none found (9 checked on frames: nothing wrong, or a layout choice) | 33 | – |

A + B + C + D + E = **152 of 187 (81%)**, five mechanisms, all in transitions.

### Not in Gemini's list, measured separately
- **Raised "~".** ASCII `~` in CMU Serif is the accent-shaped tilde at cap height (rendered side by
  side in scratch); U+223C `∼` and `MathTex \sim` sit on the maths axis, Menlo's `~` is fine. Every
  "raised ~" note in studio-tour STATUS (s4, s6, s7; still in ch1_s8 line 261) is a `T("…~…")`.
- **Labels appearing early** (director notes "up 1–3 s"). Of 1366 prose labels in 132 finished scenes,
  648 have their words spoken after they appear; **298 of those (46%) appear 1–4 s early** (median
  1.7 s; 140 are > 2 s early, 1.1 per scene). What scheduled them: one play revealing several labels
  whose words come at different times **46%**; a play cued on an earlier word (the sentence start or
  the previous beat) **35%**; cued on the label's own `{mark}` yet still early (marks or repeated
  words) 12%; no cue at all (first play of a clip, or chained after another play) 7%.

## Design
Three general mechanisms instead of per-glitch special cases:
1. **A small transition vocabulary** in lib, each move built so it can't jumble, with fixed styles and
   timings (§1), plus source fixes in existing helpers (§2).
2. **One new audit pass in `vk check`** that inspects every `play()` as it runs: what morphs into
   what, how text is revealed, what the frames *between* the endpoints look like, and when labels
   appear vs when they're spoken (§3). It judges outcomes, so it catches a glitch whatever call made it.
3. **Builder rules** that name the vocabulary and the checks (§4).

### 1. lib: the vocabulary (new `engine/lib/moves.py`, re-exported by `lib.kit`, so the file template's `from lib.kit import *` brings it in)
Fixed constants: `APPEAR_RT = 1.0`, `DISAPPEAR_RT = 0.8`, `SWAP_RT = 1.2`, `EDIT_RT = 1.5`,
`FLY_RT = 1.5`, `LABEL_SHIFT = 0.25 * DOWN` (labels drop toward what they name), `RISE = 0.2 * UP`.
Like the kit's other helpers, the return value goes into `self.play(...)`; the default run_time is set
on the animation, a `run_time=` in play() overrides it.

```python
appear(*mobs, shift=LABEL_SHIFT, lag=0.25) -> Animation
    # Each mob fades in whole (lag_ratio 0 inside a mob: never letter by letter or stroke by stroke);
    # several mobs come in as a LaggedStart over the mobs, not their glyphs.   Replaces Write, lagged FadeIn.
disappear(*mobs) -> Animation
    # Each mob fades out whole.
swap(old, new) -> list[Animation]                     # self.play(*swap(q, answer))
    # One thing replaces another in place, never a morph: old fades out rising (0–45% of the play),
    # new fades in rising into place (45–100%). No frame shows both.  The question → answer move (P23),
    # a number or caption update, a card replaced.   Replaces Transform/ReplacementTransform/FadeTransform of text.
edit(old, new) -> Animation
    # Rewrites a text (Text, Code, MathTex) keeping what's shared. Glyphs are paired by an
    # order-preserving diff of their shapes (difflib matching blocks on lib.effects._shape_key), so no
    # two moving glyphs cross: shared glyphs slide/recolour to their new place (25–85%), dropped glyphs
    # fade out where they are (0–35%), new glyphs fade in where they land (65–100%). Falls back to
    # swap() when under half of the shorter text is shared. new ends on screen as one object.
    # Replaces TransformMatchingShapes/Strings for rewrites (`append xs ys` → `xs @ ys`, trace steps).
fly(src, dst, arc=PI / 4) -> Animation
    # "New things come out of old things", safely. A copy of src travels on an arc to dst.
    # Same glyphs (any size/colour): the copy becomes dst, fading in over the first 35% so it never sits
    # doubled on its source. Different glyphs or a shape: the copy flies unchanged, scaled to dst's
    # height, and dissolves into dst over the last 35%. dst ends on screen; src stays.
    # Replaces TransformFromCopy.
derive(scene, src, dst, run_time=2.0) -> None         # calls scene.play twice, like sweep_clear
    # A trace line born from the line above: a whole copy of src drops rigidly to dst's place (fly,
    # first half), then edit()s into dst (second half). Pieces never cross each other.
    # Replaces the per-scene "birth" helpers (l03 ch4_s3 L134, ch4_s5 L95, ch4_s7 …).
```
Moves (`.animate`, `MoveToTarget`) and style changes (`restyle`, `set_alpha`, `recolor`, `token_box`
slides) stay as they are; they are same-shape transforms and pass the checks.

### 2. Source fixes in existing helpers (same signatures)
- **`kit.sweep_clear`** (class D, 20 findings): the lagged clear runs in the first half of the play;
  incoming animations without a `time_span` start at half time; incoming `time_span`s are kept (the
  usual `time_span(FadeIn(new), 0.6, 1.2)` already starts at half time). Same run_time. Finished scenes
  that use it would render differently only during their sweeps, which is the bug being fixed.
- **`style.T`** (raised ~): ASCII `~` → U+223C `∼`. `Mono`/`Code` keep `~` (a real code character,
  fine in Menlo).
- **`effects.time_span`**: also stores `anim.time_span = (start, end)`, so sweep_clear and the audit
  can read it. No render change.
- **`narration.Clip`** (early labels): `c.wait_until`, `c.until` and `c.at` also accept a Text
  mobject: the cue is that label's own first distinctive word (≥ 4 letters) spoken from now on, so
  `c.wait_until(label)` means "until this label is said"; KeyError when none of its words are spoken
  (give a phrase). The audit uses the same matcher, so the rule and the check agree.

### 3. `vk check`: one transition audit (engine/tools/check.py)
The audit already dry-runs every scene with `say()` and `wait_until()` hooked. It adds a hook on
`Scene.play` and, under the dry run, makes `Scene.get_time_progression` yield 25/50/75/100% of each
play instead of only its end, so `update_to_time` interpolates the in-between states a render would
show. New flags, reported as `transition:` / `early:` lines; all block the render like layout flags:

| Rule | Fires when | Catches | Measured on the 47 logged scenes |
|---|---|---|---|
| **T1 morph** | a Transform-family animation (incl. inside AnimationGroup/LaggedStart/Succession) whose source and target glyph lists differ by shape (`_shape_key`, ignoring size, colour, position). Same-shape moves (restyle, set_alpha, MoveToTarget, fly, token_box slides) never fire. | A | 127 plays in 36 scenes |
| **T2 partial text** | `Write`, `DrawBorderThenFill`, `AddTextLetterByLetter` or `Create` on anything containing glyphs; `FadeIn`/`FadeOut` with `lag_ratio > 0` over glyphs | E | 55 plays in 21 scenes |
| **T3 mid-transition overlap** | at the 25/50/75% samples, two different text objects overlap (both ≥ 0.3 opacity, > 35% of the smaller glyph box: the existing overlap test), when they don't overlap at the play's start or end | B, C, D, and new kinds | to calibrate in Phase 2 |
| **T4 tilde** | a CMU Serif Text containing ASCII `~` (one built without `T`) | raised ~ | – |
| **E1 early label** | a prose label starts appearing > 2.0 s before its first distinctive word is spoken (and the word wasn't said before it). 1–2 s is listed without blocking. Opt-out: a `# early: <reason>` comment on the play() line (a title, a list shown whole then walked). | early labels | 140 labels in 132 scenes |

Messages name the line and both texts, and the fix: e.g. `transition: c2.second.4 line 161:
ReplacementTransform morphs 'median 0 · real waste…' into 'arbitrary · turns…' (letters scramble):
use swap() or edit()`; `transition: c4.trace.1 line 149 @ 50%: '1 :: append [2; 3] [4]' runs over
'append [1; 2; 3] [4]' (doubled text): use derive() or fly()`; `early: c2.split.4 '≈ 190k a turn on
average' appears 2.8 s before "average": cue it with c.wait_until(label)`.
T1 and T2 are exact (they read the animation objects). T3 and E1 use thresholds; Phase 2 calibrates
them on the frame-confirmed cases and on clean moments before they block. The extra cost is 3
`update_to_time` calls and a glyph snapshot per play in a dry run that takes seconds now.

### 4. Builder rules (.claude/agents/scene-builder.md)
- A **"Transitions"** section, the whole vocabulary in one table: `appear`, `disappear`, `swap`,
  `edit`, `fly`, `derive`, `sweep_clear`, moves, style changes, each with its use, as in §1.
- Rules, each tied to the check that enforces it: never morph one text into a different text (T1);
  text appears whole, no Write, no lag_ratio on text (T2); what leaves is gone before what arrives
  takes its place, and a moving or flying thing doesn't cross other text (T3); a label lands on its
  own word: `c.wait_until(label)`, several labels = one play each on its own word (E1); `keep=` only
  what the next shot builds on (K); highlight boxes `FadeIn`, not `Create` (they start as a stray line).
- "3b1b moves" updated: TransformFromCopy → `fly`; "transform the ? into the answer" → `swap`; trace
  lines → `derive`. Pitfalls: the TransformMatchingShapes and Transform-leaves-a-ghost items fold into
  the rules above. The library API section gains the six signatures. Net size about +15 lines.
- docs/STYLE.md (P23 and the TransformFromCopy lines) and docs/LESSONS.md get the same changes, so the
  long form doesn't contradict the kit.

### Optional, outside the three files (your call)
- `vk review --transitions`: this study's prompt as a mode of tools/review.py. It is the end-to-end
  acceptance check: on the same video it found 51 glitches where the stock prompt found 1.
- Finished chapters are not reworked: 36 of the 47 logged scenes contain at least one T1 morph, so a
  `vk check` of a finished scene will now report them.

### Phase 2 test plan
1. Scratch mirrors (copied project.json + scenes, audio symlinked read-only, as in
   docs/bench/2026-10-24-renderers.md) of l03 ch4, l04 ch2, l05 ch1 and cross-product ch1. No finished
   project is edited.
2. Each helper against its class, before/after frames at the same moment, plus the transition-prompt
   Gemini review of the before/after scene renders: A `swap` on l04 ch2_s5 L155 (`?` → `- : bool =
   true`) and `fly` on l03 ch4_s6 L167 (`3 copied` → `6 conses`); B `derive` on l03 ch4_s3 L149 and `fly`
   on cross-product ch1_s3 L234; C `edit` on l03 ch4_s2 L282; D the sweep_clear fix alone (no scene
   change) on l05 ch1_s6 L328 and `swap` on l05 ch1_s4 L216; E `appear` on l04 ch2_s6 L314 and
   cross-product ch1_s2 L159 (Write); `T("~")` rendered.
3. Each lint rule fires on those lines and is silent on the swapped-in versions; `vk check
   --no-render` across a finished chapter (l04 ch2) for counts per rule; T3/E1 thresholds set so all
   frame-confirmed transition cases fire, with flags on settled moments spot-checked.
4. Back-compatibility: a finished scene without sweep_clear or `~` renders frame-identical; one with
   sweep_clear keeps its duration and differs only in the sweep frames.
5. Note: engine/tools/check.py was changed on disk today by another session (a `slots.manim` render
   slot and `code_only`); Phase 2 builds on that version.

## Phase 2: what shipped (2026-10-28)
- `engine/lib/moves.py` (re-exported by lib.kit): `appear disappear swap edit fly derive during`, as in
  §1, all list-returning and timed by the play's run_time. Glyphs are matched by `glyph_classes`
  (normalised outlines within 0.02) rather than `_shape_key`, whose rounding missed the same glyph
  at two font sizes. `fly` arcs only along the same row (a curved approach into a formula grazed
  its neighbours).
- Fixes in place: `sweep_clear` clears in the first half, incoming starts at half time unless it
  carries `time_span`/`during`; `T()` writes `∼` for `~`; `time_span` records `abs_span`;
  `c.wait_until/until/at(..., own_word=label)` (the old `cue` meaning unchanged).
- `engine/tools/transitions.py`, called by check.py: morph, partial, overlap, tilde and early rules,
  blocking in scenes with `# style: 2` (the new template line), advice (6 lines and a count per
  scene) elsewhere. Overlap blocks: it fires at 6 of 7 frame-confirmed copy-overlap moments and 4 of
  7 matching-transform ones (all 7 carry some flag), and all 8 sampled flags at moments Gemini
  hadn't reported were real jumbles on frames. Its D recall (11 of 21 non-sweep crossfades) is lower: crossfades between text
  and boxes aren't text-on-text.
- `vk review --transitions` (chapter and scene mode) → `*_transitions.{json,md}`; the director's
  final review runs it and records findings under "Glitches".
- Tests in scratch mirrors, before (finished 1080p) vs after (480p re-render), same moments: swap
  (l04 ch2_s5 L155), edit (l03 ch4_s2 L282), derive (l03 ch4_s3 birth), appear for lagged FadeIn
  (l04 ch2_s6 L314) and for Write (xp ch1_s2 L159), fly (xp ch1_s3 L221), the sweep fix alone (l05
  ch1_s6 L328): every jumble gone, and each changed line's flag gone in `vk check`. A finished
  scene without sweeps renders frame-identical (l04 ch2_s2: 1037 of 1037 frames); one with three
  sweeps keeps its 1225 frames and differs only during the sweeps.
- Advice on finished chapters (items; scenes): l03 ch4 overlap 57, morph 48, early 15, partial 6;
  l04 ch2 morph 26, overlap 20, partial 11, early 8; l05 ch1 morph 36, overlap 29, early 14,
  partial 12; cross-product ch1 partial 38, overlap 38, morph 17, early 11. No tilde (none left
  outside studio-tour).

## Findings
`where`: l03 ch4 / l04 ch2 / l05 ch1 / xp ch1 = transition-prompt reviews (scratch prompt), st ch1/2 =
studio-tour's original stock reviews, l03 ch4* = l03 ch4's stock chapter and scene reviews.
`scene @ s` is scene time. `confirmed`: yes/no = checked on frames; mechanism = classed by the call
active at that moment, same pattern as a frame-confirmed case. Offending call: `L` = line in the scene
file; TFC = TransformFromCopy, RT = ReplacementTransform, ≠ = source and target glyphs differ; the
arrow reads source → target.

| # | where | scene @ s | kind | Gemini saw | confirmed | class | offending call |
|---|---|---|---|---|---|---|---|
| 1 | l03 ch4 | s2_code @ 5.9 | glit | The title 'append' is briefly duplicated, appearing twice overlapping  | yes | B | L114: `TFC(glyph of 'append'->glyph of 'append [1; 2; 3] [4]')` |
| 2 | l03 ch4 | s2_code @ 9.9 | glit | Evaluated result shows '- : int list 1 [2; 3; 4 ]' with misplaced 1 an | mechanism | A | L119: `TFC≠(glyph of 'append [1; 2; 3] [4]'->glyph of '- : int list = [1; 2; 3;')` |
| 3 | l03 ch4 | s2_code @ 13.9 | glit | Colored boxes [1] [2] [3] [4] from previous shot linger and overlap co | mechanism | D | L144: `FadeOut(Text'append')` |
| 4 | l03 ch4 | s2_code @ 62.9 | glit | Word 'append' flies into line 3 of pattern match, displaying '/ [], ys | mechanism | B | L270: `TFC(glyph of 'let rec append xs ys = m'->glyph of 'let (@) = append')` |
| 5 | l03 ch4 | s2_code @ 68.9 | glit | Text scrambles into 'append 1; 2; 3] 4[ ]' with misplaced brackets dur | yes | C | L282: `TransformMatchingStrings(Code'append [1; 2; 3] [4]'->Code'[1; 2; 3] @ [4]')` |
| 6 | l03 ch4 | s2_code @ 86.9 | glit | Error message begins with garbled text 'Errᴰ' before displaying 'Error | no | N | L325: `.animate.set_color(glyph of '[1; 2] @ ["three"]')` |
| 7 | l03 ch4 | s3_trace @ 6.7 | glit | Text collides and overlaps: 'append [1; 2; 3] [4]' over '=> 1append [  | yes | B | L149: `TFC(glyphs of 'append [1; 2; 3] [4]'->glyphs of '1 :: append [2; 3] [4]')` |
| 8 | l03 ch4 | s3_trace @ 13.7 | glit | Digit '2' sits too high as a superscript and '::' is missing. | mechanism | B | L149: `TFC(glyphs of '1 :: append [2; 3] [4]'->glyphs of '1 :: (2 :: append [3] [4')` |
| 9 | l03 ch4 | s3_trace @ 16.6 | glit | Stray '::' appears in top-right while central text scrambles into over | mechanism | B | L149: `TFC(glyphs of '1 :: (2 :: append [3] [4'->glyphs of '1 :: (2 :: (3 :: append ')` |
| 10 | l03 ch4 | s3_trace @ 22.6 | glit | Scrambled intermediate text with curly braces '1 :: {2 :: ({3 :: appen | mechanism | B | L149: `TFC(glyphs of '1 :: (2 :: (3 :: append '->glyphs of '1 :: (2 :: (3 :: [4]))')` |
| 11 | l03 ch4 | s3_trace @ 38.6 | glit | Missing '::' and corrupted green block over bracket in '1 [ 2; 3; 4]'. | yes (mild) | A | L285: `RT≠(glyphs of '1 :: [2; 3; 4]'->glyphs of '[1; 2; 3; 4]')` |
| 12 | l03 ch4 | s4_cells @ 21.5 | glit | Digit '4' collides into and overlaps closing bracket in 'xs = [1; 2; 3 | mechanism | C | L158: `TransformMatchingShapes[Transform≠(VGroup(VGroupx9)~of'xs = [1; 2; 3]'->VGroup(VGroupx9)…` |
| 13 | l03 ch4 | s4_cells @ 27.5 | glit | Stray grey digit '4' floats in empty space between the lists. | mechanism | C | L163: `TransformMatchingShapes[Transform≠(VGroup(VGroupx9)~of'xs = [1; 2; 3; 4]'->VGroup(VGroup…` |
| 14 | l03 ch4 | s4_cells @ 78.5 | glit | Cell 3 is duplicated, showing two cell 3s stacked vertically during co | mechanism | B | L285: `LaggedStart[TFC(ConsCell(Square,Rectangle,Dot)~'1'->ConsCell(Square,Rectangle,Dot)~'1');…` |
| 15 | l03 ch4 | s4_cells @ 86.5 | glit | Label 'linear time' collides into and overlaps the bottom of 'O(n)'. | mechanism | D | L327 via sweep_clear: `LaggedStart[FadeOut(ConsChain(ConsCellx3,Arrowx3,Nil)~'1'); FadeOut(Arrow(ArrowTriangleF…` |
| 16 | l03 ch4 | s4_cells @ 95.5 | glit | Big-O notation displays garbled text 'O((m))' under append instead of  | mechanism | B | L342: `TFC(MathTex'O(n)'->MathTex'O(n)')` |
| 17 | l03 ch4 | s5_nrev @ 1.1 | glit | List elements scramble into jumbled text '[1; 2{ 3]2³; ]' with '1' bel | mechanism | B | L109: `TFC(glyphs of '[1; 2; 3]'->glyphs of '[3; 2; 1]')` |
| 18 | l03 ch4 | s5_nrev @ 30.1 | glit | Digits '3', '2', '1' in green boxes morph into Gothic Fraktur font gly | mechanism | A | L109: `TFC≠(Text'3'->glyphs of '- : int list = [3; 2; 1]')` |
| 19 | l03 ch4 | s5_nrev @ 34.1 | glit | Line duplicates and text scrambles into overlapping layers 'nrev 1; 2; | mechanism | B | L109: `TFC(glyphs of 'nrev [1; 2; 3]'->glyphs of 'nrev [2; 3] @ [1]')` |
| 20 | l03 ch4 | s5_nrev @ 38.9 | glit | Digit 3 and '@' collide outside the bracket as '@3 [ ]'. | mechanism | B | L109: `TFC(glyphs of 'nrev [2; 3] @ [1]'->glyphs of '(nrev [3] @ [2]) @ [1]')` |
| 21 | l03 ch4 | s5_nrev @ 44.9 | glit | Characters scramble into a chaotic cluster before forming '[3; 2; 1]'. | mechanism | A | L109: `TFC≠(glyphs of '(([] @ [3]) @ [2]) @ [1]'->glyphs of '[3; 2; 1]')` |
| 22 | l03 ch4 | s6_cost @ 4.3 | glit | Garbled text fragments appear directly below top expression during ani | mechanism | A | L133: `TFC≠(glyphs of '(([] @ [3]) @ [2]) @ [1]'->Code'[] @ [3]')` |
| 23 | l03 ch4 | s6_cost @ 15.3 | glit | A stray yellow bracket fragment floats in space under '@ [3]'. | mechanism | A | L157: `TFC≠(glyphs of '(([] @ [3]) @ [2]) @ [1]'->VGroup(Square,Text)~'3')` |
| 24 | l03 ch4 | s6_cost @ 23.3 | glit | The text '6 conses' morphs through heavily scrambled, doubled glyphs. | yes | A | L167: `TFC≠(VGroup(Textx2)~'3 copied'->Text'6 conses')` |
| 25 | l03 ch4 | s6_cost @ 27.3 | glit | Text '(nrev xs)' overlaps '[3; 2]' and block row is broken. | mechanism | D | L192 via sweep_clear: `LaggedStart[FadeOut(Code'(([] @ [3]) @ [2]) @ [1]'); FadeOut(Mobject[0]); FadeOut(Mobjec…` |
| 26 | l03 ch4 | s6_cost @ 38.3 | glit | Two 'n' characters collide and overlap under the bracket. | mechanism | A | L214: `RT≠(Brace[1]->Brace[1])` |
| 27 | l03 ch4 | s6_cost @ 39.3 | mism | Label under bracket reads 'm' while narration says 'n in total'. | mechanism | B | L221: `TFC(MathTex'n'->part of 'n ,\; n-1 ,\; \dots ,\; ')` |
| 28 | l03 ch4 | s6_cost @ 43.3 | glit | Digit '0' collides with preceding comma in '2, 1, 0'. | no | N | L228: `FadeIn(part of 'n ,\; n-1 ,\; \dots ,\; ')` |
| 29 | l03 ch4 | s6_cost @ 58.3 | glit | Stray blocks float near formula and staircase rows are disjointed. | mechanism | A | L277: `TFC≠(part of '0 + 1 + 2 + \cdots + n'->VGroup(Squarex2))` |
| 30 | l03 ch4 | s6_cost @ 74.8 | glit | Stray 'n' inside staircase block and garbled '(n+1)==n' appears. | mechanism | A | L311: `TFC≠(MathTex'n + 1'->part of 'n (n+1)')` |
| 31 | l03 ch4 | s6_cost @ 81.3 | glit | Formula '= n(n+1)/2' is duplicated and scrambled on top of itself. | mechanism | A | L339: `TFC≠(VGroup(MathTex,VGroup)~'='->MathTex'O(n^2)')` |
| 32 | l03 ch4 | s6_cost @ 98.3 | glit | Ghost text from earlier append trace lingers across bottom blocks. | mechanism | D | L384 via sweep_clear: `LaggedStart[FadeOut(Mobject[0]); FadeOut(Arrow(ArrowTriangleFilledTip)); FadeOut(Text'50…` |
| 33 | l03 ch4 | s6_cost @ 110.3 | glit | A stray vertical pipe character appears after 'time O(n^2)'. | no | N | L420: `FlashAround(VGroup(VMobjectx80))` |
| 34 | l03 ch4 | s7_revapp @ 11.8 | glit | Dashed card box jumps to screen edge and is clipped. | no | N | L202: `Create(DashedVMobject(RoundedRectanglex22))` |
| 35 | l03 ch4 | s7_revapp @ 16.8 | glit | Old title 'nrev O(n^2)' lingers over code; cards are tilted. | mechanism | D | L220: `FadeOut(VGroup(Text,MathTex)~'nrev')` |
| 36 | l03 ch4 | s7_revapp @ 21.8 | glit | Code shows 'withys' with 'ys' colliding directly into 'with'. | mechanism | A | L232: `TFC≠(glyphs of 'let rec rev_app xs ys = '->Text'ys')` |
| 37 | l03 ch4 | s7_revapp @ 34.8 | glit | Highlight on line 4 is an opaque rectangle obscuring code. | mechanism | D | L285: `FadeOut(Rectangle[1])` |
| 38 | l03 ch4 | s7_revapp @ 37.8 | glit | Trace text morphs through scrambled state with floating misplaced char | mechanism | B | L272: `TFC(glyphs of 'rev_app [1; 2; 3] []'->glyphs of 'rev_app [2; 3] [1]')` |
| 39 | l03 ch4 | s7_revapp @ 39.8 | glit | Arguments '[3]' and '[2; 1]' overlap on trace line 3. | mechanism | B | L272: `TFC(glyphs of 'rev_app [2; 3] [1]'->glyphs of 'rev_app [3] [2; 1]')` |
| 40 | l03 ch4 | s7_revapp @ 45.8 | glit | Result '⇒ [3; 2; 1]' morphs through doubled, garbled characters. | mechanism | B | L305: `TFC(glyphs of 'rev_app [] [3; 2; 1]'->glyphs of '[3; 2; 1]')` |
| 41 | l03 ch4 | s7_revapp @ 56.8 | glit | Stray text fragment '] 5]' appears prematurely near top-right corner. | mechanism | B | L337: `TFC(glyphs of 'rev_app [1; 2; 3] []'->glyphs of 'rev_app [1; 2; 3] [4; 5]')` |
| 42 | l03 ch4 | s7_revapp @ 65.8 | glit | The digit '5' in result list is upside-down/mirrored. | mechanism | B | L374: `TFC(glyphs of 'rev_app [1; 2; 3] [4; 5]'->glyphs of 'rev_app [1; 2; 3] []')` |
| 43 | l03 ch4 | s7_revapp @ 67.8 | glit | Incomplete duplicate line 'rev_app []' appears above trace. | mechanism | B | L384: `TFC(glyphs of 'rev_app [1; 2; 3] []'->glyphs of 'let rev xs = rev_app xs ')` |
| 44 | l03 ch4 | s7_revapp @ 72.8 | glit | Output displays heavily doubled characters '[[33; 22; 11]]'. | yes | B | L411: `TFC(glyphs of 'rev_app [1; 2; 3] []'->glyphs of 'rev [1; 2; 3]')` |
| 45 | l03 ch4 | s7_revapp @ 80.8 | glit | Letter 'n' in 'n conses' has superimposed 'h', reading 'nh'. | mechanism | A | L441: `TFC≠(MathTex'n'->MathTex'O(n)')` |
| 46 | l03 ch4 | s7_revapp @ 91.8 | glit | Y-axis labels 'conses' and 'time' collide and overlap. | no (clean dissolve) | D | L488: `FadeTransform(Group(Textx2)~'conses'->Text'time')` |
| 47 | l03 ch4 | s7_revapp @ 93.8 | glit | Legend labels are truncated mid-word as 'co' and 'com'. | mechanism | E | L501: `Create(DashedVMobject(ParametricFunctionx30))` |
| 48 | l03 ch4 | s8_strength @ 37.1 | glit | Stray black slash mark appears beneath number '14'. | mechanism | A | L236: `TFC≠(MathTex'14'->MathTex'21')` |
| 49 | l03 ch4 | s8_strength @ 40.1 | glit | Yellow highlight box frames stray '+7' underneath '0'. | no | N | L243: `LaggedStart[FlashAround(VGroup(VMobjectx80)); FlashAround(VGroup(VMobjectx80)~of'append'…` |
| 50 | l03 ch4 | s8_strength @ 60.1 | glit | Stray squiggly symbol floats above linked list node 2. | mechanism | A | L309: `TFC≠(glyph of 'iter_append [1; 2; 3] [4'->Text'3')` |
| 51 | l03 ch4 | s8_strength @ 79.1 | glit | Stray underline mark appears under 'xs' in first bullet. | no | N | L384: `.animate.set_color(glyph of 'xs')` |
| 52 | l03 ch4 | s8_strength @ 104.1 | glit | Ghost duplicate of 'then exercises' appears directly beneath line. | no | N | (no play: still frame) |
| 53 | l04 ch2 | s2_linear @ 7.5 | glit | "looking for 9" scrambles into garbled characters ("looking fo19 9") a | mechanism | B | L94: `FadeIn(Text'looking for')` |
| 54 | l04 ch2 | s2_linear @ 22.5 | glit | Orange pointer arrow jumps to element 5 instead of head element 3 befo | mechanism | A | L136: `RT≠(Text'9'->Text'6')` |
| 55 | l04 ch2 | s2_linear @ 39.5 | glit | A yellow selection highlight box briefly flashes around cell 9 before  | no | N | L164: `LaggedStart[FlashAround(VGroup(VMobjectx80)); FlashAround(VGroup(VMobjectx80)); FlashAro…` |
| 56 | l04 ch2 | s2_linear @ 42.5 | glit | List cells morph through garbled, distorted intermediate shapes and sc | yes | A | L188: `RT≠(Text'3'->MathTex'x_1')` |
| 57 | l04 ch2 | s2_linear @ 63.5 | glit | Three complexity labels and brackets collapse vertically, colliding in | mechanism | D | L237: `FadeOut(Brace[1])` |
| 58 | l04 ch2 | s3_faster @ 37.3 | glit | Text "exponentially better" and "2^20 = 1,048,576" linger from previou | yes | D | L201 via sweep_clear: `LaggedStart[FadeOut(Mobject[0]); FadeOut(Mobject[0]); FadeOut(Group[0]); FadeOut(Mobject…` |
| 59 | l04 ch2 | s3_faster @ 59.1 | glit | "linear: O(n)" in top-left summary is duplicated and overlaps with its | mechanism | D | L255: `FadeOut(Text'(within machine limits)')` |
| 60 | l04 ch2 | s3_faster @ 63.3 | glit | Green checkmark next to "simple" appears upside-down pointing downward | no | N | L286: `Create(VMobject[1])` |
| 61 | l04 ch2 | s4_member @ 49.5 | glit | Evaluation trace temporarily displays "member 9 [9; 44; 7]" with an ex | mechanism | A | L270: `RT≠(Code'member 9 [9; 4; 7]'->Code'true')` |
| 62 | l04 ch2 | s4_member @ 51.5 | glit | "member 6 [3; 5; 9; 4; 7]" appears misplaced, overlapping the left col | mechanism | C | L275: `TransformMatchingStrings(Code'member 9 [3; 5; 9; 4; 7]'->Code'member 6 [3; 5; 9; 4; 7]')` |
| 63 | l04 ch2 | s4_member @ 75.5 | glit | Type signature "val member..." appears directly on top of "O(n) time"  | mechanism | D | L339 via sweep_clear: `LaggedStart[FadeOut(Code'member 6 [3; 5; 9; 4; 7]'); FadeOut(MathTex'\Rightarrow'); Fade…` |
| 64 | l04 ch2 | s5_equality @ 19.7 | glit | Stray miniature list diagram appears briefly at the top edge during sc | mechanism | D | L117 via sweep_clear: `LaggedStart[FadeOut(Mobject[0]); FadeOut(Text'polymorphic equality'); FadeOut(Mobject[0]…` |
| 65 | l04 ch2 | s5_equality @ 24.7 | glit | Stray yellow horizontal line segment floats above the first list cell  | mechanism | E | L131: `Create(Rectangle[1])` |
| 66 | l04 ch2 | s5_equality @ 36.7 | glit | Garbled, scrambled green text artifact appears beneath '- : bool = tru | yes | A | L155: `RT≠(Text'?'->Code'- : bool = true')` |
| 67 | l04 ch2 | s5_equality @ 37.7 | glit | Stray yellow horizontal line segment floats above the first list cell  | mechanism | E | L160: `Create(Rectangle[1])` |
| 68 | l04 ch2 | s5_equality @ 41.7 | glit | Digits 2 and 3 duplicate and vertically overlap inside their cells dur | mechanism | A | L171: `TFC≠(Text'2'->MathTex'2')` |
| 69 | l04 ch2 | s5_equality @ 58.7 | glit | Jumbled, garbled green text artifact appears beneath the boolean resul | mechanism | A | L225: `RT≠(Text'?'->Code'- : bool = true')` |
| 70 | l04 ch2 | s5_equality @ 62.7 | glit | Garbled green artifact visible beside question mark beneath 'true > fa | mechanism | A | L236: `RT≠(Text'?'->Code'- : bool = true')` |
| 71 | l04 ch2 | s5_equality @ 80.7 | glit | Digit 3 inside the list cell [3] is rotated 180 degrees upside down. | no | N | L275: `Create(Line[1])` |
| 72 | l04 ch2 | s6_limits @ 15.9 | glit | Words 'double' and '_twice' collide and overlap vertically during anim | mechanism | A | L133: `TFC≠(glyphs of 'let double n = 2 * n'->Text'double')` |
| 73 | l04 ch2 | s6_limits @ 33.9 | glit | Text morphs through a garbled state with 'double double' and 'ice' ove | yes | B | L171: `TFC(Text'double'->Text'double')` |
| 74 | l04 ch2 | s6_limits @ 40.9 | glit | Garbled green leftover text '[ icouble; ]' overlaps under '[twice; dou | mechanism | A | L187: `TFC≠(glyphs of 'let twice n = n + n'->Text'twice')` |
| 75 | l04 ch2 | s6_limits @ 46.9 | glit | Stray green letters 'ouble' linger to the right of empty brackets '[ ] | mechanism | D | L202: `FadeOut(Text'twice')` |
| 76 | l04 ch2 | s6_limits @ 71.9 | glit | Stray white box corner lines appear prematurely below the text. | no | N | L257: `.animate.scale,to_edge(VGroup(Textx2,RoundedRectangle,VGroup)~'Lecture 3')` |
| 77 | l04 ch2 | s6_limits @ 83.9 | glit | Loop arrow, yellow box, and 'may never finish' linger into next shot. | mechanism | D | L305 via sweep_clear: `LaggedStart[FadeOut(Mobject[0]); FadeOut(Mobject[0]); FadeOut(Mobject[0]); FadeOut(Mobje…` |
| 78 | l04 ch2 | s6_limits @ 88.9 | glit | Letter 't' in 'systems' sits too high as a superscript during animatio | yes | E | L314: `FadeIn(VGroup(Textx2)~'large systems:') lag=0.2` |
| 79 | l04 ch2 | s6_limits @ 95.9 | glit | Letter 't' in 'functions' sits too high as a superscript during animat | mechanism | E | L320: `FadeIn(VGroup(Textx2)~'explicit compare functio') lag=0.2` |
| 80 | l04 ch2 | s7_recap @ 37.6 | mism | Pairs show ages (21, 35, 47) instead of telephone numbers mentioned in | no | N | L339: `FlashAround(VGroup(VMobjectx80))` |
| 81 | l04 ch2 | s7_recap @ 41.6 | glit | Names and numbers collide and heavily overlap directly on top of list  | mechanism | B | L353: `RT(VGroup(VMobjectFromSVGPathx2)->VGroup(VMobjectFromSVGPathx2))` |
| 82 | l05 ch1 | s2_why @ 3.0 | glit | Stray rounded box containing digit 1 floating in upper-left margin abo | no | N | L179: `MoveToTarget=(Text'Why sort?'->Text'Why sort?')` |
| 83 | l05 ch1 | s2_why @ 17.0 | glit | Box 8 hovers directly above box 7, overlapping its top edge instead of | no | N | L217: `.animate.move_to(VGroup(Square,Text)~'9')` |
| 84 | l05 ch1 | s2_why @ 22.0 | glit | Lone yellow box displaying truncated name Cle appears briefly before f | mechanism | D | L233: `FadeOut(VGroup(VGroupx3)~'2')` |
| 85 | l05 ch1 | s2_why @ 32.0 | glit | Digit 4 and table icon are superimposed and overlap inside item box 4. | mechanism | D | L262: `FadeOut(Text'4')` |
| 86 | l05 ch1 | s3_binary @ 12.9 | glit | Header morphs through scrambled text Lectur04: inary search, coming ne | mechanism | C | L174: `TransformMatchingStrings(Text'Lecture 4: binary search, coming n'->Text'binary search')` |
| 87 | l05 ch1 | s3_binary @ 27.9 | glit | Faint ghost duplicate of 41 > 37 visible directly underneath active te | yes (mild) | D | L233: `FadeOut(MathTex'41 > 19')` |
| 88 | l05 ch1 | s3_binary @ 52.9 | glit | Numbers 13 and 4 scramble into a jumbled, distorted brown mess before  | mechanism | A | L277: `RT≠(Text'13'->MathTex'O(n)')` |
| 89 | l05 ch1 | s3_binary @ 70.9 | glit | Scrambled intermediate text vs or t appears between linear and binary  | mechanism | D | L320: `FadeOut(Text'linear:')` |
| 90 | l05 ch1 | s4_contest @ 12.1 | glit | Text insertion sort morphs through a blurry distorted brownish-red int | no | D | L199 via sweep_clear: `LaggedStart[FadeOut(Mobject[0]); FadeOut(Text'insertion sort'); FadeOut(Mobject[0]); Fad…` |
| 91 | l05 ch1 | s4_contest @ 14.1 | glit | Stray vertical white stroke artifact cuts downward through text them?. | mechanism | D | L199 via sweep_clear: `LaggedStart[FadeOut(Mobject[0]); FadeOut(Text'insertion sort'); FadeOut(Mobject[0]); Fad…` |
| 92 | l05 ch1 | s4_contest @ 21.1 | glit | Previous title How do we score them? lingers in dark grey overlapping  | yes | D | L216: `FadeOut(Text'How do we score them?')` |
| 93 | l05 ch1 | s4_contest @ 46.1 | glit | Clock icon from previous DECstation shot lingers in upper-right corner | mechanism | D | L260 via sweep_clear: `LaggedStart[FadeOut(VGroup(RoundedRectanglex3,Text,Line)~'% _'); FadeOut(Mobject[0]); Fa…` |
| 94 | l05 ch1 | s4_contest @ 47.1 | glit | Word quicksort briefly pops in truncated as qui before completing. | mechanism | D | L260 via sweep_clear: `LaggedStart[FadeOut(VGroup(RoundedRectanglex3,Text,Line)~'% _'); FadeOut(Mobject[0]); Fa…` |
| 95 | l05 ch1 | s4_contest @ 71.1 | glit | Horizontal dividing rule strikes directly through lower bound: ? befor | no | N | L280: `FlashAround(VGroup(VMobjectx80))` |
| 96 | l05 ch1 | s5_bound @ 6.5 | glit | Letters scramble, duplicate (a b_a b_c), and fly erratically across ca | mechanism | B | L176: `TFC(MathTex'a'->MathTex'a')` |
| 97 | l05 ch1 | s5_bound @ 24.4 | glit | Permutation cards and target boxes collide and overlap in a jumbled me | mechanism | D | L220: `FadeOut(Order(RoundedRectangle,VGroup)~'a')` |
| 98 | l05 ch1 | s5_bound @ 43.5 | glit | Stray empty black rounded rectangular box flickers beneath the yes bra | mechanism | A | L291: `RT≠(Text'yes'->Text'yes')` |
| 99 | l05 ch1 | s5_bound @ 47.5 | glit | Text at best, each question rules out half collides directly over 2^20 | mechanism | D | L298: `FadeOut(Text'twenty questions: about a million ')` |
| 100 | l05 ch1 | s5_bound @ 81.5 | glit | Duplicate gray boxes float above leaf pairs, and second red cross over | mechanism | A | L400: `Transform≠(Text'3 questions'->Text'3 questions')` |
| 101 | l05 ch1 | s5_bound @ 85.5 | glit | Old node labels and '3 questions' linger scrambled across screen and m | mechanism | D | L421: `FadeOut(MathTex'a \le b ?')` |
| 102 | l05 ch1 | s5_bound @ 100.5 | glit | Exponent, inequality sign, and 'n!' scramble and fly apart through gar | mechanism | A | L449: `TFC≠(glyph of '$C$ comparisons: at most'->part of '2 ^{C(n)} \ge n!')` |
| 103 | l05 ch1 | s5_bound @ 102.5 | glit | Formula in yellow box is doubled/garbled, and empty parenthesis appear | yes | B | L457: `TFC(part of '2 ^{C(n)} \ge n!'->part of 'C(n) \ge \log_2 ( n! )')` |
| 104 | l05 ch1 | s6_nlogn @ 2.9 | glit | Characters '(n!)' in top formula are overwritten with scrambled overla | mechanism | B | L93: `TFC(part of 'C(n) \ge \log_2 ( n! )'->part of 'n! = 1 \times 2 \times 3')` |
| 105 | l05 ch1 | s6_nlogn @ 7.9 | glit | Formula morphs through garbled intermediate state with 'log2' glyphs s | mechanism | A | L107: `RT≠(part of 'n! = 1 \times 2 \times 3'->part of '\log_2(n!) = \log_2 1 + ')` |
| 106 | l05 ch1 | s6_nlogn @ 11.9 | glit | Numbers 1 through 8 are cramped and overlapping at far left of x-axis. | no | N | L122: `LaggedStart[FadeIn(Text'1'); FadeIn(Text'2'); FadeIn(Text'3'); FadeIn(Text'4'); +12]` |
| 107 | l05 ch1 | s6_nlogn @ 13.9 | mism | Bars 9 through 13 decrease in height, forming a bell curve before jump | no | N | L133: `LaggedStart[GrowFromEdges(Rectangle[1]->Mobject[0]); GrowFromEdges(Rectangle[1]->Mobject…` |
| 108 | l05 ch1 | s6_nlogn @ 37.9 | glit | Formula 'log2(n!)' overlaps old equation tail '= log2(n!)_2 2 + log2 3 | mechanism | B | L212: `RT(part of '\log_2(n!) = \log_2 1 + '->part of '\tfrac{n}{2}\log_2\tfrac')` |
| 109 | l05 ch1 | s6_nlogn @ 39.9 | glit | Text '24 <=' is doubled with offset orange duplicate colliding directl | mechanism | B | L223: `TFC(part of '24 \le 44.25 \le 64'->part of '\tfrac{n}{2}\log_2\tfrac')` |
| 110 | l05 ch1 | s6_nlogn @ 43.9 | glit | Duplicate superscript '<= 64' floats directly above '<= 64'. | mechanism | B | L227: `TFC(part of '24 \le 44.25 \le 64'->part of '\tfrac{n}{2}\log_2\tfrac')` |
| 111 | l05 ch1 | s6_nlogn @ 49.9 | glit | Label 'O(n log n)' morphs through a scrambled state with letters colli | mechanism | B | L243: `TFC(MathTex'O(n\log n)'->MathTex'O(n\log n)')` |
| 112 | l05 ch1 | s6_nlogn @ 51.9 | glit | Stray brown box pops up, numbers 1, 2, 3 collide with axes, equations  | mechanism | D | L253 via sweep_clear: `LaggedStart[FadeOut(Mobject[0]); FadeOut(Group[0]); FadeOut(Mobject[0]); FadeOut(Mobject…` |
| 113 | l05 ch1 | s6_nlogn @ 59.9 | glit | Faint ghost text of 'Stirling\'s formula; 1.44 \approx log2 e' lingers | mechanism | D | L273 via sweep_clear: `LaggedStart[FadeOut(MathTex'\tfrac{n}{2}\log_2\tfrac{n}{2} \le'); FadeOut(MathTex'O(n\lo…` |
| 114 | l05 ch1 | s6_nlogn @ 82.9 | glit | Scrambled, jumbled white block of distorted glyphs and visual noise ap | mechanism | A | L313: `TFC≠(part of '\log_2(n!) \approx n\log'->part of '10000\log_2 10000 - 1.44')` |
| 115 | l05 ch1 | s6_nlogn @ 85.9 | glit | Previous calculations for 5 items linger as ghost text behind active f | yes | D | L328 via sweep_clear: `LaggedStart[FadeOut(MathTex'\log_2(n!) \approx n\log_2 n - 1.4'); FadeOut(Mobject[0]); F…` |
| 116 | l05 ch1 | s6_nlogn @ 96.9 | glit | Text 'lower bound : ?' is doubled/offset, and '118,458' is doubled acr | mechanism | A | L359: `RT≠(Text'lower bound: ?'->Text'lower bound ≈')` |
| 117 | l05 ch1 | s7_testdata @ 58.5 | glit | Code lines for 'randlist' and previous 'nextrandom' code collide into  | mechanism | D | L267: `FadeOut(RoundedRectangle[1])` |
| 118 | l05 ch1 | s7_testdata @ 70.5 | glit | Faint ghost duplicate of command string lingers above the prompt. | mechanism | D | L306 via sweep_clear: `LaggedStart[FadeOut(Mobject[0]); FadeOut(Mobject[0]); FadeOut(Mobject[0]); FadeOut(Mobje…` |
| 119 | l05 ch1 | s7_testdata @ 89.5 | glit | Stray yellow box, checkmark, and text linger from previous shot with i | yes | D | L368 via sweep_clear: `LaggedStart[FadeOut(Code'# let seed, rs = randlist (1.0, []'); FadeOut(Code'[1484786315.…` |
| 120 | l05 ch1 | s7_testdata @ 92.5 | glit | Stray label '... ends 16807., 1.' from previous shot lingers in bottom | mechanism | D | L376: `FadeOut(Text'… ends 16807., 1.')` |
| 121 | l05 ch1 | s8_recap @ 24.6 | glit | Faint ghost duplicate of bound formula appears directly below fifth bu | no | N | L240: `FadeIn(VGroup(Linex2,VGroup))` |
| 122 | xp ch1 | s1_hook @ 19.0 | glit | Formula text extends past the right screen boundary and is cut off. | mechanism | E | L260: `Write(MathTex'\mathbf a \times \mathbf b = ( a_2')` |
| 123 | xp ch1 | s1_hook @ 28.0 | glit | A stray dot appears at the end of the label: a x b ·. | no | N | L296: `Create(CurvedArrow(ArrowTriangleFilledTip))` |
| 124 | xp ch1 | s2_history @ 15.2 | glit | Stray small i^2 symbol floats near the top left of the bridge arch. | mechanism | E | L159: `Write(MathTex'i^2=j^2=k^2=ijk=-1')` |
| 125 | xp ch1 | s2_history @ 18.1 | glit | A mirrored or upside-down glyph appears in place of k before correctin | yes | E | L159: `Write(MathTex'i^2=j^2=k^2=ijk=-1')` |
| 126 | xp ch1 | s2_history @ 22.1 | glit | Ghost text 'William Rowan Hamilton' lingers faintly beneath the top fo | yes | D | L169 via sweep_clear: `LaggedStart[FadeOut(VGroup(Linex2,VGroupx2,VMobjectx2)); FadeOut(Text'Brougham (Broom) B…` |
| 127 | xp ch1 | s2_history @ 32.1 | glit | An intermediate line of jumbled, garbled, overlapping characters appea | mechanism | A | L128: `RT≠(MathTex'( a_1 \mathbf i + a_2 \mathbf j + '->MathTex'= -\, \mathbf a\cdot\mathbf b +…` |
| 128 | xp ch1 | s2_history @ 43.1 | glit | Lingering orange 'scalar' and cyan 'vector' bounding boxes float at sc | mechanism | D | L242 via sweep_clear: `LaggedStart[FadeOut(MathTex'q = w + x\,\mathbf i+y\,\mathbf j+'); FadeOut(Rectangle[1]);…` |
| 129 | xp ch1 | s2_history @ 54.1 | glit | A stray orange vertical bar cursor appears after b. | no | N | L128: `.animate.set_opacity(MathTex'( a_1 \mathbf i + a_2 \mathbf j + ')` |
| 130 | xp ch1 | s2_history @ 65.2 | glit | Ghost text of the crossed-out equation lingers above Gibbs' name. | mechanism | D | L128: `FadeOut(MathTex'( a_1 \mathbf i + a_2 \mathbf j + ')` |
| 131 | xp ch1 | s2_history @ 73.2 | glit | Text blocks collide; 'cross product' jams directly into a x b. | mechanism | D | L382: `FadeOut(Group(VGroupx2,Text)~'J. Willard Gibbs')` |
| 132 | xp ch1 | s2_history @ 74.7 | glit | Two Nature labels appear simultaneously, one directly covering a · b. | no | N | L128: `LaggedStart[UpdateFromAlphaFunc(VGroup(RoundedRectangle,Text)~'Nature'); UpdateFromAlpha…` |
| 133 | xp ch1 | s2_history @ 80.2 | glit | Ghost text from previous slide lingers faintly across the background. | mechanism | B | L401: `RT(part of '= -\, \mathbf a\cdot\mat'->MathTex'\mathbf a\times\mathbf b')` |
| 134 | xp ch1 | s3_physics @ 21.1 | glit | Labels r and F double into rr and FF; garbled formula appears. | yes | B | L234: `TFC(MathTex'\mathbf r'->part of '\boldsymbol\tau = \mathb')` |
| 135 | xp ch1 | s3_physics @ 49.1 | glit | Labels double into aa and bb before resolving. | mechanism | A | L382: `TFC≠(MathTex'\mathbf a'->part of '/\mathbf a/ \,/\mathbf b')` |
| 136 | xp ch1 | s3_physics @ 52.1 | timi | Label a x b appears floating prematurely before the arrow grows to it. | yes | T | L388: `FadeIn(MathTex'\mathbf a\times\mathbf b')` |
| 137 | xp ch1 | s4_define @ 5.1 | glit | Ghost copy of b = (1, 2, 0) appears offset above-right before snapping | no | N | L204: `GrowFromPoints(VGroup(Line3D,Cone)->Mobject[0])` |
| 138 | xp ch1 | s4_define @ 12.1 | glit | Stray lowercase glyph w appears near the right edge of the screen. | yes | E | L221: `Write(part of '/\mathbf a\times\mathbf ')` |
| 139 | xp ch1 | s4_define @ 66.1 | glit | Arrow shaft is bent into a severe zig-zag before snapping straight. | mechanism | D | L377: `FadeOut(VGroup(Line3D,Cone))` |
| 140 | xp ch1 | s5_rules @ 14.9 | glit | b x a collides with vector coordinates, reading a = (3, 0, b) x a. | mechanism | B | L367: `TFC(glyph of '\mathbf b\times\mathbf a'->glyph of '\mathbf b\times\mathbf a')` |
| 141 | xp ch1 | s5_rules @ 21.9 | glit | Garbled, backwards glyph appears in place of the second a. | mechanism | E | L389: `Write(MathTex'\mathbf a\times\mathbf a = {?}')` |
| 142 | xp ch1 | s5_rules @ 28.9 | glit | Question mark morphs through a scrambled, distorted intermediate state | mechanism | A | L415: `Transform≠(part of '\mathbf a\times\mathbf a'->part of '\mathbf a\times\mathbf a')` |
| 143 | xp ch1 | s5_rules @ 38.0 | glit | Stray yellow dot lingers floating in space above the x-axis. | mechanism | D | L436 via sweep_clear: `LaggedStart[FadeOut(VGroup(Linex11)); FadeOut(ThreeDAxes(NumberLinex3)); FadeOut(MathTex…` |
| 144 | xp ch1 | s5_rules @ 48.0 | glit | Duplicate stray letter k floats between equation and table. | mechanism | B | L477: `TFC(part of '\mathbf i \times \mathbf'->MathTex'\mathbf k')` |
| 145 | xp ch1 | s5_rules @ 52.0 | mism | Equation erroneously displays j x k = j. | mechanism | C | L486: `TransformMatchingStrings(MathTex'\mathbf j \times \mathbf k = \math'->MathTex'\mathbf k …` |
| 146 | xp ch1 | s5_rules @ 63.0 | glit | Text inside parentheses scrambles and doubles with dots over character | mechanism | A | L545: `TFC≠(VGroup(MathTexPartx5)~of'( \mathbf i \times \math'->part of '( \mathbf i \times \ma…` |
| 147 | xp ch1 | s5_rules @ 69.0 | glit | Equation appears scrambled and doubled: i x (i (i x j) j). | mechanism | A | L555: `TFC≠(VGroup(MathTexPartx5)~of'\mathbf i \times ( \math'->part of '\mathbf i \times ( \ma…` |
| 148 | xp ch1 | s5_rules @ 73.0 | glit | Every character and parenthesis is doubled: ii x ((ii x jj). | yes | B | L563: `TFC(part of '( \mathbf i \times \math'->part of '( \mathbf i \times \math')` |
| 149 | xp ch1 | s6_machine @ 4.5 | glit | Stray white curved arrow scribble appears in upper-left corner. | mechanism | E | L517: `Write(VGroup(MathTexPartx7)~of'\mathbf a \times ( \math')` |
| 150 | xp ch1 | s6_machine @ 8.0 | glit | Formula shows stray angle bracket ">" after "a" on the right side of " | mechanism | E | L519: `Write(VGroup(MathTexPartx8)~of'\mathbf a \times ( \math')` |
| 151 | xp ch1 | s6_machine @ 33.0 | glit | Stray red text "a >" appears floating below "the angle to a changes". | mechanism | D | L538: `LaggedStart[FadeOut(MathTex'\text{multiply out brackets}\;\lon'); FadeOut(MathTex'/\math…` |
| 152 | xp ch1 | s6_machine @ 92.0 | glit | Middle flowchart box displays jumbled text "ro a x ( 90 )" instead of  | mechanism | D | L648: `FadeOut(MathTex'\mathbf a \times (\quad\;\;)')` |
| 153 | xp ch1 | s6_machine @ 107.0 | glit | Coordinate vectors "(1, 2, 0)" and "(0, 2, 0)" collide and overlap int | mechanism | A | L686: `TFC≠(MathTex'(1,2,0)'->MathTex'(0,2,0)')` |
| 154 | xp ch1 | s6_machine @ 111.0 | glit | Coordinates "(0, 2, 0)" and "(0, 0, 2)" collide into overlapping, garb | mechanism | A | L689: `TFC≠(MathTex'(0,2,0)'->MathTex'(0,0,2)')` |
| 155 | xp ch1 | s6_machine @ 115.0 | glit | Coordinates "(0, 0, 2)" and "(0, 0, 6)" collide into overlapping, garb | mechanism | A | L692: `TFC≠(MathTex'(0,0,2)'->MathTex'(0,0,6)')` |
| 156 | xp ch1 | s7_linear @ 56.8 | glit | Yellow text displays misspelled word "vinier" instead of "linear". | no | N | (no play: still frame) |
| 157 | xp ch1 | s7_linear @ 69.8 | glit | Equation line "= - a x b - a x c" appears doubled and superimposed on  | mechanism | C | L564: `TransformMatchingStrings(MathTex'=-\,\mathbf a\times\mathbf b-\math'->MathTex'=\mathbf b…` |
| 158 | xp ch1 | s8_components @ 6.8 | glit | Formula displays "b_{21}" with subscript 21 instead of "b_2 j". | mechanism | E | L348: `Write(MathTex'\mathbf b = b_1\mathbf i + b_2\mat')` |
| 159 | xp ch1 | s8_components @ 9.8 | glit | Entire equation line is heavily doubled with scrambled glyphs, triple  | mechanism | A | L364: `RT≠(part of '\mathbf a = a_1\mathbf i'->part of '\mathbf a\times\mathbf b')` |
| 160 | xp ch1 | s8_components @ 11.8 | glit | Duplicate row of equation terms appears shifted directly below the mai | mechanism | B | L378: `TFC(part of '\mathbf a\times\mathbf b'->MathTex'a_1\mathbf i')` |
| 161 | xp ch1 | s8_components @ 26.8 | glit | Table cell displays "a_2 \theta_3 (j x k)" with Greek letter theta rep | mechanism | B | L462: `TFC(part of '\mathbf 0'->part of '( \mathbf 0 )')` |
| 162 | xp ch1 | s8_components @ 43.8 | glit | Cell term "-a_2 b_1 k" is doubled in red, and stray text "0 a_1 b_2 k" | mechanism | B | L506: `TFC(part of '- a_2b_1 \,\mathbf k'->part of '\mathbf a\times\mathbf b')` |
| 163 | xp ch1 | s8_components @ 47.8 | glit | Duplicate "-a_3 b_2 i" appears below cell, and "j" sits outside cell b | mechanism | B | L513: `RT(part of 'a_2b_3 \,(\mathbf j\time'->part of 'a_2b_3 \,\mathbf i')` |
| 164 | xp ch1 | s8_components @ 54.8 | glit | Stray vertical bar "/" appears after line 1 and stray bracket after li | no | N | L546: `FlashAround(VGroup(VMobjectx80))` |
| 165 | xp ch1 | s8_components @ 74.8 | glit | Equation "(1, 2, 3) x (4, 5, 6) = (-3, 6, -3)" is doubled and superimp | mechanism | B | L618: `TFC(part of '(1,2,3) \times (4,5,6) ='->part of '(-3,6,-3) \cdot (1,2,3) ')` |
| 166 | xp ch1 | s8_components @ 76.8 | glit | Both zero results display an errant horizontal macron bar over them (" | no | N | L620: `FlashAround(VGroup(VMobjectx80))` |
| 167 | xp ch1 | s8_components @ 81.8 | glit | Faint leftover equation "(3, 0, 0) x (1, 2, 0) = (0, 0, 6)" lingers in | yes | D | L632 via sweep_clear: `LaggedStart[FadeOut(MathTex'\mathbf a\times\mathbf b = ( a_2b_'); FadeOut(Mobject[0]); F…` |
| 168 | xp ch1 | s8_components @ 82.8 | glit | Two checkbox icons overlap and double before resolving into a single i | mechanism | D | L636: `FadeIn(VGroup(RoundedRectanglex2,MathTexx2)~'\cdot')` |
| 169 | xp ch1 | s8_components @ 115.8 | glit | Vector "c" in "a . (b x c)" appears with an outline blackboard-bold fo | mechanism | E | L661: `Write(MathTex'\mathbf a\cdot(\mathbf b\times\mat')` |
| 170 | xp ch1 | s8_components @ 129.8 | glit | Bullet point text is truncated mid-phrase as "Torque, an" instead of f | mechanism | E | L688: `FadeIn(VGroup(Text,VGroup)~'Recap') lag=0.05` |
| 171 | st ch1/2 | s2_crew @ 85.2 | glit | stray Opus badge upper right | no: badge placed at [6, 1.9] by design (layout, not a transition) | N | L302 |
| 172 | st ch1/2 | s2_crew @ 87.2 | glit | leftover text overlaps .claude/agents/ | yes | D | L303 FadeOut(prompt…) + FadeIn(legend) same place |
| 173 | st ch1/2 | s2_turns @ 72.1 | glit | 'per million tokens' rotated | yes: '$0.20' doubled (no rotation seen); A seen 3 s later | B | L474 TFC '$0.20'; L478/481 TFC '$5'->'$2.50', '$20'->'$10' |
| 174 | st ch1/2 | s5_anatomy @ 30.8 | mism | 9 red squares labeled ~13 | no (content) | N | L265 |
| 175 | st ch1/2 | s5_anatomy @ 40.9 | glit | stray green square floats | yes (tiles fly apart into one segment) | A | L273 TFC(VGroup(3 scattered tiles) -> 1 segment) |
| 176 | st ch1/2 | s6_dials @ 52.2 | glit | stray red formula e^-x | yes ('extr', partial glyphs) + A '$159'->'≈ $278' | E | L343 FadeIn(ex_lbl, lag_ratio=0.3); ReplacementTransform(s_tot, new_tot) |
| 177 | st ch1/2 | s6_dials @ 65.2 | glit | caveat lingers into next shot | yes (kept on purpose: keep=[self.cav]) | K | L362 sweep_clear(keep=[cav]) |
| 178 | st ch1/2 | s7_second @ 54.0 | mism | failed idea box green | no (content) | N | L151 |
| 179 | st ch1/2 | s7_second @ 71.8 | glit | note scrambles into corrupted glyphs | yes | A | L161 ReplacementTransform(T 'median 0…', T 'arbitrary…') |
| 180 | st ch1/2 | s7_second @ 88.5 | glit | item 1 text overlaps green box | yes | D | L194 FadeTransform(card, item) |
| 181 | l03 ch4* | s4_cells @ 27.5 | glit | stray digit 4 under cells | yes | C | L163 TransformMatchingShapes(red_lbl, xs_back) (Code) |
| 182 | l03 ch4* | s5_nrev @ 21.0 | glit | box 2 collides with box 3 | no (cells sliding together) | N | L- |
| 183 | l03 ch4* | s5_nrev @ 30.0 | glit | digits switch to Fraktur | yes ('3₃' doubled, serif->Menlo morph) | A | L109 birth(): TFC(serif value_label, Mono glyph) |
| 184 | l03 ch4* | s6_cost @ 0.0 | glit | unmatched parenthesis | no | N | - |
| 185 | l03 ch4* | s6_cost @ 67.8 | mism | n+1 wide vs n tall | no (Gemini miscount) | N | - |
| 186 | l03 ch4* | s6_cost @ 69.5 | glit | bracket spans 7 of 8 columns | no (grid is 7 wide) | N | - |
| 187 | l03 ch4* | s6_cost @ 69.5 | mism | vertical bracket n+1 | no | N | - |

## Appendix: the study's tools (scratch, not installed)
In a session scratchpad (not kept):
`glitch_review.py` + `run_glitch.sh` (the transition-prompt review), `playlog.py` (dry-run play
logger with glyph-identity markers), `mapf.py` (finding → active plays), `classify.py` + `final.py`
+ `gen_table.py` (classes and this table), `early.py` + `runmany.py` (label timing over all
scenes), `sheet.py` (frame contact sheets), `when.py` (chapter time ↔ scene/clip). Data:
`plays2/`, `early/`, `final.json`. The play logger and the label-timing matcher are the
prototypes of check.py's T1–T3 and E1.
