# Chapter 1 · Queries inside queries

Databases, Lecture 4 (Subqueries and Documents), part 1 of 10. Source: notes pp. 32–33 (§3.6, slides 60–63); refreshers pp. 11–16 (slides 19–25, the schema and The Kid), p. 24 (slide 45, HAVING), p. 30 (slides 56–57, set operations); recording 00:04:34–00:05:47 (the lecturer's recap).

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Every query and reply below was run on DuckDB v1.5.6 against `../source/movies.duckdb` (read-only,
2026-11-01). DuckDB prints ratings as `8.200`; result tables are typeset like the slides (`8.2`,
`7.17`, `1,915`), per PLAN.md's conventions.

---

## Scene 1 · Hook (ch1_s1_hook)

> Title card: "Subqueries and Documents", "Databases · Lecture 4", "Part 1 · Queries inside queries".
> The tower, left half: a small BLUE table card "movies" as the base. Bricks (BLUE rounded rectangles, the operator in MathTex, a short DIM caption beside it) land one at a time, each growing out of the one below, with a tiny table icon passing up between them (relation in, relation out): `γ_{year; count(*)→n_movies}` "group by year, count"; `σ_{n_movies > 140}` "keep years over 140"; `γ_{count(*)→n_years}` "count those years". On {more}, two DIM ghost bricks stack above.
> The form, right half: a SQL query drawn as a form of seven labelled slots in writing order, keywords BLUE: SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT.
> On {fit}: movies drops into FROM, the first brick into GROUP BY (its count(*) into SELECT), the σ brick into HAVING; the filled slots tick GREEN. On {stuck}: the third brick hovers over the form, finds no free slot, shakes, outline RED.
> On {question}: "How do you make SQL stack?" in YELLOW under both. The tower and the form carry into s3, s5 and the recap; keep their look.

[c1.hook.1] {title} This is lecture four of Databases, on subqueries and documents. {pause} We begin inside sequel itself, with queries inside queries.

[c1.hook.2] {bricks} In relational algebra, every operator takes relations and returns a relation. {stack} So operators stack, like bricks. Each brick takes a table, and hands a table up to the next. {movies} Start with the movies table. {group} Group the movies by year, and count each group. {keep} Keep the years with more than a hundred and forty movies. {count} Then count those years. {more} And you could keep going, brick after brick.

[c1.hook.3] {form} A sequel query works differently. It's a form with fixed boxes, each used at most once, in a fixed order. {fit} The first two bricks fit. {stuck} The third one, counting the years, has nowhere to go. {pause} {question} So how do you make sequel stack? {pause}

## Scene 2 · The movies database in one minute (ch1_s2_schema)

> Build the schema map (this scene owns the helper; ch4, ch5, ch6 and Lecture 5 reuse it), laid out as slide 23: top row genres (left), ratings (middle), people (right); middle row has_genre, movies (centre), has_position; plays_role bottom right. All BLUE (the relational world): entity tables movies, people, genres as wide cards with a filled header; ratings, has_genre, has_position, plays_role narrower. Columns as on slide 23 (ratings: movie_id, rating, votes; has_position: movie_id, person_id, position, job); primary-key columns underlined.
> On {entities} the three entity cards brighten; on {links} the four others. On {keys} the underlines pulse; on {arrows} the foreign-key arrows draw, each from a foreign key to the key it references (has_genre → movies and genres; ratings → movies; has_position → movies and people; plays_role → movies and people). Small GOLD counts under movies (2,935) and people (23,179).
> From {kid}, The Kid lights up YELLOW card by card, one card per mark ({movie}, {rating}, {genres}, {chaplin}, {jobs}, {role}; slides 24–25), each card showing its rows: movies `The Kid | 1921 | movie | 68`; ratings `8.2 | 142,991`; has_genre three rows (genre_id 5, 8, 11) with links into genres Comedy, Drama, Family; people `Charles Chaplin | 1889 | 1977`; has_position five rows, positions actor, composer, director, producer, writer (the actor row's job is NULL: write it PINK, unremarked); plays_role `A Tramp`. IDs may show in DIM.
> On {join}: the movies and ratings cards slide together and their movie_id cells meet (a YELLOW link); on {match} The Kid's title lands next to 8.2. Under it, `movies ⋈_movie_id ratings` (MathTex) and the SQL, verbatim (verified): `SELECT title, rating FROM movies JOIN ratings USING (movie_id) WHERE title = 'The Kid';` with the result `title | rating` / `The Kid | 8.2`.
> On {enough} the map shrinks to a corner and fades.

[c1.schema.1] {map} First, a one-minute reminder of the movies database. Almost three thousand movies, and twenty-three thousand people, in seven tables. {entities} Three of them describe things in the world: movies, people, and genres. {links} The other four describe how those things relate: ratings, has genre, has position, and plays role.

[c1.schema.2] {keys} Every table has a primary key, underlined, that picks out exactly one row. {arrows} And each arrow is a foreign key: a column holding the key of a row in another table.

[c1.schema.3] {kid} Let's follow one movie through the tables. The Kid, from nineteen twenty-one. {movie} It's one row in movies, sixty-eight minutes long. {rating} One row in ratings, with eight point two. {genres} Three rows in has genre, pointing at Comedy, Drama, and Family. {chaplin} Charles Chaplin is one row in people. {jobs} He has five rows in has position, because he acted, composed the music, directed, produced, and wrote. {role} And one row in plays role, for the character he played, A Tramp.

[c1.schema.4] {join} To put the pieces back together, you join on keys. {match} Join movies with ratings on the movie ID, and The Kid's title lands right next to its eight point two. {enough} That's all you need from the first three lectures. Everything else, we'll build as we go.

## Scene 3 · SQL's fixed form (ch1_s3_form)

> The form from s1 returns, centre, slots in writing order. On {clauses} the slots light in turn; on {once} each gets a small DIM "×1". On {order}/{run} the slots slide into running order, each with a small DIM step number: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT (slide 45).
> On {example}, slide 45's query as Code, verbatim (verified):
> `SELECT year, COUNT(*) AS n_movies` / `FROM   movies` / `GROUP BY year` / `HAVING COUNT(*) > 140` / `ORDER BY year;`
> On {group} a stream of movie rows falls into year bins with GOLD counts; on {having} the bins at or under 140 dim. On {result} the table `year | n_movies` / `2013 | 153` / `2014 | 146` / `2016 | 147` (counts GOLD). On {eye} the three rows tick 1, 2, 3 in YELLOW.
> On {where}, the same query with HAVING removed and `WHERE  n_movies > 140` placed under FROM (the rest unchanged). On {error}, DuckDB's reply in RED, verbatim (verified), monospace with the caret line aligned under `COUNT(*)`:
> `Binder Error: WHERE clause cannot contain aggregates!` / (blank line) / `LINE 1: SELECT year, COUNT(*) AS n_movies` / `                     ^`. On {caret} a YELLOW link from n_movies in the WHERE line to COUNT(*) in line 1 (DuckDB swapped in the alias's definition).
> On {why} back to the running-order pipeline: single movie rows flow through WHERE (no groups exist yet). On {after} the rows gather into year groups at GROUP BY, and HAVING sees the groups.
> On {same} slide 60's formula in MathTex, `σ … (γ … (σ … (movies)))`: the inner σ labelled WHERE, the outer σ labelled HAVING, both σ the same BLUE. On {two} the words WHERE and HAVING pulse together. On {stuck} s1's third brick ("count those years") hovers over the full form, RED again.

[c1.form.1] {form} Let's look closer at that form. {clauses} Select, from, where, group by, having, order by, and limit. {once} Each clause appears at most once, always in that order. {order} But that's the order you write them in, not the order they run. {run} The database starts with from, then where, then group by, then having, and only then select, order by, and limit.

[c1.form.2] {example} Here's an example: which years had more than a hundred and forty movies? {group} Group the movies by year, and count each group. {having} Then keep the groups whose count is over a hundred and forty. {result} Three years: twenty thirteen, twenty fourteen, and twenty sixteen. {eye} You can count them by eye. Three. But this query has no way to count them for you.

[c1.form.3] {where} Now, why not write where N-movies is greater than a hundred and forty? {error} Duck D B refuses, with a binder error: the where clause cannot contain aggregates. {caret} It points at count star, because that's what N-movies stands for. {pause} {why} Look at the running order again. The where clause runs before group by. At that moment there are only single movies, and no groups to count. {after} The having clause runs after group by, so it sees the groups.

[c1.form.4] {same} So where and having do the same job. Both are the selection from relational algebra. {two} One concept, two keywords: one for before grouping, and one for after. {stuck} And once you've used having, the form has no box left. There's no third selection, and no second group by. That's our third brick from the start, still with nowhere to go.

## Scene 4 · Combining whole results (ch1_s4_setops)

> The Venn of Crime and Drama (this scene owns the helper; it returns in ch7 s6 and ch8 s3): two overlapping BLUE circles, names in YELLOW, "Crime" and "Drama" with DIM "genre 6" / "genre 8". Region counts GOLD (verified): Crime only 224, both 397, Drama only 1,294; totals 621 and 1,691 beside the names.
> Beside it, slide 56's query as Code, verbatim (verified): `SELECT movie_id FROM has_genre WHERE genre_id = 6` / `INTERSECT` / `SELECT movie_id FROM has_genre WHERE genre_id = 8;` The middle keyword swaps on each beat, and its region fills: {intersect} INTERSECT, the lens, 397 rows; {union} UNION, both circles, 1,915 rows; {except} EXCEPT, the Crime-only crescent, 224 rows. (DuckDB's footers read `397 rows`, `1915 rows`, `224 rows`; typeset 1,915.)
> On {columns} the two SELECT lines' `movie_id` columns light up GREEN and a link joins them: same columns on both sides.
> On {sets} a small DIM tag "set" under the result count. On {unionall} the tag becomes "multiset" and the keyword becomes `UNION ALL`: the lens is drawn twice (a GOLD copy lifts off and stacks beside), and the sum `621 + 1,691 = 2,312` appears (DuckDB: `2312 rows`, verified). On {twice} both copies of 397 pulse.
> On {limit}: under the Venn, slide 56's algebra as two small brick towers in s1's style, `π_movie_id` on `σ_genre_id=6` on has_genre, and the same with 8, bridged at the top by an `∩` brick. Then two SELECT forms (s1's form, small) side by side, glued by a UNION bar; an arrow tries to run from one form's result into the other form's FROM slot and is crossed out in RED.

[c1.setops.1] {other} Sequel does have one way to combine whole queries: the set operations. {crime} Take the movies in genre six, Crime. There are six hundred and twenty-one. {drama} And the movies in genre eight, Drama. There are one thousand, six hundred and ninety-one. {intersect} Intersect keeps the movies in both, three hundred and ninety-seven. {union} Union keeps the movies in either genre, one thousand nine hundred and fifteen. {except} And Crime except Drama leaves the Crime movies that are not Drama, two hundred and twenty-four.

[c1.setops.2] {columns} Both sides must return the same columns, here just the movie ID. {sets} And these plain forms remove duplicates, so each result is a set, like a relation in relational algebra. {unionall} But sequel tables are multisets, where the same row can appear more than once. So each operation also has an all version, which keeps the duplicates. Union all returns two thousand, three hundred and twelve rows, exactly six hundred and twenty-one plus one thousand, six hundred and ninety-one. {twice} The three hundred and ninety-seven movies in both genres are counted twice.

[c1.setops.3] {limit} In relational algebra, the intersection is one more brick, gluing two small towers together. {side} In sequel, these operations put two finished queries side by side. {notinput} But none of them lets one query's result become another query's input. {pause}

## Scene 5 · A query where a table goes (ch1_s5_derived)

> Open on a SELECT form from s1 whose output is drawn as a small BLUE table (a table comes out). On {anywhere} that table glides into the FROM slot of a second, empty form.
> On {from}, slide 61's query as Code, verbatim (verified): `-- Which years have more than 140 movie releases?` / `SELECT year, n_movies` / `FROM (SELECT year, COUNT(*) AS n_movies` / `       FROM movies GROUP BY year) AS per_year` / `WHERE n_movies > 140;`. The parentheses glow BLUE; on {name} `AS per_year` YELLOW.
> On {inner} the inner query highlights and a ghost per_year table (year, n_movies, GOLD counts, many rows) appears beside it; on {outer} the outer query highlights and filters the ghost to three rows. On {same} the result `2013 | 153`, `2014 | 146`, `2016 | 147` (slides 61 and 62 have no ORDER BY: show the slides' order, which DuckDB 1.5.6 printed in four runs out of four, though it isn't guaranteed; s3's HAVING query has ORDER BY year).
> On {plan}: a small three-box plan diagram (a drawing, not DuckDB's text), bottom to top: "scan movies", "group by year, count", "filter > 140", drawn next to the HAVING query from s3 with the identical diagram. (Checked with EXPLAIN in DuckDB 1.5.6: both physical plans are SEQ_SCAN → PERFECT_HASH_GROUP_BY → FILTER, the filter reading `(count_star() > 140)` and `(n_movies > 140)`.) On {algebra} the diagram morphs into s1's bricks, `σ` on `γ` on movies.
> On {fresh} s1's form appears small beside the code for the outer query, every slot empty. On {swap} the outer SELECT line swaps (TransformMatchingTex) for `SELECT COUNT(*) AS n_years`, the rest unchanged (verified), and s1's stuck third brick drops into the form's SELECT slot and turns GREEN. On {answer} the result `n_years` / `3`, the 3 in GOLD.
> On {rule} `AS per_year` pulses; on {duck} it fades out and the query still returns the same three rows (verified without the name).
> On {inside} a YELLOW eye-path: it starts at the top, jumps into the parentheses, reads the inner query, then jumps back out to the outer SELECT. On {deeper} a DIM sketch of parentheses nested three deep.

[c1.derived.1] {obs} Here's the observation that unlocks everything. {returns} A sequel query takes tables in, and gives a table back. {anywhere} So a query can stand wherever a table can. {pause} {from} Put it in parentheses, in the from clause of another query, and give it a name. {name} This one is called per year. A query used like this is called a derived table.

[c1.derived.2] {inner} The inner query counts the movies in each year. {outer} The outer query treats that result like any stored table, and keeps the rows where N-movies is over a hundred and forty. {same} The same three years, with the same counts. {plan} And if you ask Duck D B for its plan, it's identical to the having version: scan the movies, group them by year, then filter. {algebra} Underneath, both are the same relational algebra.

[c1.derived.3] {fresh} And here's the payoff. The outer query is a fresh form, with every box empty again. {swap} Swap its select for count star, and the third brick finally has a home. {answer} Three years. {pause} {rule} One rule to know. The sequel standard requires a name for every derived table, even when you never use it. {duck} Duck D B is more relaxed, and runs the query without one.

[c1.derived.4] {inside} There's a cost, though. You have to read this query from the inside out. {jump} Your eye jumps into the parentheses first, then back out to the start. {deeper} Nest a few more, and it gets hard to follow.

## Scene 6 · Name it first: WITH (ch1_s6_with)

> On {with}, slide 62's query as Code, verbatim (verified): `-- Define per_year as a name you can refer to later` / `WITH per_year AS (` / `    SELECT year, COUNT(*) AS n_movies` / `    FROM movies GROUP BY year` / `)` / `SELECT year, n_movies FROM per_year -- Now use it` / `WHERE n_movies > 140;`. Grow it out of s5's derived table: the parenthesised inner query lifts out of the FROM slot and moves to the top, and `per_year` (YELLOW) stays behind in its place.
> On {define} the WITH block highlights; on {use} the main query, with a YELLOW link from `FROM per_year` back up to its definition. On {read} a YELLOW eye-path runs straight down, top to bottom (contrast s5's jumping path).
> On {variable}/{ocaml}: a DIM schematic beside it, `let per_year = ( … ) in …` (OCaml-style, a sketch, not run). On {reuse} two YELLOW links run from the sketch's `in …` back to its one `per_year`.
> On {several}/{tower}: s1's tower (movies, the γ brick, the σ brick, the count brick) on the left, and on the right the chained WITH as Code, verbatim (verified, returns `n_years` / `3`): `WITH per_year AS (` / `    SELECT year, COUNT(*) AS n_movies` / `    FROM movies GROUP BY year` / `),` / `busy AS (` / `    SELECT year FROM per_year WHERE n_movies > 140` / `)` / `SELECT COUNT(*) AS n_years FROM busy;`. Names YELLOW. On {pergroup} the per_year block and the γ brick light together; on {busy} the busy block and the σ brick; on {final} the last line and the count brick, with the GOLD 3. The code reads down while the tower builds up.
> On {three}: the three versions in one layout, left to right, each with its own result table under it: s3's HAVING query, s5's derived table, the WITH query; all three tables read `2013 | 153`, `2014 | 146`, `2016 | 147` (verified). On {results} the three tables pulse GREEN together, and s5's plan diagram sits once beneath all three.

[c1.with.1] {with} A common table expression reads better. It begins with the keyword with. {define} First, define per year as the inner query. {use} Then write the main query, and use per year exactly like a table. {read} Now it reads from top to bottom, in the order it's built.

[c1.with.2] {variable} If that feels like a variable, it is one. {ocaml} In OCaml, you'd write let per year equal this query, in the main query. {reuse} And like a variable, the name can be used more than once. {several} You can also define several names, each one building on the names before it. {tower} So here's the tower from the start, one name per brick. {pergroup} First, per year groups and counts. {busy} The name busy keeps the years over a hundred and forty. {final} And the main query counts them.

[c1.with.3] {three} So now you have three ways to ask the same question. {having} The having clause, {derived} a derived table, {cte} and a common table expression. {results} All three give the same three rows, and Duck D B runs them the same way. {pick} So pick the one that reads best.

## Scene 7 · A query where a value goes (ch1_s7_scalar)

> On {question} the question in YELLOW: "Which 1976 movies are rated above the overall average?" On {obvious}, the attempt as Code, verbatim: `SELECT title, rating` / `FROM   movies JOIN ratings USING (movie_id)` / `WHERE year = 1976` / `  AND rating > AVG(rating);`. On {error}, DuckDB's reply in RED, verbatim (verified), caret aligned under `AVG`: `Binder Error: WHERE clause cannot contain aggregates!` / (blank line) / `LINE 4:   AND rating > AVG(rating);` / `                       ^`.
> On {why}: one movie row passes through a WHERE gate on its own, while AVG reaches for the whole ratings column, which is out of the gate's view.
> On {sub}, `AVG(rating)` is replaced by `(SELECT AVG(rating) FROM ratings)` (slide 63, verbatim and verified as a whole: `SELECT title, rating` / `FROM   movies JOIN ratings USING (movie_id)` / `WHERE year = 1976` / `  AND rating > (SELECT AVG(rating) FROM ratings);`). On {shape}, beside it, the subquery's result as a 1×1 table, header `avg(rating)` DIM, one cell (DuckDB prints `7.174923339011925`; show `7.17` as slide 44 does). On {value} that cell slides into the slot after `>`.
> On {once}: the subquery's text glows, and a quick scan of it finds no name from the outer query: it touches only the ratings table. On {runonce} a "1×" badge; on {collapse} the parenthesised subquery shrinks in place into a GOLD chip `7.17`. On {all} a DIM "2,935 ratings" under the chip. On {outward} a DIM arrow tries to reach from inside the parentheses out to the outer query, with a small DIM tag "part 3".
> On {five}: a horizontal number line of ratings (about 5.5 to 8.5) with a GOLD threshold at 7.17; five dots for the 1976 movies, labelled: King Kong 6.0, Carrie 7.4, Network 8.1, Rocky 8.1, Taxi Driver 8.2. On {clear} the four above the line turn GREEN; on {kong} King Kong turns RED and fades. Then the result table (verified; slide 63 has no ORDER BY, so show the slide's order, alphabetical): `title | rating` / `Carrie | 7.4` / `Network | 8.1` / `Rocky | 8.1` / `Taxi Driver | 8.2`.

[c1.scalar.1] {question} A new question. Which nineteen seventy-six movies are rated above the overall average? {obvious} The obvious attempt says where rating is greater than the average of rating. {error} And it fails with the same binder error. {pause} {why} You can see why. The where clause judges one row at a time, on its own. An average needs all the rows at once.

[c1.scalar.2] {sub} So compute the average separately, with its own query, in parentheses. {shape} Look at the shape of its result. One row, and one column. {value} That's a single value, so it can go anywhere a value can, even right after the greater-than sign. {name} This is called a scalar subquery.

[c1.scalar.3] {once} Notice that it mentions nothing from the outer query. {runonce} So the database can run it just once, before the outer query starts, {collapse} and the whole thing collapses into a number, seven point one seven. {all} That's the average over all two thousand, nine hundred and thirty-five rated movies, not just the ones from nineteen seventy-six. {outward} A subquery that does mention the outer query is a different creature. We'll meet it in part three.

[c1.scalar.4] {five} Nineteen seventy-six has five movies in the database. {clear} Four of them clear the bar. Carrie, at seven point four. Network and Rocky, at eight point one each. And Taxi Driver, at eight point two. {kong} King Kong, at six point zero, stays out. {pause}

## Scene 8 · Recap (ch1_s8_recap)

> One small callback per sentence, each in its original look, with the sentence's short line under it in DIM, arranged in a 2×2 grid that fills as the recap goes:
> {r1}: s1's tower beside s1's form, the third brick RED over the form; then s3's running order with WHERE before GROUP BY and HAVING after it. Line: "algebra stacks; SQL is a form".
> {r2}: s4's Venn with the lens lit and 397 GOLD, then the lens doubled for UNION ALL. Line: "set operations: side by side".
> {r3}: s5's query shrunk, the parenthesised derived table glowing in FROM, then s6's `WITH per_year AS (…)` with its YELLOW name tag. Line: "a query where a table goes".
> {r4}: s7's subquery collapsing into the GOLD chip `7.17`. Line: "a query where a value goes".
> On {shape}: three shape icons in a row, a grid (table → FROM), a single cell (value → after `>`), and a DIM single column with a "?" (next time). On {next} the column icon brightens, with `IN` in BLUE beside it.
> After the last word, hold ~8 s of end card (the music carries it).

[c1.recap.1] {recap} Let's recap. {r1} Relational algebra stacks freely, but in sequel, every query is a form with fixed boxes, run in a fixed order. That's why selection needs two names, the where clause before grouping, and the having clause after. {r2} Set operations put whole results side by side, and union all keeps the duplicates.

[c1.recap.2] {r3} A query returns a table, so it can go where a table goes, in the from clause as a derived table, or named up front in a with clause, read top to bottom. {r4} And when it returns one row and one column, it's a value. It runs once, collapses to seven point one seven, and goes where a value goes.

[c1.recap.3] {shape} So the shape of the result decides where a query can go. {next} Next time, a query that returns a whole column of values, the in operator, and a trap hiding in its negation. {pause}
