# Chapter 3 · Starting in a used state

Digital Electronics Lecture 10 (State Assignment), part 3 of 6. Source: the ring demo in the recording (00:25:40–00:29:59); slides p. 137 (the ring), pp. 127–128 (Lecture 9's "FSM Problems", refresher) and p. 91 (Lecture 6's asynchronous inputs).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch3_s1_hook)

> On {title}, the title card: "State Assignment", "Digital Electronics · Lecture 10", "Part 3 · Starting in a used state".
> On {ring}, ch2's ring of five carried over (ch2 s5–s6): five D flip-flops a, b, c, d, e left to right on one CLK line (YELLOW), each Q wired to the next D, and e's Q fed back along the top into a's D, as in the lecturer's simulation. No gates anywhere. Small tag beside it, the ring's scoreboard row from ch2 s7: "ring · 5 flip-flops · no gates".
> On {run}, a GREEN LED under each Q, all dark, and below the circuit the waveform panel (ch1 s5's style): CLK (YELLOW) starts ticking, "1 Hz", and the output trace "output = b" (GREEN) draws along with it.
> On {flat}, the GREEN trace runs flat along 0 while CLK keeps ticking. On {ghost}, a faint dashed ghost of the wanted wave (high for two periods, low for three, ch1 s5's waveform) appears behind the flat line.
> On {why}, a YELLOW "?" over the flat line. On {start}, a small label under the circuit: "where does a machine start?"

[c3.hook.1] {title} This is part three of our lecture on state assignment. {pause} {ring} Last time, we built the ring of five. Five flip-flops in a loop, with no logic at all. On every edge of the clock, each one simply passes its bit to the next.

[c3.hook.2] {run} So let's do what the lecturer did, and switch it on. The clock ticks away, once a second. {flat} But the output just sits at zero. {ghost} It should be high for two periods and low for three. Instead, nothing happens. {pause}

[c3.hook.3] {why} The table was right, and so is every wire. So why does it do nothing? {pause} {start} The answer is about where a machine starts. And it matters for every state machine you'll ever build.

## Scene 2 · All zeros (ch3_s2_stuck)

> The ring circuit from s1 stays, CLK still ticking, output still flat. On {ask}, a speech bubble over the circuit: "Why isn't this working?". On {think}, a YELLOW "?" over each of the five flip-flops. On {student}, a second bubble from below, the student's words (00:26:54): "We need to initialise it into one of the used states."
> On {zeros}, under each flip-flop its Q as a GREEN digit, all 0, and a readout in table order (e d c b a): "state = 00000".
> On {shift}, one edge of the clock (YELLOW tick): each 0 slides along its wire to the next flip-flop, and e's 0 travels round the top back into a. On {same}, the digits read 0 0 0 0 0 again; the readout flashes "00000 → 00000". On {forever}, two more edges, faster, each landing on 00000.
> On {table}, the circuit shrinks left and ch2 s6's table of the ring comes in (slide p. 137): "Current state e d c b a → Next state e′ d′ c′ b′ a′": 00011 → 00110, 00110 → 01100, 01100 → 11000, 11000 → 10001, 10001 → 00011, with "Unused states. Lots!" under it. On {rows}, the two adjacent 1s in each row glow GOLD.
> On {missing}, a DIM row "00000 → ?" slides along the table's left edge looking for a match, and finds none.
> On {nothing}, the five rows get a GREEN tick each; the DIM row stays outside the table.

[c3.stuck.1] {ask} The lecturer put that question to the room. Why isn't this working? {think} Before you hear the answer, think about what the five flip-flops hold when the simulation starts. {pause=1.5} {student} A student answered. "We need to initialise it into one of the used states."

[c3.stuck.2] {zeros} Look at what the flip-flops hold. The simulator starts every one of them at zero, so the state is zero, zero, zero, zero, zero. {shift} Now give it an edge of the clock. Each flip-flop copies the one before it, and every one of those holds a zero. {same} So the next state is all zeros again. {forever} And so is the one after that. A ring of zeros just shifts zeros into zeros, for ever.

[c3.stuck.3] {table} Now go back to the table we designed it from. {rows} It has five rows, one for each used state, and each one holds two ones, side by side. {missing} All zeros is missing. {pause} The counters in parts one and two also started at all zeros, and they ran, because for them all zeros was a used state. {nothing} So nothing in the design is wrong. The table only promised what happens in those five states, and the machine never got into one of them.

## Scene 3 · The power-up problem (ch3_s3_powerup)

> On {recall}, the lecturer's words "Remember, I said…" as a caption, then slide p. 127's heading "FSM Problems". On {power}, a power switch flips on beside three flip-flops with GREEN LEDs; their Q values flicker and settle at random (say 1, 0, 1). Caption from p. 127: "The state of the FFs could by chance be in one of the unused states".
> On {stuck}, an abstract sketch: a ring of four GREEN used states, and outside it two DIM circles with RED arrows between them, going round and round, never into the ring. Caption from p. 127: "stuck in some unanticipated sequence of states which never goes back to a used state".
> On {remedies}, p. 128's question "What can be done?", then its three remedies as three numbered cards side by side, slide wording. On {one}, "1 · Check to see if the FSM can eventually enter a known state from any of the unused states"; on {two}, "2 · If not, add additional logic to do this, i.e., include unused states in the state transition table along with a valid next state"; on {three}, "3 · Alternatively use asynchronous Clear and Preset FF inputs to set a known (used) state at power up". On {selfstart}, card 1 gets a GREEN tag "self-starting".
> On {traffic}, the cards shrink to the top and card 1 stays lit. ch1 s3's traffic light comes back: its four states in a ring with their lamps and codes (R A G order): red 100, red-and-amber 110, green 001, amber 010. On {codes}, the four unused codes 000, 011, 101, 111 appear as DIM circles outside the ring.
> On {feed}, p. 128's table "Start state | Next state logic output" builds one row per mark, each row also drawing an arrow from its DIM circle into the ring: {r1} 000 → 010 (amber), {r2} 011 → 100 (red), {r3} 101 → 110 (red-and-amber), {r4} 111 → 001 (green).
> On {all}, p. 128's bracket "Which are all valid states", then "So it does self start" in GREEN. All four rows checked with Lecture 9's logic D_R = R ⊕ A, D_A = Ā, D_G = R·A (Python 3.11.9, all eight states).

[c3.power.1] {recall} The lecturer tied this back to the lecture before this one, which our series skips. So here's the idea in brief. {power} When you switch a circuit on, each flip-flop comes up in a state nobody chose. So the machine can start in any pattern at all, including an unused one. {stuck} From there, it might get stuck in some sequence nobody planned, one that never goes back to a used state. {pause}

[c3.power.2] {remedies} The slides give three things you can do about it. {one} First, check. From every unused state, does the machine eventually reach a used state? {selfstart} If it does, the machine is called self-starting, and all is well. {two} Second, if not, add logic. Put the unused states into the transition table, each with a valid next state. {three} Third, use the flip-flops' asynchronous clear and preset inputs, to set a known used state at power-up.

[c3.power.3] {traffic} Lecture nine ran that check on its traffic light. {codes} You saw its codes in part one. Three flip-flops, one per lamp, so four patterns are unused. {feed} Feed each one into the next-state logic, and see where it goes. {r1} Zero, zero, zero goes to amber. {r2} Zero, one, one goes to red. {r3} One, zero, one goes to red-and-amber. {r4} And one, one, one goes to green. {all} Every unused state leads straight into the cycle. So the traffic light is self-starting. {pause}

## Scene 4 · Do our counters self-start? (ch3_s4_check)

> Left half: ch1's binary counter as the five-state ring (L6 `state_ring()` style), codes 000, 001, 010, 011, 100 at the nodes (GREEN, table order c b a), its logic beside it, small: D_a = ā·c̄, D_b = a ⊕ b, D_c = a·b (D's BLUE). On {unused}, the unused states 101, 110, 111 appear as DIM circles outside the ring, each with a small number tag 5, 6, 7 (the ring's nodes get tags 0 to 4 the same way).
> On {feed}, 111 is fed in: a = 1, b = 1, c = 1 substituted into each equation in turn, giving D_a = 0, D_b = 0, D_c = 1. On {lands}, the result assembles as c′ b′ a′ = 100 and an arrow draws from the DIM 111 to the ring's 100 node.
> On {rest}, the other two arrows draw: 101 → 010 and 110 → 010, with D_b = 1 lit in both substitutions. On {next}, all three arrows pulse together, one edge each. On {selfstart}, a GREEN "self-starting" tag under the binary ring.
> On {slide}, the right half: ch2's sliding counter the same way, ring 000, 001, 011, 110, 100 and logic D_a = b̄·c̄, D_b = a, D_c = b, with DIM 010, 101, 111 outside. On {quick}, arrows 010 → 100 and 111 → 110. On {through}, 101 → 010 draws DIM to DIM, then 010 → 100; a dot travels the two-step path.
> On {eventually}, card 1 from s3, small at the top, with its word "eventually" lit YELLOW. GREEN "self-starting" under the sliding ring too.
> On {luck}, both rings shrink up. ch1 s7's K-map for D_c comes in (rows c, columns b a in Gray order, X's at 101, 110 and 111, the loop a·b round 011 and the X at 111). On {xs}, the looped X turns into a 1 and the two X's left out turn into 0s, caption "each X became whatever the loops made it". On {lucky}, a small "(by luck)" appears beside both "self-starting" tags.
> All arrows checked by feeding every unused state into each design's logic until it reached a used state (Python 3.11.9): binary 101 → 010, 110 → 010, 111 → 100; sliding 010 → 100, 101 → 010 → 100, 111 → 110.

[c3.check.1] Now let's run the check on our own counters, starting with part one's binary count. {unused} Its unused states are the codes for five, six and seven, which the count never reaches. {feed} Take seven, one, one, one. The input to flip-flop A is not see and not A, which is zero. The input to flip-flop bee is bee exclusive-or A, also zero. The input to flip-flop see is bee and A, which is one. {lands} So seven goes to one, zero, zero. That's four, a used state.

[c3.check.2] {rest} The same check sends five and six to two, which is also used. In both, only the input to flip-flop bee comes out as one. {next} So from every unused state, the binary counter rejoins its cycle on the very next edge. {selfstart} It's self-starting.

[c3.check.3] {slide} Now the sliding counter from part two. Its unused states are zero, one, zero, then one, zero, one, and finally all ones. {quick} Zero, one, zero goes to one, zero, zero. And the all-ones state goes to one, one, zero. Both are used. {through} But one, zero, one goes to zero, one, zero, which is unused too. One more edge takes it to one, zero, zero. {eventually} That still counts. The check asks whether the machine eventually reaches a used state, and passing through another unused state on the way is fine.

[c3.check.4] {luck} So both counters are self-starting. {pause} But nobody planned that. {xs} In the K-maps, every don't care we looped became a one, and every one we left out became a zero. We chose those loops to make the logic small, and they happened to send every unused state somewhere safe. {lucky} This time we were lucky. That's why you always check.

## Scene 5 · The ring's trap (ch3_s5_loops)

> On {ring}, the ring's five flip-flops as five cells in a circle, labelled a to e, holding the pattern 00101 (e d c b a), its two 1s GOLD. On {rotate}, two edges: every bit moves one cell round, e's wrapping to a; the readout steps 00101 → 01010 → 10100. On {same}, the two GOLD 1s keep their gap; caption "same pattern, moved round".
> On {loops}, all 32 states as eight loops (each loop a small circle of dots, labelled with its first pattern). On {single}, 00000 and 11111, each a single dot with a self-arrow. On {five}, the six loops of five: 00001, 00011, 00101, 00111, 01011, 01111. On {count}, a GOLD "8 loops".
> On {ours}, the 00011 loop turns GREEN and opens up to show its codes: 00011 → 00110 → 01100 → 11000 → 10001. On {trap}, the other seven turn RED.
> On {flat}, beside the RED loops, output b under CLK for three of them: 00000 flat at 0, 11111 flat at 1. On {apart}, 00101's loop: b reads 0, 1, 0, 0, 1 and repeats (checked), drawn GREEN with a RED cross, next to the wanted wave (high two, low three).
> On {exactly}, the GREEN loop's codes again, the two GOLD 1s touching in each; caption "exactly two 1s, side by side".
> On {never}, the eight loops side by side with no arrow joining any RED loop to the GREEN one; caption "27 unused states: none reaches a used state". On {two}, s3's card 2 lights and gets a RED cross with the note "the ring's point: no logic". On {three}, card 3 lights YELLOW.
> Checked (Python 3.11.9, all 32 states): D_a = e, D_b = a, D_c = b, D_d = c, D_e = d give exactly these 8 loops (1 + 1 + 6 × 5 = 32); the 27 unused states never reach a used one.

[c3.loops.1] {ring} And what about the ring of five? {pause} Think about what a ring does. {rotate} On every edge, each bit moves one place along, and the last one wraps round to the first. {same} So the pattern never changes. It only moves round. The number of ones stays the same, and so do the gaps between them.

[c3.loops.2] {loops} That splits all thirty-two patterns into separate loops. {single} All zeros stays all zeros, and all ones stays all ones. {five} Every other pattern goes round a loop of five, and there are six of those. {count} That's eight loops in all. {ours} Only one of them is ours, the loop with two ones side by side. {trap} The other seven are traps.

[c3.loops.3] {flat} Each trap gives the wrong output, for ever. All zeros gives a flat zero, and all ones a flat one. {apart} Others are worse. Take two ones with a gap between them. The output goes high for one period, low for one, high for one, then low for two. {exactly} So the ring must hold exactly two ones, and they must be next to each other.

[c3.loops.4] {never} And none of the twenty-seven unused states ever reaches a used one. {pause} So the ring can never start itself. {two} The second remedy, adding logic, would throw away the ring's whole point, which is having no logic at all. {three} That leaves the third. Put the ring into a used state, by force.

## Scene 6 · Asynchronous set, active low (ch3_s6_preset)

> The ring circuit from s1–s2, all LEDs dark, state 00000. On {switch}, a switch in the CLK line (L6 `toggle`) opens: the YELLOW clock source keeps ticking, but the line after the switch goes dark. Caption "clock disconnected".
> On {lecture6}, one flip-flop comes forward to the centre, enlarged, labelled "74HC74" as in the simulation. On {pins}, two RED pins grow out of it: S on top and R underneath (L6 ch3 s6's `pin()`, there labelled PRE and CLR). Captions from p. 91: "Preset/Set – force Q to 1" by S, "Reset/Clear – force Q to 0" by R. On {now}, "take effect independently of any clock or enable inputs".
> On {bubble}, a YELLOW circle highlights the small bubble where S meets the box. On {low}, caption "active low: 0 = do it".
> On {idle}, beside S a push button and S's level as a digit, 1. On {press}, the button goes down, S drops to 0 (RED), and on {jump} Q jumps to 1 at once (its GREEN LED lights), with no clock edge anywhere. On {release}, the button comes up and S returns to 1; Q stays 1.
> On {held}, a ghost replay: S held at 0 while a CLK edge arrives with D = 0, and Q stays 1 (caption "held at 0: ignores D and the clock"). On {normal}, S back at 1, caption "normal D flip-flop".

[c3.preset.1] So how do you force a pattern into the flip-flops? {switch} The lecturer began by disconnecting the clock signal. He opened a switch on that wire, so nothing could shift while he worked. {lecture6} Then he used something you met in Lecture six. {pins} The flip-flops in the simulation are models of a real chip, and each one has a set input and a reset input. {now} These are asynchronous inputs. They act at once, whatever the clock is doing. Set forces cue to one, and reset forces cue to zero.

[c3.preset.2] {bubble} Now look closely at the set input. There's a little circle where it meets the box. {low} That circle means the input is active low. It does its job when you drive it to zero. {idle} So in normal use, set sits at one. In the simulation, a push button pulls it down while you press it.

[c3.preset.3] {press} To make cue go to one, you pull set down to zero. {jump} Cue jumps to one straight away, with no edge of the clock. {release} Then you let set go back to one, and cue stays at one. {held} That last step matters. Held at zero, set would keep cue at one, and the flip-flop would ignore whatever arrives at input dee. {normal} Back at one, it's a normal dee flip-flop again.

## Scene 7 · Into a used state (ch3_s7_restart)

> The full ring circuit again, clock switch open, all LEDs dark, readout "00000". On {setd}, flip-flop d's S pin pulses 1 → 0 → 1 (RED) and its LED lights GREEN, a GOLD 1 under it; readout "01000". On {sete}, the same for e; readout "11000".
> On {used}, the readout turns GREEN, "a used state", and ch2 s6's table (small, corner) lights its row 11000 → 10001.
> On {reconnect}, the switch closes and CLK (YELLOW) reaches all five flip-flops. On {run}, the two GOLD 1s step round the ring, the LEDs follow, and on {wave} the waveform panel from s1 draws output b (GREEN): from 11000 it reads 0, 0, 1, 1, 0, 0, 0, 1, 1, 0 (checked). It lands on ch1 s5's ghost wave, high for two periods, low for three.
> On {lessons}, two lines under the circuit: on {first}, "1 · This is what asynchronous set and reset are for."; on {second}, "2 · A machine must start in a used state." The flat-line trace from s1 flashes once beside line 2, small.
> On {startup}, the push buttons fade out. A power switch flips on, and on {pulse} one RED line pulses the set pins of d and e and the reset pins of a, b and c together; the LEDs come up 11000 at once. Caption from p. 91: "Often used to force a synchronous circuit into a known state, say at start-up." On {every}, three quick power-ups, each first flickering a different random pattern, then 11000.

[c3.restart.1] {setd} So the lecturer pressed the set button on flip-flop dee. Set went to zero, and cue went to one. Then he let set go back to one. {sete} Next, the same for its neighbour, flip-flop ee. {used} Now the ring holds two ones, side by side. One, one, zero, zero, zero. That's one of the five used states.

[c3.restart.2] {reconnect} Then he reconnected the clock signal. {run} The two ones step round the ring, {wave} and the output goes high for two periods, then low for three, high for two, low for three. {pause} That's exactly the divide-by-five waveform from part one. {lessons} He drew two lessons from this. {first} First, this is what asynchronous set and reset inputs are for. {second} Second, a machine has to start in one of its used states. Otherwise, this one would stay at zero for ever.

[c3.restart.3] {startup} In a real circuit, nobody stands by to press buttons. {pulse} As the slides put it, asynchronous inputs are often used to force a synchronous circuit into a known state at start-up. One pulse at power-up sets the last two flip-flops and resets the rest. {every} Whatever pattern they wake up in, the ring starts in a used state every time.

## Scene 8 · Recap and next (ch3_s8_recap)

> On {recap}, the heading "Recap". Six small panels in a 3 × 2 grid, each a small version of the visual that taught it (same objects, colours and styling), appearing on its sentence's mark with its short line under it.
> {r1}: s1's ring circuit with the flat GREEN output under the ticking CLK, "switched on, it sat at 0".
> {r2}: s2's five GREEN 0 digits with the edge arrow, "00000 → 00000".
> {r3}: s3's three remedy cards, tiny: "check · add logic · set a used state".
> {r4}: s4's two rings with DIM states leading in, "self-starting (by luck)".
> {r5}: s5's eight loops, one GREEN and seven RED, "8 loops, 1 ours".
> {r6}: s6's set pin with its bubble pulsing 1 → 0 → 1, and s7's wave (high two, low three) under it, "active-low set: start used".
> On {next}, the grid clears. A row of eight flip-flops with exactly one LED lit, the light (GOLD) stepping along it; caption "one flip-flop per state". On {real}, a small GREEN tag beside it, "used for real". Then the end card: hold about 8 s after the last word while the music carries it.

[c3.recap.1] {recap} Let's recap. {r1} Switched on, the ring of five did nothing. {r2} It started at all zeros, an unused state, and a ring of zeros only shifts zeros. {r3} At power-up, a machine can land in any unused state. You can check that it finds its own way back, add logic to make sure it does, or force it into a used state.

[c3.recap.2] {r4} Our two counters do find their way back, so they're self-starting, but only by luck. {r5} The ring never does. Its thirty-two patterns fall into eight loops, and only one is ours. {r6} So the lecturer forced it, with the active-low set inputs, and it ran. {pause}

[c3.recap.3] {next} Next time, a style that sounds just as wasteful, one flip-flop for every state. {real} But this one gets used for real. {pause}
