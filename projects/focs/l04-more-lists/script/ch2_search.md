# Chapter 2 · Searching a list

Lecture 4 (More on Lists), part 2 of 7. Source: FoCS 2026-27 notes v1.8, pp. 31–32 (§4.2–4.3),
with a forward link to p. 37 (binary search) and callbacks to Lecture 2's `power` (pp. 13–17)
and Lecture 3 (string order, the "never mix up their types" slogan).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

All code and replies below were run in OCaml 5.4.1 and are quoted verbatim.

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card, `title_card("Part 2 · Searching a list")`: "More on Lists", "Foundations of Computer
> Science · Lecture 4", "Part 2 · Searching a list".
> "Last time" (on {last}): ch1's running chain 3 → 5 → 9 → 4 → 7 → [] (ConsChain, L3 palette) comes in
> centred, with ch1's GOLD cut after cell 2 and its two braces, "take 2" over 3, 5 and "drop 2" over
> 9, 4, 7. On "copied", the 3, 5 cells pulse; on "skipped", the brace over 9, 4, 7 pulses. Then cut and
> braces fade. The chain stays for s2, and comes back in the same place in s4.
> The question in YELLOW above the chain: "Is 9 in this list?" (ch1's closing shot asked it with a
> pointer over the 9; here no pointer yet). On {glance}, all five values light up together (the eye's
> view), then settle back.
> On {one}: everything dims to DIMMED except the first cell, and a small GOLD pointer (a triangle above
> the cell) drops onto it: the program's eye, reused in s2 and s4.
> Last beat: under the question, two small tags, GOLD "how long?" and BLUE "how, in OCaml?", then on
> {equal} a third in YELLOW, "what does equal mean?".

[c2.hook.1] {title} This is part two of More on Lists. {pause=2} {last} Last time, take and drop cut a list in two. Take made a copy of the front part, and drop skipped over it.

[c2.hook.2] {chain} Here's the same list again. Three, five, nine, four, seven. {ask} Is nine in this list? {pause} {glance} You can see straight away that it is. {program} But a program has no way to take in the whole list at once. {one} It starts at the head, and looks at one element at a time. {pause}

[c2.hook.3] {how} So how long does a search take, and how do you write one in OCaml? {equal} On the way, we'll find that asking whether two values are equal is more subtle than it sounds. {pause}

## Scene 2 · One at a time (ch2_s2_linear)

> The s1 chain stays centred, the GOLD pointer on cell 1. YELLOW "looking for 9" above it, and a GOLD
> counter "comparisons: 0" at top right.
> At each comparison, a small tag pops under the current cell, `9 = 3?`, then a RED ✗; `9 = 5?` ✗;
> `9 = 9?` GREEN ✓. The counter ticks 1, 2, 3, and the pointer steps right after each ✗ (cue the
> marks {c1} {c2} {c3}). On {found}, cell 3 glows GREEN.
> Reset on {six}: tags fade, counter back to 0, pointer back to cell 1, label "looking for 6". On
> {sweep}, the pointer crosses all five cells in step with the spoken values, a RED ✗ under each, the
> counter reaching 5. On {nil}, it lands on the TEAL nil, which flashes; "not found" in RED.
> Generalise on {general}: the chain's values morph into x₁ → x₂ → … → xₙ → [] (new labels out of
> the old ones). GOLD labels in turn: {avg} a brace to the middle, "found, on average: about n/2";
> {worst} a brace over the whole chain, "found, worst case: n"; {miss} the brace takes in nil too,
> "absent: always n".
> On {big}, the three labels merge into one big GOLD "O(n)" under the title "linear search". Shrink the
> abstract chain with its "linear: O(n)" to top-left; it stays there in s3.

[c2.lin.1] {name} The obvious method is called linear search. {each} Compare the item you want with each element in turn, starting at the head. {nine} Let's look for nine. {c1} Is nine equal to three? No. {c2} Is nine equal to five? No. {c3} Is nine equal to nine? Yes. {found} Found it, after three comparisons. {pause}

[c2.lin.2] {six} Now look for six. {sweep} Three, five, nine, four, seven. {five} That's five comparisons, and every answer is no. {nil} Then we reach nil, and there's nowhere left to look. {absent} Six is not in the list. {all} To be sure that an item is missing, you have to compare it with every element.

[c2.lin.3] {general} Now think of a list of any length, say en. {avg} If the item is there, you'll find it about halfway along, on average, after checking half the elements. {worst} At worst, it's the last element, and you check every element. {miss} And if it's missing, you always check every element. {pause} {big} Either way, the time is proportional to the length of the list. Linear search takes linear time, big O of en.

