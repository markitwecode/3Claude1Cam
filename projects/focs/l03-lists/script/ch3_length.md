# Chapter 3 · Length, recursion and accumulators

Lecture 3 (Lists), part 3 of 5. Source: FoCS 2026-27 notes, pp. 24–25 (§3.3–3.4), plus Lecture 2's
`nsum`, pp. 13–14.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*; see LESSONS.md, "Write for the ear"). `{mark}` is a cue
point; `{pause}` / `{pause=1.5}` is a deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch3_s1_hook)

> Title card: "Lists", "Foundations of Computer Science · Lecture 3", "Part 3: length, recursion
> and accumulators". Then a big ConsChain 5 → 6 → 7 → [] (≈ 9 units wide), GOLD "length = ?" under it.
> "At a glance": the three values light up together, then everything dims except the first cell.
> The two patterns from ch2 drop in above it as a fork, `[]` | `x :: xs`, with a YELLOW "?" at the fork.
> Then two empty slots side by side, "version 1" and "version 2": under version 1 a small GOLD bar
> that keeps growing; under version 2 one that stays short. No code yet.

[c3.hook.1] {title} This is part three of our lecture on lists. {pause} Last time, you learned to take a list apart with pattern matching. Now let's put that to work, on the most basic question you can ask about a list. {ask} How long is it? {pause}

[c3.hook.2] {chain} Take the list five, six, seven. {glance} You can see at a glance that it has three elements. {pause} {cant} But a program can't see at a glance. {question} All it can do is ask the question that pattern matching asks. Is this list empty, or is it a head stuck onto a tail? {pause} {how} So how do you count, using nothing but that question? {pause=1.5}

[c3.hook.3] {two} We'll answer that twice in this chapter. {first} The first answer is short and natural, {catch} but it hides a cost that grows with the length of the list. {second} The second answer gives exactly the same result, without that cost. {acc} It uses a trick called an accumulator, and you'll meet it again and again.

## Scene 2 · Following the shape of the list (ch3_s2_nlength)

> Two cases as cards. Left: `[]` → GOLD `0`. Right: a ConsChain x → [xs …] with a brace over the
> tail labelled "length of xs", and the head cell tagged GOLD "1": "1 + length of xs".
> Then the code, big (≈ 44) and centred, `nlength` in YELLOW:
> `let rec nlength = function` / `  | [] -> 0` / `  | x :: xs -> 1 + nlength xs`.
> A highlight box slides (P8): the two `|`, then line 2, then line 3. A curved YELLOW arrow from
> `nlength xs` back to the name; `rec` flashes and stays BLUE. Without `rec`, OCaml's reply in RED:
> `Error: Unbound value nlength` / `Hint: If this is a recursive definition,` /
> `you should add the rec keyword on line 1`. Last beat: each clause links (TEAL) to its card,
> and the chain shrinks 5,6,7 → 6,7 → 7 → [] as "each call: one element shorter".

[c3.def.1] The trick is to think about the two kinds of list, one at a time. {empty} First, the empty list. How long is it? {pause} {zero} Zero, of course. {cons} Second, a head, ex, consed onto a tail, exes. How long is that? {pause} {plus} It's one more than the length of exes. One for the head, plus however many elements are in the tail.

[c3.def.2] {code} And that's exactly what you write in OCaml. {name} We'll call this function en-length. The en stands for naive, just like en-sum in lecture two, and you'll soon see why. {bars} The function has two clauses, each starting with a vertical bar. {nil} The empty list gives zero. {step} And ex consed onto exes gives one, plus en-length of exes.

[c3.def.3] {self} Notice that en-length calls itself, on the tail. {rec} That's why the definition starts with let rec, short for recursive, and not just let. It tells OCaml that the name en-length can be used inside its own definition. {pause} {norec} Leave out the rec, and OCaml rejects the code. It says en-length isn't defined yet, and even suggests adding the rec.

