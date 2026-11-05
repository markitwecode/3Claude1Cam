# Chapter 7 · Solutions to Examples Sheet G

NST IA Mathematics · Lecture 11 (Hyperbolic Functions and Conics), part 7 of 7 (bonus, for after the questions). Source: Examples Sheet I p. 9 (section G, G1–G4; no answers are printed, so every answer here was derived and checked with sympy 1.14 / numpy 2.1), drawing on notes pp. 33–38 ((95), Example 33, Figure 25, (96), Example 34) and pp. 41–45 (ellipse, (102), Figures 27–28).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Spoilers ahead (ch7_s1_intro)

> {title} Title card: "Hyperbolic Functions and Conics", "NST IA Mathematics · Lecture 11", "Part 7 · Solutions to Examples Sheet G", with a small GOLD "Bonus" tag. On {last}: ch6 s3's pair, small (BLUE point (cos θ, sin θ) on the circle beside the TEAL point (cosh θ, sinh θ) on x² − y² = 1), then it fades.
> On {warn}: a GOLD "SPOILERS AHEAD" banner with a large pause icon (‖), held through the pause.
> On {cards}: ch6 s7's four question cards come back in their row, same verbatim sheet text and styling (G1 tanh(x + y); G2 the two loci; G3 the six graphs; G4 tanh⁻¹ x as a log), each lighting on its mark ({g1} … {g4}).
> On {ritual}, small chips under the row: "pause ‖", "solve"; on {mistake} a RED ✗ chip "the tempting mistake"; on {check} a GREEN ✓ chip "check".
> Each later scene opens with its card grown from this row to the hero position (TransformFromCopy) plus the ‖ icon, held still through the pause.

[c7.intro.1] {title} This is part seven of Hyperbolic Functions and Conics, a bonus, with worked solutions to section G of the first examples sheet. {last} Last time, shine and cosh drew the hyperbola, and you got a hint for each question. {warn} From here on, everything is a spoiler. If you haven't tried the questions yet, pause now, and have a go. {pause}

[c7.intro.2] {cards} There are four questions. {g1} The tanch of a sum. {g2} Two curves traced by a moving point. {g3} Six graphs to sketch. {g4} And inverse tanch, as a log, differentiated. {ritual} For each, you get the question, and a moment to pause. Then the solution, {mistake} the mistake that's easy to make, {check} and a quick check that the answer makes sense.

## Scene 2 · G1: tanh(x + y) (ch7_s2_g1)

> On {card}, card G1 grown from s1's row; on {stop} the ‖ icon, held through the pause.
> On {fast}, (95)'s two lines (ch2 s4's style, TEAL, with x, y for A, B): sinh(x + y) = sinh x cosh y + cosh x sinh y and cosh(x + y) = cosh x cosh y + sinh x sinh y. On {top} and {bottom} they become the numerator and denominator of tanh(x + y) = sinh(x + y)/cosh(x + y).
> On {divide} every term gets "÷ cosh x cosh y" (a note "cosh ≥ 1, never 0"); on {collapse} each term shrinks: sinh x cosh y / cosh x cosh y → tanh x, and so on, the first term underneath → 1.
> On {result} the answer, boxed YELLOW, its + in the denominator YELLOW: tanh(x + y) = (tanh x + tanh y)/(1 + tanh x tanh y). It moves to the top right, small, for the rest.
> Second route, the one ch6's hint asked for ({second}): tanh x = (e^x − e^{−x})/(e^x + e^{−x}); on {e2x} top and bottom × e^x → (e^{2x} − 1)/(e^{2x} + 1) (e^{2x} GOLD). On {ex34} ch3 s6's line e^{2x} = (1 + tanh x)/(1 − tanh x); on {names} the YELLOW tags p = tanh x, q = tanh y.
> On {sum}: e^{2x} · e^{2y} = e^{2(x+y)} = (1 + p)(1 + q)/((1 − p)(1 − q)); on {plug}: tanh(x + y) = [(1 + p)(1 + q) − (1 − p)(1 − q)] / [(1 + p)(1 + q) + (1 − p)(1 − q)], with the expansions 1 + p + q + pq and 1 − p − q + pq. On {cancel} the cancelling pairs strike out (1 and pq on top; p and q underneath) → (2p + 2q)/(2 + 2pq); on {same} → (p + q)/(1 + pq), which flashes against the boxed answer.
> Check ({rule}): ch2's sign-flip card, the BLUE tan(x + y) = (tan x + tan y)/(1 − tan x tan y) above the boxed answer; on {hidden} its − turns into the YELLOW +, labelled "hidden sinh x sinh y". On {slip} a RED copy with the − kept.
> On {test}: tanh x = tanh y = ½ (x = y = ½ ln 3); on {right} 1/(1 + ¼) = 4/5 (GREEN), on {wrong} 1/(1 − ¼) = 4/3 (RED), plotted against a small tanh graph (ch3 s3 style: dashed GOLD y = 1, dashed PURPLE y = −1): 4/3 sits above the line y = 1, where no tanh can reach.
> Checked with sympy 1.14: tanh(x + y) minus the boxed formula simplifies to 0; route 2's fraction simplifies to (p + q)/(p*q + 1); tanh(2 · ½ ln 3) = 4/5 exactly.

