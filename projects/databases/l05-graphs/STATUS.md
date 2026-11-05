# Graph Databases: status

2026-11-01: project created; planning.

## Chapter 2 · Patterns: vertices, edges and arrows (ch2_patterns)
State: **ready for final** (2026-11-01 ~22:35). Preview `out/ch2_patterns_preview.mp4`, 10.5 min (628.0 s),
decodes end to end; `vk preview 2`: handover ok s4 → s5 (0.00%). Gemini off: built and checked without
`vk review` / `vk listen`.
- **Opening card (for ch1's last scene, s8, to end on):** `load_scene("ch2_s1_hook").open_card()`
  returns the static VGroup of ch2's first frame, which is ch1's script's end card (ch1 s8 {next}):
  the one Cypher line `(p:Person) -[:ACTED_IN]-> (m:Movie)` as a `Code` block (cypher lexer), centred,
  nothing else on screen, no updaters. ch1 s8 fades its dimmed panels out during the end-card hold and
  lands its morph on exactly this object. ch2 s1 holds it, then clears to the title card on {title}.
  **Built** (2026-11-01, scenes/ch2_s1_hook.py, check clean): `open_card()` is a VGroup holding the line
  as `Code` at size 40, cypher lexer, centred at ORIGIN; s1 holds it 0.6 s, then fades it to the title.
  Also exported for later scenes: `sql_block()` (Slide 105's SQL, lang="sql", 13 wide, at ORIGIN) and
  `join_diagram()` (people → has_position → movies boxes; `.boxes`, `.names`, `.links`, `.keys`).
- **Helpers this chapter owns, for other chapters:** **built** (2026-11-01, scenes/ch2_s3_match.py, check
  clean, static, documented in the module docstring): `movie_patch()` returns a `MoviePatch`, 5 BLUE Movie
  and 5 PINK Person circles with 7 DIM person → movie arrows (all real edges, checked with cypher-shell),
  parts `.movies`, `.persons`, `.arrows`, `.vertex(title)`, `.people()`; for ch3 s3 and ch6 s2/s4.
  `stencil(label="Movie", name="m")` returns a `Stencil`, the YELLOW stroke-only ring (radius 0.52)
  with "m" on its upper-left rim and the label above; `.ring`, `.name_tag`, `.label_tag`, `.centre()`,
  `.at(point)`.
- **Needs:** ch3's opening card (`load_scene("ch3_s1_hook").open_card()`): ch2's recap (s7) ends on it
  and is built last. ch1 s2's data-model icons and ch1 s6's two table cards, for s6 ({model}, {generic}).
- Music: `music/ch2.json`, Resonance (hook), Transformation (s3's stencil, c2.vertex.5:end → c2.match.2),
  Orbit (recap and end card).
- Narration rewritten for the ear (re-voiced 2026-11-01, `vk qa 2` clean on all five):
  c2.vertex.2 "Ask for em dot year…" → "Add em dot year and em dot genres to the return clause…"
  (heard "Ask where"); c2.vertex.4 "…a where clause. Em dot title equals…" → "…a where clause, saying
  that em dot title equals…" (sentence-initial "Em" heard "Om"); c2.match.1 "Fitting means…" → "It fits
  only where the labels agree, and where any properties you wrote down agree as well." (heard
  "Bidding"); c2.match.4 "A join in sequel also…" → "In sequel, a join also…" (heard "join and");
  c2.sql.1 "The return clause and select pick…" → "The return clause picks the same two columns as
  select." (heard "clause in select").
- Accepted voice-QA flags: "sequel" → "SQL" (9 lines; the intended word, COURSE.md); "em/pee/ar dot X"
  → "M.title" / "P.name" / "R.rolls" and "is roles a" → "Rolls" (spelling and homophones only);
  c2.sql.1 "name in its" → "name and its", c2.props.3 "actor in one" → "actor and one" (minor, base/small).
- **Ear check after the Gemini reset** (`vk listen 2 --only …`): the five rewritten lines above, plus
  c2.hook.3 ("Neo four J", "ASCII art"), c2.edge.3 / c2.edge.4 / c2.edge.6 ("E T", "A I"), c2.sql.3
  ("Duck D B").
- Scenes: all 7 built by Opus builders (s1–s4, then s6, then s5 after s4's handover, then s7 last).
  In-chapter join: s4 → s5 forward (s5 opens on s4's `handover_shot()`, 0.00% differ); others fade to
  empty. Other exports for the recap: s2 `vertex_hero()`, s4 `et_pair()`, s5 `arrow_forms()` /
  `form_row()`, s6 `edge_join_panel()`. s7's last frame is ch3's `open_card()`, unchanged, held 8 s.
  Review without Gemini: `vk check` and two holds rounds, plus each builder's `--frames` sheet of its
  riskiest play (all read clean). Round-1 fixes: s1 final hold +3.2 s (payoff line dwell); s2 stray
  stub after "exact" (c2.vertex.5); s3 "chapter 3" → "part 3"; s4 A.I. rows lifted; s5 The Kid's name
  under its circle, Keanu pair centred and 1.3×; s6 connectors re-routed through the margins so none
  crosses code (one right-angle crossing of two connectors left in empty space, c2.sql.2).
- Departures from the brief, accepted: s1 table names flash in the SQL instead of flying out, and the
  diagram sits under the SQL (the SQL is 13 wide); s2 SQL ghost uses "…" placeholders; s3 five movies
  (not six), Hook instead of E.T.; s4 and s3 fans carry no edge-type labels (types show on the result
  rows, the tally and the code); s5 The Kid's cast drawn as a column, cypher-shell row set as three
  labelled blocks; s6 Cypher stacked above the SQL rather than beside it; s7 recap panels shown one at
  a time, large, instead of a row of five (in a row their text fell to sizes 6–15).
- Check flags accepted: s1 small text, the one-line payoff Cypher at size 25 (63 characters on one
  line, as the brief's morph needs); s7 small text, ch3's own `open_card()` pattern line at 24, and
  s7 "end: pieces left on screen" (the reversed join: it ends on ch3's opening card by design). ~94 dwell
  advisories, all where the narration moves on (board clears on cue, counters ticking, s5's inherited s4
  rows faded at 0 s, the recap's panels lasting 4–9 s each).
- Glitches:
  - s2 c2.vertex.5, ~97–104 s (settled end): a faint vertical stub of outline stayed just after "exact"
    in the caption. Cause: `FlashAround(cap2, run_time=1.5, time_width=1.5)` left a sliver of its stroke
    when it ended; removing new mobjects after the play didn't catch it. Fixed (second pass) by a colour
    pulse instead of the flash; confirmed gone on the 480p render. The other ch2 scenes use the same
    call and showed no stub in either holds round. Possibly an engine issue (lib.effects.FlashAround).
- Open: nothing blocking. After the Gemini reset, the ear-check lines above and the producer's
  transitions pass are the only Gemini checks this chapter gets.

## Chapter 3 · Co-stars: bigger patterns and counting (ch3_costars)
State: **ready for final** (2026-11-01 ~22:40). Preview `out/ch3_costars_preview.mp4`, 9.2 min (551.5 s;
8.8 min of narration), decodes end to end; `vk preview 3`: handover ok s1 → s2, s2 → s3, s3 → s4 (all
0.00%); s6 ends on ch4's `open_card()` (reversed join, no mark). Built without Gemini (off until Wed
2026-11-04 ~00:30): no `vk listen` / `vk review`; Whisper vote, `vk check`, holds and builders' `--frames`.
Open for the producer: `vk finalize 3`; after the Gemini reset the transitions pass and the ear check below.
**If ch4's `open_card()` changes, re-render ch3 s6.**
- Check flags accepted:
  - small text, size ~23: the one-line pattern `MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]-
    (p2:Person)` in s2 (end), s3 (open and close) and s5 (count.1, before it splits at {slide}): the brief
    wants it on one line (the fold's payoff), and at 28 it is 16 units wide. s4's three-pattern query is
    wrapped instead (6 lines at 28, tokens verbatim).
  - small text, size ~23: s5's eight Harry Potter rows (verbatim titles and years, each with a placement
    icon); in s6 the same rows at size 8 are a 1.3 s picture before they collapse to "Radcliffe · Watson · 8".
  - s6 small V labels at 24 (six panels on one screen).
  - s6 "110 visible pieces at the end": it ends on ch4's opening card by design.
  - Dwell advisories: s1's opening card (0.7 s) and title; s4's first second (s3's eight names fading);
    short-lived notes replaced as the voice moves on (s3 IDs and "nobody is less than themself", s5
    "implied" / "the key is the value", s4 "(1.7 s)").
- Departures from the brief (accepted): s2 shows the current row under the ring during p2's hops and the
  full table on "rows" (no room for a table beside the ring); s2's two one-edge drawings sit side by side;
  s3's placements draw Coogan left, Chaplin right; s4's DuckDB reply drawn as a Mono grid (text borders
  tripped the overlap audit); s5 adds a crossed-out "SQL: GROUP BY name1, name2" card in count.3; s6 panel 2
  opens the one-line V into the comma form (narration order) and shows drawings, not code; panel 3 shows
  only `<>` → `<` beside the twin rows.
- Glitches: none found (no Gemini review; builders' `--frames` at s2's fold, s3's flip and `<>` check,
  s4's star and orderings, s5's tables, s6's panels showed no jumble).
- **Opening card (for ch2's last scene, s7, to end on):** `load_scene("ch3_s1_hook").open_card()` will
  return the static VGroup of ch3's first frame, which is ch2's script's end card (c2.recap.2): two PINK
  Person circles p1 (left) and p2 (right), each with an ACTED_IN arrow (type in small caps along it) into
  one BLUE Movie circle m between them; the caption "co-stars"; the pattern faint beneath it,
  `(p1:Person) -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]- (p2:Person)` (Cypher Code, DIM); a GOLD
  "most often?". Static, no updaters. ch3 s1 holds it briefly, then clears to the title card on {title}.
  **Built, READY** (`scenes/ch3_s1_hook.py`, 2026-11-01). Parts (centre x, y in units): `.p1` PINK "p1"
  (−4.0, 1.4), `.m` BLUE "m" (0, −0.5), `.p2` PINK "p2" (4.0, 1.4): circles r 0.95, stroke 4, fill 0.12,
  italic T 36 label (`.circ`, `.lab`); `.arrows[0/1]` FG stroke 4 into m, centred (∓2.0, 0.45);
  `.types[0/1]` "ACTED_IN" T 28 rotated along each arrow, with backstroke, (∓1.86, 0.74); `.caption`
  "co-stars" T 44 FG (0, 2.45); `.pattern` Code 28 DIM, scaled to 12.6 wide, (0, −2.3); `.most`
  "most often?" T 40 GOLD (0, −3.25). ch3 s1 holds it 0.7 s.
- Uses: ch4's opening card (`load_scene("ch4_s1_hook").open_card()`, ch3's end card c3.recap.3):
  ch3 s6 ends on it, built last.
- Build plan (in-chapter joins): s1 → s2 forward (s2 opens on s1's `handover_shot()`, the dimmed SQL
  boxes); s2 → s3 reversed (s3 owns `open_shot()`, the one-line query + 261476-row table, and
  `kid_ring()`; s2 ends on `open_shot()`); s3 → s4 forward (s4 opens on s3's ring). s4 and s5 end empty.
  Waves: s1, s3, s5 → s2, s4 → s6 (needs ch4's opening card). s1 built (49.8 s); its
  `handover_shot()` is `sql_diagram()` at 0.35 opacity. s3 built (100.1 s): `open_shot()`, `kid_ring()`
  (= `handover_shot()`), `costar_v()` / `big_v()` (the chapter's V look). s5 built (123.0 s):
  `potter_collapse()`, `return_rule()`, `top5_table()` for the recap. s2 built (98.1 s; joins to s1 and
  s3 exact), s4 built (124.1 s; `kid_chords()`, `big_star()`), s6 built (56.3 s; ends on ch4's
  `open_card()`). Review round 1: s5's cypher-shell tables switched to s3's Mono table style; s6's
  panels made legible (no code below ~24) and given margins.
- Music: `music/ch3.json`, Quaternions (hook, START → c3.two.1), Occlusion (s4's chords and tile grid,
  c3.twins.5:end → c3.predict.3), Far Away (recap and end card, swell after c3.recap.3).
- Narration rewritten for the ear (re-voiced with `--only`, both clean in `vk qa 3`):
  c3.hook.2 "held together by three join conditions" → "held together by three joins" (heard "joint
  conditions"); c3.twins.2 "with pee one and pee two swapped" → "with pee one and pee two trading
  places" (heard "P2 swap").
- Accepted voice-QA flags: "sequel" → "SQL" (c3.predict.3, c3.count.3, c3.count.4; the intended word,
  COURSE.md); c3.count.2 "Downey Junior" → "Downey Jr." (spelling); c3.two.4 "the way you'd draw it" →
  "the way you draw it" (same meaning).
- **Ear check after the Gemini reset** (`vk listen 3 --only …`): the two rewritten lines (c3.hook.2,
  c3.twins.2), plus c3.two.4 ("you'd draw"), c3.count.2 ("Downey Junior", "Bonham Carter"), c3.count.5
  ("Ving Rhames", "nineteen ninety-six"), c3.predict.2 ("ten choose two"), c3.count.1 ("count star"),
  c3.two.2 ("person ID", "pee one"): nothing has heard them yet.

## Chapter 1 · From tables and trees to graphs (ch1_graphs)
State: READY FOR FINAL (2026-11-01 ~22:55). Preview `out/ch1_graphs_preview.mp4`, 11.1 min (666.0 s;
10.5 min of narration), plays end to end; `vk preview 1`: handover s2 → s3 ok (0.00%); s8 ends on ch2's
`open_card()` (reversed join). Gemini was off: no `vk listen`/`vk review` run; the Whisper vote (0 flags)
and two holds rounds were the review. Open for the producer: `vk finalize 1`; after the Gemini reset, the
transitions pass and the ear check listed below.
- **Opening card:** none needed (ch1 is the first chapter): s1 opens from empty on the title card.
- **Waits for ch2's opening card:** ch1 s8 (recap, built last) ends on exactly
  `load_scene("ch2_s1_hook").open_card()`. ch2's director: please record it here (its objects and layout).
  (ch2 director: **READY**, scenes/ch2_s1_hook.py: a VGroup holding one `Code` block, the line
  `(p:Person) -[:ACTED_IN]-> (m:Movie)`, size 40, cypher lexer, centred at ORIGIN, nothing else.)
- **Helpers ch1 will export** (other chapters may use them; READY is marked here once built):
  - s2 `tangle()`: the m:n drawing (PINK Chaplin, Jackie Coogan on top; BLUE The Kid, The Gold Rush
    below; three plain lines). For s3, s5, s8, ch5's closing strip, and L4 ch6 s3's tangle (same picture).
    READY: `load_scene("ch1_s2_lasttime").tangle()` (also its `handover_shot()`): circles r 0.5, stroke 4,
    fill 0.2; Coogan (−2.4, 1.4), Chaplin (2.4, 1.4) PINK, names T 32 FG *above*; The Kid (−2.4, −1.4),
    The Gold Rush (2.4, −1.4) BLUE, names below; lines FG stroke 4, cut at the circle edges, order
    Coogan–Kid, Chaplin–Kid, Chaplin–Gold Rush. ~8.0 × 4.5, centred. `.v["coogan"|"chaplin"|"kid"|"gold"]`
    (each `.circle`, `.label`), `.lines`, `.people`, `.movies`.
    Data-model icons (for ch2 s6 {model}): s2's `mini_table(title)` (BLUE card), `mini_doc(title)` (TEAL
    card) and `tangle()`; s4's `tiny_table()` / `tiny_graph()` are the smaller pair of its {power} beat.
  - s3 READY: `load_scene("ch1_s3_shapes").thumbnails()`, the 3×2 grid as at the end of c1.shapes.3;
    `.tiles` social, web, roads, software, knowledge, ours (each `.drawing`, `.caption`, `.tag`, the
    last two tags None).
  - s6 READY: `load_scene("ch1_s6_tables").graph_tables()`, the two table cards (~6.3 × 5.2):
    `.vcard`, `.ecard` (each `.box`, `.title`, `.rows`), `.tails_tag`, `.heads_tag` (for ch2 s6 {generic}, s8).
  - s4 the graph look (vertex circle, label tag, property card, typed arrow with its card) and
    `chaplin_kid()` (Chaplin -ACTED_IN-> The Kid with roles card).
    READY (`load_scene("ch1_s4_propgraph")`): `vertex(name, kind="Person", at=ORIGIN, r=0.5)` (`.circle`,
    `.label`); `label_tag(text, color=FG)` (`.box`, `.text`), `tag_on(tag, v)`; `prop_card(pairs, color=FG,
    slots=None)` (`.box`, `.rows`; numbers GOLD), `card_under(card, v)`, `slot_point(card, i)`;
    `typed_edge(a, b, etype, color=FG, angle=0, side=UP, dashed=False)` (`.arrow .label .tail .head`);
    `grow_edge(line)` (GrowArrow crashes on these); `chaplin_kid()` (`.chaplin .ctag .ccard .kid .ktag
    .kcard .edge .roles`, Chaplin (−3.7, 0.6), The Kid (3.7, 0.6)); `tiny_table()`, `tiny_graph()`.
  - s5 `house_graph()` (Slide 97: Coogan, Chaplin, The Kid, The Gold Rush, ACTED_IN/DIRECTED with cards)
    and `fan()` (Chaplin's five edges to The Kid).
    READY (`load_scene("ch1_s5_moviegraph")`): `house_graph()` = Slide 97 in the tangle's arrangement with
    s4's pieces (tags, cards, ACTED_IN ×3 with Coogan's `['The Child']`, DIRECTED), laid out large and
    scaled 0.93 (cards at size 26); Chaplin's own roles cards are left off (no room). `fan()` = the five
    typed arrows Chaplin → The Kid with their GOLD property text (The Kid left, Chaplin right).
    `seven_tables()` = Lecture 4's seven BLUE cards in a column, findable by table name.
  - s1 the Lawrence–Radcliffe pair with its dashed "?" chain (for ch4–ch5's running pair).
    READY: `load_scene("ch1_s1_hook").pair()` → `VGroup(lawrence, radcliffe, chain, q)`; each person
    `VGroup(circle, label)` (`.circle` r 0.5, PINK stroke 4, solid fill = PINK at 0.2 over the bg;
    `.label` T 30 FG, 0.2 below), at (±4.8, 0.3); `chain` = `VGroup(dashed, *dots)`, a dashed FG arc
    (stroke 3, angle −0.6π, top y ≈ 2.5) with five r 0.2 dots BLUE, PINK, BLUE, PINK, BLUE; `q` YELLOW
    "?" T 64 above. Also `vertex(name, color, r, stroke, size)`.
- Narration: five QA lines rewritten and re-voiced with `--only`; `vk qa 1` now 0 flags.
  c1.last.2 "As rows of a join table, has position" → "As rows of the table in the middle, has
  position" (heard "joint table"); c1.movies.2 "the five rows of has position from before" → "the
  same five rows we saw in has position" (heard "has positioned"); c1.movies.3 "There's no Genre
  vertex" → "There are no genre vertices" (heard "Gen Ray"); c1.tables.2 "The tail and the head are
  foreign keys" → "The tail and head columns are foreign keys" (heard "the hat"/"header four keys");
  c1.recap.1 "every row of has position is an edge" → "… became one edge" (heard "position as an").
- Music: `music/ch1.json`. Centroid under the hook, Gnomon under s3's tour of graphs
  (c1.shapes.2–3), Endpoint from the recap through the end card.
- Scenes: all 8 built by Opus builders in three batches (s1 s2 s4 s7; s3 s5 s6; s8), Gemini off, so the
  review was `vk check` and two holds rounds plus each builder's `--frames` sheet of its riskiest play
  (all clean). Fix passes: s6 (the s4 drawing was at text 12–13 above the DDL: now 0.72 scale, text
  20–22; s5's `fan()` replaces its stand-in; {out}/{into} now light two outgoing / two incoming arrows on
  a tangle-layout graph; s5's `seven_tables()` in {generic}); s8 (recap panels centred and enlarged).
  s2 → s3 is a handover (0.00%).
- Check flags accepted: s8 "visible pieces left on screen" (the reversed join: ch1 ends on ch2's
  `open_card()`); small text in s6 (the full 16-line Slide 96 DDL and the query at 21, as the brief asks
  for the whole slide) and in s8's recap icons; dwell advisories on values the narration moves past
  (s1's teaser query/table, s4's ghosts and notes, s5's job cards and sentence, s6's "?" and tags, s7's
  setup dialog steps).
- Brief departures accepted: s1's Bacon table sits under the query, turned on its side (beside it ran
  off the frame); s2's top names sit above their circles, its three table cards are stacked with ⋈
  between them, the line flies into has_position with `fly` (no line-to-text morph), no DIM rows for the
  other two lines; s3 caption "road network", grid caption on {unknown}; s4's JSON sits below the card
  instead of swapping, roles card just above the arrow, The Gold Rush right of The Kid; s5's Slide 97
  has no roles cards for Chaplin (no room; `['A Tramp']` shows on the fan), position/job cells recolour
  rather than fly (any path crossed text), only plays_role/ratings/genres fly in {fold}; s7's terminal
  lines wrapped at word boundaries (text verbatim); s8's r3 upright, r4 a compact fan.
- Glitches: none confirmed (every builder's contact sheet of its riskiest play was clean).
- Finalize fix (2026-11-01 ~23:10): `vk finalize 1` failed on s1 with `KeyError … 'Jennifer Lawrence'`.
  Cause: the circles' 1.6 s entrance after {two} (3.65 s) ended at ~5.25 s, just after "Lawrence" (5.18)
  began, so `own_word` found no word at 60 fps (15 fps passed by rounding). Fixed in the scene: entrance
  1.2 s (ends ~4.85), name labels 0.8 s, every `own_word` wait has a cue fallback. 1080p60 render of s1
  passes; preview re-run ok, s2 → s3 handover still 0.00%.
- **Ear check after the Gemini reset** (`vk listen 1 --only …`): the five rewritten lines above
  (c1.last.2, c1.movies.2, c1.movies.3, c1.tables.2, c1.recap.1), plus c1.trav.1 ("Neo four J",
  "Duck D B", "Memgraph") and c1.prop.2 ("acted in" for ACTED_IN): nothing has heard them yet.

## Chapter 4 · Paths of any length (ch4_paths)
State: **READY FOR FINAL** (2026-11-01 ~22:25). Preview `out/ch4_paths_preview.mp4`, 10.4 min (623.6 s; 9.8 min
of narration), plays end to end; handover s2 → s3 ok (0.00%). Built without Gemini (off until Wed 2026-11-04
~00:30): Whisper vote, `vk check`, two holds rounds, builders' `--frames` sheets after their riskiest plays.
Open for the producer: `vk finalize 4`; after the reset, the transitions pass and the ear check listed below.
- Scenes: all 7 built by Opus builders. One fix round: s1 (the sweep from `open_card()` to the title card took
  2.2 s, so the title was readable 1.1 s; now 0.8 s before clip 1, title up 3.3 s), s4 (the {placement} patch's
  movies were boxes; now BLUE circles, "every vertex a circle"), s6 (the `8` sat beside the six-join SQL until
  {wrong}; now a DIM "?" on {six}; tag "Cypher: next part"), s7 (the size-8 SQL thumbnail became a readable
  `JOIN has_position AS h1` / ⋮ / `… h6` excerpt; the grid's margins went from 0.31 to ~0.5). I checked s3's
  bank edges against movies.tvdb (no Harrelson–The Hunger Games line). s7's last 8 s are
  `load_scene("ch5_s1_hook").open_card()` itself (reversed join), so ch4's end card is exactly ch5's opening card.
- Departures accepted: s4's layered drawing keeps its films as titled BLUE boxes (nine titles in three columns;
  circles leave no room for the names), with short titles ("Mockingjay 1", "Deathly Hallows 2"); s1's co-star
  query is re-wrapped to 4 lines (same tokens); s2's "4" doesn't fly onto the edges (every path crossed the code),
  GOLD counters 1–4 tick on instead; s5's bare-star query wraps `(b:Person …)` onto its own line.
- Check flags accepted: s6 SQL at size 22 (the brief's 13–16-line, 56-column block beside its reply; legible on
  frames); s7's r5 excerpt at size 20 (recap panel); s7 "doesn't end empty" (ch5's opening card, by design);
  dwell advisories where the narration moves on (title card 3.3 s, `open_card()` 1.0 s hold, s3 step digits,
  s5's people values before {curve}, s6 SQL blocks, s7's panels swept on {next}).
- Glitches: none confirmed. Without Gemini nobody watched motion; builders' frame sheets covered s1 {chain}, s2's
  stamp and `>` drop, s3's token walk, s4's untangle and sum, s5's table → plot, s6's six-join rewrite (b's
  `h4` reads `h .person_id` for ~0.3 s while the `6` fades in: reads as an insertion), s7's sweep and chain morph.
- **Opening card (for ch3's last scene, s6, to end on):** `load_scene("ch4_s1_hook").open_card()` will
  return the static VGroup of ch4's first frame, which is ch3's script's end card (c3.recap.3 {next}/{chain}):
  Jennifer Lawrence (PINK circle, left) and Daniel Radcliffe (PINK circle, right), between them ch1 s1's
  dashed chain (small alternating PINK and BLUE circles bending from one to the other) with a YELLOW "?"
  over it, and a YELLOW line "chains of any length" under it. Nothing else on screen, no updaters. ch4 s1
  holds it (1.0 s), then clears to the title card on {title}. **Built** (scenes/ch4_s1_hook.py, READY):
  `open_card() -> VGroup(pair, line)`, no arguments, no updaters; `.pair` = `VGroup(jl, dr, chain, q)`
  (also `.jl .dr .chain .q`), `.line`. jl: circle r 0.5 at (−4.8, −1.0), PINK stroke 4, PINK fill 0.2 over
  BG, name FG size 30 0.2 below; dr: the same at (4.8, −1.0). chain: arc (−4.3, −1.0) → (4.3, −1.0)
  bending up (angle −0.45π, top y ≈ 0.6), ~55 FG dashes stroke 3, 5 circles r 0.2 stroke 3 BLUE, PINK,
  BLUE, PINK, BLUE at 1/6…5/6 along; q: YELLOW "?" size 64, 0.25 above the arc; line: YELLOW "chains of
  any length" size 40 centred at (0, −3.0). ch3 s6: land on exactly `open_card()` (add it, or morph into it).
- **Helpers ch4 will export** (READY marked here once built): s2 `chain_example()` (Lawrence → Catching
  Fire ← Harrelson → Now You See Me 2 ← Radcliffe), s3 `pill_strip()` (`*2` 0 · `*3` 0 · `*4` 8 · `*5` 0 ·
  `*6` 495, for ch5 s1), s5 `paths_plot()` (paths vs people, log scale, for ch5 s2's "ch4's curves").
  - s2 `chain_example(arrows=True)` READY (scenes/ch4_s2_chains.py): node centres y = 0, x = 2.9·(i−2),
    i = 0–4; `.nodes[5]` (circles r 0.4, PINK people, BLUE movies), `.names[5]` (size 30, node colour, two
    lines, under each), `.edges[4]` (Arrows; plain Lines with `arrows=False`; 0 and 2 point right),
    `.types[4]` (DIM "ACTED_IN" size 30, 0.62 above), `.slot(i)` (point above edge i). Also
    `slide107_code()` (`Code(SLIDE107, size=30)`, centred, ~12.6 wide).
  - s3 `pill_strip(with_actors=True)` READY (scenes/ch4_s3_even.py): pills row at y = 0, `.pills[5]` (each
    `.box`, `.star`, `.count`; pitch 2.6, plain DIM style: colour the counts yourself), `.actors` (the two
    names and a dashed line 1.9 above the pills; empty with `with_actors=False`). Also `banks(walk=False)`.
  - s5 `paths_plot()` READY (scenes/ch4_s5_explode.py): no arguments; VGroup at its scene position (x ≈ −6.3..6.2,
    y ≈ −3.5..3.4, scale it down for a panel). Parts: `.axes` (y log10 0–8, x 1–8.6), `.yticks`, `.xticks`,
    `.log_label`, `.x_label`, `.gold_curve` `.gold_dots` `.gold_label` (paths), `.pink_curve` `.pink_dots`
    `.pink_label` (people), `.ceiling` `.ceiling_label` (dashed, "14,581 connected to her").
- **Needs:** ch5's opening card (above in ch5's section): ch4 s7 ends on it, built last.
- Narration: seven lines rewritten for the ear and re-voiced with `--only` (Whisper vote clean after):
  c4.even.4 "That halving is how" became "Taking half the length is how" (heard "having");
  c4.explode.1 "Star two dot dot six" / "star dot dot four" became "Star two, dot, dot, six" / "star, dot,
  dot, four" (heard "2.tack 6", "star .4"), and "{total} Five hundred and three." became "That's five
  hundred and three paths." (the first retake was heard "530"); c4.joins.2 "and you get one thousand and
  eighty-five" became "and the answer is one thousand and eighty-five" (heard "get E5"), "an edge it has
  just used" became "the edge it just used" (heard "it is just"); c4.joins.3 "no row of has position is
  used twice" became "each row of the has position table is used at most once" (heard "house position");
  c4.joins.4 "Star two dot dot six" became "Star two, dot, dot, six".
- QA flags accepted: "sequel" heard as "SQL" (c4.joins.1, c4.joins.4, c4.recap.1; COURSE.md's word);
  "Zero rows" heard "Zero rose" (c4.hook.1, homophone); "twelve and a half thousand" written 12,500
  (c4.explode.3, number format); function-word minors (c4.eight.1, c4.eight.2, c4.explode.1 "star on its").
- Ear check after the Gemini reset (`vk listen 4 --only …`): c4.even.4, c4.explode.1 (the comma-split
  "dot, dot" in both forms), c4.joins.2, c4.joins.3, c4.joins.4; also c4.eight.1/3 "Donal Gleeson" and
  c4.eight.3 "Ex-Men".
- Music: `music/ch4.json`: Zeta under the hook, Fragments under the parity walk (c4.even.2), The
  3Blue1Brown Experience from the recap's tease through the end card.

## Chapter 5 · Shortest paths, Bacon numbers, and the graph languages (ch5_shortest)
State: **ready for final** (2026-11-01 ~22:40). Preview `out/ch5_shortest_preview.mp4`, 12.3 min (739.5 s;
narration 11.6 min), decodes end to end; no in-chapter handovers (s1–s7 end empty, s8 ends on `end_card()`).
Built without Gemini (off until Wed 2026-11-04 ~00:30): Whisper vote, `vk check`, holds, frame sheets. Open for
the producer: `vk finalize 5`; after the reset, the ear check below (`vk listen 5 --only …`) and the transitions pass.
- **Opening card (for ch4's last scene, s7, to end on):** `load_scene("ch5_s1_hook").open_card()` will
  return the static VGroup of ch5's first frame, which is ch4's script's end card (c4.recap.2 {next}/{tease}):
  Jennifer Lawrence (PINK circle, left) and Daniel Radcliffe (PINK circle, right); between them a faint DIM
  tangle of chains (small alternating PINK and BLUE dots, no arrowheads) with one four-edge chain picked out
  in YELLOW; a GOLD "503" above the tangle (ch4 s5's `*2..6` reply) and a GOLD "?" over the YELLOW chain.
  Nothing else on screen, no updaters. ch5 s1 holds it, then clears to the title card on {title}.
  **Built** (2026-11-01, `scenes/ch5_s1_hook.py`, check clean): `open_card()` is a static VGroup, in order
  (centres): tangle (70 seeded chains, DIM edges stroke 2, r 0.07 BLUE/PINK dots, whole group opacity 0.2,
  x ±4.5, y −2.45…0.85); Lawrence circle r 0.7 at (−5.2, −0.7), PINK stroke 4, fill PINK 0.2 (ch1's vertex
  look), "Jennifer\nLawrence" T 34 0.2 below; Radcliffe the same at (5.2, −0.7), "Daniel\nRadcliffe"; YELLOW
  chain Lawrence → (−2.6, 1.25) → (0, 1.25) → (2.6, 1.25) → Radcliffe, stroke 5, dots r 0.11 BLUE/PINK/BLUE;
  GOLD "?" T 72 at (0, 2.15); GOLD "503" Mono 48 at (0, 3.15). Land ch4 s7's end on exactly this object
  (`self.add(load_scene("ch5_s1_hook").open_card())` or a morph that ends on it).
- **Helper for ch6:** s7 `exercise_cards()` in `scenes/ch5_s7_exercises.py`, the five cards 20.1, 20.2, 20.3,
  21, 22 ("Exercise 20.1" … in YELLOW, the question in plain text, a GOLD "?"); ch6 s1 opens with them.
  **READY** (2026-11-01, check clean), all module-level in `scenes/ch5_s7_exercises.py`:
  - `exercise_cards()`: VGroup of 5 small cards in a row, centred on ORIGIN, ~9.9 × 1.1; each `VGroup(box, num)`
    with `.box` (DIM RoundedRectangle 1.7 × 1.1, stroke 3), `.num` (DIM `T` size 48, "20.1"…"22"), `.key`.
    s7 parks the row at `ROW_SCALE` 0.6, `ROW_POS` (−3.0, −3.33).
  - `exercise_panel(key)` (key "20.1", "20.2", "20.3", "21", "22"): the hero card s7 grows each slot into, no
    hint: `VGroup(frame, title, qgrp)`, 13.2 × 6.1 centred at `PANEL_C` (0, 0.5); `.title` "Exercise <key>"
    T 44 YELLOW; `.qgrp` = (`.question` lines, `.qmark` GOLD "?" T 64). `QUESTIONS`, `QUESTION_SIZE`,
    `EXERCISE_KEYS` exported too. For ch6's row of full cards, scale `exercise_panel(k)` down side by side;
    to enlarge one, TransformFromCopy a slot's `.box` into the panel's `.frame` as s7 does.
- **Join to ch6 stays forward** (ch6 starts after ch5 and already depends on ch5 s7): ch5 s8 ends on its own
  `end_card()` (its last frame, the end card), and ch6 s1 opens on `load_scene("ch5_s8_recap").end_card()`.
  ch6's director: no opening card to design for ch5. Recorded here when s8 is built.
  **Built** (`scenes/ch5_s8_recap.py`): `end_card()` returns the static last frame, held 8 s under music
  (`.strip .copies .labels .tables .docs .graph .teaser`): `.strip` five panels (frames 1.05 × 1.26, centres
  x −2.226 … 2.226 at y 3.1); `.copies` three ch1 tangles at scale 0.26, x −5.8, y 1.2 / −0.6 / −2.4, with DIM
  T 30 `.labels` "tables", "documents", "graph" under them; `.tables` ch2 `join_diagram()` ×0.95 at (0.75, 1.0);
  `.docs` two TEAL mini documents at (−1.15, −0.8) and (2.65, −0.8); `.graph` Chaplin (−2.9, −2.6) –ACTED_IN→
  The Kid (0.3, −2.6), YELLOW, fading chain to x 6.6, "any length" YELLOW at (3.95, −3.15); `.teaser` "Next:
  recursive queries and Datalog" T 36 DIM at (0, 2.05). ch6 s1: `self.add(load_scene("ch5_s8_recap").end_card())`,
  hold, then clear to the title card on {title}. **If ch5 changes `end_card()`, re-render ch6 s1.**
- **Other exports ch6 s1 may use** ("last time" strip): `load_scene("ch5_s4_bacon").bacon_histogram(max_h=4.6,
  pitch=1.25, bar_w=0.9, value_size=28, tick_size=30, with_xlabel=True)` (GOLD bars, baseline y 0, centred x 0;
  `.bars .values .ticks .axis .xlabel`; when small use bars + axis only), `BACON_COUNTS`; ch5_s5_languages
  `CYPHER_SRC`, `GQL_SRC`, `plus_edge(size=36)`; ch5_s6_pgq `pgq_pattern(size=36)`, `pattern_picture()`.
- Music `music/ch5.json`: hook Spirals (START → c5.bfs.1), Bacon histogram stretch Clarity
  (c5.bacon.4:end → c5.bacon.6), recap Ongoing (c5.recap.1:end → END, swell after c5.recap.3).
- Rewritten for the ear (re-voiced, `vk qa 5` clean on both):
  - c5.bfs.2 "It has seen at most about four thousand people" (heard "It is seen") → "By then, it has looked
    at no more than about four thousand people."
  - c5.bacon.3 "That's the parity rule from last time" (heard "parody"; ch4 never says "parity") → "Every step
    flips the side, as we saw last time." (ch4 s3's wording)
- Accepted QA flags: "sequel" → "SQL" (c5.lang.2, c5.pgq.1, c5.pgq.4, c5.ex.4, c5.recap.1, c5.recap.3; the
  intended word, COURSE.md); c5.unwrap.4 "Coalesce" → "Colas" (jargon); c5.ex.2 "composed the" → "compose the"
  (d-th elision, same meaning).
- **Ear check after the Gemini reset** (`vk listen 5 --only …`): c5.unwrap.4 (Coalesce), c5.bacon.1 (Air-dish),
  c5.lang.1 (Sparkle, R D F, Neo four J), c5.bfs.4 and c5.bfs.5 (Donal Gleeson), c5.bacon.6 (Ex-Men), and the two
  rewritten lines c5.bfs.2, c5.bacon.3.
- Scenes: 8/8 by Opus scene-builders (batch 1 s1, s2, s5, s6, s7; batch 2 s3, s4 on s2's helpers; s8 last).
  Cross-chapter callbacks imported, not redrawn: s2 uses ch4 s5 `paths_plot()` and ch4 s4 `layered_paths()`
  (so s2's `eight_fan()` is ch4's picture, films as titled BLUE boxes); s6 uses ch1 s6 `graph_tables()`; s7's
  ex.4 hint is styled like ch2 s6 `edge_join_panel()`; s8 uses ch1 s2 `tangle()`, ch2 s1 `join_diagram()`,
  ch1 s4 `vertex()`. **If ch4 s4/s5, ch1 s2/s4/s6 or ch2 s1 change those helpers, re-render ch5 s2, s6, s8.**
- Review without Gemini: `vk check`, holds (2 rounds), and contact sheets after each scene's riskiest plays
  (frames grabbed from the 480p renders).
  Round 1 fixes: s2 (ch4's plot and fan, reply table raised), s4 (Kevin Bacon label off the rings), s6 (ch1's
  tables), s7 (ex.4 hint colours), s8 (bigger panels, readable panel 3/5, row labels, panel 2 label strip).
- Accepted check flags: s6 small text (CREATE at 26 beside the vertex graph; the two result tables at 23, side by
  side with "=" as the brief asks); s8 small text in panel 5 (20–21) and the strip (13), the brief's small recap
  panels; s8 "doesn't end empty" (its last frame is `end_card()`, ch6 s1's opening, forward join). Dwell
  advisories in every scene where the narration moves on.
- Departures accepted: s5 stacks the Cypher and GQL blocks (side by side would be size 16) and shows replies as
  "⇒ 4"; s3's query at size 26 (s2's is 30) and its table stays full size at the end; s2's fan film titles come
  from ch4's picture; s4's grouping key is a GREEN box, not a brace.
- Glitches (confirmed on frames, all three fixed in round 2 and re-checked on frames: s2 clears the code in its
  own 0.9 s play before the fan's 1.4 s fade-in; s4 swaps whole tokens (`swap_tokens`) and flies shrinking ring
  outlines to the bars with a FlashAround per bar; s4's "62" FlashAround box is an accepted check advisory):
  - s2 ~106.4 s (c5.bfs.5 {same}): the allShortestPaths code fading out while ch4's fan fades in at the same
    place, code text and film titles overlapping ~0.4 s. Cause: FadeOut(code) and FadeIn(fan) in one play.
  - s4 ~108.9–109.3 s (c5.bacon.5 {ripples}): pink translucent blobs and pills over the histogram. Cause:
    TransformFromCopy of a ring of dots onto a GOLD bar.
  - s4 ~31.9 s (c5.bacon.2 {kevin}): the name string morphs letter by letter (`' enn      '`). Cause: a
    per-character transform between unlike strings.

## Chapter 6 · Solutions to the exercises (ch6_solutions)
State: **READY FOR FINAL** (2026-11-01 ~23:20). Preview `out/ch6_solutions_preview.mp4`, 10.8 min (647.1 s; 10.2 min
of narration), plays end to end; 7/7 scenes built, all joins are fades to empty (no in-chapter handovers). Built
without Gemini (off until Wed 2026-11-04 ~00:30): Whisper vote, `vk check`, two holds rounds, and `--frames` sheets
after the riskiest plays of s2–s7 (query swaps, in-place rewrites, the list cross-over, recap docking). All clean, no
glitches confirmed. Scene lengths: s1 38.6, s2 91.5, s3 87.3, s4 95.3, s5 133.8, s6 150.0, s7 50.6 s.
- Uses ch5 s7's `exercise_cards()` / `exercise_panel(key)` (READY) and opens s1 on `load_scene("ch5_s8_recap").end_card()`.
- Music `music/ch6.json`: hook Reflections (START → c6.chaplin.1), Wachowski grids Fractals
  (c6.wachowski.2:end → c6.wachowski.4), recap Serendipity (c6.recap.1:end → END, swell after c6.recap.2).
- Rewritten for the ear (re-voiced 2026-11-01, `vk qa 6` clean on all three except "sequel"):
  - c6.wachowski.4 "The fix is return distinct" (heard "returned distinct") → "The fix is to add distinct to the return".
  - c6.sql.5 "Group by names, and…" / "Group by person IDs as well…, and they split again" (heard "Grouped by" /
    "Root by") → "If we group by names, …" / "If we group by person IDs as well, in either language, they split
    again."; "three join conditions" (heard "joint conditions") → "three conditions to join on".
  - c6.genres.5 "A movie's genres come with the movie" (heard "A movie genre has come with") → "Each movie carries
    its own genres".
- Accepted QA flags: "sequel" → "SQL" (c6.sql.1, c6.sql.2, c6.sql.5, c6.recap.1, c6.recap.2; the intended word,
  COURSE.md); c6.composers.1 "composed the" → "compose the" and c6.sql.1 "appeared together" → "appear together"
  (d-elision, same meaning); c6.composers.4 "nineteen oh three" → "1903" and c6.genres.2 "hundred and seventy-four"
  → "174" (number format); c6.genres.2 "the movie's genres" → "the movie genres" (possessive, same meaning).
- Shared looks: s2–s6 open on `exercise_cards()` ×1.2 at ORIGIN, grow the slot into `exercise_panel(key)`, show
  s1's `pause_icon()` on {stop}, then dock the title as a corner tag `to_corner(UL, buff=0.5)`. s4 exports
  `edge_grid(row_types, col_types, …)` (s5's {nine} 3 × 3 uses it). s2–s6 export a static `recap_tile()` that s7
  imports: **if one of them changes, re-render s7.** s1 depends on ch5 s8's `end_card()` (re-render s1 if ch5 changes it).
- Review fixes (one round): s1 banner inset to 13 wide (it ran into the frame edges); s2 {inside} now shows all five
  films' Chaplin rows (real cypher-shell rows), not two; s4 tag margin 0.3 → 0.5 and shared pause icon; s5 GROUP BY
  kept YELLOW to the end of c6.sql.2; s6 labels raised to ≥ 26, both rename queries shown together, The Kid's
  has_genre card has all three rows (5, 8, 11, checked in DuckDB), bottom rows lifted. Checked: s5's self-join row
  nm0000168 / tt0110912 (Samuel L. Jackson, Pulp Fiction, actor) is real.
- Accepted check flags: dwell advisories throughout (card-row slots fade after 0.4 s by design; Wachowski grids and
  s6 rows move at the voice's pace); s6 {copy} scratch-copy block at size 22 (the brief asks for it small and dimmed);
  s7 small text: the docked recap strip is icons at size 6–10, each with a readable label under it, and the big
  Wachowski tile reads at 22–25 and the Genre circle names at 24 (s7 rendered with `--render-anyway`). s6 renders with
  `--render-anyway` only for the {copy} block.
- Departures the builders took (accepted): long Cypher lines re-wrapped at the same tokens (s2 comma form, s4 MATCH);
  s4's 28-row reply in two columns of 14; s5 stacks Cypher over SQL (size floor) and its compare beat shows the
  pattern lines against SQL FROM…GROUP BY; s6 plays its queries one at a time in a full-width band under the split;
  s7 shows each tile big on its sentence, then docks it into a top strip rather than five small tiles throughout.
- **Ear check after the Gemini reset** (`vk listen 6 --only …`): the three rewritten lines c6.wachowski.4, c6.sql.5,
  c6.genres.5; c6.sql.3 ("Duck D B"); c6.sql.4 ("Samuel ell Jackson"); c6.wachowski.4 ("Vee for Vendetta");
  c6.genres.4 ("Food, Inc."); c6.composers.2 ("count star"); c6.recap.2 ("Datalog").

- 2026-11-04 Gemini pass (checks only, nothing fixed): ear checks ch1-6 ran (--only lists from this file). Real (+Whisper): c5.unwrap.4 'Coalesce' heard 'Coless', c6.recap.2:3 'Datalog' heard 'to tall og'. Gemini-only claims elsewhere (spoken 'and' dropped in numbers, 'Donal', c4.joins.3 'paths'->'pass', c5.bfs.2 'shortest', c3.count.5 names, c3.predict.2 'times'); see media/review/ch*_listen_partial.md.
- 2026-11-04 re-voice fix pass (the two real mishearings from the Gemini pass): c5.unwrap.4:4 "Coalesce returns" → "The function coalesce returns" (24.4 → 25.2 s); c6.recap.2:3 "Datalog" → "Data-log" (9.9 → 10.3 s). Rewrites pre-tested on the voice's own seeds with Whisper ×3; voiced with the old fixed pacing (project.json "pacing": "fixed" only during `vk voice`, then restored). `vk listen --only`: Coalesce and Datalog now heard right. Gemini-only, accepted (Whisper heard the word; its one flag is the accepted "sequel"): c5.unwrap.4:4 "null" → "nah", c6.recap.2:3 "length" → "wength". `vk check --no-render`: no overruns. `vk finalize 5 6`: clean (ch5 12:21.9, ch6 10:48.7). The 2026-11-04 listen reports are kept as media/review/ch{5,6}_listen_partial_2026-11-04.*.
