# Chapter 3 · Clock skew

Digital Electronics · Lecture 8 (Timing, Metastability and Parallelism), part 3 of 7. Source: Digital Electronics slides (combined_26.pdf), pp. 107 (second slide, "Clock Skew")–109; lecture recording 00:18:10–00:24:31.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Spoken names: "flip-flop zero" and "flip-flop one" are FF0 and FF1; "clock zero" and "clock one" are CLK0 and CLK1; "cue zero" is Q0, "dee one" is D1. Quantities in words: "the clock period" T_c, "the clock-to-cue delay" t_pc, "the logic's delay" t_pd, "the set-up time" t_su, "the hold time" t_hold, "the skew" t_skew. No code on screen. Every inequality was checked in Python 3.11.9 (standard library) against a timing model (times from CLK0's launching edge; CLK1 ahead or behind by t_skew; 200,000 random cases for all four forms), and so were the worked numbers, the shift-register race and the late-middle-flip-flop claim in s6.

---

## Scene 1 · Hook (ch3_s1_hook)

> Title card on {title}: "Timing, Metastability and Parallelism", "Digital Electronics · Lecture 8", "Part 3 · Clock skew"; it clears on {path}.
> {path}: ch1 s4's path at centre, as ch2's end card left it (its CLK line rejoined into one): FF0 → a "combinational logic" box → FF1 (L6's `make_ff()` boxes), the Q0 wire GREEN, the D1 wire BLUE, one YELLOW "CLK" line along the bottom feeding both clock triangles. Above it, ch2 s4's two inequalities side by side, small: "T_c ≥ t_pc + t_pd + t_su" tagged "set-up" and "(t_pc + t_pd)_min ≥ t_hold" tagged "hold". {early}: the set-up one brightens; {steady}: the hold one brightens.
> {same}: a bright YELLOW pulse runs along the CLK line and reaches both triangles at once; both flash together, small tag "same instant" under them.
> {board}: zoom out. The path shrinks into one corner of a large board (a dark rounded rectangle) holding about a dozen small flip-flop boxes. A YELLOW clock source sits at the left edge, with a branching tree of YELLOW wires to every box, some routes short, some long.
> {edge}: one rising edge leaves the source as a bright pulse running down every branch at the same speed. {near}: the nearest boxes flash first; {far}: the farthest flash last. Under the board, a short time axis collects one tick per box as it flashes: the ticks spread out instead of stacking on one instant.
> {question}: a YELLOW "?" over the spread of ticks, and the two inequalities return beside it, each with a small "?".

[c3.hook.1] {title} Last time, we found the hold constraint. {path} So now every path from one flip-flop to the next has two timing rules to obey. {early} Set-up needs new data to arrive early enough, before the next edge. {steady} Hold needs it to arrive late enough, after the hold time.

[c3.hook.2] {same} Both rules quietly assumed that every edge of the clock reaches every flip-flop at the same instant. {board} But a real clock signal has to travel along wires, to every flip-flop on a board or on a chip. {edge} Watch one rising edge spread out. {near} The nearby flip-flops see it first, {far} and the distant ones see it later. {pause} {question} So what happens to our two rules when an edge arrives late? {pause}

## Scene 2 · What skew is (ch3_s2_skew)

> {wire}: s1's board, dimmed, except one short YELLOW branch and one long one, each from the source to a flip-flop box. {cm} (ours, checked: c/√ε_r for FR-4, 14.5 to 17.3 cm/ns): a ruler along the long branch; a pulse moves along it and a GOLD label reads "≈ 15 cm per ns".
> {lengths}: pulses leave the source together on both branches; the short one arrives first. Each box gets its own arrival tick on a small time axis below; the two ticks sit apart.
> {chip}: the board morphs into a square chip, a branching YELLOW clock tree spread over its surface, its ends lighting at slightly different moments. {name}: a TEAL bracket spans the spread of arrival ticks, with the label "clock skew".
> {redraw}: clear. s1's path returns at centre, its single CLK line now split into two YELLOW branches from a clock source at the right ({source}): a short branch to FF1's triangle and a long one round to FF0's. {clk0}: the long branch is labelled "CLK0"; {clk1}: the short one "CLK1", drawn a little dimmer (CLK1 stays slightly dimmer for the rest of the chapter).
> {ahead}: a pulse leaves the source and reaches FF1's triangle first. Under the path, two small data-sheet-style clock traces (sloped edges, ch1 s5's style): CLK0 above, CLK1 below, CLK1's rising edges earlier. A TEAL dimension arrow between a CLK1 edge and the matching CLK0 edge, labelled "t_skew".
> {other}: for a beat, a ghost source swings to the left side and CLK1's trace slides later than CLK0's (the TEAL arrow flips round); then the ghost fades and both return. {later}: a small tag beside the traces, "first: CLK1 ahead (slides pp. 107–109)".

[c3.skew.1] {wire} Wires are fast, but every wire has a delay. {cm} On a circuit board, a signal travels roughly fifteen centimetres in a nanosecond. {lengths} The clock signal reaches each flip-flop by its own route, with its own length, so each one sees the edge after its own delay. {chip} The same is true inside a chip, where the clock signal is spread across the whole surface. {name} This variation in when the edges arrive is called clock skew. {pause}

[c3.skew.2] {redraw} So let's redraw our path, with a separate clock wire to each flip-flop. {source} Suppose the signal comes in from the right, so the wire to flip-flop one is the shorter one. {clk0} We'll call the clock signal at flip-flop zero, clock zero, {clk1} and the one at flip-flop one, clock one. {ahead} Here, clock one is ahead. Its edges arrive before clock zero's, by an amount we call the skew.

[c3.skew.3] {other} That's the case on the lecture's slides. It could just as well be the other way round, depending on how the wires are laid out. {later} We'll work through this case first, and turn it round at the end.

## Scene 3 · Skew and set-up (ch3_s3_skewsetup)

> s2's path shrinks to a strip at the top (CLK0 and CLK1 labels kept). Below it, p. 108's diagram, built slowly in ch1 s5's data-sheet style: four rows labelled at left "CLK0", "Q0", "D1", "CLK1". CLK0 and CLK1 YELLOW (CLK1 a little dimmer), Q0 GREEN, D1 BLUE. Sloped edges; Q0 and D1 as two parallel lines with a crossover where they change; D1's settling stretch hatched.
> {traces}: the four row labels appear. {clk0}: CLK0 drawn: rise, high, fall, low, rise. A YELLOW "T_c" dimension arrow above it between its two rising edges, with thin vertical guides. {clk1}: CLK1 is born from a copy of CLK0 that drops to the bottom row and slides earlier; TEAL "t_skew" arrows between each CLK1 rising edge and the CLK0 rising edge after it.
> {launch}: CLK0's first rising edge flashes. {q0}: Q0 crosses over; a PINK "t_pc" arrow from that edge to the crossover. {d1}: D1's hatched stretch (several crossovers) appears after Q0's crossing. {settle}: D1's last crossover; a PURPLE "t_pd" arrow from Q0's crossover to it.
> {deadline}: a YELLOW "?" over D1's last crossover. {capture}: CLK1's second rising edge brightens with its guide (FF1 lights in the strip at top); CLK0's second edge dims. A GOLD "t_su" arrow ends at CLK1's edge.
> {early}: the TEAL "t_skew" arrow between CLK1's second edge and CLK0's second edge brightens. {lost}: a GOLD ghost of ch1's deadline (t_su before CLK0's edge) slides left by t_skew onto the real one, and the TEAL gap it leaves behind flashes: time the data no longer has. D1's last crossover sits exactly at the start of t_su: the worst case, as on p. 108.
> {bar}: under the diagram, ch1's budget bar returns, one CLK0 period wide and aligned with the T_c arrow. {segs}: PINK "t_pc", PURPLE "t_pd" and GOLD "t_su" segments, as in ch1. {fourth}: a TEAL "t_skew" segment grows out of the diagram's t_skew arrow into the bar's right end; the four segments exactly fill the period.
> {rule}: the segments fly up into "T_c ≥ t_pc + t_pd + t_su + t_skew", each symbol in its segment's colour, T_c YELLOW. {worst}: small "max" tags on t_pc and t_pd. The inequality and the bar stay for s4.

