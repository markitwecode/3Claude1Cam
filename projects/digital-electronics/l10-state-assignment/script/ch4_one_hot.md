# Chapter 4 · One-hot

Digital Electronics · Lecture 10 (State Assignment), part 4 of 6. Source: Digital Electronics slides (combined_26.pdf), p. 137 (One Hot State Encoding) to p. 139 (the one-hot circuit), with pp. 126–127 (Lecture 9's traffic-light logic) as a refresher and Lecture 8's timing constraints (pp. 105–106) as a callback; lecture recording 00:30:40–00:38:44.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Spoken names: no single letters are spoken in this chapter. The one-hot flip-flops r, ra, g, a are "the red flip-flop", "the red-and-amber flip-flop", "the green flip-flop", "the amber flip-flop" (PLAN.md: by colour); the lamps R, A, G are "the red lamp", "the amber lamp", "the green lamp". Lecture 9's flip-flops R, A, G (one per lamp, s5 and s7 only) are "the red lamp's flip-flop" and so on. "Dee inputs" are the D inputs. On screen L8's symbols T_c, f_c, t_pc, t_pd, t_su, t_hold, spoken "the clock period", "the clock frequency", "the clock-to-output delay" (COURSE.md: not "clock-to-cue"), "the logic's delay", "the set-up time", "the hold time". No code on screen. Every table, equation, loop, gate count and number was checked in Python 3.11.9 (standard library, exhaustive over all 16 four-bit patterns and all 8 three-bit ones). Colours (PLAN.md): CLK YELLOW; state bits and flip-flop outputs GREEN; D inputs BLUE; the hot 1 GOLD; unused states DIM; lamps in their own colours (red, amber, green) and dark when off, so trouble in this chapter shows as dark or wrong lamps, never RED paint; the asynchronous set pin and its bubble RED; numbers and costs GOLD; t_pc PINK, t_pd PURPLE, t_su and t_hold GOLD.

---

## Scene 1 · Hook (ch4_s1_hook)

> Title card on {title}: "State Assignment", "Digital Electronics · Lecture 10", "Part 4 · One-hot"; it clears on {last}.
> {last}: ch3's closing picture, small and centred: the ring of five (ch2 s5's cells e d c b a in a loop) after its rescue, two adjacent GOLD 1s circulating, ch3 s6's RED set pins on d and e back at 1. Tag "Part 3: start in a used state".
> {fun}: the two flip-flops beyond the three that five states need glow GOLD for a moment, tag "+2, 'a bit of fun'". {real}: the ring slides away; a line "one-hot: used a lot" appears.
> {eight}: clear. Two machines side by side for the same eight states, with a shared state number above them (0 to 7, GOLD). Right: three flip-flop cells (L8 `build_chain()` style) reading 000 (GREEN). Left: a row of eight cells on one YELLOW CLK line, all 0 (GREEN) except one GOLD 1.
> {binary}: the right-hand bits count 000, 001, 010, … 111 in binary, one step per beat. {step}: in time with them, the GOLD 1 on the left steps one cell to the right per state, wrapping from the eighth cell back to the first. Both keep stepping quietly for the rest of the scene.
> {count}: under the left row "8 flip-flops", under the right "3 flip-flops" (numbers GOLD).
> {question}: both rows dim a little; a YELLOW "?" between them and the line "What do we gain from one flip-flop per state?"
> Checked (Python 3.11.9): the eight binary codes 000 … 111 and the eight one-hot codes 10000000 … 00000001 label the same eight states; ⌈log₂ 8⌉ = 3.

[c4.hook.1] {title} This is part four of our lecture on state assignment. {last} Last time, the ring of five did nothing until we set it into a used state. {fun} That ring spent two more flip-flops than it needed, mostly for fun. {real} This part is about a style that spends flip-flops just as freely, and is used a lot in real designs.

[c4.hook.2] {eight} Here are eight states, built two ways. {binary} On the right, three flip-flops count through them in binary. {step} On the left, eight flip-flops pass a single one along, one flip-flop for each state. {count} That's eight flip-flops where three would do. {question} So what do we gain by giving every state its own flip-flop? {pause=1.5}

