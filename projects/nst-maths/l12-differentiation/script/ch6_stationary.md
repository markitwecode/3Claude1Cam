# Chapter 6 · Stationary points

NST IA Mathematics (Differentiation), part 6 of 7. Source: Berloff, Mathematical Methods I notes, p. 60 ((113)) and pp. 63–66 (§4.10: the stationary-point figure, the classification, y = x³ and y = x⁴ with Figure 30, rising and falling points of inflection, the three unlabelled graphs); Lecture 12 recording 32:44–33:50, 47:27–53:17, and the student question at 54:57–55:20; frames 48:10, 49:05 and 52:40 (the lecturer's labels on the three graphs).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

On-screen maths is given as LaTeX for `MathTex`. Every formula, derivative and number on screen was
checked with sympy 1.14.0 (system Python 3.11): the x³ and x⁴ derivative chains and their values at 0;
−x⁴'s fourth derivative −24; y = x³ − 3x (y′ = 3(x − 1)(x + 1), stationary at ±1, y(−1) = 2, y(1) = −2,
y″ = 6x, y″(±1) = ±6, y′(0) = −3); the three inflection graphs y = x³ + x, x³, x³ − 3x (y′(0) = 1, 0, −3;
y″ = 6x for all three, negative left of 0 and positive right of it; y‴(0) = 6); y = x⁴ + x (y′(0) = 1,
y″ = 12x², no sign change); the leading Taylor term (δx)ⁿ y⁽ⁿ⁾/n! against the exact change for x³, x⁴ and
−x⁴ (24/4! = 6/3! = 1); every derivative of e^{−1/x²} tends to 0 at 0 (orders 0 to 4 checked); and the
suggested polynomial for the notes' figure (scene 1). Colours as PLAN.md: curves BLUE, tangent lines,
slopes and slope readouts GREEN, stationary points and boxed results YELLOW, increments δx TEAL,
the rejected "inflection" RED.

---

## Scene 1 · Hook (ch6_s1_hook)

> {title}: title card (`title_card("Part 6 · Stationary points")`): "Differentiation", "NST IA Mathematics · Lecture 12", "Part 6 · Stationary points".
> {last}: a small callback to part five's result (owners ch5_s5_assemble for the box, ch5_s2_define and ch5_s6_ladder for the ladder card): the boxed recursion `H_{n+1} = 2x\,H_n - 2n\,H_{n-1}` (YELLOW box) above a miniature of part five's ladder card (`H_0 = 1`, `H_1 = 2x`, `H_2 = 4x^2 - 2`). It clears at {figure}.
> {figure}: the hero, filling most of the frame: the notes' §4.10 figure (p63) redrawn in the series' style, one smooth BLUE curve on faint axes, no labels yet. Its shape: it rises from the left to a peak, falls to a valley, rises, levels off for a moment, then climbs off to the right, ending higher than the peak (scene 2 needs that). A curve with exactly these features: y′ = (x + 2)(x + ½)(x − 3/2)², i.e. y = x⁵/5 − x⁴/8 − 17x³/12 + 21x²/16 + 9x/4 on x from about −2.6 to 2.5, y scaled to fit (peak at x = −2, valley at −½, flat spot at 3/2, the bending switches at about −1.43, 0.31 and 3/2). No formula on screen.
> {peak}, {valley}, {bends}, {flat}: YELLOW dots arrive in turn: the peak; the valley; on {bends} the two points where the bending switches (one on the falling stretch, one on the rising stretch after the valley); the flat spot.
> {question}: a small YELLOW "?" beside each of the five dots; at the top, "How do derivatives tell these apart?".
> {derivs}: along the bottom, a GREEN row `y' \quad y'' \quad y''' \quad y^{(4)} \quad \cdots`. On {zero} `y'' = 0` flashes YELLOW; on {parity} the words "odd" and "even" appear under `y'''` and `y^{(4)}`. Scene 2 opens on this curve and its dots.

