# Chapter 5 · Strings, characters, and exercises

Lecture 3 (Lists), part 5 of 5. Source: FoCS 2026-27 notes, pp. 28–29 (§3.8, exercises 3.1–3.5).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*; see LESSONS.md, "Write for the ear"). `{mark}` is a cue
point; `{pause}` / `{pause=1.5}` is a deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch5_s1_hook)

> Title card: "Lists", "Foundations of Computer Science · Lecture 3", "Part 5: strings,
> characters, and exercises".
> Where strings show up, one beat each: a prompt "Name?" with a typed reply; a message line;
> `string_of_int 42` → `- : string = "42"` (a number becoming text, GOLD 42 → GREEN "42").
> Then the hook: the word `"cat"` as three letter boxes [c][a][t], with a dim, dashed
> ConsChain ghost underneath and a GOLD "?" between them. Leave the "?" up; don't answer yet.

[c5.hook.1] {title} This is the last part of our lecture on lists. {pause} We'll finish with strings and characters, {five} and then I'll hand you five exercises to try on your own.

[c5.hook.2] {why} First, why do we need strings at all? {text} Strings are how programs handle text. {users} And they're how a program talks to the people using it. Every prompt, every message, every answer on the screen. {numbers} Even a program that only crunches numbers has to turn its results into strings in the end, just so you can read them.

[c5.hook.3] {cat} Now, a string looks a lot like a list. {letters} It's a sequence of characters, in order. {ask} So here's a question. In OCaml, is a string secretly just a list of characters? {pause=1.5} {hold} Hold that thought. The answer says something about how OCaml thinks about types.

## Scene 2 · Characters and strings (ch5_s2_strings)

> Two columns, char on the left, string on the right. Quote marks in YELLOW, types in GREEN.
> Left: `'a'` → `- : char = 'a'`. Right: `"a"` → `- : string = "a"`, label "length 1";
> then `"abc"` → `- : string = "abc"`. Keep both columns up for the whole scene.
> Below: `String.length "abc"` → `- : int = 3`, a GOLD brace counting the three letters.
> Then `"abc" ^ "def"` → `- : string = "abcdef"`: the caret symbol flashes, the two strings
> slide together into one. A dim reminder beside it: `@` is for lists.

[c5.str.1] OCaml has two separate types for text. {char} The first is char, short for character. You write a character in single quotes. {letter} Put the letter A in single quotes, {reply} and OCaml tells you its type is char. {pause}

[c5.str.2] {string} The second type is string. You write a string in double quotes. {same} So the letter A in double quotes is not a character at all. It's a string, of length one. {pause} {abc} And A, B, C, in double quotes, is a string of length three.

[c5.str.3] {length} To find out how long a string is, use String dot length. {three} String dot length of A, B, C gives three. {pause} {caret} To join two strings together, use the caret symbol. {join} A, B, C, joined with D, E, F, gives a single string of six letters. {like} So the caret symbol does for strings what the at sign does for lists.

## Scene 3 · Strings are not lists (ch5_s3_notlists)

> Back to the hook's [c][a][t] with the GOLD "?": the dashed ConsChain ghost crosses out in RED,
> and the "?" turns into "its own type" (P23: the question becomes the answer).
> Two rejected inputs, RED, with OCaml's real error text:
> `"abc" @ "def"` → "Error: This constant has type string but an expression was expected of type 'a list"
> `'a' = "a"` → "Error: This constant has type string but an expression was expected of type char"
> Then the form of a character constant: `'c'` (quote, character, quote), and `','` →
> `- : char = ','`, the comma between the quotes scaled up so it's easy to see.

[c5.type.1] {back} So, back to our question. Is a string just a list of characters? {pause} {some} In a few programming languages, it really is. {no} But not in OCaml. {own} In OCaml, string is a separate type, unrelated to lists. {abstract} A string is an abstract idea in its own right, not a chain of cons cells.

