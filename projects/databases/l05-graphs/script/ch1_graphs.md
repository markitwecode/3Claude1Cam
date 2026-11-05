# Chapter 1 · From tables and trees to graphs

Databases (Lecture 5, Graph Databases), part 1 of 6. Source: notes pp. 50–53 (§5 intro, Slides 94–101); handout pp. 100–108; recording 04:43–22:51. Background: notes pp. 14–15 (Slides 24–25), 38–39 (Slides 71–73), 43 (Slide 81).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card on {title}: "Graph Databases", "Databases · Lecture 5", "Part 1 · From tables and trees to graphs"; it clears on {two}. Lecture conventions, set here and kept for all six parts (PLAN.md Decisions): every vertex is a circle, Person PINK, Movie BLUE; an edge is an arrow with its type in small caps along it and its properties in a small card at its middle; a matched pattern YELLOW; counts and numbers GOLD; RED only for wrong. Cypher is `Code(src)` (the project's cypher lexer), SQL is `Code(src, lang="sql")`, JSON is `Code(src, lang="json")`. Relational table cards keep Lecture 4's BLUE look, document cards its TEAL look.
> {two}: two PINK circles far apart, "Jennifer Lawrence" left, "Daniel Radcliffe" right (the running pair of parts four and five). {never}: a GOLD "0 films together" between them (checked with cypher-shell: the co-star pattern between them returns 0 rows).
> {chain}: a dashed path of small alternating circles (PINK, BLUE, PINK, …) bends from one to the other, a YELLOW "?" over it. Don't show how many links: part five answers that (4 edges, via Mother!, Domhnall Gleeson and Harry Potter and the Deathly Hallows: Part 2).
> {bacon}: the pair shrinks to a corner; a PINK "Kevin Bacon" circle with faint rings rippling out from it.
> {query}: Slide 109's query as Cypher, verbatim:
> ```
> MATCH path = allShortestPaths(
>         (kb:Person {name: 'Kevin Bacon'})
>         -[:ACTED_IN*]-
>         (p:Person))
> WHERE p.person_id <> kb.person_id
> RETURN length(path) / 2 AS bacon_number,
>        count(DISTINCT p.person_id) AS people
> ORDER BY bacon_number;
> ```
> {result}: its result as a small table beside it, in the slide's number format: bacon_number / people: 1 107, 2 3,519, 3 8,631, 4 1,676, 5 364, 6 212, 7 62, 8 9. Checked: cypher-shell (Traverse 0.8.0, node v24.2.0) on movies.tvdb, the same eight rows (printed without thousands separators), 84.7 s. It's a teaser: nobody is meant to read it yet.
> {shape}: everything dims except the two PINK circles and the dashed chain; on {q1} a YELLOW "What shape is this data?", on {q2} a second line, "What language fits that shape?".

[c1.hook.1] {title} This is lecture five of Databases, and it's about graphs. {two} Here are two actors, Jennifer Lawrence and Daniel Radcliffe. {never} In our movies database, they've never been in a film together. {pause} {chain} But you can still link them, through a chain of co-stars, actors who shared a film, one link at a time. How short can that chain be? {pause}

[c1.hook.2] {bacon} There's a famous game built on exactly this. Link any actor to Kevin Bacon, through as few films as possible. {query} By the end of this lecture, you'll be able to read this query. {result} It's eight lines long, and it works out how many films separate Kevin Bacon from every actor he's connected to. {pause}

[c1.hook.3] {shape} To get there, we need two answers. {q1} What shape is this data, really? {q2} And what kind of query language fits that shape? {pause}

## Scene 2 · Tables and trees (ch1_s2_lasttime)

> The tangle from Lecture 4 (its part six), redrawn from scratch at centre in this lecture's look: on {people} PINK circles "Charles Chaplin" and "Jackie Coogan" along the top; on {movies} BLUE circles "The Kid" and "The Gold Rush" along the bottom; on {lines} three plain lines grow, Coogan–The Kid, Chaplin–The Kid, Chaplin–The Gold Rush (checked: Coogan's only film in the database is The Kid). On {mn} a small "many-to-many" tag. This drawing is the chapter's anchor: s3 labels it, s5 rebuilds it as Slide 97, part five's closing strip returns to it.
> {tables}: the drawing shrinks to the top left. Three BLUE table cards in a row (Lecture 4's schema-map look): people, has_position, movies. On {rows} the Chaplin–The Kid line flies (TransformFromCopy) into has_position; on {five} it becomes Slide 25's five rows, verbatim:
> ```
> person_id     movie_id         position   job
> nm0000122     tt0012349        actor      null
> nm0000122     tt0012349        composer   composer
> nm0000122     tt0012349        director   director
> nm0000122     tt0012349        producer   producer
> nm0000122     tt0012349        writer     written by
> ```
> (Checked in DuckDB v1.5.6 on movies.duckdb, same five rows; DuckDB prints NULL for the slide's null.) The other two lines may drop in as DIM rows below, values not needed (one row for Coogan, four for Chaplin on The Gold Rush).
> {join}: people's row `nm0000122  Charles Chaplin  1889  1977` and movies' row `tt0012349  The Kid  1921  movie  68` light YELLOW, the matching IDs glow, and ⋈ appears between the cards: people ⋈ has_position ⋈ movies.
> {docs}: the cards clear; the drawing comes back and a cut line slices it into two trees. Two TEAL document cards side by side (Lecture 4's two-way copies), abridged from Slides 71 and 72 with their DIM `/* … */` elisions, as `Code(src, lang="json")`. On {kid} The Kid's:
> ```
> {
>   "movie_id": "tt0012349",
>   "title": "The Kid",
>   "year": 1921,
>   "actors": [
>     {
>       "person_id": "nm0000122",
>       "name": "Charles Chaplin",
>       "roles": ["A Tramp"]
>     },
>     /* 9 more */
>   ]
> }
> ```
> On {chaplin} Chaplin's:
> ```
> {
>   "person_id": "nm0000122",
>   "name": "Charles Chaplin",
>   "acted_in": [
>     {
>       "movie_id": "tt0012349",
>       "title": "The Kid",
>       "year": 1921,
>       "roles": ["A Tramp"]
>     },
>     /* 4 more */
>   ]
> }
> ```
> (Checked in movies-json.duckdb with DuckDB v1.5.6: The Kid's actors[0] and Chaplin's acted_in[0] hold exactly these values; the arrays have 10 and 5 elements.) The copied name and title GOLD. On {twice} the two Chaplin–The Kid entries glow YELLOW together: one line, two copies.
> {neither}: the drawing at centre, a mini has_position card on its left, the two mini TEAL cards on its right. On {asrow} a has_position row pulses next to a people row (the same shape); on {ascopies} the two copies pulse. On {third} the drawing's lines glow YELLOW, with a GOLD "?".

[c1.last.1] {tangle} Last time, we stored our movies as documents, and we hit a tangle that refused to fit in a tree. Here it is again. {people} Two people, Charles Chaplin and Jackie Coogan. {movies} Two movies, The Kid and The Gold Rush. {lines} And a line wherever a person worked on a movie. {mn} A movie has many people, and a person works on many movies. That's a many-to-many relationship.

[c1.last.2] {tables} So how do tables store a line? {pause} {rows} As rows of the table in the middle, has position. {five} Chaplin did five jobs on The Kid. Actor, composer, director, producer, and writer. So his one line is five rows. {join} And to follow a line, from Chaplin to the title of his film, you join people to has position, and has position to movies.

[c1.last.3] {docs} Documents cut the picture into trees instead. {kid} The Kid's document holds its cast, with a copy of each person's name. {chaplin} Chaplin's document holds his films, with a copy of each title and year. {twice} So the line between Chaplin and The Kid is stored twice, once in each tree, and the two copies have to be kept in step.

[c1.last.4] {neither} Now look at what both models do with a line. {asrow} In tables, a line is a row, just like a person or a movie is a row. {ascopies} In documents, a line is two copies, tucked inside two trees. {pause} Neither one stores a line as a thing of its own. {third} The third model does, and it's the subject of this lecture.

## Scene 3 · Data that forms a graph (ch1_s3_shapes)

> {graph}: s2's drawing back at centre. On {vertices} YELLOW tags on the circles, "vertices (nodes)"; on {edges} on the lines, "edges (links, arcs, relationships)".
> {everywhere}: it shrinks into the last slot of a 3×2 grid of small drawings (Slide 94), which fill in one per mark, each a few circles and lines with a caption under it and its question as a YELLOW tag. Every vertex is still a circle.
> {social} "social network": PINK circles joined by plain lines (friends); on {follows} one line becomes a one-way arrow, tagged "follows"; on {friends} a two-edge path out of one person lights YELLOW, tag "friends of friends". {web} "the web": page circles with arrows (links), tag "links → search ranking". {roads} "roads": junction dots, the roads labelled with GOLD lengths ("2 km", "5 km", …); on {route} the shortest route lights YELLOW, tag "shortest route".
> {packages} "software": "app" → "lib" → … depends-on arrows a few levels deep; on {deps} the whole downstream set lights YELLOW, tag "all transitive dependencies". {knowledge} "knowledge graph (Wikidata)": "The Kid" —director→ "Charles Chaplin" —occupation→ "actor", a little infobox card beside it. {ours} "our movies": s2's drawing.
> {chains}: in each tile in turn a chain of edges lights YELLOW; one caption under the grid, "questions follow chains of edges". On {unknown} it extends: "… often of unknown length", with a GOLD "?" over one chain's length.
> {algos}: the grid dims; a DIM card "graph algorithms: the Algorithms course". On {ours2} a YELLOW card beside it, "this course: storing and querying graphs".

[c1.shapes.1] {graph} A picture like this, dots joined by lines, is what mathematicians call a graph. {vertices} The dots are vertices, also called nodes. {edges} The lines are edges, also called links, arcs or relationships. {everywhere} And once you know the shape, you see it everywhere.

[c1.shapes.2] {social} In a social network, the vertices are people, and an edge says who's friends with whom, {follows} or who follows whom, which only goes one way. {friends} A typical question is friends of friends. {web} On the web, pages are vertices and links are edges, and search engines use those links to judge which pages matter. {roads} In a road network, junctions are vertices, and roads are edges labelled with their length. {route} A maps app planning your route is searching for a shortest path.

[c1.shapes.3] {packages} In software, a package depends on other packages, which depend on more packages, {deps} and installing it means finding all of them, however deep they go. {knowledge} Knowledge graphs like Wikidata store facts as edges, like the ones in the box beside a Wikipedia article. {ours} And our movies are a graph too. People, movies, and who worked on what.

[c1.shapes.4] {chains} Now look at the questions. Friends of friends. A route from here to there. Every dependency of every dependency. {unknown} They all follow chains of edges, and often you don't know in advance how long the chain will be. {pause} {algos} Algorithms for this, like shortest paths, belong to the Algorithms course. {ours2} Our job is storing a graph in a database, and asking it questions.

## Scene 4 · The property graph model (ch1_s4_propgraph)

> Heading "The property graph model"; built from nothing on a clean stage, in s1's conventions. This vertex-and-edge pair is reused small in s6 and in the recap.
> {vertex}: a PINK circle left of centre, "Charles Chaplin". {label}: a tag ":Person" above it (YELLOW, settling to FG), DIM note "one or more labels". {props}: a property card beside it in Slide 97's style, `name: Charles Chaplin` / `birthyear: 1889`. {json}: the card briefly shows as JSON, `{"name": "Charles Chaplin", "birthyear": 1889}` with TEAL braces (Lecture 4's document look), then back; DIM note "usually flat".
> {movie}: a BLUE circle right of centre, tag ":Movie", card `title: The Kid` / `year: 1921`. {edge}: an arrow grows from Chaplin to The Kid; its tail end, then its head end, pulse. {type}: `ACTED_IN` in small caps along it, DIM note "exactly one type · ALL_CAPS by convention".
> {where}: a GOLD card `roles: ['A Tramp']` floats above, looking for a home. On {notchaplin} it tries Chaplin (DIM ghosts of his other parts appear by him, "The Lone Prospector") and The Kid (ghosts of its other characters, "The Child"); on {onedge} it settles at the arrow's middle.
> {any}: brief: a faint arrow from Chaplin to an off-screen vertex and back fades (anything can link to anything). {several}: a second arrow curves between the same two circles, `DIRECTED`.
> {missing}: Chaplin's card gains `deathyear: 1977`; a second PINK circle below him, "Jennifer Lawrence", card `name: Jennifer Lawrence` / `birthyear: 1990` with no deathyear line, a GOLD pointer at the gap, "no key at all". Checked with cypher-shell: her vertex is `(:Person {birthyear: 1990, name: 'Jennifer Lawrence', person_id: 'nm2225369'})`, Chaplin's `(:Person {birthyear: 1889, deathyear: 1977, name: 'Charles Chaplin', person_id: 'nm0000122'})`.
> {nonsense}: a BLUE circle "The Gold Rush" below The Kid; a RED dashed `ACTED_IN` arrow from The Kid to it, captioned "stored without complaint". Checked on a scratch copy of movies.tvdb (never on source/): creating that edge printed `relationships created: 1, properties set: 1`.
> {power}: the pieces shrink; a tiny BLUE table card and the tiny graph, GOLD "≈" between them ("can express about the same"). On {language}, YELLOW: "the difference: the query language".

[c1.prop.1] {model} There are a few graph models. Most graph databases today use the property graph, so let's build a piece of one. {vertex} Start with a vertex. {label} It gets a label, Person, which says what kind of thing it is. A vertex may have several labels. {props} Then its properties, which are key-value pairs. Here, a name, Charles Chaplin, and a birth year, eighteen eighty-nine. {json} That's a little JSON object on the vertex, usually flat, with no objects nested inside.

[c1.prop.2] {movie} A second vertex, labelled Movie. The Kid, nineteen twenty-one. {edge} An edge goes from one vertex to another, so it has a direction. This one starts at Chaplin and ends at The Kid. {type} It has exactly one type, acted in, written in capitals by convention. {where} Now, where should his role, A Tramp, be stored? {pause} {notchaplin} Chaplin played other parts in other films, and The Kid has other characters. {onedge} The role belongs to the connection, so it's a property of the edge.

[c1.prop.3] That's the whole model, and it's very relaxed. {any} Any vertex can connect to any other. {several} Two vertices can have several edges between them. Chaplin also directed The Kid, so that's a second edge. {missing} And there's usually no schema. Chaplin's vertex has a death year, but Jennifer Lawrence's simply has no death year key, just like documents last time. {nonsense} Nothing even says what an edge type may join. An acted in edge from one movie to another is nonsense, and the database stores it without complaint.

[c1.prop.4] {power} So the model looks simpler than tables, yet it can express about the same things. {pause} {language} Where graphs really differ is the query language, and that's where they get exciting.

## Scene 5 · Our movies as a graph (ch1_s5_moviegraph)

> Slide 97 built up at centre, laid out as the slide, in the same positions as s2's drawing: PINK `:Person` circles on top, on {coogan} Jackie Coogan (left, card `name: Jackie Coogan` / `birthyear: 1914`), on {chaplin} Charles Chaplin (right, `name: Charles Chaplin` / `birthyear: 1889`); on {films} BLUE `:Movie` circles below, The Kid (`title: The Kid` / `year: 1921`) and The Gold Rush (`title: The Gold Rush` / `year: 1925`).
> {edges}/{acted}: arrows person → movie as on the slide: Coogan → The Kid `ACTED_IN` with `roles: ['The Child']`; Chaplin → The Kid `ACTED_IN` with `roles: ['A Tramp']`; Chaplin → The Gold Rush `ACTED_IN` with `roles: ['The Lone Prospector']`; on {directed} Chaplin → The Kid `DIRECTED`.
> {five}/{fan}: three more arrows fan out between Chaplin and The Kid, `PRODUCED`, `WROTE`, `COMPOSED_FOR`: five in all. On {rows} s2's five has_position rows slide in at the side, each linked to its arrow (actor–ACTED_IN, composer–COMPOSED_FOR, director–DIRECTED, producer–PRODUCED, writer–WROTE). On {all} GOLD "49,811 rows = 49,811 edges". On {job} each position cell flies onto its arrow as the type and each job cell as a property card: `job: 'written by'` on WROTE, `job: 'composer'`, `job: 'producer'`, `job: 'director'` (checked with cypher-shell: Chaplin's five edges to The Kid carry `{roles: ['A Tramp']}`, `{job: 'written by'}`, `{job: 'composer'}`, `{job: 'producer'}`, `{job: 'director'}`).
> {fold}: the graph slides right; Lecture 4's seven BLUE table cards on the left (movies, ratings, genres, has_genre, people, has_position, plays_role), and each flows (TransformFromCopy) to where it lives now: people → the Person circles, has_position → the arrows (already done). On {roles} plays_role → the roles cards, GOLD "30,303 roles on 29,153 ACTED_IN edges" (1,007 edges hold more than one). On {rating} ratings → `rating: 8.2` on The Kid's card; on {genres} has_genre and genres → `genres: ['Comedy', 'Drama', 'Family']`. On {nogenre} a DIM dashed circle "Genre?" with a small "Exercise 22" tag. (The Kid's vertex, cypher-shell: `(:Movie {genres: ['Comedy', 'Drama', 'Family'], minutes: 68, movie_id: 'tt0012349', rating: 8.2, rating_votes: 142991, title: 'The Kid', type: 'movie', year: 1921})`.)
> {counts}: GOLD totals: "2,935 Movie", "23,179 Person", and the five types with their edges, ACTED_IN 29,153, PRODUCED 7,429, WROTE 6,782, COMPOSED_FOR 3,281, DIRECTED 3,166 (checked with cypher-shell; DuckDB's has_position gives the same per position).
> {grammar}: zoom to one edge; on {sentence} it reads as a sentence, "Charles Chaplin  DIRECTED  The Kid": PINK noun, verb in small caps, BLUE noun, with DIM tags "noun", "past-tense verb", "noun".
> {distinct}: left, the seven table cards, all the same shape (people and has_position side by side, YELLOW "both just tables"); on {knows} right, the movie graph with its circles tagged "things: vertices" and its arrows "relationships: edges".

[c1.movies.1] {whole} Now let's turn our movies into a property graph. {coogan} People become Person vertices, like Jackie Coogan, born nineteen fourteen, {chaplin} and Charles Chaplin, born eighteen eighty-nine. {films} Movies become Movie vertices, like The Kid, from nineteen twenty-one, and The Gold Rush, from nineteen twenty-five. {edges} And every job someone did on a movie becomes an edge, from the person to the movie. {acted} Coogan acted in The Kid, as The Child. Chaplin acted in both, {directed} and he directed The Kid.

[c1.movies.2] {five} But remember, Chaplin did five jobs on The Kid. {fan} So there are five edges between these two vertices. Acted in, directed, produced, wrote, and composed for. {rows} They're the same five rows we saw in has position. {all} In fact, every row of has position becomes one edge. Forty-nine thousand, eight hundred and eleven rows, and exactly as many edges. {job} The position becomes the edge's type, and the job column becomes a property of the edge.

[c1.movies.3] {fold} The other tables fold in too. {roles} The plays role table becomes the roles list on each acted in edge. It's a list, because one actor can play several parts in one film. {rating} Ratings become movie properties, {genres} and genres become a list. Comedy, drama, family. {nogenre} There are no genre vertices, a design choice that Exercise twenty-two puts to the test. {counts} Altogether, that's two thousand, nine hundred and thirty-five movies, twenty-three thousand, one hundred and seventy-nine people, and five types of edge.

[c1.movies.4] {grammar} Notice the naming. Labels are nouns, and edge types are verbs in the past tense, so each edge reads like a sentence. {sentence} Charles Chaplin directed The Kid. {distinct} And here's a real difference from tables. To the relational model, people and has position are both just tables. {pause} {knows} The graph model knows the difference. Things are vertices, and relationships between things are edges.

## Scene 6 · A graph in two tables (ch1_s6_tables)

> Two empty `CREATE TABLE` skeletons, `Code(src, lang="sql")`, filled one column per mark until they read as Slide 96. Beside them, s4's small Chaplin → The Kid `ACTED_IN` drawing; as each column appears, the part of the drawing it stores lights YELLOW: {vneeds} vertex_id ↔ a circle; {vlabel} label ↔ the `:Person` tag; {vprops} properties ↔ the card, with a TEAL nod to Lecture 4's JSON.
> {eneeds}: edge_id, while s5's fan of Chaplin's five arrows to The Kid flashes beside it (why an edge needs its own ID); {tail} tail_vertex ↔ the arrow's tail end; {head} head_vertex ↔ its head end; {etype} type ↔ the label on the arrow; {eprops} properties ↔ the roles card. {fk}: the two REFERENCES clauses glow, arrows from them to vertices(vertex_id). {onelabel}: a DIM note by label, "one label each: a simplification (a vertex may have several)".
> {ask}: a YELLOW "?" over the drawing. On {out} Chaplin's outgoing arrows glow; on {into} The Kid's incoming arrows glow. On {indexes} the two CREATE INDEX lines type in: edges_tails pairs with the outgoing glow, edges_heads with the incoming. {either}: a GOLD "49,811 edges" stack with a jump straight to a handful of them.
> Final text, Slide 96 verbatim (checked: runs as-is in DuckDB v1.5.6 on a scratch file; filled from movies.duckdb it holds 26,114 vertices and 49,811 edges):
> ```
> CREATE TABLE vertices(
>    vertex_id  INT PRIMARY KEY,
>    label      TEXT,    -- e.g. 'Movie' or 'Person'
>    properties JSON     -- e.g. {"name": "Charles Chaplin"}
> );
>
> CREATE TABLE edges(
>    edge_id     INT PRIMARY KEY,
>    tail_vertex INT REFERENCES vertices(vertex_id),
>    head_vertex INT REFERENCES vertices(vertex_id),
>    type        TEXT,   -- e.g. 'ACTED_IN'
>    properties JSON     -- e.g. {"roles": ["A Tramp"]}
> );
>
> CREATE INDEX edges_tails ON edges(tail_vertex);
> CREATE INDEX edges_heads ON edges(head_vertex);
> ```
> {query}: the DDL shrinks to the left; this query appears, `Code(src, lang="sql")` (run on that scratch copy with DuckDB v1.5.6). On {start} the `vertices AS m` line and The Kid's condition light BLUE; on {e} the edges join and `e.type = 'ACTED_IN'` light YELLOW; on {p} the join back to vertices lights PINK.
> ```
> SELECT p.properties->>'name' AS name
> FROM vertices AS m
> JOIN edges AS e ON e.head_vertex = m.vertex_id
> JOIN vertices AS p ON p.vertex_id = e.tail_vertex
> WHERE m.properties->>'title' = 'The Kid'
>   AND e.type = 'ACTED_IN';
> ```
> {rows}: the result drawn as ten PINK circles with `ACTED_IN` arrows into The Kid's BLUE circle, names in the order DuckDB printed them (no ORDER BY, so any order is right): Charles Chaplin, Jackie Coogan, Albert Austin, Beulah Bains, Nellie Bly Baker, Henry Bergman, Edward Biby, B.F. Blinn, Carl Miller, Edna Purviance; GOLD "10 rows". {joins}: the two JOIN lines pulse GOLD, "one edge = two joins".
> {generic}: left, Lecture 4's seven table cards, DIM, "made for movies"; right, the two cards `vertices` and `edges`, and s3's six thumbnails drop into them, GOLD "any graph".

[c1.tables.1] {twist} Here's a twist. You can store any property graph in a relational database, in just two tables. Let's work out what they must hold. {vneeds} A vertex needs an ID, so that edges can point at it, {vlabel} a label, {vprops} and its properties, in a JSON column, the same type we used for documents last time.

[c1.tables.2] {eneeds} An edge needs its own ID too, since Chaplin has five edges to The Kid, all with the same two ends. {tail} Then the vertex where it starts, its tail, like the tail of an arrow, {head} and the vertex where it ends, its head. {etype} Then its type, {eprops} and its properties, again as JSON. {fk} The tail and head columns are foreign keys, so each must name a vertex that exists. {onelabel} And to keep it simple, each vertex gets just one label here.

[c1.tables.3] {ask} Now, what will queries ask of these tables? {pause} {out} Starting from a vertex, they'll want the edges going out of it, {into} and just as often, the edges coming into it. {indexes} So the edges table gets two indexes, one on the tail column and one on the head column. {either} Now the database jumps straight to a vertex's edges in either direction, instead of scanning all forty-nine thousand, so a query can walk the graph either way.

[c1.tables.4] {query} Here's what following one edge looks like. {start} Start at The Kid, {e} find the acted in edges whose head is The Kid, {p} and look up the vertex at each tail. {rows} Out come its ten actors. {pause} {joins} So every edge you follow costs two joins, one with edges and one back to vertices. {generic} And look what we've gained. Our seven tables were made for movies. These two can hold any graph at all, from friends and roads to packages and movies.

## Scene 7 · Graph databases and Traverse (ch1_s7_traverse)

> {dbs}: three name cards, "Neo4j", "Memgraph", "Amazon Neptune", and "…". On {duck} a DuckDB card wearing Lecture 4's TEAL "JSON" badge gains a second badge, "graphs" (part five shows it).
> {traverse}: a Traverse card: "Cypher" (YELLOW), and on {browser} "runs in your web browser: nothing to install" (GREEN); beside the Neo4j card a DIM "Java + a server".
> Setup as a schematic browser window, redrawn from Slides 99–101 (not the screenshots): on {download} a file icon "movies.tvdb" arriving from "course materials page"; on {open} the address bar `https://traverse.truespar.com/`; on {demo} the sidebar's database "movies" (Nodes: Movie, Person) with a DIM "demo: smaller, other properties".
> On {delete} the cylinder icon circled, the red button "Delete", then the dialog "Delete database" with "Type delete to confirm" and `delete` typed in. On {upload} the folder icon circled, the button "Upload .tvdb or .tvmodel", and movies.tvdb flies in. (Labels as on Slides 99–101.)
> {shell}: a terminal card with `https://github.com/ept/cypher-shell` above it, showing verbatim (run with Traverse 0.8.0 on node v24.2.0; the startup lines and prompt as printed):
> ```
> $ node cypher-shell.mjs movies.tvdb
> Traverse 0.8.0: movies.tvdb has 26114 nodes and 49811 relationships.
> Enter :help for help. Changes are lost on exit unless you use :save.
> cypher>
> ```
> {banner}: "26114 nodes" lights GOLD with "= 2,935 + 23,179" under it, "49811 relationships" GOLD; a DIM tag on the terminal, "tables, no picture".

[c1.trav.1] {dbs} Databases built for graphs are called graph databases. The best known is Neo four J, and others include Memgraph and Amazon Neptune. {duck} Relational databases are gaining graph features too, just as Duck D B learned to store JSON. {traverse} In this course we'll use Traverse. It speaks Cypher, the same query language as Neo four J, {browser} and it runs entirely in your web browser. No Java, no server, nothing to install.

[c1.trav.2] {setup} Setting it up takes a minute. {download} First, download the movies graph file from the course page. {open} Then open Traverse, at the address on screen. {demo} It comes with a demo database that's also about movies, but smaller, with different properties, so delete it first. {delete} Click the cylinder icon, then Delete, and type the word delete to confirm. {upload} Finally, click the folder icon, then Upload, and pick the file you downloaded.

[c1.trav.3] {shell} Prefer the command line? There's a small program, cypher shell, that runs the same engine on your own computer. {banner} Same database, same answers, shown as text tables, but without the picture of the graph.

## Scene 8 · Recap (ch1_s8_recap)

> One row of five small panels, each the object that taught the idea, in its own colours and styling, with the sentence's short line under it.
> {r1}: s2's drawing between a mini has_position card (Chaplin's five rows) and the two mini TEAL document cards, "a row per job · two copies". {r2}: s3's grid of six thumbnails with one YELLOW chain, "chains of edges". {r3}: s4's Chaplin → The Kid, with `:Person`, `:Movie`, `ACTED_IN` and `roles: ['A Tramp']`, "labels · types · properties". {r4}: s5's fan of five arrows with GOLD "49,811 rows = 49,811 edges", "a row = an edge". {r5}: s6's two table cards with the index tags edges_tails and edges_heads and a GOLD "2 joins per edge", "two tables".
> {next}: the panels dim; s4's Chaplin → The Kid drawing morphs into the Cypher text `(p:Person) -[:ACTED_IN]-> (m:Movie)`: round brackets where the circles were, the arrow where the arrow was. (It's the pattern of `MATCH (p:Person) -[:ACTED_IN]-> (m:Movie) RETURN count(*)`, checked with cypher-shell: 29153.) This morph previews part two's hook.
> End card: hold ~8 s after the last word; the music carries it.

[c1.recap.1] {recap} Let's recap. {r1} Tables store a relationship as rows of a join table, and documents store it twice, once in each tree. {r2} When anything can link to anything, and questions follow chains, your data is a graph. {r3} A property graph has labelled vertices and typed, directed edges, both carrying properties. {r4} In our movies, every row of has position became one edge. {r5} And any graph fits in two tables, with two indexes, at two joins for every edge you follow.

[c1.recap.2] {next} Next time, we'll start asking the graph questions, in a language where the query looks just like the drawing.