[c3.setup.1] {traces} Here's the timing diagram, with a row for each clock signal. {clk0} At the top, clock zero, with its period marked between two rising edges. {clk1} At the bottom, clock one. It's the same wave, shifted earlier by the skew.

[c3.setup.2] {launch} Now follow one new value along the path. Clock zero's first edge launches it. {q0} Flip-flop zero's output, cue zero, changes one clock-to-cue delay later. {d1} Then the logic gets to work, and dee one may change several times while it settles. {settle} It finally settles after the logic's delay.

[c3.setup.3] {deadline} So which edge does dee one have to beat? {pause} {capture} Flip-flop one listens to clock one, so dee one must be steady one set-up time before clock one's next edge. {early} And that edge comes early, a whole skew ahead of clock zero's. {lost} So the deadline moves earlier by the skew, and the data has that much less time to arrive.

[c3.setup.4] {bar} Now add up the period, as in part one. {segs} There's the clock-to-cue delay, the logic's delay and the set-up time, as before. {fourth} And now a fourth piece, the skew. {rule} So the clock period must be at least the clock-to-cue delay, plus the logic's delay, plus the set-up time, plus the skew. {worst} As before, these are the longest delays, because set-up is about the latest the data could arrive. {pause}

## Scene 4 · Less time for the logic (ch3_s4_lesslogic)

