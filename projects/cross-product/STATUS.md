# The Cross Product: status

2026-10-25: project created; planning.

## Chapter 1 · From a picture to a formula (ch1_cross_product)

**State: final rendered, 2026-10-25.** `out/ch1_cross_product.mp4`, 1920×1080 at 60 fps, 11.8 min
(709 s). All 8 scenes are built and reviewed over one fix round. Music is in `music/ch1.json`:
Quaternions under the hook, Machinery under the s7 proof (lin.1–lin.2), and Clarity from the
recap through the end card.

**Narration rewritten for the ear and re-voiced** (re-checked with Whisper base and small.en,
including cropped segments):
- c1.hist.1: the rule is now "Eye squared, jay squared, kay squared, and eye jay kay, all equal minus
  one." (before, "kay" came out as "chi"). Also "when, after years of hunting, the rule finally came
  to him in a flash" (before, "came to him" came out as "came down").
- c1.def.2: "…straight down to ay, meeting it at a right angle." and "So ay cross bee is as long as
  the base times the height, …" (before, "ay" came out as "AI" / "A A").
- c1.mach.3: "In other words, ay cross bee equals…". c1.mach.4: "The product, ay cross bee, meets ay at
  right angles, …". Sentence-initial "Ay" was voiced as "aye" (the word "eye").
- c1.comp.1: "a cross product of two unit arrows" (before, "unit arrows" came out as "unit errors").
- c1.comp.2: "First, ay one times bee two, … Next, ay two times bee one, … ay one times bee two,
  minus ay two times bee one." (before: sentence-initial "Ay" came out as "eye", and "ay two bee
  one" as "a1 b1").

**Voice QA flags left, all false positives:**
- hist.1, hist.3 and def.2 sentence 1: Whisper writes the spoken years and "a hundred and eighty"
  as digits.
- comp.2 (21%): Whisper writes "ay one" as the single token "a1", which the normaliser doesn't split.
  Cropped transcripts read correctly in both models.
- hist.3: "Heaviside" is transcribed as "Heveside", which is close.

**Check by ear:** c1.comp.2 (the subscripts); c1.hist.1 (the rule; "eye jay kay" has a slight pause
before "kay"); c1.mach.4 ("to ay" still transcribes as "AE"/"AI" twice, probably a drawn-out "ay");
c1.hist.3 ("Heaviside"); c1.def.2.

**Accepted check flags:**
- Dwell flags at scene handoffs, by design: the s2→s3 a×b, the s4→s5 end-shot labels, and s4's
  labels when s6 opens.
- s1 title card, 3.3 s per line: the brief clears it on {arrows}.
- s4: "a vector" / "a number" / a·b=3 are short. They are two-word tags spoken as they appear, and
  the tail was cut from 6.4 s to 3 s for pace.
- s3: "That pattern is the definition." shows 4.7 s.
- Short passing steps in s5, s6 and s8. Each fact stays on screen in the table, the formula or the
  end card.
- s6 overlap and s7 "cut off" flags: the check measures 3D objects in world coordinates, not where
  they land on screen. The frames are clean.

**Open, for the engine:** engine/lib has no 3D NarratedScene. Each 3D scene defines a local
`NarratedScene` and a `Camera3D`/`PanCamera` subclass, the latter to work around CE 0.22 applying
frame_center twice to fixed-in-frame mobjects. `vk` only finds `class X(NarratedScene)`. The voice QA
normaliser doesn't split "a1"-style tokens.
