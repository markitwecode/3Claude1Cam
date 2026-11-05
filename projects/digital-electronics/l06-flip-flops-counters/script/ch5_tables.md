# Chapter 5 · Designing a synchronous counter: the tables

Digital Electronics Lecture 6 (Flip-flops and Counters), part 5 of 6. Source: slides
(combined_26.pdf) pp. 95–99, with callbacks to p. 82 (RS state transition table) and p. 90
(J-K truth table); recording 00:42:53–00:53:21.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch5_s1_hook)

> Title card: "Flip-flops and Counters", "Digital Electronics · Lecture 6", "Part 5 · Designing a synchronous counter". It clears on {ripple}.
> {ripple}: ch4 s3's ripple counter, upper half: three negative-edge T flip-flops (bubble + triangle on the clock input), each T tied to 1; CLK (YELLOW) into the first only, Q0 into the second's clock input, Q1 into the third's. Outputs Q0, Q1, Q2 GREEN.
> {stagger}: ch4 s5's 7 → 0 zoom under it, same styling: the readout Q2 Q1 Q0 steps `111 = 7` → `110 = 6` → `100 = 4` → `000 = 0`, each step a little later than the last; `6` and `4` in RED.
> {fix} / {oneclock}: the Q0 → clock and Q1 → clock wires go RED and fade; the YELLOW CLK line extends along the bottom and branches into all three clock inputs; the bubbles vanish (triangles stay: rising edge). A YELLOW pulse runs along the line and reaches all three boxes in the same frame.
> {together}: the readout replays from `111 = 7` straight to `000 = 0`, all three bits flipping in one step, GREEN.
> {but}: the "1" ties on the T inputs fade; each box becomes a D flip-flop (D, Q, Q̄, triangle), its D input BLUE with a BLUE "?" on the wire. {tell}: the three "?" pulse in turn.
> {question}: YELLOW line under the circuit: "What should each flip-flop's input be?" Hold on the pause.

[c5.hook.1] {title} Last time, we built a ripple counter. {ripple} Each flip-flop in it was clocked by the output of the one before. {stagger} So on the step from seven back to zero, the outputs passed through six, and then four, before they settled. {pause}

[c5.hook.2] {fix} The fix sounds simple. {oneclock} Wire one clock to every flip-flop, so they all change on the same edge. {together} Then seven could go straight to zero, in a single step. {but} But now no flip-flop can wait for its neighbour. {tell} At every edge, something has to tell each flip-flop what to become next. {question} So how do we work out what each flip-flop's input should be? {pause}

## Scene 2 · Synchronous design (ch5_s2_sync)

> Slide p. 95's advice as two short cards, each with the hook's circuit shrunk beside it: RED "Ripple counters: should not usually be used" (the chained clocks), GREEN "Synchronous designs: recommended" (one CLK line).
> {clocks}: the cards clear and the hero arrives, built from the hook's end shot: three D flip-flops in a row, FF0 on the left as on slide p. 100 (so ch6 s6's circuit grows out of this one). Outputs Q0, Q1, Q2 GREEN, inputs D0, D1, D2 BLUE, one YELLOW CLK line along the bottom into every triangle.
> {same}: a YELLOW pulse along CLK; all three Q outputs change in the same frame (bright for 1, dim for 0).
> {price}: GOLD tag "the price: more combinational logic". {type}: a smaller line under it, "(different for each flip-flop type)". {wiring}: a tiny DIM copy of the ripple chain's Q0 → clock wire, crossed out.
> {structure}: a big rounded box "combinational logic" appears above the flip-flops. {current}: the Q wires (GREEN) run up into the box, labelled "current state". {block}: the box glows. {next}: three BLUE wires come down out of it into D2, D1, D0, labelled "next state".
> {edge}: a YELLOW pulse on CLK; the values on the D wires jump into the Q outputs together, flow up into the box, and new values come out: the loop goes round once more.
> {donly}: caption "D flip-flops only (the technique extends to other types)". {example}: ch4 s2's ring of eight states, `000` … `111`, decimal beside each, appears small to the right, labelled "0 to 7 up-counter".
> {job}: a YELLOW "?" fills the logic box and stays. {build}: DIM caption "this chapter: what it must produce · next chapter: the gates".

