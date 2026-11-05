# Chapter 2 · Patterns: vertices, edges and arrows

Databases · Lecture 5 (Graph Databases), part 2 of 6. Source: lecture notes ch. 5, pp. 53–55 (§5.1, Slides 102–105); handout pp. 109–112; recording 22:56–33:53.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Checked: every Cypher query and reply below was run in Kleppmann's cypher-shell (Traverse engine,
node v24.2.0) on `movies.tvdb`, every SQL query in DuckDB v1.5.6 on `movies.duckdb` (2026-11-01).
Result cells are quoted as cypher-shell prints them: lists with quoted strings,
`['Comedy', 'Drama', 'Family']` (the slides, from the browser, show `[Comedy, Drama, Family]`).
House conventions (PLAN.md): every vertex a circle, Person PINK, Movie BLUE, edge types in small
caps along the arrow, the matched pattern YELLOW, counts GOLD. Cypher blocks `Code(src)`, SQL blocks
`Code(src, lang="sql")`.

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card: "Graph Databases", "Databases · Lecture 5", "Part 2 · Patterns: vertices, edges and arrows".
> On {graph}, a small patch of ch1's movie graph in ch1 s5's styling: PINK circles Charles Chaplin and Jackie Coogan, BLUE circles The Kid and The Gold Rush, arrows person → movie labelled ACTED_IN and DIRECTED. On {ask}, it shrinks to a corner and the question appears in YELLOW: "Which movies did Steven Spielberg direct?"
> On {sql}, Slide 105's SQL as a Code block (lang="sql"), verbatim (DuckDB: 28 rows): `SELECT m.title, m.year` / `FROM   people AS p` / `JOIN   has_position AS hp ON hp.person_id = p.person_id` / `JOIN   movies AS m ON m.movie_id = hp.movie_id` / `WHERE p.name = 'Steven Spielberg'` / `  AND hp.position = 'director';`
> On {tables}, highlight boxes hop over `people`, `has_position`, `movies`; on {joins}, over the two `ON …` conditions.
> On {draw}, copies of the three table names fly out (TransformFromCopy) into a sketchy diagram beside the code: box "people" → box "has_position" → box "movies", the links labelled person_id and movie_id.
> On {morph}, the diagram turns into a drawing: the people box becomes a PINK circle "Steven Spielberg", the has_position box an arrow labelled DIRECTED, the movies box a BLUE circle "Movie".
> On {ascii}, the drawing turns into one line of Cypher: `(p:Person {name: 'Steven Spielberg'}) -[:DIRECTED]-> (m:Movie)`; each circle's outline becomes its round brackets, the arrow becomes `-[:DIRECTED]->`. The SQL dims to ~0.3 and stays to the end of the scene; scene 6 brings it back.
> Also on {ascii}, a small footnote: "Cypher docs: neo4j.com · Traverse: truespar.com".

[c2.hook.1] {title} Last time, we turned our movies into a graph. {graph} People and movies became vertices, and every job a person did on a movie became an edge, an arrow from the person to the movie. {ask} So let's ask the graph a question. Which movies did Steven Spielberg direct? {pause}

[c2.hook.2] {sql} Here's how you'd ask in sequel. {tables} It takes three tables, called people, has position, and movies. {joins} And two joins, each with a condition saying which columns must match. {pause} {draw} And to check it, you probably end up drawing a little diagram. A person, linked through a row of has position, to a movie.

[c2.hook.3] {what} So what if the query were the drawing? {pause} {morph} In Cypher, the query language of Neo four J, that's exactly how you write it. A circle for the person, an arrow for the directed edge, and a circle for the movie. {ascii} Round brackets make the circles, and dashes with an arrowhead make the arrow. It's a kind of ASCII art.

## Scene 2 · Matching a vertex (ch2_s2_vertex)

