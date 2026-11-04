# 3Blue1Brown vs our videos: a measured study (2026-11-04)

Why: the user found NST Maths L10 far too dense ("a series of arbitrary manipulations"). 8 3b1b videos
and 4 of ours, measured the same way, to test `docs/DEEP_STYLE.md` (pacing, structure, pedagogy; code
idioms are in `PATTERNS.md`). Tools, numbers (`data/final.json`) and contact sheets are in
`engine/reference/3b1b/study/` (gitignored); the videos and subtitles were deleted after measuring.

**Headline.** 3b1b is not slower than us. It speaks *more* words per minute of video and leaves fewer
silences. The difference is what the words carry: half as many new formulas per minute, twice the words
per idea, three times as many sentences of motive, a picture that stays on screen and keeps moving
while the formula is written as its caption, and a viewer who is addressed and asked things. Its
slowness comes from redundancy and motion, not from silence.

## 1. Method

**Corpus.** 3b1b, with English captions (maths written as spoken): `la3` Linear transformations and
matrices (2016); `calc2` The paradox of the derivative, `calc3` Derivative formulas through geometry,
`calc5` What's so special about Euler's number e? (2017); `eipi` e^(iπ) in 3.14 minutes, `de1`
Differential equations, a tourist's guide, `de4` But what is a Fourier series? (2019); `clt` But what
is the Central Limit Theorem? (2023; the only 2022+ one). **Ours:** L10 `ch2_de_moivre`,
`ch4_logarithm`, `ch6_oscillations` as now in `out/` (re-paced 2026-11-03) and L12
`ch1_first_principles`. L10's original fixed pacing is reconstructed from `audio/.pre-regap/` (same
words; each scene shorter by its clips' change in length, assuming unchanged visual waits).

