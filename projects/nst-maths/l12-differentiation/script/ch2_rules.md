# Chapter 2 · The rules, from first principles

NST IA Mathematics, Lecture 12 (Differentiation), part 2 of 7. Source: Berloff's notes, Chapter234_to_annotate.pdf pp. 50–55 (§4.2 tables; §4.3 derivation, (105), Example 37, the two-variable chain rule; §4.4 derivation, (106), Example 38; §4.5 (107), Example 39); lecture 08:48–09:54 and 10:44–19:30 (09:54–10:44, the log via E to the why, is part three's); Examples Sheet I, H1 and H2 (pp. 10, 15).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card: "Differentiation", "NST IA Mathematics · Lecture 12", "Part 2 · The rules, from first principles".
> On {last}, left: a small Figure 29 in part one s2's exact styling (owner ch1_s2_chord: the BLUE curve y = x³ for x from about 0 to 1.7 with no formula label, the point at x = 1, a TEAL chord to the point at x + δx with δx = 0.5, the GREEN tangent line of slope 3); the chord swings into the tangent line once. Beside it part one's boxed (103): `\frac{dy}{dx} = \lim_{\delta x \to 0} \frac{y(x+\delta x) - y(x)}{\delta x}`, δx TEAL, dy/dx GREEN.
> On {cube}: part one s3's x³ working stacks up under it in small type, line by line (`(x+\delta x)^3 = x^3 + 3x^2\delta x + 3x(\delta x)^2 + (\delta x)^3`, the subtraction, the division, then `3x^2` in GREEN): a long column, to show the effort.
> On {product}: all of that slides left and dims. Centre: `\frac{d}{dx}\left(\ln x \, \sin x\right)` with ln x BLUE and sin x PURPLE (first function BLUE, second PURPLE: the role colours start here and run through the series), and a YELLOW "?".
> On {table}: a thumbnail of scene 2's derivative table drops in under it; on {rules}, three tiles appear in a row, labelled "chain rule", "product rule", "quotient rule", each lighting as it is named.
> On {ask}: a YELLOW "why?" lands over the three tiles. On {same}: a thin arrow runs from each tile back to the dimmed boxed (103), which brightens: one limit under all three. On {first}, the table thumbnail grows, carrying into scene 2.

[c2.hook.1] {title} Welcome back. This is part two, on the rules of differentiation, from first principles. {last} Last time, we defined the derivative as the limit of chord slopes, as delta ex goes to zero. {cube} Even ex cubed took half a page of algebra. {pause}

[c2.hook.2] {product} Now try the log of ex, times sine of ex. Nobody differentiates that straight from the limit. {table} Instead, you use a short table of basic derivatives, {rules} and three rules, the chain rule, the product rule, and the quotient rule. {pause}

[c2.hook.3] {ask} But why are the rules true? {pause} {same} In this part, each of them comes out of that same limit, with one small trick apiece. {first} First, the table.

## Scene 2 · A short table, and where it comes from (ch2_s2_table)

