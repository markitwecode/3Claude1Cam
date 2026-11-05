# Chapter 2 · More flip-flops, less logic

Digital Electronics, Lecture 10 (State Assignment), part 2 of 6. Source: slides `combined_26.pdf` pp. 135 (Sliding State Assignment)–137 (Shift Register Assignment), with p. 132 for scene 7; recording 00:15:08–00:25:40 and 00:29:59–00:30:40.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card: "State Assignment", "Digital Electronics · Lecture 10", "Part 2 · More flip-flops, less logic". ch1's conventions hold all chapter: flip-flop outputs and state bits GREEN, D inputs BLUE, CLK YELLOW, travelling 1s GOLD, unused states DIM, scoreboard numbers GOLD; products with a centred dot, an overbar for NOT, a prime only for the next state. Every table, column, K-map and count in this chapter was checked by exhaustive enumeration (Python 3.11.9, itertools.product); no code on screen.
> {title}: the title card alone on an empty frame, styled as this project's ch1_s1_hook.py title card (or L8's ch2_s1_hook.py if ch1's isn't built): "State Assignment" large, "Digital Electronics · Lecture 10" under it, and the part line "Part 2 · More flip-flops, less logic". It holds through the first sentence and clears just before {last}.
> {last}: ch1 s8's finished circuit, small, upper left: D flip-flops a, b, c left to right on one YELLOW CLK line; an AND of the Q̄ outputs of a and c into D_a, an exclusive-or of a and b into D_b, an AND of a and b into D_c; the output taken from b (GREEN). Beside it, ch1's scoreboard as it was left: header "assignment | flip-flops | next-state gates | output logic", one row "binary | 3 | 3 | none".
> {gates}: the two AND gates, then the exclusive-or, pulse YELLOW as they're named.
> {same}: centre, ch1's five-state ring (L6 `state_ring()` style) with the binary codes 000, 001, 010, 011, 100 under its nodes, GREEN.
> {fun}: two small quote cards, the lecturer's words: "just a bit of fun" and "you wouldn't necessarily do it in anger".
> {question}: the five codes under the nodes turn into YELLOW "???"; in the small circuit the three gates dim behind a YELLOW "?". {pay}: a small GOLD "?" beside the scoreboard's flip-flops column.

[c2.hook.1] {title} Last time, you built a divide-by-five counter by giving its five states a plain binary count. {last} It worked, and its next-state logic cost three gates. {gates} Two and gates, and an exclusive-or. {pause}

[c2.hook.2] {same} This time, the same five states get some funkier codes. {fun} The lecturer calls them just a bit of fun, not something you'd necessarily do for real. But they show how much freedom you have when you choose the codes. {question} Can a cleverer choice make the logic almost disappear? {pause} {pay} And if it can, what do you pay for it instead? {pause}

## Scene 2 · The ones slide (ch2_s2_sliding)

