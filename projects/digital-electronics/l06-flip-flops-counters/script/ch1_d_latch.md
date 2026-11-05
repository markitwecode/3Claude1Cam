# Chapter 1 · Clocks and the transparent D latch

Digital Electronics · Lecture 6 (Flip-flops and Counters), part 1 of 6. Source: slides (combined_26.pdf) pp. 84–86, refresher pp. 79–81; recording 00:05:40–00:10:52, Yenka demo 00:21:36–00:23:16.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card on {title}: "Flip-flops and Counters", under it "Digital Electronics · Lecture 6", then the part line "Part 1 · Clocks and the transparent D latch". Clear it on {grid}.
> Hero: a 4 × 4 grid of one-bit memory cells, centre (small rounded squares, each showing a 0 or a 1; GREEN bright for 1, dim for 0). On {scatter} the cells flip one at a time at scattered, irregular moments: a restless flicker with no pattern.
> On {clock} a YELLOW square wave slides in along the bottom (the lecture's clock style: flat high and low levels, sharp edges, small up-arrows on the rising edges). On {together} the flicker stops: cells change only as a rising edge passes a thin vertical guide line, and every cell due to change flips on that edge at once. Run several beats.
> On {question} the question appears above the grid in YELLOW: "How do we make a memory change only when the clock says so?"
> On {road} grid and wave clear to a road of three boxes, left to right with arrows: "latch" → "flip-flop" → "counter", lit one by one on {latch}, {flipflop}, {counter}. On {start} "latch" stays lit in YELLOW, the other two dim, and "transparent D latch" appears under it.

[c1.hook.1] {title} Welcome to lecture six of Digital Electronics, on flip-flops and counters. {grid} Here's a grid of one-bit memories. Each one holds a zero or a one, {scatter} and each changes the instant its own inputs change. So they flip at scattered moments, whenever their inputs happen to arrive. {pause}

[c1.hook.2] {clock} Now bring in a clock, a signal that beats steadily, like a metronome. {together} If every memory waits for the beat, they all change at the same moment. {question} So here's the question for this part. How do you make a memory change only when the clock says so? {pause=1.5}

[c1.hook.3] {road} This lecture gets there in three steps. {latch} First a latch, {flipflop} then a flip-flop, {counter} and then a counter, built from flip-flops. {start} Today is step one, the transparent dee latch.

## Scene 2 · Last time: the RS latch (ch1_s2_rslatch)

> Small header "Last lecture" on {recap}. On {bistable} a single memory cell (from s1's grid) with the labels "bistable" and "state" (slide p. 79).
> Hero, centre-left (the cell makes way for it on {circuit}): slide p. 79's NOR RS latch. Two distinctive-shape NOR gates with output bubbles, gate 1 on top and gate 2 below (small "1" and "2" inside, as on slide p. 80), outputs cross-coupled. R (BLUE) enters gate 1, whose output is Q (GREEN); S (BLUE) enters gate 2, whose output is Q̄ (GREEN). Labels light on {inputs} and {outputs}. This exact drawing is reused inside the D latch in s5, and in the s7 recap.
> On {nor}, slide p. 80's NOR truth table at the right: header `a b | y`, rows `0 0 | 1`, `0 1 | 0`, `1 0 | 0`, `1 1 | 0`. On {always} rows 3–4 get a bracket "always 0"; on {comp} rows 1–2 get "b complemented".
> The walk, in the slides' order (pp. 80–81), on the circuit: wires at 1 bright, at 0 dim, and each gate tagged with its condition as it applies ("always 0" / "complement"). {reset}: R = 1, S = 0; gate 1 "always 0", Q = 0. {reset2}: gate 2 "complement", Q̄ = 1; tag "reset". {hold}: R back to 0; the 1 travelling back from Q̄ keeps gate 1 at 0; nothing changes; tag "hold".
> {set}: S = 1; gate 2 "always 0", Q̄ = 0. {set2}: gate 1 sees 0 and 0, Q = 1; tag "set". {illegal}: S = R = 1; both gates "always 0"; Q = 0 and Q̄ = 0, both in RED. {contra}: "Q = Q̄ ?!" in RED, tag "illegal".
> On {table} the NOR table makes way for slide p. 79's table, verbatim, rows building in order: header `S R | Q′ Q̄′ | comment`, rows `0 0 | Q  Q̄ | hold`, `0 1 | 0  1 | reset`, `1 0 | 1  0 | set`, `1 1 | 0  0 | illegal` (illegal row RED). On {prime} the line under it: "Where Q′ is the next state and Q is the current state".
> On {async} S pulses at an arbitrary moment and Q answers at once, no waiting; on {name} the caption "asynchronous operation" (slide p. 84).
> Checked: the NOR table, and the latch settled from both starting states for all four S R inputs, by enumeration in Python 3.11.9. The lecturer says "both equal to one" for S = R = 1 (00:08:26); slide p. 81 and the check give Q = Q̄ = 0, so show 0.

[c1.rs.1] {recap} First, a quick reminder from last lecture. {bistable} A memory that holds one bit is called a bye-stable, and the bit it holds is its state. {circuit} Here's the bye-stable you met, the reset-set latch. It's two nor gates, each feeding its output back into the other. {inputs} It has two inputs, ar, which stands for reset, and ess, which stands for set, {outputs} and two outputs, cue and not cue, which should always be opposites.

[c1.rs.2] {nor} It all follows from two facts about a nor gate. {always} If either input is one, the output is zero, whatever the other input does. The slide calls this always zero. {comp} If one input is zero, the output is the complement of the other input. {pause}

[c1.rs.3] {reset} Make input ar one, and input ess zero. Gate one has a one coming in, so cue is zero. {reset2} Gate two now sees two zeros, so not cue is one. That's reset. {hold} Now drop ar back to zero. Gate one still sees the one coming back from not cue, so cue stays at zero. Nothing changes. That's hold.

[c1.rs.4] {set} Make ess one instead. Now gate two is forced to zero, so not cue is zero, {set2} and gate one sees two zeros, so cue becomes one. That's set. {illegal} And if both inputs are one? {pause} Both gates are forced to zero, so cue and not cue are both zero. {contra} A signal and its complement, equal. That's a logical contradiction, so this input is called illegal.

[c1.rs.5] {table} Here's the whole story as a table. {prime} Cue prime is the next state, and plain cue is the current state. {async} Notice one more thing. This latch's output changes directly, the moment its inputs change. {name} That's called asynchronous operation.

## Scene 3 · The clock (ch1_s3_clock)

> On {sync} the RS latch shrinks to the top-left corner with "asynchronous" under it; "synchronous" appears top-right. On {rule} slide p. 84's line under it: "outputs change only at a time specified by a global enabling signal"; on {name} "the system clock" in YELLOW.
> Hero, across the middle: a large YELLOW square wave labelled CLK, flat levels and sharp vertical edges, in the lecture's timing-diagram style (s1's wave, enlarged; ch2–ch4 reuse it).
> {levels}: dashed horizontal guides labelled "high" and "low". {period}: a GOLD double-headed arrow over one full cycle, rising edge to the next rising edge, labelled "period". {freq}: GOLD "frequency = 1 / period". {example}: GOLD "1 ms → 1000 Hz = 1 kHz" (checked).
> {edges}: the vertical edges glow. {rising}: small YELLOW up-arrows on every rising edge, label "rising edge (positive-going)". {falling}: down-arrows on the falling edges, label "falling edge (negative-going)". Keep the arrows: they are the lecture's edge markers from here on.
> {for}: slide p. 85's heading "The Clock: What is it and what is it for?"; {order} "It imposes order on the state changes"; {together} "Allows lots of states to appear to update simultaneously", with a small copy of s1's grid flipping together as a rising edge passes.
> {question}: the corner RS latch comes back beside the clock with a YELLOW "?" between them, and slide p. 85's question: "How can we modify an asynchronous circuit to act synchronously, i.e., in synchronism with a clock signal?"

[c1.clock.1] {sync} But virtually every sequential circuit in use today works another way, called synchronous operation. {rule} Its outputs may change only at times set by one global enabling signal. {name} That signal is the system clock. {pause}

[c1.clock.2] {wave} A clock is typically a square wave at a fixed frequency. {levels} It sits at a high level, then a low level, over and over. {period} The time for one full cycle is called the period, {freq} and the frequency is one over the period. {example} So a period of one millisecond means a thousand cycles every second, one kilohertz.

[c1.clock.3] {edges} The moments where the clock signal switches are called edges. {rising} Going from low to high is a rising edge, also called positive-going. {falling} Going from high to low is a falling edge, or negative-going. {pause} You'll hear these words for the rest of the lecture.

[c1.clock.4] {for} So what is the clock for? {order} It imposes order on the state changes. {together} And it lets lots of states appear to update simultaneously, like our grid of memories, changing on the beat. {question} Which leaves the slide's question. How can we make an asynchronous circuit, like the ar-ess latch, act in step with a clock? {pause}

## Scene 4 · An AND gate as a valve (ch1_s4_andgate)

> Hero, centre-left: one distinctive-shape AND gate, inputs a (top) and b (bottom) in BLUE, output y in GREEN; wires bright at 1, dim at 0. On {table}, slide p. 86's AND truth table at the right, verbatim: header `a b | y`, rows `0 0 | 0`, `0 1 | 0`, `1 0 | 0`, `1 1 | 1`; on {one} the last row highlights.
> Above the gate, two short traces in the s3 timing style: b on top, y below.
> {block}: a is held at 0 (a small switch showing 0, wire dim); b's trace wiggles (a few irregular pulses) and the pulses travel along b's wire to the gate and stop there. {stuck}: y's trace stays flat at 0; rows `0 0` and `0 1` light; label "blocked".
> {pass}: a's switch flips to 1 (wire bright). {copy}: the same wiggle on b now passes through, and y's trace copies b's exactly, edge for edge; rows `1 0` and `1 1` light; label "passes".
> {valve}: a valve sits on the gate's b-to-y path, with a as its handle: {closed} "a = 0: closed", {open} "a = 1: open".
> {plan}: two small copies of the AND gate slide toward the shrunken RS latch from s2, one at R and one at S: the set-up for s5.

[c1.valve.1] {tool} The answer starts with a trick you've used a few times already. Use an and gate to pass or block a signal. {table} Here's its truth table, with one input on top and one below. {one} The output is one only when both inputs are one.

[c1.valve.2] {block} Hold the top input at zero, and let the bottom input wiggle. {stuck} The output stays at zero, whatever the bottom input does. The signal is blocked. {pause} {pass} Now hold the top input at one. {copy} The output copies the bottom input exactly, rising when it rises and falling when it falls. This time the signal passes.

[c1.valve.3] {valve} So one input decides whether the other gets through, like a valve. {closed} A zero closes the valve. {open} A one opens it. {pause} {plan} Put valves like this in front of the latch's inputs, and we get to decide when the latch is allowed to listen.

## Scene 5 · From RS latch to D latch (ch1_s5_dlatch)

> On {start} s2's RS latch drawing (same gates, labels and colours) sits right of centre. On {ands} two AND gates grow in front of it, one feeding R and one feeding S, their outputs labelled R and S as on slide p. 86. On {en} a new BLUE input EN enters between them and branches to one input of each AND. On {clk} a YELLOW tag "could be the clock" hangs on EN.
> For now the ANDs' other inputs are two separate BLUE input wires, one per gate, each with a small toggle switch.
> {off}: EN = 0, wire dim; the valves from s4 shut. {zeros}: pulses on the two inputs stop at the ANDs; R and S read 0; the latch is tagged "hold". {frozen}: Q and Q̄ stay as they are. {on}: EN = 1, wire bright; the pulses pass straight through to R and S. {split}: two short labels, "EN: when" and "inputs: what".
> {danger}/{both}: both inputs go to 1, so R = S = 1; {illegal}: s2's RED "Q = Q̄ = 0" flashes on the latch.
> {d}: the two inputs merge into one BLUE input D at the bottom left, laid out exactly as slide p. 86: {direct} D runs straight to the S gate; {inv} a branch goes up through an inverter (triangle with a bubble) to the R gate.
> {comp}: with EN = 1, tags "S = D" and "R = D̄" at the AND outputs; D toggles 0, 1, 0 and R and S light alternately, never together. {never}: "R and S never both 1" in GREEN. {safe}: a small copy of s2's table with its RED illegal row struck through; {gone} it fades out.
> Checked by enumeration in Python 3.11.9: for every D, EN and starting Q, R = EN·D̄ and S = EN·D are never both 1, EN = 0 always gives R = S = 0, and the gated RS latch without D (EN = 1, both inputs 1) does reach R = S = 1.

[c1.dlatch.1] {start} Start from the ar-ess latch, exactly as before. {ands} Put an and gate in front of input ar, and another in front of input ess. {en} Both gates are controlled by one new input, called enable. {clk} Enable could be the system clock itself.

[c1.dlatch.2] {off} When enable is zero, both valves are shut. {zeros} The gates force ar and ess to zero, whatever comes in, and both at zero is the hold condition. {frozen} So the latch keeps its state. {on} When enable is one, both valves are open, and the inputs go straight through to ar and ess. {split} Enable now decides when the latch may change, and the inputs decide what it changes to.

[c1.dlatch.3] {danger} But one danger is left. {both} With enable at one, the inputs pass straight through, so nothing stops someone from setting both of them to one, {illegal} and that's the illegal state again, with cue and not cue both zero. {pause} Can we make it impossible? {pause}

[c1.dlatch.4] {d} Here's the trick. Replace the two inputs with a single data input, called dee. {direct} It goes straight to the set gate, {inv} and through an inverter to the reset gate. {comp} So with enable at one, ess equals dee, and ar equals not dee. {never} They're always complements of each other, so they can never both be one. {pause} {safe} The illegal state is now impossible, by construction. {gone} Nobody has to remember to avoid it. The wiring itself rules it out.

## Scene 6 · Transparent while enabled (ch1_s6_transparent)

> s5's finished D latch circuit, smaller, on the left. On {table} slide p. 86's table builds on the right, verbatim, one row per beat: header `D EN | Q′ Q̄′ | comment`; {hold} `X 0 | Q  Q̄ | RS hold`; {reset} `0 1 | 0  1 | RS reset`; {set} `1 1 | 1  0 | RS set`. As each row lands, the circuit's wires show it (bright 1, dim 0).
> {read}: the slide's line under the table: "See Q follows D input provided EN=1. If EN=0, Q maintains previous state", lit in two halves on {follow} and {keep}.
> {name}: the word "transparent"; with EN = 1, a glowing path runs from D through the gates to Q, as if one straight wire joined them. {modes}: two labels, "transparent mode: EN = 1" and "hold mode: EN = 0".
> {symbol}: the circuit folds into slide p. 86's symbol: a tall box, D on the left, Q on the right, EN coming in from below. {square}: the small square where EN meets the box pulses, label "level-triggered". (ch2 puts two of these boxes side by side.)
> {demo}: the symbol opens back into the full gate circuit, compact, in the top half, with toggle switches on D and EN (BLUE) and LEDs on Q and Q̄ (GREEN, lit for 1). Below it an EN / D / Q timing diagram builds step by step as the switches move, 10 equal steps (the s3 style, without edge arrows since EN is a level): EN `0 0 1 1 1 1 1 0 0 0`, D `1 0 0 1 1 0 0 0 1 1`, Q `1 1 0 1 1 0 0 0 0 0`; Q̄ is Q's complement throughout.
> Beats: {setup} step 0, Q = 1, D = 1, EN = 0 (Q's LED lit). {dflip} step 1, D → 0; {nothing} both LEDs unchanged, tag "hold". {enup} step 2, EN → 1; {jump} Q → 0, the LEDs swap. {wiggle} steps 3 and 5, D → 1 then D → 0; {tracks} Q follows each. {endown} step 7, EN → 0; {freeze} Q stays 0. {ignore} step 8, D → 1; Q stays 0.
> {wave}: a pale band shades the EN-high stretch (steps 2–6) across all three traces: inside it Q copies D, outside it Q is flat. {level}: label the band "level-triggered". This band is "the window" in ch2 s1, and returns in s7.
> Checked: the table and the whole 10-step sequence were simulated at gate level (AND, inverter, cross-coupled NOR) in Python 3.11.9. The sequence follows the lecturer's Yenka run ("d_latch": Q lit, D 1 → 0 with no effect, EN up and Q drops to 0), extended by the PLAN's wiggle and freeze. His simulator labels the enable switch CLK and draws 1s in red; keep RED for trouble.

[c1.transp.1] {table} Here's the table for the new latch. {hold} When enable is zero, dee can be anything, so it's marked ex, for don't care. The latch is in the ar-ess hold condition, and cue keeps its value. {reset} When enable is one and dee is zero, the reset input is one, so the latch resets. Cue prime is zero, and not cue prime is one. {set} When enable is one and dee is one, the set input is one, so the latch sets. Cue prime is one, and not cue prime is zero.

[c1.transp.2] {read} Read the table this way. {follow} While enable is one, cue follows dee. {keep} While enable is zero, cue keeps its previous state. {name} That's why it's called transparent. With enable at one, whatever you put on the input appears at the output, as if a plain wire joined them. {pause} {modes} So the latch has two modes, transparent while enable is one, and holding while enable is zero.

[c1.transp.3] {symbol} The latch gets its own symbol, a box with dee going in, cue coming out, and enable coming in from below. {square} The small square on the enable input means the device is level-triggered. You'll see what that means in a moment.

[c1.transp.4] {demo} Let's try it, the way the lecturer did in a simulator, with switches on dee and enable, and lights on cue and not cue. {setup} Cue starts at one, dee is one, and enable is zero. {dflip} Switch dee to zero. {nothing} Nothing happens, because the latch is holding. {pause} {enup} Now raise enable. {jump} At once, cue drops to zero, to match dee.

[c1.transp.5] {wiggle} With enable still high, flick dee up, then down again. {tracks} Cue follows every change. {endown} Now drop enable. {freeze} Cue freezes at zero, {ignore} and when dee goes back up, cue ignores it. {wave} Underneath, the waveform tells the same story. Cue tracks dee for the whole stretch where enable is high. {level} The latch responds to the level of enable, high or low, so it's called level-triggered.

## Scene 7 · The catch, recap and next (ch1_s7_recap)

> {catch}: s6's EN / D / Q waveform with its shaded band returns, centre. {window}: D gets a quick flurry of extra wiggles inside the band, every one reaching Q; the band tints RED, label "still responding". {want}: beside it, CLK (YELLOW) with a single up-arrow on one rising edge, label "one instant".
> Recap: clear to a row of five small tiles, each a small version of the visual that taught the idea (same objects, colours and styling) with its line under it, appearing on {r1} … {r5}:
> {r1}: s2's NOR latch beside its four-row table, illegal row RED, line "RS latch: remembers a bit, asynchronously".
> {r2}: s3's YELLOW clock with up- and down-arrows on its edges, line "Clock: edges mark when to change".
> {r3}: s4's AND gate, a = 0 blocking and a = 1 passing, line "AND: 0 blocks, 1 passes".
> {r4}: s5's D latch circuit with "R and S never both 1" in GREEN, line "D latch: illegal state impossible".
> {r5}: s6's EN / D / Q waveform with the band, line "Transparent while EN = 1: level-triggered".
> {next}: the tiles dim; two latch symbols (s6's box, small square on EN) slide together side by side, and a YELLOW up-arrow on a rising clock edge appears under them, with "Next: the master-slave D flip-flop". Then the end card, held ~8 s after the last word while the music carries it.

[c1.recap.1] {catch} There's a catch, though. {window} The whole time enable is one, the latch is still responding to its inputs. {want} What we'd really like is for the output to respond at one instant, such as a rising edge of the clock. {pause}

[c1.recap.2] {recap} Let's recap. {r1} The reset-set latch remembers one bit, but it changes the moment its inputs do, and both inputs at one is illegal. {r2} A clock is a square wave, and its rising and falling edges are the moments things may change. {r3} An and gate acts as a valve. A zero blocks, and a one passes. {r4} Gate the latch with enable, and feed it dee and not dee, so ar and ess are never both one. {r5} And that's the transparent dee latch. While enable is one, cue follows dee, so it's level-triggered.

[c1.recap.3] {next} Next time, two of these latches, back to back, make a flip-flop that changes only on the clock's rising edge. {pause}
