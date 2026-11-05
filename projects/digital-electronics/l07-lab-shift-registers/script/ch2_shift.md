# Chapter 2 · Shift registers and serial links

Digital Electronics · Lecture 7 (Hardware Labs and Shift Registers), part 2 of 2. Source: Digital Electronics slides (combined_26.pdf), p. 101 (its first slide recapped in Scene 1 only; its second slide), pp. 102–103, and p. 104's first slide (a teaser); lecture recording 00:39:41–00:57:19.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Spoken names: "dee in" is D_in; "cue zero" to "cue three" are Q0–Q3; "flip-flop zero" is FF0; "preset" and "clear" are PRE and CLR; "chip one" and "chip two" are IC1 and IC2 (IC1a … IC2b are on screen only, never voiced); "seventy-four H C seventy-four" is 74HC74; "see-moss" is CMOS; "U-S-B" is USB; "the clock period" is T_c and "the clock frequency" f_c. Bit patterns are spoken digit by digit ("one, one, zero") and written in flip-flop order, Q0 Q1 Q2 left to right as the chain is drawn, never read as numbers. Colours (PLAN.md): CLK YELLOW; D_in and every D input BLUE; Q outputs GREEN; preset and clear RED; the travelling bits GOLD digits; an unknown drawn at both levels in a timing diagram and as a DIM "?" digit inside a box; unused states DIM; the set-up/hold window GOLD and the clock-to-Q delay PINK. Timing diagrams in L6's square style: clock on top, thin guides at the rising edges, small up-arrows, outputs changing a little after each edge, as p. 102 draws them. No code on screen, and no circuit simulator is installed. Every bit sequence below was checked in Python 3.11.9 (`python3 -I`, standard library): p. 102's trace (after each edge Q0 Q1 Q2 = 0XX, 00X, 100, 110, 111, 011, 001, 100, 110); "N stages forget their start after N edges" (N = 3, 4, 5, every start state and input); the demo's LED patterns; the latch chain; the parallel load and shift-out; the serial link for the words 110, 100, 011 and 101; the 0-to-4 counter's unused states; 1 GHz ↔ 1 ns.

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card on {title}: "Hardware Labs and Shift Registers", "Digital Electronics · Lecture 7", "Part 2 · Shift registers and serial links"; it clears on {counter}.
> {counter}: L6 ch6 s6's synchronous counter as it was built there (`sync_counter()` and `led_chain` from ../l06-flip-flops-counters/scenes/ch6_s6_circuit.py): FF0, FF1, FF2, the gates feeding D0, D1, D2 (BLUE), Q0–Q2 GREEN, one YELLOW CLK line into all three clock triangles, the readout above (Q2 Q1 Q0 in binary, the decimal GOLD). {together}: a pulse runs along CLK, the three triangles flash at the same instant, and the readout steps 0 to 7 and wraps to 0.
> {steps}: the counter shrinks to the left. At right, p. 101's first slide as three short lines that light one by one with the spoken steps: "1 · state transition table", "2 · FF excitation (easy for D-types)", "3 · combinational logic".
> {example}: under them, L6's `mod_table()` (../l06-flip-flops-counters/scenes/ch5_s3_statetable.py) for a 0-to-4 counter: rows 0–4 with next states 001, 010, 011, 100, 000 (FF inputs the same, as for D-types). {unused}: rows 5, 6, 7 (101, 110, 111) DIM, their next-state and FF-input cells filled with YELLOW "X", tag "don't care". {simpler}: the gate block in the shrunken counter shrinks a little (no gates are worked out: the K-map is L6's, not repeated).
> {strip}: the table and steps clear, the counter returns to full size, and its gates and readout fade out. {chain}: the three flip-flops line up: Q0 wired straight to FF1's D, Q1 straight to FF2's D, and a new BLUE "D_in" wire enters FF0's D from the left. This is p. 101's shift register (L8's `build_chain()` from ../l08-timing-metastability/scenes/ch2_s3_shiftreg.py), which s2 picks up as it stands.
> {question}: a YELLOW "?" over the chain.

[c2.hook.1] {title} Last time, we got ready for the hardware lab. Now it's back to the lecture's circuits, {counter} starting with lecture six's synchronous counter. {together} All three flip-flops share one clock signal, so they all change on the same edge, and it counts from zero to seven.

[c2.hook.2] {steps} The lecturer began with a reminder. Any count sequence comes from the same three steps, the state transition table, the flip-flop excitation, and the logic. {example} Here's an example, a counter from zero to four. {unused} It never visits five, six or seven, so its logic can treat them as don't cares, {simpler} and that can make the logic simpler.

[c2.hook.3] {strip} Now take the logic out completely. {chain} Line the flip-flops up, and wire each output straight into the next one's input. {question} With no logic at all, what does a chain of flip-flops do? {pause=1.5}

## Scene 2 · A chain of D flip-flops (ch2_s2_chain)

> p. 101's second slide at full size across the upper middle, carried over from s1's closing chain (L8's `build_chain()`, its make_ff boxes, in L6's style): {ffs} three boxes in a row, FF0, FF1, FF2. {din}: "D_in" (BLUE) into FF0's D. {qs}: each Q (GREEN) runs into the next D and taps up to the labels "Q_0", "Q_1", "Q_2". {clk}: one YELLOW "CLK" line along the bottom, branching into all three clock triangles, which flash together. {nobubble}: zoom on one triangle: no bubble, so beside it a tiny YELLOW clock trace with up-arrows and the tag "rising edge" (L6 ch2's symbol rule).
> {edge}: GOLD digits 1, 0, 0 in FF0, FF1, FF2, a DIM "0" on the D_in wire, and a small YELLOW CLK trace under the chain with one rising edge. {old}: at the edge, three short arrows light at the same instant, D_in → FF0, Q_0 → FF1, Q_1 → FF2, each carrying a ghost of the value it had just before; tag "all at once: the old values". {move}: the digits become 0, 1, 0; two more edges give 0, 0, 1, then 0, 0, 0 as the 1 leaves through Q_2 (checked). A small BLUE arrow under the row, "one place per edge".
> {latch}: ours, a DIM what-if with the tag "Lecture 6": the three boxes become L6 ch1's transparent D latches (EN in place of the triangle). {race}: the CLK trace goes high, a shaded band; D_in = 1 runs through all three in one go (GOLD 1, 1, 1), and the row gets a RED cross. Checked: with all three latches open, a 1 at D_in reaches Q_0 Q_1 Q_2 = 1 1 1 within one high phase. {instant}: back to the flip-flops, triangles glowing, with L6 ch2's recap line "an instant, not a window". {nextlec}: a small DIM tag "Lecture 8: why the hand-over is clean".
> {names}: the title "Shift register" above the chain. {serial}: a brace under D_in, "serial input: one bit at a time". {parallel}: a brace over Q_0, Q_1, Q_2, "parallel output: all at once". The chain carries into s3 (shrunk to a strip at the top), s5 and s6.