## Scene 3 · Faster ways to search (ch2_s3_faster)

> "linear: O(n)" sits small at top-left (from s2). In the centre, a row of 16 boxes of sorted GOLD
> numbers, `2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53`, labelled "ordered".
> Halving: on {middle} the middle box flashes YELLOW and one half dims (DIMMED); on {halve} it repeats,
> 16 → 8 → 4 → 2 → 1 live boxes, with a GOLD step counter 1, 2, 3, 4 beside the row. On {power}, a DIM
> tag "Lecture 2: power halves its exponent". On {log}, GOLD "ordered: O(log n)".
> On {million}: two GOLD columns, "linear: up to 1,000,000 comparisons" and "halving: about 20 steps"
> (with a small `2²⁰ = 1,048,576`), and on {exp} a YELLOW "exponentially better" between them.
> On {binary}: DIM caption "binary search: next lecture". On {lists}: a small ConsChain under the row,
> and an arrow that has to crawl cell by cell from the head to the middle, captioned "needs arrays or
> trees, not lists".
> Clear the row. On {index}: a YELLOW item goes into a box labelled "hash table", and one arrow lands
> straight on its slot in a column of slots. GOLD "indexed: O(1)", with a DIM footnote "(within machine
> limits)" on {limits}. On {web}, a simple search-bar icon beside it.
> The three costs line up as a ladder, top to bottom: O(n), O(log n), O(1).
> On {why}, the ladder dims and "linear: O(n)" comes back to centre, with GREEN tags appearing one by
> one: {simple} "simple", {general} "general: any order", {small} "fine for small collections",
> {start} "the starting point for better algorithms".

[c2.fast.1] {large} For a large collection, that's slow, and there are better ways. {sorted} The first is to keep the items in order. {middle} Then you can compare with the middle item, and throw away the wrong half. {halve} Then cut what's left in half, and so on. {power} The power function from lecture two uses the same halving. {log} So ordered searching takes only big O of log en.

[c2.fast.2] {million} Let's see what that means. {lin} Searching a million items one at a time can take a million comparisons. {twenty} Halving a million down to one takes only about twenty steps. {pause} {exp} That's exponentially better. {binary} This is called binary search, and it's coming next lecture. {lists} It needs arrays or trees, not lists, because a list can only be walked from the head, one cell at a time.

[c2.fast.3] {index} The second way is to index the data. {hash} A structure called a hash table can find an item in constant time, big O of one, {limits} as long as you stay within the machine's limits. {web} Efficient indexing is of prime importance. Think of web search engines. They depend on it.

[c2.fast.4] {why} So why bother with linear search at all? {pause} {simple} First, it's simple. {general} Second, it's general. The items can be in any order at all. {small} For small collections, it's fast enough. {start} And it's the starting point for better algorithms. {write} So let's write it.

## Scene 4 · member (ch2_s4_member)

> The code, big and centred, `member` in YELLOW, keywords BLUE, `[]` and `::` TEAL:
> `let rec member x = function` / `  | [] -> false` / `  | y::l ->` / `      if x = y then true` /
> `      else member x l`
> A highlight box slides: {x} the `x` ("the item"); {function} the word `function`, with a ghost slot
> after `x`, "the list" (as in ch1's `take`); {nil} `| [] -> false`; {cons} `y::l`, with tags `y` "head"
> and `l` "tail"; {test} `if x = y then true`; {else} `else member x l`, with a curved YELLOW arrow back
> to the name.
> On {reply}, OCaml's reply under the code: `val member : 'a -> 'a list -> bool = <fun>` (type GREEN,
> `'a` PINK). On {read}, braces under its three parts: "the item", "a list of the same type", "yes or no".
> The code shrinks to top-left. The s1/s2 chain comes back with its GOLD pointer. A flat trace, each row
> born from a copy of the one above, the pointer stepping in time:
> `member 9 [3; 5; 9; 4; 7]` / ⇒ `member 9 [5; 9; 4; 7]` / ⇒ `member 9 [9; 4; 7]` / ⇒ `true` (GREEN),
> then `- : bool = true`. On {six}, a second, quicker column: `member 6 [3; 5; 9; 4; 7]` ⇒ … ⇒
> `member 6 []` ⇒ `false`, then `- : bool = false`.
> On {flat}, ch1's `take` trace returns small and DIM beside it, its waiting `3 ::` and `5 ::`
> underlined YELLOW, versus member's column with nothing to underline. GOLD "O(n) time", "O(1) space".
> Last beat ({type}): the reply again, both `'a` boxed PINK, and `x = y` boxed YELLOW, a "?" between.

