# Chapter 2 · NOT IN and the NULL trap

Databases · Lecture 4 (Subqueries and Documents), part 2 of 10. Source: Kleppmann, Databases notes 2026/27, pp. 33–34 (§3.6, slide 64 and the death-year example); refreshers p. 21 (slide 39, IN), pp. 27–28 (slides 51–52, LEFT JOIN; Exercise 9), p. 30 (Exercise 11), pp. 30–32 (slides 58–59, NULL and three-valued logic); recording 00:05:47–00:06:39.

Format: `[id]` starts a narration line, spoken exactly as written (numbers and identifiers
spelled the way they're *said*). `{mark}` is a cue point; `{pause}` / `{pause=1.5}` is a
deliberate hold. `>` lines are the visual brief.

Verification: every query, result, count and error below was run on DuckDB v1.5.6 (Variegata),
`duckdb -readonly ../source/movies.duckdb`, on 2026-11-01. On-screen SQL follows the slides
(keywords upper case, the slides' aliases); `Code()` uses the project's `sql` lexer. Result tables
are typeset like the slides (DIM header row, plain values), not as DuckDB's boxes. Inside `Code()`
the lexer colours NULL BLUE: recolour every NULL PINK with `find()`. PINK means NULL and only NULL.

---

## Scene 1 · Hook (ch2_s1_hook)

> Title card: "Subqueries and Documents", "Databases · Lecture 4", "Part 2 · NOT IN and the NULL trap".
> On {table} and {value}: two small BLUE callbacks from part 1, side by side. Ch1 s5's derived table (a subquery box sliding into the FROM slot of an outer query, label "a table") and ch1 s7's `(SELECT AVG(rating) FROM ratings)` collapsing to a GOLD `7.17` (label "a value"). Both shrink to the top-left corner and stay there; s3 adds a third shape beside them.
> On {question}: the question as a YELLOW caption across the top, "Which movies came out in a year in which none of the people in the database died?". On {four}: four empty card slots in a row under it, each holding a GOLD "?", with a GOLD "4" at the row's end. The titles stay hidden until s6 fills the slots.
> On {query}: the natural query, centre, `Code(src, lang="sql")`, verbatim:
> `SELECT title FROM movies`
> `WHERE year NOT IN (SELECT deathyear FROM people);`
> On {zero}: its result below, typeset like the slides: a DIM header `title`, no rows at all, and "0 rows" in RED (checked: DuckDB 1.5.6 prints an empty `title` / `varchar` table and `0 rows`).
> On {silent}: a DIM line "no error · no warning" beside the result; the four "?" slots stay empty next to the RED "0 rows". On {worse}: the query gets a thin RED outline. On {plan}: a small PINK `NULL` chip fades in beside `deathyear` and stays, a hint of the culprit.
> Keep the query and its empty result on screen at the end: s4 opens on exactly this shot.

[c2.hook.1] {title} Last time, we put queries inside other queries. {table} A subquery could stand where a table goes, {value} or, when it returned a single number, where a value goes. {pause}

[c2.hook.2] {question} Here's a question for the movies database. Which movies came out in a year in which none of the people in the database died? {four} The right answer is four movies, all from the nineteen twenties and thirties. {pause}

[c2.hook.3] {query} And here's the query you would naturally write. Year not in the death years of people. {zero} Run it, and you get zero rows. {silent} No error, and no warning. Just an empty answer that looks perfectly believable. {pause} {worse} A query that fails loudly is annoying. A query that's quietly wrong is much worse. {plan} By the end of this part, you'll see exactly why it happens, from one small idea about what null means.

## Scene 2 · Asking about absence (ch2_s2_absent)

> Caption at the top, YELLOW: "Which movies have no actors?". On {two}: two small movie cards, "Flow · 2024" and "Kaiva · 2023" (checked: both have no rows in plays_role). They park top-right and stay for s3. On {hard}: a few BLUE movies rows pass under a WHERE filter that lights the rows it finds; a dashed, empty row slot (the role Flow never had) sits among them and the filter passes straight over it. On {earlier}: two DIM labels, "LEFT JOIN" and "EXCEPT", the two ways this scene shows.
> On {leftjoin}: the first query, left half, `Code(src, lang="sql")`, verbatim:
> `SELECT m.movie_id, m.title` / `FROM movies AS m` / `LEFT JOIN plays_role AS r ON m.movie_id = r.movie_id` / `WHERE r.movie_id IS NULL;`
> On {pad}: the join drawn as slide 52's loop, right half: three movie rows on the left (The Kid, Flow, Kaiva), joined rows coming out on the right with columns `title`, `r.movie_id`, `r.role`. The Kid fans out into its twelve rows (show three, "A Tramp", "The Child", "The Woman", then a DIM "… 12 rows" with a GOLD 12; checked). Flow and Kaiva each get exactly one row, its `r.movie_id` and `r.role` cells PINK `NULL` (checked: DuckDB returns NULL in both).
> On {isnull}: the WHERE line lights; The Kid's twelve rows dim and fall away, the two PINK-padded rows turn GREEN and become the result `movie_id | title`: Flow, Kaiva (checked; no ORDER BY, so every version of this query in s2–s3 shows the slide's order, Flow first, whatever order a run prints). On {test}: `IS NULL` gets a YELLOW box, and a small RED `= NULL` with a ✗ and "0 rows" appears under it (checked: `WHERE r.movie_id = NULL` returns 0 rows; a teaser, s5 explains it).
> On {except}: the first query dims to the left edge; the second appears, verbatim:
> `SELECT movie_id, title FROM movies` / `EXCEPT` / `SELECT movie_id, title` / `FROM movies JOIN plays_role USING (movie_id);`
> On {all} and {minus}: a set picture. A big BLUE circle "every movie" with GOLD 2,935, and inside it a slightly smaller circle "movies with a role" with GOLD 2,933 (checked: 2,933 distinct movie IDs in plays_role). On {left}: the thin sliver between them glows GREEN and holds Flow and Kaiva, GOLD "2".
> On {ids}: `movie_id` in both SELECT lines gets a YELLOW underline. On {repeat}: three pairs of same-titled cards drop in, BLUE with GOLD years: "Total Recall 1990 / 2012", "The Mummy 1999 / 2017", "The Italian Job 1969 / 2003" (checked: 31 titles appear twice in movies). On {cancel}: a hypothetical, labelled "what if": Total Recall 1990 loses its actors and slides into the sliver, then Total Recall 2012's title, from the "with a role" circle, strikes it out in RED. Caption: "compare keys, not titles".

[c2.absent.1] {absent} Let's start with a friendlier question of the same kind. Which movies have no actors? {two} The answer is two movies. Flow, an animated film with no dialogue, and Kaiva. {hard} Questions about absence are a little awkward, because a query finds rows that are there. {earlier} You've already seen two ways around that.

[c2.absent.2] {leftjoin} The first is a left join, from movies to plays role. {pad} Every movie survives the join. A movie with no match gets a single row, padded with null. {isnull} So keep only the rows where the plays role movie ID is null, and you're left with Flow and Kaiva. {test} Notice the test there, is null. Equals null would find nothing at all, and we'll see why in a moment.

[c2.absent.3] {except} The second way uses the keyword except. {all} Take every movie, {minus} and subtract every movie that appears in plays role. {left} Two movies are left over. {ids} The subtraction compares each movie's ID, and not just its title, for a good reason. {repeat} Titles repeat. There are two movies called Total Recall, and two called The Mummy. {cancel} If one of them had no actors, the other one's title would cancel it out, and a movie would quietly vanish.

## Scene 3 · A subquery that returns a column (ch2_s3_notin)

> On {list}: the keyword `IN`, BLUE, centre. On {example}: slide 39's operator as a compact query, `Code(src, lang="sql")`, verbatim: `SELECT title, year FROM movies` / `WHERE year IN (1927, 1931);`, with its result `title | year`: Metropolis 1927, City Lights 1931, M 1931 (checked; GOLD years). On {or}: the condition `year IN (1927, 1931)` transforms (TransformFromCopy) into `year = 1927 OR year = 1931`, with `OR` BLUE. That OR line shrinks into a corner and stays: s6 brings it back as the OR chain.
> On {shapes}: the hook's two corner icons return to the centre: a small table grid ("a table", FROM) and a single GOLD cell 7.17 ("a value"). On {column}: a third icon grows out of the table grid: one tall, thin column of many cells, labelled "a column".
> On {compare}: `rating > ` followed by the tall column, with a RED ✗ and "which value?". On {set}: the column slides into the parentheses of `year IN ( … )`, taking the place of `1927, 1931`, GREEN ✓, label "is it a member?".
> On {query}: slide 64's query, centre, verbatim:
> `SELECT movie_id, title FROM movies`
> `WHERE movie_id NOT IN (SELECT movie_id FROM plays_role);`
> On {reads}: the words `NOT IN` get a YELLOW underline. On {inner}: the subquery lifts out and becomes the tall column, now labelled GOLD "30,303 rows", DIM "2,933 different movies" (checked: 30,303 rows, 2,933 distinct). On {answer}: the result, `movie_id | title`: Flow, Kaiva, and s2's two parked cards pulse (checked; DuckDB 1.5.6 returns the two rows in either order run to run: show the slide's order, Flow then Kaiva).
> On {kaiva}: two small BLUE table cards from the schema map (ch1 s2). has_position with Kaiva's ten `actor` rows, a GOLD 10 (checked: ten rows with position = 'actor'); plays_role with no Kaiva rows, a GOLD 0 (checked). On {roles}: an arrow from the subquery's `plays_role` to the plays_role card only; the has_position card dims.
> On {exact}: caption "it answered exactly what it was asked". End on the query and its two-row result.

