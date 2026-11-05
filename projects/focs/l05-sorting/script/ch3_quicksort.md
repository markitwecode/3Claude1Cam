# Chapter 3 · Quicksort

Foundations of Computer Science · Lecture 5 (Sorting), part 3 of 7. Source: FoCS 2026-27 notes v1.8, pp. 40–41 (§5.3, and §5.4 up to the 0.74 s timing), with the Computer History Museum's obituary of Hoare (project.json) for the dates, Moscow and the manager story.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

All code and replies below were run in OCaml 5.4.1 and are quoted verbatim. Every comparison
count comes from a run with a tallying `le` in place of `<=` (the recipe in project.json).
The code's names are said this way: `a` "ay", `bs` "bees", `l` "ell", `r` "ar", `@` "append".
Hoare's name is written "Hoar" in the narration, as it's said; on screen it is "Hoare".

---

## Scene 1 · Hook (ch3_s1_hook)

> Title card, `title_card("Part 3 · Quicksort")`: "Sorting", "Foundations of Computer Science · Lecture 5", "Part 3 · Quicksort".
> On {last}: ch2's end card returns, rebuilt as in `scenes/ch2_s7_why.py` (its `teaser`): the scoreboard from `make_scoreboard(bound="118,458")` (import from `scenes/ch1_s4_contest.py`) with insertion sort's row filled, GOLD "25,146,194" and "174 s", the solid floor "lower bound ≈ 118,458", and quicksort's row lit YELLOW with its "?" cells pulsing. Beneath it, the chain 5 → 3 → 9 → 4 → 7 split round the YELLOW pivot 5: 3 and 4 on the left under "≤ 5", 9 and 7 on the right under "> 5".
> On {slow}: the split chain fades; "25,146,194" and then "174 s" flash.
> On {race}: the board shrinks to the top; below it, two horizontal time bars on one scale (ch2 s7's look): a long RED bar "insertion sort · 174 s", and under it a GOLD sliver "quicksort · 0.74 s" (both the notes' DECstation times, §5.2 and §5.4). Quicksort's cells on the board stay "?" until scene 7 fills them. On {under}, the sliver flashes.
> On {trick}: the bars clear; a big YELLOW "What's the trick?".
> On {split}: ch2's split comes back under the question: the chain 5 → 3 → 9 → 4 → 7 → [] (ConsChain), the 5 lifting YELLOW with a label "pivot", the 3 and 4 dropping left under "≤ 5", the 9 and 7 right under "> 5".
> On {plan}: three DIM tags in a row under the split, "the idea", "the code", "a trace". The rejoined chain 5 → 3 → 9 → 4 → 7 → [] carries into scene 2.

[c3.hook.1] {title} This is part three of Sorting. {pause=2} {last} Last time, insertion sort took its place on the scoreboard. {slow} It made over twenty-five million comparisons on our ten thousand random numbers, and took a hundred and seventy-four seconds on the Deck Station.

[c3.hook.2] {race} On the same machine, the next contestant, quicksort, sorts the same list in zero point seven four seconds. {under} That's under a second, instead of nearly three minutes. {trick} So what's the trick? {pause}

[c3.hook.3] {split} Quicksort picks one item, called the pivot, and splits the rest into the smaller items and the larger ones. {plan} Today, we'll see why that idea works, write it in OCaml, and watch it sort our running list. {pause}

## Scene 2 · Divide and conquer (ch3_s2_idea)