[c7.g1.1] {card} Question G one. Express the tanch of a sum, ex plus why, in terms of tanch of ex and tanch of why. {pause} {stop} Pause here, and try it. {pause=1.5}

[c7.g1.2] {fast} The fastest route uses the family list from part two, since tanch is shine over cosh. {top} On top, shine of ex, times cosh of why, plus cosh of ex, times shine of why. {bottom} Underneath, cosh of ex, times cosh of why, plus shine of ex, times shine of why. {divide} Divide every term by cosh of ex, times cosh of why. Cosh is never zero, so that's safe. {collapse} Each shine over its own cosh becomes a tanch, and the first term underneath becomes one. {result} So the answer has tanch of ex, plus tanch of why, on top, and one, plus their product, underneath. {pause}

[c7.g1.3] {second} Now the second route, from the hint, with exponentials only. {e2x} Multiply the top and bottom of tanch's definition by E to the ex. Tanch of ex becomes E to the two ex, minus one, over E to the two ex, plus one. {ex34} And Example thirty-four turned that around. E to the two ex is one plus tanch of ex, over one minus tanch of ex. {names} For short, call tanch of ex, P, and tanch of why, Q.

[c7.g1.4] {sum} Multiply E to the two ex by E to the two why, and you get E to the two, ex plus why, as a product of two such fractions. {plug} Put it into the tanch formula, and clear the fractions. {cancel} On top, the ones and the P Q terms cancel, leaving two P, plus two Q. Underneath, the lone P and Q terms cancel, leaving two, plus two P Q. {same} Cancel the twos, and it's the same answer. {pause}

[c7.g1.5] {rule} The sign-flip rule from part two predicts it too. {hidden} The tangent formula has a minus underneath, but tanch of ex, times tanch of why, hides a product of two shines, so the minus flips to a plus. {slip} Keeping the minus is the mistake to avoid. {test} Test both formulas with tanch of ex and tanch of why equal to a half. {right} The right one gives four fifths. {wrong} The wrong one gives four thirds, and no tanch is ever bigger than one. {pause}

## Scene 3 · G2: two loci (ch7_s3_g2)

