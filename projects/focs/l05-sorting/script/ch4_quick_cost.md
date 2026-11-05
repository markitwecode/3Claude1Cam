# Chapter 4 · How good is quicksort?

Foundations of Computer Science · Lecture 5 (Sorting), part 4 of 7. Source: FoCS 2026-27 notes v1.8, p. 41 (§5.4, the cost paragraphs), pp. 41–42 (§5.5), with Lecture 2's recurrence table (p. 19) and the summary's timing (p. 43).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

All code and replies below were run in OCaml 5.4.1 and are quoted verbatim. Every comparison
count comes from a run with a tallying `le` in place of `<=` (the recipe in project.json). The
append-copy count (76,447) comes from a `quick` that also adds `List.length (quick l)` at each
`@`. The partitions and calls drawn in scenes 3 and 5 come from traced versions of `quick` and
`quik` that print each call. The code's names are said as in ch3: `a` "ay", `bs` "bees", `l`
"ell", `r` "ar", `@` "append"; `rs` is "ar-ess" (ch1). `quik` and `quick` sound the same, so from
scene 4 on `quik` is said "quick with accumulator", and where both appear, the original is
"plain quick".

Shared pictures: ch3 s6 exports `call_tree()` from `scenes/ch3_s6_trace.py` (the call tree of
`quick [3; 5; 9; 4; 7]`); this chapter calls back to it in scenes 1, 2 and 5 instead of
redrawing it. This chapter's builders should export two trees for later chapters: scene 2's
balanced recursion tree as `recursion_tree()` in `scenes/ch4_s2_average.py` (ch5 s6 relabels it
for merge sort with 10,000 / 5,000 / 2,500; ch6 s1, s2 and s6 show it small), and scene 3's
zigzag tree on the sorted chain as `worst_tree()` in `scenes/ch4_s3_worst.py` (ch5 s1 opens on
it; ch5 s6 and ch6 s6 show it small). Quicksort's colours follow ch3: pivots YELLOW, `quick`, `quik` and `part`
YELLOW, `[]` and `::` TEAL, `@` GOLD.

---

## Scene 1 · Hook (ch4_s1_hook)

