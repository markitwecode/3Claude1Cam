# Chapter 3 · J-K, T, and asynchronous inputs

Digital Electronics, Lecture 6 (flip-flops and counters), part 3 of 6. Source: slides
`combined_26.pdf` pp. 89–91 (refresher of the RS latch table from p. 79); recording
00:25:01–00:30:36 (transcript, digest, captions).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Spoken forms used throughout: "cue" = Q, "not cue" = Q̄, "cue prime" = Q′, "dee" = D,
"jay" / "kay" = J / K, "tee" = T, "ar-ess" = RS, "ex-or" = XOR (⊕). Every table, sequence and
waveform below was checked by exhaustive enumeration in Python 3.11.9 (standard library only).

---

## Scene 1 · Hook (ch3_s1_hook)

> On {title}, the title card: "Flip-flops and Counters", "Digital Electronics · Lecture 6", "Part 3 · J-K, T, and asynchronous inputs".
> On {last}, "Last time": ch2 s6's edge-triggered D flip-flop symbol at centre (D BLUE, CLK YELLOW into the triangle, Q GREEN, Q̄). On {edge}, ch2 s5's small CLK / D / Q timing diagram beside it: Q changes only at the YELLOW up-arrows on the rising edges and holds flat between them.
> On {books}, the D symbol slides left and dims to 0.4. Out of a closed book outline on the right (an "older textbook", sepia-dim) rise two new symbols in the same box style: one with inputs J and K, one with a single input T (all BLUE), each with a YELLOW "?" over it on {ask}.
> On {pins}, the D symbol returns to full brightness and grows two RED stub pins, one out of its top and one out of its bottom, unlabelled for now. On {ignore}, a RED arrow from them curves around the YELLOW clock input without touching it; on {why}, the caption "inputs that ignore the clock?".
> End on the chapter's road as three small labels left to right: "J-K" → "T" → "asynchronous inputs".

[c3.hook.1] {title} This is part three of flip-flops and counters. {last} Last time, we put two latches back to back and built the dee flip-flop. {edge} It changes only on the rising edge of the clock, and it holds its value for the whole cycle in between. {pause}

[c3.hook.2] {books} But open an older textbook, and you'll find other flip-flops as well, with inputs called jay and kay, or a single input called tee. {ask} What do they do, and why does this course stick to dee-types? {pause} {pins} And here's a second puzzle. {ignore} We put a lot of effort into making flip-flops wait for the clock. Yet real flip-flops come with extra inputs that ignore it. {why} Why would anyone want that? {pause=1.5}

## Scene 2 · Why the D type won (ch3_s2_family)

> Slide p. 89's heading "Other Types of Flip-Flops" (BLUE) at the top. Three symbols in a row, all in ch2's symbol style with the clock entering from below into a triangle as on p. 90: the D flip-flop (D BLUE), the J-K (J, K BLUE), the T (T BLUE); outputs Q GREEN and Q̄ on each; CLK YELLOW.
> On {dtype}, the D flip-flop's D label glows, with "D = data" under it. On {three}, a small "historically important" tag in sepia hangs over J-K and T. On {t}, the T symbol brightens briefly. On {jk}, a faint state-machine sketch (three circles with arrows) appears behind the J-K for a moment ("very popular for state machines").
> On {complex}, under the D and the J-K, a GOLD bar each, labelled "complexity to build": the J-K's bar grows clearly longer than the D's (no numbers; the slide says only "a lot more complex to build than D-types").
> On {modern}, two plain chip outlines labelled "FPGA" and "VLSI" fill with small D-type symbols; the J-K and T dim to 0.4 ("fallen out of favour in modern designs").
> On {course}, the slide's line "Consequently we will only consider synchronous circuit design using D-type FFs" appears with a GREEN tick by the D. On {complete}, under J-K and T: "for completeness".
> On {later}, J-K and T return to full brightness. On {ripple}, a small forward tag from the T: "Part 4: ripple counter". On {excite}, one from the J-K: "Part 5: excitation table".

[c3.family.1] {dtype} The flip-flop from part two is called a dee flip-flop, after its dee input. {three} Historically, two other kinds of flip-flop were important. {jk} The jay-kay flip-flop was a very popular choice for building state machines. {t} And the tee flip-flop is a close relative of it. {complex} But a jay-kay flip-flop is a lot more complex to build than a dee-type. {modern} So it has fallen out of favour in modern designs, such as field-programmable gate arrays and V-L-S-I chips.

