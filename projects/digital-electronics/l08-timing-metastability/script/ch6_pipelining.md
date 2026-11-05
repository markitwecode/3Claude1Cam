# Chapter 6 · Latency, throughput and pipelining

Digital Electronics, Lecture 8 (Timing, Metastability and Parallelism), part 6 of 7. Source: slides
(`combined_26.pdf`) pp. 115 (second slide, "Parallelism") to 117 (second slide, up to its circuit);
recording 00:37:51–00:44:52.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch6_s1_hook)

> Title card, centred: "Timing, Metastability and Parallelism", then "Digital Electronics · Lecture 8" under it, then "Part 6 · Latency, throughput and pipelining". It clears on {last}.
> {last}: a small copy of ch5 s5's trial table with its "3.04 ns | 384 days ≈ 1.05 years ✓" row ticked GREEN (checked: 3.04 ns gives 1.05 years), beside ch4 s5's synchroniser (two flip-flops on one YELLOW CLK line), whose YELLOW T_c arrow stretches longer. On {now} both slide off to the left.
> Hero ({box}): one wide rounded box, centre, labelled "the system", with GOLD "10 ns" above it. A conveyor line runs into its left side and out of its right. Tasks are small rounded squares in the task colours used through ch7 (task 1 BLUE, 2 GREEN, 3 TEAL, 4 FG, then repeating), queued on the left.
> {one}: the first square slides in, and a progress sweep fills the box left to right. {done}: it leaves on the right onto a small "done" pile. {next}: only now does the second square enter.
> {queue}: new squares keep arriving on the left faster than they leave, so the queue lengthens, with a small GOLD "waiting" count ticking up.
> {fixed}: the GOLD "10 ns" gets a thin box and the tag "fixed". {question}: a YELLOW "more tasks per second?" appears under the system box. Hold on it.

[c6.hook.1] {title} This is part six of our lecture on timing, meta-stability and parallelism. {last} Last time, we gave a synchroniser a longer clock period, on purpose. Just over three nanoseconds bought a year between failures. {now} Now we turn the other way, from reliable to fast.

[c6.hook.2] {box} Here's a system that works on one task at a time. Each task takes ten nanoseconds. {one} A task goes in, {done} and ten nanoseconds later it comes out. {next} Only then can the next task start. {queue} Meanwhile, more tasks keep arriving, and the queue keeps growing. {pause}

[c6.hook.3] {fixed} Those ten nanoseconds are fixed. That's simply how long the logic takes. {question} So how can the system get more tasks done each second, without making any single task faster? {pause=1.5}

## Scene 2 · Latency and throughput (ch6_s2_speed)

> s1's system box stays (the queue and "done" pile clear); three squares in task colours wait at its left.
> {token}: one square zooms up beside the box and opens into a small bundle: two BLUE input wires on its left, one GREEN output wire on its right, and the slide's definition under it: "token: a group of inputs that are processed to produce a group of outputs". {example}: GOLD "3" and "4" on the inputs, GOLD "7" on the output (an adder). It shrinks back into its square. {task}: the square gets the tag "task = processing one token".
> {latency}: YELLOW "latency" over the box. {watch}: a small stopwatch rides with one square from the box's left edge to its right edge; a dimension arrow across the box reads GOLD "10 ns".
> {throughput}: YELLOW "throughput" at the exit. {count}: squares pass the exit one by one and a tally clicks at each; GOLD "1 every 10 ns = 100 million per second".
> {mine} / {many}: two question cards appear, "How long for mine?" under "latency" and "How many per second?" under "throughput".
> {tied}: between the cards, GOLD "throughput = 1 / latency", with the small tag "for this box".
> {improve}: three squares light up inside the box at once. {parallel}: the word "parallelism" (BLUE) above it, which splits into two empty slots, "1" and "2". The slots carry into s3.

