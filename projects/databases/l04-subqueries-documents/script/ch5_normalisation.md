# Chapter 5 · One fact, one place

Databases · Lecture 4 (Subqueries and Documents), part 5 of 10. Source: Kleppmann, Databases notes 2026/27, §4.2 pp. 40–43 (slides 76–80, Exercises 15–16); refreshers p. 19 (slide 34, CREATE INDEX) and p. 20 (slide 35, INSERT); recording 00:29:21–00:36:06.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch5_s1_hook)

> Title card: "Subqueries and Documents", "Databases · Lecture 4", "Part 5 · One fact, one place". It gives way to ch4 s5's two-way copies (The Kid's TEAL document card and Chaplin's side by side, ID arrows both ways, copied names and titles GOLD), which then split the frame: relational on the left in BLUE, documents on the right in TEAL. All counts here were run on DuckDB 1.5.6 against movies.duckdb and movies-json.duckdb.
> {relational}: left, the people card from ch1 s2's schema map, Chaplin's one row YELLOW (`nm0000122 | Charles Chaplin | 1889 | 1977`), GOLD "1". {refs}: under it, his 21 has_position rows as thin BLUE strips grouped by movie (The Kid 5, The Gold Rush 4, City Lights 4, Modern Times 4, The Great Dictator 3, Chaplin 1), each with an arrow into the one people row, DIM label "refers by person_id".
> {own}: right, Chaplin's own TEAL person card with `"name": "Charles Chaplin"`. {copies}: the 21 arrows turn into 21 GOLD "Charles Chaplin" tags (TransformFromCopy) that land in six TEAL movie cards with the same per-movie counts; GOLD counter "21 copies in 6 movie documents".
> {kid}: The Kid's card grows; its five GOLD tags label themselves with the document's keys: actors, directors, producers, writers, composers.
> {titles}: the same for the title: The Kid's own card with `"title": "The Kid"`, and ten small TEAL person cards (its ten actors, Chaplin among them), each holding a GOLD "The Kid"; GOLD "10 people documents".
> {question}: everything dims except the GOLD copies; YELLOW "Bug or feature?". {answer}: both words light, "bug" RED and "feature" GREEN.

[c5.hook.1] {title} Last time, we packed The Kid into a single document, cast, crew and all. {count} Now let's count something simple. How many times does the database store Charles Chaplin's name? {pause} {relational} In the relational database, the answer is once, in one row of the people table. {refs} He has twenty-one credits, twenty-one rows in has position, and each of them refers to him only by his person ID.

[c5.hook.2] {docs} In the documents, it's a different story. {own} His name is in his own document, of course. {copies} But every one of those twenty-one credits now carries its own copy of the name, spread over six movie documents. {kid} The Kid alone holds five of them, as actor, director, producer, writer and composer. {titles} The title is copied too. The Kid is named in its own document, and in ten people documents. {pause}

[c5.hook.3] {question} So is all this copying a bug, or a feature? {pause} {answer} It's both. In this part, we'll work out exactly what the copies buy you, and what they cost.

## Scene 2 · Normalised and denormalised (ch5_s2_terms)

