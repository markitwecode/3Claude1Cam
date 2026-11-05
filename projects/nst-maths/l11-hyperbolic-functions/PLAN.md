# Hyperbolic Functions and Conics: plan

Request: "make 3Blue1Brown-style videos of this maths lecture" ("all the lecture notes are on the
course web page"), via the producer, 2026-11-01. Audience: a Cambridge first-year natural scientist
studying NST IA Mathematics, Course B (Mathematical Methods I, N. G. Berloff). Knows A-level maths
(the lecturer assumes cosh and sinh were met there) and Lectures 1–10: complex numbers in polar form,
e^{iθ} = cos θ + i sin θ, De Moivre, cos θ and sin θ written with e^{±iθ}, the multivalued complex log,
complex powers, complex amplitudes. Has done supervision 3 (sheet sections D, E, F7–F12); section G
(hyperbolic functions) is still ahead. Sources: the Lecture 11 recording (`../source/l11-lecture.transcript.md`
and `.digest.md`), the notes `../source/Chapter234_to_annotate.pdf` pp. 30–46, Examples Sheet I section G
(`../source/M26examples1 (2).pdf`, p. 9).
Total: 7 chapters (6 + a bonus solutions chapter), ~70 min of narration (~61 core + ~9 bonus).

## Conventions (all chapters)
- Reading the sources: each chapter lists its notes pages and transcript range. The notes' text layer
  garbles the maths: render the page (`pdftoppm -f N -l N -r 80 -png …`) to read a formula. The blanks
  were filled by hand in the lecture and L11's scan isn't posted, so the digest is the only record of
  the handwriting (Examples 35 and 36, the Figure 26–28 labels, the conic summary). Where notes and
  digest disagree, trust the notes (list in Decisions).
- Notation as in the notes: cosh, sinh, tanh, sech, cosech, coth; inverses cosh⁻¹ x, sinh⁻¹ x, tanh⁻¹ x;
  z = x + iy; n, m integers; θ is the parameter of circle, ellipse and hyperbola. On screen write e^x
  throughout (the notes mix exp(x) and e^x; one form is easier to follow).
- Colours by meaning (engine palette):
  - BLUE: the circular world (cos, sin, tan; the circle; the ellipse, a stretched circle);
  - TEAL: the hyperbolic world (cosh, sinh, tanh and their inverses; the hyperbola);
  - GOLD for e^x and PURPLE for e^{−x}, the two exponentials every hyperbolic function is made of;
  - PINK: the imaginary unit i, imaginary parts and the "imaginary part" / Im labels (course-wide
    rule, producer 2026-11-01). A number keeps the colour of the function it came from: ch4's
    ln(2 + √3) = cosh⁻¹ 2 is TEAL, with its i PINK;
  - YELLOW: attention, flipped signs, boxed results, centres of conics;
  - GREEN: the root, branch or case we keep; RED: rejected roots, impossible cases (∅), pitfalls;
  - semi-major axis GOLD, semi-minor GREEN (the notes use red/green; RED means "wrong" here).
- Cross-references (continuity review, 2026-11-01): narration calls the videos "part one" … "part
  seven", the word on the title cards. "Chapter" only for the notes' own chapters ("Chapter three of
  the notes"), which would otherwise clash. G2's (i) and (ii) are "the first curve" and "the second
  curve". On-screen labels likewise: "Part 6", "solutions: Part 7 (bonus)".
- Recurring visuals: build once, reuse in the same style.
  - "The dictionary" card: cos(ix) = cosh x, sin(ix) = i sinh x, tan(ix) = i tanh x. Built in
    ch1 s4–s6, reused in ch2 s3 and s6 and in ch4 s3.
  - The circle–hyperbola pair: a point (cos θ, sin θ) running on x² + y² = 1 beside a point
    (cosh θ, sinh θ) on x² − y² = 1. Glimpsed in ch1 s1, explained by the identity in ch2 s2, paid off
    in ch6 s3.
  - Figure 25-style graphs with dashed ½e^x / ½e^{−x} asymptotes: ch1 s2, ch3, ch7 s4. Same axes and
    colours each time.
  - Example 36's ellipse: ch5 s1 and s6, ch6 s5.
  - The four G-question cards: ch6 s7, ch7 s1.
  - The PURPLE minus branch: cosh⁻¹'s lower branch (ch3 s5, ch4 s5, ch7 s4) and the hyperbola's
    left-branch running point (ch6 s3, ch7 s3).
  - tanh's dashed asymptotes GOLD y = 1 and PURPLE y = −1, which turn into GOLD x = 1 and PURPLE
    x = −1 for tanh⁻¹ (ch3 s3 and s6; ch7 s2, s4, s5).

## Voice rules for formulas
Also added to `../COURSE.md` ("Voice rules"), which is the master copy once voice QA corrects them. They
are untested with the clone: ch1's voice run is the test (see Decisions). The general studio rules apply
too (script-writer.md: no bare single letters, N as a capital, strong word after a colon).
- Circular functions in full: "cosine", "sine", "tangent". A bare "cos" may be read as "because", and
  "cosine" against "cosh" keeps the two worlds apart by ear.
- Hyperbolic ones as the notes say them: "cosh", "shine" (sinh), "tanch" (tanh). The rare three in full:
  "hyperbolic secant", "hyperbolic cosecant", "hyperbolic cotangent" (or "one over cosh" in working).
- Inverses: "inverse cosh of ex", "inverse shine", "inverse tanch". Never "cosh to the minus one": it
  sounds like one over cosh, the very confusion ch1 warns about.
- Lowercase variables spelled: x "ex", y "why", z "zed" (British, as the course); commas around them
  when they stand alone ("a real number, ex, and"). "the ex axis". The QA maps ex, why and zed.
- Other letters: capitals right after a noun (course rule): "the constant S", "semi-axis A",
  "the integer N", "the integer M", "the radius R" (never "ar": heard as "hours" in DE). In a product
  the letter ends a phrase: "cosh of A, times cosh of B", never "cosh A cosh B" (an A before a word
  is read as the article "uh"). A sum is "the cosh of the sum, A, plus B", then "the cosh of the
  sum"; never "cosh of A plus B" (DE L10 heard "uh" there).
- Avoid "halves" and "halve" (DE: "halve" heard as "have"): "the two parts", "the factors of a half".
- i is "eye" ("eye squared is minus one"). e is a capital "E": "E to the ex", "E to the minus ex",
  "E to the two why" for e^{2y} or exp(2y). If "E" garbles, try "ee", then "the exponential of ex".
- ln is "log" ("the log of two plus the square root of three"), never "ell en".
- Scope: mark what a fraction, root or log covers with "all" or a comma: "E to the ex, plus E to the
  minus ex, all over two". Better still, name a long formula by its parts while the screen highlights
  them. Never read more than about eight symbols in one breath.
- Subscripts: "ex zero", "why zero", "zed one". Never "nought": it can be heard as "not", which flips
  the meaning. The coefficients of a polynomial are "the leading coefficient", "the constant term".
- Symbols: ± "plus or minus"; ≥ "at least"; ≠ "different from"; ∅ "no solution"; ℤ "any integer";
  ≈ "about", with rounded numbers in words ("about one point three two"); (−1)^n "minus one to the
  power N"; x² "ex squared"; cosh² x "cosh squared of ex".
- Words: "hyperbolas", not "hyperbolae". Prefer "the semi-major and semi-minor axes" to a bare
  "semi-axes", which can be read as "axes" (the tools).
- Likely false flags: Whisper may write "shine", "tanch" and "cosh" oddly ("tench", "cash"). Ear-check
  with `vk listen --only` before rewriting, and add a homophone to voiceqa if one recurs.

## Chapter 1 · Cosine without the i
Slug: ch1_cosh_sinh · ~9.5 min · Source: notes pp. 31–32 (§3.1, (84)–(92)); lecture 04:41–08:10 (its recap of L10, 00:00–03:12, is the "last time")
Goal: define cosh, sinh, tanh and the three reciprocals from real exponentials, picture cosh and sinh
as the average and half-difference of e^x and e^{−x}, and derive cos(ix) = cosh x, sin(ix) = i sinh x
and tan(ix) = i tanh x for any complex x.
Scenes:
- s1_hook · Hook (~50 s): title card. Last time (one sentence, Lecture 10): cos x and sin x written
  with e^{ix} and e^{−ix}. The i's lift out of cos x's formula, leaving ½(e^x + e^{−x}), a new function.
  A glimpse of the circle–hyperbola pair. The question: what are these functions, how are they tied to
  cosine and sine, and why are they called hyperbolic?
- s2_define · Real exponentials (~110 s): from cos x = ½(e^{ix} + e^{−ix}) and
  sin x = (e^{ix} − e^{−ix})/2i, keep the shape and make the exponent real: cosh x = ½(e^x + e^{−x}) (84),
  sinh x = ½(e^x − e^{−x}) (85), with no i in sinh's denominator. Real functions of a real variable.
  Key visual: e^x (GOLD) and e^{−x} (PURPLE) on one set of axes; cosh drawn as their average (the
  midpoint at each x), sinh as half their difference. Last beat: adding the two gives
  e^x = cosh x + sinh x, the real cousin of e^{ix} = cos x + i sin x (used again in ch7).
- s3_family · tanh and three reciprocals (~80 s): tanh x = sinh x / cosh x
  = (e^x − e^{−x})/(e^x + e^{−x}) (86); sech = 1/cosh, cosech = 1/sinh, coth = 1/tanh (87)–(89), each
  beside its circular parent (sec, cosec, cot). How they're said, as the notes give them: "cosh",
  "shine", "tanch". Warning: sech x is one over cosh x; the inverse function cosh⁻¹ (ch3) is a
  different thing.
- s4_cosix · Putting the i back: cos(ix) (~100 s): the notes' trick. In cos z = ½(e^{iz} + e^{−iz}) put
  z = ix; i² = −1 turns e^{iz} into e^{−x} and e^{−iz} into e^{x}. The two terms swap places, the sum
  is unchanged: cos(ix) = cosh x (90), boxed, as the lecturer did (her margin note: i² = −1).
- s5_sinix · sin(ix) and tan(ix) (~105 s): the same with sine: sin(ix) = (e^{−x} − e^{x})/2i
  = −(e^x − e^{−x})/2i = (i/2)(e^x − e^{−x}). Slow down at 1/i = −i (multiply top and bottom by i),
  the step where people drop a sign. So sin(ix) = i sinh x (91); divide (91) by (90): tan(ix) = i tanh x (92).
- s6_dictionary · Valid for every complex number (~65 s): the notes stress that (90)–(92) hold for
  all complex arguments, not only real x. The dictionary card: cosine ↔ cosh with no i; sine ↔ sinh and
  tangent ↔ tanh with an extra i. Read backwards too: cosh x = cos(ix), sinh x = −i sin(ix). What it
  buys: every trig identity becomes a hyperbolic one (ch2), and cosine of a complex number splits into
  real functions (ch4).
- s7_recap · Recap (~60 s): the averaging picture, small → "average and half-difference of e^x and
  e^{−x}"; the family card → "tanh and three reciprocals"; the dictionary card → "an i turns cosine
  into cosh". Next: cos² + sin² = 1 has a hyperbolic twin, with a minus sign. End card.
Continuity: builds the dictionary card and the e^x / e^{−x} graph style for the whole series. Assumes
L10 (e^{iθ}, De Moivre, cos and sin as exponentials). The fundamental theorem of algebra, lectured just
before §3.1, is in ch4 (see Decisions), so ch1 starts straight on hyperbolic functions.

## Chapter 2 · Identities and the sign flip
Slug: ch2_identities · ~10 min · Source: notes pp. 33–34 (§3.2, (93)–(95), Example 33); lecture 08:10–13:00 (11:02–11:44 is a camera refocus; nothing said)
Goal: derive cosh² x − sinh² x = 1 from the definitions and cosh(A + B) through the dictionary, state
the sign-flip rule that turns any trig identity into its hyperbolic twin, and get tanh(A + B) two ways.
Scenes:
- s1_hook · Hook (~45 s): last time: an i turns cosine into cosh. On screen, cos² x + sin² x = 1 and its
  circle. Two ways to find the hyperbolic version: expand the definitions, or go through the complex
  door. The question: what changes, and is there one rule for every identity?
- s2_pythag · cosh² − sinh² = 1 (~95 s): square (84) and (85): ¼(e^{2x} + 2 + e^{−2x})
  − ¼(e^{2x} − 2 + e^{−2x}). The e^{±2x} terms cancel and the two 2's leave 4/4 = 1 (93). Side by side
  with cos² + sin² = 1: a minus where the circle has a plus (the lecturer's margin note "comp.
  sin²θ + cos²θ = 1"). One beat: so the point (cosh θ, sinh θ) lies on x² − y² = 1, a hyperbola (the
  pair from ch1; the full story is in ch6).
- s3_addition · cosh(A + B) through the complex door (~110 s): (94) cos(A + B) = cos A cos B − sin A sin B
  holds for complex A and B, so put iA and iB. The dictionary: cos(iA) cos(iB) → cosh A cosh B, and
  sin(iA) sin(iB) → (i sinh A)(i sinh B) = i² sinh A sinh B = −sinh A sinh B. The minus in front makes
  it a plus: cosh(A + B) = cosh A cosh B + sinh A sinh B. The lecturer: "notice that minus sign is
  replaced with a plus sign".
- s4_list · The whole family (~85 s): the list (95), each line beside its trig parent, changed signs in
  YELLOW: cosh(A ± B); sinh(A ± B) (no flip: no sinh·sinh product); 1 − tanh² z = sech² z (divide (93)
  by cosh²); coth² z − 1 = cosech² z (divide by sinh²).
- s5_rule · The sign-flip rule (~95 s): the notes' boxed rule: replace cos by cosh and sin by sinh, and
  change the sign wherever there's a product of two sinh's, hidden ones included (tan² = sin²/cos², so
  tanh² carries a sinh²; tanh A tanh B carries sinh A sinh B). Run it on 1 + tan² = sec²: you get
  1 − tanh² = sech², as in s4. Then predict: tan(A + B) = (tan A + tan B)/(1 − tan A tan B) becomes
  (tanh A + tanh B)/(1 + tanh A tanh B), because the hidden product flips the minus. The rule is
  usually called Osborn's rule (the name isn't in the notes). It's a memory aid: prove results with the
  definitions or the dictionary.
