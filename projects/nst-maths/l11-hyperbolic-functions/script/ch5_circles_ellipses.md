# Chapter 5 · Circles and ellipses

NST IA Mathematics · Lecture 11 (Hyperbolic Functions and Conics), part 5 of 7. Source: N. G. Berloff's
notes, `Chapter234_to_annotate.pdf` pp. 40–44 (§3.5.1–3.5.2, (98)–(101); Example 36 on p. 43 is blank,
its working is from the lecture digest, 40:00–44:08); lecture 32:42–44:58; Examples Sheet I, E2 (the circle).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch5_s1_hook)

> Title card: "Hyperbolic Functions and Conics", "NST IA Mathematics · Lecture 11", "Part 5 · Circles and ellipses".
> On {last}: ch4 s6's Argand lattice, small, styled exactly as ch4 s6 left it (GREEN crosses, BLUE 2π brace, TEAL height brace, i and the Im label PINK) with `z = 2πm ± i ln(2 + √3)` under it; it dims and clears on {turn}, where a BLUE circle and a BLUE ellipse draw themselves side by side, then shrink away.
> On {eq}: Example 36's equation, large and centred, white: `2x² + 4x + y² − 6y + 7 = 0`. A box slides on the spoken parts: `2x² + 4x` ({xpart}), then `y² − 6y + 7` ({ypart}). On {ask}: empty axes beside it with a big YELLOW "?".
> On {hint}: a faint BLUE circle equation `x² + y² = r²` appears under it for comparison. On {two}: the `2` in front of `x²` gets a YELLOW ring, and a ghost YELLOW `1` fades in before `y²`.
> On {cs}: the equation shrinks to the top left; the circle–hyperbola pair from ch1 s1 fades in: a BLUE circle `x² + y² = 1` with a point `(cos θ, sin θ)` running round it, and on {next}, beside it, a dim TEAL hyperbola `x² − y² = 1` with its point `(cosh θ, sinh θ)`, labelled "Part 6".

[c5.hook.1] {title} This is part five of Hyperbolic Functions and Conics. {last} Last time, you looked for every zed whose cosine is two, and found infinitely many, all complex. {turn} Now we turn to two familiar curves, circles and ellipses. {review} This part of the lecture is a review, so we'll move briskly, and slow down where people slip.

[c5.hook.2] {eq} Here's an equation from the notes. {xpart} It starts with two ex squared, plus four ex. {ypart} Then comes why squared, minus six why, plus seven, and all of that equals zero. {ask} What curve is this, and where does it sit? {pause} {hint} It looks almost like the equation of a circle. {two} But the ex squared has a two in front, and the why squared has only a one. {pause}

[c5.hook.3] {why} And why are circles part of a lecture on hyperbolic functions? {pause} {cs} Because cosine and sine draw circles. {next} And in part six, shine and cosh will do the same for a hyperbola.

## Scene 2 · The circle's equation (ch5_s2_circle)

> Centred axes. A YELLOW centre dot at the origin; a GOLD radius labelled `r` sweeps round once and traces the BLUE circle (the notes: every point the same distance from the centre).
> On {origin}: a point on the circle in the first quadrant, with dashed legs to the ex axis. On {tri}: legs `x` and `y` and hypotenuse `r` form a right triangle (right-angle mark). On {pyth}: `x² + y² = r²` builds from the three labels; on {tag} it gets the tag `(98)` and the notes' "for x, y, r ∈ ℝ".
> On {move}: the whole circle slides to a centre `(x₀, y₀)` in the first quadrant (YELLOW dot, dashed lines to both axes); the triangle rides along and on {legs} its legs relabel `x − x₀` and `y − y₀`. On {shift} the equation edits in place: `(x − x₀)² + (y − y₀)² = r²`. On {rule}, a small caption: "subtract the centre before squaring".
> On {expand}, the notes' two lines, each born from the one above: `x² − 2x₀x + x₀² + y² − 2y₀y + y₀² = r²`, then `x² − 2x₀x + y² − 2y₀y = r² − x₀² − y₀²`.
> On {terms}: the notes' form `x² + ax + y² + by + c = 0`, tag `(99)` on {general}, with braces linking `a` to `−2x₀`, `b` to `−2y₀` and `c` to `x₀² + y₀² − r²` (the last one moved across).
> On {hide}: the circle picture dims, its centre dot and radius fade out, and a YELLOW "?" sits where the centre was. Hold through the {pause}.
> Checked with sympy 1.14: the expansion, and the coefficients a = −2x₀, b = −2y₀, c = x₀² + y₀² − r².

