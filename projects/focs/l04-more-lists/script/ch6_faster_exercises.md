# Chapter 6 · Faster, and exercises

Lecture 4 (More on Lists), part 6 of 7. Source: FoCS 2026-27 notes v1.8, p. 35 (§4.8) and p. 36 (exercises 4.1–4.6).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*; see LESSONS.md, "Write for the ear"). `{mark}` is a cue
point; `{pause}` / `{pause=1.5}` is a deliberate hold. `>` lines are the visual brief.

All code and replies below were run in OCaml 5.4.1 (`ocaml < file.ml`) and are quoted verbatim.

---

## Scene 1 · Hook (ch6_s1_hook)

> Title card: "More on Lists", "Foundations of Computer Science · Lecture 4", "Part 6 · Faster, and exercises".
> Last time, carried over from ch5: the all-ways `change` (In [72]) small on the left, verbatim (checked; reply `val change : int list -> int -> int list list = <fun>`): `let rec change till amt =` / `  match till, amt with` / `  | _       , 0   -> [ [] ]` / `  | []      , _   -> []` / `  | c::till , amt -> if amt < c then change till amt` / `                    else let rec allc = function` / `                            | [] -> []` / `                            | cs :: css -> (c::cs) :: allc css` / `                         in` / `                            allc (change (c::till) (amt - c)) @` / `                                  change till amt`.
> {code}: `allc` and the `@` get GOLD boxes. {copy}: each box sprouts a small GOLD "copies" tag, and a few cells duplicate out of it, again and again.
> {lecture3}: L3's two fixes, small and dim on the right: {length} `nlength` → `addlen` (tag "accumulator"), {reverse} `nrev` → `rev_app` (GOLD O(n²) → O(n)).
> {ask}: a GOLD "?" between the boxed `allc` / `@` and the word "accumulators". Leave it up; scene 2 answers it. {plan}: six small dim exercise cards, 4.1–4.6, slide in along the bottom.

[c6.hook.1] {title} Last time, we found every way to make change. {code} We used all-see to put a coin on the front of every solution, and append, the at sign, to join the two lists of answers. {copy} Both of those copy cells, over and over again. {pause}

[c6.hook.2] {lecture3} We've met this kind of waste before. {length} In lecture three, an accumulator made length iterative. {reverse} And building the answer with cons, instead of appending, made reverse fast. {ask} So can accumulators speed up making change too? {pause=1.5} {plan} That's the first half of this chapter. In the second half, I'll hand you six exercises to try on your own.

## Scene 2 · Two accumulators (ch6_s2_accs)