> {cells}: hero, upper centre: three square flip-flop cells in a row, labelled c, b, a (GREEN), in the table's order with a on the right, each holding a DIM 0. Each edge of the clock is a small YELLOW tick under the row. {name}: title "Sliding State Assignment" (p. 135).
> {enter}: a GOLD 1 slides into cell a from the right (001). {follow}: it moves into b as a second GOLD 1 enters a (011). {together}: both move one cell left (110). {drop}: the first falls off past c and fades (100). {empty}: the second follows it off (000).
> As each code forms, a copy drops (TransformFromCopy) into a column on the left headed "c b a": 000, 001, 011, 110, 100, with a curved arrow from 100 back to 000. {codes}: the five codes land under the nodes of s1's five-state ring, replacing the "???".
> {two}: ch1 s5's waveform, small (CLK YELLOW, output GREEN, high for two periods, low for three); its two high periods bracket GOLD. {pass}: one GOLD 1 crossing a, b, c lights each cell for one tick; then two GOLD 1s, one behind the other, light each cell for two ticks in a row.
> {cols}: the code column widens into the table's current-state block; its a, b and c columns box GREEN one at a time as they're read: a = 0 1 1 0 0, b = 0 0 1 1 0, c = 0 0 0 1 1 (p. 135's table; checked).
> {waves}: each column lifts into a GREEN waveform under one shared YELLOW CLK, two rounds long. {shift}: dashed verticals show b is a delayed by one period, and c is b delayed by one (checked).
> {any}: all three waveforms outline GREEN; p. 135's line "By inspection we can see that we can use any of the FF outputs as the wanted output".

[c2.slide.1] {cells} These funkier assignments often borrow the action of a shift register. In a shift register, every edge of the clock passes each flip-flop's value on to the next. {name} The first example is called the sliding assignment. We start with all three flip-flops at zero, drawn in the table's order, with flip-flop A on the right. {enter} On the first edge of the clock, a one enters flip-flop A. {follow} On the next edge, it slides along to flip-flop bee, and a second one enters behind it.

[c2.slide.2] {together} On the third edge, both ones slide along together. {drop} On the fourth, the first one drops off the far end. {empty} On the fifth, the second one drops off too, and every flip-flop is back at zero. {codes} So the five states get the codes zero zero zero, zero zero one, zero one one, one one zero, and one zero zero, and then round again. {pause}

[c2.slide.3] {two} Why send in two ones? {pause} The output must be one in two of the five states, and we'd like to take it straight from a flip-flop. {pass} A single one passing through would hold each flip-flop at one for just one state. Two of them, one right behind the other, hold each flip-flop at one for two states in a row.

[c2.slide.4] {cols} Check it on the columns. Flip-flop A reads zero, one, one, zero, zero. Flip-flop bee reads zero, zero, one, one, zero. And flip-flop see reads three zeros, then two ones. {waves} Each is high for two states and low for three, the waveform we want. {shift} In fact they're the same waveform, each one period behind the last. {any} The specification never says where the output's cycle should start, so any of the three can be the output. {pause}

## Scene 3 · Logic by K-map and by eye (ch2_s3_slidelogic)

> {table}: s2's code column becomes the current-state block of the table, left, in ch1's `mod_table()` styling (p. 135): headers "Current state" `c b a` | "Next state" `c' b' a'`, state bits GREEN. Rows: 000 → 001, 001 → 011, 011 → 110, 110 → 100, 100 → 000.
> {unused}: under it, p. 135's "Unused states, 010, 101, and 111." with the three codes DIM. {binary}: a small copy of ch1's binary table appears beside it with its 010 row lit (used there); that 010 flies onto the DIM 010 here, then the copy fades.
> {kmap}: right, ch1 s7's 2 × 4 K-map (L6 `kmap()` style): corner c over b a, columns 00 01 11 10 in Gray order, rows 0 and 1, the slide's bars (a over columns 01 and 11, b under 11 and 10, c beside row 1). The a′ column's entries fly into their cells (TransformFromCopy) and the three unused cells get X: row c = 0 reads 1 1 0 X, row c = 1 reads 0 X X 0 (0s DIM; the slide leaves them blank; checked).
> {pair}: a PINK loop round the two 1s in row 0, columns 00 and 01, labelled b̄·c̄. Below the map: D_a = b̄·c̄ (D_a BLUE). {xs}: the three X's flash once and stay unlooped: no group of four holds a 1 (checked; b̄·c̄ is the only one-term cover).
> {eye}: the map shrinks to a corner. In the table, the current a column boxes GREEN (0 1 1 0 0). {match}: the next-state b′ column boxes BLUE, the same 0 1 1 0 0; an "=" between them; D_b = a appears (p. 136, "By inspection we can see that:"). {dc}: current b and next c′ (both 0 0 1 1 0) the same way; D_c = b. {quote}: small card, the lecturer: "we like things where we don't have to do anything".
> {sr}: the three equations stack, D_a = b̄·c̄, D_b = a, D_c = b. Beside them a sketch in circuit order: cells a → b → c joined by arrows, and a small BLUE box "b̄·c̄" feeding a. {gate}: in the table, rows 000 and 001 (b = c = 0) glow; caption (ours): "a new 1 enters a only when b and c are both 0".

[c2.logic.1] {table} Here's the transition table for the sliding assignment. Each state's next state is simply the code that follows it in the sequence. {unused} Three patterns never occur: zero one zero, one zero one, and one one one. {binary} Notice that zero one zero is unused here, though the binary count used it. Which patterns are unused depends on the assignment.

[c2.logic.2] {kmap} Now plot a K-map for the input of flip-flop A, with the unused states as don't cares, just as in part one. The next value of flip-flop A is one in just two states, zero zero zero and zero zero one. {pair} They sit side by side, so they make a pair, and the input to flip-flop A is not bee and not see. {xs} The don't cares can't make a bigger group, so we leave them out.

[c2.logic.3] {eye} For the other two flip-flops, you don't even need a K-map. Look at the column for flip-flop A in the current state. It reads zero, one, one, zero, zero. {match} Now look at the column for flip-flop bee in the next state. It's exactly the same. So dee bee equals A, which is just a wire. {dc} In the same way, the current column for bee matches the next column for see, so dee see equals bee. {quote} As the lecturer puts it, we like things where we don't have to do anything.

[c2.logic.4] {sr} Put the three together. Flip-flop bee copies A, and flip-flop see copies bee, on every edge of the clock. That's a shift register, running from A to bee to see. {gate} The only logic is the and gate at its input, and you can read it in words. A new one enters flip-flop A only when bee and see are both zero.

## Scene 4 · The sliding circuit (ch2_s4_slidecircuit)

> {circuit}: the circuit as in the lecturer's simulation (slide_state_ass, frame at 00:20:20), from L6 ch6_s6_circuit.py's parts: three D flip-flops (`make_ff`) a, b, c left to right; one YELLOW CLK line from `clock_source()` labelled "1 Hz"; a two-input `and_gate` fed from the Q̄ outputs of b and c, its output into D_a (BLUE); a wire from Q_a to D_b and from Q_b to D_c. An LED (`led`) on each Q. "output" (GREEN) on Q_b.
> {order}: a small reminder card: s2's row of cells (c b a) mirrors into a b c over the flip-flops; caption "circuit: a on the left · table: a on the right".
> {gate}: the AND gate glows. {wires}: the two plain wires glow, Q_a → D_b, then Q_b → D_c.
> {run}: the flip-flops start at 0 0 0, LEDs dark. {tick}: at each edge the CLK line flashes YELLOW and s2's GOLD 1s step one flip-flop to the right, a → b → c, the LEDs following; whenever Q̄_b and Q̄_c are both 1, the AND's output wire carries a GOLD 1 into D_a. Run two full rounds (000, 001, 011, 110, 100, twice; read in table order).
> {out}: the "output" label on Q_b flashes GREEN. {wave}: below, the waveform grows edge by edge: CLK YELLOW and the output (Q_b) GREEN, high for two periods and low for three, twice round. The simulator plots the clock red and the output blue; we keep our colours.
> {score}: the scoreboard (s1) returns at the right and gains a row, "sliding | 3 | 1 | none", its 1 in GOLD beside binary's 3. {less}: in the circuit the two plain wires glow again. {further}: a YELLOW "?" over the AND gate.

[c2.circ.1] {circuit} Here's the sliding counter as a circuit, laid out the way the lecturer drew it in his simulator. {order} As in part one, the circuit puts flip-flop A on the left, so here the ones slide to the right. {gate} Just one gate is needed, an and gate. It takes the not-bee and not-see outputs, and feeds flip-flop A. {wires} Then the output of flip-flop A is wired straight into the input of flip-flop bee, and the output of bee into flip-flop see.

[c2.circ.2] {run} It starts with all three flip-flops at zero, which is the first state in our table. {tick} On every edge of the clock, the ones slide one place along. {out} The lecturer takes the output from flip-flop bee, though any of them would do. {wave} It's high for two periods of the clock, then low for three, again and again.

[c2.circ.3] {score} So the sliding assignment uses the same three flip-flops as the binary count, but one gate instead of three. {pause} {less} It needs less wiring too, because two of its three inputs are plain wires from a neighbour. {further} Can we go further, and get rid of that last gate? {pause}

## Scene 5 · A ring of five (ch2_s5_ring)

> {quote}: the lecturer's words as a small card: "an even more egregious use of flip-flops"; title "Shift Register Assignment" (p. 136).
> {ring}: hero, left of centre: five square flip-flop cells labelled a, b, c, d, e (GREEN) placed round a circle, arrows a → b → c → d → e. {close}: the arrow from e back to a draws last, YELLOW, closing the circle. p. 136's bullet, small, underneath: "the output from the final shift register in the chain is connected to the input of the first FF:" and "– Consequently the data continuously cycles through the register". {cycle}: a faint GOLD sweep runs once round the circle.
> {pair}: GOLD 1s appear in a and b, the rest DIM 0. {step}: at each edge both step one cell round the circle; five steps bring them home.
> {table}: right, p. 137's table builds one row per step, in table order: header `e d c b a` | `e' d' c' b' a'`; rows 00011 → 00110, 00110 → 01100, 01100 → 11000, 11000 → 10001, 10001 → 00011 (checked). Each current-state row is copied off the circle (TransformFromCopy) with its digits placed in e d c b a order.
> {wrap}: in the table, the pair of 1s walks left row by row; the 11000 → 10001 row highlights where it wraps from the e end to the a end.
> {count}: under the circle, "5 flip-flops" beside ch1 s4's "⌈log₂ 5⌉ = 3", and "+2" in GOLD.
> {phase}: the five current-state columns lift into five GREEN waveforms under one YELLOW CLK, each 1 1 0 0 0 starting at a different edge (b's column reads 1 1 0 0 0 from the first row; checked). s1's five-state ring, small in a corner, takes the five ring codes under its nodes.
> {any}: all five waveforms outline GREEN; p. 137's "By inspection we can see that we can use any of the FF outputs as the wanted output".

[c2.ring.1] {quote} Next comes the shift register assignment, what the lecturer calls an even more egregious use of flip-flops. {ring} Take a shift register, {close} and connect the output of its last flip-flop back to the input of its first. {cycle} Now whatever is inside just cycles round and round.

[c2.ring.2] {pair} Use five flip-flops, from flip-flop A to flip-flop ee, and put two ones side by side in the ring. They have to be neighbours, so that each output stays high for two states in a row. {step} On every edge of the clock, the pair moves one step round the ring. {table} In the table's order, with flip-flop A on the right, the first state is zero zero zero one one. The next is zero zero one one zero. {wrap} The pair moves one place left each time, and wraps round from the left end back to the right. After five steps, it's back where it started.

[c2.ring.3] {count} That's five flip-flops for five states, two more than the minimum of three. {phase} And just as before, every column reads one, one, zero, zero, zero, each starting at a different point in the cycle. {any} So any of the five flip-flops can be the output.

## Scene 6 · No logic at all (ch2_s6_nologic)

> {logic}: s5's table moves left; s5's circle sits to its right. A BLUE "D = ?" over the empty space between them.
> {da}: the next-state a′ column boxes BLUE and the current e column boxes GREEN, both 0 0 0 1 1; "D_a = e" appears (p. 137's list; checked). {db}: next b′ and current a, both 1 0 0 0 1; "D_b = a". {rest}: the other three pairs light in quick turn: c′ = b (1 1 0 0 0), d′ = c (0 1 1 0 0), e′ = d (0 0 1 1 0); "D_c = b", "D_d = c", "D_e = d" (D's BLUE, letters GREEN).
> {wiring}: on the circle, each arrow flashes as its equation lights, e → a last. Caption: "each input is the output of the flip-flop before it".
> {unroll}: the circle unrolls into the circuit of the lecturer's simulation (shift_reg_state_ass, frame at 00:28:45): five D flip-flops (`make_ff`) a, b, c, d, e left to right on one YELLOW CLK line; Q_a → D_b, Q_b → D_c, Q_c → D_d, Q_d → D_e, and one long wire from Q_e back along the top into D_a; "output" GREEN on Q_b; no LEDs lit, no gates. ch3 s1 opens on this exact circuit.
> {nogates}: "no gates" in GOLD over the gap where ch1's logic used to sit.
> {unused}: a 4 × 8 grid of all 32 five-bit codes; the five used ones GREEN, the other 27 DIM. {lots}: p. 137's "Unused states. Lots!" and a GOLD "27".
> {fine}: the grid's 27 DIM codes each take an X (don't care). {remember}: they pulse once, faintly RED, and the grid shrinks away.

[c2.wire.1] {logic} So what next-state logic does the ring need? {pause} Remember, with dee flip-flops each input is just the next state. {da} The next-state column for flip-flop A reads zero, zero, zero, then one, one, exactly the current column for flip-flop ee. So flip-flop A takes its input from ee, the last flip-flop. {db} The next column for flip-flop bee matches the current column for flip-flop A, so dee bee equals A. {rest} The rest follow the same way. Flip-flop see takes its input from bee, flip-flop dee from see, and flip-flop ee from dee.

[c2.wire.2] {wiring} That's no surprise, because it's exactly how the ring is wired. Each flip-flop's input is the output of the flip-flop before it. {unroll} Laid out as a circuit, it's five flip-flops in a row, sharing one clock signal, with one long wire from the last back to the first. {nogates} There are no gates at all, only wires. {pause}

[c2.wire.3] {unused} Five flip-flops can hold thirty-two patterns, and we use only five. {lots} In the slide's words, unused states, lots! Twenty-seven of them. {fine} In the design they're just don't cares, and this time we never even drew a K-map. {remember} Keep those twenty-seven in mind. They come back in part three.

## Scene 7 · Flip-flops or wires? (ch2_s7_tradeoff)

> {slide}: s6's five-flip-flop circuit, small at the top, under p. 137's last line verbatim: "See needs 2 more FFs, but no logic and simple wiring", with "2 more FFs" GOLD.
> {fun}: a small card, the lecturer at 00:30:01: "just a couple of bits of fun". {power}: s4's and s6's circuits side by side, small, their D inputs lit BLUE: one gate, then none.
> {chip}: two chip outlines side by side (rounded rectangles labelled "chip"): left, three flip-flop blocks plus three gate blocks and a tangle of routed wires between them (binary); right, five flip-flop blocks joined by short straight wires (the ring). {area}: the flip-flop blocks pulse, small. {wiring}: the left chip's wire tangle shades GOLD, the area it costs. {more}: the right chip's spare area glows GREEN.
> {part1}: p. 132's two sub-bullets, as ch1 s4 showed them, small: "FF implementation may take less chip area than you may think given their gate level representation" and "Wiring complexity can be as big an issue as gate complexity".
> {score}: the scoreboard (s1, s4) moves to centre and gains its third row, "ring | 5 | 0 | none". {binary} / {sliding} / {ring}: the rows light in turn. GOLD arrows beside the columns: flip-flops 3, 3, 5 going up; gates 3, 1, 0 going down. {noout}: the output-logic column "none, none, none" lights GREEN.
> {depends}: under the scoreboard, p. 132's "Depends what we are trying to optimise" (ch1 s4).

[c2.trade.1] {slide} The slide sums up the ring in one line. Two more flip-flops, but no logic and simple wiring. {fun} The lecturer calls these last two designs just a couple of bits of fun. {power} But they show that you can build a working machine with no combinational logic at all, from flip-flops alone.

[c2.trade.2] {chip} And sometimes that's the cheaper design. {area} On a modern chip, each flip-flop takes up only a little room. {wiring} Logic gates need wiring between them, and wiring takes up space. {more} So using more flip-flops to avoid the logic can be the better choice. {part1} Those were the slide's two points in part one, about area and wiring.

[c2.trade.3] {score} Here's the scoreboard so far. {binary} The binary count used three flip-flops and three gates. {sliding} Sliding used three flip-flops and one gate. {ring} The ring uses five flip-flops and no gates at all. {noout} None of them needs output logic. {depends} So which is best depends on what you're trying to save.

## Scene 8 · Recap and next (ch2_s8_recap)

> Recap: one small panel per sentence, each the same object, colours and styling as the scene that taught it, with its short line beneath; the panels gather on a 3 × 2 grid.
> {recap}: a small "Recap" heading at the top (the series' recap heading, as L8's ch2_s6_recap.py) over six faint empty slot frames on the 3 × 2 grid; each r-mark fills its slot, left to right, top row first.
> {r1}: s2's three cells (c b a) with two GOLD 1s sliding through: "two 1s slide through three flip-flops".
> {r2}: s2's three GREEN waveforms, one period apart, all outlined: "same waveform, any phase".
> {r3}: s3's table with the current a and next b′ columns boxed and "D_b = a": "matching columns are wires".
> {r4}: s4's circuit with its single AND gate lit: "one AND gate".
> {r5}: s5's circle of five with the GOLD pair stepping round: "a ring of five: no gates".
> {r6}: s7's scoreboard with its GOLD arrows: "more flip-flops, less logic".
> {next}: the panels clear; s6's five-flip-flop circuit returns, the CLK line flashing at each edge, while below it the output trace (GREEN) runs flat along 0, and a RED "?" appears over it. This is ch3 s1's opening shot. {why}: the "?" pulses.
> End card after the last word, about 8 s, the music carrying it.

[c2.recap.1] {recap} To recap. {r1} In the sliding assignment, two ones slide through three flip-flops. {r2} Each flip-flop then gives the same waveform in a different phase, so any of them can be the output. {r3} Where a current column matches a next-state column, that input is just a wire. {r4} So the sliding counter needs just one and gate.

[c2.recap.2] {r5} Then join the register into a ring of five, and each flip-flop simply copies the one before it, with no gates at all. {r6} You spend flip-flops to save logic and wiring, and on a modern chip that can be the better deal. {pause} {next} Next time, we switch the ring on, and nothing happens. {why} Why? {pause=1.5}