**Speech.** Band-pass 150–4000 Hz, 20 ms RMS; voiced = within 20 dB of the file's 95th-percentile level
(a per-file `silencedetect` floor); gaps < 0.3 s count as speech; frames outside the narration (3b1b:
caption cues ± 0.3 s; ours: clips placed from `media/cues/` + `audio/manifest.json`) are silent, so music
alone never counts. *Calibration:* our clean per-clip wavs are a music-free truth; 20 dB on the mixed
track matched it best (ch2: no speech 38.8% vs 37.6%, gaps ≥ 1 s 10.45 vs 10.40/min); 25 dB missed ~20%
of gaps ≥ 2 s under music. *Cross-check:* gaps between word start times minus 0.3 s per word (3b1b:
YouTube's word-timed captions, la3 and calc2–5 only; ours: the manifest) agree within ~15%. de1 and de4
have music under the voice: their gaps are ±25%. Words: one regex on both sides.

**Visual change.** 2 fps, 256×144 grey; content = pixels > 40 levels off the frame median. *Reset*: ≥ 60%
of what was on screen 1 s earlier is gone, on a 10×6 grid of cells (motion within a cell doesn't count),
and still gone 2 s later; ≥ 3 s apart. Checked by eye on frame strips around each reset (ours kept:
`sheets/_check_l10ch2_resets.png`): all of ch2's are real clears; ~4 of 16 in de4 are camera
moves, so 3b1b's rate is up to ~20% high. *Still*: < 0.2% of pixels change in 0.5 s; *still while
speaking*: share of voiced samples that are still; *motion*: share of samples with > 5% changing.

**Density.** Contact sheets, a frame every 10 s (`sheets/<key>_NN.png`), coded by two Sonnet coders
(each 4 3b1b + 2 ours, one rubric): formula lines (a matrix = 1; lone labels on a diagram don't count),
prose lines, pictures, a category, and each line's lifetime. My re-read of de1 05:05–09:55 matched
within ±1 line per frame; our ch2 and de4 (small type) are the roughest.

**Ideas.** One Opus coder, all 12 transcripts, per sentence: F (a new formula or derivation line),
D (definition), C (new claim), R (restatement), M (motive: a step's goal or reason), Q (question to the
viewer); ideas = F + D + C. Calibrated on calc2 and our ch2; my re-code of ch2 min 1 matched within ±1
per code; its own estimate is ±15%.

**Code.** Static `ast` counts, and how equations step in calc2 (`_2017/eoc/chapter2.py` TCubedExample),
de1 (`_2019/diffyq/part1/pendulum.py` BuildUpEquation) and de4 (`part4/staging.py` SwapIntegralAndSum).

## 2. Metrics (per minute of running time)

| video | min | wpm | no speech | gaps ≥1/≥2/≥4 s per min | resets /min | still while speaking | motion | formula lines /frame | frames: picture / maths only | new formulas /min | ideas /min | words /idea | motive /idea | questions /min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| la3 (2016) | 11.0 | 167 | 23% | 3.5 / 0.9 / 0.00 | 1.9 | 56% | 21% | 1.2 | 74% / 17% | 1.5 | 3.0 | 56 | 0.36 | 0.73 |
| calc2 (2017) | 16.8 | 174 | 23% | 3.7 / 0.8 / 0.18 | 1.9 | 60% | 3% | 1.1 | 84% / 3% | 0.8 | 2.6 | 68 | 0.28 | 0.71 |
| calc3 (2017) | 17.6 | 178 | 24% | 4.5 / 0.7 / 0.18 | 1.5 | 62% | 4% | 2.3 | 76% / 14% | 1.0 | 2.8 | 62 | 0.30 | 0.68 |
| calc5 (2017) | 13.8 | 158 | 27% | 3.9 / 0.7 / 0.15 | 2.4 | 62% | 3% | 2.3 | 42% / 27% | 1.1 | 2.4 | 66 | 0.30 | 0.51 |
| eipi (2019) | 4.1 | 170 | 22% | 1.8 / 1.1 / 0.53 | 1.7 | 34% | 4% | 1.7 | 72% / 0% | 1.5 | 4.4 | 39 | 0.11 | 0.73 |
| de1 (2019) | 27.3 | 168 | 21% | 2.7 / 0.8 / 0.07 | 1.9 | 34% | 13% | 1.2 | 81% / 4% | 0.7 | 4.0 | 42 | 0.15 | 0.44 |
| de4 (2019) | 24.8 | 179 | 22% | 2.5 / 1.0 / 0.33 | 2.1 | 30% | 6% | 1.3 | 90% / 2% | 0.7 | 2.6 | 69 | 0.27 | 0.52 |
| clt (2023) | 31.2 | 201 | 20% | 1.9 / 0.7 / 0.16 | 2.1 | 40% | 9% | 1.7 | 84% / 0% | 0.8 | 3.1 | 65 | 0.22 | 0.35 |
| **3b1b 2016–17** | 14.8 | 169 | 24% | 3.9 / 0.8 / 0.13 | 1.9 | 60% | 8% | 1.7 | 69% / 15% | 1.1 | 2.7 | 63 | 0.31 | 0.66 |
| **3b1b 2019+** | 21.9 | 180 | 21% | 2.2 / 0.9 / 0.27 | 1.9 | 35% | 8% | 1.5 | 82% / 2% | 0.9 | 3.5 | 54 | 0.19 | 0.51 |
| **3b1b, all 8** | 18.3 | 174 | 23% | 3.1 / 0.8 / 0.20 | 1.9 | 47% | 8% | 1.6 | 76% / 8% | 1.0 | 3.1 | 58 | 0.25 | 0.58 |
| L10 ch2 | 11.9 | 131 | 39% | 10.5 / 3.4 / 0.34 | 1.8 | 66% | 1% | 3.3 | 61% / 35% | 2.9 | 4.6 | 28 | 0.13 | 0.17 |
| L10 ch4 | 11.7 | 137 | 40% | 11.5 / 3.9 / 0.26 | 1.5 | 72% | 1% | 1.6 | 70% / 15% | 1.8 | 4.5 | 30 | 0.08 | 0.43 |
| L10 ch6 | 10.6 | 138 | 37% | 10.7 / 3.3 / 0.19 | 1.3 | 39% | 0% | 2.0 | 83% / 16% | 2.9 | 5.6 | 24 | 0.05 | 0.47 |
| L12 ch1 | 12.8 | 122 | 45% | 12.5 / 3.6 / 0.08 | 1.6 | 69% | 1% | 2.4 | 66% / 27% | 1.1 | 4.4 | 28 | 0.07 | 0.47 |
| **ours, all 4** | 11.8 | 132 | 40% | 11.3 / 3.6 / 0.22 | 1.5 | 62% | 1% | 2.3 | 70% / 23% | 2.2 | 4.8 | 28 | 0.08 | 0.38 |
| L10 ch2/4/6, original pacing* | 9.9 | 156 | 28% | 4.0 / 1.0 / 0.17 | | | | | | | | | | |

*From the clean wavs (on ch2 now, that method reads 37.6% no speech vs the table's 38.8%).
Not in the table: words per minute *while voiced* are alike (232 vs 224). The median time between
resets is 21 vs 28 s. A formula line stays visible 31 vs 32 s on average (median 20 s on both sides,
10 s resolution). Frames with ≥ 4 formula lines: 9% vs 21% (ch2 33%, up to 13 lines). New formula
lines on screen per minute: 3.1 vs 4.8.

## 3. Findings

1. **Silence isn't the lever.** 3b1b runs 174 words per minute of video against our 132, with 3.1 gaps
   ≥ 1 s per minute against our 11.3, and no speech 23% of the time against our 40%. L10 at its
   *original* pacing sat at the edge of 3b1b's range on every speech measure (156 wpm vs 158–201; 28%
   vs 20–27%; gaps ≥ 1/≥ 2 s 4.0/1.0 vs 1.8–4.5/0.7–1.1), and the user still found it too dense.
   The re-pacing gave 3.6× 3b1b's gaps ≥ 1 s.
2. **We pack 1.5× the ideas and 2.2× the formulas.** Ideas 4.8 vs 3.1/min; new formulas 2.2 vs 1.0/min
   (ch2 and ch6: 2.9). 3b1b holds ~1 new formula per minute in every era (0.7–1.5); its claims vary more
   (de1, a survey, reaches 4.0 ideas/min). Per idea 3b1b spends 58 words and 20 s; we spend 28 and 12.6.
3. **We don't lack restatement; we lack motive and questions.** Restatements per idea are equal (0.55 vs
   0.50), but ours bunch in the recap (22–41% of them in the last 2 min; 3b1b < 20% in 5 of 8, since
   it restates as it goes). Motive per idea: 0.25 vs 0.08; questions per idea ~0.17 vs 0.08. 3b1b says
   why the next step is coming before it comes. "You/your": 2.1 vs 0.7 per 100 words; "think" is in
   every 3b1b video (0.2–0.8 per 100 words) and in none of ours.
4. **Picture first, formula as its caption, derivation beside it.** la3 moves the plane (01:11–03:23)
   long before any matrix (06:18). calc2 graphs the car (01:23) before ds/dt (05:13). clt simulates for
   15 min before its formula (15:57). calc3 reads each rule off a picture (square 02:34 → 2x at 04:07;
   unit-circle walker 15:01 → cos θ 16:21); the graph only gives the rough shape: "thinking in terms of
   the graph would never have landed us on the precise quantity" (06:42). de4 10:15 writes 2cos x =
   e^{ix} + e^{−ix} as the caption of two counter-rotating arrows and never derives it. Where there is no
   picture, it says so: calc5 03:39 uses numbers instead (picture in 42% of frames, the lowest). Ours:
   ch2 does the algebra at 09:19 and the picture at 09:54; ch6 shows the shadow first (02:13) but takes
   the physics as given (01:20).
5. **3b1b keeps the picture, not the derivation.** Maths-only frames 8% vs 23% (2019+: 2%); formula
   lines per frame 1.6 vs 2.3. Formulas live ~30 s on both sides, so 3b1b doesn't stack long
   derivations (de1's code stacks ~3 lines and fades the old ones to 0.5), but de1's pendulum diagram
   stays ~100 s (07:05–08:45) while the equation is built beside it. Resets come at about the same
   rate (1.9 vs 1.5/min): our clears aren't the problem.
6. **3b1b's frame keeps moving.** Still while speaking 47% vs 62% (2019+: 35%); in motion 8% vs 1% of
   the time. Parameters sweep with live readouts (de4 13:05 e^{it} ≈ +0.55 + 0.83i, ticking; de1 08:15
   sin(1°) = 0.017). Our ch6, with its turning arrow, is the one chapter in 3b1b's range (39%). By static
   count our scenes have *more* plays per minute (~19 vs 11–14): many short writes, then a still hold.
7. **Engagement is questions, not holds.** Explicit "pause and ponder": 0–3 per video, then only
   1.0–4.9 s of silence (median 2.6 s, n = 9); the pause is the viewer's button (calc2 15:12 "Really,
   pause and ponder that for a moment. Is the car moving at t = 0?", then 4.9 s). Narrated questions:
   0.58 vs 0.38/min.
8. **Moves are named in words, as mechanisms, with the why.** calc5 04:21 "that really is the most
   important property of exponents", then why: it lets you "relate additive ideas … to multiplicative
   ideas"; 08:59 "The key is to use the chain rule"; de4 18:48 "here's the actual clever part"; calc2
   14:13 "the heart of why calculus becomes useful". 1–5 per video; ours 0–1 per chapter.
9. **Step size.** The code does one rewrite per play: calc2 fades in the t³ expansion term by term with
   a wait after each, then cancels 2³, then dt; de1 moves Lθ̈ across, then divides by L. A concrete
   number comes before the letter (t = 2 then t, calc2 10:38–13:04; v = (−1, 2), then (x, y), then
   (a, b, c, d), la3 03:57–07:28). Skips are flagged ("a little geometry exercise for you", de1 07:25;
   "sweeping under the rug", de4 08:53; exercises, calc3 12:04, de4 23:19). Never skipped: what a step
   means, the sign convention (de1 07:46), the gut check (de1 08:07).
10. **Openings and endings.** 3b1b opens on the phenomenon or the puzzle (de4 shows the finished drawing,
    "linger", 00:31; clt the Galton board; calc2 "an oxymoron", 00:35). Ours open "Last time…" (ch2,
    ch4, ch6) and cite the notes, equation numbers or the lecturer in 5–12 sentences per chapter (3b1b:
    none). 3b1b ends on a forward link or one reframing; only la3 has a "to sum up" (09:44).
11. **2016–17 vs 2019+** (one 2022+ video, so indicative): fewer gaps ≥ 1 s (2.2 vs 3.9/min), much more
    motion while speaking (still 35% vs 60%), almost no maths-only frames (2% vs 15%), more claims per
    minute, and the same ~1 new formula per minute.
12. **The tension.** 3b1b gets its rate by choosing. de1 (27 min) sets up one ODE and never solves it
    analytically; de4 (25 min) derives one formula, c_n, and leaves the step-function integral and the
    real-form series as exercises; the rigour (convergence, discontinuities) goes under the rug. There
    are no exam-style worked examples, no drill and few recaps: one strong picture per idea. At 3.1
    ideas/min, L10's ~470 idea units (4.9/min × 95.5 min, extrapolated from 3 chapters) would take
    ~2.5 h instead of 1.6. Full coverage at full depth isn't possible, so depth must be rationed (rule 1).

## 4. Intuition patterns

What 3b1b does (timestamp), then the L10 application. P1–P3 and P6–P8 are for the SHM pilot.

**P1. Physics in words, then one symbol per fact, beside a diagram that stays.** de1 02:26 "unpack what
that's really saying": the velocity vectors gain 9.8 m/s downward each second, so ÿ = −g. The pendulum
(07:05–08:45): the diagram stays while the arc x = Lθ is drawn, gravity is split into components (the
angle is "a little geometry exercise for you"), −g sin θ is written beside its arrow, then Lθ̈ = −g sin θ,
then damping "maybe … proportional to the velocity" (08:36). *SHM:* a bob on a spring (or a small-angle
pendulum) with a restoring-force arrow that grows live as it's pulled out ("pulled back harder the
further out"); F = −kx arrives as that arrow's caption, then a = −(k/m)x, ω² = k/m "the pull per unit
stretch". Not ch6's "ω = √(g/L) … We'll take that as given" (01:09–01:22).

**P2. Gut-check the equation at its extremes, numbers on screen.** de1 08:07–08:25: θ = 0 gives no
acceleration, θ = 90° free fall; frames show "sin(1°) = 0.017", "sin(64°) = 0.899". *SHM:* x'' = −ω²x at
x = 0 (no pull, fastest) and at the turning point (strongest pull, momentarily still). Small angles:
sin 0.1 = 0.0998, so sin θ ≈ θ; at 60°, 0.866 vs 1.047, which is why a real pendulum's period grows (de1
06:35–06:55 shows the real swing leaving the cosine).

**P3. The rule draws the motion; read the solution off it.** eipi 00:17–03:17: velocity = position
means runaway growth; 2× and −0.5× position next; then velocity = i × position, a 90° turn, so the only
path from 1 is the unit circle at speed 1, and e^{iπ} = −1 is read off. *SHM:* state "acceleration =
−ω² × position" and ask which motion obeys it. A point turning at rate ω has velocity iω × position (a
quarter turn ahead) and acceleration (iω)² × position = −ω² × position: the turning arrow solves SHM
before any formula, and the pendulum is its shadow. Our ch6 runs it backwards (06:16: the acceleration
arrow last, "that's the equation of simple harmonic motion").

**P4. One knob: familiar values first, then the strange one.** eipi 00:59–02:01: e^{t}, e^{2t},
e^{−0.5t}, then e^{it}; calc5 05:14–07:22: bases 2, 3, 8 give 0.6931, 1.0986, 2.079. *L10:* x' = kx for
k = 1, −1, then iω (growth, decay, turning); for z^w: 2^1, 2^{1/2}, then 2^i.

**P5. Mystery numbers, then the move that explains them.** calc5 05:14–10:43: 0.6931 for base 2 and
2.079 = 3 × 0.6931 for base 8; "what does 2 have to do with 0.6931?"; then "2 = e^{ln 2}", "nothing
fancy". *Powers (ch5):* i^i on a calculator is 0.2079, real; its other values e^{−π/2−2πn} are 111.3,
0.00039, …; then the move "rewrite the base as a power of e" (DEEP_STYLE §2) explains them all.

**P6. A real oscillation is a mirror pair of turning arrows; the formula is the caption.** de4 10:15:
two arrows turn opposite ways, their sum rides the real axis, captioned "Sum of rotations: 2cos(x) =
e^{ix} + e^{−ix}", never derived (it's the 23:19 exercise); 11:25–12:19: frequencies ±1 are "horizontal
reflections … that sum stays fixed on the real number line, and it oscillates like a sine wave". *De
Moivre (77) and SHM:* Re[A e^{iωt}] = ½(A e^{iωt} + Ā e^{−iωt}): show the conjugate arrow turning back,
and "take the real part" is half their sum. The user's favourite L10 picture, order reversed.

**P7. Output alone first, then unroll it into a graph.** de4 11:46: "we're used to looking at its graph
rather than the output alone wandering on the real number line"; calc3 12:55–13:33: sine as the height
of a walker on the unit circle, then the wave. *SHM:* the bob on a line and the arrow's shadow on the
same line (one dot, two causes), then a time axis unrolls the wave. Ch6 02:13 has the shadow; put the
bob on that axis.

**P8. Make the moving thing hold still.** de4 18:56–20:23: "the trick is to first multiply f of t by
something that makes that vector hold still" (a smartphone for an overactive child); averaging kills
every arrow still moving; 20:10 reads the formula back in those words. *Complex amplitude, impedance
(ch6–7):* multiply by e^{−iωt}, i.e. ride along, and the arrow stops: A is the frozen arrow. In the
turning frame every current and voltage is a fixed arrow, so calculus becomes algebra.

**P9. Say the tempting wrong thing, then break it on screen.** calc5 02:21: it's "tempting to say" the
derivative of 2^t equals itself, "but it's not quite correct"; de1 06:22 calls the textbook pendulum
formulas "lies" as the real swing leaves the cosine; la3 02:50–03:16: three transformations that look
linear and aren't. *Logs (ch4):* ln(z₁z₂) = ln z₁ + ln z₂ with principal values, z₁ = z₂ = −1: 0 vs 2πi.
*SHM:* "the period doesn't depend on the amplitude": true for SHM, false for a real pendulum.

**P10. Build a formula from its requirements, one piece each.** clt 16:01–19:02: e^{x} grows, e^{−x}
decays, e^{−|x|} has a corner (rejected), e^{−x²} is smooth, a constant sets the width, √π fixes the
area. *SHM:* "start at x₀" needs a cosine, "start with speed v₀" a sine, "repeat every 2π/ω" fixes ω:
x = x₀cos ωt + (v₀/ω) sin ωt; the arrow packs both into A = x₀ − i v₀/ω. Ch6 01:25 just asserts it.

## 5. Proposed rules for DEEP_STYLE.md

For the producer to fold in; each is tagged **new** or **changes §N**.

1. **An idea budget, not a silence budget** (changes §1 sizing, §5 holds). Per scene: new formulas (F)
   ≤ ~1.5/min, ideas ~3/min (3b1b 1.0 and 3.1; ours 2.2 and 4.8), ~55 words per idea (ours 28), the
   extra words going on motive (≥ 1 motive sentence per 4 ideas; 3b1b 0.25, ours 0.08) and on
   restating as you go. No silence beyond the house pacing. The writer counts F per scene; the
   continuity review flags scenes over budget. Coverage stays fixed (§1), so the planner tiers it:
   **deep** (the 3–5 key moves per chapter, at this budget) and **reference** (routine results and the
   notes' worked examples at today's pace, marked as such on screen and collected in the moves sheet
   and solutions chapter, §10), so the viewer knows what to master and what to look up.
2. **Picture, then caption, then derivation** (changes §2). Per key formula: the picture moves while
   the narration says what it shows; the formula arrives as its caption, each symbol coloured like the
   part it names; any derivation comes after, beside the picture, which stays. The brief names each
   symbol's on-screen referent. ch2 c2.expo.2–3 is the case to invert.
3. **A live sweep with a readout for each key intuition** (new). ≥ 5 s of one parameter (θ, t, n)
   changing with a number updating beside it (P2, P8; de4 13:05). Per chapter: in motion ≥ 5% of the
   time (3b1b 3–21%, ours ~1%), still while speaking ≤ 50% (3b1b 2019+ 30–40%, ours 39–72%).
4. **The picture stays; the stack stays short** (changes §6). A picture in ≥ 75% of frames, maths-only
   frames ≤ 10% (3b1b 76% / 8%, ours 70% / 23%). Stacking and dimming stay, with ≤ 3 full-brightness
   formula lines and ~6 in all; past that the oldest leave and the legend keeps their letters.
5. **Name the move in words: an action and its effect** (changes §3). "Make the n-th arrow hold still,
   and the average kills the rest" (de4 18:56), with an analogy where one exists, not a formula; then
   why it works (calc5 04:21). About one per 5 min.
6. **Questions in the narration; few, honest holds** (changes §5). Keep 2–4 think stops per chapter;
   at ~8 s they're already longer than any 3b1b hold, so the question stays visible with "pause the
   video if you want longer". Add a narrated question or prediction at least every 2 min, answered
   within two sentences (3b1b 0.58/min, ours 0.38), and a motive or a question before every new formula.
7. **Second person** (new): "you might expect…", "ask yourself…"; ≥ 1.5 "you" per 100 words (3b1b 2.1).
8. **No lecture references in the narration** (new): no "the notes say", "equation seventy-seven";
   the reference becomes a small DIM tag on screen ("(77), notes p. 101").
9. **Open on the phenomenon, then the question** (changes §9). Within 20 s, show the thing moving (de4,
   clt) or state the puzzle (calc2), then the chapter's question; retrieval questions follow the hook.
10. **Physics before maths** (new; the SHM pilot). The model equation is assembled from named physical
    facts beside a diagram that stays (P1), gut-checked at two extremes with numbers (P2), then solved
    by reading the motion off the rule (P3), with the turning arrow's shadow as the answer (P6, P7).
    Nothing the chapter rests on is "taken as given".
11. **Atomic steps, flagged skips** (changes §4). One operation per step, as 3b1b's code does. New:
    routine algebra may be compressed only if the narration says so ("expanding, which I'll skip") and
    the full lines are in the solutions chapter; never skip what a step means, a sign convention or a
    gut check; a concrete number before the letter.
12. **Read the formula back** (new). After each key formula, one sentence reading it in the picture's
    language (de4 20:10: "out of context this expression might look complicated, but remember, you can
    read it as…").
13. **Recaps short and visual** (changes §3). 3b1b barely recaps; ours stays (retrieval is our
    addition) but ≤ 60 s, re-showing each key picture moving. Restatement runs through the chapter
    (finding 3), not only at the end.
