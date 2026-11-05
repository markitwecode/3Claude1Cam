# Chapter 4 · Paths of any length

Databases, Lecture 5 (Graph databases), part 4 of 6. Source: lecture notes ch. 5, §5.2, pp. 56–57 (Slide 107); handout p. 114; recording 40:44–45:53.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch4_s1_hook)

> Chapter conventions (PLAN.md Decisions): every vertex a circle, Person PINK, Movie BLUE, edge
> types in small caps along the arrow, the matched pattern YELLOW, counts GOLD. Cypher Code in
> `cypher`; SQL Code with `lang="sql"`. Every query and reply in this chapter was run on 2026-11-01:
> Cypher in Kleppmann's cypher-shell (Traverse engine, node v24.2.0) on `source/movies.tvdb`, SQL in
> DuckDB v1.5.6 on `source/movies.duckdb`. Titles exactly as stored ("Mockingjay - Part 1", plain hyphen).
> Title card: "Graph Databases", "Databases · Lecture 5", "Part 4 · Paths of any length".
> {costar}: ch3's co-star pattern returns as Code, the two ends filled in with names (verified):
> `MATCH (a:Person {name: 'Jennifer Lawrence'}) -[:ACTED_IN]-> (m:Movie)` /
> `      <-[:ACTED_IN]- (b:Person {name: 'Daniel Radcliffe'})` / `RETURN m.title;`
> {none}: the reply, an empty table with header `m.title` and the line `0 rows` (GOLD 0).
> {chain}: the code shrinks to the top; ch1 s1's shot comes back: PINK Lawrence left, PINK Radcliffe
> right, a dashed chain between them with a YELLOW "?" in the middle.
> {bacon}: the pair slides aside; a PINK "Kevin Bacon" vertex at centre; {rules} four or five PINK
> actors appear around it, each joined to him by a dashed chain of a different length;
> {unknown} a GOLD "?" on each chain. {question}: YELLOW line under it: "a chain of unknown length?"

[c4.hook.1] {title} This is part four of our lecture on graph databases. {last} Last time, we matched two actors who share a movie, and counted the films they made together. {costar} Now try that pattern on Jennifer Lawrence and Daniel Radcliffe. {none} It finds nothing. Zero rows. {pause} She's Katniss in The Hunger Games, he's Harry Potter, and in our data, the two of them have never been in a film together. {chain} And yet, a chain of co-stars links them.

[c4.hook.2] {bacon} There's a game built on chains like this, called Six Degrees of Kevin Bacon. {rules} Connect any actor to Kevin Bacon, through as short a chain as you can, of actors who appeared in the same movie. {unknown} The catch is that you don't know in advance how long the chain will be. {question} So how do you ask a database for a chain whose length you don't know? {pause}

## Scene 2 · Chains of co-stars (ch4_s2_chains)