[c3.family.2] {course} That's why this course designs synchronous circuits with dee flip-flops only. {complete} We'll still look at the jay-kay and tee tables briefly, for completeness, because you may well come across them. {later} And both of them come back later in this lecture. {ripple} Tee flip-flops build the ripple counter in part four. {excite} And in part five, the jay-kay shows what an excitation table is really for.

## Scene 3 · The J-K flip-flop (ch3_s3_jk)

> Slide p. 90's layout. On {symbol}, the J-K symbol draws big on the right (J upper left and K lower left, BLUE, each with a toggle switch; clock entering from below into the triangle, YELLOW, with a small push-button for edges; Q upper right GREEN and Q̄ lower right, each with an LED). Over it, the slide's line: "The J-K FF is similar in function to a clocked RS FF, but with the illegal state replaced with a new ‘toggle’ state".
> On {triangle}, the triangle on the clock input pulses YELLOW, tagged "edge-triggered". On {wiggle}, the J and K switches flick back and forth several times (wires bright at 1, dim at 0) while the Q and Q̄ LEDs stay frozen. On {edge}, a YELLOW up-arrow on the clock, and only then may the outputs change.
> On {table}, the table starts on the left, header exactly as p. 90: `J K | Q′ Q̄′ | comment`. For each row, set the switches, press a rising edge, then write the row: `0 0 | Q Q̄ | hold` on {hold}; `0 1 | 0 1 | reset` on {reset} (Q LED off); `1 0 | 1 0 | set` on {set} (Q LED on). The footnote "Where Q′ is the next state and Q is the current state" appears on {prime}. Q and Q′ GREEN, J and K BLUE. On {familiar}, a YELLOW "?" beside the three rows.
> On {rs}, the J-K symbol shrinks to the top right and ch1 s2's RS latch table (p. 79, same styling as in ch1) slides in to the left of the J-K table, rows aligned, its S R columns level with J K (S matches J, R matches K): `S R | Q′ Q̄′ | comment`, `0 0 | Q Q̄ | hold`, `0 1 | 0 1 | reset`, `1 0 | 1 0 | set`, `1 1 | 0 0 | illegal`. On {same}, GREEN "=" ticks link rows 1–3. On {differ}, both fourth rows get a box. On {illegal}, the RS row `1 1 | 0 0 | illegal` turns RED.
> On {trick}, both switches go to 1 (J and K wires bright). The J-K's fourth row on {swap}: copies of `Q Q̄` from row 1 lift out and cross over into `Q̄ Q` (TransformFromCopy), and on {name} the word "toggle" appears in YELLOW. On {flip}, on the symbol, J = K = 1 and an edge makes the Q and Q̄ LEDs swap.
> Close on {summary}: RS row 4 (RED, "illegal") with a YELLOW arrow to the J-K row 4 ("toggle"); everything else dims.
> Checked (Python 3.11.9, by enumeration): the NOR RS latch settles to Q = Q̄ = 0 for S = R = 1; the J-K rows 00, 01, 10 equal the RS rows with S = J and R = K, and only row 11 differs.

[c3.jk.1] {symbol} Here's the jay-kay flip-flop. It has two inputs, jay and kay, and the usual two outputs, cue and not cue. {triangle} Notice the triangle on its clock input. That means it's edge-triggered. {wiggle} Whatever you do to jay and kay, the outputs stay put. {edge} They can change only when a rising edge arrives on the clock. {pause}

[c3.jk.2] {table} So what happens on that edge? Let's build the table, one row at a time. {prime} As before, cue prime is the next state, and cue is the current state. {hold} With jay and kay both zero, nothing happens on the edge. Cue prime equals cue, so this is the hold condition.

[c3.jk.3] {reset} With jay at zero and kay at one, cue goes to zero when the edge arrives. That's the reset condition. {set} Now put jay at one and kay at zero, and cue goes to one. That's the set condition. {familiar} Does this look familiar? {pause}

[c3.jk.4] {rs} It's the reset-set latch from part one, with jay playing the part of set, and kay the part of reset. {same} The first three rows match exactly. {differ} The difference is in the last row. {illegal} For the reset-set latch, both inputs at one was illegal. Both outputs were forced to zero, so cue and not cue were equal, a horrible condition.

