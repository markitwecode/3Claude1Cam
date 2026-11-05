# More on Lists: plan

Request: "can you make the videos for lecture 4 of focs?" (2026-10-25). Audience: a Cambridge
first-year studying FoCS who has watched our Lecture 3 videos (lists, cons cells, patterns,
`'a`, accumulators, append, `nrev`/`rev_app`, strings) and knows Lectures 1–2 (recursion,
iteration, O-notation incl. O(log n), `let x = e1 in e2`). Sources: FoCS 2026-27 notes v1.8
(`../source/focs-202627-v1.8.pdf`), pp. 30–36; forward links to p. 37, p. 43 and p. 49.
Total: 7 chapters (6 + a bonus), ~63 min of narration.

All replies and results quoted below were checked in OCaml 5.4.1. Script-writers still run
every line themselves.

## Chapter 1 · Take and drop
Slug: ch1_take_drop · ~8 min · Source: pp. 30–31 (§4.1)
Goal: write `take` and `drop`, trace them, say which cells each one copies or shares, and derive
their costs (both O(i) time; `take` O(i) space, `drop` O(1)).
Scenes:
- s1_hook · Hook (~45 s): title card "Part 1 · Take and drop". One sentence on Lecture 3 (build,
  match, length, append, reverse). This lecture: more list utilities, more patterns of recursion,
  and at the end a program that makes change. The question: how do you cut a list in two at
  position i? The chain 3 → 5 → 9 → 4 → 7 → [] with a GOLD cut after cell 2 and a "?" on each side.
- s2_take · Taking the first i (~80 s): the notes' diagram (x₀ … x_{i−1} braced "take i xs",
  x_i … x_{n−1} braced "drop i xs"). `take`'s code clause by clause. `function` supplies the list
  as an unnamed second argument, as in L3's `addlen`. Reply `val take : int -> 'a list -> 'a list`.
- s3_trace · Watching take run (~60 s): `take 2 [3; 5; 9; 4; 7]` ⇒ `3 :: take 1 [5; 9; 4; 7]` ⇒
  `3 :: 5 :: take 0 [9; 4; 7]` ⇒ `3 :: 5 :: []` ⇒ `[3; 5]`. The conses wait, as in append, so
  it's not iterative.
- s4_drop · Dropping the first i (~70 s): `drop`'s code. Same shape, but nothing waits around
  `drop (i-1) xs`, so it's iterative. The `else x::xs` clause. Trace `drop 2 …` ⇒ `[9; 4; 7]`.
- s5_cells · Copied or shared (~80 s): in memory, `take` builds new cells for 3 and 5, a copy.
  `drop`'s answer reuses the original chain. Precise point: `else x::xs` builds ONE new cell (for
  9) on top of the shared rest. So `drop 2 l == List.tl (List.tl l)` is `false`, but their tails
  are `==`. Sharing is safe because lists never change (L3). `take 2 l @ drop 2 l` gives back
  `[3; 5; 9; 4; 7]`.
