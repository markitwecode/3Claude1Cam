# Chapter 2 · Pattern matching and polymorphism

Lecture 3 (Lists), part 2 of 5. Source: FoCS 2026-27 notes, pp. 22–24 (§3.2).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*; see LESSONS.md, "Write for the ear"). `{mark}` is a cue
point; `{pause}` / `{pause=1.5}` is a deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card: "Lists", "Foundations of Computer Science · Lecture 3", "Part 2: pattern matching".
> Ch1's two shapes, big, side by side: a TEAL Nil box labelled "nil", and a ConsChain
> 1 → 2 → 3 → [] labelled "cons", with "head"/"tail" braces. Their code forms underneath: `[]`, `x :: l`.
> The question as an object (P23): "head of [] = ?" with a GOLD "?". A YELLOW pointer reaches
> for the Nil's first cell and finds nothing. Keep the question on screen; scene 3 answers it.
> Then a box labelled "function" with a list sliding in under a grey cover, and "which shape?" beside it.
> On {types}, a PINK `'a` fades in briefly as a preview.

[c2.hook.1] {title} Welcome back. In the last chapter, we saw that every list in OCaml is one of two things. {nil} Either it's nil, the empty list. {cons} Or it's a head, consed onto a tail. {pause} {ask} And we ended on a question. What should happen if you ask for the head of an empty list? {pause=1.5}

[c2.hook.2] {nothing} There's nothing there to give back. The empty list has no first cell, so it has no head. {pause} {bigger} And behind that sits a bigger question. When a function is handed a list, how can it tell which of the two shapes it got? {pause} {must} It has to know, before it reaches for a head that might not exist.

[c2.hook.3] {plan} In this chapter, we'll answer both questions with a single idea, called pattern matching. {types} Along the way, we'll meet some strange-looking types, with a little alpha in them. {every} And we'll see how they let a single function work on lists of every kind.

## Scene 2 · Two shapes, two clauses (ch2_s2_null)

