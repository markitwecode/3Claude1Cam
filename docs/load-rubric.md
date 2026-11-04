# Load rubric: coding a chapter for the load gate

The load gate (DEEP_STYLE §13, §0) measures how fast a chapter makes the viewer hold new things, and
how much explanation each idea gets. A `load-auditor` codes the script with this rubric, and
`vk load N` times the codes and checks the thresholds. The thresholds were measured on chapters coded
with the calibration's brief (`docs/load-calibration.md`; the brief is
`engine/reference/3b1b/study/load/BRIEF.md`), and this rubric is that brief, adapted from transcripts to
scripts. **Code exactly by it, not by taste.** A coder who counts differently moves every number, and the
thresholds only mean something on this scale.

## Inputs
- **The chapter's script** `script/chN_<slug>.md`: the narration lines `[cN.key.k]` and a visual brief
  (`>` lines) per scene. Code the narration, what is **said**. Read the brief only to see what is on
  screen (e.g. whether an intermediate line is shown, or what a "this" points at).
- **The sentence numbers:** `vk -C <project> load N --list` prints every line split into sentences
  `s1, s2, …` (a sentence ends at `.`, `?` or `!`, not at a colon). These numbers are your keys. Code
  **every** sentence.
- **What the viewer already has:**
  - PLAN.md's Audience paragraph;
  - the PLAN.md sections of the earlier chapters of this project;
  - the earlier chapters' narration, from `vk load M --list` for each earlier chapter M;
  - for a course project, COURSE.md and the earlier lectures the Audience paragraph names.

## The viewer (the audience rule)
"New to this viewer" is judged against **what the viewer had before this chapter started**:
- the prerequisites PLAN.md's Audience paragraph states (e.g. "A-level Maths, not Further Maths; GCSE
  physics");
- the earlier lectures it names;
- everything the project's earlier chapters taught.

Nothing else counts as known. When the Audience paragraph is vague about something, assume the
viewer doesn't have it: in doubt, a unit is new (`+`). Say in your reply which calls that decided.
Common cases:
- A school syllabus means its standard content. A-level Maths has algebra, trig identities, radians,
  e^x and ln for reals, the chain, product and quotient rules, integration, binomial expansion,
  geometric series and simple separable ODEs. It has **no** hyperbolic functions, complex numbers,
  matrices beyond 2×2 or simple harmonic motion: those are Further Maths.
- GCSE physics: F = ma, weight = mg, Hooke's law, speed, velocity and acceleration in words.
- Anything first met **in this chapter** is new, including lines derived here from known pieces, and
  numeric values of functions defined in this chapter.

## Part 1: units per sentence (verbatim from the 3b1b study's rubric; do not reinterpret)
Code each sentence (or clause, if it holds two units) with zero or more of:
- **F, new formula:** a symbolic statement heard for the first time in this video: an equation, an
  identity, a new symbolic expression the viewer must hold, or a new line of a derivation (each new
  line = 1 F). Re-reading an earlier formula is not F.