[c6.hook.1] {title} Welcome back. This is part six: stationary points. {last} Last time, Leibniz's formula turned the definition of the Hermeet polynomials into a recursion.

[c6.hook.2] {figure} Now, back to graphs. The last section of Chapter four that the lecture covered opens with this curve. {peak} It has a peak, {valley} a valley, {bends} two places where the bending switches direction, {flat} and one spot where the curve goes flat for a moment, then keeps on rising.

[c6.hook.3] {question} How can derivatives tell these five points apart? {pause} {derivs} Most of the answer is A-level. But two parts may be new: {zero} what to do when the second derivative is zero, {parity} and why the answer then comes down to odd or even. {pause}

## Scene 2 · The vocabulary (ch6_s2_vocab)

> Opens on scene 1's curve and five YELLOW dots; the "?"s and the derivative row clear.
> {stat}: at the top, `\text{stationary point:}\quad \dfrac{dy}{dx} = 0`. {flat}: short flat GREEN tangent lines appear at the peak, the valley and the flat spot. {velocity}: a small inset in a corner: a dot sliding along a track, slowing and stopping, with a readout `v = 0` when it stops; the inset clears at {three}, when those three dots pulse and the two bend dots dim.
> {local}: label "local maximum" at the peak. {higher}: a dashed YELLOW horizontal line from the peak across the frame; the curve's right end climbs above it. {min}: "local minimum" at the valley. {turning}: a brace or bracket groups those two, "turning points"; the dashed line clears.
> {up}: a small side panel: a cup-shaped BLUE arc with two or three GREEN tangent lines lying below it, labelled "concave up"; {upsign}: `y'' > 0` under it. {down}: a cap-shaped BLUE arc with GREEN tangent lines above it, "concave down"; {downsign}: `y'' < 0`.
> {strip}: the side panel clears. Under the main curve, a sign strip for y″ builds left to right: `-` `+` `-` `+` (the notes' curve is concave down, up, down, up), split by dashed vertical lines through the two bend dots and the flat spot.
> {inflect}: the three dots on the dashed lines glow; {sign}: each dashed line gets a tiny "− | +" or "+ | −" flip.
> {labels}: the notes' labels arrive in the notes' places and arrow style: {lmax} "local maximum", {lmin} "local minimum", {two} "point of inflection" with two arrows (to the two bend dots), {rising} "(rising) stationary point of inflection" at the flat spot. {spell}: a small DIM note in the notes' grey box: "The spellings ‘inflection’ and ‘inflexion’ are both acceptable and are used interchangeably." Keep the labelled figure and the sign strip: scene 6 and the recap bring them back.

[c6.vocab.1] {stat} First, the names. A stationary point is a point where the first derivative is zero, {flat} so the tangent line there is flat. {velocity} The name comes from motion: the derivative of position with respect to time is the velocity, and an object with zero velocity is stationary. {three} This curve has three stationary points: the peak, the valley, and the flat spot.

[c6.vocab.2] {local} The peak is a local maximum: the highest point nearby, {higher} even though the curve climbs higher further to the right. {min} And the valley is a local minimum, the lowest point nearby. {turning} Together, maxima and minima are called turning points.

[c6.vocab.3] {up} Next, how the curve bends. Where it bends upward, like a cup, it's concave up, {upsign} and the second derivative is positive. {down} Where it bends downward, like a cap, it's concave down, {downsign} and the second derivative is negative. {strip} Along this curve, the bending switches three times.

[c6.vocab.4] {inflect} A point where the concavity changes is a point of inflection. {sign} In other words, it's where the second derivative changes sign. {labels} So here are the notes' labels: {lmax} a local maximum, {lmin} a local minimum, {two} two points of inflection, {rising} and a rising stationary point of inflection. {spell} The notes accept two spellings: inflection with C T, or inflexion with an X.

## Scene 3 · The second-derivative test (ch6_s3_second)

> Fresh axes in the series' graph style, x from about −2.3 to 2.3, y from about −3 to 3. {curve}: `y = x^3 - 3x` draws in BLUE, its name at the top left. This curve returns in scene 6 (the falling point of inflection).
> {deriv}: `y' = 3x^2 - 3 = 3(x - 1)(x + 1)`, GREEN for y′. {dots}: YELLOW dots at (−1, 2) and (1, −2). {ask}: a YELLOW "?" over each dot.
> {roll}: a short GREEN tangent line slides along the curve through (1, −2), from about x = 0.4 to 1.6, with a GREEN slope readout riding on it (from y′ = 3x² − 3: about −2.5 at x = 0.4, 0 at x = 1, about 4.7 at x = 1.6). It pauses at {neg} (negative readout), {zero} (exactly 0, the line flat on the dot) and {pos} (positive readout).
> {incr}: beside the dot, a small row "slope: − → 0 → +" with an upward arrow, then `y'' > 0`.
> {converse}/{rule}: the notes' rule card at the top right: `\dfrac{d^2y}{dx^2} > 0 \;\Rightarrow\; \text{local minimum}`. {max}: the tangent line rolls through (−1, 2) with the readout going +, 0, − and a downward arrow, and the card's second line: `\dfrac{d^2y}{dx^2} < 0 \;\Rightarrow\; \text{local maximum}`.
> {check}: `y'' = 6x`; `y''(1) = 6 > 0` beside the lower dot, labelled "minimum", its "?" gone. {minus}: `y''(-1) = -6 < 0` beside the upper dot, "maximum", its "?" gone.
> {umbrella}: the graph slides aside. Two simple open umbrellas, drawn in BLUE, side by side. {bowl}: the left one upside down like a bowl, short light rain streaks falling into it and pooling, labelled `y'' > 0` and "minimum". {cap}: the right one held the usual way, rain running off its edges and dry underneath, labelled `y'' < 0` and "maximum". The recap brings back this pair.

[c6.second.1] {curve} Here's an example: why equals ex cubed minus three ex. {deriv} Its derivative is three ex squared minus three, which is zero at ex equals plus or minus one. {dots} So it has two stationary points. {ask} Without looking at the graph, which one is the maximum, and which is the minimum? {pause}

[c6.second.2] {roll} Watch the tangent line roll through the point at one. {neg} Just before it, the slope is negative. {zero} At the point, it's zero. {pos} Just after, it's positive. {incr} The gradient increases as it passes through, so its own derivative, the second derivative, is positive there. {pause}

[c6.second.3] {converse} Turn that around, and you get the test. {rule} If the second derivative is positive at a stationary point, the gradient is increasing as it passes zero, so the curve falls in and climbs out: a local minimum. {max} If the second derivative is negative, the gradient decreases through zero, and it's a local maximum. {check} Here, the second derivative is six times ex. That's six at ex equals one: a minimum. {minus} And it's minus six at ex equals minus one: a maximum.

[c6.second.4] {umbrella} As a memory aid, the lecturer uses an umbrella. {bowl} Turn it upside down, like a bowl, and it collects the rain: positive second derivative, a minimum. {cap} Hold it the usual way, and there's no rain underneath: negative second derivative, a maximum. {pause}

## Scene 4 · When the second derivative is zero (ch6_s4_higher)

> {pair}: Figure 30 (notes p65), two panels side by side in the series' graph style: {cube} left `y = x^3` (BLUE), x from −2 to 2, y from −8 to 8; {quart} right `y = x^4` (BLUE), x from −2 to 2, y from −1 to 16 (the notes' ranges). A YELLOW dot at the origin of each, with a short flat GREEN tangent line.
> {both}: under both, the notes' line `\dfrac{dy}{dx} = \dfrac{d^2y}{dx^2} = 0 \quad \text{at } x = 0`. {nothing}: scene 3's rule card returns small, with a YELLOW "?" over it. {shapes}: the x³ curve brightens on both sides of 0 (rising through), then the x⁴ curve's bottom (minimum).
> {chain}/{card}: under the left panel, part four's x³ derivative-chain card, same objects and styling (owner ch1_s3_cube, extended in ch4_s2_higher: BLUE x³, GREEN derivatives, arrows between): `x^3 \to 3x^2 \to 6x \to 6 \to 0`. {atzero}: a row of values at x = 0 slides in under it, `0 \quad 0 \quad 0 \quad 6` under x³, 3x², 6x and 6. {first}: the `6` ringed YELLOW, with the notes' line `\dfrac{d^3}{dx^3}\left(x^3\right) = 6 \neq 0`.
> {quartchain}: under the right panel, the matching card in the same style: `x^4 \to 4x^3 \to 12x^2 \to 24x \to 24`; values at 0: `0 \quad 0 \quad 0 \quad 0 \quad 24`. {fourth}: the `24` ringed YELLOW, with `\dfrac{d^3}{dx^3}\left(x^4\right) = 0` and `\dfrac{d^4}{dx^4}\left(x^4\right) = 24 > 0`.
> {rule}: the two cards shrink upward; the notes' rule builds at centre: "first non-zero derivative `\dfrac{d^ny}{dx^n}` at the stationary point:". {odd}: "n odd → point of inflection", the x³ panel lit; {gradient}: on the x³ graph, two GREEN tangent lines just left and right of 0, both tilted upward, `\dfrac{dy}{dx} = 3x^2 > 0 \text{ for } x \neq 0`. {even}: "n even and positive → local minimum", the x⁴ panel lit. {neg}: "n even and negative → local maximum". {flip}: the x⁴ graph flips upside down into `y = -x^4`, its card's last entry becoming `-24`, label "local maximum"; then it flips back. {two}: a small note under the rule: "n = 2: the second-derivative test".
> {subtle}: the panels clear to one: `y = e^{-1/x^2}` with `y(0) = 0` (BLUE curve, x from −3 to 3, y from 0 to 1; it hugs the axis near 0). {aside}: the formula top left. {flatflat}: `y^{(n)}(0) = 0 \text{ for every } n`; the rule card gets a YELLOW "?". {min}: a YELLOW dot at the origin, labelled "minimum", with `y > 0 \text{ for } x \neq 0`.

