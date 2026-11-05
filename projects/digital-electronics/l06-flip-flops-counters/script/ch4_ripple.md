# Chapter 4 · Counters, and the ripple counter

Digital Electronics · Lecture 6 (Flip-flops and Counters), part 4 of 6. Source: slides (combined_26.pdf) pp. 92–95, up to the BCD bullet on p. 95; recording 00:30:36–00:42:53.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch4_s1_hook)

> Title card: "Flip-flops and Counters", "Digital Electronics · Lecture 6", "Part 4 · Counters, and the ripple counter".
> {last}: a small row of ch3's symbols (the J-K box, the T box, and a D box with RED PRE on top and RED CLR underneath), in ch3's styling; they shrink away on {work}.
> Hero: a simple digital watch, centre, its display reading 12:00:00 with the seconds digits in GOLD. On {crystal}, a small quartz crystal appears inside, and a YELLOW square wave streams out of it, far too fast to follow, labelled GOLD "tens of thousands per second".
> On {tick}, the seconds digits tick once, then again (12:00:01, 12:00:02), slow and steady, a GREEN pulse on each tick.
> On {count}, a box with a GOLD "?" sits between the fast wave and the display, labelled "something counts".
> On {question}, three empty flip-flop outlines (BLUE) fill the box, and the question appears under the watch: "How do you build a counter from flip-flops?"; on {wrong}, a second line in RED: "What can go wrong?"
> On {plan}, the three outlines line up in a chain (a foretaste of s3's circuit), and a small RED "avoid" tag appears beside them.

[c4.hook.1] {last} Last time, we met the jay-kay and tee flip-flops, and the asynchronous inputs that ignore the clock. {work} Now let's put flip-flops to work. {crystal} Inside a digital watch, a tiny quartz crystal vibrates tens of thousands of times every second. {tick} Yet the seconds on the display change just once a second. {count} Somewhere in between, something is counting those vibrations. {pause}

[c4.hook.2] {question} So how would you build a counter from flip-flops? {wrong} And what can go wrong when you do? {pause} {plan} We'll build the simplest counter there is, called a ripple counter. We'll watch it count, and then see why this course tells you to avoid it.

## Scene 2 · What a counter is (ch4_s2_counters)

> Top, slide p. 92's definition as a text block: "A counter is a clocked sequential finite state machine that goes through a predetermined sequence of states", "clocked" in YELLOW, "predetermined sequence of states" in BLUE. On {gloss}, a small sketch under it: four BLUE state circles in a row joined by arrows, a YELLOW clock tick on each arrow, a dot hopping one state per tick.
> On {binary}: "n-bit binary counter: n FFs, 2ⁿ states" with 2ⁿ in GOLD; on {order}, the order "0, 1, 2, …, 2ⁿ − 1, 0, 1, …" writes itself out, the final 0 sliding back under the first.
> On {ring}, the definition shrinks to the top and the hero appears: the running example's state ring, eight nodes in a circle, 000 at the top, going clockwise to 111. Each node shows its bits in GREEN with the GOLD decimal beside it (000 = 0, 001 = 1, …, 111 = 7). On {eight}, GOLD "2³ = 8". On {bits}, a header "Q2 Q1 Q0" with Q2 tagged "most significant bit". On {wrap}, a YELLOW dot steps node to node, one step per small YELLOW clock-edge tick, and the 111 → 000 arrow lights YELLOW as it wraps.
> This ring and its binary labels are the chapter's running counter; s3 unrolls it into a column, and ch5 and ch6 reuse both.
> On {uses}, the ring slides left and p. 92's four uses appear on the right, one per mark: "Counting" ({counting}), "Producing delays of a particular duration" ({delays}), "Sequencers for control logic in a processor" ({sequencers}), "Divide by m counter (a divider), as used in a digital watch" ({divider}, with s1's watch shrunk beside it).
> On {memories}, a DIM aside card from p. 93: "Memories", "Shift register", "Parallel loading shift register: parallel to serial conversion", "Serial in, parallel out shift register: serial to parallel conversion", tagged "next lecture".
> On {kinds}, everything clears to two labels side by side, from p. 93: "ripple counters" ({ripple}) and "synchronous counters" ({sync}). On {avoid}, under "ripple counters" in RED: "do not follow synchronous design principles: avoid if at all possible". On {why}, a magnifying glass settles over "ripple counters": "We will now look at the problems with ripple counters".

