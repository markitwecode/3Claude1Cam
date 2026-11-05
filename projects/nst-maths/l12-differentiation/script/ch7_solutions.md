# Chapter 7 · Solutions: Examples Sheet H1, H2, H4 and I1

NST IA Mathematics · Lecture 12 (Differentiation), part 7 of 7 (bonus, for after the questions). Source: Examples Sheet I pp. 10–11 (H1, H2, H4, I1) and p. 15 (printed answers, H1 and H2 only; H4 and I1 were derived and checked with sympy 1.14), drawing on notes pp. 50–51 (§4.2 tables), 54–55 ((106), (107)), 58 ((111)) and 60–62 (Leibniz).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Spoilers ahead (ch7_s1_intro)

> {title} Title card: "Differentiation", "NST IA Mathematics · Lecture 12", "Part 7 · Solutions: Examples Sheet H1, H2, H4 and I1", with a small "Bonus" tag styled as L11's part 7. On {last}: part six's labelled figure, small (owner ch6_s1_hook for the curve, y′ = (x + 2)(x + ½)(x − 3/2)²; labels as ch6_s2_vocab places them: "local maximum", "local minimum", "point of inflection" with two arrows, "(rising) stationary point of inflection"; YELLOW dots), then it fades.
> On {warn}: a "SPOILERS AHEAD" banner with a large pause icon (‖), held through the pause.
> On {cards}: four question cards in a row, all in the series' question-card style (set by ch3 s7: a rounded rectangle with a DIM border, the label in YELLOW at the top left, the sheet's text verbatim in white, course colours only inside the maths). H4 is ch3_s7_recap's card and I1 is ch5_s7_recap's card, text unchanged. ch2 s7 showed only a combined "H1 · H2" excerpt card, so this scene builds the full verbatim H1 and H2 cards (text as s2 quotes it) in the same style. They light on their marks: {h12} H1 and H2 together, then {h4}, then {i1}. On {later} two dim cards "H3" and "H5" slide off to the right under the tag "next lecture: curve sketching".
> On {ritual}, small chips under the row: "pause ‖", "solution"; on {mistake} a RED ✗ chip "the tempting mistake".
> Each later scene opens with its card grown from this row to the hero position (TransformFromCopy) plus the ‖ icon, held still through the pause.

[c7.intro.1] {title} This is part seven of Differentiation, a bonus, with worked solutions to the questions from the examples sheet that this lecture covers. {last} Last time, derivatives told maxima, minima and points of inflection apart. {warn} From here on, everything is a spoiler. If you have not tried the questions yet, pause now, and have a go. {pause}

[c7.intro.2] {cards} There are four questions, from sections H and I of the first examples sheet. {h12} H one and H two, the basic skills. {h4} H four, one derivative by two routes. {i1} And eye one, Leibniz's formula on a Gaussian. {later} H three and H five go with curve sketching, in the next lecture. {ritual} For each, you get the card and a pause, then the solution, {mistake} and the mistake that's easy to make.

## Scene 2 · H1 and H2: the basic skills (ch7_s2_basics)

