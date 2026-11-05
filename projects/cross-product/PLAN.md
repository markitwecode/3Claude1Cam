# The Cross Product: plan

Request: "can you create a short video going from why the vector product was created and what it
means geometrically to distributivity to the components form" (2026-10-25). Audience: someone
studying vectors (late school, or first-year linear algebra, physics or multivariable calculus).
They know 3D vectors as arrows and as components along **i**, **j**, **k**, addition (tip to tail,
the parallelogram rule), scalar multiples, length, the dot product with its cos θ, and
"base × height". They don't need quaternions or the word "linear" beforehand. Sources (no
material given, researched): Wilson's *Vector Analysis* (1901, from Gibbs's lectures), Arts.
31–35 (`source/gibbs-wilson-1901-arts31-35.txt`), for the definition, rules, **i**/**j**/**k**
table and expansion. The history comes from Wikipedia ("Cross product", "History of quaternions",
"Lorentz force") and a short history after Crowe. The projection proof is ProofWiki's "Vector
Cross Product Distributes over Addition", Proof 3. All of them, with URLs, are in project.json.
Total: 1 chapter, ~11 min of narration (~1750 words).

## Chapter 1 · From a picture to a formula
Slug: ch1_cross_product · ~11 min · Source: Gibbs–Wilson Arts. 31–35; the history and proof sources in project.json
Goal: explain why the cross product exists, state its geometric definition and rules, prove that
it distributes over addition by "project, rotate, scale", and derive the component formula by
multiplying out.
Scenes:
- s1_hook · Hook (~45 s): title card ("The Cross Product", the course line, part line
  "From a picture to a formula"). Then **a** and **b** from one point in 3D, the parallelogram
  between them, and a third arrow rising perpendicular to both. Beside it is the formula most
  students are handed to memorise: (a₂b₃ − a₃b₂, a₃b₁ − a₁b₃, a₁b₂ − a₂b₁). The question is
  "why would anyone define a product like this, and how does this picture turn into that formula?"
  The promise: by the end you'll derive it, not memorise it.
- s2_history · Hamilton's product, split in two (~75 s): a timeline along the bottom (GOLD
  dates), with these beats:
  - 16 October 1843: Hamilton, crossing Brougham Bridge in Dublin, carves
    i² = j² = k² = ijk = −1.
  - A quaternion is a number part plus an arrow part. Hamilton named them "scalar" and "vector".
  - Multiplying two pure arrows, (a₁i + a₂j + a₃k)(b₁i + b₂j + b₃k), gives −**a**·**b** (GOLD,
    a number) + **a**×**b** (TEAL, a vector), checked numerically.
  - 1844: Grassmann, independently, multiplies two vectors into an oriented piece of plane, the
    parallelogram itself.
  - 1873: Maxwell's *Treatise* writes electromagnetism partly in quaternion language.
  - The 1880s: Gibbs (Yale, notes printed for his students 1881–84) and Heaviside (England),
    working independently, throw away the whole quaternion and keep its two halves as separate
    products. The equation splits; its halves fly apart into **a**·**b** and **a**×**b**.
  - The names come from Gibbs's symbols, the dot and the cross (Wilson's 1901 textbook). One
    sentence on the 1890s "quaternion war" letters in *Nature*: vectors won.
- s3_physics · Three laws, one pattern (~65 s): why physicists wanted the vector half. First
  factor BLUE, second YELLOW, product TEAL, here and in every later scene.
  - Wrench: force **F** at position **r** from the bolt. Only F's part perpendicular to **r**
    turns it, so the strength is |r||F| sin θ, and the bolt moves along the axis perpendicular
    to both: **τ** = **r**×**F**.
  - Angular momentum, **L** = **r**×**p**: a ball on a string, with its axis perpendicular to
    the orbit's plane.
  - The magnetic force on a moving charge, **F** = q **v**×**B**: perpendicular to both **v**
    and **B**, zero when moving along the field.
  - The three diagrams strip down to one picture: two arrows, strength |a||b| sin θ, direction
    perpendicular to both. "That pattern is the definition."
- s4_define · Length is area, direction is the right hand (~85 s):
  - Right-handed 3D axes, z up. Running example **a** = (3, 0, 0), **b** = (1, 2, 0), lying in
    the floor.
  - |**a**×**b**| = |a||b| sin θ, with θ between 0° and 180°, so it is never negative. Drop the
    height from b's tip: height = |b| sin θ, so the length is base × height, the parallelogram's
    area (TEAL fill). Here base 3, height 2, area 6.
  - Direction: two candidates perpendicular to the floor, up and down. The right-hand rule picks
    one: fingers along **a**, curl toward **b**, thumb. Equivalently, seen from the tip, **a**
    turns to **b** counterclockwise.
  - So **a**×**b** = (0, 0, 6). The area turns into the arrow, which rises out of the
    parallelogram.
  - Close with two sentences. The rule is a convention, the same one that makes the axes
    right-handed. And **a**×**b** is a vector, where **a**·**b** is a number.
