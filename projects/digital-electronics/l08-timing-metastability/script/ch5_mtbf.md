# Chapter 5 · Mean time between failures

Digital Electronics Lecture 8 (Timing, Metastability and Parallelism), part 5 of 7. Source: slides
(combined_26.pdf) pp. 113 (second slide) to 115 (first slide), with ch4's P_fail (p. 113, first
slide) recalled; recording 00:32:43–00:37:51.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Numbers: every figure below was computed in Python 3.11.9 (standard library, `math`) from the
slides' formulas, with the one-year clock period found by bisection. One year = 31,536,000 s.

---

## Scene 1 · Hook (ch5_s1_hook)

> {title}: title card, "Timing, Metastability and Parallelism", "Digital Electronics · Lecture 8", "Part 5 · Mean time between failures". It clears on {synch}.
> {synch}: ch4 s5's synchroniser, centred high, in ch4's styling: D0 (BLUE) → FF0 → D1 (TEAL) → FF1 → Q (GREEN), flip-flop boxes from `make_ff()`, one YELLOW CLK line into both triangles. Under it, ch4 s6's last shot, small: `P_fail = (T_0/T_c) e^(−(T_c − t_su)/τ)` (P_fail GOLD, T_c YELLOW) beside the budget bar T_c = t_res (FG) + t_su (GOLD).
> {gamble}: a BLUE step on D0; D1 wobbles at the RED mid-level, and the wobble is still there at FF1's next edge, so a RED "???" flickers at Q: one change that got through.
> {years}: the circuit and formula shrink to the upper left. A long time axis appears across the middle, "0" to "2 years", with month ticks. {tenmillion}: a GOLD tag "P_fail = 1 in 10,000,000".
> {slow}: a fine BLUE comb along the axis ("1 change per second"), with a RED cross every ~116 days, about four months: "a failure every 10⁷ s ≈ 116 days" (checked: 10⁷ s = 115.7 days).
> {fast}: the comb turns solid ("10⁶ changes per second") and the axis rescales to "0" to "60 s": a RED cross every 10 s, "a failure every 10 s" (checked: 1/(10⁶ × 10⁻⁷) = 10 s). {depends}: "changes per second" gets a YELLOW underline in both tags.
> {question}: everything dims; YELLOW line "How long, on average, between failures?". {year}: second line under it, "What clock period makes that at least a year?". Hold on the pause.

[c5.hook.1] {title} Last time, we built a synchroniser from two flip-flops. {synch} And we found pee-fail, the chance that a single change at its input gets through still meta-stable. {gamble} When that happens, the synchroniser has failed.

[c5.hook.2] {years} But a real product has to run for years. {tenmillion} Say the chance is one in ten million. Is that good enough? {pause} {slow} If the input changes once a second, there's a failure about once every ten million seconds, which is nearly four months. {fast} If the input changes a million times a second, there's a failure every ten seconds. {depends} So the answer depends on how often the input changes.

[c5.hook.3] {question} How long, on average, will we wait between failures? {year} And how long must the clock period be, to make that wait at least a year? {pause}

## Scene 2 · From one change to failures per second (ch5_s2_rate)

> The hook's synchroniser, small, upper left (D0 BLUE, D1 TEAL, Q GREEN, CLK YELLOW). A horizontal time axis across the middle, ticks `0 s`, `1 s`, … `6 s`.
> {change}: a BLUE tick on the axis where D0 changes, and a small die pops up above it. {roll}: the die rolls; its face reads GOLD "P_fail".
> {safe}: it lands on a GREEN tick, and D1 in the small circuit settles. {fail}: a later change's die lands on a RED cross; D1 wobbles at the RED mid-level and a RED "???" flickers at Q.
> {once}: one BLUE tick per second along the axis, each with its die; a bracket over one second: "1 change per second → probability of failure per second = P_fail".
> {many}: the ticks multiply to three per second (the picture uses N = 3), each with its die; the bracket now holds three dice, "N changes per second". {average}: the ticks jitter into uneven spacing, about three per second still, and the label becomes "N: average changes per second".
> {formula}: p. 113's line, verbatim: `P_fail/s = N P_fail` (P_fail GOLD, N GOLD). {rate}: a label under it, "failures per second".
> {tiny}: a sample value beside it, with the hook's numbers: `N = 1, P_fail = 10⁻⁷ → 10⁻⁷ failures per second`, small and grey. {flip}: a curved YELLOW arrow loops round "failures per second", leading into s3.