> Hero: the faster `change` (In [73]), verbatim, revealed clause by clause; `change` YELLOW, `match` / `if` / `then` / `else` BLUE, `[]` and `::` TEAL, `0` GOLD: `let rec change till amt chg chgs =` / `  match till, amt with` / `  | _       , 0   -> chg::chgs` / `  | []      , _   -> chgs` / `  | c::till , amt -> if amt < 0 then chgs` / `                     else change (c::till) (amt - c) (c::chg)` / `                                 (change till amt chg chgs)`.
> {chg} / {chgs}: `chg` and `chgs` light up in the header line, with labels that stay for the scene: "coins so far (this path)" and "solutions so far". To the right, a small picture: a box for the current path (ch4's GOLD coin discs) above a stack of finished boxes.
> {zero} / {record}: clause 1 lit; the path box drops onto the stack (`chg::chgs`). {empty} / {nothing}: clause 2 lit; the stack comes back exactly as it was.
> {lessthan}: `amt < 0` in RED, with a dim ghost of ch5's `amt < c` beside it. {late}: a two-node strip in ch5's tree style, "1, [5; 2]" → edge "use 5" → "−4, [5; 2]" in RED, which hands the stack back unchanged; {caught} label "caught one call later".
> {use}: `change (c::till) (amt - c) (c::chg)` boxed, edge label "use c"; {skip}: `(change till amt chg chgs)` boxed, label "skip c" (ch5's edge labels). {feed}: an arrow carries the skip box's result into the use call's last argument slot. {nojoin}: s1's `@`, dim, crosses out.
> {reply}: OCaml's reply, verbatim with its line break, types GREEN: `val change : int list -> int -> int list -> int list list -> int list list =` / `  <fun>`. The four argument types get small labels: till, amt, chg, chgs. {types}: the third `int list` and the fourth `int list list` glow GREEN, and a link joins the fourth to the result `int list list`.
> {call}: `change [2; 1] 4 [] []`, the two `[]`s TEAL, labelled "no coins yet" and "no solutions yet". This call carries into scene 3.

[c6.accs.1] {code} Here's the faster version, from the notes. {args} Alongside the till and the amount, it takes two new arguments, both accumulators. {chg} The third is called see-aitch-gee, short for change. It holds the coins chosen so far, on the current path. {chgs} The fourth, see-aitch-gee-ess, holds the solutions found so far. {pause}

[c6.accs.2] {zero} Look at the first clause. When the amount reaches zero, the coins so far add up exactly, so they make a solution. {record} The function conses them onto the solutions so far, and returns the lot. {empty} In the second clause, the till is empty but money is still owed, so this path has failed. {nothing} It returns the solutions so far, with nothing added. {pause}

[c6.accs.3] {lessthan} The third clause begins with a new test. It asks whether the amount is below zero, not whether it's below the coin. {overshoot} So this version uses a coin even when it's too big. {late} Say the amount is one, and the coin is five. It uses the five anyway, so the next call sees minus four, and just returns the solutions so far. {caught} The overshoot is only caught one call later. {pause}

[c6.accs.4] {use} Otherwise, it makes the same two choices as last time. Use the coin, by taking it off the amount and consing it onto the coins so far. {skip} Or skip the coin, which is the call in the last argument. {feed} Here's the trick. Whatever the skip call finds is passed in as the solutions so far for the use call. {pause} {nojoin} So nothing ever has to be appended.

[c6.accs.5] {reply} OCaml's reply now lists four arguments. {types} The coins so far are an int list, and the solutions so far are an int list list, the same type as the answer. {call} To start it off, you pass two empty lists. No coins chosen yet, and no solutions found yet. {pause}

## Scene 3 · Following the accumulators (ch6_s3_trace)

> ch5's tree for making 4 from `[2; 1]` (ch5_s6: nodes "amount, till", "use" edges left, "skip" edges right), with s2's call `change [2; 1] 4 [] []` above it. Each node gets a small TEAL tag with its `chg`; a "solutions so far" stack sits on the right, empty. ch5 collapsed "4, [1]" and "2, [1]" into single nodes; here expand both ones-only chains, because the `chg` tags grow along them.
> The `chg` values. Root "4, [2; 1]" `[]`. Skip side: "4, [1]" `[]` → "3, [1]" `[1]` → "2, [1]" `[1; 1]` → "1, [1]" `[1; 1; 1]` → "0, [1]" `[1; 1; 1; 1]`, with dead ends "4, []", "3, []", "2, []", "1, []". Use side: "2, [2; 1]" `[2]`; its skip: "2, [1]" `[2]` → "1, [1]" `[1; 2]` → "0, [1]" `[1; 1; 2]`, dead ends "2, []", "1, []"; its use: "0, [2; 1]" `[2; 2]`.
> {skipfirst}: the root's use edge stays dim, tagged "needs its last argument"; a YELLOW highlight takes the skip edge first. {ones}: the highlight walks down the skip side, the `chg` tag growing at the front each step. {found}: at "0, [1]" the box `[1; 1; 1; 1]` drops onto the stack. {dead}: each dead end flashes and passes the stack back unchanged.
> {handoff}: the stack slides up and into the root's use edge (TransformFromCopy), as its solutions so far. {usetwo}: "2, [2; 1]" lights with `[2]`. {again}: inside it, skip goes first again; `[1; 1; 2]` lands on the stack. {last}: use 2, and `[2; 2]` lands on top.
> {answer}: the reply `- : int list list = [[2; 2]; [1; 1; 2]; [1; 1; 1; 1]]` (checked); under it, dim, ch5's `- : int list list = [[2; 2]; [2; 1; 1]; [1; 1; 1; 1]]` (checked). {reversed}: `[1; 1; 2]` and `[2; 1; 1]` YELLOW. {why}: a small dim `rev_app` from L3, tag "consing reverses". {fine}: "1 + 1 + 2 = 2 + 1 + 1 = 4" in GOLD.

[c6.trace.1] {tree} Let's run it on last time's example, making four from twos and ones. {same} Here's the same tree of choices. {start} We start at the top, with no coins chosen and no solutions. {pause}

[c6.trace.2] {skipfirst} Now watch the order. Before the use call can start, its last argument has to be worked out, and that's the skip call. So the skip branch runs first. {ones} Skip the two, and make four from ones. Each step down conses another one onto the coins so far. {found} At zero, we have four ones. That's the first solution. {dead} The dead ends, where the till runs out, just hand the solutions back unchanged.

[c6.trace.3] {handoff} That list, with its one solution, goes back up, and becomes the solutions so far for the use branch. {usetwo} Use a two. Now the coins so far are a single two, with two left to make. {again} Inside, the same thing happens. The skip side runs first, and finds one, one, two. {last} Then use another two, reach zero, and record two, two. {pause}

[c6.trace.4] {answer} So the answer has three solutions, the same three as last time, in the same order. {reversed} But look at the middle one. Last time it was two, one, one, and now it's one, one, two. {why} The coins so far are built by consing, so the first coin chosen ends up last, as with rev-app in lecture three. {fine} Here, that's harmless. In any order, the coins add up to the same amount. {pause}

## Scene 4 · Faster, still slow, and stepwise refinement (ch6_s4_refine)

> Left: s1's In [72], dimmed, with `allc` and `@` still GOLD-boxed. Right: s2's In [73], with `c::chg` and `chgs` GREEN-boxed. {one}: an arrow "one `c::chg`" ← "many `allc` conses". {append}: the `@` crosses out, "`chgs` instead".
> {faster}: two GOLD bars, "all ways" and "faster", the second about two and a half times shorter; caption, the notes' words, "several times faster". {measured}: small label "measured in the OCaml 5.4.1 toplevel" (99p, 300 runs: 2.51×; 199p, 20 runs: 2.46×).
> {count}: `List.length (change [50; 20; 10; 5; 2; 1] 99 [] [])` → `- : int = 4366` (checked), 4366 in GOLD. {every}: tiny solution boxes pour in and fill the background.
> {three}: clear to three steps, left to right, numbered 1 2 3: {simple} "greedy" with `val change : int list -> int -> int list = <fun>` and a RED "can fail"; {all} "every way" with `val change : int list -> int -> int list list = <fun>`; {fast} "faster", tag "two accumulators". {name}: header "stepwise refinement".
> {recipe}: under the steps, three short lines appear on {begin}, {add}, {last}: "start very simple", "add requirements one at a time", "efficiency last of all". {discard}: step 1 dims and slides aside; {learned}: tag "it taught us the task".

[c6.refine.1] {compare} So what did the two accumulators buy us? {cons} In the old version, every time a coin was used, all-see consed it onto every solution that came back. {one} Here, a single cons onto the coins so far replaces many of those. {append} And since the solutions so far are passed along, there's no append at all. {pause}

[c6.refine.2] {faster} The notes say this version runs several times faster. {measured} When we timed both versions, the new one was about two and a half times faster. {still} But it's still extremely slow, for a simple reason. The number of solutions grows rapidly with the amount. {count} With coins of fifty, twenty, ten, five, two and one pence, there are four thousand, three hundred and sixty-six ways to make ninety-nine pence. {pause} {every} And every one of them has to be built.

[c6.refine.3] {three} Now step back, and look at our three change functions. {simple} First, a greedy one. It was simple, but it could fail. {all} Then one that finds every way. {fast} Then the same thing, faster. {name} Improving simple code, step by step like this, is called stepwise refinement. {pause}

[c6.refine.4] {recipe} The recipe is short. {begin} Begin with a very simple program. {add} Add the requirements one at a time. {last} And add efficiency last of all. {discard} Sometimes the simple version has to be thrown away. {learned} Even then, writing it taught you about the task. {pause}

## Scene 5 · Exercises 4.1 to 4.3 (ch6_s5_hints1)

> "Exercises" header; six dim cards 4.1–4.6 in a row, and a small note "solutions: bonus chapter". Copy L3's card kit (BigCard, HeroCard, pause_tag, from `projects/focs/l03-lists/scenes/ch5_s6_sumlast.py`) into this scene's file; s6 and ch7 import it from here. The card text below is reused verbatim in ch7.
> Each card in turn grows to the hero position, and shrinks back when done: the task in a sentence, its example in Code, a GOLD "?" wherever an answer would go (never a solution). The hint fades in beneath. On each {pause=2}, the screen holds still with the small "pause and try it" label.
> Card 4.1 "Set union": "Sets are lists with no repeats. Using member, code set union." Example `union [4; 7; 1] [6; 4; 7]` ⇒ `[1; 6; 4; 7]`, tag "any order" (the notes' example; checked). Hint: ch2's reply `val member : 'a -> 'a list -> bool = <fun>`, dim; {walk}: a YELLOW marker steps along `[4; 7; 1]` while `[6; 4; 7]` stays whole, a GOLD "?" over each element it visits.
> Card 4.2 "Split by sign": "Return two lists: the non-negative numbers, and the negative ones." Example `[3; -1; 0; -5; 2]` ⇒ `([3; 0; 2], [-1; -5])` (checked), target type `int list -> int list * int list` in GREEN. Hint: ch3's unzip (In [65]), dim: `let rec unzip = function` / ` | [] -> ([], [])` / ` | (x, y)::pairs ->` / `     let xs, ys = unzip pairs in` / `     (x::xs, y::ys)`, with the `let xs, ys = unzip pairs in` line YELLOW. {zero}: the example's 0 in GOLD with a small "?".
> Card 4.3 "Another zip": In [74] verbatim, `let rec zip xs ys =` / `  match xs, ys with` / `  | (x::xs, y::ys) -> (x, y) :: zip xs ys` / `  | ([], [])   -> []`, with `([], [])` YELLOW where ch3's `| _ -> []` was; reply `val zip : 'a list -> 'b list -> ('a * 'b) list = <fun>`, and the question "How does it differ?".
> Hint for 4.3: {uneven} ch3's phone book, `zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47]` and `zip ["Amy"; "Bob"; "Cleo"] [21; 35]`, each ⇒ GOLD "?". {warning}: the last two lines of the warning OCaml prints for In [74], RED: `Warning 8 [partial-match]: this pattern-matching is not exhaustive.` / `  Here is an example of a case that is not matched: (x::xs, [])`, with `(x::xs, [])` covered by a GOLD "?".

[c6.ex.1] {turn} Now it's your turn. {six} The notes end with six exercises. {plan} As in lecture three, I'll state each one, give you a hint, and then pause, so you can stop the video and try it. {bonus} The worked solutions are in the bonus chapter, for after you've had a go.

[c6.ex.2] {union} Exercise four point one. {sets} You can represent a set as a list with no repeated items. {task} Using member, from chapter two, write a function for set union. {example} Take the lists four, seven, one, and six, four, seven. Their union should be one, six, four, seven. {order} Any order is fine. {pause}

[c6.ex.3] {hint} Here's the hint. {walk} Walk down the first list, one element at a time. {keep} Keep only the elements that are missing from the second list. {try} Pause the video, and try it. {pause=2}

[c6.ex.4] {signs} Exercise four point two. {task} Write a function that takes a list of integers and returns two lists. {first} The first holds the numbers that are zero or more. {second} The second holds the negative ones. {example} So three, minus one, zero, minus five, two, splits into three, zero, two, and minus one, minus five. {pause}

[c6.ex.5] {hint} The hint is in chapter three. {two} You're building two results at once, just as unzip did. {let} So remember how unzip used a let, to take its pair of results apart. {zero} And watch where zero goes. {try} Pause, and try it. {pause=2}

[c6.ex.6] {zip} Exercise four point three. {code} Here's another version of the zip function. {clause} Where chapter three's version had a wildcard, this one has a clause for two empty lists. {type} Its type is exactly the same. {task} So how does it behave differently? {pause}

[c6.ex.7] {hint} Here's the hint. {uneven} Try it on two lists of the same length, and then on lists of different lengths. {warning} Also, when you type it in, OCaml prints a warning. Read it carefully, because it even gives you an example. {try} Pause, and think it through. {pause=2}

## Scene 6 · Exercises 4.4 to 4.6 (ch6_s6_hints2)

> Same strip and card kit (imported from s5); cards 4.4–4.6, same rules: GOLD "?" for answers, never a solution, "pause and try it" on each {pause=2}.
> Card 4.4 "Hidden assumptions": "What do the change functions assume about till and amt? What could happen if those assumptions fail?" The three headers stacked, `till` and `amt` YELLOW: `let rec change till amt =` (greedy), `let rec change till amt =` (every way), `let rec change till amt chg chgs =` (faster).
> Hint for 4.4: four chips, one per beat, each with a GOLD "?": {zero} "a coin worth 0", {negative} "an amount below 0", {order} "coins smallest first", {twice} "the same coin twice". {careful}: the first chip gets a RED outline, "think before you run it". Show no results (they belong to ch7; checked: with a coin of 0, greedy and every-way overflow the stack and the faster version runs on past our timeout).
> Card 4.5 "Counting the ways": "Two coin values: show there are O(n) ways to make change for n (ignoring order). Three values? Four? …" Hint: ch4's GOLD coin discs 5 and 2, and an amount n; {fix}: a counter "how many 5s?" ticking 0, 1, 2, …; {rest}: "the rest in 2s" with a GOLD "?"; {build}: a third disc, 1, joins, with an arrow back to the two-coin picture.
> Card 4.6 "What the types force": `val f : 'a * 'b -> 'b * 'a` and `val g : 'a -> 'a list` (`'a`, `'b` PINK); {calls} `f (1, true)` ⇒ GOLD "?" and `g 0` ⇒ GOLD "?".
> Hint for 4.6: L3's `let id x = x` → `val id : 'a -> 'a = <fun>` (checked), dim. {nothing}: the PINK `'a` pulses, caption "knows nothing about 'a". {where}: dashed arrows from each part of each result back toward the arguments, every result slot still a GOLD "?" (no answers filled in).

[c6.ex.8] {assume} Exercise four point four. {task} What do our making change functions assume about the till and the amount? {happen} And what could happen if those assumptions were broken? {pause}

[c6.ex.9] {hint} Here's the hint. Try some odd inputs, and ask what each version does. {zero} A coin worth zero. {negative} An amount below zero. {order} Coins in the wrong order, smallest first. {twice} And the same coin, listed twice. {careful} With the coin of zero, think before you run it. {try} Pause, and try it. {pause=2}

[c6.ex.10] {count} Exercise four point five. {task} Suppose there are just two coin values. Show that for an amount en, the number of ways to make change is big O of en. {order} Here, two solutions with the same coins in a different order count as one. {more} Then ask the same question for three coin values, or four, or more. {pause}

[c6.ex.11] {hint} Here's the hint. {fix} With two coins, first decide how many of the larger coin you'll use. {rest} Once that's fixed, how many ways are left for the smaller one? {build} For more coins, build on the case you just solved. {try} Pause, and work it out. {pause=2}

[c6.ex.12] {types} The last exercise, four point six, is about types. {fg} We know nothing about two functions, eff and gee, except their types. {ftype} The function eff takes a pair of an alpha and a beta, and returns a pair of a beta and an alpha. {gtype} The function gee takes an alpha, and returns an alpha list. {calls} Suppose we apply eff to the pair one and true, and gee to zero, and both return. {ask} What will the results be, and why? {pause}

[c6.ex.13] {hint} The hint goes back to eye-dee, in lecture three. {nothing} A function whose type says alpha knows nothing about alpha. {invent} It has no way to make up a value of that type. It can only use the ones you give it. {where} So for each part of each result, ask where it could have come from. {try} Pause, and think it through. {pause=2}

## Scene 7 · The whole lecture (ch6_s7_recap)

> Clear the cards. A recap column, one short line per beat, each with a small icon from its chapter.
> {takedrop}: ch1's chain 3 → 5 → 9 → 4 → 7 → [] with the GOLD cut, "take copies, drop skips", GOLD "O(i)". {search}: a GOLD pointer stepping along the same chain, "linear search: O(n)". {equal}: `=` in GREEN beside a RED "functions" chip.
> {zip}: ch3's mirror, the zip and unzip types facing each other. {pattern}: `let xs, ys = unzip pairs in`, YELLOW. {change}: three GOLD coin discs labelled "greedy", "every way", "faster". {refine}: s4's three numbered steps, small, "stepwise refinement".
> {next}: clear to "Next lecture: Sorting". {fast}: a sorted row with a halving bracket, GOLD "O(log n)". {merge}: the ch1 chain splits under `take` and `drop` into two halves, labelled "merge sort".
> {bonus}: the six exercise cards in a row, "Solutions: bonus chapter". After the last word, the end card holds for about 8 s while the music carries it.

[c6.recap.1] {recap} That's the end of lecture four, so let's look back. {takedrop} Take copies the front of a list, and drop skips over it. Both need time in proportion to how far they go, but only drop runs in constant space. {search} Searching a list means looking at one element at a time, so it costs big O of en. {equal} Polymorphic equality works on numbers, strings, and lists or pairs of them, but comparing functions raises an exception. {pause}

[c6.recap.2] {zip} Zip pairs up two lists, and unzip splits the pairs apart again. {pattern} A let can match a pattern, and name every part of it at once. {change} We made change three ways. Greedy, which can get stuck. Then every way. Then every way, faster, with two accumulators. {refine} And building it up like that is stepwise refinement. Start simple, and add efficiency last. {pause}

[c6.recap.3] {next} Next lecture is about sorting. {fast} A sorted collection can be searched in big O of log en. {merge} And one way to sort, called merge sort, splits its list in two with take and drop. {bonus} But first, try the six exercises. When you're ready, the bonus chapter walks through every solution. {pause} {bye} See you there.
