# Oscillations: status

2026-11-04: project created; planning.

## Chapter 1 · The rule behind every swing (ch1_rule)
State: **ready for final** (2026-11-04 15:40). Preview `out/ch1_rule_preview.mp4`, 15.0 min
(narration 14.0 min; scenes 65.6 / 89.8 / 164.9 / 105.9 / 123.8 / 130.8 / 113.5 / 105.9 s). All six
in-chapter handovers match (0.00%). s8 ends on exactly `ch2_s1_hook.opening_card()` (added
as-is after the morph; no handover mark, since it is the chapter's last scene).
- s8 (recap): spring + pendulum in step, rule between; at {recap} the "simple harmonic motion"
  box shrinks into the band under the three move columns and stays to {next}; facts line kept to
  {arrow}; recap cards are a local `recap_card()` (kit's look, 22 px, three lines; the kit's
  `move_card` stops at two lines); the {next} dot uses ch2's ω = 2, radius 1.3; DIM "Next: shadows
  of a turning arrow" over the end hold (~10 s after the last word).
- Accepted flags: s1 DIM "?" at {lag} 2.5 s (answered at {beat}); s2 'a = ?', the arc's '?',
  'F = ma' replaced by their answers (brief); live-readout digits in s3 (52.1 s), s4 (41.2, 103.7 s)
  and s7 (90.0 s, a still copy replaces the live readout; 112.3 s labels after motion); s5's legend
  at 2.6 s (s4's long-word entries swapped for s5's short ones after ~4 min on screen); s5 advice:
  FlashAround hugs the single glyph m (c1.gravity.2/3), left as is; s8 end not empty (reversed join).
- No Gemini scene review (dropped 2026-11-04); motion checked on each builder's `--frames` sheet.
  Glitches: none found.
- Open, small: s7's move card wraps "θ:" to the start of its second line (kit `move_card` wraps
  itself); s6's legend says "arc distance" for s (fits two columns).
The bulk `vk voice` run ended 14:46 and lengthened every ch1 clip (pauses): s1, s2, s3, s5
re-rendered on the new timings. Fix passes: s1 (title card held to {next_term}, ~14 s; icon row
0.3 lower), s2 (ẍ legend entry cued on its word; cards leave after the clip; the scene's
construct only, kit API untouched). s4, s6 finished by new builders (s6: the m's pulse instead of
a hugging box; a swallowed `swap` restored; column re-spaced). s7: 113.5 s; the ghost arrow is at
its true ratio (21% longer, the "17% short" is the sine's); ẋ's legend row gives way to
"ω² pendulum g/L"; helpers for s8 in its docstring. 1440p check of s7's r4 frame (table, column,
legend, move card, pendulum at 60°): everything reads; tightest gaps are the rod's L label 0.10
above the 60° reach line and the move card 0.15 above the rule box.
Build order (handovers and shared drawings): s2 (kit) → s3 (spring drawing), s5 (pendulum
drawing) → s4, s6, s1 → s7 → s8.
- **Spring drawing** (`load_scene("ch1_s3_spring")`): `spring_drawing(x=0, y=SPRING_Y, zero=True)`
  (wall, FG coil, BLUE block, DIM table, tick "0"; x in cm), `stretch_arrow(x, y)` (BLUE),
  `pull_arrow(x, y, per_cm)` (RED), `block_center(x, y)`, `rule_boxed()` (the boxed ẍ = −ω²x);
  constants `SPRING_Y`, `SPRING_REST_X`, `SPRING_UNIT`, `RULE_POS`; legend entries `E_K`, `E_M`,
  `E_W`, `ENTRIES`. s3: 138.8 s, clean. Readouts imply k = 50 N/m, m = 0.5 kg (not on screen).
  The kit's small retrieval cards come out at ~18 px; s3 scales the trolley 1.25× to reach 22.
- **Pendulum drawing** (`load_scene("ch1_s5_gravity")`): `pendulum(theta=30, labels=True,
  angle=True)` (θ in degrees, positive = bob hangs left), `gravity_split(theta=30, label=True)`
  (mg and its DIM along-rod / RED along-swing parts), `split_labels(theta)`, `force_formula()`
  (F = −mg sin θ). s5 (107.5 s, clean) shortened legend words so 7 entries fit two columns
  (x "displacement", L "rod length", θ "angle (radians)"; `kit.legend(FINAL_ENTRIES, 4)`).
  Text-font θ renders as script ϑ: keep θ in MathTex, not in Text labels.