[c3.jk.5] {trick} Here's the neat trick of the jay-kay. Set both inputs to one, {swap} and cue prime becomes not cue, while not cue prime becomes cue. {flip} In other words, the outputs swap. Whatever state the flip-flop is in, it changes to the opposite one. {name} This is called the toggle condition. {pause} {summary} So a jay-kay works like a clocked reset-set flip-flop, with the illegal state replaced by a useful new state, toggle.

## Scene 4 · Toggling in time (ch3_s4_toggle)

> On {tie}, s3's J-K symbol shrinks to the upper left with J and K both wired to a BLUE "1" (wires bright). s3's table shrinks beside it with only the toggle row `1 1 | Q̄ Q | toggle` lit YELLOW.
> Timing diagram in ch2's style across the lower two-thirds: on {clock}, CLK on top (YELLOW) for six cycles, thin vertical guides and small up-arrows at its rising edges; on {start}, Q (GREEN) underneath, a short flat stretch at 0. Propagation delays neglected, as in ch2: Q steps exactly on the guides.
> Draw Q edge by edge as the narration counts: on {e1} it rises to 1, on {e2} falls to 0, on {e3} rises to 1, on {e4} falls to 0, each new value written small above Q at its edge; then the last two cycles fill in on their own.
> On {wave}, the whole Q trace glows GREEN. On {count}, the first four rising edges are numbered 1–4 in YELLOW above CLK, and Q's two rises in those cycles are numbered 1–2 in GREEN. On {flips}, two consecutive edges glow, the first labelled "up", the second "down". On {period}, GOLD braces: "1 clock period" under one CLK cycle, "2 clock periods" under one Q cycle.
> On {half}, GOLD frequency labels at the right end of each trace: "f" by CLK, "f/2" by Q, and the caption "half the frequency", which stays on screen to the end of the scene.
> On {chain}, a ghost of a second and third toggling trace appears below Q (f/4, f/8, dim GOLD), with a small forward tag "Part 4: dividers" on {divider}. ("half the frequency" is still up from {half} through {keep}.)
> Checked (Python 3.11.9): from Q = 0 with J = K = 1, four rising edges give 1, 0, 1, 0; sampled every half period, Q's period is twice CLK's.

[c3.toggle.1] {tie} Now hold jay and kay both at one, and watch the flip-flop over time. {clock} Here's the clock, with arrows on its rising edges. As in part two, we ignore propagation delays, so cue changes exactly on the edges. {start} Say cue starts at zero. {e1} At the first rising edge, it toggles to one. {e2} At the next edge, it goes to zero, {e3} then to one, {e4} then back to zero. {pause}

[c3.toggle.2] {wave} Now look at the shape of cue. It's a square wave as well, but a slower one. {count} Over four clock cycles, the clock rises four times, but cue rises only twice. {flips} Each rising edge flips it once, and one full cycle of cue needs two flips, one up and one down. {period} So the period of cue is two clock periods. {half} That means its frequency is half the clock's frequency. {pause}

[c3.toggle.3] {keep} Hold on to that idea. A flip-flop that toggles on every edge divides the clock frequency by two. {chain} In part four, we'll chain toggling flip-flops, each one clocked by the one before, and cut the frequency in half again and again. {divider} That's how a counter can also work as a divider.

## Scene 5 · The T flip-flop (ch3_s5_t)

> Slide p. 90's lower half. Start from s3's J-K symbol and table. On {tie}, the J and K wires bend toward each other and fuse into one BLUE wire; the labels J and K merge into "T", and the box becomes p. 90's T symbol (T on the left, clock from below into the triangle, Q GREEN, Q̄).
> On {rows}, the table rows `0 1` and `1 0` fade out (they need J ≠ K); rows `0 0` and `1 1` slide together and their J K entries merge into one T column: header `T | Q′ Q̄′ | comment`, rows `0 | Q Q̄ | hold` (on {hold}) and `1 | Q̄ Q | toggle` (on {toggle}, YELLOW), with the footnote "Where Q′ is the next state and Q is the current state". On {name}, the symbol is labelled "T flip-flop (toggle)".
> On {compact}, the T table's two rows pulse. On {xor}, the formula grows out of the table: `Q′ = T ⊕ Q` (Q′ and Q GREEN, T BLUE). Beside it, a four-row check `T Q | Q′`: `0 0 | 0`, `0 1 | 1`, `1 0 | 1`, `1 1 | 0`. On {zero}, the T = 0 pair is bracketed "keeps Q"; on {one}, the T = 1 pair "flips Q" (YELLOW). On {match}, the brackets link to the T table's "hold" and "toggle".
> On {feedback}, a fresh scene setting: ch2's D flip-flop symbol (D BLUE) with a wire from Q̄ looping back around to D. On {next}, the label `Q′ = D = Q̄`. On {same}, an "=" to the T symbol with T tied to 1, and `Q̄ = 1 ⊕ Q` under it. (This shot returns in ch6 s2.)
> On {runaway}, ch2 s2's oscillating D latch, small, on the left: the same Q̄-to-D loop on a latch (small square on EN), Q flickering RED all through the shaded EN-high window. On {safe}, on the right, the flip-flop's Q with one clean GREEN step per YELLOW rising edge.
> On {ch6}, a small forward tag under the D flip-flop loop: "Part 6: first stage of a counter".
> Checked (Python 3.11.9, by enumeration): J = K = T leaves exactly the hold and toggle rows; Q′ = T ⊕ Q for all four (T, Q); with D = Q̄, Q′ = Q̄ = 1 ⊕ Q for both values of Q.