> The §4.2 table, built here once in the style part seven s2 reuses: a ruled two-column card, header `y` | `y'` (y′ GREEN), MathTex rows with e^{ax}, never exp(ax). Block 1, caption "functions you should know how to differentiate": `x^a` → `a x^{a-1}`; `e^{ax}` → `a e^{ax}`; `\ln(ax) = \ln a + \ln x` → `\frac{1}{x}`. Block 2, caption "worth remembering, but can be derived from e^{ax}": `\sin(ax)` → `a\cos(ax)`; `\cos(ax)` → `-a\sin(ax)`; `\sinh(ax)` → `a\cosh(ax)`; `\cosh(ax)` → `a\sinh(ax)`. Block 3, caption "worth remembering (but can be derived)": `\tan(ax)` → `a\sec^2(ax)`; `\tanh(ax)` → `a\,\mathrm{sech}^2(ax)`. Every e^{ax} GOLD; hyperbolic names white (L12 rule); the constant a in each derivative YELLOW where it comes out in front. Every entry checked with sympy 1.14.
> On {table}: block 1's header and caption. On {power}: row 1; the exponent a copies down in front (TransformFromCopy) and the new exponent a − 1 appears. On {exp}: row 2, the a from the exponent copied out in front. On {log}: row 3.
> On {drop}: a YELLOW "?" beside row 3, where the a has vanished from the derivative. On {split}: under row 3, `\ln(ax) = \ln a + \ln x` expands; on {const}, ln a is boxed with the tag "a constant", an arrow to `0`, and ln x arrows to `\frac{1}{x}` (GREEN). On {exists}, a YELLOW tag `ax > 0`. On {proof}, a small tag "proof: part 3".
> On {rest}: blocks 2 and 3 slide in under block 1, dimmed, with their captions. The table shrinks to the right third and stays; the left is a workspace.
> On {hyp}: `\sinh(ax) = \tfrac12\left(e^{ax} - e^{-ax}\right)` and `\cosh(ax) = \tfrac12\left(e^{ax} + e^{-ax}\right)`, e^{ax} GOLD and e^{−ax} PURPLE as in Lecture 11. On {diffhyp}: `\frac{d}{dx}\sinh(ax) = \tfrac12\left(a e^{ax} + a e^{-ax}\right)`: each exponential's a drops out in front, and the PURPLE one's comes out as −a. On {flip}: the middle minus of the sinh line turns into a YELLOW plus, `= a\cosh(ax)`, and the sinh row of the table lights. On {cosh}: `\frac{d}{dx}\cosh(ax) = \tfrac12\left(a e^{ax} - a e^{-ax}\right) = a\sinh(ax)`, and the cosh row lights.
> The hyperbolic lines clear. On {trig}: the sin and cos rows of the table pulse. On {euler}: Lecture 10's formula with θ = ax: `e^{iax} = \cos(ax) + i\sin(ax)` (e^{iax} GOLD, every i PINK). On {left}: `\frac{d}{dx}e^{iax} = ia\,e^{iax}`, the ia copied out of the exponent. On {expand}: `ia\left(\cos ax + i\sin ax\right) = -a\sin ax + i\,a\cos ax`, the i · i flashing YELLOW into −1. On {match}: the right side differentiated, `\frac{d}{dx}\cos(ax) + i\,\frac{d}{dx}\sin(ax)`, written under it. On {pair}: brackets join real part to real part (`\frac{d}{dx}\cos(ax) = -a\sin(ax)`) and imaginary to imaginary (`\frac{d}{dx}\sin(ax) = a\cos(ax)`); the sin and cos rows of the table light GREEN.
> On {dict}: Lecture 11's dictionary card, small, top-left (i PINK, hyperbolic names white): `\cos(ix) = \cosh x`, `\sin(ix) = i\sinh x`; under it `\frac{d}{dx}\cos(ix) = -i\sin(ix) = -i \cdot i\sinh x = \sinh x` (checked with sympy 1.14).
> On {tan}: block 3 pulses, tagged "quotient rule, later in this part". On {sheet}: a small sheet card "Examples Sheet I · H2: write in exponentials".

[c2.table.1] {table} Here's the notes' short table of functions you should know how to differentiate. {power} A power of ex: bring the power down in front, and lower it by one. {exp} The exponential, with a constant in its power, gives back the same exponential, times that constant. {log} And the log of a constant times ex has derivative one over ex. {pause}

[c2.table.2] {drop} Why does the constant drop out of the log? {pause} {split} The log of a product is the sum of two logs. {const} The log of the constant is just a number, with derivative zero, so only the log of ex is left. {exists} The lecturer added a condition. The log has to exist, so the constant times ex must be positive. {proof} We'll prove the one over ex in part three.