- s6_tanh · Example 33: tanh(A + B) (~115 s): prove s5's prediction. Route 1, the notes':
  tanh(A + B) = −i tan(i(A + B)) = −i sin(iA + iB)/cos(iA + iB); expand both; apply the dictionary; the
  i's cancel to (sinh A cosh B + cosh A sinh B)/(cosh A cosh B + sinh A sinh B); divide top and bottom
  by cosh A cosh B → (tanh A + tanh B)/(1 + tanh A tanh B). Route 2, the lecturer's shortcut: write
  sinh(A + B)/cosh(A + B) straight from (95), then divide. Same answer. This is Examples Sheet question
  G1 with x and y (ch7 adds a third route).
- s7_recap · Recap (~60 s): the cancelling squares, small → "cosh² − sinh² = 1"; i times i flipping the
  sign → "through the complex door"; the side-by-side list with yellow signs → "flip on sinh times
  sinh"; the tanh formula → "tanh(A + B)". Next: what the three graphs look like, and how to undo them.
  End card.
Continuity: uses ch1's dictionary card. Letters A and B as in the notes (G1's x and y appear only in
the closing remark of s6). The hidden-product warning returns in ch7 (G1).

## Chapter 3 · Graphs and inverses
Slug: ch3_graphs_inverses · ~10.5 min · Source: notes pp. 35–38 (§3.3 Figure 25 and properties 1–6; §3.4 (96), (97), Figure 26, Example 34); lecture 13:00–24:30
Goal: sketch cosh, sinh and tanh from their exponentials (value at 0, symmetry, asymptotes, range),
and derive sinh⁻¹ x = ln(x + √(x² + 1)), cosh⁻¹ x = ±ln(x + √(x² − 1)) for x ≥ 1, and
tanh⁻¹ x = ½ ln[(1 + x)/(1 − x)] for |x| < 1.
Scenes:
- s1_hook · Hook (~45 s): last time: the identities. Three formulas made of e^x and e^{−x}: what do
  their graphs look like, and can we run them backwards? Teaser: undoing them gives logarithms.
