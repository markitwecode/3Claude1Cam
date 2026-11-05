# Chapter 2 · Insertion sort

Foundations of Computer Science · Lecture 5 (Sorting), part 2 of 7. Source: FoCS 2026-27 notes v1.8, pp. 39–40 (§5.2), with Lecture 2's recurrence table (p. 19) and the summary's timings (p. 43).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

All code and replies below were run in OCaml 5.4.1 and are quoted verbatim. Every comparison
count comes from a run with a tallying `le` in place of `<=` (the recipe in project.json).

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card, `title_card("Part 2 · Insertion sort")`: "Sorting", "Foundations of Computer Science · Lecture 5", "Part 2 · Insertion sort".
> On {last}: ch1's scoreboard (import it from `scenes/ch1_s4_contest.py`), rows insertion sort / quicksort / merge sort, every cell a GOLD "?", with its floor line "lower bound ≈ 118,458" beneath; the floor line pulses.
> On {random}: the column header "comparisons on 10,000 random items" pulses, and a DIM strip slides in under the board: `rs = [1484786315.; 925166085.; 1614852353.; …]` (ch1 s7's list, its first three values as printed).
> On {cards}: the scoreboard shrinks to the top-left corner with the insertion sort row lit YELLOW. Ch1's end card returns in the centre, five playing cards showing 3 5 9 4 7 (the card picture is beyond the notes): the 3, 5 and 9 fanned in the hand, already in order, and the 4 and the 7 lying face up a little to the right, DIM "still to pick up".
> On {pick}: the 4 lifts. On {slot}: it slides in between the 3 and the 5, which part to make room; then the 7 does the same, between the 5 and the 9. On {order}: the hand reads 3 4 5 7 9, with a GREEN tick and the label "always in order". This slide-into-place motion comes back in scene 4.
> On {chain}: the cards go back to their dealt order, 3 5 9 4 7, and each card becomes a cell (TransformFromCopy), giving the running chain 3 → 5 → 9 → 4 → 7 → [] (ConsChain, default at ORIGIN).
> On {ask}: two tags under the chain, BLUE "in OCaml?" and GOLD "how many comparisons?".

[c2.hook.1] {title} This is part two of Sorting. {pause=2} {last} Last time, we proved that any sort that works by comparing items needs about N log N comparisons, on its worst input. {random} And we made ten thousand random numbers, to race our sorts on.

[c2.hook.2] {cards} Today, the simplest contestant. It sorts the way most people sort a hand of cards. {pick} You pick up one card at a time, {slot} and slide it into its place among the cards you already hold. {order} So the cards in your hand are always in order. {pause}

[c2.hook.3] {chain} We'll sort our running list, three, five, nine, four, seven, the same way. {ask} How do you write that in OCaml, and how many comparisons does it make? {pause}

## Scene 2 · Inserting one item (ch2_s2_ins)

> The code, hero-sized and centred, laid out as in the notes (`ins` YELLOW, keywords BLUE, `[]` and `::` TEAL): `let rec ins x = function` / `  | [] -> [x]` / `  | y::ys -> if x <= y then x :: y :: ys` / `             else y :: ins x ys`.
> One highlight box slides clause by clause: {nil} `[] -> [x]`; {cons} `y::ys`; {test} `x <= y` (YELLOW); {stop} `x :: y :: ys`; {else} `y :: ins x ys`; on {carry}, `ins x ys` gets its own box, "the smaller problem".
> On {type}: the reply `val ins : 'a -> 'a list -> 'a list = <fun>` (each `'a` PINK, the types GREEN). On {poly}: `<=` in the code flashes, DIM tag "polymorphic (Lecture 4)".
> On {trace}: the code shrinks to the top; the trace builds below it, each line born from a copy of the one above: `ins 4 [3; 5; 9]` / `⇒ 3 :: ins 4 [5; 9]` / `⇒ 3 :: 4 :: 5 :: [9]` / `⇒ [3; 4; 5; 9]`. On {t1} a small GOLD "4 ≤ 3? no" beside line 2; on {t2} "4 ≤ 5? yes" beside line 3. On {done} the toplevel reply `- : int list = [3; 4; 5; 9]`; on {two} a GOLD counter "comparisons: 2".
> On {bad}: `ins 4 [9; 3]`; on {first} the 4 lands in front of the 9; on {wrong} the reply `- : int list = [4; 9; 3]` in RED with a cross, DIM tag "assumes the list is sorted".

[c2.ins.1] {job} At the heart of insertion sort is one small job. Put one item into a list that's already sorted, in its right place. {code} Here's the function. It's called ins, short for insert. {args} It takes the item, ex, and then the sorted list. {nil} If the list is empty, the answer is the list holding just ex.

[c2.ins.2] {cons} Otherwise, the list has a head, why, and a tail, whys. {test} Compare ex with why. {stop} If ex is less than or equal to why, then ex belongs right here, at the front. The answer is ex, consed onto why, consed onto whys. {else} Otherwise, why is the smaller one, so it stays in front, {carry} and we insert ex further along, into whys.

[c2.ins.3] {type} OCaml's reply says that ins takes an alpha, and an alpha list, and returns an alpha list. {poly} It works for any type, because less than or equal is polymorphic, as we saw last lecture. {pause}

[c2.ins.4] {trace} Let's insert four into the list three, five, nine. {t1} Is four at most three? No. So the three stays in front, and we insert four into five, nine. {t2} Is four at most five? Yes. So the four goes in front of the five, and the nine follows. {done} The answer is three, four, five, nine, {two} after two comparisons. {pause}

[c2.ins.5] {assume} One warning. Ins simply trusts that its list is already sorted. {bad} Insert four into the list nine, three. {first} Four is at most nine, so it goes in front, and ins stops. {wrong} You get four, nine, three, still out of order. {pause}

## Scene 3 · What insert copies (ch2_s3_cells)

> Cells in memory (ConsChain), as in L4 ch1 s5: the sorted list 3 → 5 → 9 → [] across the middle, BLUE, with a YELLOW pointer `old` on the 3 (on {old}).
> On {three}: a new YELLOW cell 3 is born above, from a copy of the original 3 (TransformFromCopy). On {four}: a new YELLOW cell 4 beside it. On {five}: a new YELLOW cell 5, born from a copy of the original 5. On {share}: the new 5's arrow reaches down into the ORIGINAL 9; on {shared} the 9 → [] glows TEAL, label "shared". A pointer `fresh` on the new 3. The original chain is untouched.
> On {drop}: a small DIM inset of L4 ch1 s5's drop picture (the rebuilt 9 pointing into the original 4 → 7 → [], "shared").
> On {check}: Code at the bottom, `==` in YELLOW, replies as printed: `let old = [3; 5; 9]` → `val old : int list = [3; 5; 9]`, `let fresh = ins 4 old` → `val fresh : int list = [3; 4; 5; 9]`. On {five2}: `List.tl (List.tl fresh) == List.tl old`, and on {false} `- : bool = false` (the two 5 cells, old and new, flash side by side). On {nine}: `List.tl (List.tl (List.tl fresh)) == List.tl (List.tl old)` → `- : bool = true` (the one shared 9 flashes).
> On {waits}: the Code clears; a small copy of `ins`'s last line, `else y :: ins x ys`, with `y ::` flashing YELLOW, label "waits" (take's waiting cons, L4 ch1).
> On {cost}: GOLD counter "new cells: 3" beside the picture, then GOLD "1 comparison + 1 copied cell per step" and "O(steps) time and space".
> On {end}: `ins 10 [3; 5; 9]` → `- : int list = [3; 5; 9; 10]`, drawn as four new YELLOW cells with nothing TEAL; the counter reads "new cells: 4".