[c2.table.3] {rest} The rest of the table, the notes say, can all be derived from the exponential. {hyp} Shine and cosh are the easiest. From Lecture eleven, shine is half the difference of two exponentials, and cosh is half their sum. {diffhyp} Differentiate, and each exponential gives back itself, times its constant. In the second one, that constant is negative. {flip} So the minus sign turns into a plus, and the derivative of shine is the constant, times cosh. {cosh} The same way, the derivative of cosh is the constant, times shine.

[c2.table.4] {trig} Sine and cosine come from Oiler's formula, from Lecture ten. {euler} E to the eye theta is cosine theta, plus eye sine theta, with theta the constant times ex. {left} Differentiating the left side brings out eye times the constant. {expand} Multiply it in. Eye times eye is minus one, so the real part is minus the constant times sine, and the imaginary part is the constant times cosine. {match} On the right, the real part is the derivative of cosine, and the imaginary part is the derivative of sine. {pair} Match them up, and both rules drop out. {pause}

[c2.table.5] {dict} The lecturer's other route is Lecture eleven's dictionary: cosine of eye ex is cosh of ex, so the cosine rule turns into the cosh rule. {tan} The last two rows, tangent and tanch, follow from the quotient rule, later in this part, so there's no need to memorise them. {sheet} And writing functions with exponentials is the method of question H two, on the first examples sheet.

## Scene 3 · The chain rule (ch2_s3_chain)

> On {setup}, top-left, a small schematic that stays all scene: x → [inner function u] → u(x) → [outer function f] → f(u(x)), u PURPLE, f BLUE. On {example}: under it `\sin(x^2)`, sin BLUE, x² PURPLE.
> On {def}, centre: `\frac{f(u(x+\delta x)) - f(u(x))}{\delta x}` (f BLUE, u PURPLE, δx TEAL).
> On {trick}: the quotient slides up to make room. On {mult}: the notes' p. 52 line grows out of it: `= \left[\frac{f(u(x+\delta x)) - f(u(x))}{u(x+\delta x) - u(x)}\right]\left[\frac{u(x+\delta x) - u(x)}{\delta x}\right]`, the two new copies of `u(x+\delta x) - u(x)` in TEAL (the notes print them green). On {one}: a small YELLOW "× 1" under the TEAL pair.
> On {regroup}: both TEAL copies collapse into `\delta u` (TEAL), labelled "change in the inner function", and the line becomes `\left[\frac{f(u + \delta u) - f(u)}{\delta u}\right]\left[\frac{u(x+\delta x) - u(x)}{\delta x}\right]`. On {first}, the first bracket lights; on {second}, the second.
> On {limit}: `\delta x \to 0` (TEAL) under the line. On {cont}: part one's differentiability box (owner ch1_s6_differentiable: the notes' box verbatim, BLUE border, h TEAL) appears small in the bottom-right corner, its line "(a) the function must be continuous" lit, and `\delta u \to 0` (TEAL) appears beside `\delta x \to 0`. On {df}: the first bracket turns into `\frac{df}{du}` (GREEN); on {du}, the second into `\frac{du}{dx}` (GREEN).
> On {rule}: (105) boxed YELLOW, `\frac{d}{dx} f\big(u(x)\big) = \frac{df}{du}\,\frac{du}{dx}` (f BLUE, u PURPLE), tag "chain rule". On {name}: the subtitle "differentiation of a function of a function".
> On {dee}: the two du's in (105) flash and a faint cancelling stroke ghosts across them, then fades; under it, in TEAL, the finite version `\frac{\delta f}{\delta u}\cdot\frac{\delta u}{\delta x}`. On {catch}: a small RED footnote `\delta u \neq 0?`; on {patch}, a GREEN tick beside (105) and the footnote dims.

[c2.chain.1] {setup} Now the chain rule. It's for a function of a function. An outer function, F, is applied to an inner function of ex. {example} In sine of ex squared, sine is the outer function, and ex squared the inner one. {def} As always, start from the definition. That's the change in F, divided by delta ex.

[c2.chain.2] {trick} Here's the trick from the notes. {mult} Multiply and divide by the same thing, the change in the inner function, as ex moves to ex plus delta ex. {one} That's multiplying by one: nothing changes. {regroup} Now regroup into two quotients. {first} The first is the change in F, over the change in the inner function. {second} The second is the change in the inner function, over delta ex.