## Scene 2 · One flip-flop per state (ch4_s2_onehot)

> {name}: p. 137's second slide title, "One Hot State Encoding", at the top. The hook's row of eight cells returns centred, all 0 except one GOLD 1; the hook's binary trio waits small at the right.
> {only}: the slide's first bullet, verbatim, under the title: "This is a shift register design style where only one FF at a time holds a 1". {hot}: the GOLD 1 steps along the row and wraps round; a small YELLOW tag "hot" rides above it; each cell it leaves drops back to 0.
> {ring}: ch2 s5's ring of five appears small at the left with its two adjacent GOLD 1s circulating, tag "Part 2: two 1s". {exactly}: under the main row, "one-hot: exactly one 1"; the ring fades.
> {perstate}: labels "state 0" … "state 7" appear under the eight cells; each label brightens as the hot tag passes its cell. {glance}: a YELLOW pointer drops onto the GOLD 1 and its state label lights, tag "state = where the 1 is". {compare}: the second bullet, verbatim apart from Part 1's ceiling convention: "Consequently we have 1 FF per state, compared with ⌈log₂ m⌉ for sequential assignment". Beneath it two columns, "sequential: ⌈log₂ m⌉" and "one-hot: m". {eight}: m = 8 fills in, "3" and "8" (GOLD); the binary trio slides up beside the "3", the row of eight beside the "8".
> {burn}: a YELLOW quote card with the lecturer's words: "here we really are burning through the flip-flops".
> {why}: the quote card and the two cost columns clear, leaving the slide title and the bullets above; the row of eight returns to the centre with its GOLD 1, and a YELLOW "?" appears above it (cleared at {simple}).
> {simple}: bullet 3, verbatim: "However, can result in simple fast state machines". {outputs}: bullet 4, verbatim: "Outputs are generated by ORing together appropriate FF outputs", with a small sketch under it: two of the eight cells' outputs (GREEN) joined by an OR gate, its output GREEN.
> {test}: the four bullets shrink to a strip in a corner; a small traffic-light head (three dark lamps) fades in beside them, pointing ahead to s3.

[c4.onehot.1] {name} This style is called one-hot encoding. {only} It's a shift-register style of design, in which only one flip-flop at a time holds a one. {hot} That flip-flop is the hot one. As the machine steps from state to state, the one steps from flip-flop to flip-flop.

[c4.onehot.2] {ring} You've seen something close to this. Part two's ring of five carried a pair of ones round. {exactly} A one-hot machine always carries exactly one. {perstate} So each state has its own flip-flop, and the state is simply wherever the one is. {glance} To see which state the machine is in, you just look for the one.

[c4.onehot.3] {compare} A sequential assignment needs only log base two of the number of states, rounded up. One-hot needs one flip-flop for every state. {eight} For eight states, that's eight flip-flops instead of three. {burn} In the lecturer's words, here we really are burning through the flip-flops.

[c4.onehot.4] {why} So why would anyone design this way? {pause} {simple} The slide's answer is that one-hot can give simple, fast state machines. {outputs} And each output comes from joining the outputs of the right flip-flops, the ones for the states where it should be on, with an or gate. {test} Let's test both claims on a machine you already know.

## Scene 3 · The traffic light, one-hot (ch4_s3_ring4)