> Hero, left: one BLUE Movie circle with the name "m" inside (YELLOW) and the label "Movie" under it. On {circle}, its outline copies out (TransformFromCopy) into the code `(m:Movie)` at the top right: outline → the round brackets; on {name}, "m" → `m`; on {label}, "Movie" → `:Movie`. A highlight box hops across the three parts, labelled "circle", "name", "label".
> On {match}, the query builds around it: `MATCH (m:Movie)`, then on {return} `RETURN m.title`. On {run}, a result table slides out below: `The Kid`, `Titane`, `Gone Baby Gone`, `The Dig`, `Blue Is the Warmest Colour`, … with a GOLD footer "2935 rows".
> On {more}, the second line becomes `RETURN m.title, m.year, m.genres` and the table widens: `The Kid │ 1921 │ ['Comedy', 'Drama', 'Family']`, `Titane │ 2021 │ ['Drama', 'Horror', 'Sci-Fi']`, `Gone Baby Gone │ 2007 │ ['Crime', 'Drama', 'Mystery']`. On {list}, a box around one genres cell, and the hero circle grows a little property card with `genres: [...]` inside it (no Genre vertex anywhere).
> On {sql}, a small SQL ghost at the side (lang="sql"): a GREEN link from `RETURN` to `SELECT`; on {from}, two links from `MATCH` to `FROM` and `WHERE`.
> On {where}, Slide 102's second form, verbatim: `MATCH (m:Movie)` / `WHERE m.title = 'The Kid' AND m.year = 1921` / `RETURN m.title, m.year, m.genres;`. On {braces}, the two conditions fly out of the WHERE line into curly braces inside the circle (TransformFromCopy), giving Slide 102's first form: `MATCH (m:Movie {title: 'The Kid', year: 1921})` / `RETURN m.title, m.year, m.genres;`. The hero circle's card now reads "title: The Kid, year: 1921".
> On {same}, both forms give the same single row (checked): `The Kid │ 1921 │ ['Comedy', 'Drama', 'Family']`, with a GOLD "1 row".
> On {case}, `match (m:Movie) return m.title` gives "2935 rows" (GREEN ✓). On {wrong}, `MATCH (m:movie) RETURN m.title` gives "0 rows" (RED), the lower-case `m` of `movie` boxed in RED, no error message. Caption: "keywords: any case · labels and property names: exact".

[c2.vertex.1] {start} Let's start with the smallest pattern, a single vertex. {circle} You draw a circle, and in Cypher, a circle is a pair of round brackets. {name} Inside goes a name for the vertex, em, so the rest of the query can refer to it, just like a table alias in sequel. {label} After a colon comes its label, Movie. {pause}

[c2.vertex.2] {match} The keyword match goes in front, {return} and the return clause says what to hand back, here em dot title. {run} Run it, and you get the title of every movie, two thousand, nine hundred and thirty-five rows. {more} Add em dot year and em dot genres to the return clause, and each row gets three columns. {list} The genres are a list of strings, stored as one property of the movie, with no separate vertex for a genre.

[c2.vertex.3] {sql} If you know sequel, the return clause plays the part of select, choosing what to show. {from} And match does the work of sequel's from and where clauses combined. It says where the data comes from, and what it must look like. {pause}

[c2.vertex.4] {filter} So how do we narrow it down to The Kid? {where} One way is the sequel way, with a where clause, saying that em dot title equals The Kid, and em dot year equals nineteen twenty-one. {braces} The other way puts those properties right inside the circle, in curly braces, like a little JSON object. {same} Both give the same single row. The Kid, nineteen twenty-one, a comedy, drama and family film.

[c2.vertex.5] {case} One more detail. Keywords like match and return can be in capitals or lower case, as in sequel. {data} But labels and property names are part of your data, and they must match exactly. {wrong} Write movie with a lower-case em, and you get zero rows. {pause} No error, just nothing. So if a query comes back empty, check your spelling.

## Scene 3 · What a match is (ch2_s3_match)

> The chapter's central picture (ch3 s3 and ch6 s2, s4 reuse it): a patch of the movie graph fills the frame, about six BLUE Movie circles (The Kid, The Gold Rush, Jaws, E.T. the Extra-Terrestrial, …) and five PINK Person circles, with arrows person → movie, ch1 styling, names small.
> On {stencil}, scene 2's `(m:Movie)` lifts off the code and becomes a YELLOW stroke-only circle with a hole tagged "m" and "Movie" on its rim: the stencil. On {place}, it glides over the graph.
> On {fits} and {each}, it snaps onto one BLUE circle after another; each snap drops one row into a small results table at the right (the title of the circle it landed on). On {bind}, an arrow runs from `m.title` in the row back to the vertex it came from. A GOLD counter ticks up, then jumps to "2,935" on {count}.
> On {person}, the stencil tries a PINK circle: the labels clash, RED ✗, it slides off.
> On {kid}, the stencil gains the card `{title: 'The Kid', year: 1921}`; on {one}, it slides past every movie with small RED ✗s and fits only The Kid (GREEN ✓): counter "1", one row.
> On {bare}, the label falls off the stencil (`(m)`), and it fits every circle, PINK and BLUE alike: counter "26,114", with a small GOLD sum "2,935 + 23,179" (checked: `MATCH (m) RETURN m.title` gives `26114 rows`).
> On {join}, the graph dims; a tiny SQL join picture appears: two small tables, rows paired off by matching keys, each matching pair → one result row, beside the caption "one placement = one row".
> On {later}, a two-circle stencil whose holes are both named `m` lands with both holes on the same BLUE circle; caption "same name = same vertex", with a small "chapter 3" tag.

