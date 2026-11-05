# Chapter 4 · Solving cos z = 2

NST IA Mathematics, Lecture 11 (Hyperbolic Functions and Conics), part 4 of 7. Source: notes p. 30
(§2.7, the fundamental theorem of algebra) and p. 39 (Example 35, blank in the notes: the working is
the lecturer's handwriting, from the digest 24:19–32:38); lecture 03:12–04:43 and 24:19–32:42.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch4_s1_hook)

> Title card: "Hyperbolic Functions and Conics", "NST IA Mathematics · Lecture 11", "Part 4 · Solving cos z = 2".
> On {last}: "Last time", small, upper left: ch3's Figure 26 sideways curve (ch3's axes and styling), upper branch TEAL labelled `\ln\left(x + \sqrt{x^2 - 1}\right)`, lower branch PURPLE labelled `-\ln\left(x + \sqrt{x^2 - 1}\right)`. On {branches}: both branches pulse; then the picture shrinks into the corner and fades.
> On {wave}: centre, wide: axes with `y = \cos x` (BLUE) over about −3π to 3π. On {band}: dashed lines at y = 1 and y = −1, the band between them faintly shaded. On {line}: a YELLOW horizontal line `y = 2` slides down from the top and stops above the crests, a small gap arrow between a crest and the line. On {none}: RED `\cos x = 2`: "no real x".
> On {parab}: the wave morphs into the parabola `y = x^2 + 1` (WHITE) on the same axes, sitting above the x-axis. On {sq}: RED `x^2 + 1 = 0`: "no real x". On {rescue}: `x = \pm i` (i PINK) appears under it with a GREEN tick.
> On {ask}: the wave comes back under the YELLOW line; the `x` in `\cos x` turns into `z`, and the question settles in the centre in YELLOW: `\cos z = 2`, with "z complex?" under it. On {many}: "how many?" joins it.

[c4.hook.1] {title} This is part four of Hyperbolic Functions and Conics. {last} Last time, you ran cosh, shine and tanch backwards, and every inverse turned out to be a logarithm. {branches} Keep the inverse cosh in mind, with both of its branches. You will need it today.

[c4.hook.2] {wave} Here's the cosine wave. {band} It swings between minus one and one, and never leaves that band. {line} So the line at height two never meets it. {pause} {none} For real ex, the equation cosine of ex equals two has no solution at all.

[c4.hook.3] {parab} You've been here before. {sq} The equation ex squared plus one equals zero has no real solution either. {rescue} Then complex numbers arrived, and gave it two roots, eye and minus eye. {pause} {ask} So does cosine of zed equals two have complex solutions? {many} And if it does, how many? {pause=1.5}

## Scene 2 · Every polynomial has its roots (ch4_s2_fta)

> On {back}: the hook's `\cos z = 2` shrinks into the upper-right corner with a small YELLOW "?" (it returns at the end of the scene). Heading `2.7\ \text{Fundamental theorem of algebra}`, with a small DIM tag "end of Chapter 2 of the notes".
> On {poly}: the notes' polynomial (p. 30): `P(z) \equiv a_0 + a_1 z + a_2 z^2 + \cdots + a_{n-1} z^{n-1} + a_n z^n`, with "degree n ≥ 1". On {coeffs}: `a_0, \ldots, a_n \in \mathbb{C}`, and a box rides onto `a_n z^n` and a new `a_n \neq 0`. On {roots}: `P(z) = 0` "has n (complex) roots (possibly repeated)", "n roots" GREEN.
> On {weaker}: below it, "every polynomial equation has at least one complex root"; on {one} a YELLOW `\Leftrightarrow` joins the two statements.
> On {peel}: the peeling chain, each line born from a copy of the one above (TransformFromCopy), the new bracket dropping out GREEN: `P(z) = (z - z_1)\,Q(z)` with "degree n − 1" under Q. On {again}: `P(z) = (z - z_1)(z - z_2)\,R(z)`, "degree n − 2". On {down}: `\cdots`, then `P(z) = a_n (z - z_1)(z - z_2)\cdots(z - z_n)`, "degree 0" under `a_n`. On {count}: a brace under the brackets, "n factors, n roots".
> On {example}: the chain shrinks left; `z^3 - 1`. On {root1}: `z = 1`. On {factor}: `z^3 - 1 = (z - 1)(z^2 + z + 1)`, and the quadratic's roots `-\tfrac{1}{2} \pm \tfrac{\sqrt{3}}{2}\,i` (i PINK). On {circle}: the three roots as GREEN dots on a small Argand diagram with the unit circle (BLUE), a third of a turn apart. On {three}: "degree 3: 3 roots". (Checked with sympy 1.14: `factor(z**3 - 1)` gives `(z - 1)*(z**2 + z + 1)`; all three roots have modulus 1.)
> On {proof}: a grey italic note "not a formal proof". On {roth}, {gauss}, {argand}: a small history strip under the theorem fills in, "Roth 1608", "Gauss 1799 (`a_j \in \mathbb{R}`)", "Argand 1806 (`a_j \in \mathbb{C}`, first complete proof)", as in the notes' box.
> On {bridge}: `\cos z = 2` returns from the corner to the centre; a RED tag "not a polynomial" attaches to `\cos z`. On {promise}: the theorem card dims behind it.

