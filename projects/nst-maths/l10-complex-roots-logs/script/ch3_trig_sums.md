# Chapter 3 · Powers and sums with exponentials

NST IA Mathematics, Lecture 10 (Powers, Logarithms and Oscillations), part 3 of 8. Source: notes
(`Chapter234_to_annotate.pdf`) PDF pp. 22–23, printed pp. 103–104 (cos³θ, (79), Example 30), with
L9's Example 27 (p. 15); scan L10 pp. 5–6; recording 00:13:36–00:19:14; Examples Sheet I, F12, F13
and F17 (PDF pp. 8–9).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch3_s1_hook)

> Title card: "Powers, Logarithms and Oscillations", course line "NST IA Mathematics · Lecture 10", part line "Part 3 · Powers and sums with exponentials".
> {last}: ch2 s6's picture, small, on the Argand plane from ch1 s2: the unit arrows e^{iθ} (GOLD) and e^{−iθ} (PURPLE) turning opposite ways, tip to tail, landing on the real axis at 2cos θ (BLUE). Beside it, on {cos}, `cos θ = ½(e^{iθ} + e^{−iθ})` with `(77)`; on {sin}, `sin θ = (1/2i)(e^{iθ} − e^{−iθ})` with `(78)`. Equation numbers small and DIM, i PINK.
> {today}: the two formulas shrink into a "toolbox" in the top-left corner. It stays there all chapter: s2 and s5 pull copies out of it.
> {q1}: a left card, `∫ cos³θ dθ = ?` (YELLOW "?"). {easy}: under it, `∫ cos 3θ dθ = ⅓ sin 3θ + C` with a tick. {power}: the exponent ³ of cos³θ gets a RED circle.
> {q2}: a right card, `1 + cos θ + cos 2θ + … + cos(N−1)θ = ?`, cosines BLUE.
> {both}: a small GOLD `e^{iθ}` badge lands on each card.

[c3.hook.1] {title} This is part three of our lecture on powers, logarithms and oscillations. {pause} {last} Last time, we wrote cosine theta with exponentials. {cos} It's E to the eye theta, plus E to the minus eye theta, all over two. {sin} And sine theta is their difference, over two eye.

[c3.hook.2] {today} Today we put those two formulas to work, on two questions. {q1} First, how do you integrate cosine cubed of theta? {pause} {easy} The cosine of three theta integrates in one line. {power} A power of cosine is harder. {q2} Second, what is one, plus cosine theta, plus cosine two theta, and so on, up to the cosine of N minus one, theta? {pause} {both} Both get much easier once you write the cosines as exponentials.

## Scene 2 · Cosine cubed (ch3_s2_cube)

