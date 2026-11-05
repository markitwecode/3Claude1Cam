# Subqueries and Documents: status

2026-11-01: project created; planning.

## Chapter 1 · Queries inside queries (ch1_subqueries)
State: **ready for final** (2026-11-01 ~23:35). Preview `out/ch1_subqueries_preview.mp4`, 10.2 min (610.8 s),
decodes end to end; `vk preview 1`: handover ok s5 → s6 (0.00%). Gemini off until 2026-11-04: built and checked
without `vk review` / `vk listen` (Whisper vote + `vk check` + two holds rounds).
- **Opening card:** none needed (ch1 is the first chapter): s1 opens from empty on its title card.
- **Ends on ch2's opening card (reversed join):** s8's end card is exactly `load_scene("ch2_s1_hook").open_card()`
  (the three shape icons, "a table / a value / a column", FROM / > / IN); the recap's slot row fades during the
  end-card hold. No handover mark on s8 (the chapter's last scene); its "end: pieces left on screen" flag is by design.
- Scenes (render vs narration): s1 55.6/50.6, s2 78.6/76.2, s3 102.6/97.4, s4 78.7/76.6, s5 85.9/81.3,
  s6 63.4/59.2, s7 88.8/82.0, s8 57.1/48.2 (+ ~8 s end card).
- Fix round (holds round 1): s2 genres rows held the whole {genres} sentence (were up 1.1 s); s3 year groups
  BLUE (were BLUE/TEAL/PURPLE); s4 UNION bar BLUE (was TEAL, the document colour); s6 {three} queries re-wrapped
  to ≤ 26-character lines at size 18 (were size 12). Round 2 holds confirmed all four.
- Accepted check flags: small text where the brief's density demands it: s2's map columns (24), The Kid's row
  tables (22) and the corner locator map (~8); s6's chained WITH (25, kept verbatim beside the tower), the
  "common table expression" header (25) and the {three} queries (18); s8's recap thumbnails in the top slot row
  (7–15; each callback is full size while it's spoken). Dwell advisories throughout (cues follow the narration's
  pace: s4's keyword swaps, s5's form and name labels, s7's error, s1's part line).
- Departures the builders made (reviewed on the holds, kept): s1 form left / tower right (copies fly up an empty
  lane); s2 shows The Kid's rows as tables beside a corner locator map, not inside the cards; s3's slots don't
  reorder in place, the keywords fly into a numbered running-order column; s4 {limit} towers without the Venn;
  s5 one plan diagram with arrows from both queries, eye-path as a sliding highlight box; s6 narrower tower
  with shortened brick labels; s8 a top row of four slots instead of the 2×2 grid (room for ch2's card).
- Glitches: none recorded (no Gemini scene review this build; motion is unwatched until the finalize pass).
- **Helpers ch1 will export** (READY is marked here once built):
  - s2 the schema map **READY** (2026-11-01, scenes/ch1_s2_schema.py, rendered; for ch4 s1/s3, ch5 s2, ch6 s2,
    Lecture 5): `m = load_scene("ch1_s2_schema").schema_map()`, full frame, slide 23's layout, static.
    `m.cards[name]` (`.box .header .divider .title .rows[col] .underlines[col] .row_y(col) .entity`),
    `m.arrows[(src, dst)]` e.g. `("has_genre", "genres")`, `m.counts["movies"|"people"]` (GOLD),
    groups `m.card_group / arrow_group / count_group`; `m.light(name)` → animations lighting a card YELLOW;
    `card_alpha(card, a)`. The Kid's rows: `kid_table(name, size=22)` (`.label .frame .head .rows[i]
    .cell(i, j)`), `place(mob, left=, top=, right=)`, data `KID_ROWS`, `SCHEMA`. Column names are size 24;
    scale the map ≥ 0.5 where the cards must be readable (s2's corner map is a locator only).
  - s4 the Venn **READY** (scenes/ch1_s4_setops.py; for ch1 s8, ch7 s6, ch8 s3): `load_scene("ch1_s4_setops").venn()`,
    static VGroup at ORIGIN: `.crime .drama` (circles), `.crime_only .both .drama_only` (also `.regions`,
    fill 0), `.crime_name .drama_name .crime_tag .drama_tag .crime_total .drama_total`, `.counts[key]`
    (crime_only, both, drama_only, crime, drama); `fill(v, keys)` → animations filling those regions.
  - s1 READY: `load_scene("ch1_s1_hook")`: `brick(tex, caption=None)`, `group_brick()`, `keep_brick()`,
    `count_brick()`, `tower()` (`.base`, `.bricks`, `.icons`, `.captions`), `table_card(name)`,
    `select_form()` (`.slots["GROUP BY"].kw` / `.box`), `slot_content`, `slot_tick`, `carry` (API in its docstring).
  - s3 READY: `load_scene("ch1_s3_form")`: `having_query(size=34)`, `result_table(size=32)` (`.header .years
    .counts .rules`), `run_column()` (`.stages[name]` → `.box .kw .num`), `YEAR_COUNTS`.
  - s5 READY: `load_scene("ch1_s5_derived")`: `derived_code(select=…, name=True, size=30)` (+ `inner_glyphs`,
    `outer_glyphs`), `derived_result(size=36)`, `plan_diagram()`, `having_code()`, `handover_shot()`.
  - s6 READY: `load_scene("ch1_s6_with")`: `with_code(size=28, comments=True)`, `chained_code()`.
  - s7 READY: `load_scene("ch1_s7_scalar")`: `subquery_code(size=30)` (`(SELECT AVG(rating) FROM ratings)`)
    and `avg_chip(size=30)`, the GOLD `7.17` chip (`.box`, `.value`), static, at ORIGIN (ch1 s8, ch2 s1).
- Waves (done): s1, s2, s7 → s3, s4, s5 (s1's form and bricks) → s6 (opens on s5's handover shot), s8.
- Music: `music/ch1.json`, Hypothesis (hook), Focal Point (s2's walk of The Kid, c1.schema.3),
  Stepwise (recap and end card).
- Narration rewritten for the ear (re-voiced with `--only`; `vk qa 1` now flags only "sequel" in them):
  c1.setops.1 "Union keeps the movies in either, one thousand, nine hundred and fifteen. And except keeps
  Crime without Drama" → "…in either genre, one thousand nine hundred and fifteen. And Crime except Drama
  leaves the Crime movies that are not Drama, …" (heard "either 10915", then "1000, 915", and "Accept keeps");
  c1.recap.1 "but a sequel query is a form" → "but in sequel, every query is a form" (heard "a simple query" /
  "a Cpl query").
- Accepted voice-QA flags: "sequel" → "SQL" (c1.hook.1, c1.hook.3 ×2, c1.setops.1, c1.setops.2, c1.setops.3,
  c1.derived.1, c1.derived.3, c1.recap.1; the course's pronunciation, COURSE.md); c1.derived.2 "Duck D B" →
  "DuckDee B" / "Duct D B" (spelling).
- **Ear check after the Gemini reset** (`vk listen 1 --only …`, one call): the two rewritten lines (c1.setops.1,
  c1.recap.1), plus c1.hook.1 ("sequel"), c1.form.3 ("N-movies", "binder error", "count star"), c1.derived.2
  ("Duck D B"), c1.with.2 ("OCaml", "let per year equal"), c1.schema.3 ("has genre", "has position", "A Tramp"),
  c1.setops.2 ("multisets", "union all"), c1.scalar.3 ("seven point one seven"): nothing has heard them yet.

## Chapter 2 · NOT IN and the NULL trap (ch2_not_in)
State: **ready for final** (2026-11-01). All 7 scenes built by Opus builders; check clean apart from the accepted
flags below; two holds rounds; preview `out/ch2_not_in_preview.mp4` (9.9 min, music 3 cues, handover s2→s3 ok). Built without Gemini (off until 2026-11-04):
no `vk listen`/`vk review` yet; Whisper vote + holds + builders' `--frames` motion sheets instead.
- **Opening card (for ch1's last scene, s8, to end on):** `load_scene("ch2_s1_hook").open_card()` will
  return the static VGroup of ch2's first frame, which is ch1's script's end card (c1.recap.3 {shape}/{next}):
  three shape icons in a row, each with a label and its SQL slot under it. No "?", no updaters, nothing else.
  `.grid` (table icon: 3 columns × 4 rows of 0.55 × 0.40 cells, BLUE stroke 3, header row BLUE fill 0.35),
  centre (−4.5, 0.6); `.cell` (one 1.5 × 0.8 cell, BLUE stroke 3, BLUE fill 0.12, GOLD "7.17" size 36 inside),
  centre (0, 0.6); `.column` (one column of 6 cells of 0.55 × 0.40, BLUE stroke 3, header cell BLUE fill 0.35),
  centre (4.5, 0.6). `.labels` = "a table", "a value", "a column", T size 36 FG, centred under each icon at
  y = −1.25. `.tags` = Mono size 32 at y = −1.95: `FROM` DIM, `>` DIM, `IN` BLUE. ch1 s8: the DIM column and
  its "?" end as the bright `.column` and the BLUE `IN` tag; land on exactly `open_card()` (add it, or morph
  into it). ch2 s1 holds it 0.7 s, then clears to the title card on {title}.
  **Built, READY** (`scenes/ch2_s1_hook.py`, 2026-11-01, check clean): `open_card()` has `.grid .cell .column
  .labels .tags`, exactly the numbers above (the cell's "7.17" is `T("7.17", 36)` GOLD; labels centred at
  x = −4.5, 0, 4.5).
- **Needs:** ch3's opening card (`load_scene("ch3_s1_hook").open_card()`): ch2's recap (s7) ends on it, built
  last. Its script end card (c2.recap.3 {next}/{exists}) is The Kid's YELLOW row sending an arrow into a small
  plays_role card with twelve rows lit, a GOLD "at least one?", and `EXISTS` in BLUE; ch2's movie card
  (s2 `movie_card()`) and s4's YELLOW Kid card are the looks to reuse.
- Music: `music/ch2.json`, Occlusion (hook), Centroid (s4's scan and the NULL bar, c2.trap.2–3),
  Endpoint (recap and end card).
- Narration rewritten for the ear (re-voiced, `vk qa 2` clean on them): c2.absent.3 "uses the keyword
  except" (was heard "accept"); c2.notin.1 "the list of nineteen twenty-seven and nineteen thirty-one"
  (was heard as a range); c2.trap.3 "So what happens to not in, when…"; c2.derive.1 "take apart the
  operator not in", "Saying a year is not in the list means that…" (was heard "You're not in"), "one long
  chain of comparisons, all joined by and" (was "chain of ands" → "ends", then "of and operators" → "of in
  operators" by all three models; the new ending is heard right by medium, "by an"/"by in" by base and small:
  accepted, ear check after the reset).
- Accepted QA flags: c2.hook.2 "nineteen twenties" → "1920s" and c2.derive.5 "Sherlock Junior" → "Jr."
  (spelling); c2.logic.3 "sequel" → "SQL" (the course's pronunciation); c2.logic.5 "where clause" →
  "A-wear clause" (homophone).
- Waves: s1 (open card, shape icons, slots, trap shot), s2 (movie card, handover to s3), s5 (NULL bar,
  grids, gate) → s3, s4 → s6 → s7 (ends on ch3's `open_card()`). Handover: s2 → s3 (parked Flow/Kaiva,
  0.00% differ); all other joins fade to empty. s7 ends on ch3's `open_card()` exactly, held ~8 s, no mark.
  **If ch3 changes `ch3_s1_hook.open_card()`, re-render ch2 s7.**
- Exports (for ch3 and later): s1 `open_card() shape_icon(kind) corner_icons() four_slots(small) trap_shot()`;
  s2 `movie_card(title, year) leftjoin_query() except_query() handover_shot()`; s3 `or_line() notin_query()
  column_into_in()`; s4 `kid_card() people_strip()`; s5 `death_bar() null_cell() rule_card() truth_grids()
  truth_grids_mini() where_gate() gate_pass() gate_bounce() chip()`; s6 `and_chain() fixed_query()
  final_results()` (the four GREEN movies beside NOT IN's RED "0 rows", for ch3 s4).
- Review round 1 (holds): s4 "should be here" no longer collides with the bar's labels; s5 chips now fly up
  into the grid headers (were up 0.1 s), grids re-laid out (AND and OR side by side with padded cells, NOT a
  1×3 strip); s6 The Gold Rush chain labelled, `3 IN (1, 2, NULL) → NULL` keeps its NULL, AND grid uses s5's
  new sizes. Round 2 (motion sheets + holds): s7's recap grid shows the completed AND table.
- Accepted check flags: s7's 29 small-text flags (the recap's shrunk thumbnails at 8–19 pt; each callback is
  shown readable while its sentence plays, as the brief's 3×2 grid of shrunk callbacks demands, same trade
  as ch1's recap); dwell advisories in every scene where the narration moves on (s1 title card 2.5 s and the
  0.7 s open-card hold, s3's condition copy 0.9 s before it becomes the OR line, s5's flickering candidate
  years, s6's compressing links, s7 "It Happened One Night" 5.1 of 5.5 s).
- Glitches (from builders' `--frames` sheets, no Gemini): s3 ~51.7 s, the subquery's YELLOW box copy
  morphing into the column (`ReplacementTransform(box.copy(), column)`) stacked a second box on the text,
  then a striped yellow blob: fixed (box → plain rectangle, column fades in). s3 ~38.6 s, the column's
  straight path to `IN ( … )` crossed the dimmed `rating >`: fixed (drop, then slide). s5 ~43.1 s,
  TRUE/FALSE/NULL slid across their own chip outlines (box FadeOut and label MoveToTarget together): fixed
  (boxes out first). s7 ~24.0 s, the WHERE tile's three tokens faded in on top of each other: fixed (laid
  out by width). s2 ~65 s, the Total Recall 1990 slide was a 0.4 s rush: now one 1.8 s play; at ~66.4 s the
  flying 2012 card's corner brushes the 1990 card's box (texts don't touch): accepted.
- **Ear check after the Gemini reset** (`vk listen 2 --only …`): c2.derive.1 ("all joined by and": base/small
  hear "by an"/"by in"), c2.absent.3 ("the keyword except": ch3 found the same phrase still heard "accept"
  there; here the vote is clean), c2.logic.5 ("A where clause" → "A-wear"), c2.trap.3 and c2.notin.1
  (rewritten, vote clean), and a general listen of c2.logic.3–4 (true/false/null said many times in a row).

## Chapter 3 · EXISTS: semijoins and antijoins (ch3_exists)
State: **ready for final** (2026-11-02). Preview `out/ch3_exists_preview.mp4`, 12.1 min (725 s), 8/8 scenes, plays end
to end; handover s2 → s3 ok (0.00%). Built without Gemini (off until 2026-11-04): Whisper vote, `vk check`, two holds
rounds, `--frames` sheets on every scene's riskiest plays.
- **Opening card (for ch2's last scene, s7, to end on):** `load_scene("ch3_s1_hook").open_card()` will return
  the static VGroup of ch3's first frame, which is ch2's script end card (c2.recap.3 {next}/{exists}):
  `.kid` The Kid's row (YELLOW card, "The Kid" + "1921") on the left, `.arrow` a YELLOW arrow from it into
  `.card` a small BLUE plays_role card (header + row strips) on the right with `.lit` its twelve Kid rows
  YELLOW, `.question` a GOLD "at least one?" above the arrow, `.exists` a BLUE Mono `EXISTS` under it.
  No counts, no updaters, nothing else. ch3 s1 holds it ~0.7 s, then clears to its title card on {title}.
  **READY** (2026-11-01, scenes/ch3_s1_hook.py, rendered). `open_card(lit=False, exists=False)` gives the unlit
  version. `.kid` YELLOW rounded card 3.6 × 0.9 at (−4.6, 1.0), stroke 3, fill 0.12, "The Kid" T 36 FG and
  "1921" T 36 GOLD. `.arrow` YELLOW stroke 4 along y = 1.0 from x = −2.75 to the card's left edge x = 2.6.
  `.question` "at least one?" T 36 GOLD at (−0.1, 1.55). `.exists` Mono 40 BLUE at (−0.1, 0). `.card`
  plays_role card, centre x = 4.0, 2.8 wide, top y = 2.3, 4.54 tall, BLUE stroke 3, 0.5 header + divider,
  "plays_role" Mono 28 bold; 16 strips 2.4 × 0.15 at pitch 0.24 from y = 1.7, unlit BLUE fill 0.3, `.lit` =
  strips 2–13 YELLOW fill 0.85.
- **Also exported by s1:** `trap_back()` → `.result` (ch2 s1's RED "0 rows" box at (−5.2, −0.6)) and `.cards`
  (the four GREEN movie cards 3.45 × 0.92 in ch2's `four_slots()` scaled 1.15, grid at (0.6, −0.6)).
- **Helpers ch3 exports** (READY = built and rendered):
  - s2 the outer loop **READY** (scenes/ch3_s2_correlated.py; for ch3 s3/s4/s6/s8, ch8 s2):
    `load_scene("ch3_s2_correlated").outer_loop(left_title="movies", left_rows=MOVIE_ROWS, right_title="plays_role",
    right_cols=PR_COLS, right_rows=PR_ROWS, dim_cols=(0,))`, static full-frame VGroup; rows are tuples of strings,
    `None` = a DIM ⋮ row. Parts `.left` (`.title .rows[i]`), `.card` (`.box .header .divider .title .heads .rows[i]`),
    `.counter` (GOLD Mono), `.counter_label`, `.cursor` (outside the group), `.cursor_at(i)`. Animations:
    `move_cursor(loop, i)`, `sweep(loop, run_time)`, `light(loop, idxs, color=YELLOW)`; `set_count(scene, loop, n, …)`.
    Data `MOVIE_ROWS`, `PR_COLS`, `PR_ROWS` (The Kid's 12 real rows), `KID_IDX`. `handover_shot()` (s2 → s3).
  - s5 **READY** (scenes/ch3_s5_semijoin.py): `plan_box(op, detail=None, size=32)` (`.box .op .rule .details`, the
    EXPLAIN box style, for s4), `zimmer_tag(size=36)` (GOLD "Hans Zimmer × 72"), `counts(size=72)` (`.left .right
    .join_n .exists_n`, GOLD 3,281 / 1,086 with DIM "JOIN" / "EXISTS"), `join_code`, `exists_code(size, colored)`,
    `distinct_code`.
  - s6 **READY** (scenes/ch3_s6_loops.py): `semi_code(size=26)`, `anti_code(size=26)`, static Code at ORIGIN, the
    semijoin / antijoin loops with the changed lines and `break` YELLOW (s7 thumbnails, s8 recap).
  - s7 the toolkit card **READY** (scenes/ch3_s7_toolkit.py; for ch3 s8, ch4 s1, ch8 s6's TEAL twin):
    `load_scene("ch3_s7_toolkit").toolkit_card(rows=TOOLKIT_ROWS, title=…, heads=("SQL", "Relational algebra"),
    footer=…, color=BLUE, plain=None)`, static VGroup ~10.1 × 6.95 at ORIGIN: `.frame .title .heads .rule .rows
    .foot_rule .footer .body`; each of the 12 rows is VGroup(`.sql` Mono 28, `.glyph` STIX Two Math 38, `.name`
    T 28); `rows` = list of (sql, glyph, name). The antijoin glyph is ⊳ (U+22B3).
  - s1: `open_card()` and `trap_back()` above.
- Handover: s2 → s3 (s3 keeps the query and the loop). All other joins fade to empty.
- **Needs ch4's opening card:** ch3 s8 (recap, built last) ends on `load_scene("ch4_s1_hook").open_card()`.
  Proposal for ch4's director (ch3's script end card, c3.recap.5 {next}/{doc}): ch3 s7's BLUE toolkit card
  (`load_scene("ch3_s7_toolkit").toolkit_card()`, READY, see above), scaled down on the left, and on
  the right an outlined TEAL document card for The Kid with a single TEAL `{` inside. Please record it in
  your section and mark it READY once `scenes/ch4_s1_hook.py` exports it.
- Narration rewritten for the ear (re-voiced): c3.anti.1 "Flow's subquery returned zero rows, so Flow stays"
  (was "Flow is kept", heard "capped") and "with the keyword ex-cept" (heard "accept"; "the keyword except" alone was still heard "accept"); c3.immune.4 "With not
  in, every comparison was linked into one long chain of and operators" (was "Not in joined", heard "Not
  enjoined"); c3.semi.1 "Now take away the word not" (was "drop the not", heard "knot"); c3.loops.2 "Now the
  append adds only the person" (was "It appends", heard "It depends"); c3.kit.2 "and the keyword ex-cept"
  (heard "accept"); c3.recap.2 "a null value in its why column" (was "a null in", heard "a no in").
- Accepted QA flags: "sequel" → "SQL" (c3.kit.1, c3.kit.3 ×2; the course's pronunciation); "role" → "roll"
  (c3.anti.2, c3.anti.3; homophone); c3.anti.3 "is null" → "isNull" (spelling); c3.immune.1 "Sherlock
  Junior" → "Jr." (spelling); c3.semi.1 "joined to" → "join to", c3.loops.1 "loop join" → "loop joined",
  c3.loops.3 "matched" → "match", c3.anti.1 "returned zero" → "returns 0" (minor, meaning kept).
- **Ends on ch4's card (reversed join):** s8's last frame is exactly `load_scene("ch4_s1_hook").open_card()`, held
  ~8 s, no fade and no handover mark (as ch1 s8 does for ch2). `vk check`'s "scene end: pieces left on screen"
  flag on s8 is accepted for that reason.
- **Accepted flags:** dwell advisories in every scene (labels cleared on their next cue by design); small text:
  s6's code at 24 (slide 67's verbatim 54-character lines), s8's Exercise 13 pairs at 24 (verbatim, up to 58
  characters), s8's end-card toolkit at 0.61 (ch4's spec), s8's recap slot thumbnails and ch2's AND chain at 22–26
  in the c3.recap.2 hint. Departures kept: s3's loop isn't "smaller" (the check's floor), s5's semijoin picture
  uses made-up people Ana/Ben/Cleo, s7's loop thumbnails are bars (code would be size 6) and its antijoin glyph is
  ⊳ (▷ renders oversized), s4's AND chain is ch2's summary pill (ch2 s6 has no per-link chain), s8's r4 shows only
  the two inner loops (to read at 26).
- **Glitches:** s4 ~28.0 s (c3.immune.2 {why}): the people strip, shrinking and fading out, is drawn faintly over
  the incoming death bar for ~0.3 s; cause: a simultaneous FadeOut(strip) + FadeIn(bar) in the same place (a
  cross-fade between unlike objects). Low contrast, accepted. All other `--frames` sheets (s1, s2, s3, s5, s6, s7,
  s8) showed clean in-place fades.
- **Ear check after the Gemini reset** (nobody has listened to this chapter): `vk listen 3` on the whole chapter, and
  above all the rewritten lines c3.anti.1 and c3.kit.2 ("ex-cept": does it sound natural?), c3.immune.4,
  c3.semi.1, c3.loops.2, c3.recap.2; the homophones c3.anti.2 / c3.anti.3 ("role"), c3.anti.3 ("is null"),
  c3.loops.3 ("matched"). No `vk review` was run for any scene: motion was checked only on `--frames` sheets.
- Music: `music/ch3.json`, Clarity (hook), Orbit (s2's outer loop, c3.corr.2), Ongoing (recap and end card).

## Chapter 4 · A movie in one piece (ch4_documents)
State: **ready for final** (2026-11-02 00:35), with the motion check still owed (open item 1 below). Preview:
`out/ch4_documents_preview.mp4`, 11.1 min (667 s), decodes end to end; no in-chapter handovers. Gemini off until
2026-11-04: no listen/review ran; Whisper vote + holds only.
- **Resume here (2026-11-02 00:35):** all seven scenes built and rendered at 480p (s7 at 53.2 s: the five
  callbacks, then it builds exactly ch5's READY `open_card()`, holds it 7.7 s through the end card and fades to
  empty; no handover mark). `vk check` on all seven: only small-text, dwell, and (s7) "Charles Chaplin"
  overlapping itself inside ch5's tilted fan (ch5's card, must land on it exactly): accepted below. Holds round 1
  (`media/ch4_holds.png`, 00:30) read: every tile matches its line, no cut-offs, consistent TEAL/BLUE looks;
  no fix notes sent. Still open: (1) motion check without Gemini, i.e. `--frames` contact sheets of the riskiest
  plays (s1 {flat} pieces splitting and {question}; s3 values gliding into the card, card ↔ `kid_tree` swaps;
  s5 {split} strips; s7 schema cards collapsing into the Kid card), one sheet per scene; (2) the readability
  doubts below, as questions to builders if anyone wants a round 2; (3) done: `vk preview 4` ok (00:33). All joins inside ch4 fade to empty (no in-chapter
  handovers).
- **Readability doubts (round 2 candidates, not bugs):** s4 c4.person.4's directed array at Code 15.5 and s1's
  schema-map column names at 16 are the smallest text in the chapter; s7's r2 Kid card and r4 two-way thumb read
  only as shapes; s4 c4.person.2 shrinks Chaplin's card to an unreadable thumbnail beside Hitchcock's.
- **After the Gemini reset:** `vk listen 4` once, then ONE batched `vk listen 4 --only <ids>` re-check; ear-check
  these first: c4.person.2 (both rewritten sentences), c4.person.4, c4.store.3, c4.recap.1 (rewrites), c4.store.4
  "dollar G T E", c4.store.5 "learned" and "My sequel, sequel light" (accepted Whisper flags), c4.json.4 "OCaml",
  "int". One `vk review` round of the seven scenes is still owed (none ran).
- **Accepted check flags (brief demands):** small text on the slide-verbatim JSON cards (s3 slide 71 at Code 18,
  s4 slide 72 at Code 16 and the directed array at 15.5, s5's two cards at Code 20 and slide 73's fields at Mono 22),
  s1's seven-card schema map at 16–17 beside the page and its toolkit callback at 13–18 (a locator, judged on the
  holds still to do), s6/s3 dwell advisories on code that the narration walks. Builders' departures: s2 fades code
  and tree out instead of shrinking them to corners (text minimum); s3 builds the card from The Kid's own tables,
  the schema map only at {ten}; s5's {own} shows only the cast part of s1's page; s6 back cards of the collection
  stack show only their first line.
- **Opening card (for ch3's last scene, s8, to end on):** `load_scene("ch4_s1_hook").open_card()` will return
  the static VGroup of ch4's first frame (ch3's script end card, c3.recap.5 {next}/{doc}), exactly:
  `.toolkit` = `load_scene("ch3_s7_toolkit").toolkit_card()` (unlit), scaled uniformly to fit inside 6.2 × 4.6,
  centred at (−3.3, 0); `.doc` = an empty TEAL document card in s3's `doc_card()` look: rounded rectangle
  3.4 wide × 4.4 tall, centre (3.9, 0), corner radius 0.2, TEAL stroke 3, TEAL fill 0.06; `.brace` = a single
  TEAL `{` (Mono 64) inside its top-left corner (left edge + 0.5, top − 0.6); `.label` = "The Kid" (T 32 FG)
  centred above the card at y = 2.6. Nothing else, no updaters. ch4 s1 holds it ~0.7 s, then clears to its
  title card on {title}. **READY** (2026-11-02, scenes/ch4_s1_hook.py, rendered): `open_card()` → `.toolkit .doc
  .brace .label`, exactly the numbers above (`.doc` = s3's `doc_card(width=3.4, height=4.4)`). ch3 s8 can use
  `load_scene("ch4_s1_hook").open_card()` directly.
  Also s1: `mock_page()` (IMDb mock, static, 6.6 × 7.1 at ORIGIN): `.frame .poster .title .genres .rating`
  (`.header`), `.director .writer` (each `.label .name`; `.crew`), `.cast_head .cast_rows[0..3]` (`.actor .role`),
  `.more` (`.cast`), `.rules`, `.pieces`; data `CAST`.
- **Helpers ch4 will export** (READY once built and rendered):
  - s2 the JSON tree **READY** (2026-11-01, scenes/ch4_s2_json.py, rendered; for ch4 s3/s7, ch6 s1, ch7 s1/s3):
    `load_scene("ch4_s2_json")`: `json_tree(value, *, open=None, elide_keys=False, counts=False, size=28, …)` →
    `JsonTree` VGroup, a file-tree layout growing right with elbow edges, keys (or DIM array positions) on the
    child's row, TEAL `{ }`/`[ ]` nodes, PINK null, centred at ORIGIN. `open` = list of paths to open (others
    collapse to `{…}`/`[…]` stubs; unopened array elements merge into "+n more"); `elide_keys` folds keys off the
    open paths into "+n more keys". Paths are tuples of keys/positions (`()` root, `("languages", 1)` "French").
    Parts `.nodes .edges .labels .kinds` (dicts by path), `.paths`, `.root`; `.node(*p) .edge(*p) .label(*p)
    .branch(*p) .children(*p) .subtree(*p) .depth_parts(d)`; call `settle(scene, tree)` after growing it piecewise.
    `ada_value()`, `ada_code(size=30)` (TEAL braces, PINK null), `ada_tree(**kw)` (~10.1 × 5.6 at size 30);
    `kid_value()` (the real stored document), `kid_tree(**kw)` (14 top-level keys, actors → [ ] → { } → roles →
    "A Tramp" open; ~12.7 × 6.6 at size 26, full frame). Text minimum is 26: scale trees only by subsetting.
  - s3 the document card **READY** (2026-11-01, scenes/ch4_s3_movie.py, rendered; for ch4 s1/s4–s7, ch5–ch8):
    `D = load_scene("ch4_s3_movie")`: `D.doc_card(src=None, size=24, width=None, height=None, pad=None)` → DocCard
    VGroup `.frame` (RoundedRectangle, corner 0.2, TEAL stroke 3, TEAL fill 0.06) + `.code` (`json_code(src, size)`,
    None when empty); with src the frame fits the code plus a pad, without it is width × height (default 3.6 × 2.4);
    static at ORIGIN (animate `.frame` and `.code` separately). `D.json_code(src, size=24)` = `Code(src, lang="json")`
    with `{ } [ ]` TEAL, `/* … */` DIM, `null` PINK. `D.fit_frame(code, pad=None, size=None, min_w=0, min_h=0)` → a
    new frame round grown code (top-left anchored). `D.kid_doc(size=18)` the finished slide-71 card (~9.5 × 7.5,
    full height; `D.KID_DOC` source, `D.KID_LINES` its 20 lines); `D.comment_glyphs(card_or_code)` one VGroup per
    `/* … */`; `D.coogan_note(width=6.6, size=28)` (`.box` DIM border, `.text`).
  - s4 **READY** (2026-11-02, scenes/ch4_s4_person.py, rendered): `chaplin_doc(size=16)` (slide 72, 22 lines),
    `hitch_doc(size=24)` (five keys, `"directed": [/* 7 items */ ]`), `directed_code()` (Chaplin's real directed
    array), `recap_thumb()` (Chaplin's card 3.6 tall beside Hitchcock's, at ORIGIN); static, docstring in the file.
  - s5 the two-way copies **READY** (2026-11-02, scenes/ch4_s5_shape.py, rendered; for ch5, Lecture 5):
    `two_way(gold=True)`: The Kid's card at x = −3.4 and Chaplin's at x = 3.4 (s3's `doc_card`, Code 20, tops at
    y = 2.2), the brief's actors / acted_in elements, ID arrows `.a1 .a2` both ways, copied name/title/year GOLD;
    same card text and x spacing as ch5 s1's bridge. `recap_thumb()` (it at 0.45), `overview()` (slide 73's cards).
  - s6 **READY** (2026-11-02, scenes/ch4_s6_store.py, rendered; for ch4 s7, ch7 s6): `recap_thumb()` (the movies
    table card with its closed TEAL boxes, ~4.4 × 2.9), `mongo_code(size=24)` (VGroup of slide 75's three
    JavaScript filter pairs; ~13 wide at size 28), plus `JsonTableCard`, `TableCard`, `doc_icon`, `closed_icon`, `chip`.
- **Needs ch5's opening card:** ch4 s7 (recap, built last) ends on `load_scene("ch5_s1_hook").open_card()`.
  Proposal for ch5's director (ch4's script end card, c4.recap.3 {next}/{cost}): s3's TEAL The Kid card with
  "Charles Chaplin" GOLD in its actors element, copies of that GOLD name spread across a fan of DIM movie
  cards (no count shown), a GOLD "buy" tag on one side and a RED "cost" tag on the other. Please record it in
  your section and mark it READY once scenes/ch5_s1_hook.py exports it.
- Music: `music/ch4.json`, Spirals (hook), Gnomon (s2's tree, c4.json.3), Serendipity (recap and end card).
- Narration rewritten for the ear (re-voiced): c4.person.2 "…lists the keys of his document, and there are just
  five. His person ID, name, …, and an array called directed, holding seven films…" (was "Person ID, name",
  heard "Chris and I D"), and "A key is there only if it applies" (was "only when", heard "only one"); c4.person.4 "because, back in the has position table, their job was null" (was "null
  in has position", heard "null and has" by all three); c4.store.3 "Mongo D B groups documents into
  collections, which is its word for…" (was "keeps documents in", heard "and"); c4.recap.1 "where the
  relational database spreads it across seven tables" (was "the tables spread it across seven"). `vk qa 4` now flags only c4.store.4/5 (accepted below).
- Accepted QA flags: "sequel" → "SQL" (c4.store.5 ×3; the course's pronunciation, "My sequel", "sequel light"
  heard as MySQL/SQLite); c4.store.4 "dollar G T E" → "$GTE" (spelling); c4.store.5 "learned" → "learn"
  (tense only, meaning kept).

## Chapter 5 · One fact, one place (ch5_normalisation)
State: **ready for final** (2026-11-02 11:45). Preview `out/ch5_normalisation_preview.mp4`, 10.5 min (630.9 s),
decodes end to end; handover s1 → s2 ok (0.00%); s7 ends on ch6's `open_card()` (no mark, by design). All 7 scenes
built and rendered, two review rounds done (round 2 by a resumed director: s6 fix pass, s7 build + one fix round).
Gemini was off (until 2026-11-04): no `vk listen` / `vk review` ever ran on ch5; the ear check below is still owed.
(Paused 00:50 by the first director, started 2026-11-01 23:30; resumed 11:16.) In the holds tiles, captions at a
frame's very bottom look struck through: that is the tile's label band (measured ≥ 0.5 inside on full frames for
c5.update.4, c5.why.1's locality line, s7's callback lines at y −3.25 and ch6's end card's last trivia line at
−3.50). s7's Flow row at c5.recap.2 is also close to the bottom edge; not measured, accepted.
- **Opening card (for ch4's last scene, s7, to end on):** `load_scene("ch5_s1_hook").open_card()` will return the
  static VGroup of ch5's first frame, ch4's script end card (c4.recap.3 {next}/{cost}), as ch4 proposed:
  `.kid` The Kid's TEAL document card in ch4 s3's `doc_card()` look (a short excerpt: `"title": "The Kid"` and
  the actors element with `"name": "Charles Chaplin"` GOLD), left of centre; `.fan` five DIM TEAL movie cards
  fanned on the right (The Gold Rush, City Lights, Modern Times, The Great Dictator, Chaplin), `.copies` their
  small GOLD "Charles Chaplin" tags, each card its real number (4, 4, 4, 3, 1), no number on screen; `.buy` a
  GOLD "buy" tag on the left, `.cost` a RED "cost" tag on the right. No updaters, nothing else. ch5 s1 holds it
  ~0.7 s, then clears to its title card on {title}.
  **READY** (2026-11-01 23:55, scenes/ch5_s1_hook.py, rendered): `open_card()` → `.kid .fan .copies .buy .cost`,
  static. `.kid` a `doc_card` in Code 19 centred at (−3.8, 0.4): title, actors [ { name: "Charles Chaplin" GOLD,
  `/* … */` }, `/* 9 more */` ]. `.fan` five `MovieCard`s 1.32 × 2.1, TEAL stroke 3 at opacity 0.45, fill 0.03,
  titles T 16 DIM, centres x = 0.125 + 1.44·i, y = 0.45 + [0, .14, .2, .14, 0], tilted [6, 3, 0, −3, −6]°.
  `.copies` their GOLD T 14 tags (4, 4, 4, 3, 1; parts of `.fan`, not separate children). `.buy` / `.cost` T 40
  in a rounded box (corner 0.18, 0.75 tall, stroke 3, fill 0.12) at (−3.8, −2.75) and (3.0, −2.75). ch4 s7: land
  on exactly `open_card()` (add it, or morph into it). s1's bridge after the title was composed from ch4 s3's
  `doc_card()` (ch4 s5 was not built yet), with ch4 s5's real values.
- **Needs ch6's opening card:** ch5 s7 (recap, built last) ends on `load_scene("ch6_s1_hook").open_card()`.
  Proposal for ch6's director (ch5's script end card, c5.recap.4 {next}/{tree}/{tangle}/{shape}): The Kid's
  document as ch4 s2's TEAL JSON tree (`kid_tree()`) on the left, its trivia_entries leaves hanging below their
  key; the "Charles Chaplin" leaf YELLOW on the actors branch, with five small TEAL movie nodes (The Gold Rush,
  City Lights, Modern Times, The Great Dictator, Chaplin) each sending a branch to it; on the right a TEAL
  document outline with a YELLOW "?" over it. No title, no counts, no updaters (it is close to ch6 s1's
  {others}/{checks} pictures, so s1 can reuse its own parts). Please record it in your section and mark it
  READY once scenes/ch6_s1_hook.py exports it. (ch6 recorded it READY 2026-11-02, its section.)
- **Helpers ch5 exports** (READY = built and rendered; APIs in each file's docstring):
  - s1 **READY** `load_scene("ch5_s1_hook")`: `open_card()` (above), `handover_shot()` (`.split .left .right .q`),
    `split_frame()`, `people_side()` (`.card .one .strips .arrows .label`), `docs_side()` (`.own .cards[i]` with
    `.frame .title .tags`, `.counter`), `question()` (`.bug .feature`), `recap_r1()`, `movie_card(title, n, …)`.
  - s3 **READY** `load_scene("ch5_s3_update")`: `recap_r2()` (`.update .row .left .copies .bad`, ~7.4 × 2.6),
    `old_bar(width, height, size=27)` (the DIM "old name" bar that stands in for Lana Wachowski's former name).
  - s4 **READY** `load_scene("ch5_s4_genres")`: `recap_r3()` (`.blue` genres card `.rows[genre_id]`, `.teal`
    `.chips[name]`, `.gaps`, ~11.5 × 5.4); data `GENRES`, `EMPTY`, `DOC_GENRES`.
  - s5 **READY** `load_scene("ch5_s5_forms")`: `title_card(size=20, pitch=0.4)` (`.base` ch1 RowTable, `.title_col`
    `.frame .head .cells`), `list_cell(size=28)` (`.box .value`), `recap_r4(size=24)` (`.rows .array`),
    `genres_line(size)`.
  - s6 **READY** `load_scene("ch5_s6_why")` (2026-11-02 00:31, rendered): `recap_r5()` (~12.9 × 3.8; `.map`
    schema map at 0.42, `.source` GREEN label, `.arrow`, `.query` YELLOW, `.stack`, `.derived`),
    `derived_stack(with_label=True)` (`.docs` back to front, `.label` TEAL "derived data, like a cache"),
    `mini_doc(width=1.9, height=2.4, color=TEAL)` (`.back .frame .brace .lines`). Tallies (movies.duckdb): movies 1,
    ratings 1, has_genre 3, genres 3, has_position 14, people 10, plays_role 12 = 44 rows.
  - s7 **READY** `load_scene("ch5_s7_recap")` (2026-11-02 11:36, rendered; for ch9 s1): `ex_card(n, size=30)`, n = 15
    or 16, the Exercise card in ch3 s8's look (`.box .text`, YELLOW "Exercise 15."), static, at ORIGIN.
- Waves: s1, s3, s4, s5 → s2 (opens on s1's handover shot), s6 (needs ch4 s1's mock IMDb page) → s7 (needs
  ch6's opening card and ch3 s8's exercise-card look). Handover: s1 → s2; all other joins fade to empty.
- Review round 1 (s1–s5, 2026-11-02 00:05–00:20; check + holds + builders' `--frames` sheets):
  - s1: the title card's three lines now arrive together and hold until {count}. Tags on the movie cards are BOLD
    (they read dull at size 17); "feature" was confirmed GREEN. The {copies} flight was rebuilt (see Glitches).
  - s2: the c5.terms.2 {join} shot is re-stacked vertically and bigger (it was small, mid-band, mono ~17).
  - s3: the drifting strings at c5.update.4 stop ≥ 0.35 above the RED caption (they were ~0.25 away).
  - s4: no change (the "27 Superhero" row sits 0.48 inside the frame).
  - s5: the c5.forms.2 code and result are centred (the right half was empty), the DIM line is raised, and the fold
    is cleaner.
- Review round 2 (2026-11-02 11:16–, resumed director; check + holds + `--frames` sheets, Gemini off):
  - s6 fix pass (11:25, 94.3 s vs 92.0 s): the {locality} line is ~0.6 inside the bottom (the tile's label band makes
    it look struck through); during {reads}/{doc} the map (0.55), page (0.44) and document (2.3 × 3.0) sit centred
    with the tallies at size 34 below, then the group lifts 1.3 for {locality}; the 44 GOLD trips run ~4.4 s against
    one big TEAL trip; "+1" is bold Mono GOLD and lands with "a second write" (2.3 s held); c5.why.3's read arrows,
    edit arrow and "credits change" land ~2 s before the clip ends (`# early:`, ahead of the words by ~2.2 s,
    accepted: the picture is cued at {movies}). Exports unchanged.
  - s7 built (11:29, 127.9 s vs 115.7 s incl. the 8 s end card). Departures: recap in ch3 s8's way (each callback
    large on its {r} mark, then shrunk into one of five top slots, pictures only); cards read "Exercise 15." /
    "Exercise 16." like ch3 and ch6 (not "Exercise 15 ·"; ch9 s1 should match); Kaiva's has_position /
    plays_role are ch2 s3's schema cards with "10 actors" / "0 roles" under them, not drawn rows; r2's and r4's
    lines arrive with their pictures. Ends on exactly `ch6_s1_hook.open_card()`, no fade, no mark.
  - s7 fix round (11:36, from the 11:30 holds): {compare} rebuilt so the frame is balanced (query on top, Kaiva's
    two cards + Flow's row on the left, held to the clip's end, ~8 s; s6's stack on the right with the YELLOW arrow
    from the result); the large callbacks fill the 12.4 × 4.9 stage under the slots (r3 10.4 wide, grid text ~19);
    each callback change is one 1.2 s move, so r4 lands ≤ 1.2 s after {r4}. The 11:37 holds confirm it.
  - `--frames` sheets (s6 {reads}/{cost}; s7 {careful}, {compare}, slot moves, the row clearing, r3 → r4): clean,
    no new glitches. Exercise cards for ch9 s1: they read "Exercise 15." / "Exercise 16." (ch3/ch6 look).
- Accepted check flags (s6–s7): small text (s6's shared mock page and schema map; s7's shrunk slot pictures, the
  schema map inside r5 at 6–9, ch6's end-card tree at 21, ch6's design); dwell advisories on clip-end holds; s7's
  "end: pieces left on screen" (it ends on ch6's `open_card()` with no fade, as ch3 s8 ends on ch4's card).
  - Engine/lib note for s3's owner: `recap_r2()` sets an `.update` attribute, which shadows Mobject.update and
    crashes `play()`; s7 re-wraps the callbacks in a fresh VGroup. Rename it if s3 is touched again.
- Accepted check flags (s1–s5):
  - **small text** (sizes 14–24), because the brief asks for many items:
    - s1: the people card 20, the movie-card tags 17, the actors' surnames 19;
    - s2: the inherited split and `title_card` 20;
    - s4: the 26-row genres grid 22 and the chips 24;
    - s5: the background document card 14 and the 12-row plays_role 20–22.
  - **dwell advisories:**
    - s1: the 0.7 s open-card hold (the join with ch4, by design), and the title card at 3.3 s, the most there is
      before {count};
    - s3: the caption at the scene's end;
    - s4: "Deletion anomaly" 4.5 s and "0 movies" 3.9 s;
    - s2 and s5: short holds where the narration moves on.
- Glitches (from `--frames` sheets, Gemini off):
  - s1 c5.hook.2 {copies} ~33 s: BLUE strip copies flew over the other strips and piled up, then the tags faded in.
    Cause: TransformFromCopy of 21 strips to tags across the split. Fixed: GOLD dots rise, fly in an arc and fade
    as the tags grow.
  - s5 c5.forms.2 ~42 s: departing has_genre rows crossed the table's border, and one fading row sat under the next.
    Cause: rows moving while the frame was still drawn. Fixed: the frame fades first and the rows leave staggered.
    The residual low-opacity overlap with the filling list cell is accepted.
  - s3 c5.update.4: the drift animations were built before the scatter, so they pulled the strings back to the grid.
    Fixed. (A logic bug, not a visual jumble.)
- **Ear check after the Gemini reset** (`vk listen 5 --only …`, one call): the three rewritten lines (c5.terms.4,
  c5.genres.3, c5.recap.1), plus:
  - c5.genres.1 "Food, Inc., from two thousand and eight";
  - c5.forms.2 "Duck D B", "list aggregate";
  - c5.forms.3 "Boyce-Codd";
  - c5.recap.2 "Kaiva", "JSON object function";
  - c5.update.1 "Lana Wachowski";
  - c5.terms.2 "John Morris".
  Nothing has heard them yet. `vk qa 5` is clean (0 flags) after the rewrites.
- Music: `music/ch5.json`, Quaternions (hook), Reflections (s6's read count, c5.why.1), Far Away (recap and
  end card).
- Narration rewritten for the ear (re-voiced with `--only`): c5.terms.4 "Add a title column to plays role. Then
  all twelve of The Kid's rows in that table hold a copy of its title." (was "The Kid's twelve role rows each
  hold", heard "12th roll rows"); c5.genres.3 "a single insert statement creates a genre called Superhero"
  (was "one insert adds a", heard "insert as a"); c5.recap.1 "An index is redundancy too. The values of the
  column it covers are stored in the table, and again in the index." (was "the indexed column's values",
  heard "the index columns").

## Chapter 6 · Documents or tables? (ch6_models)
State: **ready for final** (2026-11-02 12:16). Preview `out/ch6_models_preview.mp4`, 10.9 min (651 s), plays
end to end; no handover marks (every join fades to empty). Gemini off until 2026-11-04: no listen/review was run;
Whisper vote + check + holds only (see the ear-check list below).
- Scenes (render / narration): s1 49.1/46.6 s, s2 74.7/72.6, s3 141.5/135.1, s4 99.9/94.8, s5 78.7/76.6,
  s6 105.6/103.2, s7 101.7/88.4 (incl. the 8 s end-card hold on ch7's `open_card()`, rendered 12:11).
- Fix round (2026-11-02, director resumed 11:16; one round, holds read twice: 11:20 with s3's final render, 12:13):
  s1 `two_way_copies()` now wraps ch4 s5's `two_way(gold=True)` (centred; `.kid .chap .a1 .a2 .arrows .name_k
  .title_c .year_c` …), s1, s3 and s7 re-rendered with it. s3: the grown graph (c6.graph.2 {cross}/{downey}) re-laid
  out so no line passes through a label (28 crossings; "Hank Mann" on two lines; Gold Rush/Chaplin (1992), The
  Kid/Garcia, Goddard/Downey sit close but apart); `recap_thumb()` names drawn as outlines (the "ghosts" were
  neighbouring letters within the lint tolerance, not duplicates). s5: the migration sweep and GOLD "23,179 rows
  rewritten" land on "…twenty-three thousand of them" (~3 s before {docs}); the old/new documents and
  `first_name()` stay through {cost}, clear on {spell} (so the "The price: mistakes are not caught" title arrives on
  {spell}, ~3 s after its words: accepted). s6: {noname}'s RED "'name' is a required property" now up 2.8 s (held
  into {real}); the validator's "valid / or / what's wrong" come in on "checks a document" (2.7 s). s7: recap thumbs
  in a 3 + 2 grid, ~2.5× larger, lines under them; the c6.try.2 hint group ends at y −3.2 (validator box clears the
  bottom); the updates chip icon fits ch4's picture.
- Accepted check flags: dwell advice at clip-boundary fades throughout (195 lines, none hides a cued object before
  its words; the shortest left are s6's 2.7–2.8 s outputs above and s3's clip-4 output lines, 2.7 s, cleared for
  slide 48's loop); s1's t = 0.7 flags (ch5's end card held 0.7 s by design); small text (202 lines): the copies'
  Code 20 (ch4 s5's own cards, 12.4 wide, s3 cannot scale them up), s1's {same} icons (brief asks for small),
  s2/s4/s6 text at 14–24 (judged on the holds: legible), recap thumbnails (4–11) and ch7's card (11, 26: ch7's
  design). s3 and s7 rendered with `--render-anyway` for these.
- Builder departures accepted: trivia leaves cut to their first words (s1, s2); s2 shows tree and relational cards
  in turns; s3 at {twice} moves the graph to the top-left and drops the TEAL panel, two-role entries read "Car Thief
  +1", clip 4's arrows do not re-fire; s4's full-width console and gates header in clip 4; s5's product documents
  leave on {tables}, the wide products card drawn sideways; s5 c6.trade.3 shows the "Did you mean" frame below the
  NULL table, not beside it; s6 wraps the mistake documents one key per line.
- Glitches: none confirmed (no Gemini review; motion not watched).
- **If ch7 changes `open_card()`, re-render ch6 s7** (`vk check ch6_s7_recap --render-anyway`) before the final.
- **Opening card (for ch5's last scene, s7, to end on):** ch5's proposal accepted. `load_scene("ch6_s1_hook").open_card()`
  will return the static VGroup of ch6's first frame (ch5's script end card, c5.recap.4 {next}/{tree}/{tangle}/{shape}):
  `.tree` The Kid's TEAL JSON tree (ch4 s2's `json_tree(kid_value(), open=…)`, text ≥ 26) on the left, its five
  trivia_entries leaves hanging below their key and the actors branch open to its first element's name;
  `.chaplin` that "Charles Chaplin" leaf YELLOW; `.others` five small TEAL movie nodes (The Gold Rush, City Lights,
  Modern Times, The Great Dictator, Chaplin (1992)) around it, `.links` a TEAL branch from each to `.chaplin`;
  `.doc` a TEAL document outline on the right with `.ask` a YELLOW "?" over it. No title, no counts, no updaters.
  ch6 s1 holds it ~0.7 s, then clears to its title card on {title}.
  **READY** (2026-11-02, scenes/ch6_s1_hook.py, rendered). `.tree` = `kid_tree_compact()` (title, "+2 more keys",
  rating, rating_votes, actors → 0 → name, "+4 more keys", trivia_entries with its five short leaves), built at
  Code 26 and scaled 0.8 (text ~21), box (−6.6, −3.5)–(3.09, 0.91). `.chaplin` YELLOW name leaf centred
  (1.65, −0.80), x 0.20–3.09. `.others` five rows at y = 1.10, 0.15, −0.80, −1.75, −2.70: a TEAL `{ }` box
  (0.76 wide) centred x = 4.1 and a two-line title T 28 FG from x = 4.62 ("The Gold / Rush", "City / Lights",
  "Modern / Times", "The Great / Dictator", "Chaplin / (1992)"). `.links` five TEAL lines stroke 3 from (3.72, row
  y) to (3.19, −0.80). `.doc` ch4 s3's `doc_card` frame 1.4 × 1.8 centred (5.85, 2.62), `.braces` TEAL `{` `}`
  Mono 30 in opposite corners, `.lines` three TEAL rules; `.ask` YELLOW "?" T 72 with a BG halo on `.doc`.
  Also exported: `two_way_copies()`, since 2026-11-02 a thin wrapper over ch4 s5's `two_way(gold=True)` (centred,
  cards at x ±3.4, Code 20; `.kid .chap .a1 .a2 .arrows .name_k .title_c .year_c` …; s3 and s7 reuse it).
- **Ends on ch7's opening card:** s7 (built last) ends on part seven's opening picture (c6.recap.2 {next}): a BLUE
  movies table card (ch1 s2's schema-map style) with The Kid's row, its TEAL `movie` cell opening into The Kid's
  TEAL tree (ch4 s2's `json_tree`), `->` and `->>` as TEAL tags beside it. ch7 accepted it and its
  `load_scene("ch7_s1_hook").open_card()` is READY (see Chapter 7); s7 ends on exactly that, held ~8 s, no handover
  mark. **If ch7 changes `open_card()`, re-render ch6 s7.**
- **s7 (recap):** built and rendered 00:38 (101.7 s vs 88.4 s narration, incl. the 8 s end-card hold). Exercise
  17/18 cards verbatim in ch3 s8's `ex_card()` look (DIM rounded box, YELLOW "Exercise 17."), text ~20 (scaled to
  fit); three hint chips with icons (s2 tree + s3 `tangle()`, s1 `two_way_copies()`, s5 products); {hint18} s6's
  `validator()` with one Chaplin document and a YELLOW magnifier, chip "one document at a time", YELLOW "what must
  it look at?", DIM "worked answers: part 10". Recap (fixed 2026-11-02): five `recap_thumb()`s in a 3 + 2 grid,
  each up to 4.2 × 2.0, its line in two lines under it. Ends on ch7's `open_card()`, 8 s hold, no mark. Remaining
  flags: small text in thumbnails and in ch7's card, dwell on chip icons (accepted). **Exercise cards READY for ch10 s2:**
  `load_scene("ch6_s7_recap").exercise_card(17)`, `.exercise_card(18)`, `hint_chip()` ("one document at a time"),
  plus `chip(text, icons)` and `hint18_icon()`; all static.
- **Helpers ch6 exports** (READY = built and rendered): s1 **READY** `open_card()`, `kid_tree_compact()`,
  `two_way_copies()` (wraps ch4 s5's `two_way()`). s2 **READY** `recap_thumb()` (The Kid's tree with rating/trivia leaves
  and seven GREEN one-parent ticks, no caption). s3 **READY** `tangle()` (L4's tangle; {four} copies L5 ch1 s2's
  `tangle()` geometry), `grown()`, `haze()`, `ids_card()`, `person_card(name)`, `fetch_board()`, `movie_grid()`,
  `recap_thumb()`. s4 **READY** `typed_card()` (BLUE people card with slide 26's types), `json_card()` (TEAL
  person_id TEXT / person JSON), `Gate(color, text, solid)`, `birthyear_reply()` (RED `Did you mean: "birthyear"`
  in its BLUE frame), `recap_thumb()`. s5 **READY** `mistake_docs(highlight=True)` (`.docs .keys .quoted`),
  `recap_thumb()` (~18 wide, scale it). s6 **READY** `validator()` (2.8 × 1.1 TEAL box, `.box .label`),
  `schema_card()` (slide 83 in ch4 s3's `doc_card`, 7.1 tall, `.frame .code`), `recap_thumb()`.
  s7 (for ch10 s2): `exercise_card(17)`, `exercise_card(18)` and the "one document at a time" hint chip, in ch3 s8's
  `ex_card()` look; see the s7 line below for READY.
- Waves: s1, s2, s4 → s3 (needs L5's tangle and the two-way copies), s5 (s4's BLUE "Did you mean" frame), s6
  (s4's TEAL gate) → s7 (all callbacks, ch3 s8's exercise-card look, ch7's opening card). All joins fade to empty.
- Music: `music/ch6.json`, Fragments (hook), Fractals (s3's growing tangle, c6.graph.2), Resonance (recap and
  end card).
- Narration rewritten for the ear (re-voiced with `--only`): c6.tree.2 "In our relational database, there is no
  trivia at all. If there were, …" (was "Our relational database has no trivia. If it did,", heard "A relational");
  c6.try.2 "Exercise eighteen lists five properties of our people documents. Which of them can a JSON Schema
  enforce?" (was "…, and asks which a JSON Schema can enforce", heard "Json Seema / JSON SEMA" by all three).
- Accepted QA flags: c6.recap.2 "sequel" → "SQL" (the course's pronunciation); c6.graph.2 "Downey Junior" →
  "Downey Jr." (spelling).
- Ear check after the Gemini reset (`vk listen 6 --only …`): c6.tree.2, c6.try.2 (rewritten); c6.json.1, c6.json.4
  ("JSON Schema", base-only "Jason shima/Sheema"); c6.graph.2, c6.graph.5, c6.json.3 (long spoken numbers);
  c6.schema.1, c6.schema.2 ("Duck D B", "nmae"); c6.recap.2 ("sequel").

## Chapter 7 · Reaching inside a document (ch7_json_sql)
State: **ready for final** (director resumed 2026-11-02 11:16, handed off 11:45). Preview
`out/ch7_json_sql_preview.mp4`, 11.1 min (666.4 s, 8 scenes, 3 music cues), decodes to the end; `vk preview 7`:
handover ok s1 → s2 (0.00% differ), the only marked join. Gemini off until 2026-11-04: no listen/review this
session; Whisper vote, `vk check`, holds and frame grabs only. The ear-check list below still stands.
- **Built this session:** s6 (89.1 s after one fix pass: one 397 in the Venn overlap with "→ 397" beside the
  condition; the three Spielberg rows come in together on {three}), s8 (55.1 s after one fix pass: r2/r5/r6 rebuilt
  as trimmed thumbs, smallest text 18 in r1's tags, 20 elsewhere). s8 lands on ch8 s1's `open_card(lifted=True)`
  (READY 11:35): {next} builds `open_card(lifted=False)`, {rows} lifts the chips to exactly the lifted state, held
  ~8 s, no fade, no handover mark. **If ch8 changes `open_card()`, re-render ch7 s8.** `vk check` doesn't compare
  this reversed join (no mark): worth a frame compare once ch8 s1 is final.
- **Review (holds round 1 + 2, 2026-11-02 11:20–11:42):** open questions settled on full-size frames: s2's small
  tree along the bottom is fully in frame (actors row ~0.8 above the edge), kept; s7's person cards at JSON size 22
  read clearly at 480p, and the true/false row sits ~0.5 above the edge, kept; s3's results rows (Drama, the
  Comedy/Comedy/NULL row) are in frame, only the holds labels covered them. s5's {grab}/{doc} row at code 28 is fine.
- **Accepted `vk check` flags:** small text: s1's shrunk card (locator, scale 0.4) and tree 26, s3's tree 26, s6's
  `mongo_code(24)` (a 57-character line won't fit at 28) and directors tree 26, s7's cards 22 (above), s8's end
  card (ch8's design, table ~11, names 22). s8 "415 pieces left at the end": reversed join, ch8 s1 opens on that
  frame. s3 advice "flashbox" (c7.paths.2 line 326, FlashAround on the whole first query line, its top edge may read
  as an overbar): not blocking, left. Dwell flags (~190): s1's 0.7 s hold of ch6's end card and s2's t=0 pieces
  (the s1 → s2 handover) are by design; the rest are code and result tables that clear when the narration moves on
  (s2's actors array ~0.7 s and Chaplin's object ~1 s, s3's c7.paths.3 lists 2–4 s, s4's Star Wars rows 4 s and the
  DIM Gangs of Wasseypur note 2.1 s, s5's bare `movie` 0.6 s as it swells into the doc card, s6's summary 4.7 s,
  s8's r6 4.0 s), accepted because every one of them is spoken while it's up.
- **Glitches:** none confirmed (no Gemini motion review this session; no builder frame sheet showed a jumble).
- **Opening card (for ch6's last scene, s7, to end on):** ch6's proposal accepted. `load_scene("ch7_s1_hook").open_card()`
  will return the static VGroup of ch7's first frame (ch6's script end card, c6.recap.2 {next}), s1's {open} picture
  plus the two arrows: `.table` the BLUE `movies` table card (ch1 s2's schema-map card style: header `movies`, GOLD
  "2,935 rows", columns `movie_id` underlined and `movie` with a DIM `JSON` tag, four rows in table order, The Kid's
  YELLOW, the others' cells cut off DIM) shrunk on the left; `.cell` The Kid's `movie` cell; `.link` a TEAL line from
  the cell to `.tree`'s root; `.tree` The Kid's TEAL tree on the right (ch4 s2's `json_tree(kid_value(), open=…)`:
  title, year, minutes, genres → Comedy/Drama/Family, actors → [0] → name "Charles Chaplin", the rest folded DIM);
  `.arrows` `->` and `->>` as TEAL tags beside the tree. No title, no updaters. ch7 s1 holds it ~0.7 s, then clears
  to its title card on {title}.
  **READY** (2026-11-02 00:22, scenes/ch7_s1_hook.py, rendered): `open_card()` → VGroup(`.table .cell_box .link
  .tree .arrows`) plus `.cell`, static, no updaters. `.table` = `movies_card()` scaled 0.4, top-left, x −6.00..−2.22,
  y 1.36..3.50; `.cell` The Kid's YELLOW `movie` cell (`.table.cells[0]`, 2 lines) x −4.84..−2.55, y 2.58..2.90;
  `.cell_box` TEAL stroke 2.5 box round it; `.link` TEAL stroke 3 elbow in the left margin (−6.00, 2.74) →
  (−6.35, 2.74) → (−6.35, −1.15) → (−6.00, −1.15); `.tree` = `kid_tree_open()` at size 26, unscaled, x −6.00..4.77,
  y −3.40..1.10 (root `{ }` at x −6.00..−5.05, y −1.41..−0.90; open: title, genres → Comedy/Drama/Family, actors →
  [0] → name "Charles Chaplin"; year, minutes, type in "+3 more keys"); `.arrows` two TEAL tags (Mono 34 in TEAL
  rounded boxes 0.78 tall), `->` x −1.36..−0.44 and `->>` x −0.04..1.17, both y 2.06..2.84. ch6 s7: land on exactly
  `open_card()` (add it, or morph into it). s1 also exports `movies_card()` (`.box .header .title .count .lines .heads
  .underline .tag .ids[i] .cells[i] .rows[i] .cell .cell_right(i)`) and `kid_tree_open()`.
- **Closing picture (for ch8 s1, reversed join):** superseded: ch8 s1 owns it as `open_card()` (READY, see ch8's
  section) and ch7 s8 (built 2026-11-02) lands on it; s8 exports no `next_card()`. Original proposal, for the record:
  `load_scene("ch7_s8_recap").next_card(lifted=True)`, the chapter's end card exactly: s1's BLUE `movies` table card
  (`movie_id`, `movie`), The Kid's row YELLOW with a GOLD "1 row" tag, its `movie` cell open on a TEAL
  `"actors": [ … ]` in ch4 s3's `doc_card()` look holding ten small TEAL name chips in array order (Charles Chaplin,
  Edna Purviance, Jackie Coogan, Carl Miller, Albert Austin, Beulah Bains, Nellie Bly Baker, Henry Bergman, Edward
  Biby, B.F. Blinn); with `lifted=True` the chips hang half way out of the cell toward ten faint BLUE row slots,
  with `lifted=False` they sit inside the cell (ch8 s1's {cell} picture). ch8 s1 opens on `next_card()` (default
  lifted=True: hold ~0.7 s, clear to its title card) and can rebuild `next_card(lifted=False)` on {cell}.
  READY is marked here once s8 is rendered.
- **Helpers ch7 exports** (READY = built and rendered):
  - s1 READY: `open_card()` (above), `handover_shot()` (open_card + third tag `$.actors[0].name` at x 1.57..6.45,
    y 2.06..2.84; s2 opens on it), `movies_card()`, `kid_tree_open()`.
  - s4 READY: `star_wars_query(size=28, cast_gold=False)` (`.arrows` the two parenthesised `->>`, `.spans` both
    parenthesised expressions, `.parens` (open, close) pairs, `.cast` the `::INTEGER`); `dict_grid()` ('99' over
    '321', `.grid .col_box .cells[r][c]`, first column boxed YELLOW) for s8's r3.
  - s5 READY: `recap_thumb()` (`.code` `(movie->>'year')::INTEGER` with YELLOW parens, `.err` the struck RED
    Conversion Error above it) for s8's r4.
  - s6 READY (2026-11-02, scenes/ch7_s6_arrays.py, rendered 88.6 s): `recap_thumb()` for s8's r5, static at ORIGIN,
    ~5.8 × 5.2: `.venn` ch1 s4's `venn()` with the overlap filled BLUE (its GOLD 397), `.row` BLUE Mono
    `list_contains` → DIM arrow → GOLD `72` below it.
  - s7 READY: `recap_thumb()` (`.cards` the BLUE and TEAL 1,086 cards, `.typo` `birth_year` → PINK NULL) for s8's
    r6; `teal_card()`, `blue_card()`.
  - s3 READY (99.6 s): `list_box(items, size, item_color, bracket_color, quoted, per_line, serif, frame)` (`.items
    .punct .frame`; BLUE DuckDB list); `walk_tree(lit=(), keys=WALK_KEYS, open=(), size=26)` (static Kid subset, lit
    paths TEAL; for s6: `walk_tree([("directors", 0, "name")], keys=("movie_id", "genres", "actors", "directors"))`);
    `light_step(tree, path, on=True)` (animations), `light(tree, paths)` (static). s3 stacks the query above the tree
    (side by side doesn't fit at 26); the nine other actors are one merged "+9 more" node; ten names in 3 lines.
  - s2 READY (82.7 s; opens on s1's handover shot, 0.00% differ): `recap_thumb()` (~6.6 × 1.6: `->` → TEAL
    `"The Kid"` + `json` tag, `->>` → BLUE `The Kid` + `varchar` tag) for s8's r1. Departures: the small tree sits
    along the bottom (size 28), not top right, and the card fades instead of shrinking, so flights don't cross the
    query; short dwells on the actors array (~0.7 s) and Chaplin's object (~1 s), the PostgreSQL footnote 3.6 s.
- Waves: s1, s3, s4, s7 → s2 (opens on s1's handover shot), s5 (s4's Star Wars query), s6 (s3's list box and
  small tree) → s8 (all callbacks). Handover: s1 → s2; all other joins fade to empty.
- Colour rule for the chapter: TEAL = a JSON value, BLUE = an SQL value (strings, DuckDB lists), PINK = NULL,
  GOLD = counts and numbers.
- Music: `music/ch7.json`, Machinery (hook), Quantum Blue (s3's walk, c7.paths.2), Fives (recap and end card).
- Narration rewritten for the ear (re-voiced with `--only`, consensus-clean now): c7.parens.5 "The lecturer himself
  tripped over this one, live, …" (was "Even the lecturer tripped", heard "the lecture tripped"); c7.missing.2 "Add
  the word not, and you count the people with no key called acted in, the ones who never acted. There are seven
  thousand, seven hundred and six of them." (was "Flip it with not, and the people without an acted in key, …
  number …", heard "enacted in" / "not in the").
- Accepted QA flags: "sequel" → "SQL" (c7.arrows.4, c7.paths.5, c7.cast.1, c7.cast.5, c7.arrays.4, c7.recap.3; the
  course's pronunciation); JSON path symbols written as symbols, "dollar dot actors" → "$.actors", "dot name" →
  ".name" (c7.paths.1, .2 ×4, .3, c7.arrays.4; spelling, the words are right); c7.cast.1 "two thousand and two to
  twenty nineteen" → "2002 to 2019" (number format); c7.parens.2 "So Duck D B grouped" → "DuctDB / ducty -b" (base
  and small, jargon spelling).
- Ear check after the Gemini reset (`vk listen 7 --only …`): c7.parens.5, c7.missing.2 (rewritten); c7.parens.2
  ("Duck D B grouped"); c7.paths.1, c7.paths.2, c7.paths.3, c7.arrays.4 (spoken JSON paths: "dollar dot actors,
  star, dot name"); c7.cast.2, c7.cast.4 (digit strings "six, eight", "nine, nine, nine", "two, zero, zero,
  zero"); c7.arrows.2 ("var-char"); c7.cast.5 ("colon colon integer").

## Chapter 8 · Arrays into rows (ch8_unnest)
State: **ready for final** (2026-11-02 12:15). Preview `out/ch8_unnest_preview.mp4`, 11.3 min (676.8 s), plays end
to end; `handover ok: ch8_s1_hook → ch8_s2_unnest` (0.00% differ); 3 music cues. 8/8 scenes built (director
11:16–12:15; earlier session 00:25–00:50 voiced and fixed narration and wrote `music/ch8.json`). Gemini off until
2026-11-04: Whisper vote, `vk check`, holds and builders' `--frames` sheets only; the ear-check list below waits for it.
- **Opening card (for ch7's last scene, s8, to end on):** ch7's closing-picture proposal accepted, but ch8 s1 owns
  it (ch7 s8 isn't built, so neither side waits): `load_scene("ch8_s1_hook").open_card(lifted=True)` will return the
  static VGroup of ch8's first frame (ch7's script end card, c7.recap.3 {next}/{rows}): `.table` ch7 s1's BLUE
  `movies_card()` (`movie_id`, `movie`; READY) shrunk at the upper left, The Kid's row YELLOW, `.tag` a GOLD "1 row"
  chip beside that row; `.cell` The Kid's `movie` cell in a TEAL box; `.link` a TEAL line from the cell to `.doc`;
  `.doc` a TEAL `"actors": [ … ]` in ch4 s3's `doc_card()` / `json_code()` look (READY, not ch7 s1's tree);
  `.chips` ten small TEAL name chips (text ≥ 22) in array order: Charles Chaplin, Edna Purviance, Jackie Coogan,
  Carl Miller, Albert Austin, Beulah Bains, Nellie Bly Baker, Henry Bergman, Edward Biby, B.F. Blinn; `.slots` ten
  faint BLUE row slots in one column on the right. `lifted=True`: each chip half way from its place inside `.doc` to
  its slot, slots shown. `lifted=False`: chips inside `.doc`, no slots (s1's {cell} picture). No title, no other
  numbers, no updaters. ch8 s1 holds `open_card()` ~0.7 s, clears to its title card on {title}, rebuilds
  `open_card(lifted=False)` on {cell}. ch7 s8 lands on exactly `open_card()` (default `lifted=True`; no `next_card()`
  needed in ch7 s8: add it, or morph into it).
  **READY** (2026-11-02 11:35, scenes/ch8_s1_hook.py, rendered 46.6 s; geometry also in its docstring and
  `print_geometry()`). Both states identical except `.chips`/`.slots`. `.table` ch7 s1 `movies_card()` scaled 0.38,
  top-left corner (−6.3, 3.5), 3.59 × 2.04, centre (−4.5, 2.48), The Kid's row y 2.77. `.cell` ch7 s1 `cell_box()`
  TEAL stroke 2.5, 2.30 × 0.42, centre (−4.11, 2.77). `.tag` "1 row" T 26 GOLD in a GOLD rounded box (stroke 2, fill
  0.12), 1.13 × 0.46, centre (−1.74, 2.77). `.link` TEAL stroke 3 elbow from the table's right edge at y 2.77, out to
  x −2.51, down to the doc's top at y 1.19. `.doc` ch4 s3 frame (corner 0.2, TEAL stroke 3, fill 0.06), 5.02 × 4.62,
  centre (−3.79, −1.12); `json_code` size 22, `"actors": [` on chip 0's line, `]` on its own line under chip 9.
  `.chips` RoundedRectangle (corner 0.1, TEAL stroke 2, fill 0.12) 2.48 × 0.34, names T 22 TEAL, array order;
  unlifted x −2.72, y 0.86 → −2.74 (pitch 0.40); lifted = exact midpoint to its slot, x 1.09, y 1.78 → −2.72 (pitch
  0.50). `.slots` (lifted only) 2.78 × 0.46, BLUE stroke 2 at 0.5 opacity, fill 0.08, centre x 4.9, y 2.7 → −2.7
  (pitch 0.6). `handover_shot()` = `open_card(lifted=True)` (s1 → s2). **If ch8 changes `open_card()`, re-render ch7 s8.**
- **Ends on ch9's opening card (reversed join):** proposal for ch9's director (ch8's script end card, c8.recap.3
  {next}/{graph}): two small title cards in the lecture's title-card style, "Part 9 · Solutions: subqueries and
  redundancy" and "Part 10 · Solutions: modelling and JSON queries", and ch6 s3's `tangle()` in Lecture 5's graph
  look (`../l05-graphs/scenes/ch1_s*`: circles, Person PINK, Movie BLUE, plain lines; Charles Chaplin, Jackie
  Coogan, The Kid, The Gold Rush) captioned "Lecture 5 · Graph databases". No updaters. If ch9 s1 hasn't recorded
  an `open_card()` READY here when s8 is built, s8 exports it as `load_scene("ch8_s8_recap").next_card()` and ch9 s1
  opens on exactly that (hold ~0.7 s, clear to its title card). s8's last frame is that card, held ~8 s, no fade,
  no handover mark (the "scene end: pieces left" flag is accepted for that reason).
- **Exports planned** (READY marked here once rendered; APIs in each file's docstring):
  - s7 for ch10 s1/s4–s6: `ex19_card(i)` (i = 1..4, the full card, the notes' text verbatim, ch3 s8's `ex_card`
    look), `ex19_row()` (the "Exercise 19" header, the four DIM cards in a row, "solutions: part 10" tag), `hint(i)`
    the DIM hint line ch10 quotes: 1 "$.*[*] matches every element of every array at the top level of a
    document", 2 "json_array_length", 3 "list_has_any(l1, l2)", 4 "unnest, then AVG of the rating, cast to a
    number"; `hints_line()` "$.*[*] · json_array_length · list_has_any · unnest + AVG".
    **READY** (2026-11-02 11:50, scenes/ch8_s7_try.py, rendered 103.5 s, check passes; APIs in its docstring).
    `X = load_scene("ch8_s7_try")`, all static: `ex19_card(i, size=40)` → `.box .text .head` (ch3 s8 `ex_card` look,
    built at ORIGIN; at 40: 19.1 11.7×3.2 (4 lines), 19.2 10.3×1.8, 19.3 9.5×1.7, 19.4 12.0×2.6; s7 shows it as hero at
    (0, 0.2), then ×0.75 at the top for its hint). `ex19_row()` → `.header .cards .tag` placed for the full frame:
    "Exercise 19" T 52 at y 2.4, four DIM mini cards 3.0×2.0 at y 0, x ±1.625/±4.875 (each with a subject line: "a new
    name", "top directors", "actor-directors", "best genres"), "solutions: part 10" T 30 at y −1.9; overall 12.75×4.9.
    `mini_card(i)` one card alone. `hint(i, size=28, width=None)` → DIM T (hint 1 is 12.6 wide at 28: pass `width=`;
    hint 4 8.4; hints 2/3 ~3.3). `hints_line(size=28)` 10.0 wide. 19.3's same-name pair is John Morris, nm0606657 /
    nm0606658 (checked in DuckDB).
  - s2 for ch10 s6: `unfold()` the unnest motif (The Kid's genres cell unfolding into three rows); s3 for ch10
    s5/s6: `genre_bars()` (GOLD counts, horizontal bars); s1 `open_card(lifted)`, `handover_shot()`.
    s3 **READY** (2026-11-02 11:52, scenes/ch8_s3_group.py, rendered 81.0 s): `genre_bars(size=32, max_len=4.0,
    pitch=0.75, header=True)` ~7.3 × 3.9 at ORIGIN, `.rows[i] .names[i]` (FG) `.bars[i]` (BLUE; grow with
    `GrowFromEdge(.., LEFT)`) `.counts[i]` (GOLD) `.head` (DIM Mono "genre" / "n_movies"); Drama 1,691, Comedy 878,
    Action 869, Adventure 719, Crime 621 (s7's 19.4 uses `size=28, pitch=0.5, header=False`). `recap_thumb()` ~11.4
    wide (`.bars .card .count`, has_genre's GOLD "7,826 rows"). `kid_pairs(size=28)` The Kid's three `title | genre`
    rows (genres BLUE, BLUE frame), top-left at ORIGIN, `.frame .head .rows .cell(i, j)`; builder `pair_table(...)`.
    s2 **READY** (2026-11-02 11:57, scenes/ch8_s2_unnest.py, rendered 109.5 s, opens on s1's handover, frames match):
    `unfold(size=30)` → `.cell` (The Kid's genres, TEAL json cell) `.items` `.table` (the `t(genre)` table under it),
    ~5.6 × 4.1 at ORIGIN; animate with `play_unfold(scene, u, run_time)`. Also `recap_thumb_rows()`,
    `recap_thumb_loop()`, `genre_table()`, `table()`, data `CAST_ROLES`, `SHERLOCK`, `JOIN_ROWS`.
- **Waves:** 1) s1 (first: ch7 s8 needs `open_card()`; s1 marks READY above as soon as it renders), s7 (ch10 needs
  the 19.x cards; READY as soon as it renders), s3, s4, s5, s6, one batch. 2) s2, opening on s1's
  `handover_shot()` (s1 ends on the lifted chips, question cards cleared, `# handover: next`; s2 parks them for
  {small} and lands them on {rows}). 3) s8 (all callbacks; ch9's card or its own `next_card()`). Handover: s1 → s2;
  all other joins fade to empty.
- **Reuses (all READY or built):** ch7 s1 `movies_card()`; ch4 s2 `json_tree`/`kid_tree`; ch4 s3 `doc_card`,
  `json_code`; ch4 s5 `two_way()` (s4 {where}/{lesson}); ch5 s1 `docs_side().counter` (s4 {copy}); ch5 s5
  `recap_r4()`, `list_cell()` (s3 {rebuilt}); ch1 s2 `schema_map()` has_genre card (s3, s8); ch1 s4 `venn()` (s3);
  ch3 s2 `outer_loop()` (s2 {loop}); ch3 s6 semijoin loop (s5); ch3 s7 `toolkit_card()` (s6's TEAL twin, s6 {two});
  ch3 s8 `ex_card` (s7); ch7 s3 `walk_tree`/`light` (s7 19.1 hint); ch7 s4 GOLD `::` (s7 19.4); ch7 s5
  `paren_glyphs` (s4 {select}); ch6 s3 `tangle()` (s8). ch5 s7 / ch6 s7 exercise cards aren't built: s7 follows ch3 s8.
- Music: `music/ch8.json`, Transformation (hook), Sixes (s5's search-engine diagram, c8.text.4), The 3Blue1Brown
  Experience (recap and end card).
- Narration rewritten for the ear (re-voiced with `--only` 00:31, consensus-clean now; `vk qa 8` flags only the 3 accepted below): c8.unnest.5 "{ten} The un-nest version gives ten rows"
  (was "Un-nest gives", heard "A nest gives" by small and medium); c8.recap.1 "{r1} The un-nest function turns a
  list into rows" (was "Un-nest turns", heard "Unnus" by all three) and "like the actors' ages, send you back to
  joins" (was "need joins again", heard "joints" / "drawings").
- Accepted QA flags: c8.hook.3 "sequel" → "SQL" (the course's pronunciation); c8.unnest.3 "B. F. Blinn, Beulah
  Bains" → "Blinon, Bula, Baines" (name spelling); c8.try.1 "dollar, dot, star" → "$.star" (symbols, words right).
- Ear check after the Gemini reset (`vk listen 8 --only …`): c8.unnest.5, c8.recap.1 (rewritten); c8.unnest.3
  (names); c8.try.1 (spoken path "dollar, dot, star, then a star in square brackets"); c8.hook.3 ("sequel");
  c8.text.2 ("I-like"); c8.group.4 ("Mongo D B", "Dollar unwind"); c8.group.2, c8.group.3 (long numbers);
  c8.text.4 ("Elasticsearch and OpenSearch", "Duck D B"); c8.sum.1 ("colon colon integer").
- **Built** 2026-11-02 (480p renders): s1 46.6 s, s2 109.5, s3 81.0, s4 107.1, s5 97.5, s6 58.5, s7 103.5, s8 73.0
  (677 s ≈ 11.3 min; narration 638 s). Handover s1 → s2 0.00% differ; s8 ends on ch9 s1's READY `open_card()` held ~8 s, no mark.
  Review (Gemini off): `vk check`, two holds rounds, one `--frames` sheet per scene. Round 1 fixes: s2 c8.unnest.5
  (the 12-row join result was an unreadable thumbnail: now role/name, 12 rows beside the 10, both size 20) and
  c8.unnest.4 caption raised; s4 c8.join.2 cards/grid moved inside the bottom margin. Round 2: s8 recap grid inside
  the margins, thumbnails scaled to 4.25 × 2.05 slots, {fast} cards raised.
- **Accepted check flags:** small text, all from the brief: s1 the shrunk `movies` locator at 11 (the agreed
  `open_card()` spec, as ch7 s1) and chips 22; s2 the verbatim query and 10/12-row tables at 18–22; s3 the verbatim
  58-char SQL line and `$group` line at 24–26, ch1's has_genre card at 24; s4 JSON cards 22 and ch4 s5's `two_way()`
  at its own 20; s6 slide 93's card verbatim at 24/25 (12.2 wide), ~20 when shrunk, the {two} pair 13–17 ("small");
  s8 the recap thumbnails. Dwell advisories in s1/s5/s6/s7 (narration pace; s7's card row is up ~1.2 s between
  questions). s8 "scene end: pieces left" (ends on ch9's card). s3 c8.group.4: the YELLOW `$unwind`–`unnest` line
  crosses dimmed "DESC"/"db.movies" (minor, text dimmed).
- **Departures accepted:** s5 the six Gene Hackman titles are RED but not tagged one by one (28 titles fill the
  frame; an Unforgiven entry shows "Gene Hackman"), relevance bars illustrative; s4 "+1868" squeezes in beside
  `/* 9 more */` (Chaplin's object is the visible one); s7 19.1's question shrinks to a "19.1" badge during its
  hint (the tree is 6.3 tall); s8 {two} tints the schema map's tables YELLOW (the map has no rows); s1 clip 1 is
  left-heavy (the fixed `open_card()` layout) and the "these work on rows" arrow reaches the row via the "1 row" tag.
- **Glitches:** none confirmed (no Gemini). Transient seen on a sheet: s5 ~13.8 s, the `)` sits apart for ~0.3 s
  while the query collapses into `WHERE EXISTS ( … )` (a multi-line → one-line transform); accepted.
- **Ear-check list** (above) still stands for the Gemini reset on 2026-11-04.

## Chapter 9 · Solutions: subqueries and redundancy (ch9_solutions_queries)
State: **ready for final** (2026-11-02 12:22; director 11:16–12:25). Preview `out/ch9_solutions_queries_preview.mp4`,
12.5 min (747 s), 9/9 scenes, plays end to end; handover s7 → s8 ok (0.00%). Built without Gemini (off until
2026-11-04): Whisper vote, `vk check`, three holds reads (wave 1, waves 1–2, all), builders' `--frames` sheets.
- Scene lengths (render / narration, s): s1 41.4/37.0, s2 102.9/98.4, s3 82.1/77.7, s4 79.0/76.7, s5 82.9/80.6,
  s6 108.3/103.6, s7 117.3/110.5, s8 80.8/75.0, s9 52.6/42.8 (incl. the 8 s end card).
- Fix round (holds; one per scene, no second needed): s5 c9.composers.4 the DIM one-line `AND hp.position = 'actor'`
  fragment (read as a cut-off query) now fades out as the actor counts come in; s6 the denormalised copies were
  ch4 s5's `two_way` at text 9: now a local `two_way_big()` (same look, cut to the copied facts, stacked) at 18;
  s4 c9.notin.4's GREEN caption moved under the result row, clear of the NOT EXISTS query. Confirmed in-frame on
  `--frames` (not changed): s5's DISTINCT caption and brace, s6's CREATE INDEX line, s4's third chain row.
- **Accepted check flags:**
  - small text, verbatim queries and documents that can't fit at 28: s2's four-pair overview (Code 24); s7's naive
    query 23, solution 21, the parked json_object demo 16, The Kid documents 19–21, plays_role list 22; s8's documents
    17–24, patched plan 21, has_position card 24; s6 `UPDATE` 22 and the director query 26;
  - small text, callbacks the brief asks to be small: s4 ch2's AND chain and `trap_back()` (20–22), s8's schema map
    in c9.compare.4 (14–16), s9's recap thumbnails;
  - dwell advisories in every scene (labels cleared on their next cue as the narration moves on; s1's 0.7 s open
    card by design);
  - s9 "scene end: pieces left": it ends on ch10's `next_card()`, no fade, no mark (the reversed join).
- **Departures kept:** s1's {lasttime} callbacks are mini cards (full cards shrink to text 15–17); its card-13 hint
  and four short line labels are the builder's ("IN or JOIN", "ON or WHERE", "LEFT JOIN", "NOT IN"); 15/16 texts
  match ch5 s7's (line breaks differ). s2 the card becomes the strip on {pairs}; verdicts by pill colour, not
  TRUE/FALSE words; the database leaves for pair 2's full-width table. s3's Annie Hall query is a fragment with
  ellipses (no earlier scene shows it); its joined rows carry verdict pills. s4's NOT EXISTS query sits bottom left.
  s5's GROUP BY variant replaces the solution in place (two 7-line queries don't fit side by side). s6's two director
  queries are stacked, slide 34's code sits under card 15. s7's first plan leaves at {kid}, so the solution comes in
  after the lists split; clip 6 shows a FROM/WHERE snippet. s8's JSON The Kid is condensed (crew as a comment), key
  lists are columns, has_position columns in the schema map's order. s9 dims on "document exercises", ~1.5 s after
  {next}, so the grid split stays visible.
- **Glitches:** none confirmed. No `vk review` ran; motion was checked only on builders' `--frames` sheets (s2's
  arcs of 1s, s3's flying joined rows, s4's chains, s5's edits and Alan Parker fold, s7's grid split, s8's crossing
  lines and arcs over the schema map, s9's slot moves). s8's {add} flashes cross the map's cards for a moment.
- **Ear check after the Gemini reset** (`vk listen 9 --only …`, one call; nobody has listened to this chapter): the
  six rewritten lines c9.left.3, c9.left.4, c9.index.1, c9.build.5, c9.recap.1, c9.recap.2; the accepted flags
  c9.pairs.4 ("sequel"), c9.notin.4 ("not exists"), c9.compare.4 ("derived"); the letter words in c9.pairs.1 ("ex",
  "why", "zed") and "the first table / the second table" throughout s2–s4; names c9.composers.4 ("Alan Parkers",
  "Sam Phillips"), c9.build.6 ("Kaiva", "Albert Austin"), c9.compare.2 ("Edna Purviance", "Duck D B"); long numbers
  c9.composers.2, c9.composers.4, c9.build.4, c9.compare.1; c9.build.2 ("JSON object", "List is an aggregate").
- **Opening card (for ch8's last scene, s8, to end on):** ch8's proposal adopted.
  `load_scene("ch9_s1_intro").open_card()` will return the static VGroup of ch9's first frame (ch8's script end
  card, c8.recap.3 {next}/{graph}): `.part9` and `.part10`, two small title cards in the lecture's title-card style,
  "Part 9 · Solutions: subqueries and redundancy" and "Part 10 · Solutions: modelling and JSON queries", stacked on
  the left; `.tangle` ch6 s3's `tangle()` (READY; Lecture 5's graph look: circles, Person PINK, Movie BLUE, plain
  lines; Charles Chaplin, Jackie Coogan, The Kid, The Gold Rush) on the right, `.caption` "Lecture 5 · Graph
  databases" under it. No counts, no updaters, nothing else. ch9 s1 holds it ~0.7 s, then clears to its title card
  on {title}. ch8 s8 lands on exactly `open_card()`.
  **READY** (2026-11-02 11:35, scenes/ch9_s1_intro.py, rendered): `.part9` "Part 9" T 48, a DIM rule 3.6 wide
  (stroke 2), then T 32 on two lines "Solutions: subqueries / and redundancy", centred at (−3.9, 1.55); `.part10` the
  same build, "Solutions: modelling / and JSON queries", centred at (−3.9, −1.75); `.tangle` ch6 s3's `tangle()`
  scaled 0.7, centred at (3.4, 0.35); `.caption` "Lecture 5 · Graph databases" T 30 DIM, 0.45 below the tangle.
  Also READY in s1: `spoiler_banner()` (T 72 bold GOLD in a GOLD rounded box, at (0, 1.1); for ch10 s1),
  `pause_icon(h=1.6)`, `ex_row()` (four cards centred at y 1.5, `.cards[13..16]`; for ch10 s1), `big_card(n)`.
- **Ends on ch10's opening card (reversed join):** ch10 has none recorded yet, so s9 (built last) will export
  `load_scene("ch9_s9_recap").next_card()`, ch9's script end card (c9.recap.2 {next}): the header "Part 10 ·
  Solutions: modelling and JSON queries" over part ten's three exercise cards in a row, 17 and 18 from ch6 s7's
  `exercise_card(17)` / `exercise_card(18)` (READY), 19 from ch8 s7's `ex19_card()` (if READY then, else in the
  same ch3 s8 `ex_card()` look). Proposal for ch10's director: open on exactly `next_card()` (hold ~0.7 s, clear to
  your title card). s9's last frame is that card, held ~8 s, no fade, no handover mark (ch10 adopted it, its section).
  **READY** (2026-11-02 12:19, scenes/ch9_s9_recap.py, rendered), static: `.header` T 40 "Part 10 · Solutions:
  modelling and JSON queries" centred at (0, 3.05), 11.79 wide; `.cards[17] [18] [19]` in ch9 s1's row-card look
  (DIM rounded boxes, stroke 2, corner 0.2), all 5.3 tall, centred at y −0.45, gap 0.15, widths 3.54 / 4.69 / 4.45 at
  x −4.72 / −0.46 / 4.26 (row 12.98 wide). Each card: `.box`, `.head` (T 32 YELLOW "Exercise n"), `.title` (T 30, two
  lines: "Tables or documents?", "What can a JSON Schema enforce?", "Four queries over the JSON database"); 17 and 18
  add `.lines` (five DIM T 28 numbered lines: blog / bank / event log / shop catalogue / app settings; has a name /
  deathyear ≥ birthyear / unique person_id / movie_ids exist / titles match); 19 adds `.subs` (four DIM sub-cards 3.85
  × 0.62, "19.i" T 30 + ch8 s7's `SUBJECT` T 28). Not ch6 s7's / ch8 s7's full cards: these are row cards, like
  ch9 s1's `ex_row()`. **If ch9 s9 changes `next_card()`, ch10 s1 must be re-rendered.**
- **Exports, all READY** (rendered 2026-11-02; APIs in each file's docstring): s1 `open_card()`, `spoiler_banner()`,
  `pause_icon()`, `ex_row()`, `big_card(n)` (13–16; `.hint`, `.pause` are attributes, add them yourself; open with
  `ReplacementTransform(row.cards[n].box.copy(), big.box)` + the text appearing, since a card-to-card
  TransformFromCopy is flagged as a morph); s2 `db()` / `DbCard` (3-row slots), `insert_code`, `pair_code(i)`,
  `strip(i)`, `result_card`, `join_card()`, `recap_r1()`, `recap_r2()`; s3 `padded_row()`, `jrow()`, `recap_r3()`;
  s4 `recap_r4()` (its "NOT EXISTS" label sits on its `3`: s9 uses a local `r4_fixed()`; fix the export if anyone
  else needs it); s5 `recap_r5()`, `person_card()`; s6 `recap_r6()`, `two_way_big()`; s7 `kid_doc()`, `grid()`,
  `recap_r7()`, `handover_shot()`; s8 `recap_marks()`; s9 `next_card()`.
- **Waves:** 1) s1, s2, s5, s6, s7 (s2/s5/s6/s7 add their card opening once s1 has rendered; s5/s7 add the JOIN-card
  callback once s2 has); 2) s3, s4 (s2's database), s8 (opens on s7's `handover_shot()`); 3) s9. Handover s7 → s8;
  all other joins fade to empty.
- Music: `music/ch9.json`, Zeta (hook), Euler's Clock (s7's 3 × 10 grid, c9.build.4), Heartbeat (recap and end card).
- Narration rewritten for the ear (re-voiced with `--only` 11:25, all six clean in `vk qa 9` now): c9.left.3 "Then
  the where clause tests zed on every row" (was "Then where tests zed", heard "we're test Z"); c9.left.4 "Testing zed
  in the where clause even turns the left join back into…" (was "This where clause", heard "This work clause");
  c9.index.1 "An index is redundancy too. The values of the column it covers are stored in the table, and again in
  the index." (was "the indexed column's values", heard "The index columns'"; ch5's c5.recap.1 fix); c9.build.5
  "Instead, build each list on its own." (was "The cure is to", heard "the cures to"); c9.recap.1 "Not in breaks
  when either side holds a null, but not exists still gives the right answer." (was "breaks on a null …, and not
  exists stays safe", heard "on the null", "not exists a safe"); c9.recap.2 "hidden below the logical level" (was
  "below the level queries see", heard "level query C").
