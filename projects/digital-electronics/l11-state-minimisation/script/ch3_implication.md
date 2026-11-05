# Chapter 3 · Solving the implication table

Digital Electronics Lecture 11 (State Minimisation, Programmable Logic and Circuits), part 3 of 6. Source: slides pp. 152–155 (with p. 144's "may", p. 147's 7-state table and p. 148's definition as callbacks); recording 00:20:42–00:31:25.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch3_s1_hook)

> On {title}, the title card: "State Minimisation, Programmable Logic and Circuits" (scaled to 12 units wide, as ch1 s1), the course line "Digital Electronics · Lecture 11", and "Part 3 · Solving the implication table".
> On {table}, ch2's last shot, carried over exactly as ch2 s7 left it (ch2 s8's YELLOW outlines and "?" marks cleared). Left: p. 150's state table, header "Present State | Next State X=0 X=1 | Output (Y)", rows A D C 0, B F H 0, C E D 1, D A E 0, E C A 1, F F B 1, G B H 0, H C G 1 (state letters FG, X BLUE, a 1 output bright GREEN, 0s FG). Right: the staircase implication table, rows B to H down the left, columns A to G along the bottom, with ch2 s6's small GREEN dots beside the output-1 states: rows C, E, F and H, columns C, E and F. This frame, table and staircase, stays the chapter's home shot through s5.
> On {crosses}, the 16 RED crosses (two diagonals across the whole cell, never a letter X) pulse once: A-C, A-E, A-F, A-H, B-C, B-E, B-F, B-H, C-D, C-G, D-E, D-F, D-H, E-G, F-G, G-H.
> On {columna}, column A's three open cells light in turn, contents as p. 152 writes them, the X=0 pair on top: A-B "D-F / C-H"; A-D "A-D" struck through DIM (self-implied) over "C-E"; A-G "B-D / C-H". The other nine open cells stay empty.
> On {promise}, the A-B cell's contents lift out beside the table and become one line: "A ≡ B  if  D ≡ F  and  C ≡ H" (A and B YELLOW, the conditions FG). It stays up through {question}, with a YELLOW "?" over it and the caption "which promises can be kept?".
> On {answer}, the line fades and the 12 open cells (filled or not) get a faint YELLOW outline. A small tag under the state table: "8 states → ?".

[c3.hook.1] {title} This is part three of lecture eleven, and the last part on state minimisation. {pause} {table} Last time, we built an implication table for an eight-state machine, with a cell for every pair of states. {crosses} Sixteen cells got a cross, because their two states give different outputs. {columna} And the three open cells in column A got their promises.

[c3.hook.2] {promise} Take the top one. State A is equivalent to state B, if state D is equivalent to state F, and state C is equivalent to state H. {question} So which of these promises can be kept? {pause} {answer} By the end of this part, the table will tell us, and the machine will be two states smaller.

## Scene 2 · The other nine cells (ch3_s2_fill)

