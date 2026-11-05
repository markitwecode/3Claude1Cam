# State Minimisation: status

2026-10-31: project created; planning.

## Paused before chapters (producer, 2026-11-01)
Scripts (6, continuity-reviewed) and narration (57.8 min) are done; nothing built, no music. The user
paused for the night after DE L7. Resume: chapter-directors in pairs, 1 + 2, then 3 + 4, then 5 + 6.
Each chapter's s1 opens on the previous chapter's s8 `end_card()` (held ~0.7 s, then the title, as
L10 did); a director whose previous chapter isn't built yet builds s1 last.

Producer notes to pass on:
- all: voice rules in ../COURSE.md, including L10's: capital "A" right after a noun ("state A"), and
  "S zero" not "ess zero" (both already applied to these scripts and re-voiced). Untested here: "eff",
  "gee", "aitch", "em", "pee" for states F, G, H, M, P (try the capital letter if one is misheard, as for
  K and N); acronyms P-L-A, G-L-A, F-P-G-A, C-L-B spelled, PAL and GAL as words; "Xilinx", "Verilog",
  "Altera", "Kirchhoff", "coulomb", "joule".
- ch1: s1 opens on L10 ch6's end card, `load_scene("ch6_s8_recap").end_card()` in
  ../l10-state-assignment. `load_scene` is project-local, so load it by file path, as L10 ch4 did for L8.
- ch2 → ch3: ch2 s7's last frame is exactly ch3 s1's opening (table, green dots, 16 crosses).
- ch4, ch5: reuse L10's synchroniser drawings (L10 STATUS.md ch5 section: diagram, coded diagram, table,
  4×4 K-map, `sync_board()`); ch4's hook uses L10 ch1 s8's 74HC chips. Same state names and codes
  (Hunt 00, Sight 01, Sync 10) and D1/D0 equations as L10 ch5–6.
- ch6 (electricity) starts a new section: its circuit drawings are the first of their kind; record them
  for Lecture 12. The digest's p. 170 figure is wrong; follow the slide (V1 − V2 − V3 − V4 − V5 + V6 = 0).

## Chapter 1 · Fewer states, same machine (director, 2026-11-01): ready for final
- Preview `out/ch1_row_matching_preview.mp4` (480p, 10.4 min); 8/8 scenes by Opus scene-builders, two review rounds
  (Gemini per scene + holds). Handovers s4 → s5 and s5 → s6 match at 0.00%; `vk preview`'s "handover MISMATCH:
  ch1_s8_recap … ends the chapter" is expected (s8's `# handover: next` is the join to ch2 s1). s1 opens on L10 ch6's
  `end_card()` (held 0.7 s); s1 loads L10's file by path and temporarily points `lib.paths.project` at L10 while
  it loads (`_load_other`), since `load_scene` is project-local (the engine has no cross-project loader).
