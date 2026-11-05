# Chapter 1 · How fast can we sort?

Lecture 5 (Sorting), part 1 of 7. Source: FoCS 2026-27 notes v1.8, pp. 37–39 (the lecture's
introduction and §5.1), with callbacks to Lecture 2 (O-notation, constant factors) and Lecture 4
(linear search and the 16-prime binary-search row of ch2, `let` patterns and two results in one
accumulator), and Park and Miller's 1988 paper via project.json's web source.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

All code and replies below were run in OCaml 5.4.1 and are quoted verbatim. All arithmetic
(log₂ values, the decision tree's leaf counts and depth) was checked in Python.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card, `title_card("Part 1 · How fast can we sort?")`: "Sorting", "Foundations of Computer Science · Lecture 5", "Part 1 · How fast can we sort?".
> On {last}: three small DIM thumbnails of Lecture 4 in a row: a chain with a GOLD pointer stepping cell to cell ("search, one cell at a time"), a few coins ("making change"), and L4's row of 16 sorted primes with a halving bracket and GOLD "O(log n)". On {promise} the third one lifts out of DIM with a YELLOW caption "sorted data can be searched fast". Then all three clear.
> On {chain}: the lecture's running chain `3 → 5 → 9 → 4 → 7 → []` (ConsChain([3,5,9,4,7]) at ORIGIN, the L3/L4 palette: values GOLD, `[]` TEAL). It stays on screen for the whole hook.
> On {sort}: the cells rearrange themselves into `3 → 4 → 5 → 7 → 9 → []` (cells slide to their new places, arrows redraw), and a GREEN tick appears at its right. This sorted chain with its tick is the lecture's "done" picture; every later trace ends on it.
> On {compare}: back to the unsorted chain. Pairs of cells light up YELLOW two at a time with a small "≤ ?" between them (9 and 4, then 5 and 4, then 3 and 4), each answered by a tiny "yes" or "no".
> On {question}: a YELLOW question above the chain, "How many comparisons does sorting need?". On {clever}, a second line under it, "Could a cleverer method need fewer?". Hold both into the next scene's first beat.

[c1.hook.1] {title} This is lecture five of Foundations of Computer Science, and it's all about sorting. {last} Last lecture, we built tools for lists, searched them one cell at a time, and made change with coins. {promise} It ended on a promise, that sorted data can be searched fast. {pause}

[c1.hook.2] {chain} Here's our running list again, three, five, nine, four, seven. {sort} Sorting it means rearranging it into increasing order, three, four, five, seven, nine. {compare} Every sort in this lecture gets there the same way, by comparing two items at a time, and moving them according to the answer.

[c1.hook.3] {question} So here's the question for this chapter. How many comparisons does sorting need? {pause} {clever} And could some clever method, one nobody has thought of yet, get away with fewer? {pause=1.5}

## Scene 2 · What sorting is for (ch1_s2_why)

> A column of five icon slots down the left edge, each filled with an icon and a label on its mark: {search} a magnifier, "search"; {merge} two short rows zipping into one, "merging"; {dups} two equal tiles side by side, "duplicates"; {table} a small grid, "inverting tables"; {graphics} three overlapping shapes, "graphics". Each use plays its example on the right, then shrinks into its slot.
> Search: a magnifier over a short sorted row of GOLD numbers, DIM tag "next scene". Merging: the sorted rows 2 7 8 and 3 5 9 interleave, one item at a time, into 2 3 5 7 8 9; DIM tag "Part 5".
> Duplicates: the names Cleo, Amy, Dee, Bob, Amy in YELLOW tiles. On {sorted} they slide into order, Amy, Amy, Bob, Cleo, Dee. On {pass} a small bracket steps along the neighbouring pairs, and the Amy, Amy pair flashes.
> Table: a four-row directory with columns name / number / street (names YELLOW, numbers GOLD): Ada 52 Mill Road; Ben 17 Tenison Road; Cal 38 Hills Road; Dee 24 Mill Road. The sorted column's header is underlined. On {number}, the rows slide into number order (Ben 17, Dee 24, Cal 38, Ada 52), with a small tag "police". On {street}, they slide into street order (Cal Hills Road, Ada Mill Road, Dee Mill Road, Ben Tenison Road), tag "junk mail". On {same}, a caption under the table: "same information, different applications".
> Graphics: three overlapping shapes drawn far to near, each new one covering the last (the painter's order; this example is beyond the notes, which only name graphics).
> On {knuth}: the five icons dim. A book cover appears, "The Art of Computer Programming · Vol. 3 · Sorting and Searching", with "Donald Knuth" in YELLOW. On {sedgewick}, a second cover beside it, "Algorithms", "Robert Sedgewick".

[c1.why.1] {why} First, why sort at all? The notes list five uses. {search} The first is search. Sorted data can be searched much faster, and that's the next scene. {merge} The second is merging. Two sorted files can quickly be combined into one sorted file. We'll write that in part five.

[c1.why.2] {dups} Third, finding duplicates. Here's a list of names with a repeat hidden in it. {sorted} After sorting, equal items sit side by side, {pass} so one pass that compares each name with its neighbour finds every repeat.

[c1.why.3] {table} Fourth, inverting tables. A telephone directory is sorted by name. {number} Sort the same entries by number instead, and the book becomes useful to the police, who have a number and want the name. {street} Sort them by street address, and it's useful to junk-mail firms. {same} The same information, sorted in different ways, gets different applications.

[c1.why.4] {graphics} Fifth, graphics algorithms. One example is drawing far shapes first, so that near ones cover them. {knuth} Sorting is perhaps the most deeply studied part of algorithm design. Donald Knuth's series, The Art of Computer Programming, gives a whole volume to sorting and searching. {sedgewick} Robert Sedgewick's books cover it too.

## Scene 3 · Binary search, as promised (ch1_s3_binary)

> L4 ch2 s3's row of 16 sorted GOLD primes, `2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53`, centred on {row}, same boxes as there (`PRIMES`, `BOX` in `projects/focs/l04-more-lists/scenes/ch2_s3_faster.py`), with YELLOW "find 41" above.
> On {linear}: a GOLD pointer walks from 2 to 41 box by box with a counter that ends at "13 comparisons"; the pointer fades, and "linear: 13" stays small at the left. On {promise}: a DIM tag "Lecture 4: binary search, coming next lecture", replaced by the title "binary search".
> The four probes (the same ones as L4's `STEPS`: 19, 37, 43, 41), each probed box YELLOW with a small comparison under it and a GOLD counter "comparisons: 1 … 4": {middle} 19 (position 8 = n/2), "41 > 19", and on {left} boxes 2 to 19 dim; {second} 37, "41 > 37", boxes 23 to 37 dim; {third} 43, "41 < 43", boxes 43, 47, 53 dim (here 43 goes in step 3, not step 4 as in L4's animation); {found} 41 turns GREEN, "found".
> On {four}: "4" and "13" side by side in GOLD. On {halves}: a small line under the row, "each comparison throws away at least half", and in one clause the L4 figure "1,000,000 items → about 20". On {logn}: GOLD "binary: O(log n)" beside "linear: O(n)".
> On {lists}: the row shrinks up; under it, a ConsChain of the same primes (8 cells shown, with ⋯ in the middle) and a YELLOW pointer crawling from the head cell by cell towards the middle, with GOLD "about n/2 steps, just to reach the middle". On {trees}: the caption "needs arrays or trees, not lists", and a DIM tag "binary search trees: Lecture 7".

[c1.bin.1] {row} Last lecture, we searched for forty-one in this row of sixteen sorted primes. {linear} Searching one item at a time from the left takes thirteen comparisons to reach it. {promise} We promised something better, called binary search. Here it is, step by step.

[c1.bin.2] {middle} Compare forty-one with the middle item, in position eight, which is nineteen. {left} Forty-one is bigger, so it must be in the right half. Throw the left half away. {second} Compare with the middle of what's left, thirty-seven. Bigger again, so throw away thirty-seven and everything before it. {third} Next comes forty-three. This time forty-one is smaller, so throw away forty-three and everything after it. {found} One item is left, and the fourth comparison finds it. {pause}

[c1.bin.3] {four} Four comparisons, against thirteen. {halves} Each comparison throws away at least half of what's left, so even a million items need only about twenty. {logn} Binary search takes big O of log N time, where linear search takes big O of N.

[c1.bin.4] {lists} But there's a catch. Binary search jumps straight to the middle item. {walk} On a list, reaching the middle means walking half the list from the head, one cell at a time, and that alone takes big O of N. {trees} So binary search needs arrays or trees, and we'll meet binary search trees in lecture seven.

## Scene 4 · The contestants, and how to score them (ch1_s4_contest)

> On {algos}: four names in a row, YELLOW: "insertion sort", "quicksort", "merge sort", "heapsort". On {three}, the first three get small GOLD tags "Part 2", "Parts 3–4", "Part 5"; on {heap}, heapsort dims to DIM with a small "named only".
> On {measure}: "How do we score them?". On {count}: GOLD `C(n)` with the caption "comparisons needed to sort n items". On {why}: two GOLD values with "≤ ?" between them, captioned "the only way a sort learns the order". On {machine}: three small machine icons, each showing the same count; a DIM tag "Lecture 2: ignore constant factors".
> On {dec}: a boxy old workstation icon labelled "DECstation" with a small clock; on {mips}, "MIPS chip · an early RISC design" under it. On {relative}: the caption "times: compare them only with each other".
> On {board}: the scoreboard, defined once in this scene's file (`scenes/ch1_s4_contest.py`) so that ch2–ch6 can import it. Rows on {rows}, YELLOW: "insertion sort", "quicksort", "merge sort". Columns on {cols} and {time}: "comparisons on 10,000 random items" and "DECstation time". Under the comparisons header, on {cols}, a small DIM tag "counted by us: a tallying ≤" (ch2 s5 uses the same words). On {blank}, every cell becomes a GOLD "?".
> On {floor}: a dashed line beneath the rows, with "lower bound: ?" in GOLD at its left. Hold the board. Scene 6 brings it back and makes this line solid.

[c1.contest.1] {algos} The common sorting algorithms are insertion sort, quicksort, merge sort and heapsort. {three} We'll study the first three, {heap} and heapsort we only name. {each} Each one has its own advantages, so let's set up a fair contest.

[c1.contest.2] {measure} How should we score them? {pause} {count} The usual measure is the number of comparisons a sort makes, as a function of how many items it sorts. {why} Comparing two items is the only way these sorts learn anything about the order. {machine} And the number of comparisons comes out the same on every machine, so, as in lecture two, it ignores constant factors.

[c1.contest.3] {dec} The notes also give running times, measured on a Deck Station. {mips} That's a workstation built on the Mips chip, an early Risk design, and it's really old now. {relative} So its seconds only mean something compared with each other.

[c1.contest.4] {board} So here's the scoreboard. {rows} One row per contestant. {cols} One column counts the comparisons on ten thousand random numbers, which we'll make at the end of this chapter. The notes don't give these counts, so we make them ourselves, with a less than or equal that keeps a tally. {time} The other column gives the Deck Station's time. {blank} Every cell starts as a question mark, and later parts fill them in. {floor} But first, one more line, underneath. How low could the comparisons go, for any method at all? {pause}

## Scene 5 · Twenty questions with n! answers (ch1_s5_bound)

> On {three}: three cards labelled a, b, c (YELLOW letters) at the top. On {six} and {list}: the six orders in a 2 × 3 grid, "a b c", "a c b", "b a c", "b c a", "c a b", "c b a", and under them GOLD `3! = 3 × 2 × 1 = 6` (on "three factorial").
> On {must}: each order gets its own small arrow diagram of the moves that sort it (all different). On {only}: two cards with "≤ ?" between them; on {yesno}, two buttons, GREEN "yes" and RED "no"; on {twenty}, a caption "twenty questions: about a million things" (2²⁰ = 1,048,576, the same figure as binary search).
> On {root}: the grid becomes the decision tree, growing down from a root box "a ≤ b?". On {split}: the six orders flow down its two branches, yes: a b c, a c b, c a b; no: b a c, b c a, c b a. On {half}: the caption "at best, each question rules out half". On {tree}: the full tree. Yes → "b ≤ c?" (yes: leaf a b c; no → "a ≤ c?": leaves a c b / c a b). No → "a ≤ c?" (yes: leaf b a c; no → "b ≤ c?": leaves b c a / c b a). On {leaves}: the six leaves glow GREEN; on {depth}, a GOLD bracket down the side, "3 questions". (Checked by brute force: no tree for three items has depth 2.)
> On {two}: a GOLD cut line under depth 2. On {four}: four boxes, "yes yes", "yes no", "no yes", "no no", with `2² = 4`. On {fewer}: GOLD "4 < 6"; two orders slide into the same box. On {wrong}: one of them turns RED with a cross. On {three}: "some input needs a 3rd question".
> On {general}: the tree shrinks to the top-left corner. GOLD "n items: n! orders". On {power}: "10 comparisons: at most 2¹⁰ answer patterns", then "C comparisons: at most 2^C". On {bound}: the boxed YELLOW `2^{C(n)} \ge n!`. On {log}: under it, `C(n) \ge \log_2(n!)`. On {worst}: the caption "worst case: whatever the method, some input needs this many". The two formulas carry over into scene 6.

[c1.bound.1] {three} Let's start small, with three items. Call them ay, bee and see. {six} They can arrive in six different orders. {list} Here are all six. There are three choices for the first item, two for the second, and one for the last, so three factorial is six.

[c1.bound.2] {must} A sort has to find out which of these six orders it was given, because each one needs a different rearrangement to put it right. {only} It can only find out by asking questions like, is this item at most that one? {yesno} Each question has just two answers, yes or no. {twenty} It's a game of twenty questions, where twenty yes-or-no answers can single out one of about a million things.

[c1.bound.3] {root} Say the first question is, is ay at most bee? {split} A yes leaves three of the orders possible, and a no leaves the other three. {half} At best, a question rules out half of the orders still possible. {tree} Keep asking, and the questions form a tree. {leaves} Each leaf is one order, so this tree has six leaves, {depth} and its longest path asks three questions.

[c1.bound.4] {two} Could a cleverer sort always manage with two? {pause} {four} Two questions have only four possible answer patterns, yes yes, yes no, no yes, and no no. {fewer} Four is fewer than six, so at least two of the orders would get the same answers, and the sort would treat them the same way. {wrong} One of them would come out wrong. {three} So some input needs a third question.

[c1.bound.5] {general} The same argument works for any number of items. A list of N values can arrive in N factorial orders. {power} Each comparison at most doubles the answer patterns, so ten comparisons give at most two to the ten. {bound} So two, raised to the number of comparisons, must be at least N factorial. {log} Taking logs, the number of comparisons must be at least log base two of N factorial. {worst} This is a worst-case bound. Whatever the method, some input forces it to make this many comparisons. {pause}

## Scene 6 · How big is log₂ n!? (ch1_s6_nlogn)

> At the top, from scene 5: `C(n) \ge \log_2(n!)`. On {sum}: below it, `\log_2(n!) = \log_2 1 + \log_2 2 + \cdots + \log_2 n`.
> On {bars}: axes with 16 BLUE bars, k = 1 … 16 along the bottom, bar k of height log₂ k (bar 1 has height 0; bars 2, 4, 8, 16 reach 1, 2, 3, 4, labelled in GOLD). On {total}: the bars stack end to end into one GOLD total, "≈ 44.25" (log₂ 16! = 44.25).
> On {top}: a GOLD line at height 4 across all sixteen bars, outlining a 16 × 4 rectangle, "≤ 64". On {half}: a GOLD line at height 3 under the last eight bars (9 … 16), a shaded 8 × 3 rectangle, "≥ 24". On {exact}: `24 ≤ 44.25 ≤ 64`.
> On {general}: the bars dim, and the same sandwich in symbols, `\tfrac{n}{2}\log_2\tfrac{n}{2} \;\le\; \log_2(n!) \;\le\; n\log_2 n` (this sandwich argument is beyond the notes). On {grow}: both ends get a GOLD "O(n log n)" tag. On {sharp}: the notes' form, `\log_2(n!) \approx n\log_2 n - 1.44\,n`, with a DIM footnote "Stirling's formula; 1.44 ≈ log₂ e".
> On {five}: GOLD `5! = 120`. On {powers}: `2^6 = 64 < 120 \le 128 = 2^7`. On {seven}: "five items: some input needs at least 7 comparisons" (this 7 comes back in ch2, ch3 and ch5).
> On {tenk}: `\log_2(10000!) \approx 118{,}458`. On {formula}: `10000\log_2 10000 - 1.44 \times 10000 \approx 118{,}477` (with log₂ e itself instead of 1.44 it gives ≈ 118,450; show only the 1.44 version, which is what's on screen).
> On {merge}: "merge sort: O(n log n) comparisons (Part 5)"; on {best}, "O(n log n) is the best possible". On {floor}: scene 4's scoreboard comes back, and its dashed line turns solid, reading "lower bound ≈ 118,458" in GOLD.

[c1.nlogn.1] {how} So how big is log base two of N factorial? {sum} N factorial is one times two times three, and so on, up to N, and the log of a product is the sum of the logs. {bars} So draw one bar for each number from one to N, with height log base two of that number. Here are the bars for sixteen. {total} Their total height is what we want.

[c1.nlogn.2] {top} Every bar is at most log base two of sixteen, which is four, so the total is at most sixteen times four, sixty-four. {half} The last eight bars are each at least three, so the total is at least eight times three, twenty-four. {exact} The true total is about forty-four, in between.

[c1.nlogn.3] {general} The same sandwich works for any N. The low side is half of N, times log base two of half of N, and the high side is N times log base two of N. {grow} Both sides grow like N log N, so the total does too. {sharp} Stirling's formula gives the notes' sharper estimate, N log base two of N, minus one point four four N. {pause}

[c1.nlogn.4] {five} Let's put in numbers. For our five-item list, five factorial is a hundred and twenty. {powers} Six comparisons give only sixty-four answer patterns, and seven give a hundred and twenty-eight. {seven} So some arrangement of five items needs at least seven comparisons. {tenk} For ten thousand items, log base two of ten thousand factorial is about a hundred and eighteen thousand, four hundred and fifty-eight. {formula} The notes' formula gives nearly the same.

[c1.nlogn.5] {merge} Merge sort, in part five, needs only big O of N log N comparisons. {best} So the best possible is big O of N log N, and merge sort reaches it. {floor} That's the floor of our scoreboard. In the worst case, no comparison sort can go below it. {pause}

## Scene 7 · Ten thousand random numbers (ch1_s7_testdata)

> On {race}: the scoreboard's column header "comparisons on 10,000 random items" flashes small at the top, then clears for the code.
> The notes' code, in the code box, `nextrandom` YELLOW, keywords BLUE, numbers GOLD, `float` GREEN:
> `let nextrandom seed =` / `  let a = 16807.0 in` / `  let m = 2147483647.0 in` / `  let t = a *. seed in` / `  t -. m *. (floor (t /. m))`. On {never}, a DIM tag "never mind how this works" (the notes' words). On {mult}, `16807.0` and `a *. seed` light up; on {mod}, `2147483647.0` lights up with a GOLD tag `2^{31} - 1`. On {floats}, the operators `*.`, `/.`, `-.` are underlined. On {floor}, the last line gets a bracket, "the remainder".
> On {reply}: `val nextrandom : float -> float = <fun>`. On {one}: `nextrandom 1.0;;` ⇒ `- : float = 16807.`. On {park}: a DIM card, "Park and Miller, 1988: the 'minimal standard' generator" (beyond the notes).
> On {randlist}: the first code shrinks up, and `randlist` comes in under it: `let rec randlist (seed, seeds) = function` / `  | 0 -> (seed, seeds)` / `  | n -> randlist (nextrandom seed, seed::seeds) (n-1)`, `::` TEAL. On {pair}, `(seed, seeds)` lights up; on {count}, `(n-1)`; on {zero}, the pattern `0` (YELLOW box, "a constant pattern"). On {trick}: DIM tag "Lecture 4: two results in one accumulator". Reply: `val randlist : float * float list -> int -> float * float list = <fun>`.
> On {example}: `randlist (1.0, []) 3;;` ⇒ `- : float * float list = (1622650073., [282475249.; 16807.; 1.])`, with `1.` and `16807.` lit up and a small "newest first" arrow; the leading `1622650073.` gets "next seed".
> On {call}: `let seed, rs = randlist (1.0, []) 10000;;`, then the toplevel's reply, verbatim, scrolling as a glimpse (not read aloud): `val seed : float = 1043618065.` / `val rs : float list =` / `  [1484786315.; 925166085.; 1614852353.; 721631166.; 173942219.; 1229443779.;` / `   789328014.; 570809709.; 1760109362.; 270600523.; 2108528931.; 16480421.;` … ending `   948048264.; 1596326605.; 1816773893.; ...]` (54 lines, the same as the notes' Out[77] except that OCaml 5.4.1 ends with three ASCII dots where the notes show "…"). On {let}, the pattern `seed, rs` lights up. On {seed}, `1043618065.` glows YELLOW and a GREEN tick appears beside it with "Park and Miller's published check value". On {rs}, the `val rs : float list =` printout lights up. On {backwards}, a GOLD caption "… ends 16807., 1." (checked: `List.nth rs 9998` ⇒ `- : float = 16807.` and `List.nth rs 9999` ⇒ `- : float = 1.`; show it as a caption, not as toplevel output).
> On {poly}: the code clears. `<=` in a BLUE box, with GREEN `float`, `int`, `string` around it on {le}.

[c1.test.1] {race} For the race, we need ten thousand numbers in no particular order. {never} The notes say, never mind how this works. Good random numbers are hard to make. Here's just the shape of it. {mult} Next-random multiplies the seed by sixteen thousand, eight hundred and seven, {mod} and keeps the remainder after dividing by two to the thirty-one, minus one.

[c1.test.2] {floats} It does this in floats. {floor} The last line divides, rounds down, multiplies back, and subtracts, and what's left over is the remainder. {reply} OCaml replies that next-random takes a float, and returns a float. {one} Start it at one, and you get sixteen thousand, eight hundred and seven. {park} This is the minimal standard generator, published by Park and Miller in nineteen eighty-eight.

[c1.test.3] {randlist} Rand-list builds the list. {pair} It carries the current seed and the list so far, together in one pair, {count} and counts N down to zero. {zero} The pattern zero is a constant, and that clause stops the count. {trick} It's last lecture's trick of building two results at once in an accumulating argument. {example} Here's an example. Three steps from one give a list ending in sixteen thousand, eight hundred and seven, then one, because each new number goes on the front.

[c1.test.4] {call} Now call it ten thousand times, starting from one, with an empty list. {let} We take the pair apart with a let pattern, as in last lecture. {seed} The final seed is exactly the check value Park and Miller published, so our generator works as it should. {rs} And ar-ess holds our ten thousand numbers, {backwards} built backwards, just like the example.

[c1.test.5] {poly} These are floats, but that's no problem. {le} Less than or equal is polymorphic, so every sort in this lecture works on floats, integers and strings alike.

## Scene 8 · Recap (ch1_s8_recap)

> Recap: six short lines, one per mark ({r1} … {r6}), each with a small icon from the chapter at its left: the five-use icon column, "sorting serves search, merging, duplicates, tables"; the prime row with its halving bracket, "binary search: O(log n), needs arrays or trees"; the scoreboard in miniature, "we count comparisons"; the decision tree in miniature, `2^{C(n)} \ge n!`; `C(n) \ge \log_2(n!) \approx n\log_2 n`, with GOLD "≈ 118,458 for 10,000 items"; the `rs` printout snippet, "10,000 random numbers to race on".
> On {next}: the recap dims. "Next: insertion sort". On {cards}: ch2's opening picture (its s1 brief), five playing cards: the 3, 5 and 9 fanned in a hand, already in order, and the 4 and the 7 face up a little to the right; the 4 lifts and slides in between the 3 and the 5.
> Leave about 8 s of end card after the last word; the music carries it.

[c1.recap.1] {recap} Let's recap. {r1} Sorting makes searching, merging and finding duplicates easy, and lets one table serve many uses. {r2} Sorted data allows binary search, in big O of log N, but it needs arrays or trees. {r3} We score sorts by counting their comparisons. {r4} Each comparison has two answers, so two, raised to the number of comparisons, must be at least N factorial. {r5} That makes about N log base two of N comparisons unavoidable in the worst case. {r6} And we've made ten thousand random numbers to race on. {pause}

[c1.recap.2] {next} Next time, the first contestant, insertion sort. {cards} It sorts the way you'd sort a hand of cards, picking up one card at a time and slotting it into place. {pause}
