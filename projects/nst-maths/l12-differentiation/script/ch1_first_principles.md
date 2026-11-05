# Chapter 1 · What is a derivative?

NST IA Mathematics, Lecture 12 (Differentiation), part 1 of 7. Source: notes `Chapter234_to_annotate.pdf` pp. 47–50 (§4 intro and the "Origins of calculus" box, §4.1 (103), Figure 29, x³ from first principles, the notation box, |x|, the Heaviside step function (104), the differentiability box; the p50 handwriting read from the lecture frames at 07:00 and 08:20); lecture recording 00:00–08:48.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch1_s1_hook)

> On {title}: the title card, "Differentiation", "NST IA Mathematics · Lecture 12", "Part 1 · What is a derivative?".
> On {last}: three small thumbnails from Lecture 11 in a row, all in white (TEAL is reserved in L12 for the shrinking increment): a cosh curve, a circle beside an ellipse, a hyperbola. On {review}: they clear; a quote card, "a review of what you had in A-level maths, not even further maths" (the lecturer, 00:11), with "Chapter 4 of the notes" above it. On {rebuild}: under it, YELLOW, "from first principles".
> On {slow}: three tags fan out below, each with a small DIM part label: "implicit differentiation" (Part 3), "Leibniz's formula" (Parts 4–5), "classifying stationary points" (Part 6).
> On {one}: the card clears; left, `y = y(x)` over a single x-axis arrow, with a GREEN tag "one variable: this lecture". On {partial}: right, DIM, the notes' p47 line: `h = h(x, y)`, then `\frac{\partial h}{\partial x}` and `\frac{\partial h}{\partial y}` → "Partial differentiation", tagged "Chapter 7 of the notes, and next term".
> On {curve}: everything clears; bare axes and a BLUE curve (the same curve as s2: y = x³ for x from about 0 to 1.7), two dots on it joined by a TEAL chord. On {swing}: the right dot slides towards the left one and the chord swings round until it lies along the GREEN tangent line at the fixed dot.
> On {ask}: two question lines under the picture: "What exactly is a derivative?" and "When does it fail to exist?"; beside the second, a tiny RED V-shaped corner (a hint of s5).

[c1.hook.1] {title} This is part one of Differentiation. {last} Last time, in Lecture eleven, you met the hyperbolic functions, and the conics: circles, ellipses and hyperbolas. {review} The lecturer calls Chapter four of the notes a review of A-level maths. {rebuild} So these videos rebuild it from the foundations. {slow} And they slow down on the parts people only half remember: implicit differentiation, Leibniz's formula, and classifying stationary points.

[c1.hook.2] {one} Everything in this lecture is about functions of one variable. {partial} Taking a function of two variables and differentiating it in different directions is called partial differentiation. That comes in Chapter seven of the notes, and next term. {pause}

[c1.hook.3] {curve} So start at the very beginning: a curve, and a line through two of its points. {swing} Slide one point towards the other, and the line swings round until it just touches the curve. {ask} What exactly is a derivative? And when does it fail to exist? {pause}

## Scene 2 · From chord to tangent line (ch1_s2_chord)

