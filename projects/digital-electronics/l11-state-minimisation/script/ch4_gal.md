# Chapter 4 · State machines on a programmable chip

Digital Electronics · Lecture 11 (State Minimisation, Programmable Logic and Circuits), part 4 of 6. Source: Digital Electronics slides (combined_26.pdf), pp. 156–158 (through "GAL Devices"), with refreshers from pp. 71–73 (PLA and PAL, an earlier lecture outside our series) and p. 122 (the Moore schematic); lecture recording 00:31:26–00:35:20.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Spoken names: "P-L-A" is a PLA, "G-L-A" a GLA, "F-P-G-A" an FPGA (spelled out); "PAL" and "GAL"
are said as words. capital "A" (COURSE.md), "bee", "see" are the inputs a, b, c; "eff zero" … "eff N" the outputs
f0 … fn; "cue" and "not cue" are Q and Q̄. For the synchroniser (L10 ch5): "ee" and "ar" are the
inputs e and r, "ess" the output s, "ess one" and "ess zero" the state bits s1 and s0, "dee one" and
"dee zero" the D inputs D1 and D0, "flip-flop one" the flip-flop holding s1. Products are read by
meaning: "ess one and not ee" is s1·ē. Colours as PLAN.md sets them: inputs BLUE (a, b, c; e, r);
flip-flop feedback rails and state bits GREEN; D inputs BLUE; CLK YELLOW; outputs GREEN; AND and OR
planes as DIM-shaded panels, like the slides' hatching; kept connections are dots where a rail crosses
an AND gate's input line; synchroniser product terms in L10 ch5's K-map loop colours (D1: s1·ē PINK,
s1·r PURPLE, s0·e·r TEAL; D0: s0·ē PINK, s̄1·s̄0·r PURPLE); counts GOLD; a term made twice RED.
No code on screen. The PLA/PAL example, the synchroniser's equations, its GAL connections and every
count below were checked by exhaustive enumeration in Python 3.11.9 (standard library,
itertools.product over states and inputs); the figures were re-read from the rendered slides,
pp. 72, 73, 122, 157 and 158.

---

## Scene 1 · Hook (ch4_s1_hook)