- s2_cosh · The shape of cosh (~90 s): cosh 0 = 1 (property 1); even, cosh(−x) = cosh x (2); for large
  x, e^{−x} ≪ e^x, so cosh x hugs ½e^x (3), and ½e^{−x} far to the left (4); so cosh x ≥ 1 for every
  real x (6). Figure 25(a), grown from ch1's averaging picture, with dashed GOLD and PURPLE asymptotes.
- s3_sinh_tanh · sinh, tanh, and all three together (~110 s): sinh 0 = 0; odd; it joins cosh along ½e^x
  on the right and mirrors it, −½e^{−x}, on the left (property 4); always below cosh, since
  cosh x − sinh x = e^{−x} > 0. tanh: 0 at 0, odd, → ±1 as x → ±∞ (drop the e^{−x} terms, property 5),
  so −1 < tanh x < 1 (6). Figure 25(d): all three on one set of axes.
- s4_arsinh · Undoing sinh (~115 s): an inverse needs each output to come from one input. sinh and tanh
  always increase, so they invert everywhere; cosh doesn't (two branches, next scene). sinh y = x →
  ½(e^y − e^{−y}) = x → multiply by 2e^y → (e^y)² − 2x e^y − 1 = 0, a quadratic in e^y →
  e^y = x ± √(x² + 1). e^y > 0, and √(x² + 1) > |x|, so the minus root is negative: rejected (RED).
  sinh⁻¹ x = ln(x + √(x² + 1)) (96), for every real x. Graph: sinh reflected in y = x (G3 needs it).
  Other books write arsinh.