[c5.sync.1] {rule} Because of those problems, the slides advise against ripple counters. Use a synchronous design instead. {clocks} In a synchronous design, every flip-flop's clock input is connected directly to the clock signal. {same} So all the outputs change at the same time, on the same edge. That's what synchronous means.

[c5.sync.2] {price} There's a price. {logic} Since no flip-flop listens to its neighbour any more, we need more complex combinational logic to produce each flip-flop's input. {type} And that logic is different for each type of flip-flop we might choose. {wiring} In the ripple counter, the wiring did the counting. Here, the logic has to do it.

[c5.sync.3] {structure} Here's the shape of every synchronous counter. {current} The flip-flop outputs, cue two, cue one and cue zero, hold the current state. {block} They feed a block of combinational logic. {next} The block's outputs drive the dee inputs, and say what the next state should be. {edge} At the next rising edge, all three flip-flops load it at once, and the loop goes round again.

[c5.sync.4] {donly} In this course, we design with dee flip-flops only, although the same technique works for other types. {example} Our example is a zero to seven up-counter, the same count as last time. {job} Everything comes down to that logic block. {build} In this part, we work out exactly what it has to produce. In the next part, we build it from gates.

## Scene 3 · The state transition table, again (ch5_s3_statetable)

> {rs}: ch1 s2's RS table returns as ch1 left it (slide p. 79, same styling), with a small NOR latch icon from ch1 s2 beside it: `S R | Q′ Q̄′ | comment`, `0 0 | Q Q̄ | hold`, `0 1 | 0 1 | reset`, `1 0 | 1 0 | set`, `1 1 | 0 0 | illegal`.
> {unfold}: it unfolds into slide p. 82's state transition table: a GREEN Q column grows on the left, the four rows copy into two blocks (Q = 0 above, Q = 1 below), the hold rows' "Q" resolves to 0 and to 1, and the Q̄′ column fades. Result, verbatim: header `Q S R | Q′ | comment`; rows `0 0 0 | 0 | hold`, `0 0 1 | 0 | reset`, `0 1 0 | 1 | set`, `0 1 1 | 0 | illegal`, `1 0 0 | 1 | hold`, `1 0 1 | 0 | reset`, `1 1 0 | 1 | set`, `1 1 1 | 0 | illegal` (checked by enumeration: with NOR gates both outputs are 0 in the illegal rows). Q and Q′ GREEN, S and R BLUE, "illegal" RED.
> {cols}: braces under the three column groups in turn: "current state", "inputs", "next state". {rows}: the two blocks of four rows flash in turn (Q = 0, then Q = 1). {read}: the row `0 1 0 | 1 | set` lights YELLOW, with an arrow from its left part to its Q′.
> {counter}: the RS table shrinks to the upper left and DIMs. The counter's table begins in slide p. 99's layout: headers "Current state" `Q2 Q1 Q0` and "Next state" `Q2′ Q1′ Q0′` (GREEN), cells empty.
> {noinputs}: a small YELLOW tag "only input: CLK" beside it. {pair}: an arrow from the current-state group to the next-state group.
> {example}: one row filled: `0 1 1 | 1 0 0`, with GOLD `3` and `4` beside the halves.
> {modified}: a third column group slides in at the right, header "FF inputs" `D2 D1 D0` (BLUE), cells empty. {inputs}: a BLUE arrow from those columns down to a tiny D flip-flop. {excitation}: a YELLOW brace over them, "excitation", and a title above: "Modified state transition table". This empty skeleton (minus the sample row) is what s6 fills.