[c5.type.2] {test} You can check this for yourself. {append} Try joining two strings with the at sign, the way you'd join two lists. {pause} {reject} OCaml rejects it. It expected a list, and it got a string.

[c5.type.3] {chars} The same goes for characters. {notstr} A character is not a string of length one. It's a primitive idea, built into the language. {compare} So what happens if you ask whether the character A equals the string A? {pause} {error} OCaml won't even run it. A char and a string are different types, so comparing them is a type error.

[c5.type.4] {form} Every character constant has the same simple form. {quotes} A single quote, the character itself, and another single quote. {comma} So the comma character is written as a comma, between two single quotes. {pause}

## Scene 4 · Escape sequences (ch5_s4_escapes)

> P23 puzzle: `"She said "hi""` with a GOLD "?". Underline in RED the part OCaml actually reads
> as the string, `"She said "`, so the inner quote ends it early. (Real reply, if shown:
> "Error: This expression has type string / This is not a function; it cannot be applied.")
> The fix: `"She said \"hi\""` → `- : string = "She said \"hi\""`, each backslash in YELLOW.
> Then `"\\"` labelled "a backslash". NB: the notes print the double-quote escape as `"\\"`,
> which is really the backslash escape. The double quote is `"\""` (checked: length 1).
> `"\n"`, then `String.length "\n"` → `- : int = 1`: two keystrokes, GOLD 1, one character.
> `"I\nLIKE\nCHEESE\n"` on top; below it `print_string "I\nLIKE\nCHEESE\n"` prints three lines,
> I / LIKE / CHEESE, each `\n` drawing an arrow down to the start of the next line.

[c5.esc.1] {puzzle} Here's a puzzle. Suppose you want a string with a double quote inside it. How would you type it? {pause} {problem} If you just type the quote, OCaml thinks the string ends right there.

[c5.esc.2] {escape} The fix is called an escape sequence, and it starts with a backslash. {special} Inside a string, a backslash means the next character is special. {quote} So backslash, double quote, stands for a double quote that doesn't end the string. {self} And to get a backslash itself, you type two backslashes in a row. {pause}

[c5.esc.3] {newline} The escape you'll use most is backslash en. It stands for a newline, a jump to the start of the next line. {keys} Notice that it's two symbols when you type it, {length} but String dot length says it's just a single character. {pause}

[c5.esc.4] {cheese} So look at this string. I, backslash en, like, backslash en, cheese, backslash en. {pause} {print} When you print it, it comes out as three separate lines of text. {lines} I. Like. Cheese.

## Scene 5 · Comparing strings (ch5_s5_order)

> The four operators in a row: `<  <=  >  >=`. Then `"apple" < "banana"` → `- : bool = true`.
> The rule, P2 (whole shape, then walk it): two strings stacked, a YELLOW box sliding letter by
> letter to the first difference. `"app" < "apple"` → `- : bool = true`: the shorter string
> runs out first. Caption, then keep it: "lexicographic order".
> Code table (from `Char.code`), GOLD numbers: 'A' 65 … 'Z' 90 | 'a' 97 … 'z' 122, with a gap.
> P23 surprise: `"Zebra" < "apple"`, GOLD "?", hold, then the "?" becomes `- : bool = true`;
> the box sits on Z (90) vs a (97).

[c5.cmp.1] {ops} Strings can also be compared. {four} The usual operators all work. Less than, less than or equal, greater than, and greater than or equal. {apple} So, is apple less than banana? {pause} {yes} Yes. Apple comes first in the dictionary, so it counts as smaller.

[c5.cmp.2] {rule} The rule works character by character. {first} Compare the first characters. If they're different, that settles it. {same} If they're the same, move on to the next pair, and so on. {prefix} And if a string runs out first, that string is smaller. So app comes before apple. {pause} {name} This is called lexicographic order.

