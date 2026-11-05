# Lists (FoCS Lecture 3): status

`engine/vk -C projects/focs/l03-lists status` shows what exists: scripts, narration, scenes,
videos. This file holds what the files can't show: review state, accepted compromises, open
issues. Directors update their chapter's section.

All 6 scripts are written, voiced (182 lines, 59 min) and have music cue sheets.

## Chapter 1 · Lists and cons cells: ✅ done
`out/ch1_lists.mp4` (8 min, 1080p60, music). Polished, 0 dwell flags; approved by the user
("much better!").

## Chapter 2 · Pattern matching: ✅ done (2026-10-23)
`out/ch2_patterns.mp4` (9.8 min). Check-clean, reviewed (holds). s4–s6 were the first scenes
built by the scene-builder process.

## Chapter 3 · Length & accumulators: ✅ done (2026-10-23)
`out/ch3_length.mp4` (10.5 min). Reviewed (holds). Accepted check flags:
- s4: the parked warning panel is size 20 in bad.3; it was read at full size in bad.2.
- s5: the GOLD counts sit on opaque boxes over the hidden elements (poly.1); the stack runs off
  the top on purpose (cost.1, "stack overflow" as the script asks).
- s7: a deliberate 2 s silence before "Let's recap.", so the type lines can be read.

## Chapter 4 · Append & reverse: ✅ done (2026-10-24)
Video: `out/ch4_append_reverse.mp4`, 11.8 min (709.7 s), 1920×1080 at 60 fps, 3 music cues.
All 8 scenes built and reviewed over two holds rounds. s6 ports v1's staircase → rectangle and
opens on s5's end shot. s8 keeps the 8 s end card.
- Accepted flags: s3 has two in-between states in the collapse (`1::(2::[3;4])` for 0.1 s),
  timed to "Three onto four, then two, then one". s7's counter digits 0/1/2 tick once per card,
  and three more s7 items sit exactly at the minimum dwell.
- Accepted compromises: s2 holds silently for 4.2 s at the end so the OCaml error can be read.
  s2 colours the tail `xs` PURPLE, not TEAL (TEAL is `ys`). s4's front-vs-end payoff is stacked
  vertically, not side by side. Function names are YELLOW in definitions and examples, but trace
  rows stay default in s3/s5 and YELLOW in s7 (ch3 is mixed too).
- Check by ear: s1 "?" turning red on "worse"; s3 the quick collapse ({done} to {answer});
  s4 the copies on "for the two / and for the three"; s6 the flip ("flip it over" to "slot it in",
  ~0.8 s); s8 "Zero, seven, fourteen, twenty-one" (~0.8 s apart).

## Chapter 5 · Strings & exercises: ✅ done
- Video: `out/ch5_strings_exercises.mp4`, 10.3 min (615.7 s), 1920×1080 at 60 fps. 8/8 scenes,
  `vk check` clean on all (no flags accepted). Director review 2026-10-24, one round.
- Fixes this round: s1 hook.2 overrun trimmed; s4 esc.3/esc.4 had the String.length "1" stacked
  4× (now a single glyph); s5 cmp.3 code table is now larger and centred, then shrinks to its cmp.4 spot.
  s7's layout nudges checked in the holds and look fine.
- s8_tails built from the s6 plan. Where it departs from the plan: task reads "Return every tail
  of a list." (fits beside the slot); card height 3.5; the results turn TEAL together on {same};
  recap titled "Recap" as in ch1–4, with 7 rows (nrev O(n²) and rev_app O(n) split in two).
- The exercise-card kit in `scenes/ch5_s6_sumlast.py` is unchanged (ch6 copies it).
- By ear: the end of c5.hook.2 ("into strings … just so"), whose timing was re-tightened.

## Chapter 6 · Bonus: solutions: ✅ done (2026-10-24)
- Video: `out/ch6_solutions.mp4`, 12.3 min (735 s), 1920×1080 at 60 fps. Narration is 11.1 min;
  the rest is gaps, reading holds and the ~8 s end card. 7/7 scenes built, two review rounds.
- Cards: every scene imports the exercise-card kit from `scenes/ch5_s6_sumlast.py` read-only
  (BigCard row, HeroCard, pause_tag), so a change there changes ch6 too. Title is
  `title_card("Bonus · Solutions to the exercises")`. s2–s6 reopen on s1's five-card row (~0.9 s
  hold), then grow their card. s4's pending-conses column copies s2's plate style.
- Dwell flags: 96, after a producer-requested pass that fixed every flag where readable text
  (code, a result, a type, a warning) left the screen more than 1.5 s early. No overruns or
  layout flags. The 66 still more than 1.5 s short are all accepted:
  - 59 are the five-card row reprised for ~0.9 s at the start of s2–s6. It was read in s1, and
    the brief asks for it.
  - 6 are "[part of] ?" fade ghosts in s3.
  - 1 is the lone "?" in last.5 (decorative; the question is spoken).
  The other 30 are within 1.5 s of their need.
- The sum.7 trace is now stacked, not rewritten in place. Lines dim to 0.4, none wider than the
  one before, and the history collapses into `⇒ 17` on {flat}. This is the producer's call and
  departs from the brief's ReplacementTransform. s3 and s6 keep warnings and replies up (dimmed)
  into the next beat.
- Departures from the brief:
  - Recap row 3.1 shows `sum` only, with O(n)→O(1) on space.
  - The s5 ghost definition is `loop`, not `loop2`.
  - s4 leaves out the `val evens` reply and the `['a'..'d']` example; s6 leaves out the
    `tails []` and `val addtails` replies (no room, not narrated).
  - The s4 quote card reads "Lecture notes / Foundations of Computer Science · Lecture 3".
  - The recap ends with "Next lecture: More on Lists" (COURSE.md).
- Check by ear: the 2.4 s silence before the trace (c6.sum.6); the 2 s break after c6.types.4;
  the {four} count at the end of c6.tails.3; the clause swap on "the other way round"
  (c6.last.5). No narration was rewritten.

## For the user to check by ear (the QA can't judge pronunciation)
- ch1: the sentence breaths; "ex cons ell" (~4:40); "OCaml".
- ch3: "en-length", "add-len". Whisper hears "n length" and "Adlen", so they're probably fine.
- ch4: c4.code.2 "exes comma whys"; c4.code.4 "Let the at sign, in brackets, equal append".
- ch5: "caret symbol"; "backslash en"; "ASCII", "lexicographic"; c5.type.3 "the character A".
- ch6: c6.last.6 (Whisper heard "nil" as "nail"); "eye-dee"; the Milner quote.