- s5_rules · What the picture gives for free (~70 s), on s4's axes:
  - Swap the order: same parallelogram, but the curl reverses and the thumb flips, so
    **b**×**a** = −**a**×**b** (example (0, 0, −6)).
  - **a**×**a** = **0**: the parallelogram is flat. More generally **a**×**b** = **0** exactly
    when they are parallel (or one is zero).
  - The basis table: **i**×**j** = **k** (unit square, area 1, right hand), then
    **j**×**k** = **i** and **k**×**i** = **j** around a cyclic wheel i → j → k. Against the
    wheel gives minus. **i**×**i** = **j**×**j** = **k**×**k** = **0**. Keep the 3×3 table
    as an object; it returns in s8.
  - Pitfall: there is no associativity. (**i**×**i**)×**j** = **0**, but
    **i**×(**i**×**j**) = **i**×**k** = −**j**.
- s6_machine · Does it distribute? (~110 s): the visual heart, part 1.
  - Ask: is **a**×(**b**+**c**) = **a**×**b** + **a**×**c**? {pause}. Why that's not obvious:
    |b+c| ≠ |b| + |c|, the angle to **a** changes, and sines don't add. Why it matters:
    distributivity is what lets you multiply out brackets, i.e. compute from components.
  - Strategy: fix **a** and treat b ↦ **a**×**b** as a machine. Split **b** = b∥ (along
    **a**, DIM) + b⊥ (perpendicular, YELLOW). In the right triangle |b⊥| = |b| sin θ, so
    **a**×**b** = **a**×b⊥: the part along **a** contributes nothing.
  - Turn the view so **a** points straight up (or straight at the viewer). The plane
    perpendicular to **a** becomes the floor, and b⊥ is b's shadow under a light directly above.
    **a**×**b** lies in that plane, perpendicular to b⊥, with length |a||b⊥|. So it is b⊥
    turned a quarter turn (counterclockwise seen from a's tip), then stretched by |a|:
    **a**×**b** = |a| R(b⊥).
  - A three-box strip, fixed in frame at the top: project → rotate 90° → scale by |a|.
  - The running example goes through it: (1, 2, 0) → (0, 2, 0) → (0, 0, 2) → (0, 0, 6), the
    s4 arrow. Optional line: if **b** is parallel to **a**, its shadow is a point and the
    machine gives zero, as s5 said.
- s7_linear · Every step keeps sums (~95 s): the visual heart, part 2.
  - **a** vertical. **b** (YELLOW), **c** (PINK) and **b**+**c** (GREEN) form a parallelogram
    above the floor.
  - Shadows drop: the shadow is a parallelogram, so the shadow of the sum is the sum of the
    shadows. Turn the whole floor picture a quarter turn: still a parallelogram. Stretch by
    |a|: still one. Colours follow their inputs. As each step is shown, its box in s6's strip
    ticks GREEN.
  - Read off: sides **a**×**b** and **a**×**c**, diagonal **a**×(**b**+**c**), so
    **a**×(**b**+**c**) = **a**×**b** + **a**×**c**. Likewise **a**×(t**b**) = t(**a**×**b**),
    because each step also respects stretching (t < 0 flips).
  - Name it: a map that keeps sums and multiples is *linear*, and a chain of linear steps is
    linear.
  - The first slot borrows from s5: (**b**+**c**)×**a** = −**a**×(**b**+**c**) =
    −**a**×**b** − **a**×**c** = **b**×**a** + **c**×**a**.
  - Conclusion: you may multiply out brackets as in ordinary algebra, keeping the order.
- s8_components · Nine products, three vanish, six pair up (~120 s + ~8 s end card):
  - **a** = a₁**i** + a₂**j** + a₃**k**, likewise **b**. Components are BLUE for **a** and
    YELLOW for **b**.
  - Multiplying out gives a 3×3 grid of nine terms aₘbₙ(**e**ₘ×**e**ₙ). Bring back s5's table.
    The diagonal three vanish (dim them). The six others pair up across the diagonal, e.g.
    a₁b₂ **i**×**j** + a₂b₁ **j**×**i** = (a₁b₂ − a₂b₁)**k**.
  - Result: (a₂b₃ − a₃b₂)**i** + (a₃b₁ − a₁b₃)**j** + (a₁b₂ − a₂b₁)**k**, the hook's formula,
    now derived. Pattern: each component uses the other two indices, in cyclic order.
  - Checks: the running example gives (0, 0, 6). Then (1, 2, 3)×(4, 5, 6) = (−3, 6, −3), and its
    dot product with each factor is 0, so it is perpendicular. Both were checked with numpy.
  - Optional, one sentence each if words allow: the determinant layout as a memory aid, and
    Lagrange writing this formula in 1773, before anyone drew the arrow.
  - Recap, one sentence per idea: Hamilton's product split by Gibbs and Heaviside; the physics
    pattern; length = area and the right hand; swapping flips the sign, **a**×**a** = **0**;
    project, rotate, scale makes it distributive; the components follow by multiplying out.
  - "Where next": **a**·(**b**×**c**) is the volume of the slanted box, which is why a
    determinant appears. Phrase it as where the idea leads, without promising another video.
  - End card.
Continuity:
- One chapter, so no "last time". The hook's formula comes back, derived, in s8. The running
  example **a** = (3, 0, 0), **b** = (1, 2, 0) → (0, 0, 6) appears in s4 (picture), s5
  (swapped: (0, 0, −6)), s6 (through the machine) and s8 (formula).
- The **i**/**j**/**k** table is built in s5 and reused in s8. The project → rotate → scale
  strip is built in s6 and ticked off in s7.
- Notation on screen: bold **a**, **b**, **c**, **i**, **j**, **k** (MathTex `\mathbf`);
  b∥ and b⊥ (`b_\parallel`, `b_\perp`); R; θ.
- Colours: first factor BLUE, second YELLOW, product and area TEAL, the third vector **c**
  PINK, **b**+**c** GREEN, discarded parts DIM, dates and scalars GOLD, axes and **i**,
  **j**, **k** in FG.
- Spoken forms (TTS garbles bare letters): "ay", "bee", "see" (say "vector see" where "see" could
  be misheard); "ay cross bee"; "eye, jay, kay"; "ay one, ay two, ay three"; "sine theta";
  "the perpendicular part of bee" rather than "bee perp".
- 3D scenes: `class X(NarratedScene, ThreeDScene)`, with labels and the strip via
  `add_fixed_in_frame_mobjects`. A test render with the engine's ManimCE worked (2026-10-25).
  Keep one camera angle for s4, s5 and s8's checks, and the "a points up" view for s6 and s7.

## Decisions
- **One chapter of ~11 min, 8 scenes.** The user said "short" and the producer asked for one
  chapter. The arc fits at the top of the 8–11 min range only with tight scenes:
  - history and physics get ~2.3 min;
  - the definition and rules get ~2.6 min;
  - the proof (s6 + s7) gets ~3.4 min, about 30% of the video, as asked;
  - the components and recap get ~2 min.

  If the user would rather go calmer, the natural split is two ~8 min chapters: s1–s5 plus a
  recap ("why and what"), then s6–s8 ("distributivity and components").
- **Order** follows the producer's arc, with two moves.
  - The **i**/**j**/**k** table sits in s5, where it falls straight out of the picture. That
    leaves s8 room for the expansion and the recap, and the table comes back on screen there.
  - The scalar rule (t**a**)×**b** = t(**a**×**b**) moves to s7, because the machine proves it
    along with sums.
- **Geometry first, formula derived**, as in Gibbs–Wilson (Arts. 31–35) and as requested. Many
  calculus courses (e.g. MIT 18.02) define it by the determinant first. Here the determinant is
  at most a one-line memory aid.
- **The proof** is the producer's projection–rotation proof (ProofWiki, Proof 3). Gibbs–Wilson's
  own proof (a prism whose face areas sum to zero) is left out, since it needs vector areas of
  closed surfaces. The history scene must not claim Gibbs used our proof.
- **History accuracy.** Gibbs and Heaviside worked independently. Gibbs's notes were printed
  privately, in 1881 and 1884. "Cross product" comes from his symbol, and Wilson (1901) says
  "vector product" was then more common. The quaternion's scalar part is *minus* the dot
  product. Clifford (who named "vector product" in 1878) and Lagrange's 1773 component formula
  are optional one-liners.
- **Left out, as beyond the requested arc:** the Jacobi identity, the triple vector product
  (BAC−CAB), Lagrange's identity |a×b|² = |a|²|b|² − (a·b)², pseudovectors and mirror
  reflection, the 7D cross product, the matrix [a]×, and 3Blue1Brown's duality derivation. The
  triple product is the closing pointer.
- **No exercises** (there is no material). The worked example in s8 doubles as practice.
- **No code on screen.** `code_language` is "", and numpy is only for checking arithmetic.
  Six of the eight scenes are 3D and will render slower than the 2D FoCS scenes.