[c2.chain.3] {limit} Now let delta ex go to zero. {cont} The inner function is differentiable, so, by part one's box, it's continuous, and its change goes to zero too. {df} So the first quotient becomes the derivative of F with respect to the inner function. {du} The second becomes the derivative of the inner function with respect to ex. {rule} That's the chain rule. Differentiate the outer function, and multiply by the derivative of the inner one. {pause}

[c2.chain.4] {name} The notes also call it differentiation of a function of a function. {dee} In this notation, it looks like two fractions cancelling, and before the limit, they really were fractions. {catch} One small catch. We divided by the change in the inner function, so it must be different from zero. {patch} A full proof patches the case where it's zero, and the rule still holds.

## Scene 4 · Example 37, and a look ahead (ch2_s4_chain_ex)

> Card headed "Example 37: Chain rule", as the notes. Schematic and colours from scene 3: outer function BLUE, inner PURPLE; (105) small in the top-right corner.
> On {ex}: (a) `y = \sin x^2 = f\big(g(x)\big)`; on {outer}, `f(g) = \sin g` (BLUE) and `g(x) = x^2` (PURPLE). On {cos}: `\frac{dy}{dx} = \frac{df}{dg}\,\frac{dg}{dx} = (\cos g)`, cos g BLUE; on {inner}, `(2x)` PURPLE joins it; on {back}, g is replaced by x²: `= 2x\cos x^2`, boxed YELLOW.
> On {log}: (b) `z = \ln(\cos x) = u\big(v(x)\big)`, `u = \ln v` (BLUE), `v = \cos x` (PURPLE). On {outerlog}: `\frac{dz}{dx} = \frac{du}{dv}\,\frac{dv}{dx} = \left(\frac{1}{v}\right)` (BLUE); on {innercos}, `(-\sin x)` (PURPLE); on {tan}, `= -\frac{\sin x}{\cos x} = -\tan x`, boxed YELLOW.
> On {caveat}: a small graph of cos x over about −2π to 2π: the stretches of the x axis where cos x > 0 GREEN, the rest RED with the tag "ln undefined"; the tag `\cos x > 0` joins the boxed answer.
> On {why}: the two boxed answers shrink to the top edge. On {grow}: the examples clear. A tree diagram: h at the top (BLUE: the outer function; not TEAL, which is only ever the step h), u and v in the middle row (PURPLE), x and y at the bottom; each edge labelled with its partial derivative (`\frac{\partial h}{\partial u}`, `\frac{\partial u}{\partial x}`, …). On {tree}, the tree draws top to bottom.
> On {routes}: the path x → u → h glows YELLOW, then x → v → h. On {terms}: the notes' formula builds one term per path: `\frac{\partial h}{\partial x} = \frac{\partial h}{\partial u}\frac{\partial u}{\partial x} + \frac{\partial h}{\partial v}\frac{\partial v}{\partial x}`, tagged "Chapter 7 of the notes · next term". On {curly}: every ∂ pulses once.

[c2.chex.1] {ex} Example thirty-seven starts with sine of ex squared. {outer} The outer function is sine, of an inner function, G, which is ex squared. {cos} Differentiating the outer function gives cosine of G. {inner} Multiply by the derivative of the inner one, which is two ex. {back} Put G back, and the answer is two ex, times cosine of ex squared.

[c2.chex.2] {log} The second one is the log of cosine of ex. {outerlog} The log is outside, and its derivative is one over its inside. {innercos} The cosine is inside, with derivative minus sine of ex. {tan} Multiply them, and you get minus sine over cosine, which is minus the tangent of ex. {caveat} And, as the lecturer stressed, cosine of ex must be positive, or the log is undefined. {pause}

