# Chapter 6 · Electricity, from charge to Kirchhoff

Digital Electronics, Lecture 11 (State Minimisation, Programmable Logic and Circuits), part 6 of 6. Source: slides `combined_26.pdf` pp. 163–170 (through the KVL equation; p. 170's last bullet, the potential divider, is the next-lecture teaser); recording 00:44:41–00:59:57 (it ends while KVL is being explained; the walk round the loop is completed from the slide).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch6_s1_hook)

> Title card on {title}: "State Minimisation, Programmable Logic and Circuits" (scaled to 12 units wide, as in ch1 s1), "Digital Electronics · Lecture 11", "Part 6 · Electricity, from charge to Kirchhoff"; it clears on {last}. No code on screen. Every number in this chapter was checked in Python 3.11.9 (standard library, exact fractions). Electronics colours, new here and kept by Lecture 12: electrons BLUE dots with "−"; fixed positive ions DIM circles with "+"; conventional-current arrows GOLD; voltage arrows (emf and pd) TEAL; battery, lamp and resistor symbols FG; a lit lamp glows YELLOW; numbers GOLD, except a voltage's value, which sits by its TEAL arrow in TEAL. Symbols as on pp. 165–170: I, Q, t, E, V, P, R, V_B, V_L, P_L; units C, A, V, J, W, Ω.
> {last}: ch5 s2's FPGA array, small (TEAL CLB outlines, PURPLE switch matrices, DIM input-output blocks). {gates}: the camera dives into one CLB; its lookup table opens into a handful of FG logic gates. {transistors}: one gate turns translucent, with a DIM silhouette of transistors inside (no detail: that's Lecture 12). {turn}: everything slides away, and p. 163's section title writes on: "Electronics, Devices and Circuits", subtitle "Underlying Concepts".
> {road}: p. 164's road as two stops joined by an arrow. {concepts}: stop 1, "Underlying concepts", with three small tags, "electrical circuits", "circuit theory", "materials". {gatesnext}: stop 2, "Transistors → gates". {today}: a YELLOW "you are here" marker on stop 1, with "charge → … → Kirchhoff" under it.
> {wire}: back to one gate (the one from {gates}) driving a long FG output wire; its output flips 0 → 1 (GREEN, the course's output colour). {question}: zoom toward the wire, a YELLOW "?" inside it. {measure}: a GOLD "how much?" beside the "?". The wire carries straight into s2's opening shot.

[c6.hook.1] {title} This is part six of lecture eleven, and the last part. {last} Last time, we looked inside an F-P-G-A, a grid of logic blocks built from lookup tables, multiplexers and flip-flops. {gates} Every one of those parts is made of gates, {transistors} and every gate is made of transistors. {turn} So now the course turns a corner, to electronics, devices and circuits.

[c6.hook.2] {road} The slides set out the road ahead. {concepts} First come the underlying concepts, which are electrical circuits, circuit theory and materials. {gatesnext} Then how transistors work, and how logic gates are built from them. {today} Today we make a start, from electric charge all the way to Kirchhoff's two laws.

[c6.hook.3] {wire} So here's the question for this chapter. {question} When a gate's output changes, and a wire carries the new value, what is actually moving in that wire? {pause} {measure} And how do we measure it? {pause}

## Scene 2 · Electrons in a metal (ch6_s2_electrons)

> Continues from s1's wire. {current}: a short wire segment with BLUE "−" dots all moving one way, label "current: charged particles moving in a definite direction" (p. 164). {metals}: tag "metals: electrons". {gases}: a small side panel, a jar of gas, with BLUE "−" dots and a few larger DIM "+" ions wandering; tag "gas or liquid: electrons and ions". {focus}: the panel clears.
> {lattice}: zoom into the wire: a regular grid of DIM "+" ion circles. {loose}: BLUE "−" electrons peel off the ions and roam between them. {random}: every electron jitters on its own random path, fast (seeded random walk). {nonet}: a dashed checkpoint line across the wire with two GOLD counters, "→" and "←", ticking up at the same rate; under them "no net flow of charge", "no current".
> {battery}: zoom out: the wire bends into p. 165's loop, a battery on the left side ("+" and the long plate at the top, "−" at the bottom). This loop, in this orientation, is the chapter's running object (s3–s7). {pump}: the battery pulses, tag ‘electron pump’ (the slide's quotes). {drift}: the electrons keep jittering, but now share a slow drift anticlockwise, toward the "+" terminal and on through the battery. {slow}: GOLD "< 1 mm per second" (p. 165), and one electron, enlarged, bouncing off ions. {metre}: a ruler along the top wire marked "1 m"; GOLD "1 m ÷ 1 mm/s = 1000 s, over 15 minutes" (ours, checked: 1000 s ≈ 16.7 min).
> {instant}: the battery disconnects (electrons back to pure jitter), then reconnects: every electron round the whole loop starts drifting on the same frame. {train}: a line of small coupled carriages along the top wire, all starting together. {shows}: two empty tags appear beside the loop. {warm}: the wire picks up a faint ORANGE glow and heat shimmer (decorative, no colour role), tag "warmer"; {compass}: a small compass by the right-hand wire, its needle swinging, tag "compass deflects" (p. 165).

[c6.metal.1] {current} An electric current is charged particles moving in a definite direction. {metals} In a metal, those particles are electrons. {gases} In a gas or a liquid, they're electrons and ions. {focus} Our wires are metal, so let's follow the electrons.

[c6.metal.2] {lattice} Zoom into a metal wire. Its atoms sit in a regular lattice. {loose} Each atom holds its outer electrons so loosely that they're free to roam between the positive ions, which stay fixed in place. {random} At room temperature they rush about at random, in every direction. {pause} {nonet} So on average, as many electrons cross any point one way as the other. There's no net flow of charge, and so no current.

[c6.metal.3] {battery} Now connect the wire across the terminals of a battery. {pump} The battery acts as an electron pump. {drift} It forces the free electrons to drift toward its positive terminal, and on through the battery itself. {slow} The drift is slow, under a millimetre per second, because the electrons keep colliding with the ions. {metre} At that speed, one electron would take more than a quarter of an hour to cross a metre of wire.

[c6.metal.4] {instant} And yet the whole circuit responds the moment the battery is connected. How can that be? {pause} {train} Every free electron in the circuit starts drifting at the same time, like the carriages of a train. When one carriage moves, they all move. {shows} The current then shows itself in two ways. {warm} The wire gets warmer, {compass} and a compass needle nearby is deflected.

## Scene 3 · Which way, and how much (ch6_s3_current)

> s2's loop, unchanged, electrons drifting anticlockwise. {before}: ghost GOLD "+" charges (dashed outlines, tag "imagined, before electrons were known") stream out of the "+" terminal, clockwise round the loop, into "−". {conv}: they fade, leaving GOLD current arrows on the wire, clockwise, with p. 165's label "Direction of current flow" over the top wire and "conventional current: + → −" under the loop.
> {electrons}: the electrons brighten, each "−" pulsing. {opposite}: a BLUE arrow beside the right-hand wire pointing up, with p. 165's label "Flow of electrons in metal wire connected across a battery".
> {loop}: both arrows in view. {gold}: the GOLD arrows pulse; {blue}: the BLUE arrow pulses. {same}: small copies of the two arrows with "=" between them, "same current". {rule}: the BLUE arrow and the electrons dim; the GOLD arrows stay. From here on, every current arrow is conventional current.
> {howmuch}: zoom to one point of the wire: a dashed cross-section disc, electrons streaming through it, a GOLD counter racing. {huge}: the counter blurs past millions. {one}: one electron enlarged, tag `1.6\times10^{-19}\,\text{C}` (p. 165: "one electron has a charge of 1.6*10-19 C"). {flip}: TransformFromCopy into `1 \div (1.6\times10^{-19}) = 6.25\times10^{18}`, then "1 C = 6.25 × 10¹⁸ electrons" (p. 166).
> {amp}: a stopwatch beside the disc runs one second while a GOLD "1 C" bundle passes: "1 C per second = 1 A" ("1 Ampere (A)" as on p. 166). {formula}: `I = Q/t` (I GOLD), with tags under each letter, "current (A)", "charge (C)", "time (s)". {rate}: p. 166's words, "current is the rate of flow of charge". {milli}: `1\,\text{mA} = 10^{-3}\,\text{C/s}` → "6.25 × 10¹⁵ electrons per second" (ours, checked).

[c6.current.1] {before} There's a twist in which way current flows. Before electrons were discovered, people imagined current as positive charges, flowing out of the battery's positive terminal and round to the negative one. {conv} That's still how current is defined. It's called conventional current, and it flows from plus to minus. {electrons} But the electrons in a metal are negative, {opposite} so they drift the other way, toward the plus terminal. {pause}

[c6.current.2] {loop} So in this loop, the two arrows point opposite ways. {gold} Conventional current goes clockwise, {blue} while the electrons go anticlockwise. {same} Both describe the same current. {rule} From now on, every current arrow means conventional current, from plus to minus, whatever the electrons are doing.

[c6.current.3] {howmuch} Now, how much charge flows? {huge} A huge number of electrons drift past each point every second, so charge is counted in a much bigger unit, the coulomb. {one} One electron carries a charge of one point six times ten to the minus nineteen coulombs. {flip} Turn that around, and one coulomb is the charge of six point two five times ten to the eighteen electrons. {pause}

[c6.current.4] {amp} When one coulomb passes a point every second, the current is one amp. {formula} So current, eye, is charge, cue, divided by time, tee. {rate} In other words, current is the rate of flow of charge. {milli} Even a current of one milliamp, a thousandth of an amp, is six point two five times ten to the fifteen electrons, every second.

## Scene 4 · Volts: energy per coulomb (ch6_s4_volts)

> p. 167's circuit, built from s3's loop: {lamp}: a lamp (circle with an X, FG) drops into the right-hand wire, "Lamp" beside it; the GOLD current arrow on the top wire, labelled "Flow of current" (p. 167). {force}: the battery pulses. {printed}: beside the battery symbol, a small battery cell with "1.5 V" printed on it. {emf}: "electromotive force (emf)" writes under it, and a TEAL arrow appears left of the battery, pointing up (head at "+"), labelled `V_B`.
> {define}: a card, p. 167's definition, "emf V_B = 1 V if it gives 1 J of electrical energy to each C of charge passing through it". {joule}: a GOLD-ringed "1 C" token rides clockwise with the current arrow; passing through the battery it picks up a GOLD "+1 J" chip. {half}: with the 1.5 V battery, the chip reads "+1.5 J".
> {opposite}: the token rides on into the lamp. {heat}: its "1.5 J" chip leaves as YELLOW light rays and ORANGE shimmer; the lamp glows YELLOW and stays lit. {pd}: a TEAL arrow right of the lamp, pointing up (head at the top), labelled `V_L`, and "potential difference (pd)". {ratio}: p. 167's `V_L = E/Q`, tags "energy (J)" and "charge (C)", then "1 V = 1 J/C".
> {gives}: the battery side tagged "emf: energy given to each coulomb"; {takes}: the lamp side tagged "pd: energy taken from each coulomb". {voltages}: the two tags fold into one word, "voltages", "both measured in V" (p. 168).
> {arrows}: both TEAL arrows flash, tag "head at the higher potential". {ends}: the battery's arrowhead lights with its "+"; then the lamp's arrowhead lights at the lamp's top end, where the GOLD current arrow enters. The loop, lamp lit, carries into s5.

[c6.volts.1] {lamp} Now put a lamp in the loop. {force} The battery supplies the force that drives the electrons round the circuit, and the energy they carry. {printed} A battery has a voltage printed on it, one and a half volts, for example. {emf} That number is its electromotive force. The slide labels it vee, with a subscript bee, for battery.

[c6.volts.2] {define} Here's what one volt means. {joule} A battery's electromotive force is one volt if it gives one joule of electrical energy to each coulomb of charge passing through it. {half} So a one and a half volt battery gives every coulomb one and a half joules. {pause}

[c6.volts.3] {opposite} The lamp does the opposite. {heat} It turns most of that electrical energy into heat and light. {pd} The potential difference across the lamp is labelled vee, with a subscript ell, which stands for lamp. It's one volt if the lamp converts one joule for every coulomb that passes through it. {ratio} So a potential difference is the energy divided by the charge, measured in joules per coulomb.

[c6.volts.4] {gives} So an electromotive force gives energy to each coulomb, {takes} and a potential difference takes it away. {voltages} Both are measured in volts, so both are usually just called voltages. {arrows} On a diagram, each voltage gets an arrow, with its head at the end with the higher potential. {ends} For the battery, that's its plus end. For the lamp, it's the end where the current goes in.

## Scene 5 · Power (ch6_s5_power)

> s4's loop, small, top left, lamp lit. The derivation centred, one MathTex line per step, each new line made from a copy of the one above. Source, p. 168 verbatim: "PL=E/t (J/s). Previously we have, E = QVL, and so, PL= QVL /t (W)." and "Now substitute Q = It from before to give, PL= It VL /t = IVL (W) , an expression that hopefully is familiar".
> {ask}: p. 168's question, "What is the power dissipated (P_L) in the lamp?", and a `P_L` tag by the lamp. {def}: `P_L = E/t`, with "J/s = watts (W)". {pl}: the E and the t light.
> {how}: small copies of s4's `V_L = E/Q` and s3's `I = Q/t` drop in at the side. {sub1}: `V_L = E/Q` rearranges to `E = QV_L` (YELLOW box), which slides into the E slot: `P_L = QV_L/t`. {sub2}: `I = Q/t` rearranges to `Q = It` (YELLOW box), which slides into the Q slot: `P_L = ItV_L/t`. {cancel}: the two t's light YELLOW, then are struck through and DIM. {result}: `P_L = IV_L` (W), boxed.
> {any}: the box generalises to `P = IV`, tags "current through it" (GOLD) and "voltage across it" (TEAL). {familiar}: p. 168's "an expression that hopefully is familiar", small. {example}: back on the loop, GOLD "0.2 A" on the current arrow, TEAL "1.5 V" by `V_L`; `P = 0.2 \times 1.5 = 0.3\,\text{W}` in GOLD (ours, checked).

[c6.power.1] {ask} So how much power does the lamp use? {pause} {def} Power is energy per second. One joule per second is one watt. {pl} So the lamp's power is the energy it converts, divided by the time it takes. {how} To find it, we'll use the two definitions we already have.

[c6.power.2] {sub1} The lamp's voltage is energy per coulomb, so the energy is the charge times the voltage. Put that in. {sub2} And current is charge per second, so the charge is the current times the time. Put that in too. {cancel} Now there's a time on top and a time underneath, and they cancel. {result} The power is the current times the voltage. {pause}

[c6.power.3] {any} The same holds for any device. The power in it is the current through it, times the voltage across it. {familiar} In the slide's words, it's an expression that's hopefully familiar. {example} For example, with zero point two amps through our lamp and one and a half volts across it, the lamp uses zero point three watts.

## Scene 6 · Resistance and Ohm's law (ch6_s6_resistance)

> {view}: p. 168's heading, "Circuit Theory". {oppose}: s2's lattice, close up inside a short piece of conductor; drifting BLUE electrons bounce off the DIM ions. {resistance}: label "resistance (R)". {bigger}: two conductors side by side, the same GOLD current arrow through each; the one with the denser lattice gets the longer TEAL voltage arrow, tag "bigger R, bigger V, for a given current".
> {define}: p. 169's `R = V/I`, tags "pd across it" (TEAL), "current through it" (GOLD). {ohmslaw}: TransformFromCopy into `V = IR`, YELLOW label "Ohm's law". {unit}: "ohms (Ω)".
> {resistor}: p. 169's symbol, an FG rectangle with a lead on each side, `R\,\Omega` above it. {symbol}: it flashes. {bands}: beside it, a small drawn resistor, a beige body with four coloured bands (decorative). {swap}: back to the running loop: the lamp shrinks away and the resistor symbol slides into its place, labelled "10 Ω"; its TEAL arrow keeps s4's rule (head at the top, where the current enters), now "1.5 V". {calc}: `I = 1.5 \div 10 = 0.15\,\text{A}`, and the GOLD current arrow is relabelled "0.15 A" (ours, checked).
> {plot}: axes, V across (volts), I up (amps). {line}: an FG straight line through the origin, a GOLD dot at (1.5 V, 0.15 A). {double}: the dot slides to (3 V, 0.3 A). {zero}: the origin lights. {flatter}: a second, DIM, flatter line labelled "20 Ω" beside the first, now labelled "10 Ω" (ours: the slope is 1/R).
> {water}: p. 169's analogy as a picture: a pipe with water flowing through it, a pressure gauge at each end with different readings; tags "water ↔ charges", "pipe ↔ conductor", "pressure difference ↔ voltage". The loop with its 10 Ω resistor carries into s7.

[c6.ohm.1] {view} Electrical engineers have another way to look at potential difference. {oppose} Every conductor opposes the flow of current, some a lot, and some only a little. {resistance} That opposition is called resistance. {bigger} For a given current, the bigger the resistance, the bigger the voltage across the conductor.

[c6.ohm.2] {define} Resistance is defined as the voltage across a conductor, divided by the current through it. {ohmslaw} Turn that round, and the voltage is the current times the resistance. That's Ohm's law. {unit} Resistance is measured in ohms, written with the Greek letter omega.

[c6.ohm.3] {resistor} A conductor made to have a particular resistance is called a resistor. {symbol} In a circuit diagram, it's a small rectangle, labelled with its value in ohms. {bands} In the lab, resistors are tiny parts with coloured bands, and the bands tell you the value. {swap} So swap our lamp for a ten ohm resistor. {calc} With one and a half volts across it, the current is one and a half divided by ten, which is zero point one five amps.

[c6.ohm.4] {plot} Now plot the current against the voltage. {line} For an ohmic, or linear, conductor like this one, you get a straight line through the origin. {double} Double the voltage, and the current doubles, {zero} and with no voltage, there's no current. {flatter} And with a bigger resistance, the line is flatter. {water} The slides add an analogy. Charge flowing in a wire is like water flowing in a pipe, and it takes a difference in pressure, a voltage, to make it flow.

## Scene 7 · Kirchhoff's two laws (ch6_s7_kirchhoff)

> {two}: s6's loop moves aside, small. {kcl}: title "Kirchhoff's Current Law", and p. 170's junction: a dot (the node), two wires coming in from the left (upper and lower), one going out to the right. {signs}: GOLD arrows, the two incoming ones tagged "+ (in)", the outgoing one "− (out)".
> {slide}: labels `I_1`, `I_2` (incoming) and `I_3` (outgoing) light as they're said. {eq}: p. 170 verbatim, `I_1+I_2-I_3 = 0` or `I_1+I_2 = I_3`. {pipe}: the wires turn into pipes, water flowing in through two and out through one. {example}: GOLD "2 A" and "3 A" on the inflows, "5 A" on the outflow; {check}: `2 + 3 - 5 = 0` (ours, checked).
> {kvl}: title "Kirchhoff's Voltage Law", "in any closed loop, the sum of all the voltages is zero" (p. 170). {ours}: s6's loop returns, its two TEAL arrows labelled "1.5 V"; `+1.5 - 1.5 = 0` under it (ours, checked). {grow}: the loop grows into p. 170's loop: its sides stretch, and two more batteries and three resistors slide in where the slide has them (the 10 Ω resistor becomes R_c).
> p. 170's loop, exactly (the digest's R2/R4/R5 names and its V6 direction are wrong; follow the slide): left side, battery `V_1` ("+" at the top), its TEAL arrow pointing up, and a GOLD current arrow on the wire just above it, pointing up (clockwise); top wire, left to right, resistor `R_a` (TEAL `V_2` above, pointing left), battery `V_3` ("+" on its left; `V_3` pointing left), resistor `R_b` (`V_4` pointing left); right side, resistor `R_c` (`V_5` to its right, pointing up); bottom wire, battery `V_6` ("+" on its left; `V_6` below, pointing left); a dot at the bottom-left corner.
> {arrows}: all six TEAL arrows flash. {batteries}: the three battery arrowheads light with their "+" ends. {choose}: the GOLD current arrow pulses, tag "chosen: clockwise". {resistors}: each resistor's arrowhead lights at the end where the GOLD current enters (left for R_a and R_b, top for R_c), with a small GOLD arrow through each resistor.
> {walk}: a YELLOW dot sets off from the bottom-left corner, clockwise. {rule}: a small key, "arrow with you: +", "arrow against you: −". {v1}, {top}, {right}, {bottom}: as the dot passes each element its arrow flashes and its term drops into the equation with its sign, building `V_1-V_2-V_3-V_4-V_5+V_6`; {zero}: `= 0`, the slide's equation complete.
> {values}: values appear: TEAL 5 V, 1 V, 2 V by V_1, V_3, V_6; 1 Ω, 2 Ω, 3 Ω by R_a, R_b, R_c; GOLD "1 A" on the current arrow. {ohm}: "1 A × 1 Ω" turns into V_2's "1 V", then V_4's "2 V" and V_5's "3 V". {add}: under the equation, each number under its symbol, `5-1-1-2-3+2`; {result}: `= 0` in GOLD. (Ours, checked: consistent, since I = (5 − 1 + 2) ÷ (1 + 2 + 3) = 1 A; the current isn't derived on screen.) {negative}: a ghost copy of the GOLD current arrow flips to point down, tag "negative answer: it flows the other way".

