# Load calibration: how fast new material may arrive (2026-11-04)

Why: the user wants an equalizer for the rate at which material arrives. DE L10 and the deep pendulum
pilot feel right; old-style NST Maths L10, "the pendulum with tons of jumps" and L11's cosh feel too
dense. This finds the measured load per minute that separates the two, for sizing and checking chapters.

**Headline.** The measure is **holds per minute, H**: formulas plus definitions *new to this viewer*
(the study's F and D, `+` only). Comfortable chapters run **1.35–1.87**, dense ones **2.05–3.57**.
Credit each question to the viewer and the gap triples: **H − Q** is 0.76–1.17 vs 1.71–3.10. Ideas per
minute, new ideas per minute, words per idea and jumps do **not** separate. DE packs as many claims per
minute as old L10, but a claim about what you're watching is cheap; a new symbol or term is not. Jumps
are rare everywhere (≤ 2 per chapter). L10 ch6's "tons of jumps" is a new formula or term every 17 s,
with few questions; the comfortable chapters give 32–44 s each. **Small sample:** 8 rated chapters,
~40 measures tried, and the groups also differ by subject and style, so this is a calibrated
hypothesis. L12 ch1 is its first test (§3).

## 1. Method
- **Chapters.** Felt right: DE L10 ch2 (sliding, ring) and ch4 (one-hot); the pilot
  `nst-maths/l10-deep-oscillations` ch1–2. Too dense: Maths L10 ch2 (De Moivre), ch4 (log) and ch6
  (oscillations, taken to be "the pendulum with tons of jumps": the only other pendulum, which "took
  ω = √(g/l) as given"), and L11 ch1 (cosh, sinh). Not rated: L12 ch1 (classic-style maths), as a prediction.
- **Timing.** One line per sentence, timed from `audio/manifest.json` word times + `media/cues/` clip
  starts + rendered scene lengths (they sum to `out/`'s length within 0.1 s), at house pacing as in
  `out/`. The house pauses add 14–21% to every chapter (vs `audio/.pre-regap`), nearly uniformly, so
  ranks don't move. Maths L10 was judged at its old pacing, ~17% denser per minute than shown: it only widens the gap.
- **Rubric.** The study's (`docs/3b1b-study.md` §1), **verbatim**: the original coder's prompt was
  recovered from its session log. F new formula or derivation line, D definition, C claim,
  R restatement, M motive, Q question to the viewer; ideas = F + D + C. Coded per sentence, not per minute.
- **Novelty (new).** Each F/D/C is `+` (new to this viewer) or `k` (they had it before this video).
  The viewer: A-level Maths without Further Maths (so cosh is `+`), GCSE physics, the lectures named in
  PLAN.md's Audience paragraph, and the project's earlier chapters.
- **Jumps (new).** `s`: a step of ≥ 2 unseen operations, or a derivable result asserted and then built
  on ("take as given" counts). `m`: a move the viewer couldn't predict, with no reason for *this* move
  within ±3 sentences. At most one per sentence.
- **Coders.** Six Sonnet coders with 3 chapters each, so every chapter was coded twice. Each coder had
  both groups and didn't know the grouping, plus 23 anchor sentences that I coded. Their jumps were
  mostly my anchors played back, so one blind Opus auditor re-coded jumps with invented anchors. It
  still saw mine in BRIEF.md and departed from one; all 5 of its jumps are anchor sentences.
- **Agreement.** F totals match the original coder within 6% on L10 ch2/4/6 (L12 ch1 +43%). C, R and M
  don't: these coders find 1.1–1.5× (mean 1.3×) the original's ideas, more C and less R. So ideas/min
  here run ~1.3× the study's scale; F/min is on its scale. On H, two coders of one chapter differ by 0.22/min on average.
- **Statistics.** 2-min windows sliding in 5 s steps, each unit at its sentence's start (peak = densest
  window). AUC over the 16 comfortable/dense pairs (1 = every dense chapter above every comfortable one);
  gap = lowest dense − highest comfortable; robustness over all 256 picks of one coder per chapter, and
  leave-one-out (threshold from the other 7).

## 2. Per chapter: mean per minute (densest 2-min window)
| chapter | felt | min | ideas | new ideas | new formulas F | F new to viewer F+ | **holds H = F+ + D+** | jumps | Q | **H − Q** | words / idea |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DE L10 ch2 sliding, ring | right | 11.3 | 6.0 (9.5) | 5.0 (9.0) | 1.55 (4.0) | 1.55 (4.0) | **1.73** (4.0) | 0 | 0.58 | **1.15** (3.5) | 23 (15) |
| DE L10 ch4 one-hot | right | 11.5 | 6.5 (10.2) | 4.2 (8.5) | 1.22 (5.0) | 1.09 (5.0) | **1.35** (5.0) | 0 | 0.26 | **1.09** (5.0) | 22 (15) |
| pilot ch1 the rule | right | 15.0 | 5.2 (8.0) | 3.9 (6.5) | 1.63 (3.5) | 1.20 (3.0) | **1.87** (3.8) | 0.07 (0.5) | 0.70 | **1.17** (3.2) | 24 (16) |
| pilot ch2 shadows | right | 17.2 | 5.8 (8.0) | 4.6 (7.0) | 2.03 (4.0) | 1.69 (3.5) | **1.77** (3.5) | 0 | 1.02 | **0.76** (2.8) | 21 (16) |
| L10 ch2 De Moivre | dense | 11.9 | 5.1 (7.5) | 3.4 (6.0) | 2.78 (6.5) | 2.06 (5.5) | **2.23** (5.5) | 0 | 0.17 | **2.06** (5.5) | 26 (17) |
| L10 ch4 logarithm | dense | 11.7 | 6.7 (9.2) | 5.3 (8.8) | 1.84 (4.0) | 1.45 (3.5) | **2.05** (4.2) | 0 | 0.34 | **1.71** (4.2) | 20 (15) |
| L10 ch6 oscillations | dense | 10.6 | 6.8 (10.2) | 6.1 (9.0) | 3.01 (6.2) | 2.87 (6.0) | **3.48** (6.0) | 0.19 (1.0) | 0.38 | **3.10** (6.0) | 20 (13) |
| L11 ch1 cosh, sinh | dense | 11.8 | 6.9 (9.8) | 5.6 (7.8) | 3.61 (6.5) | 2.89 (5.8) | **3.57** (6.8) | 0.17 (0.5) | 0.51 | **3.06** (6.8) | 18 (13) |
| L12 ch1 first principles | not rated | 12.8 | 6.1 (9.5) | 4.1 (8.5) | 1.56 (3.5) | 0.74 (2.5) | **1.45** (3.2) | 0 | 0.47 | **0.98** (2.5) | 20 (13) |
| 3b1b, 8 videos (study) | – | 4–31 | 2.4–4.4 (×1.3 here) | – | 0.7–1.55 | – | F + D 0.9–2.1 | – | 0.35–0.73 | – | 39–69 (÷1.3 here) |

Q leaves out "Pause the video if you want longer" lines (else a think stop counts twice). Words per
idea: the peak is the lowest window. Jumps (Opus audit): pilot ch1 S050 (ω², reason deferred); L10 ch6
S014 (ω = √(g/L) "as given") and S018 (x = a cos ωt + b sin ωt never derived); L11 ch1 S004 ("lift out
every i") and S070 (z = ix, "the trick from the notes"). DE ch4's 5.0 peak is the one-hot ring ("in the
same way, green takes its input from…": one rule, four lines).

## 3. What separates the groups
| measure | felt right | too dense | AUC | gap | 256 coder picks / LOO |
|---|---|---|---|---|---|
| ideas/min | 5.2–6.5 | 5.1–6.9 | 0.75 | −1.4 | no |
| new-to-viewer ideas/min | 3.9–5.1 | 3.4–6.1 | 0.75 | −1.7 | no |
| jumps/min (audit) | 0–0.07 | 0–0.19 | 0.69 | – | no |
| questions/min (fewer = denser) | 0.26–1.02 | 0.17–0.51 | 0.81 | – | no |
| new formulas F/min | 1.22–2.03 | 1.84–3.61 | 0.94 | −0.20 | 25% of picks, LOO 6/8 |
| **H = F+ + D+ /min** | 1.35–1.87 | 2.05–3.57 | **1.00** | **+0.19** | **256/256, 8/8** |
| H per 100 words (pacing-free) | 0.96–1.47 | 1.50–2.82 | 1.00 | +0.04 | 128/256, 7/8 |
| H, densest 2 min | 3.5–5.0 | 4.2–6.8 | 0.94 | −0.8 | no |
| **H − Q /min** | 0.76–1.17 | 1.71–3.10 | **1.00** | **+0.54** | **256/256, 8/8** |

1. **Count what the viewer must hold, not what is said.** DE asserts as much per minute as old L10
   (state codes sliding, wires matching columns), but each claim is about something on screen and is
   checked as it's said. Symbols and named terms must be carried. F alone nearly separates; adding new
   definitions (L10 ch4's log, principal value, ladder) completes it. Known items (`k`: F = ma, Hooke,
   arc length, last lecture's cos θ) cost little: the pilot's ch1 has 7–8 of them. Words per idea
   (21–24 vs 18–26) doesn't separate.
2. **Questions buy room.** The comfortable chapters ask 0.3–1.0 questions a minute, against 0.2–0.5.
   One unit of credit per question is the simplest weight, and H − Q is the most robust measure here. It
   explains why pilot ch2 (the most formulas of the four, F 2.03) felt easy: a question a minute.
3. **Jumps, as defined, are not the lever.** Writers check every step, so failures of atomicity are
   rare (two coding passes, a blind audit: ≤ 2 per chapter, 0 in two of the four dense ones). The felt
   "jumps" are steps arriving faster than they're absorbed. L10 ch6's two real ones (ω = √(g/L) as
   given, a cos + b sin never derived) are its foundations. A count can't weigh that; the
   physics-first rule (DEEP_STYLE §10) does.
4. **Peaks add nothing here.** Every dense chapter's mean is already over the line. Each dense chapter
   has a 2-min stretch at 4.2–6.8/min, and no comfortable one passes 4.0 except DE ch4's patterned list.
5. **3b1b sits in the comfortable band.** Its F + D (nearly all new to its audience) is 0.9–2.1/min,
   median 1.3. Our dense chapters are at or above its maximum (la3, 2.1).
6. **Confounds, and the test.** Comfortable = DE + the deep pilot, dense = classic maths: subject and
   style line up with the groups, and the pilot re-taught L10 ch6, which the user had seen. L12 ch1 is
   classic-style maths at H 1.45 and H − Q 0.98, so the measure predicts *comfortable*. If the user finds
   it dense, the measure is wrong, or style and subject explain the split instead.

## 4. The equalizer
**Unit: one hold** = a formula line or a named term/notation this viewer meets for the first time
(F+ or D+). Not holds: recalls (`k`), restatements, claims about what is on screen. **Credit:** a
question to the viewer (an answered prediction or a think stop; "pause the video" lines don't count).

| | chapter mean (house pacing) | any 2-min window |
|---|---|---|
| target band | H 1.3–1.8 /min and H − Q 0.7–1.2 /min | – |
| limit | H ≤ 1.9 and H − Q ≤ 1.4 | H ≤ 4.0 /min (≤ 8 holds in 2 min); lines from one stated pattern count once |

The floor is unmeasured (nothing here felt too slow): don't pad below ~1.2. Keep both limits: H − Q alone
would pass four formulas a minute with three questions, which is outside these data.

**Sizing (planner).** List the holds each chapter must carry: every formula line and new term its
scenes will put up, after DEEP_STYLE §1's deep/reference tiering (reference lines on screen count too).
Then **minutes ≈ holds / 1.6**, with ≥ 1 question per 2 minutes: 16–18 holds and 5+ questions for a
10-min chapter. A chapter over ~20 holds is split, or its routine lines move to the solutions chapter.
Checks: the pilot's ch1–2 carried 58 holds in 32 min (1.8/min). Old L10 ch6 carried 37 in 10.6 min,
which at 1.6/min is 23 min, i.e. two chapters. That's consistent with the study's ~1.5× for full L10 coverage (finding 12).

**Checking a script before voicing (writer, or a tool).**
1. Time each sentence at **130 words per minute of finished video** (house pacing; 122–141 measured
   over these nine), plus ~8 s per think stop.
2. Code F/D with `+`/`k` and Q per sentence: one Sonnet pass with the saved rubric (Files), ~30k tokens
   and ~2 min per chapter.
3. Compute H, H − Q and the 2-min windows. Flag a chapter outside the band, and every window over
   8 holds, with its sentence numbers.
4. Fix, in this order: turn a step into a question (predict, then show); swap a new symbol for a recall
   or a picture the viewer has; move routine lines to the reference tier; split the scene. Never fix by
   adding silence.
5. After voicing, re-run on the manifest timings (as here) and log H in STATUS.md, so the band can be
   re-fitted as the user rates more chapters.

This could become `vk load N` (an engine change, the producer's or user's call). Until then the
script-writer can count holds by hand from its visual briefs, which already list every formula.

## 5. Limits
- 8 rated chapters (4 + 4), ~40 measures and weights tried. For one fixed measure, a perfect 4/4 split by
  chance has p = 1/70, so some of this may be luck. H and H − Q were natural candidates (the rubric's own
  "must hold" items, unit weights) and survive every coder pick and leave-one-out, but H's gap (0.19)
  is about one coder's noise (0.22).
- The ratings are impressions of whole lectures, mapped to chapters by us: L11 ch1 was named, and the L10
  chapters inherit L10's verdict. Not captured: abstract vs concrete claims, how much a picture carries,
  motive. These coders' M put *more* motive per idea in the dense chapters, and their M disagrees with the original coder's.
- Next ratings worth getting: L12 ch1 (the prediction), and a chapter built to H ≈ 1.6 with few
  questions, to test whether Q's credit is real.

Files (gitignored): `engine/reference/3b1b/study/load/`: `BRIEF.md` (rubric + anchors), `JUMPS.md`, `tx/`, `codes/`, `tools/`.