> The running example of s2–s4, a horizontal chain filling the frame's width: PINK "Jennifer
> Lawrence" → BLUE "The Hunger Games: Catching Fire" ← PINK "Woody Harrelson" → BLUE "Now You See
> Me 2" ← PINK "Daniel Radcliffe", every edge labelled ACTED_IN in small caps, arrowheads on.
> {two}: first only Lawrence, Catching Fire and Harrelson; GOLD counters "1", "2" tick on the two
> arrows, brace "length 2 = co-stars". {three}: Now You See Me 2 and Radcliffe join on the right;
> counters "3", "4", brace "length 4 = a co-star in common".
> {alt}: the arrowheads flash YELLOW one by one, small tags under them "→ ← → ←". {fixed}: one
> edge pattern `-[:ACTED_IN]->` slides along the chain as a stamp: GREEN on the 1st edge, RED on the 2nd.
> {drop}: Code `-[:ACTED_IN]->` loses its `>` → `-[:ACTED_IN]-` (ch2 s5's either-direction form);
> the chain's arrowheads fade to plain lines.
> {query}: Slide 107, hero Code (verified): `MATCH path = (a:Person {name: 'Jennifer Lawrence'})` /
> `             -[:ACTED_IN*4]-` / `             (b:Person {name: 'Daniel Radcliffe'})` /
> `RETURN count(path);`. {path}: `path =` YELLOW, a YELLOW outline wraps the whole chain;
> {star}: a highlight box on `*4` inside the brackets, `*4` turns GOLD; {meaning}: its "4" flies
> onto the chain's four edges, which glow YELLOW in turn. {eight}: reply table, header
> `count(path)`, value `8` (GOLD), `1 row`. The chain shrinks and stays up for s3.

[c4.chains.1] {start} Let's build up from what we know. {two} Jennifer Lawrence and Woody Harrelson share a movie, Catching Fire. {count2} To get from her to him, you follow two arrows. So co-stars are joined by a path of length two. {three} Now add Daniel Radcliffe, who made Now You See Me Two with Harrelson. {four} From Lawrence to Radcliffe, that's four arrows. {common} A path of length four joins two actors who have a co-star in common.

[c4.chains.2] {dirs} Now look at the directions. {alt} Every acted-in edge points from a person to a movie, so along the chain, the arrows alternate: forward, backward, forward, backward. {fixed} The star we're about to meet repeats one edge pattern. If every step had to point the same way, the first edge would fit, and the second would fail. {drop} But remember the arrow with no heads, from part two. It matches an edge in either direction, {either} which is exactly what a chain of co-stars needs.

[c4.chains.3] {query} Here's the query. {path} It starts with path equals. That gives the whole matched path a name, so we can return it, or count it. {ends} Then the two ends, Lawrence and Radcliffe. {star} And between them, acted-in, star four, with no arrowheads. The star and the number go right after the edge type, inside the square brackets. {meaning} Without them, this would be a single edge. With them, it's a path of four acted-in edges in a row, each in either direction. {run} Count the paths, {eight} and there are eight. {pause}

## Scene 3 · Why the length is always even (ch4_s3_even)

> The s2 chain, small, at the top. {odd}: a GOLD "length 3?" hovers over it. {sides}: main
> stage, two banks, a PINK column "people" on the left (Lawrence, Harrelson, Radcliffe and three or four more), a BLUE column "movies" on the right
> (Catching Fire, Now You See Me 2 and a few more); a dozen ACTED_IN lines, each crossing between
> the banks. {five}: five type names in small caps (ACTED_IN, DIRECTED, PRODUCED, WROTE,
> COMPOSED_FOR), each with a short arrow "person → movie". {bipartite}: YELLOW label "bipartite".
> {walk}: a YELLOW token leaves Lawrence and hops bank to bank; GOLD step counter 1, 2, 3, 4; the
> side it lands on lights up (BLUE, PINK, BLUE, PINK). {even}: "people ⇔ even" in YELLOW.
> {query}: Code (verified): `MATCH path = (a:Person {name: 'Jennifer Lawrence'})` /
> `             -[:ACTED_IN*3]- (x)` / `RETURN labels(x) AS label, count(path) AS paths;` and its
> reply, header `label | paths`, row `['Movie'] | 1353`, `1 row` (GOLD 1353, BLUE ['Movie']).
> {impossible}: a strip of five pills between the two actors: `*2` 0 · `*3` 0 · `*4` 8 · `*5` 0 ·
> `*6` 495 (all verified). `*3` and `*5` get RED "impossible"; {two}: `*2` gets a DIM "never shared a
> film"; {four} `*4` and {six} `*6` turn GOLD. {half}: back on the small chain, its two movies glow
> BLUE, "4 edges = 2 movies".

[c4.even.1] {question} Notice that the lengths we used were two and four. {odd} Could there be a path of length three between two actors? {pause} {sides} Here's how to see it. Put all the people on the left, and all the movies on the right. {cross} Every acted-in edge joins a person to a movie, so it crosses from one side to the other. {five} In fact, all five edge types do. {bipartite} A graph like this, with two sides, and every edge crossing between them, is called bipartite.

[c4.even.2] {walk} Now walk a path from Jennifer Lawrence. {s1} After one edge, you're on the movie side. {s2} After two, you're back among the people. {s3} After three, movies again. {flip} Every step flips the side. {even} So you're among the people exactly when the number of steps is even. {pause}

[c4.even.3] {check} We can check that. {query} Ask for paths of three edges from her to any vertex at all, call it ex, and count them by the labels of ex. That's a list, because a vertex may have more than one label. {reply} One thousand, three hundred and fifty-three paths, and every single one ends on a movie. {impossible} So star three and star five find nothing between two actors. Not by chance, but by necessity.

[c4.even.4] {two} Star two also finds nothing, but for a different reason. A path of length two is a shared movie, and these two never shared one. {four} Star four gives eight, {six} and star six, four hundred and ninety-five. {half} And since every hop from one actor to the next takes two edges, the number of movies in a chain is half the length of the path. {bacon} Taking half the length is how we'll measure the distance between actors, in Bacon numbers, in the next part.

## Scene 4 · Where the eight come from (ch4_s4_count8)

> Code: s2's query with the last line changed to `RETURN path;` (verified: 8 rows; Traverse draws
> them). {draw}: a deliberately tangled Traverse-style drawing of the 8 paths (shared vertices
> pulled together, edges crossing); {untangle}: it untangles into a layered layout: PINK Lawrence
> far left, PINK Radcliffe far right, three PINK middles in a column at the centre (Woody Harrelson, James McAvoy, Domhnall Gleeson), BLUE films
> between. Verified (cypher-shell, the path's vertices 1–3):
> Harrelson: left "The Hunger Games: Catching Fire", "The Hunger Games: Mockingjay - Part 1",
> "The Hunger Games: Mockingjay - Part 2"; right "Now You See Me 2".
> McAvoy: left "X-Men: First Class", "X-Men: Days of Future Past", "X-Men: Apocalypse",
> "X-Men: Dark Phoenix"; right "Victor Frankenstein".
> Gleeson: left "Mother!"; right "Harry Potter and the Deathly Hallows: Part 2".
> {first}: a DIM dashed BLUE "The Hunger Games" beside Harrelson's fan, no edge to him; caption
> "stored cast: 10 actors, Harrelson not among them" (verified). {mult}: GOLD "3 × 1" by
> Harrelson as the 3 paths light YELLOW one at a time; {vf} "4 × 1"; {domhnall} "1 × 1".
> {sum}: the three products slide together, `3 × 1 + 4 × 1 + 1 × 1 = 8`, the 8 in GOLD.
> {rule}: two short YELLOW lines, {times} "along a path: multiply" / {plus} "different middles: add".
> {placement}: one path lifts out and is laid on ch2 s3's placement picture (pattern in YELLOW on
> the graph), tag "1 path = 1 placement = 1 row".

