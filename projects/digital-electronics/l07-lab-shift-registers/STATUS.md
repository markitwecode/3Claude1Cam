# Hardware Labs and Shift Registers: status

2026-10-31: project created; planning.

## Chapter 1 · Before the hardware lab (ch1_lab)
- State (2026-11-01 ~12:00): **done.** Video `out/ch1_lab.mp4`, 12.5 min (749.6 s), 1920×1080 at 60 fps; narration 11.6 min + gaps + ~8 s end card. Review rounds: two, then this resumed round 2 (Gemini scene reviews, s8 fix pass, s5 re-rendered for its re-voiced line), final, final viewer + transitions reviews (no fix round needed). Music `music/ch1.json`: Serendipity (hook), Fragments (under wire.4), Quantum Blue (recap + end card).
- Build order (helpers flow forward): s2, s3, s5 → s4, s6 → s1, s7 → s8.
- Helpers for ch2 (s1, s4, s7 reuse them; import, don't copy):
  - end card: `Faults.end_card()` in `scenes/ch1_s8_faults.py` (~l.637): the recap tiles small, the two
    chains (`chain()`, L8's `build_chain()`) and "Next"; title card from `lib.titles.title_card(...)` as
    `scenes/ch1_s1_hook.py` uses it.
  - "74 | HC | 00" chip-number split: `part_split(center, size, gap)` + `split_box(part, color)` in
    `scenes/ch1_s4_chips.py` (`.parts`, `.split_moves()`, `.cols`, `.colors`, `.tags`; see its docstring).
  - floating-input view: `floating_inputs(at, pitch)` in `scenes/ch1_s7_build.py` (IC2 large, one gate
    wired, `.ends`/`.leads` on the spare pins), with `pickup_waves()`, `start_wobble()` and `Flicker`.
  - board and chip: `Breadboard`, `DipChip`/`dip_chip()`, `wire()`, `green_led()` in
    `scenes/ch1_s3_breadboard.py`; `two_chip_board()`/`finished_board()` in `ch1_s7_build.py`.
- Rewritten for the ear / rules (all re-voiced):
  - hook.2 {dark}: "The light at the output stays dark" → "It fails, and you have no idea why." (producer's rule: never an LED wired to the excerpt chip, so the hook has no LED; failure is a RED "?", success a GREEN tick).
  - leds.3 {noughts}: "how many noughts follow" → "how many zeros follow" (all three Whisper models heard "knots"); on-screen text says "zeros" too.
  - leds.4 {ex1}: "two, two, and one nought, two hundred and twenty ohms" → "two, two, then a single zero. That's two hundred and twenty ohms." (Whisper garbled it on all three models).
  - leds.4 {ex3}: "is forty-seven thousand too" → "also gives forty-seven thousand" (s5 review heard "forty-seven thousand two").
  - leds.3 {table}: "The digits go black, …, blue, violet, grey, white, for zero to nine" → "From zero to nine, the digits go black, brown, red, orange, yellow, then green, blue, violet, grey and white." (Gemini heard "violet" as "filet" (+qa), then "green" as "reen"; the split list re-listened clean.)
  - kit.1 {gal}/{equations}: "GALs" and "For a GAL" were read as letters ("gee ay ell", Gemini high) → "called gals, for generic array logic" and "For these chips"; the long list sentence (then heard "inegration", "perammble") split into short sentences. Re-listened clean.
  - leds.1 {led}: "light-emitting diodes, L-E-Ds" (s5 review heard "leads") → "light-emitting diodes, called L-E-D lights" (an interim take heard "dyads"); {sheet} "The worksheet says which way round it goes" (heard "wordsheet" after the re-voice) → "Which way round it goes is on the worksheet". Re-listened clean.
  - faults.4 {r4}: "An L-E-D goes" (s8 review heard "led") → "An L-E-D light goes"; {r3} "The notch marks" (heard "nudge" after the re-voice) → "The notch at one end marks". Re-listened clean.
- Round-2 Gemini scene reviews (resumed 2026-11-01 11:10), claims checked on frames and accepted as not real:
  s1 12 s "1d drawn as an inverter" (mid-draw), 41 s yellow r/t (colour sweep, as "readboard"); s2 27.5 s
  "4–5 laptops" (the big laptop plus three stations), 61 s red rail flash (the breadboards' printed red/blue
  rail lines), 93.5 s "no bar of lights" (it's there, small); s3 40 s "jumpers reversed" (frame 41 s: grey to
  the 0 V row, gold to 5 V), 57 s quote wording (the lecturer's words, verbatim by design); s4 82.5 s "AND
  without bubble" (mid-draw), 84 s "pin out" (the handout's words, verbatim), 100 s "7402 pin 13 not lit"
  (lights in turn on "thirteen", frame 104.5 s); s5 58 s equation ghost (not seen at 57.8/58.5 s), 69 s dial
  (on Ω at 70 s); s6 44–65 s pin numbers (480p misreads: power at 14/7 and 3–9, 6–10 checked at 69 s); s7
  1–73 s pin claims (squiggles on 4, 5, 9, 10, 12, 13, red on outputs 6, 8, 11, ties land on the 0 V rows:
  frames 43.5/52.5/73.5 s); s8 25 s (pin 14 marked), 87.5 s (pin 7 DIM, as styled), 115.5 s (bit in FF1 at 116 s).
  Real, sent to s8's fix pass: r6/r7 captions at the bottom edge, the recap clearing 0.6 s after r7, the probed
  pin's "9" label drawn beside "7" (read as pin 7), and three flashing captions (booby trap, short, DMM).
- `vk check` dwell flags elsewhere (s1–s7) accepted: each is a caption the narration says aloud as it shows,
  cleared at its planned beat. Small text in s8's recap tiles accepted: miniatures, the caption carries them.
  s2's displays ending on "FE" (a hex count) left as is.
- s8 fix pass (round 2): recap grid moved up (captions ~0.85 above the bottom edge), recap held until "lecture" in faults.5, the probed pin's "9" label moved to pin 9 on the top edge, and the DMM / short / booby-trap captions held longer (3.9, 1.9, 2.3 s; still under the dwell estimate, paced by the narration). Probe touches only pins 14, 7, 1, 2, 3, 9.
- Open: nothing blocking. Gemini still flags only mid-transition claims (listed under Glitches).
- Glitches (scene, time, what, cause):
  - s1 ~43.6 s {board}: "readboard" (Gemini). The road label's colour change sweeps letter by letter, so mid-sweep the first letters read dim. Accepted (mid-transition only).
  - s6 ~93 s {section}: "orange dashed highlights in the rows opposite the power wires" (Gemini). Confirmed: the dashed section box's edges ran between the rails and read as rail highlights. Fixed: the box hugs the chip's rows only. (s6 ~59–61 s "missing 4–5 wire", "stray purple segment": not real, the 4/5–12 wire being drawn on its cue.)
  - s5 ~69 s {ex3}: "a black box covers digits 0–4, digit 5 corrupted", and ~75 s {measure}: "the resistor body turns dark grey" (Gemini). Both confirmed, one cause: FadeOut/FadeIn of a whole resistor makes its opaque cream body semi-transparent, so mid-fade it reads as a dark box. Fixed: the body stays put and only the bands fade and swap.
  - final (transitions review), checked on 1080p frames: s8 ~8.3 s {probe}: "duplicate scope knobs". Confirmed as overlap only: the board fades in over the scope's knob panel while the scope slides left (a fade-in overlapping a move). Accepted (under 1 s). s2 ~54.8 s {box}: the bracket, tags and session bar clear a moment after the workshop cards (staggered clear). Accepted.
  - final, not confirmed on frames (accepted): s1 43 s "breadboard" letters (the colour sweep above); s2 16.8 s labels "morph" (they dim and go); s4 14.7 s counter cut off (fully in frame), 44.1 s GND label (sits under pin 7), 50.1 s "14" detaches (clean mid-turn); s5 68 s swatches scramble (clean); s6 5–20 s gate 1d / grey polygon / stray dot (mid-draw, clean); s7 0.8 s "1 and 4 collide" (the "14" label touches the PINK notch, legible at 1080p), 7.8 s board over item 2 (the {legs} inset over the board, intended), 92.8 s duplicate title (single); s8 116.3 s white mark on CLK (the clock-edge pulse); s2 93.8 s "no bar of lights" and 97.8 s Potentiometer callout over the displays (bar present; callout clear of them).
- Accepted voice flags (QA): chips.5:2 "seventy-four zero zero/two" → "7400/7402" (number format); leds.3:4 "grey" → "gray" (spelling); wire.2:2 "quad NAND" → "quad nant" (jargon); wire.3:1 "lecturer's" → "lectures" (apostrophe only); wire.5:1 "Route" → "Root" (homophone).

## Chapter 2 · Shift registers and serial links (ch2_shift)
- State (2026-11-01): DONE. Video `out/ch2_shift.mp4`, 1920×1080, 60 fps, 9:40.6 (narration 9.1 min). Narration done before the pause (11 lines re-voiced, QA clean) plus link.2 below; music `music/ch2.json` (Euler's Clock hook, Heartbeat under the demo, Clarity under the recap + end card).
- Final reviews (`vk review 2`, `--transitions`): every finding mid-transition. One was real and fixed before the re-final: s1 step list "2 ." / "3 ." (number labels centre-aligned, so old-style 2/3 dropped the "·" to the baseline; now on a common baseline). The rest are accepted below.
- Build order (handovers s1→s2, s4→s5, s7→s8; the s2→s3 and s5→s6 joins fade to empty, so s3 and s6 draw their chains from L8's `build_chain()`/`pin()` themselves): s1, s3, s4, s6, s7 → s2, s5 → s8.
- s1 opens on ch1 s8's `end_card()` frame (rebuilt from `ch1_s8_faults` via load_scene, held 0.7 s). If ch1's end card changes before ch2's final, re-render s1. Checked before the final: ch1_s8_faults.py last changed 11:33, end card/PICS code unchanged, s1 rendered 11:40.
- Rewritten for the ear: link.2 {e3} "At the third, the other one arrives." → "At the third edge, the other one comes in." (Gemini heard "arrives" as "arise", in the s6 review and again in `vk listen --only`; re-voiced, QA clean, re-listened clean). The 10 lines re-voiced before the pause re-listened clean (`vk listen 2 --only`, 0 findings).
- Producer notes applied: s4 runs the recording's order (ones fill, zeros follow, a single 1 walks out), no detector, no "all ones/zeros" tag, nothing on debouncing; s7's tag "it starts with the flip-flops"; s8 uses L8's WindowDiagram with the slide's t_su / t_h / t_pc (t_hold relabelled t_h), spoken "clock-to-output delay"; s4 decodes 74 | HC | 74 in ch1 s4's split style; s7's callback is ch1 s7's `floating_inputs()` + `power_tag()`.
- Two review rounds done (Gemini per scene + holds). Fixes: s1 step highlight moves with the spoken step, leftover Q̄ stubs/feedback wire fade with the gates; s2 0,0,1 held 0.7 s, serial brace/label beside D_in, Lecture 8 tag clears at {names}, FF names hidden during the latch what-if; s3 Q_0→Q_1 arrow fades at {q1known}; s4 Q_3 off before the GOLD 1 leaves, digits and "270 Ω" moved clear of wires; s5 DIM SIPO copy after the PISO tag, tags lifted, CLR pins/labels clear of the CLK bus, CLK trace labelled and the bus flashes per edge, one queue ring at a time; s6 digits bold 42, PRE/CLR words dropped, link inside the frame, an extra edge at {old} completes 1 1 0 (no lingering "?"); s7 dots/count/wave from one source, max 15 edges, T_c guides extended above the wave, chip lifted off the quote; s8 one-line captions, bigger slots, queue shows 1 1 0, bigger digits.
- Accepted (not real on frames, or by design): s1 "counter skips 2, 5, 7" (every state held 0.56 s; Gemini's 15 fps sampling; flagged again in both final reviews), s1 Q_2 "cut off" at 41 s (inside the frame); s2 "stray minus before D_in" at 29 s (frames clean); s2 faded RED cross lingering, s8 PINK arrowhead early (low, mid-transition); s4→s5 "IC labels linger" (gone by 0.4 s), s5 "1 1 0 duplicated" at 52.6 s (the last 1 entering the queue); s2 inset lingering to "Every flip-flop copies" (by design); s3 "FF1 = 1 at edge 8" (mid-run), "text cut off at 92 s" (0.7 inside); s4 "0 V" beside the last ground (design), IC label colours mid-appear, trace "CLK" label (fades with the trace), 270 Ω label stays while the resistor lifts out (the joke beat); s6 "D0 circled" (trail is FF2→FF2), "3 data wires → 1" until {usb}, balance tilt; s7 T_c on falling edges (measured: on the ▲ rising edges), dot-count claims (checked frame by frame twice); s8 "and faster bits" vs caption. Dwell advisories set by the narration's pace in every scene (biggest: s6 balance 2.5 s, s8 r6 caption 2.7 s, s5 "known start state" 1.7 s).
- Glitches (scene, time, what, cause):
  - s2 ~40.8 s: the 1 "vanishes" at the second quick edge. Real: 0,0,1 showed only 0.15 s before the third edge. Fixed (0.7 s hold).
  - s1 ~39 s: green stubs beside FF0/FF2. Real: Q̄ wires and labels faded during the flip-flops' slide into the chain, leaving ghosts. Fixed (fade with the gates first).
  - s4 ~55 s: lit Q_3 with a GOLD "1" already outside. Real mid-move: the LED faded over 20–55 % of the edge while the 1 faded in from 19 %. Fixed (1 appears after the LED is off).
  - s5 ~53 s: overlapping dashed rings spilling out of the queue box. Real: simultaneous flash rings on three digits 0.5 apart. Fixed (one tight ring at a time).
  - s6 ~30/34/46 s: receiver digits misread (0,0,? / 1,0,0). Mid-shift frames of tiny (size 30) digits; settled states were right. Fixed by size/weight.
  - s7 ~28–37 s: dots vs count vs cycles mismatch. Not reproduced in frames; contributing causes were an edge landing on the wave's cut end and 18 tiny cycles. Restructured (one edge list, no edge at the cut, 15 edges max).
  - s3 ~89 s, s4 ~29 s, s4 ~58 s: "duplicate label", "resistor missing", "stray CLK": not real (a label mid-fade-in; resistor back by 28.5 s; label fades with its trace).
- Engine note (from the s2 builder): `set_alpha(mobs, 1)` in engine/lib/kit.py can't restore a text set to 0 (it raises only the stroke); s2 works around it with per-name fill fades.

## Paused (producer, 2026-11-01 ~02:30) — resumed 2026-11-01 11:03; ch1 done since (see its section)
The user paused for the night (fan noise); both directors were stopped, and no studio processes are left.
- ch1: all 8 scenes built, two review rounds' fixes in; the round-2 holds looked right to the director,
  but its round-2 Gemini reviews were cut off. Open item it had noticed: s8's r6 recap caption
  ("…never outputs") sits at the very bottom edge. Resume: a chapter-director for ch1 to finish the
  review, then the final render and final reviews. Music done.
- ch2: narration fixes done (11 lines re-voiced, QA clean), music done, nothing built. Resume: a
  chapter-director for ch2 from the build. Its s1, s4 and s7 depend on ch1's helpers (end card, chip-number
  split, floating-input view): see ch1's section above, or scenes/ch1_*.
- Pass the producer notes again (they're in the previous section's spirit): assessed-work rules
  (PLAN.md do-not-say list; never probe pins 8/11 or show what the die displays); five-hole columns;
  "clock-to-output delay"; `vk voice --only` takes space-separated ids.
- After L7: DE L11 (paused before chapters, notes in its STATUS.md), then FoCS L5.
