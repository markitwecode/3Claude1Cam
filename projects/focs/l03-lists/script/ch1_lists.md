# Chapter 1 · Lists and cons cells

Lecture 3 (Lists), part 1 of 5. Source: FoCS 2026-27 notes, pp. 21–23.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*; see LESSONS.md, "Write for the ear"). `{mark}` is a cue
point; `{pause}` / `{pause=1.5}` is a deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card: "Lists", "Foundations of Computer Science · Lecture 3", "Part 1: building lists".
> Then the hook on a row of element boxes [3][5][9]: a new element approaching the FRONT
> (GOLD "?"), then one approaching the END ("?"). Don't answer yet, just hint that they differ.

[c1.hook.1] {title} This is lecture three of Foundations of Computer Science, and it's all about lists. {pause} Lists are the simplest way to hold a collection of things, and in OCaml, you'll use them constantly.

[c1.hook.2] Let's start with a question that sounds almost too simple. {front} Suppose you have a list, and you want to add one more element to the front. How much work is that? {pause} {end} Now suppose you want to add it to the end instead. How much work is that? {pause=1.5}

[c1.hook.3] {guess} You might guess these cost about the same. They don't. {diff} One of them takes a single step, no matter how long the list is. The other gets slower and slower as the list grows. {why} By the end of this chapter, you'll see exactly why, because you'll know what a list really looks like inside the computer.

## Scene 2 · What is a list (ch1_s2_what)

> `[3; 5; 9]` as Code, with OCaml's reply `- : int list = [3; 5; 9]`. Brackets, then semicolons.
> Order: `[5; 3; 9]` ≠. Repetition: `[3; 3; 5; 9]` ≠. "a sequence, not a set".
> Types, one row per beat, values with their types in GREEN: int list, (int * string) list,
> int list list. The general rule as MathTex: x₁ … xₙ : τ ⟹ [x₁; …; xₙ] : τ list.
> `[3; "five"]` rejected in RED (compile-time error).

[c1.what.1] Here's a list in OCaml. {list} Three, five, and nine. {brackets} It's written in square brackets, {semis} with semicolons between the elements. {pause} When you type it into OCaml, it replies with the type: {type} int list. A list of integers.

[c1.what.2] A list is an ordered collection, and that means two things. {order} First, order matters. Five, three, nine is a different list from three, five, nine. {pause} {repeat} Second, repetition matters. Three, three, five, nine is different again, because it has four elements, not three. {set} So a list is not like a set from maths. It's a sequence.

[c1.what.3] There is one strict rule. {rule} Every element of a list must have the same type. {ints} A list of integers has type int list. {pairs} Here's a list of pairs, each holding an integer and a string. Its type is int times string, list. {lists} And you can even have a list of lists. This one has type int list list. {pause}

[c1.what.4] {general} The general pattern is simple. If every element has the same type, call it tau, then the list has type tau list. {bad} So what about a list that mixes an integer with a string? {pause} {reject} OCaml rejects it, before the program even runs. {gift} That might feel strict, but it's a gift. Whenever you take an element out of a list, you know exactly what type it is.

## Scene 3 · Tuples, arrays, and two free functions (ch1_s3_compare)

> Tuple `(1, "one")`: round brackets, commas, fixed size, mixed types. List: semicolons, any
> length, one type. The trap: `[1, 2]` → `(int * int) list = [(1, 2)]` (one element!).
> Arrays: a row of indexed slots, jump to slot 5; an out-of-range index in RED. Lists: walk
> from the front. Then `[3; 5; 9] @ [2; 10]` ⇒ `[3; 5; 9; 2; 10]`, and `List.rev`.

[c1.cmp.1] You've already met another way of grouping values: tuples. {tuple} A tuple uses round brackets and commas. {fixed} It has a fixed size, and its parts can have different types: here, an integer and a string, side by side. {pause} {list} A list is different. It uses semicolons, it can be any length, and every element has the same type.

[c1.cmp.2] That comma versus semicolon difference is a classic trap. {trap} Look at this: square brackets, but with a comma inside. {pause} {reveal} OCaml doesn't see a list of two numbers. It sees a list with just one element, which is the pair, one comma two. {lesson} So inside a list, always use semicolons.

[c1.cmp.3] What about arrays, which many other languages use instead? {array} In an array, you can jump straight to any position: give me element number five. {oob} That's handy, but it's also a famous source of bugs. Ask for a position that doesn't exist, and things go wrong. {pause} {walk} Lists work differently. You don't jump into the middle. You start at the front, and work your way along. {recursion} That might sound limiting, but it fits beautifully with recursion, as you'll see in the coming chapters.

[c1.cmp.4] OCaml gives you a couple of list tools for free. {append} The at sign joins two lists end to end. Three, five, nine, joined with two and ten, gives three, five, nine, two, ten. {rev} And List dot rev reverses a list. {later} Later in this lecture, we'll build both of these ourselves, and find out how much they really cost.

## Scene 4 · Two kinds of list (ch1_s4_build)

