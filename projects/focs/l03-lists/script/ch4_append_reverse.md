# Chapter 4 · Append and reverse

Lecture 3 (Lists), part 4 of 5. Source: FoCS 2026-27 notes, pp. 26–28.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*; see LESSONS.md, "Write for the ear"). `{mark}` is a cue
point; `{pause}` / `{pause=1.5}` is a deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch4_s1_hook)

> Title card: "Lists", "Foundations of Computer Science · Lecture 3", "Part 4: append and reverse".
> Ch1's hook returns, big: cells 3 → 5 → 9 → []. A YELLOW cell 1 joins at the FRONT (GOLD "1 cons",
> O(1)); then a GOLD "?" hovers at the END. A DIM marker walks the arrows (ch1's answer, "walk the
> whole list"); on {more} the "?" stays, turning RED. Then ch1's two built-ins as Code:
> `[3; 5; 9] @ [2; 10]` ⇒ `[3; 5; 9; 2; 10]` and `List.rev [3; 5; 9]` ⇒ `[9; 5; 3]`, each tagged
> YELLOW "build it ourselves"; under `List.rev`, RED "slow" on {slow}, then GREEN "fast" on {fast}.

[c4.hook.1] {title} In the very first chapter, we asked a question that sounded almost too simple. {front} Adding an element to the front of a list is a single cons, one new cell, however long the list is. {end} But what about adding it to the end? {pause} {walk} Back then, we said you'd have to walk the whole list. {more} The truth is a little worse, and in this chapter, we'll see exactly why.

[c4.hook.2] {tools} We also met two tools that come free with OCaml. {at} The at sign, which joins two lists, {rev} and List dot rev, which reverses a list. {build} Today, we build both of them ourselves. {slow} Along the way, we'll meet a natural way to reverse a list that's painfully slow, {fast} and a small change that makes it fast.

## Scene 2 · Append, the code (ch4_s2_code)

> `append [1; 2; 3] [4]` with OCaml's reply `- : int list = [1; 2; 3; 4]` (type in GREEN). Then the
> definition, hero-sized Code (~44): `let rec append xs ys =` / `  match xs, ys with` /
> `  | [], ys    -> ys` / `  | x::xs, ys -> x :: append xs ys`. {match}: FlashUnder + YELLOW on
> `match xs, ys with`, label "a pair" on {pair}. One highlight box (P8) slides `[], ys` → `x::xs, ys`.
> Base: `ys` flies from the pattern into the answer (TransformFromCopy). {fresh}: the pattern's `xs`
> in TEAL, with a DIM tag "the tail, not the whole list"; `append xs ys` boxed as the smaller problem.
> {ride}: every `ys` turns TEAL (passed along, never opened). Infix: `let (@) = append` with reply
> `val ( @ ) : 'a list -> 'a list -> 'a list = <fun>`, then `[1; 2; 3] @ [4]` ⇒ `- : int list = [1; 2; 3; 4]`.
> {type}: the three `'a` in PINK, flashed one by one. {bad}: `[1; 2] @ ["three"]` in RED with
> `Error: This constant has type string but an expression was expected of type int`.

[c4.code.1] {goal} Let's start with append. We want a function that takes two lists, and joins them end to end. {example} Append one, two, three, and the list holding just four, and you should get one, two, three, four. {pause}

[c4.code.2] {code} Here's the definition. {match} Notice something new on the second line. Instead of matching a single list, we match two things at once, {pair} the pair, exes comma whys. {patterns} So each pattern describes both lists together. {complex} Patterns can be as complicated as we like.

[c4.code.3] {base} The first pattern matches when the first list is empty. Then the answer is simply whys. {pause} {step} The second pattern matches when the first list has a head, ex, and a tail, exes. {fresh} Careful, these are new names. Here, exes means just the tail of the first list. {result} So the answer is ex, consed onto the append of that tail and whys.

[c4.code.4] {ride} Notice that whys just comes along for the ride. Append never takes it apart, and that will decide the cost. {infix} For convenience, we turn append into an operator. {at} Let the at sign, in brackets, equal append. {use} The brackets mark it as an operator, so now it goes between the two lists.

[c4.code.5] {type} Now look at the type in OCaml's reply. It takes an alpha list, and another alpha list, and returns an alpha list. {same} The same alpha all three times. So you can join any two lists, as long as their elements have the same type. {bad} Try joining integers to strings, {reject} and OCaml rejects it, before the program even runs.

## Scene 3 · Tracing append (ch4_s3_trace)

> The trace as stacked lines, each born from a copy of the line above (P11, P13); first step slow,
> the rest faster (P24): `append [1; 2; 3] [4]` / `⇒ 1 :: append [2; 3] [4]` /
> `⇒ 1 :: (2 :: append [3] [4])` / `⇒ 1 :: (2 :: (3 :: append [] [4]))` / `⇒ 1 :: (2 :: (3 :: [4]))` /
> `⇒ [1; 2; 3; 4]`. The waiting `1 ::`, `2 ::`, `3 ::` turn YELLOW and stay; a brace under them,
> "waiting" (on {pending}). `append [] [4]` → `[4]` in TEAL. On {done} the conses fire inside out:
> `3 :: [4]`, then `2 ::`, then `1 ::`, collapsing into GREEN `[1; 2; 3; 4]`. On {echo}, a small DIM
> inset of ch3's `1 + (1 + (1 + 0))`, the same nested shape. GOLD "space: one per element of xs".

[c4.trace.1] {start} Let's run it on one, two, three, with four. {s1} The first list has a head, one. So the answer is one, consed onto the append of two, three, with four. {pause} {s2} Same again. Two, consed onto the append of three, with four. {s3} Then three, consed onto the append of nil, with four. {s4} Now the first list is empty, so that append is just four.

[c4.trace.2] {pending} Look at what has piled up. {conses} The one, the two and the three are each waiting to be consed on. {finally} Only now, with the first list used up, can the conses actually happen, from the inside out. {done} Three onto four, then two, then one. {pause} {answer} One, two, three, four.

[c4.trace.3] {notiter} So append is not iterative. {scan} It scans its first argument, sets up a string of conses, and only then does them. {echo} It's the same shape as the first length function from last chapter, with its pile of one-pluses. {space} And those waiting conses take up space, one for each element of the first list.

## Scene 4 · Copying and sharing (ch4_s4_cells)

> Cells (ConsChain), filling the frame: `xs` = 1 → 2 → 3 → [] on top, `ys` = 4 → [] lower right,
> with name pointers. {shortcut}: 3's arrow swings from [] to the 4 (YELLOW); {pause} holds on it.
> {change}: RED cross, and the `xs` pointer briefly reads [1; 2; 3; 4] in RED. Undo. {copy}: new YELLOW
> cells 1, 2, 3 born from copies of the old ones (TransformFromCopy), first slow, then faster; the
> new 3 points at the existing 4, which glows TEAL with the label "shared". Pointer `xs @ ys` on the
> new 1; the old `xs` untouched. {cost}: GOLD counter "new cells: 3" → "n = length of the FIRST list",
> GOLD O(n) time and space. {big}: `ys` stretches to "a million cells" (… and a brace); the counter
> stays at 3 (P20). Payoff, side by side: `x :: xs` = one YELLOW cell, "O(1)" | `xs @ [x]` = every
> cell of `xs` copied, "O(n)". Accumulator aside in DIM, then the maxim as a YELLOW title card:
> "Never add an accumulator merely out of habit."

[c4.cells.1] {cells} Now let's look at the cells in memory. {xs} Here's exes, one, two, three. {ys} And here's whys, the list holding four. {shortcut} The obvious shortcut would be to take the last arrow of exes, which points at nil, and point it at the four instead. {pause} {why} Why can't we do that? {pause}

[c4.cells.2] {change} Because that would change exes. Anyone still holding exes would suddenly see one, two, three, four. And OCaml lists never change once they're built. {copy} So append does the only thing it can. It copies. A new cell for the one, {two} for the two, {three} and for the three. {share} The last new cell points straight at the four, which isn't copied at all. {shared} The two lists share it.

[c4.cells.3] {cost} So append builds a new cell for each element of its first list. {first} If the first list has en elements, that's big O of en, in time and in space. {big} The second list doesn't matter. Make it a million cells long, and append does the same work. {pause}

[c4.cells.4] {payoff} Now we can answer our opening question properly. {front} To put an element on the front of exes, you cons it. A single new cell. {end} To put it on the end, you append exes and a list holding that element. {walk} That doesn't just walk along exes. It copies every cell. {pause} {costs} Front, constant time. End, linear time.

[c4.cells.5] {acc} Could an accumulator help, as it did for length? {could} It could make append iterative, but only with real complication. {still} And it would still have to copy every element of the first list, so it would still need big O of en time and space. {nogain} No gain in big O. At best, a smaller constant factor, and the extra complication will probably cost more than that. {rule} Here's a rule worth remembering. Never add an accumulator merely out of habit.

## Scene 5 · Reversing, the natural way (ch4_s5_nrev)

> `[1; 2; 3]` → `[3; 2; 1]` (Swap the 1 and the 3). Code, hero-sized: `let rec nrev = function` /
> `  | [] -> []` / `  | x::xs -> (nrev xs) @ [x]`, reply `val nrev : 'a list -> 'a list = <fun>`.
> Box slides (P8): `[] -> []`, then `(nrev xs)`, then `@ [x]` (`@` in GOLD from here on). {sense}:
> cells 1 | 2, 3 → the tail flips to 3, 2 and the 1 travels to the back. `nrev [1; 2; 3]` ⇒
> `- : int list = [3; 2; 1]`. Trace, line from copy (P11): `nrev [1; 2; 3]` / `⇒ nrev [2; 3] @ [1]` /
> `⇒ (nrev [3] @ [2]) @ [1]` / `⇒ ((nrev [] @ [3]) @ [2]) @ [1]` / `⇒ (([] @ [3]) @ [2]) @ [1]` /
> `⇒ [3; 2; 1]`. On {but}, all three `@` flash GOLD and stay.

[c4.nrev.1] {task} Now, reversing a list. Here's the most natural way, a function called en-rev. {base} The reverse of nil is nil. {step} And to reverse a list with head ex and tail exes, {tail} first reverse the tail, {end} then put ex on the end, by appending the list holding just ex. {pause}

[c4.nrev.2] {sense} That makes perfect sense. To reverse one, two, three, you reverse two, three, to get three, two, and then put the one on the end. {works} And it works. {reply} En-rev of one, two, three gives three, two, one.

[c4.nrev.3] {trace} Let's trace it. {t1} Each step peels off the head, and leaves an append waiting. {t2} First the one, {t3} then the two, {t4} then the three. When we reach nil, we're left with a chain of appends. {t5} Now they all run, {result} and out comes three, two, one. {pause} {but} But the end of a list is the expensive place to add things, and this function adds there at every step.

## Scene 6 · Counting the cost (ch4_s6_cost)

> Keep `(([] @ [3]) @ [2]) @ [1]` big at the top. Under each `@`, a brace and the cells it copies,
> in GOLD: 0, then 1 (the 3), then 2 (the 3 and the 2). Each `[x]` adds one YELLOW cell. Group by step
> into rows of 1, 2, 3 blocks; GOLD "6 conses". General case: row n = n − 1 GOLD + 1 YELLOW; rows
> n, n − 1, …, 1, 0 → MathTex `0 + 1 + 2 + \cdots + n`. Staircase proof (v1 s6_nrev.triangle,
> N = 7): rows of 0 … n blocks; a BLUE twin, Rotate by PI, slot in → rectangle, braces "n" and
> "n + 1"; formula built piece by piece (P14): `0 + 1 + \cdots + n = n(n+1)/2`. RED O(n²). Then
> n = 1000: GOLD "500,500 conses" vs GREEN "1,000 cells in the answer" (P21). Space: the copies
> appear in turn, each new copy appearing as the previous one fades (DIM "no longer needed"), so the
> cells alive at once stay short; GOLD O(n) space.

[c4.cost.1] {count} So let's count the conses exactly, using the last line of the trace. {inner} The innermost append copies nil, so it copies nothing. {middle} The next copies the list holding three, a single cell. {outer} The outer append copies three, two, which is two cells. {singles} And each little list in square brackets takes a cons to build. {total} Three conses for copying, three for building. Six in all, to reverse just three elements. {pause}

[c4.cost.2] {general} Now give en-rev a list of en elements. {copy} At the top, append copies the reversed tail, which is en minus one conses. {single} Building the list holding ex is one more, so en in total. {down} Reversing the tail costs en minus one, and so on, down to nil, which costs nothing. {sum} So the total is zero, plus one, plus two, and so on, up to en. {pause}

[c4.cost.3] {stairs} Here's a lovely way to add that up. Draw each step as a row of blocks. {stair} Zero blocks, then one, then two, all the way up to en. A staircase. {twin} Now take a second copy, {flip} flip it over, {slot} and slot it in. {rect} Together, they make a rectangle, {wide} en wide, {tall} and en plus one tall. {half} The staircase is exactly half of it. {formula} En times en plus one, over two. {pause=1.5}

[c4.cost.4] {quad} That grows like en squared, so en-rev takes big O of en squared time. Quadratic. {thousand} Reverse a list of a thousand elements, and you build about half a million cons cells, {answer} just to produce an answer with a thousand cells in it. {pause}

[c4.cost.5] {space} And yet the space is only big O of en. {why} Why? Because the copies don't all exist at the same time. {gone} Each copy is only needed until the next append has copied it again. After that, nothing points to it, and its memory can be reused. {lesson} So en-rev wastes time, but not space.

## Scene 7 · Reversing in linear time (ch4_s7_revapp)

> Card piles (v1 s7_rev): a pile with 1 on top, then 2, then 3, and an empty dashed pile. On {cards}
> the top card lifts and arcs across; {again} the next lands on it. Code: `let rec rev_app xs ys =` /
> `  match xs, ys with` / `  | [], ys    -> ys` / `  | x::xs, ys -> rev_app xs (x::ys)`, piles
> labelled `xs` and `ys`. Trace beside the piles, one card move per line (P24, first slow):
> `rev_app [1; 2; 3] []` / `⇒ rev_app [2; 3] [1]` / `⇒ rev_app [3] [2; 1]` / `⇒ rev_app [] [3; 2; 1]` /
> `⇒ [3; 2; 1]`. {flat}: the lines stay the same width (contrast with append's growing trace), DIM
> "iterative". {meaning}: `rev_app [1; 2; 3] [4; 5]` ⇒ `[3; 2; 1; 4; 5]`. Wrapper
> `let rev xs = rev_app xs []`, reply `val rev : 'a list -> 'a list = <fun>`; `rev [1; 2; 3]` ⇒
> `- : int list = [3; 2; 1]`. GOLD counter ticks with each card (P19): 3 → "n conses, exactly", O(n).
> {graph}: v1's plot, conses vs list length, RED curve n(n+1)/2 labelled `nrev`, GREEN line n labelled
> `rev`. {vary}: two DIM machines with different cons times, same straight line.

[c4.rev.1] {better} Can we do better? {cards} Think about how you'd reverse a pile of cards. You'd take the top card off, and put it on a new pile. {again} Then the next card, on top of that. {pause} {done} When the first pile is empty, the new pile is the old one, upside down.

[c4.rev.2] {code} That's exactly this function, rev-app. It takes two lists, the pile exes, and the pile whys. {base} If exes is empty, the answer is whys. {step} Otherwise, take the head, ex, off exes, and cons it onto whys. {recur} Then carry on with the rest.

[c4.rev.3] {t1} Rev-app of one, two, three, and nil. The one moves across. {t2} Then the two, on top of it. {t3} Then the three. {t4} The first list is now empty, so we return the second. Three, two, one. {pause} {flat} And this time, nothing piles up. Each call simply hands over to the next, so rev-app is iterative.

[c4.rev.4] {meaning} In general, rev-app of exes and whys reverses exes, and puts the result in front of whys. {wrap} So to reverse a list on its own, we start with whys empty. {rev} Our rev function just calls rev-app, with nil as the second list. {pause}

[c4.rev.5] {count} And the cost? One cons for each card that moves. {exact} So reversing a list takes exactly one cons per element. That's linear time. {graph} Side by side, {curve} the naive version curves upward, {line} while rev is a straight line. {pause} {whyo} If we can count conses exactly, why bother with big O? {vary} Because the time a single cons takes varies from one computer to another. Big O describes the shape of the cost, wherever you run it.

## Scene 8 · Reduction in strength (ch4_s8_strength)

> Two causes side by side: "accumulator → iterative" | "no more append → O(n) time"; box the second.
> Title "Reduction in strength" (YELLOW). One heavy RED `@` box ("O(n) each") → a run of light TEAL
> `::` boxes ("O(1) each") (v1 s7_rev.strength). History: a row `0 × 7`, `1 × 7`, `2 × 7`, `3 × 7`, DIM
> "no hardware multiply"; each × crossed out, replaced by "+ 7" arcs between 0, 7, 14, 21 (GOLD).
> Caveat: `let iter_append xs ys = rev_app (rev xs) ys`, reply
> `val iter_append : 'a list -> 'a list -> 'a list = <fun>`, `iter_append [1; 2; 3] [4]` ⇒
> `- : int list = [1; 2; 3; 4]`; cells: 3 YELLOW for `rev xs`, then 3 more for the result; GOLD
> "6 conses" vs "3 conses" for `append`; RED "an extra reversal". Recap: four short lines, one per
> beat. Teaser for chapter 5: `'a'` and `"abc"` side by side, "strings and characters", then "exercises".

[c4.str.1] {what} So what made rev-app fast? {acc} Its accumulator, whys, makes it iterative. {but} But that's not where the speed comes from. {gone} The real gain is that append is gone. {pause} {swap} We replaced an expensive operation, append, with a series of cheap ones, single conses. {name} This is called reduction in strength, and it's a common technique in computer science.

[c4.str.2] {history} The idea dates from when many computers had no hardware multiply instruction. {products} Suppose you needed zero times seven, then one times seven, then two times seven, and so on. {adds} Instead of multiplying, you could just keep adding seven. Zero, seven, fourteen, twenty-one. {same} The same answers, from cheap additions. {again} You'll see this trick many times in this course, very often to get rid of an append.

[c4.str.3] {caveat} One warning, though. {backwards} Consing onto an accumulator builds the result backwards, just as rev-app did. {iterapp} Remember the iterative append we decided not to write? With rev-app, it's short. Reverse the first list, then rev-app it onto the second. {double} It's iterative, but it makes twice as many conses as plain append. {pause} {rule} So if an accumulator forces an extra reversal, the iterative version can be much slower than the recursive one.

[c4.recap.1] {recap} Let's recap. {r1} Append copies its first list and shares its second, so its cost depends only on the first list. {r2} Adding to the end means copying, and doing that at every step made en-rev quadratic. {r3} Rev-app moves elements one at a time onto an accumulator, and reverses a list with exactly one cons per element. {r4} And replacing an expensive operation with a series of cheap ones is reduction in strength. {pause} {next} Next time, strings and characters, and then some exercises to try yourself.