> On {table}: ch2 s2's §4.2 table, small, at the left (same layout and styling, e^{ax} rather than exp(ax); rows x^a | ax^{a−1}, e^{ax} | ae^{ax}, ln(ax) | 1/x, sin(ax) | a cos(ax), cos(ax) | −a sin ax, sinh(ax) | a cosh(ax), cosh(ax) | a sinh ax, tan ax | a sec² ax, tanh ax | a sech² ax). At the right the H1 card from s1, verbatim: "H1. Calculate the following derivatives:" (a) d/dx (x² + 3) (b) d/dx (x⁴ + 2x + 6) (c) d/dx (axⁿ + bx + c) (d) d/dx e^x (e) d/dt (at + bt² sin θ) (f) d/dx (1 + x^{2/3}) (g) d/dy 1/(1 + y) (h) d/dx ln x.
> On {printed}: the sheet's p. 15 answers drop in under each part, GREEN, verbatim: "H1. (a) 2x; (b) 4x³ + 2; (c) anx^{n−1} + b; (d) e^x; (e) a + 2bt sin θ; (f) 2x^{−1/3}/3; (g) −(1 + y)^{−2}; (h) 1/x". On {power} the table's first row x^a → ax^{a−1} glows, with thin lines to (a), (b), (c), (f).
> Three parts enlarge in turn. On {time} (e): t YELLOW, tagged "variable"; θ and sin θ dim, tagged "constant"; → a + 2bt sin θ. On {frac} (f): d/dx x^{2/3} = (2/3)x^{2/3 − 1} = (2/3)x^{−1/3}, which matches the printed 2x^{−1/3}/3. On {wy} (g): y YELLOW "variable"; 1/(1 + y) = (1 + y)^{−1} → −(1 + y)^{−2}.
> On {exps}: the H2 card replaces H1, verbatim: "H2. By writing the trigonometric and hyperbolic functions in terms of exponentials, evaluate the following derivatives:" (a) d/dx sin x (b) d/dθ cos θ (c) d/dt tan t (d) d/dω sin(−iωt) (e) d/dx sinh x (f) d/dx cosh x (g) d/dx tanh x (h) d/dx tanh 2x. Its p. 15 answers sit under its parts, verbatim: "H2. (a) cos x; (b) − sin θ; (c) sec² t; (d) −it cos(−iωt); (e) cosh x; (f) sinh x; (g) sech² x; (h) 2sech² 2x". The table's rows sin … tanh get empty tick boxes; each derivation below ticks its row and its printed answer.
> On {sin}: sin x = (e^{ix} − e^{−ix})/(2i), e^{ix} GOLD, e^{−ix} PURPLE, i PINK (course colours). On {down}: (i e^{ix} − (−i) e^{−ix})/(2i), the factors i and −i flashing PINK. On {cancel}: → (e^{ix} + e^{−ix})/2 = cos x; the table's sin row ticks GREEN. On {rest} the cos, sinh, cosh rows tick in turn: cos θ → −sin θ; ½(e^x − e^{−x}) → ½(e^x + e^{−x}), and back (GOLD and PURPLE, as in ch2 s2).
> On {tanh}: tanh x = (e^x − e^{−x})/(e^x + e^{−x}), tagged "top" and "bottom". On {swap} two curved arrows: top′ = bottom, bottom′ = top. On {qrule}: ch2 s6's quotient rule (107), (v u′ − u v′)/v², fills in as (bottom² − top²)/bottom². On {four}: (e^{2x} + 2 + e^{−2x}) − (e^{2x} − 2 + e^{−2x}) = 4; bottom = 2 cosh x; 4/(2 cosh x)² = 1/cosh² x = sech² x; the tanh row ticks. On {tan}: tan t = (e^{it} − e^{−it})/(i(e^{it} + e^{−it})) → sec² t, the tan row ticks. On {chain}: tanh 2x → 2 sech² 2x, the chain rule's 2 YELLOW.
> On {omega}: d/dω sin(−iωt), ω YELLOW "variable", t dim "constant". On {dict}: i·(−iωt) = ωt, so sin(−iωt) = (e^{ωt} − e^{−ωt})/(2i) = sinh(ωt)/i = −i sinh(ωt) (GOLD/PURPLE exponentials, i PINK). On {wrt}: → −it cosh(ωt), boxed YELLOW. On {printed2}: the printed answer "−it cos(−iωt)" beside it, joined by cos(−iωt) = cosh(ωt). On {slip}: a RED −iω cosh(ωt), tagged "d/dt: the wrong variable".
> Checked with sympy 1.14: every H1 answer (d/dt gives a + 2*b*t*sin(theta); (f) 2/(3*x**(1/3)); (g) -1/(y + 1)**2); H2 from the exponential forms: sin → cos(x), cos → -sin(theta), tan t's derivative minus 4/(e^{it} + e^{−it})² and minus sec² t both simplify to 0, bottom² − top² expands to 4, tanh's derivative minus sech² x simplifies to 0, d/dx tanh 2x = 2 − 2 tanh² 2x = 2 sech² 2x; sin(−iωt) in exponentials is −i e^{ωt}/2 + i e^{−ωt}/2 = −i sinh(ωt); d/dω gives -I*t*cosh(omega*t), d/dt gives -I*omega*cosh(omega*t); cos(−iωt) = cosh(omega*t).