- **1440p check of the busiest frame** (ch1 s5 at t = 68 s, rendered `--final`: 2560×1440, 60 fps):
  legend (7 entries, two columns), move card, corner tag, split arrows with three labels, a 6-line
  column with DIM 22 px arrow labels, the small triangle card. Everything reads at 1440p,
  including the 22 px DIM labels and the dimmed old lines. The corners stay apart; the tightest gap
  is the RED `mg sin θ` label ~0.25 above the legend. Slots unchanged.
- Joins into ch2: ch1 s8 (built last) ends on exactly the opening card ch2 records here (a
  reversed join), not on an empty frame.
- **Deep-style widgets, for all four chapters (ready, built and checked at 1440p):**
  `kit = load_scene("ch1_s2_tools")`
  (`from lib.paths import load_scene`). Lay out against the slot constants; never redraw a widget.
  - Slots: `EDGE_X/EDGE_Y` (6.6, 3.5), `TAG_TL` (corner tag), `PIN_POS` (−1.7, 3.42), `MOVE_TR`,
    `LEG_BL`, `RING_POS`, `THINK_POS`; free regions `PICTURE` (x −6.6..0.6, y −1.7..2.85),
    `PICTURE_CENTER`; derivation column `COL_LEFT` 0.95, `COL_TOP` 1.5, `COL_PITCH` 0.7,
    `COL_SIZE` 34; `CARD_FILL` (#171A21).
  - Legend (bottom-left): `legend(entries, max_rows=5)`, entries (TeX, colour, words); ≤5 one
    column, 6–8 two columns while they fit, 9 one tight column up to y≈−0.3. Animate with
    `legend_set(scene, leg, entries, …)`, `legend_add(scene, leg, *entries)`,
    `legend_change(scene, leg, key, words)`, `legend_remove(scene, leg, *keys)` (they play
    themselves). Standing entries `E_X`, `E_XD`, `E_XDD`. Long words break two columns: shorten x
    to "displacement (signed)" when many letters are in play.
  - Move card (top-right): `move_card(text, small=False)` (26–28 px, ≤ 5.6 wide, 2 lines).
  - Think stop: `think_box(question, size=32, pos=None)`, `think_ring(pos=None)`,
    `drain(ring, run_time=8.0)` (linear, clockwise).
  - Tags (DIM 22 px): `tag(text, item=None, direction=RIGHT, buff=0.2)` for "reference" and
    notes-page tags; `corner_tag(text="beyond the notes")` (top-left).
  - Pinned formula (top centre, ch2–4): `pinned(tex, label=None, size=36, **kw)`, `pin_move(mob)`.
  - Column: `col_point(i)`, `col_place(mob, i)`, `step_label(text, i)` (DIM arrow + 22 px label
    above line i).
  - Joins: `chrome(entries, corner=True)` → VGroup with `.legend`, `.tag`; `self.add(*ch)`.
  - ch1 retrieval cards: `trolley_card/triangle_card/arc_card(small=False)`.
  - 1440p mock-up (all slots filled at once, s2 builder): 22–23 px text reads; fixed a legend/column
    clash, a too-wide move card (30 → 26–28 px) and the think box sitting on the column's last line.
- Music: `music/ch1.json` (hook 13 Resonance, s7 sweep 18 Centroid, recap 20 Endpoint).
- Narration rewritten for the ear (Whisper heard "pull" as "pole" in 7 sentences; Gemini heard
  them right but the meaning flips): c1.spring.3 ("name the force that pulls back", "the only force is
  the spring pulling back"), c1.gravity.4 ("gravity's pull", "gravity pulls with about sixty-four
  percent"), c1.arc.1 ("turn gravity's pull into"), c1.small.4 ("gravity really pulls with the sine
  of theta …"), c1.recap.2 ("name the force that pulls back, then use Newton"; "let" heard
  "mutt"), c1.recap.3 ("an arrow that turns in
  a circle", "turning arrow" heard "turning error"), c1.ends.3 (Gemini: "not" heard "thought":
  "Being still and being free of any pull are two different things").
  Re-listen of all 7 (one batched `vk listen 1 --only`): 0 findings. Narration 12.1 min.
- Accepted voice-QA flags: "sine of" → "sign of" (c1.tools.3, c1.gravity.4, c1.small.4: homophone);
  "point zero nine nine eight" → "0.0998" (c1.small.2: number format).

## Chapter 2 · Shadows of a turning arrow (ch2_shadow)
State: **ready for final** (2026-11-04 16:25). Preview `out/ch2_shadow_preview.mp4`, 17.2 min
(narration 15.9 min; scenes 73.2 / 136.1 / 143.3 / 85.0 / 118.3 / 77.8 / 180.1 / 141.0 / 75.7 s),
decodes end to end. Handovers s3→s4 and s5→s6 match (0.00%); s9 ends on ch3's opening card (no
mark; `vk check`'s end flag on s9 is that join, accepted). Music: `music/ch2.json` (hook 29 Orbit,
s6 mirror ride 12 Reflections, recap 25 Clarity).
Open: over deep style's 8–14 min chapter range (17.2 min; the script's 15.9 min of narration sets
it), and the recap is 62 s of narration against the ≤ 60 s rule. The kit's `step_label` at
`COL_PITCH` 0.7 leaves label-to-line gaps of ~0.05 (s2 measured); s2 now uses 0.8. Other scenes
and chapters use 0.7: tight but readable on the holds.
Build order: s1 (opening card, `rule_pin()`, hook wave), s2, s3 (the arrow kit, handover → s4) →
s4, s5 (handover → s6), s7, s8 → s6, s9. Handovers: s3→s4, s5→s6; the other joins fade.
- **Join into ch3 (reversed):** s9 ends on exactly the opening card ch3's director records in its
  STATUS.md section: `load_scene("ch3_s1_hook").opening_card()` (s9 imports it). ch1 s8 is done
  and ends on ch2's opening card.
