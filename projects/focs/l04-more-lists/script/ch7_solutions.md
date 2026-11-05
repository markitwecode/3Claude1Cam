# Chapter 7 · Bonus: solutions to the exercises

Lecture 4 (More on Lists), part 7 of 7, the bonus chapter (optional, for after the exercises). Source: FoCS 2026-27 notes v1.8, p. 36 (Exercises 4.1–4.6), drawing on pp. 30–35.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Spoiler warning (ch7_s1_intro)

> Title card (lib.titles): "More on Lists", "Foundations of Computer Science · Lecture 4", part line "Bonus · Solutions to the exercises" (L3's bonus wording). On {warn}, as in L3's ch6_s1_intro: title and rule lift away, the course and part lines rise and stay as the header, and a GOLD "SPOILERS AHEAD" banner appears with a big pause icon (‖), held through the pause.
> On {cards}: the six exercise cards from ch6 in a row, filling the frame, as ch6's recap left them ("Solutions: bonus chapter"). Import the kit (BigCard, HeroCard, pause_tag) from `scenes/ch6_s5_hints1.py`; card text verbatim as ch6 s5/s6, quoted per scene below. Titles: "4.1 Set union", "4.2 Split by sign", "4.3 Another zip", "4.4 Hidden assumptions", "4.5 Counting the ways", "4.6 What the types force". If six don't fit legibly in one row, use two rows of three.
> On {ritual}, three small steps appear under the first card: "pause ‖", "solve", "trace and cost". On {wrong}, a RED ✗ card slides in beside the row: "tempting wrong answers".
> Each later scene opens with its card enlarged from this row (TransformFromCopy) plus the ‖ icon, held still through the pause.
> All OCaml in this chapter was checked in OCaml 5.4.1 (`ocaml < file.ml`). Replies quoted below are the exact toplevel output for the code as laid out here. Code names YELLOW in definitions, types GREEN, `'a`/`'b` PINK, numbers and costs GOLD, coins as ch4's GOLD discs.

[c7.intro.1] {title} This bonus chapter for lecture four has worked solutions to the six exercises at the end of the notes. {pause} {warn} Everything from here on is a spoiler. If you'd like to try them first, stop the video now, and have a go.

[c7.intro.2] {cards} We'll take them in order. {ritual} Each one starts with the question, and a moment to pause. Then we solve it, trace it on a small example, and work out what it costs. {wrong} We'll also meet some tempting wrong answers, which teach as much as the right ones.

## Scene 2 · Exercise 4.1: set union (ch7_s2_union)

> Card 4.1 "Set union" (ch6's text): "Sets are lists with no repeats. Using member, code set union." Example `union [4; 7; 1] [6; 4; 7]` ⇒ `[1; 6; 4; 7]`, tag "any order"; + ‖. Hold through the pause. Then ch2's `member` (In [63], verbatim) sits dimmed at the top right for the whole scene, its name YELLOW.
> Wrong shortcut ({wrong}): `[4; 7; 1] @ [6; 4; 7]` → `- : int list = [4; 7; 1; 6; 4; 7]`. On {repeats} the second 4 and 7 turn RED, with a RED ✗.
> Code (hero, left), one clause lighting per beat ({base}, {skip}, {keep}): `let rec union xs ys =` / `  match xs with` / `  | [] -> ys` / `  | x::xs -> if member x ys then union xs ys` / `             else x :: union xs ys` → on {type} `val union : 'a list -> 'a list -> 'a list = <fun>`.
> Trace ({trace}) on two ConsChains, xs = 4 → 7 → 1 → [] above, ys = 6 → 4 → 7 → [] below. A YELLOW marker steps along xs. On {s1} and {s2} a member scan sweeps ys and stops on the matching cell (GREEN tick; that xs cell goes DIM, "skip"). On {s3} the scan runs past all three ys cells, and 1 drops down as a new BLUE cell. On {s4} the `[] -> ys` clause flashes and the new cell's arrow points into the ORIGINAL ys chain. On {result}: `union [4; 7; 1] [6; 4; 7]` → `- : int list = [1; 6; 4; 7]`. On {shared}, ys is tagged TEAL "shared", as for append in L3 ch4 (verified: with `let ys = [6; 4; 7]`, `List.tl (union [4; 7; 1] ys) == ys` gives `- : bool = true`).
> Cost ({cost}, {mn}): a GOLD grid, rows = the m elements of xs, columns = the n elements of ys, one square filled per comparison actually made here (2, then 3, then 3: 8 of the 9). On {total}: "≤ m·n comparisons", "time O(m·n)" in GOLD.
> Iterative variant ({acc}), beside union, the changed parts YELLOW: `let rec addunion xs ys =` / `  match xs with` / `  | [] -> ys` / `  | x::xs -> if member x ys then addunion xs ys` / `             else addunion xs (x::ys)` → `val addunion : 'a list -> 'a list -> 'a list = <fun>`. On {iter}, before it appears, union's waiting `1 ::` glows GOLD (it waits, as in append).
> On {same}: `addunion [4; 7; 1] [6; 4; 7]` → `- : int list = [1; 6; 4; 7]`; then small, side by side: `union [1; 2] [3]` → `- : int list = [1; 2; 3]` and `addunion [1; 2] [3]` → `- : int list = [2; 1; 3]`. On {grow}, ys visibly lengthens as addunion conses onto it.
> On {sets}: `union [1] [2; 2]` → `- : int list = [1; 2; 2]` (addunion gives the same; verified), the repeated 2 RED.

[c7.union.1] {card} Exercise four point one. Store a set as a list with no repeats. Using member, code set union. {example} The union of four, seven, one, and six, four, seven should be one, six, four, seven, in any order. {pause} {stop} Pause here, and try it. {pause=1.5}

[c7.union.2] {wrong} First, a shortcut that looks tempting. Just append the two lists. {repeats} That gives four, seven, one, six, four, seven, with four and seven twice. {pause} A union must never introduce repetitions.

[c7.union.3] {base} Instead, walk down the first list. The union of nil with whys is just whys. {skip} For a head, ex, if ex is already a member of whys, skip it. {keep} Otherwise, keep it, consed onto the union of the rest. {type} The type is alpha list to alpha list to alpha list.

[c7.union.4] {trace} On our example, {s1} four is in six, four, seven, so it's skipped. {s2} So is seven. {s3} One is new, so it's kept, {s4} and the union of nil with whys gives back whys itself. {result} One, six, four, seven, exactly as the notes say. {shared} Like the append function, it shares whys, rather than copying it.

[c7.union.5] {cost} What does union cost? {pause} {mn} Say the first list is em long, and the second is en long. Each member test may scan the whole of the second list, once per element of the first. {total} That's at most em times en comparisons, so big O of em times en time.

[c7.union.6] {iter} Here, each kept element waits to be consed, as in append. {acc} An iterative variant, add-union, conses the new element onto whys instead. {same} It gives the same answer here, though in general the order can differ, {grow} and each member test also scans the elements already added. {sets} Neither version removes a repeat already inside whys, so both rely on being given sets.

## Scene 3 · Exercise 4.2: two lists by sign (ch7_s3_signs)

> Card 4.2 "Split by sign" (ch6's text): "Return two lists: the non-negative numbers, and the negative ones." Example `[3; -1; 0; -5; 2]` ⇒ `([3; 0; 2], [-1; -5])`, target type `int list -> int list * int list` in GREEN; + ‖. On {halves}, two empty boxes, "≥ 0" (left) and "< 0" (right), which become the two output lists below.
> On {shape}: ch3's unzip (In [65], verbatim) dimmed on the right, its `let xs, ys = unzip pairs in` YELLOW.
> Code (hero): `let rec bysign = function` / `  | [] -> ([], [])` / `  | x::xs ->` / `      let (ps, ns) = bysign xs in` / `      if x >= 0 then (x::ps, ns) else (ps, x::ns)` → on {type} `val bysign : int list -> int list * int list = <fun>`. Highlights: {base} the `[]` clause, {let} the let line, set beside unzip's (TransformFromCopy from it), {decide} the `if`.
> Trace on a ConsChain 3 → -1 → 0 → -5 → 2 → [] (GOLD values). {down}: the calls stack downward, as in ch3's unzip trace, to `([], [])`. {up}: the two output lists build back up, each number flying to its side in turn: `([2], [])`, `([2], [-5])`, `([0; 2], [-5])`, `([0; 2], [-1; -5])`, `([3; 0; 2], [-1; -5])`. On {result}: `bysign [3; -1; 0; -5; 2]` → `- : int list * int list = ([3; 0; 2], [-1; -5])`.
> Pitfall ({zero}): the `>=` flashes YELLOW. On {pitfall}, a ghost copy with `if x > 0 then` → `- : int list * int list = ([3; 2], [-1; 0; -5])`, the 0 RED on the wrong side; on "first list" it slides back to the left, GREEN.
> Wrong 2 ({twice}), RED-boxed: `let rec slow = function` / `  | [] -> ([], [])` / `  | x::xs ->` / `      if x >= 0 then (x :: fst (slow xs), snd (slow xs))` / `      else (fst (slow xs), x :: snd (slow xs))` → `val slow : int list -> int list * int list = <fun>`. On {same}, its call gives the same `([3; 0; 2], [-1; -5])` (GREEN tick). On {double}, a binary call tree doubling per level. On {count}, GOLD counters for a 20-element list: "slow: 2097151 calls" vs "bysign: 21 calls" (measured with a call counter; on the 5-element list, 63 vs 6).
> Iterative ({iter}), with ch3's revUnzip dimmed beside it: `let rec revBysign = function` / `  | ([], ps, ns) -> (ps, ns)` / `  | (x::xs, ps, ns) ->` / `      if x >= 0 then revBysign (xs, x::ps, ns)` / `      else revBysign (xs, ps, x::ns)` → `val revBysign : int list * int list * int list -> int list * int list = <fun>`. On {rev}: `revBysign ([3; -1; 0; -5; 2], [], [])` → `- : int list * int list = ([2; 0; 3], [-5; -1])`, both lists YELLOW (reversed). On {fix}: `revBysign ([2; -5; 0; -1; 3], [], [])` → `- : int list * int list = ([3; 0; 2], [-1; -5])`. On {cost}: "time O(n)", "space O(n)" in GOLD.

[c7.signs.1] {card} Exercise four point two. Code a function that takes a list of integers, and returns two lists. {halves} The first holds the numbers that are zero or more, the non-negative ones. The second holds the negative ones. {pause} {stop} Pause, and have a go. {pause=1.5}

[c7.signs.2] {shape} Two results at once is the shape of unzip, from chapter three. {base} Let's call it by-sign. On nil, it gives back two empty lists. {let} Otherwise, split the tail first, and use a let to name the two halves of its answer. {decide} Then put ex on the front of whichever half it belongs to. {type} The type is int list to int list times int list.

[c7.signs.3] {trace} On three, minus one, zero, minus five, two, {down} the calls go down to nil, which gives two empty lists. {up} Then, on the way back, each number joins its side. {result} The answer is three, zero, two, and minus one, minus five, in their original order.

[c7.signs.4] {zero} Watch the test. It says ex is greater than or equal to zero. {pitfall} Write greater than zero instead, and zero lands with the negatives. {pause} But zero belongs in the first list.

[c7.signs.5] {twice} Another trap is to skip the let, and call the function twice, once for each half of the pair. {same} The answer is still right, {double} but each call makes two more calls, so the work doubles with every element. {count} On a list of twenty, that's over two million calls, against by-sign's twenty-one.

[c7.signs.6] {iter} Two accumulators make it iterative, like rev-unzip in chapter three. {rev} But both lists come out reversed, two, zero, three, and minus five, minus one. {fix} If the order matters, reverse the input first. {cost} Either way, the time is big O of en, and so is the space the answer takes.

## Scene 4 · Exercise 4.3: a stricter zip (ch7_s4_zip)

> Card 4.3 "Another zip" (ch6's text): In [74] verbatim, `let rec zip xs ys =` / `  match xs, ys with` / `  | (x::xs, y::ys) -> (x, y) :: zip xs ys` / `  | ([], [])   -> []`, reply `val zip : 'a list -> 'b list -> ('a * 'b) list = <fun>`, and the question "How does it differ?"; + ‖. On {diff}: ch3's zip (In [64]) dimmed beside it, and its `  | _ -> []` line turns into `  | ([], [])   -> []` (TransformFromCopy), both YELLOW.
> On {warn}, the toplevel reply, the warning YELLOW (attention, not an error), the type GREEN. Exact output: `Lines 2-4, characters 2-20:` / `2 | ..match xs, ys with` / `3 |   | (x::xs, y::ys) -> (x, y) :: zip xs ys` / `4 |   | ([], [])   -> []..` / `Warning 8 [partial-match]: this pattern-matching is not exhaustive.` / `  Here is an example of a case that is not matched: (x::xs, [])` / (blank line) / `val zip : 'a list -> 'b list -> ('a * 'b) list = <fun>`. The location lines may be left out on screen; if shown, quote them exactly. On {type}, the old zip's identical type slides under the new one.
> Running example: ch3's directory, names "Amy", "Bob", "Cleo" (YELLOW) and numbers 21, 35, 47 (GOLD), drawn as ch3 drew them. On {equal}: `zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47]` → `- : (string * int) list = [("Amy", 21); ("Bob", 35); ("Cleo", 47)]`, GREEN tick for both versions.
> Trace ({trace}), ch3's uneven trace replayed with the new zip: `zip ["Amy"; "Bob"; "Cleo"] [21; 35]` ⇒ `("Amy", 21) :: ("Bob", 35) :: zip ["Cleo"] []`, the two pairs waiting as GOLD conses. On {fail}, `(["Cleo"], [])` finds no clause (both clauses flash and fail): `Exception: Match_failure ("//toplevel//", 2, 2).` in RED. On {lost}, the two waiting pairs dissolve. Small aside: the other way round, `zip ["Amy"; "Bob"] [21; 35; 47]`, raises the same exception (verified). These are ch6's hint inputs.
> On {choice} / {strict}: two columns. "Forgiving": ch3's `zip ["Amy"; "Bob"; "Cleo"] [21; 35]` → `- : (string * int) list = [("Amy", 21); ("Bob", 35)]`, Cleo DIM. "Strict": the RED Match_failure.
> On {inverse}: under strict, `unzip (zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47])` → `- : string list * int list = (["Amy"; "Bob"; "Cleo"], [21; 35; 47])` (GREEN); under forgiving, `unzip (zip ["Amy"; "Bob"; "Cleo"] [21; 35])` → `- : string list * int list = (["Amy"; "Bob"], [21; 35])`, dimmed, Cleo missing. On {design}, a balance icon between the columns.

[c7.zip.1] {card} Exercise four point three. How does this version of zip differ from the one in chapter three? {diff} Its last clause matches a pair of empty lists, where the old one had the wildcard. {pause} {stop} Pause, and think it through. {pause=1.5}

[c7.zip.2] {warn} OCaml accepts it, with a warning. The match is not exhaustive, and OCaml gives an example it misses, a non-empty list paired with nil. {type} The type is exactly the same as before.

[c7.zip.3] {equal} On lists of equal length, the two versions behave the same. {unequal} The difference is in unequal lengths. {pause} {trace} Go back to chapter three's phone book, and zip three names with only two numbers. Amy and Bob pair up as before. {fail} Then it's left with Cleo and nil, which no clause matches, so it raises Match failure. {lost} The pairs it had already built are thrown away.

[c7.zip.4] {choice} So the old zip is forgiving. It quietly drops the surplus. {strict} This one is strict, and rejects lists of different lengths. {inverse} In return, whenever it succeeds, unzip gives back exactly the two lists you started with. {design} Which one is better? That's a design choice. Strict code makes a mismatch visible, and forgiving code can hide a bug.

## Scene 5 · Exercise 4.4: hidden assumptions (ch7_s5_assume)

> Card 4.4 "Hidden assumptions" (ch6's text): "What do the change functions assume about till and amt? What could happen if those assumptions fail?", with the three headers stacked, `till` and `amt` YELLOW; + ‖.
> The three change functions from ch4–ch6 as small code cards along the top, labelled "greedy", "every way", "faster" (ch6's labels), code verbatim and unchanged (In [71], In [72], In [73]). They may come forward one at a time but are never edited. Each result below appears under the version it belongs to.
> On {list}: four GREEN assumption rows, one per beat, in the order of ch6's hint chips: {pos} "every coin > 0", {nonneg} "amt ≥ 0", {desc} "till in descending order", {norepeat} "no coin repeated". Each later beat turns its row RED while it is being broken, and back to GREEN after.
> Zero coin ({zero}): greedy trace `change [5; 0] 3` ⇒ `change [0] 3` ⇒ `0 :: change [0] 3` ⇒ `0 :: 0 :: change [0] 3` ⇒ …, the GOLD amount 3 never shrinking. On {stack}: greedy and every-way both reply `Stack overflow during evaluation (looping recursion?).` (RED). Checked under `timeout 10` with `OCAMLRUNPARAM='l=1M'`; with OCaml 5's default stack it would take far longer, so show no timings. On {tail}: the faster version rewrites in place, `change [0] 3 [] []` ⇒ `change [0] 3 [0] []` ⇒ `change [0] 3 [0; 0] []` ⇒ …, chg growing, beside a rising memory gauge and a toplevel prompt that never replies (verified: still running when the 10 s timeout killed it, at ~4.9 GB resident). On {neg}: `change [5; -1] 3` → the same Stack overflow line (greedy and every-way; the faster version runs on), the GOLD amount 3 → 4 → 5 … rising.
> Negative amount ({negamt}): greedy `change [50; 20; 10; 5; 2; 1] (-3)` → `Exception: Failure "no more coins!".` (RED). On {empty}: every-way `change [50; 20; 10; 5; 2; 1] (-3)` → `- : int list list = []`, and faster `change [50; 20; 10; 5; 2; 1] (-3) [] []` → `- : int list list = []`.
> Ascending ({asc}, {nine}): greedy `change [1; 2; 5] 9` → `- : int list = [1; 1; 1; 1; 1; 1; 1; 1; 1]`, nine GOLD 1p discs. On {allways}: every-way `change [5; 2; 1] 9` and `change [1; 2; 5] 9` as two columns of eight solutions, matching pairs linked (same coins, other order). Exact replies, each printed after `- : int list list =` over three lines: `[[5; 2; 2]; [5; 2; 1; 1]; [5; 1; 1; 1; 1]; [2; 2; 2; 2; 1]; [2; 2; 2; 1; 1; 1]; [2; 2; 1; 1; 1; 1; 1]; [2; 1; 1; 1; 1; 1; 1; 1]; [1; 1; 1; 1; 1; 1; 1; 1; 1]]` and `[[1; 1; 1; 1; 1; 1; 1; 1; 1]; [1; 1; 1; 1; 1; 1; 1; 2]; [1; 1; 1; 1; 1; 2; 2]; [1; 1; 1; 1; 5]; [1; 1; 1; 2; 2; 2]; [1; 1; 2; 5]; [1; 2; 2; 2; 2]; [2; 2; 5]]`. (The faster version also finds 8 for each.)
> Repeated ({rep}): every-way `change [5; 2; 1; 2] 4` → `- : int list list =` / `[[2; 2]; [2; 1; 1]; [2; 2]; [1; 1; 1; 1]; [1; 1; 2]; [2; 2]]`. On {dup} the three `[2; 2]` turn YELLOW and `[2; 1; 1]` links to `[1; 1; 2]`; on {six} GOLD "6 answers, 3 ways". On {greedyok}: greedy `change [5; 2; 1; 2] 4` → `- : int list = [2; 2]`. (The faster version repeats too: `[[2; 2]; [1; 1; 2]; [2; 2]; [1; 1; 1; 1]; [2; 1; 1]; [2; 2]]`.) On {close}, the four rows back to GREEN, bracketed "the caller's job".

[c7.assume.1] {card} Exercise four point four. What do the making change functions assume about the till and the amount? And what could happen if those assumptions were broken? {pause} {stop} Pause, and list as many as you can. {pause=1.5}

[c7.assume.2] {list} Here are four assumptions. {pos} Every coin is positive. {nonneg} The amount is zero or more. {desc} The till is in descending order. {norepeat} And no coin value appears twice. {pause} Now let's break them, one at a time.

[c7.assume.3] {zero} First, a coin worth zero. Using it takes nothing off the amount, so once it's reached, the same call repeats forever. {stack} Greedy, and the first version that finds every way, leave work waiting on each call, so they run out of stack. {tail} In the faster version, that call is the last thing that happens, so it just runs on, its list of chosen coins growing, until memory runs out. {neg} A negative coin is no better. Each use makes the amount bigger, so it never reaches zero.

[c7.assume.4] {negamt} Second, a negative amount. Every coin is too big, so greedy skips them all, and raises its exception. {empty} The other two versions return the empty list, meaning no solutions.

[c7.assume.5] {asc} Third, a till in increasing order. Greedy still makes change, but it tries the smallest coins first. {nine} Asked for nine, from one, two and five, it hands back nine pennies. {allways} The other two versions find the same eight ways, in a different order.

[c7.assume.6] {rep} Last, a repeated coin. Make four pence from five, two, one, and two again. {dup} The answer two plus two turns up three times, and two plus one plus one turns up again as one plus one plus two. {six} That's six answers, for three real ways. {greedyok} Greedy happens to be unaffected here. {close} The code checks none of this. It's up to the caller.

## Scene 6 · Exercise 4.5: counting the ways (ch7_s6_count)

> Card 4.5 "Counting the ways" (ch6's text): "Two coin values: show there are O(n) ways to make change for n (ignoring order). Three values? Four? …"; + ‖.
> On {ignore}: GOLD coin discs 5, 2, 2 and 2, 5, 2 side by side, merging into one "way" = "one 5, two 2s".
> Small case ({small}): amount 20 (GOLD) with coins 5 and 2. On {k}, a column of five rows, 0 to 4 five-pence discs. On {rest} each row shows what's left, 20, 15, 10, 5, 0, and 2p discs try to fill it. On {check} rows 20, 10, 0 get a GREEN ✓ (ten 2s, five 2s, no 2s) and rows 15, 5 a RED ✗. On {three}: ch5's every-way `change [5; 2] 20` → `- : int list list =` / `[[5; 5; 5; 5]; [5; 5; 2; 2; 2; 2; 2]; [2; 2; 2; 2; 2; 2; 2; 2; 2; 2]]`, GOLD "3 ways".
> General ({general}): a big coin a and a small coin b, a > b (YELLOW symbols). On {fix}: "number of a's: 0, 1, …, n/a". On {once}: "the rest: all b's, 1 way or none". On {bound}: "ways ≤ n/a + 1", then on "big O of en" "= O(n)" in GOLD.
> Three coins ({three}, {split}): a fan with one branch per count of the largest coin, each leading to a small box "two-coin problem: O(n) ways". On {mult}: "O(n) choices × O(n) ways = O(n²)". On {induct}: a column "2 coins: O(n)", "3 coins: O(n²)", "4 coins: O(n³)", "k coins: O(n^(k−1))".
> Table ({table}), GOLD numbers, columns n = 10, 20, 40, 80, 160, one row per beat. Verified counts (List.length of ch6's faster `change … [] []`; ch5's version agrees on 2, 3, 5, 9, 17, on 10, 29, 97, 353, and on 4366): {two} `[5; 2]`: 2, 3, 5, 9, 17, tagged "≈ ×2: O(n)"; {threec} `[5; 2; 1]`: 10, 29, 97, 353, 1345, tagged "→ ×4: O(n²)"; {four} `[10; 5; 2; 1]`: 11, 40, 195, 1173, 8041, tagged "→ ×8: O(n³)".
> On {uk}: the till `[50; 20; 10; 5; 2; 1]` as six GOLD coin discs, "6 coins: O(n⁵)", and "99p: 4366 ways", the number ch6 quoted from the notes.

[c7.count.1] {card} Exercise four point five. Take two coin values, and an amount to make, called en. Ignoring order, show that the number of ways to do it is big O of en. What about three or more coin values? {pause} {stop} Pause, and try a small case first. {pause=1.5}

[c7.count.2] {ignore} Ignoring order, five, then two, then two, is the same way as two, then five, then two. A way is just how many of each coin it uses. {small} Here's an example: fives and twos, making twenty. {k} There can be zero to four fives. {rest} Whatever is left must be made of twos, in exactly one way, or not at all. {check} What's left is twenty, fifteen, ten, five or zero, and only the even amounts work. {three} So there are three ways, as change finds.

[c7.count.3] {general} In general, take two coins, a big one and a small one. {fix} A way is fixed by how many big coins it uses, which can be anything from zero to the amount divided by the big coin. {once} The rest must be all small coins, so each count gives one way, or none. {bound} So the number of ways is at most one more than en divided by the big coin. {pause} That's big O of en.

[c7.count.4] {three} Now add a third coin. {split} Fix how many of the largest coin you use. What's left is a two-coin problem, with big O of en ways. {mult} And there are big O of en choices for the largest coin, so there are big O of en squared ways altogether. {induct} Each extra coin brings one more factor of en. So the power is one less than the number of coins.

[c7.count.5] {table} Real counts agree. Watch each one as the amount doubles. {two} With fives and twos, the count roughly doubles, so it grows linearly. {threec} Add pennies, and it heads towards four times. {four} Add tens as well, and it heads towards eight times. {uk} With all six coins, from fifty down to one, the count grows as big O of en to the fifth. That's why ninety-nine pence already has four thousand, three hundred and sixty-six ways.

## Scene 7 · Exercise 4.6: what the types force (ch7_s7_types)

> Card 4.6 "What the types force" (ch6's text): `val f : 'a * 'b -> 'b * 'a` and `val g : 'a -> 'a list`; `f (1, true)` ⇒ GOLD "?" and `g 0` ⇒ GOLD "?"; + ‖. `'a`/`'b` PINK throughout.
> On {recall}: L3's `val id : 'a -> 'a = <fun>` as a dimmed machine box (L3 ch6_s5's id box, reused), with its GOLD "?" crossed out (no new α can come from nowhere).
> f as a machine box. On {fapp}, `(1, true)` goes in, with GREEN tags 'a = int, 'b = bool. On {only}, the 1 (GOLD) and `true` are the only values inside the box. On {answer} they swap places and come out as `(true, 1)`.
> On {swap}: `let f (x, y) = (y, x)` → `val f : 'a * 'b -> 'b * 'a = <fun>`; `f (1, true)` → `- : bool * int = (true, 1)`. On {cheat}: `let f (x, y) = (true, 1)` → `val f : 'a * 'b -> bool * int = <fun>`, its `bool * int` boxed RED against the required `'b * 'a`.
> g as a machine box. On {g0}, 0 goes in; on {zeros}, only 0 discs come out. On {howmany} a GOLD "how many?". On {any}: a fan of possible results `[]`, `[0]`, `[0; 0]`, `[0; 0; 0]`, …, each with a GREEN ✓ for the type. Verified examples, shown small: `let g x = [x]` → `val g : 'a -> 'a list = <fun>`, `g 0` → `- : int list = [0]`; `let g x = [x; x]` → `val g : 'a -> 'a list = <fun>`, `g 0` → `- : int list = [0; 0]`. (Careful: `let g x = []` replies `val g : 'a -> 'b list = <fun>`, a more general type, so don't use it as the example for `[]`. Inventing a value, `let g x = [1]`, replies `val g : 'a -> int list = <fun>`.)
> On {return}: L3's `val loop : 'a -> 'b = <fun>` with its circular arrow, dimmed, beside both boxes. On {lesson}: f's `(true, 1)` locked GREEN; g's `[0; …; 0]` GREEN with its length a GOLD "?".

[c7.types.1] {card} Exercise four point six. All we know about two functions, eff and gee, is their types. {f} The first, eff, takes an alpha times beta to a beta times alpha. {g} The second, gee, takes an alpha to an alpha list. {ask} Suppose eff of one, true, and gee of zero both return. What are the results? {pause} {stop} Pause, and reason it out. {pause=1.5}

[c7.types.2] {recall} Remember eye-dee, from lecture three. A function that knows nothing about alpha has no way to invent one. It can only hand back what it was given. {fapp} For eff of one, true, alpha is int, and beta is bool. {only} The only int that eff has is one, and the only bool is true. {answer} So it must swap them, giving true, one. {pause}

[c7.types.3] {swap} The obvious code, eff of ex, why, equals why, ex, has exactly this type. {cheat} Cheat by always returning true, one, and the result type becomes bool times int, which no longer matches beta times alpha.

[c7.types.4] {g0} Now gee of zero. It must return a list of alphas, and the only alpha it has is zero. {zeros} So the answer is a list of zeros. {howmany} But how many? {pause} {any} It could be the empty list, a single zero, two zeros, or more. Each fits the type, so the type alone leaves the length open.

[c7.types.5] {return} One caveat. Like loop in lecture three, either function could run forever, or raise an exception. {given} That's why the exercise says they return. {lesson} When they do, the type decides eff's answer completely, and gee's answer up to its length.

## Scene 8 · Recap (ch7_s8_recap)

> Six rows, one per beat ({r1}–{r6}), each with the exercise number, the function name YELLOW, and a GOLD cost or GREEN result: 4.1 `union`, O(m·n), "shares ys" in TEAL · 4.2 `bysign`, "a let, like unzip", "0 goes first" · 4.3 strict `zip`: `Match_failure` RED vs "drops the surplus" · 4.4 "coins > 0, distinct, descending; amt ≥ 0" · 4.5 "2 coins: O(n)", "k coins: O(n^(k−1))" · 4.6 `f (1, true)` = `(true, 1)`, `g 0` = `[0; …; 0]`.
> On {next}: the rows dim; "Next lecture: Sorting", with ch1's chain 3 → 5 → 9 → 4 → 7 → [] cut in two by take and drop (the merge sort teaser, as ch6's recap had it).
> On {end}: hold, then the end card for ~8 s after the last word; music carries it.

[c7.recap.1] {recap} Let's recap. {r1} Union walks the first list and keeps what the second lacks, in big O of em times en. {r2} Splitting by sign builds two results at once, with a let, like unzip. {r3} The stricter zip rejects unequal lengths, where the old one drops the surplus. {r4} The change functions trust the till to hold positive, distinct coins, in descending order, and the amount to be zero or more. {r5} With two coins, the ways grow as big O of en, and each extra coin multiplies that by en. {r6} And the types force eff to swap, and gee to return only copies of its argument.

[c7.recap.2] {next} Next time, in lecture five, we turn to sorting. Sorted data can be searched fast, and merge sort splits its lists with take and drop. {end} Well done. See you in the next lecture.