[c6.higher.1] {pair} But the second derivative can be zero at a stationary point. {cube} Here's why equals ex cubed, {quart} and why equals ex to the fourth. {both} At zero, both have zero first and second derivatives. {nothing} So the test tells us nothing. {shapes} Yet ex cubed keeps on rising through zero, while ex to the fourth has a minimum there. {pause}

[c6.higher.2] {chain} So keep differentiating. {card} Here's the chain for ex cubed from part four: three ex squared, six times ex, six, then zero. {atzero} At zero, the first two vanish, {first} so the first one that survives is the third: six. {quartchain} For ex to the fourth: four ex cubed, twelve ex squared, twenty-four ex, twenty-four. {fourth} At zero, the first one that survives is the fourth, and it's twenty-four, which is positive.

[c6.higher.3] {rule} Here's the general rule. Find the first derivative that's different from zero at the stationary point, and call its order N. {odd} If N is odd, it's a point of inflection, like ex cubed, {gradient} whose gradient is positive on both sides. {even} If N is even and that derivative is positive, it's a local minimum, like ex to the fourth. {neg} If N is even and it's negative, it's a local maximum, {flip} like minus ex to the fourth, whose fourth derivative is minus twenty-four. {two} The second-derivative test is just the case N equals two.

[c6.higher.4] {subtle} The lecturer added a warning: if every derivative is zero, it gets subtle. {aside} Here's an example: E to the minus one over ex squared, given the value zero at zero. {flatflat} Every derivative there is zero, so the rule is silent. {min} Yet zero is clearly a minimum, since the function is positive everywhere else. {pause}