> {title}: title card: "State Minimisation, Programmable Logic and Circuits" (scaled to 12 units wide, as L8's ch1 s1), under it "Digital Electronics · Lecture 11", then the part line "Part 4 · State machines on a programmable chip".
> {last}: ch3 s6's 6-state table (p. 155), small at the left, header "Present State | Next State X=0 X=1 | Output (Y)", rows `A | A C | 0`, `B | F H | 0`, `C | C A | 1`, `F | F B | 1`, `G | B H | 0`, `H | C G | 1`; the merged letters A and C GOLD, a GOLD tag "8 → 6 states". {build}: the table fades; a YELLOW "how?" sits where it was.
> {chips}: L10 ch1 s8's divide-by-5 circuit as the lecturer's simulator had it, drawn as three chip packages (L8's `chip()`) with small DIM part numbers: "74HC08", "74HC86", "74HC74". {kinds}: a tag lights under each as it's named: "and gates", "exclusive-or gates", "flip-flops"; DIM wires run between their pins.
> {change}: the wires flash RED and re-route into a different tangle, and a second "74HC08" slides in: a different machine, different chips, different wiring.
> {one}: the packages and their wires slide together and merge into one larger package (L8's `chip()`), blank, with a YELLOW "?" on its face. {question}: caption under it, "one chip, any state machine?". The package stays and shrinks to a corner for s2.

[c4.hook.1] {title} This is part four of our lecture on state minimisation, programmable logic and circuits. {last} Last time, the implication table found the equivalent states, and the machine shrank from eight states to six. {build} So now we know what to build. The question is how to build it.

[c4.hook.2] {chips} In Lecture ten, the lecturer built his circuits in a simulator, from seventy-four series chips. {kinds} There were chips of and gates, of exclusive-or gates and of flip-flops, all joined up with wires. {change} A different machine needs different chips, and different wiring. {one} So here's the question for this part, and the next. {question} How can a single chip become whichever state machine you need? {pause}

## Scene 2 · What a state machine needs (ch4_s2_needs)

> {schematic}: p. 122's Moore schematic, as L10 ch1 s2 drew it, left to right with the slide's labels verbatim: "Inputs" (BLUE, bus slash "n") → box "Next state combinational logic" → bus "m" (BLUE: the D inputs) → a D flip-flop box (L6's `make_ff`: D, Q, Q̄) → bus "m" (GREEN) → box "Optional combinational logic" → "Outputs" (GREEN), and "CLK" (YELLOW) into the flip-flop. A "Current state" wire (GREEN) runs from Q back over the top into the first box.
> {logic}: the "Inputs" wire and the "Current state" wire pulse into the first box. {ffs}: the flip-flop box and its YELLOW CLK line light. {loop}: a GREEN pulse runs along "Current state" from Q, over the top, back into the logic. {outlogic}: the "Optional combinational logic" box lights.
> {two}: two brackets drop under the schematic, one per mark: {comb} "combinational logic" (BLUE) spanning both logic boxes, {dtype} "D flip-flops" (BLUE) under the flip-flop box.
> {discrete}: the schematic shrinks to the top. Below at the left, s1's three chip packages wired together, tag "separate chips". {prog}: at the right, s1's single package, its "?" replaced by a small grid on its face, tag "programmable device". A DIM tag "both in the labs" spans the two.
> {slide}: clear to p. 156's first slide title "Implementation of FSMs", and a DIM tag "pp. 71–73: an earlier lecture, not in our series". {quote}: its first bullet, verbatim: "We saw previously that programmable logic can be used to implement combinational logic circuits, i.e., using PLA devices", with "PLA" YELLOW.
> {add}: s2's small D flip-flop box flies in beside the bullet with a "+", and the small Moore schematic glows once. {remind}: everything clears except the YELLOW "PLA", which moves up to become s3's title.

[c4.needs.1] {schematic} Here's the shape of the machines from Lecture ten. {logic} The inputs and the current state feed a block of next-state logic. {ffs} Its outputs go into a row of dee flip-flops, all driven by one clock signal. {loop} The flip-flops hold the current state, which loops back into the logic. {outlogic} And an optional block of output logic turns the state into the outputs.

[c4.needs.2] {two} So, as the lecturer puts it, every state machine needs just two kinds of thing. {comb} Some combinational logic, {dtype} and some dee flip-flops. {discrete} In the labs, you'll build some machines from separate chips, like the ones we just saw, wired up gate by gate. {prog} You'll also use programmable devices, chips whose logic you set yourself.

[c4.needs.3] {slide} The slides start from an earlier lecture, one that's outside our series. {quote} There, programmable logic made combinational circuits, using devices called P-L-A chips. {add} Add flip-flops to one of those, and you're most of the way to a state machine. {remind} So first, a quick reminder of how a P-L-A works.

## Scene 3 · PLAs and PALs (ch4_s3_plapal)

> p. 72's "Basic PLA Structure", rebuilt large: inputs `a`, `b`, `c` (BLUE) enter on the left; each also passes through an inverter, giving six horizontal rails `a`, `ā`, `b`, `b̄`, `c`, `c̄` (BLUE, real overbars) across the top half, a DIM-shaded panel labelled "AND plane". Three AND gates hang below the rails, each with six vertical input lines, one per rail. Below, a second DIM-shaded panel "OR plane" with three OR gates, outputs `f0`, `f1`, `f2` (GREEN), each OR gate with one input line per AND gate.
> {pla}: title "PLA: programmable logic array". {inputs}: `a`, `b`, `c` light in turn. {inverters}: the three inverters light, and each input splits into its pair of rails. {plane}: the six rails draw across, and the "AND plane" panel fades in. {gates}: the three AND gates. {full}: a dot at every crossing of a rail with an AND gate's input line, 18 dots, all lit.
> {program}: the slide's caption fades in at the left, verbatim: "Programmed by selectively removing connections in the AND and OR planes – controlled by fuses or memory bits". {fuses}: "fuses or memory bits" YELLOW. {term}: on the first AND gate, every dot fades except `a` and `b̄`; its output gets the label `a·b̄`. {one}: small chips `a = 1` and `b = 0` (BLUE) by the inputs, and a GREEN `1` on the gate's output. {each}: all three gates pulse. {others}: the other two gates keep two dots each, labels `b·c` and `ā·c̄`.
> {or}: the "OR plane" panel and the three OR gates; a dot at each crossing of an AND output with an OR input line. {sums}: the dots on the OR plane flash. {f0}: on `f0`'s OR gate every dot fades except `a·b̄` and `b·c`, and `f0 = a·b̄ + b·c` appears by its output. {f1}: on `f1`'s, all but `a·b̄` and `ā·c̄`, and `f1 = a·b̄ + ā·c̄` appears (formulas GREEN on the left of the =, terms as their gate labels); the `a·b̄` gate now feeds both. {spare}: `f2` and its OR gate go DIM. {sop}: a small tag "sum of products" under the two formulas.
> {minterm}: a small card at the side: the slides' word "minterm" in quotes. {strict}: under it, "minterm: every input, e.g. a·b̄·c". {loose}: then "product term: any AND of inputs, e.g. a·b̄", the missing `c` shown as a DIM gap. {product}: the label "product term" turns YELLOW and stays as the word for the rest of the chapter.
> {pal}: the PLA slides left and shrinks; at the right, p. 73's "Basic PAL Structure", title "PAL: programmable array logic". {fixed}: its OR plane has no dots: each OR gate is joined by plain fixed lines to its own AND gates (`f0` to the right-hand pair, `fn` to the left-hand pair, as on p. 73; `fn` is relabelled `f1` for the example). {only}: the AND plane's dots flash. {cost}: the slide's line, verbatim: "This simplifies the structure, but at the cost of lower efficiency". {share}: a ghost line from one of `fn`'s AND gates toward `f0`'s OR gate tries to cross over and stops, RED.
> {example}: the two formulas return from the PLA, and both drawings set up the same two functions, `f0 = a·b̄ + b·c` and `f1 = a·b̄ + ā·c̄`, with `a·b̄` YELLOW in both formulas. {once}: in the PLA, the single `a·b̄` gate glows YELLOW and its output runs to both OR gates. {twice}: in the PAL, `a·b̄` is made by one AND gate in each group, the second copy RED with a tag "made twice". {count}: GOLD counts under each: "3 AND gates" (PLA), "4 AND gates" (PAL). {lower}: the "lower efficiency" line pulses.
> Checked (exhaustive, Python 3.11.9): `f0`'s prime implicants are a·b̄, a·c and b·c, `f1`'s are a·b̄, ā·c̄ and b̄·c̄; the only minimum covers are a·b̄ + b·c and a·b̄ + ā·c̄, so both outputs need a·b̄. Three distinct terms (PLA), four AND gates (PAL).

[c4.pla.1] {pla} Here's a P-L-A, a programmable logic array. {inputs} On the left are three inputs, input A, input bee and input see. {inverters} Each one also passes through an inverter, so every input arrives as a pair of wires, itself and its complement. {plane} Those six wires run across the top half, called the and plane, {gates} past a row of and gates. {full} To begin with, every and gate is connected to every wire.

[c4.pla.2] {program} To program the chip, you remove connections, and keep only the ones you need. {fuses} The slide says they're controlled by fuses, or by memory bits. {term} Keep just the wires for A and not bee, and that gate makes A and not bee. {one} Its output is one only when input A is one and input bee is zero. {each} So each of these and gates makes one product, of whichever inputs and complements you keep. {others} Here, the other two make bee and see, and not A and not see.

[c4.pla.3] {or} The bottom half is the or plane. {sums} Each or gate can take any of the products, again by keeping or removing connections. {f0} Here, output eff zero is A and not bee, or bee and see. {f1} Output eff one is A and not bee, or not A and not see. {spare} Output eff two is left spare. {sop} So each output is a sum of products, the form a K-map gives you.

[c4.pla.4] {minterm} A word on names. The slides call these products minterms. {strict} Strictly, a minterm contains every input, like A and not bee and see. {loose} A product here can leave inputs out, as A and not bee leaves out see. {product} So we'll call them product terms.

[c4.pla.5] {pal} A PAL, programmable array logic, is a simpler relative. {fixed} Its or plane is fixed. Each or gate has its own and gates, wired to it for good. {only} Only the and plane is programmable. {cost} That makes the structure simpler, but there's a cost. {share} Each product term can feed only one output.

[c4.pla.6] {example} Now look at the two formulas again. Outputs eff zero and eff one both need the term A and not bee. {once} The P-L-A makes it once, and feeds that one and gate to both or gates. {twice} The PAL has to make it twice, once in each output's group. {count} So the P-L-A uses three and gates, and the PAL needs four. {lower} That's what the slide means by lower efficiency.

## Scene 4 · Add flip-flops, feed them back (ch4_s4_gla)

> s3's PLA, with every dot restored, moves to the centre, cut down to p. 157's size: three inputs with their complements (six BLUE rails), two AND gates, two OR gates, the AND and OR planes as DIM-shaded panels, every connection dot lit (both planes programmable). Inputs unlabelled, as on the slide.
> {back}: s3's PAL and the formulas fade away; the cut-down PLA stays. {modify}: two D flip-flop boxes (L6's `make_ff`: D, Q, Q̄) slide in at the right. {gla}: title "GLA: generic logic array". {like}: tag "like a PLA: both planes programmable", the dots in both panels flashing once. {ffs}: each flip-flop docks after an OR gate, the OR output wire turning BLUE into D; p. 156's words as a caption, verbatim: "one following each OR gate". {clk}: one YELLOW CLK line feeds both clock triangles from below. {edge}: a YELLOW pulse runs along CLK, and each OR gate's output value (a small `1` or `0`) drops into its flip-flop and appears at Q.
> {enough}: the outputs leave on the right; a YELLOW "?" hovers over the AND plane. {state}: the "?" becomes a small tag "next state = f(inputs, current state)". {feedback}: from each flip-flop's Q, a GREEN wire runs right, up and back over the top into the AND plane, becoming a new horizontal rail above the input rails (as on p. 157), with fresh dots where it crosses each AND gate's input lines. {sees}: an AND gate's input lines light where they meet both a BLUE input rail and a GREEN state rail. {quote}: p. 156's line, verbatim: "Consequently it becomes possible to build programmable sequential logic circuits".
> {schematic}: s2's Moore schematic appears small above. {logic}: its "Next state combinational logic" box and the two planes glow together (BLUE). {ffs2}: its flip-flop box and the two flip-flops glow. {loop}: its "Current state" wire and the GREEN feedback rails pulse together. {onechip}: a chip outline (L8's `chip()`) draws around the whole GLA; the small schematic fades.
> {figure}: tag "p. 157: very simplified", with GOLD counts "3 inputs · 2 AND · 2 OR · 2 flip-flops". {notq}: the Q̄ outputs pulse; a ghost of the slide's version shows only Q fed back. {both}: two more GREEN rails grow from the Q̄ outputs, over the top into the AND plane, with their dots (rails now: two state bits and their complements, beside the six input rails). {complex}: both panels pulse, tag "two programmable planes".

[c4.gla.1] {back} Now, back to state machines. {modify} To build them on a single chip, these arrays were given dee flip-flops. {gla} One style of chip is called a G-L-A, short for generic logic array. {like} It's like a P-L-A, with both planes programmable. {ffs} But each or gate can be followed by a dee flip-flop, {clk} and all the flip-flops share one clock signal. {edge} On every edge of the clock, each flip-flop stores what its or gate has worked out.

[c4.gla.2] {enough} Is that enough to make a state machine? {pause} {state} Not quite. The next state depends on the current state, as well as on the inputs. {feedback} So the flip-flop outputs are fed back into the and plane, as extra wires beside the inputs. {sees} Now every one of the and gates can use the inputs and the current state together. {quote} As the slide puts it, it becomes possible to build programmable sequential logic.

[c4.gla.3] {schematic} Put the Moore schematic beside it. {logic} The two planes are the next-state logic, a sum of products for each flip-flop's dee input. {ffs2} The flip-flops hold the state. {loop} And the feedback wires are the loop back. {onechip} It's the whole machine, on one chip.

[c4.gla.4] {figure} The slide's picture is very simplified, with three inputs, a pair of and gates, a pair of or gates and two flip-flops. {notq} It only feeds back cue. The lecturer said that in reality, not cue is fed back as well. He just ran out of space on the picture. {both} So we draw both. {complex} With two programmable planes, this is quite a complex device.

## Scene 5 · The GAL (ch4_s5_gal)

> {gal}: s4's GLA shrinks to the left; p. 157's line as a caption, verbatim: "A modified form of a GLA known as a Generic Array Logic (GAL) is used in the Hardware Laboratory classes to implement various FSMs." {names}: two cards, one under the other: "GLA: generic logic array" and "GAL: generic array logic". {gla}: the first card lights. {galname}: the second lights, and "logic" and "array" in the two names swap places with a YELLOW arc. {fixed}: s3's small PAL flashes beside the cards, tag "fixed OR plane, like a PAL".
> {figure}: clear to p. 158's "GAL Devices", rebuilt large, as on the slide: inputs `a` and `b` (BLUE) on the left, each with an inverter, giving four rails across a DIM-shaded "AND plane"; above them, GREEN feedback rails from the flip-flops over the top. Four AND gates, with the slide's dotted and dashed gaps between them meaning "more of these". A DIM-shaded "OR plane" below with two OR gates and the slide's dashed line between them: the right-hand pair of AND gates wired to the top OR gate, the left-hand pair to the bottom one, by fixed lines with no dots.
> {rails}: the BLUE rails, then the GREEN rails, light. {groups}: each OR gate's two AND gates glow together, the top pair in one tint, the bottom pair in another. {gaps}: the dotted and dashed gaps pulse. {ffs}: two D flip-flops (L6's `make_ff`), outputs labelled `f0` (top) and `fn` (bottom), GREEN, the dashed line between them. {clk}: "CLK" (YELLOW) enters at the bottom left and runs to both clock triangles.
> {cost}: one term, say `a·b̄`, appears on an AND gate in each group, the second RED, tag "made twice" (s3's PAL tag, same style). {same}: both copies pulse. {gain}: the OR plane's fixed lines glow; GREEN tags "simpler" and "faster". {depends}: the RED copy and the GREEN tags sit side by side, with a small YELLOW "?" between them.
> {hand}: a small hand icon reaches for a dot and is crossed out (DIM). {type}: at the left, a box with Boolean equations typed in, `f0 = …`, `fn = …`. {compiler}: an arrow from it into a box "compiler", then an arrow onward to the AND plane, whose dots blink on and off into a pattern. The GAL drawing carries into s6.

[c4.gal.1] {gal} The chips you'll use in the Hardware Labs are called Gals. {names} Careful, the names are almost the same. {gla} A G-L-A is a generic logic array. {galname} A Gal is generic array logic. {fixed} A Gal is a modified G-L-A, with a fixed or plane, just like a PAL.

[c4.gal.2] {figure} Here's the slide's picture. {rails} Inputs A and bee, with their complements, and the fed-back state, all run across the and plane. {groups} Each or gate has its own group of and gates. {gaps} The dotted gaps mean there are more and gates, and more outputs, than the picture shows. {ffs} Each or gate feeds a dee flip-flop, with outputs from eff zero down to eff N, {clk} and one clock signal drives them all.

[c4.gal.3] {cost} So a Gal pays the PAL's price. Each product term serves only one function. {same} Even if two functions need exactly the same term, each one has to make its own copy. {gain} The benefit is that there's no programmable or plane, so the device is simpler and faster. {depends} How much the price matters depends on the logic. You'll see a real case in a moment.

[c4.gal.4] {hand} And nobody removes the connections by hand. {type} In the lab, you type in the next-state logic you need. {compiler} A compiler then works out which connections to keep and which to remove, and the chip is programmed with them. {pause}

## Scene 6 · The synchroniser in a GAL (ch4_s6_sync)

> {sync}: s5's GAL moves to the lower right. At the upper left, L10 ch5 s3's diagram, small, in its layout: Sync top left, Hunt top right, Sight below between them; YELLOW names, GREEN codes `[10]`, `[00]`, `[01]`; arcs labelled `r̄`, `r`, `ē`, `e·r`, `e·r̄` (BLUE). {states}: the three circles light in turn. {inputs}: chips `e` and `r` (BLUE). {output}: a GREEN `s = 1` tag by Sync. {ffs}: two D flip-flop boxes `s1`, `s0` (GREEN outputs) beside the diagram.
> {eqs}: L10's equations under the diagram, coloured as its K-map loops: `D1 = s1·ē + s1·r + s0·e·r` (PINK, PURPLE, TEAL) and `D0 = s0·ē + s̄1·s̄0·r` (PINK, PURPLE), D1 and D0 BLUE. {products}: GOLD "3 products" under D1, "2 products" under D0.
> {rails}: the GAL's input labels `a`, `b` transform into `e`, `r` (BLUE); its rails read `e`, `ē`, `r`, `r̄`. {fed}: the GREEN feedback rails gain labels `s1`, `s̄1`, `s0`, `s̄0`, and the flip-flop outputs `f0`, `fn` become `s1` (top, D1) and `s0` (bottom, D0). {eight}: GOLD "8 rails". The GAL now has five AND gates, three in the top group, two in the bottom, with every crossing a faint dot (40).
> {d1gates}: the top group's three AND gates light. Each term flies from the D1 equation down onto its gate (TransformFromCopy), and the gate takes the term's colour: {pink} `s1·ē` PINK, {purple} `s1·r` PURPLE, {teal} `s0·e·r` TEAL. {d0gates}: the bottom group's two gates light; {pink0} `s0·ē` PINK, {purple0} `s̄1·s̄0·r` PURPLE. {loops}: small ghosts of L10 ch5 s6's and s7's K-maps flash beside the equations, each loop pulsing with its gate.
> {dots}: on each gate, the dots its term needs light in the gate's colour (`s1·ē`: `s1`, `ē`; `s1·r`: `s1`, `r`; `s0·e·r`: `s0`, `e`, `r`; `s0·ē`: `s0`, `ē`; `s̄1·s̄0·r`: `s̄1`, `s̄0`, `r`), and every other dot fades. {kept}: GOLD "12 kept of 40". {unused}: the `r̄` rail goes DIM, tag "unused". {state}: the two flip-flops pulse, `s1` and `s0` GREEN. {out}: the `s1` output is relabelled `s` (GREEN), tag "s = s1"; the `s0` output pin goes DIM.
> {cost}: a YELLOW "?" over the fixed OR plane. {none}: s3's RED "made twice" tag flashes as a ghost and fades; GREEN tag "nothing shared". {five}: GOLD "5 AND · 2 OR · 2 flip-flops". {compiler}: s5's "equations → compiler → connections" row appears small beneath, the equations box now holding D1 and D0.
> Checked (exhaustive, Python 3.11.9): D1 and D0 give the diagram's next state in all 12 used (state, e, r) combinations; s = s1 is 1 only in Sync; 8 rails × 5 AND gates = 40 crossings, 12 kept, 28 removed; r̄ is unused; no product term appears in both D1 and D0.

[c4.sync.1] {sync} Let's see what the compiler would make of a machine you know, Lecture ten's frame synchroniser. {states} It has three states, Hunt, Sight and Sync, {inputs} two inputs, ee and ar, {output} and one output, called ess, which is one only in the Sync state. {ffs} Two flip-flops, S one and S zero, hold the state.

[c4.sync.2] {eqs} Lecture ten's K-maps gave the logic for their dee inputs. {products} Three products for dee one, and two for dee zero. {rails} In the Gal, inputs A and bee become ee and ar. {fed} The feedback wires carry S one and S zero, with their complements. {eight} That's eight wires across the and plane.

[c4.sync.3] {d1gates} The or gate for dee one gets three and gates, one per product. {pink} They make S one and not ee, {purple} S one and ar, {teal} and S zero and ee and ar, all three together. {d0gates} The or gate for dee zero gets two, {pink0} for S zero and not ee, {purple0} and for not S one and not S zero and ar. {loops} The colours are the loops from Lecture ten's K-maps. Each loop has become one and gate.

[c4.sync.4] {dots} Each of the and gates keeps only the connections its product needs. {kept} That's twelve connections kept, out of forty. {unused} The wire for not ar goes unused. {state} The pair of flip-flops holds S one and S zero, {out} and the machine's output is simply the output of flip-flop one.

[c4.sync.5] {cost} So did the fixed or plane cost us anything here? {pause} {none} Nothing at all. No product term appears in both functions, so nothing is made twice. {five} Five and gates, two or gates and two flip-flops make the whole machine. {compiler} And going from equations to connections is exactly the job the lab's compiler does for you.

## Scene 7 · Recap and next (ch4_s7_recap)

> {recap}: the screen clears to five empty slots, which fill one per sentence, each a small copy of its scene's visual (same objects, colours and styling) with the sentence's short line under it.
> {r1}: s2's Moore schematic with its two brackets, "combinational logic" and "D flip-flops"; "logic + D flip-flops".
> {r2}: s3's PLA and PAL side by side, the PLA's one YELLOW `a·b̄` gate feeding both OR gates, the PAL's RED second copy, GOLD "3" and "4"; "PLA shares, PAL makes it twice".
> {r3}: s4's GLA with its GREEN feedback rails over the top and the YELLOW CLK; "flip-flops, fed back".
> {r4}: s5's GAL with its fixed OR-plane lines and the small "equations → compiler" row; "fixed OR plane, compiled".
> {r5}: s6's GAL with the five coloured AND gates (PINK, PURPLE, TEAL; PINK, PURPLE) and their 12 dots, GOLD "5 AND · 2 flip-flops"; "the synchroniser".
> {next}: the tiles dim; r5's synchroniser GAL comes to the centre (ch5 s1 opens on it). {fpga}: it shrinks into one tile of a large grid of identical tiles (TEAL outlines), with DIM wires between them, tag "FPGA" (no block count: the slides give none, and the slides' Spartan family has 100 to 784). {lut}: one tile opens to show a small 16-cell table of bits (1s GREEN, 0s DIM, as ch5 s3 draws them) where the AND gates were, tag "lookup table". Then the end card, held ~8 s after the last word while the music carries it.

[c4.recap.1] {recap} Let's recap. {r1} A state machine needs combinational logic and dee flip-flops. {r2} A P-L-A makes sums of products by removing connections. A PAL fixes its or plane, so each product term feeds only one output.

[c4.recap.2] {r3} A G-L-A puts a flip-flop after each or gate, and feeds the state back into the and plane. {r4} A Gal does the same with a fixed or plane, and a compiler picks its connections. {r5} Lecture ten's synchroniser needs only five and gates and two flip-flops. {pause}

[c4.recap.3] {next} Next time, a much bigger kind of chip. {fpga} A Gal holds a handful of flip-flops, but an F-P-G-A, a field programmable gate array, is a whole grid of logic blocks, each with flip-flops of its own. {lut} And in place of and gates, it uses lookup tables. {pause}