[c3.t.1] {tie} Now connect jay and kay together, and call that single input tee. {rows} Only two rows of the table can happen now, the ones where jay and kay are equal. {hold} With tee at zero, the flip-flop holds. {toggle} With tee at one, it toggles on every rising edge. {name} This is the tee flip-flop, or toggle flip-flop, and here's its symbol.

[c3.t.2] {compact} There's a compact way to write this table. {xor} Cue prime equals tee ex-or cue, where ex-or is the exclusive or from earlier in the course. {zero} An ex-or with zero keeps a bit as it is. {one} An ex-or with one flips it. {pause} {match} So that one formula says hold when tee is zero, and toggle when tee is one.

[c3.t.3] {feedback} There's another way to build a toggle. Take a dee flip-flop, and wire its not cue output back to its dee input. {next} At each rising edge, cue prime equals dee, which is not cue. {same} So it flips on every edge. It's a tee flip-flop with tee stuck at one. {pause}

[c3.t.4] {runaway} You've seen this wiring before. In part two, a dee latch wired the same way oscillated. While enable was high, it flipped again and again, as fast as its gates allowed. {safe} The flip-flop acts only at the edge, so it flips exactly once per clock cycle. {ch6} In part six, this little circuit becomes the first stage of a counter.

## Scene 6 · Asynchronous inputs (ch3_s6_async)

> Slide p. 91's heading "Asynchronous Inputs". On {extra}, ch2's D flip-flop symbol at centre, CLK YELLOW with its triangle, and the slide's first line: "It is common for the FF types we have mentioned to also have additional so called ‘asynchronous’ inputs". On {independent}, a RED arrow comes straight into the box from the side, past the YELLOW clock input, and Q (GREEN) changes at once, with no edge arrow anywhere; caption from the slide: "take effect independently of any clock or enable inputs".
> On {pointless}, a YELLOW "?" over the YELLOW clock input: all that effort for edges, now bypassed.
> On {startup}, a power switch flips on beside three small flip-flops. On {power}, each Q LED flickers between 0 and 1 and settles at random (e.g. 1 0 1), each with a small "?". On {machine}, the caption "a state nobody planned" in RED.
> On {pins}, back to one symbol: RED pins grow out of the box, "PRE" on top and "CLR" underneath. On {clear}, "Reset/Clear – force Q to 0" (slide wording) by CLR, and Q goes to 0; on {preset}, "Preset/Set – force Q to 1" by PRE, and Q goes to 1. On {all}, small D, J-K and T symbols side by side, each with PRE on top and CLR underneath.
> On {sketch}, a T flip-flop with T tied to 1 and its timing sketch in ch2's style: CLK (YELLOW, guides and up-arrows at rising edges 1–5), CLR (RED, low except for one short pulse between edges 1 and 2, back low well before edge 2), Q (GREEN).
> Q is unknown from power-on, drawn at both levels at once as on slide p. 88 ({unknown}); still both levels after edge 1 ({edge1}). On {pulse}, the CLR pulse rises; on {drop}, both of Q's levels collapse to a single line at 0 right there, mid-cycle, away from any guide, with a small RED "no clock edge" marker. On {known}, Q toggles 1, 0, 1 at edges 2, 3, 4, each value written above Q.
> On {use}, the slide's last line: "Often used to force a synchronous circuit into a known state, say at start-up." On {zero}, a small preview: three flip-flops in a row (ch4's ripple counter, small) with their CLR pins joined to one RED line; a pulse on it and all three Q LEDs show 0, tagged "Part 4: clear, then count". On {count}, a second tag "Part 4: back to 0 after 9".
> Checked (Python 3.11.9): with T = 1, an unknown Q stays unknown through edge 1; CLR forces Q = 0; edges 2, 3, 4 then give 1, 0, 1.