[c2.cells.1] {cells} Now let's look at the cells in memory. {old} Here's the sorted list, three, five, nine. Call it old. {three} The three stays at the front of the answer, but it must point at a new tail, so ins builds a new cell for it. {four} Then a new cell for the four. {five} And look at the clause that stopped. Why consed onto whys builds a brand new cell, holding the same five. {pause}

[c2.cells.2] {share} Its arrow points straight back into the old list, at the nine. {shared} So the nine is shared, not copied. {drop} It's the same trick as drop, last lecture, which also rebuilt a single cell, and shared the rest. {pause}

[c2.cells.3] {check} You can check this in OCaml. Call the answer fresh. Two equals signs ask whether two values are the very same cells in memory. {five2} Is the five in fresh the very same cell as the five in old? {false} False. {nine} But the nine is the very same, so that one gives true.

[c2.cells.4] {waits} Notice too that ins leaves work waiting. Each item it walks past waits to be consed onto the answer, just like in take, last lecture. {cost} So the further ins walks, the more it costs. Each step takes one comparison and one copied cell, so its time and space both grow with how far it walks. {end} Insert ten into three, five, nine, and it walks to the very end, copying the whole list. {pause}

## Scene 4 · Sorting by inserting (ch2_s4_insort)

> `ins`'s code shrinks to the top-left corner, kept as a reference. The new code, hero-sized (`insort` YELLOW): `let rec insort = function` / `  | [] -> []` / `  | x::xs -> ins x (insort xs)`. Box slides: {nil} `[] -> []`; {cons} `x::xs`; {sorttail} `insort xs`; {insert} `ins x (…)`. On {type}: the reply `val insort : 'a list -> 'a list = <fun>`.
> On {trace}: the code moves up; the running chain 3 → 5 → 9 → 4 → 7 → [] sits under it. On {unfold}: `insort [3; 5; 9; 4; 7]` unfolds into `ins 3 (ins 5 (ins 9 (ins 4 (ins 7 []))))`, each `ins k` born from its cell in the chain (TransformFromCopy). On {wait} the waiting `ins 3`, `ins 5`, `ins 9`, `ins 4` turn YELLOW under a brace "waiting". On {nlength} a small DIM inset of L3's `1 + (1 + (1 + 0))`. On {first} the innermost `ins 7 []` is boxed.
> On {r1} … {r5}: the nest collapses from the inside out, one insert per mark, while a sorted chain grows beneath, each new item sliding into its slot (the hook's card motion), with a GOLD count under each step: `[7]` 0 · `[4; 7]` 1 · `[4; 7; 9]` 2 · `[4; 5; 7; 9]` 2 · `[3; 4; 5; 7; 9]` 1. On {result} the final chain gets the lecture's GREEN tick, with the reply `- : int list = [3; 4; 5; 7; 9]`.
> On {count}: the five GOLD counts gather into `0 + 1 + 2 + 2 + 1 = 6`. On {floor}: ch1's GOLD "7" (the floor for five items) appears beside it, labelled "worst input, any comparison sort"; on {easy} the 6 sits just under the 7, GREEN.
> On {summary}: DIM caption, the notes' line: "Items from the input are copied one at a time to the output. Each new item is inserted into the right place so that the output is always in order."
> On {strings}: `insort ["dog"; "cat"; "emu"]` → `- : string list = ["cat"; "dog"; "emu"]` (the strings YELLOW, the type GREEN).

[c2.insort.1] {code} With ins in hand, the sort itself takes two lines. We'll call it in-sort. {nil} The empty list is already sorted. {cons} For a list with head ex and tail exes, {sorttail} first sort the tail, {insert} then insert ex into the result. {type} OCaml says that in-sort takes an alpha list, and returns an alpha list. {pause}

[c2.insort.2] {trace} Let's run it on our list, three, five, nine, four, seven. {unfold} In-sort must sort the rest before it can insert the three, and the same goes for the five, the nine and the four. {wait} So the inserts pile up and wait, {nlength} like the one-pluses in lecture three's length function. {first} The innermost insert, of the seven, runs first. So, unlike our hand of cards, the last item goes in first. {pause}

[c2.insort.3] {r1} Seven into nil gives the list seven, with no comparisons. {r2} Four goes in front of seven, after one. {r3} Nine walks past four and seven to the end, two comparisons. {r4} Five passes four and stops at seven, two more. {r5} And three stops at once, in front of four, just one. {result} Three, four, five, seven, nine. {pause}

[c2.insort.4] {count} Add them up. Zero, one, two, two and one make six comparisons. {floor} Last time, we found that some arrangement of five items needs at least seven. {easy} Six fits that rule, because the bound is about the worst input, and this input happens to be easy for insertion sort.

[c2.insort.5] {summary} So that's the whole idea. Items from the input are copied, one at a time, to the output, each into its right place. So the output is always in order. {strings} And since less than or equal works at any type, the same code sorts strings. Dog, cat, emu becomes cat, dog, emu.

## Scene 5 · Counting the comparisons (ch2_s5_cost)

> One insert: a sorted chain of ten cells, values 1 to 10, with a new item hovering above. On {ten} it drops in at the far left, GOLD "1 comparison", then lifts and drops in at the far right, GOLD "10 comparisons" (checked: `ins 0` and `ins 11` into `[1; …; 10]` make 1 and 10). On {half} it lands in the middle, GOLD "about 5", then "about half the list" (the notes' "n/2 comparisons on average").
> On {sum}: a staircase of GOLD rows of blocks, 0, 1, 2, …, n − 1, one row per insert (L3 ch4 s6's staircase). On {worst} the label `0 + 1 + 2 + ⋯ + (n − 1)`. On {eq}: MathTex `T(n+1) = T(n) + n`.
> On {table}: Lecture 2's recurrence table slides in beside it, as on p. 19: `T(n+1) = T(n) + 1   O(n)` / `T(n+1) = T(n) + n   O(n²)` / `T(n) = T(n/2) + 1   O(log n)` / `T(n) = 2T(n/2) + n   O(n log n)`; the second row lights YELLOW, DIM tag "nsumsum". On {closed}: `= n(n − 1)/2`, then RED `O(n²)`.
> On {average}: every row of the staircase dims to half its length, and the label becomes `≈ n²/4`. On {quad}: RED "quadratic".
> On {predict}: n = 10,000, GOLD `n²/4 = 25,000,000`. On {count}: beneath it, GOLD `25,146,194` (DIM caption "counted with a tallying <="). On {floor}: ch1's floor line "lower bound ≈ 118,458" below, and GOLD "× 212".
> On {board}: the scoreboard returns, and insertion sort's row fills its two cells: "25,146,194", then on {secs} "174 s".
> On {laptop}: a DIM aside under the board, beyond the notes, measured in the OCaml 5.4.1 toplevel on an Apple M1 Max: "insertion sort < 1 s" (runs vary, 0.6–0.8 s); on {quick}, "quicksort < 0.01 s" beside it (quicksort's row itself stays "?").

[c2.cost.1] {one} So how much work is one insert? {ten} Inserting into a sorted list of ten items takes anywhere from one comparison to ten, depending on where the new item belongs. {half} On random data, it lands somewhere in the middle, so it takes about five. In general, an insert does about half as many comparisons as the list has items. {pause}

[c2.cost.2] {sum} Now the whole sort. In-sort inserts into a list of zero items, then one, then two, and so on. {worst} At worst, each insert walks the whole list, so the comparisons add up to zero, plus one, plus two, all the way to N minus one. {eq} As a recurrence, sorting one more item adds at most N comparisons. Tee of N plus one equals tee of N, plus N.

[c2.cost.3] {table} That's a row of lecture two's table, the one for N-sum-sum. {closed} It adds up to N times N minus one, over two. Big O of N squared. {average} On average, each insert does half that work, so insertion sort makes about N squared over four comparisons. {quad} Still big O of N squared. Quadratic. {pause}

[c2.cost.4] {measure} Let's check that on our ten thousand random numbers. {predict} The formula, N squared over four, predicts twenty-five million. {count} As in part one, we counted with a less than or equal that keeps a tally. In-sort makes twenty-five million, one hundred and forty-six thousand, one hundred and ninety-four. Very close. {floor} That's two hundred and twelve times last chapter's floor, of about a hundred and eighteen thousand. {pause}

[c2.cost.5] {board} So insertion sort takes its place on the scoreboard. {secs} On the Deck Station, it took a hundred and seventy-four seconds, nearly three minutes, for ten thousand numbers. {laptop} On a laptop today, it takes under a second. {quick} That sounds fine, until you see that quicksort sorts the same list in under a hundredth of a second. {hardware} As lecture two said, faster hardware only makes better algorithms matter more.

## Scene 6 · Best and worst inputs (ch2_s6_bestworst)

> Beyond the notes; every count below was checked (OCaml 5.4.1, tallying `<=`).
> On {which}: GOLD "6" (the chain) and "25,146,194" (random `rs`) side by side. On {ask}: two chains appear, top `3 → 4 → 5 → 7 → 9 → []` labelled GREEN "sorted", bottom `9 → 7 → 5 → 4 → 3 → []` labelled RED "reversed", a YELLOW "?" over each.
> On {sorted}: the top chain runs through insort with scene 4's slide-into-place motion; on {stop} each insert stops at its first comparison, GOLD counts 0 · 1 · 1 · 1 · 1. On {four}: GOLD "4 comparisons = n − 1". On {sortedrs}: GOLD "sorted rs: 9,999"; on {linear} GREEN "O(n)".
> On {reversed}: the bottom chain runs the same way; on {walk} each new item walks the whole sorted part to the nil, GOLD counts 0 · 1 · 2 · 3 · 4. On {ten}: `0 + 1 + 2 + 3 + 4 = 10 = n(n − 1)/2`. On {revrs}: GOLD "reversed rs: 49,995,000", RED "O(n²)".
> On {range}: a horizontal GOLD scale of comparisons for 10,000 items, three ticks: 9,999 (sorted, GREEN) · 25,146,194 (random) · 49,995,000 (reversed, RED).
> On {remember}: the sorted chain gets a YELLOW frame and a DIM tag "quicksort's worst case (Part 4)".

[c2.best.1] {which} Six comparisons for our chain, twenty-five million for the random list. {kinder} Some inputs are much kinder to insertion sort than others. {ask} Which input is the best for it, and which is the worst? {pause=1.5}

[c2.best.2] {sorted} Try a list that's already sorted, three, four, five, seven, nine. {stop} Each item is smaller than everything after it, so every insert stops at its very first comparison. {four} That's four comparisons in all, one fewer than the number of items. {sortedrs} Sort our ten thousand numbers, then sort the result again, and it takes nine thousand, nine hundred and ninety-nine. {linear} On sorted input, insertion sort is linear.

[c2.best.3] {reversed} Now reverse it, nine, seven, five, four, three. {walk} This time each item is bigger than everything already sorted, so every insert walks the whole way, to the end. {ten} Zero, plus one, plus two, plus three, plus four. Ten comparisons, which is N times N minus one, over two. {revrs} Reversed, our ten thousand numbers take forty-nine million, nine hundred and ninety-five thousand. That's the worst case exactly, and about twice the random case. {pause}

[c2.best.4] {range} So insertion sort ranges from linear, on sorted input, to quadratic, on reversed input, with random input costing about half the worst. {remember} Keep sorted input in mind. It's insertion sort's favourite, but quicksort, in part four, will find it the hardest of all.

## Scene 7 · Why bother, and recap (ch2_s7_why)

> On {slow}: a YELLOW "why so slow?". On {cause}: three candidate causes in a row, GOLD boxes "O(n²) comparisons" and "lots of copying", and a DIM box "recursion". On {iter} the DIM box is struck through, with L3 ch4's maxim in DIM beneath: "Never add an accumulator merely out of habit."
> On {useless}: big RED "174 s" labelled "insertion sort", and on {times} a GOLD "1.4 s" beside it labelled "next-worst of the three" (both the notes' DECstation times; which sort it is stays a "?" on the scoreboard until Part 5, as in the notes' §5.2).
> On {worth}: GREEN tags "easy to code" and "shows the concepts". On {refine}: `ins` at the root of a small tree, two branches to "merge sort" and "heapsort" (ch1's on-screen spelling), labelled "refinements". On {merge}: `ins x ys` turns into `merge (xs, ys)` (TransformMatchingStrings), DIM "Part 5".
> Recap on {recap}: four short lines, one per mark ({r1} to {r4}), each with a small icon from the chapter: scene 3's cells (YELLOW copies, TEAL "shared"); the `insort` code in miniature with the GREEN-ticked chain; the halved staircase with "≈ n²/4, O(n²)"; the scale from scene 6, "sorted: n − 1 · reversed: n(n − 1)/2".
> Teaser on {next}: ch3's opening picture, the scoreboard with insertion sort's row filled ("25,146,194", "174 s") and quicksort's row lit YELLOW, its "?" cells pulsing. On {divide}: beneath it, the chain as `5 → 3 → 9 → 4 → 7`, the 5 YELLOW lifting as the pivot, 3 and 4 dropping to the left under "≤ 5", 9 and 7 to the right under "> 5" (ch3 s2's picture). Leave about 8 s of end card after the last word; the music carries it.

[c2.why.1] {slow} So what makes insertion sort slow? {cause} Its big O of N squared comparisons, and all that list copying. {iter} We could easily write iterative versions of ins and in-sort, but to no purpose. An accumulator would leave the comparisons and the copying exactly as they are. {pause}

[c2.why.2] {useless} The notes call insertion sort nearly useless. {times} It takes a hundred and seventy-four seconds on our list, while the next-worst of our three sorts takes just one point four seconds. {pause}

[c2.why.3] {worth} So why learn it at all? {easy} It's easy to code, and it shows the key ideas. {refine} And two efficient sorts, merge sort and heap sort, can be seen as refinements of it. {merge} In part five, merge sort's merge does what ins does, but with a whole sorted list instead of one item.

[c2.why.4] {recap} Let's recap. {r1} Ins puts one item into a sorted list. It copies every cell up to where it stops, and shares the rest. {r2} In-sort first sorts the tail, then inserts the head, so its output is always in order. {r3} Each insert does about half as many comparisons as the list has items, so the whole sort makes about N squared over four. Quadratic. {r4} Sorted input costs only N minus one comparisons, and reversed input costs N times N minus one, over two. {pause}

[c2.why.5] {next} Next time, a much faster contestant, quicksort. {divide} It picks one item, splits the rest into the smaller ones and the larger ones, and sorts each part on its own. {pause}
