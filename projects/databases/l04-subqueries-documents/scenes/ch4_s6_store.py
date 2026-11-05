"""Chapter 4, scene 6: where documents live (DuckDB's two JSON tables, MongoDB). Clips c4.store.1 – c4.store.5.

Exports (static, built at ORIGIN, no updaters):
    recap_thumb()  -> JsonTableCard: the BLUE two-column `movies` table card (movie_id | movie), its three
                      movie cells closed TEAL boxes (~4.0 × 2.7). Parts .box .title .k_head .c_head .ids
                      .icons (VGroup of the cell icons).
    mongo_code(size=24) -> VGroup of three Code(lang="javascript") pairs (comment + db.movies.find(...)),
                      slide 75 verbatim, left-aligned, one blank line apart (~11.2 × 3.6 at 24).
    JsonTableCard(name, key, col, ids, closed=False), doc_icon(), closed_icon(), chip(text, color, size).
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

D = load_scene("ch4_s3_movie")

DDL = """CREATE TABLE movies(
   movie_id TEXT PRIMARY KEY,    -- e.g. 'tt0012349'
   movie    JSON NOT NULL        -- the whole document
);

CREATE TABLE people(
   person_id TEXT PRIMARY KEY,   -- e.g. 'nm0000122'
   person    JSON NOT NULL
);"""

INSERT = """INSERT INTO movies VALUES
  ('tt0012349', '{"title": 1921, "year": "The Kid"}');

