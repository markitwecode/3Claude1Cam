# Chapter 1 · Which bits for which state?

Digital Electronics, Lecture 10 (State Assignment), part 1 of 6. Source: slides `combined_26.pdf` pp. 132–135 (to D_c), refresher pp. 120–125 (Lecture 9); recording 00:05:56–00:15:08.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card on {title}: "State Assignment", "Digital Electronics · Lecture 10", "Part 1 · Which bits for which state?"; it clears on {lights}. Lecture conventions, set here and kept for all six parts: flip-flop outputs a, b, c in lowercase (tables read c b a, with a rightmost); a prime is always the next state (c′), an overbar is NOT; products with a centred dot (MathTex `\overline{a}\cdot\overline{c}`), sums with +, ⊕ for exclusive-or. Colours: CLK YELLOW; external inputs BLUE; flip-flop outputs and state bits GREEN; D inputs BLUE; the machine's output GREEN; unused states DIM; K-map loops PINK, PURPLE, TEAL; numbers and costs GOLD; traffic-light lamps in their own red, amber and green, dark when off. No code on screen: every table, map, group, equation and count in this chapter was checked by exhaustive enumeration (Python 3.11.9, itertools.product).
> {lights}: the hero, the traffic light's four states in a ring, laid out as slides pp. 124–125: red at the top, red-and-amber on the right, green at the bottom, amber on the left, arrows clockwise. Each state is a circle holding a small three-lamp column (red top, amber middle, green bottom) with its own lamps lit. A YELLOW dot steps round the ring once. {bits}: below the ring, a row of D flip-flop boxes (L6 `make_ff`), each showing its output as a GREEN 0 or 1.
> {two}: the row holds two flip-flops. {codes2}: GREEN codes appear under the states: red 00, red-and-amber 01, green 10, amber 11. {three}: a third flip-flop slides into the row and the codes transform into Lecture 9's: red 100, red-and-amber 110, green 001, amber 010. {four}: a fourth flip-flop, and the codes become 1000, 0100, 0010, 0001.
> {question}: the codes keep cycling through the three sets; a YELLOW "?" sits between each state and its code; caption "Which bits for which state?"
> {road}: the ring shrinks to the left; on the right, the lecture's road, one chip per mark: {counter} "Parts 1–2: one counter, three ways" (a tiny waveform icon), {wake} "Part 3: waking up in an unused pattern", {onehot} "Part 4: one-hot", {exam} "Parts 5–6: an exam machine, two ways". {refresh}: a small chip "refresher: Lecture 9" lights at the start of the road.

[c1.hook.1] {title} Welcome to lecture ten of Digital Electronics, on state assignment. {lights} Here's a traffic light. It steps through four states, red, then red and amber, then green, then amber, and back to red. {bits} The circuit that drives it is built from flip-flops, and each flip-flop holds just one bit, a zero or a one.

[c1.hook.2] {two} So every state needs its own pattern of bits. {codes2} With two flip-flops, there are exactly four patterns, one for each state. {three} But you could also use three flip-flops, {four} or even four, one per state. {question} Which pattern should stand for which state, and does the choice matter? {pause=1.5}

[c1.hook.3] {road} This lecture answers that in six parts. {counter} First, one small counter, built three ways. {wake} Then what happens when a machine wakes up in a pattern we never planned for. {onehot} Then a style called one-hot, {exam} and a machine from a Cambridge exam question, built two ways. {refresh} The lecture before this one introduced state machines, so we begin with a short refresher.

## Scene 2 · State machines, briefly (ch1_s2_machines)

