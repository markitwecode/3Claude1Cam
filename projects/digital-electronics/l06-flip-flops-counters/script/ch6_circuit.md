# Chapter 6 · From table to circuit

Digital Electronics, Lecture 6 (Flip-flops and Counters), part 6 of 6. Source: slides `combined_26.pdf` pp. 99–101 (to p. 101's "Synchronous Counter" slide); recording 00:53:21–00:59:57 (it ends during the counter demo).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch6_s1_hook)

> Title card: "Flip-flops and Counters", "Digital Electronics · Lecture 6", "Part 6 · From table to circuit". Lecture conventions throughout this chapter: Q′ is the next state; an overbar is NOT (MathTex `\overline{Q_0}`); AND is the slide's dot (`Q_0.Q_1`), + is OR. CLK YELLOW, inputs D0–D2 BLUE, outputs Q0–Q2 GREEN, trouble RED, wires bright at 1 and dim at 0, decimal values GOLD beside binary (011 = 3). Every table, map, group, equation and count in this chapter was checked by exhaustive enumeration (Python 3.11.9, itertools.product); no code on screen.
> {table}: ch5 s6's settled modified state transition table returns exactly (same object, layout and colours; slide p. 99): headers "Current state" `Q_2 Q_1 Q_0` | "Next state" `Q_2' Q_1' Q_0'` (GREEN) | "FF inputs" `D_2 D_1 D_0` (BLUE), each row's decimal value 0 … 7 in GOLD at the left. This table, in this layout, is the working object of s2–s4. Rows: 000 001 001 / 001 010 010 / 010 011 011 / 011 100 100 / 100 101 101 / 101 110 110 / 110 111 111 / 111 000 000. One row (011 → 100 → 100) lights with arrows current → next → inputs.
> {equal}: the next-state and FF-inputs blocks flash together; a YELLOW `D = Q'` (ch5 s4) between them.
> {block}: the table shrinks to the upper left. ch5 s2's structure: three D flip-flops (FF0 left, FF2 right, as p. 100) on one YELLOW CLK line; their outputs Q2 Q1 Q0 (GREEN) feed a "Combinational logic" block whose outputs D2 D1 D0 (BLUE) feed back to the D inputs.
> {question}: a big YELLOW "?" on the block; the block's outputs read `D_0 = ?`, `D_1 = ?`, `D_2 = ?`.
> {tools}: three chips from p. 99's last bullet: "inspection", "Boolean algebra", "K-maps". On {all} they line up as the chapter's road.

[c6.hook.1] {title} Last time, we wrote the modified state transition table for a counter that runs from zero to seven, and back to zero. {table} Each row gives a current state, the next state, and the flip-flop inputs that get us there. {equal} With dee flip-flops, the input columns are exactly the same as the next state. {pause}

[c6.hook.2] {logic} But those inputs have to come from somewhere. {block} In the circuit, a block of gates sits between the flip-flops' outputs and their inputs. {function} So dee zero, dee one and dee two are each a function of the current state, cue two, cue one, cue zero. {question} What's inside that block? {pause} {tools} There are three tools for the job, inspection, Boolean algebra and kay-maps. {all} We'll use all three, then build the counter and watch it count.

## Scene 2 · D0 by inspection (ch6_s2_d0)

> s1's table back at full size, left of centre. {d0}: the D0 column boxed BLUE, everything else dims. {read}: its entries light one by one, 1 0 1 0 1 0 1 0. {qzero}: the Q0 column boxed GREEN, 0 1 0 1 0 1 0 1.
> {opposite}: a short link between each row's Q0 and D0 entries, flashing pair by pair: always opposite. {result}: right of the table, slide p. 100's "By inspection," and MathTex `D_0 = \overline{Q_0}`, the overbar drawn last in YELLOW.
> {meaning}: one D flip-flop (ch2 s6's symbol: box with D, Q, Q̄, clock triangle), its Q̄ wired round to D (the left stage of p. 100's circuit). {edge}: CLK under it with up-arrows on the rising edges; {flips}: Q (GREEN) steps 0, 1, 0, 1, one change per rising edge, ch3 s4's toggle waveform. {note}: slide text "Note: FF0 is toggling" under the equation.
> {tee}: beside it, ch3 s5's T flip-flop with T tied to 1, and `Q' = T \oplus Q` becoming `T = 1:\ Q' = \overline{Q}`; a YELLOW "=" between the two symbols.
> {latch}: a small inset of ch2 s2's runaway circuit, the same wiring on a D latch (small square on EN): the EN-high window shaded, Q oscillating in RED inside it. {safe}: back to the flip-flop, the triangle flashes YELLOW at each rising edge; {once}: "one edge, one flip" under the clean GREEN square wave.

[c6.inspect.1] {d0} Let's start with the easiest column, dee zero. {read} Read it down the table. One, zero, one, zero, and so on. {qzero} Now read cue zero, in the current state. Zero, one, zero, one. {pause} {opposite} In every row, dee zero is the opposite of cue zero. {result} So dee zero equals not cue zero. We found that by inspection, just by looking.

[c6.inspect.2] {meaning} What does that mean for flip-flop zero? {feed} Its input is always the complement of its current output. {edge} So at every edge, it loads the opposite of what it holds, {flips} and its output goes zero, one, zero, one. {pause} {note} In the words of the slide, flip-flop zero is toggling.

[c6.inspect.3] {wire} In the circuit, that's a dee flip-flop with its not cue output wired straight back to its dee input. {tee} You met this in part three. It acts as a tee flip-flop with tee stuck at one, so cue prime is not cue. {latch} You saw the same loop in part two, on a latch, where it ran away, flipping again and again for as long as the enable input stayed high. {safe} On a flip-flop it's safe, because a flip-flop listens only at the edge. {once} One edge, one flip.

## Scene 3 · D1 is an exclusive or (ch6_s3_xor)

> s1's table again. {d1}: the D1 column boxed BLUE; {read}: its entries light in turn, 0 1 1 0 0 1 1 0.
> {pair}: copies of the Q1 and Q0 columns slide out of the current-state block (TransformFromCopy) to stand beside D1: three columns `Q_1` | `Q_0` | `D_1`.
> {r1}–{r4}: rows 1–4 light in turn. Where Q1 and Q0 match, the pair glows DIM and D1 shows 0; where they differ, the pair glows YELLOW and D1 shows 1. {rule}: "1 exactly when Q1 ≠ Q0".
> {name}: the XOR truth table from the earlier lecture (p. 15) slides in beside and lines up row for row with ours; then slide p. 100's "Also," and MathTex `D_1 = Q_0 \oplus Q_1`, the ⊕ in YELLOW. {rest}: rows 5–8 light together, the same 0 1 1 0.
> {words}: two small lines, `Q \oplus 0 = Q` ("keep") and `Q \oplus 1 = \overline{Q}` ("flip").
> {hold} / {flip}: in the Q1 column, a curved YELLOW arrow between consecutive rows wherever Q1 changes (rows 2→3, 4→5, 6→7, 8→1 wrapping). {check}: the Q0 = 1 entry in each arrow's starting row lights YELLOW; rows starting at Q0 = 0 get no arrow.

[c6.xor.1] {d1} Next, dee one. {read} Down the table, it reads zero, one, one, zero, zero, one, one, zero. {pause} {pair} That's less obvious, so put the current state beside it, cue one and cue zero, and compare them row by row.

[c6.xor.2] {r1} In the first row, cue one and cue zero are both zero, and dee one is zero. {r2} In the second, they differ, and dee one is one. {r3} In the third, they differ again, and dee one is one. {r4} In the fourth, both are one, and dee one is zero. {rule} So dee one is one exactly when cue one and cue zero differ. {pause} {name} This is called exclusive or, the ex-or from part three. Dee one equals cue zero ex-or cue one. {rest} The last four rows follow the same pattern.

[c6.xor.3] {words} There's a neat way to say this in words. {keep} Remember from part three, an ex-or with zero keeps a bit as it is, and an ex-or with one flips it. {hold} So when cue zero is zero, cue one holds. {flip} And when cue zero is one, cue one flips. {pause} {check} Check it on the table. Every time cue one changes, the row before it has a one in cue zero.

## Scene 4 · A K-map for D2 (ch6_s4_kmap)

> s1's table. {d2}: the D2 column boxed BLUE; {read}: 0 0 0 1 1 1 1 0 light in turn. {stuck}: a faint YELLOW "?" over it. {tool}: s1's chips "Boolean algebra" and "K-maps" return; {choose}: "K-maps" lifts, slide p. 100's "Use a K-map for D2,".
> {inputs}: a small logic box, inputs Q2 Q1 Q0 (GREEN), output D2 (BLUE). {mins}: the four rows with D2 = 1 (011, 100, 101, 110) glow; {four}: their decimal values 3, 4, 5, 6 in GOLD beside them.
> {grid}: an empty K-map in slide p. 100's style: corner label `Q_1Q_0` over `Q_2` with the diagonal, column headings 00 01 11 10, row headings 0 and 1, the slide's bars (`Q_0` over columns 01 and 11, `Q_1` under columns 11 and 10, `Q_2` beside row 1). {rows} / {cols}: the headings light in turn.
> {gray}: neighbouring headings flash in pairs, 00–01, 01–11, 11–10, the one changed bit YELLOW. {wrap}: a YELLOW arc joins the left and right edges (or the map curls briefly into a cylinder); headings 00 and 10 flash with their Q1 bit YELLOW.
> {plot}: each minterm flies from its glowing table row into its cell as a "1" (TransformFromCopy), one per mark: {m3} 011 → row 0, column 11; {m4} 100 → row 1, column 00; {m5} 101 → row 1, column 01; {m6} 110 → row 1, column 10.
> {map}: the remaining cells fill with DIM 0s (the slide leaves them blank). Final map, row Q2 = 0: 0 0 1 0; row Q2 = 1: 1 1 0 1. The table fades; the map carries into s5.

[c6.kmap.1] {d2} Now, the last column, dee two. {read} Down the table, it reads zero, zero, zero, one, one, one, one, zero. {pause} {stuck} No simple pattern jumps out. {tool} When inspection runs out, the traditional tools are Boolean algebra or a kay-map. {choose} Here, we'll use a kay-map.

[c6.kmap.2] {inputs} The logic for dee two has three inputs, the current state bits cue two, cue one and cue zero. {mins} Each row where dee two is one gives a minterm of the function we need. {four} There are four of them, the rows for three, four, five and six.

[c6.kmap.3] {grid} Here's the map. {rows} One row for cue two equals zero, and one for cue two equals one. {cols} The columns are cue one and cue zero, in the order zero zero, zero one, one one, one zero. {gray} That's Gray code order, so neighbouring cells differ in just one variable. {wrap} And the map wraps around. The left and right edges are neighbours too, since zero zero and one zero differ only in cue one.

[c6.kmap.4] {plot} Now plot the minterms, one at a time. {m3} Zero, one, one goes in the top row, under one one. {m4} One, zero, zero goes in the bottom row, first column. {m5} One, zero, one sits right beside it. {m6} And one, one, zero goes in the bottom row, last column. {pause} {map} Four ones, and every other cell is zero.

## Scene 5 · Grouping, and the expression (ch6_s5_groups)

> s4's K-map, centre. Each group gets a loop in its own colour and its term underneath in that colour, as slide p. 100's labels: PINK `Q_0.Q_1.\overline{Q_2}`, PURPLE `\overline{Q_0}.Q_2`, TEAL `\overline{Q_1}.Q_2`.
> {lone}: cell 011 pulses; {around}: its neighbours 001 (left), 010 (right) and 111 (below) flash, each a DIM 0. {alone}: a PINK circle round 011 alone, and its label.
> {corners}: cells 100 and 110 pulse; {far}: a dashed double arrow across the row; {wrap}: the PURPLE loop drawn as the slide does, two half-loops opening off the left and right edges. {read}: inside the group, Q2 = 1 and Q0 = 0 hold steady while the Q1 heading bit flickers 0/1 and is struck out; {term}: the PURPLE label.
> {last}: a TEAL loop round 100 and 101; {drop}: the Q0 bit flickers and is struck out; the TEAL label.
> {ask}: YELLOW "Essential?" {yes}: GREEN "all three are essential". {cover}: each group's private cell flashes in its colour, 011 PINK, 110 PURPLE, 101 TEAL. {shared}: 100 flashes PURPLE and TEAL together, "covered twice: allowed".
> {sum} / {expr}: the three labels fly up into `D_2 = \overline{Q_0}.Q_2 + \overline{Q_1}.Q_2 + Q_0.Q_1.\overline{Q_2}`, each term keeping its colour. {factor}: the two `Q_2`s turn YELLOW; {final}: the second line is built from them, `D_2 = Q_2.(\overline{Q_0} + \overline{Q_1}) + Q_0.Q_1.\overline{Q_2}` (slide p. 100's two lines; the slide's stray dot after `\overline{Q_0}` is dropped). {third}: the PINK term slides down unchanged.
> {slip}: a small copy of the map; {miss}: its PURPLE corner loop turns RED, dashed, and is removed; 110 gets a RED circle of its own. {big}: RED `Q_2.Q_1.\overline{Q_0}` (three variables) beside PURPLE `\overline{Q_0}.Q_2` (two). {still}: GREEN tick "still correct", RED "bigger circuit". The correct map and the two-line equation carry into s6 and s7.

[c6.group.1] {rule} Now group the ones, in blocks whose sizes are powers of two, as large as you can. {lone} Start with the cell zero, one, one. {around} The cells to its left, to its right, and below it all hold zeros. {alone} So it stays on its own, and gives the term cue zero and cue one and not cue two. {pause}

[c6.group.2] {corners} Next, the two ones in the bottom corners. {far} They look far apart, {wrap} but the map wraps around, so they're neighbours. {read} In this pair, cue two is one and cue zero is zero, while cue one changes, so cue one drops out. {term} The term is not cue zero and cue two. {last} The last pair is one, zero, zero with one, zero, one. {drop} Here cue zero changes, so it drops out, leaving not cue one and cue two.

[c6.group.3] {ask} Here's the question the lecturer put to the room. Are these prime implicants essential? {pause=1.5} {yes} Yes, all three. {each} Each group covers a minterm that no other group covers. {cover} Only the single-cell group covers zero, one, one. Only the corner pair covers one, one, zero. Only the last pair covers one, zero, one. {shared} The cell one, zero, zero sits in two groups, and that's allowed.

[c6.group.4] {sum} So dee two is the or of the three terms. {expr} Not cue zero and cue two, or not cue one and cue two, or cue zero and cue one and not cue two. {factor} A little Boolean algebra tidies it up. The first two terms both contain cue two, so factor it out. {final} Cue two goes outside a bracket, and inside it, not cue zero or not cue one. {third} The third term stays as it is.

[c6.group.5] {slip} Here's a common slip. {miss} If you miss the wrap-around, the cell one, one, zero is left on its own, {big} and you get a three-variable term, cue two and cue one and not cue zero, where two variables would do. {still} The answer is still correct, but the circuit is bigger than it needs to be.

## Scene 6 · The circuit, and watching it count (ch6_s6_circuit)

> Slide p. 100's circuit, left to right: FF0, FF1, FF2 (D flip-flop boxes with D, Q, Q̄ and the clock triangle), outputs Q0, Q1, Q2 (GREEN) on wires rising to labels at the top, and CLK (YELLOW) along the bottom. {ffs}: the three boxes; {clk}: the CLK line draws and branches up into every triangle.
> {d0}: FF0's Q̄ wired round to D0 (s2's wiring). {d1}: an XOR gate fed by Q0 and Q1, its output D1 (BLUE). {d2}: a "Combinational logic" block with inputs Q0, Q̄0, Q1, Q̄1, Q2, Q̄2 and output D2 (BLUE).
> {open}: the block opens into the gates of the lecturer's Yenka circuit "sync_ctr" (chip numbers as small DIM labels), with s5's second line small above, each part lighting with its gate: {or} 74HC32 OR of Q̄0 and Q̄1; {and} 74HC08 AND of that with Q2; {three} 74HC11 three-input AND of Q0, Q1 and Q̄2; {join} 74HC32 OR of the two, into D2.
> {sync}: the three clock triangles glow YELLOW; {together}: a CLK pulse runs along the line and all three flash at once. {settle}: between edges, values flow through the gates to D0, D1, D2 (wires bright at 1, dim at 0); at the next edge all three Q's update together.
> {run}: a "1 Hz" clock source on the CLK line; under each output, a "270 Ω" resistor and an LED (lit GREEN, DIM when off). {order}: "LSB" under the left LED, "MSB" under the right, as in the Yenka window. A readout above: Q2 Q1 Q0 in binary, decimal in GOLD. {count}: it steps 0 to 7 with the spoken numbers; {wrap}: 000 = 0.
> {lab}: zoom on one 270 Ω resistor in series with its LED.
> {compare}: split screen. {ripple}: left, ch4 s5's ripple zoom, 111 (7) → 110 (6) → 100 (4) → 000 (0), its staggered traces and the RED false counts 6 and 4. {same}: right, our Q0, Q1, Q2 traces step 111 → 000 on one edge, a single YELLOW guide line through all three. {clean}: GREEN "7 → 0" under ours.