[c5.rate.1] {change} Let's count failures. Every time the input, dee zero, changes, the synchroniser takes a gamble. {roll} The chance that this one change gets through while still meta-stable is pee-fail. {safe} Almost always, dee one resolves in time. {fail} Very rarely, dee one is still meta-stable at the set-up deadline, so the output, cue, goes meta-stable too. That's a failure.

[c5.rate.2] {once} If dee zero changes once per second, there's one gamble every second. So the probability of failure per second is just pee-fail. {many} If dee zero changes N times per second, there are N gambles every second, and the probability of failure per second is N times greater. {average} Real inputs change at random times, so N is an average, the number of changes per second.

[c5.rate.3] {formula} In the slide's notation, pee-fail per second equals N times pee-fail. {rate} It's a rate, the number of failures we expect each second. {tiny} With the hook's numbers, one change a second and a chance of one in ten million, that's ten to the minus seven failures per second. {flip} A number like that is hard to picture, so engineers turn it upside down.

## Scene 3 · Seconds per failure (ch5_s3_mtbf)

> {flip}: s2's "failures per second" label swaps its two nouns round "per" and becomes "seconds per failure". {name}: above it, YELLOW "mean time between failures (MTBF)".
> {recip}: p. 114's first step builds: `MTBF = 1/(P_fail/s)`. {hundred}: a small example beside it: a time axis with a RED cross every 100 s, "0.01 failures per second ↔ MTBF = 100 s" (GOLD numbers). It clears on {sub}.
> {sub} / {nfactor}: `P_fail/s` becomes `N P_fail`, copied from s2's formula (brought back small at the top). {pfail}: `P_fail` unfolds into ch4's `(T_0/T_c) e^(−(T_c − t_su)/τ)`, giving `MTBF = 1/(N (T_0/T_c) e^(−(T_c − t_su)/τ))`.
> {invert} / {over}: `T_0/T_c` turns over: T_c (YELLOW) rises into the numerator and T_0 drops beside N. {sign}: the exponent's minus sign glows RED and fades out; the exponential moves up beside T_c. {result}: the result settles, centred, verbatim from p. 114: `MTBF = 1/(P_fail/s) = T_c e^((T_c − t_su)/τ) / (N T_0)`.
> {top}: the numerator glows. {tres}: a brace under `T_c − t_su`, labelled "t_res" (FG), with ch4 s6's small bar beside it (t_res FG + t_su GOLD, the YELLOW T_c arrow over both). {bottom}: `N T_0` glows.
> {curve}: the formula moves up. Below it, axes: "T_c" across, "MTBF" up. {grow}: a GOLD curve draws itself left to right, flat at first, then shooting up; a YELLOW dot slides right along the T_c axis and its height races up the curve.
> {nlin}: a DIM copy of the curve at half height, labelled "N doubled: MTBF halved"; then the YELLOW dot moves a short step right on the original curve, and its height multiplies many times over.

[c5.mtbf.1] {flip} So instead of failures per second, we measure seconds per failure. {name} System reliability is usually measured that way, as the mean time between failures, or em-tee-bee-eff for short. {recip} It's simply the reciprocal of the probability of failure per second. {hundred} For example, if a system fails once in every hundred seconds on average, its mean time between failures is a hundred seconds.

[c5.mtbf.2] {sub} Now put in what we know. {nfactor} The number of failures per second is N times pee-fail. {pfail} And pee-fail is last time's formula, tee-nought over the clock period, times an exponential that decays as the resolution time grows. {invert} Take the reciprocal, and two things change. {over} Tee-nought over the clock period turns upside down. {sign} And the minus sign in the exponent disappears, so the decaying exponential becomes a growing one. {pause}