- Accepted check flags: dwell only (s5's 55 are s4's arc labels at t=0, fading out as the diagram shrinks, by
  design; the rest are short clips clearing on the next beat); small text only in s8 (54: the six recap thumbnails
  and the end card's two one-row tables, which the brief asks to be small copies).
- Accepted Gemini visual claims (not on frames or by design): s1 0 s L10's end card, 17.5–19.5 s J and L GOLD (the
  brief's {pairs}); s3 ~61 s / ~85 s brace and long form (mid-fade; rows verified correct); s4 ~53 s counter on
  bit 1 (reset for the next word); s5 ~48 s labels gone (by design); s6 0–2 s "row N missing" (present), ~52 s and
  ~90 s the reading band and pairwise scan; s8 ~26 s r2 table vs caption (mid-move; settled frame clear), ~55 s
  "P" vs "p" (lowercase on frames).
- Music `music/ch1.json`: hook Quaternions (to c1.why.1), s4 Centroid (c1.tree.1:end → c1.tree.3), recap
  Transformation (c1.recap.1:end → END, swell after c1.recap.3:end).
- Built in order: s2, s3, s4; then s1 (L10 ch6's `end_card()`, s4's diagram), s5 (s4's handover), s7; then s6
  (s5's handover); s8 last.
- **Shared drawings for ch2/ch3** (module-level in scenes/, load with `load_scene(stem)`):
  - ch1_s3_mealy.py: **the state-table style** `state_table(rows=MACHINE, size=30, pitch=0.37, top=2.45, x0=0.0,
    rules_after=("A","C","G"))`, rows as (state, n0, n1, y0, y1); `.rows[r].cells`, `.cell(r, c)`, `.col(c)`,
    `.row_of(letter)`, header `.h_cs .h_ns .h_out .subs .xs .y`, `.rules .seps`, `.col_box(cols)`, `.row_box(r)`;
    letters lit as spoken with `recolor`; after `appear(*rows)` call `settle(scene, tbl)`. `MACHINE` = p. 145's 15
    rows; `moore_schematic()` (L10's, rebuilt from its helpers).
  - ch1_s4_tree.py: the 15-state diagram `tree_diagram(labelled=True, zeros_dim=True, bundle=True, ones=True)`
    (`.states[name] .arcs[(name, x)] .labels .stubs .bundle .bundle_label .ones`), `mealy_label(inp, out, size=28)`
    (input BLUE, slash FG, output GREEN; `.inp .slash .out`), `place_on_arc`, `NEXT OUT POS`.
  - ch1_s5_hi.py: **the merge animation** (replace: the letter flashes GOLD and turns into its match, the arc
    swings; delete: row and circle DIM, the row leaves, rows close up, the circle slides into its match):
    `replace_entry`, `swing_arc`, `dim_state`, `delete_row`, `merge_circle`, `arc_geometry`; layout
    `layout_table(rows)`, `place_diagram(d)`, `side_by_side(rows)`; `steps_caption()` (`.step1 .step2`),
    `state_counter(a, b)`. ch1_s6_cascade.py adds batched versions (`replace_entries`, `swing_arcs`, `delete_rows`,
    `merge_circles`), `matched_table()`, `ROWS_AFTER_L`, `ROWS_FINAL` (p. 147's 7 rows).
  - ch1_s7_left.py: `seven_diagram()` (the 7-state machine, `.states .arcs[(name, x)] .labels .returns .one
    .path(steps)`, `SEVEN_NEXT SEVEN_POS`), for ch3 s7. ch1_s2_why.py: `ladder()`, `ladder_bracket()`, `code_chips()`.
  - **End card for ch2 s1** (built): `load_scene("ch1_s8_recap").end_card()` (= `handover_shot()`, the last frame,
    held 8 s): part line "Part 2 · When are two states the same?" (FG, T 40, at y 3.2, L10's style); BLUE "0110"
    (Mono 44) at (0, 2.2) with two BLUE arrows down to circles "p" and "q" at (±3.0, 0.75), r 0.55, FG; a GREEN
    arrow from each out to GREEN "0010" at (±5.4, 0.75); under each, a one-row compact table (s3's header, ×0.62)
    at (±3.2, −1.3): "p | B C | 0 0", "q | D E | 0 0"; YELLOW "?" (96) at (0, −0.05); a faint 8-state staircase
    (28 cells of 0.28, DIM, opacity 0.4) at (0, −2.3). ch2 s1 holds it ~0.7 s, then its part line travels into the
    title. **If ch1 changes it, ch2 s1 must re-render.**
- Narration rewritten for the ear (re-voiced; QA and `vk listen --only` clean unless noted): why.2 "Remember the
  ladder" ("latter") → "Remember the doubling ladder"; left.1 "Back to the ladder" → "Back to the doubling ladder";
  why.2 "two give four" ("of four", then "foot flop" for "two flip-flops give") → "One flip-flop gives two patterns.
  Two give four, …" (Gemini still hears "give" as "gives": accepted); tree.2 "state ell" ("EEL") → "state L";
  hi.3 "state dee's right arc swings over to state aitch" ("art", "each") → "the right arc from state dee now swings
  over to state H"; hi.4 "merges into state aitch" (dropped) → "state H"; cascade.1 "match state aitch's row"
  ("Asia's") → "match the row of state H", "state eff's entry for input one" ("s entry") → "the same entry for
  state eff"; cascade.2 "from state aitch, whose" ("IH") → "state H", "replace ell by jay" ("Ella") → "replace L by
  jay"; cascade.4 "replace gee by dee, and eff by ee" ("ghee") → "replace state G by state dee, and state eff by
  state ee", "Then delete" ("Them") → "Now delete"; left.3 "go to state aitch" ("A-ish") → "state H"; recap.2 "In a
  Mealy machine, each arc carries" ("mailing") → "Mealy machines put an input and an output on each arc".
  Later rounds (Gemini review then `vk listen --only`): why.2 "First, fewer states may need fewer flip-flops"
  ("shewer"/"sheer" in two reviews) → "First, a machine with fewer states may need fewer flip-flops"; cascade.1 "and
  both of state gee's entries" ("bose", +qa) → "and the two entries for state G".
  Accepted Gemini review-only claims (not repeated by `vk listen`): s3 "refresher" → "prefresher"; s7 "row" →
  "rau"/"rouse" (×3); s6 "eye" → "one"; s8 "one zero zero one" → "one thousand and one".
  So in this lecture "aitch", "ell" and "gee" are fragile after "state": write H, L, G (capitals) in ch2–3.
- Accepted Whisper flags (spelling only): mealy.3 "letter oh" → "o"; "dee's / gee's / eff's / see's" → "d's" etc.;
  cascade.4 "going round" → "going around".
- Glitches (confirmed with frames):
  - s4 ~29.5 s (c1.tree.2 > bundle): a stray YELLOW square box below/around A; cause `FlashAround` on a circle
    (draws a square). Fixed: a flash travelling round A's outline.
  - s3 ~57 s (c1.mealy.3 > letters): YELLOW rings duplicating/overlapping on B–F; cause overlapping `FlashAround`s
    on consecutive letters. Fixed: each letter turns YELLOW and back in turn. (~85 s "wrong long form" was the fade
    making B and D rows near-invisible; the rows were right.)
  - s7 ~59.5 s (c1.left.4 > name): stray digits and braces of the two words lingering at the right edge; cause a
    lagged clear (`LaggedStart` of FadeOuts) removing the word blocks piece by piece. Fixed: one even fade.
  - s2 ~50–65 s (c1.why.3 > dontcare): the two don't-care X's sat between the chip rows (read as marking 010/011)
    and copies stayed behind after the flight into the K-map; cause the X placed under the chip, and copies flown
    while the originals stayed. Fixed: X centred on its DIM chip, the X itself moves to the K-map.
  - s5 ~30.5 s (c1.hi.2 > forever): the fused dot covered C's centre and vanished abruptly; ~40.5 s the scan band
    slid back up across rows E/K before stopping on D (read as "row E highlighted"); ~48.5 s D's two arrows to H at
    bend 1.2 formed a loop read as "a stray circle labelled D"; ~61 s circle I shrank in place instead of merging.
    Fixed: dot to C's edge then fade; band fades out, box fades in on D; bend 0.8; I slides into H then fades.
  - s6 ~99 s (c1.cascade.4 > keeps): flash rings circled empty space; cause the "H" faded out under the rings
    before the flash (Transform start). Fixed: flash first, then swap to "D". (0 s stray row and 22.5 s wrong cells:
    not on frames.)
  - s2 ~71.5 s (c1.why.4 > nine): a ring drawn over the row-4 brace and its labels; cause `FlashAround` on a tall
    thin Brace, played with the 15 → 9 rewrite. Fixed: flash removed.
  - s5 ~60–61.6 s (c1.hi.4 > merge): circle I (DIM, 0.6 from H) read as shrinking in place. Fixed in s5 only: I
    re-lights GOLD and slides fully onto H, then fades with a GOLD flash on H.
- Fix pass after the final (2026-11-01): no fix, final out/ch1_row_matching.mp4 (10:22.6) stands.
  - Accepted: transitions review, s8 @ 29.6 s (final 09:40.3) "stray graphic of figures holding hands in panel 3".
    Frames of the final at 09:39.3–09:41.7 (5–10 fps, panel 3 cropped) show panel 3 empty, then the fifteen-state
    tree and its caption fading in evenly; nothing else appears. Gemini read the faint, half-faded leaf row
    (circles on stems joined by the baseline) as figures. Not a glitch.
  - The other 11 transitions findings are mid-transition, not acted on. Spot-checked the one marked high (s5 @
    53.6 s, "row N disappears"): row N is present on every frame at 05:44.8–05:46.8. Not real.
  - The s8 "handover MISMATCH" in finalize is expected (s8 hands over to ch2 s1).

## Chapter 2 · When are two states the same? (director, 2026-11-01): ready for final
- Preview `out/ch2_equivalence_preview.mp4` (9:32, 480p, music; plays end to end). 8/8 scenes built; every in-chapter
  handover ok (s1→s2, s2→s3, s5→s6, s6→s7, s7→s8, 0.00% differ); s3→s4 and s4→s5 fade to empty. The producer runs
  `vk finalize 2`.
- Accepted check flag: s8 `end: 208 visible pieces left on screen`: the chapter ends on its end card, which ch3 s1
  opens on (forward join, as ch1's s8 does); no handover mark since it's the chapter's last scene.
- Music `music/ch2.json`: hook Hypothesis (to c2.def.1), s5 Gnomon (c2.grid.1:end → c2.cross.1), recap Endpoint
  (c2.recap.1:end → END, swell after c2.recap.2:end).
- Build order (the p. 150 table is the root every scene needs): s5 (owns the table and staircase); then s1, s2, s6;
  then s3, s7; then s4; s8 last. Joins: ch1 s8 end card → s1 (forward); s1 → s2, s2 → s3, s5 → s6 → s7 → s8
  handovers; s3 → s4 and s4 → s5 fade to empty (topic changes).
- Narration rewritten for the ear (re-voiced): hook.2 "outputs: zero, zero, one, zero, zero" (voiced an extra
  zero, all three Whisper models) → "the same five outputs: zero, zero, one, zero, and zero"; cross.1 "A crossed
  cell" ("Across cell") → "A cell with a cross in it"; cross.2 "The lecturer crosses them" ("The lecture") → "In
  the lecture, the crosses go in column by column, and you get the same sixteen"; column.2 "our pair from the
  start" ("are pair") → "the pair we started with"; "aitch" → "H" and "gee" → "G" in hook.1, grid.3, column.1,
  column.3 (Gemini and Whisper heard "A H", "A-etch"; ch1's lesson); recap.2 "And column A now holds" (Whisper "In
  column", Gemini "column uh") → "Column A, the first column, now holds" (QA and `listen --only` clean).
- Accepted Whisper flags (spelling only): step.1, pairs.2 "pee prime / cue prime" → "P' / Q'".
- **Shared drawings for ch3** (module-level, `load_scene(stem)`):
  - ch2_s5_layout.py: `p150_table()` (p. 150's 8 rows, ch1's state-table API: `.rows .cell(r,c) .col .row_of .row_box
    .col_box .xs .y`, c = 0..3, one Output column; returned at its home, left third), `implication_table()` (the
    staircase at its home: `.cell("A","B")` column letter first, `.cells .squares .col_letter .row_letter .pairs`,
    cell side 0.9), `grid8()`, `cell_label(it, col, row)`.
  - ch2_s6_outputs.py: `cell_cross(cell)` (two RED diagonals across the cell), `output_dots(it)` (GREEN dots 0.3 left
    of row letters C E F H and columns C E F), `CROSSED` (16 pairs), `OPEN12`, `handover_shot()` (table + staircase +
    dots + 16 crosses).
  - ch2_s1_hook.py: `two_lanes()` (A and D on 0 1 1 0; `.step(i) .circles .outs .out_boxes .eq`), for ch3 s5.
  - **ch2_s7_columna.py (built): `handover_shot()` = s7's exact last frame = ch3 s1's opening**: `p150_table()` left,
    the staircase with `output_dots`, the 16 `cell_cross`es, A-B "D-F" over "C-H", A-D "A-D" (struck through, DIM)
    over "C-E", A-G "B-D" over "C-H", the other nine open cells empty; no caption. Helpers for the other nine cells:
    `write_pair(scene, tbl, it, col, row, line, run_time, order="abc"|"said", clear=())` (rows/cell box YELLOW,
    outputs GOLD, next-state letters box BLUE, the table dims to 0.2 and `_Ferry` carries each letter through the
    gap between table and staircase; returns None when both next states are the same), `alphabetise(scene, pair)`
    (letters swap places), `strike_pair(scene, pair)`, `pair_text`, `pair_at`, `pair_slot`, `struck`,
    `strike_line`, `column_a_pairs`. Captions sit stacked in the empty top-right corner.
  - **ch2_s8_recap.py `end_card()` (built) for ch3 s1's forward join** = the chapter's last frame, held ~8 s: s7's
    frame with the nine open cells (B-D, B-G, C-E, C-F, C-H, D-G, E-F, E-H, F-H) outlined YELLOW, a YELLOW "?" on the
    right border of the cells beside column A's five live pairs (not the struck A-D), and the part line "Part 3 ·
    Solving the / implication table" (T 36, two lines, empty top-right corner). Clear the outlines and "?" marks to
    get back to s7's `handover_shot()`.
- Accepted check flags: small text in s2, s3 and s7 (the DIM p. 150 table at the left edge, size 18; the definition
  card shrunk to a top/corner reminder, 22 and 11; the reminder lanes), all small on purpose as the brief asks; dwell
  on s5's dimmed "A-A … H-H" labels (throwaway) and s6's "not equivalent" label (3.7 of 5.1 s).
- Gemini review (one round, frames checked): not glitches on frames: s1 27.5 s "duplicate start in D", s5 64 s
  "ghost overlay" (the title fading), s6 22/26.5 s "E/D omitted" (all four lit), s6 65 s floating cross (the planned
  flight into A-C), s7 82 s "open cells turn into crosses" (end frame clean, crosses correct), s3 27/71/81 s (fade-ins,
  empty end). Accepted: s1 0 s "flash frame" is ch1's end card by design; s1 34 s "row B highlighted" (the lanes'
  row boxes slide past B, read as motion); s5 43–48 s single letters/cells lit (lagged sweeps). Pronunciation, Gemini
  only (not in Whisper's QA, so accepted): hook.1 "finds" → "funds", step.4 "input" → "import".
- Glitches (confirmed with frames):
  - s2 ~52 s (c2.def.2 → def.3 clear): "p ≡ q", the BLUE arrow and "0 0 1 0 1" floated alone after the merged box's
    GOLD outline vanished; cause an uneven clear (outline faded before its contents). Fix pass: one even fade.
  - s2 ~66 s (c2.def.3 > hide): the tree's bottom fringe, "16" and "… ∞" lingered while "from p / from q" came in;
    cause the tree cleared top-down level by level. Fix pass: one even fade before the rows.
- Fix pass 1 (done): s2 (the two clears), s3 and s7 (reminder lanes illegible at size 11–17: ~2× larger; s7's is a
  compact text version without circles), s7 caption "3 promises" → "3 cells of promises" (Gemini read it as
  contradicting the five pairs); s4 {promise}: the dashed card repeated the line above it and "implied pair"
  labelled the card (Gemini, confirmed at 39.4 s) → the outline now draws around the line itself, "p′-q′" and its
  label stay under it; s8: re-timed for recap.2, ends on `end_card()` (it faded out after the hold), r1/r7b lanes
  enlarged (Gemini read "start in D" as "start in B"). Gemini-only "input" → "inpuk" (s4) accepted.
- Left open (accepted departures): s5 omits p. 150's three bullet sentences (no room beside table and grid); s4's
  p/q diagram opens as the hero and fades for the fork (shrunk to a corner its labels fell below size 28); s7's
  reminder lanes at {ad} are a compact text version (no circles), while s3 and s8 keep s1's circles; the lanes' GOLD
  "=" between stacked output rows reads as "‖" (as the slide's vertical ≡).
- Gemini quota low (producer, 2026-11-01): one `vk review` round per scene only; fixes confirmed on frames and the
  holds image; `vk listen --only` only for lines Whisper's QA also flags.

## Parallel build plan (producer, 2026-11-01 11:10)
The user's weekly limit resets within a day, so chapters run ~5 at once (slots.py keeps RAM safe;
the CPU had headroom at 3 directors: load ~4 of 10 cores, memory pressure normal).
- Running: ch1 (forward join: opens on L10 ch6's end card; records its end card for ch2), ch4, ch6.
- Next: ch5 when L7 ch1 finishes; ch2 once ch1 has recorded its table drawings and end card; ch3 after
  ch2 (ch2 s7 → ch3 s1 is an exact handover).
- Joins between parallel chapters are reversed: ch4, ch5 and ch6 each design their own opening
  ("Part N") card first and record it here; the previous chapter's s8 ends on exactly that card. So
  ch3's s8 ends on ch4's opening card, ch4's s8 on ch5's, ch5's s8 on ch6's. ch1 → ch2 → ch3 stay forward.

## Chapter 3 · Solving the implication table (director, 2026-11-01): ready for final
- Preview `out/ch3_implication_preview.mp4` (480p, 10.6 min, decodes end to end); `vk preview 3` handovers all ok.
  Producer: `vk finalize 3`. If ch2 s8's `end_card()` or ch2 s7's `handover_shot()` changes, s1 and s2 must
  re-render; if ch4's `open_card()` changes, s8 must.
- Music `music/ch3.json`: hook Spirals (START → c3.fill.1), s2's quick fill of the last cells Stepwise
  (c3.fill.3:end → c3.pass.1), recap Clarity (c3.recap.1:end → END, swell after c3.recap.3:end).
- Narration: every spelled state letter written as a capital (COURSE.md's L11 rule; "bee dee see ee eff gee aitch"
  → B D C E F G H), with "states" added before bare pairs ("they go to states F and A"); re-voiced, Whisper QA
  clean. Also for the QA flags: fill.1 "and aitch" ("each") → H; pass.1 "The cell for A and bee promised two pairs"
  ("promise") → "The cell for A and B holds two promises, and the first is the pair D and F"; again.2 "in this same
  pass" ("the same") → "earlier in this pass"; again.3 "the cells for A and dee, and for see and ee" ("and D") →
  "the cell for states A and D, and the cell for states C and E"; merge.1 "row see's" → "row C's" (was spelling only).
  `vk listen 3` (after the capitals) heard 3 homophones, rewritten and re-voiced, then the one `--only` re-listen
  was clean: fill.4 "each read off the state table" ("reed") → "each one taken from the state table"; again.2
  "the cell for E and H leans on" ("weans") → "depends on"; merge.3 "the count stays the same" ("says") → "the
  count of flip-flops is the same". "self-implied", "non-equivalent" and "C and E" were heard right.
- Accepted Whisper flags (minor, not consensus): again.4 "cells in matter" → "and matter" (function word).
- Build plan: s2 first (opens on ch2 s7's `handover_shot()`, owns the chapter's table API: `home_shot(stage)` for
  "full", "pass1", "pass2", "survivors", `cross_cell`, `pointer`, `pass_counter`); then s3, s4, s5, s6, s7 in
  parallel (s3 → s4 → s5 → s6 handovers, each opening on s2's stage shot); s1 (ch2 s8's end card) and s8 (ends on
  ch4's `open_card()`) last.
- **ch3_s2_fill.py (built): the chapter's table API.** `home_shot(stage)`, stages "full" (s2's last frame =
  `handover_shot()`), "pass1", "pass2", "survivors"; handles `.tbl .it .dots .texts["A-B"] .crosses["A-B"]
  .glow["A-D"/"C-E"]`; `PASS1`, `PASS2`; crosses stroke 5, pass 2's stroke 11; `cross_cell(shot, pair, thick)`
  (anims, registers the cross), `pointer(shot, text_mob, pair)` → (arrow, anims), `pass_counter(text)` (size 32,
  top right, "+n" GOLD). Departures (builder's): letters fly across the dimmed state table along the grid line,
  landing already alphabetical; the tally sits top right (no room under the staircase).
- Built 8/8 (Opus scene-builders): s2; then s3, s4, s5, s6, s7 in parallel; then s1, s8. One Gemini review round
  (all 8) + holds, one fix round (s1, s2, s3, s4, s5, s7, s8), holds again. Scene lengths 43.1 / 93.3 / 114.7 /
  84.7 / 95.6 / 74.8 / 73.9 / 55.7 s (≈ 10.6 min). Joins: ch2 s8 `end_card()` → s1 (held 0.7 s, then the part line
  re-lays into a one-line title card identical to ch2 s1's); s1 → s2 → s3 → s4 → s5 → s6 handovers (all 0.00–0.02%);
  s6 → s7 → s8 fade to empty; s8 ends exactly on `load_scene("ch4_s1_hook").open_card()`, held ~8 s, no mark.
- Accepted check flags: dwell only, short clips clearing on the next beat; small text only where the brief asks
  for small copies: s4's side-by-side staircases (×0.68, pair text ~20), s6's top-right thumbnail of the
  implication table, s7's 7-state diagram during {crossall} (it grows to letters ~25 on {enough}; arc labels ~19),
  s8's six recap panels.
- Builders' departures worth knowing: s3 marks an open cell with a YELLOW tint + a "?" inside it (E-H: in its empty
  top half; two-pair cells: a large faint "?" behind the pairs, drawn as a shape so the overlap lint passes); s3's
  p. 154 inset is drawn (no slide image in the project); s5 fades the state table out on {coords} to make room and
  brings it back at the end; s5's definition card is rebuilt at size 28 (`def_card()`, same words/colours) since
  ch2 s2's at that scale was size 19; s7's 6-state table marks the three substituted entries GOLD.
- Accepted Gemini review claims (not on frames): s2 0 s "all cells pre-crossed", ~83 s "11 promises / 17 crosses"
  (F-H mid-fill on {full}), ~90 s "F-H animates after the tally"; s3 "dark box behind A-D/B-D" (grid intact),
  ~79.5 s "D-G pointer lingers" (it was E-F's own pointer starting), ~108 s "ghost grid" (B-D's cross faded to 0.15
  on purpose: open at that moment); s4 12/17/21 s "crosses in the wrong columns" (holds show A-G, C-H, E-H); s5 row
  D "A D" (reads "A E"), ~88.5 s GOLD dot by D (a landing dot, fading); s6 "brace over 'states may'" (the brief's
  "not here" on the first "may"); s7 "C has no arc to H" (C goes to E and D), "five orange entries" (three GOLD + the
  GREEN 1s); s8 "D instead of B" (reads B); s1 0 s "flash of the table" (ch2's end card, the forward join).
  Pronunciation (review only, not repeated by `vk listen` or Whisper): s2 "H" → "age", s6 "row A" → "row of A".
- Glitches (confirmed with frames, all fixed in round 1):
  - s1 ~10.5 s (c3.hook.1 > table): a YELLOW horizontal line running above row B into empty space; cause
    `FlashAround(it.squares)` traces the staircase's rectangular bounding box. Fixed: `VShowPassingFlash` along the
    stepped outline. (~26.5 s "duplicate C-H": the in-flight copy over the grid, gone by 27.6 s; kept.)
  - s3 ~85–89 s (c3.pass.4 > eh/fh): E-H's "?" sat on the corner it shares with F-H, read as F-H's, then F-H's cross
    drawn "over" it; cause placement on a shared corner. Fixed: "?" inside its own cell.
  - s4 ~81.5–82.7 s (after c3.again.4): the return to the home shot ran in three quick phases (everything fades,
    staircase jumps to full size alone, state table pops in), read as "abruptly flashes back"; cause one 2.2 s play
    with FadeOut 0–45%, Restore from 30%, FadeIn from 65%. Fixed: one 3 s overlapped move.
  - s5 ~53.5 s (c3.survive.3 > fromce): a half-drawn square bracket round node C-E, read as a stray arc; cause
    `FlashAround` on a circle (ch1's glitch class again). Fixed: a ring flash along the circle's outline.
  - s8 ~38 s (c3.recap.2): pair texts and axis letters in r1–r4 as white blobs; cause `set_stroke` on whole groups
    in the thumbnail-thinning helper gave every glyph a 2.4-wide FG outline. Fixed: `family=False`, shapes only.
  - s8 r5: "3: 8" rung label far left of its codes, the "6 states" bracket on the top code row only (layout). Fixed.
- Other round-1 fixes: s2 E-H's rows now light on {eh} (E-F's quick fill had overrun it by ~1.5 s); s7 the 7-state
  diagram grows on {enough}; s8 the clip-3 clear moved to "how to build" so r6's "equivalent, not just identical"
  gets 6 s (scene +1.2 s).
- Post-final check (2026-11-01, `out/ch3_implication.mp4` 10:37.0): done, no fix. `ch3_finalize.md`'s one "look",
  s3 @ 73.5 s "E-H abruptly pops into cell D-G", is not real: frames of the final at 8 fps over 03:28.5–03:33.4 show
  D-G holding "A-B / E-H" unchanged throughout (only its YELLOW outline lights on {dg}); E-H was written in s2 on
  {way} by the normal read animation (A-B at 01:51.5, E-H at 01:52.0) and stays from then on. The s2 @ 68.3 s
  "E-H omitted" and s4 @ 55.6 s claims are the same misreading (mid-transition). s3's large faint "?" behind the
  pairs of open two-pair cells (A-D, C-E, A-G, C-H) checked on a native 1080p crop at 03:40: a dim GOLD "?" on the
  YELLOW tint, pairs stay fully legible in white; reads clearly. No re-final needed.

## Chapter 4 · State machines on a programmable chip (director, 2026-11-01): READY FOR FINAL
2026-11-01: 7/7 scenes by Opus scene-builders, one fix round (scene reviews + two holds rounds), preview
`out/ch4_gal_preview.mp4` 9.6 min (578.5 s); narration 9.1 min. Producer runs `vk finalize` (Gemini quota: no
final review by the director). Handovers s2→s3→s4→s5→s6 all 0.00%; s1 ends empty, s6 ends empty. `vk final`'s
"handover MISMATCH: ch4_s7_recap … ends the chapter" is expected: s7 ends on ch5's `open_card()`.
**If ch5 changes `ch5_s1_hook.open_card()`, re-render ch4 s7.**
- Accepted check flags: small text on shrunk drawings the briefs ask for (s2's schematic thumbnail 13–16 pt;
  s4's small Moore schematic 17–20; s5's shrunk GLA and small PAL 16–23 and side-size plane labels 25; s6's
  scaled GAL pins, rail and term labels 12–26 and the faint K-map ghosts); dwell advisories at the handover
  t = 0 fades, on long verbatim quotes (s2 p. 156 bullet, s4 p. 156 line), s1's 0.7 s open card and 3 s title,
  s3's minterm example (5.7 of 5.9 s), s5's "fixed OR plane, like a PAL" (2.1 s, lands on "fixed"), s7's
  "5 AND · 2 flip-flops" (3.9 s, cleared on "Next time").
- Departures from the brief: s1 ends empty (no package carried into s2); s2 two BLUE braces (one per logic
  box) and "in the labs"; s2 {add}: the flip-flop fades in beside the "+" (a fly crossed the quote); s3
  "sum of products" above the formulas, formulas fade in centred between PLA and PAL (no flight); s4 counts
  stacked, Q̄ ghost as dashed loops; s5 "simpler"/"faster" together, hand icon hand-drawn; s6 terms `fly` (no
  text morph), equations column at the left; s7 tiles carry no text inside the drawings (6–9 pt at tile scale),
  r4 a stacked "equations ↓ compiler", r2 counts GOLD "3"/"4", no GLA chip outline in r3.
- Gemini quota: s5's and s7's scene reviews ran just before the producer's quota note (the chain was stopped
  too late); no further Gemini review or listen was run after it.
- Music `music/ch4.json`: hook Machinery (START → c4.needs.1), s6 GAL-lighting stretch Focal Point
  (c4.sync.2:end → c4.sync.5), recap Fractals (c4.recap.1:end → END, swell after c4.recap.3:end).
- Build order (as run): s1 (`open_card()`), s2, s3 (owns the programmable-array style: rails, gates, dots,
  panels); then s4 (s3's handover) and s6 (owns the GAL drawing, `opening_shot()`, `compiler_row()` and the
  synchroniser GAL); then s5 (s4's handover, ends on s6's `opening_shot()`) and s7 (ends on ch5's card).
- Rewritten for the ear (all re-voiced; Whisper QA and `vk listen 4 --only` clean on each):
  - "GAL"/"GALs" was voiced as letters "G A L" (Gemini high, 6 clips): the narration now writes "Gal"/"Gals"
    (gal.1, gal.3, sync.2, recap.2, recap.3). Said as a word now. **Candidate course voice rule** (ch5 has GAL too).
  - "and gate(s)" heard "in/end gate(s)" (Gemini, Whisper ×3 on gla.4): "each of these and gates" (pla.2),
    "every one of the and gates" (gla.2), "a pair of and gates, a pair of or gates" (gla.4), "Each of the and
    gates keeps" (sync.4), "needs only five and gates" (recap.2, was "fits in five").
  - hook.2 "all wired together" (heard "wire") → "all joined up with wires"; needs.2 "a state machine needs"
    → "every state machine needs", "Combinational logic, and dee flip-flops" → "Some combinational logic, and
    some dee flip-flops"; needs.3 "called P-L-As" (review: "plahs") → "called P-L-A chips"; pla.2 "Programming
    the chip means removing connections" → "To program the chip, you remove connections", "when A is one and bee
    is zero" (heard "hey") → "when input A is one and input bee is zero"; gla.1 "a G-L-A, a generic logic array"
    → "short for generic logic array"; sync.1 "one output, ess, … only in Sync" (+qa "ES") → "one output, called
    ess, … only in the Sync state"; sync.3 "and S zero and ee and ar." (heard "A R") → "…ee and ar, all three
    together."; sync.4 "the output, ess, is simply…" (heard "S S") → "the machine's output is simply…", "The
    flip-flops hold" (heard "foot-plops") → "The pair of flip-flops holds".
- Accepted voice flags: gal.3 "a Gal pays" → "gout"/"GAU" (Whisper only, jargon; Gemini hears it right); pla.3
  "K-map" → "came app" (one scene review only; a focused listen was clean).
- Glitches (confirmed on frames by the builders, all fixed):
  - s1 hook.2 ~31.8–33.4 s {one}: the wired board stayed full size and faded in place while the merged package
    grew through its wires. Cause: each piece had a slide-and-shrink and a FadeOut in the same play; the later
    FadeOut restores the start position every frame, so the slide never showed. First fix also failed: shrink
    into the centre bunched the packages (~33.1 s); sliding into a row crossed the 74HC74 and the new 74HC08
    (~32.6 s; the list was in add order, not left to right). Now: labels and wires fade first, then the bare
    packages, sorted left to right, slide into a row and the merged package fades in around them.
  - s2 needs.3 ~51.2 s {add}: an empty, label-less box flew across the thumbnail schematic. Cause: `fly(ghost,
    ff_big)` with a ghost copied from the box outline only. Now a ring on the thumbnail's flip-flop and the full
    flip-flop fades in beside the "+".
  - s5 gal.2 ~30–36 s: GREEN feedback wires ended in mid-air before {ffs}: the flip-flops were held back from
    the drawing while their wires were shown. Now the flip-flops are DIM from {figure} and light at {ffs}.
  - s5 gal.4 ~65.5 s: the hand landed 0.16 right of the target dot, outside the AND plane, while still sliding
    in. Now it lands on a dot, with a YELLOW ring. ~78 s: one 1.8 s play faded the compiler row and restored
    every dot, so the programmed pattern seemed to vanish; now the row fades, the pattern holds 0.6 s, and the
    dots fade back in over 2 s as the GAL regrows (to s6's `opening_shot()`).
- Review findings fixed (not glitches): s1 GOLD only on the merged states' names (was every A and C); s2
  "in the labs" centred under both groups; s3 pla.6 formulas stacked once between the PLA and PAL (they read as
  f0 = PLA's, f1 = PAL's), caption and cost line raised off the bottom edge, minterm card off the rail labels;
  s4 gla.4 {notq} pulses Q's feedback on "only feeds back cue", then Q̄ on "not cue"; s6 circles light one per
  word, gates in equation order (D0: s0·ē, s̄1·s̄0·r; D1: s1·ē, s1·r, s0·e·r, also in `sync_gal()`), doubled
  a/b labels removed from `sync_gal()`, "r̄ unused" and "s = s1" moved into the left column.
- Review claims not real on frames: s1 0.0 s card (by design), ~29.5 s "chips collide" (the {change} rewire is
  clean; the "unlabelled" chip is the second 74HC08), ~17 s pin-1 dot; s3 ~55 s "ū" (a clear ā at 1080p);
  s3 ~100 s "fn not f1" (p. 73's label until {example}); s6 ~29 s "c" (the a → e fade, half way), ~51 s
  "gates 3 and 4 switch colours" (D0's gates lighting); s7 GOLD "3"/"4" (brief) and ch5 card's repeated
  lookup-table rows (ch5's D1 bits).
- Fix pass after the final (2026-11-01, ch5 director's report that `sync_gal()` leaves stale "a"/"b" under
  "e"/"r"): no fix, harmless; finals out/ch4_gal.mp4 (9:39.7) and out/ch6_electricity.mp4 (11:09) stand.
  `sync_gal()` already drops them (`g.bank.remove(*g.in_labels)`, the round-1 fix above; ch5's
  `gal_and_tag()` workaround is now a no-op, also harmless). Frames of the finals, full-res crops: ch4 s6 at
  18/37/63/81/101 s (final 07:18–08:42) show only e/r on the bank; ch4 s7 tile_r5 (final 09:12) and ch6 s8
  gal_thumb (final 10:48) strip all text, so no labels at all.
- For ch3 s8: end on `load_scene("ch4_s1_hook").open_card()` (built; `.chip .table .cap .part`): the
  6-state table (p. 155) on an L8 `chip()` package, caption "a chip you can program", part line "Part 4 ·
  State machines on a programmable chip" (T 40, y 3.2). ch4 s1 holds it 0.7 s, then the part line travels
  into the title card. Also in ch4_s1_hook.py: `six_table()` (ch1_s3's look, single "Output (Y)" column),
  `package(label)`, `three_wired()`, `four_wired()`, `merged_package()`. If ch3 changes the card, tell
  ch4's director: s1 must re-render.
- For ch5: the synchroniser GAL is `load_scene("ch4_s6_sync").sync_gal(where=MID)` (built, 9.6 × 6.1 units):
  BLUE rails e, ē, r, r̄ (r̄ DIM, "unused"), GREEN s1, s̄1, s0, s̄0; five AND gates (D1 group: s1·ē PINK,
  s1·r PURPLE, s0·e·r TEAL; D0: s0·ē PINK, s̄1·s̄0·r PURPLE) with exactly 12 lit dots; fixed OR lines; two
  flip-flops s1, s0; output `s`. Same file: `gal(left, right, gaps, inputs, outs, lit, where)` (p. 158's GAL,
  handles in its docstring), `opening_shot()`, `compiler_row(eqs, size, out=None)`. Loads s3 via `load_scene`,
  L6 `make_ff` and L10's ch5_s3/ch5_s6 by file path (not ch5_s7_d0: it calls `load_scene` on import).
  Other array helpers: ch4_s3_plapal.py (rails, gates, dots, panels, `small_pla()`, `small_pal()`),
  ch4_s4_gla.py `gla()`.

## Chapter 5 · Inside an FPGA (director, 2026-11-01): ready for final
- Preview `out/ch5_fpga_preview.mp4`, 10:41 (640.7 s), decodes end to end; narration 10.2 min. Handovers s1 → s2 and
  s4 → s5 match at 0.00%; s8 has no mark (it ends on ch6's `open_card()`, the reversed join).
- Scenes 8/8 by Opus scene-builders: s1 (card first), s3, s4, s7; then s2 (s1's handover), s5 (s4's handover);
  s6; s8 last. Fix passes: s1 (ch4's real GAL), s4 (opens from s2's array), then one review round (one Gemini review
  per scene, per the producer's quota note, plus the holds image) on s2, s4, s5, s6, s7, s8; s1 re-rendered after
  the Gal re-voice.
- Shared drawings: s1 `tile_grid()`, `gal_and_tag()` (ch4's `sync_gal()` with the a/b-label fix; text stripped at
  hook size), `laptop()`, `factory()`; s2 `spartan_array(center, with_routes)`, `ARRAY_C`, `INSET_CLB`,
  `switch_inset()`; s3 `lut_grid(bits, …)`, `lut_table()`, `D1_BITS`, `recap_shot()`; s4 `clb(programmed)`; s5
  `filled_clb()`, `recap_shot()`, `D0_BITS`; s6 `pipeline_shot()`, `strip_text`; s7 `cost_plot()`.
- Accepted check flags: s7's "millions" row off both edges (the brief asks for it; flagged on the frame before
  {asic}); s8 "doesn't end empty" (its last frame is ch6's opening card by design); small text where the brief
  shrinks things (s3's corner mux/ROM thumbnails and tiny L10 diagram; s5's CLB at 0.72 scale, the compare view and
  L10's diagram at {fit}, which can't grow without shrinking the CLB; s8's tiles, text stripped); dwell advisories
  where the narration moves on (s1 title 2.8 s and "programmed by you"; s2 inset labels; s5 "level 1/2" leave at
  {fit}; s6 "compiler", the p. 161 caption, "arithmetic", "user RAM"; s7 the short tags); s2 flashbox advice on "SM".
- Accepted Gemini review pronunciations (Gemini-only, not in the full listen or Whisper's QA): lut.4 "state" →
  "site", clb.3 "dee in" → "din", oneclb.2 "one one zero zero" → "eleven hundred" (Whisper heard it right).
- **For ch4 s7:** end on `load_scene("ch5_s1_hook").open_card()` (exactly; ch5 s1 holds it 0.7 s, then its part
  line travels into the title). **Built** (11:45, in scenes/ch5_s1_hook.py): `tile_grid(pitch=0.72, tile=0.55,
  center=(-3, -0.3))`, 8 × 6 TEAL tiles with DIM channel wires; tile (2, 7) YELLOW (`.src`), opened by two DIM lines
  (`.zoom`) into a 3.6 square TEAL tile at (3.9, -0.3) (`.tile`) holding D1's 16 bits (`.bits`, T 48, pitch 0.78,
  rows 0000 0001 1101 1101, 1 GREEN, 0 DIM); "FPGA" and "lookup table" T 36 at y -2.95 (`.fpga_tag .lut_tag`); part
  line `T("Part 5 · Inside an FPGA", 40)` at y 3.2 (`.part`); also `.grid .tiles .wires`. The grid helper is
  `tile_grid(cols=8, rows=6, pitch=1.1, tile=0.85, center=(0, 0.3), color=TEAL)` (`.tiles .tile(r, c) .wires`).
  No GAL on the card. **If ch5 changes it, ch4 s7 must re-render.**
- **For ch4's director:** `ch4_s6_sync.sync_gal()` does `g.remove(*g.in_labels)`, but the old "a"/"b" labels live
  in `g.bank`, so they stay under "e"/"r" (ch5 s1's check flagged the stacked "a"/"e"). ch5 works around it in
  ch5_s1_hook.py `gal_and_tag()` (`gal.bank.remove(*gal.bank.labels)`); check ch4's own shots. If ch4 changes
  `sync_gal()`, re-render ch5 s1, s5 and s6.
- Music `music/ch5.json`: hook Fives (START → c5.array.1), s2's array stretch Fragments (c5.array.1:end →
  c5.array.3), recap Sixes (c5.recap.1:end → END, swell after c5.recap.2:end).
- Narration rewritten for the ear after the first full `vk listen 5` (re-voiced; QA and `vk listen --only` clean):
  hook.1 "two flip-flops." ("foot-flops") → "and two flip-flops to hold the state."; hook.2, array.3, config.3 "The
  lecturer calls …" ("lecture", +qa twice) → "In the lecture, they're described as / called …", "… the Spartan is
  described as quite an old design"; oneclb.3 "the combinational outputs are left unused" ("cominational") → "the two
  combinational outputs stay unused"; oneclb.4 "two or gates, one and gate for each K-map loop" (+qa "or dates one in
  gate") → "five and gates, one for each loop on the K-map, plus two or gates to join them"; config.2 "Xilinx devices
  keep …" ("Lilinx") → "In Xilinx devices, the configuration sits in static RAM, …"; custom.2 "onto silicon"
  ("silica") → "onto a silicon wafer"; recap.1 "Let's recap." ("Must") → "Time for a recap." (L10's fix); config.3
  (second listen: "in" → "and") → "They differ in the number of logic blocks, and in how each block is built. Some
  keep the read-only memory inside the chip, others outside it, and some add extras, …".
- Glitches (one Gemini review per scene, confirmed by the builders on `--frames`, all fixed):
  - s6 config.3 ~48.5 s and ~54.5 s: the Xilinx grid and its ROM box vanished. Cause: the BG-filled "product line"
    plates behind each chip were raised over them by later animations (z-order); now pushed to the back.
  - s6 config.3 ~63 s: a lone ROM box stayed at the cut to {old}. Cause: a staggered one-by-one clear with the ROM
    boxes last; now everything fades together.
  - s6 config.3 ~74.5 s: a stray YELLOW line on the modern FPGA's border. Cause: the first frame of a glow on
    "flexible"; the glow was removed.
  - s7 custom.2 ~36.5 s: chips in the row without price tags. Cause: the tags faded in one by one after the row had
    landed; each chip now flies out with its tag on.
  - s7 custom.3 ~64.5 s: the PINK tint grew as a short rectangle. Cause: `GrowFromEdge` starts as a small box; now
    the tint spreads sideways from the dashed line at full height.
  - s8 recap.2 ~49.5 s: electrons seemed to flow clockwise (+ to −). Cause: the final park rounded each electron to
    its nearest slot, pulling some backwards after a ~2 s drift; now ch6's drift speed, forward-only parking.
  - Layout, not transitions: s2 array.2 ~28 s, the channel lines stuck out ~0.22 past the outer blocks and the
    "routing channels" arrow pointed at a stub; s4 clb.4, "all programmable" sat 0.15 from box B's "B"; s5 oneclb.3
    ~55.5 s, the `e` label sat by the `r` wire while fading in.
  - Not confirmed on frames (unchanged): s1 0 s, "stray LUT frame" (the opening card, by design); s1 ~31 s,
    "stray grid lines" (the channel wires); s2 ~48.5 s, IOBs missing (mid-fade); s2 ~53.5 s, buffer points inward
    (it points outward, toward the lamp); s4 ~66 s, a "not used here" box over H (no box; the tag was moved closer
    to its wires anyway); s5 ~52 s, the tables turn to zeros (they hold D1/D0 throughout); s8 ~2.5 s, the card border
    vanishes.
- "GAL" → "Gal" (COURSE.md rule from ch4) in hook.1, hook.2, oneclb.4, config.1; re-voiced, QA clean (no listen
  re-check, per the producer's Gemini-quota note).
- Accepted Whisper flags (spelling, format or homophone; Gemini heard them right): lut.4 "dee one" → "D1", "one one" → "1-1"; custom.3 "custom chip" →
  "custom ship"; recap.1 "round the" → "around the".

## Chapter 6 · Electricity, from charge to Kirchhoff (director, 2026-11-01): DONE
- 2026-11-01 12:45: `out/ch6_electricity.mp4`, 11:09 (669.0 s, 1920×1080, 60 fps); narration 10.2 min. 8/8 scenes by
  Opus scene-builders (s2 first; s1, s3–s7 in one batch, with s4 → s5 and s6 → s7 handovers written first; s8 last),
  one review round (Gemini per scene + holds) with fix passes on all 8, then the final viewer + transitions reviews
  (one pass each, Gemini quota low) and one last fix pass (s6 formula, s7 grow and {ours} labels), re-final, frames
  checked from out/. Handovers s1→s2, s2→s3, s4→s5, s6→s7 at 0.00%; "ch6_s8_recap … ends the chapter" is expected.
- Accepted check flags (dwell advisories only; no overrun, sync, layout or transition flags): s1's title card 1.5 s
  (the brief clears it on {last}, ~3 s into the line) and the road tags / 0 → 1 values in hook.2–3; s2's
  inherited "?"/"how much?" on frame 0 and "gas or liquid" 3.9 s; s3 "1 C" 3.6 s (clears before the formula); s4
  "+1 J" 2.9 s (swaps to "+1.5 J" on "half"); s5 rearrangement steps (they slide into the next line); s6 "0.15 A"
  3.7 s, "20 Ω" 4.1 s; s7 `2+3-5=0` 3.3 s, `+1.5-1.5=0` 4.8 s, "1 A × 1 Ω" 1.9 s; s8's KVL line and "This lecture"
  tags (the narration moves straight on).
- Open: the end card's heading "Electronics, Devices and Circuits" is a stand-in for Lecture 12's title (not mapped
  yet); if L12 picks another, re-render ch6 s8. s8 uses ch4's `sync_gal()` (labels removed): **if ch4 changes
  `sync_gal()`, re-render ch6 s8.** s7's {negative} ghost arrow flips beside the wire, not on it (Gemini "confusing",
  accepted).
- **For ch5 s8:** end on `load_scene("ch6_s1_hook").open_card()` (exactly; ch6 s1 opens on it, held 0.7 s, then
  its part line travels into the title). Design: ch6's running loop (p. 167: FG battery on the left, "+" up, the lamp
  in the right-hand wire glowing YELLOW, BLUE "−" electrons on the wire, static, seeded) under the part line
  "Part 6 · Electricity, from charge to Kirchhoff" (part-line style as L10's end cards: T 40, y 3.2). **Built**
  (2026-11-01): `open_card()` in scenes/ch6_s1_hook.py = s2's `Loop()` (slot_fill removed), `LoopElectrons(loop)`
  parked (seed 7), `lamp(lit=True)` in the slot, `T(PART6, 40)` at y 3.2. **If ch6 changes it, re-render ch5 s8.**
- Music `music/ch6.json`: hook Zeta (START → c6.metal.1), s2's lattice stretch Occlusion (c6.metal.1:end →
  c6.metal.4), recap Quantum Blue (c6.recap.1:end → END, swell after c6.recap.3:end).
- Voice: `vk listen 6` (Gemini, first pass) flagged 5; rewritten and re-voiced, `vk listen --only` clean on all 4 lines:
  metal.2 "free to roam around the fixed positive ions" ("paws the byons") → "free to roam between the positive
  ions, which stay fixed in place"; volts.3 "subscript ell, for lamp" ("wamp") → "…, which stands for lamp", and
  "energy divided by charge, in joules per coulomb" ("quon") → "the energy divided by the charge, measured in joules
  per coulomb"; ohm.4 "gives a flatter line" ("lime") → "with a bigger resistance, the line is flatter"; laws.6
  "resistors of one, two and three ohms" ("thirty", +qa) → "the resistors are one, two and three ohms, with one amp
  flowing through them all". Accepted Whisper flags (format/spelling only): volts.1 and laws.5 "round" → "around",
  ohm.3 "one and a half" → "1.5". A second `vk listen --only` (Kirchhoff lines; "Kirchhoff" itself was heard right)
  flagged two more, rewritten and re-voiced, then clean: laws.1 "Count a current…" ("Counted") → "We count a
  current…"; recap.3 "inside every gate" ("get") → "inside every logic gate".
- Build plan: s2 first (owns the circuit drawings and the `opening_shot()` s1 ends on); then s1 (`open_card()`),
  s3 (s2's handover), s4, s5 (s4's handover), s6, s7 (s6's handover); s8 last.
- **Circuit drawings (the studio's first; for Lecture 12)**, all in `scenes/ch6_s2_electrons.py`, via
  `load_scene("ch6_s2_electrons")`: `electron(r=0.14)` (BLUE "−"), `ion(r=0.3)` (DIM "+"), `lattice(cols, rows,
  pitch, r)`; `battery()` (long "+" plate up; `.plus_plate .minus_plate .plus_sign .minus_sign .leads`, leads
  `BAT_H`); `lamp(lit=False, r=0.42, span=SLOT_H)` (`.circle .cross .leads .glow`) and `lamp_glow(lamp)`;
  `resistor(label=None, vertical=True, span=SLOT_H)` (`.body .leads .label`); `current_arrow(start, end, label,
  side=UP)` GOLD and `voltage_arrow(low, high, label, side=LEFT)` TEAL (head at the high end; `.arrow .label`);
  `Loop()` (7.6 × 4.6 at (0, −0.4), battery mid-left, an empty `SLOT_H` = 1.3 slot in the right side; `.wire .battery
  .slot_fill`, `.slot_center() .battery_center() .place(mob) .corners() .point(u) .normal(u) .perimeter()`, u
  anticlockwise from bottom-left); `LoopElectrons(loop)` (28 electrons; `.start() .stop() .snap()`, `.drift .jitter`,
  `.motion(drift=, jitter=)`); `DRIFT = 0.45`; `wander(...)`; heat glow `HEAT = "#FF862F"` (no studio orange).
  Also: ch6_s2 `opening_shot()` (s1's last frame: tube y 0.5 ± 0.55, YELLOW "?", GOLD "how much?") and
  `handover_shot()` (`loop, els`); ch6_s3 `i_eq_qt(size=120)` (`I = Q/t`, I GOLD); ch6_s4 `handover_shot()` (lit
  loop, `.loop .lamp .cur .vb .vl`); ch6_s6 `handover_shot()` (10 Ω loop, 1.5 V, 0.15 A); ch6_s7 `kcl_junction()`
  (`.wires .node .arrows .labels .paths`) and `kvl_loop()` (p. 170's six-element loop, as the slide: `.wire .dot .bats
  .res .varrows .vlabels .names .current .corners`, `.through` separate); ch6_s8 `end_card()`.
- **For Lecture 12:** its first scene opens on `load_scene("ch6_s8_recap").end_card()` (= `handover_shot()`, the
  last frame): DIM "Next lecture", heading "Electronics, Devices and Circuits" (the builder's choice: p. 163's
  section; L12's real title isn't mapped yet), p. 170's last bullet in italics with "potential divider" YELLOW, a
  DIM battery-and-two-resistors silhouette with a YELLOW "?" at the middle node. `vk final`'s "handover … ends the
  chapter" line is expected.
- Glitches (confirmed with frames by the builders, all fixed in round 1):
  - s2 0.0 s: s1 → s2 handover 1% off; `_edge_fade` set the flow electrons' opacity every frame, defeating their
    FadeIn, so they showed on frame 0 (now faded in through a tracker). "compass deflects" read "defiects": Pango's
    "fl" ligature (broken with a joiner).
  - s1 ~16.8 s: the transistor silhouette poked out of the thin translucent OR gate (placement; gate enlarged,
    transistors 0.8×).
  - s3 ~28.5 s: `FlashAround` on thin arrows drew narrow rectangle slivers beside them, read as "a stray electron
    with an arrow" (now a scale pulse). s3 ~70.3 s: a lagged clear still fading the stopwatch, "1 C" block and
    coulomb label while "1 C per second = 1 A" moved up through them and `I = Q/t` faded in (now clear, move, write).
  - s4 ~39 s: `FadeOut(chip, scale=0.4, target_position=lamp)` slid the chip's opaque background box across the
    token and lamp: a flickering rectangle (now fades in place). s4 ~57 s: `1 V = 1 J/C` touched "charge (C)"
    (placement).
  - s5 ~34–37 s: a tall diagonal strike through the numerator's t crossed the I; Gemini read `P_L = I^{V_L}` (now
    short strokes inside each t, faded to 0.3).
  - s6 ~46.5 s: `ReplacementTransform(symbol, 10 Ω resistor)` shrank the symbol into a small tilted resistor under the
    banded part (now fade out / fade in). s6 ~73 s: "20 Ω" faded in before its line reached it (Gemini read "30 Ω").
    s6 ~78 s: `sweep_clear`'s lagged fade of the plot overlapped the pipe fading in (now clear first).
  - s7 ~39 s: the junction stayed ~5 s under the new KVL heading. s7 ~57 s {grow}: morphing the 3-piece wire into
    the 6-piece wire crossed lines at odd angles, and V_1's battery vanished ~1 s (it left with the old shot). s7
    ~120 s: "1 A × 1 Ω" lingered ~5 s.
  - Ruled out: s1 ~37 s "Transistors → gates fades" (it was the subtitle leaving); s4 ~76 s "GOLD highlight stuck on
    the battery" (a slow YELLOW ring fade; shortened anyway); s7 "V_6 plates horizontal" (vertical; the "+" signs were
    moved beside the long plates).
  - Final video (`vk review 6` + `--transitions`, one pass; frames checked by the director from out/ at +0.5 s):
    confirmed and fixed in a last pass (frames re-checked in the re-final): s6 ~25.2 s {ohmslaw}, `R = V/I` still
    moving up while the `fly` copy into `V = IR` crossed it (a doubled formula; now `V = IR` fades in after the move);
    s7 ~56 s {grow}, a lone vertical wire segment right of the loop for ~0.5 s: `FadeOut(loop.slot_fill)` re-added
    s6's removed slot wire at full size for the play (line deleted). Also found there: s7's {ours} labels ("1.5 V",
    "10 Ω", "0.15 A") were invisible all through laws.3, so its flashes ringed empty space: `set_alpha(..., 1)` on
    text whose fill was 0 restored only the outline (now a scene-local `_restore()`; loop back at 0.88×, labels T 28). Ruled out on frames: s4 ~43.9 s "second green arrow
    left of the lamp", s5 ~30 s "duplicate equation" (the boxed `It` sliding in), s4 ~20.9 s "doubled text" (the
    card's last line fading in). Accepted (by design or a brief fade): s2 ~63 s battery "detaching" (the brief's
    disconnect), s2 ~41 s caption lingering under the loop, s6 ~47 s resistor appearing beside the loop before it
    slides into the slot, s3 ~58.5 s the division fading in under the tag, s5 ~0.3 s / ~51 s labels fading in by the
    shrinking loop, s6 ~70.7 s small flash box at the origin, s7 ~28.8 s "+ (in)" tags fading over the pipes, s7
    ~131 s the ghost current arrow flipping beside (not on) the wire, s1 ~46 s gate tip at the frame edge during the
    zoom, "Kirchhoff" heard "kirch-hoff" (low; the listen passes heard it right).