[c4.fta.1] {back} Before we try, let's close Chapter two of the notes, with a theorem from the start of this lecture. {poly} Take a polynomial in zed, of degree N, where N is at least one. {coeffs} Its coefficients can be any complex numbers, as long as the leading coefficient is different from zero. {roots} Then the equation, P of zed equals zero, has exactly N complex roots, counting repeated roots as often as they appear. This is the fundamental theorem of algebra.

[c4.fta.2] {weaker} The notes point out that this is the same as a statement that sounds much weaker. {one} Every polynomial equation has at least one complex root. {pause} Why is that enough? {pause} {peel} Call that root zed one. Then P of zed is zed minus zed one, times a new polynomial, Q, of degree N minus one. {again} The polynomial Q has a root too, say zed two, so peel off a second factor. {down} Keep going until the degree reaches zero, and only the leading coefficient is left. {count} That's one root for every factor, so N roots in all.

[c4.fta.3] {example} Here's an example. Take zed cubed minus one. {root1} One root is easy to spot, zed equals one. {factor} Peel it off, and you're left with zed squared plus zed plus one, a quadratic with two complex roots. {circle} Together with one, they're the three cube roots of unity from earlier lectures, evenly spaced around the unit circle. {three} Three roots, for degree three.

[c4.fta.4] {proof} This is not a formal proof, and the lecturer said so. The hard part is showing that the first root exists at all. {roth} Peter Roth had the key elements in sixteen oh eight. {gauss} Gauss is often credited, in seventeen ninety-nine, for real coefficients. {argand} And Argand, in eighteen oh six, covered complex coefficients, and gave the first complete proof. {pause} {bridge} But cosine of zed is not a polynomial. {promise} So the theorem promises nothing about cosine of zed equals two. We'll have to look.

## Scene 3 · Split z into x + iy (ch4_s3_split)

> On {ex35}: the Example 35 card, styled like the notes' green-bordered box: "Example 35: Roots of complex cosine" / "Find all the roots of `\cos z = 2`." It settles at the top and stays there through scene 6.
> On {split}: `z = x + iy`, `x, y \in \mathbb{R}` (i PINK). On {reason}: a small tag beside it, "real functions".
> On {sum}: `\cos z = \cos(x + iy)`. On {formula}: `= \cos x \cos(iy) - \sin x \sin(iy)`, with ch2's addition formula card flashing beside it, `\cos(A + B) = \cos A \cos B - \sin A \sin B`; on {valid} it gains the tag "valid for complex A, B". Throughout the chapter: cos and sin BLUE, cosh and sinh TEAL, i PINK.
> On {dict}: ch1's dictionary card slides in from the top right, as built in ch1 s6 (YELLOW header "for every complex x"; rows `\cos(ix) = \cosh x`, `\sin(ix) = i\sinh x`, `\tan(ix) = i\tanh x`). On {cosiy}: its first row flies onto `\cos(iy)` and turns it into `\cosh y`. On {siniy}: its second row turns `\sin(iy)` into `i\sinh y`, and the PINK i slides out to the front of the term.
> On {result}: the lecturer's line, centred: `\cos z = \cos x \cosh y - i \sin x \sinh y`. On {real}: a brace under `\cos x \cosh y`, "real part". On {imag}: a PINK brace under `-\sin x \sinh y`, "imaginary part". On {worlds}: in each part the BLUE factor, then the TEAL factor, pulses. (Checked with sympy 1.14: `expand_complex(cos(x + I*y))` gives `-I*sin(x)*sinh(y) + cos(x)*cosh(y)`.)
> On {check}: two small panels under the line. On {yzero}, left panel "y = 0": `\cosh 0 = 1` and `\sinh 0 = 0` grey out the hyperbolic factors, leaving `\cos z = \cos x`, over a thumbnail of the hook's wave below the YELLOW line at 2. On {xzero}, right panel "x = 0": `\cos 0 = 1`, `\sin 0 = 0` grey out the circular factors, leaving `\cos(iy) = \cosh y`, over ch3's cosh curve (TEAL, horizontal axis labelled y). On {climb}: the curve rises through the YELLOW line at 2 and crosses it twice: the hook's shot with one curve swapped. Scene 5 brings this right-hand panel back.

