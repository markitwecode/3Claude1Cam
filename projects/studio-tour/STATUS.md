# How These Videos Are Made: status

2026-10-27: project created; planning.

## Chapter 1 · From a request to a finished video (ch1_pipeline)
2026-10-28: **done**, fix pass after Gemini `vk listen 1` / `vk review 1`, re-finaled. Video `out/ch1_pipeline.mp4`,
12.1 min (727.0 s), 1920×1080, 60 fps (ffprobe).
Music: music/ch1.json (Machinery under the hook, Resonance under c1.voice.1, The 3Blue1Brown
Experience under the recap and end card); no overlap with ch2's tracks.

Narration rewritten for the ear and re-voiced (check these by ear):
- c1.crew.3: "…and never the code of a scene." (was "never scene code", heard as "seen code")
- c1.script.2: "…a named spot an animation can wait for." (was "a single cue word", heard as "keyword"); "the writers start on their scripts" (re-voice heard "skip writers")
- c1.dir.1: "It fixes any narration that was flagged," (was "fixes flagged narration", heard as "flag")
- c1.dir.2: "Two at once cuts the wall time roughly in half" (was "halve", heard as "have")
- c1.build.1: "Inside the builder for our running example," (was "tracing append", heard as "a pen")
- c1.build.4: "renders a quick, low-resolution preview" (was "four-eighty p", heard as "40p"); "This tile is the answer cue in trace two, forty seconds in," (was heard as "traced to")

Fix pass (Gemini-only findings, re-voiced, then `vk listen 1 --only` clean unless noted):
- c1.crew.3: "one Man-im file" (Manim heard "May-nim"); "It reads only reports, the plan, the status file and what vee-kay status prints, never the code of a scene." (vee-kay heard "bee-kay")
- c1.script.1: "and one Man-im file." (heard "May-nim")
- c1.voice.1: "It breaks our example clip into its five sentences." (trace heard "trees"; "splits" then heard "sputs")
- c1.voice.4: "so our clip's sentence starts and marks land on a timeline." (trace two's heard "trees two"; keeps s4's phrase cues "sentence starts"/"marks land"). Gemini still hears "clip's" as "clip", "a" as "the": accepted, meaning intact.
- c1.review.4: "A tool called eff-eff-probe checks the result." (was sentence-initial "Eff-eff-probe", heard "effort probe")
- c1.sync.1 not changed: the narration says "The clip's until method", heard as "clips until", which is right; Gemini expected "see dot until" from the on-screen `c.until`.

Glitches (ch1_s2_crew, c1.crew.4 > agents; confirmed with frames from the final, both fixed by a fresh builder):
- ~85.5 s scene time (final 125.6–126.0 s): faint "Opus" badges floating through the tree, a lone one at the top right above chapter-director and one under script-writer. Cause: `LaggedStart(FadeIn(tag, shift=0.2*DOWN) …)` on tags at hand-picked spots, two of them far from their boxes. Fix: tags anchored to their boxes, `GrowFromCenter` in place.
- ~87.5 s (final 127.2–127.6 s): ".claude/agents/" page fading in over "continue <project>" still on screen. Cause: one `self.play(FadeOut(prompt, vks, states), FadeIn(legend, shift=0.2*DOWN))` cross-fading overlapping text. Fix: FadeOut alone (0.7 s), then a plain FadeIn of the legend at its final spot.
- s2 also lost a stale `wait_until("the plan")` that the new crew.3 text made match earlier; `scenes/*.py` now appears right after the reading list (dwell 3.8 s of 4.9, accepted like the other dwell notes).

