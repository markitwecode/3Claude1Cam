# Sorting: status

2026-10-27: project created; planning.

## Producer notes (2026-10-27)
- Scope: plan covers all 7 chapters; only ch1–2 commissioned.
- Shared studio with `studio-tour` (another session): first come, first served, with a message at every handoff. One `vk voice` and two chapter-directors at a time across the whole studio. Voice and directors were held until studio-tour's engine changes finished (its "engine done" message); ch1+ch2 directors start after "studio-tour directors done" unless l05 is ready first.
- Timing requested by the user: per-stage wall times, excluding waits on studio-tour, to be recorded here at the end.

## Chapter 1 · How fast can we sort? (ch1_how_fast)
State: DONE (2026-10-28). Video `out/ch1_how_fast.mp4`, 1920×1080 at 60 fps, 11.0 min (660.1 s; 10.4 min of narration).
- Narration: 32/32 lines voiced. Two QA lines were rewritten and re-voiced: c1.hook.2 ("Each sort we'll race in this lecture" became "Every sort in this lecture") and c1.contest.2 ("And a count of comparisons" became "And the number of comparisons"). Both now pass QA.
- QA flags accepted: c1.nlogn.3, c1.nlogn.4 (×3) (numbers heard as digits, spelling only); c1.test.2 ("Start it at" heard as "Started at", same meaning).
- Check by ear: c1.hook.2 and c1.contest.2 (the rewritten lines); the "N" readings ("big O of N", "N log N", "N factorial"), per the producer.
- Music: `music/ch1.json`. Transformation under the hook, Heartbeat under the binary-search walk (c1.bin.2), Endpoint under the recap and end card.
- Scenes: all 8 built, plus one fix pass on s4. The scoreboard lives in `scenes/ch1_s4_contest.py`. `make_scoreboard()` gives the all-"?" board with a dashed floor; `make_scoreboard(bound="118,458")` gives the state ch1 ends in (solid GOLD floor, "lower bound ≈ 118,458"), for ch2–ch6 to import.
- Check flags accepted: dwell only, on pass-through visuals the narration moves past (title card, L4 thumbnails, quick yes/no answers in the hook, DIM tags that get replaced, the 0.6 s carry-over at the start of s6). One small-text flag in s7: the verbatim 10,000-number printout needs size 20 to fit its 77-character lines, and the brief calls it a scrolling glimpse that isn't read aloud.
- Brief departures accepted: the running chain uses ConsChain defaults (FG values, as in L4 and the ch2 script), not the brief's GOLD values. s6 shows the bars flying into a total rather than stacking. The recap's small scoreboard and printout icons are drawn as coloured bars.
- Open: the ch1 end card (cards 3 5 9 in hand, 4 and 7 loose; spec in the s8 docstring) should match ch2 s1's opening shot. The spec was sent to the producer for ch2's director; not yet confirmed that they match.