> Title card, `title_card("Part 4 · How good is quicksort?")`: "Sorting", "Foundations of Computer Science · Lecture 5", "Part 4 · How good is quicksort?".
> On {last}: ch3's end card returns, rebuilt as in `scenes/ch3_s7_recap.py`'s teaser: the scoreboard (`make_scoreboard(bound="118,458")` from `scenes/ch1_s4_contest.py`), small, with insertion sort's row "25,146,194" / "174 s", quicksort's row "158,058" / "0.74 s" lit YELLOW, merge sort's row still GOLD "?", the floor "lower bound ≈ 118,458"; beside it ch3 s6's pivot tree (`call_tree()` from `scenes/ch3_s6_trace.py`) in its final circle form: 3 at the top, 7 below-right, 5 and 9 under the 7, 4 under the 5, pivots YELLOW, the root's empty left branch RED, a YELLOW "?" over the root; and the DIM struck-through `(quick l) @ (a :: quick r)`, its `@` GOLD, in a corner.
> On {fast}: the board grows to full size in the centre; quicksort's two cells pulse, and insertion sort's "174 s" glows RED beside them.
> On {tree}: the board shrinks back to the top-left corner (quicksort's row still YELLOW), and the pivot tree takes the centre.
> On {lopsided}: the root's two branches get the labels ch3 gave them, "0" on the empty left (its RED glow pulses) and "4" on the right; the YELLOW "?" pulses, and a caption reads "lopsided".
> On {ask}: the tree shrinks a little; a YELLOW question above it, "Why is it usually so fast?". On {wrong}: a second line, "What if every split is lopsided?". On {later}: a DIM third line, "Then: quicksort without @", with the struck-through `(quick l) @ (a :: quick r)` from the corner sliding in beside it.

[c4.hook.1] {title} This is part four of Sorting. {pause=2} {last} Last time, we met quicksort. It picks a pivot, splits the other items around it, and sorts each part. {fast} On our ten thousand random numbers, it made a hundred and fifty-eight thousand and fifty-eight comparisons. On the Deck Station, that took zero point seven four seconds, where insertion sort took a hundred and seventy-four.

[c4.hook.2] {tree} Here's the tree of pivots from our five-item list. {lopsided} Its first split was lopsided. The pivot, three, was the smallest item, so nothing went left, and all four others went right. {pause}

[c4.hook.3] {ask} So this chapter asks two questions. Why is quicksort usually so fast? {pause} {wrong} And what happens when every split is lopsided? {pause} {later} Then we'll make it faster still, by getting rid of its append.

## Scene 2 · The average case (ch4_s2_average)

> On {part}: the hook's tree clears. A wide BLUE box across the upper middle, labelled "n items", with a YELLOW square at its left end, "pivot". On {compare}: GOLD ticks run along the box, one per item, and GOLD "about n comparisons" beneath. On {halves}: the box splits into two boxes of half the width just below it, each labelled "n/2", the YELLOW pivot square between them.
> On {eq}: at the top right, MathTex `T(n) = 2T(n/2) + n`, with GOLD underbraces on `n` ("split") and on `2T(n/2)` ("two halves"). On {base}: `T(1) = 1` beside it.
> On {table}: ch2 s5's Lecture 2 table slides in small beneath it, the same four rows as on p. 19 (`T(n+1) = T(n) + 1   O(n)` / `T(n+1) = T(n) + n   O(n²)` / `T(n) = T(n/2) + 1   O(log n)` / `T(n) = 2T(n/2) + n   O(n log n)`); the last row lights YELLOW, DIM tag "Lecture 2: listed, not derived". Then the table clears; the recurrence stays at the top right.
> On {tree}: ch3's call tree (`call_tree()` from `scenes/ch3_s6_trace.py`, in its list-node form with the GOLD badges 4, 3, 1, 0) appears small at the left, DIM tag "Part 3: our five items". Then the recursion tree grows in the centre out of the split boxes (TransformFromCopy): {root} one box "n" at the top; {level1} two boxes "n/2"; {level2} four boxes "n/4"; then a "⋮" and, at the bottom, a row of many tiny boxes "1". Every row has the same total width, which is the point of the picture. Build this tree in one exported function, `recursion_tree()`, with the labels as parameters: ch5 s6 relabels it "10,000", "5,000", "2,500" for merge sort, and ch6 shows it small.
> On {work}: a GOLD sum appears at the right end of each row: {row0} "n"; {row1} "2 × n/2 = n"; {row2} "4 × n/4 = n". On {every}: all the GOLD n's glow together.
> On {levels}: a GOLD bracket down the left side with a "?"; on {halve}, the sizes n, n/2, n/4, …, 1 light in turn down the tree, and the bracket now reads "log₂ n levels". On {total}: `n \times \log_2 n` boxed under the tree, and the table's `O(n log n)` comes back beside it, GREEN.
> On {tenk}: the tree shrinks left. GOLD `\log_2 10{,}000 \approx 13.3`, with a small DIM caption under it, "perfect splits: 14 levels, the last only partly filled", then `10{,}000 \times 13.3 \approx 133{,}000` (checked: a balanced tree of 10,000 nodes has 14 levels, since 2¹³ − 1 < 10,000 ≤ 2¹⁴ − 1; the tree `quick` really builds on `rs` is 27 levels deep, so the caption says "perfect splits", not "the tree"). On {measured}: beneath it, GOLD `158,058`, with DIM "counted by us: a tallying ≤" (the scoreboard's tag). On {imperfect}: the small tree's rows wobble into uneven splits (one part wider than the other, by a different amount in each), caption "random pivots: seldom exact halves". On {aho}: DIM "proof: Aho, p. 94" (the notes' reference).
> On {ratio}: RED "174 s" (insertion sort) and GREEN "0.74 s" (quicksort), the notes' DECstation times, then GOLD "≈ 235 × faster" (174 / 0.74 = 235, the notes' figure).

[c4.avg.1] {part} Start with why it's fast. Last time, we saw that quicksort's speed depends on how evenly its pivots split. {compare} To sort N items, quicksort first compares every other item with the pivot, once each. That's about N comparisons. {halves} On random data, the pivot usually lands somewhere near the middle, so the two parts hold about half the items each. {pause}

[c4.avg.2] {eq} So sorting N items costs N comparisons for the split, plus the cost of sorting two halves. Tee of N equals two tee of N over two, plus N. {base} And as in lecture two, the smallest case costs one unit. {table} That's the last row of lecture two's table, big O of N log N. Lecture two only listed it, so let's see where it comes from.

[c4.avg.3] {tree} Last time, we drew the calls for our five items as a tree. Now draw that tree for N items, with perfect splits. {root} At the top, one call splits all N items. {level1} Below it, two calls split half of them each. {level2} Below those, four calls split a quarter each, and so on, down to parts of one item. {work} Now add up the work on each level. {row0} The top level splits N items. {row1} The next level has two halves, which is N items again. {row2} Then four quarters, still N. {every} So every level handles about N items.

[c4.avg.4] {levels} So how many levels are there? {pause} {halve} At each level, the parts are half as big. Starting from N, it takes log base two of N halvings to get down to one. {total} So there are log base two of N levels, with about N comparisons on each. That's about N log base two of N in all. Big O of N log N. {pause}

[c4.avg.5] {tenk} For ten thousand items, log base two of ten thousand is about thirteen point three. Thirteen halvings don't quite get down to single items, so with perfect splits the tree would have fourteen levels, the last one only partly filled. Ten thousand times thirteen point three predicts about a hundred and thirty-three thousand comparisons. {measured} We counted a hundred and fifty-eight thousand and fifty-eight. {imperfect} A little more, because random pivots seldom split the items exactly in half. {aho} The notes say it's not hard to prove that quicksort makes about N log N comparisons on average, and they point to a proof in a book by Aho. {ratio} And on the Deck Station, quicksort was about two hundred and thirty-five times faster than insertion sort.

## Scene 3 · The worst case (ch4_s3_worst)

> On {sorted}: the sorted chain `3 → 4 → 5 → 7 → 9 → []` across the top (ConsChain, as in ch2 s6, GREEN label "sorted"). Below it, its call tree grows one call per mark, in ch3 s6's node style (`call_tree([3, 4, 5, 7, 9])` from `scenes/ch3_s6_trace.py`): each node a small list in brackets with its pivot YELLOW and a GOLD comparison badge, the left child holding the "≤" part and the right child the ">" part.
> {p1} root `[3; 4; 5; 7; 9]`, pivot 3: left child `[]`, glowing RED as in ch3; right child `[9; 7; 5; 4]`; badge "4". On {flip}: the right child's reversed order is underlined, with DIM tag "part builds its parts backwards (Part 3)".
> {p2} node `[9; 7; 5; 4]`, pivot 9: left child `[4; 5; 7]`, right child `[]` (RED); badge "3". {p3} node `[4; 5; 7]`, pivot 4: left `[]` (RED), right `[7; 5]`, badge "2"; then node `[7; 5]`, pivot 7: left `[5]`, right `[]` (RED), badge "1"; `[5]` is a leaf, badge "0". (Checked with a traced `quick`: these are exactly the parts it builds.)
> On {stick}: the lists fade to pivot circles, as ch3 s6 did: the tree is one long zigzag branch, 3, 9, 4, 7, 5, every node with one RED empty side. It zigzags rather than running down one diagonal, because part's backwards accumulator turns each sorted part into a reversed one and back; ch5 s1 opens on this picture. Caption "every pivot the smallest or the largest". On {ten}: GOLD `4 + 3 + 2 + 1 = 10`, beside ch3's GOLD "8" for the running chain (checked: `quick [3; 4; 5; 7; 9]` makes 10, and `quick [3; 5; 9; 4; 7]` makes 8). Export this tree as `worst_tree()` (e.g. a wrapper on `call_tree([3, 4, 5, 7, 9])` that adds the RED empty sides), in both forms: ch5 s1, ch5 s6 and ch6 s6 reuse it.
> On {eq}: the zigzag shrinks left; MathTex `T(n+1) = T(n) + n`. On {table}: ch2 s5's table returns small, its second row `T(n+1) = T(n) + n   O(n²)` lit YELLOW with DIM "insertion sort's row (Part 2)"; RED `O(n²)`. On {rs}: GOLD "sorted rs: 49,995,000" `= n(n − 1)/2`; on {rev}: "reversed rs: 49,995,000" under it (both checked; `rs` sorted by `quick`, then `List.rev` of that).
> On {almost}: a long row of small sorted cells; in every block of ten, the first two cells swap places. GOLD "44,996,000" (checked: those 1,000 swaps in sorted `rs`), caption "almost sorted: nearly as bad".
> On {irony}: ch2 s6's comparison scale (`range_scale()` from `scenes/ch2_s6_bestworst.py`) with its GREEN tick "9,999 (sorted)" for insertion sort; a RED tick for quicksort lands at 49,995,000 for the same sorted input. Ch2 s6's DIM tag "quicksort's worst case (Part 4)" comes back beside it, now YELLOW.
> On {shuffle}: the sorted chain's cells shuffle into the running chain's order, 3 5 9 4 7 (cells slide, arrows redraw), GOLD "8"; beside it GREEN "random order, like rs: 158,058". On {unlikely}: caption "randomise the input: the worst case becomes highly unlikely".

[c4.worst.1] {sorted} Now the lopsided split. Give quicksort a list that's already sorted, three, four, five, seven, nine. {p1} The first pivot is three, the smallest item, so every other item goes right, and the left part is empty. That's four comparisons, just to set the three aside. {flip} And as we saw last time, part builds its parts backwards, so the right part comes out as nine, seven, five, four.

[c4.worst.2] {p2} Now the pivot is nine, the largest, so everything goes left. Three comparisons. {p3} Next, four is the smallest, and then seven is the largest. {stick} Every pivot is the smallest or the largest of what's left, so the tree is one long branch. It zigzags, because part keeps turning the order round. {ten} Four, plus three, plus two, plus one. Ten comparisons, where our running list needed only eight. {pause}

[c4.worst.3] {eq} In general, each call sets aside only its pivot. So sorting N plus one items costs N comparisons, plus sorting the other N. Tee of N plus one equals tee of N, plus N. {table} That's insertion sort's row of the table, big O of N squared. {rs} Sort our ten thousand numbers, then quicksort the result. It takes forty-nine million, nine hundred and ninety-five thousand comparisons, exactly N times N minus one, over two. {rev} Reversed input costs exactly the same. {pause}

[c4.worst.4] {almost} Almost sorted input is nearly as bad. Swap one pair of neighbours in every ten, and quicksort still makes nearly forty-five million. {irony} Remember that sorted input was insertion sort's favourite, at nine thousand, nine hundred and ninety-nine? It's quicksort's worst. {pause} {shuffle} The cure is to randomise the input first. Shuffled, a sorted list is just a list in random order, like ar-ess. {unlikely} Then the worst case becomes highly unlikely.

## Scene 4 · Without append (ch4_s4_quik)

> On {append}: ch3 s4's `quick` code, small at the top, laid out and coloured as ch3 shows it (`quick` and `part` YELLOW, `@` GOLD), with the line `        | [] -> (quick l) @ (a :: quick r)` boxed. On {copies}: under it, `quick l`'s answer as a short chain of YELLOW cells, copied cell by cell by `@` into new cells (L3 ch4 s6's GOLD copy braces), GOLD "copies the whole left answer".
> On {revapp}: a DIM inset of L3 ch4 s7's card piles, with `rev_app [1; 2; 3] [4; 5]` ⇒ `[3; 2; 1; 4; 5]`, labelled "Lecture 3: an accumulator instead of @". On {same}: the label flashes YELLOW.
> On {code}: `quick` and the inset clear. The notes' code arrives hero-sized (`quik` and `part` YELLOW, keywords BLUE, `[]` and `::` TEAL), laid out exactly as in the notes: `let rec quik = function` / `  | ([], sorted) -> sorted` / `  | ([x], sorted) -> x::sorted` / `  | a::bs, sorted ->` / `     let rec part = function` / `       | l, r, [] -> quik (l, a :: quik (r, sorted))` / `       | l, r, x::xs ->` / `           if x <= a then` / `             part (x::l, r, xs)` / `           else` / `             part (l, x::r, xs)` / `     in` / `     part ([], [], bs)`.
> On {name}: above the code, a `quick` turns into `quik` as its "c" drops out (TransformMatchingStrings), DIM caption "the notes' name", and under it a DIM line, "said: quick with accumulator". On {pair}: `sorted` in the first clause is boxed. On {meaning}: a line above the code, `quik (xs, sorted) = quick xs @ sorted`, with GREEN "means" and DIM "but with no @" (checked: `quik ([9; 1; 8], [6; 0; 7]) = quick [9; 1; 8] @ [6; 0; 7]` ⇒ `- : bool = true`).
> One highlight box slides clause by clause: {nil} `| ([], sorted) -> sorted`; {one} `| ([x], sorted) -> x::sorted`; {cons} `| a::bs, sorted ->`; {part} `let rec part = function`, with the triples `l, r, []` and `l, r, x::xs` lit; {split} `part (x::l, r, xs)` and `part (l, x::r, xs)`; {start} `part ([], [], bs)`; {combine} `| l, r, [] -> quik (l, a :: quik (r, sorted))`; on {noapp} its `a ::` glows TEAL, with GREEN "no @".
> On {type}: the reply `val quik : 'a list * 'a list -> 'a list = <fun>` (each `'a` PINK, the types GREEN). On {call}: `quik (rs, [])` beneath it (no reply shown).
> On {test}: the code shrinks up; `quik ([3; 5; 9; 4; 7], [100; 200]);;`. On {result}: `- : int list = [3; 4; 5; 7; 9; 100; 200]`, the sorted five GREEN and `100; 200` DIM.
> On {slip}: a DIM quote of the notes, "Calling quik(xs, sorted) reverses the elements of xs and prepends them to the list sorted."; on {sorts}, "reverses" is struck through in RED, and "sorts" is written above it in GREEN.

[c4.quik.1] {append} Quicksort has one more cost, hidden in its last step. {copies} Its append copies the whole sorted left part, at every call. {revapp} In lecture three, rev-app got rid of an append with an accumulator, an extra argument that holds the answer built so far. {same} The same trick works here. {pause}

[c4.quik.2] {code} Here's the append-free version. {name} The notes spell its name Q, U, I, K, which is quick without the C. Out loud, the two names sound the same, so we'll call the new one quick with accumulator. {pair} It takes a pair of lists. The first, exes, is the list to sort, and the second is called sorted. {meaning} The answer is exes sorted, in front of sorted, but it never appends. {nil} If exes is empty, the answer is just sorted. {one} With one item, ex, cons it on the front of sorted.

[c4.quik.3] {cons} Otherwise, the list has a pivot, ay, and the rest, bees. {part} The local function part splits the rest as before, except that it takes one triple, holding ell, ar, and the items still to split. {split} Items no bigger than the pivot go onto ell, and the others onto ar. {start} It starts with both parts empty.

[c4.quik.4] {combine} When nothing is left to split, part combines the pieces, in one line. One call sorts ar in front of sorted, the pivot is consed onto that, and a second call sorts ell in front of the lot. {noapp} There's no append anywhere. {type} OCaml says that quick with accumulator takes a pair of alpha lists, and returns an alpha list. {call} To sort ar-ess, give it an empty list as sorted.

[c4.quik.5] {test} Let's try it with sorted holding a hundred and two hundred. We sort three, five, nine, four, seven in front of them. {result} We get three, four, five, seven, nine, then a hundred and two hundred. {slip} The notes say that this function reverses exes, like rev-app, and puts them in front of sorted. {sorts} That's a slip. It sorts them. {pause}

## Scene 5 · Building from the right (ch4_s5_order)

> The combine line from scene 4, `| l, r, [] -> quik (l, a :: quik (r, sorted))`, large at the top. On {first}: `quik (r, sorted)` boxed YELLOW with a GOLD "1"; on {then}, `a ::` boxed, GOLD "2"; on {last}, the outer `quik (l, …)` boxed, GOLD "3". On {right}: a GOLD arrow pointing right to left along the line, "built from the largest end".
> On {tree}: the line shrinks to the top. Ch3's call tree for the running chain (`call_tree()` from `scenes/ch3_s6_trace.py`, in its list-node form: root `[3; 5; 9; 4; 7]`, children `[]` and `[7; 4; 9; 5]`, then `[5; 4]` and `[9]`, then `[4]` and `[]`, pivots YELLOW) fills the left two-thirds. At the right, the answer row, labelled `sorted`, holds only a TEAL `[]`.
> The walk, one call per mark, a YELLOW highlight on the current node and the call written beside it, verbatim: {root} `quik ([7; 4; 9; 5], [])` (the root's right child); {seven} at pivot 7, its children `[5; 4]` and `[9]` flash; {nine} `quik ([9], [])` ⇒ `[9]`, and a GREEN cell 9 is consed onto the answer row's `[]`, at its right end; {cons7} a GREEN cell 7 is consed in front: `[7; 9]`.
> {five} `quik ([5; 4], [7; 9])`; {pivot5} at pivot 5, its children `[4]` and `[]` flash; {cons5} cell 5 is consed in front: `[5; 7; 9]`; {cons4} `quik ([4], [5; 7; 9])` ⇒ `[4; 5; 7; 9]`; {cons3} back at the root, 3 is consed on, then `quik ([], [3; 4; 5; 7; 9])` ⇒ `[3; 4; 5; 7; 9]`, which gets the lecture's GREEN tick.
> (Checked with a traced `quik` in OCaml 5.4.1: it makes exactly these calls, in this order, and `quik ([5; 4], [7; 9])` ⇒ `- : int list = [4; 5; 7; 9]`. In ch3 s6 the answers flowed up the same tree by appends; here they never leave the answer row.)
> On {once}: the five answer cells flash in the order they were consed, 9, 7, 5, 4, 3, each with a GOLD "1 cons". On {noapp}: GREEN "nothing appended". On {cards}: a DIM inset of L3 ch4 s7's card piles beside the answer row, cards landing one at a time on the new pile.

[c4.order.1] {order} Look closely at that combine line. {first} The call that sorts ar runs first, because its answer is needed as an argument. {then} Then ay is consed onto that. {last} The call that sorts ell, the left part, comes last. {right} So quick with accumulator builds its answer from the right, the largest end first. {pause}

[c4.order.2] {tree} Let's watch it on our running list, with last time's tree of calls. {root} The pivot three sends everything right, so first we sort seven, four, nine, five, with sorted empty. {seven} There, the pivot seven splits off five, four on the left, and nine on the right. {nine} The right comes first. Nine is a single item, so it's consed onto the empty list. {cons7} Then seven goes on, in front of it. Seven, nine.

[c4.order.3] {five} Next comes the left part, five, four, sorted in front of seven, nine. {pivot5} Its pivot is five, with four on the left and nothing on the right. {cons5} So five goes on, {cons4} and then four. Four, five, seven, nine. {cons3} Back at the top, three goes on in front, and its left part is empty, so we're done. Three, four, five, seven, nine. {pause}

[c4.order.4] {once} Nine, then seven, five, four and three. Each item was consed onto the answer exactly once, from the right. {noapp} Nothing was appended. {cards} It's rev-app's pile of cards again, except that the cards land in sorted order.

## Scene 6 · Was it worth it? (ch4_s6_speed)

> On {worth}: YELLOW "Was it worth it?". On {same}: two calls side by side, `quick rs` and `quik (rs, [])`, each with GOLD "158,058 comparisons" under it (checked: equal counts, and `quick rs = quik (rs, [])` ⇒ `- : bool = true`).
> On {copies}: under `quick rs`, GOLD "cells copied by @: 76,447"; under `quik (rs, [])`, GREEN "0" (checked with the instrumented `quick`; on the five-item chain its appends copy 3 cells).
> On {board}: the scoreboard returns at full size (`make_scoreboard(bound="118,458")`, filled as in the hook). On {secs}: quicksort's time cell "0.74 s" slides just below the cell, small and DIM, labelled `quick`; "0.53 s" takes its place in GOLD. On {reading}: a DIM tag under it, "the notes' summary; our reading: quik". On {cell}: the comparisons cell "158,058" gets a small GREEN "same for quik". By the end of the scene the DIM "0.74 s" and both tags fade, so the board ch4 leaves (ch5 s1, ch6) reads quicksort "158,058" / "0.53 s".
> On {pascal}: the board shrinks up. Two bars of nearly equal length: an array icon (a row of boxes) labelled "Pascal quicksort on arrays (Sedgewick)", and a chain icon labelled `quik`, the Pascal bar a little shorter; caption "only slightly faster". On {lists}: the chain icon's cells light one by one, each with a small DIM "new memory" tag.
> On {real}: GOLD "comparisons dominate", over a balance with comparisons heavy on one side and list overheads light on the other. On {strings}: two long YELLOW names, "Smithson-Whitworth, Alexandra" and "Smithson-Whitworth, Alexander", with a pointer stepping along both letter by letter, DIM "one comparison" (this example is beyond the notes).

[c4.speed.1] {worth} So was it worth it? {same} Quick with accumulator makes exactly the same comparisons as plain quick, since it splits the same items around the same pivots. On ar-ess, both make a hundred and fifty-eight thousand and fifty-eight. {copies} What's gone is the copying. On ar-ess, the appends in plain quick copy seventy-six thousand, four hundred and forty-seven cells, and quick with accumulator copies none. {pause}

[c4.speed.2] {board} The notes say the speedup is significant. {secs} Their summary gives quicksort zero point five three seconds, down from zero point seven four. That's more than a quarter of the time saved. {reading} The notes don't say which version that is, but we read it as the time for quick with accumulator. {cell} So that's quicksort's entry on our scoreboard, with the same count of comparisons.

[c4.speed.3] {pascal} Here's a surprise. An imperative quicksort in Pascal, from Sedgewick's book, which sorts an array in place, is only slightly faster than quick with accumulator. {lists} That's surprising, because lists cost more than arrays. Every cons needs new memory. {real} And in real applications, comparisons are the dominant cost, so those overheads matter even less. {strings} Comparing two long names, for example, can take far more work than a cons. {pause}

## Scene 7 · Recap (ch4_s7_recap)

> Recap in ch2 s7's layout (ch1 s8's look: "Recap" title, one row per mark, a small icon at the left and its line at the right): {r1} scene 2's recursion tree in miniature (BLUE boxes, a GOLD "n" at each level, the bracket "log₂ n"), "random pivots: log₂ n levels of n, O(n log n)"; {r2} scene 3's zigzag branch on the sorted chain (YELLOW pivots, RED empty sides) with RED "O(n²)", "sorted or reversed: every split lopsided"; {r3} scene 3's shuffled chain with its GREEN "158,058", "randomise: worst case unlikely"; {r4} scene 5's answer row growing from the right (GREEN cells, the GOLD right-to-left arrow), "quik: an accumulator, no @"; {r5} the scoreboard's quicksort row in miniature, "158,058" and "0.53 s", "same comparisons, less copying".
> On {next}: the rows sweep out; the title becomes "Next: merge sort". The scoreboard returns as ch5 s1's {board} shows it: quicksort's cells "158,058" and "0.53 s", merge sort's row label YELLOW, its two "?" cells pulsing GOLD.
> On {never}: beneath it, L4 ch1 s7's take/drop shot, which ch5 s1 uses for its {promise} (`where_used` in `projects/focs/l04-more-lists/scenes/ch1_s7_edges.py`): the running chain `3 → 5 → 9 → 4 → 7 → []`, the GOLD cut after cell 2, and `[3; 5]` and `[9; 4; 7]` lifting apart, two parts of nearly equal size.
> Leave about 8 s of end card after the last word; the music carries it.

[c4.recap.1] {recap} Let's recap. {r1} On random data, the pivots split the items roughly in half, so there are about log base two of N levels of N comparisons. Big O of N log N, on average. {r2} On sorted or reversed input, every split is lopsided, and the cost is quadratic. {r3} Randomising the input makes that worst case highly unlikely. {r4} Quick with accumulator gets rid of append, and builds its answer from the right, one cons per item. {r5} It makes the same comparisons as before, without the copying, and on the Deck Station it took zero point five three seconds. {pause}

[c4.recap.2] {next} Next time, merging two sorted lists, {never} and merge sort, which splits its list by counting, so its splits are never lopsided. {pause}
