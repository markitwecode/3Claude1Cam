# How 3Blue1Brown builds, paces and reveals ideas

Measured from Grant Sanderson's own video code. Paths are relative to `reference/3b1b/videos/`
unless they start with `manimgl/`. All snippets are **ManimGL** (`from manimlib import *`), so
port the idea and don't paste the code (API translation: `GL_TO_CE.md`). Our own rules in
`STYLE.md` / `LESSONS.md` win wherever they disagree with anything here.

Numbers come from `tools/pacing_stats.py` (stdlib; parses with `ast`, never runs his code):
`python3 -I reference/3b1b/tools/pacing_stats.py` covers 2023–2026; `--help` lists `--projects`,
`--by-year`, `--exclude`, and `--examples FlashAround` (every use as file:line).

## 1. Pacing, measured (2023–2026)

Corpus: 111 of 112 files parse (`_2023/optics_puzzles/slowing_waves_insert_embed.py` has a stray
`self.embed()` and doesn't), 1,625 scene classes, 8,955 `self.play`, 5,786 `self.wait`.
ManimGL defaults: `run_time` 1.0 s (`manimgl/manimlib/animation/animation.py:19`), bare
`wait()` 1.0 s (`manimgl/manimlib/scene/scene.py:77`, `default_config.yml:86`), `LaggedStart`
lag 0.05 (`composition.py:24`), `LaggedStartMap` 2 s, `TransformMatching*` 2 s, `Write` 1 or 2 s
by sub-path count (`creation.py:173-176`).

| Measure | Median | p25–p75 | p90 | Notes |
|---|---|---|---|---|
| Effective play duration (explicit, else class default) | **1.5 s** | 1–2 s | 5 s | 45% are exactly 1 s (the default), 18% 2 s, 10% 1.5 s. Pi-creature plays excluded |
| Play-level `run_time=` when given (25% of plays) | 3 s | 2–5 s | 10 s | modes 2 s (29%), 3 s (20%). Camera moves alone: median 3 s, p90 12 s (n=1,095) |
| `run_time` on an animation inside a play | 2 s | 1.5–3 s | 5 s | 2 s is 34% of them |
| `wait()` | **1 s** | 1 s | 3 s | **70% are bare `wait()`** = 1 s |
| Explicit `wait(n)` only | 3 s | 2–4 s | 9 s | modes 2 s (29%), 3 s (17%); `wait(0.5)` 6% |
| Plays back to back before a wait | **1** | 1–2 | 3 | 68% one, 21% two, 7% three. 64% of plays are followed straight by a `wait` |
| **Beat** = run of plays + the wait(s) after it | **3 s** | 2–5 s | 10 s | the screen is still for a median **40%** of each beat (p25 25%, p75 50%) |
| Animations passed to one `play` | 1 | 1–2 | 4 | 50% one, 26% two, 12% three |
| `lag_ratio` literal values (in 19% of plays) | 0.1 | 0.05–0.25 | 0.5 | modes 0.1 (30%), 0.5 (12%), 0.01 (10%), 0.2, 0.25 (9% each) |
| Plays per scene (scenes with ≥1 play) | 3 | 1–6 | 14 | max 121 (`_2024/transformers/mlp.py:390`); 199 scenes have no play at all |
| Straight-line scene length (estimate, n=191) | 15 s | 8–38 s | 75 s | 31% of it is `wait` |

`lag_ratio` by context: `LaggedStart` median 0.2, `LaggedStartMap` 0.25 (p75 0.5),
`AnimationGroup` 0.2, `FadeIn(group, lag_ratio=…)` 0.1, `Write` 0.02, `ShowCreation` 0.01
(plus 418 `LaggedStart`/`LaggedStartMap` left at the 0.05 default).

Most-used arguments to `play` (share of 17.6k): `.animate` 23.7% (methods: `reorient` 793, i.e.
camera, `set_opacity` 565, `set_value` 542, `move_to`, `shift`), `FadeIn` 12.5%, `FadeOut` 11.8%,
`Write` 5.7%, `ShowCreation` 5.1%, `LaggedStart` 3.7%, `LaggedStartMap` 3.4%, `TransformFromCopy`
3.0%, `MoveToTarget` 1.7%, `ReplacementTransform` 1.6%, `GrowArrow` 1.4%, `Transform` 1.3%,
`FadeTransform` 1.2%, `Restore` 1.1%, `TransformMatchingTex` 0.9%, `FlashAround` 0.6%.
Pi-creature calls (`change`, `says`, `Blink`, …) are 11% of plays. `Indicate(` is on 19 lines,
16 of them in two files written in a different style (see caveats): Grant himself essentially
never uses it. 28% of `FadeIn`s carry a shift (`UP`, `DOWN`, `0.5 * UP` most common).
`rate_func` is overridden in about 3% of plays (`linear` 113, `there_and_back` 56). 53% of scenes
begin with `self.add` (continuing the previous scene's state) and 74% end on a `wait`.

The CS-flavoured videos (`--projects _2024/transformers _2026/cross_entropy _2025/grover`, 2,556
plays) run slightly quicker: effective play median **1.0 s** (p75 2, p90 3), explicit play-level
`run_time` median 2 s, explicit wait median 2 s, beat median 3 s (p75 4.6), `lag_ratio` in 27%
of plays, straight-line scene median 13 s.

**What this means for a narrated video (our ~160 wpm ≈ 2.7 words/s):**
- The rhythm is **play, then hold**. One change, then stillness. A median beat of 3 s is about
  8 spoken words, so roughly one visual change per clause, and a 15-word sentence gets two beats.
- Let animations fill about half to two-thirds of the gap to the next cue and hold for the rest
  (he holds ~40% of each beat). In our pipeline: `run_time` a little short of `c.until(cue)`,
  then `c.wait_until(cue)`.
- Durations: incidental fades 1 s; a transform that *carries meaning* (`TransformFromCopy`,
  `ReplacementTransform`, `MoveToTarget`, `FadeTransform`) 2 s is his explicit median; big
  restructures 3 s; "feel how long this takes" sweeps 5–20 s at `rate_func=linear`. STYLE.md's
  0.8–1.5 s for meaningful animations is on the brisk side of him; 1.5–2 s is closer.
- Never more than 2–3 animations per play (88% of his plays), and lag 0.1–0.25 when a group
  enters, 0.5+ when the items should be read one after another.

**Caveats.** These are static counts of source: plays inside loops (9%) and helper methods
are counted once, and inherited `construct`s aren't counted. He renders many short scenes and
assembles them in an editor (`stage_scenes.py` orders the renders, `GRANT_CLAUDE.md.txt:22`)
against narration recorded separately, so a bare `wait()` is often a "hold here while I talk"
placeholder that the edit stretches or trims; 199 scenes have no `play` at all (stills).
Some long waits are presenter-mode holds: `self.wait(10, note="Talk through projection")`
(`_2024/puzzles/added_dimension.py:600`), and in presenter mode `wait` blocks until a key
press (`manimgl/manimlib/scene/scene.py:605-608`). Two big 2026 files,
`_2026/cross_entropy/robot.py` (8.8k lines) and `_2026/2025_P6/p6.py`, are written in a different
style (explicit `wait(1)`/`wait(2)`, never a bare `wait()`). They are why 2026 has only 50%
bare waits against 73–81% in 2023–25 (`--by-year`); whether someone else wrote them is not
stated in the repo. `--exclude robot.py p6.py` gives 76% bare waits, explicit-wait median 3 s.
Absolute seconds matter less than the *proportions*: his edit adjusts timing, while ours is set
by the voice track.

## 2. Patterns

Counts in [brackets] are non-comment source lines in 2023–2026, from the script's "idiom line
counts" block. Snippets are trimmed (`...`) or condensed; the cited lines have the full code.

### Introducing a thing and letting it sit

**P1. One change, then hold.** Each beat of a long walkthrough is a comment, one `play`, one
`wait`. The next change only happens after the hold.
```python
# Sequence of embeddings comes in to an MLP block            (mlp.py:399)
self.play(FadeIn(embedding_array, shift=2 * OUT))
self.wait()
# Highlight one vector                                        (mlp.py:419)
self.play(MoveToTarget(embedding_array), ShowCreation(highlight_rect))
self.wait()
```
`_2024/transformers/mlp.py:399-433` (`BasicMLPWalkThrough`, 121 plays, 78 waits).
*Ours:* one `{mark}` per beat; `play(..., run_time=…)` then `c.wait_until(next mark)`.

**P2. Preview the whole pipeline before explaining any step.** He shows Linear → ReLU →
Linear on one vector as three arrows and vectors (`LaggedStartMap(FadeIn, vects, shift=RIGHT,
lag_ratio=0.8)`), then every vector gets a copy of the circuit
(`LaggedStart(TransformFromCopy(simple_phases, sp_copy) …, lag_ratio=0.1), run_time=3`), and only
then the steps one by one: up-projection, ReLU, down-projection.
`_2024/transformers/mlp.py:456-487, 504-532`, then `571`, `1088`, `1336`.
*Ours:* show `rev [1;2;3]`'s whole trace skeleton first, then do call 1 slowly.

**P3. Enter with a direction.** 28% of his `FadeIn`s carry a shift, most often `UP`, `DOWN`,
`0.5 * UP`. Labels drop in toward what they name: `FadeIn(label, 0.5 * DOWN)` with
`GrowFromCenter(brace)` (`_2024/transformers/network_flow.py:797-800`); a key icon drops in
under its number, `FadeIn(key_icon, 0.25 * DOWN)` (`_2025/grover/runtime.py:258-262`).
*Ours:* CE `FadeIn(m, shift=0.3 * DOWN)`. Keep shifts small (0.25–0.5).

**P4. Build the final layout first, then animate *into* it.** Lay everything out, `save_state()`,
collapse it, and `Restore`. Bars grow from zero height while their percentages count up:
```python
bar.save_state()
bar.stretch(0, 1, about_edge=DOWN)
bar.set_opacity(0)
...
self.play(LaggedStartMap(Restore, bars, lag_ratio=0.01),
          LaggedStartMap(CountInFrom, decs, lag_ratio=0.01), run_time=4)
```
`_2022/wordle/scenes.py:2846-2857`; covers growing out of their left edge,
`_2025/grover/runtime.py:20-34` [`.save_state()` 404, `Restore(` 219].
*Ours:* build the full `ConsChain` laid out correctly, then reveal or restore parts of it. Don't
compute positions mid-animation.

**P5. New things come out of old things.** `TransformFromCopy` is his most-used Transform
(840 lines; passed to 529 plays directly, vs 291 `MoveToTarget`, 277 `ReplacementTransform`): a
result is born from the thing it was computed from, while the source stays put.
Each prediction step grows from an invisible copy of the previous one:
```python
self.play(TransformFromCopy(last_group[0], rect),
          TransformFromCopy(last_group[1], arrow), ...)
self.wait()
last_group = VGroup(rect, arrow, prediction)
```
`_2024/transformers/generation.py:920-935`.
*Ours:* the head value flies out of the code `x :: xs` into the new cell's slot; a frame of the
trace comes out of a copy of the frame above.

### Emphasis

**P6. `FlashAround` plus a colour change, never `Indicate`.** [`FlashAround(` 124 lines in 40
files; `Indicate(` 3 lines once two differently-styled files are excluded.] His signature call:
```python
self.play(FlashAround(formulas[-1], run_time=2, time_width=1.5))      # clt/main.py:1518
self.play(FlashAround(key_input),
          key_input.animate.set_color(YELLOW),
          FadeIn(key_icon, 0.25 * DOWN))                               # grover/runtime.py:258-262
```
The flash's colour can match the object: `color=BLUE` for a blue label
(`_2025/grover/state_vectors.py:1700-1703`). FlashAround removes itself, so nothing needs undoing.
*Ours:* `Circumscribe(m, color=YELLOW, time_width=1.5, run_time=2)` or
`ShowPassingFlash(SurroundingRectangle(m).set_stroke(YELLOW, 4), time_width=1.5)`. Both are
stroke-only, so they avoid the LESSONS.md `Indicate` flood.

**P7. Underline a phrase and recolour it in the same play, so the emphasis stays.**
```python
self.play(FlashUnder(question[r"95% sure"], color=TEAL),
          question[r"95% sure"].animate.set_color(TEAL))
```
`_2023/clt/wordy_scenes.py:933-936`; the same with a drawn `Underline` that stays,
`_2025/laplace/main_equations.py:1576-1591` [`FlashUnder(` 22].
*Ours:* `ShowPassingFlash(Underline(tok).set_stroke(YELLOW, 4), time_width=1.5)` together with
`tok.animate.set_color(YELLOW)`.

**P8. A highlight box that slides from term to term.** Draw a box once, then move it onto each
term while talking: `stroke YELLOW 2`, `fill YELLOW 0.25`, behind the text.
```python
self.add(rect, coulombs_law)        # rect drawn behind the formula
self.play(FadeIn(rect)); self.wait()
self.play(rect.animate.surround(coulombs_law[R"4 \pi \epsilon_0"])); self.wait()
self.play(rect.animate.surround(coulombs_law[R"\frac{1}{r^2}"])); self.wait()
```
`_2023/optics_puzzles/e_field.py:202-219` [`.animate.surround(` 119].
*Ours:* CE `surround` keeps the aspect ratio (`manim/mobject/mobject.py:2056`). Use
`rect.animate.become(SurroundingRectangle(next_tok, buff=0.05))`. This is the right tool for
stepping through `x :: xs` token by token.

**P9. Spotlight by dimming the rest.** Most common dim levels: `set_opacity(0.2)`, `0.25`,
`0.35`, or `fade(0.75)` [`.animate.set_opacity(` 585]. Others dim and a box appears on the
chosen one in the same play:
```python
ndp_columns[:index].animate.set_opacity(0.35),
ndp_columns[index + 1:].animate.set_opacity(0.35),
```
`_2024/transformers/attention.py:883-889`; per-item loop with `wait(0.5)`,
`_2024/transformers/embedding.py:432-447`; dim all rows, `Restore` one,
`_2025/laplace/exponentials.py:1899-1903`. When a new line arrives he dims the previous one to
0.5 (`_2023/clt/main.py:1346-1349`).
*Ours:* CE `fade()` multiplies the current opacity (`vectorized_mobject.py:557-560`), so use
explicit `set_opacity(0.25)` and restore to 1.

**P10. Backstroke text over busy backgrounds.** `weight_words.set_backstroke(BLACK, 8)` on a
label over a grid (`_2024/transformers/attention.py:878`); braces get one too
(`_2023/gauss_int/integral.py:63-65`) [`.set_backstroke(` 258, most often `(BLACK, 3–5)`].
*Ours:* `set_stroke(BG, 5, background=True)` on labels that sit over arrows or cells.

### Stepping through an expression

**P11. A vertical derivation: copy the line, transform the copy into the next line, hold.**
```python
for line1, line2 in zip(new_lines, new_lines[1:]):
    ...
    self.play(TransformMatchingTex(line1.copy(), line2, key_map=key_map, run_time=1, lag_ratio=0.01))
    self.wait()
```
`_2025/laplace/shm.py:735-765`. The lines are built up front, arranged `DOWN,
aligned_edge=LEFT`, and the first step's `key_map` substitutes values in
[`TransformMatchingTex(` 177; `key_map=` 52].
*Ours:* `[3; 5; 9]` → `3 :: [5; 9]` → `3 :: 5 :: [9]` → `3 :: 5 :: 9 :: []` as stacked
lines. CE `TransformMatchingTex` matches whole `MathTex` parts split with `{{ }}`; for `Code`
or `Text` swap single tokens in place (LESSONS.md).

**P12. Substitute with a box that rides along.** Box the part about to change, transform, and
move the box onto the replacement in the same play; then fade the box.
```python
self.play(ShowCreation(v0_rect))
self.play(TransformMatchingTex(ddx_lt_rhss[0], ddx_lt_rhss[1], ...,
              key_map={R"x'(0)": R"v_0"}, run_time=1),
          v0_rect.animate.surround(ddx_lt_rhss[1][R"v_0"]))
self.play(FadeOut(v0_rect))
```
`_2025/laplace/derivatives.py:912-924`.
*Ours:* unfolding `length (x :: xs)` → `1 + length xs`: box `length xs`, rewrite, box follows.

**P13. Unroll a recursion one level per beat.** `b_8 = π/4 b_6` → `… b_4` → `… b_2` → `… b_0`,
each `TransformMatchingTex(stages[i], stages[i+1], key_map={"b_6": "b_4"}, run_time=1)` plus a
`wait()` (`_2026/spheres_talk/volumes.py:363-367, 413-418`).
*Ours:* `3 :: (5 :: (9 :: []))` and the trace of `sum [3;5;9]` both fit this.

**P14. Build the right-hand side piece by piece.** Write the fraction bar, hold; write
`· (7 − 1)`, hold; write the `2`, hold (`_2023/moser_reboot/main.py:248-257`).
*Ours:* a cost formula like `n + (n−1) + … + 1 = n(n+1)/2`, one term per narration beat.

### Labels: braces and arrows

**P15. Grow the brace from its centre, drop the label in, hold; make the brace hop.**
```python
self.play(GrowFromCenter(brace), FadeIn(label, 0.5 * DOWN))
self.wait()
...
self.wait(3)                                    # after the key number lands
```
`_2024/transformers/network_flow.py:786-812`. A brace that hops between tokens with a
`wait()` after each: `self.play(brace.animate.become(Brace(token_rects[index], buff=0.05)))`
(`_2024/transformers/embedding.py:251-257`) [`Brace(` 227; `GrowFromCenter(...brace` 125].
*Ours:* head/tail braces over a `ConsChain`. CE `brace.get_text` makes LaTeX; for prose use
`T(...)` with `label.next_to(brace, DOWN)`.

**P16. Arrows: `GrowArrow`, label in the arrow's colour.** [`GrowArrow(` 294 lines vs
`ShowCreation(…arrow` 66.] Name in YELLOW, `Arrow(name, target).match_color(name)`, then
`Write(name)` with `ShowCreation(arrow)`, `wait()` (`_2023/clt/main.py:1340-1355`). An arrow
that must keep pointing at a moving target gets an updater (`clt/main.py:1211-1214`). One label
for many items: arrows from the label to each item,
`LaggedStartMap(VFadeInThenOut, arrows, lag_ratio=0.25, run_time=4)`
(`network_flow.py:217-219`).
*Ours:* `label_pointer` / `link`, introduced with `GrowArrow`. `follow=True` links ignore colour
changes (LESSONS.md).

### Colour carries meaning

**P17. One symbol, one colour, for the whole video.** In `_2025/laplace` every `"{s}"` key in
a colour dict maps to YELLOW (34 of 34: `grep -rhoE '"\{s\}": [A-Z_]+' _2025/laplace | sort | uniq -c`),
with module constants
`S_COLOR = YELLOW`, `T_COLOR = BLUE` (`exponentials.py:5-6`). A module-level `EQUATION_T2C` is
reused for boxes and words, not just TeX: `VGroup(lf_rect, lf_words).set_color(EQUATION_T2C[
R"\omega_l"])` (`_2023/optics_puzzles/ior_annotations.py:5-12, 1093-1094`). Category colours live
on the class: `QueryMap.map_color = YELLOW`, `KeyMap.map_color = TEAL`
(`_2024/transformers/attention.py:1715-1721, 1841-1842`) [`t2c=` 587].
*Ours:* the palette in STYLE.md is this dict. A highlight box, its label and the flash all take
the colour of the thing they point at.

### Clearing and transitions

**P18. Clear the board in a lagged sweep, keep what the next idea needs.**
```python
# Clear the board
self.play(LaggedStart(FadeOut(implies), FadeOut(cos_equation), ...,
                      FadeOut(consolidated_lines[2:]), ..., lag_ratio=0.1))
```
`_2025/laplace/shm.py:721-731` keeps `consolidated_lines[:2]`. Other forms: fade everything
while a copy of the key equation shrinks to the corner as a reminder
(`_2023/optics_puzzles/annotations.py:528-537`); fade the board while
`TransformFromCopy` carries one piece into the next idea (`_2025/laplace/main_equations.py:598-608`);
a title fades out while one of its words becomes the next heading
(`_2023/gauss_int/supplements.py:705-725`) [`LaggedStartMap(FadeOut` 104; `self.clear()` 41, a hard cut].
*Ours:* do this at the start of the next `say` block (STYLE.md). Carry the one object the next
idea builds on rather than fading everything.

### Counting, cost and growth

**P19. A counter bound to what it counts, animated with it.** The count is a function of the
things on screen: `f_always(counter.set_value, lambda: len(one_rects))`, then
`ShowIncreasingSubsets(one_rects)` makes it tick (`_2020/hamming.py:128-134, 2062`). Or play the
number and the items together over the same `run_time=3`:
`ChangeDecimalToValue(rhs_num, choose(self.n, 2), run_time=3), ShowIncreasingSubsets(pair_rects,
run_time=3)` (`_2023/moser_reboot/main.py:235-240`). A step counter can be pinned to a corner
(`_2025/colliding_blocks_v2/blocks.py:1150-1154`).
*Ours:* "cells copied: n" in GOLD next to `append`, `ChangeDecimalToValue` stepped with each copy.

**P20. Two growth rates, the bigger one hidden until the reveal.** Chords (∝ n) and their
intersections (∝ n²) get live counters. When the chords jump to 100, a `cover_rect` hides the
intersection count; then `FadeOut(cover_rect)` while the counter races up
(`_2026/monthly_mindbenders/chords.py:24-35, 75-89`).
*Ours:* the O(n) vs O(n²) reveal for `rev`: run both counters, cover the n² one, hold, uncover.

**P21. Growth curves one at a time, label riding the tip; then concrete numbers.** Five
complexity curves, each `ShowCreation(graph)` with its label pinned to the end by
`UpdateFromFunc` (`_2025/grover/runtime.py:184-213`). Then "N = 10⁶ → ~10³ steps", with a box
sliding from √N onto the number (`runtime.py:903-936`), and a literal 9⁶⁰ printed in full under a
brace (`_2025/grover/clarification.py:1347-1350`).
*Ours:* plot n and n²/2, then "n = 1,000 → 500,000 conses" spelled out.

### Camera

**P22. Zoom in on a detail and come back.** [`frame.save_state()` 33; plays that move the camera:
median 3 s, p25–p75 2–6 s.]
```python
frame.save_state()
self.play(frame.animate.set_height(4).move_to(Group(low_rect, low_title)), ..., run_time=2)
self.wait()
self.play(Restore(frame), run_time=2)
```
`_2024/holograms/supplements.py:305-318`. Labels that must not move with the camera use
`fix_in_frame()` (`_2024/inscribed_rect/loops.py:1806-1807`).
*Ours:* `MovingCameraScene`, `self.camera.frame.save_state()` / `Restore(self.camera.frame)`, 2 s
each way. Use it only for chains too long for the frame (a 20-cell `append`).

### Suspense and reveals

**P23. Ask, hold, then answer.** The question goes on screen as an object: `Tex(R"???",
font_size=90)` over the mystery machine, later
`LaggedStartMap(FadeOut, q_marks, shift=0.25 * DOWN, lag_ratio=0.1)`
(`_2025/grover/runtime.py:239-247`); a question as the right-hand side, `"= (What formula goes
here?)"`, then `wait()` (`_2023/convolutions2/dice.py:1041-1044`); dim the context, box the
target, ask "When is this 0?", hold, then `FadeTransformPieces(zero_question, eq_0)` turns the
question into the answer (`_2025/laplace/derivatives.py:1309-1338`). Big-O answer choices hide
under grey covers that wipe off with `lag_ratio=0.25`, followed by `self.wait(16)`
(`runtime.py:18-34, 96-103`). There is a literal "(Pause and ponder to taste)"
(`_2025/laplace/derivative_supplements.py:565-572`) [question marks 170 lines].
*Ours:* the script's `{pause}` after a question = a still screen with the question visible.
Turn the question into the answer, rather than fading one out and the other in.

### Repeated steps

**P24. Full detail for the first iterations, then faster, then cuts.**
```python
for n in range(6):
    ...
    if n > 2:
        self.skip_animations = True        # later words: only a 0.5 s glimpse
```
`_2024/transformers/chm.py:826-853`. Other forms:
- 120 predictions; after the first 11 the input animation is skipped (`quick=(n > 10)`,
  `generation.py:127-134`).
- Parity checks: one fully narrated (`_2020/hamming.py:2734-2800`), then four in a loop with a
  `wait()` each (`3146-3165`), binary counting at `run_time=0.5` per step (`3175-3183`), and
  finally plain `add`/`wait`/`remove` cuts (`3278-3283`).
- Plots at 0.5 s each for `n < 12`, then one frame each (`_2023/clt/main.py:3066-3079`).
- Flips at 0.5 s for `n < 2`, then 1/30 s (`_2025/grover/state_vectors.py:2649-2655`).
- One softmax column at `run_time=3` with staged `time_span`s, the rest at the default 1 s
  (`_2024/transformers/attention.py:919-947`).
*Ours:* trace `rev [1;2;3;4]` call 1 slowly with narration, call 2 at half the time, the rest as
quick cuts, then hold on the result.

## 3. Discrete data, sequences and step-by-step processes (the CS videos)

Closest to ours: transformers (`_2024/transformers/`), cross-entropy / compression
(`_2026/cross_entropy/`), Grover and its runtime (`_2025/grover/`), and older Wordle
(`_2022/wordle/scenes.py`), Hamming codes (`_2020/hamming.py`), Bitcoin (`_2017/crypto.py`),
Hanoi (`_2016/hanoi.py`). Pre-2021 files use the old API (`CONFIG`, `self.play(mob.method, arg)`).

**How he draws a sequence.** Elements are separate mobjects in a row, each with its own box.
Boxes share one height, have a faint fill and a stroke of the same hue:
`get_piece_rectangles(..., h_buff=0.05, v_buff=0.1, fill_opacity=0.15, stroke_width=1)`
(`_2024/transformers/embedding.py:53-90`). The text comes first, then the boxes
(`DrawBorderThenFill` per box, `lag_ratio=0.02`), then the words take their box's colour
(`embedding.py:138-158`). The "unknown next" slot is a yellow box with `???` under it. Bits are a
monospace `Text` with 0s and 1s in two greys (`_2026/cross_entropy/entropy.py:12-20`). A bit
grid stores *both* glyphs per cell and hides one, so a flip is an opacity swap
(`_2020/hamming.py:10-27`).

**Linked structures.** The nearest thing to cons cells in his repo is the blockchain: blocks in
a row with `buff=MED_SMALL_BUFF`, arrows with `tip_length=0.15` from each block's right edge to
the next one's left edge (`_2017/crypto.py:3256-3283`). The "prev hash" field of each block is
literally the previous block's digest moved into place, `ReplacementTransform(digests[i],
prev_hashes[i+1])` (`crypto.py:3087-3091`). Walking the chain is a red rectangle that is created
on a block, then moves onto the next field (`crypto.py:3116-3127`).

**One item → arrow → its value.** Each token block moves into place above its vector while the
vectors fade in (`LaggedStartMap(FadeIn, vectors, shift=0.5 * DOWN)`) and arrows grow between them
(`LaggedStartMap(GrowFromCenter, arrows)`), all in one play, then `wait()`
(`embedding.py:162-189`). Vector brackets take the colour of their token (`embedding.py:171`).

**Walking a sequence.** A cursor (here a vector) moves over item *n* while every other item fades
to 25% (GL `fade(0.75)` sets opacity 0.25, `manimgl/manimlib/mobject/mobject.py:1439-1440`), then a 2 s "work"
animation runs at that position (`_2024/transformers/chm.py:666-682`). This is the closest model
for tracing a recursive list function: an accumulator box riding above the current cell.

**Brute force as a scan whose length *is* the cost.** Cells of a 10×10 grid are dimmed one by
one at `run_time=self.wait_time_per_mob` (0.1 s) until the key (cell 42) is found; a 30×30
subclass uses 0.01 s (`_2025/grover/runtime.py:405-452, 464-470`). O(N) is felt as screen time.

**Growing a sequence.** The next-slot marker is a TEAL `Underline` at the end of the text
(`_2024/transformers/generation.py:166-172`). Appending is `FadeTransform` of the chosen item into
place plus moving the marker (`generation.py:335-345`). He then rebuilds the whole text mobject
and swaps it in, rather than editing the old one in place.

**Prefixes / call stack as rows.** All prefixes of a phrase are stacked as rows at 0.75 scale,
left-aligned, and each row is copied out of the row below in a 0.5 s linear step
(`_2024/transformers/attention.py:2110-2141`). Rows of an `f [1;2;3]`, `f [2;3]`, `f [3]`, `f []`
trace could be built the same way. The code tree in `entropy.py:250-268` grows each layer out of
a copy of the previous one (`TransformFromCopy(layer_copy, l2[0::2])`, then `l2[1::2]`,
`lag_ratio=0.5`, `run_time=1.5`, `wait(0.5)`).

**A process with fixed beats per step.** Arithmetic coding runs three plays per letter:
highlight the letter's interval, zoom into it, fade in the next layer while the camera shifts down
(`_2026/cross_entropy/arithmetic_coding.py:615-624`). Hanoi spells recursion out as text: "Move
4-tower" over a brace over "Move 3-tower, Move disk 3, Move 3-tower", with a nested brace below
(`_2016/hanoi.py:1438-1460`).

**Lists too long to show.** Show the head, `...`, then the true last few (`dots_index=-5`); in a
single column the dots turn vertical (`_2022/wordle/scenes.py:243-277`). The total appears as a
count label that counts up while the words appear (`scenes.py:1168-1173`). For a feel of sheer
size, pan the camera over the whole grid for 15 s (`scenes.py:1286-1292`).

**Filtering a list.** Rejected items turn red at half opacity immediately (`scenes.py:436-442`).
Then survivors slide from their old positions into a compact new list with
`LaggedStartMap(Restore, shown_words, run_time=1)` while the rejected ones shift left and fade
(`scenes.py:552-590`). That is `List.filter`, almost verbatim.

| Our idea | His precedent |
|---|---|
| `[3; 5; 9]` as boxes | token boxes `embedding.py:53-90`; bit grid `hamming.py:10-27` |
| cons cell → next cell | blockchain arrows `crypto.py:3256-3283` |
| head / tail labels | hopping brace `embedding.py:251-257`; `brace.get_text` `network_flow.py:786-799` |
| walking to the last element | cursor + fade `chm.py:666-682`; scan `runtime.py:405-452` |
| recursion / call trace | prefix rows `attention.py:2110-2141`; Hanoi braces `hanoi.py:1438-1460` |
| `x :: xs` builds a new list | append + rebuild `generation.py:335-345`; layer from copy `entropy.py:250-268` |
| `List.filter` | Wordle filtering `scenes.py:552-590` |
| O(n) vs O(n²) | growth curves `runtime.py:184-213`; cost as screen time `runtime.py:405-452` |
| a list of 10,000 | head … tail `scenes.py:243-277`; camera pan `scenes.py:1286-1292` |

## 4. What not to copy

- **Pi creatures.** `change`, `says`, `Blink`, `change_students`, `debubble` make up 11% of his
  plays, and 52 of 111 files touch `PiCreature`/`TeacherStudentsScene` (`custom/characters/`).
  They do the "student is confused" beat; we do that in the narration ("You might guess…").
- **His workflow.** `InteractiveScene` (100 of 111 files), `-se <line>`, `checkpoint_paste()`
  and `self.embed()` (`GRANT_CLAUDE.md.txt:17-19, 53-55`) are for live iteration in a GL window.
  So is toggling `self.skip_animations` to fast-forward loop iterations (`chm.py:834-850`,
  `generation.py:364-366`). In our pipeline you compress a loop with shorter `run_time`s or
  `self.add` cuts, and the cue system decides when.
- **Fixed waits as timing.** His `wait(3)` is a placeholder he cuts against the voice later.
  Ours must come from `c.wait_until(...)` (STYLE.md). Copy his *proportions*, never his numbers.
  Presenter-mode `wait(note=...)` holds (`_2024/puzzles/added_dimension.py:546-669`) are for live
  talks.
- **4K, 30 fps, boosted colour.** He renders 3840×2160 at 30 fps, black background, CMU Serif,
  and pipes the video through ffmpeg `eq=saturation=1.5` (`custom_config.yml:20-27`;
  `manimgl/manimlib/scene/scene_file_writer.py:230-232`). Frame units are the same as ours (8
  tall), so positions and font sizes transfer, but stroke widths like `set_backstroke(BLACK, 8)`
  are tuned for his saturated 4K output. Also, his `YELLOW` is `#FFFF00`
  (`manimgl/manimlib/default_config.yml:162`), while CE's is `#F7D96F` and ours is `#F4D345`.
  Don't chase his exact hues; our palette is fixed in `lib/style.py`.
