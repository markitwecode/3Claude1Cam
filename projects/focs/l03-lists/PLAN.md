# Lists: plan

Request: "turn Lecture 3 of the FoCS notes into 3b1b-style videos" (2026-10-20). Audience: a
Cambridge first-year studying FoCS. Knows Lecture 1–2 (expressions, recursion, `nsum`, O-notation),
new to lists. Sources: FoCS 2026-27 notes v1.8 (`../source/focs-202627-v1.8.pdf`), pp. 21–29.
Total: 6 chapters, ~59 min of narration. Written after the fact from the finished scripts (the
first project predates the planner), so it doubles as the reference for the format.

## Chapter 1 · Lists and cons cells
Slug: ch1_lists · ~8 min · Source: pp. 21–23
Goal: say what an OCaml list is, build one from `[]` and `::`, and picture it as cons cells.
Scenes:
- s1_hook · Hook (~45 s): title card; a list as "a row of values", the question of what's inside.
- s2_what · What is a list (~85 s): list syntax, element types, `'a list`.
- s3_compare · Tuples, arrays, and two free functions (~90 s): how lists differ; `@` and `List.rev` previewed.
- s4_build · Two kinds of list (~95 s): `[]` and `x :: xs`; building `[3; 5; 9]`.
- s5_cells · Inside the computer (~80 s): cons cells and pointers.
- s6_headtail · Head, tail, and the end of the list (~95 s): `hd`, `tl`, recap, next: patterns.
Continuity: the running chain 3 → 5 → 9 → []; ConsChain styling used for the whole lecture.

## Chapter 2 · Pattern matching and polymorphism
Slug: ch2_patterns · ~9 min · Source: pp. 22–24 (§3.2)
Goal: write list functions by pattern matching, and see why that beats `hd`/`tl`.
Scenes:
- s1_hook · Hook (~50 s)
- s2_null · Two shapes, two clauses (~100 s)
- s3_hdtl · Head and tail, and the empty list (~100 s)
- s4_why · Why patterns beat head and tail (~95 s)
- s5_poly · Alpha: one function, every type (~105 s)
- s6_checked · Checked before it runs (~100 s): exhaustiveness warnings; recap.

## Chapter 3 · Length, recursion and accumulators
Slug: ch3_length · ~10 min · Source: pp. 24–25 (§3.3–3.4), plus Lecture 2's `nsum`, pp. 13–14
Goal: write `nlength`, trace it, see its O(n) space, and fix that with an accumulator.
Scenes:
- s1_hook · Hook (~50 s)
- s2_nlength · Following the shape of the list (~90 s)
- s3_trace · Watching it run (~65 s)
- s4_faulty · A tempting mistake (~75 s): two `let rec`s replace, not extend.
- s5_cost · Any type, but wasteful (~95 s)
- s6_addlen · The accumulator (~140 s)
- s7_recap · The wrapper, and recap (~75 s)

## Chapter 4 · Append and reverse
Slug: ch4_append_reverse · ~11 min · Source: pp. 26–28
Goal: write `@` and reverse; see copying vs sharing, nrev's O(n²) and the linear `revApp`.
Scenes: s1_hook, s2_code, s3_trace, s4_cells, s5_nrev, s6_cost (reuse v1's staircase → rectangle),
s7_revapp, s8_strength (reduction in strength; recap and end card).

## Chapter 5 · Strings, characters, and exercises
Slug: ch5_strings_exercises · ~10 min · Source: pp. 28–29 (§3.8, exercises 3.1–3.5)
Goal: chars and strings (not lists), escapes, ordering; hints for the five exercises.
Scenes: s1_hook, s2_strings, s3_notlists, s4_escapes, s5_order, s6_sumlast, s7_evensid,
s8_tails (exercise 3.5 hint, then the whole-lecture recap and end card).

## Chapter 6 · Solutions to the exercises
Slug: ch6_solutions · ~11 min (bonus) · Source: p. 29, drawing on pp. 21–29
Goal: worked solutions to 3.1–3.5 with traces, costs and tempting wrong answers.
Scenes: s1_intro (spoiler warning, the five exercise cards), s2_sum, s3_last, s4_evens, s5_types,
s6_tails, s7_recap. The exercise cards match ch5's (`scenes/ch5_s6_sumlast.py`).

## Decisions
- 6 chapters rather than one 8-minute video: v1 compressed the hour-long lecture into 8 minutes
  at ~195 wpm and was "damn near impossible" to follow.
- Exercises: hints at the end of ch5, full solutions in a bonus ch6, so viewers can try first.
- ch3 borrows Lecture 2's `nsum` to show the same waiting-additions pattern twice.