## Chapter 2 · Insertion sort (ch2_insertion)
State: DONE (2026-10-28). Video `out/ch2_insertion.mp4`, 1920×1080 at 60 fps, 10.6 min (638.5 s; 10.1 min of narration).
- Narration: 31/31 lines voiced. Three QA lines were rewritten and re-voiced with `--only`: c2.insort.2 ("like the one-pluses in N-length" became "like the one-pluses in lecture three's length function"; it was heard as "end length"), c2.cost.4 ("N squared over four predicts…" became "The formula, N squared over four, predicts…"; all three models heard "In squared"), c2.why.4 ("In-sort sorts the tail" became "In-sort first sorts the tail"; it was heard as "Inns/INS/IN sorts"). All three now pass consensus QA.
- QA flags accepted (spelling only, numbers heard as digits): c2.cost.3:1, c2.cost.4:6, c2.cost.5:2, c2.why.2:2. A base-only hallucination on c2.cost.4 (extra words after the last sentence) is not confirmed by small or medium.
- Check by ear: c2.insort.2, c2.cost.4, c2.why.4 (the rewritten lines); every "N" reading ("N squared", "N-sum-sum", "Tee of N", "N minus one"), per the producer.
- Music: `music/ch2.json`. Euler's Clock under the hook, One, Two, Zeta under the insort collapse (c2.insort.3), Ongoing from the recap through the end card.
- Scenes: all 7 built; one fix pass on s1, s5 and s7. s1, s5 and s7 import `make_scoreboard(bound="118,458")` unchanged. s1's cards follow ch1's s8 spec (1.6×2.24, fan pivot 6.5 below, 10°, hand x −2.15, y −0.4, loose 4 and 7 at x 1.57 and 3.47), so ch1's end card matches ch2's opening: ch1's open item above is settled. s2 exports `ins_code()` (every `ins` YELLOW), which s4 and s7 reuse. s6 exports `range_scale()`, which s7's recap reuses.
- Check flags accepted: small text only where the brief asks for miniatures (s1's corner scoreboard, s4's top-left `ins` reference, s7's recap icons and the end-card board at about 0.69). Dwell: the unfold and collapse steps in s4, which are replaced as the voice moves on; the title card (only 3.9 s before {last}); replies held through a scene's final fade; transient pieces of transforms.
- Brief departures accepted: s5's laptop aside is one line, and "OCaml 5.4.1, Apple M1 Max" is in the docstring only. s7 shows `merge (xs, ys)` born beneath `ins x ys` rather than replacing it. The end card is "Next: quicksort" with the board and the split chain. s2 adds a trace line `⇒ 4 :: 9 :: [3]` to the warning example. s6's slide motion was written before s1's existed: an item turns GREEN once it's in the sorted part, and the item and its neighbour swap as it passes.
- Open: nothing.

## Timing, ch1–2 run (producer, 2026-10-27/28)
Wall clock 21:49 → 00:14 = 144 min, of which 36.6 min was waiting on studio-tour's engine changes. Active: ~107 min.

| Stage | Wall time | Context read |
|---|---|---|
| Plan (whole lecture, 7 ch) | 14.1 min | 3.3M (incl. continuity review) |
| Scripts ch1+ch2, in parallel | 9.0 min | 5.1M |
| Continuity review | 3.2 min | (in planner) |
| `vk voice`, 20.4 min of narration, new consensus QA | 43.6 min | 0 |
| Directors ch1+ch2 in parallel (QA re-voices → 15 builders → review/fix → final) | 36.1 min | 28.4M (directors 6.4M, builders 22.0M) |
| Producer (main session) | — | 5.4M |

- Per chapter: ~14M context each, ~36 min wall time when two run in parallel, under the runbook's 16–30M and 40–60 min. Inside the directors: QA re-voices 2–6 min, building ~22 min, review, fixes and final render ~8 min.
- Voice was the bottleneck: 2.1 s of wall time per second of audio, against the runbook's ~0.4. Cause: the new 3-model consensus QA with retries (studio-tour session is tightening it).
- Session total: 42.1M context read (`vk usage`).
- (2026-10-28) The voice QA fix has landed (studio-tour session): numbers are normalised, identifiers agree when 2 models hear the same thing, and consensus-only retakes are capped at 1. Expect ~1.26× the old voice time, not the ~6× of this run. To do when the voice slot is free: `vk voice 1 --qa-only` and `vk voice 2 --qa-only` to clear stale flags (the audio is unchanged).

## Producer notes (2026-10-30): ch3–7 scripted, parked before voice
- ch3–7 scripts written (Opus writers) and continuity-reviewed by the planner: ch3 8.9 min, ch4 10.3, ch5 10.3, ch6 8.1, ch7 9.3 (~47 min). ch1–2 untouched. Parked at the user's request (they wanted DE next); nothing voiced.
- Resume: `vk voice` (ch3–7), then directors in pairs. Builders are Opus scene-builders now (Codex only at a usage limit).
- Build order matters: the briefs ask ch3 s6 to export `call_tree()`, ch4 s2/s3 `recursion_tree()`/`worst_tree()`, ch6 s4/s5 `card_5_1()`…`card_5_4()`. So ch3 before ch4, ch4 before ch5 and ch6, ch6 before ch7. Director order: 3, then 4, then 5 + 6 as a pair, then 7.
- Listen at voicing: c4.quik.2 "Q, U, I, K" (the spoken name is "quick with accumulator" from there on).
- Stale note above: ch2 s2's `ins_code()` doesn't exist; the code is `ocode(INS_SRC)` in `scenes/ch2_s2_ins.py`.

## Build plan (producer, 2026-11-01 18:15): ch3–7 without Gemini
Voiced 2026-11-01 (ch3–7, 47.3 min new; lecture total 67.8 min). The user chose to build now with
Gemini off (its weekly quota ran out; engine/logs/gemini-off until Wed 2026-11-04 ~00:30), using
chapter-director.md "When Gemini is off". All five directors in parallel:
- Joins: ch3 s1 opens on ch2's end card (ch2 is final). For ch4–7 each director designs its own
  opening card first and records it here; the previous chapter's s8 ends on exactly that card.
- Helpers, recorded here early by their owners, used by the dependent scenes built last:
  ch3 s6 `call_tree()` (for ch4); ch4 s2/s3 `recursion_tree()` / `worst_tree()` (for ch5 and ch6);
  ch6 s4/s5 `card_5_1()`…`card_5_4()` (for ch7).
- After the Gemini reset: `vk review N --transitions` on ch3–7 (and nst-maths L10 ch8, L11 ch4–6,
  whose final reviews were skipped), then fix-pass directors only for real findings.
  Also `vk listen 4 --only` on c4.quik.2 ("Q, U, I, K") and ch4's six rewritten lines (c4.avg.4,
  c4.quik.2–4, c4.order.1, c4.speed.1): nothing has heard them yet. Other chapters add theirs below.
  ch3: the "ay", "bees", "ell", "ar" readings and the rewritten c3.hoare.2, c3.recap.2, c3.idea.1.
  ch6: in the transitions pass, look at s5's 9/4 swap (the two middle boxes empty at the midpoint,
  the 9 dipping below the row; seen on a builder's frame sheet, unconfirmed); ear: c6.recap.1.

## Chapter 7 · Bonus: solutions to the exercises (ch7_solutions)
State: READY FOR FINAL (2026-11-01 19:30). Preview `out/ch7_solutions_preview.mp4`, 10.3 min (617.9 s;
9.6 min of narration), plays end to end. No handovers inside ch7 (every scene ends empty; s6 ends the
lecture). The join ch6 → ch7: ch6 s6 ends on `load_scene("ch7_s1_intro").open_card()`, check it at finalize.
- Scenes: all 6 built by Opus scene-builders (s1, s3 from 18:48; s2, s4, s5 from 19:00; recap 19:10), one
  fix round on s3, s4, s5, s6. Every OCaml reply and comparison count was re-run in OCaml 5.4.1. Exports:
  s1 `open_card()`, `test_chains()`; s2 `selsort_board()`, `staircase()`, `three_chains()`; s3
  `select_code()`, `dups_reply()`; s4 `bubble_board(ratios=False)`, `pass_rows()`; s5 `rule_pair()`,
  `bpass_code()`, `bubble_code()`.
- Gemini was off: no `vk listen`, no `vk review`. Motion was checked on `--frames` sheets instead: s1's
  opening card to title and header to card row, and s2's quick selection rounds (both read by me, clean),
  plus s3–s6's riskiest plays (read by their builders: three glitches found and fixed, below).