- s5_arcosh · Undoing cosh: two branches (~120 s): the same steps give e^{2y} − 2x e^y + 1 = 0 →
  e^y = x ± √(x² − 1). This time both roots are positive (for x ≥ 1), so neither is rejected. Their
  product is 1, so x − √(x² − 1) = 1/(x + √(x² − 1)), whose log is −ln(x + √(x² − 1)). So
  y = ±ln(x + √(x² − 1)): the ± is there because cosh(−y) = cosh y. The principal (non-negative) value:
  cosh⁻¹ x = ln(x + √(x² − 1)) (97), only for x ≥ 1, since no real number has a cosh below 1.
  Figure 26: cosh, and the sideways curve with its upper branch +ln(…) (TEAL) and lower branch −ln(…)
  (PURPLE), labelled as the lecturer did. Keep both branches in view: ch4 needs the minus one.
- s6_artanh · Example 34: undoing tanh (~95 s): x = tanh y → x(e^y + e^{−y}) = e^y − e^{−y} → multiply
  by e^y → (1 − x)e^{2y} = 1 + x → e^{2y} = (1 + x)/(1 − x) → tanh⁻¹ x = ½ ln[(1 + x)/(1 − x)], |x| < 1.
  Graph: tanh's horizontal asymptotes at ±1 become vertical ones; near 0 it's almost the line y = x.
  The lecturer's conclusion: the inverse hyperbolic functions are logarithms.
- s7_recap · Recap (~60 s): three small graphs, each with its inverse and its log formula under it;
  the two-branch picture → "cosh⁻¹: plus or minus". Next: cos z = 2, which needs the inverse cosh
  of 2. End card.