> Keeps s1's split: left BLUE (Chaplin's people row and the 21 ID arrows), right TEAL (the six movie cards with their GOLD copies).
> {redundancy}: the GOLD copies pulse; YELLOW heading "Redundancy: the same fact stored in several places". {normalised}: BLUE label on the left "Normalised: every fact in exactly one place"; {refer}: the arrows pulse, DIM "other places refer to it by its key". {denorm}: TEAL label on the right "Denormalised: copies stored where reads need them". {ours}: small tags "our relational schema" and "our documents" under each side.
> {why_id}: zoom on Chaplin's people row, the key `nm0000122` underlined. {change}: the name cell flickers to a DIM "new name?" and back while the ID stays put. {shared}: three people rows named `John Morris` stack up, each with a different person_id (verified: `SELECT name, count(*) FROM people GROUP BY name HAVING count(*) > 1` puts John Morris and Sam Phillips at 3). {join}: a ⋈ between a has_position strip and the people card, "to show a name: a join".
> {copies}: right side, slide 77's consequences as short lines: {fast}: GREEN "Reads: faster and simpler, fewer joins"; {slow}: RED "Writes: slower and more complex, every copy updated"; {drift}: one GOLD copy turns RED, "copies may disagree".
> {flip}: both sides clear. {title_col}: the BLUE plays_role card (schema-map style) with The Kid's 12 rows (verified: 12) grows a fourth column `title`, "The Kid" twelve times in GOLD; tag "denormalised, relational".
> {ids_only}: a TEAL movie card whose actors entries keep only `"person_id"` (the `"name"` lines struck out), arrows out to person cards and a ⋈; tag "normalised, documents".
> {rule}: slide 77's closing lines, the first BLUE and the second TEAL: "Relational DBs: often normalised, can be denormalised" / "Document DBs: often denormalised, can be normalised".

[c5.terms.1] {redundancy} Storing the same fact in several places has a name. It's called redundancy. {normalised} A schema without redundancy, where every fact is stored in exactly one place, is called normalised. {refer} Everywhere else refers to that fact by its key. {denorm} A schema that deliberately keeps copies, in the places where they're read, is called denormalised. {ours} Our relational schema is normalised, and our documents are denormalised.

[c5.terms.2] {why_id} Why refer to a person by an ID, and not by name? {pause} {change} Because names change, and an ID never needs to. It's just letters and digits that mean nothing to anyone, so there's no reason ever to edit it. {shared} Also, two people can share a name, and this database holds three different people called John Morris. {join} The price of normalising is joins, because to show a name, you have to look up what the ID refers to.

[c5.terms.3] {copies} Denormalised data turns that around. {fast} Reads get faster and simpler, with fewer joins, because the copy is right where you need it. {slow} Writes get slower and more complex, because every copy has to be updated. {drift} And if one copy gets missed, the copies disagree with each other.

[c5.terms.4] {flip} This choice has nothing to do with documents as such. {title_col} Add a title column to plays role. Then all twelve of The Kid's rows in that table hold a copy of its title. That's a denormalised relational schema. {ids_only} Now go the other way, and let movie documents store only their actors' IDs. Each name is then stored once, so the documents are normalised, but you need a join to find the names. {rule} As a loose rule, relational databases are often normalised, and document databases often denormalised, but both can go either way.

## Scene 3 · When a copied fact changes (ch5_s3_update)

> Split again, relational left (BLUE), documents right (TEAL). Running example Lana Wachowski (person_id nm0905154). Never show or say her former name: wherever the old value appears it is a DIM bar labelled "old name".
> {one_row}: the people card, her row YELLOW: `nm0905154 | ▭ old name | 1965 | NULL` (NULL in PINK). Code (sql), verbatim slide 78: `UPDATE people` / `SET    name = 'Lana Wachowski'` / `WHERE person_id = 'nm0905154';`. {done}: the name cell becomes "Lana Wachowski", GOLD "1 row". Checked on DuckDB 1.5.6 against a scratch copy of movies.duckdb: the CLI prints nothing, and with `.changes on` it reports `changes:   1   total_changes: 1`. {refs}: her 17 has_position strips (verified) hold only the ID and glow GREEN, "already right".
> {docs}: right, her own TEAL person card updates first. {find}: a wall of tiny TEAL movie-document tiles (2,935 in spirit). {scan}: a scan bar sweeps the wall; a DIM side card offers the alternative, "or keep an index: person_id → documents".
> Copies light up YELLOW but stay uncountable: open only The Matrix and Cloud Atlas, the rest is "…". {matrix}: The Matrix's card shows her twice, under `directors` and under `writers` (verified; Lilly Wachowski sits beside her in writers). {rewrite}: the copies are rewritten one at a time, DIM bar → "Lana Wachowski". {count}: GOLD "how many documents?" with DIM "Exercise 19, part 8". Never show the number (it is 19.1's answer).
> {miss}: three small RED failure panels, each ending with copies that disagree (one card still showing the DIM bar, another the new name): "missed one"; {crash}: "crashed halfway, no transaction" (a lightning bolt stops the sweep half done); {race}: "two updates at once" (two cursors interleaving over the same cards).
> {anomaly}: YELLOW heading "Update anomaly". {nothing}: the copies drawn as loose, unconnected strings, with RED "nothing in the database prevents it".

