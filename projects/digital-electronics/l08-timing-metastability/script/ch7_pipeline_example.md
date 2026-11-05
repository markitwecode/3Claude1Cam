# Chapter 7 · Pipelining a circuit

Digital Electronics, Lecture 8 (Timing, Metastability and Parallelism), part 7 of 7. Source: slides `combined_26.pdf` pp. 117 (second slide)–119, with p. 120's title as the next-lecture teaser; recording 00:43:52–00:54:49.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch7_s1_hook)

> Title card: "Timing, Metastability and Parallelism", "Digital Electronics · Lecture 8", "Part 7 · Pipelining a circuit". Lecture conventions as in ch1–ch6: CLK lines and the T_c arrow YELLOW; t_pc PINK, t_pd PURPLE, t_su GOLD; numbers and costs GOLD; violations RED, a satisfied constraint a GREEN tick; ch6's task colours (task 1 BLUE, 2 GREEN, 3 TEAL, 4 FG). Every flip-flop box is L6's `make_ff()`. Every number in this chapter was checked in Python 3.11.9 (standard library); there is no code on screen.
> {last}: ch6 s6's closing picture, small: two blocks of combinational logic with a register between them on a YELLOW CLK line, and ch6's bars (one long period becoming two short ones).
> {circuit}: p. 117's circuit draws itself left to right, centred. It is the working object of s2–s5, always in this layout: "Input" → D flip-flop → its Q forks to CB1 (upper, `t_{pd} = 3.2\text{ ns}`) and CB2 (lower, `t_{pd} = 2.5\text{ ns}`); both outputs enter CB3 (`t_{pd} = 3\text{ ns}`) → CB4 (`t_{pd} = 5.5\text{ ns}`) → D flip-flop → "Output". The CLK line (YELLOW) runs along the bottom to both clock triangles. A small circle "A" on a stalk points up at the wire between CB3 and CB4, with a small DIM tag "the slide's point A" beside it (never spoken: the voice reads "ay" as "eye"; the narration says "between block three and block four"). Block outlines BLUE, the `t_pd` labels PURPLE.
> {fast}: a YELLOW `T_c = ?` above the circuit. {extra}: a dashed ghost flip-flop hovers over the CB3–CB4 wire, with a YELLOW "?". {almost}: beside it a GOLD "× 2 ?", the "?" lingering.

[c7.hook.1] {title} Last time, we saw that registers between blocks of logic split a task into shorter stages, {last} and shorter stages can run with a shorter clock period. {circuit} Now let's try it on a real circuit, with real delays. Here's the one from the slides. A register at the input, four blocks of logic, and a register at the output.

[c7.hook.2] {fast} Two questions. How fast can this circuit run as it stands? {pause} {extra} And if we add just one more register in the middle, what does that buy us? {almost} By the end, you'll have exact numbers for both, and you'll see why one register almost doubles the speed, but not quite.

## Scene 2 · The circuit and its critical path (ch7_s2_circuit)

