# Chapter 3 · Graphs and inverses

NST IA Mathematics (Hyperbolic Functions and Conics), part 3 of 7. Source: Berloff, Mathematical Methods I notes, pp. 35–38 (§3.3 Figure 25 and properties 1–6; §3.4 (96), (97), Figure 26, Example 34); Lecture 11 recording 13:00–24:30.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

On-screen maths is given as LaTeX for `MathTex`. Every formula, number and check on screen was
verified with sympy 1.14.0 (system Python): the definitions, cosh − sinh = e^{−x}, the limits of
tanh, both quadratics and their roots, (96), (97) and Example 34 against sympy's asinh, acosh and
atanh, the root product 1, and the ln 2 checks (sinh = 3/4, cosh = 5/4, tanh = 3/5).
Colours as PLAN.md: hyperbolic curves and names TEAL, e^x / e^y / e^{2y} GOLD, e^{−x} / e^{−y}
PURPLE, attention and boxed results YELLOW, kept roots GREEN, rejected roots RED.

---

## Scene 1 · Hook (ch3_s1_hook)

> Title card (`title_card("Part 3 · Graphs and inverses")`): "Hyperbolic Functions and Conics", "NST IA Mathematics · Lecture 11", "Part 3 · Graphs and inverses".
> {last}: a small callback to ch2's sign flip: `\cos(A+B) = \cos A\cos B - \sin A\sin B` (BLUE) above `\cosh(A+B) = \cosh A\cosh B + \sinh A\sinh B` (TEAL), the flipped `+` YELLOW. It clears at {three}.
> {three}: the three definitions stack at centre-left, names TEAL, every e^x GOLD, every e^{−x} PURPLE, exactly as ch1 showed them: `\cosh x = \tfrac12\left(e^{x} + e^{-x}\right)`, `\sinh x = \tfrac12\left(e^{x} - e^{-x}\right)`, `\tanh x = \dfrac{e^{x} - e^{-x}}{e^{x} + e^{-x}}`. {gold} and {purple} flash the GOLD terms, then the PURPLE ones.
> {shape}: on the right, empty axes with a YELLOW "?" where a curve should be.
> {back}: under the axes, `x \longrightarrow \sinh x`, then a reverse arrow from `\sinh x` back to a YELLOW "?" ("which x?").
> {teaser}: that "?" is swapped for `\ln`, YELLOW. Hold on the three formulas, the empty axes and the `\ln`.

[c3.hook.1] {title} Welcome back. This is part three: graphs and inverses. {last} Last time, every trig identity got a hyperbolic twin, with a sign flip wherever two shines multiply.

[c3.hook.2] {three} So far, cosh, shine and tanch are just formulas, built from the same two exponentials. {gold} Gold for E to the ex, {purple} and purple for E to the minus ex. {shape} But what do they look like, as graphs? {pause} {back} And can you run them backwards? Given the value of shine, can you find the ex that produced it? {pause}

[c3.hook.3] {plan} We'll sketch all three, using nothing but the two exponentials. {undo} Then we'll undo them, one by one. {teaser} And all three answers will turn out to be logarithms. {pause}

## Scene 2 · The shape of cosh (ch3_s2_cosh)