[c5.update.1] {change} Let's watch that cost happen. Suppose a person changes their name, as the film director Lana Wachowski did. {credits} Every credit on her movies should now show her current name. {one_row} In the relational database, that's a single update statement, setting the name where the person ID is hers. {done} One row changes, and you're done. {refs} Her credits refer to her by ID, so every one of them is already right.

[c5.update.2] {docs} In the documents, you start with her own person document. {find} Then you have to find every movie document that holds a copy of her name. {scan} Either you scan through all the movie documents, or you keep an index just for this. {matrix} And one document can hold several copies. The Matrix lists her as a director, and again as a writer. {rewrite} Then you rewrite each copy, one by one.

[c5.update.3] {count} How many documents is that? You'll count them yourself, in an exercise in part eight. {miss} Now, what can go wrong? {pause} The application might miss one copy. {crash} It might crash halfway through, with the updates not wrapped in a transaction. {race} Or two updates might run at the same time, and get in each other's way.

[c5.update.4] {disagree} In every case, some copies show the new name, and some still show the old one. {anomaly} That's called an update anomaly. {nothing} And nothing in the database stops it. As far as the database knows, those copies are just unrelated strings.

## Scene 4 · Losing a genre, and never gaining one (ch5_s4_genres)

> Documents first, TEAL: a few movie cards with their `"genres"` arrays; chips float out of them into a TEAL grid "genres in the documents" (23 chips: the distinct names in movies-json.duckdb, verified). {inside}: each chip stays tethered to the cards it came from; no card of its own.
> {news}: the "News" chip YELLOW; its single tether leads to Food, Inc. (2008), whose card shows `"genres": ["Documentary", "News"]` (Code, lang="json"; verified: the only document with News); GOLD "1 movie".
> {delete}: Code (sql) `DELETE FROM movies WHERE movie_id = 'tt1286537';` (run on a scratch copy of movies-json.duckdb, DuckDB 1.5.6: prints nothing; afterwards the documents hold 22 distinct genres, verified). {gone}: the Food, Inc. card dissolves, the News chip goes RED and fades, GOLD counter 23 → 22. {anomaly}: YELLOW "Deletion anomaly".
> {relational}: left, the BLUE genres card from the schema map (26 rows as a compact two-column grid). Food, Inc.'s movies row and its two has_genre rows (genre_id 7 and 20) fade; the `20 | News` row stays, GREEN (verified on a scratch copy of movies.duckdb). No SQL for this delete: DuckDB refuses to delete the movies row before its has_genre rows (foreign key, verified).
> {insert}: slide 35's Code (sql) `INSERT INTO genres (genre_id, name)` / `VALUES (27, 'Superhero');` (verified on the scratch copy: `changes:   1`); the row `27 | Superhero` slides into the BLUE card, GREEN. {nowhere}: a TEAL "Superhero" chip hovers over the documents with no card to land in, RED "?"; YELLOW "Insertion anomaly". {cause}: one YELLOW line over the TEAL side: "a genre has no home of its own".
> {proof}: reset to the real databases (the delete and the insert ran on copies): GOLD "26" over the BLUE grid, GOLD "23" over the TEAL one. {three}: Epic, Experimental and Gothic flash YELLOW in the BLUE grid with GOLD "0 movies" (verified with a LEFT JOIN on has_genre), and their places on the TEAL side open as dashed RED gaps.