Continuity: same axes and colours as ch1 s2. The reciprocal step x − √(x² − 1) = 1/(x + √(x² − 1))
returns in ch4's check. The sinh⁻¹ and tanh⁻¹ graphs return in ch7 (G3), Example 34 in ch7 (G1, G4).

## Chapter 4 · Solving cos z = 2
Slug: ch4_cos_z · ~10 min · Source: notes p. 30 (§2.7) and p. 39 (Example 35, blank in the notes: the working is in the digest, 24:19–32:38); lecture 03:12–04:43 and 24:19–32:42
Goal: state the fundamental theorem of algebra and why "at least one root" gives all n of them, then
find every complex solution of cos z = 2 by splitting it into real and imaginary parts, and plot them.
Scenes:
- s1_hook · Hook (~50 s): last time: the inverses are logarithms. A cosine wave trapped between −1 and
  1; the line y = 2 never meets it. x² + 1 = 0 had no real roots either, until complex numbers. The
  question: does cos z = 2 have complex solutions, and how many?
- s2_fta · Every polynomial has its roots (~100 s): closing Chapter 2 of the notes (§2.7, lectured at
  the start of L11). A polynomial of degree n ≥ 1 with complex coefficients and a_n ≠ 0 has exactly n
  complex roots, counting repeats. This is the same as "at least one root": factor out (z − z₁), the
  quotient Q has degree n − 1, repeat down to degree 0. Example: z³ − 1 = (z − 1)(z² + z + 1), the
  three cube roots of unity (from L9–L10). Not a formal proof (the lecturer said so). History, from the
  notes: Peter Roth 1608, Gauss 1799 (real coefficients), Argand 1806 (complex coefficients, the first
  complete proof). Bridge: cos z isn't a polynomial, so the theorem promises nothing here. Let's look.
- s3_split · Split z into x + iy (~105 s): z = x + iy with x and y real (the lecturer: so we can use
  what we know about real functions). cos(x + iy) = cos x cos(iy) − sin x sin(iy), the addition formula,
  valid for complex arguments (ch2). The dictionary: cos(iy) = cosh y, sin(iy) = i sinh y. So
  cos z = cos x cosh y − i sin x sinh y. Real part and imaginary part colour-coded (imaginary PINK).
- s4_cases · Two real equations, one dead end (~100 s): two complex numbers are equal when their real
  parts are equal and their imaginary parts are equal, and 2 has imaginary part 0: cos x cosh y = 2,
  sin x sinh y = 0. The lecturer's tip: start with the equation that equals zero, because a product is
  zero only when a factor is. Case tree: sinh y = 0 → y = 0 (sinh is zero only at 0, ch3) → cosh 0 = 1
  → cos x = 2: no solution (∅, RED; the real dead end again). Or sin x = 0 → x = nπ.
- s5_even · Only even multiples of π (~100 s): x = nπ gives cos nπ = (−1)^n, so (−1)^n cosh y = 2.
  cosh y ≥ 1 > 0, so (−1)^n must be +1: n is even, n = 2m. Left with x = 2πm and cosh y = 2, so
  y = ±cosh⁻¹ 2 = ±ln(2 + √(2² − 1)) = ±ln(2 + √3) ≈ ±1.32. Both of ch3's branches count: y can be any
  real number, not only the principal value.
- s6_lattice · Infinitely many solutions (~95 s): z = 2πm ± i ln(2 + √3), m any integer. The Argand
  diagram from the lecturer's sheet: a pair of crosses above and below 0, ±2π, ±4π, …, spaced 2π
  apart, each pair a conjugate pair. Check one root: cos(i ln(2 + √3)) = cosh(ln(2 + √3))
  = ½(2 + √3 + 1/(2 + √3)) = ½(2 + √3 + 2 − √3) = 2 (ch3's reciprocal trick). Contrast with s2: a
  polynomial of degree N has exactly N roots; cos z − 2 has infinitely many.
- s7_recap · Recap (~65 s): the wave and the line y = 2 → "no real solution"; the peeling chain →
  "N roots for degree N"; the split card → "real and imaginary parts"; the case tree → "only x = 2πm
  survives"; the lattice → "infinitely many, 2π apart". Try it yourself: cos z = −2 (N odd, so the
  crosses shift by π). Next: circles, ellipses and hyperbolas. End card.
Continuity: uses ch1's dictionary, ch2's addition formula, and ch3's two-branch cosh⁻¹ and reciprocal
step. ∅ in RED and the kept case in GREEN, as ch3's rejected and kept roots.

## Chapter 5 · Circles and ellipses
Slug: ch5_circles_ellipses · ~10.5 min · Source: notes pp. 40–44 (§3.5.1–3.5.2, (98)–(101); Example 36 on p. 43 is blank: the working is in the digest, 40:00–44:08); lecture 32:42–44:58
Goal: recognise a circle or an axis-aligned ellipse from its equation by completing the square, read
off the centre, radius or semi-axes, write both in parametric form, and give the ellipse's area.
Scenes:
- s1_hook · Hook (~45 s): last time: cos z = 2. The lecturer calls this part a review, so the video
  moves calmly and slows down at the step people slip on. Example 36's equation
  2x² + 4x + y² − 6y + 7 = 0 on screen: what shape is it, and where? (Solved in s6.)