- Accepted QA flags: c9.pairs.4 "sequel" → "SQL" (the course's pronunciation); c9.notin.4 "not exists behaves" →
  "not exist behaves" (grammar only); c9.compare.4 "derived from" → "derive from" (meaning kept).

## Chapter 10 · Solutions: modelling and JSON queries (ch10_solutions_documents)
State: **ready for final** (2026-11-02 12:57; director 12:13–12:57). Preview
`out/ch10_solutions_documents_preview.mp4`, 11.3 min (677.5 s), 7/7 scenes, decodes end to end; no handovers in
ch10. The lecture's last frame: s7 holds the end card ~8 s, then fades to empty. Built without Gemini (off until
2026-11-04): Whisper vote, `vk check`, two holds reads, one `--frames` sheet per scene.
- Scene lengths (render / narration, s): s1 49.7/43.7, s2 152.5/147.3, s3 114.7/110.8, s4 95.5/92.3,
  s5 113.5/110.8, s6 93.2/90.2, s7 58.4/48.1 (incl. ~8 s end card).
- **Cross-chapter join ch9 → ch10:** ch9 s9's last frame vs ch10 s1's frame at 0.3 s: 0.008% of pixels differ
  (ok). ch9_s9_recap.py (12:12) is older than ch10 s1's render (12:27); if ch9 s9's `next_card()` changes, re-render
  ch10 s1.