[c6.speed.1] {measure} First, we need words for speed. The slides measure it with tokens moving through the system. {token} A token is a group of inputs, processed together to produce a group of outputs. {example} Here's an example. Say the system adds pairs of numbers. Then a token is one pair going in, and its sum coming out. {task} Processing one token is one task.

[c6.speed.2] {latency} The latency is the time one token takes to pass through the system, from start to end. {watch} Follow one token with a stopwatch, and you get ten nanoseconds. {throughput} The throughput is the number of tokens produced per unit time. {count} Stand at the exit and count. One token every ten nanoseconds is a hundred million tokens per second.

[c6.speed.3] {two} These answer two different questions. {mine} Latency asks, how long until mine is done? {many} And throughput asks, how many get done each second? {tied} For this box, the two are tied together. The throughput is just one over the latency. {pause} {improve} But throughput improves if we process several tokens at the same time. {parallel} That's called parallelism, and it comes in two types.

## Scene 3 · Two kinds of parallelism (ch6_s3_twokinds)

> Opens on s2's two empty slots under "parallelism", left and right.
> {spatial}: slot 1 gets the title "spatial". s2's box moves into slot 1 and a second copy comes out of it (TransformFromCopy) underneath, each with its own square (BLUE, GREEN). {copies}: both squares exit together; GOLD "2 tasks every 10 ns" and a GOLD cost tag "× 2 hardware".
> {temporal}: slot 2 gets the title "temporal". One box splits along a vertical line into two half-width boxes labelled "stage 1" and "stage 2" (BLUE outlines). {spread}: squares fill them, task 1 (BLUE) in stage 2 while task 2 (GREEN) is in stage 1. {through}: a thin arrow traces task 1's route through stage 1, then stage 2. {overlap}: both stages light up at once, each holding a different colour.
> {pipelining}: under slot 2, "temporal parallelism = pipelining". {attractive}: GREEN "more throughput, same hardware" under slot 2, beside slot 1's GOLD "× 2 hardware".
> {bake}: the slots dim and shrink to the top. Simple icons: a tray of dough circles, a rolling pin, and an oven (a box with a window and a dial), with the two steps "roll" → "bake". {oven}: a second baker and a second oven appear beside the first, each baking its own tray: tag "spatial", linked to slot 1. {tray}: back to one oven, tray 1 baking (BLUE glow) while tray 2 (GREEN) is rolled: tag "temporal", linked to slot 2.

[c6.kinds.1] {spatial} The first type is spatial parallelism. Provide multiple copies of the hardware, so that multiple tasks can be done at the same time. {copies} Two copies of our box finish two tasks every ten nanoseconds. That's simple, but you pay for every copy.

[c6.kinds.2] {temporal} The second type is temporal parallelism. Break each task into a number of sequential stages, {spread} and spread several tasks over those stages. {through} Each task still passes through every stage, in order. {overlap} But at any given time, a different task is in each stage, so the tasks overlap. {pipelining} Temporal parallelism is often known as pipelining. {attractive} It's attractive because it can raise the throughput without duplicating hardware. The same stages simply stay busy more of the time.

[c6.kinds.3] {bake} Here's an everyday picture, from the textbook by David and Sarah Harris. You're baking trays of cookies. First you roll out a tray, and then it goes in the oven. {oven} If a friend with a second oven bakes a tray alongside yours, that's spatial parallelism. {tray} Roll out the next tray while the first one bakes, and that's temporal. Both steps are busy at once, with only one oven.

## Scene 4 · One task at a time (ch6_s4_nopipe)