SELECT * FROM movies;"""

MONGO = [
    '// Movies released in 2021 or later\ndb.movies.find({ year: { $gte: 2021 } })',
    '// Movies with "War" among their genres\ndb.movies.find({ genres: "War" })',
    '// Movies directed by Steven Spielberg\ndb.movies.find({ "directors.name": "Steven Spielberg" })',
]

MOVIE_IDS = ["tt0012349", "tt0015324", "tt0015864"]     # first three movie_ids (movies-json.duckdb)
PERSON_IDS = ["nm0000002", "nm0000004", "nm0000005"]    # first three person_ids

# collection cards (real values from movies-json.duckdb)
COLL = [
    ['{', '  "_id": "tt0012349",', '  "title": "The Kid",', '  "year": 1921', '}'],
    ['{', '  "_id": "tt0052357",', '  "title": "Vertigo",', '  "year": 1958', '}'],
    ['{', '  "_id": "tt0044741",', '  "title": "Ikiru",', '  "year": 1952', '}'],
]
COLL_SHAPED = [
    ['{', '  "_id": "tt0012349",', '  "title": "The Kid",', '  "year": 1921,', '  "minutes": 68', '}'],
    ['{', '  "_id": "tt0052357",', '  "title": "Vertigo"', '}'],
    ['{', '  "_id": "tt0044741",', '  "title": "Ikiru",', '  "year": 1952,', '  "minutes": 143,',
     '  "genres": ["Drama"]', '}'],
]

CARD_FILL = "#141C1F"   # TEAL at 0.06 over BG, opaque, so stacked cards hide the ones behind

GENRES_SRC = '"genres": ["Drama", "War"]'
DIRECTORS_SRC = """"directors": [
  { "person_id": "nm0000229",
    "name": "Steven Spielberg" }
]"""


# ══ pieces ══════════════════════════════════════════════════════════════════════

def doc_icon():
    """Small TEAL document: a 0.5 × 0.36 rounded sheet with two text lines."""
    r = RoundedRectangle(corner_radius=0.06, width=0.5, height=0.36).set_stroke(TEAL, 2).set_fill(TEAL, 0.08)
    l1 = Line([-0.15, 0.06, 0], [0.15, 0.06, 0]).set_stroke(TEAL, 2)
    l2 = Line([-0.15, -0.06, 0], [0.08, -0.06, 0]).set_stroke(TEAL, 2)
    return VGroup(r, l1, l2)


def closed_icon():
    """Closed TEAL box, same 0.5 × 0.36 footprint: filled body, a lid line and a clasp."""
    r = RoundedRectangle(corner_radius=0.04, width=0.5, height=0.36).set_stroke(TEAL, 2.5).set_fill(TEAL, 0.4)
    lid = Line([-0.25, 0.07, 0], [0.25, 0.07, 0]).set_stroke(TEAL, 2.5)
    clasp = Rectangle(width=0.08, height=0.08).set_stroke(TEAL, 2).set_fill(BG, 1).move_to([0, 0.07, 0])
    return VGroup(r, lid, clasp)


def chip(text, color=DIM, size=28, serif=False):
    t = (T if serif else Mono)(text, size, color=color if color != DIM else FG)
    r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.44, height=0.0095 * size * 1.6 + 0.36)
    r.set_stroke(color, 2).set_fill(color, 0.1)
    t.move_to(r)
    g = VGroup(r, t)
    g.box, g.text = r, t
    return g


TTL_H, HDR_H, ROW_P, CS = 0.6, 0.54, 0.54, 28


class TableCard(VGroup):
    """BLUE table card (ch1 s2's look, Mono 28): title bar, column header row, rows.
    A cell "doc" is a TEAL document icon, "box" a closed TEAL box; other cells are Mono text."""
    def __init__(self, name, cols, rows, widths, pk=1):
        super().__init__()
        W = sum(widths)
        H = TTL_H + HDR_H + len(rows) * ROW_P + 0.1
        top, left = H / 2, -W / 2
        xs = [left + sum(widths[:j]) for j in range(len(widths))]
        self.box = Rectangle(width=W, height=H).set_stroke(BLUE, 3).set_fill(BG, 0)
        self.title_bg = Rectangle(width=W, height=TTL_H).set_stroke(BLUE, 0).set_fill(BLUE, 0.35)
        self.title_bg.move_to([0, top - TTL_H / 2, 0])
        self.title = Mono(name, 30, weight=BOLD).move_to(self.title_bg)
        y_div = top - TTL_H
        hy = y_div - HDR_H / 2
        kinds = [("doc" if any(r[j] in ("doc", "box") for r in rows) else "txt") for j in range(len(cols))]
        self.heads = VGroup()
        for j, cname in enumerate(cols):
            h = Mono(cname, CS, color=TEAL if kinds[j] == "doc" else DIM)
            if kinds[j] == "doc":
                h.move_to([xs[j] + widths[j] / 2, hy, 0])
            else:
                h.move_to([xs[j] + 0.2, hy, 0], aligned_edge=LEFT)
            self.heads.add(h)
        self.pks = VGroup(*[Line(h.get_corner(DL) + 0.07 * DOWN, h.get_corner(DR) + 0.07 * DOWN)
                            .set_stroke(DIM, 2) for h in self.heads[:pk]])
        lines = [Line([left, y_div, 0], [left + W, y_div, 0]).set_stroke(BLUE, 2),
                 Line([left, y_div - HDR_H, 0], [left + W, y_div - HDR_H, 0]).set_stroke(BLUE, 1.5)]
        lines += [Line([x, y_div, 0], [x, -H / 2, 0]).set_stroke(BLUE, 1.5) for x in xs[1:]]
        self.lines = VGroup(*lines)
        self.cells, self.icons = VGroup(), VGroup()
        for i, r in enumerate(rows):
            y = y_div - HDR_H - (i + 0.5) * ROW_P - 0.03
            for j, v in enumerate(r):
                if v in ("doc", "box"):
                    m = (closed_icon() if v == "box" else doc_icon()).scale(1.15)
                    m.move_to([xs[j] + widths[j] / 2, y, 0])
                    self.icons.add(m)
                else:
                    m = Mono(v, CS)
                    m.move_to([xs[j] + 0.2, y, 0], aligned_edge=LEFT)
                    self.cells.add(m)
        self.add(self.title_bg, self.box, self.lines, self.title, self.heads, self.pks,
                 self.cells, self.icons)


def JsonTableCard(name, key, col, ids, closed=False):
    return TableCard(name, [key, col], [[i, "box" if closed else "doc"] for i in ids], [2.75, 1.65])


def recap_thumb():
    return JsonTableCard("movies", "movie_id", "movie", MOVIE_IDS, closed=True)


def mongo_code(size=24):
    g = VGroup(*[Code(s, size=size, lang="javascript") for s in MONGO])
    g.arrange(DOWN, buff=0.018 * size + 0.12, aligned_edge=LEFT)
    return g.move_to(ORIGIN)


def coll_card(lines, size=20):
    return D.doc_card("\n".join(lines), size=size)


def stack_card(first_line, w, h, size=28):
    """An opaque card for the back of the stack: only its first line shows above the card in front."""
    g = D.doc_card(None, width=w, height=h)
    g.frame.set_fill(CARD_FILL, 1)
    back = RoundedRectangle(corner_radius=0.2, width=w, height=h).set_stroke(BG, 0).set_fill(BG, 1)
    code = D.json_code(first_line, size=size)
    pad = 0.013 * size
    code.move_to(g.frame.get_corner(UL) + np.array([pad, -pad, 0]), aligned_edge=UL)
    out = VGroup(back, g.frame, code)
    out.back, out.frame, out.code = back, g.frame, code
    return out


def check_row(label):
    m = check_mark()
    t = T(label, 34)
    t.next_to(m, RIGHT, buff=0.3)
    return VGroup(m, t)


def block_box(code, a, b, color=BLUE):
    """Highlight rectangle round lines a..b of a Code (not animating the glyphs)."""
    g = VGroup(*[code.line(i) for i in range(a, b + 1)])
    r = Rectangle(width=code.width + 0.4, height=g.height + 0.24)
    r.move_to([code.get_center()[0], g.get_center()[1], 0])
    return r.set_stroke(color, 2).set_fill(color, 0.12).set_z_index(-1)


# ══ the scene ═══════════════════════════════════════════════════════════════════

class Ch4S6Store(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c1: two tables
    def clip1(self):
        with self.say("c4.store.1") as c:
            src_m, src_p = DDL.split("\n\n")
            dm, dp = Code(src_m, size=28), Code(src_p, size=28)
            VGroup(dm, dp).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([0, 0.2, 0])
            self.play(*appear(dm, dp, shift=None, lag=0.3), run_time=1.4)  # early: the DDL answers the question
            c.wait_until("movies")
            dm.generate_target()
            dm.target.move_to([0, 2.45, 0])
            self.play(*during(disappear(dp), 0, 0.4), *during([MoveToTarget(dm)], 0.2, 1), run_time=1.4)
            mv = JsonTableCard("movies", "movie_id", "movie", MOVIE_IDS).move_to([-3.4, -0.75, 0])
            pp = JsonTableCard("people", "person_id", "person", PERSON_IDS).move_to([3.4, -0.75, 0])
            self.play(*appear(mv), run_time=1.2)
            c.wait_until("of type JSON")
            self.play(*flash(list(mv.icons), color=TEAL), run_time=1.5)
            c.wait_until("people")
            dp.move_to(dm)
            self.play(*swap(dm, dp), run_time=1.0)
            self.play(*appear(pp), run_time=1.0)
            ddl = dp
            c.wait_until("rows")
            cards = VGroup(mv, pp)
            cards.generate_target()
            cards.target.scale(1.1).move_to([0, 0.75, 0])
            self.play(*disappear(ddl), run_time=0.8)
            self.play(MoveToTarget(cards), run_time=1.2)
            n1 = T("2,935 rows", 38, color=GOLD).next_to(mv, DOWN, buff=0.4)
            n2 = T("23,179 rows", 38, color=GOLD).next_to(pp, DOWN, buff=0.4)
            c.wait_until("two thousand")
            self.play(*appear(n1), run_time=1.0)
            c.wait_until("twenty-three thousand")
            self.play(*appear(n2), run_time=1.0)
            c.wait_until("course")
            ch = chip("course page: movies-json.duckdb · browser or command line", DIM, 30, serif=True)
            ch.text.set_color(DIM)
            ch.move_to([0, -3.35, 0])
            self.play(*appear(ch), run_time=1.0)  # early: one chip for the whole sentence
            self.mv, self.pp, self.n1, self.n2, self.chip = mv, pp, n1, n2, ch

    # ------------------------------------------------------------ c2: a closed box
    def clip2(self):
        mv = self.mv
        with self.say("c4.store.2") as c:
            mv.generate_target()
            mv.target.scale(1.3 / 1.1).move_to([-3.3, 0, 0])
            self.play(*disappear(self.pp, self.n1, self.n2, self.chip), run_time=0.8)
            self.play(MoveToTarget(mv), run_time=1.0)
            tgts = []
            for ic in mv.icons:
                b = closed_icon()
                b.scale(ic[0].width / 0.5).move_to(ic[0])
                tgts.append(b)
            self.play(*[Transform(ic, b) for ic, b in zip(mv.icons, tgts)], run_time=1.5)
            rows = VGroup(*[check_row(s) for s in ("ID unique", "document present", "parses as JSON")])
            rows.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([3.0, 0, 0])
            for r in rows:
                c.wait_until(own_word=r[1])
                self.play(*appear(*r, lag=0.2), run_time=1.0)
            c.wait_until("insert")
            self.play(*set_alpha([mv, rows], 0.4), run_time=0.8)
            c.wait_until("In an empty copy")
            ins = Code(INSERT, size=27).move_to([0, 1.9, 0])
            sweep_clear(self, *appear(ins, shift=None), run_time=1.6)
            c.wait_until("swapped")
            bad = [ins.find("1921"), ins.find('"The Kid"')]
            u_in = [underline(g, RED, buff=0.1) for g in bad]
            self.play(*[Create(u) for u in u_in], *flash(bad, color=RED), run_time=1.2)
            c.wait_until("accepted")
            res = self.result_table().move_to([0, -1.2, 0])
            self.play(*appear(res, shift=None), run_time=1.2)
            v = res.row_val
            u_out = [underline(select(v, "1921")[0], RED, buff=0.1),
                     underline(select(v, '"The Kid"')[0], RED, buff=0.1)]
            self.play(*[Create(u) for u in u_out], run_time=1.0)
            c.wait_until("edge")
            big = closed_icon()
            big.scale(9).move_to([0, -0.3, 0])
            big[0].set_stroke(TEAL, 5)
            big[1].set_stroke(TEAL, 5)
            big[2].set_stroke(TEAL, 4).scale(0.5)
            sweep_clear(self, FadeIn(big), run_time=1.4)
            L, R = big.get_left()[0], big.get_right()[0]
            tp = big.get_top()[1]
            spec = [("PRIMARY KEY", LEFT, 0.5), ("REFERENCES", LEFT, -1.0),
                    ("NOT NULL", RIGHT, 0.5), ("UNIQUE", RIGHT, -1.0), ("CHECK", UP, 0.0)]
            chips, ins_moves = [], []
            for txt, side, y in spec:
                ch = chip(txt, BLUE, 28)
                if side is LEFT:
                    ch.move_to([L - 0.1 - ch.width / 2, y, 0])
                elif side is RIGHT:
                    ch.move_to([R + 0.1 + ch.width / 2, y, 0])
                else:
                    ch.move_to([0, tp + 0.1 + ch.height / 2, 0])
                ch.shift(-side * 1.0 if side is not UP else UP * 0.8)
                chips.append((ch, side if side is not UP else DOWN))
            self.play(*appear(*[ch for ch, _ in chips], shift=None, lag=0.15), run_time=1.2)  # early: the list read as one
            self.play(*[ch.animate(rate_func=rush_into).shift(d * (1.0 if d is not DOWN else 0.8))
                        for ch, d in chips], run_time=0.8)
            self.play(*[ch.animate.shift(-d * 0.18) for ch, d in chips],
                      FlashAround(big[0], color=TEAL, buff=0.05), run_time=0.8)
            self.big, self.chips = big, [ch for ch, _ in chips]

    def result_table(self):
        hk, hv = Mono("movie_id", 28, color=DIM), Mono("movie", 28, color=DIM)
        rk = Mono("tt0012349", 28)
        rv = Mono('{"title": 1921, "year": "The Kid"}', 28)
        x0, x1 = 0, rk.width + 0.6
        hk.move_to([x0, 0.3, 0], aligned_edge=LEFT)
        rk.move_to([x0, -0.4, 0], aligned_edge=LEFT)
        hv.move_to([x1, 0.3, 0], aligned_edge=LEFT)
        rv.move_to([x1, -0.4, 0], aligned_edge=LEFT)
        W = x1 + rv.width
        hl = Line([-0.2, -0.05, 0], [W + 0.2, -0.05, 0]).set_stroke(DIM, 2)
        vl = Line([x1 - 0.3, 0.6, 0], [x1 - 0.3, -0.75, 0]).set_stroke(DIM, 2)
        g = VGroup(hk, hv, hl, vl, rk, rv)
        g.row_val = rv
        return g

    # ------------------------------------------------------------ c3: document databases
    def clip3(self):
        with self.say("c4.store.3") as c:
            c.wait_until("docdb")
            tbl = recap_thumb().scale(1.3).move_to([0, 0, 0])
            sweep_clear(self, *appear(tbl, shift=None), run_time=1.6)
            c.wait_until("built around documents")
            front = coll_card(COLL[0], size=28)
            front.move_to([1.0, 0.5 - front.height / 2, 0])
            front.frame.set_fill(CARD_FILL, 1)
            backs = []
            for k, ls in ((2, COLL[2]), (1, COLL[1])):
                b = stack_card("{ " + ls[1].strip(), front.width, front.height)
                b.move_to(front).shift(np.array([-0.45, 0.95, 0]) * k)
                backs.append(b)
            stack = VGroup(*backs, front)
            self.play(*swap(tbl, stack), run_time=1.4)
            c.wait_until("mongo")
            names = [chip(s, DIM, 28) for s in ("MongoDB", "CouchDB", "Couchbase")]
            for i, n in enumerate(names):
                n.move_to([-5.0, 1.0 - 1.0 * i, 0])
            self.play(*appear(names[0]), run_time=0.9)
            c.wait_until("Couch D B")
            self.play(*appear(names[1], names[2], lag=0.4), run_time=1.2)
            lab = T("collection: movies", 38, t2c={"movies": TEAL}).move_to([0.55, 3.25, 0])
            c.wait_until("coll")
            self.play(*appear(lab), run_time=1.0)  # early: said as "collections" on {coll}
            c.wait_until("id")
            cards = [backs[0], backs[1], front]
            ids = [cd.code.find('"_id"') for cd in cards]
            self.play(*[a for g in ids for a in recolor(g, YELLOW)], *flash(ids), run_time=1.5)
            c.wait_until("shapes")
            new = D.json_code("\n".join(COLL_SHAPED[0]), size=28)
            new.move_to(front.code.get_corner(UL), aligned_edge=UL)
            for g in new.find('"_id"'):
                g.set_color(YELLOW)
            anims = list(edit(front.code, new))
            anims.append(Transform(front.frame, D.fit_frame(new, size=28).set_fill(CARD_FILL, 1)))
            for b, w, rad in ((backs[1], 6.5, 0.05), (backs[0], 7.4, 0.45)):
                for part in (b.frame, b.back):
                    tgt = RoundedRectangle(corner_radius=rad, width=w, height=part.height)
                    tgt.match_style(part).move_to(part.get_corner(UL), aligned_edge=UL)
                    anims.append(Transform(part, tgt))
            self.play(*anims, run_time=2.0)

    # ------------------------------------------------------------ c4: MongoDB's filters
    def clip4(self):
        with self.say("c4.store.4") as c:
            c.wait_until("query")
            gen = Mono("db.movies.find({ … })", 44, t2c={"{ … }": TEAL}).move_to([0, 0.6, 0])
            sweep_clear(self, *appear(gen, shift=None), run_time=1.6)
            br_src = select(gen, "{ … }")[0]
            br = Brace(br_src, DOWN, buff=0.15, color=YELLOW)
            flab = T("filter", 34, color=YELLOW).next_to(br, DOWN, buff=0.15)
            c.wait_until("filters")
            self.play(GrowFromCenter(br), *appear(flab), run_time=1.0)
            code = mongo_code(28)
            code.to_edge(UP, buff=0.5)
            p1, p2, p3 = code
            c.wait_until("gte")
            self.play(*during(disappear(gen, br, flab), 0, 0.45),
                      *during(appear(p1, shift=None), 0.5, 1), run_time=1.6)
            c.wait_until("dollar G T E")
            tb = token_box(p1.find("$gte"), p1.line(1))
            self.play(FadeIn(tb), run_time=0.8)
            c.wait_until("quotes")
            u1 = underline(p1.find("year"), YELLOW, buff=0.08)
            self.play(FadeOut(tb), Create(u1), run_time=1.0)
            c.wait_until("war")
            self.play(*appear(p2, shift=None), run_time=1.0)
            u2 = underline(p2.find("genres", nth=1), YELLOW, buff=0.08)
            self.play(Create(u2), run_time=0.8)
            c.wait_until("any")
            gen_c = D.json_code(GENRES_SRC, size=32).move_to([1.8, -1.7, 0])
            self.play(*appear(gen_c, shift=None), run_time=1.0)
            dr, wr = gen_c.find('"Drama"'), gen_c.find('"War"')
            box = token_box(dr, gen_c)
            c.wait_until("element")
            self.play(FadeIn(box), *recolor(dr, RED), run_time=0.9)
            self.play(Transform(box, token_box(wr, gen_c, color=GREEN)), run_time=0.9)
            self.play(*recolor(wr, GREEN), *flash([wr], color=GREEN), run_time=0.9)
            spr = T("Saving Private Ryan", 32, color=DIM)
            spr.move_to([-4.4, -1.85, 0])
            c.wait_until("Saving", own_word=spr)
            self.play(*appear(spr), run_time=0.9)
            c.wait_until("spielberg")
            dcode = D.json_code(DIRECTORS_SRC, size=28).move_to([1.9, -2.2, 0])
            self.play(*during(disappear(gen_c, box), 0, 0.45),
                      *during(appear(p3, dcode, shift=None, lag=0.2), 0.45, 1), run_time=1.6)
            c.wait_until("dotted path")
            self.play(FlashAround(p3.find('"directors.name"'), run_time=1.0))
            steps = [(dcode.find('"directors"'), 0), (dcode.find("["), 0), (dcode.find('"name"'), 2)]
            pb = token_box(steps[0][0], dcode.line(0))
            self.play(FadeIn(pb), run_time=0.5)
            for g, ln in steps[1:]:
                self.play(Transform(pb, token_box(g, dcode.line(ln))), run_time=0.6)
            ss = dcode.find('"Steven Spielberg"')
            self.play(Transform(pb, token_box(ss, dcode.line(2), color=GREEN)), *recolor(ss, GREEN),
                      run_time=min(0.8, c.until(floor=0.3)))

    # ------------------------------------------------------------ c5: SQL learned JSON
    def clip5(self):
        with self.say("c4.store.5") as c:
            head = T("relational databases", 44, color=BLUE).move_to([0, 3.15, 0])
            sweep_clear(self, *appear(head), run_time=1.4)
            c.wait_until("list")
            names = VGroup(*[chip(s, BLUE, 28) for s in ("PostgreSQL", "MySQL", "SQLite", "DuckDB")])
            names.arrange(RIGHT, buff=0.45).move_to([0, 2.15, 0])
            self.play(*appear(*names, lag=0.3), run_time=1.6)  # early: four names, read in one breath
            c.wait_until("standard")
            std = T("SQL standard: JSON functions since 2016", 34, t2c={"2016": GOLD, "JSON": TEAL})
            std.move_to([0, 1.2, 0])
            self.play(*appear(std), run_time=1.0)
            c.wait_until("both")
            rel = TableCard("movies", ["movie_id", "title", "year"],
                            [["tt0012349", "The Kid", "1921"], ["tt0052357", "Vertigo", "1958"]],
                            [2.6, 2.1, 1.3]).move_to([-2.45, -2.05, 0])
            doc = TableCard("people", ["person_id", "person"], [[PERSON_IDS[0], "doc"], [PERSON_IDS[1], "doc"]],
                            [2.75, 1.65]).move_to([3.25, -2.05, 0])
            db = RoundedRectangle(corner_radius=0.3, width=11.8, height=3.4).set_stroke(DIM, 2.5)
            db.move_to([0, -1.75, 0])
            dlab = T("one database", 30, color=DIM)
            dlab.next_to(db.get_corner(UL), DR, buff=0.15)
            self.play(Create(db), *appear(dlab), run_time=1.2)
            self.play(*appear(rel, doc, lag=0.4), run_time=1.4)
            c.wait_until("seven")
            code = mongo_code(28).move_to([0, 0.4, 0])
            tag = T("→ part 7", 32, color=DIM).next_to(code, DOWN, buff=0.45).align_to(code, RIGHT)
            sweep_clear(self, *appear(code, shift=None), run_time=1.4)
            self.play(*appear(tag), run_time=0.8)
