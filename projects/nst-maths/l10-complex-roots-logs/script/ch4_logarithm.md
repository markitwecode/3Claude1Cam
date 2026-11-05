# Chapter 4 · The complex logarithm

NST IA Mathematics, Lecture 10 (Powers, Logarithms and Oscillations), part 4 of 8. Source:
Mathematical Methods I notes (N. G. Berloff), PDF pp. 24–25 (printed 105–106: §2.5 and the
principal-value box); the lecturer's scan pp. 7–8; the recording 00:19:14–00:28:21 and
00:35:46–00:36:09; Examples Sheet I, F18 (PDF p. 9).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch4_s1_hook)

> Title card: "Powers, Logarithms and Oscillations", course line "NST IA Mathematics · Lecture 10", part line "Part 4 · The complex logarithm".
> "Last time", small, upper left: ch3 s3's curling chain of GOLD unit arrows with its BLUE shadow on the real axis, beside ch3 s2's "cos³θ = ¼cos 3θ + ¾cos θ". On "{back}" a GOLD arrow labelled "e^w", pointing from w to z, flips round to point from z back to w.
> The real case, left half: a number line with "e^x = 2  ⇒  x = ln 2 ≈ 0.693" above it and one BLUE dot at 0.693. One dot, one answer.
> The complex case, right half: the Argand plane from ch1 s2 (axes Re and Im, faint grid, DIM unit circle), with 2i as ch1's YELLOW dot at height 2 on the imaginary axis. Above it "e^w = 2i", then "w = ?" with the "?" YELLOW. On "{many}" the "?" pulses; no answer yet.
> On "{defn}" the lecturer's definition slides in at the bottom as a preview of scene 2, "w = ln z  if  e^w = z", and on "{quote}" her line appears under it in quotes, small: "each time you see the logarithm, you have to go through this definition".

[c4.hook.1] {title} This is part four. {last} Last time, exponentials turned powers and sums of cosines into simple algebra. {back} Now we run the exponential backwards.

[c4.hook.2] {real} For real numbers, that's easy. If E to the ex equals two, then ex is log two, about zero point six nine, and that's the only answer. {plane} Now take two eye, our running number from part one. {ask} Which complex numbers W make E to the W equal to two eye? {pause} {many} Is there one answer, or many? {pause}

[c4.hook.3] {defn} To find out, we'll do what the lecturer does. We define the logarithm by undoing the exponential, which we already know. {quote} In her words, each time you see the logarithm, you have to go through this definition.

## Scene 2 · From the definition (ch4_s2_define)