[c2.chain.1] {ffs} Here's the chain from the slides, three dee flip-flops in a row. {din} Data comes in on the left, at the data input. {qs} Each output goes straight into the next flip-flop's dee input, and up to its own label, cue zero, cue one and cue two. {clk} One clock signal drives all three, so the chain is synchronous. {nobubble} And there's no bubble on the clock inputs, so they trigger on the rising edge.

[c2.chain.2] {edge} So what happens at a rising edge? {pause} Every flip-flop copies its own dee input, and that's its left-hand neighbour's output. {old} They all sample at the same instant, so each one takes its neighbour's old value, from just before the edge. {move} The result is that every bit moves exactly one place to the right.

[c2.chain.3] {latch} Why flip-flops, and not lecture six's transparent latches? {pause} {race} With latches, while the clock signal is high, every stage is open at once, so a bit runs straight through all three in one go. {instant} That's why we wanted changes at one instant, the edge. {nextlec} How flip-flops hand over so cleanly, despite their own delays, is next lecture's question.

[c2.chain.4] {names} This circuit is called a shift register. {serial} It has one serial input, on the left, which takes one bit at a time, {parallel} and parallel outputs, cue zero, cue one and cue two, which you read all at once.

## Scene 3 · Following the bits (ch2_s3_trace)