> Layout: the algebra on the left, the Argand plane from ch1 s2 on the right (axes Re and Im, faint grid, DIM unit circle). Throughout: e^{+…iθ} terms GOLD, e^{−…iθ} terms PURPLE, cosines BLUE, i PINK.
> cube.1, {swap}: `cos³θ = [½(e^{iθ} + e^{−iθ})]³`, the bracket a copy pulled out of the toolbox's (77). {pascal}: Pascal's row `1 3 3 1` pops in above (one row up from ch2 s4's `1 4 6 4 1`). {eighth}: the ½ cubes into ⅛.
> cube.2: the four terms appear one per mark ({t1}…{t4}), as in the notes: `= ⅛[e^{3iθ} + 3e^{2iθ}e^{−iθ} + 3e^{iθ}e^{−2iθ} + e^{−3iθ}]`. {collapse}: the middle products shrink in place to `3e^{iθ}` and `3e^{−iθ}`, with `2θ − θ = θ` and `θ − 2θ = −θ` flashing YELLOW.
> cube.3, {pairs}: arcs link the mirror pairs ({p3}, {p1}), and the line regroups: `= ⅛[e^{3iθ} + e^{−3iθ}] + ⅜[e^{iθ} + e^{−iθ}]`. {arrows}: on the plane, in ch2 s6's styling, the GOLD arrow at angle 3θ and the PURPLE one at −3θ go tip to tail and land on the real axis at 2cos 3θ; then the pair at ±θ lands at 2cos θ (BLUE dots). θ drifts a little: the arrows turn opposite ways, and the tips slide along the real axis without leaving it.
> cube.4, {result}: each bracket turns into `2cos 3θ` and `2cos θ`. {box}: `= ¼cos 3θ + ¾cos θ`, boxed YELLOW. {gone}: the RED-circled ³ from the hook fades away.
> cube.5, {answer}: under the box, `∫ cos³θ dθ = (1/12) sin 3θ + ¾ sin θ + C`, each term dropping out of its cosine term. {check}: `θ = 0:`, then {lhs} `cos³0 = 1`, {rhs} `¼ + ¾ = 1`, and a tick.
> Checked (sympy 1.14.0, Python 3.11.9): every line equals cos³θ, and the integral differentiates back to cos³θ.

[c3.cube.1] {start} Let's start with cosine cubed. {swap} Replace the cosine by its exponential form, and cube it. {pascal} Cubing a sum of two terms uses the binomial row one, three, three, one. {eighth} And one half, cubed, is one eighth.

[c3.cube.2] {terms} That gives four terms. {t1} E to the three eye theta. {t2} Three times E to the two eye theta, times E to the minus eye theta. {t3} Three times E to the eye theta, times E to the minus two eye theta. {t4} And E to the minus three eye theta. {collapse} Multiplying adds the angles, so the middle two simplify. {mid} They become three E to the eye theta, and three E to the minus eye theta.

[c3.cube.3] {pairs} Now group the terms in mirror pairs. {p3} E to the three eye theta goes with E to the minus three eye theta. {p1} And E to the eye theta goes with E to the minus eye theta. {picture} You saw last time why a pair like this is special. {arrows} Two arrows turning opposite ways, placed tip to tail, always land on the real axis. {twice} Each pair adds up to twice a cosine.

[c3.cube.4] {result} So we get one eighth of twice cosine three theta, plus three eighths of twice cosine theta. {box} That's one quarter cosine three theta, plus three quarters cosine theta. {pause} {gone} The power has gone. Only cosines of multiples of theta are left.

[c3.cube.5] {integrate} And those integrate in one line. {answer} The integral of cosine cubed is one twelfth of sine three theta, plus three quarters of sine theta, plus a constant C. {check} Here's a quick check, at theta equals zero. {lhs} Cosine cubed of zero is one, {rhs} and one quarter plus three quarters is one too. {pause}

## Scene 3 · A sum of cosines as a real part (ch3_s3_sum)

> {sigma}: top centre, `S_N = Σ_{k=0}^{N−1} cos kθ`. {written}: it unrolls into the lecturer's handwritten line (scan p. 5), `= 1 + cos θ + cos 2θ + … + cos(N−1)θ`, cosines BLUE.
> {cosk}: `cos kθ = Re[e^{ikθ}]` drops in. {swap}: the first line becomes `S_N = Re[Σ_{k=0}^{N−1} e^{ikθ}]`, with `Re` BLUE and {eq} `(79)` small and DIM. (On screen it's always `Re[…]`, as in the lecturer's handwriting; the notes print ℜ.)
> sum.3, {terms}: the inside, written out as on the scan, `1 + e^{iθ} + e^{2iθ} + …`. {times}: small curved GOLD arrows labelled `× e^{iθ}` hop from each term to the next, then `= Σ_{k=0}^{N−1} (e^{iθ})^k`. {gp}: tags "geometric progression", "first term 1", "common ratio e^{iθ}".
> sum.4 (ours; the algebra shrinks to the top-left): the Argand plane from ch1 s2. {six}: six unit arrows (GOLD), N = 6 and θ = π/6, tip to tail from 0, the first along the real axis. {curl}: each one turned θ further than the last, so the chain curls up and to the left. {end}: a YELLOW dot at the chain's end, labelled `Σ e^{ikθ}`.
> {shadow}: each arrow drops its shadow onto the real axis, BLUE segments laid end to end: 1, cos θ, cos 2θ, … (cos 3θ = 0 is a single point, and the last two segments point back to the left). {total}: a BLUE bracket from 0 to the end's shadow, labelled `S_N`. For N = 6, θ = π/6 it lands at exactly 1 (checked: the chain ends at 1 + 3.732i).
> Keep this chain: s6 brings it back.

[c3.sum.1] {sum} Now the second question. {sigma} It's the sum, from K equals zero to N minus one, of cosine of K theta. {written} Written out, that's one, plus cosine theta, plus cosine two theta, and so on, up to the cosine of N minus one, theta. {hard} As cosines, it's hard to see where to start.

[c3.sum.2] {trick} Here's the trick. Each cosine is the real part of an exponential. {cosk} Cosine of K theta is the real part of E to the eye K theta. {swap} So the cosine sum is the real part of a sum of exponentials. {eq} The notes call this equation seventy-nine.

[c3.sum.3] {inside} Look at the sum inside. {terms} One, plus E to the eye theta, plus E to the two eye theta, and so on. {times} Each term is the one before, times E to the eye theta. {gp} So it's a geometric progression, with first term one, and common ratio E to the eye theta. {pause}

[c3.sum.4] {chain} Here's a picture. Each term is an arrow of length one, so place the arrows tip to tail. {six} Here are six of them, with theta equal to pi over six. {curl} Each arrow turns theta further than the one before, so the chain curls round. {end} The end of the chain is the whole complex sum. {shadow} Now drop each arrow's shadow onto the real axis. The shadow of an arrow is its cosine. {total} So the shadow of the whole chain is exactly our cosine sum.

## Scene 4 · Geometric series, recalled (ch3_s4_geometric)

> {formula}: centre, `Σ_{k=0}^{N−1} aλ^k = a (1 − λ^N)/(1 − λ)`, λ GOLD (it will become e^{iθ}). The notes call this sum S_N too; on screen it's named G, so it can't be mixed up with the cosine sum.
> geo.2, the proof (ours, A-level), as two aligned rows. First `G = a + aλ + aλ² + … + aλ^{N−1}`; on {shift}, a copy slides down and one place to the right: `λG = aλ + aλ² + … + aλ^{N−1} + aλ^N`.
> {subtract}: matching terms strike out in pairs, leaving `G − λG = a − aλ^N`. {divide}: `G(1 − λ) = a(1 − λ^N)`, then the formula again.
> {complex}: a small tag, "λ can be complex: only + and × were used".
> geo.3, {flag}: the denominator `1 − λ` pulses. {one}: a small RED flag, `λ ≠ 1`, plants itself beside the formula. The formula and its flag shrink to a corner and stay for s5 and s6.

[c3.geo.1] {recall} Let's recall how to sum a geometric progression. {setup} Take N terms, with a first term, and a common ratio, lambda. {formula} The sum is the first term, times one minus lambda to the N, all over one minus lambda.

[c3.geo.2] {why} Here's why, in one line. {shift} Multiply the sum by lambda, and every term moves one place along. {subtract} Subtract the two, and almost everything cancels. Only the first term and the very last one are left. {divide} Then divide by one minus lambda. {complex} Nothing in that argument needs lambda to be real. So it works just as well for a complex ratio, like E to the eye theta.

[c3.geo.3] {flag} But that last step divides by one minus lambda. {pause} {one} So it only works when lambda is different from one. {keep} Keep that in mind. It's going to matter.

## Scene 5 · Example 30: a real denominator (ch3_s5_conjugate)

> Header "Example 30", as in the notes. Top-left: s3's `S_N = Re[Σ e^{ikθ}]`. Top-right: s4's formula with its RED `λ ≠ 1` flag. The notes write z = exp(iθ) and then λ = z; the lecturer switched to λ (scan p. 6), and so do we, since z is the complex variable everywhere else.
> conj.1, {sub}: `a = 1` and `λ = e^{iθ}` (GOLD) slot into s4's formula (TransformFromCopy). {lamN}: `λ^N = (e^{iθ})^N = e^{iNθ}`. {fraction}: `S_N = Re[(1 − e^{iNθ}) / (1 − e^{iθ})]`.
> conj.2, {bottom}: the denominator glows. A small inset on the Argand plane shows the point 1 − e^{iθ}, off the real axis, with its imaginary part PINK; a YELLOW "?" sits over `Re`. {recall}: a small card from L9 (Example 27, notes p. 15): `(3 + i)/(1 − i) · (1 + i)/(1 + i) = (2 + 4i)/2 = 1 + 2i`, the `(1 + i)/(1 + i)` YELLOW on {trick}.
> conj.3, {conj}: `× (1 − e^{−iθ})/(1 − e^{−iθ})` joins the fraction, as in the notes, e^{−iθ} PURPLE. {bottom2}: the bottom expands in place, `(1 − e^{iθ})(1 − e^{−iθ}) = 2 − e^{iθ} − e^{−iθ}` ({ones}: the two 1s merge into 2; {cross}: the cross terms). conj.4, {pair}: the GOLD/PURPLE pair glows, and (77) comes out of the toolbox. {real}: `= 2 − 2cos θ = 2(1 − cos θ)`, BLUE, tagged "real". {mod}: small, beside it, `= |1 − e^{iθ}|²`.
> conj.5: the top expands one term per mark ({t1}…{t4}) into `1 − e^{−iθ} − e^{iNθ} + e^{i(N−1)θ}`. {adds}: the last term forms from `e^{iNθ} · e^{−iθ}`, with `Nθ − θ = (N − 1)θ` flashing YELLOW.
> {done}: the end state, the notes' line with the bottom already rewritten: `S_N = Re[(1 − e^{−iθ} − e^{iNθ} + e^{i(N−1)θ}) / (2(1 − cos θ))]`. It carries over to s6.
> Checked (sympy 1.14.0): both expansions, and |1 − e^{iθ}|² = 2(1 − cos θ).

[c3.conj.1] {ex} Now put the two together. This is example thirty in the notes. {sub} The first term is one, and the common ratio, lambda, is E to the eye theta. {lamN} Lambda to the N is then E to the eye times N theta. {fraction} So the cosine sum is the real part of one minus E to the eye times N theta, all over one minus E to the eye theta.

[c3.conj.2] {which} So what is the real part of that fraction? {pause} {bottom} The trouble is the bottom. It's complex, and the real part of a fraction is easy to read off only when the bottom is real. {recall} You met this in example twenty-seven, when you divided by one minus eye. {trick} The trick was to multiply the top and the bottom by the conjugate, one plus eye.

[c3.conj.3] {same} We do the same here. {conj} The conjugate of one minus E to the eye theta is one minus E to the minus eye theta. {bottom2} Multiply out the bottom first. {ones} One times one is one, and E to the eye theta, times E to the minus eye theta, is one too. {cross} The cross terms are minus E to the eye theta, and minus E to the minus eye theta.

[c3.conj.4] {pair} There's our mirror pair again, adding up to twice cosine theta. {real} So the bottom is two times, one minus cosine theta, a real number. {pause} {mod} That's no accident. Any number times its conjugate is its modulus squared, which is real.

[c3.conj.5] {top} Now the top. It has four terms. {t1} One, {t2} minus E to the minus eye theta, {t3} minus E to the eye times N theta, {t4} and E to the eye times N theta, times E to the minus eye theta. {adds} When you multiply, the angles add, so that last one is E to the eye, N minus one, theta. {done} Four terms on top, and a real number underneath.

## Scene 6 · The answer, and θ = 2πm (ch3_s6_result)

> Carry s5's end state. {euler}: each top term unfolds by (71) into a cosine plus i times a sine, as the digest shows the lecturer's step: `1 − cos θ + i sin θ − cos Nθ − i sin Nθ + cos(N−1)θ + i sin(N−1)θ`, cosines BLUE, sine terms PINK. {drop}: the PINK terms slide down and park in a PINK row at the bottom edge. {left}: `S_N = [1 − cos θ − cos Nθ + cos(N−1)θ] / [2(1 − cos θ)]`.
> res.2, {half}: the `1 − cos θ` on top and the one underneath glow, and split off as `½`. {box}: boxed YELLOW, `S_N = ½ + [cos(N−1)θ − cos Nθ] / [2(1 − cos θ)]`, its top lit on {top} and its bottom on {bottom}.
> res.3, the check (ours). Left, on {chain}: a three-arrow chain in s3's styling with θ = π/2 (right, up, left), ending at i; its shadow goes out to 1 and back to 0. {direct}: `1 + 0 + (−1) = 0`. Right, on {formula}: `½ + (cos π − cos(3π/2)) / (2(1 − cos(π/2))) = ½ + (−1 − 0)/2 = 0`, and a tick.
> res.4, {flag}: the RED `λ ≠ 1` flag returns. {lam}: the lecturer's fill (scan p. 6), `λ = 1 ⇔ θ = 2πm, m ∈ ℤ`, with the 2πm TEAL (whole turns, as in ch1). {sweep}: s3's six-arrow chain comes back, and θ grows from π/6 to 2π: the chain curls tighter, closes up, winds round, and at {straight} lies flat as one straight line of six arrows along the real axis. {ones}: the scan's line `S_N = 1 + 1 + … + 1 = N`, a brace under the ones labelled `N` (GOLD, a length, as in ch8 s4's straight chain; TEAL stays for the whole turns, 2πm). {zero}: in the boxed formula the bottom `2(1 − cos θ)` turns RED: `= 0`.
> res.5 (ours), {sines}: the parked PINK row rises into the imaginary part, `Σ_{k=0}^{N−1} sin kθ = [sin θ − sin Nθ + sin(N−1)θ] / [2(1 − cos θ)]`, PINK, with a small tag "F13(b)" on {sheet}.
> Checked (Python 3.11.9): the boxed form, the long form and the sine form agree with the direct sums to 1e−14 for N = 1, 2, 3, 4, 5, 6, 8, 13 at seven values of θ; θ = 2πm (m = 1, 2, −1) gives N; N = 3, θ = π/2 gives 0.