- **Needs an ear check after the Gemini reset** (`vk listen 10 --only …`, one call): c10.schema.1, c10.rename.3,
  c10.genres.2 (rewritten, Whisper-clean now); c10.rename.1 (the path read as "dollar, dot, star, then a star in
  square brackets"); c10.directors.3 ("JSON exists", "Postgres"); c10.directors.5 ("Sherlock Junior", "Buster
  Keaton"); c10.genres.2 also for "un-nest" and "colon colon double"; c10.genres.4 ("Food, Inc."). ch10 has no
  "sequel" lines.
- Fix round 1 (holds + sheets): s2: card 17 size 19 → 24 (‖ beside the hint); the {hybrid} products table now
  holds ch6 s5's three products (My Autobiography / Charles Chaplin, Walking boot / 42, Cinema 55 / 3840x2160), not
  Emma / Jane Austen / screen_inches; orders and stock reduced to header cards so their arrows no longer cross text.
  s3: the size-9 full schema replaced by a size-20 excerpt of ch6 s6's schema (the lines the scene lights, `…` for
  the rest), the enlarged rule row dropped; the RED reply fades before the window moves (66.5 s); the Ajv tag
  inside the frame. s7 re-rendered after both (it loads their recap exports).
- Accepted `vk check` flags: small text on s2's card 17 (24) and s3's card 18 (23), the notes' text verbatim in
  ch6 s7's card; s3's schema excerpt (20) and validator documents (22), to fit window, schema and three columns;
  s6's queries (25) and the {same} relational card and side-by-side tables (22), verbatim queries; s7's recap
  thumbnails (7–26), five callbacks in one grid with their DIM T 30 captions carrying the words. s2's orders /
  stock cards end 0.23 units above the bottom edge at c10.choose.5's end (inside the frame). Dwell advisories
  everywhere follow the narration's pace.