[c2.notin.1] {list} There's a third way, and it starts from an operator you already know. {example} The condition, year in the list of nineteen twenty-seven and nineteen thirty-one, finds three movies, including Metropolis and City Lights. {or} It's shorthand for, year equals nineteen twenty-seven, or year equals nineteen thirty-one. {pause}

[c2.notin.2] {shapes} Now, the subqueries in part one came in two shapes, a whole table, and a single value. {column} Here's a third shape. A query that returns one column, with many rows. {compare} A greater-than sign needs a single value on each side. Which of these values would it compare with? {pause} {set} But you can put it where the list goes, after the keyword in, which only asks whether a value is a member.

[c2.notin.3] {query} So here's the no-actors question, written that way. {reads} Movie ID not in the movie IDs of plays role. {inner} The subquery returns thirty thousand, three hundred and three IDs, one per role, with lots of repeats. {answer} And the answer is Flow and Kaiva, once again. {english} It reads almost like the question in English.

[c2.notin.4] {kaiva} One thing about Kaiva, though. In the has position table, it lists ten actors. {roles} But none of them has a character in plays role, and plays role is the only table this query looks at. {exact} So the query answered exactly the question it was asked. {pause}

## Scene 4 · The trap, in full (ch2_s4_trap)

> Opens on the hook's last shot: `SELECT title FROM movies` / `WHERE year NOT IN (SELECT deathyear FROM people);` with its empty result and RED "0 rows". On {same}: s3's no-actors query slides in above it, small and DIM, so the two `NOT IN (SELECT … )` shapes line up. On {zero}: the RED "0 rows" pulses.
> On {kid}: The Kid's movies row, BLUE card style, `The Kid | 1921`, lights YELLOW (GOLD 1921). The hook's four "?" slots return along the bottom.
> On {scan}: the `deathyear` column of people as a tall strip on the right, rows named: Charles Chaplin 1977, Jackie Coogan 1984, Edna Purviance 1958, Hans Zimmer NULL, Tom Hanks NULL, … (checked; years GOLD, NULL PINK). A YELLOW 1921 slides down the strip, checking each year. On {none}: no year lights; a GOLD "died in 1921: 0" (checked: `WHERE deathyear = 1921` counts 0).
> On {should}: The Kid's card drops into the first "?" slot, outlined GREEN with "should be here" (title still DIM: it isn't confirmed until s6).
> On {column}: the strip compresses into one bar of 23,179 people (GOLD). On {known}: the bar splits, a GOLD block "2,685 known death years"; on {nulls}: a much longer PINK block "20,494 NULL", with "88%" (checked: 20,494 of 23,179, 88.4%). On {why}: DIM labels under the PINK block: "alive", "died, year unknown?".
> On {ask}: `NOT IN` in the query gets a YELLOW box, and a line runs from it to the PINK block, with a "?" between them. Hold.