- s2_circle · The circle's equation (~85 s): every point at distance r from the centre: x² + y² = r² (98).
  Centre (x₀, y₀): subtract before squaring. Expand to x² + ax + y² + by + c = 0 (99): a circle can hide
  in this form.
- s3_complete · Completing the square (~105 s): x² + ax = (x + a/2)² − (a/2)², the same in y; so
  r² = (a/2)² + (b/2)² − c and the centre is (−a/2, −b/2). The lecturer's warning: not every equation of
  this form is a circle. r² > 0 gives a circle, r² = 0 a single point, r² < 0 nothing. Worked:
  x² − 2x + y² = 0 → (x − 1)² + y² = 1 (the circle of Examples Sheet E2); x² + 2x + y² + 2 = 0 →
  (x + 1)² + y² = −1, no points at all.
- s4_ellipse · A stretched circle (~105 s): rewrite (98) as (x/r)² + (y/r)² = 1: the same scale both
  ways. Different scales: (x/a)² + (y/b)² = 1 (100). x = 0 gives y = ±b, y = 0 gives x = ±a; a and b are
  the semi-axes, the larger the semi-major, the smaller the semi-minor; a > b lies wide, b > a stands
  tall (the notes' two pictures). Shift the centre as for the circle. Preview from the notes: tilted
  ellipses come in NST IB (matrix form xᵀAx = s); in the general form Ax² + Bxy + Cy² + Dx + Ey + F = 0
  the tilt is the xy term, so an equation with no xy term is lined up with the axes.
- s5_param · cos and sin draw both (~75 s): circle: x = x₀ + r cos θ, y = y₀ + r sin θ, 0 ≤ θ < 2π
  (check with cos² + sin² = 1); ellipse: x = x₀ + a cos θ, y = y₀ + b sin θ. A point running round each.
  For the ellipse θ is a parameter, not the angle the point makes. Sets up ch6, where cosh and sinh
  draw the hyperbola.
- s6_example · Example 36 (~125 s): 2x² + 4x + y² − 6y + 7 = 0. Factor the 2 out first:
  2(x² + 2x + 1) − 2 (adding 1 inside the bracket adds 2, so subtract 2 outside: the classic slip);
  (y² − 6y + 9) − 9; constants −2 − 9 + 7 = −4 → 2(x + 1)² + (y − 3)² = 4 → divide by 4 →
  ((x + 1)/√2)² + ((y − 3)/2)² = 1. Centre (−1, 3); a = √2 ≈ 1.41, the semi-minor axis, along x; b = 2,
  the semi-major axis, along y. Sketch: a tall ellipse from y = 1 to 5 and x from about −2.41 to 0.41,
  so it pokes across the y-axis (the lecturer pointed this out).
- s7_area · Area and circumference (~65 s), then s8_recap (~50 s; the writer split the recap off): stretching a unit circle by a and b multiplies its area
  π by ab: A = πab (101); Example 36's is 2√2 π ≈ 8.9. But the circumference is not π(a + b) (the
  lecturer's warning; it needs elliptic integrals, beyond this year's course). Recap: the completed
  square → "centre and radius"; the stretched circle → "semi-major and semi-minor axes"; the running
  point → "cos and sin draw both"; Example 36 → "factor, complete, divide". Next: flip one plus sign to
  a minus. End card.
Continuity: circle and ellipse in BLUE, semi-major GOLD, semi-minor GREEN, centre YELLOW. Example 36's
ellipse returns in ch6 s5; the running point of s5 returns beside the hyperbola in ch6 s3.

## Chapter 6 · Hyperbolas and the conic family
Slug: ch6_hyperbolas · ~10.5 min · Source: notes pp. 44–45 (§3.5.3, (102), Figures 27–28); the closing summary was handwritten on a separate sheet (digest 49:18–54:55; the final version from 51:39); Examples Sheet I p. 9 (section G); lecture 44:58–54:55
Goal: draw x² − y² = s² and y² − x² = s², parametrise them with cosh and sinh, classify any
ax² + bx + cy² + dy + e = 0 by completing the square, and get started on the G questions.
Scenes:
- s1_hook · Hook (~45 s): last time: circles and ellipses. Flip the plus in x² + y² = r² to a minus.
  And ch1's open question: why are cosh and sinh called hyperbolic?
- s2_hyperbola · Flip one sign (~95 s): x² − y² = s² (102), s a non-zero real constant;
  y = ±√(x² − s²), real only when |x| ≥ |s|. The four quarter-pieces (+√ and −√, for x > s and for
  x < −s, as the lecturer labelled Figure 27) join into two branches, with vertices at ±s and an empty
  band between. One observation beyond the notes, for sketching: far out, √(x² − s²) ≈ |x|, so the
  branches approach the lines y = ±x.