[c7.basics.1] {table} H one and H two are the basic skills, and their answers are printed on the last page of the sheet. {printed} Here they are. {power} Most of H one is the power rule, the first row of the table from part two. Three of them are worth a second look.

[c7.basics.2] {time} In the one with theta, the variable is time, T. Theta is a constant, so sine of theta is just a number. {frac} For one plus ex to the two thirds, the power rule works with a fractional power: two thirds, times ex to the minus one third. {wy} In the next one, the variable is why. One over, one plus why, is one plus why, to the power minus one. So its derivative is minus, one plus why, to the power minus two.

[c7.basics.3] {exps} H two says how: write each function with exponentials. {sin} Sine of ex is E to the eye ex, minus E to the minus eye ex, all over two eye. {down} Differentiating brings down eye from the first exponent, and minus eye from the second. {cancel} The eye cancels the one underneath, the two minus signs make a plus, and what's left is cosine of ex. {rest} Cosine goes the same way, to minus sine. Shine differentiates to cosh. Cosh differentiates to shine.

[c7.basics.4] {tanh} Tanch is a quotient: E to the ex, minus E to the minus ex, over their sum. {swap} The top differentiates to the bottom, and the bottom to the top. {qrule} So the quotient rule gives the bottom squared, minus the top squared, over the bottom squared. {four} The squares differ by four, and the bottom is twice cosh of ex, so that's one over cosh squared, the hyperbolic secant squared. {tan} Tangent goes the same way, to secant squared. {chain} For tanch of two ex, the chain rule adds a factor of two.

[c7.basics.5] {omega} The last trap: sine of minus eye omega T, differentiated with respect to omega. {dict} In exponential form, eye times minus eye omega T is just omega T, so the sine is shine of omega T, over eye. That's minus eye, times shine of omega T. {wrt} Differentiating with respect to omega brings down a T: minus eye T, times cosh of omega T. {printed2} That's the printed answer, since cosine of minus eye omega T is cosh of omega T. {slip} Differentiate with respect to T by mistake, and you get omega in place of T.

## Scene 3 · H4, the first route: x as a function of y (ch7_s3_h4_one)