[c5.genres.1] {only} Copies cause two more problems, and our data shows both. {inside} In the documents, a genre's name lives only inside the movies that have it. {news} Take the genre News. Exactly one movie has it, Food, Inc., from two thousand and eight.

[c5.genres.2] {delete} Suppose you delete that one document. {gone} Then News vanishes from the database entirely. {anomaly} That's a deletion anomaly. You deleted a movie, and lost a genre with it. {relational} In the relational database, News is a row of its own, in the genres table. Delete the movie and its has genre rows, and the genre is still there.

[c5.genres.3] {insert} The opposite problem is an insertion anomaly. {superhero} In the relational database, a single insert statement creates a genre called Superhero, before any movie has it. {nowhere} In the documents, there's nowhere to record it until some movie has that genre. {cause} Both problems have one cause. In the documents, a genre has no home of its own.

[c5.genres.4] {proof} And our real data already shows it. {count} The genres table lists twenty-six genres, but the documents only know twenty-three. {three} Epic, Experimental and Gothic have no movies at all, so they exist only in the relational database.

## Scene 5 · Normal forms (ch5_s5_forms)

> Hero: The Kid's BLUE movies row (schema-map style) with a ghost extra cell `genres` holding `[Comedy, Drama, Family]`. {first}: heading "First normal form (1NF): every value in a table is atomic", DIM under it "(a single number or string, not a list or nested record)".
> {genres}: the list cell cracks RED and splits; {rows}: out come three has_genre rows `tt0012349 | 5`, `tt0012349 | 8`, `tt0012349 | 11` (verified), each with a foreign-key arrow to the genres rows Comedy, Drama, Family.
> {doc}: right, ch4 s3's document card for The Kid; its line `"genres": ["Comedy", "Drama", "Family"]` (Code, lang="json", brackets TEAL) lifts out. {violates}: RED tag "violates 1NF, by design".
> {list}: Code (sql) `SELECT m.title, list(g.name) AS genres` / `FROM movies m` / `JOIN has_genre hg ON hg.movie_id = m.movie_id` / `JOIN genres g ON g.genre_id = hg.genre_id` / `WHERE m.movie_id = 'tt0012349'` / `GROUP BY m.title;` with its result as a slide table: DIM header `title | genres`, row `The Kid | [Comedy, Drama, Family]`. Verified on DuckDB 1.5.6 (column type `varchar[]`, same order on five runs). The three has_genre rows fly into the one list cell (TransformFromCopy). {mean}: DIM "many databases support JSON and list/array types".
> {further}: a small ladder "1NF → 2NF → 3NF → BCNF → …", DIM beyond 1NF. {example}: s2's plays_role card returns with its GOLD title column; {depends}: the key (movie_id, person_id, role) underlined, an arrow from `movie_id` alone to `title`, RED "determined by part of the key".
> {skip}: the ladder dims; one YELLOW line stays: "one fact, one place". {choice}: GREEN "break it on purpose" beside the genres array.

[c5.forms.1] {forms} The relational model makes this idea formal, through a series of normal forms. {first} The first is called first normal form. Every value in a table must be atomic, meaning a single number or a single string, never a list, and never a nested record. {genres} That's why has genre exists. In first normal form, The Kid's three genres cannot sit in one column of movies as a list. {rows} So instead, there's one row for each pairing of a movie and a genre.

[c5.forms.2] {doc} Now look at The Kid's document. Its genres are an array, three names in one value. {violates} Documents break first normal form by design. {list} Duck D B can break it too. The list aggregate folds the three has genre rows back into a single value, a list of names. {mean} Many databases support JSON and list types, so breaking the rule is a real option.