## Scene 5 · Why odd and even? (ch6_s5_why)

> {question}: a quote card, white text: "Can I just ask where this odd and even will come from?" with "a student, after the lecture" in DIM; {answer}: under it, "With a Taylor expansion." with "the lecturer" in DIM (recording 54:57–55:18). It clears at {fig}.
> {fig}: part one's Figure 29 on the left, same objects, colours and styling as ch1 s2 (owner ch1_s2_chord: y = x³ for x from about 0 to 1.7, the point at x = 1, δx = 0.5 to start): the BLUE curve, the point at x, the second point at x + δx, TEAL `\delta x` and `\delta y`, the TEAL chord, the GREEN tangent line at x.
> {def}: on the right, `\dfrac{dy}{dx} \approx \dfrac{y(x + \delta x) - y(x)}{\delta x}` with "δx small, but not yet 0" in DIM. {rearrange}: `\times\, \delta x` in the margin. {eq}: `y(x + \delta x) \approx y(x) + \delta x\,\dfrac{dy}{dx}` tagged "(113)", boxed YELLOW.
> {tangent}: the right-hand side `y(x) + \delta x\,\dfrac{dy}{dx}` turns GREEN, and a GREEN dot marks where the tangent line meets the vertical at x + δx; the small gap between it and the curve is marked YELLOW. {shrink}: the second point slides in towards x; the gap shrinks much faster than δx (scale both readouts if needed).
> {taylor}: Figure 29 clears; (113) moves to centre and grows to the right, a preview of §6.3 of the notes: `y(x_0 + \delta x) = y(x_0) + \delta x\, y'(x_0)`, then {sq} `+ \dfrac{(\delta x)^2}{2!}\, y''(x_0)`, then {cube} `+ \dfrac{(\delta x)^3}{3!}\, y'''(x_0) + \cdots`, the label "Taylor series" above it. δx TEAL throughout.
> {stat}: a YELLOW dot on a flat GREEN tangent line appears small beside it ("stationary point at x₀"); {gone}: `y'(x_0) = 0` under its term and the whole `\delta x\, y'(x_0)` term greys out. {first}: the series is rewritten with the general term showing, `\cdots + \dfrac{(\delta x)^n}{n!}\, y^{(n)}(x_0) + \cdots`, and every term before it greys out. {small}: the terms after it dim to half ("higher powers of δx: tiny"). {lead}: the result, boxed YELLOW: `y(x_0 + \delta x) - y(x_0) \approx \dfrac{(\delta x)^n}{n!}\, y^{(n)}(x_0)`, its left side labelled "height above the flat tangent line".
> {panels}: three small panels in a row, each a flat GREEN tangent line through a YELLOW dot at the origin and a BLUE curve over δx from −1 to 1: `(\delta x)^2`, `(\delta x)^3`, `(\delta x)^4`. {even}: on the n = 2 and n = 4 panels, YELLOW "+" signs on both sides. {evenmin}: those curves sit above the GREEN line on both sides, "minimum"; {evenmax}: a ghost copy flips below the line on both sides, "maximum (negative y⁽ⁿ⁾)", then fades. {odd}: on the n = 3 panel, "−" on the left and "+" on the right. {cross}: the curve passes through the GREEN line, "point of inflection".
> {check}: under the n = 4 panel, `y = x^4:\quad \dfrac{24}{4!} = 1`, so the change is exactly `(\delta x)^4`; {cubecheck}: under the n = 3 panel, `y = x^3:\quad \dfrac{6}{3!} = 1`, so the change is `(\delta x)^3`. The recap brings back the three panels.