[c2.chex.3] {why} Why go over this again? {pause} {grow} Because the chain rule grows, next term, and in Chapter seven of the notes. {tree} Take a function of two inner functions, each depending on ex and why. {routes} Now there are two routes from ex up to the top, one through each inner function. {terms} Each route gives one chain-rule term, and the two terms add. {curly} The rounded symbols mark partial derivatives, which come later.

## Scene 5 · The product rule (ch2_s5_product)

> On {setup}, top: `y(x) = f(x)\,g(x)`, f BLUE, g PURPLE. On {def}: `\frac{dy}{dx} = \frac{d}{dx}(fg) = \lim_{h \to 0}`, with the step h TEAL (part one's box used h too). On {top}, the numerator `f(x+h)g(x+h) - f(x)g(x)`; on {over}, the denominator `h`.
> On {trick}: the notes' second line, with `- f(x+h)g(x) + f(x+h)g(x)` slotted into the middle of the numerator, framed YELLOW (the notes print this pair purple; here PURPLE is g's colour). On {nothing}: the two framed terms flash and a small "= 0" tag appears under them.
> On {regroup}: the notes' third line, `= \lim_{h \to 0}\left[f(x+h)\,\frac{g(x+h) - g(x)}{h} + \frac{f(x+h) - f(x)}{h}\,g(x)\right]`. On {first}, terms one and two slide together and f(x+h) lifts out in front; on {second}, terms three and four slide together and g(x) lifts out behind.
> On {limit}: `h \to 0` (TEAL). On {quot}: the g-quotient becomes `g'` and the f-quotient `f'`, both GREEN. On {shift}: f(x+h) is outlined YELLOW and becomes f(x). On {careful}: part one's differentiability box, small in the corner, with "(a) the function must be continuous" lit, as in scene 3.
> On {result}: `= f'g + fg'`, then (106) boxed YELLOW: `\frac{d}{dx}(fg) = \frac{df}{dx}\,g + f\,\frac{dg}{dx}`, tag "product rule".
> On {rect}: the derivation shrinks left. Right: a rectangle, width f (BLUE side), height g (PURPLE side), labelled "area fg". On {grow}: it widens by δf and rises by δg (TEAL edges); the right strip `g\,\delta f` and the top strip `f\,\delta g` fill in lightly. On {corner}: the small corner square `\delta f\,\delta g` blinks and fades out. On {strips}: arrows from the two strips to the two terms of (106).
> On {ex}: card "Example 38: Product rule", `y = \ln x \sin x`, `f(x) = \ln x` (BLUE), `g(x) = \sin x` (PURPLE). On {f}: `f' = \frac{1}{x}`; on {g}: `g' = \cos x`. On {answer}: `\frac{dy}{dx} = f'g + fg' = \frac{1}{x}\sin x + \ln x \cos x`, boxed YELLOW: the hook's question answered. On {pos}: the tag `x > 0`.

[c2.prod.1] {setup} Next, the product rule, for F of ex, times G of ex, where we can differentiate each factor on its own. {def} Start from the definition, with a step H. {top} On top goes the change in the product. That's F times G at ex plus H, minus F times G at ex. {over} Underneath goes the step H.

[c2.prod.2] {trick} Here's the trick this time. Subtract a mixed term, F at ex plus H, times G at ex, and add it straight back. {nothing} Nothing has changed. {regroup} Now regroup the four terms in pairs. {first} The first pair shares F at ex plus H, and what's left is the chord slope for G. {second} The second pair shares G at ex, and what's left is the chord slope for F.

[c2.prod.3] {limit} Let the step H go to zero. {quot} The two chord slopes become G prime and F prime. {shift} And F at ex plus H becomes F at ex. {careful} The lecturer calls that the only non-trivial step. It needs F to be continuous, and part one's box says that a differentiable function is. {result} So the derivative of F times G is F prime times G, plus F times G prime. {pause}

[c2.prod.4] {rect} Here's a picture to remember it by. Take a rectangle with sides F and G, so its area is the product. {grow} Nudge ex, and the area gains two thin strips, one along each side, {corner} plus a tiny corner, the product of two small changes, which vanishes in the limit. {strips} The two strips are the rule's two terms.