[c5.mtbf.3] {result} Here's the result. {top} On top is the clock period, times an exponential. {tres} Its exponent is the clock period minus the set-up time, which is the resolution time from last time, divided by tau. {bottom} Underneath is N, times tee-nought.

[c5.mtbf.4] {curve} Now watch what the clock period does. {grow} Make it longer, and the resolution time grows, so the mean time between failures grows exponentially. {nlin} The input's rate, N, only divides it. If the input changes twice as often, the mean time halves. But a slightly longer clock period can multiply it many times over.

## Scene 4 · The example, set up (ch5_s4_example)

> {card}: p. 114's example as a card on the left, titled "Metastability - Example". {chars}: a DIM sub-heading, "flip-flop characteristics". Its lines arrive on their words: {tau} `τ = 200 ps`, {tnought} `T_0 = 150 ps`, {tsu} `t_su = 500 ps` (GOLD, the window's colour), {rate} `N = 0.2 changes per second, on average`. With {rate}, s2's time axis returns small under the card, a BLUE tick every 5 s: "about once every 5 s" (1/0.2 = 5).
> {question}: right half, YELLOW: "How long must the clock period be for the MTBF to exceed 1 year?" with `T_c = ?` under it. Hold through the pause.
> {year}: a GOLD sum builds under the question: `365 × 24 × 3600 = 31,536,000 s` (checked); {about}: `1 year ≈ 31.5 × 10⁶ s`, as on the slide.
> {sub}: s3's result, `MTBF = T_c e^((T_c − t_su)/τ) / (N T_0)`, is copied into the right half and each symbol is replaced by its value, flying in from the card. {left}: `31.5 × 10⁶` takes MTBF's place. {right}: `500×10⁻¹²` and `200×10⁻¹²` land in the exponent. {below}: `(0.2)150 × 10⁻¹²` lands underneath. Result, in the slide's layout: `31.5 × 10⁶ = T_c e^((T_c − 500×10⁻¹²)/(200×10⁻¹²)) / ((0.2)150 × 10⁻¹²)`. Both T_c stay as symbols, YELLOW.
> {unknown}: both T_c pulse once.
> {twice} / {outside}: a YELLOW ring round the T_c outside the exponential; {inside}: a second ring round the T_c in the exponent.
> {noclosed}: RED, under the equation, the slide's words: "This equation has no closed form solution". {guess}: GREEN tag beside it, "trial and error". The equation stays for s5.

[c5.example.1] {card} Here's the slide's worked example. {chars} The flip-flops in a synchroniser have these characteristics. {tau} Tau is two hundred picoseconds. {tnought} Tee-nought is a hundred and fifty picoseconds. {tsu} And the set-up time is five hundred picoseconds. {rate} The input changes zero point two times per second, on average. That's about once every five seconds.

[c5.example.2] {question} How long must the clock period be, for the mean time between failures to exceed one year? {pause} {year} First, we need a year in seconds. That's three hundred and sixty-five days, times twenty-four hours, times three thousand six hundred seconds in an hour. {about} It comes to about thirty-one point five million seconds.

[c5.example.3] {sub} Now substitute everything into the formula. {left} On the left is our target, thirty-one point five million seconds. {right} On the right, the set-up time and tau go into the exponent, in seconds. {below} And underneath, N times tee-nought is zero point two, times a hundred and fifty picoseconds. {unknown} The only unknown left is the clock period.

[c5.example.4] {twice} But look where it appears. {outside} Once outside the exponential, {inside} and once inside it. {noclosed} There's no way to rearrange the equation to get the clock period on its own, so it has no closed form solution. {guess} So we do what the slide does, and find it by trial and error. {pause}

## Scene 5 · Trial and error (ch5_s5_trial)