[c2.mem.1] {code} In OCaml, linear search is a function called member. {x} Its first argument, ex, is the item we're looking for. {function} As in take, the word function supplies the list, as a second argument with no name. {nil} If the list is empty, the answer is false. {cons} Otherwise, the list has a head, why, and a tail, ell.

[c2.mem.2] {test} If ex equals why, that's a match, and the answer is true. {else} If not, we look in the tail, with member of ex and ell. {reply} OCaml replies with its type, alpha to alpha list to bool. {read} That's an item, a list of items of the same type, and a yes or no answer.

[c2.mem.3] {run} Let's run it on our list, looking for nine. {s1} Nine is not three, so we search the tail, five, nine, four, seven. {s2} Nine is not five, so we move on again. {s3} Nine equals nine, so the answer is true. {six} Looking for six, the search runs all the way to nil, and the answer is false. {pause}

[c2.mem.4] {flat} Notice that nothing piles up from row to row, the way the conses did in take. {last} The recursive call is the very last thing member does, just like in drop. {iter} So member is iterative. {cost} It takes big O of en time, but only constant space. {pause}

[c2.mem.5] {type} Now look at that type again. {alpha} The alpha means member works on lists of any type. It's polymorphic. {yet} Yet it tests whether ex equals why. {how} How can it compare two values without knowing their type? {pause=1.5}

## Scene 5 · Polymorphic equality (ch2_s5_equality)

> Title "polymorphic equality". The five operators in a row, BLUE: `=  <  <=  >  >=`, each lighting on
> its spoken name ({ops}).
> On {lists}: two small ConsChains, 1 → 2 → [] above 1 → 2 → []. On {walk}, a YELLOW scanner pairs
> cell with cell, a GREEN tick per pair and on the two nils, then `[1; 2] = [1; 2]` → `- : bool = true`.
> On {less}: the lower chain's 2 becomes 3. Same scan: 1 and 1 tick, then the 2 / 3 pair glows GOLD
> ({decide}) → `[1; 2] < [1; 3]` → `- : bool = true`. On {strings}, L3's `"apple" < "banana"` →
> `- : bool = true` appears small and DIM beside it, its first letters boxed the same way.
> On {tuples}: `("Bob", 1) > ("Amy", 9)` (ch3's names; checked), the two names boxed GOLD ({first}), the 1 and 9 dimmed to
> DIMMED on {never} → `- : bool = true`. On {bools}: `true > false` → `- : bool = true`.
> On {member}: `member "dog" ["cat"; "dog"]` → `- : bool = true`, then on {nested}
> `member [1; 2] [[3]; [1; 2]]` → `- : bool = true`, the inner `[1; 2]` boxed.
> On {safe}: the six lines stack as a table, every reply `- : bool = true` in GREEN, captioned "ints,
> strings, bools, and tuples or lists of them".

[c2.eq.1] {answer} The answer is a special feature of OCaml, called polymorphic equality. {ops} It covers the equals sign, and the four comparisons, less than, less than or equal, greater than, and greater than or equal. {any} All five work at any type. {inspect} They inspect the structure of the two values, and compare them in a consistent order.

[c2.eq.2] {lists} Start with lists. Is the list one, two equal to the list one, two? {walk} OCaml walks along both lists, comparing the elements pair by pair. {match} They match all the way to nil, so the answer is true. {less} Is one, two less than one, three? {pause} {decide} Yes. The first elements are equal, so it comes down to the second elements, and two is less than three. {strings} It's the rule from lecture three that put apple before banana.

[c2.eq.3] {tuples} Tuples work the same way, from left to right. {bob} The pair Bob and one is greater than the pair Amy and nine, {first} because the names are compared first, and Bob comes after Amy. {never} The one and the nine are never even compared. {bools} Even booleans have an order. True is greater than false.

[c2.eq.4] {member} So member can search all sorts of lists. {dog} Is dog a member of the list cat, dog? True. {nested} Is the list one, two a member of a list of two lists, the list three, and the list one, two? Also true. {whole} Each element is itself a list, and equality compares them whole. {safe} Integers, strings, booleans, and tuples or lists of them, all compare safely. {pause}

## Scene 6 · Where equality stops (ch2_s6_limits)

> Two definitions, names YELLOW, with OCaml's replies (types GREEN):
> `let double n = 2 * n` → `val double : int -> int = <fun>`
> `let twice n = n + n` → `val twice : int -> int = <fun>`
> On {same}, the two `int -> int` glow together. On {ask}: `double = twice`, a GOLD "?" held.
> On {checks}, a GREEN tag under it, "type-checks". On {raise}, the "?" becomes, in RED,
> `Exception: Invalid_argument "compare: functional value".`, with a RED tag "fails at run time".
> On {self}: `double = double` → the same RED exception.
> On {list}: `member double [twice; double]` → the same RED exception (the first comparison, double
> against twice, flashes). On {empty}: `member double []` → `- : bool = false` in GREEN, "no comparison".
> On {slogan}: L3 bonus's line as a small card, "Well-typed programs cannot go wrong. They might run
> forever, or raise an exception, but they never mix up their types", with "raise an exception" underlined YELLOW (and
> "run forever" underlined on {cycle}). On {later}, DIM "functions as values: a later lecture".
> On {loop}, no code (cyclic lists are not taught): a few BLUE cells in a ring, the last arrow curving
> back to the first; on {forever}, a YELLOW comparison pointer circles it and keeps circling, DIM
> "may never finish".
> On {contentious}: two columns, GREEN "small programs: easy" ({small}) and RED "large systems:
> dangerous" ({large}). On {explicit}, under the red one: "explicit compare functions (later, with
> higher-order functions)". On {fine}, GREEN "fine for us, for now".