- s3_param · cosh and sinh draw it (~105 s): x = r cosh θ, y = r sinh θ → x² − y² = r²(cosh² θ − sinh² θ)
  = r² (ch2's identity), so r = ±s, and each sign gives one branch (cosh θ ≥ 1, so x keeps r's sign);
  y needs no ± because sinh θ takes every real value. The two running points side by side,
  (cos θ, sin θ) on the circle and (cosh θ, sinh θ) on the hyperbola (ch1's glimpse, now explained):
  circular functions draw circles, hyperbolic functions draw hyperbolas. θ here is a parameter, not an
  angle.
- s4_turn · A quarter turn (~60 s): reverse the sign of the right-hand side: x² − y² = −s², that is
  y² − x² = s². x and y swap roles; the branches open up and down, vertices (0, ±s);
  x = s sinh θ, y = ±s cosh θ (Figure 28).
- s5_classify · One equation, many shapes (~115 s): every curve today except the tilted ellipse fits
  ax² + bx + cy² + dy + e = 0 (no xy term). Complete both squares: a(x − x₀)² + c(y − y₀)² = f. The
  lecturer's table, final board version: circle a = c and f/a > 0; ellipse ac > 0, af > 0, a ≠ c;
  hyperbola ac < 0, f ≠ 0; nothing ac > 0, af < 0. Warn: here a and c are coefficients, not the
  semi-axes (the lecturer flagged the letter clash herself). Run Example 36 through it: a = 2, c = 1,
  f = 4, so ac > 0, af > 0, a ≠ c: an ellipse.
- s6_odd_cases · The odd cases (~70 s): f = 0 with ac < 0 gives two crossing lines (x² − y² = 0, so
  y = ±x); f = 0 with ac > 0 a single point (x² + y² = 0); a missing squared term a parabola (y = x²);
  even two parallel lines (x² = 1). "One equation, a lot of possibilities." That closes Chapter 3 of the
  notes.
- s7_hints · Examples Sheet G: four hints (~90 s): four question cards (reused in ch7 s1). G1, tanh(x + y):
  Example 33 with new letters; try it from exponentials too. G2, the two loci: eliminate θ with
  cos² + sin² = 1 and cosh² − sinh² = 1, then ask which part of the curve the point really reaches
  (cosh θ ≥ 1). G3, six sketches: pair each function with its inverse (a reflection in y = x), and mark
  intercepts and asymptotes. G4: start from Example 34, and split the log of a quotient before
  differentiating. Pause and try; the solutions are in the bonus chapter.
- s8_recap · Recap (~55 s): a small hyperbola with its four quarter-pieces → "x² − y² = s²"; the two
  running points → "cosh and sinh draw the hyperbola"; the turned pair → "flip the right-hand side";
  the table → "complete the squares, read the signs". Next time: differentiation (Chapter 4 of the
  notes); the bonus chapter has the G solutions. End card.
Continuity: hyperbola in TEAL (the hyperbolic world), circle and ellipse BLUE as in ch5. The
circle–hyperbola pair from ch1 s1 and ch2 s2 is paid off in s3. The four G cards are built here.

## Chapter 7 · Solutions to Examples Sheet G
Slug: ch7_solutions · ~9 min (bonus) · Source: Examples Sheet I p. 9 (G1–G4; no printed answers, so derive and verify each with sympy), drawing on notes pp. 31–45
Goal: worked solutions to G1–G4, with the tempting mistakes.
Scenes:
- s1_intro · Spoilers ahead (~45 s): pause and try first; the four cards from ch6 s7.
- s2_g1 · G1: tanh(x + y) (~100 s): fastest, sinh(x + y)/cosh(x + y) from (95), divided through by
  cosh x cosh y → (tanh x + tanh y)/(1 + tanh x tanh y). A third route, from exponentials:
  tanh u = (e^{2u} − 1)/(e^{2u} + 1), and Example 34 gives e^{2x} = (1 + tanh x)/(1 − tanh x); multiply
  out for the same answer. Check with the sign-flip rule from tan(x + y). Pitfall: missing the hidden
  sinh·sinh in tanh x tanh y and leaving a minus in the denominator.
- s3_g2 · G2: two loci (~125 s): (i) x/a = cos θ, y/b = sin θ → x²/a² + y²/b² = 1: an ellipse with
  semi-axes |a| and |b| (a circle when |a| = |b|), all of it. (ii) x/a = cosh θ, y/b = sinh θ →
  x²/a² − y²/b² = 1: a hyperbola, but only one branch: x/a = cosh θ ≥ 1, so x has the sign of a (the
  right branch when a > 0). Sketch with asymptotes y = ±(b/a)x. Pitfall: the Cartesian equation has two
  branches; the parametrised set has one (ch6: each sign of r gives one branch).
- s4_g3 · G3: six sketches (~115 s): pairs mirrored in y = x: e^x and ln x; sinh x and sinh⁻¹ x (through
  0 with slope 1, then growing slowly, like a log); tanh x and tanh⁻¹ x (the horizontal asymptotes at
  ±1 become vertical). cosh x on its own (minimum 1 at 0, even). For each: intercepts, asymptotes,
  symmetry, domain.
- s5_g4 · G4: tanh⁻¹ as a log, and its derivative (~105 s): from Example 34,
  tanh⁻¹ x = ½ ln[(1 + x)/(1 − x)] = ½[ln(1 + x) − ln(1 − x)], |x| < 1. Differentiate (A-level rules):
  ½[1/(1 + x) + 1/(1 − x)] = 1/(1 − x²). Pitfall: the chain-rule minus from ln(1 − x). Checks: positive
  on (−1, 1), so increasing, as the graph; 1 at x = 0, ch3's near-linear start; blows up at ±1, the
  vertical asymptotes. Optional cross-check: dy/dx = 1/(dx/dy) = 1/sech² y = 1/(1 − tanh² y) = 1/(1 − x²),
  with ch2's identity (d tanh y/dy = sech² y is sheet question H2(g), next lecture's material).