[c5.forms.3] {further} The further normal forms, second and third normal form, Boyce-Codd normal form and others, remove other kinds of redundancy. {example} Remember the title column we imagined in plays role? {depends} The title is determined by the movie ID alone, which is only part of that table's key. That's the kind of redundancy these forms rule out.

[c5.forms.4] {skip} Their formal definitions are beyond this course. The idea that matters is one fact, one place. {choice} And breaking a normal form can be a deliberate choice. As the lecturer put it, you're not a bad person for doing it. Just do it on purpose.

## Scene 6 · Why denormalise anyway (ch5_s6_why)

> {reads}: ch4 s1's mock IMDb page for The Kid, small, centre. Left: ch1 s2's schema map; all seven cards light up, The Kid's rows YELLOW, and the rows fly to the page while a GOLD tally builds per card: movies 1, ratings 1, has_genre 3, genres 3, has_position 14, people 10, plays_role 12 → GOLD "44 rows, 7 tables" (each count verified on movies.duckdb). {doc}: right, one TEAL document card flies to the page, GOLD "1 document".
> {locality}: YELLOW label "locality: data read together is stored together". {cost}: the 44 rows become 44 short trips to a disk and to a distant machine, against one trip for the document.
> {precompute}: a BLUE threads card (`thread_id | title | reply_count`, reply_count GOLD) beside a BLUE replies card, with made-up values (illustration only, no SQL on screen). {forum}: a counting sweep over replies is crossed out; the number is read straight from the thread row. {extra}: a new reply arrives, and two writes happen: a new replies row, and reply_count ticking +1; RED "a second write".
> {writes}: a balance. {gain}: GREEN pan "Reads: fast and simple". {price}: RED pan "Writes: more data to write and store; every copy kept consistent". {choose}: it tips toward GREEN under "mostly read, rarely updated → denormalise". {movies}: the movie page with many read arrows and a single, rare edit arrow.
> {truth}: final picture. {source}: the schema map (BLUE) labelled GREEN "source of truth (normalised)". {derived}: an arrow labelled "query" produces a stack of TEAL documents labelled "derived data, like a cache". {broken}: one document cracks RED; {regen}: it's discarded and regenerated along the arrow, GREEN. Slide 80's last line under it: "Best if you can regenerate the denormalised data at any time."

[c5.why.1] {why} If copies cause all this trouble, why would anyone denormalise? {pause} {reads} Count the reads. To show The Kid's web page from the relational database, you gather forty-four rows from all seven tables. {doc} From the documents, you read one document. {locality} Data that's read together is stored together, a property called locality. {cost} It matters most when the data is on disk, or on another machine, where every separate lookup has a cost.

[c5.why.2] {precompute} You can also denormalise by storing a result, instead of computing it again. {forum} A discussion forum might keep each thread's number of replies in the thread's own row, instead of counting the replies every time it lists the threads. {relational} That's denormalisation inside a relational database. {extra} And it has the same price. Every new reply needs a second write, to update the count.

[c5.why.3] {writes} So here's the trade. {gain} Reads get fast and simple. {price} Writes get slower and more complex, since there's more data to write and store, and the application must keep every copy consistent. {choose} Neither choice is simply right. If you mostly read the data, and rarely update it, denormalising may be just what you want. {movies} A movie database is a good example, since its pages are read far more often than its credits change.

[c5.why.4] {truth} You can get the best of both worlds with one rule. {source} Keep the normalised data as your source of truth. {derived} Treat the denormalised data as derived from it, like a cache, computed by a query over the normalised tables. {broken} If a copy is ever lost, or goes wrong, {regen} throw it away, and compute it again from the source of truth.

## Scene 7 · Try these, and recap (ch5_s7_recap)

