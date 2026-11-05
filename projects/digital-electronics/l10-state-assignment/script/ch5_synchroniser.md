# Chapter 5 · Hunt, Sight and Sync

Digital Electronics · Lecture 10 (State Assignment), part 5 of 6. Source: Digital Electronics slides (combined_26.pdf), pp. 139 (Tripos Example)–141 (FF 0's K-map), with p. 123 (Lecture 9's Moore example, the same machine); lecture recording 00:38:44–00:51:53 (00:38:56–00:39:36 skipped).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Spoken names: "ee" and "ar" are the inputs e and r; "ess" is the output s; "ess one" and "ess
zero" are the flip-flop outputs s1 and s0 (here s1 is the high bit, 1 only in Sync); "ess one
prime" is s1′, the next state; "dee one" and "dee zero" are D1 and D0; "flip-flop one" is FF 1.
Boolean terms are read by meaning: "ess one and not ee" is s1·ē. "An ex" is the X of the table and
the K-maps. Colours as PLAN.md sets them: CLK YELLOW; e and r BLUE; state bits s1 s0 and the
output s GREEN; D1 and D0 BLUE; unused state 11 DIM; K-map loops PINK, PURPLE, TEAL; trouble RED.
No code on screen. Every table, K-map, grouping, equation and gate count below was checked by
exhaustive enumeration in Python 3.11.9 (standard library, itertools.product over states and
inputs); the diagram, table and maps were re-read from the rendered slides, pp. 139–141.

---

## Scene 1 · Hook (ch5_s1_hook)

> {title}: title card: "State Assignment", under it "Digital Electronics · Lecture 10", then the part line "Part 5 · Hunt, Sight and Sync".
> {last}: ch4's one-hot traffic light, small, at the left: its ring of four flip-flops with the GOLD 1 stepping round, the three lamps lighting in their own colours. {clockonly}: ch1's five-state ring of the divide-by-5 (binary codes) appears at the right. Each machine gets a single YELLOW CLK wire going in and nothing else, with a DIM tag "inputs: none" under each.
> {stream}: clear to a long tape of white bits sliding right into a box "receiver" at the right edge, no gaps between them. {pattern}: one fixed 8-bit pattern, YELLOW-boxed, comes past again and again at an equal spacing. {ask}: YELLOW "?" marks hover over the stream: where does each frame start?
> {tripos}: a small card "Tripos question (a Cambridge exam question)". {lecture9}: p. 123's three state circles in the slide's layout, A top left, B top right, C below between them; letters A, B, C only, no arcs, no codes. {names}: the letters transform into YELLOW names, A → Sync, B → Hunt, C → Sight (the same machine: p. 123's A [10], B [00], C [01] are p. 139's Sync, Hunt, Sight). This layout is the one s3 builds on.
> {plan}: two chips under the circles, "Part 5: two flip-flops" (lit) and "Part 6: one-hot" (DIM).

[c5.hook.1] {title} This is part five of our lecture on state assignment. {last} Last time, you met one-hot, with a flip-flop for every state. {clockonly} But every machine so far has run on the clock alone. Nothing from outside could change its path. {pause}

[c5.hook.2] {stream} Now picture a receiver at the end of a serial link. Bits pour in, one after another, with no gaps between them. {pattern} Every so often, a known pattern comes past. {ask} How can the receiver lock on to that pattern, and stay locked on? {pause}

[c5.hook.3] {tripos} The answer is a state machine with two inputs, from an old Tripos question, which is a Cambridge exam question. {lecture9} You saw its diagram in part one. Back then, its three states were just letters, state A, state bee and state see. {names} Now they're called Hunt, Sight and Sync, and the machine has a job. {plan} We'll build it with two flip-flops in this part, and one-hot in the next.

## Scene 2 · Frame synchronisation (ch5_s2_frames)

