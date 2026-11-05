# Differentiation: plan

Request: "make the next math lecture (in my downloads)", via the producer, 2026-11-03. Audience: a
Cambridge first-year natural scientist studying NST IA Mathematics, Course B (Mathematical Methods I,
N. G. Berloff). Knows A-level differentiation (the lecturer calls Chapter 4 "a review of what you
had in A-level maths, not even further maths") and Lectures 1–11: complex numbers, e^{iθ} =
cos θ + i sin θ, the hyperbolic functions and their inverses, circles and conics. Has done supervision
3 (sheet sections D, E, F7–F12); sections H and I are still ahead. Sources: the Lecture 12 recording
(`../source/l12-lecture.transcript.md`; the digest is empty, Gemini was off, so the handwritten blanks
come from frames the planner read, listed in `project.json`), the notes
`../source/Chapter234_to_annotate.pdf` pp. 47–66, Examples Sheet I sections H and I
(`../source/M26examples1 (2).pdf`, pp. 10–11).
Total: 7 chapters (6 + a bonus solutions chapter), ~63.5 min of narration planned (~55 core + ~8.5 bonus).
With the house pacing that's ~76 min of video (~66 + ~10). The scripts came in at ~11,000 words, ~69 min
(each chapter 8–9% over its target, inside the ±10% band), so expect ~83 min of video.

## Conventions (all chapters)
- Reading the sources: each chapter lists its notes pages and transcript range. The notes' text layer
  garbles the maths: render the page (`pdftoppm -f N -l N -r 80 -png …`) to read a formula. Four
  blanks were filled by hand and L12's scan isn't posted: the Heaviside sketch and differentiability
  definition (p50), Example 41's working (pp. 57–58), Leibniz's pattern and formula (pp. 60–61) and the
  labels of the three graphs (p66). `project.json` (the `l12-lecture.mp4` source note) records what the
  frames show. Where you need a board drawing it doesn't describe, grab a frame:
  `ffmpeg -ss <t> -i ../source/l12-lecture.mp4 -frames:v 1 -vf scale=960:-2 <scratchpad>/f.jpg`.
- Lecture boundary: L12 covers §4 to §4.10 (notes pp. 47–66) and ends "next time: curve sketching"
  (§4.11, p66 on), so no chapter teaches §4.11 or Example 43.
- Notation as in the notes: δx, δy, δu for increments; h in the differentiability box and the product
  rule (the lecturer: "h is just a variable"); dy/dx, y′, f′, f″; the nth derivative d^n y/dx^n and
  f^(n) with brackets; binomial coefficient (n choose m) (C_n^m shown once, ch4); sin⁻¹, tan⁻¹ (said
  "inverse sine"); H(x) the Heaviside function; H_n the Hermite polynomials (ch5 only). On screen e^{ax}
  rather than exp(ax), as L11 did. "Leibniz" on screen (the notes mix "Leibnitz" in §4.9 and the sheet
  with "Leibniz" in the history box). "Point of inflection" (the notes allow "inflexion" too).
- Colours by meaning (engine palette; course-wide rules in `../COURSE.md`):
  - BLUE: the curve y(x) being differentiated, as the notes draw it (Figures 29, 30). In two-function
    rules, the first function: f of the product rule, the outer f of the chain rule, u of the quotient.
  - PURPLE: the second function (g; the inner u of the chain rule; v of the quotient). This agrees with
    the course's e^{−x} PURPLE: the second factor is e^{−x} in ch4's example, e^{−x²} in ch5 and
    e^{−x²/2} in I1.
  - GOLD: e^x, e^{ax}, e^{iax}, e^{x²} (course rule). In ch5 the GOLD e^{x²} cancels the PURPLE e^{−x²}.
  - TEAL: L12's own thread: the increment that shrinks to zero (δx, δy, δu, h) and the chord it makes.
    Nothing else is TEAL in L12, so hyperbolic function names (L11's TEAL) are white here.
  - GREEN: the tangent line and the derivative it gives, the limit we keep; the kept sign (cos y > 0,
    ch3).
  - YELLOW: attention, boxed results, binomial coefficients and Pascal's triangle, stationary points.
  - RED: where a derivative fails (the corner, the jump, a vertical tangent line, dy/dx = 0 in the
    reciprocal rule), rejected signs, pitfalls.
  - PINK: i only (ch2's e^{iax}; ch7's sin(−iωt)).
- Words: the line through two points of the curve is "the chord", never "secant" (that's sec x, in
  ch2). The line that touches is "the tangent line", always with "line"; tan x is "tangent of ex" or
  "the tangent function". Ex 41's angle range is "the range of inverse sine".
- Cross-references (the L11 rule): the videos are "part one" … "part seven", the title cards' word;
  "Chapter four of the notes" for the notes' chapters (Chapter five: limits; Chapter six: Taylor series,
  §6.3; Chapter seven: partial differentiation; §8.4.2: Pascal's rule). Sheet questions by name ("H four",
  "eye one", written so since "I one" can come out as "I won"); parts by content ("the first route").
- Recurring visuals: build once, reuse in the same style.
  - Figure 29, chord to tangent line: ch1 s2, ch1 recap; small in ch3 s6 (axes swapped) and ch6 s5
    (the tangent line as the linear approximation (113)).
  - The derivative-chain card for x³ (x³ → 3x² → 6x → 6 → 0): ch1 s3 gets the first link, ch4 s2 builds
    the chain, ch6 s4 sets it beside x⁴'s (x⁴ → 4x³ → 12x² → 24x → 24).
  - The corner (|x|) and the jump (H(x)): ch1 s5–s6 and recap.
  - The differentiability box: ch1 s6; cited in ch2 s3 and s5 (continuity), ch3 s3 (finite).
  - The §4.2 derivative table: ch2 s2, ch7 s2.
  - Example 40's circle (centre (1, 0), radius 3) with two tangent lines: ch3 s3, s6, recap.
  - Pascal's triangle and the Leibniz sum card: ch4 s3 builds rows 1–3 as on her board, ch4 s4 adds the
    row-0 "1" when it numbers the rows (rows 0–3 from then on: ch4 s7, recap, ch5 s1), ch5 s4 grows row 4,
    ch7 s5 shows row 5 alone. The sum card is ch4 s4's `(fg)^(n)` form: ch4 s5–s8, ch5 s1 and s4, ch7 s5.
  - Sheet question cards, one style series-wide (set by ch3 s7): rounded rectangle, DIM border, YELLOW
    label top left, the sheet's text verbatim in white, course colours only inside the maths. Owners: H4
    ch3 s7, I1 ch5 s7, full H1 and H2 ch7 s1 (ch2 s7 shows only an excerpt card); ch6 s7 and ch7 reuse.
  - The H_n ladder card (H0 … H4): ch5 s2, s6, recap.
  - The notes' stationary-point figure (p63): ch6 s1 owns the curve (y′ = (x + 2)(x + ½)(x − 3/2)²), ch6 s2
    the labels; previewed in ch5's recap, reused in ch6 s6–s7 and ch7. The row of three inflection graphs
    (p66), y = x³ + x, x³ and x³ − 3x: ch6 s6 and recap.

## Voice rules for formulas
The course rules in `../COURSE.md` apply (cosine/sine/tangent in full, "ex", "why", "zed", "E to the
ex", "log", capitals after a noun, no "solve", no "you'll", "Oiler", "Time for a recap"). L12's new
ones are proposed here, untested with the clone; ch1's voice run tests the derivative words, ch4's
"Leibniz", ch5's "Hermite". Copied to `../COURSE.md`, the master once QA corrects them.
- Derivatives by meaning where you can: "the derivative of why with respect to ex", "the second
  derivative". Read the symbol, "dee why by dee ex" or "dee by dee ex", only where the notation is the
  subject (ch1 s4, (110), (111)). Risk: "dee" heard as "the". Check ch1's QA before the rest is voiced.
- Primes: "F prime", "G double prime", "F triple prime"; y′ "why prime". f^(n) is "the Nth derivative
  of F"; f^(n−m) "F differentiated N minus M times".
- Increments: "delta ex", "delta why", "the change in the inner function". u and v are named by role
  ("the inner function", "the top", "the bottom"): a bare "U" is heard as "you". h is "the step H".
- H overload: the Heaviside function is always named ("the Heaviside step function"), never "H of ex"
  aloud, because ch1 s6's step is "H" too. "H N", "H three" are only the Hermite polynomials (ch5, ch7).
- Limits: "the limit, as delta ex goes to zero, of …"; "the left-hand limit", "the right-hand limit".
  |x| is "mod ex" (first use: "mod ex, the absolute value of ex").
- "N choose M", "N factorial"; Σ "the sum, from M equals zero to N, of …", then "the sum".
- Inverses: "inverse sine of …", "inverse tangent of ex"; never "sine to the minus one" (course rule).
  sec² "secant squared"; sech² "hyperbolic secant squared".
- Scope: "one plus ex squared, all to the power three over two"; "E to the minus ex squared";
  "E to the ex squared"; e^{−x²/2} "E to the power minus ex squared over two".
- Names (untested): "Leibniz" as written (fallback spelling "Libe-nits" if QA hears it wrong);
  Hermite written "Hermeet" (the physicists' her-MEET; fallback "Air-meet"); "Heaviside", "Newton",
  "Lagrange", "Pascal" as written; Euler is "Oiler" (course rule).
- "concave up", "concave down"; "rearrange for the derivative", not "solve for".

## Chapter 1 · What is a derivative?
Slug: ch1_first_principles · ~9 min · Source: notes pp. 47–50 (§4 intro and history box, §4.1 (103), Figure 29, x³, notation box, |x|, (104), the differentiability box; the p50 handwriting is in the frame notes); lecture 00:00–08:48
Goal: define the derivative as the limit of chord slopes, differentiate x³ from first principles, read
the notations, and say what "differentiable at x" demands, with |x| and the Heaviside function as the
two ways it fails.
Scenes:
- s1_hook · Hook (~50 s): title card. Last time (one sentence, Lecture 11): the hyperbolic functions,
  and the circles, ellipses and hyperbolas they draw. Chapter four of the notes is, the lecturer says,
  a review of A-level, so these videos rebuild it from the foundations and slow down on the parts people
  half-remember: implicit differentiation, Leibniz's formula, classifying stationary points. One
  sentence: functions of one variable only; differentiating h(x, y) in different directions (partial
  derivatives) comes in Chapter seven of the notes. Opening visual: a curve, a chord swinging into a
  tangent line. The question: what exactly is a derivative, and when does it fail to exist?
- s2_chord · From chord to tangent line (~100 s): Figure 29 built step by step: the point (x, y(x)), a
  second point at x + δx, the rise δy = y(x + δx) − y(x), the chord's slope δy/δx (TEAL). Let δx shrink:
  the chords turn into the tangent line (GREEN). Definition (103), boxed. Newton's idea divides zero by
  zero, which was controversial in the 17th century ("another mathematical crisis successfully
  resolved", the lecturer). The notes' filled blank: it's a linear operation: the derivative of a sum is
  the sum of the derivatives, and constants come out, because limits behave that way.
- s3_cube · x³ from first principles (~85 s): the lecturer's recipe: substitute, expand, subtract,
  divide, take the limit. (x + δx)³ = x³ + 3x²δx + 3x(δx)² + (δx)³; subtract x³; divide by δx:
  3x² + 3xδx + (δx)²; let δx → 0: 3x², as the rule ax^{a−1} says. The notes add "provided |δx| < 1 then
  1 > |δx| > |δx|² > …"; the lecturer says it isn't needed: each leftover term carries a factor δx, so
  it goes to zero anyway. Starts the x³ derivative-chain card (3x²).
- s4_notation · Notation, and who invented it (~70 s): the notes' history box: Newton (limits; his
  breakthrough 1665/66, published 1687) and Leibniz (published 1686; geometric arguments; the d/dx and
  ∫ we still use); the priority quarrel; Britain kept Newton's notation through the 18th century and
  fell behind; Newton's dot, ẋ for dx/dt, survives; Euler ("Oiler") wrote Df, D²f, Lagrange the primes
  f′, f″; similar ideas in India a couple of centuries earlier. The notation box: dy/dx, d/dx y, y′,
  y_x, y_{,x}, Dy, and u̇ for time (the lecturer: D later in the course). dy/dx is the operator d/dx
  acting on y. It looks like a quotient, and some manipulations will treat it like one, but it isn't one
  (this pays off in part three's reciprocal rule).
- s5_fail · A corner and a jump (~100 s): y = |x| (BLUE V): continuous, slope −1 on the left, +1 on the
  right; at the corner no single tangent line (chords from the right have slope +1, from the left −1),
  so the derivative doesn't exist at 0 (RED). The Heaviside step function (104): 0 for x < 0, 1 for
  x > 0. Conventions at 0 differ; draw the lecturer's: open circle at (0, 0), filled dot at (0, 1).
  Derivative 0 for every x ≠ 0, undefined at 0 (her board: dH/dx = 0 for x ≠ 0, undefined at x = 0).
  A chord from the left across the jump has slope 1/h, which grows without bound.
- s6_differentiable · What "differentiable" demands (~85 s): her handwritten definition: f is
  differentiable at x if the limit of (f(x + h) − f(x))/h as h → 0 exists and is finite. The notes'
  box: (a) f must be continuous; (b) f′ finite and defined, so the left-hand and right-hand limits
  (the two quotients in the box) are equal. Run both examples: |x| is continuous, but its one-sided
  limits are −1 and +1. The step looks flat on both sides (both pieces have slope 0: the lecturer's
  point at 08:15), but it isn't continuous, so the limit can't exist. Differentiable ⇒ continuous (if f′
  exists, δf → 0 as δx → 0), but not the other way round: |x|. "Finite" matters too: a vertical tangent
  line has no finite slope (part three's circle has two).
- s7_recap · Recap (~50 s): small Figure 29 → "derivative = limit of chord slopes"; the x³ algebra →
  "first principles: expand, subtract, divide, limit"; the V and the step side by side → "a corner or a
  jump: no derivative"; the box → "differentiable: continuous, both sides agree, finite". Next: the
  chain, product and quotient rules, each from this same limit. End card.
Continuity: builds Figure 29, the x³ card, the corner and jump, and the differentiability box for the
series. TEAL increments and the GREEN tangent line start here. Assumes the informal idea of a limit
(Chapter five of the notes does limits properly; say so once in s2).

## Chapter 2 · The rules, from first principles
Slug: ch2_rules · ~9.5 min · Source: notes pp. 50–55 (§4.2 tables; §4.3 derivation, (105), Example 37, two-variable chain rule; §4.4 derivation, (106), Example 38; §4.5 (107), Example 39); lecture 08:48–09:54 and 10:44–19:30 (09:54–10:44, ln via e^y, is in ch3)
Goal: know the basic derivatives and get sin, cos, sinh and cosh from the exponential; derive the
chain, product and quotient rules from the limit and use each on the notes' example.
Scenes:
- s1_hook · Hook (~40 s): last time: the derivative as a limit; even x³ took a page. Nobody
  differentiates ln x · sin x that way: a short table and three rules do it. The question: why are the
  rules true? Each comes from the same limit.
- s2_table · A short table, and where it comes from (~120 s): §4.2: x^a → ax^{a−1}; e^{ax} → ae^{ax};
  ln(ax) = ln a + ln x → 1/x (the a drops out: ln a is a constant; the lecturer: the log must exist,
  so ax > 0); proof in part three. The rest "can be derived from e^{ax}": sinh(ax), cosh(ax) from
  ½(e^{ax} ± e^{−ax}) (L11's definitions; GOLD and PURPLE); sin and cos by differentiating
  e^{iax} = cos ax + i sin ax: ia·e^{iax} = −a sin ax + i·a cos ax, then match real and imaginary parts
  (L10's e^{iθ}; i PINK). The lecturer's other route: L11's dictionary (put ix for x). tan → a sec² ax,
  tanh → a sech² ax: derive them (quotient rule, s6), no need to memorise. This is the method of sheet
  question H2.
- s3_chain · The chain rule (~100 s): y = f(u(x)), e.g. sin x², outer f BLUE, inner u PURPLE. The notes'
  trick (p52): multiply and divide the difference quotient by u(x + δx) − u(x), the change δu (TEAL; the
  notes' green factor). Two quotients: (f(u + δu) − f(u))/δu times δu/δx. As δx → 0, δu → 0 too (u is
  differentiable, so continuous: part one's box). The limit is df/du · du/dx (105): "differentiation
  of a function of a function". Optional one-line footnote: dividing by δu needs δu ≠ 0; a full proof
  patches that case, and the rule stands.
- s4_chain_ex · Example 37, and a look ahead (~75 s): (a) sin x²: outer sin g, inner g = x², so
  cos g · 2x = 2x cos x². (b) ln(cos x): (1/v)(−sin x) = −tan x, only where cos x > 0 (the lecturer's
  caveat: otherwise the log is undefined). Look ahead (p53): for h(u(x, y), v(x, y)), ∂h/∂x =
  ∂h/∂u · ∂u/∂x + ∂h/∂v · ∂v/∂x: two routes from x to h, one term each (a small tree diagram); Chapter
  seven of the notes, and next term.
- s5_product · The product rule (~100 s): the derivation (p54): the limit of
  [f(x + h)g(x + h) − f(x)g(x)]/h; add and subtract f(x + h)g(x) (the notes' purple terms); regroup into
  f(x + h) times g's quotient plus f's quotient times g(x). The one non-trivial step (the lecturer):
  f(x + h) → f(x), which needs continuity, and f differentiable gives it (part one). (106):
  (fg)′ = f′g + fg′. Optional picture: a rectangle with sides f and g grows by two strips. Example 38:
  ln x sin x → (1/x) sin x + ln x cos x, for x > 0.
- s6_quotient · The quotient rule (~75 s): u/v = u × (1/v); the product rule, then the chain rule on
  1/v: −(1/v²) dv/dx; common denominator: (v u′ − u v′)/v² (107). Example 39: sin x / x (x ≠ 0) by the
  quotient rule, then by the product rule with h = 1/x: both give (x cos x − sin x)/x². The lecturer:
  forget the quotient rule and you can still rebuild it from the other two.
- s7_recap · Recap (~60 s): the table → "basic derivatives; the rest from E to the A ex"; the δu factor →
  "chain rule"; the add-and-subtract → "product rule"; u times one over v → "quotient rule". Try sheet
  H1 and H2 (basic skills; answers printed on the sheet's last page): in H1 check which letter is the
  variable (t in (e), y in (g)); in H2 write each function with exponentials as in s2, and in (d) the
  variable is ω. Next: equations that don't hand you y, starting with a circle. End card.
Continuity: uses part one's limit, box and TEAL increments. Role colours (first function BLUE, second
PURPLE) start here and carry into ch4, ch5, ch7. The table returns in ch7 s2.

## Chapter 3 · Implicit differentiation and inverse functions
Slug: ch3_implicit · ~10 min · Source: notes p. 51 (ln via e^y), pp. 56–58 (§4.6 (108)–(110), Example 40, Example 41: its working is handwritten, see the frame notes, §4.7 (111)); lecture 09:54–10:44 and 19:32–31:35
Goal: differentiate an equation g(y) = h(x) without solving for y, find both slopes of a circle, do
Tripos Example 41 with the right sign for cos y, and prove and use dx/dy = 1/(dy/dx).
Scenes:
- s1_hook · Hook (~40 s): last time: three rules. Now two awkward ones: the circle y² = 9 − (x − 1)²,
  which gives two y's for most x, and y = sin⁻¹(x/√(1 + x²)), which nobody wants to differentiate
  head-on. The question: how do you differentiate when y isn't handed to you as a formula you like?
- s2_implicit · Differentiate both sides (~95 s): (108) g(y) = h(x). One option is y = g⁻¹(h(x)), but
  that's not always possible or practical (and derivatives of inverse functions are easy to forget,
  the lecturer). Instead differentiate both sides, remembering y depends on x: the chain rule gives
  dg/dy · dy/dx (109), so dy/dx = (dh/dx)/(dg/dy) (110), provided dg/dy ≠ 0, which is exactly the
  condition for inverting g near that point (the lecturer: "so all is consistent"). First example,
  part two's promise (p51): y = ln(ax) ⇔ e^y = ax; e^y y′ = a; y′ = a/e^y = a/(ax) = 1/x.
- s3_circle · Example 40: both slopes of a circle (~130 s): y² = 9 − (x − 1)² is a circle, centre
  (1, 0), radius 3 (L11's completing the square), from x = −2 to 4 (the lecturer's sketch). Differentiate:
  2y y′ = −2(x − 1), so y′ = −(x − 1)/y (one-beat check: perpendicular to the radius). For the slope in
  terms of x alone, put in y = ±√(9 − (x − 1)²): y′ = ∓(x − 1)/√(9 − (x − 1)²). Two points above each x,
  two tangent lines (the lecturer: "you should give me two derivatives"). Valid for −2 < x < 4: at the
  ends the tangent line is vertical and the gradient infinite, so not differentiable there (part one's
  "finite"), hence the strict inequalities. Vertical tangent lines RED.
- s4_tripos · Example 41: take the sine of both sides (~85 s): Tripos 2006, paper 2, question 1A(a),
  4 marks: y = sin⁻¹(x/√(1 + x²)), find dy/dx as a function of x. The trick: sin y = x/√(1 + x²), and
  y is a function of x. Differentiate: cos y · y′ on the left; on the right the quotient rule (part two):
  [(1 + x²) − x²]/(1 + x²)^{3/2} = 1/(1 + x²)^{3/2}. Show that step; the lecturer skipped it ("I already
  simplified it").
- s5_sign · The sign of cos y (~100 s): we need cos y in terms of x, and cos y = ±√(1 − sin² y). "That's
  where most of the students made a mistake" (the lecturer, about this exam question). Inverse sine takes
  values from −π/2 to π/2: to invert sine you take a piece where it's monotonic (A-level, and L11's
  inverses). There cos y ≥ 0; and since |x/√(1 + x²)| < 1, y is strictly inside, so cos y > 0, which we
  need because we divide by it. So cos y = +√(1 − x²/(1 + x²)) = 1/√(1 + x²) (GREEN; the − root RED).
  y′ = 1/(1 + x²), boxed. Her note: "in fact y = tan⁻¹ x": a right triangle with sides x and 1 and
  hypotenuse √(1 + x²) has sin y = x/√(1 + x²) and tan y = x.
- s6_reciprocal · The reciprocal rule (~95 s): (111) dx/dy = 1/(dy/dx). Geometrically: swap the axes and
  the tangent line's slope turns over (small Figure 29 reflected in y = x). It looks like flipping a
  fraction, but dx and dy aren't numbers (part one), so prove it: with finite δx and δy,
  δx/δy = (δy/δx)^{−1}; as δy → 0, δx → 0 too (the lecturer: they're tied together); then take the
  limit inside the power. It fails when dy/dx = 0: there x(y) has a vertical tangent line (y = x³ at 0,
  whose inverse is the cube root). Use it: x = tan y gives dx/dy = sec² y = 1 + x², so
  dy/dx = 1/(1 + x²): Example 41 by a second route. (L11's G4 solution used this rule ahead of time.)
- s7_recap · Recap (~55 s): the circle with its two tangent lines → "differentiate both sides; chain rule
  on y"; the triangle → "pick the sign from the range: cos y > 0"; the swapped axes → "dx/dy is one over
  dy/dx, unless that's zero". Try sheet H4, which asks for both routes: (i) is the reciprocal rule,
  (ii) implicit differentiation; the answers look different until you use the original equation. Next:
  differentiate again and again. End card.
Continuity: uses part two's chain and quotient rules and part one's "finite". Example 40's circle in BLUE
(as L11's circles), tangent lines GREEN. The H4 card is reused in ch7.

## Chapter 4 · Leibniz's formula
Slug: ch4_leibniz · ~10 min · Source: notes pp. 59–62 (§4.8 (112), the note, x³; §4.9: p60 blank, filled on the board, see the frame notes; the proof (114) and Pascal's rule); lecture 31:39–32:44 and 33:50–42:36 ((113), 32:44–33:50, is in ch6)
Goal: compute nth derivatives, state Leibniz's formula for the nth derivative of a product, see why its
coefficients are Pascal's triangle, use it, and follow the induction proof.
Scenes:
- s1_hook · Hook (~45 s): last time: implicit differentiation and inverses. Differentiate a product
  once: the product rule. Ten times? The tenth derivative of x² e^{−x}. The question: is there a formula
  for the nth derivative of a product? (Answered in s5: e^{−x}(x² − 20x + 90).) Some of the room had
  met it, some hadn't (the lecturer's show of hands: "at least I'll tell you something new today").
- s2_higher · Again and again (~70 s): (112) d^n y/dx^n, defined recursively (the lecturer: "a trivial
  comment"), linear like the first derivative. The notes' note: d^n y/dx^n = (d/dx)^n y, not (dy/dx)^n:
  for x³ the second derivative is 6x, the square of the first is 9x⁴. The x³ chain card: 3x², 6x, 6, 0,
  and every later derivative 0.
- s3_pattern · The pattern (~95 s): the board (frame 36:25): y = fg; y′ = f′g + fg′ (1, 1);
  y″ = f″g + 2f′g′ + fg″ (1, 2, 1), the two middle terms coinciding; y‴ = f‴g + 3f″g′ + 3f′g″ + fg‴
  (1, 3, 3, 1). "What's this?" A student: Pascal's triangle, the coefficients of (a + b)^n. Why: each
  differentiation splits every term in two (the prime lands on f or on g), just as multiplying by
  (a + b) does.
- s4_formula · The formula (~75 s): (n choose m) = n!/(m!(n − m)!); other notations, C_n^m (the
  lecturer's poll: France, Russia, Ukraine, Kazakhstan, China). Her board (frame 38:55):
  (fg)^(n) = Σ_{m=0}^{n} (n choose m) f^(n−m) g^(m): m derivatives land on g, the rest on f. Check n = 2
  against s3.
- s5_example · When most terms vanish (~65 s): an example beyond the notes (their only use is Example 42):
  (x² e^{−x})^(n). Make the polynomial the factor that runs out: x² has three non-zero derivatives (x²,
  2x, 2), so three terms survive; e^{−x}'s derivatives alternate in sign. Result:
  (−1)^n e^{−x}(x² − 2nx + n(n − 1)); n = 1 matches the product rule; n = 10 gives
  e^{−x}(x² − 20x + 90) (sympy-checked). Part five uses the same idea.
- s6_proof1 · Proof by induction: two sums (~100 s): induction: true for n = 1 (the product rule), and
  true for n ⇒ true for n + 1. Differentiate the formula once more: the product rule inside the sum gives
  two sums (114). In the second, split off the last term f^(0) g^(n+1) and shift m → m − 1, so it runs
  from 1 to n with coefficient (n choose m − 1) and f^(n−m+1) g^(m): the same products as the first sum.
- s7_proof2 · Proof by induction: Pascal's rule (~95 s): split off the m = 0 term f^(n+1) g^(0) of the
  first sum. Both sums now run m = 1 … n, with coefficient (n choose m) + (n choose m − 1) =
  (n + 1 choose m), Pascal's rule (proved in §8.4.2 of the notes): each entry is the sum of the two above
  it. Fold the two end terms back in ((n + 1 choose 0) = (n + 1 choose n + 1) = 1): the formula for
  n + 1. Visual: two rows of the triangle linking up.
- s8_recap · Recap (~55 s): the x³ chain → "the Nth derivative: differentiate N times, not raise to the
  Nth power"; Pascal's triangle beside the y‴ line → "Leibniz: binomial coefficients"; the three
  surviving terms → "a polynomial factor cuts the sum short"; the linked rows → "induction and Pascal's
  rule". Next: Leibniz at work, on the Hermite polynomials of quantum mechanics. End card.
Continuity: the x³ chain from part one, continued, and reused in ch6. The Leibniz sum card and the
triangle return in ch5 s4 and ch7 s5. f BLUE, g PURPLE, coefficients YELLOW.

## Chapter 5 · Hermite polynomials
Slug: ch5_hermite · ~8 min · Source: notes pp. 62–63 (Example 42 and the H_n list; the lecturer's two corrections are in the frame notes); lecture 42:36–47:26
Goal: compute Hermite polynomials from their definition and prove the recursion
H_{n+1} = 2x H_n − 2n H_{n−1} with Leibniz's formula.
Scenes:
- s1_hook · Hook (~45 s): last time: Leibniz's formula. Where nth derivatives matter: quantum mechanics
  (the lecturer). Example 42: H_n(x) = (−1)^n e^{x²} d^n/dx^n e^{−x²}. The claim:
  H_{n+1} = 2x H_n − 2n H_{n−1}. The question: how does a definition with an nth derivative in it turn
  into a recursion?
- s2_define · The definition at work (~90 s): e^{−x²} is the Gaussian (PURPLE); e^{x²} (GOLD) cancels it.
  n = 0: H_0 = 1. n = 1: the derivative is −2x e^{−x²}; times −e^{x²}: H_1 = 2x. n = 2:
  (4x² − 2)e^{−x²}, so H_2 = 4x² − 2. Every derivative leaves a polynomial times e^{−x²}, the prefactor
  clears the Gaussian, and (−1)^n makes the leading coefficient 2^n positive. Check the claim at n = 1:
  2x·2x − 2·1·1 = 4x² − 2. The H_n ladder card starts.
- s3_peel · Peel off one derivative (~70 s): H_{n+1} = (−1)^{n+1} e^{x²} d^{n+1}/dx^{n+1} e^{−x²}
  = (−1)^{n+1} e^{x²} d^n/dx^n (d/dx e^{−x²}) = (−1)^{n+1} e^{x²} d^n/dx^n (−2x e^{−x²}). Pull out the
  −2: (−1)^{n+1}·(−2) = 2(−1)^n (the lecturer: (−1)^{n+2} is (−1)^n). What's left is the nth derivative
  of the product x e^{−x²}.
- s4_leibniz · Leibniz with a factor that runs out (~85 s): f = x (BLUE), g = e^{−x²} (PURPLE). f has
  one non-zero derivative (f′ = 1, then 0), so of the n + 1 terms only m = n − 1 and m = n survive:
  (n choose n − 1) f′ g^(n−1) + (n choose n) f g^(n) = n g^(n−1) + x g^(n). Show the row of Pascal's
  triangle with only its last two entries lit. The notes print the second coefficient as (n choose 0);
  the lecturer corrected it to (n choose n) on the page. Both are 1; show (n choose n).
- s5_assemble · Assemble the recursion (~70 s): H_{n+1} = 2(−1)^n e^{x²}[x g^(n) + n g^(n−1)]. The first
  part is 2x H_n. The second, 2n(−1)^n e^{x²} g^(n−1), is −2n(−1)^{n−1} e^{x²} g^(n−1) = −2n H_{n−1}
  (one factor −1 moved across). So H_{n+1} = 2x H_n − 2n H_{n−1}, boxed.
- s6_ladder · Climb the ladder (~70 s): from H_1 and H_2: H_3 = 2x(4x² − 2) − 4·2x = 8x³ − 12x (the notes
  print 8x³ − 12, a typo the lecturer corrected), H_4 = 2x H_3 − 6H_2 = 16x⁴ − 48x² + 12 (she checked:
  "this is not the typo"). Why physicists care (one beat): H_n(x) e^{−x²/2} are the states of the quantum
  harmonic oscillator, a Gaussian with n wiggles (plots, n = 0 to 3; the lecturer: "localized packets of
  the wave function").
- s7_recap · Recap (~50 s): the definition with GOLD and PURPLE cancelling → "a polynomial times the
  Gaussian, Gaussian removed"; the two lit entries → "x runs out after one derivative: two terms"; the
  ladder → "the recursion builds them all". Try sheet I1, the same trick: write g = e^{−x²/2}, notice
  g′ = −x g, and differentiate that N plus one times with Leibniz. Next: back to graphs, and what the
  derivatives say about a curve's shape. End card.
Continuity: uses part four's sum card and triangle, part two's chain rule. The colours make the
cancellation visible: GOLD e^{x²} against PURPLE e^{−x²}. I1's card is reused in ch7 s5.

## Chapter 6 · Stationary points
Slug: ch6_stationary · ~8.5 min · Source: notes p. 60 ((113)) and pp. 63–66 (§4.10, the figure, the classification, Figure 30, rising/falling inflection, the three graphs labelled by hand); lecture 32:44–33:50, 47:27–53:17, and the student question at 54:57–55:20
Goal: find and classify stationary points with the second and higher derivatives, explain why the
parity of the first non-zero derivative decides, and recognise inflection points that aren't stationary.
Scenes:
- s1_hook · Hook (~45 s): last time: Hermite polynomials. The last section of Chapter four of the notes
  (as far as this lecture went): the notes' figure, a curve with a local maximum, a local minimum, points
  of inflection and a rising stationary point of inflection. The question: how do derivatives tell
  these apart?
- s2_vocab · The vocabulary (~75 s): a stationary point is where dy/dx = 0 (the name: a stationary object
  has zero velocity, and velocity is the first derivative of position, the lecturer). Local maximum and
  minimum: highest or lowest nearby, not overall. Concave up, concave down; a point of inflection is
  where the concavity changes, that is, where the second derivative changes sign. Labels arrive on the
  notes' figure.
- s3_second · The second-derivative test (~70 s): y″ > 0 at a stationary point: a minimum, because the
  gradient increases through it (negative, zero, positive: a tangent line rolling through with its slope
  readout). y″ < 0: a maximum, the gradient decreases. The lecturer's umbrella: open it upright and it
  collects rain, positive second derivative, a minimum; upside down, no rain under it, a maximum.
- s4_higher · When the second derivative is zero (~90 s): y = x³ and y = x⁴ (Figure 30): both have
  y′ = y″ = 0 at 0. Their chains side by side: x³ → 3x², 6x, 6 (part four's card), first non-zero is the
  third, 6 ≠ 0: inflection (the gradient is positive on both sides). x⁴ → 4x³, 12x², 24x, 24 > 0: the
  fourth: minimum. The rule (p64): first non-zero derivative of order n; n odd → point of inflection;
  n even and positive → minimum; even and negative → maximum (−x⁴). The lecturer: if all the
  derivatives vanish it gets subtle; one aside beyond the notes, optional: e^{−1/x²} has a minimum at 0
  and every derivative 0 there.
- s5_why · Why odd and even? (~95 s): a student asked this after the lecture; the lecturer's answer: a
  Taylor expansion. Start from (113): y(x + δx) ≈ y(x) + δx dy/dx, the definition rearranged, better as
  δx → 0: the tangent line as the best straight-line fit (small Figure 29). More terms in powers of δx
  give Taylor series (§6.3 of the notes). At a stationary point whose first non-zero derivative is the
  nth, the change is about y^(n)(x₀) δx^n / n!. For even n, δx^n has the same sign on both sides: both
  sides above (minimum) or both below (maximum). For odd n it flips: the curve crosses its tangent line,
  an inflection. Visual: δx², δx³, δx⁴ near 0.
- s6_nonstat · Inflections that aren't stationary (~85 s): y″ = 0 and changing sign while y′ ≠ 0: a
  rising (y′ > 0) or falling (y′ < 0) point of inflection (the notes' filled blanks). Stationary ones are
  rising or falling too (x³ rises). The board's three graphs with her labels (frame 52:40): left
  y′(0) ≠ 0, y″(0) = 0, rising; middle y′(0) = y″(0) = 0, y‴(0) ≠ 0, stationary; right y′(0) ≠ 0,
  y″(0) = 0, falling; concave down to concave up in all three. The notes don't name the functions:
  use y = x³ + x, y = x³ and y = x³ − 3x on −1 ≤ x ≤ 1 (the writer's fix: the planned −x³ − x has
  y″ = −6x and bends the wrong way; all three need y″ = 6x). Pitfall: y″ = 0 alone isn't enough; x⁴
  has y″(0) = 0 and no inflection, and x⁴ + x looks like a rising inflection but isn't (ch6's trap). The sign of y″ must change, as the lecturer defined it.
- s7_recap · Recap (~50 s): the labelled figure → "stationary: y′ = 0"; the umbrella → "y″ > 0
  minimum, y″ < 0 maximum"; x³ beside x⁴ → "first non-zero derivative: odd, inflection; even, max or
  min"; the δx^n signs → "why: Taylor"; the three graphs → "inflection: y″ changes sign". Next time:
  curve sketching (§4.11), which puts all of this to work, with sheet H3 and H5. The bonus part has the
  solutions to H1, H2, H4 and I1. End card.
Continuity: Figure 29 and the x³ chain come back. Curves BLUE, tangent lines GREEN, stationary points
YELLOW. Ends the series' core.

## Chapter 7 · Solutions: Examples Sheet H1, H2, H4 and I1
Slug: ch7_solutions · ~8.5 min (bonus) · Source: Examples Sheet I pp. 10–11 (H1, H2, H4, I1; answers are printed on p. 15 for H1–H3 only, so H4 and I1 are derived and checked with sympy), drawing on notes pp. 50–62
Goal: worked solutions to the sheet questions this lecture covers, with the tempting mistakes.
Scenes:
- s1_intro · Spoilers ahead (~35 s): pause and try first; the cards from the recaps of parts two, three
  and five. H3 and H5 go with curve sketching, next lecture.
- s2_basics · H1 and H2 (~125 s): H1 at speed, slowing on the traps: (e) d/dt(at + bt² sin θ) =
  a + 2bt sin θ, since θ is a constant; (f) (2/3)x^{−1/3}; (g) the variable is y: −(1 + y)^{−2}. H2 by
  exponentials: (a) sin x = (e^{ix} − e^{−ix})/2i gives cos x; (g) tanh x = (e^x − e^{−x})/(e^x + e^{−x}),
  quotient rule: 4/(e^x + e^{−x})² = sech² x; (h) chain rule: 2 sech² 2x; (d) d/dω sin(−iωt): the
  variable is ω, so −it cos(−iωt), which is −it cosh(ωt) by L11's dictionary. The rest match the printed
  answers.
- s3_h4_one · H4, the first route: x as a function of y (~95 s): y + e^y sin y = 1/x, so
  x = 1/(y + e^y sin y); dx/dy = −(1 + e^y sin y + e^y cos y)/(y + e^y sin y)²; the reciprocal rule:
  dy/dx = −(y + e^y sin y)²/(1 + e^y(sin y + cos y)).
- s4_h4_two · H4, the second route, and why they agree (~90 s): differentiate with respect to x:
  y′ + e^y y′ sin y + e^y cos y · y′ = −1/x², so y′ = −1/(x²(1 + e^y(sin y + cos y))). They agree
  because the original equation gives (y + e^y sin y)² = 1/x². Pitfall: dropping the y′ that the chain
  rule puts on e^y. Both fail where 1 + e^y(sin y + cos y) = 0, where dx/dy = 0.
- s5_i1 · I1: Leibniz on a Gaussian (~115 s): g = e^{−x²/2}, Z_n = g^(n). Key fact: g′ = −x g.
  Differentiate it n + 1 times with Leibniz; x has two non-zero derivatives, so
  g^(n+2) = −[x g^(n+1) + (n + 1) g^(n)], that is Z_n″ + x Z_n′ + (n + 1)Z_n = 0. Check n = 0: Z_0 = g,
  Z_0′ = −xg, Z_0″ = (x² − 1)g, and (x² − 1) − x² + 1 = 0. Part five's Hermite proof is the same trick
  on e^{−x²}.
- s6_recap · Recap (~50 s): the four cards, each with its key picture (the table; the two routes
  meeting; the Leibniz sum cut to two terms). Next lecture: curve sketching. End card.
Continuity: cards match the hints in ch2 s7, ch3 s7 and ch5 s7. Uses ch2's table, ch3's two routes and
ch4–ch5's sum card.

## Decisions
- **6 core chapters + a bonus (~55 + 8.5 min of words, ~66 + 10 min of video).** The lecture runs 53
  minutes (00:00–53:17) and splits at natural seams: definition and differentiability → ch1; the
  basic derivatives and the three rules → ch2; implicit differentiation, Examples 40–41 and the
  reciprocal rule → ch3; higher derivatives, Leibniz and its proof → ch4; Example 42 → ch5;
  stationary points → ch6. The words-to-lecture ratio (~1.04) is a little under L11's (61 min for 52),
  because the lecturer calls the chapter A-level review: Examples 37–39 move briskly, and the time goes
  to the derivations from the limit (which A-level skips), Example 41's sign trap, and the parts she
  said would be new to some (Leibniz, the higher-derivative test).
- **Hermite gets its own chapter.** Example 42 took 5 minutes of careful sign and index bookkeeping. It
  doesn't fit beside ch4's formula and proof (that would be ~14 min), and it has nothing in common with
  stationary points. It runs at 8 minutes, the minimum, with a direct H_0–H_2 computation, so the
  definition is concrete before the proof.
- **Two moves within the lecture's order.** (1) ln's derivative via e^y = ax (§4.2, lectured
  09:54–10:44 before the chain rule) goes to ch3 s2: it is implicit differentiation (the notes say "see
  §4.6") and needs the chain rule, so it lands as the first implicit example. (2) The linear
  approximation (113) (§4.8, 32:44–33:50) goes to ch6 s5, where it sets up the answer to the student's
  odd/even question; ch4 keeps the rest of §4.8 for the nth-derivative notation Leibniz needs.
- **Lecture boundary.** The lecturer opened with "start and hopefully finish chapter four", but stopped
  after §4.10 (p66) with "next time: curve sketching". §4.11 and Example 43 (pp. 66–70) are left for
  L13; the Ch 5+6 notes weren't needed (opened only to place sheet J1 and §6.3).
- **Exercises.** L12's sheet questions are H1, H2, H4 and I1: hints at the end of the chapter that
  teaches each (H1/H2 ch2, H4 ch3, I1 ch5, as L10 did), full solutions in ch7. H1 gets only its three
  traps (answers are printed, and it's pure A-level). Not here: H3 (even or odd) and H5 (sketching)
  belong to §4.11; J1 (continuity and differentiability, with x sin(1/x)) belongs to Chapter five of the
  notes, limits and continuity, though its |x| part is ch1's material. Supervision 3 has no calculus, so
  all of H and I is ahead of the user.
- **Additions beyond the notes**, one beat each: "chord" as the name; linearity spelled out; the 1/h
  slope across the jump; sin and cos from e^{iax}; the δu ≠ 0 footnote (optional); the
  perpendicular-radius check and the tan⁻¹ triangle; the cube root as the reciprocal rule's failure and
  tan⁻¹ by the second route; ch4's worked example (x² e^{−x})^(n); ch5's direct H_0–H_2 and the
  oscillator plots; ch6's e^{−1/x²} aside (optional), the δx^n parity picture, and named functions for
  the notes' three unnamed graphs. Left out: nothing lectured. The 53:17–54:56 stretch is silence that
  Whisper filled with one repeated line.
- **Source conflicts.** Where the lecturer corrected the notes, her correction wins: H_3 = 8x³ − 12x (the
  notes print 8x³ − 12; 47:18, frame 47:20); the second coefficient in Example 42's expansion is
  (n choose n), not (n choose 0) (46:01; equal values). Where her speech slipped, the notes win: 33:58
  "find the antiderivative of the product" means the nth derivative. Two clarifications: the notes'
  "provided |δx| < 1" chain isn't needed (she says so, 03:26); the notes' rising/falling rule says "a
  point where y″ = 0", and we add "and y″ changes sign" (her own definition at 48:12; x⁴ is the
  counterexample). Heaviside at 0: the notes leave H(0) undefined, her sketch has H(0) = 1, and she says
  definitions vary; ch1 draws hers and says so.
- **No digest.** Gemini was off, so the four handwritten blanks come from eight frames the planner read
  (07:00, 24:50, 28:40, 29:30, 36:25, 38:55, 47:20, 52:40), recorded in `project.json`. Example 41's earlier lines (p57) come from the transcript, which states every step.
  Directors can run `vk lecture` again after Gemini's reset for board-drawing detail, but the plan
  doesn't depend on it.
- **Colours.** L12 makes TEAL its own thread (the increment that goes to zero), as L10 and L11 each did,
  so hyperbolic function names are white here; i stays PINK and e^{±x} GOLD/PURPLE. The role colours
  for two-function rules (first BLUE, second PURPLE) were picked so that every second factor this
  lecture meets (e^{−x}, e^{−x²}, e^{−x²/2}) is already PURPLE by the course rule.
- **Continuity review (2026-11-03).** All seven scripts read against this plan. Fixed in ch2–ch7: "I one" →
  "eye one" (ch5–ch7); one owner and one exact form for every reused asset (Figure 29 = y = x³ at x = 1,
  the circle's line at x = 2.8, the box, the x³ card, the triangle's rows, the question cards, ch6's
  figure); ch7 s1 now takes the labelled figure from ch6 s2, not s1. ch5's board sign slip at 45:01 was
  checked on the frame and holds. ch1 was being voiced, so its two edits went to the producer as a list.
- **Voice.** The derivative words ("dee why by dee ex", primes, "delta ex") and the names Leibniz and
  Hermite are untested with the clone. Voice ch1 first and check its QA before the rest; ch4 and ch5
  test the names.