> Same shot as s1: state table left, implication table right, 16 crosses and column A filled. Reading a cell is ch2 s7's animation, used for all nine: the two state-table rows box YELLOW and the cell outlines YELLOW; their two outputs box GOLD (the same; 1s stay bright GREEN). Then in the X=0 column (BLUE header) the two next-state letters box, and copies fly out (TransformFromCopy) to land on the cell's first line as one pair in alphabetical order, joined by a hyphen (letters swap places as they land if needed); then the same for X=1 on the second line, as p. 152 writes them.
> On {colb}, column B's label lights. On {bd}, rows B and D light; outputs 0 and 0. On {bd0}, F and A fly in and land as "A-F". On {bd1}, H and E land as "E-H". On {bdcell}, the cell settles: "A-F / E-H".
> On {bg}, rows B and G light; 0 and 0. On {bg0}, F and B land as "B-F". On {bg1}, H and H fly toward the cell, merge into one H and fade before landing; on {same}, a small caption "H ≡ H: always true, not written" (00:22:15). On {bgcell}, the cell shows "B-F" alone.
> On {ce}, rows C and E light; 1 and 1, both bright GREEN. On {ce0}, E and C land as "C-E", the cell's own label on both axes flashes YELLOW, and "C-E" takes a DIM strikethrough, matching "A-D" in the A-D cell (which flashes once). On {ce1}, D and A land as "A-D". On {cecell}, the cell settles: struck "C-E" over "A-D".
> On {rest}, a caption quoting the lecturer (00:23:21): "you just have to keep doing these pairwise comparisons". On {six}, the same reading animation, quicker, fills C-F "E-F / B-D", then C-H "C-E / D-G", then on {way} D-G "A-B / E-H" and E-F "C-F / A-B".
> On {eh}, E-H: rows E and H light; on X=0 both go to C, and the two C's merge and fade like B-G's H's. On {single}, "A-G" lands, alone in the cell.
> On {full}, F-H fills "C-F / B-G", and the whole table settles as p. 152: 12 cells of promises (FG text), 16 RED crosses. Small tally under it: "12 cells of promises · 16 crosses".
> All 28 cells checked against p. 152 (Python 3.11.9, from p. 150's table): A-B D-F, C-H; A-D (A-D) C-E; A-G B-D, C-H; B-D A-F, E-H; B-G B-F; C-E (C-E) A-D; C-F E-F, B-D; C-H C-E, D-G; D-G A-B, E-H; E-F C-F, A-B; E-H A-G; F-H C-F, B-G.

[c3.fill.1] {colb} Column B comes next, comparing state B with every state below it. {bd} States B and D both output zero. {bd0} On input zero, they go to states F and A. {bd1} On input one, they go to states H and E. {bdcell} So the cell for B and D holds two promises, the pair A and F, and the pair E and H.

[c3.fill.2] {bg} States B and G both output zero too. {bg0} On input zero, they go to states F and B. {bg1} On input one, they both go to state H. {same} A state is always equivalent to itself, so that promise asks for nothing, and it's left out. {bgcell} So the cell holds just the pair B and F.

[c3.fill.3] {ce} In column C, states C and E both output one. {ce0} On input zero, they go to states E and C. That's the very pair we're testing, so it's self-implied, and we strike it out, just as we did in the cell for A and D. {ce1} On input one, they go to states D and A. {cecell} So states C and E are equivalent if states A and D are.

[c3.fill.4] {rest} The lecturer did these columns, and then said that you just have to keep doing these pairwise comparisons. {six} So here are the rest, {way} each one taken from the state table the same way. {eh} One more cell has a state twice. From states E and H, input zero leads to state C both times. {single} So that cell holds just the pair A and G. {full} And now the table is complete, with twelve cells of promises and sixteen crosses.

## Scene 3 · The first pass (ch3_s3_pass1)

> Same shot: p. 152's complete table from s2, the state table still on the left. Caption at the top, from p. 153 (its ≠ written ≢, as everywhere in this lecture): "If one of the pairs in say cell i-j is not equivalent, then i ≢ j". A small counter in the corner: "pass 1".
> The pointer (one animation, used all scene): a YELLOW arrow curves from an implied pair's text to the cell that pair names, and that cell flashes. If the named cell is crossed, the pair's text turns RED and a RED cross draws across the cell being checked; its text stays, DIM, under the cross, as on p. 154. If the named cell is open, the arrow fades and a small YELLOW "?" sits in the checked cell.
> On {check}, the A-B cell outlines YELLOW. On {pointer}, the pointer runs from "D-F" to the D-F cell (row F, column D). On {crossed}, that cell's cross pulses, and in the state table the outputs of rows D (0) and F (1, bright GREEN) light. On {broken}, the RED cross draws over A-B.
> On {ad}, the pointer runs from A-D's "C-E" to the C-E cell; on {open}, open: "?". On {ag}, two pointers from A-G, "B-D" and "C-H", both to open cells: "?", and the caption "yet".
> On {colb}, column B's label lights. On {bd}, "A-F" points to a crossed cell: cross B-D. On {bg}, "B-F" points to a crossed cell: cross B-G. On {colc}, column C's label lights. On {cf}, the pointer runs from C-F's "B-D" (its "E-F" points to a cell still open); on {fresh}, the B-D cross drawn a moment ago pulses, caption "use a cross as soon as it's made", and C-F is crossed. On {ceh}, C-E's "A-D" and C-H's "C-E" and "D-G" point to open cells: two more "?".
> On {dg}, D-G's "A-B" points to the A-B cell (this pass's first cross): cross. On {ef}, E-F's "A-B" does the same (its "C-F" is crossed too): cross. On {eh}, E-H's "A-G" points to an open cell: "?". On {fh}, F-H's "B-G" points to a crossed cell: cross.
> On {seven}, the seven new crosses pulse together, A-B, B-D, B-G, C-F, D-G, E-F, F-H; the counter reads "pass 1: +7". This is p. 154's table. Checked (Python 3.11.9), checking cells column by column and using each cross as soon as it's made.
> On {later}, a small inset of p. 154's slide picture, its B-D cell ringed YELLOW (already crossed), beside our A-G cell; caption, the lecturer's words (00:25:32): "comes from later on". On {firstpass}, the inset fades: in our table, at the moment A-G was checked, B-D was still open (replay the "?" on A-G briefly).

