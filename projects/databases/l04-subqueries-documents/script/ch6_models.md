# Chapter 6 · Documents or tables?

Databases · Lecture 4 (Subqueries and Documents), part 6 of 10. Source: Kleppmann, Databases notes 2026/27, pp. 43–45 (§4.3, slides 81–83, Exercises 17–18); refreshers p. 16 (slide 28, relationship shapes), p. 19 (slide 33, schema migration), p. 26 (slide 48, index nested loop join); recording 00:36:06–00:39:48.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Verification (2026-11-01): every query, result, count and error below was run on DuckDB v1.5.6
(Variegata): relational ones on `duckdb -readonly ../source/movies.duckdb`, document ones on
`duckdb -readonly ../source/movies-json.duckdb`. Statements that must *succeed* at writing (the
document inserts in s4, the migration in s5) ran in an in-memory DuckDB 1.5.6, on a table made with
slide 74's `CREATE TABLE` or on an in-memory copy of `people`, so the course files stay read-only.
JSON Schema messages: Python `jsonschema` 4.22.0, Draft 2020-12 validator. OCaml 5.4.1 (`ocamlc`),
Python 3.11.9. On-screen SQL is `Code(src, lang="sql")`, JSON `Code(src, lang="json")`, Python
`Code(src, lang="python")`, OCaml `Code(src, lang="ocaml")`. Result tables are typeset like the
slides (DIM header row, plain values), not as DuckDB's boxes. BLUE is the relational world, TEAL
the document world. PINK is NULL everywhere except s3, which borrows Lecture 5's graph look
(Person PINK, Movie BLUE; no NULL appears in s3).

---

## Scene 1 · Hook (ch6_s1_hook)

> Title card: "Subqueries and Documents", "Databases · Lecture 4", "Part 6 · Documents or tables?".
> On {lasttime}: ch4 s5's two-way copies, small (The Kid's card and Chaplin's card, ID arrows both ways, copied names and titles GOLD), with ch5's verdict under it: GREEN "reads: one document", RED "writes: every copy".
> On {same}: the copies shrink away; a small BLUE schema map (ch1 s2) and a small TEAL document card face each other across a "=", with a DIM footnote "apart from the trivia and the order of the cast". On {which} a YELLOW "which is better?" between them; on {depends} it becomes "it depends on how the data is used"; on {shape} the word "shape" stays YELLOW.
> On {tree}: The Kid's document as ch4 s2's JSON tree, centre: root, keys on the edges (title, year, rating, rating_votes, genres, actors, trivia_entries; directors, producers, writers, composers DIM), values at the leaves. On {trivia}: the five trivia_entries leaves hang below their key, each a short string fragment ("Due to the fact that…", "The off-screen chemistry…", "This was Sir Charles Chaplin's first…", "Sir Charles Chaplin and Jackie Coogan met…", "The production company tried…"), a small GREEN tick on each: one parent.
> On {chaplin}: the actors branch opens to its first element; the "Charles Chaplin" leaf glows YELLOW. On {others}: five small TEAL trees fade in around it, The Gold Rush, City Lights, Modern Times, The Great Dictator and "Chaplin (1992)", and each sends a branch to that same YELLOW Chaplin node (checked in has_position: six movies, actor on five, writer on Chaplin). The neat outline of The Kid's tree breaks.
> On {ask}: a big YELLOW "a tree?" over the picture. On {checks}: beside it a small TEAL document with a YELLOW tag "who checks the shape?".

[c6.hook.1] {title} This is part six: documents or tables? {pause} {lasttime} Last time, you saw that copies make reads fast, and writes costly. {same} Our two databases hold the same information, apart from the trivia and the order of the cast. {which} So which one is better? {pause} {depends} As usual, it depends on how the data is used, {shape} and on the shape of the data itself.

[c6.hook.2] {tree} Here's The Kid's document again, drawn as a tree. {trivia} Its five trivia entries hang off it neatly. Each one is about this movie, and nothing else. {chaplin} Now look at Charles Chaplin, on the actors branch. {others} He belongs to five other movies as well. {pause} {ask} So is a movie really a tree? {pause} {checks} And while we're at it, who checks that a document has the shape you expect? {pause}

## Scene 2 · What fits in a tree (ch6_s2_tree)