[c4.split.1] {ex35} Now for Example thirty-five in the notes. Find all the roots of cosine of zed equals two. {split} Write zed as ex plus eye times why, where ex and why are real numbers. {reason} The lecturer's reason is that we know real functions well, so let's turn the problem into questions about them.

[c4.split.2] {sum} So cosine of zed is the cosine of a sum, ex plus eye times why. {formula} That calls for the addition formula from part two. Cosine of ex, times cosine of eye why, minus sine of ex, times sine of eye why. {valid} The formula holds for complex arguments too, so it's safe to use here.

[c4.split.3] {dict} Now bring in the dictionary from part one. {cosiy} Cosine of eye why is cosh of why, with no eye left over. {siniy} Sine of eye why is eye times shine of why. This time, an eye comes out in front. {result} So cosine of zed is cosine of ex, times cosh of why, minus eye, times sine of ex, times shine of why. {pause}

[c4.split.4] Look at the two terms. {real} The first is a real number. It's the real part of cosine of zed. {imag} The second is eye times a real number, so minus sine of ex, times shine of why, is the imaginary part. {worlds} Each part mixes the two worlds. It's a circular function of ex, times a hyperbolic function of why.

[c4.split.5] {check} Here's a quick check. {yzero} Put why equal to zero, so that zed is real. Cosh of zero is one, shine of zero is zero, and you're back to plain cosine of ex, stuck below two. {xzero} Now put ex equal to zero instead, so that zed is on the imaginary axis. Cosine of zed becomes cosh of why, {climb} and cosh climbs right past two. {pause} So off the real line, cosine can reach two after all.

## Scene 4 · Two real equations, one dead end (ch4_s4_cases)