[c3.pass.1] {check} Now we test the promises, starting again at the top of column A. The cell for A and B holds two promises, and the first is the pair D and F. {pointer} That pair has a cell of its own, so follow the pointer there. {crossed} It's crossed, because state D outputs zero and state F outputs one. {broken} So that promise is broken, and states A and B are not equivalent. Cross their cell too.

[c3.pass.2] {ad} Next is the cell for A and D. Its one promise is the pair C and E. {open} That cell has no cross, so it's too early to tell, and we leave it open. {ag} The cell for A and G is the same story. Neither of its pairs, B and D, or C and H, has a cross. Not yet, anyway.

[c3.pass.3] {colb} On to column B. {bd} The cell for B and D leans on A and F, which is crossed, so cross it. {bg} The cell for B and G leans on B and F, also crossed. {colc} Then column C. {cf} The cell for C and F leans on B and D, {fresh} which we crossed a moment ago. Use a cross as soon as it's made, so cross this one too. {ceh} The cells for C and E, and for C and H, lean only on open cells, so leave them.

[c3.pass.4] {dg} In the rest of the table, the cell for D and G leans on A and B, the first cell we crossed. Cross it. {ef} The cell for E and F leans on A and B too, so cross it. {eh} The cell for E and H leans on A and G, still open. {fh} And the cell for F and H leans on B and G, which is crossed. {seven} That's the first pass, and it made seven new crosses.

[c3.pass.5] {later} If you follow the slides, watch out for one thing. When the lecturer checks the cell for A and G, the pair B and D already shows a cross, which he says comes from later on. The slide's picture already holds crosses from further down the table. {firstpass} On your first pass, that cell is still open.

## Scene 4 · Again, until nothing changes (ch3_s4_again)

