# Chapter 5 · Every way to make change

Lecture 4 (More on Lists), part 5 of 7. Source: FoCS 2026-27 notes v1.8, pp. 34–35 (§4.7); forward link p. 49.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

As in ch4, the narration never says the letter for the variable `c`; it says "the coin", while the
screen highlights `c`. The local function `allc` is said "all-see"; `cs` and `css` are spelled out.

---

## Scene 1 · Hook (ch5_s1_hook)

> Title card: "More on Lists", "Foundations of Computer Science · Lecture 4", "Part 5 · Every way to make change".
> Reopen on ch4_s6_greedy's setting: the till as a ConsChain of GOLD discs 5 → 2 → [], the GOLD amount counter "6", an empty "paid" row below. {stuck}: a copy of the 5 disc drops into the paid row, the counter 6 → 1.
> {fail}: the 5 cell, then the 2 cell, dims with a small RED "too big" and slides off; only the TEAL nil is left, and ch4's reply appears in RED, `Exception: Failure "no more coins!".` (ch4's code on `change [5; 2] 6`, checked in OCaml 5.4.1).
> {twos}: three 2 discs drop into a fresh row, GREEN "2 + 2 + 2 = 6".
> {idea}: the paid row shrinks into one path, an edge from a node "6, [5; 2]" down to a RED dead end, labelled "use 5". {all}: YELLOW "every way, not one". {tree}: a second edge opens beside the first, "skip 5", down to the three GREEN 2s. Outline only; s3 fills in this tree.
> {today}: a preview of the answer's shape, a TEAL bracket box holding a few small TEAL boxes of GOLD discs.

[c5.hook.1] {title} Last time, we wrote a greedy function for making change, which always grabs the largest coin that fits. {stuck} With coins of five and two, and an amount of six, it took the five, and that left one. {fail} Every coin was now too big, the till ran out, and it raised an exception. {pause} {twos} Yet there's a way to make six. Two, plus two, plus two.

[c5.hook.2] {idea} The trouble is that greedy commits to its first choice, and never takes it back. {all} So here's a new idea. Instead of returning one way to make change, return every way. {tree} Then a dead end only closes one path, and the other paths still get explored. {today} In this chapter, we'll write that function, and see how one list can hold all of its answers. {pause}

## Scene 2 · A list of answers (ch5_s2_answers)

> {type}: top, DIM, ch4's reply `val change : int list -> int -> int list = <fun>`. {one}: below it, one solution, a TEAL bracket box holding GOLD discs 2, 2, 2, labelled "one way: `int list`".
> {many}: a bigger TEAL box opens around it; {example} its contents become three solution boxes, [2 2], [2 1 1], [1 1 1 1], with `[[2; 2]; [2; 1; 1]; [1; 1; 1; 1]]` under it. These are s6's answers; keep this look for every list of solutions in the chapter.
> {listlist}: the type grows, `int list` → `int list list`, the new `list` flashing GREEN; label "a list of solutions".
> Clear to a split. Left, {zero}: GOLD amount "0" → {nil} a TEAL box holding one empty box, `[[]]`; {success} GREEN "one way: no coins".
> Right, {none}: an empty till `[]` with GOLD "6" still owed → {noway} an empty TEAL box, `[]`; {failure} RED "no ways".
> {pair}: the two boxes side by side, centred and large, GREEN "success" under `[[]]`, RED "failure" under `[]`; hold through the pause.
> {noraise}: a small RED `Exception: Failure "no more coins!".` (ch4) is struck out. {combine}: an empty box drops into a row of solution boxes, and the row stays exactly as it was.

[c5.answers.1] {type} First, what should the new function return? {one} One way of making change is a list of coins, such as two, two, two. {many} So every way, all together, is a list of those lists. {example} Here's an example: coins of two and one give three ways to make four. Two and two. Two, one and one. And four ones. {listlist} So the result type becomes int list list, a list of int lists.