> On {set}: the result line moves up under the Example 35 card and gains its right-hand side: `\cos x \cosh y - i \sin x \sinh y = 2`. On {zero}: a ghost `+\,0\,i` appears after the 2 (0 YELLOW, i PINK).
> On {realeq}: a WHITE arrow from `\cos x \cosh y` to the 2, and the line `\cos x \cosh y = 2`. On {imageq}: a PINK arrow from `-\sin x \sinh y` to the 0, and the line `-\sin x \sinh y = 0`. The two lines sit in the lecturer's left brace, one over the other. On {drop}: the minus fades, leaving `\sin x \sinh y = 0`.
> On {pair}: a small "2 equations, 2 unknowns: x, y". On {tip}: in YELLOW, "start with the one that equals 0". On {either}: `\sin x \sinh y = 0` splits into a case tree, "either `\sinh y = 0` or `\sin x = 0`".
> On {sinh}: the left branch lights up. On {graph}: ch3's sinh graph, small (TEAL), with a YELLOW dot at the origin, the only place it crosses zero. On {y0}: `y = 0`. On {sub}: `\cosh 0 = 1` → `\cos x = 2`. On {dead}: a RED `\emptyset`, with a thumbnail of the hook's wave under the line at 2; then the branch dims (it stays, dim, for the recap's tree).
> On {sin}: the right branch lights up. On {circle}: a unit circle (BLUE) with GREEN dots at the angles 0 and π, labels `0, \pi, 2\pi, \ldots` and `-\pi, -2\pi, \ldots`. On {npi}: `x = n\pi,\ n \in \mathbb{Z}` in GREEN. On {alive}: tag "still alive". On {feed}: `x = n\pi` slides towards `\cos x \cosh y = 2`, ready for scene 5.

[c4.cases.1] {set} Now set it equal to two. Two complex numbers are equal when their real parts are equal, and their imaginary parts are equal. {zero} Two is a real number, so its imaginary part is zero. {realeq} Matching real parts, cosine of ex, times the hyperbolic cosine of why, equals two. {imageq} Matching imaginary parts, minus sine of ex, times shine of why, equals zero. {drop} And since the right-hand side is zero, we can drop the minus sign.

[c4.cases.2] {pair} One complex equation has become two real ones, for two real unknowns. Which one should you start with? {pause} {tip} The lecturer's tip is to start with the one that equals zero. A product is zero only when one of its factors is zero. {either} So either shine of why is zero, or sine of ex is zero. That gives two cases, and we'll follow each one.

[c4.cases.3] {sinh} First case: shine of why is zero. {graph} Remember the graph of shine from part three. It always increases, and it crosses zero only once, at the origin. {y0} The only solution is why equals zero. {sub} Put that into the real equation. Cosh of zero is one, so cosine of ex equals two. {pause} {dead} That's the dead end from the start of this part. It has no solution, so this case is empty.

[c4.cases.4] {sin} Second case: sine of ex is zero. {circle} On the unit circle, sine is zero at zero, at pi, at two pi, and so on, and at the negative multiples too. {npi} So ex is N times pi, where N is any integer. {alive} Nothing has gone wrong yet, so this case survives. {feed} Next, we feed it into the real equation.

## Scene 5 · Only even multiples of π (ch4_s5_even)

> Upper left, kept from scene 4: the brace system and the GREEN `x = n\pi,\ n \in \mathbb{Z}` (the `\emptyset` branch is gone).
> On {sub}: `\cos x \cosh y = 2`, with `n\pi` flying in from `x = n\pi` to replace x: `\cos(n\pi) \cosh y = 2`. On {cosnpi}: a tiny strip under `\cos(n\pi)`: n = 0, 1, 2, 3 → 1, −1, 1, −1, with a dot hopping between 0 and π on a small unit circle. On {power}: `\cos(n\pi)` becomes `(-1)^n`. On {eq}: `(-1)^n \cosh y = 2`.
> The lecturer's sign marks. On {pos}: under `\cosh y` a GREEN `> 0` (with a thumbnail of ch3's cosh graph and `\cosh y \ge 1`). On {two}: under the 2 a GREEN `> 0`. On {ask}: under `(-1)^n` a YELLOW "?"; on {plus} it turns into `+1`.
> On {odd}: "n odd": `-\cosh y = 2` appears and gets a RED cross ("`\cosh y = -2`: impossible"). On {even}: "n even", GREEN `n = 2m,\ m \in \mathbb{Z}`.
> On {left}: the reduced system, braced. On {xeq}: `x = 2\pi m`. On {yeq}: `\cosh y = 2`. On {inv}: `y = \pm\cosh^{-1} 2 = \pm\ln\left(2 + \sqrt{2^2 - 1}\right)`, cosh⁻¹ and ln TEAL, the ± YELLOW. On {sqrt}: `2^2 - 1` boxed, collapsing to 3. On {result}: `y = \pm\ln\left(2 + \sqrt{3}\right)`. On {about}: `\approx \pm 1.32`. (Checked with sympy 1.14: `acosh(2).rewrite(log)` gives `log(sqrt(3) + 2)`, about 1.3170; over the reals, `solveset(cosh(y) - 2, y, S.Reals)` gives `{-acosh(2), acosh(2)}`.)
> On {both}: scene 3's right-hand panel returns, larger: the cosh curve (TEAL, horizontal axis labelled y) and the YELLOW line at 2. On {principal}: one crossing, at y ≈ 1.32, becomes a GREEN dot labelled "principal". On {mirror}: the second crossing, at y ≈ −1.32, becomes a GREEN dot too, dashed drops from both to the axis, a mirror arrow across the vertical axis tagged `\cosh(-y) = \cosh y`. On {graph}: beside it, ch3's Figure 26, small: a vertical line at 2 meets the upper branch (TEAL, `\ln\left(x + \sqrt{x^2 - 1}\right)`) and the lower branch (PURPLE, `-\ln\left(x + \sqrt{x^2 - 1}\right)`). On {lose}: the lower branch and its dot grey out with a RED "half the solutions lost"; then both come back GREEN.

[c4.even.1] {sub} Put ex equals N times pi into the real equation. {cosnpi} Cosine of N times pi is one when N is even, and minus one when N is odd. {power} In short, it's minus one to the power N. {eq} So minus one to the power N, times cosh of why, equals two.