[c2.lim.1] {limits} But polymorphic equality has its limits. {two} Here are two functions. Double of en is two times en, and twice of en is en plus en. {same} They have the same type, int to int, and they give the same answer for every number. {ask} So is double equal to twice? {pause=1.5}

[c2.lim.2] {checks} OCaml accepts the question, because both sides have the same type. {raise} But when it runs, it raises an exception. Invalid argument, compare, functional value. {nofun} Polymorphic equality refuses to compare functions at all. {self} Even double equals double fails, though it's the very same function.

[c2.lim.3] {inherit} Member inherits the problem. {list} Ask whether double is a member of the list twice, double, and you get the same exception. {empty} But ask whether double is a member of the empty list, and the answer is just false, because no comparison ever happens. {slogan} Notice that this is a run-time exception, not a type-checking error, just as lecture three promised. Well-typed programs cannot go wrong. They might run forever, or raise an exception, but they never mix up their types. {later} Functions as values come later in the course.

[c2.lim.4] {cycle} There's a second limit. {loop} A structure can loop back on itself, like a list whose last cell points back to its first. {forever} Comparing two of those may never finish, as OCaml goes round and round. {pause}

[c2.lim.5] {contentious} In fact, polymorphic equality is a contentious feature. {small} In small programs, it's easy. {large} In large systems, it becomes dangerous, and most large-scale users of OCaml avoid it in important code. {explicit} They write explicit compare functions instead, which you'll meet with higher-order functions, later on. {fine} For us, for now, it's just fine.

## Scene 7 · Recap (ch2_s7_recap)

> Recap: five short lines appear one per mark ({r1} to {r5}), each with a small icon from the
> chapter on its left: the chain with its GOLD pointer and "O(n)"; the halving row with "O(log n)" and
> the hash-table slot with "O(1)"; the `member` code in miniature with "iterative, O(1) space"; the
> five operators `=  <  <=  >  >=` with "by structure"; RED `Invalid_argument "compare: functional value"`
> beside the small ring of cells, "may never finish".
> Teaser on {next}: the recap dims, and ch3's phone book slides in as three ConsChain cells, each
> holding a tuple: `("Amy", 21)`, `("Bob", 35)`, `("Cleo", 47)` (names YELLOW, numbers GOLD, as ch3).
> On {phone}, the pairs split into two separate lists, `["Amy"; "Bob"; "Cleo"]` and `[21; 35; 47]`.
> Leave about 8 s of end card after the last word; the music carries it.

[c2.recap.1] {recap} Let's recap. {r1} Linear search compares the item with each element in turn, so it takes big O of en time. {r2} Data kept in order can be searched in big O of log en, and an index, like a hash table, can reach big O of one. {r3} Still, linear search is simple and general. On lists, it's member, which is iterative, so it needs only constant space. {r4} Member works at any type, thanks to polymorphic equality, which compares values by their structure. {r5} But equality raises an exception on functions, and may never finish on a structure that loops back on itself. {pause}

[c2.recap.2] {next} Next time, we'll look at lists of pairs. {phone} We'll pair up names with phone numbers, like a telephone directory, and then split the pairs apart again. {pause}