- Builders' departures accepted: s1 draws part nine's cards as heads only (ch9 s1's `ex_row()` text falls to
  18–21 at that scale) and lifts the row 1.3 on {hints} so the hints fit; s4–s6 grow only the sub-card's box
  (text fades), as ch8 s7's `grow()`; s4 wraps the long WHERE lines; s5 uses John Morris for "two people, one name"
  (verified: three person documents share that name); s7 shows "Next: Lecture 5 · Graph Databases" on the spoken
  words and sweeps the grid away before the tangle.
- Glitches (found on builders' `--frames`, fixed): s3 ~66.5 s, the window's "validator" label slid over the RED
  reply still fading out (window shift started during the reply's FadeOut); s4 ~85.5 s, the nine document tiles
  faded in over the outgoing person document card (FadeIn overlapping a FadeOut in place).
- **Opening card (reversed join with ch9):** ch9's proposal adopted. ch10 s1 opens on exactly
  `load_scene("ch9_s9_recap").next_card()` (loaded, not copied, so ch9's later changes carry over), holds ~0.7 s,
  then clears to its title card on {title}. s1's {cards} row reuses the same `next_card()` cards at the same
  positions, and s2–s6 open with their card enlarged out of that row. ch10 records no opening card of its own.
- Music: `music/ch10.json`, One, Two, Zeta (hook), The Wallis Ballade (s4's walk through The Kid's tree,
  c10.rename.2), Grant's Opus (recap and end card).
- Narration rewritten for the ear (re-voiced with `--only` 12:20, all three clean in `vk qa 10` now):
  c10.schema.1 "And every movie title stored in a person document matches the movie's own title." (was "each
  copied title", heard "each copy title"); c10.rename.3 "you'd need list contains five times, once per array" (was
  "five list contains, one per array", heard "five lists contains" by all three models); c10.genres.2 "The top genre
  is Film noir, at eight point two seven" (was "double. Film noir comes top", heard "Bill noir" by all three).
- Accepted QA flags (spelling only): c10.rename.1 "path dollar, dot, star" → "path $.star"; c10.directors.5
  "Sherlock Junior" → "Sherlock Jr.".
- Builders: s1–s6 launched 12:21 in one batch (no handovers; every join fades to empty); s7 (recap) after them.
  Recap exports: s2 `recap_r1()`, s3 `recap_r2()`, s4 `recap_r3()`, s5 `recap_r4()`, s6 `recap_r5()`.

- 2026-11-04 Gemini pass (checks only, nothing fixed): ear checks ch1-10 ran (--only lists from this file). Real (+Whisper): c2.logic.5:3 'where' heard 'were', c6.recap.2:1 'paths' heard 'pass', c8.unnest.3:7 'Blinn' heard 'Blinen', c3.anti.3:4 'the' omitted and c3.semi.1:5 'joined'->'join' (low). ch4 and ch9: 0 findings. Gemini-only claims: 'semijoin'/'antijoin' heard 'semi one'/'anti one' (c3.*, c7.missing.2), Bergman, numbers without 'and', c1.with.2 OCaml, c10.rename.1 Lana; see media/review/ch*_listen_partial.md.
- 2026-11-04 re-voice fix pass (the mishearings from the Gemini pass): c2.logic.5:3 "A where clause keeps" → "In any query, a where clause keeps" (keeps s5's "a where clause" cue); c6.recap.2:1 "a small language for paths" → "a small path language"; c8.unnest.3:7 "Blinn" → "Blin" (screen keeps "B.F. Blinn"); "semijoin"/"antijoin" → "semi-join"/"anti-join" in every spoken ch3 line (c3.anti.3, immune.5, semi.3, loops.2–4, kit.2, recap.4) and c7.missing.2 (the hyphen keeps the "antijoin"/"semijoin" cues; "semi join" was heard "semi-joint"). Pre-tested on the voice's own seeds with Whisper ×3; voiced with the old fixed pacing (project.json "pacing": "fixed" only during `vk voice`, then restored); durations within ±0.5 s. `vk listen --only` (one per chapter): ch2 and ch6 0 findings; every semi-join/anti-join, "where", "paths" and "Blin" now heard right. Gemini-only, accepted: c3.immune.5:4 "fix" → "thicks", c7.missing.2:4 "and" dropped (low), c8.unnest.3:3 "un-nest" → "un-nesk" (already in the 2026-11-04 pass), c8.unnest.3:6 "F." → "S". Whisper-only on re-synthesised, unchanged sentences (Gemini didn't hear them), accepted: c3.loops.3:3 "matched" → "match", c8.unnest.3:1 "from" → "Frem". `vk check --no-render`: no overruns; one new advisory in ch3 s6, label "movies 2,935" up 2.0 s before its word (the new c3.loops.4 take's timings; scene code untouched). `vk finalize 2 3 6 7 8`: all clean (ch2 9:58.0, ch3 12:05.9, ch6 10:51.7, ch7 11:07.6, ch8 11:18.0). Not touched: c8.text.1 and c9.pairs.3 still say "semijoin" (no listen sampled them; probably the same "semi one"). The 2026-11-04 listen reports are kept as media/review/ch{2,3,6,7,8}_listen_partial_2026-11-04.*.
