# More on Lists: status

2026-10-25: project created; planning.
2026-10-25: plan approved as written (user: "when you're done planning shift to execution"): 7 chapters
(6 + bonus). All 7 scripts written, continuity-reviewed by the planner: 10,575 words, ~66 min
(ch7 +9% over target, kept). Voicing started.

## Ear-check list (from writers + continuity review)
- ch1: c1.take.1 "Take eye of exes", "ex en minus one"; c1.take.2 "add-len"; c1.cells.3 "Two equals signs"
- ch2: c2.mem.1 "a tail, ell"; c2.lim.2 "Invalid argument, compare, functional value"; c2.eq.1 comparison operators; "contentious"
- ch3: "cons-pair" (c3.cons.1–3), "ex-why" (c3.cons.3), "rev-unzip" (c3.rev.1), "warning eleven" (c3.order.4), long type in c3.cons.2, "Cleo"
- ch4: "forty-three pence"/"pennies" (c4.hook.1, c4.idea.1); c4.code.2 "Failure, with the message, no more coins"; "nil"
- ch5: "all-see" (c5.allc.1–4), "see-ess"/"see-ess-ess" (c5.allc.1, .4), "int list list" (c5.answers.1)
- ch6: "see-aitch-gee(-ess)" (c6.accs.1), "minus four" (c6.accs.3), "four thousand, three hundred and sixty-six" (c6.refine.2), "eff and gee" (c6.ex.12), "eye-dee" (c6.ex.13)
- ch7: "em times en" (c7.union.5), "add-union" (c7.union.6), "by-sign" (c7.signs.2), "Match failure" (c7.zip.3), "big O of en to the fifth" (c7.count.5), "eff of one, true" (c7.types.2), "non-negative", "gee"

## Accepted compromises
- ch5 s4: notes' In [72] has `else` one column left of `if`; kept as in the notes (builder may straighten).
- ch6/ch7: zero-coin faster version shown without timings (it runs until killed).