[c4.def.1] {def} First, what is a counter? {fsm} The slides define it as a clocked sequential finite state machine that goes through a predetermined sequence of states. {gloss} In other words, it has a fixed set of states, and each clock edge moves it on to the next one, in an order fixed in advance. {binary} The most common is the N-bit binary counter. It has N flip-flops, so it has two to the N states. {order} It passes through them in order, zero, one, two, and so on, up to two to the N, minus one, and then it goes back to zero.

[c4.def.2] {ring} Here's an example, with three flip-flops. {eight} Two to the three is eight, so there are eight states, and it counts from zero to seven. {bits} We'll write each state as three bits, cue two, cue one, cue zero, with cue two as the most significant bit. {wrap} Each clock edge moves the counter one step around the ring, and after seven, it wraps back to zero.

[c4.def.3] {uses} So what are counters for? {counting} Counting, of course. {delays} Producing delays of a set length. {sequencers} Sequencing the control logic in a processor. {divider} And dividing down a frequency, as in our digital watch. {memories} Flip-flops also build memories, both memory arrays and shift registers, which convert data between parallel and serial form. The next lecture builds one of those.

[c4.def.4] {kinds} Most books show two basic kinds of counter. {ripple} Ripple counters, {sync} and synchronous counters. {avoid} Ripple counters break the synchronous design rules this course is built on, so the slides say to avoid them if at all possible. {why} Then why study one? {pause} Because its problems show exactly why synchronous design matters.

## Scene 3 · The ripple counter circuit (ch4_s3_ripple)

