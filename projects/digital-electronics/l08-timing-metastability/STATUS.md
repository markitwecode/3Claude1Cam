# Timing, Metastability and Parallelism: status

2026-10-31: project created; planning.

## Chapter 1 · How fast can the clock tick? (ch1_setup)
- State (2026-10-31): **done.** out/ch1_setup.mp4, 1920×1080 60 fps, 9:53.8 (narration
  9.2 min). All 8 scenes built by Opus scene-builders, two review rounds plus one post-final
  transitions fix round (s2, s6, s7).
- Open (low, not acted on): the final review notes that "the slide calls this a generic path"
  (c1.path.3) has no on-screen "generic path" label. The hook's count shows "1" only ~0.3 s
  between the quickly spoken "zero, one" (2 and 3 are fine; Gemini's "skips 2" was false).
- Music (music/ch1.json): Quaternions under the hook, Occlusion under c1.path.3 (the counter
  mapped onto the path), Focal Point under the recap and end card.
- **Lecture-wide drawings (ch2–ch7 copy these; each sits between `# ===` rulers in its file):**
  - *Dimension arrow:* ch1_s5_datasheet.py `dim_arrow` + `grow_dim(arr)` (thin DoubleArrow,
    stroke 3, tips ~0.15, label in the interval's colour, DIM guides stroke 1.5). Use `grow_dim`,
    not GrowFromCenter (that squeezes both tips into a lone arrowhead). s2 and s3 have
    same-spec copies.
  - *Data-sheet diagram:* ch1_s5_datasheet.py `clock_wave` (sloped edges, 0.35 wide), `bus`
    (two lines with X crossovers), `hatch` (run of X's), `guide`, `sweep_in` (pen-sweep draw; no
    dot artefacts). The p. 105 diagram: rows CLK 2.1 / Q0 0.4 / D1 −1.3, traces x −4.6..6.3,
    rising edges x −2.8 and 4.2, Q0's X at −1.6; the exact calls are at the end of s5's construct
    (ch1_s6_setup.py redraws it).
  - *Window diagram (square style, p. 104):* ch1_s3_ffnumbers.py `WindowDiagram(origin, k, fs,
    words)` with `d_change(x)` (RED dashed change) and `q_unknown()` (RED "???"); full size at
    origin (0, 0.3), k 1 (edge x 0, band x −1.3..1.0); small at (−2.6, 0.3), k 0.6. L6's
    master-slave and door helpers are copied in the same file.
  - *The path:* ch1_s4_path.py `path_diagram()`: L6 `make_ff()` boxes at (±4.4, 0.5), CL box
    3.4 × 1.6 at (0, 1.1), CLK bus y −1.8 from x −5.6; each clock branch is its own part
    (`.clk_br0`, `.clk_br1`) for ch3's CLK0/CLK1, `.clk_paths()` for pulses. Also `box_flash`
    (flash along a box's own outline) and `fly_outline` (outline copy flight without skew).
  - *Budget bar (canonical):* ch1_s6_setup.py `budget_bar(segs, total, x0=-3.3, y=0.0,
    tc_tex="T_c", syms=True, nums=None, sym_size=40, num_size=34)`; segs = [(tex, colour,
    length)], height 0.5, fill 0.85, YELLOW outline stroke 3 on top; segments may overrun the
    outline (a broken budget). ch1_s7_marketing.py has `pcs_bar(...)` (adds `padlock()`s) and
    `one_ns_bar(unit=7.5, left=-3.3, y=0.8)`, the 1 ns bar with the 0.7 ns slot.
  - *Clock + period:* ch1_s2_clock.py `clock_with_period(periods=5, i=1)` (L6 `clock_wave` with
    the T_c arrow).
  - *Counter:* ch1_s1_hook.py `hook_counter()` (L6 `sync_counter()`/`led_chain`/`clock_source`
    at scale 0.86, bottom y −3.4), readout Mono GREEN bits + GOLD decimal, trail T 42 (wrong
    values RED). Title card styling: ch1_s1_hook.py.
- **Narration rewrites (all re-voiced; `vk listen --only` clean afterwards):**
  - c1.hook.1 "In lecture six, we built this" → "Back in lecture six, we designed this" (Whisper
    heard "build").
  - c1.clock.2 "A processor at one gigahertz" → "A processor running at one gigahertz" (Gemini
    heard "yigahertz").
  - c1.window.2 "here a one." → "Here, that value is one." (+qa: the "a" was dropped);
    "You don't calculate these three times." → "You never calculate these three numbers."
    (Gemini review heard "ties").
  - c1.path.1 "Flip-flop zero launches the data, and flip-flop one receives it." → two
    sentences (Gemini review heard "fwit flop").
- **Accepted voice flags:** c1.clock.2:1 "one hertz" → "1 Hz" and c1.window.3:4 "Dee's" →
  "D's" (format/spelling only). Gemini scene reviews later heard "foot flop" (c1.path.1),
  "fup-flops" (c1.window.1) and "cock-to-Q" (c1.setup.2); `vk listen --only` on those three
  clips found nothing, so accepted as Gemini variance.
- **Accepted check flags:** c1.path.3 small text (24–25 in the counter, CL label 20): the brief
  puts the shrunken path and the counter on screen together. Dwell advisories left where the
  narration's cue spacing sets them (title card 5 s before {counter}; the hook's blurring
  frequency tags on purpose; s2's closing question; "Part 4"; recap panel lines).
- **Departures worth knowing:** s3's caveat tag reads "simplified picture" and appears with the
  master-slave pair; s4's self-loop tag reads "launches and receives" (beside the counter's
  FF0), not "FF0 = FF1"; s6 has no "part 7" tag; the recap's r6 bar shows only "0.7 ns" (no
  symbols), as in s7's compare shot.
- **Glitches** (scene, time, what, cause; all fixed):
  - s1 ~52 s (hook.3 chips): a flash box drawn tight round each chip body cut across its pins
    and read as a stray RED line. Cause: flash rectangle hugging the body, not the pins.
  - s2 ~8.8 s (clock.1 > repeat): the T_c copies slid out together in one `.animate.shift` and
    overlapped mid-move into one long arrow. Fixed: each fades in at its own period, lagged.
  - s2 ~44 s (clock.3 > step): new GOLD dots faded in while `ReplacementTransform` was still
    compressing the wave, so they sat under moving edges. Fixed: fade out, compress, then
    add in three phases.
  - s5 ~42 s: `Create` of the clock showed its round line cap as a dot in the first frames;
    ~49 s: `sweep_in` lines too short read as two dots; ~54 s: `GrowFromCenter` on a
    DoubleArrow squeezed both tips into a lone PINK arrowhead. Fixed with `sweep_in` (hidden
    under 0.15 long) and `grow_dim`.
  - s4 ~39 s (path.2 > deadline): `FlashAround(ff1.box)` traced an offset partial bracket over
    the output pins. Fixed with `box_flash`.
  - s4 ~65 s (path.3 > map): three `MoveToTarget` outline copies flew at once through the CLK
    label and each other; `path_arc` skewed them into parallelograms. Fixed with `fly_outline`,
    one at a time.
  - s7 ~70 s (market.4 > grow): two touching rectangles moved with `.animate.move_to` left a
    seam, and one covered the GOLD segment. Fixed: one `Transform`, the other under it.
  - Not reproduced: s4 ~45 s stray YELLOW wire segment.
  - Final-video transitions pass (confirmed with ffmpeg frames, fixed, re-finalled):
    s2 ~45 s (clock.3 > step): `ReplacementTransform` between square waves of 8 and 11 periods
    went through jagged, irregular shapes; now redrawn from a ValueTracker on the period count
    (`square_wave_line`). s6 ~32 s (setup.2 > bar): the bar outline transformed from the T_c
    DoubleArrow swept a skewed yellow polyline with arrow tips across Q0/D1; now
    `GrowFromEdge(outline, LEFT)` after a flash of the arrow. s7 ~68 s (market.4 > grow): the
    fading "0.7 ns" label was half covered by the rising segment ("der ns"); labels now fade
    out before the move.
  - Accepted: s1 ~48 s, the RED flash border traced round the metastability chip briefly
    overshoots it (a passing-flash border, mid-draw).

## Chapter 2 · Hold time (ch2_hold)
- State (2026-10-31): DONE. `out/ch2_hold.mp4`, 7:47 (466.7 s, 1920×1080, 60 fps); narration
  7.1 min, 21 lines; 6/6 scenes built (Claude scene-builders: s1–s3, then s4, s5, s6 in sequence,
  since s4 opens on s3's end shot and s5 on s4's). Music `music/ch2.json` (hook Serendipity, s3
  shift-register stretch Stepwise, recap Orbit). Review: Gemini per-scene review + holds, one fix
  pass per scene (s4 two), then final viewer + transitions reviews; one confirmed fix (s4 caption
  overlap), re-finalled, not re-reviewed by Gemini.
- Shared drawings (ch3+ can copy them): ch2_s2_hold.py `hold_diagram(hatch0, k, shift)` (ch1_s5/s6
  geometry; hatch0 0.4 good, 0.2 violating; `.band`, `.thold`, `.d1`, `.d1_lab`); ch2_s3_shiftreg.py
  `build_chain()`, `digit()` (three-FF shift register); ch2_s4_noclockfix.py `routes_path()`,
  `routes(pin)` (the path with its CL opened into a long and a short route, FG buffers);
  ch2_s5_contamination.py `hold_budget(x0, y, L, hold, su, lo, hi)` (budget bar with the GOLD
  hold fence, set-up deadline and BLUE "D1 may change" stretch; `.fence .deadline .stretch` for
  ch3's skew).
- Accepted departures: ch2's budget bar (s1, s5, s6) adds an unlabelled YELLOW T_c arrow 0.35
  under ch1_s6's bar, which ch2's brief stretches on {slower}; s1's hook tokens are dots with
  small "old"/"new" tags (the D1 wire is short); s2's diagram is 0.8 of ch1's size so the ghost row
  and inequality fit; s3's boxes are L6's sketch style (D/Q, no Q̄), unlike the path's make_ff;
  s6 tile 1 drops the old/new tags at tile scale; end card "Part 3 · Clock skew" styled as ch1's
  "Part 2 · Hold time". Dwell advisories left: s1 title card 3.2 s (check wants ~6), s1 "new"
  token and "too soon?", s3/s4/s5 tags cleared by the brief's next beat.
- Rewritten lines: c2.hold.3:1 "after the hold time has run out" → "after the hold time ends"
  (Whisper heard "time is run"); c2.hook.1:5 "For set-up, slowing down always works" → "So when
  set-up fails, slowing down always works" (Gemini heard "It preset up"); c2.noclock.4:4 "by
  Harris and Harris" → "by David and Sarah Harris" (Gemini heard "Harrison Harris"). Both
  re-listened clean. c2.hook.1:5 again after the s1 review (Gemini heard "slowing downed", then
  "a slower clock" as "a slower quack"): now "So when set-up fails, a longer clock period always
  fixes it.", re-listened clean. c2.recap.1 after the s6 review (Gemini heard "clock-to-cue" as
  "cock-to-Q", twice across takes, then "launches" as "wauches"): now "One edge captures the old
  data and sends out new data, …", "The fastest way through, from the edge to the first change at
  dee one, must take at least the hold time." and "…the flip-flop's own shortest delay, from the
  edge to its output, has to cover it." Re-listened clean; Whisper's "at dee one" → "of D1" is
  spelling only, accepted.
- Accepted QA flags: c2.hook.2:2 and c2.hold.3:1 "the hold time" → "the whole time" (Whisper
  base/small/medium; Gemini's full-chapter listen hears "hold" in both); c2.shift.1:5
  "left-hand neighbour" → "left hand neighbor" (spelling only).
- Glitches (ch2, confirmed by the builder on frames, all fixed):
  - s2 ~43 s (c2.hold.2 {d1}): the new short PURPLE t_pd arrow drawn on the same row as ch1's
    dimmed long t_pd arrow, two arrows overlapping (both left on screen). Now the old one fades out.
  - s2 ~60 s (c2.hold.3 {bad}): the ghost D1 row slid in under the brace and its
    "(t_pc + t_pd)_min" label (layout, not motion). Now the brace leaves first.
  - s3 ~10.8 s (c2.shift.1 {clk}): FF2's clock stub drawn before the CLK bus reached it, so the
    wire seemed to meet the box's corner (Create order). Now bus first, then stubs.
  - s3 ~54 s and ~62 s (c2.shift.3): pictures cleared piece by piece (separate FadeOuts), leaving
    labels, digits and dots floating. Now one FadeOut per picture.
  - s3 ~73 s (c2.shift.4 {rule}): editing (t_pc + t_pd)_min to (t_pc)_min left a gap before the
    closing parenthesis mid-move (transform between unlike MathTex). Now t_pd fades while the rest
    slides left.
  - s4 ~21–22 s (c2.noclock.2 {hold}): the YELLOW highlight box jumped between terms and at one
    point framed only ")_min" (box transformed between unlike-sized targets). Now one linear widening sweep.
  - s4 ~70 s (c2.noclock.4 {moved}): the RED overlap block shrank towards the band's right edge
    and stayed beside the GREEN tick, and the GOLD band seemed to stretch (whole D1 wave morphed by
    Transform). Now one play slides the hatch start and shrinks the RED block to nothing.
  - s5 ~58 s (c2.range.3 → .4): the T_c double arrow's tips sat full-size at the centre while
    `GrowFromCenter` grew its line (Manim keeps arrow tips at full size), shown before {bar}; the
    bar outline showed as a stray YELLOW stub in its zero-width start state during the board clear.
    Now the arrow fades in, and the clear and the bar's growth are separate plays.
  - s5 ~60 s (c2.range.4): the GOLD hold fence and set-up deadline showed as dots at the start of
    `GrowFromCenter`. Now they fade in whole. (Gemini's ~43 s "stray text" was not on the frames.)
  - s6 ~35 s (c2.recap.2 → .3 {next}): tiles faded out one after another, so tile 4's line was
    left alone on screen (staggered FadeOut). Now all tiles fade together.
  - s6 ~41 s (c2.recap.3 {late}): the skew pulse flashed at the CLK fork without visibly
    travelling to the flip-flops. Now one dot per branch, FF0 reached first and FF1 later.
  - Final reviews (viewer + transitions, out/ch2_hold.mp4), checked on 1080p frames:
    - s4 ~47.5 s (c2.noclock.4 {rare}): the p.106 caption's third line overlapped the diagram's
      T_c label and arrow (caption placed in the gap between the inequalities and the raised
      diagram). Confirmed; fix pass sent, re-finalled.
    - s3 end → s4 start (~94 s / 04:04): picture dips to near-black and comes back, both passes
      flag it. Cause: the end-on-empty-frame rule plus s4 reopening on s3's end shot (FadeOut,
      then FadeIn of the same picture). Accepted as the convention's cost; s4 → s5 does the same.
    - Accepted as brief or as brief crossfades: s1 ~23.5 s mini budget bar in the corner (the
      brief puts it there); s2 ~2.5 s a thin vertical line beside "CLK" mid-flash (highlight in
      progress); s2 ~45.5 s brace grows from a flat line (GrowFromCenter on a Brace); s3 ~0.2 s
      and ~3.2 s FF1 and its label dim while fading in (staggered fade-in); s3 ~34 s SIPO brace
      spans Q_1–Q_2 mid-growth, all three when settled; s4 ~15.4 s the old GREEN tick fading
      during the clear; s4 ~21.4 s highlight covering "(t_pc" first (the intended widening
      sweep); s6 ~12.3 s the "1" in FF0 (tile 3's content).

## Chapter 3 · Clock skew (ch3_skew)
- State (2026-10-31): **done.** out/ch3_skew.mp4, 1920×1080 60 fps, 8:16.4 (narration 7.6 min,
  21 lines). 7 scenes built by Opus scene-builders (s1+s3, then s2+s4+s5, then s6, then the
  recap); two review rounds plus one post-final transitions fix round (s3, s4, s5, s6), then
  re-finalled. Gemini's final viewer pass: 0 findings. ch2 scene files rechecked before the final
  (none changed after 14:46); s1 now uses ch2_s4's stacked inequality layout.
- Music (music/ch3.json): Euler's Clock under the hook, Machinery under c3.other.2 (the
  shift-register race), Clarity under recap.2 and the end card.
- **Narration rewrites (re-voiced; `vk listen --only` clean but for one low finding):**
  - c3.skew.2:2 "Suppose the clock signal comes in from the right, so its wire…" → "Suppose the
    signal comes in from the right, so the wire…" (Gemini heard "quack").
  - c3.other.2:4 "The bit has jumped two places on one edge." → "So the bit has gone two places
    on a single edge." (heard "jumps").
  - c3.recap.1:2 "takes time to travel, so" → "takes time to travel along the wires, so" (heard
    "traveled"); c3.recap.1:4 "When the receiving flip-flop's clock is ahead, the skew joins the
    clock period's budget, as a fourth piece." → "When the receiving flip-flop gets its edge
    early, the skew becomes a fourth piece of the period's budget." (heard "quack").
- **Accepted voice flags:** c3.less.2:5 "one and a half centimetres" → "1.5 cm" (format);
  c3.less.2:4 "Now add a" → "Now, at a" (Whisper small+medium; Gemini's full listen didn't hear
  it); c3.other.2:4 "a single edge" → "the single edge" (Gemini, low); c3.hold.2 "the" → "thef"
  (Gemini scene review; `listen --only` clean); c3.hold.4 "so" → "su" (low).
- **Accepted check flags:** dwell advisories where cue spacing sets them: s1 title card (clears on
  {path}), "same instant", the closing "?"; s2 tag "first: CLK1 ahead" 2.0 s and the end-shot
  lettering (s3 reopens on it); s5 p. 109 quote 3.7 s, "easier" 4.3 s; s6 digit swaps, s5's skew
  labels leaving at {slide}, the {nofix} rule 3.5 s; s7 r6 tags and line (4.4 s sentence). s5
  flashbox advice on the bracket's box flash (a bracket has no overbar problem).
- **Departures worth knowing:** s1's corner path has no lettering, and the returning inequalities
  have no tags; s2's "clock skew" stays as a small heading until the t_skew arrow; s3's strip
  lettering is faded (CLK0/CLK1 kept at 30), and at {rule} the bar's symbols fly (the segments
  stay); s4 {eats}: TEAL collapses (a no-skew moment), then pushes back in; s5 writes the set-up
  rule with (t_pc + t_pd)_max; s6 {nofix} shows the skewed hold rule (no T_c in it); s7 r6 opens
  already slid left (only the slide right animates); end card "Part 4 · Metastability and the
  synchroniser" at T 40.
- **Helpers later chapters can copy:** ch3_s1_hook.py `clock_board()` (board, 12 flip-flops,
  clock tree, tick axis); ch3_s3_skewsetup.py `split_path()` (CLK0/CLK1 branches from a source
  ring at the right, CLK1 at opacity 0.55) and `skew_traces()` (p. 108's four rows);
  ch3_s6_otherway.py `skew_fences(skew)` (ch2's fence bar at any ±skew; s5's copy is + only).
- **Glitches** (scene, time, what, cause; all fixed unless noted):
  - s1 ~23 s: "same instant" still faint after the path shrank into the corner. Cause: its FadeOut
    spanned the 1.6 s shrink while the other labels left in 0.8 s.
  - s2 ~26 s: "clock skew" and its brace still on screen under the fading chip (staggered clear).
  - s2 ~64–66 s: traces vanished, then the path snapped to full size with lettering half faded
    (separate fades plus a state restore). Now one play.
  - s2 ~46 s: CLK0's edge drawn before CLK1's mid-sweep. Cause: each trace swept by segment
    count, not x. Now one vertical front across both.
  - s3 ~57 s: the bar outline as a collapsed yellow stub (GrowFromEdge from zero width). Now
    grows from 20% width.
  - s3 ~72 s: t_su doubled as its fly copy left a fully visible source. Now the source dips.
  - s4 ~7 s: the rearrangement passed through a garbled state (≥, t_pd, + faded in place, the new
    line ghosted over the old). Cause: `edit()` not keying the MathTex pieces. Now keyed moves.
  - s4 ~60 s: stray gold line above "909 MHz" (FlashAround caught part-way). Now FlashUnder.
  - s5 ~38.5 s: a big white circle below the traces. Cause: FlashAround(Brace) rings a brace as
    if it were one glyph. Now a box flash.
  - s5 ~77 s, ~79 s, ~71 s: t_su and TEAL segments and the hatched stretch grew from a centre
    point (dot/small square). Cause: grow animations scaling height. Now widen at full height.
  - s5 ~50 s: t_pd landed before its "+" existed and read as a loose piece. Now "+" first.
  - s6 ~75 s: a thin green bar above the wire (FlashAround on a flat wire), then a green oval
    (stroke-12 tapered passing flash). Now a wire-width passing flash.
  - s6 ~16 s: t_skew flew to the frame's top edge (path_arc −0.8π). Now −0.35π.
  - s6 ~28 s: CLK0/CLK1 labels squeezed against the clock bus (layout). Now below the bus.
  - Not reproduced on frames: s1 ~32 s box lighting early, ~37 s dim hold rule (mid-fade); s3
    ~38 s duplicate CLK1 edge, ~56 s CLK1 jump; s4 ~13 s gap in the bar (the intended no-skew
    beat); s5 ~82 s TEAL line; s7 r2 CLK1 order, ~38 s panel ghosts, ~47 s early "???", ~49 s torn
    title (fade-ins).
  - Accepted: s3 ~58.5 s a small pink shape as the t_pc arrow turns into its segment (reads as
    the arrow travelling).
- Open (low): the transitions pass was not re-run after the last fix round (each fix was
  frame-checked by its builder). s7's r2 panel shows CLK1's lead as only ~0.25 units, at 0.55
  opacity.

## Chapter 4 · Metastability and the synchroniser (ch4_metastability)
- State (2026-10-31): final rendered, `out/ch4_metastability.mp4`, 9:07 (547.3 s, 1920×1080,
  60 fps); narration 24/24 voiced, 8.5 min. Music `music/ch4.json` (hook Hypothesis, s3 ball
  stretch Gnomon over ball.2–ball.3, recap Far Away with the swell). 7/7 scenes by Opus
  scene-builders in dependency order (s1 + s3; s2 + s5; s4 + s6; recap), Gemini review per scene
  + holds, two fix rounds (s2, s4, s6 two each; s5, s7 one; s1, s3 none).
- Shared drawings (ch5+ can copy them; each between `# ===` rulers):
  - ch4_s1_hook.py `push_button(center)`, `fingertip()`, `button_ff()` (make_ff ×0.85 at
    (0.6, 0.95), button at x −4.0 on the D row; `.btn.plunger` moves by PUSH 0.18).
  - ch4_s2_undefined.py `undefined_diagram()` (rows 1.0/−0.3/−1.6, edge x −0.6, traces −5..3,
    Q's RED halfway level, "???") and `volt_axis()` (x 4.3, y −3.4..0.2, GREEN valid / RED
    invalid bands).
  - ch4_s3_ball.py `hill()`, `ball()`, `place()`, `timer()` (`.point(u)`, valleys u = ±1,
    summit u = 0), plus L6's `rs_latch()` copy.
  - ch4_s4_model.py `model_formula(size)` (P(t_res > t) = T₀/T_c e^(−t/τ), parts addressable).
  - ch4_s5_synchroniser.py `decay_graph()`, `sync_circuit()`, `sync_timing()` (boxes y 2.244,
    FF0 x −1.7, FF1 x 2.1, ×0.62; rows CLK 0 / D1 −0.95 / Q −1.95, rising edges −2.4 / 2.6,
    traces end x 4.2). ch5's hook can open from these.
  - ch4_s6_fail.py `res_bar()` (t_res FG + t_su GOLD = T_c), `pfail_formula()` (boxed YELLOW),
    `fail_condition()`.
- Departures worth knowing: s3's ball race uses five stacked mini-hills (the true distances
  would overlap on one hill); s5's shift-register ghost sits below the circuit, not behind;
  s4's key point sits as a 3-line block in the graph's upper right; s6's "slower" sits right of
  the T_c label; the recap's tiles clear (not dim) before the synchroniser stream.
- Accepted check flags: dwell advisories only (s1 title/quote/road, s2 corner pin labels and
  "Metastability" 5.0 s, s4 tallies/τ tag/derivation note, s5 opening lines and ghost labels,
  s6 old-bar segments and the formula rewritten into P_fail, s7 P_fail 7.6 s): each is set by
  the brief's cue spacing or a deliberate brief flash.
- Glitches (scene, time, what, cause; confirmed on frames by the builders, all fixed):
  - s2 ~52 s (c4.undef.3 {confused}): the lower fan-out gate's wire dropped past the Q̄ pin, so
    it read as wired from Q̄ (layout). Now a junction dot on Q's wire 0.45 right of the pins.
  - s2 ~53 s: after the t_su/t_hold arrows faded, the window guides stuck out ~0.3 above the
    band as stray vertical stubs (arrows faded, guides left full height). Guides now shrink to
    the band in the same play. (Gemini's "window jumps left" was not real.)
  - s4 ~34 s (c4.model.2 {afford}): a GOLD flash ring round the lone exponent t crossed the
    minus and slash, reading as a broken exponent. Ring removed; t just recolours.
  - s4 ~46 s (c4.model.3): the T_c DoubleArrow grown from centre showed its two tips alone in
    empty space (GrowFromCenter keeps tips full size, as in ch2 s5). Now fades in whole.
  - s4 ~59 s (c4.model.3 {slower}): the clock's point list morphed 1× → 2× period, so falling
    edges passed under the danger zones and T_c briefly spanned rising→falling (Transform
    between unlike square waves, as in ch1 s2). Now rebuilt every frame from a period tracker.
  - s4 ~66 s (c4.model.4 {tau}): the board cleared object by object, leaving BLUE ticks and
    the tally floating after the clock (staggered FadeOut, as in ch2 s3). Now one fade.
  - s4 ~77 s: the first "÷ e" arc began on the RED T₀/T_c label and read as a stroke through
    it while drawing. Arc start moved clear.
  - s6 ~63 s (c4.fail.4 {pfail}): the P_fail box grew from the formula's centre, so on
    "pee-fail" it first framed only the e. Now fades in at full size.
  - s6 ~6–21 s: the t_res arrow stayed thickened (stroke 5) through unrelated lines after its
    {wait} beat (Gemini called it a lingering box). Now reverts on its next beat.
  - s7 ~48–51 s (c4.recap.3): each tick's P_fail tag faded in while the previous one was still
    fading out on the short D0 wire, two tags overlapping; the last slid under "FF0". Tags now
    live for 70% of a tick's run and stop left of FF0.
  - Not real: s5 ~33.5 s "D0 label missing", ~38.3 s "D0 pulse vanishes" (the press flash
    ending); s6 ~61.5 s "t_sv" in flight (480p softness of a same-string transform).
  - Final reviews (out/ch4_metastability.mp4): viewer pass 0 findings. Transitions pass, both
    checked by the director on 1080p frames and accepted, no re-final: 03:21 (s4 c4.model.1,
    "garbled doubled line under resolution time") is t_res and "resolution time" fading in with
    a small upward slide, faintly overlapping for ~0.4 s, then clean (FadeIn with shift);
    06:21 (s5 c4.sync.4, "faint duplicate of sees a settled input") is one label fading in with
    a slight rise, with no duplicate in any frame.
- Open (low): Gemini scene reviews also flagged, and I dismissed: s3 "dashed line to the wrong
  valley" (it follows the spoken order, Q = 0 first), s4 "5τ highlighted" (matches "after five
  tau"), s5 "new value on D1, not Q" (the brief puts it on D1). The scene renders run 2–11 s past
  their narration (end holds; the recap's 8 s end card).
- Rewritten lines (all re-voiced; `vk listen --only` clean afterwards):
  - c4.sync.3 "one clock-to-cue delay after the edge" → "one clock-to-output delay after the
    edge" (pre-emptive: ch1/ch2 Gemini heard "clock-to-cue" as "cock-to-Q").
  - c4.undef.2 "After it, cue can become undefined." → "After the edge, cue can be undefined."
    (Gemini heard "undefied"); "Here's what that means in volts." → "…as a voltage." (Gemini
    heard "vols" in the re-voiced take).
  - c4.ball.1 "Think of a ball on a hill, with a valley on each side." → "Think of a hill with a
    valley on each side, and a ball that can roll between them." (Gemini heard "in a hill").
  - c4.model.3 "If each zone is a twentieth…" → "If each zone takes up a twentieth…" (+qa:
    "is" heard as "has"); after the s4 review, "at every edge of the clock" → "at every rising
    edge of the clock" (the zones sit on rising edges only).
  - c4.undef.2 again after the s2 review: "Between them lies an invalid range." → "Between them
    lies a range where the voltage is not valid." (Gemini heard noun-stressed "IN-valid").
  - c4.fail.1 after the s6 review: "How can we make an invalid output even less likely?" → "How
    can we make a meta-stable output even less likely?" (same "IN-valid"); then "But flip-flop
    one still needs dee one steady a set-up time before its next edge." → "But dee one must
    still be steady one set-up time before the next edge." (re-voiced take heard "flip-plop").
- Accepted voice flags: c4.model.3:4 "a twentieth" → "a 20th" (number format, producer's call).
  Gemini's re-listen heard "with" as "wit" in c4.sync.3:5 (same audio the full listen passed):
  variance.

## Chapter 5 · Mean time between failures (ch5_mtbf)
- State (2026-10-31): final rendered, `out/ch5_mtbf.mp4`, 8:50 (530.4 s, 1920×1080, 60 fps);
  narration 24/24 voiced, 8.2 min. Music `music/ch5.json` (hook Spirals, s3 curve stretch
  Resonance over c5.mtbf.4, recap Endpoint with the swell). 7/7 scenes by Opus scene-builders:
  s1, s2, s4, s6 before the pause; on resume s3 (from s2's end shot) + s5 (from s4's), then the
  recap. Gemini review per scene + holds, two fix rounds (s1, s7 one; s2, s3, s5, s6 two; s4
  none), then one round after the final reviews (s3, s5) and a re-final.
- **Recap teaser (ch5_s7_recap.py, built 2026-10-31), for ch6**: ch6_s1_hook.py `system_hero()`
  mapped p → (0, 1.0) + 0.65·(p − (0, 0.3)). Box 2.86 × 1.17, corner 0.1625, FG stroke 4,
  centre (0, 1.0); "the system" T 30 (unscaled) at (0, 1.12); DIM belts stroke 4 at y 0.44,
  x −4.29..−1.43 and 1.43..4.29; everything at opacity 0.6 (square fill 0.85 × 0.6). Four
  squares 0.325, corner 0.065, BLUE/GREEN/TEAL/FG, queued at x −1.79/−2.24/−2.70/−3.15, y 0.62,
  slide in from 0.3 right. On "without" task 1 enters to (0, 0.62) as the queue advances
  (1.2 s); then twice: wait 1.4 s, busy square to the done pile (3.45, 0.62 + 0.377k) (1 s),
  next enters (1 s); ends pile 2, 1 inside, 1 queued; 2.2 s hold, fade. Below it, "Part 6 ·
  Latency, throughput and pipelining" T 40 at (0, −1.3) comes in on "fast".
- Rewritten lines (all re-voiced; `vk listen --only` clean afterwards):
  - c5.cascade.3 "Each extra flip-flop would just halve the chance" → "…would only cut the chance
    in half" (+qa: "halve" heard as "have" by all three Whisper models, as in L6).
  - c5.rate.3 "The slide writes it like this: pee-fail per second…" → "In the slide's notation,
    pee-fail per second…" (Gemini heard "pee-feel").
  - c5.mtbf.2 "Failures per second are N times pee-fail." → "The number of failures per second
    is N times pee-fail." (Gemini heard "Billions").
  - Resumed run, after the Gemini scene reviews (each `vk listen --only` clean afterwards):
    c5.hook.2 "the synchroniser fails about once…" / "it fails every ten seconds" → "there's a
    failure about once…" / "there's a failure every ten seconds" ("fails" heard "fills");
    c5.rate.1 "gets through still meta-stable" → "gets through while still meta-stable"
    ("stoo"); c5.cascade.1 "But a clock period of three nanoseconds may be too long for the rest
    of the system." → "But for the rest of the system, a clock period of three nanoseconds may
    be too long." ("clock" heard "clat"); c5.cascade.4 "and the clock period can shrink" → "Or
    keep the one-year target instead, and…" (same "clat"), "Take two additional flip-flops" →
    "Add two extra flip-flops" ("adishmal" in the re-voiced take), "using the slide's formula"
    → "with the formula from the slide" ("fornula" in the next take).
  - "kay" → capital "K" in c5.cascade.2 (×4) and c5.cascade.4 (×1): "kay" came out as "chi"/"kai"
    (+qa, all three Whisper models and Gemini) even after a rewrite; capital K, like the "N"
    rule, voices cleanly.
  - After the round-2 reviews: c5.trial.4 "about one in six and a half million" → "about one in
    six point six million" (the screen says 1 in 6.6 million, the true 1/1.51e-7; Gemini flagged
    the mismatch twice); c5.mtbf.1 "count seconds per failure" → "we measure seconds per
    failure" (Gemini heard "caught", then "kout").
- Shared drawings (ch6+ can copy them): mini synchroniser in s1/s2 = `sync_circuit()` ×0.6,
  to_corner(UL, buff 0.5); s3 `MTBF = T_c e^((T_c − t_su)/τ) / (N T_0)` (same TeX/colours as s4);
  s5 trial table (T_c YELLOW, MTBF GOLD, crosses RED, 3.04 tick GREEN) and the GOLD answer box
  `T_c ≥ 3.04 ns` (size 40, buff 0.18, corner 0.08, stroke 3, to_corner(UL, 0.5)), as s6 opens.
- Accepted check flags: s1/s2 mini synchroniser labels at size 18 (FF0/FF1/CLK; the brief asks
  for a small reminder circuit, and nothing in it is read); dwell advisories set by the brief's
  cue spacing (s2 dice faces and "N: average…", s3 "0.01 … ↔ 100 s" example and the short
  "failures" flip, s5 opening carry-over from s4, the 5τ bracket and the last check line, s6
  "K = 1" and "10 million times smaller", s1 title/"???").
- Departures: s3's brace sits above `T_c − t_su` (no room under it), with the t_res/t_su bar at
  the upper left; s5's answer box sits right of the table, ruler cleared (not dimmed) at
  {check}; recap tiles uneven widths (r3 widest), r2 curve under the formula, r4's 3.04 row
  without "≈ 1.05 years", r5 chain without labels, Part 6 title as the end card (as ch4).
- Glitches (scene, time, what, cause; confirmed on frames, all fixed):
  - s3 ~38 s (c5.mtbf.2 {invert}): the "two things change" flash also ringed the exponent's
    minus, before {sign} (one flash over both changes). ~41 s: the T_0/T_c flip waited for the
    phrase "upside down" and ran 3.1 s, still moving at {sign} (phrase cue + long run_time). Now
    the flash rings T_0/T_c only and the flip starts on {over}, scaled to end before {sign}.
  - s6 ~32 s (c5.cascade.2 {kone}, trim back to FF0 + FF1): the extra stages faded first and Q
    + the CLK bus only began to move at 45% of the play, so a lone Q sat at the far right and CLK
    ran into empty space (staggered sub-animations). The first fix overlapped the timings, but
    frames at 32.5 s still showed Q with no wire to it (the output wire didn't follow the
    label). Now a GREEN wire's end moves with Q in the same animation and CLK retracts with
    the triangles; the grow-back mirrors it.
  - s2 ~12 s (c5.rate.1 {safe}, a picture/words mismatch): a separate 0.6 s RED flash on D1 at
    "resolves" read as metastability during "resolves in time". Removed; a TEAL ring marks D1
    settling.
  - Not real (frames clean): s7 ~46.5 s "FG square disappears from the queue"; s5 ~67 s "cross
    and tick overlap"; s5 ~88 s "stray 7. in the header" (plain fade); s3 ~17.5 s "duplicate
    100 s labels" (plain fade-in); s5 ~55 s "missing ×e label" (labels arrive one by one).
    Matches the brief: s1 ~9.8 s Q label beside the RED "???"; s3 ~69/82 s dot on the T_c axis
    and the step along the original curve; s6 ~69 s "(ours)"; s7 ~50 s vertical done pile (as
    ch6 s1).
  - Final reviews (out/ch5_mtbf.mp4), both fixed and re-finaled:
    - 04:52 (s5 opening, both passes): s5 faded s4's dimmed list, T_c rings and tags back in,
      then cleared them, right after s4 had faded to empty. They read as cleared content
      flickering back (my round-1 continuity note plus the empty-frame rule). s5 now opens on
      the equation alone.
    - 02:45 (s3 ~45.6 s, c5.mtbf.2 {sign}): the arriving exponential parked on T_c's subscript
      and read "T_e" for ~0.5 s, and "N T_0" crossed the "=" (wrong glyph index as the move
      target: `at_glyph(…, 1)` was T_c's "c"). It now lands at its final spot; T_c moves first.
  - Final reviews, accepted: s3 02:00 "second per failures" for ~0.5 s while the two nouns swap
    round "per" (the swap moves the words, then fixes the plurals); s3 02:31 "P_fail =" fading
    a beat after its right side leaves (low); s2 01:07 "lowercase q" (italic math Q); s5 05:38
    "×15 between 311 and 384 days" (frames show 1.4→21 and 21→311: false); s6 06:34
    "flip-plob" (`vk listen --only c5.cascade.1` clean: variance).
- Open (low): s2→s3 and s4→s5 hand over their picture through the empty frame (the engine
  rule noted under "Paused"); s3 re-shows s2's formula after the dip, and s5 now re-shows only
  the equation. The re-voiced c5.trial.4 runs at 186 wpm, faster than its neighbours (~150–175);
  it passed QA and Gemini. Scene renders run 3–11 s past their narration (end holds; the
  recap's ~9 s end card).
- Accepted voice flags: number formats (producer's call): "three point oh four/oh three
  nanoseconds" (c5.trial.2, c5.trial.4, c5.cascade.4, c5.recap.1), "every hundred seconds"
  (c5.mtbf.1), "tee-nought" → "t0" (c5.example.3). c5.cascade.3:5 "But square" → "Put square"
  (Whisper small + medium; Gemini's full listen passed it, and `vk listen --only c5.cascade.3`
  passed it again on resume) and c5.cascade.3:4 "you'd need" → "you need" (meaning kept).
  "pee-fail" passed Gemini's full listen. Gemini's s2 review "book's → hook's" is a false
  finding (the script says "hook's").

## Chapter 6 · Latency, throughput and pipelining (ch6_pipelining)
- State (2026-10-31): **done.** `out/ch6_pipelining.mp4`, 1920×1080 60 fps, 9:10.7 (550.7 s;
  narration 8.5 min). Narration 25/25 voiced; Gemini full listen clean after the rewrites below.
  Music `music/ch6.json` (hook Fractals, s3 baking picture Reflections over c6.kinds.3, recap
  Ongoing with the swell). 7/7 scenes by Opus scene-builders: s1 + s2 + s4 before the pause, then
  s3 (from s2's end shot) + s5 (from s4's lanes) + s6, then the recap. Two review rounds
  (round 1: s1–s5; round 2: s1, s5, s6, s7) plus one post-final fix (s3 tags).
- **For ch7's director (helpers between `# ===` rulers):**
  - *Task colours:* task 1 BLUE, 2 GREEN, 3 TEAL, 4 FG, repeating (`TASK_COLORS` in s1).
  - *Staircase:* ch6_s5_pipe.py `staircase()` + `column_box()`, using s4's `stage_box`
    unchanged. Boxes 1.7 × 0.9, task-coloured outline stroke 3, fill 0.18, MathTex 40 label
    (A₁, B₁, …). Column 0's left edge x −5.1 (s4's grid); row r (0–3) centred y 1.75 − 1.3r,
    Aᵣ₊₁ in column r, Bᵣ₊₁ in column r+1; spans x −5.1..3.4. Five YELLOW thin double arrows at
    y 2.65, one per column (inset 0.05), MathTex 36 "T_c" above. DIM dashed guides stroke 2 at
    each column boundary from y 2.3 down to the lowest box they touch. Finish ticks GOLD stroke
    6 at each B's right end; column highlight YELLOW stroke 3, fill 0.12. Compact copy (c6.pipe.5):
    `x0=-6.2, top=0.25, pitch=0.75, w=1.4, h=0.6, size=32`. s4's one-at-a-time row
    (A₁ B₁ A₂ B₂ A₃, two lanes, DIM "idle" hatching) is in ch6_s4_nopipe.py on the same grid.
  - *Pipelined path:* ch6_s6_registers.py `pipe_diagram(fy)` / `pipelined_parts(D)` (closing
    picture at fy 1.8). Registers (`make_ff` ×0.75, box 1.125 × 1.95, BG fill, two DIM ghosts
    offset +0.1/+0.2 up-right) at x −5, 0, 5, pin row y 2.25; logic blocks BLUE, 1.3 tall, at x
    −3.8..−1.2 and 1.2..3.8; labels T 30 on y 3.3 ("register" FG, "stage 1/2 logic" BLUE);
    Q_0 GREEN, D_1 BLUE MathTex 36; CLK YELLOW at y 0.075 from x −5.6 to 5, dots at −5 and 0.
  - *"The slowest stage decides":* same file, `stage_bar(i)`, `t_brace`, `t_guide`,
    `closing_tag`. Bars start x −4.4, bar 1 y −0.9, bar 2 y −2.2; t_pc 0.7 PINK, t_pd 2.2 / 3.1
    PURPLE, t_su 0.6 GOLD, both outlines 4.4 long (stage 1's stretched with slack); "stage 1/2"
    T 30 left; YELLOW brace under bar 2 from x −4.4 to 0 with T_c (44) below, dashed YELLOW guide
    at x 0; tag "the slowest / stage decides" T 36 YELLOW centred (3.3, −1.55).
  - *Recap teaser (ch7's circuit, unlabelled):* ch6_s7_recap.py, DIM input register → fork into
    blocks 1 and 2 → block 3 → YELLOW register (the added one) → block 4 → output register.
- Departures worth knowing: s1's synchroniser and table are stacked (side by side is 13.5 units
  wide, more than the margins), the synchroniser without ch4's push button; s3 keeps only the slot
  headers at {bake}; s5's long T_c arrow replaces the first two per-stage arrows in turn (not
  drawn over them), the staircase's latency brace sits below the staircase, and c6.pipe.6's
  summary is a right-column "latency / in periods: 1 → 2 / in ns: 10 → 10 (ideal) / real
  circuit: a little more"; s6's bars stack before the bracket, and coloured squares in the
  registers show which token each holds; the recap tiles are rebuilt at tile size (r2's split box
  reads "1 | 2"), r4's brace is under task 4.
- Accepted check flags: dwell advisories only (s1 title card fading on {last}; s2's "7" and the
  end shot s3 opens from; s3's slot "1" and closing "temporal"; s4's "the system" and the
  throughput lines leaving at c6.seq.3; s5's s4 hand-off labels, "free", "latency?", "real
  circuit"; s6's "???" 2.7 s, which must clear on {with}): each is set by the brief's cues or a
  hand-off.
- Glitches (scene, time, what, cause; confirmed on frames):
  - s1 ~17 s (c6.hook.2 {box}): the system box's right border showed a gap: `Create` still
    drawing the outline round. Now fades in whole. Fixed.
  - s1 ~34 s (c6.hook.3 start): a dark rectangle popped into the box: the progress sweep jumped
    35% in 1 s at the clip start. Now advances steadily. Fixed. Same pass: the "10 ns" frame grew
    from a dot (read "10·ns"); now fades in at slight scale.
  - s1 ~33 s: "waiting" with no digit for a moment: the count swap faded the old digit out fully
    before the new one came in. Now swaps in place mid-play. Fixed.
  - s6 ~21 s (c6.reg.1 {shorter}): two arrow tips alone above the middle register:
    `GrowFromCenter` on a DoubleArrow keeps tips full size (as ch2 s5, ch4 s4). Now fades in whole.
    Fixed. Also the dashed YELLOW guide slid across stage 2's t_su label at {decides}; now
    fades out/in. Fixed.
  - s6 ~52–55 s: RED wire and "???" stayed ~2.5 s past {with} (cleared at {hold}). Fixed.
  - s7 ~30 s: r4's caption line "about half as long" landed ~1 s after its words (read as
    vanishing). Fixed.
  - s3 ~21.7 s (c6.kinds.2 {temporal}): the box splitting into two stage boxes shows two
    overlapping outlines mid-move (final at 142.5 s). Accepted: brief, low.
  - Not real (checked on frames): s1 squares "turning white" (tasks 4 and 8 are FG), "GREEN turns
    TEAL" (each slides, keeps its colour), the {now} slide-off; s5 "B₄ reads B₁" and "duplicate
    10 ns brace"; s6 "duplicate t_su"; s2 "stray dark square" (the queue fading in); s4 "yellow
    dashed outline" at 242 s of the final.
- **ch5's recap teaser copies ch6 s1's hero** (ch5's brief says so): ch6_s1_hook.py holds it
  between `# ===` rulers. Spec: RoundedRectangle 4.4 × 1.8, corner 0.25, FG stroke 4, no fill,
  centre (0, 0.3), "the system" FG 36; task squares side 0.5, corner 0.1, fill 0.85, no stroke,
  task 1 BLUE, 2 GREEN, 3 TEAL, 4 FG, repeating.
- Rewritten lines (re-voiced; `vk listen` clean afterwards):
  - c6.hook.1 "we made a synchroniser's clock period longer on purpose" → "we gave a
    synchroniser a longer clock period, on purpose" (writer's risk: "synchroniser's").
  - c6.hook.3 "finish more tasks per second" → "get more tasks done each second" (Gemini heard
    "task").
  - c6.kinds.3 "from Harris and Harris, one of the course's books" → "from the textbook by David
    and Sarah Harris" (as ch2); "Borrow a friend with a second oven, and that's…" → "If a friend
    with a second oven bakes a tray alongside yours, that's…" (Whisper heard "Bar a").
  - c6.reg.4 "clock-to-cue delay" ×2 → "clock-to-output delay" (as ch4; "cock-to-Q" risk).
  - c6.speed.3:3 "Throughput asks, how many…" → "And throughput asks, how many…" (s2's Gemini
    review and a re-listen both heard "Throughbut"; re-voiced, `vk listen --only` clean).
  - c6.recap.1 "Latency is… Throughput is…" → "The latency is… The throughput is…";
    "Temporal parallelism, or pipelining…" → "And temporal parallelism, or pipelining…" (the
    recap's Gemini review and a re-listen heard "laydency" and "tepporal"; re-voiced, clean).
- Accepted voice flags: c6.reg.2:3 "Combinational" → "Commonational" (Whisper base + small;
  Gemini's full listen and a targeted `vk listen --only c6.reg.2` both passed it: jargon).
  "Garbage.", "Wait." and "slides'" passed Gemini.
- Consistency with ch5 (checked against ch5_s5_trial.py and ch5_s7_recap.py, 18:2x): the hook's
  trial table has ch5's values, colours (T_c YELLOW, MTBF GOLD, RED crosses, GREEN tick); ours
  sets them as text, not MathTex (small font difference, accepted). Both use SYS_W × SYS_H
  4.4 × 1.8 for the system box.
- Final reviews (out/ch6_pipelining.mp4): viewer pass and transitions pass. Both flagged s3's
  c6.kinds.3 tags (dim "spatial" beside the pin, "temporal" beside the oven read as "roll =
  spatial, bake = temporal"); fixed after the final ("spatial" fades with the second baker's row
  on {tray}, "temporal" lands centred under the roll → bake picture), re-final 9:10.7. The s3
  re-review no longer reads it that way; its two remaining claims are mid-move and accepted
  (22 s, the split boxes overlapping; 59 s, the "spatial" tag flying past "roll", confirmed on
  frames at 179.8 s of the final). The "spatial" tag is up only ~0.7 s (dwell flag): accepted, the
  lit "spatial" header carries the word. Dismissed: s6 ~21.7 s "T_c spans
  both stages" (it shrinks from the whole path on {shorter}, as briefed); s1 ~30 s "waiting 3 with
  four queued" (mid-arrival; the settled count matches).

## Chapter 7 · Pipelining a circuit (ch7_pipeline_example)
- State (2026-10-31): **done.** `out/ch7_pipeline_example.mp4`, 1920×1080 60 fps, 9:33.5 (573.5 s;
  narration 8.8 min). Narration 27/27 voiced. Music `music/ch7.json`: Fragments under the hook (to
  c7.circuit.1), Centroid under c7.payoff.1 (tokens flowing through the two stages), Quantum Blue
  from c7.recap.1:end with the swell after c7.recap.4 (end card). 7/7 scenes by Opus
  scene-builders: s2 (owns the circuit helpers) + s6, then s1, s3, s4, s5 from s2's helpers, then
  the recap. Two review rounds (r1: s1–s6; r2: s3, s4), one post-final fix (s6, s7), re-final.
- **Shared drawings (between `# ===` rulers):**
  - *p. 117 circuit:* ch7_s2_circuit.py `circuit()` (every part addressable, routes `.r1`/`.r2`,
    `C.xy`), `a_register(C)` (flip-flop at A), `s5_registers(C)` (on CB1's and CB2's outputs),
    `stage_panel(C, x0, x1, k)`, `run_pulse`/`route_path`. Full width 13.3, centred (0, 0.4); blocks
    BLUE outline, names T 32, t_pd PURPLE MathTex 38, CLK YELLOW.
  - *Shrunk circuit (s3, s4):* scale 0.66, top y 3.55, centre x 0.6; small labels faded, CB names
    T 28 outside their blocks.
  - *Bars:* ch1 `budget_bar`, 0.85 units per ns, left edge x −4.6, height 0.5; PURPLE segments
    carry block names (FG T 28) with BG dividers. Corner numbers s3→s4: GOLD T 30 "12 ns" over
    "83.3 MHz", left x −6.6, top y 3.5.
  - *Stalled staircase:* ch7_s6_limits.py (ch6 grid, rows 0.6 lower; YELLOW dependency wire,
    dashed RED "stall" slot).
  - The recap imports its builders from the source scene files (ch7 s2–s6, ch1_s1, ch1_s3, ch4_s5,
    ch6_s6) instead of copying them, so edits there change the recap.
- Departures: s1's ghost register sits in its slot (the t_pd labels fill the space above), with
  "× 2 ?" on its own line under the YELLOW "?"; s2 leaves out the "slide's point A" tag (s1 shows
  it), and CB1's label ticks 3.2 → 2.9 → 2.3 instead of going back between; s3 and s4 shrink the
  circuit and fade its small labels; s4's bar sums sit right of the bars; s5's 12 ns bar is
  labelled "one stage", and its three-stage circuit is up only ~3.5 s (it clears for the bars);
  s6's "add" / "use the sum" are tags left of the rows, and the staircase drops 0.6 for the quote;
  recap slot 4 is three lines of numbers, not the full table.
- Accepted check flags: dwell advisories only (s1 title card and ch6 picture; s2's clip-5 ticks
  and stamps; s3's fading circuit labels; s4's A marker 1.4 s and "2.5 < 3.2" 3.3 s; s5's
  three-stage circuit, throughput line and p. 118 quote; s6's "use the sum", "processors: special
  measures", "temporal:"; recap's "stall" tags): each is set by its cue. The corner-number margin
  flags (my spec said top y 3.7) were fixed.
- Rewritten lines (re-voiced; `vk listen --only` clean afterwards):
  - "clock-to-cue delay" → "clock-to-output delay" in c7.circuit.2, c7.unpiped.1, c7.cut.4,
    c7.payoff.3 (producer note). c7.cut.1 "dee-type flip-flop" → "dee flip-flop" (as ch2, ch6).
  - c7.recap.2 "Throughput nearly doubled, while latency grew…" → "The throughput nearly doubled,
    while the latency grew…" (bare-noun opening); "the pipeline stalls" → "the pipeline has to
    stall" (Gemini "pipelane").
  - c7.payoff.3 "That's zero point three nanoseconds." → "Together, they add zero point three
    nanoseconds." (Gemini "point three").
  - c7.limits.1 "Pipelining is powerful…" → "Now, pipelining is powerful…"; "The pipeline is
    built for it." → "…designed for that."; "That's called a pipeline stall." → "This is called a
    pipeline stall." (Gemini "pipelning", "build", "pipelan").
  - c7.unpiped.1 "how short can the clock period be? … The clock period must be…" → "how short
    can the period be? … The period must be…" (Gemini "cock", "quack"); "…plus the set-up time." →
    "…plus the set-up time of the next register." (Gemini "ten"). A later "zero" → "viro" didn't
    repeat on a re-listen of the same audio.
  - c7.recap.4 "We'll start with some definitions" → "…with a few basic terms" (s7's review and a
    re-listen heard "dethinitions" / "deafenitions").
- Accepted voice flags: c7.circuit.5:2 "route" → "root" (British, producer); c7.recap.2:2 and
  c7.payoff.3:5 "register costs time" → "cost" (Whisper; Gemini passed it in three listens);
  c7.recap.3:3 "time buys years" and c7.payoff.5:4 "seventeen point four" (base only). The
  writer's risks (synchronous state machines, 153.85 MHz, 1.85 times, every edge of the clock)
  passed every listen. Spoken "eighty-three megahertz" against "83.3 MHz" on screen at s3's close:
  accepted (the line rounds on purpose).
- Glitches (scene, time, what, cause; confirmed on frames):
  - s2 ~78 s and ~90 s (c7.circuit.5 ticks, restore): sums read "2. + 3 + 5.5 = 1 . ns": `edit`
    faded only the digits that differ while shared glyphs stayed. Now old numbers fade whole, new
    ones in place. Fixed.
  - s3 ~2 s: the bar's YELLOW outline growing from its left edge read as a stray bracket; now fades
    in. ~57 s: the rotated "=" squeezed between two "12 ns" read as tick marks; given room. ~17 s:
    PURPLE segments started on the "plus" before their number (CB4 lit during "plus three"). Fixed.
  - s4 ~46 s: the GOLD 0.1 came out of the new register as a grey sliver while CB3 was still bold,
    so CB3 read as its source. The register now turns GOLD and a gold copy drops in. Fixed.
  - s5 ~85 s: the board clear faded pieces one by one, so "stage k" labels left before their bars
    (jump at the left edge) and faded CB names flashed back. Rows now leave whole. Fixed.
  - s6 ~64 s: per-box flashes on eight tiny staircase boxes drew loose YELLOW strokes past the chip
    outline; one flash round the core now. Fixed.
  - s6 ~38.7 s (final 07:38, c7.limits.2 {every}): A₃ passed through B₂ (A₂ grazed B₁) as the
    staircase straightened: one linear play moving every box diagonally. Now task 3 slides along
    its row first, then all rise straight up. Fixed.
  - s7 ~41.6 s (final 08:53, c7.recap.3 {lecture}): bottom-row slots crossed the shrinking top-row
    tiles: one play moved all six slots in the same window. Now staggered (text fades, top row
    shrinks, bottom row rises, chips last). Fixed.
  - Not real (frames): s4 "5.8 ns twice" (the second is stage 2's sum); s5 "duplicate register"
    (registers see-through mid-fade); s6 "rows 3–4 stay put" at 21 s; s6 "13 not RED".
  - Accepted, mid-move, low: s1 ~5 s "D_1" (ch6's own label), ~25 s A marker under the dropping
    ghost; s4 ~26 s GREEN dot appears, then runs; s6 ~15 s dependency label fading in.
- Final reviews: viewer pass clean (0 findings). The second transitions pass found nothing in s6
  or s7 but raised seven new mid-move claims in s1–s5. The producer asked for one more small round,
  so each was checked on 1080p frames of the final (times in the final):
  - Not real: s5 06:22, the caption "cut where the stages come out equal" never touches the
    formula (the old caption fades before the new one fades in above it); s2 01:48, "part 1" stays
    inside the frame; s3 02:30, the "B2" is CB1's copy flying to the bar over CB2's dim name.
  - Real, fixed (glitch log): s4 04:50 (c7.cut.5 {slide}), the T_c label read "5  ns" ~0.5 s:
    `edit(5.8, 6.5)` kept the shared "5" while the rest faded; now `ride_swap` fades whole numbers.
    s4 03:58 and s3 02:15 (the shrinks): small labels faded through `disappear` where they stood,
    detached from the moving circuit, and s3's CB names slid out through their block borders; now
    labels scale and move with the circuit while fading (`_ride` in s3), and names crossfade
    inside → outside. s1 00:09 (circuit draw): each part started when the sweep reached its left
    edge, so outgoing wires, t_pd labels and the A marker showed before their block finished; now
    held until their block (A until `w_34`) has drawn.
  - Re-final 9:33.5 (573.5 s), 1920×1080 60 fps; the four fixed spots checked on its frames. No
    further Gemini pass (the fixes change motion only at those spots).

## Paused (producer, 2026-10-31), resumed the same day; ch5–7 finished, notes below kept for the record
The user paused the work mid-run; both directors were stopped and no studio processes are left.
- ch1–4 done (`out/`). ch5: s1, s2, s4, s6 built, their Gemini reviews were cut off; s3, s5, s7 not built
  (s3 and s5 builders were stopped mid-work, so any half-written scene file there is unfinished). ch6: s1, s2, s4
  built, unreviewed; s3, s5, s6, s7 not built. ch7: nothing built, no music.
- Resume: a chapter-director each for ch5 and ch6 (two at once), then ch7. Built scenes still need review.
- Producer notes to pass on again:
  - ch5: reword c5.cascade.3:4 "halve" (heard as "have"); check "But square" with `vk listen`; accept the
    "three point oh four", "hundred seconds" and "tee-nought" number-format flags. Copy ch4's synchroniser and
    t_res + t_su bar.
  - ch6: reword c6.kinds.3:4 "Borrow a"; check "Combinational" with `vk listen`; say "David and Sarah Harris"
    as ch2 does. Copy ch5 recap's system-box teaser. Record the staircase helpers for ch7.
  - all: Gemini has heard "clock" as "quack", "clock-to-cue" as "cock-to-Q" (ch4 says "clock-to-output"),
    "flip-flop" as "foot flop"/"flip-plop", "launches" as "wauches", and "invalid" with the noun's stress.
- Open for after the lecture: the near-black dip between scenes that hand over their picture (ch2 s3→s4→s5)
  comes from the "end on an empty frame" rule. That's an engine change, not done.

## Done (producer, 2026-10-31)
All 7 chapters are in `out/`, 62.6 min at 1080p60. Claude tokens for the lecture: 187M context read + 11M cache
writes over 146 agents (`vk usage`), inside the planner's 160–230M estimate. The near-black dip between scenes that hand over their picture (ch2, ch5, ch7) is fixed in the
engine from 2026-10-31 (`# handover: next`, docs/LESSONS.md); these videos keep their dips, by the user's choice
(no re-render). To apply it here later: a fix pass per chapter on those 7 joins, then `vk final`.
