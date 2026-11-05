# Chapter 1 · How fast can the clock tick?

Digital Electronics · Lecture 8 (Timing, Metastability and Parallelism), part 1 of 7. Source: Digital Electronics slides (combined_26.pdf), p. 103 (System Timing, Lecture 7's slide, as a refresher) and pp. 104–105; lecture recording 00:03:34–00:11:17.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Spoken names: "dee" is D, "cue" is Q, "cue zero" is Q0, "dee one" is D1, "dee two" is D2, "not cue" is Q̄, "flip-flop zero" is FF0. On screen the slides' symbols, spoken as words: T_c "the clock period", f_c "the clock frequency", t_su "the set-up time", t_hold "the hold time" (the slide's t_h), t_pc "the clock-to-cue delay", t_pd "the logic's delay". No code on screen. Every number, inequality and the hook's wrong count sequence were checked in Python 3.11.9 (standard library). Colours (PLAN.md): CLK and T_c YELLOW; Q, Q0 GREEN; D, D0, D1 BLUE; t_pc PINK; t_pd PURPLE; t_su, t_hold and the "keep D still" window GOLD; violations and wrong counts RED, a met constraint a GREEN tick.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card on {title}: "Timing, Metastability and Parallelism", "Digital Electronics · Lecture 8", "Part 1 · How fast can the clock tick?"; it clears on {counter}.
> {counter}: L6 ch6 s6's synchronous counter returns as it was built there (`sync_counter()` and `led_chain` from ../l06-flip-flops-counters/scenes/ch6_s6_circuit.py): FF0, FF1, FF2 on one YELLOW CLK line, Q0–Q2 GREEN, the three LEDs, the readout above (Q2 Q1 Q0 in binary, the decimal in GOLD). A small YELLOW frequency tag on the clock source reads "1 Hz". {together}: a rising edge runs along CLK and all three flip-flops update at once. {count}: the readout steps 0, 1, 2, 3 with the spoken numbers.
> {faster}: the frequency tag steps to "1 kHz", then "1 MHz"; the readout flickers faster, and a short trail of past values beside it shows every value is one more than the last (all GOLD).
> {wrong}: the tag keeps climbing, its digits blurring upwards (no figure is shown for where it breaks: that depends on the chips). {wrong2}: the trail now reads 0, 1, 2, 3, then 0, 5, 2, 7, and those last four values turn RED with the readout's decimal; the gates feeding D2 flicker. {same}: the circuit stays exactly as drawn; only the frequency tag pulses.
> Checked (Python 3.11.9, a simplified model, ours): with L6's logic (D0 = Q̄0, D1 = Q0 ⊕ Q1, and the gate block for D2) the counter steps 0 → 7 → 0. If only D2's logic, the deepest and so the slowest, settles one period late, FF2 loads a stale bit while FF0 and FF1 load correct ones, and the readout cycles 0, 1, 2, 3, 0, 5, 2, 7. Each RED value is not one more than the value before it (7 → 0 is a correct step).
> {question}: the counter dims; a YELLOW "?" over its CLK line, with the line "What sets the fastest clock?".
> {road}: three chips in a row, the lecture's road: {timing} "timing rules", {meta} "metastability", {parallel} "parallelism" (on screen without the hyphen), each lighting as it's named. {start}: the first chip stays lit, the others dim, and "Part 1 · the set-up rule" appears under it.

[c1.hook.1] {title} Welcome to lecture eight of Digital Electronics, on timing, meta-stability and parallelism. {counter} Back in lecture six, we designed this synchronous counter. {together} All three flip-flops change on the same edge of the clock, {count} and the lights count up, zero, one, two, three.

[c1.hook.2] {faster} Now let's speed the clock signal up. A thousand ticks a second, then a million, and the count is still right. {wrong} But push it further, and something breaks. {wrong2} After three comes zero, then five, then two, then seven. {pause} {same} Nothing in the circuit has changed, except how fast the clock signal ticks.

[c1.hook.3] {question} So what sets the fastest clock speed a circuit can use? {pause=1.5} {road} This lecture covers three topics. {timing} First, the timing rules that every flip-flop needs. {meta} Then meta-stability, what happens when those rules are broken. {parallel} And finally parallelism, getting more work done per second. {start} This part finds the first rule, and with it, the answer to that question.

## Scene 2 · Period and frequency (ch1_s2_clock)

> {wave}: L6's `clock_wave` (ch1_s1_hook.py), YELLOW, across the upper middle, a small up-arrow on each rising edge.
> {period}: a YELLOW dimension arrow from one rising edge to the next, thin vertical guides at both, label `T_c` and "clock period". {repeat}: copies of the arrow tile along the wave, one per period.
> {freq}: under the wave, MathTex `f_c = \frac{1}{T_c}` (f_c YELLOW), with the label "clock frequency: rising edges per second". {hertz}: "unit: hertz (Hz)" beside it.
> {slow}: a two-row table below: "1 Hz ↔ T_c = 1 s" with a tiny LED icon and the tag "lecture 6's counter". {fast}: "1 GHz ↔ T_c = 1 ns" with a tiny chip icon, and "1 ns = 10⁻⁹ s" under it. Numbers GOLD. {several}: a small "several GHz" tag on the chip. {inverse}: between the two rows, a small pair of arrows, "f_c ↑ ⇔ T_c ↓".
> {work}: p. 103's last bullet, verbatim, as a line along the bottom: "All things being equal, increasing the clock frequency increases the 'work' that a digital system can accomplish per unit time". {step}: under the wave, one small GOLD dot drops from each rising edge (one step each); the wave compresses sideways (more edges in the same width) and more dots drop.
> {limit}: the compression stops. One period is highlighted, and inside it a grey box, "the circuit's work for one step", that only just fits. {measure}: a YELLOW "?" on the T_c arrow, "how short can T_c be?".

[c1.clock.1] {wave} First, two ways to say how fast a clock signal ticks. {period} The clock period is the time from one rising edge to the next. {repeat} It's the same every cycle. {freq} The clock frequency is one over the period, the number of rising edges per second. {hertz} It's measured in hertz.

[c1.clock.2] {slow} Lecture six's counter ran at one hertz, so its period was one second. {fast} A processor running at one gigahertz ticks a billion times a second, so its period is one nanosecond, a billionth of a second. {several} Modern processors run at several gigahertz. {inverse} The higher the frequency, the shorter the period.

[c1.clock.3] {work} All things being equal, a faster clock signal gets more work done per second, {step} because a synchronous circuit takes one step on every rising edge. {limit} So why not tick as fast as we like? {pause} Because every period has to leave the circuit enough time to finish its step. {measure} This lecture measures exactly how much time that is.

## Scene 3 · A flip-flop's three numbers (ch1_s3_ffnumbers)

> p. 104's first diagram, large, in L6's square timing style (vertical edges, as this slide draws it; the data-sheet style arrives in s5): rows CLK (YELLOW), D (BLUE), Q (GREEN), labels at left, one rising edge at centre with a thin vertical guide down all rows.
> {edge}: CLK drawn, its rising edge marked with a small up-arrow. {setup}: D drawn, rising a little before the edge; a GOLD dimension arrow from D's rise to the guide, "t_su", with "set-up time". {hold}: D falls a little after the edge; a GOLD arrow from the guide to D's fall, "t_hold", with "hold time" and a small DIM note "(slide: t_h)". We write t_hold from here on.
> {window}: a GOLD shaded band over the D row, from t_su before the edge to t_hold after it, labelled "keep D still". {q}: Q drawn, rising later; a PINK arrow from the guide to Q's rise, "t_pc", with "clock-to-Q delay". {follows}: a small BLUE "1" on D at the guide, and a GREEN "1" on Q after its rise. {datasheet}: a small data-sheet card slides in at top right, headed "Timing characteristics", listing t_su, t_hold and t_pc, each with "… ns".
> {why}: the diagram shrinks to the left. At right, L6's master-slave pair (`master_slave_end_shot` from ../l06-flip-flops-counters/scenes/ch2_s3_masterslave.py) with its two door icons, master open and slave shut, and a BLUE dot (D's value) on the D wire. {shut}: a small CLK trace under the pair rises; the master's door swings shut with the dot just inside it, and the t_su arrow on the small diagram flashes. {still}: the door's swing is drawn slowly, the dot sits still at the doorway, and the t_hold arrow flashes. {slave}: the slave's door opens and the dot travels on through the slave to Q (GREEN), with a PINK "t_pc" tick; the t_pc arrow flashes.
> {caveat}: a small DIM tag under the pair, "simplified: real flip-flops are built differently". {plant}: the pair fades. On the diagram, a RED dashed change of D appears inside the GOLD band, and a RED "???" on Q after the edge, with the tag "Part 4". {job}: the RED change slides out of the band to just before it; Q's "???" clears, and the band gets a GREEN tick. This GOLD window returns in ch2 (hold) and ch4 (violated).

[c1.window.1] {ff} Our circuits are built from flip-flops, so start with just one. It has three timing numbers, and all three sit around the rising edge. {edge} Here's one rising edge, with the input, dee, and the output, cue, below it. {setup} The input must be steady for a short time before the edge. That's the set-up time. {hold} And it must stay steady for a short time after the edge. That's the hold time.

[c1.window.2] {window} Together they make a window around the edge, and inside it, dee must keep still. {q} The output answers a little later. The time from the edge to cue changing is the clock-to-cue delay. {follows} And cue takes the value dee had at the edge. Here, that value is one. {datasheet} You never calculate these three numbers. You read them from the flip-flop's data sheet.

[c1.window.3] {why} Why a window, and not an instant? {pause} Here's a simplified picture, using lecture six's master-slave flip-flop. {shut} At the rising edge, the master latch shuts. Dee's value has to be inside before the door closes. That's the set-up time. {still} Closing takes a moment, so dee must not change while it shuts. That's the hold time. {slave} Then the slave passes the value on to cue, and that takes time too. That's the clock-to-cue delay.

[c1.window.4] {caveat} Real flip-flops are built differently, but they have the same three numbers. {plant} And what if dee does change inside the window? {pause} That's part four's story. {job} For now, our job is to make sure it never happens, anywhere in the circuit.

## Scene 4 · The path between two flip-flops (ch1_s4_path)

> p. 104's second diagram, built left to right across the middle. This is the lecture's running picture, "the path" (reused through ch3, and in ch4 and ch6–ch7). {path} {ffs}: FF0 (L6's `make_ff()` box, from ch2_s6_symbols.py, labelled "FF0") with D0 (BLUE) in and Q0 (GREEN) out; Q0's wire into a box "Combinational Logic (CL)"; its output D1 (BLUE) into FF1, with Q1 (GREEN) out. {clk}: one YELLOW CLK line along the bottom, branching up into both clock triangles. {roles}: small tags "launches" under FF0 and "receives" under FF1.
> {edge}: a bright YELLOW pulse runs along CLK and reaches both triangles at the same moment. {q0}: a beat later, Q0's wire brightens from FF0 into CL, with a PINK "t_pc" tag at FF0's output. {logic}: CL flickers; then D1's wire brightens up to FF1, with a PURPLE "t_pd" tag. {deadline}: a second YELLOW pulse approaches along CLK; before it arrives, a GOLD "t_su" tag on D1, "settled t_su before the next edge".
> {every}: the path slides to the top, smaller. {counter}: the hook's counter (`sync_counter()`) returns small below it. {route}: one route lights, from FF0's Q0 through the gate block for D2 into FF2; everything else dims. {map}: copies of the lit parts fly up onto the path (TransformFromCopy): FF0 onto FF0, D2's gate block onto CL, FF2 onto FF1.
> {self}: in the counter, FF0's own loop lights, Q̄0 wired back to D0: one flip-flop that both launches and receives, tag "FF0 = FF1".

[c1.path.1] {path} Now put two flip-flops in a row, with combinational logic between them. {ffs} Flip-flop zero's output, cue zero, feeds the logic. The logic's output, dee one, is the input of flip-flop one. {clk} Both flip-flops share one clock signal, so they see the same edges at the same moment. {roles} Flip-flop zero launches the data. Flip-flop one receives it.

[c1.path.2] {edge} Follow one rising edge. {q0} After the clock-to-cue delay, cue zero changes. {logic} The logic responds, and after the logic's own delay, dee one changes too. {deadline} Dee one has to settle at least one set-up time before the next edge, so that flip-flop one catches it.

[c1.path.3] {every} The slide calls this a generic path, because every synchronous circuit is built from paths like this one. {counter} Take lecture six's counter. Its flip-flops feed logic, and the logic feeds the same flip-flops. {route} Pick out one route, from flip-flop zero, through the logic that makes dee two, into flip-flop two, {map} and it's exactly our picture. {self} A path can even start and end at the same flip-flop, like flip-flop zero, whose input is its own not cue.

## Scene 5 · Reading a data-sheet timing diagram (ch1_s5_datasheet)

> {sheet}: at left, a small L6-style trace (square, vertical edges), labelled "lecture 6". {datasheet}: at right, a copy of it becomes the data-sheet version, one convention at a time, each with a short label:
> {slope}: the copy's edges tilt, "real edges take time". {either}: a data row appears as two parallel lines, one high and one low, "0 or 1: we don't care which". {when}: a small tag beside it, "when, not what". {cross}: the two lines swap through an X, "the value changes here". {hatch}: a run of several X's in a row, "may change several times". {glitch}: beside it, a small callback of the hazards lecture (pp. 59–62): a gate output with a brief RED glitch spike, and an arrow from it to the run of X's.
> {diagram}: clear. p. 105's first diagram is built large, as the slide draws it: rows CLK (YELLOW), Q0 (GREEN), D1 (BLUE), labels at left. {clk}: CLK with two sloped rising edges and a sloped fall between them. {tc}: thin vertical guides through the middle of each rising edge, down all rows; a YELLOW T_c dimension arrow above, between them.
> {q0}: Q0 as two parallel lines, crossing in an X a little after the first edge; a thin guide through the X; a PINK "t_pc" dimension arrow under the traces, from the first edge's guide to Q0's. {d1}: D1 as two parallel lines; a hatched run of X's starting about halfway along the period, then one last X, then parallel lines to the end (as on the slide).
> {times}: the X's in D1's run light YELLOW one after another.
> The diagram stays exactly as it is for s6. From here on, all of the lecture's timing diagrams use this data-sheet style.

[c1.sheet.1] {sheet} To count the time exactly, we need a more careful timing diagram. {datasheet} Data sheets draw them in a slightly different style from lecture six, and we'll use it from now on. {slope} First, the edges slope, because a real signal takes time to rise or fall.

[c1.sheet.2] {either} Second, a data signal is often drawn as two parallel lines, one high and one low. That means it could be zero or one, and we don't care which. {when} A diagram like this is about when signals change, not which values they carry. {cross} Where the two lines cross over, the value changes. {hatch} And a run of crossings means it may change several times before it settles. {glitch} Those are the glitches from the lecture on hazards, while the logic works out its answer.

[c1.sheet.3] {diagram} Now the path's timing diagram. {clk} At the top, the clock signal, with two rising edges. {tc} The time between them is one clock period. {q0} Cue zero could be zero or one, so it gets two lines, and it crosses over one clock-to-cue delay after the first edge. {d1} Below it, dee one, the logic's output. {times} Each of these crossings is a time when it might change, depending on how slow the logic is.

## Scene 6 · The set-up constraint (ch1_s6_setup)

> s5's diagram stays. {latest}: D1's last X brightens and a thin guide drops from it; a GOLD "t_su" dimension arrow from that guide to the second edge's guide. {earlier}: the earlier X's in the run get small GREEN ticks. {late}: a ghost X inside the t_su span, RED, with a RED cross.
> {sum}: a PURPLE "t_pd" dimension arrow fills in, from Q0's guide to D1's last X. {tpc} {tpd} {tsu}: the PINK t_pc, PURPLE t_pd and GOLD t_su arrows flash in turn, end to end under the traces, exactly spanning the T_c arrow above.
> {bar}: the three arrows lift out (TransformFromCopy) into the budget bar below the diagram: one horizontal bar the length of T_c, YELLOW outline and "T_c" label, three segments PINK "t_pc", PURPLE "t_pd", GOLD "t_su", in the diagram's proportions. This is the lecture's running budget bar (s7, the recap, then ch3, ch4 and ch7). {ineq}: under it, p. 105's equation, MathTex `T_c \ge t_{pc} + t_{pd} + t_{su}`, each term in its segment's colour, T_c YELLOW.
> {worst}: small "max" tags under t_pc and t_pd. {limit}: a GREEN outline round the inequality, "minimum clock period". {short}: a small tag "part 2: the shortest delays" beside the "max" tags.
> {example}: the diagram clears; the bar stays. Under its segments (not to scale): "0.2 ns" and "0.1 ns" under t_pc and t_su, tagged "flip-flops: from the data sheet" and "part 7", and {logic} "4.7 ns" under t_pd, tagged "logic". Numbers GOLD. {add}: `T_c \ge 0.2 + 4.7 + 0.1 = 5.0\ \text{ns}`. {freq}: `f_c \le \frac{1}{5.0\ \text{ns}} = 200\ \text{MHz}`, with a GREEN tick.
> {hook}: the hook's counter returns small at the side, with its RED trail 0, 5, 2, 7. {tooshort}: a second, shorter T_c bar: the three segments no longer fit, and the GOLD t_su segment hangs off its right end, RED. {stale}: in the counter, the D2 wire is still flickering as the next edge arrives; FF2 flashes RED.
> Checked (Python 3.11.9): 0.2 + 4.7 + 0.1 = 5.0 ns; 1 / 5.0 ns = 200 MHz.

[c1.setup.1] {latest} Which of these crossings is the worst case? {pause} The last one. Dee one can settle as late as one set-up time before the next edge, and no later. {earlier} If it settles earlier, that's fine, with time to spare. {late} If it settles any later, flip-flop one's set-up time is broken.

[c1.setup.2] {sum} So follow the worst case along the bottom. {tpc} First the clock-to-cue delay, {tpd} then the logic's delay, {tsu} then the set-up time. In the worst case, together they fill one period exactly. {bar} Stack them into one bar, a budget for the clock period, and the rule is plain. {ineq} The clock period must be at least the clock-to-cue delay, plus the logic's delay, plus the set-up time.

[c1.setup.3] {worst} Worst case means the longest delays, the flip-flop's slowest clock-to-cue delay and the slowest route through the logic. {limit} So this sum is the minimum clock period, the shortest one that always works. {short} The shortest delays get their turn in part two.

[c1.setup.4] {example} Here's an example with real numbers. These flip-flops have a clock-to-cue delay of zero point two nanoseconds, and a set-up time of zero point one nanoseconds. {logic} Say the logic takes four point seven nanoseconds. {add} The sum is five nanoseconds, so the clock period must be at least five nanoseconds. {freq} That's a frequency of at most two hundred megahertz.

[c1.setup.5] {hook} That's what went wrong with our counter. {tooshort} Its clock period got shorter than its slowest path's sum. {stale} So flip-flop two took its input before dee two had settled, and stored a bit that was out of date.

## Scene 7 · Who sets the clock? (ch1_s7_marketing)

> {marketing}: p. 105's second slide, first bullet, verbatim, as a quote card: "Note that the clock period of a system (i.e., the clock speed) is often set by the marketing dept!". {billboard}: beside it, a small billboard reading "1 GHz!" in YELLOW.
> {fixed}: s6's budget bar returns (general form, no numbers). Small padlocks on the PINK t_pc segment, tag "max", and the GOLD t_su segment, tag "min"; the slide's words above, "worst case values of t_pc (i.e., max) and t_su (i.e., min) are specified by the chip manufacturer". {free}: the PURPLE t_pd segment glows, tag "the designer's".
> {rearrange}: `T_c \ge t_{pc} + t_{pd} + t_{su}` rearranges into p. 105's `t_{pd} \le T_c - (t_{pc} + t_{su})`, every term keeping its colour, t_pd moving to the left.
> {target}: the bar resizes to the billboard's period, "T_c = 1 ns". {budget}: now drawn to scale: PINK "0.2" and GOLD "0.1" locked at the ends, and the PURPLE slot between them, "0.7 ns"; `t_{pd} \le 1 - (0.2 + 0.1) = 0.7\ \text{ns}`. Numbers GOLD.
> {compare}: s6's 4.7 ns PURPLE segment, to the same scale, lines up under the slot and runs far past it, RED where it overflows; tag "≈ 6.7 ×".
> {redesign}: two branches. "redesign the logic": the PURPLE segment squeezes but stops short of 0.7. {grow}: "increase T_c": the bar stretches until it holds the 4.7 segment, back to 5.0 ns, and the billboard's "1 GHz!" swaps to "200 MHz". {upset}: the billboard droops, with the slide's words "the clock period has to be increased to ensure correct operation".
> Checked (Python 3.11.9): 1 GHz ↔ 1 ns; 1 − (0.2 + 0.1) = 0.7 ns; 4.7 / 0.7 = 6.71.

[c1.market.1] {marketing} The lecturer makes a slightly cynical point here. The clock period is often set by the marketing department. {billboard} They want a processor they can advertise at so many gigahertz, and that fixes the period.

[c1.market.2] {fixed} The flip-flops' numbers are fixed by the chip maker. The clock-to-cue delay is given as a maximum, the slowest it can be. The set-up time is given as a minimum, the least time dee must be ready before the edge. {free} That leaves the logic's delay, usually the only thing the designer controls. {rearrange} So rearrange the rule. The logic's delay must be at most the clock period, minus the clock-to-cue delay and the set-up time together.

[c1.market.3] {target} Say marketing wants one gigahertz. Then the clock period is one nanosecond. {budget} Take away zero point three nanoseconds for the flip-flops, and the logic gets zero point seven. {compare} Our logic from before took four point seven nanoseconds. It would have to get almost seven times faster.

[c1.market.4] {redesign} The designer can try to make the logic faster, for example with fewer levels of gates. If that can't get there, there's only one option left. {grow} The clock period has to increase, until the circuit works correctly. {upset} And the marketing department is very upset, because it can't advertise that high clock rate anymore.

## Scene 8 · Recap and next (ch1_s8_recap)

> Six small panels fill the frame one per sentence, each a small version of its scene's visual (same objects, colours and styling) with its short line under it.
> {r1}: s2's YELLOW clock wave with the T_c arrow and `f_c = \frac{1}{T_c}`; "frequency = 1 / period".
> {r2}: s3's CLK / D / Q diagram with the GOLD window and the PINK t_pc arrow; "keep D still: t_su before, t_hold after; Q after t_pc".
> {r3}: s4's path, FF0 → CL → FF1 on one YELLOW CLK line; "FF0 launches, FF1 receives".
> {r4}: s5's data-sheet conventions: a sloped edge, two parallel lines, one X, a run of X's; "data-sheet style".
> {r5}: s6's budget bar, PINK t_pc, PURPLE t_pd, GOLD t_su, with `T_c \ge t_{pc} + t_{pd} + t_{su}`.
> {r6}: s7's 1 ns bar with the padlocked ends and the PURPLE 0.7 ns slot, with `t_{pd} \le T_c - (t_{pc} + t_{su})`; {grow}: as in s7, that bar stretches to hold a longer PURPLE segment, "or T_c grows".
> {next}: the panels shrink away. s4's path returns: on one rising edge, FF1's GOLD window sits just after the edge while a new value (BLUE dot) races out of FF0 through CL towards D1. {race}: the dot arrives inside FF1's window, which flashes RED; a YELLOW "?" and, under it, "Part 2 · Hold time".
> End card after the last word, held ~8 s; the music carries it.

[c1.recap.1] {recap} Let's recap. {r1} The clock period is the time between rising edges, and the frequency is one over it. {r2} A flip-flop needs its input still for the set-up time before the edge and the hold time after it, and its output answers after the clock-to-cue delay. {r3} Every synchronous circuit is built from paths, one flip-flop, through logic, to the next.

[c1.recap.2] {r4} Data-sheet diagrams draw sloped edges, both values at once, and crossings where data may change. {r5} The clock period must cover the clock-to-cue delay, the logic's delay and the set-up time. {r6} So when the clock period is fixed, the logic gets whatever time the flip-flops leave. {grow} And if the logic can't fit, the clock period has to grow. {pause}

[c1.recap.3] {next} Next time, the opposite danger, new data that arrives too soon. {race} And why slowing the clock signal down can't help. {pause}
