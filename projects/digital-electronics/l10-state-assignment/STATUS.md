# State Assignment: status

2026-10-31: project created; planning.

## Chapter 1 · Which bits for which state?
2026-10-31: DONE. Video `out/ch1_assignment.mp4`, 10.9 min (652.8 s), 1920×1080 at 60 fps; 8 scenes, all
handovers (s5→s6→s7→s8) match exactly. Music `music/ch1.json`: hook Zeta (to machines.1), s5 waveform
stretch Fives (choice.4:end → divide.3), recap Sixes (circuit.2:end → END, swell after circuit.4).
- Rewritten for the ear (all re-voiced, re-checked with `vk listen --only`): "ay" was voiced "eye" /
  "ay ay" / "AI" (+qa) in divide.3, count.2, kmaps.1, kmaps.3, circuit.1, so those sentences write a
  capital "A" ("flip-flop A", "not A and not see", "bee and A"), same as ch2. Unflagged "ay" stays in
  kmaps.4, kmaps.5 and count.2's "ay prime". "flip-flops" heard "foot-flops"/"flit-flops"/"fwit-flop"
  (Gemini, high): hook.2 "With two flip-flops, there are exactly four patterns"; machines.2 "Its
  outputs feed a row…", "Together they hold the current state, and it loops back"; circuit.1 "And a
  second and gate, of A and bee, is the input to flip-flop see." divide.2 "halved" (heard "habd") →
  "cut the frequency in half". choice.4 "In the lecturer's words" → "As the lecturer put it";
  circuit.4 "the lecturer's more funky assignments" → "the lecturer shows some more funky
  assignments"; circuit.1 "drawn ay, bee, see … as in the lecturer's simulation" → "drawn from left
  to right as A, then bee, then see, just as the lecturer drew them".
- circuit.2 "stepping from zero zero zero up to one zero zero" (review heard "one hundred") → "counting
  up through all five codes, then back to zero zero zero."
- Accepted voice flags (Whisper only, meaning unchanged): kmaps.1
  bit strings as digits (number format); circuit.2 "in his simulator" → "in a simulator". The
  writer's watch list ("em states", "FPGA", "Mealy", "see prime", "seventy-four series", "one
  hertz", "exclusive-or gate") passed the full Gemini listen.
- traffic.4 now reads p. 124's quote verbatim ("the optimum choice"), matching the screen (Gemini
  review mismatch); kmaps.2 likewise says the lecturer's full words, "Gray coding of these
  assignments". divide.3's names: two Gemini reviews heard "bee and A" / "flip-flop A" as "uh", so
  it's now "Call them see, bee and A. They're written in that order, so the bit on the right is A."
  (each A ends a sentence). kmaps.5: "Last, flip-flop see" (heard "flit flap", "foot flop") → "The
  last one is the see flip-flop."; the closing "no help for flip-flop ay" (review: "uh") → "For
  flip-flop A, the don't cares gave no help at all. For bee and see, they doubled every group."
- Shared drawings (load with `load_scene(stem)`): `traffic_ring(codes=None, …)` (ch1_s1_hook.py);
  **`moore_diagram(names=("A","B","C"), r=0.62)`** (ch1_s2_machines.py: p. 123's Moore diagram, A
  (-3, 1.9), B (3, 1.9), C (0, -1.2), no codes; `.circles .names .arcs .labels .by_state`; s2 shows it
  with a "Part 5" tag; **ch5's hook calls back to it**) and `recipe_row()`; `doubling_ladder()`,
  `ceil_log2()` (ch1_s4_choice.py); `divide5_wave()`, `state_ring(codes=None, …)` (ch1_s5_divide5.py,
  the five-state ring, GOLD numbers inside, codes outside); `count_table(boxed, d_row)`
  (ch1_s6_count.py).
- Glitches (confirmed with frames, all fixed):
  - s1 ~7.8 s and ~8.3 s, s3 ~7.6 s: a stray stroke / yellow corner bracket by a state circle.
    Cause: `FlashAround` on a Circle traces a square round its bounding box. Replaced by a
    `VShowPassingFlash` round the circle (`ring_flash`).
  - s4 ~51.5 s and ~54.5 s: the "5 states" brace sat between rows with no label, then a stray brace.
    Cause: the label swapped in place while the brace moved separately (`animate.move_to`). Now
    brace and label move as one.
  - s6 ~57 s: a flying bit sat on the table's header rule (fly route along the D-row band). Now the
    bits fade in at their slots. s6 ~64.4 s: GREEN lines above a′: `FlashAround` on a table `.bbox`
    that was never on screen and stayed at the old layout.
  - s5 ~52 s (claim): flip-flop boxes and their c/b/a labels were separate objects faded apart; not
    seen in frames, now grouped.
  - s1 ~29.4–29.8 s: the right and left codes read "10"/"01" for a moment during the 3 → 4 flip-flop
    change. Cause: `edit` keeps glyphs the old and new strings share ("110" → "0100" kept "10") and
    fades the extra digit in late. Now `swap` (all out, all in).
  - s7 ~82.5 s: a YELLOW ring left round the spare X at 111: `FlashAround` on the X, slow fade. Now a
    colour pulse. s7 ~64 s: D_b's 1s flew straight across the a′ column (row 2 read "11") and the map's
    row heading; now routed below the table.
  - s8 ~31 s: a duplicate "b" input label over the exclusive-or gate: the circuit moved while the
    D_b equation was still fading, and the gate labels rose into it. Now the equations clear first.
  - s5: brace and walking box placed from `divide5_wave().rise_x`, which holds pre-move positions
    (0.15 off); now placed from the drawn guides. Later scenes using `rise_x` on a moved wave: beware.
  - Accepted (seen by the builder, minor, not fixed): s7 ~92 s the PINK loop starts as a short
    stroke beside the 1; s7 ~100 s mid-{compare} D_b's equation briefly shows "D_b = a … ⊕ b";
    s4 ~53 s a faint tick after "11" on row 2 (tail of the red row flash).
- Gemini claims checked and rejected (frames show them wrong): s1 amber lit in all states / grey
  bars at the road shrink; s3 arrows backwards (frame at 4 s: clockwise), "care" vanishing; s6
  highlight lingering; s7 D_a's 1s during D_b; s8 LED sequence (LEDs and the "c b a =" readout agree
  in every frame; the LEDs read right to left, hence the readout).
- Accepted check flags: dwell advisories throughout (codes and bits that step with the voice);
  small text in s7's table (size 24, from s6's handover at 0.8), s8's DIM chip numbers (23–26, as
  the brief asks) and s8's recap thumbnails.
- Final review (`vk review 1`, `--transitions`): 16 claims, all mid-transition; checked against
  frames of the final video. Seen and accepted (motion, not settled frames): s7 ~19.8 s an X
  mid-drop below the unused-states line; s7 ~36.8 s the YELLOW column box slides across b′ on its
  way to a′; s7 ~99.8 s D_b's equation split mid-move; s8 ~9.3 s the fading "table c b a" tag; s2
  ~26.4 s the Moore diagram shrinking as it fades (by design); s1/s3 brief cross-fades of codes and
  captions. Rejected: "umsed" typo (frame reads "unused"); s5 brace "4 cycles" (spans edges 0–5);
  s8 LED c dark (LEDs match the readout); s1 amber in all states. Open, minor: in s5's divide.3 the
  "5 clock periods" brace stays at the top without its label while the ring drops in.