[c6.why.1] {question} But why should odd or even decide anything? {pause} A student asked exactly this after the lecture, {answer} and the lecturer's answer was short: with a Taylor expansion. Here's the idea behind it.

[c6.why.2] {fig} Start from part one's picture. {def} When delta ex is small, but not yet zero, the derivative is about equal to the rise over delta ex. {rearrange} Multiply by delta ex, {eq} and you get the notes' approximation: the value of why at ex plus delta ex is about its value at ex, plus delta ex times the derivative. {tangent} That's the height of the tangent line, {shrink} and as delta ex shrinks, its gap to the curve shrinks even faster.

[c6.why.3] {taylor} Chapter six of the notes adds more terms, in higher powers of delta ex: a Taylor series. {sq} Next comes delta ex squared over two factorial, times the second derivative, {cube} then delta ex cubed over three factorial, and so on. {stat} At a stationary point, {gone} the delta ex term is zero. {first} If the first derivative that's different from zero is the Nth, every term before it is zero too, {small} and the later ones are tiny when delta ex is small. {lead} So the change in why is about delta ex to the N, over N factorial, times the Nth derivative.

[c6.why.4] {panels} So everything hangs on the sign of delta ex to the N. {even} When N is even, it's positive on both sides of the point. {evenmin} The curve sits above its flat tangent line on both sides, a minimum, if the Nth derivative is positive, {evenmax} or below it on both sides, a maximum, if it's negative. {odd} When N is odd, delta ex to the N flips sign with delta ex, {cross} so the curve crosses its tangent line: a point of inflection. {pause}

