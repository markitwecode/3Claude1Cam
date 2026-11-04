# Teaching styles: auto (the default) and deep

The house teaching rules, set per project by `"style"` in project.json. `vk new` writes `"auto"` unless
told `--style deep` (or `--style classic`, the pre-2026-11-04 style at 1080p). A project with no `"style"`
field (everything made before 2026-11-04) keeps the classic style. Where this file conflicts with an agent
file's sizing, depth or order rules, this file wins. §0 says which sections apply to which style;
§11 (budgets and rules from the measured 3b1b study) refines §1–§6 wherever they differ.

## 0. The two styles (the user's decision, 2026-11-04, after watching the pilot)
"yeah i love it. i would keep this as deep but then keep auto as default. so first of all the extra
screen real estate should be the default and the idea of keeping stuff on screen for one idea. and
then for the depth auto would basically take what is already good from the lecture but any gaps or
unintuitive steps make atomic or add context to explain and build from ground up. enhance … oh and
the questions are quite nice"

**Shared by both styles (the new defaults):**
- **The board** (§6): finals at 2560×1440. One idea's picture and its derivation stay on screen together.
  A pinned legend holds the letters, and text may go down to 22. The widgets are in `engine/lib/teach.py`
  (§7); every project imports them and never rebuilds its own.
