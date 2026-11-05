# Chapter 1 · Cosine without the i

NST IA Mathematics, Lecture 11 (Hyperbolic Functions and Conics), part 1 of 7. Source: notes `Chapter234_to_annotate.pdf` pp. 31–32 (§3.1, equations (84)–(92)); lecture recording 04:41–08:10, and its recap of Lecture 10 (00:00–03:12) for "last time".

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card: "Hyperbolic Functions and Conics", "NST IA Mathematics · Lecture 11", "Part 1 · Cosine without the i".
> On {last}: last time's pair, centred, as the notes' §3.1 writes them (with x; Lecture 10 used θ): `\cos x = \frac{e^{ix} + e^{-ix}}{2}` above `\sin x = \frac{e^{ix} - e^{-ix}}{2i}`. cos and sin BLUE, e^{ix} GOLD and e^{−ix} PURPLE, every i PINK.
> On {cosine}: the sine line dims. On {lift}: the two PINK i's in the cosine's exponents float up out of the formula and fade. On {left}: what stays re-forms as `\frac{1}{2}\left(e^{x} + e^{-x}\right)` (GOLD e^x, PURPLE e^{−x}), with a TEAL "?" where the function's name goes. On {new}: the "?" pulses.
> On {pair}: the formulas clear. Left: the unit circle x² + y² = 1 (BLUE) with a point (cos θ, sin θ) running round it. On {hyper}: right, the hyperbola x² − y² = 1 (TEAL), right branch solid and left branch DIM, with a point (cosh θ, sinh θ) running up the right branch in step with the circle's point. Coordinate labels under each point; no angle arcs (θ is a parameter here, not an angle).
> On {ask}: three short lines under the pair, one per question: "What are they?", "How are they tied to cosine and sine?", "Why 'hyperbolic'?". On {answer}: the first two get a GREEN tag "this chapter", the third a DIM tag "Parts 2 and 6".
> The circle–hyperbola pair is a running visual: ch2 s2 explains it with an identity and ch6 s3 pays it off, so keep its style reusable.

[c1.hook.1] {title} This is part one of Hyperbolic Functions and Conics. {last} Last time, in Lecture ten, you wrote cosine and sine with complex exponentials, E to the eye ex, and E to the minus eye ex. {pause}

[c1.hook.2] {cosine} Take the formula for cosine of ex. {lift} Now lift out every eye. {left} What stays is E to the ex, plus E to the minus ex, all over two. {pause} {new} It looks almost the same, but it's built from real exponentials only, and it's a brand new function.

[c1.hook.3] {pair} Here's a glimpse of where it leads. On the left, cosine and sine carry a point round a circle. {hyper} On the right, this new function and its partner carry a point along a different curve, a hyperbola. {pause}

[c1.hook.4] {ask} So, three questions. What are these new functions? How are they tied to cosine and sine? And why are they called hyperbolic? {answer} You'll answer the first two in this chapter. The third takes a little longer. {pause}

## Scene 2 · Real exponentials (ch1_s2_define)

> Top: last time's pair from the hook (same colours). On {old} it settles there; on {ask} a YELLOW ring round the PINK i's in the exponents.
> On {cosh}: TransformFromCopy of the cosine line into `\cosh x = \frac{1}{2}\left(e^{x} + e^{-x}\right)` (84) below it, the PINK i's dropping out, cosh TEAL. On {sinh}: the same from the sine line to `\sinh x = \frac{1}{2}\left(e^{x} - e^{-x}\right)` (85). On {denom}: a YELLOW flash on the sine's 2i, its PINK i fades, leaving the ½. Equation numbers small and DIM. On {real}: a small GREEN tag "real in, real out". (Checked with sympy 1.14.)
> On {axes}: the two definitions shrink to the top-left corner; axes appear (x from about −2.5 to 2.5, y from about −3 to 5, curves clipped at the frame). On {gold}: e^x draws in GOLD; on {purple}: e^{−x} in PURPLE, its mirror image in the y-axis. These axes and colours are the series' graph style: ch3 reuses them and adds dashed ½e^x and ½e^{−x}.
> On {stand}: a DIM vertical line at x = 1, a GOLD dot on e^x labelled "2.72" and a PURPLE dot on e^{−x} labelled "0.37". On {mid}: a TEAL dot halfway between them, labelled "cosh 1 ≈ 1.54".
> On {sweep}: the line slides across the axes and the midpoint dot traces the cosh curve (TEAL). On {gap}: back at x = 1, a brace on the gap between the GOLD and PURPLE dots; the brace halves and is set down on the x-axis, giving a dot labelled "sinh 1 ≈ 1.18"; a second sweep traces sinh (TEAL, a lighter shade so the two stay distinct, each curve labelled). On {zero}: at x = 0 the exponentials cross at 1 and sinh passes through 0; left of 0 the PURPLE curve is on top and sinh dips below the axis.
> On {add}: the graph dims; `\cosh x + \sinh x = \tfrac{1}{2}e^{x} + \tfrac{1}{2}e^{-x} + \tfrac{1}{2}e^{x} - \tfrac{1}{2}e^{-x}`. On {cancel}: the two ½e^{−x} terms strike out (RED) and the two ½e^x merge. On {result}: `e^{x} = \cosh x + \sinh x`, boxed YELLOW. On {cousin}: beside it, `e^{ix} = \cos x + i\sin x` (BLUE, i PINK), its circular cousin. (Ch7 uses e^x = cosh x + sinh x again.)

