# Chapter 2 · When are two states the same?

Digital Electronics, Lecture 11 (State Minimisation, Programmable Logic and Circuits), part 2 of 6. Source: slides `combined_26.pdf` pp. 148 (State Equivalence)–152 (Implication Table, through the A-G cell); recording 00:11:57–00:20:42.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch2_s1_hook)

> {title}: title card, scaled to 12 units wide as in ch1: "State Minimisation, Programmable Logic and Circuits", "Digital Electronics · Lecture 11", "Part 2 · When are two states the same?". ch1's conventions hold all chapter: state letters FG; input X BLUE; output Y GREEN (a 1 bright GREEN, 0s FG); GOLD means "the same"; ≡ is "is equivalent to", ≢ "is not equivalent to"; implication-table crosses are RED diagonals across the whole cell, never a letter X. No code on screen: every table, run, cell, implied pair and count in this chapter was checked by exhaustive enumeration (Python 3.11.9, itertools.product).
> {last}: ch1 s6's moment, small, upper left: ch1's compact table (header "Current State | Next State X=0 X=1 | Output (Y) X=0 X=1") with rows D and G, both "H H 0 0", glowing GOLD. {merged}: ch1's merge animation: the G in row C's X = 1 entry flashes GOLD and becomes D, then row G goes DIM and leaves. The small table clears.
> {table}: hero, left half: p. 150's table, header verbatim "Present State | Next State X=0 X=1 | Output (Y)" (X BLUE, Y GREEN); rows A: D C 0 · B: F H 0 · C: E D 1 · D: A E 0 · E: C A 1 · F: F B 1 · G: B H 0 · H: C G 1 (1s bright GREEN). This table stays on screen, in this styling, through s7.
> {nomatch}: a row-matching sweep, as in ch1: each row in turn is compared with the rows below it; nothing lights GOLD. A small DIM line under the table: "no two rows identical" (checked).
> {run}: right half, two lanes labelled "start in A" and "start in D"; the inputs 0, 1, 1, 0 (BLUE) along the top. Rows A and D box YELLOW. Step by step, each lane grows a chain of small state circles joined by arrows labelled with the input: lane A visits A, D, E, A, D; lane D visits D, A, C, D, A (checked). Each circle's output sits under it, 0s FG and 1s bright GREEN, and each step lights the table row it reads.
> {differ}: the five pairs of circles flash column by column: a different letter in every column, none GOLD. {same}: the two output rows, 0 0 1 0 0 and 0 0 1 0 0, box GOLD together with a GOLD "=" between them. This two-lane run returns small in s3, s7 and s8, and in ch3 s5.
> {question}: centred YELLOW line under the lanes: "same outputs, different rows?"; the table's rows A and D pulse once.

[c2.hook.1] {title} This is part two of lecture eleven. Last time, you removed states by row matching. {last} When two rows of the state table were identical, {merged} one state replaced the other, and its row was deleted. {table} Here's a new machine, with eight states, from state A to state H, and one output for each state. {nomatch} Look for two identical rows. {pause} No two rows match, so row matching finds nothing to merge.

[c2.hook.2] {run} Now start the machine in state A, start a copy of it in state dee, and feed both the same inputs: zero, one, one, zero. {differ} At every step, the two copies are in different states. {same} Yet both give exactly the same five outputs: zero, zero, one, zero, and zero. {question} So how can you find states that behave the same, when their rows are different? {pause}

## Scene 2 · Same outputs, for ever (ch2_s2_definition)

