# Chapter 2 · Where the tokens go, and where to cut

3Claude1Cam · A studio tour (how these videos are made), part 2 of 2. Source: source/measured-costs.md (all, including "Later findings", 2026-10-27); source/LESSONS.md, "Token budget"; source/PIPELINE.md, "Design notes"; source/studio-CLAUDE.md, "Rules" and "Costs".

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Numbers: every figure on screen and in the narration is from source/measured-costs.md or
LESSONS.md "Token budget", rounded as there. The derived ones (the studio's dollar split in s2, the
pair of scenes in one builder in s4, the per-kind dollar bars in s6) were recomputed with the
engine's Python 3.11.9 on 2026-10-27. The running example's builder is never given numbers here:
s5 is "a typical build" (medians of 76).

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card: "How These Videos Are Made", "3Claude1Cam · A studio tour", "Part 2 · Where the tokens go".
> {crew}: ch1's master shot returns exactly as ch1 s2 built it (YELLOW "you"; the producer; "series-planner", "script-writer ×N", DIM-outlined `vk voice`, "chapter-director ×N"; "scene-builder × 6–8"). {costs}: the small GOLD token mark that ended part 1 lands on every BLUE agent box (none on `vk voice`, which uses no tokens).
> {total}: the tree shrinks to the upper left. GOLD counters "9 producer sessions" and "175 sub-agent runs" flow into one GOLD total "≈ 850 million tokens".
> {kinds}: the total splits into three horizontal bars, lengths to scale: GREEN "794M cache reads" (nearly the full width), GOLD "39.5M cache writes", RED "13.8M output". The GOLD and RED bars are tiny; they come back as s2's slivers.
> {dollars}: GOLD "≈ $633 at Opus list prices". {unit}: a DIM tag under it, "subscription: a unit for comparing parts, not money spent".
> {question}: everything clears to one YELLOW line, "Where does it go? What can we cut without making the videos worse?"
> {cards}: three cards with the user's questions, verbatim from measured-costs.md, each lighting YELLOW on its spoken line: {sonnet} "Can any step run on Sonnet instead of Opus?" / {many} "Do we need so many scene-builders per chapter? Starting an agent costs money." / {how} "How does scene building work? What does each agent do?"
> {third}: card 3 DIMs with a small tag "Part 1"; cards 1 and 2 stay lit. Card 2 returns in s4 and card 1 in s6, same styling.

[c2.hook.1] {title} Last time, we followed one scene from a line in a plan to a finished frame. {crew} Here's the crew again. {costs} Every blue box is an agent, and every turn an agent takes costs tokens. {total} Everything ever run in this studio, nine producer sessions and a hundred and seventy-five sub-agent runs, comes to about eight hundred and fifty million tokens. {kinds} Nearly all of it is re-reading.

[c2.hook.2] {dollars} At Opus list prices, that's over six hundred dollars, six hundred and thirty-three in total. {unit} You're on a subscription, so this is not money spent, just a common unit for comparing the parts. {question} So where does it go, and what can we cut without making the videos worse? {pause}

[c2.hook.3] {cards} You asked three questions. {sonnet} Can any step run on Sonnet instead of Opus? {many} Do we need so many scene builders, since starting an agent costs money? {how} And how does scene building work? {third} Part one answered the third. This part answers the other two.

## Scene 2 · Every turn re-reads everything (ch2_s2_turns)

