# Chapter 1 · From a picture to a formula

Vector algebra · From geometry to components (the cross product), part 1 of 1. Source: E. B. Wilson,
*Vector Analysis* (1901, from Gibbs's lectures), Arts. 31–35, pp. 60–66; history from Wikipedia
("Cross product", "History of quaternions", "Lorentz force") and Crowe via McGill; the
distributivity proof is ProofWiki, "Vector Cross Product Distributes over Addition", Proof 3.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card on {title}: "The Cross Product", course line "Vector algebra · From geometry to components", part line
> "From a picture to a formula" (no "Part 1": this is the only chapter); it clears on {arrows}.
> 3D, right-handed FG axes, z up, slow camera drift. {arrows}: **a** (BLUE) and **b** (YELLOW) grow from the
> origin; use the running example a = (3, 0, 0), b = (1, 2, 0) so s4 can reuse the shot, no coordinates yet.
> {area}: the parallelogram fills TEAL (low opacity). {rise}: a TEAL arrow grows out of it, straight up, with
> right-angle marks against a and b; fixed-in-frame label `\mathbf a\times\mathbf b`.
> {formula}: fixed in frame, right: `\mathbf a\times\mathbf b=(a_2b_3-a_3b_2,\ a_3b_1-a_1b_3,\ a_1b_2-a_2b_1)`
> (a's BLUE, b's YELLOW; it returns, derived, in s8). {shuffle}: its subscripts flash in turn. {why}: a YELLOW
> "?" above it. {bridge}: a curved arrow from the 3D picture to the formula, "?" on it. {derive}: under the
> formula, "memorise" struck through (RED), then "derive" (GREEN). No code on screen in this chapter; every
> number in it was checked with numpy 2.4.6 in the engine venv.

[c1.hook.1] {title} This is the story of a strange way to multiply two arrows. {arrows} Take two vectors in space, ay and bee, starting from the same point. {area} Together, they span a parallelogram. {rise} Their cross product, ay cross bee, is a third arrow, rising out of it at right angles to both.

[c1.hook.2] {formula} And here's the formula that most students are handed to memorise. {shuffle} It looks like a random shuffle of subscripts. {why} So why would anyone define a product like this? {pause} {bridge} And how does that picture turn into this formula? {derive} By the end of this video, you'll derive it yourself, instead of memorising it.

## Scene 2 · Hamilton's product, split in two (ch1_s2_history)

> 2D. A timeline along the bottom gains GOLD ticks as the story reaches them: 1843, 1844, 1873, 1880s, 1890s.
> {bridge}: "16 October 1843", caption "Brougham (Broom) Bridge, Royal Canal, Dublin", a stone-bridge
> silhouette. {hamilton}: "William Rowan Hamilton" (YELLOW). {carve}/{rule}: carved into the stone, stroke by stroke,
> `i^2=j^2=k^2=ijk=-1`.
> {quat}: `q=w+x\,\mathbf i+y\,\mathbf j+z\,\mathbf k`; {names} `w` boxed GOLD "scalar", the rest boxed TEAL
> "vector". {multiply}: `(a_1\mathbf i+a_2\mathbf j+a_3\mathbf k)(b_1\mathbf i+b_2\mathbf j+b_3\mathbf k)` (a's
> BLUE, b's YELLOW); {split} `=-\,\mathbf a\cdot\mathbf b+\mathbf a\times\mathbf b`, {dot} first part GOLD "a
> number", {cross} second part TEAL "a vector". (Checked with numpy 2.4.6 and a hand-written Hamilton product: pure quaternions (1, 2, 3) times (4, 5, 6) give
> −32 + (−3, 6, −3), and a·b = 32, a × b = (−3, 6, −3).)
> {grassmann}: 1844, "Hermann Grassmann", a parallelogram filling as an oriented patch, "a piece of plane".
> {maxwell}: 1873, a book, "Maxwell, A Treatise on Electricity and Magnetism". {gibbs}: 1880s, "J. Willard
> Gibbs, Yale" left; {heaviside} "Oliver Heaviside, England" right, DIM "independently" between. {apart}: the
> equation cracks at the plus; the bracket and minus sign fall away DIM; `\mathbf a\cdot\mathbf b` (GOLD) and
> `\mathbf a\times\mathbf b` (TEAL) fly apart, two separate products.
> {symbols}: the dot and the cross enlarge, "dot product", "cross product"; small caption from Gibbs–Wilson
> (1901): "It is written C = A × B and read A cross B. For this reason it is often called the cross product."
> {war}: 1890s, letter cards marked "Nature" fly between "quaternions" and "vectors". {won}: "vectors" turns
> GREEN, the other side dims. {why}: only `\mathbf a\times\mathbf b` (TEAL) stays, carried into s3.

[c1.hist.1] {bridge} The story starts in Dublin, on the sixteenth of October, eighteen forty-three. {hamilton} William Rowan Hamilton was walking along a canal when, after years of hunting, the rule finally came to him in a flash. {carve} He carved it into the stone of Broom Bridge. {rule} Eye squared, jay squared, kay squared, and eye jay kay, all equal minus one.

[c1.hist.2] {quat} His new numbers, quaternions, each have a number part and an arrow part. {names} Hamilton named them the scalar part and the vector part. {multiply} Now multiply two pure arrows. {split} The answer has both parts. {dot} In today's terms, its number part is minus ay dot bee, {cross} and its arrow part is ay cross bee.

[c1.hist.3] {grassmann} A year later, the German schoolteacher Hermann Grassmann multiplied two vectors into a piece of plane, the parallelogram itself. {maxwell} In eighteen seventy-three, Maxwell's great book on electricity and magnetism used Hamilton's language in places. {gibbs} Then in the eighteen eighties, Willard Gibbs at Yale, {heaviside} and Oliver Heaviside in England, each on his own, {apart} threw away the whole quaternion, and kept its two halves as separate products.

[c1.hist.4] {symbols} Gibbs wrote one with a dot and the other with a cross, and that's where the names come from. {war} In the eighteen nineties, the two camps fought it out in letters to the journal Nature. {won} The vectors won. {pause} {why} But why did physicists want the arrow half so badly?

## Scene 3 · Three laws, one pattern (ch1_s3_physics)

> Three panels in a row, each built on its mark; first factor BLUE, second YELLOW, product TEAL.
> {wrench}: a bolt and wrench in perspective; {push} position `\mathbf r` (BLUE) from the bolt along the
> handle, force `\mathbf F` (YELLOW) at the hand, angle θ. {part}: F splits into its part along the handle
> (DIM) and its part at right angles (YELLOW). {strength}: `|\mathbf r|\,|\mathbf F|\sin\theta` (GOLD).
> {axis}: a TEAL arrow along the bolt's axis. {torque}: `\boldsymbol\tau=\mathbf r\times\mathbf F`.
> {spin}: a ball circling on a string, `\mathbf r` (BLUE) from the centre, momentum `\mathbf p` (YELLOW) along
> the path; {momentum} a TEAL arrow along the circle's axis, `\mathbf L=\mathbf r\times\mathbf p`.
> {magnet}: field arrows `\mathbf B` (YELLOW), a charge q with velocity `\mathbf v` (BLUE), a TEAL force at
> right angles to both, `\mathbf F=q\,\mathbf v\times\mathbf B`. {along}: v turns to lie along B and the force
> shrinks to "0" (GOLD).
> {strip}: bolt, ball and field fade; the three arrow-triples merge into one picture: {two} **a** (BLUE),
> **b** (YELLOW), θ; {size} `|\mathbf a|\,|\mathbf b|\sin\theta` (GOLD); {dir} a TEAL arrow at right angles
> to both. {defn}: "That pattern is the definition." (YELLOW). This picture leads into s4.

[c1.phys.1] {wrench} Take a wrench on a bolt. {push} You push on the handle at some distance from the bolt, with some force. {part} Only the part of the force at right angles to the handle turns it. {strength} So the turning strength is the distance, times the force, times the sine of the angle between them. {axis} And the bolt moves along its own axis, at right angles to both. {torque} That's the torque, the position cross the force.

[c1.phys.2] {spin} Now swing a ball on a string. {momentum} Its angular momentum, the position cross the momentum, points along the axis of the circle. {magnet} And a charge moving through a magnetic field feels a force at right angles to both its velocity and the field. {along} Move it along the field, and that force is zero.

[c1.phys.3] {strip} Strip away the physics, and all three pictures are the same. {two} Two arrows. {size} A strength, the two lengths times the sine of the angle. {dir} And a direction, at right angles to both. {pause} {defn} That pattern is the definition.

## Scene 4 · Length is area, direction is the right hand (ch1_s4_define)

> {axes}: 3D, right-handed FG axes, z up; this camera is kept for s5 and for s8's check. Numbers GOLD.
> {a}: `\mathbf a=(3,0,0)` (BLUE); {b} `\mathbf b=(1,2,0)` (YELLOW); {floor} a faint floor grid, θ arc a → b.
> {len}: fixed in frame, `|\mathbf a\times\mathbf b|=|\mathbf a|\,|\mathbf b|\sin\theta`; {range} below it,
> `0^\circ\le\theta\le180^\circ`, then `\sin\theta\ge0`.
> {height}: a dashed drop from (1, 2, 0) to (1, 0, 0), right-angle mark; {h} label `|\mathbf b|\sin\theta`;
> {area} the parallelogram 0, a, a + b, b fills TEAL; {six} "base 3", "height 2", "area 6".
> {dir}: two DIM candidate arrows, up and down. {hand}: a schematic right hand: {fingers} along a, {curl}
> curling toward b, {thumb} thumb up; the down candidate fades. {ccw}: a counterclockwise arrow from a to b in
> the floor.
> {rise}: the TEAL area lifts off and becomes the arrow (0, 0, 6) (TransformFromCopy), label
> `\mathbf a\times\mathbf b=(0,0,6)`. {conv}: DIM tag "right-handed" on the axes. {vec}: side by side,
> `\mathbf a\cdot\mathbf b=3` (GOLD, "a number") and `\mathbf a\times\mathbf b=(0,0,6)` (TEAL, "a vector").
> Checked (numpy 2.4.6): np.cross([3,0,0],[1,2,0]) → `[0 0 6]`; a·b = 3; |a||b| sin θ = 6.0.

[c1.def.1] {axes} Let's make it exact, with a running example. {a} Take ay equal to three, zero, zero, {b} and bee equal to one, two, zero. {floor} Both lie flat in the floor. {len} The length of ay cross bee is the length of ay, times the length of bee, times sine theta, where theta is the angle between them.

[c1.def.2] {range} Theta runs from zero to a hundred and eighty degrees, so its sine is zero or positive, and so is the length. {height} Now drop a line from the tip of bee straight down to ay, meeting it at a right angle. {h} This height is the length of bee times sine theta. {area} So ay cross bee is as long as the base times the height, which is the area of the parallelogram. {six} Here the base is three, the height is two, and the area is six.

[c1.def.3] {dir} Now the direction. {two} At right angles to the floor, there are two choices, up or down. {hand} The right-hand rule picks one. {fingers} Point the fingers of your right hand along ay, {curl} curl them toward bee, {thumb} and your thumb gives the direction. {ccw} Put another way, seen from the tip of ay cross bee, ay turns toward bee counterclockwise.

[c1.def.4] {rise} So ay cross bee is the arrow zero, zero, six. {pause} The area has become an arrow. {conv} The right hand is a convention, the same one that makes the axes right-handed. {vec} And unlike ay dot bee, which is a number, ay cross bee is a vector.

## Scene 5 · What the picture gives for free (ch1_s5_rules)

> s4's axes, camera and end state.
> {order}: the label becomes `\mathbf b\times\mathbf a`; {same} the parallelogram flashes; {flip} the curl
> reverses and the TEAL arrow swings down; {neg} `\mathbf b\times\mathbf a=-\,\mathbf a\times\mathbf b`, {ex}
> `(0,0,-6)` (checked, numpy 2.4.6: np.cross([1,2,0],[3,0,0]) → `[ 0  0 -6]`).
> {self}: b swings onto a; {flat} the parallelogram squashes to a segment, "area 0",
> `\mathbf a\times\mathbf a=\mathbf 0`. {par}: b slides to (−2, 0, 0), still flat, still zero.
> {unit}: clear to **i**, **j**, **k** (FG). {square}: the unit square fills TEAL, "area 1", k flashes,
> `\mathbf i\times\mathbf j=\mathbf k`. {wheel}: a cyclic wheel i → j → k → i, then
> `\mathbf j\times\mathbf k=\mathbf i`, `\mathbf k\times\mathbf i=\mathbf j`; {against} the wheel reversed, a
> RED minus. These fill a 3 × 3 table (rows i, j, k times columns i, j, k): 0, k, −j / −k, 0, i / j, −i, 0;
> {diag} the diagonal 0s DIM (checked with np.cross). The table parks in a corner, kept for s8.
> {left}: `(\mathbf i\times\mathbf i)\times\mathbf j=\mathbf 0\times\mathbf j=\mathbf 0`; {right}
> `\mathbf i\times(\mathbf i\times\mathbf j)=\mathbf i\times\mathbf k=-\mathbf j`; {brackets} a RED ≠ between
> them, the brackets glow YELLOW.

[c1.rules.1] {swap} The picture hands us the rules for free. {order} Swap the order, to get bee cross ay. {same} The parallelogram is the same, so the length is the same. {flip} But now your fingers curl the other way, and your thumb points down. {neg} So bee cross ay is minus ay cross bee. {ex} In our example, zero, zero, minus six.

[c1.rules.2] {self} What is ay cross ay? {pause} {flat} The parallelogram is squashed flat, its area is zero, so ay cross ay is the zero vector. {par} In fact, the cross product is zero exactly when the two arrows are parallel, or one of them is zero.

[c1.rules.3] {unit} Now the unit arrows, eye, jay and kay. {square} Eye and jay span a square of area one, and the right hand points up, so eye cross jay is kay. {wheel} Going round the wheel, jay cross kay is eye, and kay cross eye is jay. {against} Going against the wheel gives a minus sign. {diag} And each one crossed with itself is zero.

[c1.rules.4] {warn} One warning. {left} Cross eye with eye first, and you get zero, so crossing that with jay still gives zero. {right} Now cross eye with jay first, to get kay. Then eye cross kay is minus jay. {brackets} Same three arrows, different answers. So with cross products, the brackets matter.

## Scene 6 · Does it distribute? (ch1_s6_machine)

> Opens on s4's axes: a (BLUE), b (YELLOW), a × b = (0, 0, 6) (TEAL).
> {question}: fixed at the top, `\mathbf a\times(\mathbf b+\mathbf c)\overset{?}{=}\mathbf a\times\mathbf b+\mathbf a\times\mathbf c`
> (c PINK, b + c GREEN, "?" YELLOW); {matters} DIM below, "multiply out brackets → components".
> {hard}: RED notes, {lengths} `|\mathbf b+\mathbf c|\ne|\mathbf b|+|\mathbf c|`, {angle} "the angle to a
> changes", {sines} the recipe `|\mathbf a|\,|\mathbf b|\sin\theta` + a right-hand icon, a RED "+ ?" beside it
> (nothing in the recipe mentions sums; don't show sin(α+β): the new angle is not a sum of angles). {plan}: the notes clear; a box "a × ( )",
> b goes in, a × b comes out.
> {split}: from b come {par} `\mathbf b_\parallel` along a (DIM) and {perp} `\mathbf b_\perp` (YELLOW), a right triangle;
> {tri} `|\mathbf b_\perp|=|\mathbf b|\sin\theta`; {same} the parallelogram on a, b shears into the rectangle on
> a, b⊥ (same base, same height, same plane; the TEAL arrow doesn't move), then `\mathbf a\times\mathbf b=\mathbf a\times\mathbf b_\perp`;
> {drop} b∥ fades.
> {turn}: the camera moves so a points straight up (the "a up" view, kept for s7). {plane}: a floor grid at
> right angles to a. {shadow}: a light directly above; b's shadow falls, exactly b⊥. {lies}: a × b (TEAL)
> lies in the floor, right-angle mark against the shadow; {long} `|\mathbf a|\,|\mathbf b_\perp|`.
> {three}: fixed at the top, the strip "project" → "rotate 90°" → "scale by |a|" (kept for s7), each box
> lighting on its word: {project} the shadow drops, {rotate} a quarter turn counterclockwise seen from above,
> {scale} a stretch into the TEAL arrow. Under it, `\mathbf a\times\mathbf b=|\mathbf a|\,R(\mathbf b_\perp)`.
> {run}: GOLD, {p} `(1,2,0)\to(0,2,0)`, {r} `\to(0,0,2)`, {s} `\to(0,0,6)`, landing on s4's arrow (flash).
> Checked (numpy 2.4.6): b∥ = (1, 0, 0), b⊥ = (0, 2, 0), turned (0, 0, 2), times 3 = np.cross([3,0,0],[1,2,0]) = `[0 0 6]`.
> {point}: a (generic) b swings onto a's line; its shadow shrinks to a dot at the origin, the output to "0" (GOLD).
> This closes the one case the right-triangle split skips, so the machine formula holds for every b (s7 needs that).

[c1.mach.1] {ask} So far, the picture has given us every rule. {question} Here's the big one. Is ay, crossed with the sum of bee and vector see, equal to ay cross bee, plus ay cross vector see? {pause} {matters} That rule is what lets you multiply out brackets, and that's how you compute with components.

[c1.mach.2] {hard} And it's far from obvious. {lengths} The sum, bee plus see, has a different length, {angle} and a different angle to ay, {sines} and the recipe of lengths, sines and a right hand says nothing at all about sums. {plan} So here's a better plan. Fix ay, and think of crossing with ay as a machine. Bee goes in, and ay cross bee comes out.

[c1.mach.3] {split} Split bee into two parts, {par} one along ay, {perp} and one at right angles to it. {tri} In this right triangle, the perpendicular part is opposite theta, so its length is the length of bee times sine theta. {same} That's the height from before. So crossing ay with this part alone gives a rectangle with the same base and height, in the same plane, turning the same way. In other words, ay cross bee equals ay cross the perpendicular part. {drop} The part along ay adds nothing.

[c1.mach.4] {turn} Now turn the view, so that ay points straight up. {plane} The plane at right angles to ay becomes the floor. {shadow} And the perpendicular part of bee is simply bee's shadow, under a light directly above. {lies} The product, ay cross bee, meets ay at right angles, so it lies in this floor too, at right angles to the shadow, {long} and its length is the length of ay times the length of the shadow.

[c1.mach.5] {three} So the machine has three steps. {project} Project bee onto the floor. {rotate} Turn the shadow a quarter turn, counterclockwise seen from above, as the right hand says. {scale} Then scale it by the length of ay. {run} Let's run our example through. {p} One, two, zero has the shadow zero, two, zero. {r} The quarter turn makes it zero, zero, two. {s} Scaling by three gives zero, zero, six, our arrow from before. {point} And if bee lies along ay, its shadow is a single point, so the machine gives zero, just as it should. {pause}

## Scene 7 · Every step keeps sums (ch1_s7_linear)

> s6's "a up" view, a (BLUE) vertical; s6's strip at the top, boxes unticked.
> {bc}: b (YELLOW), c (PINK), b + c (GREEN) above the floor, dashed parallelogram. In s4's coordinates
> (a = (3, 0, 0) is "up"): b = (1, 2, 0), c = (1, 1, 2), b + c = (2, 3, 2).
> {proj}: three shadows drop, colours kept: (0, 2, 0), (0, 1, 2), (0, 3, 2); {sum} the GREEN one glows as
> the shadow parallelogram's diagonal; "project" ticks GREEN. {rot}: the floor picture turns a quarter turn
> counterclockwise as one piece: (0, 0, 2), (0, −2, 1), (0, −2, 3); tick. {stretch}: times 3 about the
> origin: (0, 0, 6), (0, −6, 3), (0, −6, 9); tick.
> {sides}: labels `\mathbf a\times\mathbf b`, `\mathbf a\times\mathbf c`; {diag}
> `\mathbf a\times(\mathbf b+\mathbf c)`. {eq}: s6's "?" drops out; the equation is boxed GREEN. Checked (numpy 2.4.6):
> np.cross([3,0,0],[2,3,2]) → `[ 0 -6  9]` = `[0 0 6]` + `[ 0 -6  3]`.
> {t}: a GOLD slider t on b (2, then −1); every stage stretches with it, flipping for t < 0;
> `\mathbf a\times(t\,\mathbf b)=t\,(\mathbf a\times\mathbf b)` (t = 2 gives (0, 0, 12), t = −1 gives (0, 0, −6)).
> {lin}: "linear" (YELLOW), "keeps sums and multiples"; {chain} one bracket under the three ticked boxes.
> {first}: a 2D card, each line born from the one above ({borrow} for the middle two, {result} the last): `(\mathbf b+\mathbf c)\times\mathbf a` /
> `=-\,\mathbf a\times(\mathbf b+\mathbf c)` / `=-\,\mathbf a\times\mathbf b-\mathbf a\times\mathbf c` /
> `=\mathbf b\times\mathbf a+\mathbf c\times\mathbf a`, the swaps tagged DIM "swap: minus sign". On "Multiples come out",
> a DIM line under the card: `(t\,\mathbf b)\times\mathbf a=t\,(\mathbf b\times\mathbf a)` (s8's expansion needs scalars in both slots).
> {conclude}: "Multiply out brackets as usual, keeping the order." (GREEN).

[c1.lin.1] {feed} Now feed the machine a sum. {bc} Here are bee, vector see, and their sum, the diagonal of the parallelogram they span. {proj} Step one, project. The shadow of a parallelogram is a parallelogram, {sum} so the shadow of the sum is the sum of the shadows.

[c1.lin.2] {rot} Step two, rotate. Turn the whole floor picture a quarter turn, and the parallelogram is still a parallelogram. {stretch} Step three, scale it by the length of ay. Still a parallelogram. {read} Now read off the result. {sides} Its sides are ay cross bee, and ay cross see. {diag} Its diagonal is ay cross the sum. {eq} So ay cross, bee plus see, equals ay cross bee, plus ay cross see. {pause=1.5}

[c1.lin.3] {scalar} Each step also respects stretching. {t} Stretch bee by any number, and every step stretches its output by the same number, flipping it if the number is negative. {lin} A map that keeps sums and multiples like this is called linear. {chain} And a chain of linear steps is linear too.

[c1.lin.4] {first} What about the first slot? {borrow} Swap the order, which costs a minus sign. Use the rule we just proved. Then swap back. {result} So bee plus see, all crossed with ay, is bee cross ay, plus vector see cross ay. Multiples come out of the first slot the same way. {conclude} The upshot is that you can multiply out brackets just as in ordinary algebra, as long as you keep the order in every product.

## Scene 8 · Nine products, three vanish, six pair up (ch1_s8_components)

> 2D. {write}: `\mathbf a=a_1\mathbf i+a_2\mathbf j+a_3\mathbf k` (BLUE components, FG i, j, k); {b}
> `\mathbf b=b_1\mathbf i+b_2\mathbf j+b_3\mathbf k` (YELLOW components).
> {expand}/{grid}: a's terms down the left, b's across the top, nine cells like `a_1b_2\,(\mathbf i\times\mathbf j)`.
> {table}: s5's table slides in; each cell's cross product becomes its entry (TransformFromCopy).
> {diag}: diagonal cells become 0, DIM. {pair}: arcs join mirror cells; {k} `a_1b_2\,\mathbf k` and {kminus}
> `-a_2b_1\,\mathbf k` merge into {kcomp} `(a_1b_2-a_2b_1)\,\mathbf k`; {others}
> `(a_2b_3-a_3b_2)\,\mathbf i`, `(a_3b_1-a_1b_3)\,\mathbf j`.
> {result}: `\mathbf a\times\mathbf b=(a_2b_3-a_3b_2)\,\mathbf i+(a_3b_1-a_1b_3)\,\mathbf j+(a_1b_2-a_2b_1)\,\mathbf k`;
> the hook's tuple returns and matches term by term (GREEN ticks). {pattern}: a wheel 1 → 2 → 3; the index
> pairs (2, 3), (3, 1), (1, 2) light in turn.
> {six}: `(3,0,0)\times(1,2,0)=(0,0,6)` with an inset of s4's arrow; {test} `(1,2,3)\times(4,5,6)=(-3,6,-3)`;
> {perp} both dot products `=0`, GREEN. Checked (numpy 2.4.6): np.cross → `[0 0 6]`, `[-3  6 -3]`; dots 0 and 0.
> {recap}: six short lines on {r1} … {r6}, each with a tiny icon (split equation, wrench, TEAL
> parallelogram, flipped arrow, three-box strip, grid).
> {next}: 3D, a (BLUE), b (YELLOW), c (PINK) span a slanted box (TEAL faces, low opacity); {triple}
> `\mathbf a\cdot(\mathbf b\times\mathbf c)`, b × c rising from the base; {box} "= volume (up to sign)"; {det}
> `=\det\begin{pmatrix}a_1&a_2&a_3\\b_1&b_2&b_3\\c_1&c_2&c_3\end{pmatrix}` (checked: (3, 0, 0), (1, 2, 0),
> (1, 1, 2), the same c as s7, give 12 both ways). End card: hold ~8 s after the last word, music carries it.

[c1.comp.1] {write} Now the payoff. Write ay as ay one eye, plus ay two jay, plus ay three kay, {b} and bee the same way. {expand} Multiply out the brackets, keeping the order. {grid} Every term of ay meets every term of bee, giving nine products in a three by three grid. {table} Each one is two numbers times a cross product of two unit arrows, and we already have the table for those.

[c1.comp.2] {diag} The three on the diagonal cross a unit arrow with itself, so they vanish. {pair} The other six pair up across the diagonal. {k} First, ay one times bee two, with eye cross jay, gives plus kay. {kminus} Next, ay two times bee one, with jay cross eye, gives minus kay. {kcomp} So the kay component is ay one times bee two, minus ay two times bee one. {others} The other two pairs give the eye and jay components the same way.

[c1.comp.3] {result} And there it is, the formula from the start, now derived. {pattern} Each component uses the other two indices, in cyclic order. {six} Check it on our example. Three, zero, zero, cross one, two, zero, gives zero, zero, six, just as the picture said. {test} And one, two, three, cross four, five, six, gives minus three, six, minus three. {perp} Its dot product with each factor is zero, so it really is at right angles to both. {pause}

[c1.comp.4] {recap} Let's recap. {r1} Hamilton's product held two products, and Gibbs and Heaviside split them apart. {r2} Torque, angular momentum and magnetic force share one pattern. {r3} The length of ay cross bee is the parallelogram's area, and the right hand gives its direction. {r4} Swapping the order flips the sign, and ay cross ay is zero. {r5} Project, rotate, scale, three linear steps, make it distribute over sums. {r6} And multiplying out gives the components.

[c1.comp.5] {next} So where does this lead? {triple} Bring in a third vector, vector see, and dot ay with bee cross see. {box} You get the volume of the slanted box the three of them span, up to a sign. {det} That volume is a determinant, which is why determinants keep turning up around the cross product. {pause}
