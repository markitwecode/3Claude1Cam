# How These Videos Are Made: plan

Request: "ok can you create a video on how the videos are currently made lol with all the subs etc.
so i understand how it works and where we can cut?" (2026-10-27). Audience: the studio's owner. They
run it: they talk to the producer, approve plans, watch the videos and check lines by ear. They know
the finished projects (FoCS Lectures 3–5, the cross product), Claude Code, and the words Opus, Sonnet
and tokens. They haven't seen inside: what each sub-agent does, how one scene gets built and
reviewed, and where the tokens go. They want enough to make decisions, above all what to cut.
"Subs" means the sub-agents. Sources: the studio's own docs, snapshotted 2026-10-27 in `source/`:
measured-costs.md (the authority for every number in chapter 2, used as is), studio-CLAUDE.md,
PIPELINE.md, LESSONS.md ("Token budget" is the cost history), and the four agent files; plus real
artifacts of one finished scene in `source/figures/` (below). All listed in project.json.
Total: 2 chapters, ~22 min of narration.

## Shared by both chapters
Running example: FoCS Lecture 3, chapter 4, scene 3, "Tracing append" (`ch4_s3_trace`, clips
c4.trace.1–3, 60.6 s of narration). It's a finished scene the viewer has watched. Chapter 1 follows
it from a line in a plan to a finished frame. Its real artifacts, frozen in `source/figures/`:
- `packet_ch4_s3_trace.txt`: its `vk packet`, the builder's whole input;
- `check_ch4_s3_trace.txt`: its `vk check --no-render` output (65.0 s vs 60.6 s narration; 4 dwell
  flags, accepted, with the reason in the scene's docstring STATUS);
- `ch4_s3_trace_beats.png` (1720×972, 14 tiles): the beats image its builder judged;
- `ch4_holds.png` (1720×1948): the director's holds image for that chapter. It was made before
  `vk holds` switched to the render's real timings, but it looks the same. Show it as what a holds
  image is, without claiming which method made it;
- `final_ch4_s3_trace_frame.png` (1920×1080): the finished video at the "answer" beat.
Its script (`../focs/l03-lists/script/ch4_append_reverse.md`, Scene 3), code
(`../focs/l03-lists/scenes/ch4_s3_trace.py`, `say` blocks at lines 160–350) and cue sheet
(`../focs/l03-lists/music/ch4.json`) are quoted verbatim. Show the PNGs as `ImageMobject`s: the real
artifacts beat mock-ups. Retype text from the files as `Mono`/`Code`, exactly.

Visual language (the palette's meanings for this topic):
- BLUE: agents, as rounded boxes, one size per level of the tree. DIM outline: local tools that use
  no tokens (`vk voice`, the renders). TEAL: files, as small page shapes labelled in Mono.
- YELLOW: attention, names, `{marks}`, the running example, "you". GOLD: tokens, dollars, counts.
  GREEN: good, clean, cheap. RED: waste, errors.
- Chapter 2's token kinds: cache reads GREEN, cache writes GOLD, output (incl. thinking) RED.
  Models: Opus BLUE, Sonnet PURPLE.
- **The master shot:** the agent tree built in ch1 s2. It returns in the same layout every time
  (ch1 s5, s8; ch2 s1, s4, s8).
- **The context bar:** a GOLD vertical bar beside an agent, growing with everything it reads (ch1
  s6). Ch2 s2 lines up one per turn into a staircase.

Terms, the same in both scripts: producer (the main session you talk to), series-planner then
"planner", script-writer, chapter-director then "director", scene-builder then "builder", turn,
context, cache. Spoken forms to keep consistent: "vee-kay" for `vk`, "the plan file" or "plan dot
em-dee", "the status file", "the manifest", "send message", "Manim", "ten-eighty p, sixty frames a
second". Numbers spoken: "a hundred and thirty-two thousand tokens", "two million", "three dollars
fifteen".

## Chapter 1 · From a request to a finished video
Slug: ch1_pipeline · ~11 min · Source: studio-CLAUDE.md (who does what, new project, rules);
PIPELINE.md (diagram, granularity, folder, vk, review standard, recovery, design notes); the four
agent files; LESSONS.md (Voice, Automatic QA, Sync, Working with agents)
Goal: name every agent and tool in the pipeline, say what each one reads, writes and decides, and
follow one scene from request to finished frame, including the builder's write → check → beats
image → fix loop and the director's review.
Scenes:
- s1_hook · Hook (~50 s): title card ("How These Videos Are Made", "3Claude1Cam · A studio tour",
  "Part 1 · From a request to a finished video"). Then the running example's finished frame, big
  (`final_ch4_s3_trace_frame.png`). No single agent made it, and none saw the whole video. The same
  goes for this video: each of its scenes was built by its own agent, which never saw the others.
  The question: who does what, in what order, and how does one sentence of narration become an
  animation that moves exactly on its words? Promise for next chapter: what each part costs, and
  where we can cut. Count roles ("a planner, a writer and a director per chapter, a builder per
  scene"), not a made-up total.
- s2_crew · The crew and the conveyor (~100 s): the master shot, built top-down:
  - "you", then the producer (the main Claude Code session; it talks to you, plans with the
    planner, runs the stages, keeps the state files current);
  - under it the series-planner, the script-writers (one per chapter, in parallel), `vk voice`
    (DIM: a local tool on the Mac's GPU, no tokens) and the chapter-directors (one per chapter,
    one at a time);
  - under a director, 6–8 scene-builders, one per scene, in parallel.

  Then the same crew as a left-to-right conveyor of TEAL files: request + material → PLAN.md,
  project.json → `script/chN_….md` → `audio/*.wav` + manifest.json → `scenes/chN_sK_….py` →
  `out/chN_….mp4`. Points:
  - Agents hand work over through files, never through each other's memory. The producer briefs
    them with paths and decisions, not content. It reads only reports, `vk status`, STATUS.md and
    PLAN.md, never scene code.
  - The one checkpoint: you approve the plan (YELLOW tick).
  - State lives in files (STATUS.md per project, projects/INDEX.md). A session that dies at a
    usage limit resumes with "continue <project>": `vk status` reads the files.
  - Each agent type is a file in `.claude/agents/`, pinned to Opus. It skips CLAUDE.md and carries
    its whole kit in its own system prompt. Nesting is two deep (producer → director → builder),
    within Claude Code's limit of three.
- s3_script · A plan, then a script (~85 s):
  - The planner reads the request and material and decides the shape. Show the granularity ladder
    as nested boxes, labelled with the running example:
    - project (`focs/l03-lists`);
    - chapter (ch4: 8–11 min, about 1300–1800 words at ~160 words a minute);
    - scene (`ch4_s3_trace`: 45–150 s, one Manim file);
    - clip (`[c4.trace.2]`: 15–40 s, one narration line, the unit of voicing and of syncing);
    - mark (`{pending}`: a cue word).
  - PLAN.md goes to you for approval.
  - Script-writers, one per chapter, all at once. The real `[c4.trace.2]` line, retyped verbatim
    with its marks in YELLOW, under its `>` visual brief lines.
  - Narration is written for the ear. One before/after: "exactly en conses" was heard as "exactly
    unconscious", so the script says "one cons per element".
  - Every code example is run with the real toolchain, and the replies are pasted exactly.
  - The planner comes back for a continuity review of all scripts (terms, "last time" and "next
    time", lengths) before anything is voiced.
- s4_voice · A voice that costs no tokens (~70 s): `vk voice` runs locally.
  - `[c4.trace.2]`'s five sentences split apart. Each is voiced on its own by Chatterbox Turbo,
    cloned from one reference recording, on the Mac's GPU (2.5–3.5× faster than real time). They're
    joined by 0.55 s breaths, which gives ~160 words a minute.
  - Several Whisper models listen back to every sentence, and they must agree that it says what
    the script says (word errors, stutters). Why several: the smallest model alone passed real
    mishearings ("nil" heard as "no", "type error" as "tie bearer").
  - A failing sentence (RED) is re-voiced with a new seed, and the best take is kept. If it fails
    across seeds, the text changes, not the seed. A sentence that's still flagged is stored with
    what was heard, and a command lists those for the director to rewrite. Nothing depends on
    someone remembering a manual check.
  - Whisper also times every word. The five sentence starts of c4.trace.2 (0.0, 2.2, 6.5, 12.0,
    15.4 s; 18.2 s long) and its marks land on a timeline, which goes into the manifest.
  - An hour of narration voices in ~20–30 min.
  - No agent can hear the audio, so you still get a list of lines to check by ear.
- s5_director · One director per chapter (~70 s): zoom the master shot to one director's subtree.
  - Its steps as a checklist that stays up here and returns in s8: orient (`vk status`, its own
    sections of PLAN.md and STATUS.md, the script once) → narration fixes → music → builders →
    review → final → record.
  - Directors run one at a time. Each starts 6–8 builders, which all render, so two at once means
    12–16 renders and a usage spike. Two at once roughly halves the wall time, if you ask for speed.
  - Music: a cue sheet places beds by narration line, never by seconds. Show the real
    `"from": "c4.nrev.3:end"` from music/ch4.json. The shape: a bed under the hook, one under a
    visual stretch, one under the recap carrying the end card; dense explanation stays dry.
  - Builders: all launched in one message, in the background. Each gets only the project folder,
    its scene's name, and ≤ 3 lines of continuity (a shared shot, a running example's styling).
    When one scene flows into the next, builder K ends on the shared shot and reports its
    position, size and colours for builder K+1. Builders never share files.
  - Why an agent and not a fixed script: the review loop needs judgment.
- s6_builder · Inside a scene-builder (~125 s): the heart of the chapter. One builder, one scene,
  `ch4_s3_trace`.
  - The context bar appears, small: the kit (its system prompt, identical for every builder, so it
    comes from the cache) plus the packet (`vk packet`, ~1k tokens: the brief, every sentence with
    its start time, the neighbouring scenes). Show an excerpt of the real packet.
  - It's told not to read the docs, the whole script, other scenes or engine sources: the kit is
    their distilled form, down to the library's complete signatures, so there's nothing to look up.
  - The loop as a cycle that keeps turning:
    - design once (about one visual change per 8 spoken words; the layout; the cue for each change);
    - write the whole file in one go;
    - `vk check`;
    - read the beats image;
    - fix, all at once;
    - check again.
  - `vk check`, part 1: a dry run audits the scene without rendering it. It looks for errors,
    overruns, text removed before it can be read twice, and cut-off, overlapping or small text. It
    also flags hard-coded times and a scene that doesn't end on an empty frame.
  - Show the real lint output (`check_ch4_s3_trace.txt`: four dwell flags). Dwell flags are notes,
    and the render goes ahead. Overrun, sync (hard-coded time) and layout flags stop the check
    there: no render, no image, until the builder fixes them. A flag the brief really demands can be
    pushed through with `--render-anyway`.
  - `vk check`, part 2, once no blocking flag is left: a 480p render and one beats image, one tile
    per settled moment, labelled "clip > next cue". Show the real beats image. Highlight one tile
    (`trace.2 > answer 40.0s`) next to the words being said at that moment.
  - The builder judges as the viewer: does each tile show what is being said?
  - A median of 25 turns, about five of them check runs. It stops when the check is clean and the
    beats look right, and doesn't polish beyond what a viewer would notice.
  - Every pass adds to the context bar (the file, the check output, a 2–4k-token image), and
    everything added stays. Then a ≤ 12-line report goes up to the director.
- s7_sync · Cued on words, never on seconds (~80 s):
  - The `with self.say("c4.trace.2") as c:` block as Python Code: an excerpt of the real block
    (scene file lines 228–290), trimmed to 4–6 lines, every call as in the file.
  - What each line does:
    - `say` starts the clip's audio now;
    - `c.until(cue)` gives the seconds to a cue, used as a run_time;
    - `c.wait_until(cue)` idles until the cue;
    - leaving the block waits out the clip, plus 0.35 s.
  - A cue is a `{mark}` or any phrase spoken in the clip, looked up in the manifest's word times.
  - Why: v1's agents wrote 157 hard-coded times, and every re-voiced line silently desynced.
    Visual: the clip is re-voiced longer, its cue pins slide with their words, and the cued
    animations slide with them. A hard-coded block stays put, RED, off its word.
  - `vk check` flags hard-coded times, and overruns (animations that outlast the clip push the
    next line late).
- s8_review · Review, the final cut, and recap (~100 s): back to the director's checklist.
  - Once every builder reports: `vk check --chapter 4 --no-render`. Every flag is fixed or accepted
    for a stated reason. Example: the trace's dwell flags were accepted, because the in-place
    collapse shows passing states while the voice says "three onto four, then two, then one". The
    reason is recorded.
  - `vk holds 4`: one settled frame per narration line, labelled with its clip id. It's taken at
    the moment the render itself logged for that clip, so it can't drift. Show a crop of
    `ch4_holds.png` around the c4.trace tiles. The director reads it once per round and looks for:
    - frames that don't match the narration;
    - sizes, colours or placement that differ across scenes;
    - wrong code;
    - cramped, cut-off or half-empty frames.
  - A doubt about composition goes as a question. Once a director called a table "left-heavy" from
    a downscaled tile; the builder measured, and it spanned the frame.
  - Fix notes: observable, and tied to a beat label (the form "acc.3 > give: the reply overlaps
    the chain; move the chain down ~0.5"). They go by send message to the builder that made the
    scene if it finished under ~1 h ago, since it still has the scene in context; otherwise to a
    fresh builder. At most two rounds.
  - `vk final 4`: every scene at 1080p60 in parallel, stitched with the music mixed in (~2–3 min),
    then checked with ffprobe.
  - STATUS.md is updated. A ≤ 12-line report goes to the producer, who relays ≤ 5 lines to you,
    with the lines to check by ear.
  - Recap, one sentence per stage, on the master shot.
  - Next time: every turn of every agent costs tokens; where they go, and where we can cut.
  - ~8 s end card.
Continuity: the master shot, built in s2, reused in s5 (zoomed) and s8, and handed to ch2. The
running example threads every scene: its clip (s3), its voicing (s4), its builder's brief (s5), its
packet, check and beats image (s6), its `say` block (s7), its holds tile and final frame (s8). The
director's checklist is shared by s5 and s8 (same position and styling). The context bar starts in
s6 and opens ch2. Numbers in ch1 are about process (minutes, words a minute, counts, turns). Dollars
wait for ch2, apart from "no tokens" for the voice.

## Chapter 2 · Where the tokens go, and where to cut
Slug: ch2_costs · ~11 min · Source: measured-costs.md (every number, the questions and answers,
the caveats, and "Later findings": the anatomy of a build, effort level, the second opinion, the
three engine changes, this video as the test); LESSONS.md "Token budget"; PIPELINE.md design notes;
studio-CLAUDE.md "Costs", "Rules"
Goal: explain why cost ≈ turns × context, and why the dollars sit in output (mostly thinking) and
cache writes rather than in re-reads. Read the measured breakdown down to one build. Weigh, with
the numbers, fewer builders, Sonnet, effort level, and an outside model's suggestions.
Scenes:
- s1_hook · Hook (~45 s): title card, part line "Part 2 · Where the tokens go". One sentence of last
  time (one scene, from request to finished frame).
  - The master shot returns: every BLUE box is an agent, and every agent turn costs tokens.
  - Everything ever run in the studio (9 producer sessions, 175 sub-agent runs) comes to ~850
    million tokens (794M cache reads, 39.5M cache writes, 13.8M output), ~$633 at Opus list prices.
  - Said once, plainly: you're on a subscription, so dollars here are a common unit for comparing
    the parts (relative weight), not money spent.
  - The question: where does it go, and what can we cut without making the videos worse?
  - The three questions you asked, as cards: could steps run on Sonnet? Do we need so many
    builders? How does building work? The third was last chapter; this one answers the other two.
- s2_turns · Every turn re-reads everything (~90 s): the model.
  - The context bar from ch1 s6 returns. An agent keeps no memory between turns: each turn sends
    its whole context again (instructions, every file read, every reply, its own thinking) and
    adds a little.
  - Turn by turn, the bars line up into a staircase. The tokens read = the staircase's area ≈ turns
    × average context. (FoCS L3 ch4 felt nrev's cost the same way, staircase into area.)
  - The three prices per million tokens (Opus list): re-reading from the cache $0.20, new tokens
    written to the cache $5, output including thinking $20. The area is recoloured: a big GREEN
    body (cache reads), a thin GOLD sliver per step (cache writes), a thin RED cap (output).
  - The body is most of the tokens; the slivers are most of the dollars. Across the studio, reads
    are 25% of the dollars, writes 31%, output 44% (derived from the totals at those prices;
    recompute). The builder's own split comes in s5.
  - Sonnet's prices beside them: the same $0.20 for cache reads, $2.50 for writes, $10 for output.
    Half of the two expensive kinds.
  - The cache expires after a while (the studio's rule of thumb is about an hour). An agent woken
    later re-writes its whole context at the write price.
- s3_history · The first lecture: 450 million tokens (~65 s): the model, proven the hard way.
  - The first production run processed ~450M tokens and hit the plan's limit with chapters 2–5 half
    built.
  - Bloat 1: one orchestrator session did everything and grew to 854k context, ~0.8M a turn
    mostly to read a notification. 170M, 38%.
  - Bloat 2: scene agents took 6–11M per scene. They spent ~15 turns reading docs and other scenes
    (60–80k), then 20–60 turns of render → image → patch, with ~300 images kept in context.
  - The fixes, each aimed at turns or context:
    - nested agents (each level holds only its own concerns);
    - the scene-builder type with its distilled kit, cached;
    - `vk packet` (~1k tokens instead of the docs);
    - `vk check` (a lint instead of looking at images);
    - a shared helper library.
  - Result: 2.3–3.8M per scene, finished and check-clean. The ~90M of one-off research was done once
    and is reused.
- s4_breakdown · Where it goes now (~105 s): the master shot, with each part's share written on its
  box (at Opus prices).
  - Scene work ≈ 78%: scene-builders $278 (94 runs, 18 of them fix passes) plus the older
    general-purpose scene agents $217.
  - Director $40 + script-writer $17 + planner $9 ≈ 10%.
  - Producer sessions $72 ≈ 11%, almost all of it one early, bloated session (168M cache reads).
  - Zoom on one builder (medians of 76 fresh builds): first turn 12k (10k from the cache, 2k new),
    25 turns, peak 132k, 2.0M re-read in total, $3.15. A fix pass (18 runs): 7 turns, peak 30k,
    0.2M, $0.25.
  - Starting a builder costs ~$0.01, about 0.4% of a build: its instructions are the same for every
    builder, so all but the first read them from the cache.
  - Your second question: so do we need so many builders? Fewer would cost more.
    - Two staircases side by side: scene 1 and scene 2, each ~25 turns averaging ~80k.
    - Against them, one builder doing both: scene 2's staircase sits on a ~130k plinth left over
      from scene 1, so its turns re-read ~190k each instead of ~80k. That's roughly 70% more
      re-reading for the pair (about 4.0M → 6.75M, derived; recompute).
    - It also halves the parallelism (a chapter takes about twice as long), and risks mixing up
      the scenes.
    - The same plinth explains why late fix notes go to a fresh builder, and why the producer
      stays out of scene work.
- s5_anatomy · Inside one build (~75 s): ch1 s6's context bar, opened up. These are medians of 76
  fresh builds: call it "a typical build", never the trace's own numbers.
  - Its 25 turns, as a row of tiles coloured by kind:
    - ~5 `vk check` runs (2 of them with `--frames`) and ~5 image reads;
    - 1 Write and ~0 Edits;
    - ~13 other shell calls. ~9 of those are lookups (the engine library, Manim's source, other
      scenes, odds and ends), plus ~2 shell patches.
  - Its ~132k peak context as a stacked bar: ~12k startup, ~15k images (5 × ~3k), ~11k tool
    output, ~8k file writes and patches, and the remaining ~80k is thinking (RED; the rest in GOLD
    shades).
  - The surprise: thinking is ~60% of the peak. Images, the old suspect, are only ~10%.
  - Its dollars, from the source: output (mostly thinking) about half, cache writes about 30%,
    re-reads about 15%. Thinking is the biggest single cost.
  - So two questions: can it think less, and look things up less?
- s6_dials · Two dials: the model and the effort (~95 s): two dials appear on the builder's box.
  - Dial 1, the model (your first question):
    - Only the builders matter (~80% of agent spend). The planner, writer and director are small
      and they're the judgment gates (plan, teaching, review), so they stay on Opus.
    - The same builder tokens at Sonnet prices: $278 → $159, ~43% less. In the bars (Opus BLUE,
      Sonnet PURPLE), the GREEN reads are identical and the GOLD and RED parts halve.
    - The catch: only if Sonnet finishes in the same number of turns. Building a scene is the
      hardest job (Manim code, plus judging layout from the beats image), and Sonnet 5.5 trails
      Opus most on hard coding (SWE-Bench Pro, about 81 vs 90). Extra check runs or review rounds
      would eat the saving: the Sonnet staircase grows extra steps until its cost catches up.
    - Transcripts may undercount output; if so, Sonnet's relative saving is larger.
    - Fix passes are well scoped (apply the notes, re-check), so they're the safe place for Sonnet.
      The producer could run on Sonnet too, but it's lean now, so the saving is small.
  - Dial 2, effort level: how much the model thinks before it acts. It's set per agent type and has
    never been tuned. It's the lever that hits thinking directly, and thinking is the biggest
    single cost. Same catch: thinking less might mean more check runs and fix rounds.
  - Neither dial can be set by argument. It has to be measured (pays off in s8).
- s7_second · A second opinion (~75 s): you asked another AI model, Gemini, to review the pipeline.
  Each of its claims was checked against the code and the transcripts. Its ideas go up on a board,
  and each one turns GREEN (held up), RED (didn't) or DIM (missed).
  - Held up, and adopted:
    - Skip the render and beats image while the lint still has flags. True, since the check used
      to render anyway. A small saving (~1–2 image reads a build, 3–5%), and cheap.
    - Move the several-model voice check into `vk voice`. True, and its best idea, for quality
      rather than tokens. The three-model check lived only in a lessons file directors are told
      not to read, so it had probably stopped running.
    - `vk holds` guessed clip times by adding up audio durations, and sampled 0.4 s before each
      clip's end. True, and worse than it said: any animation outside a `say` block shifted every
      later tile.
  - Didn't hold up:
    - Pre-made skeleton files and a shared helper file per chapter. Rejected: builders already
      write the file in one go (~1k tokens of boilerplate), and a shared file breaks "builders
      never share files", the rule that keeps parallel builds safe.
    - "Builders make many small Edit calls." Wrong: the median is zero. The real waste is the ~9
      lookups per build.
    - A 12–15 turn cap. Rejected: arbitrary, and turns aren't the main cost.
  - It agreed on Sonnet for fix passes (repeating the analysis), and it missed effort level
    entirely.
  - The three changes, as done (2026-10-27). One sentence first: you saw them in part one as how
    things work.
    1. `vk voice`'s QA needs several Whisper models to agree. Flagged sentences are stored with
       what was heard, and a command lists them.
    2. `vk holds` takes each frame from the render's real timings.
    3. The builder's prompt carries the library's complete signatures (no more lookups), and
       `vk check` skips the render while the lint has flags.
- s8_test · The levers, this video as the test, and recap (~110 s):
  - The levers on one board, ranked, each pointing back to its scene: thinking (effort level, s6),
    the model (s6), turns (fewer lookups, no renders while flagged, s7), and context (images are
    only ~10%).
  - Habits that already save:
    - fix notes within the hour, or to a fresh builder ($0.25), rather than waking a cold
      300–400k agent;
    - a lean producer (it was once 38% of a lecture);
    - one director at a time, to keep usage bursts down (two at once halves the wall time if speed
      matters more).
  - What not to cut: the planner, writers and directors (~10% together, the gates that stop
    expensive rework), and an agent's startup cost.
  - Caveats, once:
    - the dollars are relative;
    - the counts cover the transcripts on disk, which is nearly everything;
    - how your plan weighs Sonnet against Opus usage isn't published.
  - This video is the test. Its 16 scenes were built three ways, rotated across scenes: Opus as
    now, Opus at lower effort, and Sonnet. Show the 16 scene boxes of both chapters, with the three
    variants as small builder icons (BLUE, dimmed BLUE, PURPLE). Don't map them to particular
    scenes.
  - Measured afterwards: cost per finished scene, including fix passes, check runs and review
    notes. The results land in STATUS.md. Narrate no outcome and hint at none ("the scene you're
    watching was built by one of them" is fine).
  - Recap of both chapters, one sentence per idea, on the master shot:
    - the crew, with files as the hand-offs; the builder's loop and the director's review;
    - cost ≈ turns × context, with the dollars in output (mostly thinking) and writes;
    - scene work is ~78%, and fewer builders would cost more;
    - two dials, the model and the effort;
    - a second opinion, and three changes.
  - In place of "next time" (there's no part 3), your next step: when the results are in STATUS.md,
    choose the builders' default model and effort, and the fix passes'.
  - ~8 s end card.
Continuity: opens with one sentence of last time. The master shot and the context bar come from
ch1, in the same layout and colours.
- s5's anatomy is "a typical build" (medians). Never attribute numbers to the trace's builder.
- Ch1 already showed the new voice QA, holds and check behaviour as how things work; s7 reveals they
  came out of the review. Ch1 is not to call them new.
- The test's three variants are always named "Opus as now", "Opus at lower effort", "Sonnet".
- Dollars are always "at Opus list prices": said in s1 and again in s8. Tokens are in millions,
  spoken "million".
- No new measurements: only measured-costs.md (including "Later findings") and LESSONS.md "Token
  budget". The derived figures (the studio-wide dollar split, the pair's 4.0M vs ~6.75M) are
  computed in Python and said as "about".

## Decisions
- **Two chapters of ~11 min each, ~22 min in all.** These are the producer's two halves, and each
  answers one question: how is a video made, and where do the tokens go? Each needs the top of the
  range to stay calm:
  - ch1 has six roles plus two loops in detail;
  - ch2 has the model, the history, the breakdown down to one build, two dials, a second opinion
    and the levers.

  I considered three chapters (~30 min). That's calmer, but it costs ~25M more tokens to animate, in
  a video about cutting tokens. The coordinator confirmed two.
- **Revision 2026-10-27** (the coordinator, after "Later findings" was added to
  measured-costs.md). Ch2 was rebalanced and keeps 8 scenes and ~11 min:
  - new s5_anatomy (thinking is ~80k of the ~132k peak, and the biggest cost);
  - s6_dials (effort level joins Sonnet);
  - s7_second (the Gemini review: verdicts, and the three engine changes, described as done);
  - s8 ends on this video as the test, with no outcomes.

  To make room, the history is shorter, "fewer builders" moved into s4_breakdown (it follows from
  "startup costs a cent"), and the levers fold into the last scene. Ch1's voice QA, holds and check
  loop now describe the new behaviour.
- **Order.** Ch1 follows the pipeline's own order (PIPELINE.md). Ch2 goes model → history →
  breakdown → anatomy → dials → second opinion → levers and test:
  - every later number is read through turns × context;
  - the anatomy (thinking is the biggest cost) comes before the dials, because it's why effort
    level is a lever;
  - the second opinion comes after the viewer has the numbers to judge each idea themselves.
- **One running example** (ch4_s3_trace) instead of a fresh one per stage, with its real files
  frozen in `source/figures/`. Seeing the actual packet, check output, beats and holds images is the
  most direct way to understand what each agent sees.
- **Scope.** "Everything in the material" can't mean all of the studio's docs here; the request
  scopes it to the process and its cost. Left out because they don't bear on either: Manim pitfalls,
  the renderer and encoder benchmarks, the voice-reference experiments, music licensing, setup,
  `vk` commands beyond the ones the stages use.
- **No exercises and no bonus chapter** (producer's decision). The last chapter's "next time"
  becomes the user's next step, since there's no part 3.
- **Numbers.** Dollars are API list prices, as measured-costs.md gives them, framed as relative
  weight (the user is on a subscription). The builder's dollar split now comes from the source.
  Only the studio-wide split and the two-scenes-in-one-builder re-reading are derived: recomputed
  in Python and labelled "about".
- **Code on screen** is Python (the `say` block, excerpts of the real scene file). `vk` commands and
  tool output appear as plain Mono text.
