# Flip-flops and Counters: plan

Request: "produce the Digital Electronics lecture from its recording and the course notes"
(2026-10-28, relayed). This is Cambridge CST Part IA Digital Electronics (Prof. I. J. Wassell),
Lecture 6. The number is inferred: the lecturer never says it. Slides pp. 85–101.
Audience: a Cambridge first-year studying the course. Earlier lectures gave them gates (AND, OR,
NOT, NOR, XOR p. 15), Boolean algebra and De Morgan, minterms and sum of products, and K-maps
(pp. 26–36: Gray-code order, wrap-around groups, don't cares entered as X, prime and essential
prime implicants). They also have gate propagation delay (p. 58) and timing diagrams (p. 60).
Last lecture began sequential logic (pp. 78–84): memory, state, bistables, the NOR RS latch, its
state transition table and its state diagram. Everything clocked is new.
Sources: the slides (`../source/combined_26.pdf`), pp. 85–101, plus pp. 78–84 for the
refresher. The 60-min recording (`../source/l06-lecture.{transcript,digest,captions}.md`): the
teaching runs 00:04:59–00:59:57, and the first 5 min (mic checks, admin) are skipped. Where the
digest disagrees with the slides, the slides win (see Decisions).
Total: 6 chapters, ~60 min of narration (~9,600 words).

Every count, table, K-map group and equation below was checked by exhaustive enumeration in
Python. Script-writers still check their own.

