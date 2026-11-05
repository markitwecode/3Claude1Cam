# Chapter 7 · Reaching inside a document

Databases · Lecture 4 (Subqueries and Documents), part 7 of 10. Source: lecture notes (Kleppmann,
2026/27) pp. 45–47, §4.4 up to slide 88 (handout pp. 90–94); recording 00:39:48–00:47:54. Every
query on screen was run on DuckDB v1.5.6 against `movies-json.duckdb` (2026-11-01).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

---

## Scene 1 · Hook (ch7_s1_hook)

> Title card: "Subqueries and Documents", "Databases · Lecture 4", "Part 7 · Reaching inside a document".
> On {table}: the JSON database's `movies` table as a BLUE table card (the schema map's card style from ch1 s2): header `movies` with a GOLD "2,935 rows", columns `movie_id` (underlined, the primary key) and `movie` (a DIM type tag `JSON`). Four rows in table order, The Kid's first and YELLOW: `tt0012349` · `{"movie_id": "tt0012349", "title": "The Kid", …`, then Sherlock Jr., The Gold Rush, Metropolis, their `movie` cells cut off in DIM (the stored text and row order, checked on DuckDB 1.5.6).
> On {open}: The Kid's `movie` cell lifts out and unfolds into The Kid's JSON tree in TEAL (ch4 s2's tree helper, The Kid as ch4 s3 and ch6 s1 draw it; ch8 s1 reopens this same table card and cell): root, keys on the edges, values at the leaves. Expanded: title "The Kid", year 1921, minutes 68, genres → Comedy, Drama, Family, actors → [0] → name "Charles Chaplin" (the other nine actors as one DIM `/* 9 more */` stub). The other keys (movie_id, type, rating, rating_votes, directors, producers, writers, composers, trivia_entries) are folded DIM stubs. The table card stays, shrunk to the left, a TEAL line from the cell to the tree's root.
> On {flat}: a flat BLUE row strip beside the card, holding a condition `title = 'The Kid'` that has nothing to attach to: a YELLOW "?" in the gap between the BLUE row and the TEAL tree. On {ask}: the leaves "The Kid" and "Charles Chaplin" pulse YELLOW.
> On {tools}: `->`, `->>` and `$.actors[0].name` drop in under the tree as TEAL tags. On {traps}: three small markers flash along the bottom and dim: GOLD `'99' > '321'`, RED `( )`, PINK `NULL` (previews of s4, s5, s7).

[c7.hook.1] {title} This is part seven of our lecture on subqueries and documents. {last} Last time, you saw when data fits a document, and when it fits tables. {table} Now look at where our documents actually live. In Duck D B, the movies are an ordinary table with two columns, an ID and the whole document. {open} Each movie is one cell, but open The Kid's cell, and there's an entire tree inside.

[c7.hook.2] {flat} Sequel thinks in flat rows. A where clause compares one value with another, and a select picks out columns. {ask} So how do you ask for The Kid's title, or its first actor, when they're buried inside a single cell? {pause} {tools} Duck D B gives you two arrows, and a small language for routes through the tree. {traps} Along the way you'll meet a few traps, where a query goes wrong, sometimes loudly, and sometimes without a word.

## Scene 2 · Two arrows (ch7_s2_arrows)

> The table card and the tree shrink to the top; the small tree stays at the top right as the chapter's map. Centre: slide 84's query as `Code(src)` (sql lexer), verbatim:
> `SELECT movie->'title' AS title_json,` / `       movie->>'title' AS title_text,` / `       movie->'genres' AS genres` / `FROM   movies` / `WHERE movie_id = 'tt0012349';` → result typeset like the slides, with DuckDB's type row as small DIM tags under the headers (checked on DuckDB 1.5.6): `title_json` `json` → `"The Kid"` · `title_text` `varchar` → `The Kid` · `genres` `json` → `["Comedy","Drama","Family"]`. The ID is never read aloud ("The Kid's ID").
> On {single}: `->` on line 1 lights YELLOW and the tree's `title` leaf flies into the first cell (TransformFromCopy). On {quoted}: the two `"` of `"The Kid"` flash TEAL. On {double}: `->>` on line 2 lights YELLOW and the same leaf flies into the second cell, quotes stripped.
> On {types}: the type tags brighten. On {json} the `json` tags turn TEAL (still a JSON value); on {text} `varchar` turns BLUE (a plain SQL value). Keep this all chapter: TEAL = JSON value, BLUE = SQL value. On {genres}: the genres leaf with its three children flies into the third cell, its brackets TEAL.
> On {chain}: the query clears to one expression, built arrow by arrow, `movie->'actors'->0->>'name'` (checked: `Charles Chaplin`, varchar). Each arrow lights one edge of the tree as it's added: root → actors (a TEAL array card), → 0 (Chaplin's object, TEAL: `{"person_id":"nm0000122","name":"Charles Chaplin","roles":["A Tramp"]}`), → name with the double arrow, landing as BLUE `Charles Chaplin`. On {steps}: the three edges pulse in order.
> On {funcs}: two small cards, `->` = `json_extract(movie, 'title')` and `->>` = `json_extract_string(movie, 'title')` (checked: same `"The Kid"` and `The Kid`). On {standard}: DIM footnote "not standard SQL"; on {postgres} "PostgreSQL uses the same operators".