[c4.eight.1] {draw} Return the path itself instead of its count, and Traverse draws all eight paths. It's a tangle, because the same people and films turn up in several of them. {untangle} Let's untangle it. {mid} Every path has a person in the middle, who acted with Lawrence, and also with Radcliffe. {three} There are only three of them: Woody Harrelson, James McAvoy, and Donal Gleeson. {pause}

[c4.eight.2] {woody} Take Woody Harrelson. {hg} He's with Lawrence in three Hunger Games films: Catching Fire, and both parts of Mockingjay. {first} He was in the first film too, but our data keeps at most ten actors per film, and his name isn't among them. {nysm} With Radcliffe, he has just one film, Now You See Me Two. {mult} So a path through him picks one of three films on the left, then the one film on the right. Three times one, three paths.

[c4.eight.3] {james} James McAvoy is with Lawrence in four Ex-Men films, {vf} and with Radcliffe in one, Victor Frankenstein. Four times one, four paths. {domhnall} Donal Gleeson has one film with each, the film Mother, and the last Harry Potter. One path. {sum} Three, plus four, plus one. Eight. {pause}

[c4.eight.4] {rule} So here's the rule for counting paths. {times} Choices along a path multiply. {plus} Paths through different middles add. {placement} Each path is one placement of the pattern on the graph, and one row of the answer, just like the matches in part two. {why} And it's that multiplying that makes these numbers grow so fast, as we're about to see.

## Scene 5 · The explosion (ch4_s5_explode)

