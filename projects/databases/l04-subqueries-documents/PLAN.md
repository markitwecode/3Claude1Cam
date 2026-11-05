# Subqueries and Documents: plan

Request: "make videos on the two database lectures in downloads. all the notes and materials are on
the course page. now, try to structure it so it makes sense and is engaging, builds from first
principle with minmimal arbitrary memorization. make databases cool again. (but also of course all
the material should be there)" (via the producer, 2026-11-01). This is Lecture 4 of Databases
(Cambridge CST Part IA, Michaelmas 2026/27, Dr Martin Kleppmann), recorded Tue 2026-10-27. The
producer's scope: all of §3.6 Query composition (the recording recaps its first half, which
Lecture 3 taught) and all of ch. 4 Document databases, up to the JSON summary.
Audience: a Cambridge first-year studying the course. They attended Lectures 1–3 (no videos exist):
the movies database and its seven tables, keys, SELECT / WHERE / ORDER BY / LIMIT, GROUP BY and
HAVING, aggregates, inner and LEFT joins (with the nested-loop pseudocode), set operations,
DISTINCT and multisets, NULL and three-valued logic, the relational algebra operators σ π ρ γ × ⋈.
From FoCS they know OCaml (static types); from the notes' pseudocode, Python.
Sources (project.json): notes `../source/databases-notes.pdf` pp. 32–49 (PDF page = printed page;
refreshers from pp. 11–16 and 24–32); slides `../source/databases-handout.pdf` (slide N is handout
p. N+3 up to slide 69 = p. 73; slides 70–93 are pp. 76–99); exercises 13–19; the real databases
`../source/movies.duckdb` and `../source/movies-json.duckdb`; the recording's transcript
(`../source/94772e13-….transcript.md`, teaching 00:04:34–00:57:20). There is no digest (Gemini
was off); see Decisions.
Total: 10 chapters (8 core + 2 bonus solution chapters), ~101 min of narration (~16,200 words):
core ~80.5 min, bonus ~20.5 min.

Every query, count and error message in this plan was run on DuckDB 1.5.6 against the real
databases (2026-11-01). Script-writers still run every query they put on screen (project.json
`toolchain`), including the ones meant to fail, and quote output exactly.

## Lecture-wide conventions (set in ch1 and ch4, kept to the end)

