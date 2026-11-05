# Chapter 4 · Making change

Lecture 4 (More on Lists), part 4 of 7. Source: FoCS 2026-27 notes v1.8, pp. 33–34 (§4.6).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*; see LESSONS.md, "Write for the ear"). `{mark}` is a cue
point; `{pause}` / `{pause=1.5}` is a deliberate hold. `>` lines are the visual brief.

All code and replies below were run in OCaml 5.4.1 (`ocaml < file.ml`) and are quoted verbatim.
Coins are GOLD discs labelled with their value, the style ch5–ch7 reuse. The narration never says
the letter for `c`; it says "the coin", while the screen highlights `c`.

---

## Scene 1 · Hook (ch4_s1_hook)

> Title card: "More on Lists", "Foundations of Computer Science · Lecture 4", "Part 4 · Making change".
> {title}: under the card, small and DIM, ch3's picture `[x₁ … xₙ], [y₁ … yₙ] ↦ [(x₁, y₁) … (xₙ, yₙ)]`
> zipping and unzipping once; it clears on {till}.
> {till}: the till, a row of six GOLD coin discs labelled 50, 20, 10, 5, 2, 1, each with a short stack
> behind it and a DIM caption "unlimited supply". {owe}: GOLD "43p" at the right, YELLOW tag "change".
> {which}: a YELLOW "?" between them.
> {grab}: a YELLOW ring hops onto the 50 (RED flash: too big), then the 20 (fits); a copy of the 20
> disc drops below the till, and the amount reads "43p → 23p". {program}: a copy of the discs becomes
> Code `[50; 20; 10; 5; 2; 1]` beside a GOLD `43` (the numbers GOLD).
> {catch}: a small second till at the side, discs 5 and 2, amount "6p", with a RED "?" (scene 6's case).
> End on the six discs alone, centred; scene 2 fades them back in as the start of its list.

[c4.hook.1] {title} Last time, we zipped two lists into a list of pairs, and unzipped them again. {till} This time, a problem from everyday life. You're working at a till with an endless supply of coins, fifty, twenty, ten, five, two and one pence. {owe} A customer is owed forty-three pence in change. {pause} {which} Which coins do you hand over? {pause}

[c4.hook.2] {grab} Most people grab the biggest coin that fits, here a twenty, and then repeat with what's left. {program} In this chapter, we'll turn that into a program, and watch it make forty-three pence. {catch} Then we'll find a till where it gets stuck, even though the change can be made. {pause}

## Scene 2 · The plan (ch4_s2_idea)

> Opens on the hook's six GOLD discs. {list}: they slide into a ConsChain 50 → 20 → 10 → 5 → 2 → 1 → []
> (each cell holds its disc, nil TEAL), with the name `till` in YELLOW pointing at the first cell.
> {desc}: a BLUE arrow above the chain, large to small, labelled "descending". {ints}: GREEN `int list`
> under the chain.
> {head}: the first cell glows YELLOW; the `till` pointer's arrow is labelled "one arrow away" (L3 ch1:
> taking the head is O(1)). {pennies}: a long DIM row of forty-three 1p discs flashes up, struck through
> in RED, and clears.
> {obs}: three observation cards stack at the right, BLUE numbers, one per mark: {zero} "1. change for 0
> = no coins", with a TEAL `[]`; {try} "2. largest coin fits? use it, reduce the amount"; {skip}
> "3. too large? remove it".
> {try43}: GOLD "43" under the chain. {fifty}: the 50 cell dims and slides off to the left (card 3
> flashes); `till` now points at the 20. {twenty}: a copy of the 20 disc drops into an answer row below
> (card 2 flashes); the amount ticks 43 → 23. {again}: the 20 cell stays put, a YELLOW ring on it,
> "still in the till".
> {each}: the chain clears; end on the three cards alone. Scene 3 re-creates them beside the clauses.

[c4.idea.1] {list} First, the till becomes a list of coin values, {desc} in descending order, fifty, twenty, ten, five, two, one. {ints} Coin values are just whole numbers, so the till is an int list. {head} Why that order? {pause} Because the head of a list is the element that's easiest to reach, just one arrow away. {big} So the largest coin is always at hand. {pennies} We want to try it first, rather than hand over forty-three pennies.

[c4.idea.2] {obs} The code rests on three simple observations. {zero} First, change for zero is the empty list, no coins at all. {try} Second, for any other amount, try the largest coin. If it's small enough, use it, and take its value off the amount. {skip} Third, if a coin is too large, we remove it from consideration. {pause}

[c4.idea.3] {try43} Let's try them on forty-three. {fifty} Fifty is too large, so it goes. {twenty} Twenty fits, so we use it, and twenty-three is left. {again} And the twenty stays in the till, because we might need it again. {pause} {each} Each observation will become one clause of the program.