[c3.def.4] {shape} Here's the deeper idea. {mirror} A list is either empty, or a head on a tail, and the function has a clause for each of those two shapes. {smaller} Each recursive call works on the tail, which is one element shorter. {ends} So the calls must eventually reach the empty list, and that's where they stop. {pause} {most} Most functions on lists work this way. The recursion follows the shape of the data.

## Scene 3 · Watching it run (ch3_s3_trace)

> The code shrinks to the top. The trace as stacked rows, each born from a copy of the row above
> (P11, P13), with a box riding on the part that changes (P12):
> `nlength [a; b; c]` / ⇒ `1 + nlength [b; c]` / ⇒ `1 + (1 + nlength [c])` /
> ⇒ `1 + (1 + (1 + nlength []))` / ⇒ `1 + (1 + (1 + 0))`.
> The waiting `1 +`s get YELLOW underlines as they pile up (v1 `s4_length.py`, `pending_line`), so
> the staircase shape is obvious. Then unwind the last row in place, innermost first:
> `1 + (1 + 1)` → `1 + 2` → GOLD `3` (the notes' "⇒ … 3"). Keep the trace (dimmed to 0.4) and add
> OCaml's replies beside it: `nlength []` → `- : int = 0`, `nlength [5; 6; 7]` → `- : int = 3`.

[c3.trace.1] Let's run en-length on a list of three elements, A, B, C. {s1} The list isn't empty. Its head is A, and its tail is B, C. So the second clause applies, and we get one, plus en-length of B, C.

[c3.trace.2] {s2} Same again. B, C isn't empty, so en-length of B, C becomes one, plus en-length of C. {s3} And en-length of C becomes one, plus en-length of nil. {s4} At last the list is empty. The first clause applies, and en-length of nil is zero.

[c3.trace.3] {look} Now look at what we've built. One plus, one plus, one plus zero. {pause} {none} Not a single addition has happened yet. Each of them was waiting for an answer from further down. {unwind} Only now can they run, from the inside out. {u1} One plus zero is one. {u2} One plus one is two. {u3} And one plus two is three. {pause}

[c3.trace.4] {check} OCaml agrees. {c1} En-length of nil is zero, {c2} and en-length of five, six, seven is three. {pause}

## Scene 4 · A tempting mistake (ch3_s4_faulty)

> Two separate blocks, each with its own `let rec` and OCaml's reply in GREEN:
> `let rec nlength [] = 0` → `val nlength : 'a list -> int = <fun>`
> `let rec nlength (x::xs) = 1 + nlength xs` → `val nlength : 'a list -> int = <fun>`
> On screen "what goes wrong?" (P23), held, then turned into the answer: a YELLOW name tag
> `nlength` points at block 1, then moves to block 2 while block 1 dims to 0.25 ("replaced").
> The real toplevel (5.4.1) warns under each (after a location line, safe to omit):
> `Warning 8 [partial-match]: this pattern-matching is not exhaustive.`
> `  Here is an example of a case that is not matched: _::_` (first; `[]` for the second).
> Run `nlength [5; 6; 7]` on a small chain: heads peel off, nil arrives, no clause matches, RED
> `Exception: Match_failure ("//toplevel//", 1, 16).` Then `nlength []` gives the same exception.
> Last beat: the correct version beside it, its `|` bars glowing: "one function, two clauses"
> versus "two functions, one clause each".

[c3.bad.1] Before we go on, here's a tempting mistake. {split} Why not write the two cases as two separate definitions? {first} First, en-length of nil is zero. {second} Then, en-length of ex consed onto exes is one plus en-length of exes. {pause} {ask} It looks reasonable, and OCaml accepts both. So what goes wrong? {pause=1.5}

[c3.bad.2] {two} These are two declarations, not one. {replace} The second let doesn't add a case to the first. It replaces it. {gone} The first en-length is simply forgotten, and the name now means a function that only handles lists that aren't empty. {warn} In fact, OCaml warns you both times that some lists aren't covered.

[c3.bad.3] {run} So let's call it on five, six, seven. {down} It strips off five, then six, then seven, {stuck} and reaches the empty list. But there's no clause for that anymore. {fail} So the program stops, with an error called a match failure. {pause} {nil} Even en-length of nil fails now. {never} This version can never deliver a result, because every call ends up at the empty list.

[c3.bad.4] {lesson} So a second let never extends an earlier one. It replaces it. {bar} To give a function several cases, put them all in a single definition, separated by vertical bars.

## Scene 5 · Any type, but wasteful (ch3_s5_cost)

> The correct code at the top with OCaml's reply `val nlength : 'a list -> int = <fun>`, the type
> GREEN and `'a` PINK. Three calls drop in one by one: `nlength ["to"; "be"; "or"; "not"]` → `- : int = 4`,
> `nlength [true; false]` → `- : int = 2`, `nlength [[3]; []; [5; 6]]` → `- : int = 3`. The `x` in
> `x :: xs` gets a box: matched, never used on the right.
> Cost (v1's "promise" stack, P19): walk a ConsChain while YELLOW `1 +` boxes stack up, one per call,
> with a GOLD counter "additions waiting" bound to the stack: 1, 2, 3, then racing to 1,000,000. GOLD
> "O(n) space". Then the stack grows off the top of the frame, with a RED "stack overflow" label.
> (Don't show a million crashing: with OCaml 5's default stack a million still fits.)
> Then Lecture 2's trace, small, beside the nlength staircase, same shape: `nsum 3` ⇒ `3 + (nsum 2)`
> ⇒ `3 + (2 + (nsum 1))` ⇒ `3 + (2 + (1 + (nsum 0)))` ⇒ `3 + (2 + (1 + 0))`. Label: "not tail-recursive".

[c3.poly.1] Back to the correct en-length. {reply} When you define it, OCaml replies that its type is alpha list to int. {alpha} En-length is polymorphic. It works on lists of any type at all. {strings} A list of strings, {bools} a list of booleans, {lists} even a list of lists. {pause} {why} That makes sense, because en-length never looks inside the elements. The head, ex, is matched, but never used. Each element just gets counted, whatever it is. {free} Many languages don't offer this kind of flexibility, or make you ask for it. In OCaml, you get it for free, without writing a single type.

[c3.cost.1] {but} Unfortunately, en-length is wasteful. {back} Remember those additions that had to wait? {stack} The computer must keep track of every one of them, until the recursion reaches the end of the list. {three} A list of three elements leaves three additions waiting. {million} A list of a million elements leaves a million additions waiting, all at once. {pause} {space} So the memory needed grows in proportion to the length of the list. We write that as big O of en space, where en is the length. {room} With a long enough list, it can even run out of room altogether, and crash with a stack overflow.

[c3.cost.2] {nsum} You've seen this problem before. En-sum, from lecture two, built exactly the same staircase. Three plus, two plus, one plus zero. {nest} In both functions, the recursive calls nest inside each other. Each call has to wait for the call inside it, and then do one more addition. {pause} {tail} A function like that is not tail-recursive. {cure} And lecture two gave us the cure, an accumulating argument.

## Scene 6 · The accumulator (ch3_s6_addlen)

> The code, big, `addlen` in YELLOW and `n` in GOLD:
> `let rec addlen n = function` / `  | []    -> n` / `  | x::xs -> addlen (n + 1) xs`
> with OCaml's reply `val addlen : int -> 'a list -> int = <fun>`. A box slides: `n` ("count so far"),
> `[]    -> n`, `(n + 1)`. For `function`: a ghost slot appears after `n`, "unnamed argument", with
> an arrow down to the patterns. The type splits into three pieces under braces: `int` "the count",
> `'a list` "any list", `int` "the length".
> Flat trace: `addlen 0 [a; b; c]` ⇒ `addlen 1 [b; c]` ⇒ `addlen 2 [c]` ⇒ `addlen 3 []` ⇒ `3`, beside
> a ConsChain A → B → C → [] with a GOLD count box riding above the current cell (PATTERNS §3),
> ticking 0 → 1 → 2 → 3 and landing on nil. Then side by side (v1's comparison): nlength's
> staircase with its YELLOW underlines, addlen's flat column. For "tail": box `1 + nlength xs` ("+ still
> to do") versus `addlen (n + 1) xs` ("last thing"). Costs: DIM "O(n) space" under the staircase,
> GOLD "O(1) space" then "O(n) time" under the column.

[c3.acc.1] {idea} Here's the idea. Instead of leaving each addition for later, {now} we do it right away, and carry the running count along with us. {code} This is add-len. {n} Its first argument, en, is the count so far. {nil} When the list runs out, en has counted every element, so the answer is simply en. {step} Otherwise, we ignore the head, add one to en, and carry on down the tail.

[c3.acc.2] {where} But wait. Add-len names only one argument, en. So where's the list? {pause} {function} Remember that the word function introduces an argument of its own. That argument has no name. Instead, it's matched straight away against the patterns underneath. {here} Here, that's what breaks open the list. {type} So add-len really takes two arguments, and OCaml gives its type as int to alpha list to int. {t1} First comes the count, an integer. {t2} Then a list of any type, so add-len is polymorphic too. {t3} And out comes the length, another integer.

[c3.acc.3] Let's watch it run, starting the count at zero. {s1} Add-len of zero, and A, B, C. The list isn't empty, so we add one to the count, and move on to the tail. {s2} That gives add-len of one, and B, C. {s3} Then two, and C. {s4} Then three, and nil. {s5} Now the list is empty, so the answer is the count, three. {pause}

[c3.acc.4] {compare} Now put the two traces side by side. {grows} En-length's expression grows longer at every step, as the additions pile up. {flat} Add-len's stays the same size. {hand} Each call just hands over to the next call, with nothing left to do afterwards. {pause} {iter} The recursive calls don't nest. As lecture two put it, add-len is iterative, or tail-recursive.

[c3.acc.5] {careful} Careful with that word, tail, again. {not} The tail in tail-recursive has nothing to do with the tail of a list. {last} It means the recursive call is the very last thing the function does. {nothing} So there's nothing to remember, and OCaml can reuse the same space for every call.

[c3.acc.6] {space} That means add-len needs only a fixed amount of space, however long the list is. Big O of one. {time} But its time is still big O of en. {why} There's no way to find the length of a list without visiting each of its elements. {pause} {sum} Same time as before, but far less space.

## Scene 7 · The wrapper, and recap (ch3_s7_recap)

> `let length xs = addlen 0 xs` → `val length : 'a list -> int = <fun>`, the `0` in GOLD.
> Below, two calls: `addlen 10 [5; 6; 7]` → `- : int = 13` (the 10 boxed, "wrong start"), then
> `length [5; 6; 7; 8]` → `- : int = 4`.
> Recap: four short lines, one per beat. Teaser for chapter 4: `[1; 2; 3] @ [4]` →
> `- : int list = [1; 2; 3; 4]` as two chains joining end to end, then `[1; 2; 3]` flipping to
> `[3; 2; 1]` under a GOLD "how slow?".

[c3.wrap.1] {annoy} There's one small annoyance left. Nobody wants to pass in a zero every time they ask for a length. {wrap} So we wrap add-len in a tiny function, called length, that supplies the zero for us. {start} That zero matters, because it's where the count starts. {ten} Start at ten instead, and add-len of ten, and the list five, six, seven, gives thirteen. {pause} {four} With the wrapper, length of five, six, seven, eight gives four. {type} And its type is alpha list to int, just like en-length. Same answer, in constant space.

[c3.recap.1] {recap} Let's recap. {r1} A recursive function on lists follows the shape of the list, with a clause for the empty list, and a clause for a head on a tail. {r2} The clauses belong in a single definition, separated by vertical bars. A second let doesn't extend the first. It replaces it. {r3} En-length works on lists of any type, but it leaves an addition waiting for every element, so it needs big O of en space. {r4} An accumulator does the work as it goes. Add-len still takes big O of en time, but only constant space. {pause}

[c3.recap.2] {next} Next time, we'll write our own function for joining two lists end to end. {rev} And we'll see why the obvious way to reverse a list turns out to be surprisingly slow. {pause}
