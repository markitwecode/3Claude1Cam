# Chapter 1 · Take and drop

FoCS Lecture 4 (More on Lists), part 1 of 7. Source: FoCS 2026-27 notes v1.8, pp. 30–31 (§4.1); forward link to p. 43 (merge sort).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

All code and replies below were run in OCaml 5.4.1 (`ocaml < file.ml`) and are quoted verbatim.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card (lib/titles.py): "More on Lists", "Foundations of Computer Science · Lecture 4", "Part 1 · Take and drop".
> On {title}, a quick DIM row of Lecture 3's tools, one small label per beat of the sentence: "build", "match", "length", "append", "reverse". On {plan}, they clear and two short lines appear, "more list utilities" and "more patterns of recursion"; on {change}, a small row of GOLD coin discs labelled 50, 20, 10, 5, 2, 1 (the disc style ch4–ch7 reuse), captioned "making change". All of it clears on {chain}.
> Hero, on {chain}: the running chain (ConsChain, L3 palette: BLUE cells, TEAL nil) 3 → 5 → 9 → 4 → 7 → [], centred and wide. It extends L3's 3 → 5 → 9, so build the first three cells first and let the 4 and 7 join.
> On {cut}: a GOLD dashed vertical cut drops between the 5's cell and the 9's cell. On {sides}: a YELLOW "?" over each side. On {cost}: a small GOLD "cost?" under each "?".
> On {names}: the two "?" turn into YELLOW `take` (left) and `drop` (right). The chain and the cut stay for scene 2.

[c1.hook.1] {title} Last time, we built lists, took them apart with patterns, and wrote length, append and reverse for ourselves. {plan} In this lecture, we'll write more list utilities, and meet more patterns of recursion. {change} And at the end, we'll write a small program that makes change, the way a till hands you coins. {pause}

[c1.hook.2] {chain} Let's start with a simple question. Here's a list, three, five, nine, four, seven. {cut} Suppose you want to cut it in two, right after the second element. {sides} How do you get the front part, and how do you get the rest? {pause} {cost} And what does each part cost? {names} In this chapter, we'll write the two functions that do it, called take and drop.

## Scene 2 · Taking the first i (ch1_s2_take)