> Top strip, small and DIM, slide 28's three shapes as labelled pairs: "one-to-one" (movie — rating), "one-to-many" (movie — trivia entries), "many-to-many" (movies — people). Each lights YELLOW when narrated; "many-to-many" stays DIM until s3.
> Left, TEAL: The Kid's tree from s1, trimmed to the root, title, rating, rating_votes and trivia_entries. Right, BLUE: the movies and ratings cards from ch1 s2's schema map (same styling, primary keys underlined), The Kid's rows YELLOW.
> On {keys}: the leaves `rating: 8.2` and `rating_votes: 142991` pulse, hanging straight from the root beside `title`. On {table}: the ratings card shows its row as slide 24 does (columns movie_id, rating, votes; `tt0012349`, `8.2`, `142,991`), movie_id underlined as the whole key. On {join}: `movies ⋈_movie_id ratings` appears between the two cards.
> On {many}: trivia_entries opens into its five leaves, opening words verbatim: "Due to the fact that Jackie Coogan's mother…", "The off-screen chemistry between Sir Charles Chaplin…", "This was Sir Charles Chaplin's first feature length film he directed.", "Sir Charles Chaplin and Jackie Coogan met for the last time…", "The production company tried to cheat…". On {nest} the five leaves and their parent glow together: one read.
> On {rel}: a dashed BLUE card titled `trivia` (dashed = imagined: the relational database stores no trivia), columns movie_id and entry, five rows, each starting with The Kid's ID, and a foreign-key arrow to movies. On {join2}: `movies ⋈_movie_id trivia`.
> On {parent}: in the tree, a GREEN tick lands on the single edge above each leaf (rating, rating_votes, each trivia entry). On {rule}: the caption, YELLOW, "one owner → nest it inside"; "one-to-one" and "one-to-many" in the strip get GREEN ticks.

[c6.tree.1] {shapes} Relationships come in three shapes: one-to-one, one-to-many, and many-to-many. {one} Start with one-to-one. A movie has one rating, and a rating belongs to one movie. {keys} In the document, that's easy. The rating and its number of votes are just two more keys, next to the title. {table} Relationally, ratings is a table of its own, whose whole key is the movie ID. {join} So to show a title with its rating, you need a join.

[c6.tree.2] {many} Now one-to-many. A movie has many trivia entries, but each entry is about exactly one movie. {nest} In the document, they're an array nested inside the movie. Read the movie, and its trivia comes along. {rel} In our relational database, there is no trivia at all. If there were, the entries would need a table of their own, each row pointing back to its movie by ID. {join2} And reading a movie with its trivia would take a join.

[c6.tree.3] {why} Why do these two fit so well? {parent} Because in a tree, everything hangs from exactly one parent. {owner} The rating has one owner, and so does every trivia entry. {rule} So here's the test. If something belongs to one entity and nothing else, nest it inside that entity's document. {pause}

## Scene 3 · Many-to-many is not a tree (ch6_s3_graph)

