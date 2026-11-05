# Chapter 4 · Metastability and the synchroniser

Digital Electronics · Lecture 8 (Timing, Metastability and Parallelism), part 4 of 7. Source: slides (combined_26.pdf) pp. 110–113, to the P_fail formula (p. 113, second slide, first bullet); recording 00:24:31–00:33:04.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch4_s1_hook)

> Title card on {title}: "Timing, Metastability and Parallelism", under it "Digital Electronics · Lecture 8", then the part line "Part 4 · Metastability and the synchroniser". On-screen text spells "metastability" / "metastable" as the slides do, all through the chapter; only the narration hyphenates them.
> {ours}: the card clears to a small copy of ch3 s2's path in the upper left (FF0 → CL → FF1, CLK0 and CLK1 in YELLOW, CLK1 a little dimmer), with ch1 s3's GOLD window on FF1's edge, a GREEN tick, and the line "our own signals: we choose when they change". It dims on {button}.
> Hero, centre: one flip-flop box (L6's `make_ff()`), D (BLUE) in on the left, Q (GREEN) out on the right, CLK (YELLOW) in from below. On {button} a push-button grows at the far left, wired to D. Under the circuit, two traces in ch1 s5's data-sheet style, scrolling slowly left: CLK (YELLOW, sloped edges) and D (BLUE). Every rising edge carries ch1 s3's GOLD window (set-up before the edge, hold after).
> This is the shot ch3's end card teased (push-button on D, the clock ticking past); here it plays out in full.
> {press}: a fingertip presses the button and D steps up at that instant, in the open between two windows (small GREEN tick); later it lets go and D steps down, also between windows.
> {inside}: the next press lands inside a GOLD window, just before the edge. The window flashes RED and the scrolling stops.
> {sigh}: the lecturer's words as a quote, upper right, YELLOW italics: "So many problems with flip-flops!", with a small "— the lecturer" under it.
> {question}: everything dims except that window with D's edge in it. Above it, in YELLOW: "What does a flip-flop do when its input changes inside the window?"
> {road}: ch1 s1's road of three chips along the bottom, "timing rules", "metastability", "parallelism". The first dims as done, and "metastability" lights YELLOW.

[c4.hook.1] {title} Last time, clock skew pushed our two timing rules around. {ours} But we could always meet them, because we decide when our own signals change. {button} Now wire a push-button to a flip-flop's dee input. {press} A person presses it whenever they like, with no idea where the edges of the clock are. {inside} So sooner or later, a press lands right inside the window where dee must keep still.

[c4.hook.2] {sigh} As the lecturer put it, there are so many problems with flip-flops! {question} So here's the question for this part. What does a flip-flop do when its input changes inside the window? {pause=1.5} {road} Answering it takes us to the lecture's second topic, meta-stability.

## Scene 2 · Neither 0 nor 1 (ch4_s2_undefined)

> {recall}: s1's button-and-flip-flop shrinks to the top-left corner. Centre: slide p. 110's diagram, redrawn in ch1 s5's data-sheet style: CLK (YELLOW) with one sloped rising edge, D (BLUE) and Q (GREEN) under it.
> {window}: thin vertical guides t_su before the edge and t_hold after it, with GOLD dimension arrows labelled "t_su" and "t_hold" (the slide writes t_h; we write t_hold, as ch1 s3 said). The GOLD window shades lightly across all three traces.
> {change}: D rises from 0 to 1 inside the window, just before the edge, as on the slide. {violate}: the window tints RED, with the slide's phrase as a caption: "violates the dynamic requirements". {hold}: a dashed ghost of D's edge appears just after the clock edge, inside t_hold, also RED, then fades. {nocontrol}: a small RED "no control" tag on the corner circuit's button.
> {before}: Q sits at a clean 0 up to the edge. {undefined}: after the edge, Q's line drifts up to halfway between the 0 and 1 levels and runs flat there in RED, with the slide's "???" above it.
> {volts}: a vertical voltage axis grows to the right of the traces, "0 V" at the bottom and "V_DD" at the top. A GREEN band near 0 V labelled "valid 0", and a GREEN band near V_DD labelled "valid 1". {invalid}: the gap between them fills RED, labelled "invalid". A dashed line carries Q's RED level across to the axis: it lands in the RED band.
> {confused}: Q's wire in the top-left circuit fans out to two small identical gates. {gates}: one gate is tagged "reads 0", the other "reads 1", both RED.
> {name}: "Metastability" appears above the diagram, large, in RED. s4 brings this diagram back.

[c4.undef.1] {recall} Here's that moment on a timing diagram, from the slides. {window} Around each rising edge is the window from part one, the set-up time before the edge and the hold time after it. {change} This time, dee changes from zero to one just before the edge, inside the window. {violate} In the slide's words, that violates the flip-flop's dynamic requirements. {hold} A change just after the edge, inside the hold time, would break them too. {nocontrol} And there's no way to make a user respect our set-up time.

[c4.undef.2] {before} Before the edge, cue was a clean zero. {undefined} After the edge, cue can be undefined. {pause} The slide just writes three question marks. {volts} Here's what that means as a voltage. A valid zero is near zero volts, and a valid one is near the supply voltage. {invalid} Between them lies a range where the voltage is not valid. For a moment, cue can sit right there, neither zero nor one.

[c4.undef.3] {confused} That's a serious problem for any logic connected to cue. As the lecturer says, that logic is highly confused. {gates} One gate might read the voltage as a zero, and another as a one, so the circuit disagrees with itself. {name} This condition is called meta-stability, and we have to counteract it. {pause}

## Scene 3 · The ball on the hill (ch4_s3_ball)

> {hill}: s2's diagram clears. Centre, large: slide p. 110's picture, a smooth BLUE curve with two valleys and a rounded hill between them. Under the left valley "stable" with a GREEN "0", under the right one "stable" with a GREEN "1"; over the summit "metastable" in RED.
> {valleys}: a GREEN ball rests in the left valley. {nudge}: a small arrow nudges it; it rocks and settles back. A second GREEN ball does the same in the right valley.
> {summit}: one ball, RED, balanced exactly on the summit. {forever}: a small FG timer runs beside it while nothing moves. {wind}: faint wavy wind lines drift in and the ball trembles. {roll}: it rolls down into the right valley and turns GREEN there.
> {balls}: reset to five RED balls on the slopes at different distances from the top, on both sides, each with a small FG timer. {race}: all released together. The furthest off reaches its valley almost at once. {closest}: the one nearest the summit waits longest. Each ball turns GREEN as it lands and its timer stops, so the frozen times read short to long. For believable timing (the straight-line model near the top, checked in Python): a ball starting a fraction x of the way down leaves after about τ·ln(1/x), so starts at 0.3, 0.1, 0.03, 0.01 and 0.003 of the way leave after about 1.2, 2.3, 3.5, 4.6 and 5.8 τ: evenly spaced, though each start is only about three times closer.
> {eventually}: one line under the hill: "eventually a valid 0 or 1, at an unpredictable time".
> {loop}: the hill shrinks to the left. On the right, L6's reset-set latch (`rs_latch()` from l06 ch1_s2_rslatch.py: two cross-coupled NOR gates, R and S BLUE, Q and Q̄ GREEN), and its feedback loop glows. {states}: two small tags beside it, "Q = 0" and "Q = 1", with thin dashed lines to the two valleys. {balance}: a third tag, RED, "Q and Q̄ both halfway", with a dashed line to the summit.

[c4.ball.1] {hill} The slides give a way to picture this. Think of a hill with a valley on each side, and a ball that can roll between them. {valleys} The two valleys are the stable states, zero and one. {nudge} Nudge a ball in a valley, and it settles back. It stays there as long as nothing disturbs it.

[c4.ball.2] {summit} But a ball could also rest on the very top of the hill. {forever} If it were perfectly balanced, it would stay there forever. That's why the hilltop is called meta-stable. {wind} Of course, nothing is perfect. There's a breath of wind, and no ball is perfectly round. {roll} So sooner or later, it rolls down one side or the other, into a stable state.

[c4.ball.3] {balls} How long that takes depends on how well balanced the ball was to begin with. {race} Start a few balls at different distances from the top. The one furthest off rolls away almost at once. {closest} The one closest to the summit waits the longest. {pause} {eventually} A meta-stable flip-flop behaves the same way. It does settle to a valid zero or one, but nobody can say exactly when.

[c4.ball.4] {loop} Why does a flip-flop have a hilltop at all? {pause} Inside it, the bit is held by a feedback loop, like the reset-set latch from lecture six. {states} The loop has two resting states, cue at zero and cue at one. {balance} And between them sits a balance point, with both outputs halfway, each gate holding the other there.

## Scene 4 · How long might it take? (ch4_s4_model)

> {resolve}: s2's CLK / D / Q diagram returns, small, at the top. Q's RED halfway level now ends: it splits into two parallel GREEN lines ("0 or 1", ch1 s5's style). An FG dimension arrow from the clock edge to the split, labelled "t_res", with "resolution time" under it.
> {unbounded}: the split point slides right, and right again, the t_res arrow stretching each time; "no upper limit" in RED.
> {model}: centre, large, slide p. 111's formula, typeset as on the slide (a fraction T₀ over T_c, then e to the power −t/τ): `P(t_res > t) = (T₀ / T_c) e^(−t/τ)`, with t_res in FG. {tc}: T_c lights YELLOW. {consts}: T₀ and τ light together, labelled "characteristics of the flip-flop". {afford}: the t in the exponent pulses, tagged "time we can afford to wait".
> {bad}: the formula rises to the top and its T₀/T_c factor glows. Below, a long YELLOW CLK trace across the screen, many periods. Each rising edge sits in a narrow danger zone (thin FG outline, faint RED tint) a twentieth of the period wide; one zone gets a dimension arrow "T₀", one period the YELLOW "T_c" arrow.
> {rain}: about forty small BLUE ticks (input changes) drop onto the trace at random moments. Most land between zones; the two or so inside a zone turn RED. A tally: "≈ 1 in 20". {slower}: the trace stretches to twice the period, the zones spread out, and a fresh shower gives about half as many RED hits: tally "≈ 1 in 40".
> {tau}: the trace clears and the e^(−t/τ) factor glows. Beside it, a small copy of s3's hill with a ball leaving the summit, tagged "τ: how fast it leaves the summit".
> {curve}: the formula moves to the upper left. Axes: horizontal "t" (time waited) with ticks τ, 2τ, 3τ, 4τ, 5τ; vertical "P(t_res > t)", with "T₀ / T_c" at the top of the curve. The decay curve draws in RED from T₀/T_c at t = 0 down toward zero. {divide}: at each τ tick a small step arrow and GOLD "÷ e" (e ≈ 2.7). {five}: at 5τ, GOLD "≈ 150× smaller".
> {key}: under the graph, the slide's key point: "the longer we wait, the lower the probability of a metastable output", and a small grey note "derivation: not on the course".
> Checked in Python 3.11.9 (math, random): e = 2.718, e⁵ = 148.4; a zone a twentieth of the period catches 0.050 of random changes, and 0.025 with the period doubled.

[c4.model.1] {resolve} So the output does settle eventually, to a valid zero or one. The time it takes is called the resolution time. {unbounded} But in theory, the resolution time has no upper limit. {pause} So instead of a deadline, the slides give us a probability.

[c4.model.2] {model} Here's the model. The probability that the resolution time is longer than some time, tee, equals tee-nought over the clock period, times the exponential of minus tee over tau. {tc} The clock period is the same one as always. {consts} Both tee-nought and tau are characteristics of the flip-flop itself. {afford} Soon, tee will be the time our circuit can afford to wait.

[c4.model.3] {bad} You can read tee-nought over the clock period as the chance that the input changes at a bad time. Picture a narrow danger zone, tee-nought wide, at every rising edge of the clock. {rain} An input that changes at a random moment lands in a zone with probability tee-nought over the period. If each zone takes up a twentieth of the period, that's about one change in twenty. {slower} Make the period longer, and the zones get further apart, so fewer changes hit one.

[c4.model.4] {tau} Tau is a time constant. It says how fast the flip-flop leaves the summit of the hill. {curve} Now plot the probability against tee, the time you wait. {divide} It falls exponentially. Every extra tau of waiting divides it by the same factor, about two point seven. {five} After five tau, it's about a hundred and fifty times smaller. {key} So the longer you wait, the less likely the output is still meta-stable. The slides leave out the derivation, and so will we.

## Scene 5 · One more flip-flop (ch4_s5_synchroniser)

> {problems}: s4's decay curve shrinks to a corner. Slide p. 111's line in RED: "Metastability gives rise to severe system problems". {minimise}: under it, "→ minimise its probability: a synchroniser (cascaded flip-flops)".
> {circuit}: slide p. 112's circuit across the top half: two flip-flop boxes (L6's `make_ff()`), labelled FF0 and FF1. D0 (BLUE) enters FF0 from the left, with s1's push-button wired to it. FF0's Q drives the wire D1 (TEAL) into FF1's D. FF1's Q (GREEN) leaves on the right. {shiftreg}: one CLK line (YELLOW) feeds both clock inputs from below. A ghost of ch2 s3's shift-register chain (Din → Q0 → Q1 → Q2) flashes behind it and shrinks to two stages, lining up with the circuit; tag "a two-stage shift register".
> {timing}: under the circuit, p. 112's timing diagram in ch1 s5's data-sheet style: CLK (YELLOW, sloped edges) over one full period, with the YELLOW T_c dimension arrow between its two rising edges. Before the first edge D1 (TEAL) is two parallel lines ("0 or 1").
> {meta}: at the first edge, D1's two lines converge into one flat line at the midpoint, in RED: D1 is metastable. {settles}: later, before the next edge, the RED line diverges again into two parallel TEAL lines (resolved, 0 or 1).
> {tres}: dimension arrows under the traces, with thin vertical guides at the edges: t_res (FG) from the first rising edge to D1's split, then t_su (GOLD) from the split to the next rising edge.
> {valid}: at the second edge, FF1 samples D1; GREEN tick on FF1. {q}: Q (GREEN, two parallel lines) crosses over, a clean X, t_pc after the second edge, with a PINK t_pc arrow. {likely}: the slide's line under the diagram: "D1 will resolve to a valid level with high probability if T_c is long enough".
> {either}: D1's two resolved lines get small tags, "old value" and "new value", each with a GREEN tick: "either is fair".
> {risk}: FF0's outline turns RED, tagged "takes the risk"; FF1's turns GREEN, tagged "sees a settled input". s6 keeps this diagram.

[c4.sync.1] {problems} Meta-stability causes severe problems in a system, so we have to make it as unlikely as we can. {minimise} The tool for that is called a synchroniser, a chain of flip-flops. {circuit} In its simplest form, it's just one more flip-flop after the input one. The input, dee zero, goes into flip-flop zero, whose output, dee one, goes straight into flip-flop one. Its output is cue. {shiftreg} Both flip-flops share one clock signal. It's the shift register from part two, with just two stages.

[c4.sync.2] {timing} Here's its timing diagram. {meta} Suppose dee zero changes at a bad moment. At this edge, flip-flop zero goes meta-stable, and dee one sits halfway. {settles} But flip-flop one only reads dee one at the next edge, so dee one has most of a period to settle.

[c4.sync.3] {tres} The time it gets is the resolution time. It runs from the first edge up to the set-up time before the next one. {valid} If dee one has settled by then, flip-flop one sees a valid input that meets its set-up and hold times. {q} So it gives a valid output, cue, one clock-to-output delay after the edge. {likely} If the clock period is long enough, that happens with high probability.

[c4.sync.4] {either} Does it matter which way dee one settles? {pause} Either way is fine. The button was being pressed at that very moment, so the old value and the new one are both fair answers. At worst, the press is seen one period later. {risk} So flip-flop zero takes the risk, and flip-flop one almost never sees it.

## Scene 6 · When the synchroniser fails (ch4_s6_fail)

> {longer}: s5's circuit and timing diagram compact into the upper half, and a small YELLOW "?" appears beside Q.
> {wait}: the FG t_res arrow brightens. The GOLD t_su stretch before the second edge pulses: FF1's deadline. {later}: the second rising edge slides right (T_c grows), carrying the t_su stretch with it, and the t_res arrow stretches; D1's RED stretch has more room to end. {slower}: "slower" in YELLOW under the T_c arrow.
> {fails}: a second run. {late}: D1's RED line carries on past the t_su guide, unsplit at FF1's deadline, and the GOLD t_su stretch tints RED. {broken}: at the second edge Q goes to a RED halfway level with "???", and FF1's outline turns RED: "synchroniser fails: Q metastable".
> {budget}: below the diagram, the budget bar from ch1 s6, one clock period T_c long. A ghost of ch1's bar (t_pc PINK, t_pd PURPLE, t_su GOLD) shows first. {slot}: its PINK and PURPLE segments fade and an FG t_res segment grows into their place, leaving t_res + t_su = T_c.
> {condition}: the slide's condition beside the bar: "fails if t_res > T_c − t_su" (t_res FG, T_c YELLOW, t_su GOLD, the ">" in RED).
> {plug}: s4's formula `P(t_res > t) = (T₀ / T_c) e^(−t/τ)` returns. A copy of "T_c − t_su" flies out of the condition into the place of t in the exponent, giving `P_fail = (T₀ / T_c) e^(−(T_c − t_su)/τ)` as on p. 113, boxed. {pfail}: under it, "probability of failure for a single input change".
> {twice}: two arrows from a "longer T_c" tag: a thin one to T₀/T_c ("fewer bad times") and a thick one to the exponential ("more time to settle: the big effect").
> Checked in Python 3.11.9 with ch5's flip-flops (τ = 200 ps, T₀ = 150 ps, t_su = 500 ps): from T_c = 3.00 to 3.04 ns, T₀/T_c falls 1.3% and the exponential factor 18%, and P_fail goes from 1.9 × 10⁻⁷ to 1.5 × 10⁻⁷. None of these numbers goes on screen.

[c4.fail.1] {longer} How can we make a meta-stable output even less likely? {pause} {wait} Wait longer for dee one to resolve. But dee one must still be steady one set-up time before the next edge. {later} So the only way to wait longer is to move that edge later, with a longer clock period, {slower} which means running the synchroniser more slowly. Reliability costs speed.

[c4.fail.2] {fails} We say the synchroniser fails if its output, cue, goes meta-stable. {late} That can happen if dee one is still unresolved at flip-flop one's set-up deadline, one set-up time before the next edge. {broken} Then flip-flop one's own window is broken, and its output can be undefined.

[c4.fail.3] {budget} Put it on the budget bar from part one. {slot} The clock period now holds the resolution time, then the set-up time. The resolution time sits where the logic's delay used to be. {condition} So the synchroniser fails if the resolution time is longer than the clock period minus the set-up time.

[c4.fail.4] {plug} And the model already gives the chance of that. For the time, tee, put in the clock period minus the set-up time. {pfail} That's pee-fail, the probability of failure for a single input change. It's tee-nought over the clock period, times the exponential of minus, the clock period minus the set-up time, over tau. {twice} A longer period helps twice. Bad times get rarer, and the exponential gets more time to shrink. The exponential is by far the bigger effect.

## Scene 7 · Recap and next (ch4_s7_recap)

> {recap}: clear to a grid of six small tiles (two rows of three), each a small version of the visual that taught the idea (same objects, colours and styling), with its short line under it, appearing on {r1} … {r6}:
> {r1}: s1's push-button wired to D, the press landing in a GOLD window that flashes RED; line "Outside inputs ignore the window". {r2}: s2's Q trace going to the RED halfway level with "???", beside the voltage axis with its GREEN valid bands and RED invalid band; line "Q undefined: neither 0 nor 1".
> {r3}: s3's BLUE hill with a RED ball on the summit and arrows down both sides; line "Metastable: resolves, in its own time". {r4}: s4's RED decay curve with "÷ e" at each τ; line "P(t_res > t) = (T₀ / T_c) e^(−t/τ)".
> {r5}: s5's two-flip-flop synchroniser (D1 TEAL) over its CLK / D1 / Q traces, with the FG t_res arrow; line "One more flip-flop: a period to settle". {r6}: s6's bar (t_res FG + t_su GOLD = T_c) with the boxed P_fail formula; line "Fails if t_res > T_c − t_su".
> {next}: the tiles dim. s5's synchroniser alone, centre; a stream of BLUE ticks (input changes) runs into D0, each with a tiny GOLD "P_fail" tag, and the stream speeds up; now and then one flashes RED (no odds on screen: ch5's hook owns "1 in 10,000,000"). {years}: GOLD "P_fail → years" appears beside a small calendar. Then the end card, held ~8 s after the last word while the music carries it.

[c4.recap.1] {recap} Let's recap. {r1} Inputs from the outside world, like a button, can change inside the set-up and hold window. {r2} Then a flip-flop's output can be undefined for a while, at a voltage that is neither a valid zero nor a valid one. {r3} That's meta-stability, a ball balanced on a hilltop. It always rolls off in the end, but the better balanced it is, the longer it takes.

[c4.recap.2] {r4} The chance that it's still undecided after a time, tee, falls exponentially, divided by about two point seven for every tau. {r5} A synchroniser adds one more flip-flop, so flip-flop zero gets most of a period to settle. {r6} It fails if the resolution time is longer than the clock period minus the set-up time, and the model turns that into pee-fail.

[c4.recap.3] {next} Next time, how often will a synchroniser actually fail? A tiny chance on each input change still adds up, when the changes keep coming. {pause} {years} So we'll turn pee-fail into a time we can plan around, measured in years. {pause}