[c5.table.1] {recall} To design that logic, we'll use a tool from last lecture. {rs} In part one, we wrote the reset-set latch's behaviour as a table, with plain cue standing for the current state. {unfold} The state transition table spells that out. {cols} Now cue, the current state, gets a column of its own, beside the set and reset inputs. Then comes cue prime, the next state. {rows} That makes eight rows, hold, reset, set and illegal, once with cue at zero, and once with cue at one. {read} Read any row, and it tells you where the latch goes next.

[c5.table.2] {counter} A counter's table is simpler. {noinputs} Apart from the clock, it has no inputs at all. {pair} So each row is just a current state, and the next state we want. {example} For example, in state three, written zero, one, one, the next state must be four, written one, zero, zero.

[c5.table.3] {modified} For design, we add more columns. {inputs} They hold each flip-flop's input, the value that makes the next edge take it to that next state. {excitation} Those required inputs are known as the excitation, and the bigger table is called the modified state transition table. {pause}

## Scene 4 · The D excitation table (ch5_s4_dexcite)

> A D flip-flop (ch2 s6's symbol: D, Q, Q̄, triangle) with Q showing 0 (GREEN), a note "want Q′ = 1" beside its output, and a BLUE "D = ?" on its input.
> {truth}: two arrows under it: "truth table: inputs → next state", pointing right; then {backwards} "excitation table: current state, next state → input", pointing left, in YELLOW.
> The table from slide p. 97 (checked by enumeration), header `Q Q′ | D`: `0 0 | 0` on {r1}, `0 1 | 1` on {r2}, `1 0 | 0` on {r3}, `1 1 | 1` on {r4}. Each row arrives with a tiny before → after strip (Q then Q′) beside it. Q, Q′ GREEN, D BLUE.
> {copy}: the Q′ column glows; a copy slides across onto the D column and matches it cell for cell.
> {rule}: "D = Q′" large (D BLUE, Q′ GREEN), from slide p. 97. {current}: the Q column DIMs, tagged "makes no difference".
> {little}: hold. {other}: a J-K flip-flop symbol (ch3 s3: J, K, triangle, Q, Q̄) slides in at the right with a YELLOW "?", leading into s5.

[c5.dexc.1] {reverse} To fill in those columns, we need each flip-flop's excitation table. {question} It answers a reverse question. {given} Given the current state, cue, and the next state we want, cue prime, what input must we apply? {truth} A truth table goes forwards, from the inputs to the next state. {backwards} An excitation table goes backwards. {pause}

[c5.dexc.2] {dff} For a dee flip-flop, it's easy. {r1} To go from zero to zero, set dee to zero. {r2} From zero to one, set dee to one. {r3} From one to zero, set dee to zero. {r4} And from one to one, set dee to one. {pause} {copy} Now look down the columns. The dee column is a copy of the cue prime column.

[c5.dexc.3] {rule} So for a dee flip-flop, dee equals cue prime. {current} The next state depends only on dee. The current state makes no difference. {little} So for dee flip-flops, the excitation table adds very little. {other} For other types, such as the jay-kay flip-flop, the current state matters, and that's where an excitation table earns its keep.

## Scene 5 · The J-K excitation table (ch5_s5_jkexcite)

> Two tables side by side, as on slide p. 98. Left, "Truth table": ch3 s3's J-K table in its styling, cut to slide p. 98's Q′ column, with ch3's comments kept: `J K | Q′`: `0 0 | Q | hold`, `0 1 | 0 | reset`, `1 0 | 1 | set`, `1 1 | Q̄ | toggle`. {roles}: small BLUE tags "J acts as S" over J and "K acts as R" over K. Right, "Excitation table": header `Q Q′ | J K`, rows `0 0`, `0 1`, `1 0`, `1 1`, with the J and K cells empty. J, K BLUE; Q, Q′ GREEN.
> For each transition, its row on the right lights YELLOW, and the truth-table rows that produce it get YELLOW boxes. Their J values, then their K values, fly across (TransformFromCopy) into the empty cells. Two equal values merge into that value; a 0 and a 1 merge into a lowercase `x`.
> {t00}: the row `0 0` lights; {hold} and {reset} box those two rows. {jzero}: J 0, 0 → `0`. {kfree}: K 0, 1 → `x`, which flashes YELLOW on {x}.
> {t01}: set and toggle → `1 x`. {t10}: reset and toggle → `x 1`. {t11}: the row `1 1` lights and its cells show a YELLOW "?" through the pause; {t11ans}: hold and set get their boxes → `x 0`.
> The finished table, verbatim from slide p. 98 (and checked by enumeration): `0 0 | 0 x`, `0 1 | 1 x`, `1 0 | x 1`, `1 1 | x 0`.
> {one}: the four `x` cells pulse one after another, one per row. {free}: a small generic 2-by-2 K-map below, DIM: cells `1`, `1`, `X`, `0`; a loop grows round the two 1s and the X together, larger than the loop round the 1s alone would be. {dnone}: s4's `Q Q′ | D` table, small, beside it: no `x` anywhere. Both fade before s6.

[c5.jk.1] {other} You can work out an excitation table for any type of flip-flop, and whenever you design with some other type, that's the table to use. {jk} Take the jay-kay flip-flop. {truth} On the left is its truth table, from part three. {rows} Zero, zero is hold. Zero, one is reset. One, zero is set. And one, one is toggle. {roles} Here, jay plays the part of set, and kay the part of reset. {goal} On the right, we'll build its excitation table, one transition at a time.

[c5.jk.2] {t00} First, zero to zero. Which rows can do that? {pause} {hold} Hold keeps cue at zero. {reset} And reset forces it to zero. {jzero} In both rows, jay is zero. {kfree} But kay is zero in one of them, and one in the other, so kay can be either. {x} We call that a don't care, and write it as a small ex. So jay is zero, and kay is ex.

[c5.jk.3] {t01} Next, zero to one. Set does it, and so does toggle, since toggling a zero gives a one. Both have jay equal to one, so jay is one, and kay is a don't care. {t10} Then one to zero, by reset or by toggle. Here kay must be one, and jay is a don't care. {t11} Finally, one to one. Which rows give that? Try this one yourself. {pause=1.5} {t11ans} Hold, or set. So kay must be zero, and again, jay is a don't care.

[c5.jk.4] {done} Look at the finished table. {one} Every row has exactly one don't care. {free} Each one is a free choice, and when we design the logic, a kay-map can use those free cells to make bigger groups, and a simpler circuit. {dnone} The dee table, by contrast, has no free choices at all.

## Scene 6 · The counter's modified table (ch5_s6_modtable)

> s3's empty skeleton returns, full size, in slide p. 99's layout: "Current state" `Q2 Q1 Q0` | "Next state" `Q2′ Q1′ Q0′` (GREEN) | "FF inputs" `D2 D1 D0` (BLUE), eight empty rows. To the right, p. 99's procedure as three short numbered lines, revealed one at a time on {step1}, {step2}, {step3}: "1. Write down the desired count sequence in the current state columns", "2. Write down the required next states in the next state columns", "3. Fill in the FF inputs required to give the defined next state".
> {three}: three small D flip-flop icons, then GOLD "2³ = 8 states". {current}, {next}, {inputs}: each header group glows in turn; a small "MSB" tag under Q2.
> {count}: ch4's binary column `000` … `111` flies in (TransformFromCopy) and fills the current-state columns, with each row's decimal value 0 … 7 in GOLD at the left. {order}: a downward arrow beside the column, "count order".
> {step2}: each next-state cell group is born from a copy of the row below's current state: {r0} row 0 gets `0 0 1`, {r1} row 1 gets `0 1 0`, then the rest fill quickly on {down}. {wrap}: the last row gets `0 0 0`, copied from row 0's current state along a curved arrow from the top of the table to the bottom.
> {step3} / {lookup}: s4's small table `Q Q′ | D` and "D = Q′" sit beside the table. {copy}: the three next-state columns slide right as copies into the D columns.
> The full table, verbatim from slide p. 99 (checked by enumeration): `0 0 0 | 0 0 1 | 0 0 1`, `0 0 1 | 0 1 0 | 0 1 0`, `0 1 0 | 0 1 1 | 0 1 1`, `0 1 1 | 1 0 0 | 1 0 0`, `1 0 0 | 1 0 1 | 1 0 1`, `1 0 1 | 1 1 0 | 1 1 0`, `1 1 0 | 1 1 1 | 1 1 1`, `1 1 1 | 0 0 0 | 0 0 0`.
> {skip}: an "=" sign between the next-state group and the D group, and the slide's note under the table: "Note: Since D = Q′, for a D-FF, the required FF inputs are identical to the required next state". The D group DIMs briefly, then comes back.
> {fn}: the three D columns glow BLUE as columns of eight bits; {logic}: s2's logic box, small, with Q2 Q1 Q0 arrows in and D2 D1 D0 arrows out. {keep}: the table alone, settled. This exact table opens ch6.

[c5.mod.1] {need} Now the counter itself. {three} To count from zero to seven, we need eight states, and three flip-flops give two to the power three, which is eight. {layout} The table has three groups of columns. {current} The current state, cue two, cue one and cue zero, with cue two as the most significant bit. {next} The next state, cue two prime, cue one prime and cue zero prime. {inputs} And the flip-flop inputs, dee two, dee one and dee zero.

[c5.mod.2] {step1} There are three steps. Step one, write the count sequence down the current state columns. {count} That's zero to seven in binary, from zero, zero, zero, at the top, to one, one, one, at the bottom. {order} It's the same binary column as last time, and it's the order we want the counter to step through.

[c5.mod.3] {step2} Step two, write down the state the counter must go to next. {add} That's just the count plus one. {r0} After zero, zero, zero comes zero, zero, one. {r1} After zero, zero, one comes zero, one, zero. {down} And so on, down the table. {wrap} In the last row, after one, one, one, the counter goes back to the start, so its next state is zero, zero, zero. {pause}

[c5.mod.4] {step3} Step three, fill in the inputs that give each next state. {lookup} For each bit, we look up its transition in the excitation table. {copy} For dee flip-flops, the answer is always dee equals cue prime, so each dee column is a copy of its next state column. {pause} {skip} In fact, with dee flip-flops, you can skip writing the input columns entirely. They're identical to the next state.

[c5.mod.5] {fn} So here's what the logic block must produce. {columns} Each of dee two, dee one and dee zero is a column of eight bits, one for every current state. {logic} The logic has to compute those columns from cue two, cue one and cue zero. {keep} Keep this table in mind. It's the one we'll turn into gates.

## Scene 7 · If we'd used J-K flip-flops (ch5_s7_jkcolumns)

> s6's table, with the D group sliding out and six empty BLUE columns sliding in: `J2 K2 J1 K1 J0 K0` (on {names}, each header lights as it's said). s5's finished J-K excitation table, small, in the corner as the lookup: `0 0 | 0 x`, `0 1 | 1 x`, `1 0 | x 1`, `1 1 | x 0`.
> {first}: row 0's Q0 cell and Q0′ cell light YELLOW. {t01}: tag "0 → 1". {look}: the lookup row `0 1 | 1 x` lights. {cell1}: its `1 x` flies (TransformFromCopy) into row 0's J0 and K0 cells.
> {second} / {cell2}: row 1, Q0 1 → 0; the row `1 0 | x 1` lights and `x 1` flies into row 1's J0 K0.
> {rest}: the other six rows of J0 and K0 fill quickly, each from its lookup row. {pattern}: the two columns, verbatim: J0 `1 x 1 x 1 x 1 x`, K0 `x 1 x 1 x 1 x 1` (checked by enumeration).
> {choose}: every `x` in those two columns flashes YELLOW and turns into `1`. {toggle}: J0 and K0 read all 1s; beside them, ch3 s4's toggling waveform, small: Q0 flipping on every rising CLK edge, labelled "J = K = 1: toggle".
> {others}: the other four columns fill fast, in a lighter weight, verbatim per row (checked by enumeration): J2 K2 J1 K1 = `0 x 0 x`, `0 x 1 x`, `0 x x 0`, `1 x x 1`, `x 0 0 x`, `x 0 1 x`, `x 0 x 0`, `x 1 x 1`. Every J/K pair holds exactly one `x`; the x's flash once.
> {contrast}: the J-K columns slide out and the D columns slide back in, under a GREEN tag from slide p. 101: "excitation: easy for D-types". End on s6's table.

