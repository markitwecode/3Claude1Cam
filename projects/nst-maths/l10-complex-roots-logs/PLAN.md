# Powers, Logarithms and Oscillations: plan

Request: "make 3Blue1Brown-style videos of this maths lecture"; "all the lecture notes are on the
course web page" (via the producer, 2026-11-01). This is NST Part IA Mathematics, Course B
(Mathematical Methods I, N. G. Berloff), **Lecture 10**, Thursday 29 October 2026 (confirmed in
Decisions). Audience: a Cambridge first-year studying the course, very likely a CST student (the
studio's other courses are FoCS and Digital Electronics, and CST students take this maths
course). They know A-level maths: the binomial expansion, geometric series, trig identities. From
Lecture 9 (not in our series) they know z = x + iy, the Argand diagram, modulus and argument,
the principal argument, polar and exponential form, multiplication and division, and the roots of
unity. Their supervision 3 work (`../source/HW math supo 3.pdf`) covers sheet sections D, E and
F5–F12, all correct; F12 (De Moivre) is already done. Their physics may be GCSE-level only: a CST
student asked the lecturer exactly that at the end (00:56:12).
Sources: the typeset notes with blanks (`../source/Chapter234_to_annotate.pdf`), PDF pp. 19–29
(printed pp. 100–110), plus pp. 15–19 for the refresher. p. 30 (§2.7) belongs to L11 (Decisions).
The lecturer's handwritten fills (`../source/Lecture10_scanned.pdf`, 12 pp.). The 60-min recording
(`../source/l10-lecture.{transcript,digest}.md`, frames from `l10-lecture.mp4`): teaching runs
00:00:00–00:55:40, then one student question. Examples Sheet I (`../source/M26examples1
(2).pdf`), section F, PDF pp. 8–9. Where the digest disagrees with the notes or the scan, they win
(see Decisions).
Total: 8 chapters (7 + a bonus), ~75 min of narration (~11,900 words): 7 core chapters ~63 min,
bonus ~11 min.

Every formula, example and exercise answer below was checked numerically in Python (Decisions,
"Checked"). Script-writers still check their own (project.json `toolchain`).

Lecture-wide conventions (set in ch1, kept to the end):
- **Notation, as in the notes:**
  - z = x + iy = |z| e^{iθ}; modulus |z|; argument arg z = θ + 2πn, n ∈ ℤ; principal argument
    −π < θ ≤ π; conjugate z*. Euler's formula (71): e^{iθ} = cos θ + i sin θ.
  - On screen, write e^{…} throughout, not the notes' exp(…), except for a long exponent where
    exp[…] reads better. Say once in ch1 that the notes write both.
  - The integer that counts full turns is n, and the term is written "+ 2πn" after the angle:
    π/2 + 2πn. The notes sometimes write 2nπ; we always write 2πn. Exception: the roots of unity
    in ch1 s3 keep Figure 23's letters (degree n, counter m). ch1 s4 says once that from then on
    n counts turns.
  - Other letters, settled by the scripts (continuity review, 2026-11-01): ch1 s5's general recipe
    writes the power as k ("zed to the K equals W"), so n only counts turns. ch2 follows the notes,
    n = the power, and says so aloud. Where n is taken by something else, m counts the turns: ch3
    (N terms, θ = 2πm) and ch8's F16 (the sheet's n is the power). ch7 calls the current "the
    current" or "I zero", never next to i in one breath; ch8 has no current.
  - ln z means **all** the values, as in the course. A principal value carries a small GREEN tag,
    "principal value". No capital-L "Ln": the lecturer says the course doesn't use it (00:36:00).
    ch4 s6 says so once.
  - Re[…] and Im[…], as in the lecturer's handwriting (the notes print ℜ).
  - Equation numbers (71), (73), (77), (78), (79), (81), (82), (83) sit small and DIM beside
    their formulas, so the viewer can find them in the notes.
  - The oscillator's complex amplitude is A = α + iβ while it's being matched to a and b (ch6 s3,
    s5). The lecturer used c̃ + id̃ (see Decisions).
