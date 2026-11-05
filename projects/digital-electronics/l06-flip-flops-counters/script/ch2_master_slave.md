# Chapter 2 · The master-slave D flip-flop

Digital Electronics · Lecture 6 (Flip-flops and Counters), part 2 of 6. Source: Digital Electronics slides (combined_26.pdf), pp. 87–88; lecture recording 00:10:52–00:21:36, demo 00:23:16–00:25:01.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Spoken names: "dee" is D, "cue" is Q, "not cue" is Q̄, "cue-int" is Q_int, "not clock" is CLK̄,
"enable" is EN. No code on screen. Every waveform, table and demo step in the briefs was checked by
simulation in Python 3.11.9 (standard library): an ideal master-slave model for slide p. 88 and the
demo, and a unit-delay gate model of p. 86's D latch and p. 87's flip-flop for the oscillation.

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card on {title}: "Flip-flops and Counters", "Digital Electronics · Lecture 6", "Part 2 · The master-slave D flip-flop"; it clears on {latch}.
> {latch}: ch1 s6's latch symbol returns at left as ch1 left it: a tall box, D on the left, Q on the right, EN coming in from below with the small square. D and EN wires BLUE, Q GREEN. Beside it, ch1 s6's EN / D / Q timing diagram with its pale band over the EN-high stretch.
> {follows}: the band brightens, and Q (GREEN) is seen copying each change of D (BLUE) inside it. {holds}: outside the band, Q is flat while D still changes.
> {clock}: a YELLOW "CLK" wire slides into the EN input (the EN label stays). The waveform clears to two stacked copies of one CLK square wave (YELLOW).
> {window}: on the top copy, every high level fills with a faint YELLOW band (ch1's band, repeated each cycle), label "listens: a window". {instant}: the bottom copy dims to a thin line; {edge}: each of its rising edges gets a small up-arrow and a bright dot, label "listens: an instant".
> {question}: a YELLOW "?" beside the bottom copy. {answer}: two copies of the latch box slide out of the one at left and settle side by side, under the line "master-slave D flip-flop" (they become s3's circuit).

[c2.hook.1] {title} Last time, we built the transparent dee latch. {latch} It has an input, dee, an output, cue, and an enable input. {follows} While enable is one, cue follows dee, and copies every change. {holds} When enable drops to zero, cue holds whatever it had.

[c2.hook.2] {clock} Now put the clock on enable. {window} The latch listens to its input for the whole time the clock is high. That's a window, half of every cycle. {instant} But usually, we want it to listen at one instant, {edge} the moment the clock rises, and to ignore its input the rest of the time. {question} Can we build a memory that listens only at the edge? {pause} {answer} We can, with two of these latches, back to back. It's called the master-slave flip-flop.

## Scene 2 · Why a window is a problem (ch2_s2_window)

> Top third, p. 87's first bullet as two short lines: "D latch: level-triggered, transparent while EN = 1" ({level}) and "simpler: outputs change only on clock edges" ({simpler}). Beside the second line, small CLK traces (YELLOW): {rising} one with up-arrows on its rising edges, {falling} one with down-arrows on its falling edges. {why}: on a third small trace, a shaded high level with a few RED sparks at scattered moments inside it. {instant}: the up-arrow trace brightens.
> {example}: clear. ch1's D latch symbol at centre-left, now with a Q̄ (overbar) output under Q, as the lecture's boxes carry D, Q and Q̄ from here on. {wire}: a GREEN wire leaves Q̄, loops over the top of the box and comes down into D (the D stub stays BLUE). {clock}: a YELLOW "CLK" wire into EN. {want}: caption "goal: flip once per clock cycle". {ask}: a "?" on the output.
> Under the circuit, a two-row timing diagram in the lecture style (clock on top, labels "CLK" and "Q"): CLK with its high levels shaded faintly YELLOW, as in s1.
> In the first shaded window: {open} D's level copies Q̄; {flip} Q flips once; {back} a dot runs round the feedback loop on the circuit; {again} Q flips again; {fast} Q becomes a fast, regular buzz, drawn RED, filling the whole window, label "as fast as the gates allow". {buzz} The next windows fill with the same RED buzz.
> {stop}: at each falling edge the buzz stops and Q goes flat, at a different level each time (high after one window, low after the next, high after the third), each frozen level tagged with a small RED "?". {depends}: the shaded windows flash, then the gate symbols inside the latch flash.
> {wanted}: a third row, "Q wanted", GREEN and clean: one flip at each rising edge, with up-arrows and thin guide lines on the rising edges; small digits "0 1 0 1" over its levels.
> {remember}: the circuit gets a soft YELLOW outline. {later}: a small tag beside it, "part 6: the heart of a counter".
> Checked (unit-delay gate model of p. 86's latch, Q̄ wired to D): while EN = 1, Q oscillates with a period of 5 gate delays; with EN high for 18 to 29 gate delays it flips 6 to 10 times and ends at 0 or 1 depending on the width. (Some widths leave the model racing forever, its stand-in for metastability, which is next lecture's: don't draw that.) The edge-triggered version flips exactly once per rising edge.

[c2.window.1] {level} The dee latch is called level-triggered, because it keeps responding while enable is one. {simpler} But sequential circuits are often simpler to design if their outputs change only on the clock's edges, {rising} the rising edge, {falling} or the falling edge. {why} Inside a window, an output can change at any moment, and one change can even set off another. {instant} At an edge, everything happens at one precise instant.

[c2.window.2] {example} Here's an example of what can go wrong. {wire} Take a dee latch, and connect its not cue output back to its dee input. {clock} Put the clock on enable. {want} The idea is a circuit that flips once every clock cycle. {ask} So what does it actually do while the clock is high? {pause}

[c2.window.3] {open} With the clock high, the latch is transparent, so cue copies dee, which is not cue. {flip} So cue flips. {back} The new not cue travels back round to dee, {again} and cue flips again, {fast} and again, as fast as the gates allow. {buzz} For the whole window, the output oscillates. {stop} When the clock falls, it freezes wherever it happens to be. {depends} That depends on how long the clock was high, and on how fast the gates are.

[c2.window.4] {wanted} What we wanted was one clean flip at each rising edge. Zero, one, zero, one. {remember} So keep this circuit in mind. {later} Once it listens only at the edge, it becomes the heart of a counter, in part six.

## Scene 3 · Two latches, back to back (ch2_s3_masterslave)

> Slide p. 87's circuit, built left to right across the upper two-thirds. {two}: the two latch boxes from s1's answer move into place. {master}: the left box gets the label "Master" above it, and D (BLUE) wires into its D input. {qint}: a TEAL wire from the master's Q to the slave's D, labelled "Q_int" (Q with subscript int). {slave}: the right box gets "Slave". {q}: a GREEN wire from the slave's Q out to the label "Q". {names}: a small TEAL arrow along Q_int, master → slave. Both boxes keep ch1's small square on the enable input, on the bottom edge.
> {clk}: a YELLOW "CLK" wire enters at the bottom left. {inv1}: it passes an inverter (triangle with bubble), whose output rises into the master's enable; label that wire "CLK̄" (overbar). {inv2}: from the same node, a second inverter, whose output rises into the slave's enable. {double}: the two bubbles flash in turn, and a small line appears under the second inverter, "not not CLK = CLK"; label the slave's enable wire "CLK". {both}: both enable wires glow YELLOW together.
> {never}: CLK set low (dim wire, CLK̄ bright). {low}: the master's outline brightens, tag "transparent", and D's level flows on into Q_int; the slave dims, tag "hold", Q flat. {high}: CLK set high (bright); swap: master "hold", slave "transparent".
> {airlock}: two door icons above the boxes, one open and one shut; they swap once as CLK toggles. Caption: "never both open". {race}: a DIM ghost of both doors open at once, with a BLUE dot racing straight from D to Q, then crossed out in RED.
> {path}: the doors return to the real state, and a BLUE dot travels from D toward Q, stopping at whichever door is shut. {ask}: a YELLOW "?" over the pair. {trace}: the circuit shrinks to the top of the frame, as on slide p. 88, leaving room for s4's diagram below.

[c2.pair.1] {two} The fix uses two dee latches, one after the other. {master} The first is called the master. It takes the input, dee. {qint} Its output is an internal signal, called cue-int, {slave} and that's the input to the second latch, the slave. {q} The slave's output is the output of the whole circuit, cue. {names} The names tell you who's in charge. The slave only ever copies what the master gives it.

[c2.pair.2] {clk} Now the clock. {inv1} It goes through an inverter to the master's enable, so the master sees not clock. {inv2} A second inverter feeds the slave. {double} Two complements cancel out, so the slave sees the original clock. {both} So both latches are driven by the same clock, one of them complemented.

[c2.pair.3] {never} That means the two latches are never transparent at the same time. {low} While the clock is low, the master is open, following dee, and the slave is shut, holding cue. {high} While the clock is high, it's the other way round. The master is shut, and the slave is open. {airlock} Think of an airlock, with two doors that are never both open. {race} If both were open at once, a change at dee would rush straight through to cue, just as it did in a single latch.

[c2.pair.4] {path} So a change at dee has to get through both doors to reach cue. {ask} When can it make it all the way? {pause} {trace} To find out, we'll draw a timing diagram, one signal at a time.

## Scene 4 · Timing diagram, part 1: the master (ch2_s4_master)

> Layout as slide p. 88: s3's circuit small at the top; below, a timing diagram with five rows, labels at left: "CLK", "CLK̄" (overbar), "D", "Q_int", "Q". CLK and CLK̄ YELLOW, D BLUE, Q_int TEAL, Q GREEN (its row stays empty until s5). To the right, the slide's note in small text on {neglect}: "Note propagation delays have been neglected in the timing diagram".
> Geometry (from p. 88, checked): CLK starts high for a little under half a period, falls (f1), and then runs regularly. Its rising edges r1 to r4 get small up-arrows and thin vertical guide lines down all five rows; a fifth rising edge r5, at the right end, gets an arrow only. Falling edges f2 to f5 sit midway between the rising edges.
> {clk}: draw CLK left to right. {notclk}: CLK̄ is born from a copy of CLK, flipped upside down into the row below. {edges}: the arrows and guide lines drop in, r1 to r4.
> {d}: D drawn low. {rise}: D steps up halfway through the high stretch after r1 (between r1 and f2); {fall}: D steps down just after r3 (between r3 and f4). At each step a small YELLOW tag "CLK high"; {note}: both tags flash.
> {qint}: the Q_int label lights TEAL. {rule}: the CLK̄-high stretches flash. {shade}: on the Q_int row, the stretches where CLK̄ = 1 shade faintly TEAL, tag "master open". {unknown}: Q_int drawn at both levels at once up to f1 (slide style). {copy}: at f1 it settles to 0, with a small TEAL arrow from D's level.
> {hold1}: flat through r1. {drise}: as D steps up, a small shut-door icon on the master; Q_int stays at 0. {catch}: at f2 Q_int rises to 1, with a TEAL arrow from D's step across to f2 (the catch-up). {stay}: flat at 1 through f3 and two guide lines. {dfall}: the shut-door icon again as D steps down. {catch2}: at f4 Q_int falls to 0, and stays.
> {pattern}: caption under the diagram, "Q_int follows D while CLK is low, and freezes while CLK is high".
> Checked (ideal master-slave model, Python 3.11.9): Q_int is unknown until f1, then 0; 1 from f2; 0 from f4. D's two changes both happen while CLK = 1.

[c2.master.1] {clocks} When you draw a timing diagram, start with the clocks, because they drive everything. {clk} Here's the clock, {notclk} and under it, not clock, its complement. {edges} Each rising edge of the clock gets a small arrow, and a thin guide line down the page. {neglect} We'll ignore propagation delays, so every change happens instantly.

[c2.master.2] {d} Next, the input, dee. It starts at zero. {rise} Just after the first rising edge, while the clock is high, it rises to one. {fall} Then just after the third rising edge, again while the clock is high, it falls back to zero. {note} Both of its changes happen while the clock is high, and that will matter.

[c2.master.3] {qint} Now the master's output, cue-int. {rule} The master's enable is not clock, so it's transparent while the clock is low, and holds while the clock is high. {shade} We'll shade the stretches where it's open. {unknown} At the start, the clock is high, so the master is holding an unknown value. {both} We draw it at both levels at once. {copy} Then the clock falls. The master opens, and copies dee, which is zero.

[c2.master.4] {hold1} The clock rises, and the master shuts, holding that zero. {drise} Now dee rises to one. But the master is shut, so cue-int ignores it. {pause} {catch} Only when the clock falls, and the master opens again, does cue-int catch up to one. {stay} It stays at one for two whole cycles. {dfall} Then dee falls, again while the master is shut, {catch2} so cue-int follows it down at the next falling edge. {pattern} So cue-int follows dee while the clock is low, and freezes while the clock is high. {pause}

## Scene 5 · Timing diagram, part 2: the slave (ch2_s5_slave)

> Same diagram, continued from s4. {slave}: the Slave box at the top highlights. {rule}: Q_int's TEAL shading dims; on the Q row, the stretches where CLK = 1 shade faintly GREEN, tag "slave open".
> {start} / {unknown}: Q drawn at both levels at once, up to r1.
> {e1}: at r1, a TEAL arrow from Q_int's level down to the Q row; Q settles to 0. {low1}: flat. {e2}: at r2, Q steps up to 1. {e3}: at r3, Q stays at 1 (a small "=" on the guide line). {e4}: at r4, Q steps down to 0. Every Q step lands exactly on its guide line.
> {flat}: on each CLK-high stretch, the Q_int segment glows TEAL with a small shut-door icon on the master, and the Q segment beside it is the same flat value. {cycle}: Q's four steps flash YELLOW, all on guide lines.
> {read}: the four guide lines brighten in turn. {d_at}: D's value just left of each line pops up in BLUE, "0 1 1 0". {q_at}: Q's value just right of each line pops up in GREEN, "0 1 1 0"; the two rows line up. {words}: beside the circuit, the slide's words: "See Q changes on rising edge of CLK".
> {blip} (ours, not on the slide): two short DIM dashed blips are added on D after r4. {high}: one inside a CLK-high stretch; Q_int and Q stay flat (shut-door icon on the master). {low}: one inside the next CLK-low stretch, ending before r5; Q_int copies it as a dashed TEAL blip, Q stays flat (shut-door icon on the slave). {only}: a YELLOW dot on D at each rising edge: the only values that reach Q.
> {airlock}: s3's two door icons return small beside the circuit and swap at a rising edge: the master's door shuts as the slave's opens.
> Checked (ideal master-slave model, Python 3.11.9): Q is unknown until r1, then 0, 1 at r2, still 1 at r3, 0 at r4, matching D just before each edge. A blip on D while CLK = 1 changes neither Q_int nor Q; a blip while CLK = 0 that ends before the next rising edge changes Q_int but not Q.

[c2.slave.1] {slave} Now the slave. Its input is cue-int, and its enable is the clock itself. {rule} So it's transparent while the clock is high, and holds while the clock is low. {start} At the start, the clock is high, so the slave is copying cue-int, which is unknown. {unknown} So cue is unknown too.

[c2.slave.2] {e1} At the first rising edge, the slave opens. The master is holding a zero, so cue becomes zero. {low1} The clock falls, and the slave holds that zero. {e2} At the second edge, the master holds a one, so cue rises to one. {e3} At the third, the master still holds a one, so cue stays at one. {e4} And at the fourth, the master holds a zero, so cue falls to zero.

[c2.slave.3] {flat} Notice that while the slave is open, the master is shut, so cue-int stays frozen underneath it. {cycle} So cue changes only at a rising edge, and then holds steady for a whole cycle.

[c2.slave.4] {read} Now read down the guide lines. {d_at} At each rising edge, here's dee just before it. Zero, one, one, zero. {q_at} And here's cue just after it. Zero, one, one, zero. {pause} {takes} At each rising edge, cue takes the value dee had, and holds it until the next one. {words} Cue changes on the rising edge of the clock. {pause=1.5}

[c2.slave.5] {blip} What about a brief blip on dee, between two edges? {pause} {high} If the clock is high, the master is shut, and the blip is stopped there. {low} If the clock is low, the blip gets into cue-int, but the slave is shut, and by the next rising edge it's gone. {only} Either way, cue stays exactly as it was. Only dee's value at the rising edge gets through. {airlock} That's the airlock at work. At the rising edge, the master's door shuts just as the slave's door opens, and that's the one moment a value passes through.

## Scene 6 · Flip-flops vs latches, and their symbols (ch2_s6_symbols)

> {name}: s5's whole master-slave circuit collapses into one box (p. 87's symbol): D at left, Q and Q̄ (overbar) at right, the clock entering from below with a small triangle. {terms}: beside it, ch1's latch symbol (EN from below with the small square). Labels under them: "latch: level-triggered" and "flip-flop: edge-triggered". {state}: GOLD "99 times out of 100" under the flip-flop.
> {symbols}: the two markers glow. {square}: the latch's square flashes YELLOW, and under it a tiny clock trace with one high level shaded. {triangle}: the flip-flop's triangle flashes YELLOW, and under it a tiny clock trace with one rising up-arrow.
> {bubble}: a third, smaller flip-flop with a bubble before its triangle, a tiny trace with a falling down-arrow, and the tag "falling edge"; {ripple}: a small tag "part 4: ripple counter". {data}: the D label briefly expands to "D = data", and the title "D flip-flop" sits over the box.
> Demo (re-enacts the lecturer's Yenka run "ms_d_ff"): {demo} p. 87's master-slave circuit returns large, with a toggle switch on D (BLUE), a toggle switch on CLK (YELLOW), and two LEDs, Q and Q̄ (GREEN when lit, as in ch1 s6). Wires at 1 bright, at 0 dim. Q_int's TEAL wire stays visible, so the viewer sees the master take the 1 before Q does. A small CLK trace under the circuit records each switch flip.
> Steps (checked, Python 3.11.9): {start} CLK = 1, D = 0, Q_int = 0, Q = 0, the Q̄ LED lit (as in the recording). {setd} D → 1: nothing else changes. {fall} CLK → 0: Q_int → 1 (TEAL wire brightens), Q stays 0.
> {rise} CLK → 1: Q → 1, the Q LED lights and the Q̄ LED goes out. {more} two more clock cycles on the switch: Q stays 1. {zero} with CLK = 0, D → 0: Q_int → 0 at once; {waits} Q stays 1. {edge} CLK → 1: Q → 0, the Q LED goes out. {edgeaction}: the CLK trace's rising arrows flash.
> {modern}: clear to p. 88's lower slide, "D Flip-Flops", as three short lines: {superseded} "Master-slave: superseded by new flip-flop circuits", "easier to implement, better performance"; {use} "use truly edge-triggered flip-flops"; {inside} DIM "their design: not on this course". {box}: the lines clear, and the flip-flop symbol alone settles at centre. It's the box the rest of the lecture uses.

[c2.symbol.1] {name} This circuit is a flip-flop. {terms} Here's the usual naming. A latch is level-triggered, and a flip-flop is edge-triggered. {state} When you build state machines, you'll use flip-flops ninety-nine times out of a hundred, because changes at a single instant make the design much easier.

[c2.symbol.2] {symbols} Their symbols tell them apart. {square} The latch has a small square on its enable input, which means level-triggered. {triangle} The flip-flop has a small triangle on its clock input, which means edge-triggered, here on the rising edge. {bubble} Put a bubble before the triangle, and since bubbles mean complement, that flip-flop changes on the falling edge instead. {ripple} The ripple counter in part four uses those. {data} And the dee stands for data, so this is a dee flip-flop.

[c2.symbol.3] {demo} Let's try it, with switches on dee and the clock, and a light on cue. {start} The clock is high, and cue is zero. {setd} Now set dee to one, and nothing happens at cue. {fall} Let the clock fall. Still nothing, because only the master has taken the one.

[c2.symbol.4] {rise} Now the clock rises, and cue lights up. {more} Keep the clock going, and it simply stays at one. {zero} Next, with the clock low, set dee back to zero. {waits} Cue keeps its one. {edge} At the next rising edge, the zero is clocked through, and cue goes dark. {pause} {edgeaction} That's edge-triggered action.

[c2.symbol.5] {modern} One last note. {superseded} The master-slave circuit has since been superseded by newer flip-flop circuits, which are easier to implement and perform better. {use} So when you design synchronous circuits, use truly edge-triggered flip-flops. {inside} How those work inside is beyond this course. {box} From here on, a flip-flop is simply this box.

## Scene 7 · Recap and next (ch2_s7_recap)

> Five small panels fill the frame one per sentence, each the scene's own visual (same objects, colours and styling) with its short line under it.
> {r1}: s1's two CLK traces, the shaded window above and the rising-edge arrows below; "a window, or an instant".
> {r2}: s2's latch with its Q̄ → D loop, and one shaded window filled with the RED buzz; "fed back, a latch oscillates".
> {r3}: s3's master-slave circuit with its CLK̄ and CLK labels and the two door icons; "two latches, never open together".
> {r4}: s4–s5's diagram cut down to CLK, D and Q, with the four guide lines and the GREEN "0 1 1 0"; "Q takes D at each rising edge".
> {r5}: s6's latch and flip-flop symbols, square and triangle flashing YELLOW; "square: latch, triangle: flip-flop".
> {next}: the panels shrink away; a J-K flip-flop box (J and K in BLUE, clock triangle, Q and Q̄) fades in beside a T flip-flop box (T in BLUE). {async}: a RED "CLR" pin grows under one box, with a RED pulse on it between two clock arrows. {why}: a YELLOW "?" beside it.
> End card after the last word, held ~8 s; the music carries it.

[c2.recap.1] {recap} Let's recap. {r1} A latch listens for a whole window, but we want changes at one instant, the clock's edge. {r2} With its output fed back, a latch oscillates for as long as the window is open. {r3} A master-slave flip-flop is two latches on opposite phases of the clock, never transparent together. {r4} So at each rising edge, cue takes dee's value, and holds it for a whole cycle. {r5} In the symbols, a square marks a latch, and a triangle marks an edge-triggered flip-flop. {pause}

[c2.recap.2] {next} Next time, the dee flip-flop's older relatives, the jay-kay and tee flip-flops. {async} And inputs that change a flip-flop without waiting for the clock at all. {why} After all this work to make everything wait for the clock, why would anyone want those? {pause}
