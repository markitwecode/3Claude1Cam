# State Minimisation, Programmable Logic and Circuits: plan

Request: "the next priority after l7 is this latest digital electronics lecture i downloaded."
(2026-10-31). This is Cambridge CST Part IA Digital Electronics (Prof. I. J. Wassell), **Lecture 11**,
recorded Friday 2026-10-30 (confirmed in Decisions). The recording is the source of truth, lined up
with the slides, as in Lecture 10.

Audience: a Cambridge first-year studying the course, who may have watched our Lecture 6, 8 and 10
videos. From L10 they know state assignment, the ⌈log₂ m⌉ flip-flop bound, unused states as don't
cares, the Moore schematic (p. 122), and the frame synchroniser (Hunt, Sight, Sync) with
D1 = s1·ē + s1·r + s0·e·r and D0 = s0·ē + s̄1·s̄0·r. From L6 they know D flip-flops, K-maps and sums
of products. Not in our series: Lecture 9's Mealy machines (p. 123) and the earlier lecture on
PLAs, PALs, ROMs and multiplexers (pp. 64–77). This lecture leans on both, so ch1 s3, ch4 s3 and
ch5 s3 re-teach what it needs.

Sources: the slides (`../source/combined_26.pdf`), pp. 144–170: the whole "Sequential Logic: Further
Considerations" section (pp. 144–162), then "Electronics, Devices and Circuits: Underlying Concepts"
up to Kirchhoff's voltage law (pp. 163–170). Refreshers from pp. 66, 70–73 and 122–123. The
60-min recording (`../source/l11-lecture.{transcript,digest,captions}.md`, frames from
`l11-lecture.mp4`): teaching runs 00:04:21–00:59:57 after ~4 min of setup, and the recording ends
mid-sentence while KVL is being explained. Where the digest disagrees with the slides or the frames,
they win (see Decisions).

Total: 6 chapters, ~61.5 min of narration (~9,850 words), 47 scenes.

The lecture has three parts, so the chapters do too:
- removing redundant states (ch1–ch3, ~27 min of lecture);
- building state machines on programmable chips (ch4–ch5, ~13 min);
- the start of the electronics half of the course (ch6, ~15 min).

Every table, pass, equivalence, LUT content and number below was checked in Python (Decisions,
"Checked"). Script-writers still check their own.