[c5.circle.1] {def} A circle is every point at the same distance from a centre. That distance is the radius, R. {origin} Put the centre at the origin, and pick a point on the circle, at ex, why. {tri} Its two coordinates and the radius make a right-angled triangle. {pyth} So by Pythagoras, ex squared, plus why squared, equals R squared. {tag} That's equation ninety-eight in the notes.

[c5.circle.2] {move} Now move the centre to the point ex zero, why zero. {legs} The legs of the triangle are now ex minus ex zero, and why minus why zero. {shift} So the square of ex minus ex zero, plus the square of why minus why zero, equals R squared. {rule} To move the centre, subtract it before you square.

[c5.circle.3] {expand} Now multiply out the brackets, and gather everything on one side. {terms} You get ex squared, plus a number times ex, plus why squared, plus a number times why, plus a constant, equals zero. {general} That's equation ninety-nine, and the notes call the three numbers A, B and C. {hide} In this form, the centre and the radius are hidden inside them. {ask} So if you're handed an equation like this, how do you find the circle again? {pause}

## Scene 3 · Completing the square (ch5_s3_complete)

> (99) `x² + ax + y² + by + c = 0` stays at the top, carried over from s2.
> On {pic}, the square picture for `x² + ax`: a BLUE x-by-x square, and two strips `x` by `½a` along two of its sides. On {corner}, the missing `½a`-by-`½a` corner flashes YELLOW; on {add} it is added in, then a YELLOW copy is taken away. On {result}: `x² + ax = (x + ½a)² − (½a)²`.
> On {both}: the notes' line, the added and subtracted pairs YELLOW: `x² + ax + (½a)² − (½a)² + y² + by + (½b)² − (½b)² + c = 0`. On {close} it closes up into `(x + ½a)² + (y + ½b)² = (½a)² + (½b)² − c = r²`, the right-hand side boxed on {rhs}, and labelled `r²` on {rsq}.
> On {centre}: `centre (−½a, −½b)` in YELLOW, both minus signs flashing against the pluses in the brackets.
> On {warn}: a case card under the boxed right-hand side, one row per cue: {pos} `r² > 0` with a small BLUE circle; {zero} `r² = 0` with a single YELLOW point; {neg} `r² < 0` with a RED `∅` and "no points".
> Clear to Examples Sheet E2's circle (small label "Examples Sheet I, E2"): `x² − 2x + y² = 0` → on {half} `x² − 2x + 1 − 1 + y² = 0` → on {done} `(x − 1)² + y² = 1`. On {read}: axes, YELLOW centre `(1, 0)`, GOLD radius 1, BLUE circle; on {origin} flash the point where it passes through the origin.
> On {slide}: a GOLD constant `c` appears on the left: `x² − 2x + y² + c = 0` ⇒ `(x − 1)² + y² = 1 − c`. On {plus1}, c = 1: the right side reads `0` and on {point} the circle shrinks to the YELLOW point `(1, 0)`. On {plus2}, c = 2: `(x − 1)² + y² = −1`; on {none} the point blinks out and a RED "no points" takes its place. This is the case card made concrete.
> Checked with sympy 1.14: the completed form of (99); E2's circle; c = 0, 1, 2 give right-hand sides 1, 0, −1, and only `(1, 0)` solves the c = 1 equation.

[c5.complete.1] {undo} You run the expansion backwards, and that's called completing the square. {pic} Picture ex squared as a square, and the ex term as two strips along its sides, each as wide as half the number A. {corner} Together they're one small corner short of a bigger square. That corner's area is the square of its width. {add} So add the corner, and take it away again. {result} The ex terms become ex plus half the number A, all squared, minus the corner.

[c5.complete.2] {both} Do the same with the why terms, adding and subtracting their own corner. {close} The brackets close up into two perfect squares, {rhs} and everything else moves to the right. That's half the number A, squared, plus half of B, squared, minus C. {rsq} If that's positive, it's R squared, and you have a circle. {centre} Its centre is at minus half the number A, minus half of B, with the signs flipped, because each bracket has a plus.

