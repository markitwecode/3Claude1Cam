# Coding brief: idea units, novelty and jumps

You are one of six coders in a measured study of our narrated lecture explainer videos (studio:
/Users/markgolbraikh/Documents/3Claude1Cam). Each chapter is coded by two coders independently, so
code exactly by this rubric, not by your own taste. **Read-only everywhere** except your own output
files in `/Users/markgolbraikh/Documents/3Claude1Cam/engine/reference/3b1b/study/load/codes/`.

S = `/Users/markgolbraikh/Documents/3Claude1Cam/engine/reference/3b1b/study/load`
P = `/Users/markgolbraikh/Documents/3Claude1Cam/projects`

## Inputs per chapter
- **Transcript** `S/tx/<key>.txt`: what was actually voiced, one sentence per line:
  `S017 [01:25] (c6.pend.2) text`. TTS spelling: "eye" = i, "E to the eye theta" = e^{iθ},
  "zed" = z, "ex" = x, "shine" = sinh, "tanch" = tanh, "bee/see/dee/ee" = flip-flop letters B–E.
  Code **every** sentence; the sentence numbers are your keys. Read it in full.
- **Script** (the chapter's narration plus a visual brief per scene): use it only to see what is on
  screen (e.g. whether an intermediate line is shown). Where its narration differs, the transcript wins.
- **What the viewer already has**: the PLAN.md lines listed below (the Audience paragraph, then the
  sections of the earlier chapters of the same project, which the viewer has watched). Skim the
  earlier-chapter sections for *what they taught*; skip scene mechanics.

| key | transcript | script | PLAN.md lines to read |
|---|---|---|---|
| de10ch2 | S/tx/de10ch2.txt | P/digital-electronics/l10-state-assignment/script/ch2_sliding_ring.md | P/digital-electronics/l10-state-assignment/PLAN.md 1–213 |
| de10ch4 | S/tx/de10ch4.txt | P/digital-electronics/l10-state-assignment/script/ch4_one_hot.md | same PLAN.md 1–356 |
| pil1 | S/tx/pil1.txt | P/nst-maths/l10-deep-oscillations/script/ch1_rule.md | P/nst-maths/l10-deep-oscillations/PLAN.md 10–22 |
| pil2 | S/tx/pil2.txt | P/nst-maths/l10-deep-oscillations/script/ch2_shadow.md | same PLAN.md 10–22 and 226–361 |
| l11ch1 | S/tx/l11ch1.txt | P/nst-maths/l11-hyperbolic-functions/script/ch1_cosh_sinh.md | P/nst-maths/l11-hyperbolic-functions/PLAN.md 1–13 |
| l10ch2 | S/tx/l10ch2.txt | P/nst-maths/l10-complex-roots-logs/script/ch2_de_moivre.md | P/nst-maths/l10-complex-roots-logs/PLAN.md 1–107 and 108–184 |
| l10ch4 | S/tx/l10ch4.txt | P/nst-maths/l10-complex-roots-logs/script/ch4_logarithm.md | same PLAN.md 1–107 and 108–321 |
| l10ch6 | S/tx/l10ch6.txt | P/nst-maths/l10-complex-roots-logs/script/ch6_oscillations.md | same PLAN.md 1–107 and 108–470 |
| l12ch1 | S/tx/l12ch1.txt | P/nst-maths/l12-differentiation/script/ch1_first_principles.md | P/nst-maths/l12-differentiation/PLAN.md 1–16 |

**The viewer, for every chapter:** a Cambridge first-year with **A-level Maths (not Further Maths)**
and **GCSE physics only**, who has every earlier lecture of the course named in the Audience
paragraph and every earlier chapter of the same project. Concretely: A-level Maths has algebra,
trig identities, radians, sin/cos/tan, e^x and ln for reals, differentiation (chain, product,
quotient rules), integration, binomial expansion, geometric series, simple separable ODEs; it has
**no** hyperbolic functions, **no** complex numbers (those come from the course's own lectures), **no**
simple harmonic motion or angular frequency. GCSE physics: F = ma, weight = mg, Hooke's law
(force proportional to extension), speed/velocity/acceleration in words, g ≈ 9.8 m/s².

## Rubric part 1: idea units (verbatim from the original study; do not reinterpret)

Code each sentence (or clause, if it holds two units) with zero or more of:
- F, new formula: a symbolic statement heard for the first time in this video: an equation, an identity, a new symbolic expression the viewer must hold, or a new line of a derivation (each new line = 1 F). Re-reading an earlier formula is not F.
- D, definition: a new technical term or notation introduced with its meaning ("this ratio is called the derivative", "the modulus is the length").
- C, claim: a new mathematical or physical assertion presented as true (a property, a rule, a result, a reason why something is true), stated for the first time. Not narration about the video, not a question, not an analogy by itself, not a restatement.
- R, restatement: a sentence that re-expresses an idea already given (recap, "in other words", saying the same thing a second way, reading a picture's meaning again).
- M, motive: a sentence that gives the goal of a step or why we are about to do something ("to get rid of the sine, we...", "the question is how to...", "this is useful because...").
- Q, question to the viewer: an explicit question posed to the audience, rhetorical or real (including "pause and ponder"), plus predictions asked for.
- A worked arithmetic or numeric step counts as F only if it is a new equation line.
Be consistent; when unsure between C and R, ask "would a viewer learn something new from this sentence?"

(In these transcripts, a digital-electronics state code, a K-map group or a Boolean expression such
as "D_B = A" counts as a formula, F, like any equation.)

## Rubric part 2: novelty of each idea unit (new)

Every F, D and C gets a suffix: **`+` new to this viewer**, or **`k` known**: a recall, reuse or
re-wording of something the viewer already had *before this video* (A-level Maths, GCSE physics, an
earlier lecture or an earlier chapter, as above). Anything first met in this video is `+`, including
lines derived here from known pieces and numeric values of functions defined in this video. Numeric
values of functions the viewer already had (sin 30° = ½, e ≈ 2.72) are `k`. "Last time, we showed
X" is `Ck` (or `Fk`). R, M and Q take no suffix. Hyperbolic functions are `+` (Further Maths).

## Rubric part 3: jumps (new)

A jump is a place where this viewer must do unstated work to follow the argument, or must accept a
move without knowing why it is made. At most one jump per sentence, with its type(s):
- **`s`, non-atomic step.** (a) A new line or result that follows from what is on screen and just
  said by **two or more** elementary operations (substitute, expand, collect, cancel, apply one
  identity or one rule, solve one linear equation, take one limit…) whose intermediate is neither
  said nor shown (check the visual brief). Test: could this viewer verify it in a few seconds of
  thought? (b) A derivable result (a formula, a solution, a consequence) asserted with no reason or
  derivation, which the chapter then builds on, including "we'll take that as given". It is not a
  jump if the reason or derivation follows within the next ~6 sentences or the same scene ("But why
  does this work?…"). Plain facts of the world, definitions and conventions, stated as such, are not
  jumps; nor is anything the viewer already had (`k`).
- **`m`, unmotivated move.** The narration makes a choice the viewer couldn't predict (a
  substitution, a trick, a new construction or object, a particular rearrangement, a new case, a
  change of direction), and nothing in this sentence or the three before or after says why *this
  move* should help: a goal it serves, a question it answers, or why it works. An overall chapter
  goal is enough only when it makes the move the obvious next thing. Obvious next moves (divide to
  isolate, substitute the value just found, apply the rule just stated) never count. A question posed
  just before ("What happens if the exponent is real?") counts as the reason for the move that answers it.
- Both at once: `sm`. If the narration explicitly flags the skip ("we'll take that as given", "I'll
  skip the algebra"), append `f` (e.g. `sf`): still a jump.
Put the jump on the sentence where the viewer is asked to accept the result or make the move.

## Anchors (codes fixed by the study lead: match this standard)

| sentence | units | J | why |
|---|---|---|---|
| l10ch6 S014 "For small swings, it rocks back and forth with an angular frequency, omega, equal to the square root of G over L…" | D+ F+ | sf | ω = √(g/L) asserted; S015 "We'll take that as given" |
| l10ch6 S017–S018 "Then the displacement always has this form. / It's a real constant times the cosine of omega T, plus another real constant times the sine of omega T." | S017: none; S018: F+ | S018: s | general solution asserted, never derived, then built on |
| l10ch6 S020 "This is called simple harmonic motion." | D+ | | |
| l10ch6 S033 "In symbols, the displacement is the real part of this turning arrow." | F+ | | justified at S039–S043 |
| l10ch6 S042 "Eye times eye is minus one, so the two imaginary pieces multiply to give a real term, minus beta times the sine of omega T." | F+ | | one operation, said |
| l10ch6 S071 "Do it twice, and you multiply by eye omega twice, which is minus omega squared." | F+ | | one step from the rule just stated |
| l10ch4 S083 "Here it's zed, plus two pi eye N." (log of e^z) | F+ | s | needs modulus and argument of e^z, then the log formula: unspoken |
| pil1 S022 "Force equals mass times acceleration, so you divide the force by the mass." | Fk | | GCSE |
| pil1 S035–S036 "…the pull is proportional to the stretch. / That's Hooke's law, from GCSE physics." | S035: Ck; S036: Dk | | GCSE |
| pil1 S040 "So the pull is minus the stiffness K, times ex." | F+ | | new signed line; sign shown at S038–S039 |
| pil1 S045 "So the move here is: name the force that pulls back, then let Newton turn it into an acceleration." | M | | |
| pil1 S050–S051 "Call it omega squared. / It's written as a square for a reason part two makes clear." | S050: D+ | S050: mf | why a square is deferred to part two |
| pil1 S117 "…so its distance along the arc is L times theta, with theta in radians." | Fk | | A-level arc length |
| pil1 S118 "The length L is fixed, so differentiate twice: the acceleration along the arc is L times theta double dot." | F+ | | one operation, reason given |
| l11ch1 S004–S005 "Now lift out every eye. / What stays is E to the ex, plus E to the minus ex, all over two." | S005: F+ | S004: m | no reason given for removing the i |
| l11ch1 S069–S070 "Here's the trick from the notes. / Put zed equal to eye times ex, where ex can be complex too." | S070: none | S070: m | goal stated (S066), but not why this substitution |
| de10ch2 S036–S037 "…one in just two states, 000 and 001. / They sit side by side, so they make a pair, and the input to flip-flop A is not bee and not see." | S036: C+; S037: F+ | | K-map pair, one step, shown |

## Output

One file per chapter: `S/codes/<key>.<coder>.json` (your coder id is in your prompt), written as
soon as that chapter is done:
```json
{"key": "pil1", "coder": "c2", "sentences": [
  {"i": 1, "u": ["C+"], "J": "", "why": ""},
  {"i": 2, "u": [], "J": "", "why": ""},
  {"i": 3, "u": ["F+", "Ck"], "J": "s", "why": "s: two steps unspoken; Ck: L9 polar form"}
]}
```
One object per transcript sentence, in order, none skipped. `u` holds tokens from
`F+ Fk D+ Dk C+ Ck R M Q` (repeats allowed: two new derivation lines = `["F+","F+"]`). `J` is
`""`, `"s"`, `"m"`, `"sm"`, optionally with `f`. `why` (≤ 15 words) is required whenever `J` is
set or any unit is `k`; else empty. Validate each file with
`python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); print(len(d['sentences']))" <file>`
and check the count equals the transcript's line count.

**Calibrate first:** code the first 3 minutes of your first chapter, re-read those codes against
the rubric and the anchors, fix them, then go on at that standard. Code chapters in the order given.

**Reply** in ≤ 8 lines: per chapter, the counts of F+D+C, of those marked `+`, of R, M, Q, and of
jumps (s / m); then one line on the hardest recurring judgement call.