- s8 deviations: the circuit is ch2's `binary_circuit()` (gate inputs as labels ā, c̄, a, b, not a Q̄
  wire back along the bottom), output label "out"; the scoreboard is ch2's `scoreboard()` at native
  scale under the circuit; recap on ch2_s8's grid; a GREEN "c b a = …" readout beside the LEDs.

## Chapter 2 · More flip-flops, less logic
2026-10-31: DONE. `out/ch2_sliding_ring.mp4`, 9:31 (571.5 s, 1920×1080, 60 fps); narration 8.9 min, 8/8 scenes by
Opus scene-builders in dependency batches (s1, s2, s5; then s3, s4, s6; then s7, s8), two scene-review rounds
(Gemini per scene + holds), the final viewer and transitions reviews, one fix round from those, then re-finalled
(not re-reviewed, per the one-round rule). Check: no overruns or errors.
- Accepted check flags: small text in s1's corner circuit, s7's side-by-side {power} circuits and s8's six recap
  panels (the briefs ask for them small); dwell advisories where cue spacing sets them (s1 title card ~4 s and
  {pay} "?" 3 s; s2's travelling bits and closing quote; s4's per-edge digits; s5 p. 137 quote 4.7 s; s6
  "no gates" 4.3 s; s7 "one gate"/"no gates"; s8 r6 labels); s4 flashbox advice on the Q̄/b̄/c̄ flashes.