> On {card}: card H4 grown from s1's row (the card from ch3 s7's hint), verbatim: "H4. Find dy/dx if y + e^y sin y = 1/x by: i. expressing x as a function of y and then finding dx/dy; and ii. differentiating the original expression with respect to x. (Your answers should agree!)". {first} and {second} light the "i." and "ii." lines; {agree} lights "(Your answers should agree!)" YELLOW. The ‖ icon on {stop}, held through the pause.
> Colours for s3–s4: e^y GOLD (the course's exponential colour); the left side y + e^y sin y in a BLUE box; its derivative with respect to y, 1 + e^y(sin y + cos y), in a GREEN box (the derivative); every y′ the chain rule makes YELLOW (s4); slips RED. A route label at the top left: "route i: x as a function of y".
> On {flip}: the equation y + e^y sin y = 1/x; both sides turn upside down → x = 1/(y + e^y sin y), the left side in its BLUE box as the bottom of the fraction. On {alone} the box gets the tag "no x: a function of y alone".
> On {dxdy}: d/dy (1/□) = −□′/□², tagged "chain rule, part 2". On {prod}: d/dy y = 1, and d/dy (e^y sin y) = e^y sin y + e^y cos y, the two product-rule terms lighting one after the other ((106), as in ch2 s5); a small RED ✗ beside a lone "e^y cos y": "the product rule gives two terms". On {dp}: the GREEN box 1 + e^y(sin y + cos y); the line reads dx/dy = −(1 + e^y(sin y + cos y))/(y + e^y sin y)².
> On {recip}: ch3 s6's small swapped-axes picture (Figure 29 reflected in y = x) with (111), dx/dy = 1/(dy/dx), and the fraction turning upside down. On {answer1}: dy/dx = −(y + e^y sin y)²/(1 + e^y(sin y + cos y)), boxed YELLOW, labelled "route i". On {only_y} its y's flash: no x in it. It shrinks to the upper left and stays there for s4.
> Checked with sympy 1.14: diff(1/(y + exp(y)*sin(y)), y) prints (-exp(y)*sin(y) - exp(y)*cos(y) - 1)/(y + exp(y)*sin(y))**2; its reciprocal minus −(y + e^y sin y)²/(1 + e^y(sin y + cos y)) simplifies to 0.

[c7.h4one.1] {card} Question H four. The equation is why, plus E to the why, times sine of why, equals one over ex. Find the derivative of why with respect to ex, two ways. {first} First, write ex as a function of why. {second} Second, differentiate the equation as it stands. {agree} The sheet adds that your answers should agree. {pause} {stop} Pause here, and try both routes. {pause=1.5}

[c7.h4one.2] {flip} The first route. Ex appears only once, in one over ex, so turn both sides upside down. Now ex is one over the left side. {alone} The left side, why, plus E to the why, times sine of why, has no ex in it. So ex is a function of why alone.

[c7.h4one.3] {dxdy} Differentiate with respect to why. One over something gives minus its derivative, over its square: the chain rule from part two. {prod} For the left side's derivative, the why term gives one, and E to the why, times sine of why, needs the product rule. Both factors change, so it gives two terms, one with sine of why, and one with cosine of why. {dp} Altogether, one, plus E to the why, times the sum of sine and cosine of why.

[c7.h4one.4] {recip} Now the reciprocal rule from part three. Turn the derivative of ex with respect to why upside down. {answer1} The derivative of why with respect to ex is minus the left side squared, over the left side's derivative. {only_y} Notice that it's written in why alone. Keep it in view.

## Scene 4 · H4, the second route, and why they agree (ch7_s4_h4_two)

> Route i's boxed answer stays small at the upper left. At the centre, the original equation y + e^y sin y = 1/x, the route label now "route ii: differentiate as it stands".
> On {second}: d/dx applied to both sides; y gets the tag "y = y(x)". On {chain}: every function of y grows a YELLOW y′. On {terms}: y → y′; e^y sin y → e^y y′ sin y + e^y cos y · y′ (each term with its YELLOW y′); on {rhs}: 1/x → −1/x².
> On {collect}: the three y′ terms slide together and y′ comes out: y′(1 + e^y(sin y + cos y)) = −1/x². On {same} the bracket gets route i's GREEN box (TransformFromCopy from route i's denominator), tagged "same as route i". On {answer2}: dy/dx = −1/(x²(1 + e^y(sin y + cos y))), boxed YELLOW, labelled "route ii".
> On {compare}: the two boxed answers side by side, their GREEN bottoms aligned. On {look} their tops light: (y + e^y sin y)² against 1/x². On {orig}: the original equation drops in between them, its BLUE box matching route i's top. On {square} it squares to (y + e^y sin y)² = 1/x², the two tops lock together, and a GREEN ✓ "the answers agree" ticks the card's "(Your answers should agree!)".
> On {slip}: route ii again, the y′ beside both e^y terms struck RED: y′ + e^y sin y + e^y cos y = −1/x² → y′ = −1/x² − e^y(sin y + cos y), RED. On {test}: at y = ½ (x ≈ 0.775), the right answer ≈ −0.514 (GREEN) against the wrong ≈ −3.90 (RED), with a RED ✗ on the card's "(Your answers should agree!)".
> On {fail}: both GREEN bottoms flash. On {curve}: the curve's branch with 0 < y < 3.267, x = 1/(y + e^y sin y), plotted BLUE (stretch the x axis so the left end is visible): it comes in from the right just above the x axis (y ≈ 0.406 at x = 1), runs left to a tip at (0.1015, 2.419), and goes back out to the right towards the dashed line y = 3.267 (y ≈ 3.230 at x = 1). YELLOW dot at the tip. On {vertical}: a RED vertical tangent line at the tip, tagged "dx/dy = 0: no finite dy/dx", beside ch3 s6's cube-root picture, small.
> Checked with sympy 1.14 (mpmath for the roots): implicit differentiation gives y′ = −1/(x²(1 + e^y(sin y + cos y))) (sympy prints the bracket as sqrt(2)*exp(y)*sin(y + pi/4) + 1); with x = 1/(y + e^y sin y) it equals route i (difference 0); the dropped-y′ version gives −3.9026 against −0.5144 at y = ½ (x = 0.7749); 1 + e^y(sin y + cos y) first vanishes at y = 2.41917 (x = 0.101535) and stays positive for y ≤ 0; y + e^y sin y = 0 again at y = 3.26650.