> {link}: L8 ch2 s3's serial data link (p. 103), reused: a left box "Parallel in, serial out", one wire "Serial Data", a right box "Serial in, parallel out", one YELLOW CLK line under both. {wire}: white bits leave the left box one at a time and run along the wire into the right box. {plain}: zoom on the wire: the bits become s1's long tape, evenly spaced and unmarked, with a YELLOW "?" over it.
> {insert}: s1's YELLOW-boxed 8-bit sequence now sits in the tape at equal spacing, with a GOLD tag "8 or 16 bits". {frames}: braces between consecutive copies, each labelled "frame". {sync}: the receiver box gets a GREEN tick as each copy arrives; caption "frame synchronisation".
> {notL8}: a small DIM inset of L8 ch4 s5's two-flip-flop synchroniser, tagged "Lecture 8: metastability", with a "≠" between it and the caption; the inset fades.
> {signals}: under the tape, a box "state machine" fed by two BLUE wires from the receiver, `r` and `e`; its output `s` (GREEN) leaves on the right. {r}: a BLUE trace for r, high for one bit as the last bit of each copy enters the receiver. {e}: a BLUE trace for e, high in a short window at each due time, lined up with r's pulses. {s}: the GREEN `s` wire glows.
> {why}: hold the picture. {chance}: a copy of the pattern turns up inside the data between two due times; r pulses there while e stays low. That copy's box turns RED, tag "by chance". {false}: a RED ghost brace starts from it, "wrong frame". {guard}: the RED copy fades; the next real copy arrives with e and r high together, GREEN tick, caption "seen, then seen again on time".

[c5.frames.1] {link} Remember the serial data link from Lectures seven and eight. {wire} A transmitter sends bits down a single wire, one after another, and a receiver collects them at the other end. {plain} But the stream carries no markings. On its own, the receiver has no way to tell where one block of data ends and the next begins.

[c5.frames.2] {insert} So at regular intervals, the transmitter inserts a known sequence of bits, say eight or sixteen of them. {frames} The data between two copies is called a frame. {sync} Once the receiver finds the sequence, it knows where each frame starts, and it can stay in step with the transmitter. That's frame synchronisation. {notL8} It's a different job from Lecture eight's synchroniser, the chain of flip-flops that tamed meta-stability. Same word, different machine.

[c5.frames.3] {signals} Two signals in the receiver are the inputs to our machine. {r} Signal ar goes to one when the receiver thinks it has just received the special sequence. {e} Signal ee is one when the receiver is expecting the sequence right now. It can work that out, because the spacing is known. {s} And the machine's output, called ess, will say whether we're in sync.

[c5.frames.4] {why} But why do we need input ee at all? {pause} {chance} Because the special sequence can also turn up by chance, in the middle of the data. {false} If the receiver believed every sighting, it would lock on to the wrong place. {guard} So a single sighting proves nothing. The machine waits for the next copy, and checks that it arrives exactly when it's due.

## Scene 3 · Reading the state diagram (ch5_s3_diagram)