[c6.circuit.1] {build} Now we can build the counter. {ffs} Three dee flip-flops, {clk} and one clock line, wired to every clock input. {d0} Flip-flop zero takes its own not cue output as its input. {d1} Flip-flop one gets an ex-or gate, fed by cue zero and cue one. {d2} And for flip-flop two, there's a block of combinational logic, fed by every output and its complement.

[c6.circuit.2] {open} Open the block, and there's our expression for dee two. {or} An or gate makes not cue zero or not cue one, {and} and an and gate combines that with cue two. {three} A three-input and gate makes cue zero and cue one and not cue two. {join} Finally, an or gate joins the two. {sim} The lecturer built it exactly this way in the simulator.

[c6.circuit.3] {sync} Why is this synchronous? {pause} {together} Because all the clock inputs are connected together, so all three flip-flops change state at the same time. {settle} Between edges, the gates work out the next state, and the next edge loads all of it at once. {key} That's the key thing in a synchronous machine.

[c6.circuit.4] {run} Time to run it, with a one hertz clock and a light on each output. {order} Flip-flop zero is on the left, so the least significant bit is the left-hand light. {count} Zero, one, two, three, four, five, six, seven, {wrap} and back to zero. {lab} One note from the lab. Every light-emitting diode needs a resistor in series, to stop it burning out.