[c2.trap.1] {back} Now back to the death-year question. {same} It has the same shape as the no-actors query. {zero} And it returns zero rows. {pause}

[c2.trap.2] {kid} So let's check one movie by hand. The Kid came out in nineteen twenty-one. {scan} Go through the death years in the people table, looking for nineteen twenty-one. {none} Not one of them matches. Nobody in the database died that year. {should} So nineteen twenty-one is not in the list, and The Kid belongs in the answer. {pause}

[c2.trap.3] {column} But look more closely at that column. {known} Two thousand, six hundred and eighty-five people have a death year. {nulls} The other twenty thousand, four hundred and ninety-four have null. That's eighty-eight percent. {why} Most of them are still alive. Some may have died in a year that nobody recorded. {pause} {ask} So what happens to not in, when the list it searches is full of nulls? {pause=1.5}

## Scene 5 · Three-valued logic from one idea (ch2_s5_logic)

> On {unknown}: a single PINK cell `NULL` from s4's strip, centre, next to two DIM labels from slide 58: "value unknown" and "not applicable (death year of someone alive)". On {treat}: both labels merge into one PINK "unknown".
> On {compare}: the comparison `1921 <> NULL`, GOLD 1921, PINK NULL. On {cant}: the NULL becomes a PINK box with a "?" that flickers through candidate years (1921, 1958, 1977, …); the comparison would come out GREEN for some and RED for one. On {result}: the result settles to PINK `NULL` (checked: `SELECT 1921 <> NULL;` returns NULL; DuckDB prints the header as `(1921 != NULL)`, so show the slides' `<>`).
> On {isnull}: under it, `NULL = NULL` gives PINK `NULL` (checked), and s2's YELLOW `IS NULL` box returns beside it. Two tiny counts: `WHERE deathyear = NULL` gives 0 rows (RED), `WHERE deathyear IS NULL` gives 20,494 (GOLD) (both checked).
> On {three}: three chips, TRUE GREEN, FALSE RED, NULL PINK. On {rule}: the rule as a card, centre-top, and it stays for the whole scene: "NULL = could be TRUE, could be FALSE", "try both", "same answer → that answer", "different → NULL".
> On {how}: the truth tables appear, slide 59's, drawn as three small grids (the running visual): AND and OR as 3×3 grids with TRUE / FALSE / NULL along both edges, NOT as 1×3. The TRUE/FALSE cells are filled already (ordinary logic); every cell with a NULL input holds a PINK-outlined "?". Each NULL cell is then computed on screen under the rule card: on {fa} the cell `FALSE AND NULL` splits into two ghosts, `FALSE AND TRUE` and `FALSE AND FALSE`, both RED, which merge on {agree} into a RED FALSE. On {ta}: `TRUE AND NULL` splits into GREEN and RED ghosts, which merge on {disagree} into PINK NULL. On {or}: the OR grid's TRUE OR NULL fills GREEN and FALSE OR NULL PINK; on {not}: NOT NULL fills PINK. On {grids}: the remaining "?" cells fill quickly. Every cell must match DuckDB 1.5.6's output for all nine combinations of a and b (checked): AND is TRUE only for TRUE/TRUE, FALSE whenever either side is FALSE, NULL otherwise; OR is FALSE only for FALSE/FALSE, TRUE whenever either side is TRUE, NULL otherwise; NOT swaps TRUE and FALSE and keeps NULL.
> On {where}: the grids shrink left; a WHERE gate appears (two posts and a bar). Three row tokens arrive: TRUE passes GREEN; on {drop}, FALSE bounces off RED, and NULL bounces off too, PINK.
> On {cracks}: two queries, verbatim, `Code(src, lang="sql")`: `SELECT COUNT(*) FROM people WHERE deathyear < 2000;` and `SELECT COUNT(*) FROM people WHERE NOT (deathyear < 2000);`. A bar of all 23,179 people underneath. On {before}: a GOLD segment 959 fills from the left (checked). On {opposite}: a second segment 1,726 fills next to it (checked). On {sum}: a brace over both, GOLD 2,685, equal to s4's "known" block. On {fall}: the rest of the bar, 20,494, stays PINK and empty, with both WHERE gates bouncing it.

[c2.logic.1] {what} To answer that, we need to be precise about null. {unknown} Null is not a value. It marks a value that's missing. Maybe it's unknown, or maybe there's nothing to record, like the death year of someone alive. {treat} Either way, sequel treats it as unknown.

[c2.logic.2] {compare} So, is nineteen twenty-one not equal to null? {pause} {cant} There's no way to tell. The missing year might be nineteen twenty-one, or anything else. {result} So the answer is neither true nor false. It's null, unknown. {isnull} Even null equals null is null. That's why the left join needed its own test, is null.

[c2.logic.3] {three} So a condition in sequel has three possible values. True, false, and null. {how} How do the logic operators, and, or, and not, handle the third one? {rule} There's no table to memorise. One rule builds all of it. Treat null as, could be true, could be false, and try both. If the two answers agree, that's the answer. If they disagree, the answer is null.

[c2.logic.4] {fa} Take false and null. If the null were true, you'd have false and true, which is false. If it were false, you'd get false again. {agree} They agree, so false and null is false. {ta} Now take true and null. One way you get true, the other way false. {disagree} They disagree, so the answer is null. {or} Or is the mirror image. True or null is true either way, but false or null is null. {not} And not, applied to null, gives true or false, so it's null too.

[c2.logic.5] {grids} Fill in every cell that way, and you get the full tables for and, or, and not. {where} Then one last rule, and it's the one that matters here. In any query, a where clause keeps a row only when its condition is true. {drop} False drops the row, and so does null. {pause}

[c2.logic.6] {cracks} Here's what that does in practice. {before} Count the people who died before two thousand. You get nine hundred and fifty-nine. {opposite} Now count the opposite, not died before two thousand. You get one thousand, seven hundred and twenty-six. {sum} Together, that's two thousand, six hundred and eighty-five, exactly the people with a known death year. {fall} The twenty thousand nulls fail both conditions, a question and its opposite. {pause}

## Scene 6 · Why NOT IN can never be true (ch2_s6_derive)

> On {differs}: slide 64's expansion, `MathTex`/code style, centre: `c NOT IN (v1, v2, …, vn)` transforms (TransformFromCopy) into `(c <> v1) AND (c <> v2) AND … AND (c <> vn)`, with `AND` BLUE. On {chain}: the `<>` links light one after another, left to right, and the `…` stretches. On {and}: s3's corner line `year = 1927 OR year = 1931` comes back beside it, small: IN is an OR chain, NOT IN an AND chain.
> On {kid}: the AND chain (the running visual), drawn as links in a horizontal chain for The Kid, each link a small pill `1921 <> v`. On {green}: the first links, `1921 <> 1977`, `1921 <> 1984`, `1921 <> 1958`, …, all GREEN TRUE, compressed into a GOLD "2,685 links: TRUE" (checked: `WHERE deathyear <> 1921` counts 2,685). On {pink}: the chain continues with PINK links `1921 <> NULL`, compressed into "20,494 links: NULL".
> On {need}: a caption "AND chain: TRUE only if every link is TRUE". On {one}: s5's AND grid flies in small and its `TRUE AND NULL` cell lights PINK; a single PINK link pulses and the whole chain turns PINK. On {dropped}: The Kid's YELLOW card from s4 hits s5's WHERE gate and bounces off PINK; its outline in the first slot turns back to an empty "?".
> On {rush}: a second, shorter chain for The Gold Rush, `1925 <> v`. One link, `1925 <> 1925`, turns RED FALSE (checked: two people in people died in 1925, Jane Connelly and Jean C. Havez; names may appear small and DIM). On {false}: the chain turns RED and The Gold Rush bounces off the gate.
> On {every}: a fast montage of movie tokens hitting the gate, each bouncing off RED or PINK; the result box from the hook, "0 rows" RED.
> On {small}: s6's chains clear. On {three}: the notes' small case, three lines, each with its expansion beneath (all checked on DuckDB 1.5.6): `3 NOT IN (1, 2, NULL)` → PINK `NULL`, from `(3 <> 1) AND (3 <> 2) AND (3 <> NULL)`; on {safe}: s3's corner OR line lights again; on {found}: `1 IN (1, 2, NULL)` → GREEN `true`, from `(1 = 1) OR (1 = 2) OR (1 = NULL)`, the first link GREEN; on {miss}: `3 IN (1, 2, NULL)` → PINK `NULL`, then a tiny WHERE gate drops it like a RED FALSE.
> On {fix}: the death-year query returns and gains one line, verbatim (the new line written in, GREEN highlight):
> `SELECT title FROM movies` / `WHERE year NOT IN (SELECT deathyear FROM people` / `                   WHERE deathyear IS NOT NULL);`
> On {filter}: in s4's bar, the PINK block slides away, leaving only the GOLD 2,685. On {green}: The Kid's chain loses all its PINK links; every link GREEN, the chain GREEN. On {four}: the hook's four "?" slots fill GREEN, in this order: The Kid 1921, Sherlock Jr. 1924, The General 1926, It Happened One Night 1934 (checked: exactly these four rows; no ORDER BY, so show this order, the notes', in ch3 s4 too).
> On {key}: the plays_role BLUE card, its `movie_id` column underlined as a primary-key column, with a small "never NULL" (checked: DESCRIBE plays_role shows movie_id `not null`). On {alarm}: `NOT IN` gets a RED ring that pulses twice, with a small bell icon. End on two results side by side for ch3: the four movies GREEN, and NOT IN's empty result "0 rows" RED.

