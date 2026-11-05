# Chapter 8 · Arrays into rows

Databases · Lecture 4 (Subqueries and Documents), part 8 of 10. Source: Kleppmann, Databases notes 2026/27, pp. 47–49 (§4.4 from slide 89: slides 89–93, Exercise 19), handout pp. 95–99; refresher p. 21 (slide 39, LIKE); recording 00:47:54–00:57:20.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Verification: every query, result, count and error below was run on DuckDB v1.5.6 (Variegata),
`duckdb -readonly ../source/movies-json.duckdb` (and `movies.duckdb` for the relational
comparisons), on 2026-11-01. The MongoDB pipeline in s3 was run on MongoDB 8.0.10 (a scratch
`mongod`, driven through pymongo 4.19.0, on the 2,935 movie documents exported from
movies-json.duckdb); mongosh isn't installed, so its shell syntax below is the same four stages
written the shell's way. On-screen SQL follows the slides; JSON blocks are `Code(src, lang="json")`
in the slides' layout (two-space indentation, braces and brackets TEAL); result tables are typeset
like the slides (DIM header row, plain values, numbers with commas), not as DuckDB's boxes.

---

## Scene 1 · Hook (ch8_s1_hook)

> Title card: "Subqueries and Documents", "Databases · Lecture 4", "Part 8 · Arrays into rows".
> On {cell}: ch7 s8's closing picture comes back (a new video, so after the title card, not a handover): ch7 s1's BLUE `movies` table card with two columns, `movie_id` and `movie`, The Kid's row YELLOW, its `movie` cell open on the TEAL `"actors": [ … ]` in ch4 s3's document-card look (not ch7 s1's tree). The array shows ten small TEAL name chips in array order (Charles Chaplin, Edna Purviance, Jackie Coogan, Carl Miller, Albert Austin, Beulah Bains, Nellie Bly Baker, Henry Bergman, Edward Biby, B.F. Blinn), all still inside the one YELLOW cell; a GOLD "1 row" tag on the row.
> On {sort}, {genres}, {ages}: three question cards appear one per beat, each with a GOLD "?": "Sort the cast by name", "How many movies in each genre?", "How old was each actor?".
> On {tools}: under the cards, `ORDER BY`, `GROUP BY`, `JOIN` in BLUE. On {rows}: a DIM label "these work on rows", an arrow from it to the single YELLOW row with its ten chips squeezed inside.
> On {ask}: the ten chips lift out of the cell and hang in the air, half way to becoming ten rows. Hold there; s2 lands them.

[c8.hook.1] {title} Last time, the arrows and JSON paths reached inside a document and pulled out titles, years, even whole lists. {cell} Here's The Kid again. All ten of its actors sit inside one value, in a single row of the movies table.

[c8.hook.2] {questions} Now try three questions. {sort} Sort the cast by name. {genres} Count the movies in each genre. {ages} Find out how old each actor was when the film came out. {tools} Sequel has a tool for each: order by, group by, and joins. {rows} But those tools work on rows, and here the ten actors are squeezed into one. {pause}

[c8.hook.3] {ask} So how do you turn a list inside one row into rows of its own? {pause} {answer} It takes a single function, and once you have it, the whole of sequel comes back.

## Scene 2 · One row per element (ch8_s2_unnest)

> On {small}, concrete first: `SELECT * FROM unnest(['Comedy', 'Drama', 'Family']) AS t(genre);` (`Code`, sql lexer). On {three}: the list's three items slide down into a three-row result, header `genre`, rows Comedy / Drama / Family (verified). On {name}: brackets under `t` "table" and under `genre` "its one column".
> On {query}: slide 89's query becomes the hero, top left, verbatim:
> `SELECT   a->>'name' AS name, a->'roles' AS roles` / `FROM     movies, unnest(movie->'$.actors[*]') AS t(a)` / `WHERE    (movie->>'title') = 'The Kid'` / `ORDER BY name` / `LIMIT    4;` (five lines, the slide's spacing).
> On {from}: `unnest(movie->'$.actors[*]')` highlights; on {rows} the hook's ten hanging chips land as ten rows of a new table `t`, column `a`, each row one actor object with TEAL braces. On {select}: `a->>'name'` pulls a plain name out of each row, `a->'roles'` a TEAL JSON list.
> On {loop}: ch3 s2's outer-loop visual returns: movies on the left with the YELLOW cursor, the unnest box on the right. On {comma}: a DIM `×` (ch3 s7's toolkit row `FROM a, b`) sits on the comma; on {depends} it crosses out and becomes "for each movie". On {outer}: cursor on The Kid, ten rows drop out, counter 10; the cursor steps to the next movie and its own actors drop out.
> On {result}: the result (verified), slide layout, names plain, roles TEAL with their quotes: `name / roles`: `Albert Austin  ["Car Thief","Man in Shelter"]`, `B.F. Blinn  ["His Assistant"]`, `Beulah Bains  ["Bride"]`, `Carl Miller  ["The Man"]`.
> On {order}: ORDER BY and LIMIT dim out; two runs side by side, both verified. On {title}: with `WHERE (movie->>'title') = 'The Kid'` the ten names come back in array order, Charles Chaplin first, B.F. Blinn last. On {id}: with `WHERE movie_id = 'tt0012349'` the same ten come back reversed, B.F. Blinn first, Charles Chaplin last; a YELLOW arrow shows the flip. On {never}: caption "no ORDER BY, no order".
> On {compare}: slide 49's three-table join, small and BLUE on the right, verbatim: `SELECT   m.title, r.role, p.name` / `FROM     movies AS m` / `JOIN     plays_role AS r ON m.movie_id = r.movie_id` / `JOIN     people AS p ON r.person_id = p.person_id` / `WHERE    m.title = 'The Kid'` / `ORDER BY r.role` / `LIMIT    4;`, with its result (verified): `title / role / name`: `The Kid  A Tramp  Charles Chaplin`, `The Kid  Bride  Beulah Bains`, `The Kid  Car Thief  Albert Austin`, `The Kid  His Assistant  B.F. Blinn`. On {twelve}: LIMIT dims, GOLD "12 rows" (one per role; verified), Albert Austin's and Henry Bergman's two rows each YELLOW. On {ten}: GOLD "10 rows" under the unnest version, their roles as two-element lists.

[c8.unnest.1] {small} The function is called un-nest. {list} Give it a list, and it returns a table with one row per element. {three} The list comedy, drama, family becomes three rows. {name} And the alias at the end names two things: the new table, and its one column.

[c8.unnest.2] {query} Now use it on The Kid. {from} In the from clause, after movies, we un-nest the path to the actors, with the single arrow, so each element stays a JSON object. {rows} The ten actors come out as ten rows, one actor object each. {select} Then the select clause reaches into each one: the double arrow for the name, and the single arrow for the list of roles.

[c8.unnest.3] {loop} But why does un-nest sit in the from clause, after a comma? {pause} {comma} Normally, a comma there means a product of two independent tables. {depends} But this un-nest mentions movie, so it can't be computed on its own. {outer} It runs once for each movie, on that movie's own list, just like the correlated subquery from part three. {result} Sorted by name, the first four are Albert Austin, B. F. Blin, Beulah Bains, and Carl Miller.

[c8.unnest.4] {order} What happens if you leave out the order by? {pause} {title} Filtered by title, Duck D B happened to return the cast in array order, with Chaplin first. {id} Filter by The Kid's ID instead, and the same ten rows come back reversed. {never} Rows have no order unless you ask for one.

[c8.unnest.5] {compare} Compare the three-table join from earlier lectures, through movies, plays role, and people. {twelve} It gives The Kid twelve rows, one per role, because Albert Austin and Henry Bergman played two parts each. {ten} The un-nest version gives ten rows, one per actor, with the roles still in a list. {depends} Neither one is wrong. Some queries are easier on tables, and some on documents, and the queries you need should decide.

## Scene 3 · Grouping over documents (ch8_s3_group)

> On {genres}: slide 90's query, verbatim: `SELECT   genre, COUNT(*) AS n_movies` / `FROM     movies, unnest(movie->>'$.genres[*]') AS t(genre)` / `GROUP BY genre` / `ORDER BY n_movies DESC, genre` / `LIMIT    5;`. On {double}: the double arrow `->>` YELLOW for a moment.
> On {kid}: The Kid's genres, `[Comedy, Drama, Family]` (the double arrow's VARCHAR[], no quotes; verified), unfold into three rows The Kid · Comedy, The Kid · Drama, The Kid · Family (verified).
> On {all}: every movie unfolds at once; a GOLD counter runs up to 7,826 rows (verified). On {hasgenre}: ch1 s2's BLUE has_genre card slides in beside it with its own GOLD 7,826 (verified). On {same}: the two columns of pairs line up; small caption "same 7,826 (movie, genre) pairs, names for IDs" (verified: EXCEPT ALL both ways returns 0 rows). On {rebuilt}: ch5 s5's first-normal-form callback, `"genres": ["Comedy", "Drama", "Family"]` flattening into has_genre's rows.
> On {group}: the rows drop into genre bins and become bars, GOLD counts. On {result}: the result (verified), slide layout: `genre / n_movies`: `Drama 1,691`, `Comedy 878`, `Action 869`, `Adventure 719`, `Crime 621`.
> On {venn}: ch1 s4's Venn of Crime (621) and Drama (1,691), small, next to the Crime and Drama bars; the numbers pulse together.
> On {pipeline}: a DIM-framed panel, "MongoDB", `Code(src, lang="javascript")`: `db.movies.aggregate([` / `  { $unwind: "$genres" },` / `  { $group: { _id: "$genres", n_movies: { $sum: 1 } } },` / `  { $sort: { n_movies: -1, _id: 1 } },` / `  { $limit: 5 }` / `])`. On {steps}: the four stages get step numbers 1–4 and an arrow runs down them, beside the SQL's single declarative block. Same five results (run, see Verification).
> On {unwind}: `$unwind` YELLOW, joined by a line to `unnest` in the SQL above.

