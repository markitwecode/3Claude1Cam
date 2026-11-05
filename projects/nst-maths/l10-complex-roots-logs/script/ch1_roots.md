# Chapter 1 · Roots of a complex number

NST IA Mathematics, Lecture 10 (Powers, Logarithms and Oscillations), part 1 of 8. Source: notes `Chapter234_to_annotate.pdf` PDF pp. 19–20 (printed 100–101: the remark under Figure 23, Example 28), refresher PDF pp. 16–19 (printed 97–100); Lecture 10 scan pp. 1–3; Lecture 9 scan pp. 13, 15; recording 00:00:00–00:07:45; Examples Sheet I, F15 and F16 (PDF pp. 8–9).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card (`lib.titles`) on {title}: "Powers, Logarithms and Oscillations", course line "NST IA Mathematics · Lecture 10", part line "Part 1 · Roots of a complex number".
> {real}: a real number line across the middle (ticks −3 … 3), with `x^5 = 32` above it. On {two} one GOLD dot drops onto 2, labelled `x = 2`. Nothing else appears on the line: one real answer (checked: sympy 1.14.0 `real_roots(x**5 - 32)` → `[2]`).
> {plane}: the number line becomes the Re axis of the Argand plane, the course's running helper (axes labelled Re and Im, faint DIM grid, DIM unit circle; the same helper s2 uses): the Im axis grows up out of 0 and the grid fades in. `x^5 = 32` gives way to `z^5 = 2i`.
> {point}: 2i, a YELLOW dot two units up the Im axis, labelled `2i`. {ask}: a few faint YELLOW "?" marks scattered round the plane. Don't place any answers.
> {frame}: the plane dims to ~0.3. Centre: "everything comes from definitions". {names}: two columns, real → complex, with the same names: `x^5` → `z^5`, `\ln x` → `\ln z`. {diff}: a YELLOW underline under the complex column, "what's different".
> {road}: seven small numbered tiles in a row across the lower third, one per Part: "1 Roots", "2 De Moivre", "3 Sums of cosines", "4 Logarithms", "5 Powers", "6 Oscillations", "7 Circuits". Tile 1 YELLOW, the rest DIM. Fade out.

[c1.hook.1] {title} Powers, logarithms and oscillations. This is lecture ten of the first-year maths course, and part one is about roots.

[c1.hook.2] {real} Start with an easy question. Which real number, ex, has ex to the fifth equal to thirty-two? {pause} {two} The only answer is two. {plane} Now move into the complex plane. {point} Here's the number two eye, two units up the imaginary axis. {ask} Which complex numbers, zed, have zed to the fifth equal to two eye? How many are there, and where? {pause=1.5}

[c1.hook.3] {frame} The lecture opens with a reminder. Everything here comes from definitions. {names} Powers and logarithms keep their real-number names, {diff} but today is about what's different. {road} Here's the road. Roots, then De Moivre's theorem, sums of cosines, logarithms, complex powers, oscillations and circuits.

## Scene 2 · Lecture 9 in one picture (ch1_s2_polar)

