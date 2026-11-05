# Chapter 6 · Hyperbolas and the conic family

NST IA Mathematics · Lecture 11 (Hyperbolic Functions and Conics), part 6 of 7. Source: notes pp. 44–45 (§3.5.3, equation (102), Figures 27–28); the lecturer's handwritten summary sheet (lecture 49:18–54:55, final version from 51:39 in the digest); Examples Sheet I p. 9 (section G).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch6_s1_hook)

> Title card: "Hyperbolic Functions and Conics", "NST IA Mathematics · Lecture 11", "Part 6 · Hyperbolas and the conic family".
> Last time, small, side by side: ch5's BLUE circle with `x² + y² = r²` above it, and Example 36's tall BLUE ellipse as ch5 s6 left it (centre (−1, 3) YELLOW, semi-major GOLD, semi-minor GREEN). On {circle} the `+` in the circle's equation pulses.
> On {flip} the circle and ellipse dim and slide aside; the equation moves to the centre. Its `+` turns YELLOW, flips over and lands as a YELLOW `−`, and `r²` becomes `s²`: `x² − y² = s²`. A GOLD "?" beside it.
> On {pair}, ch1 s1's glimpse comes back, small, under the equation: the BLUE point (cos θ, sin θ) running on the unit circle beside the TEAL point (cosh θ, sinh θ) running on its curve. Over the TEAL point, "why hyperbolic?" in YELLOW.
> Leave the "?" and the pair up as the scene ends: s2 answers the first question, s3 the second.

[c6.hook.1] {title} This is part six, on hyperbolas and the family of curves they belong to. {last} Last time, we drew circles and ellipses. {circle} Both came from adding two squares, like ex squared, plus why squared, equals the radius squared.

[c6.hook.2] {flip} Now flip that plus sign to a minus. {minus} Ex squared, minus why squared, equals S squared, where S is a constant. {ask} What curve is that? {pause} {pair} And there's a question left over from part one. Why are shine and cosh called hyperbolic? {pause} {promise} By the end of this part, you will be able to answer both, and to name almost any curve of this kind at a glance.

## Scene 2 · Flip one sign (ch6_s2_hyperbola)