> s3's inequality "T_c ≥ t_pc + t_pd + t_su + t_skew" at the top, s3's four-segment bar below it; the timing diagram clears.
> {rearrange}: the PURPLE t_pd glows; the other symbols dim slightly. {solve}: it rearranges as in ch1 s7, t_pd moving to the left and the rest flying across, into "t_pd ≤ T_c − (t_pc + t_su + t_skew)". {eats}: on the bar, the TEAL segment pushes in from the right and the PURPLE segment shrinks by the same width.
> {example}: ch1 s7's worked numbers return in GOLD, left: "t_pc = 0.2 ns", "t_su = 0.1 ns". {ghz}: "f_c = 1 GHz  →  T_c = 1 ns"; the bar is redrawn 1 ns wide as ch1 s7 left it, PINK 0.2 | PURPLE 0.7 | GOLD 0.1, the PURPLE labelled "0.7 ns".
> {skew}: "t_skew = 0.1 ns" (GOLD number, TEAL symbol), with a small tag "≈ 1.5 cm of extra board wire". {left}: a TEAL 0.1 segment slides in at the right end, the PURPLE shrinks to "0.6 ns", and the sliver it lost flashes with the tag "1/7 of the logic's time".
> {other} / {keep}: a second bar below the first, with PURPLE kept at 0.7: PINK 0.2 | PURPLE 0.7 | GOLD 0.1 | TEAL 0.1, running past a thin vertical "1 ns" mark carried down from the first bar. {grow}: "T_c ≥ 1.1 ns" under it. {mhz}: "f_c ≤ 909 MHz" (GOLD) beside a struck-through "1 GHz".
> {cost}: the TEAL segment and the 909 MHz both flash.
> Checked (Python 3.11.9): 1 − (0.2 + 0.1) = 0.7 ns; 1 − (0.2 + 0.1 + 0.1) = 0.6 ns; 0.1/0.7 = 0.143 ≈ 1/7; 0.2 + 0.7 + 0.1 + 0.1 = 1.1 ns, 1/1.1 ns = 909.09 MHz, a 9.1% drop; 0.1 ns × 15 cm/ns = 1.5 cm. All "ours" (PLAN.md), built on p. 118's flip-flops.

