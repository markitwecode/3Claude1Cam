# Sorting: plan

Request: "hey! can you create a couple chapters for lecture 5 in focs" (2026-10-27). The user chose
to plan all of Lecture 5, so continuity is right, but to commission only chapters 1 and 2 for
production now. Chapters 3–7 are planned, not commissioned: they fix what ch1–2 set up and
promise, and get scripted only if the user asks for them later.
Audience: a Cambridge first-year studying FoCS who has watched our Lecture 3 and 4 videos (lists,
cons cells, patterns, `'a`, accumulators, `@` and `rev_app`, take/drop with copying vs sharing,
linear search, polymorphic `=` and `<=`, zip/unzip and `let` patterns, making change, stepwise
refinement). They know Lectures 1–2 from the notes: floats and `*.`, recursion vs iteration,
O-notation, and the recurrence table (`nsumsum`'s T(n+1) = T(n) + n is O(n²); T(n) = 2T(n/2) + n
is O(n log n), tabulated but never derived). Sources: FoCS 2026-27 notes v1.8
(`../source/focs-202627-v1.8.pdf`), pp. 37–44, plus the two web sources in project.json (Hoare's
dates, the random-number generator).
Total: 7 chapters (6 + a bonus), ~65 min of narration. Commissioned now: ch1–2, ~19.5 min.

All replies, results and comparison counts quoted below were checked in OCaml 5.4.1. The counts
come from replacing `<=` with a counting `le` (recipe in project.json). Script-writers still run
every line themselves.

Lecture-wide visuals (set in ch1, kept to the end):
- **The running chain** `3 → 5 → 9 → 4 → 7 → []` (L3/L4's chain, default `ConsChain([3,5,9,4,7])`
  at ORIGIN). Every sort in the lecture is traced on it and returns `[3; 4; 5; 7; 9]`, drawn as
  a chain with a GREEN tick.
- **The scoreboard**: rows insertion sort / quicksort / merge sort. Columns: "comparisons on
  10,000 random items" (our counts) and "DECstation time" (the notes'). A floor line beneath reads
  "lower bound ≈ 118,458". Every cell starts as a GOLD "?" and is filled in when its chapter
  earns it. Defined once in `scenes/ch1_s4_contest.py` for later scenes to import.