> {ex15}: the Exercise 15 card, in the style of ch3 s8's exercise cards (ch9 s1 shows it again): "Exercise 15 · An index is a form of redundancy too. How is it similar to denormalisation, and how is it different?" {index}: beside it, slide 34's Code (sql) verbatim: `-- Make an index to efficiently find movies by year` / `CREATE INDEX movies_by_year ON movies (year);` (verified on a scratch copy, DuckDB 1.5.6: no output). Hint lines, one per mark: {who} "Who keeps the copies consistent?", {rw} "What happens on reads? On writes?", {queries} "Does it change how queries are written, or what they return?"
> {ex16}: the Exercise 16 card: "Exercise 16 · One query over the relational tables → one JSON document per movie: ID, title, year, genres (array of strings), actors (array of {person_id, name}). How does your output differ from the JSON database?" {object}: Code (sql) `SELECT json_object('title', title, 'year', year) AS doc` / `FROM movies` / `WHERE movie_id = 'tt0012349';` with its result `{"title":"The Kid","year":1921}` (verified, DuckDB 1.5.6). {list}: s5's list cell `[Comedy, Drama, Family]`, small. {careful}: ch2 s3's two small BLUE table cards: has_position with Kaiva's GOLD 10 actor rows, plays_role with a GOLD 0 for Kaiva; then Flow (2024) as a small BLUE movie row with RED edges, "no actors anywhere" (verified: Flow has no actor rows in either table). Part 9 takes the actors from has_position, so there only Flow has none. {compare}: an arrow from the query to s6's "derived data" stack.
> Recap: five small callbacks in a row, each lit as its sentence is said, its short line under it. {r1}: s1's one BLUE people row against the six TEAL movie cards with Chaplin's 21 GOLD copies, "once, or 21 copies". {r2}: s3's single BLUE UPDATE row against TEAL copies, one RED, "update anomaly". {r3}: s4's BLUE 26 and TEAL 23 grids with the three RED gaps, "deletion and insertion anomalies".
> {r4}: s5's three has_genre rows beside the genres array, "first normal form: atomic values". {r5}: s6's source of truth → derived data arrow, "derive the copies".
> {next}: the row clears to ch6 s1's picture, as a preview only: The Kid as a TEAL tree, the trivia hanging neatly off it, Chaplin's branch reaching out to five other movies. {shape}: a YELLOW "?" over a document outline. Then ~8 s of end card after the last word; music carries it.

[c5.recap.1] {try} Here are two exercises to try. {ex15} The first is about indexes. An index is redundancy too. The values of the column it covers are stored in the table, and again in the index. {index} Remember create index, from earlier in the course. How is an index like denormalisation, and how is it different? {who} Think about who keeps the copies consistent, {rw} what happens on reads and on writes, {queries} and whether an index changes how you write queries, or what they return. {pause}

[c5.recap.2] {ex16} In the second, you build the documents yourself. Write one query over the relational tables that produces a JSON document per movie, with its ID, title and year, its genres, and its actors, each with a person ID and a name. {object} The JSON object function takes keys and values, alternating, and returns an object. {list} The list aggregate, which you just saw, collects a group into a list. {careful} Choose your actors' table with care. Kaiva, from part two, has actors in has position, but no roles in plays role. And Flow has no actors at all. {compare} Then compare your documents with the real ones. {pause}

[c5.recap.3] {recap} Let's recap. {r1} Normalised data stores each fact once, while denormalised data keeps copies, like Chaplin's name, twenty-one times over. {r2} When a copied fact changes, every copy must change, or the copies disagree. That's an update anomaly. {r3} A fact with no home of its own can be lost, or never added. That's why the documents know twenty-three genres, and the tables twenty-six.

[c5.recap.4] {r4} First normal form keeps every value atomic, which is why has genre exists. {r5} And copies make reads fast and writes costly, so derive them from a normalised source of truth. {pause} {next} Next time, we ask when a document is the right shape in the first place. {tree} Some data hangs off a movie like branches off a tree, {tangle} and some never will. {shape} And who checks that a document really has the shape your code expects?