[c2.match.1] {idea} Now, what exactly is a match? Everything else builds on this. {stencil} Think of the pattern as a stencil, a tiny graph with named holes in it. {place} The database slides it across the big graph, looking for every place where it fits. {fits} It fits only where the labels agree, and where any properties you wrote down agree as well.

[c2.match.2] {each} Each place where it fits is one placement, and each placement becomes one row. {bind} In that row, em stands for the vertex it landed on, so em dot title is that movie's title. {count} Our circle labelled Movie fits two thousand, nine hundred and thirty-five times, once per movie. {person} It never fits on a person, because the label is wrong. {pause}

[c2.match.3] {kid} Now add the curly braces, with the title The Kid and the year nineteen twenty-one. {one} The stencil still slides over every movie, but now it fits in just one place. One placement, one row. {bare} Leave out the label, and a bare circle fits every vertex in the graph, movies and people alike. That's twenty-six thousand, one hundred and fourteen placements.

[c2.match.4] {join} If this sounds familiar, it should. {rows} In sequel, a join also gives one row for every combination of rows that meets its conditions. {same} A pattern match is the same idea, drawn as a picture. {pause} {later} And when a pattern uses the same name twice, both copies must land on the same vertex. That's the key to the next part.

## Scene 4 · Following an edge (ch2_s4_edge)

> Hero: Steven Spielberg as a PINK circle at the centre, with a fan of BLUE Movie circles around him (about twelve of his 35, including Jaws, Close Encounters of the Third Kind, Raiders of the Lost Ark, E.T. the Extra-Terrestrial, A.I. Artificial Intelligence, and Spielberg), arrows out of him with their types in small caps. E.T. has two arrows (PRODUCED, DIRECTED), Close Encounters two (WROTE, DIRECTED), A.I. three (WROTE, PRODUCED, DIRECTED), the movie Spielberg (2017) one ACTED_IN.
> Code at the top, built piece by piece on {person}, {arrow}, {return}: `MATCH (p:Person {name: 'Steven Spielberg'}) --> (m:Movie)` / `RETURN m.title`. On the first {pause}, the caption "how many rows?" with a GOLD "?".
> On {rows}, GOLD "55 rows"; on {but}, beside it GOLD "35 movies" and "+20 ?" (checked: `count(*)` 55, `count(DISTINCT m)` 35).
> On {look}, the return line becomes `RETURN m.title, m.year` / `ORDER BY m.year` / `LIMIT 6`, and the result, verbatim: `Jaws │ 1975`, `Close Encounters of the Third Kind │ 1977`, `Close Encounters of the Third Kind │ 1977`, `Raiders of the Lost Ark │ 1981`, `E.T. the Extra-Terrestrial │ 1982`, `E.T. the Extra-Terrestrial │ 1982`. On {twice}, the repeated rows flash YELLOW.
> On {edge}, scene 3's YELLOW stencil, now two circles and an arrow, appears; on {any}, every arrow out of Spielberg glows faintly, whatever its type; then the stencil lands on Spielberg → E.T.; on {et}, once along PRODUCED (that arrow lights, row 1 drops out) and once along DIRECTED (row 2); on {two}, the two rows link to the two lit arrows.
> On {ai}, A.I.'s three arrows light, three rows. On {sum}, GOLD tallies by the fan: DIRECTED 28 + PRODUCED 22 + WROTE 4 + ACTED_IN 1 = 55 (checked with `RETURN type(r), count(*)`). On {spiel}, the ACTED_IN arrow to the circle "Spielberg (2017)" pulses.
> On {type}, `-->` in the code becomes `-[:DIRECTED]->` (the square brackets slide in); in the fan, only the DIRECTED arrows stay lit, the rest dim; on {directed}, GOLD "28 rows". On {careful}, `DIRECTED` gets a YELLOW box tagged "edge type", beside a crossed-out "directed graph".
> On {order}, Slide 103 verbatim: `MATCH (p:Person {name: 'Steven Spielberg'})` / `      -[:DIRECTED]-> (m:Movie)` / `RETURN m.title, m.year` / `ORDER BY m.year` / `LIMIT 4;` and on {list} its result: `Jaws │ 1975`, `Close Encounters of the Third Kind │ 1977`, `Raiders of the Lost Ark │ 1981`, `E.T. the Extra-Terrestrial │ 1982`.