- **On-screen SQL** as in the notes' slides: keywords upper case, table and column names lower
  case, the slides' aliases (`m`, `r`, `p`, `hp`, `t(a)`). `Code()` colours it with the `sql`
  lexer (keywords BLUE, strings and numbers GOLD). Result tables are typeset like the slides
  (a DIM header row, plain values, the slides' number formats such as 7.4 and 1,086) and must match
  what DuckDB returns. Error messages are quoted verbatim, DuckDB's wording and all.
- **On-screen JSON** as in slides 70–73: two-space indentation, keys in double quotes, the slides'
  `/* 9 more */` elisions in DIM. Say once (ch4 s3) that these comments are slide shorthand and
  JSON itself has no comments. Brief every JSON block as `Code(src, lang="json")` (the
  per-block lexer); recolour where meaning needs it: braces and brackets TEAL, `null` PINK.
- **Relational algebra** as in the notes: σ selection, π projection, ρ renaming, γ grouping,
  × product, ⋈ join, ⟕ left outer join, ⋉ semijoin, ▷ antijoin, ∪ ∩ −. The condition goes in
  the subscript: `movies ▷_movie_id plays_role`. Narration names the operator ("the antijoin"),
  never the glyph.
- **Cross-references aloud:** the videos are "part one" … "part ten", the title cards' word.
  "Chapter" is kept for the notes' chapters ("chapter four of the notes"), since the notes'
  ch. 4 and our part four are different things. Slides are never cited aloud by number.
- **Names (used the same way in every chapter):** derived table; common table expression;
  scalar subquery; correlated subquery; semijoin and antijoin (one word each, as in the notes);
  three-valued logic; document; collection (MongoDB's word, ch4 only); redundancy; normalised and
  denormalised (British spelling on screen, as the notes); update / deletion / insertion anomaly;
  first normal form; source of truth and derived data; locality; schema-on-write and
  schema-on-read; JSONPath; unnest.
- **Narration (write for the ear):**
  - SQL is "sequel", the lecturer's own word (the captions write "sequel practicals",
    00:17:44). DuckDB is "Duck D B". JSON is "JSON" (listen once: it should come out "jay-son").
    MongoDB "Mongo D B", CouchDB "Couch D B", PostgreSQL "Postgres" (the lecturer's word).
  - Keywords in narration in lower case: "not in", "not exists", "exists", "with", "having",
    "union all", "null". Upper-case "IN" or "AS" may be spelled out letter by letter.
  - Table and column names as words: "plays role", "has position", "has genre", "movie ID",
    "person ID", "death year", "birth year", "rating votes", "trivia entries", "acted in",
    "composed for". Function names likewise: "list contains", "list has all", "JSON exists",
    "JSON array length", "un-nest". ILIKE is "I-like" (listen). `->` is "the arrow", `->>` "the
    double arrow", `::INTEGER` "colon colon integer", `$` "dollar", `[*]` "the star", `[0]`
    "index zero", `<>` "not equal to". MongoDB's `$gte`: "a greater-than-or-equal operator,
    dollar G T E" (listen).
  - Never read an ID aloud (tt0012349, nm0000122): say "The Kid's ID", "Chaplin's person ID".
  - Aliases by role, not by letter: "the outer movie", "a role row". Exercise 13's tables and
    columns are "table ar", "table ess", "ex", "why", "zed" (the studio's letter words).
  - Titles to listen for: "Sherlock Junior" (written Sherlock Jr.), Kaiva, Wachowski, "Food,
    Inc.", B. F. Blinn, Boyce–Codd.
- **Colours** (meaning first; `lib.style` names):
  - BLUE: the relational world. SQL keywords, table cards, the schema map.
  - TEAL: the document world. JSON braces and brackets, document cards, the JSON tree, JSONPath
    steps. Nothing relational is TEAL.
  - YELLOW: attention. The running movie's rows when they light up; the current outer row in a
    correlated subquery (ch3, ch8).
  - GOLD: numbers that matter. Row counts (1,086 vs 3,281), copies (21), ages, ratings.
  - GREEN: TRUE, rows kept, a correct result. RED: FALSE, errors, the traps.
  - PINK: NULL and only NULL, the unknown third truth value (ch2–ch3), and the SQL NULL that a
    missing key returns (ch7). Inside `Code()` blocks the lexer colours NULL BLUE; recolour it PINK
    with `find()` where it matters.
  - One stated exception, ch6 s3's tangle only: it previews Lecture 5's graph look (its PLAN.md
    conventions), so its vertices are circles, Person PINK and Movie BLUE. No NULL appears in that
    scene.
  - PURPLE is unused.
  - DIM: header rows, elisions, secondary labels, what's out of focus.
- **Running examples:**
  - *The Kid* (1921, Charles Chaplin), the notes' own running movie: across the seven tables
    (ch1), caught by the NOT IN trap (ch2) and freed by NOT EXISTS (ch3), as one document (ch4),
    its copies (ch5), as a tree (ch6), under the arrows and JSONPath (ch7), its cast unnested and
    its actors' ages (ch8).
  - *Which movies have no actors?* Flow (2024) and Kaiva (2023), answered four ways: LEFT JOIN with
    IS NULL and EXCEPT (recalled, ch2), NOT IN (ch2), NOT EXISTS (ch3). Flow is the dialogue-free
    animated film; Kaiva has ten actor credits in has_position but no rows in plays_role, so the
    query answers exactly what was asked (say so once, ch2 s3).
  - *The death-year question:* "Which movies came out in a year in which none of the people in
    the database died?" Four movies: The Kid 1921, Sherlock Jr. 1924, The General 1926, It Happened
    One Night 1934. NOT IN gives 0 rows (ch2); `WHERE deathyear IS NOT NULL` or NOT EXISTS gives
    the four (ch2, ch3).
  - *Composers:* 1,086 people hold 3,281 composer credits (Hans Zimmer 72). The semijoin finds the
    1,086 (ch3); `json_exists(person, '$.composed_for')` finds the same 1,086 in the documents
    (ch7): one fact, two models.
  - *Crime and Drama:* 621 Crime, 1,691 Drama, 397 both (ch1's Venn); the document database counts
    the same 621 and 1,691 after unnest (ch8).
  - *Lana Wachowski* (person ID nm0905154): the update anomaly (ch5) and Exercise 19.1 (ch8 hint,
    ch10 solution). ch5 doesn't give the number of documents; that is 19.1's answer.
- **Running visuals** (the scene that first builds one owns its helper, imported with
  `load_scene`; its director records the name in STATUS.md, so build those scenes first):
  - *The schema map* (ch1 s2), the relational motif: seven table cards laid out as on slide 23,
    entity tables (movies, people, genres) and ratings, and the three join tables (has_genre,
    has_position, plays_role) drawn as narrower cards between them; primary-key columns underlined;
    foreign-key arrows. The Kid's rows can light up YELLOW in each card. Back in ch4 s1 (seven
    tables for one web page), ch4 s3 (rows fly into the document), ch5 s2, ch6 s2, and Lecture 5.
  - *The Venn of Crime and Drama* (ch1 s4): back in ch7 s6 and ch8 s3.
  - *The truth tables* (ch2 s5): AND, OR and NOT as small 3×3 grids, TRUE GREEN, FALSE RED, NULL
    PINK. *The AND chain* (ch2 s6): `1921 <> v` links, one PINK link poisoning the chain.
  - *The outer loop* (ch3 s2): the movies list on the left with a YELLOW cursor, the subquery's
    scan of plays_role on the right, a row counter between them. Back in ch3 s6 (the pseudocode)
    and ch8 s2 (unnest runs once per movie).
  - *The JSON tree* (ch4 s2) and *the document card* (ch4 s3), the document motif: the same
    value drawn two ways, as indented JSON and as a tree (root, keys on the edges, values at the
    leaves). JSONPath walks the tree in ch7 s3.
  - *The two-way copies* (ch4 s5): The Kid's card and Chaplin's card side by side, ID references as
    arrows both ways, copied names and titles GOLD. ch5 counts on it; Lecture 5 calls back to it.
  - *The tangle* (ch6 s3): the many-to-many relationship drawn as itself, in Lecture 5's look
    (circles; Person PINK, Movie BLUE; plain lines). Start from Lecture 5's house subgraph, Charles
    Chaplin, Jackie Coogan, The Kid and The Gold Rush, then let it grow (Chaplin's other movies:
    City Lights, Modern Times, The Great Dictator, Chaplin; The Kid's other actors) until the lines
    cross: "not a tree but a graph". Lecture 5's ch1 s2 redraws the same four from first
    principles, so the two lectures meet on one picture.
  - *The toolkit cards:* the relational-algebra summary (ch3 s7, slide 68) and the JSON summary
    (ch8 s6, slide 93), drawn as the same kind of card, BLUE and TEAL.

## Chapter 1 · Queries inside queries
Slug: ch1_subqueries · ~10 min · Source: notes pp. 32–33 (§3.6, slides 60–63); refreshers
pp. 11–16 (slides 19–25, schema and The Kid), p. 24 (slide 45, HAVING), p. 30 (slides 56–57, set
operations) · Recording: 00:04:34–00:05:47 (the lecturer's recap)
Goal: explain why SQL can't stack operators the way relational algebra does, and use a query's
result as a table (derived table, WITH) or as a single value (scalar subquery).
Scenes:
- s1_hook · Hook (~50 s): title card ("Subqueries and Documents", "Databases · Lecture 4",
  "Part 1 · Queries inside queries"). In relational algebra every operator takes relations and
  returns a relation, so they stack: build σ(γ(σ(movies))) up from the movies table like bricks.
  SQL's SELECT is a form with fixed boxes, each used once, in order. Question: how do you make SQL
  stack?
- s2_schema · The movies database in one minute (~80 s): refresher, slides 19 and 23–25.
  - Build the schema map (see conventions): entity tables, join tables, keys, arrows.
  - The Kid across the tables: one movies row (1921, 68 minutes), one ratings row (8.2), three
    has_genre rows to Comedy, Drama, Family; Chaplin's one people row, his five has_position rows
    (actor, composer, director, producer, writer), one plays_role row ("A Tramp").
  - A join matches keys: movies ⋈ ratings on movie_id puts The Kid's title next to its 8.2. This
    is all the viewer needs from Lectures 1–3; nothing more.
- s3_form · SQL's fixed form (~85 s): slides 60 and 45.
  - The clauses SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY: each at most once, in that
    order; executed FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.
  - Derive why one σ needs two names: WHERE sees single rows before grouping, HAVING sees groups
    after it. "Which years had more than 140 movies?" with HAVING: 2013 153, 2014 146, 2016 147.
  - `WHERE n_movies > 140` fails: "Binder Error: WHERE clause cannot contain aggregates!" (DuckDB
    resolves the alias to COUNT(*)). Selection happens before grouping.
  - The clunkiness: one concept, two keywords, and no third σ after that.
- s4_setops · Combining whole results (~80 s): slides 56–57, the notes' remark on slide 60.
  - Crime (genre 6) and Drama (genre 8) as a Venn diagram: INTERSECT 397, UNION 1,915, EXCEPT
    (Crime but not Drama) 224. UNION ALL gives 2,312 = 621 + 1,691: the 397 counted twice. Both
    sides need the same columns; the plain forms remove duplicates.
  - The limit: these put two results side by side. None of them lets one query's result be
    another query's input.
- s5_derived · A query where a table goes (~90 s): slide 61.
  - Since a query returns a relation, it can stand wherever a table can: parentheses in FROM,
    named with AS. The 140-movie question as a derived table, `per_year`: same three rows, and the
    same plan as the HAVING version (the DBMS sees the same algebra).
  - The SQL standard requires the name even when it's never used; DuckDB doesn't (both run).
  - You read it inside out: show the eye jumping to the inner query first.
- s6_with · Name it first: WITH (~70 s): slide 62.
  - The same query as a common table expression: run A, name its result, use the name like a
    table. Read top to bottom. Like a variable: a name can be used more than once, and you can
    define several.
- s7_scalar · A query where a value goes (~100 s): slide 63.
  - "Which 1976 movies are rated above the overall average?" The obvious
    `WHERE ... rating > AVG(rating)` fails with the same binder error. Derive it: WHERE judges one
    row at a time, and an average needs all of them.
  - The subquery `(SELECT AVG(rating) FROM ratings)` returns one row and one column: a scalar
    subquery, usable wherever a value is. It mentions nothing from the outer query, so it runs
    once and becomes a number, 7.17, before the outer query starts.
  - 1976 has five movies; four clear 7.17: Carrie 7.4, Network 8.1, Rocky 8.1, Taxi Driver 8.2.
    King Kong (6.0) stays out.
- s8_recap · Recap (~65 s, then the ~8 s end card): three small callbacks with one line each: the
  algebra tower vs the fixed form (s1/s3), the Venn (s4), the subquery as a table in FROM and as
  a name in WITH (s5/s6), the subquery collapsing to 7.17 (s7). Next: a subquery that returns a
  whole column of values, the IN operator, and a trap hiding in its negation.
Continuity: builds the schema map and the Venn (conventions). Table, value, and next time column:
the three shapes of a subquery carry through ch2. The 140-movie query appears three times (HAVING,
derived table, WITH) with identical results: keep the three on screen in one layout.

## Chapter 2 · NOT IN and the NULL trap
Slug: ch2_not_in · ~9 min · Source: notes pp. 33–34 (slide 64 and the death-year example);
refreshers pp. 27–28 (slides 51–52, LEFT JOIN), p. 30 (Exercises 9 and 11), pp. 30–32 (slides
58–59, NULL and three-valued logic) · Recording: 00:05:47–00:06:39
Goal: use IN and NOT IN with a subquery, and derive from three-valued logic why a single NULL in
the list makes NOT IN return nothing, and how to defend against it.
Scenes:
- s1_hook · Hook (~50 s): title card ("Part 2 · NOT IN and the NULL trap"). Last time: a subquery
  can stand for a table or a single value. The death-year question: "Which movies came out in a
  year in which none of the people in the database died?" The answer is four movies. The natural
  query returns 0 rows: no error, no warning. {pause}
- s2_absent · Asking about absence (~70 s): the friendlier example, "which movies have no actors?"
  Flow and Kaiva. The two ways from earlier lectures:
  - LEFT JOIN plays_role, then `WHERE r.movie_id IS NULL`: the NULL padding marks the missing
    match (Exercise 9, slide 52's loop).
  - EXCEPT on movie IDs (Exercise 11). One line on why IDs and not titles: titles repeat (two
    movies each called The Italian Job, Total Recall, The Mummy), so EXCEPT on titles could hide a
    movie.
- s3_notin · A subquery that returns a column (~75 s): slide 64's query.
  - `movie_id NOT IN (SELECT movie_id FROM plays_role)`: one column, many rows, so it can't go
    next to `>`, but it can go after IN, which tests membership of a set. It reads like the
    English question. Result: Flow, Kaiva.
  - Kaiva lists ten actors in has_position, but none of them has a character in plays_role. The
    query answered exactly what it was asked.
- s4_trap · The trap, in full (~65 s): the death-year query
  `SELECT title FROM movies WHERE year NOT IN (SELECT deathyear FROM people)` → 0 rows. Show
  why it should be four: The Kid came out in 1921, and nobody in people died in 1921. 20,494 of
  23,179 people have a NULL death year (alive, or unknown). {pause} What does NOT IN do with them?
- s5_logic · Three-valued logic from one idea (~105 s): refresher of slides 58–59, derived rather
  than memorised.
  - NULL isn't a value; it means "unknown". So `1921 <> NULL` is unknown: NULL.
  - The rule that builds every table: treat NULL as "could be TRUE, could be FALSE". Try both. If
    both give the same answer, that's the answer; if not, the answer is NULL.
  - FALSE AND NULL: false either way, so FALSE. TRUE AND NULL: depends, so NULL. TRUE OR NULL:
    TRUE. NOT NULL: NULL. Fill the AND, OR, NOT grids this way, cell by cell.
  - WHERE keeps a row only when its condition is TRUE. NULL and FALSE both drop it.
- s6_derive · Why NOT IN can never be true (~105 s): slide 64's bullets, as a derivation.
  - `c NOT IN (v1, …, vn)` means `(c <> v1) AND … AND (c <> vn)`. For The Kid: 2,685 TRUE links
    (every known death year differs from 1921) and 20,494 `1921 <> NULL` links, PINK. An AND chain
    needs every link TRUE, and a single unknown link would already stop it being TRUE. The Kid is dropped, and so is every other movie: either some
    death year equals its year (FALSE) or a NULL makes it NULL. 0 rows.
  - The notes' small case: `3 NOT IN (1, 2, NULL)` is NULL, though 3 plainly isn't in the list.
  - The positive form is safe: IN is an OR chain, and `1 IN (1, 2, NULL)` finds its TRUE link.
    (`3 IN (1, 2, NULL)` is NULL, and WHERE drops it exactly as it would drop FALSE.)
  - The fix: `WHERE deathyear IS NOT NULL` inside the subquery gives the four movies.
  - Why slide 64's query was safe: plays_role.movie_id is part of the primary key, so it is never
    NULL. The lecturer's advice: when you see NOT IN, let alarm bells go off.
- s7_recap · Recap (~65 s, then the ~8 s end card): the column-shaped subquery (s3), the grids
  (s5), the AND chain with its PINK link (s6), the fix. Next: ask the question we meant, "is there
  at least one match?", directly. The operator is called EXISTS.
Continuity: from ch1, the three shapes of subquery (here the column). The death-year question and
Flow and Kaiva both return in ch3, solved by NOT EXISTS: end this chapter with the four movies
GREEN and NOT IN's empty result RED. Exercise 13.4 (in ch3's hints) compares s2's LEFT JOIN with
NOT IN.

## Chapter 3 · EXISTS: semijoins and antijoins
Slug: ch3_exists · ~11 min · Source: notes pp. 34–36 (slides 65–68, Exercises 13–14); refresher
p. 26 (slide 48, nested loop join) · Recording: 00:06:39–00:16:47
Goal: write correlated subqueries with EXISTS and NOT EXISTS, explain why NOT EXISTS is immune to
NULLs, tell a semijoin from a join, and read the whole relational-algebra toolkit.
Scenes:
- s1_hook · Hook (~50 s): title card ("Part 3 · EXISTS: semijoins and antijoins"). Last time: one
  NULL made NOT IN return nothing. The question we meant was simpler: for this movie, is there at
  least one matching row? The Kid has twelve rows in plays_role; Flow has none. SQL can ask that
  directly.
- s2_correlated · A subquery that looks outward (~90 s): slide 65, the notes' paragraph above it.
  - The subquery mentions `m`, a movie from the outer query: a correlated subquery. Picture it
    run once per outer row (the outer loop visual): the cursor on The Kid, the inner scan finds
    twelve rows; on Flow, it finds none.
  - Contrast ch1: the 7.17 subquery mentioned nothing outside and ran once. The real query plan
    may be cleverer than per-row; the meaning is per-row.
- s3_notexists · NOT EXISTS: the antijoin (~95 s): slide 65.
  - EXISTS is TRUE if the subquery returns at least one row; NOT EXISTS if it returns none.
    Result: Flow, Kaiva, the same two as LEFT JOIN, EXCEPT and NOT IN.
  - `SELECT 1`: the rows' content doesn't matter, only whether there are any. The lecturer's demo:
    `SELECT role FROM plays_role` and `SELECT 1 FROM plays_role` both return 30,303 rows, the
    second just a column of ones.
  - In relational algebra, the antijoin: movies ▷_movie_id plays_role. The lecturer's picture: a
    LEFT JOIN with the IS NULL filter baked in, without building the matched rows only to throw
    them away. A good optimiser runs all these versions the same way; pick the one that reads best.
- s4_immune · Why NOT EXISTS can't be fooled (~85 s): the notes' remark before slide 65.
  - The death-year question with NOT EXISTS (`WHERE p.deathyear = m.year` inside) returns the four
    movies (verified).
  - Derive it. Inside the subquery, a NULL death year makes `p.deathyear = 1921` NULL, and WHERE
    drops that row: an unknown simply isn't a match. EXISTS only asks how many rows came back,
    zero or more, and that answer is always TRUE or FALSE. The NULL never reaches the outer
    condition.
- s5_semijoin · EXISTS: the semijoin (~105 s): slide 66, the lecturer's live demo
  (00:11:37–00:14:44).
  - "Who is credited as a composer on at least one movie?" The JOIN version returns 3,281 rows,
    one per credit: Hans Zimmer appears 72 times. The EXISTS version returns 1,086 rows, one per
    person.
  - The semijoin ⋉: the left rows that have at least one match, no columns from the right, never
    duplicated. people ⋉_person_id (σ_position='composer'(has_position)).
  - The lecturer fixed the join with `DISTINCT people.person_id, name`, also 1,086. Leave open
    what would go wrong with DISTINCT name alone: that is Exercise 14.
- s6_loops · Two loops, one difference (~85 s): slide 67, with slide 48's nested loop join as the
  starting point.
  - The inner join's loop outputs every match. The semijoin's loop appends the person and breaks
    at the first match (at most one row per person). The antijoin's loop sets `matched` and
    outputs the movie only when nothing matched. Animate on the outer-loop visual from s2.
  - EXISTS and NOT EXISTS are inverses, and so are semijoin and antijoin.
- s7_toolkit · The whole toolkit on one card (~60 s): slide 68 built row by row (WHERE σ, SELECT
  π, AS ρ, GROUP BY γ, FROM a, b ×, JOIN ⋈, LEFT JOIN ⟕, EXISTS ⋉, NOT EXISTS ▷, UNION ∪,
  INTERSECT ∩, EXCEPT −), the two new rows flashing. Relational algebra works on sets, SQL on
  multisets (ch1 s4's UNION ALL is the reminder).
- s8_recap · Try these, and recap (~100 s, then the ~8 s end card):
  - Exercise 13 card (the four pairs over tables ar(ex, why) and ess(why, zed)) with hints: (1)
    what does a join do when a row of ar matches two rows of ess? (2) for an inner join, does it
    matter whether a condition sits in ON or WHERE? (3) for a LEFT JOIN it does: remember
    slide 54's Annie Hall; (4) what if ess.why contains a NULL, or ar.why is NULL? Think of ch2.
  - Exercise 14 card: the composers with an inner join, correct even when two different people
    share a name. Hint: what does DISTINCT compare?
  - Recap: the outer loop (s2), the four movies back (s4), 3,281 vs 1,086 (s5), the two loops
    (s6). Next: the relational toolkit is complete. A completely different way to store the same
    movies: documents.
Continuity: the outer-loop visual returns in ch8 s2 (unnest "like a correlated subquery") and the
EXISTS shape in ch8 s5 (searching trivia). 1,086 returns in ch7 s7. Solutions to 13 and 14 are in
ch9.

## Chapter 4 · A movie in one piece
Slug: ch4_documents · ~10 min · Source: notes pp. 36–40 (§4 intro and §4.1, slides 69–75) ·
Recording: 00:16:47–00:29:21 (00:16:47–00:18:58 is course logistics: one sentence at most)
Goal: read and write JSON, explain how the movies database becomes two collections of documents,
and say what a document database is.
Scenes:
- s1_hook · Hook (~55 s): title card ("Part 4 · A movie in one piece"). Last time: the relational
  toolkit complete. Slide 69: IMDb's "Full cast & crew" page for The Kid (redraw it as a simple
  mock page: title, poster box, director, writer, cast). To build it, the schema map lights up all
  seven tables (the lecturer counts them, 00:19:37). Question: what if the database stored this
  page's data the way the page reads it, in one piece?
- s2_json · JSON in two minutes (~100 s): slide 70, the notes' paragraphs around it.
  - The Ada Lovelace object: objects `{ }` of key–value pairs with string keys; arrays `[ ]`,
    ordered; scalars: strings in double quotes, numbers, true, false, null.
  - Nesting to any depth makes a tree: redraw the object as the JSON tree (the lecturer's
    description, 00:21:16).
  - Minimal types: one kind of number (no integer/float split), no dates (strings instead).
  - Everywhere: web APIs, configuration files, logs; every language reads it (a Python dict and
    list). XML did this job once. Using the same format in the database as in the web API saves
    conversion code.
- s3_movie · The Kid as one document (~110 s): slide 71. Build it by gathering from the schema
  map: rows fly from the tables into the card.
  - movie_id, title, year, type, minutes from movies; rating and rating_votes from ratings.
  - genres becomes an array of names: no has_genre table needed.
  - actors: an array of objects with person_id, name, and an array of roles (plays_role plus
    people): ten of them. directors, producers, writers, composers: the same with a job key.
  - trivia_entries: snippets of IMDb trivia that exist only in the JSON version.
  - Say once: the `/* 9 more */` comments are slide shorthand; JSON allows no comments.
- s4_person · Chaplin as a document (~95 s): slide 72 and the paragraph after it.
  - acted_in: an array of {movie_id, title, year, roles}, five movies; also directed, produced,
    wrote, composed_for.
  - A key exists only if it applies: Alfred Hitchcock's document has just person_id, name,
    birthyear, deathyear, directed (verified with json_keys). An unknown birth year is left out,
    not set to null. The lecturer: an empty array would also have been a fine design (00:23:59).
  - Even elements of one array differ: 731 elements of directed arrays have a job key, 2,435
    don't. Nothing forces two documents to share a structure.
- s5_shape · Two kinds of document (~80 s): slide 73.
  - The structure map of both: movies and people. Arrows are references by ID; names and titles
    are also copied, so each document is useful on its own.
  - The many-to-many relationship that has_position and plays_role held is now stored twice,
    once inside each movie and once inside each person. Build the two-way copies visual.
- s6_store · Where documents live (~100 s): slides 74–75.
  - In DuckDB: `CREATE TABLE movies(movie_id TEXT PRIMARY KEY, movie JSON NOT NULL)` and the same
    for people: 2,935 and 23,179 rows. The database knows nothing about what's inside the JSON,
    and the notes' §2 constraints (keys, NOT NULL, foreign keys) don't reach inside it. The file is on the course page and opens in
    the same DuckDB, in the browser or on the command line.
  - Document databases: MongoDB (collections; each document's key is `_id`), CouchDB,
    Couchbase. MongoDB's queries are themselves JSON-like: `{ year: { $gte: 2021 } }`;
    `{ genres: "War" }` matches if any element of the array matches; `"directors.name"` reaches
    into nested objects. The lecturer isn't a fan of the `$gte` style (00:28:52).
  - Relational databases added JSON (PostgreSQL, MySQL, SQLite, DuckDB; the SQL standard since
    2016), so one database can mix both models.
- s7_recap · Recap (~65 s, then the ~8 s end card): the tree (s2), the gathering (s3), Hitchcock's
  short document (s4), the two-way copies (s5), two tables in DuckDB (s6). Next: those copies,
  what they buy and what they cost.
Continuity: builds the JSON tree, the document card and the two-way copies (conventions); JSON
blocks are `Code(src, lang="json")`. ch7 queries exactly these documents, and the MongoDB filters
of s6 return in ch7 s6 as SQL.

## Chapter 5 · One fact, one place
Slug: ch5_normalisation · ~10 min · Source: notes pp. 40–43 (§4.2, slides 76–80, Exercises
15–16); refresher p. 20 (slide 35, INSERT) · Recording: 00:29:21–00:36:06
Goal: define redundancy, normalised and denormalised data, derive the update, deletion and
insertion anomalies from where copies live, and weigh what denormalising buys against what it
costs.
Scenes:
- s1_hook · Hook (~50 s): title card ("Part 5 · One fact, one place"). Last time: The Kid in one
  document. Count Chaplin's name (slide 76): once in the relational database, but in the
  documents once in his own and 21 times in six movie documents, five of them in The Kid alone
  (actor, director, producer, writer, composer). The Kid's title: its own document plus ten people
  documents. Bug or feature?
- s2_terms · Normalised and denormalised (~100 s): slides 76–77.
  - Redundancy: the same fact stored in several places. Normalised: every fact in exactly one
    place, everything else refers to it by key. Denormalised: copies kept where reads need them.
  - Why a key and not the name: an ID that never needs to change and means nothing to humans;
    names change, and two people can share one (the lecturer, 00:30:33).
  - Not tied to the model: a title column added to plays_role would denormalise the relational
    schema; movie documents holding only actor IDs would be normalised (and need a join). As a
    loose rule, relational databases are often normalised, document databases often
    denormalised.
- s3_update · When a copied fact changes (~100 s): slide 78.
  - Lana Wachowski changes her name. Relational: one UPDATE of one row (the slide's SQL).
  - Documents: her own document, then every movie document holding a copy. First find them
    (scan every movie document, or keep an index for it), then rewrite each one. Don't give the
    count; it's Exercise 19.1.
  - Miss one, or crash halfway without a transaction, or race a concurrent update (the lecturer,
    00:33:45), and the copies disagree. That's an update anomaly, and nothing in the database
    prevents it.
- s4_genres · Losing a genre, and never gaining one (~80 s): the notes' paragraph after slide 78,
  made real with the data.
  - In the documents, genre names live only inside movies. Deletion anomaly: delete the last
    movie of a genre and the genre vanishes. News appears in exactly one document, Food, Inc.
    (2008).
  - Insertion anomaly: a genre can't exist until some movie has it. The relational genres table
    has 26 genres; the documents only know 23. Epic, Experimental and Gothic have no movies, so
    they exist only in the relational database. slide 35's `INSERT INTO genres ... (27,
    'Superhero')` works with no movie at all.
- s5_forms · Normal forms (~75 s): slide 79.
  - First normal form: every value in a table is atomic, a single number or string, never a list
    or a nested record. That is why has_genre exists: one row per movie–genre pair instead of a
    list in a column. `"genres": ["Comedy", "Drama", "Family"]` violates it by design.
  - Second, third, Boyce–Codd normal form remove other redundancy, for example a column determined
    by another column that isn't the key. Not examined in detail; the principle is one fact, one
    place.
  - Violating them can be a deliberate choice: many databases support JSON and arrays. The
    lecturer: you're not a bad person for it (00:34:52).
- s6_why · Why denormalise anyway (~100 s): slide 80.
  - Count the reads: the movie page is one document read, against most of the seven tables. Data
    read together is stored together (locality), and that matters most when each lookup costs a
    disk seek or a network round trip. Precomputed results too: a forum stores each thread's reply
    count instead of counting every time.
  - Count the writes: more data to write and store, and every copy must be kept consistent.
  - The trade: if you mostly read and rarely update, denormalise (the lecturer, 00:32:26).
  - The rule that gets the best of both: the normalised data is the source of truth; denormalised
    data is derived from it, like a cache, and can be regenerated whenever it's lost or wrong.
- s7_recap · Try these, and recap (~95 s, then the ~8 s end card):
  - Exercise 15 card: an index is redundancy too. Hint: who keeps the copies consistent, what
    happens on reads and on writes, and does an index change how queries are written or what they
    return? (slide 34: an index changes performance, not results.)
  - Exercise 16 card: build one document per movie from the relational tables. Hint: json_object
    takes alternating keys and values; the list aggregate collects a group into a list; think
    about movies with no genres or no actors.
  - Recap: Chaplin's 21 copies (s1), one UPDATE vs many documents (s3), 26 vs 23 genres (s4),
    has_genre vs the genres array (s5), source of truth and derived data (s6). Next: when is a
    document the right shape, and who checks that it has one?
Continuity: counts on ch4's two-way copies. ch8 s4 returns to "denormalised documents only help
the queries their designer anticipated". Solutions to 15 and 16 are in ch9.

## Chapter 6 · Documents or tables?
Slug: ch6_models · ~9.5 min · Source: notes pp. 43–45 (§4.3, slides 81–83, Exercises 17–18);
refreshers p. 16 (slide 28, relationship shapes), p. 19 (slide 33, schema migration), p. 26
(slide 48, index nested loop join) · Recording: 00:36:06–00:39:48
Goal: decide when data fits documents and when it fits tables, from the shape of its
relationships and from when its schema is checked; read a JSON Schema.
Scenes:
- s1_hook · Hook (~50 s): title card ("Part 6 · Documents or tables?"). Last time: denormalising
  buys fast reads and costs careful writes. But some data fits a document naturally and some
  doesn't. Is a movie a tree? Show The Kid's tree: the trivia hangs off it neatly; Chaplin's
  branch also belongs to five other movies.
- s2_tree · What fits in a tree (~85 s): slide 81's first half, slide 28.
  - One-to-one: keys in the same document (rating, rating_votes); relationally, the separate
    ratings table.
  - One-to-many: an array nested inside (trivia_entries: each entry belongs to one movie and
    nothing else). In a relational schema it needs its own table and a join to read the movie with
    its details.
- s3_graph · Many-to-many is not a tree (~110 s): slide 81's second half, the notes' paragraph.
  - Build the tangle (conventions): Chaplin, Jackie Coogan, The Kid, The Gold Rush, then more
    movies and people until the lines cross. A movie has many people, a person many movies: no
    single document naturally contains both. The lecturer: you can't nest people
    inside movies, since a person may have no movie at all (00:36:40).
  - Two ways out: store the relationship twice with copies (what our database does, paying ch5's
    costs), or store only IDs and look them up on read, which is a join in all but name. Some
    document databases have no joins, so the application fetches each referenced document one by
    one, the index nested loop join of slide 48 done by hand.
  - Query in both directions (a movie's cast, an actor's movies): store it twice, or add a
    secondary index.
  - Tease Lecture 5: a third model built for exactly this picture, the graph.
- s4_schema · Who checks the shape? (~95 s): slide 82's first half.
  - Schema-on-write: the relational database checks every write; no unknown column, no string in
    an INT column. Reads return known types, and queries can be type-checked.
  - Schema-on-read: a document database accepts any JSON. "Schemaless" is misleading: the code
    that reads the documents assumes a structure (a name key holding a string), so there is a
    schema; it is implicit and checked only on read.
  - The analogy the viewer knows: OCaml's compiler checks types before the program runs (static);
    Python finds a type error when the line runs (dynamic).
- s5_tradeoff · When reading-time schemas win, and what they cost (~100 s): slide 82's second
  half, the notes' paragraphs after it.
  - Heterogeneous data: an online shop's books, shoes and TVs (screen resolution means nothing for
    a shoe, shoe size nothing for a TV). Relationally, a table per product type (the lecturer,
    00:38:08).
  - Schema changes: write new documents in the new format and handle both on read, instead of
    an expensive migration that rewrites a big table (slide 33).
  - The cost: mistakes aren't caught. birthyear, birthYear and birth_year written by three parts
    of one app; the year 1889 stored as the string "1889". A misspelt key isn't an error: Chaplin's
    `person->>'birth_year'` is just NULL (verified; ch7 explains the arrow).
- s6_jsonschema · JSON Schema (~90 s): slide 83, the notes' paragraphs around it.
  - A schema that is itself a JSON document, checked by a validator. Walk slide 83's schema for
    people: type, properties, required (person_id and name), additionalProperties: false, items
    for array elements, pattern `^nm[0-9]+$` for IDs. birthyear may be absent, but if present it
    must be an integer.
  - Used to describe data exchanged between systems (OpenAPI), to generate documentation, code
    and forms; some databases validate on write. The lecturer: know it exists; you don't need its
    details (00:39:43).
- s7_recap · Try these, and recap (~95 s, then the ~8 s end card):
  - Exercise 17 card (the five applications: blog, bank, event log, shop catalogue, app
    settings). Hint: for each, sketch its relationships (tree or tangle?), ask what gets updated
    and how often, and whether the items share one structure.
  - Exercise 18 card (the five properties of people documents). Hint: a JSON Schema looks at one
    document at a time, one value at a time.
  - Recap: the tree (s2), the tangle (s3), the two checkpoints (s4), the shop (s5), the schema
    card (s6). Next: querying these documents with SQL.
Continuity: the tangle is Lecture 5's starting picture (COURSE.md). Solutions to 17 and 18 are in
ch10.

## Chapter 7 · Reaching inside a document
Slug: ch7_json_sql · ~10.5 min · Source: notes pp. 45–47 (§4.4 up to slide 88) · Recording:
00:39:48–00:47:54
Goal: extract values from JSON documents in DuckDB with the arrow operators and JSONPath, compare
them correctly (casts, parentheses), search inside arrays, and test for missing keys.
Scenes:
- s1_hook · Hook (~45 s): title card ("Part 7 · Reaching inside a document"). Last time: when
  documents fit and when tables do. Now the documents sit in one DuckDB column each. SQL thinks in
  flat rows; how does it reach into a tree? Show a movies row whose movie cell opens into The Kid's
  tree.
- s2_arrows · Two arrows (~85 s): slide 84.
  - `movie->'title'` gives `"The Kid"`, quotes included, a value of type JSON;
    `movie->>'title'` gives `The Kid`, a VARCHAR. genres comes back as the JSON array
    `["Comedy","Drama","Family"]`.
  - Why two: keep it JSON to go deeper, take a string to compare or print. They are
    json_extract and json_extract_string. Not standard SQL; PostgreSQL uses the same operators.
- s3_paths · JSONPath: a route through the tree (~100 s): slide 85, on ch4's JSON tree.
  - `$` the whole document, `.actors` a key, `[0]` the first element, `[*]` every element.
    `$.actors[0].name` → Charles Chaplin; `$.genres[1]` → Drama; `$.genres[*]` → the list
    [Comedy, Drama, Family]. Animate each path as a walk from the root.
  - A wildcard returns a list (VARCHAR[] with the double arrow, JSON[] with the single one).
  - Off by one: JSON arrays count from 0, DuckDB lists from 1. `$.genres[0]` and
    `(movie->>'$.genres[*]')[1]` are both Comedy (verified).
  - JSONPath is a small declarative query language of its own (the lecturer, 00:57:02).
- s4_cast · Compare numbers as numbers (~95 s): slide 86.
  - The Star Wars films since 2000 (five rows, 2002–2019), with `(movie->>'year')::INTEGER`.
  - Why the cast: `->>` always gives a string, and strings compare character by character.
    `MAX(movie->>'minutes')` is '99', while the longest movie runs 321 minutes: '9' beats '3'.
    And `'999' > '2000'` is true. DuckDB 1.5.6 refuses the mixed comparison outright: "Binder
    Error: Cannot compare values of type VARCHAR and type INTEGER_LITERAL - an explicit cast is
    required". (All verified.)
  - `CAST(x AS INTEGER)` is standard SQL; `x::INTEGER` is DuckDB's shorthand.
- s5_parens · The arrows bind loosely (~80 s): the notes' paragraph before slide 86.
  - `movie->>'year'::INTEGER` casts the key: "Conversion Error: Could not convert string 'year'
    to INT32". The cast binds tighter than the arrow.
  - `movie->>'title' = 'The Kid' AND movie->>'type' = 'movie'` fails with a baffling conversion
    error (quote it verbatim), because AND binds tighter than the arrows in current DuckDB. DuckDB
    says this changes from version 2.0.
  - The rule: parentheses around every arrow in a condition. The lecturer tripped on exactly this
    live (00:43:06).
- s6_arrays · Searching inside arrays (~95 s): slide 87.
  - `list_contains(movie->>'$.genres[*]', 'War')`: 72 war movies.
  - `list_has_all(..., ['Romance', 'Comedy'])`: 174 romantic comedies, one condition. The
    relational version needed INTERSECT or a self-join (ch1's Venn, Exercise 10).
  - `$.directors[*].name` contains 'Steven Spielberg': 28 movies; the first three Jaws 1975,
    Close Encounters of the Third Kind 1977, Raiders of the Lost Ark 1981. These are ch4's three
    MongoDB questions, now in SQL.
- s7_missing · Missing keys (~85 s): slide 88.
  - `json_exists(person, '$.composed_for')`: 1,086 composers, the same 1,086 the semijoin found
    in ch3. One fact, two models. `NOT json_exists(person, '$.acted_in')`: 7,706 people never
    acted.
  - `(person->>'acted_in') IS NULL` also works: a missing key gives SQL NULL (PINK). The
    difference: json_exists is TRUE for a key present with the JSON value null, and the arrows
    give SQL NULL in both cases. Our documents never contain null, so here it makes no difference.
  - The cost: a typo isn't an error. `person->>'birth_year'` is NULL for everyone (ch6's warning,
    now explained).
- s8_recap · Recap (~65 s, then the ~8 s end card): the two arrows (s2), the walk through the tree
  (s3), '99' vs 321 (s4), the parentheses (s5), the war and Spielberg lists (s6), 1,086 twice
  (s7). Next: turning an array into rows of its own.
Continuity: uses ch4's tree and document card throughout; the Venn from ch1 and the 1,086 from ch3
return as callbacks.

## Chapter 8 · Arrays into rows
Slug: ch8_unnest · ~10.5 min · Source: notes pp. 47–49 (slides 89–93, Exercise 19) · Recording:
00:47:54–00:57:20
Goal: turn arrays into rows with unnest, then group, join and search over documents with ordinary
SQL, and know when a query is telling you the data should have been relational.
Scenes:
- s1_hook · Hook (~45 s): title card ("Part 8 · Arrays into rows"). Last time: reaching inside
  documents. The Kid's ten actors are packed into one cell. Sorting them by name, counting genres
  across all movies, asking how old the actors were: each needs one row per element.
- s2_unnest · One row per element (~110 s): slide 89.
  - `FROM movies, unnest(movie->'$.actors[*]') AS t(a)`: one row per actor; `a->>'name'` and
    `a->'roles'`. The cast of The Kid, ORDER BY name, LIMIT 4: Albert Austin
    ["Car Thief","Man in Shelter"], B.F. Blinn ["His Assistant"], Beulah Bains ["Bride"], Carl
    Miller ["The Man"].
  - It sits in FROM because it runs once per movie, on that movie's own list: like ch3's
    correlated subquery (the outer-loop visual). `AS t(a)` names the table and its one column.
  - Without ORDER BY, DuckDB 1.5.6 returned The Kid's cast in reverse array order (verified):
    rows have no order unless you ask (slide 36).
  - Compare the three-table join of slide 49. The lecturer: this one would have been easier in
    the relational database (00:51:04).
- s3_group · Grouping over documents (~85 s): slide 90.
  - Movies per genre: Drama 1,691, Comedy 878, Action 869, Adventure 719, Crime 621. The same
    Drama and Crime counts as ch1's UNION ALL: one dataset, two shapes, same facts.
  - After unnest, array elements are ordinary rows: WHERE, GROUP BY, joins all work. Many document
    databases offer less: MongoDB's aggregation pipeline makes you describe the steps instead of
    declaring the result.
- s4_join · When the document doesn't have it (~100 s): slide 91.
  - How old were The Kid's actors? Birth years live only in person documents, so join people on
    `person_id = (a->>'person_id')` and subtract: Henry Bergman 53, B.F. Blinn 49, Albert Austin
    39, Edward Biby 35.
  - Denormalised documents answer the questions their designer anticipated; anything else needs
    joins again. The lecturer: at that point, maybe it should have been relational in the first
    place (00:52:32), and decide up front which data you'll want (00:53:43).
- s5_text · Searching text (~90 s): slide 92.
  - Trivia that mentions hackers: `WHERE EXISTS (SELECT 1 FROM unnest(movie->>'$.trivia_entries[*]')
    AS t(e) WHERE e ILIKE '%hacker%')`. Ch3's semijoin, inside one document. ILIKE is LIKE ignoring
    case. Result: Hackers 1995, Mission: Impossible 1996, Notting Hill 1999, Upgrade 2018, Who Am I
    2014.
  - Crude: it matches "hackers" but not "hacking" or "hacked", matches any word containing the
    letters, and doesn't rank. Full-text search engines (Elasticsearch, OpenSearch) split words,
    reduce them to stems, tolerate typos and rank by relevance; they store JSON too. DuckDB has a
    full-text search extension.
- s6_summary · The JSON toolkit on one card (~70 s): slide 93 built row by row in the TEAL
  toolkit card (the twin of ch3's BLUE one): ->, ->>, wildcard lists, the cast, json_exists,
  json_array_length (first seen here, needed for Exercise 19), list_contains, list_has_all,
  unnest. "Put parentheses around -> and ->> in conditions!"
- s7_try · Try these (~70 s): Exercise 19's four questions as cards, with hints. (1) Every
  document to update when Lana Wachowski renamed: `$.*[*]` matches every element of every
  top-level array, and don't forget her own document. (2) The five people who directed the most
  movies: json_array_length. (3) Movies where a director also acted: list_has_any on two lists,
  compared by ID, not by name. (4) The five genres with the highest average rating: unnest, then
  AVG of the rating, cast to a number.
- s8_recap · Recap (~80 s, then the ~8 s end card): the unfolding cast (s2), the genre bars
  (s3), the join back to people (s4), the hacker semijoin (s5), the toolkit card (s6). One closing
  line for the lecture: the same movies, two shapes, each fast at different questions. Next:
  worked solutions in the two bonus parts, then Lecture 5, where the tangle from part six gets a
  model of its own.
Continuity: closes the lecture. Solutions to 19 are in ch10.

## Chapter 9 · Solutions: subqueries and redundancy
Slug: ch9_solutions_queries · ~10.5 min (bonus) · Source: notes pp. 34–35 (Exercises 13–14), pp.
42–43 (Exercises 15–16), drawing on slides 52, 54, 64–66 and p. 19 (slide 34, indexes) ·
Recording: none (the exercises weren't discussed in the lecture)
Goal: worked solutions to Exercises 13–16, with a smallest counterexample database for each
pair in 13 that differs, all run in DuckDB.
Scenes:
- s1_intro · Spoiler warning (~45 s): title card ("Part 9 · Solutions: subqueries and
  redundancy"); the four exercise cards as in ch3 s8 and ch5 s7; pause and try first.
- s2_pairs · Exercise 13, pairs 1 and 2 (~100 s): (1) differ when ess has two rows with the same
  why: the join repeats the ar row, IN doesn't. Counterexample ar = {(1, 10)}, ess = {(10, 99),
  (10, 5)}: IN gives 1 once, the join twice (verified). (2) always the same: for an inner join,
  a condition in ON and in WHERE filter the same pairs.
- s3_left · Exercise 13, pair 3 (~85 s): differ. In ON, `s.z = 99` only decides which ess rows
  match, and every ar row survives, padded with NULL. In WHERE, it runs after the padding, and
  `NULL = 99` is NULL, so unmatched rows are dropped. Smallest example, run both.
- s4_notin · Exercise 13, pair 4 (~100 s): differ in two ways, both NULLs. If ess.why contains a
  NULL, NOT IN returns nothing (ch2) while the LEFT JOIN still finds the unmatched rows. If ar.why
  is NULL, the LEFT JOIN keeps that row (it matches nothing) while NOT IN drops it. Verified:
  ar = {(1,10), (2,NULL), (3,30)}, ess = {(10,99), (10,5)}: LEFT JOIN gives 2 and 3, NOT IN gives
  3; add (NULL, 1) to ess and NOT IN gives nothing. When neither column holds a NULL they agree.
- s5_composers · Exercise 14 (~75 s): `SELECT DISTINCT p.person_id, p.name FROM people p JOIN
  has_position hp ON ... AND hp.position = 'composer'` (or GROUP BY both), 1,086 rows. DISTINCT
  name alone would merge two different composers who share a name. The data has no such pair
  among composers today (1,086 names, 1,086 IDs), but people does have shared names (three Sam
  Phillips, three John Morris), so the query must not rely on luck.
- s6_index · Exercise 15 (~90 s): what an index shares with denormalisation (a redundant copy for
  faster reads, slower writes) and how it differs: the DBMS keeps it consistent automatically and
  within the same write; queries are written the same way and return the same results (slide 34);
  denormalised copies are kept by the application, change how queries are written, and can drift.
- s7_build · Exercise 16 (~120 s): the query with json_object and list over movies, has_genre,
  genres, plays_role and people, run in DuckDB and its output shown for The Kid. Then the
  differences from the JSON database: whatever the writer's run shows (expected: no rating,
  roles, crew or trivia; actors' order; duplicates if a person played two roles; movies with no
  actors or genres need care).
- s8_recap · Recap (~55 s, then the ~8 s end card): one small card per answer. Next: the document
  exercises.
Continuity: the counterexample tables are tiny ar and ess tables in BLUE cards, the same style as
the schema map. The exercise cards match ch3 s8 and ch5 s7.

## Chapter 10 · Solutions: modelling and JSON queries
Slug: ch10_solutions_documents · ~10 min (bonus) · Source: notes pp. 44–45 (Exercises 17–18), p. 49
(Exercise 19), drawing on slides 76–93 · Recording: none
Goal: worked solutions to Exercises 17–19: reasoned modelling choices, what JSON Schema can and
can't enforce, and four verified queries over the JSON database.
Scenes:
- s1_intro · Spoiler warning (~40 s): title card ("Part 10 · Solutions: modelling and JSON
  queries"); the three exercise cards as in ch6 s7 and ch8 s7.
- s2_choose · Exercise 17 (~140 s): each application judged with ch5–ch6's questions (tree or
  tangle, how often updated, one structure or many). Blog posts with tags and comments: a tree,
  documents (comment authors are references). Bank: transfers connect two accounts, a tangle,
  and correctness matters most: relational. Event log: write-once, varied arguments: documents
  (no updates, so no anomalies). Shop catalogue: heterogeneous attributes: documents, or a hybrid.
  App settings: one document per user, read together. The notes give no official answers: say
  the reasoning is what's examined.
- s3_schema · Exercise 18 (~100 s): (1) yes, `required`. (2) no: it compares two values in one
  document (standard JSON Schema has no such keyword; the writer checks this claim against the
  spec). (3) no: uniqueness spans documents, and a validator sees one at a time (the primary key
  does it in our database). (4) and (5) no: they refer to other documents.
- s4_rename · Exercise 19.1 (~90 s): `$.*[*].person_id` over movies with list_contains, plus her
  own person document: 8 movie documents and 1 person document (verified). Ties back to ch5 s3.
- s5_directors · Exercise 19.2 and 19.3 (~110 s): json_array_length(person, '$.directed'),
  ORDER BY it DESC LIMIT 5; list_has_any of directors' and actors' person_id lists. Run both;
  show the results.
- s6_genres · Exercise 19.4 (~80 s): unnest genres, AVG((movie->>'rating')::DOUBLE) or DECIMAL,
  GROUP BY, top five. Run it.
- s7_recap · Recap (~55 s, then the ~8 s end card): one card per exercise. Next: Lecture 5, graph
  databases.
Continuity: exercise cards match ch6 s7 and ch8 s7; query layout as ch7–ch8.

## Decisions
- **Size: 10 chapters, ~80.5 min core plus ~20.5 min of solutions.** The core is above the
  studio's 45–60 min per lecture hour because the project owns all of §3.6 on top of the full
  Oct 27 hour: ch1–ch2 (~19 min) are Lecture 3's share (derived tables, WITH, scalar subqueries,
  NOT IN and its trap), which the recording recaps in ~70 s, and ch3–ch8 (~61 min) cover the
  53 taught minutes of 00:04:34–00:57:20, the ratio of recent lectures (maths L10 63 min, DE L11
  62 min). No material was dropped to get there, and none would need to be.
- **Split.** Subqueries in three parts, one shape of subquery each: table and value (ch1), column
  and the NULL trap (ch2), EXISTS (ch3). Documents follow §4.1–4.4 in order: JSON (ch4),
  normalisation (ch5), comparing models (ch6), and querying, split at unnest (ch7, ch8), since
  slides 84–93 are ~17 live minutes.
- **Order:** the notes' throughout, with two refreshers placed where they're needed: the set
  operations (§3.5, slides 56–57) in ch1, where slide 60 points to them, and three-valued logic
  (§3.5, slides 58–59) in ch2, rebuilt from "unknown = could be either" so the viewer can derive
  every cell rather than memorise it.
- **Exercises:** hints at the end of the part that teaches each one (ch3: 13–14; ch5: 15–16; ch6:
  17–18; ch8: 19), not all in the last core part as the studio usually does. The notes embed them
  after their sections, and Exercise 13's hint five parts later would be cold. Full solutions in
  two bonus parts: about twenty sub-questions would get ~35 s each in one part.
- **Left out:** Exercise 12 (De Morgan and "a or not a" in three-valued logic) sits in §3.5,
  Lecture 3's section, so it's out of the producer's scope. It would fit naturally after ch2 s5's
  truth tables (a ~30 s hint, ~1 min in ch9) if the user wants it. The course logistics at
  00:16:47–00:18:58 (practicals for documents, graphs and Datalog; Traverse; Datalog notes
  coming) get one sentence in ch4 s6. Nothing else in pp. 32–49 is left out.
- **Running example:** the notes' The Kid throughout. The lecturer's live demos used Wild
  Strawberries for the arrows and JSONPath (00:25:28, 00:40:01); the slides use The Kid, and so
  do we, for continuity with ch1 and ch4.
- **No digest:** Gemini was off (quota). The slides come from the handout, the demos from the
  transcript and the real database. One frame checked (00:21:36: the DuckDB 1.5.6 terminal,
  `.tables` shows movies 2,935 and people 23,179 rows), consistent with the notes. No student
  questions were asked ("any questions?" at 00:16:43 and 00:33:11 got no answers).
- **Added from the data (not in the notes, all verified):** Kaiva's ten has_position actors with
  no plays_role rows (ch2); 26 genres relationally vs 23 in the documents, with News only in Food,
  Inc. (ch5, the anomalies made real); `MAX` of minutes as strings '99' vs 321, and DuckDB 1.5.6's
  binder error for VARCHAR vs an integer (ch7); unnest's reverse row order without ORDER BY (ch8);
  1976's fifth movie, King Kong, below average (ch1); Hans Zimmer's 72 composer credits (the
  notes say "dozens", ch3); the Exercise 13 counterexamples (ch9).
- **Colours:** BLUE relational and TEAL documents, so the two models are told apart at a glance
  and Lecture 5 can call back to both. PINK means NULL throughout this lecture, except in ch6 s3's
  tangle, which borrows Lecture 5's graph look (Person PINK, Movie BLUE circles; planned at the
  same time) so that the teaser and Lecture 5's opening show the same picture.
