# Chapter 3 · Lists of pairs: zip and unzip

Lecture 4 (More on Lists), part 3 of 7. Source: FoCS 2026-27 notes v1.8, pp. 32–33 (§4.4–4.5).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch3_s1_hook)

> Title card, `title_card("Part 3 · Lists of pairs: zip and unzip")`: "More on Lists", "Foundations of Computer Science · Lecture 4", "Part 3 · Lists of pairs: zip and unzip". It holds through the "last time" sentence.
> Running example for the whole chapter (s1–s8): the phone book, names `["Amy"; "Bob"; "Cleo"]` with numbers `[21; 35; 47]`. Palette as L3: function names YELLOW in definitions, types GREEN, `'a` PINK, `'b` PURPLE (L3 ch2's fst colours), nil and `::` TEAL, numbers GOLD.
> Hero, centre: two Code lists stacked, `["Amy"; "Bob"; "Cleo"]` above `[21; 35; 47]`, elements aligned in three columns (names YELLOW on {names}, numbers GOLD on {numbers}). On {match}, thin DIM lines join each column: first with first, second with second.
> On {pair}, each name and its number slide together (TransformFromCopy) into one list below: `[("Amy", 21); ("Bob", 35); ("Cleo", 47)]`. On {split}, a GOLD "?" and an arrow pointing back up from the pairs to the two lists.
> On {general}, the specific lists dim and the notes' picture appears as MathTex: `[x_1, \ldots, x_n]` over `[y_1, \ldots, y_n]`, a right brace, `\longmapsto [(x_1, y_1), \ldots, (x_n, y_n)]`.
> On {zipname}, YELLOW "zip" over the rightward arrow; on {unzipname}, YELLOW "unzip" under a leftward arrow. Clear to empty.
> Every value shown in this chapter was checked in OCaml 5.4.1.

[c3.hook.1] {title} Last time, we searched a list with member, and saw which values OCaml's equality can compare. {book} This time, we start with a tiny phone book. {names} Three names, Amy, Bob and Cleo, {numbers} and their phone numbers, short office extensions, twenty-one, thirty-five and forty-seven. {match} The two lists are in matching order, so Amy goes with twenty-one, Bob with thirty-five, and Cleo with forty-seven.

[c3.hook.2] {pair} How do you pair them up, into one list of name and number pairs? {pause} {split} And given a list of pairs, how do you split it back into two lists? {pause} {general} In general, we want to turn a list of exes and a list of whys into one list of pairs, and back again. {zipname} The two functions are called zip, {unzipname} and unzip.

## Scene 2 · Zip (ch3_s2_zip)

> Hero Code, large and centred, `zip` YELLOW:
> `let rec zip xs ys =` / `  match xs, ys with` / `  | (x::xs, y::ys) -> (x, y) :: zip xs ys` / `  | _ -> []`
> On {match}, FlashUnder on `match xs, ys with`, small label "a pair, as in append" (L3 ch4). One highlight box slides clause to clause: `(x::xs, y::ys)` on {first}, with braces "head, tail" under `x::xs` and `y::ys`; on {fresh}, the pattern's `xs` and `ys` turn TEAL with a DIM tag "the tails: new names".
> On {result}, `(x, y)` is built from copies of the pattern's `x` and `y` (TransformFromCopy); `zip xs ys` boxed as "the smaller problem". `::` TEAL.
> On {wild}, the box slides to `_`, which glows YELLOW; label "wildcard: matches anything". On {empty}, the clause's `[]` in TEAL.
> On {var}, `_` morphs into `p` and the reply below stays the same (checked: OCaml accepts it with no warning); on {ignore}, it morphs back to `_`, label "this clause ignores its argument".
> On {type}, OCaml's reply under the code: `val zip : 'a list -> 'b list -> ('a * 'b) list = <fun>`, type GREEN, each `'a` PINK and each `'b` PURPLE. Braces on {args} under `'a list -> 'b list` ("two lists") and on {out} under `('a * 'b) list` ("a list of pairs").
> On {two}, a small DIM inset of L3 ch2's fst reply `- : 'a * 'b -> 'a = <fun>`. On {fill}, `string` slides onto every `'a` and `int` onto every `'b` (L3's substitution move), then the type snaps back. Clear to empty.
> Code and reply checked in OCaml 5.4.1 (the `p` version too).

[c3.zip.1] {code} Here's zip. It takes two lists, exes and whys. {match} As with the append function, we match the pair, exes comma whys, so each pattern looks at both lists at once. {first} The first pattern needs both lists to have a head, ex on one side and why on the other. {fresh} As before, exes and whys in the pattern are new names, for the two tails.

[c3.zip.2] {result} Then the answer is the pair, ex comma why, consed onto the zip of the two tails. {pause} {wild} The second pattern is a single underscore. That's called the wildcard, and it matches anything at all. {empty} Whatever arrives there, the answer is nil. {var} We could have written a variable name instead of the underscore, and zip would work just the same. {ignore} But the wildcard tells the reader something useful. This clause ignores its argument. {pause}

[c3.zip.3] {type} Now look at OCaml's reply. {args} Zip takes an alpha list, and a beta list, {out} and returns a list of pairs, alpha times beta. {two} There are two type variables, just as for the built-in function that takes the first part of a pair. The two lists can hold different types. {fill} Our names are strings and our numbers are ints, so for the phone book, alpha is string, and beta is int.

## Scene 3 · Uneven lists, and clause order (ch3_s3_order)

> s2's code shrinks to the top-right corner and stays. Trace as stacked lines, each born from a copy of the line above (L3 ch4's append trace style), first step slow, the rest faster:
> `zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47]` / `⇒ ("Amy", 21) :: zip ["Bob"; "Cleo"] [35; 47]` / `⇒ ("Amy", 21) :: ("Bob", 35) :: zip ["Cleo"] [47]` / `⇒ ("Amy", 21) :: ("Bob", 35) :: ("Cleo", 47) :: zip [] []` / `⇒ ("Amy", 21) :: ("Bob", 35) :: ("Cleo", 47) :: []` / `⇒ [("Amy", 21); ("Bob", 35); ("Cleo", 47)]`
> One line per mark, {s1} to {s4}. The waiting `("Amy", 21) ::` etc. turn YELLOW and stay. On {s4}, the corner code's `_ -> []` lights up and `zip [] []` becomes TEAL `[]`. On {done}, the conses fire; on {answer}, the result as three ConsChain cells holding tuples, with OCaml's reply `- : (string * int) list = [("Amy", 21); ("Bob", 35); ("Cleo", 47)]`.
> On {uneven}, clear the trace. On {short}: `zip ["Amy"; "Bob"; "Cleo"] [21; 35]` / `⇒ ("Amy", 21) :: ("Bob", 35) :: zip ["Cleo"] []`. On {catch}, the corner's first pattern gets a RED cross (no second head) and `_ -> []` lights up. On {drop}, `"Cleo"` turns RED and fades, label "dropped". Reply `- : (string * int) list = [("Amy", 21); ("Bob", 35)]`. On {surplus}, beside it `zip ["Amy"; "Bob"] [21; 35; 47]`, same reply, with `47` dropped.
> On {order}, the corner code returns to the centre with small GOLD tags "1st" and "2nd" by the clauses; on {tried}, an arrow tries "1st", then falls through to "2nd". On {sees}, a label by `_`: "at least one list is empty".
> On {swap}, the two clauses swap places (RED): `let rec zip xs ys =` / `  match xs, ys with` / `  | _ -> []` / `  | (x::xs, y::ys) -> (x, y) :: zip xs ys`. On {warn}, OCaml's full reply, in a YELLOW-stroked box (as L3 ch2's warning; the three location lines may be dropped, as there):
> `Line 4, characters 4-18:` / `4 |   | (x::xs, y::ys) -> (x, y) :: zip xs ys;;` / `        ^^^^^^^^^^^^^^` / `Warning 11 [redundant-case]: this match case is unused.` / (blank line) / `val zip : 'a list -> 'b list -> ('a * 'b) list = <fun>`
> On {never}, the second clause DIMs. On {nil}, `zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47]` with reply `- : (string * int) list = []` in RED. On {rule}, a YELLOW line: "specific patterns first, catch-all last". Clear to empty.
> Every trace line, reply and the warning were checked in OCaml 5.4.1.

[c3.order.1] {trace} Let's zip our phone book. {s1} Both lists have a head, so Amy pairs with twenty-one, and we zip the rest. {s2} Then Bob with thirty-five, {s3} and Cleo with forty-seven. {s4} Now both lists are empty. The first pattern fails, so the wildcard takes over, and gives nil. {done} As in append, the conses were waiting, and now they all happen. {answer} Three pairs, in order.

[c3.order.2] {uneven} But what if the lists have different lengths? {pause} {short} Suppose Cleo has no number yet, so we zip three names with only two numbers. Amy and Bob pair up as before. {catch} That leaves the list holding Cleo, and nil. The first pattern needs two heads, so the wildcard returns nil. {drop} Cleo is simply dropped. {surplus} Zip discards any surplus at the end of the longer list, whichever list that is.

[c3.order.3] {order} Now, the wildcard matches every argument, not just empty lists. So how does the first clause ever get a turn? {pause} {tried} Because OCaml tries the clauses in order. The first pattern is tried first, and the wildcard only when that fails. {sees} So the wildcard only ever sees arguments where at least one list is empty.

[c3.order.4] {swap} That makes the order matter. Put the wildcard first, {warn} and OCaml warns you, with warning eleven. This match case is unused. {pause} {never} The wildcard now catches every call, so the second clause can never run. {nil} Zip still has the same type, but it returns nil for everything. {rule} So put the specific patterns first, and the catch-all pattern at the end.

## Scene 4 · What pairs are for (ch3_s4_pairs)

> On {book}, `let book = zip ["Amy"; "Bob"; "Cleo"] [21; 35; 47]` with reply `val book : (string * int) list = [("Amy", 21); ("Bob", 35); ("Cleo", 47)]`; `book` YELLOW. On {cells}, below it, the same three ConsChain tuple cells as s3's answer, labelled `book` (s5–s8 reuse this name).
> On {assoc}, the notes' MathTex `[(x_1, y_1), \ldots, (x_n, y_n)]` above, with a small two-way arrow inside each pair; in the cells, names YELLOW, numbers GOLD. A DIM tag "a telephone directory".
> On {find}, a YELLOW query tag `"Cleo"` and a GOLD pointer walking from the front, comparing only the name part: RED cross at Amy, RED cross at Bob; on {found}, a GREEN tick at Cleo and `47` lifts out in GOLD.
> On {back}, a second query, GOLD `35`; the pointer compares the number parts: cross at 21, tick at 35; on {bob}, `"Bob"` lifts out.
> On {slow}, a small DIM "linear search (last time)". On {big}, the chain stretches to "a million pairs" (… and a brace), with a GOLD counter "up to 1,000,000 comparisons" and RED "very slowly".
> On {square}, clear the chain; `[1; 2; 3]` above, arrows down from each element, then `[(1, 1); (2, 4); (3, 9)]` built from copies, with a label "each number, with its square" (a value only, no code; checked in OCaml 5.4.1, like `book`'s reply). On {later}, DIM "how to write it: a later lecture". Clear to empty.

[c3.pairs.1] {book} Let's give our phone book a name, book. {cells} In memory, it's a list, and each of its cells holds a pair. {assoc} A list of pairs like this associates each first part with its second part. Here, each name with its number, just like a telephone directory.

[c3.pairs.2] {find} To find Cleo's number, search from the front, comparing names. {found} Not Amy, not Bob, but Cleo, so the number is forty-seven. {back} You can also go the other way. To find whose number is thirty-five, compare the numbers instead, {bob} and you reach Bob.

[c3.pairs.3] {slow} That's linear search from last time. It works, but very slowly. {big} A phone book with a million names could take a million comparisons. {square} Pairs can also come from applying a function to each element of another list, for instance, pairing each number with its square. {later} You'll see how to write that in a later lecture.

## Scene 5 · Unzip: two results at once (ch3_s5_unzip)

> On {split}, s4's `book` list `[("Amy", 21); ("Bob", 35); ("Cleo", 47)]` comes apart into `["Amy"; "Bob"; "Cleo"]` and `[21; 35; 47]` (s1's animation, run backwards). On {problem}, a box "unzip pairs" hands back `(?, ?)`, both "?" GOLD.
> On {code}, hero Code, `unzip` YELLOW: `let rec unzip = function` / `  | [] -> ([], [])` / `  | (x, y)::pairs ->` / `      let xs, ys = unzip pairs in` / `      (x::xs, y::ys)`, with reply `val unzip : ('a * 'b) list -> 'a list * 'b list = <fun>` (type GREEN, `'a` PINK, `'b` PURPLE). A highlight box slides: `[] -> ([], [])` on {base}, `(x, y)::pairs` on {step}, the let line on {let}, `(x::xs, y::ys)` on {cons} (x flies onto xs, y onto ys, `::` TEAL). On {func}, the word `function` flashes, DIM tag "the list: an unnamed argument (as in take)".
> On {refresh}, the code dims and slides left; a side panel: `let half = 21 in half + half` with reply `- : int = 42` (on {half} and {value}); on {brackets}, `1 + (let half = 21 in half + half)` with reply `- : int = 43`, the brackets flashing.
> On {new}, the panel clears; `let P = E` with P YELLOW, E BLUE, label "match P against E's value, bind every variable in P". On {demo}, `let name, number = ("Amy", 21);;` with OCaml's two-line reply `val name : string = "Amy"` / `val number : int = 21`; on {both}, arrows from `name` to `"Amy"` and from `number` to `21`. On {here}, the unzip code returns and its let line glows.
> On {trace}, the code moves to the top. A down-and-up ladder: calls down the left (each from a copy of the one above), `unzip book` / `unzip [("Bob", 35); ("Cleo", 47)]` / `unzip [("Cleo", 47)]` / `unzip []`, each DIM-tagged "waiting".
> On {nil}, `([], [])` in TEAL beside the bottom call. Results climb the right side, one per mark ({up1}, {up2}, {up3}), each new name YELLOW and number GOLD consed on: `(["Cleo"], [47])` / `(["Bob"; "Cleo"], [35; 47])` / `(["Amy"; "Bob"; "Cleo"], [21; 35; 47])`. On {result}, the reply `- : string list * int list = (["Amy"; "Bob"; "Cleo"], [21; 35; 47])`. Clear to empty.
> Code, the let examples and every rung of the ladder were checked in OCaml 5.4.1.

[c3.unzip.1] {split} Now the other direction. Unzip takes a list of pairs, and splits it into two lists, the first parts and the second parts. {two} So it has to build two results at once, which is awkward with recursion. {problem} The recursive call hands back a pair of lists, and we need to get at both of them. {pause}

[c3.unzip.2] {code} Here's the definition. {base} Unzip of nil is a pair of empty lists. {step} For a list whose head is the pair, ex comma why, {let} let exes comma whys equal the unzip of the rest. {cons} Then ex is consed onto exes, and why onto whys, and we return the two lists as a pair. {func} As with take, the word function supplies the list as an argument with no name.

[c3.unzip.3] {refresh} That let deserves a closer look. You met let in lecture two. {half} For example, let half equal twenty-one, in the expression half plus half. {value} It computes twenty-one, calls it half inside the second part, and gives forty-two. {expr} The whole let is an expression, so it can go wherever an expression goes, {brackets} wrapped in brackets if needed. Add one to it, and you get forty-three.

[c3.unzip.4] {new} What's new is the left-hand side. {pattern} In general, when you write let, a pattern, equals, an expression, OCaml matches the pattern against the expression's value, and binds every variable in the pattern. {demo} Let name comma number equal Amy comma twenty-one, {both} and OCaml binds both at once. {here} In unzip, one let catches both results of the recursive call, as exes and whys. {pause}

[c3.unzip.5] {trace} Let's unzip our phone book. {down} Each call takes off one pair, and leaves work waiting. {nil} At the bottom, unzip of nil gives two empty lists. {up1} On the way back, Cleo goes onto the names, and forty-seven onto the numbers. {up2} Then Bob and thirty-five, {up3} then Amy and twenty-one. {result} Out come the names, Amy, Bob, Cleo, and the numbers, twenty-one, thirty-five, forty-seven. {pause}

## Scene 6 · Mirror images (ch3_s6_types)

> The two replies stacked, aligned on the colon, as the notes show them (In [66], In [67], typed as bare `zip;;` and `unzip;;`): `- : 'a list -> 'b list -> ('a * 'b) list = <fun>` labelled YELLOW `zip`, and `- : ('a * 'b) list -> 'a list * 'b list = <fun>` labelled YELLOW `unzip`. Types GREEN, `'a` PINK, `'b` PURPLE.
> On {zip}, braces under zip's type: "two lists" → "a list of pairs". On {unzip}, under unzip's: "a list of pairs" → "a pair of lists". On {mirror}, a curved arrow links the two `('a * 'b) list` parts; `->` between zip's two lists flashes ("one after the other") and `*` in unzip's result flashes ("together, as a pair").
> On {undo}, the types move up. On {cut}: `unzip (zip ["Amy"; "Bob"; "Cleo"] [21; 35])` with reply `- : string list * int list = (["Amy"; "Bob"], [21; 35])`; on {gone}, a RED ghost of `"Cleo"` fades from beside it, label "gone for good".
> On {other}, below: `let xs, ys = unzip book in zip xs ys` with reply `- : (string * int) list = [("Amy", 21); ("Bob", 35); ("Cleo", 47)]` and a GREEN tick, "back where you started". On {equal}, braces of equal length under the two halves, GOLD "3" and "3". Clear to empty.
> All replies checked in OCaml 5.4.1.

[c3.types.1] {side} Now put the two types side by side. {zip} Zip takes two lists, and gives a list of pairs. {unzip} Unzip takes a list of pairs, and gives a pair of lists. {mirror} They're almost mirror images. Zip takes its two lists one after the other, and unzip hands them back together, as a pair. The types say exactly what the functions do.

[c3.types.2] {undo} So unzip can undo zip, with one catch. {cut} Zip three names with two numbers, and Cleo is dropped. Unzip that, and you get Amy and Bob, with twenty-one and thirty-five. {gone} Cleo is gone for good. {pause}

[c3.types.3] {other} The other way round always works. Unzip a list of pairs, zip the two halves, and you're back where you started. {equal} Unzip always gives two lists of the same length, so zip has nothing to drop.

## Scene 7 · Without the let (ch3_s7_conspair)

> On {helper}, Code: `let conspair ((x, y), (xs, ys)) = (x::xs, y::ys)`, `conspair` YELLOW. Nested braces under the argument: on {outer} "a pair" under `(x, y)`, on {inner} "a pair of lists" under `(xs, ys)`, and an outer brace "one argument: a pair of pairs". On {body}, `x` flies onto `xs` and `y` onto `ys` (TransformFromCopy), `::` TEAL.
> On {reply}, OCaml's reply on its own line, with room to breathe: `val conspair : ('a * 'b) * ('a list * 'b list) -> 'a list * 'b list = <fun>` (type GREEN, `'a` PINK, `'b` PURPLE). Braces on {in} under `('a * 'b) * ('a list * 'b list)` ("in") and on {out} under the last `'a list * 'b list` ("out"). On {lineup}, thin lines join `('a * 'b)` to `(x, y)` and `('a list * 'b list)` to `(xs, ys)`.
> On {last}, `conspair (("Cleo", 47), ([], []))` with reply `- : string list * int list = (["Cleo"], [47])`, and a small DIM inset of s5's ladder with its first step up highlighted.
> On {new}, s5's unzip appears at the left, DIM; its let lines morph into the new clause (TransformMatchingTex energy), giving `let rec unzip = function` / `  | [] -> ([], [])` / `  | xy :: pairs -> conspair (xy, unzip pairs)`. Highlight `[] -> ([], [])` on {base}, `xy` on {step} (tag "not taken apart"), `conspair (xy, unzip pairs)` on {call}.
> On {same}, reply `val unzip : ('a * 'b) list -> 'a list * 'b list = <fun>`, identical to s5's (flash both to show they match), and `unzip book` with reply `- : string list * int list = (["Amy"; "Bob"; "Cleo"], [21; 35; 47])`. On {but}, the s5 let line `let xs, ys = unzip pairs in` returns in YELLOW: "worth knowing". Clear to empty.
> Both definitions, replies and the conspair example were checked in OCaml 5.4.1.

[c3.cons.1] {without} Can we write unzip without the let? {pause} {helper} Here's a helper function, called cons-pair. Its argument is a pattern, written right in the definition. {outer} It's a pair, whose first part is a pair, ex comma why, {inner} and whose second part is a pair of lists, exes comma whys. {body} Cons-pair conses ex onto exes, and why onto whys.

[c3.cons.2] {reply} Its type is quite a mouthful, so let's take it slowly. {pause} {in} It takes an alpha times beta, paired with an alpha list times a beta list. {out} And it returns an alpha list times a beta list. {lineup} Each part of the type matches a part of the pattern. {last} Give it Cleo's pair and two empty lists, and you get the list holding Cleo, and the list holding forty-seven. That's the first step back up our trace.

[c3.cons.3] {new} Now unzip needs no let. {base} On nil, it still gives two empty lists. {step} Otherwise, call the head ex-why, without taking it apart, {call} and hand it to cons-pair, along with the unzip of the rest. {same} OCaml gives the same type as before. It's the same computation, and possibly clearer. {but} But not every local binding can be removed so easily, so let with a pattern is well worth knowing.

## Scene 8 · Iterative, and backwards (ch3_s8_revunzip)

> On {waiting}, s7's two unzips side by side, small, with DIM "waiting" tags on the cons step. On {acc}, hero Code, `revUnzip` YELLOW: `let rec revUnzip = function` / `  | ([], xs, ys) -> (xs, ys)` / `  | ((x, y)::pairs, xs, ys) ->` / `      revUnzip (pairs, x::xs, y::ys)`. OCaml's reply, keeping its line break exactly: `val revUnzip : ('a * 'b) list * 'a list * 'b list -> 'a list * 'b list =` / `  <fun>`.
> On {triple}, braces under the triple: "pairs to do", "xs so far", "ys so far" (the accumulators TEAL). On {base}, box `([], xs, ys) -> (xs, ys)`; on {step}, box the second clause. On {many}, the three argument slots pulse one by one.
> On {trace}, L3 ch4's rev_app card piles, three of them: a pile of pair cards (Amy's card on top, then Bob's, then Cleo's) and two empty piles, names and numbers. Beside them, one line per move, each from a copy of the line above: `revUnzip ([("Amy", 21); ("Bob", 35); ("Cleo", 47)], [], [])` / `⇒ revUnzip ([("Bob", 35); ("Cleo", 47)], ["Amy"], [21])` / `⇒ revUnzip ([("Cleo", 47)], ["Bob"; "Amy"], [35; 21])` / `⇒ revUnzip ([], ["Cleo"; "Bob"; "Amy"], [47; 35; 21])` / `⇒ (["Cleo"; "Bob"; "Amy"], [47; 35; 21])`. On {t1}, {t2}, {t3}, the top pair card splits and its halves land on the two piles. On {flat}, DIM "iterative". On {done}, the reply `- : string list * int list = (["Cleo"; "Bob"; "Amy"], [47; 35; 21])`; on {backwards}, both lists turn RED.
> On {fix}, `revUnzip (List.rev book, [], [])` with reply `- : string list * int list = (["Amy"; "Bob"; "Cleo"], [21; 35; 47])` in GREEN. On {copy}, `List.rev book` boxed GOLD, with its value `[("Cleo", 47); ("Bob", 35); ("Amy", 21)]` drawn as three new cells, GOLD "+ one cell per pair, + one pass". On {total}, "revUnzip + reversal" vs "unzip", with a GOLD "probably more" on the first. On {rule}, L3 ch4's caveat as a YELLOW line: "an accumulator that forces an extra reversal can lose".
> Recap, one short line per idea, each appearing on its mark ({r1} … {r5}): "zip pairs up two lists, drops the surplus" / "_ matches anything; clauses tried in order, so it goes last" / "a list of pairs: a directory, searched one pair at a time" / "unzip: two results at once, with let and a pattern" / "conspair: no let; revUnzip: iterative, but backwards".
> On {next}, the recap dims; teaser for ch4: a row of GOLD coin discs 50, 20, 10, 5, 2, 1 (ch4's coins) beside a till, and "making change". Hold the end card about eight seconds after the last word (music carries it), then clear to empty.
> Code, its two-line reply and every trace line were checked in OCaml 5.4.1.

[c3.rev.1] {waiting} Both versions of unzip leave work waiting on the way back, so neither is iterative. {acc} Making it iterative gives this function, rev-unzip. {triple} It takes a triple, made of the remaining pairs, and two accumulators, exes and whys. {base} When the pairs are used up, it returns the two accumulators. {step} Otherwise, it conses ex onto exes, and why onto whys, and carries on with the rest. {many} Iteration can build several results at once, each in its own argument position.

[c3.rev.2] {trace} Let's run it on the phone book, starting with two empty lists. {t1} Amy and twenty-one move across. {t2} Then Bob and thirty-five, on top. {t3} Then Cleo and forty-seven. {flat} Nothing piles up, because each call just hands over to the next. {done} The pairs are used up, so we return the two lists. {pause} {backwards} Cleo, Bob, Amy. Both lists come out backwards.

[c3.rev.3] {why} That's the accumulators at work. Like rev-app, they build by consing onto the front. {fix} To fix it, reverse the input first. {copy} But that reversal copies the whole list of pairs, which costs one extra pass, and one new cell for each pair. {total} So in total, rev-unzip will probably cost more than plain unzip, despite being iterative. {rule} It's the warning from lecture three again. An accumulator that forces an extra reversal can lose.

[c3.rev.4] {recap} Let's recap. {r1} Zip pairs up two lists, and drops the surplus of the longer one. {r2} The wildcard matches anything, and since clauses are tried in order, it goes last. {r3} A list of pairs makes a simple directory, searched one pair at a time. {r4} Unzip builds two results at once, by matching the recursive call's answer with a let and a pattern. {r5} Cons-pair does the same without the let, and rev-unzip does it iteratively, but backwards. {pause} {next} Next time, we put lists to work, with a till full of coins, and a program that makes change.
