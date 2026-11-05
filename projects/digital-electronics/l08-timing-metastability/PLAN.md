# Timing, Metastability and Parallelism: plan

Request: "i moved a new lecture video to the digital electronics folder. i want you to do this
lecture." (2026-10-31). This is Cambridge CST Part IA Digital Electronics (Prof. I. J. Wassell),
**Lecture 8**, recorded Friday 2026-10-23. The number is inferred (see Decisions). Audience: a Cambridge first-year studying the course, who may have watched our Lecture 6 videos.
They know gates, Boolean algebra and K-maps, gate propagation delay (p. 58), hazards and glitches
(pp. 59–62), timing diagrams (p. 60). From Lectures 5–6 (pp. 78–101) they know the reset-set latch,
the transparent D latch, the master-slave D flip-flop and edge-triggering, J-K and T flip-flops,
asynchronous inputs, and the ripple and synchronous counters. Lecture 7 (Wed 2026-10-21) isn't in
our series: it introduced the hardware labs and, from this lecture's references, covered the shift
register, the serial data link and system timing (pp. 101–103). So this plan re-teaches the parts
of it this lecture leans on (ch1 s2–s3, ch2 s3). Set-up time, hold time and clock-to-Q delay are
new to our viewers.
Sources: the slides (`../source/combined_26.pdf`), pp. 104–119. The 60-min recording
(`../source/l08-lecture.{transcript,digest,captions}.md`): the teaching runs 00:03:34–00:54:49,
after ~3.5 min of hardware-lab admin, which we skip. Where the digest disagrees with the slides,
the slides win (see Decisions).
Total: 7 chapters, ~61 min of narration (~9,800 words).

Every number below was checked in Python (Decisions, "Checked numbers"). Script-writers still
check their own.

Lecture-wide conventions (set in ch1, kept to the end):
- **Notation, as on the slides:** T_c is the clock period (capital T) and f_c = 1/T_c. The rest:
  t_su (set-up time), t_hold (hold time), t_pc (clock-to-Q propagation delay), t_pd (propagation
  delay through the combinational logic), t_skew, t_res (resolution time), T_0 and τ (flip-flop
  constants), N (input changes per second), P_fail, MTBF, K, and CB1–CB4. A subscript "min"
  marks the shortest value, as in (t_pc + t_pd)_min. FF0 launches and FF1 receives; the signals
  are Q0, D1, CLK0 and CLK1. pp. 104 and 110 abbreviate the hold time t_h; we write t_hold
  everywhere and say so once (ch1 s3). Units: ps, ns, MHz, GHz.