[c6.why.5] {check} For ex to the fourth, twenty-four over four factorial is one, so the change is exactly delta ex to the fourth. {cubecheck} For ex cubed, it's delta ex cubed, negative on the left and positive on the right. {pause}

## Scene 6 · Inflections that aren't stationary (ch6_s6_nonstat)

> {back}: scene 2's labelled figure of the notes, with its y″ sign strip, full size.
> {plain}: the two plain points of inflection pulse YELLOW; {tilt}: tilted GREEN tangent lines appear at both (the first sloping down, the second up), against the flat ones at the three stationary points. {defn}: the two dashed lines of the sign strip through those points flash, with `y'' = 0`.
> {rising}: the notes' definitions at the side: "`y'' = 0` and changes sign, `\dfrac{dy}{dx} > 0`: rising point of inflection". {falling}: "`\dfrac{dy}{dx} < 0`: falling point of inflection". {figure}: small labels "falling" and "rising" by the two points. {stationary}: the label "(rising) stationary point of inflection" glows. {cubic}: scene 4's small x³ graph appears in a corner, "rising".
> {three}: clear to the board's three graphs (notes p66, labelled by hand by the lecturer, frame 52:40) in a row, in the notes' style: small axes, BLUE curves, each name above its graph: left `y = x^3 + x`, middle `y = x^3`, right `y = x^3 - 3x` drawn between its maximum and minimum (x from −1 to 1, the shape of the notes' right graph; scene 3's curve). A YELLOW dot at the origin of each.
> {left}: a GREEN tangent line of slope 1 through the origin (her board has it), labels `y'(0) = 1 \neq 0`, `y''(0) = 0`, "rising". {middle}: a flat GREEN tangent, `y'(0) = 0`, `y''(0) = 0`, `y'''(0) = 6 \neq 0`, "stationary", under her heading "point of inflection". {right}: a GREEN tangent line of slope −3 (on her board too), `y'(0) = -3 \neq 0`, `y''(0) = 0`, "falling".
> {same}: `y'' = 6x` once, under all three; on each curve, "concave down" over the left half and "concave up" over the right half.
> {trap}: clear to one panel: `y = x^4 + x` (BLUE), x from about −1.5 to 1.2, y from about −0.6 to 3.6. {quart}: at the origin a YELLOW dot and a GREEN tangent line of slope 1, with `y'(0) = 1`, `y''(0) = 0`. {looks}: a label "rising point of inflection?", the "?" YELLOW. {never}: `y'' = 12x^2 \geq 0`. {cup}: "concave up" on both sides of 0; the label is struck through in RED, "no inflection". {change}: boxed YELLOW: "point of inflection: `y''` changes sign".