- **Questions** (§5, and §11's "questions in the narration"): 2–4 think stops per chapter, and a
  narrated question or prediction at least every ~2 minutes.
- **Named moves** (§3, and §11's "name the move as an action and its effect"): each derivation's 1–2
  key moves on a card, and the recap built from them.
- **Atomic steps and motives** (§4, and §2's rule "say the goal and why this move gets there"): one
  operation per step on screen, and a motive before every new formula.
- **Picture first** for every key formula, read back in the picture's language (§11). Plus second
  person, no lecture references aloud, a retrieval opener, and a short visual recap (§9, §11).
- **All of the 3b1b study's rules (§11), in both styles** (the user, 2026-11-04: "ALL the 3b1b findings
  let's implement!"). That includes live sweeps, pictures in ≥ 75% of frames, the deep/reference tiers for
  routine material, and opening on the phenomenon. §11's idea budget is replaced by the measured
  **load equalizer** (§13), which is a gate, not a guideline.
- **Explain each idea substantively** (3b1b: 58 words per idea vs our 28; 0.25 motive sentences per idea vs
  our 0.08; the user: "more narration per idea … if we could do that substantively"). Every hold gets four
  things:
  1. its motive before it: why we need it, why this move;
  2. the statement;
  3. a read-back in plain words or in the picture's language;
  4. a restatement when it's used again.

  The extra words are motive, meaning, consequence and questions, never padding. The load gate (§13)
  checks it from the auditor's coding: ≥ 0.20 motive sentences per idea and ≥ 32 words per idea, chapter
  mean. The auditor (Sonnet) counts ~1.3× the ideas the 3b1b study's coder did, so 3b1b reads ~45
  words and ~0.19 motive sentences per idea on this scale, and the loved pilot reads 18–26 words. 32 asks for
  ~30% more explanation than the pilot; it's provisional until the first auto lecture is rated. A chapter
  below either threshold goes back to its writer, who revises it or justifies it in the script report.
- **Pauses:** varied, at 1.5× (`vk new` writes `"pacing": {"scale": 1.5}`; the classic projects stay at
  2×). The think stops' "pause and ponder" invites the viewer to press pause (§5).
- **The reference rail** (§15): definitions, key results and letters stay visible on a side panel while they are in use: "use screen real estate to offload ram".
- **Keep the original during algebra** (§14): a rewrite never replaces an expression in place. The
  new form is written after an "=" below or beside it, and the change animates from a copy.

**auto, the default: the lecture, enhanced.**
- Coverage *and* order follow the lecture. Keep what it already does well: its examples, its order, and
  its pace wherever the steps are clear. Restructure only locally. A missing prerequisite becomes a
  scene just before the step that needs it, and a section may open on its motivating question.
- **The enhancement audit** (the planner's core job in auto). For every definition, derivation, claim
  and worked example in the material, ask four questions:
  1. Is every step atomic?
  2. Is the motive stated, i.e. why this move?
  3. Does it rest on something the viewer may lack, or that the course defers ("taken as given",
     "proved later")?
  4. Is there an intuition: a picture that makes it feel obvious?

  Each "no" becomes a planned enhancement: split steps, a motive line, a refresher built from the
  ground up (the pilot's "physics first" is the model), or an intuition picture. PLAN.md lists the
  audit per chapter: what is kept as the lecture does it, and each enhancement with its reason.
  Additions carry the "beyond the notes" tag.
- Pace: set by the load equalizer (§13), the same gate as deep. The lecture's own pace stands wherever
  it already sits inside the band; where it doesn't, the chapter gets more minutes, questions, or a
  refresher. There's no fixed minutes-per-lecture-hour target: report the length and its ratio to the
  lecture.
- Sections that apply in full: §3–§6, §9 (with "try before telling" used where it fits, not as the
  chapter order), §11, §12, §13 and §14. §1's free restructuring and §2's "build everything from first
  principles" apply only where the audit finds a gap.

**deep, on request ("do X in depth", "deep style"): the pilot's style.** All of §1–§12. Claude
restructures freely from first principles, uses §11's idea budget everywhere, and tiers the coverage
deep/reference. The model is `projects/nst-maths/l10-deep-oscillations/` (4 parts, 58 min, the user's
verdict "yeah i love it").

## Why
The user watched NST Maths L10 (`projects/nst-maths/l10-complex-roots-logs`) on 2026-11-03:
- "the pace is insane": from the definition of a complex number to simple harmonic motion in ~40
  min; "what is a ln of complex"; SHM named but never built ("which i don't even remember what it is").
- Steps aren't atomic: `i = e^{i(π/2+2πn)}` → `ln i = i(π/2+2πn)` in one transform (part 4).
- "pausing and asking a question? so i can actually engage? and not be force fed material at a
  crazy speed"
- "build from first principle and highlight why something is done", "Claude should be allowed to
  structure the lecture how it thinks is best. the material should be covered."
- "key ideas highlighted so i can actually remember. like 'the move here is this' and the rest
  could be derived … rather than a series of arbitrary manipulations like in the lectures"
- Screen: a 4K monitor run at 2560×1440. "more stuff can fit in one frame … so stuff can stack and
  i don't have to go back to check what a letter is"

The causes in the default style: the planner's "a lecture hour → 45–60 min, everything in the
material, follow its order" pins the video to the lecture's pace (but a lecturer writing by hand is
slower than an equation appearing in a second, and the lecture leans on notes, supervisions and the
example sheet). "Prerequisites: a one-scene refresher" and "the course proves it later" (Euler's
formula, L10 ch1) leave the foundations on trust. L10's 8 scripts have 114 `{pause}`s, all 1–1.5 s:
breaths, not thinking time. The board clears when a new idea needs room, so earlier lines vanish.

## 1. The lecture is the syllabus, not the script
- **Coverage is fixed.** Every definition, result, worked example, pitfall and exercise in the
  material appears somewhere. The planner keeps a coverage table in PLAN.md (material item →
  chapter and scene), and the continuity review checks it.
- **Everything else is Claude's call:** order, framing, examples, the number and length of
  chapters. Restructure so each idea arrives when the viewer needs it. E.g., open on "what could
  2^i even mean?" and introduce ln *because* powers need it, rather than defining ln cold. Say in
  Decisions where and why the order differs from the lecture.
- **No minutes-per-lecture-hour budget.** Size by what the explanation needs, and report the total
  and its ratio to the lecture. Chapters stay 8–14 min; a scene is still one idea.
- **Additions are marked.** Content beyond the notes (motivation, intuition, derivations the course
  puts off) gets a small DIM "beyond the notes" tag on screen, and the narration says so once.

## 2. First principles, and a motive for every move
- Build each idea from what the viewer already has. A result the course defers gets at least an
  intuitive derivation where later ideas rest on it. E.g., Euler's formula: d/dt e^{it} = i·e^{it},
  so the velocity is always perpendicular to the position and has length 1, so the point walks the
  unit circle at one radian per second.
- Prerequisites the viewer may lack are **built, not named**. E.g., SHM: a spring pulls back in
  proportion to how far it's stretched, so x'' = −ω²x. Which functions do that? Take as many scenes
  as that needs.
- Before each manipulation, say **the goal and why this move gets there**. The user's model: "We
  rewrite z₁^{z₂} as e^{z₂ ln z₁}. That turns a power we don't yet know how to compute into e to the
  product of two things we do know." Never a manipulation without its motive.
- Every definition answers "why would anyone define it this way, and what does it buy us?"
- **Intuition is the point, not decoration.** Lectures teach the technique; we add why it's true.
  Every formula worth remembering gets a picture that makes it feel obvious, and the picture comes
  first, with the formula read off it. The user's model ("elite", 2026-11-03): L10 part 2's two
  arrows. e^{iθ} and e^{−iθ} turn opposite ways, their imaginary parts cancel, and the sum slides
  along the real axis at 2cos θ. In that video the algebra came first and the picture second
  (`script/ch2_de_moivre.md`, c2.expo.2–3); deep style reverses that order. The planner lists, per
  chapter, the key intuitions and the picture for each, and a formula with no picture needs a
  stated reason.

## 3. Moves: what to remember vs. what follows
- Each derivation names its **1–2 key moves**: the non-obvious ideas, the ones you'd have to
  remember (e.g., "write the number with every version of its angle"; "rewrite the base as a power
  of e"). On screen: a boxed card, "The move: …", that stays on the board for the scene. In the
  narration: "The move here is …". The planner fixes one look for it across the project.
- Everything else is presented as following on its own: "from here, every step is forced."
- The recap is the chapter's moves (each with a small version of the visual that taught it), plus
  the few facts that can't be derived and must be remembered. It is not a list of results.

## 4. Atomic steps
- One operation per arrow. Each arrow carries a justification of five words or fewer beside it:
  "take ln of both sides", "ln undoes e^", "a full turn changes nothing". Never one transform that
  changes two things.
- The writer's test: could the viewer say why each arrow is true in five words? If not, split it.
  The continuity review checks every derivation for skipped steps.
- The user's screenshot, done right:
  `i = e^{iπ/2}` [distance 1, angle π/2] → `i = e^{i(π/2 + 2πn)}` [a full turn changes nothing]
  → `ln z` = every w with e^w = z [the definition] → `ln i = i(π/2 + 2πn)` [read off the exponent].

## 5. Think stops: engage, don't force-feed
- **2–4 per chapter.** Each is a real question the viewer can answer from what they've just seen:
  predict a result, the next step or a count. On screen: the question in a box (`lib.teach.think_box`)
  with a small DIM "pause and ponder" line. Nothing else moves. In the narration: the question, then
  an invitation to pause ("pause and think it through", "pause here and try it"), a short beat, then
  the answer worked out.
- **The viewer pauses, the video doesn't wait** (changed 2026-11-04, the user: "let's have [the pauses]
  be optional so i can pause and it's interactive. like he does"; the 3b1b study found his "pause and
  ponder" holds last only 1–5 s). Write `{pause=1.5}` after the invitation (~3 s with house pacing).
  The question stays on screen through the start of the answer, so a viewer who pauses a moment
  late still sees it. The draining ring is optional; with a short hold, leave it out.
- Quick predictions before a reveal ("before we divide by five: how many answers do you expect?")
  need only `{pause}`.

## 6. The board, built for a 2560×1440 screen
- Finals render at 1440p60 (manim `-qp`, 2560×1440 at 60 fps).
- The key picture stays on screen, and the derivation stacks beside it, top to bottom. Earlier lines
  dim to ~0.4 instead of vanishing; at most 3 lines at full brightness. A derivation in progress stays
  whole until it ends (atomic steps make derivations long; ~8 lines fit at 1440p). After that, the
  oldest finished lines leave, and the legend keeps their letters.
- **The reference rail** (§15) replaces the corner legend (since 2026-11-04): a panel down the left edge
  (x −6.8..−3.4) holding the letters, definitions and results in play. The picture sits in the middle
  (x −3.1..1.0, full height), the stacked column on the right (x 1.25..6.6), and the think box under the
  column. The slot map lives in `engine/lib/teach.py`, and the `legend*` calls are wrappers around the rail.
  Nobody should rewind to check a letter.
- Text may go below the house minimum of 28, down to ~22, for legends, arrow labels and dimmed
  earlier lines. Check it on a 1440p frame during the pilot.
- More on screen is fine; crowding is not. The current line stays the brightest, largest thing.

## 7. Engine wiring (done 2026-11-04)
- project.json `"resolution": "1440p"` makes finals render `-qp` (2560×1440 at 60 fps) into
  `media/videos/<stem>/1440p60/`. The helper is `lib/paths.py` `final_quality()`, used by
  `tools/render.py` and the resolution check in `tools/finalize.py`. Previews stay 480p15.
  `review.py` detects quality from the file. The 1440p render slot asks 1.6 GB (a guess).
- project.json `"style": "deep"`: all four agent files open with a line telling them to read this
  file first. `tools/check.py`'s minimum font size drops from 26 to 20 (22 here, minus the usual
  2 of tolerance).
- `vk new --style auto|deep|classic` (default auto) writes `"style"` and, for auto and deep,
  `"resolution": "1440p"`.
- The widgets live in `engine/lib/teach.py` (`from lib.teach import *`; promoted 2026-11-04 from the
  pilot's `ch1_s2_tools.py`): the slot constants, legend panel (`legend`, `legend_add`/`_set`/
  `_change`/`_remove`), `move_card`, `think_box` + `think_ring` + `drain`, `tag`/`corner_tag`,
  `pinned`/`pin_move`, the derivation column (`col_place`, `step_label`), `chrome` for joins,
  `arrow_between`, and `clock`. scene-builder.md lists the API and the slot layout. The look and the
  slots are the pilot's, with two changes: column pitch 0.8 (was 0.7; step labels sat ~0.05 from
  the lines), and move cards that break into even lines at 28→24 px before taking a third line.

## 8. The pilot: the pendulum (the user's choice, 2026-11-04)
- "for the first in depth trial do the pendulum stuff. explaining the physics first etc." The
  material is L10 §2.6: simple harmonic motion, the pendulum, complex amplitudes, differentiating by
  multiplying by iω, and Examples Sheet F19. In the old series this was part 6 (8.5 min, from 4.5
  min of lecture, 00:41:45–00:46:18). The circuit example (Ex 32, the old part 7) is out of scope.
- Project: `projects/nst-maths/l10-deep-oscillations/` (style deep, 1440p). The old part 6 stays in
  `l10-complex-roots-logs/out/ch6_oscillations.mp4` for a side-by-side comparison.
- Build the physics first: what a pendulum or spring does, why the restoring force gives
  x'' = −ω²x, which functions do that, and only then the complex-number view (the solution as the
  shadow of a turning arrow, d/dt = ×iω as a quarter turn). The viewer has seen L10's parts 1–5
  (e^{iθ}, De Moivre, cos θ = (e^{iθ}+e^{−iθ})/2 as two arrows).
- Inputs: `docs/3b1b-study.md` (its patterns for DE1 and DE4 especially), this file, and L10's
  PLAN.md (conventions, colours, and its chapter 6 section as the old version).
- Measure: minutes against the old part 6, the Claude cost (`vk usage`), and the user's verdict.
- If the user likes it: make deep the default for maths, update the "Depth" decision in CLAUDE.md
  and the agent files, and record the cost per lecture against the <10% weekly target.

## 9. From learning science (added 2026-11-03, after the user asked "this should be studied")
Evidence strength is in brackets. All of these go into the pilot's scripts; they cost little beyond
some extra minutes.
- **Try before telling** [meta-analysis: Sinha & Kapur 2021, 53 studies; g ≈ 0.37–0.58 when done
  faithfully, for concepts in maths and science; worse for young children]. Open a chapter on a problem
  the viewer can't yet solve ("what is 2^i?"), give a think stop, let the attempt fail, then build the
  tool that answers it. With section 1's freedom, this is how chapters should be ordered.
- **A retrieval opener instead of "last time"** [practice testing and distributed practice: the two
  "high utility" techniques, Dunlosky et al. 2013]. 2–3 quick questions on the previous chapter's moves,
  answered after a short hold; now and then one on an earlier lecture's move (spacing).
- **Worked → faded → yours** [worked-example fading, Renkl & Atkinson; expertise reversal, Kalyuga].
  The first example is fully worked, with its moves named. In the second, the viewer supplies the moves
  at think stops. The third is a sheet question with a hint only.
- **Concrete before abstract** [concreteness fading, Fyfe et al. 2014]. Numbers first: compute 2^i ≈
  0.77 + 0.64i and see it on the plane, then the general formula.
- **Name the wrong idea, then break it** [refutation texts, meta-analysis g = 0.41, Schroeder &
  Kucera 2022]. State the tempting mistake outright ("ln(z₁z₂) = ln z₁ + ln z₂, always?", "i^i must
  be imaginary"), show it fail on a number, and explain why. A deliberate beat, not a passing RED word.
- **Names before process** [Mayer's pre-training principle]. A short cast list at the start of a
  chapter (the objects and letters it will use), and from then on the pinned legend.
- **Ask why before showing why** [self-explanation, elaborative interrogation: "moderate utility"].
  At some arrows, ask why it's allowed, hold, and only then show the label.

## 10. Beyond the videos (after the pilot; the strongest evidence is for what happens after watching)
- **A deck of the moves.** Anki cards made from each chapter's move cards and its must-remember
  facts. The front gives the situation ("a power with a complex exponent"); the back gives the move
  and why it works. This is practice testing plus spacing, the two high-utility techniques.
- **Hint ladders instead of full solutions.** For each sheet question: hint 1 names the move, hint 2
  gives the first step, then the solution. This could replace the bonus solutions chapter, or sit
  beside it as a page.
- **A one-page moves sheet per lecture:** the moves, the skeleton of each derivation, and what comes
  from what.
- **Interleaved practice** ["moderate"]: now and then, mixed questions from several lectures. "Which
  move?" comes before "do it".
- **Scene chapter markers in the mp4s** (ffmpeg chapter metadata; IINA, VLC and QuickTime show them),
  so a scene or a think stop is one click away. This is learner control (Mayer's segmenting
  principle). It's a small change in `tools/render.py` `stitch()`.
- **A learner profile in COURSE.md:** what the user already knows and what didn't land (e.g., SHM:
  physics only to GCSE). Every planner reads it, and it's updated after each lecture's feedback.
- **How to study with it:** re-watching is like rereading ("low utility"). Better: attempt the think
  stops for real, try the sheet with the hint ladder, review the deck daily, and a few days later
  re-derive the moves on a blank page.

## 11. Budgets and rules from the 3b1b study (2026-11-04; `docs/3b1b-study.md`)
Measured on 8 3b1b videos against 4 of ours (study §2). 3b1b is *not* slower: it speaks 174 words per
minute of video against our 132, and is silent 23% of the time against our 40%. What differs is how
the words are spent. We introduce 4.8 ideas and 2.2 new formulas per minute against 3.1 and 1.0. We
spend 28 words per idea against 58. We have a third as many motive sentences and half as many
questions per idea. 23% of our frames are maths-only against 8%. So the lever is ideas per minute and
the words around each idea, not more silence. The house pacing stays as it is; add no extra holds
beyond the think stops.

- **An idea budget, in two tiers** (refines §1). The planner tiers every item of the coverage table:
  - **Deep:** the chapter's 3–5 key moves and intuitions. At most ~1.5 new formulas and ~3 ideas a
    minute, ~55 words per idea, the extra words spent on motive (≥ 1 motive sentence per 4 ideas),
    questions and restating as you go.
  - **Reference:** routine results and the notes' remaining worked examples. Faster, and marked on
    screen with a small DIM "reference" tag, so the viewer knows what to master and what to look up.
    The producer's ruling: reference items still follow §2 (a motive for every move) and §4 (atomic
    steps on screen). They get less intuition-building and fewer stops, never bigger steps.

  The writer counts new formulas per scene, and the continuity review flags scenes over budget.
- **Picture, then caption, then derivation** (refines §2). For each key formula, the picture moves
  while the narration says what it shows. The formula arrives as the picture's caption, each symbol
  coloured like the part of the picture it names. Any derivation comes after, beside the picture,
  which stays. The brief names each symbol's on-screen referent.
- **Read the formula back.** After each key formula, one sentence reads it in the picture's language
  ("out of context this looks complicated, but you can read it as …").
- **A live sweep for each key intuition.** At least 5 s of one parameter (θ, t, n) changing, with its
  number updating beside it. Per chapter: in motion ≥ 5% of the time (3b1b 3–21%, ours ~1%), and the
  frame still while speech continues ≤ 50% of the time (3b1b 2019+ 30–40%, ours 39–72%).
- **Pictures over bare maths.** A picture in ≥ 75% of frames; maths-only frames ≤ 10%.
- **Name the move as an action and its effect** (refines §3): "make the N-th arrow hold still, and the
  average kills the rest". Use an analogy where one exists, then say why it works.
- **Questions in the narration** (refines §5). Besides the 2–4 think stops, a question or prediction
  at least every 2 minutes, answered within two sentences, and a motive or a question before every new
  formula. Think stops keep the question visible with "pause the video if you want longer", since
  ~8 s is already longer than any 3b1b hold.
- **Second person:** "you might expect …", "ask yourself …", at least 1.5 "you" per 100 words.
- **No lecture references in the narration.** Not "the notes say", not "equation seventy-seven". The
  reference becomes a small DIM tag on screen ("(77), notes p. 101").
- **Open on the phenomenon, then the question** (refines §9's "try before telling"). Within 20 s, show
  the thing happening or state the puzzle, then the chapter's question. The retrieval questions come
  after the hook.
- **Physics before maths** (the pilot). Assemble the model equation from named physical facts beside
  a diagram that stays (study P1). Gut-check it at two extremes with numbers (P2). Solve it by reading
  the motion off the rule (P3), with the turning arrow's shadow as the answer (P6, P7). Nothing the
  chapter rests on is "taken as given". The old part 6 said "we'll take that as given" of ω = √(g/L).
- **Atomic on screen, summarised by voice** (refines §4; the study proposed allowing skips, which the
  producer overruled because the user asked for every step). Every step is on screen. The narration
  may summarise routine algebra ("expanding the bracket gives …") instead of reading each line, but
  never skips what a step means, a sign, or a gut check. A concrete number comes before the letter.
- **Recaps short and visual** (refines §3): ≤ 60 s, each key picture re-shown moving. Restating runs
  through the chapter, not only at the end.

## 12. Refinements from the pilot's planner (2026-11-04)
- The 1.5-new-formulas-a-minute budget counts **new formulas** (a new relation the viewer has to
  understand), not every line of a worked example. An atomic worked example runs 4–5 lines a minute
  and is paced as reference material.
- When nearly a whole chapter goes beyond the notes (e.g. the pilot's physics part), use one corner
  tag for the chapter instead of a tag on every item.
- The first chapter of a new topic has no previous chapter to retrieve from: its opener retrieves the
  prerequisites instead (e.g. F = ma, right-angled trigonometry, arc length).
- The corners fill up at 1440p (legend, move card, pinned formula, think-stop ring, tags). The planner
  gives each a fixed slot, and the busiest scene's frame is checked first.

## 13. The load equalizer: a gate on how fast material arrives (2026-11-04; `docs/load-calibration.md`)
Measured on chapters the user rated. What separates "felt fine" from "too dense" is **holds per minute
(H)**: new formulas plus new terms or definitions the viewer hasn't met before, the things they must hold in
their head. Raw ideas per minute, words per idea, voice speed and "jumps" didn't separate the groups.
Questions to the viewer (Q per minute) offset load: H − Q separates the groups ~3× more cleanly.
Comfortable: DE L10, the pendulum pilot, H 1.35–1.87, H − Q 0.76–1.17. Too dense: old maths L10, L11's
cosh, H 2.05–3.57, H − Q 1.71–3.10. It's a small sample (8 chapters), so the numbers are provisional.

- **Thresholds per chapter:** mean H 1.3–1.8, never above 1.9; mean H − Q 0.7–1.2, never above 1.4. A
  question to the viewer in every 2 minutes is the target, but it's advice, not a fail: all four
  comfortable chapters have 2.4–5.3 min gaps.
- **Peak limit:** no 2-minute stretch introduces more than 9 holds (hard); 8 is the target (advice). A
  comfortable DE chapter sits at exactly 8, and the estimate before voicing is ±0.5. A chapter can average fine and still
  have one burst (four new formulas and a definition in 90 s) that loses the viewer for the rest of it.
  The peak limit catches the burst.
- **Planner:** count the holds in the material first; chapter minutes ≈ holds ÷ 1.6. Spread them out,
  and put questions between them.
- **The gate:** after the continuity review and before voicing, an independent `load-auditor` agent
  (Sonnet, not the writer) codes each chapter's script clip by clip with the fixed rubric in
  `docs/load-rubric.md`. `vk load N` then times the clips (words at 130 wpm before voicing, real
  durations after) and checks every threshold. A chapter over a limit goes back to its writer with the
  flagged windows; it is re-audited after the rewrite. `vk load` runs again after voicing as a check.

## 14. Keep the original during algebra (the user, 2026-11-04)
"when stuff just gets replaced in an expression the animation is nice but it's confusing coz you don't
see what was there. first rewrite it with an equals, then do the transform shenanigans so i can always
see the original."
- Never transform an expression in place (`TransformMatchingTex(old, new)` where `new` replaces `old`).
  Write the next line *beneath* (or beside) with a leading "=", animate the change from a copy
  (`TransformFromCopy` or the matching-parts variant on a copy), and keep the original visible. It may
  dim to ~0.4 once the new line has landed.
- A substitution shows where things came from: the replaced part is coloured in the original before
  the copy moves.
- The helper is `lib.teach.derive_step` (see the scene-builder kit). The stacked column (§6) is where the
  lines go.

## 15. Offload working memory onto the screen: the reference rail (the user, 2026-11-04)
"i would really emphasize using screen real estate to offload ram. like i have a 27 inch 2k. you can keep
definitions and stuff visible."
- Every project with a style has a **reference rail**: one panel along a side edge holding everything a
  viewer might otherwise rewind for. That's the letters (the legend becomes the rail's top section) and the
  definitions and key results currently in play, each as a short formula or definition plus a few words of
  meaning, at 22–26 px (`lib.teach.rail`).
- **Every hold goes on the rail** (§13: each new formula or term). It is added when it's introduced, and it
  stays while the chapter still uses it. When the narration uses an entry again, `rail_highlight` flags it
  briefly. An entry leaves only when the chapter is done with it.
- This is the other half of the equalizer: a hold that stays on screen costs less to keep in your head. It
  takes priority over §11's "the stack stays short" and over picture size: the picture and the column may
  shrink a little to make room.
- The planner lists each chapter's rail entries (what goes on it, when, and when it leaves). The writer's
  brief names the rail changes per scene. The rail carries across scene joins like the legend did.