> Same shot, with pass 1's seven RED crosses. On {seven}, they pulse once. On {lean}, three open cells light YELLOW, A-G, C-H and E-H, each with a faint YELLOW pointer from one of its pairs to a newly crossed cell (A-G's "B-D", C-H's "D-G"; E-H's "A-G" stays DIM for now). On {again}, the caption from p. 154: "So, we must go through again to see if the added Xs make any other pairs non-equivalent". The counter turns to "pass 2".
> s3's pointer animation again. Pass 2's crosses are drawn thicker than the others, as p. 155 draws them bold. On {ag}, A-G's "B-D" points to a crossed cell: thick cross on A-G. On {ch}, C-H's "D-G" points to a crossed cell (its "C-E" points to an open one): thick cross on C-H. On {eh}, E-H's "A-G" points to the cross drawn a moment ago, which pulses: thick cross on E-H. On {three}, the three thick crosses pulse together; counter "pass 2: +3".
> On {pass3}, the counter turns to "pass 3". On {left}, the only two open cells, A-D and C-E, outline YELLOW. On {lean2}, two YELLOW pointers: from A-D's "C-E" to the C-E cell, and from C-E's "A-D" to the A-D cell, closing a loop; neither cell is crossed. On {stop}, the counter reads "pass 3: +0" and stops. On {quote}, p. 155's bullet as a caption: "No more Xs are added, so all cells with non equivalent states have now been Xed out".
> On {order}, the table shrinks left. Beside it, a second copy of p. 152's table (no pass crosses yet), titled "only crosses from earlier passes". On {waves}, its crosses arrive in waves, each wave's cells all at once: wave 1 A-B, B-D, B-G; wave 2 A-G, C-F, D-G, E-F, F-H; wave 3 C-H, E-H; wave 4 none. Under each table its tally: "+7, +3, +0" and "+3, +5, +2, +0".
> On {why}, the two tables' open cells, A-D and C-E in both, glow GOLD together (the same result); caption "the order changes the passes, never the result". Both orders checked (Python 3.11.9).

[c3.again.1] {seven} Those seven crosses are seven new broken promises. {lean} And some of the cells we left open lean on them. {again} So, as the slide says, we must go through again.

[c3.again.2] {ag} Here's pass two. The cell for A and G leans on B and D, crossed in pass one, so cross it. {ch} The cell for C and H leans on D and G, also crossed in pass one. {eh} And the cell for E and H depends on A and G, which we crossed a moment ago, earlier in this pass. {three} That's three more crosses.

[c3.again.3] {pass3} So we go through once more, for pass three. {left} Only two cells are still open, the cell for states A and D, and the cell for states C and E. {lean2} Each one leans only on the other, and neither is crossed. {stop} Nothing changes, so we stop. {quote} As the slide puts it, every cell with non-equivalent states has now been crossed out.

[c3.again.4] {order} Does the order you check the cells in matter? {pause} Here's an example. In each pass, use only the crosses from earlier passes, never one made during the pass. {waves} Then the crosses arrive in three waves instead of two, and the same two cells survive. {why} A cross only ever goes where a promise is broken, and you only stop when no open cell leans on a crossed one. So the order can change how many passes it takes, but never the result.

## Scene 5 · Promises that hold (ch3_s5_survivors)

