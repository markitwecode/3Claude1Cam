# Chapter 1 · The rule behind every swing

NST IA Mathematics · Lecture 10 (Oscillations, deep-style pilot), part 1 of 4. Source: notes `Chapter234_to_annotate.pdf`, PDF p. 27 (printed p. 108: the §2.6 opening, the pendulum paragraph, ω = √(g/l)); Lecture 10 scan p. 10 (the margin pendulum sketch, scanned upside down); recording 00:41:45–00:42:58. Nearly all of this part is beyond the notes (DEEP_STYLE §12: one corner tag, s3–s7).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch1_s1_hook)

> Board for the whole chapter (PLAN.md "The board"): picture centre-left (~55% of the width), derivation in a right-hand column, legend panel bottom-left, move card top-right, the "beyond the notes" corner tag top-left (s3–s7), the think-stop ring bottom-right. Colours: x and the bob/weight BLUE, velocity GREEN, every pull and acceleration RED, angles YELLOW, constants (k, m, g, L, ω) and gravity's full arrow FG, the rod's along-rod part DIM.
> {swing}: from the first frame, the phenomenon. Centre-left, the 1 m pendulum (s5's drawing: hatched FG ceiling, FG rod, BLUE bob) swings at about ±12°. Centre-right, the weight on a spring (s3's drawing: wall, FG coil, BLUE block on a DIM table line) oscillates in step with it: both at ω = 3.13 per second (√9.81, checked). A small FG seconds counter sits top-centre. {second}: each time the pendulum reaches an end, the counter ticks over: about one second each way (period 2.006 s, checked in Python 3.11.9).
> {twins}: the spring fades out. A second, identical pendulum joins the first; one swings at 15°, the other at 5°, each with a small YELLOW angle readout under it. {lag}: a DIM "?" over the wide one. {beat}: they keep the same beat. Animate both with the same ω (the small-angle rule); real pendulums at 15° and 5° differ by only 0.4% per swing (exact period ratios 1.0043 and 1.0005, checked with the AGM formula in Python 3.11.9), so this is honest. Keep them swinging under everything that follows in this scene.
> {question}: over the pendulums, two YELLOW lines: "What rule makes it swing?" and "What sets the beat?"
> {title}: the title card over the still-swinging pendulums: "Oscillations", "NST IA Mathematics · Lecture 10", "Part 1 · The rule behind every swing". It clears on {things}.
> {things}: along the bottom, three small DIM icons with their words: a pendulum ("pendulums"), a circle with `\sim` inside ("alternating currents"), a water wave ("waves"); a DIM "reference" tag and a DIM tag "§2.6 · notes p. 108" beside them. {complex}: a small GOLD arrow turns once beside the icons (a hint of part two). {next_term}: under them, DIM: "their equations: next term"; then the icons and the arrow fade.
> {beyond}: the DIM corner tag "beyond the notes" (22 px) fades in top-left; it stays in that corner through s7 (one tag for the chapter, DEEP_STYLE §12). New formulas: none.

[c1.hook.1] {swing} Here's a pendulum one metre long, and beside it, a weight on a spring. Two very different machines, and you can see them swinging in perfect step. {second} The pendulum takes about one second to swing across, and one second to swing back. {twins} Now take two identical pendulums, and give one a wide swing and the other a narrow one. {lag} You might expect the wide one to fall behind. {beat} It doesn't: they keep the same beat.

[c1.hook.2] {question} So what rule makes things swing like this, and what sets the beat? {pause} {title} This part finds that rule, from the physics up. {things} Pendulums, alternating currents and waves all swing like this, and complex numbers turn out to be the natural language for all of them, {complex} from part two on. {next_term} The general theory of their equations comes next term. {beyond} Most of this part goes beyond the notes, which take the physics as given. Here you build it from facts you already know.

## Scene 2 · Three tools (ch1_s2_tools)