> p. 139's state diagram, large and centred, built arc by arc in s1's layout: Sync top left, Hunt top right, Sight below between them. White circles with YELLOW names, no codes yet (s4 adds them). Arcs as on the slide, labels BLUE with real overbars and a centred dot: `r̄`, `r`, `ē`, `e·r`, `e·r̄`. Arcs re-read from the rendered p. 139 (the digest's 00:38:44 version is wrong; PLAN.md Decisions).
> {three}: the three empty circles. {hunt}: Hunt lights (YELLOW outline). {stay}: Hunt's self-loop `r̄` (upper right). {go}: the arc Hunt → Sight `r` (right side). {either}: a small DIM tag "e: either value" by that arc.
> {sight}: Sight lights. {wait}: Sight's self-loop `ē` (below it). {confirm}: the arc Sight → Sync `e·r` (lower left). {ask}: a YELLOW "?" where the inner arc will go; {fluke}: it becomes the inner arc Sight → Hunt `e·r̄`.
> {sync}: Sync lights. {between}: Sync's upper self-loop `ē`. {kept}: Sync's lower self-loop `e·r`. {lost}: the top arc Sync → Hunt `e·r̄`.
> {check}: hold the finished diagram. {grids}: beside each state, a tiny 2 × 2 grid of the four input combinations (rows e = 0, 1; columns r = 0, 1; labels BLUE). {hunt2}: Hunt's arcs flash YELLOW in turn; `r̄` fills cells 00 and 10, `r` fills 01 and 11. {others}: the same for Sight and Sync: `ē` fills 00 and 01, `e·r` fills 11, `e·r̄` fills 10. Every cell fills exactly once; three GREEN ticks. Ours, checked (exhaustive, Python 3.11.9): from each state the labels cover every (e, r) exactly once.
> {why2}: two RED ghost grids flash beside the diagram, one with an empty cell ("nowhere to go"), one with a cell filled twice ("two places to go"), then fade.
> {output}: a GREEN tag `s = 1` beside Sync, DIM `s = 0` beside Hunt and Sight (p. 139: "An output, s should be true if in Sync state"). {moore}: caption "Moore: output from the state alone". {design}: the grids clear; the diagram stays for s4.

[c5.diagram.1] {three} Here's the machine's state diagram, with its three states. {hunt} In Hunt, it's looking for the sequence. {stay} While ar is zero, there's nothing yet, so it stays in Hunt. {go} When ar is one, it has spotted the sequence, and it moves to Sight. {either} Input ee plays no part here.

[c5.diagram.2] {sight} In Sight, the sequence has been seen once. {wait} While ee is zero, the next copy is still to come, so it stays in Sight. {confirm} When ee and ar are both one, the sequence came exactly when expected, so the machine moves to Sync. {ask} And when ee is one but ar is zero? {pause} {fluke} The sequence was due, but it was missing. The first sighting was a fluke, so it's back to Hunt.

[c5.diagram.3] {sync} In Sync, the receiver has locked on to the sequence. {between} While ee is zero, nothing is expected, so it stays in the Sync state. {kept} When ee and ar are both one, the sequence arrived on time, so it stays. {lost} When ee is one and ar is zero, an expected copy is missing. Sync is lost, and the machine goes back to Hunt.

[c5.diagram.4] {check} Here's a check you can do on any diagram like this. {grids} From each state, the arcs leaving it should cover every combination of ee and ar exactly once. {hunt2} From Hunt, not ar takes two combinations, and ar takes the other two. {others} From Sight and from Sync, not ee takes two, and the other two arcs take one each. {why2} Miss a combination, and the machine has nowhere to go. Cover one twice, and it has two places to go.

[c5.diagram.5] {output} Finally, the output, ess, should be one only in Sync. {moore} It depends on the state alone, so this is a Moore machine, like every machine in this lecture. {design} The diagram pins down what the machine must do. Now we can design it.

## Scene 4 · Two flip-flops, and the output (ch5_s4_twoffs)

> s3's diagram moves left and shrinks. {count}: at the right, ch1 s4's doubling ladder, small: "1 flip-flop → 2 patterns", "2 flip-flops → 4 patterns". {ladder}: GOLD `⌈log₂ 3⌉ = 2`, and the ladder's second rung lights. {labels}: two D flip-flop boxes (L6's `make_ff`), outputs `s1` and `s0` in GREEN, with the slide's tag "FF labels [s1 s0]".
> {assign}: a GREEN code drops under each name in the slide's brackets: {hunt} Hunt `[00]`, {sight} Sight `[01]`, {sync} Sync `[10]`. {unused}: a fourth DIM circle `[11]` beside the diagram, tagged "unused".
> {output}: a small table, columns state | `s1 s0` | `s`: Hunt `0 0` `0`; Sight `0 1` `0`; Sync `1 0` `1`; and a DIM row `1 1` `–`. {column}: the `s1` column boxed YELLOW next to the `s` column: they match row for row. {equal}: `s = s1` (GREEN), p. 140's "From inspection, s = s1".
> {why}: Sync's row pulses, then the DIM `1 1` row flashes once, tag "never occurs".
> {nologic}: the `s` wire drawn straight from the s1 flip-flop's Q output, GREEN, tag "no output logic". Checked (Python 3.11.9): ⌈log₂ 3⌉ = 2, and s = s1 in all three used states.