> s1's circuit at full width (same object). {input}: the input register's clock triangle flashes on a rising edge and its Q output glows; {fork} a small bright pulse leaves Q and splits at the fork into the CB1 and CB2 wires.
> {cb1}, {cb2}, {cb3}, {cb4}: each block lights in turn as it is named, its PURPLE `t_pd` label brightening.
> {spec}: under the circuit, slide p. 118's first line verbatim: "Assume that for each D-type FF, max t_pc = 0.2 ns and min t_su = 0.1 ns." (MathTex subscripts; `t_{pc}` PINK, `t_{su}` GOLD). {same}: a small DIM inset of ch1 s6's budget bar beside it, `0.2 + 4.7 + 0.1 = 5.0 ns`, tagged "part 1".
> {routes}: two pulses leave the fork together, each moving at the speed its delays set: route 1 through CB1, CB3, CB4 and route 2 through CB2, CB3, CB4. {sum1}: a GOLD running sum over route 1, `3.2 + 3 + 5.5 = 11.7 ns`; {sum2}: under route 2, `2.5 + 3 + 5.5 = 11.0 ns`.
> {wait}: freeze at CB3's two inputs, each with a small GOLD time stamp: the CB2 pulse got there at 2.5 ns and sits waiting (DIM); CB3 lights only when the CB1 pulse arrives at 3.2 ns.
> {critical}: route 1 (CB1, CB3, CB4 and their wires) is brightened and thickened, YELLOW label "critical path" above it. {dim}: CB2 and its wires dim (critical-path styling only, no colour role). {why}: a tiny DIM ch1 reminder in the corner, "worst case = longest delays".
> {faster}: (ours, checked) CB2's label ticks 2.5 → 2.0 ns and its route's sum 11.0 → 10.5, while the critical 11.7 stays put; it ticks back. {cb1fast}: CB1's label ticks 3.2 → 2.9 ns and the critical sum 11.7 → 11.4 (GOLD); it ticks back. {until}: CB1's label slides further down and, as it passes 2.5, route 2 brightens and route 1 dims: the critical path has moved. Restore.

[c7.circuit.1] {input} On every edge of the clock, the input register sends a new value into the logic. {fork} Its output splits two ways. {cb1} One branch goes through combinational block one, which takes three point two nanoseconds. {cb2} The other goes through block two, which takes two point five. {cb3} Both feed block three, which takes three nanoseconds, {cb4} and then block four, five point five, on its way to the output register.

[c7.circuit.2] {spec} For the registers, the slide gives a clock-to-output delay of at most zero point two nanoseconds, and a set-up time of zero point one. {same} Those are the same numbers we used in part one.

[c7.circuit.3] {routes} So which route through the logic matters? {pause} {sum1} Through block one, it's three point two, plus three, plus five point five. That's eleven point seven nanoseconds. {sum2} Through block two, it's eleven point zero. {wait} Block three can only finish once both of its inputs have arrived. So block two's early answer is no help. Block three has to wait for block one.

[c7.circuit.4] {critical} The slowest route is called the critical path. Here, it runs through blocks one, three and four. {dim} Block two's route is shorter, so it's off the critical path. {why} As in part one, the worst case uses the longest delays, because the output is only safe once the slowest signal has arrived.

[c7.circuit.5] {faster} So making block two faster would change nothing at all. {cb1fast} Make block one faster, and the whole circuit speeds up, {until} at least until block two's route becomes the slowest one. Then the critical path moves.

## Scene 3 · Without pipelining (ch7_s3_unpiped)