[c6.nonstat.1] {back} Back to the notes' picture. {plain} Two of its points of inflection are not stationary. {tilt} The tangent line there is tilted, because the first derivative is not zero. {defn} The second derivative still changes sign there, as at any point of inflection.

[c6.nonstat.2] {rising} If the first derivative is positive there, it's a rising point of inflection. {falling} If it's negative, it's a falling point of inflection. {figure} On this curve, the first one is falling, and the second is rising. {stationary} Stationary points of inflection can be rising or falling too, {cubic} like ex cubed at zero, which is rising.

[c6.nonstat.3] {three} The lecturer ended with three graphs from the notes, labelled by hand. {left} Why equals ex cubed plus ex has slope one at zero: rising. {middle} Ex cubed has slope zero, second derivative zero, and third derivative six: stationary. {right} And ex cubed minus three ex, from earlier, has slope minus three: falling. {same} All three share the same second derivative, six times ex, so all three change from concave down to concave up at zero. {pause}

[c6.nonstat.4] {trap} One trap: a zero second derivative is not enough on its own. {quart} Take why equals ex to the fourth plus ex. At zero, the slope is one and the second derivative is zero, {looks} so it looks like a rising point of inflection. {never} But its second derivative is twelve ex squared, which is never negative. {cup} The curve is concave up on both sides: no inflection at all. {change} The second derivative has to change sign. {pause}

## Scene 7 · Recap (ch6_s7_recap)

> {recap}: a grid of small callbacks, each built on its sentence's mark with its short line under it (same objects, colours and styling as where they were taught):
> {r1}: scene 2's labelled figure of the notes, small, the three stationary dots YELLOW with flat GREEN tangent lines. Line: "stationary: y′ = 0".
> {r2}: scene 3's umbrella pair (the bowl with rain, the usual way up and dry). Line: "y″ > 0: minimum · y″ < 0: maximum".
> {r3}: scene 4's two chain cards with their values at 0, the `6` and the `24` ringed YELLOW, beside tiny x³ and x⁴ graphs. Line: "first non-zero derivative: odd → inflection; even → max or min".
> {r4}: scene 5's three panels, (δx)², (δx)³, (δx)⁴ with their YELLOW signs. Line: "why: Taylor, the change ≈ (δx)ⁿ y⁽ⁿ⁾/n!".
> {r5}: scene 6's row of three graphs with their GREEN tangent lines and "rising", "stationary", "falling". Line: "inflection: y″ changes sign".
> {next}: the grid clears to part seven's preview: four small cards labelled "H1", "H2", "H4", "I1" under the heading "Part 7 · Solutions", in the series' question-card style (set by ch3 s7: rounded rectangle, DIM border, YELLOW label), showing only their labels at this size. {lecture}: beside them, the notes' heading "4.11 Curve sketching" (p66) with two cards "H3" and "H5".
> End card: hold ~8 s after the last word; the music carries it.

[c6.recap.1] {recap} Time for a recap. {r1} A stationary point is where the first derivative is zero. {r2} If the second derivative there is positive, it's a minimum; if negative, a maximum. {r3} If it's zero, find the first derivative that's different from zero: odd order means a point of inflection, even order a maximum or a minimum. {r4} A Taylor series explains why: near the point, the change goes like delta ex to the N. {r5} And a point of inflection, flat or not, is where the second derivative changes sign. {pause}

[c6.recap.2] {next} Next time, in the bonus part seven: the worked solutions to this lecture's sheet questions, H one, H two, H four and eye one. Try them first. {lecture} After that, the next lecture puts all of this to work in curve sketching, with H three and H five. {pause=1.5}