- **D, definition:** a new technical term or notation introduced with its meaning ("this ratio is
  called the derivative", "the modulus is the length").
- **C, claim:** a new mathematical or physical assertion presented as true (a property, a rule, a
  result, a reason why something is true), stated for the first time. Not narration about the video,
  not a question, not an analogy by itself, not a restatement.
- **R, restatement:** a sentence that re-expresses an idea already given (recap, "in other words",
  saying the same thing a second way, reading a picture's meaning again).
- **M, motive:** a sentence that gives the goal of a step or why we are about to do something ("to get
  rid of the sine, we...", "the question is how to...", "this is useful because...").
- **Q, question to the viewer:** an explicit question posed to the audience, rhetorical or real
  (including "pause and ponder"), plus predictions asked for.
- A worked arithmetic or numeric step counts as F only if it is a new equation line.

Be consistent. When unsure between C and R, ask "would a viewer learn something new from this
sentence?"

Subject notes:
- A digital-electronics state code, a K-map group or a Boolean expression such as "D_B = A" counts as
  a formula, F, like any equation.
- A line of code the viewer must read and hold (a new function, a new type) counts as F. Code chapters
  weren't in the calibration, so flag that in your reply.

## Part 2: novelty
Every F, D and C gets a suffix:
- **`+` new to this viewer**;
- **`k` known:** a recall, reuse or re-wording of something the viewer had before this chapter (see
  the audience rule). "Last time, we showed X" is `Ck` (or `Fk`). Numeric values of functions the viewer
  already had (sin 30° = ½, e ≈ 2.72) are `k`.

R, M and Q take no suffix.

## What goes in the coding
- **Holds** are the F+ and D+ units: the things the viewer must now carry in their head. A recall (`k`)
  is not a hold, and neither is a restatement, or a claim about what's on screen.
- **Questions** are the Q units, with one exception: a "pause the video if you want longer" line
  doesn't count, since its think stop already counts as a question.
- **Ideas** are F + D + C, both `+` and `k`: count every unit.
- **Motive** is the number of sentences coded M.
- **Patterns.** Sometimes one stated rule is applied to several parallel cases in a row ("in the same
  way, green takes its input from red-and-amber, amber from green, and red from amber"). Each line is
  still its own hold, but give them all the same `pattern` label. The 2-minute peak counts a pattern
  once; the chapter mean counts every line.
- **Until (optional; for the reference rail, DEEP_STYLE §15):** the last line id where the chapter
  uses that hold again, if it does.

## Part 3: jumps (optional extra field; not part of the gate)
A jump is a place where this viewer must do unstated work to follow, or accept a move without knowing
why it's made. Code at most one per sentence:
- **`s`, non-atomic step.** Either of:
  - (a) a new line that follows from what's on screen and just said by **two or more** elementary
    operations whose intermediate is neither said nor shown;
  - (b) a derivable result asserted with no reason, which the chapter then builds on (including "we'll
    take that as given").

  It isn't a jump if the reason follows within ~6 sentences or the same scene.
- **`m`, unmotivated move.** The narration makes a choice the viewer couldn't predict, and nothing in
  this sentence or the three before or after says why *this* move helps. Obvious next moves never
  count, and a question posed just before counts as the reason.

Both at once is `sm`. Add `f` when the narration flags the skip ("I'll skip the algebra").

## Anchors (fixed codes from the calibration: match this standard)
| sentence | units | J | why |
|---|---|---|---|
| "For small swings, it rocks back and forth with an angular frequency, omega, equal to the square root of G over L…" (next: "We'll take that as given") | D+ F+ | sf | ω = √(g/L) asserted |
| "Then the displacement always has this form. / It's a real constant times the cosine of omega T, plus another real constant times the sine of omega T." | none / F+ | – / s | general solution asserted, then built on |
| "This is called simple harmonic motion." | D+ | | |
| "In symbols, the displacement is the real part of this turning arrow." | F+ | | justified a few sentences later |
| "Eye times eye is minus one, so the two imaginary pieces multiply to give a real term, minus beta times the sine of omega T." | F+ | | one operation, said |
| "Do it twice, and you multiply by eye omega twice, which is minus omega squared." | F+ | | one step from the rule just stated |
| "Force equals mass times acceleration, so you divide the force by the mass." | Fk | | GCSE |
| "…the pull is proportional to the stretch. / That's Hooke's law, from GCSE physics." | Ck / Dk | | GCSE |
| "So the pull is minus the stiffness K, times ex." | F+ | | a new signed line |
| "So the move here is: name the force that pulls back, then let Newton turn it into an acceleration." | M | | |
| "Call it omega squared. / It's written as a square for a reason part two makes clear." | D+ / – | mf / – | why a square is deferred |
| "…so its distance along the arc is L times theta, with theta in radians." | Fk | | A-level arc length |
| "The length L is fixed, so differentiate twice: the acceleration along the arc is L times theta double dot." | F+ | | one operation, reason given |
| "Now lift out every eye. / What stays is E to the ex, plus E to the minus ex, all over two." | – / F+ | m / – | no reason given for removing the i |
| "…one in just two states, 000 and 001. / They sit side by side, so they make a pair, and the input to flip-flop A is not bee and not see." | C+ / F+ | | a K-map pair, one step, shown |
| "Pause the video if you want longer." | – | | not a question: the think stop before it is |

TTS spelling in scripts: "eye" = i, "E to the eye theta" = e^{iθ}, "zed" = z, "ex" = x, "why" = y,
"shine" = sinh, "bee/see/dee" = letters.

## Output: `script/chN_load.json`
One entry per narration line, in script order, none skipped (a line with nothing to code still gets
an entry with empty lists and zeros):
```json
{"chapter": 1, "script": "script/ch1_first_principles.md", "coder": "load-auditor", "rubric": 1,
 "audience": "A-level Maths (not Further Maths), GCSE physics, NST Maths Lectures 1–11",
 "clips": [
  {"id": "c1.chord.2",
   "holds": [{"s": 1, "kind": "D", "text": "chord: the line through two points of the curve", "until": "c1.recap.1"},
             {"s": 2, "kind": "F", "text": "slope = δy/δx (rise over run)"}],
   "questions": [],
   "ideas": 4, "motive": 0,
   "recalls": [{"s": 3, "text": "y = x³ (A-level)"}],
   "jumps": []}
 ]}
```
- `holds`: `s` is the sentence number from `--list`; `kind` is `"F"` or `"D"`; `text` is the formula
  in plain maths notation, or the term with a few words of meaning (≤ 15 words). `pattern` and `until`
  are optional.
- `questions`: `s`, plus `text` (≤ 15 words).
- `ideas` and `motive`: whole numbers for the line.
- `recalls` (the `k` units) and `jumps` (`{"s", "J", "why"}`) are optional, but list the recalls: they
  show why a formula *wasn't* counted.
- Check it with `vk -C <project> load N --check`, which compares it with the script without showing
  any verdict. Fix every error and warning it prints.

## Calibration notes
- Two calibration coders of one chapter differed by 0.22 holds per minute on average. A chapter within
  ~0.2 of a limit is a judgement call, not a measurement.
- These coders (Sonnet) find ~1.3× as many ideas as the 3b1b study's original coder (Opus), mostly
  more C and less R. Their holds (F+, D+) are on the study's scale. Their words per idea run lower:
  DE L10, the pendulum pilot and old maths L10 all came out at 18–26.