[c1.def.1] {old} Here's last time's pair again. Cosine of ex is the sum of the two exponentials, over two. Sine of ex is their difference, over two eye. {ask} The lecture asks a simple question. What happens if the exponent is real, with no eye in it? {pause}

[c1.def.2] {cosh} Keep the shape, and use real exponentials. E to the ex, plus E to the minus ex, all over two, is the hyperbolic cosine, cosh of ex. {sinh} Their difference over two is the hyperbolic sine, shine of ex. {denom} Look at its denominator. It's just two, with no eye this time. {real} These are real functions. Feed them a real number, and you get a real number back.

[c1.def.3] {axes} To see them, put both exponentials on one set of axes. {gold} E to the ex, in gold, climbs to the right. {purple} E to the minus ex, in purple, is its mirror image. {stand} Now stand at ex equals one. Here E to the ex is about two point seven two, and E to the minus ex is about zero point three seven. {mid} Cosh of one is their average, the point halfway between, about one point five four.

[c1.def.4] {sweep} Now slide across, taking the midpoint everywhere. The midpoints trace out cosh. {gap} Shine is half the gap between the two curves, gold minus purple. At ex equals one, that's about one point one eight. {zero} At zero, the curves cross, so the gap is zero. To the left, purple is on top, and shine goes negative. {pause} So cosh is the average of the two exponentials, and shine is half their difference.

[c1.def.5] {add} One more thing falls out. Add cosh and shine. {cancel} The E to the minus ex terms cancel, and the two E to the ex terms, a half each, add up to one whole E to the ex. {result} So E to the ex equals cosh of ex, plus shine of ex. {cousin} Compare that with E to the eye ex, which is cosine of ex, plus eye times sine of ex. It's the same pattern, without the eye.

## Scene 3 · tanh and three reciprocals (ch1_s3_family)

> Top-left, small: s2's cosh and sinh definitions (same colours).
> On {tanh}: `\tan x = \frac{\sin x}{\cos x}` (BLUE) on the left; on the right, copies of sinh and cosh slide into `\tanh x = \frac{\sinh x}{\cosh x}` (TEAL). On {one}: s2's two labels "sinh 1 ≈ 1.18" and "cosh 1 ≈ 1.54" fly in as a fraction, giving "tanh 1 ≈ 0.76" (GOLD numbers), then clear. On {expand}: it expands to `\frac{\frac{1}{2}(e^{x} - e^{-x})}{\frac{1}{2}(e^{x} + e^{-x})}`; the two ½ flash YELLOW and cancel, leaving `\tanh x = \frac{e^{x} - e^{-x}}{e^{x} + e^{-x}}` (86), GOLD e^x, PURPLE e^{−x}. (Checked with sympy 1.14.)
> On {names}: the notes' grey box, verbatim: "When spoken, the names ‘hyperbolic cosine’, ‘hyperbolic sine’ and ‘hyperbolic tangent’ are often abbreviated to ‘cosh’, ‘shine’ and ‘tanch’." Small YELLOW speech labels pop under cosh, then sinh ({shine}), then tanh ({tanch}). On {circ}: a BLUE header "cosine, sine, tangent" over the circular column and a TEAL header "cosh, shine, tanch" over the hyperbolic one.
> On {recip}: the family card, two columns. Left (BLUE): `\sec x = \frac{1}{\cos x}`, `\operatorname{cosec} x = \frac{1}{\sin x}`, `\cot x = \frac{1}{\tan x}`. On {sech}, {cosech}, {coth}: each TEAL row grows out of its parent: `\operatorname{sech} x = \frac{1}{\cosh x}` (87), `\operatorname{cosech} x = \frac{1}{\sinh x}` (88), `\coth x = \frac{1}{\tanh x}` (89). On {letter}: the trailing "h" of every hyperbolic name on the card flashes TEAL (cosh, sinh, tanh too).
> On {warn}: the card dims except the sech row. On {inv}: beside it, in RED, `\cosh^{-1} x \neq \frac{1}{\cosh x}`. On {undo}: under it, "the inverse: undoes cosh" with a small `\ln` in TEAL. On {later}: a DIM tag "Part 3", then the RED card shrinks to a corner.
> The family card (with the tanh row on top) comes back small in the recap (s7).