> {diagram}: s2's chain shrinks to a strip along the top, a DIM "?" digit in each box. Below it, p. 102's timing diagram in L6's square style (`timing_diagram()` from ../l06-flip-flops-counters/scenes/ch2_s4_master.py): rows "CLK" (YELLOW), "D_in" (BLUE), "Q_0", "Q_1", "Q_2" (GREEN), labels at left; nine rising edges with thin vertical guides and small up-arrows, numbered 1–9 in small DIM text above.
> {clock}: CLK drawn. {input}: D_in drawn whole, as on p. 102: low, rising between edges 2 and 3, falling between edges 5 and 6, rising between edges 7 and 8 and staying high, so it reads 0, 0, 1, 1, 1, 0, 0, 1, 1 at edges 1–9; a small BLUE digit at each guide as the values are spoken. {unknown}: before edge 1, Q_0, Q_1 and Q_2 are each drawn at both levels, tag "unknown".
> Q_0, edge by edge, each change a little after its edge, with a BLUE dot on D_in at the guide and a GREEN dot on Q_0 just after: {e1} edge 1, the two levels end at 0; {e2} edge 2, stays 0; {e3} edge 3, rises to 1; {e5} edges 4 and 5, stays 1; {e6} edge 6, falls to 0. {copy}: Q_0's trace flashes against D_in's.
> {q1first}: Q_1 at edge 1: an arrow from Q_0's unknown stretch, and Q_1 stays at both levels. {q1known}: edge 2, it settles to 0. {q1rest}: edges 3–6 draw 0, 1, 1, 1. {q2}: Q_2 stays at both levels until edge 3, then draws 0, 0, 1, 1 at edges 3–6. {run}: edges 7–9 play on their own across all three rows (Q_0: 0, 1, 1; Q_1: 0, 0, 1; Q_2: 1, 0, 0). All along, the top strip's GOLD digits update with each edge: 0??, 00?, 100, 110, 111, 011, 001, 100, 110 (PLAN.md's checked table).
> {same}: a ghost copy of Q_0's waveform drops onto Q_1 and slides one clock period right to match it exactly, then onto Q_2, two periods right. {first}: a GOLD highlight follows the first 1: on Q_0 at edge 3, Q_1 at edge 4, Q_2 at edge 5, while in the top strip a GOLD "1" hops FF0 → FF1 → FF2.
> {slide}: p. 102's line, verbatim, under the diagram: "See data moves one position to the right on application of each clock edge". {forget}: ours, checked: the three two-level stretches flash in turn, ending at edges 1, 2 and 3; tag "after 3 edges: all known", then "N stages: N edges".

[c2.trace.1] {diagram} Let's follow some bits, using the slide's timing diagram. {clock} The clock signal is on top, with nine rising edges. {input} Below it is the data input. Read at each edge, it's zero, zero, one, one, one, zero, zero, one, one. {unknown} Before the first edge, the flip-flops could hold anything, so all three outputs are drawn at both levels.

[c2.trace.2] {e1} At the first edge, the input is zero, so cue zero becomes zero, a moment after the edge. {e2} At the second edge, it's still zero. {e3} At the third, the input is one, so cue zero goes to one, {e5} and stays there for two more edges. {e6} At the sixth, it drops back to zero. {copy} Cue zero is just the input, taken at each edge.

[c2.trace.3] {q1first} Now cue one. Its input is cue zero, so at the first edge it copies cue zero's old value, which is unknown. {q1known} It becomes known at the second edge, as zero, {q1rest} and from then on it follows cue zero, one edge behind. {q2} Cue two follows cue one in the same way, and stays unknown until the third edge. {run} The last three edges work just the same.

[c2.trace.4] {same} Now look at the outputs together. It's the same waveform three times, each one clock period further right. {first} Follow the first one that goes in. It enters cue zero at edge three, cue one at edge four, and cue two at edge five. {slide} The data moves one position to the right on every edge. {forget} And after three edges, every output is known. In general, a shift register forgets how it started after one edge for every stage.

## Scene 4 · Watching it shift (ch2_s4_demo)

> A re-enactment of the lecturer's simulation "Four-Bit Shift Register" (Yenka, frame 00:46:40), redrawn in our style, not a screenshot: the title "Four-Bit Shift Register" and a small DIM "simulation" tag. Leave the S and R pins out of this drawing; s5 introduces them.
> {sim}: four make_ff boxes in a row, each Q (GREEN) into the next D, labelled "Q_0" to "Q_3". {chips}: the boxes take the labels IC1a, IC1b, IC2a, IC2b, and two DIM outlines group them in pairs (part 1's labelling, ch1 s6). {decode}: each outline is tagged "74HC74"; under one, ch1 s4's part-number split, styled as there for 74 | HC | 00, now "74 | HC | 74", with "dual D flip-flop" under the last 74.
> {leds}: under each Q, a "270 Ω" resistor and an LED to 0 V, so a 1 lights it (ch1 s5's LED-and-resistor; L6's `led`, GREEN when lit, DIM when off). {boom}: on one LED, a DIM what-if: the resistor lifts out and the LED bursts in RED (the lecturer's joke about the simulator), then the resistor is back.
> {switches}: at left, two L6 `toggle` switches: "INPUT" (BLUE) into IC1a's D, and "CLK" (YELLOW) on one line into all four clock triangles. A small CLK trace logs each flip of the switch; every 0 → 1 is marked with an up-arrow.
> The run, as in the recording (checked; LEDs listed Q_0 to Q_3, left to right): {fill} INPUT → 1, four rising edges: 1000, 1100, 1110, 1111. {empty} INPUT → 0, four edges: 0111, 0011, 0001, 0000. {single} INPUT → 1 for one edge (1000), then back to 0. {walk} three edges: 0100, 0010, 0001. {out} one more: 0000, and a GOLD "1" slides off the right end.
> {sipo}: a short stream of GOLD bits on the INPUT wire flows in, and a bracket over the four LEDs reads them as one 4-bit word; tag "serial in, parallel out".

[c2.demo.1] {sim} The lecturer then showed a four-bit version in a circuit simulator. {chips} Its four dee flip-flops sit on two chips, two on each, labelled the way part one taught. {decode} Each chip is a seventy-four H C seventy-four, and you can decode that now. The last seventy-four means two dee flip-flops in one package. {leds} Every output drives a light through a two hundred and seventy ohm resistor, as part one said it must. {boom} Take the resistor out, and the simulator makes the light explode.

[c2.demo.2] {switches} There's a switch on the input, and one on the clock signal, flipped by hand, so each flip from zero to one is a rising edge. {fill} Set the input to one, and give it four edges. Ones fill the register from the left. {empty} Set it to zero, and on each edge, a zero moves in behind them.

[c2.demo.3] {single} Now send a single one, for just one edge. {walk} The light that's on walks along, one place per edge, {out} and the next edge shifts it out of the end. {sipo} Bits go in one at a time on one wire, and come out as a four-bit word. That's serial in, parallel out.

## Scene 5 · Loading in parallel (ch2_s5_load)

> {back}: s4's drawing clears to one of its flip-flop boxes, enlarged at centre, with a small DIM "simulation" tag. {pins}: RED pins grow from it, "PRE" on top and "CLR" underneath (L8's `pin()`, L6 ch3's style), tag "asynchronous".
> {force}: a YELLOW CLK trace beside it stays flat (no edge); CLR pulses and Q drops to 0 at once, then PRE pulses and Q jumps to 1. Tag "no clock edge needed". {start}: a small reminder of L6 ch3's preview: three flip-flops with their CLR pins joined on one RED line; a pulse, and three GOLD 0s; tag "known start state".
> {second}: s2's three-flip-flop chain returns at centre, each box now with RED PRE and CLR pins; D_in shows a DIM "0" (tied to 0 from here on). {load}: above the chain, "D_0 D_1 D_2 = 1 1 0" (GOLD digits). PRE flashes on FF0 and FF1 and CLR on FF2, all at once, and GOLD digits 1, 1, 0 appear in the three boxes together. {word}: the three digits pulse. {parallel}: tag "parallel in".
> {shift}: a small CLK trace under the chain; a short queue area opens to the right of Q_2. {way}: Q_2's wire glows, showing the 0. {e1}: rising edge 1: the 0 drops off Q_2 into the queue, and the digits step right, a DIM 0 entering from D_in: 0, 1, 1. {e2}: edge 2: a 1 drops into the queue, pushing the 0 right, and the chain reads 0, 0, 1. {e3}: edge 3: the other 1 follows; the chain reads 0, 0, 0 and the queue "1 1 0", the first bit out furthest right (checked: 110 → 011 → 001 → 000; out 0, 1, 1).
> {piso}: tag "parallel in, serial out", beside a small copy of s4's "serial in, parallel out" tag. The chain, its pins and the queue's "1 1 0" carry into s6.

[c2.load.1] {back} Back in the simulator, the lecturer pointed out two more pins on every flip-flop. {pins} They're the asynchronous inputs from lecture six, preset and clear. {force} Clear forces the output to zero, and preset forces it to one, at once, whatever the clock signal is doing. {start} Their usual job is to start a state machine in a known state.

[c2.load.2] {second} But they have a second use. {load} Preset each flip-flop that should hold a one, and clear each one that should hold a zero, all at the same moment. {word} Here, that loads the word one, one, zero. {parallel} All three bits go in together, so that's a parallel input.

[c2.load.3] {shift} Now apply edges of the clock, with the data input held at zero. {way} Cue two is the way out, and it starts by showing the zero. {e1} At the first edge, that zero leaves, and the bits all step right. {e2} At the next edge, a one leaves, {e3} and then the other one. {piso} The word went in all at once, and came out one bit at a time. That's parallel in, serial out.

## Scene 6 · The serial data link (ch2_s6_link)

> {link}: p. 103's diagram, centre: a box "Parallel in serial out" (left) with "D_0 D_1 D_2" on wires into its top under "Parallel Data Input"; a box "Serial in parallel out" (right) with "Q_0 Q_1 Q_2" on wires out of its top under "Parallel Data Output". {tx}: the left box lights; it is s5's loaded chain, shrunk to fit (RED PRE/CLR pins, D_in a DIM 0). {wire}: one wire between them, "Serial Data". {rx}: the right box lights; it is s2's chain, three DIM "?" digits. {clk}: one YELLOW "CLK" line under both boxes, into both.
> {load}: GOLD 1, 1, 0 appear in the left chain (from D_0 D_1 D_2); the Serial Data wire shows the 0 from its last flip-flop.
> The transfer, one rising edge at a time on a small CLK trace (checked: the wire carries 0, 1, 1; the receiver's Q_0 Q_1 Q_2 after each edge are 0??, 10?, 110; also checked for 100, 011, 101): {e1} the 0 crosses the wire into the receiver's FF0 (0 ? ?), and the left chain steps right (0 1 1), the wire now showing 1. {e2} the 1 arrives and the 0 moves on (1 0 ?). {e3} the other 1 arrives (1 1 0); the left chain reads 0 0 0.
> {match}: the receiver's "Q_0 Q_1 Q_2 = 1 1 0" lines up under "D_0 D_1 D_2 = 1 1 0", a GREEN tick. {far}: a GOLD trail shows the 0's path, the longest, from FF2 on the left across the wire to FF2 on the right.
> {half}: ours: rewind to after edge 2; the receiver's 1 0 ? glows RED, "part of a word"; tag "which edge completes a word?".
> {old}: above, a DIM ghost of a parallel link (as in L8 ch2 s3): three wires D_0 → Q_0, D_1 → Q_1, D_2 → Q_2, plus a clock wire; a tag "often 8 or more". {cable}: the ghost's wires thicken into a heavy bundle, "heavy, costly cable". {fewer}: the count "3 data wires → 1" between ghost and link.
> {usb}: a small USB plug icon on the Serial Data wire, "USB: a serial link"; ours, a small tag under it: "no clock wire: the receiver recovers it from the data". {cost}: under the wire, "one bit at a time" and then "same time per word → bits N× faster", with "3 bits: ×3" and "a byte: ×8" (numbers GOLD). {trade}: a small balance, "much less cable" (GREEN) against "faster bit rate" (GOLD).

[c2.link.1] {link} Put the two kinds of shift register together, and you get the slide's serial data link. {tx} On the left is parallel in, serial out. {wire} A single serial data wire leads to {rx} a serial in, parallel out register on the right. {clk} And the same clock signal goes to both.

[c2.link.2] {load} Load the word one, one, zero on the left. The wire already carries the bit in the last flip-flop, the zero. {e1} At the first edge, that zero lands in the receiver's first flip-flop. {e2} At the second edge, a one arrives, and the zero moves on. {e3} At the third edge, the other one comes in. {match} Now the receiver reads one, one, zero, the word we sent. {far} The bit that leaves first travels furthest, so every bit lands in its own place.

[c2.link.3] {half} Halfway through, the receiver holds only part of the word, so it has to know which edge completes it. {old} So why go serial at all? Years ago, links were parallel, with one wire per bit, often eight or more, and another wire to carry the clock signal. {cable} Between distant ends, that's a lot of heavy, costly cable. {fewer} A serial link needs just one data wire.

[c2.link.4] {usb} You already know one serial link, U-S-B. It goes a step further, and sends no separate clock signal at all. The receiver recovers the timing from the data itself. {cost} There's a price, though. Bits go one at a time, so to move a word in the same time, they must go N times faster. That's three times here, and eight times for a byte. {trade} Much less cable, but the bit rate goes up.

## Scene 7 · How fast should the clock tick? (ch2_s7_timing)

> {wave}: L6's `clock_wave()` (../l06-flip-flops-counters/scenes/ch1_s1_hook.py), YELLOW, across the upper middle, small up-arrows on its rising edges. {period}: a YELLOW dimension arrow from one rising edge to the next, thin guides at both, "T_c" and "clock period". {falling}: a DIM aside: a small flip-flop symbol with a bubble before its triangle, and the arrow measured between falling edges instead, tag "rare".
> {freq}: under the wave, MathTex `f_c = 1/T_c` (f_c YELLOW), "unit: hertz (Hz)". {ghz}: a small chip icon tagged "several GHz", and "1 GHz ↔ T_c = 1 ns" (numbers GOLD).
> {work}: p. 103's last bullet, verbatim, along the bottom: "All things being equal, increasing the clock frequency increases the 'work' that a digital system can accomplish per unit time". A GOLD dot drops under each rising edge (one step each); the wave compresses sideways and more dots drop. {linkfast}: a small copy of s6's link with its "N×" tag.
> {energy}: a GOLD energy meter beside the wave climbs as the wave compresses, labelled "energy per second". {switch}: callback, small: ch1 s7's spare gate on the 74HC00 flickering RED, with its line "power goes with how often it switches".
> {battery}: two devices under the wave: a small sensor node with a coin-cell battery and a slow YELLOW wave beside it; {laptop}: a laptop with a big battery and a mains plug, and a fast wave.
> {limit}: the laptop's wave keeps compressing, then stops against a YELLOW "?"; {ff}: a small D flip-flop symbol appears by the "?", tag "a limit set by the flip-flops". It leads into s8's flip-flop diagram.

[c2.timing.1] {wave} So how fast should the clock signal tick? {period} The clock period is the time between rising edges. {falling} In a circuit triggered on falling edges, it's between falling edges, but that's rare. {freq} The clock frequency is one over the period, measured in hertz. {ghz} Processors run at several gigahertz, and one gigahertz means a period of one nanosecond.

[c2.timing.2] {work} All things being equal, a faster clock signal gets more work done per second, because every edge is one more step. {linkfast} And a serial link needs a fast clock signal too. {energy} But here's the catch. The faster you run see-moss logic, the more energy it uses each second, {switch} because its power goes with how often it switches. We met that in part one, with the floating inputs.

[c2.timing.3] {battery} So a sensor node on a small battery ticks slowly, {laptop} while a laptop with a big battery, or on mains power, can run much faster. {limit} But even with unlimited power, there's a limit, {ff} and it starts with the flip-flops themselves.

## Scene 8 · A flip-flop's three numbers; recap and next (ch2_s8_recap)

> p. 104's first diagram, as a preview, in L8's `WindowDiagram` (../l08-timing-metastability/scenes/ch1_s3_ffnumbers.py), in its square style: rows "CLK" (YELLOW), "D" (BLUE), "Q" (GREEN), one rising edge at centre with a thin guide down all rows. {window}: CLK and D drawn. {setup}: a GOLD arrow from D's change to the guide, "t_su  Set-up time". {hold}: a GOLD arrow from the guide to D's next change, "t_h  Hold time" (the slide's labels; L8 writes t_hold). {q}: Q drawn rising later, a PINK arrow from the guide, "t_pc  CLK-to-Q Propagation delay" (verbatim from p. 104).
> {bad}: the GOLD band shades between the two arrows; a RED dashed change of D appears inside it, and a RED "???" on Q after the edge. {names}: a small tag "Lecture 8". No numbers, no explanation.
> {recap}: the diagram clears to six slots, filled one per sentence, each a small copy of its scene's visual in the same colours and styling, with the sentence's short line under it; earlier slots dim slightly as each new one arrives.
> {r1}: s2's chain on its YELLOW CLK line, a GOLD "1" hopping one box; "one place per edge". {r2}: s3's Q_0, Q_1, Q_2 rows, the same waveform stepped one period right each time; "same waveform, one period later". {r3}: s4's four LEDs, the lit one walking; "serial in, parallel out". {r4}: s5's chain with its RED PRE and CLR pins, 1 1 0 loaded and the queue at Q_2; "parallel in, serial out".
> {r5}: s6's link with 1 1 0 arriving in the receiver; "one data wire, bits N× faster". {r6}: s7's `f_c = 1/T_c` beside the sensor node's battery; "faster clock: more work, more energy".
> {next}: the slots clear; a YELLOW clock wave compresses against a YELLOW "?", with "What sets the fastest clock speed?" and "Lecture 8". Hold the end card for about 8 seconds after the last word, with the music carrying it.

[c2.recap.1] {window} The lecture ends with a preview, around one rising edge. {setup} A flip-flop's input must be steady for a set-up time before the edge, {hold} and for a hold time after it. {q} Its output answers a clock-to-output delay later. {bad} If the input changes inside that window, the output becomes unreliable. {names} Next lecture explains all three properly.

[c2.recap.2] {recap} Let's recap. {r1} Chain dee flip-flops on one clock signal, and every bit moves one place per edge. {r2} So each output repeats the one before it, one clock period later. {r3} Bits go in one at a time and come out side by side, serial in, parallel out. {r4} Preset and clear load a whole word at once, and then the bits leave one at a time, parallel in, serial out.

[c2.recap.3] {r5} Together, they make a serial link, with one data wire instead of many, and faster bits. {r6} And a faster clock signal does more work, but uses more energy. {next} Next lecture asks, what sets the fastest clock speed a circuit can use? {pause}
