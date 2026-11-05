# Chapter 2 · Hold time

Digital Electronics · Lecture 8 (Timing, Metastability and Parallelism), part 2 of 7. Source: Digital Electronics slides (combined_26.pdf), pp. 106–107 (to "Propagation Delay – Note"), with pp. 101–103 (shift register, serial data link) as a refresher; lecture recording 00:11:17–00:18:10.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Spoken names: "cue zero" is Q0, "dee one" is D1, "dee in" is D_in, "cue one" and "cue two" are Q1
and Q2. "The clock-to-cue delay" is t_pc, "the logic's delay" t_pd, "the set-up time" t_su, "the
hold time" t_hold, "the clock period" T_c; "flip-flop zero" is FF0 (it launches) and "flip-flop
one" FF1 (it captures), as in ch1 and ch3. On screen t_hold, as pp. 106–107 write it (only pp. 104
and 110 abbreviate it t_h, so no "(slide: t_h)" note is needed here). Colours as PLAN.md sets them: CLK YELLOW, Q0 GREEN, D1 and
D_in BLUE, t_pc PINK, t_pd PURPLE, t_su and t_hold GOLD, violations RED, a met constraint a GREEN
tick. No code on screen, and no numbers on screen in this chapter. Every claim the briefs draw was
checked in Python 3.11.9 (standard library): a delay model showing the hold result unchanged for
every clock period, the buffer fix leaving the latest settle time and the set-up check unchanged,
the shift register's bit pattern, and the parallel-in, serial-out order.

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card on {title}: "Timing, Metastability and Parallelism", "Digital Electronics · Lecture 8", "Part 2 · Hold time"; it clears on {bar}.
> {bar}: ch1 s6's budget bar returns at centre, in its general form as ch1 s6 drew it (no numbers): one clock period, YELLOW outline and "T_c" label, filled left to right by t_pc (PINK), t_pd (PURPLE) and t_su (GOLD), with "T_c ≥ t_pc + t_pd + t_su" under it. {late}: the PURPLE segment grows, pushing the GOLD segment past the bar's right end, where the overhang turns RED. {slower}: the bar and its T_c arrow stretch to the right until GOLD fits again; a GREEN gap opens just before it.
> {path}: the bar shrinks into the top-right corner. ch1 s4's path at centre: FF0 → "CL" → FF1 (make_ff boxes), Q0 GREEN, D1 BLUE, one YELLOW CLK line under both. ch1 s3's GOLD window sits small over FF1's D input, split at the edge into a left half "set-up" and a right half "hold". {sides}: the right half brightens and the left dims.
> {edge}: a YELLOW pulse runs along CLK and reaches both clock triangles at the same instant. {capture}: a small BLUE token "old" sits on D1 at FF1's input, and pulses as the hold half glows. {launch}: a GREEN token "new" leaves FF0's Q along Q0. {race}: it enters CL and comes out on D1 (now BLUE), running towards the "old" token while the hold half still glows; it stops just short of the input.
> {question}: a YELLOW "too soon?" beside the two tokens. The path, tokens and window carry into s2's opening and s6's first recap tile.

[c2.hook.1] {title} Last time, we found the set-up constraint. {bar} New data has to reach the next flip-flop at least one set-up time before the next edge of the clock. {late} If the logic is too slow, the data arrives late. {slower} But stretch the clock period, and there's room again. So when set-up fails, a longer clock period always fixes it.

[c2.hook.2] {path} But the window around the edge has two sides. {sides} After the edge, the input has to stay steady for the hold time. {edge} Now look at what one edge does to this path. {capture} Flip-flop one is capturing the old value on its input. {launch} At the same instant, flip-flop zero sends out a new value, {race} which runs through the logic, straight towards that same input. {question} So can new data arrive too soon? {pause}

## Scene 2 · The hold constraint (ch2_s2_hold)