[c3.res.1] {real} Since the bottom is now real, we only need the real part of the top. {euler} Write each exponential as a cosine, plus eye times a sine. {drop} The cosines are real. The sines all come with an eye, so they drop out. {pause} {left} On top, that leaves one, minus cosine theta, minus cosine N theta, plus cosine of N minus one, theta.

[c3.res.2] {split} One last tidy-up. {half} The one minus cosine theta on top matches the bottom, so it splits off as one half. {box} The cosine sum is one half, plus a fraction. {top} On top, cosine of N minus one, theta, minus cosine N theta. {bottom} Underneath, two times, one minus cosine theta. {pause=1.5}

[c3.res.3] {check} Let's check it on a small case. Take N equal to three, and theta equal to pi over two. {chain} The arrows go right, then up, then left. {direct} The cosines are one, zero and minus one, so the sum is zero. {formula} In the formula, the top is minus one minus zero, and the bottom is two. One half, minus one half, is zero. {pause}

[c3.res.4] {flag} Now remember the red flag. {lam} Lambda, E to the eye theta, equals one exactly when theta is a whole number of turns, two pi M, for an integer M. {sweep} Watch the chain as theta grows to a full turn. {straight} At two pi, every arrow points the same way again. {ones} Every term is one, so the sum is one, plus one, plus one, N times. It's just N. {zero} And that's exactly where the bottom of the formula is zero. {pause}