[c2.prod.5] {ex} Example thirty-eight is the product from the start of this part, the log of ex, times sine of ex. {f} The first factor, the log, has derivative one over ex. {g} The second, sine, has derivative cosine. {answer} So the derivative is one over ex, times sine of ex, plus the log of ex, times cosine of ex, {pos} for ex positive, where the log exists.

## Scene 6 · The quotient rule (ch2_s6_quotient)

> On {setup}, top: `\frac{u}{v}`, u BLUE (labelled "top"), v PURPLE ("bottom"), with a YELLOW "new limit?" that is struck out as {split} begins. On {split}: `\frac{u}{v} = u \times \left(\frac{1}{v}\right)`. On {apply}: (106)'s tag flashes; `\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{du}{dx} \times \left(\frac{1}{v}\right) + u\,\frac{d}{dx}\left(\frac{1}{v}\right)`.
> On {chain}: an aside under it, (105)'s tag flashing: `\frac{d}{dx}\left(\frac{1}{v}\right) = \frac{d}{dv}\left(\frac{1}{v}\right)\frac{dv}{dx} = -\frac{1}{v^2}\,\frac{dv}{dx}`; on {inner}, the dv/dx lights. On {common}: the aside slots back into the line, both terms over v². On {result}: (107) boxed YELLOW, `\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{v\,\frac{du}{dx} - u\,\frac{dv}{dx}}{v^2}`, tag "quotient rule".
> On {ex}: card "Example 39: Quotient rule", `y = \frac{\sin x}{x}` (sin x BLUE, x PURPLE), tag `x \neq 0`; two columns. On {quot}, left: `\frac{dy}{dx} = \frac{f'g - fg'}{g^2} = \frac{(\cos x)\,x - (\sin x)(1)}{x^2} = \frac{x\cos x - \sin x}{x^2}`. On {prod}, right: `y = \sin x \cdot \frac{1}{x}` (1/x PURPLE; the notes call it h, shown here as 1/x because h is the TEAL step in this series), `\frac{dy}{dx} = (\cos x)\left(\frac{1}{x}\right) + (\sin x)\left(-\frac{1}{x^2}\right)`. On {same}: the right column gathers to `\frac{x\cos x - \sin x}{x^2}` and a GREEN "=" joins the two answers. On {forget}: small tiles "product rule" + "chain rule" → "quotient rule".
> On {tan}: the table from scene 2 returns small, block 3 lit. On {tanq}: `\frac{d}{dx}\tan x = \frac{d}{dx}\frac{\sin x}{\cos x} = \frac{\cos x\cos x - \sin x(-\sin x)}{\cos^2 x} = \frac{\cos^2 x + \sin^2 x}{\cos^2 x}` (sin x BLUE, cos x PURPLE). On {sec}: the numerator turns YELLOW and becomes 1: `= \frac{1}{\cos^2 x} = \sec^2 x`. On {tanh}: `\frac{d}{dx}\tanh x = \frac{\cosh^2 x - \sinh^2 x}{\cosh^2 x} = \mathrm{sech}^2 x`. On {const}: `\frac{d}{dx}\tan(ax) = a\sec^2(ax)` with the a YELLOW, and the table's tan and tanh rows light GREEN. All checked with sympy 1.14.

[c2.quot.1] {setup} Do we need a new limit for the quotient rule? {pause} No. {split} Write the top over the bottom as the top, times one over the bottom. {apply} The product rule gives the derivative of the top, times one over the bottom, plus the top, times the derivative of one over the bottom.

[c2.quot.2] {chain} For that last derivative, use the chain rule. The outer function is one over something, with derivative minus one over its square. {inner} Multiply by the derivative of the bottom. {common} Now put both terms over a common denominator, the bottom squared. {result} That's the quotient rule. The bottom, times the derivative of the top, minus the top, times the derivative of the bottom, all over the bottom squared. {pause}