[c8.group.1] {genres} Once the elements are rows, they're ordinary rows. {double} Here, each movie's genres are un-nested, this time with the double arrow, so each genre comes out as a plain string. {kid} The Kid becomes three rows: comedy, drama, and family.

[c8.group.2] {all} Do that for every movie, and you get seven thousand, eight hundred and twenty-six rows. {pause} {hasgenre} Now count the rows of the has genre table, in the relational database. Seven thousand, eight hundred and twenty-six again. {same} And they're the same pairs, movie for movie, with genre names where the table has genre IDs. {rebuilt} Un-nest has rebuilt the join table that first normal form asked for, back in part five.

[c8.group.3] {group} Now group by genre and count. {result} Drama comes first, with one thousand, six hundred and ninety-one movies, then comedy, action, adventure, and crime, with six hundred and twenty-one. {venn} Those are the drama and crime numbers from the Venn diagram in part one. One dataset, two shapes, and the same facts.

[c8.group.4] {mongo} Many document databases give you less than this. {pipeline} In Mongo D B, you'd build an aggregation pipeline: unwind the genres, group them, sort, and limit. {steps} You describe the steps one after another, instead of declaring the result you want. {unwind} And look at the first step. Dollar unwind is Mongo D B's name for un-nest.

## Scene 4 · When the document doesn't have it (ch8_s4_join)