[c5.jkcol.1] {swap} Now suppose we'd built the counter from jay-kay flip-flops instead. {cols} Each flip-flop has two inputs, so the input columns double. {names} They're jay two, kay two, jay one, kay one, jay zero, kay zero. {lookup} And this time, filling them in takes a real lookup.

[c5.jkcol.2] {first} Take the first row, and look at cue zero. {t01} It goes from zero to one. {look} In the excitation table, zero to one needs jay equal to one, and kay is a don't care. {cell1} So jay zero is one, and kay zero is ex. {second} In the second row, cue zero goes from one to zero. {cell2} That needs jay to be a don't care, and kay equal to one. {pause}

[c5.jkcol.3] {rest} Fill in the rest of those two columns the same way. {alt} Cue zero alternates, zero, one, zero, one, so every row is one of those same two transitions. {pattern} Down the table, jay zero reads one, ex, one, ex, and kay zero reads ex, one, ex, one. {choose} Now use the freedom, and make every don't care a one. {toggle} Then jay zero and kay zero are both one in every row, and as we saw in part three, that means toggle. The first flip-flop simply toggles on every edge. {pause}

[c5.jkcol.4] {others} The other four columns fill in the same way, one lookup per cell, and each jay and kay pair gets exactly one don't care. {contrast} With a dee flip-flop, that whole step disappears, because its input is simply the next state. So for dee-types, the excitation step is easy.