> The chain from scene 1, 5 → 3 → 9 → 4 → 7 → [] (ConsChain), across the top. A column of four step labels down the left edge, each appearing on its mark and lighting YELLOW while its step plays, then staying DIM: "1 choose", "2 divide", "3 conquer", "4 combine" (the notes' four steps, §5.3).
> On {choose}: the 5 lifts out of the chain, YELLOW, labelled "pivot a" (the `a` YELLOW).
> On {divide}: two empty groups appear beneath, labelled "≤ a" (left) and "> a" (right). On {tests}: the other four cells drop one at a time, each with a small GOLD "≤ 5?" and a "yes" or "no": 3 left, 9 right, 4 left, 7 right. The left group reads 3 4 and the right 9 7, in input order (scene 5 shows how the code really orders them). On {four}: a GOLD counter "comparisons: 4".
> On {conquer}: each group gets a box labelled `quick`; on {small} the left group stays 3 → 4 and the right becomes 7 → 9 (the 9 and 7 swap places), each with a GOLD "+1".
> On {combine}: the pieces slide together, left part, then the pivot, then the right part; on {done} they join into 3 → 4 → 5 → 7 → 9 → [] with the lecture's GREEN tick. On {six}: the counter reads "comparisons: 6" (checked: `quick [5; 3; 9; 4; 7]` makes 6).
> On {because}: a vertical YELLOW dashed line through the 5 in the sorted chain, "everything ≤ 5" on its left and "everything > 5" on its right. On {nowork}: the counter flashes, with a GOLD tag "combine: 0 comparisons".
> On {dc}: the four step labels gather under a brace, "divide and conquer". On {merge}: a DIM tag "merge sort: Part 5" beside it.

[c3.idea.1] {steps} Quicksort works in four steps. {choose} First, choose an item, called the pivot. Call it ay. Here, it's the first item, five. {divide} Second, divide the other items into two parts, those at most the pivot, and those bigger than it. {tests} Three and four go left, and nine and seven go right. {four} Each item is compared with the pivot once, so that's four comparisons.

[c3.idea.2] {conquer} Third, conquer. Sort each part, using quicksort itself. {small} Each part has two items, so sorting it takes one comparison, giving three, four, and seven, nine. {combine} Fourth, combine. Put the smaller part first, then the pivot, then the larger part. {done} Three, four, five, seven, nine. {six} Six comparisons in all. {pause}

[c3.idea.3] {why} But why is the result sorted? {pause} {because} Everything in the left part is at most the pivot, and everything in the right part is bigger. So once each part is sorted, nothing needs to cross the pivot. {nowork} The combine step makes no comparisons at all. All the comparing happens while dividing.

[c3.idea.4] {dc} This is divide and conquer. Split a problem into smaller problems of the same kind, solve those, and combine their answers. {basic} It's one of the basic principles of algorithm design. {merge} Merge sort, in part five, uses it too, but it splits the list in a different way.

## Scene 3 · Hoare's idea (ch3_s3_hoare)

> A plain name card, no photo: YELLOW "Sir Tony Hoare", GOLD "1934–2026" beneath (the notes' dates; the notes write "Sir Anthony Hoare", while the Computer History Museum gives "Sir Antony Hoare", known as Tony, so the card uses "Tony"). On {moscow}: a DIM line under it, "quicksort: Moscow State University, 1959" (CHM, beyond the notes). On {msr}: DIM "later: Microsoft Research, Cambridge" (the notes). On {died}: DIM "died 5 March 2026, aged 92" (CHM).
> On {array}: the card shrinks to the left. On the right, an array: a row of five touching square boxes (BLUE outlines, no arrows, so clearly not cons cells) holding 5 3 9 4 7, the 5 YELLOW. DIM label "array".
> On {clever}: a GREEN label over the row, "in place". On {swap}: two small BLUE pointers scan in from the two ends; the left one stops at the 9 (bigger than 5), the right one at the 4 (at most 5); the 9 and the 4 trade places along two arcs, giving 5 3 4 9 7. On {middle}: the 5 and the 4 trade places the same way, giving 4 3 5 9 7, with a brace "≤ 5" under 4 3 and "> 5" under 9 7. On {nonew}: GREEN "no new cells". (This exchange sequence illustrates the notes' "exchanging array elements" and is beyond the notes; checked by hand and with a Hoare-style scan in Python.)
> On {hard}: the array dims; a DIM tag "before recursion was well known". On {manager}: a quote card in italics, "Tony, I don't care if the program talks to itself, as long as it doesn't do it on company time." with a DIM attribution "his manager at Elliott Brothers, 1960s (Computer History Museum)".
> On {list}: everything clears except the name card; the ConsChain 5 → 3 → 9 → 4 → 7 → [] returns and splits as in scene 2, but this time the parts are new YELLOW cells born from copies of the old ones (TransformFromCopy), with a GOLD tag "copies". On {easier}: a GREEN tag "easier to follow".

[c3.hoare.1] {who} Quicksort was invented by Sir Tony Hoar. {moscow} He came up with it in nineteen fifty-nine, as a student at Moscow State University. {msr} In later life, he worked at Microsoft Research, in Cambridge. {died} He died in March twenty twenty-six, aged ninety-two.

[c3.hoare.2] {array} His original quicksort works on an array, a row of boxes in memory. {clever} The cleverest part is that it divides the items in place. {swap} It scans in from both ends, and when it finds an item bigger than the pivot on the left, and one at most the pivot on the right, it swaps them. {middle} At the end, the pivot swaps into the middle. {nonew} The two parts are formed without building anything new.

[c3.hoare.3] {hard} Quicksort was invented before recursion was well known, and people found it extremely hard to understand. {manager} When Hoar tried to explain recursive subroutines to his manager, the reply was this. Tony, I don't care if the program talks to itself, as long as it doesn't do it on company time. {pause}

[c3.hoare.4] {list} As usual, we'll write a list version instead. {copies} It copies the items into new lists, rather than swapping them. {easier} But it's still fast, and it's much easier to understand.

## Scene 4 · The code (ch3_s4_code)

> The notes' In [80], hero-sized and centred, laid out exactly as printed (2-space steps; checked against the PDF's character positions): `let rec quick = function` / `  | [] -> []` / `  | [x] -> [x]` / `  | a::bs ->` / `      let rec part l r = function` / `        | [] -> (quick l) @ (a :: quick r)` / `        | x::xs ->` / `            if (x <= a) then` / `              part (x::l) r xs` / `            else` / `              part l (x::r) xs` / `      in` / `      part [] [] bs`. Colours: `quick` and `part` YELLOW, keywords BLUE, `[]` and `::` TEAL, `@` GOLD (as in L3).
> One highlight box slides clause by clause: {nil} `[] -> []`; {one} `[x] -> [x]`, with a small DIM tag "exactly one element"; {many} `a::bs`; {pivot} `a` alone, YELLOW tag "pivot"; {local} the lines from `let rec part` to `in`, bracketed, "local helper"; {start} `part [] [] bs`.
> On {spare}: beside the `[x]` clause, a DIM note "without it: same answers, same comparisons" (checked: with the clause removed, `quick [3; 5; 9; 4; 7]` still makes 8 comparisons and the 10,000 random items still take 158,058). On {special}: DIM "lists up to five or so: often special-cased for speed".
> On {why}: the `a` in `x <= a` and the `a` in `a :: quick r` glow YELLOW, with an arrow back to the `a` of `a::bs`. A small DIM inset of L4 ch5's `allc` line, `| cs :: css -> (c::cs) :: allc css`, its `c` glowing, labelled "local, like allc (Lecture 4)". On {calls}: both `quick l` and `quick r` flash YELLOW, "recursive calls".
> On {acc}: `l` and `r` in `part l r` light up, tags "left: ≤ a" and "right: > a". On {test}: box on `if (x <= a) then`; on {left} `part (x::l) r xs`, its `x::l` TEAL; on {right} `part l (x::r) xs`, its `x::r` TEAL.
> On {end}: box on `| [] -> (quick l) @ (a :: quick r)`; on {combine} the pieces light in order: `(quick l)`, then `a ::`, then `quick r`, with `@` GOLD, label "combine".
> On {type}: the code shrinks to the left; the reply `val quick : 'a list -> 'a list = <fun>` (each `'a` PINK, `list` GREEN). On {poly}: `quick ["dog"; "cat"; "emu"]` → `- : string list = ["cat"; "dog"; "emu"]`. On {check}: `quick [3; 5; 9; 4; 7]` → `- : int list = [3; 4; 5; 7; 9]`, drawn as the GREEN-ticked chain.

[c3.code.1] {code} Here's the list version, from the notes. {nil} It has three clauses. The empty list is already sorted. {one} The second clause uses the pattern ex in square brackets. It matches a list of exactly one element, and a single item is already sorted too.

[c3.code.2] {spare} Strictly, this clause is optional. Without it, the third clause would still return a one-item list unchanged, with the same comparisons, just a little more work. {special} It's there for speed. Real sorts often treat lists of up to five or so items as special cases.

[c3.code.3] {many} The third clause handles two or more items. {pivot} The head, ay, is the pivot, and bees are the rest. {local} Inside this clause, we declare a helper, called part, that divides bees into two parts. {why} It has to be local, like all-see in last lecture's making change, because it uses the pivot, ay, which only has a name inside this clause. {calls} It also calls quick, to sort the parts. {start} The clause ends by calling part with two empty lists, and bees.

[c3.code.4] {acc} Part's first two arguments, ell and ar, are accumulators, for the left part and the right. {test} For each item, ex, part asks, is ex at most ay? {left} If so, ex is consed onto ell. {right} If not, it's consed onto ar. {end} When the items run out, part sorts both parts, with quick of ell and quick of ar. {combine} Then it combines them, in order. First the sorted left part, then ay, then the sorted right part. Ay goes on with a cons, and the left part with an append.

[c3.code.5] {type} OCaml replies that quick takes an alpha list, and returns an alpha list. {poly} Like in-sort, it works at any type, because less than or equal is polymorphic. Dog, cat, emu becomes cat, dog, emu. {check} And our running list comes out as three, four, five, seven, nine. {pause}

## Scene 5 · Partitioning (ch3_s5_part)

> The code from scene 4 shrinks to the top-left corner, with `part`'s lines lit. On {setup}: the pivot 5 YELLOW at the top centre, the input `[3; 9; 4; 7]` as a ConsChain under it, and two accumulator chains below, labelled `l` and `r`, each just a TEAL `[]`.
> The trace builds on the right, each line born from a copy of the one above, with the test that produced it in small GOLD beside it: `part [] [] [3; 9; 4; 7]` / {t1} `⇒ part [3] [] [9; 4; 7]` "3 ≤ 5? yes" / {t2} `⇒ part [3] [9] [4; 7]` "9 ≤ 5? no" / {t3} `⇒ part [4; 3] [9] [7]` "4 ≤ 5? yes" / {t4} `⇒ part [4; 3] [7; 9] []` "7 ≤ 5? no". As each test lands, the item's cell leaves the input chain and is consed onto the FRONT of `l` or `r` (a new cell born from it, landing at the left end).
> On {count}: a GOLD counter "comparisons: 4", then GOLD "n items → n − 1 comparisons".
> On {iter}: the four `part` lines flash one after another, each replacing the last, with a DIM tag "nothing waits: iterative"; beside it, a small DIM tag "each call hands over to the next". On {hand}: the last line becomes `⇒ (quick [4; 3]) @ (5 :: quick [7; 9])`, with `@` GOLD.
> On {backwards}: `l = [4; 3]` and `r = [7; 9]` glow YELLOW. On {earlier}: scene 2's groups, 3 4 and 9 7, appear small and DIM beside them, with a two-way arrow "reversed"; on {reversed} a small DIM inset of L3's `rev_app [1; 2; 3] [4; 5]` ⇒ `[3; 2; 1; 4; 5]`, "consing onto an accumulator reverses".
> On {fine}: each part gets a `quick` box and comes out `[3; 4]` and `[7; 9]`, with a GREEN tag "each part is sorted next, so order doesn't matter".
> On {equal}: a ghost 5 drops onto the pivot's test, GOLD "5 ≤ 5? yes", and slides left, tag "equal to the pivot: left". On {dupes}: `quick [5; 3; 5; 1]` → `- : int list = [1; 3; 5; 5]` (checked), both 5s YELLOW.

[c3.part.1] {zoom} Let's watch part at work, on the example from earlier. {setup} The pivot is five, and the other items are three, nine, four, seven. Both accumulators start empty. {t1} Is three at most five? Yes, so three goes onto ell. {t2} Nine is bigger, so it goes onto ar. {t3} Four goes left, {t4} and seven goes right.

[c3.part.2] {count} That's one comparison for each item after the pivot, so dividing N items takes N minus one comparisons. {iter} And notice that each call to part simply hands over to the next one. Nothing waits to be done afterwards, so part is iterative. {hand} When the items run out, part hands its two lists to quick. {pause}

[c3.part.3] {backwards} Now look at the two parts. Ell is four, three, and ar is seven, nine. {earlier} Earlier, we drew them in their original order. {reversed} Like rev-app in lecture three, part conses each item onto the front of an accumulator, so each part comes out backwards. {fine} Here, that's harmless. Each part is about to be sorted anyway. {pause}

[c3.part.4] {equal} One more detail. The test is less than or equal, so an item equal to the pivot goes left. {dupes} Quick of five, three, five, one gives one, three, five, five, and both fives are kept.

## Scene 6 · Watching it run (ch3_s6_trace)

> The running chain 3 → 5 → 9 → 4 → 7 → [] at the top centre. Below it a call tree grows, one node per call of `quick`, each node a small list in brackets with its pivot YELLOW and a GOLD comparison badge; left children hold the "≤" part, right children the ">" part. Build it in one exported function, `call_tree()`, that takes the input list (default `[3, 5, 9, 4, 7]`) and draws either form: the list nodes with their GOLD badges, or the final pivot circles of {tree}. Later scenes import it from `scenes/ch3_s6_trace.py`: ch4 s1 (circles), ch4 s2 (list nodes, small), ch4 s3 (list nodes for the sorted chain `[3, 4, 5, 7, 9]`, which give a zigzag), ch4 s5 (list nodes, to retrace `quik`), ch6 s6 (circles) and ch7 s3 (the first split, small).
> On {p1}: the root `[3; 5; 9; 4; 7]`, its 3 YELLOW. On {all}: the other four items slide right one by one; on {first} two children appear, left `[]` and right `[7; 4; 9; 5]` (built backwards, as in scene 5), and on {c1} the root's GOLD badge "4". Under the tree, the step `quick [3; 5; 9; 4; 7] ⇒ (quick []) @ (3 :: quick [7; 4; 9; 5])`.
> On {p2}: the `[]` child gets GREEN "= []"; the right child's 7 turns YELLOW. On {split2}: its children `[5; 4]` (left) and `[9]` (right); on {c2} badge "3". On {p3}: in `[5; 4]` the 5 turns YELLOW; on {c3} its children `[4]` and `[]`, badge "1". On {leaves}: the leaves `[]`, `[4]`, `[]`, `[9]` get GOLD badges "0", DIM tag "one item or none: no comparisons".
> On {up}: results flow back up the tree as GREEN lists, each born from its children and the pivot (TransformFromCopy): on {a1} `[4] @ (5 :: [])` ⇒ `[4; 5]`; on {a2} `[4; 5] @ (7 :: [9])` ⇒ `[4; 5; 7; 9]`; on {a3} `[] @ (3 :: [4; 5; 7; 9])` ⇒ `[3; 4; 5; 7; 9]`. On {result}: the root's result becomes the GREEN-ticked chain, with the reply `- : int list = [3; 4; 5; 7; 9]`. (Don't show any order between `quick l` and `quick r`; OCaml in fact evaluates `quick r` first.)
> On {count}: the badges gather into GOLD `4 + 3 + 1 = 8` (checked with the tallying `<=`). On {floor}: ch1's GOLD "7" beside it, "floor for five items"; on {ins} GOLD "6: insertion sort (Part 2)". On {even}: a small copy of scene 2's even split of `[5; 3; 9; 4; 7]` beside it with GOLD "6".
> On {tree}: the lists fade from the nodes, leaving only the pivots and the one-item leaves as circles: 3 at the top, 7 below-right, then 5 (below-left of 7) and 9 (below-right), then 4 below-left of 5. On {lopsided}: the root's empty left branch glows RED, with the root's two children labelled "0" and "4". On {evensplit}: the small even-split picture glows GREEN, "2 and 2". On {hold}: a YELLOW "?" over the root's lopsided split.

[c3.trace.1] {run} Now let's run quicksort on our running list, three, five, nine, four, seven. {p1} The pivot is three, the first item. {all} Every other item is bigger, so they all go right. {first} Ell is empty, and ar is seven, four, nine, five, built backwards. {c1} That's four comparisons so far.

[c3.trace.2] {p2} Quick of the empty list is just nil. On the right, the pivot is seven. {split2} Four goes left, nine goes right, and five goes left, {c2} with three more comparisons. {p3} Its left part, five, four, has the pivot five, and the four goes left, {c3} with one more. {leaves} What's left are lists of one item or none, and those need no comparisons at all.

[c3.trace.3] {up} Now the appends rebuild the answer, from the bottom up. {a1} At the bottom, four, then the pivot five, gives four, five. {a2} One level up, four, five, then the pivot seven, then nine. {a3} And at the top, nothing on the left, then the pivot three, then the rest. {result} Three, four, five, seven, nine. {pause}

[c3.trace.4] {count} Add up the comparisons. Four, plus three, plus one, makes eight. {floor} That's one more than the floor of seven from part one, {ins} and two more than insertion sort made on the same list. {even} Yet earlier, the same five numbers, with five in front, took only six.

[c3.trace.5] {tree} Look at the pivots. They form a tree, with three at the top, then seven, then five and nine, then four. {lopsided} The first pivot was the smallest item, so nothing went left, and the split was as lopsided as it could be. {evensplit} With five in front, the first split was even, two and two. {hold} Hold that thought. How evenly the pivots split decides how fast quicksort is. {pause}

## Scene 7 · Recap (ch3_s7_recap)

> On {board}: the scoreboard returns (`make_scoreboard(bound="118,458")`), insertion sort's row filled as in scene 1. On {count}: quicksort's comparisons cell fills with GOLD "158,058" (checked: `quick rs` with the tallying `<=`, result checked sorted); on {floor} the floor line "lower bound ≈ 118,458" flashes, with a small GOLD "× 1.33" between them. On {secs}: the time cell fills with GOLD "0.74 s" (the notes, §5.4).
> Recap on {recap}: the board dims; "Recap" at the top, then four short lines, one per mark ({r1} to {r4}), each with a small icon from the chapter at its left, in ch2 s7's recap layout: scene 2's split of 5 → 3 → 9 → 4 → 7 round the YELLOW pivot 5 into "≤ 5" and "> 5", line "choose, divide, conquer, combine"; scene 3's array row 4 3 5 9 7 with its two swap arcs beside a small GOLD "copies" chain, line "Hoare: in place · ours: lists"; scene 5's `part` trace in miniature with `l = [4; 3]` and `r = [7; 9]`, line "part: one pass, two accumulators, n − 1 comparisons"; scene 6's pivot tree with its RED empty branch, line "our list: 8 comparisons, a lopsided first split".
> On {next}: the recap dims; "Next: how good is quicksort?". On {fast}: the scoreboard, small, with quicksort's row filled and lit YELLOW, and beside it scene 6's pivot tree, its RED lopsided branch and YELLOW "?". On {quik}: a small DIM `(quick l) @ (a :: quick r)` with the `@` GOLD, then struck through.
> Leave about 8 s of end card after the last word; the music carries it.

[c3.recap.1] {board} Back to the scoreboard. {count} On our ten thousand random numbers, quicksort makes a hundred and fifty-eight thousand and fifty-eight comparisons, counted with our tallying less than or equal. {floor} That's only about a third more than the floor. {secs} And on the Deck Station, it takes zero point seven four seconds. {pause}

[c3.recap.2] {recap} Let's recap. {r1} Quicksort chooses a pivot, divides the other items into those at most the pivot and those above it, sorts each part, and combines them. {r2} The original, by Tony Hoar, divides an array in place, by swapping. Ours copies into new lists, but it's much easier to follow. {r3} Part makes one pass with two accumulators, so dividing N items takes N minus one comparisons. {r4} On our running list, quicksort made eight comparisons, and its first split was lopsided. {pause}

[c3.recap.3] {next} Next time, how good is quicksort? {fast} We'll see why it's fast on average, and how it can be slow. {quik} And we'll write a version that never appends. {pause}