> The Argand plane helper fills the right two-thirds (axes Re and Im, DIM grid and unit circle), formulas stacked on the left, as on L10 scan p. 1's recap. The director records the helper's name in STATUS.md.
> {point}: `z = x + iy` and `i^2 = -1`. {plane}: a point z in the first quadrant; dashed BLUE drop to x on the Re axis, dashed PINK line to y on the Im axis (scan p. 1's sketch). {mod}: a GOLD arrow from 0 to z, labelled `|z|`. {arg}: a YELLOW arc from the positive Re axis, labelled `\theta`.
> {trig}: from the picture, `x = |z|\cos\theta` (BLUE) and `y = |z|\sin\theta` (PINK), combining into `z = |z|(\cos\theta + i\sin\theta)`. {euler}: `\cos\theta + i\sin\theta = e^{i\theta}`, `e^{i\theta}` GOLD, a small DIM "(71)" beside it; {expform}: the bracket collapses into it, `z = |z|e^{i\theta}`. {later}: DIM "proved in §6.3". {exp}: small `\exp(i\theta) = e^{i\theta}` under it, then it fades.
> {mult}: Figure 22 (left), in our colours: two arrows z₁ and z₂ with angle arcs θ₁ and θ₂. {product}: the product arrow `z_1z_2` comes out of the two of them: its angle arc is θ₁'s arc and θ₂'s arc laid end to end, its length `|z_1||z_2|` (GOLD). `z_1z_2 = |z_1||z_2|e^{i(\theta_1+\theta_2)}` with DIM "(73)". {conj}: clear back to the one z; its mirror image `z^*` (PURPLE) below the Re axis, with `z^* = |z|e^{-i\theta}`.
> {turn}: the GOLD arrow sweeps one full turn anticlockwise, slowly and at constant speed, a TEAL arc tracing the 2π, and lands back on z. {anyn}: one more turn forwards, then two back, faster. {formula}: `\arg z = \theta + 2\pi n,\ n \in \mathbb{Z}` with `2\pi n` TEAL; {why}: `e^{2\pi i n} = 1` beside it (L9 scan p. 13).
> {principal}: a short θ number line under the plane from −π to π, the interval GREEN: an open circle at −π, a filled GREEN dot at π, label `-\pi < \theta \le \pi`. {ends}: on the plane, the point −1 gets the GREEN label π (not −π). {keep}: everything dims except the TEAL `2\pi n`, which flashes and stays lit. Fade out.

[c1.polar.1] {recap} First, Lecture nine in one picture. {point} A complex number, zed, is ex plus eye why, where eye squared is minus one. {plane} On the Argand diagram, it's the point with ex along the real axis, and why up the imaginary axis. {mod} Its distance from zero is the modulus, mod zed. {arg} Its angle from the positive real axis is the argument. Call it theta.

[c1.polar.2] {trig} So the real part is mod zed times the cosine of theta, and the imaginary part is mod zed times the sine of theta. {euler} Oiler's formula, equation seventy-one, says that cosine theta, plus eye sine theta, is E to the eye theta. {expform} So zed is mod zed, times E to the eye theta. {later} The course proves it in section six point three. {exp} The notes sometimes write the exponential as a function name. It's the same thing.

[c1.polar.3] {mult} This form makes multiplication easy. Take zed one and zed two. {product} Their product has length mod zed one, times mod zed two, and angle theta one plus theta two. {rule} Lengths multiply, and angles add. {conj} The conjugate, zed star, keeps the length and flips the sign of the angle. It's the mirror image of zed in the real axis.

[c1.polar.4] {multi} Now the key fact for today. The argument has many values. {turn} Add two pi to theta, and the arrow sweeps one full turn, and lands exactly where it started. {anyn} Any whole number of turns does the same, forwards or backwards. {formula} So the argument of zed is theta plus two pi N, for any integer N, {why} because E to the two pi eye times N equals one. {pause}

[c1.polar.5] {principal} To pick one value, Lecture nine defined the principal argument, between minus pi and pi. {ends} The lecturer stressed that pi is included and minus pi is left out, so each point gets exactly one. {pause} {keep} Keep an eye on that two pi N. This whole lecture is about what it does.

## Scene 3 · Roots of unity (ch1_s3_unity)

> L9's last example, as on L9 scan p. 15: the working on the left, the Argand plane helper on the right. Here the unit circle is the hero, so draw it at full strength.
> {example}: `z^4 = 1`. {polar}: `z = re^{i\theta}` (r GOLD, θ YELLOW). {power}: `r^4e^{4i\theta} = 1`.
> {mod}: `r^4 = 1 \Rightarrow r = 1` (GOLD). {angle}: `4\theta = 2\pi m,\ m \in \mathbb{Z}`, with `2\pi m` TEAL. {theta}: `\theta = \frac{\pi m}{2}`.
> {m0} … {m4}: a small table, m = 0, 1, 2, 3, 4 → `1`, `i`, `-1`, `-i`, `1`. Each row drops a dot on the unit circle as a GOLD arrow steps a quarter turn: m = 0 at 1 in GREEN (the one with no extra turns), then i, −1, −i in TEAL (the ones the 2πm makes). On {m4} the arrow lands on 1 again: no new dot, the GREEN dot flashes, and the table's last entry reads "1 (again)".
> {quote}: L9's handwritten line, in italics: "Infinitely many in θ, but four distinct in z." (Checked in Python 3.11.9: `cmath.exp(1j*pi*m/2)` gives 1, i, −1, −i, 1 for m = 0…4, each with fourth power 1.)
> {general}: Figure 23's result, `z^n = 1 \Rightarrow z = e^{2\pi i m/n},\ m = 0, 1, \dots, n-1`. {ring}: the four dots clear and N dots appear round the circle (Figure 23 style, with rays). {gap}: an arc between neighbours, labelled `2\pi/n`. {start}: the m = 0 dot at 1 flashes GREEN.
> {five}: settle on n = 5, the five fifth roots of unity, a regular pentagon with one vertex at 1 (GREEN at 1, the other four TEAL). Keep this exact picture: s5 scales and turns it onto the ring.

[c1.unity.1] {last} Lecture nine ended with the roots of unity. {example} Take the equation zed to the fourth equals one. {polar} In polar form, zed is R, times E to the eye theta. {power} Then zed to the fourth is R to the fourth, times E to the four eye theta, and that must equal one.

[c1.unity.2] {mod} Compare lengths. R to the fourth is one, and R is a positive length, so R equals one. {angle} Compare angles. Four theta must be a whole number of turns, two pi M, for some integer M. {theta} So theta is M times pi over two, which is M quarter turns.

[c1.unity.3] {m0} M equals zero gives one. {m1} M equals one is a quarter turn, which lands on eye. {m2} Then minus one, {m3} then minus eye. {m4} And M equals four is a full turn, back to one again. {quote} As Lecture nine put it, infinitely many in theta, but four distinct in zed. {pause}

[c1.unity.4] {general} For any power, N, the solutions of zed to the N equals one are E to the two pi eye M over N, for M from zero up to N minus one. {ring} They're N points, evenly spaced round the unit circle, {gap} two pi over N apart, {start} starting at one. {five} Here are the five fifth roots of unity. Keep this picture in mind.

## Scene 4 · Example 28: three steps (ch1_s4_method)

> Left: Example 28's working, built line by line (notes p. 19, scan p. 2), in e^{…} form. Right: the Argand plane helper.
> {back}: `z^5 = 2i` at the top, `2i` YELLOW; the YELLOW dot at 2i on the plane, as in s1. {step1}: a small "1", `z = re^{i\theta}`. {left}: `z^5 = r^5e^{5i\theta}` (r and r⁵ GOLD, θ YELLOW).
> {step2}: "2". {up}: an arrow from 0 straight up to 2i, a GOLD brace "2" along it, a YELLOW right-angle arc `\pi/2` (the lecturer's margin sketch). {modarg}: `|2i| = 2`, `\arg 2i = \pi/2`. {every}: the arrow sweeps one more full turn (TEAL arc), as in s2. {keep}: `2i = 2e^{i(\pi/2 + 2\pi n)}` with `+\,2\pi n` TEAL. {hand}: a small DIM aside, the printed `2i = 2\exp(i\pi/2)`, with the TEAL `+2\pi n` pushed in under a caret, as written by hand on scan p. 2.
> {turns}: a TEAL tag on the n: "n counts full turns". {notdeg}: beside it a DIM "degree" tag (s3's meaning) crossed out.
> {step3}: "3". {r}: `r^5 = 2`; {root}: `\Rightarrow r = 2^{1/5} \approx 1.149` (GOLD). A dashed GOLD circle of radius 2^{1/5} appears on the plane.
> {theta}: `5\theta = \pi/2 + 2\pi n`. {divide}: `\theta = \frac{\pi}{10} + \frac{2\pi n}{5}`, the second term TEAL. {fifths}: on the plane, the TEAL full-turn arc shrinks to a fifth of a turn, `2\pi/5`. {roots}: five ghost ticks on the dashed circle, one per fifth of a turn from π/10 (s5 places the dots).
> {trap}: a RED-framed side column. {drop}: `2i = 2e^{i\pi/2}` with no 2πn. {one}: `5\theta = \pi/2 \Rightarrow \theta = \pi/10`: one GREEN dot on the dashed circle. {lost}: four RED "?" where the other roots should be. {late}: `\theta = \pi/10 + 2\pi n`: an arrow goes a full turn round and lands on the same GREEN dot. {rule}: the RED column is crossed out and the TEAL `+2\pi n` in the correct line flashes, with "put the 2πn in first, then divide". (All checked in Python 3.11.9: |2i| = 2, arg 2i = 0.5π, 2^{1/5} = 1.148698…; π/10 + 2πn gives the same point for every n.)

[c1.method.1] {back} Now back to our question, zed to the fifth equals two eye. {same} The method is the one we just used, in three steps. {step1} Step one. Write zed in polar form, R times E to the eye theta. {left} Then zed to the fifth is R to the fifth, times E to the five eye theta.

[c1.method.2] {step2} Step two. Write the right-hand side in the same form. {up} Two eye points straight up, two units from zero, {modarg} so its modulus is two, and its angle is pi over two. {every} But that's only one of its angles, {keep} so write them all. Two eye is two, times E to the eye times an angle, and the angle is pi over two plus two pi N. {hand} The printed notes leave out the two pi N here. The lecturer added it by hand.

[c1.method.3] {turns} Here, N counts full turns. {notdeg} It's no longer the degree, as it was for the roots of unity. {step3} Step three. Match the two sides. {r} The lengths agree, so R to the fifth is two, {root} and R is the ordinary, positive fifth root of two, about one point one five.

[c1.method.4] {theta} The angles agree too, so five theta equals pi over two, plus two pi N. {divide} Divide by five, and theta is pi over ten, plus two pi N over five. {pause} {fifths} Look at what dividing did. The full turns became fifths of a turn, {roots} and each fifth of a turn lands on a new root.

[c1.method.5] {trap} Here's the trap. {drop} Drop the two pi N, and the angle of two eye is just pi over two. {one} Divide by five, and you find only pi over ten, a single root. {lost} The other four are lost. {pause} {late} Adding two pi N after dividing is no help either, because whole turns land on the same point. {rule} So put the two pi N in first, then divide.

## Scene 5 · The ring of five (ch1_s5_ring)

> Left: the table from notes p. 20, columns n | θ | z, rows n = 0 … 5. Right: the Argand plane helper with s4's dashed GOLD circle of radius 2^{1/5}, and the DIM unit circle inside it.
> {n0}: `\pi/10`, `2^{1/5}e^{i\pi/10}`; a GREEN dot at angle π/10, just above the Re axis. {n1}: `5\pi/10 = \pi/2`, `2^{1/5}e^{i\pi/2} = 2^{1/5}\,i` (the i PINK); {imag}: a TEAL dot straight up on the Im axis. {n234}: `9\pi/10`, `13\pi/10`, `17\pi/10`, three more TEAL dots. {n5}: `\pi/10 + 2\pi`; {same}: the arrow makes a full TEAL turn and lands on the GREEN dot, which flashes; the row reads "same as n = 0" (scan p. 3).
> {circle}: the five dots join in a faint pentagon. {radius}: radius label `r = 2^{1/5}` (GOLD), as on scan p. 3. {first}: a YELLOW arc from the Re axis to the first dot, `\pi/10`. {spacing}: an arc between two neighbours, `2\pi/5 = 4\pi/10`. {contrast}: s3's two features as RED-crossed ghosts: the unit circle and a dot at 1.
> {pentagon}: s3's pentagon of fifth roots of unity (same dots, GREEN at 1, four TEAL) appears on the unit circle. {scale}: it scales out by 2^{1/5} onto the dashed circle. {turn}: it turns by π/10 (YELLOW arc). {land}: it lands exactly on the five roots, which flash. (Checked in Python 3.11.9: 2^{1/5}e^{iπ/10}e^{2πim/5}, m = 0…4, equals Example 28's five roots.)
> {principal}: next to `13\pi/10` and `17\pi/10` in the table, GREEN `= -7\pi/10` and `= -3\pi/10`, labelled "principal argument"; {green}: the same two dots flash; nothing moves. (Python `cmath.phase` gives −0.7π and −0.3π.)
> {recipe}: the general method, boxed YELLOW: `z^k = w`: `|z| = |w|^{1/k}` (GOLD) and `\arg z = \dfrac{\arg w + 2\pi n}{k}`, `n = 0, 1, \dots, k-1` (2πn TEAL). Degree k on screen, so the turn counter n keeps its letter. (Checked on random w for k = 2, 3, 5: k distinct roots, each with k-th power w.)
> {quote}: the notes' remark from p. 19, verbatim: "Indeed, for any polynomial of degree n, there will always be n roots in the complex plane (counted with multiplicity)." {fta}: the lecturer's handwritten margin note under it, verbatim: "This the fundamental theorem of algebra (see §2.7)." {five}: `z^5 - 2i`, a tag "degree 5", and the five ring dots counted off one to five. {l11}: DIM "Lecture 11". Fade out.

[c1.ring.1] {table} Now fill in the table. {n0} N equals zero gives an angle of pi over ten. {n1} N equals one gives five pi over ten, which is pi over two. {imag} That root is straight up, so it's purely imaginary. {n234} Then nine pi over ten, thirteen pi over ten, and seventeen pi over ten. {n5} What about N equals five? {pause} {same} That's pi over ten plus a full turn, the same root as N equals zero.

[c1.ring.2] {circle} Here's the picture. Five roots, evenly spaced on a circle. {radius} Its radius is the fifth root of two, a little bigger than the unit circle. {first} The first root sits at pi over ten, just above the real axis. {spacing} Neighbours are two pi over five apart, which is four pi over ten. {contrast} As the lecturer pointed out, unlike the roots of unity, the circle is bigger and the start is turned.

[c1.ring.3] {pentagon} In fact, you can build this ring from the five fifth roots of unity. {scale} Stretch them by the fifth root of two, {turn} and turn them by pi over ten. {land} They land exactly on our five roots. {pause}

[c1.ring.4] {principal} Thirteen and seventeen pi over ten are fine as they are. {green} Their principal arguments, minus seven pi over ten and minus three pi over ten, give the same two points. {recipe} In general, every root of zed to the K equals W has length mod W, to the power one over K, {angles} and its angle is the argument of W, plus two pi N, all over K. That makes K roots.

[c1.ring.5] {why} So why five roots, and no more? {pause} {quote} Just before this example, the notes promise that a polynomial has as many roots in the complex plane as its degree, counting a repeated root more than once. {fta} The lecturer's margin note gives it a name, the fundamental theorem of algebra. {five} Zed to the fifth, minus two eye, has degree five, and we found five different roots, so that's all of them. {l11} Lecture eleven explains the theorem.

## Scene 6 · Try it, and recap (ch1_s6_recap)

> {f15}: the F15 card, verbatim from Examples Sheet I p. 8: "F15. Find all solutions of the following equations and indicate their location on the Argand diagram: (a) `z^3 = -1` (b) `z^4 = 1` (c) `z^2 = i` (d) `z^3 = -i`." Under it, four small Argand plane helpers, empty: no answers on screen.
> {args}: on (a)'s plane, the point −1 with a YELLOW arc `\pi`; on (d)'s, the point −i with a clockwise YELLOW arc `-\pi/2` (Python `cmath.phase`: π and −0.5π). {keep}: a TEAL "+ 2πn" tag on each. {b}: (b) gets a small tag "s3".
> {f16}: the F16 card, verbatim from p. 9: "F16. Show that the roots of the equation `z^{2n} - 2bz^n + c = 0` will, for general complex values of b and c and positive integer values of n, lie on two circles in the Argand diagram. Give a condition on b and c such that the circles coincide. Find the largest value of `|z_1 - z_2|` when z₁ and z₂ are roots of `z^6 - 2z^3 + 2 = 0`." {sub}: `w = z^n` under the middle term, then `w^2 - 2bw + c = 0` (checked with sympy). {rings}: a schematic of two concentric dashed GOLD circles, labelled `|w_1|^{1/n}` and `|w_2|^{1/n}`, with no dots on them. {part8}: DIM "Full solutions: Part 8".
> Recap, on {recap}: a 2 × 2 grid of small panels, each a shrunken copy of the visual that taught it (same objects, same colours), with its short line under it, appearing on its sentence:
> {r1}: s2's point, GOLD arrow `|z|`, YELLOW arc θ and the TEAL full-turn sweep; "modulus, argument, + 2πn". {r2}: s3's four roots of unity on the unit circle (GREEN 1; TEAL i, −1, −i); "z⁴ = 1: four roots".
> {r3}: s4's three steps condensed: `2i = 2e^{i(\pi/2 + 2\pi n)}`, `r = 2^{1/5}`, `\theta = \pi/10 + 2\pi n/5`, the 2πn TEAL; "polar form, keep the 2πn, match". {r4}: s5's ring of five, the dashed GOLD circle with one GREEN and four TEAL dots; "degree 5, five roots".
> {next}: the grid dims; a GOLD unit arrow `e^{i\theta}` steps round, θ, 2θ, 3θ, 4θ, with `(\cos\theta + i\sin\theta)^n` and DIM "Part 2 · De Moivre's theorem". Then the end card: hold about 8 s after the last word, with the music carrying it.

[c1.recap.1] {try} Now try some yourself. {f15} Question F fifteen, on the first examples sheet, has four equations like ours. Use the same three steps. {args} The argument of minus one is pi, and the argument of minus eye is minus pi over two. {keep} And keep the two pi N. {b} The second one is the roots of unity you've just seen.

[c1.recap.2] {f16} Question F sixteen is a quadratic in disguise. {sub} Call the power of zed in the middle term, W. Then the first term is W squared, and the equation is a quadratic in W. {rings} Each of its two solutions gives a ring of roots, so the roots lie on two circles. {part8} Full solutions are in Part eight.

[c1.recap.3] {recap} Let's recap. {r1} A complex number has a modulus and an argument, and the argument is only fixed up to whole turns, two pi N. {r2} The roots of unity sit evenly around the unit circle. {r3} To find every zed with zed to the fifth equal to two eye, write both sides in polar form, keep the two pi N, and match lengths and angles. {r4} Dividing the full turns by five gives five roots in a ring, and degree five means that's all of them.

[c1.recap.4] {next} Next time, we raise E to the eye theta to a whole-number power. {dm} That's De Moivre's theorem, and it gives the cosine of four theta in one line.
