# State Assignment: plan

Request: "build lecture 10, i added the video file. do check which lecture it is exactly to line up
with the notes, but yeah, the video is your source of truth." (2026-10-31). This is Cambridge CST
Part IA Digital Electronics (Prof. I. J. Wassell), **Lecture 10**, recorded Wednesday 2026-10-28
(confirmed in Decisions). Audience: a Cambridge first-year studying the course, who may have
watched our Lecture 6 and Lecture 8 videos. From L6 they know D flip-flops (D = Q′), asynchronous
preset and clear, and how to design a synchronous counter: transition table, D columns equal to the
next state, K-maps with Gray-code order and don't cares, unused counts as X. From L8 they know
T_c ≥ t_pc + t_pd + t_su and the shift register. Earlier lectures gave XOR, K-maps and Boolean
algebra. Lecture 9 (Mon 2026-10-26) isn't in our series. It introduced state machines, pp. 120–131:
FSM definitions, Moore and Mealy machines, state diagrams, the traffic-light controller, and
power-up into unused states. This lecture leans on all of it, so ch1 s2–s3, ch3 s3 and ch4 s5
re-teach those parts where they're needed.
Sources: the slides (`../source/combined_26.pdf`), pp. 132–143 (the whole "Synchronous State
Machines 2" section), plus pp. 121–128 for the refresher. The 60-min recording
(`../source/l10-lecture.{transcript,digest,captions}.md`, frames from `l10-lecture.mp4`): teaching
runs 00:05:56–00:59:56, after ~6 min of room chat and lab admin, which we skip. Where the digest
disagrees with the slides or the video frames, they win (see Decisions).
Total: 6 chapters, ~61 min of narration (~9,700 words).

Every table, equation, K-map group, self-start check and gate count below was checked by
enumeration in Python (Decisions, "Checked"). Script-writers still check their own.

Lecture-wide conventions (set in ch1, kept to the end):
- **Notation, as on the slides.**
  - Divide-by-5 flip-flop outputs a, b, c (the ring adds d, e), lowercase. Tables read c b a,
    with a rightmost (pp. 134–137). Next state c′ b′ a′; inputs D_a, D_b, D_c.
  - Circuits are drawn a, b, c left to right, as in the lecturer's simulations. Say once, in
    ch1 s8, that the circuit runs left to right while the table reads right to left.
  - Products with a centred dot (ā·c̄), sums with +, ⊕ for exclusive-or, an overbar for NOT. A
    prime is always "next state", never NOT.
  - The minimum flip-flop count is shown as ⌈log₂ m⌉ and said "log base two of em, rounded up"
    (the slide writes log₂ m; see Decisions).
  - Traffic light: Lecture 9's design has flip-flops R, A, G, one per lamp. The one-hot design
    has flip-flops r, ra, g, a (lowercase, one per state) and lamps R, A, G (uppercase), as on
    pp. 138–139.
  - Synchroniser: states Hunt, Sight, Sync; inputs e and r; output s. Sequential labels s1 s0
    (Hunt 00, Sight 01, Sync 10); one-hot labels s2 s1 s0 (Hunt 001, Sight 010, Sync 100). Next
    states s1′ s0′ (s2′); D inputs D1, D0 (D2).
  - **s1 changes meaning between ch5 and ch6.** It is the high bit (1 only in Sync) in ch5, and
    Sight's flip-flop in ch6. ch6 says so, and each one-hot flip-flop is labelled with its state's
    name throughout ch6.
- **Names:** "state assignment"; "sequential", "sliding" and "shift register" assignment;
  "one-hot" (the slides' "1 hot"); "used" and "unused states"; "don't care"; "self-starting"
  (L9's word, p. 128); "next-state logic", "output logic"; "state transition table"; "state
  diagram"; "arc". "The lecturer's simulator", not "Yenka". "Tripos question", glossed once as a
  Cambridge exam question.
- **Narration:**
  - Letters as in L6/L8: "cue", "dee", "ess", "ar". This lecture adds "ay", "bee", "see" and "ee".
    Always put a word before a letter ("flip-flop ay", "input ee", "column bee"). LESSONS: a bare
    "ay" comes out "eye".
  - Subscripts are said "ess one", "dee two". Capital "K" in "K-map" (COURSE.md).
  - Read Boolean terms by meaning after their first reading, while the term is on screen: "from
    Sight, when ee and ar are both one", not "ess one ee ar". Strings of letters can't be followed
    by ear, just as L8 read its inequalities in words.
  - Traffic-light flip-flops by colour: "the red flip-flop", "the red-and-amber flip-flop".
  - "Exclusive-or" at first use in ch1. Avoid a bare "or gate" after a pause (L6 heard "error
    gate"): "joined by an or gate". Keep "every edge of the clock".
  - "Sight" and "Sync" come back from Whisper as "site" and "sink": homophones, not voice errors.
- **Colours** (L6's roles, extended):
  - CLK YELLOW. External inputs e and r BLUE. Flip-flop outputs and state bits GREEN (current-
    and next-state headers, as in L6's `mod_table()`). D inputs BLUE, as in L6.
  - The machine's output (the divide-by-5 output, s) is GREEN with its label. It's always a
    flip-flop output or an OR of them.
  - The travelling 1s in shift-register-style designs (sliding, ring, one-hot) are GOLD, like
    L8 ch2 s3's moving bit.
  - Unused states DIM (grey circles, grey rows). K-map don't cares X as on the slides. K-map loops
    PINK, PURPLE, TEAL, as in L6 ch6 s5.
  - RED for trouble: trap loops (ch3), the stuck simulations, and the asynchronous set pin and its
    active-low bubble (L6: asynchronous inputs RED).
  - Traffic-light lamps light in their own colours (red, amber, green) and are dark when off. A
    lamp is a lamp, not a signal role. In ch4 trouble shows as all lamps dark, not RED.
- **Running visuals:**
  - *The five-state ring* (L6's `state_ring()` style): the divide-by-5's states in a cycle. The
    codes under the nodes change per assignment: binary (ch1), sliding and ring (ch2). In ch3 the
    unused states are drawn round it.
  - *The waveform:* CLK and the output, high for two periods and low for three (p. 133's
    diagram). Every divide-by-5 design ends by producing it.
  - *The scoreboard:* a small table with columns assignment, flip-flops, next-state gates and
    output logic, grown chapter by chapter (numbers in Decisions, "Checked").
    - ch1: binary (3 flip-flops, 3 gates, none).
    - ch2: sliding (3, 1 gate, none) and ring (5, none, none).
    - ch4: the traffic-light pair. L9: 3, 2 gates (exclusive-or and AND), none. One-hot: 4, none,
      2 OR gates.
    - ch5–ch6: the synchroniser pair. Sequential: 2, 7 gates, none. One-hot: 3, 8 gates, none.
  - *The synchroniser's state diagram* (p. 139), drawn once in ch5 and reused in ch6 with the
    codes swapped.
- **Reuse from L6** (`../l06-flip-flops-counters/scenes/`):
  - `kmap()` (ch6_s4_kmap.py) for every 2 × 4 map in ch1–ch2, with the axes relabelled c and
    b a. `loop_round()`/`map_loops()` (ch6_s5_groups.py) for the loops.
  - `mod_table()`'s styling (ch6_s4_kmap.py) for the transition tables.
  - From ch6_s6_circuit.py: `make_ff(d_text=…)`, `or_gate`, `xor_gate`, `and_gate`,
    `and3_gate`, `led`/`set_led`, `clock_source()`.
  - The switch widgets `toggle`/`flip` (ch2_s6_symbols.py) for the clock switch and the set
    buttons. `state_ring()` (ch4_s2_counters.py). `async_sketch()`, `pin()` (ch3_s6_async.py) for
    the set pin. `clock_wave()` (ch1_s1_hook.py).
  - ch5 needs a new 4 × 4 K-map (rows s1 s0, columns e r). Build it in `kmap()`'s style.
- **Reuse from L8** (`../l08-timing-metastability/scenes/`):
  - `build_chain()`, `digit()`, `pin()` (ch2_s3_shiftreg.py) for the shift-register chains and the
    moving GOLD 1. Its serial-link sketch for ch5 s2.
  - `path_diagram()` (ch1_s4_path.py) and `budget_bar()` (ch1_s6_setup.py) for ch4 s7.

## Chapter 1 · Which bits for which state?
Slug: ch1_assignment · ~11 min · Source: pp. 132–135 (to D_c), refresher pp. 120–126 · Recording:
00:05:56–00:15:08
Goal: say what state assignment is and what it trades off, and give the ⌈log₂ m⌉ minimum. Then
design the divide-by-5 counter with the sequential assignment: transition table, output by
inspection, three K-maps with the unused states as don't cares, and the circuit.
Scenes:
- s1_hook · Hook (~45 s): title card ("State Assignment", course line "Digital Electronics ·
  Lecture 10", part line "Part 1 · Which bits for which state?").
  - The lecture before this one (not in our series) introduced synchronous state machines. A
    short refresher comes first.
  - Visual: the traffic light's four states in a ring, each with its lamps, and a row of
    flip-flops below. Candidate codes cycle under the states:
    - 00, 01, 10, 11 (two flip-flops);
    - 100, 110, 001, 010 (three, Lecture 9's);
    - 1000, 0100, 0010, 0001 (four).
  - The question: states have names, but flip-flops only hold bits. Which pattern should stand
    for which state, and does the choice matter?
  - The road, in one line: one small counter built three ways (Parts 1–2); what happens when a
    machine wakes up in a pattern we never used (Part 3); one-hot (Part 4); a real exam machine
    built two ways (Parts 5–6).
- s2_machines · State machines, briefly (~95 s): refresher of Lecture 9, pp. 120–122.
  - A finite state machine produces outputs that depend on its internal state and its external
    inputs (p. 121).
  - On a state diagram, states are circles. Arcs between them carry the input conditions that
    cause each transition.
  - p. 122's Moore schematic: inputs and the current state feed the next-state logic, which feeds
    the D flip-flops, then optional output logic. One clock.
  - Counters are the special case with no inputs (p. 120), so L6's counters were state machines
    all along.
  - Moore vs Mealy, one sentence: in a Moore machine the outputs depend on the state alone, and
    every machine in this lecture is one. A Mealy machine's outputs also depend directly on the
    inputs.
  - The recipe (L6 ch6 s8's procedure, extended): state diagram → state transition table →
    next-state logic → output logic, if any. With D flip-flops the D inputs are just the next
    state.
- s3_traffic · The traffic light's codes (~80 s): Lecture 9's example, pp. 124–125.
  - Four states in the UK order, red → red-and-amber → green → amber → red, driven by the clock
    alone.
  - Two flip-flops would be enough. Lecture 9 used three, one per lamp (R, A, G): red 100,
    red-and-amber 110, green 001, amber 010. Each lamp is simply its flip-flop's output, so there
    is no output logic.
  - The other four patterns (000, 011, 101, 111) never occur. They're unused states, and the
    K-maps treat them as don't cares.
  - That choice of codes was a state assignment, today's subject. Its next-state logic comes back
    in Part 4.
- s4_choice · What makes a good assignment? (~80 s): p. 132, p. 133 first slide, 00:06:19–00:07:13.
  - The choice isn't obvious: it depends on what you optimise.
    - Complexity, which depends on the technology (an FPGA, or 74-series chips like those in the
      lecturer's simulations). A flip-flop may take less chip area than its gate drawing
      suggests, and wiring can matter as much as gates.
    - Speed.
  - Algorithms for the best assignment exist, but they aren't for working by hand.
  - The lower bound: m states need at least log₂ m flip-flops, rounded up. Show the doubling
    ladder, 1, 2, 3, 4 flip-flops giving 2, 4, 8, 16 patterns. 8 states need 3, 5 states need 3
    (two give only four patterns), and 3 states need 2.
  - More than the minimum is allowed (the traffic light used 3 for 4). Today some assignments use
    more on purpose. The lecturer: some of these are "just a bit of fun", to show how creative you
    can be.
- s5_divide5 · The divide-by-5 counter (~55 s): p. 133 second slide, 00:07:13–00:08:30.
  - The specification: the output is 1 for two clock edges and 0 for three, then repeats. There
    are no inputs, only the clock.
  - Draw CLK and the output (p. 133's diagram): one output cycle per five clock periods, so five
    states.
  - It's called a divide-by-5 counter because the output goes round once every five periods of
    the clock. Ours, one sentence: like L6's frequency dividers, but by five.
  - Five states need three flip-flops (s4). Call their outputs c, b, a.
- s6_count · Counting in binary (~85 s): p. 134, 00:08:30–00:10:12.
  - Sequential assignment: give the states an increasing binary count, 000, 001, 010, 011, 100,
    and back to 000.
  - Fill in the transition table (current c b a → next c′ b′ a′) row by row, as the lecturer
    reads it.
  - Unused states: 101, 110, 111.
  - Output by inspection: flip-flop b's column reads 0, 0, 1, 1, 0. That's high for two states
    in a row and low for three, going round. So the output is just b, with no output logic. The
    lecturer: "that's just a fluke".
  - With D flip-flops the next-state columns are the D inputs (s2).
- s7_kmaps · Three K-maps (~115 s): pp. 134–135, 00:10:12–00:13:40.
  - Rows c = 0 and 1; columns b a in Gray-code order 00, 01, 11, 10; unused states as X.
  - The lecturer's "we have to do Gray coding of these assignments" (00:11:33) means the map's
    order, not the state codes. Say it that way.
  - D_a: 1s at 000 and 010, the two ends of row 0, adjacent by wrap-around. D_a = ā·c̄. The X's
    can't make a bigger group, so leave them out.
  - D_b: 1s at 001 and 010, each paired with the X below it: a·b̄ and ā·b. So
    D_b = a·b̄ + ā·b = a ⊕ b, the exclusive-or.
  - D_c: one 1 at 011, paired with the X at 111. D_c = a·b.
- s8_circuit · The circuit, and recap (~95 s): 00:13:48–00:15:08.
  - Three D flip-flops on one CLK line:
    - an AND of the not-a and not-c outputs into D_a;
    - an exclusive-or into D_b;
    - an AND into D_c;
    - the output taken from b.
  - Drawn a, b, c left to right, as in the lecturer's simulation (see conventions).
  - Re-enact the demo: a 1 Hz clock (YELLOW) and the output (GREEN), high for two periods, low
    for three. The simulator plots the clock red and the output blue; we keep our colours.
  - The scoreboard starts: binary, 3 flip-flops, 3 gates, no output logic.
  - Recap with small versions of:
    - the codes under the traffic light (s3);
    - the log₂ ladder (s4);
    - the waveform (s5);
    - the table with b's column lit (s6);
    - the three K-maps (s7);
    - the circuit (s8).

  Next time: the lecturer's "more funky" assignments. What if the codes are chosen so that the
  logic almost disappears? End card.
Continuity: sets the notation, colours, waveform, K-map style and scoreboard. The divide-by-5 is
the running example through ch3. The traffic light returns in ch4; the state-diagram vocabulary
returns in ch5.

## Chapter 2 · More flip-flops, less logic
Slug: ch2_sliding_ring · ~9.5 min · Source: pp. 135 (Sliding State Assignment)–137 (Shift
Register Assignment) · Recording: 00:15:08–00:25:40, and 00:29:59–00:30:40 for s7
Goal: design the divide-by-5 with the sliding assignment (one gate) and the shift-register
assignment (no gates), read both tables by inspection, and explain the trade: more flip-flops for
less logic and wiring.
Scenes:
- s1_hook · Hook (~40 s): part line "Part 2 · More flip-flops, less logic".
  - Last time: counting in binary cost an exclusive-or and two ANDs. Show the circuit, small.
  - The lecturer's "funkier" assignments are often based on a shift register's action. "A bit of
    fun"; "you wouldn't necessarily do it in anger". But they show how much freedom there is.
  - The question: can a cleverer choice of codes make the logic almost vanish?
- s2_sliding · The ones slide (~100 s): p. 135, 00:15:17–00:17:02.
  - Three cells a, b, c, all 0. A 1 enters at a and moves to b, then to c, and a second 1
    follows it. At the far end they drop off, and everything is 0 again. Animate the GOLD 1s.
  - In table order (c b a): 000 → 001 → 011 → 110 → 100 → 000.
  - Why two 1s: each output must be 1 for two of the five states.
  - Read the columns:
    - a = 0, 1, 1, 0, 0;
    - b = 0, 0, 1, 1, 0;
    - c = 0, 0, 0, 1, 1.

    Each is high for two and low for three: the same waveform, shifted by one clock. The
    specification doesn't fix the phase, so any of them can be the output.
- s3_slidelogic · Logic by K-map and by eye (~100 s): pp. 135–136, 00:17:03–00:19:25.
  - The table. Unused states: 010, 101, 111. Note that 010 is unused here, though binary counting
    used it.
  - D_a: 1s at 000 and 001, a pair: D_a = b̄·c̄. The X's don't help.
  - D_b and D_c by inspection. The a column equals the b′ column, so D_b = a. The b column equals
    c′, so D_c = b. No logic, just two wires.
  - The result is a shift register a → b → c, with b̄·c̄ feeding its input.
- s4_slidecircuit · The sliding circuit (~60 s): 00:19:39–00:20:39.
  - One AND gate, of the not-b and not-c outputs, into D_a. Then Q_a is wired to D_b and Q_b to
    D_c.
  - Run it with the output from b (the lecturer's choice; any would do): high for two, low for
    three.
  - Scoreboard: sliding, 3 flip-flops, 1 gate.
- s5_ring · A ring of five (~85 s): p. 136 second slide, p. 137, 00:20:40–00:22:52.
  - "An even more egregious use of flip-flops": a shift register whose last output feeds back
    into the first input, so the data cycles round and round.
  - Two adjacent 1s circulate through five flip-flops: 00011 → 00110 → 01100 → 11000 → 10001 →
    00011 (e d c b a).
  - Five flip-flops for five states, two more than the minimum.
  - Every output reads 1 1 0 0 0 in some phase, so any of them can be the output.
- s6_nologic · No logic at all (~70 s): p. 137, 00:22:52–00:25:40.
  - Each flip-flop's next state is its neighbour's current state: D_a = e, D_b = a, D_c = b,
    D_d = c, D_e = d. That follows from the shift register's wiring, and also from the table.
  - No gates at all, only wires.
  - "Unused states. Lots!": 27 of the 32.
  - The lecturer misreads one row at 00:24:41 and corrects himself. Follow the slide.
- s7_tradeoff · Flip-flops or wires? (~65 s): p. 137 ("needs 2 more FFs, but no logic and
  simple wiring") and the lecturer at 00:29:59–00:30:40 (moved here, see Decisions).
  - On a modern chip flip-flops don't take up much room. Combinational logic needs wiring, and
    wiring takes space. So more flip-flops can make the cheaper design. These are p. 132's bullets
    from Part 1.
  - The scoreboard so far: binary 3 flip-flops and 3 gates; sliding 3 and 1; ring 5 and 0.
- s8_recap · Recap and next (~55 s): recap with small versions of:
  - the sliding 1s (s2);
  - the three columns as one waveform in three phases (s2);
  - D_b = a and D_c = b (s3);
  - the one-gate circuit (s4);
  - the ring of five (s5);
  - the scoreboard (s7).

  Next time: switch the ring on, and nothing happens. Why? End card.
Continuity: ch1's table, K-map style, waveform and scoreboard. The ring and its circuit open ch3.
The GOLD travelling 1 returns in ch4.

## Chapter 3 · Starting in a used state
Slug: ch3_startup · ~9.5 min · Source: the ring demo, refresher pp. 127–128 (Lecture 9's "FSM
Problems"), callback to L6's asynchronous inputs (p. 91) · Recording: 00:25:40–00:29:59
Goal: explain why a state machine can start in an unused state, check whether a design is
self-starting, see why the ring never is, and use the active-low asynchronous set to start it in a
used state.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 3 · Starting in a used state".
  - Last time: the ring of five, five flip-flops and no logic at all.
  - Re-enact the lecturer's simulation: the clock ticks, and the output stays flat at 0.
  - The question: the design is right, so why does it do nothing?
- s2_stuck · All zeros (~70 s): 00:25:51–00:27:12.
  - The lecturer asks the room. A student answers: "we need to initialise it into one of the
    used states".
  - The simulated flip-flops start at 00000, which isn't one of the five used states. A ring of
    zeros shifts zeros into zeros for ever.
  - Nothing in the design is wrong: the table only said what happens in the five used states.
- s3_powerup · The power-up problem (~80 s): Lecture 9's pp. 127–128, refresher. The lecturer:
  "Remember, I said…".
  - At power-up the flip-flops can come up in any pattern, including an unused one. Then the
    machine may be stuck in some unplanned sequence that never returns to a used state.
  - p. 128's three remedies:
    1. check whether it eventually reaches a used state from every unused state (if so, it is
       self-starting);
    2. if not, add logic: put the unused states into the transition table, each with a valid
       next state;
    3. or use the flip-flops' asynchronous clear and preset inputs to set a known used state at
       power-up.
  - Lecture 9's check of the traffic light (p. 128): 000 → 010, 011 → 100, 101 → 110,
    111 → 001. All are used states, so it self-starts.
- s4_check · Do our counters self-start? (~85 s): ours, by p. 128's method, checked.
  - Feed each unused state into ch1's logic: 101 → 010, 110 → 010, 111 → 100. All used.
  - Sliding (ch2): 010 → 100 and 111 → 110. But 101 → 010 → 100: an unused state can pass
    through another unused state first. "Eventually" is what counts.
  - Draw each as its five-state ring, with the unused states as DIM circles whose arrows lead in.
  - Both self-start, but by luck: the K-map groupings decided what each X became.
- s5_loops · The ring's trap (~80 s): ours, checked.
  - A ring only rotates, so a pattern never changes, it only moves round.
  - The 32 states fall into 8 loops: 00000 and 11111 on their own, and six loops of five. Only one
    loop is ours, two adjacent 1s.
  - Every other loop gives a wrong output for ever: flat 0, flat 1, or worse. For example, 00101's
    loop has two 1s that aren't neighbours, so the output is high for one clock, low for one, high
    for one, low for two. Hence the lecturer's "at least two adjacent ones".
  - Draw the trap loops RED and ours GREEN.
  - No unused state ever reaches a used one: the ring never self-starts. It has to be put into a
    used state.
- s6_preset · Asynchronous set, active low (~80 s): 00:27:12–00:28:00, callback to L6 ch3's
  asynchronous inputs.
  - The simulation's D flip-flops (74-series chips) have asynchronous set and reset inputs. They
    act at once, whatever the clock is doing.
  - The little circle on the set pin means active low. To set Q to 1, drive set to 0; then put it
    back to 1 so the chip behaves as a normal D flip-flop again.
  - First the lecturer disconnects the clock with a switch, so nothing shifts while he works.
- s7_restart · Into a used state (~65 s): 00:28:00–00:29:53.
  - Set two neighbouring flip-flops (d and e, giving 11000, a used state). Release the set inputs
    and reconnect the clock: high for two, low for three.
  - The lecturer's two lessons:
    - this is what asynchronous set and reset are for;
    - a machine must start in a used state. Otherwise this one would stay at 0 for ever.
  - One sentence, from the slides rather than the demo: in a real circuit this is done at
    start-up, not by hand. p. 91 (L6): asynchronous inputs are "often used to force a synchronous
    circuit into a known state, say at start-up"; p. 128: "at power up".
- s8_recap · Recap and next (~60 s): recap with small versions of:
  - the flat-line simulation (s1);
  - 00000 shifting into itself (s2);
  - p. 128's three remedies (s3);
  - the two self-starting rings with DIM states leading in (s4);
  - the eight loops, one GREEN and the rest RED (s5);
  - the active-low set pin (s6).

  Next time: a style that sounds just as extravagant and is used for real, one flip-flop per
  state. End card.
Continuity: ch1's and ch2's logic and tables (s4), ch2's ring and circuit. The set-pin drawing
and the "same trap" return in ch4 s6.

## Chapter 4 · One-hot
Slug: ch4_one_hot · ~9.5 min · Source: pp. 137 (One Hot State Encoding)–139 (circuit), refresher
pp. 126–127 (Lecture 9's traffic-light logic), callback to L8 ch1 · Recording: 00:30:40–00:38:44
Goal: explain one-hot encoding and its cost (m flip-flops instead of ⌈log₂ m⌉), design the
one-hot traffic light (a ring of four, outputs by OR), compare it with Lecture 9's three-flip-flop
design, and explain why it is as fast as a machine can be.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 4 · One-hot".
  - Last time: starting a machine in a used state.
  - Part 2's ring spent flip-flops "for fun". Now a style that spends them for real, and is used a
    lot.
  - Visual: a row of eight flip-flops with one lit, the light stepping along. Beside it, three
    flip-flops counting in binary through the same eight states.
  - The question: what do we gain by giving every state its own flip-flop?
- s2_onehot · One flip-flop per state (~85 s): p. 137 second slide, 00:30:40–00:31:51.
  - A shift-register design style in which only one flip-flop at a time holds a 1, the "hot" one.
  - So there's one flip-flop per state: m flip-flops instead of log₂ m rounded up. Eight states
    need eight flip-flops instead of three. The lecturer: "here we really are burning through
    the flip-flops".
  - But it can give simple, fast machines. Outputs come from OR-ing the right flip-flop outputs.
  - Part 2's ring carried two 1s; a one-hot machine always carries exactly one.
- s3_ring4 · The traffic light, one-hot (~90 s): p. 138, 00:31:51–00:34:21.
  - The lecturer returns to the traffic light from Part 1. Four states, so four flip-flops, r,
    ra, g and a, one per state.
  - The table: 1000 → 0100 → 0010 → 0001 → 1000. Unused states: "lots" (12 of 16).
  - Read by inspection: D_ra = r, D_g = ra, D_a = g, D_r = a. A ring of four, with no next-state
    logic at all.
- s4_outputs · Lighting the lamps (~70 s): pp. 138–139, 00:34:21–00:35:46.
  - The red lamp is on in red and in red-and-amber: R = r + ra.
  - The amber lamp is on in red-and-amber and in amber: A = ra + a.
  - The green lamp is on only in green: G = g.
  - p. 139's circuit: the ring of four on one CLK line and two OR gates. G is just a wire.
- s5_compare · Two ways to light the lamps (~70 s): refresher of pp. 126–127 and our comparison.
  - Lecture 9's design used Part 1's codes: three flip-flops R, A, G. Its next-state logic is
    D_R = R ⊕ A, D_A = Ā (a wire from not-A) and D_G = R·A, with no output logic (p. 127's
    circuit, small).
  - One-hot: four flip-flops, no next-state logic, two OR gates of output logic.
  - The logic has moved from inside the loop to after it. Add both rows to the scoreboard.
- s6_demo · The same trap (~65 s): 00:35:58–00:37:46.
  - The simulation runs and nothing lights. "Same deal as before": all zeros isn't a one-hot
    state, because one flip-flop must hold a 1.
  - The lecturer sets one flip-flop (a, amber) with its active-low set, releases it and
    reconnects the clock. The lights run amber, red, red-and-amber, green, amber…
  - Ours, one sentence: like the ring of five, it can't find its own way back, because any
    pattern just rotates.
- s7_fast · As fast as it gets (~80 s): 00:37:47–00:38:44, callback to L8 ch1 (the path and the
  budget bar, small).
  - The lecturer: what limits the clock is the delay of the logic between the flip-flop outputs
    and inputs. That's L8's T_c ≥ t_pc + t_pd + t_su.
  - The one-hot ring has no logic in its loop, so t_pd = 0 and T_c ≥ t_pc + t_su. With L8's
    flip-flops (0.2 ns and 0.1 ns, ours) that's 0.3 ns, about 3.3 GHz.
  - The output OR gates sit outside the loop, so they don't slow it.
  - Ours, one sentence: with no logic between flip-flops, the hold question is L8's shift-register
    case, which flip-flops are designed to meet.
  - One-hot machines can be fast, but they burn flip-flops.
- s8_recap · Recap and next (~60 s): recap with small versions of:
  - the one hot flip-flop stepping along the row (s2);
  - the ring of four and its table (s3);
  - the OR gates and lamps (s4);
  - the two designs side by side (s5);
  - the set pin (s6);
  - the budget bar with no logic segment (s7).

  Next time: a real machine with inputs, from a Cambridge exam, built both ways. End card.
Continuity: ch1 s3's codes and lamps; ch3's set pin and stuck simulation; L8's path and budget
bar. One-hot returns in ch6 on a machine with inputs.

## Chapter 5 · Hunt, Sight and Sync
Slug: ch5_synchroniser · ~11 min · Source: pp. 139 (Tripos Example)–141 (FF 0's K-map), with
p. 123 (Lecture 9's Moore example, the same machine) · Recording: 00:38:44–00:51:53 (skip
00:38:56–00:39:36, closing the simulator)
Goal: explain what the frame synchroniser does and read its state diagram. Assign Hunt 00,
Sight 01, Sync 10. Write the transition table with don't-care inputs and the unused state 11, and
derive D1 = s1·ē + s1·r + s0·e·r and D0 = s0·ē + s̄1·s̄0·r from four-variable K-maps.
Scenes:
- s1_hook · Hook (~50 s): part line "Part 5 · Hunt, Sight and Sync".
  - Last time: one-hot. Every machine so far has run on the clock alone.
  - Visual: a receiver at the end of a serial link sees a stream of bits with no gaps, and somewhere
    in it a known pattern recurs. Where does each frame start?
  - It's a Tripos question (a Cambridge exam question). The machine is Lecture 9's Moore example
    (p. 123, states A, B, C), now with names and a job.
- s2_frames · Frame synchronisation (~85 s): 00:39:36–00:42:20.
  - A serial data link (Lecture 7's, refreshed in L8 ch2 s3): a transmitter sends bits one after
    another down one wire.
  - Periodically, at a known spacing, the transmitter inserts a known sequence of, say, 8 or 16
    bits. Finding it lets the receiver lock on to the frames. That's frame synchronisation.
  - The receiver makes two signals:
    - r = 1 when it thinks it has just received the special sequence;
    - e = 1 when it is expecting the sequence now, from the known spacing.
  - Why e: the magic pattern can also turn up by chance in the data. Expecting it at the right
    time guards against a false detection.
- s3_diagram · Reading the state diagram (~100 s): p. 139, 00:42:20–00:44:09.
  - Hunt, looking for the sequence: r̄, stay; r, go to Sight, whatever e is.
  - Sight, seen once:
    - ē (not expecting it yet): stay;
    - e·r (expected and there): go to Sync;
    - e·r̄ (expected but missing, so the first sighting was a fluke): back to Hunt.
  - Sync: ē, stay; e·r, stay; e·r̄, lost sync, back to Hunt.
  - Ours, a check the viewer can do (checked): from each state, the arc labels cover every
    combination of e and r exactly once.
  - The output s should be 1 only in Sync. It depends on the state alone, so this is a Moore
    machine.
- s4_twoffs · Two flip-flops, and the output (~65 s): p. 139, 00:44:09–00:45:12.
  - Three states need at least two flip-flops (log₂ 3, rounded up).
  - Sequential assignment: Hunt 00, Sight 01, Sync 10, labels s1 s0. 11 is unused.
  - s = 1 only in Sync (10). Column s1 is 1 only there (11 never occurs), so s = s1. No output
    logic.
- s5_table · The table, with don't-care inputs (~95 s): p. 140, 00:45:12–00:48:20.
  - Columns: current state s1 s0 | inputs e r | next state s1′ s0′. Build it state by state
    from the diagram, as the lecturer does:
    - Hunt: X 0 → 00; X 1 → 01.
    - Sight: 0 X → 01; 1 0 → 00; 1 1 → 10.
    - Sync: 0 X → 10; 1 0 → 00; 1 1 → 10.
    - Unused 11: X X → X X.
  - Two kinds of X:
    - an X under the inputs means "either value, same result", so that row stands for two rows;
    - an X in the next state means "this never happens, so we don't care what the logic gives".
- s6_d1 · A four-variable K-map: D1 (~105 s): p. 140, 00:48:20–00:50:23.
  - Four variables: s1, s0, e, r. Rows s1 s0 and columns e r, both in Gray order 00, 01, 11, 10.
    So the 11 row sits between 01 and 10, and that whole row is X.
  - Plot the 1s of s1′:
    - 0111 (Sight, e r = 11);
    - 1000 and 1001 (Sync with e = 0: one table row, two cells);
    - 1011 (Sync, e r = 11).
  - Groups:
    - s1·ē, four cells with the X row;
    - s1·r, four cells;
    - s0·e·r, a pair with the X row.

    All three are essential. D1 = s1·ē + s1·r + s0·e·r.
- s7_d0 · D0, and the finished design (~85 s): p. 141, 00:50:23–00:51:53.
  - The 1s of s0′: 0001 and 0011 (Hunt, r = 1); 0100 and 0101 (Sight, e = 0).
  - Groups: s0·ē, four cells with the X row, and s̄1·s̄0·r, a pair. D0 = s0·ē + s̄1·s̄0·r.
  - The design: two flip-flops, these two sums of products, and s = s1.
  - Add the synchroniser's sequential row to the scoreboard: 2 flip-flops, 7 gates (ours,
    counted).
- s8_recap · Recap and next (~60 s): recap with small versions of:
  - the bit stream with its recurring pattern (s2);
  - the state diagram (s3);
  - the codes and s = s1 (s4);
  - the table with its two kinds of X (s5);
  - the two K-maps with their loops (s6–s7).

  Next time: the same machine one-hot, with three flip-flops and no K-maps. End card.
Continuity: ch1's recipe and log₂ bound; L8 ch2 s3's serial link. The state diagram drawn in s3
is reused in ch6 with the codes swapped. Its layout follows p. 139: Sync top left, Hunt top
right, Sight below.

## Chapter 6 · One-hot, straight from the diagram
Slug: ch6_onehot_sync · ~11 min · Source: pp. 141 (re-implement with 1 hot)–143 · Recording:
00:51:53–00:59:56 (the recording ends as the last slide is discussed)
Goal: re-implement the synchroniser one-hot and write its next-state equations straight from the
table, without K-maps. Simplify them using "exactly one flip-flop is 1" (s̄0 = s1 + s2) and
A + Ā·B = A + B. Read the same equations off the diagram's incoming arcs, and weigh one-hot
against sequential.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 6 · One-hot, straight from the diagram".
  - Last time: the synchroniser with two flip-flops and two four-variable K-maps.
  - The same state diagram, now with one flip-flop per state.
  - The question: for one extra flip-flop, how much easier does the design get?
- s2_codes · Three flip-flops, one per state (~85 s): pp. 141–142, 00:51:53–00:54:18.
  - Hunt 001, Sight 010, Sync 100, labels s2 s1 s0.
  - Careful: s1 now means the Sight flip-flop (in Part 5 it was the high bit). Label each flip-flop
    with its state's name, and keep the labels.
  - s = s2, by inspection.
  - The table: the same transitions with the new codes. The lecturer does two rows; the rest
    follow the same way. The five unused patterns aren't even listed.
- s3_inspect · Equations without K-maps (~95 s): p. 142, 00:53:53–00:55:29 and 00:56:38–00:57:58.
  - The slide's note: only one flip-flop is 1 at a time. So each row is identified by its hot
    flip-flop alone, and the others are 0 by definition.
  - D2 (Sync next): the rows with s2′ = 1 are Sight with e·r, Sync with ē, and Sync with e·r.
    So D2 = s1·e·r + s2·ē + s2·e·r.
  - D1 (Sight next): Hunt with r; Sight with ē. D1 = s0·r + s1·ē.
  - D0 (Hunt next): Hunt with r̄; Sight with e·r̄; Sync with e·r̄.
    D0 = s0·r̄ + s1·e·r̄ + s2·e·r̄.
  - At 00:57:02 the lecturer says "S2" for a moment; the term is s1·ē.
- s4_onehot_rule · Using "exactly one is hot" (~85 s): p. 142, 00:55:29–00:56:38.
  - In every used state exactly one flip-flop is 1: s2 + s1 + s0 = 1. So "s1 or s2" is the same
    as "not s0": s̄0 = s1 + s2.
  - D2: s1·e·r + s2·e·r = (s1 + s2)·e·r = s̄0·e·r. So D2 = s̄0·e·r + s2·ē.
  - Ours, one sentence: this holds only in used states. That's fine, because the others never
    occur (Part 3 was about what happens if they do).
- s5_d0 · Simplifying D0 (~85 s): p. 142.
  - D0 = s0·r̄ + (s1 + s2)·e·r̄ = s0·r̄ + s̄0·e·r̄ = r̄·(s0 + s̄0·e).
  - The step: s0 + s̄0·e = (s0 + s̄0)·(s0 + e) = s0 + e, by the distributive law
    (A + Ā·B = A + B). Show it with a four-row truth table (ours).
  - D0 = r̄·(s0 + e) = r̄·s0 + r̄·e.
  - Read it (ours): go to, or stay in, Hunt whenever the sequence is absent and we were either
    already hunting or expecting it.
- s6_arcs · Straight from the diagram (~95 s): p. 143 first slide, 00:58:12–00:59:41.
  - You don't need the table at all. Each state's flip-flop gets the OR of the arcs coming into
    that state. Each arc contributes (the flip-flop of the state it comes from) AND (its
    condition).
  - D2, arcs into Sync: from Sight with e·r, from Sync with ē, from Sync with e·r. Light each arc
    as its term appears.
  - Ours: the same for Sight (D1: from Hunt with r, from Sight with ē) and for Hunt (D0: three
    arcs). They match s3.
- s7_verdict · One-hot or sequential? (~70 s): p. 143 second slide (on screen at ~00:59:48).
  - The slide: in this example one-hot is easier to design, but it needs slightly more hardware
    than the sequential assignment.
  - Ours, counted: sequential is 2 flip-flops and 7 gates; one-hot is 3 flip-flops and 8 gates,
    with D0 factored. Neither has output logic. The extra is mostly the flip-flop. Add the row to
    the scoreboard.
  - The lecture's thread: there's no single best assignment. It depends on what you optimise
    (Part 1, p. 132).
- s8_recap · Recap, the lecture, and next (~85 s): recap with small versions of:
  - the one-hot codes with state names (s2);
  - the three equations by inspection (s3);
  - s̄0 = s1 + s2 (s4);
  - the D0 algebra (s5);
  - the arcs into Sync lit (s6);
  - the full scoreboard (s7).

  Then the lecture in one line: how you assign the states decides how much logic you need, from
  binary count through sliding and ring to one-hot.

  Next lecture: "Further Considerations" (p. 144). Sometimes a design has more states than it
  needs, and removing the redundant ones can save flip-flops and logic. End card.
Continuity: ch5's state diagram and table layout; ch3's "used states only" for s4; ch4's one-hot
idea; ch1's p. 132 for s7. The end card points to Lecture 11.

## Decisions
- **Lecture number: 10, confirmed.** The file's date (Wed 2026-10-28) gives Lecture 10 by the
  course's Mon/Wed/Fri numbering (L8 = Fri 10-23). The recording agrees:
  - it opens on p. 132's title slide, "Synchronous State Machines 2" (frame at 00:03:00);
  - it refers back to Lecture 9's slides: "as we have seen, at least log2 n flip-flops" (00:06:36),
    "you can use more, as we've seen" (L9's Example 2), "remember I said … start in one of the
    used states" (00:26:58, pp. 127–128), "return to the traffic light example" (00:31:51);
  - it refers to Lecture 7's serial data link (00:39:59);
  - Boole's birthday, 2 November, is "a few days" away (00:05:56).

  The digest's "Lecture 10" comes from the file name, not the video.
- **What L10 assumes from Lecture 9 (no recording here).** L10 starts cleanly at p. 132, so L9
  covered pp. 120–131: FSM definitions, Moore and Mealy, state diagrams, the traffic light with
  three flip-flops, power-up and self-starting, and Example 2 (four flip-flops for six states).
  Precedent: L8 re-taught L7 where it leaned on it. Here:
  - ch1 s2 re-teaches state machines (pp. 120–122): definitions, the Moore schematic, the
    recipe, and Moore vs Mealy in one sentence;
  - ch1 s3 the traffic light's codes and unused states (pp. 124–125);
  - ch3 s3 the power-up problem and its remedies (pp. 127–128);
  - ch4 s5 the traffic light's logic (pp. 126–127).

  Left out: the Mealy diagram (p. 123), Moore vs Mealy timing (p. 122), and Example 2
  (pp. 129–131), which this lecture doesn't use. L11 opens with a Mealy table (p. 145), so a
  future L11 project should refresh Mealy machines.
- **Scope: pp. 132–143, the whole section, confirmed from the frames.** p. 143's closing slide is
  on screen at ~00:59:48. The recording ends mid-sentence a few seconds later, back on p. 143's
  first slide. Nothing in pp. 132–143 is left out. pp. 144+ ("Further Considerations") are next
  lecture's: teaser only (ch6 s8).
- **Title: kept, "State Assignment".** It's p. 132's first heading, and every part of the lecture
  is a state assignment and its consequences. The section's own name, "Synchronous State
  Machines 2", says less on a title card. The folder keeps its name.
- **Size: 6 chapters, ~61 min**, like L6's approved 61.3 min and L8's ~61.
  - The lecture has ~54 min of teaching: the divide-by-5 three ways (00:06–00:30), one-hot
    (00:30–00:39) and the synchroniser two ways (00:39–01:00).
  - We add ~5 min re-teaching Lecture 9, plus two short checks of our own (ch3 s4–s5).
  - Each chapter answers one question: what assignment is and the obvious one; spending flip-flops
    to save logic; starting in a used state; one-hot; the synchroniser done the usual way; done
    one-hot.
  - **To shorten** (the user may prefer): drop ch3 s4–s5 (ours, ~2.75 min). Put the demo and its
    fix at the end of ch2 (+1.5 min), and the power-up refresher in ch4 s6 (+1 min). That gives
    5 chapters, ~56 min.
- **Order: the lecture's, with three moves:**
  - the lecturer's "flip-flops are cheap, wiring is expensive" (00:29:59–00:30:40), said after the
    ring demo, closes ch2 (s7) beside p. 137's "no logic and simple wiring", so ch3 is purely
    about starting up;
  - Lecture 9's traffic light is split: its codes motivate the topic in ch1 s3, and its logic is
    compared with one-hot in ch4 s5;
  - the self-start refresher (pp. 127–128) sits where the demo fails (ch3 s3), as the lecturer
    recalled it there.
- **Exercises:** pp. 132–143 have none, so there are no hints and no bonus chapter. The Tripos
  question is worked in full in ch5–ch6. A bonus of our own problems is possible if the user wants
  one, for example:
  - a one-hot divide-by-5;
  - a self-start check of the synchroniser. Ours, checked: sequential 11 stays in 11 while e = 0,
    claiming sync (s = s1 = 1); one-hot 000 stays dark while e = 0, then e·r jumps straight to
    Sync.
- **Student questions:** one, at 00:26:38: why the ring does nothing. The student's answer ("put
  it into one of the used states") is ch3 s2. The digest's other "Questions" are Gemini's own.
  Likely confusions, answered where they arise:
  - the lecturer's "Gray coding of these assignments" (ch1 s7);
  - why 010 is unused in the sliding assignment (ch2 s3);
  - why any output works (ch2 s2, s5);
  - the two meanings of X in the synchroniser table (ch5 s5);
  - s1 changing meaning (ch6 s2);
  - why s̄0 = s1 + s2 is allowed (ch6 s4).
- **Source disagreements (the slides and frames win):**
  - The synchroniser's diagram. Slide p. 139 and the transcript:
    - Hunt: r̄ stay, r → Sight;
    - Sight: ē stay, e·r → Sync, e·r̄ → Hunt;
    - Sync: ē and e·r stay, e·r̄ → Hunt.

    The digest's 00:38:44 segment has wrong arcs (Hunt self-loop "ē + e·r", Sight → Sync
    "e·r̄", Sync → Hunt "ē + e·r"). Its 00:40:00 segment is right.
  - The digest's 00:50:00 table (01 10 → 10, 01 11 → 00, 10 X0 → 10) and its
    D1 = s1·ē + s1·r̄ + s0·e·r̄ are wrong. p. 140: D1 = s1·ē + s1·r + s0·e·r (its own 00:48:21
    segment agrees).
  - The digest's one-hot diagram and table (00:51:53–00:54:18) have Sync staying on e, going to
    Sight on ē·r and to Hunt on ē·r̄. That's wrong: it's the same machine (p. 142). Its
    D2 = s1·e·r + s2·e·r̄ + s2·e·r and D1 = s0·r + s1·ē + s2·ē·r are also wrong. p. 142:
    D2 = s1·e·r + s2·ē + s2·e·r and D1 = s0·r + s1·ē.
  - The digest calls r "the received data bit". r = 1 means the special sequence has just been
    recognised (00:41:05).
  - The ring demo: the frame at 00:28:45 shows d and e preset, giving 11000. The one-hot demo: the
    frame at 00:37:35 shows a (amber) preset. The digest says "the first flip-flop".
  - The divide-by-5 circuits (frames at 00:14:30 and 00:19:55): D_a is a 74HC08 AND fed by the
    Q̄ outputs in both, not a NOR. We draw ANDs with not-inputs.
  - p. 133 writes "log₂ m" without ceiling brackets, the digest ⌈log₂ m⌉. We show ⌈log₂ m⌉ and
    say "rounded up", because the slide's own example (5 states → 3 flip-flops) needs it.
  - The lecturer's last words (00:59:48, "slightly more complicated than you might like, but
    nonetheless…") are cut off. ch6 s7 follows p. 143's slide: one-hot is easier to design but
    needs slightly more hardware.
- **Transcript slips, corrected silently:**
  - 00:06:36 "log 2 to the n" is log₂ m;
  - 00:11:33 "Gray coding of these assignments" is the K-map's ordering;
  - 00:24:41 "the input to the C flip-flop is the output of the D flip-flop" (he corrects it);
  - 00:46:38 "R goes to 1, sorry, E goes to 1";
  - 00:57:02 "which is sorry S2" is s1·ē;
  - Whisper's "Yenka", "yanker" and "anchor" are the simulator, and "site" is Sight.
- **Voice notes for the producer:**
  - "ee" (the letter e: input e and the ring's flip-flop e) isn't in voice.py's `SPELLED` or
    voiceqa.py's `LETTERS`. Add "ee" → "e", or QA will flag every "ee".
  - "Sight"/"site" and "Sync"/"sink" are homophones for QA.
  - "Tripos" is untested; if the voice mangles it, say "a Cambridge exam question".
- **Beyond the slides, each short and labelled "ours" in the scene list,** all checked:
  - ch1: "divide by five" as one output cycle per five clock periods (s5).
  - ch3: the self-start checks of the binary and sliding counters (s4); the ring's eight loops
    (s5).
  - ch4: the eight-flip-flop visual (s1); the L9-vs-one-hot comparison (s5); "any pattern just
    rotates" (s6); the 0.3 ns / 3.3 GHz bound and the hold remark (s7).
  - ch5: the arcs cover every input combination exactly once (s3); the gate count (s7).
  - ch6: the used-states-only caveat (s4); the D0 truth table and its reading (s5); D1 and D0
    from the arcs (s6); the gate counts (s7).
- **Checked** (Python, standard library, exhaustive):
  - ⌈log₂ m⌉: 3 → 2, 4 → 2, 5 → 3, 6 → 3, 8 → 3, 9 → 4.
  - Binary divide-by-5: D_a = ā·c̄, D_b = a ⊕ b, D_c = a·b reproduce 000 → 001 → 010 → 011 →
    100 → 000. b = 0, 0, 1, 1, 0. Unused: 101 → 010, 110 → 010, 111 → 100 (self-starting).
  - Sliding: D_a = b̄·c̄, D_b = a, D_c = b reproduce 000 → 001 → 011 → 110 → 100 → 000.
    a = 0, 1, 1, 0, 0; b = 0, 0, 1, 1, 0; c = 0, 0, 0, 1, 1. D_a's map: row c = 0 is 1 1 0 X,
    row c = 1 is 0 X X 0. Unused: 010 → 100, 101 → 010 → 100, 111 → 110 (self-starting).
  - Ring: D_a = e, D_b = a, D_c = b, D_d = c, D_e = d reproduce 00011 → 00110 → 01100 → 11000 →
    10001 → 00011. 27 unused states. 8 loops: 00000, 11111 and six of five (starting 00001,
    00011 [used], 00101, 00111, 01011, 01111). No unused state reaches a used one. Output b on
    the 00101 loop: 0, 1, 0, 0, 1.
  - L9 traffic light: D_R = R ⊕ A, D_A = Ā, D_G = R·A reproduce 100 → 110 → 001 → 010 → 100.
    Unused: 000 → 010, 011 → 100, 101 → 110, 111 → 001 (p. 128).
  - One-hot traffic light: D_ra = r, D_g = ra, D_a = g, D_r = a. Lamps R = r + ra, A = ra + a,
    G = g give R, R+A, G, A. 16 states in 6 loops: 0000, 1111, the one-hot loop, 0011's (4),
    0101/1010 (2) and 0111's (4). Not self-starting.
  - Synchroniser, sequential: D1 = s1·ē + s1·r + s0·e·r and D0 = s0·ē + s̄1·s̄0·r match all 12
    used (state, e, r) rows. Both are minimal; D0 has one more prime implicant, s̄1·ē·r, which
    isn't needed. s = s1. From 11: e r = 00 or 01 → 11, 10 → 00, 11 → 10.
  - Synchroniser, one-hot: D2 = s1·e·r + s2·ē + s2·e·r = s̄0·e·r + s2·ē; D1 = s0·r + s1·ē;
    D0 = s0·r̄ + s1·e·r̄ + s2·e·r̄ = r̄·(s0 + e). All match the 12 used rows. The raw and
    simplified forms differ only in unused states (000, 011, 101, 111).
    s0·r̄ + s̄0·e·r̄ = r̄·(s0 + e) for all 8 inputs. From 000: ē → 000, e·r̄ → 001, e·r → 100.
  - Gate counts (not counting inverters; flip-flop Q̄ outputs are free; e and r need inverters):
    - binary divide-by-5: 3 (2 AND, 1 exclusive-or);
    - sliding: 1 AND;
    - ring: 0;
    - L9 traffic light: 2 (exclusive-or, AND);
    - one-hot traffic light: 2 OR;
    - synchroniser sequential: 7 (5 AND, 2 OR) + 1 inverter (ē);
    - synchroniser one-hot: 8 (5 AND, 3 OR, with D0 = r̄·(s0 + e)) + 2 inverters (ē, r̄).
  - ch4 s7: 0.2 + 0.1 = 0.3 ns, 1/0.3 ns = 3.33 GHz.
- **Skipped from the recording:**
  - 00:00–00:05:56: room chat, lab groups, Boole's birthday;
  - 00:38:56–00:39:36: closing the simulator's leftover tooltip.