- **Narration:** name quantities in words: "the set-up time", "the hold time", "the clock-to-cue
  delay", "the logic's delay", "the clock period", "the skew", "the resolution time". Read
  inequalities in words: "the clock period must be at least the clock-to-cue delay, plus the
  logic's delay, plus the set-up time". Don't read symbol strings like "tee-pee-cee".
  Spellings: letters as in L6 ("cue", "dee", "cue zero", "dee one"); "tau"; "tee-nought" for T_0;
  capital "N" for N (LESSONS: "en" is heard as "an"); "meta-stability" and "meta-stable", as L6
  wrote them. Say "mean time between failures" in full and introduce "em-tee-bee-eff" once. Say
  "block one" for CB1 after introducing "combinational block one". "Every edge of the clock",
  never a bare "clock" in a short phrase (L6's "quack").
- **Colours:** L6's roles, extended for this lecture.
  - CLK, CLK0, CLK1 and the T_c arrow: YELLOW.
  - Outputs Q0 and Q: GREEN. Inputs D, D0 and D1: BLUE. The synchroniser's middle node D1 is
    TEAL (an internal node, like L6's Q_int).
  - Intervals: t_pc PINK and t_pd PURPLE (the delays). t_su and t_hold GOLD (the flip-flop's
    "keep D still" window). t_skew TEAL (ch3 has no TEAL signal). t_res FG.
  - Violations, the meta-stable level, "???" and wrong counts: RED. A satisfied constraint gets
    a GREEN tick.
  - The critical path (ch7) is brightened and thickened, and the rest dimmed: no colour role.
  - Pipeline tasks keep one colour each across ch6–ch7: task 1 BLUE, 2 GREEN, 3 TEAL, 4 FG.
- **Timing diagrams in data-sheet style** from ch1 s5 on, as on pp. 104–112:
  - sloped edges;
  - a signal that "could be 0 or 1" drawn as two parallel lines, with a crossover X where it
    changes;
  - a hatched stretch while the logic's output settles;
  - intervals as dimension arrows under the traces, with thin vertical guides at the edges.

  L6's square style appears only in ch1 s5's side-by-side and in callbacks.
- **Running visuals:**
  - *The path:* FF0 → combinational logic → FF1, on one CLK line (p. 104). Drawn in ch1 s4 and
    reused through ch3, where its clock splits into CLK0 and CLK1. ch4's synchroniser is the
    path with the logic taken out, and each pipeline stage in ch6–ch7 is a path.
  - *The budget bar:* one clock period as a horizontal bar, filled with coloured segments. In
    ch1 they are t_pc + t_pd + t_su; ch3 adds t_skew; ch4 has t_res + t_su; ch7 has one bar per
    stage. Hold is a fence at the bar's left end (ch2 s5).
  - *Running numbers:* p. 118's flip-flops, t_pc = 0.2 ns and t_su = 0.1 ns, appear in ch1's
    worked example (ours), so ch7's slide numbers arrive familiar.
- **Reuse from L6** (`../l06-flip-flops-counters/`; its STATUS.md lists them):
  - `make_ff()` (ch2_s6_symbols.py) for every flip-flop box;
  - `sync_counter()` and `led_chain` (ch6_s6_circuit.py) for ch1's hook;
  - `master_slave_end_shot` (ch2_s3_masterslave.py) for ch1 s3;
  - the shift-register sketch on ch6_s8_anysequence.py's end card for ch2 s3;
  - `rs_latch` (ch1_s2_rslatch.py) for ch4 s3;
  - `clock_wave` (ch1_s1_hook.py).

## Chapter 1 · How fast can the clock tick?
Slug: ch1_setup · ~10 min · Source: pp. 103 (System Timing, refresher) and 104–105 · Recording:
00:03:34–00:11:17
Goal: name a flip-flop's three timing numbers (set-up time, hold time, clock-to-Q delay), read a
data-sheet timing diagram of the path from one flip-flop through logic to the next, and derive
and use T_c ≥ t_pc + t_pd + t_su and t_pd ≤ T_c − (t_pc + t_su).
Scenes:
- s1_hook · Hook (~50 s): title card ("Timing, Metastability and Parallelism", course line
  "Digital Electronics · Lecture 8", part line "Part 1 · How fast can the clock tick?").
  - Last time: the synchronous counter, every flip-flop changing on the same edge. Bring back
    L6's `sync_counter()` with its LEDs counting.
  - Speed its clock up (ours): the counting stays right … until, past some speed, the LEDs show
    wrong counts in RED.
  - The question: what sets the fastest clock a circuit can use?
  - The road for the lecture, in one line: timing rules → meta-stability → parallelism.
- s2_clock · Period and frequency (~60 s): p. 103's "System Timing", a refresher (Lecture 7's
  slide; L6 ch1 s3 had the vocabulary).
  - The clock period T_c is the time between rising edges; the frequency f_c = 1/T_c, in hertz.
    Processors run at several gigahertz: 1 GHz ↔ 1 ns.
  - All things being equal, a faster clock gets more work done per second (p. 103).
  - So why not go as fast as we like? Because every tick has to leave the circuit time to do its
    work. This lecture measures that time.
- s3_ffnumbers · A flip-flop's three numbers (~100 s): p. 104, first slide. Its "Previously, we
  saw" was Lecture 7, so teach this from scratch.
  - CLK, D and Q traces around one rising edge. D must be steady for the set-up time t_su before
    the edge and for the hold time t_hold after it (the slide's t_h; we write t_hold throughout).
    Q answers the clock-to-Q delay t_pc after the edge.
  - Shade the window around the edge in GOLD: keep D still here. Values like these come from
    the chip's data sheet.
  - Why a window (ours, ~20 s, a simplified picture): bring back L6's master-slave pair. At the
    rising edge the master latch shuts, so D has to have settled into it before it shuts
    (set-up) and must not change while it's shutting (hold). Then the slave takes time to pass
    the value on to Q (clock-to-Q).
  - Plant: what happens if D does change inside the window is chapter 4's story.
- s4_path · The path between two flip-flops (~75 s): p. 104, second slide.
  - FF0 → combinational logic (CL) → FF1, both clocked by the same CLK.
  - On a rising edge, FF0's output Q0 changes after t_pc. The logic responds, and its output D1,
    FF1's input, changes t_pd after Q0 does.
  - D1 must settle no later than t_su before the next edge.
  - Every synchronous circuit is built of such paths: L6's counter is flip-flops feeding logic
    that feeds the same flip-flops. Shrink the counter onto this picture.
- s5_datasheet · Reading a data-sheet timing diagram (~80 s): p. 105's drawing style, which the
  lecturer explains at 00:05:24. Build it beside a small L6-style diagram:
  - edges drawn sloped, because real edges take time;
  - two parallel lines for "could be 0 or 1, we don't care which";
  - a crossover where the value changes;
  - a hatched stretch where D1 may change several times while the logic settles. Those are the
    glitches of the hazards lecture (pp. 59–62).

  Then draw CLK (with the T_c arrow between rising edges), Q0 (crossing t_pc after the edge) and
  D1. The lecturer marks several possible times D1 might change, depending on the logic's delay.
- s6_setup · The set-up constraint (~95 s): p. 105.
  - The worst case is the latest D1 may settle, exactly t_su before the next edge. Earlier is
    fine.
  - Add up the period: T_c ≥ t_pc + t_pd + t_su. The budget bar appears for the first time, with
    the three segments filling one period.
  - "Worst case" means the largest t_pc and the largest t_pd: maximum delays.
  - Worked example (ours, with p. 118's flip-flops): t_pc = 0.2 ns, t_su = 0.1 ns and 4.7 ns of
    logic give T_c ≥ 5.0 ns, so f_c ≤ 200 MHz.
  - Back to the hook: the counter went wrong once its clock period was shorter than its path's
    sum.
- s7_marketing · Who sets the clock? (~75 s): p. 105, second slide.
  - The lecturer's cynical note: the clock speed is often set by the marketing department.
  - The chip maker fixes the worst-case t_pc (max) and t_su, so rearrange:
    t_pd ≤ T_c − (t_pc + t_su). The logic's delay is usually the only thing the designer
    controls.
  - If redesigning the logic can't meet it, the clock period has to grow, and marketing is "very
    upset".
  - Worked (ours): a 1 GHz target means T_c = 1 ns, so with these flip-flops the logic gets
    0.7 ns. s6's 4.7 ns of logic would have to get almost seven times faster.
- s8_recap · Recap and next (~60 s): recap with small versions of:
  - the clock with T_c and f_c = 1/T_c (s2);
  - the GOLD window with t_su, t_hold and t_pc (s3);
  - the path (s4);
  - the data-sheet diagram (s5);
  - the budget bar, T_c ≥ t_pc + t_pd + t_su (s6);
  - t_pd ≤ T_c − (t_pc + t_su) (s7).

  Next time: the opposite danger, new data arriving too soon, and why a slower clock can't help.
  End card.
Continuity: sets the lecture's notation, colours, data-sheet diagram style, the path and the
budget bar. The numbers t_pc = 0.2 ns and t_su = 0.1 ns return in ch3 s4 and ch7. s3's GOLD
window returns in ch2 (hold) and ch4 (violated).

## Chapter 2 · Hold time
Slug: ch2_hold · ~8 min · Source: pp. 106–107 (to "Propagation Delay – Note"), refresher pp.
101–102 · Recording: 00:11:17–00:18:10
Goal: derive the hold constraint (t_pc + t_pd)_min ≥ t_hold, apply it to directly cascaded
flip-flops (the shift register), explain why slowing the clock can't fix a hold violation, and
say which constraint uses maximum delays and which minimum (contamination) delays.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 2 · Hold time".
  - Last time: set-up time. Data must arrive early enough, and a slower clock always buys more
    time.
  - Now the other side of the window. On one edge FF1 is capturing the old D1 while FF0 is
    already launching the new value towards it: a race (animate the new value running along the
    path).
  - The question: can new data arrive too soon?
- s2_hold · The hold constraint (~105 s): p. 106, first slide.
  - The same CLK/Q0/D1 diagram, now looking just after the first edge. FF1 needs the old D1
    steady for t_hold after that edge.
  - The same edge makes Q0 change after t_pc, and D1 after a further t_pd.
  - The lecturer's two cases: if the change comes after the hold window ends, fine; before it,
    bad (RED).
  - So (t_pc + t_pd)_min ≥ t_hold. It's the minimum because what matters is the earliest the
    change could possibly arrive, the fastest way through.
- s3_shiftreg · Two flip-flops, no logic: the shift register (~90 s): refresher of pp. 101–102
  (Lecture 7's), since the lecturer leans on it here ("the shift register design that I showed
  you", 00:13:54).
  - Three D flip-flops in a chain: Din → Q0 → Q1 → Q2, one CLK line. Reuse L6's end-card sketch.
  - Animate p. 102's diagram: a 1 entering at Din moves one place right on every rising edge.
  - One sentence: that's serial in, parallel out. Loading the flip-flops through their preset and
    clear inputs gives parallel in, serial out, and the two together make a serial data link with
    fewer wires than a parallel one (pp. 102–103).
  - Then the hold question (p. 106, second slide): with no logic between them, t_pd = 0, so
    (t_pc)_min ≥ t_hold. Each flip-flop reads its neighbour's output at the very edge that
    changes it.
  - The slide's conclusion: a reliable flip-flop must have a hold time shorter than its own
    minimum clock-to-Q delay.
- s4_noclockfix · Why the clock can't save you (~80 s): p. 106, second slide.
  - Flip-flops are often designed with t_hold = 0, and then the condition always holds, because
    t_pc is always positive. (At 00:15:35 the lecturer says "less than zero"; he means greater.)
  - Put the two inequalities side by side. T_c appears in the set-up one but not in the hold one,
    so changing the clock period can't fix a hold violation.
  - Hold violations are rarer, but hard to fix, so they "have to be taken seriously".
  - What you do instead (ours, from Harris and Harris, the recommended book): change the circuit
    itself, typically by adding delay (buffers) to the path that's too fast.
- s5_contamination · Longest and shortest delays (~80 s): p. 107, first slide.
  - Every delay is really a range, from shortest to longest. Show t_pc and t_pd as bars with a
    min end and a max end.
  - Set-up cares about the longest (the latest arrival), hold about the shortest (the earliest
    change).
  - Harris and Harris call the minimums contamination delays: (t_pc)_min is the clock-to-Q
    contamination delay and (t_pd)_min the combinational one. It's the earliest an output can
    start to change, "contaminating" the old value. The lecturer: it "sounds slightly scary".
  - Synthesis on the budget bar: the window in which D1 can change, from min to max, must start
    after the hold fence at the left and end before the set-up deadline at the right. Maximum
    delay limits the clock rate; contamination delay decides hold.
- s6_recap · Recap and next (~60 s): recap with small versions of:
  - the race on the path (s1);
  - the hold diagram with its GOOD/BAD sides (s2);
  - the shift register with (t_pc)_min ≥ t_hold (s3);
  - the two inequalities, T_c in only one (s4);
  - the min–max bar between the two fences (s5).

  Next time: so far every flip-flop has seen the edge at the same instant. What if the clock
  arrives late at some of them? End card.
Continuity: same diagram and path as ch1. The shift register returns in ch3 s6 (the bad skew
direction) and ch4 s5 (a synchroniser is a two-flip-flop shift register). s5's two fences are
what ch3 moves with skew.

## Chapter 3 · Clock skew
Slug: ch3_skew · ~8.5 min · Source: pp. 107 (Clock Skew)–109 · Recording: 00:18:10–00:24:31
Goal: say what clock skew is and where it comes from, derive T_c ≥ t_pc + t_pd + t_su + t_skew
and t_skew + (t_pc + t_pd)_min ≥ t_hold for the slide's case, and explain why skew hurts one
constraint and helps the other.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 3 · Clock skew".
  - Last time: both rules assumed the edge reaches every flip-flop at the same instant.
  - Visual: a clock edge travelling as a bright pulse along the wires of a board, reaching
    nearby flip-flops first and distant ones later.
  - The question: what does a late clock do to our two rules?
- s2_skew · What skew is (~65 s): p. 107, second slide.
  - Wires have a delay, and different wire lengths give different delays. So the edges don't
    arrive at all the flip-flops at once, on a big board or across a chip. That variation is
    clock skew.
  - Redraw the path with two clock branches, CLK0 to FF0 and CLK1 to FF1.
  - The slide's case: CLK1 is in advance of CLK0 by t_skew. It could be the other way round,
    depending on the layout (00:19:56).
- s3_skewsetup · Skew and set-up (~100 s): p. 108, first slide. Build the four traces, CLK0, Q0,
  D1 and CLK1, slowly.
  - Q0 changes t_pc after CLK0's edge, and D1 settles t_pd later.
  - FF1's next edge comes t_skew before CLK0's, so D1's deadline (t_su before CLK1's edge) moves
    earlier by t_skew.
  - The budget bar gains a fourth segment: T_c ≥ t_pc + t_pd + t_su + t_skew.
- s4_lesslogic · Less time for the logic (~70 s): p. 108, second slide.
  - Rearranged: t_pd ≤ T_c − (t_pc + t_su + t_skew). Skew eats into the logic's budget.
  - Equivalently, for fixed logic the clock period must grow and the frequency fall.
  - Worked (ours, ch1's numbers): at 1 GHz the logic had 0.7 ns; 0.1 ns of skew leaves 0.6 ns.
    Or keep 0.7 ns of logic, and T_c ≥ 1.1 ns, about 909 MHz.
- s5_skewhold · Skew and hold (~100 s): p. 109.
  - On the same four traces, look at the first edges. FF1's capturing edge (CLK1) comes t_skew
    before FF0's launching edge (CLK0).
  - So, counted from FF1's edge, the new data reaches D1 after t_skew + t_pc + t_pd. The
    constraint: t_skew + (t_pc + t_pd)_min ≥ t_hold.
  - In this case skew makes hold easier: "the availability of hold time is increased".
  - Side by side: the same skew hurt set-up and helped hold.
- s6_otherway · The other direction (~70 s): the lecturer says only that the effect depends on
  which clock is ahead (00:24:02). The algebra here is ours, from the same diagrams.
  - Reverse it, so CLK1 lags CLK0 by t_skew. Set-up gets easier (T_c ≥ t_pc + t_pd + t_su −
    t_skew), and hold gets harder: (t_pc + t_pd)_min ≥ t_hold + t_skew.
  - The worst place for that is ch2's shift register, with no logic to slow the data down. If
    the next flip-flop's clock arrives later than the first flip-flop's minimum clock-to-Q delay,
    a bit can race through two stages on one edge. That's a hold violation no slower clock can
    fix.
  - The lecturer's advice: check skew both ways, because it affects both constraints.
- s7_recap · Recap and next (~60 s): recap with small versions of:
  - the edge travelling across the board (s1);
  - the path with CLK0 and CLK1 (s2);
  - the four-segment budget bar (s3);
  - t_pd ≤ T_c − (t_pc + t_su + t_skew) with 0.6 ns (s4);
  - the hold diagram, skew helping (s5);
  - the two directions as a seesaw (s6).

  Next time: inputs from the outside world, which obey no clock at all, and what a flip-flop
  does when its window is broken. End card.
Continuity: ch1's path and budget bar, ch2's fences and shift register. CLK0 and CLK1 stay
YELLOW, labelled, with CLK1's trace a little dimmer.

## Chapter 4 · Metastability and the synchroniser
Slug: ch4_metastability · ~9.5 min · Source: pp. 110–113 (to the P_fail slide) · Recording:
00:24:31–00:33:04
Goal: explain what metastability is, when it happens, and why it eventually resolves (the ball on
the hill). Read the model P(t_res > t) = (T_0/T_c)·e^(−t/τ), explain how a two-flip-flop
synchroniser works, and derive P_fail = (T_0/T_c)·e^(−(T_c − t_su)/τ).
Scenes:
- s1_hook · Hook (~50 s): part line "Part 4 · Meta-stability".
  - Last time: we can arrange our own signals to respect set-up and hold. A person pressing a
    button can't: they press whenever they like.
  - Visual: a button wired to a flip-flop's D, with the clock ticking past and the press landing
    inside the GOLD window.
  - The lecturer's sigh, quoted: "so many problems with flip-flops!"
  - The question: what does a flip-flop do when its input changes inside the window?
- s2_undefined · Neither 0 nor 1 (~85 s): p. 110, first slide.
  - We can't always control when an input changes, for example one from a button. We can't make
    users respect our set-up time.
  - The slide's diagram: D changes inside t_su/t_hold, and Q becomes "???" (RED).
  - The output is undefined. For a moment it can sit at a voltage between 0 and V_DD (the supply
    voltage), in the invalid range. Show a voltage axis with a valid-0 band, a valid-1 band and a
    RED invalid band between.
  - Logic connected to Q is "highly confused": one gate may read it as 0 and another as 1 (ours,
    a short gloss). This is metastability, and we have to counteract it.
- s3_ball · The ball on the hill (~90 s): p. 110, second slide.
  - Two valleys are the stable states, 0 and 1: a ball stays there unless disturbed.
  - The hilltop is meta-stable: a perfectly balanced ball would stay there forever.
  - Nothing is perfect (the lecturer's wind and imperfect ball), so it eventually rolls to one
    side or the other.
  - How long that takes depends on how well balanced it was. Animate several balls started at
    different distances from the summit: the closest waits longest.
  - Ours, one sentence: inside the flip-flop the memory is a feedback loop like L6's reset-set
    latch, with two resting states and a balance point between them. Show the small `rs_latch`.
- s4_model · How long might it take? (~95 s): p. 111.
  - The output does resolve, but in theory there's no upper limit on the time.
  - The model: P(t_res > t) = (T_0/T_c)·e^(−t/τ). T_c is the clock period; T_0 and τ are
    properties of the flip-flop.
  - T_0/T_c is the chance the input changes at a "bad" time, and it falls as T_c grows. Ours, a
    picture: a narrow window of width T_0 in each period T_c; a random change lands in it with
    probability T_0/T_c.
  - τ is a time constant: how fast the flip-flop leaves the summit.
  - The key point (p. 111, second slide): the probability falls exponentially. Each extra τ of
    waiting divides it by e ≈ 2.7. Plot the decay curve. The derivation isn't on the course (the
    slide says so).
- s5_synchroniser · One more flip-flop (~100 s): pp. 111–112.
  - Meta-stability causes severe system problems, so we minimise its probability with a
    synchroniser. In its simplest form that's one more flip-flop.
  - The circuit: D0 → FF0 → D1 → FF1 → Q, one CLK. It's ch2's shift register with two stages.
  - p. 112's diagram:
    - after an edge, D1 may be meta-stable (RED, mid-level);
    - it has until t_su before the next edge to resolve: that time is t_res;
    - then FF1 sees a valid input that satisfies its set-up and hold, and gives a valid Q t_pc
      after the edge.
  - FF0 takes the risk, so FF1 almost never sees it.
- s6_fail · When the synchroniser fails (~80 s): p. 113.
  - To make an invalid output less likely, give D1 longer to resolve: increase t_res, which means
    a longer T_c, a slower clock.
  - The synchroniser fails if Q goes meta-stable. That can happen if D1 hasn't resolved before
    FF1's set-up deadline, that is if t_res > T_c − t_su. The budget bar: T_c = t_res + t_su,
    with resolution time in the slot the logic had in ch1.
  - Put t = T_c − t_su into the model: P_fail = (T_0/T_c)·e^(−(T_c − t_su)/τ), the probability of
    failure for one input change.
- s7_recap · Recap and next (~60 s): recap with small versions of:
  - the button press in the window (s1);
  - Q's "???" and the voltage bands (s2);
  - the ball on the hill (s3);
  - the decay curve (s4);
  - the synchroniser with its timing (s5);
  - P_fail on the t_res + t_su bar (s6).

  Next time: one failure in ten million changes; is that good enough? We turn P_fail into years.
  End card.
Continuity: ch1's GOLD window (now violated), ch2's shift register (s5), L6's reset-set latch
(s3). P_fail is carried straight into ch5 s1.

## Chapter 5 · Mean time between failures
Slug: ch5_mtbf · ~8.5 min · Source: pp. 113–115 (to the cascade slide) · Recording:
00:32:43–00:37:51
Goal: turn P_fail into a failure rate and an MTBF, MTBF = T_c·e^((T_c − t_su)/τ)/(N·T_0), work
the slide's one-year example by trial and error, and say what cascading K flip-flops does.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 5 · Mean time between failures".
  - Last time: P_fail, the chance that one input change gets through the synchroniser still
    meta-stable.
  - A product has to run for years. Is a failure every ten million changes good enough? That
    depends on how often the input changes.
  - The question: how long, on average, between failures, and how slow must the synchroniser's
    clock be to make that a year?
- s2_rate · From one change to failures per second (~65 s): p. 113, second slide.
  - If D0 changes once per second, the probability of failure per second is just P_fail. If it
    changes N times per second, it's N times greater: P_fail/s = N·P_fail.
  - Visual: a timeline of input changes, each a small dice roll with odds P_fail.
- s3_mtbf · Seconds per failure (~80 s): p. 114, first slide.
  - Reliability is usually measured as the mean time between failures, MTBF: seconds per failure
    rather than failures per second, so MTBF = 1/(P_fail/s).
  - Substitute P_fail and watch it flip: MTBF = T_c·e^((T_c − t_su)/τ)/(N·T_0). The exponent
    changes sign, and T_0/T_c turns upside down.
  - MTBF grows exponentially as the clock period grows.
- s4_example · The example, set up (~85 s): p. 114, second slide.
  - The flip-flops: τ = 200 ps, T_0 = 150 ps, t_su = 500 ps. The input changes 0.2 times per
    second on average, once every five seconds.
  - How long must the synchroniser's clock period be for the MTBF to exceed one year?
  - One year ≈ 31.5 × 10⁶ s (365 × 24 × 3600 = 31,536,000).
  - Substitute, in the slide's layout: 31.5 × 10⁶ = T_c·e^((T_c − 500 ps)/200 ps)/(0.2 × 150 ps).
  - T_c appears both outside and inside the exponential, so there's no closed-form solution.
- s5_trial · Trial and error (~85 s): the slide's method. Fill in a table of tries:

  | T_c | MTBF |
  |---|---|
  | 2.0 ns | 1.4 days |
  | 2.5 ns | 21 days |
  | 3.0 ns | 311 days, just short |
  | 3.04 ns | 384 days ≈ 1.05 years ✓ |

  - The slide's answer is T_c = 3.04 ns, about 329 MHz. (The exact solution is 3.03 ns. The
    lecturer's spoken "three nanoseconds" falls just short of a year; we show the slide's figure.)
  - Ours, the moral: every extra τ (200 ps) of waiting multiplies the MTBF by e, and every extra
    nanosecond by about 150. A small slowdown buys a lot of reliability.
- s6_cascade · More flip-flops (~85 s): p. 115, first slide.
  - If T_c becomes excessive for the MTBF we need, cascade more flip-flops. With K additional
    flip-flops (K = 1 is s5's synchroniser): P_fail_K = (P_fail)^K, so P_fail_K/s = N·(P_fail)^K
    and MTBF = 1/(N·(P_fail)^K).
  - For this to work with a reasonable number of flip-flops, P_fail must be much less than 1.
    Ours: squaring 0.5 only halves it, while squaring 10⁻⁷ gives 10⁻¹⁴.
  - Ours, by the slide's formula: with K = 2, the one-year target needs a clock period of only
    about 1.6 ns instead of 3.03 ns.
  - Present the formula as the course's model (see Decisions); don't add refinements.
- s7_recap · Recap and next (~55 s): recap with small versions of:
  - the timeline of input changes, N per second (s2);
  - the MTBF formula with its flipped exponent (s3);
  - the example's numbers (s4);
  - the trial table with 3.04 ns ticked (s5);
  - the K-stage chain (s6).

  Next time: from making circuits reliable to making them fast. More work per second, without a
  faster flip-flop. End card.
Continuity: P_fail from ch4 s6; the synchroniser drawing from ch4 s5, which grows to K + 1
flip-flops in s6. The trial-table style can match ch1's worked examples.

## Chapter 6 · Latency, throughput and pipelining
Slug: ch6_pipelining · ~8.5 min · Source: pp. 115 (Parallelism)–117 (to the circuit) ·
Recording: 00:37:51–00:44:52
Goal: define token, latency and throughput, tell spatial from temporal parallelism (pipelining),
read the non-pipelined and pipelined task timelines (latency T_c → 2T_c, throughput 1/T_c),
explain why the pipelined T_c is shorter, and say why registers go between pipeline stages.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 6 · Latency, throughput and pipelining".
  - Last time: slowing a clock to buy reliability. Now the other direction: more work per
    second.
  - Visual: tokens entering a box one at a time, each taking the whole period, while the queue
    grows.
  - The question: if one job takes a fixed time, how can we finish more jobs per second?
- s2_speed · Latency and throughput (~75 s): p. 115, second slide.
  - A token is a group of inputs processed to produce a group of outputs.
  - Latency is the time for one token to pass through the system from start to end. Throughput
    is the number of tokens produced per unit time.
  - Animate both on the box from s1. Two different questions: "how long for mine?" and "how
    many per second?".
  - Throughput improves if we process several tokens at once. That's parallelism, and it comes
    in two types.
- s3_twokinds · Two kinds of parallelism (~85 s): p. 116, first slide.
  - Spatial: multiple copies of the hardware, working on several tasks at once.
  - Temporal: break a task into sequential stages and spread several tasks over them. Each task
    passes through every stage, but a different task is in each stage at any time, so tasks
    overlap. Temporal parallelism is often called pipelining.
  - Pipelining is attractive because it raises throughput without duplicating hardware.
  - An everyday picture (ours, from Harris and Harris): baking. A second oven is spatial; rolling
    out the next tray while one bakes is temporal.
- s4_nopipe · One task at a time (~65 s): p. 116, second slide.
  - A task split into stages A then B, taking one clock period T_c in all. Latency T_c,
    throughput 1/T_c.
  - The timeline A1 B1 A2 B2 A3 …: while B works, A's hardware sits idle.
- s5_pipe · Overlapping tasks (~95 s): p. 117, first slide.
  - Start A2 as soon as A's hardware is free, alongside B1. Build the staircase: A1; B1 + A2;
    B2 + A3; B3 + A4.
  - Read the columns as the lecturer does: tasks 1 and 2 here, 2 and 3 here.
  - Latency 2T_c: each task now takes two clock periods. Throughput 1/T_c: one task finishes
    every period once the pipe is full.
  - The puzzle a viewer will spot: throughput is 1/T_c in both slides, so what changed? This T_c
    is the time for one stage, about half the old one. So throughput nearly doubles, and latency
    (two half-periods) stays about the same. Draw the two timelines to one time scale to show it.
- s6_registers · Registers between the stages (~75 s): p. 117, second slide.
  - To pipeline, place registers (D flip-flops) between blocks of combinational logic. That
    divides the logic into shorter stages, which can run on a faster clock.
  - The registers stop a token in one stage catching up with, and corrupting, the token in the
    next. Animate it without a register: the new token's fast signals race into the next block
    while the old ones are still settling. Then with one: each token waits at the register for
    the edge.
  - Each stage is now ch1's path, register → logic → register, so T_c ≥ t_pc + t_pd + t_su
    stage by stage. One clock serves every stage, so (plant) the slowest stage decides.
- s7_recap · Recap and next (~55 s): recap with small versions of:
  - the token box with latency and throughput (s2);
  - copies vs stages (s3);
  - the one-at-a-time timeline (s4);
  - the staircase with latency 2T_c (s5);
  - the register between blocks (s6).

  Next time: a real circuit with real delays. How much does one register buy? End card.
Continuity: ch1's path and inequality (s6). The task colours carry into ch7. "The slowest stage
decides" is ch7 s4.

## Chapter 7 · Pipelining a circuit
Slug: ch7_pipeline_example · ~9 min · Source: pp. 117 (circuit)–119, next-lecture teaser p. 120 ·
Recording: 00:43:52–00:54:49
Goal: find a circuit's critical path and minimum clock period, pipeline it with one register,
compute latency and throughput before and after (12 ns, 83.3 MHz → 13 ns, 153.85 MHz), explain
why the gain is less than double, and say when pipelining can't help.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 7 · Pipelining a circuit".
  - Last time: registers between stages give a shorter clock period.
  - Here's p. 117's circuit: a register, four blocks of logic, a register.
  - The question: how fast can it run, and what does one extra register buy?
- s2_circuit · The circuit and its critical path (~85 s): pp. 117–118.
  - The input flip-flop's Q feeds CB1 (3.2 ns) and CB2 (2.5 ns) side by side. Both feed CB3
    (3 ns), then CB4 (5.5 ns), then the output flip-flop. Point A lies between CB3 and CB4.
  - Every flip-flop has max t_pc = 0.2 ns and min t_su = 0.1 ns: ch1's numbers.
  - Two routes through the logic: CB1 → CB3 → CB4 = 11.7 ns and CB2 → CB3 → CB4 = 11.0 ns. The
    critical path is the slowest route, so CB1, CB3, CB4. Brighten it and dim the rest.
- s3_unpiped · Without pipelining (~65 s): p. 118.
  - T_c = 0.2 + 3.2 + 3 + 5.5 + 0.1 = 12 ns, ch1's inequality on the critical path, shown as a
    budget bar.
  - Latency: one clock cycle, 12 ns. Throughput: 1/12 ns ≈ 83.3 MHz. (The slide prints 83.34;
    show 83.3.)
- s4_cut · One register at A (~95 s): p. 118.
  - Insert a D flip-flop at A, giving two stages.
  - Stage 1: CB1 then CB3 (CB2 is shorter, so it isn't on the critical path). Its bar is
    0.2 + 3.2 + 3 + 0.1 = 6.5 ns.
  - Stage 2: CB4 alone. Its bar is 0.2 + 5.5 + 0.1 = 5.8 ns.
  - One clock drives both, so T_c = 6.5 ns. At 5.8 ns stage 1 would break its set-up constraint
    (ch1). The slowest stage decides (ch6's plant).
- s5_payoff · Nearly double (~90 s): pp. 118–119.
  - Latency: two cycles, 2 × 6.5 = 13 ns, against 12. Throughput: 1/6.5 ns ≈ 153.85 MHz, against
    83.3. That's ×1.85: almost double the throughput for a small increase in latency.
  - Why not exactly double (p. 119)? The stages are unequal, so stage 2 idles 0.7 ns every cycle.
    And the extra register costs its own t_pc + t_su, 0.3 ns.
  - Ours, checked: even a perfectly balanced cut would give 6.15 ns (162.6 MHz), not 6 ns,
    because of that overhead.
  - Ours, checked: a third register, before CB3, gives stages of 3.5, 3.3 and 5.8 ns. T_c drops
    only to 5.8 ns (172 MHz) while latency grows to 17.4 ns. CB4 alone now sets the clock.
- s6_limits · When pipelining can't help (~75 s): p. 119.
  - Pipelining can't help if there are dependencies between tasks. If the current task needs the
    result of a previous task (not just earlier steps of its own), it can't start until that
    task has finished.
  - The lecturer calls this a pipeline stall; processors need special measures for it. Show the
    staircase with a gap.
  - Still, pipelining is one of the most important techniques in high-performance processors.
    Modern chips use both kinds: several cores (spatial), each one pipelined (temporal).
- s7_recap · Recap, the lecture, and next (~85 s): recap with small versions of:
  - the circuit with its critical path (s2);
  - the 12 ns bar (s3);
  - the two stage bars, 6.5 and 5.8 (s4);
  - the before/after numbers (s5);
  - the stalled staircase (s6).

  Then the lecture in one line: flip-flops need time (set-up, hold, skew); outside inputs need
  synchronisers; registers between stages buy throughput. Next lecture: synchronous state
  machines, of which counters are a special case (p. 120). End card.
Continuity: ch1's numbers, inequality and budget bar; ch6's staircase and task colours. The end
card points to Lecture 9.

## Decisions
- **Lecture number: 8, not 7.** The recording doesn't say a number, but three things point to a
  lecture between L6 and this one:
  - L6's recording (Mon 2026-10-19, 00:01:46 and 00:04:59) announces "Wednesday's lecture", which
    would introduce the hardware labs.
  - This recording (Fri 2026-10-23) refers back to "the shift register design that I showed you"
    (00:13:54) and to set-up and hold shown "a couple of times previously" (00:03:34). Its slide
    sorter opens just after the Shift Register, Serial Data Link and System Timing slides
    (digest 00:00:00). None of these is in L6's recording, which ends mid-demo on p. 101's
    counter.
  - The lecturer thanks the students for the lab "yesterday" (Thursday).

  So the course line says "Lecture 8"; the folder and source files were renamed to `l08-`.
  COURSE.md now lists Lecture 7 as unrecorded. The digest's "Lecture 7" is Gemini's guess from
  the file name.
- **Scope: pp. 104–119**, confirmed from the recording. It opens on p. 104 at 00:03:34 and ends
  on p. 119 at 00:54:47; p. 120's title is shown only as the laptop closes (teaser in ch7 s7).
  - pp. 101–103 (shift register, serial data link, system timing) are *not* taught here; they
    were Lecture 7's. This lecture leans on them, and L6's videos ended promising shift
    registers. So ch1 s2 re-teaches system timing and ch1 s3 the flip-flop's three numbers
    (p. 104's "previously"). ch2 s3 gives the shift register as a refresher, with one sentence
    on parallel in/serial out and the serial data link.
  - Nothing in pp. 104–119 is left out.
- **Size: 7 chapters, ~61 min**, at the top of the range, like L6's approved 61.3 min and FoCS
  L4's 7 chapters.
  - The lecture has ~51 min of teaching in three parts: timing (21 min), meta-stability (13 min),
    parallelism (17 min).
  - Each part splits into separate questions: set-up / hold / skew; what meta-stability is /
    how often it fails; the idea of pipelining / the worked circuit.
  - We also teach from scratch ~3 min that the lecturer could assume (t_su, t_hold, t_pc, the
    shift register), because our series has no Lecture 7.
  - Six chapters would need a 12–13-minute pipelining or meta-stability chapter.
  - **To shorten** (the user may prefer): merge ch6 and ch7 into one ~11-min chapter, dropping
    ch7 s5's two "ours" extras and tightening ch6 s3. That gives 6 chapters, ~56 min.
- **Order:** the lecture's, with chapter boundaries placed for one question each.
  - P_fail (p. 113, second slide) closes ch4 and is recalled to open ch5.
  - p. 117's "registers between blocks" closes ch6 as an idea; ch7 opens on its circuit.
- **Title:** kept, "Timing, Metastability and Parallelism". It names the slides' three headings
  (the set-up/hold/skew slides, Metastability, Parallelism). "Pipelining" would undersell the
  spatial half, which is brief but present.
- **Exercises:** pp. 104–119 have none, so there are no hints and no bonus chapter. The slides'
  two worked examples (MTBF, pipelined circuit) are worked in full in ch5 and ch7. A bonus of our
  own practice problems is possible if the user wants one.
- **Student questions:** the only one in the recording is about lab scheduling (skipped). The
  digest's "Questions" are Gemini's own. We answer likely confusions where they arise:
  - why hold uses minimum delays (ch2 s2, s5);
  - why the clock can't fix hold (ch2 s4);
  - why skew hurts one constraint and helps the other (ch3 s5–s6);
  - why the synchroniser's second flip-flop is safe (ch4 s5);
  - why throughput is 1/T_c on both pipelining slides (ch6 s5).
- **Source disagreements (the slides win):**
  - Clock-skew direction. Slide p. 107 and the transcript (00:19:11) say CLK1 is *in advance* of
    CLK0, and pp. 108–109 draw CLK1's edges first. The digest (00:20:00, 00:22:06) says CLK1 is
    delayed. We follow the slides.
  - The pipeline circuit. p. 117 (checked on the rendered page): CB1 3.2 ns and CB2 2.5 ns in
    parallel, both feeding CB3 (3 ns), then CB4 (5.5 ns); A is between CB3 and CB4. The digest
    is wrong twice. At 00:43:52 it has a CB2 → CB4 path of 8.0 ns; it's CB2 → CB3 → CB4,
    11.0 ns. At 00:50:00 it has CB1 = 1.8 ns and CB2 = 3.2 ns, with a critical stage through CB2
    and CB3.
  - The digest's "min tcd = 0.1 ns" (00:50:00); slide p. 118 says min t_su = 0.1 ns.
  - MTBF answer: slide 3.04 ns, lecturer "three nanoseconds" (00:36:23), exact 3.030 ns. At
    3.00 ns the MTBF is 311 days, short of a year; 3.04 ns gives 1.05 years. ch5 shows the
    slide's 3.04 ns and the 3.0 ns row.
  - Unpipelined throughput: the slide prints 83.34 MHz; 1/12 ns = 83.33 MHz. We show ≈ 83.3 MHz.
  - The slides write the hold time t_h (pp. 104, 110) and t_hold (pp. 106–109). We use t_hold.
  - pdftotext shows τ as "t" on pp. 111 and 114: it's τ.
  - The digest's laundry / assembly-line example is Gemini's, not the lecturer's. ch6 s3's
    baking picture is ours, from Harris and Harris.
- **Transcript slips, corrected silently:**
  - 00:09:24 "the value of TPC, which is the propagation delay through the combinational logic"
    means t_pd.
  - 00:15:35 "always less than zero" means greater.
  - 00:42:19 "latency is 2C" is 2T_c.
  - 00:49:01 "now 5.0" is 5.5 ns.
  - 00:49:26 "0.2 I believe, or 0.1" is t_su = 0.1 ns.
- **The cascade formula (p. 115)** treats the K stages as failing independently, so (P_fail)^K
  also raises the T_0/T_c factor to the K-th power. Published multi-stage models instead add the
  resolution times in the exponent and count that factor once, which gives a smaller (still
  huge) MTBF. We teach the slide's model as the course states it, with ch5 s6's number labelled
  "by the slide's formula", and add no refinement in the narration.
- **Beyond the slides, each short and labelled "ours" in the scene list,** all checked:
  - ch1: the counter miscounting at high speed (s1); the master-slave reason for the window
    (s3); the 200 MHz and 0.7 ns worked numbers (s6, s7).
  - ch2: adding delay as the hold fix (s4).
  - ch3: the 0.6 ns / 909 MHz numbers (s4); the reverse-skew algebra and the shift-register race
    (s6).
  - ch4: the reset-set latch as the hill (s3); the T_0 window picture (s4).
  - ch5: the trial table (s5); "×e per τ, ×~150 per ns" (s5); the K = 2 at 1.6 ns example (s6).
  - ch6: the baking analogy (s3).
  - ch7: the balanced cut (6.15 ns) and the three-stage cut (5.8 ns, 17.4 ns) (s5).
- **Checked numbers** (Python, standard library):
  - Paths 11.7 and 11.0 ns. Unpipelined T_c 12.0 ns, 83.33 MHz.
  - Stages 6.5 and 5.8 ns (idle 0.7 ns). Latency 13.0 ns, 153.846 MHz, speed-up ×1.846.
  - Balanced 2-stage 6.15 ns, 162.6 MHz. Three-stage 3.5/3.3/5.8 ns: T_c 5.8 ns, 172.4 MHz,
    latency 17.4 ns. The cut before CB3 alone gives 3.5/8.8 ns.
  - MTBF example: 1 year = 31,536,000 s; exact T_c = 3.0301 ns.
    | T_c | MTBF | P_fail |
    |---|---|---|
    | 2.0 ns | 1.4 days | |
    | 2.5 ns | 21.2 days | |
    | 3.0 ns | 311 days | |
    | 3.04 ns | 384 days, 1.05 yr | 1.5 × 10⁻⁷ (T_0/T_c = 0.049) |

    e^(1 ns/τ) = 148.
  - K = 2 by the slide's formula: 1 year at T_c = 1.593 ns (P_fail = 4.0 × 10⁻⁴); at 3.04 ns,
    2.2 × 10¹⁴ s (about 7 million years).
  - ch1/ch3 worked examples: 0.2 + 4.7 + 0.1 = 5.0 ns, 200 MHz; 1 − 0.3 = 0.7 ns;
    1 − 0.4 = 0.6 ns; 1.1 ns = 909 MHz.
- **Skipped from the recording:** 00:00–00:03:34 (lab attendance, the rota, a question about lab
  dates) and 00:54:49–end (packing up).