- s6_cost · What they cost (~80 s): `take` is O(i) time and O(i) space, for the waiting conses
  and the copy itself. An iterative `take` wouldn't help: it must copy i elements anyway, and an
  accumulator builds them backwards and then needs a reverse (L3 ch4's caveat). `drop` is O(i)
  time and O(1) space. Both are O(i), but skipping beats copying: drop's constant factor is
  smaller, and O-notation hides constant factors (Lecture 2).
- s7_edges · Off the end, and recap (~65 s): `take 10 [3; 5; 9]` = `[3; 5; 9]` (a copy) and
  `drop 10 [3; 5; 9]` = `[]`. With i ≤ 0, `take` gives `[]` and `drop` gives the whole list. The
  `[]` clause means no exception. Use: splitting a collection into equal parts for recursive
  processing (next lecture's merge sort splits with `take`/`drop`, p. 43). Recap. Next time: is
  this element in the list?
Continuity: the running chain 3 → 5 → 9 → 4 → 7 → [] (L3's 3 → 5 → 9, extended) and ConsChain
from `engine/lib/style.py` with L3's palette. ch2 searches this same chain. The waiting-conses
trace style matches L3 ch4's append trace.

## Chapter 2 · Searching a list
Slug: ch2_search · ~8 min · Source: pp. 31–32 (§4.2–4.3)
Goal: explain linear search and its O(n) cost against O(log n) and O(1), write `member`, and say
what OCaml's polymorphic equality can and can't compare.
Scenes:
- s1_hook · Hook (~45 s): last time, take and drop. Is 9 in this list? A program can only look,
  one cell at a time. A GOLD pointer on the ch1 chain.
- s2_linear · One at a time (~70 s): linear search compares x with each element in turn. If x is
  there, it takes n/2 comparisons on average and n at worst; if it isn't, all n. That's O(n).
  A comparison counter on the chain: looking for 9 takes 3 comparisons; looking for 6 takes 5,
  then nil.
- s3_faster · Faster ways to search (~75 s): ordered data gives O(log n) (the halving refresher
  from Lecture 2: a million sorted items in about 20 comparisons; binary search proper comes
  next lecture, and it needs arrays or trees, not lists). Indexing gives O(1), e.g. a hash
  table, "as long as machine limits aren't exceeded". That's exponentially better, and it's why
  web search engines can work. Linear search still earns its place: it's simple, general (no
  order needed) and fine for small collections, and it's where better algorithms start.
- s4_member · member (~85 s): the code. Trace `member 9 [3; 5; 9; 4; 7]` ⇒ `true` and
  `member 6 …` ⇒ `false`. Iterative, so O(n) time and O(1) space. Reply
  `val member : 'a -> 'a list -> bool`: polymorphic, yet it tests `x = y`. How?
- s5_equality · Polymorphic equality (~80 s): `=`, `<`, `<=`, `>`, `>=` work at any type by
  inspecting the structure of values, in a consistent order. That's fine for ints, strings,
  bools, and tuples or lists of them: `[1; 2] = [1; 2]`, `[1; 2] < [1; 3]` (element by element,
  like strings in L3 ch5), `("b", 1) > ("a", 9)` (the first parts decide), `true > false`,
  `member "dog" ["cat"; "dog"]`, `member [1; 2] [[3]; [1; 2]]`. All are `true`.
- s6_limits · Where equality stops (~80 s): functions. `let double n = 2 * n` and
  `let twice n = n + n`, then `double = twice` type-checks, but at run time gives
  `Exception: Invalid_argument "compare: functional value".` So does `double = double`, and so
  does `member double [twice; double]`, while `member double []` is just `false`. Functions as
  values come in a later lecture. Cyclic structures: the comparison may never finish (say it in
  words; cyclic lists aren't taught). The feature is contentious: easy in small programs,
  dangerous in large systems, where most OCaml users avoid it in important code and write
  explicit compare functions (higher-order functions, later). It's fine for us now.
- s7_recap · Recap (~45 s): recap. Next time: lists of pairs, a telephone directory.
Continuity: the same chain as ch1. L3 ch6's "they might raise an exception, but never mix up
their types" squares with `double = twice` (an exception, not a type error), so say so in one
sentence. The directory teaser leads into ch3.

## Chapter 3 · Lists of pairs: zip and unzip
Slug: ch3_zip_unzip · ~10 min · Source: pp. 32–33 (§4.4–4.5)
Goal: write `zip` with a wildcard and `unzip` with a local pattern binding, read their types, and
compare three ways to unzip (`let`, `conspair`, `revUnzip`).
Scenes:
- s1_hook · Hook (~45 s): last time, member and equality. A list of names and a list of phone
  numbers, in matching order. How do you pair them up, and how do you split pairs back apart?
  The notes' picture: [x₁ … xₙ], [y₁ … yₙ] ↦ [(x₁, y₁) … (xₙ, yₙ)].
- s2_zip · Zip (~90 s): match the pair `xs, ys` at once (as append did, L3 ch4). The first
  clause is `(x::xs, y::ys) -> (x, y) :: zip xs ys`. The wildcard `_` matches anything: a
  variable like `p` would also work, but `_` says this clause ignores its argument. Reply
  `'a list -> 'b list -> ('a * 'b) list`, with two type variables, as for `fst` (L3 ch2).
- s3_order · Uneven lists, and clause order (~80 s): trace zip on the directory. With unequal
  lengths it discards the surplus: `zip [1; 2; 3] ["a"; "b"]` = `[(1, "a"); (2, "b")]`. Clauses
  are tried in order, so `_` only ever sees arguments where at least one list is empty.
  Pitfall: put `_` first and every call returns `[]`, with
  `Warning 11 [redundant-case]: this match case is unused.`
- s4_pairs · What pairs are for (~50 s): a list of pairs associates each xᵢ with yᵢ, like a
  telephone directory. Linear search (ch2) finds a number from a name, or a name from a number,
  "very slowly". Pairs can also come from applying a function to each element of another list.
- s5_unzip · Unzip: two results at once (~110 s): building two results is awkward with
  recursion. The code uses `let xs, ys = unzip pairs in (x::xs, y::ys)`. One clip of refresher:
  Lecture 2's `let x = e1 in e2` is an expression and can go wherever an expression goes
  (parenthesised if needed). New: `let P = E` matches the pattern P against E's value and binds
  every variable in it. Trace on three pairs: down to `[]` ⇒ `([], [])`, then one cons onto
  each list on the way back.
- s6_types · Mirror images (~45 s): the two types side by side. zip takes two lists to a list of
  pairs, and unzip takes a list of pairs to a pair of lists. Unzip undoes zip, except for the
  surplus: `unzip (zip [1; 2; 3] ["a"; "b"])` = `([1; 2], ["a"; "b"])`.
- s7_conspair · Without the let (~70 s): `let conspair ((x, y), (xs, ys)) = (x::xs, y::ys)` puts
  the pattern right in the argument. Then `unzip` = `conspair (xy, unzip pairs)`: the same
  computation, possibly clearer, but not every local binding can be removed so easily. Reply
  `('a * 'b) * ('a list * 'b list) -> 'a list * 'b list` (long, so let it breathe).
- s8_revunzip · Iterative, and backwards (~110 s): `revUnzip` takes a triple
  `(pairs, xs, ys)`. Iteration can build several results at once, in different argument
  positions. The trace comes out reversed, `([3; 2; 1], ["c"; "b"; "a"])`; reverse the input
  first to fix it. Its total cost probably exceeds unzip's despite the iteration (L3 ch4: an
  accumulator that forces an extra reversal can lose). Recap. Next time: making change.
Continuity: one running directory of three short names and three numbers (the writer picks them)
through s1–s5, with `[1; 2; 3]` / `["a"; "b"; "c"]` where the notes use them. Pairs are drawn as
ConsChain cells holding a tuple. Function names YELLOW in definitions, types GREEN, as in L3.

## Chapter 4 · Making change
Slug: ch4_change · ~8 min · Source: pp. 33–34 (§4.6)
Goal: write the greedy `change`, trace it, explain its zero base case and its exception, and show
an input where greedy fails although change exists.
Scenes:
- s1_hook · Hook (~45 s): last time, zip and unzip. A till with unlimited 50, 20, 10, 5, 2 and
  1p coins, and you owe 43p. Most people grab the biggest coin that fits. Let's write that.
- s2_idea · The plan (~65 s): the till is a list in descending order, so the largest coin is the
  head, the easiest element to reach (L3's cells). Three observations: change for zero is no
  coins; otherwise try the largest coin, and if it fits, use it and reduce the amount; exclude
  coins that are too large.
- s3_code · The code (~100 s), clause by clause: match on the pair `till, amt`. `_, 0 -> []`
  puts a constant in a pattern, next to ch3's wildcard. `[], _ -> raise (Failure "no more
  coins!")` is our first `raise`: the program signals failure itself, where L3's match failure
  came from OCaml (exceptions properly in a later lecture). In `c::till, amt -> if amt < c then
  change till amt else c :: change (c::till) (amt - c)`, the new `till` is the rest (a new name,
  as in L3), and `c::till` puts c back so it can be used again. Reply
  `val change : int list -> int -> int list`.
- s4_trace · Making 43p (~80 s): `change [50; 20; 10; 5; 2; 1] 43` ⇒ `[20; 20; 2; 1]`: skip 50,
  use 20 twice, skip 20, 10 and 5, use 2, skip 2, use 1, reach 0. The conses wait, as in take.
  (99p gives `[50; 20; 20; 5; 2; 2]`.)
- s5_zero · Why zero (~60 s): there are two ways to stop, amt = 0 (success) or the till running
  out (failure). Nobody asks for change for zero, but it's the simplest way to make the
  algorithm terminate: most procedures are simplest when their base case does nothing. A base
  case of one instead of zero is often a sign of a novice.
- s6_greedy · Where greedy fails (~85 s): greedy means largest first, never reconsidering. Coins
  `[5; 2]`, amount 6: 5 fits, leaving 1; 5 and 2 are too big; the till is empty ⇒
  `Exception: Failure "no more coins!".` Yet 2 + 2 + 2 = 6. Greedy algorithms are often
  effective (UK coins always work), but not here.
- s7_recap · Recap (~45 s): recap. Next time: find every way, so one dead end can't stop us.
Continuity: coins as GOLD discs labelled with their value, reused in ch5–ch7. The UK till
`[50; 20; 10; 5; 2; 1]` and the notes' failing case (`[5; 2]`, 6) carry into ch5.

## Chapter 5 · Every way to make change
Slug: ch5_all_ways · ~9 min · Source: pp. 34–35 (§4.7)
Goal: explain the all-ways `change`: its list-of-lists result, `[[]]` versus `[]`, the use-or-skip
split, and the local `allc`.
Scenes:
- s1_hook · Hook (~45 s): last time, greedy took the 5 and got stuck on 6 = 2 + 2 + 2. New idea:
  return all the ways, not one. ch4's stuck trace, then a branching tree's outline.
- s2_answers · A list of answers (~75 s): the result type is now `int list list`, a list of
  solutions. Zero has exactly one way, using no coins, so `change … 0` = `[[]]` (success). An
  empty till with money left has no ways, `[]` (failure). So this version never raises. Draw it
  as a box holding an empty box vs an empty box. Verified: `change [5; 2] 0` = `[[]]`,
  `change [5; 2] 1` = `[]`.
- s3_choices · Use it, or skip it (~95 s): at each coin c there are two sources of solutions:
  use c (if amt ≥ c) and make change for amt − c, or remove c from consideration. The tree for
  `change [5; 2] 6`: "use 5" reaches a dead end at 1; "skip 5" makes 6 from 2s ⇒ `[[2; 2; 2]]`,
  the answer greedy missed.
- s4_code · The code (~90 s): In [72] clause by clause: `_, 0 -> [ [] ]`, `[], _ -> []`,
  `if amt < c then change till amt` (too big, so skip only), else the two sources joined with
  `@`. Reply `val change : int list -> int -> int list list`.
- s5_allc · Putting c on every answer (~85 s): `allc` adds c to the front of every solution:
  with c = 2, `[[2]; [1; 1]]` becomes `[[2; 2]; [2; 1; 1]]`. It's local because it needs c.
  Pitfall: plain `c :: change …` would try to add c as a new solution, not to each one (int vs
  int list, a type error). Naming: `cs` is a list of coins, `css` a list of such lists.
- s6_trace · Three ways to make 4 (~100 s): `change [2; 1] 4` ⇒ `[[2; 2]; [2; 1; 1]; [1; 1; 1; 1]]`:
  "use 2" gives `change [2; 1] 2` = `[[2]; [1; 1]]`, then allc ⇒ `[[2; 2]; [2; 1; 1]]`; "skip 2"
  gives `change [1] 4` = `[[1; 1; 1; 1]]`; `@` joins them. Also: `change [5; 2; 1] 6` has five
  ways.
- s7_recap · Recap (~50 s): the notes call this program a challenge, and finding it hard is
  normal. Making change returns with exceptions in a later lecture (p. 49). Recap. Next time:
  allc and `@` copy a lot; can accumulators help?
Continuity: the tree layout (nodes "amount, till", edges "use c" / "skip c") is reused in ch6's
trace. `[2; 1]` for 4 is the multi-answer example for ch5–ch6; `[5; 2]` for 6 links back to ch4.

## Chapter 6 · Faster, and exercises
Slug: ch6_faster_exercises · ~9.5 min · Source: p. 35 (§4.8), p. 36 (exercises 4.1–4.6)
Goal: explain how two accumulating parameters speed up all-ways change, say what stepwise
refinement is, and start the six exercises from hints.
Scenes:
- s1_hook · Hook (~40 s): last time, every way to make change, built with allc and `@`, which
  both copy. Accumulators fixed length and reverse in Lecture 3. Can they help here?
- s2_accs · Two accumulators (~100 s): In [73]. `chg` holds the coins chosen so far on this path,
  `chgs` the solutions found so far. Amount 0 ⇒ `chg::chgs` (record a solution); empty till ⇒
  `chgs`; `if amt < 0 then chgs`. That's `amt < 0`, not `amt < c`: an overshoot is caught one
  call later. Otherwise use c (`amt - c`, `c::chg`), passing in the result of skipping c as the
  `chgs`. Reply with four arguments; call it with `[] []`.
- s3_trace · Following the accumulators (~90 s): on ch5's tree, `change [2; 1] 4 [] []` ⇒
  `[[2; 2]; [1; 1; 2]; [1; 1; 1; 1]]`. The skip branch is evaluated first, and its solutions
  become the use branch's `chgs`. Each solution comes out reversed (`[1; 1; 2]`, not
  `[2; 1; 1]`) because `chg` is built by consing, as in rev_app; coin order doesn't matter here.
- s4_refine · Faster, still slow, and stepwise refinement (~95 s): one `c::chg` replaces many
  allc conses, and `chgs` removes the append, so it runs several times faster (we measured
  ~2.6× in the toplevel; say "several times"). It's still slow, because the number of solutions
  grows rapidly: 4366 ways to make 99p from 50, 20, 10, 5, 2, 1. Stepwise refinement means
  three versions: write the simplest first, add requirements one at a time, efficiency last.
  Even a discarded version teaches you the task.
- s5_hints1 · Exercises 4.1–4.3 (~85 s): one card per exercise, with a hint and a pause.
  4.1: set union with member (`[4; 7; 1]`, `[6; 4; 7]` ⇒ `[1; 6; 4; 7]`, in any order); hint:
  walk the first list, keep what the second lacks. 4.2: non-negatives and negatives; hint: two
  results at once, like unzip. 4.3: zip with `([], [])` instead of `_`; hint: unequal lengths,
  and read OCaml's warning.
- s6_hints2 · Exercises 4.4–4.6 (~85 s): 4.4: what the change functions assume about till and
  amt; hint: a coin of zero, a negative amount, coins out of order, a repeated coin. 4.5: two
  coin values give O(n) ways; hint: fix how many of the larger coin. 4.6:
  `f : 'a * 'b -> 'b * 'a`, `g : 'a -> 'a list`; hint: L3's id, where a function that knows
  nothing about alpha can't invent one.
- s7_recap · The whole lecture (~75 s): recap (take/drop, searching and equality, zip/unzip and
  `let` patterns, change three ways, stepwise refinement). Next lecture: Sorting (sorted data
  allows fast search; merge sort splits with take and drop). The bonus chapter has the
  solutions. End card (~8 s).
Continuity: the exercise cards copy L3's kit (BigCard, HeroCard, pause_tag in
`projects/focs/l03-lists/scenes/ch5_s6_sumlast.py`) into s5's file, and ch7 imports from there.
The card text is reused verbatim in ch7.

## Chapter 7 · Bonus: solutions to the exercises
Slug: ch7_solutions · ~10.5 min (bonus) · Source: p. 36, drawing on pp. 30–35
Goal: worked solutions to 4.1–4.6, with traces, costs and tempting wrong answers.
Scenes:
- s1_intro · Spoiler warning (~40 s): the six cards from ch6 in a row; try them first.
- s2_union · 4.1 Union (~90 s): `union xs ys`: `[] -> ys`, else skip x if `member x ys`, else
  `x :: union xs ys` ⇒ `[1; 6; 4; 7]`, exactly the notes' answer. Cost: m·n comparisons. Consing
  onto ys instead is iterative and also gives `[1; 6; 4; 7]`. Both trust the inputs to be sets.
- s3_signs · 4.2 Two lists by sign (~85 s): unzip's shape, `let (ps, ns) = … xs in if x >= 0
  then (x::ps, ns) else (ps, x::ns)`. `[3; -1; 0; -5; 2]` ⇒ `([3; 0; 2], [-1; -5])`. Pitfall:
  `x > 0` sends 0 the wrong way. Two accumulators reverse both, like revUnzip.
- s4_zip · 4.3 A stricter zip (~65 s): `Warning 8 [partial-match]: this pattern-matching is not
  exhaustive. Here is an example of a case that is not matched: (x::xs, [])`. Equal lengths
  behave the same; unequal ones raise `Match_failure` instead of dropping the surplus. Same
  type. Strict vs forgiving is a design choice.
- s5_assume · 4.4 Hidden assumptions (~100 s): coins are positive, the till is descending, no
  coin repeats, and amt ≥ 0. Verified: a zero coin never terminates (greedy and all-ways
  overflow the stack; the accumulator version's use-call is a tail call, so it just runs on
  with `chg` growing, past our 10 s timeout). A negative coin overflows greedy's stack. An
  ascending till still makes change, but small coins first (`change [1; 2; 5] 9` = nine 1s),
  and all-ways gives the same solutions in another order. A repeated coin repeats solutions (`[5; 2; 1; 2]` for 4 lists
  `[2; 2]` three times). A negative amount: greedy raises Failure, and the all-ways versions
  return `[]`.
- s6_count · 4.5 Counting the ways (~120 s): with two coins a > b, a solution is fixed by how
  many a's (0 to n/a), and the rest must be b's in at most one way, so ≤ n/a + 1 ways: O(n).
  Three coins: a two-coin problem for each count of the largest, O(n²). With k coins,
  O(n^(k−1)). Verified counts for n = 10, 20, 40, 80(, 160): `[5; 2]` 2, 3, 5, 9, 17 (linear);
  `[5; 2; 1]` 10, 29, 97, 353 (heading for ×4 per doubling); `[10; 5; 2; 1]` 11, 40, 195, 1173
  (heading for ×8). Six UK coins make it O(n⁵), hence 4366 for 99.
- s7_types · 4.6 What the types force (~85 s): f can only move what it's given, so
  `f (1, true)` = `(true, 1)`. `g 0` is a list holding only 0s (`[]`, `[0]`, `[0; 0]` …), and
  the type can't tell how many. Either could loop or raise instead, as L3's `loop` showed, but
  the exercise says they return.
- s8_recap · Recap (~45 s): one row per exercise. Next lecture: Sorting. End card.
Continuity: card kit and colours as ch6. The ch4–ch6 change code is shown unchanged when 4.4/4.5
refer to it. The recap's closing line matches L3's bonus ("See you in the next lecture").

## Decisions
- 7 chapters, ~63 min. L4's notes have 93% of L3's prose (2629 vs 2812 words) but more code (60
  vs 53 lines) and six exercises to L3's five (one a proof). L3 became 59 min, which the user
  approved. Each block below fills 8–10 min on its own, and any merge would make a 15+ min video.
  So the split follows the notes' sections: §4.1 | §4.2–4.3 | §4.4–4.5 | §4.6 | §4.7 | §4.8 +
  hints | solutions.
- If you'd rather have 6 videos: merge ch1 and ch2 into one ~11 min chapter (lighter traces,
  shorter equality examples). That saves ~5 min and one chapter's animation.
- Making change gets three chapters, one per version (greedy, all ways, faster), because the
  notes flag §4.7–4.8 as "challenges". Each version is traced on a small input, on a shared tree.
- Exercises follow L3 and COURSE.md: hints at the end of ch6 (the last core chapter), worked
  solutions in a bonus ch7.
- Order: the notes' own. No reordering needed.
- Beyond the notes, all verified: drop's one rebuilt cell (ch1), `double = twice` instead of
  anonymous functions, which aren't taught yet (ch2), the redundant-case warning (ch3), the
  faster version's reversed solutions (ch6), and the failure modes and counts in ch7. Each one
  clarifies a claim in the notes; none adds a topic.
- Left out: nothing from pp. 30–36. Binary search, hash tables and exceptions are named only as
  "later", as the notes do.
