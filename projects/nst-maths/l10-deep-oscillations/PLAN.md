# Oscillations: plan

Request: "for the first in depth trial do the pendulum stuff. explaining the physics first etc."
(the user, 2026-11-04, via the producer). The rest of the request is quoted in
`docs/DEEP_STYLE.md`, "Why": build from first principles, give a motive for every move, name the key
moves so they're remembered, keep steps atomic, ask questions to engage with, and give intuition
(they called L10's two-arrows picture of cos θ "elite"). **Style: deep** (`docs/DEEP_STYLE.md`;
its §11 wins over §1–§6). Finals render at 1440p60.

Audience: the user, a Cambridge first-year (very likely CST) taking NST IA Maths.
- Maths: A-level. Derivatives of sin, cos and e^{kx}, the chain rule, right-angled trig, radians.
- Physics: maybe GCSE only (F = ma, Hooke's law, weight = mg). Of simple harmonic motion they said
  "which i don't even remember what it is".
- Already seen, in L10's old-style parts 1–5 (`../l10-complex-roots-logs/out/`):
  - e^{iθ} as the unit arrow at angle θ;
  - "multiplying multiplies lengths and adds angles";
  - De Moivre, and cos θ = ½(e^{iθ} + e^{−iθ}) as two arrows;
  - the complex log, and z^w.
  Euler's formula was taken as given there. From L9: modulus, argument, conjugate, polar form.

Sources (project.json `sources`): the notes `../source/Chapter234_to_annotate.pdf`, PDF pp. 27–28
(printed 108–109: §2.6, Figure 24, (81)–(83), the oscillator example); the lecturer's scan
`../source/Lecture10_scanned.pdf` p. 10 (the pendulum sketch, upside down) and p. 12 (its
oscillation part: the three rules); the recording `../source/l10-lecture.{transcript,digest}.md`,
00:41:45–00:46:18, plus 00:50:59–00:51:48 for the rules; Examples Sheet I, F19
(`../source/M26examples1 (2).pdf`, PDF p. 9). Out of scope: Example 32, the circuit (the old part 7,
which follows this pilot).

Total: 4 chapters, ~42 min of narration (~6,700 words at 160 wpm). With the house pacing and 14 think
stops that's ~50 min of video. The lecture spent 4.5 min on this, so ~9× its time. The old part 6
had 8.5 min of narration and 10.6 min of video, so ~4.8× that. Decisions explains why.

Every number and identity below was checked in Python 3.11 (cmath, sympy 1.14.0); see Decisions,
"Checked". Script-writers still check their own (project.json `toolchain`).

## Conventions (all four chapters)

**This pilot and the old series.**
- Title card: title "Oscillations", course line "NST IA Mathematics · Lecture 10", part lines
  "Part 1 · …" to "Part 4 · …".
- These four videos replace the old part 6, and the old part 7 (impedance) follows them.
- In speech, this pilot's videos are "part one" to "part four". The old L10 videos are named by
  topic ("the video on De Moivre's theorem", "the impedance video"), never by number, because their
  numbers clash with ours.

**Notation.**
- x: displacement from the middle, signed (right or outward is positive). For the spring it's a
  distance. For the pendulum it's an angle, the notes' "angular displacement x(t)".
- θ: the pendulum's angle in ch1 s5–s7 only, for the geometry. ch1 s8 renames it x, as the notes
  do. θ appears nowhere else, and never names the arrow's angle.
- ẋ = v: velocity. ẍ: acceleration. Newton's F = ma appears once (ch1 s2's retrieval card) and
  becomes F = mẍ straight away, because from ch2 on a and b are (81)'s coefficients.
- k: the spring's stiffness. m: mass. L: the pendulum's length (the notes write l, which is
  unreadable at size, and is spoken "L" anyway). g = 9.81 m/s². s: distance along the arc.
- ω: angular frequency, in radians per second. ω² = k/m (spring) or g/L (pendulum).
- λ: the rate in the trial e^{λt} (ch2 s2). k is taken by the spring.
- e^{iωt}: the turning unit arrow. e^{−iωt}: its mirror.
- A: the complex amplitude. While matching (ch3 s4) its parts are α + iβ, the old plan's rename of
  the lecturer's c̃ + id̃. |A| is the amplitude and arg A the phase. At time t the arrow's angle is
  ωt + arg A.
- a, b: (81)'s coefficients ("the cosine coefficient", "the sine coefficient" in speech).
- T: the period, on screen only. In speech it's always "the period", since t and T sound alike.
- x₀, v₀: start position and start velocity (ch2 s7, ch4).
- F19: the sheet's X = (24 − 7i)e^{3it}, and δ = arctan(7/24). The sheet's own "A e^{iϕ}, A and ϕ
  real" appears once, small, as a mapping: the sheet's A is our |A| = 25, and its ϕ is 3t − δ.
- Re[…], as the lecturer writes it (the notes print ℜ). e^{…}, not exp(…).
- Equation tags are small and DIM, beside their formulas: "(81) · notes p. 108", "(82) · notes
  p. 108", "(83) · notes p. 109", "Fig. 24 · notes p. 108", "example · notes p. 109", "F19 · Examples
  Sheet I". They are never spoken (deep style: no lecture references in the narration).

**Colours** (lib.style). L10's conventions apply, plus three roles fixed for this pilot:
- BLUE: displacement x, meaning the bob's position, the shadow dot and real parts (a, α, the real
  leg of A). The bob and the shadow are the same BLUE dot.
- GREEN: velocity ẋ, its arrows and its shadow. This is a new role; L10's GREEN (principal value)
  never appears here.
- RED: the pull, meaning restoring force and acceleration: F, ẍ, gravity's along-swing part, the
  −ω²A arrow. This is a new role. Pitfalls keep RED only as a ✗ on struck-through text, never as an
  arrow.
- GOLD: e^{iωt}, the arrow A e^{iωt}, and lengths |A|. e^{iωt} is GOLD in every part, including as the factor in (82): A e^{iωt} reads as the moving GOLD arrow, and its angle ωt is the YELLOW arc (settled in the continuity review).
- PURPLE: the mirror arrows e^{−iωt} and A* e^{−iωt}.
- PINK: i and imaginary parts (the −ib leg, the i of iω).
- YELLOW: angles (θ, ωt, arg A, δ) and boxed results.
- TEAL: one full turn only: 2π, and the period T = 2π/ω.
- DIM: grid, unit circle, the rod's along-rod component, tags, earlier lines.
- FG: constants (k, m, g, L, ω) and gravity's full arrow mg.

**The board** (1440p, §6). A default layout; directors may adjust it.
- The picture sits centre-left (~55% of the width) and stays for the whole scene.
- The derivation stacks in a right-hand column, top to bottom. At most 3 lines are at full
  brightness; older lines dim to 0.4. ~6–8 lines in all.
- Legend: a small panel in the bottom-left corner (DIM border, 22–24 px). It lists every letter in
  play, in its colour, and updates as letters enter.
- The move card goes in the top-right slot. Tags are DIM, 22 px, beside their items.
- Pinned formulas. ch2 pins "the rule", ẍ = −ω²x, small at top centre for the whole chapter. ch3
  (from s2) and ch4 pin x = Re[A e^{iωt}] in the same place.

**The move card** (one look in every chapter).
- A rounded rectangle (corner radius ~0.12), YELLOW stroke 2, fill #171A21.
- The label "The move" in YELLOW at 24 px, top-left inside the card.
- The move itself in FG at ~30 px: ≤ 2 lines, ≤ 14 words, phrased as an action and its effect.
- It stays for the scene, dims to 0.6 during a think stop, and returns small in the recap beside its
  picture. In the narration: "The move here is …".

