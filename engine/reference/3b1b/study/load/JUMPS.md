# Jump audit brief

You are auditing nine chapter transcripts of our narrated lecture explainer videos for **jumps**, one
code only, with one consistent standard across all nine. Read-only everywhere except your output
files. S = `/Users/markgolbraikh/Documents/3Claude1Cam/engine/reference/3b1b/study/load`.

**Inputs.** For each chapter key, read `S/BRIEF.md`'s input table (rows: transcript, script, the
PLAN.md lines that say what this viewer already has) and its paragraph "The viewer, for every
chapter". Read each transcript in full, and the script's visual briefs wherever you need to know what
is on screen. **Ignore everything else in BRIEF.md** (its rubric parts 1–2, its anchors table and its
output section are not yours).

**The viewer:** a Cambridge first-year with A-level Maths (not Further Maths) and GCSE physics only,
plus the earlier lectures and earlier chapters that PLAN.md lists. Read every sentence as this viewer,
hearing it once at speaking pace, seeing what the visual brief puts on screen.

## What a jump is

A place where this viewer must do unstated work to follow the argument, or must accept a move without
knowing why it is made. The felt test: would they think "wait, where did that come from?" or "why are
we doing this?" At most one jump per sentence, with its type(s):
- **`s`, non-atomic step.** (a) A new line or result that follows from what is on screen and just
  said by **two or more** elementary operations (substitute, expand, collect, cancel, apply one
  identity or one rule, solve one linear equation, take one limit, read one value off a picture…)
  whose intermediate is neither said nor shown. Test: could this viewer verify it in a few seconds?
  (b) A derivable result (a formula, a solution, a consequence) asserted with no reason or
  derivation, which the chapter then builds on, including "we'll take that as given". Not a jump if
  the reason follows within ~6 sentences or the same scene. Plain facts of the world, definitions
  and conventions stated as such are not jumps, nor is recalling something the viewer already had.
- **`m`, unmotivated move.** The narration makes a choice the viewer couldn't predict (a
  substitution, a trick, a new construction or object, a particular rearrangement, a new case, a
  change of direction), and nothing in this sentence or the three before or after says why *this
  move* should help: a goal it serves, a question it answers, or why it works. An overall goal is
  enough only when it makes the move the obvious next thing. Obvious next moves (divide to isolate,
  substitute the value just found, apply the rule just stated) never count. A question posed just
  before counts as the reason for the move that answers it.
- Both: `sm`. Explicitly flagged skips ("we'll take that as given", "I'll skip the algebra"): append
  `f` (`sf`). Still a jump. Put the jump on the sentence where the viewer must accept or follow it.

Calibration examples (invented, not from these chapters):
| sentence | J | why |
|---|---|---|
| "Square both sides and tidy up, and y is three." (no lines shown) | s | square, expand, collect: unseen |
| "The period is two pi root L over g. We'll take that as given." (then used) | sf | asserted, then built on |
| "Now multiply both sides by E to the minus ex." (no reason near) | m | why this factor? |
| "To clear the exponential, multiply both sides by E to the minus ex." | – | motive in the sentence |
| "Divide by the mass: the acceleration is F over M." | – | obvious next move |
| "Here's a neat trick: write one as sine squared plus cosine squared." (no reason near) | m | trick unmotivated |
| "Expand the bracket: x squared plus two x, plus one." (one operation, said) | – | atomic |
| "So the answer is the real part, A cos omega t minus B sin omega t." (product of two complex numbers, real part taken, nothing shown) | s | multiply out, i² = −1, take Re: unseen |

## Order, output, reply

Code in this order: l12ch1, pil2, l10ch4, de10ch4, l11ch1, pil1, l10ch2, de10ch2, l10ch6. Before
you start, re-read the definition and the examples; after the first chapter, re-read your jumps
against them, fix them, and keep that standard. Be neither lenient nor eager: flag what this viewer
would actually trip on.

One file per chapter, `S/codes/<key>.jumps.json`, written as soon as that chapter is done:
`{"key": "pil2", "n_sentences": 177, "jumps": [{"i": 117, "J": "s", "why": "≤ 15 words"}, ...]}`
(only the flagged sentences). Reply in ≤ 10 lines: per chapter, the number of jumps (s / m), then
one line on what kind of jump recurs most.