> {back}: ch1 s3's traffic light returns as p. 138 draws it: four states in a ring, each a three-lamp head with its lamps lit in their own colours (red at the top, red-and-amber at the right, green at the bottom, amber at the left), arrows clockwise. Under each state, ch1 s3's three-bit code (100, 110, 001, 010, GREEN). {order}: an arrowhead runs round clockwise as each state is named, its head brightening. {clock}: a small YELLOW tag "CLK only, no inputs".
> {four}: p. 138's text, verbatim: "For 1 hot, we need 1 FF for each state, i.e., 4 in this case". Four flip-flop cells appear below the ring, labelled r, ra, g, a (GREEN), each with a tiny copy of its state's head. {names}: each label lights as its colour is said. {perstate}: tag "one per state (Part 1: one per lamp)", ch1 s3's three lamp-named flip-flops shown DIM beside the four for a moment.
> {codes}: the three-bit codes dim and fly away; one-hot codes come out of the cells (TransformFromCopy) to sit under the states: 1000 (red), 0100 (red-and-amber), 0010 (green), 0001 (amber), each with its single 1 in GOLD.
> {table}: p. 138's table builds at the right, verbatim: headers `r ra g a` | `r′ ra′ g′ a′` (GREEN), rows 1000 | 0100, 0100 | 0010, 0010 | 0001, 0001 | 1000, each row flying in from its state on the ring. {wrap}: an arrow from the last row's next state loops back up to the first row. {unused}: under the table, "Unused states. Lots!" (slide verbatim) and "16 − 4 = 12" (GOLD).
> {inspect}: the table's next-state half gets a BLUE tag "= D inputs". {dra}: the next-state column ra′ (1, 0, 0, 0) and the current column r (1, 0, 0, 0) glow together; `D_{ra} = r` appears (D BLUE, r GREEN). {dg} `D_g = ra`, {da} `D_a = g`, {dr} `D_r = a` follow, each pair of columns glowing as it's named. They line up as the slide writes them: "D_a = g   D_g = ra   D_ra = r   D_r = a".
> {shift}: the four cells wire up into p. 139's shift register: Q of r into D of ra, ra into g, g into a, and Q of a back over the top into D of r, one YELLOW CLK line underneath. A GOLD 1 circulates. This ring of four is the hero of s4 to s7. {same5}: ch2 s5's ring of five appears small beside it, its two GOLD 1s circulating, then fades.
> Checked (Python 3.11.9): D_ra = r, D_g = ra, D_a = g, D_r = a reproduce 1000 → 0100 → 0010 → 0001 → 1000 (bit order r ra g a); 12 of the 16 patterns are unused.

[c4.ring.1] {back} The lecturer goes back to the traffic light from part one. {order} It steps through four states in the British order: red, then red and amber, then green, then amber, and back to red. {clock} It has no inputs, and it moves on one state at every edge of the clock. {four} Four states, so one-hot needs four flip-flops, one for each state. {names} Call them the red, red-and-amber, green and amber flip-flops. {perstate} This time each one stands for a state, not a lamp.

[c4.ring.2] {codes} In part one, these states had three-bit codes. Now each code has a single one, in that state's own flip-flop. Red is one, zero, zero, zero, red and amber is zero, one, zero, zero, and so on. {table} In the transition table, each state's next state is the next row down, {wrap} and amber goes back to red. {unused} Four flip-flops give sixteen patterns, and only four are used. That leaves twelve unused states, or as the slide says, lots.

[c4.ring.3] {inspect} Now read the dee inputs off the table. With dee flip-flops, they're just the next state. {dra} The next-state column for red-and-amber reads one, zero, zero, zero, exactly the current red column. So the red-and-amber flip-flop's input is the red flip-flop's output.

[c4.ring.4] {dg} In the same way, green takes its input from red-and-amber, {da} amber from green, {dr} and red from amber. {shift} That's a ring of four, a shift register fed back on itself, and it needs no logic at all to work out the next state. {same5} It has the same shape as part two's ring of five, but it carries a single one.

## Scene 4 · Lighting the lamps (ch4_s4_outputs)