> A clean stage in Lecture 5's graph look (the stated exception to PINK = NULL): every vertex a circle, Person PINK, Movie BLUE, names as labels beside them, plain lines with no arrowheads and no types. This scene owns the tangle helper (record its name in STATUS.md); Lecture 5's ch1 s2 redraws the first four.
> On {four}: Charles Chaplin and Jackie Coogan, The Kid and The Gold Rush; lines Chaplin–The Kid, Chaplin–The Gold Rush, Coogan–The Kid (has_position: Coogan's only movie is The Kid). On {nest}: The Kid's circle swells into a container and Chaplin moves inside; The Gold Rush swells too and needs a GOLD copy of Chaplin; RED tag "two parents". On {flip}: undo; Chaplin swallows The Kid, and Coogan reaches for it too: RED again. On {orphan}: a lone PINK circle with no lines and a RED "?" (hypothetical: in our data every person has at least one credit).
> On {grow}: The Kid's other eight actors fan out around it (Edna Purviance, Carl Miller, Albert Austin, Beulah Bains, Nellie Bly Baker, Henry Bergman, Edward Biby, B.F. Blinn); Chaplin's other movies join him (City Lights, Modern Times, The Great Dictator, and "Chaplin (1992)", where he is credited as a writer). On {cross}: the cross-links, all from has_position: Henry Bergman to The Gold Rush and Modern Times, then Paulette Goddard to Modern Times and The Great Dictator, Hank Mann and Al Ernest Garcia to City Lights and Modern Times. Lay it out so the lines visibly cross. On {downey}: Robert Downey Jr. hangs off "Chaplin (1992)", and twenty more lines run from him off the edge of the frame (21 movies in has_position).
> On {reach}: pull back; the tangle thickens into a haze of circles; a GOLD counter "2,902 of 2,935 movies" (checked: a recursive query over has_position, any position, from Chaplin reaches 2,902 movies and 22,724 of 23,179 people). On {graph}: the caption "not a tree but a graph".
> On {twoways}: the tangle shrinks to the left third; the right is TEAL. On {twice}: ch4 s5's two-way copies (The Kid's card and Chaplin's card, ID arrows both ways, copied names and titles GOLD); on {cost} ch5's tag in RED, "every copy kept in step". On {ids}: it gives way to The Kid's card in an IDs-only design, `"actors"` holding ten DIM person_id chips with their roles and no names. On {fetch}: ten arrows fly from the chips to ten people cards.
> On {loop}: the application's join (first block below), with a GOLD counter "1 + 10 fetches" ticking as the arrows fire; under it the first output lines `Charles Chaplin ['A Tramp']`, `Edna Purviance ['The Woman']`, `Jackie Coogan ['The Child']`, then DIM "… 7 more" (run in Python 3.11.9 on the real documents with the copied names stripped). On {slide}: slide 48's index nested loop join beside it (second block, verbatim from the notes), the two `.get(...)` lookups boxed YELLOW and aligned. On {who}: the label "the database" under slide 48's loop, "your code" under the application's.
> ```python
> movie = movies_by_id.get("tt0012349")             # 1 fetch
> for actor in movie["actors"]:                      # 10 more
>     person = people_by_id.get(actor["person_id"])
>     print(person["name"], actor["roles"])
> ```
> ```python
> results = []
> for movie in movies:                # scan the movies
>     rating = ratings_by_movie_id.get(movie["movie_id"])
>     if rating is not None:          # no rating, no row
>         results.append((movie["title"], rating))
> ```
> On {directions}: a movie card and a person card, with "cast" → one way and ← "movies" the other. On {movies}: Chaplin's card in the IDs-only design (person_id, name, birthyear, deathyear; no acted_in) and a grid of 2,935 tiny TEAL cards swept left to right; five light YELLOW, The Kid, The Gold Rush, City Lights, Modern Times, The Great Dictator (checked: the movies whose actors include him); GOLD "2,935 read, 5 found". On {fixes}: two GREEN labels, "store it twice" and "secondary index: person ID → movies". On {next}: the tangle returns full-frame, glowing, with the caption "Lecture 5: graph databases".

[c6.graph.1] {four} Now the hard case: two people, Charles Chaplin and Jackie Coogan, and two movies, The Kid and The Gold Rush. {nest} Try to make it a tree. Put Chaplin inside The Kid, and he must also go inside The Gold Rush. {flip} Turn it around, and The Kid must sit inside both Chaplin and Jackie Coogan. {pause} {both} A movie has many people, and a person has many movies, so something always needs two parents. {orphan} And, as the lecturer pointed out, a person with no movies would have nowhere to live.

[c6.graph.2] {grow} And the picture keeps growing: The Kid's other actors, Chaplin's other movies. {cross} Henry Bergman acted in The Kid, The Gold Rush and Modern Times, so the lines start to cross. {downey} Chaplin, the nineteen ninety-two film about his life, brings in Robert Downey Junior, and twenty more movies. {reach} Follow the lines from Chaplin, and you reach two thousand, nine hundred and two of our two thousand, nine hundred and thirty-five movies. {pause} {graph} This data is not a tree. It's a graph.

[c6.graph.3] {twoways} A document database has two ways out. {twice} The first is ours: store each relationship twice, in the movie and in the person, with copied names and titles. {cost} Reads are fast, and you pay with the anomalies of part five. {ids} The second: store only IDs. {fetch} Then to show The Kid's cast, you look up each of its actors' IDs. That's a join, in all but name.

[c6.graph.4] {loop} Some document databases have no joins, so the application does it by hand. It fetches the movie, then each actor, one at a time. That's eleven fetches for one page. {slide} It's the index nested loop join from earlier in the course, where each movie looks up its rating directly. {who} Same loop, but now your code runs it.

[c6.graph.5] {directions} And you'll want both directions. {cast} A movie's cast is easy: follow its IDs. {movies} But which movies did Chaplin act in? His document holds no IDs here, so you'd read all two thousand, nine hundred and thirty-five movies to find five. {fixes} So you either store the relationship twice after all, or add a secondary index, from each person ID to the movies that mention it. {awkward} Many-to-many is where documents get awkward. {next} The next lecture is about a model built for exactly this picture, the graph.

## Scene 4 · Who checks the shape? (ch6_s4_schema)

> Split screen. Left, BLUE: a small people card from ch1 s2's schema map, with its types as slide 26 declares them (`person_id TEXT`, `name TEXT`, `birthyear INT`, `deathyear INT`). Right, TEAL: slide 74's `CREATE TABLE people(person_id TEXT PRIMARY KEY, person JSON NOT NULL)`, small. Between each side's code and its table, a "write" gate.
> On {column}: left, `INSERT INTO people (person_id, name, birth_year)` / `VALUES ('nm9999999', 'Ann Example', 1990);` and DuckDB's reply in RED, verbatim: `Binder Error: Table "people" does not have a column with name "birth_year"` / `Did you mean: "birthyear"` (the suggested "birthyear" YELLOW). On {type}: `INSERT INTO people (person_id, name, birthyear)` / `VALUES ('nm9999999', 'Ann Example', 'unknown');` → RED `Conversion Error: Could not convert string 'unknown' to INT32` (DuckDB also prints a LINE/caret context; omit it). Both ran on the real movies.duckdb with -readonly: the errors come before the read-only check. On {name}: the left gate turns solid BLUE, labelled "schema-on-write".
> On {query}: `SELECT name + 1 FROM people WHERE false;` → RED `Binder Error: No function matches the given name and argument types '+(VARCHAR, INTEGER_LITERAL)'. You might need to add explicit type casts.` (DuckDB then lists about 45 candidate functions: show a DIM "…"). `WHERE false` boxed, "reads no rows"; label "checked before it runs".
> On {nmae}: right, `INSERT INTO people VALUES ('nm9999999', '{"nmae": 42}');` passes its gate with a GREEN tick (DuckDB prints nothing; the row is stored). On {malformed}: `INSERT INTO people VALUES ('nm9999998', '{name: 42}');` → RED `Conversion Error: Malformed JSON at byte 1 of input: unexpected character.  Input: "{name: 42}"` (two spaces before "Input", as printed). These two ran in an in-memory DuckDB 1.5.6 on a table made with slide 74's statement.
> On {schemaless}: the word "schemaless", in quotes, over the TEAL side; on {misleading} it is struck through in RED. On {reader}: a small reading-code card on the far right, `person["name"]`, tagged "expects: a string". On {implicit}: the TEAL gate slides from the write side to the read side; on {sor} it is labelled "schema-on-read".
> On {analogy}: both sides shrink upward; below them two terminal panels, OCaml in a BLUE frame on the left, Python in a TEAL frame on the right, each with the same small program (blocks below, `next_year` YELLOW, the `"1889"` string boxed). On {compile}: `ocamlc nextyear.ml` prints OCaml 5.4.1's error and nothing else; "running" never appears. On {python}: `python3 nextyear.py` prints `running`, then the traceback (its file lines DIM "…"), ending in RED `TypeError: can only concatenate str (not "int") to str`. On {map}: under the panels, "static types ≈ schema-on-write" (BLUE) and "dynamic types ≈ schema-on-read" (TEAL).
> ```ocaml
> let next_year y = y + 1
> let () = print_endline "running"
> let () = print_int (next_year "1889")
> ```
> ```
> File "nextyear.ml", line 3, characters 30-36:
> 3 | let () = print_int (next_year "1889")
>                                   ^^^^^^
> Error: This constant has type string but an expression was expected of type
>          int
> ```
> ```python
> def next_year(y):
>     return y + 1
>
> print("running")
> print(next_year("1889"))
> ```
> ```
> running
> Traceback (most recent call last):
>   …
> TypeError: can only concatenate str (not "int") to str
> ```

[c6.schema.1] {write} A relational database checks every write against its schema. {column} Misspell a column, and Duck D B refuses the insert, and even suggests the right name. {type} Put the word unknown into an integer column, and it refuses that too. {name} This is called schema-on-write. {query} It pays off on reads: every value has a known type, so queries can be checked before they run. Adding one to a name is rejected, even with where false, which reads no rows at all.

[c6.schema.2] {docs} A document database usually accepts any document. {nmae} Here's a person whose only key is a misspelt name, holding the number forty-two. Duck D B stores it without a word. {malformed} The one thing it checks is that the text is valid JSON. Leave the quotes off a key, and that's refused.

[c6.schema.3] {schemaless} This is sometimes called schemaless. {misleading} But that's misleading. {reader} The code that reads these documents still assumes a structure, for example that a person has a name key, holding a string. {implicit} So there is a schema. It's implicit, and it's only checked when the data is read. {sor} That's why it's better called schema-on-read. {pause}

[c6.schema.4] {analogy} You've met this difference before, in programming languages. {ocaml} Here's one mistake, in two languages. A function adds one to a year, and someone passes it the year as a string. {compile} The OCaml compiler rejects the program before it runs, so "running" is never printed. {python} Python happily prints "running", and crashes only when it reaches the bad line. {map} Static type checking is like schema-on-write. Dynamic type checking is like schema-on-read.

## Scene 5 · When reading-time schemas win, and what they cost (ch6_s5_tradeoff)

> On {shop}: three TEAL product documents stacked in one `products` table, each `Code(src, lang="json")` (all valid JSON, checked): `{"type": "book", "title": "My Autobiography", "author": "Charles Chaplin"}`, `{"type": "shoe", "name": "Walking boot", "size": 42}`, `{"type": "tv", "name": "Cinema 55", "resolution": "3840x2160"}`. On {attrs}: "resolution" and then "size" glow YELLOW, each casting a RED "?" ghost onto the other product. On {json}: the three sit happily in their one table. On {tables}: the BLUE alternatives slide in below: three cards books(product_id, title, author), shoes(product_id, name, size), tvs(product_id, name, resolution); then one wide card products(product_id, type, title, author, name, size, resolution) whose three rows are mostly PINK NULL cells.
> On {change}: clear. On {alter}: BLUE, slide 33's idea made concrete: `ALTER TABLE people ADD COLUMN first_name TEXT;` / `UPDATE people SET first_name = split_part(name, ' ', 1);`, a sweep down a tall people card and a GOLD "23,179 rows rewritten" (run on an in-memory copy of people: all 23,179 rows filled; with `.changes on` DuckDB reports `changes: 23179`).
> On {docs}: TEAL, two documents side by side, old `{"person_id": "nm0000122", "name": "Charles Chaplin"}` and new `{"person_id": "nm0001067", "first_name": "Jackie", "last_name": "Coogan"}`. On {both}: the reading code below them (it returns Charles for the old document and Jackie for the new; Python 3.11.9), its two branches pointing at the two documents:
> ```python
> def first_name(person):
>     if "first_name" in person:
>         return person["first_name"]
>     return person["name"].split(" ")[0]
> ```
> On {spell}: three small TEAL documents, `{"name": "Charles Chaplin", "birthyear": 1889}`, `{"name": "Jackie Coogan", "birthYear": 1914}`, `{"name": "Edna Purviance", "birth_year": 1895}` (their real birth years), the three key spellings YELLOW. On {string}: a fourth, `{"name": "Charles Chaplin", "birthyear": "1889"}`, the quoted `"1889"` boxed. On {accepted}: all four get GREEN "accepted" ticks, which then turn RED-outlined: accepted, but wrong.
> On {typo}: the query on the real document database, and its result typeset like the slides, with NULL PINK:
> ```sql
> SELECT person->>'name' AS name,
>        person->>'birthyear' AS birthyear,
>        person->>'birth_year' AS birth_year
> FROM   people
> WHERE  person_id = 'nm0000122';
> ```
> Result: header `name | birthyear | birth_year`, one row `Charles Chaplin | 1889 | NULL`. On {contrast}: s4's RED `Did you mean: "birthyear"` comes back small in its BLUE frame beside the PINK NULL in its TEAL frame.

[c6.trade.1] {when} So when does checking on read win? {shop} Picture an online shop that sells books, shoes and TVs. {attrs} A TV has a screen resolution, which means nothing for a shoe. A shoe has a size, which means nothing for a TV. {json} As documents, they can all share one table, each with its own keys. {tables} Relationally, you'd need a table for each type of product, or one wide table that's mostly null.

[c6.trade.2] {change} The second win is changing the schema. {split} Say you decide to store first names on their own. {alter} Relationally, that's a migration: add the column, then rewrite every row, more than twenty-three thousand of them. On a huge table, that can be slow. {docs} With documents, you just start writing new documents in the new format. {both} The old ones stay as they are, and the code that reads them handles both.

[c6.trade.3] {cost} The price is that mistakes are not caught. {spell} One part of an app writes birth year as one word, another in camel case, a third with an underscore. {string} Someone stores the year as a string, in quotes, instead of a number. {accepted} Every one of these is accepted. {typo} And a misspelt key is not even an error when you read it. Ask Chaplin's document for birth underscore year, and you just get null. {pause} {contrast} The relational database asked, did you mean birth year? The documents say nothing.

## Scene 6 · JSON Schema (ch6_s6_jsonschema)

> On {exists}: a TEAL title "JSON Schema". On {people}: slide 83's JSON Schema, centre, on a TEAL card, `Code(src, lang="json")`, verbatim from the slide (two-space indentation, values aligned in a column as on the slide), its `/* likewise … */` line DIM (slide shorthand, like ch4's `/* 9 more */`):
> ```json
> {
>   "type": "object",
>   "properties": {
>     "person_id": {"type": "string", "pattern": "^nm[0-9]+$"},
>     "name":      {"type": "string"},
>     "birthyear": {"type": "integer"},
>     "deathyear": {"type": "integer"},
>     "acted_in": {
>       "type": "array",
>       "items": {
>         "type": "object",
>         "properties": {
>           "movie_id": {"type": "string", "pattern": "^tt[0-9]+$"},
>           "title":    {"type": "string"},
>           "year":     {"type": "integer"},
>           "roles":    {"type": "array", "items": {"type": "string"}}
>         },
>         "required": ["movie_id", "title", "year", "roles"]
>       }
>     },
>     /* likewise "directed", "produced", "wrote", "composed_for" */
>   },
>   "required": ["person_id", "name"],
>   "additionalProperties": false
> }
> ```
> On {validator}: a small TEAL "validator" box left of the card, two inputs (schema, document) and one output (GREEN "valid" or a RED message).
> A YELLOW box walks the schema, one mark each: {object} `"type": "object"`; {props} `"properties"`; {pattern} `"pattern": "^nm[0-9]+$"`; {year} `"birthyear": {"type": "integer"}`; {array} acted_in's `"type": "array"` and `"items"`; {required} `"required": ["person_id", "name"]`; {extra} `"additionalProperties": false`. On {absent}: `{"person_id": "nm0000122", "name": "Charles Chaplin"}` goes through the validator: GREEN "valid".
> On {catch}: s5's mistakes go through one by one, each answered in RED, verbatim (Python jsonschema 4.22.0): on {underscore} `{"person_id": "nm0000122", "name": "Charles Chaplin", "birth_year": 1889}` → `Additional properties are not allowed ('birth_year' was unexpected)`; on {quoted} `{"person_id": "nm0000122", "name": "Charles Chaplin", "birthyear": "1889"}` → `'1889' is not of type 'integer'`; on {noname} `{"person_id": "nm0000122"}` → `'name' is a required property`.
> On {real}: GOLD "23,179 of 23,179 valid" (checked on every people document in movies-json.duckdb, with the slide's "likewise" line written out as four arrays of objects with movie_id, title, year and an optional job; job must be optional, since many elements have none).
> On {uses}: the label "OpenAPI: descriptions of web services" beside the card; on {generate} three small chips pop out of the card, "documentation", "code", "input forms". On {onwrite}: the validator box slides onto s4's TEAL write gate, which turns solid: "validate on write". On {details}: the card dims under the caption "know that it exists".

[c6.json.1] {exists} If you do want the shape checked, you can write it down, in a language called JSON Schema. {itself} A JSON Schema is itself a JSON document. {validator} A program called a validator checks a document against a schema, and reports what's wrong, if anything. {people} Here's part of a schema for our people documents.

[c6.json.2] {object} The type says what kind of value is allowed: here, an object. {props} Under properties, each key gets a schema of its own. {pattern} A person ID must be a string that matches a pattern, a regular expression. Two fixed letters, then nothing but digits. {year} Birth year is an integer. {array} Acted in is an array, and items gives the schema for every element. {required} Only person ID and name are required, {extra} and additional properties false forbids any other key. {absent} So a birth year may be missing, which is how our documents say it's unknown. But if it's there, it must be an integer.

[c6.json.3] {catch} Now feed it the mistakes from before. {underscore} Birth underscore year is an extra key, so it's rejected. {quoted} A year in quotes is a string, and a string is not an integer. {noname} A person without a name is missing a required key. {real} And all twenty-three thousand, one hundred and seventy-nine real people documents pass. {pause}

[c6.json.4] {uses} JSON Schema is widely used to describe the data that systems exchange, for example in Open A P I, a format for documenting web services. {generate} Tools can generate documentation, code and input forms from a schema. {onwrite} Validators exist for many languages, and some databases check documents against a schema on every write, which gives documents schema-on-write after all. {details} As the lecturer said, know that it exists. You do not need to learn its details.

## Scene 7 · Try these, and recap (ch6_s7_recap)

> On {ex17}: Exercise 17's card (the same card style as ch3 s8 and ch5 s7), verbatim from the notes p. 44: "For each of the following applications, would you store the data in a relational schema or as documents? Justify your answers, and if you choose documents, say what each document would contain." / "1. A blogging platform, where each post has a title, a body text, some tags, and comments from readers." / "2. A bank, which stores customers, their accounts, and the transfers between accounts." / "3. An event log, which stores every time various functions were invoked, and what arguments were passed to the function invocation." / "4. An online shop's product catalogue, in which different types of product have different attributes." / "5. A system for storing the settings of a mobile app, such as the user's preferred language, notification preferences, and so on."
> On {hint17}, {updates}, {shared}: three hint chips appear under it in turn, each with a tiny icon from this chapter: "tree or tangle?" (s2's tree beside s3's tangle), "what is updated, and how often?" (ch4 s5's GOLD copies), "one structure or many?" (s5's three products).
> On {ex18}: Exercise 18's card, verbatim from p. 45: "Which of the following properties of the people documents in the example database can be enforced by a JSON Schema, and which cannot? Explain why." / "1. Every person has a name." / "2. A person's deathyear, if present, is not earlier than their birthyear." / "3. No two documents have the same person_id." / "4. Every movie_id in a person's acted_in array is the ID of a movie document." / "5. The title in each element of acted_in is the same as the title in the corresponding movie document." On {hint18}: s6's validator box holding a single document, a magnifier over one value, and the hint chip "one document at a time" (ch10 s1 shows the same chip). On {ask}: YELLOW "what must it look at?". On {answers}: DIM "worked answers: part 10".
> Recap, {r1} to {r5}: five small callbacks in a row, each in its own scene's objects and colours, its line under it: {r1} s2's tree of The Kid with rating and trivia leaves and GREEN one-parent ticks, "one owner: a tree, so nest it"; {r2} s3's tangle, small, with the two-way copies and the "1 + 10 fetches" arrows, "many-to-many: a graph, so copies or joins"; {r3} s4's two gates, BLUE with `Did you mean: "birthyear"` at write, TEAL at read, "schema-on-write, schema-on-read"; {r4} s5's three products and the PINK NULL for birth_year, "flexible, and silent about typos"; {r5} s6's schema card with the RED `'birth_year' was unexpected`, "JSON Schema writes the shape down".
> On {next}: the recap slides away; a BLUE-framed movies row whose TEAL movie cell opens into The Kid's tree, with `->` and `->>` hovering beside it (part seven's opening picture). Then the end card, held about 8 s after the last word while the music carries it.