> Top: the notes' question as printed on p. 24 (with e^{iθ} for the notes' exp): "If z = x + iy = |z|e^{iθ} with x, y, θ ∈ ℝ, then what is ln z?". On "{define}" the lecturer's red definition from scan p. 7 appears under it: "For z ≠ 0, define  w = ln z  if  e^w = z." The question then dims; the definition stays.
> The derivation grows downward, each line coming out of the one above (TransformFromCopy), in scan p. 7's words: "write  w = u + iv  and  z = |z|e^{iθ}", then "e^w = e^u · e^{iv} = |z|e^{iθ}". Throughout: i PINK, θ YELLOW, |z| GOLD.
> Lengths ("{lengths}"): small DIM tags "length 1" under e^{iv} and under e^{iθ}. On "{mod}" the remaining parts pull out into "e^u = |z|  (modulus)", and on "{u}" that turns into "u = ln|z|", both GOLD. On "{once}" a small inset on the right: the graph of e^u, rising and always above the axis, crossed once by a GOLD horizontal line at height |z|; a dot drops from the crossing to u = ln|z| on the axis.
> Angles ("{angles}"): two unit arrows, one at angle v and one at angle θ, landing on the same point. On "{turns}" the θ arrow sweeps one full turn (TEAL arc) and lands where it started (ch1 s2's sweep). On "{v}" the line "v = θ + 2πn  (argument)   n ∈ ℤ" appears, θ YELLOW and 2πn TEAL; on "{thread}" the 2πn glows.
> The result ("{formula}"), boxed in YELLOW, out of the u and v lines: "∴ ln z = ln|z| + i(arg z + 2πn)", with ln|z| GOLD, i PINK, arg z YELLOW, 2πn TEAL. On "{values}" the notes' sentence appears under it: "Infinitely many values spaced 2πi apart on a vertical line in the complex plane."
> Why z ≠ 0 ("{zero}"): the e^u inset comes back; follow the curve to the left, where it hugs the axis but never touches it. "|e^w| = e^u > 0", then "ln 0" in RED, struck out.
> Checked (Python 3.11.9, cmath): e^{ln|z| + i(arg z + 2πn)} = z for random z and n = −1, 0, 2.

[c4.def.1] {question} The notes ask the question directly. If zed equals ex plus eye why, or mod zed times E to the eye theta, then what is log zed? {pause} {define} Here's the definition. For any zed other than zero, W is the log of zed if E to the W equals zed. {pause} {same} That's how you define the log of a real number too, by undoing the exponential.

[c4.def.2] {use} Now use what you know. {w} Split W into its real and imaginary parts, U plus eye V. {z} Write zed with its modulus and argument, mod zed times E to the eye theta. {expand} Then E to the W is E to the U, times E to the eye V. {equal} And that has to equal mod zed, times E to the eye theta.

[c4.def.3] {lengths} Compare the two sides, one part at a time. E to the eye V and E to the eye theta both have length one. {mod} So the lengths must agree, and E to the U equals mod zed. {u} That's an ordinary real equation, and its answer is U equals log of mod zed. {once} There's exactly one answer, because E to the U is positive and always increasing, so it reaches each positive height exactly once.

[c4.def.4] {angles} Now the angles. E to the eye V points at angle V, and E to the eye theta points at angle theta. {turns} They point at the same place, so the two angles can differ by any whole number of turns. {v} V equals theta, plus two pi N, for any integer N. {pause} {thread} There's that two pi N again, the thread of this whole lecture.

[c4.def.5] {box} Put the two parts together. {formula} Log zed equals log of mod zed, plus eye times the bracket, arg zed plus two pi N. {pause} {values} Every integer N gives a value. So, in the words of the notes, there are infinitely many values, spaced two pi eye apart, on a vertical line in the complex plane.

[c4.def.6] {zero} And why leave out zero? {pause} {never} E to the W has length E to the U, which is always positive. So E to the W can never be zero, and zero has no logarithm at all.

## Scene 3 · What the exponential does to the plane (ch4_s3_map)

> Two planes side by side. Left: the w-plane, axes "Re w" and "Im w", faint grid, no unit circle. Right: the z-plane, ch1's Argand helper (Re, Im, DIM unit circle). Between them a GOLD arrow labelled "e^w". On "{arrow}" a dot w on the left sends a copy of itself across to its image e^w on the right.
> On "{line}" a GOLD vertical line on the left at Re w = ln 2, with the tick "ln 2" on the Re axis. On "{circle}" it maps across (TransformFromCopy) onto the GOLD circle of radius 2 round 0 on the right. On "{slide}" the line slides right (the circle grows), then left (the circle shrinks towards 0 without reaching it), then back to ln 2.
> On "{climb}" a YELLOW dot climbs the line from height 0, and its image runs round the circle, the swept angle YELLOW. On "{wrap}" a TEAL brace "2π" marks the first climb, and the image is back at 2. On "{again}" a second climb and a second turn. On "{spool}" the whole line coils round the circle, turn on turn, slightly offset, then settles onto it.
> On "{back}" the arrow between the planes reverses. On "{point}" one point on the circle lights up: put it at 2i (YELLOW), which previews scene 4. On "{ladder}" thin arrows run back from it to a column of TEAL dots on the line, 2π apart, fading out at both ends: the ladder's first appearance.
> On "{real}", a small contrast strip under the planes: the w-plane's real axis (BLUE) lands once along the z-plane's positive real axis, with no wrapping; one arrow back, one dot, "one log". On "{complex}" beside it: "one z  ←  infinitely many w", the many in TEAL.

[c4.map.1] {planes} Here's a picture of what that formula means. {left} On the left is the plane of W, the inputs. {right} On the right is the plane of zed, the outputs. {arrow} The exponential sends each point W to the point E to the W.

[c4.map.2] {line} Take a vertical line on the left, where the real part, U, is fixed. Let's use log two. {circle} Every point on it lands at distance E to the U from zero, and that's two. So the line lands on a circle of radius two. {slide} Slide the line right, and the circle grows. Slide it left, and the circle shrinks towards zero, but never reaches it.

[c4.map.3] {climb} Now climb the line. The imaginary part, V, sets the angle, so the image goes round the circle. {wrap} Climb two pi, and it's back where it started. {again} Climb another two pi, and it goes round again. {pause} {spool} The exponential wraps the line round the circle, over and over, like thread round a spool.

[c4.map.4] {back} Now run it backwards. {point} Pick one point on the circle. {ladder} It came from a whole column of points on the line, two pi apart, one for each turn. {pause} {real} The real exponential never wraps. It lays the real line once along the positive real axis, so the real log has one value. {complex} The complex exponential wraps, so the complex log has infinitely many.

## Scene 4 · The ladder for 2i (ch4_s4_ln2i)

> Right third: the z-plane from scene 3 (ch1's helper), with 2i as the YELLOW dot at height 2, its modulus 2 in GOLD and its angle π/2 as a YELLOW arc. On "{form}" a TEAL sweep adds full turns to the angle (ch1 s4's styling).
> Left top, as on scan p. 7: "z = 2i = 2e^{i(π/2 + 2πn)}" (2πn TEAL). On "{result}", out of it: "ln z = ln 2 + i(π/2 + 2πn)". Braces underneath, as the lecturer drew them: "Re" under ln 2 (BLUE label) on "{re}", with "ln 2 ≈ 0.69" in GOLD; "Im" under (π/2 + 2πn) (PINK label) on "{im}".
> The hero, centre-left: the w-plane (axes Re and Im). On "{line}" a thin GOLD dashed vertical line at Re w = ln 2, with the tick "ln 2". On "{principal}" the n = 0 dot at height π/2, GREEN, with the tag "principal value" and the tick "π/2" on the Im axis. On "{rungs}" the TEAL dots for n = 1, −1, 2, −2 (at least n = −1 to 2 on screen), with fading dots beyond both ends. On "{brace}" a TEAL brace "2πi" between two neighbours. This is "the ladder", reused in ch5 s5: keep its styling.
> The warning ("{quote}"): the "π/2" tick flashes; a small angle arc drawn at the origin gets a RED strike, and on "{height}" the tick's label becomes "π/2 ≈ 1.57, a height". Caption in quotes: "it's not the angle anymore. This is the actual value."
> The check ("{check}"): from every rung a thin GOLD arrow ("e^w") runs across to the z-plane, and they all land on the same YELLOW dot, 2i.
> Checked (Python 3.11.9, cmath): the principal ln 2i is 0.6931 + 1.5708i; the rungs at heights −10.9956, −4.7124, 1.5708, 7.8540 and 14.1372 each exponentiate to 2i.

[c4.ladder.1] {two_i} Let's try it on two eye, the number from part one. {form} As before, write it with its modulus and every version of its angle. {read} Its modulus is two. Its argument is pi over two, plus two pi N.

[c4.ladder.2] {plug} Put those into the formula. {result} Log of two eye equals log two, plus eye times the bracket, pi over two plus two pi N. {re} The real part is log two, about zero point six nine. {im} The imaginary part is pi over two, plus two pi N.

[c4.ladder.3] {plot} Now plot these values in the plane of W. {line} They all have the same real part, so they sit on one vertical line, at log two. {principal} N equals zero uses the principal argument, pi over two, so that point is the principal value. {rungs} Then come N equals one and minus one, two and minus two, and so on, in both directions. {brace} Neighbours are two pi eye apart. {pause} This is the ladder of log two eye, and every rung is a correct answer.

[c4.ladder.4] {warn} The lecturer adds a warning here. {quote} Notice, it is not the angle anymore. This is the actual value. {height} On this ladder, pi over two is a height on the imaginary axis, the number one point five seven, not an angle. {check} And every rung really works. Raise E to any of them, and you land on two eye.

## Scene 5 · Two consequences (ch4_s5_consequences)

> The heading "Consequences:" from scan p. 7, with its two bullets dropping in as they're named: on "{first}" "• ln e^z = z + 2πin", and on "{rule}" "• ln(z₁z₂) = ln z₁ + ln z₂  modulo 2πi" (2πin and 2πi TEAL).
> First bullet ("{here}"): the w-plane with a YELLOW point z. A GOLD loop arrow "e^z" goes out of it, and the return arrow "ln" comes back split into the whole ladder through z (TEAL rungs, 2π apart). The naive "ln e^z = z" appears in RED and is struck out.
> The example (ours, "{example}"): z = 3 + 4i at (3, 4). On "{strip}" shade the strip −π < Im w ≤ π faint GREEN, labelled "principal values". On "{above}" the point 3 + 4i is seen just above the strip (4 > π). On "{down}" its ladder appears, and the rung at height 4 − 2π ≈ −2.28 is the one inside the strip: GREEN tag "principal value", beside "ln e^{3+4i} = 3 + (4 − 2π)i ≈ 3 − 2.28i". On "{differ}" a RED "≠ 3 + 4i".
> Second bullet ("{sets}"): four columns of dots on one shared vertical scale of imaginary parts, labelled "ln z₁", "ln z₂", "ln z₁ + ln z₂", "ln(z₁z₂)". Use the heights from z₁ = z₂ = −1 (odd multiples of π, π + 2πn, in the first two columns; 2πn for the product) but leave the numbers unlabelled; scene 6 names them. One rung from each of the first two columns lights up, their heights add, and a dot appears in the third column; then every pair fills it. The fourth column slides over: identical. On "{pick}" one dot in the third column and a different dot in the fourth light up, with a TEAL brace "2πi" between their heights.
> Last beat ("{ln2}"): a small ladder at Re w = ln 2, ln 2 + 2πin. The n = 0 rung sits on the real axis, GREEN, labelled "the real ln 2"; all the other rungs are TEAL, off the axis. On "{next}" a small tag: "→ Part 5: 2^i".
> Checked (Python 3.11.9, cmath): the principal ln e^{3+4i} is 3 − 2.2832i, and 4 − 2π = −2.2832; with z₁ = z₂ = −1, the sums of rungs give exactly the heights 2πn of ln 1.

[c4.cons.1] {heading} The definition has two consequences that catch people out. {first} The first is about the log of E to the zed. For real numbers, the log of E to the ex is just ex. {here} Here it's zed, plus two pi eye N. {why} The way back gives the whole ladder through zed, so you can land on any rung.

[c4.cons.2] {example} Here's an example: zed equals three plus four eye. {strip} The principal value is the rung whose height lies between minus pi and pi. {above} But four is bigger than pi, so three plus four eye sits above that strip. {down} The principal value of the round trip is one rung lower. Its real part is three, and its imaginary part is four minus two pi, about minus two point two eight. {pause} {differ} So even the principal value is a different number from the zed you started with.

[c4.cons.3] {second} The second consequence is about products. {rule} The log of zed one times zed two equals log zed one, plus log zed two, up to whole multiples of two pi eye. {sets} As whole ladders, the two sides match exactly. {pick} But pick one value on each side, and they can differ by a multiple of two pi eye. {advice} So, as the lecturer says, remember that you can always add or subtract two pi eye.

[c4.cons.4] {ln2} One more thing. Even log two has a whole ladder. It's log two, plus two pi eye N. {real} Only N equals zero gives a real number, the familiar log of two. {next} That small fact is the key to the next part.

## Scene 6 · Principal values (ch4_s6_principal)

> The box from notes p. 25, verbatim, "principal value" in italics as printed: "Often the principal value of ln z is defined by choosing just one of these possible values of θ, and the usual convention with ln z is to choose −π < θ ≤ π. For example, on sheet 1 question 10 note that the principal values in (a) and (b) differ by (almost) 2πi. This will be considered further in later maths courses." On "{choose}" "−π < θ ≤ π" turns GREEN. On "{warn}" "sheet 1 question 10" gets a small DIM note: "an older sheet's numbering".
> On "{rung}" the ladder of ln 2i from scene 4, small, with scene 5's faint GREEN strip −π < Im w ≤ π: the n = 0 rung inside it, with the GREEN tag "principal value".
> Notation: on "{capital}" "Ln z" appears and gets a RED strike. On "{same}" "ln z" stands over the whole ladder, and "ln z" with the GREEN tag "principal value" points at the one rung. On "{quote}" a caption in quotes: "please bear with this abuse of the notation".
> The example (ours): "z₁ = z₂ = −1". On "{each}" the principal "ln(−1) = iπ" (GREEN tag), twice, and their sum "2πi". On "{product}" "z₁z₂ = 1", with the principal "ln 1 = 0" (GREEN tag). On "{differ}" the two results side by side, "2πi ≠ 0" in RED, with a TEAL brace "2πi" between them on a small ladder (scene 5's fourth column).
> The angles ("{add}"), on ch1's Argand plane: an arrow at angle π, pointing at −1, with a YELLOW arc; add another π and the arc runs on to 2π, the arrow pointing at 1. On "{outside}" the principal range is drawn as a GREEN arc from just above −π round to π (open at −π), and the YELLOW arc overshoots it. On "{pull}" a RED arc pulls the angle back one full turn, to 0.
> F18 ("{try}"), from Examples Sheet I p. 9, as printed: "F18. Find the (natural) logarithms of the following: (a) −1  (b) i  (c) 1 + i  (d) (x + iy)*  (e) ire^{iθ}." On "{hint}" the template under it: "r e^{i(θ + 2πn)}  →  ln r + i(θ + 2πn)", with 2πn TEAL. On "{conj}" a small Argand picture for (d): a point and its mirror image in the real axis, θ becoming −θ. On "{times}" one for (e): the arrow r e^{iθ} turned a quarter turn by i (YELLOW arc "+π/2"). On "{sol}" the tag "Solutions: Part 8".
> Checked (Python 3.11.9, cmath): Ln(−1) = 3.1416i, Ln(−1) + Ln(−1) = 6.2832i, Ln 1 = 0; F18's principal values: ln i = 1.5708i, ln(1 + i) = 0.3466 + 0.7854i.

[c4.prin.1] {box} The notes give principal values a box of their own. {choose} You choose just one value of the angle, and the usual choice is the principal argument. It lies between minus pi and pi, with pi included and minus pi left out. {rung} On a ladder, that picks out one rung, the one inside this strip. We tag it in green, principal value.

[c4.prin.2] {notation} A word on notation. {capital} Some books write the principal value with a capital L. {same} This course uses the same log for both, the whole ladder and the principal value. {quote} In the lecturer's words, please bear with this abuse of the notation. {tag} In these videos, the green tag tells you which one is meant.

[c4.prin.3] {warn} The box also warns that principal values can break the product rule. {example} Here's an example: zed one and zed two both equal minus one. {each} The principal log of minus one is eye times pi. So the two principal logs add up to two pi eye. {product} But minus one times minus one is one, and the principal log of one is zero. {pause} {differ} The two answers differ by exactly two pi eye.

[c4.prin.4] {angles} Here's why, in terms of angles. {add} Multiplying adds the angles, so pi plus pi gives two pi. {outside} But two pi lies outside the principal range. {pull} To get the principal argument, pull it back one full turn, to zero. {pause} {lesson} So the product rule holds for the full sets of values, but principal values can be off by one rung.

[c4.prin.5] {try} Now try question F eighteen on Examples Sheet One, the logarithms of five numbers. {hint} Write each one with its modulus and every version of its argument, and then read off the log. {conj} Taking the conjugate of ex plus eye why flips the sign of the argument. {times} And in the last one, multiplying by eye adds pi over two to the argument. {sol} Full solutions are in part eight.

## Scene 7 · Recap (ch4_s7_recap)

> Five small panels in a row (or a 3 + 2 grid), each a shrunken copy of the visual that taught it, same objects and colours, with its short line beneath. Each appears on its mark; the earlier ones stay.
> "{r1}": scene 2's YELLOW box "ln z = ln|z| + i(arg z + 2πn)" (ln|z| GOLD, i PINK, arg z YELLOW, 2πn TEAL). Line: "undo the exponential".
> "{r2}": scene 3's two planes, the GOLD line coiling onto the GOLD circle. Line: "lines wrap into circles".
> "{r3}": scene 4's ladder for ln 2i, GREEN principal rung, TEAL rungs, brace "2πi". Line: "a ladder, rungs 2πi apart".
> "{r4}": scene 5's 3 + 4i ladder with the GREEN strip and the GREEN rung inside it. Line: "ln e^z: any rung".
> "{r5}": scene 6's π + π arc with its RED pull-back. Line: "principal values: off by a rung".
> "{next}": the panels dim; "2^i" appears with a TEAL column of dots behind it. On "{ii}" "i^i = ?" with the "?" YELLOW.
> End card: hold about 8 s after the last word; music carries it.

[c4.recap.1] {r1} To recap. The log of zed comes from undoing the exponential. Its real part is the ordinary log of the modulus, and its imaginary part is the argument, plus two pi N. {r2} The exponential wraps vertical lines into circles, so each zed comes from a whole column of points. {r3} For two eye, that column is a ladder at log two, with rungs two pi eye apart. {r4} The log of E to the zed can land on any rung of zed's ladder. {r5} And principal values can break the product rule, by a whole two pi eye.

[c4.recap.2] {next} Next time, if log two has infinitely many values, then so does two to the power eye. {ii} And eye to the power eye turns out to be a real number.