> Refresher of Lecture 9 (no recording; slides pp. 120–122). {fsm}: heading "Finite State Machine". {def}: p. 121's definition, verbatim: "a deterministic machine (circuit) that produces outputs which depend on its internal state and external inputs", with "internal state" GREEN and "external inputs" BLUE. {memory}: the words "internal state" fly down onto a small flip-flop box.
> {diagram}: p. 123's Moore state diagram, redrawn without its codes: three circles A (top left), B (top right), C (below, between them). {circles}: the three circles pulse. {arcs}: the arcs draw with their BLUE labels exactly as on the slide: A's two self-loops `\overline{e}` and `e\cdot r`; A → B `e\cdot\overline{r}`; B's self-loop `\overline{r}`; B → C `r`; C's self-loop `\overline{e}`; C → A `e\cdot r`; C → B `e\cdot\overline{r}`. {later}: a small forward tag "Part 5"; the diagram shrinks into a corner and fades. (ch5 redraws this machine in the same layout, with names.)
> {schematic}: p. 122's Moore schematic, left to right, with its labels verbatim: "Inputs" (BLUE, bus slash "n") → box "Next state combinational logic" → bus "m" (BLUE: the D inputs) → a D flip-flop box (D, Q, Q̄; L6's symbol) → bus "m" (GREEN) → box "Optional combinational logic" → "Outputs" (GREEN). A "Current state" wire (GREEN) runs from Q back over the top into the first box.
> {logic}: the Inputs wire and the Current state wire light together into the next-state box. {ffs}: the flip-flop box lights. {clk}: "CLK" (YELLOW) draws into its clock triangle. {loop}: a GREEN pulse runs round the Current state loop. {outlogic}: the output box lights, then "Outputs".
> {moore}: label "Moore: outputs from the state alone" under the output box. {mealy}: a dashed BLUE wire (as in p. 122's Mealy schematic) runs from Inputs straight into the output box, label "Mealy: outputs also from the inputs"; it fades, leaving "Moore" with a YELLOW tag "every machine today".
> {noinputs}: the Inputs wire and its label DIM and slide away. {counter}: GREEN tag "a counter (Lecture 6)", with p. 120's words "synchronous state machines (of which counters are a subset)".
> {recipe}: the schematic shrinks to the top; four chips joined by arrows, lit one per mark: {s1} "state diagram" → {s2} "state transition table" → {s3} "next-state logic" → {s4} "output logic (if any)". {dee}: YELLOW `D = Q'` (L6 ch5 s4's) attaches under "next-state logic". This recipe row returns small in s6.

[c1.machines.1] {fsm} So, what is a state machine? {def} A finite state machine is a circuit whose outputs depend on two things, its internal state and its external inputs. {memory} The state is what it remembers, and flip-flops hold it. {diagram} Here's a state diagram. {circles} Each state is a circle. {arcs} Each arc between circles is labelled with the input condition that makes the machine move along it. {later} This particular machine returns in Part five, with names and a job.

[c1.machines.2] {schematic} Here's the shape of the circuit. {logic} The inputs and the current state feed a block of next-state logic. {ffs} Its outputs feed a row of dee flip-flops, {clk} all driven by one clock signal. {loop} Together they hold the current state, and it loops back into the logic. {outlogic} An optional block of output logic turns the state into the outputs.

[c1.machines.3] {moore} When the outputs depend on the state alone, as in this drawing, it's called a Moore machine. Every machine in this lecture is one. {mealy} In a Mealy machine, the outputs also depend directly on the inputs. {noinputs} Now take the inputs away. {counter} What's left is a counter, so the counters you designed in Lecture six were state machines all along.

[c1.machines.4] {recipe} The design recipe is the one you used for counters. {s1} Draw the state diagram. {s2} Write the state transition table. {s3} Find the next-state logic, {s4} then the output logic, if there is any. {dee} And with dee flip-flops, each flip-flop's input is simply its next state.

## Scene 3 · The traffic light's codes (ch1_s3_traffic)

> Lecture 9's example, slides pp. 124–125. {ring}: s1's traffic-light ring returns at centre left (same object: circles with lamp columns; red top, red-and-amber right, green bottom, amber left; arrows clockwise). {order}: a YELLOW dot steps red → red-and-amber → green → amber → red, each state's lamps glowing as the dot arrives. {noinputs}: a YELLOW CLK wave (L6 `clock_wave()`, up-arrows) under the ring, the dot moving once per rising edge; no input wires anywhere. {two}: GOLD "4 states: 2 flip-flops would do".
> {three}: three D flip-flops in a row on the right, Q outputs GREEN; {names} they're labelled R, A, G.
> {red}, {redamber}, {green}, {amber}: each state's code appears beside its circle in GREEN, as on p. 125 ("State 100", "State 110", "State 001", "State 010"), one per mark, while the dot sits on that state and the flip-flop row shows the same three bits.
> {lamps}: a wire from each flip-flop's Q to the matching lamp of a lamp column beside the row (R → red, A → amber, G → green); caption "no output logic".
> {eight}: all eight 3-bit patterns as a 2 × 4 grid of chips (000 … 111); the four used ones light GREEN, each with a tiny lamp icon. {unused}: 000, 011, 101, 111 turn DIM. {name}: label "unused states", with p. 125's line "Unused states, 000, 011, 101 and 111." {dontcare}: an X drops onto each DIM chip, tag "don't care".
> {assign}: the ring with its four codes moves to centre; caption "a state assignment". {hard}: p. 124's line in YELLOW, verbatim: "In general, state assignment is a difficult problem and the optimum choice is not always obvious". {later}: a small forward tag "Part 4". This ring with its codes is recap slot r1 in s8.

[c1.traffic.1] {ring} The last lecture's main example was this traffic light. {order} It runs through four states in the British order, red, red and amber, green, amber, and back to red. {noinputs} It has no inputs, and moves one step on every edge of the clock. {two} With four states, two flip-flops would be enough.

[c1.traffic.2] {three} But the last lecture used three flip-flops, {names} one for each lamp, red, amber and green. {red} Red is one zero zero. {redamber} Red and amber is one one zero. {green} Green is zero zero one, {amber} and amber is zero one zero. {lamps} Each lamp is wired straight to its own flip-flop, so there's no output logic at all.

[c1.traffic.3] {eight} Three bits give eight patterns, and only four are used. {unused} The other four, zero zero zero, zero one one, one zero one and one one one, never occur. {name} They're called unused states. {dontcare} Since they never happen, we don't care what the next-state logic does with them, so in the K-maps they become don't cares.

[c1.traffic.4] {assign} That choice of codes was a state assignment, and that's today's subject. {hard} The last lecture's slides put it plainly. In general, state assignment is a difficult problem, and the optimum choice is not always obvious. {later} The traffic light's next-state logic comes back in Part four, beside a very different design.

## Scene 4 · What makes a good assignment? (ch1_s4_choice)

> p. 132, then p. 133's first slide. {question}: heading "State Assignment" and a YELLOW "?". {depends}: p. 132's lines, verbatim: "As we have mentioned previously, state assignment is not necessarily obvious or straightforward" / "Depends what we are trying to optimise, e.g.,".
> Two branches grow from "optimise". {complexity}: "Complexity", {tech} with two icons, "FPGA" (a grid chip) and "74 series logic chips" (a small DIP chip). {area}: under it, "FF implementation may take less chip area than you may think given their gate level representation": a flip-flop's gate-level drawing (L6's master-slave gates, small) shrinks into a much smaller box. {wiring}: "Wiring complexity can be as big an issue as gate complexity": a tangle of wires between small gates, the wires YELLOW. {speed}: the second branch, "Speed".
> {algorithms}: "Algorithms do exist for selecting the 'optimising' state assignment, but are not suitable for manual execution", the last four words YELLOW.
> {fixed}: the screen clears to the doubling ladder, four rows: "1 flip-flop: 2 patterns", "2: 4", "3: 8", "4: 16", counts GOLD, each row with its patterns small in GREEN beside it (0 1 / 00 01 10 11 / 000 … 111 / sixteen 4-bit patterns as a 4 × 4 block). {ladder}: the rows appear one per spoken number.
> {eight}: a GOLD bracket "8 states" lands on the 3 row. {five}: "5 states": it tries the 2 row, which flashes ("4 < 5"), then lands on the 3 row. {threestates}: "3 states" lands on the 2 row.
> {formula}: p. 133's line "If we have m states, we need at least log₂ m FFs (or more informally, bits) to encode the states" and below it, large, MathTex `\lceil \log_2 m \rceil`, the ceiling brackets YELLOW with the tag "rounded up".
> {more}: GREEN "more than the minimum: allowed". {tl}: s3's ring small beside it, tag "3 flip-flops for 4 states (minimum 2)". {today}: p. 133's "some using more FFs than the minimum". {fun}: the lecturer's words in YELLOW quotes: "just a bit of fun, just to show you how creative you can be". The ladder is recap slot r2 in s8.

[c1.choice.1] {question} So what makes a good state assignment? {pause} {depends} The slides say the choice is not necessarily obvious, because it depends on what you're trying to optimise. {complexity} One goal is a simple circuit, and what counts as simple depends on the technology, {tech} a programmable chip called an FPGA, say, or the seventy-four series logic chips in the lecturer's simulations.

[c1.choice.2] {area} On a chip, a flip-flop may take less room than its drawing in gates suggests. {wiring} And the wiring between gates can be as big a cost as the gates themselves. {speed} Another goal is speed. {algorithms} Algorithms do exist that pick the best assignment, but they're far too heavy to run by hand.

[c1.choice.3] {fixed} One thing is fixed, the minimum number of flip-flops. {ladder} One flip-flop gives two patterns, two give four, three give eight, and four give sixteen. {eight} So eight states need at least three flip-flops. {five} Five states need three as well, since two flip-flops give only four patterns. {threestates} And three states need two. {formula} In general, em states need log base two of em flip-flops, rounded up.

[c1.choice.4] {more} Using more than the minimum is allowed, {tl} as the traffic light did, with three flip-flops for four states. {today} Some of today's designs use more on purpose. {fun} As the lecturer put it, some of them are just a bit of fun, to show how creative you can be.

## Scene 5 · The divide-by-5 counter (ch1_s5_divide5)

> p. 133's second slide. {spec}: heading "Example Problem" and the slide text verbatim: "We wish to investigate some state assignment options to implement a divide by 5 counter which gives a 1 output for 2 clock edges and is 0 for 3 clock edges". {noinputs}: a box with a YELLOW "?" inside; only "CLK" (YELLOW) goes in, no input wires, and "Output" (GREEN) comes out.
> The text shrinks to the top; the chapter's running waveform, p. 133's diagram: CLK (YELLOW, L6 `clock_wave()` with up-arrows) over Output (GREEN), thin vertical guides at every rising edge. {high}: the output rises on a rising edge and stays high for two periods; {low}: it falls on the next edge and stays low for three; {repeat}: the same shape draws again. {edges}: the guides at the output's two changes flash YELLOW, each on a rising edge.
> {five}: a GOLD brace over one output cycle, "5 clock periods". {name}: GOLD "÷ 5" and the title "divide-by-5 counter". {lecture6}: a small inset of L6 ch3 s4's toggle traces with their GOLD labels "f" and "f/2" (and the dim "f/4"). {byfive}: back on our waveform, GOLD "f" beside CLK and "f/5" beside Output.
> {states}: five circles in a ring (L6 `state_ring()` style), one dropping from each period under the brace, arrows round; their codes show "? ? ?" in GREEN. This is the chapter's five-state ring; s6 fills in its codes. {threeffs}: three D flip-flop boxes appear, with GOLD "5 states: 3 flip-flops" (s4's ladder, its 3 row). {names}: their outputs labelled c, b, a in GREEN, the header "c b a", and a small tag on "a": "rightmost bit". The waveform is recap slot r3 in s8.