2026-10-25: voiced, 188 lines, 65.0 min. Line-level QA worth an ear: c4.code.1 (stutter 5, WER 17%),
c1.take.1 (WER 19%), c5.allc.1 (WER 16%), c5.recap.2 (WER 13%, stutter 2); passed to the directors.
(The per-sentence "still flagged" log was lost: the run's output was piped through tail.)
Chapters 1 and 2 directing (two directors in parallel).

## Chapter 1 · Take and drop
2026-10-25: DONE. out/ch1_take_drop.mp4, 8.7 min (521.7 s), 1920x1080, 60 fps. 7 scenes built, two review
rounds (fixes in s4 and s7). Music: music/ch1.json (Resonance under the hook, Centroid under c1.cells.1,
Fractals under the recap and end card; no overlap with ch2).
Voice QA: c1.take.1 (WER 19%) is a false alarm. Whisper base and small both transcribe it word for word,
writing the letter names as letters ("x0", "xi", "xn-1").
Rewritten for the ear (re-voiced with --only): c1.take.2. Its last word "nil" was heard as "no" by Whisper
base, small and medium on two voicings. Now "...just as it did for add-len, last lecture. ... so take gives nil."
Whisper now hears it correctly.
Continuity set here: coin disc for ch4–ch7 = `Circle(radius=0.42).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)`,
value `T(str(v), size=34, color=GOLD)`, row buff 0.28 (`coin(v)` helper in scenes/ch1_s1_hook.py).
The running chain is default ConsChain([3,5,9,4,7]) at ORIGIN; the GOLD cut is a DashedLine at x -1.774, ±1.05,
dash 0.12, width 5. The end card reads "Is 9 in this list?", matching ch2's hook.
Accepted flags (all dwell):
- s1: the L3 tools row (length/append/reverse, 2.9–4.2 s) is a quick row by brief. take/drop are the
  hand-off shot, which s2 fades back in. "cost?" is up 4.3 s of 4.4.
- s2: "position i" 2.9 s (it stays until {code}); the DIM `val drop` preview 2.6 s (it starts on the
  last sentence).
- s3: s2's reply is faded back in only to fade out (already read in s2). The collapsing `3 :: 5 :: []` copy
  is up 1.7 s (row 3 shows the same text throughout).
- s4: the skipped 3 and 5 fall out and fade by design. The DIM take-trace copy is up 5.3 s of ~6 (it is
  there for its shape).
- s6: "O(1) space" 4.5 s of 5.5 (the next clip's top row restates it).
- s7: "a copy" and the recap's "no exception" are each ~0.1 s short. Clip 1's "no exception" is 4.2 s of 4.9,
  and the take/drop result blocks are up 3.7 s before the recap (topic change).
Brief departures kept: s2 stacks the DIM `val drop` preview under the type labels (no room to the right).
s4 stacks the two codes (42-char lines) instead of placing them side by side. s4/s6 traces are about Code 28
in the two-column shots.
Ear-check: c1.take.2 (rewritten line above); c1.take.1 letter names; c1.take.2 "add-len" (Whisper hears
"Adlen", jargon); c1.cells.3 "Two equals signs". Builders' timing items: s1 take→drop renames land at
the very end of c1.hook.2; s2 slot opening on "of its own"; s6 reversal step (one 1.7 s move); s7 {zero}
sentence (four changes in 6.7 s) and the end card arriving in the last 2 s of the clip.

## Chapter 2 · Searching a list
2026-10-25: DONE (voice QA fix pass, re-rendered). out/ch2_search.mp4, 9.0 min (542.9 s), 1920x1080, 60 fps.
7 scenes built, two review rounds, then one voice fix pass. Music: music/ch2.json (Hypothesis under the hook,
Stepwise under c2.fast.1–2, Endpoint under the recap and end card; no overlap with ch1).
Voice QA (fix pass): all 26 lines checked with Whisper base, small and medium. A line was rewritten and
re-voiced (--only) when two or more models agreed on a real mishearing. All 11 are now heard correctly by base,
small and medium (only jargon or a single model's slip remains):
- c2.hook.1 {last} "Take made a copy of the front part" (was "Take copied the front part", heard "Take copy the" by
  all three). Its {pause} is now {pause=2}, which gives the title card 5.0 s (was 3.9 s).
- c2.lin.3 {worst} "...and you check every element." {miss} "...you always check every element." (were "you need all
  en", heard "all in" by all three); {big} "Either way, the time is proportional to the length of the list. Linear
  search takes linear time, big O of en." (was "...grows in proportion to..." ("into a portion", "and proportion") and
  "big O of en time", heard "big O of in time" by all three)
- c2.fast.1 {halve} "Then cut what's left in half, and so on." (was "Then halve what's left": "have", all three);
  {power} "The power function from lecture two uses the same halving." (was "It's the same halving that made power
  fast": "may power", all three; then "that sped up power": "that's better"; then "used": "use"/"uses");
  {log} "So ordered searching takes only big O of log en." (was "...needs only big O of log en steps": "loggy end"
  by small and medium, on two takes)
- c2.fast.2 {million} "Let's see what that means." (was "Here's what that means.", heard "Cures what")
- c2.mem.2 {test} "If ex equals why, that's a match, and the answer is true." {else} "If not, we look in the tail,
  ..." (were "we've found it" → "we found it" and "we search the tail" → "we searched", all three)
- c2.eq.2 {walk} "...comparing the elements pair by pair." (was "comparing elements in pairs": "and pairs", two takes);
  {decide} "...so it comes down to the second elements, and two is less than three." (was "so the second ones
  decide": "aside"); {strings} "It's the rule from lecture three that put apple before banana." (was "It's the same
  rule that put apple before banana, in lecture three.")
- c2.eq.3 {first} "because the names are compared first, and Bob comes after Amy." (was "because the names already
  decide it. Bob comes after Amy.", heard "the name's already decided")
- c2.eq.4 {member} "So member can search all sorts of lists." (was "So member works on...", heard "words", all three)
- c2.lim.3 {slogan} "Notice that this is a run-time exception, not a type-checking error, ..." (was "an exception, not
  a type error", heard "tie bearer" by all three)
- c2.recap.1 {r2} "Data kept in order can be searched in big O of log en, ..." (was "Ordered data", heard "Order data")
- c2.recap.2 {next} "Next time, we'll look at lists of pairs." (was "Next time, lists of pairs.", heard "whists"/"wists")
Accepted: c2.eq.1 "the equals sign" is heard as "the equal sign" by all three (the s runs into "sign", same meaning; as
ch6 accepted plural s before "so"). False alarms: "OCaml", ex/why/ell/en written as letters, "conses", "alpha to"
heard "alpha2", medium writing "O(n)" for "big O of en" in recap.1, "run-time" vs "runtime".
Re-sync (fix-pass builders): s1 (pulse on "copy"), s2 (worst/miss braces on "check every element", the merge into O(n)
on "takes linear time … big O of en", plus a 1.4 s hold so "linear: O(n)" stays readable 3.5 s as reviewed), s3
(the Lecture 2 tag now holds through "Let's see what that means", 8.2 s; "ordered: O(log n)" waits for it), s5
(scanner on "pair by pair", GOLD column on "comes down to the second elements", `2 < 3` held into c2.eq.3), s6
("type-checks" flash on "type-checking", the slogan card on "lecture three"), s7 (r2 row text now "Data in order:").
s4 needed no change. Check after the pass: s5 and s6 clean; the other flags are the ones accepted below.
Accepted flags:
- s1: the title card is readable for 5.0 s (after the re-voice; the check wants 5.7 for the part line and 7.1 for
  the course line). It clears on "cut a list", where the chain has to come in (card and chain share the centre).
- s2: the counter-digit dwell flags (a ticking counter, ~0.6 s per spoken value). "linear: O(n)" is
  visible 3.5 s at the end of s2, but s3 fades the same group straight back in.
- s3: the s2 corner group's small text (sizes 24 and 17: the agreed 0.4 scale). The last tag shows
  6.0 s (wants 6.9); "needs arrays or trees, not lists" 6.2 s (just meets 6.2).
- s4: small dwell shortfalls ("tail" 4.2/4.3 s, "yes or no" 4.1 s, "O(n) time"/"O(1) space" 3.7 s, transient "?"
  pieces in the trace). The top-right of c2.mem.3 stays empty: the full-width chain leaves no other layout.
- s7: small text in the recap icons (sizes 11–24) and in the dimmed end-card recap. The icons are pictures, not text to read.
- s1→s2 and s2→s3 hand off by fading the shot out and back in, because the check requires each scene to end on an empty frame.
Additions, all checked in OCaml 5.4.1: s3 searches for 41 (19, 37, 43, 41); s5 shows `'a -> 'a -> bool` for the operators.
Ear-check: the 11 rewritten lines above; c2.eq.1 "the equals sign" (accepted above); c2.lin.2 "Then we reach nil"
(small alone hears "new"; base and medium hear "nil"); c2.fast.2 "arrays" (small alone hears "a raise"); plus the plan
list: c2.mem.1 "a tail, ell"; c2.lim.2 "Invalid argument, compare, functional value"; c2.eq.1 operator names;
c2.lim.5 "contentious" (heard correctly by small and medium).
Builders' timing items to check by ear: s1 per-value growth on "three … seven", the title card clearing on "cut a
list" after the longer pause, the 3, 5 pulse on "copy"; s2 the busy ~1 s merge into "linear: O(n)" (~64 s); s3 the
first halving slide on "cut what's left in half"; s5 operator boxes ~1 s apart, the scanner step on "pair by pair";
s6 the "type-checks" flash on "not a type-checking error"; s7 "names"/"phone numbers" flashes (<1 s apart).

## Chapter 3 · Lists of pairs: zip and unzip
2026-10-25: DONE. out/ch3_zip_unzip.mp4, 10.7 min (643.6 s), 1920x1080, 60 fps. 8 scenes built, two review
rounds. Music: music/ch3.json (Serendipity under the hook, Quaternions under c3.pairs.2–3 (the directory
search and the million), Orbit under the recap and end card; no overlap with ch1/ch2).
2026-10-25 voice-QA fix pass: DONE. out/ch3_zip_unzip.mp4 re-rendered, 10.8 min (650.1 s), 1920x1080, 60 fps
(narration 10.1 min). All 27 lines checked with Whisper base, small and medium. 11 lines were rewritten for the
ear and re-voiced with --only (a fix wherever two or more models agreed on a real mishearing). All 11 are now
heard correctly by base, small and medium, apart from the jargon below:
- c3.hook.1 {match} "...so Amy goes with twenty-one, Bob with thirty-five, and Cleo with forty-seven." (was "so the
  first name goes with the first number, and so on": "first thing", base+small)
- c3.zip.1 {match} "As with the append function, we match the pair," (was "As with append": "the pen" base, "the
  append" medium)
- c3.order.4 {rule} "...and the catch-all pattern at the end." (was "and the catch-all last": "casual"/"catchroll"/
  "catch roll", all three)
- c3.pairs.1 {cells} "In memory, it's a list, and each of its cells holds a pair." (was "a list whose cells each hold
  a pair": "who sells", base+small)
- c3.unzip.2 {cons} "Then ex is consed onto exes, and why onto whys, and we return the two lists as a pair." (was
  "Then cons ex onto exes, ...": all three heard "cons x's and y onto y's", the take lost "ex onto")
- c3.unzip.3 {half} "For example, let half equal twenty-one, in the expression half plus half." (was "Let half
  equal twenty-one, in half plus half": "that half", base+medium; a first rewrite "For example, let half equal
  twenty-one, in half plus half" was heard "and half plus half" by all three)
- c3.types.2 {undo} "So unzip can undo zip, with one catch." (was "So unzip undoes zip": "undo", all three)
- c3.cons.2 {lineup} "Each part of the type matches a part of the pattern." (was "lines up with": "winds up", all
  three)
- c3.cons.3 {base} "On nil, it still gives two empty lists." (was "Nil still gives...": "Neil"/"Niel"/"Neelstow",
  all three)
- c3.rev.1 {triple} "It takes a triple, made of the remaining pairs, and two accumulators, exes and whys." {base}
  "When the pairs are used up, it returns the two accumulators." (were "The pairs still to do" / "When the pairs run
  out": "pair is" both times, all three)
- c3.rev.3 {copy} "...copies the whole list of pairs, which costs one extra pass, and one new cell for each pair."
  (was ", an extra pass, with one new cell per pair": "prepare" base+small; then "and extra pass" base+small)
False alarms (jargon/spelling/homophone): ex/exes/why/whys as letters, "wild card", Cleo/"Clio", OCaml spellings,
"conses"/"consed" ("can seize", "consists", "const"), "cons-pair" ("conspare"; medium "compare" in c3.cons.3),
"rev-unzip"/"rev-app", c3.types.3 "you're" written "your". Single-model slips left: c3.order.1 "Three pairs"
(medium drops "Three"), c3.order.3 "OCaml tries" (small), c3.zip.2 "This clause" (small).
Re-sync: fix-pass builders on all 8 scenes. s2, s4, s6 needed no code change (cues are marks/phrases); s1 now
draws each column's joining line on its name; s3 comment/docstring only; s5 x flight on "ex is consed", `let half
= 21` / `in half + half` in two steps on their words; s7 the base-case box on "two empty lists" (morph ends at
{base}); s8 "pairs to do" on "the remaining pairs", cost label on "one extra pass". Chapter check: no errors,
overruns or layout flags; the remaining dwell/small-text flags are the ones accepted below (all in unchanged clips).
Shared styling: tuple cells are s4's PairCell/PairChain (value box 2.7 x 1.0, text 30), copied into s3 and s8
(lib ConsChain's value boxes are too narrow for tuples). Recursive calls (zip, unzip, revUnzip) YELLOW like the
defined name. s5 replays s1's list/pairs layout backwards; s2 hands its code to s3 by fade out/in.
Accepted flags:
- Dwell shortfalls, all small or by design: s2 "the smaller problem" 4.9/5.4 s, "this clause ignores its
  argument" 5.0/6.3, fst inset 5.6/6.1, plus the string/int substitution's token pieces (false alarm). s3
  trace row 4 (its content stays in row 6), reply A 7.2/8.3, "at least one list is empty" (it stops being
  true at the swap). s4 the climbing million counter's digits (animation) and the last two lines 4–5.5/6 s.
  s5 `unzip pairs` 4.4/4.8, `1 + (…)` 6.7/6.8, 43 4.4/5.0, final answer 8.1/9.8 (values stay in the ladder). s7
  Cleo reply 5.5/7.8 (synced to "you get"), `unzip book` reply 9.0/9.8, morph pieces at 0 s. s8 the s5/s7
  callback 3.5 s (narration moves on at 4.9 s), caveat 6.1/7.8 (read aloud in full).
- Small text, s8: trace rows and the c3.rev.2 reply at size 26 (56-character rows), and the end-card recap at
  24 (same 0.7 dim scale as ch2).
- Long OCaml replies are wrapped after `=` or `->` where one line won't fit at size ≥ 28 (s5, s6, s7; s8's
  revUnzip reply wraps after `->`, not at OCaml's own break).
- Silent tails: s1 ~5 s (under the hook music, so `unzip` stays readable), s2 ~3 s, s3 ~4 s (rule readable).
Ear-check: the 11 rewritten lines above (hook.1, zip.1, order.4, pairs.1, unzip.2, unzip.3, types.2, cons.2, cons.3,
rev.1, rev.3); c3.rev.1 "it conses" (heard "consists"/"can says"); the plan list's "cons-pair" (c3.cons.1–3),
"ex-why" (c3.cons.3), "rev-unzip" (c3.rev.1), "warning eleven" (c3.order.4), long type in c3.cons.2, "Cleo".
Fix-pass timing items: s1 each joining line reaching its number (Cleo → 47 near the clip end); s3 the "warning
eleven" flash (may start ~0.3 s after the word); s5 x flight on "consed", `in half + half` on "in the expression";
s7 the `[] -> ([], [])` box on "two empty lists"; s8 "pairs to do" on "the remaining pairs".
Builders' timing items to check by eye/ear: s1 names/numbers land on their words, names brush the number glyphs
around 24–25 s; s2 "this clause ignores its argument" appears ~2 s before it's said; s4 "not Amy / not Bob /
but Cleo" ~0.8 s apart; s6 values fly on "you get Amy", RED box on "Cleo is dropped"; s7 the 1.4 s morph at
the start of c3.cons.3, and the finished `(x::xs, y::ys)` held ~0.6 s before it moves up; s8 x/y flights on
"conses ex onto exes" / "why onto whys".

Producer note (2026-10-25): library wish, ConsChain needs a tuple-width option (ch3 built its own
tuple cell in s4; s3/s8 copy it). Engine change, for the user or producer, not scene agents.

## Chapter 4 · Making change
2026-10-25: DONE. out/ch4_change.mp4, 8.5 min (511.3 s), 1920x1080, 60 fps. 7 scenes built, two review
rounds (fixes in s1, s3, s4, s6; s2's till chain swapped into s4, s6, s7). Music: music/ch4.json (Clarity
under the hook, Fives under c4.trace.1–2, Far Away under c4.recap.2 and the end card; no overlap with ch1–3).
Voice QA: c4.code.1's "stutter 5" is a Whisper-base hallucination. It repeats "Change for zero is nil" in
0.2 s at confidence 0.00 over the decaying tail; the audio has it once. Its WER came from "Like append and
zip", which base, small and medium all heard as "a pendant zip". Small and medium checks of all 21 lines found three more.
Rewritten for the ear and re-voiced with --only (now heard correctly by base, small and medium):
- c4.code.1 "Like append, and like zip, it matches two things at once,"
- c4.code.2 "The second clause catches the case where the till is empty, but money is still owed." (was "an
  empty till", heard as "an empty tell" / "enough detail")
- c4.idea.2 "First, change for zero is the empty list, no coins at all." and "Third, if a coin is too large,
  we remove it from consideration." (were "...no coins at all, the empty list" → "the empty waste", and
  "is removed" → "is a roof")
- c4.zero.1 "Even from an empty till, change for zero gives nil, the empty list." (was "...for zero is nil",
  and a "returns nil" try: both heard as "no", the ch1 problem)
"nil" is now heard correctly in all four lines that say it (c4.code.1, c4.trace.2, c4.zero.1, c4.zero.2).
Continuity set here (for ch5–ch7): s2's `coin`, `till_chain(values, scale=0.85)` (ConsChain scaled, each label
swapped for `coin(v, r=0.357)`, value T 34 GOLD, nil TEAL) and `till_pointer` (YELLOW Mono "till" 36, arrow
stroke 3, length 0.75) in scenes/ch4_s2_idea.py; s4, s6, s7 copy them. Hero code: Code 28, left -6.5, top 3.25.
Ch5's hook opens on s6's end shot (positions are in ch4_s6_greedy.py's docstring): till [5; 2] by
`till_chain(scale=1.0)` centred (-1.30, 2.55), cells x -3.32/-1.02, nil 1.03; DIM "amount" T 30 (3.40, 3.25)
over GOLD "6" T 64 (3.40, 2.55); DIM "paid" T 30 (-4.43, 1.20), first slot (-3.32, 1.20); trace Code 36 left
x -5.80, baselines -0.02/-0.78/-1.54/-2.30, DIM ⇒ MathTex 58 at x -6.33; RED exception Code 32 left -6.60,
baseline -3.10; GREEN coin(2) ×3 at x 3.83/4.95/6.07, y -1.20; GREEN MathTex 56 `2 + 2 + 2 = 6` at (4.95, -2.20).
s7's end card (node "6, [5; 2]", use 5 / skip 5 tree) is described in ch4_s7_recap.py's docstring.
Accepted flags (all dwell or icon size):
- s1: title card 5.3 s and ch3's zip picture ("unzip" 1.7 s). They now clear on "everyday life" (6.4 s), the
  latest point before the till is narrated. RED "?" 3.5 s of 4.1 before the hand-off.
- s3: s2's three cards up 0.3 s at the open (hand-off shot, just read in s2).
- s4: call-line rewrites while 20, 10, 5 are skipped (brief: quick succession, one call each); counter "23"
  3.1 s; the collapsing copy (as ch1 accepted); 50 coin / `change [1] 0` / 99p reply about 0.2 s short.
- s5: the six-line `nchange` card 14.5 s (the narration walks it); its call and RED reply ~6 s of 7;
  "does nothing" 4.8 s of 4.9.
- s6: the two "too big" labels (the narration gives the skip ~2 s); "fewest coins, for every amount" 2.7 s
  (spoken word for word).
- s7: small text in the recap icons (sizes 14–22), as ch2 accepted. The icons are pictures, not text to read.
Brief departures kept: s2 cards build centred under the chain, then move right on {try43}. s3 cards 2 and 3
sit under the code (lines 4–6 run full width). s5 `nchange` card replaces the code, centred (52 chars, too
wide beside it). s6 crossed-out 5 is one diagonal strike. s7 r1 icon is a short till `50 → 20 → 10 → … → []`.
Ear-check: the four rewritten lines above; "consed" (c4.code.4, c4.trace.1, c4.trace.3: Whisper hears
"can cede"/"concede"/"considered", jargon); c4.zero.1 "tried in order" (medium hears "tried and ordered");
c4.code.4 "We put the coin back" (small hears "Reput"); "forty-three pence"/"pennies" (c4.hook.1, c4.idea.1);
c4.code.2 "Failure, with the message, no more coins". Builders' timing items: s3 c4.code.4 cues on "It's
the coin", "twenty", "thirty-eight", and the c4.code.5 braces on "the till"/"the amount"/"the coins"; s6 "One is
less than five, and less than two" (two trace steps 0.9 s apart).

## Chapter 5 · Every way to make change
2026-10-26: DONE. out/ch5_all_ways.mp4, 9.6 min (575.2 s), 1920x1080, 60 fps. 7 scenes built (s3, s5, s6 resumed
after the usage limit), two review rounds (round 2: s6's tree nodes/edges matched to s3's constants; s1 and s7
re-synced to re-voiced lines). Music: music/ch5.json (Sixes under the hook, Gnomon under
c5.choices.2–3 (the tree grows), Reflections under c5.recap.2 and the end card; no overlap with ch1–4).
Voice QA: all 24 lines checked with Whisper base, small and medium. "nil" is heard correctly in every line by all
three. c5.allc.1 (WER 16%) is a false alarm: jargon only ("All C", "CS", "CSS", "consents" for conses).
Rewritten for the ear and re-voiced with --only (a fix was made when two or more models agreed on a real mishearing):
- c5.hook.2 {today} "In this chapter, we'll write that function," (was "we write", heard "rewrite")
- c5.choices.4 {growing} "a single two, then a pair of twos, then three twos." (was "two, two, … two, two, two": the
  TTS added a fourth "two")
- c5.code.3 {at} "Then the at sign appends both lists of solutions." (was "the two lists", heard "two wists")
- c5.allc.2 {example} "Let's try an example, with the coin two." (was "Here's an example", heard "Use an example")
- c5.trace.1 {root} "The two fits, so we can use it, or skip it." (was "both choices are open", heard "both traces")
- c5.trace.3 {front} "giving two plus two, and two plus one plus one." (the TTS added a third "one")
- c5.trace.4 {greedy} "Five plus one comes first, and that's exactly what greedy would have given." (was "the very
  first, five plus one", heard "first by plus one", then "In five plus one")
- c5.recap.1 {later} "We'll come back to making change in a later lecture," (was "We'll meet making change")
- c5.recap.2 {r1} "We return every way as a list of solutions, where each solution is an int list." (the TTS dropped
  one "list" from "int list list" on two takes; "To find every way" was then heard "Defined"); {r2} "an empty till,
  with money still owed, has none" (was heard "money out"); "the append" in {r3} and {next} (bare "append" heard "a pen").
Shared looks set here (for ch6's trace): solution box = coins (coin ×0.6) in a TEAL RoundedRectangle (corner 0.1,
stroke 3, pad 0.12); a list of solutions = those in a bigger TEAL box (corner 0.15, stroke 4, pad 0.2), `[]` = it empty.
Tree = Mono "amount, till" (GOLD/TEAL) in BLUE rounded boxes, "use c" down-left, "skip c" down-right. Numbers are in
scenes/ch5_s3_choices.py's docstring (s6 matches them): Mono 30, box h 0.62, width text + 2 × 0.25, corner 0.15, BLUE
stroke 3; levels 1.4 apart; edges parent bottom ±0.35 → child top, FG 4; labels T 30 (value GOLD), "(too big)" DIM;
results Mono 30, GREEN answers, RED dead ends. Collapsed subtree (s6): a second card edge peeking out behind the node.
In [72] is Code 24 (62-column lines), left -6.2, top 3.6 (s4 → s5); verbatim, `else` one column left of `if`.
Accepted flags (all dwell or small text; no errors, overruns or layout flags):
- s1: title card's course/part lines 5.1 s (the till comes in on "five and two"); the two "too big" labels
  (measured 0.8 s, readable ~1.5 s: the slide-off is delayed inside the play; the narration gives it ~2 s).
- s2: ch4's struck exception 5.5 s of 7.0 (read in ch4, struck on the line that says so).
- s3: "two sources of solutions" 3.1 s (the board clears at "for six" so the outline is up by {root});
  `[] @ [[2; 2; 2]]` 2.1 s (it becomes the answer on "Joined together"); "greedy's path" 4.9/5.0; "[part of] ?"
  pieces are node labels rewritten from their parent's (false alarm, as in s6).
- s4: In [72] and replies at size 24 (62-column verbatim lines; 24 is the largest that fits); "no ways" 4.4/4.5.
- s5: In [72] 0.7 s at the open (s4's hand-off shot) and the long code/error blocks (on screen for as long as the
  narration allows); "2 solutions → 2 solutions" 2.7 s (clip end); coin digits 24 at the chapter's 0.6 coin scale.
- s6: greedy reply 4.4 s of 5.8 (enters with the last sentence, held 1.9 s after it); coin digits 24 (s5's 1.2 pair).
- s7: icon text 16–26 and In [72] at 22 on the end card (pictures, as ch2/ch4 accepted); r4 icon coins 3.2/4.1 s;
  In [72] 14 s on the end card (shown at length in s4).
Brief departures kept: s1's root/children sit a little lower and wider than ch4's end card (room for the answer
preview), its dead end is ch4's RED cross, and its twos row is centred, not at ch4's spot (a title card sits between).
s2 adds DIM "amount"/"till" labels (so the till's `[]` isn't read as an answer). s3's rising answers are Mono text,
not coin boxes; its outline is its own (DIM full tree), not s1's. s4's `[[]]`/`[]` boxes sit right of lines 1–3,
the greedy inset under the code. s5's {step} labels go on the data row, the {letin} brace on the left, the type
error without location lines (RED underline instead of carets). s6's replies wrap over 3 lines (the 72-column line
doesn't fit at size ≥ 28). s7 adds a small-case tree on "Trace a small case by hand"; its header is "Next: faster,
and exercises".
Ear-check: the rewritten lines above (all heard correctly by base/small/medium after re-voicing, except c5.recap.2
"And the local function", which small and medium hear as "In the local function"; accepted, the meaning holds);
c5.allc.1–4 "all-see", "see-ess", "see-ess-ess", "conses" (jargon); c5.answers.1 "int list list"; c5.trace.2 "We owe two".
Builders' timing items: s3 "a single two / a pair of twos / three twos" steps ~1.2 s apart; s5 the coin flights on
"two, two" / "two, one, one"; s7 the GOLD highlights on "copying" / "append do"; s1 the till on "five and two", the
cells sliding off on "the till ran out".

Producer note (2026-10-25): voice QA (Whisper base) misses real mishearings that small/medium
catch (ch1 "nil"→"no"; ch4 "a pendant zip", "enough detail", "nil"→"no" again). ch1 and ch4 were
fully checked with base/small/medium; ch5–7 directors told to do the same. **ch2 and ch3 got
only a flagged-line check**, so give them a full multi-model check and fix pass once ch7 is done.

Producer note (2026-10-26): a usage limit stopped the ch5 and ch6 directors (and ch5_s5/s6 builders)
mid-run; both directors resumed after the reset. ch7 not started yet.

## Chapter 6 · Faster, and exercises
2026-10-26: DONE. out/ch6_faster_exercises.mp4, 11.1 min (668.1 s), 1920x1080, 60 fps. 7 scenes built, two review
rounds (fixes: s1 In [72] spacing to match ch5; s2 accs.5 reply wrapped to size 26; s7 end card on s5's `six_cards()`).
Music: music/ch6.json (Spirals under the hook, Focal Point under
c6.trace.1–3 (the accumulator trace), Quantum Blue under c6.recap.2–3 and the end card; no overlap with ch1–5).
Length: 11.1 min against the plan's ~9.5 (narration 10.3 min plus gaps, holds and the 8 s end card); kept.
Continuity set here: the exercise-card kit lives in scenes/ch6_s5_hints1.py (L3's BigCard/HeroCard/pause_tag etc.,
`six_cards()` = six dim cards in two rows of three + the "Solutions: bonus chapter" note, EX_* text constants;
`__all__`, no side effects). s6 and s7 import it, and so does ch7; don't change its API. s5 and s6 end on the pill strip
`make_strip(...)` (left x -6.5, y 3.2). s7's end card = `six_cards()` scaled 0.85, top at y -0.09, under dimmed
"Next lecture: Sorting" pictures (ch7 opens on s5's native layout, after a fade).
In [72] in s1/s4 is ch5's string, column for column (`else` one column left of `if`). s2 → s3 hand off
`change [2; 1] 4 [] []` (Code 32 at (0, 3.3)) by fade out/in. s3 uses ch5's tree style with its own spacing (6 levels).
Accepted flags (all dwell or small text; no overruns or layout flags):
- s1: title card readable 3.9 s (as ch2/ch4 accepted); In [72] at size 22 (ch5's end-card size) and up 33 s of the
  41 s its length asks for.
- s2: "caught one call later" 3.5/5.5 s (the next clip clears on its first words); "no solutions yet" 5.1/5.2;
  coin digits 24 (ch5's 0.6 coin scale).
- s3: coin digits 19 in the `chg` tags and the solutions row (16-node tree); `[2; 2]` 3.8/4.1 s (it turns into the
  reply); `1 + 1 + 2 = 2 + 1 + 1` 4.4/4.8 s and rev_app 12.1/12.2 s (both up to the closing fade).
- s4: both full listings 18 s (shown at length in s1/s2), In [72] at size 18 and In [73] at 24 (stacked, 62-column
  lines); "`chgs` instead" 4.5/4.9 s.
- s5: OCaml's 4.3 warning at size 23 (67-column verbatim line).
- s7: icon text (chain values 11, card titles 24 on the end card), pictures as ch2/ch4/ch5 accepted.
Brief departures kept: s1 In [72] is the centred hero in clip 1 and small only in clip 2, and its plan cards show
numbers only. s2 code at size 26 (61-column lines; top 2.62 so the chg/chgs labels sit above); `chg` GOLD, `chgs` TEAL;
the feed arrow runs on a small fork under the code; the solutions frame is a row, as in ch5. s3: the solutions stack is
a row (top right, new ones on the left); only the root's edges are labelled; replies use ch5's two-line layout; the
dead ends light on {dead}, after the four-ones solution, as the narration orders it (the program reaches them first).
s4: codes stacked (old top-right, new bottom-left). s5: cards in two rows of three; 4.2's "?" is under the hint as
"0 → ?"; ch3's unzip indentation. s6: 4.6's {where} arrows point at the whole `(1, true)` (not giving the answer away).
s7: two recap pages (seven rows don't fit one column); no "two accumulators" tag.
Voice QA: all 31 lines checked with Whisper base, small and medium. A line was rewritten and re-voiced (--only)
when the models agreed on a real mishearing. All are now heard correctly by base, small and medium:
- c6.hook.2 {reverse} "instead of appending, made reverse fast." (was "instead of append", heard "a pen"/"a pent")
- c6.accs.3 {lessthan} "The third clause begins with a new test." and {caught} "The overshoot is only caught one call
  later." (were heard "pause"/"plaza" and "cut" by base and small)
- c6.trace.4 {reversed} "Last time it was two, one, one, and now it's one, one, two." (was "It's one, one, two, not
  two, one, one": the TTS added a fourth "one", heard by all three)
- c6.refine.2 {measured} "When we timed both versions, the new one was about two and a half times faster." (was "in
  the OCaml toplevel", heard "topple" by all three; then "the two in OCaml", heard "the Tuono camel")
- c6.ex.6 {code} "Here's another version of the zip function." (was "version of zip", heard "sip" by all three)
False alarms: "see-aitch-gee(-ess)", "all-see", "conses"/"consing", "rev-app", "eye-dee", "eff"/"gee", "en", "OCaml"
(jargon/letters); the repeated last sentence over {pause} tails (hook.1, hook.2, ex.3, ex.11: no-speech prob ≥ 0.76,
a hallucination); digits for "fifty … ninety-nine pence".
Ear-check: the five rewritten lines above. "solutions so far"/"coins so far" (accs.2–4, trace.2–3, refine.1): all three
models often hear the singular, because the plural s runs into "so"; accs.5 and trace.3 are heard correctly, so this was
accepted as co-articulation. c6.ex.5 "just as unzip did" (base/small hear "unzipped"); c6.recap.2 "A let can match"
(heard "alet"); c6.hook.2 "appending" (small hears "a pending"); plus the plan list (see-aitch-gee, minus four,
four thousand…, eff and gee, eye-dee).
Builders' timing items: s1 three quick cell copies ~1.4 s after "over and over"; s6 phrase cues "each version",
"count as one", "and gee", "both return", "It can only use"; s7 {merge} four beats in 5.7 s.

## Chapter 7 · Bonus: solutions to the exercises
2026-10-26: DONE. out/ch7_solutions.mp4, 12.6 min (755.4 s), 1920x1080, 60 fps. 8 scenes built, two review rounds
(round 1: s1 cards switched to ch6's titled `six_cards()` layout; s3–s7 pill kept CURRENT during the solution;
round 2: s3/s6 pill blink removed). Length: narration 11.5 min plus gaps, pause holds and the 8 s end card, against the
plan's ~10.5; kept (the bonus script was already +9%). Music: music/ch7.json (Zeta under the hook, Occlusion under
c7.count.2 (the coin rows), Ongoing under c7.recap.2 and the end card; no overlap with ch1–6).
Continuity: every card scene (s2–s7) opens the same way, using ch6's kit imported read-only from scenes/ch6_s5_hints1.py.
ch6's pill strip `make_strip` (left -6.5, y 3.2) fades in with earlier exercises DONE, its own CURRENT and later TODO.
The card grows out of its pill onto the HeroCard, with pause_tag top right, held through the pause. Then the card's
contents fade and its frame shrinks onto the pill as it is (not the kit's `exit_card`, which marks it DONE). The pill
stays YELLOW as the scene's header until the final fade. s1 shows `six_cards()` (two rows of three, as ch6's end card)
and ends by shrinking them into that strip.
Accepted flags (no errors, overruns or layout flags):
- s3: dwell on the ladder's "waiting" tags (replaced as calls return, as in ch3), the unzip/revUnzip/slow code leaving
  as the narration moves on (revUnzip ~3 s), and the 20-element counters / earlier `slow` answer (~4.9 s).
- s4: OCaml's 4.3 warning at size 23 (the 67-column verbatim line; ch6 accepted the same). Dwell on short-lived states:
  the card on {warn}, the equal-length cells cleared on {trace}, the old type ~2 s, the unzip blocks cleared on {design}.
- s5: the three change functions are small labelled code-card thumbnails along the top (size 4). They act as pictures:
  the full functions can't be legible three across, the labels and YELLOW/RED highlighting carry identity, and the
  traces show the behaviour. The two eight-way columns and the `[5; 2; 1; 2] 4` reply are size 26 (verbatim one-line
  reply). Dwell on results the narration replaces quickly (`Failure`/`[]` 4–5 s, greedy's `[2; 2]` ~2 s before
  {close}, the eight-way columns ~4 s).
Brief departures kept: s1 routine centred under the rows ("‖ pause → solve → trace and cost"), the RED ✗ card on the
bottom band (the "Solutions: bonus chapter" note leaves on {wrong}). s2 union rewrites into addunion in place (no
room side by side), no `val addunion` reply, union's `x ::` glows on {iter} (trace gone by then). s3 long `if` lines
wrapped, unzip/revUnzip below the code. s4 Forgiving/Strict stacked, not columns. s6 the 20p case as rows of coins with
the remainder packed with 2p discs; reply wrapped one inner list per line. s7 g examples as definitions only; loop
under the boxes. s8 recap rows clear (not dim) for the Sorting teaser, numbers/names kept as a dim column; "ways" and
`f, g` as row names for 4.5/4.6.
Voice QA: all 36 lines checked with Whisper base, small and medium. "non-negative" (c7.signs.1) heard correctly by all
three. Rewritten for the ear and re-voiced with --only (a fix whenever two or more models agreed on a real mishearing):
- c7.union.2 {wrong} "First, a shortcut that looks tempting." (was "a tempting shortcut", heard "attempting")
- c7.union.4 {shared} "Like the append function, it shares whys," (bare "append" heard "a pen", as in ch4/ch5)
- c7.union.5 {cost} "What does union cost?" (was "What does it cost?", heard "What is a cost?"); {mn} "Each member
  test may scan the whole of the second list, once per element of the first." (was "up to en comparisons", heard "in")
- c7.signs.2 {shape} "Two results at once is the shape of unzip, from chapter three." (was "unzip's shape", heard
  "unzipped shape"); {base} "On nil, it gives back two empty lists." (was "Nil gives a pair of empty lists": "wists",
  then "Neil")
- c7.signs.6 {cost} "Either way, the time is big O of en, and so is the space the answer takes." ("big O of en time"
  heard "big O of in time")
- c7.zip.4 {design} "Which one is better? That's a design choice." (was "Which is better is a design choice", heard
  "...started with, which is better as a design choice" by all three)
- c7.assume.3 {zero} "First, a coin worth zero." (was "a coin of zero", heard "a coin, a zero" by all three; now
  matches ch6's chip "a coin worth 0")
- c7.assume.5 {asc} "Third, a till in increasing order." (was "ascending", heard "a summing"/"a semi"); {nine} "Asked
  for nine, from one, two and five, it hands back nine pennies." (was "Nine pence ...", heard "Nine pens" by all three)
- c7.count.1 {card} "Take two coin values, and an amount to make, called en. Ignoring order, show that the number of
  ways to do it is big O of en." (was "...big O of en ways ... for an amount, en, ignoring order": "NA ways", "and")
- c7.count.3 {fix} "...which can be anything from zero to the amount divided by the big coin." (was "from zero up to
  en": "of", then "to on"); {once} "...so each count gives one way, or none." (was "at most one way": "it most")
- c7.count.4 {mult} "...so there are big O of en squared ways altogether." (was "ways in all", heard "and all");
  {induct} "Each extra coin brings one more factor of en." (was "multiplies by another en": "eon", "ian")
- c7.count.5 {uk} "With all six coins, from fifty down to one, the count grows as big O of en to the fifth." (was
  "With the whole till": "tail"; then "it's big O" lost its "O")
- c7.recap.1 {r4} "The change functions trust the till to hold positive, distinct coins, in descending order, and the
  amount to be zero or more." ("descending, and" heard "descending in"); {r5} "With two coins, the ways grow as big O
  of en, ..." (was "big O of en ways", heard "inlays")
All now heard correctly by at least two of the three models. Accepted: c7.intro.2 "the question" heard "a question"
(small, medium; same meaning); "consed"/"conses" in c7.union.3 and .6 (heard "consistent", "can seize": jargon, as ch3–ch5);
c7.count.4 and c7.count.5 "still flagged" by the voice tool: Whisper base only (a repeated last sentence with no
second take in the audio, and digits for "ninety-nine pence"); small and medium hear both lines correctly.
Ear-check: the rewritten lines above (c7.union.2, .4, .5; c7.signs.2, .6; c7.zip.4; c7.assume.3, .5; c7.count.1, .3,
.4, .5; c7.recap.1); the plan list ("em times en", "add-union", "by-sign", "Match failure", "big O of en to the fifth",
"eff of one, true", "non-negative", "gee"); "consed"/"conses" (c7.union.3, .6); c7.intro.2 "the question".
Builders' timing items: s1 cues "lecture four", "worked solutions", "the question", "trace it"; s2 the four-step trace on
"So is seven" / "One is new"; s3 the down/up ladder (steps 0.45–1.0 s); s4 dimming on "unequal lengths", the 47 dropping
on "two numbers", the box on "Cleo and nil"; s5 the c7.assume.3 run "last thing" → "runs on" → "growing" → "memory"
(ends ~0.2 s before {neg}); s6 the {check} flashes on "twenty, fifteen, ten, five or zero" and the coins-to-reply move
under "three ways, as change finds"; s7 the "single zero / two zeros / or more" entries ~1 s apart; s8 the `[0; …; 0]`
copies on "to return" and the 4.4 conditions on their words.

## Done (2026-10-26)
All 7 videos in out/, 70.4 min (ch1 8.7, ch2 9.0, ch3 10.8, ch4 8.5, ch5 9.6, ch6 11.1, ch7 12.6).
Every chapter's narration got the full base/small/medium Whisper check; misheard lines were
rewritten and re-voiced (ch1 1, ch2 11, ch3 11, ch4 4, ch5 10, ch6 5, ch7 13). Each chapter's
section above lists the rewritten lines and the accepted flags: those lines are the ear-check list.