> Names before process, then three retrieval questions. The pendulums from s1 fade; the corner tag stays.
> {legend}: the legend panel opens bottom-left (DIM border, 22–24 px) with its first entry, `x` BLUE: "displacement from the middle (signed)". Above it, centre: a horizontal line, a DIM tick "0" at the middle and a BLUE dot; a BLUE arrow from 0 to the dot. {signed}: the dot slides to the left of 0, the arrow flips, and a small BLUE "x < 0" appears.
> {dot}: the legend adds `\dot{x}` GREEN "velocity" and `\ddot{x}` RED "acceleration"; a DIM caption under the line: "one dot: rate of change in time · two dots: twice".
> {quiz}: three small retrieval cards appear one at a time across the upper middle (no box, no ring: quick questions). Each shows its picture and question, then its answer writes in on the answer mark.
> {trolley}: a trolley labelled "2 kg", an FG arrow "10 N" pushing it, "a = ?". {five}: "a = F/m = 10/2 = 5 m/s²". Then the card's `F = ma` transforms into `F = m\ddot{x}` (ẍ RED): the only time `a` means acceleration.
> {triangle}: a right-angled triangle, hypotenuse "10", a YELLOW angle "30°", the side opposite it "?". {opposite}: "opposite = hypotenuse × sin 30° = 10 × ½ = 5".
> {arc}: a sector of radius "2" with a YELLOW angle "0.5 rad"; its arc BLUE, "?". {arc_answer}: "arc = radius × angle = 2 × 0.5 = 1", DIM "(angle in radians)".
> {tools}: the three cards shrink and leave. Each returns small when it's used: the trolley's `F = m\ddot{x}` in s3, the triangle in s5, the arc in s6. Answers checked in Python 3.11.9 (10 sin 30° = 5; 2 × 0.5 = 1).

[c1.tools.1] {legend} First, the names. Whatever swings, ex is how far it is from the middle. {signed} It's signed: positive on one side, negative on the other. {dot} Ex with one dot on top is its rate of change in time, the velocity. Two dots means you take the rate of change again: that's the acceleration.

[c1.tools.2] {quiz} Now three quick questions, on tools this part will need. {trolley} A ten newton push on a two kilogram trolley. What's its acceleration? {pause=1.5} {five} Five metres per second squared. Force equals mass times acceleration, so you divide the force by the mass. From here on, the acceleration is written ex double dot.

[c1.tools.3] {triangle} A right-angled triangle with a hypotenuse of ten, and an angle of thirty degrees. How long is the side opposite that angle? {pause=1.5} {opposite} Ten times the sine of thirty degrees, which is five. {arc} Last one: an arc of a circle with radius two and an angle of half a radian. How long is it? {pause=1.5} {arc_answer} One. Arc length is radius times angle, with the angle in radians. {tools} All three get used in the next few minutes.

## Scene 3 · The pull grows with the stretch (ch1_s3_spring)