> On {look}: Henry Bergman's actor object from The Kid's actors array (the value of `a`, verified, shown in the slides' layout), `Code(src, lang="json")`: `{` / `  "person_id": "nm0074788",` / `  "name": "Henry Bergman",` / `  "roles": ["Professor Guido", "Night Shelter Keeper"]` / `}` (its keys are exactly these three: `json_keys` gives `[person_id, name, roles]`).
> On {missing}: an empty dashed RED slot under it, labelled "birthyear?". On {where}: an ID-reference arrow in ch4 s5's two-way-copies style runs from its `person_id` to his person document (verified): `{` / `  "person_id": "nm0074788",` / `  "name": "Henry Bergman",` / `  "birthyear": 1868,` / `  "deathyear": 1946,` / `  "acted_in": [ /* 3 movies */ ]` / `}`, with `1868` GOLD (the elision DIM, as the slides do it).
> On {query}: slide 91's query, verbatim: `SELECT   a->>'name' AS name,` / `         (movie->>'year')::INTEGER` / `            - (person->>'birthyear')::INTEGER AS age` / `FROM     movies, unnest(movie->'$.actors[*]') AS t(a),` / `         people` / `WHERE    person_id = (a->>'person_id')` / `  AND    (movie->>'title') = 'The Kid'` / `ORDER BY age DESC, name` / `LIMIT    4;`.
> On {from}: the FROM's three parts as three small stacked cards: movies, the unnested actors `t(a)`, people. On {product}: the comma before `people` becomes a `×`, and a grid of actor-by-person pairs flashes. On {select}: `person_id = (a->>'person_id')` keeps the matching pairs GREEN, the rest fade; the parentheses YELLOW (ch7 s5). On {join}: small caption "σ over × = ⋈".
> On {subtract}: the two casts produce GOLD `1921` and `1868`, and `1921 − 1868 = 53` builds beside them.
> On {top}: the result (verified), slide layout: `name / age`: `Henry Bergman 53`, `B.F. Blinn 49`, `Albert Austin 39`, `Edward Biby 35`. On {all}: LIMIT dims and the table grows to the full ten (verified): Henry Bergman 53, B.F. Blinn 49, Albert Austin 39, Edward Biby 35, Charles Chaplin 32, Nellie Bly Baker 28, Carl Miller 27, Edna Purviance 26, Beulah Bains 16, Jackie Coogan 7, with Jackie Coogan's row YELLOW. On {approx}: a DIM note "year − year: may be one too high".
> On {lesson}: ch4 s5's two-way copies (The Kid's card and Chaplin's card, copied names and titles GOLD). On {anticipated}: a GREEN tick on "Who's in this movie?" (one document read). On {other}: a RED "Their ages?" card points to a join. On {copy}: a GOLD "+1868" squeezes into The Kid's card, and the copy counter from ch5 s1 ticks up. On {lecturer}: a quote card, "maybe it should have been relational in the first place". On {upfront}: The Kid's TEAL card with its keys framed GREEN, caption "decided up front".

[c8.join.1] {ask} Now the third question. How old were The Kid's actors when it came out? {pause} {look} Look at one actor inside the movie document. A person ID, a name, a list of roles. {missing} No birth year. {where} Birth years live only in the people documents.

[c8.join.2] {query} So you fetch them, with a join. {from} The from clause now has three parts. The movies, the un-nested actors, and the people table. {product} That last comma is a real product, every actor paired with every person. {select} The where clause keeps the pairs where the people table's primary key matches the person ID inside the actor object, with parentheses around the arrow, as always. {join} A product, followed by a selection: that's a join.

[c8.join.3] {subtract} Then subtract. Take the movie's year, cast to an integer, minus the person's birth year, also cast. {top} Henry Bergman was born in eighteen sixty-eight, so he was fifty-three. Then B. F. Blinn at forty-nine, Albert Austin at thirty-nine, and Edward Biby at thirty-five. {all} Drop the limit, and at the bottom is Jackie Coogan, the kid himself, at seven. {approx} Strictly, it's a year minus a year, so each age may be one too high.

[c8.join.4] {lesson} Here's the lesson. {anticipated} The movie documents were designed for questions like, who's in this movie? That takes a single read. {other} Ask something the designer didn't anticipate, and you're back to joins. {copy} You could copy the birth years into every movie document, but that's more copies to keep in step, the cost from part five. {lecturer} As the lecturer put it, once you need joins, maybe it should have been relational in the first place. {upfront} With documents, you decide up front which data belongs together.

## Scene 5 · Searching text (ch8_s5_text)

> On {free}: The Kid's `trivia_entries`, five DIM text strips (the first begins "Due to the fact that Jackie Coogan's mother and stepfather…"). On {ask}: the question as a YELLOW caption, "Which movies have trivia mentioning hackers?".
> On {query}: slide 92's query, verbatim: `SELECT movie->>'title' AS title, movie->>'year' AS year` / `FROM    movies` / `WHERE EXISTS (` / `     SELECT 1` / `     FROM   unnest(movie->>'$.trivia_entries[*]') AS t(e)` / `     WHERE e ILIKE '%hacker%'` / `)` / `ORDER BY title;`. On {exists}: ch3 s6's semijoin loop, small: The Kid's five strips are tested one by one, none matches (verified), and The Kid is dropped RED; Hackers' strips are tested and the loop stops at the first GREEN match (its entry "The bearded London hacker is David A. Stewart of Eurythmics."). On {semijoin}: label "⋉ inside one document".
> On {ilike}: `ILIKE` YELLOW, "LIKE, ignoring case"; the two `%` signs GOLD, "any run of characters" (slide 39's LIKE).
> On {result}: the result (verified), slide layout: `title / year`: `Hackers 1995`, `Mission: Impossible 1996`, `Notting Hill 1999`, `Upgrade 2018`, `Who Am I 2014`. On {notting}: Notting Hill's row YELLOW, with a GOLD "?".
> On {thacker}: Notting Hill's matching entry, verbatim from its start: "(at around 1h 28 mins) The long shot where William Thacker walks through Notting Hill during summer, fall, winter, and spring was actually four different shots, all filmed the same day." The letters "hacker" inside "Thacker" light RED.
> On {hacked}: Snowden's entry, verbatim: "To make sure the screenplay was not hacked or leaked, Oliver Stone wrote the script on a single computer with no Internet connection." "hacked" GREEN, with a RED "missed" tag. On {hack}: the pattern edits to `'%hack%'`; GOLD 5 becomes GOLD 28 (verified). On {hackman}: six of the 28 titles RED, each tagged "Gene Hackman" (verified): Enemy of the State, RKO 281, Runaway Jury, The Royal Tenenbaums, The Shawshank Redemption, Unforgiven; one entry shown, "The script floated around Hollywood for almost 20 years. Gene Hackman read and rejected it, …" (Unforgiven). On {rank}: the five hacker results as equal-height bars, Hackers' and Notting Hill's the same.
> On {engines}: a search-engine diagram, names Elasticsearch and OpenSearch. On {words}: a trivia sentence splits into word tiles. On {stems}: hacker, hackers, hacking, hacked all funnel to one GREEN stem "hack"; "Hackman" stays a DIM tile of its own. On {typos}: "hakcer" bends to "hacker". On {relevance}: the results reorder by a GOLD relevance bar. On {json}: a TEAL document card drops into the engine. On {duck}: a small DuckDB tag "full-text search extension" (named only: it isn't installed here, so nothing was run).

[c8.text.1] {free} Documents often hold free text, like the trivia entries in each movie. {ask} So which movies have trivia that mentions hackers? {query} For each movie, un-nest its trivia into rows, and keep the entries that match a pattern. {exists} Then exists asks, is there at least one? {semijoin} That's the semijoin from part three, now running inside a single document.

[c8.text.2] {ilike} I-like is a version of like that ignores the difference between upper and lower case. The percent signs match any run of characters. {result} Five movies come back. Hackers, Mission Impossible, Upgrade, Who Am I, {notting} and Notting Hill. {pause} {thacker} Notting Hill has no hackers. Its hero is called William Thacker, and the six letters of hacker sit right inside his name.

[c8.text.3] {loose} So this pattern matches too much, and it also matches too little. {hacked} Snowden's trivia talks about keeping its script from being hacked, and hacked doesn't contain hacker. {hack} Shorten the pattern to hack, and you get twenty-eight movies, {hackman} six of them because of Gene Hackman. {rank} And nothing is ranked: Notting Hill counts as much as Hackers.

[c8.text.4] {engines} Searching text properly is the job of full-text search engines, such as Elasticsearch and OpenSearch. {words} They split text into words, {stems} and reduce each word to its stem, so hacker, hacking and hacked all match hack, while Hackman stays a word of its own. {typos} They tolerate spelling mistakes, {relevance} and they rank the results by relevance. {json} They store JSON documents too, so they can be used a bit like document databases, though they're built for search. {duck} And Duck D B has a full-text search extension of its own.

## Scene 6 · The JSON toolkit on one card (ch8_s6_summary)

> The TEAL toolkit card, the twin of ch3 s7's BLUE relational-algebra card (same card shape, same row-by-row build), titled "JSON in DuckDB", slide 93 verbatim, two columns `Syntax` / `Meaning` with a DIM header:
> `j->'key', j->'$.a[0].b'` extract a value as JSON · `j->>'key', j->>'$.a[0].b'` extract a value as a string · `j->>'$.a[*].b'` list of values, one per array element · `(j->>'key')::INTEGER` extract a number · `json_exists(j, '$.key')` does the key exist? · `json_array_length(j, '$.a')` number of elements in an array · `list_contains(l, x)` does list l contain x? · `list_has_all(l1, l2)` does l1 contain all of l2? · `FROM t, unnest(l) AS u(x)` one row per element of list l.
> Each row lands on its mark with a small DIM callback on The Kid at its right, from one verified run: `"The Kid"` and `The Kid` ({arrows}); `[Charles Chaplin]` for `movie->>'$.directors[*].name'` ({paths}); `1921` ({cast}); `true` for `json_exists(movie, '$.composers')` ({exists}); `true` for `list_contains(movie->>'$.genres[*]', 'Drama')` and for `list_has_all(movie->>'$.genres[*]', ['Comedy', 'Family'])` ({lists}); s2's ten rows ({unnest}).
> On {length}: the `json_array_length` row flashes YELLOW as the one new row: `json_array_length(movie, '$.actors')` → `10` (verified), the hook's ten chips counted off in GOLD.
> On {parens}: the footer "Put parentheses around -> and ->> in conditions!" in YELLOW.
> On {docs}: a DIM footnote under the card, "full details: DuckDB's JSON functions documentation".
> On {two}: ch3 s7's BLUE card slides in small at the left, the TEAL card beside it, the same size.

[c8.sum.1] {card} Here's everything we've used to query JSON in Duck D B, on one card, the twin of the card from part three. {arrows} The single arrow extracts a value as JSON, and the double arrow extracts it as a string. {paths} Either one takes a key or a JSON path, and a path with a star gives you a list. {cast} Cast with colon colon integer to get a number.

[c8.sum.2] {exists} JSON exists asks whether a key is there at all. {length} And here's one new function: JSON array length counts the elements of an array. The Kid's actors array has ten. {lists} List contains and list has all search inside a list. {unnest} And un-nest, in the from clause, gives you one row per element.

[c8.sum.3] {parens} The card ends with a warning: put parentheses around both arrows in every condition. {docs} For everything else, the notes point you to Duck D B's documentation of its JSON functions. {two} So now you have two toolkits on two cards, one for tables and one for documents.

## Scene 7 · Try these (ch8_s7_try)

> "Exercise 19" header; four DIM cards 19.1–19.4 in a row, the same exercise-card style as ch3 s8, ch5 s7 and ch6 s7, and a small tag "solutions: part 10". Each card grows to the hero position in turn and shrinks back when done. No solution query appears anywhere. On each {pause=2} the screen is still, with a small "pause and try it" label.
> 19.1 ({rename}): "What are the IDs of all documents that needed to be updated when Lana Wachowski changed her name? Assume you know her person_id is nm0905154." On {hint}: the path `$.*[*]` as a walk on The Kid's JSON tree (ch4's tree look, as ch7 s3 walked it): the `*` lights every top-level key, the `[*]` every element of the arrays. On {kid}: a GOLD counter reaches 22 (verified: genres 3, actors 10, directors 1, producers 1, writers 1, composers 1, trivia_entries 5). On {own}: a TEAL person card with a YELLOW outline, "her own document".
> 19.2 ({directors}): "Who are the five people who have directed the most movies?" On {hint}: `json_array_length(person, '$.directed')` with Charles Chaplin's value `5` in GOLD (verified). On {never}: Jackie Coogan's card beside it (no `directed` key) with a PINK `?` in place of a number; don't show the value (it's NULL, verified; the solution in part 10 deals with it).
> 19.3 ({acted}): "In which movies did one of the directors also act?" On {hint}: `list_has_any([1, 2], [2, 3])` → `true`, `list_has_any([1, 2], [3])` → `false` (verified). On {kid}: The Kid's two small lists, directors and actors, with Charles Chaplin YELLOW in both. On {ids}: two person cards with the same name and different IDs; the IDs GREEN, the names DIM.
> 19.4 ({rating}): "What is the average rating of the movies in each genre, for the five genres with the highest average rating?" On {hint}: s3's genre bars, small. On {cast}: `movie->>'rating'` with a RED tag "a string" and ch7 s4's GOLD `::` beside it.

[c8.try.1] {turn} Now it's your turn. {four} Exercise nineteen has four questions over the JSON database. For each, I'll give you a hint, and then a pause. {sol} The worked solutions are in part ten. {rename} One. When Lana Wachowski changed her name, which documents needed updating? You know her person ID. {hint} Here's the hint. The path dollar, dot, star, then a star in square brackets, matches every element of every array at the top level of a document. {kid} In The Kid, that's twenty-two elements. {own} And don't forget her own document. {pause=2}

[c8.try.2] {directors} Two. Who are the five people who have directed the most movies? {hint} The hint is the new function from the card, JSON array length. Charles Chaplin's directed array has five elements. {never} And think about what it returns for someone who never directed anything. {pause=2}

[c8.try.3] {acted} Three. In which movies did one of the directors also act? {hint} Hint: list has any is true when two lists have at least one element in common. {kid} The Kid qualifies, because Chaplin is in both lists. {ids} Compare people by ID, not by name, since two different people can share a name. {pause=2}

[c8.try.4] {rating} Four. Which five genres have the highest average rating? {hint} Hint: un-nest the genres, as before. {cast} But the double arrow gives you each rating as a string, so turn it into a number before you average it. {pause=2}

## Scene 8 · Recap (ch8_s8_recap)

> Each recap sentence brings back a small version of the visual that taught it, same objects, colours and styling, with its short line under it; they gather into a grid:
> {r1}: s2's three genre chips dropping into three rows, "un-nest: one row per element". {r2}: s2's outer loop, YELLOW cursor on The Kid, "once per movie, like a correlated subquery". {r3}: s3's genre bars next to has_genre's GOLD 7,826, "then all of SQL works". {r4}: s4's arrow from Henry Bergman's actor object to his person document, GOLD 1868, "unplanned questions need joins". {r5}: s5's "Thacker" with "hacker" RED inside it, "patterns are crude; search engines stem and rank". {r6}: s6's TEAL card, small, "the JSON toolkit".
> On {close}: the grid clears. On {two}: ch1 s2's BLUE schema map with The Kid's rows YELLOW, and ch4 s3's TEAL document card of The Kid, side by side; caption "same movies, two shapes". On {fast}: a few question cards from the lecture ("who's in The Kid?", "movies per genre", "actors' ages") slide to the side that answers them more easily.
> On {next}: two small title cards, "Part 9 · Solutions: subqueries and redundancy" and "Part 10 · Solutions: modelling and JSON queries". On {graph}: ch6 s3's tangle returns in Lecture 5's graph look (circles, Person PINK, Movie BLUE, plain lines: Charles Chaplin, Jackie Coogan, The Kid, The Gold Rush), captioned "Lecture 5 · Graph databases".
> Leave ~8 s of end card after the last word; the music carries it.

[c8.recap.1] {recap} Let's look back. {r1} The un-nest function turns a list into rows, one row per element. {r2} It runs once for each movie, on that movie's own list, like a correlated subquery. {r3} After that, the elements are ordinary rows, so grouping, sorting and joins all work. {r4} But questions the designer didn't anticipate, like the actors' ages, send you back to joins. {r5} Pattern matching on text is crude, and search engines do better: they split words, find stems, and rank. {r6} And the whole JSON toolkit fits on one card. {pause}

[c8.recap.2] {close} That completes the lecture. {two} We stored the same movies in two shapes: tables, with each fact in one place, and documents, with each movie in one piece. {fast} Each shape makes different questions easy, so the questions you'll ask should pick the shape. {pause}

[c8.recap.3] {next} Next time, the worked solutions, in parts nine and ten. {graph} Then lecture five, where the tangle from part six, the people and movies that wouldn't fit in a tree, gets a model of its own: the graph. {pause}