[c2.quot.3] {ex} Example thirty-nine is sine of ex, over ex, for ex different from zero. {quot} The quotient rule gives ex times cosine of ex, minus sine of ex, all over ex squared. {prod} Or use the product rule on sine of ex, times one over ex. That gives cosine of ex over ex, minus sine of ex over ex squared. {same} Over a common denominator, that's the same answer. {forget} Forget the quotient rule, the lecturer said, and you can rebuild it from the other two.

[c2.quot.4] {tan} Now the promise from the table. {tanq} The tangent of ex is sine over cosine, so the quotient rule gives cosine squared, plus sine squared, all over cosine squared. {sec} The top is one, so the derivative is one over cosine squared, which is secant squared. {tanh} For tanch, the top is cosh squared minus shine squared, also one, so its derivative is hyperbolic secant squared. {const} And a constant inside comes out in front, by the chain rule, as in every row.

## Scene 7 · Recap (ch2_s7_recap)

> Four small panels (2 × 2), each a miniature of the visual that taught it, same objects and colours, with its sentence's short line under it; each lights on its mark while the others dim.
> On {r1}, from scene 2: the derivative table thumbnail, with the GOLD `e^{iax}` line (i PINK) beside it. Line: "basic derivatives; the rest from e^{ax}".
> On {r2}, from scene 3: the two-bracket line with its TEAL δu, and the boxed (105) (f BLUE, u PURPLE). Line: "chain rule: × and ÷ by δu".
> On {r3}, from scene 5: the numerator with the YELLOW-framed pair `- f(x+h)g(x) + f(x+h)g(x)`, and the rectangle with its two strips. Line: "product rule: subtract, add back".
> On {r4}, from scene 6: `\frac{u}{v} = u \times \left(\frac{1}{v}\right)` (u BLUE, v PURPLE) above the boxed (107). Line: "quotient rule: u × 1/v".
> On {sheet}: the panels shrink to a strip at the top; a sheet card "Examples Sheet I · H1, H2 · answers on p. 15", in the series' question-card style (ch3 s7 sets it: a rounded rectangle with a DIM border, the label "H1 · H2" in YELLOW at the top left, white text). This card shows excerpts only; the full verbatim H1 and H2 cards are built in ch7 s1. On {h1}: H1(e) `\frac{d}{dt}\left(at + bt^2\sin\theta\right)` and H1(g) `\frac{d}{dy}\,\frac{1}{1+y}`, the t of d/dt and the y of d/dy YELLOW, θ tagged "constant". On {h2}: a few H2 functions with "write in exponentials"; on {omega}, H2(d) `\frac{d}{d\omega}\sin(-i\omega t)` with ω YELLOW and i PINK.
> On {next}: the strip and card clear; part three's circle `y^2 = 9 - (x-1)^2` (owner ch3_s1_hook / ch3_s3_circle: BLUE, centre (1, 0), radius 3, equal-unit axes) on small axes, with the dashed vertical line at x = 2.8. On {circle}: the two points, (2.8, 2.4) and (2.8, −2.4), light YELLOW and their two GREEN tangent lines draw in.
> End card: hold for about eight seconds after the last word; the music carries it.

[c2.recap.1] {recap} Time for a recap. {r1} A short table covers the basic functions, and the rest comes from the exponential. {r2} The chain rule: multiply and divide by the change in the inner function. {r3} The product rule: subtract a mixed term, and add it back. {r4} The quotient rule: write the top, times one over the bottom. {pause}

[c2.recap.2] {sheet} Now try questions H one and H two, on the first examples sheet. The answers are on its last page. {h1} In H one, check which letter you're differentiating with respect to. In two parts it's tee, or why, and other letters are constants. {h2} In H two, write each function with exponentials, as we did in this part. {omega} In the one with omega, the variable is omega, not tee. {pause}

[c2.recap.3] {next} Next time: equations that don't hand you why as a formula in ex. {circle} We'll start with a circle, which has two values of why for most ex, and so two tangent lines. {pause}