> {diagram}: clear to ch1 s5–s6's data-sheet timing diagram, as ch1 s6 drew it, without s6's ticks and ghost X (this is p. 106's first slide). Geometry: ch1 starts D1's hatching "about halfway"; here it starts at 0.4 (below), so ease it there as the scene opens: rows CLK (YELLOW), Q0 (GREEN), D1 (BLUE); the YELLOW "T_c" arrow between two rising edges; Q0's crossover just after the first edge; D1 as two parallel lines with a hatched stretch, then its crossover; PINK "t_pc", PURPLE "t_pd" and GOLD "t_su" dimension arrows under the traces, with thin guides.
> {first}: everything right of D1's hatched stretch dims (the second edge, t_su, the T_c arrow), and the view eases in on the first edge. {window}: a GOLD band on the D1 row only, from the first edge for one hold time, with a GOLD dimension arrow "t_hold" under the others, starting at the edge (p. 106's place). {right}: a small tag on the band, "right side of the window". {only}: the band's outline traces along the D1 row (it stays off the Q0 row), and Q0's crossover, which falls inside the band's time span, gets a small GREEN tag "free to change".
> {launch}: the first rising edge pulses YELLOW. {q0}: Q0's crossover brightens, with the PINK "t_pc" arrow from the edge to it. {hatch}: D1's hatched stretch brightens, and a YELLOW guide drops at its left end, tag "first change". {d1}: a new, shorter PURPLE "t_pd" arrow runs from Q0's crossover to that guide (ch1's own t_pd arrow, ending where D1 settles, stays dimmed: ranges are s5's topic). {earliest}: one bracket from the edge to the guide, labelled "(t_pc + t_pd)_min".
> Geometry (unitless, one period = 1, checked): the hold band ends at 0.3; Q0 crosses at about 0.15 (inside the band, which is fine, since the band is on D1's row); D1's first change at 0.4; its hatching ends (settled) at 0.8; the set-up deadline at 0.9.
> {fine}: the guide sits right of the band's end: GREEN tick, "fine". {bad}: a ghost copy of the D1 row slides in below, its hatched stretch starting at 0.2, inside the band; the overlap glows RED, "bad". {wrong}: a RED "?" on the ghost's band: flip-flop one is still reading its input. It stays up through the next sentence.
> {rule}: the ghost fades. Under the diagram, the inequality as on p. 106: "(t_pc + t_pd)_min ≥ t_hold" (t_pc PINK, t_pd PURPLE, t_hold GOLD). {min}: the "min" subscript glows YELLOW, and a thin line joins it to the "first change" guide.
> {early}: two short tags: at the t_su end, "set-up: arrive early enough"; at the t_hold end, "hold: change late enough". The diagram (good geometry) and the ghost's RED geometry return in s4; the tags clear at the end of the scene.

[c2.hold.1] {diagram} Here's the timing diagram from last time, with the clock signal, cue zero, and dee one. {first} This time, we'll look just after the first edge. {window} At that edge, flip-flop one captures dee one. So dee one has to stay steady for one hold time after the edge. {right} That's the right-hand side of the window from part one. {only} The window is on dee one's row only, because dee one is what flip-flop one reads. Cue zero is free to change inside it.

[c2.hold.2] {launch} But that same edge also launches new data. {q0} Cue zero changes one clock-to-cue delay after the edge. {hatch} The logic responds, and while it settles, dee one may change several times. {d1} Its first change comes after the logic's delay. {earliest} So, counted from the edge, the first change at dee one comes after the clock-to-cue delay plus the logic's delay.

[c2.hold.3] {fine} If that change comes after the hold time ends, everything's fine. Flip-flop one has already taken the old value. {bad} But if it comes sooner, inside the window, that's bad. {wrong} Flip-flop one is still reading its input as it changes, so it may store the wrong value. It might catch the new value a whole cycle early, or neither value cleanly.

[c2.hold.4] {rule} So here's the hold constraint. The clock-to-cue delay plus the logic's delay must be at least the hold time. {min} And it's the minimum of that sum, because what matters is the earliest the change could possibly arrive, by the fastest way through. {early} Set-up needs new data to arrive early enough. Hold needs it to arrive late enough. {pause}

## Scene 3 · Two flip-flops, no logic: the shift register (ch2_s3_shiftreg)

> {chain}: clear. {shiftreg}: p. 101's shift register, from L6's end-card sketch, at full size across the upper half: three make_ff boxes in a row, labelled FF0, FF1, FF2. {wires}: each Q wired straight to the next D, with taps rising to output labels "Q_0", "Q_1", "Q_2" (GREEN). {clk}: one YELLOW "CLK" line along the bottom into all three clock triangles. {din}: "D_in" (BLUE) into the first D. {move}: a small BLUE arrow under the row, pointing right, "one place per edge".
> Under the circuit, p. 102's timing diagram, simplified: rows "CLK", "D_in", "Q_0", "Q_1", "Q_2", in ch1 s5's data-sheet style (sloped edges; single lines rather than the two-line "0 or 1", since the values matter here; delays ignored, as on that slide), with five rising edges and thin guides. ch1 told viewers this style is used "from now on", so no square edges here. All three flip-flops start at 0, and D_in is 1 across the second rising edge only. Checked: after edge 2, Q_0 Q_1 Q_2 = 1 0 0; after edge 3, 0 1 0; after edge 4, 0 0 1; after edge 5, 0 0 0.
> {one}: D_in rises and falls, a single pulse around the second edge. {catch}: at edge 2, Q_0 steps up, and a GOLD digit "1" appears in FF0. {move1}: at edge 3, Q_0 falls and Q_1 rises; the "1" hops to FF1. {move2}: at edge 4, the "1" hops to FF2 as Q_1 falls and Q_2 rises. The high pulses on Q_0, Q_1, Q_2 read as a staircase. {sipo}: a brace over the three output labels, "serial in, parallel out".
> {piso}: the diagram clears. Small PRE pins on the top edges and CLR pins on the bottom edges of the three boxes (L6 ch3's asynchronous-input style). {load}: they flash, and the digits "1 0 1" appear in FF0, FF1, FF2 at once. {out}: D_in dims to 0; on three edges the digits step right, and each leaves FF2's Q into a short queue at the right, reading "1", then "1 0", then "1 0 1". Tag: "parallel in, serial out". Checked: loading Q_0 Q_1 Q_2 = 1 0 1 sends out 1, 0, 1.
> {link}: clear to p. 103's serial data link: a left box "Parallel in, serial out" with three input wires on top ("Parallel Data Input"), one wire across the middle ("Serial Data"), a right box "Serial in, parallel out" with three output wires on top ("Parallel Data Output"), and one CLK line under both. Leave out the slide's D0/D1/D2 and Q0/Q1/Q2 labels, so D1 keeps meaning the path's input. {fewer}: a DIM ghost of a parallel link (three wires) above it, and the count "3 wires → 1".
> {hold}: clear back to the chain, then the view narrows to FF0 and FF1 only. {zero}: s2's "CL" box appears as a ghost between them and squeezes to nothing, leaving the bare Q_0 wire; tag "t_pd = 0". {rule}: "(t_pc)_min ≥ t_hold", as on p. 106's second slide (t_pc PINK, t_hold GOLD).
> {same}: a YELLOW pulse along CLK reaches both boxes at once; Q_0 flickers as FF1 reads it. {skip}: a DIM what-if: FF1's GOLD hold window widened past Q_0's change, and the "1" jumps two boxes in one edge, crossed in RED. {reliable}: the slide's conclusion as one line under the inequality: "a reliable flip-flop: t_hold shorter than its own (t_pc)_min". The two-box picture with its inequality carries into s4.

[c2.shift.1] {chain} Now take the simplest path of all, with no logic. {shiftreg} Here's a shift register, three dee flip-flops in a chain. {wires} Each cue output is wired straight into the next dee input, {clk} and one clock signal drives all three. {din} Data goes in at the left, at dee in. {move} On every rising edge, each flip-flop copies its left-hand neighbour, so the data moves one place to the right.

[c2.shift.2] {one} Watch a single one go in. {catch} On this edge, cue zero picks it up. {move1} On the next, it moves to cue one, {move2} and then to cue two. {sipo} The bits go in one at a time, and come out side by side. That's serial in, parallel out.

[c2.shift.3] {piso} It works the other way, too. {load} Load all three flip-flops at once, through their asynchronous preset and clear inputs. {out} Then shift the bits out of cue two, one per edge. That's parallel in, serial out. {link} Put the two together, and you have a serial data link. {fewer} It sends one bit at a time, over fewer wires than a parallel link.

[c2.shift.4] {hold} Now the hold question. You'd expect two flip-flops wired directly together to just work. {zero} With no logic between them, the logic's delay is zero. {rule} So the rule shrinks. The shortest clock-to-cue delay must be at least the hold time. {same} Each flip-flop reads its neighbour's output at the very edge that changes it. {skip} If the hold time were longer, a bit could jump two places on one edge. {reliable} So a reliable flip-flop needs a hold time shorter than its own shortest clock-to-cue delay.

## Scene 4 · Why the clock can't save you (ch2_s4_noclockfix)

> {zero}: s3's two-box picture shrinks to the top left with "(t_pc)_min ≥ t_hold". The GOLD t_hold becomes a GOLD "0": "(t_pc)_min ≥ 0". {free}: FF1's hold half-window (s1's) shrinks to a line at the edge. {always}: a GREEN tick, and the tag "t_pc > 0, always".
> {both}: clear. Two inequalities stacked at the top: "T_c ≥ t_pc + t_pd + t_su" (label "set-up") and "(t_pc + t_pd)_min ≥ t_hold" (label "hold"). {setup}: T_c glows YELLOW. {hold}: a YELLOW highlight sweeps along the hold line and finds no T_c; tag "no T_c".
> {stretch}: below them, s2's diagram returns in the ghost's bad geometry: D1's hatched stretch starts at 0.2, inside the GOLD hold band, overlap RED. {later}: the second rising edge slides to the right; the T_c arrow and the t_su deadline move with it, and a GREEN gap opens between the end of D1's hatching (still 0.8) and the deadline. {stuck}: the first edge, the GOLD band and the RED overlap stay put and pulse RED; a thin YELLOW pin at the first edge, tag "measured from this edge". {any}: the second edge slides further right, twice more, and each time the RED overlap at the first edge is unchanged; tag "fails at any T_c".
> {rare}: a small caption, p. 106's bullet verbatim: "Note that hold time violations cannot be overcome by adjusting the clock period. Consequently, they can be hard to fix and have to be taken seriously". {serious}: "taken seriously" glows.
> {fix}: the inequalities and caption clear; the second edge slides back; ch1's path returns across the top, above the diagram. {routes}: the "CL" box opens into two routes from Q0 to D1: a long one through three small gate boxes and a short one through a single gate; the short route glows YELLOW, tag "fastest way through".
> {buffers}: two buffer triangles (plain, no bubble) slide into the short route. {moved}: on the diagram, the left end of D1's hatched stretch slides right from 0.2 to 0.4, out of the GOLD band; RED becomes a GREEN tick. {slowest}: the long route brightens; the right end of the hatching (0.8) and the t_su deadline stay where they were, and a second GREEN tick appears at the set-up side. Checked: with buffers only on the short route, the earliest change moves from 0.2 to 0.4 and the latest settle stays at 0.8.
> The path with its two routes carries into s5.

[c2.noclock.1] {zero} Many flip-flops, though not all, are designed with a hold time of zero. {free} Then the input is free to change the moment the edge has passed. {always} And the shift-register rule is always met, because a clock-to-cue delay is always greater than zero.

[c2.noclock.2] {both} Now put the two constraints side by side. {setup} The set-up constraint has the clock period in it. {hold} The hold constraint has no clock period at all. Every term in it is measured from the same edge.

[c2.noclock.3] {stretch} So watch what slowing down does to a hold violation. {later} The next edge moves later, and set-up gets more room. {stuck} But the hold window and the early change stay exactly where they were, pinned to the first edge. Changing the clock period does nothing for hold. {any} A circuit with a hold violation can fail at any clock speed, however slow.

[c2.noclock.4] {rare} Hold violations are rarer than set-up violations, {serious} but they're hard to fix, so they have to be taken seriously. {fix} What you change instead is the circuit. {routes} Inside the logic, the earliest change comes down the shortest route. {buffers} The recommended textbook, by David and Sarah Harris, fixes it by adding delay to that route, usually with buffers, gates that pass their input on a little later. {moved} That pushes the first change out of the hold window. {slowest} And the slowest route is untouched, so set-up is still met.

## Scene 5 · Longest and shortest delays (ch2_s5_contamination)

> {range}: the diagram clears; the path with its two routes (s4) moves to the top left. Centre: two horizontal bars, t_pc (PINK) and t_pd (PURPLE), each drawn from a "min" tick to a "max" tick, labelled "(t_pc)_min" … "(t_pc)_max" and "(t_pd)_min" … "(t_pd)_max". {why}: the bars' spread pulses. {routes}: on the path, the short route flashes and a line joins it to the PURPLE bar's min end; the long route flashes and joins the max end. {bars}: both bars settle, the min ends and max ends lined up in two columns.
> {longest}: the max ends glow, tag "set-up: latest settle". {shortest}: the min ends glow, tag "hold: earliest change".
> {book}: a small plain card "Harris & Harris" (no cover art) beside the bars. {cq}: under the PINK min end, "(t_pc)_min: clock-to-Q contamination delay". {comb}: under the PURPLE min end, "(t_pd)_min: combinational contamination delay" (p. 107's wording).
> {meaning}: a short D1 trace beside them: the old level steady, then from the earliest change a RED smudge spreads over it into the hatching; tag "contaminated".
> {bar}: clear to the budget bar (s1's, ch1's style): one clock period under the YELLOW "T_c" arrow, the first edge at its left end and the next at its right. On it, a GOLD hold fence, a short vertical bar at t_hold (0.3) from the left end, labelled "t_hold", and the GOLD t_su segment at the right end (0.9 to 1), its left edge the set-up deadline.
> {spread}: under the bar, two stacked delay sums grow from the left end: the min pair (PINK + PURPLE) ending at 0.4 and the max pair ending at 0.8. Between those two ends, a BLUE hatched stretch on the bar, labelled "D1 may change". {fence}: its left end and the hold fence flash; GREEN tick. {deadline}: its right end and the deadline flash; GREEN tick.
> {max}: the max pair and the T_c arrow glow, tag "max delays → clock rate". {min}: the min pair and the hold fence glow, tag "contamination delays → hold". This bar between its two fences is s6's fifth recap tile, and ch3 moves the fences with skew.

[c2.range.1] {range} So far, we've treated each delay as one number. In fact, each one is a range. {why} It depends on which route a signal takes, and it varies from one chip to the next. {routes} In the logic from before, the short route sets the shortest delay, and the long route the longest. {bars} So draw each delay as a bar, from its shortest value to its longest.

[c2.range.2] {longest} Set-up asks how late the new data could settle, so it uses the longest delays, the right-hand ends of the bars. {shortest} Hold asks how early the data could start to change, so it uses the shortest, the left-hand ends. Same circuit, same path, but the two rules read opposite ends.

[c2.range.3] {book} Harris and Harris give the shortest delays a name. {cq} The shortest clock-to-cue delay is called the clock-to-cue contamination delay, {comb} and the shortest logic delay is the combinational contamination delay. {meaning} The name sounds slightly scary, but it just means the earliest an output can start to change, contaminating the old value.

[c2.range.4] {bar} Now put it all on one clock period. {spread} Dee one can change anywhere from its earliest time to its latest. {fence} That whole stretch has to start after the hold fence on the left, {deadline} and end before the set-up deadline on the right. {max} The longest delays are usually the main concern, because they limit how fast the clock can run. {min} But the contamination delays decide whether hold is safe. {pause}

## Scene 6 · Recap and next (ch2_s6_recap)

> Five small tiles fill in one per sentence (two rows: three, then two), each a small copy of the visual that taught the idea, in the same colours and styling, with its short line under it. Earlier tiles dim slightly as each new one arrives.
> {race}: tile 1, s1's path with the BLUE "old" token at FF1's input and the GREEN "new" token racing towards it; line "one edge: capture old, launch new".
> {holdrule}: tile 2, s2's diagram trimmed to the D1 row: the GOLD hold band, the GREEN-ticked first change, and the RED ghost change inside the band; line "(t_pc + t_pd)_min ≥ t_hold".
> {shift}: tile 3, s3's three-flip-flop chain with the "1" in FF0; line "(t_pc)_min ≥ t_hold".
> {noclock}: tile 4, s4's two inequalities with T_c YELLOW in the set-up one only, and a buffer triangle beside the hold one; line "fix hold with delay, not the clock period".
> {range}: tile 5, s5's budget bar with the BLUE "D1 may change" stretch between the hold fence and the set-up deadline; line "max → clock rate · min → hold".
> {next}: the tiles clear. ch1's path returns with its CLK line, and a YELLOW pulse reaches FF0 and FF1 together. {late}: the CLK line splits into two branches, and the next pulse reaches the two flip-flops at different instants (one branch a little dimmer). {skew}: the words "clock skew" and a small "Part 3". Then hold the end card for about 8 seconds after the last word, with music carrying it.

[c2.recap.1] {race} One edge captures the old data and sends out new data, so new data can arrive too soon. {holdrule} The fastest way through, from the edge to the first change at dee one, must take at least the hold time. {shift} With no logic, as in a shift register, the flip-flop's own shortest delay, from the edge to its output, has to cover it.

[c2.recap.2] {noclock} The clock period appears only in the set-up constraint, so slowing down does nothing for hold. To fix hold, add delay to the fast path. {range} And every delay is a range. The longest delays limit the clock period, and the shortest, the contamination delays, decide hold.

[c2.recap.3] {next} So far, every flip-flop has seen each edge of the clock at the same instant. {late} Next time, what if the edge arrives late at some of them? {skew} That's called clock skew. {pause}