[c7.arrows.1] {query} Here's the first query. It picks the movie with The Kid's ID, and pulls three things out of its document. {single} The arrow, written as a minus sign and a greater-than sign, takes a key, here title, and returns that key's value. {quoted} Out comes The Kid, in double quotes. {double} The double arrow, with two greater-than signs, returns The Kid without the quotes. {pause}

[c7.arrows.2] {why} Why the difference? {types} Duck D B prints each column's type under its name. {json} The single arrow returns a value of type JSON, and in JSON, a string is written in double quotes. {text} The double arrow returns a var-char, sequel's name for a plain string. {genres} Ask the single arrow for genres, and you get a JSON array, Comedy, Drama, Family.

[c7.arrows.3] {which} So when do you want which? {deeper} Keep the value as JSON when you want to go deeper. {chain} The arrow actors gives the array of actors, arrow zero gives the first of them, and the double arrow name gives Charles Chaplin. {steps} Each arrow takes one step down the tree. {print} Take a string when the walk is over, and you want to compare the value or print it.

[c7.arrows.4] {funcs} The two arrows are shorthand for two functions, JSON extract and JSON extract string. {standard} The arrows are not part of standard sequel, and other databases spell them differently. {postgres} Postgres, though, uses the same two arrows.

## Scene 3 · JSON path: a route through the tree (ch7_s3_paths)