[c7.h4two.1] {second} The second route. Differentiate both sides with respect to ex, remembering that why depends on ex. {chain} So every function of why picks up a factor, why prime, from the chain rule. {terms} The why term gives why prime. E to the why, times sine of why, gives the same two terms as before, each now carrying a why prime. {rhs} On the right, one over ex gives minus one over ex squared.

[c7.h4two.2] {collect} Every term on the left now has a why prime, so take it out. {same} What's left in the bracket is the left side's derivative, the same as in the first route. {answer2} So why prime is minus one over ex squared, divided by that bracket.

[c7.h4two.3] {compare} The two answers have the same bottom. {look} But the first has the left side squared on top, and the second has one over ex squared. Are they really equal? {pause} {orig} The original equation says that the left side is one over ex. {square} Square it, and the two tops match. So the answers agree, as the sheet promised.

[c7.h4two.4] {slip} The tempting mistake: treating E to the why as if why were the variable, and dropping its why prime. {test} Then the routes disagree. At why equals a half, the correct slope is about minus a half, and the wrong one about minus four. That's what the sheet's reminder is for.

[c7.h4two.5] {fail} One last thing. Both answers divide by the left side's derivative. {curve} Here's the curve where that's zero, near why equals two point four. {vertical} There the derivative of ex with respect to why is zero, the tangent line is vertical, and the reciprocal rule fails, as it did for the cube root in part three.

## Scene 5 · I1: Leibniz on a Gaussian (ch7_s5_i1)

> On {card}: card I1 grown from s1's row (the card from ch5 s7's hint), verbatim except for the series' spelling "Leibniz" (the sheet prints "Leibnitz's"): "I1. Use Leibniz's formula to establish that Z_n ≡ d^n/dx^n e^{−x²/2} is a solution of the differential equation d²Z_n/dx² + x dZ_n/dx + (n + 1)Z_n = 0." The ‖ icon on {stop}, held through the pause.
> Colours as ch4–ch5: x, the first function, BLUE; g = e^{−x²/2} and its derivatives (so every Z) PURPLE; binomial coefficients YELLOW, and the equation's (n + 1) YELLOW too.
> On {gauss}: g = e^{−x²/2} beside a small PURPLE bell curve; Z_n = g^(n). On {key}: g′ = −x g, boxed; on {runs} the BLUE x tagged with its chain "x → 1 → 0".
> On {count}: Z_n″ = g^(n+2) = (g′)^(n+1), the one derivative already in g′ ticked. On {left}: d^{n+1}/dx^{n+1} applied to both sides of g′ = −x g; the left side becomes g^(n+2) = Z_n″. On {right}: the right side becomes −(x g)^(n+1).
> On {leibniz}: ch4 s4's Leibniz sum card with n + 1 for n: (x g)^(n+1) = Σ_{m=0}^{n+1} (n+1 choose m) x^(n+1−m) g^(m). On {row}: a sample row of Pascal's triangle, row 5 (1 5 10 10 5 1), dim. On {survive}: every term with x differentiated twice or more fades with a RED "0", and only the row's last two entries (5, 1) stay lit YELLOW, as ch5 s4 lit two. On {last}: m = n + 1: (n+1 choose n+1) · x · g^(n+1) = x Z_n′. On {before}: m = n: (n+1 choose n) · 1 · g^(n) = (n + 1) Z_n, the (n + 1) YELLOW.
> On {assemble}: Z_n″ = −x Z_n′ − (n + 1) Z_n. On {move} the terms move left: Z_n″ + x Z_n′ + (n + 1)Z_n = 0, boxed YELLOW, matched against the card's equation. On {coef} the YELLOW (n + 1) links back to (n+1 choose n). On {slip}: a RED variant "differentiate only n times: Z_{n−1}″ + x Z_{n−1}′ + n Z_{n−1} = 0", tagged "the equation for Z_{n−1}".
> On {check}: n = 0. On {z0}: Z_0 = g, Z_0′ = −x g, Z_0″ = (x² − 1)g. On {sum}: (x² − 1) − x² + 1 = 0, GREEN ✓. On {same}: ch5 s4's step, small, beside this one: d^n/dx^n (x e^{−x²}) with its two lit entries.
> Checked with sympy 1.14: g′ + x g simplifies to 0; Z_n″ + x Z_n′ + (n + 1)Z_n = 0 for n = 0 … 7; for n = 0 … 5 only the last two Leibniz terms of (x g)^(n+1) are non-zero, and (x g)^(n+1) = x Z_{n+1} + (n + 1)Z_n; Z_0″ prints (x - 1)*(x + 1)*exp(-x**2/2); differentiating n times gives the equation for Z_{n−1} (n = 1 … 4), and Z_n does not satisfy it with n in place of n + 1; row 5 is 1, 5, 10, 10, 5, 1.

