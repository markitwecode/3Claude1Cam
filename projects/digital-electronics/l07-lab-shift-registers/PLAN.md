# Hardware Labs and Shift Registers: plan

Request: make Lecture 7 of Digital Electronics. Its first ~40 min introduce the hardware
practical classes, which the user hasn't done yet, so a lab-prep video is genuinely useful; the
rest is course content (relayed by the producer, 2026-10-31, with the brief: ~20 min in 2
chapters, overriding the usual depth rule for this lecture only).

This is Cambridge CST Part IA Digital Electronics (Prof. I. J. Wassell), **Lecture 7**, recorded
Wed 2026-10-21. The date confirms COURSE.md's inferred number: the lecture opens with the lab
introduction L6 announced for "Wednesday", and its content part is what L8 refers back to.

Audience: a Cambridge first-year who has watched our L6 videos (latches, D/J-K/T flip-flops,
asynchronous preset and clear, ripple and synchronous counters, the any-count-sequence
procedure). They are about to start the hardware practicals and haven't built a circuit on a
breadboard. In viewing order this lecture sits between L6 and L8. L8 re-teaches system timing as
a refresher (its ch1 s2) and the shift register with one sentence on the serial link (its ch2 s3).
It teaches set-up, hold and clock-to-Q from scratch (its ch1 s3).

Sources:
- The recording (`../source/l07-lecture.{transcript,digest,captions}.md`). Lab part
  00:04:49–00:39:32, content part 00:39:41–00:57:19. Nothing is said before 00:03:27, and
  00:03:27–00:04:49 is admin (skipped). The lab-intro slides are a separate deck that isn't in our
  material, so their text comes from the digest. I checked it on frames.
- The handout `../source/Hardware_26.pdf`: pp. 3, 5–8 for ch1, p. 9's LED pin-out drawing.
  Workshops 1–4 (pp. 9–26) are assessed: orientation only (see Decisions, "Assessed work").
- The slides `../source/combined_26.pdf`: pp. 101–103, and p. 104's first slide as a teaser.

Total: 2 chapters, ~20 min of narration (~3,200 words).

Every bit sequence, colour code and number below was checked in Python (Decisions, "Checked").
Script-writers still check their own.

Lecture-wide conventions:
- **Title card:** "Hardware Labs and Shift Registers", course line "Digital Electronics ·
  Lecture 7". Part lines "Part 1 · Before the hardware lab" and "Part 2 · Shift registers and
  serial links".
