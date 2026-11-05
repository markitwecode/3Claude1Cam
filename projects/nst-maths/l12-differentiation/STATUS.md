# Differentiation: status

2026-11-03: project created; planning.

## Chapter 1 · What is a derivative? (ch1_first_principles)
State: **ready for final** (2026-11-03 18:47). Preview `out/ch1_first_principles_preview.mp4`,
12.8 min (767.0 s), decodes end to end; `vk preview 1`: handover ok s3 → s4 (0.00%); s7 ends on ch2's
opening card (reversed join, no mark). Narration voiced, paced and QA'd (29 lines, 11.9 min).
- Re-timed 18:44: the bulk run's pacing changed c1.diff.4–5 (s6 narration 108.8 → 117.5 s). s6 re-rendered
  against the current manifest (124.5 s); its beats image shows every cue of c1.diff.4–5 in sync. No other
  ch1 line changed; nothing downstream depends on s6's timing (s7 imports only static `diff_box()`/`thumbs()`).
Gemini off until ~00:30: `vk listen 1` and `vk review` (scene) are skipped; Whisper vote, `vk check`,
holds and builders' `--frames` sheets are the review.
- **Opening card (ch1's first frame; the pattern for ch2–7):** ch1 opens from empty on the engine title
  card, `title_card("Part 1 · What is a derivative?")` from `lib.titles` (project title "Differentiation",
  course line "NST IA Mathematics · Lecture 12", as L11 did). `load_scene("ch1_s1_hook").open_card()` will
  return it as a static VGroup, as it stands once settled (no updaters). Suggested for every chapter:
  part N's opening card is `title_card("Part N · <title>")` alone on screen, so each recap's end card
  lands on it. **READY** (scenes/ch1_s1_hook.py): `open_card()` is the TitleCard VGroup centred at
  ORIGIN, static; parts `.title` ("Differentiation", T 96, not rescaled), `.rule` (DIM line, 5.6 wide),
  `.course` ("NST IA Mathematics · Lecture 12"), `.part`. s1 fades it in from empty and holds it 4.9 s.
- **Waits for ch2's opening card:** ch1 s7 (recap, built last) ends on exactly
  `load_scene("ch2_s1_hook").open_card()`, no handover mark. ch2's director: please record it here
  (objects, layout, and whether it is the bare title card). Until then s7's `end_card()` returns the
  stand-in `title_card("Part 2 · The rules, from first principles")`; it switches by itself once
  scenes/ch2_s1_hook.py defines `open_card` (entered with one `sweep_clear(... FadeIn(card) ...)` after
  c1.recap.3's last word, held 8 s alone, then a 1 s fade). ch2 recorded its card at 18:45: the same bare
  title card, so the join is the same picture with or without ch2's file. Note for ch2: for a seamless
  join ch2 s1's first frame should be the card itself (its record says s1 fades it in from empty).
- **Helpers ch1 exports** (planned forms; READY + exact parts are added as each is built):
  - Figure 29, `load_scene("ch1_s2_chord").figure29(...)`: axes "x" / "y(x)", BLUE y = x³ on x ∈ [0, 1.7]
    (no formula label), dot at x = 1, second dot at x + δx, TEAL δx/δy braces and chord, GREEN tangent
    line of slope 3 at x = 1. For ch1 s7, ch3 s6 (reflected in y = x), ch6 s5.
    `definition_box()`: (103) boxed YELLOW, `\frac{dy}{dx} = \lim_{\delta x \to 0} \frac{y(x+\delta x) -
    y(x)}{\delta x} = \lim_{\delta x \to 0} \frac{\delta y}{\delta x}`, δx/δy TEAL, dy/dx GREEN.
    **READY** (scenes/ch1_s2_chord.py): `figure29(dx=0.5, tangent=False, chord=True, braces=True,
    q_labels=None, x0=1.0)`, full size at a fixed place (axes origin (−5.6, −3); x 0–1.8 over 7 units,
    y 0–5 over 6); parts `.axes .xlab .ylab .curve .p_dot .p_drop .p_lab .q_dot .q_drop .q_lab .run_leg
    .rise_leg .right_angle .run_brace .run_lab .rise_brace .rise_lab .chord .chord_lab .tangent
    .tangent_lab` (None when off). Helpers `chord_line(axes, dx, x0)`, `tangent_line(axes, x0)`,
    `corner_tag()` (`y = x^3,\ \text{at}\ x = 1`, size 36, FG, UR buff 0.5). `definition_box(size=44)` →
    VGroup(`.rect`, `.formula` (7 parts, δx/δy TEAL, part 0 GREEN), `.num` "(103)" DIM 28), at ORIGIN.
  - x³ derivative-chain card, `load_scene("ch1_s3_cube").cube_card()`: `x^3 \to 3x^2` (3x² GREEN), top-left
    of the frame, room on the right. **READY** (scenes/ch1_s3_cube.py, also `handover_shot()`):
    `MathTex("x^3", r"\to", "3x^2", font_size=44)`, 3x² GREEN, rest FG, in a RoundedRectangle (corner 0.15,
    YELLOW stroke 2.5, no fill, 0.3 padding); parts `.frame`, `.expr`; whole card `to_corner(UL, buff=0.5)`.
    `derivation()`: the five step labels and the column ending in the boxed GREEN 3x². ch4 s2 extends it to `x^3 \to 3x^2 \to 6x \to 6 \to 0`, ch6 s4 sets
    x⁴'s chain (`x^4 \to 4x^3 \to 12x^2 \to 24x \to 24`) beside it.
  - Differentiability box, `load_scene("ch1_s6_differentiable").diff_box()`: BLUE border, the notes'
    text verbatim: "For a function f(x) to be differentiable at x:" / "(a) the function must be
    continuous" / "(b) the derivative f′ exists if it is finite and defined." / "⇒ the left- and
    right-hand limits must be the same:" / `\lim_{h \to 0}\left(\frac{f(x) - f(x-h)}{h}\right) =
    \lim_{h \to 0}\left(\frac{f(x+h) - f(x)}{h}\right)`, every h TEAL. For ch2 s3/s5, ch3 s3, ch1 s7.
    **READY** (scenes/ch1_s6_differentiable.py): VGroup with `.border .head .a .b .then .eq .lq .eqsign
    .rq`; `.lq`/`.rq` are MathTex with every h TEAL; brackets are `\Big( \Big)`; `.b` has ligatures off
    (`select(box.b, "finite")` works); 10.0 × 3.87 at full size. `thumbs()` → VGroup(v, step) at
    (∓3.4, x-axes at y = −1.5), built from s5's `v_graph()`/`step_graph()` scaled uniformly by 0.4
    (V arms at 45°); parts are s5's (`.ax .curve .corner` / `.ax .left .right .jump .hole .dot`), with the
    old names `.dot` (V), `.lo`/`.hi` (step) kept as aliases.
  - The corner and the jump (s5 `v_graph()`, `step_graph()`; s6 `thumbs()`): BLUE y = |x| on [−2, 2]
    with a RED corner dot; BLUE step, 0 for x < 0 and 1 for x > 0, open circle at (0, 0), filled dot at
    (0, 1), dashed RED vertical (0, 0)–(0, 1). s5 **READY**: `v_graph()` → VGroup(`.ax` DIM x −2.4..2.4,
    y −0.6..2.4; `.curve`; `.corner`), `step_graph()` → VGroup(`.ax` x −2.2..2.2, y −0.6..1.8; `.left`,
    `.right`, `.jump`, `.hole`, `.dot`), both at ORIGIN, 1.6 units per step; `axis_labels(ax)`.
- Music: `music/ch1.json`: Zeta (hook, START → c1.chord.1), Stepwise (s5's corner, c1.fail.1:end →
  c1.fail.3), Euler's Clock (recap + end card, c1.recap.1:end → END, swell after c1.recap.3).
- Waves: s1, s2, s3, s5, s6 → s4 (opens on s3's `handover_shot()`, the x³ card) and s7 (after ch2's card).
- Built 2026-11-03 18:00–18:37, all seven scenes by Claude scene-builders: s1 79.4 s, s2 141.5, s3 122.1,
  s4 120.9, s5 124.2, s6 114.2, s7 54.5 (narration 11.7 min). Handover s3 → s4 (the x³ card) 0.00%.
- Review (Gemini off, so no `vk review`/`vk listen`): `vk check`, two holds rounds, builders' `--frames`
  sheets (read for s2, s3, s5, s6, s7). Round 1 fixes: s2 slope readouts stack as a table (4.75, 3.31,
  3.03, then the GREEN δx → 0 row) and the shrunk figure's "tangent" label is off the curve; s5 the
  10 → 100 readouts stack, the ±1 chords stay through {fails}; s6 thumbnails rebuilt from s5's helpers
  at uniform scale (V at 45°, was squashed 3.6 × 1.3), result rows moved up; s7 the three rule labels
  stay through "Each one comes from this same limit" (were up 0.4 s), with arrows to (103), and grow
  from the box's edge instead of frame copies crossing the formula.
- Accepted check flags: s6 small text 26 in the shrunk differentiability box at {runmod}–{blow} (the
  brief's box + two thumbnails + three result rows don't fit at 28 without cramping; the box is the
  dimmed reference there, the rows are the focus); s7 small text 7–10 in the recap strip's thumbnails
  (pictures of earlier panels, each shown full size while its sentence plays) and caption/(103) dwell
  (the clip's length); dwell advisories everywhere else are voice-driven (s1 title card 4.9 s, s1's last
  tags 3.1 s at the end of c1.hook.1, s2 lecturer quote 6.7 s and the closing quotients, s6 0.1–0.8 s).
- Departures accepted: s1's YELLOW "from first principles" lands on "from the foundations"; s4 ticks under
  both fractions and y′ ("the fractions"); s6's quotient copy is in f/h form rather than (103)'s y/δx, the
  box leaves at {implies}; s7 shows each panel big, then shrinks it into a strip of four (a 2×2 grid put
  the derivation and box text at 10–17), and its rule labels grow from the box (no text morph).
- Glitches: none confirmed on frames (s2, s3, s5, s6, s7 sheets clean; s4's split and pull-apart sheet
  reported clean by its builder). s3's δx copies flying into the denominator are faint and tilt on their arc.
- Gemini checks skipped (quota until ~00:30): `vk listen 1` (the ear check of all 29 lines) and the
  per-scene `vk review`. Voice QA: the 5 Whisper flags the producer accepted (Oiler→Euler, Heaviside→
  "heavy side", "why prime"→y′, "dee ex. Some"→"DXS", "this same"→"the same"); no narration changes.

## Chapter 2 · The rules, from first principles (ch2_rules)
State: **ready for final** (2026-11-03 19:33). Preview `out/ch2_rules_preview.mp4`, 12.6 min (755.9 s),
decodes end to end; `vk preview 2`: handover ok s1 → s2 and s3 → s4 (0.00%). Narration voiced and paced
(27 lines, 11.8 min); no narration changes (the producer accepted the 3 `vk qa 2` flags: Oiler→Euler,
"F/G prime"→F′/G′, "route"→"root", a homophone).
Gemini off until ~00:30, so skipped: `vk listen 2` (the ear check of all 27 lines) and the per-scene
`vk review`. Review was `vk check`, two holds rounds and the builders' `--frames` sheets (all 7 scenes).
- **Opening card (decided 18:45, for ch1 s7's end card):** the bare engine title card, as ch1's:
  `title_card("Part 2 · The rules, from first principles")` from `lib.titles` alone on screen, centred at
  ORIGIN, static (no updaters), parts `.title` ("Differentiation"), `.rule`, `.course` ("NST IA Mathematics
  · Lecture 12"), `.part`, nothing else in the frame. `load_scene("ch2_s1_hook").open_card()` returns
  exactly that. It is identical to ch1 s7's stand-in, so ch1 s7 can render now; the join is the same
  picture either way. s1's first frame is the card itself, fully drawn (no fade-in), exactly as ch1 s7
  ends on it (producer's join note, 18:55); s1 holds it to {last}. Form unchanged. **READY** (19:30,
  scenes/ch2_s1_hook.py): `open_card()` builds only the card (side-effect free); s1's first frame is it,
  fully drawn. ch1 s7: re-render against it if your render predates 19:30.
- **Reversed join out:** ch2 s7 ends on `load_scene("ch3_s1_hook").open_card()`, stand-in
  `title_card("Part 3 · Implicit differentiation and inverse functions")` until ch3 defines it.
- **Helpers ch2 exports** (planned; READY + exact parts added as each scene is built):
  - §4.2 derivative table, `load_scene("ch2_s2_table").table_card()`: ruled two-column card, header y | y′
    (y′ GREEN), three captioned blocks, e^{ax} GOLD, hyperbolic names white. For s1, s6, s7 and ch7 s2.
    **READY** (scenes/ch2_s2_table.py): `table_card()` parts `.header`, `.hrule`, `.blocks[i]` (each
    `.caption .rows .vrule .rule`), `.rows[0..8]` with `.lhs/.rhs` (`.h` row height); row 3 reads
    `\ln(ax) = \ln a + \ln x`. `row_glow(card, j)` = GREEN band behind row j at any scale. `euler_line()` =
    `e^{iax} = \cos(ax) + i\sin(ax)` (GOLD/PINK). `open_shot()` = s2's first frame (card at 0.9, top at
    y 3.7, header + block 1 caption/rules + the three left entries DIMMED).
  - (105), (106), (107) in one form, boxed like ch1's `definition_box()` (`.rect` YELLOW, `.formula`, `.num`
    DIM 28) plus `.tag` ("chain rule" / "product rule" / "quotient rule"): `ch2_s3_chain.chain_box()`,
    `ch2_s5_product.product_box()`, `ch2_s6_quotient.quotient_box()`. **READY** (105): `chain_box()`
    `.rect .formula .num .tag`, formula `.lhs .dfdu .dudx .du1 .du2` (df/du, du/dx GREEN), rect at ORIGIN;
    `bracket_line()` (`.eq .br1 .br2 .du .c2`); `small_diff_box()` = ch1's box at 0.45, DR buff 0.4, `.a`
    YELLOW. **READY** (106): `product_box()` (formula MathTex 44 with `.parts`); `framed_numerator()`,
    `strips_picture()`. **READY** (107): `quotient_box()` (`.formula.parts` = [d/dx(u/v), =, fraction]),
    `split_line(size=56)` (`.parts` = [u/v, =, u, ×, (1/v)]). All three tags: `T(<name>, 32, YELLOW)
    .next_to(rect, DOWN, buff=0.22)` (s5 and s6 changed to match s3 in round 1).
  - Sheet excerpt card (s7, H1 · H2), question-card style (ch3 s7 owns the style); ch7 reuses it.
    **READY** (scenes/ch2_s7_recap.py): `sheet_card()` = `load_scene("ch3_s7_recap").question_card("H1 ·
    H2", lines, width=12.4, size=48, indent=0.0, colors=…)`; lines: header "Examples Sheet I · answers on
    p. 15"; H1 (e) `\frac{d}{dt}\left(at + bt^2\sin\theta\right)`, (g) `\frac{d}{dy}\,\frac{1}{1+y}`; "H2
    write in exponentials:" then (a) sin x, (e) sinh x, (g) tanh x on one row (each with d/dx, verbatim from
    sheet p. 10), then (d) `\frac{d}{d\omega}\sin(-i\omega t)`. Parts `.frame .label .body .head .h1 .h2
    .page .t .y .theta .omega` (a list of two) `.i`. Excerpts only; the full H1/H2 cards are ch7 s1's.
- Music: `music/ch2.json`: Reflections (hook, START → c2.table.1), Gnomon (the product rule's rectangle,
  c2.prod.3:end → c2.prod.5), Clarity (recap + end card, c2.recap.1:end → END, swell after c2.recap.3).
- Build waves: s2, s3, s5 (18:50) → s1 (ends on s2's `open_shot()`, reversed handover), s4 (opens on s3's
  `handover_shot()`, (105) top-right), s6 → s7. Handovers: s1 → s2, s3 → s4; other joins fade to empty.
- Built 2026-11-03 18:50–19:30, all seven scenes by Claude scene-builders: s1 51.9 s, s2 161.2, s3 115.1,
  s4 83.1, s5 135.9, s6 120.8, s7 87.9 (s7 ends on ch3's READY `open_card()`, 8 s hold, 1 s fade).
- Review fixes: s3 ended on its live box (0.4% off s4's first frame), now swaps in a fresh `handover_shot()`
  (0.00%). Round 1 holds: s2 real-part connector at {pair} was TEAL (L12 keeps TEAL for the increment),
  now FG; s2 block-3 tag reworded "quotient rule, later in this part" (was "scene 6", brief updated);
  s5 and s6 rule-box tags matched to s3's (YELLOW 32), s5's stack lifted (tag 0.51 inside the edge);
  s6 tan(ax) line off the bottom edge (tan working clears at {tanh}), Example 39's tile row lifted 0.67
  inside. Round 2 holds: clean.
- Accepted check flags: small text in thumbnails and reduced references the briefs ask for (s1's table
  thumbnail 7–10 and dimmed left strip 15–24; s2's right-third table 17–27; ch1's differentiability box at
  0.45 in s3/s5, 13–17; the small (105)/(106) in s4/s6, 11–15; s6's returning table 17–24; s7's strip
  thumbnails, as ch1 s7). Dwell advisories are voice-driven (lines folded into the next one in s6
  c2.quot.2, s4 "ln undefined" 3.4 s cut by the clip clear, s1 "why?" 2.5 s handing over to the arrows,
  s2 "proof: part 3" 3.7 s, s5 δf δg corner 2.8 s as the brief's blink-and-fade).
- Departures accepted: s1 uses ch1's full `definition_box()` (with "= lim δy/δx"); s3's schematic starts big
  and shrinks to the top-left on {def}, only one TEAL copy flies into δu (the other flashes); s4 keeps (a)'s
  answer small during (b), tree terms fade in as their route lights; s5 mirrors clip 4 ((106) right,
  rectangle left), "= 0" above the frame; s6 colours sinh BLUE / cosh PURPLE in the tanh line (top/bottom
  roles), "top"/"bottom" labels 4 s early (`# early`); s7 shrinks each panel in place, then glides it to
  its slot (a direct shrink swept over filled slots).
- Glitches: none confirmed on frames (all seven builders' sheets clean). s2's minus → plus flip leaves a
  brief gap before the + fades in; s3's δu rewrite shows a half-rebuilt `f(u + δ) − f(u)` for a few
  frames as glyphs fade in (by design, not a jumble).
- Open: s7's second ω in H2(d) is recoloured YELLOW glyph by glyph and reads pale beside the PINK i at
  480p; check it on the final.

## Chapter 3 · Implicit differentiation and inverse functions (ch3_implicit)
State: **ready for final** (2026-11-03 19:25). Preview `out/ch3_implicit_preview.mp4`, 12.7 min (762.0 s),
decodes end to end; `vk preview 3`: handover ok s4 → s5 (0.00%); s7 ends on ch4's real `open_card()`.
Narration voiced and paced (27 lines, 11.8 min).
- **Opening card (decided 18:50, for ch2 s7's end card):** the bare engine title card, as ch1's and ch2's:
  `title_card("Part 3 · Implicit differentiation and inverse functions")` from `lib.titles` alone on screen,
  centred at ORIGIN, static (no updaters), parts `.title` ("Differentiation"), `.rule`, `.course` ("NST IA
  Mathematics · Lecture 12"), `.part`, nothing else in the frame. `load_scene("ch3_s1_hook").open_card()`
  returns exactly that, so ch2 s7's stand-in is the same picture. s1 fades it in from empty and holds it to
  {last}. **READY** (scenes/ch3_s1_hook.py, 18:58): `open_card()` is exactly that title card (no width
  rescale), static, at ORIGIN, parts `.title .rule .course .part`; s1 holds it 6.7 s then clears at {last}.
- **Reversed join out:** ch3 s7 (recap, built last) ends on `load_scene("ch4_s1_hook").open_card()`, no
  handover mark; stand-in `title_card("Part 4 · Leibniz's formula")` (ch4's record, 18:50) until then.
- **Question-card style (ch3 s7 owns it; ch5 s7, ch6 s7, ch7 reuse; planned, READY once s7 is built):**
  `load_scene("ch3_s7_recap").question_card(label, lines, width=9.4)` → VGroup centred at ORIGIN with
  `.frame` (RoundedRectangle, corner radius 0.2, DIM stroke width 2, no fill, ~9.4 wide = two thirds of the
  frame at hero size), `.label` (the sheet label, e.g. "H4", YELLOW, size 36, top left inside the frame,
  buff 0.35), `.body` (the sheet's text verbatim, white Tex size 30, left-aligned under the label, maths in
  `$…$` with course colours only inside the maths; one entry per line/part so parts can be lit or tagged).
  `h4_card()` → the H4 card (e^y GOLD) with `.i` and `.ii` as the two route lines; part seven reuses it.
  Until s7 exists, build a stand-in to this spec that switches to the helper once it is defined.
  **READY** (scenes/ch3_s7_recap.py, 19:16), as built (body size 40, not 30: 30 didn't read at hero size):
  `question_card(label, lines, width=9.4, colors=None, size=40, indent=0.6)` → VGroup at ORIGIN, `.frame`
  (corner 0.2, DIM stroke 2, no fill), `.label` (`T` 36 YELLOW, 0.35 in from the top-left edges), `.body`
  (one entry per item of `lines`; an item is one Tex line or a list of lines for a part that wraps,
  continuation lines indented 0.6); `colors` is a tex→colour dict, e.g. `{"e^y": GOLD}`. `h4_card()`
  ~9.4 × 4.9, extra parts `.q .i .ii .agree` (routes i and ii two lines each, sheet text verbatim).
- **Helpers ch3 exports** (planned; exact parts added as each scene is built):
  - Example 40's circle, `load_scene("ch3_s3_circle").circle_figure(...)`: equal-unit axes (x −3..5,
    y −3.5..3.5), BLUE circle centre (1, 0) radius 3; optional centre dot, dashed vertical at x = 2.8,
    YELLOW points (2.8, ±2.4), their two GREEN tangent lines, the two RED vertical tangent lines at
    x = −2 and 4. For ch3 s6 ({circle}) and the recap. **READY** (scenes/ch3_s3_circle.py, 19:05):
    `circle_figure(centre_dot=True, ticks=True, dashed=False, points=False, tangents=False,
    verticals=False)` → VGroup at a fixed place (centre (1, 0) at screen (−3.4, −0.4), 0.8 per unit),
    parts `.axes .xlab .ylab .circle .centre .ticks .dashed .p_top .p_bot .t_top .t_bot .v_left .v_right`
    (None when off); also `tangent_seg(ax, x0, y0, color=GREEN, length=2.6)`.
  - Ex 41's triangle and answer, `load_scene("ch3_s5_sign").triangle()` → VGroup at ORIGIN: right angle
    at bottom right, bottom side "1", right side "x", hypotenuse `\sqrt{1 + x^2}`, angle y at the left
    corner (YELLOW arc and y); parts `.tri .right_angle .one .x .hyp .arc .y`. `answer_box()` →
    VGroup(`.rect` YELLOW, `.formula` `\dfrac{dy}{dx} = \dfrac{1}{1 + x^2}`, dy/dx GREEN) at ORIGIN.
    For ch3 s6 ({use}) and the recap. **READY** (scenes/ch3_s5_sign.py, 19:08): `triangle()` ~4.6 × 3.1
    with labels (legs 3.2 × 2.2, MathTex 40), `.tri` BLUE stroke 4 fill 0.08, `.arc` YELLOW r 0.75;
    `answer_box(size=48)` ~3.3 × 2.0, `.rect` YELLOW buff 0.3 stroke 3, `.formula` 3 parts.
  - The swapped pair, `load_scene("ch3_s6_reciprocal").swapped_pair()`: Figure 29's curve and its mirror
    in the dashed y = x, TEAL slope triangles, readouts 3 and ⅓. For the recap. **READY**
    (scenes/ch3_s6_reciprocal.py, 19:12): ~10.6 × 6.5 at a fixed place (axes origin (−4.6, −3.3), 1.6 per
    unit, 0–3.7 both ways), parts `.axes .xlab .ylab .diag .diag_lab .orig .mirror .r3 .r13`; `.orig`/
    `.mirror` have `.curve .tangent .run_leg .rise_leg .right_angle .run_brace .run_lab .rise_brace
    .rise_lab .p_dot .q_dot`; also `picture(mirror, ax, chord)`.
- Music: `music/ch3.json`: Quantum Blue (hook, START → c3.implicit.1), Far Away (the reflection in
  y = x, c3.sign.5:end → c3.recip.2), Serendipity (recap + end card, c3.recap.1:end → END, swell after
  c3.recap.3).
- Voice QA: 6 Whisper flags accepted by the producer, no narration changes: "one-ten"/"one-eleven" →
  numerals (c3.implicit.3, c3.circle.5, c3.recip.1, false); "sign"↔"sine" (c3.sign.1, c3.sign.5) and
  "route"→"root" (c3.recip.4), homophones the screen disambiguates (the ± is on screen at "Which sign?").
- Gemini off until ~00:30: `vk listen 3` and the per-scene `vk review` are skipped; the Whisper vote,
  `vk check`, holds and builders' `--frames` sheets are the review.
- Built 2026-11-03 18:46–19:21, all seven by Claude scene-builders, in waves: s1–s4; then s5 (opens on s4's
  `handover_shot()`) and s6; then s7. Lengths: s1 63.5 s, s2 114.3, s3 136.9, s4 94.8, s5 132.8, s6 138.5,
  s7 81.1. s6 rendered after s5's helpers existed (s5 file 19:01, s6 render 19:07), so it shows the real
  triangle and box, not its stand-in.
- Review: `vk check`, three holds images, and `--frames` sheets: s3 and s7 from their builders; mine for s5
  (98.5/131.5 s), s2 ({chain}, {eq110}), s4 ({sine}, {so}), s6 ({swap}, {reflect}) and s7 ({h4}, {next}).
  Fixes: s3 the differentiability box at {finite} was 0.52 scale (text 16–20), now 0.8 over a cleared right
  column (text 24–26), gone by {strict}; s7 ch4's question now arrives at {next} (the frame was empty for
  ~3 s under "Next time, we differentiate again, and again"). s7's bottom margins measured ≥ 0.58 (the holds
  tile label had hidden them).
- Accepted check flags: s3 small text 24–26 in the differentiability box at {finite}–{strict} (a callback
  for "finite"; at 28 the box would be ~9.4 wide and cover the circle; ch1 accepted 26 for the same box),
  and the box covers the top of the RED x = 4 vertical for its 4.4 s. Dwell advisories everywhere are
  voice-driven: s1 title card 6.7 s and the rules strip (cleared at {circle}, as the brief asks); s2's
  per-word swaps and the (109)→(110) copies (0.0 s, not read); s3 readouts as they climb; s4 the margin
  multiplier 3.1 s; s5 the "most students slipped here" tag 2.5 s; s6 δx/δy 2.0 s before the flip (they
  return mirrored); s7 the r3 line 5.9 s.
- Departures accepted: no TransformFromCopy for text (studio rule): s2's (109) builds from a sliding copy,
  s3's "comes out of" lines flash the source and fade in, s4's sin⁻¹ flies and lands as sin; s1's rules
  strip is size 48 (not "small") and its dx/dy icon swaps top and bottom along an arc; s2 adds a DIM
  "Example" heading; s3's "Find the gradient." sits under the equation, readouts inside the circle; s5 adds
  `cos² y + sin² y = 1` (the voice says it) and draws ± as a split + over − so the halves take colours; s6
  rebuilds Figure 29 on equal units (ch1's figure29() is unequal) with a 3D flip about y = x, and puts
  dy/dx ≠ 0 beside the result; s7's route tags sit in a row under the H4 card, its question-card body is
  size 40, and its r3 panel drops s6's tiny δ labels.
- Open, minor: s6's TEAL chord and BLUE curve run close together near (1, 1) on equal units (hard to tell
  apart while the chord is up); s6 clip 1 leaves the middle of the frame fairly empty between the picture
  and the slope readouts.
- Glitches (frames): none confirmed as jumbles. s4 {so} (~87.6–88.0 s): the result 1/(1+x²)^{3/2} flying
  into the main line crosses the panel's vertical divider for ~0.3 s (a fly across a rule, not text;
  accepted). s4 {sine} (~19.2–19.6 s): the y =, sin⁻¹ and fraction copies separate from the question line
  and stack briefly mid-flight (the planned fly; accepted).

## Chapter 4 · Leibniz's formula (ch4_leibniz)
State: **ready for final** (2026-11-03 19:15). Preview `out/ch4_leibniz_preview.mp4`, 13.4 min (806.2 s),
decodes end to end; `vk preview 4`: handover ok s6 → s7 (0.00%), s8 unmarked (ends on ch5's card).
Narration voiced and paced (31 lines, 12.5 min).
- **Opening card (decided 18:45, for ch3 s7's end card):** the bare engine title card, as ch1's and ch2's:
  `title_card("Part 4 · Leibniz's formula")` from `lib.titles` alone on screen, centred at ORIGIN, static
  (no updaters), parts `.title` ("Differentiation"), `.rule`, `.course` ("NST IA Mathematics · Lecture
  12"), `.part`, nothing else in the frame. `load_scene("ch4_s1_hook").open_card()` returns exactly that,
  so ch3 s7 can use `title_card("Part 4 · Leibniz's formula")` as its stand-in now: the join is the same
  picture either way. s1 fades it in from empty and holds it to {last}. **READY** (scenes/ch4_s1_hook.py,
  18:55): `open_card()` is exactly that title card, parts `.title .rule .course .part`.
- **Reversed join out:** ch4 s8 (recap, built last) ends on `load_scene("ch5_s1_hook").open_card()`, no
  handover mark; stand-in `title_card("Part 5 · Hermite polynomials")` until ch5's director records it.
- **Helpers ch4 exports** (planned; READY + exact parts added as each scene is built):
  - Pascal's triangle, `load_scene("ch4_s3_pattern").pascal_triangle(n_max=3, start=0)`: rows numbered
    from 0 (row 0 is the single 1), entries YELLOW MathTex at a fixed horizontal pitch so a row added later
    lines up; `.rows[k][m]` is row k, place m. `pascal_row(n)` builds any row (e.g. row 4 for ch5 s4, row 5
    for ch7 s5) in the same style. s3 shows rows 1–3 (`start=1`, as on her board); s4 adds row 0; from s4 on
    (s7, recap, ch5 s1) the series' triangle is rows 0–3.
    **READY** (scenes/ch4_s3_pattern.py): `pascal_triangle(n_max=3, start=0, size=44)` → VGroup of rows,
    `.rows[k][m]` YELLOW MathTex (`.rows[k]` None for k < start), `.pitch`, `.size`; apex (row 0's place) at
    ORIGIN, row k at y = −0.7k, entry m at x = (m − k/2)·0.8 (pitch widens only for 3-digit rows).
    `pascal_row(n, size=44, pitch=None, like=None)`: with `like=tri` it is built in that triangle's moved/
    scaled frame, so ch5 s4 grows row 4 with `r = pascal_row(4, like=tri); tri.rows.append(r); tri.add(r)`.
    `board_lines(size=44, gap=0.85)` → `.lines[0..2]` (y′, y″, y‴), each with `.lhs .eq .terms .coefs .plus`.
  - Leibniz sum card, `load_scene("ch4_s4_formula").leibniz_card()`: `(fg)^{(n)} = \sum_{m=0}^{n}
    \binom{n}{m} f^{(n-m)} g^{(m)}`, f BLUE, g PURPLE, the binomial YELLOW, one object with addressable
    parts (lhs, sum sign, binomial, f-part, g-part). For s5–s7, the recap, ch5 (s1, s4) and ch7 s5.
    **READY** (scenes/ch4_s4_formula.py): `leibniz_card(size=56)` → VGroup at ORIGIN, parts `.lhs`
    `(fg)^{(n)}` (f BLUE, g PURPLE), `.eq`, `.sum` `\sum_{m=0}^{n}` (FG), `.binom` (YELLOW), `.fpart`
    `f^{(n-m)}` (BLUE), `.gpart` `g^{(m)}` (PURPLE); `.tex[0..5]` the same in order. s4 shows it at size 68.
    Also `prime_slots(n, m=None, picks=None, side=0.8, pitch=1.0)` (`.slots[i]` = (box, prime), `.boxes`,
    `.primes`; picks PURPLE, rest BLUE).
  - x³ chain card extended, `load_scene("ch4_s2_higher").chain_card()`: ch1 s3's `cube_card()` styling,
    `x^3 \to 3x^2 \to 6x \to 6 \to 0` (x³ BLUE, derivatives GREEN). For the recap and ch6 s4.
    **READY** (scenes/ch4_s2_higher.py): `chain_card()` → VGroup(`.frame`, `.expr`), expr = MathTex("x^3",
    "\to","3x^2","\to","6x","\to","6","\to","0","\to","0,\,0,\,0,\,\dots", font_size=44), x³ BLUE,
    derivatives GREEN, arrows FG, last arrow + tail DIM; `.terms[5] .arrows[4] .tail`; frame as `cube_card()`
    (RoundedRectangle corner 0.15, 0.3 padding, no fill), ~4.6 wide at ORIGIN; `chain_frame(card, k)` is the
    frame round terms 0..k. Also `notation_card()` (f^{(n)} = dⁿf/dxⁿ, f^n "a power" DIM, f^{(0)} = f) and
    `power_contrast(with_label=False)` (GREEN 6x, RED ≠, RED (3x²)² = 9x⁴).
- Narration: c4.pascal.4 sentences 2 and 4 rewritten for the ear ("two end terms"/"the end terms" were
  heard as "n terms" by all three Whispers) to "two outer terms"/"the outer terms"; c4.pascal.5's last
  sentence follows ("the ones at the ends are the outer terms") so the wording stays one term. Re-voiced.
  Accepted Whisper flags: c4.pattern.2 "F prime"→F', "G prime"→G' (notation, false).
- Music: `music/ch4.json`: Spirals (hook, START → c4.higher.1), Hypothesis (the Pascal reveal,
  c4.pattern.2:end → c4.pattern.4), Endpoint (recap + end card, c4.recap.1:end → END, swell after
  c4.recap.2).
- Gemini off until ~00:30: `vk listen 4` and the per-scene `vk review` are skipped; the Whisper vote,
  `vk check`, holds and builders' `--frames` sheets are the review.
- Waves: s1–s6 in parallel (18:47; owners define helpers first, dependents wait on them), then s7 (opens
  on s6's `handover_shot()`) with s8 (recap, ends on ch5's opening card).
- Built 2026-11-03 18:47–19:12, all eight scenes by Claude scene-builders: s1 69.1 s, s2 100.9, s3 111.9,
  s4 101.5, s5 96.5, s6 129.0, s7 137.9, s8 59.2 (narration 12.5 min). Handover s6 → s7 0.00%.
  s1's {last} thumbnails are ch3's real `circle_figure(dashed=True, points=True, tangents=True)` and
  `swapped_pair()` (trimmed of its δ pieces in ch4's `_trim_pair()`; ch3 untouched). s8 ends on
  `load_scene("ch5_s1_hook").open_card()` (defined; same picture as the stand-in) and takes the
  recursion from ch5 s5's public `boxed_recursion()[0]`, H_n from ch5 s2's `def_line()`.
  Other helpers: s1 `question()`, `doubling_tree(levels)`, `counter_1024()`, `product_rule()`; s5
  `answer_box()`, `row_last3()`; s6 `dominoes()`, `topple()`; s7 `linked_rows(labels, heads, y3)`.
- Review (Gemini off): `vk check`, two holds rounds, builders' `--frames` sheets. Round 1 fixes: s1 uses
  ch3's real figures (were stand-ins; ch3 landed mid-build); s2 c4.higher.4's dimmed context was invisible
  (a family-opacity bug in its dim helper wiped the formulas, leaving empty frames), now ~0.45; s7 {add}
  merged line centred then rises on {pascal}, triangle ×1.3 with the V arrows clear of the digits, the
  count one line "3 + 3 = 6 = C(4,2)" off the bottom edge, the {done} result and s4's card at 54 (were 37
  in an empty frame); s8 no longer imports ch5's private `_result_eq()`. s6's domino labels checked on
  full-size frames: clear of the fallen tiles, no change.
- Accepted check flags: small text in s1's thumbnails (ch3's axis labels, 21–26), s2's dimmed context at
  c4.higher.4 (17–21, background), s8's 2×2 recap grid (21–25, the brief's thumbnails of each panel) and its
  dimmed strip after {next} (8–13, decorative). Dwell advisories are voice-driven: s1 title card 2.9 s (the
  brief holds it to {last}), counter ticks 2/4 and s4's 1/2 count (replaced on purpose), s3 "?" 2.1 s and
  row ten 5.6 s, s4 "· France" 2.1 s, s5 0.5–2 s short, s6 (114) 9.0 s (its halves stay as the two sums),
  s7 "the outer terms" 3.6 s (last words, 3.5 s hold).
- Departures accepted: s2's strip keeps only the recursive formula; s3's coefficients move into the
  triangle (copies crossed their sources); s4 numbers places under row 3 only and slides the y″ line in
  under the simplified line; s5 no strike on "…", the 1024 counter lands on "thousand"; s6's top lines
  continue with a bare "=" once (fg)^{(n+1)} has left; s7's m = 0 box drops into the bottom row, mirrored;
  s8 drops s7's product heads and y‴ line from panel 4, its Leibniz card sits under the board lines.
- Glitches: none confirmed on frames (no Gemini motion review; builders' `--frames` sheets for s1, s2,
  s6, s7, s8 clean).
- Gemini checks skipped (quota until ~00:30): `vk listen 4` (all 31 lines) and the per-scene `vk review`
  of all eight scenes. The producer's `vk finalize` transitions pass is the only Gemini look at motion.

## Chapter 5 · Hermite polynomials (ch5_hermite)
State: **ready for final** (2026-11-03 19:45). Preview `out/ch5_hermite_preview.mp4`, 10.7 min (641.9 s),
decodes end to end; `vk preview 5`: handovers ok s1 → s2 → s3 → s4 → s5 → s6 (all 0.00%); s7 ends on ch6's
real `open_card()` (READY, so no stand-in left). Narration voiced and paced (26 lines, 9.8 min).
- **Opening card (decided 18:58, for ch4 s8's end card):** the bare engine title card, as ch1–ch4 and ch6:
  `title_card("Part 5 · Hermite polynomials")` from `lib.titles` alone on screen, centred at ORIGIN, static
  (no updaters), parts `.title` ("Differentiation"), `.rule`, `.course` ("NST IA Mathematics · Lecture
  12"), `.part`, nothing else in the frame. `load_scene("ch5_s1_hook").open_card()` returns exactly that,
  so ch4 s8's stand-in `title_card("Part 5 · Hermite polynomials")` is already the same picture. s1 fades it
  in from empty and holds it to {last}. **READY** (scenes/ch5_s1_hook.py): `open_card()` is exactly that
  title card, parts `.title .rule .course .part`. s1 ends on s2's `open_shot()` (handover verified).
- **Reversed join out:** ch5 s7 (recap, built last) ends on `load_scene("ch6_s1_hook").open_card()`, no
  handover mark; stand-in `title_card("Part 6 · Stationary points")` (ch6's record, 18:55).
- **Helpers ch5 exports** (planned; READY + exact parts added as each scene is built):
  - Definition line, owner s2. **READY** (scenes/ch5_s2_define.py, 19:10): `load_scene("ch5_s2_define").def_line()`
    = one MathTex 44, `H_n(x) \equiv (-1)^n e^{x^2} \frac{d^n}{dx^n}\Big(e^{-x^2}\Big)`, centred (−0.8, 3.0)
    (spans about x −3.8..2.2, y 2.5..3.5); parts (sub-mobjects of it) `.lhs` H_n(x), `.equiv` ≡, `.sign`
    (−1)^n, `.front` e^{x²} GOLD, `.dn` dⁿ/dxⁿ, `.lpar` (, `.gauss` e^{−x²} PURPLE, `.rpar` ). Static, never
    changed in s2. Room for one strip line under it: y ≈ 1.9–2.3, x ≤ 2.6 (left of the ladder card). The
    top-right corner (x > 3.1, y > 1.85) is free for ch4's parked Leibniz card. Colour helper `mtex(*parts,
    size, color)` (parts holding e^{x^2} GOLD, e^{-x^2} PURPLE).
  - H_n ladder card, owner s2. **READY**: `load_scene("ch5_s2_define").ladder_card(k)`: box x 2.7..6.6,
    y −3.7..1.75 (DIM rounded rect); `.box`, `.heading` ("H_n ladder", H_n YELLOW, y 1.3), `.rungs[j]`
    j = 0..4 bottom-up at y = −3.2 + 0.98 j, each VGroup with `.bar` (DIM line under it), `.label` (MathTex
    34 `H_j`, YELLOW), `.eq` ("="), `.value` (`rung_value(j)`; None while empty), `.slot` (DIM dashed line;
    None once filled). Rung j filled iff j < k; empty rungs have label and "=" at opacity 0.4. Values FG
    MathTex 34, left edge x 3.95: `1`, `2x`, `4x^2 - 2`, `8x^3 - 12x`, `16x^4 - 48x^2 + 12` (scaled to fit
    the card if wider than 2.45). To fill rung j: `rung_value(j)` builds the value already in place;
    restore that rung's label/eq to opacity 1 and drop its slot (ladder_card(j+1) is the result).
    `open_shot()` = VGroup(def_line()) (s1 ends on it). `handover_shot()` = VGroup(def_line(),
    ladder_card(3)), s2's last frame (s3 opens on it).
  - Boxed recursion, owner s5: **READY** `load_scene("ch5_s5_assemble").boxed_recursion()` = VGroup(eq, box,
    caption): eq MathTex 48, parts 0 `H_{n+1}` 1 `=` 2 `2` 3 `x` (BLUE) 4 `H_n` 5 `-` 6 `2` 7 `n` 8 `H_{n-1}`,
    at (≈−2.1, 1.75) (top-centre of the area left of the ladder, under the def line); box YELLOW
    RoundedRectangle (corner 0.15, stroke 2.5, pad 0.35/0.3); caption MathTex `n \ge 1` 36 right of the box.
    For s6, the recap, ch6 s1.
  - Example 42 mini card, owner s5: **READY** `load_scene("ch5_s5_assemble").example42_mini()` = VGroup(border,
    header, claim): border RoundedRectangle corner 0.15, GREEN stroke 3, BG fill; header T 32 GREEN "Example 42:
    Hermite polynomials"; claim = VGroup(T 30 "Show that the recursion relation", VGroup(MathTex 36
    `H_{n+1} = 2xH_n - 2nH_{n-1}`, T 30 "holds.")); built at ORIGIN, ~6.4 × 2.4. s1: match this styling.
  - s5 shots: **READY** `open_shot()` = VGroup(def_line, ladder_card(3), strip, two_term) (strip MathTex 44
    `= 2(-1)^n e^{x^2} d^n/dx^n \Big(x e^{-x^2}\Big)` at (xc, def bottom − 0.85); two-term MathTex 44
    `= n d^{n-1}/dx^{n-1} e^{-x^2} + x d^n/dx^n e^{-x^2}` 0.5 under it; s4 lands on it).
    `handover_shot()` = VGroup(def_line, ladder_card(3), boxed_recursion()) (s6 opens on it).
  - Oscillator plots, owner s6: **READY** `load_scene("ch5_s6_ladder").osc_plots()` = VGroup(*rows, caption):
    `.rows[n]` n = 0..3 bottom-up, each VGroup(base, curve, label) with `.base` (DIM line), `.curve` (BLUE
    H_n(x)e^{-x^2/2}, unnormalised, same height 0.55, x -4..4 at 1 unit/unit), `.label` (MathTex 34 "n = k")
    and `.dots` (YELLOW zero crossings, NOT in the group); `.caption` MathTex 44 `H_n(x) e^{-x^2/2}`
    (e^{..} PURPLE) at y 3.3. Centred x 2.2, base lines at y -2.55 + 1.5 n; spans x -2.8..6.2. Same curves
    and stacking as s1's preview. s6 also leaves the ladder at scale 0.88, centre (-4.95, -0.7), with all 5
    rungs filled (ladder_card(5)); scene ends empty.
  - I1 question card, owner s7: **READY** (scenes/ch5_s7_recap.py): `load_scene("ch5_s7_recap").i1_card()`
    = ch3 s7's `question_card("I1", …)`: DIM rounded frame 9.4 wide, YELLOW "I1" top left, Tex 40 body
    verbatim (sheet p. 11, "Leibniz's"), e^{-x^2/2} PURPLE, built at ORIGIN (~3.5 tall); parts `.frame`
    `.label` `.body` (4 Tex lines; `.body[3]` is the differential equation). s7 shows it scaled 0.88 at
    the top. For ch7 s5.
- Plan (joins): s1 → s2 → s3 → s4 → s5 → s6 are handovers (the definition line stays at the top and the
  ladder at the right throughout); s6 → s7 fades to empty. Reversed inside the chapter where the later
  scene is built first: s1 ends on s2's `open_shot()`, s4 ends on s5's `open_shot()`.
- Waves: s2, s5 (18:58; s5 waited on s2's helpers), then s1, s3 (19:02, ch4's card and triangle READY),
  s6 (on s5's shot), s4 (on s3's and s5's shots), then s7. All seven by Claude scene-builders, 18:58–19:37:
  s1 68.5 s, s2 105.5, s3 83.2, s4 117.9, s5 87.1, s6 109.5, s7 70.1.
- Departures from the brief (accepted): ch4's sum card and triangle leave at the end of s1's hook instead
  of staying parked through s2–s3; s3 brings the card back small in the top-right corner on {leibniz}
  and s4 flies it to the centre. s4's unrolled sum is two lines (one row doesn't fit left of the ladder).
  s5/s6 use flies instead of TransformFromCopy (check flags copies on their source). s6: the notes' box
  replaces the boxed recursion at the top for c5.ladder.2–3; ladder grows only ×1.05. s7: r4's ladder
  and box are compact rebuilds in the same style (`ladder_card(5)` at quarter size came out at 15).
- Review (Gemini off): `vk check`, two holds rounds, builders' `--frames` sheets (read: s2). Round 1
  fixes: s2 the flying 2x (one mover, no ghost) and the values into the ladder (one at a time from H_0,
  no crossing), colour pulse instead of FlashAround on a lone glyph; s3 the sign row raised to hero size
  (was 48 on the bottom edge); s4 bottom lines inside the margin, Pascal's triangle ~28 → ~36; s5 the
  assembled H_{n+1} line held centred at hero size through c5.build.1 (centre was empty); s6 parity tags
  white/YELLOW (were TEAL/PINK, reserved colours). Round 2 holds clean.
- Accepted check flags: s4 c5.leib.4 transition overlap, the handwritten "n" over the notes' printed 0 in
  the inset (the brief asks for the overwrite). Dwell advisories are voice-driven: s1 title card 5.3 s
  (held to {last}) and "quantum mechanics" 1.9 s (leaves on {define} as briefed); s2–s7 working lines
  replaced on their spoken cues (2–7 s).
- Glitches (confirmed on frames, fixed): s2 ~44.4 s, the "2x" flying into the H_1 cell showed a doubled
  glyph (a fly over a fading in-row copy); s2 ~101–102 s, the three H values crossed while sliding into
  the ladder together (table top-down order inverted to bottom-up rungs, simultaneous moves).
- Gemini checks skipped (quota until ~00:30): `vk listen 5` (the ear check of all 26 lines) and the
  per-scene `vk review`; the Whisper vote, `vk check`, holds and the `--frames` sheets were the review.
- Narration: c5.ladder.3 "One more rung." → "One more step up the ladder." (all three Whispers heard
  "round"); re-voiced, QA clean. Accepted: c5.leib.4 "two are left" → "two were left" (base, small; minor).
- Music: `music/ch5.json`: Orbit (hook, START → c5.def.1), Quaternions (the oscillator plots,
  c5.ladder.3:end → c5.recap.1), Focal Point (recap + end card, c5.recap.1:end → END, swell after
  c5.recap.3).

## Chapter 6 · Stationary points (ch6_stationary)
State: **ready for final** (2026-11-03 19:20). Preview `out/ch6_stationary_preview.mp4`, 11.9 min
(715.4 s), decodes end to end; `vk preview 6`: handover ok s1 → s2 (0.00%). s7's end card is the stand-in
`title_card("Part 7 · Solutions: Examples Sheet H1, H2, H4 and I1")` (no "Bonus" tag) until ch7 defines
`ch7_s1_intro.open_card()`; it switches by itself then: re-render s7 (`vk check ch6_s7_recap
--render-anyway`, r3's accepted small text) and re-check the join. Narration voiced and paced (26 lines,
11.1 min).
- **Opening card (decided 18:55, for ch5's recap end card):** the bare engine title card, as ch1's, ch2's
  and ch4's: `title_card("Part 6 · Stationary points")` from `lib.titles` alone on screen, centred at
  ORIGIN, static (no updaters), parts `.title` ("Differentiation"), `.rule`, `.course` ("NST IA Mathematics
  · Lecture 12"), `.part`, nothing else in the frame. `load_scene("ch6_s1_hook").open_card()` returns
  exactly that, so ch5's recap can use `title_card("Part 6 · Stationary points")` as its stand-in now: the
  join is the same picture either way. s1 fades it in from empty and holds it to {last}. READY once
  scenes/ch6_s1_hook.py is built (marked here).
- **Reversed join out:** ch6 s7 (recap, built last) ends on `load_scene("ch7_s1_intro").open_card()`, no
  handover mark; stand-in `title_card("Part 7 · Solutions: Examples Sheet H1, H2, H4 and I1")` (ch7's
  script also wants a small "Bonus" tag) until ch7's director records its card here.
- **Helpers ch6 exports** (planned; READY + exact parts added as each scene is built):
  - The notes' stationary-point figure (p63), owner s1: `load_scene("ch6_s1_hook").notes_figure()`: faint
    axes and one BLUE curve, y′ = (x + 2)(x + ½)(x − 3/2)² (y = x⁵/5 − x⁴/8 − 17x³/12 + 21x²/16 + 9x/4,
    x ≈ −2.6..2.5), five YELLOW dots (peak x = −2, valley −½, bends ≈ −1.43 and 0.31, flat 3/2), full size
    at a fixed place, no labels. **READY** (scenes/ch6_s1_hook.py, 19:05): `notes_figure()` → `NotesFigure`
    VGroup, static: `.axes` (DIM, opacity 0.55, no ticks/tips, x −2.8..2.7 over 11.4 wide, y −2..6.6 over
    4.9 tall, centred at 0.15·UP), `.curve` (BLUE, stroke 6, x −2.6..2.5), `.dots` (YELLOW r 0.11) in order
    `.peak .valley .bend1 .bend2 .flat`; `.at_x(x)` the curve point; module `curve_y(x)`, `PEAK_X` etc.
    `open_card()` READY as above. s1 → s2 is a handover (`handover_shot()`: `.fig .qs .question .row
    .odd .even`).
  - The labelled figure, owner s2: `load_scene("ch6_s2_vocab").labelled_figure()`: s1's figure with the
    notes' labels and arrows ("local maximum", "local minimum", "point of inflection" with two arrows,
    "(rising) stationary point of inflection") and the y″ sign strip (− + − +) under it, as s2 ends. For
    s6, the recap, and ch7 s1 (small) and ch7's recap. **READY** (scenes/ch6_s2_vocab.py, 19:10): static
    VGroup, full size at s1's place: `.fig` (= `notes_figure()`), `.dots` (= `.fig.dots`), `.labels` with
    `.lmax` (text, arrow), `.lmin` (text, arrow), `.inflect` (text, arrow to bend1, arrow to bend2), `.rising`
    (two-line text, arrow), each also on the figure directly; `.strip` with `.ylab .signs` (4 MathTex) `.dashes`
    (3 DashedLine) `.flips` (3 MathTex). Excludes the DIM spelling note. For a small copy without the strip:
    `f = labelled_figure(); f.remove(f.strip)`, then scale.
  - **READY** (19:10–19:20): s3 `cubic_graph(dots=False)` (`.axes .xlab .ylab .curve .name`, `.max_dot
    .min_dot`), `umbrellas()` (`.left .right`, `.bowl .bowl_rain .pool .bowl_tex .bowl_lab .cap .cap_rain
    .cap_tex .cap_lab`); s4 `figure30()` (`.cube .quart`, each `.axes .xlab .ylab .curve .tan .dot .lab`),
    `chain_cards()` (`.cube .quart`, each `.frame .expr .vals .ring`; x³'s card built in s4 to ch4's spec,
    not imported from ch4_s2_higher, which didn't exist yet); s5 `power_panels()` (`.p2 .p3 .p4`, each
    `.line .curve .dot .title .signs`); s6 `three_graphs()` (`.heading`, `.left .middle .right`, each `.axes
    .curve .name .dot .tan .info .word .down .up`; `.same`).
  - y = x³ − 3x graph (s3, returns in s6 as the falling inflection), Figure 30 pair and the x³/x⁴ chain cards
    (s4; x³'s card from ch4's `chain_card()`), the umbrella pair (s3), the (δx)ⁿ panels (s5), the three
    inflection graphs y = x³ + x, x³, x³ − 3x (s6): for the recap.
- Music: `music/ch6.json`: Resonance (hook, START → c6.vocab.1), Fractals (the umbrella,
  c6.second.3:end → c6.higher.1), Far Away (recap + end card, c6.recap.1:end → END, swell after
  c6.recap.2).
- Gemini off until ~00:30: `vk listen 6` and the per-scene `vk review` are skipped; the Whisper vote,
  `vk check`, holds and builders' `--frames` sheets are the review.
- Narration rewritten for the ear (re-voiced, Whisper vote clean after): c6.second.4 "The lecturer's memory
  aid is an umbrella." → "As a memory aid, the lecturer uses an umbrella." (all three Whispers heard
  "lecture's"); c6.vocab.2 "The valley is a local minimum" → "And the valley is…" (heard "DeValley");
  c6.nonstat.3 "All three have the same second derivative" → "All three share…" (heard "three of the").
  Accepted: c6.recap.2 "seven: worked solutions" → "7, work solutions" (producer: minor). Not heard by
  Gemini (`vk listen 6` skipped).
- Built 2026-11-03 18:58–19:10, all seven by Claude scene-builders: s1 51.3 s, s2 98.6, s3 113.0, s4 130.5,
  s5 132.9, s6 115.3, s7 73.7. Waves: s1, s3, s4, s5 → s2 (opens on s1's `handover_shot()`) → s6 (opens on
  s2's `labelled_figure()`) → s7. Handover s1 → s2 0.00%. Other joins fade to empty.
- Review (Gemini off): `vk check`, two holds rounds, `--frames` sheets around the riskiest plays (s3's
  y″ > 0 → y″ = 6x edit, s4's x⁴ ↔ −x⁴ flip, s5's (113) → Taylor rewrite and the general-term rewrite).
  Round 1 fixes: s2 sign-strip flips lifted inside the 0.5 margin (the bend1 flip was hidden only under
  the beats caption); s3 the umbrella's rain pool FG/grey (was TEAL, which L12 keeps for δx and h); s5
  the (δx)ⁿ panel labels all YELLOW (minimum was GREEN, maximum RED); s4 the curve no longer sweeps
  through its name during the flip (round 2).
- Accepted check flags: s7 small text 24 in r3's two chain cards (thumbnails of s4's cards beside tiny
  graphs, as ch1's recap accepted); dwell advisories driven by the brief's clears (s1 title card 6.0 s and
  the ch5 callback 5.1–5.9 s, cleared at {figure}; s2 `v = 0` 1.3 s and concave-down panel 2.3–3.3 s,
  cleared at {three}/{strip}, the DIM spelling note 7.8 s at the scene's end; s3 "maximum" 2.2 s before the
  umbrellas; s4 the −x⁴ state 3.9 s between {flip} and {two}; s5 the running δx/gap readout; s6 the y″ = 0
  labels 4.0 s and the small x³ panel 3.6 s; s7 r5's line 6.9 s).
- Departures accepted: s1 flashes y″ in the derivative row for {zero} (no "= 0" written); s1 builds the
  ch5 box and ladder callback itself (ch5's scenes didn't exist yet); s2's labels sit near, not exactly at,
  the notes' p63 places (max label up-left of the peak, the rising label above the flat spot, so the sign
  strip stays clear); s4 negates the whole x⁴ chain for −x⁴, and builds x³'s chain card itself to ch4's
  spec (not imported from ch4_s2_higher); s5 trims Figure 29's labels (δy short form, no "tangent" label);
  s6 colours the concavity labels as the sign strip does (concave down RED, up GREEN, chapter-wide); s7
  trims its thumbnails (r1 without labels or strip, r2 and r5 without their sub-labels).
- Glitches (from `--frames`, Gemini off): s4 {flip} ≈ 89.6 s and flip back ≈ 95.0–95.3 s, the x⁴ panel's
  curve sweeping through its "y = x⁴" label (Transform of curve and label together): fixed in round 2.
  Accepted: s5 {first} ≈ 68.2–68.5 s, the (δx)³/3! term reads "(δx) ! y (x₀)" for ~0.4 s while the
  edit fades the 3s out before the n's fade in; s3 {check} ≈ 71.1–71.4 s, "y″" alone between "> 0" and
  "= 6x" (the same two-step edit, reads cleanly); s5 the δx/gap readouts outlive Figure 29 by ~1.5 s.
- Gemini checks skipped: `vk listen 6` and the per-scene `vk review` (7 scenes).

## Chapter 7 · Solutions: Examples Sheet H1, H2, H4 and I1 (ch7_solutions, bonus)
State: **ready for final** (2026-11-03 19:58). Preview `out/ch7_solutions_preview.mp4`, 11.4 min (684.2 s),
decodes end to end; `vk preview 7`: handover ok s1 → s2 and s3 → s4 (0.00%), s6 unmarked (ends the
lecture on the "Next lecture" end card). Narration voiced and paced (24 lines, 10.6 min). Scenes 6/6
(Opus); fix passes s2, s4; two review rounds (check + holds), no Gemini.
- **Opening card (decided 19:20, for ch6 s7's end card):** the bare engine title card, as ch1–ch6:
  `title_card("Part 7 · Solutions: Examples Sheet H1, H2, H4 and I1")` from `lib.titles` alone on screen,
  centred at ORIGIN, static (no updaters), parts `.title` ("Differentiation"), `.rule`, `.course` ("NST IA
  Mathematics · Lecture 12"), `.part`, nothing else in the frame (no width fitting; `.part` at size 36
  fits). `load_scene("ch7_s1_intro").open_card()` returns exactly that, so ch6 s7's stand-in
  `title_card(PART7)` is already the same picture. The "Bonus" tag is NOT on the card: s1's first frame is
  the card itself, fully drawn, and the GOLD "Bonus" tag (L11 part 7's: T 30 GOLD in a GOLD
  RoundedRectangle, corner 0.15, stroke 2, fill 0.12, under `.part`) joins it as "a bonus" is spoken.
  **READY** (scenes/ch7_s1_intro.py, 19:25): `open_card()` is exactly that title card (`.part` 11.79
  wide, under ch6's 12.6 fit, so ch6 s7's stand-in is the same picture); s1's first frame is it.
- **Helpers ch7 s1 exports** (READY, 19:25): `open_card()`, `pause_icon()`, `h1_card()`, `h2_card()`
  (verbatim, `question_card` style, ~9.4 × 6.5/6.7, parts `.frame .label .body .intro .parts`), `h4_card`
  and `question_card` (from ch3 s7), `i1_card()` (stand-in that switches to ch5_s7_recap's once defined),
  `CARD_MAKERS`, `card_row(lit)` (lit True/False or a set of indices), `handover_shot()` (the lit row).
  To grow a card: `Transform(row[i], h1_card().move_to(...))`.
- Ends the lecture: s6 (recap) ends on the house end card, no handover mark.
- Reuses (all READY unless noted): ch3 s7 `question_card()` and `h4_card()`; ch5 s7 `i1_card()` (NOT yet
  built: s1 uses a stand-in to the same spec that switches by itself; s5 is built last); ch6 s2
  `labelled_figure()`; ch2 s2 `table_card()`/`row_glow()`; ch2 s6 quotient rule; ch3 s6 `swapped_pair()`;
  ch4 s4 `leibniz_card()`, ch4 `pascal_row()`; ch5 s4's two-term step (NOT yet built). H1 and H2 cards
  are built in ch7 s1, verbatim, in ch3 s7's style (ch2 s7's excerpt card is not used).
- Narration rewritten and re-voiced (19:22), both QA clean: c7.i1.3:2 "and G prime has used one" →
  "and G prime already takes care of one" (all three Whispers heard "is used"; the phrase read oddly);
  c7.intro.1:1 "solutions to the sheet questions this lecture covers" → "solutions to the questions from
  the examples sheet that this lecture covers" (small, medium heard "the chic questions"); c7.intro.1:3
  "If you haven't tried" → "If you have not tried" (ear rule: no negative contractions, it flips the
  meaning). Accepted (producer, COURSE.md false flags): "shine" → sine, "cosh" → cos/cash/cush, "why
  prime" → y', "minus sine" → "sign", "row N" → "rho n" (the screen shows the row).
- Music: `music/ch7.json`: Centroid (hook, START → c7.basics.1), Transformation (H4's curve and vertical
  tangent, c7.h4two.4:end → c7.i1.1), The 3Blue1Brown Experience (recap + end card, c7.recap.1:end → END,
  swell after c7.recap.2). None used elsewhere in L12.
- Joins: s1 → s2 and s3 → s4 are handovers (s1's lit card row; route i's small boxed answer + small H4
  card); every other join fades to empty. s3 and s5 open from empty on s1's `card_row(lit=True)` and grow
  their card from it. Waves: s1 + s3 (19:24; s3 waits on s1's helpers), then s2 and s4, then s5 (once
  ch5 s7's `i1_card()` and ch5 s4 exist) and the recap. s1 19:25, s3 19:31, s4 19:39 built; s5 launched
  19:40 (ch5 s7's `i1_card()` defined by then; ch5 s4 has no step helper, s5 rebuilds it small).
- Built departures: s1 the row cards are scaled copies of the full cards, bodies size 11–13 as texture,
  labels size 32 (accepted small-text flag; also in s2, s3, s5 while the row shows); H3/H5 and their tag
  come in together on {later}. s3 the small H4 card is compact (frame, "H4", the agree line: the full
  card shrunk read at ~15); the {recip} flip is a swap in place (a fly crossed text); the swapped pair
  is shown without its δ labels and readouts. s4 {same} flies route i's GREEN box (not a text morph:
  it overlapped the bracket's own copy); tops and the wrong answer flash at source and fade in at the
  target; the cube-root picture is rebuilt small (`cube_root_pic()`, ch3 has no helper for it).
- Recap helpers: s2 `ticked_table()`, `sin_line()`, `variable_tags()`; s4 `answers_pair()`,
  `answer_ii_group()`, `squared_eq()`, `ey_good()`, `ey_struck()`; s5 `leibniz_n1()`, `survivor_last()`,
  `survivor_before()`, `survivors_shot()`. s2, s5 built 19:44–19:47; recap launched 19:48.
- Review round 1 (19:50, holds s1–s5; Gemini off): fix passes s2 (table's last rows at the frame's
  bottom edge, the slip tag against the tick column, sinh/cosh exponentials uncoloured) and s4 (route ii
  label styled unlike s3's route i label); s3 re-rendered (render was older than its file).
- Accepted check flags: small text in s1's card row (bodies 11–13 as texture, labels 32; also while
  the row shows at the start of s2, s3, s5) and s2's §4.2 table (entries 25, captions 17: the brief
  wants it small beside the working); dwell advisories where the voice moves on (row cards fading at
  0.9 s as the hero grows; working lines replaced on their cues).
- Round 2 (19:56, check + holds of all six): s2's table now 6.6 tall inside the frame and the slip tag
  1.5 clear of the tick column (the sinh/cosh exponentials were already GOLD/PURPLE); s4's route ii label
  now TEAL "route ii:" + white, size 32, as s3's. Nothing new. Recap accepted as built: departure from
  the brief, each callback shown large in the centre on its sentence with its line, then shrunk into
  its panel in a row of five along the top (five panels in a row from the start put the text at size
  6–25); r5 leaves with everything on {next}, so the fifth panel stays empty; r2's YELLOW tags come in
  ~2.6 s before "variable" (otherwise up ~1 s); captions for r1/r3/r2 up 5.0/5.6/2.9 s (short sentences);
  thumbnails' small text accepted. End card: "Next lecture: curve sketching (§4.11)", ch6's labelled
  figure (no strip), dim H3/H5 cards, held 7.5 s, 1 s fade.
- Glitches: none confirmed on frames; no motion review this round (Gemini off). Builders' `--frames`:
  s2 (15, 89, 168 s) clean.
- Gemini checks skipped (quota until ~00:30): `vk listen 7` (all 24 lines, including the two rewritten
  ones) and the per-scene `vk review` of all six scenes. The producer's `vk finalize` transitions pass is
  the only Gemini look at motion.
- Note for ch6: ch6 s7's stand-in already equals ch7's `open_card()` (bare title card, no tag).

- 2026-11-04 Gemini pass (checks only, nothing fixed): full vk listen 1-7 ran. Real (+Whisper): c1.notation.4:2 'dee ex'->'dee exes', c3.implicit.3:3, c3.recip.1:2 (low), c6.recap.2:2 'worked'->'work', c7.basics.3:8 'Cosh'->'cush' (known false). Gemini-only claims: c3.tripos.2 'quotient'->'portion', c4.formula.4 'M'/'F', c4.recap.2 Hermite, c7.recap.1 'hyperbolic', c7.h4two.5 'root'.
- 2026-11-04 re-voice fix pass (the two real mishearings from the Gemini pass): c1.notation.4:2 "It looks like a fraction, dee why over dee ex." → "Dee why over dee ex looks like a fraction." ("dee ex" no longer sentence-final; 24.7 → 24.2 s); c6.recap.2:2 "worked solutions" → "the worked solutions" (23.2 s, was 22.3; a first try, "worked-out", broke ch6 s7's `c.until("worked solutions")` cue, caught by `vk check` and replaced before the listen). Pre-tested on the voice's own seeds with Whisper ×3; house pacing applied by `vk voice`. `vk listen --only`: both now heard right; ch6 0 findings; Gemini-only, accepted: c1.notation.4:5 "that" → "of" (unchanged sentence, already in the 2026-11-04 pass). `vk check --no-render`: no overruns. `vk finalize 1 6`: clean (ch1 12:47.5, ch6 11:57.6).