[c3.async.1] {extra} Practical flip-flops often have extra inputs, called asynchronous inputs. {independent} They take effect independently of any clock or enable input. Apply one, and the flip-flop changes state right away, without waiting for an edge. {pause} {pointless} That sounds a bit pointless. We spent all that effort making flip-flops synchronous, and now there are inputs that ignore the clock? {pause}

[c3.async.2] {startup} The reason goes back to a question someone asked at the end of the last lecture. What happens at start-up? {power} When you turn a circuit on, each flip-flop comes up in a state nobody chose. Its output could be one, or it could be zero. {machine} So a state machine could begin in a state its designer never planned for, and go wrong from there. {pause}

[c3.async.3] {pins} The fix is two extra inputs, drawn on the top and the bottom of the box. {clear} Reset, also called clear, forces cue to zero. {preset} Preset, also called set, forces cue to one. {all} It's common for all the flip-flop types we've met to have them.

[c3.async.4] {sketch} Let's watch clear at work, on a tee flip-flop with tee at one. {unknown} At power-on, cue is unknown, so it's drawn at both levels. {edge1} The first edge toggles it, and it's still unknown. {pulse} Then a pulse arrives on clear, between two edges. {drop} Cue drops to zero at once, with no clock edge at all. {known} From then on, each edge does what we expect, one, zero, one. {pause}

[c3.async.5] {use} That's what these inputs are for. They force a synchronous circuit into a known state, say at start-up. {zero} Part four's counter starts exactly this way, with every flip-flop cleared to zero before it counts. {count} And a clear input will also send that kind of counter back to zero after nine.

## Scene 7 · Recap and next (ch3_s7_recap)

> On {recap}, the heading "Recap". Then one small version of each scene's visual per sentence, same objects, colours and styling, laid out left to right in two rows, each with its short line under it; the previous one dims to 0.5 as the next arrives.
> On {r1}: s2's row of three symbols, the D with its GREEN tick, J-K and T dimmed. Line: "D-types in modern designs; J-K and T for completeness".
> On {r2}: s3's RS table beside the J-K table, RS row 4 RED "illegal", J-K row 4 YELLOW "toggle". Line: "J-K: the illegal state becomes toggle".
> On {r3}: s4's CLK and Q traces with the GOLD "f" and "f/2". Line: "toggling halves the frequency".
> On {r4}: s5's T table with `Q′ = T ⊕ Q`. Line: "T: 0 holds, 1 toggles". On {loop}: beside it, s5's small D flip-flop with Q̄ looped back to D, "=" a T with T = 1. Line: "D = Q̄ toggles".
> On {r5}: s6's timing sketch, the RED CLR pulse and Q collapsing to 0 between edges. Line: "PRE and CLR: no edge needed".
> On {next}: everything clears; three toggling flip-flops in a chain (bubble before each triangle, ch4 s3's ripple-counter silhouette) with three GREEN LEDs. On {ripple}, a GOLD "simplest to build" and a RED "worst to use" under it. Then the end card: hold about 8 s after the last word while the music carries it.

[c3.recap.1] {recap} Let's recap. {r1} Modern designs use dee flip-flops, and the jay-kay and tee types are here for completeness. {r2} A jay-kay flip-flop is like a clocked reset-set flip-flop, with the illegal state replaced by toggle. {r3} Toggling on every edge makes a square wave at half the clock's frequency.

[c3.recap.2] {r4} A tee flip-flop holds when tee is zero and toggles when tee is one, so cue prime equals tee ex-or cue. {loop} A dee flip-flop with not cue fed back to dee is a tee flip-flop with tee at one. {r5} And asynchronous preset and clear force cue to one or zero at once, with no clock edge, to start a circuit in a known state. {pause}

[c3.recap.3] {next} Next time, we'll put flip-flops to work, starting with counters. {ripple} First comes the simplest counter to build, and the worst one to use. {pause}