[c1.divide.1] {spec} Here's the example for the rest of this part and the next two. {noinputs} It has no inputs, only the clock signal. {high} Its output should be one for two edges of the clock, {low} then zero for three, {repeat} and then repeat. {edges} Like everything synchronous, it changes only on a rising edge of the clock.

[c1.divide.2] {five} So one full cycle of the output takes five periods of the clock. {name} That's why it's called a divide-by-five counter. {lecture6} Lecture six's dividers cut the frequency in half, again and again. {byfive} This one divides it by five. {pause}

[c1.divide.3] {states} The pattern repeats every five periods, so the machine needs five states, one for each period of the clock. {threeffs} And five states need three flip-flops, the minimum we just found. {names} Call them see, bee and A. They're written in that order, so the bit on the right is A.

## Scene 6 · Counting in binary (ch1_s6_count)

> p. 134. {simplest}: s5's five-state ring at centre. {numbers}: GOLD 0, 1, 2, 3, 4 appear at the nodes; {bits}: each becomes its GREEN code, 000, 001, 010, 011, 100, one per spoken code; {wrap}: the arrow 100 → 000 lights YELLOW. {name}: heading "Sequential State Assignment" and p. 134's line "Here we simply assign the states in an increasing natural binary count".
> {table}: the ring shrinks to the upper left; a state transition table in L6's `mod_table()` styling: headers "Current state" `c b a` | "Next state" `c' b' a'` (GREEN). {current}, {next}: each header lights. Rows as p. 134: 000 | 001; 001 | 010; 010 | 011; 011 | 100; 100 | 000. {row1}: row 1 draws, a YELLOW arrow from the current to the next state; {row2}: row 2; {rest}: rows 3–5 together, the 100 → 000 row YELLOW for the wrap.
> {unused}: under the table, DIM, p. 134's line "Unused states, 101, 110 and 111."
> {output}: s5's waveform returns small above the table, Output GREEN. {column}: the b column of the current state boxed GREEN; its entries light one by one, 0, 0, 1, 1, 0. {twothree}: a copy of those five bits flies out (TransformFromCopy) and lines up under the waveform, one bit per period, repeating, so the 1 1 sits under the high part and the 0 0 0 under the low part.
> {wire}: p. 134's "The required output is from FF b" and GREEN "Output = b"; "output logic: none". {fluke}: the lecturer's words in YELLOW quotes: "that's just a fluke".
> {dee}: s2's recipe chip with YELLOW `D = Q'` flashes small in a corner. {inputs}: the next-state header gains a BLUE row beneath it, `D_c D_b D_a`. {job}: three BLUE lines on the right, `D_a = ?`, `D_b = ?`, `D_c = ?`. The table (with b's column boxed) carries into s7, shrunk to the left, and is recap slot r4 in s8.