> Figure 29, built step by step. This is the series' recurring figure (the recap shrinks it; ch3 s6 reflects it in y = x; ch6 s5 reuses its tangent line), so build it as one reusable object. Axes labelled "x" and "y(x)"; the BLUE curve is y = x³ for x from about 0 to 1.7 (convex and rising, like the notes' curve), drawn first with no formula label. On {curve}: the axes and the curve draw in.
> On {point}: a dot on the curve at x = 1, a dashed drop line to the x-axis labelled "x". On {step}: a second dot at x + δx (δx = 0.5 to start), its axis label "x + δx", and a TEAL brace over the run labelled "δx". On {rise}: a TEAL brace on the rise labelled `\delta y = y(x+\delta x) - y(x)`, with the dashed right-angle corner of the notes' left panel.
> On {chord}: the TEAL chord through the two dots, extended a little both ways, labelled "chord". On {slope}: a TEAL readout `\frac{\delta y}{\delta x}` beside it. On {example}: a small tag "y = x³, at x = 1" in the corner. On {half}: the readout shows "δx = 0.5: slope 4.75". On {tenth}: the second dot slides in and the chord swings: "δx = 0.1: slope 3.31". On {hundredth}: "δx = 0.01: slope 3.03", the dots nearly together. (Checked with sympy 1.14: at x = 1 the chord slope is 3 + 3δx + (δx)², giving 4.75, 3.31, 3.0301.)
> On {shrink}: the notes' right panel: faint ghosts of the earlier chords stay, a "δx → 0" arrow, and the chord settles onto the GREEN tangent line; the readout turns GREEN, "slope 3". On {deriv}: under it, "the derivative" (GREEN). On {box}: below the figure, (103) boxed YELLOW: `\frac{dy}{dx} = \lim_{\delta x \to 0} \frac{y(x+\delta x) - y(x)}{\delta x} = \lim_{\delta x \to 0} \frac{\delta y}{\delta x}`, every δx and δy TEAL, dy/dx GREEN, "(103)" small and DIM. On {later}: a small DIM tag "limits, properly: Chapter 5 of the notes".
> On {zero}: inside the box, the top and the bottom of the last quotient each get a small TEAL "→ 0", and a YELLOW "0/0 ?" pops up beside it. On {newton}: a YELLOW name "Newton" and "17th century", with a small RED "controversial". On {resolved}: the "0/0 ?" turns into the GREEN "3" from the figure, with the lecturer's line in quotes under it: "another mathematical crisis successfully resolved".
> On {linear}: the figure slides aside; the notes' filled blank "linear operation" (YELLOW). On {sum}: `\frac{d}{dx}\big(f + g\big) = \frac{df}{dx} + \frac{dg}{dx}` (f BLUE, g PURPLE). On {const}: `\frac{d}{dx}\big(c\,f\big) = c\,\frac{df}{dx}`, the c sliding out in front. On {quot}: under the sum, its difference quotient splits in two: `\frac{(f+g)(x+\delta x) - (f+g)(x)}{\delta x} = \frac{f(x+\delta x) - f(x)}{\delta x} + \frac{g(x+\delta x) - g(x)}{\delta x}`, δx TEAL.

[c1.chord.1] {curve} Take a function of one variable, why of ex, drawn in blue. {point} Pick a point on it, at ex. {step} Now step along by a small amount, delta ex, to a second point, at ex plus delta ex. {rise} Between the two points, the curve rises by delta why: the height at the second point, minus the height at the first.

[c1.chord.2] {chord} The line through the two points is called the chord. {slope} Its slope is the rise over the run, delta why over delta ex. {example} Here's an example: why equals ex cubed, at ex equals one. {half} With delta ex equal to a half, the chord's slope is four point seven five. {tenth} With a tenth, it's three point three one. {hundredth} With a hundredth, three point zero three. {pause}

[c1.chord.3] {shrink} As delta ex shrinks, the chords swing round and settle on one line, the tangent line. Here its slope is three. {deriv} That slope is the derivative, the gradient of the curve at that point. {box} So here's the definition. The derivative of why with respect to ex is the limit, as delta ex goes to zero, of delta why over delta ex. {later} Chapter five of the notes does limits properly. For now, closer and closer is enough.

[c1.chord.4] {zero} Look closely at that limit. The top goes to zero, and so does the bottom. {newton} Newton's idea, in effect, divides zero by zero, and in the seventeenth century that was controversial. {resolved} Yet the ratio heads somewhere definite, here to three. As the lecturer puts it, another mathematical crisis successfully resolved. {pause}

[c1.chord.5] {linear} One property follows straight away: differentiation is a linear operation. {sum} The derivative of a sum is the sum of the derivatives, {const} and a constant factor comes out in front. {quot} That's because the quotient for a sum splits into one quotient per function, and limits add up the same way.

## Scene 3 · x³ from first principles (ch1_s3_cube)