[c5.complete.3] {warn} But the lecturer warned that not every equation of this form is a circle. {sign} It all depends on the sign of that right-hand side. {pos} Positive gives a circle. {zero} Zero gives a circle of radius zero, which is a single point. {neg} And negative gives no points at all, because two squares can never add up to a negative number. {pause}

[c5.complete.4] {e2} Here's an example, the circle from question E two of the examples sheet. Ex squared, minus two ex, plus why squared, equals zero. {half} Half of minus two is minus one. So add its square, which is one, and take it away again. {done} That gives ex minus one, all squared, plus why squared, equals one. {read} It's a circle with its centre at one, zero, and radius one, {origin} so it passes through the origin.

[c5.complete.5] {slide} Now put a constant on the left, and watch the radius. {plus1} Add one, and the right-hand side drops to zero. {point} The circle shrinks to the single point one, zero. {plus2} Add two, and the right-hand side is minus one. {none} No point in the plane fits that, so the equation describes nothing at all. {pause}

## Scene 4 · A stretched circle (ch5_s4_ellipse)

> Centred axes, the BLUE circle `x² + y² = r²` at the origin. On {divide}: the notes' line `x²/r² + y²/r² = (x/r)² + (y/r)² = 1`; on {same} both `r`s get YELLOW boxes (one scale in every direction).
> On {ab}: the two `r`s split, the one under x becoming `a` (GOLD) and the one under y becoming `b` (GREEN); on {eq} the equation reads `(x/a)² + (y/b)² = 1`, tag `(100)` and the notes' "equation of an ellipse" on {tag}. As the letters change, the circle stretches sideways into a wide BLUE ellipse.
> Intercepts on cue: {x0} `x = 0  ⇒  y = ±b` with GREEN ticks at ±b on the why axis; {y0} `y = 0  ⇒  x = ±a` with GOLD ticks at ±a on the ex axis. On {reach}: GOLD and GREEN arms from the origin out to a and b.
> On {major} and {minor}: the notes' first picture, a brace on a labelled "Semi-major axis" (GOLD) and one on b labelled "Semi-minor axis" (GREEN). On {tall}: the notes' second picture beside it, a tall ellipse (b > a), now with b's brace "Semi-major axis" (GOLD) and a's "Semi-minor axis" (GREEN). Colour follows the role, not the letter (the notes draw the major axis red; here GOLD, since RED means wrong).
> On {shift}: the wide ellipse slides to a YELLOW centre `(x₀, y₀)`: `((x − x₀)/a)² + ((y − y₀)/b)² = 1`.
> On {aligned}: its two braces line up with the axes (flash them). On {ib}, the notes' third picture: the ellipse tilts, its GOLD semi-major and GREEN semi-minor arrows tilting with it; a small label "NST IB" and the lecturer's handwritten `xᵀAx = s` beside it.
> On {general}: the notes' `More general form Ax² + Bxy + Cy² + Dx + Ey + F = 0` under the picture, with `Bxy` in YELLOW on {xy} (purple in the notes). On {noxy}: the ellipse turns back onto the axes and the `Bxy` term fades out.
> Checked with sympy 1.14: the intercepts of (100) are y = ±b at x = 0 and x = ±a at y = 0.

[c5.ellipse.1] {stretch} The notes call an ellipse a stretched circle. Here's what that means. {divide} Divide the circle's equation by R squared. {over} You get ex over R, all squared, plus why over R, all squared, equals one. {same} Ex and why are both divided by the same R, so the circle has the same scale in every direction.

[c5.ellipse.2] {two} Now give the two directions different scales. {ab} Divide ex by one number, A, and why by another, B. {eq} Ex over A, all squared, plus why over B, all squared, equals one. {tag} That's equation one hundred, the basic equation of an ellipse. {x0} Put ex equal to zero, and why is plus or minus B. {y0} Put why equal to zero, and ex is plus or minus A.