[c3.less.1] {rearrange} The flip-flops come from a data sheet, so the part the designer controls is the logic. {solve} Rearrange, and the logic's delay must be at most the clock period, minus the sum of the clock-to-cue delay, the set-up time and the skew. {eats} So the skew eats into the logic's budget.

[c3.less.2] {example} Here's an example, with the flip-flops from part one. Their clock-to-cue delay is zero point two nanoseconds, and their set-up time is zero point one. {ghz} At one gigahertz, the period is one nanosecond, which left zero point seven nanoseconds for the logic. {skew} Now add a skew of zero point one nanoseconds. On a board, that's only about one and a half centimetres of extra wire. {left} The logic is left with zero point six nanoseconds, a seventh of its time gone.

[c3.less.3] {other} Or look at it the other way. {keep} Keep the logic's zero point seven nanoseconds. {grow} Then the clock period must grow to at least one point one nanoseconds, {mhz} and the fastest clock rate falls to about nine hundred and nine megahertz. {pause} {cost} A tenth of a nanosecond of skew has cost almost a tenth of the clock speed.

## Scene 5 · Skew and hold (ch3_s5_skewhold)

> {back}: s3's four traces return (CLK0, Q0, D1, CLK1), now as p. 109 draws them; s3's bar and set-up arrows are gone. {first}: the right half of the diagram dims, the first edges stay bright.
> {capture}: CLK1's first rising edge brightens with its guide (FF1 lights in the top strip). {window}: a GOLD "t_hold" arrow starts at that edge, and a GOLD band over D1's row for the same stretch, tagged "old D1 steady".
> {launch}: a TEAL "t_skew" arrow from CLK1's first edge to CLK0's first edge, which flashes (FF0 lights). {q0}: a PINK "t_pc" arrow to Q0's crossover. {d1}: a PURPLE "t_pd" arrow to the start of D1's hatched stretch, the earliest change. Small "min" tags on t_pc and t_pd. {count}: one long bracket from CLK1's edge to D1's first change gathers the TEAL, PINK and PURPLE arrows, set against the GOLD t_hold above it.
> {good}: a ghost D1 change after the GOLD band's end gets a GREEN tick. {bad}: a ghost change inside the band gets a RED cross, and the band flashes RED.
> {rule}: the bracket's three arrows fly into "t_skew + (t_pc + t_pd)_min ≥ t_hold" (TEAL, PINK, PURPLE, GOLD); the ghosts clear. {min}: the "min" subscript glows.
> {helps}: "t_skew" in the inequality glows TEAL, with a GREEN tick beside it. {quote}: under it, p. 109's words in small italics, "in effect, the availability of hold time is increased".
> {fences}: clear to ch2 s5's budget bar, same proportions: one CLK0 period under the YELLOW "T_c" arrow; the GOLD hold fence at 0.3 of the period; the BLUE hatched stretch "D1 may change" from (t_pc + t_pd)_min at 0.4 to (t_pc + t_pd)_max at 0.8; the GOLD t_su segment from 0.9 to the right end, its left edge the set-up deadline. The two inequalities sit above, small. {slide}: both fences slide left together by 0.1 of the period, a short TEAL "t_skew" arrow under each; the TEAL t_skew segment fills the 0.9 to 1 gap left at the right end (s3's four-segment bar again).
> {hurt}: the deadline closes in until it touches the hatched stretch's right end (0.8: met, nothing to spare); the set-up inequality is tagged "harder" (RED). {help}: the hold fence moves away from the stretch's left end (0.2 against 0.4); the hold inequality is tagged "easier" (GREEN). This picture carries into s6.
> Checked (Python 3.11.9 timing model): with CLK1 ahead by t_skew, the hold fence sits at t_hold − t_skew and the deadline at T_c − t_skew − t_su, measured from CLK0's edge, which gives exactly p. 108's and p. 109's inequalities.