- **Voice** (COURSE.md's rules, plus these for the lab vocabulary):
  - Part numbers in words with capital letters: "seventy-four H C zero zero", "seventy-four H C
    seventy-four", "seventy-four H C one nine three". Check them with `vk listen`.
  - Never voice a bare "a" or "ay" (heard "eye"). The screen shows IC1a…IC1d; the narration says
    "chip one", "the first gate on chip one", "integrated circuit" once, then "chip".
  - "five volts", "zero volts" (not "nought", not "vee-see-see"); "ground" for GND; "ohms",
    "two hundred and twenty ohms", "ten thousand ohms"; "multimeter" (the screen may say DMM);
    "dual in-line"; "small-scale integration" in words, with SSI/MSI/VLSI only on screen.
  - "L-E-D" may be read badly. Listen to it once in ch1 s2, and use "light" where natural if it
    fails.
  - ch2: as L6/L8. "dee in", "cue zero", "flip-flop", "preset" and "clear" (not "ess"/"ar"),
    "every edge of the clock" / "clock signal", never a bare "clock" in a short phrase. Use
    "clock-to-output delay" (COURSE.md: "clock-to-cue" was heard as "cock-to-Q"; L8 ch2 on says
    "clock-to-output"), and capital "N".
- **Colours.** ch2 keeps L6's roles: CLK YELLOW, D_in and D inputs BLUE, Q outputs GREEN,
  preset/clear RED, the travelling bits as GOLD digits (L8 ch2 s3, L10), an unknown value drawn
  at both levels. ch1 sets the lab drawings' roles:
  - the 5 V supply (rails, power wires, Vcc pin): GOLD;
  - 0 V/ground: DIM, labelled;
  - so a 1 is bright and a 0 dim, as in L6;
  - the hidden metal strips of the breadboard: TEAL;
  - logic-switch inputs BLUE, LEDs and outputs GREEN (L6's `led`), the clock YELLOW;
  - the pin-1 notch/dot marker: PINK;
  - signal wires in ch1 s6: one colour per connection, from BLUE (input nets) and PURPLE;
  - trouble (floating noise, contention, a grounded output, wires over a chip): RED;
  - correct: GREEN tick.
- **Chip orientation, one view throughout:** chips sit with the notch (pin 1 end) to the left, as
  on the board and the lecture's 7400 drawing. Pin 1 is bottom left. Pins 1–7 run along the bottom
  left to right, and 8–14 along the top right to left. GND (pin 7) is bottom right and Vcc
  (pin 14) top left, at diagonally opposite corners.
  - The handout's p. 7 drawing has the notch at the top (pin 1 top left, GND bottom left, Vcc top
    right), which is the lecturer's "bottom left is ground, top right is five volts". Show that
    once in ch1 s4 as the same chip turned a quarter turn, and use the notch-left view everywhere
    else.
- **Timing diagrams (ch2):** L6's square style, with the clock on top, thin guides at the rising
  edges and small up-arrows. Unknowns are drawn at both levels. Outputs change a little after the
  edge, as p. 102 draws it. L8's sloped data-sheet style is not used here.
- **Running visuals:**
  - ch1: the lecturer's four-NAND excerpt (his Wiring slide) is the hook's diagram and s6's
    worked wiring. The breadboard from s3 carries through s6–s8.
  - ch2: the three-flip-flop chain (L8's `build_chain()`) carries s2–s6. The word 1 1 0 is loaded
    in s5 and sent across the link in s6. Bit patterns are written in flip-flop order Q0 Q1 Q2, left
    to right as the chain is drawn, and never read as numbers.
- **Reuse:**
  - From L6 (`../l06-flip-flops-counters/scenes/`):
    - `make_ff()`, `toggle`/`flip` switches (fixed: off reads as off) and `led`/`set_led`
      (ch2_s6_symbols.py, ch6_s6_circuit.py);
    - `sync_counter()` (ch6_s6_circuit.py) for ch2 s1;
    - `mod_table()` (ch5) for the 0-to-4 count;
    - `timing_diagram()` (ch2_s4_master.py);
    - `async_sketch()`/`pin()` (ch3_s6_async.py);
    - `clock_wave()` (ch1_s1_hook.py).
  - From L8 (`../l08-timing-metastability/scenes/`):
    - `build_chain()`, `digit()`, `pin()` and the serial-link sketch (ch2_s3_shiftreg.py). Set its
      `wave()` slope to 0 for L6's square style.
    - `WindowDiagram` (ch1_s3_ffnumbers.py) for ch2 s8's teaser.
  - ch1's drawings are new: the box, the breadboard, the DIL chip, the multimeter. They're worth
    recording in STATUS.md for later lectures (the electronics part, pp. 163–190).

## Chapter 1 · Before the hardware lab
Slug: ch1_lab · ~10.5 min · Source: handout pp. 3, 5–8 (and p. 9's LED pin-out); lab slides via
the digest · Recording: 00:04:49–00:06:55 (orientation only), 00:06:55–00:39:32
Goal: arrive at the first practical able to find your way round the prototyping box, say which
breadboard holes are joined, find pin 1 and the power pins and decode a 74-series part number,
read a resistor, turn a labelled circuit diagram into short checkable wiring, build in the safe
order (power first, unused inputs tied down) and say why floating inputs misbehave, and
fault-find methodically with a multimeter.
Scenes:
- s1_hook · Hook (~45 s): title card and part line.
  - One bridging sentence: Lecture 6 ended promising shift registers. They're part 2, because the
    lecture began with the hardware labs, and so do we.
  - Visual: the lecturer's four-NAND excerpt on paper beside an empty breadboard. Wires go in
    anyhow, long and crossing, until it's "electrical spaghetti" (his phrase) and the output LED
    stays dark with a RED "?". Rewind. The same circuit goes in short and neat, and the LED
    lights.
  - The question: how do you turn a circuit diagram into a circuit that works first time, and
    find the fault fast when it doesn't?
  - The road, in one line: the box → the breadboard → the chips → wiring → the build order →
    fault-finding.
- s2_kit · Four workshops, one box (~80 s): the "Introduction" and "Prototyping Box" slides (frame
  00:09:30) and handout pp. 3 and 5; 00:04:49–00:11:46.
  - What you build with: logic gates (small-scale integration), counter chips (medium-scale),
    memory chips (very-large-scale), and programmable logic, PALs, in particular the GAL.
    - For a GAL you type your next-state logic as Boolean equations; a programmer writes them into
      the chip. If it's wrong, you reprogram it, which is why people use them. The lab has three
      programming stations for Workshops 2 and 3.
  - The four workshops, titles only (p. 3), each tagged with the kind of chip it uses (from the
    handout's parts lists): 1 Electronic Die (gates, a counter); 2 Shaft Position Encoder (a GAL,
    a counter); 3 Debouncing a Switch (gates, a counter, a GAL); 4 Framestore for an LED Array (a
    memory chip, gates, a counter, flip-flops).
  - Workshop 1 has no preparation, just questions at the end. Workshops 2–4 begin with design work
    to do *before* the session (the lecturer, 00:05:50). Arrive without it and you spend the lab
    designing instead of building and testing.
  - The box, as callouts on a drawing traced from the slide's photo and p. 5's board drawing:
    - the power supply (a power brick into the socket at top left);
    - the power strip;
    - three breadboards;
    - the clock generator: variable frequency, manual or free-running, with a switch to set the
      rate. "Synchronous circuits need a system-wide clock";
    - push switches: two plain and one debounced. Name them only; what "debounced" means is
      Workshop 3's subject;
    - 8 logic switches: left gives 0 V, a 0; right gives 5 V, a 1. They come out on a header that
      you wire to your circuit's inputs, never to 5 V or 0 V;
    - on the left, outputs:
      - two 7-segment displays (each shows 0–F from four binary inputs);
      - an 8-LED bar, which lets you watch signals without wiring your own LEDs;
      - a 10 × 7 LED matrix;
    - a potentiometer.
- s3_breadboard · Which holes are joined (~80 s): the "Breadboard" slide (frame 00:15:00) and
  handout p. 6; 00:11:46–00:17:16.
  - Under the plastic, metal strips join the holes (reveal them in TEAL). Long rows at the top and
    bottom carry power. In the middle, short columns of five holes are joined (the lecturer counts
    them on the real board). Anything in a column is connected to everything else in it.
  - The central trench: a column never crosses it. A chip sits astride it, so each pin gets its
    own column and opposite pins aren't joined (the lecturer, 00:25:59).
  - Power: the white strip beside the boards has a 0 V column (left) and a 5 V column (right).
    Short jumpers carry them to each board's rows, and every chip needs both.
    - Some rows start with no jumpers, so add them.
    - A previous user may have pulled jumpers out: check before you start.
    - Ours, one clause, from p. 6's drawing: a long rail can be broken halfway along, so a chip on
      the far half can sit unpowered.
  - Crowding: a lead pushed into the wrong column makes a connection you never meant. "There's no
    prizes for making this as small as possible."
  - Keep wires short: it's neater, you make fewer mistakes, and fault-finding is easier. Lay the
    circuit out to flow left to right, inputs on the left and outputs on the right (p. 6).
- s4_chips · Reading a chip (~85 s): the "DIL Package" slide (frame 00:20:40), the Wiring slide's
  7400 pin-out (frame 00:23:00) and handout p. 7; 00:17:26–00:21:51.
  - A dual in-line package: 14 pins, 7 a side. The lab's counter has 16.
  - Find pin 1 first. Older chips have a white dot; newer ones are laser-marked and hard to read,
    so look for the semicircular notch at one end. Get it wrong and the whole chip is wired wrong.
  - Numbering runs anticlockwise from pin 1, seen from above (the convention's view; animate the
    count 1 → 14).
  - Power pins: pin 7 is ground and pin 14 is 5 V; on a 16-pin chip, 8 and 16. That's the last pin
    of pin 1's row and the very last pin, at diagonally opposite corners. Show the quarter turn to
    the handout's notch-up view once: "bottom left ground, top right five volts" (the lecturer).
    The slide warns "there are exceptions", though none among the lab's chips.
  - The part number, 74 | HC | 00:
    - 74 is the series, around since the 1960s;
    - HC is the technology, high-speed CMOS. They were first made in bipolar technology, which was
      too power-hungry and expensive. CMOS is in nearly every chip today and comes later in this
      course;
    - 00 is the function: four 2-input NAND gates, a "quad NAND".
  - Never take a pin-out for granted (p. 7): the 7400 (quad NAND) beside the 7402 (quad NOR). The
    package and power pins are the same, but the NAND's outputs are pins 3, 6, 8, 11 and the
    NOR's are 1, 4, 10, 13. The lab has a pin-out booklet.
- s5_leds · LEDs and resistors (~55 s): handout pp. 7–9 (Appendix 1; the LED pin-out drawing);
  00:17:16 and 00:29:25–00:29:53.
  - An LED lights only one way round: the longer leg is the anode, the shorter one (by the flat
    on the rim) the cathode (p. 9's drawing). The worksheet says which way it goes.
  - It needs a resistor in series, or it can draw enough current to destroy itself (p. 9). The
    worksheet gives the value. Draw it only as 5 V/output → resistor → LED → 0 V (see Assessed
    work).
  - Reading the value (Appendix 1):
    - the first two bands are digits, the third is how many noughts follow, and a last band gives
      the tolerance (gold is 5%);
    - the digits 0–9 are black, brown, red, orange, yellow, green, blue, violet, grey, white.
      Ours: 2 to 7 run through the rainbow;
    - examples: red-red-brown is 220 Ω; brown-black-orange is 10 kΩ; the appendix's own
      yellow-violet-orange is 47,000 Ω;
    - some resistors have three digit bands; the appendix's yellow-violet-black-red is also
      47,000 Ω.
  - Unsure? Measure it: the multimeter reads resistance (the lecturer).
- s6_wiring · From diagram to wires (~100 s): the Wiring slide (frame 00:23:00) and the "Building
  - Tips" slide (00:28:57–00:31:14), handout pp. 6–7; 00:21:51–00:28:57 and 00:29:53–00:31:18.
  - Before any wire, draw the circuit in your log book (p. 7):
    - number the chips IC1, IC2 …;
    - letter the gates on each, IC1a to IC1d;
    - write a pin number on every gate input and output.
  - Why the labels matter:
    - with two identical chips (Workshop 1 uses two quad NANDs), unlabelled gates mean "a wiring
      disaster";
    - a demonstrator can't help you check a design that's only in your head.
  - The lecturer's excerpt, exactly as on his slide and no more: gates 1a and 1b with inputs tied
    in pairs, 1c fed by their outputs (pins 9, 10 → 8), and 1d (pins 13, 12 → 11). Read off the
    connections as a list: 1–2, 1/2–13, 4–5, 4/5–12, 3–9, and 6–10, which the slide shows but
    the lecturer doesn't walk through.
  - Wire them on the s3 board, one at a time, striking each off the list in pencil as it goes in:
    - 1–2: a short U-shaped wire right beside the chip. Two long wires running to the same distant
      point is how spaghetti starts;
    - 1/2 to 13, and 4/5 to 12: across the trench, which doesn't connect anything by itself;
    - 3 to 9, and 6 to 10 (each output goes up across the trench).
  - The rules, shown as the wires go in:
    - route round the chip, never over it, or you can't probe its pins or pull out a faulty chip
      (RED cross on a wire over the top);
    - every chip faces the same way, pin 1 to the left. Flipping one might save a wire, but it
      confuses you and the demonstrator;
    - put chips that share many connections next to each other;
    - use colours for different kinds of wire (p. 6);
    - build and test one section at a time (p. 6).
- s7_build · Power first, and the inputs you don't use (~90 s): the "Building - Tips" and "Building
  and Testing - Tips" slides (frame 00:34:30); 00:31:18–00:36:33.
  - The build order, as a checklist that ticks down the screen:
    1. check every chip has all its legs (other people have used them);
    2. insert all the chips, the same way round, checking that no pin has folded under or
       sideways;
    3. wire 5 V and 0 V to every chip;
    4. tie unused inputs down;
    5. then the rest.
  - Why power first: diagrams usually leave out the supply pins, as "taken as read", so they're
    easy to forget. A CMOS chip with no supply can power itself up through any input that's at
    5 V. Then it half works, depending on the inputs: "almost working but not quite". (Ours,
    optional clause: through the protection diodes on its inputs.)
  - Floating inputs, on the 74HC00 with one gate used and three spare (the lecturer: Workshop 1
    starts like that):
    - a CMOS input has a very high resistance, so tiny currents picked up from stray
      electromagnetic radiation become real voltages;
    - an unconnected input drifts, and its gate switches at random (a RED flicker);
    - nobody uses that output, but CMOS power goes with how often it switches, so the chip draws
      more power;
    - it can also upset the other gates in the same package (the slide).
  - The lecturer's story: a shop's heating-and-ventilation controller switched things on and off
    when someone waved their hands near it. Inside, unused inputs had been left unconnected.
  - The fix: tie each unused gate input to 0 V. Ours, one sentence, echoing the handout's
    "appropriate logic levels": a control input on a bigger chip goes to whichever level keeps it
    idle, so check the pin-out.
  - Never tie an unused *output*. An output is either unused, so leave it alone, or it drives
    inputs. Grounded, it will try to push 5 V into a short circuit whenever it outputs a 1 (RED).
  - Plant: "power goes with how often it switches" comes back in part 2.
- s8_faults · When it doesn't work, and recap (~125 s): the "Testing" slides (00:28:57) and three
  "Building and Testing - Tips" slides (frame 00:37:00); 00:28:57–00:29:25 and
  00:36:35–00:39:23.
  - Tools:
    - an oscilloscope shows voltage against time, but takes desk space, so it's for when you're
      really stuck. If you use one, connect its probe's ground to the circuit's ground;
    - the lab's tool is the digital multimeter, used as a voltmeter (it also measures current and
      resistance).
  - The hunt, in order, on the s6 board with a probe:
    1. supply pins first: 5 V and 0 V where expected. If every 5 V pin reads 0 V, suspect a short
       between 5 V and 0 V;
    2. the clock: is it reaching every clocked chip, at the frequency you set? A forgotten
       flip-flop is easy;
    3. then follow the signal: a gate's inputs, then its output against what it should be, then
       that output arriving at the next input pin. Stop at the first thing that looks fishy.
  - A reading that's neither near 0 V nor 5 V (the lecturer's made-up 1.2 V, in RED) shouldn't
    exist in a logic circuit. Usually two outputs are wired together and fighting, one pulling to
    1 and the other to 0. Sometimes a chip is broken.
  - A faulty chip goes in the bin, not back in the box: otherwise it's "a booby trap for next
    week's class".
  - Still stuck? Ask a demonstrator. A clear diagram and tidy wiring make that quick.
  - Recap, with small versions of each scene's visual and one line each:
    - the box (s2): "switches in, displays out, clock and 5 V on board";
    - the TEAL strips and trench (s3): "columns joined, the trench splits them";
    - the chip with pin 1, the power corners and 74 | HC | 00 (s4);
    - the LED, resistor and colour bands (s5);
    - the labelled excerpt with its struck-off list (s6);
    - the build checklist with the spare inputs grounded (s7);
    - the probe reading 1.2 V (s8).
  - Next: back to the lecture. Wire Lecture 6's flip-flops in a chain and they pass bits along:
    shift registers, and how a serial link sends a whole word down one wire. End card.
Continuity: the four-NAND excerpt (hook, s6) and the s3 board (s6–s8) carry the chapter. The
chip orientation is fixed in s4 and kept. s7's "power goes with switching" is called back in ch2
s7. s5's LED-plus-resistor returns in ch2 s4 (the demo's 270 Ω resistors). s6's IC1a labelling
returns in ch2 s4 (the demo's chips are labelled that way).

## Chapter 2 · Shift registers and serial links
Slug: ch2_shift · ~9.5 min · Source: slides pp. 101–103, p. 104 first slide (teaser) ·
Recording: 00:39:41–00:57:19
Goal: build a shift register from D flip-flops and trace it edge by edge (serial in, parallel
out); load it in parallel through preset and clear (parallel in, serial out); explain how the
two make a serial data link, and what it trades; define clock period and frequency, and say why
a faster clock costs energy.
Scenes:
- s1_hook · Hook (~45 s): part line "Part 2 · Shift registers and serial links"; 00:39:41–00:42:16.
  - Last time: the lab bench. Before that, Lecture 6's synchronous counter: three D flip-flops on
    one clock line (L6's `sync_counter()`, counting).
  - The lecturer's reminder (p. 101, first slide; L6 ch6 s8 taught it): any count sequence comes
    from the same three steps. A 0-to-4 counter never visits 5, 6 or 7 (DIM in `mod_table()`), so
    they're don't cares.
  - Now take the logic out: the counter's logic fades and the flip-flops line up, each Q wired
    straight to the next D.
  - The question: with no logic at all, what does a chain of flip-flops do?
- s2_chain · A chain of D flip-flops (~75 s): p. 101, second slide; 00:42:21–00:43:31.
  - p. 101's drawing (L8's `build_chain()`):
    - three D flip-flops; D_in (BLUE) goes into the first;
    - each Q (GREEN) goes into the next D and up to an output label, Q0, Q1, Q2;
    - one CLK line (YELLOW) feeds every clock input, so it's synchronous;
    - the triangle has no bubble, so they're positive-edge-triggered (L6's symbol rules).
  - At a rising edge, every flip-flop copies its own D, which is its left neighbour's Q. They all
    sample at the same instant, so each takes its neighbour's *old* value. A bit (GOLD digit)
    moves one place per edge.
  - Ours (checked): build it from L6's transparent latches instead, and while the clock is high a
    bit runs through every stage at once. That's L6 ch2's reason for edge-triggering. Why
    flip-flops hand over cleanly despite their own delays is next lecture's question (one clause).
  - Names: a serial input D_in, one bit at a time; parallel outputs Q0, Q1, Q2, all at once.
- s3_trace · Following the bits (~95 s): p. 102, first slide; 00:43:00–00:46:16.
  - Build p. 102's diagram in L6's style: CLK, D_in, Q0, Q1, Q2, with nine rising edges. D_in is
    sampled 0 0 1 1 1 0 0 1 1 (Decisions, "Checked").
  - Before the first edge all three outputs are unknown, drawn at both levels.
  - Walk edges 1–6 as the lecturer does, then let 7–9 run:
    - Q0 takes D_in at each edge;
    - Q1 takes Q0's old value, so at edge 1 it copies an unknown and stays unknown until edge 2;
    - Q2 is unknown until edge 3.
  - The picture: the same waveform appears three times, each a clock period further right. "Data
    moves one position to the right on application of each clock edge." A GOLD highlight follows
    the first 1 as it enters Q0 at edge 3, Q1 at edge 4 and Q2 at edge 5.
  - Ours, checked: after three edges every output is known. A register of N stages forgets how it
    started after N edges.
- s4_demo · Watching it shift (~55 s): the Yenka demo, 00:46:16–00:48:17 (frame 00:46:40).
  - Re-enact the simulation "Four-Bit Shift Register":
    - four D flip-flops on two 74HC74 chips, labelled IC1a, IC1b, IC2a, IC2b. That's part 1's
      labelling, in the lecturer's own drawing. 74HC74 decodes as in part 1: 74, HC, and 74 is a
      dual D flip-flop;
    - an INPUT switch and a CLK switch, which he flips by hand, so each 0 → 1 is one rising edge;
    - an LED on every Q through a 270 Ω resistor. That's part 1's rule; the lecturer jokes that
      the simulator makes the LED explode without one.
  - Run it:
    - INPUT 1 and one edge: the first LED lights;
    - INPUT back to 0, then three edges: the lit LED walks along to the last one (checked: 1000,
      0100, 0010, 0001), and a fourth edge shifts it out;
    - then a few 1s and 0s, and the pattern marches right.
  - Serial in, parallel out: a stream of bits on one wire becomes a 4-bit word on four outputs.
  - Leave the S and R pins out of this drawing; s5 introduces them.
- s5_load · Loading in parallel (~75 s): p. 102, second slide; 00:48:25–00:50:12.
  - The lecturer goes back to the simulation. Each flip-flop has two more pins: asynchronous
    preset and clear (L6 ch3, RED). They force Q to 1 or 0 at once, whatever the clock is doing.
    Their usual job is starting a state machine in a known state (L6).
  - A second use: set every flip-flop at once, preset where the bit should be 1 and clear where it
    should be 0. That's a parallel input.
    - On the chain, grow PRE/CLR pins (L8's `pin()`, L6's style) and load the word 1 1 0 into
      FF0, FF1, FF2.
  - Now apply edges of the clock: the bits leave through Q2, one per edge. First FF2's 0, then 1,
    then 1, filling a small queue at the right. That's parallel in, serial out.
- s6_link · The serial data link (~95 s): p. 103, first slide; 00:50:07–00:52:32.
  - p. 103's diagram:
    - a "Parallel in, serial out" box with D0 D1 D2 on top ("Parallel Data Input");
    - one "Serial Data" wire to a "Serial in, parallel out" box with Q0 Q1 Q2 on top ("Parallel
      Data Output");
    - one CLK line under both.
  - Send the word 1 1 0 across, one edge at a time (checked):
    - edge 1: the wire carries D2 = 0, which lands in the receiver's Q0;
    - edge 2: D1 = 1 arrives and the 0 moves on;
    - edge 3: D0 = 1 arrives;
    - the receiver now reads Q0 Q1 Q2 = 1 1 0. The bit that leaves first travels furthest, so
      every bit lands in its own place.
  - Ours, one sentence: in between, the receiver holds a half-shifted word, so it has to know
    which edge completes a word.
  - Why bother: the old parallel links had one wire per bit, often eight or more, plus a clock.
    That's heavy, costly cable between distant ends. A serial link needs one data wire, plus the
    clock in the slide's design. Show beside it a DIM parallel link (L8's ghost: "3 wires → 1").
  - USB is a serial link (the lecturer's example). Ours, one clause (checked): USB goes further and
    sends no separate clock; the receiver recovers it from the data.
  - The cost: one bit at a time, so the bits must go N times faster to move a word in the same
    time: three times here, eight for a byte. Much less cable, a faster rate.
- s7_timing · How fast should the clock tick? (~55 s): p. 103, second slide; 00:52:35–00:55:08.
  - The clock period T_c is the time between rising edges (between falling edges for a
    falling-edge circuit, which is rare). The frequency is f_c = 1/T_c, in hertz. Processors run
    at several gigahertz: 1 GHz means 1 ns.
  - All things being equal, a faster clock does more work per second: more edges, more steps. The
    serial link wants one too.
  - The lecturer's catch: the faster CMOS logic is clocked, the more energy it uses each second,
    because its power goes with how often it switches (part 1's floating inputs). So small
    battery-powered devices, like sensor nodes, run slow clocks, while a laptop with a big battery
    or on mains can run faster.
  - Plant: even with unlimited power there's a limit, set by the flip-flops themselves.
- s8_recap · A flip-flop's three numbers; recap and next (~75 s): p. 104, first slide;
  00:55:08–00:57:19.
  - The lecture's last slide, as a preview (~25 s; L8 ch1 s3 teaches it at length). Use L8's
    `WindowDiagram`: CLK, D, Q around one rising edge.
    - D must be steady for a set-up time before the edge and a hold time after it (the GOLD
      window);
    - Q answers a clock-to-output delay later (PINK);
    - if D changes inside the window, the output can't be guaranteed.
    - Names only, no "why" and no numbers.
  - Recap with small versions of:
    - the chain on one CLK line (s2);
    - the three shifted waveforms (s3);
    - the walking LED (s4);
    - the preset/clear load and the bits leaving Q2 (s5);
    - the link with 1 1 0 arriving (s6);
    - f_c = 1/T_c beside a battery (s7).
  - Next lecture: what sets the fastest clock speed a circuit can use? (L8 ch1's opening
    question.) End card.
Continuity: ch1's LED-and-resistor (s4), IC labelling and part numbers (s4) and "power goes with
switching" (s7) are called back. L6's counter, `mod_table()`, transparent latch, and preset/clear
are called back (s1, s2, s5). The chain and the word 1 1 0 carry s2–s6. The teaser hands over to
L8 ch1, whose refreshers (system timing, the shift register) now repeat this chapter briefly.

## Decisions
- **Size: 2 chapters, ~20 min (~10.5 + ~9.5),** per the brief's override of the 45–60 min rule
  for this lecture only.
  - ch1 runs slightly over 10 min because the lab part is 33 min of dense practical advice, and
    the handout adds the box's contents and the colour code.
  - Each chapter has 8 scenes. To trim ch1 to 10 min, fold s5 (LEDs and resistors) into s4 and
    s2's box tour, and drop the colour code's second example.
- **Scope, confirmed from the recording.** The content part covers:
  - p. 101's first slide, recapped with a new 0-to-4 example (00:39:41). It goes into ch2 s1 only,
    since L6 ch6 s8 taught it;
  - pp. 101 (second slide) to 103;
  - p. 104's first slide (00:55:08–00:57:19): set-up, hold and clock-to-Q, which the lecturer
    calls "a reminder of what I said previously".
  - Since L8 ch1 s3 teaches that slide from scratch at length, ch2 s8 gives it a ~25 s preview
    with names only. The brief's "pp. 101–103" is therefore pp. 101–104 (first slide).
  - Nothing from the slides is left out.
- **Skipped as admin:**
  - 00:03:27–00:04:49: where to find the handout, the lab room, days and times, the first group
    "tomorrow";
  - the ticking logistics (hand answers to a named demonstrator, re-ticking, storing an
    unfinished box, leaving when done);
  - the demonstrators' names;
  - "any questions?" (none were asked);
  - the handout's rules on sessions, punctuality and the Head of Department's portfolio notice.
  - Kept as practice, not admin: do the preparation before the session; keep a log book someone
    else could follow; draw before you wire.
- **ch1 order:** the recording's, with three moves that teach better.
  - "Draw and label the diagram first" (00:29:53, after his wiring example) opens s6, because it's
    step one of wiring.
  - The scope and multimeter slide (00:28:57) moves to s8, where they're used.
  - The LED's orientation (00:17:16) and the multimeter's resistance range (00:29:40) join the
    handout's colour code in s5.
- **ch1 additions from the handout:**
  - the four workshops' titles (p. 3);
  - the box's full contents: manual/free-running clock, the debounced button, the LED bar and
    matrix, the potentiometer (p. 5);
  - signal flow left to right, colour-coded wires, one section at a time (p. 6);
  - 7400 versus 7402 and the pin-out booklet (p. 7);
  - the log book (p. 7);
  - Appendix 1's colour code (pp. 7–8);
  - the LED pin-out (p. 9);
  - the "appropriate logic levels" caution for control inputs (pp. 15, 23, generalised).
- **Assessed work (binding on script-writers and directors).** The workshops are assessed by
  demonstrators, so ch1 says at most what each is about. In particular:
  - **Workshop 1** (no preparation; four questions):
    - don't work out what the die circuit displays for any input (Q1);
    - don't give how much current a 74HC00 output can supply or sink (Q2);
    - never draw or describe an LED lit by a *low* output, that is an LED and resistor returning to
      5 V, nor how that saves gates (Q3–Q4);
    - don't work the sheet's resistor calculation or show Steps 3–4 (the counter, the count-of-7
      decode).
    - ch1 s6 wires only the lecturer's own excerpt (his slide), never evaluates it, and shows no
      more of the die.
  - **Workshop 2:** no state table, K-map, PAL equation syntax or Gray-code sequence. Don't say why
    the encoder needs no debouncing (Q1) or how fast it may turn (Q2).
  - **Workshop 3:**
    - don't explain what switch bounce is or why a debouncer is needed (Q1);
    - ch2 must not link shift registers to debouncing in any way: no "wait for several samples to
      agree", no all-ones or all-zeros detectors. Its Step 4 preparation is a shift-register
      debouncer;
    - say nothing about choosing a sampling clock (Q2);
    - nothing on active-low reset-set latches (its Step 3 preparation).
  - **Workshop 4:** nothing beyond "a memory chip". Don't discuss the write button, synchronising
    it (Q3), the LED matrix's current (Q1), or control-logic timing (Q2, Q4). ch2's mention of the
    74HC74 is identification only (the demo uses it).
  - Allowed, because they're the lecture's own: unused inputs to 0 V; outputs fighting; LEDs need
    series resistors; a GAL is programmed with Boolean equations.
- **Source disagreements:**
  - Breadboard columns: the lecturer counts five holes on a photo of the real board (00:15:02),
    and his slide says "five hole strips"; the handout (p. 6) says and draws six. We say five, the
    real board. p. 6's drawing also breaks the top rail halfway, the source of ch1 s3's "ours"
    clause.
  - p. 102's diagram has 9 rising edges with D_in 0 0 1 1 1 0 0 1 1 (rendered page). The
    digest's "6 cycles" covers only the edges the lecturer walked through.
  - The demo's chips are 74HC74 (frame 00:46:40); the digest says 74HCT74.
  - Pin 1: the digest's "pin 1 to the left of the notch with the notch up" and its DIL layout
    paragraph are muddled. Conventions above (from the lecture's 7400 drawing and p. 7).
  - The digest's glosses (CMOS "harvesting power through protection diodes", the HVAC unit
    reacting to "electrostatic charge from passing hands") aren't the lecturer's words. The diode
    mechanism is correct, so it's offered as an optional "ours" clause in ch1 s7; the story is
    told as the lecturer told it.
  - The digest's Wiring-photo "decoupling capacitor" isn't mentioned by the lecturer: left out.
  - The lecturer implies USB has "one data wire and one clock wire" (00:51:44). USB sends its
    clock inside the data, and the receiver recovers it (NRZI with bit stuffing). ch2 s6 calls USB
    a serial link and attributes the clock wire to the slide's design only.
  - The demo's flip-flops have active-low preset/clear (S and R tied to 5 V when idle, frame
    00:46:40). ch2 draws L6's active-high PRE/CLR style and doesn't show the ties, so L6's
    convention holds. L10 introduces active-low bubbles later.
  - The handout says the lab introduction is in "week 2 (Lecture 4)"; it was Lecture 7 (admin,
    not used).
- **Transcript slips, corrected silently:**
  - "Yankathy", "Yenca", "Janka" are Yenka;
  - "nanogates" are NAND gates;
  - "the whole time" is the hold time (00:56:03);
  - "OrkVolts" is nought volts.
- **Beyond the material, each short and labelled "ours" in the scene list:**
  - ch1: the split rail (s3); the rainbow digits (s5); protection diodes (s7, optional);
    control-input levels (s7).
  - ch2:
    - the transparent-latch contrast (s2);
    - "N stages forget their start after N edges" (s3);
    - the receiver needing to know when a word is complete (s6);
    - USB's recovered clock (s6);
    - "×N faster" (s6, implied by the lecturer's "the rate … increases").
- **Title:** kept, "Hardware Labs and Shift Registers". It names the lecture's two halves (the
  lab slide deck is "Digital Electronics: Hardware Labs"). The serial link and system timing sit
  under "shift registers" in ch2's part line.
- **No exercises** in pp. 101–104, so no hints and no bonus chapter. The workshops' questions are
  assessed and must not be answered.
- **Checked** (Python 3.11.9, `python3 -I`):
  - p. 102's trace, after each rising edge (X = unknown):

    | edge | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
    |---|---|---|---|---|---|---|---|---|---|
    | D_in | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
    | Q0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
    | Q1 | X | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 |
    | Q2 | X | X | 0 | 0 | 1 | 1 | 1 | 0 | 0 |

  - Demo, 4 bits, input 1 for one edge, then 0: 1000, 0100, 0010, 0001, 0000.
  - Serial link (one shared clock, the transmitter's own D_in tied to 0), word D0 D1 D2 = 1 1 0:
    - the wire carries 0, 1, 1 (D2, D1, D0);
    - the receiver's Q0 Q1 Q2 after each edge: 0XX, 10X, 110;
    - also checked for 100 and 011: the word always arrives in place.
  - Colour codes: red-red-brown 220 Ω; brown-black-orange 10,000 Ω; yellow-violet-orange and
    yellow-violet-black-red 47,000 Ω; red-violet-brown 270 Ω (the demo's resistors).
  - The 0-to-4 counter's unused states: 5, 6, 7. 1 GHz ↔ 1 ns.
  - 7400 outputs: pins 3, 6, 8, 11; 7402 outputs: pins 1, 4, 10, 13 (both GND 7, Vcc 14).