> p. 116's second slide, rebuilt. The slides' letters stay on screen (A, B, task subscripts); the narration says "first stage" and "second stage", because the voice reads "ay" as "eye". {task}: top left, "Task" and a bar of two boxes side by side, "A" | "B", with a YELLOW T_c dimension arrow over both and a small legend beside it, "A = stage 1, B = stage 2" (s3's and ch7's on-screen names; the letters stay only because the slide's timelines use them). {result}: a small arrow from A's right edge into B, "A's result". {period}: GOLD "= 10 ns" under the T_c arrow, as s1's box splits into these two halves.
> {latency}: at the right, "Latency = T_c" (T_c YELLOW) lights, with a brace from A's left edge to B's right edge. {throughput}: "Throughput = 1/T_c" lights under it; {frequency} a small "= f_c, the clock frequency" joins it (ch1 s2's relation).
> {timeline}: the slide's timeline in one row: A₁ B₁ | A₂ B₂ | A₃, with dashed vertical guides at the period boundaries and a YELLOW T_c arrow over each period. Boxes take the task colours (task 1 BLUE, 2 GREEN, 3 TEAL): {t1} A₁ then B₁, {t2} A₂ then B₂, {t3} A₃.
> {look}: the row splits into two lanes, "first-stage hardware" (A₁, A₂, A₃) and "second-stage hardware" (B₁, B₂), each box keeping its time position, so each lane has gaps.
> {idle}: the gaps in both lanes fill with DIM hatching labelled "idle". Keep the lanes for s5.

[c6.seq.1] {example} Now the slides' example. {task} Here's a task that breaks down into two stages, a first stage and then a second stage. {result} The second stage works on the first stage's result. {period} Together they take one clock period. In our example, that's ten nanoseconds.

[c6.seq.2] Without pipelining, the second stage finishes at the end of the period. {latency} So the latency is one clock period. {throughput} And one task finishes every period, so the throughput is one over the clock period. {frequency} That's just the clock frequency, counted in tasks per second.

[c6.seq.3] {timeline} Now run several tasks. {t1} Task one runs its first stage, then its second. {t2} Only then does task two start, with its own first stage. {t3} Then task three, and so on. {pause} {look} Look at the hardware for the first stage. What is it doing while the second stage works? {pause} {idle} Nothing. It sits idle, waiting for the next task. And the second stage's hardware is just as idle, while the first stage works.

## Scene 5 · Overlapping tasks (ch6_s5_pipe)

> From s4's lanes, which merge back into one row. {start}: A₂ (GREEN) lifts out and slides back one stage-width to sit under B₁; the first-stage lane flashes YELLOW "free". {stair}: A₃ B₃ (TEAL) and A₄ B₄ (FG) follow, building p. 117's staircase: row 1 A₁ B₁, row 2 A₂ B₂, row 3 A₃ B₃, row 4 A₄ B₄, each row one stage-width to the right of the one above. Dashed guides at each stage boundary; the YELLOW T_c arrows above now span one stage box each, as on p. 117.
> {cols}: a YELLOW column highlight. {fill}: on the first column (A₁ alone). {c1}: B₁ + A₂. {c2}: B₂ + A₃. {c3}: B₃ + A₄. {each}: the slide's side note appears small at the left: "Each task passes through both stages, but a different task will be in each stage at any given time, i.e., multiple tasks can overlap".
> {two}: a GOLD brace under row 2 (A₂ B₂), "Latency = 2T_c". {thru}: GOLD ticks at the right ends of B₁, B₂, B₃, B₄, one per period, and "Throughput = 1/T_c".
> {puzzle}: s4's "Throughput = 1/T_c" flies in beside this one; both glow, with a YELLOW "?" between them. {period}: s4's T_c arrow (spanning A and B) is drawn over this staircase's T_c arrow (spanning one stage): the same symbol, half the length.
> Numbers here are ours, checked in Python 3.11.9: 1/10 ns = 100 million per second, 1/5 ns = 200 million per second, latency 2 × 5 ns = 10 ns; over 25 ns, finishes at 10 and 20 ns (top) and at 10, 15, 20 and 25 ns (bottom).
> {scale}: both timelines on one nanosecond axis, 0 to 25 ns, GOLD ticks every 5 ns. Top: s4's row A₁ B₁ A₂ B₂ A₃, "T_c = 10 ns". Bottom: the staircase, "T_c = 5 ns". Every stage box is 5 ns wide in both, as on the slides.
> {ten}: GOLD finish ticks on the top row at 10 and 20 ns, "1 every 10 ns: 100 million / s". {five}: on the staircase at 10, 15, 20 and 25 ns, "1 every 5 ns: 200 million / s". {latency}: the same GOLD "10 ns" brace over task 2 in each timeline. {untied}: s2's GOLD "throughput = 1 / latency" returns small at the side and is struck through.
> {lecturer}: under the bottom timeline, "latency: 1 period → 2 periods" with a GOLD "× 2". {ns}: beside it, "in ns: 10 → 10 (ideal)", then a small "real circuit: a little more".

[c6.pipe.1] {free} Pipelining puts that idle time to work. {start} As soon as task one leaves the first stage, that hardware is free. So task two starts its first stage right away, alongside task one's second stage. {stair} Task three follows one step behind task two, and task four behind task three. The timeline becomes a staircase.

[c6.pipe.2] {cols} Read it one column at a time, as the lecturer does. {fill} In the first period, only task one is inside. {c1} In the next, tasks one and two. {c2} Then tasks two and three. {c3} Then three and four. {pause} {each} Every task still passes through both stages, but there's a different task in each stage at any given time.

[c6.pipe.3] {lat} So what are the latency and throughput now? {pause} {two} Each task spends one clock period in each stage, so the latency is two clock periods. {thru} But once the pipe is full, a task finishes at the end of every period. So the throughput is one over the clock period.

[c6.pipe.4] {puzzle} Wait. That's the same throughput as before, one over the clock period. So what did we gain? {pause=1.5} {period} The clock period itself changed. Before, one period had to fit both stages. Now it only has to fit one stage, so it's about half as long.

[c6.pipe.5] {scale} Draw both timelines to the same time scale. {ten} Without pipelining, the period is ten nanoseconds, so a task finishes every ten. That's a hundred million per second. {five} With it, the period is five nanoseconds, and a task finishes every five. That's two hundred million per second, twice the throughput. {latency} And the latency is two periods of five, still ten nanoseconds. {untied} So the throughput is no longer just one over the latency.

[c6.pipe.6] {lecturer} The lecturer sums it up. We've increased the throughput, but we've also increased the latency. Counted in clock periods, the latency went from one to two. {ns} In nanoseconds, it stayed the same in this ideal picture. In a real circuit, it grows only a little.

## Scene 6 · Registers between the stages (ch6_s6_registers)

> {path}: ch1 s4's path, centre: FF0 (`make_ff`) → a wide "combinational logic" block → FF1, one YELLOW CLK line beneath both, Q0 GREEN and D1 BLUE as in ch1. {register}: each flip-flop gains two ghost copies stacked behind it (one per bit), and the label "register".
> {cut}: the logic block splits into "stage 1 logic" and "stage 2 logic" (the lecturer's "part A and part B"; no letters on screen here, because ch7's circuit uses "A" for a point on a wire), and a third register drops into the gap, its clock pin joining the same CLK line. {shorter}: the YELLOW T_c arrow above the path shrinks from the whole path to one stage.
> {without}: the middle register lifts out, leaving a DIM dashed outline. Token 1 (BLUE) is still a set of wavefronts crawling through the stage 2 logic, its slow paths lagging. {ripple}: the input register lets token 2 (GREEN) in; its wavefronts run through the stage 1 logic and straight on into the stage 2 logic. {race}: the fastest GREEN front overtakes the lagging BLUE ones inside the stage 2 logic. {corrupt}: the wire into FF1 turns RED with "???".
> {with}: the register drops back into place. {hold}: GREEN stops at its input, and its output stays BLUE and steady while token 1 settles in the stage 2 logic. {edge}: a YELLOW pulse runs along the CLK line, and all three registers clock at once: FF1 captures BLUE, GREEN moves into the stage 2 logic, TEAL (token 3) enters the stage 1 logic. Repeat once with the next pulse.
> {stop}: the slide's sentence, small, under the circuit: "Registers stop a token in one pipeline stage catching up with and corrupting the token in the next stage."
> {stage}: each stage boxed in turn, register → stage 1 logic → register, then register → stage 2 logic → register. {rule}: under each, ch1 s6's budget bar (t_pc PINK, t_pd PURPLE, t_su GOLD) with "T_c ≥ t_pc + t_pd + t_su"; the PURPLE segments differ in length. {pay}: the PINK and GOLD segments flash in both bars.
> {slowest}: one YELLOW T_c bracket spans both bars. {decides}: it snaps to the longer one, with the tag "the slowest stage decides". Leave the two bars on screen for the recap.

[c6.reg.1] {how} So how do you build a pipeline in hardware? {path} Start from part one's path, a flip-flop, then combinational logic, then another flip-flop. {register} A token has many bits, so each flip-flop is really a register, a row of dee flip-flops sharing the same clock signal, one per bit. {cut} To pipeline, you place another register between blocks of the logic. {shorter} That divides the logic into shorter stages, which can run with a shorter clock period.

[c6.reg.2] {why} But why does the middle need a register at all? {pause} {without} Imagine splitting the logic without one, and feeding in a new token as soon as the first block is done. {ripple} Combinational logic has no memory, so the new token's signals ripple straight on, into the second block. {race} There, the old token's slowest signals are still settling. The fast new signals catch up with them, {corrupt} and the output is a mix of both tokens. Garbage.

[c6.reg.3] {with} Now put the register back. {hold} It holds the first block's result steady at the second block's input, for a whole clock period, while the first block works on the next token. {edge} On every edge of the clock, each token moves forward one stage, all together. {stop} In the slides' words, registers stop a token in one stage catching up with, and corrupting, the token in the next.

[c6.reg.4] {stage} And now each stage is part one's path again: register, logic, register. {rule} So for each stage, the clock period must be at least the clock-to-output delay, plus the logic's delay in that stage, plus the set-up time. {pay} Notice that every stage pays its own clock-to-output delay and set-up time. {slowest} And every stage shares one clock signal. So which stage sets the clock period? {pause} {decides} The slowest one. The period has to be long enough for every stage.

## Scene 7 · Recap and next (ch6_s7_recap)

> A grid of five small tiles, one per recap sentence, each a shrunk copy of the visual that taught it (same objects and colours), with the sentence's short line under it:
> {r1}: s2's system box with the stopwatch "latency 10 ns" and the exit tally "throughput": "how long for one · how many per second".
> {r2}: s3's two copies beside the box split into "stage 1 | stage 2": "spatial: copies · temporal: stages".
> {r3}: s4's two lanes with their DIM "idle" hatching: "one task per period, stages idle".
> {r4}: s5's staircase, its GOLD "Latency = 2T_c" brace and the half-length YELLOW T_c arrow: "2 periods, each about half as long".
> {r5}: s6's register between the stage 1 and stage 2 logic on one CLK line: "registers keep tokens apart".
> {next}: the tiles clear. A teaser: a DIM row of four logic blocks between two flip-flops, with a GOLD "?" over a register-shaped dashed outline that blinks between two of the blocks (ch7's circuit, unlabelled; its delays stay hidden). {add}: the dashed outline fills in as a register. {buy}: GOLD "how much faster?".
> End card after the last word, held about 8 s; music carries it.

[c6.recap.1] {recap} Let's recap. {r1} The latency is how long one token takes. The throughput is how many tokens finish per second. {r2} Spatial parallelism copies the hardware. And temporal parallelism, or pipelining, splits each task into stages. {r3} Without pipelining, each task fills a whole clock period, and each stage's hardware sits idle part of the time.

[c6.recap.2] {r4} With pipelining, the tasks overlap. The latency becomes two clock periods, but each period is about half as long, so the throughput nearly doubles. {r5} And registers between the stages stop each token corrupting the next. {pause}

[c6.recap.3] {next} Next time, a real circuit from the slides, with real delays. We'll find how fast it can run, {add} and then add one register. {buy} How much faster does that one register make it? {pause}