[c6.laws.1] {two} Last, two laws from Kirchhoff, which you'll use in almost every circuit. {kcl} First, the current law. At a junction, or node, where wires meet, the currents entering add up to zero. {signs} We count a current flowing in as positive, and a current flowing out as negative.

[c6.laws.2] {slide} Here, eye one and eye two flow in, and eye three flows out. {eq} So eye one plus eye two minus eye three equals zero. Or, eye one plus eye two equals eye three. {pipe} What goes in must come out, just like water at a junction of pipes. {example} If two amps and three amps flow in, then five amps flow out, {check} and two plus three minus five is zero.

[c6.laws.3] {kvl} Second, the voltage law. Around any closed loop, the voltages add up to zero. {ours} Our little loop already obeys it. The battery gives one and a half volts, and the resistor takes one and a half volts, so the total is zero. {grow} The slides' loop is bigger, with three batteries and three resistors.

[c6.laws.4] {arrows} Each voltage has an arrow, with its head at the higher potential. {batteries} For a battery, that's its plus end. {choose} For a resistor, it depends on the current, and often you have no idea which way that will flow. So choose a direction, here clockwise, and stick to it. {resistors} Each resistor's arrow then points to the end where the current goes in.

[c6.laws.5] {walk} Now walk round the loop clockwise, starting up through the left battery. {rule} When an arrow points the way you're walking, add its voltage, and when it points against you, subtract it. {v1} Up the left side, plus vee one. {top} Along the top, three arrows against you, minus vee two, minus vee three, minus vee four. {right} Down the right side, minus vee five, {bottom} and back along the bottom, plus vee six. {zero} All of that equals zero. {pause}