> s4's equation, compact, across the top. {start}: under it, a two-column table, header "T_c" | "MTBF", and a GOLD target line under the header: "target: 1 year ≈ 365 days". Every row was computed from the slide's formula (Python 3.11.9).
> Rows arrive on their words: {two} `2.0 ns | 1.4 days` (RED cross); {twofive} `2.5 ns | 21 days` (RED cross); {three} `3.0 ns | 311 days` (RED cross, small "just short"); {answer} `3.04 ns | 384 days ≈ 1.05 years` (GREEN tick). T_c values YELLOW, MTBF values GOLD.
> {slide}: an answer box under the table: `T_c ≥ 3.04 ns` and `f_c ≤ 329 MHz` (checked: 1/3.04 ns = 328.9 MHz). {exact}: a small DIM note under it: "exact boundary: 3.03 ns" (bisection: 3.0303 ns).
> {growth}: small GOLD arrows between the first three rows: "×15", "×15" (checked: 21.2/1.4 = 15.2, 310.6/21.2 = 14.6).
> {pertau}: a ruler along the bottom, a T_c axis cut into steps of τ = 200 ps, each step labelled "× e ≈ 2.7" for the exponential part. {perns}: five steps bracketed: "1 ns = 5τ → e⁵ ≈ 148" (checked: 148.4). {cheap}: the bracket glows GREEN.
> {check}: the table and ruler slide left and dim. A sanity check builds on the right: {pfail} `P_fail at 3.04 ns ≈ 1.5 × 10⁻⁷ ≈ 1 in 6.6 million` (checked: 1.51 × 10⁻⁷); {changes} `0.2 per second × 31.5 × 10⁶ s ≈ 6.3 million changes per year` (checked: 6.31 million); {once} `→ just under 1 failure per year` with a GREEN tick (checked: 0.95).

[c5.trial.1] {start} So make a guess, work out the mean time between failures, and compare it with a year. {two} Try two nanoseconds first. That gives about one point four days, far too short. {twofive} Two and a half nanoseconds gives about twenty-one days. Better, but still short. {three} Three nanoseconds gives about three hundred and eleven days, just short of a year. {pause}

[c5.trial.2] {answer} Three point oh four nanoseconds gives about three hundred and eighty-four days. That's just over a year. {slide} So that's the slide's answer. The clock period must be at least three point oh four nanoseconds, a frequency of at most about three hundred and twenty-nine megahertz. {exact} Solved more precisely, the boundary is three point oh three nanoseconds.

[c5.trial.3] {growth} Look how fast those numbers grew. {pertau} Most of that comes from the exponential. Each extra tau of waiting, two hundred picoseconds, multiplies the exponential by about two point seven. {perns} So one extra nanosecond, which is five taus, multiplies it by about a hundred and fifty. {cheap} A small slowdown buys a lot of reliability.

[c5.trial.4] {check} Here's a check that makes sense of the answer. {pfail} At three point oh four nanoseconds, pee-fail is about one in six point six million. {changes} And an input that changes every five seconds changes about six point three million times a year. {once} So we expect just under one failure a year, which is exactly what we asked for.

## Scene 6 · More flip-flops (ch5_s6_cascade)

> s5's answer box, `T_c ≥ 3.04 ns`, small at the upper left; on {long} a RED tag beside it, "too long?".
> {cascade}: ch4 s5's synchroniser returns, full width, in its styling: D0 (BLUE) → FF0 → D1 (TEAL) → FF1 → Q (GREEN), one YELLOW CLK line. {chain}: Q's wire extends, a third flip-flop (`make_ff()`) slides in after FF1, then a faded fourth with "…"; the GREEN Q label moves to the last output, and the CLK line stretches to reach every triangle. A brace under FF0, "input flip-flop"; a brace under the rest, "K additional flip-flops".
> {each}: a GOLD tag "P_fail" appears above each additional flip-flop, one after another. {kfold}: the tags merge into p. 115's line, verbatim: `P_fail_K = (P_fail)^K`. {kone}: the chain trims back to FF0 and FF1, with "K = 1: Part 4's synchroniser", then grows again.
> {persec}: `Hence, P_fail_K/s = N P_fail_K = N(P_fail)^K`. {mtbfk}: `MTBF = 1/(N(P_fail)^K)`. Both verbatim from p. 115.
> {catch} / {low}: the slide's condition under them, YELLOW: "P_fail ≪ 1". {half}: RED example at the left: `(0.5)² = 0.25`, `(0.5)³ = 0.125`, with "each flip-flop only halves it". {tiny}: GREEN example at the right: `(10⁻⁷)² = 10⁻¹⁴`, with "10 million times smaller".
> {ours}: a small panel, headed in DIM italics "by the slide's formula (ours)": {two} `K = 2`; {keep} `T_c = 3.04 ns → MTBF ≈ 7 million years` (checked: 2.2 × 10¹⁴ s); {shrink} `MTBF = 1 year → T_c ≈ 1.6 ns`, beside a DIM `3.03 ns` for K = 1 (checked by bisection: 1.593 ns, where P_fail = 4.0 × 10⁻⁴).