> s3's ring of four stays at the top, its GOLD 1 paused in r; s3's traffic-light ring sits small at the left. Three lamp icons (red, amber, green, all dark) wait at the bottom right, labelled R, A, G.
> {lamps}: a small tag between the cells and the lamps: "4 flip-flops, 3 lamps".
> {red}: on the small state ring, the red and red-and-amber states glow; among the cells, r and ra glow. {redor}: an OR gate appears below r and ra, wired from their outputs; its output runs down to the red lamp. p. 138's `R = r + ra` beside it (r, ra GREEN).
> {amber}: the red-and-amber and amber states glow. {amberor}: a second OR gate, fed by ra and a, runs to the amber lamp; `A = ra + a`. {green}: only the green state glows; a plain wire from g to the green lamp; `G = g`. The three equations line up as p. 138 writes them: "R = r + ra   A = ra + a   G = g". {rule}: in s2's corner strip, bullet 4 ("Outputs are generated by ORing together appropriate FF outputs") glows.
> {circuit}: the pieces settle into p. 139's circuit, its layout verbatim: flip-flops r, ra, g, a left to right with D_r, D_ra, D_g, D_a at their inputs (BLUE), Q of each into the next D, Q_a back over the top into D_r, CLK (YELLOW) along the bottom. Below them, the OR gate for R (fed by Q_r and Q_ra), the OR gate for A (fed by Q_ra and Q_a), and G as a straight wire down from Q_g. {ors}: the two OR gates and the G wire flash.
> {run}: the GOLD 1 steps round on the spoken beats; the lamps light in their own colours, red, red-and-amber, green, amber, and are dark otherwise; the small state ring's arrowhead keeps step.
> {logic}: a dashed box round the four flip-flops tagged "next-state logic: none"; another round the OR gates tagged "output logic: 2 OR gates" (GOLD 2).
> Checked (Python 3.11.9): with R = r + ra, A = ra + a, G = g, state 1000 lights red; 0100 red and amber; 0010 green; 0001 amber.

[c4.lamps.1] {lamps} The flip-flops now say which state we're in, but there are four flip-flops and only three lamps. {red} The red lamp is on in two states, red and red-and-amber. So it should light when either the red flip-flop or the red-and-amber flip-flop holds the one. {redor} An or gate joins those two outputs.

[c4.lamps.2] {amber} The amber lamp is on in red-and-amber and in amber, {amberor} so another or gate joins those two flip-flops. {green} The green lamp is on only in the green state. It's simply the green flip-flop's output, a plain wire. {rule} That's the slide's rule at work. Each output joins the flip-flops of the states where it's on.

[c4.lamps.3] {circuit} Here's the whole circuit, as the slide draws it. Four dee flip-flops share one clock signal. Each output is wired to the next input, and the last one runs back to the first. {ors} Underneath are the two or gates and the wire for green. {run} As the one goes round, the lamps follow, red, then red and amber, then green, then amber. {logic} So the next-state logic is gone, but we do need a little output logic, two gates.

## Scene 5 · Two ways to light the lamps (ch4_s5_compare)

> Two panels. Left, headed "Lecture 9": p. 127's circuit, small and redrawn in our style: flip-flops R, A, G (GREEN labels) on one YELLOW CLK line; an exclusive-or gate into D_R fed by Q_R and Q_A; D_A wired from Q̄_A; an AND gate into D_G fed by Q_R and Q_A; the three lamps hang straight off Q_R, Q_A and Q_G. Above it ch1 s3's codes, R A G = 100, 110, 001, 010, and p. 126's equations `D_R = R \oplus A`, `D_A = \bar{A}`, `D_G = R \cdot A` (D BLUE). Right, headed "one-hot": s4's circuit, small.
> {l9}: the left panel builds; the right one waits dim. {xor}: the exclusive-or gate and `D_R = R ⊕ A` glow. {toggle}: the wire from Q̄_A to D_A glows, and beside it the A column of the codes, 0, 1, 0, 1, flips on the beat. {and}: the AND gate and `D_G = R·A` glow; on the codes, 110 (red-and-amber) lights, then 001 (green) after it. {noout}: a tag on the lamps, "no output logic".
> {side}: both panels at full brightness. {loop}: in each circuit, a translucent band marks the loop (flip-flop outputs back to flip-flop inputs) and a second band marks what comes after the flip-flops. Left: the exclusive-or and AND gates sit in the loop band. Right: the loop band holds only wires, and the two OR gates sit in the after band. {moved}: an arrow carries a small gate icon from the left panel's loop band to the right panel's after band.
> {same}: one line under both panels: "same machine, same lamps, different state assignment".
> {board}: the panels shrink up; the scoreboard (started in ch1 s8, extended in ch2 s7: columns assignment, flip-flops, next-state gates, output logic; rows binary, sliding, ring) slides in. A sub-heading "traffic light" and two new rows: {row9} "Lecture 9 | 3 | 2 (⊕, AND) | none", {rowhot} "one-hot | 4 | 0 | 2 OR". Numbers GOLD. {depends}: a small tag recalling p. 132, "best depends on what you optimise".
> Checked (Python 3.11.9): D_R = R ⊕ A, D_A = Ā, D_G = R·A reproduce 100 → 110 → 001 → 010 → 100 (bit order R A G); the A column is 0, 1, 0, 1. Gate counts (inverters and Q̄ outputs free): Lecture 9, 2 next-state gates and no output logic; one-hot, none and 2 OR gates.