[c5.answers.2] {zero} Now the base cases, which need some care. How many ways are there to make change for zero? {pause} {exactly} Exactly one. You hand over no coins at all. {nil} No coins is the empty list, so the answer is a list holding one empty list. {success} That's success, with one solution, which happens to be empty.

[c5.answers.3] {none} Now suppose the till is empty, but there's still money to pay. {noway} Then there are no ways at all, so the answer is the empty list, holding no solutions. {failure} That's failure. {pair} So a list holding nil means one way, using nothing, while nil itself means no way. {pause=1.5}

[c5.answers.4] {noraise} So this version has no need for an exception. {quiet} It reports failure by returning no solutions. {combine} And no solutions is easy to combine with others. When we gather up the answers from several paths, a dead end simply adds nothing.

## Scene 3 · Use it, or skip it (ch5_s3_choices)

> {coin}: hero, the till [5; 2] as GOLD discs, the 5 lifted and glowing. {two}: two arrows out of it, "use 5" and "skip 5". {use}: "use 5" shows 6 − 5 with the 5 returning to the till; {skip}: "skip 5" shows the 5 leaving the till, amount still 6. {sources}: YELLOW "two sources of solutions" bracing both arrows.
> {tree}: s1's outline grows into the full tree for `change [5; 2] 6`, top-down. Nodes read "amount, till" (amount GOLD, till TEAL), edges "use c" / "skip c". {root}: "6, [5; 2]".
> {usefive}: left edge "use 5" → "1, [5; 2]". {toobig}: → "skip 5 (too big)" → "1, [2]" → "skip 2 (too big)" → "1, []". {dead}: RED `[]`.
> {skipfive}: right edge "skip 5" → "6, [2]"; {chain}: "use 2" → "4, [2]" → "use 2" → "2, [2]" → "use 2" → "0, [2]"; {success}: GREEN `[[]]`. {stubs}: the three "skip 2" branches, "6, []", "4, []", "2, []", each end in a small DIM RED `[]`.
> {back}: answers rise up the tree, each written beside its node: `[[]]` → `[[2]]` → `[[2; 2]]` → `[[2; 2; 2]]`. {add}: on every "use 2" edge a GOLD 2 disc slides onto the front of each solution box passing up. The left branch carries `[]` up, and the "use 5" edge has nothing to put a 5 on.
> {join}: at the root, `[] @ [[2; 2; 2]]` (the `@` GOLD) ⇒ {answer} GREEN `[[2; 2; 2]]`. {missed}: the left path glows RED, labelled "greedy's path".
> Keep this layout: s6 reuses it for `change [2; 1] 4`, and so does ch6's trace.

[c5.choices.1] {coin} So how do we find every way? Look at the largest coin in the till, and ask one question about it. {pause} {two} Every solution either uses that coin, or leaves it out. {use} If it uses the coin, we hand that coin over, and still need change for the amount minus the coin. And the same coin may be used again. {skip} If it leaves the coin out, we need change for the whole amount, from the rest of the till. {sources} So there are two sources of solutions, and we want them both.

[c5.choices.2] {tree} Let's draw it as a tree, for six, with fives and twos. {root} Each node shows the amount still owed, and the coins still allowed. {usefive} On the left, we use the five. That leaves one, still with fives and twos. {toobig} Now the five is too big, so it must be skipped, and so must the two. {dead} The till is empty, with one still owed. A dead end, with no solutions. {pause}

[c5.choices.3] {skipfive} On the right, we skip the five, and need six from twos alone. {chain} Use a two, leaving four. Use another, leaving two. Use a third, leaving zero. {success} Zero is success, one way, with no coins. {stubs} Along the way, each skip branch empties the till with money still owed, so those are dead ends too.

[c5.choices.4] {back} Now the answers flow back up. {add} On each edge where we used a two, a two goes onto the front of every solution coming up. {growing} The empty solution becomes a single two, then a pair of twos, then three twos. {join} At the top, the left side brings nothing, and the right side brings one solution. {answer} Joined together, that's a list holding one solution, two, two, two. {pause} {missed} That's the answer greedy missed, because greedy only ever walked the left path.