[c1.family.1] {tanh} Just as tangent is sine over cosine, the hyperbolic tangent is shine over cosh. {one} Back at ex equals one, that's about one point one eight over one point five four, so tanch of one is about zero point seven six. {expand} Write both in exponentials, and the factors of a half cancel. What's left is the difference of the two exponentials, over their sum. {pause}

[c1.family.2] {names} About those names. The notes say how to pronounce them: cosh, {shine} shine, {tanch} and tanch. {circ} In this series, cosine, sine and tangent always mean the circular functions, and cosh, shine and tanch always mean the hyperbolic ones.

[c1.family.3] {recip} The circular functions have three reciprocals: secant, cosecant and cotangent. {sech} The hyperbolic ones copy them. The hyperbolic secant is one over cosh. {cosech} The hyperbolic cosecant is one over shine. {coth} And the hyperbolic cotangent is one over tanch. {letter} On paper, each hyperbolic name is its circular parent, with one extra letter on the end.

[c1.family.4] {warn} Here's a warning, because this one trips people up. The hyperbolic secant is one over cosh. {inv} That is a different thing from the inverse of cosh, written with a small minus one up top. {undo} The inverse is the function that undoes cosh, and it's built from logarithms. {later} You'll meet it properly in part three. {pause}

## Scene 4 · Putting the i back: cos(ix) (ch1_s4_cosix)