> Same shot, the final table: 26 RED crosses (pass 2's thick), two open cells. On {two}, the crosses dim a little and the cells A-D (row D, column A) and C-E (row E, column C) glow GOLD, the colour of "the same". On {cellad}, A-D's letters on the axes light YELLOW; on {cellce}, C-E's do.
> On {coords}, p. 155's bullet as a caption: "The ‘coordinates’ of the remaining cells correspond to the equivalent state pairs, i.e., cell A-D and cell C-E so," then its line "A ≡ D and C ≡ E" (letters YELLOW).
> On {doubt}, s4's loop of two YELLOW pointers (A-D to C-E and back) returns, with a YELLOW "?" in the middle.
> On {cross}, the A-B cell's RED cross pulses. On {ab}, the pointer from its "D-F" to the crossed D-F cell. On {input}, a small run below the table (two rows, Moore style: each state with its output under it): "A —0→ D" with outputs 0, 0, and "B —0→ F" with outputs 0, 1; the input 0 BLUE, F's 1 bright GREEN. On {apart}, the last two outputs ring YELLOW and "A ≢ B" appears in RED. Checked: 0 is the shortest input that separates A and B.
> On {loop}, the pair graph (ours): two GOLD nodes labelled "A-D" and "C-E", each with its two states' outputs under it ("0, 0" and "1, 1", 1s bright GREEN). On {fromad}, A-D's arcs: input 0 is a self-loop back to A-D (A goes to D, D goes to A), input 1 goes to C-E (A to C, D to E); input labels BLUE. On {fromce}, C-E's arcs: input 0 is a self-loop (C to E, E to C), input 1 goes to A-D (C to D, E to A).
> On {closed}, a YELLOW dot walks the graph on the inputs 1, 0, 1, 1, 0, never leaving the two nodes, each node's matching outputs lighting as it lands. On {never}, ch2 s2's definition card returns, small, in its styling (p and q YELLOW, "same output sequence" GREEN, "any input bit sequence" BLUE), and both phrases pulse.
> On {callback}, the pair graph shrinks aside and ch2 s1's two-lane run comes back (same object): lanes "start in A" and "start in D", inputs 0, 1, 1, 0 (BLUE) along the top; lane A visits A, D, E, A, D; lane D visits D, A, C, D, A; both output rows read 0, 0, 1, 0, 0 with the GOLD "=" between them. On {pairs}, the states pair up column by column into (A, D), (D, A), (E, C), (A, D), (D, A). On {lands}, each pair flies to its GOLD cell in the table: A-D, A-D, C-E, A-D, A-D.
> Checked (Python 3.11.9): A ≡ D and C ≡ E for every input sequence up to length 8; partition refinement gives exactly {A, D}, {C, E} and the rest alone; the run and the pair graph's arcs as above.

[c3.survive.1] {two} Two cells survive, {cellad} the cell for A and D, {cellce} and the cell for C and E. {coords} The slide reads the answer from their coordinates. State A is equivalent to state D, and state C is equivalent to state E. {pause=1.5} {doubt} But each of those two promises leans only on the other. Is that really enough? {pause}

[c3.survive.2] {cross} Look first at what a cross means. Every cross records a real difference. {ab} The cell for A and B was crossed because of the pair D and F. {input} So feed in a zero. State A goes to D and outputs zero, while state B goes to F and outputs one. {apart} Now you can tell them apart. Every cross traces back like this, to two outputs that differ.

[c3.survive.3] {loop} Now look at the two survivors. {fromad} From states A and D, input zero leads to D and A, and input one leads to C and E. {fromce} From states C and E, input zero leads to E and C, and input one leads to D and A. {closed} Whatever you feed in, the pair never leaves these two cells, and in each cell, both states give the same output. {never} So no input sequence can ever tell them apart. That's exactly what equivalent meant in part two.

[c3.survive.4] {callback} You saw this at the start of part two. One copy of the machine started in state A, the other in state D, and both were fed zero, one, one, zero. They visited different states, but gave the same outputs. {pairs} Now pair up their states, step by step. {lands} Every pair lands in one of the two surviving cells.

## Scene 6 · Six states (ch3_s6_merge)

> The implication table shrinks to the top right, keeping only its two GOLD cells lit. The state table moves to the centre, larger, p. 150's header and rows unchanged.
> On {keep}, row labels A and C light GOLD; D and E get a small "→ A" and "→ C" beside them.
> On {replace}, ch1's merge animation: every D in the next-state columns (row A's X=0, row C's X=1) flashes GOLD and becomes A. On {replacee}, every E (row C's X=0, row D's X=1) flashes GOLD and becomes C.
> On {match}, row D, now "A C 0", slides up beside row A, "A C 0", and both glow GOLD (ch1 s6's matching rows); then row E, now "C A 1", beside row C, "C A 1", both GOLD. On {rowmatch}, the caption "identical rows". On {delete}, rows D and E go DIM, then leave, and the table closes up; ch1 s6's GOLD state counter in the corner reads "8 → 6".
> On {six}, p. 155's 6-state table, exactly: "Present State | Next State X=0 X=1 | Output (Y)", A A C 0, B F H 0, C C A 1, F F B 1, G B H 0, H C G 1. Checked: the merge gives this table, it behaves like the 8-state machine on every input sequence up to length 8, and it's minimal (Python 3.11.9).
> On {ladder}, ch1 s2's ladder returns (same object as ch1 s2 and s7, L10 ch1 s4's doubling ladder): rows "1 flip-flop: 2 patterns", "2: 4", "3: 8", "4: 16", counts GOLD. A GOLD bracket "8 states" lands on the 3 row, with `\lceil \log_2 8 \rceil = 3`; on {no}, a second bracket "6 states" lands on the same row, `\lceil \log_2 6 \rceil = 3`, tag "still 3" (this pays off ch1 s2's forward tag "Part 3: 8 states → 6, still 3 flip-flops").
> On {spare}, the 3 row opens into its eight GREEN code chips, 000 to 111 (ch1 s2's styling): six lit, two DIM, each DIM chip taking a don't-care X with the tag "don't care" (L10 ch1 s3's styling). Which two codes are unused depends on the assignment; the drawing just takes the last two.
> On {may}, p. 144's bullet as a caption: "In general, reducing the number of states may reduce the number of FFs required and may also reduce the complexity of the next state logic owing to the presence of more unused states (don't cares)". The first "may" gets a small "not here"; the second "may" lights YELLOW.

[c3.merge.1] {keep} Now we merge, just as in row matching. We keep states A and C, and drop states D and E. {replace} Wherever D appears as a next state, we write A. That's row A's entry for input zero, and row C's for input one. {replacee} And wherever E appears, we write C. That's row C's entry for input zero, and row D's for input one.

[c3.merge.2] {match} Now look at rows D and E. Row D now reads A and C, with output zero, exactly like row A. Row E reads C and A, with output one, exactly like row C. {rowmatch} After the replacements they're identical rows, the kind row matching merges. {delete} And since nothing leads to D or E any more, we delete both rows.

[c3.merge.3] {six} Here's the result, the slide's six-state table. {ladder} So did that save a flip-flop? {pause} {no} Eight states need three flip-flops, and so do six, so no. {spare} But two of the eight codes are now unused, and unused codes are don't cares in the next-state logic. {may} That's why the slides said fewer states may reduce the flip-flops. Here the count of flip-flops is the same, but the logic may still get simpler.

## Scene 7 · The method (ch3_s7_method)

> On {steps}, the screen clears to four numbered cards in a column, each with a tiny icon from this chapter. On {step1}, "1 · Compare every pair of states" (the empty staircase, ch2 s5). On {step2}, "2 · Outputs differ: cross the cell. Outputs match: write the implied pairs" (one RED cross beside one cell reading "D-F / C-H"). On {step3}, "3 · Go through again and again, crossing every cell with a crossed pair, until nothing changes" (the pass counter, "+7, +3, +0"). On {step4}, "4 · Merge the pairs that survive" (the two GOLD cells, and a D flashing GOLD into an A).
> On {power}, the cards shrink to the left. Two columns on the right, headed "row matching" and "implication table". On {identical}, under row matching: "next states identical", with ch2 s3's merged copy of p. 148's diagram (p′ and q′ one GOLD circle, "row matching: p′ = q′"). On {equivalent}, under the implication table: "next states equivalent", with ch2 s3's original beside it (p → p′ labelled "x_p/y_p", q → q′ labelled "x_q/y_q", a GOLD "≡" between p′ and q′, "equivalence: p′ ≡ q′").
> On {here}, under each column, its score on p. 150's machine: row matching "no identical rows: 0 merges"; the implication table "2 merges: A ≡ D, C ≡ E" (GOLD). Checked: p. 150 has no two identical rows.
> On {part1}, the columns clear. ch1 s7's 7-state diagram returns (A, B, C, D, E, H, J, with J's 1/1 arc GREEN), small, left; beside it p. 147's 7-state table (header "Current State | Next State X=0 X=1 | Output (Y) X=0 X=1") and a new implication table for it: rows B, C, D, E, H, J, columns A, B, C, D, E, H, 21 cells.
> On {crossall}, its crosses arrive in three waves (Mealy table: outputs compared for each input, as ch2 s4 said): first the 6 cells that pair J with another state (J's output for X=1 is 1); then pass 1's 7; then pass 2's last 8. Every cell is crossed. Checked (Python 3.11.9): 6 + 7 + 8 = 21; no equivalent pairs; partition refinement on p. 145's 15 states gives the same 7 classes row matching found.
> On {enough}, a caption under the 7-state machine: "already minimal: row matching was enough"; beside it, small, the 6-state table with "needed the implication table".
> On {try}, a caption with the lecturer's words: "the best way of … understanding this is just to have a go and do it" (00:31:12), and under it "an example in the examples paper".

[c3.method.1] {steps} The lecturer summed up the method in four steps. {step1} One, compare every pair of states. {step2} Two, where the outputs differ, cross the cell, and where they match, write in the implied pairs. {step3} Three, go through again and again, crossing every cell with a crossed pair, until a pass changes nothing. {step4} Four, merge the pairs whose cells survive.

[c3.method.2] {power} He called it more powerful than row matching. {identical} Row matching needs two states to have identical next states. {equivalent} The implication table only needs their next states to be equivalent. {here} On this machine, row matching found nothing at all, while the table found two merges.

[c3.method.3] {part1} Part one left a promise of its own. Row matching cut that machine to seven states, but was that the smallest it could be? {pause} {crossall} Run the implication table on those seven states, and every single cell ends up crossed. So no two of them are equivalent. {enough} Row matching had already found the smallest machine. That time, row matching was enough. This time, we needed the table.

[c3.method.4] {try} The lecturer's advice is that the best way to understand this is to have a go yourself. There's an example in the course's examples paper.

## Scene 8 · Recap and next (ch3_s8_recap)

> On {recap}, the heading "Recap". Six small panels in a 3 × 2 grid, each a small version of the visual that taught it (same objects, colours and styling), appearing on its sentence's mark with its short line under it.
> {r1}: s2's complete table, 12 cells of FG promises among 16 RED crosses, "matching outputs: write the promises".
> {r2}: s3's YELLOW pointer from A-B's "D-F" to the crossed D-F cell, and the RED cross landing on A-B, "a broken promise: cross the cell".
> {r3}: s4's pass counter stepping "+7", "+3", "+0", the thick pass-2 crosses lit, "again, until nothing changes".
> {r4}: s5's two GOLD cells, A-D and C-E, with their loop of YELLOW pointers, "the survivors: A ≡ D, C ≡ E".
> {r5}: s6's 6-state table with the ladder's "6 states" marker on the 3-flip-flop rung, "6 states, still 3 flip-flops".
> {r6}: s7's two columns, "identical" under row matching and "equivalent" under the implication table, "equivalent, not just identical".
> On {next}, the grid clears. The 6-state table slides into a chip package (L8's `chip()`, as ch4 s1 will use), and the caption "a chip you can program" appears under it. Then the end card: hold about 8 s after the last word while the music carries it.

[c3.recap.1] {recap} Let's recap. {r1} Every cell whose states give the same output holds a promise, its pairs of next states. {r2} A promise that leans on a crossed cell is broken, so that cell gets crossed too. {r3} New crosses can break more promises, so you go through again and again, until a pass changes nothing.

[c3.recap.2] {r4} The cells that survive are the equivalent pairs, here state A with state D, and state C with state E. {r5} Merging them left six states. That's still three flip-flops, but with two spare codes. {r6} And unlike row matching, the method finds states that are equivalent, not just identical. {pause}

[c3.recap.3] {next} Next time, we know what to build, so the question becomes how to build it, on a chip you can program. {pause}