- s6_recap · Recap (~60 s): the four cards, each with its key picture (the formula; the one-branch
  hyperbola; the mirrored pairs; the derivative's graph). Next time: differentiation. End card.
Continuity: question cards match ch6 s7. Uses ch2's (95) and rule, ch3's graphs and Example 34, ch5's
ellipse and ch6's branches.

## Decisions
- **6 core chapters + a bonus (~61 + 9 min).** The recording has ~52 min of material after the L10
  recap (03:12–54:55), with no slack: Example 35 alone took 8 minutes. Each chapter is one section
  of the notes: §3.1 → ch1, §3.2 → ch2, §3.3 + §3.4 → ch3, Example 35 → ch4, §3.5.1–3.5.2 → ch5,
  §3.5.3 + the summary → ch6. The inverses need the graphs (monotonic pieces, ranges, branches), so
  §3.3 and §3.4 share ch3. The conics get two chapters because the lecture spends 22 min on them. The
  core runs a minute over the studio's 60 because the lecture is dense; every chapter is within 8–11
  minutes.
- **Retitled "Hyperbolic Functions and Conics".** A third of the lecture is §3.5, and ch5–ch6 would
  look off-topic under the old title. The folder name is unchanged.
- **One reorder.** The fundamental theorem of algebra (§2.7, end of Ch 2, lectured 03:12–04:43) moves
  from the start to ch4 s2. That way ch1 answers one question (what are cosh and sinh?). And the
  theorem lands where it means most: just before an equation with no real solution (cos z = 2) turns
  out to have infinitely many complex ones, against "exactly N roots for degree N". L10's transcript
  doesn't reach §2.7, so L10's plan should leave p. 30 to this project.
- **Exercises.** Section G (G1–G4) gets hints at the end of ch6 and worked solutions in ch7 (no answers
  are printed for G). G has no conic question apart from G2. E2 (polar form of a circle) and F11 (circles
  as contours of 1/z) belong to earlier sections; F11 is already done in supervision 3, so ch5 only
  borrows E2's circle as an example. H2's hyperbolic derivatives belong to next lecture.
- **Supervision 3** (F7–F12) has no hyperbolic work yet, so G is still ahead and the hint and solution
  chapters matter. It also shows completing the square for circles is already comfortable, so ch5 keeps
  that brisk and spends its time on the ellipse and on Example 36's factor-out-the-2 step.
- **Small additions beyond the notes**, one beat each: e^x = cosh x + sinh x (ch1); the name "Osborn's
  rule" (ch2); arsinh as another name, and the sinh⁻¹ graph (ch3, for G3); the z³ − 1 example, the
  root check and a cos z = −2 prompt (ch4); E2's circle, a no-points example and Example 36's area (ch5);
  the asymptotes y = ±x, the parallel-lines example x² = 1, and "θ is a parameter, not an angle"
  (ch5–ch6). Left out: only the L10 recap (00:00–03:12, used for ch1's "last time") and the
  announcements after 54:55.
- **Source conflicts: the notes win.** tanh⁻¹ x = ½ ln[(1 + x)/(1 − x)] with square brackets and |x| < 1
  (the digest has a modulus); "tanch" (the digest says "tansh"). cosh⁻¹ needs x ≥ 1 (the lecturer said
  "between −1 and 1" at 21:08, then corrected herself). sinh⁻¹ has √(x² + 1) (18:23 says "x plus 1").
  Example 36's constants are −2 − 9 + 7 = −4 (41:57, "7 minus 11"). The conic table is the lecturer's
  final board version, with a, c, f, after her b → c correction at 50:00–51:39.
- **Notation.** e^x throughout (the notes mix exp(x) and e^x). θ is the parameter for circle, ellipse
  and hyperbola, as in the notes, and in G2.
- **Voice.** The maths voice rules above (also added to COURSE.md) are untested with the clone. Voice ch1
  and run its QA before the other chapters are voiced, and fix the rules in COURSE.md if a form fails
  ("tanch", "shine", "E to the ex" and "zed" are the uncertain ones). L10 is planned in parallel and
  will lean on "eye" and "E to the eye theta" even more; its first voice run tests the same forms.
