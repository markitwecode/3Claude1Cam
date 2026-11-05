# Chapter 8 · Solutions to the examples

NST IA Mathematics · Lecture 10 (Powers, Logarithms and Oscillations), part 8 of 8 (bonus, for after the exercises). Source: Examples Sheet I (`../source/M26examples1 (2).pdf`), PDF pp. 8–9, questions F12, F13, F15–F19; the methods are Parts 1–6 (notes PDF pp. 19–28).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Spoiler warning (ch8_s1_intro)

> Title card: "Powers, Logarithms and Oscillations", course line "NST IA Mathematics · Lecture 10", part line "Part 8 · Solutions (bonus)". On {warn}, a YELLOW "SPOILERS AHEAD" banner with a big pause icon (‖), held through the pause.
> On {cards}, seven question cards in one row, in the order this chapter takes them: "F15", "F16", "F17", "F12", "F13", "F18", "F19". Each has a small DIM tag naming the Part that teaches it, with a tiny icon of that Part's picture.
> The tags light up group by group: on {roots}, "Part 1" on F15 and F16 (a tiny ring of dots, ch1 s5's ring: one GREEN, the rest TEAL); on {sums}, "Parts 2–3" on F17, F12 and F13 (a tiny tip-to-tail chain of GOLD arrows, ch3 s3); on {logs}, "Part 4" on F18 (a tiny ladder, ch4 s4: TEAL rungs, one GREEN); on {osc}, "Part 6" on F19 (a tiny GOLD arrow with its BLUE shadow, ch6 s3).
> On {ritual}, four small steps appear under the row: "read", "pause ‖", "solve", "compare".
> Every later scene opens with its card enlarged out of this row (TransformFromCopy), showing the question as quoted in that scene's brief, plus the ‖ icon, held still through the pause.
> Every answer in this chapter was checked with Python 3.11.9 (cmath) and sympy 1.14.0; each scene's brief lists its checks.

[c8.intro.1] {title} The lecture is done, and this bonus part works through the seven questions on the first examples sheet that use it. {pause} {warn} From here on, it's all spoilers. If you still want to try them yourself, pause now, and have a go.

[c8.intro.2] {cards} Each question is tagged with the part that teaches it. {roots} F fifteen and F sixteen are roots, from Part one. {sums} F seventeen, F twelve and F thirteen are De Moivre and geometric series, from Parts two and three. {logs} F eighteen is logarithms, from Part four. {osc} And F nineteen is oscillations, from Part six. {ritual} Read each question, pause, work it out, then compare.

## Scene 2 · F15: four equations, one method (ch8_s2_f15)

> Card: "F15 · Find all solutions of the following equations and indicate their location on the Argand diagram: (a) z³ = −1 (b) z⁴ = 1 (c) z² = i (d) z³ = −i" + ‖, held through the pause.
> Then four small copies of the series' Argand plane helper (ch1 s2: Re and Im axes, faint grid, unit circle DIM) in a 2 × 2 grid, labelled (a) to (d). One lights up per part while the others dim. On {all_unit}, all four unit circles brighten together, with "|z| = 1" in GOLD.
> Each part runs ch1 s4's three steps: the right-hand side as a YELLOW dot with its polar form ("+ 2πn" in TEAL), the argument divided, then the roots as dots styled like ch1 s5's ring (the n = 0 root GREEN, the roots the 2πn adds TEAL), joined by a thin outline. Each root's Cartesian form appears beside its dot.
> (a), from {a}: "−1 = e^{i(π + 2πn)}"; on {a_div}, "z = e^{i(π/3 + 2πn/3)}", n = 0, 1, 2; on {a_vals}, dots at 60°, 180°, 300°; on {a_cart}, "½ + (√3/2)i", "−1", "½ − (√3/2)i"; on {a_tri}, the outline: a triangle with a corner at −1.
> (b), on {b}: "1 = e^{2πin}" ⇒ "z = e^{iπn/2}": "1", "i", "−1", "−i", a square with its corners on the axes (ch1 s3's four roots of unity, reused).
> (c), on {c}: "i = e^{i(π/2 + 2πn)}" ⇒ "z = e^{i(π/4 + πn)}", dots at 45° and 225°; on {c_cart}, "(1 + i)/√2" and "−(1 + i)/√2", two opposite points on the diagonal.
> (d), on {d}: "−i = e^{i(−π/2 + 2πn)}"; on {d_div}, "z = e^{i(−π/6 + 2πn/3)}", dots at −30°, 90°, 210°; on {d_cart}, "(√3 − i)/2", "i", "(−√3 − i)/2"; on {d_tri}, a triangle with a corner at i. End on all four diagrams lit together.
> Checked: sympy 1.14.0 `solve` gives `[-1, 1/2 - sqrt(3)*I/2, 1/2 + sqrt(3)*I/2]` for (a), `[-1, 1, -I, I]` for (b), `[-sqrt(I), sqrt(I)]` for (c) (that is, ±(1 + i)/√2), and `[I, -sqrt(3)/2 - I/2, sqrt(3)/2 - I/2]` for (d). With cmath, every root satisfies its equation to within 1e-15.

[c8.f15.1] {card} Question F fifteen. Find all the solutions of four equations, and show where they sit on the Argand diagram. {eqs} Zed cubed equals minus one, zed to the fourth equals one, zed squared equals eye, and zed cubed equals minus eye. {pause} {stop} Pause, and try them. {pause=1.5}

[c8.f15.2] {method} All four fall to Part one's three steps. {all_unit} Every right-hand side has modulus one, so every root lies on the unit circle, {args} and the two pi N goes in before you divide.

[c8.f15.3] {a} Minus one is E to the eye, pi plus two pi N. {a_div} Divide by three, to get pi over three, plus two pi N over three. {a_vals} Then N equals zero, one and two give sixty degrees, a hundred and eighty, and three hundred, {a_cart} so the roots are a half plus eye root three over two, minus one, and a half minus eye root three over two. {a_tri} They make a triangle.

[c8.f15.4] {b} Zed to the fourth equals one was Lecture nine's example, with roots one, eye, minus one and minus eye, a square. {c} For zed squared equals eye, the argument is pi over two, so the roots sit at pi over four and five pi over four. {c_cart} That's one plus eye over root two, and its negative.

[c8.f15.5] {d} For zed cubed equals minus eye, the argument is minus pi over two. {d_div} Divide by three, and you get minus thirty degrees, ninety, and two hundred and ten. {d_cart} The roots are root three minus eye, over two, then eye, then minus root three minus eye, over two. {d_tri} Another triangle, with a corner at eye.

## Scene 3 · F16: two circles (ch8_s3_f16)

> Card: "F16 · Show that the roots of z^{2n} − 2bz^n + c = 0 lie on two circles in the Argand diagram. Give a condition on b and c such that the circles coincide. Find the largest value of |z₁ − z₂| when z₁ and z₂ are roots of z⁶ − 2z³ + 2 = 0." + ‖.
> On {sub}, "w = zⁿ" (YELLOW), and the equation rewrites in place into "w² − 2bw + c = 0"; on {roots}, "w = b ± s, s = √(b² − c)", then "w₁ = b + s, w₂ = b − s".
> The two circles, with illustrative values (small on screen, never spoken): n = 4, b = 0.6 + 0.5i, c = −0.4 + 0.3i, so w₁ ≈ 1.342 + 0.702i and w₂ ≈ −0.142 + 0.298i. On {ring1}, w₁'s four roots appear as a ring (ch1 s5's ring style) on the circle of radius |w₁|^{1/n} ≈ 1.109 (GOLD label), then w₂'s ring on radius |w₂|^{1/n} ≈ 0.758. On {two_circles}, both circles pulse and the line "same circle ⇔ |w₁| = |w₂|" appears.
> The condition, on a fresh Argand plane, from {para}: arrows b and s from 0 in FG (white: here they're general complex numbers, and BLUE/PINK mean real and imaginary parts), with their parallelogram, the diagonals b + s and b − s in YELLOW with their lengths in GOLD. On {rect}, s swings round to a right angle with b: the parallelogram becomes a rectangle (right-angle mark) and the two lengths match. On {algebra}, "s = itb, t real", then "s² = −t²b² = b² − c ⇒ c = b²(1 + t²)". On {answer}, boxed (YELLOW): "c/b² real and ≥ 1 (or b = 0)".
> The example, from {example}: "z⁶ − 2z³ + 2 = 0: n = 3, b = 1, c = 2", "c/b² = 2 ✓". On {square}, the rectangle again with b = 1 and s = i, now a square, with w = 1 ± i at its far corners; now b = 1 is real and s = i imaginary, so they turn BLUE and PINK. On {mod}, "|1 ± i| = √2 ⇒ |z| = (√2)^{1/3} = 2^{1/6} ≈ 1.12" (GOLD), and one circle of that radius.
> The six roots: on {ring_a}, from 1 + i, "π/12 + 2πm/3" at 15°, 135°, 255° (GOLD dots), with a small note "m counts turns (n is the sheet's power here)", m and 2πm in TEAL (m counts turns whenever n is taken, as in ch1 s3 and ch3 s6). On {mirror}, the GOLD triple reflects in the real axis onto 1 − i's roots, "−π/12 + 2πm/3", at 345°, 225°, 105° (PURPLE: 1 − i is the conjugate of 1 + i).
> On {none}, a dashed RED diameter from the 15° root to 195° finds no root at its far end. On {chord_long}, the chord from 15° to 225° in YELLOW, with its 150° angle at the centre (YELLOW); the other two longest chords (105° to 255°, 135° to 345°) flash. On {len}, boxed: "|z₁ − z₂| = 2 · 2^{1/6} sin 75° = (1 + √3)/∛2 ≈ 2.17".
> Checked (sympy 1.14.0, cmath): the six roots of z⁶ − 2z³ + 2 all have modulus 1.12246 = 2^{1/6}, at 15°, 105°, 135°, 225°, 255°, 345°; the only pairwise angular separations are 30°, 90°, 120° and 150°; the largest |z₁ − z₂| over all pairs is 2.16843, and sympy confirms 2 · 2^{1/6} sin 75° = (1 + √3)/∛2 exactly. Also |b + s|² − |b − s|² = 4 Re(b s*); s = itb gives c = b²(1 + t²); and "c/b² real and ≥ 1" agreed with |w₁| = |w₂| in 3000 random cases.

[c8.f16.1] {card} Question F sixteen. Show that the roots of zed to the two N, minus two B zed to the N, plus C, equals zero, lie on two circles, and say when they coincide. {chord} Then find the largest distance between two roots of zed to the sixth, minus two zed cubed, plus two. {pause} {stop} Pause, and try it. {pause=1.5}

[c8.f16.2] {sub} Put W equal to zed to the N, and the equation becomes a quadratic, W squared, minus two B W, plus C, equals zero. {roots} So W is B plus or minus S, where S is the square root of B squared minus C. {ring1} Each W gives Part one's ring of N roots, of radius the N-th root of mod W. {two_circles} So there are two circles, and they coincide when the two values of W have the same modulus.

[c8.f16.3] {when} When is that? {pause} {para} Draw B and S as arrows. Then B plus S and B minus S are the diagonals of their parallelogram, {rect} which are equal exactly when it's a rectangle, with S at right angles to B. {algebra} Then S is B, times eye, times a real number T, and squaring gives C equals B squared, times one plus T squared. {answer} So C over B squared must be real, and at least one, or B must be zero.

[c8.f16.4] {example} In the example, N is three, B is one and C is two. {square} Here S is the square root of minus one, which is eye, at right angles to one. {mod} So W is one plus or minus eye, with modulus root two, and every root has modulus the sixth root of two.

[c8.f16.5] {ring_a} Here N is the power, so count the turns with M. One plus eye gives pi over twelve, plus two pi M over three, so fifteen, a hundred and thirty-five and two hundred and fifty-five degrees. {mirror} One minus eye gives the mirror images. {none} No two roots are opposite, {chord_long} so the longest chords span a hundred and fifty degrees. {len} Their length is twice the radius, times the sine of seventy-five degrees. That's one plus root three, over the cube root of two, about two point one seven.

## Scene 4 · F17 and F12 (ch8_s4_f17_f12)

> Card: "F17 · If ω³ = 1, find all values of 1 + ω + ω². Generalise your result to the case ωⁿ = 1 for n a positive integer." + ‖. Then the series' Argand plane, unit circle DIM, with the three cube roots of unity as dots and ω in YELLOW.
> On {one}, ω = 1: three unit arrows tip to tail along the real axis, a straight chain of length 3 (ch3 s6's straight chain), "= 3" in GOLD. On {other}, "(ω − 1)(1 + ω + ω²) = ω³ − 1 = 0", the middle terms ω and ω² striking out in pairs as the product expands; then "ω ≠ 1 ⇒ 1 + ω + ω² = 0".
> On {tri}, ω = e^{2πi/3}: arrows 1, ω, ω² tip to tail in GOLD (ch3 s3's chain), each turned a third of a turn; the chain closes into an equilateral triangle back at 0, "= 0". Boxed: "1 + ω + ω² = 3 or 0".
> On {gen}, "ωⁿ = 1: 1 + ω + … + ωⁿ⁻¹ = n if ω = 1"; on {poly}, "= (1 − ωⁿ)/(1 − ω) = 0 otherwise". On {closed}, the triangle turns into the chain for n = 5, ω = e^{2πi/5}: a closed regular pentagon.
> F12, on {f12}: its card, "F12 · Express: i. sin 3θ in terms of powers of sin θ; ii. sin⁵θ in terms of sin θ, sin 2θ, sin 3θ etc.", with no ‖ (it's quick). Real terms BLUE, terms with i PINK throughout.
> (i), on {i}: "sin 3θ = Im (cos θ + i sin θ)³ = 3cos²θ sin θ − sin³θ"; on {swap}, cos²θ is replaced in place by (1 − sin²θ); on {i_ans}, boxed "sin 3θ = 3 sin θ − 4 sin³θ".
> (ii), on {ii}: "sin⁵θ = (e^{iθ} − e^{−iθ})⁵ / (2i)⁵". On {pascal}, Pascal's row 1 5 10 10 5 1 with signs + − + − + − (ch2 s4's row), and the six terms "e^{5iθ} − 5e^{3iθ} + 10e^{iθ} − 10e^{−iθ} + 5e^{−3iθ} − e^{−5iθ}" (e^{+…} GOLD, e^{−…} PURPLE). On {pairs}, mirror terms bracket together (as in ch3 s2), and each pair becomes "2i sin kθ", with ch2 s6's two opposite arrows whose difference lands on the imaginary axis (PINK). On {ans}, "(2i)⁵ = 32i" and boxed "sin⁵θ = (sin 5θ − 5 sin 3θ + 10 sin θ)/16". On {check}, "θ = π/2: (1 + 5 + 10)/16 = 1".
> Checked (sympy 1.14.0, cmath): 1 + ω + … + ωⁿ⁻¹ is n for ω = 1 and 0 for every other n-th root of unity, n = 3 to 7. Both F12 identities simplify to 0 in sympy; (x − 1/x)⁵ expands to `x**5 - 5*x**3 + 10*x - 10/x + 5/x**3 - 1/x**5`, and (2i)⁵ is `32*I`.

[c8.duo.1] {card} Question F seventeen. If omega cubed is one, find all the values of one plus omega plus omega squared, then generalise to omega to the N equals one. {pause} {stop} Pause, and try it. {pause=1.5}

[c8.duo.2] {one} If omega is one, the sum is three. {other} Otherwise, multiply the sum by omega minus one. Everything cancels except omega cubed minus one, which is zero, so the sum is zero. {tri} Three unit arrows, tip to tail, each turned a third of a turn, close up into a triangle.

[c8.duo.3] {gen} For any N, the sum of N powers of omega, starting at one, is N when omega is one. {poly} Otherwise, the geometric series gives one minus omega to the N, over one minus omega, which is zero. {closed} The arrows always close up.

[c8.duo.4] {f12} Question F twelve is quick. {i} For sine of three theta, take the imaginary part of De Moivre's theorem with N equals three. That's three cosine squared of theta, times sine theta, minus sine cubed of theta. {swap} Swap the cosine squared for one minus sine squared, {i_ans} and you get three sine theta, minus four sine cubed of theta.

[c8.duo.5] {ii} For sine to the fifth of theta, raise Part two's formula for sine to the fifth power. {pascal} Pascal's row, with alternating signs, gives six terms, {pairs} and the mirror terms pair up, each pair two eye times a sine. {ans} Dividing by two eye to the fifth, thirty-two eye, gives sine five theta, minus five sine three theta, plus ten sine theta, all over sixteen. {check} At pi over two, that's one plus five plus ten, over sixteen, which is one.

## Scene 5 · F13: three sums (ch8_s5_f13)

> Card: "F13 · Evaluate the following sums: (a) Σ_{n=1}^{5} cos nθ (b) Σ_{n=1}^{5} sin nθ (c) Σ_{n=1}^{5} rⁿ cos nθ" + ‖.
> On {complex}, "Σ cos nθ + i Σ sin nθ = Σ_{n=1}^{5} e^{inθ}", the cosine sum BLUE and the sine sum PINK. On {gp}, "= e^{iθ}(1 − e^{5iθ}) / (1 − e^{iθ})", with small tags "first term", "ratio", "5 terms".
> The half-angle trick, from {factor}: "1 − e^{5iθ} = e^{5iθ/2}(e^{−5iθ/2} − e^{5iθ/2}) = −2i e^{5iθ/2} sin(5θ/2)", the bracket turning into "−2i sin(5θ/2)" by (78) (DIM equation number); then the same for the bottom, "1 − e^{iθ} = −2i e^{iθ/2} sin(θ/2)". On {cancel}, the two "−2i" strike out and the exponentials combine: "e^{iθ} · e^{5iθ/2} / e^{iθ/2} = e^{3iθ}". On {result}, boxed: "Σ e^{inθ} = e^{3iθ} sin(5θ/2) / sin(θ/2)".
> The picture, from {arrows} (ch3 s3's curling chain, at θ = 0.4 rad): five GOLD unit arrows e^{iθ}, …, e^{5iθ} tip to tail from 0; the total, from 0 to the chain's end, in YELLOW, lying exactly on a dashed line at angle 3θ drawn parallel to the middle (third) arrow. On {length}, its length "sin(5θ/2)/sin(θ/2) ≈ 4.24" in GOLD. On {a_ans}, its BLUE shadow on the real axis (≈ 1.53) and boxed "(a) cos 3θ sin(5θ/2)/sin(θ/2)"; on {b_ans}, its PINK shadow on the imaginary axis (≈ 3.95) and boxed "(b) sin 3θ sin(5θ/2)/sin(θ/2)".
> On {edge}, θ = 2πm: the chain straightens along the real axis (ch3 s6's straight chain), "(a) = 5, (b) = 0".
> (c), from {c}: "Σ rⁿ cos nθ = Re Σ (re^{iθ})ⁿ = Re[ re^{iθ}(1 − r⁵e^{5iθ}) / (1 − re^{iθ}) ]". The chain is redrawn with r = 0.8 (each arrow 0.8 times the last, a shrinking spiral), and a small RED ✗ crosses out "half-angle trick". On {conj}, top and bottom × (1 − re^{−iθ}) (PURPLE), as in ch3 s5. On {bottom}, "bottom = 1 − 2r cos θ + r²" (real, BLUE). On {top}, "top = re^{iθ} − r² − r⁶e^{6iθ} + r⁷e^{5iθ}", its four terms lighting one by one as their real parts are read. On {c_edge}, boxed: "(c) = (r cos θ − r² − r⁶ cos 6θ + r⁷ cos 5θ) / (1 − 2r cos θ + r²)", with "= 5 if re^{iθ} = 1" beneath.
> Checked (cmath, sympy 1.14.0): the half-angle form equals the direct sum at θ = 0.3, 1.1, 2.0, −0.7, 2.9 (error < 1e-15), and sympy confirms it exactly; its real part also equals Part 3's formula with N = 6, minus the first term 1. (c) equals the direct sum for r = 0.5, 2, −0.7, 1.3, 1 at five θ (error < 2e-14), and sympy confirms it exactly. At θ = 0.4 the sum is 1.535 + 3.948i, at angle 68.75°, which is 3θ.

[c8.f13.1] {card} Question F thirteen. Evaluate three sums, from N equals one to five, of cosine N theta, of sine N theta, and of R to the N, times cosine N theta. {pause} {stop} Pause, and try them. {pause=1.5}

[c8.f13.2] {complex} The first two are the real and imaginary parts of one sum, of E to the eye times N theta. {gp} It's a geometric series, so it's E to the eye theta, times one minus E to the five eye theta, over one minus E to the eye theta.

[c8.f13.3] {half} Here's a quicker route than Part three's conjugate. {factor} From one minus E to the eye times an angle, take out E to the eye times half the angle, leaving minus two eye times the sine of the half angle. {cancel} Do that top and bottom, and the minus two eyes cancel. {result} The sum is E to the three eye theta, times the sine of five theta over two, over the sine of theta over two.

[c8.f13.4] {arrows} By symmetry, the total of the five arrows lies along three theta, the middle arrow's direction. {length} Its length is the ratio of sines. {a_ans} So the cosine sum is cosine three theta, times that ratio, {b_ans} and the sine sum is sine three theta, times the ratio. {edge} When theta is a whole number of turns, they're five and zero.

[c8.f13.5] {c} In the third sum, the ratio is R times E to the eye theta, so the arrows shrink or grow, and the trick fails. {conj} Use Part three's conjugate, one, minus R times E to the minus eye theta. {bottom} The bottom becomes one, minus two R cosine theta, plus R squared. {top} The real part of the top is R cosine theta, minus R squared, minus R to the sixth times cosine six theta, plus R to the seventh times cosine five theta. {c_edge} Put that over the bottom, and you have the answer, unless R times E to the eye theta is one, when the sum is five.

## Scene 6 · F18: five logarithms (ch8_s6_f18)

> Card: "F18 · Find the (natural) logarithms of the following: (a) −1 (b) i (c) 1 + i (d) (x + iy)* (e) i r e^{iθ}" + ‖.
> On {rule}, ch4 s2's boxed rule, styled as there: "z = |z| e^{i(θ + 2πn)} ⇒ ln z = ln|z| + i(θ + 2πn)", modulus GOLD, angle YELLOW, "+ 2πn" TEAL.
> On {ladder}, five small w-planes in a row, each to hold ch4 s4's ladder: a vertical column of dots on the line Re w = ln|z|, rungs 2π apart (a TEAL brace "2πi"), the principal value GREEN with its tag "principal value", the other rungs TEAL. Above each, a tiny Argand plane with the point z and its argument (YELLOW). One ladder fills per beat.
> (a), on {a}: "ln(−1) = i(π + 2πn)", the ladder on the imaginary axis at …, −πi, πi, 3πi, … (principal πi); on {a_odd}, "= (2n + 1)πi". (b), on {b}: "ln i = i(π/2 + 2πn)", on the imaginary axis, principal iπ/2. (c), on {c}: "1 + i = √2 e^{i(π/4 + 2πn)}"; on {c_ans}, "ln(1 + i) = ½ ln 2 + i(π/4 + 2πn)", on the line Re w = ½ ln 2 ≈ 0.35, principal 0.35 + 0.79i.
> (d), on {d}: "(x + iy)* = x − iy", same modulus; on {d_arg}, "θ = arg(x + iy)" and the tiny point reflecting in the real axis, θ becoming −θ (as in ch4 s6's F18 hint); on {d_ans}, "ln[(x + iy)*] = ½ ln(x² + y²) + i(−θ + 2πn)". On {d_mirror}, the ladder of ln(x + iy) for a sample point (3 + 4i, so Re w = ln 5 ≈ 1.61) reflects in the real axis onto this one (PURPLE, the conjugate's colour).
> (e), on {e}: "i r e^{iθ} = r e^{i(θ + π/2)}", the tiny arrow turning a quarter turn; on {e_ans}, "ln(i r e^{iθ}) = ln r + i(θ + π/2 + 2πn), r > 0", and the ladder of ln(r e^{iθ}) slides up by π/2.
> Checked (cmath): every rung exponentiates back to its number (error < 5e-15): (a)–(c); (d) at 3 + 4i, −2 + i, 1 − 5i, −3 − 0.5i; (e) at (r, θ) = (2, 0.7), (0.5, −2), (3, 2.9). Principal values: ln(−1) = 3.1416i, ln i = 1.5708i, ln(1 + i) = 0.3466 + 0.7854i.

[c8.f18.1] {card} Question F eighteen. Find the logarithms of minus one, eye, one plus eye, the conjugate of ex plus eye why, and eye times R, times E to the eye theta. {pause} {stop} Pause, and try them. {pause=1.5}

[c8.f18.2] {rule} Part four's rule does them all. Write the number as its modulus, times E to the eye, argument plus two pi N. Its log is the real log of the modulus, plus eye times the argument plus two pi N, {ladder} a ladder of values, two pi eye apart.

[c8.f18.3] {a} Minus one has modulus one and argument pi, so its log is eye times pi plus two pi N, {a_odd} the odd multiples of pi eye. {b} Similarly, log of eye is eye times pi over two plus two pi N. {c} One plus eye has modulus root two and argument pi over four, {c_ans} so its log is half of log two, plus eye times pi over four plus two pi N.

[c8.f18.4] {d} The conjugate, ex minus eye why, has the same modulus as ex plus eye why, {d_arg} but if theta is the argument of ex plus eye why, the conjugate's is minus theta. {d_ans} So its log is half the log of ex squared plus why squared, plus eye times minus theta plus two pi N, {d_mirror} the mirror image of the other ladder.

[c8.f18.5] {e} Multiplying by eye is a quarter turn, so eye times R, times E to the eye theta, is R times E to the eye, theta plus pi over two. {e_ans} With R positive, its log is log R, plus eye times theta plus pi over two plus two pi N.

## Scene 7 · F19: a shifted oscillation (ch8_s7_f19)

> Card: "F19 · x = 7 + 24 cos 3t + 7 sin 3t. Show that the displacement from the centre (at x = 7) is the real part of X = (24 − 7i)e^{3it}, and obtain the amplitude. By writing X in the form Ae^{iϕ} (A, ϕ real), find the time of the first two passages through the centre after t = 0, and the distances of the stationary points from the origin." + ‖.
> On {centre}, "x − 7 = 24 cos 3t + 7 sin 3t" (with ch6 s6's number line, centre 7 in YELLOW). On {form}, it is matched to ch6's (81) "a cos ωt + b sin ωt", with tags a = 24 and b = 7 (both BLUE, the real coefficients as in ch6 s2), ω = 3. On {amp}, ch6 s3's boxed "A = a − ib" ⇒ "24 − 7i". On {expand}, "Re[(24 − 7i)(cos 3t + i sin 3t)] = 24 cos 3t + 7 sin 3t", the product "−7i · i sin 3t = +7 sin 3t" flashing.
> The arrow, on {triangle}, in ch6 s3's style (GOLD arrow, BLUE shadow dot on the real axis): 24 − 7i on the Argand plane, with its right triangle, 24 along the real axis (BLUE), 7 down (PINK), hypotenuse 25 (GOLD); "|24 − 7i| = √(576 + 49) = 25", boxed "amplitude 25". On {delta}, the angle below the axis in YELLOW, "δ = arctan(7/24) ≈ 0.284 rad ≈ 16.3°", and "24 − 7i = 25 e^{−iδ}" (ch6 s6's |A| e^{i arg A}, with arg A = −δ). On {polar}, "X = 25 e^{i(3t − δ)}", then "x − 7 = 25 cos(3t − δ)". Beside it, small and DIM, the sheet's letters mapped to ours: "sheet's A e^{iϕ}: its A = |24 − 7i| = 25, its ϕ = 3t − δ". Never write "A = 25" or a bare φ on its own: on screen A is the complex amplitude 24 − 7i, as in ch6.
> The motion, from {centre_pass}: the arrow turns anticlockwise from −δ while, beside it, the shadow's trace unrolls as a wave in t, drawn with x on the vertical axis (the centre line x = 7 DIM, the extremes 32 and −18 marked). On {t1}, the arrow points straight up and the shadow is at the centre: "3t − δ = π/2 ⇒ t₁ = (π/2 + δ)/3 ≈ 0.618", marked on the wave. On {t2}, straight down: "t₂ = (3π/2 + δ)/3 ≈ 1.665", with "half a turn later: + π/3" between the two marks.
> On {stat}, the arrow lies flat and the shadow sits at ±25 from the centre. On {ends}, the number line again with the origin 0, the centre 7, and the stationary points x = 32 and x = −18. On {dist}, GOLD distance braces from 0: "32" and "18" (ch6's RED "from the origin" tag returns, now answered).
> Checked (cmath): Re[(24 − 7i)e^{3it}] equals 24 cos 3t + 7 sin 3t at 60 sample times; 25 cos(3t − δ) matches it to 4e-14; |24 − 7i| = 25.0 and arg(24 − 7i) = −0.28379 = −arctan(7/24) (16.26°); the first zeros after t = 0 are 0.61820 and 1.66539 (also found by a brute-force scan), π/3 apart; x runs between −18 and 32.

[c8.f19.1] {card} Question F nineteen. The motion is ex equals seven, plus twenty-four times the cosine of three T, plus seven times the sine of three T. {show} Show that the displacement from the centre is the real part of twenty-four minus seven eye, times E to the three eye T, and find the amplitude. {times} Then find the first two passages through the centre, and the distances of the stationary points from the origin. {pause} {stop} Pause, and try it. {pause=1.5}

[c8.f19.2] {centre} So ex minus seven is twenty-four cosine of three T, plus seven sine of three T, {form} Part six's simple harmonic motion, with angular frequency three. {amp} Its complex amplitude is the cosine coefficient, minus eye times the sine coefficient, so twenty-four minus seven eye. {expand} Multiplying out confirms it, since minus seven eye, times eye, is plus seven.

[c8.f19.3] {triangle} Twenty-four minus seven eye makes a seven, twenty-four, twenty-five right triangle, so the amplitude is twenty-five. {delta} The arrow points below the real axis, at minus delta, where delta is the angle whose tangent is seven over twenty-four, about sixteen degrees. {polar} So the complex quantity is twenty-five, times E to the eye, three T minus delta, and ex minus seven is twenty-five cosine of three T minus delta.

[c8.f19.4] {centre_pass} The motion passes the centre when the arrow points straight up or down. {t1} The first time, three T minus delta is pi over two, so T is pi over two plus delta, all over three, about zero point six two. {t2} The next is half a turn later, three pi over two plus delta, all over three, about one point six seven.

[c8.f19.5] {stat} The motion turns back when the arrow lies flat, twenty-five either side of the centre. {ends} So ex reaches thirty-two and minus eighteen, {dist} and the stationary points are thirty-two and eighteen from the origin.

## Scene 8 · Recap and close (ch8_s8_end)

> Recap: five small panels in a row, one per sentence, each brought back from its scene (same objects, colours and styling) with its short line under it. On {r1}, s3's six roots on the circle of radius 2^{1/6} (GOLD and PURPLE triples, TEAL m), "keep the 2πn, then divide". On {r2}, s4's Pascal row with its mirror pairs bracketed, "De Moivre and exponentials". On {r3}, s5's curling chain with its YELLOW total along 3θ, beside s4's closed triangle, "sums are geometric series". On {r4}, s6's five mini-ladders (TEAL rungs, GREEN principal values), "the modulus, then every argument". On {r5}, s7's 24 − 7i arrow with its 7-24-25 triangle and BLUE shadow, "size and phase from one complex amplitude".
> On {threads}, the panels sort into two labelled rows, as in ch7 s6's two-thread picture: "the 2πn" in TEAL (F15, F16, F18) and "the turning arrow" in GOLD (F17, F12, F13, F19).
> On {next}, the panels clear to "Lecture 11 · Hyperbolic functions", then "cosh x = ½(e^x + e^{−x})" with e^x GOLD and e^{−x} PURPLE (L11's colours, as in ch7 s6's teaser).
> On {end}, the end card. Hold it ~8 s after the last word; the music carries it.

[c8.end.1] {recap} Seven questions, and a handful of moves. {r1} For roots, keep the two pi N, then divide. {r2} For multiple angles and powers, use De Moivre and the exponential forms. {r3} For sums, find the geometric series. {r4} For logs, take the modulus and every argument. {r5} And for oscillations, one complex amplitude gives the size and the phase.

[c8.end.2] {threads} Two threads ran through them all, the two pi N and the turning arrow. {next} Next time, in Lecture eleven, the exponent turns real, and we meet the hyperbolic functions, starting with the hyperbolic cosine. {end} Well done, and see you there.