Lecture-wide conventions (set in ch1, kept to the end):
- **Notation, as on the slides:** Q′ (prime) is the next state, Q the current state, and an
  overbar is the complement (Q̄, CLK̄, D̄). Never use a prime for NOT. Narration says "Q prime"
  or "the next Q", and "not Q", "not clock" (the lecturer's words).
- **Names:** "flip-flop" in narration ("FF" only in slide-style table headers),
  "transparent D latch", "master-slave D flip-flop", "J-K flip-flop", "T flip-flop",
  "excitation", "modified state transition table", "don't care" (x in the J-K excitation table
  as on p. 98; X in K-maps and in the D-latch table as on p. 86). Signals: CLK, EN, D, Q, Q_int.
- **Bits:** Q2 Q1 Q0, with Q2 the most significant, written left to right as on the slides.
  Counts are shown in binary with the decimal value beside them (011 = 3).
- **Colours:** one per role, all lecture. CLK and its edge arrows YELLOW. Inputs (D, D0–D2, J,
  K, T, EN) BLUE. Outputs Q, Q0–Q2 GREEN. Q_int TEAL. Asynchronous preset/clear and anything
  going wrong (illegal state, ripple glitches) RED. A wire at logic 1 is drawn bright and at 0
  dim. (The lecturer's simulator draws 1s in red; we keep RED for trouble.)
- **Symbols, as on the slides:** distinctive-shape gates, with a bubble meaning NOT. Latch and
  flip-flop boxes have D, Q and Q̄. A small square on EN marks a level-triggered latch; a
  triangle on the clock input marks an edge-triggered flip-flop; a bubble before the triangle
  means it triggers on the falling edge.
- **Timing diagrams, one style (ch1–ch4):** signals stacked with the clock on top, thin
  vertical guides at the active edges, and small arrows on those edges (up for rising, down for
  falling, as on the slides). An unknown value is drawn at both levels at once (slide p. 88).
  Delays are omitted, except in ch4, where they are the point.
- **Running example:** the 3-bit counter Q2 Q1 Q0 counting 0 to 7 and back to 0. It's built as a
  ripple counter in ch4 and synchronously in ch5–ch6. Its 7 → 0 step is the comparison: ripple
  passes through 6 and 4, the synchronous one changes all three bits on one edge.
- **Threads:**
  - The toggle: ch2's latch with not Q fed back to D, which oscillates; ch3's J = K = 1 and
    T = 1, with Q′ = T ⊕ Q; ch4's ripple counter and dividers; ch6's D0 = Q̄0, and every bit
    flipping when all lower bits are 1.
  - Asynchronous clear: ch3, then ch4's count-to-nine counter.
  - The state transition table: ch1's RS latch, then ch5's modified table.
- **Demos:** the lecturer's three Yenka simulations (D latch, master-slave D flip-flop,
  synchronous counter) become animated switches and LEDs on the slide circuits, inside the
  chapters that teach those circuits.

## Chapter 1 · Clocks and the transparent D latch
Slug: ch1_d_latch · ~9 min · Source: pp. 84–86, refresher pp. 79–82 · Recording:
00:05:40–00:10:52, demo 00:21:36–00:23:16
Goal: explain what a clock is for, and build the transparent D latch from the RS latch: why
EN = 0 holds, why the illegal state can't happen, and why it's called transparent and
level-triggered.
Scenes:
- s1_hook · Hook (~50 s): title card ("Flip-flops and Counters", the course line, part line
  "Part 1 · Clocks and the transparent D latch"). A grid of one-bit memories, each flipping the
  instant its own inputs change, at scattered moments. Then a clock's square wave sweeps in and
  they all flip together on its beat. The question: how do we make a memory change only when
  the clock says so? The road for the lecture, in one line: latch → flip-flop → counter.
- s2_rslatch · Last time: the RS latch (~90 s): a refresher of pp. 79–81 for viewers who missed
  Lecture 5.
  - Two cross-coupled NORs, with R going into the gate that makes Q. The NOR's two "conditions":
    a 1 on either input forces the output to 0 ("always 0"); a 0 on one input makes it invert
    the other ("complement").
  - Walk the four input pairs on the circuit, with the wires lighting up: S R = 00 hold, 01
    reset (Q = 0), 10 set (Q = 1), 11 illegal. In the illegal case both NORs are forced to 0, so
    Q = Q̄ = 0, which is a logical contradiction.
  - The table with Q′ ("next state") and Q ("current state").
  - Close on p. 84: the output changes directly in response to the inputs. That's
    asynchronous operation.
- s3_clock · The clock (~80 s): pp. 84–85.
  - Synchronous operation: outputs may change only at times set by one global enabling signal,
    the system clock.
  - It's typically a square wave at a fixed frequency. Name the vocabulary the whole lecture
    uses: high and low levels, the period, frequency = 1/period, and rising (positive-going)
    and falling (negative-going) edges.
  - What it's for (p. 85): it imposes order on the state changes, and lets lots of states
    appear to update simultaneously.
  - The slide's question, carried into s4–s5: how can we make the asynchronous RS latch act in
    step with a clock?
- s4_andgate · An AND gate as a valve (~60 s): the AND truth table (p. 86). Hold input a at 0
  and the output is stuck at 0, whatever b does (block). Hold it at 1 and the output copies b
  (pass). Animate b wiggling, first with a = 0, then with a = 1. The lecturer: "we've done this
  a few times", passing or blocking a signal.
- s5_dlatch · From RS latch to D latch (~100 s): p. 86.
  - Put an AND gate in front of R and another in front of S, both controlled by a new input EN
    ("enable"; it could be the clock). EN = 0 makes R = S = 0, which is hold, whatever comes in.
    EN = 1 lets R and S straight through.
  - Then remove the danger. Use one data input D, fed straight to S's gate and through an
    inverter to R's gate. With EN = 1, S = D and R = D̄: always complements, never both 1. The
    illegal state is impossible by construction.
- s6_transparent · Transparent while enabled (~100 s): p. 86.
  - The table D, EN → Q′, Q̄′: X 0 → hold; 0 1 → reset (0 1); 1 1 → set (1 0). Read it as: while
    EN = 1, Q follows D; while EN = 0, Q keeps its previous state.
  - Why "transparent": with EN = 1, whatever is on the input shows straight through to the
    output.
  - The symbol: a box with D, Q and EN, and the small square on EN that marks a level-triggered
    device.
  - Then re-enact the lecturer's Yenka demo, with switches on D and EN and LEDs on Q and Q̄.
    Change D with EN = 0: nothing happens. Raise EN: Q jumps to D. Wiggle D with EN high: Q
    follows every change. Drop EN: Q freezes.
  - Under it, a short EN/D/Q waveform with Q tracking D across the whole EN-high stretch. Name
    this behaviour: level-triggered.
- s7_recap · The catch, recap and next (~65 s): the catch, in the lecturer's words: the whole
  time EN is 1, the circuit is still responding to its inputs, but we want the output to
  respond at one instant. Recap, each idea as a small version of its scene's visual with one
  line under it:
  - the NOR latch with its table (s2);
  - the clock with labelled edges (s3);
  - AND as a valve (s4);
  - the D latch with "R and S never both 1" (s5);
  - the EN/D/Q waveform (s6).

  Next time: two latches back to back make a flip-flop that changes only on the clock's rising
  edge. End card.
Continuity: this chapter sets the lecture's notation, colours, gate and symbol styles. The NOR
latch drawing sits inside the D latch (s5), and the D latch becomes ch2's box. s2's table
returns, in its 8-row state-transition form (p. 82), in ch5 s3. s6's waveform returns in ch2 s1
as "the window".

## Chapter 2 · The master-slave D flip-flop
Slug: ch2_master_slave · ~10 min · Source: pp. 87–88 · Recording: 00:10:52–00:21:36, demo
00:23:16–00:25:01
Goal: explain why edge-triggering beats level-triggering and how two latches in master-slave
form make a flip-flop that changes only on the rising edge. Trace its timing diagram, and tell
latch and flip-flop symbols apart.
Scenes:
- s1_hook · Hook (~50 s): title card (part line "Part 2 · The master-slave D flip-flop"). Last
  time: the transparent D latch follows D for as long as EN is 1. Draw the clock twice: once
  with its whole high level shaded (the latch's window), once with only its rising edges marked
  (an instant). The question: can we build a memory that listens only at the edge?
- s2_window · Why a window is a problem (~85 s):
  - Slide p. 87: sequential circuits are simpler to design if outputs change only on rising or
    falling edges. The lecturer's reason: while transparent, the circuit keeps responding to its
    inputs, and we want changes at one well-specified instant, not across long periods.
  - Then a concrete case (ours, a standard textbook argument): a D latch with its own Q̄ wired
    back to D, meant to flip once per clock. While EN is high, each flip feeds back and causes
    another, as fast as the gates allow. Where it stops depends on how long EN stays high.
  - Show Q oscillating inside the shaded window, beside what we wanted: one clean flip per
    rising edge.
  - Plant it: "keep this circuit in mind; in chapter 6 it's the heart of a counter."
- s3_masterslave · Two latches, back to back (~95 s): p. 87.
  - The master D latch feeds Q_int to the slave D latch, which gives Q.
  - CLK goes through one inverter to the master's enable, so the master sees not-clock. A
    second inverter feeds the slave: a double complement, so the slave sees CLK. The slide's
    note: both latches are effectively connected to the clock, one complemented.
  - So they're never transparent together. CLK low: master open, slave shut. CLK high: master
    shut, slave open. The image is an airlock, two doors that are never both open (ours, not
    the lecturer's).
- s4_master · Timing diagram, part 1: the master (~105 s): build slide p. 88's diagram line by
  line.
  - The lecturer's habit: draw the clocks first, since they drive everything. CLK and not-clock,
    with arrows and guide lines on the rising edges.
  - D starts at 0. It rises to 1 while CLK is high (after the first rising edge) and falls back
    to 0 while CLK is high (after the third).
  - Q_int is unknown at first, drawn at both levels. It's transparent while not-clock is 1, so it
    copies D, and holds while not-clock is 0.
  - Point out that D rose while the master was holding, so Q_int caught up only when CLK fell.
    Propagation delays are neglected (the slide's note).
- s5_slave · Timing diagram, part 2: the slave (~105 s):
  - The slave's input is Q_int and its enable is CLK: transparent while CLK is high, holding
    while it's low.
  - Q is unknown until the first rising edge, then 0. At edge 2 it becomes 1, at edge 3 it stays
    1, and at edge 4 it becomes 0.
  - Read the result off the guide lines: at each rising edge Q takes the value D had just before
    it, and holds it for a whole cycle. D's wiggles between edges never reach Q.
  - The slide's words: "Q changes on rising edge of CLK".
- s6_symbols · Flip-flops vs latches, and their symbols (~100 s):
  - The lecturer's terms: a latch is level-triggered, a flip-flop edge-triggered. For building
    state machines it's flip-flops "99 times out of 100".
  - The symbols side by side: the latch has a small square on EN; the flip-flop has a triangle on
    its clock input (edge-triggered, rising). A bubble before the triangle means the falling
    edge ("circles mean complement"); ch4's ripple counter uses those. D stands for "data".
  - Re-enact the lecturer's Yenka demo on the master-slave circuit:
    - set D = 1 while CLK is high;
    - CLK falls: nothing happens at Q;
    - CLK rises: Q becomes 1, and more clocks keep it at 1;
    - set D = 0 while CLK is low; at the next rising edge, Q goes to 0.
  - Close on p. 88: master-slave has been superseded by truly edge-triggered circuits, which are
    easier to implement and perform better. Use edge-triggered flip-flops; their internals aren't
    on this course.
- s7_recap · Recap and next (~70 s): recap with small versions of:
  - the window vs the instant (s1);
  - the oscillating latch (s2);
  - the master-slave pair with CLK and not-clock (s3);
  - the timing diagram with Q changing at rising edges (s4–s5);
  - the two symbols (s6).

  Next: other flip-flops, J-K and T, and inputs that ignore the clock. End card.
Continuity: the D latch box and the CLK colour come from ch1. The timing-diagram style set here
carries into ch3 and ch4. ch6 s2 calls back the oscillating latch, and ch3 and ch4 use the
triangle and bubble symbols.

## Chapter 3 · J-K, T, and asynchronous inputs
Slug: ch3_jk_t_async · ~9 min · Source: pp. 89–91 · Recording: 00:25:01–00:30:36
Goal: give the J-K and T flip-flops' tables, explain toggling, say why D-types replaced them, and
explain asynchronous preset and clear and what they're for.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 3 · J-K, T, and asynchronous inputs". Last time: the
  edge-triggered D flip-flop. Old textbooks are full of other flip-flops: what do they do? And
  after all that work to make everything wait for the clock, why do real flip-flops come with
  inputs that ignore it?
- s2_family · Why the D type won (~60 s): p. 89.
  - J-K and T flip-flops were historically important. J-K is a lot more complex to build than D,
    so it has fallen out of favour in modern designs (FPGAs, VLSI chips).
  - The course designs synchronous circuits with D flip-flops only and shows J-K and T "for
    completeness".
  - Say why they still matter here: T flip-flops build ch4's ripple counter, and the J-K is
    where an excitation table earns its keep (ch5).
- s3_jk · The J-K flip-flop (~110 s): p. 90.
  - It's like a clocked RS flip-flop with the illegal state replaced by a new "toggle" state.
  - Its symbol (J, K, clock triangle, Q, Q̄) is edge-triggered: nothing happens until a rising
    edge.
  - Build the table row by row: 00 hold (Q′ = Q), 01 reset (Q′ = 0), 10 set (Q′ = 1), 11 toggle
    (Q′ = Q̄, Q̄′ = Q). J plays S's role and K plays R's.
  - Put the RS table beside it: the only row that changed is the forbidden 11, which the lecturer
    calls "this horrible condition" where Q and Q̄ are equal.
- s4_toggle · Toggling in time (~75 s): with J = K = 1, each rising edge flips Q: 1, 0, 1, 0
  (the lecturer counts them out). In the timing diagram, Q is a square wave with twice the
  clock's period, so half its frequency. Leave "half the frequency" on screen: it becomes ch4's
  divider.
- s5_t · The T flip-flop (~90 s): p. 90.
  - Tie J and K together and call the input T. Only two rows survive: T = 0 hold, T = 1 toggle.
    Show the symbol.
  - A compact form, read straight off the table: Q′ = T ⊕ Q. XOR with 0 keeps a bit, XOR with 1
    flips it.
  - One more view, for ch6: a D flip-flop whose D is its own Q̄ is a T flip-flop with T stuck at
    1. That's ch2's runaway circuit, made safe because the flip-flop only acts on the edge. The
    lecturer says the same of the counter's first stage (00:54:34).
- s6_async · Asynchronous inputs (~100 s): p. 91.
  - The lecturer's own objection: we've spent all this effort making flip-flops synchronous, so
    why add inputs that change them without the clock?
  - The answer came from a student's question after the previous lecture: what happens at
    start-up? At power-on each flip-flop may come up 0 or 1, and a state machine can start in a
    state nobody planned.
  - Reset/Clear forces Q to 0 and Preset/Set forces Q to 1, at once, whatever the clock is
    doing. Show a flip-flop symbol with PRE on top and CLR underneath, and a timing sketch where a
    CLR pulse between two clock edges drops Q immediately, with no edge needed.
  - Their use: forcing a synchronous circuit into a known state at start-up. ch4 also uses CLR to
    stop a counter at 9.
- s7_recap · Recap and next (~70 s): recap with small versions of:
  - the D-type beside the J-K (s2);
  - the J-K table with the toggle row lit (s3);
  - the toggling waveform (s4);
  - the T table with Q′ = T ⊕ Q (s5);
  - the CLR pulse (s6).

  Next: what flip-flops are for, starting with counters. First the simplest one to build, and
  the worst to use. End card.
Continuity: the symbol and timing-diagram styles are ch2's. The toggle waveform returns as ch4's
Q0 and dividers. Q′ = T ⊕ Q and "D = Q̄ is a T flip-flop" are called back in ch6 s2 and s7. CLR
is used in ch4 s7, and ch5 s5 puts the J-K truth table beside its excitation table.

## Chapter 4 · Counters, and the ripple counter
Slug: ch4_ripple · ~11 min · Source: pp. 92–95 (to the BCD slide) · Recording:
00:30:36–00:42:53
Goal: define counters and their uses, explain how a ripple counter of T flip-flops counts, read
its timing diagram, and explain its two problems, its use as a divider, and a count-to-nine
counter made with reset.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 4 · Counters, and the ripple counter". Last time: J-K,
  T and asynchronous inputs. Inside a digital watch, a crystal vibrates tens of thousands of
  times a second, yet the display ticks once a second: something counts. The question: how do
  you build a counter from flip-flops, and what can go wrong?
- s2_counters · What a counter is (~85 s):
  - p. 92: a counter is a clocked sequential finite state machine that goes through a
    predetermined sequence of states. An n-bit binary counter has n flip-flops and 2ⁿ states,
    passed through in the order 0, 1, …, 2ⁿ − 1, 0, …
  - For n = 3: the eight states 000 to 111 drawn as a ring, labelled Q2 Q1 Q0 with Q2 the most
    significant bit.
  - Uses (p. 92): counting, producing delays of a set length, sequencers for control logic in a
    processor, and divide-by-m counters (dividers), as in a watch.
  - An aside from p. 93: flip-flops also make memories, both memory arrays and shift registers
    that convert between parallel and serial data. The next lecture builds one.
  - Most books show two kinds of counter (p. 93): ripple and synchronous. Ripple counters break
    the synchronous rules, which is exactly why we look at one: to see the problems.
- s3_ripple · The ripple counter circuit (~90 s): p. 94.
  - Three negative-edge-triggered T flip-flops, every T tied to 1 (toggle mode). The clock drives
    only the first; Q0 drives the second's clock input, and Q1 the third's.
  - Read the symbol: bubble plus triangle means it toggles on falling edges.
  - So it isn't synchronous: the flip-flops aren't clocked by the same clock.
  - Why it counts up (ours, short): write 0 to 7 in binary in a column. A bit flips exactly when
    the bit to its right falls from 1 to 0, a carry, and that's precisely a falling edge on its
    clock input.
- s4_timing · The timing diagram (~110 s): p. 94.
  - Start with every flip-flop reset to 0, using ch3's clear inputs. Draw CLK with down-arrows on
    its falling edges.
  - Q0 toggles at each falling CLK edge, but slightly after it. The lecturer stresses that the
    shift is deliberate: it's the flip-flop's propagation delay.
  - Q1 toggles on each falling edge of Q0, and Q2 on each falling edge of Q1, each a little
    later.
  - Read the counts along the bottom, 0, 1, …, 7, 0, with Q2 Q1 Q0 in binary under each.
- s5_problems · Where ripple goes wrong (~95 s): zoom in on 7 → 0.
  - Just after the edge it still reads 111 (7). Q0 falls: 110 (6). Q1 falls: 100 (4). Q2 falls:
    000 (0), at last. The false counts are RED.
  - The slide's problems: the outputs don't change at the same time, so it's hard to know when
    the count is valid. The delay also builds up stage by stage: three stages, three delays here,
    and n delays for n stages.
  - If the next clock edge comes before the ripple has finished, the outputs never show the
    right count. That caps the clock speed before miscounting starts.
  - The lecturer's balance: it's very simple (just string flip-flops together), but it isn't
    synchronous.
- s6_divider · Counters as dividers (~75 s): p. 95.
  - Each output has half the frequency (twice the period) of the one before: Q0 is f/2, Q1 f/4,
    Q2 f/8. That's why counters are called dividers.
  - The watch: the lecturer's "about 32 kilohertz … some funny number" is 32,768 Hz = 2¹⁵, so a
    chain of 15 toggling flip-flops brings it down to one tick per second.
- s7_bcd · Counting to nine (~90 s): p. 95.
  - Often we want a count that isn't a power of 2, such as binary-coded decimal, 0 to 9. Use four
    flip-flops with Reset/Clear inputs, and an AND gate that detects the count of 10 and resets
    them all.
  - Which inputs: 1010 is the first count with Q3 = Q1 = 1, so a two-input AND of Q3 and Q1 is
    enough (the standard decade counter; the slide says only "an AND gate to detect the count of
    10").
  - Why 10 and not 9: 9 must last a full clock period, while 10 exists only for the instant
    before the asynchronous reset acts. Animate 8, 9, a flash of 10 in RED, then 0.
  - The lecturer's verdict: arbitrary counts are easy this way, and a ripple counter may do for
    unsophisticated jobs, but in general stick to synchronous designs.
- s8_recap · Recap and next (~60 s): recap with small versions of:
  - the 000–111 ring (s2);
  - the ripple circuit (s3);
  - the staircase timing diagram (s4);
  - the 7 → 6 → 4 → 0 zoom (s5);
  - f/2, f/4, f/8 (s6);
  - the AND-reset count-to-nine counter (s7).

  Next: the synchronous counter, with one clock for every flip-flop and the logic that makes it
  count. End card.
Continuity: this chapter introduces the running counter Q2 Q1 Q0 (0–7), with its binary column
and state ring; ch5 and ch6 reuse both. ch6 s6 replays the 7 → 0 zoom for contrast. The
timing-diagram style is ch2–ch3's, now with delays drawn, and the chapter uses ch3's T
flip-flop and CLR.

## Chapter 5 · Designing a synchronous counter: the tables
Slug: ch5_tables · ~10 min · Source: pp. 95–99 · Recording: 00:42:53–00:53:21
Goal: explain what makes a counter synchronous, derive the D and J-K excitation tables, and fill
in the modified state transition table for the 0-to-7 counter.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 5 · Designing a synchronous counter". Last time: the
  ripple counter and its 7 → 6 → 4 → 0 stagger. The fix: wire one clock to every flip-flop, so
  they all change together. But then no flip-flop can wait for its neighbour to fall, so
  something must tell each one what to become. The question: how do we work out each
  flip-flop's input?
- s2_sync · Synchronous design (~85 s): pp. 95–96.
  - All flip-flop clock inputs connect directly to the clock, so all outputs change at the same
    time. The price is more complex combinational logic to generate each flip-flop's inputs, and
    that logic depends on the flip-flop type.
  - The structure: three D flip-flops on one CLK line. Their outputs (the current state) feed a
    block of combinational logic, whose outputs feed the D inputs (the next state), loaded at the
    next edge.
  - The course uses D-types only; the technique extends to other types. The example is a 0-to-7
    up-counter, the same count as ch4.
- s3_statetable · The state transition table, again (~60 s): p. 96.
  - Call back last lecture's table for the RS latch (p. 82): columns Q, S, R → Q′, eight rows.
    Current state and inputs give the next state.
  - The counter's version lists current state → next state. The modified table adds columns for
    the flip-flop inputs needed to get there, and those inputs are called the excitation.
- s4_dexcite · The D excitation table (~65 s): p. 97.
  - An excitation table answers the reverse question: given the current state Q and the next
    state Q′ we want, what input must we apply?
  - For a D flip-flop: 0→0 needs D = 0, 0→1 needs D = 1, 1→0 needs D = 0, 1→1 needs D = 1. So
    D = Q′: the D column copies the Q′ column and doesn't depend on Q at all.
  - The lecturer calls it "not stupendously valuable" for D-types; it's different for other
    types.
- s5_jkexcite · The J-K excitation table (~115 s): p. 98.
  - Derive it from ch3's J-K truth table, shown side by side. For each transition, find every row
    that produces it:
    - 0→0: hold (00) or reset (01), so J = 0 and K = x (don't care);
    - 0→1: set (10) or toggle (11), so J = 1, K = x;
    - 1→0: reset (01) or toggle (11), so J = x, K = 1;
    - 1→1: hold (00) or set (10), so J = x, K = 0.
  - Every row has one don't care, a freedom that K-maps turn into simpler logic. The slide writes
    don't cares as a lowercase x.
- s6_modtable · The counter's modified table (~105 s): p. 99. The 0-to-7 counter needs 3 D
  flip-flops. Fill in the table one column group at a time, as the lecturer does:
  1. write the count sequence, 000 to 111, in the current-state columns Q2 Q1 Q0;
  2. write each required next state in Q2′ Q1′ Q0′: add one, and 111 wraps to 000;
  3. fill in the flip-flop inputs D2 D1 D0 that give that next state.

  Since D = Q′, the input columns are identical to the next-state columns: for D-types you
  needn't write them at all (p. 99).
- s7_jkcolumns · If we'd used J-K flip-flops (~75 s): p. 99.
  - With J-K flip-flops, each one needs a J and a K column: J2 K2 J1 K1 J0 K0.
  - The lecturer's two cells: Q0 going 0 → 1 needs J0 = 1, K0 = x, and Q0 going 1 → 0 needs
    J0 = x, K0 = 1.
  - Fill in the rest of the J0 and K0 columns the same way (ours, to show the method running).
    Every row is one of those two, so J0 = K0 = 1 works everywhere: the first stage just
    toggles.
  - With D-types there's no such lookup step.
- s8_recap · Recap and next (~60 s): recap with small versions of:
  - the one-clock structure with its logic block (s2);
  - the RS state table growing into the modified table (s3);
  - D = Q′ (s4);
  - the J-K excitation table with its x's (s5);
  - the 0–7 table with its D columns equal to the next state (s6);
  - the J0 K0 columns (s7).

  Next: turning the D columns into gates, by inspection and with a K-map, then running the
  finished counter. End card.
Continuity: the 0–7 count and its binary column come from ch4, the J-K truth table from ch3 s3,
and the RS state table from ch1 s2. The modified table laid out in s6 (slide p. 99's layout) is
the one ch6 works from: reuse it directly.

## Chapter 6 · From table to circuit
Slug: ch6_circuit · ~11 min · Source: pp. 99–101 (to the "arbitrary count sequence" slide) ·
Recording: 00:53:21–00:59:57 (the recording ends during the demo)
Goal: derive D0, D1 and D2 for the 0-to-7 counter (by inspection, as an XOR, and from a K-map
with essential prime implicants). Then draw the circuit, see why it counts, and state the
procedure for any count sequence.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 6 · From table to circuit". Last time: the modified
  state transition table, where for D flip-flops the D columns equal the next state. Each of D0,
  D1 and D2 is a function of the current state Q2 Q1 Q0, and we need its logic. p. 99 lists
  three tools, inspection, Boolean algebra and K-maps, and we'll use all three.
- s2_d0 · D0 by inspection (~80 s): p. 100.
  - Down the table D0 is 1, 0, 1, 0, … while Q0 is 0, 1, 0, 1, so D0 = Q̄0.
  - Flip-flop 0 toggles every clock (the slide: "FF0 is toggling"). A D flip-flop with Q̄ fed
    back to D is a T flip-flop with T = 1 (ch3 s5).
  - It's also ch2's troublesome latch circuit, which works here because the flip-flop only
    listens at the edge.
- s3_d1 · D1 is an XOR (~75 s): D1 reads 0, 1, 1, 0, 0, 1, 1, 0. Compare it with Q1 and Q0 row by
  row: D1 is 1 exactly when they differ, so D1 = Q0 ⊕ Q1. In words, Q1 flips exactly when Q0 is
  1.
- s4_kmap · A K-map for D2 (~85 s): D2 isn't obvious, so use a K-map.
  - Refresh the earlier lecture's rules as needed: Gray-code column order 00, 01, 11, 10;
    adjacent cells differ in one variable; the edges wrap around.
  - Rows are Q2 = 0 and 1; columns are Q1 Q0.
  - D2 = 1 on the minterms 011, 100, 101 and 110. Plot them one by one, as the lecturer did.
- s5_groups · Grouping, and the expression (~100 s): group in the largest powers of 2.
  - 011 can't join anything, so it stays alone: Q̄2 Q1 Q0 (the slide writes Q0·Q1·Q̄2).
  - 100 and 110, in the corners, are adjacent by wrap-around: Q2 Q̄0.
  - 100 and 101 give Q2 Q̄1.
  - The lecturer's question to the room: are these prime implicants essential? Pause. Yes, all
    three: each covers a minterm that no other covers.
  - So D2 = Q̄0·Q2 + Q̄1·Q2 + Q0·Q1·Q̄2 = Q2·(Q̄0 + Q̄1) + Q0·Q1·Q̄2 (p. 100's two lines).
  - The common slip: missing the wrap-around pair.
- s6_circuit · The circuit, and watching it count (~90 s): p. 100.
  - Three D flip-flops with one CLK line into every clock input. D0 comes from Q̄0; an XOR of Q0
    and Q1 drives D1; a combinational-logic block fed by Q0, Q̄0, Q1, Q̄1, Q2 and Q̄2 drives D2.
  - Open the block the way the lecturer's simulation built it: an OR for (Q̄0 + Q̄1), an AND with
    Q2, a three-input AND for Q0·Q1·Q̄2, and an OR joining them.
  - It's synchronous because all the clock inputs are connected together.
  - Re-enact the Yenka run: a 1 Hz clock and an LED on each output (LSB on the left, as in the
    simulation), counting 0 to 7 and round again.
  - Replay the 7 → 0 step beside ch4's stagger: here all three bits change on the same edge.
  - One lab note from the demo: in the hardware labs, every LED gets a resistor in series to stop
    it burning out.
- s7_pattern · Why it counts: the carry pattern (~70 s): ours, beyond the slides, and checked.
  - De Morgan turns Q̄0 + Q̄1 into the complement of Q0·Q1, so D2 = Q2 ⊕ (Q1·Q0).
  - Line up the three: D0 = Q0 ⊕ 1, D1 = Q1 ⊕ Q0, D2 = Q2 ⊕ Q1·Q0. That's Q′ = Q ⊕ T, as in
    ch3: each bit toggles exactly when all the bits below it are 1.
  - That's the carry of binary counting, the same rule ch4's ripple counter obeyed. Here the logic
    works it out before the edge, and every flip-flop applies it on the same edge.
  - A fourth bit would be D3 = Q3 ⊕ Q2·Q1·Q0.
- s8_anysequence · Any count sequence, and recap (~100 s): p. 101.
  - The same procedure designs a counter with any count sequence:
    1. write down the state transition table;
    2. determine the flip-flop excitation (easy for D-types);
    3. determine the combinational logic that makes that excitation from the current state.
  - Remember unused counts: states the counter never enters are don't cares in the K-maps.
    Illustration (ours): a 0-to-5 counter never enters 110 or 111, so those two cells are X in
    every map.
  - Recap with small versions of: the D0 = Q̄0 column (s2), the XOR match (s3), the K-map with
    its three groups (s5), the circuit on one CLK line (s6), the XOR ladder (s7), and the
    three-step procedure (s8).
  - The lecture in one line: latch → flip-flop → counter. Next time: shift registers, and the
    timing rules that keep synchronous circuits honest (set-up and hold times, clock skew,
    metastability). End card.
Continuity: ch6 works from ch5 s6's table, in the same layout. It calls back ch2's oscillating
latch (s2), ch3's Q′ = T ⊕ Q (s2, s7) and ch4's 7 → 0 stagger (s6). Its teaser points to the next
lecture (p. 101's shift register onwards).

## Decisions
- **Size:** 6 chapters, ~60 min, the top of the 4–6 range. The lecture is ~55 min of teaching in
  two halves: flip-flops (00:05–00:30) and counters (00:30–01:00). Each half splits into three
  questions of 9–11 min: latch, edge, other types; ripple, tables, logic. Five chapters would
  mean 12-minute videos or dropping worked derivations.
- **To shorten:** drop the beyond-the-slides extras listed below (~3 min), or fold ch3 s2 into
  s3.
- **Order:** the lecture's, with one move. The lecturer ran the D-latch and master-slave Yenka
  demos back to back (00:21:36–00:25:01), after the master-slave slides. Each demo goes into the
  chapter that teaches its circuit (ch1 s6, ch2 s6), and p. 88's "superseded" slide closes ch2
  s6.
- **Scope:** pp. 85–101, up to p. 101's "Synchronous Counter" slide. That slide was shown at
  ~00:58:49 but not discussed, so ch6 s8 covers it from the slide.
  - p. 101's shift-register slide and pp. 102+ (set-up and hold, clock skew, metastability,
    parallelism) are next lecture's: teaser only.
  - p. 93's "Memories" slide gets the 2–3 sentences the lecturer gave it (ch4 s2).
  - The previous lecture's pp. 78–84 appear as a refresher (ch1 s2) and a callback (ch5 s3).
    The RS state diagram (pp. 82–84) is left out because this lecture never uses it.
  - Nothing in pp. 85–101 is left out.
- **Exercises:** this part of the slides has none, so there are no hints and no bonus chapter. A
  bonus of our own design problems (e.g. a 0-to-5 counter with D and with J-K flip-flops, using
  don't cares) is possible if the user wants one.
- **Source disagreements (the slides win):**
  - At 00:08:26 the lecturer says R = S = 1 makes Q and Q̄ "both equal to one" (the captions
    agree). Slide p. 81: with NOR gates both are forced to 0. We say 0.
  - The digest's 00:20:00 segment has D starting at 1 and Q rising at the first edge. Slide p. 88
    and the transcript: D starts at 0, and Q is 0, 1, 1, 0 at edges 1–4. We follow the slide.
  - The digest (00:58:52) says the simulated counter is "sync_3b" and builds D2 from an AND and
    an XOR. The video frame at 00:59:30 shows "sync_ctr", with D2 built from 74HC32 OR, 74HC08
    AND, 74HC11 3-input AND and 74HC32 OR: the slide's factored sum of products. ch6 s6 draws
    that. The XOR form appears only as our extra (ch6 s7).
  - The digest writes the next state as Q^{t+1} or Q+; the slides write Q′, and we use Q′.
  - At 00:59:49 the lecturer calls the MSB "the Q1 output"; it's Q2.
  - The request said the recording ends with the master-slave demo. That demo is at
    00:23:16–00:25:01; the recording ends during the synchronous counter demo. Both are used.
- **Beyond the slides, each short and labelled "ours" in the scene list**, all checked by
  enumeration:
  - ch2 s2's oscillating latch, as the concrete reason for edge-triggering;
  - Q′ = T ⊕ Q, and D = Q̄ as a T flip-flop (ch3 s5). The lecturer says FF0 "is essentially a
    toggle flip-flop".
  - why falling edges make the ripple counter count up (ch4 s3);
  - 32,768 Hz = 2¹⁵ for the lecturer's "some funny number" (ch4 s6);
  - Q3·Q1 as the count-of-10 detector, and why 10 rather than 9 (ch4 s7);
  - the full J0/K0 columns (ch5 s7);
  - the XOR/carry pattern (ch6 s7);
  - the 0-to-5 don't-care illustration (ch6 s8).
- **Skipped from the recording:** 00:00–00:04:59 (mic checks; the hardware-practicals
  announcement; the volume remarks).