[c4.even.2] Now look at the signs. {pos} Cosh is at least one for every real input, so cosh of why is positive. {two} Two is positive too. {ask} So what must minus one to the power N be? {pause} {plus} Plus one. {odd} If N were odd, you'd need cosh of why to equal minus two, and cosh is never negative. {even} So N must be even. Write it as two times M, for any integer M.

[c4.even.3] {left} That leaves two simple equations. {xeq} Ex equals two pi times M, {yeq} and cosh of why equals two. {inv} For the second, run cosh backwards, with the formula from part three. {sqrt} With two as the input, the number under the square root is two squared minus one, which is three. {result} That gives why equals plus or minus the log of two plus the square root of three. {about} That's about plus or minus one point three two.

[c4.even.4] {both} Keep both signs. {principal} The inverse cosh function gives only the non-negative value, the principal one. But here, the unknown why can be any real number. {mirror} And cosh is even, so plus one point three two and minus one point three two both give cosh equal to two. {graph} The line at height two crosses the cosh graph twice, once on each side. {lose} Keep only the principal value, and you lose half of the solutions.

## Scene 6 · Infinitely many solutions (ch4_s6_lattice)

> The Example 35 card at the top. On {together}: the answer in a YELLOW box, its pieces flying in from scene 5's `x = 2\pi m` and `y = \pm\ln\left(2 + \sqrt{3}\right)`: `z = 2\pi m \pm i\ln\left(2 + \sqrt{3}\right),\quad m \in \mathbb{Z}`. Colour by origin: `2\pi m` BLUE (from sine's zeros, the circular world); `\ln\left(2 + \sqrt{3}\right)` TEAL (from cosh⁻¹, the hyperbolic world); i PINK; ± YELLOW. On {re} and {im} the two pieces pulse in turn; on {m}, `m \in \mathbb{Z}`.
> On {plane}: the box shrinks up; the lecturer's Argand diagram, wide: axes `\mathrm{Re}\,z` and `\mathrm{Im}\,z` (the Im label PINK, as every i and imaginary part in L11; the height itself stays TEAL because it is cosh⁻¹ 2, a hyperbolic value), ticks `-4\pi, -2\pi, 0, 2\pi, 4\pi` on the real axis, a TEAL brace on the imaginary axis, `\ln\left(2 + \sqrt{3}\right) \approx 1.32`. On {first}: two GREEN crosses above and below 0. On {conj}: a YELLOW dashed reflection along the real axis maps one onto the other. On {repeat}: the pairs at ±2π, then ±4π, with a BLUE brace `2\pi` between neighbours, and `\cdots` with crosses fading past both edges. On {infinite}: "infinitely many".
> On {check}: the top cross at `z = i\ln\left(2 + \sqrt{3}\right)` pulses; the diagram slides left. On {cosh}: `\cos\left(i\ln(2 + \sqrt{3})\right) = \cosh\left(\ln(2 + \sqrt{3})\right)`. On {avg}: beside it, ch1 s2's averaging picture, small, same axes and styling: `e^{y}` GOLD and `e^{-y}` PURPLE. On {up}: a vertical line at y ≈ 1.32 meets them; the GOLD dot labelled `2 + \sqrt{3} \approx 3.73`. On {down}: the PURPLE dot labelled `2 - \sqrt{3} \approx 0.27`, with the side note `(2 + \sqrt{3})(2 - \sqrt{3}) = 4 - 3 = 1` (ch3's reciprocal trick). On {mid}: the YELLOW midpoint dot lands at exactly 2, and the algebra completes: `= \tfrac{1}{2}\left(2 + \sqrt{3} + \tfrac{1}{2 + \sqrt{3}}\right) = \tfrac{1}{2}\left(2 + \sqrt{3} + 2 - \sqrt{3}\right) = 2`, GREEN tick.
> (Checked: with Python's cmath, `cos(2πm ± i ln(2 + √3))` equals 2 to within 1e−12 for m = −3 … 3; sympy 1.14's `solveset(cos(z) - 2, z, S.Complexes)` gives `2nπ ± acos(2)`, and `acos(2)` evaluates to `1.31695789692482*I`: the same set.)
> On {below}: the check clears and the Argand diagram returns, full width; the bottom cross of the m = 0 pair pulses, with a small TEAL `\cosh(-y) = \cosh y`. On {period}: the row of crosses brightens. On {shift}: the whole row of crosses slides right by 2π and lands on itself. On {contrast}: two small cards side by side: scene 2's peeling chain, "degree n: exactly n roots" (GREEN), and the lattice, "`\cos z - 2`: infinitely many" (YELLOW). On {fine}: scene 2's RED "not a polynomial" tag returns on `\cos z`.