[c5.cmp.3] {codes} But there's a catch. Every character has a number, called its ASCII code. {upper} The capital letters have codes sixty-five to ninety. {lower} The lowercase letters start at ninety-seven. {bycode} And strings are compared by those codes, not by the dictionary.

[c5.cmp.4] {zebra} So which comes first? Zebra, with a capital Z, or apple, all in lowercase? {pause=1.5} {answer} OCaml says zebra is smaller. {why} Capital Z is ninety, and lowercase A is ninety-seven. {every} In fact, every capital letter comes before every lowercase letter. {careful} So if you ever sort words this way, watch out for capitals.

## Scene 6 · Exercises: sum and last (ch5_s6_sumlast)

> "Exercises" header; five dim cards 3.1–3.5 in a row, and a small note "solutions: bonus
> chapter". Each card in turn grows to the hero position, and shrinks back when done.
> Every card: the task in a sentence, its example in Code, a GOLD "?" where the answer would go
> (never a solution). The hint fades in beneath. On each {pause=2} the screen is still, with a
> small "pause and try it" label.
> Card 3.1: `sum [1; 2; 3; 4]` ⇒ `10`, target type `int list -> int`; two tags, "recursive",
> then "iterative". Hint: chapter 3's `nlength` and `addlen` side by side (dimmed code), the
> count in addlen highlighted as "running total".
> Card 3.2: `last [3; 5; 9]` ⇒ `9`, type `'a list -> 'a`, tag "non-empty lists only".
> Hint: chapter 1's ConsChain 3 → 5 → 9 → [], a YELLOW marker walking the arrows; GOLD
> "how efficiently?". The last cell (the one pointing at nil) gets a GOLD "?".

[c5.ex.1] {turn} Now it's your turn. {five} The notes end with five exercises, and they're exactly the kind of thing you'll meet in supervisions. {plan} For each exercise, I'll state it, give you a single hint, and then pause, so you can stop the video and try it. {bonus} There are no solutions here. The worked solutions are in a bonus chapter, for after you've had a go.

[c5.ex.2] {sum} Exercise three point one. {task} Write a function that adds up the elements of a list of integers. {example} The sum of one, two, three, four is ten. {twice} Write it twice. First recursively, and then iteratively. {comment} Then comment on how much the iterative version improves the efficiency.

[c5.ex.3] {hint} Here's the hint. {nlength} The recursive version has the same shape as en-length, from chapter three. {addlen} The iterative version carries a running total, the way add-len carried a count. {space} So when you compare them, think about space. {try} Pause the video, and try it. {pause=2}

[c5.ex.4] {last} Exercise three point two. {task} Write a function that returns the last element of a list. {nine} The last element of three, five, nine is nine. {nonempty} You can assume the list has at least one element. {how} And the real question is, how efficiently can this be done? {pause}

[c5.ex.5] {hint} The hint comes from chapter one. {walk} There's no shortcut to the end of a list. You have to follow the arrows, cell by cell. {stop} So ask yourself this. Which pattern tells you that you've reached the last cell? {try} Pause, and give it a go. {pause=2}

## Scene 7 · Exercises: even elements, and two strange types (ch5_s7_evensid)

> Card 3.3: `[a; b; c; d]` ⇒ `[b; d]` as in the notes, positions 1 2 3 4 numbered small above,
> 2 and 4 in GOLD. Second example: `[1; 2; 3; 4; 5]` ⇒ `[2; 4]`. Type `'a list -> 'a list`.
> Hint: the pattern `x :: y :: rest`, braces "first", "second", "the rest" dropping onto it.
> Card 3.4, as in the notes: `let id x = x` → `val id : 'a -> 'a = <fun>`, and
> `let rec loop x = loop x` → `val loop : 'a -> 'b = <fun>` ('a and 'b in PINK).
> Then the two expressions, `id [id [id 0]]` and `loop true / loop 3`, each with a GOLD "?" for
> its type. Do NOT show their types or values. Small label: "/ is integer division".
> Hint: the three `id`s each get their own PINK 'a (different shades); an arrow from inside out.