[c3.res.5] {free} One more thing, for free. {sines} The sines we dropped add up to the sum of sine K theta. {same} Keep them, and the same working sums the sines. {sheet} That comes up on the examples sheet.

## Scene 7 · On the examples sheet (ch3_s7_tryit)

> Three question cards from Examples Sheet I (pp. 8–9), quoted verbatim, one per clip. Each hint grows out of a small icon from this chapter or ch2. Footer on {solutions}: "Full solutions: Part 8".
> try.1, {f12}: "F12. Express: i. sin 3θ in terms of powers of sin θ; and ii. sin⁵ θ in terms of sin θ, sin 2θ, sin 3θ etc." Hint (i): ch2's unit arrow at angle 3θ, `(cos θ + i sin θ)³`, then `Im` (PINK), then `cos²θ = 1 − sin²θ`. Hint (ii), on {f12b}: `sin⁵θ = [(e^{iθ} − e^{−iθ})/(2i)]⁵`, Pascal's row `1 5 10 10 5 1`, and s2's mirror pair as a difference, `e^{5iθ} − e^{−5iθ} = 2i sin 5θ`.
> try.2, {f13}: "F13. Evaluate the following sums: (a) Σ_{n=1}^{5} cos nθ (b) Σ_{n=1}^{5} sin nθ (c) Σ_{n=1}^{5} rⁿ cos nθ ." Hint, on {first}: s3's chain, now five arrows starting at e^{iθ}, with "first term e^{iθ}, ratio e^{iθ}, five terms". {second}: (b) gets `Im` of the same sum (PINK). {third}: (c) gets "ratio r e^{iθ}", the arrows shrinking by r at each step, so the chain becomes a spiral.
> try.3, {f17}: "F17. If ω³ = 1, find all values of 1 + ω + ω². Generalise your result to the case ωⁿ = 1 for n a positive integer." Hint, on {gp}: "geometric progression, ratio ω". {careful}: s4's RED flag comes back, now reading `ω = 1 ?`. No arrows here: Part 8 draws them.

