# Chapter 6 · Solutions to the exercises

Lecture 3 (Lists), bonus chapter (optional, for after the exercises). Source: FoCS 2026-27 notes,
p. 29 (Exercises 3.1–3.5), drawing on pp. 21–29.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*; see LESSONS.md, "Write for the ear"). `{mark}` is a cue
point; `{pause}` / `{pause=1.5}` is a deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Spoiler warning (ch6_s1_intro)

> Title card: "Lists", "Foundations of Computer Science · Lecture 3", "Bonus: solutions to the
> exercises". Then a GOLD "SPOILERS AHEAD" banner with a big pause icon (‖), held through the pause.
> The five exercises as five cards in a row, filling the frame: "3.1 sum", "3.2 last",
> "3.3 even positions", "3.4 two strange types", "3.5 tails". On {ritual}, the first card shows
> the routine every exercise will follow, as three small steps under it: "pause ‖", "solve",
> "trace and cost". On {wrong}, a RED ✗ card slides in beside it: "tempting wrong answers".
> Each later scene opens with its card enlarged from this row (TransformFromCopy) plus the ‖ icon.
> All OCaml in this chapter was checked in OCaml 5.4.1. The replies quoted below are the exact
> toplevel output for the code as shown.

[c6.intro.1] {title} This bonus chapter for lecture three has solutions to the five exercises at the end of the notes. {pause} {warn} Everything from here on is a spoiler. If you haven't tried the exercises yet, stop the video now, and have a go.

[c6.intro.2] {cards} We'll take them in order. {ritual} Each exercise starts with the question and a moment to pause. Then we solve it, trace it, and work out its cost. {wrong} We'll also look at tempting wrong answers, which teach as much as right ones.

## Scene 2 · Exercise 3.1: summing a list (ch6_s2_sum)

