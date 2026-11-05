# nst-maths

NST Part IA Mathematics, Course B (Mathematical Methods I), Michaelmas 2026, Cambridge.
Lecturer: Natalia G. Berloff (DAMTP). 24 lectures, Tue/Thu/Sat 9:00, from Thu 8 Oct.
Notes (with blanks filled in during lectures) and the scanned annotations are on Moodle
(vle.cam.ac.uk, Raven login). The lecturer works through the typeset notes under a visualiser,
so the lecture digest reproduces most of the notes page by page.

Material: `source/`. Each lecture is its own project folder here.
- `M26examples1 (2).pdf`: Examples Sheet I (A vectors … G hyperbolic functions … M power series).
- `HW math supo 3.pdf`: the user's supervision 3 work (19 pages).
- `LectureNN_scanned.pdf`: the lecturer's handwritten annotations, one scan per lecture (L9, L10
  here; L1–10 are in `~/Downloads/Scanned Lectures-20261101.zip`). The typeset notes with blanks
  are `Chapter234_to_annotate.pdf` (Ch 2 complex numbers p2–30, Ch 3 hyperbolic p31–46, Ch 4 differentiation p47–70); Ch 0+1 and 5+6 are in `~/Downloads/Lecture Notes to Annotate-20261101.zip`.
- `lNN-lecture.mp4`: the recordings; `vk lecture` writes `.transcript.md` and `.digest.md` beside them.

| # | Lecture | Project | State |
|---|---|---|---|
| 10 | Powers, Logarithms and Oscillations (Thu 29 Oct) | `l10-complex-roots-logs/` | ✅ done: 8 videos in `out/`, 80.7 min (2026-11-01) |
| 11 | Hyperbolic Functions and Conics (Sat 31 Oct) | `l11-hyperbolic-functions/` | ✅ done: 7 videos in `out/`, 74.4 min (2026-11-01) |
| 12 | Differentiation (Tue 3 Nov) | `l12-differentiation/` | ✅ done: 7 videos in `out/`, 85.7 min; built with Gemini off, full listen pending (2026-11-03) |
| 10 (deep) | Oscillations (deep-style pilot: L10 §2.6, F19) | `l10-deep-oscillations/` | ✅ done: 4 videos in `out/`, 58.4 min, 1440p (2026-11-04) |

Lecture boundaries (from the transcripts): L11 opened with §2.7, the fundamental theorem of algebra
(notes p30), so it lives in L11 (ch4 s2); L10 ends with §2.6. L11 then covered all of Ch 3 (pp31–46,
incl. §3.5 conics) and ended "next time differentiation" (Ch 4, p47). L12 covered Ch 4 §4.1–§4.10
(pp47–66, through the stationary-point examples) and ended "next time: curve sketching", so L13
opens with §4.11 (pp66–70, Example 43). Examples Sheet I by lecture: G → L11; H1, H2, H4, I1 → L12;
H3 (even/odd) and H5 (sketching) → §4.11; J1 (continuity, differentiability) → Ch 5 of the notes
(limits and continuity). L12's digest is empty (Gemini off): its handwritten blanks were read from
frames and are recorded in `l12-differentiation/project.json`.