> Hero Code (~48), exactly as in the notes:
> `let null = function` / `  | [] -> true` / `  | x :: l -> false`, with OCaml's reply
> `val null : 'a list -> bool = <fun>` below (DIM for now, but 'a stays PINK; scene 5 reads it).
> P8 highlight box slides: `function` (BLUE keyword) → both `|` bars → the left of each `->`
> (the patterns, TEAL) → the right (`true`, `false`). On {two}, each pattern grows an arrow to a
> small drawing of its shape: `[]` → a Nil box; `x :: l` → one cell with x in its slot, its arrow
> to a box labelled l. Caption: "the two shapes from chapter 1".
> Matching `null [1; 2; 3]`: the chain 1 → 2 → 3 → [] tries clause 1, which gets a RED ✗. Then clause 2:
> `x` drops onto the cell holding 1 (YELLOW) and a TEAL brace `l` grows under 2 → 3 → []. GREEN ✓,
> and `false` flies out of the clause (TransformFromCopy) into the reply `- : bool = false`.
> Then `null []`: clause 1 ✓ at once, `- : bool = true`. Finally a stroke-only flash on the
> unused `x` and `l` in clause 2.

[c2.null.1] {code} Here's our first pattern match. It's a function called null, which tells you whether a list is empty. {pause} {function} The keyword, function, says that null takes a single argument. {shapes} But instead of giving that argument a name, we list the shapes it might have.

[c2.null.2] {clauses} Each shape gets its own line, called a clause, and the clauses are separated by vertical bars. {left} On the left of each arrow is a pattern, a shape the list might have. {right} On the right is the answer to give back, if the list has that shape. {pause}

[c2.null.3] {two} Now look closely at the two patterns. {empty} The first is the empty list. {conspat} The second is ex cons ell, some head consed onto some tail. {pause} {same} These are exactly the two shapes of a list from chapter one. {cover} No list has both shapes, and every list has one of them. So for any list at all, exactly one clause fits.

[c2.null.4] {how} So how does OCaml pick the clause? Let's call null on the list one, two, three. {top} OCaml tries the clauses in order, from the top. {first} Is this list empty? {pause} {no} No, so the first clause doesn't fit. {second} Is it some head, ex, consed onto some tail, ell? {pause} {yes} Yes. Ex matches the first element, one, and ell matches the rest, two, three. {false} So the second clause fits, and null gives back false.

[c2.null.5] {nil} Now call null on the empty list. {fits} This time, the very first clause fits, so the answer is true. {pause} {names} Notice something else. The second pattern gives names to the parts of the list, ex and ell, even though null never uses them. {next} Those names are where patterns get their real power, as the next two functions show.

## Scene 3 · Head and tail, and the empty list (ch2_s3_hdtl)

> `let hd (x::l) = x` big. On {where}, a ghost argument name `xs` fades out of the spot where
> `(x::l)` sits: the pattern takes the name's place. `hd [1; 2; 3]`: the pattern lies over the
> chain, x on the cell holding 1, giving `- : int = 1` (GOLD 1).
> `let tl (x::l) = l` directly beneath, aligned so the two lines differ only in the final `x` / `l`.
> The highlight box hops between those two tokens. `tl [7; 6; 5]`: TEAL brace `l` over 6 → 5 → [],
> giving `- : int list = [6; 5]`, with a small RED reminder "a list, not an element".
> The real toplevel output for hd, in the order OCaml prints it: the warning first, in a
> YELLOW-stroked box, then `val hd : 'a list -> 'a = <fun>`. Warning text (real, location lines dropped):
> `Warning 8 [partial-match]: this pattern-matching is not exhaustive.`
> `Here is an example of a case that is not matched: []`. On {nil}, that `[]` gets a RED box.
> hd []: the `[]` copies out of the warning (TransformFromCopy) into `hd []`. The pattern tries to
> lie over a Nil box, finds no cell, and gets a RED ✗. Then `Exception: Match_failure ("//toplevel//", 1, 7).`
> (may be shortened to `Exception: Match_failure …`). `tl []` gives the same exception, smaller.
> On {answer}, scene 1's "head of [] = ?" returns and its "?" turns into a RED "error" (P23).
> Then the guard: `null xs` gives `false`, and only then `hd xs`, with a GREEN ✓.

[c2.hdtl.1] {hd} Here's the head function, written with a pattern. {where} This time there's no keyword, function. Instead, the pattern sits right where the argument's name would normally go. {pause} {reads} It says, the argument must be some head, ex, consed onto some tail, ell. {gives} And the answer is ex. {call} So on the list one, two, three, ex matches the first element, and the head function gives back one.

[c2.hdtl.2] {tl} The tail function is identical, except for what it gives back at the very end. {ell} Instead of ex, it hands back ell. {call} So the tail of seven, six, five is six, five. {pause} {list} And remember from chapter one, that's a whole list, not a single element.

[c2.hdtl.3] {type} But when you type the head function into OCaml, something new happens. Before it even tells you the type, it prints a warning. {warn} It says this pattern matching is not exhaustive. In other words, there are lists it doesn't handle. {example} And it even shows you an example of such a list. {pause} {nil} The empty list.

[c2.hdtl.4] {only} It's only a warning, so OCaml accepts the function anyway. {call} But watch what happens when you ask for the head of the empty list. {pause} {nofit} The pattern needs a first cell, and there isn't one. No clause fits, so there's no answer to give back. {raise} Instead, OCaml raises an exception, called match failure. For now, think of that as the program giving up. {tail} The tail function fails in exactly the same way.

[c2.hdtl.5] {answer} So that's the answer to our opening question. The head of an empty list isn't nil, or zero, or anything else. {error} It's an error. {pause} {null} So if a list might be empty, check it with null first, {safe} and only ask for the head when null says false.

## Scene 4 · Why patterns beat head and tail (ch2_s4_why)

> Caption "the second element". Left half, version A: `let second xs = hd (tl xs)`, with the reply
> `val second : 'a list -> 'a = <fun>` and NO warning (an empty slot where scene 3's warning box sat).
> `second [3; 5; 9]` on the chain 3 → 5 → 9 → []: `tl` moves a YELLOW marker on to the 5 cell,
> `hd` lifts out the 5, giving `- : int = 5`.
> `second [3]` on the chain 3 → []: `tl [3]` gives `- : int list = []` (fine, GREEN). Then hd on the Nil:
> RED `Exception: Match_failure ("//toplevel//", 1, 7).` Caption "found only at run time".
> Right half (A dims to ~0.4), version B: `let second = function` / `  | x :: y :: rest -> y`.
> The pattern lies over 3 → 5 → 9 → []: x on 3, y on 5 (YELLOW), brace `rest` over 9 → [].
> On {warn}, the real warning appears: `Warning 8 [partial-match]: this pattern-matching is not exhaustive.`
> `Here is an example of a case that is not matched: x::[]`. Draw `x::[]` as a single cell → Nil,
> and on {same} link it with a TEAL line to A's crashed `second [3]`.
> Final split, kept on screen: A "silent until it crashes" (RED) | B "warned before it runs" (GREEN).

[c2.why.1] Now, you could take lists apart using nothing but head and tail. {task} Say you want the second element of a list. {combo} That's the head of the tail. {works} Try it on three, five, nine. The tail is five, nine, and its head is five. {pause} {silent} And notice that this time, OCaml prints no warning at all. There's no pattern here for it to check.

[c2.why.2] {short} But what about a list with only a single element, like the list containing just three? {pause} {tail} Its tail is nil, and that part is fine. {head} But then we ask for the head of nil. {crash} Match failure. {pause} {late} And nothing warned us. This mistake only shows up while the program is running, on exactly the wrong input.

[c2.why.3] {hard} That's why taking lists apart with head and tail is so hard to get right. Every call quietly assumes the list is long enough. {pattern} Here's the same function, written with a pattern instead. {shape} The pattern spells out exactly what we expect. Some element, ex, then a second element, called why, then the rest of the list. {give} And the answer is that second element. {pause} {picture} You can almost see the shape of the list in the code.

[c2.why.4] {warn} And now OCaml can check our work. It warns that this match is not exhaustive, {example} and the example it gives is ex cons nil, a list with just a single element. {pause} {same} That's precisely the case that crashed before. {lesson} With head and tail, nobody warns you. With patterns, OCaml spots the missing shapes before the program ever runs, {you} and it's up to you to decide what those shorter lists should do. {seldom} So in practice, you'll rarely need head and tail at all.

## Scene 5 · Alpha: one function, every type (ch2_s5_poly)

> Hero: three signatures stacked and aligned on the colon (~48), every 'a PINK:
> `val null : 'a list -> bool`, `val hd : 'a list -> 'a`, `val tl : 'a list -> 'a list`
> (OCaml's replies from scenes 2–3, with `= <fun>` dropped). On {arrow}, braces on the hd row:
> "in" under `'a list`, "out" under the result.
> On {tick}, zoom in on one `'a`: the apostrophe gets a stroke-only flash, MathTex α appears beside it,
> and the label "type variable = any type" drops in.
> P12 substitution under the hd row: `hd ["cat"; "dog"]`. Boxes ride onto both 'a, which turn GREEN
> `string`, and the type reads `string list -> string`. Reply `- : string = "cat"`. Then faster:
> `hd [1; 2; 3]`, 'a ↦ `int`, giving `- : int = 1`. Then `hd [[1; 2]; [3]]`, 'a ↦ `int list`,
> giving `- : int list = [1; 2]`. Then the type snaps back to `'a list -> 'a`: still the same function.
> "polymorphic" with "= many shapes" beneath, and three differently typed lists flowing into the hd row.
> On {fst}, OCaml's reply to `fst`: `- : 'a * 'b -> 'a = <fun>`, with 'b in its own colour, distinct
> from 'a's PINK. The ch1 pair `(1, "one")` flows in, 'a ↦ int and 'b ↦ string, giving `- : int = 1`.
> On {greek}, a row of `'a 'b 'c` with MathTex α β γ under them.

[c2.poly.1] Now let's look at the types OCaml gave these three functions. {null} Null takes an alpha list, and gives back a boolean, true or false. {hd} Head takes an alpha list, and gives back an alpha. {tl} And tail takes an alpha list, and gives back another alpha list. {arrow} In each type, the arrow separates what goes in from what comes out.

[c2.poly.2] {what} So what is alpha? {pause} {tick} On screen, it has an apostrophe in front, and that apostrophe marks it as a type variable. {any} A type variable stands for any type at all. {pause}

[c2.poly.3] {use} Watch what happens when we use the head function. {strings} Give it a list of strings, cat and dog. {fill} Now alpha has to be string, everywhere it appears. {result} So head now takes a string list and gives back a string, and the answer is the string, cat. {ints} Give it a list of integers, and alpha becomes int. {lists} Give it a list of lists, and alpha becomes int list, so the answer is a whole list, one, two. {pause}

[c2.poly.4] {poly} A function like this is called polymorphic, from the Greek for many shapes. {single} It's a single function that works on lists of every element type. {sense} And that makes sense, if you think about what the head function actually does. It hands back whatever is in the first cell, without ever looking inside it. {pause} {care} It doesn't care what the elements are, so its type doesn't either.

[c2.poly.5] {more} Sometimes a type needs more than one type variable. {fst} For example, OCaml's built-in function for the first part of a pair takes an alpha times beta, and gives back an alpha. {parts} The two parts of a pair can have different types, so they get different variables, alpha and beta. {same} And the answer always has the type of the first part. {greek} In general, these variables are read as Greek letters, alpha, beta, gamma, and so on.

## Scene 6 · Checked before it runs (ch2_s6_checked)

> A horizontal timeline: a "compile time" zone (GREEN, with a type-check tick) then a "run time"
> zone (BLUE, ▶). On {mix}: `hd ["cat"; "dog"] + 1` with a RED underline and the real error on two
> lines: `Error: This expression has type string` / `but an expression was expected of type int`.
> It stays in the compile-time zone and never reaches ▶. Beside it, `hd [1; 2; 3] + 1` gives `- : int = 2` (GREEN).
> check.2: a chain whose cells all carry the same GREEN `int` tag. Whatever hd lifts out keeps the tag.
> check.3: ch1's reply returns, `[]` → `- : 'a list = []`. Then `1 :: []` → `- : int list = [1]`
> (PINK 'a turns GREEN int) and `"cat" :: []` → `- : string list = ["cat"]`. Then `null []` →
> `- : bool = true`, the 'a in `[]` staying PINK.
> Recap: five short lines, one per beat. Teaser: the chain 5 → 6 → 7 → [] with only the first
> cell lit and the rest dimmed, under a GOLD "how many?".

[c2.check.1] {when} All of this type checking happens before your program runs, at what's called compile time. {mix} So suppose you take the head of cat and dog, and try to add one to it. {pause} {reject} OCaml rejects it straight away. The head of a string list is a string, and you can't add a number to a string. {fine} Do the same sum with the list one, two, three instead, and it's fine. The answer is two.

[c2.check.2] {guarantee} Checking early buys you strong guarantees once the program does run. {same} For example, every element of a list is sure to have the same type. {never} So whatever the head function hands back, its type is already known. You'll never find a string where you expected a number. {pause}

[c2.check.3] {back} And now we can finally read a type from chapter one. {niltype} The empty list has type alpha list. {open} That's a list whose element type is still open. {int} Cons an integer onto it, and alpha becomes int. {string} Cons a string onto it, and alpha becomes string. {pause} {null} And null of nil is simply true. Its alpha never gets decided, and it never needs to be.

[c2.recap.1] {recap} Let's recap. {r1} Pattern matching takes a list apart by its shape, with a clause for nil and a clause for cons. {r2} OCaml tries the clauses in order, and the pattern gives names to the parts. {r3} Head and tail have a single clause each, so the empty list makes them raise an exception, and OCaml warns you in advance. {r4} Their types contain alpha, a type variable, so a single function works for every element type. {r5} And all of it is checked before the program runs. {pause}

[c2.recap.2] {next} Next time, we'll put patterns and recursion together. {count} How do you count the elements of a list, when all you can see is its first cell? {pause} {length} We'll write a function that computes the length of any list.