[c6.circuit.5] {compare} Now watch the step from seven back to zero, {ripple} beside part four's ripple counter. {stagger} The ripple counter passed through six and four on its way to zero. {same} Here, all three bits change on the same edge. {pause} {clean} Seven, then zero, with nothing in between.

## Scene 7 · Why it counts: the carry pattern (ch6_s7_carry)

> Ours, beyond the slides; checked by enumeration (3, 4 and 5 bits). {why}: s5's second line, `D_2 = Q_2.(\overline{Q_0} + \overline{Q_1}) + Q_0.Q_1.\overline{Q_2}`.
> {demorgan}: `\overline{Q_0} + \overline{Q_1}` transforms into `\overline{Q_0.Q_1}` (YELLOW tag "De Morgan"). {swap}: a two-row table below it: `Q_1.Q_0 = 0` → `D_2 = Q_2` ("copy"); `Q_1.Q_0 = 1` → `D_2 = \overline{Q_2}` ("flip"). {xor}: the line collapses to `D_2 = Q_2 \oplus Q_1.Q_0`.
> {ladder}: three lines stacked and aligned on the ⊕: {l0} `D_0 = Q_0 \oplus 1`, {l1} `D_1 = Q_1 \oplus Q_0`, {l2} `D_2 = Q_2 \oplus Q_1.Q_0`, the right-hand parts in BLUE. {tee}: ch3 s5's `Q' = T \oplus Q` on the right, with braces naming the BLUE parts `T_0 = 1`, `T_1 = Q_0`, `T_2 = Q_1.Q_0`. {rule}: YELLOW line "a bit toggles when all the bits below it are 1".
> {binary}: ch4 s3's binary column 000 to 111 (decimal in GOLD), the bits that flip at each step turning YELLOW. {carry}: zoom on 011 (3) → 100 (4): the two low 1s glow, all three bits flip, a YELLOW carry arrow sweeps right to left.
> {ripple}: a small inset of ch4's ripple circuit, its stages flipping one after another; {here}: our circuit from s6, its gates lighting before the edge, then all three Q's switching on one edge.
> {four}: a fourth line drops onto the ladder, {d3} `D_3 = Q_3 \oplus Q_2.Q_1.Q_0` (checked on a 0-to-15 counter).

[c6.carry.1] {why} Why does this circuit count? Look at dee two once more. {demorgan} By De Morgan's theorem, not cue zero or not cue one is the complement of cue zero and cue one. {swap} Write it that way, and dee two copies cue two when cue one and cue zero are not both one, and flips it when they are. {xor} That's an ex-or. Dee two equals cue two, ex-or cue one and cue zero.

[c6.carry.2] {ladder} Now line up all three. {l0} Dee zero is cue zero, ex-or one. {l1} Dee one is cue one, ex-or cue zero. {l2} Dee two is cue two, ex-or cue one and cue zero. {tee} Each one follows the rule from part three, cue prime equals tee ex-or cue. {pause} {rule} So each bit toggles exactly when all the bits below it are one.

[c6.carry.3] {binary} That's just binary counting. {carry} Going from three to four, the two low bits are both one, so all three bits flip. That's the carry. {ripple} Part four's ripple counter obeyed the same rule, one stage at a time. {here} Here, the gates work out every flip before the edge, and every flip-flop makes its move on that same edge. {four} Want a fourth bit? {d3} Dee three equals cue three, ex-or cue two and cue one and cue zero.

## Scene 8 · Any count sequence, and recap (ch6_s8_anysequence)

> {general}: slide p. 101's first slide, verbatim: "Synchronous Counter" / "• A similar procedure can be used to design counters having an arbitrary count sequence" / "– Write down the state transition table" / "– Determine the FF excitation (easy for D-types)" / "– Determine the combinational logic necessary to generate the required FF excitation from the current states – Note: remember to take into account any unused counts since these can be used as don't care states when determining the combinational logic circuits". {one}, {two}, {three}: each step lights with a small icon beside it: ch5 s6's table, ch5 s4's `D = Q'`, s5's K-map.
> {unused}: the "Note: remember to take into account any unused counts…" part turns YELLOW. {five}: a ring of six states 000 → 001 → 010 → 011 → 100 → 101 → back to 000 (ch4 s2's ring style), with 110 and 111 outside it, DIM. {never}: those two stay unlit.
> {dc}: three small K-maps for the 0-to-5 counter (s4's layout), X in the cells 110 and 111 of each: D2 rows 0 0 1 0 / 1 0 X X; D1 rows 0 1 0 1 / 0 0 X X; D0 rows 1 0 0 1 / 1 0 X X. {pair}: on the D2 map, a loop joins 011 and the X below it, label `Q_1.Q_0` (checked: with 100 + X at 110 as `Q_2.\overline{Q_0}`, it gives the 0-to-5 counter's D2).
> {recap}: the screen clears to six slots, filled one per sentence, each a small copy of its scene's visual with that sentence's short line under it: {r1} s2's Q0 and D0 columns beside the flip-flop with Q̄ wired back to D, "D0 = Q̄0: FF0 toggles"; {r2} s3's Q1 | Q0 | D1 columns, "D1 = Q0 ⊕ Q1"; {r3} s5's K-map with its PINK, PURPLE and TEAL loops, "three essential prime implicants"; {r4} s6's circuit on its YELLOW CLK line with the readout 111 → 000, "one clock: every bit on the same edge"; {r5} s7's ladder, "a bit flips when all the bits below it are 1"; {r6} this scene's three steps, "table → excitation → logic".
> {line}: the slots shrink; ch1's road returns as one line, "latch → flip-flop → counter". {next}: small sketch of p. 101's shift register (Din into three D flip-flops in a chain, outputs Q0 Q1 Q2, one CLK line); {timing}: the words "set-up and hold times", "clock skew", "metastability" appear under it.
> End card after the last word, held ~8 s; the music carries it.

[c6.any.1] {general} Nothing here depended on counting from zero to seven. {steps} The same procedure designs a counter with any count sequence. {one} First, write down the state transition table. {two} Second, find the flip-flop excitation, which is easy for dee-types. {three} Third, find the combinational logic that makes that excitation from the current state.

[c6.any.2] {unused} And remember the unused counts. {five} Here's an example, a counter from zero to five. {never} It never enters six or seven, so its logic may do anything there. {dc} Those two states become don't cares in every map. {pair} In the map for dee two, the lone cell at zero, one, one can now pair with the don't care below it, and its term shrinks to cue one and cue zero.

[c6.any.3] {recap} Let's recap. {r1} Dee zero is not cue zero, so flip-flop zero toggles. {r2} Dee one is one when cue one and cue zero differ, an ex-or. {r3} For dee two, a kay-map gave three essential prime implicants. {r4} With one clock line, all three bits change on the same edge. {r5} Each bit flips when all the bits below it are one, the carry. {r6} And any count sequence follows the same three steps.

[c6.any.4] {line} That's the whole lecture in one line. A latch, then a flip-flop, then a counter. {next} Next lecture, shift registers, {timing} and the timing rules that keep synchronous circuits working, set-up and hold times, clock skew, and meta-stability.