[c4.compare.1] {l9} Now compare lecture nine's design. It used part one's codes, with three flip-flops, one per lamp. {xor} The red lamp's flip-flop is fed by an exclusive-or gate, which takes the red and amber outputs. {toggle} The amber lamp's flip-flop takes its own inverted output, so amber simply flips on every edge of the clock. {and} The green lamp's flip-flop gets an and gate, fed by the red and amber outputs, because green always follows the one state with both of them lit. {noout} And each lamp is driven straight from one of the flip-flops, so there's no output logic.

[c4.compare.2] {side} Put the two side by side. {loop} Lecture nine's design needs two gates between its flip-flops. One-hot needs none there, and two gates after them, for the lamps. {moved} So the logic hasn't vanished, it has moved from inside the loop to the outputs. {same} Same machine, same lamps. Only the state assignment changed.

[c4.compare.3] {board} Both designs go on the scoreboard. {row9} Lecture nine's has three flip-flops, two next-state gates and no output logic. {rowhot} One-hot has four flip-flops, no next-state gates, and two output gates. {depends} Which is better depends on what you optimise, as part one said. {pause}

## Scene 6 · The same trap (ch4_s6_demo)

> Re-enact the lecturer's simulation (frames 00:36:10 to 00:37:44) in our style, not the simulator's: s4's circuit, with a "1 Hz" YELLOW clock source wired through a switch (L6 `toggle`) into CLK, the four flip-flops reading 0 (GREEN), and the three lamps dark. Each flip-flop has ch3 s6's set pin on top (an input with a bubble, RED) with its push button, held at 1.
> {sim}: the circuit builds, tag "the lecturer's simulator". {run}: YELLOW pulses run along CLK, one per beat; nothing changes and the lamps stay dark. {why}: a YELLOW "?" over the lamps.
> {zeros}: the four 0s glow; tag "0000: unused" (DIM) and the lecturer's words, "same deal as before". {shift}: on the next edge each 0 visibly slides into the next cell and lands as 0 again.
> {stop}: the switch opens and CLK greys out. {any}: the four set pins glow briefly in turn. {set}: the amber flip-flop's set pin flips to 0 (RED) and its bubble flashes. {amber}: Q_a turns 1 (GOLD), and the amber lamp lights at once through its OR gate, with no edge of the clock (as in the frame at 00:37:20). {release}: the set pin flips back to 1.
> {clock}: the switch closes and CLK turns YELLOW again. {go}: the GOLD 1 circulates on the spoken beats, amber, red, red-and-amber, green, amber, the lamps lighting in their own colours.
> {trap}: the circuit slides to one side, small, its GOLD 1 still going round. {loops}: beside it, the sixteen patterns as six small loops of DIM four-bit cells, laid out like ch3 s5's eight loops of the ring of five: 0000 alone, 1111 alone, the used loop GREEN-outlined, and three more; each loop's arrows go only round itself. {gap}: one loop is pulled out large, 0101 ⇄ 1010, each with its traffic-light head: red and amber lit, then red and green lit together, with a YELLOW "!" on the red-and-green head. No RED paint: the wrong lamps are the trouble.
> {startup}: a closing line under the loops: "start it in a used state".
> Checked (Python 3.11.9): 0000 → 0000. Setting a gives 0001 (the amber lamp lights at once, since A = ra + a), then red, red-and-amber, green, amber. The 16 patterns fall into 6 loops: 0000; 1111; the used loop; 0011 → 1001 → 1100 → 0110; 0101 → 1010; 0111 → 1011 → 1101 → 1110. No unused pattern reaches a used one. 0101 lights red and amber, 1010 red and green.