- s4 built (85.0 s, clean, handover from s3 0.00%; recap export `fan(t, scale, origin, glow,
  width)`, `FAN_SCALE`), s5 built (118.3 s, clean; handover shot GOLD at 50°), s8 built (141.0 s,
  clean). s6 built (77.8 s, clean, handover from s5 0.00%; `mirror_pair(t, scale, origin, …)`),
  s7 built (180.1 s; `example_graph()`, `graph_axes`, `graph_waves(a, b)`, `block_card(x_cm)` for
  the 3-4-5 swing), s9 built (75.7 s; ends on `ch3_s1_hook.opening_card()`, no handover mark).
- Review round 1 (`vk check --chapter 2`, holds; round 2 confirmed both fixes on the holds): only dwell flags (live digits; s7's dense lines
  short on purpose, per the producer's note) and s9's end flag (the reversed join, accepted).
  Fixes sent: s8 θ → x (BLUE) in the big-angle beat (PLAN's notation; the director's prompt had
  said θ̈); s2's column step labels jammed at c2.guess.2.
- Accepted on the holds: ω's legend word changes from "angular frequency, rad/s" (s1–s2) to
  "turning rate" (s3 on, where s4 says why); the arrow at angle 0 lies along the spring's coil
  (s8 beat.1, s7 every.1), the kit's P7 design (block on the real axis).
- **Opening card (reversed join with ch1's end):** `load_scene("ch2_s1_hook").opening_card()`
  returns ch2's first frame as a VGroup: ch1 s3's spring drawing alone (`spring_drawing`, wall, FG
  coil, BLUE block on the DIM table line), the block at its right end and at rest (x = 2.6 cm =
  1.3 scene units, the radius of ch2's unit circle), the table line in the upper half of the
  picture area (y ≈ 2.0), the block's rest point at x = −3.2 (`SPRING_REST_X`). Nothing else: no
  legend, pin, tags or text. ch2 s1 opens with `self.add(opening_card())` (no FadeIn) and lets the
  block go from there. ch1 s8 ends on exactly what it draws. **Built** (2026-11-04):
  `opening_card()` = `spring_drawing(x=2.6, y=TABLE_Y)`, TABLE_Y = 2.0, rest point −3.2.
- ch2_s1_hook also exports `rule_pin()` (the chapter's pinned rule, label "the rule"),
  `hook_wave(origin, t_end, t_start=0.0, color=BLUE, width=4)` (x = 1.3 cos 2t on its side, time
  down), `block_x(t)`, `WAVE_SEC` 0.45, `WAVE_AMP` 1.3, `OMEGA` 2, `WAVE_ORIGIN` (−3.2, 1.25).
- Narration: `vk listen 2` found 0. Rewritten for Whisper "pull" → "pole" and a tense slip:
  c2.every.2 ("Physically, the forces pulling back add together"; "In part one, you met simple
  harmonic motion through its rule"), c2.beat.5 ("a real pendulum is pulled back less than the
  rule says"). The batched re-listen of both heard c2.every.2's new take as "swinks", "borm", so it
  got a plainer rewrite ("Now mix these two motions", "Now you have its formula") and passed
  `vk qa 2` (no further listen, per the one-re-listen rule). Narration 15.9 min.
- Accepted voice-QA flags: "runs round" → "runs around" (c2.vel.2, spelling); "Oiler's" →
  "Euler's" (c2.vel.4, c2.vel.5, c2.every.1, c2.recap.1: the intended name); "sine of" → "sign
  of" (c2.every.1, homophone); "zero point nine nine four metres" → "0.994 meters" (c2.beat.2,
  number format).
- s1 built (73.2 s, clean), s2 built (136.1 s, clean; recap pieces `lambda_picture(scale, lam)`,
  `parabola_picture(scale)`, each driven by `g.tracker`), s3 built (143.3 s, clean).
- **Arrow kit, for ch2 s4–s9 and parts 3–4:** `ak = load_scene("ch2_s3_velocity")`. `t` is a
  ValueTracker (moving) or a number (still).
  - Geometry: `OMEGA` (2), `PLANE_O` (origin (−3.2, 0.4)), `PLANE_R` (1.3), `plane_point(z, scale,
    origin)`, `plane(scale, origin, re_units, im_units, labels)`.
  - Arrows: `turning_arrow(t, omega, offset, length, color, scale, origin, width)` (mirror:
    `omega=-OMEGA, color=PURPLE`; −i sine arrow: `offset=-PI/2`); `velocity_arrow` /
    `accel_arrow(t, base=1|0|tracker, …, glow)` at the tip or from the origin at true length;
    `arrow_between(start, end, color)`.
  - Marks: `right_angle(t, at_tip, …)`, `angle_arc(t, …)`, `t_readout(t)`, `wt_readout(t)`.
  - Shadow: `shadow(t, …)` (.line, .dot); `spring_on_axis(t, …, scale)` (ch1's block, centre on the
    shadow).
  - Clock: `clock(t)` / `run(t, on)`, then `t.animate` to an exact value to freeze.
  - Fixed pieces: `rule_pin()`, `lambda_box()`, `velocity_caption()`, `ENTRIES`, `LEG_ROWS` (4),
    `MOVE_M5`, `handover_shot()`. Legend words from s3: ω "turning rate", e^{iωt} "turning arrow".

## Chapter 4 · Putting it to work (ch4_work)
State: **ready for final** (2026-11-04 17:20). Preview `out/ch4_work_preview.mp4`, 13.7 min
(narration 12.4 min; scenes 83.5 / 161.5 / 146.6 / 136.7 / 140.9 / 84.1 / 68.1 s). Handovers
s2→s3 and s4→s5 match (0.00%); s7 ends the pilot on the usual end card (DIM "Next: the
impedance video" over an 8 s hold), no handover mark. Music: `music/ch4.json` (hook 19 Spirals,
s5 sweep 04 Euler's Clock, recap 34 The 3Blue1Brown Experience).
- Accepted check flags: s4 c4.sheet.3 "transition early": M8's card (now ch3's
  `move_m8()`) arrives on {hint1}, 2.4 s before "Add the arrows" is said, as the brief places it
  ("Hint one is the move from part three"); s4 advice: FlashAround on the single glyph 7 (advice
  only); dwell advisories on short-lived labels in s1–s7 (each scene's line above).
- **Opening card (reversed join with ch3's end):** `load_scene("ch4_s1_hook").opening_card()`
  returns ch4's first frame as a VGroup: the hanging spring alone, at rest. A DIM hatched ceiling
  at the top of the picture area, ch1's FG coil hanging from it, and the BLUE weight (ch1's block)
  at its rest level, all centred on x = −3.2 (`SPRING_REST_X`). Nothing else: no legend, pin,
  tags, dashed level or text. ch4 s1 opens with `self.add(opening_card())` (no FadeIn), then pulls
  the weight down. ch3's last scene ends on exactly what it draws (call it, never copy).
  **Built** (2026-11-04 16:00, final): `opening_card()` = `hanging_spring(7)`: ceiling line at
  y = 3.1 (1.8 wide, hatching to 3.32) centred on x = −3.2; the weight (0.9 × 0.8 block) at rest
  centred at (−3.2, −0.3); 1 cm = 0.06 units upward (`HANG_UNIT`), so x = 32 → y = 1.2,
  x = −18 → y = −1.8. Also `weight_center(x, pos, scale)`, `ceiling_y(pos, scale)`, `HANG_REST`,
  `X_REST` (7), `f19(t)`, `f19_v(t)`.
- **Shared with ch3 (ch4 must match exactly):** ch4 takes the pinned `x(t) = Re[A e^{iωt}]` and
  M8's move card ("Add the arrows, not the waves: …") from ch3's scene files. ch3: please record
  here (or in your section) the functions that return them (e.g. `amp_pin()` in ch3_s2_freeze,
  `MOVE_M8`/`move_m8()` in ch3_s4_add). Until they exist, ch4 routes every use through
  `ch4_s1_hook.amp_pin()`: it returns `load_scene("ch3_s2_freeze").amp_pin()` when that exists,
  else its own build to PLAN.md's spec (`kit.pinned`). ch3: naming your pin function `amp_pin`
  in ch3_s2_freeze makes ch4 follow it with no edit.

## Chapter 3 · The complex amplitude (ch3_amplitude)
State: **ready for final** (2026-11-04 17:56). Preview `out/ch3_amplitude_preview.mp4`, 12.5 min
(narration 11.6 min; scenes 81.9 / 129.1 / 126.3 / 178.3 / 171.1 / 62.4 s). Handover s2→s3 ok
(0.00%). s1 opens on its `opening_card()` (ch2's last frame); s6 ends on exactly
`ch4_s1_hook.opening_card()` (no mark: the chapter's last scene). Music: `music/ch3.json` (hook 31 Quantum
Blue, s3 knobs 24 Transformation, recap 28 Gnomon; none shared with ch1, ch2 or ch4).
Build order: s1 (opening card first), s2 (plane, pin and arrow exports; handover → s3) → s3, s4,
s5 → s6 (ends on ch4's opening card). Joins: s2→s3 is a handover; the others fade to empty.
- **For ch4:** the pin is `load_scene("ch3_s2_freeze").amp_pin()` (**built**); M8's card text will
  be `load_scene("ch3_s4_add").MOVE_M8` (with `move_m8()` returning the card), and s5 exports the
  fan of three arrows. Confirmed here when built.
- s2 built (129.1 s; handover → s3). **Plane kit** (`load_scene("ch3_s2_freeze")`, docstring lists
  all): `PLANE3_O` (−3.2, 0.6: at 0.4 the radius-5 plane ran into the two-column legend), `CM` 0.42
  scene units per cm, `S3`, `A3` = 3 − 4j, `R3`, `PHI3`, `OMEGA3` 3, `CLOCK` 2/3, `PERIOD3`; `pt`,
  `plane3`, `plane_labels`, `arrow3`, `shadow3`, `spring3`, `frozen_A`; `amp_pin`, `amp_caption`,
  `MOVE_M7`/`move_m7`; legend `E_A` ("frozen arrow"), `E_ANGLE3` ("angle"), `E_MIRROR`
  ("mirror"), `E_RULE`, `ENTRIES3_0`, `ENTRIES3`, `LEG_ROWS3` 4 (longer words break the two 22 px
  columns); `handover_shot()`. `clock3` drifts ~1 s per 40 s: use a frame-exact clock for landings.
  Accepted: the "beyond the notes" tag under line 3 dwells 4.1 s (check wants 5.2; the column must
  clear before the handover). The mirror sum zooms the view out to half and back.
- s3 built (126.3 s; s2→s3 handover 0.00%). The spring fades at {two} and returns at {ours} (it sat
  on the arc's wedge); "amplitude"/"phase" and the DIM questions sit in a side panel that becomes
  the live readouts; `kit.LEG_MAX_RIGHT = -0.3` set in the scene only; T3.1's question in the box's
  three lines. Sweeps ~5.5 s each, frame-exact. Accepted: the "?" 4.1 s; the readout stand-in
  digits at {ours} 0 s (a hand-off from the live readouts, as ch1's).
- s4 built (178.3 s). Exports `MOVE_M8`, `move_m8()`, `tip_to_tail(t, a, b, origin, unit, gold,
  shadows, width)`, `A_DEMO` 4, `B_DEMO` 2. Hook rows return at 0.4 scale in the right column
  (no room left of the plane); one arrow 4 − 2i throughout, so at {quarter} the PINK part swings
  right; the dashed arrow sits 0.16 aside until {merge}; the legend drops the rule, A* and later
  ωt to fit a, b, α, β. T3.2: the 6 + 8i triangle beside the plane at its own scale (0.21 per cm),
  PINK leg up. Accepted: short dwells on the i² line (rewritten in place, as briefed), "real parts
  equal" (the quarter turn sweeps through), "sine arrow starts at −i" (4.7 of 5.6 s).
- s5 built (171.1 s). Exports `fan3(t, origin, scale, labels, amp, marks)`, `E_V`, `E_ACC`,
  `ENTRIES5`, `MOVE_M9`/`move_m9()`. GREEN and RED arrows labelled "not to scale: length 15/45";
  T3.3's 6i "not to scale: length 6". Accepted: the ẋ = Re[iωA e^{iωt}] line dwells 6.1 s.
- s6 built (62.4 s, narration 50.0 s). Three panels with `recap_card` (ch1 s8) for M7–M9, s3's
  brace and arc as local copies (s3 exports none), s4's `tip_to_tail`, s5's `fan3`; {next} uses
  ch4 s2's `spring_at(3)` and push arrow; DIM "Next: putting it to work" ~5.8 s, then the
  horizontal spring morphs into ch4's hanging one and `ch4_s1_hook.opening_card()` is added as-is
  (held 1.2 s). Accepted: check's "end" flag (the reversed join, as ch2 s9); the F19 card comes
  on {sheet}, ~2.3 s before "examples sheet" is said (marked early, as briefed).
- No Gemini scene review (dropped 2026-11-04); motion checked on each builder's `--frames` sheet
  (s1 rows → strip, s2 spin, s3 |A| sweep, s4 tip slide, s6 shrink and morph). Glitches: none.
- Review round 1 (holds 17:07): fix passes on s2 (ωt readouts count total time, 42.01 / 56.80 rad,
  while the arc shows under a turn; the A e^{iωt} label near the block), s4 (M8 card wraps to a
  crammed third line; b alone BLUE as in s1), s5 (t readout 0.36 s at the t = 0 freeze; the {ours}
  calc lines against the legend; the readouts against the column's step labels).
- Round 2 (holds 17:46) confirmed all of them. s2: both ωt readouts count from the moment the
  arrow was at A, mod 2π (4.31 / 0.25 rad on the tiles); the A e^{iωt} label slides clear of the
  block, with a background outline. s4: `MOVE_M8` = "Add the arrows, not the waves: flat a plus
  downward −ib is A." (two even lines, a/−ib/A as coloured maths; the recap re-rendered with it);
  b BLUE wherever it stands alone (also the 2 in 2 sin 3t; −2i stays PINK). s5: the fan stays
  frozen at t = 0 from {starts} through the think stop (t = 0.00 s); calc rows 0.4 from the legend;
  readouts 0.6 from the step labels. **For ch4:** `ch4_s4_f19` keeps a fallback copy of the old
  M8 text, used only if ch3's `move_m8` is missing.
- Open, small (two review rounds done): the M7 and M9 cards wrap one or two words onto a third
  line (the kit's `move_card` wraps itself; even spacing, unlike M8's old card); s5's riding "not
  to scale" labels pass over the coil and the Re/Im labels for a moment; s5's legend drops "angle",
  "rule" and "mirror" (one column would cover the plane); s4's legend likewise drops the rule, A*
  and ωt. Nothing running.
- Narration (before building): `vk listen 3` found 5, `vk qa 3` 4. Rewritten and re-voiced in one
  `vk voice 3`: c3.hook.1 ("Here are three weights", Gemini: "Three" → "Tree"), c3.hook.3 ("Which
  arrow throws a shadow equal to the sine of omega T?", +qa "casts … its" → "cast … a"),
  c3.freeze.4 ("Put the mirror on the arrow's tip, and their vertical parts cancel. So the sum sits
  on the real axis", Whisper "Tip" → "Chip", +qa "lands" → "leans"), c3.read.4 ("It's the second
  weight from the opening, but sent off the other way", "pushed" → "push"), c3.add.3 ("The sine
  wave starts at zero", heard "The sign starts" right after "Why a minus sign?"). Batched re-listen:
  only "Here are" → "Here" (c3.hook.1, "are" swallowed; meaning intact, accepted). Narration 11.6 min.
- Accepted: "sine of" → "sign of" (c3.hook.3, homophone); "examples sheet" → "example sheet"
  (c3.recap.2, Gemini-only; the s-sh run elides, same meaning, the course's phrase).
- **Opening card (reversed join with ch2's end):** `load_scene("ch3_s1_hook").opening_card()`
  returns ch3's first frame as a VGroup: three copies of ch1's spring drawing
  (`load_scene("ch1_s3_spring").spring_drawing`, wall, FG coil, BLUE block, DIM table line, tick
  "0"), stacked down the left of the frame (rows near y ≈ 1.9, −0.2, −2.3, scaled together to fit),
  every weight at rest at its middle (x = 0); plus ch2's pinned rule
  (`load_scene("ch2_s1_hook").rule_pin()`, ẍ = −ω²x, "the rule") at its usual top-centre place.
  Nothing else: no time axes, waves, legend, tags or text. ch3 s1 opens with
  `self.add(*opening_card())` (no FadeIn). ch2 s9 ends on exactly what it draws (call it, never
  copy). **Built** (2026-11-04 16:10): a VGroup of 4 (rows 0–2, then the pin). Each row is
  `spring_drawing(0, y=0)` moved so its rest point (the "0" tick) sits at (REST_X, y), then scaled
  by ROW_S = 0.8 about that point; `ROW_YS = [2.1, 0.4, -1.3]` (table lines), `REST_X = -3.92`;
  left edge x = −6.6, table right ends x ≈ −1.04; item 3 is ch2's `rule_pin()`. ch3 s1 adds it at
  t = 0 and only then fades in its legend.
- s1 built (81.9 s, clean). Exports `OMEGA = 3`, `CLOCK = 2/3` (one model-time tracker drives
  every swing). Accepted dwell advisories: the derivative line 4.7 s (cleared for the question),
  the title card 4.3–5 s (gap after c3.hook.2 lengthened to 3.2 s), the two "?" 3.9 s.
- Narration (12.4 min): rewritten for the ear, one `vk voice 4` batch plus one line:
  c4.start.2 ("It's a snapshot taken before the arrow starts to turn, so the complex amplitude
  tells you the start directly": "has turned" heard "is turned", "read" heard "red" +qa),
  c4.sheet.1 ("from the first sheet of examples": Gemini heard "example"; "how far from the origin
  the weight is": "it" heard "that"; then "stop the video here": the batched re-listen heard
  "pause" as "pass", so a plainer rewrite and `vk qa 4` only), c4.sheet.2 ("until its force
  balances gravity": "pull" heard "pole"), c4.events.1 ("The second hint is the first step":
  "Hint two" heard "and 2" +qa). Re-listen of the four: only the sheet.1 finding above.
- Accepted voice-QA flags: c4.events.2:3 "Lying flat" (base "Line flat", medium "Flying flat":
  the models disagree, Gemini heard it right), c4.events.3:1 "three T minus delta" → "3t-delta"
  (number format).
- Build order: s1 (opening card, `hanging_spring`, `amp_pin` first), s2 (handover → s3), s4
  (handover → s5), s6 → s3, s5 → s7.
- s1 built (83.5 s, clean; title card ~3.3 s and the last T line 6.4 s of 7.3: dwell, accepted).
  `amp_pin()` is its own build until ch3_s2_freeze exports `amp_pin`.
- s2 built (161.5 s, clean; the reset t readout's dwell flag is a redraw, accepted). M10 card
  reads "Set t = 0: the turning factor becomes 1, so the start reads off A" (two lines; e^{iωt}
  can't go in the card's text font). Exports: `MOVE_M10`, `move_m10()`, `start_picture(v0, x0=3,
  omega=3, origin=O, unit=U, push=F, weight=False)` (v0 may be a tracker), `handover_shot()`,
  `amp_plane()`, `spring_at(x_cm)`, `general_box()`, `ENTRIES`, `O`, `U` (0.38/cm), `F`.
- s4 built (136.7 s, clean; dwell flags on short-lived labels accepted). M8 card via `move_m8()`:
  `kit.move_card` with ch3's exact text (wraps to three lines), switching to
  `ch3_s4_add.move_m8()` once that exists. Handover → s5: plane `f19_plane()` (origin `F19_O`
  (−5.0, 1.2), `F19_U` 0.2/cm, `f19_point(z)`), `gold_arrow()`, `inset_spring()`, `x_line()`,
  legend, pin, `strip()`.
- s6 built (84.1 s, clean). Exports (each a VGroup with `.static .dynamic .op .plane`; t, gap,
  back take a tracker or a number): `panel_commute(t, scale, origin, omega)`, `panel_cancel(t,
  gap=0, …)`, `panel_quarter(t, back=0, …, label)`, `fan(t, scale, origin, omega, tracks)`,
  `circuit_small(scale, arrows)`, `panel_title(k)`, `panel_caption(k)`, `show(pic)`,
  `hide(pic)`; `W_D` 1.3, `PANEL_SCALE` 0.45, `FAN_SCALE` 0.615. Panel 2 shows A₂ starting
  apart and closing onto A₁ on "the same arrow" (two different arrows can't share every shadow).
- s5 built (140.9 s; handover from s4 0.00%). Plane re-framed in one move (0.08/cm, centre 7 at
  (−0.85, 0.35)). Legend's X entry is "turning arrow" (a superscript reads badly in the legend).
  Exports: `MOVE_M11`, `events_picture(t, scale=1.0, center=ORIGIN, flags=True)` (`.arrow
  .shadow .spring .circle .flags`), `DELTA`, `PERIOD`, `T_TOP`, `T_PASS1`, `T_BOT`, `T_PASS2`,
  `T_END`, `zf(t)`, `xf(t)`. Rendered past one transition flag ("3" over "1" in the sweep's
  live x readout): to confirm on frames in review.
- s3 built (146.6 s; handover from s2 0.00%; dwell flags on short-lived labels accepted). The
  long way sits in a DIM card over the picture area and builds in ~9 s of silence after
  c4.faded.2 (the narration gives it 4 s). `think_math()` (maths-capable think box, kit look).
- s7 built (68.1 s incl. the 8 s end hold; dwell advisories on the last two r3 lines accepted).
  p3 drawn with the arrow kit (ch3_s2_freeze has no shrinkable freezing-arrow export); small move
  cards scaled ×1.1 (the kit's `small=True` gives 20 px); the circuit's arrows turn here
  (`circuit_small` draws them still).
- ch3's `amp_pin()` exists since ~16:40, so `ch4_s1_hook.amp_pin()` now returns it; the whole
  chapter is re-rendered for review so every scene shows ch3's pin.
- Review round 1 (holds + full-size `--frames` I pulled at the doubtful tiles): fix passes on s2
  (c4.start.5's labels moved clear of the circle, grid and column) and s5 (plane labels off the
  circle and axis lines, the circle a little smaller (0.07/cm), the {turn} beat stops at 1.4 rad
  so 3t − δ has room, the wave lobe 0.2 clear of the legend; the "3 over 1" flag was the live x
  readout's per-digit MathTex: the readouts are now single texts, flag gone). s6's `~` tile is
  its panels turning all clip long (content checked on a frame); s2's 7-row legend is inside the
  frame (the tile misled). s4's `move_m8()` now returns `ch3_s4_add.move_m8()`.
- Glitches: none confirmed (the s5 flag was an audit artefact of the redrawn readout).
- Review round 2 (holds after the fixes): s2's and s5's fixes confirmed; nothing new. Open,
  small: s6's panels are small (unit circle ~0.6 wide) with the lower frame empty; the M8 and
  toolkit move cards wrap to three lines (the kit wraps itself); s3's long way builds in ~9 s of
  silence. Gemini: `vk listen 4` and one batched re-listen done (above); no visual review.
