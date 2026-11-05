# Chapter 7 · Impedance

NST IA Mathematics · Lecture 10 (Powers, Logarithms and Oscillations), part 7 of 8. Source: notes PDF pp. 28–29 (printed 109–110; Example 32, p. 29 blank, filled on the lecturer's scan pp. 11–12); recording 00:46:18–00:55:46 and the student question 00:56:12–00:56:28; Examples Sheet I, F1(h) and F3(d) (PDF pp. 6–7), answers PDF p. 15.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch7_s1_hook)

> Title card: "Powers, Logarithms and Oscillations", course line "NST IA Mathematics · Lecture 10", part line "Part 7 · Impedance"; it clears on {last}.
> {last}: a small copy of ch6 s4's shot: the GOLD arrow A e^{iωt} with the PURPLE velocity arrow a quarter turn ahead, and under it "d/dt  →  × iω" (the i PINK). It dims away on {today}.
> {task}: Example 32's header, as in the notes (p. 28): "Example 32: Impedance of AC circuit". {circuit}: the circuit draws in, as on p. 28 (the same drawing as ch6's closing shot): the source on the left (a circle with ∼, labelled V), the resistor zigzag R on the top wire, the capacitor C (two plates) on the right, the return wire along the bottom, and a GOLD arrow labelled I on the top wire. Small DIM dots (charge) drift along the wire, back and forth.
> {find}: the task, verbatim, under the circuit: "Find the complex resistance of a capacitor and resistor connected in series to an applied alternating voltage."
> {student}: the circuit slides left; a quote card on the right (transcript, 00:56:12): "I'm one of the computer scientists who also does this. Is it okay that I didn't understand any of that physics stuff?" {answer}: the reply under it: "Yes, yes, yes, that's absolutely fine." with a GREEN tick. {plan}: the card shrinks to a corner and fades.
> {ohm}: beside the resistor alone: "V = R I" (R BLUE, I GOLD). {question}: beside the whole circuit: "V = ? · I", the "?" in a YELLOW box. {complex}: the box gets a small PINK tag "complex". The circuit carries over into scene 2.

[c7.hook.1] {title} This is part seven, and it's about impedance. {last} Last time, you saw that differentiating an oscillation is easy in complex form. You just multiply its complex amplitude by eye omega. {today} Today, that trick solves a real problem.

[c7.hook.2] {task} This is Example thirty-two in the notes. {circuit} An alternating voltage drives a current through a resistor and a capacitor, connected in series, one after the other. {find} The task is to find the complex resistance of the pair.

[c7.hook.3] {student} At the very end of the lecture, a student said: I'm one of the computer scientists. Is it okay that I didn't understand any of that physics stuff? {answer} The lecturer's answer was yes, that's absolutely fine. {plan} So this chapter builds the little physics it needs from scratch. The maths is the point.

[c7.hook.4] {ohm} For a single resistor, the voltage is the resistance times the current. {question} Is there one number that does the same job for the whole circuit? {pause} {complex} There is, if you let it be complex.

## Scene 2 · The circuit and its four laws (ch7_s2_circuit)

> s1's circuit, large in the centre, gains the lecturer's labels (scan p. 11): "applied voltage V(t)" at the source {source}, "R resistance" over the resistor {resistor}, "capacitance C" at the capacitor {capacitor}, "current I(t)" on the GOLD arrow {current}. Each part lights as it's named.
> Colours, kept to the end of the chapter: the current GOLD; the resistor and everything of its own (V_R, V_{R0}) BLUE; the capacitor and everything of its own (V_C, V_{C0}) PINK, because it becomes Z's imaginary part in scene 5; the source voltage V in FG (white).
> Plain physics (ours): {push} a small label "voltage: the push"; {flow} charge dots stream past a DIM gate line on the wire, "current: charge per second"; {water} a tiny pipe sketch, a pressure gauge ("push") and flow arrows ("current"), then gone. {ac}: the source's ∼ wobbles and the GOLD current arrow shrinks, flips and regrows in rhythm; caption "ω: angular frequency of the source" (the scan says "angular velocity"; the course's name is angular frequency).
> Then the circuit shrinks to the left third and the four laws arrive on the right, one per beat, each lighting its part of the circuit (notation as on scan p. 11): {ohm} "Ohm's law:  V_R(t) = R I(t)" (the resistor glows); {store} "Q(t) = C V_C(t)", with + and − charges gathering on the two plates; {rate} "I = dQ/dt", with dots arriving at a plate; {loop} "V = V_R + V_C", with the loop traced once.
> {clash}: the laws dim; centre, "I" in GOLD ("the current") beside "i" in PINK ("√−1"), with a small RED sound wave between them ("same sound"). {j}: under them, small: "engineers write  j = √−1". {colours}: both settle into their colours. The four laws stay on screen into scene 3.