[c5.ex.6] {evens} Exercise three point three. {task} Write a function that returns the even-numbered elements of a list. {example} Given A, B, C, D, it should return B, D. {count} Counting from the front, that's the second element and the fourth. {odd} And given one, two, three, four, five, you'd get two and four. {pause}

[c5.ex.7] {hint} Here's the hint. {front} So far, our patterns have taken a single element off the front. {deeper} But a pattern can take two at once. Ex, cons why, cons the rest. {left} Then ask what to do with the short lists that pattern doesn't match. {try} Pause, and try it. {pause=2}

[c5.ex.8] {types} Exercise three point four is different. It's about types. {id} Here's a function called eye-dee, short for identity. It just hands back its argument. {idtype} Its type is alpha to alpha. {loop} And here's a function called loop, which calls itself, forever. {looptype} Its type is alpha to beta. {pause}

[c5.ex.9] {job} Your job is to explain why these types make sense, and why they can never lead to a type error at run time. {nest} Even for strange expressions, like eye-dee, applied to a list containing eye-dee, applied to a list containing eye-dee of zero. {div} Or loop true, divided by loop three. The slash here is integer division. {pause}

[c5.ex.10] {hint} The hint goes back to chapter two. {fresh} Alpha can stand for any type, and each use of eye-dee gets to choose its own. So work from the inside out. {ever} And for loop, ask yourself a simple question. Does it ever actually return? {try} Pause, and think it through. {pause=2}

## Scene 8 · Tails, and the whole lecture (ch5_s8_tails)

> Card 3.5: `tails [1; 2; 3]` ⇒ `[[1; 2; 3]; [2; 3]; [3]; []]`, type `'a list -> 'a list list`.
> The four results appear one per beat as the narration lists them.
> Hint: chapter 1's ConsChain 1 → 2 → 3 → []; a TEAL brace boxes each tail in turn: the whole
> list, then from 2, then from 3, then nil. No code. Bonus question in GOLD: "new cells?".
> Recap: clear the cards. Five short lines in a column, one per beat, each with a small icon:
> a cons cell; the pattern `x :: xs`; PINK 'a; an accumulator; GOLD O(n²) → O(n) beside
> `nrev` / `rev_app`; and `"abc"` with "not a list". Closing card: "Solutions: bonus chapter".

[c5.ex.11] {tails} The last exercise is three point five. {task} Write a function called tails, which returns the list of all the tails of its argument. {example} Given one, two, three, it returns four lists. {whole} First, the whole list, one, two, three. {two} Then two, three. {three} Then the list containing just three. {nil} And finally, nil. {pause}

[c5.ex.12] {hint} The hint is in chapter one. {walk} Remember taking the tail, then the tail of that, all the way down to nil? {same} That walk visits exactly these lists. {share} And here's a bonus question to think about. How many new cons cells does your answer really need to build? {try} Pause, and try it. {pause=2}

[c5.recap.1] {recap} That's the end of lecture three, so let's look back at the big ideas. {r1} Every list is either nil, or a head consed onto a tail, and cons takes constant time. {r2} Pattern matching takes lists apart, with a case for each shape. {r3} Polymorphic types, with alpha and beta, let a single function work on lists of any type. {pause}

[c5.recap.2] {r4} An accumulating argument makes a function iterative, so it runs in constant space. {r5} Append copies its whole first list, so the naive reverse costs big O of en squared. {r6} Replacing append with cons brings that down to big O of en. That's called reduction in strength. {r7} And in OCaml, strings and characters are types of their own, not lists. {pause}

[c5.recap.3] {next} Now, try those five exercises yourself. {bonus} When you're ready, the bonus chapter walks through every solution, step by step. {pause} {bye} See you there.