[c3.try.1] {sheet} Three questions on the first examples sheet use these ideas. {f12} In question F twelve, for sine of three theta, use De Moivre's theorem with the power three, and take the imaginary part. Then replace cosine squared by one minus sine squared. {f12b} For sine to the fifth of theta, raise the sine formula to the fifth power, and pair the mirror terms, as we did for cosine cubed. This time each pair is a difference, which gives a sine.

[c3.try.2] {f13} Question F thirteen has three sums, each running from one to five. {first} The cosine sum is the real part of a geometric progression, whose first term is E to the eye theta. {second} The sine sum is the imaginary part of the same progression. {third} In the third sum, the common ratio becomes R times E to the eye theta.

[c3.try.3] {f17} In question F seventeen, omega cubed is one. {gp} One plus omega plus omega squared is a geometric progression, with ratio omega. {careful} Watch out for omega equal to one. That's our exception again. {general} Then do the same when omega to the N is one. {solutions} Full solutions are in part eight.

## Scene 8 · Recap (ch3_s8_recap)

> Five small panels (a row of three over a row of two), one per recap sentence. Each lights on its mark and dims when the next one arrives, and is a small version of the visual that taught it, in the same colours, with its short line under it:
> {r1}: s2's mirror pairs, GOLD and PURPLE arrows tip to tail landing on the real axis; line `cos³θ = ¼cos 3θ + ¾cos θ`.
> {r2}: s3's curling chain of six arrows with its BLUE shadow; line `S_N = Re[Σ e^{ikθ}]`.
> {r3}: s4's two shifted rows with the middle struck out, and the RED flag; line `λ ≠ 1`.
> {r4}: s5's conjugate step; line `(1 − e^{iθ})(1 − e^{−iθ}) = 2(1 − cos θ)`, tagged "real".
> {r5}: s6's boxed formula beside the straight chain of N arrows; line `θ = 2πm: S_N = N`, 2πm TEAL.
> {next}: the panels clear. ch1's point 2i (YELLOW) on the Argand plane, and a GOLD arrow labelled `e^w` reaching it from a `w = ?`. {many}: a TEAL column of faint "?" stacks up above and below the `w`, a hint of Part 4's ladder. Hold the end card for ~8 s after the last word; the music carries it.

[c3.recap.1] {recap} Let's recap. {r1} To remove a power of cosine, write the cosine with exponentials, expand, and pair the mirror terms back into cosines. {r2} A sum of cosines is the real part of a sum of exponentials, and here that's a geometric progression. {r3} The formula divides by one minus lambda, so lambda must be different from one. {r4} Multiplying by the conjugate makes the bottom real, so you can read off the real part. {r5} And when theta is a whole number of turns, every term is one, and the sum is N. {pause}

[c3.recap.2] {next} Next time, we run the exponential backwards. {log} What is the logarithm of a complex number? {many} And why does it have infinitely many values? {pause}