- **3D camera choreography.** `frame.animate.reorient(...)` is the single most common `.animate`
  method (793 uses). It tilts a 3D scene. Our scenes are flat: at most a 2D pan or zoom with
  `MovingCameraScene`, and only when a structure is too big for the frame.
- **GL-only APIs** (translations in `GL_TO_CE.md` / `ce_ports.py`): `set_backstroke`,
  `FlashAround`/`FlashUnder`, `Text(…)["sub"]` / `Tex(…)["x"]` indexing,
  `TransformMatchingStrings`, `make_number_changeable`, `f_always`/`.always`, `time_span=`,
  `set_anim_args`, `CountInFrom`, `VFadeIn(ThenOut)`, `FullScreenFadeRectangle`, `get_grid`,
  tapered stroke widths. CE `ShowIncreasingSubsets` works by setting opacity, so it wipes any
  dimming or faint fill on the parts.
- **Variants and stills.** Many scenes are `…V2`/`…V3`/`Test` variants or stills with no
  `play` (199). Read the newest variant, not the first match.

## 5. Checklist for a scene agent

1. One visual change per narration beat, then stillness until the next cue (P1). About 8 words
   per beat; no more than two plays in a row without a hold.
2. Meaningful transforms 1.5–2 s, incidental fades 1 s, long "feel the length" sweeps 5–20 s
   linear. A beat is roughly 60% motion, 40% hold.
3. Show the whole shape first (skeleton of the trace, the full chain), then walk it (P2, P4).
4. New objects come out of the objects they were made from (`TransformFromCopy`, P5).
5. Emphasis: a flash that removes itself plus a colour change that stays (P6, P7), or a box that
   slides term to term (P8). Dim the rest to about 0.25 (P9). No `Indicate`.
6. Rewrite expressions line by line from copies (P11–P13). Box the part that changes (P12).
7. Every symbol keeps one colour for the whole chapter; boxes and labels take the colour of
   what they mark (P17).
8. Counters move *with* the things they count (P19). Make cost visible as screen time (§3) and
   as a number spelled out (P21).
9. Ask on screen, hold on the question, then turn the question into the answer (P23).
10. First iteration slow with narration, then faster, then cuts (P24). Clear the board in a
    lagged sweep that keeps what the next idea needs (P18).
