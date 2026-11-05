# Chapter 5 · Complex powers

NST IA Mathematics, Lecture 10 (Powers, Logarithms and Oscillations), part 5 of 8. Source: typeset notes PDF pp. 25–26 (printed 106–107: Example 31, "General powers"); the lecturer's fills, scan pp. 8–9; recording 00:26:49–00:41:45.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch5_s1_hook)

> Title card: "Powers, Logarithms and Oscillations", course line "NST IA Mathematics · Lecture 10", part line "Part 5 · Complex powers".
> {ladder}: a small copy of ch4 s4's ladder for ln 2i (same object and styling: the vertical line Re w = ln 2, the n = 0 rung GREEN tagged "principal value", the other rungs TEAL, the brace "2πi" between two neighbours). It settles at the left and dims.
> {cube}: centre, 2³ = 2 · 2 · 2 = 8, the three 2s appearing one by one.
> {ii}: below it, a large i^i (both i's PINK) with a YELLOW "?" beside it. On {nomult}, try the same trick: "i · i · … (i times?)" appears and is struck through in RED.
> {claim}: a small tag under the "?", "real?" (YELLOW), echoing ch4's closing claim. {promise}: hold i^i, the "?" and the tag to the end of the scene. Do not show any value: s4 reveals them.

[c5.hook.1] {title} This is part five, on complex powers. {ladder} Last time, the logarithm of a complex number turned out to have a whole ladder of values, with rungs two pi eye apart. {pause} Today that ladder pays off.

[c5.hook.2] {cube} Two to the power three is easy. Multiply three twos together, and you get eight. {ii} So what is eye to the power eye? {pause=1.5} {nomult} There's no way to multiply eye by itself eye times. {claim} Yet last time ended with a strange claim, that the answer is a real number. {promise} By the end of this chapter, you'll work out every value it has, and see why.

## Scene 2 · The definition (ch5_s2_define)

> {cube}: top, 2³ = 8. {exp}: 2³ = e^{3 ln 2} grows out of it (TransformFromCopy). {why}: the chain e^{3 ln 2} = (e^{ln 2})³ = 2³ = 8, with e^{ln 2} = 2 underlined.
> {general}: the real rule a^b = e^{b ln a} (a > 0), with b and ln a bracketed as "exponent × log of the base". Real things BLUE.
> {box}: the real rule transforms into the definition z^w := e^{w ln z}, boxed YELLOW, with a small "Definition" label (the lecturer wrote a red "Def" on scan p. 8; RED is kept for pitfalls here). Small note under it: "z ≠ 0".
> {exp2} and {ln}: two small tags point at the two parts of e^{w ln z}: "exponential" and "logarithm (Part 4)".
> {ladder}: ln z glows, and a small copy of ch4's ladder drops out of it (TEAL rungs, GREEN n = 0 rung). {spread}: each rung sends a thin arrow to its own dot labelled z^w: one GREEN dot, several TEAL dots. {many}: "many values" beside them.
> {fm}: the Further Maths habit: everything but the GREEN rung and the GREEN dot dims; the dot gets the GREEN tag "principal value". {only}: the TEAL dots come back, with the label "only one of the values".
> Checked with Python 3.11.9: math.exp(3*math.log(2)) gives 7.999999999999998 (that is, 8).

[c5.def.1] {real} Start with real numbers, where you know the answer. {cube} Two to the power three is eight. {exp} You can also write it as E to the power, three log two. {why} That works because E to the log two is just two, and tripling the exponent cubes it. {general} Every real power works this way. Multiply the log of the base by the exponent, then raise E to that.

[c5.def.2] {define} For complex numbers, we take that as the definition. {box} Zed to the power W is E to the power, W log zed, for any zed except zero, which has no logarithm. {parts} Nothing new is needed. {exp2} It's built from the exponential, {ln} and the logarithm from Part four. {theme} That's this lecture's theme again. Start from the definitions, and see what they give you.

[c5.def.3] {catch} But you can already see the catch. {ladder} Log zed has a whole ladder of values. {spread} Each rung, multiplied by W and raised as a power of E, gives its own value of zed to the W. {many} So in general, zed to the power W has many values too. {pause} As the lecturer said, let's keep that in mind.

[c5.def.4] {fm} If you met complex powers in Further Maths, you probably used only one value of the log, the principal value. {green} That gives a correct answer. {only} But it's only one of the answers. {next} Let's find the rest, starting with two to the power eye.

## Scene 3 · Two to the power i (ch5_s3_two_i)

> {task}: heading "Example 31: Complex logarithms" and the notes' task, "Use complex logarithms to evaluate 2^i and i^i in the form x + iy." (every i PINK).
> {quick}: the notes' printed route, left column: z = 2^i ⟹ ln z = ln 2^i = i ln 2 (principal value) ⟹ z = e^{i ln 2} = cos(ln 2) + i sin(ln 2). The notes write exp(i ln 2); write e^{i ln 2}. "(principal value)" as a GREEN tag; cos(ln 2) BLUE, i sin(ln 2) PINK.
> {circle}: right, the Argand plane (ch1 s2's helper), unit circle DIM. A GOLD arrow of length 1; {angle}: it turns to angle ln 2, YELLOW arc labelled "ln 2 ≈ 0.69 rad ≈ 40°". {numbers}: its tip becomes a GREEN dot labelled "0.769 + 0.639i"; {tag}: GREEN tag "principal value".
> {proper}: the lecturer's handwritten line (scan p. 8), built under the printed route: 2^i = e^{i(ln 2 + 2πin)} = e^{−2πn} e^{i ln 2} = e^{−2πn}(cos ln 2 + i sin ln 2). The 2πin TEAL (the scan writes 2πni; write 2πin, the order the voice reads). {square}: in i · 2πin the two i's flash PINK and collapse into −1, leaving e^{−2πn} (GOLD: it's a modulus).
> {n0}: "n = 0" lights the GREEN dot again. {modulus}: the GOLD arrow stretches into a long ray at angle ln 2 (YELLOW angle kept). {n1} and {nm1}: at true scale, the n = 1 value sits almost on 0 and the n = −1 value runs off-screen; labels "n = 1: e^{−2π} ≈ 0.0019" and "n = −1: e^{2π} ≈ 535".
> {strip}: a log-scale strip laid along the ray, one equal step per factor e^{2π}, ticks e^{−4π}, e^{−2π}, 1, e^{2π}, e^{4π}; dots TEAL with their n (n = 2, 1, 0, −1, −2 outward from 0), the n = 0 dot GREEN. {many}: ellipses at both ends, "infinitely many values". This ray comes back in s7 and s8.
> Checked with Python 3.11.9 (cmath) and sympy 1.14.0: 2**1j = (0.7692389013639721+0.6389612763136348j); ln 2 = 0.6931 rad = 39.7°; i(ln 2 + 2πin) = −2πn + i ln 2; e^{−2π} = 0.0018674, e^{2π} = 535.49; every value has argument ln 2 and modulus e^{−2πn}.

[c5.two.1] {task} Example thirty-one in the notes asks for two to the power eye, in the form ex plus eye why. {def} By the definition, two to the power eye is E to the power, eye log two. {quick} The notes first take log two to be the ordinary real log, about zero point six nine. {euler} Then by Oiler's formula, E to the eye log two is the cosine of log two, plus eye times the sine of log two.

[c5.two.2] {where} So where is that? {circle} Its modulus is one, so it sits on the unit circle, {angle} at an angle of log two radians, about forty degrees. {numbers} Its real part is about zero point seven seven, and its imaginary part about zero point six four. {tag} This is the principal value. {pause}

[c5.two.3] {proper} Now let's do it properly, as the lecturer did. {ladder} In the complex world, even log two has a ladder of values, log two plus two pi eye times N, one for every integer N. {sub} Put the whole ladder into the exponent. {square} Eye times two pi eye times N is minus two pi N, because eye squared is minus one. {result} So two to the power eye is E to the minus two pi N, times E to the eye log two.

[c5.two.4] {n0} Set N to zero, and you're back at the principal value. {modulus} But every other N changes the modulus. {n1} N equals one shrinks it to E to the minus two pi, about two in a thousand. {nm1} N equals minus one stretches it to E to the two pi, about five hundred and thirty-five. {ray} The angle stays log two, so all the values lie on one ray. {strip} They're so spread out that we need a log scale to see them. {many} Infinitely many values, one for each rung of the ladder. {pause}

## Scene 4 · i to the power i (ch5_s4_i_i)

> {back}: the hook's i^i (both i's PINK) with its YELLOW "?", top left. {def}: at the top, the definition z^w := e^{w ln z}; the lecturer's curved arrow (scan p. 8) runs from it to the line i^i = e^{i ln i}.
> {polar}: right, a small Argand plane: i as a dot at distance 1 straight up, angle π/2 YELLOW. {turns}: ch1 s2's full-turn sweep, with the TEAL "+ 2πn": i = e^{i(π/2 + 2πn)}.
> {log}: ln i = i(π/2 + 2πn). {mult}: i^i = e^{i · i(π/2 + 2πn)}. {square}: the two i's flash PINK and collapse into −1. {answer}: i^i = e^{−π/2 − 2πn}, boxed YELLOW.
> {notes}: small, to the side, the notes' printed route: ln z = i ln i = i[i(π/2 + 2nπ)] = −(π/2 + 2nπ), z = e^{−(π/2 + 2nπ)} (printed as 2nπ, written 2πn here), with a tick: "same answer".
> {noeye}: the boxed result turns BLUE as the last PINK disappears: "real". {principal}: the positive real axis as a log-scale strip (s3's styling, now horizontal), dots at e^{−π/2 − 2πn}: the GREEN n = 0 dot "e^{−π/2} ≈ 0.208"; {others}: TEAL dots "n = 1: ≈ 0.00039" and "n = −1: ≈ 111"; ellipses both ways. {axis}: s3's ray, small, beside it: the same e^{2π} spacing.
> {recipe}: the method card, four numbered steps, kept for s8: 1. write the base as |z| e^{i(arg z + 2πn)} (2πn TEAL); {s2} 2. take ln; {s3} 3. multiply by the exponent; {s4} 4. exponentiate. {hard}: caption, the lecturer at 00:33:58: "probably the hardest problems you're going to get on the complex numbers".
> Checked with Python 3.11.9 (cmath) and sympy 1.14.0: i · i(π/2 + 2πn) = −π/2 − 2πn; 1j**1j = (0.20787957635076193+0j); n = 1 gives 0.000388, n = −1 gives 111.32; e^{i(π/2 + 2πn)} = i for n = −2…2.

[c5.ii.1] {back} Now back to the question from the start, eye to the power eye. {def} By the definition, it's E to the power, eye log eye. {need} So you need log eye, which means writing eye in polar form, with every version of its angle. {polar} Eye sits at distance one, straight up, at angle pi over two. {turns} So eye is E to the eye times its angle, and the angle is pi over two, plus two pi N.

[c5.ii.2] {log} Taking the log reads off the exponent, so log eye is eye times, pi over two plus two pi N. {mult} Now multiply by the outer eye. {square} Eye times eye is minus one, so the exponent becomes minus pi over two, minus two pi N. {answer} Eye to the power eye is E to the minus pi over two, minus two pi N. {pause} {notes} The notes take the log of both sides first, and reach the same line.

[c5.ii.3] {look} Look at that answer. {pause} {noeye} There's no eye left in it. Every value of eye to the power eye is a real number. {principal} The principal value, N equals zero, is E to the minus pi over two, about zero point two one, just over a fifth. {others} N equals one gives about four in ten thousand, and N equals minus one gives about a hundred and eleven. {axis} So the values sit on the positive real axis, spaced just like the ray for two to the power eye.

[c5.ii.4] {hard} The lecturer called these probably the hardest problems you'll get on complex numbers. {recipe} But the method is always the same four steps. Write the base in polar form, keeping the two pi N in its angle. {s2} Take the log. {s3} Multiply by the exponent. {s4} Then raise E to that power. {pause}

## Scene 5 · How many values? (ch5_s5_count)

> {general}: heading as on scan p. 9: "General powers z₁^{z₂}, z₁, z₂ ∈ ℂ. How many different values?" {def}: z₁^{z₂} = e^{z₂ ln z₁}.
> {ladder}: ch4 s4's ladder comes back (same styling: vertical line, GREEN principal rung, TEAL rungs, brace "2πi"), now generic, its rungs labelled "principal value", "+ 2πi", "+ 4πi", "− 2πi", … {rungs}: beside it the scan's line "with ln z₁ = ln z₁ + 2πin" (scan: 2πni), the right-hand ln z₁ with an upward arrow and the GREEN tag "principal value", as the lecturer drew it; 2πin TEAL.
> {abuse} and {theta}: a DIM bracket "same habit" joins that line to "θ = θ + 2πn" written beside it.
> {split}: multiply by z₂: z₁^{z₂} = e^{z₂ ln z₁} · e^{2πinz₂} (scan: e^{z₂ 2πni}). {fixed}: the first factor GREEN, labelled "one fixed number". {factor}: the second TEAL, labelled "depends on n". {rungs2}: each ladder rung sends a thin TEAL arrow to its own copy of e^{2πinz₂}.
> {ask}: the question card, kept for s6 and s7: "How many distinct numbers does e^{2πinz₂} give, as n runs through ℤ?" {depends}: z₂ highlighted YELLOW. {cases}: under the card, four empty gallery frames (small Argand planes, ch1's helper) in a row, captioned "integer", "fraction p/q", "irrational", "imaginary part".
> Checked with Python 3.11.9 (cmath): e^{z₂(Ln z₁ + 2πin)} = e^{z₂ Ln z₁} · e^{2πinz₂} for z₁ = 3 − 4i, z₂ = 0.7 + 0.2i, n = −2…2.

[c5.count.1] {general} Now for the general case, any complex number, zed one, raised to any complex power, zed two. {question} How many different values does it have? {pause} {def} By the definition, zed one to the power zed two is E to the power, zed two log zed one.

[c5.count.2] {ladder} Here's the ladder again. {rungs} Each value of log zed one is the principal value, plus two pi eye times N. {abuse} The lecturer writes log on both sides of that line, with the principal value on the right. {theta} It's a common shorthand for things with many values, like saying theta is also theta plus two pi N.

[c5.count.3] {split} Multiply by zed two, and the power of E splits in two. {fixed} One part, zed two times the principal log, gives one fixed number. {factor} The other part gives a factor, E to the power, two pi eye times N times zed two. {rungs2} Each rung of the ladder gives its own factor. {pause}

[c5.count.4] {ask} So the real question is how many different numbers this factor gives, as N runs through all the integers. {depends} That depends only on the exponent, zed two. {cases} Four cases cover everything: integers, fractions, irrational numbers, and numbers with an imaginary part.

## Scene 6 · Integer and rational exponents (ch5_s6_finite)

> Keep s5's question card, the TEAL factor e^{2πinz₂} and the four gallery frames.
> {int}: "i) z₂ = m ∈ ℤ" (the scan's wording). {factor}: on a DIM unit circle, the factor's dot starts at 1; for n = 1, 2, 3 its arrow sweeps whole turns (TEAL arcs, ch1 s2's sweep) and lands back on 1. {room}: "e^{2πinm} = ?" held through the pause; {one}: "= 1", "one value" (scan p. 9).
> {formula}: z₁^m = |z₁|^m e^{imθ₁} (|z₁|^m GOLD, mθ₁ YELLOW). {demoivre}: tag "De Moivre, Part 2". {example}: gallery frame 1 fills: one GREEN dot at −4, label "(2i)² = −4", caption "integer: 1 value".
> {rat}: "ii) z₂ = p/q in lowest terms, q > 0", factor e^{2πi(p/q)n}. {star}: on the unit circle, p/q = 2/5: the dot jumps 2/5 of a turn per step, landing at 0, 2/5, 4/5, 1/5, 3/5 of a turn (TEAL chords trace a five-point star). {room2}: "how many?" held through the pause. {q}: "q distinct values". {repeat}: the sixth jump lands on the first dot; label "5 steps = 2 full turns". {list}: "n = 0, 1, …, q − 1" (scan p. 9).
> {twofour}: "2/4 = 1/2". {half}: four slots under "2/4", two filled (the dots 1 and −1), two struck through in RED: "2 values, not 4".
> {ring}: the running example, line by line: (2i)^{1/5} = e^{(1/5) ln 2i} {log}= e^{(1/5)(ln 2 + i(π/2 + 2πn))} {result}= 2^{1/5} e^{i(π/10 + 2πn/5)}, 2i YELLOW, 2πn TEAL, 2^{1/5} GOLD. {back}: ch1 s5's ring of five comes back, same object and styling (circle of radius 2^{1/5} ≈ 1.149, first dot at π/10), with "z⁵ = 2i" beside it. {same}: "same five points"; the ring shrinks into gallery frame 2, caption "fraction p/q: q values".
> End on frames 1 and 2 filled, frames 3 and 4 empty: s7 starts from this shot.
> Checked with Python 3.11.9 (cmath) and sympy 1.14.0: e^{2πinm} = 1 and e^{2πi(p/q)(n+q)} = e^{2πi(p/q)n} (symbolic); distinct values of the factor over n = −200…200: exponent 3 → 1, 2/5 → 5, 1/5 → 5, 1/2 → 2, 2/4 → 2; the 2/5 star visits 0, 0.4, 0.8, 0.2, 0.6 of a turn; (2i)² = −4; (2i)^{1/5} for n = 0…4 equals ch1's five roots (modulus 1.148698, arguments 0.1π, 0.5π, 0.9π, −0.7π, −0.3π).

[c5.fin.1] {int} In the first case, the exponent is an integer, call it M. {factor} Then N times M is a whole number, so the factor is E to the power, two pi eye times a whole number. {room} The lecturer asked the room what that is. {pause=1.5} {one} It's one, every time. A whole number of full turns lands right back on one.

[c5.fin.2] {single} So there's exactly one value. {formula} It's the modulus of zed one to the M, times E to the eye times M theta one, where theta one is the angle of zed one. {demoivre} That's De Moivre's theorem from Part two, with a modulus in front. {example} For example, two eye, all squared, is minus four, and nothing else.

[c5.fin.3] {rat} In the second case, the exponent is a fraction, P over Q, in lowest terms, with Q positive. {step} Now each step turns the factor by P over Q of a full turn. {star} For two fifths, say, the dot jumps two fifths of the way round each time. {room2} How many different values? {pause=1.5} {q} Q of them, so here, five. {repeat} After Q steps the dot has made P full turns, and it's back where it started. {list} So N from zero up to Q minus one gives all Q values, evenly spread round a circle.

[c5.fin.4] {lowest} Why lowest terms? {twofour} Two quarters is the same number as one half. {half} One half gives two values, so two quarters gives two as well, not four. Cancel first, then count.

[c5.fin.5] {ring} Here's an example you've already seen. Take two eye to the power one fifth. {log} Its log is log two, plus eye times, pi over two plus two pi N. {result} Take a fifth of that and raise E to it, and you get the fifth root of two, times E to the eye times, pi over ten, plus one fifth of two pi N. {pause} {back} That's Part one's ring of five, exactly. {same} Raising two eye to the power one fifth is the same job as finding every fifth root of two eye.

## Scene 7 · Irrational and complex exponents (ch5_s7_infinite)

> Opens on s6's last shot: the question card, the TEAL factor e^{2πinz₂}, gallery frames 1 and 2 filled.
> {irr}: "iii) z₂ real and irrational" (scan p. 9), with the example z₂ = √2 (ours). {step}: on a DIM unit circle, the factor's dot jumps √2 turns per step (net about 0.414 of a turn) and leaves a TEAL dot at each landing. {never}: n = 0 … 10 slowly, with a counter "n = …"; {norepeat}: then faster, to a few hundred, the circle filling more and more densely and no dot landing on an earlier one. {infinite}: "∞ many values".
> {modulus}: "with modulus |z₁|^{z₂}" (scan p. 9; GOLD). {example}: gallery frame 3 fills: (2i)^{√2}, a circle of radius 2^{√2} ≈ 2.67 filling with dots (GREEN principal dot), caption "irrational: ∞ values, one circle".
> {cplx}: "iv) z₂ = x + iy, y ≠ 0" (iy PINK). {formula}: the scan's line |e^{2πinz₂}| = e^{−2πny} (GOLD), {differ}: "different for different n", {infinite2}: "So ∞ many values with different moduli." {x}: the x in z₂ = x + iy greys out (the lecturer: "I don't even worry what x is").
> {ray}: s3's ray for 2^i comes back small (x = 0, y = 1): dots a factor e^{2π} apart along one ray. {spiral}: gallery frame 4 fills with a spiral of dots, the values of (2i)^{0.1 + 0.03i} for n = −5 … 10 (each step turns 36° and shrinks by e^{−0.06π} ≈ 0.83), a faint spiral curve through them; principal dot GREEN, others TEAL; caption "imaginary part: ∞ values, all moduli different". (The exponent 0.1 + 0.03i is ours, chosen with a small imaginary part so the spiral fits a frame.)
> {gallery}: the full gallery in a row, each frame lighting as it's named: one dot | five dots on a ring | a dense circle | a spiral. Keep it for s8.
> Checked with Python 3.11.9 (cmath) and sympy 1.14.0: exponent √2 gives 401 distinct values over n = −200…200, all with modulus 2^{√2} = 2.665144; |e^{2πin(x + iy)}| = e^{−2πny} (symbolic); (2i)^{0.1 + 0.03i}: principal 1.0063 + 0.1809i (modulus 1.022, at 10.2°), n = −5 modulus 2.624, n = 10 modulus 0.155.

[c5.inf.1] {irr} In the third case, the exponent is real but irrational, like root two. {step} Each step turns the factor by root two full turns. {never} After N steps that's N root two turns, and N root two is a whole number only when N is zero. {norepeat} So no dot ever lands on an earlier one. {pause} {infinite} Infinitely many values.

[c5.inf.2] {modulus} But they all have the same modulus, the modulus of zed one, to the power zed two. {circle} So they lie on one circle, {dense} and as N runs on, they fill it more and more densely. {example} For two eye to the power root two, that circle has radius two to the power root two, about two point six seven.

[c5.inf.3] {cplx} In the last case, zed two is ex plus eye why, and its imaginary part, why, is different from zero. {formula} Now the modulus of the factor is E to the power, minus two pi N times why. {differ} Every N gives a different modulus, so every N gives a different value. {infinite2} Infinitely many values, with different moduli. {pause} {x} As the lecturer said, you don't even need to worry about the real part, ex.

[c5.inf.4] {ray} Two to the power eye was this case, with ex equal to zero. Its values sat on one ray, a factor of five hundred and thirty-five apart. {spiral} Give the exponent a real part as well, and each step can turn the dot as it shrinks, so the values trace out a spiral. {gallery} That completes the gallery. One value, Q values on a circle, a circle filled densely, and a spiral.

## Scene 8 · Recap (ch5_s8_recap)

> Five small cards, one per sentence, each a shrunk copy of the visual that taught it (same objects, colours and styling), its short line under it:
> {r1}: (s2) the YELLOW box z^w := e^{w ln z}, with the tiny ladder hanging from ln z; line "every rung of ln z gives a value".
> {r2}: (s3) the ray at angle ln 2 on its log strip, GREEN n = 0 dot; line "2^i = e^{−2πn}(cos ln 2 + i sin ln 2)".
> {r3}: (s4) the dots on the positive real axis, GREEN e^{−π/2}; line "i^i = e^{−π/2 − 2πn}: all real".
> {r4}: (s5) the ladder's rungs feeding the TEAL factor e^{2πinz₂}; line "count the factors".
> {r5}: (s6–s7) the gallery row: one dot | ring of five | dense circle | spiral; line "1 · q · ∞ · ∞".
> {next}: the cards clear; a small GOLD arrow turns on the unit circle (ch2's turning arrow) while a BLUE dot, its shadow, slides along the real axis: a hint of Part 6. Then the end card, held ~8 s after the last word (music carries it).

[c5.recap.1] {recap} Time for a recap. {r1} Zed to the power W is defined as E to the W log zed, so its values come from the rungs of the log's ladder. {r2} Two to the power eye has infinitely many values, all on one ray, with moduli E to the minus two pi N. {r3} Every value of eye to the power eye is real, and the principal one is E to the minus pi over two. {r4} In general, you count the values by counting the different factors, E to the power, two pi eye times N times zed two.

[c5.recap.2] {r5} An integer power has one value, a fraction P over Q has Q values, and an irrational or complex power has infinitely many. {pause} {next} Next time, we go back to the physical world, with a swinging pendulum, drawn as the shadow of a turning complex arrow.