## Scene 4 · The code (ch5_s4_code)

> In [72], hero-sized Code, verbatim from the notes (p. 34; `else` sits one column left of `if`, as printed; this text, and every reply in this scene, checked in OCaml 5.4.1): `let rec change till amt =` / `  match till, amt with` / `  | _       , 0   -> [ [] ]` / `  | []      , _   -> []` / `  | c::till , amt -> if amt < c then change till amt` / `                    else let rec allc = function` / `                           | [] -> []` / `                           | cs :: css -> (c::cs) :: allc css` / `                         in` / `                           allc (change (c::till) (amt - c)) @` / `                                 change till amt`.
> {match}: FlashUnder on `match till, amt with`. {first}: a highlight box (P8) on the `0` clause, and s2's GREEN box-in-box flies in beside it. {second}: the box slides to the `[]` clause, s2's RED empty box beside it. {noraise}: DIM inset of ch4's `raise (Failure "no more coins!")`, struck out.
> {third}: box on `c::till`, with `c` YELLOW. {toobig}: `if amt < c then change till amt` boxed, label "too big: skip only" (s3's left path). {else}: the `let rec allc … in` lines dim (s5 opens them up).
> {usecall}: `allc (change (c::till) (amt - c))` YELLOW, label "use c"; {back}: `(c::till)` flashes TEAL, "c goes back". {skipcall}: the last line's `change till amt` BLUE, label "skip c". {at}: the `@` GOLD. {deadend}: a small `[] @` row joins a solution row, which stays the same. {allc}: `allc` flashes YELLOW.
> {reply}: `val change : int list -> int -> int list list = <fun>`, with `int list list` GREEN.
> {check}: three calls stack below, each with its reply: {zero} `change [5; 2] 0` ⇒ `- : int list list = [[]]`; {one} `change [5; 2] 1` ⇒ `- : int list list = []`; {six} `change [5; 2] 6` ⇒ `- : int list list = [[2; 2; 2]]` (GREEN, s3's answer).

[c5.code.1] {code} Here's the code. It starts just like the greedy version. {match} We match on the till and the amount together. {first} The first clause says that change for zero, whatever the till, is a list holding one empty list. {second} The second says that an empty till, with money still owed, gives no solutions. {noraise} Where greedy raised an exception, this version simply returns nil.

[c5.code.2] {third} The third clause takes the till apart, into its largest coin, and the rest of the till. {toobig} If the amount is less than the coin, the coin is too big, so skipping it is the only choice. We make change from the rest of the till, for the same amount. {pause} {else} Otherwise, both choices are open.

[c5.code.3] {usecall} To use the coin, we make change for the amount minus the coin, {back} with the coin put back on the till, so it can be used again, as in the greedy version. {skipcall} To skip it, we make change for the full amount, from the rest of the till. {at} Then the at sign appends both lists of solutions. {deadend} If one side is a dead end, it contributes nil, and appending nil changes nothing. {allc} Before the append, the use side's solutions pass through all-see, which we'll open up next.

[c5.code.4] {reply} OCaml's reply confirms the new type. It takes an int list and an int, and returns an int list list. {check} Let's check the cases we've seen. {zero} Change for zero, with fives and twos, gives a list holding nil. {one} Change for one gives nil. No way. {six} And change for six gives one solution, two, two, two, the answer from our tree. {pause}

## Scene 5 · Putting c on every answer (ch5_s5_allc)

> The four `allc` lines lift out of In [72] (TransformFromCopy) and grow to hero size: `let rec allc = function` / `  | [] -> []` / `  | cs :: css -> (c::cs) :: allc css` / `in`. Name `allc` YELLOW.
> {walk}: a YELLOW pointer steps down a list of solution boxes. {base}: highlight box on `| [] -> []`. {step}: box on `cs :: css`, labels "one solution" under `cs` and "the rest" under `css`. {cons}: `(c::cs)` YELLOW.
> {example}: a GOLD 2 disc labelled `c = 2` hovers; {input} `[[2]; [1; 1]]` as two TEAL solution boxes (s2's look); {output} the 2 disc copies onto the front of each box in turn ⇒ `[[2; 2]; [2; 1; 1]]`; {same} GOLD "2 solutions → 2 solutions". This exact pair returns in s6 on the top-left edge. Checked standalone: after `let c = 2;;`, `allc [[2]; [1; 1]]` ⇒ `- : int list list = [[2; 2]; [2; 1; 1]]`.
> {needs}: the `c` in `(c::cs)` glows YELLOW, with an arrow back to the `c` of `c::till` in In [72]. {outside}: the same `allc` typed alone at top level, with OCaml 5.4.1's reply in RED (checked): `Line 3, characters 18-19:` / `3 |   | cs :: css -> (c::cs) :: allc css;;` / `                      ^` / `Error: Unbound value c` (at least the `Error` line; the caret sits under the `c` of `(c::cs)`). {letin}: back in In [72], a bracket from `let rec allc` to `in`, labelled "local, as in unzip".
> {tempt}: the tempting edit, In [72] without `allc`, its `else` branch now `                    else (c :: change (c::till) (amt - c)) @` / `                              change till amt`. {wrong}: a lone 2 disc joins the row of solution boxes as if it were one more solution, RED "?". {error}: in RED, OCaml 5.4.1's reply (checked): `Line 6, characters 31-57:` / `6 |                     else (c :: change (c::till) (amt - c)) @` / `                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^` / `Error: This expression has type 'a list list` / `       but an expression was expected of type int list` / `       Type 'a list is not compatible with type int` (the location lines may go; the carets underline `change (c::till) (amt - c)`).
> {names}: `cs` and `css` big, side by side, with L3's `xs` DIM beside them; {cs} label "a list of coins", {css} label "a list of such lists"; {plural} each trailing `s` flashes YELLOW.

[c5.allc.1] {what} All-see takes a list of solutions, and puts the coin on the front of every one. {walk} It walks down the list, one solution at a time. {base} No solutions in, no solutions out. {step} Otherwise, there's a first solution, see-ess, and the rest, see-ess-ess. {cons} It conses the coin onto see-ess, and does the same to the rest.

[c5.allc.2] {example} Let's try an example, with the coin two. {input} Suppose change for the smaller amount gave two solutions, a single two, and one plus one. {output} All-see turns them into two, two, and two, one, one. {pause} {same} The same number of solutions, each one coin longer.

[c5.allc.3] {local} Why is it declared inside change? {needs} Because it uses the coin, and the coin only has a name inside the third clause. {outside} Declare all-see on its own, outside change, and OCaml stops with an error. The coin's name is unbound there. {letin} This is a let expression, just as in unzip, but this time, what it declares locally is a recursive function.

[c5.allc.4] {tempt} You might be tempted to skip all-see, and cons the coin straight onto the result of the recursive call. {pause} {wrong} But that would try to add the coin as one more solution, instead of adding it to each solution. {error} OCaml rejects it. After the coin, the cons expects a list of coins, but change returns a list of lists. {names} Notice the names, too. {cs} See-ess is a list of coins. {css} See-ess-ess is a list of such lists. {plural} The trailing ess suggests a plural, just as exes was the plural of ex.

## Scene 6 · Three ways to make four (ch5_s6_trace)

> s3's tree layout, for `change [2; 1] 4`. {root}: "4, [2; 1]". {use}: left edge "use 2" → "2, [2; 1]". {skip}: right edge "skip 2" → "4, [1]".
> {left}: "2, [2; 1]" splits again. {zero}: "use 2" → "0, [2; 1]" → GREEN `[[]]`, and a 2 disc slides on as it rises ⇒ `[[2]]`. {ones}: "skip 2" → "2, [1]", drawn as one collapsed node with result `[[1; 1]]` (DIM "ones only: one way"). {joinleft}: `[[2]] @ [[1; 1]]` ⇒ `[[2]; [1; 1]]` beside "2, [2; 1]".
> {allc}: s5's shot returns on the top-left "use 2" edge, the same two boxes, a 2 disc onto each ⇒ {front} `[[2; 2]; [2; 1; 1]]`.
> {right}: "4, [1]" collapsed, result `[[1; 1; 1; 1]]`.
> {join}: at the root, `[[2; 2]; [2; 1; 1]] @ [[1; 1; 1; 1]]` (the `@` GOLD) ⇒ {answer} GREEN `[[2; 2]; [2; 1; 1]; [1; 1; 1; 1]]`, then the three solution boxes exactly as in s2.
> {reply}: `change [2; 1] 4` ⇒ `- : int list list = [[2; 2]; [2; 1; 1]; [1; 1; 1; 1]]` (every reply in this scene checked in OCaml 5.4.1). {order}: brace the first two boxes "use 2", the last "skip 2".
> {five}: `change [5; 2; 1] 6` with its reply, which OCaml prints over two lines: `- : int list list =` / `[[5; 1]; [2; 2; 2]; [2; 2; 1; 1]; [2; 1; 1; 1; 1]; [1; 1; 1; 1; 1; 1]]`, and a GOLD counter "5 ways".
> {greedy}: `[5; 1]` turns YELLOW, with ch4's greedy reply beside it, `- : int list = [5; 1]` (ch4's `change [5; 2; 1] 6`, checked).

[c5.trace.1] {start} Now let's trace a case with more than one answer. Change for four, with twos and ones. {root} The two fits, so we can use it, or skip it. {use} We can use the two, leaving two, still with twos and ones. {skip} Or we can skip it, and make four from ones alone. {pause}

[c5.trace.2] {left} Take the left side first. We owe two, with twos and ones still allowed, and it splits again. {zero} Using a two reaches zero, which gives the list holding nil. All-see puts a two on that empty solution, so we get a single two. {ones} Skipping the two means making two from ones, and that gives one plus one. {joinleft} Append them, and change for two has two solutions, a single two, and one plus one.

[c5.trace.3] {allc} That's exactly what we gave all-see a moment ago. {front} Back on the top-left edge, a two goes onto the front of each, giving two plus two, and two plus one plus one. {right} On the right, four from ones alone has one way, four ones. {join} The at sign appends the two sides. {answer} Three ways. Two, two. Two, one, one. And one, one, one, one. {pause}

[c5.trace.4] {reply} OCaml agrees. {order} Notice the order. Solutions with larger coins come first, because the use branch goes in front of the skip branch. {five} With all three coins, five, two and one, there are five ways to make six, from five plus one, down to six ones. {greedy} Five plus one comes first, and that's exactly what greedy would have given.

## Scene 7 · Recap (ch5_s7_recap)

> {challenge}: a quote card, the notes' own words (p. 35): "This complicated program, and the even trickier one in the next section, are included as challenges." "challenges" YELLOW.
> {later}: DIM "making change returns, with exceptions, in a later lecture".
> Recap: four short lines appear one per beat, {r1} to {r4}, each with a small icon from its scene: the box of boxes with `int list list` (s2), `[[]]` beside `[]` (s2), the use / skip fork (s3), and a 2 disc sliding onto each box (s5).
> {next}: In [72] returns small; `allc` and `@` glow GOLD, labelled "copies"; then YELLOW "accumulators?".
> End card after the last word (~8 s; music carries it).

[c5.recap.1] {challenge} The notes call this program a challenge, and they promise an even trickier one next. {normal} If it took you a couple of passes, that's normal. Trace a small case by hand, and it gets much clearer. {later} We'll come back to making change in a later lecture, when we study exceptions.

[c5.recap.2] {recap} Let's recap. {r1} We return every way as a list of solutions, where each solution is an int list. {r2} Change for zero has exactly one solution, using no coins, and an empty till, with money still owed, has none. {r3} At each coin, there are two sources of answers, using it or skipping it, and the append joins them. {r4} And the local function all-see puts the coin on the front of every solution from the use branch. {pause} {next} Next time, we'll notice how much copying all-see and the append do, and ask whether accumulators can help, as they did for reverse.
