# Chapter 2 · De Moivre's theorem

NST IA Mathematics · Lecture 10 (Powers, Logarithms and Oscillations), part 2 of 8. Source: typeset notes (Chapter234_to_annotate.pdf) PDF pp. 20–21, printed pp. 101–102 (§2.4, Example 29, (77), (78)); the lecturer's fills, Lecture10_scanned.pdf pp. 3–4; lecture recording 00:07:45–00:13:36.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Spoken forms: "eye" is i; "E to the eye theta" is e^{iθ}; "zed" is z; capital "N" is the power n (in this chapter n is the power, as in the notes, never the turn count); "a modulus R" is r; "cosine" and "sine" always in full; "cosine to the fourth" is cos⁴θ. In s4–s5 (Example 29), a bare "cosine" or "sine" means cos θ or sin θ (s4's {short} says so). On screen: e^{…} rather than the notes' exp(…), equation numbers (71), (77), (78) small and DIM. No code on screen. Every formula, expansion and number below was checked with Python 3.11.9 (cmath, math) and sympy 1.14.0: De Moivre for n = −3 … 6, the five-term expansion and its collected form, each line of the cos 4θ reduction, all four forms of sin 4θ, the θ = π/4 check, (77), (78), and the square-root demonstration (θ = 100°: halves at 50° and 230°, opposite, both squaring back to e^{iθ}).

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card on {title}: "Powers, Logarithms and Oscillations", "NST IA Mathematics · Lecture 10", "Part 2 · De Moivre's theorem"; it clears on {ring}.
> {ring}: ch1 s5's ring of five comes back small at left, on ch1's Argand plane (the helper ch1's director named in STATUS.md: axes Re and Im, faint grid, DIM unit circle): as ch1 s5 left it: the dashed GOLD circle of radius 2^{1/5}, the GREEN dot at angle π/10 and the four TEAL dots, and the label z⁵ = 2i with 2i YELLOW.
> {turns}: a GOLD arrow to the GREEN dot (angle π/10) and its YELLOW angle arc; the arc copies itself four times to make 5 × π/10 = π/2 while the arrow grows to length 2 and lands on 2i, with the line "multiplying adds angles" under the plane.
> {question}: the ring slides off. Centre: "cos 4θ = ?", the "?" YELLOW, and under it "in terms of cos θ" (cos θ BLUE).
> {long}: at right, smaller, the double-angle route writes itself: cos 4θ = 2cos²2θ − 1 = 2(2cos²θ − 1)² − 1. {seven}: "cos 7θ = ?" appears beneath it, and DIM compound-angle lines (cos(A + B) = cos A cos B − sin A sin B, then more of the same) stack up under it until the corner is crowded.
> {power}: the stack fades; in the centre, (cos θ + i sin θ)⁴ (cos θ BLUE, i sin θ PINK) with a YELLOW outline: one power.

[c2.hook.1] {title} This is part two of Powers, Logarithms and Oscillations, on De Moivre's theorem. {pause} {ring} Last time, you solved zed to the fifth equals two eye, and found five roots, spaced evenly round a ring. {turns} The key was that multiplying complex numbers adds their angles, so a fifth power multiplies an angle by five.

[c2.hook.2] {question} Today's question sounds like plain trigonometry. What is cosine of four theta, written using only cosine theta? {pause} {long} You could use the double-angle formula twice, since four is two times two. {seven} But for cosine of seven theta, you'd be stacking compound-angle formulas, line after line. {power} De Moivre's theorem gets any of them from a single power.

## Scene 2 · The theorem (ch2_s2_theorem)

> ch1's Argand plane fills the left two-thirds, DIM unit circle. {arrow}: a GOLD unit arrow at θ = 25°, its angle arc and "θ" YELLOW. {euler}: at right, z = cos θ + i sin θ = e^{iθ} (cos θ BLUE, i sin θ PINK, e^{iθ} GOLD), "(71)" small and DIM beside it.
> {power}: under it, zⁿ = (cos θ + i sin θ)ⁿ. {note}: a small YELLOW tag on the n: "n: the power (not the turn count)".
> {rule}: the chain continues, the notes' line with e^{…} for exp: = (e^{iθ})ⁿ. {chain}: = e^{inθ}, the outer n sliding down into the exponent (TransformFromCopy). {back}: = cos nθ + i sin nθ.
> {box}: (cos θ + i sin θ)ⁿ and cos nθ + i sin nθ lift out of the chain into a YELLOW box, titled "De Moivre's theorem": cos nθ + i sin nθ = (cos θ + i sin θ)ⁿ. {read}: each side highlights as it's read.
> {picture}: the box shrinks to the top right; the plane takes the stage. {lengths}: a small line "× : lengths multiply, angles add" (ch1 s2's words). {two} {three} {four}: copies of the arrow step round to 2θ, 3θ and 4θ = 100°, each step adding one more YELLOW θ-arc; earlier arrows stay, dimmed. {length}: all the tips sit on the unit circle; "1 × 1 × 1 × 1 = 1" in GOLD.
> {trivial}: a quote card, the lecturer at 00:08:01: "the proof is rather trivial". {general}: beside the unit arrow, a GOLD arrow of length r = 1.3 at θ, and its fourth power at 4θ with length r⁴ ≈ 2.86, labelled (r e^{iθ})ⁿ = rⁿ e^{inθ}, the rⁿ GOLD.
> {negative}: back to the unit arrow at θ. {minus}: "n = −1": cos θ − i sin θ appears. {mirror}: a PURPLE arrow at −θ, below the real axis, the mirror image of the GOLD one. {conj}: label e^{−iθ} (PURPLE); it stays for s6.

[c2.thm.1] {arrow} Start with a complex number of modulus one, at angle theta. {euler} It's cosine theta, plus eye sine theta, and by Euler's formula, that's E to the eye theta. {power} Now raise it to a whole-number power, N. {note} Here, as in the notes, N is the power. It's no longer the count of full turns from last time.

[c2.thm.2] {rule} When you raise an exponential to a power, you multiply the exponents. {chain} So E to the eye theta, to the power N, is E to the eye N theta. {back} And by Euler's formula again, that's cosine of N theta, plus eye sine of N theta. {box} Set the first expression equal to the last, and you have De Moivre's theorem. {read} Cosine of N theta, plus eye sine of N theta, equals cosine theta plus eye sine theta, all to the power N. {pause}

[c2.thm.3] {picture} Here's what that means in the plane. {lengths} Multiplying complex numbers multiplies their lengths and adds their angles. {two} So the arrow times itself points at angle two theta. {three} Times itself again, three theta. {four} And once more, four theta. {length} Each step turns it by another theta, and its length stays one, because one times one is still one.

[c2.thm.4] {trivial} The lecturer calls the proof rather trivial. Those were good times, she says, when putting your name on a theorem took very little labour. {general} She keeps the modulus equal to one, for simplicity. With a modulus R, the only change is the length, which becomes R to the power N.

[c2.thm.5] {negative} The power N can be negative, too. {minus} With N equal to minus one, you get cosine theta, minus eye sine theta. {mirror} That's the arrow turned back by theta, to its mirror image below the real axis. {conj} It's the conjugate, and you'll need it again at the end of this chapter.

## Scene 3 · Why N must be an integer (ch2_s3_integer)

> {note}: the notes' sentence, verbatim (p. 101): "Note that n must be an integer here: for other n the left-hand side is multivalued." {integer}: "n must be an integer" turns YELLOW.
> {hand}: under it, the lecturer's handwritten line (scan p. 3), in her red-pen style: (e^{iθ})ⁿ = e^{inθ}, n ∈ ℤ. {lhs}: the left side (e^{iθ})ⁿ is underlined, and joined to the notes' words "the left-hand side is multivalued". {why}: a YELLOW "n = ½ ?".
> The text shrinks to the top; ch1's Argand plane, DIM unit circle. {turn}: a GOLD unit arrow at θ = 100°, YELLOW arc. {same}: it sweeps one full turn along a TEAL arc and lands where it started; the label e^{iθ} = e^{i(θ + 2π)}, with "+ 2π" TEAL.
> {half}: a YELLOW "÷ 2" acts on both angles. {first}: a GOLD arrow at θ/2 = 50°, labelled e^{iθ/2}. {second}: a TEAL arrow at θ/2 + π = 230°, labelled e^{i(θ/2 + π)} = −e^{iθ/2}, with a TEAL half-turn arc from the first tip to the second.
> {two}: both tips glow, opposite each other; each arrow's angle doubles briefly back onto the 100° arrow (both square to e^{iθ}). {notone}: "(e^{iθ})^{1/2}" with a RED tag "two values".
> {whole}: the halves clear. With n = 3: a GOLD arrow at 3θ, and a TEAL one for 3(θ + 2π) = 3θ + 6π that winds three full TEAL turns and lands on it; a GREEN check, "one point".
> {ring}: s1's small ring of five returns with z⁵ = 2i. {fifths}: under it, ch1's angle line (π/2 + 2πn)/5 = π/10 + 2πn/5, the 2πn TEAL with a small TEAL tag "full turns" (ch1's n, not this chapter's power); the five dots light up in turn, a fifth of a turn apart.
> {later}: a small card "Part 5: how many values?" with i^i on it.

[c2.int.1] {note} The notes add a warning. {integer} The power N must be an integer here. {hand} The lecturer wrote it as E to the eye theta, to the N, equals E to the eye times N theta, for whole numbers N. {lhs} For any other N, the left-hand side has more than one value. {why} So what goes wrong with a fraction, like one half? {pause}

[c2.int.2] {turn} Remember the full turns from last time. {same} The point E to the eye theta is also E to the eye, theta plus two pi, one full turn later. {half} Now take N equal to one half, and take half of each angle. {first} Half of theta gives E to the eye, theta over two. {second} Half of the second angle, theta plus two pi, is theta over two, plus pi. That's an extra half turn, which lands on the opposite point, minus E to the eye, theta over two. {pause}

[c2.int.3] {two} Two different points, and both of them square back to the same number. {notone} So E to the eye theta, to the power one half, has two values, the two square roots. {whole} With a whole number N, the extra turn becomes N full turns, and every version lands on the same point. {pause}

[c2.int.4] {ring} That's exactly why, last time, zed to the fifth equals two eye had five roots. {fifths} Dividing the full turns by five gave fifths of a turn, and five different points. {later} In part five, you'll count the values of any power, even eye to the power eye.

## Scene 4 · Example 29: expand (ch2_s4_expand)

> {task}: the notes' green box header "Example 29: De Moivre's theorem" and the task, verbatim: "Use De Moivre's Theorem to determine expressions for cos 4θ and sin 4θ in terms of cos θ and sin θ." {goal}: "in terms of cos θ and sin θ" is the lecturer's handwritten fill (scan p. 4): show it in her handwriting style, YELLOW.
> {theorem}: s2's YELLOW box returns small, and a GOLD 4 drops onto each n. {lhs}: the task shrinks to the top; the notes' first line: cos 4θ + i sin 4θ = (cos θ + i sin θ)⁴ (cos BLUE, i sin PINK), with the lecturer's "← Th." in the margin.
> {binom}: the lecturer's "(a + b)⁴" small at right. {pascal}: Pascal's triangle builds rows 0 to 4 beside it, row 4 "1 4 6 4 1" in GOLD. {count}: under the first line, five slots fill: cos⁴θ, cos³θ (i sin θ), cos²θ (i sin θ)², cos θ (i sin θ)³, (i sin θ)⁴, the GOLD coefficients dropping in from row 4. {short}: a DIM note "cos, sin = cos θ, sin θ".
> {powers}: the triangle clears. {dial}: a small dial at right, the unit circle with a PINK dot: i, then a quarter turn to i² = −1; {cube}: another quarter turn, i³ = −i; {fourth}: and back to i⁴ = 1. {quarter}: the four positions stay marked, each with its value.
> {five}: the notes' expansion, verbatim: = cos⁴θ + 4i cos³θ sin θ + 6i² cos²θ sin²θ + 4i³ cos θ sin³θ + i⁴ sin⁴θ. {real}: i² and i⁴ flash, take −1 and 1 from the dial, and those three terms (with cos⁴θ) turn BLUE. {imag}: the i and i³ terms turn PINK. {signs}: "+6" becomes "−6" and "+4i" becomes "−4i", briefly RED, then settle.
> {collect}: the terms slide into the notes' next line: = cos⁴θ − 6cos²θ sin²θ + sin⁴θ + 4i(cos³θ sin θ − cos θ sin³θ). {blue}: the BLUE group gets a brace "real". {pink}: the PINK group gets a brace "imaginary". This line carries into s5.

[c2.exp.1] {task} Here's Example twenty-nine from the notes. {goal} Use De Moivre's theorem to write cosine of four theta and sine of four theta, in terms of cosine theta and sine theta. {theorem} Take the theorem with N equal to four. {lhs} Cosine of four theta, plus eye sine of four theta, equals cosine theta plus eye sine theta, all to the fourth.

[c2.exp.2] {binom} The right side is a sum of two terms, raised to the fourth power. {pascal} So the coefficients come from row four of Pascal's triangle, one, four, six, four, one. {count} In each term, the power of cosine counts down from four, and the power of eye sine counts up from zero. {short} Every cosine and sine here is of theta, so for this example, I'll just say cosine and sine.

[c2.exp.3] {powers} Each term also carries a power of eye. {dial} Eye squared is minus one. {cube} Eye cubed is minus eye. {fourth} And eye to the fourth is one. {quarter} On the Argand diagram, each factor of eye is a quarter turn, so the powers go round a dial, eye, minus one, minus eye, and back to one. {pause}

[c2.exp.4] {five} Now put those values into the five terms. {real} The terms with eye squared and eye to the fourth become real. {imag} The terms with eye and eye cubed stay imaginary. {signs} That's how plus six becomes minus six, and plus four eye becomes minus four eye. {collect} Now collect them. {blue} The real terms are cosine to the fourth, minus six cosine squared sine squared, plus sine to the fourth. {pink} The imaginary terms share a factor of four eye, times a bracket, cosine cubed sine, minus cosine sine cubed. {pause}

## Scene 5 · Real and imaginary parts (ch2_s5_simplify)

> s4's collected line stays at the top. {equal}: two small tags, "real = real" (BLUE) and "imaginary = imaginary" (PINK), joining the two sides of the line.
> {re}: cos 4θ (BLUE) lifts out of the left side and the BLUE group slides beside it: cos 4θ = cos⁴θ − 6cos²θ sin²θ + sin⁴θ, with the lecturer's "Re" in the margin. {im}: sin 4θ = 4(cos³θ sin θ − cos θ sin³θ), the i dropping away, "Im" in the margin. {met}: a GREEN check against the task's YELLOW "in terms of cos θ and sin θ".
> {further}: the sin 4θ line moves aside. The notes' lines, verbatim, one per beat. {swap}: a YELLOW tag "sin²θ = 1 − cos²θ"; {sixline}: = cos⁴θ − 6cos²θ(1 − cos²θ) …; {square}: … + (1 − cos²θ)², with sin⁴θ shown first as (sin²θ)²; {expand}: = cos⁴θ − 6cos²θ + 6cos⁴θ + 1 − 2cos²θ + cos⁴θ.
> {gather}: the three cos⁴θ coefficients (1, 6, 1) glow GOLD and merge into 8cos⁴θ; then the cos²θ ones (−6, −2) merge into −8cos²θ. {one}: the + 1 glows. {result}: = 8cos⁴θ − 8cos²θ + 1, boxed YELLOW.
> {sine}: the sin 4θ line returns and becomes the notes' sin 4θ = 4cos θ sin θ(cos²θ − sin²θ), the common factor 4cos θ sin θ pulled out front. {bracket}: the bracket highlights. {forms}: = 4cos θ sin θ(2cos²θ − 1); {or}: = 4cos θ sin θ(1 − 2sin²θ). {hand}: those two lines in the lecturer's handwriting style, with her margin note "cos²θ + sin²θ = 1".
> {check}: clear to the boxed cos 4θ = 8cos⁴θ − 8cos²θ + 1. {quarter}: "θ = π/4" (YELLOW). {left}: under the left side: 4θ = π, cos π = −1, with a tiny unit circle and its dot at −1. {right}: under the right side, cos²(π/4) = ½ and cos⁴(π/4) = ¼ (GOLD). {sum}: 8 · ¼ − 8 · ½ + 1 = 2 − 4 + 1 (GOLD). {total}: = −1, and a GREEN check joins it to the −1 on the left.

[c2.simp.1] {equal} Two complex numbers are equal exactly when their real parts match and their imaginary parts match. {re} So cosine of four theta is the real part, cosine to the fourth, minus six cosine squared sine squared, plus sine to the fourth. {im} And sine of four theta is the imaginary part, four times the bracket. {met} That's the task done, with both written in terms of cosine and sine of theta.

[c2.simp.2] {further} Now write cosine of four theta using cosine alone. {swap} Replace each sine squared with one minus cosine squared. {sixline} The middle term becomes minus six cosine squared, times one minus cosine squared. {square} Sine to the fourth becomes one minus cosine squared, all squared. {expand} Multiply everything out. {gather} The fourth powers come with one, six and one, eight in all. The squares come with minus six and minus two, minus eight in all. {one} And a plus one is left over. {result} So cosine of four theta is eight cosine to the fourth, minus eight cosine squared, plus one. {pause}

[c2.simp.3] {sine} For sine of four theta, take out the common factor, four cosine sine. {bracket} What's left in the bracket is cosine squared minus sine squared. {forms} Since cosine squared plus sine squared is one, that bracket is also two cosine squared minus one, {or} or, equally, one minus two sine squared. {hand} Those are the two endings the lecturer wrote in by hand.

[c2.simp.4] {check} A quick check never hurts. {quarter} Take theta equal to pi over four. {left} Then four theta is pi, and cosine of pi is minus one. {right} On the right, cosine squared of pi over four is one half, so cosine to the fourth is one quarter. {sum} Eight quarters make two. Eight halves make four. So you get two, minus four, plus one. {total} That's minus one. {pause} It matches.

## Scene 6 · Cosine and sine as exponentials (ch2_s6_expo)

> {other}: clear to ch1's Argand plane on the left (DIM unit circle), formulas on the right. {seventy}: e^{iθ} = cos θ + i sin θ (e^{iθ} GOLD, cos θ BLUE, i sin θ PINK), "(71)" small and DIM; the GOLD unit arrow at θ = 50°.
> {conj}: the arrow reflects in the real axis into a PURPLE arrow at −θ (s2's mirror, ch1's conjugate). {minus}: under (71), e^{−iθ} = cos θ − i sin θ (e^{−iθ} PURPLE), the "+" flipping to "−".
> {add}: a "+" joins the two lines. {cancel}: the two PINK i sin θ terms cross out; e^{iθ} + e^{−iθ} = 2cos θ. {cos}: cos θ = ½(e^{iθ} + e^{−iθ}); {num77}: "(77)" small and DIM at its right.
> {sub}: a "−" instead; the two BLUE cos θ terms cross out; e^{iθ} − e^{−iθ} = 2i sin θ. {sin}: sin θ = (1/2i)(e^{iθ} − e^{−iθ}); {num78}: "(78)". Both formulas stay at the right, boxed YELLOW.
> {picture}: the plane takes centre stage. {gold}: the GOLD arrow e^{iθ} turns slowly anticlockwise as θ grows; {purple}: the PURPLE arrow e^{−iθ} turns clockwise, always its mirror image.
> {tip}: the PURPLE arrow is carried to the GOLD arrow's tip. {real}: the chain's end sits on the real axis, a BLUE dot labelled 2cos θ, which slides between −2 and 2 along the axis as θ keeps turning; the two PINK vertical parts cancel.
> {diff}: the PURPLE arrow flips through the origin to −e^{−iθ} and moves to the GOLD tip; the end now rides the imaginary axis, a PINK dot labelled 2i sin θ. {divide}: a "÷ 2i" carries that dot to the real number sin θ (BLUE) on the real axis.
> {easier}: a quote card beside the two boxed formulas, the lecturer at 00:12:31: "working with exponentials is easier than working with cosines and sines".

[c2.expo.1] {other} You can use the same idea another way, and it's even more useful. {seventy} Here's Oiler's formula, equation seventy-one in the notes. E to the eye theta equals cosine theta, plus eye sine theta. {conj} Take the complex conjugate, which turns every plus eye into minus eye. {minus} You get E to the minus eye theta equals cosine theta, minus eye sine theta. {pause}

[c2.expo.2] {add} Add the two equations. {cancel} The eye sine terms cancel, and you're left with two cosine theta. {cos} So cosine theta is E to the eye theta, plus E to the minus eye theta, all over two. {num77} That's equation seventy-seven. {sub} Subtract instead, and the cosines cancel, leaving two eye sine theta. {sin} So sine theta is E to the eye theta, minus E to the minus eye theta, all over two eye. {num78} That's equation seventy-eight.

[c2.expo.3] {picture} Here's the picture. {gold} The gold arrow, E to the eye theta, turns one way as theta grows. {purple} Its mirror image, E to the minus eye theta, turns the other way. {tip} Put them tip to tail. {real} Their imaginary parts cancel, so the sum always lands on the real axis, at two cosine theta. {pause}

[c2.expo.4] {diff} Their difference does the opposite. The real parts cancel, and it lands on the imaginary axis, at two eye sine theta. {divide} Dividing by two eye brings it back to a real number, sine theta. {easier} As the lecturer puts it, working with exponentials is easier than working with cosines and sines. {pause}

## Scene 7 · Recap and next (ch2_s7_recap)

> {recap}: s6's picture clears. Five small panels fill the frame one per sentence, each the scene's own visual (same objects, colours and styling) with its short line under it.
> {r1}: s2's GOLD arrows at θ, 2θ, 3θ, 4θ on the DIM unit circle, with their YELLOW arcs; "(e^{iθ})ⁿ = e^{inθ}".
> {r2}: s3's two half-angle arrows (GOLD at 50°, TEAL at 230°) with the TEAL half-turn arc and the RED "two values" tag; "n must be an integer".
> {r3}: s4's Pascal row "1 4 6 4 1" (GOLD) beside the PINK i dial; "Pascal's row, powers of i".
> {r4}: s5's boxed cos 4θ = 8cos⁴θ − 8cos²θ + 1 over sin 4θ = 4cos θ sin θ(2cos²θ − 1), tagged "Re" and "Im"; "match real parts, match imaginary parts".
> {r5}: s6's GOLD and PURPLE arrows tip to tail, ending at the BLUE 2cos θ on the real axis, with (77) and (78) small beneath; "cos θ and sin θ as exponentials".
> {next}: the panels shrink away; "cos³θ = ▢ cos 3θ + ▢ cos θ" appears, the boxes YELLOW. {sums}: under it, 1 + cos θ + cos 2θ + … + cos(N − 1)θ = ?, with a YELLOW "?".
> End card after the last word, held ~8 s; the music carries it.

[c2.recap.1] {recap} Let's recap. {r1} De Moivre's theorem says that E to the eye theta, to the power N, is E to the eye N theta, the arrow turned to angle N theta. {r2} The power N must be a whole number, because a fraction splits the full turns into several values. {r3} To expand a power, use Pascal's row, and let the powers of eye sort the real terms from the imaginary ones. {r4} Matching real parts, then imaginary parts, gives cosine and sine of four theta. {r5} And adding or subtracting two mirror-image arrows writes cosine and sine as exponentials. {pause}

[c2.recap.2] {next} Next time, those two formulas turn a power like cosine cubed into single cosines, {sums} and a sum of cosines into a geometric series. {pause=1.5}