> "Every list is one of two things": `[]` (nil) | `x :: l` (cons). Head/tail labels on x and l.
> Build `[3; 5; 9]` right to left as an expression: [] → 9 :: [] → 5 :: 9 :: [] → 3 :: 5 :: 9 :: [].
> Show `[3; 5; 9]` = `3 :: 5 :: 9 :: []` = `3 :: (5 :: (9 :: []))` (grouping from the right).
> Finally `[]` on its own with OCaml's reply `- : 'a list = []`, 'a in PINK.

[c1.build.1] Now for the most important idea in this chapter. {two} Every list in OCaml is built from just two pieces. {nil} The first is the empty list, written as a pair of empty square brackets, and usually called nil. {cons} The second is cons, written as a double colon. {pause} {what} Cons takes one element and a list, and builds a new, longer list, with that element stuck on the front.

[c1.build.2] {names} In the expression ex cons ell, the element on the left, ex, is called the head. {tail} And the list on the right, ell, is called the tail. {pause} {every} Every list that isn't empty is exactly this: a head, stuck onto a tail.

[c1.build.3] So let's build three, five, nine, one step at a time. {start} Start with nil, the empty list. {nine} Cons nine onto it, and you get the list containing just nine. {five} Cons five onto that, and you get five, nine. {three} Cons three onto that, and you get three, five, nine. {pause}

[c1.build.4] {sugar} So the square bracket notation is really just a convenient shorthand. Three, five, nine in brackets means three cons five cons nine cons nil. {right} Notice how the conses group from the right. The nine is attached to nil first, then the five, then the three. {pause} {back} The list is built from the back, but read from the front.

[c1.build.5] {niltype} One small puzzle. What is the type of nil on its own? {pause} {cant} It can't be int list, because it could just as well be an empty list of strings. {alpha} So OCaml gives it the type alpha list, which means a list of any type you like. We'll see much more of that little alpha in the next chapter.

## Scene 5 · Inside the computer (ch1_s5_cells)

> Box-and-pointer cells (ConsChain). A cell = value slot + arrow. Build 3 → 5 → 9 → [].
> Cons 1 on the front: the tempting wrong picture (everything shuffles along) crossed out;
> then one new YELLOW cell pointing at the existing first cell. GOLD O(1).
> Name the lists: x → old first cell, y → new cell; the shared cells glow TEAL.

[c1.cells.1] Now let's look inside the computer. {cells} Each cons builds one small cell in memory. {value} A cell holds two things: {slot} the value, {arrow} and an arrow pointing to the rest of the list. {pause} {chain} So three, five, nine is a chain of three cells, ending in nil.

[c1.cells.2] Now, back to our opening question. Suppose we want to put a one on the front. {shuffle} You might imagine the computer shuffling every element along, to make room. {pause} {nope} It doesn't do that at all. {new} It builds one new cell, holding the one, {point} and points its arrow at the list that was already there. {pause} That's it.

[c1.cells.3] {cost} One new cell, one arrow. It doesn't matter whether the list has three elements or three million. Cons always does the same tiny amount of work. {o1} We say it takes constant time, written big O of one. {pause}

[c1.cells.4] And there's a second, more surprising consequence. {old} The old list, three, five, nine, hasn't changed at all. {x} If we had called it ex, then ex still means three, five, nine. {y} The new list, call it why, is one, three, five, nine. {share} And the two lists share the very same cells. {pause} {immut} This sharing is only safe because OCaml lists never change once they're built. Nobody can come along and modify a cell behind your back.

## Scene 6 · Head, tail, and the end of the list (ch1_s6_headtail)

> On the chain: head = value in the first cell; tail = where the first arrow points (box the
> whole rest). "tail ≠ last element" in RED. Tails of tails down to nil.
> Last element: a YELLOW marker walks the arrows one by one; GOLD O(n). Back to the hook:
> front = 1 step, end = walk the whole list. Empty list: no head, no tail, "?".
> Recap: four short lines, one per beat. Teaser for chapter 2.

[c1.ht.1] Taking a list apart is just as cheap as building one. {head} The head of a list is the value in its first cell. {tail} The tail is wherever the first cell's arrow points. {cheap} Each of these just follows one arrow, so both take constant time.

[c1.ht.2] {warn} But be careful with that word, tail. It's easy to think the tail is the last element. {pause} It isn't. {rest} The tail of three, five, nine is the whole rest of the list: five, nine. {tailtail} And the tail of that is the list containing just nine. {nil} And the tail of that is nil.

[c1.ht.3] {last} So what if you really do want the last element? {walk} Then there's no shortcut. You have to start at the front, and follow the arrows, one by one, all the way to the end. {million} For a list with a million elements, that's a million steps. {pause} {answer} And that's the answer to our opening question. Adding to the front is one step. But anything at the end of a list means walking the whole length of it.

[c1.ht.4] {empty} One last thing to notice. The empty list has no first cell. So it has no head, and no tail. {pause} {ask} What should happen if you ask for one anyway? That's where we'll pick up in the next chapter.

[c1.recap.1] {recap} Let's recap. {r1} A list is a sequence of elements, all of the same type. {r2} Every list is either nil, or a head consed onto a tail. {r3} Cons, head, and tail are all constant time, because each one makes or follows a single arrow. {r4} And lists never change, so new lists can safely share the cells of old ones. {pause} {next} Next time: taking lists apart properly, with pattern matching.