> Hero: one set of axes, −4 to 4 both ways (Figure 27's window), centred. Top-left, as the notes write it: `x² − y² = s²   (102)` with "s: a non-zero real constant" under it. On {one} the `s²` becomes `1` (GOLD): `x² − y² = 1`.
> On {root}, `y = ±√(x² − 1)` grows out of the equation (TransformFromCopy), the `±` in YELLOW. On {band} a light RED band covers −1 < x < 1, labelled "no real y".
> The four quarter-pieces, drawn one per mark in TEAL, each with the lecturer's handwritten label from the lecture (digest 44:58): {tr} top right `+√(x² − s²), x > s`; {tl} top left `+√(x² − s²), x < −s`; {bottom} bottom right `−√(x² − s²), x > s` and bottom left `−√(x² − s²), x < −s`. Signs in YELLOW, the rest of each label white.
> On {join} the labels fade and the pieces fuse into two TEAL branches, through YELLOW vertex dots at (1, 0) and (−1, 0). On {name} the word "hyperbola" (TEAL), and the notes' caption small: "Figure 27: Simple hyperbola given by x² − y² = 1."
> General s: on {cond} the condition as the notes print it, `|x| ≥ |s|`; on {vertices} the vertex labels become `s` and `−s`; on {gap} a GOLD brace across the empty band reads `2s`.
> Asymptotes: on {lines} dashed lines y = x and y = −x fade in (dim white). A marker rides far up the right branch while a zoom-out shows the gap to y = x shrinking; `√(x² − s²) ≈ |x|` beside it, with a small "not in the notes" tag.
> Keep the axes, the s = 1 hyperbola and the dashed asymptotes: s3 draws on this same picture. (Checked with sympy 1.14.0: √(x² − s²) − x → 0 as x → ∞, the gap being −s²/(√(x² − s²) + x), so the curve stays strictly inside y = ±x.)

[c6.flip.1] {eq} Here's the new curve, as the notes write it. Ex squared, minus why squared, equals S squared, where S is a non-zero real constant. {one} To see its shape, take S equal to one, as the figure in the notes does. {solve} Then make why the subject, the same way you would for a circle. {root} That gives why equals plus or minus the square root of ex squared minus one.

[c6.flip.2] {real} That square root is real only when ex squared is at least one. {band} So ex must be at least one, or at most minus one. In the band between minus one and one, there's no curve at all. {pause}

[c6.flip.3] {quarters} Now build the curve one piece at a time. {tr} Take the plus sign, with ex greater than one. That's this piece, rising from the ex axis at one. {tl} The plus sign with ex less than minus one gives its mirror image on the left. {bottom} And the minus sign gives the two pieces underneath. {join} Put the four quarter-pieces together, and they join into two branches, opening left and right. {name} This curve is a hyperbola.

[c6.flip.4] {general} Now back to a general S. {cond} The condition is that the modulus of ex is at least the modulus of S. {pos} Take S positive, as the lecturer did. {vertices} Then the branches start at the vertices, ex equals S and ex equals minus S, {gap} with an empty band two S wide between them.

[c6.flip.5] {asym} One more thing makes the sketch easy, though the notes leave it out. {far} Far from the centre, ex squared is huge, and taking away S squared hardly changes it. {close} So the square root is close to the modulus of ex, {lines} and the branches creep towards the two lines, why equals ex, and why equals minus ex. {name2} These lines are the asymptotes. The curve gets closer and closer to them, but never touches. {pause}

## Scene 3 · cosh and sinh draw it (ch6_s3_param)

> Start from ch5 s5's shot, small, top-left: the BLUE circle with its running point, `x = r cos θ,  y = r sin θ` and, under it, `cos² θ + sin² θ = 1`. On {identity}, ch2 s2's card `cosh² θ − sinh² θ = 1` (TEAL, the minus in YELLOW) appears beside it.
> Main: s2's axes, the s = 1 hyperbola and its dashed asymptotes. The notes' working, line by line, top-right: {sub} `x = r cosh θ,  y = r sinh θ` → {square} `x² − y² = r² cosh² θ − r² sinh² θ` → {factor} `= r²(cosh² θ − sinh² θ)` (the r² slides out to the front) → {one} `= r²` (the bracket glows and collapses to 1, TransformFromCopy from the identity card). On {match}: `r² = s²` → `r = ±s`, boxed YELLOW, with the notes' line "Each sign gives one branch."
> Branches: on {ge} a GREEN tag `cosh θ ≥ 1`. On {right} a TEAL point traces the right branch as θ runs from about −2 to 2 (GOLD θ readout), label `x = s cosh θ`; on {left} a PURPLE point traces the left branch (the minus branch PURPLE, as ch3 s5 coloured cosh⁻¹'s; it's the branch ch1 s1's glimpse left dim), label `x = −s cosh θ`. On {ynosign} the lecturer's form from Figure 28's handwriting: `x = ±s cosh θ,  y = s sinh θ`, the `±` on x YELLOW and a small "no ± on y".
> On {pair}, split screen (ch1 s1's glimpse, now explained): left, the BLUE unit circle with its point (cos θ, sin θ); right, the TEAL hyperbola x² − y² = 1 with its point (cosh θ, sinh θ); both driven by one shared GOLD θ readout. On {answer} captions "circular functions draw circles" (BLUE) and "hyperbolic functions draw hyperbolas" (TEAL); hook's "why hyperbolic?" turns into a GREEN tick.
> On {angle}: on the circle, θ marked as the angle at the centre. On {param}: on the hyperbola, a dim ray from the origin to the running point; the arc between the ray and the x-axis is labelled "not θ". On {wedge} the point runs far out and the ray stays inside the dashed asymptote y = x, a small "< 45°" by the arc. Caption: "θ is a parameter, not an angle".
> Checked with sympy 1.14.0: (r cosh θ)² − (r sinh θ)² = r², and cosh² θ − sinh² θ = 1. The ray's angle is arctan(tanh θ): 24.8° at θ = 0.5, 37.3° at θ = 1, 43.95° at θ = 2, always under 45°.

[c6.param.1] {back} Last time, cosine and sine drew the circle. {why} That worked because cosine squared, plus sine squared, is one. {need} For a hyperbola you'd want the same trick, but with a minus sign. You need two functions whose squares differ by one. {pause} {identity} You already have them, from part two. Cosh squared, minus shine squared, equals one.

[c6.param.2] {sub} So, as the notes do, put ex equal to R, times cosh theta, and why equal to R, times shine theta, where R is a constant. {square} Square both, and subtract. {factor} R squared comes out as a common factor, {one} and what's left in the bracket is cosh squared, minus shine squared, which is one. {result} So ex squared, minus why squared, is R squared. {match} To match S squared, the constant R must be plus or minus S. {pause}

[c6.param.3] {branch} The notes add that each sign gives one branch. {ge} That's because cosh theta is always at least one, so ex always has the same sign as R. {right} With R equal to S, ex is at least S, and you get the right branch. {left} With R equal to minus S, you get the left branch. {ynosign} The why coordinate needs no plus or minus. Shine theta takes every real value, so as theta runs over all the real numbers, the point sweeps out a whole branch, end to end.

[c6.param.4] {pair} Now put two running points side by side, driven by the same theta. {circ} Cosine theta and sine theta go round the circle. {hyp} Cosh theta and shine theta run along the hyperbola. {pause} {answer} That answers the question from part one. Circular functions draw circles, and hyperbolic functions draw hyperbolas. That's where the name comes from. {pause}

[c6.param.5] {angle} One warning. On the circle, theta is the angle of the point. {param} On the hyperbola, theta is only a parameter, a label for each point. {wedge} The point's real angle from the ex axis always stays within forty-five degrees, however far it runs, because the branch stays inside its asymptotes.

## Scene 4 · A quarter turn (ch6_s4_turn)

> s2's picture (s = 1, TEAL, dashed asymptotes) shrinks into the left half, labelled with the lecturer's handwriting from Figure 28: `x = ±s cosh θ`, `y = s sinh θ`, `x² − y² = s²`.
> Centre top, on {rhs}: (102) again, `x² − y² = s²`; on {neg} the right-hand `s²` turns YELLOW and gains a minus: `x² − y² = −s²`. On {across} the terms move across: `y² − x² = s²`. On {swap} the x and the y glow YELLOW and visibly trade places with the left-hand equation.
> Right half, on {turn}: a copy of the left hyperbola (TransformFromCopy) reflects in the dashed line y = x (shown as a mirror). On {quarter} a faint ghost turns a quarter turn about the origin and lands on the same curve.
> On {updown} the branches open up and down; on {vertices} YELLOW dots at (0, 1) and (0, −1) on the y-axis, labelled `s` and `−s`. On {asym} the dashed asymptotes y = ±x are highlighted in both halves: the same two lines.
> On {param2}, under the right half: `x = s sinh θ`, `y = ±s cosh θ`, cosh and sinh trading places with the left labels (TransformFromCopy). The notes' caption, small, under both: "Figure 28: Hyperbolae at different orientations." (Checked with sympy 1.14.0: x = s sinh θ, y = s cosh θ gives y² − x² = s², and the quarter turn (x, y) → (−y, x) maps x² − y² = s² onto y² − x² = s².)

[c6.turn.1] {rhs} The notes ask one more question. What if you reverse the sign on the right-hand side instead? {neg} Then ex squared, minus why squared, equals minus S squared. {pause} {across} Move both terms across, and it reads why squared, minus ex squared, equals S squared. {swap} It's the same equation, with ex and why swapped.

[c6.turn.2] {turn} Swapping ex and why reflects the picture in the line why equals ex. {quarter} For this curve, that's the same as a quarter turn. {updown} So now the branches open up and down, {vertices} with their vertices on the why axis, at S and minus S. {asym} The asymptotes are the same two lines. {param2} And the parametric form swaps too. Ex equals S, times shine theta, and why equals plus or minus S, times cosh theta. {pause}

## Scene 5 · One equation, many shapes (ch6_s5_classify)

> Top, on {all}: the general equation from the lecturer's sheet, `ax² + bx + cy² + dy + e = 0`, with small icons of today's circle, ellipse and hyperbola beside it. On {noxy} ch5 s4's tilted ellipse, small and dim, with "has an xy term: not here".
> On {form} the x terms and the y terms each pull together into a bracket (TransformFromCopy): `a(x − x₀)² + c(y − y₀)² = f`. On {names} a and c turn YELLOW; on {careful} a RED tag "a, c: coefficients, not the semi-axes" (and a dim ghost of ch5's GOLD/GREEN semi-axis labels being crossed out).
> On {divide}: `(a/f)(x − x₀)² + (c/f)(y − y₀)² = 1`, "f ≠ 0". The lecturer's table (her final sheet, digest 51:39) sits below in her row order, each row filling in on its mark with a small icon:
> `circle       a = c   and   f/a > 0` (BLUE circle, on {circle}); `ellipse      a·c > 0   and   a·f > 0,   a ≠ c` (BLUE ellipse, on {same}); `hyperbola    a·c < 0 ,  f ≠ 0` (TEAL hyperbola, on {opp}); `no solution  a·c > 0   and   a·f < 0` (RED ∅, on {neg}). On {sheet} a small key: "a·c > 0: same sign", "a·c < 0: opposite signs".
> Test, on {ex36}: Example 36 from ch5 s6, `2x² + 4x + y² − 6y + 7 = 0` → `2(x + 1)² + (y − 3)² = 4`; on {read} `a = 2, c = 1, f = 4` in GOLD; on {verdict} the ellipse row lights GREEN and ch5's tall ellipse appears small beside it.
> On {turned}: s4's `y² − x² = s²`, read as `a = −1, c = 1`; on {verdict2} the hyperbola row lights GREEN, with s4's up-and-down hyperbola small beside it.
> Keep the table: s6 starts from it. (Checked with sympy 1.14.0: 2x² + 4x + y² − 6y + 7 = 2(x + 1)² + (y − 3)² − 4, semi-axes √2 and 2 as in ch5; each verdict in s5 and s6 checked against the table.)

[c6.class.1] {all} Every curve we've drawn today, except the tilted ellipse, fits one general equation. {terms} Some number times ex squared, plus some number times ex, then the same two kinds of term in why, plus a constant, all equal to zero. {noxy} There's no term with ex times why, and that's what keeps these curves lined up with the axes.

[c6.class.2] {complete} Complete the square in ex, and again in why, just as in Example thirty-six. {form} You get a multiple of one square in ex, plus a multiple of one square in why, equal to a constant, F. {names} Call the two multiples the coefficients, A, and C. {careful} Careful here. These letters are coefficients now, not the semi-major and semi-minor axes from last time. The lecturer stopped to sort out these letters in the lecture too.

[c6.class.3] {divide} Now suppose F is different from zero, and divide both sides by it. {decide} Then the signs decide everything. {same} If both coefficients have the same sign as F, you get two squares adding up to one. That's an ellipse, {circle} and it's a circle when the two coefficients are equal. {pause}

[c6.class.4] {opp} If the coefficients have opposite signs, one square is taken away from the other. That's a hyperbola. {neg} And if both coefficients have the sign opposite to F, two squares would have to add up to a negative number. There's no solution at all. {sheet} On the lecturer's sheet, same sign is written as a product greater than zero, and opposite signs as a product less than zero.

[c6.class.5] {test} Now test the table. {ex36} Last time, Example thirty-six became two times a square in ex, plus one times a square in why, equal to four. {read} So the coefficients are two and one, and F is four. {verdict} All three are positive, and the coefficients are different. So it's an ellipse, just as we found. {turned} And the turned hyperbola from a moment ago? {pause} {verdict2} Its coefficients are minus one and one, with opposite signs. So it's a hyperbola.

## Scene 6 · The odd cases (ch6_s6_odd_cases)

> s5's table shrinks to the top-left, still readable; on {gap} a GOLD "f = 0 ?" beside it.
> Crossing lines: on {shrink} s2's TEAL hyperbola with its dashed asymptotes, a GOLD readout `s = 1` running down through 0.5 and 0.1 to 0. On {collapse} the vertices slide into the origin and the branches flatten onto the asymptotes; on {lines} the asymptotes turn solid TEAL: `x² − y² = 0  ⇒  y = ±x`.
> Point: on {circle} ch5's BLUE circle shrinks the same way; on {point} it ends as a single YELLOW dot at the origin: `x² + y² = 0`.
> On {outside}, two cases outside the table, side by side, small: {parabola} a parabola `y = x²` (the missing `cy²` shown as `c = 0` in YELLOW); {parallel} two parallel vertical lines `x² = 1`, at x = −1 and x = 1.
> On {family}, a grid of every shape from this chapter and the last, under `ax² + bx + cy² + dy + e = 0`: circle, ellipse, hyperbola, ∅ (RED), crossing lines, point, parabola, parallel lines; one lights per item on {list}. The lecturer's words as a caption: "One equation, a lot of possibilities."
> On {end} a small stamp: "End of Chapter 3 of the notes".

[c6.odd.1] {gap} The table leaves out one case. What if F is zero? {pause} {shrink} Watch the hyperbola as S shrinks towards zero. {collapse} The vertices slide into the centre, and the branches close in on their asymptotes. {lines} At S equals zero, ex squared minus why squared equals zero, which is just two crossing lines, why equals ex, and why equals minus ex.

[c6.odd.2] {circle} Shrink a circle the same way, and you're left with ex squared, plus why squared, equals zero. {point} Only one point satisfies that, the origin. {pause} {outside} Some curves fall outside the table altogether, because a squared term is missing. {parabola} The curve why equals ex squared has no why squared term, and it's a parabola. {parallel} The equation ex squared equals one has no why at all. It's two parallel lines, ex equals one, and ex equals minus one.

[c6.odd.3] {family} So, as the lecturer put it, one equation has a lot of possibilities. {list} Circles, ellipses, hyperbolas, crossing lines, a point, a parabola, parallel lines, or nothing at all. {end} And that closes chapter three of the notes. {pause}

## Scene 7 · Examples Sheet G: four hints (ch6_s7_hints)

> Header "Examples Sheet I · G. Hyperbolic functions"; four dim cards in a row and a small note "solutions: Part 7 (bonus)". Each card in turn grows to the hero position and shrinks back when done (ch7 s1 reuses these cards). Card text verbatim from the sheet (p. 9):
> G1: "Express tanh(x + y) in terms of tanh x and tanh y."
> G2: "Consider the set of points in the x, y plane described by: i. (x, y) = (a cos θ, b sin θ); and ii. (x, y) = (a cosh θ, b sinh θ), where a and b are real, non-zero and fixed and θ is a real parameter. In each case, find the Cartesian equation of the locus and sketch it."
> G3: "Sketch the graphs of the following functions: (a) eˣ (b) cosh x (c) tanh x (d) ln x (e) sinh⁻¹ x (f) tanh⁻¹ x."
> G4: "Express tanh⁻¹ x as a logarithm and differentiate."
> Hints under each card, never a solution. G1 ({hint1}): ch2 s6's Example 33 card, small, its A, B turning into x, y in YELLOW; on {exp} "try exponentials too" and "check: sign-flip rule". G2 ({hint2}): the two identity cards, `cos² θ + sin² θ = 1` (BLUE) and `cosh² θ − sinh² θ = 1` (TEAL); on {which} a GOLD "which part?" beside a GREEN `cosh θ ≥ 1`.
> G3 ({pairs}): three empty mini-axes, each with a dashed mirror line y = x, labelled `eˣ ↔ ln x`, `sinh x ↔ sinh⁻¹ x` (sinh x tagged "draw first"), `tanh x ↔ tanh⁻¹ x`; on {cosh} a fourth, `cosh x`, alone; on {mark} small tags "intercepts", "asymptotes". G4 ({hint4}): ch3 s6's result `tanh⁻¹ x = ½ ln[(1 + x)/(1 − x)]`, |x| < 1; on {split} a YELLOW bracket under the log of the quotient, "split first"; on {chain} a YELLOW ring round `(1 − x)`.
> On every {pause=2}, the screen holds still with a small "pause and try it" label.

[c6.hints.1] {turn} Now it's your turn. {sheet} Section G of the first examples sheet has four questions on hyperbolic functions. {plan} For each one, here's a hint, but no solution. The worked solutions are in part seven, the bonus.

[c6.hints.2] {g1} Question G one. Express tanch of the sum, ex plus why, in terms of tanch of ex and tanch of why. {hint1} You've done this already. It's Example thirty-three from part two, with new letters. {exp} So try a second route as well, starting from exponentials, and check your answer with the sign-flip rule. {try} Pause, and try it. {pause=2}

[c6.hints.3] {g2} Question G two traces two curves with a parameter, theta. {first} In the first, ex equals the constant A, times cosine theta, and why equals the constant B, times sine theta. {second} In the second, cosine changes to cosh, and sine to shine. {task} Find the Cartesian equation of each curve, and sketch it. {hint2} Get rid of theta with the right identity, the way we checked the hyperbola earlier. {which} Then ask which part of the curve the point really reaches. Remember that cosh theta is at least one. {try} Pause, and try it. {pause=2}

[c6.hints.4] {g3} Question G three asks for six sketches. {pairs} Pair each function with its inverse, and draw them together. E to the ex with the log of ex, shine with inverse shine, and tanch with inverse tanch. Each inverse is its function reflected in the line why equals ex. {cosh} Cosh stands on its own. {mark} For every graph, mark where it crosses the axes, and draw its asymptotes. {try} Pause, and give it a go. {pause=2}

[c6.hints.5] {g4} Question G four. Express inverse tanch of ex as a log, and differentiate. {hint4} That log form is Example thirty-four, from part three. {split} Before you differentiate, split the log of a quotient into a difference of two logs. {chain} And watch the chain rule on the second one. {try} Pause, and try it. {pause=2}

## Scene 8 · Recap (ch6_s8_recap)

> Five small panels (a row of three over a row of two), each a small version of the shot that taught it, same objects and colours, its short line under it, one per mark:
> {h} s2's TEAL hyperbola (s = 1) with its four quarter-piece labels (tiny) and dashed asymptotes → "x² − y² = s²: two branches, two asymptotes".
> {p} s3's pair, the BLUE circle point and the TEAL hyperbola point on one GOLD θ → "cosh and sinh draw the hyperbola".
> {t} s4's two orientations, Figure 28 style → "flip the right-hand side: a quarter turn".
> {c} s5's table, small, with Example 36's ellipse row lit GREEN → "complete the squares, read the signs".
> {o} s6's shrinking hyperbola collapsing onto its solid crossing lines, with the tiny parabola and parallel lines beside it → "f = 0, or a missing square: the odd cases".
> On {bonus} the four G cards from s7 in a short row, "solutions: Part 7 (bonus)"; on {next} "Next: differentiation (Chapter 4 of the notes)".
> End card: hold about eight seconds after the last word; music carries it.

[c6.recap.1] {r1} Time for a recap. {h} Flip one sign in the circle's equation, and you get a hyperbola, with two branches and two asymptotes. {p} Shine and cosh draw it, just as cosine and sine draw a circle. That's why they're called hyperbolic. {t} Flip the sign on the right-hand side, and the hyperbola makes a quarter turn. {c} For any curve of this kind, complete the squares, then read the signs. {o} And when F is zero, or a square is missing, you get the odd cases, like crossing lines, a point, or a parabola.

[c6.recap.2] {bonus} Part seven, the bonus, works through all four questions from section G. {next} Next time, we start differentiation, chapter four of the notes. {pause} {bye} See you there.