[c5.cascade.1] {long} But for the rest of the system, a clock period of three nanoseconds may be too long. {cascade} When the clock period this needs is excessive, the slide's answer is to cascade more flip-flops. {chain} After the input flip-flop, add a third flip-flop, or a fourth, in a chain, like a longer shift register.

[c5.cascade.2] {each} A failure now has to get through every one of them. {kfold} The slide treats each additional flip-flop as one more gamble with the same odds. So with K additional flip-flops in the chain, the probability of failure is pee-fail to the power K. {kone} With K equal to one, that's the synchroniser we already had. {persec} Per second, multiply by N, as before. {mtbfk} So the mean time between failures is one over N times pee-fail to the power K.

[c5.cascade.3] {catch} There's a catch. {low} For this to work with a reasonable number of flip-flops, pee-fail has to be much lower than one. {half} If it were a half, squaring it would only give a quarter. Each extra flip-flop would only cut the chance in half, and you'd need a long chain. {tiny} But square ten to the minus seven, and you get ten to the minus fourteen, ten million times smaller, from one more flip-flop.

[c5.cascade.4] {ours} Here's what that means for our example, with the formula from the slide. {two} Add two extra flip-flops, so K is two. {keep} At three point oh four nanoseconds, the mean time between failures becomes about seven million years. {shrink} Or keep the one-year target instead, and the clock period can shrink from about three nanoseconds to about one point six nanoseconds. {pause}

## Scene 7 · Recap and next (ch5_s7_recap)

> {recap}: a small "Recap" heading. Then one small visual per sentence, each in its scene's colours and styling, laid out in two rows (three, then two), with the sentence's short line under it:
> {r1}: s2's time axis with BLUE change ticks, their small GOLD dice and the bracket "N per second" — "failures per second = N × P_fail".
> {r2}: s3's result `MTBF = T_c e^((T_c − t_su)/τ) / (N T_0)` with the GOLD exponential curve beside it — "MTBF: seconds per failure".
> {r3}: s4's substituted equation with its two YELLOW T_c rings, the RED "no closed form" under it — "T_c inside and outside the exponential".
> {r4}: s5's table, rows 2.0, 2.5 and 3.0 ns RED-crossed, 3.04 ns GREEN-ticked — "trial and error: T_c ≥ 3.04 ns".
> {r5}: s6's chain of K + 1 flip-flops with `MTBF = 1/(N(P_fail)^K)` — "cascade: needs P_fail ≪ 1".
> {next}: the five shrink away. {more}: ch6 s1's hero, small and faint: a rounded box "the system" with a conveyor line through it, and small rounded squares in the task colours (BLUE, GREEN, TEAL, FG) queuing on the left to enter it one at a time. Then the end card: hold about 8 seconds after the last word, music carrying it.

[c5.recap.1] {recap} Here's a quick recap. {r1} If the input changes N times a second, the failures per second are N times pee-fail. {r2} The mean time between failures is the reciprocal, seconds per failure, and it grows exponentially with the clock period. {r3} In the slide's example, the clock period appears inside and outside the exponential, so there's no closed form solution. {r4} By trial and error, a year needs a clock period of at least three point oh four nanoseconds.

[c5.recap.2] {r5} And cascading more flip-flops raises pee-fail to a power, which works well when pee-fail is already much less than one. {pause} {next} Next time, we turn from making circuits reliable to making them fast. {more} How can a circuit finish more work per second, without faster flip-flops? {pause}