[c2.edge.1] {edge} Now let's draw an arrow. {person} On the left, a circle for a person, called pee, with the name Steven Spielberg in curly braces. {arrow} Then two dashes and an arrowhead, pointing to a second circle, em, with the label Movie. {return} And we return em dot title. {pause} So how many rows do you expect? {pause=1.5}

[c2.edge.2] {rows} Fifty-five. {but} But Spielberg worked on only thirty-five different movies in this database. So where do the extra twenty rows come from? {pause} {look} Sort the result by year, and look closely. {twice} Close Encounters of the Third Kind appears twice. So does E T, the Extra-Terrestrial.

[c2.edge.3] {why} Think in placements. {edge} Now the stencil has an arrow, so each placement must land on a real edge, pointing the same way. {any} Our arrow has no type, so any edge out of Spielberg will do. {et} On E T, he has two edges. He directed it, and he produced it. {two} Two edges, two placements, two rows.

[c2.edge.4] {ai} On A I, Artificial Intelligence, he directed, produced and wrote, so it appears three times. {sum} Add up every edge out of him, and you get the fifty-five. {spiel} That even includes one acted-in edge, for a TV documentary from two thousand and seventeen called, of course, Spielberg.

[c2.edge.5] {type} To ask only about directing, write the edge type inside the arrow, after a colon, in square brackets. {directed} Now only directed edges fit, and we get twenty-eight rows, one per film he directed. {pause} {careful} Careful with that word. Here, directed is the name of an edge type, and has nothing to do with a directed graph. {every} Every edge in our graph has a direction anyway.

[c2.edge.6] {order} Order by and limit work just as they do in sequel. {list} Sort by year, keep the first four, and you get Jaws, from nineteen seventy-five, Close Encounters of the Third Kind, from nineteen seventy-seven, Raiders of the Lost Ark, and E T.

## Scene 5 · Naming the edge, and its direction (ch2_s5_props)