- Music: hook Serendipity, s4 circuit-run stretch Orbit (circ.2), recap Ongoing (ch1 uses Zeta, Fives, Sixes).
- Shared drawings, coordination with ch1 (running at the same time): ch2_s1_hook.py defines the
  scoreboard (`scoreboard()`: header "assignment | flip-flops | next-state gates | output logic",
  numbers GOLD, row "binary | 3 | 3 | none") and the five-state ring with codes. If ch1_s8_circuit.py
  already has its scoreboard when ch2 s1 builds, ch2 copies ch1's; otherwise ch1 s8 should copy
  ch2_s1_hook.py's so the two match. ch2 s4 adds the "sliding | 3 | 1 | none" row, ch2 s7 the
  "ring | 5 | 0 | none" row (ch5/ch6 extend it from s7's helper).
- Rewritten for the ear (all re-voiced; Whisper QA and a Gemini re-listen came back clean): "ay" was voiced
  "eye" (Gemini + QA: "dee eye", "AI", "ay ay") in logic.2, logic.3, logic.4, ring.2 and wire.1, so those lines
  now write a capital "A" ("flip-flop A", "dee A equals ee"), the same fix as the N/K rule. ch1 is doing the
  same. Unflagged "ay" stays in slide.1 and circ.1. slide.4 "see reads zero, zero, zero, one, one" came out
  with a third "one" (+qa) → "see reads three zeros, then two ones". wire.1 "So dee A equals ee." (Gemini
  "E E") → "So dee A equals ee, the output of the last flip-flop."; its "zero, zero, zero, one, one" gained
  "then". trade.2 "flip-flops take up very little room" (Gemini "thirty") → "only a little room";
  "Combinational logic needs wiring" (+qa "Common national") → "Logic gates need wiring between them".
- Accepted voice flags (Whisper only; Gemini heard them right): hook.1:3 "Two and gates" → "two in gates";
  circ.1:1 "lecturer's" → "lecture's"; wire.2:3 "Laid" → "Layed" (spelling). The writer's watch list
  ("egregious", "funkier", "not-bee and not-see", "dee" for both D and flip-flop d, the s2 bit strings)
  passed the full Gemini listen apart from the slide.4 fix above.
- More ear rewrites after the scene reviews (each re-listened clean): circ.1 ("ay" → "uh" ×3 in the s4 review → "A";
  "lecturer's simulation" → "the way the lecturer drew it in his simulator"; "A single and gate" heard "in gate" →
  "Just one gate is needed, an and gate. It takes…"); logic.2 and wire.1 ("dee A" heard "dah" in the s3 and s6
  reviews → "the input to flip-flop A is not bee and not see", "So flip-flop A takes its input from ee, the last
  flip-flop."); trade.1 now says "just a couple of bits of fun", matching the card (s7 review mismatch); trade.2
  ("flip-flops" heard "foot-flops" → "each flip-flop takes up…"; then "So it can be better…" lost its "it" → "So
  using more flip-flops to avoid the logic can be the better choice."); recap.2 ("flip-flop" heard "fup-flop", then
  "shift" → "shist", then "Close" → "Closed" → "Then join the register into a ring of five, and each flip-flop
  simply copies the one before it…").
- Accepted scene-review ear claims that a focused listen didn't confirm: ring.2 "place" → "class", ring.3 "five" →
  "fight" (s5 review).
- Glitches (scene reviews, confirmed on frames by the builders unless noted):
  - s2 ~98 s slide.4 {any}: "stray green rectangle on the waveforms". The three GREEN outlines were mid-`GrowFromCenter`,
    so the c outline was half-size and cut across its trace. Fixed: fade in place.
  - s6 ~22 s wire.1 {db}/{rest}: "column c highlighted". The column boxes slid from e/a′ across d, c and b, so mid-slide
    they framed the wrong columns. Fixed: fade out, fade in at the new columns.
  - s1 ~24 s hook.2 {question}: "duplicate offset code labels". Not an overlap on frames: the codes moved upward
    while turning into "???". Changed to an in-place fade anyway.
  - s3 ~27 s logic.2: "010 read as 101". The X copies flew from the unused codes over other codes (not caught on a
    frame). Changed: each X fades in on its cell while its code flashes.
  - s3 ~79 s and ~87 s logic.4 (leftovers, not transitions): the DIM bracket's two halves stayed on screen after
    its fade-out missed them; the "shift register" brace was measured from mid-height and ran through the cells
    like a wire. Both fixed.
  - Not reproduced: s1 ~10 s "only the exclusive-or lit on 'two and gates'"; s2 ~55 s "out waveform inverted"
    (the holds tile misled me too: frames show high 2, low 3); s3 ~63 s "D_a = a" (the half-faded D_b = a line
    under D_a); s6 ~39 s "duplicate '= d'"; s5 ~38 s "stray yellow triangle" (the clock-edge marker, by design).
- Review-led layout fixes: s1's YELLOW "?" now sits over each of the three dimmed gates (was the middle gate only);
  s4 circ.2 waveform block lifted and circ.3's circuit shrinks/rises so the board clears the CLK labels; s5 ring
  table restyled to s3's (Mono digits, GOLD 1s, "Current state"/"Next state"); s6 `ring_circuit()`'s "output" arrow
  now points down off the Q_b → D_c wire (it read as a tap on the feedback wire); s6 caption clears before {nogates};
  s7's GOLD arrows point down the rows, labelled more/fewer.
- Final-video reviews (viewer + transitions) on the first final; one fix round, each confirmed on frames by its
  builder, then re-finalled (not re-reviewed, per the one-round rule):
  - s4 circ.2 ~33.6/38.6/43.6 s (both passes, and the round-2 scene review): "two digits above flip-flop c". The bit
    leaving c slid right until it sat over c's LED probe and read as c's second digit. Fixed: it fades in place
    (0.25 s) at the start of each edge.
  - s2 slide.1 ~27.3 s (every code drop): "0 1 1 scattered over the clock ticks". The code copy's custom path dipped
    under the row through the YELLOW edge ticks. Fixed: no flight; the cells flash and the code fades in at its row.
  - s2 slide.3 {two}: the GOLD brace under the high part was read as marking the low part by three Gemini passes
    (and by me at tile scale), though frames showed it right. Moved above the high segment, pointing down.
  - s2 ~73.3 s: a {pass} 0 outlived its cell into slide.4. Fixed: clears with its cell.
  - s3 logic.2 ~34.8 s: "a doubled 1 in K-map cell 01". `carry()` crossfaded each copy with its entry before the copy
    stopped, and the cell-01 copy flew over the 1 landing in cell 00. Fixed: land, fade out, then fade in; copies
    run along the map's middle line.
  - s6 wire.2 {unroll} ~45.9 s: "four stray blue squares on the right". Transforming the circle's cells into the
    flip-flop boxes bunched them up mid-morph. Fixed: the circle fades out, the boxes fade in.
  - Accepted: s1 hook.2 shows the binary codes on "funkier codes" (the brief: they turn to "???" at {question});
    the s1 quote card "you wouldn't necessarily do it in anger" against the narration's "for real" (the lecturer's
    words); s8's end card "Part 3 · Starting in a used state" (ch3's real title; Gemini expected "unused").
- Shared drawings for later directors (all standalone helpers in scenes/):
  - ch2_s1_hook.py: `scoreboard(rows, n_rows=3)` + `sb_cell(sb, r, col, text)` (header "assignment | flip-flops |
    next-state gates | output logic", numbers GOLD); `five_ring(codes)` with `ring.code_at()` (BLUE nodes 0–4,
    codes outside the nodes; s2 and s5 use it); `binary_circuit()` (ch1's circuit, gate inputs as labels).
  - ch2_s2_sliding.py: `SlideRow`, `cell_bit`, `code_column`, `clk_wave`, `bit_wave` (the GOLD travelling 1s; ch4's
    travelling 1 can copy them).
  - ch2_s3_slidelogic.py: `slide_table()`, `col_box()` (the chapter's table style: Mono digits, GOLD 1s, "Current
    state"/"Next state"), `carry()`, L6's `kmap()` with c/b/a labels.
  - ch2_s4_slidecircuit.py: `sliding_circuit()`, `place_small()`, `board()`/`sliding_cells(sb)`, i.e. the scoreboard's
    "sliding | 3 | 1 | none" row.
  - ch2_s5_ring.py: `ring_circle(center, R, bits)`, `ring_table(center, rows)` (`TABLE_C`, `.titles`), `ring_wave()`.
  - ch2_s6_nologic.py: `ring_circuit()`, the unrolled ring that ch3 s1 opens on: five `make_ff` a–e on one YELLOW
    CLK line, centred (0, -0.2), 12.93 × 4.02 (x -6.46…6.46, y -2.21…1.81); Q of each into the next D; a GREEN
    feedback wire from Q_e along the top into D_a; "output" as a short GREEN arrow pointing down off the
    Q_b → D_c wire (tap (-0.74, 0.19) → (-0.74, -1.35)), label centred (-1.12, -1.59); no gates, no LEDs.
  - ch2_s7_tradeoff.py: `board3()`, `ring_cells(sb)` (the "ring | 5 | 0 | none" row), `sb_arrows(sb)` +
    `sb_arrow_labels()` (GOLD arrows pointing down the rows, "more"/"fewer"), `row_box(sb, r)`. ch5/ch6 extend this.
  - ch2_s8_recap.py's end card (ch3 s1's opening): `ring_circuit()` at its own geometry, a flat GREEN output trace
    (stroke 4, (-5.0, -3.3) → (6.0, -3.3)) with "output" (T 30 GREEN) right-aligned at x -5.25, CLK pulsing about
    every 1.2 s, a RED "?" (T 64) at (0.5, -2.75), and "Part 3 · Starting in a used state" (T 40, y 3.2). ch3's
    brief asks for a YELLOW "?", so ch3's director should pick one.
- Brief additions (the continuity review's gaps): s1 {title} is the title card alone, cleared before {last};
  s8 {recap} is a "Recap" heading over six faint slot frames on the 3 × 2 grid that r1–r6 fill.

## Chapter 3 · Starting in a used state
2026-10-31: DONE. `out/ch3_startup.mp4`, 9:57 (596.8 s, 1920×1080, 60 fps); narration 9.4 min. Music
`music/ch3.json`: hook Heartbeat (to stuck.1), s7 ring-runs stretch Machinery (restart.1:end → restart.3), recap
Focal Point (recap.1:end → END, swell after recap.3). Check: no overruns, sync or transition flags. `vk final`
prints "handover MISMATCH: ch3_s8_recap … ends the chapter": expected, s8's `# handover: next` is the join to ch4.
- Rewritten for the ear (re-voiced; QA and a Gemini re-listen came back clean): check.1 "ay" (+qa "AI") →
  "A" after a noun or at a phrase end, per the producer's ch1 note ("flip-flop A is not see and not A", "bee
  exclusive-or A", "bee and A"; the screen keeps D_a = ā·c̄, D_b = a ⊕ b, D_c = a·b); check.3 bit strings
  (+qa, an extra "one" in "one, one, one") → "…and finally all ones", "And the all-ones state goes to one,
  one, zero. Both are used."; stuck.3 "Now look back" (Gemini "book") → "Now go back"; preset.1 "a switch in
  the clock line" (Gemini "cock") → "a switch on that wire"; preset.3 "ignore its input" (Gemini "inplit") →
  "ignore whatever arrives at input dee".
- Accepted voice flags (Whisper only, meaning unchanged): loops.2 "goes round a" → "goes around a". The
  writer's watch list ("flip-flop ee", "not see", "active low", "initialise", s4's code list) passed the
  full Gemini listen.
- Scenes: 8/8 by Opus scene-builders in dependency batches (s1, s3; then s2, s6 from s1 and s4, s5 from s3;
  then s7 from s6; s8 last), two review rounds (Gemini per scene + holds). Handovers: s1 → s2 (s1's
  `handover_shot()`, ring with LEDs and wave panel) and s6 → s7 (ring with open clock switch and d/e set
  pins + buttons), both 0.00% on `vk check`; s8 ends on `end_card()` for ch4 s1.
- Producer decisions applied: s1 opens on ch2's end card (held 0.7 s; its part line then travels into the title
  card); every "?" is RED (ch2's join colour); s4's rings rebuilt on ch2's `five_ring()` (was ch1's
  `state_ring()`).
- Accepted check flags: small text from the ring's own D/Q/"output" labels at the scale that leaves room for
  the wave panel (s1, s2, s6, s7; ch2 accepted the same), the shrunk card/ring reminders in s3 clip 3 and s4
  (the brief asks for them small), s7's table (size 25, the room under the ring), s8's thumbnails; dwell
  advisories where cue spacing sets them (s1 ch2 frame 0.7 s, s2 student bubble 7.1 s, s5 "8 loops", s6
  "clock disconnected", s7 set-pin levels, s8 r6 level pulse).
- Accepted review claims (not real on frames, or by design): s1 0.0 s "flash frame" (the ch2 join, required),
  1.0 s "Starting in an unused state" (Gemini's misreading of the title), 4 s Q̄ stub on e (ch2's ring);
  s3 71/75 s "no 101→110 / 111→001 arrow" (frames show both, after they were lengthened); s4 58/63 s "arrows
  late" (frames: they draw on their words), 91 s "101 shows 0" (after {xs}); s5 46/47 s "00000 high, 11111 low"
  (traces were right; 0/1 level labels added), the "10010" row label (the start state that reads 1,0,1,0,0 as
  said); s6 0 s "output c" (ch2's ring label sits beside c), 30 s highlight "on the LED" (it ringed the bubble;
  LED now dims meanwhile); s7 26 s "wave pre-drawn" (the ghost; dimmed to 0.25), 63 s "c stays set"; s8 20 s
  r3 line in panel 6, 44 s "hot bit skips", 53 s "nothing lit"; "light" → "layt" (s3; a focused listen was
  clean).
- Glitches (scene reviews, confirmed on frames by the builders unless noted):
  - s1 ~15 s and s2 0 s: "stray circle on the feedback wire above e", "LEDs shifted right, none on a". s1's LEDs
    were small dark circles on stubs off each Q wire, e's at the feedback wire's corner, read as inverter
    bubbles. Fixed in `ring_leds()`: GREEN-ringed LEDs directly above their own boxes, clear of the wire.
  - s2 ~36.5 s: "a 0 frozen on the feedback wire". The riding 0s outlived their clock pulse (0.4–1.3 s against
    0–0.6 s). Fixed: riders and pulse run together and fade at the D inputs. s2 ~28 s: "two stacked rows of
    zeros" (riders plus the bright digits under the boxes). Fixed: the digits fade while the riders travel.
  - s2 stuck.1 (holds): the RED "?"s sat on the new LEDs; now inside each LED ring.
  - s3 ~17 s: "stray RED segments at the unused circles": `set_fill(RED)` filled each arc into a crescent whose
    ends poked past the circles. Fixed: stroke-only `CurvedArrow`, rim to rim. s3 ~7 s: "quote over the
    flip-flops": the quote's fade-out ran for the whole move. Fixed: fade out, then fade in.
  - s3 `remedy_card().word()` counted spaces (Text has no space glyphs), so word flashes landed on the wrong
    letters (s5 ~80 s "boxes 'asynchronous'"; s3/s4 "eventually"). Fixed in the helper; s5 now colours
    "Clear"/"Preset" YELLOW in place instead of flash boxes.
  - s5 ~64 s: "exactly two 1s, side by side" outlived loops.3. Fixed. ~60 s "middle 0 underlined in 10001":
    not on frames (underlines growing in); a GOLD wrap arrow was added.
  - s6 ~61 s: "held at 0" caption over the previous one. Fixed (fade out first). ~75 s: d/e's S labels and
    buttons on the feedback wire (handover shot). Fixed: S pin left of the LED, label under the wire, button
    above the loop. ~74 s "white rectangle round c": c's own box at full brightness before the ring faded in;
    the lead is now under 0.5 s.
  - s7 ~17 s: corner table at size 14–17 read as "11000 twice": enlarged to 25. ~48 s: the small flat trace read
    as "a stray green underline": now a mini CLK/output scope. ~11 s "duplicate GOLD 1": the S-pin level was
    GOLD like the state digits; now RED. ~30 s LED fill lagging the moving 1s mid-step: steps tightened.
    FlashAround on the glyph "S" → `pin_pulse()`.
  - s8 ~39 s: the grid cleared panel by panel, leaving the bottom row behind; now one fade.
- Final-video reviews (viewer + transitions) on the first final (596.8 s); one fix round, each confirmed on frames
  by its builder, then re-finalled (not re-reviewed, per the one-round rule):
  - s2 ~54.7 s stuck.3 {missing} (both passes): "a duplicate row 11000 between rows 4 and 5" / "stray 11000 and
    10001 under 00000 → ?". The stepping DIM "00000 → ?" row's RED "?" sat 0.2 from the table's left edge and
    read as part of each row it passed. Fixed: the DIM row sits 1.2 clear of the table.
  - s3 ~17.4 s power.1 {stuck}: "two captions collide, illegible": the p. 127 captions crossfaded in place
    (a transform between unlike texts). Fixed: the first fades out completely, then the second fades in.
  - s4 ~47.1 s check.2 {selfstart}: "'self-starting' covers 101": the tag slid down through node 5's code while
    appearing. Fixed: both tags rise in from below and settle clear.
  - Accepted: s1 0.0 s ch2 join (both passes; required by the producer); s4 "exclusive" → "excuisive"
    (Gemini-only, medium; the focused listen of check.1 was clean); s5 row label "10010" (the start state that
    makes the wave read as said); s7 ~26.8 s "bits shift leftward, output starts high" (frames: b draws 0,0,1,1,0;
    the readout is in e d c b a order while the boxes run a→e) and ~52.8 s "c and d lit" (the run ends at
    01100; the LEDs then go dark before power-up).
- For ch4: ch4 s1 opens on `load_scene("ch3_s8_recap").end_card()` (eight unconnected flip-flops on a CLK bus,
  LED 0 lit GOLD, "Part 4 · One-hot" T 40 at y 3.2). Other helpers: ch3_s1_hook.py `ring_leds()`, `set_led()`,
  `wave_panel()`, `ghost_wave()`; ch3_s3_powerup.py `remedy_cards()` (`.cards[i].word()`), `selfstart_tag()`;
  ch3_s4_check.py `check_rings()`, `checked_ring()`; ch3_s5_loops.py `loops_row()`, `loop_icon()`; ch3_s6_preset.py
  `preset_ring()`, `pin()`, `push_button()`, `press()`, `toggle()`/`flip()` (ch4 s6 brings back the set pin and
  "the same trap").

## Chapter 4 · One-hot
2026-11-01: DONE. `out/ch4_one_hot.mp4`, 9:43 (583.1 s, 1920×1080, 60 fps); narration 9.0 min. 8/8 scenes by
Opus scene-builders in dependency batches (s1, s3; s2 from s1; s4 from s3's handover; s5, s6, s7 from s4's
circuit; s8 last), two scene-review rounds (Gemini per scene + holds), then the final viewer and transitions
reviews: no confirmed findings, so no re-final. Handover s3 → s4 0.00%; `vk final`'s "handover MISMATCH:
ch4_s8_recap … ends the chapter" is expected (s8's `# handover: next` is the join to ch5). Music `music/ch4.json`:
hook Stepwise (to onehot.1), s4 circuit-run stretch Gnomon (lamps.2:end → compare.1), recap Endpoint
(recap.1:end → END, swell after recap.3).
- Brief additions (continuity review's gaps): s2 {why} clears the quote card and cost columns, the row of eight
  returns centred with a YELLOW "?" (gone at {simple}); s8 {recap} is a "Recap" heading over six faint slot frames
  on ch2_s8's 3 × 2 grid, filled with this chapter's own visuals.
- Producer decisions applied: s1 opens on `load_scene("ch3_s8_recap").end_card()`, held 0.7 s, its part line
  travelling into the title card (title then fully up 2.0 s); s6's six loops in ch3 s4's ring style (nodes with
  four-bit codes, arrows per loop), the wrong lamps (red with green, YELLOW "!") and no RED paint; one-hot
  flip-flops r, ra, g, a "one per state", Lecture 9's R, A, G "one per lamp" (s3 tag, s5 labels).
- Rewritten for the ear (all re-voiced; Whisper QA and `vk listen --only` came back clean on each):
  ring.4 "with no next-state logic at all" (+qa "next-date") → "and it needs no logic at all to work out the next
  state"; lamps.1 "Those two outputs are joined by an or gate" (+qa "or date") → "An or gate joins those two
  outputs."; compare.1 "takes the exclusive-or of the red and amber outputs" (Gemini + qa "exclusively or") → "is
  fed by an exclusive-or gate, which takes the red and amber outputs", and "each lamp is just its flip-flop's
  output" (Gemini "foot-flop's") → "each lamp is driven straight from one of the flip-flops"; fast.4 "has an
  exclusive-or gate and an and gate inside its loop" (s7 review "excusifer") → "has two gates inside its loop, an
  and gate and an exclusive-or gate"; lamps.2 "are joined by a second or gate" (s4 review "er gate") → "so another
  or gate joins those two flip-flops".
- Accepted voice flags (Whisper only, number format): fast.3 "3.3 GHz", "200 MHz". The writer's watch list
  ("red-and-amber" vs "red and amber", "or gate"/"and gate", "dee inputs", "clock-to-output", "three point three
  gigahertz", "the British order", "hot one") passed the full Gemini listen; the final viewer review heard nothing.
- Accepted check flags: s5's small text (both circuits side by side at ~6.2 units, as the brief asks); dwell
  advisories where cue spacing sets them (s1 title 2.0 s and the 0.7 s ch3 join; s4 "output logic: 2 OR gates"
  4.5 s; s5 "best depends…" at its limit; s7 "flip-flops alone" 2.9 s, "slower of ⊕ and AND" 4.3 s; s8 r6
  caption 4.3 s; every stepping 0/1 digit).
- Deviations from the brief: s3's one-hot codes and table rows appear with flashes instead of flying (flights ran
  over the pin labels); s6 shrinks the circuit to 0.5 with its labels faded out; s7 and s8 drop the D/Q letters
  and tiny lamp heads in their small circuits (they read as tofu); s7 loads L8's `path_diagram()`/`budget_bar()`
  by file path from ../l08-timing-metastability (breaks if L8 moves); s8's tape pattern 01111110 is its own pick.
- Glitches (confirmed on frames by the builders unless noted):
  - s1 hook.2 18–29 s: "9 flip-flops". Layout, not a transition: the binary trio sat flush against the row of
    eight and read as one 12-cell row. Fixed: 2.0-unit gap, "?" in it, the trio on its own CLK line.
  - s1 hook.2 ~28–35 s: "stepping stops at state 4, then one tick and freezes". The ticks ran only between cues.
    Fixed: a fixed 1.4 s tick grid through the end (one 7 → 0 wrap seen).
  - s2 onehot.2 ~29 s: "cell 4 blank, the 1 skips a cell". The per-cell swap faded the old digit out before the new
    one faded in; round 2 still had the label and fill fading over the whole tick, so the next label lit ahead of
    the 1. Fixed: digit, fill, label and "hot" tag switch on one frame mid-step.
  - s3 ring.4 ~87 s and s4 lamps.3 ~58.4 s: "all four cells 0" / "g shows 0 during green". `ring4().step()` faded
    the 1 out before fading it into the next cell. Fixed in `ring4()` (the new 1 lands before the old one leaves;
    the brief overlap then read as "r 1 alongside a", accepted) and in s4 with a local `slide_step()` (the 1
    slides along the wire).
  - s3 ring.2 ~32 s: "flip-flop a blank". ring.1 drew the cells empty and 1000 faded in late. Fixed.
  - s4 lamps.3 ~49 s: "the loopback wire never highlights" (both rounds). The flash crossed the long top stretch
    too fast to see. Fixed: even speed, stroke 9. ~55 s "state dot moves counter-clockwise": it cut straight
    across the small ring. Fixed: an inner track beside the arrows.
  - s6 demo.3 ~51.5 s: "stray orange switch contact on CLK". The GOLD flash for the a → r feedback wire wasn't
    moved onto the drawn wire and cut across the flip-flops at Q height. Fixed.
  - s6 {loops} ~61 s: "five dots on the 4-state loop, four on the 2-state loop": ch3 s5's `loop_icon()` places 5
    positions. Redrawn in ch3 s4's ring style (producer).
  - s7 fast.2 ~26 s: "T_c ≥ t_pc + t    su". The equation edit matched t_pd's "t" with t_su's "su". Fixed: "t_pd +"
    fades as one piece, then the gap closes.
  - Not reproduced or by design: s1 0.0 s the ch3 end-card join (required, as in ch3); s1 21 s "two flip-flops"
    (my frames from the final show three); s2 1 s "stray flip-flops" (the waiting trio, now tagged "binary"); s2
    36 s wrap arrow, 45 s "8 over the row" (a near miss, now clear); s2 ~26 s (final transitions) "labels on one
    line, too high, then jumping" (my frames: a staggered fade-in with an upward drift); s3 70 s highlights; s4
    46 s ra → g; s4 0.0 s "a's head red and amber" (correct at full size; the heads are ~0.14 units); s6 55 s Q
    labels; s6 69/71 s "1010's head amber and green" (three passes; frames show red and green); s6 69 s "switches
    to 0001" (the small circuit keeps running the used loop, per the brief); s7 57 s OR gates; s7 62 s "AND
    missing" (circuit not yet on screen; gates enlarged anyway); s7 88 s "burus" (Write mid-stroke of the "n");
    s8 13 s "three ORs", 22 s "stray A" (the amber lamp's label), 33 s "9 bits"; s8 42 s Part 5 header vs chip.
- Open for the producer: s7's verdict shows s2's "8 vs 3" as the brief asks; three Gemini passes expected the
  traffic light's "4 vs 3". Change it only if you prefer the traffic-light numbers.
- Shared helpers (module-level in scenes/): ch4_s1_hook.py `onehot_row(n, hot, side, pitch)`, `binary_trio()`,
  `cell_box()`, `hot_bit()`; ch4_s2_onehot.py `bullet_strip()`, `flip()`; ch4_s3_ring4.py `ring4(bits)` (`.ffs .cells
  .bits .labels .heads .wires .wire_paths .clk .bit_pos(i)`, `.step()`), `place_code()`, `final_ring()`,
  `handover_shot()`; ch4_s4_outputs.py `onehot_circuit(bits)` (`.ring .gates .g_wire .lamps .light(state)`),
  `slide_step()`, `ring_track()`; ch4_s5_compare.py `l9_circuit()` (Lecture 9's R, A, G circuit); ch4_s7_fast.py
  `hide_heads()`; ch4_s8_recap.py `end_card()`.
- For ch5: ch5 s1 opens on `load_scene("ch4_s8_recap").end_card()` (same as `handover_shot()`, the last frame
  of ch4): a tape of white bits stopped at `END_OFF` with `01111110` outlined YELLOW every 16 bits (s8's pick:
  ch5's script names no pattern, so ch5 may reuse it), three empty BLUE circles in p. 123's layout (A, B on
  top, C below), the chips "Part 5: two flip-flops" (lit, YELLOW border) and "Part 6: one-hot" (DIM), and
  "Part 5 · Hunt, Sight and Sync" (T 40, y 3.2). Parts: `.tape .circles .chips.lit .chips.dim .part`.

## Chapter 5 · Hunt, Sight and Sync
2026-11-01: DONE. `out/ch5_synchroniser.mp4`, 11:56 (715.6 s, 1920×1080, 60 fps); narration 11.2 min. Music
`music/ch5.json`: hook Hypothesis (START → frames.1), s7 circuit stretch Reflections (finish.3:end → finish.5), recap
Clarity (recap.1:end → END, swell after recap.2). Check: no overrun, sync, layout-collision or transition flags.
- Scenes: 8/8 by Opus scene-builders in dependency order (s2, s3; then s4 from s3's handover, s5, and s1 once ch4's
  `end_card()` was recorded; s6 from s5; s7 from s6; s8). Two review rounds (Gemini per scene + holds), then the final
  viewer + transitions reviews, one fix round from those, re-finalled (not re-reviewed, per the one-round rule).
  Handovers s3→s4, s5→s6, s6→s7 match at 0.00%. s4 ends empty, and s5 fades the coded diagram in at s4's placement.
  `vk final`'s "handover MISMATCH: ch5_s8_recap … ends the chapter" is expected: s8's mark is the join to ch6.
  **If ch4 changes its `end_card()`, re-render ch5 s1.**
- Rewritten for the ear (all re-voiced; QA and `vk listen --only` came back clean on each):
  - hook.3 "with states called ay, bee and see" (producer's A rule) → "You saw its diagram in part one. Back then,
    its three states were just letters, state A, state bee and state see."; "Now they get names" (QA "maims") →
    "Now they're called Hunt, Sight and Sync, and the machine has a job."
  - frames.3 "the machine's output, ess," (s2 review: "seconds") → "output, called ess,"; frames.4 "why have ee at
    all" (QA "why heavy at") → "why do we need input ee at all".
  - diagram.3 "stays in Sync" (Gemini "sing") → "stays in the Sync state"; "the receiver is locked on" (two reviews:
    "locked ont(d)") → "has locked on to the sequence".
  - codes.1 "Call their outputs" (Gemini "ess ess") → "We'll call their outputs…"; codes.3 "one in Sync" (Gemini
    "sank") → "in the Sync state"; "the output, ess, is just ess one" (Gemini "ess ess", then "ess ess one" again) →
    "So the output is just flip-flop one's output."; "also has ess one at one" (+qa "esses one") → "would also give
    a one".
  - table.1 "On the left" (QA "weft") → "The first two columns hold the current state"; kmap.3 "Now plot the ones"
    (QA "pot") → "Now put the ones of ess one prime on the map."
  - kmap.4, the three loop terms, after several takes ("ES, E0", "termizes", "ess ess zero", "and" → "end", "term" →
    "germ" +qa): now "That's the term ess one and not ee." / "That group gives ess one and ar." / "That pair makes
    the term S zero and ee and ar." (a capital S, tried like the A/K/N rule; listen clean).
  - finish.1 "Hunt with ar one" (QA "their one"), "Sight with" (QA "Psych") → "In Hunt, when ar is one, the table has
    a single row, …" / "In Sight, when ee is zero, two more cells fill, …"; finish.4 "joined by an or gate." (QA "or
    date") → "…joined by an or gate at the end."; recap.1 "Let's recap." (Gemini "Must") → "Time for a recap."
- Accepted voice flags (Whisper only or number/spelling format): bit strings as digits (codes.2, codes.3, kmap.2,
  finish.3); "S1'" (table.1, kmap.3); kmap.4 "in Sight's row" → "incites" (the Sight/site homophone); finish.5 "five
  and gates" → "five end gates", "seven in all" → "seven and all" (Gemini listen heard both right; ch2 precedent);
  the final review's s7 "and gates" → "in gates" (medium, not in the listen). The writer's watch list ("Tripos",
  "ee", "ar", "ess one prime", "meta-stability", "and gates, and two or gates", "an ex") passed the full listen.
- Accepted check flags: small text on the shrunk coded diagram (s4–s6 opening, 0.55 scale, 16–24 pt: the brief
  shrinks it beside the table), s7's corner D1 thumbnail and the shrunk circuit beside the scoreboard, s8's recap
  tiles (r4 table 15–16 pt); dwell advisories where the cues set them (s2 "8 or 16 bits", L8 inset, "wrong frame",
  closing caption; s3 "?" 2.3 s, "two places to go"; s5 "never sees 11"; s7 ghost zeros, "free", "two essential
  groups"; s8 r5 before {next}).
- Accepted review claims (not real on frames, or by design): s1 0.0 s ch4's end card (required); s1 "A, B, C renamed
  Sync, Hunt, Sight" (intended); s1 ~27 s "?" fixed while the stream runs; s3 grid cells (frames: ē fills the top
  row), Sync's e·r loop "disappearing", Sync loop "flicker" (the arc flash); s4 "clock triangle misplaced" (L6
  `make_ff` clocks on the bottom edge; the "jump" was the output arrow; triangles enlarged); s5 "row 8 omitted" (lands
  66.0–66.5 s), {xx} boxing only next-state X's (brief), "D1 equation at 109.7 s"; s6 [11] kept from {d1} to {xrow}
  (brief), "doubled [11]" and "ghost s0·e·r" (a single fading label on frames); s7 "s̄1 on D1's first gates" (three
  Gemini passes; a full 1080p frame shows plain s1), "traffic light header misplaced", "ghost [11] at the s7 → s8
  join" (not in the re-final's frames); s8 "Part 11" (not on frames; now fades in place), codes during {next}.
- Glitches (confirmed on frames by the builders, all fixed):
  - s1 hook.2 ~23 s: a pattern box read as 10 bits. s2's `pattern_box` is 8 bit-spacings + 0.08 wide, so its edges
    sat on the neighbouring digits. s1 and s8 now use exactly 8 spacings with YELLOW boxed bits (s2 keeps its own).
  - s1 hook.3 ~34 s: three "?" lingered over the Tripos card: `sweep_clear`'s lagged fade cleared them last while the
    card faded in. Now they fade first. ~43.4 s: a stray vertical line beside A: `FlashAround` on a Circle (its
    bounding box), as in ch1; now ch1's `ring_flash`.
  - s2 frames.4 ~70.6 s and ~82.1 s: the r trace "melted" into curved humps: `Transform` between r traces with
    different point counts. Now the chance pulse is its own piece, faded in and out. Same beats: the swapped digits
    rose above and below the tape (`swap`'s default shift); now `shift=None`.
  - s3 diagram.3 ~56.8 s: the gently bent Sync → Hunt arc, drawn with `Create`, read as a straight stub into empty
    space. Now it fades in whole, then a flash runs Sync → Hunt.
  - s5 table.5 ~98 s {expand}: Hunt's row 1 vanished mid-split (old row out over 0–45%, new rows in from 50%). Now row
    1 stays and a copy fades into a gap under it. table.4 ~68.5 s: `FlashAround` on the DIM [11] hardly showed; now a
    YELLOW pulse. table.5 end: the captions sat inside the bottom margin and under [11]; re-placed under the table.
  - s6 kmap.2 ~17.6 / ~20 s: stray dots beside the grid: `Create` on the bar lines starts as a dot; now `FadeIn`.
    s6 kmap.4 ~75.9 s and s7 finish.2 ~27 s: `Create` on rounded loops drew a corner tick / a stroke past the grid
    edge; loops now fade in in place.
  - s7 finish.3 → 4 ~65 s: "two essential groups" alone on an empty frame: `sweep_clear` faded it last (last
    added). Now one fade. s8 r5: the "sequential 2 7 none" row touched its caption (0.12 apart); now 0.26. s8 r3:
    `s = s1` sat by Sight and faded in before it was said; the object is dropped, the caption's line lands on "ess one".
- Departures from the briefs: s1's title card is up 2.3 s (the one-hot ring arrives on "one-hot"); s1's letters swap
  (not morph) into the names; s2's GREEN ticks sit above each copy in clip 2 (no receiver box until clip 3) and the
  L8 inset has no labels; s4's ladder reads "1 flip-flop: 2 patterns", "2: 4" (ch1's helper wording); s6's map
  slides to the centre for the loops (table and [11] cleared); s8's r3 is a compact triangle of coded circles.
- Shared drawings for ch6 (standalone helpers in scenes/, load with `load_scene(stem)`):
  - ch5_s3_diagram.py `sync_diagram(codes=None, unused=False, r=0.62)`: p. 139's diagram on ch1's `moore_diagram`
    positions (Sync (-3, 1.9), Hunt (3, 1.9), Sight (0, -1.2)), YELLOW names at size 32; `.circle[name]
    .name[name] .by_state[name] .code[name]`, `.circles`/`.names` in (Sync, Hunt, Sight) order, `.arcs .labels` in
    ch1's order; `codes` is a name → string mapping (GREEN [..] above Sync and Hunt, left of Sight); `unused=True`
    adds the DIM [11] circle at (4.6, -2.3) as `.unused`. `handover_shot()` = the bare diagram.
  - ch5_s4_twoffs.py: `coded_diagram()` (scaled 0.55 about the origin, then shifted (-3.9, 0.05); spans x
    -6.58…-1.03), `ff_pair()`, `output_table()`, `s_eq()`, `nologic_wire(pair)`.
  - ch5_s5_table.py: `state_table(rows, heads, titles, head_colors, breaks, dim_rows, x, filled)` (one string per
    column group per row, e.g. ("00","X0","00"); `.titles .heads .rows[i] .cell(i,g,j) .col .row_y .make_row .hrules
    .vlines`), `sync_table()`, `coded_diagram(codes=None)` (one-hot codes at the same placement).
  - ch5_s6_d1.py: `kmap4(values, center, scale, title)` (`.sq .pos .value .edge .ent`), `loop4`, `loop_label`,
    `term_eq(lhs, terms, colors, cx, y)`, `d1_parts`, `d1_shot(cx)`; `D1_MAP D1_LOOPS D1_TERMS D1_COLORS EQ_XS MAP_Y`.
  - ch5_s7_d0.py: the D0 map (s6's `kmap4`), `sync_circuit()` (`.ffs .qlabels .clk .d1 .d0 .ands .ors .out .inv
    .inputs`; gate inputs as labelled stubs) and `sync_board(with_row=True)`: ch2's `scoreboard()` at native scale
    with ch4's "traffic light" rows, the "synchroniser" sub-heading and "sequential | 2 | 7 | none", placed at x
    -6.5…-0.05; the row is slot 7 (y -1.9), and slot 8 (y -2.5) is free for ch6 s7's one-hot row (`sb_cell()`).
  - ch5_s2_frames.py: `bit_tape(bits, y)`, `bx(i)`, `PATTERN` (01111110), `COPIES` (1, 19, 37), `FRAMED`,
    `pattern_box(i0, y)`, `r_trace(extra)`, `e_trace()`, `trace_label()`, `pulse_bump(i)`.
  - For ch6 s1: `load_scene("ch5_s8_recap").end_card()` (= `handover_shot()`, the last frame): s3's diagram (codes
    faded) at the left with the arcs into Sync YELLOW, three flip-flops labelled Hunt, Sight, Sync, GOLD "3
    flip-flops", a small DIM K-map with "no K-maps", and "Part 6 · One-hot, straight from the diagram" (T 40, y 3.2);
    parts `.diagram .ffs (.ffs.ffs, .ffs.names) .tag .kmap .kmap_tag .part`. ch4's `part_chips()` sets `.dim`,
    which shadows `Mobject.dim`: animate its chips separately.

## Chapter 6 · One-hot, straight from the diagram
2026-11-01: DONE. `out/ch6_onehot_sync.mp4`, 11:06 (666.2 s, 1920×1080, 60 fps); narration 10.7 min. Music
`music/ch6.json`: hook Resonance (START → codes.1), s6 arc-reading stretch Spirals (arcs.1:end → arcs.4), recap
Far Away (recap.1:end → END, swell after recap.3). Check: no overrun, sync, layout-collision or transition flags.
- Scenes: 8/8 by Opus scene-builders in dependency batches: s2 first (owns the shared drawings, and an
  `opening_shot()` that s1 ends on), s3 from s2's handover (owns the equation style), then s1 (on ch5's `end_card()`),
  s4 (s3's handover), s5, s6, s7; s8 last. Two review rounds (Gemini per scene + holds), then the final viewer +
  transitions reviews: nothing confirmed there, so no re-final. Handovers s1→s2, s2→s3, s3→s4 match at 0.00%;
  `vk final`'s "handover MISMATCH: ch6_s8_recap … ends the chapter" is expected (the end card → Lecture 11).
  **If ch5 changes its `end_card()`, re-render ch6 s1.** Producer's brief fix applied: s7's board is ch2's
  `scoreboard()` at native scale via ch5_s7's `sync_board()`, new row "one-hot | 3 | 8 | none" in slot 8.
- Rewritten for the ear (all re-voiced; QA and `vk listen --only` clean on each):
  - "ess zero" was heard "ess ess zero" / "ess ee zero" (Gemini high, several +qa) in rule.1, rule.2, rule.4,
    dzero.2, dzero.4 and recap.1: those sentences now write a capital "S zero" ("S one", "S two" alongside in rule.1
    and rule.4), as ch5's kmap.4 did. Listen clean. Unflagged lines keep "ess zero". Candidate course voice rule.
  - codes.1 "hops from flip-flop to flip-flop" (s2 review "foot-flop", Whisper base) → "hops from one flip-flop to
    the next"; codes.5 "like zero, zero, zero, or one, one, one" (QA ×3: an extra "one") → "like all zeros, or all
    ones", and "in one of the three used states" (review "use states") → "staying in the three states we use".
  - inspect.4 "or ess one, ee and not ar, or ess two, ee and not ar" (QA "S Sue") → "or ess one, and ee, and not
    ar, or ess two, and ee, and not ar".
  - dzero.3 "check it with a truth table. There are only four rows." (QA ×3 "truce table") → "check it in a table.
    It has only four rows."; dzero.4 "not ar and ess zero, or not ar and ee" (QA "RNA") → "S zero and not ar, or ee
    and not ar" (the screen keeps p. 142's r̄·s0 + r̄·e), "you were either hunting already, or expecting it" (QA
    "you are") → "either you were hunting already, or you were expecting it", "in Sight or Sync" (QA "Cider") → "in
    Sight, or in Sync".
  - arcs.1 "Here's the last surprise." (two scene reviews "Hue's") → "And now, the last surprise."; arcs.2 "Sync's
    own loop, labelled not ee" (Gemini "naughty") → "Sync's own loop, taken when ee is zero".
  - recap.2 "to one-hot." (Gemini "one hopped") → "all the way to one-hot codes."; recap.3 "can save flip-flops, and
    leave more don't cares" → "can mean fewer flip-flops, or more don't cares" (s8 review: four states on two
    flip-flops leave no unused codes, so "and" was wrong for the pictured example; "save" was then heard "say"). The
    end card shows a DIM "or" before the K-map of X's.
- Accepted voice flags: rule.1 "every used state" → "use state" (Whisper only); dzero.4 "S zero" → "S0" (format);
  inspect.3 "not ee" → "not he" (first full listen, medium confidence, not re-flagged). The writer's watch list
  ("not ee"/"not ar", "the output ess equals ess two", "Sync's own loop", "the or of those three terms") passed
  except arcs.2's "not ee", rewritten above.
- Accepted check flags: small text in s8 (recap tiles, the shrunk scoreboard at 18 pt, road thumbnails 9–13 pt, as
  ch5's recap); dwell advisories where the cues set them (s1 ch5 end card 0.7 s, title, inset digits; s2 hopping 0s,
  ≠, ghost row; s3 dashed slot; s4 factored D2, "Part 3"; s5 (s1+s2) line, 1·(s0+e); s6 table ghost, comparison
  lines; s7 "no output logic", quote card, raw D0, "−3"; s8 r6 panel, road).
- Departures from the brief (builders, for the small-text limit or overlap): diagrams enlarged where shrunk (s2's
  "top"/"left" placements circles r 0.9, names ~26; s1 a 0.7 side placement; s5 a 0.85 local diagram; s6 circles r
  0.78); s3 has no small diagram in the corner (row/column boxes instead); s4 clip 3's diagram is large under D2 and
  the stack's name tags fade when it shrinks; s1's small K-maps have no headings; s7's thread sits right of the board
  (no room under it); s8 adds a DIM "Next lecture" line and the "or"; terms appear in place where a flight would cross
  text (s3, s6).
- Accepted review claims (not real on frames, or by design): s1 0.0 s ch5's end card (required), ~4 s "two Sight →
  Sync arrows" (the second e·r is Sync's loop label), ~7.2 s "Sight pulse skipped" (frames: 7.6/8.2/8.8 s), ~35.8 s
  arc shimmer (brief); s2 ~86 s rows 7/8 (data right, mid-build); s3 "ε" header; s4 ~26 s Hunt tick (lands ~30 s),
  ~48 s "Sync" tag (by design); s5 ~79 s arcs (frames: 3, 7, 2 lit; their labels now light too), ~31 s p. 142's
  line "stray" (brief), ~63 s lingering ticks (frames: none), ~77 s Sync → Hunt "omitted" (lights on "expecting
  it"); s6 ~70–72.5 s flip-flop bits (frames: 0 0 1 with Hunt hot, arc 4 lit), ~90 s lines (settled frame right);
  s7 ~7 s D2 (frames: present), quote paraphrased (brief), "Lecture 9" row name (ch4's), Hunt box GOLD through clip 2
  (the extra flip-flop); s8 "in one line" over the board (brief), ~34 s "Lecture 9 white" (frames: plain), ~17.5 s
  grouping (low).
- Glitches (confirmed on frames by the builders, all fixed unless marked accepted):
  - s1 hook.1 3.6–3.8 s: the title card still fading out under the incoming diagram (`sweep_clear(self,
    *appear(d, lab…))` overlapped the halves). Now sequential with a brief empty frame.
  - s1 hook.1 ~16 s: in the small D1 map the TEAL s0·e·r and PURPLE s1·r loops shared their right edge and read as
    one 3-cell group. TEAL is now a narrow pill; dimmed loops keep 0.75 opacity.
  - s1 hook.2 ~25.6 s: the new s2 flip-flop showed without its label (`appear(ffs[0])` staggered the pieces). Now
    one object. ~34 s: the old "FF labels" still fading while the diagram grew back; leavers now go in the first 30%.
  - s3 inspect.1 ~23.5 s: the "Sight" tag faded in on top of a caption 0.6 below the term; caption lowered.
    inspect.4 ~99.5 s: the column and row boxes outlived the table (`sweep_clear` fades in on-screen order and they
    were last); now first.
  - s6 arcs.3 52.2–52.6 s: `fly_term(..., arcs=(0.8, -1.5))` sent ē on a deep curve to the bottom-left before it rose
    into s1·ē; now it appears in place while the label flashes.
  - s7 verdict.3 ~63.5 s: a stray vertical rule, the fading tail of a full-height `FlashAround(col2)` (and a bar by
    "Complexity" from `FlashAround`); then ~62.6 s the replacement box's outline (`Transform(box, col_box(col2))`)
    clipped the "f" of "flip-flops". Now a fill-only GOLD band with edges in the column gaps, and `FlashUnder`.
  - s8 recap.2 ~31.5 s: "slkding": the six-slot grid fading out (first 50%) overlapped the board fading in (from
    45%). Now sequential.
  - Accepted transients (final reviews, mid-move): s2 ~22.3 s the hopping 1 passes just under Sight's ē label; s2
    ~54.8 s the s wire's first stub as it grows (read as "e"); s4 ~73.8 s "unmsed" mid-morph (two passes; cause not
    checked); s5 ~34 s e read as ε mid-morph; s6 ~24.2 s the "Sight" tag in flight past Hunt (the brief's fly).
- Shared helpers (module-level in scenes/): ch6_s2_codes.py `onehot_diagram(where="native"|"top"|"left")`,
  `place_diagram`, `light_arc(d, i)`, `glow_state(d, name)`, `ROW_ARC` (arcs 0 Sync ē loop, 1 Sync e·r loop, 2 Sync →
  Hunt, 3 Hunt loop, 4 Hunt → Sight, 5 Sight loop, 6 Sight → Sync, 7 Sight → Hunt), `onehot_ff`, `onehot_ffs`,
  `ff_bit`, `hop_path`, `state_var(tex, tag)`, `onehot_table()`, `pattern_chips(state)`, `opening_shot()`;
  ch6_s3_inspect.py `eq_line(lhs, tokens, size, tags)`, `put_line`, `raw_line`, `RAW`, `d_stack()`;
  ch6_s4_onehot_rule.py `check_table(rows)`, `rule_line()`, `final_d2()`; ch6_s5_d0.py `final_line()`,
  `final_pair()`, `truth_table()`, `expr()`; ch6_s6_arcs.py `sync_arcs_shot()`, `big_diagram()`; ch6_s7_verdict.py
  `panels()`, `final_board()` (the full scoreboard), `thread()`, `gate_icon`, `icon_row`, `inv_icon`.
- For Lecture 11: `load_scene("ch6_s8_recap").end_card()` (= `handover_shot()`, the last frame): p. 144's headings
  under a DIM "Next lecture", five circles merged to four (the merged one YELLOW), two flip-flops, GOLD
  ⌈log₂ 4⌉ = 2, a DIM "or", and a small K-map outline with DIM X's.