> {slide}: s1's table shrinks to the left edge, DIM. p. 148's first slide title, "Elimination of Redundant States – State Equivalence", then its first two bullets, verbatim: "The previous row matching approach only works in certain cases." and "We will now consider a more general approach that identifies state equivalence to help eliminate states". {powerful}: a small quote card, the lecturer at 00:11:57: "a more powerful way of trying to identify equivalent states".
> {quote}: the bullets clear to the definition card, p. 148 verbatim: "Two states, say p and q, can be considered equivalent, i.e., p ≡ q, if from each of these states, a finite state machine generates the same output sequence in response to any input bit sequence." p and q YELLOW (names); "same output sequence" GREEN; "any input bit sequence" BLUE. {symbol}: "p ≡ q" lifts out of the card, large, its ≡ GOLD.
> {boxes}: the card shrinks to the top. Below, two copies of the machine as rounded boxes, stacked, labelled "start in p" and "start in q" (p, q YELLOW). {feed}: one BLUE input stream, 0 1 1 0 1 0 …, splits and runs into both boxes. {watch}: a GREEN output stream comes out of each box on the right, bit by bit.
> {agree}: the two output streams match bit for bit; a GOLD "=" between them. {merge}: the two boxes slide together into one box labelled "p ≡ q", outlined GOLD. {move}: beside it, ch1's merge on a small two-row table: one state letter in a next-state entry flashes GOLD and becomes the other, then the extra row goes DIM and leaves.
> {any}: the word "any" in the card boxes YELLOW. {grow}: below, a tree of input sequences grows from one root: 2 branches (0, 1), then 4, then 8, then 16, each level's count in GOLD beside it; the tree runs off the bottom of the screen and "…" follows. {infinite}: a GOLD "∞" beside the "…".
> {hide}: two short GREEN output rows, one above the other, agree for three bits and differ at the fourth, which flashes RED (generic bits; in p. 150's machine, states C and H first differ on the input 1, 0, 0, checked; not named on screen).
> {lecturer}: small quote card, the lecturer at 00:12:52: "we don't really want to be applying an infinitely long sequence to check".

[c2.def.1] {slide} The slide puts it plainly. Row matching only works in certain cases, so we need a more general approach. {powerful} The lecturer calls it a more powerful way of finding equivalent states. {quote} Take two states, and call them pee and cue. They're equivalent if, starting from each one, the machine gives the same output sequence in response to any input sequence. {symbol} We write it with three bars, and say pee is equivalent to cue.

[c2.def.2] {boxes} Picture two copies of the machine, one started in state pee, the other in state cue. {feed} Feed them the same inputs, {watch} and watch only what comes out. {agree} If the outputs always agree, nobody watching could ever tell which copy started where. {merge} So one state is enough. You can merge the two, and the machine behaves exactly as before. {move} In the table, that's part one's move: replace one state by the other, and delete its row.

[c2.def.3] {any} The catch is the word any. {grow} There are two input sequences of length one, four of length two, eight of length three, and they keep doubling. {infinite} To check them all, you'd need sequences of every length, and that never ends. {hide} And stopping early is no help, because two states can agree for several steps and only then differ. {lecturer} As the lecturer says, we do not really want to apply an infinitely long sequence to check. {pause}

## Scene 3 · One step at a time (ch2_s3_onestep)

> {test}: the definition card shrinks to a corner. p. 148's second slide title, "State Equivalence", and its first bullet verbatim: "In practice, 2 states p and q can be considered to be equivalent if for any input bit sequence x , the corresponding outputs y are identical and the next states p′ and q′ are equivalent, i.e., p′ ≡ q′".
> {arcs}: hero, left: p. 148's diagram, rebuilt: circles p and q stacked on the left (YELLOW labels), p′ and q′ on the right; arcs p → p′ labelled "x_p/y_p" and q → q′ labelled "x_q/y_q" (x BLUE, y GREEN), drawn as ch1's Mealy arcs.
> {rule}: right, the slide's line builds clause by clause, verbatim "if x_p = x_q , y_p = y_q and p′ ≡ q′ then p ≡ q": {inputs} "x_p = x_q" (BLUE) as both arc inputs pulse; {outputs} "y_p = y_q" (GREEN) as both outputs pulse; {nexts} "p′ ≡ q′" with a GOLD ≡ drawn between p′ and q′ in the diagram (vertical, as on the slide), then "then p ≡ q" and a GOLD ≡ between p and q. {each}: the arcs fan into two pairs, one for x = 0 and one for x = 1.
> {why}: under the diagram, p's output sequence as a row of GREEN boxes; the first box splits off, labelled "y_p", and the rest is bracketed "sequence from p′". q's row the same, beneath it. {match}: the first boxes link with a GOLD "=" and the brackets with a GOLD "≡"; then both whole rows glow GOLD. {repeat}: the bracket "sequence from p′" itself splits into a first box and a bracket, twice more, a small staircase receding to "…".
> {contrast}: the slide's last bullet, verbatim: "This is in contrast to row matching where p′ and q′ have to be the same, i.e., the identical state." {rowmatch}: a copy of the diagram with p′ and q′ merged into one circle (ch1's merge, GOLD), labelled "row matching: p′ = q′". {here}: beside it the original, labelled "equivalence: p′ ≡ q′".
> {ad}: the diagram's letters become s1's pair (TransformFromCopy from the table's rows A and D): A → D and D → A on input 0 (arcs labelled BLUE "0"). {onone}: A → C and D → E on input 1. Each state's output beside its circle in GREEN (A, D: 0; C, E: 1). A GOLD "≡ ?" between each pair of next states. A small copy of s1's two lanes, with their GOLD "=", sits above.

[c2.step.1] {test} Luckily, there's an equivalent test that only looks one step ahead. {arcs} Take states pee and cue, and give them the same input. Each moves to its next state, called pee prime and cue prime, and each arc is labelled with its input and its output.

[c2.step.2] {rule} Then state pee is equivalent to state cue if three things hold. {inputs} The inputs are the same. {outputs} The outputs are the same. {nexts} And the next states, pee prime and cue prime, are equivalent. {each} That has to hold for each value of the input.

[c2.step.3] {why} Why is one step enough? {pause} The output sequence from state pee is its first output, followed by the output sequence from its next state. The same goes for cue. {match} So if the first outputs are the same, and the next states are equivalent, then the whole sequences are the same. {repeat} The next states pass the same test one step later, and so on, which covers sequences of any length.

[c2.step.4] {contrast} Compare that with row matching, {rowmatch} where the next states had to be identical, the same state. {here} Here, they only have to be equivalent. {ad} That's how states A and dee could behave the same. On input zero, state A goes to dee, while state dee goes back to A. {onone} On input one, they go to states see and ee. Different next states, but they could still be equivalent, and part three shows that they are.

## Scene 4 · Implied pairs (ch2_s4_implied)

> {fork}: p. 149's slide title, "State Equivalence"; s3's p/q diagram, small, upper left; its arrow of reasoning reverses: the GOLD ≡ between p and q lights first, then the two outputs, then the GOLD ≡ between p′ and q′ (if p ≡ q, then these must hold).
> {method}: p. 149's first bullet, verbatim: "What we need is a method to identify equivalent and not just identical next states."; then the diagram moves aside and the hero builds: a decision fork. At the top, "compare p and q, same input x" (p, q YELLOW, x BLUE); two branches down.
> {differ}: left branch, "outputs differ", leads to a RED cross (two diagonals over a square, the style s6 uses), then "p ≢ q" and "settled". Under it, p. 149 verbatim: "Note that if the outputs are different, then the checked states cannot be equivalent."
> {same}: right branch, "outputs same" (GREEN), leads to "p ≡ q if p′ ≡ q′". {implied}: the pair "p′-q′" lifts out of that line, labelled "implied pair" (YELLOW label; the pair in FG, hyphenated as the table will write it). {promise}: it settles into a dashed card, a promise: "p ≡ q, if p′ ≡ q′".
> {quote}: p. 149's second slide line, verbatim: "Just because a particular pairwise comparison implies that some pairs of next states are equivalent, it does not mean they definitely are." {broken}: a short chain of three promise cards, each leaning on the next by an arrow: "p ≡ q if p′ ≡ q′", "p′ ≡ q′ if p″ ≡ q″", "p″, q″: outputs differ". The last gets a RED cross; the RED runs back along the arrows, cracking each card it reaches. Generic letters only: ch3 s3 does this with p. 150's real cells.
> {moore}: the fork clears. Two table headers side by side: left, p. 150's "Present State | Next State X=0 X=1 | Output (Y)" with its one Output column boxed GREEN, labelled "one output per state, like a Moore machine". {mealy}: right, ch1's compact header "Current State | Next State X=0 X=1 | Output (Y) X=0 X=1" (with ch1's row A, "A | B C | 0 0"), its two output columns boxing GREEN one after the other, labelled "Mealy: compare the output for each input value".

[c2.pairs.1] {fork} Now turn the test around. If two states are to be equivalent, then for the same input their outputs must match, and their next states must be equivalent too. {method} So we need a method that finds equivalent next states, not just identical ones. Compare the states two at a time, giving both the same input. {differ} If their outputs differ, you can already tell them apart, so they are not equivalent. That pair is settled. {pause}

[c2.pairs.2] {same} If their outputs are the same, the answer depends on their next states. The two states are equivalent only if those are equivalent too. {implied} Those pairs of next states are called implied pairs. {promise} Think of each one as a promise, not a fact. State pee is equivalent to cue, provided pee prime is equivalent to cue prime.

[c2.pairs.3] {quote} The slide is careful here. Just because one comparison implies that some next states are equivalent, it does not mean they definitely are. {broken} A later comparison may show that an implied pair is not equivalent after all. Then every promise that leaned on it is broken too.

[c2.pairs.4] {moore} One more detail. This machine has one output for each state, like a Moore machine, so you compare the two states' outputs. {mealy} In a Mealy table like part one's, the output depends on the input too. Then you compare the outputs for each input value, column by column.

## Scene 5 · A cell for every pair (ch2_s5_layout)

> {title}: p. 150's slide title, "Determination of State Equivalence using an Implication Table". s1's state table returns to full brightness in the left third, full size; it stays there, unchanged, through s7.
> {grid}: right two thirds: an 8 × 8 grid of empty square cells, A to H along the bottom (left to right) and A to H down the left side (top to bottom), letters FG. p. 150's bullet: "It has a cell for every possible pair of states". {cell}: the cell in column A, row B outlines YELLOW with a small "A-B" inside; the table's rows A and B box YELLOW.
> {mirror}: the cell in column B, row A lights too, labelled "B-A"; both glow GOLD (the same pair). Then every cell above the diagonal glows GOLD with its mirror cell, and the upper ones fade out. p. 150's bullet: "Note cells above the diagonal are omitted (since they already exist below the diagonal)".
> {diag}: the eight diagonal cells label "A-A" … "H-H", go DIM and fade out. Bullet: "Diagonal cells are also omitted since they correspond to same state pairs". {empty}: the top row (row A) and the last column (column H) are now empty; their labels fade.
> {stair}: the remaining cells re-centre as p. 150's staircase, slide title "Example – Implication Table": rows B to H down the left, columns A to G along the bottom, all cells empty. {count}: a GOLD tick runs through the 28 cells, then "28" in GOLD beside the staircase, with "8 × 7 ÷ 2" under it.
> {corner}: the top-left cell outlines YELLOW with a small "A-B"; it fades, leaving the staircase empty. This staircase, with the table to its left, is the drawing that s6, s7 and ch3 build on.

[c2.grid.1] {title} To keep track of every comparison, we use an implication table. {grid} You need to compare every pair of states. So start with a grid, with the eight states along the bottom, and the same eight down the side. {cell} Each cell compares the state of its column with the state of its row. It will hold the result of that comparison, either a cross, or the implied pairs it depends on.

[c2.grid.2] {mirror} But comparing state A with state bee is the same as comparing bee with A. So every cell above the diagonal repeats one below it, and we drop them. {diag} The diagonal would compare each state with itself, which tells us nothing, so it goes too. {empty} That leaves the top row and the last column empty, so they go as well.

[c2.grid.3] {stair} What's left is a staircase. Its rows run from state bee down to state H, and its columns from state A across to state G. {count} That's twenty-eight cells, one for every pair of states. Eight times seven is fifty-six, and half of that is twenty-eight. {corner} The top-left cell compares states A and bee. We name each cell by its pair, with the column's letter first.

## Scene 6 · Crosses from the outputs (ch2_s6_outputs)

> {ac}: in the table, rows A and C box YELLOW; in the staircase, the cell in column A, row C outlines YELLOW. {outs}: their outputs, 0 (FG) and 1 (bright GREEN), box in the Output column, with a RED "≠" between copies of them. {cross}: a RED cross draws into the A-C cell: two diagonals from corner to corner across the whole cell (p. 152's style). Caption, p. 151 in our notation: "A ≢ C" (≢ RED).
> {dots}: the table's Output column glows; a small GREEN dot appears beside each output-1 state's letter on the staircase's axes: rows C, E, F and H, columns C, E and F (H has no column). The dots stay for the rest of the chapter and into ch3. {zeros}: rows A, B, D and G of the Output column glow FG; their axis letters get no dot.
> {all}: every cell where exactly one of its two letters has a dot tints faintly RED. {sixteen}: their crosses draw in one sweep, all 16: A-C, A-E, A-F, A-H, B-C, B-E, B-F, B-H, C-D, C-G, D-E, D-F, D-H, E-G, F-G, G-H (checked). "16" in GOLD beside the staircase, "4 × 4" under it. {lecturer}: a small note, "the lecturer: column by column, the same 16".
> {twelve}: the 12 open cells outline GOLD briefly (same outputs); "12" in GOLD under the "16"; then the outlines and numbers fade.
> {notation}: the staircase dims; p. 151's words, small: "we place an X in this cell". {three}: a panel of three X's in a row, each labelled: the input X from the table's header "X=0 X=1" (BLUE), "input"; an "X" in one cell of a small 2 × 2 K-map (L6 `kmap()` style), "don't care"; our cross (RED diagonals across a whole cell), "not equivalent".
> {draw}: the first two fade; the cross flies back into the A-C cell, and the staircase returns to full brightness: 16 RED crosses, GREEN dots, 12 empty cells.

[c2.cross.1] {ac} Start with states A and see. {outs} State A outputs zero, but state see outputs one. Their outputs differ, so they are not equivalent. {cross} So we cross out their cell. A cross means not equivalent, and that pair is settled. A cell with a cross in it gets no implied pairs, because whatever the next states do, the outputs already differ.

[c2.cross.2] {dots} Now mark each state that outputs one with a green dot. Four states get a dot, {zeros} and the other four output zero. {all} Any pair with one of each has different outputs. {sixteen} That's four times four, so sixteen cells get a cross at once. {lecturer} In the lecture, the crosses go in column by column, and you get the same sixteen. {twelve} That leaves twelve open cells, the pairs whose outputs match: six among the zeros, and six among the ones.

[c2.cross.3] {notation} A word about the cross. The slides call it placing an ex in the cell. {three} But this course already uses ex for the input, and for don't cares in K-maps. {draw} So we draw the cross over the whole cell, as the slide does, and it means just one thing. These two states are not equivalent.

## Scene 7 · Column A (ch2_s7_columna)

> {ab}: rows A and B of the table box YELLOW; the A-B cell outlines YELLOW. {zeroout}: their outputs, 0 and 0, box GOLD (the same). {zero}: in the X=0 column (BLUE header), D and F box; copies fly from the table (TransformFromCopy) and land on the first line of the A-B cell as "D-F" (FG). {one}: in the X=1 column, C and H box; copies land on the second line as "C-H". {write}: caption, p. 151 verbatim: "A ≡ B if D ≡ F and C ≡ H." Every implied pair is written in alphabetical order, as on p. 152.
> {ad}: rows A and D box YELLOW; the A-D cell outlines; outputs 0 and 0 box GOLD. s1's two lanes, small, above the staircase, with their GOLD "=". {self}: X=0 gives D and A; they land in alphabetical order as "A-D" on the cell's first line. Caption: "A ≡ D if A ≡ D". {strike}: that "A-D" is struck through and turns DIM, kept in place as p. 152 shows it; p. 152's line: "Note that 'self implied' pairs are removed from the table". {ce}: X=1 gives C and E; they land as "C-E" on the second line, FG. {promise}: caption "A ≡ D if C ≡ E"; the lanes fade.
> {ag}: rows A and G box; the A-G cell outlines; outputs 0 and 0 box GOLD. {ag0}: X=0 gives D and B; the two letters swap places as they land, "B-D" (alphabetical order). {ag1}: X=1 gives C and H: "C-H". {twice}: the two "C-H" pairs, in the A-B and A-G cells, pulse YELLOW together, joined by a faint YELLOW link that then fades (no pointer to the C-H cell yet: that's ch3).
> {done}: column A's three filled cells (A-B, A-D, A-G) outline YELLOW together, then its four crosses (A-C, A-E, A-F, A-H) pulse RED; caption "column A: 3 promises, 4 crosses" (3 and 4 GOLD). The caption then fades, leaving p. 152's column A exactly: the table on the left; the staircase with its GREEN dots; 16 RED crosses; A-B "D-F" over "C-H"; A-D "A-D" (struck, DIM) over "C-E"; A-G "B-D" over "C-H"; the other nine open cells empty. ch3 s1 opens on this exact frame.

[c2.column.1] {ab} Now fill in the open cells, starting with column A and its first cell, states A and bee. {zeroout} Both output zero, so look at where they go next. {zero} On input zero, they go to states dee and eff. {one} On input one, they go to states see and H. {write} So state A is equivalent to state bee, if dee is equivalent to eff, and see to H. Those two implied pairs go in the cell.

[c2.column.2] {ad} Next come states A and dee, the pair we started with, and again both output zero. {self} On input zero, state A goes to dee, and state dee goes to A. So the two are equivalent if they are equivalent, which tells us nothing. {strike} A pair that implies itself is struck out. {ce} On input one, they go to states see and ee. {promise} So the pair from the start comes down to one promise, that state see is equivalent to state ee.

[c2.column.3] {ag} Last, states A and G, which also both output zero. {ag0} On input zero, they go to states dee and bee, written in alphabetical order, bee and dee. {ag1} On input one, they go to states see and H. {twice} Notice that the pair see and H turns up in two cells. If it ever fails, both of those promises fail with it. {done} Column A is done, with three cells of promises and four crosses.

## Scene 8 · Recap and next (ch2_s8_recap)

> Recap: one small panel per sentence, each the same object, colours and styling as the scene that taught it, with its short line beneath; the panels gather on a 4 + 3 grid. {recap}: the full table and staircase clear first.
> {r1}: s1's two lanes (A and D on 0, 1, 1, 0) with their GOLD "=" between the output rows: "different rows, same outputs".
> {r2}: s2's two machine boxes fed one BLUE stream, GREEN streams out, GOLD "=": "same outputs for every input sequence".
> {r3}: s3's p/q diagram with the GOLD ≡ between p′ and q′: "same outputs, equivalent next states". {r4}: s4's fork, RED cross on the left, the dashed promise card on the right: "differ: settled · same: implied pairs".
> {r5}: s5's 8 × 8 grid shrinking to the staircase, GOLD "28": "a cell for every pair". {r6}: s6's staircase with GREEN dots and its 16 RED crosses: "different outputs: 16 crosses". {r7}: s7's column A, "D-F / C-H", struck "A-D" / "C-E", "B-D / C-H": "column A: three promises". {r7b}: the A-D cell's "C-E" pulses GOLD beside a tiny copy of s1's two lanes.
> {next}: the panels clear; s7's final frame returns exactly. The nine empty open cells (B-D, B-G, C-E, C-F, C-H, D-G, E-F, E-H, F-H) outline YELLOW one after another. {which}: a small YELLOW "?" appears beside each of column A's five live implied pairs (D-F, C-H, C-E, B-D, C-H; never the struck A-D). This is ch3 s1's opening shot.
> End card after the last word, about 8 s, the music carrying it.

[c2.recap.1] {recap} To recap. {r1} States A and dee have different rows, yet on the same inputs they gave the same outputs. {r2} Two states are equivalent if they give the same output sequence for any input sequence. {r3} You can check that one step at a time, by asking for the same outputs and equivalent next states. {r4} If the outputs differ, the pair is settled. If they match, the next states become implied pairs, promises still to be tested.

[c2.recap.2] {r5} The implication table has one cell for every pair, a staircase of twenty-eight. {r6} Different outputs crossed out sixteen of them at once. {r7} Column A, the first column, now holds three cells of promises. {r7b} Our pair from the start, states A and dee, now rests on just one of them. {pause} {next} Next time, we fill in the other nine cells, and then test every promise. {which} Which of them will hold? {pause=1.5}