[c4.lattice.1] {together} Now put the two parts back together. {re} The real part of zed is two pi times M, {im} and the imaginary part is plus or minus the log of two plus the square root of three. {m} And M can be any integer, positive, negative or zero. {pause}

[c4.lattice.2] {plane} Let's plot them on the Argand diagram, as the lecturer did. {first} With M equal to zero, there are two roots, straight above and below the origin, about one point three two away. {conj} They're complex conjugates, mirror images in the real axis. {repeat} Then the same pair appears again at two pi, at four pi, at minus two pi, and so on, forever, in both directions. {pause} {infinite} So cosine of zed equals two has infinitely many solutions, spaced two pi apart.

[c4.lattice.3] {check} Let's check the root at the top. {cosh} It's on the imaginary axis, where cosine of eye why equals the hyperbolic cosine of why. {avg} And cosh is the average of E to the why, and E to the minus why. {up} At this root, why equals the log of two plus root three, so E to the why equals two plus root three. {down} E to the minus why equals one over that, which is two minus root three, because their product is four minus three, which is one. {mid} The average of two plus root three and two minus root three is exactly two. {pause} It works.

[c4.lattice.4] {below} The root below it works the same way, because cosh is even. {period} And the rest follow, because cosine repeats every two pi. {shift} Slide the whole picture along by two pi, and it lands on itself. {pause} {contrast} Now compare with the theorem from the start. A polynomial of degree N has exactly N roots. Cosine of zed minus two has infinitely many. {fine} There's no contradiction. Cosine is not a polynomial, and the theorem never promised anything about it.

## Scene 7 · Recap (ch4_s7_recap)

> A small "Recap" heading. Five small panels, filling two rows left to right, one per recap sentence, each built from the same objects, colours and styling as the scene it comes from, with its short line under it:
> On {r1}: scene 1's cosine wave (BLUE) under the YELLOW line at 2. Line: "no real solution".
> On {r2}: scene 2's peeling chain, three lines with GREEN brackets. Line: "degree n: exactly n roots".
> On {r3}: scene 3's split line `\cos z = \cos x \cosh y - i \sin x \sinh y` with its two braces (imaginary PINK). Line: "split into real and imaginary parts".
> On {r4}: scenes 4–5's case tree, the RED `\emptyset` branch and the GREEN `x = 2\pi m` branch. Line: "only x = 2πm survives".
> On {r5}: scene 6's lattice of GREEN crosses with its BLUE `2\pi` brace and TEAL height brace. Line: "infinitely many, 2π apart".
> On {try}: the panels clear except the lattice, which grows; `\cos z = -2` in YELLOW above it. On {odd}: tag "n odd". On {slide}: every pair slides right by π, to π, 3π, −π, …, at the same heights. (Checked with cmath: `cos((2m + 1)π ± i ln(2 + √3))` equals −2 for m = −3 … 3.)
> On {next}: a circle and an ellipse (BLUE) and a hyperbola (TEAL), sketched in thin lines, with the line "Part 5 · Circles and ellipses". Then the end card, held about eight seconds after the last word (music carries it).

[c4.recap.1] {recap} Time for a recap. {r1} On the real line, cosine never reaches two. {r2} A polynomial of degree N has exactly N complex roots, peeled off one factor at a time. {r3} To handle an equation in zed, write zed as ex plus eye times why, and split it into real and imaginary parts. {r4} The imaginary part gave two cases. One was empty, and the other left only even multiples of pi. {r5} So the roots of cosine of zed equals two come in pairs, two pi apart, and there are infinitely many of them. {pause}

[c4.recap.2] {try} Now try this yourself. Find every zed whose cosine is minus two. Follow the same steps. Which values of N survive this time? {pause=1.5} {odd} The odd ones. {slide} The pairs keep their heights, but slide along by pi.

[c4.recap.3] {next} Next time, we leave equations in zed behind, for curves in the plane. Circles and ellipses first, then hyperbolas, and how to tell them all apart from their equations. {pause}