> One centred derivation column. On {setup}: s2's cos x and cosh x lines side by side, small, then clear. On {cosz}: `\cos z = \frac{e^{iz} + e^{-iz}}{2}` (cos BLUE, i PINK, e^{iz} GOLD, e^{−iz} PURPLE), with a small DIM note "any complex z".
> On {sub}: a YELLOW tag `z = ix` (with "x complex too"); each z turns into ix. On {isq}: `\cos(ix) = \frac{e^{i \cdot ix} + e^{-i \cdot ix}}{2}` then `= \frac{e^{i^2 x} + e^{-i^2 x}}{2}` (the notes' form).
> On {margin}: the lecturer's margin note at the right, YELLOW, handwriting-style: `i^2 = -1`.
> On {flip}: the first term becomes `e^{-x}` and turns PURPLE; on {flip2}: the second becomes `e^{x}` and turns GOLD: `= \frac{e^{-x} + e^{x}}{2}`.
> On {swap}: the two terms slide past each other into `= \frac{e^{x} + e^{-x}}{2}`; on {order} s2's (84) appears beside it, small, and the two match term for term.
> On {boxed}: `\cos(ix) = \cosh x` (90), boxed YELLOW (the lecturer boxed it too), cos BLUE, cosh TEAL. This row starts the dictionary card in the top-right corner, which s5 extends and s6 completes. (Checked with sympy 1.14, and numerically at complex x with Python 3.11 cmath.)
> On {check}: `\cos(i) = \cosh 1 \approx 1.54`. On {midpoint}: a thumbnail of s2's graph at x = 1, its TEAL midpoint dot lighting up. On {stuck}: a small cosine wave (BLUE) between dashed lines y = 1 and y = −1, and the value 1.54 as a YELLOW dot above the band.

[c1.cosix.1] {setup} The new functions look like cousins of cosine and sine. Now let's find the exact family tie. {cosz} Start from cosine of zed, where zed can be any complex number. It's E to the eye zed, plus E to the minus eye zed, all over two.

[c1.cosix.2] {sub} Here's the trick from the notes. Put zed equal to eye times ex, where ex can be complex too. {isq} The first exponent becomes eye, times eye ex. That's eye squared, times ex. {margin} And eye squared is minus one. {flip} So E to the eye zed turns into E to the minus ex. {flip2} In the second exponent, the minus in front meets eye squared, and two minuses make a plus. You get E to the ex.

[c1.cosix.3] {swap} Look at what happened. The two exponentials have swapped places. {pause} {order} But you can add in any order, so the sum is unchanged. It's E to the ex, plus E to the minus ex, over two, which is exactly cosh of ex. {boxed} So cosine of eye ex equals cosh of ex. {pause=1.5}

[c1.cosix.4] {check} Try it with ex equal to one. The cosine of eye is cosh of one, about one point five four. {midpoint} That's the midpoint you found on the graph. {pause} {stuck} So here's a cosine bigger than one. On the real line, cosine is stuck between minus one and one. Once you step off the real line, it breaks free.

## Scene 5 · sin(ix) and tan(ix) (ch1_s5_sinix)

> Same derivation layout and colours as s4; the dictionary card's first row stays small in the top-right.
> On {sine}: `\sin z = \frac{e^{iz} - e^{-iz}}{2i}`. On {sub}: the YELLOW tag `z = ix`, and as in s4 each exponential turns into the other: `\sin(ix) = \frac{e^{-x} - e^{x}}{2i}` (PURPLE first, GOLD second). On {backwards}: a YELLOW flash on the minus between them, "order matters".
> On {minus}: `= -\frac{e^{x} - e^{-x}}{2i}`, the leading minus YELLOW. On {slow}: everything but this line dims.
> On {onei}: a side panel slides in: `\frac{1}{i}`. On {mult}: `= \frac{1 \cdot i}{i \cdot i} = \frac{i}{i^2} = \frac{i}{-1}`, one step at a time; on {result}: `= -i`, boxed GREEN. On {cancel}: in the main line `-\frac{1}{2i}` becomes `\frac{i}{2}` (the two minus signs flash YELLOW and vanish): `= \frac{i}{2}\left(e^{x} - e^{-x}\right)`. (The notes print this bracket as (−e^{−x} + e^{x}); same thing.)
> On {sinh}: the ½ and the bracket glow TEAL and become `\sinh x`. On {boxed}: `\sin(ix) = i\sinh x` (91), boxed YELLOW, the i PINK; the dictionary card gains this row. On {extra}: the PINK i pulses. On {slip}: below, the classic slip `\sin(ix) = -i\sinh x` in RED, crossed out, with an arrow back to the 1/i panel.
> On {tan}: the column clears to `\tan(ix) = \frac{\sin(ix)}{\cos(ix)}`. On {ratio}: the two boxed results drop in from the card: `= \frac{i\sinh x}{\cosh x}`. On {tanh}: `= i\tanh x`. On {boxed2}: `\tan(ix) = i\tanh x` (92), boxed; the card gains its third row. (The notes print (92) with z: tan(iz) = i tanh z. All of it checked with sympy 1.14.)

[c1.sinix.1] {sine} Now the same trick with sine. Sine of zed is E to the eye zed, minus E to the minus eye zed, all over two eye. {sub} Put zed equal to eye ex, and once again the two exponentials swap. {backwards} But this time, order matters. The difference comes out backwards, E to the minus ex, minus E to the ex, over two eye.

[c1.sinix.2] {minus} Turn it round by pulling out a minus sign. Now the bracket reads E to the ex, minus E to the minus ex, and in front sits minus one over two eye. {slow} This next step is where people drop a sign, so let's go slowly. {pause}

[c1.sinix.3] {onei} What is one over eye? {pause} {mult} Multiply the top and the bottom by eye. The top becomes eye. The bottom becomes eye squared, which is minus one. {result} So one over eye is minus eye. {cancel} That turns minus one over two eye into plus eye over two. The two minus signs cancel.

[c1.sinix.4] {sinh} What's left is eye, times half the difference of the exponentials. And half their difference is shine of ex. {boxed} So sine of eye ex equals eye times shine of ex. {pause} {extra} Compared with the cosine, there's an extra eye in front. {slip} If you ever get minus eye instead, go back and check the one over eye step.

[c1.sinix.5] {tan} Tangent comes for free. Divide the sine of eye ex by the cosine of eye ex. {ratio} That's eye times shine of ex, over cosh of ex. {tanh} And shine over cosh is tanch. {boxed2} So tangent of eye ex equals eye times tanch of ex. {pause}

## Scene 6 · Valid for every complex number (ch1_s6_dictionary)

> On {card}: the dictionary card moves to the centre, full size. Header "for every complex x" (YELLOW); rows `\cos(ix) = \cosh x`, `\sin(ix) = i\sinh x`, `\tan(ix) = i\tanh x`; circular names BLUE, hyperbolic TEAL, the extra i PINK, (90)–(92) small and DIM. This card is reused in ch2 s3 and s6, ch4 s3, and small in this chapter's recap: build it as one reusable object.
> On {all}: the header pulses. On {check}: under the card, `x = 1 + 2i`, then `\cos\big(i(1 + 2i)\big) \approx -0.642 + 1.069i` and `\cosh(1 + 2i) \approx -0.642 + 1.069i`, the two values lighting up GREEN together (checked with Python 3.11 cmath).
> On {read}: the check clears; a GREEN tick by the cosine row, "no i". On {extrai}: the PINK i's in the sine and tangent rows pulse.
> On {back}: an arrow flips the card's direction, hyperbolic on the left: `\cosh x = \cos(ix)`; on {back2}: `\sinh x = -i\sin(ix)`, the −i PINK (since −i · i sinh x = sinh x; checked with sympy 1.14).
> On {buys}: the card shrinks up; two preview cards appear below. On {ident}: "Part 2": `\cos^2 x + \sin^2 x = 1` (BLUE), an arrow to TEAL `\cosh^2 x \;?\; \sinh^2 x = 1`, the "?" YELLOW. On {split}: "Part 4": `\cos z = 2`, with `z = x + iy` and two short arrows to "real part" and "imaginary part" (imaginary PINK).

[c1.dict.1] {card} Put the three results together, and you get a small dictionary between the two worlds. {all} The notes stress that these hold for every complex ex, and not only for real ones. Nothing in the working needed ex to be real. {check} Try a properly complex ex, one plus two eye. Work out both sides, and they come out the same.

[c1.dict.2] {read} Reading across the card, cosine turns into cosh with no change at all. {extrai} Sine and tangent turn into shine and tanch, with an extra eye in front. {back} You can also read it backwards. Cosh of ex is cosine of eye ex. {back2} And shine of ex is minus eye, times sine of eye ex. {pause}

[c1.dict.3] {buys} So what does the dictionary buy you? {ident} First, every identity for cosine and sine becomes one for cosh and shine, sometimes with a sign flipped. That's Part two. {split} Second, the cosine of any complex number splits into a real part and an imaginary part, built from cosine, sine, cosh and shine of real numbers. That's Part four, where you'll find every zed whose cosine is two.

## Scene 7 · Recap (ch1_s7_recap)

> A small "Recap" heading. Three panels in a row, one per sentence, each with its short line under it, built from the same objects, colours and styling as the scene it comes from:
> On {r1}: s2's averaging picture, small (GOLD e^x, PURPLE e^{−x}, the TEAL midpoint dot at x = 1, cosh and the lighter TEAL sinh). Line: "cosh, sinh: average and half-difference of e^x and e^{−x}".
> On {r2}: s3's family card, small (BLUE parents; TEAL tanh, sech, cosech, coth). Line: "tanh = sinh / cosh, and three reciprocals". On {r2b}: s3's RED card `\cosh^{-1} x \neq \frac{1}{\cosh x}` tucks in beside the sech row. Line: "sech is not the inverse".
> On {r3}: s6's dictionary card, small, its PINK i's pulsing on {extra}. Line: "an i turns cosine into cosh". On {r4}: the card's YELLOW header "for every complex x" pulses.
> On {next}: the panels slide up and dim. `\cos^2 x + \sin^2 x = 1` (BLUE) beside a small unit circle (the hook's). On {twin}: TEAL `\cosh^2 x \;\square\; \sinh^2 x = 1` with an empty YELLOW box for the sign. On {minus}: the box fills with a YELLOW minus, `\cosh^2 x - \sinh^2 x = 1`. On {hyp}: the hook's hyperbola x² − y² = 1 (TEAL) appears beside it, and the line "Part 2 · Identities and the sign flip".
> Then the end card, held about eight seconds after the last word (music carries it).

[c1.recap.1] {recap} Let's recap. {r1} Cosh is the average of E to the ex and E to the minus ex, and shine is half their difference. {r2} Tanch is shine over cosh, and the three reciprocals are one over cosh, one over shine, and one over tanch. {r2b} One over cosh is the hyperbolic secant, a different thing from the inverse of cosh.

[c1.recap.2] {r3} Putting an eye inside a cosine turns it into a cosh. {extra} For sine and tangent, an extra eye comes out in front. {r4} And this dictionary holds for every complex number, not only for real ones. {pause}

[c1.recap.3] {next} Next time, start from an identity you know well: cosine squared of ex, plus sine squared of ex, equals one. {twin} Cosh and shine have a twin of it, {minus} with the plus flipped to a minus. {hyp} And that minus sign is where the name hyperbolic comes from. {pause}