> Card G2 enlarged + ‖ ({card}, {part2}, {task} light its three parts). Screen splits: the sheet's "i." left, "ii." right (narration says "the first curve", "the second curve": "part" names the videos). Example values for both sketches, labelled: a = 2, b = 1.
> Part i ({div}): x/a = cos θ, y/b = sin θ (BLUE); on {sq} squared and added with cos² θ + sin² θ = 1 → (x/a)² + (y/b)² = 1, boxed. On {ellipse} ch5's ellipse style: BLUE curve, centre YELLOW at the origin, semi-major GOLD along x (|a| = 2), semi-minor GREEN along y (|b| = 1), labels "|a|", "|b|".
> On {circle} a ghost with |a| = |b| rounds into a circle and back. On {all} ch5 s5's running point goes once round, anticlockwise. On {signs} a becomes −2: the curve stays put, the point now runs clockwise (sympy: x·dy/dθ − y·dx/dθ = ab, so anticlockwise when ab > 0, clockwise when ab < 0).
> Part ii ({hyp}): x/a = cosh θ, y/b = sinh θ (TEAL); on {identity} cosh² θ − sinh² θ = 1 (ch2) → (x/a)² − (y/b)² = 1, boxed. On {hyperbola} both branches of x²/4 − y² = 1, faint dashed TEAL (ch6's four-quarter style), vertices (±2, 0). Hold on {ask}.
> On {catch}: x/a = cosh θ ≥ 1 in YELLOW; on {sign} "x has the sign of a, |x| ≥ |a|"; on {right} a TEAL point runs θ from −3 to 3 along the RIGHT branch only, bottom to top, which turns solid; the left branch stays dashed with a RED ✗ "never reached".
> On {flip} a = −2: a PURPLE point (ch6 s3's colour for the minus branch) traces only the left branch, and the RED ✗ moves to the right one. On {whole} y = b sinh θ with a vertical arrow covering the whole y axis.
> On {asym} dashed dim-white asymptotes (ch6 s2's style) y = ±(b/a)x, here y = ±x/2. On {slip} the two-branch Cartesian sketch beside the one-branch locus, the extra branch RED; on {pm} ch6 s3's x = ±s cosh θ, y = s sinh θ (Figure 28's handwriting), the ± in YELLOW, and the notes' line "Each sign gives one branch".
> Checked with sympy 1.14: both eliminations simplify to 1; for a = 2, x = 2 cosh θ has minimum 2; y/x → b/a as θ → ∞ and −b/a as θ → −∞, and the gaps to the asymptotes are −b e^{−θ}, b e^{θ} → 0.

[c7.g2.1] {card} Question G two. A point has ex equal to the constant A, times the cosine of theta, and why equal to the constant B, times the sine of theta. {part2} For the second curve, cosine changes to cosh, and sine to shine. {task} For each, find the Cartesian equation of the curve, and sketch it. {pause} {stop} Pause, and try it. {pause=1.5}

[c7.g2.2] {div} The first curve. Divide ex by A, and why by B, to leave the cosine and sine of theta. {sq} Their squares add to one, so ex over A, all squared, plus why over B, all squared, equals one. {ellipse} That's the ellipse from part five, centred at the origin, reaching out to mod A, along the ex axis, and to mod B, along the why axis. {circle} When those two are equal, it's a circle. {all} As theta goes once round, the point covers all of it. {signs} Making either constant negative changes only the direction it goes round.

[c7.g2.3] {hyp} The second curve, the same move. {identity} Now the identity from part two, cosh squared minus shine squared equals one, gives ex over A, all squared, minus why over B, all squared, equals one. {hyperbola} That's a hyperbola, with two branches. {ask} But does the point reach both? {pause=1.5}

[c7.g2.4] {catch} Look at ex over A. It's cosh of theta, and cosh is at least one. {sign} So ex has the same sign as A, and is at least as far out as mod A. {right} So for positive A, the point stays on the right-hand branch. {flip} For negative A, it stays on the left. {whole} The point's why coordinate is B, times shine of theta, which takes every real value. So the point runs along the whole of one branch, and never reaches the other.

[c7.g2.5] {asym} For the sketch, far out the branch hugs the lines why equals plus or minus B over A, times ex. {slip} The tempting mistake is to draw both branches, because the equation has both. {pm} This point reaches only one. In part six, it took a plus or minus in front of cosh to draw the other.

## Scene 4 · G3: six sketches (ch7_s4_g3)

> Card G3 enlarged + ‖. All panels use ch3's equal-unit axes and styling: TEAL for the hyperbolic curves and a lighter TEAL for their inverses (as ch3 s4 and s6), GOLD for e^x and a lighter GOLD for ln x (e^x reflected), the mirror line y = x dashed, YELLOW dots on key points. On {mirror} a curve flips over the dashed y = x; on {pairs} the six names regroup into pairs: e^x | ln x, tanh x | tanh⁻¹ x, and sinh⁻¹ x with a ghost sinh x (TEAL, dimmed); cosh x on its own.
> Panel 1 ({exp}): e^x through (0, 1) with a short slope-1 tangent; the negative x axis lights YELLOW as its asymptote. On {log} it reflects into ln x: only x > 0, the dot (1, 0) with slope 1, the y axis dashed as its vertical asymptote, a slow climb on the right.
> Panel 2 ({cosh}): cosh x alone, minimum dot (0, 1), even; on {halves} dashed ½e^x (GOLD) on the right, ½e^{−x} (PURPLE) on the left, exactly Figure 25(a) as in ch3 s2. On {nomirror} its reflection in y = x appears faint: ch3 s5's sideways curve, upper branch TEAL, lower PURPLE, "two values for each x".
> Panel 3 ({sinh}): the ghost sinh through the origin, slope 1; on {asinh} its mirror sinh⁻¹ x (solid TEAL) bending over, with a faint dashed ln(2x) beside it for large x; label "all real x, no asymptotes".
> On {tanh}: ch3 s6's pair: tanh x between dashed y = 1 (GOLD) and y = −1 (PURPLE); on {atanh} the dashed lines swing to vertical x = 1 (GOLD) and x = −1 (PURPLE) as tanh reflects into tanh⁻¹ x, which runs off to +∞ and −∞ beside them.
> On {features}: the six final sketches in the sheet's order (a)–(f) as a 2×3 grid, each tagged with its marks: (a) (0, 1), y → 0; (b) min (0, 1), even; (c) y = ±1, odd; (d) (1, 0), x = 0, x > 0; (e) slope 1 at 0, odd; (f) x = ±1, odd.
> Checked with sympy 1.14 / numpy 2.1: values and slopes at the marked points (e^x: 1, 1; ln x at 1: 0, 1; sinh⁻¹, tanh, tanh⁻¹ at 0: 0, 1; cosh at 0: 1, 0); sinh⁻¹ 100 = 5.29834 against ln 200 = 5.29832; tanh⁻¹ x → +∞ as x → 1 from below and −∞ as x → −1 from above.

[c7.g3.1] {card} Question G three. Sketch six graphs, E to the ex, cosh, tanch, log of ex, inverse shine, and inverse tanch. {pause} {stop} Pause, and sketch them. {pause=1.5}

[c7.g3.2] {mirror} Here's the shortcut. Each inverse is its function reflected in the line why equals ex. {pairs} So log pairs with E to the ex, inverse tanch with tanch, and inverse shine with shine, which the sheet leaves out, but is easy to draw first.

[c7.g3.3] {exp} E to the ex passes through the point zero, one, with slope one. On the left it sinks towards the ex axis, but stays positive. {log} Reflect it to get log of ex. It exists only when ex is positive, crosses the ex axis at one, and plunges down beside the why axis as ex shrinks to zero. On the right it keeps climbing, slowly.

[c7.g3.4] {cosh} Cosh stands alone. It's even, with its lowest point at zero, one, so it never meets the ex axis. {halves} Far out, it follows half of E to the ex on the right, and half of E to the minus ex on the left, as in part three. {nomirror} Its mirror image would give two values for each ex, which is why inverse cosh had two branches.

[c7.g3.5] {sinh} Shine is odd, and climbs through the origin with slope one. {asinh} Its mirror, inverse shine, starts the same way, then bends over and grows like the log of two ex. It's defined for every ex, with no asymptotes.

[c7.g3.6] {tanh} Tanch is odd too, with slope one at the origin, squeezed between why equals minus one and why equals one. {atanh} Reflect it, and those asymptotes turn vertical. Inverse tanch lives between ex equals minus one and ex equals one, and runs off to plus and minus infinity at the edges. {features} For every sketch, mark where it crosses the axes, its asymptotes, and its symmetry.

## Scene 5 · G4: tanh⁻¹ x as a log, and its derivative (ch7_s5_g4)

> Card G4 enlarged + ‖.
> On {ex34} ch3 s6's chain, compact, same colours (e^y GOLD, e^{−y} PURPLE): x = tanh y → x(e^y + e^{−y}) = e^y − e^{−y} → (1 − x)e^{2y} = 1 + x → e^{2y} = (1 + x)/(1 − x). On {log}: tanh⁻¹ x = ½ ln[(1 + x)/(1 − x)], |x| < 1, boxed (square brackets, as the notes).
> On {split}: a number line from −1 to 1 with 1 + x > 0 and 1 − x > 0 ticked GREEN, then tanh⁻¹ x = ½[ln(1 + x) − ln(1 − x)]. On {first}: d/dx ln(1 + x) = 1/(1 + x). On {second}: d/dx ln(1 − x) = 1/(1 − x) · (−1), the chain-rule factor (−1) in YELLOW. On {minus} the two minuses meet and become +: ½[1/(1 + x) + 1/(1 − x)].
> On {common}: (1 − x) + (1 + x) = 2 over (1 + x)(1 − x) = 1 − x², the 2 cancelling the ½. On {answer}, boxed YELLOW: d/dx tanh⁻¹ x = 1/(1 − x²).
> On {slip} a RED version with the (−1) dropped: ½[1/(1 + x) − 1/(1 − x)]; on {wrong} = −x/(1 − x²), with a small RED falling curve for 0 < x < 1 beside G3's rising tanh⁻¹ graph (from s4).
> On {checks}: G3's tanh⁻¹ x graph (s4 styling) on top, the graph of 1/(1 − x²) below it on −1 < x < 1, sharing dashed vertical lines x = 1 (GOLD) and x = −1 (PURPLE), as in s4 and ch3 s6. On {pos} the lower curve sits above the axis; on {one} its value 1 at x = 0 (YELLOW dot) matches the slope-1 tangent at the origin above; on {blow} it shoots up at both dashed lines.
> On {flip}: x = tanh y; dx/dy = sech² y, tagged "sheet H2(g), next lecture"; on {sech} = 1 − tanh² y (ch2's list) = 1 − x²; on {recip} dy/dx = 1/(dx/dy) = 1/(1 − x²), flashing against the boxed answer.
> Checked with sympy 1.14: diff of ½(ln(1 + x) − ln(1 − x)) minus 1/(1 − x**2) simplifies to 0 (and sympy's own diff(atanh(x)) is 1/(1 - x**2)); the dropped-minus version factors to x/((x - 1)*(x + 1)); diff(tanh(y)) is 1 - tanh(y)**2.

[c7.g4.1] {card} Question G four. Express inverse tanch of ex as a logarithm, and differentiate it. {pause} {stop} Pause, and try it. {pause=1.5}

[c7.g4.2] {ex34} The first half is Example thirty-four. Write ex as tanch of why, clear the fractions, and E to the two why equals one plus ex, over one minus ex. {log} Take logs, and divide by two. Inverse tanch of ex is a half, times the log of the ratio, one plus ex, over one minus ex, for ex between minus one and one.

[c7.g4.3] {split} Now split the log. Between minus one and one, both one plus ex and one minus ex are positive, so the log of the quotient is a difference of logs. {first} The first, log of one plus ex, differentiates to one over one plus ex. {second} The second, log of one minus ex, gives one over one minus ex, times the derivative of one minus ex, which is minus one. {minus} That minus meets the minus in front, and makes a plus.

[c7.g4.4] {common} Over the common denominator, one minus ex squared, the top is two, and the half cancels it. {answer} So the derivative of inverse tanch is one, over one minus ex squared. {pause} {slip} The easy slip is to drop the chain-rule minus. {wrong} That gives minus ex, over one minus ex squared, which is negative for every positive ex. But inverse tanch always climbs.

[c7.g4.5] {checks} The right answer passes three checks. {pos} It's positive everywhere, so the graph rises. {one} It's one at the origin, the slope we drew in G three. {blow} And it blows up near plus and minus one, at the vertical asymptotes. {flip} One more, ahead of next lecture. With ex equal to tanch of why, the derivative of ex with respect to why is the hyperbolic secant squared, from question H two. {sech} By the family list from part two, that's one minus tanch squared, which is one minus ex squared. {recip} Turn it upside down, and it's the same answer.

## Scene 6 · Recap (ch7_s6_recap)

> On {recap}, four small panels in a 2×2 grid, the card colours from s1, each lit on its sentence with a short line under it.
> On {r1}: s2's boxed tanh(x + y) formula under the dimmed BLUE tan formula, the − turning into the YELLOW + — "divide by cosh x cosh y". On {r2}: s3's two sketches, small: the BLUE ellipse with its running point, and the TEAL hyperbola with the right branch solid, the left dashed with the RED ✗ — "cosh θ ≥ 1: one branch".
> On {r3}: s4's tanh / tanh⁻¹ panel, the dashed y = x between them, the asymptotes swinging — "inverse = mirror in y = x". On {r4}: s5's boxed d/dx tanh⁻¹ x = 1/(1 − x²) over its graph, the YELLOW (−1) chip beside it — "mind the chain-rule minus".
> On {next}: the grid shrinks away; "Next lecture: differentiation (Chapter 4 of the notes)", as ch6 s8 words it, with a sheet card "H2: d/dx sinh x, d/dx cosh x, d/dx tanh x, from exponentials" (GOLD e^x and PURPLE e^{−x} chips). On {end}, and after the last word, hold an end card for about 8 seconds (music carries it).

[c7.recap.1] {recap} Let's recap. {r1} For G one, divide through by cosh of ex, times cosh of why, and you get a plus underneath, where the tangent formula has a minus. {r2} For G two, cosine and sine trace the whole ellipse, but with shine and cosh, the point reaches only one branch of the hyperbola. {r3} For G three, each inverse is its function mirrored in the line why equals ex. {r4} For G four, inverse tanch is a log, with derivative one, over one minus ex squared. Mind the chain-rule minus. {pause}

[c7.recap.2] {next} Next time, differentiation, chapter four of the notes. Section H of the sheet asks you to differentiate shine, cosh, and tanch, starting from their exponentials. {end} Well done for working through these.
