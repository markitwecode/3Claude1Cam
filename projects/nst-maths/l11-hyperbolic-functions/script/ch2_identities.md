# Chapter 2 · Identities and the sign flip

NST IA Mathematics, Lecture 11 (Hyperbolic Functions and Conics), part 2 of 7. Source: Berloff's notes, Chapter234_to_annotate.pdf pp. 33–34 (§3.2, (93)–(95), the boxed rule, Example 33); lecture 08:10–13:00 (11:02–11:44 is a camera refocus); Examples Sheet I, G1 (p. 9).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card: "Hyperbolic Functions and Conics", "NST IA Mathematics · Lecture 11", "Part 2 · Identities and the sign flip".
> On {dict}, ch1's dictionary card returns, in ch1 s6's exact styling: `cos(ix) = cosh x`, `sin(ix) = i sinh x`, `tan(ix) = i tanh x`, circular side BLUE, hyperbolic side TEAL, every i PINK. It then shrinks into the top-right corner, where ch1 s4–s5 kept it, and stays there for the whole chapter (scenes 3 and 6 pull from it).
> On {circle}, centre left: a BLUE unit circle with a point at angle θ, its right triangle drawn in (legs cos θ and sin θ, hypotenuse 1). Beside it `cos² x + sin² x ≡ 1` (BLUE). On {triangle}, the legs and hypotenuse flash.
> On {twin}, below it the twin promised at the end of ch1: `cosh² x − sinh² x ≡ 1` (TEAL), its minus YELLOW. On {ask}, a YELLOW "?" lands over that minus: the question as an object.
> On {doors}, two labelled panels open under the question. On {expand}, left: "expand the definitions", holding `½(e^x + e^{−x})` with e^x GOLD and e^{−x} PURPLE. On {door}, right: "through the complex door", holding a PINK i and a thumbnail of the dictionary card.
> On {rule}, everything else dims; a BLUE card "trig identity" on the left, an arrow labelled "one rule?" (YELLOW), and an empty TEAL card "hyperbolic twin" on the right.

[c2.hook.1] {title} Welcome back. This is part two, on identities and the sign flip. {dict} Last time, we found that putting an eye inside a cosine turns it into a cosh. The cosine of eye ex is cosh of ex, and the sine of eye ex is eye times shine of ex. {pause}

[c2.hook.2] {circle} Now, trigonometry is full of identities. The most famous one says cosine squared, plus sine squared, equals one. {triangle} It's Pythagoras, on a circle of radius one. {twin} Cosh and shine have a twin of it, with a minus sign. {ask} But where does that minus come from? {pause} {doors} There are two ways to find out. {expand} You can expand the definitions, in exponentials. {door} Or you can go through the complex door, with the dictionary.

[c2.hook.3] {both} In this chapter, we'll take both routes, and watch what changes. {rule} Then we'll ask a bigger question. Is there one simple rule that turns every trig identity into its hyperbolic twin? {pause}

## Scene 2 · cosh² − sinh² = 1 (ch2_s2_pythag)

