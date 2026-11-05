# Hyperbolic Functions: status

2026-11-01: project created; planning.

## Producer notes for chapter-directors
- Gemini quota low (2026-11-01, ~20% left for 2 days): ONE round of `vk review` per scene, no
  round 2; `vk listen --only` only for lines Whisper also flags.

## Continuity review (2026-11-01, ch1–7 scripts)
Narration is 11,575 words, ~72 min (ch1 9.2, ch2 9.9, ch3 11.0, ch4 10.7, ch5 11.1, ch6 10.9,
ch7 9.4). Coverage matches PLAN.md; the "last time" / "next time" chain holds (ch6 s3 delivers ch5's
"why hyperbolic" promise, and so do c6.param.4 and the recap). No ids, marks or stems were changed.
- Cross-references: "part N" everywhere (the title cards' word). "Chapter" is reserved for the notes'
  chapters. ch7's G2 sub-parts are now "the first/second curve". Changed lines: c1.family.4, c4.cases.3,
  c5.hook.3, c5.param.4 (also no longer a near-copy of hook.3), c6.hook.2, c6.param.1, c6.param.4,
  c6.hints.1, .2, .5, c6.recap.2, c7.intro.1, c7.g1.2, c7.g1.5, c7.g2.1, .2, .3, .5, c7.g3.4,
  c7.g4.5. Kept: the voiced "this chapter" in c1.hook.4 and c2.hook.3 (no number, so it can't be misread).
- Capital A before a word ("cosh of A plus B"): now "the cosh of the sum, A, plus B", then "the cosh of
  the sum". Lines: c2.add.1–4, c2.list.1, .2, c2.rule.4, c2.tanh.1, .3, .4, c2.recap.1, c6.class.2.
  Most ch2 lines were already voiced and will be re-voiced. The A in "of A plus" lasted 0.14–0.16 s in
  c2.add.1/2, about as long as the article.
- "halves" removed: c1.def.5, c1.family.1, c3.cosh.1, c3.cosh.2, c3.odd.1.
- Scope and teaser: c7.g4.2 ("the log of the ratio, one plus ex, over one minus ex", as ch3 says it);
  c4.recap.3 (circles and ellipses first, then hyperbolas).
- Briefs: i PINK everywhere (no other colour for i anywhere). ch4 s6's Im label is PINK, and its
  ln(2 + √3) height stays TEAL (cosh⁻¹ 2); ch5 s1's lattice callback now matches ch4 s6. ch7's reused
  visuals checked against ch2 s4/s5, ch3 s3/s5/s6, ch5 s4/s5 and ch6 s2/s3/s7. Colours added for the
  ±1 asymptotes (GOLD/PURPLE) in ch7 s2 and s5, and dim-white asymptotes in s3. On-screen labels
  "next chapter" / "bonus chapter" are now "Part 6" / "Part 7 (bonus)". ch7's end label reads
  "Chapter 4 of the notes".
- Voice forms (shine, tanch, zed, E to the ex, eye, log, inverse cosh) are applied the same way in
  all chapters. The two sentences that start with "Why" (c4.fta.2, c6.hook.2) use it as the question
  word, not the variable. QA on ch2 already shows "cosh" transcribed as "cos"/"caution" (c2.hook.2
  consensus): ear-check before rewriting, as PLAN.md says.

## Chapter 1 · Cosine without the i (ch1_cosh_sinh)
State: ready for final (director, 2026-11-01). Preview: out/ch1_cosh_sinh_preview.mp4. Scenes 7/7
(Opus scene-builders), ~9.7 min. Music: music/ch1.json (Euler's Clock hook, Orbit under the s2 graph
sweep c1.def.3–4, Focal Point recap + end card).
Shared builders (import with load_scene) for later chapters: ch1_s1_hook cos_sin_pair(),
circle_hyperbola_pair() (labels are now groups, formula at .tex); ch1_s2_define graph_axes, exp_curve,
emx_curve, cosh_curve, sinh_curve, SINH_C, x_marks, exp_graph; ch1_s3_family family_card(),
card_headers(), inverse_card(); ch1_s4_cosix dictionary_card(rows, full) (the dictionary card);
ch1_s6_dictionary part2_formula(). Handovers: s4→s5 and s5→s6 (the dictionary card, top-right).
Voice (first maths-readings run): `vk voice 1` re-voiced c1.family.1, c1.family.4 and the unvoiced line.
- Readings that work: "shine", "cosh", "tanch", "zed", "E to the (minus) eye ex", "eye". Whisper's
  flags on them are false: "shine"→"sine" (3/3 models, 10 sentences), "cosh"→"cache/Cauchy/caution/cos",
  "tanch"→"tinge". Gemini (`vk listen 1 --only` the 9 flagged lines) heard all of them as written.
  Acoustic check of every token in ch1's clips (spectrum of the fricative): all 21 "shine" onsets
  are "sh" (centroid ~3.2 kHz, 2–4.5 kHz band +10 dB over 5–11 kHz) against "sine" (~6.3 kHz,
  −14.6 dB); all 28 "cosh" and 9 "tanch" endings are "sh"-like (+12 / +9 dB, never below +5.7)
  against word-final "s" in "this"/"is" (−11 / −6 dB). Accepted: every shine/cosh/tanch QA flag.
- Rewritten (Gemini-confirmed): c1.dict.3 "where you'll solve cosine of zed equals two" (heard
  "saw", +qa) → "where you'll find every zed whose cosine is two"; c1.def.4 "Slide along" (heard
  "alon", clip start) → "Now slide across"; c1.sinix.5 "Divide sine … by cosine …" (voice inserted
  "the") → "Divide the sine of eye ex by the cosine of eye ex". All three pass `vk qa 1`.
- Accepted: c1.recap.3 "with the plus" → "with a plus" (same meaning); c1.family.2 "cosh" → "kosh"
  (Gemini, spelling only).
- Scene reviews (one Gemini round, s1–s7), pronunciation, all accepted: s5 "tanch"→"touch"/"tee anch"
  (87.7, 91.3 s), s4 "cosine"→"kusine" (77.6 s) and "one and point five four", s6 "sine"→"signed".
  All three Whisper models transcribed those exact words as written (the coined "tanch" included),
  so these are Gemini-only false hearings; no re-voice.
Review: round 1 Gemini + holds → fix passes s1, s3, s4, s6, s7; round 2 holds → s3 box margin. No
Gemini round 2 (quota). Fixed: title card lines arrive together (3.3 s each, was 1.1 s); hyperbola
label clear of the y-axis (background card); s3 orphaned "undoes cosh / built from ln" lines fade with
the card; s6 "read backwards" tag replaces the arrow from (92); s6 Part 4 preview shows cos(x + iy)
splitting, with cos z = 2 on "That's Part four"; s6 check block raised; s7 recap panels fade on {next}
(no unreadable dimmed strip), end card centred; s3 notes box padded and raised.
Accepted: dwell advisories (brief-driven clears: title 3.3 s, hook end tags, s2 labels, s3 tanh 1 and
exponential tanh, s5 boxed (92) 2.7 s before the handover card, s6 check values); FlashAround advice
(s3 line 193, s5 line 136); the + fading out mid-swap in s4 (by design).
Glitches (for the glitch study):
- s1 44.6 s (c1.hook.4): both running dots off their curves during `ch.animate.scale(0.75).move_to(…)`;
  position updaters ran on .animate's hidden copies and aimed at the previous frame's curve. Fixed
  (updaters act only on the on-screen dots).
- s3 41.2 s (c1.family.3 start): "cosh"/"shine" speech labels left alone at the top after their
  definitions faded; cause: lagged `sweep_clear` faded definitions before labels. Fixed (one play).
- s4 63.6–64.3 s (c1.cosix.4): empty YELLOW box left in the centre while the boxed formula shrank into
  the card; cause: FadeOut(box) in place while its content flew away. Fixed (box rides with it).
- s7 15.0–15.5 s ({r2b}): a lone RED "]" after "1/cosh x"; cause: FlashAround(time_width=1.5, 1.2 s)
  is fully drawn for only ~0.2 s, leaving one edge. Fixed (a RED box fades in and stays).
- After `vk finalize 1` (transitions, s3 62.8 s "rings miss coth"): coth's ring is there at final
  248.9 s (staggered rings; Gemini sampled 248.4 s, before coth's turn), but every ring sat ~half a
  glyph right of its h, covering the x ("h x"). Fixed: a YELLOW 1.3× colour pulse of the h glyph alone
  (nine targets). The same pass cleared a blocking overlap flag at c1.family.1 line 172 (copies flying
  off the definitions over the cosh line): copies now appear just under their definitions, then fly
  into tanh. Chapter check clean, handovers ok, preview re-rendered (9.7 min). Back to ready for final.
- Not glitches (checked on frames): s1 10 s flash targets; s3 {letter} rings (all on hyperbolic h's,
  denominators included); s4 39.2–39.5 s exponent gap (mid-`edit`, dropped −i² fades first); s6 63 s
  "tears" (thin DIM strokes at 20–30 % opacity in the final fade, plus compression); s7 {extra}.

## Chapter 2 · Identities and the sign flip (ch2_identities)
State: ready for final (director, 2026-11-01). Preview out/ch2_identities_preview.mp4, 10.4 min (621 s),
plays end to end; handover s3 → s4 ok (0.00% differ). Music: music/ch2.json (Resonance hook, Transformation
under c2.pythag.4's compare + circle/hyperbola picture, Endpoint recap + end card).
Voice: `vk voice 2` re-voiced the 11 continuity-review lines; narration 24/24, 9.8 min.
- Rewritten (Whisper medium agreed, meaning changed): c2.pythag.3:5 "cosh squared of ex, minus shine
  squared of ex" (heard "square root of") → "cosh squared, minus shine squared, equals one" (passes);
  c2.pythag.4:3 and c2.list.3:1 commas around "minus shine squared"; c2.add.3:2 "eye times shine of"
  → "eye, times the shine of".
- Rewritten (Gemini `vk listen 2`, high confidence): c2.hook.2:2 "says that cosine" (heard "tosine")
  → "says cosine"; "tanch" heard "tant"/"tonch" in c2.list.3:4, :6 and c2.tanh.3:2–4 → small rewrites
  ("gives tanch squared", commas, "turns into a tanch", "So the tanch of the sum", "it has one").
  Not re-listened (producer's Gemini rule: Whisper doesn't flag them); they pass `vk qa 2`.
- s6's scene review then still heard "tanch" as "tangent" (c2.tanh.1 @4 s, c2.tanh.3 ×4), so a plainer
  rewrite: "the hyperbolic tangent of the sum" (tanh.1 {find}, tanh.3 {answer}), "turns into a
  hyperbolic tangent" (tanh.3 {ratio}); and c2.tanh.4 "Part seven solves it" (heard "softs it") →
  "Part seven finds a third way, using the exponentials". All pass `vk qa 2`. Open question for the
  producer: Gemini hears "tanch" as "tant"/"tonch"/"tangent" in some ch2 takes (ch1's ear checks passed).
- Accepted Whisper flags (Gemini heard them as written; ch1's acoustic check found the same flags
  false): "shine"→"sine" (c2.pythag.4:3, c2.add.3:2, c2.list.3:7), "cosh"→"cos/caution" (hook.2:4,
  list.2, list.3, rule.2, tanh.3, recap.2), sine/sign and eyes/i's homophones (add.3, list.2,
  rule.2–3, tanh.1–2), "routes"→"roots" (hook.3, British reading), "round"→"around".
- Accepted Gemini-only: c2.list.2:6 "the difference" → "a difference" (same meaning).
- Plan: the dictionary card docks top-right in s1, s3 and s6 only (each fades it in and out; the
  other scenes stay card-free so every scene can end empty). s3 → s4 is a handover (s3's boxed
  cosh(A + B) becomes s4's row 1).
Scenes: all 7 built (Opus builders), one Gemini `vk review` round, one fix round on all 7.
- Fixed: s1 title card held 4.5 s (was 1.9); s2 hyperbola drawn from its vertex, circle's finished
  dot dimmed, working raised off the bottom edge; s3 one ring on the sign (not a box + ring);
  s4 list enlarged to size 34 and spread, (93) relabelled to z on {squares}, i's joined into one
  equation and struck on both sides, tail cut to ~3.75 s; s5 Osborn caption held through the shrink;
  s6 re-synced to the new narration, flashes row 2 on {why}, takes s5's prediction_shot(); s7
  captions are panel titles ("expanding the definitions", "a plus underneath"), r1's circle/hyperbola
  on axes, r4 larger.
- Accepted: dwell advice on working steps that are rewritten in place (s2 ½→¼, s3 line rewrites,
  s4 workspace terms, s5 test steps, s6 fraction swaps); title card 4.5 s of the 6.3 s the metric
  wants (holding longer would make the PINK i flash late); s3 quote 4.3 s (spoken as the scene ends);
  s7 r4 dwell (recap of s6); s2 flashbox advice on (84)/(85). Brief-mandated: s1 uses x in the
  identity and θ on the circle, a cosh-only "definitions" panel and an empty "hyperbolic twin" card.
  Gemini claims not confirmed on frames: s2 @47 s (ring on the minus beside a bracket), s2 @57 s
  (no overlap), s4 @69 s (the child's − is the YELLOW one; parent brighter mid-swap). s3 "plus" →
  "plust" (Gemini, medium, spelling only).
- Glitches (for the glitch study):
  - s1 @19 s: a right-angle mark at the circle's centre; `Create(hyp)` and `Create(leg_c)` in one play
    grew from the same point. Fixed (triangle drawn as one path).
  - s1 @26 s: an orange bracket beside sin θ; FlashAround on the cos θ / sin θ labels left bracket-shaped
    strokes as it faded. Fixed (label flashes removed).
  - s2 @95 s: two green fragments at the bottom; `Create` on each hyperbola branch started from its
    bottom end. Fixed (branches grow out of the vertex).
  - s3 @33 s: "cos(i(A + B)))" for a moment; `edit()` slides the shared ")" while the new brackets fade
    in. Accepted (correct from 33.3 s).
  - s4 @40 s (builder's note): mid-join, the `edit` keeps the shared "sin", so it briefly reads
    "sin (A + B)". Accepted.
- Finalize (vk finalize 2, verdict "look"): ch2_s7_recap @1.4 s "header 'expanding the definitions'
  doubled with a blurry copy" is not real. Frames of out/ch2_identities.mp4 at 575.9–576.75 s are
  empty, 576.9 s shows the header fading in (one copy), and 577.05/577.2/577.5/579.0 s show one sharp
  copy. The fade-in briefly crosses the panel's top border; there is no second copy. No fix pass.

## Chapter 3 · Graphs and inverses (ch3_graphs_inverses)
State: ready for final (director, 2026-11-01). Preview out/ch3_graphs_inverses_preview.mp4, 11.0 min
(657 s), plays end to end; handovers s2 → s3 ok (0.10% differ), s3 → s4 ok (0.00%). Chapter check: no
blocking flags (dwell advisories only, listed below). Scenes 7/7 (Opus builders).
Music: music/ch3.json (Centroid hook to c3.cosh.1, Fractals
under the Figure 25(d) / line-test stretch c3.odd.4:end → c3.arsinh.2, Gnomon recap + end card, swell
after c3.recap.3).
Voice: re-voiced 3 lines by the COURSE.md rules (narration 31/31, 10.4 min), all pass `vk qa 3`:
c3.artanh.1 "no quadratic to solve" → "no quadratic at all"; c3.recap.1 "Let's recap" → "Time for a
recap", "and solve for the exponential" → "find the exponential, then take logs"; c3.recap.3 "we solve
cosine of zed equals two" → "we find every zed whose cosine is two", and "finding all of them takes"
→ "every one of them comes from" (no second "find").
- Accepted Whisper flags (known false, COURSE.md / ch1's acoustic check): "cosh" → Kosh/Cauch/Cache/kash
  (hook.2, cosh.1 ×2, cosh.3 ×2, odd.2 ×4, odd.3), "tanch" → "tinge" (recap.1), homophone "roles" →
  "rolls" (cosh.3). Minor: cosh.4 "And a" → "In a", artanh.2 "Divide, and" → "Divide an". No `vk listen`
  (producer: only for lines Whisper flags beyond the known-false ones; none).
Plan: handovers s2 → s3 (cosh_figure) and s3 → s4 (s4's fig25d_shot(), built first so s3 ends on it);
other joins fade to empty. Waves: s1 + s2 + s4, then s3 + s5 + s6, then the recap. (Wave 2's builders
died on a DNS outage at start and were resumed; Gemini failed studio-wide in the same minutes with
"invalid model selection", and a single retry worked.)
Shared (load_scene): ch3_s2_cosh fig_axes(), FIG_CENTER, cosh_figure(), handover_shot(),
half_exp_curve/half_emx_curve/half_label/zero_dot; ch3_s4_arsinh fig25d_shot(), check_card(),
sinh_chain(), l1()…l6(), warning_card(), sinh_graph(unit, center), TANH_C; ch3_s5_arcosh
cosh_check_card(), fig26() (two-panel Figure 26, for ch4 s5), mini_cosh(); ch3_s7_recap cos_z2_shot()
(matched to ch4 s1's wave_shot(): solid YELLOW y = 2, WAVE_CENTER). Inverse curves use ch7_s4_g3's INV_C
and dashed-line style, so ch3 and ch7 match.
Review: one Gemini round on all 7 scenes + holds; fix passes s1–s7; round 2 = check + holds only.
- Fixed: s1 GOLD/PURPLE term pulses on {gold}/{purple} (FlashAround gone from the scene); s2 floor grows
  from the vertex; s4 `\sinh x` label off the y = x line in fig25d_shot() (s3 re-rendered, handover
  0.00%), cosh two-dot picture held through "So cosh gets the next scene to itself", check_card strike
  diagonal across the whole rejected root; s5 (97) box before its tag, Figure 26 U grows from its vertex,
  longer labelled y = x mirror line, flip folds onto y = x then opens into the sideways U; s6 uses s5's
  cosh_check_card() (its stand-in struck the ½ root, which s5 keeps); s7 matched to ch4 s1's wave shot.
- Not confirmed on frames: s2 @63–64 s "duplicate floor / floor at y ≈ 0.6" (one line at y = 1; a Create
  stub sat above the flat dashed tails); s3 @5 s "dot still at (0, 1)" (at the origin by 5.8 s, 3 s
  before "is zero"); s5 "no x-axis in Figure 26" (both panels have axes); s6 @91.5 s "only two ln's"
  (third turns YELLOW at ~94 s); s7 @28 s "keep the plus outside its card" (inside once settled).
- Accepted: dwell advisories (title card 4.9 s; s1 cos/cosh pair clears at {three} per the brief; s3
  ½e^{-x} label restyled, cosh − sinh label 4.5 s; s4 side notes and the edited quadratic; s6 tanh(ln 2)
  line and y = ±1 labels as in ch7; s6/s7 final holds); s3 gap segments linger 1.9 s into c3.odd.3; s4
  sweep line passing labels; s4 c3.arsinh.3's rejected root struck flat (unlike the card's diagonal);
  s6 vertical number line labelled x (correct: tanh⁻¹'s input); s7 "×2e^y" on screen while the voice
  says "multiply by E to the why" (s4's actual step), `\pm\cosh^{-1} 2` without i (as briefed), and the
  ~10 s still end card (music carries it in the final).
- Gemini pronunciation, all accepted (Whisper base/small/medium raised no flag on any of these
  sentences): "inverse shine" → "inber shine" ×4 (s4, high; s+sh run together), "tanch" → "tank" (s4,
  high), "tonch" (s3 ×2), "tainsh" (s7), "view" → "biew" (s5, high), "log two" → "wad two" (s6, high).
  s6's "tansh → tanch" lines list the written form as heard.
Glitches (for the glitch study):
- s1 ~19.3–20.3 s (c3.hook.2 {purple}): GOLD FlashAround tails still on e^x as {purple} began, PURPLE
  outlines too dim to read. Fixed (scale/colour pulses).
- s1 37.2–37.8 s (c3.hook.3): YELLOW FlashAround box round "← sinh x" left a stray vertical stroke; 41.6–
  42.2 s, the ring round `\ln` faded out as a partial circle. Fixed (pulses).
- s5 ~79.5 s (c3.arcosh.5): the YELLOW box grew from its centre, so a small box sat across the formula
  for ~0.5 s. Fixed (box fades in at full size, then the tag).
- s5 ~90.5 s (c3.arcosh.6): Create drew cosh from its top-left end while the axes were still faint, a
  lone TEAL slash. Fixed (axes first, U grows from its vertex).
- s4 ~105–106 s (c3.arsinh.5): the strike ran flat at fraction-bar height over the − and =, reading
  "¾ 5⁄4 ▬ ½". Fixed (diagonal strike).
- s7 ~24.5–25.3 s (c3.recap.2 r5): two ticked mini axes almost touching. Fixed (no ticks, 0.45 gap,
  (97) moved off the U). ~42.2–42.6 s ({next}): the gap arrow's tip showed alone before its body
  (GrowFromCenter on a DoubleArrow). Fixed (FadeIn whole).
- After `vk finalize 3` (transitions, s4 @50.8 s): real. Final frames at 301.1 and 301.5 s read
  "e² − 2x e^y − 1 = 0", then "e  2 − 2x  e^y" in flight; settled frames at 299.1–300.7 s and from
  301.9 s were correct. Cause: `edit()` from e^{2y} − 2x e^y − 1 = 0 into (e^y)² − 2x(e^y) − 1 = 0 shared
  the e and 2 glyphs and dropped the exponent's y first. Fixed: e^{2y} fades out whole, the shared glyphs
  slide, then (e^y)² and the brackets fade in (~0.2 s with the left term empty). Chapter check: no
  blocking flags; handovers s2 → s3 0.10%, s3 → s4 0.00%. Back to ready for final.
Left open (minor): the {cosh2} miniature branches at the recap's end still carry tick marks; the music
mid bed moved from Spirals to Fractals because ch4 took Spirals. For ch4's director: ch3_s5_arcosh
fig26() is the Figure 26 picture ch4 s5 reuses (its left panel is now x from −3 to 6 with a labelled
y = x); ch3_s7_recap cos_z2_shot() matches ch4 s1's wave_shot() (plus a "Next time" title and the
`\cos z = 2` line).

## Chapter 4 · Solving cos z = 2 (ch4_cos_z)
State: ready for final (director, 2026-11-01). Preview out/ch4_cos_z_preview.mp4, 11.0 min (657.7 s),
plays end to end; handovers s1 → s2, s3 → s4, s4 → s5, s5 → s6 all ok (0.00% differ). Scenes 7/7 (Opus
scene-builders). Music: music/ch4.json (Hypothesis hook to c4.fta.1, Spirals under the lattice plot
c4.lattice.1:end → c4.lattice.3, Far Away recap + end card, swell after recap.3; no clash with ch1–3, ch7).
Shared builders (load_scene): ch4_s1_hook handover_shot(), wave_shot() (.ax .band .wave .line …),
fig26() (now ch3_s5_arcosh's inverse panel: .ax .upper .lower .lab_up .lab_lo .dot); ch4_s2_fta
peel_chain(), peel_labels(chain), not_poly_tag(target); ch4_s3_split ex35_card(pos), result_line(),
cosh_panel(), wave_panel(); ch4_s4_cases case_tree(right, steps); ch4_s5_even xeq_line(), yres_line();
ch4_s6_lattice lattice(center, xs, ys, …) (.pairs .pair(m) .crosses .b2 .bh …), answer_line().
- For ch5's director: ch5_s1_hook draws its own lattice_shot() rather than calling ch4_s6_lattice.lattice()
  (s6 builder's note); the brief's colours agree (i PINK, 2πm BLUE, ln(2 + √3) TEAL), but the shapes may not.
- Gemini: the first `vk review` (s1, s3) failed on a model-selection error (transient); one round later
  covered s1–s6, then the quota ran out (429, resets ~55 h) before s7. s7 was checked with `--frames` only;
  every builder sent one `--frames` sheet of its riskiest plays (the "Gemini off" flow).
- Re-voiced after the scene review (Gemini-only, high confidence): c4.even.2 "Write it as two M, where M is
  any integer" (heard "two meters") → "Write it as two times M, for any integer M" (s5 cues "write it
  as"); c4.lattice.3 "E to the minus why is one over that" (pause after "minus", heard "Why is one over
  that") → "… equals one over that", and "so E to the why is" → "so E to the why equals" (ch7's fix
  for the same trap). Both pass `vk qa 4` (base-only repeat hallucination on even.2:8 accepted: the clip
  grew 0.5 s, no doubled audio). Not re-listened (quota).
- Scene-review claims checked on frames and not real: s2 5.5 s "a₂ z z²" (P(z) fading in), 78 s roots
  uneven (dots arriving one by one; final 0°/120°/240°), s3 45 s arrow source (mid-move), 74 s brace
  omits minus (settled brace includes it, 77 s), s5 48 s double brace (one brace), s6 6 s highlight
  only ± i (the sweep then boxes ln(2 + √3)), s6 44.5 s unlabelled brace on the thumbnail (both braces
  correct, labels hidden on purpose). As designed: s2 box on a_n zⁿ and on (z − z₁), s3 panels clearing
  for the handover, s5 Figure 26 arriving on {graph}.
- Fixed after review: s1 x → z slot empty (below); s3 sin(ix) arrow ran over the "t" of tan(ix) (rerouted);
  s5 2² − 1 → 3 box framed empty space, cos(nπ) → (−1)ⁿ middle empty, nπ copy invisible in flight
  (cross-fades, solid copy); s1 fig26 rebuilt from ch3 (producer), so s5's Figure 26 labels moved back to
  ch3's spot, top label INV_C, panel 0.3 right; s7 bottom panel row raised to 0.55 clear of the edge.
- Accepted: dwell advisories (46, brief- and voice-driven: title card, ±ln labels, x = ±i, "real functions",
  edit-chain steps, minus line, tip, "still alive", ?, n = 2m, "half the solutions lost", algebra cleared
  at {below}, "not a polynomial", recap r5 line / "which n?" / odd π labels); s1 `transition overlap` at
  line 214 (the deliberate x/z cross-fade in one slot). s5 nπ copy is hidden ~0.5 s while leaving its source.
- Departures the builders made (accepted): s2 ⇕ instead of ⇔ (stacked statements), peels as drop + edit
  (no text morphs), cos z = 2 returns at bottom centre on {bridge}; s4 branches drop in; s5 brace dropped
  from the handover; s6 averaging graph on its own y-range; s7 r2 without degree labels, r5 without the
  1.32 label (too small at panel size), r3 braces "real"/"imaginary".
- Note: lib `edit()` became term-safe mid-build (producer); the final render uses it. s1's x → z no longer
  goes through edit().
Glitches (for the glitch study):
- s1 43.0–43.7 s (c4.hook.3 {ask}): "cos _ = 2", variable slot empty ~0.5 s; cause: `edit(ceq, …)` fades
  the dropped x out before fading z in (term-safe edit too). Fixed with a same-span cross-fade.
- s5 (builder's sheet) 59.2–59.8 s: YELLOW box around an empty √ while 2² − 1 → 3 (sequential fade out/in);
  9.4–10.0 s cos(nπ) → (−1)ⁿ empty middle (edit's fade-out-then-in). Fixed (overlapping fades).
- s3 44.7–51 s: TEAL pointer arrow crossed the tan(ix) row's "t" (path, not a transform). Fixed.
Voice: `vk voice 4` re-voiced 7 lines (narration 27/27, 10.4 min). Rewritten by the COURSE.md rules:
- c4.hook.1 "You'll need it today" → "You will need it today"; c4.fta.4 "This isn't a formal proof"
  → "This is not a formal proof" (negative contraction would flip the meaning).
- cosine next to cosh (Whisper base+small heard "cosine" for cosh): c4.cases.1:4 "times cosh of why"
  → "times the hyperbolic cosine of why"; c4.lattice.3:2 "is cosh of why" → "equals the hyperbolic
  cosine of why". Both pass `vk qa 4`.
- "solve": c4.even.3 "To solve the second" → "For the second"; c4.recap.1 "To solve an equation in
  zed" → "To handle an equation in zed"; c4.recap.2 "Solve cosine of zed equals minus two" → "Find
  every zed whose cosine is minus two". c4.recap.1 "Let's recap" → "Time for a recap".
- Accepted Whisper flags (known false): "shine" → "sine" (split.3 ×2, split.4, cases.1); "sixteen oh
  eight"/"eighteen oh six" → 1608/1806 (number format); base-only "cosh" → "cos" (even.4). No
  `vk listen` (producer: only for lines Whisper flags beyond the known-false ones; none left).
Build: handovers s1 → s2 (question block), s3 → s4 (Example 35 card + split line), s4 → s5 (brace
system + x = nπ), s5 → s6 (card + x = 2πm, y = ±ln(2 + √3)); s2 → s3 and s6 → s7 fade to empty. Waves:
s1 + s3, then s2 + s4 (re-spawned after the 16:20 network outage; s2 finished the partial file), s5, s6,
recap.

## Chapter 5 · Circles and ellipses (ch5_circles_ellipses)
State: ready for final (director, 2026-11-01). Preview: out/ch5_circles_ellipses_preview.mp4,
11.0 min (657.7 s, 8 scenes); handover s2 → s3 ok (0.00%); last scene has no handover mark.
Music: music/ch5.json (Heartbeat hook to c5.circle.1,
Fragments under s5's parameter-vs-angle drift c5.param.3, Quaternions from c5.recap.1:end + end card;
swapped from Serendipity/Ongoing on the producer's note, since ch6 opens and closes on those).
Plan: handover s2 → s3 ((99) stays at the top); all other joins fade to empty. Waves: s1, s2, s4–s7,
then s3 (from s2's handover_shot) + recap.
Voice (`vk voice 5`, re-voiced sentences only; COURSE.md rules applied before building):
- Rewritten: c5.hook.1:2 "you solved cosine of zed equals two" → "you looked for every zed whose
  cosine is two" (no "solve"); c5.hook.1:4 "The lecturer called this part a review" → "This part of
  the lecture is a review" (heard "The lecture called"); c5.hook.3:3, c5.param.4:4, c5.recap.2:4
  "cosh and shine" → "shine and cosh" (heard "caution"), hook.3 now "will do the same for a
  hyperbola", param.4 "trace out a hyperbola" (all three Whispers dropped "a" in "draw a hyperbola");
  c5.recap.2:4 "you'll see at last" → "which finally explains" (heard "see it last"); c5.ellipse.4:3
  "in Part One B" → "in second-year maths" ("part" is the videos' word); c5.recap.1:1 "Let's recap"
  → "Time for a recap".
- Accepted Whisper flags: "cosh" → "caution"/"Kosh"/"cash" (param.4:4, recap.2:4; known false);
  c5.area.2:2 "round" → "around" (spelling only); c5.complete.1:2 "term as two" → "term is two"
  (base, small; same meaning). No `vk listen` (producer's Gemini rule: no flag left beyond the
  known-false ones).
- Rewritten after the scene reviews (Gemini, high confidence; Whisper can't tell "A" from the article
  "a"): "half of A" was heard "half of uh" 5× in s3. faster-whisper word timings agreed: the A lasted
  0.20–0.26 s against 0.30–0.42 s for unflagged letters ("numbers A,", "over A", "times A") and
  0.10–0.16 s for the article. Now "half the number A" (letter after a noun, COURSE.md's rule):
  c5.complete.1:2/:6, c5.complete.2:5/:7; c5.complete.1:4 "That corner's area is half of A, squared"
  → "is the square of its width". Re-voiced A lasts 0.28–0.34 s. Also c5.example.4:3 "it's two, the
  semi-major axis" → "it's two, and that's the semi-major axis" ("axis" heard "access").
- Accepted Gemini-only: "axes" said "ax-ez" (s4 ×2, s7; low, a common reading); c5.circle.3 "numbers
  A, B and C" → "uh" once (that A lasts 0.42 s); recap "shine and cosh" against `(cosh θ, sinh θ)`
  (COURSE.md order); s4 "the circle now reaches" over an ellipse (the script's stretched circle).
Scenes: 8/8 built (Opus scene-builders); s3 opens on s2's handover_shot() (0.00% diff). One Gemini
`vk review` round (all 8) + holds → one fix round on all 8 → `vk check` + holds clean (dwell only).
Shared builders (load_scene): s1 lattice_shot(), example36_eq(); s2 handover_shot(); s3 e2_equation(),
e2_figure(), case_icons(), case_rows(); s4 wide_ellipse(), ellipse_picture(a, b); s5
circle_ellipse_pair(), unit_hyperbola_shot() (for ch6 s3); s6 example36_sketch(unit, center) (for ch6
s5); s7 ex36_area(), ex36_ellipse(), ex36_formula().
Fixed in round 1: s1 circle/ellipse cleared before c5.hook.1 ends, points move with θ increasing;
s2 a/b/c rings fitted to the letters; s3 origin dot leaves with the shrinking circle, ghost result
line cleared; s4 wide/tall pair held 4.1 s (was 1.7), shifted braces labelled a/b, {aligned} flashes
arms + axes; s5 finished checks held (≥ 3.5 s, ellipse check at the top through {warn}); s6 cross
legible over the RED −1, FlashAround → colour pulse; s7 "Example 36" label, visible y-stretch (×1.9);
recap r1 "(1, 0)" off the circle, r3 brace inside its panel.
Accepted flags (dwell only): s1 title card 2.7 s ({last} at 3.7 s) and lattice 4–5 s (a callback);
end-of-scene labels before the closing fades (s1, s3, s4, s5, s7); s3 centre line 6.0 s (cleared for
the case card); s4 a/b labels 3.3 s; s5 intermediate check steps (on the way to `= r²`); s7 "Example
36" tag 3.1 s; recap r6 panel 2.9–3.9 s and the "+" 1.9 s before it flips (the beat).
Gemini claims not confirmed on frames: s1 duplicate "(cos θ, sin θ)" @46 s; s5 small dashed circle
@48 s; s6 centre recolour @77 s (both terms YELLOW by 78.5 s); recap r4 dial out of sync.
Glitches (confirmed, fixed):
- s2 @18.4 s (Gemini said 17 s): the GOLD "r" flying into `r²` left a copy with a dark outline that
  read as a grey duplicate beside the label (`fly` from an outlined label). Now flies an outline-free copy.
- s3 @30.5 s ({close}): `derive` dropped a full copy of the long expanded line onto itself (two
  stacked identical lines); a glyph-matching `edit` scattered half-formulas. Now dim + whole fade-in.
- s3 @87.1–88 s ({done}, found by the producer's edit() frame check): `x² − 2x + 1` faded and the
  corner's `− 1` slid into the bracket as `(x − 1)`, pairing the wrong terms. Now a whole fade-in + ring.
- s5 @60 s ({unit}): `sweep_clear` of the angle view overlapped the arriving unit circle (caption,
  readouts, radius lingering on it). Now one play: old view out in the first 40%, circle in from 50%.
- s6 @37.5 s ({times}/{sub}): a RED cross over the RED `− 1` read as a scribble over empty space. Now
  an off-white cross.
- s7 @12 s ({sy}): the y-stretch (×1.3) was too small to see. Now ×1.9.
- Accepted: s2 {shift} ~33 s, for ~0.5 s only `² + ² = r²` shows while the bare x, y leave and the
  brackets fade in (`edit`, no crossing); s6 {factor} 21.8 s brief gaps, {tuck} 67.2 s new line faint
  at first (`edit` fades every new glyph).

## Chapter 6 · Hyperbolas and the conic family (ch6_hyperbolas)
State: ready for final (director, 2026-11-01). Preview: out/ch6_hyperbolas_preview.mp4, 11.3 min
(676 s), plays end to end; handovers s2 → s3 and s5 → s6 ok (0.00% differ); s8 ends the chapter. Music: music/ch6.json (Serendipity hook to c6.flip.1,
Quantum Blue under s3's two running points c6.param.3:end → c6.param.5, Ongoing recap + end card,
swell after recap.2). Avoids ch1, ch2, ch3, ch4 and ch7 tracks.
Voice: `vk voice 6` re-voiced 5 lines (narration 29/29, 10.7 min). Rewritten by the COURSE.md rules:
- c6.hook.2 "Why are cosh and shine called hyperbolic?" → "Why are shine and cosh …" ("cosh and"
  → cos/Cauch, 3/3); "By the end of this part you'll be able" → "…, you will be able".
- c6.recap.1 "Let's recap" → "Time for a recap"; "Cosh and shine draw it" (heard "Caution shine",
  3/3) → "Shine and cosh draw it, just as cosine and sine draw a circle" (a "sine and cosine" take
  was heard "just a sign in cosine": back to the original order).
- "solve": c6.flip.1 "Then solve for why" → "Then make why the subject"; c6.odd.2 "Only one point
  solves that" → "Only one point satisfies that".
- c6.hints.3 "cosine and sine become cosh and shine" → "cosine changes to cosh, and sine to shine"
  (ch7's wording for the same line).
- Accepted Whisper flags (known false, COURSE.md): "shine" → "sine" (param.1, turn.2), "cosh" →
  cos/gauche/Kosh/Cauch/Cache (param.2 ×2, turn.2, hints.3, recap.1), "round" → "around"
  (param.4). No `vk listen` (producer: only for lines Whisper flags beyond the known-false ones;
  none left).
Plan: handovers s2 → s3 (axes, s = 1 hyperbola, asymptotes) and s5 → s6 (the table); the others fade
to empty (s1 → s2 too: the hook's "?" and pair stay to its last beat). ch5 is built in parallel, so
ch6 draws its circle/ellipse callbacks from ch5's briefs instead of importing them. Waves: s1, s2,
s5, s7, then s3, s4, s6, then the recap.
- From the scene reviews (Gemini-only, high/medium; no `vk listen`, per the producer's Gemini rule):
  c6.class.5 "Let's test the table" (clip start, heard "what's") → "Now test the table";
  c6.hints.5 "as a logarithm … The logarithm is Example thirty-four" ("wogrithm") → "as a log …
  That log form is Example thirty-four". Both pass `vk qa 6`. Accepted Gemini-only: "axes" →
  "ax-ez", "different" → "differ" (class.3, same meaning), "hyperbola" → "hyper bola" (s3),
  "asymptotes" → "ay-simp-totes" (s4), "cosh" → "cush" (s7).
Scenes: 8/8 built (Opus scene-builders) in three waves; one Gemini `vk review` round on all 8 + holds;
one fix round (s2, s3, s4, s5, s6, s7, s8; s1 none); round 2 = check + holds only. Handovers s2 → s3
and s5 → s6 match (0.00% differ).
Shared (load_scene): ch6_s1_hook why_label(), glimpse_pair(); ch6_s2_hyperbola to_world, make_axes,
make_branches (.right/.left), make_asymptotes, quarter_labels, handover_shot; ch6_s4_turn
two_orientation_shot() (+ left/right_picture …); ch6_s5_classify classify_table(lit), row_light,
circle/ellipse/hyperbola/updown_hyperbola/empty/tilted_ellipse/ex36_ellipse_icon(s);
ch6_s6_odd_cases collapse_shot(), crossing/point/parabola/parallel_icon(s), FAMILY; ch6_s7_hints
sheet_header(), hints_row(lit) (= ch7_s1 card_row), sheet_note(). s7's cards are ch7_s1_intro's
g_card/card_row (short keys).
- Fixed: s2 quarter labels written for s = 1 (`+√(x² − 1), x > 1` …; the voice says "one", the
  screen showed s); s2 zoom counter removed (a lone "4" at the axis tip); s3 "< 45°" moved by the arc;
  s4 right picture's bottom branch PURPLE (y = −s cosh θ, the reflection of the left minus branch),
  "−s" label clear of the curve; s5/s7 re-synced to the re-voiced lines; s7 G2 line highlight moves
  per curve, G3 pairs stacked f / ⇕ / f⁻¹ under each mini-axes at size 44 (were one run-together
  line, and "↔" read "++"), split-first bracket spans ln[…]; s8 panels clear before the G cards,
  bottom margin 0.35 → 0.45.
- Accepted: dwell advice where the narration moves on (title card 3.1 s, "Last time" at 4.4 s;
  s2 x² − s² ≈ x² rewritten in place; s3 ?² − ?² = 1, r² = s², θ readouts; s4 −s², y = x tag;
  s6 live s counter and circle steps; s7 pause labels cleared by the next question; s8 "the odd
  cases" caption 3.7 s). Brief-mandated: s1 dimmed circle/ellipse on {flip} (Gemini "faint outlines
  remain"); s8 ellipse row lit on {c}. s1 "why hyperbolic?" sits over the TEAL branch, not on the
  moving point (Gemini "stuck at vertex"): it labels the curve. s8 caption "cosh and sinh draw the
  hyperbola" against the voiced "shine and cosh" (COURSE.md order rule; same meaning).
  Departures: s6 parabola and parallel lines PURPLE (the brief gave no colour); s3 bracket fades and
  "· 1" appears instead of a morph; s4 reflection is a 3D flip about y = x.
- Gemini claims not confirmed on frames: s6 @42/46 s hyperbola branches beside x² = 1 (only the
  table's small icon and the grey axis); s6 @55–57 s list highlight "lagging" (each move starts on
  its word); s6 "Chapter 6 of the notes" (the stamp and voice say 3); s8 @14 s yellow line
  "persists" (FlashAround tail, gone by 14.8 s).
- Glitches (for the glitch study):
  - s3 ~37.7 s (c6.param.2 {one}): a lone "1" floating below the working; `fly(card.tex[4], …,
    arc=2.0)`'s wide arc dipped below the rows. Fixed (no flight: ring the card's 1, "· 1" in place).
  - s3 ~80 s (c6.param.4): a yellow arc on the circle's far rim; `VShowPassingFlash` along the whole
    circle, not with the θ-driven point (same on the branch). Fixed (trails grow behind the points).
  - s3 ~102.5 s (c6.param.5, Gemini "HOLD placeholder box"): a detached red tick by a half-drawn
    ray; `Create` on `always_redraw` ray and arc. Fixed (both grow from the origin together).
  - s6 ~17.5 s (c6.odd.1): a "brown" line right of "f = 0 ?"; `FlashAround` on the crossing-lines
    group traced its panel-sized bounding box. Fixed (VShowPassingFlash along each line).
  - s8 ~32.5 s (c6.recap.2 {bonus}): G1 card fading in over the still-fading panels; a one-play sweep
    squeezed into a short gap. Fixed (panels clear on "Part seven", cards on "the bonus").
  - s8 ~14.3 s: a short vertical bar by θ = 0.95, the tail of FlashAround on the readout. Accepted.
  - s7 ~81 s: "↔" at small size read as "++" at 480p. Fixed (⇕ at size 44).
- Producer FYI (lib `edit()` now term-safe) arrived during the fix round; s3, s7, s8 fix renders
  used it; no scene was redone for it.

## Chapter 7 · Solutions to Examples Sheet G (ch7_solutions, bonus)
State: ready for final (director, 2026-11-01). Preview out/ch7_solutions_preview.mp4, 10.1 min (607 s),
plays end to end; handover s1 → s2 ok (0.00% differ). Music: music/ch7.json (Orbit hook to c7.g1.1,
Reflections under G3's sketches c7.g3.2:end → c7.g4.1, Clarity under the recap + end card, swell after
c7.recap.2). Orbit is also in ch1; ch6's director may want to avoid Reflections/Clarity.
Voice: `vk voice 7` re-voiced the 10 continuity-review lines; narration 25/25, 9.4 min.
- Rewritten (Whisper consensus, meaning changed): c7.intro.1 "cosh and shine drew" → "shine and cosh
  drew" ("cosh and" → "caution", 3/3); c7.g2.1:3 "cosine and sine become cosh and shine" → "For the
  second curve, cosine changes to cosh, and sine to shine" ("cos", then "curve" → "turv" +qa);
  c7.g3.4 "it hugs a half E to the ex" → "it follows half of E to the ex" ("huts"/"huds");
  c7.recap.1 → "but with shine and cosh, the point reaches only one branch" ("sine", then "coast
  reach" +qa); c7.recap.2 → "differentiate shine, cosh, and tanch, starting from their exponentials"
  ("Cache"/"cauches"; order now matches the H2 card).
- Rewritten (Gemini, high): c7.g2.1:2 "times cosine theta" → "times the cosine of theta" ("coosign");
  from the scene reviews, c7.g3.3 "only for positive ex" → "only when ex is positive" ("positive es")
  and c7.g4.2 "E to the two why is" → "E to the two why equals" (a pause made it "two, why is").
  All pass `vk qa 7`.
- One Gemini listen (`--only` the 5 Whisper-flagged lines). Accepted, Gemini heard them as written:
  "cosh" → Kosh/cash/cauch in c7.intro.1:2, c7.g2.5:4, c7.recap.2:2. Accepted homophone: c7.g1.5:1
  "sign-flip" → "sine flip". Scene reviews heard "tanch" as tainch/tench/tonch/tonsh (s2 ×3, s5 ×1):
  accepted as the agreed voice form (same open question as ch2).
Scenes: 6/6 built (Opus). s1 first (it owns the cards), s2–s5 in parallel, recap last. Shared (load_scene):
ch7_s1_intro g_card(k, lit), card_row(lit), pause_icon(height, color), ROW_X/ROW_Y, handover_shot();
ch7_s2_g1 boxed_answer(), tan_sum_formula(); ch7_s3_g2 ellipse_sketch(), hyperbola_sketch();
ch7_s4_g3 tanh_panel(inverse_only, unit, center), mini(kind, center), INV_C #A8EBD9 (lighter TEAL),
LGOLD_C #F7D3A6 (ln x); ch7_s5_g4 g4_answer(), minus_one_chip(), deriv_graph(), graph_pair().
For ch6's director: ch6 s7 should reuse ch7_s1_intro's g_card/card_row so the cards match. The cards
carry short keys, not the verbatim sheet text (G2's ~290 characters can't fit a 3-unit card).
Review: one Gemini round (s1–s6) + holds; fix passes s1, s2, s4, s5, s6 (+ an s2 transition-overlap
follow-up); round 2 = check + holds only.
- Fixed: s1 cards pulse as each lights on {g1}–{g4}, ‖ icon pulse; s2 c7.g1.4 expanded fraction held
  through {cancel}, strikes only on the cancelling pairs, whole-fraction swaps; s2 c7.g1.2 sinh/cosh(x+y)
  fade in place; s4 asymptote labels switch y = ±1 → x = ±1 cleanly; s4/s5 re-timed to the re-voiced
  lines; s6 {r1} boxed tanh(x + y) has its + from the start (it was boxed with a minus for 2.3 s), then
  tan's − and the + flash in turn; s6 {r2} RED ✗ lands by "only one branch".
- Accepted: dwell advice (the card row shows 0.6 s at each opening because {card} is at 0.0; s1 title
  and circle/hyperbola pair; s2 algebra steps, (2p + 2q)/(2 + 2pq) 1.6 s before {same}; s3 given line
  0.3 s before it is rewritten; s4 labels; s5 final dy/dx spoken as the scene ends). Departures from
  the brief: hero cards move the row's own card (Transform; TransformFromCopy was flagged as doubled
  text); only G1's hero shows the sheet sentence; s3's point runs θ in ±1.45 (plot cut at |x| ≤ 4.5);
  the recap grid shrinks away, so the end card is the "Next lecture" heading + the H2 card.
- Gemini claims not confirmed on frames: s3 @119 s (±s cosh θ correct when settled); s4 @48 s (ln x
  asymptote is on x = 0), @105 s "tánh" (label mid-fade), @19 s curve in the third quadrant (a true
  reflection in y = x sweeps e^x's left tail through it: geometry); s5 @94 s (third ✓ there by 94.2 s),
  @121 s "corrupted frame" (a plain FadeOut, the video ends at 120.7 s); s6 @20 s G3 tag (visible,
  mid colour change); s6 "Section H vs H2" (H2 is in section H); s2 @44 s (the YELLOW + is the brief's).
- Glitches (for the glitch study):
  - s1 ~17.5 s (c7.intro.1 {warn}): a stray gold vertical line under SPOILERS AHEAD; FlashAround caught
    mid-trace round the ‖ icon. Also ~28 s, a yellow line beside G3 (FlashAround on each card). Fixed
    (scale pulses).
  - s2 ~93 s (c7.g1.4 {cancel}): strikes on the denominator's 1s; the strikes were indexed on a
    half-reduced equation made by `edit`, so they landed on the wrong pieces. Fixed.
  - s2 ~96 s and ~99 s: "+ pq" shown without "2 +" and without the leading 1; `edit` letter-sharing
    rewrites. Fixed (whole-fraction swaps).
  - s2 ~101 s: a short vertical line beside the denominator, the tail of FlashAround on (p + q)/(1 + pq).
    Accepted (the brief's flash).
  - s4 ~103.5 s (c7.g3.6 {atanh}): "y = ±1" labels on lines that had already turned vertical; the
    labels rode with the lines and swapped text 2 s later. Fixed.
- Finalize (vk finalize 7, verdict "look"): ch7_s2_g1 @ 91.9 s "red slashes strike out the ones in
  the denominator" is not real. Frames of out/ch7_solutions.mp4 at 136.5–142.5 s (s2 90.4–96.4 s):
  the numerator's 1s and +pq are struck; from 139.3 s the denominator's strikes are only on +p, +q,
  −p, −q; its 1s and pq's are never struck. No fix pass.
- (producer, 2026-11-01) For ch6's director: s7's question cards reuse `g_card` / `card_row` from
  scenes/ch7_s1_intro.py (short keys, not the sheet's full text). Music: avoid Reflections and Clarity
  (ch7's); ch1 used Euler's Clock, Orbit, Focal Point; ch2 Resonance, Transformation, Endpoint.
- (producer, 2026-11-01 evening) Gemini is about to run out (engine/logs/gemini-off): when
  `vk review`/`vk listen` say "skipped", follow chapter-director.md "When Gemini is off" (Whisper
  `vk qa` is the ear; COURSE.md voice rules on every line before building; `vk check` + holds;
  `--frames` sheets). `vk finalize` then renders + checks format/handovers only: "clean" = done.
- (producer, 2026-11-01 ~17:30) Gemini quota exhausted (429, engine/logs/gemini-off). ch6 final
  `out/ch6_hyperbolas.mp4` 11:17.6, handovers ok; its finalize transitions review couldn't run
  ("look" from the failed review only). Accepted as done: every scene had its one review round.
  ch5 and ch4 finalize without review. When the quota resets, `vk finalize 4 5 6` (with review) can
  re-check them.

- 2026-11-04 Gemini pass (checks only, nothing fixed): ch4-6 ear checks ran: ch4 clean; ch5 c5.hook.3:2 'circles' (Gemini-only); ch6 c6.recap.1:3 'draw'->'draws' (+qa, low), others Gemini-only.