[c7.i1.1] {card} Question eye one. Zed N is the Nth derivative of E to the power minus ex squared over two. Use Leibniz's formula to show that zed N double prime, plus ex times zed N prime, plus N plus one, times zed N, equals zero. {pause} {stop} Pause, and try it. {pause=1.5}

[c7.i1.2] {gauss} Call the Gaussian G, so zed N is G differentiated N times. {key} The key fact: by the chain rule, G prime is minus ex, times G. {runs} And ex runs out of derivatives fast: it gives one, and then zero.

[c7.i1.3] {count} How many times should you differentiate? Zed N double prime is G differentiated N plus two times, and G prime already takes care of one. {left} So differentiate both sides of the key fact N plus one times. The left side becomes zed N double prime. {right} The right side is minus ex times G, differentiated N plus one times.

[c7.i1.4] {leibniz} That's Leibniz's formula, with ex as the first function, and G as the second. {row} Its coefficients are row N plus one of Pascal's triangle. {survive} But any term that differentiates ex twice or more is zero, so only the last two survive. {last} The last is ex, times G differentiated N plus one times: ex times zed N prime. {before} In the one before, ex is differentiated once, to one, and the coefficient, N plus one choose N, is N plus one. That term is N plus one, times zed N.

[c7.i1.5] {assemble} So zed N double prime equals minus ex times zed N prime, minus N plus one, times zed N. {move} Bring everything to the left, and that's the equation. {pause} {coef} The N plus one in it is that binomial coefficient. {slip} Differentiate only N times, and you get N in its place: the right equation, but for zed N minus one.

[c7.i1.6] {check} Check it with N equal to zero. {z0} Zed zero is G, its derivative is minus ex, times G, and its second derivative is ex squared minus one, times G. {sum} So the equation gives ex squared minus one, minus ex squared, plus one, all times G. That's zero. {same} Part five proved the Hermeet recursion with the same trick.

## Scene 6 · Recap (ch7_s6_recap)

> On {recap}: five small panels in a row, each lit on its sentence with its short line under it, the same objects and colours as the scenes they come from.
> On {r1}: s2's §4.2 table with its GREEN ticks, and beside it s2's line sin x = (e^{ix} − e^{−ix})/(2i) (GOLD, PURPLE, PINK i): "trig and hyperbolic: from exponentials". On {r2}: s2's three YELLOW "variable" tags, t, y and ω, each on its derivative: "check the variable".
> On {r3}: s4's two boxed answers with their shared GREEN bottom, the squared original equation (y + e^y sin y)² = 1/x² locking the tops: "two routes, one answer". On {r4}: s4's e^y with its YELLOW y′, and the struck RED one beside it: "every function of y carries a y′".
> On {r5}: s5's Leibniz card with only its last two terms lit and the YELLOW (n + 1): "x runs out: two terms survive".
> On {next}: the panels shrink away; "Next lecture: curve sketching (§4.11)", with s1's dim H3 and H5 cards sliding back in, and a small copy of ch6's labelled figure. On {end}, and after the last word, hold an end card for about 8 seconds (music carries it).

[c7.recap.1] {recap} Time for a recap. {r1} For H one and H two, every trig and hyperbolic derivative in the table comes from exponentials. {r2} Before you differentiate, check which letter is the variable. {r3} For H four, the two routes give one answer, once you use the original equation. {r4} The chain rule puts a why prime on every function of why. {r5} And for eye one, differentiate the fact that G prime is minus ex, times G, with Leibniz, and only two terms survive. {pause}

[c7.recap.2] {next} Next time, curve sketching, which puts the stationary points of part six to work, along with H three and H five. {end} Well done for working through these.