[c6.laws.6] {values} With numbers, say the batteries give five, one and two volts, and the resistors are one, two and three ohms, with one amp flowing through them all. {ohm} Ohm's law gives the resistors' voltages, one, two and three volts. {add} So we have five, minus one, minus one, minus two, minus three, plus two, {result} which is zero. {pause} {negative} And if a current you solve for comes out negative, it simply flows the other way.

## Scene 8 · Recap and next (ch6_s8_recap)

> Recap: a 3 × 2 grid of small panels, each the scene's own object in its own colours, its short line under it, appearing on its sentence (never a bare text list). {recap}: the grid frame. {r1}: s2's loop with jittering BLUE electrons drifting together, and the little train; "slow drift, all at once". {r2}: s3's loop with the GOLD clockwise arrows and the BLUE electron arrow; `I = Q/t`, "1 A = 1 C/s". {r3}: s4's battery and lit lamp with the TEAL `V_B` and `V_L` arrows; "1 V = 1 J/C".
> {r4}: s5's two substitutions collapsing into the boxed `P = IV`. {r5}: s6's resistor symbol beside its straight line through the origin; `V = IR`. {r6}: s7's junction with `I_1+I_2 = I_3`, beside the six-element loop with `V_1-V_2-V_3-V_4-V_5+V_6 = 0`.
> {lecture}: the grid shrinks away; three small pictures in a row, joined by arrows: ch1 s7's 7-state diagram, ch4 s6's GAL with the synchroniser's coloured AND gates, and s4's lit lamp loop; tags "shrink it", "put it on a chip", "what it runs on".
> {next}: p. 170's last bullet, "We will now analyse a simple 2 resistor circuit known as a potential divider", over a DIM silhouette of a battery with two resistors in series and a YELLOW "?" at the point between them. End card after the last word, held ~8 s; the music carries it.

[c6.recap.1] {recap} Let's recap. {r1} A current is charge drifting one way, slowly, but all at once. {r2} Conventional current flows from plus to minus, against the electrons, and one amp is one coulomb per second. {r3} A volt is one joule per coulomb, given by a battery, or taken by a lamp.

[c6.recap.2] {r4} Power is current times voltage. {r5} In a resistor, voltage is current times resistance, which is Ohm's law. {r6} At every junction the currents balance, and around every loop the voltages add up to zero. {lecture} So in this lecture, we shrank a state machine, put it on a chip, and asked what the chip runs on.

[c6.recap.3] {next} Next lecture, we put Ohm and Kirchhoff to work, on a simple circuit with two resistors. It's called a potential divider, and it leads on to the transistors inside every logic gate. {pause}