> The JSON tree (ch4 s2's helper) moves centre-left, large: genres expanded as [0] Comedy, [1] Drama, [2] Family; actors expanded as [0] Chaplin's object (person_id, name, roles) with the other nine as DIM stubs. Right: slide 85's query, verbatim (checked on DuckDB 1.5.6):
> `SELECT movie->>'$.actors[0].name' AS first_actor,` / `       movie->>'$.genres[1]'      AS second_genre,` / `       movie->>'$.genres[*]'      AS all_genres` / `FROM   movies` / `WHERE movie_id = 'tt0012349';` → `first_actor` `Charles Chaplin` · `second_genre` `Drama` · `all_genres` `[Comedy, Drama, Family]` (types varchar, varchar, varchar[]).
> The walk: on {example} the path `$.actors[0].name` splits into TEAL step chips. On {dollar} `$` lights the root; on {key} `.actors` lights the actors edge; on {index} `[0]` lights the first element; on {leaf} `.name` lights the leaf, which flies into the first_actor cell. On {genre}: `$.genres[1]` walks root → genres → [1] and lands on Drama.
> On {star}: `[*]` replaces the index; on {fan} the walk forks along all three genre edges at once, and the three leaves gather into one BLUE list box `[Comedy, Drama, Family]` (DuckDB's list, so BLUE brackets). On {kinds}: beside it, the single-arrow version `movie->'$.genres[*]'` → `["Comedy", "Drama", "Family"]`, type `json[]` (TEAL elements inside a BLUE list), against `varchar[]` (checked). On {names}: `$.actors[*].name` forks across all ten actors → `[Charles Chaplin, Edna Purviance, Jackie Coogan, Carl Miller, Albert Austin, Beulah Bains, Nellie Bly Baker, Henry Bergman, Edward Biby, B.F. Blinn]` (checked, varchar[]; wrap it over two lines).
> Off by one, on {zero}: the genres as a JSON array with TEAL indices 0 1 2 above the elements; on {one}, the same three as a DuckDB list with BLUE positions 1 2 3 below. On {both}, the query (checked):
> `SELECT movie->>'$.genres[0]'      AS json_first,` / `       (movie->>'$.genres[*]')[1] AS list_first,` / `       (movie->>'$.genres[*]')[0] AS list_zero` / `FROM   movies` / `WHERE movie_id = 'tt0012349';` → `Comedy` · `Comedy` · `NULL`; on {null} the NULL turns PINK.
> On {lang}: slide 85's legend as a small TEAL card: `$` the whole document · `.actors` value of the key actors · `[0]` first element of an array (counting from 0) · `[*]` every element of an array ⇒ result is a list. On {decl}: caption "a small declarative query language".

[c7.paths.1] {long} Writing one arrow per step gets long. {route} So instead of a single key, the right side of an arrow can be a whole route through the tree, written as one string. {name} That route is called a JSON path. {example} Here's an example. Dollar, dot actors, index zero, dot name.

[c7.paths.2] {dollar} Let's walk it. Dollar stands for the whole document, the root of the tree. {key} Dot actors follows the edge labelled actors, down to the array. {index} Index zero, in square brackets, takes the first element, {leaf} and dot name takes that actor's name, Charles Chaplin. {genre} In the same way, dollar dot genres, index one, gives Drama.

[c7.paths.3] {star} Now put a star in the brackets, instead of a number. The star means every element. {fan} The walk splits, and reaches all three genres at once. {list} So the answer is no longer one value, but a list, Comedy, Drama, Family. {kinds} With the double arrow, that's a list of strings, and with the single arrow, a list of JSON values. {names} And dollar dot actors, star, dot name, collects the names of all ten actors.

[c7.paths.4] {wait} Notice that index one gave Drama, the second genre. {zero} JSON arrays count from zero. {one} But a Duck D B list, like the one the star gives you, counts from one. {both} So index zero inside the path, and index one on the list, both give Comedy. {null} And index zero on the list is no error at all. It quietly gives null.

[c7.paths.5] {lang} Look at what a path really is. You describe where the values sit, and Duck D B goes and finds them. {decl} It's a small declarative query language of its own, living inside sequel.

## Scene 4 · Compare numbers as numbers (ch7_s4_cast)

> Slide 86's query, verbatim (checked on DuckDB 1.5.6): `SELECT movie->>'title' AS title, movie->>'year' AS year` / `FROM   movies` / `WHERE (movie->>'title') LIKE 'Star Wars%'` / `  AND (movie->>'year')::INTEGER >= 2000` / `ORDER BY year;` → five rows: `Star Wars: Episode II - Attack of the Clones` 2002 · `Star Wars: Episode III - Revenge of the Sith` 2005 · `Star Wars: Episode VII - The Force Awakens` 2015 · `Star Wars: Episode VIII - The Last Jedi` 2017 · `Star Wars: Episode IX - The Rise of Skywalker` 2019.
> On {use}: small DIM tags, "projection π" on the SELECT line and "selection σ" on the WHERE line. On {like}: line 3 boxed YELLOW. On {year}: line 4 boxed, `::INTEGER` GOLD. On {result}: the rows drop in.
> On {string}: from the small tree, the leaf `minutes: 68` (a GOLD number) passes through `->>` and comes out as the BLUE string `'68'` (`movie->>'minutes'` for The Kid → `68`, varchar, checked).
> On {dict}: two strings aligned character by character in a grid, `'99'` over `'321'`. On {first} (next clip) the first column, `9` against `3`, lights: `9` wins and the remaining columns are never looked at. On {max}: (checked) `SELECT MIN(movie->>'minutes') AS shortest,` / `       MAX(movie->>'minutes') AS longest` / `FROM   movies;` → longest `99` in RED; on {min} shortest `100` in RED.
> On {real}: the cast version (checked) `SELECT MIN((movie->>'minutes')::INTEGER) AS shortest,` / `       MAX((movie->>'minutes')::INTEGER) AS longest` / `FROM   movies;` → `22` · `321`, GOLD, with GREEN ticks (on screen only, DIM: 321 minutes is Gangs of Wasseypur).
> On {order}: back to the Star Wars result: the year column gets a DIM `varchar` tag and the years' four digits line up in a character grid, caption "sorted as text: safe only because every year has 4 digits".
> On {forget}: line 4 loses its cast, `  AND (movie->>'year') >= 2000`; on {binder} DuckDB's reply in RED, verbatim (checked): `Binder Error: Cannot compare values of type VARCHAR and type INTEGER_LITERAL - an explicit cast is required`. On {strings}: (checked) `SELECT '999' > '2000' AS as_strings,` / `       999 > 2000     AS as_numbers;` → `true` RED · `false` GREEN.
> On {spell}: `CAST(x AS INTEGER)` and `x::INTEGER` side by side with "=" between them, tagged "standard SQL" and, on {short}, "DuckDB shorthand".

[c7.cast.1] {use} With the arrows, a value from inside a document can go anywhere sequel expects a value. In a select, that's projection, and in a where clause, it's selection. {query} So which Star Wars films came out in two thousand or later? {like} The title, as a string, must be like Star Wars, followed by anything. {year} The year, cast to an integer, must be at least two thousand. {result} That gives five films, from two thousand and two to twenty nineteen.

[c7.cast.2] {why} Why the cast? {string} Because the double arrow always gives a string, even when the document holds a number. The Kid's sixty-eight minutes come back as the text six, eight. {dict} And strings compare character by character, like words in a dictionary. {max} So ask for the longest running time without a cast, and the answer is ninety-nine. {min} The shortest comes out as a hundred. {pause}

[c7.cast.3] {first} The first character decides, and nine beats three, so ninety-nine beats three hundred and twenty-one. {real} Cast to integers, the shortest is twenty-two minutes, and the longest three hundred and twenty-one. {order} Even our order by year sorts strings. It only works because every year has four digits.

[c7.cast.4] {forget} What if you forget the cast in the condition itself? {binder} Then the current Duck D B refuses to compare a string with an integer. It stops with a binder error, and asks for an explicit cast. {friendly} That's a friendly error. {strings} But it can't help when both sides are strings. The string nine, nine, nine counts as greater than the string two, zero, zero, zero.

[c7.cast.5] {spell} The cast has two spellings. Standard sequel writes cast, then the value, then as integer. {short} Duck D B also accepts the value followed by colon colon integer, a shorthand for the same thing.

## Scene 5 · The arrows bind loosely (ch7_s5_parens)

> Slide 86's query from s4 returns, its two parenthesised arrows ringed YELLOW. On {drop}: the parentheses around line 4's arrow fade out, leaving `  AND movie->>'year'::INTEGER >= 2000`. On {cast}: DuckDB's reply in RED, verbatim (checked on DuckDB 1.5.6): `Conversion Error: Could not convert string 'year' to INT32`, with its pointer line `LINE 4:   AND movie->>'year'::INTEGER >= 2000` and the caret under `::`.
> On {group}: DuckDB's grouping drawn as ghost brackets (taken from DuckDB's own parse tree via `json_serialize_sql`, checked): `movie->>('year'::INTEGER)`, the inner bracket RED around `'year'::INTEGER` with a RED tag "the key, cast to a number?". On {fails}: the word `'year'` shakes.
> On {kid}: the second example (checked; the error quoted Chennai Express in five runs out of five, but it quotes whichever document fails first, so another machine could name another movie; the narration says "Here"): `SELECT movie->>'title' AS title` / `FROM   movies` / `WHERE movie->>'title' = 'The Kid'` / `  AND movie->>'type' = 'movie';` → RED, verbatim: `Conversion Error: Failed to cast value to numerical: {"movie_id":"tt2112124","title":"Chennai Express",... when casting from source column movie`. On {fail}: "Chennai Express" in the message gets a YELLOW underline.
> On {grab}: ghost brackets showing DuckDB's actual parse (json_serialize_sql, checked): `((movie->>'title' = 'The Kid') AND movie)->>'type' = 'movie'`. The AND's left operand gets a GREEN/RED truth-value tag; its right operand, the bare `movie`, swells into a small TEAL document card with a RED "TRUE or FALSE?" tag on {doc}. (Checked: `movie::BOOLEAN` raises exactly this error message.)
> On {fix}: parentheses fly in around both arrows, `WHERE (movie->>'title') = 'The Kid'` / `  AND (movie->>'type') = 'movie';` → GREEN `The Kid` (checked).
> On {future}: a DIM note "DuckDB: arrows bind more tightly from version 2.0". On {rule}: a YELLOW rule card with slide 86's line, "Arrow operators have low precedence: always use parentheses!". On {live}: a DIM tag "the lecturer, live, 00:43".

[c7.parens.1] {look} Look again at the Star Wars query. Every arrow in the condition sits inside parentheses. {pause} {drop} What happens if you leave them out? {cast} Drop them from the year test, and Duck D B stops with a conversion error. It could not convert the string year to an integer.

[c7.parens.2] {tight} The cast binds more tightly than the arrow. {group} So Duck D B grouped the expression like this. First it casts the key, the word year, to an integer, and only then would it apply the arrow. {fails} And the word year is not a number.

[c7.parens.3] {kid} Here's a stranger one. Find the movie titled The Kid, whose type is movie. {fail} Without parentheses, you get a conversion error about failing to cast a value to numerical. Here, it even quotes the document of Chennai Express, a movie you never asked about. {pause} {baffle} Baffling, until you see the grouping.

[c7.parens.4] {and} In current Duck D B, the and operator also binds more tightly than the arrows. {grab} So it takes the comparison on its left, and on its right, just the word movie. {doc} It tries to use a whole movie document as true or false, and that's the cast that fails. {fix} Add the parentheses, and out comes The Kid.

[c7.parens.5] {future} Duck D B says the arrows will bind more tightly from version two onwards. {rule} Until then, the rule is simple. Put parentheses around every arrow in a condition. {live} The lecturer himself tripped over this one, live, in the middle of a demo.

## Scene 6 · Searching inside arrays (ch7_s6_arrays)

> Left: ch4 s6's block of the three MongoDB queries comes back, the same `Code(src, lang="javascript")` with its comments, verbatim from slide 75: `// Movies released in 2021 or later` / `db.movies.find({ year: { $gte: 2021 } })` / (blank) / `// Movies with "War" among their genres` / `db.movies.find({ genres: "War" })` / (blank) / `// Movies directed by Steven Spielberg` / `db.movies.find({ "directors.name": "Steven Spielberg" })`. On {first}: the first transforms into its SQL condition `(movie->>'year')::INTEGER >= 2021` with a GOLD `383` (checked on DuckDB 1.5.6: `SELECT COUNT(*) FROM movies` / `WHERE (movie->>'year')::INTEGER >= 2021;` → 383).
> On {contains}: slide 87's first query, verbatim (checked): `SELECT COUNT(*) FROM movies` / `WHERE list_contains(movie->>'$.genres[*]', 'War');` → GOLD `72` on {war}. Beside it, The Kid's BLUE list box from s3 `[Comedy, Drama, Family]`: a "War?" probe slides along it and finds nothing (RED); then ch4 s6's Saving Private Ryan list `[Drama, War]` (real data, checked) lights GREEN on War. On {any}: a DIM link back to the MongoDB `{ genres: "War" }`.
> On {all}: slide 87's second query (checked): `SELECT COUNT(*) FROM movies` / `WHERE list_has_all(movie->>'$.genres[*]',` / `                   ['Romance', 'Comedy']);` → GOLD `174` on {romcom}. `['Romance', 'Comedy']` is a DuckDB list literal (BLUE brackets).
> On {venn}: ch1 s4's Venn of Crime and Drama returns (same circles, colours and labels, its INTERSECT in a small BLUE card, a DIM tag "or a self-join: Exercise 10"). On {crime}: the TEAL condition `list_has_all(movie->>'$.genres[*]', ['Crime', 'Drama'])` lands on the overlap, and a GOLD `397` (checked in movies-json.duckdb) settles onto ch1's own 397. (Romance and Comedy with INTERSECT in movies.duckdb also give 174, checked; not shown.)
> On {through}: the small tree from s3 with the directors branch expanded; on {directors} `$.directors[*].name` forks across the directors array (The Kid's has one element, Charles Chaplin).
> On {spielberg}: slide 87's third query (checked): `SELECT movie->>'title' AS title, movie->>'year' AS year` / `FROM   movies` / `WHERE list_contains(movie->>'$.directors[*].name',` / `                    'Steven Spielberg')` / `ORDER BY year` / `LIMIT 3;` with a GOLD "28 movies" (28 rows without the LIMIT, checked). On {three}: `Jaws` 1975 · `Close Encounters of the Third Kind` 1977 · `Raiders of the Lost Ark` 1981.
> On {answered}: the three MongoDB filters and their three SQL conditions side by side, linked by TEAL lines, a GREEN tick on each.

[c7.arrays.1] {mongo} In part four, you saw three questions in Mongo D B's query language. Movies from twenty twenty-one on, movies in the War genre, and movies directed by Steven Spielberg. {first} The first needs only the cast, and finds three hundred and eighty-three movies. {rest} The other two search inside arrays.

[c7.arrays.2] {list} A path with a star gives a list, and Duck D B has functions for searching lists. {contains} List contains asks whether a list holds a value. Is War among this movie's genres? {war} Seventy-two movies say yes. {any} That's Mongo D B's rule, any element may match, written as a function call.

[c7.arrays.3] {all} List has all asks whether a list holds every element of a second list. {romcom} With Romance and Comedy, it finds a hundred and seventy-four romantic comedies, in a single condition. {venn} Remember part one's Venn diagram? In the relational database, two genres at once needed an intersect, or a table joined with itself. {crime} Swap in Crime and Drama, and list has all finds three hundred and ninety-seven, the same overlap as before.

[c7.arrays.4] {through} A path can also pass through an array of objects. {directors} Dollar dot directors, star, dot name, is the list of every director's name. {spielberg} Ask whether it contains Steven Spielberg, and twenty-eight movies come back. {three} The first three, by year, are Jaws, Close Encounters of the Third Kind, and Raiders of the Lost Ark. {answered} So all three of Mongo D B's questions now have an answer in sequel.

## Scene 7 · Missing keys (ch7_s7_missing)

> Three person document cards (ch4 s4's TEAL document card; keys only, values elided as DIM `…`), keys checked with `json_keys` on DuckDB 1.5.6: Charles Chaplin `person_id, name, birthyear, deathyear, acted_in, directed, produced, wrote, composed_for`; Hans Zimmer `person_id, name, birthyear, composed_for`; Alfred Hitchcock `person_id, name, birthyear, deathyear, directed` (ch4 s4's short document). On {cards}: the `composed_for` keys light YELLOW on the first two; Hitchcock's card shows a dashed empty slot where the key would be.
> On {exists}: `json_exists(person, '$.composed_for')` slides over the three cards: GREEN `true`, GREEN `true`, RED `false` (checked).
> On {composers}: slide 88's code, verbatim (checked): `-- People who have composed music for a movie` / `SELECT COUNT(*) FROM people` / `WHERE json_exists(person, '$.composed_for');` / (blank line) / `-- People who have never acted` / `SELECT COUNT(*) FROM people` / `WHERE NOT json_exists(person, '$.acted_in');`, comments DIM. GOLD `1,086` lands under the first; on {acted} GOLD `7,706` under the second.
> On {semijoin}: ch3 s5's BLUE semijoin card `people ⋉_person_id (σ_position='composer' (has_position))` with its GOLD 1,086 slides in beside the TEAL 1,086. On {two}: caption "one fact, two models".
> On {isnull}: (checked) `SELECT COUNT(*) FROM people` / `WHERE (person->>'acted_in') IS NULL;` → GOLD `7,706`, a PINK NULL tag on the arrow's output.
> On {differ}: a 2×2 grid, rows `{"a": null}` (key present, its JSON `null` PINK) and `{}` (key missing, a dashed slot); columns `json_exists(…, '$.a')` and `… ->> 'a'`. On {says}: `true` GREEN · `NULL` PINK in the first row, `false` RED · `NULL` PINK in the second (checked in an in-memory DuckDB 1.5.6). The two PINK cells pulse together: "can't tell them apart". On {ours}: DIM note "no JSON null in any of our 2,935 + 23,179 documents" (checked).
> On {typo}: (checked) `SELECT person->>'name'       AS name,` / `       person->>'birth_year' AS birth_year,` / `       person->>'birthyear'  AS birthyear` / `FROM   people` / `WHERE (person->>'name') = 'Charles Chaplin';` → `Charles Chaplin` · PINK `NULL` · `1889`; the `_` in `birth_year` RED. On {null}: GOLD "0 of 23,179 people have a birth_year" (checked). On {six}: a DIM chip calling back ch6 s5's three spellings, `birthyear`, `birthYear`, `birth_year`.

[c7.missing.1] {absent} A document only has the keys that apply to it. {cards} Chaplin and Hans Zimmer both composed film music, so their documents have a composed for key. Hitchcock's document has no such key. {ask} So how do you ask whether a key is there at all? {pause} {exists} JSON exists takes a document and a path, and answers true or false.

[c7.missing.2] {composers} Count the people whose documents have a composed for key, and you get one thousand and eighty-six. {pause} {semijoin} That's the number the semi-join found in part three, from the has position table. {two} One fact, two models, the same answer. {acted} Add the word not, and you count the people with no key called acted in, the ones who never acted. There are seven thousand, seven hundred and six of them.

[c7.missing.3] {arrow} There's a second way. Looking up a missing key with an arrow gives sequel's null. {isnull} So asking whether the double arrow of acted in is null finds the same seven thousand, seven hundred and six. {differ} The two ways differ only for a key that is present, but holds JSON's own null. {says} JSON exists says true, because the key is there, while the double arrow gives null, as if it were missing. {ours} Our documents never contain null, so here the two agree.

[c7.missing.4] {price} That forgiveness has a price. {typo} Misspell a key, say birth underscore year, instead of birthyear as one word, and nothing complains. {null} Every single person just gets null. {six} That was the warning in part six, and now you can see why. To Duck D B, a typo looks exactly like a missing key.

## Scene 8 · Recap (ch7_s8_recap)

> Six small callbacks in a 3×2 grid, each built on its sentence's mark with the sentence's short line under it, the earlier ones dimming as the next arrives:
> {r1} (s2): `->` → TEAL `"The Kid"` and `->>` → BLUE `The Kid`, with their `json` / `varchar` tags. Line: "-> keeps JSON · ->> gives a string".
> {r2} (s3): the mini JSON tree with the `$.actors[0].name` walk lit TEAL down to Charles Chaplin, and the `[*]` fork across genres. Line: "$ · .key · [0] · [*]".
> {r3} (s4): `'99'` over `'321'` with the first characters lit, beside a GOLD `321`. Line: "cast before comparing numbers".
> {r4} (s5): `(movie->>'year')::INTEGER` with YELLOW parentheses, the RED conversion error crossed out behind it. Line: "parentheses around every arrow".
> {r5} (s6): the Crime and Drama Venn with GOLD 397, and `list_contains` → GOLD 72. Line: "list_contains · list_has_all".
> {r6} (s7): the BLUE and TEAL 1,086 cards side by side, and `birth_year` → PINK NULL. Line: "json_exists · missing key = NULL".
> On {next}: the grid clears to s1's BLUE `movies` table card, The Kid's row YELLOW, its cell open on the TEAL `"actors": [ … ]` with ten small name chips inside the one cell (the picture ch8 s1 opens on). On {rows}: the chips lift out toward ten BLUE rows and stop half way, a preview of part 8's unnest. Then the end card, held ~8 s after the last word while the music carries it.

[c7.recap.1] {recap} Let's recap. {r1} The single arrow keeps a value as JSON, so you can go deeper, and the double arrow gives a string. {r2} A JSON path is a route from the root, with dollar, keys, indexes counted from zero, and a star for every element. {r3} The double arrow always gives a string, so cast before you compare numbers, or ninety-nine beats three hundred and twenty-one.

[c7.recap.2] {r4} The arrows bind loosely, so put parentheses around every one. {r5} A star gives a list, and list contains and list has all search inside it. {r6} JSON exists tests whether a key is there, and a missing key gives null, even when the reason is a typo. {pause}

[c7.recap.3] {next} Next time, we'll turn an array into rows of its own. {rows} Then grouping, joining and searching inside documents become ordinary sequel again. {pause}
