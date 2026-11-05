# Complex Roots and Logarithms: status

2026-11-01: project created; planning.

## Producer notes for chapter-directors
- Gemini quota low (2026-11-01, ~20% left for 2 days): ONE round of `vk review` per scene, no
  round 2; `vk listen --only` only for lines Whisper also flags.

## Chapter 1 · Roots of a complex number (director, 2026-11-01)
State: **ready for final** (2026-11-01). Preview: out/ch1_roots_preview.mp4, 9:27 (6 scenes, 26
clips, 8.8 min narration + end card). `vk preview 1`: handover ok s4 → s5 (0.00%); every other
scene ends empty; decodes clean end to end. `vk check`: dwell advisories only (accepted below).
- Narration: c1.hook.1 re-voiced (continuity review). Rewritten for the ear: c1.hook.3 "The
  lecturer began" → "The lecture opens" (Whisper small+medium heard "lecture"); c1.polar.2
  "Euler's" → "Oiler's" (COURSE.md rule); c1.ring.4 "to solve … angle arg W plus" → "every root of
  … its angle is the argument of W, plus" ("arg W" heard "rw"; "solve" per COURSE.md); c1.recap.3
  "To solve" → "To find every zed with" (COURSE.md). From the full Gemini listen: c1.polar.1 "arg for
  short" dropped (heard "arc"); c1.polar.4 "arg zed" → "the argument of zed" (heard "ard");
  c1.method.4 "a different root" → "a new root" (heard "differ", +qa; re-listened with `--only`:
  clean); c1.ring.1 "gives pi over ten" → "gives an angle of pi over ten" (heard "tan"); c1.recap.1
  "Examples Sheet One, question F fifteen" → "Question F fifteen, on the first examples sheet"
  (heard "Example"). From the scene reviews: c1.polar.4 "E to the two pi eye N" → "E to the two pi
  eye times N" (heard "two pie in"; the "eye N" rule from ch2); c1.unity.1 "Write zed as R" → "In
  polar form, zed is R" (heard "zedge"). The Gemini-only rewrites were not re-listened (quota
  note); `vk qa 1` is clean on all of them apart from a base-only flag on c1.polar.4.
- Accepted Whisper flags (spelling or number format): "first-year maths" → "math" (c1.hook.1),
  "Oiler's" → "Euler's" (c1.polar.2, intended), "defined" → "define(s)" (c1.polar.5, tense only),
  "round" → "around" (c1.unity.4), "five fifth roots" → "5 5th" (c1.ring.3 ×2), "F sixteen" →
  "Bustion F16" (c1.recap.2, small only; medium heard it right), "De Moivre's" (c1.recap.4,
  course-wide "de MOY-ver").
- Music (music/ch1.json): Serendipity under the hook, Fives under the ring picture (c1.ring.1:end →
  c1.ring.4), Gnomon under the recap proper and end card (c1.recap.2:end → END). ch2 used Euler's
  Clock, Orbit, Reflections.
- Argand helper: every ch1 scene uses ch2's `argand_plane(center, unit, extent)` from
  scenes/ch2_s2_theorem.py (ch2 was built first); the ring matches ch2's `ring_of_five()`
  (scenes/ch2_s1_hook.py). Reusable ch1 helpers: `polar_z()` (s2), `four_roots()`,
  `unity_pentagon()` (s3), `ring_circle()`, `ghost_ticks()`, `condensed_steps()`, `handover_shot()`
  (s4).
- Scenes: all 6 built by Claude scene-builders (s1–s4 in parallel, then s5 on s4's handover and the
  recap); one Gemini review round each, one fix round on s2–s6 (s1 needed none). Fixed: s2 z₁/z₂
  arrows FG with YELLOW arcs (were BLUE/PINK, which mean real/imaginary parts), "proved in §6.3" and
  the exp line no longer crowd; s5 r = 2^{1/5} label clears at {pentagon} (it sat on the pentagon's
  edge), margin note "This [is] the fundamental theorem…" (verbatim note lacks "is"); s6 "roots of
  unity" tag FG (was GREEN), F16 pieces fade together, "Full solutions: Part 8" raised off the edge,
  (a) reads "π + 2πn".