[c2.derive.1] {meaning} Now we can take apart the operator not in. {differs} Saying a year is not in the list means that it differs from every element of the list. {chain} It's not equal to the first, and not equal to the second, and so on, to the very end. {and} So not in becomes one long chain of comparisons, all joined by and. {pause}

[c2.derive.2] {kid} Build that chain for The Kid. {green} Two thousand, six hundred and eighty-five links compare nineteen twenty-one with a known death year, and every one of them is true. {pink} Then come twenty thousand, four hundred and ninety-four links that compare it with null. Each of those is null. {need} For a chain of ands to be true, every link has to be true. {one} But true and null is null, so a single unknown link is enough to spoil it. {dropped} The whole chain is null, and the where clause drops The Kid. {pause}

[c2.derive.3] {rush} The other movies fare no better. The Gold Rush came out in nineteen twenty-five, and two people in the database died that year. {false} So one of its links is false, and its chain is false. That movie is dropped for the right reason. {every} Every movie ends up either false or null. None is true, so you get zero rows. {pause}

[c2.derive.4] {small} The notes show the same thing with a tiny list. {three} Ask whether three is not in the list one, two, null. The answer is null, even though three is plainly missing from the list. {safe} The positive form is safe. In is a chain of ors, {found} so one in the list one, two, null, finds its true link, and true or null is true. {miss} And three in that list gives null, which the where clause drops, exactly as it would drop false.