- Notation: C(n) is the comparisons needed for n items (the notes'), and T(n) is a cost recurrence
  (Lecture 2's). Write log₂ on screen wherever we count steps (the bound, tree levels), and plain
  log inside O(…), where the base doesn't matter (Lecture 2). Say "log base two of N" and "N log
  N" (as ch1–2 were voiced). The algorithm is "merge sort", two words, and the code's name is
  `tmergesort`. `quik` sounds like `quick`, so the narration calls it "quick with accumulator" (and
  the original "plain quick" where both appear). Colours as
  in L3/L4: function names YELLOW, numbers and costs GOLD, types GREEN, `'a` PINK.

## Chapter 1 · How fast can we sort?
Status: COMMISSIONED (2026-10-27)
Slug: ch1_how_fast · ~10 min · Source: pp. 37–39 (intro, §5.1)
Goal: say what sorting is for, step through binary search, prove that any comparison sort needs
about n log₂ n comparisons (2^C(n) ≥ n!), and describe the 10,000-number test list.
Scenes:
- s1_hook · Hook (~50 s): title card "Part 1 · How fast can we sort?". One sentence on last
  lecture: list tools, search one cell at a time, making change, and its closing promise that
  sorted data can be searched fast. The chain 3 → 5 → 9 → 4 → 7 → [] rearranges itself into
  3 → 4 → 5 → 7 → 9 → []. Every method we'll meet gets there by comparing two items at a time.
  The question: how many comparisons does sorting need, and could some clever method need fewer?
- s2_why · What sorting is for (~85 s): the notes' five uses, one icon each. Search (next scene).
  Merging (two sorted files combine quickly; a preview of Part 5). Duplicates (after sorting,
  equal items sit side by side, so one pass over neighbours finds them; show a short name list).
  Inverting tables (the telephone directory, sorted by name; re-sort it by number, which is useful
  to the police, or by street address, useful to junk-mail firms. The same information gets
  different applications; L4 ch3's directory of pairs). Graphics algorithms (name only; one
  optional clause of example, e.g. drawing far shapes before near ones, is beyond the notes).
  Sorting is perhaps the most deeply studied part of algorithm design: Knuth's *The Art of Computer
  Programming* gives it a whole volume (Vol. 3, *Sorting and Searching*), and Sedgewick covers it
  too.
- s3_binary · Binary search, as promised (~75 s): L4 ch2 said "binary search, coming next
  lecture". The notes give its idea, and here it is step by step. Reuse L4 ch2 s3's row of 16
  sorted primes `2 3 5 … 53` and its search for 41 (`STEPS` in
  `projects/focs/l04-more-lists/scenes/ch2_s3_faster.py`). Compare with the middle item (position
  n/2), 19: 41 is bigger, so discard the left half. Then 37, then 43, then 41 found: four
  comparisons, where linear search needs 13. O(log n) against O(n). L4 already gave the
  million-in-20 figure, so recall it in one clause at most. Why not on lists: reaching the middle
  of a list means walking n/2 cells from the head. So it needs arrays or trees, and binary search
  trees come later (DIM tag "Lecture 7").
- s4_contest · The contestants, and how to score them (~70 s): the common algorithms are
  insertion sort, quicksort, merge sort and heapsort. We study the first three (heapsort is named
  only, as in the notes), and each has its advantages. The usual measure is the number of
  comparisons, C(n): it's how these sorts learn the order, and it doesn't depend on the machine
  (Lecture 2: ignore constant factors). Alongside, the notes give run times on a DECstation (MIPS,
  an early RISC chip, really old now), useful only relative to each other. Build the scoreboard
  here, all "?". The notes give no comparison counts, so say once that we count them ourselves,
  "with a less than or equal that keeps a tally" (ch2 reuses those words).
- s5_bound · Twenty questions with n! answers (~115 s): the lower bound. Three items a, b, c have
  3! = 6 possible orders; list all six. A sort must find out which order it was given, since each
  one needs a different rearrangement. A comparison is a yes/no question, so at best it rules out
  half the orders still possible. Draw the decision tree for three items: root "a ≤ b?", six
  leaves, depth 3. Two questions reach at most 4 leaves, fewer than 6, so some input needs a third
  question. In general, C comparisons tell apart at most 2^C orders, so 2^C(n) ≥ n! and
  C(n) ≥ log₂(n!). It's a worst-case bound: whatever the method, some input forces this many.
  (The notes' bullet says "each comparison eliminates half of the permutations"; that's the best a
  comparison can do.)
- s6_nlogn · How big is log₂ n!? (~95 s): log₂(n!) = log₂ 1 + log₂ 2 + … + log₂ n, drawn as bars
  of heights log₂ k. Every bar is at most log₂ n, so the sum is ≤ n log₂ n. The taller half are
  each ≥ log₂(n/2), so the sum is ≥ (n/2) log₂(n/2). So it grows like n log n. (This sandwich
  argument is beyond the notes; the notes go straight to it.) The notes' sharper form is
  ≈ n log₂ n − 1.44n (from Stirling's formula; 1.44 ≈ log₂ e, name only). Numbers: for our five
  items, 5! = 120 and log₂ 120 ≈ 6.9, so some arrangement of five needs 7 comparisons. For 10,000
  items, log₂(10000!) ≈ 118,458 (the formula with 1.44 gives ≈ 118,477, and with log₂ e itself
  ≈ 118,450; the script shows the 1.44 value and says "nearly the same"). Merge sort needs only O(n log n)
  (Part 5), so O(n log n) is the best possible, and merge sort reaches it. Draw the scoreboard's
  floor line.
- s7_testdata · Ten thousand random numbers (~85 s): the notes say "never mind how this works",
  so show the shape only. `nextrandom` multiplies by 16807 and keeps the remainder after dividing
  by 2147483647 (= 2³¹ − 1), done in floats: `t -. m *. floor (t /. m)` is that remainder.
  `nextrandom 1.0` ⇒ `16807.`. Reply `val nextrandom : float -> float`. It's Park and Miller's
  1988 "minimal standard" generator (beyond the notes). `randlist` carries the current seed and
  the list so far in one pair and counts n down. That's L4's trick of building two results in an
  accumulating argument; `| 0 ->` is a constant pattern. Reply
  `val randlist : float * float list -> int -> float * float list`. Then
  `let seed, rs = randlist (1.0, []) 10000` (L4 ch3's pattern `let`) ⇒ `val seed : float =
  1043618065.`, which is exactly the check value Park and Miller published, a sign the generator
  is right. `rs` starts `[1484786315.; 925166085.; 1614852353.; …]` and, built backwards, ends
  `…; 16807.; 1.]`. The toplevel's long printout is a scrolling glimpse, not read aloud.
  `<=` is polymorphic (L4), so every sort works on these floats as well as on ints and strings.
- s8_recap · Recap (~45 s): uses of sorting; binary search; comparisons as the measure; the
  bound 2^C(n) ≥ n!, so about n log₂ n; the test list. Next time: the first contestant, sorting
  the way you'd sort a hand of cards. The end card shows ch2's opening picture.
Continuity: the running chain and the scoreboard start here. The 16-prime row and search for 41
come from L4 ch2. The "7 comparisons for five items" floor comes back in ch2 (insertion sort
uses 6 on our chain), ch3 (quicksort uses 8) and ch5 (merge sort uses 7).

## Chapter 2 · Insertion sort
Status: COMMISSIONED (2026-10-27)
Slug: ch2_insertion · ~9.5 min · Source: pp. 39–40 (§5.2), plus Lecture 2's recurrence table, p. 19
Goal: write `ins` and `insort`, trace them, say which cells `ins` copies or shares, and derive
its O(n²) comparisons on average (n²/4), with its best case (sorted, n − 1) and its worst
(reversed, n(n−1)/2).
Scenes:
- s1_hook · Hook (~45 s): title card "Part 2 · Insertion sort". Last time: no comparison sort
  can beat about n log₂ n comparisons, and we made 10,000 random numbers to race on. Today, the
  simplest contestant, which works the way you sort a hand of cards: pick up one card at a time
  and slot it into place (the card picture is beyond the notes). The hand of cards, then the
  chain.
- s2_ins · Inserting one item (~95 s): `ins` clause by clause. `[] -> [x]`. Then
  `y::ys -> if x <= y then x :: y :: ys else y :: ins x ys`: stop at the first item at least as
  big, otherwise keep y and carry on. Reply `val ins : 'a -> 'a list -> 'a list`, polymorphic
  through `<=` (L4 ch2). Trace `ins 4 [3; 5; 9]` ⇒ `3 :: ins 4 [5; 9]` ⇒ `3 :: 4 :: 5 :: [9]` ⇒
  `[3; 4; 5; 9]`, two comparisons. It assumes the list is already sorted: `ins 4 [9; 3]` is
  `[4; 9; 3]` (the writer verifies).
- s3_cells · What insert copies (~75 s): in memory, `ins 4 [3; 5; 9]` builds new cells for 3
  (copied on the way down), for 4, and for 5, because `y :: ys` is a fresh cell. It shares `[9]`.
  Checked: with `l = [3; 5; 9]` and `r = ins 4 l`, `List.tl (List.tl r) == List.tl l` is `false`,
  but `List.tl (List.tl (List.tl r)) == List.tl (List.tl l)` is `true`. It's the same single
  rebuilt cell as drop's `else x::xs` (L4 ch1). Inserting at position k copies k cells, so time
  and space are O(k); `ins 10 [3; 5; 9]` copies all of it.
- s4_insort · Sorting by inserting (~90 s): `insort`: `[] -> []`, `x::xs -> ins x (insort xs)`.
  Reply `val insort : 'a list -> 'a list`. Trace on the chain: `insort [3; 5; 9; 4; 7]` unfolds to
  `ins 3 (ins 5 (ins 9 (ins 4 (ins 7 []))))`. The inserts wait, as in L3's `nlength`, so the last
  item goes in first: `[7]`, `[4; 7]`, `[4; 7; 9]`, `[4; 5; 7; 9]`, `[3; 4; 5; 7; 9]`. The
  comparisons are 0 + 1 + 2 + 2 + 1 = 6. That's below ch1's 7: the bound is about the worst
  input, and this one is easy for insertion sort. The notes' summary: items are copied one at a
  time to the output, each into its right place, so the output is always in order. Also checked:
  `insort ["dog"; "cat"; "emu"]` ⇒ `["cat"; "dog"; "emu"]`.
- s5_cost · Counting the comparisons (~100 s): inserting into a sorted list of k items takes
  from 1 to k comparisons, about k/2 on random data (the notes' "n/2 on average"). Summed over the
  whole sort: (0 + 1 + … + (n−1))/2 ≈ n²/4, so O(n²). As a recurrence it's T(n+1) = T(n) + n,
  Lecture 2's `nsumsum` row (one-line refresher, closed form n(n−1)/2). Measured on `rs`:
  25,146,194 comparisons, against n²/4 = 25,000,000. That's 212 times ch1's floor of 118,458.
  Fill the scoreboard row: 25,146,194, and 174 s on the DECstation. Optional, beyond the notes:
  on a laptop today, in the toplevel, it takes under a second (0.6–0.8 s across runs), still more
  than a hundred times quicksort's time. Faster hardware magnifies the gap (Lecture 2).
- s6_bestworst · Best and worst inputs (~80 s, beyond the notes, all checked): already-sorted
  input stops each insert after one comparison, so n − 1 in all: `insort [3; 4; 5; 7; 9]` makes 4,
  and sorted `rs` makes 9,999, which is linear. Reversed input makes every insert walk the whole
  sorted part, n(n−1)/2 in all: `insort [9; 7; 5; 4; 3]` makes 10, and reversed `rs` makes
  49,995,000. Keep sorted input in mind: quicksort will find it hardest of all (ch4).
- s7_why · Why bother, and recap (~80 s): it's slow because of O(n²) comparisons and lots of
  copying, not because it's recursive. Iterative versions would be "to no purpose", like L4 ch1's
  iterative take. The notes call it nearly useless: 174 s, while the next-worst contestant takes
  1.4 s. It's worth knowing because it's easy to code and shows the concepts, and two efficient
  sorts, merge sort and heapsort, can be seen as refinements of it (merge sort's `merge`
  generalises `ins`, ch5). Recap. Next time: quicksort, divide and conquer. The end card shows
  ch3's opening picture.
Continuity: the chain, the scoreboard and the ch1 floor of 7 (for five items) and 118,458 (for
`rs`). The ConsChain copy/share colouring (TEAL "shared") matches L4 ch1 s5. ch3's hook picks up
"174 seconds".

## Chapter 3 · Quicksort
Status: planned, not commissioned
Slug: ch3_quicksort · ~9 min · Source: pp. 40–41 (§5.3, §5.4 up to the timing)
Goal: explain quicksort as divide and conquer, read the list code (singleton clause, local
`part` with two accumulators), and trace it.
Scenes:
- s1_hook · Hook (~45 s): title card "Part 3 · Quicksort". Last time, insertion sort took 174 s.
  Quicksort takes 0.74 s. What's the trick?
- s2_idea · Divide and conquer (~85 s): the notes' four steps. Choose a pivot a; divide the rest
  into those ≤ a and those > a; conquer by sorting each part recursively; combine by appending.
  Shown on the same five numbers with 5 first, `[5; 3; 9; 4; 7]`, so the pivot 5 splits them two
  and two (checked: 6 comparisons). Pivot YELLOW, the two parts labelled "≤ a" and "> a".
- s3_hoare · Hoare's idea (~60 s): invented by Sir Tony Hoare (1934–2026, per the notes; he died
  5 March 2026, and devised it in Moscow in 1959, per the Computer History Museum), who later
  worked at Microsoft Research, Cambridge. Divide and conquer is a basic design principle. The
  cleverest part was partitioning in place by exchanging array elements. It came before recursion
  was well known, and people found it extremely hard to understand. We use a list version, which
  copies but is much easier to follow.
- s4_code · The code (~105 s): clause by clause. `[] -> []`. `[x] -> [x]`, a new pattern for a
  list of exactly one element, which is already sorted (lists of up to five or so are often
  special-cased for speed). Then `a::bs` with the local `let rec part l r = function …`, needed
  inside because it uses a and calls `quick` (as L4's `allc` was local because it needed c).
  `[] -> (quick l) @ (a :: quick r)` combines; `x::xs` sends x left if `x <= a`, else right.
  `in part [] [] bs`. Reply `val quick : 'a list -> 'a list`.
- s5_part · Partitioning (~80 s): `part` on pivot 3 and `[5; 9; 4; 7]`: one comparison per item,
  so n − 1 to partition n items. Nothing waits, so it's iterative. The accumulators build their
  parts backwards (`r = [7; 4; 9; 5]`), which doesn't matter because each part is sorted next
  (L4 ch6's reversed solutions). Items equal to the pivot go left.
- s6_trace · Watching it run (~100 s): `quick [3; 5; 9; 4; 7]`. Pivot 3 sends everything right:
  `[] @ (3 :: quick [7; 4; 9; 5])`. Pivot 7 gives l = `[5; 4]` and r = `[9]`; pivot 5 gives `[4]`;
  then the appends rebuild `[4; 5]`, `[4; 5; 7; 9]`, `[3; 4; 5; 7; 9]`. That's 8 comparisons, one
  more than ch1's 7. The pivots form a tree. The first pivot was the smallest item, a lopsided
  split: hold that thought.
- s7_recap · Recap (~60 s): fill the scoreboard row (158,058 comparisons, 0.74 s). Recap. Next
  time: why it's fast on average, how it can be slow, and a version without append.
Continuity: the pivot tree drawn in s6 is ch4's recursion-tree picture, and ch4 reuses this trace
for `quik`.

## Chapter 4 · How good is quicksort?
Status: planned, not commissioned
Slug: ch4_quick_cost · ~10 min · Source: p. 41 (§5.4 cost), pp. 41–42 (§5.5), Lecture 2's table p. 19
Goal: derive quicksort's average O(n log n) with a recursion tree, explain its O(n²) worst case
on sorted input, and read the append-free `quik`.
Scenes:
- s1_hook · Hook (~45 s): last time, quicksort's code and 0.74 s. Why so fast, and what was that
  lopsided first split?
- s2_average · The average case (~120 s): random pivots split roughly in half, so T(1) = 1 and
  T(n) = 2T(n/2) + n. Lecture 2 only tabulated this, so derive it here with the recursion tree:
  level k has 2^k parts of size n/2^k, n work per level, log₂ n levels, so n log₂ n. For 10,000
  items, log₂ n ≈ 13.3, so perfect splits give 14 levels, the last partly filled (the real tree on
  `rs` is 27 deep), and n log₂ n ≈ 133,000; we measured 158,058 (the splits aren't perfect halves). The
  notes: "not hard to prove … n log n comparisons in the average case" (Aho, p. 94). It's about
  235 times faster than insertion sort (174 / 0.74).
- s3_worst · The worst case (~100 s): sorted or reverse-sorted input makes every pivot the
  smallest or largest, so one part is empty: T(n+1) = T(n) + n, which is O(n²) (Lecture 2's
  table again). Checked: `quick [3; 4; 5; 7; 9]` makes 10 comparisons, and sorted `rs` makes
  49,995,000. Almost-sorted input is nearly as bad. Insertion sort's best input is quicksort's
  worst (ch2 s6). Randomising the input makes the worst case highly unlikely.
- s4_quik · Without append (~105 s): the standard technique for eliminating `@`, an accumulator,
  as in L3's `rev_app`. `quik (xs, sorted)` returns xs sorted, in front of `sorted`. The code
  clause by clause, with `part` on triples; reply `val quik : 'a list * 'a list -> 'a list`,
  called as `quik (rs, [])`. The notes say it "reverses the elements of xs and prepends them",
  echoing `rev_app`, but it sorts them: `quik ([3; 5; 9; 4; 7], [100; 200])` ⇒
  `[3; 4; 5; 7; 9; 100; 200]`. Say so in one sentence.
- s5_order · Building from the right (~90 s): in `part`'s `[]` clause, `quik (r, sorted)` runs
  first, then a is consed on, then `quik (l, …)`, so the answer is built from its largest end.
  Trace on ch3's call tree: `quik ([5; 4], [7; 9])` ⇒ `[4; 5; 7; 9]`, then
  `quik ([], 3 :: …)` ⇒ `[3; 4; 5; 7; 9]`. Each item is consed onto the answer once, and nothing
  is appended.
- s6_speed · Was it worth it? (~75 s): the same comparisons (158,058 on `rs`) but no `@` copying,
  and the speedup is significant. The summary's 0.53 s appears to be this version's time (our
  reading; the notes don't say). An imperative quicksort in Pascal on arrays (Sedgewick) is only
  slightly faster, which is surprising since lists cost more than arrays. In realistic
  applications comparisons dominate, so those overheads matter even less.
- s7_recap · Recap (~60 s): recap. Next time: merging two sorted lists, and a sort that never
  splits badly. End card.
Continuity: the recursion tree from s2 is reused by ch5 for merge sort. The scoreboard gets
quicksort's 0.53 s here.

## Chapter 5 · Merging and merge sort
Status: planned, not commissioned
Slug: ch5_merge_sort · ~10 min · Source: pp. 42–43 (§5.6–5.7)
Goal: write `merge` and `tmergesort`, count merge's comparisons, and explain why merge sort's worst
case is O(n log n).
Scenes:
- s1_hook · Hook (~45 s): last time, quicksort's quadratic worst case. Can we guarantee n log n?
  L4 promised that merge sort splits its list with take and drop.
- s2_merge · Merging two sorted lists (~95 s): the code; reply
  `val merge : 'a list * 'a list -> 'a list`. Trace `merge ([3; 5], [4; 7; 9])` ⇒
  `[3; 4; 5; 7; 9]` with 3 comparisons, as a zipper.
- s3_mergecost · What merging costs (~85 s): at most m + n − 1 comparisons (each one places an
  item, and the last comes free; the notes also say "at most m + n"). Checked:
  `merge ([1; 2; 3], [4; 5; 6])` makes 3, and `merge ([1; 3; 5], [2; 4; 6])` makes 5. With
  n = 1 it degenerates to insertion (`merge ([5], [1; 2; 3; 4])`, 4 comparisons): much work for
  little gain. Equal lengths make it efficient. It's not iterative, and an iterative version
  wouldn't help, for the same reasons as append (L3).
- s4_tmerge · Merge sort (~95 s): the code; `k = List.length xs / 2`, `take k` and `drop k`
  (L4 ch1 s7's exact shot, `[3; 5]` and `[9; 4; 7]`). It divides by counting, not by pivot, and
  the work moves from dividing to combining. It's seldom used with arrays, which make it hard to
  code, but it's natural for lists.
- s5_trace · Watching it run (~100 s): `tmergesort [3; 5; 9; 4; 7]`: split, recurse, and merge
  `[3; 5]` with `[4; 7; 9]`. That's 7 comparisons, exactly ch1's floor for five items.
- s6_cost · Never a bad split (~90 s): take and drop always halve (they differ by at most one), so
  T(n) = 2T(n/2) + n always, on ch4's tree, and the worst case is O(n log n). Measured: 120,392 on
  `rs`, within 2% of the floor of 118,458; 64,608 sorted; 69,008 reversed. Scoreboard: 1.4 s.
  Quicksort is nearly 3 times as fast: merge sort is safe but slower.
- s7_bottomup · Bottom-up, and recap (~85 s): start from one-item lists and merge neighbours until
  one is left. A refinement starts from the runs already in the input, increasing or decreasing.
  Recap. Next time: which sort is best, and a sort that uses no comparisons at all.
Continuity: the zipper picture returns in ch7 (bubble sort's passes).

## Chapter 6 · Which sort? And exercises
Status: planned, not commissioned
Slug: ch6_summary_exercises · ~8.5 min · Source: pp. 43–44 (§5.8, exercises 5.1–5.4)
Goal: compare the three sorts, say why radix sort escapes the n log n bound, and start the four
exercises from hints.
Scenes:
- s1_hook · Hook (~40 s): last time, merge sort: always n log n, but slower. So which is best?
- s2_summary · The full scoreboard (~105 s): optimal is O(n log n). Insertion sort: simple but
  quadratic, 174 s. Quicksort: fast on average, quadratic at worst, 0.53 s. Merge sort: optimal
  in theory, often slower, 1.4 s. Add a "sorted input" column: 9,999 / 49,995,000 / 64,608. Match
  the algorithm to the application. For large n, O(n²) is catastrophic (Lecture 2's table: in an
  hour, 1,897 items at n² against 204,095 at n log n).
- s3_radix · Sorting without comparing (~105 s): radix sort orders many small integers by their
  digits in O(n). It doesn't contradict ch1, because it never compares two items. Show buckets,
  last digit first (writer checks): `[53; 19; 51; 37; 12; 34]` ⇒ `[51; 12; 53; 34; 37; 19]` ⇒
  `[12; 19; 34; 37; 51; 53]`. It's linear only if the largest integer is fixed in advance, and as
  n grows, more and more items are equal. A simple special case. Many other sorts exist.
- s4_hints1 · Exercises 5.1–5.2, selection sort (~85 s): card kit from L4 ch6 s5 (and L3). Hints:
  how many comparisons does finding the minimum of k items take, and does the input's order
  change that? Write the recurrence. For the code, return the minimum and the rest at once (two
  results, like unzip).
- s5_hints2 · Exercises 5.3–5.4, bubble sort (~85 s): hints: what does one pass guarantee about
  the largest item? How many passes at most? What happens on sorted input? For the code, a pass
  over `x::y::ys` that also reports whether it swapped. Test it on a list with repeated items.
- s6_recap · The whole lecture (~90 s): recap of all six chapters. Next lecture: Datatypes and
  Trees (our own types, exceptions, making change once more, binary trees, which lead to binary
  search trees in Lecture 7). The bonus chapter has the solutions. End card.
Continuity: the exercise cards are reused verbatim in ch7.

## Chapter 7 · Bonus: solutions to the exercises
Status: planned, not commissioned
Slug: ch7_solutions · ~8.5 min (bonus) · Source: p. 44, drawing on pp. 37–43
Goal: worked solutions to 5.1–5.4 with recurrences, code, comparison counts and a tempting bug.
Scenes:
- s1_intro · Spoiler warning (~40 s): the four cards; try them first.
- s2_selcost · 5.1 Selection sort's cost (~95 s): the minimum of k items takes k − 1 comparisons
  whatever the order, so T(n) = T(n−1) + (n−1), n(n−1)/2: O(n²) in every case. Checked: 10
  comparisons on five items whether random, sorted or reversed (insertion sort makes 4 on sorted).
- s3_selcode · 5.2 Selection sort in OCaml (~110 s): a `select m acc` helper returns
  `(minimum, rest)`, and `selsort` conses the minimum onto the sorted rest. Checked:
  `[3; 5; 9; 4; 7]` ⇒ `[3; 4; 5; 7; 9]`, `[3; 5; 3; 1; 5]` ⇒ `[1; 3; 3; 5; 5]`. Pitfall: removing
  the minimum by value loses duplicates (the writer builds and checks a wrong version).
- s4_bubcost · 5.3 Bubble sort's cost (~100 s): a pass makes n − 1 comparisons and carries the
  largest unsettled item to its place, so at most n − 1 swapping passes plus one quiet one: O(n²)
  in the worst and average case. On sorted input one pass suffices: O(n). Checked on five items:
  chain 12, sorted 4, reversed 20.
- s5_bubcode · 5.4 Bubble sort in OCaml (~110 s): `bpass` returns `(list, swapped)`, and `bubble`
  repeats until a pass swaps nothing. Checked on the chain and on duplicates. Pitfall (checked):
  swapping when `y <= x` exchanges equal neighbours forever, so `[3; 5; 3; 1; 5]` never finishes.
  Swap only when `x > y`.
- s6_recap · Recap (~50 s): five sorts side by side, three O(n²) and two O(n log n). Next
  lecture: Datatypes and Trees. "See you in the next lecture." End card.
Continuity: card kit and colours as in ch6. The closing line matches L3's and L4's bonuses.

## Decisions
- Commissioned now: ch1–2 (the user's "a couple chapters"); ch3–7 are planned only. Together
  ch1–2 cover the notes' intro and §5.1–5.2: why sort, the lower bound, the test data and
  insertion sort. That's a natural stopping point, before divide and conquer starts.
- 7 chapters (6 + bonus), ~65 min. The notes' L5 prose is 2,205 words, 84% of L4's 2,629 (63 min
  planned, 65 voiced), with as much code (56 lines vs 51). It's denser in theory, though: a
  lower-bound proof, two recurrences actually solved, and average vs worst cases. The split
  follows the notes: intro + §5.1 | §5.2 | §5.3–5.4 | §5.4's cost + §5.5 | §5.6–5.7 | §5.8 + hints
  | solutions. The one cut inside a section: §5.4's cost paragraphs move to ch4, so ch3 is
  "what quicksort does" and ch4 "how good it is", each ~9–10 min. Merged, they'd make one
  ~17 min video.
- To shorten: drop the beyond-the-notes extras (insertion sort's best and worst cases, the log₂ n!
  sandwich, modern timings) to save ~3 min, or merge ch1's s4 into s2.
- Beyond the notes, all checked: the comparison counts (a counting `<=`), `ins`'s one rebuilt cell,
  insertion sort's best and worst cases, the sandwich bound, Park–Miller's check value, Hoare's
  dates, the radix example (by hand), and the bubble-sort duplicates bug. Each clarifies a claim
  in the notes; none adds a topic.
- Slips in the notes, handled: `quik` "reverses" its input (it sorts, ch4 says so). Quicksort is
  0.74 s in §5.4 but 0.53 s in the summary; we read 0.53 as `quik`'s time and say it's our
  reading. Merge's bound is given as both m + n − 1 and m + n; we use m + n − 1. The bound's
  "log" is log₂, so we write it.
- L4 ch2 promised "binary search, coming next lecture". The notes give only its idea, so ch1 steps
  through it on L4's own example and points to binary search trees (Lecture 7) for code.
- Exercises follow COURSE.md: hints at the end of ch6 (the last core chapter), worked solutions in
  a bonus ch7.
- Left out: nothing from pp. 37–44. Heapsort and binary-search code are named only, as in the
  notes; the 10,000-number printout is shown, not read.