Lecture-wide conventions (set in ch1, kept to the end):
- **Notation, as on the slides.**
  - State tables keep each slide's header words: p. 145 "Current State | Next State X=0 X=1 |
    Output (Y) X=0 X=1"; p. 150 "Present State | Next State X=0 X=1 | Output (Y)". Narration always
    says "current state".
  - States are capital letters: A–P on p. 145 (15 states; there's no O), A–H on p. 150. The input is
    X and the output is Y, both capitals. Generic states are p and q, with primes for next states
    (p′, q′), as in the course's Q′.
  - Equivalent: ≡, said "is equivalent to". Not equivalent: ≢. The slides' bullets write ≠; we use ≢
    so the negation matches the ≡ (see Decisions).
  - Implication-table cells are named by their pair with a hyphen, column letter first ("A-B"), as on
    the slides. Implied pairs are written the same way, in alphabetical order (p. 152 writes "B-F"
    for next states F and B).
  - **Crosses** are two diagonals across the whole cell, as p. 152 draws them, never a letter X.
    This course already uses X for don't cares, and these tables use X for the input. ch2 s6 says
    so once.
  - Self-implied and same-state pairs are struck through, DIM, as p. 152 strikes "A-D" in the A-D
    cell.
  - Products with a centred dot, sums with +, an overbar for NOT, as in L10. The synchroniser keeps
    L10's labels: Hunt 00, Sight 01, Sync 10 (s1 s0), inputs e and r, output s = s1.
  - Programmable-logic drawings follow pp. 157–158: AND plane on top, OR plane below, flip-flops on
    the right, feedback over the top. Kept connections are dots where a rail crosses an AND gate's
    input line (ours, a common convention; the slides draw only the kept wires).
  - Electronics symbols as on pp. 165–170: I, Q, t, E, V, P, R; V_B for the battery, V_L and P_L
    for the lamp; units C, A, V, J, W, Ω. Voltage arrows point their head at the higher-potential
    end (p. 170's rule, also p. 167's V_B and V_L arrows).
- **Names:**
  - Minimisation: "redundant states"; "row matching"; "identical" (same row) vs "equivalent" (same
    behaviour); "unreachable" (the lecturer's "no way to get to"); "implied pair"; "self-implied";
    "implication table"; "pass" for one run through the table (ours; the slides say "go through
    again"); "Mealy machine", "Moore machine".
  - Programmable logic: "product term" (the slides' "minterm", see ch4 s3); "AND plane", "OR plane";
    PLA, PAL, GLA, GAL, FPGA; "configurable logic block" (CLB); "lookup table" (say this, not
    "LUT"); "multiplexer"; "switch matrix"; "routing channel"; "input-output block"; "combinational
    output" and "registered output"; "hardware description language", "Verilog", "synthesis tool";
    "custom chip" (the lecturer's words), glossed once as an ASIC (ours).
  - Electronics: "conventional current"; "electron flow"; "charge"; "coulomb"; "amp" (the slides'
    Ampere); "electromotive force" (emf); "potential difference" (pd); "voltage" for both; "power";
    "resistance"; "Ohm's law"; "resistor"; "junction" or "node"; "loop"; "Kirchhoff's current law",
    "Kirchhoff's voltage law".
- **Narration:**
  - Letters as in L6/L8/L10: always put a word before a letter. "State ay", "state aitch", "input
    ex", "output why", "flip-flop ess one". LESSONS: a bare "ay" comes out "eye".
  - Capital "K" and "N" for those letters (COURSE.md), so "state K", "state N". I is "eye".
    Untested: "eff", "gee", "aitch", "em", "pee" (F, G, H, M, P). If the voice mangles one, try the
    capital letter, as for K and N.
  - Pairs are said with "and": "states ay and dee", "the cell for ay and bee", "the implied pair dee
    and eff". Never run letters together ("ay-bee").
  - Letters pile up in ch1–ch3, so the screen carries them: every letter spoken lights on screen
    (the row, the cell, the arc) as it's said. After a pair's first reading, use meaning where you
    can: "its two next states", "the cell below", "this promise".
  - Formulas are read by meaning after their first reading, as in L8 and L10: "power is current
    times voltage", not "pee equals eye vee". Units in words: "volts", "amps", "coulombs",
    "joules", "watts", "ohms". "One point six times ten to the minus nineteen coulombs."
  - Acronyms: see the voice notes in Decisions. Prefer the words ("lookup table", "multiplexer",
    "input-output block") where the acronym isn't on screen.
  - Keep L6's "every edge of the clock" and L10's "joined by an or gate". "Sight"/"site" and
    "Sync"/"sink" are homophones for QA.
- **Colours** (the course's roles, extended):
  - State tables: state letters FG; input X BLUE; outputs Y GREEN (a 1 output bright GREEN, 0s FG).
    Mealy arcs are labelled "input/output" with the input BLUE and the output GREEN.
  - **GOLD means "the same"**: matching rows (ch1), surviving cells and merged states (ch3). A
    replaced letter flashes GOLD and becomes the kept letter. An unreachable row goes DIM, then
    leaves.
  - Implication table: crosses RED; implied-pair text FG; the pointer from an implied pair to the
    cell it names is YELLOW (attention, as in L10); output-1 states carry a small GREEN dot beside
    their letter on the table's axes (ch2 s6 onward).
  - Programmable logic: inputs BLUE (a, b; e, r); flip-flop feedback rails GREEN (state bits); D
    inputs BLUE; CLK YELLOW; outputs GREEN; AND and OR planes as DIM-shaded panels, like the slides'
    hatching. In the synchroniser example each product term (its AND gate and kept dots) takes L10
    ch5's K-map loop colour: D1's s1·ē PINK, s1·r PURPLE, s0·e·r TEAL; D0's s0·ē PINK, s̄1·s̄0·r
    PURPLE.
  - FPGA: CLBs TEAL outlines (the slide's green blocks); switch matrices PURPLE; input-output blocks
    DIM; routing wires DIM; a configured route GOLD. LUT bits: 1 GREEN, 0 DIM. Multiplexers are
    trapezoids, as on p. 160.
  - ch5 s7's cost plot: FPGA TEAL, custom chip PINK, the crossing YELLOW.
  - **Electronics (new; L12 should keep them):** electrons BLUE dots with "−"; fixed positive ions
    DIM circles with "+"; conventional current arrows GOLD; voltage arrows (emf and pd) TEAL; battery
    and resistor symbols FG; a lit lamp glows YELLOW (a lamp is a lamp, as in L10).
- **Running visuals:**
  - *The ⌈log₂ m⌉ ladder* (L10 ch1 s4's doubling ladder): ch1 s2 and s7 (15 states → 4 flip-flops,
    7 → 3), ch3 s6 (8 → 3, 6 → 3).
  - *The 15-state diagram* (ours, ch1 s4): p. 145's table drawn in four layers under A, reduced in
    ch1 s5–s6 to the 7-state diagram, which returns in ch3 s7.
  - *The implication table* (ch2–ch3): one drawing, carried across. ch2 ends with 16 crosses and
    column A filled; ch3 opens on exactly that.
  - *L10's synchroniser* (diagram in L10 ch5 s3's layout: Sync top left, Hunt top right, Sight
    below; its equations and loop colours): ch4 s6 in a GAL, ch5 s3 and s5 in one CLB.
  - *The GAL drawing* (ch4 s5–s6) returns small in ch5 s1.
  - *The battery-and-lamp loop* (p. 167) carries ch6: electrons (s2), currents (s3), voltages (s4),
    power (s5); the lamp becomes a resistor (s6), and the loop grows into p. 170's junction and loop
    (s7).
- **Reuse:**
  - From L6 (`../l06-flip-flops-counters/scenes/`): `make_ff`, `and_gate`, `and3_gate`, `or_gate`
    (ch6_s6_circuit.py); `clock_wave()` (ch1_s1_hook.py).
  - From L8 (`../l08-timing-metastability/scenes/`): `chip()` (ch1_s1_hook.py) for chip packages in
    ch4 s1, ch5 s1 and ch5 s7.
  - From L10 (`../l10-state-assignment/scenes/`): no scene files exist yet. If they do when you
    build, copy the ⌈log₂ m⌉ ladder (ch1 s4), the Moore schematic (ch1 s2) and the synchroniser
    diagram (ch5 s3). Otherwise build them in the style L10's PLAN.md describes.

## Chapter 1 · Fewer states, same machine
Slug: ch1_row_matching · ~10 min · Source: pp. 144–147, refresher pp. 122–123 (Lecture 9's Mealy
machine) · Recording: 00:04:21–00:11:57
Goal: explain why redundant states are worth removing; read a Mealy machine's compact state table;
reduce p. 145's 15-state machine to 7 states by row matching, going round until no rows match; and
say why row matching isn't enough in general.
Scenes:
- s1_hook · Hook (~50 s): title card ("State Minimisation, Programmable Logic and Circuits", course
  line "Digital Electronics · Lecture 11", part line "Part 1 · Fewer states, same machine").
  - Last lecture: how to choose the bit codes for a machine's states. It ended on a teaser: some
    designs have more states than they need.
  - Visual: p. 145's machine as a diagram (s4's), 15 circles in four layers under A. Pairs of
    circles at the bottom pulse together.
  - The question: can two different states be impossible to tell apart? And if they are, why keep
    both?
  - The road, in one line: remove states by matching rows (Part 1), then by a stronger test
    (Parts 2–3); build state machines on chips you can program (Parts 4–5); then the course turns to
    electricity (Part 6).
- s2_why · Why fewer states? (~75 s): p. 144, 00:04:21–00:05:18.
  - "Sometimes, when designing state machines it is possible that unnecessary states may be
    introduced." Drawing a diagram state by state, it's easy to add states you didn't need.
  - Fewer states may need fewer flip-flops. The ladder (ours): this chapter's 15 states need 4;
    7 would need 3.
  - Fewer states also leave more unused codes, which are don't cares in the K-maps (L10). So the
    next-state logic may get simpler, and you're freer to choose the assignment (the lecturer,
    00:04:48–00:05:18).
  - "May": the count only drops when you cross a power of two. Part 3 meets a case where it
    doesn't.
- s3_mealy · Mealy machines and the compact table (~95 s): refresher of pp. 122–123, then p. 145,
  00:05:18–00:07:00.
  - Lecture 9 (not in our series; L10 used Moore machines only): in a Mealy machine the outputs
    depend on the current state and the current inputs. So the output belongs on the arc, labelled
    input/output (p. 123). In a Moore machine the outputs depend on the state alone.
  - p. 122's Mealy schematic, small: the output logic is fed by the current state and the inputs.
  - p. 145's compact table: one input X, one output Y. Each row gives the current state, its next
    state for X = 0 and for X = 1 side by side, then the output for X = 0 and for X = 1.
  - Read row A: on 0 go to B, output 0; on 1 go to C, output 0. Draw the two arcs, "0/0" and
    "1/0".
  - Why compact: the two input values sit in parallel columns instead of a row each (the lecturer:
    "rather than a long sequential table").
- s4_tree · The table as a diagram (~65 s): ours, checked.
  - Draw every row's arcs: A → B, C; B → D, E; C → F, G; D to G → H to P. Each of the eight bottom
    states goes back to A on either input (one bundled arrow back to the top).
  - Only two arcs output a 1, both on input 1: from J and from L (GREEN). Every other output is 0.
  - So the machine reads its input four bits at a time and starts again at A. What it's looking
    for comes out in s7.
- s5_hi · H and I (~85 s): pp. 145–146, 00:06:59–00:08:20.
  - Rows H and I: both go to A on either input, and both output 0. The lecturer: "we can't tell
    them apart". Starting in H or in I, nothing you could observe ever differs.
  - So replace I by H wherever I appears as a next state. That's only row D's X = 1 entry, which
    becomes H.
  - Now nothing leads to I. It's unreachable, so delete row I.
  - On the diagram: I's circle merges into H, and D's arc swings over to H.
- s6_cascade · Matches that appear (~105 s): pp. 146–147, 00:08:20–00:11:01.
  - K, M, N and P match H too (A, A / 0, 0). Replace them: E's X = 1 entry (K), F's X = 1 (M), and
    both of G's (N, P) become H. Delete four rows.
  - J and L match each other (A, A / 0, 1), but not H, because their X = 1 output is 1. Replace L
    by J in row F, and delete row L.
  - Look again. Rows D and G now both read H, H / 0, 0. Rows E and F both read J, H / 0, 0. These
    matches weren't there at the start: the replacements created them.
  - Replace G by D and F by E. Row C, which was F, G, becomes E, D. Delete rows G and F.
  - No two rows match now: 15 states have become 7, A, B, C, D, E, H and J (p. 147's table).
  - The rule: keep going round until nothing matches.
- s7_left · What's left (~65 s): ours, checked; p. 147 first bullet.
  - The ladder: 7 states need 3 flip-flops instead of 4, with one code to spare.
  - The 7-state diagram reads like a sentence. After two bits the machine only remembers whether
    they differed (E) or were the same (D). D leads to H, a dead end for this word. From E, a 0
    leads to J, and from J a 1 outputs 1.
  - So the output is 1 exactly when the four-bit word is 0101 or 1001.
  - p. 147: "the procedure employed … is known as row matching." It merges states whose next states
    are identical.
- s8_recap · Recap and next (~60 s): p. 147 second slide, 00:11:01–00:11:57.
  - p. 147: "row matching is not sufficient to find all the equivalent states except for certain
    special cases". Here it happened to find the smallest machine (ours, checked; Part 3 shows how
    we know).
  - Recap with small versions of:
    - the ladder (s2);
    - a "1/0" arc and the compact row A (s3);
    - the 15-state diagram (s4);
    - H and I merging (s5);
    - D, G and E, F lighting up after the replacements (s6);
    - the 7-state diagram with "0101 or 1001" (s7).

  Next time: two states whose rows don't match, and yet no input can ever tell them apart. End card.
Continuity: picks up L10 ch6's teaser. Sets the state-table style, GOLD for "the same", Mealy arcs,
and the merge animation (replace, then delete the unreachable row), which ch3 s6 reuses. The 7-state
diagram returns in ch3 s7.

## Chapter 2 · When are two states the same?
Slug: ch2_equivalence · ~10 min · Source: pp. 148–152 (through the A-G cell) · Recording:
00:11:57–00:20:42
Goal: state when two states are equivalent, and its one-step form (same outputs, equivalent next
states). Explain why it finds more than row matching. Lay out an implication table, cross out the
pairs whose outputs differ, and write the implied pairs for column A.
Scenes:
- s1_hook · Hook (~50 s): part line "Part 2 · When are two states the same?"
  - Last time: row matching merged states whose rows were identical.
  - p. 150's 8-state table (one output per state). Ours, checked: no two rows are identical, so
    row matching finds nothing.
  - Yet run states A and D side by side on the same inputs, 0, 1, 1, 0. A visits A, D, E, A, D; D
    visits D, A, C, D, A. Different states all the way, but both output 0, 0, 1, 0, 0.
  - The question: how do we find states that behave the same when their rows don't match?
- s2_definition · Same outputs, for ever (~85 s): p. 148 first slide, 00:11:57–00:13:03.
  - p. 148: "two states, say p and q, can be considered equivalent, i.e., p ≡ q, if from each of
    these states, a finite state machine generates the same output sequence in response to any
    input bit sequence."
  - Equivalent states can be merged: nobody watching the outputs could ever notice.
  - The catch: "any" sequence means infinitely many, of any length. The lecturer: we don't really
    want to apply an infinitely long sequence to check.
- s3_onestep · One step at a time (~100 s): p. 148 second slide, 00:13:03–00:15:06.
  - The practical form: p ≡ q if, for the same input (x_p = x_q), the outputs are the same
    (y_p = y_q) and the next states are equivalent (p′ ≡ q′).
  - p. 148's diagram: p → p′ and q → q′, each arc labelled input/output, with ≡ between p′ and q′.
  - Why it works (ours, two sentences): an output sequence is the first output, followed by the
    sequence from the next state. Same first outputs and equivalent next states give the same whole
    sequence.
  - The contrast with row matching: there, p′ and q′ had to be the same state. Here they only have
    to be equivalent. That's how A ≡ D can hold although their next states are D and A, then C and
    E.
- s4_implied · Implied pairs (~80 s): p. 149, 00:15:06–00:17:17.
  - Compare the states two at a time, for the same input.
  - If the outputs differ, they can't be equivalent, and that pair is settled.
  - If the outputs are the same, they're equivalent only if their next states are. Those next-state
    pairs are implied pairs: promises, not facts.
  - p. 149: "Just because a particular pairwise comparison implies that some pairs of next states
    are equivalent, it does not mean they definitely are." A later comparison may show an implied
    pair isn't.
  - Ours, one sentence: p. 150's table has one output per state, like a Moore machine, so we
    compare the two states' outputs. In a Mealy table like Part 1's, compare the output for each
    input value.
- s5_layout · A cell for every pair (~75 s): p. 150, 00:15:11–00:16:45.
  - We need every pair of states. Start from an 8 × 8 grid, A to H both ways.
  - The cells above the diagonal repeat those below it (A with B is B with A), so drop them. The
    diagonal compares a state with itself, so drop it too.
  - What's left is p. 150's staircase: rows B to H, columns A to G, 28 cells, one per pair. The
    top-left cell is A-B.
- s6_outputs · Crosses from the outputs (~70 s): p. 151, 00:17:17–00:19:58.
  - A and C: outputs 0 and 1. Cross the A-C cell. A cross means "not equivalent".
  - Ours: mark each state by its output. A, B, D and G output 0; C, E, F and H output 1 (GREEN dot).
    Every cell with one of each gets a cross: 16 cells at once (4 × 4). The lecturer crosses them
    column by column, which gives the same 16.
  - 12 cells remain, the pairs with matching outputs.
  - Say once: the cross is drawn across the whole cell, as on the slide. It isn't a don't care, and
    it isn't the input X.
- s7_columna · Column A (~85 s): pp. 151–152, 00:17:17–00:20:42.
  - A-B: both output 0. On input 0 they go to D and F; on input 1, to C and H. So A ≡ B needs D ≡ F
    and C ≡ H. Write "D-F, C-H" in the cell.
  - A-D: on 0 they go to D and A, which says "A ≡ D if A ≡ D". That tells us nothing, so strike it
    out (p. 152: self-implied pairs are removed). On 1 they go to C and E. Keep C-E.
  - A-G: B-D and C-H.
  - Column A is done: three cells hold promises, four hold crosses.
- s8_recap · Recap and next (~55 s): recap with small versions of:
  - A and D running side by side with the same outputs (s1);
  - the definition card (s2);
  - p. 148's p/q diagram (s3);
  - "outputs differ: cross; outputs same: implied pairs" (s4);
  - the staircase cut from the grid (s5);
  - the 16 crosses (s6);
  - column A filled (s7).

  Next time: fill in the other nine cells, then test every promise. End card.
Continuity: ch1's table style and row matching (s1, s3). The table drawn here goes on to ch3
unchanged. The A-and-D run returns in ch3 s5.

## Chapter 3 · Solving the implication table
Slug: ch3_implication · ~10.5 min · Source: pp. 152–155 · Recording: 00:20:42–00:31:25
Goal: complete the implication table; cross out cells pass by pass until nothing changes; read the
equivalent pairs from the cells that survive; merge them into p. 155's 6-state table; and explain
why the method finds more than row matching.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 3 · Solving the implication table".
  - Last time: equivalent states, and an implication table with 16 crosses and column A filled.
  - Every open cell holds a promise, such as "A ≡ B, if D ≡ F and C ≡ H".
  - The question: which promises can be kept?
- s2_fill · The other nine cells (~105 s): p. 152, 00:20:42–00:23:44.
  - The lecturer does columns B and C, then: "you just have to keep doing these pairwise
    comparisons". We do all nine, each cell lighting as its pairs are read off the state table:
    - B-D: A-F, E-H. B-G: B-F (H and H is the same state, so it isn't written, 00:22:15).
    - C-E: A-D (C-E itself struck, self-implied). C-F: E-F, B-D. C-H: C-E, D-G.
    - D-G: A-B, E-H.
    - E-F: C-F, A-B. E-H: A-G (C with C isn't written).
    - F-H: C-F, B-G.
  - p. 152's table, complete: 12 cells of promises and 16 crosses.
- s3_pass1 · The first pass (~105 s): pp. 153–154, 00:23:44–00:26:41.
  - Each implied pair names another cell. Follow the pointer (YELLOW). If that cell is crossed, the
    promise is broken, so cross this cell too.
  - Column by column, as p. 153 does:
    - A-B: D-F is crossed, so cross A-B. D and F have different outputs.
    - A-D: C-E isn't crossed, so we can't tell yet. A-G: B-D and C-H aren't crossed yet either.
    - B-D: A-F is crossed, so cross it. B-G: B-F is crossed, so cross it.
    - C-F: B-D was crossed a moment ago, so cross it. Use a cross as soon as it's made.
    - D-G: A-B, cross. E-F: A-B, cross. F-H: B-G, cross.
  - The first pass adds seven crosses (p. 153).
  - At 00:25:32 the lecturer points at a cross that "comes from later on". p. 154's picture
    already shows later crosses. We show the passes in order.
- s4_again · Again, until nothing changes (~80 s): pp. 154–155, 00:26:41–00:27:41.
  - New crosses can break promises we've already checked. p. 154: "we must go through again".
  - Pass 2: A-G (B-D is now crossed), C-H (D-G), E-H (A-G, crossed earlier in this same pass).
  - Pass 3: nothing changes, so stop. p. 155: "all cells with non equivalent states have now been
    Xed out."
  - Ours, checked: the order you check cells in can change how many passes it takes, never the
    result.
- s5_survivors · Promises that hold (~85 s): p. 155, 00:27:41–00:28:35, then ours.
  - Two cells survive. A-D needs C ≡ E, and C-E needs A ≡ D. Each leans only on the other, so
    A ≡ D and C ≡ E: p. 155, "the coordinates of the remaining cells".
  - Ours, why a loop of promises is enough: every cross records a real difference. Follow a crossed
    cell's pairs and you reach two states with different outputs, so some input sequence tells
    them apart. A-B: input 0 takes A to D and B to F, and they output 0 and 1. A-D and C-E only ever
    lead to each other, so no input sequence can separate them. That's Part 2's definition.
  - Callback: Part 2's A and D, side by side.
- s6_merge · Six states (~75 s): p. 155 second slide, 00:28:35–00:29:29.
  - As in row matching: replace D by A and E by C in the next-state columns, then delete rows D and
    E (ch1's merge animation).
  - p. 155's 6-state table: A: A, C / 0; B: F, H / 0; C: C, A / 1; F: F, B / 1; G: B, H / 0;
    H: C, G / 1.
  - Ours, the ladder: 8 states and 6 states both need 3 flip-flops, so none is saved here. But two
    of the eight codes are now unused, and they're don't cares for the next-state logic. That's
    p. 144's "may".
- s7_method · The method (~75 s): 00:29:29–00:31:25.
  - The lecturer's summary, four steps:
    1. compare every pair of states;
    2. where the outputs differ, cross the cell; otherwise write the implied pairs;
    3. go through again and again, crossing every cell with a crossed pair, until nothing changes;
    4. merge the pairs that survive.
  - "More powerful than row matching": row matching needs identical next states, while this finds
    equivalent ones.
  - Ours, checked: Part 1's 7-state machine is already as small as it gets (its table crosses every
    cell). Row matching was enough there; this machine needed the table.
  - The lecturer: the best way to understand it is to have a go. There's an example in the course's
    examples paper.
- s8_recap · Recap and next (~60 s): recap with small versions of:
  - the full table of promises (s2);
  - pass 1's pointers and seven new crosses (s3);
  - pass 2's three crosses, and pass 3 with none (s4);
  - the two surviving cells leaning on each other (s5);
  - the 6-state table (s6);
  - the four steps (s7).

  Next time: we know what to build; now, how to build it, on a chip you can program. End card.
Continuity: ch2's table, exactly as ch2 left it; ch1's merge animation (s6) and 7-state diagram
(s7); the ladder (s6). Closes the minimisation half of the lecture.

## Chapter 4 · State machines on a programmable chip
Slug: ch4_gal · ~9.5 min · Source: pp. 156–158 (through "GAL Devices"), refresher pp. 71–73 (PLA
and PAL, from an earlier lecture) and p. 122 · Recording: 00:31:26–00:35:20
Goal: explain how a PLA or a PAL makes sums of products; how the GLA adds D flip-flops and feeds
their outputs back to make a state machine; how the GAL (used in the Hardware Labs) differs; and
show L10's synchroniser laid out in a GAL.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 4 · State machines on a programmable chip".
  - Last time: removing redundant states, so the design is as small as it can be.
  - L10's designs ran on separate chips in the lecturer's simulator: AND, exclusive-or and
    flip-flop packages, wired by hand.
  - Visual: those chips and wires gather into one chip package (L8's `chip()`).
  - The question: how can one chip become whatever state machine you need?
- s2_needs · What a state machine needs (~65 s): p. 156 first slide, 00:31:26–00:31:53.
  - The lecturer: combinational logic and D flip-flops. p. 122's Moore schematic, small: inputs and
    the current state feed the next-state logic, which feeds the flip-flops, then optional output
    logic.
  - You can build it from separate chips, as in the labs, or with programmable devices, also in the
    labs.
  - p. 156: "programmable logic can be used to implement combinational logic circuits, i.e., using
    PLA devices". So first, a reminder of those.
- s3_plapal · PLAs and PALs (~130 s): refresher of pp. 71–73 (an earlier lecture, not in our
  series); the lecturer's "remember the PALs" at 00:31:53–00:32:20.
  - A PLA, a programmable logic array (p. 72): inputs a, b, c, each with its complement, run as
    rails across the AND plane. Every AND gate starts connected to every rail. Programming removes
    the connections you don't want ("controlled by fuses or memory bits"), so each AND gate makes
    one product term.
  - The OR plane: each OR gate combines whichever product terms you keep, giving outputs f0, f1,
    f2, each a sum of products, the form a K-map gives.
  - Ours, one sentence: the slides call the AND outputs minterms. Strictly a minterm uses every
    variable, and these needn't, so we say product terms.
  - A PAL (pp. 72–73) has a fixed OR plane: each OR gate has its own AND gates. A product term
    can't be shared between outputs, so if two outputs need the same term it's made twice. The
    structure is simpler, at the cost of efficiency.
  - Ours: two outputs that both need a·b̄. The PLA makes it once and feeds both OR gates; the PAL
    makes it twice.
- s4_gla · Add flip-flops, feed them back (~95 s): pp. 156–157, 00:32:20–00:34:00.
  - A GLA, generic logic array (p. 156): a PLA with a D flip-flop after each OR gate, all on one
    clock.
  - The flip-flop outputs are fed back into the AND plane as extra rails, beside the inputs. Now
    the AND plane sees the inputs and the current state: p. 122's schematic on one chip.
  - p. 157's figure, rebuilt: three inputs with complements, two AND gates, two OR gates, two
    flip-flops, feedback over the top. The lecturer: in reality not-Q is fed back too, but he ran
    out of space on the picture. We draw both.
  - Both planes are programmable, which makes it quite a complex device.
- s5_gal · The GAL (~85 s): pp. 157–158, 00:34:00–00:35:20.
  - The GAL, generic array logic, is what the Hardware Labs use (p. 157). It's a GLA with a fixed
    OR plane, PAL-style. p. 158's figure: inputs a and b, AND gates, each OR gate with its own AND
    gates, flip-flops with outputs f0 to fn, CLK.
  - The cost: product terms can't be shared between functions. The benefit: no programmable OR
    plane, so the device is simpler and faster.
  - Nobody removes connections by hand. In the lab you type in the logic you need, and a compiler
    works out which connections to keep (00:34:44–00:35:20).
- s6_sync · The synchroniser in a GAL (~95 s): ours, checked; callback to L10 ch5.
  - L10's synchroniser, small: Hunt, Sight and Sync; inputs e and r; output s = s1. Its equations:
    D1 = s1·ē + s1·r + s0·e·r and D0 = s0·ē + s̄1·s̄0·r.
  - In p. 158's GAL, inputs a and b become e and r. The feedback rails carry s1 and s0 and their
    complements.
  - D1's OR gate gets three AND gates: s1·ē (PINK), s1·r (PURPLE), s0·e·r (TEAL). D0's gets two:
    s0·ē (PINK), s̄1·s̄0·r (PURPLE). These are L10's K-map loop colours: each loop became one AND
    gate.
  - The kept connections light as dots, and every other connection fades. The flip-flops hold s1
    and s0, and the output s is just s1's flip-flop.
  - No term is needed twice, so the fixed OR plane costs nothing here. This is what the lab's
    compiler works out for you.
- s7_recap · Recap and next (~55 s): recap with small versions of:
  - the Moore schematic (s2);
  - the PLA and the PAL side by side, one shared term and one made twice (s3);
  - the GLA with its feedback (s4);
  - the GAL (s5);
  - the synchroniser's five coloured AND gates (s6).

  Next time: a GAL holds a handful of flip-flops. An FPGA is a whole grid of logic blocks, with
  lookup tables instead of AND gates (no block count: the slides give none). End card.
Continuity: L10's Moore schematic and synchroniser (diagram, equations, K-map loop colours); L8's
chip drawing. The GAL drawing returns in ch5 s1; the synchroniser returns in ch5 s3 and s5.

## Chapter 5 · Inside an FPGA
Slug: ch5_fpga · ~10.5 min · Source: pp. 158 (FPGA)–162, refresher pp. 66, 70–71 and 73 ·
Recording: 00:35:20–00:44:37 (the screen is blank from 00:42:40)
Goal: describe an FPGA's array of configurable logic blocks, routing and input-output blocks;
explain lookup tables; read the Spartan CLB (two 4-input lookup tables, one 3-input, two flip-flops,
multiplexers); say how an FPGA is configured; and say when an FPGA beats a custom chip.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 5 · Inside an FPGA".
  - Last time: the synchroniser in a GAL, five AND gates and two flip-flops.
  - p. 158: field programmable gate arrays are "the latest type of programmable logic". Ours, one
    sentence: "field programmable" means you program it yourself, after it's made.
  - Visual: ch4's GAL shrinks into one tile of a large grid of tiles.
  - The question: what's in each tile, and how does a blank chip become your circuit?
- s2_array · Blocks, wires and switches (~90 s): pp. 158–159, 00:35:20–00:37:10.
  - An array of configurable logic blocks, CLBs. The lecturer nearly says "complex", then
    "configurable, that's the word". They're all identical, and all programmable.
  - Routing channels run between them: wires, plus programmable switch matrices where the wires
    cross (p. 159's second figure, with its crossbar inset). The switches can connect any block to
    any other.
  - Input-output blocks round the edge: "some nice big transistors", so the chip's pins can drive
    real loads. Logically they do nothing.
  - p. 159's first figure is Xilinx's Spartan block diagram. Leave out its corner blocks, which the
    lecture doesn't discuss.
  - p. 158: you configure it by specifying the contents of the lookup tables and the select signals
    of the multiplexers.
- s3_lut · A lookup table (~85 s): refresher of pp. 66 and 70–71 (an earlier lecture).
  - A ROM (p. 70) is a lookup table: its input lines give an address, and out comes the word stored
    there. p. 66 calls a multiplexer used this way "a hardware look-up table".
  - A 4-input lookup table: the four inputs form an address from 0 to 15, and each of the 16
    locations stores one bit, the function's value for that input. Store a truth table, and the
    table is that function. Any function of four variables fits.
  - Ours, checked: store the synchroniser's D1, with address bits s1 s0 e r: rows 00, 01, 10, 11 of
    s1 s0 read 0000, 0001, 1101, 1101 across e r = 00, 01, 10, 11. The 11 row is the unused state;
    it stores what the equation gives.
- s4_clb · The Spartan's logic block (~105 s): p. 160, 00:37:10–00:40:56.
  - p. 160's CLB, built up piece by piece:
    - two 4-input lookup tables, G (inputs G1–G4) and F (F1–F4);
    - a 3-input lookup table, H, which can combine G's output, F's output and one more input, H1;
    - two combinational outputs: Y comes from G or H, and X from F or H;
    - two D flip-flops giving registered outputs YQ and XQ. Their D inputs are chosen from DIN, F, G
      or H. Each also has a clock and two control pins the lecture doesn't use.
  - Every trapezoid is a multiplexer "controlled by configuration program". The lecturer: all of
    it is programmable, the multiplexers and the logic in the tables.
  - The slide's slip: the F table's output is labelled G. The lecturer (00:39:25): "someone noticed
    ages ago", and it should say F. Draw it as F.
- s5_oneclb · What one block can do (~85 s): p. 161 first slide, 00:39:07–00:39:25 and
  00:41:06–00:41:16; then ours, checked.
  - Each CLB can make up to two combinational and/or two registered functions.
  - Each function can use at least 4 input variables, and up to 9: G1–G4 into G, F1–F4 into F, and
    both into H with H1. That's two levels of tables, two feeding a third.
  - Ours: the whole synchroniser fits in one CLB. D1 depends on s1, s0, e and r, four variables, so
    it fits the G table (s3's 16 bits). D0 goes in the F table: 0101, 1100, 0000, 1100. The
    flip-flops behind them hold s1 (YQ) and s0 (XQ). Routing brings s1 and s0 back to the tables'
    inputs, and the output s is YQ.
  - Ch4's GAL needed five AND gates, two OR gates and two flip-flops. Here it's two 16-bit tables
    and two flip-flops.
- s6_configure · Programming an FPGA (~85 s): pp. 161–162, 00:41:16–00:42:40.
  - Nobody sets the table bits and switches by hand. You describe the design in a hardware
    description language, such as Verilog, or as a schematic. The synthesis tool works out the
    table contents, the multiplexer settings and the routing, and that configuration is downloaded
    to the FPGA.
  - p. 161: Xilinx devices keep their configuration in static RAM, so they're easy to reprogram.
    Ours, via p. 73: static RAM loses its contents when the power goes. So the configuration is
    loaded again at every power-up, from a computer or from an EEPROM chip.
  - p. 162: there are other manufacturers, for example Altera, each with many product lines. They
    differ in the number of CLBs, their structure, internal or external ROM, and extras such as
    arithmetic blocks and user RAM.
  - The lecturer: the Spartan's is "quite an old FPGA architecture". Some modern FPGAs even have a
    processor, an ARM core, beside the logic.
- s7_custom · FPGA or custom chip? (~80 s): 00:42:49–00:44:37 (no slide; the screen is blank).
  - An FPGA can be reprogrammed, so it's ideal for prototypes. The lecturer: "if it doesn't work,
    who could imagine that?", you reprogram it until it does. It also suits small numbers of
    products.
  - For millions of units, design a custom chip (ours: often called an ASIC, an application-specific
    integrated circuit). Designing it and making its masks costs a lot up front, but after that each
    extra chip is really cheap. Each FPGA costs more.
  - Ours: total cost against the number made. The FPGA line starts low and climbs steeply; the
    custom-chip line starts high and climbs slowly; they cross. Below the crossing, use FPGAs; above
    it, a custom chip. No numbers: the lecturer gave none.
- s8_recap · Recap and next (~55 s): recap with small versions of:
  - the array of blocks, switch matrices and input-output blocks (s2);
  - a lookup table holding 16 bits (s3);
  - the CLB with F, G, H and its two flip-flops (s4);
  - the synchroniser in one CLB (s5);
  - design → synthesis tool → static RAM in the chip (s6);
  - the two cost lines crossing (s7).

  Next time: "a slight change of topic" (00:44:44). Every gate in these chips is built from
  transistors, and to understand transistors we start with electricity itself. End card.
Continuity: ch4's GAL (s1, s5) and the synchroniser (s3, s5); L8's chip drawing (s7). Hands over to
ch6, the electronics half of the course.

## Chapter 6 · Electricity, from charge to Kirchhoff
Slug: ch6_electricity · ~11 min · Source: pp. 163–170 (through the KVL equation) · Recording:
00:44:41–00:59:57 (the recording ends while KVL is being explained)
Goal: explain current as drifting charge, and why conventional current runs the other way. Define
the coulomb, the amp, and the volt both as emf and as potential difference. Derive P = IV, state
Ohm's law, and apply Kirchhoff's current and voltage laws to the slide's examples.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 6 · Electricity, from charge to Kirchhoff".
  - Last time: FPGAs, made of logic blocks, made of gates.
  - The course turns a corner (p. 163): "Electronics, Devices and Circuits". p. 164's road:
    underlying concepts first (circuits, circuit theory, materials), then transistors and how gates
    are built from them, in the lectures to come.
  - The question: when a gate's output changes, what is actually moving in the wire?
- s2_electrons · Electrons in a metal (~90 s): pp. 164–165, 00:45:24–00:47:50.
  - A current is charged particles moving in a definite direction: electrons in metals, electrons
    and ions in gases or liquids.
  - In a metal, fixed positive ions sit in a lattice. Their outer electrons are held so loosely that
    they're free to roam. At room temperature they move at random, so there's no net flow, and no
    current.
  - Connect a wire across a battery, and the battery acts as an "electron pump". It forces the free
    electrons to drift toward its positive terminal, and through it.
  - The drift is slow, under a millimetre per second, because the electrons keep bumping into the
    ions. But they all start together the moment the battery is connected, like the carriages of a
    train (the lecturer).
  - A current shows itself: the wire warms up, and a compass needle nearby deflects.
- s3_current · Which way, and how much (~100 s): pp. 165–166, 00:47:50–00:50:11.
  - Before electrons were discovered, current was imagined as positive charges flowing out of the +
    terminal toward the −. That's still the definition of conventional current, + to −, the
    opposite way to the electrons in a metal. p. 165's loop: GOLD current arrows one way, BLUE
    electrons the other.
  - Charge is measured in coulombs. One electron carries 1.6 × 10⁻¹⁹ C, so one coulomb is
    6.25 × 10¹⁸ electrons.
  - One coulomb passing a point every second is a current of one amp: I = Q/t. Current is the rate
    of flow of charge.
  - Ours, optional: a milliamp is 6.25 × 10¹⁵ electrons every second.
- s4_volts · Volts: energy per coulomb (~100 s): p. 167 and p. 168's first bullet, 00:50:11–00:52:53.
  - p. 167's circuit: a battery and a lamp. The battery supplies the force and the energy that drive
    the electrons round.
  - The number printed on a battery ("one and a half volts or something") is its electromotive
    force, V_B. It's 1 volt if the battery gives 1 joule of electrical energy to each coulomb of
    charge passing through it.
  - The lamp does the opposite, turning electrical energy into heat and light. The potential
    difference across it, V_L, is 1 volt if it converts 1 joule for each coulomb passing through:
    V_L = E/Q.
  - Both are measured in volts, so both are usually just called voltages (p. 168).
- s5_power · Power (~60 s): p. 168 first slide, 00:52:53–00:54:50.
  - Power is energy per second: P_L = E/t, joules per second, which is watts.
  - From V_L = E/Q, E = Q·V_L, so P_L = Q·V_L/t. From I = Q/t, Q = I·t, so P_L = I·t·V_L/t, and the
    t's cancel: P_L = I·V_L. Show each substitution as a step.
  - The power in any device is the current through it times the voltage across it. "Hopefully
    familiar." Ours: 0.2 A through a lamp with 1.5 V across it is 0.3 W.
- s6_resistance · Resistance and Ohm's law (~95 s): pp. 168–169, 00:54:53–00:57:08.
  - The engineer's view of potential difference (p. 168): conductors oppose the flow of current, to
    a greater or lesser extent. That opposition is resistance, R. For a given current, the bigger
    the resistance, the bigger the voltage across the conductor.
  - R = V/I, usually written V = IR: Ohm's law. Resistance is measured in ohms (Ω).
  - For an ohmic, linear conductor, current plotted against voltage is a straight line through the
    origin. No voltage, no current.
  - Resistors are conductors made to have a specific resistance. The symbol (p. 169) is a rectangle
    labelled R Ω. In the lab they're "little tiny things with coloured bars", and the bars give the
    value.
  - p. 169's analogy (on the slide, not spoken): charge in a conductor is like water in a pipe. It
    takes a pressure difference, a voltage, to make it flow.
  - Visual: s4's lamp is swapped for a resistor.
- s7_kirchhoff · Kirchhoff's two laws (~120 s): p. 170, 00:57:08–00:59:57, completed from the slide.
  - Kirchhoff's current law: the currents entering a junction (a node) add up to zero. Count
    currents in as positive and out as negative: I1 + I2 − I3 = 0, so I1 + I2 = I3. What goes in
    comes out, like water at a pipe junction. Ours: 2 A and 3 A in, 5 A out.
  - Kirchhoff's voltage law: around any closed loop, the voltages add up to zero.
  - Each voltage gets an arrow whose head points to the end at the higher potential, such as a
    battery's + end.
  - Choose a direction for the current and stick to it. If the answer comes out negative, the
    current really flows the other way. The recording ends here.
  - From the slide: walk round p. 170's loop clockwise, starting up through V1. Add a voltage whose
    arrow points the way you're walking, and subtract one that points against you. That gives
    V1 − V2 − V3 − V4 − V5 + V6 = 0. The loop has three batteries (V1, V3, V6) and three resistors
    (Ra, Rb, Rc, with voltages V2, V4, V5).
  - Ours, checked, optional: with V1 = 5 V, V3 = 1 V, V6 = 2 V, and 1 A flowing through
    Ra = 1 Ω, Rb = 2 Ω and Rc = 3 Ω, Ohm's law gives V2 = 1 V, V4 = 2 V and V5 = 3 V, and
    5 − 1 − 1 − 2 − 3 + 2 = 0. Don't solve for the current: next lecture's potential divider does
    that.
- s8_recap · Recap, the lecture, and next (~50 s): recap with small versions of:
  - drifting electrons and the train (s2);
  - the opposite arrows, and I = Q/t (s3);
  - the battery and lamp with V_B and V_L (s4);
  - P = IV's two substitutions (s5);
  - the straight line and the resistor symbol (s6);
  - the junction and the loop (s7).

  Optional, the lecture in one line: shrink the machine, put it on a chip, then ask what the chip
  runs on.

  Next lecture: p. 170's last line, "we will now analyse a simple 2 resistor circuit known as a
  potential divider". End card.
Continuity: a new section; it sets the electronics symbols and colours for Lecture 12. The
battery-and-lamp loop runs through s2–s6 and grows into p. 170's junction and loop in s7. Its
emf/pd arrows follow the same rule as KVL's.

## Decisions
- **Lecture number: 11, confirmed.** The file was recorded Friday 2026-10-30 (12:51 UTC), which is
  Lecture 11 by the course's Mon/Wed/Fri numbering (L10 = Wed 10-28). The recording agrees:
  - it opens on p. 144's title slide, "Sequential Logic: Further Considerations" (frame at
    00:03:30), the page right after L10's last slide (p. 143);
  - "today we're going to carry on looking at finite state machines" (00:04:21);
  - "remember the PALs that I described to you" (00:32:00) refers back to pp. 71–73.

  The lecturer never says the number.
- **Scope: pp. 144–170, confirmed from the frames.** That's all of "Further Considerations"
  (pp. 144–162), then "Underlying Concepts" up to KVL. p. 170's KVL slide is on screen at 00:59:50,
  and the recording ends mid-explanation at 00:59:57. Nothing in pp. 144–170 is left out. p. 170's
  last bullet (the potential divider) and pp. 171+ belong to Lecture 12: teaser only.
  - Taken from the slides, because the lecturer skipped them: p. 161's static RAM and EEPROM
    (ch5 s6), p. 169's resistor symbol and water analogy (ch6 s6), and KVL's equation (ch6 s7).
  - In the recording but on no slide: FPGA vs custom chip (00:42:49–00:44:37, blank screen),
    ch5 s7.
- **The electronics part is its own chapter (ch6), not a closing part.**
  - It's bigger than the caption skim suggested: 15 minutes of the lecture (00:44:41–00:59:57,
    ~2,300 spoken words), pp. 163–170, starting at 44:41, not ~50 min.
  - It opens a new section of the course with nothing in common with state machines. Tacked onto
    ch5 it would bury the electronics and swell that chapter past 20 minutes.
  - One chapter (~11 min), not two of ~7. Both would fall below the 8-minute floor, and the second
    would be padding: the lecturer spends only 5 minutes on resistance and Kirchhoff.
  - For Lecture 12's planner: L11 ch6 covers pp. 163–170 through the KVL equation and sets the
    electronics colours (conventions above). L12 can open with one "last time" sentence. If the user
    would rather have it, ch6 could move to the start of L12's project instead.
- **Title: changed to "State Minimisation, Programmable Logic and Circuits".**
  - State minimisation is only ~27 of the ~56 teaching minutes (ch1–ch3). ch4–ch5 are programmable
    logic (the slides' own term, pp. 156, 158), and ch6 is circuits (p. 163, "Electronics, Devices
    and Circuits"; pp. 168–170, "Circuit Theory").
  - This follows L8's three-part title, "Timing, Metastability and Parallelism". It's long, so the
    title card scales it to 12 units wide, as L8's ch1 s1 does.
  - Alternatives, if the user prefers a short card: "State Minimisation" (the old title), or
    "Further Considerations" (the slides' section name, which misses ch6 and says less).
  - The folder keeps its name.
- **Size: 6 chapters, ~61.5 min**, like L6 (61.3 min), L8 (~61) and L10 (~61).
  - The lecturer speaks ~8,100 words in ~56 minutes of teaching. State minimisation takes ~27 min
    (3 chapters), programmable logic ~13 min (2 chapters), electronics ~15 min (1 chapter).
  - Programmable logic grows most, from 13 to 20 minutes. GLAs and GALs are defined as changes to
    PLAs and PALs, and FPGAs by their lookup tables, all from a lecture outside our series, so ch4 s3
    and ch5 s3 re-teach them. The synchroniser built both ways (ch4 s6, ch5 s5) makes the two
    architectures concrete for a student who'll program a GAL in the lab.
  - Electronics shrinks, from 15 to 11 minutes: it's the most repetitive stretch of the lecture,
    and much of it is school physics (the lecturer: "hopefully familiar").
  - **To shorten** (the user may prefer): drop the "ours" extras, ~5 min, keeping 6 chapters at
    ~56 min: ch1 s7's reading of the machine, ch3 s5's argument, the synchroniser (ch4 s6, ch5 s5),
    and ch5 s7's plot.
- **Order: the lecture's, with three small changes:**
  - ch2 s6 crosses all 16 output-differing cells at once. The lecturer crosses them column by
    column, with the same result.
  - ch5 s3 explains lookup tables before the CLB. The lecture names them (p. 158) but never says
    what they are.
  - In ch5, p. 161's first slide (what a CLB can do) goes in s5 and its second (configuration) in
    s6. The lecturer moves back and forth between pp. 160–162 at 00:39:07–00:42:40.
- **Exercises:** pp. 144–170 have none, so there are no hints and no bonus chapter. The lecturer
  points to "an example in the examples paper" (00:31:18), which we don't have. If the user wants a
  bonus of our own, two checked candidates:
  - run the implication table on Part 1's 15-state table (it gives row matching's 7 classes);
  - run it on the 7-state result (every cell is crossed).
- **Student questions:** none in the recording. The transcript's "What are the benefits of using a
  custom chip?" (00:43:58) is a Whisper insertion; the captions don't have it. Likely confusions,
  answered where they arise:
  - matches that appear only after replacements (ch1 s6);
  - three different X's: input, don't care and cross (ch2 s6);
  - why a loop of promises proves equivalence (ch3 s5);
  - why 8 → 6 states saves no flip-flop (ch3 s6);
  - "minterm" vs product term (ch4 s3);
  - conventional current vs electron flow (ch6 s3);
  - emf vs pd (ch6 s4);
  - KVL's signs (ch6 s7).
- **Notation: ≢ for "not equivalent".** The slides' bullets write ≠ ("A ≠ C"), which literally says
  the states are different, and they always are. ≢ says what's meant and pairs with the slides' ≡.
- **Source disagreements (the slides and frames win):**
  - The digest says the p. 145 table has "16 initial states". It has 15: A to P, without O.
  - The digest's 00:10:00 table has row C → D, E. p. 147 has C → E, D (F became E, G became D).
  - The digest's 00:30:00 table is wrong (eight rows, B → C, D …). The frame at 00:30:20 shows
    p. 155's 6-state table, as the digest's own 00:27:38 segment has it.
  - The digest's KVL figure names the resistors R2, R4, R5. The slide's are Ra, Rb, Rc, with
    voltages V2, V4, V5; the batteries are V1, V3, V6. The clockwise current arrow is on the wire
    above V1.
  - The digest says "ASIC" and "NRE" at 00:42:47. The lecturer says "custom chip"; ch5 s7 glosses
    ASIC once, as ours.
  - The digest calls p. 150's machine a "Moore FSM". The slide doesn't say. With one output per
    state it reads like a Moore table (ch2 s4, ours).
  - The digest calls the CLB's flip-flop controls "synchronous". The slide doesn't say, and we
    don't either.
  - The captions' "lab" at 00:53:00 is "lamp" (Whisper has it right).
- **Transcript slips, corrected silently:**
  - 00:17:40–00:17:53: "in the AD box" is the A-B cell (he corrects himself);
  - 00:19:10: "if A is equivalent to E … D equivalent to C and C equivalent to A" is the A-D cell,
    D-A and C-E;
  - 00:23:04: "E and F, E and C … D and A" is the C-E cell, E-C (self-implied) and D-A;
  - 00:25:32: the cross "which comes from later on" (p. 154 shows later crosses);
  - 00:30:44: "the output states are equal" means identical next states;
  - 00:33:59–00:34:28: "minterms" are product terms (ch4 s3);
  - 00:35:47 and 00:36:15: "complex logic blocks" are configurable logic blocks;
  - 00:39:57–00:40:56: the G/F table mix-ups (follow p. 160);
  - Whisper's "VariLog" is Verilog (00:42:33), "energy per coolant" is per coulomb (00:52:44), and
    "three batches" are batteries (00:58:36).
- **Voice notes for the producer:**
  - Letters for state names: "eff", "gee", "aitch", "em" and "pee" aren't in voice.py's `SPELLED`
    or voiceqa.py's `LETTERS`. Add them (→ f, g, h, m, p), or QA will flag every one. "ell" and
    "eye" are already there. K and N are written as capitals (COURSE.md).
  - Acronyms are untested: PLA, PAL, GLA, GAL, FPGA, CLB, ASIC, EEPROM, RAM. In speech PAL and GAL
    are usually words ("pal", "gal"), and the others are spelled out. Whisper writes them all as
    capitals, so QA may flag spelled-out forms.
  - Untested words: "coulomb", "joule", "Kirchhoff", "Verilog", "Xilinx" ("zy-links"), "Spartan",
    "Altera", "emf". Fallbacks: "electromotive force" and "potential difference" in full.
- **Beyond the slides, each short and labelled "ours" in the scene list,** all checked:
  - ch1: flip-flop counts 15 → 4 and 7 → 3 (s2, s7); the diagram of p. 145's table (s4); what the
    machine detects (s7).
  - ch2: row matching finds nothing on p. 150's table, and A and D run on 0, 1, 1, 0 (s1); why the
    one-step form works (s3); comparing outputs in Moore vs Mealy tables (s4); the 16 crosses by
    output (s6).
  - ch3: checking order (s4); why the survivors are equivalent, and A-B's distinguishing input
    (s5); 8 → 6 states keeps 3 flip-flops (s6); the 7-state machine is minimal (s7).
  - ch4: product term vs minterm, and the shared-term example (s3); the synchroniser in a GAL (s6).
  - ch5: "field programmable" (s1); D1's table bits (s3); the synchroniser in one CLB (s5); static
    RAM is volatile, so it's reloaded at power-up (s6, via p. 73); the ASIC gloss and the cost plot
    (s7).
  - ch6: a milliamp in electrons (s3); 0.3 W (s5); the KCL and KVL numbers (s7).
- **Checked** (Python 3.11.9, standard library, exhaustive):
  - Row matching on p. 145 (15 states), in the slides' order (I → H; K, M, N, P → H; L → J;
    G → D; F → E): each pair matches when it's merged. The result is A, B, C, D, E, H, J with
    C → E, D (p. 147). Partition refinement gives the same 7 classes, {A}, {B}, {C}, {D, G},
    {E, F}, {H, I, K, M, N, P}, {J, L}, so row matching found the minimum, and the 7-state table is
    minimal.
  - The 15-state machine: from A, every four-bit word returns to A, the first three outputs are 0,
    and the fourth output is 1 exactly for 0101 and 1001.
  - ⌈log₂ m⌉: 15 → 4, 8 → 3, 7 → 3, 6 → 3.
  - p. 150: no two rows are identical. 28 cells; 16 are crossed by outputs. The 12 open cells match
    p. 152: A-B D-F, C-H; A-D C-E; A-G B-D, C-H; B-D A-F, E-H; B-G B-F; C-E A-D; C-F E-F, B-D;
    C-H C-E, D-G; D-G A-B, E-H; E-F C-F, A-B; E-H A-G; F-H C-F, B-G.
  - Passes in p. 153's order (column by column, using crosses as soon as they're made): pass 1
    A-B, B-D, B-G, C-F, D-G, E-F, F-H; pass 2 A-G, C-H, E-H; pass 3 none. The survivors are A-D
    and C-E.
  - The same passes all at once (each pass only uses earlier passes' crosses): A-B, B-D, B-G; then
    A-G, C-F, D-G, E-F, F-H; then C-H, E-H; then none. Same survivors.
  - Partition refinement on p. 150: {A, D}, {C, E}, the rest alone. A ≡ D and C ≡ E for every input
    sequence up to length 8. From A and from D on 0, 1, 1, 0 the states are A D E A D and D A C D A,
    and the outputs are 0 0 1 0 0 both times.
  - Shortest distinguishing inputs: A-B "0" (D outputs 0, F outputs 1); A-G "00"; C-H "100";
    E-F "10".
  - p. 155's 6-state table follows from the merge and is minimal.
  - Synchroniser (L10's equations): D1 and D0 match all 12 used rows. In a GAL: 5 AND gates, none
    shared; rails e, ē, r, s1, s̄1, s0, s̄0 (r̄ unused). Lookup tables, rows s1 s0 = 00, 01, 10, 11,
    columns e r = 00, 01, 10, 11: D1 0000 0001 1101 1101; D0 0101 1100 0000 1100. The 11 row is
    filled from the equations; it's unused.
  - CLB: 4 + 4 + 1 = 9 inputs. A 4-input table holds 16 bits, so 2¹⁶ = 65,536 functions fit.
  - Electronics:
    - 1 ÷ (1.6 × 10⁻¹⁹) = 6.25 × 10¹⁸ electrons per coulomb;
    - 1 mA = 6.25 × 10¹⁵ electrons per second;
    - 1.5 V × 0.2 A = 0.3 W;
    - KCL: 2 + 3 − 5 = 0;
    - KVL: I = (5 − 1 + 2) ÷ (1 + 2 + 3) = 1 A, so 5 − 1 − 1 − 2 − 3 + 2 = 0.
- **Skipped from the recording:** 00:00:00–00:04:21, setup and room chat. 00:42:40–00:44:41 is a
  blank screen, but the talk over it is ch5 s7.