> ch1 s6's GOLD context bar returns beside one BLUE builder box, in ch1's position and styling (bottom-anchored segments, thin dark separators). {resend}: a YELLOW sweep runs up the whole bar while its segments are regrouped under four labels, as spoken: "instructions" (ch1's kit), "files read", "replies", and a new top segment "thinking". {adds}: a thin new segment lands on top.
> {stairs}: the bar copies itself left to right (TransformFromCopy), one bar per turn, each a little taller, about 25 bars, into a staircase on axes "turns" (x) and "context" (y). {area}: the staircase fills as one shape, YELLOW "tokens read = area". {formula}: a dashed average-height line and a rectangle of the same area; under it, "cost ≈ turns × average context". {nrev}: a small DIM inset of FoCS L3 ch4's nrev staircase (rows of 0, 1, 2 … blocks), labelled "nrev · Lecture 3".
> {prices}: a BLUE price column on the right, header "Opus, per million tokens", rows lighting on their words: {reads} GREEN "cache read  $0.20", {writes} GOLD "cache write  $5", {output} RED "output (incl. thinking)  $20".
> {recolour}: the staircase recolours by kind: a big GREEN body (re-reading), and on each step a thin GOLD sliver (new tokens written to the cache) and a thin RED cap (output). Keep the slivers thin: the picture is "most tokens are GREEN".
> {body}: GREEN tag "most of the tokens"; {slivers} GOLD + RED tag "most of the dollars". {split}: three tags, the studio's dollars at Opus list prices: GREEN "reads 25%", GOLD "writes 31%", RED "output 44%" (derived from the totals 794M / 39.5M / 13.8M: $158.8 / $197.5 / $276.0 of $632.3; checked in Python 3.11.9).
> {sonnet}: a PURPLE column "Sonnet" beside the price column: "$0.20", "$2.50", "$10"; a small "=" on the read row and "½" on the write and output rows.
> {expire}: a small clock over the builder box; the bar's cached look fades. {cold}: the whole bar flashes GOLD, label "re-written at $5 per million". The staircase and bar styling carry into s4, s5 and s6.

[c2.turns.1] {bar} Here's the context bar from part one, beside a builder. {nomemory} An agent keeps no memory between turns. {resend} Each turn, it sends its whole context again: its instructions, every file it has read, every reply, and its own thinking. {adds} Then it adds a little.

[c2.turns.2] {stairs} Line up one bar per turn, and you get a staircase. {area} The tokens it reads add up to the area of that staircase. {formula} So the cost is roughly the number of turns, times the average context. {pause} {nrev} It's the same staircase as N-rev, in the lecture on lists.

[c2.turns.3] {prices} But tokens have three prices. Here's what Opus charges per million. {reads} Re-reading from the cache costs twenty cents. {writes} Writing new tokens into the cache costs five dollars. {output} And output, which includes thinking, costs twenty dollars. {recolour} Colour the staircase that way. A big green body of re-reading, and on each step, a thin gold sliver and a thin red cap.

[c2.turns.4] {body} The green body is most of the tokens. {slivers} The slivers are most of the dollars. {split} Across the studio, re-reading is about twenty-five percent of the dollars, cache writes about thirty-one, and output about forty-four. {sonnet} Sonnet charges the same twenty cents for re-reading, and half for the other two, two dollars fifty and ten dollars.

[c2.turns.5] {expire} One more rule. By the studio's rule of thumb, the cache expires after about an hour. {cold} An agent woken later writes its whole context into the cache again, at five dollars a million.

## Scene 3 · The first lecture: 450 million tokens (ch2_s3_history)

> A tall gauge "≈ 450M tokens" fills toward a RED line "the plan's limit". {limit}: it touches the line; beside it, five chapter boxes "ch1" to "ch5", with ch2–ch5 half filled and hatched DIM ("half built").
> {orch}: one oversized BLUE box "one main session"; its GOLD context bar shoots up to "854k". {notify}: a tiny notification icon pings, and a GOLD arrow sweeps the whole bar, "≈ 0.8M a turn". {share}: a RED slice of the 450M gauge, "170M · 38%".
> {scenes}: a row of scene boxes, each with a tall bar, "6–11M per scene". {onboard}: TEAL page shapes ("docs", "other scenes") pour into one bar, "~15 turns · 60–80k". {loop}: a small cycle "render → image → patch", labelled "20–60 turns". {images}: little image thumbnails stack inside the bar and stay there; GOLD "≈ 300 images".
> {fixes}: the clutter clears; five GREEN cards, one per spoken item, each with a small DIM tag for what it shrinks: {nested} "nested agents" (context), {kit} "scene-builder type · cached kit" (context), {packet} "`vk packet` · ~1k tokens" (turns + context), {check} "`vk check` · a lint, not images" (turns), {lib} "shared helper library" (turns).
> {result}: the "6–11M per scene" bar shrinks to GREEN "2.3–3.8M per scene · finished, check-clean". {research}: a DIM side box "≈ 90M one-off research · done once, reused".

[c2.history.1] {first} The studio learned this the hard way. {run} Its first lecture processed about four hundred and fifty million tokens, {limit} and hit the plan's limit with chapters two to five half built. {pause}

[c2.history.2] {orch} First, one main session did everything, and its context grew to eight hundred and fifty-four thousand tokens. {notify} For an hour of supervising, each turn cost about zero point eight million tokens, mostly just to read a notification. {share} That session came to a hundred and seventy million, thirty-eight percent.

[c2.history.3] {scenes} Second, the scene agents took six to eleven million tokens per scene. {onboard} Each spent about fifteen turns reading docs and other scenes, sixty to eighty thousand tokens, {loop} then twenty to sixty turns of render, look at an image, and patch. {images} About three hundred images went into context, and every one stayed there.

[c2.history.4] {fixes} Each fix aims at turns or context. {nested} Nested agents, so each level holds only its own concerns. {kit} A dedicated agent type for building scenes, with its distilled kit in the cache. {packet} Vee-kay packet, about a thousand tokens instead of the docs. {check} Vee-kay check, a lint instead of looking at images. {lib} And a shared helper library. {result} A scene now takes two point three to three point eight million tokens, finished and check-clean. {research} The ninety million of one-off research was done once.

## Scene 4 · Where it goes now (ch2_s4_breakdown)

> The master shot returns in ch1's layout; each part gets its share in GOLD, at Opus prices. {scene}: the builders' row glows, "scene-builders $278 · 94 runs (18 fix passes)"; {old} a DIM ghost row beside it, "older general-purpose scene agents $217"; a brace over both, "scene work ≈ 78%".
> {gates}: "director $40", "writer $17", "planner $9" on their boxes, brace "≈ 10%". {producer}: "producer sessions $72 · ≈ 11%", with a DIM note "mostly one early session (168M cache reads)".
> {zoom}: zoom into one builder box, s2's context bar beside it. A stat card titled "a typical fresh build (median of 76)", lines appearing on their words: {first} "first turn 12k (10k cached + 2k new)", {grow} "25 turns · peak 132k", {total} "2.0M re-read · $3.15". {fix}: a smaller card beside it, "fix pass (median of 18): 7 turns · peak 30k · 0.2M · $0.25".
> {start}: GREEN "start ≈ $0.01 ≈ 0.4% of a build"; {cache} the bar's instruction layer glows GREEN (from the cache).
> {question}: s1's card 2 returns: "Do we need so many scene-builders per chapter? Starting an agent costs money." {answer}: under it, YELLOW "Fewer would cost more."
> {two}: two staircases side by side in s2's styling, "scene 1" and "scene 2", each "25 turns · avg ≈ 80k". {one}: they slide onto one builder. {plinth}: scene 2's staircase lifts onto a GOLD plinth, "≈ 130k left from scene 1", and grows on it as before (+~120k over its 25 turns, the same shape as a fresh build), label "starts at ~130k, grows as before". Never write "130k + 80k". {each}: a dashed average line across it, "≈ 190k a turn on average", against scene 1's DIM average line "≈ 80k". {more}: GOLD "4.0M → ≈ 6.75M", RED "≈ 70% more re-reading" (derived: 2 × 25 × 80k = 4.0M; 25 × 80k + 25 × 190k = 6.75M, +69%; checked in Python 3.11.9).
> {slow}: a time bar doubles, "≈ 2× as long"; {mix}: the two scenes' tiles tangle, RED "?". {same}: the plinth stays, with two DIM tags: {fresh} "late fix notes → a fresh builder", {lean} "producer stays out of scene work".

[c2.split.1] {shares} Here's where it goes now, at Opus prices. {scene} Scene work is about seventy-eight percent. That's the scene builders, two hundred and seventy-eight dollars over ninety-four runs, {old} plus the older general-purpose scene agents, two hundred and seventeen. {gates} The director, writer and planner make about ten percent together. {producer} The producer sessions are about eleven percent, almost all of it one early, bloated session.

[c2.split.2] {zoom} Now zoom in on one builder, with medians of seventy-six fresh builds. {first} Its first turn is twelve thousand tokens, ten thousand from the cache and two thousand new. {grow} It takes twenty-five turns, peaking at a hundred and thirty-two thousand. {total} It re-reads two million tokens in total, and costs three dollars fifteen. {fix} A fix pass takes seven turns, peaks at thirty thousand, and costs twenty-five cents.

[c2.split.3] {start} Starting a builder costs about a cent, about zero point four percent of a build. {cache} That's the shared kit from part one, read from the cache. {question} So, your second question. Do we need so many builders? {pause} {answer} Fewer would cost more.

[c2.split.4] {two} Here are two scenes, each with its own builder: twenty-five turns, averaging about eighty thousand tokens. {one} Now give both scenes to one builder. {plinth} Scene two's staircase starts on a plinth, about a hundred and thirty thousand tokens left over from scene one, and grows as before. {each} So its turns re-read about a hundred and ninety thousand on average, instead of eighty. {more} For the pair, about four million tokens become about six point seven five million, roughly seventy percent more.

[c2.split.5] {slow} It also halves the parallelism, so a chapter takes about twice as long, {mix} and it risks mixing up the scenes. {same} The same plinth explains two habits. {fresh} Late fix notes go to a fresh builder, {lean} and the producer stays out of scene work.

## Scene 5 · Inside one build (ch2_s5_anatomy)

> ch1 s6's context bar, opened up. Title: "a typical build (medians of 76 fresh builds)". Never label anything as the trace's own build. The turn counts are separate medians and don't add up: show each group with its "about" count, and no total and no 25-tile row.
> {tiles}: groups of small square tiles (one per turn) appear one group at a time, each labelled with its count: {checks} "~5" BLUE "vk check" (2 of them tagged "--frames"); {images} "~5" GOLD image tiles; {write} "1" GREEN "Write", with a DIM "Edits: ~0" beside it.
> {shell}: a group "~13 other shell calls"; {lookups} "~9" of them turn RED "lookup", with a small breakdown "engine library 2.7 · Manim source 1.2 · other scenes 1.1 · misc 3.8"; {patches} "~2" tagged "patch".
> {peak}: the tile groups slide up and shrink; a tall stacked bar, "peak ≈ 132k", builds from the bottom in GOLD shades as spoken: {startup} "startup 12k", {imgs} "images 15k (5 × ~3k)", {tool} "tool output 11k", {files} "writes and patches 8k"; {think} a big RED segment fills the rest to the top, "thinking ≈ 80k".
> {surprise}: YELLOW "thinking ≈ 60% of the peak". {suspect}: the images segment gets a DIM tag "the old suspect: ≈ 10%".
> {dollars}: a second bar beside it, "a builder's dollars": RED "output (mostly thinking) ≈ ½", {writes} GOLD "cache writes ≈ 30%", {reads} GREEN "re-reading ≈ 15%". {biggest}: the RED parts of both bars pulse together.
> {two}: two YELLOW questions with arrows: "think less?" to the RED thinking segment, {look} "look up less?" to the 9 RED lookup tiles. Both stay for s6's dials.

[c2.anat.1] {open} So what fills a builder's context? Let's open up a typical build. {tiles} Here are its turns, grouped by kind, in typical counts. {checks} About five are vee-kay check runs, {images} and about five read an image. {write} One writes the whole scene file, and the median number of edits is zero. {shell} About thirteen are other shell calls. {lookups} About nine of those are lookups, in the engine library, Man-im's source, other scenes, and odds and ends. {patches} And about two patch the file.

[c2.anat.2] {peak} Now stack up its peak context, about a hundred and thirty-two thousand tokens. {startup} Twelve thousand to start. {imgs} About fifteen thousand of images. {tool} Eleven thousand of tool output. {files} Eight thousand of file writes and patches. {think} And the rest, about eighty thousand, is thinking. {pause}

[c2.anat.3] {surprise} That's the surprise. Thinking is about sixty percent of the peak. {suspect} Images, the old suspect, are only about ten percent. {dollars} And the dollars? Output, mostly thinking, is about half. {writes} Cache writes are about thirty percent, {reads} and re-reading about fifteen. {biggest} Thinking is the biggest single cost. {pause} {two} So, two questions. Can it think less? {look} And can it look things up less?

## Scene 6 · Two dials: the model and the effort (ch2_s6_dials)

> One BLUE builder box, centre, with two dials on its face: "model" (BLUE "Opus", PURPLE "Sonnet") and "effort" (needle at the default). Above the box, the builder type's real frontmatter line in Mono, `model: opus` (verbatim from source/agent-scene-builder.md, line 5).
> {model}: dial 1 lights; s1's card 1 returns small: "Can any step run on Sonnet instead of Opus?". {only}: a mini master shot, the builders' row lit, GOLD "≈ 80% of what today's four agent types spend ($278 of ~$344)". {gates}: planner, writer and director boxes get GREEN tags "judgment gate" (plan, teaching, review) and a BLUE "Opus" lock.
> {same}: two cost bars side by side, BLUE "Opus $278" and PURPLE "Sonnet $159": GREEN reads $40.8 on both, GOLD writes $85.5 → $42.75, RED output $152 → $76 (from the type table's 204M / 17.1M / 7.6M; checked in Python 3.11.9). {halve}: the GOLD and RED parts shrink to half; GREEN "≈ 43% less".
> {catch}: YELLOW "only if it takes the same number of turns". {bench}: "SWE-Bench Pro: Sonnet 5.5 ≈ 81, Opus ≈ 90". {grow}: a PURPLE staircase (s2 styling) grows extra steps outlined RED ("extra check runs", "review rounds") while its cost bar rises to meet the BLUE one. {under}: DIM caveat "transcripts may undercount output → Sonnet's saving would be larger".
> {fix}: a small fix-pass builder icon turns PURPLE; {safe} GREEN "the safe place for Sonnet". {prod}: the producer box gets a DIM "Sonnet? small saving: lean now".
> {effort}: dial 2 lights, "effort level: how much it thinks before it acts"; {tuned} DIM "set per agent type · never tuned". {direct}: an arrow from the dial to s5's RED "thinking ≈ 80k" segment. {again}: the RED segment shrinks while RED-outlined extra check steps appear beside it.
> {measure}: both dials get a YELLOW tag "measure it". It pays off in s8.

[c2.dials.1] {dials} Two dials sit on the builder's box. {model} The first is the model, your first question. {only} Only the builders matter here, about eighty percent of what today's four agent types spend. {gates} The planner, writer and director are small, and they're the judgment gates, so they stay on Opus.

[c2.dials.2] {same} Now take the same tokens and price them at Sonnet's rates. {drop} Two hundred and seventy-eight dollars becomes a hundred and fifty-nine, about forty-three percent less. {bars} The green re-reading is identical. {halve} The gold and red parts are cut in half. {pause}

[c2.dials.3] {catch} But that holds only if Sonnet finishes in the same number of turns. {hard} Building a scene is the hardest job here, Man-im code plus judging a layout from the beats image. {bench} And on hard coding, Sonnet five point five trails Opus most, about eighty-one against ninety on one benchmark. {grow} Each extra check run or review round adds steps to its staircase, until the cost catches up. {under} One caveat cuts the other way. If the transcripts undercount output, Sonnet saves more.

[c2.dials.4] {fix} Fix passes are well scoped. They apply the notes and check again, {safe} so they're the safe place for Sonnet. {prod} The producer could run on Sonnet too, but it's lean now, so the saving would be small.

[c2.dials.5] {effort} The second dial is effort level, how much the model thinks before it acts. {tuned} It's set per agent type, and it has never been tuned. {direct} It hits thinking directly, the biggest single cost. {again} The same catch applies. Thinking less might mean more check runs and fix rounds. {measure} Neither dial can be set by argument. It has to be measured.

## Scene 7 · A second opinion (ch2_s7_second)

> A board titled "Gemini's review · each claim checked against the code and transcripts". Idea cards appear neutral (white outline) and turn GREEN (held up) or RED (didn't) on their verdicts; one DIM card comes last.
> {skip}: "skip the render + beats image while the lint has flags" → GREEN; {small} tag "≈ 1–2 image reads a build · 3–5% · cheap". {voice}: "several-model voice check inside vk voice" → GREEN, YELLOW star "best idea: quality". {lived}: a TEAL page "LESSONS.md" with a DIM stamp "directors: don't read".
> {holds}: "vk holds: summed audio durations, sampled 0.4 s before each clip's end" → GREEN. {worse}: tag "worse than stated"; a small row of holds tiles slips one notch off after a RED marker "animation outside a say block".
> {reject}: three cards turn RED as spoken, each with its reason: {skeleton} "pre-made skeletons + a shared helper file per chapter" ("~1k tokens of boilerplate · breaks: builders never share files"); {edits} "many small Edit calls" ("median 0 · real waste: ~9 lookups"); {cap} "a 12–15 turn cap" ("arbitrary · turns aren't the main cost").
> {agreed}: a small GREEN card "Sonnet for fix passes: agreed". {missed}: a DIM card "effort level", stamped "missed".
> {changes}: the three GREEN adopted cards slide into a numbered list, "Changes made 2026-10-27": {c1} "1  vk voice: several Whisper models must agree; flagged sentences kept with what was heard, and listed" / {c2} "2  vk holds: each frame from the render's real timings" / {c3} "3  builder prompt: the library's complete signatures · vk check: no render while overrun, sync or layout flags remain". Leave the command that lists flagged sentences unnamed on screen.
> Under item 3, an overrun case as the current engine/tools/check.py prints it (format strings at lines 216–217, 336 and 346, read 2026-10-27; not a real run, so `<clip>` and `<n>` are DIM placeholders and no scene is named), Mono, two lines: `  overrun: <clip>: the block runs <n> s past its clip (the next clip starts late: shorten run_times or cue earlier)` / `  render and beats image skipped until the audit is clean (--render-anyway to render with these flags)`. Dwell flags no longer block the render, so don't use a dwell example.

[c2.second.1] {gemini} You also asked another AI model, Gemini, to review the pipeline. {checked} Each claim was checked against the code and the transcripts. {board} Green means it held up, red means it failed.

[c2.second.2] {skip} First, skip the render and beats image while the lint has flags. True, since the check used to render anyway. {small} A small saving, three to five percent, and cheap. {voice} Second, run the several-model voice check inside vee-kay voice. True, and its best idea, for quality rather than tokens. {lived} That check lived only in a lessons file that directors are told not to read, so it had probably stopped running.

[c2.second.3] {holds} Third, vee-kay holds guessed each clip's time by adding up audio durations, and sampled just before each clip's end. {worse} True, and worse than it said. Any animation outside a self dot say block shifted every later tile.

[c2.second.4] {reject} Three ideas did not hold up. {skeleton} Pre-made skeleton files and a shared helper file per chapter. Builders already write the file in one go, and a shared file breaks the rule that keeps parallel builds safe. {edits} Many small edits? Wrong, the median is zero. The real waste is the nine lookups. {cap} And a turn cap of twelve to fifteen is arbitrary. Turns are not the main cost.

[c2.second.5] {agreed} It agreed on Sonnet for fix passes, {missed} and missed effort level entirely. {changes} Three changes came out of this review. You saw them in part one as simply how things work. {c1} The voice check with several models. {c2} Holds from the render's real timings. {c3} And a builder prompt with the library's complete signatures, which ends the lookups, plus a check that skips the render while there are flags to fix.

## Scene 8 · The levers, this video as the test, and recap (ch2_s8_test)

> A board "The levers, ranked", each with a small icon from its scene: {thinking} "1  thinking → effort level" (s5's RED segment), {model} "2  the model" (s6's dial), {turns} "3  turns → fewer lookups, no renders while must-fix flags remain" (s5's tile row), {context} "4  context → images only ≈ 10%" (an image tile).
> {habits}: a GREEN column "Habits that already save": {notes} "fix notes within the hour, or a fresh builder ($0.25), not a cold 300–400k agent", {lean} "a lean producer (once 38% of a lecture)", {onedir} "one director at a time (two at once ≈ half the wall time)".
> {keep}: a BLUE column "Don't cut": "planner, writers, directors ≈ 10% · the gates", {startup} "agent startup ≈ $0.01". {caveats}: three DIM lines: {rel} "dollars: Opus list prices, a relative weight", {disk} "counts: transcripts on disk (nearly all)", {plan} "how the plan weighs Sonnet vs Opus: not published".
> {test}: the boards clear. {scenes}: 16 scene boxes in two rows, ch1 s1–s8 and ch2 s1–s8 (stems in Mono), each with a grey "?" builder icon. A legend beside them, lighting on its words: {asnow} BLUE "Opus as now", {lower} dimmed BLUE "Opus at lower effort", {sonnet} PURPLE "Sonnet", with a DIM "rotated across scenes". Never map a variant to a scene. {watching}: a YELLOW outline on the ch2_s8_test box, "you are here", its icon still "?".
> {measure}: a GOLD meter "cost per finished scene", fed by three DIM inputs "fix passes", "check runs", "review notes". {status}: it points to an empty TEAL page "STATUS.md", "results go here". No values, bars, rankings or ticks: nothing that hints at an outcome.
> {recap}: ch1's master shot returns, small on the left; on the right, one line per recap sentence, each lighting the part it names: {r1} the crew and its TEAL file hand-offs; {r2} s2's GREEN / GOLD / RED staircase, small; {r3} "scene work ≈ 78%"; {r4} the two dials; {r5} the review board, "3 changes".
> {next}: a YELLOW card "Your next step": "when the results are in STATUS.md, choose the default model and effort for the builders, and for the fix passes". Then the end card: leave ~8 s after the last word; the music carries it.

[c2.test.1] {levers} Here are the levers, ranked. {thinking} First, thinking, through effort level. {model} Second, the model. {turns} Third, turns, with fewer lookups and no renders while there are flags to fix. {context} Last, context, where images are only about ten percent.

[c2.test.2] {habits} Some habits already save. {notes} Fix notes go out within the hour, or to a fresh builder for twenty-five cents, rather than waking a cold agent. {lean} The producer stays lean, after once costing thirty-eight percent of a lecture. {onedir} And one director runs at a time, to keep usage bursts down.

[c2.test.3] {keep} Keep the planner, the writers and the directors. Together they're about ten percent, and they're the gates that stop expensive rework. {startup} And an agent's startup, about a cent, is not worth cutting. {caveats} Three caveats. {rel} The dollars are at Opus list prices, a relative weight. {disk} The counts cover the transcripts on disk, which is nearly everything. {plan} And how your plan compares Sonnet usage with Opus usage is not published.

[c2.test.4] {test} And this video is the test. {scenes} Its sixteen scenes were built three ways, rotated across scenes. {asnow} Opus as now, {lower} Opus at lower effort, {sonnet} and Sonnet. {watching} The scene you're watching was built by one of them. {measure} Afterwards, each way is measured by its cost per finished scene, including fix passes, check runs and review notes. {status} The results go in the status file.

[c2.test.5] {recap} Let's recap both parts. {r1} A crew of agents hands work over through files, with a loop per scene and a review per chapter. {r2} Cost is roughly turns times context, and the dollars sit in output, mostly thinking, and in cache writes. {r3} Scene work is about seventy-eight percent, and fewer builders would cost more. {r4} Two dials, the model and the effort, have to be measured. {r5} And a second opinion led to three changes. {pause}

[c2.test.6] {next} There's no part three, so here's your next step. Once the results are in the status file, choose the default model and effort for the builders, and for the fix passes.