- Glitches (found on frames, all fixed):
  - s3 c7.selcode.6 ~125.5 s, the reply swap after {again}: the old reply drifted up into the input line
    above it (`swap`'s upward drift, with lines too close together), and the ✓ landed on the longer new
    reply. Fixed with `swap(shift=None)`, the ✓ moved right of the reply, and the RED ghost cells faded first.
  - s4 c7.bubcost.2 ~21.2 s and c7.bubcost.4 ~70.6 s: each new pass row's copy (`fly`, standing in for
    TransformFromCopy) was drawn half over its source row at +0.5 s. Fixed: the new row fades in while
    dropping 0.3 into its slot.
  - s5 c7.bubcode.5 {equal} ~101.5 s: the equal tiles sat on the code line `in (x::zs, s)`, and the 3s,
    moving without their boxes, cut through the box edges and the bracket. Fixed: the tiles moved to the
    empty right side and swap whole on a half-circle. Also {never} ~111.8 s: 0.7π arcs pushed the digits
    into the `;` between them; fixed with half-circle arcs.
- Check flags accepted:
  - Dwell advisories:
    - the four-card row each solution card grows from (held about 1 s by design);
    - s1's inherited opening card, cleared on {title} as the reversed join requires;
    - replies and pair slots replaced as the voice moves on;
    - s4's time column at 3.9 s, shortened by the 2 s board arrival;
    - the recap's r3/r4 lines, cleared by {board}.
  - Small text, s6 only:
    - the miniature recap tiles (18–24), as the brief asks;
    - the board at ×0.85 (24–26), to fit the O-tag column;
    - the dimmed board behind the end card (19–22).
- Brief departures accepted:
  - s1: the {cards} row has no "Solutions" note; the "tempting bugs" card takes the steps' place at the
    left, because the row fills the width.
  - s2: the board isn't scaled down (its headers would drop under 25); the closed form is written
    `T(n) = n(n−1)/2`; DIM "running"/"result" labels added; the 3/2/1 rounds run quickly to fit the voice.
  - s3: the pitfall blocks are stacked vertically and `select` fades rather than dimming aside; the fix
    uses `edit` (style 2 bans the morph); `val select` is on two lines.
  - s4: it builds its own selection row (same values and colours as s2's); the time column fades on
    {double} to make room for the arcs; pass rows fade and drop rather than TransformFromCopy; "passes:
    10,000" stays as a note at the board's top left.
  - s5: `edit` for the slip; ch6's braces sit under a separate large `x::y::ys`; the slip's pass rows are
    reply lines, not chains.
  - s6: r2's `select` is re-wrapped over 6 lines (the same code) so it's legible; r3 shows only the
    reversed rows.
- Open:
  - The × 2 arrowhead nearly touches selection sort's "49,995,000" on `bubble_board` (s4's end, the recap).
    Minor, left alone.
  - After the Gemini reset, the producer's transitions pass is the only Gemini check this chapter gets.