> Card: "Exercise 3.1 · Sum a list's elements. Recursive first, then iterative. Comment on the
> improvement in efficiency." + ‖. Hold, still, through the pause.
> Recursive version as Code (hero, upper left), and its reply in GREEN:
> `let rec nsum = function | [] -> 0 | x :: xs -> x + nsum xs` (three lines)
> → `val nsum : int list -> int = <fun>`. Beside it, dimmed, the lecture's
> `val nlength : 'a list -> int`: the PINK `'a` against nsum's GREEN `int` on {notpoly}.
> Trace (P11/P13), each line born from a copy of the one above:
> `nsum [3; 5; 9]` ⇒ `3 + nsum [5; 9]` ⇒ `3 + (5 + nsum [9])` ⇒ `3 + (5 + (9 + nsum []))`.
> On {pending} the waiting `3 +`, `5 +`, `9 +` turn GOLD and slide into a column on the right,
> stacked like plates, labelled "pending additions". On {unwind} they pop from the top:
> `3 + (5 + (9 + 0))` ⇒ `3 + (5 + 9)` ⇒ `3 + 14` ⇒ `17`. Reply: `- : int = 17`.
> Cost tags under nsum in GOLD: "time O(n)", "space O(n)".
> On {slip}, a RED-boxed wrong version: `| x :: xs -> x + addsum total xs`. Reply
> `val addsum : int -> int list -> int` (it type-checks, and returns 17), but the GOLD stack
> column reappears beside it. (Verified: with a 1 MB stack limit, `OCAMLRUNPARAM=l=128k`, this
> version and `nsum` raise Stack_overflow on a million-element list, while the right `addsum`
> doesn't. OCaml 5's default stack is 1 GiB, so don't put a specific crash size on screen.)
> Iterative half (from {iter}): keep the nsum code and its GOLD cost tags dimmed to ~0.4 at
> the top left; the stack column and the wrong version fade out.
> Code: `let rec addsum total = function | [] -> total | x :: xs -> addsum (total + x) xs`
> → `val addsum : int -> int list -> int = <fun>`; then `let sum xs = addsum 0 xs`
> → `val sum : int list -> int = <fun>`; `sum [3; 5; 9]` → `- : int = 17`.
> Highlight `total` in GOLD wherever it appears (it's the running total, like `summing`'s in
> lecture 2 and `addlen`'s n).
> Trace (P24: first step slow, the rest quicker), on the same list, with the total in a GOLD box
> riding above the current cell of a ConsChain 3 → 5 → 9 → []:
> `addsum 0 [3; 5; 9]` ⇒ `addsum 3 [5; 9]` ⇒ `addsum 8 [9]` ⇒ `addsum 17 []` ⇒ `17`.
> Each line REPLACES the previous one in place (ReplacementTransform), so the expression never
> grows: that is the "nothing waits" picture. No stack column appears.
> Comparison table, GOLD costs, one row per beat: nsum, time O(n), space O(n); sum, time O(n),
> space O(1). (Same as the lecture 2 table for nsum / summing.)

[c6.sum.1] {card} Exercise three point one. Code a recursive function to sum the elements of a list, then an iterative version, and comment on the improvement in efficiency. {pause} {stop} Pause here if you want to try it. {pause=1.5}

[c6.sum.2] {base} The recursive version has the same shape as en-length. The sum of nil is zero. {step} And the sum of a head, ex, consed onto exes, is ex plus the sum of exes. {name} As in the lecture, we'll call it en-sum, en for naive.

[c6.sum.3] {type} Its type is int list to int. {pause} {notpoly} Unlike length, it isn't polymorphic, because plus only works on integers.

[c6.sum.4] {trace} Let's trace it on three, five, nine. {s1} It becomes three plus en-sum of five, nine. {s2} Then three plus five plus en-sum of nine. {s3} Then three plus five plus nine plus en-sum of nil. {pause} {pending} Look at those additions, waiting. None can happen until we reach nil, so they all sit on the stack. {unwind} Then they finally happen, {total} giving seventeen.

[c6.sum.5] {cost} So en-sum takes big O of en time, and also big O of en space, for that stack of pending additions. {overflow} On a long enough list, it can run out of stack. {slip} A common slip is to add an accumulator, but still write ex plus add-sum of the rest. The addition still waits, and the stack is back.

[c6.sum.6] {iter} The cure, as for length, is an accumulator. {addsum} Add-sum carries a running total. {acc_base} On the empty list, it returns the total. {acc_step} Otherwise, it adds the head to the total, and carries on with the tail. {wrap} Sum starts it off from zero.

[c6.sum.7] {trace2} On the same list, {t1} the total starts at zero, with three, five, nine to go. {t2} Then three, with five, nine to go. {t3} Then eight, with nine to go. {t4} Then seventeen, with nothing left. {pause} {flat} Nothing waits. Each call replaces the call before it.

[c6.sum.8] {compare} So, the comment on efficiency. {time} Both versions take big O of en time, since each visits every element. {gain} The gain is in space, from big O of en down to big O of one, because the calls no longer nest.

## Scene 3 · Exercise 3.2: the last element (ch6_s3_last)

> Card: "Exercise 3.2 · Return the last element of a non-empty list. How efficiently can this
> be done?" + ‖. Hold through the pause.
> Code (hero): `let rec last = function | [x] -> x | x :: xs -> last xs`. The toplevel reply,
> shown in full, the warning in YELLOW (attention, not an error), the type in GREEN:
> `Warning 8 [partial-match]: this pattern-matching is not exhaustive.`
> `Here is an example of a case that is not matched: []`
> `val last : 'a list -> 'a = <fun>`
> Calls: `last [3; 5; 9]` → `- : int = 9`; `last ["only"]` → `- : string = "only"`;
> `last []` → `Exception: Match_failure ("//toplevel//", 1, 15).` in RED. Beside it, dimmed,
> the lecture's `hd`, which has the same warning.
> Trace on a ConsChain 3 → 5 → 9 → []: a YELLOW marker steps cell to cell (P24, quicker each
> step) while the call rewrites in place: `last [3; 5; 9]` ⇒ `last [5; 9]` ⇒ `last [9]` ⇒ `9`.
> On {s3} the `[x]` clause flashes.
> Wrong attempt 1 ({swap}), the clauses swapped: `| x :: xs -> last xs` then `| [x] -> x`.
> Hold on the question. On {catch}, show `[9]` = `9 :: []`, with `xs = []` in TEAL, matching
> the first clause. Reply: `Warning 11 [redundant-case]: this match case is unused.` under
> `[x] -> x`, and `last [3; 5; 9]` → `Exception: Match_failure ("//toplevel//", 1, 15).`
> Wrong attempt 2 ({zero}): add `| [] -> 0` → `val last : int list -> int = <fun>`. The PINK
> `'a` turns GREEN `int`; RED ✗ on "works on any list".
> Cost: the marker's walk replayed as a long linear sweep (cost felt as screen time),
> "time O(n)" in GOLD, "space O(1)". On {rev}: `List.hd (List.rev [3; 5; 9])` → `- : int = 9`,
> with a whole reversed copy 9 → 5 → 3 being built: "time O(n)", "space O(n)".

[c6.last.1] {card} Exercise three point two. Code a function to return the last element of a non-empty list. How efficiently can this be done? {pause} {stop} Pause now, if you'd like a go. {pause=1.5}

[c6.last.2] {shapes} Which lists have an obvious last element? {pause} {single} If the list holds a single element, ex, the answer is ex. {longer} Any longer list is a head consed onto exes, and its last element is the last element of exes.

[c6.last.3] {warning} OCaml accepts it with a warning, because the empty list isn't covered. {fine} That's fine, since the exercise promised a non-empty list. Like the head function, it raises an exception on nil. {type} Its type is alpha list to alpha, so it works on lists of anything.

[c6.last.4] {trace} On three, five, nine, it steps along, {s1} to five, nine, {s2} then to nine, {s3} which matches the single element clause, so the answer is nine.

[c6.last.5] {swap} Here's a classic mistake. Write the two clauses the other way round. {ask} What goes wrong? {pause=1.5} {catch} A list of just nine is also a head consed onto a tail, the tail being nil. So the general clause catches it, and the walk carries on to nil, where nothing matches. {unused} OCaml even warns that the single element clause is unused. {order} Order matters. Put the most specific pattern first.

[c6.last.6] {zero} Another temptation is to say that the last element of nil is zero. {mono} But then the type becomes int list to int, and on nil it returns a made-up answer.

[c6.last.7] {cost} So how efficient is it? {walk} There's no shortcut to the end of a list, so it takes big O of en time. {space} But the space is only big O of one, because the recursive call is the last thing that happens. {pause} {already} It's already iterative, with no accumulator needed. {rev} Reversing the list and taking its head also works, but the reversed copy costs big O of en space.

## Scene 4 · Exercise 3.3: the even positions (ch6_s4_evens)

> Card: "Exercise 3.3 · Return the even-numbered elements: [a; b; c; d] ⇒ [b; d]" + ‖.
> Positions: [10; 20; 30; 40; 50] as boxes, hero width, DIM position labels 1–5 underneath.
> On {values} every value glows GREEN ("even number"), then positions 2 and 4 turn YELLOW and
> the rest go RED at half opacity; 20 and 40 slide together into [20; 40] (the Wordle filter move).
> Code: `let rec evens = function | [] -> [] | [x] -> [] | x :: y :: xs -> y :: evens xs`
> → `val evens : 'a list -> 'a list = <fun>`; `evens ['a'; 'b'; 'c'; 'd']` →
> `- : char list = ['b'; 'd']` (the exercise's own example). One clause lights up per beat
> ({empty}, {single}, {pair}); on {pair} a bracket spans two cells of a ConsChain at once.
> Trace: `evens [10; 20; 30; 40; 50]` ⇒ `20 :: evens [30; 40; 50]` ⇒ `20 :: 40 :: evens [50]`
> ⇒ `20 :: 40 :: []` = `[20; 40]`; reply `- : int list = [20; 40]`. The bracket hops two cells
> per step; at [50] it can't span two, and the `[x]` clause flashes.
> Wrong attempt ({forget}): the `[x]` clause deleted. Reply:
> `Warning 8 [partial-match]: this pattern-matching is not exhaustive.`
> `Here is an example of a case that is not matched: x::[]` (OCaml 5.4.1's exact wording).
> `evens [10; 20; 30; 40]` → `- : int list = [20; 40]` (GREEN, looks fine);
> `evens [10; 20; 30]` → `Exception: Match_failure ("//toplevel//", 1, 16).` (RED).
> Cost: "time O(n)" GOLD. On {space}, the pending `20 ::`, `40 ::` stack up in GOLD like
> append's (the sum scene's stack column, reused): "space O(n)". On {rev}, a ghost accumulator version
> producing [40; 20], then needing a reverse: RED ✗ "no gain". The lecture's line
> "Never add an accumulator merely out of habit." as a quote card.

[c6.evens.1] {card} Exercise three point three. Code a function that returns the even-numbered elements of a list. Given four letters, it should keep the second and the fourth. {pause} {stop} Pause, and try it. {pause=1.5}

[c6.evens.2] {careful} Be clear what's asked. {positions} Even-numbered means even positions, the second, the fourth, and so on, not even values. {values} In ten, twenty, thirty, forty, fifty, every value is even, but we keep only twenty and forty.

[c6.evens.3] {shapes} This time, a list has three shapes. {empty} Empty gives empty. {single} A single element gives empty too, with no second element to keep. {pair} And for two or more, the pattern ex, cons why, cons exes, grabs two at once. {keep} We keep why, drop ex, and carry on with exes.

[c6.evens.4] {trace} On ten, twenty, thirty, forty, fifty, {s1} we keep twenty, and carry on with thirty, forty, fifty. {s2} We keep forty, and carry on with fifty. {s3} A single element gives nil, {result} so the answer is twenty, forty. {pause}

[c6.evens.5] {forget} The common mistake is to forget the single element case. {warn} OCaml warns you, with an example it can't match, a list of just one element. {even} On even lengths, the function seems fine. {odd} But on ten, twenty, thirty, it's left with the thirty on its own, and fails. {pause} {lesson} So test odd and even lengths, and read the warnings.

[c6.evens.6] {cost} The time is big O of en. {space} But like append, it builds a chain of pending conses, so it needs big O of en space. {acc} Could an accumulator fix that? {pause} {rev} It would build the answer backwards, needing a reverse at the end, and the answer itself takes big O of en space anyway. {habit} As the notes say, never add an accumulator merely out of habit.

## Scene 5 · Exercise 3.4: two strange types (ch6_s5_types)

> Card: "Exercise 3.4 · Why do these types make logical sense, and prevent run-time type errors?"
> `let id x = x` → `val id : 'a -> 'a = <fun>`
> `let rec loop x = loop x` → `val loop : 'a -> 'b = <fun>`
> and the two test expressions `id [id [id 0]]`, `loop true / loop 3` ("/ is integer division")
> + ‖. All `'a`/`'b` PINK throughout.
> id as a machine (a box labelled `id`): on {id_meaning} "for every type α: α in, α out".
> On {only} a GOLD "?" appears inside the box where a new α would have to come from, then
> crossed out: the only α in reach is the input. On {except} a faint loop arrow, "or never return".
> `id [id [id 0]]` built inside out (P11), each `id` tagged with its own α in GREEN:
> `id 0` α = int; `id [id 0]` α = int list; outer `id` α = int list list.
> Reply: `- : int list list = [[0]]`.
> Contrast ({bad}): `id true / id 3` → RED, OCaml's exact reply:
> `Error: This expression has type bool but an expression was expected of type int`
> (under `id true`). Rejected before it runs.
> loop: `loop : α → β`; underline the body `loop x`, which has type β, the same β, so nothing
> fixes it ({infer}). On {free} the PINK `'b` pulses (a flash that removes itself).
> On {never}, the call `loop true` → `loop true` → `loop true` … on a circular arrow, forever.
> `loop true / loop 3`: each `loop` gets β = int (GREEN tags), and `/ : int -> int -> int`, so it
> type-checks: `fun () -> loop true / loop 3` → `- : unit -> int = <fun>`. Then the toplevel
> prompt `# loop true / loop 3;;` with no reply ever: a blinking cursor and a ticking clock (true,
> it runs forever and prints nothing). On {contrast2} a ghost `'a -> 'a` loop:
> `let rec loop2 (x : 'a) : 'a = loop2 x` → the same RED "type bool … expected of type int" error.
> Quote card: "Well-typed programs cannot go wrong." Robin Milner, 1978 (A Theory of Type
> Polymorphism in Programming).

[c6.types.1] {card} Exercise three point four. {id} The identity function, eye-dee, returns its argument, and has type alpha to alpha. {loop} Loop calls itself forever, and has type alpha to beta. {question} Why do these types make sense? And why can't they cause type errors at run time, even in strange expressions like these? {pause} {stop} Pause, and think it through. {pause=1.5}

[c6.types.2] {id_meaning} Read alpha to alpha as a promise. Whatever alpha is, give the function an alpha, and you get an alpha back. {pause} {only} But it knows nothing about alpha, so it can't make up a new alpha. All it can hand back is the value you gave it. {except} Or it could never return at all. Hold that thought.

[c6.types.3] {nested} Now take eye-dee of a list, of eye-dee of a list, of eye-dee of zero. Work from the inside out. {inner} The innermost eye-dee is given an int. {middle} The next, an int list. {outer} And the outer one, an int list list. {pause} {three} The same function, at three different types, because each use gets its own fresh alpha. {fresh} Every promise is kept, and the result is a list of lists holding zero.

[c6.types.4] {contrast} Compare eye-dee of true, divided by eye-dee of three. {bad} That's rejected before it runs, because eye-dee of true is a bool, and you can't divide a bool.

[c6.types.5] {strange} Now, alpha to beta. {where} Where does the beta come from? {pause} {infer} The definition says loop of ex is loop of ex, so the result is whatever loop returns, and nothing pins that down. {free} So the result type stays free. That's beta.

[c6.types.6] {absurd} As a promise, it sounds absurd. Give loop anything, and it returns any type you like. {question} How can that be safe? {pause} {never} Because loop never returns. {vacuous} A promise about the result can't be broken if the result never arrives.

[c6.types.7] {division} So look at loop of true, divided by loop of three. {checks} Division needs integers, and loop can promise integers, so OCaml accepts it. {run} But whichever loop starts first never finishes, so the division never happens. {pause} {safe} No bool ever turns up where an integer was expected. It runs forever, but it never goes wrong. {contrast2} Give loop the type alpha to alpha, and this would be rejected.

[c6.types.8] {guarantee} That's the guarantee. Types are checked before the program runs, so no value can ever turn up with the wrong type. {quote} Robin Milner, who created ML, OCaml's ancestor, put it as a slogan. Well-typed programs cannot go wrong. {pause} {caveat} They might run forever, or raise an exception, but they never mix up their types.

## Scene 6 · Exercise 3.5: tails (ch6_s6_tails)

> Card: "Exercise 3.5 · tails [1; 2; 3] ⇒ [[1; 2; 3]; [2; 3]; [3]; []]" + ‖.
> On {notempty}: point at the final `[]` in the example's answer.
> Code (hero): `let rec tails l = match l with | [] -> [[]] | x :: xs -> l :: tails xs`
> → `val tails : 'a list -> 'a list list = <fun>`; the whole-list `l` in YELLOW, matching the
> `l ::` in the result. `tails [1; 2; 3]` → `- : int list list = [[1; 2; 3]; [2; 3]; [3]; []]`;
> `tails []` → `- : 'a list list = [[]]`.
> Trace: `tails [1; 2; 3]` ⇒ `[1; 2; 3] :: tails [2; 3]` ⇒ `[1; 2; 3] :: [2; 3] :: tails [3]`
> ⇒ `… :: [3] :: tails []` ⇒ `… :: [3] :: [[]]`. Four tails counted on {four}.
> Sharing ({cells}): a ConsChain 1 → 2 → 3 → [] across the frame; above it, a new outer spine
> of four BLUE cells, whose value arrows drop into the SAME chain at cell 1, cell 2, cell 3 and
> nil (TEAL, "shared"). The tempting picture first ({ask}): three separate copies, six number
> boxes, crossed out. Then counters: "new cells: 4" (GOLD), not "copied: 6". (Verified with
> physical equality: the second element of `tails l` is `==` `List.tl l`.)
> Wrong 1 ({nilbase}): `| [] -> []` → same type `'a list -> 'a list list`, but
> `- : int list list = [[1; 2; 3]; [2; 3]; [3]]`, the missing `[]` as a RED gap.
> Wrong 2 ({append}): `let rec addtails acc l = match l with | [] -> acc @ [[]] | x :: xs ->
> addtails (acc @ [l]) xs` → `val addtails : 'a list list -> 'a list -> 'a list list`,
> `addtails [] [1; 2; 3]` gives the right answer, but each `@` copies acc: "1 + 2 + … + n" in
> GOLD → O(n²), beside a dimmed `nrev`.
> Cost: "time O(n)", "space O(n)", "a new cell per tail".

[c6.tails.1] {card} Finally, exercise three point five. Code a function, tails, returning the list of all the tails of its argument. {example} Given the list one, two, three, it should return one, two, three, then two, three, then three, then nil. {pause} {stop} Pause here, for the last time. {pause=1.5}

[c6.tails.2] {sense} Here, a tail means any suffix, from the whole list down to nil. {base} So what are the tails of nil? {pause} {notempty} The answer always ends with nil, so the tails of nil must be a list containing nil. {step} For a non-empty list, ell, the tails are ell itself, consed onto the tails of exes. {match} Using match gives us a name, ell, for the whole list.

[c6.tails.3] {trace} On one, two, three, {s1} the first tail is the whole list, consed onto the tails of two, three. {s2} Then comes two, three, {s3} then three, {s4} and finally the tails of nil, the list containing nil. {four} Four tails, for three elements.

[c6.tails.4] {cells} Now look at it in memory. {looks} The answer seems to hold six numbers. {ask} So does it copy the list, again and again? {pause} {share} No. Each tail is the original list, from some cell onwards, so the answer points into the same chain. {spine} The only new cells are the four in the outer list. {immut} As we saw in chapter one, that sharing is safe because lists never change.

[c6.tails.5] {wrong} There are two tempting mistakes. {nilbase} First, making the tails of nil just nil. The type is the same, so OCaml can't help, but the empty tail goes missing. {append} Second, using append to add each tail on the end of an accumulator. Each append copies the accumulator, so that's one, plus two, plus three, and so on, which is big O of en squared, just like en-rev.

[c6.tails.6] {cost} It makes a call per element, plus a call for nil, so it takes big O of en time. {space} It builds a new cell per tail, so its space is big O of en too. {pause} {close} It isn't iterative, but there's nothing to gain, since the answer itself is that big.

## Scene 7 · Recap (ch6_s7_recap)

> Five rows, one per beat, each with the exercise number, the function name in YELLOW and its
> GOLD costs: 3.1 `nsum` O(n) / O(n) → `sum` O(n) / O(1) · 3.2 `last` O(n) / O(1) ·
> 3.3 `evens` O(n) / O(n) · 3.4 `'a -> 'a`, `'a -> 'b` in PINK · 3.5 `tails` O(n) / O(n),
> "shared" in TEAL. Hold, then end card.

[c6.recap.1] {recap} Let's recap. {r1} For sum, an accumulator cut the space from big O of en to big O of one. {r2} Last is already iterative, but it can't avoid the walk to the end. {r3} The even positions need three clauses, and an accumulator wouldn't help. {r4} Alpha to alpha forces a function to return its argument, and alpha to beta is safe because loop never returns. {r5} And tails is only big O of en, because every tail is shared. {pause} {end} Well done. See you in the next lecture.
