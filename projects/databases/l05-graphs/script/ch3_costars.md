# Chapter 3 · Co-stars: bigger patterns and counting

Databases · Lecture 5 (Graph Databases), part 3 of 6. Source: lecture notes ch. 5, pp. 55–56 (§5.1, Slide 106; the setting of Exercise 21); handout p. 113; recording 34:00–40:44.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch3_s1_hook)

> Title card: "Graph Databases", "Databases · Lecture 5", "Part 3 · Co-stars: bigger patterns and counting".
> "Last time" strip, small, from ch2's recap: a BLUE circle beside `(m:Movie)`, then Spielberg's pattern `(p:Person {name: 'Steven Spielberg'}) -[:DIRECTED]-> (m:Movie)` with its arrow linked by a line to two small join boxes ("an edge ≈ a join with has_position"). It clears.
> The question in YELLOW, centred: "Which pairs of actors have appeared together most often?"
> What SQL needs, as a diagram, never as a query (the full SQL is Exercise 21, solved in ch6): four table boxes in a row with BLUE headers, `people AS p1`, `has_position AS h1`, `has_position AS h2`, `people AS p2`. Three link lines between neighbours, labelled `h1.person_id = p1.person_id`, `h2.movie_id = h1.movie_id` (with a YELLOW tag "same movie"), `h2.person_id = p2.person_id`. Under each has_position box a small `position = 'actor'`. GOLD tally under the row: "4 tables · 3 join conditions". (Checked in DuckDB v1.5.6: these joins, with `p1.person_id < p2.person_id` and a GROUP BY on the names, give Slide 106's top five.)
> On "drawing a picture" a faint pencil sketch starts beside the boxes and stops half-way; a YELLOW "?" replaces it on the last question. The four boxes stay, dimmed, into scene 2.

[c3.hook.1] {title} This is part three of our lecture on graph databases. {pause} {last} Last time, you wrote your first patterns. Round brackets draw a vertex, an arrow draws an edge, and each edge in a pattern does the work of a join. {ask} Today's question is bigger. Which pairs of actors have appeared together in the most movies? {pause}

[c3.hook.2] {sql} Think about what sequel would need. {hp} Each actor's link to a movie is a row of the has position table, so you need two of those rows, {same} one per actor, with the same movie. {people} Then the people table, twice, for the two names. {four} That's four tables, held together by three joins. {draw} And to check it's right, you'd probably end up drawing a picture. {pause} {shape} So what does "two actors, one movie" look like, drawn as a pattern? {pause}

## Scene 2 · Two actors, one movie (ch3_s2_twoedges)

> The dimmed SQL boxes of scene 1 turn into the drawing (TransformFromCopy): the two people boxes become PINK circles p1 (left) and p2 (right), the has_position boxes become two arrows, and the "same movie" link becomes one BLUE circle m between them, both arrows pointing into it, ACTED_IN in small caps along each. The drawing moves to the top.
> Code below it, built in the lecturer's order, comma form: `MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie),` / `      (p2:Person) -[:ACTED_IN]-> (m:Movie)`. First the drawing splits into two one-edge drawings, one above each code line, each with its own m circle. On "same name" both `m` in the code flash YELLOW and the two m circles slide together and merge into one: the V comes back. p1 and p2 stay apart; on "promise nothing" a small grey "?" sits between them.
> Then line 3, `WHERE p1.person_id <> p2.person_id`, `<>` in YELLOW, and line 4, `RETURN p1.name, p2.name, m.title`.
> The run, on the house subgraph: The Kid (BLUE) in the middle, its ten actors in a ring of PINK circles, named as cypher-shell lists them: Charles Chaplin, Jackie Coogan, Albert Austin, Nellie Bly Baker, Edward Biby, Edna Purviance, Carl Miller, Beulah Bains, Henry Bergman, B.F. Blinn. The pattern, as ch2 s3's YELLOW stencil, lands with p1 on Chaplin and p2 on Coogan; the row drops into a table on the right; then p2 hops round the ring, one row per hop.
> The table, verbatim from cypher-shell (Traverse engine, node v24.2.0), headers `p1.name | p2.name | m.title`, first ten rows: `Charles Chaplin | Jackie Coogan | The Kid`, `Charles Chaplin | Albert Austin | The Kid`, `Charles Chaplin | Nellie Bly Baker | The Kid`, `Charles Chaplin | Edward Biby | The Kid`, `Charles Chaplin | Edna Purviance | The Kid`, `Charles Chaplin | Carl Miller | The Kid`, `Charles Chaplin | Beulah Bains | The Kid`, `Charles Chaplin | Henry Bergman | The Kid`, `Charles Chaplin | B.F. Blinn | The Kid`, `Jackie Coogan | Charles Chaplin | The Kid`. Then the shell's footer in GOLD: `261476 rows (showing the first 40)`.
> The fold: line 2's `(p2:Person) -[:ACTED_IN]-> (m:Movie)` is rewritten from the movie's end as `<-[:ACTED_IN]- (p2:Person)` (the arrowhead now on the left; in the drawing the p2 arrow doesn't move, it still points into m), then slides up onto the end of line 1; the second `(m:Movie)` and the comma fade. Result: `MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]- (p2:Person)` / `WHERE p1.person_id <> p2.person_id` / `RETURN p1.name, p2.name, m.title`. Each piece of the line lights up under its part of the drawing (person, arrow, movie, arrow, person).
> Both forms were run: the same 261476 rows, the same first rows. Keep the one-line query and the table on screen for scene 3.

[c3.two.1] {draw} Here's the picture. Two people and one movie, with an acted-in arrow from each person into the movie. {comma} The lecturer first wrote it as two small patterns, separated by a comma. {p1} The first says that pee one acted in a movie, em. {p2} The second says that pee two acted in a movie, em.

[c3.two.2] {same} Both patterns use the same name for the movie. {merge} In Cypher, the same name always means the same vertex, so the two movie circles become one, and both arrows must point into it. {diff} The people, on the other hand, have different names, but different names promise nothing. {free} Each is free to land on any person, and nothing so far says they're two different people. {where} So we add a condition, that the person ID of pee one is not equal to that of pee two. {pause}

[c3.two.3] {run} Now run it, returning both names and the movie's title. {kid} The first placement lands on The Kid, {chaplin} with Charles Chaplin as pee one, and Jackie Coogan as pee two. {hop} Then pee two moves on to each of Chaplin's other co-stars, {rows} and every placement is one more row. {total} Across the whole graph, that's over a quarter of a million rows, in well under a second.

[c3.two.4] {twice} Now look at the code, where the movie, em, is written out twice. {rewrite} So write the second edge starting from the movie. {left} The arrowhead now points left, but it's the same edge as before, from pee two into the movie. {attach} Hang it onto the end of the first pattern, {line} and you get one line, a person, an arrow, a movie, an arrow, a person. {same2} It gives exactly the same rows. {pause} {paper} It's the same query, drawn the way you'd draw it on paper, with one person on each side of the movie.

## Scene 3 · Every pair twice (ch3_s3_twins)

> Opens on scene 2's table and one-line query. Rows 1 and 10 get YELLOW boxes: `Charles Chaplin | Jackie Coogan | The Kid` and `Jackie Coogan | Charles Chaplin | The Kid`; a YELLOW "?" between them.
> The V pattern big in the centre (p1 PINK left, m BLUE, p2 PINK right). A dashed vertical mirror line through m; the pattern reflects onto itself, and only the labels p1 and p2 trade places. Then the same flip on The Kid: placement A (p1 on Chaplin, p2 on Coogan) and its mirror, placement B (p1 on Coogan, p2 on Chaplin), side by side, each with GREEN ticks for "Person", "ACTED_IN", "into m". Each placement points to its row in the table.
> Second example, small, verbatim from cypher-shell: `Daniel Radcliffe | Emma Watson | Harry Potter and the Sorcerer's Stone` and `Emma Watson | Daniel Radcliffe | Harry Potter and the Sorcerer's Stone`, then a row of eight little BLUE film circles (the eight Harry Potter films) each with a "×2".
> GOLD count: `261476` splits into `2 × 130738`.
> The WHERE line comes forward: `WHERE p1.person_id <> p2.person_id`. Both twins are tested: GREEN tick, GREEN tick, a GREY note "`<>` only rules out p1 = p2".
> The fix: `<>` morphs into `<` (one character, YELLOW). The two IDs appear on the PINK circles, as stored: Chaplin `nm0000122`, Coogan `nm0001067`. Placement A, `'nm0000122' < 'nm0001067'`: GREEN tick; placement B, the reverse: RED cross, and its row dims and slides out of the table, `Jackie Coogan | Albert Austin | The Kid` moving up into row 10. Third mini-case, one circle under both labels: `nm0000122 < nm0000122`, RED cross ("nobody is less than themself").
> New footer, GOLD: `130738 rows (showing the first 40)` (cypher-shell, the one-line form with `<`, checked). Final query on screen: `MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]- (p2:Person)` / `WHERE p1.person_id < p2.person_id` / `RETURN p1.name, p2.name, m.title`. The Kid's ring of ten stays for scene 4.

[c3.twins.1] {spot} Now look closely at those rows. {r1} The first one is Chaplin with Coogan. {r10} The tenth is Coogan with Chaplin. {pause} {why} The same two people, on the same movie, listed twice. Why? {pause}

[c3.twins.2] {shape} Look at the shape of the pattern. A person on each side, each with an arrow into the movie. {flip} Flip it like a mirror, and you get the same pattern back, with pee one and pee two trading places. {swap} So take any placement, swap the two people, and you get another placement, which obeys every rule just as well. {both} Chaplin with Coogan is a match, and so is Coogan with Chaplin.

[c3.twins.3] {potter} It happens to every pair, on every movie. Daniel Radcliffe and Emma Watson appear once in each order, on each Harry Potter film. {double} And the count agrees. Two hundred and sixty-one thousand, four hundred and seventy-six rows is exactly twice a hundred and thirty thousand, seven hundred and thirty-eight. {neq} Not-equal is no help here, because in both twins, the two people really are different. {only} All it rules out is a person paired with themself.

[c3.twins.4] {lt} The fix is a single character. Replace not-equal with less-than. {ids} Person IDs are short strings, and less-than compares them alphabetically. {pick} Of two different IDs, exactly one comes first, so exactly one twin survives. {self} And nobody's ID is less than their own, so less-than also rules out a person paired with themself. {pause}

[c3.twins.5] {once} Now each pair appears once per movie, {result} and the count is a hundred and thirty thousand, seven hundred and thirty-eight. {which} It makes no difference which twin survives. Less-than just picks one, the same way every time.

## Scene 4 · Predict the count (ch3_s4_predict)

> The Kid's ring of ten from scene 3, alone and larger, GOLD "45 rows" beside it (cypher-shell: 45 rows for The Kid with `<`, 90 with `<>`). A GOLD "how many?" over it.
> A caption under the ring: "at most 10 actors per movie: only the most prominent cast". Pairs drawn as chords: Chaplin's nine chords at once (GOLD "9"), then Coogan's eight new ones (GOLD "8"), then the rest in quick runs down to one. GOLD sum builds: `9 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1 = 45`, then `10 × 9 / 2 = 45`, labelled "10 choose 2".
> The ring shrinks into one tile of a grid of 2,935 tiny movie tiles; a GOLD ceiling `2935 × 45 = 132075`. Nearly every tile is full (DuckDB: 2,878 movies have exactly 10 actors, 56 have fewer, 1 has none); the few short ones flicker paler.
> SQL card (`Code(src, lang="sql")`), verbatim, run in DuckDB v1.5.6 on movies.duckdb: `SELECT sum(k * (k - 1) // 2) AS pairs,` / `       sum(k * (k - 1) * (k - 2) // 6) AS triples` / `FROM (SELECT movie_id, count(*) AS k` / `      FROM has_position` / `      WHERE position = 'actor'` / `      GROUP BY movie_id);`. Reply, verbatim: `┌────────┬─────────┐` / `│ pairs  │ triples │` / `│ int128 │ int128  │` / `├────────┼─────────┤` / `│ 130738 │  347841 │` / `└────────┴─────────┘`, the triples column covered for now. The pairs cell flies next to scene 3's `130738` and they match (GREEN).
> Trios: the V drawing returns. A third PINK circle p3 tries to join the end of the line and can't (both ends are people already, a RED flash on the line's ends); it comes in from below with its own arrow into m instead: a star with three arms. Code, verbatim: `MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]- (p2:Person),` / `      (p3:Person) -[:ACTED_IN]-> (m:Movie)` / `WHERE p1.person_id < p2.person_id AND p2.person_id < p3.person_id` / `RETURN count(*);`, the shared `m` YELLOW in both places.
> Six orderings of three PINK dots in a small grid, five dim, one GREEN (IDs increasing). GOLD "10 choose 3 = 120" on The Kid (cypher-shell: 120 trios for The Kid, checked).
> A strikethrough note "too slow to try?" (the lecturer's caution), replaced by cypher-shell's reply: `347841` in GOLD, with the shell's time `(1.7 s)`. The SQL card's triples column uncovers: `347841`, GREEN match.

[c3.predict.1] {kid} With less-than, The Kid gives forty-five rows. {guess} Could you have predicted that, without running anything? {pause} {clue} Here's a clue. This database keeps only the most prominent cast of each movie, at most ten actors, and The Kid has exactly ten. {chords} Chaplin pairs with the other nine, and Coogan with eight more, since his pair with Chaplin is already counted. And so on, down to one.

[c3.predict.2] {sum} Nine plus eight, and so on down to one, makes forty-five. That's ten times nine, over two, or ten choose two. {ceiling} So no movie gives more than forty-five pairs, and two thousand, nine hundred and thirty-five movies give at most about a hundred and thirty-two thousand. {most} Nearly all of them have the full ten actors, so the true count should sit just below that.

[c3.predict.3] {check} Let's check, in sequel, on the relational version of the database. Count each movie's cast, and add up the pairs it makes. {match} A hundred and thirty thousand, seven hundred and thirty-eight. Exactly the number of rows Cypher found. {pause} {meaning} So a match is nothing mysterious. It's every combination that fits the pattern, and you can count those combinations yourself.

[c3.predict.4] {three} What about three actors on the same movie? {ends} A pattern written as one line passes through the movie only once, with one arrow arriving from each side. {comma} So the third person needs a second pattern, after a comma, that shares the movie, em. {star} Now the pattern is a star, with three arms. Patterns can have any shape you like, not just a line.

[c3.predict.5] {orders} Three different people can be listed in six orders, and in only one of them are the IDs increasing. {chain} So the condition, pee one's ID below pee two's, and pee two's below pee three's, keeps each trio once. {per} Ten actors make ten choose three, a hundred and twenty trios. {dare} The lecturer was afraid to run this query live, worried it would take too long, or use too much memory. {result} In fact, it returns three hundred and forty-seven thousand, eight hundred and forty-one, in under two seconds, {sum3} exactly the trios that sequel counts. {pause}

## Scene 5 · Counting without GROUP BY (ch3_s5_aggregate)

> Starts from scene 3's final query. `m.title` in the RETURN line morphs into `count(*) AS movies` (GOLD), the names gain `AS name1` / `AS name2` (YELLOW), ORDER BY and LIMIT lines drop in, and the MATCH breaks over two lines: Slide 106, verbatim: `MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie)` / `      <-[:ACTED_IN]- (p2:Person)` / `WHERE p1.person_id < p2.person_id` / `RETURN p1.name AS name1, p2.name AS name2,` / `       count(*) AS movies` / `ORDER BY movies DESC, name1, name2` / `LIMIT 5;`.
> The result, verbatim from cypher-shell (checked, 581 ms), headers `name1 | name2 | movies`: `Daniel Radcliffe | Emma Watson | 8`, `Rupert Grint | Daniel Radcliffe | 8`, `Rupert Grint | Emma Watson | 8`, `Johnny Depp | Helena Bonham Carter | 7`, `Robert Downey Jr. | Scarlett Johansson | 7`; the 8s and 7s GOLD. A small grey footnote: "only the most prominent cast is stored".
> "Before counting": the Radcliffe–Watson rows stacked, verbatim (`p1.name | p2.name | m.title | m.year`): Harry Potter and the Sorcerer's Stone 2001, … and the Chamber of Secrets 2002, … and the Prisoner of Azkaban 2004, … and the Goblet of Fire 2005, … and the Order of the Phoenix 2007, … and the Half-Blood Prince 2009, … and the Deathly Hallows: Part 1 2010, … and the Deathly Hallows: Part 2 2011, each title as its own small placement (two PINK circles, one BLUE). The title column dims, the eight rows slide together and collapse into `Daniel Radcliffe | Emma Watson | 8`, the 8 GOLD.
> The rule: in the RETURN, `p1.name AS name1, p2.name AS name2` get YELLOW brackets "grouping keys", `count(*)` a GOLD bracket "aggregate". A ghost line `GROUP BY p1.name, p2.name` writes itself under the RETURN, the two names glowing in both places ("SQL: keys twice"), then fades to nothing ("implied").
> The test: `m.title,` slides back into the RETURN, before `count(*) AS movies`, and gets its own YELLOW bracket. New result, verbatim (checked): `David Arquette | Courteney Cox | Scream | 2`, `Neve Campbell | Courteney Cox | Scream | 2`, `Neve Campbell | David Arquette | Scream | 2`, `Tia Carrere | Chris Sanders | Lilo & Stitch | 2`, `'Poo' Ram | Aparna Balamurali | Soorarai Pottru | 1` (only these four groups score 2; the rest are 1). Two BLUE Movie circles, both titled "Scream" (1996, 2022), drop into one YELLOW group box: "the key is the value".
> The title leaves again. Two details on the top five: Rupert Grint's two rows get his ID beside Radcliffe's and Watson's (`nm0342488` < `nm0705356`, `nm0914612`): "smaller ID, so p1". Then a sixth row greys in under the LIMIT line, `Tom Cruise | Ving Rhames | 7` (verbatim, row 6 of the same query without the limit): the three 7s sorted J < R < T by name1, and LIMIT 5 cuts the third.

[c3.count.1] {back} Back to the question. Which pairs share the most movies? {replace} Replace the title in the return clause with count star, and call it movies. {sort} Then order by movies, descending, and keep the top five. {slide} This is the query on the slide, with the pattern split over two lines to fit.

[c3.count.2] {top} At the top, three pairs with eight movies each. {trio} Daniel Radcliffe with Emma Watson, Rupert Grint with Radcliffe, and Grint with Watson, all from the Harry Potter films. {seven} Then two pairs with seven. Johnny Depp with Helena Bonham Carter, and Robert Downey Junior with Scarlett Johansson. {prominent} These counts are lower than you might expect, because the database stores only the most prominent cast.

[c3.count.3] {missing} Notice that in sequel, counting per pair would need a group by clause, and Cypher has none. {how} So how does it know what to count? {pause} {before} Picture the rows before counting. Radcliffe and Watson appear in eight of them, one placement per film. {sensible} With two names and a count in the return clause, the only sensible thing to count is the rows that share both names. {collapse} So those eight rows collapse into one, with a count of eight.

[c3.count.4] {rule} That's the rule. Every expression in the return clause, other than the aggregates, becomes a grouping key. {twice} Sequel makes you write the keys twice, once in select and again in group by. {reads} Cypher just reads them off the return clause. {test} To test the rule, put the title back, next to the count. {split} Now the title is a key as well, so each group is one pair on one title, and almost every count drops to one.

[c3.count.5] {scream} Only four rows score two, because some titles exist twice. There are two films called Scream, from nineteen ninety-six and twenty twenty-two, and each pair who acted in both gets a count of two. {value} The key is the title's value, not the movie itself. {grint} Back in the top five, Rupert Grint always comes first in his pairs, because his ID is the smaller one. {tie} And Tom Cruise and Ving Rhames also share seven movies, but the names break the tie, alphabetically, and limit five cuts them off.

## Scene 6 · Recap (ch3_s6_recap)

> One small visual per sentence, in a 2 × 3 grid filling in left to right, each with its short line under it:
> 1. From scene 2: the two one-edge drawings, their m circles (BLUE) merging, `m` YELLOW: "same name, same vertex".
> 2. From scene 2: the comma form folding into `(p1:Person) -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]- (p2:Person)`, beside scene 4's three-armed star: "one line, or pieces joined by commas".
> 3. From scene 3: the mirrored V with the twin rows Chaplin–Coogan / Coogan–Chaplin, `<>` turning into `<`, the second row striking out RED: "less-than keeps one twin".
> 4. From scene 4: The Kid's ring with its 45 GOLD chords, "10 choose 2 = 45", and "120" for trios: "predict the count".
> 5. From scene 5: the eight Harry Potter rows collapsing into `8`, `name1, name2` in YELLOW brackets: "non-aggregates are the keys".
> Next time (sixth cell, then full frame): Jennifer Lawrence and Daniel Radcliffe as two PINK circles; the co-star V tried between them finds nothing (cypher-shell: 0 rows, checked); then ch1's dashed "?" chain between them stretches longer, link by link: "chains of any length".
> Hold the end card about 8 s after the last word; music carries it.

[c3.recap.1] {recap} Let's recap. {r1} The same name in a pattern means the same vertex, so two edges can meet at one movie. {r2} You can draw a pattern as one line, like the picture, or join pieces with commas, and a pattern can take any shape. {r3} A symmetric pattern matches every pair twice, once in each order, and less-than on the IDs keeps exactly one.

[c3.recap.2] {r4} You can predict the count from the data. Ten actors make forty-five pairs, and a hundred and twenty trios. {r5} And Cypher has no group by. Everything in the return clause except the aggregates is a grouping key. {pause}

[c3.recap.3] {next} Next time, Jennifer Lawrence and Daniel Radcliffe. They never made a movie together, so the co-star pattern finds nothing at all. {chain} To link them, we'll need chains of co-stars, of any length. {pause}
