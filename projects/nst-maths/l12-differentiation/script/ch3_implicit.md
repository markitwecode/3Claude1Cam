# Chapter 3 · Implicit differentiation and inverse functions

NST IA Mathematics (Differentiation), part 3 of 7. Source: Berloff, Mathematical Methods I notes, p. 51 (ln via e^y) and pp. 56–58 (§4.6 (108)–(110), Example 40, Example 41 with its handwritten working, §4.7 (111)); Lecture 12 recording 09:54–10:44 and 19:32–31:35 (board frames 24:50, 26:40, 28:10, 29:30).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

On-screen maths is given as LaTeX for `MathTex`. Every formula, number and check on screen was
verified with sympy 1.14.0 (system Python 3.11): ln(ax) via e^y = ax gives 1/x; the circle's implicit
derivative −(x − 1)/y, both explicit branches ∓(x − 1)/√(9 − (x − 1)²), the roots −2 and 4, the
point (2.8, ±2.4) with slopes ∓3/4, the perpendicular check (product −1); Example 41's quotient step
(the middle line equals 1/(1 + x²)^{3/2}), cos y = 1/√(1 + x²), dy/dx = 1/(1 + x²) against sympy's own
derivative of asin(x/√(1 + x²)), and asin(x/√(1 + x²)) = atan x at five points; sec² y = 1 + tan² y;
the slopes 3 and ⅓ for x³ and its cube root at (1, 1) (part one's Figure 29 point); x³'s slope 0 at 0 and the cube root's infinite one; the
circle as x(y), dx/dy = 0 at y = 0; part four's tease, the tenth derivative of x²e^{−x} =
e^{−x}(x² − 20x + 90). There is no code in this chapter.
Colours as PLAN.md: the curve being differentiated BLUE (the circle, as L11's circles), the tangent line
and dy/dx GREEN, the increments δx, δy and the chord TEAL, e^y GOLD, the quotient's top BLUE and bottom
PURPLE (part two's role colours), attention and boxed results YELLOW, the kept sign GREEN, vertical
tangent lines, the rejected sign and dy/dx = 0 RED.

---

## Scene 1 · Hook (ch3_s1_hook)

> {title}: title card (`title_card("Part 3 · Implicit differentiation and inverse functions")`): "Differentiation", "NST IA Mathematics · Lecture 12", "Part 3 · Implicit differentiation and inverse functions".
> {last}: a small callback strip of part two's three rules in its role colours (first function BLUE, second PURPLE), labelled "chain rule", "product rule", "quotient rule", as part two boxed them: `\frac{d}{dx} f\big(u(x)\big) = \frac{df}{du}\,\frac{du}{dx}`, `\frac{d}{dx}(fg) = \frac{df}{dx}\,g + f\,\frac{dg}{dx}`, `\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{v\,\frac{du}{dx} - u\,\frac{dv}{dx}}{v^2}`. At {circle} the strip clears, except the chain rule, which shrinks to the top-right corner and stays.
> {circle}/{first}: left half: equal-unit axes (x from −3 to 5, y from −3.5 to 3.5) with the BLUE circle, centre (1, 0), radius 3 (scene 3 and the recap reuse it); `y^2 = 9 - (x - 1)^2` above it. {two}: a dashed vertical line at x = 2.8 meets the circle twice: two YELLOW dots, at (2.8, 2.4) and (2.8, −2.4).
> {second}: right half: `y = \sin^{-1}\!\left(\dfrac{x}{\sqrt{1 + x^2}}\right)`. {headon}: under it `\dfrac{dy}{dx} = \;?`, the "?" YELLOW.
> {question}: both halves stay; a YELLOW "?" pulses between them. {plan}: a `\dfrac{d}{dx}` drops in front of both sides of each equation, and the corner chain rule flashes.
> {preview}: two small icons along the bottom, lighting in turn with the sentence: a tag "Tripos 2006" with a `\pm` whose minus is RED; `\dfrac{dx}{dy} = \dfrac{1}{dy/dx}`, its fraction flipping over.

[c3.hook.1] {title} Welcome back. This is part three: implicit differentiation and inverse functions. {last} Last time, the chain, product and quotient rules all came out of the same limit.

[c3.hook.2] {circle} Here are two awkward cases. {first} The first is a circle, with the equation why squared equals nine, minus the square of ex minus one. {two} For most ex, there are two values of why, one above the other. {second} The second is the function why equals the inverse sine of the fraction ex, over the square root of one plus ex squared. {headon} Nobody wants to differentiate that head-on.

[c3.hook.3] {question} So how do you find the derivative of why, when it comes tangled up in an equation, or wrapped in an inverse? {pause} {plan} Differentiate both sides of the equation, and let the chain rule do the work. {preview} Along the way, a Tripos question sets a sign trap, and a derivative gets turned upside down.

## Scene 2 · Differentiate both sides (ch3_s2_implicit)

> {explicit}: `y = f(x)` at the top-left, then it dims. {implicit}: centre: `g(y) = h(x)` tagged "(108)" (notes p56), braces under the two sides: "a function of y", "a function of x".
> {invert}: an arrow to `y = g^{-1}\big(h(x)\big)`; {but}: it greys out under a RED "not always possible".
> {instead}: `\dfrac{d}{dx}` in front of both sides. {remember}: the y inside g becomes `y(x)`, YELLOW. {right}: the right side becomes `\dfrac{dh}{dx}`. {left}/{chain}: `\dfrac{d}{dx}\,g\big(y(x)\big) = \dfrac{dg}{dy}\,\dfrac{dy}{dx}` builds out of the left side (TransformFromCopy), `\dfrac{dy}{dx}` GREEN; the line settles as `\dfrac{dg}{dy}\,\dfrac{dy}{dx} = \dfrac{dh}{dx}`, tagged "(109)".
> {rearrange}/{eq110}: `\dfrac{dy}{dx} = \dfrac{dh}{dx}\bigg/\dfrac{dg}{dy}` (the notes' slash form) tagged "(110)", boxed YELLOW, dy/dx GREEN. {cond}: `\dfrac{dg}{dy} \neq 0` under the box, the denominator flashing.
> {inverse}: a small side graph of g against y (BLUE). Near a point where its slope is non-zero, a horizontal line meets it once (GREEN dot); at a turning point, where the slope is zero, a nearby horizontal line meets it twice (two RED dots): there g has no single inverse. {consistent}: the GREEN dot and the `\neq 0` pulse together.
> {ln}: clear to the example: the notes' p51 chain, verbatim, one step per mark, e^y GOLD, dy/dx GREEN. {lnx}: `y = \ln ax`, with a small label "a: a constant"; {exp}: `\Rightarrow e^{y} = ax`; {lhs}/{rhs}: `\Rightarrow \dfrac{d}{dx}e^{y} = e^{y}\dfrac{dy}{dx} = \dfrac{d}{dx}(ax) = a`; {result}: `\Rightarrow \dfrac{dy}{dx} = \dfrac{a}{e^{y}} = \dfrac{a}{ax}`; {cancel}: the two a's strike out in YELLOW and `= \dfrac{1}{x}` arrives, boxed YELLOW, tagged "part two's promise".

[c3.implicit.1] {explicit} So far, every function came as why equals a formula in ex. {implicit} But often you get an equation instead, with a function of why on the left, and a function of ex on the right. {invert} One option is to undo the left-hand function, and get why on its own. {but} But that's not always possible, or practical.

[c3.implicit.2] {instead} Instead, differentiate both sides with respect to ex, {remember} remembering that why depends on ex. {right} The right-hand side is routine. {left} On the left, the function has why inside it, so the chain rule from part two applies. {chain} You get the derivative of the function with respect to why, times the derivative of why with respect to ex.

[c3.implicit.3] {rearrange} Now rearrange for the derivative we want. {eq110} The derivative of why with respect to ex is the derivative of the right-hand side, divided by the derivative of the left with respect to why. That's equation one-ten. {cond} The bottom must be different from zero. {pause} {inverse} And that's the same condition that lets you undo the left-hand function smoothly near that point, {consistent} so all is consistent.

[c3.implicit.4] {ln} Here's an example that keeps a promise from part two. {lnx} Let why be the log of a constant times ex. {exp} Then E to the why equals the constant times ex. {lhs} Differentiate. On the left, the chain rule gives E to the why, times why prime, {rhs} and on the right, just the constant. {result} That makes why prime the constant over E to the why, that is, over the constant times ex. {cancel} The constants cancel, and the derivative of the log is one over ex. {pause}

## Scene 3 · Example 40: both slopes of a circle (ch3_s3_circle)

> Hero: the hook's circle: equal-unit axes (x from −3 to 5, y from −3.5 to 3.5) on the left two thirds, the BLUE circle, a small dot at the centre (1, 0). {ex40}: heading "Example 40" (YELLOW) and `y^2 = 9 - (x - 1)^2` at the top-left; the working builds in a right-hand column.
> {move}: `(x - 1)^2 + y^2 = 9`; {centre}: a white radius from (1, 0), labelled 3; {span}: tick labels −2 and 4 on the x-axis, as on the lecturer's sketch. {task}: under the heading, the notes' line "Find the gradient."
> {diff}: `\dfrac{d}{dx}` in front of both sides of the original equation. {left}/{right}: `2y\,\dfrac{dy}{dx} = -2(x - 1)`, the `2y\,\dfrac{dy}{dx}` coming out of `y^2` with a small YELLOW tag "chain rule: y depends on x"; {divide}/{result}: `\dfrac{dy}{dx} = -\dfrac{x - 1}{y}` (notes p57, verbatim), dy/dx GREEN.
> {check}/{radius}: the point (2.8, 2.4) on the upper arc and the radius out to it, labelled with its slope `\dfrac{y}{x - 1}`; {perp}: the GREEN tangent line through the point, a right-angle mark, and `\dfrac{y}{x - 1}\cdot\left(-\dfrac{x - 1}{y}\right) = -1`.
> {xonly}: the y in the result's denominator flashes YELLOW. {sub}: `y = \pm\sqrt{9 - (x - 1)^2}` (her red handwritten line, YELLOW here); {two}: her dashed vertical line, at x = 2.8, with a dot at each crossing; {lines}: a second GREEN tangent line, at (2.8, −2.4). {sign}: `\dfrac{dy}{dx} = -\dfrac{x - 1}{\pm\sqrt{9 - (x - 1)^2}} = \mp\dfrac{x - 1}{\sqrt{9 - (x - 1)^2}}` (notes p57, verbatim), ± and ∓ YELLOW. {num}/{slopes}: readouts `y = 2.4,\ \dfrac{dy}{dx} = -\tfrac34` by the top point and `y = -2.4,\ \dfrac{dy}{dx} = +\tfrac34` by the bottom one, numbers GOLD.
> {ends}: the dashed line slides right towards x = 4; the two points close in and their tangent lines steepen until they merge into one vertical line, RED, at (4, 0); {vertical}: the same at (−2, 0). {infinite}: the slope readout climbs and becomes `\infty`, RED. {finite}: part one's differentiability box (owner ch1_s6_differentiable: the notes' box verbatim, BLUE border), small, its word "finite" lit. {strict}: `-2 < x < 4` with her red underline.
> {cond}: `2y = 0` (RED) at both ends, with an arrow to a small copy of scene 2's `\dfrac{dg}{dy} \neq 0`.
> End on the circle with its two GREEN tangent lines at x = 2.8 and the two RED vertical ones: scene 6 and the recap reuse it.

[c3.circle.1] {ex40} Now Example forty in the notes, the circle from the start. {move} Moving the square to the left gives ex minus one, squared, plus why squared, equals nine. {centre} So the centre is the point one, zero, and the radius is three, as in the last lecture. {span} The circle runs from ex equals minus two to ex equals four. {task} The task is to find the gradient.

[c3.circle.2] {diff} Differentiate both sides with respect to ex. {left} On the left, why squared is a function of why, so the chain rule gives two why, times why prime. {right} On the right, the nine drops out, and the square gives minus two, times ex minus one. {divide} Divide by two why. {result} That leaves why prime equal to minus the fraction, ex minus one, over why. {pause}

[c3.circle.3] {check} Here's a quick check. {radius} The radius out to the point has slope why over ex minus one, {perp} and the product of the two slopes is minus one. So the tangent line is perpendicular to the radius, as it should be.

[c3.circle.4] {xonly} But this slope still contains why, and we want it in terms of ex alone. {sub} The equation gives why as plus or minus the square root of nine, minus the square of ex minus one. {two} So each ex has two points on the circle, {lines} and two tangent lines with different slopes. {sign} Substitute, and the plus or minus flips to minus or plus. {num} At ex equals two point eight, the points are at plus and minus two point four, {slopes} and the slopes are minus three quarters on top, and plus three quarters below. {pause}

[c3.circle.5] {ends} Now look at the two ends, where the circle crosses the ex axis. {vertical} There the tangent line is vertical, {infinite} and the gradient becomes infinite. {finite} From part one, a derivative must be finite, so the circle has no derivative there. {strict} That's why the answer holds only for ex strictly between minus two and four. {cond} And at the ends, two why is zero, which is exactly the warning that came with equation one-ten. {pause}

## Scene 4 · Example 41: take the sine of both sides (ch3_s4_tripos)

> A box in the notes' style: heading "Example 41: Tripos question 2006, paper 2, 1A – (a) only" (YELLOW), then "If" `y = \sin^{-1}\!\left(\dfrac{x}{\sqrt{1 + x^2}}\right)`, "find dy/dx as a function of x." with "[4]" at the right in GOLD (notes p57, verbatim). {card} lights the heading, {q} the question.
> {trick}/{sine}: `\sin y = \dfrac{x}{\sqrt{1 + x^2}}` comes out of the question line (TransformFromCopy: the `\sin^{-1}` slides across the `=` and becomes `\sin`); {depends}: `y(x)` written beside it (her board), y YELLOW.
> {diff}: `\dfrac{d}{dx}(\sin y) = \dfrac{d}{dx}\left(\dfrac{x}{\sqrt{1 + x^2}}\right)` (her board); {left}: the left side becomes `\cos y\,\dfrac{dy}{dx}`, dy/dx GREEN.
> {right}: a side panel: the top `x` BLUE and the bottom `\sqrt{1 + x^2}` PURPLE (part two's quotient colours). {rule}: part two's (107) above it, small, u BLUE, v PURPLE: `\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{v\,\frac{du}{dx} - u\,\frac{dv}{dx}}{v^2}`. {pieces}: `\frac{du}{dx} = 1`, `\frac{dv}{dx} = \dfrac{x}{\sqrt{1 + x^2}}`.
> {plug}: `\dfrac{\sqrt{1 + x^2} - \dfrac{x^2}{\sqrt{1 + x^2}}}{1 + x^2}`; {clear}: `\times\dfrac{\sqrt{1 + x^2}}{\sqrt{1 + x^2}}` in the margin; {one}: `\dfrac{(1 + x^2) - x^2}{(1 + x^2)^{3/2}}`, the two x² striking out in YELLOW; {power}: `= \dfrac{1}{(1 + x^2)^{3/2}}`.
> {so}: the panel's result flies into the main line: `\cos y\,\dfrac{dy}{dx} = \dfrac{1}{(1 + x^2)^{3/2}}` (her board, verbatim). End on the question box and this line: scene 5 starts from them.

[c3.tripos.1] {card} Example forty-one is a Tripos question, from two thousand and six, worth four marks. {q} It's the inverse sine from the start: find the derivative of why, as a function of ex. {pause} {trick} The trick is to take the sine of both sides. {sine} Sine of why equals ex over the square root of one plus ex squared, {depends} keeping in mind that why depends on ex.

[c3.tripos.2] {diff} Now differentiate both sides. {left} On the left, the chain rule again: cosine of why, times why prime. {right} On the right, a quotient, with ex on top and the square root of one plus ex squared below. {rule} By the quotient rule from part two, that's the bottom times the derivative of the top, minus the top times the derivative of the bottom, all over the bottom squared.

[c3.tripos.3] {pieces} The top's derivative is one. The bottom's, by the chain rule, is ex over the same square root. {plug} So you get the square root, minus ex squared over the square root, all over one plus ex squared. {clear} Multiply above and below the line by the square root. {one} Above, one plus ex squared, minus ex squared, leaves just one. {power} Below, one plus ex squared, times its square root, is one plus ex squared, all to the power three over two. {so} So cosine of why, times why prime, equals one over that.

## Scene 5 · The sign of cos y (ch3_s5_sign)

> Scene 4's last line stays at the top: `\cos y\,\dfrac{dy}{dx} = \dfrac{1}{(1 + x^2)^{3/2}}`. {need}: `\cos y` gets her wavy underline and her note "Need cos y in terms of x."
> {identity}: `\cos y = \pm\sqrt{1 - \sin^2 y}`, the `\pm` YELLOW; {which}: a YELLOW "?" over it. {trap}: a small RED tag "most students slipped here".
> {range}: a graph of `\sin y` (BLUE) for y from −π to π, the horizontal axis labelled y. {wiggle}: a horizontal line at height 0.5 meets it twice (two RED dots). {piece}: the piece from `-\tfrac{\pi}{2}` to `\tfrac{\pi}{2}` brightens, the rest dims, and the line now meets it once; her board line `\sin^{-1} \text{ takes values in } \left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right]`. {cos}: the cosine graph (white, dashed) over the same piece, the area under it faint GREEN, and her "so cos y ≥ 0".
> {strict}: `\left|\dfrac{x}{\sqrt{1 + x^2}}\right| < 1`, since `\sqrt{1 + x^2} > |x|`; {inside}: the ends of the piece become open circles, RED; {positive}: `\cos y > 0`, GREEN. {divide}: a small `\div \cos y` arrow towards the top line. {plus}/{reject}: the `+` of the `\pm` turns GREEN; the `-` turns RED and is struck out.
> {sub}: `\cos y = +\sqrt{1 - \dfrac{x^2}{1 + x^2}} = \sqrt{\dfrac{1}{1 + x^2}}` (her board, verbatim; {common} flashes the cancelling x² YELLOW); {simplify}: `= \dfrac{1}{\sqrt{1 + x^2}}`, GREEN. {divide2}: `\dfrac{dy}{dx} = \dfrac{(1 + x^2)^{1/2}}{(1 + x^2)^{3/2}}`, exponents GOLD; {answer}: `\dfrac{dy}{dx} = \dfrac{1}{1 + x^2}`, boxed YELLOW (her box), dy/dx GREEN.
> {wrong}: a RED ghost `-\dfrac{1}{1 + x^2}` beside the box; {check}: a small plot of the original y against x (BLUE, rising from near −π/2 to near π/2, a GREEN tangent line with positive slope), and the ghost is struck out.
> {note}: her note "(in fact y = tan⁻¹ x)". {draw}: a right triangle: horizontal side 1, vertical side x, hypotenuse `\sqrt{1 + x^2}`, the angle y at the left corner (YELLOW arc). {sin}: `\sin y = \dfrac{x}{\sqrt{1 + x^2}}` lights (opposite over hypotenuse); {tan}: `\tan y = \dfrac{x}{1} = x`, then `y = \tan^{-1} x`. Keep the triangle and the boxed answer: scene 6 and the recap use them.

[c3.sign.1] {need} To finish, we divide by cosine of why, so we need it in terms of ex. {identity} Cosine squared plus sine squared is one, so cosine of why is plus or minus the square root of one minus sine squared. {which} Which sign? {pause} {trap} According to the lecturer, this is where most of the students made a mistake.

[c3.sign.2] {range} Go back to what inverse sine means. {wiggle} Sine goes up and down, so it can only be undone on a piece where it keeps increasing. {piece} The usual piece, as at school, runs from minus pi over two to pi over two, so inverse sine gives angles in that range. {cos} And on that piece, cosine is at least zero.

[c3.sign.3] {strict} Better still, our fraction lies strictly between minus one and one, because the square root is bigger than mod ex, the size of ex. {inside} So the angle, why, stays strictly inside the range, {positive} and cosine of why is strictly positive. {divide} That matters, because we're about to divide by it. {plus} So keep the plus sign, {reject} and reject the minus.

[c3.sign.4] {sub} Now substitute the fraction for sine of why. Cosine of why is the square root of one, minus ex squared over one plus ex squared. {common} Over a common denominator, the ex squared cancels, {simplify} leaving one over the square root of one plus ex squared. {divide2} Divide by that, and the power three over two drops to one. {answer} The derivative of why with respect to ex is one, over one plus ex squared. {pause=1.5}

[c3.sign.5] {wrong} The minus sign would give a negative slope, {check} but the angle grows as ex grows. {note} The lecturer added a note. The function we started with is, in fact, the inverse tangent of ex. {draw} Take a right triangle with sides one and ex, so its hypotenuse is the square root of one plus ex squared. {sin} The sine of the angle opposite ex is our fraction, {tan} and its tangent is ex over one, which is ex. {pause}

## Scene 6 · The reciprocal rule (ch3_s6_reciprocal)

> {around}/{rule}: `\dfrac{dx}{dy} = \dfrac{1}{dy/dx}` tagged "(111)" at the top.
> {pic}: part one's Figure 29 object itself (owner ch1_s2_chord; y = x³ for x from 0 to about 1.7, the point at x = 1, the TEAL chord with its δx and δy braces, the GREEN tangent line of slope 3), shown on equal-unit axes so the mirror is true. {swap}: a dashed line y = x; the whole picture reflects across it (the axis labels x and y trade places too) and becomes the cube root at the same point (1, 1). {triangle}: the δx brace now stands upright and the δy brace lies flat. {over}: readouts `\text{slope } 3` before and `\text{slope } \tfrac13` after, numbers GOLD.
> {looks}: the picture shrinks to a corner. {but}: a small DIM aside "dx and dy are not numbers (part one)". The notes' derivation (p58, verbatim) builds down the centre, increments TEAL: {finite}/{power}: `\dfrac{dx}{dy} = \lim_{\delta y \to 0} \dfrac{\delta x}{\delta y} = \lim_{\delta y \to 0} \left(\dfrac{\delta y}{\delta x}\right)^{-1}`; {tied}/{switch}: `= \lim_{\delta x \to 0} \left(\dfrac{\delta y}{\delta x}\right)^{-1}`, the subscript `\delta y \to 0` turning into `\delta x \to 0`; {inside}: `= \left(\lim_{\delta x \to 0} \dfrac{\delta y}{\delta x}\right)^{-1}`, the lim sliding inside the bracket; {done}: `= \dfrac{1}{dy/dx}`, dy/dx GREEN.
> {zero}: `\dfrac{dy}{dx} \neq 0` under the result, the `\neq 0` RED. {cube}: the same BLUE curve, now extended to negative x on small equal-unit axes: `y = x^3`; {flat}: a flat GREEN tangent line at the origin; {reflect}: the curve reflects in a dashed y = x into `y = x^{1/3}`; {vertical}: its tangent line at the origin stands vertical, RED. {nofinite}: `\dfrac{1}{0}` RED. {circle}: a small copy of scene 3's circle with its two RED vertical tangent lines flashes once.
> {use}: scene 5's triangle and boxed answer return, small, at the right. {tan}: `x = \tan y`; {dxdy}: `\dfrac{dx}{dy} = \sec^2 y`; {identity}: `= 1 + \tan^2 y`; {back}: `= 1 + x^2`; {flipit}: `\dfrac{dy}{dx} = \dfrac{1}{1 + x^2}`, boxed YELLOW; {same}: it slides beside scene 5's box, the two match, GREEN tick.

[c3.recip.1] {around} Sometimes it's simpler to treat ex as a function of why. {rule} The reciprocal rule, equation one-eleven, says that dee ex by dee why is one over dee why by dee ex. {pic} Take part one's picture, with a curve, a chord, and the tangent line. {swap} Swap the axes, by reflecting everything in the line why equals ex. {triangle} The rise becomes the run, and the run becomes the rise, {over} so the slope turns upside down. A slope of three becomes a slope of one third.

[c3.recip.2] {looks} It looks like flipping a fraction, {but} but as part one warned, a derivative is a limit, not a fraction. So let's prove it. {finite} Before the limit, delta ex and delta why are ordinary numbers, {power} so delta ex over delta why really is delta why over delta ex, to the power minus one. {tied} Let delta why go to zero. The two are tied together by the curve, so delta ex goes to zero too, {switch} and we can take the limit in delta ex instead. {inside} Then move the limit inside the power, {done} and you get one over dee why by dee ex.

[c3.recip.3] {zero} That last move needs the derivative of why to be different from zero. {cube} Here's where it fails: the same curve, why equals ex cubed, at the origin. {flat} Its tangent line there is flat, with slope zero. {reflect} Reflect it, and you get the cube root, {vertical} whose tangent line at the origin is vertical. {nofinite} One over zero is no finite slope, so the cube root has no derivative there. {circle} The circle's two ends fail in the same way.

[c3.recip.4] {use} Now Example forty-one, by a second route. {tan} The angle, why, is the inverse tangent of ex, so ex is the tangent of why. {dxdy} The derivative of ex with respect to why is secant squared of why, {identity} which is one plus tangent squared of why, {back} that is, one plus ex squared. {flipit} Turn it over, and the derivative of why with respect to ex is one over one plus ex squared, {same} the same answer as before. {pause}

## Scene 7 · Recap (ch3_s7_recap)

> {recap}: a "Recap" heading; then a row of three small callbacks, each built on its mark with its short line under it (same objects, colours and styling as where they were taught):
> {r1}: scene 3's circle (BLUE, centre (1, 0), radius 3) with the dashed line at x = 2.8 and its two GREEN tangent lines; under it `2y\,\dfrac{dy}{dx} = -2(x - 1)`. Line: "differentiate both sides; chain rule on y".
> {r2}: scene 5's triangle (sides 1 and x, hypotenuse √(1 + x²), angle y YELLOW) with `\cos y = +\dfrac{1}{\sqrt{1 + x^2}}`, the + GREEN beside a struck RED −. Line: "pick the sign from the range: cos y > 0".
> {r3}: scene 6's swapped pair, the curve and its mirror in the dashed y = x, slope triangles TEAL, readouts 3 and ⅓; under it `\dfrac{dx}{dy} = \dfrac{1}{dy/dx}`. Line: "dx/dy = 1/(dy/dx), unless dy/dx = 0".
> {h4}: the row shrinks up; the H4 card, in the series' question-card style (this scene owns the H4 card; ch5 s7 builds I1 and ch7 s1 builds H1 and H2 the same way): a rounded rectangle with a DIM border, the label "H4" in YELLOW at the top left, the sheet's text verbatim in white under it, course colours only inside the maths, about two thirds of the frame wide at hero size. The text, verbatim from the sheet: "H4. Find dy/dx if y + e^y sin y = 1/x by: i. expressing x as a function of y and then finding dx/dy; and ii. differentiating the original expression with respect to x. (Your answers should agree!)", e^y GOLD. {routes}: routes i and ii light in turn. {first}: route i gets a tag with a small (111); {second}: route ii a tag "differentiate both sides"; {agree}: two arrows meet at a YELLOW "=". Part seven reuses this card.
> {next}: clears to part four's opening question: `\dfrac{d^{10}}{dx^{10}}\left(x^2 e^{-x}\right) = \;?`, x² BLUE, e^{−x} PURPLE, the "?" YELLOW. {nth}: `\dfrac{d^{n}}{dx^{n}}(fg) = \;?` appears under it.
> End card: hold ~8 s after the last word; the music carries it.

[c3.recap.1] {recap} Time for a recap. {r1} When an equation ties why to ex, differentiate both sides, with the chain rule on every why. {r2} For an inverse, take the function of both sides, then pick the sign from the range. For inverse sine, cosine of why is positive. {r3} And dee ex by dee why is one over dee why by dee ex, unless that's zero. {pause}

[c3.recap.2] {h4} Now try question H four on the first examples sheet. {routes} It asks for one derivative, by two routes. {first} The first writes ex as a function of why, and uses the reciprocal rule. {second} The second differentiates the equation just as it stands. {agree} The two answers look different, until you use the original equation. {pause}

[c3.recap.3] {next} Next time, we differentiate again, and again. What is the tenth derivative of ex squared, times E to the minus ex? {nth} And is there a formula for the Nth derivative of a product? {pause=1.5}