> Ranges first, Code beside s2's query: `-[:ACTED_IN*2..6]-` with reply `count(path)` = `503`
> (verified), and under it GOLD `0 + 8 + 495 = 503`. {upto}: `*..4` (verified: 8 between the two),
> DIM note "1 to 4". {bare}: `*` alone, "1 or more", a GOLD "?" over it.
> {anyone}: clear; Radcliffe fades, Lawrence at left. A table builds row by row, columns
> "length" | "paths" | "different people at the end": 2 | 153 | 117 · 4 | 12,160 | 3,985 ·
> 6 | 700,512 | 12,686 · 8 | 39,584,716 | 14,072. {one}: on the first row, her 17 BLUE films fan out,
> each with 9 PINK co-star dots: GOLD `17 × 9 = 153`. {factor}: GOLD "× 79", "× 58", "× 57" arcs
> between the paths rows (12,160 / 153 ≈ 79.5, 700,512 / 12,160 ≈ 57.6, 39,584,716 / 700,512 ≈ 56.5).
> Footnote DIM: "lengths 6 and 8 counted outside Traverse, with Cypher's rules".
> {curve}: the table becomes a plot, log-scale y axis (labelled "log scale"), x = path length 2–8:
> GOLD "paths" rising steadily, PINK "people" bending flat under a dashed ceiling "14,581 connected
> to her (counting herself)" (BFS, verified). {per}: GOLD "≈ 2,800 paths per person" at x = 8
> (39,584,716 / 14,072 ≈ 2,813). {pause} holds on the two curves.
> {crash}: Code (verified): `MATCH path = (a:Person {name: 'Jennifer Lawrence'})` /
> `             -[:ACTED_IN*6]- (b:Person)` / `RETURN count(path);` and the shell's reply in RED,
> verbatim: `Error: unreachable`. Tag DIM: "the engine gave up; it says nothing about the graph".
> {barecrash}: the `*6` line becomes `-[:ACTED_IN*]- (b:Person {name: 'Daniel Radcliffe'})`; the same
> RED `Error: unreachable` (verified).
> {lesson}: `*` returns, the GOLD "?" replaced by "a very large number of paths" (the notes' words).

[c4.explode.1] {fixed} So far, the length was fixed. {range} A range lets it vary. {twosix} Star two, dot, dot, six, means between two and six edges. Between our two actors, that's zero, plus eight, plus four hundred and ninety-five. {total} That's five hundred and three paths. {upto} Leave out the first number, as in star, dot, dot, four, and it means from one up to four. {bare} And a star on its own means any length, from one edge up. {pause} {how} But how many paths could that be?

[c4.explode.2] {anyone} Let's let go of Radcliffe, and count the paths from Lawrence to anyone. {one} She has seventeen films, each with nine other actors, so there are seventeen times nine, a hundred and fifty-three, paths of length two. {grow} Length four, about twelve thousand. {six} Length six, seven hundred thousand. {eight} Length eight, nearly forty million. {factor} Each path can carry on through any other film of the actor it reached, and then to any of that film's other actors. So every extra hop multiplies the count, here by about eighty, then sixty, then sixty again.

[c4.explode.3] {people} Now count something else: the different people at the far end. {grow2} A hundred and seventeen, then about four thousand, then twelve and a half thousand, then fourteen thousand. {curve} That curve flattens out. {ceiling} Counting herself, only fourteen thousand, five hundred and eighty-one actors are connected to her at all. {runout} The paths keep multiplying, but the people run out, so more and more paths lead to the same people. {per} At length eight, that's nearly three thousand paths, on average, for every person reached. {pause}

[c4.explode.4] {outside} Those last two path counts didn't come from Traverse. {crash} Ask the shell for every path of length six, from her to anyone, and it gives up, with the message, error, unreachable. {meaning} That's the engine falling over, not a statement about the graph. {barecrash} A star on its own, between Lawrence and Radcliffe, makes it give up in the same way. {lesson} So a bare star is easy to write, but it can mean a very large number of paths.

## Scene 6 · Six joins (ch4_s6_joins)

> Hero Code, `lang="sql"` (verified, DuckDB v1.5.6):
> `SELECT count(*) AS paths` / `FROM   people AS a` /
> `JOIN   has_position AS h1 ON h1.person_id = a.person_id` /
> `JOIN   has_position AS h2 ON h2.movie_id  = h1.movie_id` /
> `JOIN   has_position AS h3 ON h3.person_id = h2.person_id` /
> `JOIN   has_position AS h4 ON h4.movie_id  = h3.movie_id` /
> `JOIN   people AS b        ON b.person_id  = h4.person_id` /
> `WHERE  a.name = 'Jennifer Lawrence'` / `  AND  b.name = 'Daniel Radcliffe'` /
> `  AND  h1.position = 'actor' AND h2.position = 'actor'` /
> `  AND  h3.position = 'actor' AND h4.position = 'actor';` → reply `paths` = `8`.
> {edge}: beside it, s2's chain small; each of its four edges colour-matched to its `has_position`
> line (h1–h4), the two end circles to the two `people` lines. {six}: two more JOIN lines slide in,
> `JOIN   has_position AS h5 ON h5.person_id = h4.person_id` /
> `JOIN   has_position AS h6 ON h6.movie_id  = h5.movie_id`, b's line becomes
> `JOIN   people AS b        ON b.person_id  = h6.person_id`, and a third filter line
> `  AND  h5.position = 'actor' AND h6.position = 'actor';` (the `;` moves to this new last line;
> verified as a whole) →
> {wrong}: reply `paths` = `1085` in RED, beside GOLD "Cypher: 495".
> {bounce}: a walk drawn PINK/BLUE: Lawrence → Mother! → Domhnall Gleeson, then a RED marker going
> back and forth along the Gleeson–Mother! edge, then on → Harry Potter and the Deathly Hallows:
> Part 2 → Radcliffe; six GOLD step numbers; RED tag "same edge again".
> {loop}: GREEN example: Lawrence → Silver Linings Playbook → Bradley Cooper → American Hustle →
> Lawrence, a loop of four different edges (verified, one of 112 length-4 paths back to her).
> {sqlfix}: DIM caption under the SQL: "+ conditions: no has_position row used twice".
> {fourok}: the four-join block's `8` turns GREEN, tag "a step back would need both in one film".
> {union}: three small stacked query blocks "2 joins", "4 joins", "6 joins" glued by `UNION ALL`.
> {question}: everything dims; YELLOW "shortest chain, however long?", then {joins} a GOLD "? joins".
> {cypher}: two small tags: BLUE "Cypher: next chapter", DIM "SQL: recursive queries, next lecture".

[c4.joins.1] {sql} What would all this look like in sequel? {edge} Every edge in a path is a join with has position. {four} So star four between our two actors is has position four times, each one restricted to actors, plus the people table twice, for the two names. {run} Duck D B agrees: eight. {six} Star six needs six joins. Painful, but possible.

[c4.joins.2] {careful} But careful. Write those six joins the obvious way, {wrong} and the answer is one thousand and eighty-five, not four hundred and ninety-five. {why} Why the difference? {pause} {bounce} Because sequel is happy to step back along the edge it just used. Lawrence, the film Mother, Donal Gleeson, then back and forth along that same edge, and on through the last Harry Potter to Radcliffe. {six2} That's six steps. {rule} Cypher never counts it, because a path never uses the same edge twice.

[c4.joins.3] {vertex} A vertex, though, may come back. {loop} A hundred and twelve paths of length four lead from Lawrence back to herself, like this one, through Silver Linings Playbook, Bradley Cooper, and American Hustle. {distinct} Four different edges, so it counts. {sqlfix} To match Cypher, the sequel needs extra conditions, saying that each row of the has position table is used at most once. {fourok} With four joins, the answer happened to be right, because any step back would need our two actors in the same film.

[c4.joins.4] {union} A range is worse. Star two, dot, dot, six, is one such query for each even length, two, four and six, glued together with union all. {shortest} And then comes the real problem. {question} What about the shortest chain between two actors, however long it turns out to be? {pause} {joins} How many joins would you write? {unknown} You can't know, until you've found the chain. {pause} {cypher} Cypher has an answer, coming next. Sequel will need a new tool, recursive queries, in the next lecture.

## Scene 7 · Recap (ch4_s7_recap)

> One row of small panels, each a shrunken copy of the visual that taught it, its line underneath;
> they appear one per sentence and stay:
> {r1}: s2's chain Lawrence → Catching Fire ← Harrelson → Now You See Me 2 ← Radcliffe, arrowheads
> fading, `-[:ACTED_IN*4]-` under it; line "no arrowheads, star four".
> {r2}: s3's two banks, PINK and BLUE, with the token's zigzag; line "every step flips the side".
> {r3}: s4's layered drawing with `3 × 1 + 4 × 1 + 1 × 1 = 8` in GOLD; line "multiply along, add across".
> {r4}: s5's log plot, GOLD paths rising, PINK people flat under the ceiling; line "paths explode,
> people level off".
> {r5}: s6's SQL block with the RED `1085`; line "one join per edge, no edge twice".
> {next}: panels dim; s5's `*2..6` reply `503` in GOLD, one YELLOW path picked out of a tangle,
> then a GOLD "?" for "without listing millions".
> End card after the last word: hold about 8 s on the series title, music carries it.

[c4.recap.1] {recap} Let's recap. {r1} A chain of co-stars alternates direction, so we drop the arrowheads, and star four asks for four edges in a row. {r2} Every edge crosses between people and movies, so paths between actors have even length. {r3} Choices along a path multiply, and different routes add: three, plus four, plus one, makes eight. {r4} So path counts explode, while the number of people levels off. {r5} And in sequel, every edge is a join, and you have to rule out using an edge twice yourself. {pause}

[c4.recap.2] {next} Of those five hundred and three paths between Lawrence and Radcliffe, we usually want just one, the shortest. {tease} Next time, we'll find it, without listing millions of paths. {pause}