[c5.ellipse.3] {reach} So the circle now reaches as far as A, along the ex axis, and as far as B, along the why axis. {pos} The lecturer takes both numbers positive. {major} The larger one is called the semi-major axis, {minor} and the smaller one the semi-minor axis. {wide} If the stretch along ex is the larger, the ellipse lies wide. {tall} If the stretch along why is the larger, it stands tall.

[c5.ellipse.4] {shift} As with the circle, to move the centre, subtract it before you square. {aligned} But this ellipse always lines up with the axes. {ib} Tilted ellipses come next year, in second-year maths, written with a matrix. {general} The most general equation of this kind has a term in ex times why as well, {xy} and that term only appears when the ellipse is tilted. {pause} {noxy} So no ex why term means the ellipse is lined up with the axes.

## Scene 5 · Cosine and sine draw both (ch5_s5_param)

> Left half: the BLUE circle with YELLOW centre `(x₀, y₀)` (dashed lines to the axes, as in the lecturer's margin sketch), a GOLD radius `r` at angle `θ` from a dashed horizontal line, and a point running round it. On {fx} and {fy}: `x = x₀ + r cos θ`, `y = y₀ + r sin θ`; on {run}: `0 ≤ θ < 2π`.
> On {check}, the check, each line born from the one above: `(x − x₀)² + (y − y₀)² = r² cos²θ + r² sin²θ` → `= r²(cos²θ + sin²θ)`; on {one} the bracket is boxed and turns into `1`, leaving `= r²`.
> Right half, on {ell}: the ellipse version, a GOLD `a` and GREEN `b`: on {efx} `x = x₀ + a cos θ`, on {efy} `y = y₀ + b sin θ`. One θ dial now drives both running points.
> On {warn}, parameter versus angle on the ellipse (a wide one, a = 2, b = 1): a dashed auxiliary circle of radius a round it; θ's radius on that circle, with a vertical dashed drop to the ellipse point (the stretch). On {angle}: the true angle from the centre to the ellipse point, drawn in YELLOW. On {drift}: θ turns and the two angles separate (at θ = 45° the true angle is about 26.6°), meeting only at 0°, 90°, 180° and 270°. Caption: "θ is a parameter, not the angle".
> On {unit}: end on the unit circle at the origin with its point `(cos θ, sin θ)`, `x = cos θ, y = sin θ` and `cos²θ + sin²θ = 1` under it (ch6 s3 opens from this shot). On {next}: beside it a dim TEAL hyperbola `x² − y² = 1` with its point `(cosh θ, sinh θ)`, the circle–hyperbola pair from ch1 s1, labelled "Part 6".
> Checked with sympy 1.14: both parametrisations satisfy their equations; the angles at θ = 30°, 45°, 60° are 16.1°, 26.6°, 40.9° for a = 2, b = 1.

[c5.param.1] {param} A circle can also be drawn with cosine and sine. {fx} Ex equals ex zero, plus R times cosine theta, {fy} and why equals why zero, plus R times sine theta. {run} As theta runs from zero up to two pi, the point goes once round. {polar} These are polar coordinates about the centre, with theta the angle of the radius.

[c5.param.2] {check} To check, subtract the centre, then square and add. {sum} You get R squared, times cosine squared plus sine squared. {one} That bracket is one, so you get R squared, as you should. {pause} {ell} For the ellipse, scale the two directions separately. {efx} Ex equals ex zero, plus A, times cosine theta, {efy} and why equals why zero, plus B, times sine theta.

[c5.param.3] {echeck} The same check works, once the stretches are divided out. {warn} But here theta is only a parameter, the angle on the circle before the stretch. {angle} The angle from the centre to the moving point is a different thing. {drift} Watch the two drift apart, and agree only at the quarter turns. {pause}

[c5.param.4] {unit} Centre a circle of radius one at the origin, and the point is simply cosine theta, sine theta. {draw} Cosine and sine draw circles and ellipses. {next} Hold on to that picture. In part six, shine and cosh take over, and trace out a hyperbola.

## Scene 6 · Example 36 (ch5_s6_example)

> On {back}: the equation from s1 flies into the notes' Example 36 card (GREEN-edged, as in the notes): "Example 36: Properties of an ellipse" / "Find the centre and the semi-axes of the ellipse given by" / `2x² + 4x + y² − 6y + 7 = 0.`
> On {factor}: `2x² + 4x` becomes `2(x² + 2x)`, the `2` YELLOW. Then the lecturer's first line builds piece by piece: on {inside} `2(x² + 2x + 1)`; on {slip} a RED ghost `− 1` after it, which on {times} gets a YELLOW arrow from the `+ 1` inside through the `2` outside ("× 2") and on {sub} is crossed out and replaced by a GREEN `− 2`; on {yterms} `+ (y² − 6y + 9) − 9 + 7 = 0`. Full line: `2(x² + 2x + 1) − 2 + (y² − 6y + 9) − 9 + 7 = 0`.
> On {collect}: `−2 − 9 + 7 = −4` in GOLD; on {move} the 4 crosses over and on {sq}: `2(x + 1)² + (y − 3)² = 4`. On {div}: `(x + 1)²/2 + (y − 3)²/4 = 1`. On {tuck}: `((x + 1)/√2)² + ((y − 3)/2)² = 1`, the `√2` and `2` sliding inside the brackets.
> On {read}: s4's `((x − x₀)/a)² + ((y − y₀)/b)² = 1` slides in under it, matched term by term. Then the lecturer's read-off, one line per cue: {centre} `x₀ = −1, y₀ = 3   (centre)` in YELLOW; {a} and {minor} `a = √2   semi-minor axis   in x-direction` in GREEN; {b} `b = 2   semi-major axis   in y-direction` in GOLD.
> On {sketch}: axes; YELLOW centre `(−1, 3)` with dashed lines to the axes; on {updown} GOLD arms up and down by 2 (y = 1 to 5); on {side} GREEN arms left and right by √2 ≈ 1.41 (x ≈ −2.41 to 0.41); the tall BLUE ellipse draws through those four points. On {cross}: flash where its right side crosses the why axis (it meets x = 0 at y = 3 ± √2, about 1.59 and 4.41). Keep this ellipse: it returns in s7, s8 and ch6 s5.
> Checked with sympy 1.14: each line equals the original (the last two after multiplying by 4); the constants sum to −4 (the transcript's "7 minus 11" at 41:57 is a slip); the wrong `− 1` leaves the equation off by 1; the four extreme points satisfy it.

[c5.example.1] {back} Now back to the equation from the start. It's Example thirty-six in the notes. {task} Find the centre of the ellipse, and its semi-major and semi-minor axes. {method} The method is the one you used for the circle, completing the square. {first} But first, deal with the two in front of ex squared. {factor} Take it out of both ex terms, so two ex squared plus four ex becomes two, times ex squared plus two ex.

[c5.example.2] {inside} Inside the bracket, half of two is one, and its square is one, so add one. {slip} Here's the step where people slip. {pause} {times} That one sits inside a bracket that gets multiplied by two, so you've really added two. {sub} Two is what you must take away, not one. {yterms} The why terms are simpler. Half of minus six is minus three, so add its square, nine, and take nine away.

[c5.example.3] {collect} Now gather the loose numbers, minus two, minus nine, plus seven, which makes minus four. {move} Move it across as plus four. {sq} So two, times the square of ex plus one, plus the square of why minus three, equals four. {div} Divide everything by four, to get a one on the right. {tuck} Then write each divisor as a square. Two is root two, squared, and four is two squared.

[c5.example.4] {read} Now it matches the ellipse equation, and you can read everything off. {centre} The centre is at minus one, three, with the signs flipped, as for the circle. {a} Along ex, the semi-axis is root two, about one point four one. {minor} That's the smaller one, so it's the semi-minor axis. {b} Along why, it's two, and that's the semi-major axis. {pause}

[c5.example.5] {sketch} To sketch it, mark the centre, at minus one, three. {updown} Go up and down by two, from why equals one to why equals five. {side} Go left and right by root two. {cross} That's more than the one unit to the why axis, so the ellipse pokes across it, to about ex equals zero point four one. {tall} So it's a tall ellipse that just crosses the why axis, as the lecturer pointed out.

## Scene 7 · Area and circumference (ch5_s7_area)

> On {circle}: a unit circle at the origin, BLUE and lightly filled, with a grid of small squares inside it; label `A = πr²`, and with r = 1, `π`.
> On {sx}: a GOLD arrow stretches it along x by a; the fill and every grid square widen. On {sy}: a GREEN arrow stretches it along y by b; they grow taller. On {formula}: the label edits to `A = πab`, tag `(101)`, boxed YELLOW with the notes' "area of an ellipse".
> On {ex36}: Example 36's tall ellipse from s6 returns, filled: `A = π · √2 · 2 = 2√2 π ≈ 8.9`.
> On {circ}: `Γ = 2πr` under a small circle. On {guess}, under the ellipse: `Γ = π(a + b)`. On {not}: the notes' "the circumference of an ellipse is **not** Γ = π(a + b)", the formula struck through in RED.
> On {flat} (an addition, not in the notes): an ellipse squashing nearly flat, semi-major 1 (GOLD), semi-minor shrinking towards 0 (GREEN). On {around}: a dot runs round it while a GOLD counter climbs to about 4 (across 2 and back 2). On {guessval}: beside it, RED `π(1 + 0) ≈ 3.14`.
> On {integrals}: the notes' words, small: "it needs 'elliptic integrals'".
> Checked numerically (mpmath quad, perimeter integral): a = 1, b = 0.001 gives 3.999 against π(a + b) = 3.145; for a circle the guess is exact (2πr); Example 36's true perimeter is 10.81 against π(√2 + 2) = 10.73. Area 2√2 π = 8.886 (sympy).

[c5.area.1] {area} One more fact, about area. {circle} A circle of radius one has area pi. {sx} Stretch it along ex by a factor of A, and every little piece of area gets wider by that factor. {sy} Stretch it along why by a factor of B, and every piece gets taller by that factor. {formula} So the area of the ellipse is pi, times A, times B. That's equation one hundred and one.

[c5.area.2] {ex36} For Example thirty-six, that's pi, times root two, times two, about eight point nine. {circ} But the distance round an ellipse is much harder. {guess} A circle's circumference is two pi R, so you might guess pi times the sum of the semi-major and semi-minor axes. {not} The notes say plainly that this is wrong. {pause}

[c5.area.3] {flat} To see why, squash an ellipse almost flat, with a semi-major axis of one, and a semi-minor axis of almost zero. {around} Going round it is nearly two units across and two units back, about four. {guessval} The guess gives only pi, about three point one four. {integrals} The true circumference needs elliptic integrals, which are beyond this year's course.

## Scene 8 · Recap (ch5_s8_recap)

> One small picture per sentence, each a miniature of the scene it comes from (same objects, colours and styling), with its short line under it, filling a grid as they arrive:
> {r1}: s3's E2 circle, YELLOW centre `(1, 0)` and `(x − 1)² + y² = 1` → "complete the square";
> {r2}: s3's shrinking sequence, BLUE circle → YELLOW point → RED ∅ → "the sign decides";
> {r3}: s4's wide ellipse with its GOLD semi-major and GREEN semi-minor braces → "a stretched circle";
> {r4}: s5's two running points on the circle and the ellipse, one θ dial → "cosine and sine draw both";
> {r5}: s6's tall ellipse at `(−1, 3)` beside the GREEN `− 2` from the slip → "factor, complete, divide"; {r6}: s7's filled ellipse with `A = πab` → "area πab".
> On {next}: the grid clears to the unit circle `x² + y² = 1`; the `+` turns YELLOW and flips to `−`, and on {hyper} the circle opens out into the TEAL hyperbola `x² − y² = 1` with its point `(cosh θ, sinh θ)`.
> End card held ~8 s after the last word; the music carries it.

[c5.recap.1] {recap} Time for a recap. {r1} To find the circle in an expanded equation, complete the square in ex and in why. {r2} The sign of what's left on the right decides between a circle, a single point, and nothing at all. {r3} An ellipse is a circle stretched by different amounts along the two axes, which become its semi-major and semi-minor axes. {r4} Cosine and sine draw both, with theta as a parameter.

[c5.recap.2] {r5} When a square has a number in front, as in Example thirty-six, factor it out, complete the squares, then divide. {r6} And an ellipse's area is pi, times A, times B. {pause} {next} Next time, the plus sign in the circle's equation flips to a minus. {hyper} Out comes a hyperbola, which finally explains why shine and cosh are called hyperbolic. {pause}