[c4.demo.1] {sim} The lecturer built this circuit in his simulator. {run} The clock signal ticks, and nothing lights up. {why} Can you see why? {pause} {zeros} It's the same deal as the ring of five. The flip-flops start at all zeros, and all zeros is an unused state, because a one-hot state has exactly one flip-flop at one. {shift} So every edge of the clock shifts zeros into zeros.

[c4.demo.2] {stop} First he disconnects the clock signal, so that nothing shifts while he works. {any} Any single one would make a used state. {set} He picks the amber flip-flop and pulls its asynchronous set input low. Remember, the little circle means active low. {amber} Its output goes to one, and the amber lamp lights at once, through its or gate. {release} Then he puts the set input back high, so the flip-flop works normally again.

[c4.demo.3] {clock} He reconnects the clock signal, {go} and the lights run. Amber, red, red and amber, green, amber. {trap} Like the ring of five, this ring can never find its own way back, because any pattern just goes round. {loops} Its sixteen patterns fall into six loops, and only one of them is ours. {gap} Power it up with two ones that have a gap between them, and the lamps alternate for ever between red with amber, and red with green. {startup} So a one-hot machine has to start in a used state.

## Scene 7 · As fast as it gets (ch4_s7_fast)

> {limit}: L8 ch1 s4's path returns (`path_diagram()`, ../l08-timing-metastability/scenes/ch1_s4_path.py): FF0 → "Combinational Logic (CL)" → FF1 on one YELLOW CLK line, Q0 GREEN, D1 BLUE. {path}: a pulse runs FF0 → CL → FF1. {bar}: L8 ch1 s6's budget bar (`budget_bar()`, ch1_s6_setup.py) under it: YELLOW T_c outline, segments PINK "t_pc", PURPLE "t_pd", GOLD "t_su", with `T_c \ge t_{pc} + t_{pd} + t_{su}`, each term in its segment's colour.
> {ring}: s4's ring of four comes in above the path; one link, Q_r into D_ra, lights; copies of r and ra fly onto FF0 and FF1 (TransformFromCopy), and the CL box collapses to a bare wire.
> {zero}: the PURPLE segment shrinks to nothing; `t_{pd} = 0` in PURPLE. {shrink}: the inequality loses its middle term, `T_c \ge t_{pc} + t_{su}`. {nums}: L8's flip-flop numbers under the segments, "0.2 ns" under PINK and "0.1 ns" under GOLD, then `T_c \ge 0.2 + 0.1 = 0.3\ \text{ns}`. {freq}: `f_c \le \frac{1}{0.3\ \text{ns}} \approx 3.3\ \text{GHz}` with a GREEN tick. Numbers GOLD. {example}: L8 ch1 s6's worked bar appears small underneath for scale, PINK 0.2, PURPLE 4.7, GOLD 0.1, "T_c ≥ 5.0 ns, f_c ≤ 200 MHz". {alone}: the ring's bar, now only PINK and GOLD, glows beside it, tag "flip-flops alone".
> {outside}: the ring's two OR gates hang below it; a dashed box round the ring is tagged "the loop", and the OR gates sit outside it, tagged "after the loop: delays the lamps, not the clock".
> {l9}: s5's Lecture 9 circuit, small, beside it, with its exclusive-or and AND gates inside its loop; under it a second budget bar with the PURPLE t_pd segment back, tagged "slower of ⊕ and AND".
> {hold}: back on the ring's bar, L8 ch2's hold check in small: a GOLD t_hold window just after the edge, and the PINK t_pc arrow reaching past it, tagged "shift-register case (Lecture 8, Part 2)". {verdict}: the lecturer's verdict in two halves, side by side: "fast" (GREEN tick, the 0.3 ns bar) and "burns flip-flops" (s2's "8 vs 3", GOLD).
> Checked (Python 3.11.9): 0.2 + 0.1 = 0.3 ns; 1 / 0.3 ns = 3.33 GHz; L8's example 0.2 + 4.7 + 0.1 = 5.0 ns, 1 / 5.0 ns = 200 MHz.