[c2.derive.5] {fix} The fix is one line. {filter} Inside the subquery, keep only the rows where death year is not null. {green} Now every link in The Kid's chain is true. {four} And out come the four movies. The Kid, Sherlock Junior, The General, and It Happened One Night. {pause}

[c2.derive.6] {key} The no-actors query was safe all along. Movie ID is part of the primary key of plays role, and a primary key can never be null. {alarm} But whenever you see not in, let an alarm bell ring. Ask yourself whether the subquery could ever return a null. {pause}

## Scene 7 · Recap (ch2_s7_recap)

> One small callback per sentence, built left to right and top to bottom in a 3×2 grid, each with its short line underneath (DIM caption style). Each is the same object, colours and styling as the scene that taught it, shrunk.
> On {absent}: s2's three queries as three mini code cards (LEFT JOIN … `IS NULL`, `EXCEPT`, `NOT IN`), each ending in "Flow, Kaiva". Line: "three ways to ask about absence".
> On {column}: s3's tall column icon sliding into `IN ( … )`, GREEN ✓. Line: "a column goes after IN".
> On {logic}: s5's rule card and its AND grid, with the `TRUE AND NULL` cell splitting into GREEN and RED ghosts and merging PINK. Line: "unknown: try both".
> On {where}: s5's WHERE gate, TRUE through GREEN, FALSE and NULL bouncing. Line: "WHERE keeps only TRUE".
> On {chain}: s6's AND chain for The Kid with its one pulsing PINK link. Line: "one NULL spoils NOT IN". On {fix}: s6's fixed subquery line `WHERE deathyear IS NOT NULL` with the four GREEN movie cards beside NOT IN's RED "0 rows". Line: "filter out the NULLs".
> On {next}: the grid dims; The Kid's YELLOW row from s4 sends an arrow into a small plays_role card, where twelve rows light up, under a GOLD "at least one?"; on {exists}: the word `EXISTS` appears in BLUE.
> After the last word, hold the end card for about 8 s (music carries it).

[c2.recap.1] {recap} Let's recap. {absent} There are three ways to ask about absence, a left join with is null, except, and not in. {column} A subquery that returns one column goes after the keyword in, which tests membership. {logic} Null means unknown, so to combine it, try both true and false. If they agree, that's the answer. Otherwise, it's null. {where} And a where clause keeps a row only when its condition is true.

[c2.recap.2] {chain} Not in is a chain of ands, so a single null in the list stops it from ever being true. {fix} Filter the nulls out of the subquery, or make sure its column can never hold one. {pause}

[c2.recap.3] {next} Next time, we'll ask the question we really meant. For this movie, is there at least one matching row? {exists} The operator for that is called exists, and nulls never fool it. {pause}