> Carries over: scene 1's chain and GOLD cut. On {general}, it shrinks to the top and the notes' diagram is built under it, MathTex `xs = [x_0, \ldots, x_{i-1}, x_i, \ldots, x_{n-1}]` (on {elems}), the cut now between x_{i−1} and x_i. On {front}, a brace under x_0 … x_{i−1} labelled `take i xs`; on {rest}, a brace under x_i … x_{n−1} labelled `drop i xs` (function names YELLOW, `i` GOLD). On {cutpos}, the GOLD cut flashes, label "position i".
> On {code}, the diagram moves up and DIMs; the code comes in, hero-sized: `let rec take i = function` / `  | [] -> []` / `  | x::xs ->` / `      if i > 0 then x :: take (i - 1) xs` / `      else []`. Colours: `take` YELLOW, `let rec` and `function` BLUE, `[]` and `::` TEAL, `0` and `1` GOLD.
> On {function}: box on `i`, label "the count". On {list}: a ghost slot appears after `i`, labelled "unnamed list" (L3 ch3's addlen gesture), with a DIM inset of `let rec addlen n = function` for the callback.
> One highlight box (P8) slides through the clauses: `| [] -> []` on {empty}, `| x::xs ->` on {cell}, `if i > 0 then x :: take (i - 1) xs` on {keep} (the `x ::` YELLOW, `take (i - 1) xs` boxed as "the smaller problem"), `else []` on {stop}.
> On {type}: OCaml's reply under the code, `val take : int -> 'a list -> 'a list = <fun>`, `int` GREEN and both `'a` PINK. Labels under it beat by beat: "count" under `int` on {int}, "list in" under the first `'a list` on {inlist}, "list out, same 'a" under the last on {out}.
> On {droptype}: a DIM copy of the type slides to the right, prefixed `val drop :`, as a preview of scene 4.

[c1.take.1] {general} Here's the general picture. {elems} A list, exes, holds elements ex zero, ex one, and so on, up to ex en minus one. {front} Take eye of exes returns the front of the list, ex zero up to ex eye minus one. {rest} Drop eye of exes returns the rest, from ex eye onwards. {cutpos} Together, they cut the list at position eye. {pause}

[c1.take.2] {code} Let's write take first. {function} It names one argument, eye, the count. {list} Remember that the word function introduces an argument of its own, with no name, just as it did for add-len, last lecture. Here, that argument is the list. {empty} If the list is empty, there's nothing to take, so take gives nil.

[c1.take.3] {cell} Otherwise, the list has a head, ex, and a tail, exes. {keep} If eye is greater than zero, we still need more elements. So we keep ex, and cons it onto take eye minus one, of the tail. {stop} Once eye reaches zero, we've taken enough, and the answer is nil. {pause}

[c1.take.4] {type} OCaml's reply gives the type. {int} First comes an integer, the count. {inlist} Then an alpha list, a list of any type. {out} And out comes an alpha list, with the same alpha, because take only hands back elements it was given. {droptype} Drop has exactly the same type.

## Scene 3 · Watching take run (ch1_s3_trace)

> Take's code shrinks to the upper left and DIMs; on each step its line `if i > 0 then x :: take (i - 1) xs` lights briefly (and `else []` on {s3}).
> The trace as stacked lines, each born from a copy of the line above (L3 ch4's append trace, P11/P13; first step slow, the rest faster): `take 2 [3; 5; 9; 4; 7]` ({start}) / `⇒ 3 :: take 1 [5; 9; 4; 7]` ({s1}) / `⇒ 3 :: 5 :: take 0 [9; 4; 7]` ({s2}) / `⇒ 3 :: 5 :: []` ({s3}) / `⇒ [3; 5]` ({answer}).
> The count in GOLD, ticking 2 → 1 → 0. On {s3}, `take 0 [9; 4; 7]` becomes TEAL `[]`, and the 9, 4, 7 DIM ("never looked at").
> On {pending}: the waiting `3 ::` and `5 ::` turn YELLOW and stay; a brace under them, "waiting". On {fire}: the conses fire inside out, `5 :: []` first, then `3 ::`, collapsing into GREEN `[3; 5]`, OCaml's reply `- : int list = [3; 5]`.
> On {echo}: a small DIM inset of L3 ch4's trace line `⇒ 1 :: (2 :: (3 :: append [] [4]))`, the same nested shape; label "not iterative" on {notiter}.
> On {space}: GOLD "space: one waiting cons per element taken". The finished trace stays for scene 4's comparison.

[c1.trace.1] {start} Let's take two from our list, three, five, nine, four, seven. {s1} The list has a head, three, and two is greater than zero. So the answer is three, consed onto take one, of five, nine, four, seven. {pause} {s2} Same again. Keep the five, and take zero, of nine, four, seven. {s3} Now the count is zero, so that take gives nil, however much of the list is left.

[c1.trace.2] {pending} Look at what has piled up. {conses} The three and the five are each waiting to be consed on. {fire} Only now can those conses happen, from the inside out. Five onto nil, then three onto that. {pause} {answer} The answer is three, five.

[c1.trace.3] {notiter} So take is not iterative. {echo} It has the same shape as append, from last lecture. It walks down the list, leaves a cons waiting at every step, and only then builds the answer. {space} Each of those waiting conses takes up space, one for every element taken. We'll count that cost shortly.

## Scene 4 · Dropping the first i (ch1_s4_drop)

> Take's code DIMs on the left; drop's code appears on the right, hero-sized, lines aligned with take's: `let rec drop i = function` / `  | [] -> []` / `  | x::xs ->` / `      if i > 0 then drop (i-1) xs` / `      else x::xs`, with OCaml's reply `val drop : int -> 'a list -> 'a list = <fun>` (`drop` YELLOW, `int` GREEN, `'a` PINK, same colour rules as scene 2).
> On {same}: the lines both functions share glow together (`| [] -> []`, `| x::xs ->`, `if i > 0 then`). Box on `| [] -> []` on {empty}, on `drop (i-1) xs` on {skip}.
> On {nothing}: in take's code, the `x ::` in front of `take (i - 1) xs` flashes YELLOW, label "waits"; in drop's, the empty space in front of `drop (i-1) xs` gets a GREEN label "nothing waits" on {last}, then "iterative".
> On {keep}: box on `else x::xs`, label "ex put back on its tail".
> On {trace}: both codes clear; a flat trace, every line the same width (contrast with scene 3's growing trace, as rev_app in L3 ch4): `drop 2 [3; 5; 9; 4; 7]` / `⇒ drop 1 [5; 9; 4; 7]` ({d1}) / `⇒ drop 0 [9; 4; 7]` ({d2}) / `⇒ [9; 4; 7]` ({d3}), reply `- : int list = [9; 4; 7]`. On each skip, the skipped element (the 3, then the 5) slides out and fades; the GOLD count ticks 2 → 1 → 0.
> On {flat}: a DIM copy of scene 3's growing take trace beside it, for the contrast in shape.

[c1.drop.1] {code} Now drop. {same} It has the same shape as take, clause for clause. {empty} Dropping from the empty list gives nil. {skip} And if eye is greater than zero, we skip the head, and drop eye minus one from the tail. {pause}

[c1.drop.2] {nothing} But look at what's missing. In take, ex was left waiting, to be consed onto the result of the recursive call. {last} Here, the recursive call is the very last thing drop does. Nothing waits for it, so drop is iterative. {keep} Once eye reaches zero, we stop skipping. The answer is ex consed back onto exes, which is the list we were handed at this step.

[c1.drop.3] {trace} Let's drop two from three, five, nine, four, seven. {d1} Skip the three, and drop one, from five, nine, four, seven. {d2} Skip the five, and drop zero, from nine, four, seven. {d3} The count is zero, so the answer is nine, four, seven. {flat} Notice that the expression never grows. Each call just hands over to the next. {pause}

## Scene 5 · Copied or shared (ch1_s5_cells)

> Cells in memory (ConsChain), filling the frame: the running chain 3 → 5 → 9 → 4 → 7 → [] across the middle, YELLOW pointer `xs` on the 3 (on {xs}).
> On {copy}: `take 2 xs` builds two new YELLOW cells above, 3 then 5, each born from a copy of its original (TransformFromCopy), ending in its own new TEAL nil; pointer `take 2 xs`. GOLD "new cells: 2". The original chain is untouched. On {why}: the original 5 → 9 arrow flashes, against the new 5 → [] arrow.
> On {skip}: a marker walks the original chain from the 3 to the 9 (the skipping). On {rebuild}: a new YELLOW cell 9 is born below from a copy of the original 9, and on {shared} its arrow reaches up into the ORIGINAL 4; the 4 → 7 → [] cells glow TEAL, label "shared". Pointer `drop 2 xs` on the new 9. On {one}: GOLD "new cells: 1".
> On {check}: Code at the bottom, `==` in YELLOW, replies as printed: `let xs = [3; 5; 9; 4; 7]` → `val xs : int list = [3; 5; 9; 4; 7]`, then on {nine} `drop 2 xs == List.tl (List.tl xs)` → on {false} `- : bool = false` (the two 9 cells, original and new, flash side by side), then on {four} `List.tl (drop 2 xs) == List.tl (List.tl (List.tl xs))` → `- : bool = true` (the one shared 4 flashes). `List.tl` is OCaml's built-in tail, L3 ch2's `tl`.
> On {safe}: DIM caption, L3 ch1's line "lists never change once they're built".
> On {glue}: the take cells and the drop cells slide together under scene 1's GOLD cut: `take 2 xs @ drop 2 xs` → `- : int list = [3; 5; 9; 4; 7]` (GREEN).

[c1.cells.1] {cells} Now let's look at the cells in memory. {xs} Here's our list, exes. {copy} Take two builds new cells, one for the three, and one for the five, ending in a nil of its own. {why} It has to copy. In the original list, the five points on to the nine, but take's answer must stop after the five. {pause}

[c1.cells.2] {share} What about drop? Its answer, nine, four, seven, is already sitting there, at the end of the original list. {skip} Drop just walks along to it. {rebuild} But look closely at its last clause. The pattern took the nine's cell apart, into ex and exes, and ex consed onto exes builds a brand new cell, holding the same nine. {shared} Its arrow points straight back into the original list, at the four. {one} So drop makes exactly one new cell, and shares all the rest. {pause=1.5}

[c1.cells.3] {check} You can check this in OCaml. Two equals signs ask whether two values are the very same cells in memory. {nine} Is drop two of exes the very same as the tail of the tail of exes? {false} False, because the nine is a new cell. {four} But their own tails are the very same, so that gives true.

[c1.cells.4] {safe} Sharing cells like this is safe, because lists never change once they're built. Nobody can change the four behind drop's back. {glue} And if you append the two pieces, you get back the whole list, three, five, nine, four, seven. {pause}

## Scene 6 · What they cost (ch1_s6_cost)

> Two columns: take's finished trace (scene 3) on the left with its YELLOW waiting conses; drop's flat trace (scene 4) on the right. Costs build up under each column in GOLD.
> On {time}: under take, a GOLD tick per call, 1, 2 → "one call per element taken" → GOLD "O(i) time". On {space}: GOLD "O(i) space", with two reasons stacked under it, "waiting conses: i" on {waiting} and "new cells: i" on {copy} (scene 5's two YELLOW cells flash).
> On {acc}: a DIM sketch with L3 ch4's card piles: the 3, then the 5, move onto an accumulator pile, which reads 5 → 3; on {back}, RED "backwards". On {rev}, a reverse arrow flips it to 3 → 5, GOLD "+ a reversal". (Checked: an accumulator take, `rtake 2 [] [3; 5; 9; 4; 7]`, gives `- : int list = [5; 3]`; not shown as code.) On {warn}: L3 ch4's caveat as a DIM caption, "an extra reversal can cost more than it saves".
> On {drop}: under drop, GOLD "O(i) time"; on {const}, GREEN "nothing waits" and "new cells: 1" (scene 5's single new 9); on {one}, GREEN "O(1) space".
> On {both}: the two "O(i) time" labels pulse together. On {factor}: two straight lines on small axes (across "i", up "work"), both straight, take's steeper (GOLD, "copy") and drop's shallower (GREEN, "skip"). On {hide}: caption "O-notation hides constant factors" (Lecture 2).

[c1.cost.1] {time} Now, the costs. Take makes one call for each element it takes. So with a count of eye, its time is big O of eye. {space} Its space is big O of eye too, for two reasons. {waiting} While it runs, a cons waits for every element. {copy} And when it's done, the answer is a copy, with one new cell for every element taken. {pause}

[c1.cost.2] {acc} Could an accumulator help, as it did for length? {pause} {must} Not here. The answer is a copy, one new cell per element taken, so it needs big O of eye space whatever we do. {back} And an accumulator would build that copy backwards, five, three. {rev} So we'd need a reverse at the end. {warn} That's the warning from last lecture. If an accumulator forces an extra reversal, it can cost more than it saves.

[c1.cost.3] {drop} Drop is different. It skips the elements one call at a time, at most eye of them, so its time is big O of eye as well. {const} But it's iterative, so nothing waits, and it builds at most one new cell. {one} So its space is constant, big O of one.

[c1.cost.4] {both} So both of them take big O of eye time. Are they equally fast? {pause} {factor} No. Skipping an element is much cheaper than copying it, so drop's constant factor is smaller. {hide} And as lecture two showed, big O hides constant factors. Two functions with the same big O can run at very different speeds.

## Scene 7 · Off the end, and recap (ch1_s7_edges)

> A short chain 3 → 5 → 9 → [] (L3's chain) with Code beside it, replies as printed: on {takeall} `take 10 [3; 5; 9]` → `- : int list = [3; 5; 9]` (three new YELLOW cells copied from the chain, "a copy"); on {dropall} `drop 10 [3; 5; 9]` → `- : int list = []` (TEAL).
> On {zero}, GOLD "i ≤ 0": `take 0 [3; 5; 9]` → `- : int list = []`, `drop 0 [3; 5; 9]` → `- : int list = [3; 5; 9]`, then `take (-1) [3; 5; 9]` → `- : int list = []`, `drop (-1) [3; 5; 9]` → `- : int list = [3; 5; 9]`.
> On {nofail}: the `| [] -> []` line of both functions glows TEAL, GREEN "no exception".
> On {use}: the running chain 3 → 5 → 9 → 4 → 7 → [] returns. On {half}: DIM forward-link tag "Lecture 5: merge sort", then `List.length xs / 2` → `- : int = 2`; the GOLD cut falls after cell 2 (scene 1's shot again). On {split}: `take 2 xs` → `[3; 5]` and `drop 2 xs` → `[9; 4; 7]` lift apart, the two halves differing by one element.
> Recap on {recap}: four short lines, one per beat ({r1} to {r4}): "take: the front · drop: the rest", "take: waiting conses + a copy · O(i) time and space", "drop: iterative, 1 new cell, shares the rest · O(i) time, O(1) space", "past the end: they stop, no exception".
> On {next}: the recap clears to the running chain with a GOLD pointer over the 9 and "is 9 in the list?" (ch2's hook shot). Hold an end card ~8 s after the last word; music carries it.

[c1.edges.1] {off} What if you ask for more elements than the list has? {pause} {takeall} Take ten, of three, five, nine, gives three, five, nine, a fresh copy of the whole list. {dropall} And drop ten gives nil. {zero} With a count of zero, or a negative count, take gives nil, and drop gives the whole list back. {nofail} Either way, the nil clause catches the end of the list, so neither function ever raises an exception.

[c1.edges.2] {use} So where would you use them? Typically, to split a collection into equal parts, and process each part recursively. {half} In the next lecture, merge sort does exactly that. It takes half the length, and half of five, rounded down, is two. {split} So take gives three, five, and drop gives nine, four, seven.

[c1.edges.3] {recap} Let's recap. {r1} Take returns the front of a list, and drop returns the rest. {r2} Take leaves a cons waiting for every element it takes, and copies each one, so it needs big O of eye time and space. {r3} Drop is iterative. It rebuilds just one cell, and shares the rest of the list. That's big O of eye time, and constant space. {r4} And past the end of the list, both simply stop, with no exception. {pause} {next} Next time, a question programs ask all the time. Is this element in the list?