[c1.count.1] {simplest} The most straightforward choice is to count in binary. {numbers} Number the states zero to four, {bits} which in three bits is zero zero zero, zero zero one, zero one zero, zero one one and one zero zero, {wrap} and then back to the start. {name} This is called the sequential state assignment.

[c1.count.2] {table} Now write the state transition table. {current} On the left, the current state, see, bee and A. {next} On the right, the next state, see prime, bee prime and ay prime. {row1} From zero zero zero, the next state is zero zero one. {row2} From zero zero one, it's zero one zero, {rest} and so on, until one zero zero goes back to zero zero zero.

[c1.count.3] {unused} The other three patterns, one zero one, one one zero and one one one, are unused states. {output} So where does the output come from? {pause} {column} Read down the column for flip-flop bee. Zero, zero, one, one, zero. {twothree} That's high for two states in a row, then low for three, going round and round.

[c1.count.4] {wire} So the output is simply flip-flop bee, with no output logic at all. {fluke} As the lecturer put it, that's just a fluke. {dee} And with dee flip-flops, {inputs} the next-state columns are exactly the inputs the flip-flops need. {job} So the job is to find three functions of the current state.

## Scene 7 · Three K-maps (ch1_s7_kmaps)

> pp. 134–135. s6's table stays small at the left. Maps in L6's `kmap()` style (ch6_s4_kmap.py), axes relabelled as p. 134: corner label "b a" over "c" with the diagonal; column headings 00 01 11 10; row headings 0 and 1; the slide's bars ("a" over columns 01 and 11, "b" under columns 11 and 10, "c" beside row 1). Loops with L6's `loop_round()`/`map_loops()`: first group PINK, second PURPLE. Zeros are DIM 0s (the slide leaves them blank).
> {map}: an empty map at centre. {rows}, {cols}: the row headings, then the column headings light. {gray}: neighbouring headings flash in pairs (00–01, 01–11, 11–10), the changed bit YELLOW; a YELLOW arc joins the left and right edges for the wrap-around. {xs}: three X's drop into row c = 1, columns 01, 11 and 10 (101, 111, 110), from the DIM unused line under the table. Cell 100 (row 1, column 00) is a DIM 0 in every map.
> {lecturer}: the lecturer's words in YELLOW quotes, "we have to do Gray coding of these assignments", while the column headings flash again; tag "= the map's order". {codes}: the codes in the table flash GREEN; tag "the codes: free to choose".
> {da}: title "For FF a:"; the a′ column in the table boxed. {plot_a}: 1s fly from rows 000 and 010 (TransformFromCopy) into row 0, columns 00 and 10. Map: row 0 `1 0 0 1`, row 1 `0 X X X`. {ends}: the two 1s pulse; {wrap}: the PINK loop drawn as two half-loops opening off the left and right edges (L6 ch6 s5's corner pair). {term_a}: PINK label `\overline{a}\cdot\overline{c}` and the equation `D_a = \overline{a}\cdot\overline{c}` (D_a BLUE). {nox}: the X's flash and settle DIM, unlooped.
> {db}: title "For FF b:", the map refills with D_b's values. {plot_b}: 1s from rows 001 and 010: row 0 `0 1 0 1`, row 1 `0 X X X`. {pairs}: the X under each 1 pulses. {t1}: PINK vertical pair in column 01, label `a\cdot\overline{b}`; {t2}: PURPLE vertical pair in column 10, label `\overline{a}\cdot b`. {xor}: `D_b = a\cdot\overline{b} + \overline{a}\cdot b = a \oplus b`, the ⊕ YELLOW. {spare}: the X at 111 flashes and stays DIM, unlooped.
> {dc}: title "For FF c:", D_c's map. {plot_c}: the 1 from row 011: row 0 `0 0 1 0`, row 1 `0 X X X`. {pair_c}: PINK vertical pair in column 11, through the X at 111; {term_c}: label `a\cdot b` and `D_c = a\cdot b`.
> {compare}: the three maps shrink into a row, each equation under its map, the looped X's glowing in their loop colours and the rest DIM. The row of maps carries into s8 and is recap slot r5.

[c1.kmaps.1] {map} Each of those functions gets a three-variable K-map. {rows} Its two rows are for flip-flop see at zero and at one. {cols} Its four columns are for bee and A, in the order zero zero, zero one, one one, one zero. {gray} That's Gray code order, so neighbouring cells differ in just one bit. {xs} And the three unused states go in as don't cares, marked with an ex.

[c1.kmaps.2] {lecturer} When the lecturer says we have to do Gray coding of these assignments, he means this order along the edge of the map. {codes} The state codes themselves can be any patterns you like. That freedom is what this lecture is about.

[c1.kmaps.3] {da} First, flip-flop ay. {plot_a} Its next state is one in two rows, from zero zero zero and from zero one zero. {ends} Those cells sit at the two ends of the top row, {wrap} and since the map wraps around, they're neighbours. {term_a} In that pair, both A and see are zero, so the input to flip-flop A is not A and not see. {nox} The don't cares would only help by making a bigger group, and none is possible here, so they're left out.

[c1.kmaps.4] {db} Next, flip-flop bee. {plot_b} Its ones are at zero zero one and zero one zero. {pairs} Each pairs with the don't care right below it. {t1} The first pair gives ay and not bee, {t2} and the second gives not ay and bee. {xor} Together, that's one exactly when ay and bee differ, which is the exclusive-or of ay and bee. {spare} The third don't care, at one one one, stays out.

[c1.kmaps.5] {dc} The last one is the see flip-flop. {plot_c} There's a single one, at zero one one. {pair_c} It pairs with the don't care below it, {term_c} so the input to flip-flop see is ay and bee. {pause} {compare} For flip-flop A, the don't cares gave no help at all. For bee and see, they doubled every group.

## Scene 8 · The circuit, and recap (ch1_s8_circuit)

> The circuit as in the lecturer's simulation "Divide by 5 Example - Sequential State Assignment" (frame at 00:14:30). {ffs}: three D flip-flops (L6 `make_ff`) left to right, labelled a, b, c, Q outputs GREEN; {clk}: one YELLOW CLK line into every clock triangle. {order}: a small copy of s6's header "c b a" with a right-to-left arrow under it, beside the circuit's a, b, c with a left-to-right arrow.
> Gates (L6 `and_gate`, `xor_gate`), each one's equation flying down from s7's row of maps to its gate (TransformFromCopy): {da}: an AND fed by Q̄ of a and Q̄ of c (the Q̄ wire from c runs back left along the bottom) into D_a (BLUE); {db}: an exclusive-or of a and b into D_b; {dc}: an AND of a and b into D_c. Small DIM chip numbers as in the simulation: 74HC08, 74HC86, 74HC08, flip-flops 74HC74.
> {out}: a GREEN "Output" label on b's Q wire. {run}: a "1 Hz" clock source (L6 `clock_source()`) on the CLK line; an LED (L6 `led`/`set_led`) under each Q. {leds}: the circuit runs from 000, and the LEDs step 000 → 001 → 010 → 011 → 100 → 000 (a's LED on the left). Below, a plot of CLK (YELLOW) and the output (GREEN); the simulator draws them red and blue, but we keep our colours. {high}: the output trace high for two periods; {low}: low for three; {again}: repeating, a ghost of s5's waveform laid over it, matching.
> {score}: the lecture's scoreboard appears top right, columns "assignment", "flip-flops", "next-state gates", "output logic". {row}: its first row, "binary | 3 | 3 | none", numbers GOLD. (ch2 adds sliding and ring.)
> {recap}: the screen clears to six slots, filled one per sentence, each a small copy of its scene's visual (same object, colours and styling) with the line under it: {r1} s3's traffic-light ring with codes 100, 110, 001, 010, "a pattern of bits for each state"; {r2} s4's doubling ladder with `\lceil \log_2 m \rceil`, "m states: ⌈log₂ m⌉ flip-flops"; {r3} s5's waveform with its GOLD "÷ 5", "5 states: 3 flip-flops"; {r4} s6's table with b's column boxed GREEN, "output = b"; {r5} s7's three maps with their loops, "unused states as don't cares"; {r6} this scene's circuit with its scoreboard row, "3 flip-flops, 3 gates".
> {next}: the slots clear; the circuit returns alone, and a GOLD 1 hops from flip-flop a to b to c, as in L8 ch2 s3's shift register. {vanish}: its three gates fade one by one, leaving gaps in the wires, and a YELLOW "?" appears where the logic was. End card after the last word, held ~8 s; the music carries it.