Course-wide colours (L10 and L11 plans agree; the PINK i is the producer's course-wide rule, 2026-11-01): i and imaginary parts PINK; real parts and the
circular functions BLUE; e^{iθ} / e^x GOLD and e^{−iθ} / e^{−x} PURPLE; the kept root, branch or
principal value GREEN; pitfalls and rejected cases RED; attention and boxed results YELLOW. L10's
own thread, the 2πn (extra roots, the ln ladder, the values of z^w), is TEAL; L11's TEAL is the
hyperbolic functions. Notation as in the notes: ln z means all values (principal value tagged in
words, no capital-L Ln, the lecturer's rule); "+ 2πn" after the angle; e^{…} rather than exp(…).
L10 hints each exercise at the end of the chapter that teaches it (not all in the last chapter).
L10 additions (its continuity review, 2026-11-01): TEAL marks full turns and nothing else (2πn
and 2πm, the extra-turn roots, the ladder's rungs, the period 2π/ω in its ch6). L10 ch7 makes the
current I GOLD, so there the e^{iωt} factor and the source voltage are white, the resistor's
quantities BLUE and the capacitor's PINK (Z's real and imaginary parts).
L12's own (its planner, 2026-11-03): TEAL is the increment that shrinks to zero (δx, δy, δu, h) and the
chord it makes, nothing else, so hyperbolic function names are white in L12. The curve being
differentiated is BLUE (as the notes draw it), the tangent line and the derivative GREEN, binomial
coefficients and Pascal's triangle YELLOW. In two-function rules the first function (f; the outer
function of the chain rule; u of a quotient) is BLUE and the second (g; the inner function; v) PURPLE,
which keeps every decaying exponential L12 meets (e^{−x}, e^{−x²}, e^{−x²/2}) PURPLE by the course rule.
Words: "the chord" for the line through two points (never "secant", which is sec x); "the tangent
line", always with "line", against "tangent of ex" for tan x.

## Voice rules (TTS) for maths
Learnt per lecture; script-writers follow these, and add any new ones they hit.
- Don't end a sentence on "dee ex": it was heard as "dee exes" (L12; fixed as "Dee why over dee ex looks
  like a fraction."). "worked" before a noun can lose its "-ed": "the worked solutions" passed.
- Letters as capitals right after a noun ("point A", "matrix M"), as in the DE course.
- **Tested on the clone (L11 ch1, 2026-11-01): keep** "shine", "cosh", "tanch", "zed", "eye", "E to
  the (minus) eye ex". Whisper's flags on them are false ("shine"→"sine", "cosh"→"cache/Cauchy",
  "tanch"→"tinge"): Gemini heard all as written and a spectrum check confirms the "sh". Accept those
  flags without rewriting. **Avoid "solve"**: heard as "saw" by Gemini and Whisper ("find every zed
  whose …"). The voice may insert "the" in "Divide the sine … by the cosine"-type lines: check QA.
  Gemini's own claims "tanch"→"touch", "cosine"→"kusine" were false (all three Whispers agreed).
- **"tanch" stays the reading of tanh** (producer, 2026-11-01). Some takes in L11 ch2 were heard as
  "tant"/"tonch"/"tangent" by Gemini; that's a per-take problem, not the word: re-voice the take,
  or say "hyperbolic tangent" in that one line (ch2 does in three places). Don't switch series-wide.
  Also from ch2: "cosh squared of ex" can be heard "square root of"; "solves" heard "softs".
- **Names (L10 ch2, 2026-11-01):** write Euler as **"Oiler"** ("Euler's" came out "Yooler's").
  "De Moivre" comes out "de MOY-ver" consistently, an accepted English reading: keep it.
  "E to the eye N theta" was heard "in theta": write "E to the eye times N theta". "two ends"
  heard "two N's": avoid a word that sounds like a letter next to letters.
- **"cosh and" is heard "caution"** (L11 ch7): say "shine and cosh", not "cosh and shine"; "curve"
  came out "turv" once, "hugs" "huts": re-voice the take.
- **Avoid "you'll"** (heard "I'll", L10 ch6). Say **"the first examples sheet"**, not "Examples Sheet
  One" ("Example"). Plural "sines" is heard "signs": an accepted homophone.
- **Never "arg"** (L10 ch1: heard "arc", "ard", "rw"): say "the argument of zed". And "two pi eye
  times N", not "two pi eye N".
- From L10 ch5: "Let's recap" was heard "Must": open with "Time for a recap". "two pi N over five"
  heard "pi and over": say "one fifth of two pi N". "wind" (a curve) came out as the breeze: "trace
  out". A bare "plus" between numbers was heard "pus": name the parts ("its real part is …").
- From L10 ch3: "three terms" was heard "three turns" (fatal in a lecture about turns): say "three
  of them" or name the terms. "adds the angles" heard "at z angles": "the angles add up".
- From L11 ch5: a capital A after "of" is too short to read as a letter ("half of A" heard "half
  of uh"; A lasted 0.20–0.26 s against 0.30–0.42 s for clear letters, measured with Whisper word
  timings): say "half the number A". Whisper can't catch it (A and a spell alike): check A's
  duration. "axis" was heard "access": "the ex axis" in full, or "the line".
- From the L11 continuity review (2026-11-01), applied in all L11 scripts:
  - A capital A never stands before another word: "the cosh of the sum, A, plus B", then "the cosh of
    the sum"; "eye A, and eye B" (DE L10 heard the article "uh" there).
  - No "halves" or "halve" (DE: "halve" heard "have"): "the two parts", "the factors of a half".
  - Cross-references: the videos are "part one" … (the title cards' word); "chapter" only for the
    notes' chapters ("Chapter three of the notes"); an exercise's (i)/(ii) by content ("the first curve").
- From the L10 continuity review (2026-11-01), applied in all L10 scripts:
  - The three rules above (L10's "Part One A maths" became "first-year maths", "halve" went, and
    F12's "part one / part two" became "for sine of three theta" / "for sine to the fifth").
  - A letter next to E gets "times": "R times E to the eye theta", "eye times R, times E to the eye
    theta" ("eye R E to the eye theta" is a string of letter sounds). An exponent ends with "times"
    before a function: "R to the sixth times cosine six theta".
  - Turn counters: N counts turns unless N is already the power or a count; then M does (L10 ch3,
    ch8's F16). L10 ch1's general recipe writes the power as K.
  - "Why" may start a question ("Why lowest terms?"), as L11 decided; never as the variable y.
- Proposed by the L11 planner (2026-11-01), untested with the clone until the first maths voice run;
  correct them here when QA says otherwise:
  - Circular functions in full: "cosine", "sine", "tangent" (a bare "cos" may be read "because";
    "cosine" against "cosh" also keeps the two apart by ear). Hyperbolic ones as the notes say them:
    "cosh", "shine" (sinh), "tanch" (tanh); sech, cosech, coth in full ("hyperbolic secant", …).
  - Inverses: "inverse cosh of ex", "inverse shine", "inverse tanch"; never "cosh to the minus one"
    (heard as one over cosh).
  - Lowercase variables spelled: "ex", "why", "zed" (British), with commas when they stand alone;
    "the ex axis". Other letters capital after a noun ("the integer N", "the constant S", "the radius
    R", never "ar"). In a product the letter ends a phrase: "cosh of A, times cosh of B".
  - i is "eye"; e is a capital "E": "E to the ex", "E to the minus ex", "E to the two why" (fallbacks:
    "ee", then "the exponential of ex"). ln is "log", never "ell en".
  - Subscripts: "ex zero", "zed one", never "nought" (heard "not", which flips the meaning).
  - Scope: "E to the ex, plus E to the minus ex, all over two"; name a long formula by its parts while
    the screen highlights them, never more than ~8 symbols in one breath.
  - Symbols: ± "plus or minus", ≥ "at least", ≠ "different from", ∅ "no solution", ≈ "about" with
    rounded numbers in words; (−1)^n "minus one to the power N"; x² "ex squared"; cosh² x "cosh
    squared of ex". "hyperbolas", not "hyperbolae"; prefer "semi-major and semi-minor axes" to a bare
    "semi-axes" (may be read as "axes", the tools).
  - Whisper may write "shine", "tanch", "cosh" oddly ("tench", "cash"): ear-check with
    `vk listen --only` before rewriting; add a homophone to voiceqa if one recurs.
- Proposed by the L12 planner (2026-11-03), untested; L12 ch1's voice run tests the derivative
  words, ch4 "Leibniz", ch5 "Hermite". Correct them here when QA says otherwise:
  - Derivatives by meaning where possible ("the derivative of why with respect to ex", "the second
    derivative"); the symbols "dee why by dee ex", "dee by dee ex" only where the notation itself is the
    subject (risk: "dee" heard as "the").
  - Primes: "F prime", "G double prime", "F triple prime", "why prime"; f^(n) "the Nth derivative of F";
    f^(n−m) "F differentiated N minus M times".
  - Increments: "delta ex", "delta why". u and v named by role ("the inner function", "the top", "the
    bottom"): a bare "U" is heard as "you". The step h is "the step H"; the Heaviside function is always
    named, never "H of ex" aloud; "H N", "H three" are only Hermite polynomials.
  - "the limit, as delta ex goes to zero, of …"; "the left-hand limit"; |x| is "mod ex" (first use
    "mod ex, the absolute value of ex"). "N choose M", "N factorial".
  - "inverse sine", "inverse tangent of ex"; "secant squared", "hyperbolic secant squared"; "one plus ex
    squared, all to the power three over two"; "E to the minus ex squared", "E to the ex squared".
  - Names: "Leibniz" as written (fallback "Libe-nits"); Hermite written "Hermeet" (fallback
    "Air-meet"); "Heaviside", "Lagrange", "Pascal" as written. "concave up", "concave down".
  - Settled in the L12 continuity review (2026-11-03), used the same way in all seven L12 scripts:
    "Leibniz" and "Leibniz's formula" (never "Leibnitz", the sheet's spelling); "Hermeet polynomials"
    in speech, "Hermite" on screen; "dee why by dee ex" and "dee ex by dee why" only where the notation
    is the subject; sheet questions are "H one", "H four" and **"eye one"** (written so: "I one" can
    come out as the pronoun, "I won"). Whisper will write "eye one" as "I one" or "I won": accept that
    flag after an ear check. The Hermite polynomials are "H N", "H three" only in L12 part five and the
    bonus, and never in a scene that also names a sheet question. The Heaviside function is always
    named; the step h is "the step H" or "the step".
  - L12 ch1's QA (2026-11-03, Whisper only, Gemini off): "successfully resolved" was heard as written:
    keep it ("resolved" is safe; the bare "solve" stays banned). "dee why by dee ex", "dee by dee ex",
    "Leibniz", "why prime", "mod ex" passed. Whisper's "Oiler"→"Euler" and "Heaviside"→"heavy side(step)"
    are false flags: accept them. **"a quotient" is heard as "equation"** (all three Whispers): say "the
    difference quotient" or "the quotient".
- Added by the L10 planner (2026-11-01), also untested; same status as the L11 list above:
  - Powers: "zed to the fifth", "zed to the N", "zed to the power W", "two to the power eye", "eye
    to the power eye"; 2^{1/5} is "the fifth root of two". Trig powers and multiples: "cosine cubed
    of theta", "cosine to the fourth of theta", "cosine of four theta".
  - Exponentials: "E to the eye theta", "E to the minus eye theta", "E to the eye N theta", "E to
    the two pi eye N". Multiples of pi: "pi over ten", "two pi N" (the full turns), "two pi eye"
    (2πi).
  - |z| is "mod zed" (first use "the modulus, mod zed"); arg z is "arg zed" (first use "the
    argument, arg for short"); z* is "zed star"; Re and Im are "the real part of", "the imaginary
    part of"; "modulo two pi eye" is "up to whole multiples of two pi eye".
  - Sums: "the sum, from K equals zero to N minus one, of cosine of K theta", then "the sum".
    Derivatives by meaning: "the derivative with respect to time". p/q is "P over Q, in lowest
    terms". Impedance Z is "zed" too; "one over eye omega C".
  - Letters that are fragile in speech are named by their role: "the cosine coefficient" (a), "the
    sine coefficient" (b), "the complex amplitude" (A), "the current" (I, which sounds like i).
    Avoid "phi": say "the angle".
  - Untested names: "De Moivre" (Whisper wrote "deMoverit"), "Euler" (may come out "you-ler";
    fallback "Oiler"), "Argand" (Whisper wrote "argon"). QA homophones worth adding to voiceqa.py:
    "pi pie", "principal principle", "sine sign", "argand argon".
- Proposed by the L10 deep-pilot continuity review (2026-11-04), untested; correct them here when QA
  says otherwise:
  - Once a capital A is a variable (a complex amplitude, a constant), no sentence starts with the
    article "A": it can be heard as the letter. "Say the complex amplitude is two eye", "One quarter
    turn later".
  - Two letters in a row run together ("M G"): say "M times G".
  - "Shine" in its English sense is out: in this course it's sinh. "Drop a line straight down", not
    "shine a light".
  - On screen it's "Euler"; "Oiler" is only the spoken spelling, and must not leak into a brief's
    on-screen text.
