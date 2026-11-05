# Digital Electronics (Cambridge CST Part IA, Prof. I. J. Wassell)

Material: `source/combined_26.pdf`, the slides for the whole course (190 pp., dated 23/08/2026).
Each recorded lecture comes as `source/lNN-lecture.mp4`, processed by `vk lecture` into
`.transcript.md`, `.digest.md` and `.captions.md`. Each lecture is its own project folder here,
`lNN-<slug>/`. Its title card is the lecture's title, under the course line
"Digital Electronics · Lecture N". No code is shown on screen. Truth tables and logic are checked
by enumeration in Python.

The course has 12 lectures (slides p. 2). The slides aren't split by lecture, and the lecturer
doesn't say the numbers, so numbers and page ranges are inferred from each recording. A lecture
can start or stop mid-section (L6 spans two).

| # | Lecture | Slides | Project | State |
|---|---|---|---|---|
| 1–4 | (combinational logic; not yet mapped) | pp. 1–77 | — | not started |
| 5 | Sequential logic intro, RS latch (inferred: L6 opens with its recap) | pp. 78–84 | — | not started |
| 6 | Flip-flops and Counters | pp. 85–101 | `l06-flip-flops-counters/` | ✅ done: 6 videos in `out/`, 61.3 min (2026-10-28) |
| 6 (Codex comparison) | Flip-flops and Counters | pp. 85–101 | `l06-flip-flops-counters-codex/` | done: 6 videos, 58.4 min, 1080p60; sampled comparison complete, mixed preferences (2026-10-30) |
| 6 (Astra chapter test) | Clocks and the transparent D latch | frozen Chapter 1 inputs | `l06-flip-flops-counters-astra-ch1/` | video complete and frozen: 9:12, 1080p60, Astra medium builder-only; blind comparison running (2026-10-30) |
| 7 | Hardware Labs and Shift Registers: the hardware-labs intro (with `source/Hardware_26.pdf`), then shift register, serial data link, system timing (recorded Wed 2026-10-21) | pp. 101–104 (p. 104's first slide only) | `l07-lab-shift-registers/` | ✅ done: 2 videos in `l07-lab-shift-registers/out/`, 22.2 min (2026-11-01) |
| 8 | Timing, Metastability and Parallelism (recorded Fri 2026-10-23) | pp. 104–119 | `l08-timing-metastability/` | ✅ done: 7 videos in `out/`, 62.6 min (2026-10-31) |
| 9 | Synchronous State Machines 1: FSM definitions, Moore and Mealy, state diagrams, the traffic-light controller, power-up and self-starting, Example 2 (inferred: Mon 2026-10-26, no recording here) | pp. 120–131 | — | no recording. L10 opens on p. 132's title and refers back to these slides, so L9 covered pp. 120–131. L10's ch1 s2–s3, ch3 s3 and ch4 s5 re-teach what L10 needs; the Mealy diagram and Example 2 aren't re-taught. As a project it would be one or two chapters from the slides |
| 10 | State Assignment ("Synchronous State Machines 2"; recorded Wed 2026-10-28) | pp. 132–143 | `l10-state-assignment/` | ✅ done: 6 videos in `out/`, 63.1 min, 1080p60 (2026-11-01) |
| 11 | State Minimisation, Programmable Logic and Circuits: redundant states (row matching, the implication table), GLA, GAL and FPGAs, then the start of the electronics section, up to Kirchhoff's voltage law (recorded Fri 2026-10-30) | pp. 144–170 | `l11-state-minimisation/` | ✅ done: 6 videos in `l11-state-minimisation/out/`, 62.0 min (2026-11-01) |
| 12 | (presumably the potential divider on, p. 170's last bullet: the rest of Underlying Concepts, then Transistors and Gates; not yet mapped) | pp. 170–190 | — | not started |

Slide sections, for mapping later lectures:

| Section | Pages |
|---|---|
| Introduction | 1–9 |
| Combinational Logic: Logic Gates and Boolean Algebra | 10–25 |
| Combinational Logic: Logic Minimisation | 26–44 |
| Combinational Logic: Binary Adders | 45–54 |
| Combinational Logic: Multilevel Logic and Hazards | 55–63 |
| Combinational Logic: Beyond Simple Logic Gates | 64–77 |
| Sequential Logic: Introduction, Latches and Flip-Flops | 78–91 |
| Sequential Logic: Flip-Flop Applications and Timing Considerations | 92–119 |
| Sequential Logic: Synchronous State Machines 1 | 120–131 |
| Sequential Logic: Synchronous State Machines 2 | 132–143 |
| Sequential Logic: Further Considerations | 144–162 |
| Electronics, Devices and Circuits: Underlying Concepts | 163–178 |
| Electronics, Devices and Circuits: Transistors and Gates | 179–190 |

Lecture numbers come from the dates. Lectures are Mon/Wed/Fri: L6 on Mon 2026-10-19 announces a
lecture on Wednesday, and the Friday 2026-10-23 recording refers back to shift-register slides
that aren't in L6. So the 10-23 recording is L8 (details in its PLAN.md Decisions). The Wed 10-21
recording confirms L7: it opens with the hardware-labs introduction L6 announced, and ends on
p. 104's first slide, where L8 picks up. The Wed 10-28
recording is L10: it opens on p. 132's title slide, refers back to L9's slides (the traffic light,
power-up in unused states, "at least log2 m … as we have seen"), and puts Boole's birthday (2 Nov)
"a few days" away (details in its PLAN.md Decisions).

Course-wide decisions:
- Same structure as FoCS: chapters of 8–11 min with recaps. Exercise hints and a bonus
  solutions chapter are added only where the slides have exercises (L6's don't).
- Notation as on the slides: Q′ is the next state, an overbar is the complement. Signal colours
  are set in L6 ch1: CLK YELLOW, inputs BLUE, outputs GREEN, Q_int TEAL, asynchronous inputs and
  errors RED. Later lectures keep them, along with L6's timing-diagram and flip-flop-symbol
  styles.
- Later lectures may assume the earlier ones were watched.
- Voice, as learned in L6 (details in docs/LESSONS.md): spell letters out ("cue", "dee", "ess",
  "jay-kay", "kay-map"); say "reset-set latch", not "ar-ess"; "every edge of the clock", not a bare
  "clock" in a short phrase (heard as "quack"). Gemini hears "ex-or" as "axer" (Whisper doesn't);
  L6 accepted it. Consider "exclusive-or" at first use in later lectures.
  L8 added: write the letter K as a capital "K" ("kay" came out "chi"/"kai" even after rewording,
  like the N rule); say "clock-to-output", not "clock-to-cue" (heard "cock-to-Q"); avoid "a slower clock"
  ("quack") and "launches" ("wauches"); say "David and Sarah Harris", not "Harris and Harris".
  L10 added: write the letter A as a capital "A" too: "ay" came out "eye" or "uh" (Gemini and
  Whisper both heard it; L10 ch2 re-listened clean with "A"). Mid-sentence, "A" can still be
  read as the article "uh" (L10 ch1 twice): put it right after a noun ("flip-flop A", "state A") or
  at the end of a phrase, never before another word that makes it look like "a".
  Same for a letter with a subscript: "S zero", "S one" (capital), not "ess zero" (heard "ess ess
  zero" six times in L10 ch6; clean as "S zero" in ch5 and ch6).
  L11 added: the same for every state letter after a noun ("state H", "state L", "state G"):
  "aitch", "ell" and "gee" were misheard there. Write letters as capitals, always after a word.
  Acronyms said as words are written as words: "Gal"/"Gals" (written "GAL", it was spelled out
  G-A-L in L11 ch4), and the same would go for "Pal". Spelled acronyms keep their hyphens
  ("F-P-G-A", "P-L-A").
- Timing notation and colours (from L8): T_c, t_su, t_hold, t_pc, t_pd, t_skew as on the slides,
  with data-sheet-style timing diagrams. Delays t_pc PINK and t_pd PURPLE; the set-up/hold window
  GOLD; t_skew TEAL. L8's PLAN.md has the full list.
- State machines (from L10): state diagrams as on the slides (circles with [codes], arcs labelled
  with input conditions); external inputs BLUE, state bits GREEN, D inputs BLUE, unused states
  DIM, the travelling 1 of shift-register designs GOLD, K-map loops PINK/PURPLE/TEAL; letters
  always after a word ("flip-flop ay", "input ee"). L10's PLAN.md has the full list.
- Reusable drawings: L6's STATUS.md lists each chapter's helpers (gates, latches, flip-flop box,
  J-K symbol, clock wave, timing diagram, counters, `mod_table()`, `kmap()`, `sync_counter()`).