**Think stop** (§5, one look).
- The question sits in a box in the lower third (rounded, FG stroke 2, fill #171A21), with DIM
  "pause the video if you want longer" under it.
- A DIM ring (r ≈ 0.3) in the bottom-right corner drains during the hold.
- Everything else freezes, swinging pendulums included.
- In the script: the question, "pause the video if you want longer", `{pause=4}`, then the answer
  worked out.
- Quick predictions and retrieval questions are plain text with `{pause=1.5}`: no box, no ring.

**Tags.**
- "beyond the notes" (DIM, 22 px) marks additions; the narration says it once per chapter. ch1 is
  almost all addition, so it has one corner tag from s3 to s7 instead of one per item.
- "reference" (DIM, 22 px) marks reference-tier items (Coverage).

**Narration** (deep §11, plus COURSE.md "Voice rules").
- No lecture references in speech.
- At least 1.5 "you" per 100 words.
- A narrated question at least every 2 minutes, and a motive or a question before every new formula.
- After each key formula, one sentence reading it in the picture's language.
- Name things by role, never by fragile letter: "the cosine coefficient", "the sine coefficient",
  "the complex amplitude", "the phase", "the period", "the velocity", "the acceleration".
- Speak symbols as words: "omega", "omega squared", "lambda", "theta", "delta", "alpha", "beta",
  "E to the eye omega T", "E to the minus eye omega T", "the stiffness K", "the mass M", "the
  length L", "G, the strength of gravity".
- COURSE.md rules that bite here:
  - never "solve": use "find" or "obeys";
  - never "arg";
  - no capital A after "of": say "the length of the complex amplitude";
  - "Oiler" for Euler;
  - avoid "you'll";
  - "the first examples sheet", "F nineteen";
  - "three of them", not "three terms".
- New words to ear-check: "Hooke", "pendulum", "lambda". Never "isochronous": say "keeps the same beat".
- Settled in the continuity review: "M times G", never "M G"; no "shine" in its English sense (it's
  this course's sinh); "centripetal" is an on-screen tag only, never spoken; in parts three and four
  no sentence starts with the article "A" (it can be heard as the complex amplitude A): "Say the
  complex amplitude is …", "One quarter turn …". On screen it's "Euler", in speech "Oiler"; (71)
  is tagged "notes p. 97" (handwritten there in Lecture 9).

**Running examples.**
- *The 1 m pendulum* (ch1 s1 and s7, ch2 s8, ch4 s1): ω = √9.81 ≈ 3.13 per second and the period is
  ≈ 2.01 s, so about one second each way. A grandfather clock's "seconds pendulum" is 0.994 m long.
- *The 3-4-5 swing*: a weight on a spring with ω = 3 per second, x in cm. It starts at 3 cm, moving
  outward at 12 cm/s, so x = 3 cos 3t + 4 sin 3t.
  - ch2 s7: an instance of (81).
  - ch3 s3–s5: A = 3 − 4i, |A| = 5, arg A ≈ −0.93 rad ≈ −53°. The velocity's amplitude is
    3i·A = 12 + 9i and the acceleration's is −9A = −27 + 36i.
  - ch4 s2: found from its start.
  - F19 (7-24-25, also ω = 3) is its big sibling.
  - On screen and in speech it's "the third weight" (ch3's hook) or "the swing from part two",
    never "3-4-5"; that name is for this plan only.
- *The arrow*: the GOLD arrow and its BLUE shadow, built in ch2 s3–s5 and kept in every scene after
  that. Whenever both are on screen, the bob sits on the shadow's line (P7).

**Recaps** (≤ 60 s): the chapter's moves, each beside a small moving version of the picture that
taught it, then the facts that can't be derived. Then "next time", then ~8 s of end card.

## Coverage

Each item of the material, where it goes, and its tier.
- **Deep:** the chapter's key moves and intuitions, at §11's budget.
- **Reference:** routine material, tagged "reference" on screen. It still gets a motive and atomic
  steps.

| # | Material | Where | Tier |
|---|---|---|---|
| 1 | §2.6 opening: complex numbers suit oscillatory or periodic motion (a pendulum, AC circuits, waves in air and water); their differential equations come next term (notes p. 108) | ch1 s1; circuits again in ch4 s6 | reference |
| 2 | A simple pendulum swinging under gravity with angular frequency ω (notes p. 108). Scan p. 10's margin sketch: hatched ceiling, l, m, x(t), g | ch1 s5–s7 (the sketch is ch1's diagram) | deep |
| 3 | Small amplitude: ω = √(g/l), with g the gravitational acceleration. The notes state it without derivation | ch1 s7, derived; used in ch2 s8 | deep |
| 4 | x(t), the angular displacement about the vertical | ch1 s8 | reference |
| 5 | (81) x(t) = a cos ωt + b sin ωt, with a and b real | ch2 s7 | deep |
| 6 | "simple harmonic motion" (boxed term) | ch1 s8 (by its rule), ch2 s7 (by its form, the notes' sense) | deep |
| 7 | Figure 24: an arrow turning at ω round a circle, with a dot at its tip and its shadow dot on Re | ch2 s3–s5; ch3 s2 | deep |
| 8 | (82) x(t) = Re[A e^{iωt}], A a complex constant: the "complex amplitude" (boxed term) | ch3 s2 | deep |
| 9 | A = a − ib by comparing (81) and (82). The lecturer's working (scan p. 10): A = c̃ + id̃, Re = c̃ cos ωt − d̃ sin ωt, c̃ = a, −d̃ = b | ch3 s4: the picture is deep, the expansion reference | deep / ref |
| 10 | (83) v = dx/dt = d/dt Re[A e^{iωt}] = Re[d/dt A e^{iωt}] = Re[iωA e^{iωt}]; "differentiation is very easy, and is handled in the same way as for real variables" | ch3 s5 | deep |
| 11 | "to differentiate e^{iωt} we simply multiply by iω before taking the real part" | ch2 s3 (the arrow's derivative), ch3 s5 | deep |
| 12 | Example: x(0) = c, v(0) ≡ ẋ(0) = √3cω, so Re(A) = c and Re(iωA) = √3cω, so A = c(1 − i√3) = 2c e^{−iπ/3}. Amplitude \|A\| = 2c, phase −π/3, x(t) = 2c cos(ωt − ⅓π) (notes p. 109) | ch4 s3, as the faded example | deep |
| 13 | Amplitude \|A\| and phase (the notes' θ = −π/3) | ch3 s3; ch4 s3 | deep |
| 14 | Scan p. 12: "Re and d/dt commute" | ch2 s5 (the shadow of the acceleration), ch3 s5 (named), ch4 s6 | deep |
| 15 | Scan p. 12: "e^{iωt} on two sides of eq → cancel" | ch3 s4 (same shadow ⇒ same arrow), ch4 s6 | deep |
| 16 | Scan p. 12: "(e^{iωt})′ = iω e^{iωt}" | ch2 s3; ch4 s6 | deep |
| 17 | Scan p. 12 heading: "each oscillating quantity via complex amplitudes" (each its own amplitude, one e^{iωt}) | ch3 s5 (x, ẋ, ẍ as A, iωA, −ω²A); ch4 s6 | deep / ref |
| 18 | Recording 00:44:38: the complex form also makes integrals easy ("we'll do it later") | ch4 s6: integrating divides by iω | reference |
| 19 | Recording 00:45:34–00:46:08: the complex amplitude hands over the phase at once; "an easy, more convenient way to work with the oscillations" | ch4 s3, a side panel against the cos/sin route | reference |
| 20 | Examples Sheet I, F19, every part: show that X works, find the amplitude, write X = A e^{iϕ}, find the first two passages through the centre after t = 0, and the distances of the stationary points from the origin | ch4 s4–s5: hint ladder, then the solution | moves deep, solution ref |
| 21 | Student question 00:56:12: a CST student with GCSE physics asks whether it's OK not to follow the physics | shapes ch1: all its physics is built from GCSE facts. Not quoted | — |

Nothing in §2.6, or in the oscillation part of scan p. 12, is left out. Out of scope: Example 32
and the circuit on scan pp. 11–12 (the old part 7).

**Additions** (beyond the notes), each tagged on screen:
- ch1:
  - Hooke's law plus Newton, giving ẍ = −(k/m)x;
  - the rule read at its extremes;
  - gravity split along the rod and along the swing;
  - s = Lθ, and the mass cancelling;
  - sin θ ≈ θ, with numbers and where it fails;
  - one rule for two machines.
- ch2:
  - e^{λt}, giving λ² = −ω²;
  - the turning arrow's velocity, and Euler's formula seen from motion;
  - the acceleration pointing at the centre;
  - why the shadow obeys the rule;
  - the mirror pair;
  - the sine arrow starting at −i;
  - linearity;
  - a = x(0) and b = ẋ(0)/ω;
  - why every swing has this form (intuition only; proved next term);
  - the period 2π/ω and the 1 m pendulum;
  - the same beat at any size, and the large-angle caveat.
- ch3:
  - riding along with the arrow (A as the frozen arrow);
  - |A| cos(ωt + arg A) in general;
  - adding the arrows;
  - same shadow ⇒ same arrow;
  - the mirror-pair reading of Re.
- ch4:
  - A = x₀ − iv₀/ω in general;
  - the worked 3-4-5 example;
  - F19's centre as a hanging spring's balance point.

## Chapter 1 · The rule behind every swing
Slug: ch1_rule · ~11 min (~1750 words) · Source: notes PDF p. 27 (printed 108: the §2.6 opening, the
pendulum paragraph, ω = √(g/l)); scan p. 10 (the pendulum sketch, upside down) · Recording:
00:41:45–00:42:58 ("I'm not going to show you a physics course… take-home message…")
Goal: explain why a spring and a small-angle pendulum obey the same rule, ẍ = −ω²x, building it from
named physical facts (Hooke, Newton, gravity's components, the arc, sin θ ≈ θ), and read the rule at
its extremes.
Question: what makes things swing the way they do?
Key moves:
- M1 "Name the pull, then let Newton turn it into an acceleration": F = −kx, so ẍ = F/m = −(k/m)x.
- M2 "Split gravity along the rod and the swing: only the swing part drives" (ch1's wording, used
  everywhere). The along-swing part is mg sin θ. Not "the rod cancels one part": while the bob
  moves, the rod also supplies the pull toward the pivot that keeps it on its arc.
- M3 "For small swings, trade sin θ for θ: the arc and the sideways reach are almost equal."
Must remember: F = mẍ; Hooke's F = −kx; g = 9.81 m/s²; arc = radius × angle (in radians).
Pictures (the picture first, the formula as its caption):
- the spring stretched live, its RED pull arrow growing in step → F = −kx;
- the weight oscillating, with GREEN velocity and RED acceleration arrows, frozen at the end and in
  the middle with numbers → ẍ = −ω²x at its extremes;
- scan p. 10's pendulum, gravity split into a DIM along-rod arrow and a RED along-swing arrow. The
  RED arrow grows live as θ sweeps, with a readout of mg sin θ → F = −mg sin θ;
- the arc s (BLUE, with the YELLOW angle) on the same diagram → s = Lθ;
- on the same diagram, the bob's sideways reach L sin θ against its arc Lθ, swept live from 0 to
  60° with both readouts → sin θ ≈ θ.
Motives:
- M1: we want the motion, and Newton ties force to acceleration, which is position differentiated
  twice.
- M2: only the part of gravity along the swing can change the bob's speed.
- s = Lθ: Newton counts distance travelled and the pendulum counts angle; the arc converts one into
  the other.
- M3: θ̈ = −(g/L) sin θ has no answer in familiar functions. Trading sin θ for θ turns it into the
  spring's rule.
Think stops:
- T1.1 (s3) "Same spring, twice the mass. Is the acceleration back toward the middle bigger or
  smaller, and by how much?" → Half: ẍ = −(k/2m)x. So a heavier weight on the same spring swings
  more slowly.
- T1.2 (s4) "At the very end of its swing the weight is still for an instant. Is its acceleration
  zero there too?" → No, it's the largest: −ω² times the furthest x. Being still isn't the same as
  being unpulled (a named wrong idea, P9).
- T1.3 (s6) "Swap the bob for one twice as heavy. Does the pendulum swing faster, slower, or the
  same?" → The same: m cancels, because gravity's pull doubles with the mass. The spring's pull
  doesn't, which is why the mass mattered in T1.1.
Scenes:
- s1_hook · Hook (~50 s):
  - The phenomenon, within 20 s: a 1 m pendulum and a weight on a spring, side by side, swinging in
    step. A seconds counter shows the pendulum taking about one second each way.
  - Two identical pendulums, one swinging wide and one narrow, keep the same beat. Keep both
    amplitudes ≤ 15°, so this is honest (Decisions, "Checked").
  - The questions: what rule makes things swing like this, and what sets the beat?
  - The title card ("Part 1 · The rule behind every swing") over the swinging.
  - Framing (item 1), with DIM icons: pendulums, alternating currents, waves; their full equations
    come next term. By part two, complex numbers will turn out to be the natural language for all
    of them.
  - Say once that most of this part goes beyond the notes, which take the physics as given. The
    corner tag appears.
- s2_tools · Three tools (~55 s): names before process.
  - The legend opens: x (displacement from the middle, signed), ẋ velocity, ẍ acceleration. "A dot
    means rate of change in time; two dots, twice."
  - Three quick retrieval questions, each with a small picture, `{pause=1.5}` each, answered in a
    line:
    - a 10 N push on a 2 kg trolley → 5 m/s² (F = ma, so a = F/m; from here on, a is ẍ);
    - a right triangle with hypotenuse 10 and a 30° angle: the side opposite it → 5 (opposite =
      hypotenuse × sin);
    - an arc of radius 2 and angle 0.5 rad → length 1 (arc = radius × angle, in radians).
  - "Each one gets used in the next five minutes."
- s3_spring · The pull grows with the stretch (~95 s):
  - A weight on a spring on a frictionless table. It's horizontal so gravity stays out of it until
    ch4.
  - Pull it out live and the RED pull arrow grows. Twice the stretch, twice the pull: Hooke's law,
    from GCSE.
  - The sign beat, never skipped: x to the right is positive and the pull points left, so
    F = −kx. The minus means "back toward the middle".
  - M1, one operation per line: F = mẍ; substitute, mẍ = −kx; divide by m, ẍ = −(k/m)x.
  - Name ω² = k/m, "the pull back per unit of stretch, per kilogram". One sentence: why it's
    written as a square waits for part two.
  - T1.1.
- s4_extremes · Reading the rule (~75 s):
  - The spring now oscillates, with BLUE position, GREEN velocity and RED acceleration arrows on
    the weight; ẍ = −ω²x on screen.
  - A number first: ω² = 4, x = 0.5 gives ẍ = −2.
  - Freeze in the middle: x = 0, no pull, but the GREEN arrow is at its longest. It's fastest here,
    so it overshoots.
  - Freeze at the end: the GREEN arrow is gone and the RED one is at its longest.
  - T1.2.
  - So it can never settle in the middle: that's why it swings.
- s5_gravity · What pulls a pendulum back (~115 s):
  - Scan p. 10's sketch, redrawn: hatched ceiling, dashed vertical, rod L, bob m, gravity mg (FG)
    straight down, and the YELLOW angle θ ("the notes call this angle x; for the geometry, θ for
    now").
  - Two forces act on the bob: gravity, and the rod's pull along itself. The rod pulls at right
    angles to the swing, so it can't speed the bob up along the swing.
  - M2, atomic: gravity is vertical; the rod leans θ off the vertical; so gravity and the rod are
    θ apart. Split gravity along the rod (DIM, mg cos θ) and along the swing (RED).
  - The along-swing part is the side opposite θ: mg sin θ (s2's triangle). It points back toward
    the bottom, so F = −mg sin θ.
  - Live sweep, θ from 0 to 40° to −40°: the RED arrow grows and flips, with a readout of mg sin θ.
- s6_arc · From angle to distance (~85 s):
  - Newton along the swing: m × (acceleration along the arc) = −mg sin θ. Divide by m: the
    acceleration is −g sin θ.
  - T1.3, contrasted with the spring.
  - The bob moves on an arc of radius L, so the distance along it is s = Lθ (s2's arc, θ in
    radians). Differentiate twice: s̈ = Lθ̈, since L is fixed.
  - So Lθ̈ = −g sin θ, and θ̈ = −(g/L) sin θ.
  - Read it back: "almost the spring's rule, but with sin θ where θ should be".
  - One sentence: that equation has no answer in familiar functions.
- s7_small · Small swings (~90 s):
  - M3. On the same diagram: the bob's sideways reach L sin θ (BLUE, straight) against its arc Lθ
    (YELLOW, curved).
  - Live sweep, θ from 0 to 60°, with readouts of θ, sin θ and the gap:
    - 0.1 rad: 0.0998 (0.2% short);
    - 10° = 0.1745 rad: 0.1736 (0.5% short);
    - 30°: 4.5% short;
    - 60° = 1.047 rad: 0.866 (17% short).
  - For small swings, θ̈ ≈ −(g/L)θ: the spring's rule, with ω² = g/L, so ω = √(g/L) (DIM tag
    "notes p. 108": the notes state it, and here it's built).
  - Read it back: "a longer pendulum is pulled back more gently, per radian".
  - The 1 m pendulum: ω² = 9.81, so ω ≈ 3.13 per second. Its beat is part two's.
  - An honest flag: at big angles the real pull is weaker than the rule says (sin θ < θ). Part two
    shows what that costs.
  - The corner tag "beyond the notes" leaves here.
- s8_recap · One rule, and recap (~95 s):
  - One rule, two machines (~35 s): the spring and the pendulum side by side under ẍ = −ω²x, with
    ω² = k/m and ω² = g/L. "Whatever swings, call its displacement x": the pendulum's θ becomes x,
    the notes' name for the angle.
  - Anything pulled back in proportion to how far out it is obeys this rule. That's simple harmonic
    motion, named here by its rule; part two finds its form.
  - Recap (≤ 60 s), each small and moving: M1 (the spring's growing arrow), M2 (the split gravity),
    M3 (arc against reach). The must-remember facts in one DIM line.
  - Next time: which motion obeys ẍ = −ω²x, a function that comes back as −ω² times itself after
    two derivatives? The answer is the shadow of a turning arrow. End card.
Continuity:
- x BLUE, ẋ GREEN, and ẍ and every pull RED, from here to ch4.
- The pendulum drawing (scan p. 10's sketch) and the spring drawing are reused in every chapter.
  Build each once, and record the helper names in STATUS.md.
- The 1 m pendulum returns in ch2 s8. ch2 pins the rule ẍ = −ω²x.

## Chapter 2 · Shadows of a turning arrow
Slug: ch2_shadow · ~12 min (~1900 words) · Source: notes PDF p. 27 ((81), "simple harmonic motion",
Figure 24); scan p. 10. The prior picture is the old De Moivre video's two arrows
(`../l10-complex-roots-logs/script/ch2_de_moivre.md`, c2.expo.3), here moving in time · Recording:
00:42:44–00:43:03 ("a superposition of the sine and cosine… simple harmonic motion")
Goal: find the motions that obey ẍ = −ω²x by reading them off a turning arrow. Its velocity is iω
times the arrow, a quarter turn ahead; its acceleration is (iω)² = −ω² times the arrow, straight back.
Get cos ωt and sin ωt as its shadows and every motion as a cos ωt + b sin ωt, and explain the period
2π/ω and why it ignores the size of the swing.
Question: which motion obeys the rule?
Key moves:
- M4 "Try e^{λt}: differentiating it only multiplies by λ, so the rule becomes λ² = −ω²." No real λ
  works; λ = ±iω. The rule itself asks for complex numbers.
- M5 "Differentiating a turning arrow turns it a quarter turn ahead and stretches it by ω":
  d/dt e^{iωt} = iω e^{iωt}. Twice is half a turn, −ω², so the arrow obeys the rule.
- M6 "Take the shadow: the real part of an arrow that obeys the rule is a real motion that obeys
  it." A real swing is a mirror pair of arrows.
Must remember: e^{iθ} = cos θ + i sin θ (known from before, now seen from motion), and the period
2π/ω.
Pictures:
- one knob (P4): graphs of e^{λt} for λ = 1 (grows) and λ = −1 (decays). Neither swings → λ² = −ω²
  has no real answer;
- the GOLD arrow e^{iωt} turning, with a readout like "ωt = 1.20 rad". A GREEN velocity arrow rides
  its tip at right angles, then slides to the origin: a quarter turn ahead → d/dt e^{iωt} = iω e^{iωt};
- a RED acceleration arrow, a further quarter turn on, pointing at the centre → (iω)² = −ω²;
- the BLUE shadow dot on the real axis, with the bob on that same line (one dot, two causes, P7).
  Then a time axis unrolls the wave → cos ωt;
- the user's picture (P6), now moving in time: GOLD e^{iωt} and PURPLE e^{−iωt} tip to tail, their
  sum riding the real axis at 2cos ωt → cos ωt = ½(e^{iωt} + e^{−iωt});
- an arrow starting at −i, straight down → sin ωt; two waves adding → (81);
- the arrow's full turn as a TEAL arc, with a t readout → T = 2π/ω;
- two arrows of different lengths turning together, their shadows returning together → the same
  beat at any size.
Motives:
- M4: exponentials are the functions that differentiation only rescales, so two derivatives become
  one multiplication.
- M5: we need to know what e^{iωt} does over time, and whether the exponential rule survives an
  imaginary λ.
- M6: the bob is real and the arrow is complex; the shadow brings the answer back to the line.
- The mirror pair: the rule allowed two λ's, and combining them is how a real answer comes out of
  complex ones.
- (81): a swing can start anywhere at any speed. One cosine can't match that; mixes can.
- The period: the hook of part one asked what sets the beat.
Think stops:
- T2.1 (s2) "e^{λt}, differentiated twice, is λ² e^{λt}. Which λ makes λ² = −ω²?" → λ = iω or
  λ = −iω: since i² = −1, (iω)² = −ω², and (−iω)² too.
- T2.2 (s4) "The velocity is the arrow turned a quarter turn ahead and stretched by ω. Where does the
  acceleration point, and how long is it?" → Another quarter turn on: straight back at the centre,
  length ω². It is −ω² times the arrow.
- T2.3 (s7) "A pendulum is released from rest at 0.1 radians. What are the cosine coefficient and
  the sine coefficient?" → a = 0.1 and b = 0 (ẋ(0) = bω = 0), so x = 0.1 cos ωt.
- T2.4 (s8) "A pendulum four metres long. What's its period?" → ω² = g/L is a quarter as big, so ω
  halves and the period doubles: ≈ 4.0 s.
Scenes:
- s1_hook · Hook (~55 s):
  - The phenomenon: the weight oscillating on its line, its BLUE position wave drawing beside it,
    with the pinned rule ẍ = −ω²x as its caption.
  - The question: which x(t) obeys this?
  - Title card ("Part 2 · Shadows of a turning arrow").
  - Retrieval, `{pause=1.5}` each:
    - ω² for a pendulum of length L → g/L (part one);
    - what multiplying by i does to an arrow → a quarter turn anticlockwise (the earlier L10
      videos);
    - the derivative of cos 3t → −3 sin 3t (the chain rule; needed in s5).
- s2_guess · Try an exponential (~85 s):
  - "You may already have a guess; hold on to it."
  - M4, numbers first: e^{t} grows and e^{−t} decays (live graphs). For e^{λt}, the rate of change
    is λ times the value.
  - Differentiate twice: λ² e^{λt}. Put it into the rule: λ² e^{λt} = −ω² e^{λt}. e^{λt} is never
    zero, so λ² = −ω².
  - T2.1.
  - A real λ, squared, is never negative, so no real exponential swings. λ = ±iω.
  - "Before trusting this, check that the exponential rule still holds when λ is imaginary, and see
    what e^{iωt} does": the next scene.
  - The chapter's "beyond the notes" is said here.
- s3_velocity · A quarter turn ahead (~110 s): picture first.
  - e^{iωt} is the unit arrow at angle ωt: the earlier videos' e^{iθ}, with θ = ωt growing at ω
    radians per second. Live: the GOLD arrow turns, with an ωt readout.
  - The tip runs along the circle, so its velocity is along the circle: at right angles to the
    arrow, a quarter turn ahead. Its speed is ω (radius 1, ω radians per second).
  - Slide the GREEN velocity arrow to the origin: it is the arrow, times i (a quarter turn), times
    ω (the length).
  - Caption: d/dt e^{iωt} = iω e^{iωt} (M5). The exponential rule holds with λ = iω.
  - The other way round (beyond the notes, two sentences): an arrow whose velocity is always a
    quarter turn ahead never changes its length. So, starting at 1, it stays on the unit circle and
    covers ω radians a second. That's why e^{iωt} = cos ωt + i sin ωt: Oiler's formula, seen from
    motion.
  - Reference check, atomic, beside the picture: d/dt(cos ωt + i sin ωt) = −ω sin ωt + iω cos ωt =
    iω(cos ωt + i sin ωt), since iω · i sin ωt = −ω sin ωt.
- s4_accel · Half a turn: back to the centre (~65 s):
  - T2.2.
  - The answer: the RED acceleration arrow, half a turn on, pointing at the centre:
    d²/dt² e^{iωt} = (iω)² e^{iωt} = −ω² e^{iωt}.
  - Live: the GOLD, GREEN and RED arrows turning together.
  - The arrow obeys the rule, as a picture: it's always pulled toward the centre, harder the
    further out it is. (Physicists call this centripetal acceleration: optional, one clause.)
- s5_shadow · The shadow (~95 s):
  - But the bob lives on a line, and x is real. M6: watch the arrow's shadow on the real axis,
    BLUE, and put the bob on the same line. They move as one (P7).
  - Why the shadow obeys the rule: take the real part of both sides. The shadow of the acceleration
    is the acceleration of the shadow, because the sideways motion and the up-and-down motion are
    separate. (Coverage item 14, first used here, named in ch3.)
  - So x = Re e^{iωt} = cos ωt. Unroll it along a time axis into a wave.
  - Concrete check (reference, atomic): x = cos ωt; ẋ = −ω sin ωt; ẍ = −ω² cos ωt = −ω²x ✓.
  - Read it back: "cos ωt is the shadow of a point going round at ω radians per second."
  - A confusion to name (from the old part 6): two different angles. The arrow's angle ωt grows
    forever; the pendulum's angle x stays small, and it's the shadow.
- s6_mirror · Two arrows, one swing (~70 s):
  - The other answer, λ = −iω: e^{−iωt}, the PURPLE mirror arrow, turning clockwise. It obeys the
    rule too, since (−iω)² = −ω², and its shadow is the same cos ωt.
  - The user's picture from the De Moivre video, now moving in time: put the two arrows tip to
    tail. The vertical parts cancel, and the sum rides the real axis at 2cos ωt (live, BLUE
    readout).
  - Caption: cos ωt = ½(e^{iωt} + e^{−iωt}).
  - Read it back: "a real swing is two complex swings turning opposite ways. Taking the shadow is
    the same as averaging an arrow with its mirror."
- s7_every · Every swing (~95 s):
  - The sine: an arrow starting at −i, pointing straight down, turning anticlockwise. Its shadow
    starts at 0 and reaches +1 a quarter turn later: sin ωt = Re(−i e^{iωt}). One line:
    −i(cos ωt + i sin ωt) = sin ωt − i cos ωt.
  - Mixes: the rule is linear. If x₁ and x₂ obey it, so does a x₁ + b x₂. Atomic: ẍ₁ = −ω²x₁ and
    ẍ₂ = −ω²x₂; add a times the first to b times the second. Physically: add two motions, and their
    pulls add.
  - Caption: x(t) = a cos ωt + b sin ωt (81), with "simple harmonic motion" boxed (the notes'
    term).
  - What a and b mean, one line each: x(0) = a, and ẋ(0) = bω. So a is where it starts, and b is
    how fast it starts, divided by ω.
  - The running example: start at 3 cm, moving out at 12 cm/s, ω = 3, so x = 3 cos 3t + 4 sin 3t
    (its wave drawn as two waves adding).
  - A flagged skip (beyond the notes; proved next term): why these are all the motions. The rule
    fixes the acceleration from the position, so a start position and a start velocity leave
    nothing free, and a and b can match any start.
  - T2.3.
- s8_period · The beat (~95 s): the hook of part one asked for this.
  - One full turn of the arrow is one swing, there and back: ωt grows by 2π (TEAL) in T = 2π/ω.
  - Numbers: the 1 m pendulum has ω ≈ 3.13 per second, so T ≈ 2.01 s, a second each way. A
    grandfather clock's pendulum is 0.994 m long for exactly that reason.
  - T2.4.
  - A named wrong idea (P9): "a wider swing takes longer, since it has further to go." But
    T = 2π/ω has no size in it: a longer arrow turns at the same rate. Show two arrows, one twice as
    long, their shadows returning together. Physically: twice as far out means twice the pull, and
    twice the speed all the way.
  - The honest caveat (part one's flag): a real pendulum at big angles is pulled back less than the
    rule says, so its big swings are slower. With an amplitude of 10° the period is 0.2% longer; 30°,
    1.7%; 60°, 7.3%. Live: a 10° and a 60° pendulum drifting apart. Integrate the real equation
    θ̈ = −(g/L) sin θ numerically (RK4) for the 60° one.
- s9_recap · Recap (~50 s):
  - Each small and moving: M4 (the λ graphs), M5 (the arrow with its GREEN and RED arrows), M6 (the
    shadow, and the mirror pair).
  - Must remember: Oiler's formula, and T = 2π/ω.
  - Next time: (81) needs two numbers and two functions, and every derivative swaps cosine for
    sine. One complex number can hold the whole swing. End card.
Continuity:
- Built here and reused unchanged in ch3–4: the GOLD arrow, its BLUE shadow with the bob on the same
  line, the GREEN and RED arrows, the PURPLE mirror, and the TEAL turn.
- The sine arrow starting at −i is the key to ch3 s4. The 3-4-5 swing starts here.

## Chapter 3 · The complex amplitude
Slug: ch3_amplitude · ~9 min (~1440 words) · Source: notes PDF pp. 27–28 ((82), the boxed "complex
amplitude", A = a − ib, (83)); scan p. 10 (the A = c̃ + id̃ working); scan p. 12 (the three rules,
and "each oscillating quantity via complex amplitudes") · Recording: 00:43:03–00:44:59, and
00:50:59–00:51:48 (the rules, said there for the circuit: use only what applies to one oscillator)
Goal: write any swing as x(t) = Re[A e^{iωt}], read its amplitude and phase off A, convert between A
and (81)'s a and b (A = a − ib), and differentiate by multiplying A by iω.
Question: can one number hold a whole swing?
Key moves:
- M7 "Ride along with the arrow and it holds still: that frozen arrow, A, is the whole motion" (P8).
- M8 "Add the arrows, not the waves: a cos ωt + b sin ωt is the shadow of the one arrow a − ib."
- M9 "The velocity of the shadow is the shadow of the velocity: differentiate the arrow (×iω), then
  take the shadow."
Must remember: A = a − ib (or re-derive it with M8); |A| is the amplitude and arg A the phase.
Pictures:
- an arrow starting anywhere (length 5, angle −53°: the 3-4-5 swing), turning. The camera rides
  along at ω and the arrow freezes as A. Release it, and A e^{iωt} turns again → x = Re[A e^{iωt}]
  (82), with A GOLD, e^{iωt} GOLD (its angle ωt is the YELLOW arc), and Re the BLUE shadow;
- knobs on the frozen A: its length stretches the wave and its angle slides it (live, with readouts
  of |A| and arg A) → x = |A| cos(ωt + arg A);
- the cosine arrow (a, along Re) and the sine arrow (b, pointing down) tip to tail, turning as one
  rigid piece; their shadows add → A = a − ib;
- two arrows turning together, their shadows equal at t = 0 and again a quarter turn later → they're
  the same arrow, so matching is allowed;
- the GOLD, GREEN and RED arrows from the origin, locked a quarter turn apart, turning as one fan.
  Their three shadows are x, ẋ, ẍ (live readouts) → amplitudes A, iωA, −ω²A.
Motives:
- M7 and (82): (81) needs two numbers and two functions, and each derivative swaps them. One arrow
  holds both and differentiates by one multiplication.
- |A| and arg A: how big a swing is, and where it starts, are the two things you want to know.
- M8: to move between the two descriptions. Same shadow ⇒ same arrow: to be sure comparing them is
  allowed.
- M9 and (83): velocity is what start conditions talk about.
Think stops:
- T3.1 (s3) "A complex amplitude of 2i. Where does the swing start, and which way does it move
  first?" → The arrow points straight up, so its shadow is at the centre. Turning anticlockwise, it
  heads left: x goes negative first (x = −2 sin ωt).
- T3.2 (s4) "Which complex amplitude gives 6 cos 3t − 8 sin 3t, and how big is that swing?" →
  b = −8, so A = 6 + 8i (above the axis this time), and |A| = √(36 + 64) = 10. Changed in the
  continuity review: the third weight's size was already on screen (the hook's crest tick, s3's
  readout). The scene then turns the third weight into 3 − 4i, five long, outside the stop.
- T3.3 (s5) "A complex amplitude of 2, with ω = 3. What's the velocity's complex amplitude, and what
  is the weight doing at t = 0?" → iωA = 6i. Its shadow is 0, so the weight is still for an
  instant, at the far end (x(0) = 2, the full amplitude).
Scenes:
- s1_hook · Hook (~55 s):
  - The phenomenon: three weights on identical springs, started differently (from rest at the edge;
    pushed from the middle; halfway out and moving). Three waves with one beat, but different
    heights and shifts.
  - Each is a cos + b sin with its own two numbers, and every derivative swaps cosines and sines.
    The question: can one number hold a whole swing?
  - Title card ("Part 3 · The complex amplitude").
  - Retrieval, `{pause=1.5}` each:
    - where the arrow whose shadow is sin ωt starts → at −i, pointing down;
    - what differentiating does to e^{iωt} → a quarter turn ahead, stretched by ω;
    - the modulus of 3 + 4i → 5 (from Lecture 9).
- s2_freeze · One arrow (~100 s): picture first.
  - Any arrow, of any length, starting at any angle, turning at ω: its shadow obeys the rule too.
    Part two's argument never used where the arrow started: the velocity is iω times the arrow and
    the acceleration −ω² times it.
  - M7: ride along at ω (the plane counter-rotates) and the arrow holds still. That frozen arrow is
    A.
  - Release it: multiplying by e^{iωt} keeps the length and adds ωt to the angle (from the earlier
    videos).
  - Caption: x(t) = Re[A e^{iωt}] (82), with "complex amplitude" boxed. Each symbol is coloured like
    its referent.
  - Read it back: "start at the arrow A, turn it by ωt, take the shadow." A is complex and x is
    real: the shadow throws the vertical part away.
  - The mirror-pair reading, one beat: the shadow is also half the sum of A e^{iωt} and its PURPLE
    mirror A* e^{−iωt}. That's part two's picture, with any arrow.
- s3_read · Size and start (~85 s):
  - The frozen A, with its length (GOLD) and its angle (YELLOW).
  - Its length is how far the shadow reaches: the amplitude, |A|. Its angle is where the arrow
    starts: the phase, arg A (the notes' words). So x = |A| cos(ωt + arg A).
  - Live knobs: stretch A and the wave grows; turn A and the wave slides (with readouts).
  - The 3-4-5 swing's A as an example: length 5, angle ≈ −0.93 rad.
  - T3.1.
- s4_add · From a and b to A (~125 s): M8, picture first.
  - The cosine arrow starts at 1 (from part two), so a cos ωt is the shadow of the arrow a e^{iωt}.
    The sine arrow starts at −i, so b sin ωt is the shadow of −ib e^{iωt}.
  - Put them tip to tail: they turn together as one rigid arrow, and shadows add. So
    a cos ωt + b sin ωt = Re[(a − ib)e^{iωt}], and A = a − ib (boxed; a BLUE, −ib PINK).
  - Why the minus: the sine part has to start pointing down, so that a quarter turn later it points
    right.
  - Reference check: the expansion, by scan p. 10's route, with α + iβ for the lecturer's c̃ + id̃.
    - (α + iβ)(cos ωt + i sin ωt) = α cos ωt + iα sin ωt + iβ cos ωt + i²β sin ωt;
    - i² = −1;
    - the real part is α cos ωt − β sin ωt;
    - so α = a and −β = b.
  - Why matching is allowed: if two arrows turning together cast the same shadow at every moment,
    they're the same arrow. At t = 0 the shadows give the real parts. A quarter turn later the
    vertical parts have swung onto the axis, and the shadows give the imaginary parts. That's the
    rule "e^{iωt} on both sides cancels".
  - T3.2. Its answer gives |A| = √(a² + b²) by Pythagoras.
- s5_velocity · Calculus becomes multiplication (~125 s): M9.
  - (83), atomic:
    - v = ẋ = d/dt Re[A e^{iωt}];
    - = Re[d/dt (A e^{iωt})]: the derivative of the shadow is the shadow of the derivative, since
      d/dt(u + iv) = u̇ + iv̇;
    - = Re[iωA e^{iωt}]: part two's quarter turn.
  - In words: to differentiate, multiply by iω before taking the real part.
  - Picture: the GREEN arrow iωA e^{iωt}, a quarter turn ahead of the GOLD one. Its shadow and the
    weight's velocity readout agree (live). Once more: the RED −ω²A e^{iωt}, half a turn ahead.
  - Every oscillating quantity gets its own complex amplitude, all turning with one e^{iωt}:
    position A, velocity iωA, acceleration −ω²A.
  - The 3-4-5 swing: 3 − 4i, 12 + 9i and −27 + 36i, so ẋ(0) = 12 and ẍ(0) = −27.
  - The rule ẍ = −ω²x now reads −ω²A = −ω²A: it holds by multiplication alone.
  - T3.3.
- s6_recap · Recap (~50 s):
  - Each small and moving: M7 (the arrow freezing), M8 (two arrows tip to tail), M9 (the fan of
    three arrows and their shadows).
  - Must remember: A = a − ib; |A| is the amplitude and arg A the phase.
  - Next time: a swing's start decides its A, and the sheet question. End card.
Continuity:
- ch3 pins x = Re[A e^{iωt}] from s2 on, and ch4 keeps it pinned.
- The fan of three arrows (s5) is what ch4 s6 shows for "each quantity its own amplitude".
- ch4 s2 finds the 3-4-5 swing's A from its start.

## Chapter 4 · Putting it to work
Slug: ch4_work · ~10 min (~1610 words) · Source: notes PDF p. 28 (printed 109: the example after
(83)); scan p. 12 (the three rules); Examples Sheet I, F19 (PDF p. 9) · Recording:
00:44:35–00:46:18 (the example; 00:44:38 the integrals remark; 00:45:34–00:46:08 "an easy, more
convenient way") and 00:50:59–00:51:48 (the rules)
Goal: find a swing's complex amplitude from how it starts (A = x₀ − iv₀/ω), read off its amplitude
and phase, time events by where the arrow points, and collect the rules that turn oscillation
problems into algebra.
Question: given how a swing starts, can you predict every moment of it?
Key moves:
- M10 "Set t = 0: the turning factor becomes 1, so the start reads straight off A". Re A = x₀ and
  Re(iωA) = v₀, so A = x₀ − iv₀/ω.
- M11 "Ask where the arrow points: straight up or down, the weight is passing the centre; flat, it's
  still for an instant."
- The toolkit: "every oscillating quantity becomes a frozen arrow; ×iω differentiates; equal
  shadows mean equal arrows."
Must remember: the three rules (scan p. 12).
Pictures:
- the frozen arrow A, with its BLUE real leg x₀ and its PINK vertical leg −v₀/ω (pointing down for
  an outward push) → A = x₀ − iv₀/ω;
- the 1-√3-2 triangle: an arrow of length 2c at −60°, its shadow starting at c (half the amplitude)
  and moving outward;
- F19: the 7-24-25 arrow turning at 3 rad/s over a number line centred at 7. A t sweep with
  readouts of t, the arrow's angle 3t − δ, and x; each event flagged as the arrow passes vertical or
  horizontal;
- the toolkit card: three small pictures (the shadow of the derivative equals the derivative of the
  shadow; two arrows with equal shadows are one arrow; the quarter turn), plus the quarter turn back
  for integration.
Motives:
- M10: problems tell you how a swing starts, not its A.
- M11: the sheet's questions are about where the weight is, and the arrow's angle answers them at
  once. Polar form hands over that angle directly.
- The toolkit: the next video's circuit needs these rules.
Think stops:
- T4.1 (s3) "It starts at C, moving outward at root three times C omega. Using the move, what's the
  complex amplitude?" → A = c − i√3cω/ω = c(1 − i√3).
- T4.2 (s3) "How long is that arrow, and at what angle?" → √(c² + 3c²) = 2c, at −π/3 (−60°),
  taking c > 0.
- T4.3 (s4, after hint 1) "The displacement from the centre is the shadow of (24 − 7i)e^{3it}. How
  big is the swing?" → |24 − 7i| = √(576 + 49) = √625 = 25.
- T4.4 (s5, after hint 2) "The weight passes the centre when the arrow points straight up or down.
  When does it first point straight up?" → When 3t − δ = π/2, so t = (π/2 + δ)/3 ≈ 0.618 s.
Scenes:
- s1_hook · Hook (~55 s):
  - The phenomenon: a weight hanging from a spring, bobbing about the point where it would hang at
    rest.
  - The question: if you know how a swing starts, can you predict every moment of it?
  - Title card ("Part 4 · Putting it to work").
  - Retrieval, `{pause=1.5}` each:
    - the complex amplitude of 3 cos 3t + 4 sin 3t → 3 − 4i (part three);
    - the velocity's complex amplitude → iω times A (part three);
    - the period of a 1 m pendulum → about 2 s (part two, spaced).
- s2_start · Worked: from the start to the swing (~105 s): worked, with the moves named, numbers
  first.
  - The 3-4-5 swing from its start: ω = 3, starting at 3 cm and moving outward at 12 cm/s.
  - Atomic steps:
    - x(t) = Re[A e^{3it}];
    - set t = 0, where e^0 = 1 (M10): x(0) = Re A = 3;
    - ẋ(t) = Re[3iA e^{3it}], so ẋ(0) = Re(3iA) = 12;
    - write A = 3 + iβ;
    - 3iA = 9i − 3β;
    - its real part: −3β = 12, so β = −4;
    - A = 3 − 4i, |A| = 5, arg A = −arctan(4/3) ≈ −0.93 rad (−53°);
    - x = 5 cos(3t − 0.93).
  - Check: that's part two's 3 cos 3t + 4 sin 3t.
  - Picture: the frozen arrow, with legs 3 (BLUE) and −4i (PINK, down); the shadow starts at 3 and
    moves out.
  - Then the general case with letters (tag "beyond the notes"): A = x₀ − iv₀/ω. Read it back: "the
    real part is where it starts; the vertical part, times minus omega, is how fast; an outward
    push tips the arrow below the axis."
- s3_notes · Faded: your turn, with letters (~115 s):
  - The example from the notes (tag "example · notes p. 109"): x(0) = c, ẋ(0) = √3cω. "This time
    you supply the moves."
  - T4.1.
  - Then the notes' own route, atomic: Re(A) = c; Re(iωA) = √3cω; A = c + iβ; iωA = iωc − ωβ;
    −ωβ = √3cω; β = −√3c. It arrives at the same A = c(1 − i√3).
  - T4.2: the 1-√3-2 triangle, so A = 2c e^{−iπ/3}. Amplitude 2c, phase −π/3, and
    x(t) = 2c cos(ωt − π/3) (the notes write −⅓π).
  - Check on the picture: the shadow starts at c, half the amplitude, and moves out. The GREEN
    velocity arrow is at +30°, and its shadow is √3cω.
  - Side panel (reference): with sines and cosines you'd find a = c and b = √3c, then need a trig
    identity for the amplitude and phase. The complex amplitude hands over both at once, in polar
    form.
- s4_f19 · F19: the question and the move (~100 s):
  - The sheet's question card, verbatim (DIM tag "F19 · Examples Sheet I").
  - The 7: a weight hanging on a spring bobs about the point where the spring's pull balances
    gravity. Measured from there, it's the same rule (tag "beyond the notes"). So x − 7 is the
    swing.
  - Hint 1, the move: x − 7 is the shadow of an arrow; read A off with M8 (part three). a = 24,
    b = 7, ω = 3, so A = 24 − 7i and X = (24 − 7i)e^{3it}.
  - The "show that", atomic: expand, use i² = −1, take the real part: Re X = 24 cos 3t + 7 sin 3t.
  - T4.3. The amplitude is 25: a 7-24-25 triangle, the 3-4-5's big sibling.
- s5_events · F19: where the arrow points (~120 s):
  - Hint 2, the first step: polar form. 24 − 7i = 25 e^{−iδ}, with δ = arctan(7/24) ≈ 0.284 rad
    (16.3°), so X = 25 e^{i(3t − δ)}.
  - That's the sheet's A e^{iϕ}, with A = 25 and ϕ = 3t − δ. A small DIM mapping box: "the sheet's
    A = our |A|; the sheet's ϕ = the arrow's angle".
  - M11. T4.4.
  - The solution (tag "reference": atomic on screen, summarised aloud):
    - the weight passes the centre when cos(3t − δ) = 0: 3t − δ = π/2 gives t ≈ 0.618 s, and
      3t − δ = 3π/2 gives t ≈ 1.665 s;
    - it's stationary when the arrow lies flat: x − 7 = ±25, so x = 32 or x = −18.
  - A named wrong idea: "the distances are 25". The sheet asks for distances from the origin, so
    they're 32 and 18.
  - Live t sweep from 0 to 2.2 s. The arrow starts just below flat: x(0) = 31, rising to 32 at
    t ≈ 0.095, through 7 at 0.618, down to −18 at 1.142, and through 7 again at 1.665.
- s6_toolkit · The toolkit (~60 s), reference:
  - The three rules from scan p. 12, each with its small picture from parts two and three: Re and
    d/dt commute; e^{iωt} on both sides of an equation cancels; (e^{iωt})′ = iω e^{iωt}.
  - Integrating runs the other way: it divides by iω, a quarter turn back. This is the lecturer's
    integrals remark; it holds up to a constant, which is zero for a pure swing.
  - Every oscillating quantity gets its own complex amplitude, all turning with one e^{iωt}.
  - Teaser: in a circuit, a voltage, a current and two more quantities oscillate together. Each
    becomes a frozen arrow, every derivative becomes ×iω, and the circuit becomes algebra. That's
    the next video, on impedance.
- s7_recap · Recap (~50 s):
  - Each small and moving: M10 (the frozen arrow's legs), M11 (the F19 arrow at its four events),
    the toolkit card.
  - Then the whole pilot in one line, over four thumbnails: the rule (part one), the arrow (part
    two), the amplitude (part three), the start (part four). End card.
Continuity:
- This closes the pilot. The old part 7 (impedance) follows; its hook says "d/dt becomes
  multiplication by iω", which is true here too.
- Build the toolkit card's three pictures so they can be reused if part 7 is redone in deep style.

## Decisions
- **Four chapters: ~42 min of narration, ~50 min of video.** That's ~9× the lecture's 4.5 min, and
  ~4.8× the old part 6. Why so much more:
  - ch1 (~11 min) is built entirely from what the notes take as given: ω = √(g/l), with the physics
    "next term". The user asked for "the physics first", and a CST student asked about exactly this
    at 00:56:12.
  - ch2 derives the solution of SHM, which the notes state without derivation, plus Euler's formula
    seen from motion (DEEP_STYLE §2 names exactly this).
  - ch3–4 cover the notes' own content at the deep budget (~3 ideas a minute), with worked → faded →
    yours.
  - Each chapter answers one question.
- **Why not three or five chapters.**
  - Merging ch3 and ch4 gives ~16 min, over the 14-min cap. It would hold (82), (83), the arrow
    algebra, two examples and F19 at once, the density the user objected to.
  - Splitting ch1 into spring and pendulum would leave two halves under 8 min.
  - ch2 has 9 scenes, above the agent file's 6–8, because s3 and s4 (velocity, acceleration) would
    run ~5 ideas a minute as one scene.
- **To shorten** (the user may prefer):
  - (a) drop the spring and keep only the pendulum: −1.5 min. It loses the cleanest picture of "pull
    ∝ stretch", and F19's hanging-spring centre.
  - (b) fold ch2 s6 (the mirror pair) into s5: −0.8 min. It's the user's favourite picture, so I
    kept it.
  - (c) move F19's solution to a hint-ladder page (§10): −1.5 min.
  - (d) drop ch4 s2's worked numeric example and use the notes' example as the worked one: −1.7 min.
    It loses concrete-before-abstract, and the running example's payoff.
  - All four together: ~36 min.
- **Order** (§1 lets us restructure). The notes go (81) → Figure 24 → (82) → A = a − ib → (83) →
  example. Here:
  - Physics first (ch1). The notes take ω = √(g/l) as given; here it's derived. (81) comes after
    it, as the answer to "which motion obeys the rule?".
  - The turning arrow comes before (81) (study pattern P3). The arrow's derivative, ×iω (the idea
    behind (83)), is the reason the motion is a cosine. So d/dt = ×iω appears in ch2 for e^{iωt},
    and again in ch3 for A e^{iωt} as (83).
  - (81) arrives as the general shadow (ch2 s7). (82) then packs it into one number (ch3).
  - A = a − ib is read off a picture (two arrows tip to tail) before the notes' expansion.
  - "Re and d/dt commute" is used informally in ch2 s5 before being named in ch3 s5.
  - The notes' example becomes the second, faded example in ch4, after a worked numeric one (§9:
    concreteness fading; worked → faded → yours). F19 is "yours".
- **F19 is in ch4**: hint 1 (the move), a think stop, hint 2 (the first step), a think stop, then
  the solution (reference tier), all in the same video.
  - There's no bonus chapter: F19 alone is ~4 min, under the 8-min floor.
  - The old part 8 already has an old-style F19 solution (`../l10-complex-roots-logs/out/`, its s7).
  - If chapter markers are added to `stitch()` (§10), the viewer can stop before the solution.
- **Tiers.**
  - Deep: the moves M1–M11 and their pictures; the period and the same beat at any size; (82),
    (83), A = a − ib's picture; the notes' example.
  - Reference: the §2.6 framing; naming x as the notes' angle; the derivative checks by expansion
    (ch2 s3, s5); the lecturer's expansion for A = a − ib (ch3 s4); the side panel (ch4 s3); F19's
    solution lines; the toolkit and integration (ch4 s6).
- **14 think stops** (3, 4, 3, 4). Each is answerable from the previous minute. Quick predictions
  (`{pause=1.5}`) are separate: the retrieval questions (3 per chapter) and any "which way will it
  go?" beats.
- **Retrieval openers.**
  - ch1's predecessor, the old part 5 (z^w), holds nothing ch1 needs. So ch1 retrieves its tools
    instead: F = ma, opposite = hypotenuse × sin, arc = radius × angle.
  - ch2 retrieves ch1, plus L10's "×i is a quarter turn" and the chain rule.
  - ch3 retrieves ch2, plus L9's modulus.
  - ch4 retrieves ch3, plus ch2's period (spacing).
- **Hooks open on the phenomenon** (§11):
  - ch1: a pendulum and a spring in step;
  - ch2: the weight and its rule;
  - ch3: three swings with one beat;
  - ch4: a hanging spring.
  The title card comes over the moving picture, so the agent file's "title card, then the question"
  and §11's "phenomenon within 20 s" both hold.
- **Colours.**
  - Three roles beyond L10's conventions, for this pilot: displacement BLUE, velocity GREEN, and the
    pull (force, acceleration) RED. They're the same in every chapter, because x, ẋ and ẍ are often
    on screen together.
  - L10's GREEN (principal value) never appears here. L10's RED (pitfalls) survives only as a ✗ on
    struck-through text, never as an arrow.
  - The old part 6 made the velocity arrow PURPLE. Here PURPLE has to stay the mirror arrow
    e^{−iωt} (ch2 s6, ch3 s2), so velocity moved to GREEN.
- **Notation.**
  - θ only for the pendulum's angle in ch1 s5–s7, renamed x in s8 as the notes do. Figure 24 labels
    the arrow's angle θ, and the notes call −π/3 "phase θ". We write those as ωt + arg A and arg A,
    so θ never means two things.
  - L for the notes' l.
  - λ for the trial exponent (k is the spring's).
  - ẍ for acceleration after one line of F = ma, since a and b are (81)'s.
  - α + iβ for A's parts while matching, the old plan's rename of the lecturer's c̃ + id̃. She had
    renamed c + id at 00:45:07, because c is also x(0).
  - F19: δ as in the old plan. The sheet's real A and ϕ are mapped once (the sheet's A = |A| = 25,
    ϕ = 3t − δ) and never used as our A.
  - "The period" in speech, T on screen.
- **Cross-references.** This pilot's videos are "part one" to "part four". The old L10 videos are
  named by topic ("the video on De Moivre's theorem", "the impedance video"), since "part two" would
  be ambiguous. The old part 7's hook ("Last time: d/dt becomes multiplication by iω") still holds
  after ch4.
- **Additions are tagged** (§1). ch1 is nearly all addition, so it carries one corner tag through
  s3–s7 instead of a tag per item, and s1 says so once. Elsewhere, tags go per item.
- **The student question** (00:56:12, a CST student: "is it okay that I didn't understand any of
  that physics stuff? … not done physics since GCSE"). ch1 builds every physical fact from GCSE ones
  (F = ma, Hooke, weight) and A-level trig. There are no lecture references in the narration, so
  the question isn't quoted.
- **Left out.** Nothing from §2.6, or from the oscillation part of scan p. 12.
  - Not in the material, so not added: damping, forcing, resonance, energy, and the exact
    large-angle period (only its numbers appear, as a caveat).
  - Example 32 and the circuit labels on scan p. 11 belong to the old part 7.
- **Source notes** (the notes and the scans win over the digest).
  - Figure 24: the red dot is the arrow's tip and the green dot its shadow on Re. The digest calls
    the shadow the red dot. Ours: arrow GOLD, shadow BLUE.
  - Figure 24's angle is labelled θ, and the notes call −π/3 "phase θ" (see Notation).
  - Scan p. 10's working reads "Re(A e^{iωt}) = c̃ cos ωt − d̃ sin ωt", with c̃ = a and −d̃ = b
    written underneath; the digest drops the tildes. Scan p. 10 is upside down in the PDF: rotate it
    180° when rendering.
  - The notes print ℜ; the lecturer writes Re, and so do we.
  - The digest's 00:44:34 example adds "= −ω Im(A)" to v(0). That's the digest's own (correct)
    gloss, not something on the page.
  - Transcript slips: "EI omega T" is e^{iωt}; "C plus ID" is c + id; "brings about I omega" is iω;
    "the frequency" (00:42:10) means angular frequency. 00:44:38's "easily find the integrals… We'll
    do it later" is the integrals remark (item 18).
- **Checked** (Python 3.11 with cmath, and sympy 1.14.0):
  - small angles: sin 0.1 = 0.0998; sin 10° = 0.1736 vs 0.1745 rad; sin 30° = 0.5 vs 0.5236;
    sin 60° = 0.866 vs 1.047;
  - pendulums (g = 9.81): 1 m gives ω = 3.1321 per second and T = 2.0061 s; 4 m gives T = 4.0121 s;
    the seconds pendulum is 0.9940 m;
  - the large-amplitude period ratio (by the AGM): 5° 1.0005, 10° 1.0019, 15° 1.0043, 20° 1.0077,
    30° 1.0174, 45° 1.0400, 60° 1.0732;
  - sympy:
    - d/dt e^{iωt} = iω e^{iωt}, and d/dt(cos ωt + i sin ωt) = iω(cos ωt + i sin ωt);
    - a cos ωt + b sin ωt obeys ẍ = −ω²x;
    - Re[(a − ib)e^{iωt}] = a cos ωt + b sin ωt, and Re[(α + iβ)(cos ωt + i sin ωt)] =
      α cos ωt − β sin ωt;
    - Re(−i e^{iωt}) = sin ωt, and ½(e^{iωt} + e^{−iωt}) = cos ωt;
    - Re[A e^{iωt}] = ½(A e^{iωt} + A* e^{−iωt});
    - x(0) = a and ẋ(0) = bω, so A = x₀ − iv₀/ω;
  - |A| cos(ωt + arg A) = a cos ωt + b sin ωt, for four (a, b) pairs;
  - the 3-4-5 swing: A = 3 − 4i, |A| = 5, arg A = −0.9273 rad (−53.13°); iωA = 12 + 9i and
    −ω²A = −27 + 36i; x(0) = 3, ẋ(0) = 12, ẍ(0) = −27;
  - the think stops: T3.1, A = 2i gives x(0) = 0, moving negative. T3.3, A = 2 and ω = 3 give
    iωA = 6i and ẋ(0) = 0;
  - the notes' example: A = c(1 − i√3) = 2c e^{−iπ/3}. x = 2c cos(ωt − π/3) has x(0) = c and
    ẋ(0) = √3cω. iωA has modulus 2cω and angle +30°;
  - F19:
    - |24 − 7i| = 25, and δ = 0.28379 rad (16.26°);
    - passages through the centre at t = 0.6182 and 1.6654 (the next is 2.7126);
    - stationary at t = 0.0946 (x = 32) and 1.1418 (x = −18);
    - x(0) = 31;
    - Re[(24 − 7i)e^{3it}] = 24 cos 3t + 7 sin 3t at four values of t;
  - integration: d/dt[A e^{iωt}/(iω)] = A e^{iωt}.
- **Cost and time**, for the producer: 4 scripts at ~3M tokens each, and 4 chapters at ~20–30M each
  to animate. ~45 min of wall time per chapter, plus the 1440p final renders, which take longer than
  1080p; previews are unchanged.
- **DEEP_STYLE.md points the pilot should settle:**
  1. §11's "≤ 1.5 new formulas a minute" can't hold inside an atomic worked example. ch4 s2, s3 and
     s5 run ~4–5 lines a minute, because §4 and the producer's ruling keep every step on screen.
     Here a worked example's lines are paced as reference and its moves as deep. The continuity
     review should count formulas per scene outside the examples.
  2. §1's per-item "beyond the notes" tag is noise when a whole chapter is addition (ch1), so ch1
     uses one corner tag instead.
  3. §9's retrieval opener assumes the previous chapter feeds this one. For the first chapter of a
     new topic, prerequisite retrieval stands in.
  4. §6 fills the corners all at once: the legend, the move card, a pinned formula, the think-stop
     ring and tags. The default layout gives each its own slot. Check a 1440p frame of ch1 s5, the
     busiest scene (diagram, split arrows, stack, legend, move card, corner tag).