[c4.fast.1] {limit} The lecturer's last point is speed. Remember from lecture eight what limits the clock speed. {path} Every path runs from one flip-flop, through logic, to the next. {bar} So the clock period must cover the clock-to-output delay, the logic's delay, and the set-up time.

[c4.fast.2] {ring} Now look at the one-hot ring. Each output is wired straight into the next input. {zero} There's no logic in the loop, so the logic's delay is zero. {shrink} The clock period only has to cover the clock-to-output delay and the set-up time. {nums} With lecture eight's flip-flops, that's zero point two plus zero point one, which is zero point three nanoseconds.

[c4.fast.3] {freq} That's a clock frequency of about three point three gigahertz, as fast as these flip-flops can go. {example} In lecture eight's example, four point seven nanoseconds of logic held the clock to two hundred megahertz. {alone} Here the flip-flops alone set the limit.

[c4.fast.4] {outside} The or gates for the lamps sit after the loop. They delay the lamps a little, but the clock never waits for them. {l9} Lecture nine's design has two gates inside its loop, an and gate and an exclusive-or gate, so its clock period must also cover the slower of the two.

[c4.fast.5] {hold} One more check from lecture eight. With no logic between flip-flops, new data reaches the next input as early as it possibly can. That's the hold-time worry, in the shift register's case, and flip-flops are normally designed to meet it. {verdict} So, in the lecturer's words, one-hot machines can be fast, but we could end up burning lots of flip-flops.

## Scene 8 · Recap and next (ch4_s8_recap)

> {recap}: a "Recap" heading at the top over six faint empty slot frames on the 3 × 2 grid (ch2_s8_recap.py's layout) that r1–r6 then fill, each a visual callback to this chapter's own scenes, not a text list.
> Six small panels fill the frame one per sentence, each a small version of its scene's visual (same objects, colours and styling) with its short line under it.
> {r1}: s2's row of eight cells, the GOLD 1 stepping along under its "hot" tag; "one 1 at a time: one flip-flop per state".
> {r2}: s3's ring of four, r → ra → g → a → r on a YELLOW CLK line, beside p. 138's table; "a ring of four: no next-state logic".
> {r3}: s4's two OR gates and the G wire under the ring, the lamps lit in their colours; "R = r + ra, A = ra + a, G = g".
> {r4}: s5's two panels with the arrow carrying the gate from the loop to the outputs; "the logic moved out of the loop".
> {r5}: s6's amber flip-flop with its RED active-low set pin, the amber lamp lit; "start in a used state".
> {r6}: s7's budget bar with the PURPLE segment gone, `T_c \ge t_{pc} + t_{su}`; "no logic in the loop: as fast as the flip-flops".
> {next}: the panels shrink away. ch5's subject in silhouette: a stream of bits (white 0s and 1s) sliding past, with one recurring 8-bit pattern outlined in YELLOW each time it passes; three empty state circles fade in below it. {both}: under the circles, two chips as in ch5's hook, "Part 5: two flip-flops" and "Part 6: one-hot".
> End card after the last word, held ~8 s; the music carries it.

[c4.recap.1] {recap} Let's recap. {r1} In one-hot encoding, exactly one flip-flop holds a one, so there's one flip-flop per state. {r2} Built one-hot, the traffic light is a ring of four, with no next-state logic at all. {r3} Its lamps come from two or gates and one plain wire.

[c4.recap.2] {r4} Compared with lecture nine's design, the logic moved out of the loop and onto the outputs. {r5} Like any ring, it has to be set into a used state, here with an asynchronous set. {r6} And with no logic in its loop, it runs as fast as its flip-flops allow. {pause}

[c4.recap.3] {next} Next time, a real machine with inputs, from a Cambridge exam question. {both} We'll build it the usual way, with two flip-flops, and then one-hot. {pause}