## Scene 8 · Recap and next (ch5_s8_recap)

> One small visual per sentence, each in its scene's colours and styling, laid out left to right in two rows of three, with the sentence's short line under it:
> {r1}: s2's three D flip-flops on one YELLOW CLK line, under the "combinational logic" box with its "?" — "one clock, logic makes the inputs".
> {r2}: s3's small DIM RS table beside the counter's two column groups, a third group (`D2 D1 D0`, BLUE) growing in under the YELLOW "excitation" brace — "the modified table adds the inputs".
> {r3}: s4's `Q Q′ | D` table with "D = Q′" — "excitation works backwards".
> {r4}: s5's J-K excitation table with its four `x` cells lit — "one don't care per row".
> {r5}: s6's 0-to-7 table with the "=" between next state and D — "D columns = next state".
> {r6}: s7's J0 K0 columns, all 1s after the swap — "with J-K: a lookup per cell".
> {next}: the six shrink away; s6's table stays alone in the centre, and three small arrows leave its D columns towards a faint gate outline (ch6's circuit), with a tiny K-map grid beside it. Then the end card: hold about 8 seconds after the last word, music carrying it.

[c5.recap.1] {recap} Here's a quick recap. {r1} In a synchronous counter, one clock drives every flip-flop, and combinational logic works out each flip-flop's input from the current state. {r2} The modified state transition table lists each current state, its next state, and the inputs needed to get there, the excitation. {r3} An excitation table works backwards, and for a dee flip-flop, dee equals cue prime.

[c5.recap.2] {r4} The jay-kay excitation table comes straight from its truth table, with one don't care in every row. {r5} For our zero to seven counter, the dee columns are simply the next state. {r6} With jay-kay flip-flops, every input takes a lookup, and the first stage just toggles. {pause} {next} Next time, we turn those dee columns into gates, first by inspection, then with a kay-map. And then we watch the complete counter in action.
