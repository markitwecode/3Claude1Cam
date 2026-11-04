# Projects

One line per project. The producer updates it at the end of every stage. `engine/vk -C <folder>
status` gives the live file state.

| Project | What | State (updated) |
|---|---|---|
| `focs/l03-lists` | FoCS Lecture 3 · Lists: 6 chapters, 59 min | ✅ done: 6 videos in `out/`, 63 min; ear-check list in STATUS.md (2026-10-24) |
| `cross-product` | The Cross Product (Vector algebra · From geometry to components) | ✅ done: 1 video in `out/`, 11.8 min; ear-check list in STATUS.md (2026-10-25) |
| `focs/l04-more-lists` | FoCS Lecture 4 · More on Lists: 7 chapters (6 + bonus), 70 min | ✅ done: 7 videos in `out/`, 70.4 min; ear-check list in STATUS.md (2026-10-26) |
| `focs/l05-sorting` | FoCS Lecture 5 · Sorting: 7 chapters planned (~65 min) | ✅ done: 7 videos in `out/`, 72.3 min; ch3–7 built without Gemini: transitions pass + ear checks after the Wed 2026-11-04 reset (list in STATUS.md) (2026-11-01) |
| `studio-tour` | How These Videos Are Made (3Claude1Cam · A studio tour) | ✅ done + Gemini fix round: 2 videos in `out/`, 24.8 min; builder test results in STATUS.md; 3 confirmed transition overlaps in ch1 + 8 unconfirmed in ch2 left for the glitch study (2026-10-28) |
| `digital-electronics/l06-flip-flops-counters` | Flip-flops and Counters (Digital Electronics · Lecture 6) | ✅ done: 6 videos in `out/`, 61.3 min; Gemini leftovers in STATUS.md (2026-10-28) |
| `digital-electronics/l06-flip-flops-counters-codex` | Flip-flops and Counters (Digital Electronics · Lecture 6) | done: 6 videos, 58.4 min, 1080p60; 19 matched comparisons + 5 retests, mixed preferences (benchmark/SUMMARY.md); original preserved (2026-10-30) |
| `digital-electronics/l06-flip-flops-counters-astra-ch1` | Astra builder-only test · Lecture 6 Chapter 1 | video complete and frozen: 9:12, 1080p60, Astra medium; blind comparison running (2026-10-30) |
| `digital-electronics/l08-timing-metastability` | Timing, Metastability and Parallelism (Digital Electronics · Lecture 8) | ✅ done: 7 videos in `out/`, 62.6 min; Gemini leftovers + accepted flags in STATUS.md (2026-10-31) |
| `digital-electronics/l10-state-assignment` | State Assignment (Digital Electronics · Lecture 10) | ✅ done: 6 videos in `out/`, 63.1 min; Gemini leftovers in STATUS.md (2026-11-01) |
| `digital-electronics/l07-lab-shift-registers` | Hardware Labs and Shift Registers (Digital Electronics · Lecture 7) | ✅ done: 2 videos in `out/`, 22.2 min (ch1 12.5, ch2 9.7); Gemini leftovers in STATUS.md (2026-11-01) |
| `digital-electronics/l11-state-minimisation` | State Minimisation, Programmable Logic and Circuits (Digital Electronics · Lecture 11) | ✅ done: 6 videos in `out/`, 62.0 min; Gemini leftovers in STATUS.md (2026-11-01) |
| `nst-maths/l10-complex-roots-logs` | Powers, Logarithms and Oscillations (NST IA Mathematics · Lecture 10) | ✅ done: 8 videos in `out/`, 80.7 min; ch8 final review skipped (Gemini quota), see STATUS.md (2026-11-01) |
| `nst-maths/l11-hyperbolic-functions` | Hyperbolic Functions and Conics (NST IA Mathematics · Lecture 11) | ✅ done: 7 videos in `out/`, 74.4 min; ch4–6 final reviews skipped (Gemini quota), see STATUS.md (2026-11-01) |
| `databases/l04-subqueries-documents` | Subqueries and Documents (Databases · Lecture 4) | ✅ done: 10 videos in `out/`, 111.1 min (8 + 2 bonus; part 1 re-paced with `vk regap 1 --scale 2`, 12:20, 2026-11-03); built without Gemini: transitions pass + ear checks after the Wed reset (lists in STATUS.md); part 4's motion contact sheets were never made (2026-11-02) |
| `databases/l05-graphs` | Graph Databases (Databases · Lecture 5) | ✅ done: 6 videos in `out/`, 64.4 min (5 + bonus); built without Gemini: transitions pass + ear checks after the Wed reset (lists in STATUS.md) (2026-11-01) |
| `nst-maths/l12-differentiation` | Differentiation (NST IA Mathematics · Lecture 12) | ✅ done: 7 videos in `out/`, 85.7 min (6 + bonus); built entirely with Gemini off (no digest, listens, scene or final reviews): full listen queued in "Pending" below (2026-11-03) |
| `nst-maths/l10-deep-oscillations` | Oscillations, deep-style pilot (NST IA Mathematics · Lecture 10 §2.6) | ✅ done: 4 videos in `out/`, 58.4 min (15:00, 17:12, 12:29, 13:42), 2560×1440 60 fps, all clean; ~158M ctx tokens over 47 agents; the user loved it; deep style's model (2026-11-04) |

Courses: `focs/COURSE.md` (Foundations of Computer Science, 11 lectures); `digital-electronics/COURSE.md`; `nst-maths/COURSE.md`; `databases/COURSE.md`.

## Pacing (house default since 2026-11-03: varied pauses, twice as long)
New projects get it from `vk voice`. Older projects have the old fixed pacing until re-paced on request:
`vk -C <project> regap N` per chapter, then `vk finalize N… --no-review`. Update this list when you do.
- Re-paced (re-rendered files carry a green Finder tag): `databases/l04-subqueries-documents` ch1;
  `nst-maths/l10-complex-roots-logs` ch1–8, `nst-maths/l11-hyperbolic-functions` ch1–7,
  `digital-electronics/l10-state-assignment` ch1–6, `digital-electronics/l11-state-minimisation` ch1–6
  (all re-rendered clean 2026-11-03: maths L10 95.5 min, L11 89.2; DE L10 75.0, L11 73.9).
- Not yet (user's call, 2026-11-03: "just these for now"; DE up to L8 already watched): databases L4 ch2–10,
  databases L5, digital-electronics L6–L8, focs, cross-product, studio-tour.

## Teaching styles (2026-11-04): auto by default, deep on request
The user loved the deep pilot (`nst-maths/l10-deep-oscillations`, 58.4 min). New projects are `"style": "auto"`:
the lecture's structure, enhanced at every gap. `--style deep` gives the pilot's first-principles rebuild. Both
use the 1440p board, named moves and think-stop questions. Spec: `docs/DEEP_STYLE.md` §0. Projects made
before today keep the classic style. The widgets are in `engine/lib/teach.py` (tested at 1440p, documented for builders).
The first auto lecture will measure the real length and cost.

## Done 2026-11-04: re-voiced the lines Gemini heard wrong
The fixes were confirmed by one Gemini re-listen per chapter, and all 11 chapters were re-finalized clean:
databases L5 ch5–6, L4 ch2, 3, 6, 7 and 8, nst-maths L12 ch1 and 6. Details are in each STATUS.md.
Left open (small): databases L4 c8.text.1 and c9.pairs.3 still say "semijoin" without a hyphen. They are
probably heard "semi one" too, but no listen sampled them. And L4 ch3 s6's "movies 2,935" label now
appears 2 s before its word (an advisory).