- **Names:** "Argand diagram"; "modulus"; "argument"; "principal argument"; "principal value";
  "roots of unity"; "De Moivre's theorem"; "geometric progression" (the notes' term; "geometric
  series" is fine too); "complex logarithm"; "multi-valued"; "complex amplitude"; "simple
  harmonic motion"; "angular frequency"; "complex impedance", glossed once as the notes'
  "complex resistance"; "fundamental theorem of algebra"; "Examples Sheet One, question F15".
- **Cross-references** (as in L11, COURSE.md): the videos are "part one" … "part eight" aloud, the
  title cards' word; "chapter" only for the notes' chapters. An exercise's (i)/(ii) is named by its
  content ("for sine of three theta"), never "part one".
- **Narration:** the maths voice rules in COURSE.md ("Voice rules"), summarised:
  - Letters as capitals right after a word ("integer N", "constant C", "capacitance C"),
    except z, i, x and y, which are always "zed", "eye", "ex" and "why". Capital N, K, M for the
    integers n, k, m. Impedance Z is "zed" too.
  - e^{iθ} is "E to the eye theta" (untested, as in L11; fallbacks "ee", then "the exponential of
    eye theta"). "cosine" and "sine" in full, never "cos" or "sin"; powers as "cosine cubed of
    theta", as L11 says "cosh squared of ex". ln is "log" ("log of two eye"). |z| is "mod zed", arg z
    is "arg zed". Re and Im are "the real part of", "the imaginary part of".
  - Subscripts: "zed one", "V zero", "I zero". Never "nought" (heard as "not").
  - Read a formula aloud once, while it's on screen, never more than about eight symbols in one
    breath. Mark scope with "all" or a comma: "E to the eye theta, plus E to the minus eye theta,
    all over two". After that, read it by meaning ("the modulus part", "the full turns", "the five
    roots"): strings of symbols can't be followed by ear.
  - Name things with fragile letters by their role: "the cosine coefficient" (a), "the sine
    coefficient" (b), "the complex amplitude" (A), "the current" (I).
- **Colours** (by meaning, from `lib.style`; shared with L11's plan where they overlap):
  - **TEAL: full turns, the 2πn**, and everything it creates: the extra roots, the ladder's rungs,
    the extra values of z^w, and the period 2π/ω (one full turn of the arrow, ch6). It's the
    lecture's main thread. Nothing else is TEAL. (L11 uses TEAL for the hyperbolic functions, which
    never appear here.)
  - PINK: the imaginary unit i and imaginary parts (terms with i, the Im of a result), in every
    chapter of L10 and L11 (the producer's course-wide rule).
  - BLUE: real parts (real terms, cosines, shadows on the real axis), like L11's "circular world".
  - GOLD: e^{iθ} and the turning arrows built from it, and moduli and lengths (r, |z|, 2^{1/5},
    e^{−2πn}, |A|). PURPLE: the conjugate e^{−iθ}. This matches L11's GOLD e^x and PURPLE e^{−x}.
  - GREEN: the principal value or principal argument (the n = 0 choice), like L11's "the branch we
    keep".
  - YELLOW: angles and arguments, the running number 2i, boxed results.
  - RED: pitfalls (dropping the 2πn, a non-integer n in De Moivre, principal values that don't
    add, λ = 1).
  - DIM: grid, unit circle, equation numbers.
  - Two stated exceptions. ch6's velocity arrow iωA e^{iωt} is PURPLE (no conjugate appears in
    ch6). ch7 makes the current I GOLD, so its e^{iωt} factor and the source voltage V are white
    (FG); the resistor's quantities are BLUE and the capacitor's PINK, since they become Z's real and
    imaginary parts. ch8's F19 is an oscillation, not a circuit, so it keeps ch6's GOLD arrow.
- **Running visuals:**
  - *The Argand plane:* axes labelled Re and Im (as in the notes' figures), a faint grid, the unit
    circle DIM. ch1 s2 builds it; every later Argand diagram reuses it. ch1's director records the
    helper's name in STATUS.md.
  - *2i, the lecture's own running number:* z⁵ = 2i (ch1), ln 2i (ch4), and (ours) (2i)^{1/5},
    which brings back ch1's ring (ch5 s6).
  - *The ring of five* (ch1 s5): the circle of radius 2^{1/5} with five dots. Back in ch1's recap
    and ch5 s6.
  - *The ladder* (ch4 s4): the column of values of ln 2i on the line Re w = ln 2, rungs 2π
    apart. Back in ch5 s5.
  - *The turning arrow:* e^{iθ} stepping round (ch2), arrows tip to tail (ch3), the arrow
    A e^{iωt} with its shadow on the real axis (ch6), four arrows turning together (ch7), the
    closed triangle (ch8 F17).
  - *The gallery* (ch5 s6–s7): four small Argand diagrams, for the four kinds of exponent.

## Chapter 1 · Roots of a complex number
Slug: ch1_roots · ~8.5 min · Source: notes PDF pp. 19–20 (Example 28 and the remark above it);
refresher pp. 15–19 (L9's) · Recording: 00:00:00–00:07:45 · Scans: L10 pp. 1–3; L9 pp. 13, 15
Goal: solve z^n = w for any complex w by writing both sides in polar form and keeping the 2πn,
draw the n roots as a ring, and know that n is the right count for degree n.
Scenes:
- s1_hook · Hook (~45 s): title card ("Powers, Logarithms and Oscillations", course line "NST IA
  Mathematics · Lecture 10", part line "Part 1 · Roots of a complex number").
  - On the real line, x⁵ = 32 has one answer, 2.
  - In the plane, z⁵ = 2i: the point 2i (YELLOW) on the imaginary axis. How many zeds, and where?
  - The lecturer's frame (00:00:13–00:01:20): everything comes from definitions; powers and
    logarithms keep their real-number names, but today is about what's *different*.
  - The road in one line: roots (1), De Moivre (2), sums of cosines (3), logarithms (4), powers
    (5), oscillations (6), circuits (7).
- s2_polar · Lecture 9 in one picture (~100 s): refresher, notes pp. 16–17, scan p. 1 (the
  lecturer's recap, 00:01:20–00:03:02), L9's scan p. 13.
  - z = x + iy with i² = −1, a point on the Argand diagram. Modulus |z| (GOLD) is its distance
    from 0; argument θ (YELLOW) is its angle from the positive real axis.
  - z = |z|(cos θ + i sin θ) = |z| e^{iθ}, by Euler's formula (71), which the course proves later
    (§6.3). The real part BLUE, the imaginary part PINK.
  - Multiplying multiplies moduli and adds arguments, (73) and Figure 22: show z₁z₂ appear. The
    conjugate z* = |z| e^{−iθ} is the reflection (one line).
  - The argument is multi-valued: θ + 2πn, n ∈ ℤ, is the same point, because e^{2πin} = 1 (L9's
    scan p. 13). Animate the arrow sweeping one full turn and landing where it started. 2πn TEAL.
  - Principal argument: −π < θ ≤ π. Minus pi is left out, so each point gets exactly one
    (00:02:41–00:02:58, the lecturer's emphasis). GREEN.
  - Close: "keep an eye on that 2πn; this whole lecture is about what it does."
- s3_unity · Roots of unity (~70 s): L9's last example, notes pp. 18–19, Figure 23; L9's scan
  p. 15; 00:03:10–00:03:35.
  - z⁴ = 1: z = r e^{iθ}, so r⁴ e^{4iθ} = 1. Then r = 1 and 4θ = 2πm, so θ = πm/2: 1, i, −1, −i.
    m = 4 gives 1 again. L9's words: "infinitely many in θ, but four distinct in z".
  - z^n = 1: z = e^{2πim/n}, m = 0, …, n − 1. These are n points spaced 2π/n apart round the unit
    circle, starting at 1 (Figure 23).
- s4_method · Example 28: three steps (~105 s): notes pp. 19–20, scan p. 2, 00:03:39–00:05:30.
  - Solve z⁵ = 2i. Left side: z = r e^{iθ}, so z⁵ = r⁵ e^{5iθ}.
  - Right side in the same form. |2i| = 2 and its angle is π/2 (show 2i straight up at height 2).
    Keep every version: 2i = 2 e^{i(π/2 + 2πn)}, with the 2πn in TEAL. The printed notes have
    2e^{iπ/2}; the lecturer added the 2πn by hand.
  - Equate moduli: r⁵ = 2, so r = 2^{1/5}, the real positive fifth root, about 1.149 (GOLD).
  - Equate arguments: 5θ = π/2 + 2πn, so θ = π/10 + 2πn/5.
  - Say once: here n counts full turns. It isn't the degree, as it was in Figure 23.
  - The pitfall (RED): drop the 2πn before dividing by five and you find one root, not five.
    Dividing turns whole turns into fifths of a turn, and those are the other roots.
- s5_ring · The ring of five (~105 s): notes p. 20, scan p. 3 (diagram), 00:05:30–00:07:45.
  - Fill the table n = 0 to 4: π/10; 5π/10 = π/2 (that's 2^{1/5} i, pure imaginary, the
    lecturer's annotation); 9π/10; 13π/10; 17π/10. n = 5 gives π/10 + 2π: "same as n = 0"
    (scan). A dot appears on the plane as each row fills.
  - The picture: a circle of radius 2^{1/5}, not the unit circle; the first dot at angle π/10,
    not on the real axis; neighbours 2π/5 = 4π/10 apart. The lecturer contrasts it with the roots
    of unity (00:07:17–00:07:43).
  - Ours: the ring is the five fifth roots of unity, scaled by 2^{1/5} and turned by π/10. Show
    s3's unit-circle pentagon (redrawn for n = 5) scaling and turning onto this ring.
  - 13π/10 and 17π/10 are fine as written. Their principal arguments are −7π/10 and −3π/10, the
    same points.
  - The recipe in general (ours, one line): if z^k = w, then |z| = |w|^{1/k}, and the arguments
    are (arg w + 2πn)/k for n = 0, …, k − 1.
  - Why five, and no more: the remark printed just above Example 28 (p. 19, on screen at
    00:03:35), "for any polynomial of degree n, there will always be n roots in the complex plane
    (counted with multiplicity)". The lecturer's margin note names it: "the fundamental theorem of
    algebra (see §2.7)". z⁵ − 2i has degree 5, and we found five different roots, so that's all of
    them. One sentence only: Lecture 11 states and explains the theorem.
- s6_recap · Try it, and recap (~75 s):
  - Examples Sheet I, F15 (p. 8): z³ = −1, z⁴ = 1, z² = i, z³ = −i. Hint: the same three steps.
    The argument of −1 is π, and of −i it's −π/2. Keep the 2πn.
  - F16 (p. 9): put w = zⁿ. The equation becomes a quadratic in w, and each w gives a ring of n
    roots of radius |w|^{1/n}. Full solutions in Part 8.
  - Recap, with small versions of:
    - the point with its modulus, angle and full-turn sweep (s2);
    - the four roots of unity (s3);
    - the three steps, with the 2πn in TEAL (s4);
    - the ring of five, with "degree 5, five roots" (s5).

  Next time: raise e^{iθ} to the power N. De Moivre's theorem, and cos 4θ in one line. End card.
Continuity: sets the Argand plane, the colours, 2πn in TEAL and principal values in GREEN. 2i and
the ring come back in ch4 (ln 2i) and ch5 ((2i)^{1/5}). "Multiplying adds angles" is ch2's proof.
The fundamental theorem of algebra itself is L11's (its ch4 s2).

## Chapter 2 · De Moivre's theorem
Slug: ch2_de_moivre · ~9 min · Source: notes PDF pp. 20–21 (§2.4, Example 29, (77), (78)) ·
Recording: 00:07:45–00:13:36 · Scans: L10 pp. 3–4
Goal: state and prove De Moivre's theorem and say why n must be an integer; use it to write cos 4θ
and sin 4θ in terms of cos θ and sin θ; write cos θ and sin θ as exponentials.
Scenes:
- s1_hook · Hook (~40 s): part line "Part 2 · De Moivre's theorem".
  - Last time: z⁵ = 2i gave five roots in a ring (small).
  - The question: what is cos 4θ in terms of cos θ? Applying the double-angle formula twice is a
    page of algebra. De Moivre gets it from one fourth power.
- s2_theorem · The theorem (~90 s): §2.4, notes p. 20, scan p. 3, 00:07:45–00:09:29.
  - If z = cos θ + i sin θ = e^{iθ}, then zⁿ = (cos θ + i sin θ)ⁿ = (e^{iθ})ⁿ = e^{inθ}
    = cos nθ + i sin nθ.
  - De Moivre's theorem, boxed: cos nθ + i sin nθ = (cos θ + i sin θ)ⁿ.
  - The picture, from ch1's "multiplying adds angles": the unit arrow at θ (GOLD). Multiply it
    by itself again and again: 2θ, 3θ, 4θ. Each step turns it by θ more, and its length stays 1.
  - The lecturer: "the proof is rather trivial… very good times, when putting your name on a
    theorem didn't require much labour" (00:08:01). She uses modulus 1 for simplicity. With a
    general modulus r, it just becomes rⁿ (ours).
  - n can be negative. n = −1 gives cos θ − i sin θ, turning back (ours, one line).
- s3_integer · Why n must be an integer (~70 s): notes p. 20 (last line), scan p. 3
  ("(e^{iθ})ⁿ = e^{inθ}, n ∈ ℤ"), 00:08:32–00:08:57.
  - The notes: "n must be an integer here: for other n the left-hand side is multivalued."
  - Show it with ch1's 2πn (ours): e^{iθ} is also e^{i(θ + 2π)}. Take n = ½. Halving the first
    angle gives e^{iθ/2}; halving the second gives e^{iθ/2 + iπ} = −e^{iθ/2}. Two different points
    (TEAL), so "(e^{iθ})^{1/2}" isn't one number (RED).
  - For a whole number n, n × 2π is a whole number of turns, so every version lands on the same
    point.
  - That's exactly why ch1 found five fifth roots. Teaser: Part 5 counts the values of any power.
- s4_expand · Example 29: expand (~105 s): notes p. 21, scan p. 4, 00:09:44–00:10:53.
  - The task, with the lecturer's handwritten ending: cos 4θ and sin 4θ "in terms of cos θ and
    sin θ".
  - By the theorem: cos 4θ + i sin 4θ = (cos θ + i sin θ)⁴.
  - Expand as (a + b)⁴. The coefficients 1, 4, 6, 4, 1 come from Pascal's triangle (show the row).
  - Powers of i: i² = −1, i³ = −i, i⁴ = 1. Show a small dial with i turning a quarter turn each
    time.
  - The five terms: cos⁴θ + 4i cos³θ sin θ + 6i² cos²θ sin²θ + 4i³ cos θ sin³θ + i⁴ sin⁴θ
    = cos⁴θ − 6cos²θ sin²θ + sin⁴θ + 4i(cos³θ sin θ − cos θ sin³θ).
  - As they settle, terms without i turn BLUE (real) and terms with i turn PINK (imaginary).
- s5_simplify · Real and imaginary parts (~95 s): notes p. 21, scan p. 4, 00:10:53–00:12:13.
  - Real parts: cos 4θ = cos⁴θ − 6cos²θ sin²θ + sin⁴θ.
  - Imaginary parts: sin 4θ = 4(cos³θ sin θ − cos θ sin³θ). That's the goal met.
  - In cos θ alone, line by line as in the notes, using sin²θ = 1 − cos²θ:
    cos⁴θ − 6cos²θ(1 − cos²θ) + (1 − cos²θ)²
    = cos⁴θ − 6cos²θ + 6cos⁴θ + 1 − 2cos²θ + cos⁴θ = 8cos⁴θ − 8cos²θ + 1.
  - sin 4θ = 4cos θ sin θ(cos²θ − sin²θ) = 4cos θ sin θ(2cos²θ − 1)
    = 4cos θ sin θ(1 − 2sin²θ). These are the lecturer's handwritten forms, from
    cos²θ + sin²θ = 1.
  - A check (ours): at θ = π/4, cos π = −1, and 8·¼ − 8·½ + 1 = −1.
- s6_expo · Cosine and sine as exponentials (~85 s): notes p. 21 (bottom), scan p. 4,
  00:12:14–00:13:36.
  - (71): e^{iθ} = cos θ + i sin θ. Its conjugate: e^{−iθ} = cos θ − i sin θ.
  - Add them: cos θ = ½(e^{iθ} + e^{−iθ}) (77). Subtract: sin θ = (1/2i)(e^{iθ} − e^{−iθ}) (78).
  - The picture (ours): two unit arrows turning opposite ways, e^{iθ} GOLD and e^{−iθ} PURPLE.
    Tip to tail, their sum always lands on the real axis at 2cos θ (BLUE). Their difference lands
    on the imaginary axis at 2i sin θ (PINK); dividing by 2i brings it back to a real number.
  - The lecturer: "working with exponentials is easier than working with cosines and sines."
- s7_recap · Recap (~50 s): small versions of:
  - the arrow stepping θ, 2θ, 3θ (s2);
  - the two square roots, half a turn apart (s3);
  - Pascal's row and the i dial (s4);
  - cos 4θ = 8cos⁴θ − 8cos²θ + 1 (s5);
  - the two opposite arrows (s6).

  Next time: (77) and (78) turn powers like cos³θ into single cosines, and sums of cosines into
  geometric series. End card.
Continuity: the unit arrow and "multiplying adds angles" come from ch1; the 2πn is TEAL again in
s3. (77) and (78) are ch3's tools. F12's hint is in ch3, since part ii needs ch3's method.

## Chapter 3 · Powers and sums with exponentials
Slug: ch3_trig_sums · ~9.5 min · Source: notes PDF pp. 22–23 (cos³θ, (79), Example 30) ·
Recording: 00:13:36–00:19:14 · Scans: L10 pp. 5–6
Goal: rewrite cos³θ as a sum of single cosines, and sum 1 + cos θ + … + cos(N−1)θ as the real
part of a geometric series, including the case θ = 2πm.
Scenes:
- s1_hook · Hook (~40 s): part line "Part 3 · Powers and sums with exponentials".
  - Last time: cos θ = ½(e^{iθ} + e^{−iθ}) and its partner for sin θ.
  - Two questions. How would you integrate cos³θ? (The lecturer's reason: we can integrate the
    cosine of a multiple of θ, but not a power.) And what is 1 + cos θ + cos 2θ + … + cos(N−1)θ?
- s2_cube · Cos cubed (~95 s): notes p. 22 (top), 00:13:36–00:14:25.
  - cos³θ = [½(e^{iθ} + e^{−iθ})]³ = ⅛[e^{3iθ} + 3e^{2iθ}e^{−iθ} + 3e^{iθ}e^{−2iθ} + e^{−3iθ}],
    using the binomial row 1, 3, 3, 1.
  - Pair the mirror terms: ⅛[e^{3iθ} + e^{−3iθ}] + ⅜[e^{iθ} + e^{−iθ}] = ¼cos 3θ + ¾cos θ. By
    (77), each pair is twice a cosine.
  - The picture: each mirror pair of arrows closes onto the real axis (a callback to ch2 s6).
  - Why it helps (ours): ∫cos³θ dθ = (1/12)sin 3θ + ¾ sin θ + C. A check: at θ = 0, 1 = ¼ + ¾.
- s3_sum · A sum of cosines as a real part (~75 s): notes p. 22, scan p. 5, 00:14:25–00:16:14.
  - S_N = Σ_{k=0}^{N−1} cos kθ = 1 + cos θ + cos 2θ + … + cos(N−1)θ, written out as the lecturer
    did.
  - Since cos kθ = Re(e^{ikθ}): S_N = Re[Σ e^{ikθ}] (79).
  - Σ e^{ikθ} = Σ (e^{iθ})^k = 1 + e^{iθ} + e^{2iθ} + …: each term is the one before times e^{iθ}.
    It's a geometric progression, first term 1, common ratio e^{iθ}.
  - The picture (ours): unit arrows placed tip to tail, each turned θ further than the last, so
    the chain curls round. The real-axis shadow (BLUE) of the whole chain is S_N.
- s4_geometric · Geometric series, recalled (~55 s): notes p. 23 ("recall"), 00:16:14–00:17:05.
  - Σ_{k=0}^{N−1} aλ^k = a(1 − λ^N)/(1 − λ), for λ ≠ 1.
  - Why (ours, A-level, one line): S − λS = a − aλ^N. The algebra is the same for complex λ.
  - λ ≠ 1 matters, since the formula divides by 1 − λ. Keep a small RED flag on it for s6.
- s5_conjugate · Example 30: a real denominator (~105 s): notes p. 23, 00:17:05–00:17:53.
  - With a = 1 and λ = e^{iθ}: S_N = Re[(1 − e^{iNθ})/(1 − e^{iθ})].
  - You can't read off the real part of a fraction whose bottom is complex. Make the bottom real:
    multiply top and bottom by the conjugate, 1 − e^{−iθ}, as in L9's division (Example 27,
    p. 15).
  - Bottom: (1 − e^{iθ})(1 − e^{−iθ}) = 2 − e^{iθ} − e^{−iθ} = 2 − 2cos θ = 2(1 − cos θ), real
    by (77).
  - Top: 1 − e^{−iθ} − e^{iNθ} + e^{i(N−1)θ}.
- s6_result · The answer, and θ = 2πm (~90 s): notes p. 23 (bottom), scan p. 6, 00:17:41–00:19:10.
  - The real part of the top: 1 − cos θ − cos Nθ + cos(N−1)θ. The sines (PINK) drop out.
  - S_N = [1 − cos θ − cos Nθ + cos(N−1)θ] / [2(1 − cos θ)]
    = ½ + [cos(N−1)θ − cos Nθ] / [2(1 − cos θ)].
  - A check (ours): N = 3, θ = π/2. The sum is 1 + 0 − 1 = 0, and the formula gives
    ½ + (−1 − 0)/2 = 0.
  - The exception (the lecturer's handwritten fill): λ = 1 exactly when θ = 2πm, m ∈ ℤ. Then
    every term is 1, so S_N = 1 + 1 + … + 1 = N. The picture: all the arrows point the same way,
    a straight chain of length N. That's also exactly where the bottom, 2(1 − cos θ), is zero
    (ours).
  - Ours, one line: the imaginary part of the same sum is Σ sin kθ, for free (F13(b)).
- s7_tryit · On the examples sheet (~55 s): Examples Sheet I hints. Full solutions in Part 8.
  - F12 (p. 8). (i) sin 3θ: De Moivre with n = 3, take the imaginary part, then use
    cos²θ = 1 − sin²θ. (ii) sin⁵θ: raise (78) to the fifth (Pascal's row 1, 5, 10, 10, 5, 1) and
    pair the mirror terms into sines, as with cos³θ.
  - F13 (p. 8): (a) and (b) are this chapter's sum, running from 1 to 5; (b) is the imaginary
    part. (c) has common ratio r e^{iθ}.
  - F17 (p. 9): if ω³ = 1, then 1 + ω + ω² is a geometric series with ratio ω (or multiply it
    by ω − 1). Then do the same for any n.
- s8_recap · Recap (~50 s): small versions of:
  - the mirror pairs closing onto the real axis (s2);
  - the curling chain and its shadow (s3);
  - the one-line geometric-series proof (s4);
  - the conjugate making the bottom real (s5);
  - the final formula, and the straight chain for θ = 2πm (s6).

  Next time: run the exponential backwards. What is the logarithm of a complex number, and why
  does it have infinitely many values? End card.
Continuity: (77) and (78) come from ch2, the conjugate trick from L9. The tip-to-tail chain
returns in ch8 (F17's closed triangle). ch4 picks up 2i again.

## Chapter 4 · The complex logarithm
Slug: ch4_logarithm · ~9.5 min · Source: notes PDF pp. 24–25 (§2.5 and the principal-value box)
· Recording: 00:19:14–00:28:21 (the box is on screen 00:26:49–00:28:21), plus 00:35:46–00:36:09
· Scans: L10 pp. 7–8
Goal: define ln z from e^w = z; derive ln z = ln|z| + i(arg z + 2πn) and draw its values as a
vertical ladder 2π apart; handle ln e^z, ln(z₁z₂) and principal values correctly.
Scenes:
- s1_hook · Hook (~40 s): part line "Part 4 · The complex logarithm".
  - Last time: exponentials make trigonometry easy. Today we run them backwards.
  - The question: which w solve e^w = 2i? For real numbers ln gives one answer. Here?
  - The lecturer: "I'm working from what I know… I use this relationship to define what I mean by
    logarithm" (00:20:08); "each time you see the logarithm, you have to go through this
    definition" (00:20:29).
- s2_define · From the definition (~125 s): notes p. 24, scan p. 7, 00:19:14–00:23:32.
  - The notes ask: if z = x + iy = |z| e^{iθ}, what is ln z?
  - Definition: for z ≠ 0, w = ln z if e^w = z.
  - Write w = u + iv and z = |z| e^{iθ}. Then e^w = e^u · e^{iv} = |z| e^{iθ}.
  - Moduli: e^u = |z|, so u = ln|z|. That's the ordinary real log, with one answer, since e^u is
    positive and increasing. GOLD.
  - Arguments: v = θ + 2πn, n ∈ ℤ (TEAL), since two arguments of one point agree only up to
    full turns.
  - The result, boxed: ln z = ln|z| + i(arg z + 2πn).
  - The notes: "infinitely many values spaced 2πi apart on a vertical line in the complex plane".
  - Why z ≠ 0 (ours): e^u > 0, so e^w is never 0, and 0 has no logarithm.
- s3_map · What the exponential does to the plane (~80 s): ours, the 3b1b view of s2's result.
  - Two planes side by side: the w-plane (left) and the z-plane (right), joined by an arrow
    labelled e^w.
  - The real part u sets the distance e^u: a vertical line in w goes to a circle in z. The
    imaginary part v sets the angle: climbing 2π up the line wraps once round the circle.
  - So, going backwards, one point z comes from a whole ladder of w's, 2π apart (TEAL rungs).
  - The real exponential never wraps, so the real log has one value. The complex exponential
    wraps, so the complex log can't have just one.
- s4_ln2i · The ladder for 2i (~85 s): notes p. 24 (handwritten), scan p. 7, 00:23:32–00:25:31.
  - z = 2i, ch1's number: 2i = 2e^{i(π/2 + 2πn)}, as before.
  - ln 2i = ln 2 + i(π/2 + 2πn). The real part is ln 2 ≈ 0.69; the imaginary part is
    π/2 + 2πn.
  - Plot it in the w-plane. Draw the vertical line Re w = ln 2, with dots at heights π/2 (GREEN,
    the principal value) and π/2 ± 2π, ± 4π, … (TEAL). Put a brace marked 2πi between
    neighbours.
  - The lecturer's warning (00:24:59): "notice it's not the angle anymore. This is the actual
    value." The vertical axis here is the imaginary part of w, a height: π/2 is the number 1.57,
    not an angle.
- s5_consequences · Two consequences (~85 s): notes p. 24 (bottom), scan p. 7, 00:25:35–00:27:20.
  - ln e^z = z + 2πin. Going there and back can land on any rung of z's ladder. Example (ours):
    z = 3 + 4i. Since 4 > π, the principal value of ln e^{3+4i} is 3 + (4 − 2π)i, not 3 + 4i.
  - ln(z₁z₂) = ln z₁ + ln z₂ modulo 2πi. As whole sets of values the two sides match, but one
    value from each side may differ by a multiple of 2πi. The lecturer: "they give me the sum,
    but I can also add or subtract 2πi."
  - Even ln 2 is multi-valued: ln 2 + 2πin, and only n = 0 is real (00:26:54). That's next
    chapter's 2^i.
- s6_principal · Principal values (~95 s): the box on notes p. 25, scan p. 8, 00:26:49–00:28:21
  and 00:35:46–00:36:09.
  - The principal value picks −π < θ ≤ π (the box). For a principal arg it's the n = 0 rung:
    GREEN tag "principal value".
  - Notation: this course writes ln for both and doesn't use a capital L. The lecturer: "please
    bear with this abuse of the notation" (00:36:09).
  - The box: the principal values of ln(z₁z₂) and ln z₁ + ln z₂ can differ by 2πi. Example
    (ours; the box cites "sheet 1 question 10" from an older sheet): z₁ = z₂ = −1. The principal
    ln(−1) is iπ, so the sum is 2πi. But z₁z₂ = 1, whose principal ln is 0. The picture: the angles
    π + π = 2π land outside (−π, π] and are pulled back one full turn (RED arc).
  - F18 hint (p. 9): write each number as modulus times e^{i(arg + 2πn)} first, then read off
    ln. For (x + iy)* the argument changes sign; for i r e^{iθ}, multiplying by i adds π/2 to the
    argument. Solutions in Part 8.
- s7_recap · Recap (~55 s): small versions of:
  - the derivation box (s2);
  - the two planes, with a line wrapping into a circle (s3);
  - the ladder for ln 2i (s4);
  - ln e^z landing on a rung (s5);
  - the π + π overshoot (s6).

  Next time: if ln 2 has infinitely many values, so does 2 to the power i. And i to the power i
  turns out to be real. End card.
Continuity: 2i comes from ch1. The ladder returns in ch5 s5. Principal values GREEN, 2πn TEAL.

## Chapter 5 · Complex powers
Slug: ch5_powers · ~10.5 min · Source: notes PDF pp. 25–26 (Example 31; p. 26 is the blank
"General powers" page) · Recording: 00:26:49–00:41:45 · Scans: L10 pp. 8–9
Goal: define z^w = e^{w ln z}; evaluate 2^i and i^i with all their values; say how many values
z₁^{z₂} has when z₂ is an integer, rational, irrational, or has an imaginary part.
Scenes:
- s1_hook · Hook (~40 s): part line "Part 5 · Complex powers".
  - Last time: ln has a ladder of values.
  - The question: what is i to the power i? Hold the answer back (it's real).
- s2_define · The definition (~75 s): scan p. 8 (the lecturer's red "Def z^w := e^{w ln z}"),
  00:26:54–00:28:21.
  - For real numbers a^b = e^{b ln a}, e.g. 2³ = e^{3 ln 2}. Take the same as the definition:
    z^w := e^{w ln z}.
  - It's built from two things already defined, exp and ln: the lecturer's theme again.
  - ln z has many values, so z^w generally does too ("let's keep that in mind", 00:28:19).
  - The Further Maths habit is to use the principal value. That's true, but it's only one of the
    values (00:28:46–00:29:07).
- s3_two_i · Two to the power i (~95 s): Example 31, notes p. 25, scan p. 8, 00:28:21–00:31:14.
  - The principal value (the notes): ln 2^i = i ln 2, so 2^i = e^{i ln 2} = cos(ln 2) + i sin(ln 2).
    It's on the unit circle, at angle ln 2 ≈ 0.69 radians (about 40°).
  - Properly (the lecturer's handwriting): ln 2 is really ln 2 + 2πni. So
    2^i = e^{i(ln 2 + 2πni)} = e^{−2πn} e^{i ln 2} = e^{−2πn}(cos ln 2 + i sin ln 2).
  - n = 0 gives the principal value. Other n change the modulus: e^{−2π} ≈ 0.0019 and
    e^{2π} ≈ 535 (ours).
  - The picture: one ray at angle ln 2, with the values on it at distances e^{−2πn} (TEAL dots,
    GREEN for n = 0). They're too far apart for a linear scale, so use a log-scale strip along
    the ray (ours).
- s4_i_i · i to the power i (~90 s): notes p. 25, scan p. 8, 00:31:14–00:33:58.
  - The notes' route: z = i^i, so ln z = i ln i. With i = e^{i(π/2 + 2πn)}, ln i = i(π/2 + 2πn).
    So ln z = i · i(π/2 + 2πn) = −(π/2 + 2πn), and z = e^{−(π/2 + 2πn)}.
  - The lecturer's shortcut, straight from the definition: i^i = e^{i ln i}
    = e^{i · i(π/2 + 2πn)} = e^{−π/2 − 2πn}. The same answer.
  - Every value is real. The principal value is e^{−π/2} ≈ 0.208. Show the dots on the positive
    real axis (log-scale strip).
  - The lecturer: "probably the hardest problems you're going to get on the complex numbers"
    (00:33:58). The method in one line: write the base as modulus × e^{i(arg + 2πn)}, take ln,
    multiply by the exponent, exponentiate.
- s5_count · How many values? (~80 s): notes p. 26 (blank) and scan p. 9, 00:34:17–00:37:04.
  - z₁^{z₂} = e^{z₂ ln z₁}, with ln z₁ = (principal value) + 2πni.
  - So z₁^{z₂} = e^{z₂ (principal ln z₁)} · e^{2πniz₂}: one fixed number, times a factor that
    depends on n. Bring back the ladder from ch4: each rung gives one factor.
  - The question: as n runs through the integers, how many different numbers does e^{2πniz₂}
    give? It depends on z₂.
  - The notation note: the same "ln" on both sides is a common abuse for multi-valued functions,
    like θ = θ + 2πn (00:35:46).
- s6_finite · Integer and rational exponents (~95 s): scan p. 9 (i), (ii), 00:37:04–00:39:11.
  - (i) z₂ = m ∈ ℤ. The lecturer asks the room what e^{2πinm} is (pause): 1, for every n. One
    value: z₁^m = |z₁|^m e^{imθ₁}, which is De Moivre again.
  - (ii) z₂ = p/q in lowest terms, q > 0. e^{2πipn/q} repeats after q steps (the room's answer:
    q). q distinct values, for n = 0, 1, …, q − 1. Why lowest terms (ours): 2/4 is ½, which has
    two values, not four.
  - The running example comes full circle (ours, checked):
    (2i)^{1/5} = e^{(1/5) ln 2i} = e^{(1/5)(ln 2 + i(π/2 + 2πn))} = 2^{1/5} e^{i(π/10 + 2πn/5)}.
    That's exactly ch1's ring of five: bring it back.
  - The gallery starts: one dot for (i); q dots on a circle for (ii).
- s7_infinite · Irrational and complex exponents (~95 s): scan p. 9 (iii), (iv), 00:39:19–00:41:41.
  - (iii) z₂ real and irrational (√2, say; ours). nz₂ is never a whole number for n ≠ 0, so the
    values never repeat: infinitely many, all with modulus |z₁|^{z₂}. The picture: dots filling
    a circle more and more densely.
  - (iv) z₂ = x + iy with y ≠ 0. |e^{2πinz₂}| = e^{−2πny}, different for every n. So there are
    infinitely many values, with different moduli. The lecturer: "I don't even worry what x is"
    (00:41:19). The picture: dots on a spiral, or on a ray when x = 0, like 2^i.
  - The gallery is complete: one dot | q dots | a dense circle | a spiral.
- s8_recap · Recap (~55 s): small versions of:
  - the definition line (s2);
  - the 2^i ray (s3);
  - the i^i dots on the real axis (s4);
  - the factor e^{2πniz₂} (s5);
  - the gallery (s6–s7).

  Next time: back to the physical world. A swinging pendulum, drawn as the shadow of a turning
  complex arrow. End card.
Continuity: the ladder comes from ch4, the ring from ch1, De Moivre from ch2. The sheet has no
question on general powers (F18 is about logs only), so there are no hints here.

## Chapter 6 · Oscillations and the complex amplitude
Slug: ch6_oscillations · ~8.5 min · Source: notes PDF pp. 27–28 (§2.6, (81)–(83), Figure 24, the
oscillator example) · Recording: 00:41:45–00:46:18 · Scans: L10 pp. 10–11 (p. 10 is scanned
upside down)
Goal: write simple harmonic motion as x(t) = Re[A e^{iωt}] with A = a − ib, differentiate by
multiplying by iω, and solve an initial-value problem by reading the amplitude and phase off A.
Scenes:
- s1_hook · Hook (~40 s): part line "Part 6 · Oscillations and the complex amplitude".
  - Last time: z^w. Now §2.6: complex numbers are "especially useful" for anything that
    oscillates, like pendulums, AC circuits and waves. Their differential equations come next
    term.
  - The question: why describe a real swinging pendulum with a complex number?
- s2_pendulum · Simple harmonic motion (~80 s): notes p. 27, scan p. 10 (the pendulum sketch),
  00:41:45–00:43:03.
  - A pendulum of length l, under gravity g. For small swings its angular frequency is
    ω = √(g/l). Take this as given; the physics comes next term.
  - Its angular displacement is x(t) = a cos ωt + b sin ωt (81), with a and b real: simple
    harmonic motion.
  - What ω means (ours): the angle ωt grows by ω radians per second, so one swing there and back
    takes 2π/ω.
  - The picture: the pendulum swinging beside a graph of x(t).
- s3_phasor · The turning arrow and its shadow (~120 s): notes p. 27 (Figure 24, (82)), scan
  p. 10, 00:43:03–00:44:32.
  - x(t) = Re[A e^{iωt}] (82), where A is a complex constant: the complex amplitude.
  - Figure 24: the arrow A e^{iωt} turns at rate ω round a circle of radius |A|, and its shadow
    on the real axis is x(t). Animate the arrow (GOLD) and the shadow dot (BLUE), with the
    shadow's trace unrolling beside it as a cosine wave (ours).
  - Why A = a − ib. Write A = α + iβ. Then
    Re[(α + iβ)(cos ωt + i sin ωt)] = α cos ωt − β sin ωt. Comparing with (81): α = a and
    β = −b, so A = a − ib.
  - What A tells you (ours): |A| = √(a² + b²) is the size of the swing, and arg A is where the
    arrow starts, the phase. So x(t) = |A| cos(ωt + arg A).
- s4_derivative · Differentiating means multiplying by iω (~85 s): notes p. 28 ((83)),
  00:44:34–00:45:04.
  - v = dx/dt = d/dt Re[A e^{iωt}] = Re[d/dt (A e^{iωt})] = Re[iωA e^{iωt}] (83).
  - The notes: "to differentiate e^{iωt} we simply multiply by iω before taking the real part".
  - Why Re and d/dt can swap (ours): the derivative acts on the real and imaginary parts
    separately.
  - The picture (ours): multiplying by i turns the arrow a quarter turn ahead, and ω stretches
    it. The velocity arrow (PURPLE; no conjugate appears in ch6) leads the position arrow by 90°.
- s5_example · Amplitude and phase from the start (~105 s): notes p. 28, 00:45:04–00:46:16.
  - At t = 0, x(0) = c and v(0) = √3cω.
  - So Re(A) = c and Re(iωA) = √3cω.
  - Write A = c + iβ. Then iωA = iωc − ωβ, whose real part is −ωβ = √3cω. So β = −√3c and
    A = c(1 − i√3) = 2c e^{−iπ/3} (taking c > 0; ours).
  - Amplitude |A| = 2c and phase −π/3, so x(t) = 2c cos(ωt − π/3).
  - The picture: an arrow of length 2c starting at −π/3. Its shadow starts at c, half the
    amplitude, as required.
  - The lecturer's point: with sines and cosines you match coefficients twice. Here it's two
    lines.
- s6_recap · Try it, and recap (~75 s):
  - F19 (p. 9): the motion's centre is at 7. The rest, 24 cos 3t + 7 sin 3t, is our A = a − ib
    with a = 24 and b = 7. Write 24 − 7i as |A| e^{i arg A} (no φ on screen: the sheet's ϕ is
    3t − δ, see ch8 s7). The passages through the
    centre are where the shadow crosses zero; the stationary points are where it's at ±|A|.
    Solutions in Part 8.
  - Recap, with small versions of:
    - the pendulum and its graph (s2);
    - the arrow with its shadow (s3);
    - the velocity arrow a quarter turn ahead (s4);
    - the 2c arrow at −π/3 (s5).

  Next time: a circuit where four quantities oscillate together. The derivative becomes
  multiplication by iω, and a calculus problem becomes algebra. End card.
Continuity: the turning arrow from ch2, and the polar form of A from ch1. ch7 reuses the arrow and
shadow styling.

## Chapter 7 · Impedance
Slug: ch7_impedance · ~8.5 min · Source: notes PDF pp. 28–29 (Example 32; p. 29 is blank, filled
on scan p. 12) · Recording: 00:46:18–00:55:46, and the student question 00:56:12–00:56:28 ·
Scans: L10 pp. 11–12
Goal: set up the series RC circuit from its four laws, replace each oscillating quantity by its
complex amplitude, and derive Z = R + 1/(iωC) = R − i/(ωC).
Scenes:
- s1_hook · Hook (~45 s): part line "Part 7 · Impedance".
  - Last time: d/dt becomes multiplication by iω.
  - Example 32: "find the complex resistance of a capacitor and resistor connected in series to an
    applied alternating voltage."
  - At the end of the lecture a student asked: "I'm one of the computer scientists… is it okay
    that I didn't understand any of that physics stuff?" The answer: "yes, that's absolutely
    fine." So this chapter builds every physics fact it uses, and the maths is the point.
- s2_circuit · The circuit and its four laws (~105 s): notes p. 28 (the diagram), scan p. 11
  (labels), 00:46:18–00:49:49.
  - The circuit, as on p. 28: a source V(t) (a circle with ∼), a resistor R, a capacitor C, and
    the current I(t) round the loop.
  - The minimum physics (ours, plain words): voltage is the push; current is how much charge
    flows past each second. The source pushes back and forth at angular frequency ω.
  - The four laws, the lecturer's list:
    - Ohm's law: V_R = R I;
    - the capacitor stores charge: Q = C V_C;
    - current is the rate at which charge arrives: I = dQ/dt;
    - the voltages add round the loop: V = V_R + V_C.
  - i and I (ours): I is the current, and i is still √−1. Engineers write j for √−1 for exactly
    this reason. One colour per quantity, kept to the end (I GOLD; i PINK, as in every chapter).
- s3_amplitudes · Four amplitudes and three rules (~90 s): scan p. 12 (top), 00:50:00–00:52:13.
  - All four quantities oscillate at the same ω; the lecturer calls it a linear system. Each gets
    its own complex amplitude: V = Re(V₀ e^{iωt}), I = Re(I₀ e^{iωt}), V_R = Re(V_R0 e^{iωt}),
    V_C = Re(V_C0 e^{iωt}).
  - The lecturer's three rules:
    - Re and d/dt commute;
    - e^{iωt} on both sides of an equation cancels;
    - (e^{iωt})′ = iω e^{iωt}.
  - The goal: Z with V₀ = Z I₀, which is Ohm's law with a complex resistance. Z is the complex
    impedance.
  - The picture (ours): four arrows turning together at the same rate, with fixed angles between
    them.
- s4_parts · Resistor and capacitor (~100 s): scan p. 12, 00:52:21–00:53:40.
  - Resistor: V_R = RI, so Re(V_R0 e^{iωt}) = R Re(I₀ e^{iωt}). Drop the e^{iωt}: V_R0 = R I₀.
  - Capacitor: I = dQ/dt = C dV_C/dt, since C is constant. So I₀ = iωC V_C0, and
    V_C0 = I₀/(iωC).
  - A derivative has become a multiplication: no calculus is left.
- s5_impedance · Z (~95 s): scan p. 12 (bottom), 00:53:38–00:55:40.
  - V = V_R + V_C gives V₀ = V_R0 + V_C0 = (R + 1/(iωC)) I₀, so Z = R + 1/(iωC).
  - Clear the i from the bottom (1/i = −i): Z = R − i/(ωC), boxed as the lecturer did.
  - What Z tells you (ours, short): |Z| sets the size of the current for a given voltage. arg Z is
    negative, so the voltage lags the current. At low ω, 1/(ωC) is huge (the capacitor blocks a
    steady current). At high ω, Z approaches R.
  - Pointer (ours): the sheet's basic-skills F1(h) and F3(d) use R + iωL + 1/(iωC). An inductor
    adds iωL. Their answers are at the end of the sheet.
  - The lecturer's summary (00:54:56): writing everything with exponentials turned "equating
    sines and cosines" and differentiating into equating amplitudes.
- s6_recap · Recap, the lecture, and next time (~75 s):
  - Chapter recap, small versions of:
    - the circuit with its four laws (s2);
    - the four arrows turning together (s3);
    - the two amplitude laws (s4);
    - Z, boxed (s5).
  - The lecture in one picture (ours, two sentences): two threads, with thumbnails from each
    chapter in two rows.
    - The 2πn: roots, logarithms and powers (Parts 1, 4, 5).
    - The turning arrow: De Moivre, sums, oscillations and circuits (Parts 2, 3, 6, 7).
  - Next time (Lecture 11): what if the exponent is real, not imaginary? ½(e^x + e^{−x}) is the
    hyperbolic cosine. And Part 8 has full solutions to F12, F13 and F15–F19. End card.
Continuity: the arrow-and-shadow style from ch6. Closes the lecture; the teaser points to L11.

## Chapter 8 · Solutions to the examples
Slug: ch8_solutions · ~11 min (bonus) · Source: Examples Sheet I (`../source/M26examples1
(2).pdf`), PDF pp. 8–9: F12, F13, F15, F16, F17, F18, F19. Answers checked (Decisions)
Goal: full worked solutions using the lecture's methods, with the final answers on screen.
Scenes:
- s1_intro · Spoiler warning (~35 s): part line "Part 8 · Solutions (bonus)". Pause and try
  first. Show the seven question cards, each tagged with the Part that teaches it: F15 and F16
  (Part 1), F12, F13 and F17 (Parts 2–3), F18 (Part 4), F19 (Part 6).
- s2_f15 · F15: four equations, one method (~90 s): four small Argand diagrams.
  - (a) z³ = −1 = e^{i(π + 2πn)}, so z = e^{i(π/3 + 2πn/3)}: e^{iπ/3} = ½ + (√3/2)i, then −1, then
    e^{−iπ/3} = ½ − (√3/2)i.
  - (b) z⁴ = 1: 1, i, −1, −i (Lecture 9's example, ch1 s3).
  - (c) z² = i = e^{i(π/2 + 2πn)}: e^{iπ/4} = (1 + i)/√2 and e^{5iπ/4} = −(1 + i)/√2.
  - (d) z³ = −i = e^{i(−π/2 + 2πn)}: e^{−iπ/6} = (√3 − i)/2, e^{iπ/2} = i, and
    e^{7iπ/6} = (−√3 − i)/2.
- s3_f16 · F16: two circles (~125 s):
  - Put w = zⁿ: w² − 2bw + c = 0, so w = b ± s with s = √(b² − c). Call the two values w₁, w₂.
  - zⁿ = w₁ gives n roots on the circle |z| = |w₁|^{1/n}; zⁿ = w₂ gives n on |z| = |w₂|^{1/n}.
  - The circles coincide when |w₁| = |w₂|. Since |b + s|² − |b − s|² = 4 Re(b̄s), that means b and
    s are at right angles in the Argand diagram (the parallelogram becomes a rectangle).
    Equivalently, for b ≠ 0: c/b² is real and at least 1 (or b = 0).
  - z⁶ − 2z³ + 2 = 0: n = 3, b = 1, c = 2, and c/b² = 2, so there's one circle. w = 1 ± i
    = √2 e^{±iπ/4}, so |z| = (√2)^{1/3} = 2^{1/6}.
  - The roots are at ±π/12 + 2πm/3 (m counts turns: the sheet's n is the power): 15°, 105°,
    135°, 225°, 255°, 345°. No two are opposite. The
    widest pairs are 150° apart (15° and 225°, 105° and 255°, 135° and 345°), so the largest
    |z₁ − z₂| = 2·2^{1/6} sin 75° = 2^{1/6}√(2 + √3) ≈ 2.17.
- s4_f17_f12 · F17 and F12 (~95 s):
  - F17: ω³ = 1. If ω = 1, the sum is 3. Otherwise (ω − 1)(1 + ω + ω²) = ω³ − 1 = 0, so
    1 + ω + ω² = 0. The picture: three unit arrows tip to tail close a triangle (ch3's chain).
    For ωⁿ = 1, Σ_{k=0}^{n−1} ω^k is n if ω = 1, and otherwise (1 − ωⁿ)/(1 − ω) = 0: a closed
    regular polygon.
  - F12, short (the user solved it in supervision 3; keep to the key steps and answers):
    - (i) The imaginary part of (cos θ + i sin θ)³: sin 3θ = 3cos²θ sin θ − sin³θ
      = 3 sin θ − 4 sin³θ.
    - (ii) sin⁵θ = (e^{iθ} − e^{−iθ})⁵/(2i)⁵. The top is
      (e^{5iθ} − e^{−5iθ}) − 5(e^{3iθ} − e^{−3iθ}) + 10(e^{iθ} − e^{−iθ}), and (2i)⁵ = 32i, so
      sin⁵θ = (sin 5θ − 5 sin 3θ + 10 sin θ)/16.
- s5_f13 · F13: three sums (~115 s):
  - Σ_{n=1}^{5} e^{inθ} = e^{iθ}(1 − e^{5iθ})/(1 − e^{iθ}).
  - The half-angle trick (ours; quicker here than the conjugate):
    1 − e^{5iθ} = −2i e^{5iθ/2} sin(5θ/2) and 1 − e^{iθ} = −2i e^{iθ/2} sin(θ/2). So the sum is
    e^{3iθ} sin(5θ/2)/sin(θ/2).
  - (a) Σ cos nθ = cos 3θ sin(5θ/2)/sin(θ/2). (b) Σ sin nθ = sin 3θ sin(5θ/2)/sin(θ/2). For
    θ = 2πm they're 5 and 0.
  - (c) Σ rⁿ cos nθ = Re Σ (re^{iθ})ⁿ = Re[re^{iθ}(1 − r⁵e^{5iθ})/(1 − re^{iθ})]. Multiply by the
    conjugate 1 − re^{−iθ}, so the bottom is 1 − 2r cos θ + r². The answer:
    (r cos θ − r² − r⁶ cos 6θ + r⁷ cos 5θ)/(1 − 2r cos θ + r²). When re^{iθ} = 1 it's 5.
- s6_f18 · F18: five logarithms (~80 s):
  - (a) ln(−1) = i(π + 2πn) = (2n + 1)πi.
  - (b) ln i = i(π/2 + 2πn).
  - (c) ln(1 + i) = ½ ln 2 + i(π/4 + 2πn).
  - (d) With θ = arg(x + iy): ln((x + iy)*) = ½ ln(x² + y²) + i(−θ + 2πn). These are the
    conjugates of the values of ln(x + iy).
  - (e) i r e^{iθ} = r e^{i(θ + π/2)} (r > 0), so ln = ln r + i(θ + π/2 + 2πn).
- s7_f19 · F19: a shifted oscillation (~105 s):
  - x − 7 = 24 cos 3t + 7 sin 3t = Re[(24 − 7i)e^{3it}]: A = a − ib from Part 6, with a = 24,
    b = 7 and ω = 3.
  - Amplitude |24 − 7i| = √(576 + 49) = 25.
  - 24 − 7i = 25e^{−iδ} with δ = arctan(7/24) ≈ 0.284 rad (16.3°). So
    x − 7 = 25 cos(3t − δ). (The script calls it δ; the sheet's A e^{iϕ} is mapped once, small: its
    A is our |A| = 25 and its ϕ is 3t − δ.)
  - Through the centre (x = 7) when 3t − arctan(7/24) = π/2 + kπ. The first two times after 0 are
    t = [π/2 + arctan(7/24)]/3 ≈ 0.618 and t = [3π/2 + arctan(7/24)]/3 ≈ 1.665.
  - Stationary points: x − 7 = ±25, so x = 32 and x = −18, at distances 32 and 18 from the origin.
- s8_end · Close (~25 s): one line back to the lecture's two threads. Next lecture: hyperbolic
  functions. End card.
Continuity: every method is one taught in Parts 1–6. F17's closed triangle reuses ch3's chain, and
F19 reuses ch6's arrow and shadow.

## Decisions
- **Lecture 10, confirmed.**
  - The recording opens "so quick recap of what we did last time" with the scan's p. 1 heading,
    "Recap of lecture 9".
  - L9's scan ends on p. 19 (printed 100) with the same "fundamental theorem of algebra (see §2.7)"
    annotation, so L10 starts at Example 28.
  - The lecture ends "next time we start hyperbolic functions" (00:55:40), and L11's recording
    opens with a recap of exactly this lecture.
  - The digest's last segment shows the next lecture in the room (Physics, "Lecture 10,
    Dynamics"): a different course.
- **Scope: notes PDF pp. 19–29 (printed 100–110).**
  - The lecture covers everything from Example 28 to Example 32's Z = R − i/(ωC) (scan p. 12).
    Nothing in those pages is left out.
  - p. 18 (§2.3's opening and z⁴ = 1) is L9's: it's refresher material in ch1 s3.
  - **§2.7 (p. 30), the fundamental theorem of algebra, is L11's.** It was lectured at the start
    of L11 (00:03:12–00:04:41), and L11's plan teaches it in its ch4 s2. L10's transcript never
    reaches it. ch1 s5 keeps only the p. 19 remark that's on screen in L10 (00:03:35): degree n,
    n roots, with the theorem's name and "Lecture 11 explains it".
  - The request asked to check whether L10 went past p. 30. It stopped at p. 29.
- **Title: "Powers, Logarithms and Oscillations"**, replacing the working title "Complex Roots
  and Logarithms".
  - The lecture has no title of its own. The lecturer frames it as "mostly complex functions…
    what is different when we take logarithms of the powers".
  - "Powers" covers roots (fractional powers), De Moivre (integer powers), cos³θ and z^w.
  - About a quarter of the lecture is oscillations and impedance, which the old title left out.
  - The folder keeps its name.
- **Size: 7 core chapters (~63 min) plus a bonus (~11 min), ~75 min in all**, above L3's 63 and
  L4's 70.
  - The lecture has ~52 min of dense teaching: 11 pages of derivations, and the lecturer moves
    fast.
  - We add:
    - ~3 min re-teaching L9 (ch1 s2–s3);
    - a physics primer for a CST viewer (ch7 s2, prompted by the student question);
    - ~3.5 min of exercise hints.
  - Each chapter answers one question: how to take roots; De Moivre; trig powers and sums; what
    ln z is; what z^w is; oscillations; impedance.
  - **To shorten** (the user may prefer):
    - (a) merge ch6 and ch7 into one ~11-min "Oscillations and impedance" (−6 min). The physics
      gets rushed, which is the part a CST student asked about.
    - (b) drop the bonus (−11 min).
    - (c) drop ch4 s3 (ours, −1.3 min).
- **Order: the lecture's, with two moves.**
  - Example 30's "recall" of the geometric series gets its own short scene (ch3 s4), so ch3 s5–s6
    can stay on the algebra.
  - The impedance pointer to F1(h)/F3(d) sits at the end of ch7.
- **Exercise hints are spread out, not all in the last chapter (a change from the studio
  default).**
  - The exercises span five topics: roots (F15, F16), De Moivre and sums (F12, F13, F17), logs
    (F18) and oscillations (F19). Hints for roots and logs at the end of an impedance chapter
    would be unconnected to it, the user's complaint about text-only recaps.
  - So each chapter ends with hints for its own questions: ch1 (F15, F16), ch3 (F12, F13, F17;
    F12 waits for ch3 because part ii needs cos³θ's method), ch4 (F18), ch6 (F19).
  - Full solutions for all seven are in the bonus ch8.
  - To revert: the hints can't all fit in ch7 (it would reach ~12 min). They'd go at the start of
    ch8 instead, before the solutions.
- **Exercises chosen:** F12, F13, F15–F19 use this lecture.
  - F1–F11 are L9 basics or supervision 3 work (done).
  - F14 is L9's complex exponential.
  - F1(h) and F3(d), basic skills with answers on the sheet, get a pointer in ch7 s5.
  - F12 stays short in ch8, since the user's supervision 3 shows it solved correctly
    (sin 3θ = 3 sin θ − 4sin³θ; sin⁵θ = (sin 5θ − 5 sin 3θ + 10 sin θ)/16).
  - The bonus is one chapter at ~11 min. A calmer two-chapter split would be roots, sums and De
    Moivre (F15, F16, F17, F12, F13) versus logs and oscillations (F18, F19), ~8 min each with
    fuller explanations.
- **Colours follow L11's plan where they overlap:** i and imaginary parts PINK, e^{iθ} GOLD and
  e^{−iθ} PURPLE (L11's e^x and e^{−x}), real parts BLUE, kept or principal choices GREEN, pitfalls
  RED. The 2πn, L10's own thread, takes TEAL, which L11 uses for hyperbolic functions (none appear
  here). Recorded in COURSE.md.
- **Notation choices:**
  - The oscillator. The lecturer first wrote A = c + id, then renamed it c̃ + id̃ (00:45:07)
    because c is also x(0). We use α + iβ ("alpha", "beta"), which also avoids the fragile letters
    a and b in speech.
  - 2πn everywhere (the notes mix 2πn and 2nπ).
  - e^{…} instead of exp(…).
  - No capital-L Ln (the lecturer's rule). The principal value is a GREEN tag.
- **Student questions:**
  - The one real question, at 00:56:12 ("I'm one of the computer scientists… is it okay that I
    didn't understand any of that physics stuff?"), shapes ch7: its hook, and the plain physics
    in s2.
  - The lecturer's questions to the room become pause-and-think beats in ch5 s6: e^{2πinm} = 1
    (00:37:33), and q values (00:38:44). The digest's "Questions" are those two plus the student.
  - Likely confusions, answered where they arise:
    - why the 2πn goes in before dividing (ch1 s4);
    - n switching from degree to counter (ch1 s4);
    - why De Moivre needs an integer (ch2 s3);
    - "it's not the angle anymore" (ch4 s4);
    - principal values that don't add (ch4 s6);
    - lowest terms (ch5 s6);
    - i versus the current I (ch7 s2).
- **Source disagreements** (the notes and the scan win):
  - Example 28's printed line is 2i = 2exp(iπ/2), without the 2πn. The lecturer added "+2πn" by
    hand (scan p. 2), and the next printed line has it. We show the 2πn from the start.
  - Example 29's printed question stops at "in terms ." The lecturer filled in "of cos θ and
    sin θ" (scan p. 4). The printed sin 4θ ends at "="; the fills are 4cos θ sin θ(2cos²θ − 1)
    = 4cos θ sin θ(1 − 2sin²θ).
  - The p. 25 box cites "sheet 1 question 10, (a) and (b)". On this year's sheet F10 is the
    parallelogram identity, so the box refers to an older sheet. ch4 s6 uses our own example
    (−1 × −1). The digest's 00:26:49 segment garbles the box as "the principal values ln(ab) and
    ln(a) + ln(b)"; its 00:30:00 segment has the printed words.
  - The digest's 00:03:35 screen text shows "This the fundamental theorem of algebra (see §2.7)"
    as if printed. It's the lecturer's handwriting (scan p. 2, and already on L9's scan).
  - The digest's 00:40:00 points write "e^{z₂ Ln z₁}". The lecturer never wrote Ln.
  - Figure 24 in the notes has a red dot (the arrow's tip on the circle) and a green dot (its
    shadow on the real axis). The digest calls the shadow the red dot. Our colours: arrow
    GOLD, shadow BLUE.
  - The transcript's ln example says "z equal to i" (00:23:35) and "the modulus of 2 is 2"
    (00:24:25). The scan and the digest have z = 2i: Whisper slips.
  - Scan p. 10 (notes p. 27) is upside down.
- **Transcript slips, corrected silently:**
  - 00:02:52 "minus five" is minus pi.
  - 00:06:25 "adding 3 pi over 2, 4 pi over 10": the spacing is 4π/10 = 2π/5.
  - 00:35:56 "theta is theta plus 2 pi i" means θ + 2πn.
  - 00:36:40 "E2, pi, and I, Z2" is e^{2πniz₂}.
  - 00:52:25 "bring about I omega t" is iω.
  - Whisper's names:
    - "deMoverit", "Mori", "Moivre's"/"Morse" are De Moivre;
    - "argon diagram"/"our gun diagram" is the Argand diagram;
    - "order representation" (00:03:54) is the Euler representation;
    - "Seventy-one" is equation (71);
    - "further mass" is Further Maths.
- **Skipped from the recording:**
  - 00:09:39–00:09:40 and 00:55:46–00:56:11: Whisper loops ("So." ×15, "I'm sorry" ×25) over
    silence and applause, not speech.
  - 00:56:28–00:57:17: the rest of the student exchange (inaudible).
  - 00:57:17–00:59:57: a department announcement (year-group reps) and the next lecture's title
    slide.
- **Voice notes for the producer** (rules in COURSE.md):
  - Before bulk voicing, test a short throwaway clip of these phrases:
    - "E to the eye theta";
    - "zed to the fifth equals two eye";
    - "the fifth root of two";
    - "log of mod zed, plus eye times arg zed plus two pi N";
    - "cosine to the fourth of theta";
    - "De Moivre's theorem";
    - "Euler's formula";
    - "the Argand diagram";
    - "eye to the power eye";
    - "P over Q, in lowest terms";
    - "one over eye omega C";
    - "V zero equals zed times I zero".
  - Untested: "zed" (Whisper may write "said" or "Z"), capital "E" for e, "De Moivre", "Euler"
    (may come out "you-ler"; fallback "Oiler"), "Argand" (Whisper wrote "argon"), "phi" (F19
    avoids it: "the angle").
  - QA homophones worth adding to voiceqa.py: "pi pie", "principal principle", "sine sign",
    "argand argon". Whisper may also write symbols (π, θ, ω), which QA strips, so expect false
    flags there.
- **Beyond the notes, each short and labelled "ours" in the scene lists**, all checked:
  - ch1: the ring as scaled and rotated roots of unity, and the general recipe (s5).
  - ch2: general modulus and n = −1 (s2); the square-root demonstration (s3); the θ = π/4 check
    (s5); the two-arrow picture (s6).
  - ch3: the integral of cos³θ (s2); the tip-to-tail chain (s3); the one-line geometric-series
    proof (s4); the N = 3 check and the sine sum (s6).
  - ch4: why z ≠ 0 (s2); the two-plane map (s3); the 3 + 4i example (s5); the −1 × −1 example
    (s6).
  - ch5: the 2^i moduli and the log-scale strip (s3); lowest terms, and (2i)^{1/5} = the ring
    (s6); the √2 example (s7).
  - ch6: the meaning of ω (s2); |A| and arg A (s3); why Re and d/dt swap, and the quarter-turn
    (s4); c > 0 (s5).
  - ch7: the plain physics and engineers' j (s2); the turning arrows (s3); the meaning of Z and
    the F1(h)/F3(d) pointer (s5); the two-thread summary (s6).
  - ch8: the half-angle trick (s5); F16's geometric condition.
- **Checked** (Python 3.11, cmath; numbers to the precision shown):
  - Example 28: the five values 2^{1/5}e^{i(π/10 + 2πn/5)} satisfy z⁵ = 2i. Their principal
    arguments are 0.1π, 0.5π, 0.9π, −0.7π, −0.3π; the modulus is 1.1487; n = 5 equals n = 0.
  - Example 29: cos 4θ = cos⁴θ − 6cos²θ sin²θ + sin⁴θ = 8cos⁴θ − 8cos²θ + 1, and
    sin 4θ = 4cos θ sin θ(cos²θ − sin²θ) = 4cos θ sin θ(2cos²θ − 1) = 4cos θ sin θ(1 − 2sin²θ),
    at four θ.
  - cos³θ = ¼cos 3θ + ¾cos θ; its integral (1/12)sin 3θ + ¾ sin θ differentiates back.
  - Example 30: S_N = ½ + [cos(N−1)θ − cos Nθ]/[2(1 − cos θ)] for N = 1, 2, 3, 5, 8 at four θ.
    θ = 2πm gives N. N = 3, θ = π/2 gives 0.
  - ln 2i: the principal value is 0.6931 + 1.5708i, and every rung exponentiates to 2i.
  - Principal values:
    - Ln(−1) + Ln(−1) = 2πi, but Ln 1 = 0;
    - 2Ln(−1 + i) − Ln((−1 + i)²) = 2πi;
    - Ln e^{3+4i} = 3 + (4 − 2π)i = 3 − 2.2832i.
  - 2^i = e^{−2πn}(cos ln 2 + i sin ln 2). n = 0: 0.7692 + 0.6390i (modulus 1); n = 1: modulus
    0.001867; n = −1: modulus 535.49. ln 2 rad = 39.7°.
  - i^i = e^{−π/2 − 2πn}: 0.20788 (n = 0, matches Python's 1j**1j), 0.000388 (n = 1),
    111.32 (n = −1).
  - Distinct values of e^{2πinz₂} over n ∈ [−200, 200]: z₂ = 3 → 1; 2/5 → 5; 3/4 → 4; −1/2 → 2;
    √2 → all distinct.
  - (2i)^{1/5} = e^{(1/5)(ln 2i + 2πin)}, n = 0…4, gives exactly Example 28's five roots.
  - Oscillator: A = c(1 − i√3) = 2ce^{−iπ/3} (|A| = 2c, arg −π/3). x(0) = c, v(0) = √3cω, and
    x(t) = 2c cos(ωt − π/3) = c cos ωt + √3c sin ωt, so a = c, b = √3c, A = a − ib.
  - Impedance: Z = R + 1/(iωC) = R − i/(ωC). For R = 5, C = 0.01, ω = 30, the amplitudes
    satisfy V = V_R + V_C and I = C dV_C/dt at sample times. Z = 5 − 3.33i, arg −33.7°: the
    voltage lags the current.
  - F12: sin 3θ = 3 sin θ − 4sin³θ; sin⁵θ = (10 sin θ − 5 sin 3θ + sin 5θ)/16.
  - F13: (a) and (b) in the half-angle form; (c)'s formula for r = 0.5, 2, −0.7 at four θ.
  - F15: (a) ½ ± (√3/2)i and −1; (c) ±(1 + i)/√2; (d) (±√3 − i)/2 and i.
  - F16:
    - z⁶ − 2z³ + 2 has six roots of modulus 2^{1/6} = 1.12246, at 15°, 105°, 135°, 225°, 255°,
      345°.
    - The largest |z₁ − z₂| is 2.16843 = 2^{1/6}√(2 + √3) = 2^{7/6} sin 75°.
    - c = b²(1 + t²) always gave |w₁| = |w₂| (2000 random b, t). For 2000 random (b, c),
      "c/b² real and ≥ 1" matched |w₁| = |w₂| every time.
  - F17: 1 + ω + ω² = 0 for ω = e^{±2πi/3}. Σω^k = 0 for every n-th root of unity ≠ 1, for
    n = 4, 5, 7.
  - F18:
    - the principal values ln(−1) = iπ, ln i = iπ/2, ln(1 + i) = 0.3466 + 0.7854i;
    - ln z* = (ln z)* off the negative real axis;
    - ln(i r e^{iθ}) = ln r + i(θ + π/2) for r = 2, θ = 0.7.
  - F19:
    - |24 − 7i| = 25, and arg = −arctan(7/24) = −0.2838;
    - Re[(24 − 7i)e^{3it}] = 24 cos 3t + 7 sin 3t;
    - zeros at t = 0.6182 and 1.6654;
    - x = 32 and −18 at the stationary points.