> Opens on scene 4's Slide 103 code, which slides up and dims. On {colon}, two pieces stacked and aligned on their colons: `(m:Movie)` tagged "name : label" and `-[r:ACTED_IN]->` tagged "name : type", the `r` YELLOW; on {r}, a small ACTED_IN arrow drawn under it carries the tag "r"; on {props}, a property card `roles: [...]` hangs from that arrow.
> On {kid}, Slide 104 verbatim: `MATCH (p:Person) -[r:ACTED_IN]->` / `      (m:Movie {title: 'The Kid'})` / `RETURN p.name, r.roles` / `ORDER BY p.name` / `LIMIT 4;`. Beside it, ch1's The Kid as a BLUE circle with PINK cast circles pointing in along ACTED_IN arrows, each arrow carrying a small roles card.
> On {rows}, the result, each roles cell flying out of the card on its arrow (TransformFromCopy): `Albert Austin │ ['Car Thief', 'Man in Shelter']`, `B.F. Blinn │ ['His Assistant']`, `Beulah Bains │ ['Bride']`, `Carl Miller │ ['The Man']`. On {chaplin}, ch1's Charles Chaplin arrow with `['A Tramp']` and Jackie Coogan's with `['The Child']` light up (rows 5 and 9 of the 10 without the LIMIT, checked).
> On {list}, the square brackets of every roles cell in the result flash; on {several}, Albert Austin's two-item list pulses. On {keanu}, a single PINK circle Keanu Reeves → BLUE The Matrix Resurrections, ACTED_IN, card `['Neo', 'Thomas Anderson']` (checked). On {edge}, the card pulses on the arrow, between the two circles, belonging to neither.
> On {whole}, `MATCH (p:Person {name: 'Steven Spielberg'}) -[r:DIRECTED]-> (m:Movie)` / `RETURN p, r, m`. On {star}, a Traverse-style picture: Spielberg in the middle, 28 BLUE circles in a ring, all DIRECTED arrows (GOLD "28").
> On {text}, the first row as cypher-shell prints it (checked; may be set small, the m cell may wrap): `(:Person {birthyear: 1946, name: 'Steven Spielberg', person_id: 'nm0000229'})` │ `[:DIRECTED {job: 'director'}]` │ `(:Movie {genres: ['Action', 'Adventure'], minutes: 127, movie_id: 'tt0097576', rating: 8.2, rating_votes: 847877, title: 'Indiana Jones and the Last Crusade', type: 'movie', year: 1989})`. Boxes on the round brackets of the vertices and the square brackets of the edge.
> On {dir}, a three-row table of arrow forms (Slide 104's lines), each with a tiny drawing and its count for Spielberg (checked, e.g. `MATCH (p:Person {name: 'Steven Spielberg'}) <-[:DIRECTED]- (m:Movie) RETURN m.title`): on {back} `(p) <-[:DIRECTED]- (m)`, "edge from m to p", RED "0 rows"; on {both} `(p) -[:DIRECTED]- (m)`, "edge in either direction", GOLD "28 rows"; on {any} `(p) --> (m)`, "edge of any type from p to m", GOLD "55 rows". The recap reuses this table.

[c2.props.1] {name} An edge can have a name too. {colon} As with a vertex, the name goes before the colon, and the type after it. {r} So ar, colon, acted in, is an edge of type acted in, called ar. {props} And once an edge has a name, you can read its properties.

[c2.props.2] {kid} Here's an example. Who acted in The Kid, and which parts did they play? {query} The pattern ends at the movie, and we return pee dot name and ar dot roles. {rows} Sorted by name, Albert Austin comes first. He played two parts, a car thief and a man in a shelter. {chaplin} Further down are two faces from last time, Charles Chaplin as a tramp, and Jackie Coogan as the child.

[c2.props.3] {list} Why is roles a list? {pause} {several} Because one actor can play several parts in the same movie. {keanu} Keanu Reeves, in The Matrix Resurrections, plays both Neo and Thomas Anderson. {edge} And the list sits on the edge, not on either vertex, because a part belongs to one actor in one film.

[c2.props.4] {whole} You can also return pee, ar and em themselves, whole vertices and edges. {star} Traverse then draws the part of the graph that matched. For Spielberg's directed edges, it's a star, with his twenty-eight films around him. {text} On the command line, you get text instead, in the same notation as the pattern, round brackets for vertices and square brackets for edges.

[c2.props.5] {dir} Finally, direction. {back} Flip the arrow, so that it points from the movie to Spielberg, and you get zero rows. {why} Every edge in our graph goes from a person to a movie, so the flipped arrow fits nowhere. {pause} {both} Leave out the arrowhead, and either direction will do, so it's twenty-eight rows again. {any} And leave out the square brackets, and any type will do.

## Scene 6 · Cypher next to SQL (ch2_s6_vssql)

> Slide 105 side by side. Left, the Cypher, verbatim: `MATCH (p:Person {name: 'Steven Spielberg'})` / `      -[:DIRECTED]-> (m:Movie)` / `RETURN m.title, m.year;`. Right, scene 1's SQL brought back to full opacity (lang="sql"): `SELECT m.title, m.year` / `FROM   people AS p` / `JOIN   has_position AS hp ON hp.person_id = p.person_id` / `JOIN   movies AS m ON m.movie_id = hp.movie_id` / `WHERE p.name = 'Steven Spielberg'` / `  AND hp.position = 'director';`
> Colour-matched pairs, lit one at a time with a connector between them: on {return} `RETURN m.title, m.year` ↔ `SELECT m.title, m.year` (GREEN); on {person} `(p:Person {name: 'Steven Spielberg'})` ↔ `people AS p` and `p.name = 'Steven Spielberg'` (PINK); on {movie} `(m:Movie)` ↔ `movies AS m` (BLUE).
> On {arrow}, the arrow `-[:DIRECTED]->` lights YELLOW, with a GOLD "?" over the SQL. On {row}, `has_position AS hp` lights YELLOW. On {ends}, the arrow's two ends get dots; on {tail}, the tail dot links to `hp.person_id = p.person_id`; on {head}, the head dot to `m.movie_id = hp.movie_id`. On {type}, `:DIRECTED` ↔ `hp.position = 'director'` (YELLOW).
> On {rule}, Slide 105's caption: "An edge in a pattern ≈ a join with has_position". On {generic}, a small schematic of ch1 s6's two tables (same styling as there): `vertices AS p` — `edges AS e` — `vertices AS m`, the links labelled `ON e.tail_vertex = p.vertex_id` and `ON m.vertex_id = e.head_vertex` (checked on a scratch DuckDB whose vertices and edges were built from movies, people and has_position: the Spielberg query gives the same 28 rows).
> On {same}, a GOLD "28 rows" under each side (cypher-shell and DuckDB), with scene 4's first four rows (Jaws … E.T. the Extra-Terrestrial) under each.
> On {draw}, the SQL's join clauses get scribbled arrows between them, which assemble into the scene 1 diagram (people → has_position → movies); on {diagram}, it slides across and lands exactly on the Cypher line, the boxes on the circles and the middle box on the arrow. On {is}, caption "the query is the diagram".
> On {model}, the three data models as tiny icons (tables, tree, graph) from ch1 s2. On {cost}, the ch3 preview: a second arrow with a PINK circle at its far end attaches to the movie circle, and on the SQL side two ghost lines `JOIN has_position …` / `JOIN people …` appear (GOLD "+2 joins").

[c2.sql.1] {side} Now let's put the two versions of the Spielberg query side by side, and match them up piece by piece. {return} The return clause picks the same two columns as select. {person} The person circle is the people table, and the name in its curly braces becomes a condition in the where clause. {movie} And the movie circle is the movies table.

[c2.sql.2] {arrow} So what does the arrow become? {pause} {row} In the relational database, a job a person did on a movie is a row of has position, so the arrow becomes that table. {ends} An arrow has two ends, and each end becomes a join condition. {tail} The person ID in has position must be the person's, {head} and the movie ID must be the movie's. {type} And the edge type becomes a filter, saying the position must be director.

[c2.sql.3] {rule} So an edge in a pattern is roughly a join with has position, tied down at both ends. {generic} In the two general-purpose tables from last time, it's a join with edges, and then with vertices. {same} Either way, the answer is the same. Duck D B returns the same twenty-eight films as Cypher.

[c2.sql.4] {taste} So which is better? {pause} Partly, it's a matter of taste. {draw} But to check the sequel, you have to read the join clauses carefully and work out what's joined to what, and most people end up sketching a diagram. {diagram} That diagram looks just like the Cypher pattern. {is} In Cypher, the query is the diagram. {pause}

[c2.sql.5] {model} That's a lesson for this whole lecture. The data model you choose can change how simple your queries are. {cost} And the gap grows with every arrow, because each extra arrow, with the circle at its far end, costs the sequel two more joins.

## Scene 7 · Recap (ch2_s7_recap)

> Five small panels in a row, each the visual that taught its idea (same objects, colours and styling), with the sentence's short line beneath:
> On {r1}, scene 2's BLUE circle beside `(m:Movie {title: 'The Kid'})`, the circle, name, label and property card coloured as there: "a vertex: round brackets".
> On {r2}, scene 3's YELLOW stencil snapping onto a BLUE circle, a row dropping out, GOLD counter "2,935": "one placement = one row".
> On {r3}, scene 4's Spielberg → E.T. pair with its two arrows (PRODUCED, DIRECTED) and the two identical rows: "an edge: square brackets; two edges, two rows".
> On {r4}, scene 5's three arrow forms with their counts, RED 0, GOLD 28, GOLD 55: "the arrowhead sets the direction".
> On {r5}, scene 6's arrow with its two end dots linked to `has_position` and the two `ON` conditions: "an edge ≈ a join with has_position".
> On {next}, the panels clear. Two PINK circles with ACTED_IN arrows point into one BLUE movie circle from either side; on {costars}, the caption "co-stars", and the pattern faint beneath it: `(p1:Person) -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]- (p2:Person)` (checked: it runs; ch3 builds it). On {count}, a GOLD "most often?".
> Hold the end card ~8 s after the last word; the music carries it.

[c2.recap.1] {recap} Let's recap. {r1} A vertex is a circle in round brackets, with a name, a label, and perhaps some properties in curly braces. {r2} Matching finds every placement of the pattern on the graph, and each placement is one row. {r3} An edge is an arrow, with its name and type in square brackets, and every arrow must land on a real edge, so several edges mean several rows. {r4} The arrowhead sets the direction, and leaving it out allows either. {r5} And in sequel, every edge becomes a join through has position. {pause}

[c2.recap.2] {next} Next time, we'll draw two arrows into the same movie. {costars} Two actors, one film. In other words, co-stars. {pause} {count} And we'll find out which two actors have appeared together most often.