> Top: (84) `cosh x = ½(e^x + e^{−x})` and (85) `sinh x = ½(e^x − e^{−x})`, styled as in ch1 s2: e^x GOLD, e^{−x} PURPLE, cosh and sinh TEAL. On {sinh}, the middle minus of (85) flashes YELLOW.
> Below them, the notes' derivation (p. 33), built line by line. On {square}: `cosh² x − sinh² x = ¼(e^x + e^{−x})² − ¼(e^x − e^{−x})²`, each bracket copied out of (84) and (85) (TransformFromCopy); on {quarter}, each ½ squares into ¼.
> On {expand}..{second}: `= ¼[(e^{2x} + 2 + e^{−2x}) − (e^{2x} − 2 + e^{−2x})]`. On {ends}, the GOLD e^{2x} and PURPLE e^{−2x} grow out of the squared terms. On {middle}, a small aside: `2 · e^x · e^{−x} = 2 · e^0 = 2`, the 2 in GOLD. On {second}, the second bracket's −2 flashes YELLOW.
> On {cancel}: the two e^{2x} strike through together, then the two e^{−2x}. On {four}: the +2 and the −(−2) (inner minus YELLOW) merge into 4, and ¼ · 4 → `= 1`.
> On {result}: (93) `cosh² x − sinh² x ≡ 1`, boxed (YELLOW box). On {identity}, the ≡ flashes, label under it: "identity: true for every x".
> Clear the working. On {compare}: the boxed (93) slides right; `cos² x + sin² x ≡ 1` (BLUE) appears on the left at the same height. On {plus} and {minus}, each sign lights YELLOW in turn. A handwriting-style margin note beside (93), as the lecturer wrote: "comp. sin²θ + cos²θ = 1".
> Every expansion here checked with sympy 1.14.0.
> On {curve}: the identities move up; below, ch1's circle–hyperbola pair. Left, a BLUE unit circle labelled `x² + y² = 1`, a point `(cos θ, sin θ)` running round it. On {hyper}, right: the TEAL hyperbola `x² − y² = 1` (both branches; faint dashed asymptotes y = ±x), a point `(cosh θ, sinh θ)` running along the right branch. On {name}, the label "hyperbola" and a small tag "part 6".

[c2.pythag.1] {defs} Let's take the first route, starting from the definitions. {cosh} Cosh of ex is E to the ex, plus E to the minus ex, all over two. {sinh} Shine of ex is the same, with a minus in the middle. {square} We want cosh squared, minus shine squared, so square each one. {quarter} Squaring the half puts a quarter in front of each bracket.

[c2.pythag.2] {expand} Now expand the brackets. {ends} E to the ex, squared, is E to the two ex. And E to the minus ex, squared, is E to the minus two ex. {middle} The middle term is twice E to the ex, times E to the minus ex. Their exponents cancel, so that product is one, and the middle term is just two. {second} The second bracket is the same, except that its middle term is minus two. {pause}

[c2.pythag.3] {subtract} Now subtract. {cancel} The E to the two ex terms cancel, and so do the E to the minus two ex terms. {four} All that's left is two, minus the minus two. That makes four, and a quarter of four is one. {result} So cosh squared, minus shine squared, equals one. {pause} {identity} The notes write it with three bars instead of two, to say it's an identity, true for every value of ex.

[c2.pythag.4] {compare} Put it beside the circle identity. {plus} Cosine squared plus sine squared equals one. {minus} Cosh squared, minus shine squared, equals one. Same shape, but the plus has become a minus. {pause} {curve} Here's a picture of what that means. The point with coordinates cosine theta and sine theta runs round the circle, ex squared plus why squared equals one. {hyper} The point with coordinates cosh theta and shine theta runs along a different curve, ex squared minus why squared equals one. {name} That curve is a hyperbola. It's a first hint of where the name hyperbolic comes from, and part six tells the full story.

## Scene 3 · cosh(A + B) through the complex door (ch2_s3_addition)

