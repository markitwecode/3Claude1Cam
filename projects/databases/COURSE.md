# Databases (Cambridge CST Part IA, Michaelmas 2026/27, Dr Martin Kleppmann)

Course page: https://www.cl.cam.ac.uk/teaching/2627/Databases/ (materials.html; "complete" as of
2026-11-01). 8 lectures. The materials are brand new this year.

Material in `source/`:
- `databases-notes.pdf`: the lecture notes, 72 pp., the primary text. Chapters: 1 Introduction (p. 2),
  2 Relational data modelling (10), 3 SQL and relational algebra (17; 3.6 Query composition, 32),
  4 Document databases (36), 5 Graph databases (50), 6 Datalog and recursive queries (59),
  7 Conclusions (71). The supervision exercises are embedded in the notes.
- `databases-handout.pdf`: the slides without builds, 141 pp. Landmarks: subqueries pp. ~60–71,
  Document Databases 72–99, Graph databases 100–118, Datalog 119–.
- `databases-exercises.pdf`: the supervision exercises on their own (4 pp.).
- The course's running example, a movies database, in every form the course uses:
  `movies.duckdb` (relational), `movies-json.duckdb` (JSON documents), `movies.tvdb` (property
  graph, Traverse), `movies-souffle.zip` (Datalog facts and schema).
- Recordings: each lecture's `vk lecture` output (`*.transcript.md`, and a digest when Gemini is on).
  The videos themselves stay in ~/Downloads (read in place).

Each lecture is its own project folder here, `lNN-<slug>/`, under the course line
"Databases · Lecture N". The lecturer doesn't seem to number lectures; the numbers are inferred
from the recording dates (Tue/Thu: L4 = Tue 2026-10-27, L5 = Thu 2026-10-29).

## Toolchain (verify every query on screen against the real database)
- **SQL and JSON:** DuckDB CLI v1.5.6, `duckdb` (~/.local/bin). `duckdb -readonly
  projects/databases/source/movies.duckdb -c "<sql>"` (or `movies-json.duckdb`). Same version as the
  lecture's demos.
- **Cypher:** Kleppmann's `cypher-shell` (the Traverse engine, same results as the browser app),
  installed at `projects/databases/tools/cypher-shell`. From that folder:
  `printf "<query>;\n" | node cypher-shell.mjs ../../source/movies.tvdb`.
- **SQL/PGQ** (not examinable): DuckDB's `duckpgq` community extension, installed
  (2026-11-01). `LOAD duckpgq;` as its own statement (in a single `-c` string the parser rejects
  `CREATE PROPERTY GRAPH`).
- **Mixed languages on screen:** `Code(src, lang="sql")` highlights one block in another lexer
  than the project's `code_language` (added 2026-11-01).
- **Datalog:** Soufflé is not installed (needed from the Datalog lecture on).

| # | Lecture | Notes | Project | State |
|---|---|---|---|---|
| 1–3 | Introduction, relational modelling, SQL and relational algebra (not recorded here) | ch. 1–3.5 | — | not started |
| 4 | Subqueries and Documents (recorded Tue 2026-10-27) | §3.6, ch. 4 | `l04-subqueries-documents/` | ✅ done: 10 videos in `out/`, 111.1 min; Gemini checks after the Wed reset (2026-11-02) |
| 5 | Graph Databases (recorded Thu 2026-10-29) | ch. 5 | `l05-graphs/` | ✅ done: 6 videos in `out/`, 64.4 min; Gemini checks after the Wed reset (2026-11-01) |
| 6–8 | Datalog and recursive queries, conclusions / trade-offs | ch. 6–7 | — | not started |

## Shared across lectures
- **Narration:** SQL is "sequel" (the lecturer's word; the captions write "sequel practicals"),
  DuckDB "Duck D B", MongoDB "Mongo D B", Neo4j "Neo four J", SQL/PGQ "sequel P G Q", GQL "G Q L".
  IDs (tt…, nm…) are never read aloud. Spoken cross-references say "part N", as the title cards
  do. (L5-only names are in its PLAN.md Decisions.)
- **The models' looks** (L4's PLAN.md conventions, L5's Decisions): relational = BLUE table cards
  (L4's schema map, slide 23's layout); documents = TEAL JSON cards and trees (L4 ch4); graphs =
  circles, Person PINK, Movie BLUE (L5). L4 ch6 s3's "tangle" (the movie–person many-to-many drawn
  as itself, from Chaplin, Jackie Coogan, The Kid and The Gold Rush) already uses L5's graph look,
  so L5 ch1 s2's redraw of those four meets it. Within L4, PINK otherwise means NULL.
- **Code colouring:** the project's lexer is the default (L4 `sql`, L5 `cypher`); a block in
  another language passes it per block: `Code(src, lang="json")` in L4, `Code(src, lang="sql")`
  in L5.

## Voice rules (TTS), learnt 2026-11-04 from Gemini listens
- Hyphenate "semi-join" and "anti-join" in narration (unhyphenated, the voice says "semi one" or
  "semi-joint"). Scenes' cue words still match.
- "Data-log", not "Datalog" (heard "to tall og"). Put "coalesce" after a word, as in "the function
  coalesce", not at the start of a sentence (heard "Coless").
- "where" at the start of a phrase can come out as "were": put a word before it ("In any query, a
  where clause"). "paths" can come out as "pass": prefer "path language".
- Names: spell them as said ("Blin" for B.F. Blinn); the screen keeps the real spelling.