[c3.hold.1] {back} Now the hold rule, on the same four traces. {first} This time, look at the first edges. {capture} Clock one's edge arrives first, and flip-flop one captures the old dee one there. {window} So the old value must stay steady for one hold time after that edge.

[c3.hold.2] {launch} Only a skew later does clock zero's edge arrive, and launch the new value. {q0} Cue zero changes one clock-to-cue delay after that, {d1} and dee one starts to change the logic's delay later still. {count} So, counted from flip-flop one's edge, the new value reaches dee one after the skew, plus the clock-to-cue delay, plus the logic's delay.

[c3.hold.3] {good} If that change comes after the hold window ends, all is well. {bad} If it comes inside the window, the old value is lost. {rule} So the skew, plus the shortest clock-to-cue and logic delays, must be at least the hold time. {min} Here the delays are the shortest ones, because hold is about the earliest the change could arrive. {helps} The skew is added to the delays, so in this case it makes hold easier to meet. {quote} In the slide's words, the availability of hold time is increased.

[c3.hold.4] {fences} Here's part two's picture of both rules at once. Dee one may change anywhere between its earliest and latest arrival, and that stretch must sit between the hold fence and the set-up deadline. {slide} The skew slides both fences earlier, together. {hurt} The deadline closes in on the data, so set-up gets harder. {help} The hold fence moves away from it, so hold gets easier. {pause}

## Scene 6 · The other direction (ch3_s6_otherway)