> The dictionary card stays in the top-right corner (from scene 1); keep the hero formulas clear of it.
> Hero, centred high: (94) `cos(A + B) ≡ cos A cos B − sin A sin B` (BLUE; A and B YELLOW as names). On {complex}, a caption under it: "true for all complex A and B". On {why}, a small aside: `cos z = ½(e^{iz} + e^{−iz})`, `e^{a+b} = e^a e^b` "for complex numbers too".
> On {sub}, PINK i's drop in front of every A and B: the notes' line `cos(iA + iB) ≡ cos iA cos iB − sin iA sin iB`.
> On {left}, the left side's `iA + iB` regroups into `i(A + B)`. On {dictleft}, an arrow from the card's first row turns `cos(i(A + B))` into `cosh(A + B)` (TEAL).
> On {cos}, `cos iA cos iB` becomes `cosh A cosh B` (each factor TransformFromCopy from the card's first row).
> On {each}, `sin iA` → `i sinh A` and `sin iB` → `i sinh B` (from the card's second row; i PINK). On {product}, the two PINK i's slide together into `i²`. The notes' line is now complete: `cos(iA + iB) ≡ cosh(A + B) ≡ cosh A cosh B − i² sinh A sinh B`. On {isq}, `i² = −1` drops in beside it (YELLOW).
> On {minus}, the minus in front of `i²` lights YELLOW; on {times}, `−i²` → `−(−1)`; on {plus}, the two minuses fuse and turn into a YELLOW `+`.
> On {result}: `cosh(A + B) ≡ cosh A cosh B + sinh A sinh B` (TEAL), boxed. On {compare}, (94) slides in above it, row to row, the − in (94) and the + in the result both YELLOW; caption, the lecturer's words: "minus sign is replaced with a plus sign". Both notes lines checked with sympy 1.14.0 for complex A and B.

[c2.add.1] {door} Now the second route, through the complex door. {start} Start with the addition formula for cosine. {formula} The cosine of the sum, A, plus B, equals cosine of A, times cosine of B, minus sine of A, times sine of B. {complex} You probably met it for real angles, but it holds for any complex numbers, A, and B. {why} That's because it follows from the exponential forms of cosine and sine, and the rules for exponents work for complex numbers too.

[c2.add.2] {sub} So we're allowed to put in eye A, and eye B. {left} On the left, take out the common factor of eye. {dictleft} By the dictionary, the cosine of eye times the sum is the cosh of the sum. {cos} On the right, the cosine of eye A, turns into cosh of A, and the cosine of eye B, into cosh of B.

[c2.add.3] {sines} Now the interesting part, the two sines. {each} The sine of eye A, turns into eye, times the shine of A, and the sine of eye B, into eye, times the shine of B. {product} Multiply them, and the two eyes make eye squared. {pause} {isq} And eye squared is minus one.

[c2.add.4] {sign} So look at the sign in front of that term. {minus} The cosine formula had a minus. {times} Now we have minus, times eye squared, so minus, times minus one. {plus} That's a plus. {result} So the cosh of the sum, A, plus B, equals cosh of A, times cosh of B, plus shine of A, times shine of B. {pause} {compare} It's the same shape as the cosine formula. But, as the lecturer put it, the minus sign is replaced with a plus sign.

## Scene 4 · The whole family (ch2_s4_list)

> Two columns, aligned row by row: the trig parents on the left (BLUE), the notes' list (95) on the right (TEAL), verbatim from p. 34:
> `cosh(A + B) ≡ cosh A cosh B + sinh A sinh B` / `cosh(A − B) ≡ cosh A cosh B − sinh A sinh B` / `sinh(A + B) ≡ sinh A cosh B + sinh B cosh A` / `sinh(A − B) ≡ sinh A cosh B − sinh B cosh A` / `1 − tanh² z ≡ sech² z` / `coth² z − 1 ≡ cosech² z`.
> Parents, same order: `cos(A + B) = cos A cos B − sin A sin B` / `cos(A − B) = cos A cos B + sin A sin B` / `sin(A + B) = sin A cos B + sin B cos A` / `sin(A − B) = sin A cos B − sin B cos A` / `1 + tan² z = sec² z` / `cot² z + 1 = cosec² z`. Each row pair appears on its mark; every sign that differs from its parent turns YELLOW.
> On {first}, row 1 arrives from scene 3's box (same object, moved). On {minusB}, row 2, its − YELLOW.
> On {sinh}, row 3; on {nochange}, a small GREEN "no change" tag on rows 3–4. On {why}, a side box: `sin(iA + iB) = i sinh A cosh B + cosh A · i sinh B` with one PINK i per term, and on the left `sin(i(A + B)) = i sinh(A + B)`. On {cancel}, the i's strike out on both sides; no i² ever forms. On {diff}, row 4.
> On {squares}, scene 2's boxed (93) returns small, beside the list. On {divcosh}, "÷ cosh²" under it; on {terms}, its three terms turn into `1`, `tanh²`, `sech²` one by one, and on {res} slide into row 5 (its − YELLOW). On {divsinh}, "÷ sinh²" instead: `coth²`, `1`, `cosech²`, sliding into row 6.
> All twelve lines checked with sympy 1.14.0 (exponential form, complex A and B, plus cmath spot checks).
> The finished two-column list stays as one object: scene 5 reuses rows 1 and 5, scene 6 rows 1 and 3.

[c2.list.1] {family} The same door works for every identity in the family. {list} Here they are, each beside its trig parent, with the changed signs in yellow. {first} The first line is the one we just derived. {minusB} Swap the sum for a difference, A, minus B, and the plus in the answer becomes a minus. Again, it's the opposite of the cosine formula.

[c2.list.2] {sinh} Now the shine of a sum. {same} Shine of the sum equals shine of A, times cosh of B, plus shine of B, times cosh of A. {nochange} Here, no sign changes at all. {why} Through the door, each term on the right has just one sine, so it picks up just one eye. {cancel} That eye cancels the eye on the left, and nothing is ever squared. {diff} Shine of the difference works the same way. {pause}

[c2.list.3] {squares} The last two lines come straight from the identity, cosh squared, minus shine squared, equals one. {divcosh} Divide every term by cosh squared. {terms} Cosh squared over cosh squared is one. Shine squared over cosh squared gives tanch squared. And one over cosh squared is the hyperbolic secant, squared. {res} So one, minus tanch squared, equals hyperbolic secant squared. {divsinh} Divide by shine squared instead, and you get hyperbolic cotangent squared, minus one, equals hyperbolic cosecant squared. {pause}

## Scene 5 · The sign-flip rule (ch2_s5_rule)

> The notes' boxed rule (p. 34), verbatim, in a grey-bordered box across the top: "The basic pattern is that to get the hyperbolic identity you simply take the corresponding circular trigonometric identity, replace 'cos' by 'cosh', 'sin' by 'sinh' etc., and then wherever there is a product of two 'sinh' functions (also implied, as in tanh²), change the sign."
> On {rename}, highlight "replace 'cos' by 'cosh', 'sin' by 'sinh' etc."; on {flip}, highlight "wherever there is a product of two 'sinh' functions … change the sign" (YELLOW). On {name}, a small caption under the box: "usually called Osborn's rule (the name is not in the notes)".
> The box shrinks to a strip at the top. Under it, a two-step machine: "1 · rename" (BLUE → TEAL) and "2 · flip the sign of every sinh × sinh" (YELLOW).
> Test 1, on {test}: `cos² x + sin² x ≡ 1` (BLUE) goes in. On {cos2}, cos² → cosh². On {sin2}, sin² → sinh², which unfolds into `sinh x · sinh x`, outlined YELLOW. On {flipped}, its + flips to −: `cosh² x − sinh² x ≡ 1`. On {check}, scene 2's boxed (93) slides in next to it, GREEN tick.
> Test 2, on {tan2}: `1 + tan² z ≡ sec² z`. On {unfold}, after renaming, tanh² z unfolds into `sinh² z / cosh² z`, the sinh² outlined YELLOW. On {flips}, the + flips: `1 − tanh² z ≡ sech² z`; on {result}, row 5 of scene 4's list flies in to match, GREEN tick. On {secant}, `sec² z = 1 / cos² z` with "no sin" (no flip).
> Prediction, on {predict}: `tan(A + B) = (tan A + tan B) / (1 − tan A tan B)` (BLUE). On {top}, the numerator lights; on {bottom}, the denominator. On {hide}, after renaming, `tanh A tanh B` unfolds into `sinh A sinh B / (cosh A cosh B)`, outlined YELLOW. On {flipdown}, the denominator's − flips to a YELLOW +.
> On {guess}: `tanh(A + B) = (tanh A + tanh B) / (1 + tanh A tanh B)` with a YELLOW "prediction?" tag (scene 6 proves it). On {aid}, caption: "memory aid, not a proof". The tan(A + B) parent and the predicted tanh formula checked with sympy 1.14.0.

[c2.rule.1] {pattern} By now you can see a pattern, and the notes put it in a box. {take} Take any trig identity. {rename} Replace cosine by cosh, sine by shine, and so on. {flip} Then, wherever two shines are multiplied together, change the sign. {pause} {name} This is often called Osborn's rule.

[c2.rule.2] {test} Let's test it on the circle identity. {cos2} Cosine squared becomes cosh squared. {sin2} Sine squared becomes shine squared, which is shine times shine, a product of two shines. {flipped} So its sign flips, and we get cosh squared minus shine squared equals one. {check} That's exactly what we found by expanding. {pause}

[c2.rule.3] {hidden} The catch is that the product can be hidden. {tan2} Take one plus tangent squared equals secant squared. {unfold} Tanch squared is shine squared over cosh squared, so there's a shine times shine inside it. {flips} Its sign flips, {result} and we get one minus tanch squared equals hyperbolic secant squared, the line from the family list. {secant} Secant squared is one over cosine squared. There's no sine in it, so it keeps its sign.

[c2.rule.4] {predict} Now let's use the rule to predict something new, the tangent of the sum, A, plus B. {top} On top, tangent of A, plus tangent of B. {bottom} Underneath, one, minus tangent of A, times tangent of B. {hide} Once it's renamed, that product hides shine of A, times shine of B, {flipdown} so the minus underneath flips to a plus. {guess} The prediction has the same top, with tanch in place of tangent, and a plus underneath. {pause} {aid} But a rule like this is a memory aid, not a proof. To be sure, we derive it.

## Scene 6 · Example 33: tanh(A + B) (ch2_s6_tanh)

> A green-bordered card, as in the notes (p. 34): "Example 33: Identity for hyperbolic tangent" / "Find an identity for tanh(A + B)." Then the notes' line "Recall that sin(iz) = i sinh z and cos(iz) = cosh z." copies out of the dictionary card in the corner (TransformFromCopy).
> The notes' chain, verbatim, one line per beat (the chain is tall: keep at most three lines on screen, scrolling up; the i's the notes print in red are PINK here):
> On {start}: `tanh(A + B) = sinh(A + B) / cosh(A + B)`. On {times}: `= i sinh(A + B) / (i cosh(A + B))`, both PINK i's dropping in together. On {top}/{bottom}: `= sin(iA + iB) / (i cos(iA + iB))`, the numerator and then the denominator turning over.
> On {expand}: `= [sin(iA)cos(iB) + cos(iA)sin(iB)] / (i[cos(iA)cos(iB) − sin(iA)sin(iB)])`. On {dict}: `= [i sinh(A)cosh(B) + cosh(A) i sinh(B)] / (i[cosh(A)cosh(B) + (−i²)sinh(A)sinh(B)])`; on {numi}, the two PINK i's in the numerator flash; on {denom}, `(−i²)` → `+1` (YELLOW).
> On {cancel}: the i in each numerator term and the i in front of the bracket underneath strike out together. On {real}: `= [sinh(A)cosh(B) + cosh(A)sinh(B)] / [cosh(A)cosh(B) + sinh(A)sinh(B)]`, all TEAL, no PINK left.
> On {divide}: the notes' "Divide through by cosh(A)cosh(B)"; each of the four terms gets a small `÷ cosh A cosh B`. On {ratio}, `sinh(A)cosh(B)` → `tanh(A)` and `cosh(A)sinh(B)` → `tanh(B)`; on {one}, `cosh(A)cosh(B)` → `1`, and the last term → `tanh(A)tanh(B)`.
> On {answer}: `tanh(A + B) = [tanh(A) + tanh(B)] / [1 + tanh(A)tanh(B)]`, boxed. On {match}, scene 5's prediction slides in beside it and its "prediction?" tag becomes a GREEN tick.
> Clip 4, the lecturer's shortcut: on {family}, rows 3 and 1 of scene 4's list fly in as numerator and denominator of `sinh(A + B) / cosh(A + B)`; on {same}, they land on the same real fraction as {real} (GREEN "same"). On {again}, the same division, the same box.
> Every line of the chain checked with sympy 1.14.0 (each equals tanh(A + B) for complex A and B).
> On {sheet}: the G1 card, verbatim from Examples Sheet I: "G1. Express tanh(x + y) in terms of tanh x and tanh y.", with A ↦ x and B ↦ y written under it. A small tag "part 7: a third route".

[c2.tanh.1] {example} So here's Example thirty-three in the notes. {find} Find an identity for the hyperbolic tangent of the sum, A, plus B. {start} Start from the definition, shine over cosh. {times} Then multiply the top and the bottom by eye. That changes nothing, {why} but eye times shine is exactly what the dictionary turns into a sine. {top} So the top becomes the sine of the sum, eye A, plus eye B. {bottom} And the bottom becomes eye, times the cosine of that same sum.

[c2.tanh.2] {expand} Expand both with the trig addition formulas, {dict} then translate each piece back with the dictionary. {numi} On top, each term picks up a single eye. {denom} Underneath, the product of the two sines gives minus eye squared, which is plus one. {pause} {cancel} So every term on top has an eye, and so does the bottom, in front of its bracket. The eyes cancel. {real} What's left is all real. On top, shine of A, times cosh of B, plus cosh of A, times shine of B. Underneath, cosh of A, times cosh of B, plus shine of A, times shine of B.

[c2.tanh.3] {divide} The last step is to divide the top and the bottom by cosh of A, times cosh of B. {ratio} Each shine, over its own cosh, turns into a hyperbolic tangent, {one} and the first term underneath becomes one. {answer} So the hyperbolic tangent of the sum has tanch of A, plus tanch of B, on top. And underneath, it has one, plus tanch of A, times tanch of B. {pause} {match} That's exactly what the sign-flip rule predicted.

[c2.tanh.4] {short} In the lecture, there was also a shortcut. {family} We already have the shine and the cosh of the sum in the family list. {write} Write their ratio straight down, {same} and you land on the same real fraction, without a single eye. {again} Then divide through by cosh of A, times cosh of B, as before. {pause} {sheet} This is question G one on the examples sheet, with ex and why in place of A, and B. Part seven finds a third way, using the exponentials.

## Scene 7 · Recap (ch2_s7_recap)

> Four small panels (2 × 2), each a miniature of the visual that taught it, same objects and colours, with its sentence's short line under it; each lights on its mark while the others dim.
> On {r1}, from scene 2: the cancelling GOLD e^{2x} and PURPLE e^{−2x}, the boxed `cosh² x − sinh² x ≡ 1`, and the tiny circle and hyperbola pair. Line: "cosh² − sinh² = 1".
> On {r2}, from scene 3: `i sinh A · i sinh B` → `i²` → `−1`, the minus turning into a YELLOW plus (PINK i's). Line: "through the complex door".
> On {r3}, from scenes 4 and 5: two rows of the side-by-side list with YELLOW signs, and tanh² unfolding into sinh² / cosh². Line: "flip on sinh × sinh, hidden ones too".
> On {r4}, from scene 6: the boxed `tanh(A + B) = (tanh A + tanh B) / (1 + tanh A tanh B)` with its GREEN tick, the YELLOW + underneath. Line: "tanh(A + B)".
> On {next}, the panels clear; cosh, sinh and tanh appear small in TEAL on ch1 s2's axes, with the dashed GOLD ½e^x guide. On {undo}, a dashed mirror line y = x and a YELLOW "?"; on {logs}, the word "log" fades in beside it.
> End card: hold for about eight seconds after the last word; the music carries it.

[c2.recap.1] {recap} Let's recap. {r1} Expanding the definitions gives cosh squared minus shine squared equals one, the circle identity with a minus. {r2} Through the complex door, eye times eye is minus one, and that flips a sign. {r3} So to convert a trig identity, rename the functions, and flip the sign of every product of two shines, hidden ones included. {r4} And tanch of the sum has a plus underneath, where the tangent formula has a minus. {pause}

[c2.recap.2] {next} Next time, we'll draw the graphs of cosh, shine and tanch, {undo} and learn how to run them backwards. {logs} The answers turn out to be logarithms. {pause}