[c7.circuit.1] {circuit} Here's the circuit, as drawn in the notes. {source} On the left is the source, a circle with a wave inside. {resistor} Along the top is a resistor, with resistance R. {capacitor} On the right is a capacitor, with capacitance C. {current} And a current flows round the loop.

[c7.circuit.2] Now the physics, in plain words. {push} Voltage is a push. {flow} Current is the flow it causes, measured as the charge that passes a point each second. {water} Picture water in a pipe. Voltage is the pressure, and current is the flow. {ac} This source pushes one way, then the other, over and over, at angular frequency omega, like last chapter's pendulum.

[c7.circuit.3] The circuit obeys four laws, and you can take each one as given. {ohm} First, Ohm's law. The voltage across the resistor is R times the current. {store} Second, the capacitor stores charge, and the charge is C times the voltage across it. A bigger capacitor holds more charge for the same push.

[c7.circuit.4] {rate} Third, the current is the rate at which that charge arrives. That's the derivative of the charge with respect to time. {loop} Fourth, the voltages add up round the loop. The source's push is shared between the resistor and the capacitor. {pause}

[c7.circuit.5] {clash} One warning before the maths. The current is written as a capital eye, and the imaginary unit as a small eye. Out loud, they sound the same. {j} That's exactly why engineers write jay for the square root of minus one. {colours} Here, the current is always gold, and the imaginary unit is always pink.

## Scene 3 · Four amplitudes and three rules (ch7_s3_amplitudes)