> s2's circuit shrinks to the top third, critical path still bright. {bar}: below it, ch1's budget bar style (one clock period as a horizontal bar). {rule}: ch1's inequality `T_c \ge t_{pc} + t_{pd} + t_{su}` above the bar, each term in its segment's colour.
> The segments come out of the circuit pieces they belong to (TransformFromCopy), on the words: {pink} PINK 0.2 from the input register; {purple} PURPLE 3.2, 3 and 5.5 from CB1, CB3 and CB4 (thin dividers, block names inside); {gold} GOLD 0.1 from the output register. Scale: 12 ns spans most of the frame width; s4 and s5 keep exactly this scale.
> {total}: MathTex built term by term under the bar, `T_c = 0.2 + 3.2 + 3 + 5.5 + 0.1 = 12\text{ ns}`; the YELLOW T_c arrow spans the bar, labelled "12 ns".
> {faster}: a YELLOW period marker nudges left of the bar's end; the GOLD set-up segment pokes past it and turns RED; the marker snaps back to 12 ns (GREEN tick).
> {latency}: on the circuit, a BLUE token (ch6's task 1) leaves the input register on a rising edge, runs the critical path and is captured by the output register on the next edge; GOLD "latency = 1 cycle = 12 ns".
> {throughput}: a GREEN token follows one period later, then a TEAL one: one result per 12 ns; GOLD "throughput = 1/12 ns ≈ 83.3 MHz" (the slide prints 83.34 MHz; 1/12 ns = 83.33 MHz, checked, so show 83.3). {million}: small "≈ 83 million results per second" under it.
> {same}: the GOLD "latency = 12 ns" and the bar's YELLOW "T_c = 12 ns" flash together, joined by a small "=".
> {keep}: the two GOLD numbers, "12 ns" and "83.3 MHz", shrink into the top-left corner and stay there through s4.

[c7.unpiped.1] {bar} So how short can the period be? {rule} It's the rule from part one. The period must be at least the clock-to-output delay, plus the logic's delay, plus the set-up time of the next register. {pink} Along the critical path, that's zero point two, {purple} plus three point two, plus three, plus five point five, {gold} plus zero point one. {total} Twelve nanoseconds. {pause}

[c7.unpiped.2] {faster} Any shorter, and block four's result would reach the output register too late for its set-up time. {latency} A value that leaves the input register on one edge is captured at the output on the next. So the latency is one clock cycle, twelve nanoseconds.

[c7.unpiped.3] {throughput} And a new result comes out every twelve nanoseconds. That's a throughput of one over twelve nanoseconds, about eighty-three point three megahertz, {million} or eighty-three million results a second. {same} With just one stage, the latency and the clock period are the same thing. Pipelining will pull them apart. {keep} So keep both numbers in mind, twelve nanoseconds of latency, and eighty-three megahertz of throughput.

## Scene 4 · One register at A (ch7_s4_cut)

> s2's circuit back at full size (the 12 ns and 83.3 MHz stay in the corner). {insert}: a new D flip-flop drops onto the wire between CB3 and CB4, where the "A" marker was (the marker fades as it lands). {wire}: the YELLOW CLK line grows a branch up to its clock triangle; a rising edge flashes on all three clock triangles at once.
> {stages}: two soft background panels: "stage 1" from the input register to the new one (CB1, CB2, CB3), "stage 2" from the new one to the output register (CB4).
> {hold}: a BLUE dot (ch6's task 1) runs through CB1 and CB3 and waits at the new register's D; on the rising edge it appears at Q and stays lit there, steady, while CB4 works on it; {meanwhile} a GREEN dot leaves the input register into CB1 at that same edge.
> {s1path}: in stage 1, CB1 and CB3 brighten and thicken (critical-path styling), CB2 dims. {s1bar}: stage 1's budget bar builds at s3's scale, segments from their sources as in s3: PINK 0.2 | PURPLE 3.2 | PURPLE 3 | GOLD 0.1 (the GOLD from the new register), with `T_c = 0.2 + 3.2 + 3 + 0.1 = 6.5\text{ ns}`. {cb2}: CB2's route flickers, with a DIM `2.5 < 3.2`.
> {s2path}: in stage 2, CB4 brightens. {s2bar}: its bar builds under stage 1's, same left edge and scale: PINK 0.2 (from the new register) | PURPLE 5.5 | GOLD 0.1, with `T_c = 0.2 + 5.5 + 0.1 = 5.8\text{ ns}`.
> {question}: a YELLOW `T_c = 6.5 or 5.8 ?` beside the two bars.
> {try}: the three clock triangles flash together once more; one YELLOW vertical period marker spans both bars, with the YELLOW T_c arrow over them. {short}: the marker at 5.8 ns: stage 2's bar ends exactly on it (GREEN tick). {red}: stage 1's bar overshoots it by 0.7 ns; the overshoot (the end of its PURPLE and all of its GOLD set-up segment) turns RED, label "set-up violated" (ch1's deadline).
> {slide}: the marker slides right to 6.5 ns: stage 1 fits (GREEN tick); stage 2's bar now has a dashed empty 0.7 ns box after it, DIM "idle".
> {slowest}: YELLOW "the slowest stage decides" (ch6 s6's plant), with `T_c = 6.5 ns` in GOLD.

[c7.cut.1] {insert} Now let's pipeline it. We put one more register on the wire between block three and block four. The slide draws it as a single dee flip-flop. {wire} Every edge of the clock reaches it at the same moment as the other two. {stages} That cuts the logic into two stages. Each one is the path from part one, a register, then logic, then a register.

[c7.cut.2] {hold} On every edge, the new register catches stage one's result, and holds it steady for stage two through the whole next period. {meanwhile} Meanwhile, stage one is already working on the next value. So the new value can never catch up with the old one, and corrupt it.

[c7.cut.3] {s1path} In stage one, the critical path runs through block one and block three. {s1bar} So stage one needs zero point two, plus three point two, plus three, plus zero point one. That's six point five nanoseconds. {cb2} Block two's route is still the shorter one, so again it's off the critical path.

[c7.cut.4] {s2path} Stage two is block four on its own. {s2bar} The new register's clock-to-output delay, zero point two, plus five point five, plus zero point one. Five point eight nanoseconds. {question} So what's the clock period now, six point five, or five point eight? {pause}

[c7.cut.5] {try} Every edge of the clock reaches both stages at once, so they must share one period. {short} Try five point eight. Stage two just fits. {red} But stage one's result would settle zero point seven nanoseconds after its set-up deadline. That breaks the rule from part one. {slide} So the period has to stretch to six point five, and stage two gets more time than it needs. {slowest} The slowest stage decides.

## Scene 5 · Nearly double (ch7_s5_payoff)

> {blue}: the pipelined circuit (s4's, with its two stage panels). A BLUE token (ch6's task 1) leaves the input register on a rising edge, waits at the new register for the next edge, and leaves through the output register on the edge after; GOLD "latency = 2 × 6.5 = 13 ns". {green}: as BLUE crosses into stage 2, a GREEN token enters stage 1 behind it (then TEAL, then FG): both stages busy at once. {throughput}: one token leaves every 6.5 ns; GOLD "throughput = 1/6.5 ns ≈ 153.85 MHz".
> {compare}: the circuit shrinks away; a comparison table, numbers GOLD. Columns "no pipeline" | "two stages"; rows "clock period" 12 ns | 6.5 ns, "latency" 12 ns | 13 ns, "throughput" 83.3 MHz | 153.85 MHz. {times}: GREEN "× 1.85" on the throughput row, small DIM "+ 1 ns" on the latency row. Under the table, slide p. 118's line verbatim: "It can be seen that the 2-stage pipeline has almost doubled the throughput (clock frequency), with only a small increase in latency."
> {why}: the table shrinks; s3's 12 ns bar returns with s4's two stage bars under it, same scale. Slide p. 119's line verbatim at the top: "Note the throughput is not exactly doubled since the pipeline stages are not equal and a penalty is also incurred owing to the additional D-type FF." {half}: a YELLOW dashed line at 6 ns, "half of 12 ns".
> {unequal}: stage 2's dashed 0.7 ns idle box (from s4) flashes, "stage 2 idles 0.7 ns every cycle". {overhead}: the new register's two segments flash, stage 2's PINK 0.2 and stage 1's GOLD 0.1: "+ 0.3 ns: the extra register". {sum}: GOLD `6.5 + 5.8 = 12.3 = 12 + 0.3`.
> {balanced}: (ours, checked) the two bars morph into equal bars, `0.2 + 5.85 + 0.1 = 6.15 ns` each, both still ending past the dashed 6 ns line; GOLD "6.15 ns, 162.6 MHz". {balance}: GREEN "≈ × 1.95" beside them, caption "cut where the stages come out equal".
> {three}: (ours, checked) back to the circuit: two more flip-flops, one on each wire into CB3 (CB1's output and CB2's output), on the same CLK line: three stages. Three bars at the same scale: 3.5 (`0.2 + 3.2 + 0.1`), 3.3 (`0.2 + 3 + 0.1`), 5.8 (`0.2 + 5.5 + 0.1`). {pace}: the period marker lands at 5.8 ns; CB4's bar outlined YELLOW, "CB4 sets the pace"; GOLD "5.8 ns, 172.4 MHz". {longer}: GOLD "latency = 3 × 5.8 = 17.4 ns", the 17.4 tinted RED. {lesson}: caption under the three bars, "each new stage: + 0.3 ns, + 1 cycle of latency".

[c7.payoff.1] So what did one register buy? {blue} A value now takes two clock cycles to get through, one per stage. So the latency is two times six point five, thirteen nanoseconds. {green} But while it's in stage two, the next value is already in stage one. {throughput} So a result comes out every six point five nanoseconds. That's a throughput of one hundred and fifty-three point eight five megahertz.

[c7.payoff.2] {compare} Side by side, the latency went from twelve nanoseconds to thirteen. As last time warned, in a real circuit the latency grows a little. {times} But the throughput is one point eight five times what it was. {pause} Almost double, for the price of one register.

[c7.payoff.3] {why} So why not exactly double? {pause} {half} That would need a period of six nanoseconds, half of twelve. {unequal} First, the stages are unequal. Stage two finishes in five point eight, then sits idle for zero point seven nanoseconds, every cycle. {overhead} Second, the new register costs time of its own, its clock-to-output delay and its set-up time. Together, they add zero point three nanoseconds. {sum} The two stages add up to twelve point three, not twelve.

[c7.payoff.4] {balanced} So even a perfect split stays above six. If we could cut the logic exactly in half, each stage would still need six point one five nanoseconds. {balance} That's still about one point nine five times the throughput. So a designer tries to cut where the stages come out equal.

[c7.payoff.5] {three} What about cutting again? Put registers on both wires into block three, and you get three stages, of three point five, three point three and five point eight. {pace} Now block four alone sets the pace. The period only drops to five point eight nanoseconds, about one hundred and seventy-two megahertz, {longer} while the latency grows to seventeen point four. {lesson} So more registers are not automatically better. Each new stage adds a register's delay, and another cycle of latency.

## Scene 6 · When pipelining can't help (ch7_s6_limits)

> {stair}: ch6 s5's staircase returns at the same size and style (A₁ B₁ … boxes, one row per task, task colours BLUE, GREEN, TEAL, FG, YELLOW T_c arrows along the top): A1; B1 + A2; B2 + A3; B3 + A4. {within}: a GREEN arrow from A1 to B1, "earlier step of the same task".
> {depend}: slide p. 119's sentence verbatim at the top: "If a current task is dependent on the result of a prior task, rather than just prior steps in the current task, the task cannot start until the prior task has completed." A YELLOW arrow from B1's right end to A2's left end, "task 2 needs task 1's result".
> {wait}: A2, and every box after it, slides right by one period, so A2 starts where B1 ends. {stall}: the slot A2 left behind gets a dashed RED outline, labelled "stall".
> {cpu}: (ours) the first two rows relabel as instructions: task 1's boxes "add" (BLUE), task 2's boxes "use the sum" (GREEN); the YELLOW dependency arrow stays between them.
> {every}: (ours, checked) every task now waits for the one before: the staircase straightens into ch6 s4's one-at-a-time row, A1 B1 A2 B2 A3 B3, each box 6.5 ns; GOLD "one task per 2 × 6.5 = 13 ns". {worse}: beside it, s3's GOLD "12 ns" from the circuit without pipelining; the 13 tints RED.
> {measures}: a small DIM tag under the row, "processors: special measures".
> {still}: the staircase flows again, full. {cores}: a chip outline with four cores, each holding a tiny staircase. {spatial}: the four cores flash together, label "spatial: several cores"; {temporal}: one core's staircase flashes, label "temporal: each core pipelined" (ch6 s3's two words).

[c7.limits.1] {stair} Now, pipelining is powerful, but it has a limit. {within} Each task's second stage needs the result of its own first stage. That's fine. The pipeline is designed for that. {depend} But suppose task two needs the result of task one, the finished result. {pause} {wait} Then task two must wait until task one has completed. {stall} The pipeline has to wait, leaving an empty slot. This is called a pipeline stall.

[c7.limits.2] {cpu} In a processor, the tasks are instructions. If one instruction adds two numbers, and the very next one needs that sum, the second one has to wait. {every} If every task needed the one before it, our circuit would finish just one task every two cycles, thirteen nanoseconds. {worse} That's slower than the twelve we had with no pipeline at all. {measures} So processors need special measures to deal with stalls.

[c7.limits.3] {still} Even so, pipelining is one of the most important techniques in high-performance processors. {cores} And modern chips use both kinds of parallelism. {spatial} Several cores side by side, that's spatial. {temporal} And inside each core, a pipeline. That's temporal.

## Scene 7 · Recap, the lecture, and next (ch7_s7_recap)

> The screen clears to six slots (two rows of three), filled one per sentence, each a small copy of its scene's visual (same objects, colours and styling) with that sentence's short line under it:
> {r1} s2's circuit, critical path bright, CB2 dim: "the slowest route sets the period"; {r2} s3's 12 ns budget bar (PINK | PURPLE × 3 | GOLD) with its YELLOW T_c arrow: "12 ns, 83.3 MHz"; {r3} s4's two stage bars, 6.5 and 5.8, with the period marker at 6.5 and the dashed idle box: "the slowest stage decides".
> {r4} s5's comparison table with its GREEN "× 1.85": "throughput × 1.85, latency + 1 ns"; {short}: back in slot 3, the idle box and the new register's PINK and GOLD segments flash: "unequal stages, + 0.3 ns"; {r5} s5's three bars, 3.5, 3.3 and 5.8, CB4's outlined YELLOW: "cutting again helps less"; {r6} s6's staircase with its dashed RED stall: "dependencies stall the pipeline".
> {lecture}: the slots shrink to a row along the top; the lecture in one line as three chips, each with a tiny icon from its chapter, lit in turn: {time} ch1 s3's GOLD window round a rising edge, "flip-flops need time: set-up, hold, skew"; {sync} ch4 s5's synchroniser (two flip-flops in a row) with ch5 s5's GOLD "3.04 ns → 1.05 years", "outside inputs need synchronisers"; {stages} ch6 s6's register between two blocks, "registers between stages buy throughput".
> {next}: p. 120's title slide text: "Digital Electronics: Sequential Logic" / "Synchronous State Machines 1". {counters}: L6's `sync_counter()` small beneath it, LEDs counting, with p. 120's words "(of which counters are a subset)". {types}: two blank machine outlines side by side, each with a "?".
> End card after the last word, held ~8 s; the music carries it.

[c7.recap.1] {recap} Let's recap. {r1} The critical path, the slowest route through the logic, sets the shortest clock period. {r2} Without pipelining, our circuit needed twelve nanoseconds, about eighty-three megahertz. {r3} One register split it into two stages, and the slower stage, six point five nanoseconds, set the period for both.

[c7.recap.2] {r4} The throughput nearly doubled, while the latency grew by one nanosecond. {short} It fell short of double, because the stages were unequal, and the new register costs time of its own. {r5} Cutting again helped less, once block four alone set the pace. {r6} And when a task needs the result of the one before, the pipeline has to stall. {pause}

[c7.recap.3] {lecture} That's the whole lecture in one line. {time} Flip-flops need time, a set-up time before each edge, a hold time after it, and room for clock skew. {sync} Inputs from the outside world need synchronisers, and a little extra time buys years between failures. {stages} And registers between stages buy throughput, as long as the tasks are independent.

[c7.recap.4] {next} Next lecture, synchronous state machines. {counters} The counters from lecture six turn out to be one special case. {types} We'll start with a few basic terms, and then meet two popular kinds of machine.