- Gemini claims checked on frames and found false or by design: s1 x = 2 dot stays on the Re axis
  (builder's choice, keeps the real answer visible), six "?" (brief: "a few"), the dimmed plane
  behind the names columns (brief), "box 8 cut off" (seven tiles, all inside); s2 doubled "y"
  (copy sits on the label before it flies), arrow "detached" from z (the brief's sweep), TEAL arc
  short of the tip (an angle arc at radius 1); s3 arrow below the axis, missing pentagon edge, stray
  45° arc (all mid-move frames); s4 θ line colliding with the tags (0.7 apart throughout); s5 "only
  two red crosses" (the brief's two ghosts); s6 "2i on the ring" (step 2's text in the next panel).
- Accepted dwell advisories (each cleared by the beat the brief asks for, 0.1–1.4 s short): s1 part
  line (8.5 s opening clip); s2 exp line; s3 4θ = 2πm, n = 5; s4 closing caption; s5 "principal
  argument", n = 0 … k−1, "Lecture 11".
- Accepted departures: s3 uses n = 8 for the generic ring; s6's end card shows the "Next" shot only
  (the half-size recap grid fell to ~15 pt text, so it clears first); s6 (b)'s tag reads "roots of
  unity", not "s3".
- Glitches (for the glitch study):
  - s5 c1.ring.4 ~71 s: "= −7π/10", "= −3π/10", "principal argument" and table rows 3–5 still fading
    while `z^k = w` faded in. Cause: one `sweep_clear(..., run_time=2.0)` with the incoming formulas
    starting at half time, and the sweep's lag clears the lower rows last. Fixed: a 1.0 s clear with
    nothing incoming, then `appear`.
  - s6 c1.recap.1 ~17 s: a "cursor bar" after z⁴ = 1. Cause: the edge of a `FlashAround` ring caught
    mid-flash. Fixed: `FlashUnder`.
  - s6 end of c1.recap.2 ~45 s: F16's circles and labels lingered after the rest (staggered clear).
    Fixed: one fade.
- Finalize "look" (ch1_transitions.json), checked on frames of out/ch1_roots.mp4, both false, no
  fix: s2 @ 159 s chapter time "open circle at −1 labelled π". Frames 159.0, 161.0, 166.5: on the plane, −1 is a
  filled GREEN dot labelled π (its principal argument, per the brief). The open circle is the θ
  line's −π end below the plane, labelled −π, with π filled. s2 @ 134 s "sweep starts from the
  real axis". Frames 133–137 and 134.2–135.2 every 0.2 s: the arrow leaves from z's angle θ, and the
  TEAL arc starts at θ. Frames 143.4–144.4 every 0.2 s: the fast backward turns land back on z, with
  no pop.
- Open: none for the final.

## Chapter 2 · De Moivre's theorem (director, 2026-11-01)
State: **ready for final** (2026-11-01). Preview: out/ch2_de_moivre_preview.mp4, 9:52 (7 scenes,
25 clips, 9.4 min narration + end card). `vk preview 2`: handover ok s4 → s5 (0.00%), no other
handovers (every other scene ends empty). `vk check`: only dwell advisories, accepted as below.
- Narration: c2.int.2 re-voiced (continuity review's "halve" change). Rewritten for the ear:
  c2.thm.2 "Put the two ends together" → "Set the first expression equal to the last" (Whisper
  small+medium heard "two N's together"); c2.thm.4 "keeps the modulus at one" → "equal to one"
  (Gemini, high confidence, heard "of one"; not re-listened, per the quota note). From the scene
  reviews: c2.int.1 "E to the eye N theta" → "E to the eye times N theta" (heard "in theta");
  c2.expo.1 "Euler's" → "Oiler's" (heard "Yooler's"; COURSE.md's fallback; Whisper small and
  medium now write "Euler's"). Not re-listened (quota); `vk qa 2` clean on both.
- Accepted Whisper flags (spelling only; Gemini's full listen heard none of them): "De Moivre's"
  (c2.thm.2, c2.recap.1: "Demovers'", "DeMoyver's"), "labour"/"labor" (c2.thm.4), "eye sine" →
  "i-sign" (c2.expo.2 ×2, the sine/sign homophone), "Oiler's" → "Euler's" (c2.expo.1).
- Accepted pronunciations (Gemini scene reviews): the voice says "de MOY-ver" for De Moivre (s1,
  s2, s7; a common anglicised form, consistent in every line; a respelling would touch every L10
  chapter, so it is the producer's call); "conjugate" as "CON-joo-gate" (c2.thm.5); "two theta"
  heard "to theta" (homophone).
- Music (music/ch2.json): Euler's Clock under the hook, Orbit under s6's turning arrows
  (c2.expo.2:end → recap), Reflections under the recap and end card.
- No ch1 Argand helper existed when ch2 was built, so each ch2 scene draws its own plane to
  PLAN.md's spec (s1 has `argand_plane()` and `ring_of_five()`).
  ch1's director may want to match ch2's look (s2's `argand_plane()`: origin (−3.3, −0.2), unit 1.9).
- Scenes: all 7 built by Claude scene-builders; one Gemini review round each, one fix round on
  s2–s7 (s1 needed none). Fixed: s2 highlight now includes the exponent n, "1×1×1×1 = 1" fades
  when the modulus-r arrow arrives, r⁴ label 1.9 → 3.5 s; s3 "n = ½ ?" and the half-angle tags clear
  before n = 3, the TEAL winding arrow is shown landing on the GOLD 3θ arrow; s4 dial steps on its
  words, theorem box no longer duplicates the first line; s5 and s7 margin tags "Re:"/"Im:" (read as
  "Re cos 4θ" before); s6 PURPLE arrow appears as a clear mirror at −130°; s7 margins and spacing.
- Gemini claims checked on frames and found false: s2 base arrow not scaled to r (mid-zoom frame);
  s4 "(i sin θ)³ over cos θ" (~34 s, not reproduced); s6 "sin θ on the imaginary axis" (it was the
  PINK 2i sin θ dot); s7 duplicate caption at 24 s (not present). Gemini's s2 "first = last order"
  (box reads last = first) and s5's Im-above-Re order accepted: equality is symmetric; margin tags.
- Accepted dwell advisories: s1 title card (5 s, fixed by the narration), the DIM compound-angle
  pile (meant as a crowd, not read), 5 × π/10 = π/2; s2 lone "=", r⁴ label, (r e^{iθ})ⁿ line; s3
  "one point", 3θ + 6π, Part 5 card; s4 theorem box (cleared on purpose); s5 tags and handwritten
  endings; s6 −e^{−iθ} label, sin θ; s7 r5 panel (cleared at {next} per the brief). Each is cleared
  by the next beat the brief asks for.
- Glitches (for the glitch study):
  - s3 c2.int.4 ~73 s: a faint second "full turns" under the label. Cause: `appear` drops labels in
    from 0.25 above, so the tag faded in through the equation line. Fixed: fade in place.
  - s4 c2.exp.4 ~79.5 s: the copy dropping into the collected line ran ~1.6 units past the left
    edge. Cause: `derive()` aligns the copy on the longest shared glyph run. Fixed: straight drop +
    `edit()`. Same pass: `_FlyCopy` sat on its source line (slow ease start; eased t³ instead).
  - s4 c2.exp.1 ~16 s: the equation shown twice (flown line + theorem box). Cause: `fly()` leaves
    its source on screen. Fixed: box fades once the line is out.
  - s6 c2.expo.3 ~70 s: dashes and the 2cos θ label stayed while the arrow reset (cleared in the
    same play). Fixed: clear first, then move. Not a morph jumble.
  - Builders of s4 and s5 report that `fly()`/`derive()` (engine/lib/moves.py) show a full-opacity
    copy over the source at close row spacing or over long distances; both scenes work around it
    locally (constant-speed fly, a scene-local `Merge`).
- Open: none for the final. Producer's call: De Moivre as "de MOY-ver" (see above).

## Chapter 3 · Powers and sums with exponentials (director, 2026-11-01)
**State: ready for final.** Preview `out/ch3_trig_sums_preview.mp4`, 10.5 min (631.8 s; narration
9.7 min over 29 lines). 8/8 scenes built (Opus builders), one fix round. `vk check`: dwell advisories
only. Handover s5 → s6 ok (0.00%); every other scene ends empty.
- Music (`music/ch3.json`): Focal Point under the hook (START → c3.cube.1), Fractals under s3's
  curling chain (c3.sum.3:end → c3.geo.1), Quantum Blue under the recap and end card
  (c3.recap.1:end → END, swell after c3.recap.2).
- Shared helpers (imported via load_scene): `toolbox()` in s1 (s2, s5, s6); chain helpers in s3
  (s6, s7, s8); `geo_formula()`/`lam_flag()` in s4 (s5–s8); `mirror_pairs()` in s2 (s7, s8);
  `conj_step()` in s5 (s8); `boxed_result()`/`straight_chain()` in s6 (s8).
- Narration rewritten for the ear (all re-voiced, `vk qa 3` after):
  c3.try.1 re-voiced for the continuity review, and "Examples Sheet One" → "the first examples
  sheet" (COURSE.md). c3.conj.1, c3.conj.5 "E to the eye N theta" → "E to the eye times N theta"
  (COURSE.md). c3.conj.5 "Multiplying adds the angles" (Whisper: "multiplying at z angles") →
  "When you multiply, the angles add"; its {done} "Four exponentials on top" → "Four terms on top"
  (Gemini review: the 1 isn't an exponential). c3.res.3 "Take three terms" (Whisper small+medium:
  "three turns") → "Take N equal to three". c3.res.5 "You'll want that" → "That comes up"
  (COURSE.md). The arg / "two pi eye N" rule touches no ch3 line ("two pi M" has no "eye").
- Gemini listen (one full run, after the rewrites): 0 findings. No `--only` re-listen.
- Accepted Whisper flags: c3.cube.3 "placed tip" → "place tip" (same meaning); c3.res.5 "sines" →
  "signs" ×2 (COURSE.md homophone); base-only "sign of" / "Des Moevers'" in c3.try.1.
- Accepted Gemini-review pronunciation claims (each Gemini-only, and Gemini's full listen of the
  same audio heard them right; not re-listened, quota): c3.cube.4 "left" → "let", c3.conj.3 "minus
  eye theta" → "minus ay theta", c3.res.4 "theta" → "data", c3.res.5 "free" → "freep",
  c3.recap.1 "lambda" → "landa", c3.try.1 "De Moivre" (COURSE.md keeps "de MOY-ver").
- Accepted review/check items: s4 geo.2 (Gemini: "divide" while the factored line shows): the
  factored line is the step before dividing, and the formula flashes on {divide}. s3's DIM unit
  half-circle (Gemini "stray arc"): it belongs to the plane. s6's parked PINK sine row: by design,
  it rises in res.5 (inside the 0.5 margin). Dwell advisories: s2 `¼ + ¾ = 1` 6.1/6.6 s; s3 tags;
  s5 the `1`/`+1` merge and `|1 − e^{iθ}|²` 5.1/5.6 s; s6 the ½ step 3.7/7.2 s, the N = 3 check
  8.7/10.6 s; s7 the F-tags, hint (i) cleared for hint (ii), "ratio r e^{iθ}" 3.1/6.3 s; s8 r5's
  items when the panels clear on "exponential". s2 flashbox advice (not blocking).
- Glitches (confirmed with `--frames`, all fixed):
  - s1 ~40 s: the e^{iθ} badges' BG fill is see-through mid-fade, so the card border showed
    through; then FlashAround drew a straight line along the badge's top. Badge moved above the
    corner, flash along its outline.
  - s2 ~43 s: the YELLOW pairing arc drawn with Create: its first frames are a short stroke on the
    exponent 3 of e^{3iθ}, read as "the red ring jumps". Now FadeIn, raised.
  - s2 ~85 s: `appear(..., shift=0.5*DOWN)` faded the integral term in from 0.5 higher, a faint
    copy between the box and its row. Shift 0.2.
  - s3 ~42 s: `appear()`'s default drop started the `×e^{iθ}` labels inside their hop arcs.
  - s5 ~5.5 s: the FlashAround ring on `a` took in `λ` too. Now one underline flash per symbol.
  - s6 ~81–97 s: `LaggedStart(GrowArrow(a) for a in chain0)` adds each arrow to the scene;
    `self.remove(chain0)` removed only the group, leaving a frozen curled chain above the straight
    one. Fixed with `self.remove(chain0, *chain0)`.
  - s7 ~28.5 s and ~48.7 s: `edit()` of the title "F12" → "F13" kept the shared "F1" and faded the
    old digit before the new one: a half tag "F1". The tag is now its own Text, swapped whole.
  - s7 ~48 s: `sweep_clear`'s lagged FadeOut left items faint on an empty board. Fades at once.
  - s7 ~62 s: the old short brace stayed under the growing `1 + ω + … + ω^{n−1}`, then none, before
    the new one grew. Now rebuilt per frame with the edit.
  - s8 ~8.5 s: the r1 caption's `appear()` drop overlapped the r1 grid mid-fade (read as a
    duplicate). s8 ~9.5 s: r2's unit semicircle stuck out of its cropped grid.
  - Not confirmed: s1 "2ℓ" in (78) (a faint i mid-fade), s1 q2 formula before its card, s3
    "missing length-1 shadow", s7 "−5" in the sin⁵θ bracket, s6/s8 bottom margins (≥ 0.57).
- Builders of s2, s4, s5 again report `fly()`/`derive()` flagged as text overlapping its source at
  close row spacing; they used flash-then-appear-in-place or a scene-local Slide instead.
- Open: none.

## Continuity review (2026-11-01, ch1–8 scripts)
Narration is 12,750 words, ~80 min (ch1 9.2, ch2 9.6, ch3 10.1, ch4 9.9, ch5 11.2, ch6 9.1,
ch7 8.6, ch8 11.9). Each is within +10% of PLAN.md, ~5 min over its ~75 in all. Coverage matches
PLAN.md. The "last time" / "next time" chain holds. ch4's last line says i^i is real, and ch5's
hook builds on it and holds back the value until s4. No ids, marks or stems were changed.
- Changed narration (8 clips): c1.hook.1 ("Part One A maths" puts A before a word and collides
  with "part one"), c2.int.2 ("halve"), c3.try.1 (F12's "part one / part two" became sub-parts
  named by content, and "De Moivre with the power three", because N is ch3's number of terms),
  c4.prin.5 ("in the last part" could be heard as the previous video), c8.f13.5 ("R E to the …",
  and "R to the sixth cosine six theta" read as one exponent), c8.f16.5 (turns counted with M, not
  K, since K is ch1's power), c8.f18.1 and c8.f18.5 ("eye R E to the eye theta").
- Kept, as L11 did for its voiced lines: un-numbered "this chapter" (c2.thm.5, c5.hook.2,
  c6.hook.2), "all chapter" (c6.ex.5) and "last chapter" (c7.circuit.2, c7.amp.3, c7.parts.3).
  No number, so they can't be misread, and they were being voiced. Every numbered reference is
  "part N". Also kept: "Why lowest terms?" (c5.fin.4: the question word, as in L11); "part H",
  "part D" (c7.imp.5: letters, not Part numbers); "two B zed to the N" (c8.f16.1, .2, with the card
  on screen) and "two pi eye N zed two" (c5.recap.1).
- Letters: ch1 writes the power as k, so n counts turns. ch2 says aloud that n is the power. ch3
  counts turns with m (N terms), and so does ch8's F16 (the sheet's n is the power). ch4 and ch5
  keep n for turns. ch6 and ch8 have no n. Neither ch7 nor ch8 puts capital I next to i.
- Briefs (no re-voicing): TEAL is only full turns. ch3 s6's N brace is now GOLD (a length). PINK is
  only i and imaginary parts. ch8 s3's general b and s are white, turning BLUE/PINK only at b = 1,
  s = i. ch7 s4's callback to ch6's pair recolours into ch7's colours (position PINK, velocity GOLD),
  so GOLD is only the current there. ch7's white e^{iωt} is stated in s3. ch8 F19 keeps ch6's GOLD
  arrow (an oscillation, no current). F19's letters: ch6 s6 writes |A| e^{i arg A}, and ch8 s7 maps
  the sheet's A e^{iϕ} once (its A = 25, its ϕ = 3t − δ), never a bare "A = 25". ch6 s6 and ch8 s7
  now colour b BLUE. ch8's spoiler banner is YELLOW. ch8 s3 and s8 now use m for turns.
- Recaps: all eight bring back their own scene visuals with a line under each, including ch8 s8
  (five panels from s3–s7, then the two threads). Each ends with an ~8 s end card.
- PLAN.md updated to match: colours (TEAL incl. 2π/ω, ch6/ch7 exceptions), letters,
  cross-references, ch1 s5's recipe in k, ch8's m and δ. COURSE.md: lines added, nothing rewritten.

## Chapter 6 · Oscillations and the complex amplitude (ch6_oscillations)
State: **ready for final** (director 2026-11-01). Preview out/ch6_oscillations_preview.mp4, 9.1 min
(547 s); 6/6 scenes built, one review round + one fix round (s2–s6); `vk preview 6` handover ok.
- Music: music/ch6.json: Heartbeat under the hook, Serendipity under s3's arrow.1 (c6.pend.3:end →
  c6.arrow.2), Ongoing from c6.try.2:end under the recap and end card (swell after c6.recap.1).
  Euler's Clock and Orbit were dropped because ch2 uses them.
- Build order: s3 first (owns the shared helpers in scenes/ch6_s3_phasor.py: pendulum,
  inset_pendulum, argand_plane, phasor_arrow, shadow, x_graph, Clock; load_scene("ch6_s3_phasor")),
  then s1, s2, s4, s5, then s6. Handover s3 → s4 only (0.00% diff). There's no s1 → s2 handover
  (a fade), although the brief says "hold the pendulum". Running example: A = 2e^{−iπ/3},
  one turn = one swing = 4 s on screen, pendulum ±20°. s4 subclasses s3's Clock as PClock, because
  Clock drifted ~2.7 s.
  Colour choices: s4's acceleration arrow and ẍ = −ω²x are FG (white): TEAL is only full turns, and
  PLAN names no colour. s6's teaser arrows use ch7's colours (I GOLD, V_R BLUE, V_C PINK, V white).
- Narration rewritten (re-voiced, QA clean): c6.deriv.4 "which you'll meet next term" (Whisper: "I'll")
  → "and the course comes back to it next term"; c6.try.1 "from Examples Sheet One, question F
  nineteen" (Gemini: "Example") → "Here's a question to try. It's F nineteen, on the first examples
  sheet." Gemini-only, so it wasn't re-listened (producer's quota note).
- Accepted QA flag: c6.ex.5 "sines" → "signs" (homophone, base+small).
- Accepted check flags: dwell advisories only (~79), mostly labels that leave on the next cue and the
  ωt counter's digits. No sync, layout, overrun or transition flags.
- Gemini scene review (one round), each claim checked on frames:
  - Real, fixed: s2 wave only drawn after "smooth wave"; s3 stray inset x(t) label (~46 s); s3 TEAL
    box flicker (~127 s); s4 "still" tag and "acceleration" label left in place as the arrows resumed;
    s5 start picture not shown at {half}; s6 r4 "2c" (now |A| = 2c).
  - False: s2 pendulum freeze; s3 "only a highlighted"; s4 frozen right-angle mark; s5 anti-phase
    pendulum.
  - Accepted: s1 strip lingering in the corner (the brief); s1's end fade (pendulum last, as asked);
    s5 ex.2 "no arrows shown" (the brief has no plane there).
- From the holds, fixed: s3 ωt spiral coil and the arrow.5 label pile-up; s5 −ωβ and "real part"
  were PINK (now BLUE).
- Glitches (for the glitch study):
  - s3 ~127 s and the {swing} beat: a box round the inset pendulum flickers.
    Cause: `FlashAround(inset)` with the box crossing the frame's top edge; replaced by a flash
    along the bob's path.
  - s3 ~55 s: the ωt arc reads as a tight coil of ~5 rings.
    Cause: a spiral arc that keeps every turn with small radial growth; now 1.5 turns, older ones fade.
  - s4 ~91 s: a fading "acceleration" label sits over the PURPLE arrow.
    Cause: `disappear(acc)` bundled with `FlashAround(law)` while the clock restarted.
  - s4 ~69 s: "still" stays up after the motion resumes.
    Cause: its `disappear` was bundled with a later flash.
  - s5 ~93.5 s: the brace and the √3cω tick stay in the arrows' path.
    Cause: nothing removed them before {compare}'s FadeOut.
- Open: holds tiles c6.pend.2 and c6.arrow.1 are `~` (motion through the clip end); builders confirmed
  those end frames on --frames. The recap's caption dwell is short (4.9/6.2 s) by design.
- (producer, 2026-11-01) ch1's director: match ch2's Argand plane look (`argand_plane()` in
  scenes/ch2_s2_theorem.py); ch2's music uses Euler's Clock, Orbit, Reflections: ch1/ch3 pick others.
- (producer) Engine issue reported by ch2's s4/s5 builders: `fly()`/`derive()` in engine/lib/moves.py
  briefly show a full copy over the source; worked around locally. FIXED in the library 2026-11-01 (DE session: _clear_alpha both axes, cap 0.9; end frames unchanged), so new scenes use fly()/derive() as normal.

## Chapter 4 · The complex logarithm (ch4_logarithm)
State: ready for final (director 2026-11-01). Preview out/ch4_logarithm_preview.mp4, 9.8 min
(narration 9.1 min); 7/7 scenes, one fix round, no handovers (every scene fades to empty).
- Music: music/ch4.json (Transformation under the hook, Quaternions under s3's wrap
  c4.map.2–map.3, Clarity under the recap with the end card).
- Build: s1–s6 in parallel, then s7 (recap). No handovers (each scene fades to empty). s4 owns
  "the ladder" (module-level `ladder()` in ch4_s4_ln2i.py; ch5 s5 should copy its look: GOLD dashed
  line at Re w = ln 2, TEAL rungs r ~0.08, GREEN n = 0 rung tagged "principal value", fading ends,
  TEAL brace "2πi"). Built: `ladder(origin=W_O, sx=W_SX, sy=W_SY, ns=(-2,-1,0,1,2), n_fade=3,
  fade_step=0.28, y_lo=-3.6, y_hi=3.5)` returns a VGroup with .line .ln2 .pi2 .dots{n} .tag
  .fade_top .fade_bot .brace .brace_label .point(n); w-plane 2.0 units per Re w, 0.2 per Im w
  (grid at Im w = ±5, ±10, ±15); helpers `w_plane()`, `z_plane()` beside it.
  s5 introduces the faint GREEN strip −π < Im w ≤ π. Argand plane: ch1 isn't
  built, so every scene copies `argand_plane()`'s look from ch2_s1_hook.py.
- Narration rewritten for the ear (before builds): c4.hook.2 "Which complex numbers W solve E to
  the W …" → "make E to the W equal to two eye" (COURSE.md: avoid "solve"); c4.prin.4 "holds for
  whole ladders" → "for the full sets of values" (Whisper ×3 heard "whole letters"). c4.prin.5
  re-voiced for the continuity review's change.
- Accepted Whisper flags (spelling / no change of meaning): c4.recap.1 "zed's" → "z's";
  c4.map.3 "goes round" → "goes around"; c4.prin.1 "this strip" → "the strip"; c4.prin.2
  "lecturer's" → "lecture's" (base, small only).
- Gemini listen (one full run): two Gemini-only, high-confidence findings, rewritten and re-voiced,
  not re-listened (quota note): c4.cons.4 "the log two you know" (heard "lod") → "the familiar log
  of two"; c4.prin.1 "gather principal values in a box" (heard "bops") → "give principal values a
  box of their own". `vk qa 4` clean on both. From the s2 scene review (Gemini, high): c4.def.1
  "W is log zed if …" (heard "wog zed") → "W is the log of zed if …"; `vk qa 4` clean, not
  re-listened.
- Scene reviews (one round, s1–s7), accepted: s1 the reversed hook arrow keeps its "e^w" label
  (the brief: we run e^w backwards; ln isn't defined yet); s1 screen "≈ 0.693" vs spoken "zero
  point six nine" (brief); s6 c4.prin.4's GREEN principal arc drawn as a spiral with an open end
  at −π (intended: −π excluded); s6 "ex plus eye, why" phrasing (low); s7 the five captions stay
  through "Next time" (they become the end card's list, by design).
- Glitches (Gemini scene reviews, confirmed on frames by the builders; all fixed):
  - s3 ~21 s: the GOLD line → circle `ReplacementTransform` bent the line into a curly-bracket
    shape mid-morph. Now a flash up the line, then the circle drawn from 2 (no morph).
  - s3 ~32 s: the sliding line passed over the "l" of the "ln 2" tick ("n 2"). The label now
    fades during the slide.
  - s3 ~60 s: `GrowArrow` arrows caught mid-grow, aimed at ladder dots not yet shown ("stray arrow
    into empty space"). Dots now appear first.
  - s3 ~69 s: an arcing copy of the ℝ line in flight read as a duplicate BLUE segment. Now a flash
    along ℝ while the ray draws out.
  - s4 ~8 s: `FlashAround` on the single glyph "2" made a ring over "= … e" ("circles 2e"). Now
    `FlashUnder`.
  - Not confirmed (mid-move frames, correct): s2 ~77 s θ arrow "pointing down" (mid-sweep), s2
    ~90 s stray text, s3 ~46 s dot "stationary", s4 ~23 s ghost text (a fade-in), s4 ~77 s end
    fade, s5 ~33 s stray dot (the 3 + 4i copy sliding down a rung).
- Fix round (holds + reviews): s1 title card now held ≥ 4.3 s (silent 2.6 s lead-in); s2 e^{iv}
  arrow GOLD (was BLUE); s3 reversed arrow "ln z" (was "log z"), "infinitely many w → one z";
  s5 strip edges (π solid, −π dashed), z label off the ladder line, column labels inside the
  margin; s6 takeaway lines held ≥ 6 s, (e) flash on the expression, longer end hold; s7 flash
  under "?", bottom row lifted, r5 shrunk.
- Accepted `vk check` flags: dwell advisories only (18), each ≤ ~2.5 s short, e.g. s1's card lines
  4.3 s of 6.1–6.7, s1 quote 6.3 of 9.1, s6's "π" label (replaced by "2π" on purpose), s7 r5's
  "−2π"/"0" (1.5 s before the end card clears the panels; the voice moves on).
- Open: none. Gemini still flags nothing unhandled (listen: 2 findings rewritten; reviews: above).
- Finalize "look" (transitions, s5 @ 10.1 s = 5:46.0, "duplicate red ln e^z = z below-left"): not
  real. Frames of out/ch4_logarithm.mp4 at 5:42.0–5:43.1 (15 fps), 5:45.3–5:47.6 (10 fps),
  5:45.8–5:46.9 (15 fps, full frame), 5:47.0–5:49.2 (5 fps) show one copy: it fades in with a small
  rise at 5:42.4–5:43.0, and the strike draws left to right from 5:46.5 (its start shows as a red
  tick left of "ln"). No fix; still ready for final.

## Chapter 5 · Complex powers (ch5_powers)
State: ready for final (director 2026-11-01). Preview out/ch5_powers_preview.mp4, 10.9 min (654 s),
8/8 scenes; handovers s5→s6 and s6→s7 match (0.00%). Narration 10.3 min, 29 lines.
- Music: music/ch5.json (Hypothesis under the hook, Spirals under s7's filling circle
  c5.inf.1–inf.2, Far Away under recap.2 and the end card).
- Build order: s3 (owns the 2^i ray + log strip) and s5 (owns the ladder, question card, gallery
  frames; hands over to s6) first; then s1, s2, s4, s6 (s6 hands over to s7); then s7; then s8.
  Ladder: s5's `ladder()` (used by s1, s2, s5) now wraps ch4_s4_ln2i.py's `ladder()` (producer,
  2026-11-01) so the look matches ch4. Music checked against ch2/ch4/ch6: no shared tracks.
- Narration rewritten for the ear (before builds): c5.fin.5 "and solving zed to the fifth equals
  two eye, are the same job" → "is the same job as finding every fifth root of two eye" (COURSE.md:
  avoid "solve"), and "plus two pi N over five" → "plus one fifth of two pi N" (Gemini + Whisper ×3
  heard "pi and over", +qa); c5.two.1 "Euler's" → "Oiler's" (Gemini heard "orlers"; ch2's fix);
  c5.two.2 "roughly 0.77, plus 0.64 eye" → "Its real part is about …, and its imaginary part about
  …" (Gemini heard "pus"); c5.recap.1 "Let's recap" → "Time for a recap" (Gemini heard "Must" at
  0.0 s), and "E to the two pi eye N zed two" → "E to the power, two pi eye N times zed two" (the
  retake was heard "i and z too", Whisper medium; now count.3's wording). Not re-listened (quota).
- Accepted Whisper flags (Gemini's full listen heard them as written): "ladder" → "latter"
  (c5.count.2, flap-t homophone, the ladder on screen); "lecturer" → "lecture" (c5.ii.4,
  c5.count.2); "asked" → "asks" (c5.fin.1); "De Moivre's" spelling (c5.fin.2); "Oiler's" →
  "Euler's" (c5.two.1, the intended word).

## Chapter 7 · Impedance (ch7_impedance)
State: ready for final (director 2026-11-01). Preview out/ch7_impedance_preview.mp4, 8.9 min (531 s);
6/6 scenes built; `vk check` clean bar dwell advisories; handovers s1→s2 and s4→s5 ok (0.00%).
- Music: music/ch7.json (Machinery under the hook, Resonance under s5's triangle (imp.3–imp.4),
  Endpoint under the recap with the end card). None of ch6's tracks.
- Build order: wave 1 s1 (owns `circuit()`; hands over to s2) and s5 (owns `amp_plane()`,
  `amp_arrows()` in the 3–4–5 shape, and `opening_shot()` with s4's two results, which s4 ends on
  as its handover into s5); wave 2 s2 (opens on s1's handover), s3, s4; wave 3 s6. Joins s2→s3 and
  s3→s4 are fades (topic changes), so s3 and s4 fade their small circuit, laws and rules back in.
- Gemini listen (one full run): one Gemini-only, high-confidence finding: c7.hook.1 "impedance" →
  "impenence". Rewritten "This is part seven, on impedance." → "This is part seven, and it's about
  impedance." and re-voiced; `vk qa 7` clean. Not re-listened (quota note).
- c5.inf.4 "the values wind along a spiral" → "trace out a spiral" (scene review: the voice said
  "wind" as in breeze; a heteronym Whisper can't flag). `vk qa 5` clean on it.
- Producer's voice rule (from ch1): "two pi eye N" → "two pi eye times N" in c5.two.3 (×2),
  c5.count.2, c5.count.3, c5.recap.1; re-voiced, `vk qa 5` adds no new flags; s3, s5, s8
  re-rendered on the new audio. No narration line says "arg".
- Accepted review pronunciation flags: "theta" → "fay-tuh" (s5, Gemini only; the full listen and
  Whisper heard it); "De Moivre" as "de MOY-ver" (s6, the producer's call in ch2).
- Glitches (scene reviews, round 1; confirmed by the builders on frames unless marked):
  - s2 ~50.3 s (c5.def.3): a faint 0.3-scale ladder over "w ln z", then sliding left. Cause:
    `FadeIn(lad, target_position=lnz, scale=0.3)` starts a shrunken ghost on the text. Fixed: TEAL
    streak from below ln z + ladder fading in at its own place.
  - s2 ~73 s (c5.def.4): a broken rectangle flickering into the dot. Cause: FlashAround hugging
    the single glyph z^w. Fixed: colour pulse.
  - s4 ~16–21 s (c5.ii.1): Gemini read "−i". Cause: the PINK i label's halo cut the unit circle,
    leaving a stroke that read as a minus. Not a transition. Fixed: label raised clear.
  - s4 ~76 s (c5.ii.4): the quote faded in over the strip still on screen. Cause: the quote's
    FadeIn carried its own timing inside the clearing play. Fixed: lag to the second half.
  - s5 ~55.5 s (c5.count.4): the TEAL factor's exponent shown twice. Cause: `fly()` copy rising
    straight up through its own source. Fixed: curved path through empty space.
  - s5 ~58.4 s (c5.count.4 {depends}): the ring meant for z₂ also covered n. Cause: FlashAround
    on a tiny glyph (padding). Fixed: FlashUnder.
  - Not confirmed: s1 11 s brace spanning two rungs, s1 13 s "2³" ghost (the normal fade-in start),
    s3 55–57 s stray "+ 2" (12 frames clean; Gemini may have seen an older render).
- Review round 1 (Gemini one round per scene; holds): s1 clean. Fix passes on s2–s5: s3 now
  imports s2's `four_laws()` (dQ/dt was inline in s3, a fraction in s2); I₀ drawn at 2 units and on
  top in s3/s4/s5 (it was a stub hidden under V_R0); s3's left column tightened and amp.4's two
  labels moved off the axes. Gemini claims checked on frames and accepted: s2 0 s "V = ? · I"
  flicker (s1's handover clearing); s4 ~63 s "purple ahead of orange" (ch6's pair before its
  recolour, as briefed); s4 ~78 s "no calculus left" too dim (already YELLOW: stale render); s5
  ~68 s arrows "detach" (frames show a rigid turn about the origin).
- Glitches (confirmed on frames, fixed):
  - s2 ~47 s, c7.circuit.3 {ohm}: two overlapping YELLOW rings; separate FlashAround on the
    adjacent glyphs R and I. Now one FlashAround round "RI".
  - s3 ~77 s, amp.4 → amp.5: grid and axes gone while the arrow and labels floated; a lagged board
    clear removed the plane first. Now one even fade.
  - s4 ~56 s, c7.parts.3 {quarter}: the ×i step read backwards (GOLD into PINK); a full GOLD arrow
    faded in on top of PINK and then turned away. Now a PINK copy turns a quarter anticlockwise and
    becomes GOLD.
  - s5 ~25 s, c7.imp.2 {clear}: the highlight on the i also took in the ω; FlashAround's box round a
    narrow glyph overreached. Now FlashUnder on the i.
  - s5 ~88 s, c7.imp.5: grid, axes and unit circle vanished in ~0.2 s ahead of the rest; lagged
    board clear. Now one 0.8 s fade.
- s6 recap (Gemini one round, frames checked, no fix needed): "2πn" read as "2τn" (a 480p
  misread; the glyph is π at full size); GOLD-row cards "linger" at ~43 s (a lagged clear that
  ends before "Lecture 11" arrives); "De Moivre" heard "de MOY-ver" (accepted reading, COURSE.md).
  Thumbnails for ch1 s5, ch3 s3, ch4 s4, ch5 s7 and ch6 s3 are simplified stand-ins drawn in
  ch7_s6_recap.py (ch1/ch3 weren't built; ch4–ch6 were in fix passes), so they won't track later
  changes to those scenes. Panel r1 uses s3's `law_lines()` (s2's `four_laws()` shrank below the
  minimum text size).
- Accepted (by design): s1's circuit keeps ch6's drawing, with the current arrow on the bottom
  wire, not the top wire as the brief says; s1's {last} shows ch6's pair in ch6's colours (GOLD/PURPLE),
  and s4 recolours it on screen; s2→s3 and s3→s4 are fades (topic changes). Dwell advisories left
  in every scene (labels cleared on their next beat).
- Open: none. Engine note from s4's builder: check's flash-box audit (engine/tools/transitions.py
  ~l.274) crashes on a ValueTracker left in the scene (worked around by removing trackers).
  - s7 ~76–81 s (c5.inf.4): the 2^i ray diagram half-faded behind the spiral going into frame 4.
    Cause: only the text lines were cleared when the spiral arrived; the ray faded later, at
    {gallery}. Fixed: the ray clears with the text.
  - Not confirmed (round 1): s6 89 s exponent "on the baseline" (LaTeX correct; a plain fade-in),
    s6 70 s circle vanishing early (it holds through the clip), s8 44–45 s frozen BLUE dot and
    changing shadow (one dot, rebuilt each frame; the arrow lies flat near 45.5 s).
- Round 2 (holds): s6 frame 2 got its "(2i)^{1/5}" label (frames 1, 3, 4 had theirs) and
  "e^{2πinm} = 1" lost a stray gap (the "?" it replaces had TeX's tight spacing); s7 re-rendered
  on the new handover. s3 re-cued to the re-voiced "two pi eye times N".
- Accepted check flags: dwell only. s2 "2³ = 8" 4.1/4.1 s, s4 "exponentiate" 5.0/5.0 s, s5
  "θ = θ + 2πn"/"same habit" 0.3–0.5 s short (cleared on "Multiply"), s6 "?" and "how many?"
  (question cards the answer replaces on its cue), s6 "n = 0, …, q − 1" and "2 values, not 4"
  (≤ 0.2 s short), s7 five (the spoken words say the same; "values a factor e^{2π} ≈ 535 apart"
  3.3 s and "different for different n" 3.8 s give way to the spiral / the ∞ line). s6's flashbox
  advice on the "1" (non-blocking).
- Accepted review notes: s3 "awkward pause" in "two pi eye N" (low; the line has since been
  re-voiced); s4 two "n = 1" labels (two different strips); s5 dim fourth frame (low; holds fine);
  s7 caption "imaginary part: ∞" (s7 shortened all four captions to fit, by design); s8 w vs z₂
  in r4 (the general case uses z₂, as the script says).
- Gemini budget: one full listen, one `vk review` per scene (8), no re-listen (no rewritten line
  stayed Whisper-flagged).
- Open: none for the final. The end card is the recap's list + ch6's turning arrow and shadow under
  "Next time" (ch4's layout).

## Chapter 8 · Solutions to the examples (ch8_solutions)
State: **ready for final** (director 2026-11-01). Preview out/ch8_solutions_preview.mp4, 12.0 min
(721.6 s; 34 clips, 11.3 min narration + end card), decodes clean. 8/8 scenes built by Claude
scene-builders; one Gemini review round each, one fix round (s2–s8; s1 had a re-voice pass).
`vk preview 8`: handover ok s1 → s2 (0.00%); every other scene ends empty.
Build: s1 first (owns `card_row()`, `question_card()`, `pause_icon()`, `ritual_steps()`,
`handover_shot()` in scenes/ch8_s1_intro.py), then s2–s7 in parallel (each opens with its card out
of the row; s3–s7 expose `recap_panel()` / `recap_pascal()` / `recap_triangle()`), then s8.
- Narration: re-voiced the continuity review's four changes (c8.f13.5, c8.f16.5, c8.f18.1,
  c8.f18.5). Rewritten for the ear: c8.f13.2 "E to the eye N theta" → "E to the eye times N theta"
  (Whisper ×3 heard "i and theta"; ch2's fix); c8.f19.1 "ex equals seven, plus twenty-four cosine
  of three T, plus seven sine of three T" → "… plus twenty-four times the cosine of three T, plus
  seven times the sine of three T" (Gemini-only, high: "plus" heard "prost"; not re-listened, per
  the quota note). `vk qa 8` clean on both.
- Accepted Whisper flags (spelling, number format or homophone): "F fifteen" → "F-15" (c8.f15.1);
  degrees as digits (c8.f15.3, c8.f16.5); "chords" → "cords" (c8.f16.5); "De Moivre's" spelling
  (c8.duo.4, course-wide); "signs" → "sines" (c8.duo.5, COURSE.md's sines/signs homophone); "two
  eyes" → "two i's" (c8.f13.3); base-only "Pause and try it" repeated (c8.f19.1, a base
  hallucination; small and medium heard it once).
- Gemini listen: one full run, one finding (c8.f19.1 above).
- Music (music/ch8.json): Zeta under the hook (START → c8.f15.1), Stepwise under s5's arrow
  picture (c8.f13.3:end → c8.f13.5), The 3Blue1Brown Experience under the recap and end card
  (c8.f19.5:end → END, swell after c8.end.2). None used by ch1–ch7.
- Voice rules pass (producer, Gemini nearly off): c8.intro.1 "solves the seven questions on
  Examples Sheet One" → "works through the seven questions on the first examples sheet";
  c8.intro.2 "pause, solve it, then compare" → "pause, work it out, then compare" (COURSE.md: avoid
  "solve", "Examples Sheet One"); s1's ritual step "solve" → "work it out" to match. `vk qa 8`
  clean on both. No "arg", "you'll", "Euler" or "two pi eye N" in ch8.
- Scene reviews (Gemini, one round each, s1–s8; s8's after its build). Accepted: De Moivre as
  "de MOY-ver" (s1, s4, s8; course-wide); s1 "works" → "warps" (medium confidence, Whisper heard
  "works"); s1 tags staying lit after their group (the brief: they light cumulatively); s3
  "chords" → "cords" (+qa: Whisper ×3 agrees, but a true homophone, chords on screen; same call
  as sines/signs); s3 "two point one seven" → "point seventeen" (low); s5 the DIM "(78)" (the
  brief's equation number); s7 "(81)" (ch6's equation number from the notes).
- Claims checked on frames by the builders and found false: s2 (d) label sign (it reads
  (−√3 − i)/2); s4 ~67 s duplicate sin 3θ (the boxed line is a different equation); s5 "1,53"
  comma (no comma; a grid line crossed the label, now backed); s5 arrows "grow" on "shrink"
  (they shrank, but late: now a separate shrink on the word); s6 (d)/(e) equations over
  (c)/(d) (they take turns, never both visible), s6 (e) header late (it changes on {e}); s7 old
  equations lingering at 52 s, duplicate |24 − 7i| at 56 s, note over the grid at 78 s, wave
  starting at 32 (it starts at 31, peaks at 32 at t = δ/3).
- Fixed in round 1 (reviews + holds): s2 (d)'s lower labels moved clear of plane (c); s3 the
  "b − s" label sat across its own diagonal, now upright beside it; s4 F17's card now held through
  the pause (it cleared on "try it"), F12's tiny shrunk card body replaced by an "F12" header; s5
  the "θ = 2πm" note clears at {c}; s6 the rule's box grew through "ln"; s7 the "from the origin"
  underline drops in with its tag, and the plane's grid sheared while shrinking (builder found).
- Glitches (for the glitch study):
  - s3 ~57 s, c8.f16.3 {para}: the YELLOW b − s diagonal ran through its own label. Cause: the
    label rotated along the diagonal came out steep, across the line. Fixed: upright, offset.
  - s6 ~26 s, c8.f18.2: a small YELLOW box cut through "ln". Cause: the rule's box grew outward
    from the formula's centre (Create). Fixed: `FadeIn(rect, scale=1.04)` at full size.
  - s7 ~78 s, c8.f19.4: the plane's grid turned into slanted, sheared lines as the plane shrank
    left. Cause: a transform between two planes of different extents. Fixed: old grid fades out,
    new plane fades in, the arrow and shadow move across.
  - s7 ~105 s, c8.f19.5: the RED underline looked like a stray pink line. Cause: it grew in
    place while its tag dropped in from above. Fixed: they drop in together.
  - s5 ~62 s: "≈ 1.53" read "1,53". Cause: a grid line and the unit circle through the label at
    480p. Fixed: dark backing, larger label.
  - s8 ~26.4 s, c8.end.2 {threads}: a "stray box fragment" beside the De Moivre panel. Cause: the
    GOLD thread line drawn with `Create` from the left while its frames faded in. Fixed: lines
    fade in with their frames.
  - s8 ~35.4 s, c8.end.2 {end}: a "cursor bar" after cosh x. Cause: the edge of a `FlashAround`
    ring mid-flash (as in ch1 s6). Fixed: `FlashUnder`.
- s8 also: "Next: Lecture 11" now lands on "Lecture eleven" (was ~1 s late); the rows clear on
  "Next time". Departures accepted: recap panels in two rows (five in one row were unreadable),
  r1 without s3's angle formulas, r3's chain without its plane; the end card keeps the two thread
  names on the left (ch4 s7's layout).
- Accepted `vk check` flags: dwell advisories (the inherited card row cleared at each scene's
  start, ~1 s by the brief; s1's title card before {warn}; s4's F12 card, now cleared on "i";
  s5's "θ = 2πm" note, cleared at {c} as asked; s6's rule 9.3/12.2 s; others ≤ ~2 s short, each
  cleared by its brief's next beat) and s8's small text inside the recap panels (10–22 pt: the
  brief's small panels are for recognition; the captions carry the meaning).
- Open: none for the final. Gemini still flags only accepted items (De Moivre, chords/cords).
- Finalize "look" (2026-11-01): neither s3 finding is on out/ch5_powers.mp4 (s3 starts at 120.68 s).
  "y wraps alone" @ 4.8 s: s3 0.3–6.5 s (10 frames), "x + iy." is one line throughout. "Formula
  scrambles" @ 53.3 s: s3 52.9–56.4 s (12 frames), the line is static until ~54.7 s, then fades out
  whole and 2^i = e^{i(ln 2 + 2πin)} fades in whole; no doubled glyphs. No fix; still ready for final.
- (producer, 2026-11-01 evening) Gemini is about to run out (engine/logs/gemini-off): when
  `vk review`/`vk listen` say "skipped", follow chapter-director.md "When Gemini is off" (Whisper
  `vk qa` is the ear; COURSE.md voice rules on every line before building; `vk check` + holds;
  `--frames` sheets). `vk finalize` then renders + checks format/handovers only: "clean" = done.
- (producer, 2026-11-01 ~16:40) ch8 final `out/ch8_solutions.mp4` 12:02.8, handovers ok; finalize said
  "look" only because its Gemini transitions review failed (agy "invalid model selection" on part 1,
  twice; part 2 ok). Accepted as done: every scene had its one review round, and Gemini quota is
  nearly gone. When the quota resets, `vk finalize 8` (with review) can re-check it.

- 2026-11-04 Gemini pass (checks only, nothing fixed): ch8 ear check ran: only c8.f13.2:1 'N' heard 'and' (Gemini-only claim).