> {flip}: s5's fence picture stays. Beside it, s2's small path: its clock source moves from the right to the left, so the CLK1 branch is now the long one; under it, CLK1's small trace slides later than CLK0's and the TEAL "t_skew" arrow flips round.
> {slide}: both fences slide right together, 0.1 of the period past where ch2 had them (0.2 from s5's position). {setup}: the deadline moves away from the hatched stretch to the bar's right end (the GOLD t_su segment pokes out past it, up to CLK1's late edge); the set-up inequality becomes "T_c ≥ t_pc + t_pd + t_su − t_skew", tagged "easier" (GREEN). {hold}: the hold fence closes in until it touches the stretch's left end (0.4: met, nothing to spare); the hold inequality becomes "(t_pc + t_pd)_min ≥ t_hold + t_skew", tagged "harder" (RED).
> {shift}: clear to ch2 s3's shift register, same drawing and colours: FF0, FF1, FF2 in a row, each Q wired straight to the next D, "D_in" BLUE, "Q_0", "Q_1", "Q_2" GREEN. Its YELLOW clock line now comes from a source at the left, so each flip-flop's branch is longer than the one before; "CLK0" and "CLK1" labels on the first two branches.
> {late}: a small "t_hold = 0" tag. Two small traces under FF0 and FF1: CLK0, and CLK1 later by a TEAL "t_skew" arrow that is visibly longer than a PINK "(t_pc)_min" arrow measured from CLK0's edge.
> {race}: D_in is 1 and all three flip-flops hold 0. On one edge: the pulse reaches FF0's triangle and ch2's GOLD digit "1" appears in FF0; Q_0 changes after (t_pc)_min and the "1" runs along the wire to FF1's D; only then does the pulse reach FF1's triangle, and a second "1" appears in FF1.
> {two}: after that single edge, the "1" sits in FF0 and FF1 at once: ch2 s3's crossed-out what-if, now real. RED tag "two places in one edge"; a dim GREEN ghost of the correct state (the "1" in FF0 only) beside it. {nofix}: ch2 s4's hold inequality returns, with no T_c in it; beside it, a slower-clock icon (a stretched YELLOW wave) gets struck through in RED.
> {advice}: clear to a three-flip-flop row: FF0 → FF1 → FF2, FF1 in the middle with its own clock branch. {both}: a YELLOW "?" over FF1's branch. {middle}: arrows on the data path, one into FF1 and one out of it. {inpath}: FF1's clock marked late (a TEAL tag); the arrow into it lights with "hold harder" (RED). {outpath}: the arrow out of it lights with "set-up harder" (RED). {check}: a caption under the row, "check skew both ways: it affects both rules".
> Checked (Python 3.11.9): with CLK1 lagging by t_skew the timing model gives exactly these two inequalities; with t_hold = 0, FF1 takes the new bit whenever t_skew > (t_pc)_min (e.g. 0.15 ns of skew against a 0.1 ns shortest clock-to-Q delay); and a middle flip-flop's late clock shrinks the hold margin on the path in and the set-up margin on the path out. The skew-reversed algebra, the race and the middle flip-flop are ours (PLAN.md); the slides only say it depends on which clock leads.

[c3.other.1] {flip} Now turn it round, so clock one lags behind clock zero by the skew. {slide} The fences slide later instead. {setup} Set-up gets easier. The clock period must be at least the old sum, minus the skew. {hold} But hold gets harder. The shortest clock-to-cue and logic delays must now be at least the hold time, plus the skew. {pause}

[c3.other.2] {shift} It's most dangerous in part two's shift register, with no logic between the flip-flops to slow the data down. {late} Say the hold time is zero, as it often is, and flip-flop one's clock signal is late by more than flip-flop zero's shortest clock-to-cue delay. {race} On a single edge, flip-flop zero takes in a new bit and passes it straight on, and the late edge catches it at flip-flop one too. {two} So the bit has gone two places on a single edge. {pause} {nofix} That's a hold violation, and as we saw last time, no slower clock can fix it.

[c3.other.3] {advice} So which way does the skew go in your circuit? {both} Usually, both ways at once. {middle} Most flip-flops take data in from one neighbour and pass it on to another. {inpath} If one flip-flop's clock signal is late, hold gets harder on the path coming in, {outpath} and set-up gets harder on the path going out, because its own data leaves late. {check} That's why the lecture's advice is to check skew in both directions. It affects both rules.

## Scene 7 · Recap and next (ch3_s7_recap)

> Six small panels fill the frame one per sentence, each the scene's own visual (same objects, colours and styling), with its short line under it.
> {r1}: s1's board with the bright pulse mid-spread and the ticks spreading on the time axis; "edges arrive at different times".
> {r2}: s2's path with its YELLOW CLK0 and CLK1 branches and the TEAL "t_skew" arrow between the two small clock traces; "clock skew".
> {r3}: s3's four-segment budget bar (PINK, PURPLE, GOLD, TEAL) under "T_c ≥ t_pc + t_pd + t_su + t_skew"; "skew joins the budget".
> {r4}: s4's 1 ns bar, its PURPLE segment labelled "0.6 ns" with a dim ghost of the 0.7; "t_pd ≤ T_c − (t_pc + t_su + t_skew)".
> {r5}: s5's hold view cut down to CLK1's edge, the GOLD t_hold band and the TEAL + PINK + PURPLE bracket, with a GREEN tick; "skew helps hold".
> {r6}: s5–s6's fence picture: the two GOLD fences slide left (set-up "harder", hold "easier"), then right (the tags swap); "turn it round: the trade reverses".
> {next}: the panels shrink away. A push button wired to a flip-flop's D (BLUE), the clock ticking past; {broken}: the press lands inside ch1's GOLD set-up and hold window, and Q shows a RED "???".
> End card after the last word, held ~8 s; the music carries it.

[c3.recap.1] {recap} Let's recap. {r1} A clock edge takes time to travel along the wires, so it reaches different flip-flops at different moments. {r2} That difference is clock skew, and it splits our path's clock signal into two, clock zero and clock one. {r3} When the receiving flip-flop gets its edge early, the skew becomes a fourth piece of the period's budget. {r4} So the logic gets less time. At one gigahertz, its zero point seven nanoseconds shrink to zero point six. {r5} But the same skew gives the hold rule more room. {r6} Turn the skew round, and the trade reverses, so check it both ways. {pause}

[c3.recap.2] {next} Next time, inputs from the outside world, like a button press, which obey no clock at all. {broken} And what a flip-flop does when its input changes inside its set-up and hold window. {pause}