[c1.circuit.1] {ffs} Now build it, with three dee flip-flops, {clk} all driven by the same clock signal. {order} They're drawn from left to right as A, then bee, then see, just as the lecturer drew them, so the circuit runs the opposite way to the table. {da} An and gate takes the inverted outputs of A and see, and feeds flip-flop A. {db} An exclusive-or gate of A and bee feeds flip-flop bee. {dc} And a second and gate, of A and bee, is the input to flip-flop see.

[c1.circuit.2] {out} The output is taken straight from flip-flop bee. {run} The lecturer ran it in his simulator, with a clock signal at one hertz. {leds} The lights show the state, counting up through all five codes, then back to zero zero zero. {high} The output is high for two periods, {low} low for three, {again} and round again. {score} Let's start a scoreboard. {row} Counting in binary costs three flip-flops, three gates, and no output logic.

[c1.circuit.3] {recap} Let's recap. {r1} A state assignment picks a pattern of bits for each state. {r2} With em states, you need at least log base two of em flip-flops, rounded up. {r3} The divide-by-five counter has five states, so it needs three. {r4} Counting in binary, the output came free from flip-flop bee. {r5} K-maps with the unused states as don't cares gave the next-state logic, {r6} and the circuit came to three gates.

[c1.circuit.4] {next} Next time, the lecturer shows some more funky assignments, built on the way a shift register moves its bits. {vanish} What if the codes are chosen so that the logic almost disappears?