> {spring}: the spring drawing, centre-left (built once here, reused in every chapter; record its helper in STATUS.md): a wall at the left, an FG coil, the weight as a BLUE block on a DIM table line, a DIM tick "0" under its rest position. DIM tag under the table: "no friction". The corner tag "beyond the notes" stays top-left. Legend: x, ẋ, ẍ from s2. New formulas: 3 (F = −kx, ẍ = −(k/m)x, the rule ẍ = −ω²x; ω² = k/m is a name, F = mẍ retrieved).
> {pull}: live, the block is pulled right. A BLUE arrow from 0 to the block grows with the stretch, and a RED pull arrow on the block points left, growing in step. Readouts beside the picture: `x` (BLUE, cm) and "pull" (RED). {twice}: hold at 2 cm, then 4 cm: a RED ghost of the 2 cm arrow stays beside the new one, which is exactly twice as long; label "twice the stretch, twice the pull". A DIM tag "Hooke's law (GCSE)".
> {sign}: the block is pushed left of 0: the BLUE arrow flips (x negative), and the RED arrow flips to point right, still toward 0.
> {hooke}: the caption arrives under the picture: `F = -kx`, with F RED, k FG, x BLUE. The legend adds `k` "stiffness" and `m` "mass" (both FG). {minus}: the minus sign flashes YELLOW, with a DIM label "back toward the middle".
> {move}: the move card appears top-right (PLAN.md's look: YELLOW stroke, fill #171A21, "The move" in YELLOW 24 px): "Name the pull, then let Newton turn it into an acceleration." It stays for the scene.
> The derivation stacks in the right column, one operation per line, each arrow with its DIM label (≤ 5 words); at most 3 lines at full brightness, older ones at 0.4: {newton} `F = m\ddot{x}` ["Newton", the s2 card's line, TransformFromCopy from its small return]; {sub} `m\ddot{x} = -kx` ["the force is the pull"]; {divide} `\ddot{x} = -\frac{k}{m}\,x` ["divide by m"]; {name} `\omega^2 = \frac{k}{m}` ["a name"], the legend adds `\omega` FG "pull back per unit stretch, per kg"; {rule} `\ddot{x} = -\omega^2 x` boxed YELLOW (ẍ RED, x BLUE). Every step checked in sympy 1.14.0.
> {stop}: T1.1 think stop (PLAN.md's look): the question box in the lower third, "Same spring, twice the mass. Is the acceleration back toward the middle bigger or smaller, and by how much?", DIM "pause the video if you want longer" under it; the DIM ring bottom-right drains; nothing else moves, and the move card dims to 0.6. {same_pull}: a second block, labelled `2m`, on an identical spring below the first, at the same stretch: its RED pull arrow equal to the first. {half}: its acceleration readout half the first; the line `\ddot{x} = -\frac{k}{2m}\,x` with a YELLOW "half" (checked in sympy: the ratio is 1/2). Then the second spring leaves.

[c1.spring.1] {spring} Start with the simplest thing that swings: a weight on a spring, lying on a smooth table, so gravity plays no part for now. {pull} Pull the weight out, and the spring pulls back. The further you pull, the harder it pulls. {twice} Twice the stretch gives twice the pull: the pull is proportional to the stretch. That's Hooke's law, from GCSE physics.

[c1.spring.2] {sign} Now the sign. Ex to the right is positive, and the pull points left. Push the weight to the left, and you see both flip. {hooke} So the pull is minus the stiffness K, times ex. The stiffness says how strong the spring is. {minus} The minus sign means the pull always points back toward the middle.

[c1.spring.3] But you want the motion, not the force. Newton ties a force to an acceleration, and the acceleration is the position, differentiated twice. {move} So the move here is: name the force that pulls back, then let Newton turn it into an acceleration. {newton} Force equals mass times acceleration. {sub} The only force is the spring pulling back, so the mass M, times ex double dot, is minus K times ex. {divide} Divide by the mass: ex double dot equals minus K over M, times ex.

[c1.spring.4] {name} That ratio, K over M, is the pull back per unit of stretch, for each kilogram it has to move. Call it omega squared. It's written as a square for a reason part two makes clear. {rule} So ex double dot equals minus omega squared, times ex. Out of context it looks abstract, but you can read it as: the acceleration always points back to the middle, and it grows with the distance.

[c1.spring.5] {stop} Here's one for you. Same spring, twice the mass. Is the acceleration back toward the middle bigger or smaller, and by how much? Pause the video if you want longer. {pause=4} {same_pull} The pull depends only on the stretch, so it's the same as before. But now it has twice the mass to move. {half} So the acceleration is half as big: minus K over two M, times ex. A heavier weight on the same spring swings more slowly.

## Scene 4 · Reading the rule (ch1_s4_extremes)

> The spring drawing stays centre-left. s3's boxed rule `\ddot{x} = -\omega^2 x` moves to the top of the right column; the rest of s3's stack and its move card leave. Legend as in s3. New formulas: none (a number put into the rule).
> {number}: the right column, a number first: `\omega^2 = 4`, `x = 0.5\text{ m}`, then `\ddot{x} = -4 \times 0.5` ["put the numbers in"], then `\ddot{x} = -2\ \text{m/s}^2` ["multiply"]. The block sits at 0.5 m with a RED arrow pointing back to 0 (checked: −4 × 0.5 = −2).
> {swing}: the weight oscillates between −0.5 m and +0.5 m (ω = 2 per second), carrying three arrows: BLUE from 0 to the block (position), GREEN on the block (velocity, length ∝ ẋ), RED on the block (acceleration, length ∝ ω²x, pointing to 0). Live readouts: `x` BLUE and `\ddot{x}` RED.
> {middle}: freeze as the block crosses 0 moving right: the BLUE and RED arrows have shrunk to nothing, the GREEN arrow is at its longest. Readouts `x = 0`, `\ddot{x} = 0`; tag "no pull · fastest". {coast}: resume; a DIM ghost of the block shows it carrying on past 0.
> {end}: freeze at x = 0.5 m: the GREEN arrow is gone. The RED arrow is hidden here until {answer}, so the picture doesn't give the answer away.
> {stop}: T1.2 think stop: "At the very end of its swing the weight is still for an instant. Is its acceleration zero there too?", DIM "pause the video if you want longer", the ring drains, everything frozen.
> {answer}: the RED arrow grows in at full length; the readout `\ddot{x} = -4 \times 0.5 = -2\ \text{m/s}^2`, tagged "the largest". {still}: a struck-through line "still ⇒ no acceleration", with a RED ✗ (the named wrong idea).
> {never}: resume the oscillation, all three arrows live. DIM labels flash in turn: "overshoots" at the middle, "turns back" at each end. The weight keeps swinging under the rest of the scene.

[c1.ends.1] {number} First, try it with numbers. Say omega squared is four, and the weight is half a metre out. Then the acceleration is minus four times a half: two metres per second squared, back toward the middle. {swing} Now let it swing, out to half a metre on each side. Keep your eye on the green velocity arrow and the red acceleration arrow.

[c1.ends.2] {middle} Freeze it as it crosses the middle. Here ex is zero, so the rule says there's no pull at all. But the weight is moving at its fastest. {coast} With nothing there to slow it down, it carries straight on past.

[c1.ends.3] {end} Now let it run out to the end of its swing, and freeze. {stop} The weight is still, for an instant. Is its acceleration zero there too? Pause the video if you want longer. {pause=4} {answer} You might expect so, since nothing is moving. But the rule only looks at where the weight is, and here it's as far out as it ever gets. So the pull is the largest it ever is: minus four times a half, minus two. {still} Being still and being free of any pull are two different things.

[c1.ends.4] {never} So now you can see why the weight never settles. In the middle there's no pull, but it's moving too fast to stop. At each end it stops, but that's where it's pulled hardest. That's why it swings.

## Scene 5 · What pulls a pendulum back (ch1_s5_gravity)

> {pendulum}: the pendulum drawing, centre-left (scan p. 10's margin sketch, redrawn; built once here and reused in every chapter, helper recorded in STATUS.md): a hatched FG ceiling, a DIM dashed vertical from the pivot, the FG rod labelled `L`, the BLUE bob labelled `m`, leaning left of the vertical as in the sketch. The spring leaves. Legend: x, ẋ, ẍ, m, plus `L` "length of the rod" and `g` "9.81 m/s²" (FG). The busiest frame of the chapter (diagram, split arrows, stack, legend, move card, corner tag): check it at 1440p first (DEEP_STYLE §12). New formulas: 1 (F = −mg sin θ).
> {theta}: the YELLOW angle θ between the dashed vertical and the rod, at the pivot; the legend adds `\theta` YELLOW "angle from the vertical (radians)". A DIM tag beside it: "the notes call this angle x(t) · scan p. 10".
> {weight}: gravity's arrow `mg` (FG) straight down from the bob. {rod}: the rod's pull, a DIM arrow along the rod toward the pivot. {right_angle}: a DIM dashed line through the bob along the direction of the swing (the tangent to its arc), with a small right-angle mark between it and the rod.
> {question}: a YELLOW "?" beside the tangent line, over the bob. {move}: the move card, top-right: "Split gravity along the rod and the swing: only the swing part drives." (PLAN.md's M2 says "the rod cancels one part"; see the report.)
> Atomic steps in the right column, each with its DIM label: {g_vert} "gravity: straight down"; {rod_tilt} "the rod: θ off the vertical"; {apart} "so gravity and the rod's line are θ apart": the YELLOW θ is copied (TransformFromCopy) from the pivot down to the bob, between the `mg` arrow and the rod's dashed extension past the bob.
> {split}: `mg` splits into two arrows that form a right-angled triangle with `mg` as its hypotenuse: along the rod, outward (DIM), `mg\cos\theta`; along the swing, toward the bottom (RED), `mg\sin\theta`. {opposite}: s2's triangle card returns small for a moment beside it ("opposite = hypotenuse × sin"), then leaves.
> {sign}: the caption `F = -mg\sin\theta` (F RED, m g FG, θ YELLOW) ["points back to the bottom"], its minus flashing YELLOW.
> {sweep}: a live sweep: θ goes 0 → 40° (the bob moves along its arc and the whole split redraws), with readouts θ (YELLOW, in degrees and radians) and "pull = 0.643 mg" (RED, live; at 40°, sin 40° = 0.643, checked). {flip}: θ sweeps on through 0 to −40°: the RED arrow shrinks to nothing at the bottom, then flips, still pointing to the bottom. Back to θ = 30°, frozen, for s6.

[c1.gravity.1] {pendulum} Now the pendulum: a weight called the bob, on a rod of length L, hung from a fixed point. {theta} You measure its angle from the vertical, and call it theta for now. {weight} Two forces act on the bob. Gravity pulls it straight down with its weight: the mass M, times G, the strength of gravity. {rod} And the rod pulls along itself, toward the pivot. {right_angle} But the bob can only move along its arc, and the rod pulls at right angles to that. So the rod can't speed the bob up, or slow it down.

[c1.gravity.2] {question} So which part of gravity can? {pause=1.5} {move} The move here is: split gravity into a part along the rod and a part along the swing. Only the part along the swing drives the motion. {g_vert} Gravity points straight down. {rod_tilt} The rod leans theta away from the vertical. {apart} So gravity and the line of the rod are theta apart, too.

[c1.gravity.3] {split} Now you draw gravity's arrow as the hypotenuse of a right-angled triangle, with one side along the rod, and one along the swing. {opposite} The part along the swing is the side opposite theta: M times G, times the sine of theta, just like the triangle you saw at the start. {sign} It points back toward the bottom, so the pull is minus M times G, times sine theta.

[c1.gravity.4] {sweep} Watch gravity's pull as you change the angle. At the bottom, theta is zero, and there's no pull at all. Swing out to forty degrees, and gravity pulls with about sixty-four percent of the bob's weight. {flip} Swing to the other side, and it flips, still pointing home. Read it back: the further out the bob is, the harder gravity drags it home, but by the sine of the angle, not by the angle itself.

## Scene 6 · From angle to distance (ch1_s6_arc)

> s5's pendulum stays centre-left, frozen at θ = 30°, with its RED along-swing arrow and DIM along-rod arrow. s5's stack leaves except `F = -mg\sin\theta`, now at the top of the right column; s5's move card leaves. Legend as in s5. New formulas: 2 (s = Lθ, θ̈ = −(g/L) sin θ).
> {newton}: `m \times (\text{acceleration along the swing}) = -mg\sin\theta` ["Newton, along the swing"]. {divide}: `\text{acceleration along the swing} = -g\sin\theta` ["divide by m"], the two m's struck out together.
> {stop}: T1.3 think stop: "Swap the bob for one twice as heavy. Does the pendulum swing faster, slower, or the same?", DIM "pause the video if you want longer", the ring drains, frozen.
> {same}: the bob grows into a bigger bob labelled `2m`; its `mg` arrow doubles and so does its RED along-swing arrow; the struck-out m's flash: the acceleration along the swing is unchanged. {spring_contrast}: s3's T1.1 picture returns small beside it, a two-row comparison: spring "pull: same · mass ×2 → slower"; pendulum "pull ×2 · mass ×2 → same" (checked in sympy 1.14.0: m is absent from θ̈).
> {arc}: the arc from the bottom of the swing up to the bob, BLUE, labelled `s`; s2's arc card returns small for a moment. Caption: `s = L\theta` (s BLUE, L FG, θ YELLOW) ["arc = radius × angle"]; the legend adds `s` BLUE "distance along the arc".
> {twice}: `\dot{s} = L\dot{\theta}` ["differentiate; L is fixed"], then `\ddot{s} = L\ddot{\theta}` ["differentiate again"] (ṡ, θ̇ GREEN; s̈, θ̈ RED). A brace joins `\ddot{s}` to the words "acceleration along the swing" in the line above.
> {sub}: `L\ddot{\theta} = -g\sin\theta` ["substitute"]; {divide_L}: `\ddot{\theta} = -\frac{g}{L}\sin\theta` ["divide by L"], boxed. Older lines dim to 0.4.
> {compare}: s3's boxed `\ddot{x} = -\omega^2 x` slides in beside it; `\sin\theta` in the new box glows against the `x` in the old one, with a YELLOW "almost". {hard}: a DIM tag under the pendulum's equation: "no answer in familiar functions".

[c1.arc.1] {newton} Now let Newton turn gravity's pull into an acceleration along the swing: the mass, times the acceleration along the swing, equals minus M times G, times sine theta. {divide} Divide by the mass, and the acceleration along the swing is minus G, times sine theta. The mass is gone.

[c1.arc.2] {stop} Now a question for you. Swap the bob for one twice as heavy. Does the pendulum swing faster, slower, or the same? Pause the video if you want longer. {pause=4} {same} The same. Twice the mass means twice the weight, so the pull doubles too, and the two cancel. {spring_contrast} The spring is different: its pull depends only on the stretch, which is why the heavier weight on the spring was slower.

[c1.arc.3] There's one snag left. Newton counts the distance the bob travels, but you're describing the pendulum by its angle. {arc} The arc turns one into the other. The bob moves on a circle of radius L, so its distance along the arc is L times theta, with theta in radians. {twice} The length L is fixed, so differentiate twice: the acceleration along the arc is L times theta double dot.

[c1.arc.4] {sub} Put that in: the length L, times theta double dot, equals minus G, times sine theta. {divide_L} Divide by the length L: theta double dot equals minus G over L, times sine theta. {compare} Now read it back, next to the spring's rule. It's almost the same, but with the sine of theta where theta should be. {hard} And that sine makes it much harder: this equation has no answer in any functions you know.

## Scene 7 · Small swings (ch1_s7_small)

> The same pendulum, centre-left, at θ = 30°, with s6's BLUE arc `s`. s6's boxed `\ddot{\theta} = -\frac{g}{L}\sin\theta` sits at the top of the right column. Legend as in s6. New formulas: 2 (sin θ ≈ θ, ω = √(g/L)).
> {move}: the move card, top-right: "For small swings, trade sin θ for θ: arc and reach almost agree."
> {reach}: the bob's sideways reach, a straight FG dashed segment from the dashed vertical across to the bob, labelled `L\sin\theta` (the side opposite θ again). {arc_len}: the BLUE arc keeps s6's colour and gains the label `L\theta`. (PLAN.md drew the reach BLUE and the arc YELLOW here; the arc keeps s6's BLUE, so the reach takes FG. See the report.)
> {sweep}: a live sweep, θ from 0 up to 60°, slowly, with the arc and the reach redrawn and a growing table of readouts: θ (YELLOW, rad), sin θ, and "short by". The table's rows stay as the sweep passes them: {r1} `0.1` · `0.0998` · 0.2%; {r2} `10° = 0.1745` · `0.1736` · 0.5%; {r3} `30° = 0.5236` · `0.5000` · 4.5%; {r4} `60° = 1.047` · `0.866` · 17%. The gap between the arc and the reach opens visibly at 60° (all values checked in Python 3.11.9).
> {trade}: back to a small swing (10°). In the column: `\sin\theta \approx \theta` ["small swings"], then `\ddot{\theta} \approx -\frac{g}{L}\,\theta` ["trade sin θ for θ"]. {match}: s3's `\ddot{x} = -\omega^2 x` beside it, `\omega^2 = \frac{g}{L}` ["match the two"]; the legend's ω entry gains "pendulum: g/L". {root}: `\omega = \sqrt{g/L}` boxed YELLOW ["square root"], with a DIM tag "notes p. 108: stated there, built here".
> {numbers}: `L = 1\text{ m}`: `\omega^2 = 9.81`, `\omega \approx 3.13` per second (checked: 3.1321); the pendulum swings gently at 10°.
> {flag}: the pendulum moves out to 60° and freezes: its RED true pull `mg\sin\theta` against a dashed RED ghost arrow, "the rule's pull, mg θ", about 17% longer; DIM tag "big swings: a weaker pull than the rule says (part two)". {done}: the corner tag "beyond the notes" leaves.

[c1.small.1] {move} So here's the last move: for small swings, trade sine theta for theta. {reach} To see why that's fair, you can compare two lengths on the same picture. The bob's sideways reach is L times sine theta, the side opposite the angle. {arc_len} Its distance along the arc is L times theta. For a small swing, the arc is nearly straight, so the two almost agree.

[c1.small.2] {sweep} How good is that trade, would you guess? {pause=1.5} {r1} At a tenth of a radian, the sine is point zero nine nine eight: two tenths of a percent short. {r2} At ten degrees, it's half a percent short. {r3} At thirty degrees, four and a half percent. {r4} At sixty degrees, the sine is seventeen percent short, and the trade starts to fail.

[c1.small.3] {trade} So for small swings, theta double dot is about minus G over L, times theta. {match} That's the spring's rule exactly, with omega squared equal to G over L. {root} So omega is the square root of G over L. Read it back: a longer pendulum is pulled back more gently, for each radian of swing. {numbers} For the one metre pendulum, omega squared is nine point eight one, so omega is about three point one three per second. What that does to its beat is part two's story.

[c1.small.4] {flag} One honest warning. At big angles, gravity really pulls with the sine of theta, and that is weaker than the rule, which uses theta itself. So for big swings the rule is only an approximation, and part two shows what that costs. {done} For small swings, though, you now have the rule.

## Scene 8 · One rule, and recap (ch1_s8_recap)

> {both}: s3's spring drawing on the left and s5's pendulum on the right, both swinging in step (as in s1), each with its RED pull arrow live. Between them, boxed YELLOW: `\ddot{x} = -\omega^2 x`; under the spring `\omega^2 = \frac{k}{m}`, under the pendulum `\omega^2 = \frac{g}{L}`.
> {rename}: on the pendulum, the YELLOW θ label transforms into a BLUE `x`; DIM tags "angular displacement x(t) · notes p. 108" and "reference". The legend's entries collapse to the chapter's set: x "displacement (spring: distance · pendulum: angle)", ẋ, ẍ, ω.
> {shm}: under the rule, a YELLOW box "simple harmonic motion", with DIM "named by its rule · its form: part two".
> {recap}: the two machines shrink away. Three columns, each a small moving version of the picture that taught its move, with that scene's move card small above it: {m1} s3's spring, pulled out and released, its RED arrow growing with the stretch, "name the pull, let Newton make it an acceleration"; {m2} s5's pendulum swaying, gravity split into its DIM along-rod and RED along-swing arrows, "split gravity: only the swing part drives"; {m3} s7's BLUE arc and FG dashed reach sweeping together out to 60° and back, "small swings: sin θ ≈ θ".
> {facts}: one DIM line under the three: "F = mẍ · Hooke: F = −kx · g = 9.81 m/s² · arc = radius × angle (radians)".
> {next}: the columns clear. A BLUE dot moves back and forth on a horizontal line, `\ddot{x} = -\omega^2 x` above it, and a YELLOW "x(t) = ?". {arrow}: a faint GOLD arrow appears above the line, turning, its tip joined to the BLUE dot by a DIM dashed line straight down: the dot is its shadow. Then the end card: hold about 8 s after the last word while the music carries it.

[c1.recap.1] {both} So here are two very different machines, obeying one rule: ex double dot equals minus omega squared, times ex. For the spring, omega squared is K over M. For the pendulum, it's G over L. {rename} From now on, whatever swings, you call its displacement ex, even when it's an angle. {shm} Anything pulled back in proportion to how far out it is obeys this rule. Its motion has a name: simple harmonic motion.

[c1.recap.2] {recap} Time for a recap. {m1} First move: name the force that pulls back, then use Newton to turn it into an acceleration. {m2} Second: split gravity along the rod and along the swing. Only the swing part drives the bob. {m3} Third: for small swings, trade sine theta for theta, because the arc and the reach almost agree. {facts} And four facts you need to keep: Newton's law, Hooke's law, G is nine point eight one metres per second squared, and arc length is radius times angle.

[c1.recap.3] {next} Next time: which motion obeys this rule? You need a function that comes back as minus omega squared times itself after two derivatives. {pause} {arrow} The answer is the shadow of an arrow that turns in a circle.