Open after the re-final's `vk review 1` (one round only, not fixed; checked against frames 0.5 s after each time):
- Real mid-transition overlaps (unflagged in the previous review, present before): s2 crew.3→crew.4 (final ~108.5 s), the reading list and conveyor fade out over the tree growing back, "PLAN.md" across chapter-director, ~1 s; s5 dir.3→dir.4 (~361.5 s), the director tree fades in over the music cue sheet; s4 voice.3→voice.4 (~288.5 s, mild), the flagged-lines/director diagram still up as the timeline line draws. Likely cause each time: FadeOut and FadeIn in the same play. Fix: clear first, then bring in.
- Not glitches: s2 ~111.5 s "ghost under the one checkpoint" is STATUS.md fading in on {state}; s2 ~131.5 s red X on CLAUDE.md is the brief's strike; s4 ~245.5 s faint text above the waveform is the voice boxes mid-fade.
- Mismatches accepted by brief: s4 timeline has no {pause} pin (brief lists five pins); s6 "empty last frame" labels the rule the narration describes.
- Pronunciation, Gemini-only (not in `vk listen 1`/Whisper): c1.dir.3 "N-rev" → "on-rev" (the ear rule's spelling); c1.recap.1 "renders" → "menders"; c1.sync.1 "see until" (not in the text, false).

Accepted voice QA flags (meaning intact): Mac's/max (crew.2, voice.1), cue/Q (sync.2), cued/queued
(sync.3, recap.1), Fix notes/Fixed notes (review.3, like "fix passes"); spelling-only: project.json
(crew.3), 1300/1800 (script.1), 15-40 (script.2), Self.say (sync.1); c1.script.3's quoted mishearing.

Accepted check flags: dwell notes in every scene (clip-boundary clears; judged on holds). Small text:
s2 c1.crew.3 shrunk, dimmed tree (the brief demands it); s6 lint-output page at Mono 19 (verbatim
120-character output, doesn't fit at the lint minimum); s8 c1.review.1 lint thumbnail at size 7 (brief:
"small"). Holds `~` on c1.build.2: the loop's dot keeps turning, as the brief asks.

Builder test (A = Opus xhigh, B = Opus medium, C = Sonnet). No builder stated its number of check
runs. Tool calls from the completion notices are given instead. Round 1 = first holds (s1–s7); round 2 =
second holds (s6, s8).

| Scene | Setting | Build (from report) | Round 1 notes | Round 2 notes | Fix passes | Final state |
|---|---|---|---|---|---|---|
| s1_hook | A | 30 tool calls; check clean | none | none | 0 | clean (dwell only) |
| s2_crew | B | 16 tool calls; render-anyway past small text | row labels at 21/25 → one size ≥ 26 with "×N" tags; "request + material" | none | 1 (9 calls) | small text on shrunk tree accepted |
| s3_script | C | 8 tool calls; check clean | raised serif tilde "~1300"; line box near bottom edge | none | 1 (2 calls, 1 check) | clean (dwell only) |
| s4_voice | A | 12 tool calls; check clean | ear icon read as "?" → headphones | none | 1 (3 calls) | clean (dwell only) |
| s5_director | B | 11 tool calls; check clean | match s2's new master-shot labels (knock-on from s2) | none | 1 (4 calls) | clean (dwell only) |
| s6_builder | C | 32 tool calls; render-anyway past small text | spoken lines cut off behind beats image (bug); packet Mono 24 and lint page 18; raised tildes; box padding | packet rows touching after fix, "…" rows gone | 2 (6 + 5 calls) | lint page Mono 19 accepted |
| s7_sync | A | 14 tool calls; check clean | margin question only (already clear) | none | 0 | clean (dwell only) |
| s8_review | B | 28 tool calls (launched after the others); render-anyway past lint thumbnail | (not built yet) | r7 vignette up 1.8 s → hold grid; restore checklist sub-labels; raised tildes; 2 margin questions | 1 (3 calls) | thumbnail accepted; recap = 7 vignettes from s2–s8 |

Continuity for ch2: master shot as in scenes/ch1_s2_crew.py (row labels 26.5, separate DIM "×N" tags
at the stacks' bottom-right, box centres as in PLAN); context bar as in scenes/ch1_s6_builder.py
(centre x −6.1, width 0.8, bottom y −3.2, GOLD 0.9 with BG separators).
Engine (resolved 2026-10-28): engine/lib now applies the Pillow 13 image fix itself; the local
`_patch_image_canvas()` shims in s1, s6 and s8 are redundant but harmless and left in place. The sync lint
now ignores text inside strings (s7's workaround stays).

## Chapter 2 · Where the tokens go (ch2_costs)
2026-10-28: **done** (fix pass re-finaled 15:14). Video `out/ch2_costs.mp4`, 12.7 min (763.5 s), 1920×1080, 60 fps (ffprobe);
narration 11.9 min plus clip gaps, holds and the ~8 s end card. Music: music/ch2.json (Fractals
under the hook, Transformation under s3's story c2.history.1–3, Orbit from c2.test.4:end under the
recap and end card); no overlap with ch1's tracks.

Narration rewritten for the ear and re-voiced (check these by ear):
- c2.history.4: "A dedicated agent type for building scenes, with its distilled kit in the cache."
  (was "The scene builder type", heard as "scene dollar/duller type")
- c2.split.2: "It re-reads two million tokens in total" (was "in all", heard as "and all")
- c2.dials.2: "Now take the same tokens and price them at Sonnet's rates." (was "same builder
  tokens", heard as "dolder tokens"); "The gold and red parts are cut in half." (was "halve", heard
  as "have")
- c2.test.3: "And how your plan compares Sonnet usage with Opus usage is not published." (was
  "weighs Sonnet against", heard as "weighs on it against")
- Fix pass: c2.hook.2 "that's over six hundred dollars, six hundred and thirty-three in total." (was
  "about six hundred and thirty-three dollars", heard as "six thirty-three" by Gemini + Whisper;
  "six hundred thirty-three" failed the same way). All three Whisper models now hear "$600, $633".
- Fix pass: c2.anat.1 "Man-im's source", c2.dials.3 "Man-im code" (was "Manim", heard as "Manam" /
  "Manium"). `vk listen --only` is clean on both; the final's review still hears "may-nim" in anat.1.
- Gemini-only, unconfirmed by Whisper (check by ear): c2.hook.2 "worse" heard as "worst" (sentence 3,
  unchanged audio); c2.turns.2 "N-rev" heard as "on-rev"; c2.dials.1 "judgment" heard as "judgema".
Accepted voice QA flags (spelling or homophones, meaning intact): dollar and percent figures
($633, $278, $3.15, 3–5%, "2.3 to 3.8 million"), cache/cash, writes/rights, guessed/guest, fix/fixed
passes and notes, "check-clean" heard as "checked clean", "and in cache writes" heard as "and then
cash rights" (c2.test.5).

Accepted check flags:
- ch2_s4 overlap at [c2.split.5 > same] ('scene 1' overlaps 'scene 2'): the brief asks for the two
  scenes' tiles to tangle at {mix}; s4's last two passes ran with --render-anyway for it.
- Dwell flags only elsewhere, mostly 3–4.5 s against a 4.5–6 s rule of thumb where the next clip
  needs the space. The shortest: s2 "thinking" label 2.8 s by the audit (the builder measures
  ~3 s), s4 "mostly one early session" 3.9 s, s1 title lines ~3.3 s.

Fix pass (2026-10-28, from vk listen/review 2 + producer): s4 split.1 "≈ 10%" brace now spans
planner, writer and director with their $ labels (off-centre tip at x −4.4, "$9"/"$17" raised 0.16).
s5 tile-group labels checked against the narration (~13 shell, ~9 lookup, ~2 patch): correct, no
change beyond the fade order below. s7 ~54 s "green failed idea": not real (the green cards are
the adopted column; rejected cards turn RED on their words). New dwell flag accepted: s6 caveat
"transcripts may undercount…" 5.7 s of 6.5 (it now clears with the rest at c2.dials.4).

Glitches (scene, time, what it looked like, cause):
- s2 ~72 s, "per million tokens" rotated along the box edge: not reproduced (frames 70.6–73.0); a
  "$0.20" copy flying over the Opus "$0.20" reads "$0.$020" at 72.6 s for a moment. Accepted.
- s5 ~30.3 s, "∼13" count slid past the still-visible "Write" name: the row names faded 0.4–1.1 s
  into a 1.8 s shrink-and-move. Fixed: names/brace fade 0–0.6 s first.
- s5 ~41.5 s, stray GREEN square: TransformFromCopy of the Write tile flying ~9 units across the
  empty middle into the "writes and patches" segment. Fixed: segment grows from the bar, flashes
  on the tiles in place.
- s6 ~52.4 s, stray RED "e^-x": the "extra check runs" label caught half-faded as "ex" by
  FadeIn(..., lag_ratio=0.3) over letters. Fixed: LaggedStart over whole lines.
- s6 ~52.8 s, "$15€": ReplacementTransform "$159" → "≈ $278". Fixed: fade out, then fade in.
- s6 ~64.8 s, caveat lingering into c2.dials.4: clear() kept it (keep=[cav]) until {safe}. Fixed.
- s7 ~66.9 s and ~72.3 s, scrambled reason text: ReplacementTransform between unlike reason texts.
  Fixed: fade out, then rise in.
- s7 ~89.0 s, list item 1 over the green card: FadeTransform(card, item) stretching the two into
  each other (items 2 and 3 too). Fixed: card shrinks into the item's number, then the item fades in.

Still flagged by `vk review 2` on the re-final (all mid-transition, none confirmed, one-round limit):
s2 76.8 s stray red "$200" over "$20"; s3 7.1 s ch5 box cut at the right edge, 33.1 s "6–11M per
scene" over the mini bars, 50.1 s two image icons left over; s4 3.4 s builder and older-agent
labels at the same spot, 103.4 s "late fix notes" over the time graphic; s5 38.2 s a duplicate tile
row flickers; s8 86.7 s labels linger into the recap.

Open (accepted at the two-round limit):
- s6's mini master shot (dials.1, dials.4) is a simplified tree (no "you", no vk voice); s6 isn't
  one of the master-shot scenes in PLAN.md.
- s5 uses "∼" (U+223C) for "about" counts; the other scenes use "≈".
- Cross-chapter: s1, s4 and the s8 recap copy ch1_s2_crew.py's master shot (ROW 26.5, separate
  ×N tags); s2 opens on ch1_s6_builder.py's exact box and bar (fill 0.9, stroke 3, checked after
  ch1's 01:20 change); s3's bars and s4's split.2 bar use the same styling.

### Builder test (A = Opus xhigh default, B = Opus medium effort, C = Sonnet)
Check runs are from each builder's own reports. Fix passes were SendMessage to the same builder.
Many round-1 notes were continuity, not quality: builders s1–s7 started in parallel, before any
shared visual existed (ch1 was being built at the same time), so most copied nothing and had to be
aligned afterwards. Notes are tagged (q) quality or (c) continuity.

| Scene | Set | Check runs (build + fixes) | Round 1 notes | Round 2 notes | Fix passes | Final |
|---|---|---|---|---|---|---|
| s1_hook | C | 5 + 3 + 1 = 9 | (q) title lines up 0.9–2.9 s; (c) master shot to ch1_s2; (q) question line up 3.1 s | (c) row labels 26.5 (ch1 change) | 2 | clean, dwell only |
| s2_turns | A | 3 + 1 + 1 = 5 | (c) box and bar to ch1_s6; (q) formula at the bottom margin | (c) re-compare with ch1_s6: no change needed | 2 | clean, dwell only |
| s3_history | B | 3 + 1 + 1 = 5 | (q) "≈ 300 images" up 2.1 s; (q) end hold; (c) bar style to s2 | (c) bar style to final ch1_s6 | 2 | clean, dwell only |
| s4_breakdown | C | 2 + 2 + 3 = 7 | (c) master shot to ch1_s2; (c) GOLD bar from s2; (q) answer card up 1.2 s; (q) split.4 cued labels missing at clip end, punchline up 1.0 s; (q) split.5 "?" 0.6 s and short end hold; (q) "~" glyph | (c) labels 26.5, bar to ch1_s6; (q) split.1 left side crowded; (q) producer note up 2.2 s | 2 | tangle overlap accepted; "≈ 10%" brace left open |
| s5_anatomy | A | 3 | none | none | 0 | clean, no flags at all |
| s6_dials | B | 3 + 3 = 6 | (c) card 1 to s1's style, drop icon; (q) "~" glyph; (q) bench gone by clip end; (c) thinking segment from s5; (q) caveat outside the bottom margin | none | 1 | clean, dwell only |
| s7_second | C | 2 + 3 = 5 | (q) board didn't accumulate and adopted cards didn't slide into the list (brief); (q) four items up ~1 s; (q) overrun example wrapped mid-phrase, up 3.7 s; (q) "~" glyph | none | 1 | clean, dwell only |
| s8_test | A | 4 + 2 = 6 | (built after the others; recap as five small panels from s1/s2/s4/s6/s7 helpers) (q) next-step card at the bottom edge | none | 1 | clean, dwell only |

## Builder test results (producer, 2026-10-28)
Cost per finished scene from the builder transcripts (fix passes went to the same builder, so they are
included), at API list prices; quality notes = round-1+2 director notes tagged or judged (q), not
continuity catch-up (c).

| Setting | Scenes | $/scene median (mean) | Output tokens median | Quality notes/scene | Fix passes/scene |
|---|---|---|---|---|---|
| A Opus xhigh | ch1 s1 s4 s7, ch2 s2 s5 s8 | 2.86 (3.16) | 97k | 0.5 | 0.7 |
| B Opus medium | ch1 s2 s5 s8, ch2 s3 s6 | 1.63 (1.89) | 43k | 2.2 | 1.2 |
| C Sonnet (ran at medium) | ch1 s3 s6, ch2 s1 s4 s7 | 0.64 (1.05) | 31k | 3.8 | 1.6 |

All 16 ended check-clean. C had the chapter's only real bug (ch1_s6: spoken lines behind the beats
image) and the only brief not followed (ch2_s7: board didn't accumulate). Caveats: n = 5–6 per setting,
a fixed rotation (not difficulty-matched), the director knew the settings, and ch2's round 1 was
inflated by catch-up to ch1 (tagged c, excluded). Recurring across settings: raised "~" glyph,
elements appearing 1–3 s before their cue: glitch-study items, not builder-specific.
Builder working time (prompt to end of turn, summed over build + fix passes; medians): Opus xhigh
16.7 min first build / 17.1 with fixes; Opus medium 7.0 / 9.6; Sonnet 4.6 / 5.7. Medium is faster,
not slower: less thinking per turn outweighs its extra fix passes.