[c5.codes.1] {count} How many flip-flops do three states need? {pause} {ladder} At least log base two of three, rounded up, which is two, as part one's ladder showed. {labels} We'll call their outputs ess one and ess zero.

[c5.codes.2] {assign} The exam question uses the sequential assignment, counting in binary, as in part one. {hunt} Hunt is zero zero. {sight} Sight is zero one. {sync} And Sync is one zero. {unused} That leaves one one as the unused state.

[c5.codes.3] {output} Now, what logic makes the output? It must be one in Sync, and zero in Hunt and Sight. {column} Look at ess one. It's one in the Sync state, and zero in Hunt and Sight. {equal} That's exactly what we need. So the output is just flip-flop one's output. {why} The fourth pattern, one one, would also give a one, but it never occurs. {nologic} So there's no output logic at all, just a wire from flip-flop one.

## Scene 5 · The table, with don't-care inputs (ch5_s5_table)

> s4's diagram, with its codes, shrinks to the left and stays; each arc lights YELLOW as its row is written. At the right, p. 140's table in L6's `mod_table()` style: header "Current state | Input | Next state", sub-headers `s1 s0` (GREEN) | `e r` (BLUE) | `s1′ s0′` (GREEN), the slide's double rule before the next state, and rules between Hunt's two rows, Sight's three, Sync's three and the unused row. {table}: the empty frame. {cols}: the three sub-headers light in turn. {build}: Hunt's circle pulses.
> Rows, verbatim from p. 140: `0 0 | X 0 | 0 0`, `0 0 | X 1 | 0 1`, `0 1 | 0 X | 0 1`, `0 1 | 1 0 | 0 0`, `0 1 | 1 1 | 1 0`, `1 0 | 0 X | 1 0`, `1 0 | 1 0 | 0 0`, `1 0 | 1 1 | 1 0`, `1 1 | X X | X X`. Checked (exhaustive, Python 3.11.9): the eight used rows expand to the 12 used (state, e, r) combinations, each once, and each matches the diagram.
> {hunt}: Hunt glows. {r0}: row 1, with the self-loop `r̄` lit. {r1}: row 2, with the arc `r`. {ex}: both X's under e get a YELLOW box.
> {sight}: Sight glows. {e0}: row 3, its X under r boxed YELLOW. {e1r0}: row 4. {e1r1}: row 5. {sync}: Sync glows; rows 6, 7 and 8 appear, one per clause.
> {unused}: the DIM row `1 1 | X X | X X`, and s4's DIM circle `[11]` flashes. {never}: DIM caption "next-state logic never sees 11". {xx}: the next-state `X X` pulses.
> {kinds}: two tags appear side by side, "X under the inputs" and "X in the next state". {inputx}: Hunt's input X boxed YELLOW, tag "either value, same next state". {expand}: row 1 splits into two ghost rows, `0 0 | 0 0 | 0 0` and `0 0 | 1 0 | 0 0`, then folds back. {nextx}: the unused row's next-state `X X` boxed DIM, tag "never happens: 0 or 1, whichever is simpler".

[c5.table.1] {table} Next comes the state transition table. {cols} The first two columns hold the current state, ess one and ess zero. In the middle, the inputs, ee and ar. On the right, the next state, ess one prime and ess zero prime. {build} We fill it in one state at a time, straight from the diagram.

[c5.table.2] {hunt} Start with Hunt, zero zero. {r0} If ar is zero, it stays at zero zero. {r1} If ar is one, it goes to Sight, zero one. {ex} In both rows, input ee makes no difference. So the ee column gets an ex, meaning don't care.

[c5.table.3] {sight} Next, Sight, zero one. {e0} If ee is zero, it stays at zero one, whatever ar is, so ar gets the ex. {e1r0} If ee is one and ar is zero, it falls back to Hunt, zero zero. {e1r1} And if both are one, it moves to Sync, one zero. {sync} Sync, one zero, follows the same pattern. With ee zero, it stays at one zero. With ee one, it goes to zero zero if ar is zero, and stays at one zero if ar is one.