[c6.try.1] {ex17} Now try two exercises. {seventeen} Exercise seventeen gives you five applications, from a blog and a bank to an event log, a shop's product catalogue, and a mobile app's settings. Would you store each one in tables, or as documents? {hint17} For each, sketch its relationships. Is it a tree, or a tangle? {updates} Ask what gets updated, and how often. {shared} And ask whether all the items share one structure.

[c6.try.2] {ex18} Exercise eighteen lists five properties of our people documents. Which of them can a JSON Schema enforce? {hint18} Here's a hint. A validator is handed one document, and nothing else. And each keyword you've seen constrains one value: its type, its pattern, or whether it's there. {ask} So for each property, ask what you'd need to look at to check it. {answers} Worked answers to both are in part ten. {pause}

[c6.recap.1] {recap} Let's recap. {r1} Data with one owner forms a tree, and nests neatly in a document. {r2} Many-to-many data forms a graph, so documents either store it twice, or join on read. {r3} Relational databases check the schema on every write; documents leave it to the code that reads. {r4} That makes varied data and schema changes easy, and typos silent. {r5} And JSON Schema lets you write the shape down, and check it. {pause}

[c6.recap.2] {next} Next time, we'll query these documents with sequel, reaching inside a document with two arrows and a small path language. {pause}