> Slide p. 94's circuit, hero, built left to right: three T flip-flop boxes in ch3's T symbol style (T input on the left, Q and Q̄ on the right, the clock input on the bottom edge with a bubble before its triangle, as on p. 94), each T input wired to a BLUE '1' (on {one}). Each Q runs right, then down into the next box's clock input; outputs labelled Q0, Q1, Q2 (GREEN) on top. On {toggle}, a small inset of ch3's T table with its toggle row lit ("1 | Q̄ Q | toggle").
> On {bubble}, zoom on the first clock input; on {triangle} the triangle flashes YELLOW; on {circle} the bubble in front of it flashes. On {falling}, a tiny YELLOW falling edge with a down-arrow appears beside it, labelled "toggles on the falling edge" (ch2 s6's bubble-and-triangle symbol). Beside it, briefly, ch3's T symbol with its plain triangle and a rising edge with an up-arrow, DIM, labelled "so far: rising edge".
> On {clock}, zoom back out: CLK (YELLOW) enters the first clock input only, and that wire glows. On {chain}, the wire from Q0 down into the second flip-flop's clock input glows GREEN; on {next}, the wire from Q1 into the third does the same.
> On {notsync}, a RED label over the three clock inputs: "not clocked using the same clock: not a synchronous design" (p. 94's words).
> On {column}, the circuit shrinks to the top and s2's ring unrolls (TransformFromCopy) into a column: 000, 001, …, 111, then 000 again, headed Q2 Q1 Q0, GOLD decimals beside. On {lsb}, the Q0 column's every flip ticks YELLOW.
> On {carry}, each place where Q0 goes from 1 to 0 gets a YELLOW arrow pointing at Q1's flip on the same step (1 → 2, 3 → 4, 5 → 6, 7 → 0). On {edge}, one of those 1 → 0 steps flies up to the wire from Q0 into the second clock input and becomes a falling edge on it, with its down-arrow. On {same}, the same arrows appear from Q1's falls to Q2's flips (3 → 4 and 7 → 0).
> (Checked in Python 3.11.9 by enumeration for 3, 4 and 8 bits: counting up by one, bit 0 always flips, and every other bit flips exactly when the bit to its right goes from 1 to 0.)

[c4.ripple.1] {circuit} Here's the ripple counter from the slides. {tflip} It's three tee flip-flops in a chain, {one} and every tee input is tied to one. There's no other logic at all, only wires. {toggle} Remember from last time that a tee flip-flop with tee at one is in toggle mode. Every active clock edge flips its output.

[c4.ripple.2] {bubble} Now look closely at the clock inputs. {triangle} As in part two, the triangle means edge-triggered, {circle} and the circle in front of it means complemented. {falling} Together, they mean these flip-flops toggle on the falling edge of their clock, the negative-going edge. So far, every flip-flop we've used acted on the rising edge. These are the first to act on the falling one.

[c4.ripple.3] {clock} The clock goes only into the first flip-flop. {chain} Its output, cue zero, drives the clock input of the second, {next} and cue one drives the clock input of the third. {notsync} So the flip-flops do not all share the same clock. This is not a synchronous design, and as the slide warns, that gives some problems. {pause}

[c4.ripple.4] {why} But first, why does this chain count at all? {column} Write zero to seven in binary, in a column. {lsb} The last bit, cue zero, flips on every step. {carry} Now watch cue one. It flips exactly when the bit to its right falls from one to zero. That's the carry, when you add one. {edge} And a fall from one to zero is precisely a falling edge on its clock input. {pause} {same} The same goes for cue two, so the chain counts up.

## Scene 4 · The timing diagram (ch4_s4_timing)

> A timing diagram in ch2–ch3's style, filling the frame: rows CLK (YELLOW), Q0, Q1, Q2 (GREEN), labels on the left, as slide p. 94. New in this chapter: delays are drawn, as a small, clearly visible gap after each cause.
> On {reset}, all three Q rows start at 0, with a small RED "CLR" pulse at their left end (ch3 s6's clear input).
> On {clk}, CLK draws first: it begins low, rises, and falls at the first arrow, as on p. 94, for eight falling edges. On {arrows}, a small down-arrow appears on each falling edge, with a thin vertical guide line through all rows.
> On {q0}, Q0 draws itself segment by segment: up after the first guide, down after the second, up, down. On {delay}, zoom on the first edge: a GOLD bracket spans the gap between the guide line and Q0's change; on {prop} it is labelled "propagation delay".
> On {q1}, Q0's falling edges flash. On {q1first}, a short arrow runs from Q0's first fall (at the second guide) down to Q1, which rises a further gap later; on {q1rest}, the same at each later fall of Q0: down, up, down. On {q2}, Q1's first fall (at the fourth guide) arrows down to Q2, which rises; on {q2fall}, Q2 falls after the eighth guide. On {stair}, the three stacked changes at the fourth and eighth guides glow GOLD: a little staircase, one delay per step.
> On {read}, the GOLD counts appear along the bottom, one under each stretch between guides, with the bits Q2 Q1 Q0 in GREEN above each: 000 = 0 ({r0}), 001 = 1 ({r1}), 010 = 2 ({r2}), 011 = 3 ({r3}), 100 = 4 ({r4}), then 5 to 7 quickly ({rest}), and 000 = 0 ({wrap}). A cursor sweeps left to right as they are read.
> Keep this diagram: s5 zooms into its eighth falling edge, and s6 measures its periods.
> (Checked in Python 3.11.9 by an event-driven simulation, delay 1, clock period 20: the settled count before each falling edge is 0, 1, 2, 3, 4, 5, 6, 7, 0; Q0's period is 2, Q1's 4 and Q2's 8 clock periods.)

[c4.timing.1] {diagram} Let's draw its timing diagram. {reset} We start with every flip-flop reset to zero, using the clear inputs from last time. {clk} As always, the clock comes first. {arrows} The first flip-flop triggers on falling edges, so we mark each falling edge with a little down arrow.

[c4.timing.2] {q0} Cue zero toggles at every falling edge of the clock. Up to one, down to zero, up, and down again. {delay} But notice that each change comes slightly after the edge. That gap is drawn on purpose. {prop} It's the flip-flop's propagation delay, the time between the clock edge and the change at the output. In this part, those delays are the whole point.

[c4.timing.3] {q1} Now cue one. Its clock is cue zero, so we look for the falling edges of cue zero. {q1first} The first one comes at the second clock edge, and a delay after it, cue one toggles up to one. {q1rest} At each later fall of cue zero, cue one toggles again. Down, up, and down. {q2} Cue two's clock is cue one. Cue one first falls at the fourth clock edge, so that's where cue two goes up, {q2fall} and it comes back down at the eighth. {stair} At those two edges, the changes stack into a little staircase, each one a delay after the last.

[c4.timing.4] {read} Now let's read the count, with cue two as the most significant bit. {r0} At the start, it reads zero, zero, zero, which is zero. {r1} After the first edge, zero, zero, one, which is one. {r2} Then zero, one, zero, which is two. {r3} Zero, one, one, three. {r4} One, zero, zero, four. {rest} Then five, six, seven, {wrap} and back to zero, zero, zero. {pause} It counts from zero up to seven, and starts again.

## Scene 5 · Where ripple goes wrong (ch4_s5_problems)

> Zoom into s4's diagram at the eighth falling edge, the step from 7 to 0: its YELLOW guide line, and the three falls stacked one delay apart, Q0, then Q1, then Q2, each delay a GOLD bracket.
> A readout box under the zoom steps as a cursor moves right: "111 = 7" in GREEN ({still}), "110 = 6" in RED ({six}), "100 = 4" in RED ({four}), "000 = 0" in GREEN ({zero}). On {passed}, the trail 7 → 6 → 4 → 0 stays under the zoom, the 6 and 4 RED. (Checked in Python 3.11.9 by simulation: one, two and three delays after the edge the outputs read 6, 4, 0.) ch6 s6 replays this zoom for contrast, so keep it self-contained.
> On {sametime}, p. 94's first problem as a text block: "See outputs do not change at the same time, i.e., synchronously. So hard to know when count output is actually valid." On {valid}, a RED "?" over the readout while it is 6 or 4.
> On {buildup}, the three GOLD delay brackets slide together end to end; on {three}, "3 stages → 3 delays"; on {general}, "n stages → n delays".
> On {fast}, the clock is squeezed: on {early}, the next falling edge (a new YELLOW guide with its down-arrow) arrives two and a half delays after the 7 → 0 edge, cutting through the staircase before Q2 has fallen. On {wrong}, the readout at that edge says "100 = 4" with a RED "not 0". (Checked in Python 3.11.9: with a clock period of 2.5 flip-flop delays, the outputs read 100 at the next falling edge.) On {limit}, p. 94's second problem: "Propagation delay builds up from stage to stage, limiting maximum clock speed before miscounting occurs."
> On {balance}, a two-sided card: GREEN "very simple: just string flip-flops together" ({simple}) | RED "not synchronous: outputs change at different times" ({rules}).

[c4.prob.1] {zoom} Now zoom in on the step from seven back to zero. {still} Just after the clock edge, the outputs still read one, one, one, which is seven. {six} Then cue zero falls, and they read one, one, zero, which is six. {four} Then cue one falls, and they read one, zero, zero, which is four. {zero} Only when cue two falls do we reach zero, zero, zero, the count we wanted. {pause} {passed} On its way from seven to zero, the counter passed through six and four.

[c4.prob.2] {sametime} That's the first problem on the slide. The outputs change at different times, not synchronously. {valid} So it's hard to know when the count is actually valid. Read the outputs during the ripple, and you might get six, or four, instead of zero.

[c4.prob.3] {buildup} The second problem is that the delay builds up, stage by stage. {three} Here, three flip-flops means three delays before the count settles. {general} With N flip-flops, it's N delays. {fast} Now speed up the clock. In other words, bring its falling edges closer together. {early} The next edge can arrive before the ripple has finished. {wrong} At that edge, the outputs still read four, not zero. {limit} So the delay that builds up sets a maximum clock speed. Any faster, and the counter miscounts.

[c4.prob.4] {balance} So that's the ripple counter. {simple} It's very simple. You just string a bunch of flip-flops together. {rules} But it breaks the synchronous rules, and these two problems are the price.

## Scene 6 · Counters as dividers (ch4_s6_divider)

> s4's full diagram returns, unzoomed. On {period}, GOLD brackets measure one period on each row: on {q0}, CLK's period and, on Q0, a bracket twice as long; on {q1}, Q1's period, twice Q0's; on {q2}, Q2's, twice again. Frequency labels appear at the right end of each row in GOLD: "f" (CLK), "f/2" (Q0), "f/4" (Q1), "f/8" (Q2).
> On {callback}, a small inset of ch3 s4's toggling waveform with its "half the frequency" label, set beside the Q0 row.
> On {dividers}, p. 95's sentence as a text block: "each has half the frequency, i.e., double the repetition period of the previous one. This is why counters are often known as dividers", with "dividers" in YELLOW ({name}).
> On {more}, the chain of s3's flip-flops stretches to the right with more stages, the frequency labels continuing "f/16, f/32, …"; then "n flip-flops: f / 2ⁿ". On {thousand}, GOLD "3 → ÷ 8" and "10 → ÷ 1,024".
> On {watch}, s1's watch returns. On {crystal}, its crystal is labelled "about 32 kHz"; on {exact}, the label resolves to GOLD "32,768 Hz", and on {power}, "= 2¹⁵ Hz".
> On {chain}, a ripple chain of 15 small toggling flip-flops runs from the crystal to the display, each output labelled with its frequency: 16,384, 8,192, 4,096, …, 4, 2, 1 Hz (the first few and last few shown, an ellipsis in the middle). On {second}, the final output "1 Hz" drives the seconds digits, which tick once. (Checked in Python 3.11.9: 32,768 = 2¹⁵, and 32,768 / 2¹⁵ = 1 Hz.)

[c4.div.1] {period} Now look at how often each output repeats. {q0} Cue zero goes through one cycle for every two clock cycles. It has twice the period of the clock, so half the frequency. {callback} That's the toggling flip-flop from last time. {q1} Cue one has twice the period of cue zero, so a quarter of the clock's frequency. {q2} And cue two has an eighth.

[c4.div.2] {dividers} Each output has half the frequency of the one before it. {name} That's why counters are often called dividers. {more} Add more flip-flops to the chain, and each one cuts the frequency in half again. With N flip-flops, you divide the clock's frequency by two to the N. {thousand} Three flip-flops divide by eight. Ten flip-flops would divide by one thousand and twenty-four.

[c4.div.3] {watch} Back to the watch, and the something that counts. {crystal} The lecturer puts its crystal at about thirty-two kilohertz, some funny number. {exact} The usual number is thirty-two thousand, seven hundred and sixty-eight hertz. {power} And that's exactly two to the power of fifteen. {chain} So a chain of fifteen toggling flip-flops cuts it in half fifteen times, {second} and out comes one cycle per second. {pause} The funny number was chosen to be a power of two.

## Scene 7 · Counting to nine (ch4_s7_bcd)

> On {power}, the 3-bit column from s3 (0 to 7), then a 4-bit one (0 to 15), each wrapping to 0. On {bcd}, p. 95's line: "Often we wish to have a count which is not a power of 2, e.g., for a BCD counter (0 to 9)", and a row of GOLD digits 0 to 9, each with its four bits underneath in GREEN (0000 … 1001).
> On {recipe}, p. 95's two bullets: "use FFs having a Reset/Clear input" ({clr}) and "Use an AND gate to detect the count of 10 and use its output to Reset the FFs" ({and}).
> Circuit: s3's ripple chain grows to four T flip-flops, outputs Q0, Q1, Q2, Q3 (GREEN), each now with a RED CLR input underneath (ch3 s6's symbol), the four CLR inputs joined by one RED line.
> On {which}, the 4-bit column 0000 to 1010 with headers Q3 Q2 Q1 Q0; on {ten}, row 1010 = 10 lights YELLOW; on {first}, the Q3 and Q1 bits light in every row, and 1010 is the first row where both are 1. A two-input AND gate (distinctive shape) takes Q3 and Q1, and its output wires to the RED CLR line. A small DIM tag: "ours: the slide says only 'an AND gate to detect the count of 10'". (Checked in Python 3.11.9 by enumeration: Q3 = Q1 = 1 first at 10 among 0–15, and none of the ripple's in-between states on the way from 0 to 10 has both.)
> On {run}, a GOLD count display above the circuit, with the bits Q3 Q2 Q1 Q0 lit underneath (bright for 1, dim for 0): 8 = 1000 ({eight}), 9 = 1001 ({nine}), each held for a clock period. On {appears}, 10 shows in RED; on {reset}, the AND output pulses RED, the CLR line fires, and all four Q drop to 0 together, with no clock edge. On {flash}, the display reads 0; a mini timeline under it shows 8 and 9 as full-width blocks and 10 as a thin RED sliver.
> On {held}, the 9 block in the mini timeline glows GOLD under a bracket "one clock period". On {ifnine}, a second, DIM timeline: "reset at 9": 9 is only a thin sliver, and the counter shows 0 to 8. On {glitch}, the RED sliver of 10 is set beside s5's RED 6 and 4.
> On {verdict}, two lines: GREEN "arbitrary counts: easy" ({simple}) and, on {stick}, BLUE "in general: stick to synchronous designs".

[c4.bcd.1] {power} A binary counter counts up to a power of two, minus one. Three bits count to seven, and four bits count to fifteen. {bcd} But often we want a different count. A common one is binary-coded decimal, which counts from zero to nine, and then starts again.

[c4.bcd.2] {recipe} The slide's recipe has two parts. {clr} Use flip-flops that have a reset, or clear, input. {and} And use an and gate to detect the count of ten, and use its output to reset the flip-flops. {which} Which bits does the gate need to look at? {pause} {ten} Ten is one, zero, one, zero. {first} It's the first count where cue three and cue one are both one. So an and gate on just those two bits is enough.

[c4.bcd.3] {run} Let's run it. {eight} Eight, one, zero, zero, zero. {nine} Nine, one, zero, zero, one. {appears} And then ten appears. {reset} The gate's output goes high, the clear inputs act, and every flip-flop drops to zero together, without waiting for the clock. {flash} Ten lasts only an instant. {pause}

[c4.bcd.4] {why} Why detect ten, and not nine? {pause} {held} Because nine has to last a full clock period, like every other count. {ifnine} If the gate detected nine, then nine would only flash, and the counter would really count from zero to eight. {glitch} The flash of ten is one more false count, like the six and four from before.

[c4.bcd.5] {verdict} So arbitrary counts are easy to make this way, {simple} and for unsophisticated jobs, a ripple counter might do. {stick} But in general, the lecturer's advice is to stick to synchronous designs.

## Scene 8 · Recap and next (ch4_s8_recap)

> Recap: a grid of six small panels, each a miniature of its scene's visual in that scene's colours and styling, its line underneath, appearing one per mark:
> {r1}: s2's state ring, 000 to 111 with GOLD decimals, the YELLOW dot stepping once round; line "counter: n flip-flops, 2ⁿ states". {r2}: s3's ripple circuit, CLK into the first flip-flop only, Q0 and Q1 wires glowing into the next clock inputs; line "each stage clocked by the one before".
> {r3}: s4's timing diagram, CLK and Q0 to Q2 with the counts 0 to 7, 0 along the bottom; line "it counts, one delay per stage". {r4}: s5's 7 → 0 zoom with its trail 7 → 6 → 4 → 0, the 6 and 4 RED; line "delays add up: false counts, speed limit".
> {r5}: s6's frequency labels f, f/2, f/4, f/8 beside their rows; line "each output halves the frequency: dividers". {r6}: s7's four-flip-flop chain with the Q3·Q1 AND gate on the RED CLR line, and its 8, 9, sliver of 10, 0 timeline; line "AND gate + clear: count 0 to 9".
> On {next}, the grid clears. Teaser: s3's three flip-flops reappear, their clock inputs rewired to one YELLOW CLK line, and the three outputs change together on one edge; on {logic}, a BLUE box marked "?" appears in front of their inputs, with "Part 5 · Designing a synchronous counter".
> Hold the end card for about eight seconds after the last word; the music carries it.

[c4.recap.1] {recap} Let's recap. {r1} A counter steps through a fixed sequence of states, one step at every edge of the clock. An N-bit binary counter has two to the N states. {r2} A ripple counter chains toggling flip-flops, each clocked by the output of the one before. {r3} Each one flips when the bit before it falls, one delay later, and together they count.

[c4.recap.2] {r4} But those delays add up, so the count passes through false values on its way, and the clock speed is limited. {r5} Each output halves the frequency, which is why counters are also dividers. {r6} And an and gate on the clear inputs cuts the count short, so it counts from zero to nine.

[c4.recap.3] {next} Next time, the synchronous counter, the design this course recommends. One clock goes to every flip-flop, so they all change together. {logic} The price is some extra logic, to work out what each flip-flop should become. {pause}