> Hero: ch1 s2's averaging picture, same axes, colours and styling (the series' graph style: x from about −2.5 to 2.5, y from about −3 to 5, curves clipped at the frame), filling most of the frame. `e^{x}` solid GOLD, `e^{-x}` solid PURPLE, `\cosh x` TEAL running through their midpoints.
> {halves}: each exponential squashes to half height and turns dashed: `\tfrac12 e^{x}` (GOLD dashed), `\tfrac12 e^{-x}` (PURPLE dashed); the solid ones fade. {sum}: the formula `\cosh x = \tfrac12 e^{x} + \tfrac12 e^{-x}` at the top, colour-coded, and at three or four x positions a PURPLE bar stacked on a GOLD bar reaches exactly the TEAL curve.
> {zero}: YELLOW dot at (0, 1) with `\cosh 0 = \dfrac{1 + 1}{2} = 1` (property 1).
> {mirror}: the two dashed curves swap by reflection in the y-axis (GOLD onto PURPLE and back); the TEAL curve stays put. {even}: `\cosh(-x) = \cosh x` (property 2), with a faint mirror line on the y-axis.
> {tiny}: a DIM vertical marker at x = 2 (ch1's "stand at" marker) with readouts `\tfrac12 e^{2} \approx 3.69` (GOLD) and `\tfrac12 e^{-2} \approx 0.068` (PURPLE). {hug}: the TEAL curve merges into the GOLD dashed curve on the right (property 3). {left}/{hugleft}: the mirror image, merging into the PURPLE dashed curve on the left (property 4).
> {floor}: a dashed YELLOW line at y = 1 touching the bottom of the U, `\cosh x \ge 1` (property 6). {why}: a side card `e^{-x} = \dfrac{1}{e^{x}}`; {recip}: `a + \dfrac{1}{a} \ge 2 \quad (a > 0)` with the example `2 + \tfrac12 = 2\tfrac12` underneath.
> {U}: the side card clears, the dot at (0, 1) pulses once; end on the full Figure 25(a): the TEAL U labelled `\cosh x`, both dashed halves still in place. Scene 3 reuses these axes and dashed curves (handover).

[c3.cosh.1] {pic} Here's the picture from part one. {gold} The gold curve is E to the ex, {purple} the purple one is E to the minus ex, {avg} and the teal one, cosh, runs exactly halfway between them. {halves} Now split that average into two parts: half of E to the ex, and half of E to the minus ex, {dashed} both drawn dashed. {sum} Cosh is simply their sum.

[c3.cosh.2] {zero} Start at ex equals zero. Both exponentials equal one there, so cosh of zero is one plus one, over two, which is one. {mirror} Next, replace ex with minus ex. The two dashed curves swap places, and their sum stays the same. {even} So cosh of minus ex equals cosh of ex. The graph is its own mirror image, across the why axis. {pause}

[c3.cosh.3] {right} Now go far to the right. {tiny} At ex equals two, half of E to the ex is about three point seven, and half of E to the minus ex is less than a tenth. {hug} The small one hardly counts, so cosh hugs the gold dashed curve. {left} Far to the left, the roles swap, {hugleft} and cosh hugs the purple one instead.

[c3.cosh.4] {floor} In fact, cosh of ex is at least one, for every real ex. {why} Here's why. E to the minus ex is one over E to the ex. {recip} And a positive number plus its reciprocal is always at least two. Two plus a half, for example, is two and a half. {pause} {U} So their average, cosh, is at least one, and it equals one only at zero. Cosh is a U, climbing exponentially on both sides.

## Scene 3 · sinh, tanh, and all three together (ch3_s3_sinh_tanh)

> Opens on scene 2's picture and axes (Figure 25(b) in the series' graph style); cosh dims to 0.3 but stays.
> {sinh}: `\sinh x = \tfrac12 e^{x} - \tfrac12 e^{-x}` replaces the cosh formula at the top. The PURPLE dashed curve flips below the x-axis to become `-\tfrac12 e^{-x}`; the GOLD dashed `\tfrac12 e^{x}` stays. The sinh curve draws in, in ch1's lighter TEAL. {zero}: dot at the origin, `\sinh 0 = \dfrac{1 - 1}{2} = 0`. {antisym}: the curve spins half a turn about the origin and lands on itself; `\sinh(-x) = -\sinh x` (property 2).
> {right}: sinh merges into the GOLD dashed curve, the same one as cosh (property 3). {left}/{flip}: on the left it merges into the flipped PURPLE curve; a ghost copy of the dimmed cosh reflects in the x-axis there and lies on top of it (property 4).
> {gap}: cosh returns to full; three or four PURPLE vertical segments between cosh above and sinh below, shrinking to the right, labelled `\cosh x - \sinh x = e^{-x} > 0`.
> {tanh}: clear to new axes, x from −3 to 3, y from −1.2 to 1.2 (Figure 25(c)). `\tanh x = \dfrac{\sinh x}{\cosh x} = \dfrac{e^{x} - e^{-x}}{e^{x} + e^{-x}}`; a YELLOW box slides from the top ({top}) to the bottom ({bottom}). {zero}/{odd}: the TEAL tanh curve draws through the origin; `\tanh(-x) = -\tanh x`.
> {bigx}: the e^{−x} terms dim to 0.25, leaving `\dfrac{e^{x}}{e^{x}} = 1`; a GOLD dashed line at y = 1. {negx}: the e^{x} terms dim instead, `\dfrac{-e^{-x}}{e^{-x}} = -1`; a PURPLE dashed line at y = −1 (the notes' Figure 25(c) dashes, recoloured). {band}: `-1 < \tanh x < 1` (property 6), the band between the dashes faintly shaded.
> {all}: Figure 25(d), back on the series' axes from scene 2: cosh, sinh and tanh in three shades of TEAL (cosh and sinh as in ch1, tanh a third shade), each labelled at its right end (`\cosh x`, `\sinh x`, `\tanh x`); each brightens on its own mark ({cosh}, {sinh}, {tanh}). {slope}: a YELLOW dashed line y = x through the origin; sinh and tanh both hug it near 0. Scene 4 opens on this picture.

[c3.odd.1] {sinh} Shine is made of the same two dashed curves, with a minus sign between them. {zero} At zero, that's one minus one, over two, so shine of zero is zero. {swap} Replace ex with minus ex, and the two curves swap again, but this time the swap flips the sign. {antisym} So shine of minus ex is minus shine of ex. Spin the graph half a turn about the origin, and it lands on itself.

[c3.odd.2] {right} Far to the right, the small half fades again, and shine hugs the same gold curve as cosh. {left} Far to the left, the purple half takes over, with a minus sign, {flip} so shine hugs the purple curve turned upside down. Out there, it looks like cosh reflected in the ex axis. {gap} And shine always stays below cosh, because cosh minus shine is exactly E to the minus ex, which is positive.

[c3.odd.3] {tanh} Now tanch, which is shine divided by cosh. {top} In exponentials, the top is the difference of E to the ex and E to the minus ex, {bottom} and the bottom is their sum. {zero} At zero, the top is zero, so tanch of zero is zero. {odd} And tanch is odd, like shine, because it's an odd function divided by an even one.

[c3.odd.4] {bigx} For large positive ex, drop E to the minus ex, top and bottom. {one} What's left is E to the ex over E to the ex, which is one. {negx} For large negative ex, drop E to the ex instead, and you get minus one. {band} The top is always smaller in size than the bottom, so tanch stays strictly between minus one and one, for every real ex. {pause}

[c3.odd.5] {all} Here are all three on one set of axes. {cosh} Cosh, the U, at least one. {sinh} Shine, climbing all the way up through the origin, always under cosh. {tanh} And tanch, squeezed between minus one and one. {slope} Notice that near zero, shine and tanch both look like the line why equals ex. Keep that in mind. {pause}

## Scene 4 · Undoing sinh (ch3_s4_arsinh)

> {undo}/{line}: scene 3's Figure 25(d) picture. A YELLOW horizontal line sweeps up and down: on sinh it always meets one point (one YELLOW dot). {tanh}: on tanh, one point (for heights between −1 and 1). {cosh}: above height 1 it meets cosh twice, two dots, the pair ringed in RED. Clear, keeping a small sinh graph in a corner.
> {def}: the derivation builds down the centre, each line derived from the one above (`derive`), e^y and e^{2y} GOLD, e^{−y} PURPLE: `y = \sinh^{-1} x \iff \sinh y = x`. {minus}: a small RED aside `\sinh^{-1} x \ne \dfrac{1}{\sinh x}` (ch1's warning), which fades after the sentence.
> {expo}: `\tfrac12\left(e^{y} - e^{-y}\right) = x` with `\times\, 2e^{y}` in the right margin, as in the notes ({times}). {square}/{one}: `e^{y}\cdot e^{y} = e^{2y}` and `e^{y}\cdot e^{-y} = 1` as brief side notes, then the next line `e^{2y} - 2x\,e^{y} - 1 = 0`. {quad}: it is rewritten `\left(e^{y}\right)^2 - 2x\left(e^{y}\right) - 1 = 0`, both `e^{y}` boxed YELLOW, label "a quadratic in e^y".
> {formula}: `e^{y} = x \pm \sqrt{x^2 + 1}`. {pos}: `e^{y} > 0`. {bigger}: `\sqrt{x^2 + 1} > |x|`. {neg}/{reject}: the minus root `x - \sqrt{x^2 + 1}` turns RED, `< 0`, and is struck out; the plus root turns GREEN.
> {result}: `y = \sinh^{-1} x = \ln\left(x + \sqrt{x^2 + 1}\right)` boxed YELLOW, tagged "(96)"; {every}: "every real x" under it. The chain above shrinks and dims to make room.
> {check}: a side card for x = ¾: `\sqrt{\tfrac{9}{16} + 1} = \tfrac54`, roots `\tfrac34 + \tfrac54 = 2` (GREEN) and `\tfrac34 - \tfrac54 = -\tfrac12` (RED, struck), so `y = \ln 2`; {verify}: `\sinh(\ln 2) = \dfrac{2 - \frac12}{2} = \tfrac34` with a GREEN tick. Keep this card: scene 5 and scene 6 bring it back.
> {graph}: equal-unit axes (x and y from −4 to 4, so the reflection is a true mirror), sinh TEAL, a dashed line y = x. {mirror}: a copy of sinh flips across the line into `\sinh^{-1} x` (TEAL, lighter), through the origin with slope 1, then flattening like a log. {names}: a small DIM note `\sinh^{-1} x = \operatorname{arsinh} x` ("other books"). This graph returns in ch7 (G3).

[c3.arsinh.1] {undo} To undo a function, each output must come from exactly one input. {line} Slide a horizontal line up the graph of shine, and it meets the curve exactly once, at every height. {mono} Shine only ever increases, because E to the ex grows while E to the minus ex shrinks. {tanh} Tanch always increases too. {cosh} But above height one, the line meets cosh twice. {pause} So cosh gets the next scene to itself.

[c3.arsinh.2] {def} So, inverse shine of ex is the number, why, whose shine is ex. {minus} As in part one, that minus one means the inverse function, which is different from one over shine. {expo} Write shine of why in exponentials, set it equal to ex, {times} and multiply both sides by two, E to the why. {square} E to the why, times E to the why, is E to the two why, {one} and E to the why, times E to the minus why, is just one. {quad} So you get a quadratic, and its unknown is E to the why. {pause}

[c3.arsinh.3] {formula} The quadratic formula gives two roots. E to the why equals ex, plus or minus the square root of ex squared plus one. {pos} But E to the why is positive. {bigger} And that square root is always bigger than ex, whether ex is positive or negative, {neg} so ex minus the square root is negative. {reject} That root is impossible, and we reject it. {pause}

[c3.arsinh.4] {keep} That leaves E to the why equals ex plus the square root. Take logs, {result} and inverse shine of ex is the log of, ex plus the square root of ex squared plus one. {every} The input to that log is always positive, so inverse shine works for every real ex. {pause}

[c3.arsinh.5] {check} Let's test it with ex equals three quarters. The square root is five quarters, so the roots are two, and minus a half. {verify} Rejecting minus a half leaves log two. And shine of log two is two, minus a half, all over two, which is three quarters. {pause}

[c3.arsinh.6] {graph} On a graph, undoing a function means reflecting it in the line why equals ex. {mirror} Inverse shine passes through the origin with slope one, then grows slowly, like a logarithm. {names} Other books call it by the name on screen. It's the same function.

## Scene 5 · Undoing cosh: two branches (ch3_s5_arcosh)

> {same}: the same layout as scene 4. Scene 4's chain sits small and DIM in a left column for comparison; the cosh chain builds at centre, each line derived from the one above: `y = \cosh^{-1} x \iff \cosh y = x`; {expo}: `\tfrac12\left(e^{y} + e^{-y}\right) = x`, `\times\, 2e^{y}` in the margin ({times}); {quad}: `e^{2y} - 2x\,e^{y} + 1 = 0`. {sign}: its `+1` and scene 4's `-1` both flash YELLOW.
> {roots}: `e^{y} = x \pm \sqrt{x^2 - 1}`, with `x \ge 1` beside it. {test}: a YELLOW "?" over the minus root.
> {try}/{nums}: a side card in scene 4's check-card style, for x = 5/4: `\sqrt{\tfrac{25}{16} - 1} = \tfrac34`, roots `\tfrac54 + \tfrac34 = 2` and `\tfrac54 - \tfrac34 = \tfrac12`. {both}: both GREEN, no strike-out this time. {general}: both roots in the main chain turn GREEN.
> {two}: `y = \ln 2` or `y = \ln\tfrac12`, and on the card `\cosh(\ln 2) = \dfrac{2 + \frac12}{2} = \tfrac54` with a GREEN tick (scene 6 brings this card back). {product}: `2 \times \tfrac12 = 1` (YELLOW), then {square} the general line `\left(x - \sqrt{x^2 - 1}\right)\left(x + \sqrt{x^2 - 1}\right) = x^2 - \left(x^2 - 1\right) = 1`.
> {recip}: `x - \sqrt{x^2 - 1} = \dfrac{1}{x + \sqrt{x^2 - 1}}`; {neglog}: `\ln\left(x - \sqrt{x^2 - 1}\right) = -\ln\left(x + \sqrt{x^2 - 1}\right)`; {pm}: `y = \pm\ln\left(x + \sqrt{x^2 - 1}\right)`. {sym}: `\cosh(-y) = \cosh y`, with a quick mirror flash on the dimmed cosh U.
> {pick}/{result}: `y = \cosh^{-1} x = \ln\left(x + \sqrt{x^2 - 1}\right)` boxed YELLOW, tagged "(97)". {domain}: `x \ge 1`, with a small cosh U whose region below y = 1 is shaded RED ("no real x has cosh x < 1").
> {fig}: Figure 26, two panels on equal-unit axes. Left: `\cosh x` (TEAL), x from −3 to 3. {reflect}: a copy flips across a dashed y = x into the right panel: a sideways U starting at (1, 0) and opening to the right (x from 0 to 10, y from −3 to 3). {upper}: the upper branch TEAL, labelled `\ln\left(x + \sqrt{x^2 - 1}\right)`; {lower}: the lower branch PURPLE, labelled `-\ln\left(x + \sqrt{x^2 - 1}\right)` (the lecturer's labels).
> {keep}: the upper branch glows briefly (the principal value); the lower stays fully visible. End on both branches: ch4 s5 reuses this picture.

[c3.arcosh.1] {same} Now cosh, with the same plan. {expo} Write cosh of why in exponentials, set it equal to ex, {times} and multiply by two, E to the why. {quad} You get the same kind of quadratic, {sign} except for the last sign: plus one, where shine had minus one. {roots} So the roots are ex, plus or minus the square root of ex squared minus one.

[c3.arcosh.2] {test} So which root do we reject this time? {pause} {try} Try ex equals five quarters. {nums} The square root is three quarters, so the roots are two, and one half. {both} Both are positive. {pause} {general} In fact, for any ex at least one, ex is bigger than that square root, so both roots are positive. This time, we reject neither.

[c3.arcosh.3] {two} So the unknown, why, can be log two, or log of a half. {product} And notice that two times a half is one. {square} That's always true. By the difference of two squares, the product of the roots is ex squared, take away ex squared minus one, which is one.

[c3.arcosh.4] {recip} So the smaller root is one over the larger, {neglog} and its log is minus the log of the larger. {pm} The two answers are plus and minus the same log. {sym} That's because cosh is even. A number and its negative have the same cosh.

[c3.arcosh.5] {pick} A function needs one output, so we take the non-negative one. {result} Inverse cosh of ex is the log of, ex plus the square root of ex squared minus one. {domain} It needs ex at least one, which makes sense, because every real number has a cosh of at least one. {pause}

[c3.arcosh.6] {fig} Here's cosh again. {reflect} Reflect it in the line why equals ex, and you get a sideways U, starting at one on the ex axis. {upper} Its upper branch is plus the log, {lower} and its lower branch is minus the log. {keep} Inverse cosh means the upper one, but keep the lower one in view. In the next part, we'll need both.

## Scene 6 · Example 34: undoing tanh (ch3_s6_artanh)

> {last}: heading "Example 34" (YELLOW) with the notes' title "Identity for inverse hyperbolic tangent" in DIM. The chain builds down the centre, each line derived from the one above, e^y and e^{2y} GOLD, e^{−y} PURPLE:
> {write}: `x = \tanh y = \dfrac{e^{y} - e^{-y}}{e^{y} + e^{-y}}`; {through}: `x\left(e^{y} + e^{-y}\right) = e^{y} - e^{-y}`; {ey}: `x\left(e^{2y} + 1\right) = e^{2y} - 1` with `\times\, e^{y}` in the margin. {nosq}: each `e^{2y}` flashes GOLD and each plain number YELLOW: no `e^{y}` term is left, so no quadratic.
> {collect}: `(1 - x)\,e^{2y} = 1 + x`; {divide}: `e^{2y} = \dfrac{1 + x}{1 - x}`; {log}/{result}: `y = \tanh^{-1} x = \tfrac12 \ln\left[\dfrac{1 + x}{1 - x}\right], \quad |x| < 1`, boxed YELLOW (square brackets as in the notes).
> {domain}: a number line from −1.5 to 1.5 with open circles at −1 and 1 and the stretch between them GREEN. {fits}: scene 3's tanh band (dashed GOLD y = 1, PURPLE y = −1) appears small beside it, its band lined up with the GREEN stretch.
> {check}: a check card in scene 4's style, for x = 3/5: `\dfrac{1 + \frac35}{1 - \frac35} = 4`, {ln2} `\tfrac12 \ln 4 = \ln 2`. {again}: scene 4's and scene 5's check cards return small beside it (`\sinh(\ln 2) = \tfrac34`, `\cosh(\ln 2) = \tfrac54`), and their two values fly into `\tanh(\ln 2) = \dfrac{3/4}{5/4} = \tfrac35`, GREEN tick.
> {graph}: equal-unit axes, tanh TEAL with its dashed GOLD y = 1 and PURPLE y = −1, a dashed y = x. A copy flips across y = x into `\tanh^{-1} x` (TEAL, lighter); {asym}: the two horizontal dashed lines turn with it into vertical ones at x = 1 (GOLD) and x = −1 (PURPLE), and the curve shoots up and down beside them. {near}: a YELLOW dashed y = x; tanh and its inverse both hug it near 0. This pair returns in ch7 (G3, G4).
> {logs}: the three boxed results line up, (96), (97) and Example 34, each `\ln` flashing YELLOW in turn: "the inverses are logarithms".

[c3.artanh.1] {last} Last, tanch. Its inverse is Example thirty-four in the notes. {write} Write ex equals tanch of why, as a fraction of exponentials, {through} and multiply through by the bottom. {ey} Then multiply both sides by E to the why. {nosq} Now every term is either E to the two why, or a plain number, so this time there's no quadratic at all.

[c3.artanh.2] {collect} Gather the E to the two why terms on the left. You get one minus ex, times E to the two why, equals one plus ex. {divide} Divide, and E to the two why is one plus ex, over one minus ex. {log} Take logs, and divide by two. {result} Inverse tanch of ex is half the log of the ratio, one plus ex, over one minus ex. {pause}

[c3.artanh.3] {domain} That ratio must be positive, so ex has to lie strictly between minus one and one, {fits} which is exactly the range of tanch. {check} Test it with ex equals three fifths. One plus three fifths, over one minus three fifths, is four, {ln2} and half the log of four is log two. {again} The same log two as before: tanch of log two is shine over cosh, three quarters over five quarters, which is three fifths. {pause}

[c3.artanh.4] {graph} Now reflect the graph of tanch in the line why equals ex. {asym} Its flat asymptotes at minus one and one turn into upright ones, so inverse tanch shoots up near one, and down near minus one. {near} And near zero, it's almost the line why equals ex, just as tanch was. {pause} {logs} So all three inverses came out as logarithms. That's the main conclusion of this whole section.

## Scene 7 · Recap (ch3_s7_recap)

> A grid of small callbacks, each built on its sentence's mark with its short line under it (same objects, colours and styling as where they were taught):
> {r1}: scene 2's Figure 25(a): TEAL U over its GOLD and PURPLE dashed halves, the YELLOW dot at (0, 1). Line: "cosh x ≥ 1, hugs ½e^x". {r2}: scene 3's Figure 25(d), the three TEAL curves, the tanh band between dashed ±1. Line: "sinh, tanh odd, increasing; −1 < tanh x < 1".
> {r3}: scene 4's boxed quadratic `\left(e^{y}\right)^2 - 2x\left(e^{y}\right) - 1 = 0`. Line: "a quadratic in e^y".
> {r4}: scene 4's sinh / sinh⁻¹ mirror pair with the dashed y = x; under it `\sinh^{-1} x = \ln\left(x + \sqrt{x^2 + 1}\right)`. {r5}: scene 5's Figure 26, upper branch TEAL, lower PURPLE; under it `\cosh^{-1} x = \ln\left(x + \sqrt{x^2 - 1}\right)` and the line "cosh⁻¹: plus or minus; keep the plus". {r6}: scene 6's tanh / tanh⁻¹ pair with its asymptotes; under it `\tanh^{-1} x = \tfrac12 \ln\left[\dfrac{1 + x}{1 - x}\right]`.
> {r7}: the three `\ln` glow YELLOW together. Line: "all three inverses are logs".
> {next}: the grid clears to ch4 s1's opening shot: a BLUE cosine wave trapped between −1 and 1 and a dashed YELLOW line y = 2 above it, with `\cos z = 2`. {cosh2}: `\pm\cosh^{-1} 2` (TEAL) appears beside it, and scene 5's two branches flash once in miniature.
> End card: hold ~8 s after the last word; the music carries it.

[c3.recap.1] {recap} Time for a recap. {r1} Cosh is a U, at least one, hugging half of E to the ex on the right. {r2} Shine and tanch are odd and always increasing, and tanch is trapped between minus one and one. {r3} To undo them, multiply by E to the why, find the exponential, then take logs.

[c3.recap.2] {r4} Inverse shine is the log of, ex plus the square root of ex squared plus one, for every ex. {r5} Inverse cosh has two branches, plus or minus a log, and we keep the plus. {r6} Inverse tanch is half the log of a ratio, for ex between minus one and one. {r7} All three inverses are logarithms. {pause}

[c3.recap.3] {next} Next time, we find every zed whose cosine is two. No real number has a cosine that big. {cosh2} But complex numbers do, and every one of them comes from inverse cosh of two, with both of its branches. {pause=1.5}