- **Opening card (for ch6's last scene, s6, to end on):** `load_scene("ch7_s1_intro").open_card()` returns
  the static VGroup of ch7's first frame, which is ch6's script's end card (ch6 s6 {bonus}/{bye}): the
  four exercise cards 5.1–5.4 in one row exactly as ch6 s4 draws its row (kit and `EX_TITLES` from
  `scenes/ch6_s4_hints1.py`), with the note "Solutions: bonus chapter" ("bonus chapter" YELLOW) under
  them, nothing else on screen, no updaters. ch7 s1 holds it, then clears to the title card on {title}.
  **Built** (2026-11-01 18:51, scenes/ch7_s1_intro.py, check clean): `open_card()` is ch6 s4's
  `four_cards()` unchanged (four BigCards 3.1 × 2.0, radius 0.2, DIM 2.5 stroke, fill #161A21, number
  T 44 at centre + 0.48, name two lines T 28 DIM at centre − 0.38; spacing 0.2, row centred (0, 0.2),
  x −6.5..6.5) plus the note "Solutions: bonus chapter", T 34 DIM, "bonus chapter" YELLOW, at (0, −2.1).
  Parts: `.cards`, `.note`. ch6 s6: end on `load_scene("ch7_s1_intro").open_card()`, held still.
- Uses: ch6 s4/s5 `card_5_1()`…`card_5_4()` + kit + hint visuals (s1–s5); ch6 s2's three-column board
  (s2, s4, s6); ch6 s6's next-lecture pictures (s6); ch3 s6 `call_tree()` (s3); ch1 s4 `make_scoreboard`,
  ch1 s7's rs caption, ch2 s5's table and staircase.
- Narration: QA rewrites, re-voiced, QA now clean (0 consensus flags): c7.selcode.2 "It carries em, the
  smallest so far" became "It carries two values along. Em is the smallest so far" (heard "carries
  them"); c7.bubcode.3 "Carrying ex on" became "Carrying ex forward" (heard "Exxon"); c7.recap.1
  "returns the smallest item and the rest as a pair" became "returns a pair, the smallest item and the
  rest" (heard "rest is a pair").
- COURSE.md letter rule (producer, 2026-11-01): ch7 has no "ay", "ell", "gee" or "aitch". Its spelled
  letters are "em" (c7.selcode.2), "ex"/"why" (c7.bubcode.2, .3, .6) and "tee" (c7.selcost.4), each
  said after a role noun ("the next item, ex", "the smallest so far"). All three Whisper models hear
  every one of them right, with no flag at all, base-only included. Not rewritten, since s3 is
  built and s5 is building on these timings.
- Music: `music/ch7.json`. Serendipity under the hook, Machinery under bubble sort's three passes
  (c7.bubcost.1:end → c7.bubcost.4), The 3Blue1Brown Experience from the recap's board through the end card.

## Chapter 6 · Which sort? And exercises (ch6_summary_exercises)
State: **ready for final** (2026-11-01 ~19:20). Preview `out/ch6_summary_exercises_preview.mp4`, 8:54
(533.8 s), decodes end to end; `vk preview 6`: handover ok s1 → s2 (0.00%). Built without Gemini.
- **Opening card (for ch5's last scene to end on):** `load_scene("ch6_s1_hook").open_card()`, ch5's
  script's end card (c5.bottom.4): title "Next: which sort is best?" laid out like ch5's own
  `open_card()` ("Next: merge sort", ch2 s7's end-card layout); the scoreboard
  `make_scoreboard(bound="118,458")`, all six cells filled (insertion sort "25,146,194" / "174 s",
  quicksort "158,058" / "0.53 s", merge sort "120,392" / "1.4 s"), floor solid GOLD; beneath it ten
  DIM buckets 0–9 with 53, 19, 51 resting in buckets 3, 9, 1 (s3's radix picture, static), GOLD tag
  "no comparisons". Static, no updaters. ch6 s1 holds it 0.7 s, then clears to the title card.
  **Built** (2026-11-01, scenes/ch6_s1_hook.py; uses only lib and ch1_s4's `make_scoreboard`/`SB_TALLY`):
  `.title` `T("Next: which sort is best?", 52)` ("which sort is best?" YELLOW) at (0, 3.3); `.board` =
  `filled_board()` ×0.74 (x ±4.59, y −2.05..2.60, six GOLD T 44 cells); `.buckets` `bucket_row(color=DIM)`
  ×0.75 (x −6.20..2.65, y −3.60..−2.52); `.tiles` `num_tile` 53, 19, 51 ×0.75 in buckets 3, 9, 1;
  `.tag` `T("no comparisons", 34, GOLD)` right of the buckets. **If ch6 changes it, re-render ch5's last scene.**
  Also exported: `bucket_row()`, `num_tile()`, `place_tile()`, `filled_board()`, `fit_board()`, and
  `handover_shot()` (s1 → s2: the board ×0.878 centred, YELLOW "Which sort is best?", two DIM tags).
- `card_5_1()`/`card_5_2()` (scenes/ch6_s4_hints1.py, with the kit and `EX_TITLES`) and
  `card_5_3()`/`card_5_4()` (scenes/ch6_s5_hints2.py), for ch7. **s4 READY** (2026-11-01): importing
  `scenes/ch6_s4_hints1.py` only defines things; everything is in its `__all__`. Kit: `make_strip(states)`,
  `Pill(i, state)`, `restyled`, `TODO CURRENT DONE`, `BigCard(i)`, `four_cards()` (`.cards .note`: the
  overview row and "Solutions: bonus chapter"), `HeroCard(i, height, step, lifted)` (`.row_y .at_row
  .lower .lift .tag .keep .whole()`), `Slot(type_src, ...)`, `Tag(text, color)`, `enter_card(strip, card,
  extra, light)` / `exit_card(...)`, `hint_label`, `pause_tag()`, `pause_icon`, `hold_for`, `finish`,
  `mini_chain`, `tiles`, `l2_table`, `glyph`; text `EX_NUMS EX_TITLES EX_CARD_LINES EX_TASKS RUNNING
  EX51_LINES EX52_*`, `UNZIP_SRC`, `L2_ROWS`. `card_5_1()` (`.rows .chain .res_lbl .lift_by .tail
  .tail_q .brace .brace_lbl`), `card_5_2()` (`.task .name .slot .tests .rep`); `card.whole()` is the
  card as stated (3 not lifted, no YELLOW). **s5 READY** (2026-11-01, scenes/ch6_s5_hints2.py, kit
  imported read-only from s4): `card_5_3()` (chain example), `card_5_4()` (task + answer slot only; the
  test belongs to the hint), each self-contained with `.whole()`; also `bracket_over()`, `EX53_LINES`, `EX54_*`.
- **`board3(stage="full", with_optimal=True)`** (scenes/ch6_s2_summary.py, for ch7 s2/s4/s6): READY. The
  three-column board in frame coordinates (x −6.5..6.6, y 3.0..−2.9), submobjects in `filled_board()`'s
  order (a two-column board can Transform into `stage="two"`; `"ask"` has GOLD "?" in column 3). Row labels
  YELLOW T 30 at x −6.5, rows y 0.8/−0.4/−1.6; columns centred x −2.0/1.55/4.9; headers T 28 two lines
  (y 2.85, 2.46); rule y 1.62; cells GOLD T 40, column 3 GREEN "9,999" / RED "49,995,000" / GREEN "64,608";
  floor GOLD T 30 at y −2.75 with GOLD T 28 "O(n log n) is optimal". Attributes `.rule .row_labels
  .col_headers .tally_tag .cells[r][c] .floor_line .floor_label .floor_value .col3_header .col3_cells .optimal`.
- **Next-lecture pictures** (scenes/ch6_s6_recap.py, for ch7's recap): READY, all centred on ORIGIN.
  `vehicle_reply(size=30)` (Mono; `type` BLUE, constructors YELLOW), `exception_shot(size=30)`
  (`VGroup(code, coin)`, `.code .coin`), `tree_reply(size=30)` (Mono ~11.9 wide; `'a` PINK, `type`/`of`
  BLUE, `Lf`/`Br` YELLOW), `binary_tree(radius=0.3, dx=0.9, dy=0.8, size=30)` (`VGroup(edges, *nodes)`,
  `.nodes` dict value → node, `.edges`), `halving_bracket(op=0.45, side=0.26)` (`.boxes .spans`),
  `coin(v=20, r=0.42)` (L4 ch4's coin spec, redrawn). s6 ends exactly on ch7's `open_card()` (no mark).
- Uses: ch4 `recursion_tree()` (s1, s2, s6), `worst_tree()` (s6); ch5 s2's zipper and s4's take/drop
  split (s1, s6); ch3 `call_tree()` (s6); s6 ends on ch7's opening card (built last).
- Narration: c6.recap.1 "so sorting N items needs" became "so a list of length N needs … comparisons
  to sort" (Whisper heard "sorting in items"); re-voiced, QA clean (0 flags). COURSE.md's letters rule
  (producer, 2026-11-01): ch6 has no "ay"/"ell"/"gee"/"aitch"; its only spelled letters, c6.ex.7's
  "ex cons why cons whys", are heard right by Whisper base, small and medium (`vk qa 6 --all`). No change.
- Music: `music/ch6.json`. Focal Point under the hook, Gnomon under radix sort's two passes
  (c6.radix.1:end → c6.radix.4), Reflections from the recap through the end card.
- Scenes: all 6 built by Opus scene-builders. Order: s1 in two phases (phase 1 = `open_card()`, the
  bucket/tile helpers and `handover_shot()`, so ch5 and s3 could start; phase 2 = the merge-sort beats
  once ch4/ch5 were in), s4 → s5, s3, s2, then s6. One fix round from the holds: s4 (5.1's hint keeps
  its three chains, counters, `T(n) = ?` and the table up through the pause) and s6 (Part 4's text
  inside its tile, Part 3's tree and Part 1's icon enlarged, Part 6's board fills its tile at {best}).
- Joins: s1 → s2 is a handover (`handover_shot()`). s6 ends exactly on `load_scene("ch7_s1_intro").open_card()`
  (reversed join, no mark): `vk check`'s "end: 110 visible pieces" on s6 is by design. **If ch7 changes
  its `open_card()`, re-render ch6 s6; if ch6 changes `open_card()`, re-render ch5's last scene.**
- Accepted check flags (advice only): dwell on fast beats where the narration moves on (s1's open card
  0.7 s, title ~2 s, take/drop labels, "nearly 3 times as fast", the verdict line; s2's inherited
  question/tags, the third row note, the first "?", the reprised question; s3 "n × log n again" and the
  two card outlines; s4 "Solutions: bonus chapter" 4.3 s, "smallest so far" 3.5 s; s5 "again, until a
  pass swaps nothing" 5.8 of 6.3 s; s6 "for small integers" ~1.2 s, next-lecture items). Small text in
  s6's miniature tiles (trees, buckets, the Part 6 board thumbnail), as the brief's miniatures demand.
- Departures the builders made, accepted: s2's board slides off on "N squared" (not at {catastrophic})
  and is rebuilt at fixed sizes for the third column; s3's buckets are taller (two tiles stack); s4's
  three small chains are stacked, not side by side; s6's halving bracket and L4 coin are redrawn, not
  imported.
- Glitches: none confirmed. Gemini off, so motion was checked on each builder's `--frames` sheet after
  its riskiest plays. The builders caught and fixed, before review: s4 a faded arrow out of the 3
  coming back during 5.1's lift; s1 a leftover 7→[] arrow during the split and a GREEN dot before the
  tick; s6 the four cards fading in over the leaving tree reply. Unconfirmed: s5's 9/4 swap leaves the
  two middle boxes empty at its midpoint, with the 9 dipping just below the row (the builder's own note).
- Open: Gemini listen/review not run (quota). Producer's transitions pass after the reset.

## Chapter 4 · How good is quicksort? (ch4_quick_cost)
State: READY FOR FINAL (2026-11-01 ~19:05). Preview `out/ch4_quick_cost_preview.mp4`, 11.0 min (659.9 s; 10.3 min of narration), plays end to end; no in-chapter handovers (every scene ends empty). Open for the producer: `vk finalize 4`; after the Gemini reset, the transitions pass, and an ear check of c4.quik.2 ("Q, U, I, K") and the six rewritten lines below.
- **Opening card (for ch3's last scene, s7, to end on):** `load_scene("ch4_s1_hook").open_card()` returns
  the static VGroup of ch4's first frame, ch3's script's end card: title "Next: how good is quicksort?"
  (laid out like ch2 s7's "Next: quicksort" end card); the scoreboard `make_scoreboard(bound="118,458")`,
  small, insertion sort "25,146,194" / "174 s", quicksort "158,058" / "0.74 s" with its row lit YELLOW,
  merge sort's "?" cells GOLD (static: ch3 may pulse them before the end); beside it ch3 s6's pivot tree
  (`call_tree()` circle form: 3 on top, 7 below-right, 5 and 9 under 7, 4 under 5, pivots YELLOW) with
  the root's empty left branch RED and a YELLOW "?" over the root (no "0"/"4" labels); a small DIM
  `(quick l) @ (a :: quick r)`, its `@` GOLD, struck through. ch4 s1 holds it, then clears to the
  title card. Built in `scenes/ch4_s1_hook.py`.
- `recursion_tree()` (scenes/ch4_s2_average.py, for ch5 s6 and ch6): READY. `load_scene("ch4_s2_average").recursion_tree(labels=("n", "n/2", "n/4", "1"), sums=("n", r"2 \times n/2 = n", r"4 \times n/4 = n"), levels_label=r"\log_2 n", width=6.0, leaves=16, pitch=1.0, box_h=0.65, color=BLUE, with_sums=False, with_bracket=False)` → VGroup of the rows + ⋮, rows centred on ORIGIN (3.5·pitch tall, `width` wide; every row the same width). Labels are MathTex strings (ch5 s6: `("10{,}000", "5{,}000", "2{,}500", "1")`). Parts (always built and positioned; in the group only with the flags): `.rows` (4 VGroups: root, level 1, level 2, leaves; each node `VGroup(rect, label)` with `.rect` `.label`), `.rects[r][j]`, `.labels[r][j]`, `.dots` (⋮), `.sums` (3 GOLD MathTex left-aligned 0.5 right of the rows; `.sums[i][-1]` is the final "n"), `.bracket` (GOLD Brace down the left side + label; `.bracket.brace`, `.bracket.label` = VGroup(MathTex levels_label, T "levels")). Scaled to 0.5 its labels drop below 28: fine for a small recap.
- `worst_tree()` (scenes/ch4_s3_worst.py, for ch5 s1/s6 and ch6 s6): READY. `load_scene("ch4_s3_worst").worst_tree(form="lists"|"circles", **call_tree_kwargs)` → ch3's CallTree for [3; 4; 5; 7; 9] (max_depth=4: leaf [5] not expanded; total 10); place with `.place(scale, point)` (point = layout origin: root row, rank centre). lists: pivots YELLOW, GOLD badges 4/3/2/1/0, empty calls RED "[]". circles: zigzag 3, 9, 4, 7, 5, ch3's BLUE rings with YELLOW digits, one bold RED stub (stroke 5) toward each empty side (`node.stubs`). s3 draws circles with `size=36, radius=0.45, pitch=1.5, gap=1.25`. Also `sorted_chain(scale=0.7)` (.chain .label GREEN "sorted") and `shuffled_chain(scale=0.7)` (.chain 3→5→9→4→7, .label, .count GOLD "8 comparisons", .note GREEN "random order, like rs: 158,058") for the recap.
- Uses: ch3 `call_tree()` (s1, s2, s3, s5); ch5's opening card (s7, built last).
- Narration: six lines rewritten for the ear and re-voiced with `--only`: c4.avg.4 ("Each level halves the size of the parts" became "At each level, the parts are half as big"; heard "haves"/"has"); c4.quik.2 ("cons it onto sorted" became "cons it on the front of sorted"; heard "undistorted"); c4.quik.3 ("Items at most ay go onto ell" became "Items no bigger than the pivot go onto ell"; "ay" heard "a e"); c4.quik.4 ("ay is consed onto that" became "the pivot is consed onto that"; "ay" heard "I"/"IE"); c4.order.1 ("The call that sorts ell comes last" became "The call that sorts ell, the left part, comes last"; heard "sorts that"); c4.speed.1 ("plain quick's appends copy" became "the appends in plain quick copy"; heard "depends"/"of pens").
- QA flags accepted (spelling only): "bees" heard "b's" (c4.quik.3), "ar" heard "are" (c4.quik.4), "accumulator" spelt oddly by medium (c4.order.1). c4.quik.2's "Q, U, I, K" passes QA; with Gemini off it has had no ear check.
- Music: `music/ch4.json`. Fives under the hook, Spirals under the recursion tree's growth (c4.avg.3), Quantum Blue from the recap through the end card.
- Scenes: all 7 built (Opus builders), Gemini off, so the review was `vk check` and two holds rounds. One fix round: s1 (the hook's last frame: the tree is centred under the questions, not low-left), s3 (a one-frame pop, see Glitches), s4 (GREEN "no @" held ~10 s beside the shrunk code, was 1.3 s), s5 (c4.order.3's call band no longer lingers into c4.order.4), s7 (recap icons enlarged, block centred). Other exports: s4 `quik_code()`, `revapp_inset()`; s3 `sorted_chain()`, `shuffled_chain()`; s5 `answer_row()`. s7's last frame is built from ch5's `open_card()` objects, so ch4's end card is exactly ch5's opening card.
- Check flags accepted: small text only where the brief asks for miniatures (s1's small board, the open card, s2's `call_tree()` inset and the shrunk tree in c4.avg.5, s4's small reference code at size 15, s7's recap icons and ch5's end-card board at ch5's own scale). Dwell advisories: values the narration moves straight past (e.g. s3's 44,996,000 at 2.3 s, s4's `quik (rs, [])` at 2.3 s before the test call, s6's "new memory" tags), title-card lines, and the `quick`→`quik` morph pieces. s3's five "'[part of] ?' shown 0.0s" at t≈39.4 are same-place copies swapped in for a fade; confirmed invisible on frames.
- Brief departures accepted: s1 holds open_card() 0.7 s, then the title card; pivot digits YELLOW in ch3's BLUE rings (ch3's own circles have FG digits). s2 keeps `n × log₂ n` and O(n log n) up through c4.avg.5. s3 rebuilds ch2 s5's table locally (ch2 exports no builder); the sorted chain's label turns to "shuffled". s4's `quick`→`quik` is an `edit` move; "means" is a column right of the code (no room above); the code shrinks on {type}. s5 writes each call in a fixed band at the bottom; the cards inset lands 3 4 5 7 9 rather than L3's rev_app content. s6's board fades out on {pascal} rather than staying small (it'd be size 12–18). s7's r2 zigzag has no sorted chain above it.
- Glitches: s3 (ch4_s3_worst) t≈39.4 s, c4.worst.2 at "…so the tree is": four RED "0" badges popped in beside the empty `[]` nodes for a moment, just before the list nodes turned into circles. Cause: the FadeOut list held every badge in `call_tree()`, including the empty calls' badges that had never been added, so FadeOut drew them for its first frames. Fixed by fading only the badges on screen.

## Chapter 5 · Merging and merge sort (ch5_merge_sort)
State: READY FOR FINAL (2026-11-01 19:17). Preview `out/ch5_merge_sort_preview.mp4`, 10.9 min (654.5 s; 10.3 min of narration), plays end to end; `vk preview 5`: handover s2 → s3 ok (0.00%). Gemini was off: no `vk listen`/`vk review` run; the Whisper vote (0 flags) was the ear.
- **Opening card (for ch4's last scene to end on):** `load_scene("ch5_s1_hook").open_card()` returns
  the VGroup of ch5's first frame, ch4's script's end card: title "Next: merge sort" (laid out like
  ch2 s7's "Next: quicksort" end card); the scoreboard `make_scoreboard(bound="118,458")` with
  insertion sort "25,146,194" / "174 s", quicksort "158,058" / "0.53 s" (no 0.74 s), merge sort's
  row label YELLOW and its two "?" cells GOLD (static: ch4 may pulse them before the end); beneath
  it L4 ch1 s7's take/drop shot, finished: chain `3 → 5 → 9 → 4 → 7 → []`, GOLD cut after cell 2,
  `[3; 5]` and `[9; 4; 7]` lifted apart. ch5 s1 holds it, then clears to the title card.
  Confirmed (18:50): `open_card()` in `scenes/ch5_s1_hook.py` returns `VGroup(nxt, board, run, cut, L, R)`
  (also attributes): `nxt` = `T("Next: merge sort", 52, t2c={"merge sort": YELLOW})` at (0, 3.3);
  `board` scaled `min(4.40/h, 12.0/w)`, centred x = 0, top y = 2.78, cells T 44 GOLD, the other
  row labels FG; the split at scale 0.5: `run` = `ConsChain([3,5,9,4,7])` at y = −3.0, `cut` a GOLD
  dashed line (stroke 5), `L`/`R` = `ConsChain([3,5])` / `ConsChain([9,4,7])` at y = −2.05, 0.8 apart.
  ch5 s1 does `self.add(*open_card())` at t = 0. Add the same objects as ch4's last frame.
- Uses: ch4 `worst_tree()` (s1, s6) and `recursion_tree()` (s6); waits for ch6's opening card (s7).
- Narration: three QA lines rewritten and re-voiced with `--only`; `vk qa 5` now 0 flags.
  c5.mcost.4 "just as in append" → "just like lecture three's append" and "as with append" → "just
  as for the append function" (heard "a pen"); c5.code.3 "and then it just appends" → "and then all
  it does is append the two parts" (heard "just depends"); c5.trace.1 "The first let sorts the left
  half" → "In the code, the left half is sorted first" (heard "let's sort").
  COURSE.md's letter rule (producer, 2026-11-01): ch5 has no "ay"/"ell"/"gee"/"aitch". Its letters
  ("ex and why", "em plus N", "Kay", "tee-merge-sort", "tee of N") pass the Whisper vote with no
  flag, even minor, so they stay as voiced.
- Music: `music/ch5.json`. Orbit under the hook, Centroid under the merge trace (c5.merge.4),
  Clarity from c5.bottom.1's end through the recap and end card.
- Exports for ch6/ch7: s2 `Zipper(top, bot, cy, left, scale)` (`.take`/`.rest` → animation lists),
  `handover_shot()`; s4 `split_shot()`; s5 `split_tree(values=…)`; s6 `level_tree(partial=True)`,
  `quick_tree()`; s1 `filled_board()`, `open_card()`; s1 `hook_tree()` (worst_tree at hero size).
- Scenes: all 7 built (Opus builders, three batches: s1 s2 s4 s5, then s3 s6, then s7). s1 had one
  fix pass to swap its stand-in tree for ch4's real `worst_tree("circles")`. s2 → s3 is a handover
  (0.00% of pixels differ). s7 ends on ch6's `open_card()` (no fade, no handover mark).
- Check flags accepted: dwell only in s1–s6 (the inherited open card at t = 0; the title card; the
  worked-merge notes in s3 replaced as the voice moves on; s5's "sorted"/"an insert" tags; s6's
  {shape} beat, where the tree's values change every ~1 s by design; s7's bottom-up pass rows).
  Small text only in s7: the recap miniatures (digits 5–14, tree tags 7–10; the brief asks for
  miniatures, as ch1/ch2's recaps did) and ch6's end-card board headers (21–25, ch6's own design).
- Brief departures accepted (from the builders' reports): s2 clears the code at {trace} instead of
  shrinking it (no room at legible size); s3 puts `m = 2`/`n = 3` on the trace line and stacks `ins`
  above `merge`; s4 keeps only the three `let` lines at {split} and stacks the arrays/lists shot;
  s5's merges rebuild each parent row in place, leaving the dimmed tree; s6 has "+1.6%" as a label,
  not a brace (gap 0.17 units); s7's r5 reads "within 2% of the floor, still slower than quicksort".
- Motion (Gemini off): one contact sheet of mid-transition frames over every scene's riskiest play
  (s1 {merging}, s2 {s1}, s3 {deep}, s4 {moves}, s5 {count}, s6 {tree}, s7 {bottom}).
- Glitches:
  - s6 (ch5_s6_safe), c5.safe.2 {tree}, t ≈ 16.25–16.6 s: as the two small trees clear, the
    merge-sort tree's cells, arrows and `[]` fade out first and its digits stay bright for ~0.4 s
    as bare floating numbers. Cause: the digits are re-sized separately by `grow_text` and leave in
    a later play than their cells. Fixed (one play: left tree fades 0–0.7 s, right tree with its
    digits 0.2–0.9 s); confirmed on frames 16.15–16.6 of the new render.
- Accepted flag in s7: "does not end empty" (217 pieces): it ends on ch6's `open_card()` by
  design, the cross-chapter join. No `# handover` mark, as it's the chapter's last scene.
- Open: after the Gemini reset, the producer's transitions pass. ch4's last scene must end on
  `open_card()` above (ch4 records it); if ch6 changes its `open_card()`, re-render ch5 s7.

## Chapter 3 · Quicksort (ch3_quicksort)
State: READY FOR FINAL (2026-11-01 19:05). Preview `out/ch3_quicksort_preview.mp4`, 9.6 min (575 s; 9.0 min of narration); both in-chapter handovers ok (s1→s2 0.01%, s4→s5 0.00%). Built with Gemini off: no `vk listen`/`vk review` yet. After the reset, the producer's transitions pass is the only Gemini check.
- `call_tree()` (scenes/ch3_s6_trace.py, for ch4): READY. `from lib.paths import load_scene; m = load_scene("ch3_s6_trace")`; `m.call_tree(values=[3, 5, 9, 4, 7], form="lists"|"circles", size=32, pitch=1.6, gap=1.4, badges=True, pivot_color=YELLOW, empties=True, stubs=True, radius=0.38, color=BLUE, edge_color=DIM, max_depth=None, leaf_size=1)` (one-item lists are leaves) → CallTree VGroup built at the layout origin (root row y=0, x=0 = centre of the sorted ranks; pitch per rank, gap per level); move it with `.place(scale, point)`. lists: Mono list nodes ("[]" TEAL; pivot glyph in pivot_color, None = FG), x = centre of the node's rank span, GOLD ring badges (len-1; leaves 0) right of each node; [3, 4, 5, 7, 9] gives the zigzag (parts are built backwards). circles: pivots only, BLUE rings at x = rank (BST shape; 3 top-left, 7, 5/9, 4), stubs = short DIM lines toward empty children (`tree.root.stubs["left"]` is the lopsided empty branch: `.animate.set_color(RED)`; the "?" is `T("?", 64, YELLOW).next_to(tree.root.body, UP, buff=0.2)`). Attributes: `.root .nodes` (preorder, shown ones) `.edges .stubs .badges .total .node(values) .origin`; each TreeNode: `.values .pivot .level .left .right .parent .comparisons .body .badge` (`.badge.num`) `.edge .stubs .pivot_glyph .item(i)`. Also `m.list_text(values, size)`, `m.list_item(text, values, i)`, `m.even_split(scale=0.67)` (YELLOW pivot cell 5, rows "≤ 5" 3→4→[] and "> 5" 9→7→[]; `.pivot .left .right .lab_l .lab_r`).
- Narration: c3.hoare.2 ("Hoar's quicksort works" became "His original quicksort works") and c3.recap.2 ("Hoar's original divides" became "The original, by Tony Hoar, divides") rewritten and re-voiced: "Hoar's" was heard as "Horrors"/"whore's". Both now pass QA.
- c3.idea.1 rewritten and re-voiced: "those at most ay, and those bigger than ay" became "those at most the pivot, and those bigger than it" (all three models heard "ay" there as "AI"); it now passes QA.
- QA flags accepted (spelling only): "ay" heard as "AE"/"ae" (c3.code.3, c3.code.4; the letter's name; "Call it ay" passes), "bees" heard as "B's" (c3.code.3). With Gemini off, no ear has checked the "ay"/"bees"/"ell"/"ar" readings.
- Music: `music/ch3.json`. Hypothesis under the hook, Stepwise under the bottom-up rebuild (c3.trace.3), Fractals from the recap through the end card.
- Scenes: all 7 built by Opus builders; one fix pass each on s3 (the pivot copy on {copies} is now a YELLOW cell like s2's; "easier to follow" raised under "copies") and s5 (the {t4} trace line now lands in c3.part.1; the trace's rows are tighter, so the bottom row clears ~0.7).
- Joins: s1 opens on ch2's end card (rebuilt from `WhyAndRecap.teaser()` in scenes/ch2_s7_why.py; it matches out/ch2_insertion.mp4's card), holds 0.7 s, then crossfades to the title. s1→s2 and s4→s5 are handovers (`handover_shot()`). s7 builds ch4's `open_card()` (scenes/ch4_s1_hook.py) from its parts, holds it 8 s, then fades to black over 1 s, as ch2 does. If ch4 changes `open_card()`, re-render s7.
- Exports: s2 `split_icon()`; s3 `array_row()`, `swap_arcs()`, `hoare_row()`, `copies_icon()`; s4 `quick_code()` (In [80], for s5, s7 and ch4) and `handover_shot()`; s5 `part_icon()`; s6 `call_tree()`, `even_split()`, `list_text`, `list_item`. s7's r4 icon is ch4's `pivot_tree().ct`.
- Check flags accepted. Small text appears only where the brief asks for miniatures or a corner reference: s1's rebuilt ch2 end card and the board shrunk to the top (sizes 19–25, as ch2 accepted); s4 c3.code.5 and all of s5, where the corner code is at size 15 (the brief asks for the code shrunk to the left or corner, beside 40-character replies); s7's recap icons (sizes 10–15) and ch4's card board (14–22, ch4's spec). Dwell flags are on pass-through pieces the voice moves past or replaces: s1's title card and DIM plan tags; s2's per-item "≤ 5?" tags, "combine: 0 comparisons" and "merge sort: Part 5"; s3's "died…" line, the quote (read aloud, and on screen from "the reply was this", early on purpose) and "easier to follow"; s6's append steps in c3.trace.3, which are replaced line by line; s7's "?" placeholder and "0.74 s" before the recap.
- Brief departures accepted: s1's halves rejoin as loose cells. s2's pivot drops below the chain rather than lifting, because the chain is at the top; "merge sort: Part 5" sits under the brace. s3 uses `fly` copies instead of TransformFromCopy. In s4 the three `a`s glow together instead of an arrow back to `a::bs`, and {check} sits top right. s5's trace is under the corner code, not on the right. s6 lays the even split in two rows; pivot circles sit at sorted rank, so the root 3 is top-left (the brief's relative positions hold); results flow up by move-and-swap, not morph. s7's r3 and r4 lines are two lines each.
- Glitches (from builders' `--frames`, Gemini off): none confirmed. Possible ones: s1 ~44.0 s, cell corners of 9 and 4 touch during the rejoin (the numbers never overlap); s2 ~33.8–34.4 s (after the re-voice), the 9/7 swap boxes touch at mid-move; s3 c3.hoare.4, the pivot copy shows faintly in the 5 cell's pointer slot for ~0.1 s at the start of the flight; s4 ~41.0 s, the growing highlight box and brace sweep over the code for a moment (an animated box growth over text).
- Open: the bottom rows of s6's two-line step (c3.trace.1) and reply (c3.trace.3) sit ~0.45 above the frame's edge, inside the check's margin; accepted. s6's RED empty branch in the circle tree is a short stub with a RED "0" (ch4 shares that styling through `call_tree()`, so it was left alone). With Gemini off, nobody has heard the narration or watched the motion. The producer's transitions pass after the reset is the first look at both.

- 2026-11-04 Gemini pass (checks only, nothing fixed): transitions ch3-7: ch3-6 clean, ch7 look (1: ch7_s2_selcost @ 73.0 s duplicate red O(n^2)); mid-transition mismatches ch4_s4_quik @ 64.3 s, ch5_s1_hook @ 40.0 s (label 'Part 5' vs 'part 1'), ch6_s3_radix @ 47.0 s (circle on 34 not 53), unconfirmed on frames. Listens ch3/ch4/ch6: real (Gemini+Whisper) c3.code.3:4 and c3.code.4:7 'ay' heard 'ay ee'; Gemini-only claims: c3.idea.1:3, c3.code.4 'consed', c4.avg.4 'log', c4.quik.2 'exes', c4.quik.4 'ar-ess', c4.order.1 'consed'; c6.recap.1 clean. Details: media/review/ch*_transitions.md, ch*_listen_partial.md.