## Scene 3 · The code (ch4_s3_code)

> Hero Code, verbatim (the notes' In [71], checked in OCaml 5.4.1), function name YELLOW:
> `let rec change till amt =` / `  match till, amt with` / `  | _, 0         -> []` /
> `  | [], _        -> raise (Failure "no more coins!")` /
> `  | c::till, amt -> if amt < c then change till amt` / `                    else c :: change (c::till) (amt - c)`
> {match}: FlashUnder on `match till, amt with`; {pair}: tag "a pair, as in append and zip". One
> highlight box slides clause to clause; scene 2's cards come back, each beside its clause.
> {zero}: box on `_, 0 -> []`, card 1 beside it; {const}: the `0` GOLD, tag "a constant: matches only 0";
> {any}: the `_` flashes, tag "wildcard: any till"; the `[]` TEAL.
> {raise}: box on clause 2, `raise (Failure "no more coins!")` RED; {first}: YELLOW tag "our first raise".
> {before}: a DIM inset from L3 ch2, `Exception: Match_failure ("//toplevel//", 1, 7).` labelled "from
> OCaml"; {own}: beside it, RED `Exception: Failure "no more coins!".` labelled "from our program".
> {later}: DIM tag "exceptions: a later lecture". Insets clear.
> {third}: box on clause 3. {names}: `c` YELLOW ("first coin"); {fresh}: the pattern's `till` TEAL, tag
> "the rest: a new name". {small}: `if amt < c then change till amt` underlined; {obs3}: card 3 flashes.
> {use}: `else c :: change (c::till) (amt - c)`, card 2 beside it; {back}: `(c::till)` boxed YELLOW,
> {again}: tag "put the coin back". {forget}: `(c::till)` becomes `till` in RED, and under it
> `change [50; 20; 10; 5; 2; 1] 43` ⇒ `Exception: Failure "no more coins!".` (checked); {short}: GOLD
> `20 + 10 + 5 + 2 + 1 = 38`. Undo: `(c::till)` returns.
> {type}: reply `val change : int list -> int -> int list = <fun>`, types GREEN; {parts}: braces under
> the three parts, "till", "amount", "coins to hand over". {ints}: the `-` in `amt - c` flashes GREEN,
> tag "int only" (`<` alone would work at any type, ch2). {fits}: clause 2's `raise` flashes, tag
> "never returns". End on the code and reply; scene 5 brings the code back, compact.

[c4.code.1] {code} Here's the program. {match} Like append, and like zip, it matches two things at once, {pair} the till and the amount, as a pair. {zero} The first clause is our first observation. Its pattern is the wildcard, and a zero. {const} That zero is a constant inside a pattern, so it only matches when the amount is exactly zero. {any} The wildcard says any till will do. Change for zero is nil.

[c4.code.2] {empty} The second clause catches the case where the till is empty, but money is still owed. {raise} There's nothing left to hand over, so the program raises an exception, called Failure, with the message, no more coins. {first} That's our first raise. {before} So far, every exception came from OCaml itself, like match failure in lecture three, when no clause fitted. {own} Here, the program decides to fail, and says why. {later} Exceptions are covered properly in a later lecture.

[c4.code.3] {third} The third clause does the real work. {names} Its pattern splits the till into its first coin, and the rest, which it calls till again. {fresh} That's a new name, as in lecture three. From here on, till means just the rest. {small} If the amount is less than the coin, the coin is too large, so we make change from the rest of the till. {obs3} That's observation three.

[c4.code.4] {use} Otherwise, the coin fits, so we use it. {cons} The answer is the coin, consed onto the change for the amount minus the coin. {back} But look at the till in that call. {pause} It's the coin, consed back onto the rest. {again} We put the coin back, so it can be used again. {forget} Forget that, and each coin could be used only once. {short} Then forty-three would fail, because twenty, ten, five, two and one only add up to thirty-eight. {pause}

[c4.code.5] {type} OCaml's reply gives the type. {parts} It takes an int list, the till, and an int, the amount, and returns an int list, the coins to hand over. {ints} The values are ints, not alpha, because the code subtracts them, and minus works only on ints. {fits} And the raise clause never returns at all, so it can stand in for an int list.

## Scene 4 · Making 43p (ch4_s4_trace)

> Scene 2's setting returns: the till ConsChain 50 → 20 → 10 → 5 → 2 → 1 → [] top left with its `till`
> pointer, a big GOLD amount counter "43" at the right, an empty answer row below. Across the top, the
> current call as one line of Code, rewritten at each step (Transform). The ten calls, checked by
> instrumenting `change` (OCaml 5.4.1): `change [50; 20; 10; 5; 2; 1] 43`, `change [20; 10; 5; 2; 1] 43`,
> `change [20; 10; 5; 2; 1] 23`, `change [20; 10; 5; 2; 1] 3`, `change [10; 5; 2; 1] 3`, `change [5; 2; 1] 3`,
> `change [2; 1] 3`, `change [2; 1] 1`, `change [1] 1`, `change [1] 0`.
> A skip: the head cell dims and slides off left, and `till` moves on. A use: a copy of the head disc
> drops into the answer row as a YELLOW `20 ::`, and the counter ticks down. First step slow, the rest
> faster. {fifty} skip 50; {twenty} use 20 (43 → 23); {again} use 20 (23 → 3); {skips} skip 20, 10, 5 in
> quick succession; {two} use 2 (3 → 1); {skip2} skip 2; {one} use 1 (1 → 0); {zero} a TEAL `[]` closes
> the row: `20 :: 20 :: 2 :: 1 :: []`.
> {wait}: brace under the row, "waiting", in the style of L3's append trace and ch1's take trace.
> {notiter}: DIM "not iterative"; {space}: GOLD "one waiting cons per coin".
> {fire}: the conses fire inside out, collapsing into GREEN `[20; 20; 2; 1]`; {answer}: reply
> `- : int list = [20; 20; 2; 1]`. {check}: GOLD `20 + 20 + 2 + 1 = 43`.
> {ninety}: `change [50; 20; 10; 5; 2; 1] 99`; {nn}: `- : int list = [50; 20; 20; 5; 2; 2]` (checked).

[c4.trace.1] {start} Let's make change for forty-three. {fifty} Forty-three is less than fifty, so the fifty goes, and we carry on with the rest of the till. {twenty} Twenty fits. So the answer starts with twenty, consed onto the change for twenty-three, with twenty still at the front of the till. {again} Twenty fits again, and three is left.

[c4.trace.2] {skips} Three is less than twenty, less than ten, and less than five, so those coins go, one call each. {two} Two fits, and one is left. {skip2} Now two is too large, so it goes too. {one} One fits, and zero is left. {zero} And change for zero is nil. {pause}

[c4.trace.3] {wait} Look at what has piled up. A twenty, another twenty, a two and a one, each waiting to be consed on, just like in take. {notiter} So change is not iterative. {space} Like take, it holds one waiting cons for every coin it hands over. {fire} Now the conses happen, from the inside out, {answer} and out comes twenty, twenty, two, one. {check} That adds up to forty-three. {pause} {ninety} Try ninety-nine pence instead, {nn} and you get fifty, twenty, twenty, five, two, two.

## Scene 5 · Why stop at zero? (ch4_s5_zero)

> Scene 3's code, compact at the left. {success}: GREEN tag "success" on `_, 0 -> []`; {failure}: RED
> tag "failure" on the raise clause. {order}: `change [] 0` ⇒ `- : int list = []` (checked): the first
> clause wins, because clauses are tried in order (ch3).
> {last}: the end of scene 4's trace, three lines, each from a copy of the one above: `change [1] 1` /
> `⇒ 1 :: change [1] 0` / `⇒ 1 :: []`. The last coin is used like every other one; {nothing}: the `[]`
> glows TEAL, tag "does nothing".
> {novice}: a DIM-framed card at the right, "a base case of one", with Code (checked, OCaml 5.4.1):
> `let rec nchange till amt =` / `  match till with` / `  | []      -> raise (Failure "no more coins!")` /
> `  | c::till -> if amt = c then [c]` / `               else if amt < c then nchange till amt` /
> `               else c :: nchange (c::till) (amt - c)`. {work}: `if amt = c then [c]` RED, tag "the base
> case builds a list". {fails}: `nchange [50; 20; 10; 5; 2; 1] 0` ⇒ `Exception: Failure "no more coins!".` in RED
> (on 43 it does give `[20; 20; 2; 1]`, so it is only zero that breaks).
> {rule}: everything clears to a YELLOW title card, "Most procedures are simplest when their base case
> does nothing."; {sign}: under it, smaller, "A base case of one instead of zero is often a sign of a novice."

[c4.zero.1] {stops} So there are two ways for change to stop. {success} If the amount reaches zero, that's success. {failure} If the till runs out first, that's failure, and the exception. {order} The clauses are tried in order, so an empty till with nothing owed still counts as success. Even from an empty till, change for zero gives nil, the empty list. {pause}

[c4.zero.2] {why} Nobody ever asks for change for zero. {pause} So why is that the base case? {simple} Because it's the simplest way to make the algorithm stop. {last} Look at the last coin from our trace. The one went in just like every other coin, and left zero behind. {nothing} Then the base case does nothing at all. It just returns nil.

[c4.zero.3] {novice} A beginner might stop one step earlier, when the amount equals a coin, and return just that coin. {work} Then the base case has work of its own to do, building a list with that coin in it. {fails} And it gets zero wrong. Ask it for zero, and it runs out of coins. {rule} The course notes draw a general lesson. Most procedures that repeat a step are simplest when, in their base case, they do nothing. {sign} A base case of one, instead of zero, is often the sign of a novice. {pause}

## Scene 6 · Where greedy fails (ch4_s6_greedy)

> {greedy}: YELLOW word "greedy", with "largest first, never reconsider" under it. {new}: a new till,
> a ConsChain of GOLD discs 5 → 2 → [], the GOLD amount counter "6", and an empty "paid" row below.
> The trace, stacked lines, each born from a copy of the one above (checked): `change [5; 2] 6` /
> `⇒ 5 :: change [5; 2] 1` / `⇒ 5 :: change [2] 1` / `⇒ 5 :: change [] 1`. {five}: a copy of the 5 disc
> drops into the paid row, the counter 6 → 1; {stuck5} and {stuck2}: the 5 cell, then the 2 cell, dims
> with a small RED "too big" and slides off; {empty}: only the TEAL nil is left, the counter stuck RED
> at 1; {fail}: RED `Exception: Failure "no more coins!".`
> {but}: beside it, GREEN: three 2 discs and `2 + 2 + 2 = 6`; {ignore}: a DIM 5 disc, crossed out.
> {blame}: a RED arrow from the dead end back to the first line, "never goes back". {code}: scene 3's
> third clause returns small, `if amt < c then change till amt` boxed, tag "skip only if too large";
> then `c :: change (c::till) (amt - c)` boxed, tag "fits: used, for good". It clears after {can}.
> {often}: the UK till returns, small; {uk}: its 1 disc glows GREEN, "1p always finishes the job";
> {fewest}: GREEN "fewest coins, for every amount" (checked against a fewest-coins count for every
> amount from 1 to 999: greedy matched it every time). {nothere}: the UK till clears.
> End on the stuck trace, its exception and the `2 + 2 + 2 = 6` card alone. Ch5's hook reopens on
> this shot (till 5 → 2, amount "6", the paid row), so report its layout.

[c4.greedy.1] {greedy} Our change function is greedy. It grabs the largest coin that fits, and never reconsiders. {pause} {new} Now take a different till, with only fives and twos, and make change for six. {five} Five fits, so we use it, and one is left. {stuck5} One is less than five, {stuck2} and less than two, so both coins go. {empty} The till is empty, with a penny still owed. {fail} So change raises its exception. No more coins. {pause}

[c4.greedy.2] {but} But change for six can be made. {twos} Two, plus two, plus two. {ignore} The only way is to ignore the five altogether. {blame} Greedy took the five, and never went back to try without it. {code} Look at the code again. It skips a coin only when the coin is too large. Once the five fits, it's used, and nothing ever undoes that choice. {pause=1.5} {can} So greedy change can fail, even when change is possible.

[c4.greedy.3] {often} Greedy algorithms are often effective. {uk} With British coins, this one can never get stuck, because the one pence coins can always finish the job. {fewest} And for every amount, it uses the fewest coins possible. {nothere} But with fives and twos, largest first leads to a dead end.

## Scene 7 · Recap (ch4_s7_recap)

> Recap: five short lines, one per mark, each with a small icon from its scene: {r1} the till chain,
> head glowing; {r2} the three clauses, tagged "success", "failure", "use it if it fits, else skip"; {r3} the GOLD `0`
> in `_, 0` and the YELLOW `(c::till)`; {r4} `_, 0 -> []`, "does nothing"; {r5} the stuck
> `change [5; 2] 6` trace in RED beside GREEN `2 + 2 + 2 = 6`.
> {next}: the recap clears to one node, "6, [5; 2]" (ch5's tree labels: amount, till); the outline
> of a branching tree grows from it, two edges labelled "use 5" and "skip 5", and a GOLD "?" where
> the answers will go. {paths}: more branches fan out. End card: hold ~8 s after the last word (music
> carries it).

[c4.recap.1] {recap} Let's recap. {r1} The till is a list in descending order, so the largest coin is its head. {r2} Change has three clauses, success at zero, an exception when the till runs out, and for the first coin, use it if it fits, or skip it if it's too large. {r3} A constant in a pattern matches only that value, and putting the coin back lets it be used again. {r4} The base case does nothing, which keeps the program simple. {r5} And greedy, largest first, can get stuck even when change exists. {pause}

[c4.recap.2] {next} Next time, instead of one answer, we'll find every way to make change. {paths} Then a dead end is just one path among many. {pause}