[c5.table.4] {unused} Last, the unused state, one one. {never} As long as it starts in a used state, the machine never gets there, so the next-state logic never sees it. {xx} Every entry in that row is an ex.

[c5.table.5] {kinds} Notice that this table uses ex in two different ways. {inputx} An ex under the inputs is shorthand. It means both values give the same next state. {expand} So Hunt's first row really stands for two rows, ee zero and ee one, and later it will fill two cells of a K-map. {nextx} An ex in the next state is a true don't care. That row never happens, so the logic may give a zero or a one there, whichever makes it simpler.

## Scene 6 · A four-variable K-map for D1 (ch5_s6_d1)

> {dee}: a small reminder from ch1 s2, `D = Q′`. {d1}: s5's table shrinks to the left; its `s1′` column is boxed BLUE, labelled `D1 = s1′` (D1 BLUE). {four}: four chips, `s1` `s0` (GREEN) and `e` `r` (BLUE).
> {grid}: a new 4 × 4 K-map in L6's `kmap()` style, as on p. 140, titled "For FF 1:": corner label `e r` over `s1 s0` with the diagonal; column headings `00 01 11 10` (BLUE), row headings `00 01 11 10` (GREEN); the slide's bars, `e` over columns 11 and 10, `r` under columns 01 and 11, `s0` right of rows 01 and 11, `s1` left of rows 11 and 10. {gray}: neighbouring headings flash in pairs, the one changed bit YELLOW. {wrap}: the top and bottom edges flash as a pair, then the left and right edges (or a brief cylinder curl, as in L6). {xrow}: row 11 fills with X (DIM, as in ch1's maps) and s4's DIM `[11]` circle flashes.
> {ones}: each 1 is written as its table row lights. {first}: row 01, column 11 (Sight, e r = 11). {sync}: Sync's `0 X` row lights, and cells 1000 and 1001 fill together, the row's X boxed YELLOW (one row, two cells). {last}: row 10, column 11. Other cells stay empty, as on the slide. {try}: hold the bare map, with a small "your turn" tag.
> Loops in L6's `loop_round()` style, each with its term in its own colour, placed like the slide's labels. {pink}: PINK `s1·ē` around rows 11–10 × columns 00–01. {purple}: PURPLE `s1·r` around rows 11–10 × columns 01–11, overlapping PINK in column 01 (inset so both outlines show). {teal}: TEAL `s0·e·r` around rows 01–11 × column 11.
> {essential}: the cell each loop alone covers pulses in its loop's colour: 1000 PINK, 1011 PURPLE, 0111 TEAL. {result}: the equation, p. 140 verbatim, terms coloured to match: `D1 = s1·ē + s1·r + s0·e·r`. {meaning}: under each term, a short caption in its colour: {m1} "in Sync, nothing expected", {m2} "in Sync, sequence there", {m3} "from Sight, on time".
> Checked (exhaustive, Python 3.11.9): the map reads row 00 `0 0 0 0`, row 01 `0 0 1 0`, row 11 `X X X X`, row 10 `1 1 1 0` (columns 00 01 11 10); its only prime implicants are s1·ē, s1·r and s0·e·r, all essential; D1 matches all 12 used rows.

[c5.kmap.1] {dee} With dee flip-flops, each dee input is just the next state. {d1} So the input to flip-flop one, dee one, is the ess one prime column. {four} It depends on four variables, ess one, ess zero, ee and ar. So we need a four-variable K-map.

[c5.kmap.2] {grid} The rows are ess one and ess zero, and the columns are ee and ar. {gray} Both run in Gray code order, zero zero, zero one, one one, one zero, so neighbouring cells differ in one variable. {wrap} The map also wraps around, top to bottom and side to side. {xrow} Notice the row for one one, between zero one and one zero. It's the unused state, so the whole row is don't cares.

[c5.kmap.3] {ones} Now put the ones of ess one prime on the map. {first} The first is Sight with ee and ar both one, in row zero one, column one one. {sync} Next, Sync with ee zero. That's one table row, but ar is an ex, so it fills two cells. {last} The last is Sync with ee and ar both one. {try} Four ones, and a row of don't cares to help. Try grouping them yourself. {pause=1.5}

[c5.kmap.4] {pink} Here's the slide's answer. Sync's two cells with ee zero join the two don't cares above them, a block of four. That's the term ess one and not ee. {purple} The middle two cells of Sync's row join the don't cares above them too. That group gives ess one and ar. {teal} The lone one in Sight's row pairs with the don't care right below it. That pair makes the term S zero and ee and ar.

[c5.kmap.5] {essential} Each group covers a one that no other group reaches, so all three are essential. {result} So dee one is ess one and not ee, or ess one and ar, or ess zero and ee and ar. {meaning} In words, {m1} stay in Sync while nothing is expected, {m2} or whenever the sequence is there. {m3} And enter Sync from Sight when the sequence comes on time.

## Scene 7 · D0, and the finished design (ch5_s7_d0)

> s6's map and its equation slide up-left and shrink (kept, DIM). {d0}: s5's `s0′` column boxed BLUE, `D0 = s0′`; a fresh 4 × 4 map in the same style, titled "For FF 0:". {hunt}: Hunt's `X 1` row lights and fills 0001 and 0011 together, its X boxed YELLOW. {sight}: Sight's `0 X` row fills 0100 and 0101. {xrow}: row 11 fills with DIM X.
> {pink}: PINK loop `s0·ē` around rows 01–11 × columns 00–01. {purple}: PURPLE loop `s̄1·s̄0·r` around row 00 × columns 01–11; then three ghost outlines try to double it (down into row 01, wrapping up to row 10, across the whole of row 00), each catching a 0 cell that flashes RED, and fade. {result}: p. 141's equation verbatim, coloured: `D0 = s0·ē + s̄1·s̄0·r`.
> {other}: a dashed grey loop around 0001 and 0101 (column 01, rows 00–01), tag `s̄1·ē·r`. {valid}: tag "also a group". {spare}: 0011 pulses: only PURPLE covers it; then the dashed loop's two cells pulse, already covered by PURPLE and PINK, and the dashed loop fades. {min}: tag "two essential groups". Ours, checked (exhaustive, Python 3.11.9): the map reads row 00 `0 1 1 0`, row 01 `1 1 0 0`, row 11 `X X X X`, row 10 `0 0 0 0`; its prime implicants are s̄1·s̄0·r, s̄1·ē·r and s0·ē, of which only s̄1·s̄0·r and s0·ē are essential, and together they cover every 1; D0 matches all 12 used rows.
> {design}: clear to the circuit, drawn left to right with L6's `make_ff`, `and_gate`, `and3_gate`, `or_gate`. {ffs}: two D flip-flops, `s1` and `s0` (GREEN outputs), on one YELLOW CLK line; BLUE inputs `e` and `r` enter from the left, `e` through one inverter giving `ē`. {logic1}: D1's block: AND(`s1`, `ē`), AND(`s1`, `r`), 3-input AND(`s0`, `e`, `r`), into a 3-input OR, into D1. {logic0}: D0's block: AND(`s0`, `ē`), 3-input AND(`s̄1`, `s̄0`, `r`), into a 2-input OR, into D0. Feedback by short labelled wire stubs (`s1`, `s0`, `s̄1`, `s̄0`) rather than long wires, to keep it readable. {out}: the output `s` (GREEN) wired straight from `s1`.
> {count}: GOLD counts under the blocks, "5 AND", "2 OR", "= 7 gates", and a DIM "+ 1 inverter (ē)". {free}: the Q̄ outputs of both flip-flops glow, tag "free". {score}: the scoreboard slides in (ch1 s8's table, header "assignment | flip-flops | next-state gates | output logic", with the rows from ch1, ch2 and ch4 s5), and under a new sub-heading "synchroniser" a new row writes itself in: "sequential | 2 | 7 | none", numbers GOLD (ch6 s7 adds the one-hot row under it). Checked: 5 AND + 2 OR = 7, inverters not counted, as in PLAN.md's count. {plain}: the codes `[00]` `[01]` `[10]` appear small beside the row, tag "just counting".

[c5.finish.1] {d0} Now the same for dee zero, the ess zero prime column. {hunt} In Hunt, when ar is one, the table has a single row, but ee is an ex, so it fills two cells, in columns zero one and one one. {sight} In Sight, when ee is zero, two more cells fill, in columns zero zero and zero one. {xrow} And the unused row is don't cares again. {pause}

[c5.finish.2] {pink} Sight's pair joins the two don't cares below it, a block of four. That's ess zero and not ee. {purple} Hunt's pair is stuck at two, because every way of doubling it takes in a zero. So it stays a pair, and its term is not ess one and not ess zero and ar. {result} So dee zero is ess zero and not ee, or not ess one and not ess zero and ar.

[c5.finish.3] {other} You might spot a different pair, Hunt's one in column zero one, with the Sight cell below it. {valid} That's a valid group too. {spare} But Hunt's one in column one one still needs the slide's pair, and then the other group adds nothing. {min} So the slide's answer is the smallest.

[c5.finish.4] {design} That's the whole design. {ffs} Two dee flip-flops share one clock signal. {logic1} The input dee one comes from three and gates, joined by an or gate at the end. {logic0} The input dee zero comes from two more, joined by a second or gate. {out} And the output, ess, is wired straight from ess one.

[c5.finish.5] {count} Counting gates, that's five and gates and two or gates, seven in all, plus an inverter to make not ee. {free} Not ess one and not ess zero come free, from the flip-flops' inverted outputs. {score} On the scoreboard, the synchroniser with sequential assignment takes two flip-flops, seven gates, and no output logic. {plain} And that's with the plainest choice of codes, just counting the states, zero, one, two.

## Scene 8 · Recap and next (ch5_s8_recap)

> {recap}: the screen clears to five empty slots, which fill one per sentence, each a small copy of its scene's visual (same objects, colours and styling) with the sentence's short line under it.
> {r1}: s2's tape with the YELLOW-boxed sequence at equal spacing and the BLUE `r` and `e` traces; "known sequence, known spacing".
> {r2}: s3's diagram with all eight arcs; the arcs Hunt → Sight → Sync light in turn; "seen once, then on time".
> {r3}: s4's circles with GREEN codes `[00]` `[01]` `[10]`, the DIM `[11]`, and `s = s1`; "two flip-flops, s = s1".
> {r4}: s5's table with the input X's boxed YELLOW and the unused row's `X X` boxed DIM; "shorthand X, don't-care X".
> {r5}: s6's and s7's maps side by side with their PINK, PURPLE and TEAL loops, the equations under them, and the scoreboard row "2 | 7 | none"; "D1, D0: seven gates".
> {next}: the tiles dim; s3's diagram returns to the centre, its codes fade, and three flip-flop boxes appear, each labelled with a state's name, Hunt, Sight, Sync. {more}: GOLD "3 flip-flops". {easy}: a small DIM K-map with a "no K-maps" tag, while the arcs into Sync glow. Then the end card, held ~8 s after the last word while the music carries it.

[c5.recap.1] {recap} Time for a recap. {r1} To find frames in a serial stream, the receiver looks for a known sequence, repeated at a known spacing. {r2} The state diagram hunts for it, sights it once, and moves to Sync only when it comes again on time. {r3} Three states need two flip-flops, and with Sync at one zero, the output is just ess one. {r4} In the table, an ex under the inputs is shorthand for both values, and an ex in the next state is a true don't care. {r5} Two four-variable K-maps, helped by the unused row, give dee one and dee zero, with seven gates in all. {pause}

[c5.recap.2] {next} Next time, the same machine, one-hot. {more} It costs a third flip-flop. {easy} But you'll write its logic straight from the table, and even straight from the diagram, with no K-maps at all. {pause}