> On {why}: one derivation column, centred; s2's tag "y = x³, at x = 1" stays small in the top-right corner. δx TEAL throughout, the powers of x white, the result GREEN.
> On {recipe}: five small step labels across the top, "substitute · expand · subtract · divide · limit" (the lecturer's recipe, 02:56); each lights YELLOW while its step happens. On {sub}: `y(x+\delta x) = (x+\delta x)^3`.
> On {expand}: `= x^3 + 3x^2\,\delta x + 3x\,(\delta x)^2 + (\delta x)^3`, one term at a time. On {subtract}: `y(x+\delta x) - y(x) = 3x^2\,\delta x + 3x\,(\delta x)^2 + (\delta x)^3`, the x³ striking out (RED) as it cancels. On {left}: every TEAL δx factor pulses.
> On {divide}: `\frac{y(x+\delta x) - y(x)}{\delta x} = 3x^2 + 3x\,\delta x + (\delta x)^2`, one δx from each term flying down into the denominator. On {check}: a side calculation by the corner tag: `3 + 3\,\delta x + (\delta x)^2`, and δx = 0.5 gives "4.75", s2's first readout (TEAL).
> On {limit}: `3x\,\delta x` and `(\delta x)^2` shrink and fade to 0. On {result}: the notes' line `\frac{dy}{dx} \equiv \lim_{\delta x \to 0} \frac{y(x+\delta x) - y(x)}{\delta x} = 3x^2`, 3x² GREEN, boxed YELLOW. On {rule}: beside it, `y = x^a \;\Rightarrow\; \frac{dy}{dx} = a\,x^{a-1}`, the a in front and the a − 1 flashing YELLOW, then a = 3 written under it. On {three}: by the corner tag, "x = 1: 3x² = 3" in GREEN, matching s2's tangent-line slope.
> On {notes}: below, DIM, the notes' line verbatim: `\text{Provided } |\delta x| < 1 \text{ then } 1 > |\delta x| > |\delta x|^2 > |\delta x|^3 > \cdots`. On {needed}: a YELLOW tag "not needed" (the lecturer, 03:26), and arrows back to the two faded terms, each with its δx factor circled.
> On {card}: the boxed result shrinks into the x³ derivative-chain card in the top-left corner: `x^3 \to 3x^2`, with room on the right for more links (ch4 s2 extends it to 6x, 6, 0; ch6 s4 sets it beside x⁴'s). (All algebra checked with sympy 1.14: expand, subtract, divide, and the limit 3x².)

[c1.cube.1] {why} So why do those chord slopes head for three? Work it out from first principles. {recipe} The lecturer's recipe has five steps: substitute, expand, subtract, divide, and take the limit. {sub} First, substitute ex plus delta ex into ex cubed.

[c1.cube.2] {expand} Expand the cube. You get ex cubed, plus three ex squared times delta ex, plus three ex times delta ex squared, plus delta ex cubed. {subtract} Now subtract why of ex, which is ex cubed. It cancels the first term. {left} Every term that's left has at least one factor of delta ex.

[c1.cube.3] {divide} Divide by delta ex. Each term loses one factor of it. You get three ex squared, plus three ex times delta ex, plus delta ex squared. {check} At ex equals one, with delta ex equal to a half, this comes to four point seven five. That's the first chord slope you saw. {pause}

[c1.cube.4] {limit} Now let delta ex go to zero. The last two terms each carry a factor of delta ex, so they go to zero. {result} What's left is three ex squared. {pause} {rule} That's the power rule you already know: the power comes down in front, and the new power is one less. {three} At ex equals one, it gives three, the slope of the tangent line.

[c1.cube.5] {notes} The notes add a condition here: if delta ex is smaller than one in size, each power of it is smaller than the last. {needed} The lecturer says you can skip it: every leftover term has a factor of delta ex, so it goes to zero anyway. {card} Keep the result on a card, ex cubed to three ex squared. Part four takes it further.

## Scene 4 · Notation, and who invented it (ch1_s4_notation)

> On {box}: s3's card stays small top-left; `\frac{dy}{dx}` (GREEN) sits centre, lifted from (103). On {two}: it moves up; a white timeline appears with two YELLOW names: "Isaac Newton" and "Gottfried Wilhelm Leibniz".
> On {dates}: GOLD year ticks, each with a small caption: "1665/66" (Newton's breakthrough), "1686" (Leibniz publishes), "1687" (Newton publishes); a brace from 1665/66 to 1686, "some 20 years". On {quarrel}: a jagged RED line between the two names, "each claiming to have been first".
> On {styles}: under Newton, "limits"; under Leibniz, "geometric arguments" and his symbols `\frac{d}{dx}` and `\int` (BLUE). On {britain}: DIM under Newton, "Britain, 18th century"; under Leibniz, "rest of the world", with a GREEN up-arrow "more progress". On {dot}: from Newton's side, `\dot{x} = \frac{dx}{dt}`, the dot YELLOW, "still used".
> On {euler}: two more YELLOW names join the timeline: "Euler" with `Df,\ D^2 f`, and "Lagrange" (his student) with `f',\ f''`. On {india}: a DIM note at the far left of the timeline, "India: similar ideas, a couple of centuries earlier".
> On {list}: the timeline clears; the notes' "Other notations" line verbatim, each item lighting as it's said: `\frac{dy}{dx},\ \frac{d}{dx}y,\ y',\ y_x,\ y_{,x},\ Dy`. On {time}: under it, `\dot{u} \equiv \frac{du}{dt}` with "a function of time, u(t)". On {lecturer}: a GREEN tick under the fraction and under the prime, "this course"; a DIM tag under Dy, "later, especially next term".
> On {operator}: `\frac{dy}{dx}` splits into the operator `\frac{d}{dx}` (BLUE) and the function y, with an arrow "acting on y" and the notes' words "differential operator". On {quotient}: dy and dx pull apart over a fraction bar, with a YELLOW "?". On {treat}: a small DIM preview, `\frac{dx}{dy} = 1 \Big/ \frac{dy}{dx}`. On {not}: a RED tag on the fraction bar, "not a quotient". On {part3}: the preview gets a DIM tag, "proved in Part 3".

[c1.notation.1] {box} The symbol in that box, dee why by dee ex, has a history. {two} Calculus was invented by two people at around the same time, Isaac Newton and Gottfried Leibniz. {dates} Leibniz published in sixteen eighty-six, and Newton in sixteen eighty-seven. But it seems Newton made his breakthrough some twenty years earlier, in sixteen sixty-five and sixty-six. {quarrel} Each claimed to be first, and they fell out badly.

[c1.notation.2] {styles} Newton's approach was based on limits. Leibniz used geometric arguments, and a much simpler notation, including dee by dee ex and the integral sign. {britain} Britain kept Newton's notation through the eighteenth century, and the rest of the world, using Leibniz's, made more progress. {dot} Newton's dot, for a derivative with respect to time, survives. {euler} Oiler wrote a capital D, and his student Lagrange gave us primes. {india} And mathematicians in India seem to have had similar ideas a couple of centuries earlier.

[c1.notation.3] {list} So here are the notations in the notes. First, dee why by dee ex, and dee by dee ex acting on why. Then why prime, two kinds of subscript, and a capital D. {time} For a function of time, a dot on top. {lecturer} This course uses mostly the fractions and the primes. The capital D comes later, especially next term.

[c1.notation.4] {operator} Read dee why by dee ex as an operator, dee by dee ex, acting on the function why. {quotient} Dee why over dee ex looks like a fraction. {treat} Some manipulations will treat it like one. {not} But it is not a fraction. {part3} So when part three flips it over, it proves that the flip is allowed.

## Scene 5 · A corner and a jump (ch1_s5_fail)

> On {graph}: axes centred, x from about −2 to 2. On {modx}: the BLUE V, labelled `y = |x|` as on her board (04:20). On {left}: a short GREEN tangent-line segment along the left arm, "slope −1"; on {right}: one along the right arm, "slope +1". On {continuous}: a pen-dot traces the whole V in one stroke, left to right.
> On {corner}: zoom in a little on the origin; the corner dot turns RED. On {candidates}: a white line pivots through the origin, sweeping between the two arms (each position meets the V only at the corner), with a YELLOW "?". On {rightchord}: TEAL chords from the origin to points on the right arm, each reading "slope +1"; on {leftchord}: chords to points on the left arm, "slope −1". On {fails}: the notes' formula to the right, `\frac{d|x|}{dx} = \begin{cases} -1 & \text{if } x < 0, \\ +1 & \text{if } x > 0, \end{cases}` and under it, in RED, "but d|x|/dx does not exist at x = 0."
> On {step}: the V shrinks into a thumbnail on the left third of the screen and stays. The notes' (104): `H(x) = \begin{cases} 0 & x < 0, \\ 1 & x > 0, \end{cases}` with "(104)" small and DIM. On {zero}: on fresh axes, a BLUE line along the negative x-axis; on {one}: a BLUE line at height 1 for x > 0.
> On {conv}: a YELLOW "x = 0 ?" at the gap, and a DIM tag "definitions vary". On {dots}: the lecturer's convention (frame 07:00): an open circle at (0, 0) and a filled dot at (0, 1).
> On {flat}: GREEN "slope 0" labels on both pieces. On {undefined}: her board's line beside the graph, `\frac{dH}{dx} = \begin{cases} 0 & x \neq 0 \\ \text{undefined at } x = 0 \end{cases}`, "undefined" RED; a dashed RED vertical segment from (0, 0) to (0, 1) marks the jump.
> On {cross}: a TEAL chord from (−δx, 0) on the left piece up to the filled dot at (0, 1), a TEAL brace "δx" under the run and "1" beside the rise. On {slopeh}: the readout `\text{slope} = \frac{1}{\delta x}`. On {grow}: δx shrinks and the chord steepens: "δx = 0.1: slope 10", then "δx = 0.01: slope 100", the readout turning RED. (Checked in Python 3.11 with the lecturer's H(0) = 1.)
> The V thumbnail and a matching step thumbnail come back side by side in s6 and the recap.

[c1.fail.1] {graph} Now, when does it fail? Functions are not always differentiable. {modx} Here's an example: why equals mod ex, the absolute value of ex. {left} To the left of zero it's minus ex, a straight line with slope minus one. {right} To the right it's just ex, with slope plus one. {continuous} And it's continuous. You can draw it without lifting the pen.

[c1.fail.2] {corner} But look at the corner, at zero. {candidates} Which line is the tangent line there? Lots of lines touch the corner, and none of them is the right one. {rightchord} Chords from the right all have slope plus one. {leftchord} Chords from the left all have slope minus one. {fails} There's no single slope, so the derivative of mod ex does not exist at zero. Everywhere else, it's fine. {pause}

[c1.fail.3] {step} The second example is the Heaviside step function. {zero} It's zero for negative ex, {one} and one for positive ex. {conv} At zero itself, definitions vary, and the notes leave it out. {dots} The lecturer puts that point in the top piece: a filled dot at height one, and an open circle at the origin. That way the function has exactly one value at zero.

[c1.fail.4] {flat} Away from zero, the graph is flat, so its derivative is zero. {undefined} At zero, it's undefined. {cross} To see why, take a chord from the left that crosses the jump. {slopeh} It rises by one over a run of delta ex, so its slope is one over delta ex. {grow} With delta ex equal to a tenth, that's ten. With a hundredth, a hundred. {pause} The slope grows without bound, so no tangent line can match it.

## Scene 6 · What "differentiable" demands (ch1_s6_differentiable)

> On {def}: at the top, her handwritten definition (frames 07:00 and 08:20) in a handwriting-style font, YELLOW: "f is differentiable at x if" `\lim_{h \to 0} \frac{f(x+h) - f(x)}{h}` "exists and finite.". On {quot}: a small copy of (103)'s quotient from s2 slides up under it and lines up term by term. On {rename}: the TEAL δx in the copy morphs into the TEAL h; a small tag "h: just a variable".
> On {box}: the notes' box below, verbatim, BLUE border: "For a function f(x) to be differentiable at x:" / "(a) the function must be continuous" / "(b) the derivative f′ exists if it is finite and defined." / "⇒ the left- and right-hand limits must be the same:" / `\lim_{h \to 0}\left(\frac{f(x) - f(x-h)}{h}\right) = \lim_{h \to 0}\left(\frac{f(x+h) - f(x)}{h}\right)`, every h TEAL. On {a} and {b}: those lines light YELLOW in turn. On {lefthand}: the left quotient lights, with a tiny sketch of a TEAL chord from x − h to x; on {righthand}: the right one, with a chord from x to x + h.
> On {runmod}: the box shrinks to the top; s5's V thumbnail (left) and step thumbnail (right) sit under it, each with an (a) row and a (b) row. Under the V: "(a) continuous", GREEN tick. On {modsides}: "(b) left −1, right +1", with s5's two TEAL chords; on {modfail}: "−1 ≠ +1", RED cross.
> On {runstep}: the step's column lights. On {pieces}: GREEN "slope 0" on both pieces and a YELLOW "0 = 0 ?" (the lecturer's point, 08:15). On {jump}: the RED dashed jump flashes; "(a) not continuous", RED cross. On {blow}: under (b), "left: 1/h → ∞" in RED, "right: 0".
> On {implies}: the thumbnails clear; the notes' line under the box: "If f′ exists, then Δf → 0 as Δx → 0 ⇒ f is continuous." Under it the reason: `f(x+h) - f(x) = h \cdot \frac{f(x+h) - f(x)}{h} \;\to\; 0 \cdot f'(x) = 0`. On {cont}: "differentiable ⇒ continuous" (GREEN). On {converse}: "continuous ⇏ differentiable" (RED), with the V thumbnail beside it.
> On {finite}: a small BLUE circle (part three's Example 40: centre (1, 0), radius 3, from x = −2 to x = 4) with RED vertical tangent lines at x = −2 and x = 4, each labelled "slope: infinite". On {circle}: a DIM tag "Part 3". (Checked with sympy 1.14: the upper semicircle's slope tends to −∞ as x → 4 and to +∞ as x → −2.)
> The box is the series' differentiability box: build it as one object (ch2 s3 and s5 and ch3 s3 cite it; the recap shrinks it).

[c1.diff.1] {def} So what exactly does differentiable demand? Here's the lecturer's definition. F is differentiable at ex if this limit exists, and is finite. {quot} It's the quotient from before: the change in F, over a small step. {rename} She calls the step H, instead of delta ex. As she says, H is just a variable.

[c1.diff.2] {box} The notes' box says what that takes. {a} First, the function must be continuous. {b} Second, the derivative must be finite and defined. {lefthand} That means the left-hand limit, where you step back from ex by H, {righthand} must equal the right-hand limit, where you step forward. {pause}

[c1.diff.3] {runmod} Run mod ex through the box, at zero. It's continuous, so the first test passes. {modsides} But the left-hand limit is minus one, and the right-hand limit is plus one. {modfail} They disagree, so the second test fails.

[c1.diff.4] {runstep} Now the Heaviside step function. {pieces} Both pieces are flat, with slope zero, so the two sides seem to agree. {jump} But the function jumps, so it is not continuous, and the first test fails. {blow} Indeed, the left-hand quotient is one over the step, which blows up. {pause}

[c1.diff.5] {implies} Notice which way it goes. If the derivative exists, the change in F is the step, times the difference quotient, which stays finite, so it goes to zero with the step. {cont} So a differentiable function is continuous. {converse} The reverse is false, and mod ex shows it. {finite} Finite matters too. Where the tangent line is vertical, its slope is infinite. {circle} The circle in part three has two such points.

## Scene 7 · Recap (ch1_s7_recap)

> On {recap}: a small "Recap" heading. Four panels, two by two, one per sentence, each with its short line under it, made from the same objects, colours and styling as the scene it comes from (never a bare list of text):
> On {r1}: s2's Figure 29, small: the BLUE curve, faint TEAL chords converging onto the GREEN tangent line. Line: "derivative = limit of chord slopes".
> On {r2}: s3's derivation, small: the five step labels over the δx column, ending in the boxed GREEN 3x². Line: "first principles: substitute, expand, subtract, divide, limit".
> On {r3}: s5's V and step side by side, the RED corner dot and the RED dashed jump flashing. Line: "a corner or a jump: no derivative".
> On {r4}: s6's differentiability box, small, its (a), its (b) and the word "finite" lighting in turn. Line: "differentiable: continuous, both sides agree, finite".
> On {next}: the panels dim; s2's (103) box moves to the centre and three labels come out of it (TransformFromCopy): "chain rule", "product rule", "quotient rule". On {same}: "Part 2 · The rules, from first principles".
> Then the end card, held about eight seconds after the last word (music carries it).

[c1.recap.1] {recap} Time for a recap. {r1} The derivative is the limit of chord slopes, as delta ex goes to zero. {r2} From first principles, you substitute, expand, subtract, divide, and take the limit. For ex cubed, that gives three ex squared.

[c1.recap.2] {r3} At a corner or a jump, there's no derivative. {r4} To be differentiable, a function must be continuous, its left-hand and right-hand limits must agree, and its slope must be finite. {pause}

[c1.recap.3] {next} Next time: the chain rule, the product rule and the quotient rule. {same} Each one comes from this same limit. {pause}