> The small circuit and its four laws stay top-left. On the right, an Argand plane (ch1's helper: axes "Re" and "Im", DIM grid and unit circle).
> {settle}: "ω" appears beside the source. {linear}: the four laws flash their kinds in turn, small tags "sum", "constant multiple", "derivative" (V = V_R + V_C; V_R = R I and Q = C V_C; I = dQ/dt).
> {arrows}: four arrows from the origin, turning together anticlockwise at one steady rate with fixed angles between them, each casting a shadow dot on the real axis in its own colour (ch6 s3's arrow-and-shadow style): the current I₀ GOLD; V_{R0} BLUE, along the current; V_{C0} PINK, a quarter turn behind the current; V₀ FG, their sum, about 37° behind the current. Use the 3–4–5 shape (R = 4 and 1/(ωC) = 3 per unit of current: |Z| = 5, arg Z = −36.87°, checked); no numbers on screen. Scene 5 freezes these same arrows into its triangle.
> {forms}: the four lines, as on the lecturer's p. 12, each amplitude in its quantity's colour and the factor e^{iωt} in FG (GOLD means the current in this chapter):
> `V = Re(V₀ e^{iωt})` / `I = Re(I₀ e^{iωt})` / `V_R = Re(V_{R0} e^{iωt})` / `V_C = Re(V_{C0} e^{iωt})`, stacked. {vzero} lights V₀, {izero} lights I₀, {others} lights V_{R0} and V_{C0}.
> The three rules, the lecturer's bullets (scan p. 12), one per beat: {commute} "• Re and d/dt commute"; {cancel} "• e^{iωt} on two sides of eq → cancel"; {deriv} "• (e^{iωt})′ = iω e^{iωt}". A DIM "(83)" beside the first and third (ch6's equation).
> {why}: the second rule's reason (ours), on the plane: two arrows drawn on top of each other (one FG, one a dashed YELLOW outline). {t0} At t = 0 their shadows coincide: label "real parts equal". {quarter} Both step a quarter turn; the shadows coincide again: label "imaginary parts equal". {same} The two merge into one arrow. (Checked, sympy 1.14.0: Re[(A − B)e^{iωt}] = (a − c)cos ωt − (b − d)sin ωt for A = a + ib, B = c + id, so it vanishes for all t only when A = B.)
> {goal}: the scan's line, boxed in YELLOW: "Find Z:  V₀ = Z I₀". {ohm}: a small "V = R I" beside it maps onto it (V → V₀, R → Z, I → I₀). {name}: caption "Z: the complex impedance (the notes: complex resistance)".

[c7.amp.1] {settle} Once the circuit has settled, all four quantities oscillate at the source's angular frequency, omega. {linear} The lecturer calls it a linear system. Every law is a sum, a constant multiple, or a derivative, and none of those changes the frequency. {arrows} So each quantity is the shadow of its own turning arrow. All four arrows turn together, with fixed angles between them.

[c7.amp.2] {forms} In symbols, each quantity is the real part of its own complex amplitude, times E to the eye omega T. {vzero} The source's amplitude is called V zero, {izero} and the current's is called I zero. {others} The voltages across the resistor and the capacitor get amplitudes of their own.

[c7.amp.3] Three rules make these easy to handle. {commute} First, you can take the real part and the derivative in either order. You saw why last chapter. {cancel} Second, if the same turning factor appears on both sides of an equation, you can drop it. {deriv} Third, differentiating E to the eye omega T multiplies it by eye omega.

[c7.amp.4] {why} The second rule needs a reason. Suppose two turning arrows cast the same shadow at every moment. {t0} At time zero, the shadows are their real parts, so those match. {quarter} A quarter turn later, the shadows are minus their imaginary parts, so those match too. {same} So it's the same arrow, and the two amplitudes are equal. {pause}

[c7.amp.5] {goal} Now the goal. We want a number zed, with V zero equal to zed times I zero. {ohm} That's Ohm's law again, with amplitudes in place of the voltage and current, and a complex number in place of the resistance. {name} Zed is called the complex impedance. The notes call it the complex resistance.

## Scene 4 · Resistor and capacitor (ch7_s4_parts)

> Two columns under the shrunken circuit: the resistor (BLUE) on the left, the capacitor (PINK) on the right. The three rules sit small at the top right; each flashes YELLOW when it's used.
> Resistor, line by line (ours, between the scan's first and last lines): {law} `V_R = R I`; {sub} `Re(V_{R0} e^{iωt}) = R Re(I₀ e^{iωt}) = Re(R I₀ e^{iωt})`, R sliding inside the Re with the tag "R is real"; {drop} both e^{iωt} fade out (rule 2), leaving the scan's line {result} `V_{R0} = R I₀`. {along}: on s3's plane (small, below the column), the BLUE arrow lies along the GOLD current arrow, longer; as they turn, both shadows cross zero together.
> Capacitor: {rate} `I = dQ/dt = C dV_C/dt` ({const}: C slides out in front, tag "C is constant"); {swap} `Re(I₀ e^{iωt}) = C d/dt Re(V_{C0} e^{iωt})`, the d/dt moving inside the Re (rule 1); {iw} rule 3 turns it into `= Re(iωC V_{C0} e^{iωt})`, the iω dropping down from the exponent (i PINK); {drop} the e^{iωt} fade → `I₀ = iωC V_{C0}` (the scan's line).
> {solve}: `V_{C0} = I₀ / (iωC)` (the scan's line). {quarter}: on the small plane, the PINK capacitor arrow, and the GOLD current arrow a quarter turn ahead of it, with a YELLOW right-angle mark.
> {pendulum}: beside it, a small copy of ch6 s4's pair as it was (position arrow GOLD, velocity arrow PURPLE a quarter turn ahead), with mapping labels under the two pairs: "position → charge Q", "velocity → current I = dQ/dt". As the labels land, the copy recolours into this chapter's colours, so GOLD means only the current: the position arrow turns PINK (the charge Q = C V_C lies along V_{C0}) and the velocity arrow turns GOLD (the current). The two pairs then match exactly.
> {nocalc}: the "d/dt" in the capacitor's first line TransformFromCopy into "× iω" {deriv}; caption {algebra} "no calculus left". The two results `V_{R0} = R I₀` and `V_{C0} = I₀ / (iωC)` stay for scene 5.
> Checked (Python 3.11.9, sympy 1.14.0): R real moves inside Re; Re(iωC V_{C0} e^{iωt}) = C d/dt Re(V_{C0} e^{iωt}); with R = 5, C = 0.01, ω = 30, the current arrow is exactly 90° ahead of V_{C0}, and I = C dV_C/dt holds at 50 sample times.

[c7.parts.1] Start with the resistor. {law} Ohm's law says its voltage is R times the current. {sub} Write each side as a real part. R is a real number, so it can move inside. {drop} The same turning factor is now on both sides, so drop it. {result} The resistor's amplitude is R times the current amplitude. {along} Its arrow points the same way as the current's, so the two rise and fall in step.

[c7.parts.2] Now the capacitor. {rate} The current is the rate of change of the charge, and the charge is C times the capacitor's voltage. {const} C is a constant, so it comes out in front of the derivative. {swap} Write both sides as real parts, and let the derivative act on the turning factor. {iw} It brings down eye omega. {drop} Drop the turning factor, and the current amplitude is eye omega C, times the capacitor's amplitude.

[c7.parts.3] {solve} Divide, and the capacitor's amplitude is the current amplitude, over eye omega C. {quarter} Multiplying by eye turns an arrow a quarter turn ahead. So the current's arrow runs a quarter turn ahead of the capacitor's. {pendulum} That's last chapter's picture again. The charge plays the position, and the current plays the velocity. {pause}

[c7.parts.4] {nocalc} Look at what just happened. {deriv} In the capacitor's law, a derivative turned into a multiplication by eye omega. {algebra} Both laws are now plain algebra between complex numbers, the amplitudes. There's no calculus left, and time has dropped out completely.

## Scene 5 · Z (ch7_s5_impedance)

> s4's two results top-left. {loop}: the scan's "Since V = V_R + V_C ⇒"; {amps}: it becomes `V₀ = V_{R0} + V_{C0}` (rule 2 flashes). {fill}: TransformFromCopy s4's results into the slots: `V₀ = R I₀ + I₀ / (iωC)`. {factor}: I₀ pulls out: `V₀ = (R + 1/(iωC)) I₀`. {z}: an underbrace on the bracket, labelled "Z  complex resistance" (as on scan p. 12).
> {clear}: small `1/i = −i`, with `i · (−i) = 1` under it. {box}: `Z = R − i/(ωC)`, boxed in YELLOW as the lecturer boxed it. {parts}: R in BLUE, labelled "real part: the resistor"; −1/(ωC) in PINK, labelled "imaginary part: the capacitor, negative".
> {triangle}: s3's plane and arrows return, frozen: the BLUE arrow V_{R0} along the GOLD current; the PINK V_{C0} slides tip to tail onto its end, pointing a quarter turn behind the current; the FG arrow V₀ closes the right triangle {sum}; its legs are R|I₀| (BLUE) and |I₀|/(ωC) (PINK), the same shape as Z's real and imaginary parts. {size}: `|I₀| = |V₀| / |Z|` in FG (GOLD means the current here). {lag}: a YELLOW arc from the current arrow back to V₀, labelled "arg Z < 0"; the triangle turns once as a whole, V₀ reaching each angle after I₀; caption "the voltage lags the current".
> After {lag}, the triangle clears to Z as a YELLOW dot on the plane at R − i/(ωC), with a BLUE leg R along the real axis and a PINK leg 1/(ωC) straight down; an ω slider. {low}: ω slides small and the dot runs far down the vertical line Re Z = R, caption "low ω: |Z| huge, almost no current". {high}: ω slides large and the dot rises to R on the real axis, caption "high ω: Z ≈ R". (Checked: R = 5, C = 0.01 gives 5 − 10000i at ω = 0.01 and 5 − 0.01i at ω = 10⁴.)
> {sheet}: the sheet's expression, as printed in F1(h) and F3(d): e^{iωt} / (R + iωL + (iωC)^{−1}), tagged "Examples Sheet I, F1(h) and F3(d)". {inductor}: the iωL term lights, with a small coil symbol and the tag "inductor L"; under it "answers: end of the sheet".
> {summary}: two columns. Left, DIM with a RED cross: "sines and cosines: equate, differentiate, equate again". {exp} Right, with a GREEN tick: "exponentials: equate amplitudes;  d/dt → × iω".
> Checked (Python 3.11.9, sympy 1.14.0): R + 1/(iωC) = R − i/(ωC) and 1/i = −i symbolically; for R = 5, C = 0.01, ω = 30 the amplitudes satisfy V = V_R + V_C at 50 sample times, Z = 5 − 3.333i, arg Z = −33.69° = arg V₀ − arg I₀ (the voltage lags); the sheet's printed answers to F1(h) and F3(d) (PDF p. 15, with X ≡ ωL − 1/(ωC)) match e^{iωt}/(R + iωL + (iωC)^{−1}) at six (ω, t) pairs.

[c7.imp.1] {loop} Now the fourth law. The voltages add up round the loop. {amps} Write each one as a real part, drop the turning factor, and the amplitudes add up the same way. {fill} Put in the two results you just found. {factor} The current amplitude is a common factor. {z} So the source's amplitude is R, plus one over eye omega C, all times the current amplitude. That bracket is zed. {pause}

[c7.imp.2] {clear} One last step clears the eye from the bottom. One over eye is minus eye, because eye times minus eye is one. {box} So zed equals R, minus eye over omega C. {parts} Its real part is the resistance. Its imaginary part comes from the capacitor, and it's negative. {pause}

[c7.imp.3] What does zed tell you? {triangle} Put the two voltage arrows tip to tail. The resistor's lies along the current, and the capacitor's is a quarter turn behind, so they meet at a right angle. {sum} Their sum is the source's arrow, the long side of a right triangle.

[c7.imp.4] {size} The modulus of zed sets how much current flows. Divide the size of the voltage by mod zed, and you get the size of the current. {lag} The argument of zed is negative, so the voltage arrow trails the current's. The voltage lags the current. {pause}

[c7.imp.5] {low} At low frequency, one over omega C is huge, so almost no current flows. A capacitor blocks a steady current. {high} At high frequency, that term shrinks towards zero, and zed is almost just R. {sheet} Two basic skills questions on the examples sheet, F one, part H, and F three, part D, use R, plus eye omega L, plus one over eye omega C. {inductor} The extra term comes from an inductor, a coil of wire. Their answers are at the end of the sheet.

[c7.imp.6] {summary} The lecturer summed it up like this. With sines and cosines, this problem means equating coefficients, differentiating, and equating them again. {exp} With exponentials, it comes down to equating amplitudes, and multiplying by eye omega wherever there's a derivative.

## Scene 6 · Recap, the lecture, and next time (ch7_s6_recap)

> Recap: four small panels in a 2×2 grid, one per sentence, each a shrunken copy of the shot that taught it (same objects, same colours), with its short line under it:
> {r1} s2's circuit beside its four laws, "four laws: two parts, the current, the loop"; {r2} s3's four arrows turning together with their shadows, "every quantity: a turning arrow"; {r3} s4's "d/dt → × iω" with the GOLD-ahead-of-PINK quarter-turn pair, "derivatives become × iω"; {r4} s5's boxed `Z = R − i/(ωC)` with its triangle, "one complex resistance".
> {lecture}: the grid clears; two rows of thumbnails, the lecture in one picture. {thread1}: the TEAL row "the 2πn": ch1 s5's ring of five, ch4 s4's ladder for ln 2i, ch5 s7's gallery, tagged "Parts 1, 4, 5". {thread2}: the GOLD row "the turning arrow": ch2 s2's arrow stepping θ, 2θ, 3θ; ch3 s3's curling chain with its shadow; ch6 s3's arrow and shadow; this chapter's four arrows; tagged "Parts 2, 3, 6, 7".
> {next}: the rows clear to "Lecture 11". {cosh}: `½(e^x + e^{−x}) = cosh x`, e^x GOLD and e^{−x} PURPLE (L11's colours). {bonus}: a card "Part 8 · Solutions (bonus): F12, F13, F15–F19".
> End card after the last word: hold about 8 s while the music carries it.

[c7.recap.1] {recap} Let's recap. {r1} The circuit obeys four laws: one for each part, one for the current, and one for the loop. {r2} Every quantity is the shadow of a turning arrow, and the arrows all turn together. {r3} A derivative becomes a multiplication by eye omega, so the laws become algebra. {r4} And the whole circuit acts like one complex resistance: zed equals R, minus eye over omega C.

[c7.recap.2] {lecture} That's the end of the lecture, and it ran on two threads. {thread1} The two pi N gave roots, logarithms and powers their many values. {thread2} The turning arrow gave De Moivre's theorem, the sums of cosines, oscillations, and circuits. {pause}

[c7.recap.3] {next} Next time, in Lecture eleven, the exponent turns real instead of imaginary. {cosh} E to the ex, plus E to the minus ex, all over two, is the hyperbolic cosine. {bonus} And Part eight has full solutions to this lecture's exercises. {pause=1.5}
