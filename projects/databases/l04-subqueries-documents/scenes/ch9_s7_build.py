"""Chapter 9, scene 7: Exercise 16, documents from tables. Clips c9.build.1 – c9.build.6.

Exports (static, built in place; `load_scene("ch9_s7_build").<name>()`):
- kid_doc(): our generated document for The Kid, a TEAL doc card (ch4 s3's look, json_code 21),
  17 lines (DuckDB's one-line output laid out, actors after the third elided /* 7 more */),
  centred at KID_POS (-3.55, 0): the left half. `.frame .code`.
- grid(): the 3 x 10 grid of {grid}: `.cells[r][c]` BLUE squares, `.rows` the genre labels (T 30),
  `.heads` the ten actor surnames (T 26, rotated 45 deg) above the columns. Centred near (0, 0.6).
- recap_r7(): the grid split into two lists (static): `.genres` (3 squares + labels) `.actors`
  (10 squares + surnames), GOLD `.n3` "3" and `.n10` "10".
- handover_shot(): this scene's last frame (s8 opens on it): VGroup(kid_doc()).
"""
# style: 2
# handover: next
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

S1 = load_scene("ch9_s1_intro")
D = load_scene("ch4_s3_movie")
OL = load_scene("ch3_s2_correlated")
SCH = load_scene("ch1_s2_schema")
A2 = load_scene("ch2_s2_absent")
R57 = load_scene("ch5_s7_recap")


def _join_card():
    """s2's JOIN result card (1, 1), its YELLOW "JOIN" moved beside it, for the {again} inset."""
    jc = load_scene("ch9_s2_pairs").join_card()
    jc.label.next_to(jc.card, RIGHT, buff=0.3)
    return jc


TT = "tt0012349"
OBJ_SRC = "SELECT json_object('title', 'The Kid', 'year', 1921);"
OBJ_OUT = '{"title":"The Kid","year":1921}'
LIST_SRC = """SELECT list(g.name)
FROM has_genre AS hg
JOIN genres AS g ON g.genre_id = hg.genre_id
WHERE hg.movie_id = 'tt0012349';"""
LIST_VAL = "[Comedy, Drama, Family]"

NAIVE_SRC = """SELECT json_object('movie_id', m.movie_id,
                   'title', m.title, 'year', m.year,
                   'genres', list(g.name),
                   'actors', list(json_object(
                       'person_id', p.person_id, 'name', p.name)))
FROM movies AS m
JOIN has_genre AS hg ON hg.movie_id = m.movie_id
JOIN genres AS g ON g.genre_id = hg.genre_id
JOIN has_position AS hp ON hp.movie_id = m.movie_id
                       AND hp.position = 'actor'
JOIN people AS p ON p.person_id = hp.person_id
GROUP BY m.movie_id, m.title, m.year;"""

SOL_SRC = """SELECT json_object(
    'movie_id', m.movie_id,
    'title',    m.title,
    'year',     m.year,
    'genres',   (SELECT list(g.name)
                 FROM has_genre AS hg
                 JOIN genres AS g ON g.genre_id = hg.genre_id
                 WHERE hg.movie_id = m.movie_id),
    'actors',   (SELECT list(json_object('person_id', p.person_id,
                                         'name', p.name))
                 FROM has_position AS hp
                 JOIN people AS p ON p.person_id = hp.person_id
                 WHERE hp.movie_id = m.movie_id
                   AND hp.position = 'actor')
  ) AS movie
FROM movies AS m;"""

EDNA = ['    {"person_id": "nm0701012",', '     "name": "Edna Purviance"},']
NAIVE_DOC = "\n".join(
    ["{", '  "movie_id": "tt0012349",', '  "title": "The Kid",', '  "year": 1921,',
     '  "genres": [', '    "Comedy", "Drama", "Family",', '    "Comedy", "Drama", "Family",',
     "    /* 24 more */", "  ],", '  "actors": ['] + EDNA * 3 + ["    /* 27 more */", "  ]", "}"])

KID_DOC = "\n".join(
    ["{", '  "movie_id": "tt0012349",', '  "title": "The Kid",', '  "year": 1921,',
     '  "genres": [', '    "Comedy", "Drama", "Family"', "  ],", '  "actors": [',
     '    {"person_id": "nm0000122",', '     "name": "Charles Chaplin"},',
     '    {"person_id": "nm0001067",', '     "name": "Jackie Coogan"},',
     '    {"person_id": "nm0042317",', '     "name": "Albert Austin"},',
     "    /* 7 more */", "  ]", "}"])
KID_POS = np.array([-3.55, 0.0, 0])
KID_SIZE = 21

GENRES = ["Comedy", "Drama", "Family"]
SURNAMES = ["Chaplin", "Coogan", "Austin", "Bains", "Baker", "Bergman", "Biby", "Blinn", "Miller",
            "Purviance"]
GP, GSQ = 0.9, 0.72                      # grid pitch, square side
GX0, GY0 = -3.6, 0.6                     # centre of cell (0, 0)
G_SHIFT = np.array([-0.6, -0.35, 0])     # the genre list after the split
A_SHIFT = np.array([0, 0.55, 0])         # the actor list after the split

ROLES_LINES = ["[Charles Chaplin, Jackie Coogan,", " Albert Austin, Beulah Bains,", " Nellie Bly Baker,",
               " Henry Bergman, Edward Biby,", " B.F. Blinn, Carl Miller,",
               " Edna Purviance, Albert Austin,", " Henry Bergman]"]
LIGHT_RED = "#FDA59C"
RX = 3.6            # right-half centre in clips 5-6


# ---------------------------------------------------------------- exports
def kid_doc():
    card = D.doc_card(KID_DOC, size=KID_SIZE)
    card.move_to(KID_POS)
    return card


def handover_shot():
    return VGroup(kid_doc())


def _square(x, y):
    return Square(GSQ).set_stroke(BLUE, 2).set_fill(BLUE, 0.28).move_to([x, y, 0])


def _cell_xy(r, c):
    return GX0 + c * GP, GY0 - r * GP


def _row_label(r):
    x, y = _cell_xy(r, 0)
    return T(GENRES[r], 30).move_to([0, y, 0]).align_to([x - GSQ / 2 - 0.3, 0, 0], RIGHT)


def _head(c):
    x, y = _cell_xy(0, c)
    h = T(SURNAMES[c], 26).rotate(PI / 4)
    h.move_to([x - 0.2, y + GSQ / 2 + 0.14, 0], aligned_edge=DL)
    return h


def grid():
    g = VGroup()
    g.cells = [[_square(*_cell_xy(r, c)) for c in range(10)] for r in range(3)]
    g.rows = VGroup(*[_row_label(r) for r in range(3)])
    g.heads = VGroup(*[_head(c) for c in range(10)])
    g.add(g.rows, g.heads, *[s for row in g.cells for s in row])
    return g


def recap_r7():
    gs = VGroup(*[VGroup(_square(*_cell_xy(r, 0)), _row_label(r)).shift(G_SHIFT) for r in range(3)])
    acts = VGroup(*[VGroup(_square(*_cell_xy(0, c)), _head(c)).shift(A_SHIFT) for c in range(10)])
    n3 = T("3", 44, GOLD).next_to(gs, DOWN, buff=0.3).set_x(gs[0][0].get_x())
    n10 = T("10", 44, GOLD).next_to(acts[-1][0], RIGHT, buff=0.35)
    g = VGroup(gs, acts, n3, n10)
    g.genres, g.actors, g.n3, g.n10 = gs, acts, n3, n10
    return g


# ---------------------------------------------------------------- helpers
def list_cell(size=30, center=ORIGIN):
    """BLUE result cell at center: DIM header list(g.name) over the value, value split into pieces
    (.names[genre], .punct; not members: they arrive one by one)."""
    head = Mono("list(g.name)", size - 2, DIM)
    full = Mono(LIST_VAL, size, YELLOW)
    w = max(head.width, full.width) + 0.6
    p = 0.6
    box = Rectangle(width=w, height=2 * p).set_stroke(BLUE, 2.5).move_to(center)
    hl = Line(box.get_left(), box.get_right()).set_stroke(BLUE, 2)
    head.move_to(box.get_top() + DOWN * p / 2)
    full.move_to(box.get_bottom() + UP * p / 2)
    names = {n: Mono(n, size, YELLOW).move_to(select(full, n)[0]) for n in GENRES}
    punct = VGroup(*[Mono(ch, size, YELLOW).move_to(gl) for ch, gl in _punct_glyphs(full)])
    g = VGroup(box, hl, head)
    g.box, g.head, g.names, g.punct = box, head, names, punct
    return g


def _punct_glyphs(full):
    out = [("[", select(full, "[")[0]), ("]", select(full, "]")[0])]
    for occ in select(full, ","):
        out.append((",", occ))
    return out


def chip(text, size=21):
    value = Mono(text, size, GOLD)
    box = RoundedRectangle(corner_radius=0.12, width=value.width + 0.32, height=value.height + 0.3)
    box.set_stroke(GOLD, 2.5).set_fill(GOLD, 0.15).move_to(value)
    g = VGroup(box, value)
    g.box, g.value = box, value
    return g


def movies_inset():
    loop = OL.outer_loop(left_rows=[("The Kid", "1921"), ("Sherlock Jr.", "1924"),
                                    ("The Gold Rush", "1925"), None],
                         lsize=26, title_size=26, lpitch=0.46, cursor_pad=0.24)
    left = loop.left
    curs = [loop.cursor_at(i) for i in range(3)]
    g = VGroup(left, *curs)
    g.move_to([RX + 0.3, 2.45, 0])
    return left, curs


def flow_movie():
    f = R57.flow_row()
    for cell in f.cells:
        cell[0].set_stroke(BLUE, 3)
    return f


# ---------------------------------------------------------------- scene
class Ch9S7Build(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()

    # ------------------------------------------------------------ c9.build.1
    def clip1(self):
        with self.say("c9.build.1") as c:
            row = S1.ex_row()
            self.play(*appear(row, shift=None), run_time=0.8)  # early: the exercise row, as s1 left it
            big = S1.big_card(16)
            others = [row.cards[n] for n in (13, 14, 15)]
            src = row.cards[16]
            self.play(*during(disappear(*others, src), 0, 0.4),  # early: the exercise card, read whole
                      *during([ReplacementTransform(src.box.copy(), big.box)], 0.1, 0.7),
                      *during(appear(big.text, shift=None), 0.55, 1),
                      run_time=1.8)  # early: the exercise card, read whole
            self.card = big
            c.wait_until("compare")
            self.play(*appear(big.hint), run_time=1.0)  # early: the hint, shown with the question
            c.wait_until("stop")
            self.play(FadeIn(big.pause, scale=0.8), run_time=0.8)

    # ------------------------------------------------------------ c9.build.2
    def clip2(self):
        with self.say("c9.build.2", gap=1.0) as c:
            c.wait_until("object")
            code = Code(OBJ_SRC, 28).move_to([0, 1.0, 0])
            sweep_clear(self, *during(appear(code, shift=None), 0.5, 1), run_time=1.4)
            arcs = VGroup()
            for k, v in (("'title'", "'The Kid'"), ("'year'", "1921")):
                a, b = code.find(k), code.find(v)
                arc = ArcBetweenPoints(a.get_top() + 0.1 * UP, b.get_top() + 0.1 * UP, angle=-PI / 2)
                arcs.add(arc.set_stroke(YELLOW, 4))
            c.wait_until("alternating")
            self.play(Create(arcs[0]), run_time=0.9)
            self.play(Create(arcs[1]), run_time=0.9)
            c.wait_until("builds an object")
            out = D.json_code(OBJ_OUT, 40).move_to([0, -0.7, 0])
            self.play(*appear(out), run_time=min(1.2, c.until("list")))
            c.wait_until("list")

            top = VGroup(arcs, code, out)
            top.generate_target()
            top.target.scale(0.56).move_to([0, 3.6 - 0.56 * top.height / 2, 0])
            lcode = Code(LIST_SRC, 26).move_to([0, 1.0, 0])
            self.play(*during([MoveToTarget(top)], 0, 0.6), *during(appear(lcode, shift=None), 0.5, 1),
                      run_time=min(1.6, c.until("genres")))
            tab = SCH.RowTable("has_genre JOIN genres", ["movie_id", "genre_id", "name"],
                               [[TT, "5", "Comedy"], [TT, "8", "Drama"], [TT, "11", "Family"]],
                               colors=[[DIM, FG, YELLOW]] * 3, size=28, pitch=0.48)
            tab.move_to([-3.45, 0, 0]).align_to([0, -0.45, 0], UP)
            cell = list_cell(30, center=[3.85, -1.95, 0])
            arrow = Arrow(tab.get_right() + 0.1 * RIGHT + 0.25 * DOWN, cell.box.get_left() + 0.1 * LEFT,
                          buff=0.05, stroke_width=4, color=YELLOW)
            self.play(*appear(tab, shift=None), run_time=1.0)
            self.play(*appear(cell, shift=None), GrowArrow(arrow), run_time=1.0)
            c.wait_until("genres")
            names = [tab.cell(i, 2) for i in range(3)]
            spans = [(0.5, 1), (0.25, 0.75), (0, 0.5)]
            self.play(*[a for n, g, (a0, a1) in zip(names, GENRES, spans)
                        for a in during(fly(n, cell.names[g], arc=0), a0, a1)],
                      run_time=min(1.8, 0.6 * c.until()))
            self.play(*appear(cell.punct, shift=None), run_time=0.6)

    # ------------------------------------------------------------ c9.build.3
    def clip3(self):
        with self.say("c9.build.3") as c:
            code = Code(NAIVE_SRC, 23).move_to([0, 0.1, 0])
            sweep_clear(self, *during(appear(code, shift=None), 0.5, 1), run_time=1.6)
            box = SurroundingRectangle(VGroup(*[code.line(i) for i in range(6, 11)]), buff=0.1)
            box.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12).set_z_index(-1)
            c.wait_until("genres")
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("group by")
            box2 = SurroundingRectangle(code.line(11), buff=0.05).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12)
            self.play(Transform(box, box2.set_z_index(-1)), run_time=0.8)
            c.wait_until("collect")
            box3 = SurroundingRectangle(VGroup(code.find("list(g.name)", line=2),
                                               code.find("list(json_object(", line=3), code.line(4)), buff=0.1)
            self.play(Transform(box, box3.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12).set_z_index(-1)),
                      run_time=0.8)

            c.wait_until("kid")
            card = D.doc_card(NAIVE_DOC, size=19)
            card.move_to([1.3, 0, 0])
            self.play(*during([FadeOut(box)], 0, 0.3), *during(disappear(code), 0, 0.45),
                      *during(appear(card, shift=None), 0.5, 1), run_time=min(1.8, c.until("thirty")))
            c.wait_until("thirty")
            n1 = T("30", 40, GOLD).next_to(card.code.line(8), RIGHT, buff=0.35)
            n2 = T("30", 40, GOLD).next_to(card.code.line(17), RIGHT, buff=0.35)
            self.play(*appear(n1, n2, shift=None, lag=0.4), run_time=1.1)
            ednas = VGroup(*[card.code.line(i) for i in range(10, 16)])
            self.play(FlashAround(ednas, time_width=1.5, run_time=1.4))
            c.wait_until("ask")
            q = T("Why thirty?", 48, YELLOW).move_to([-4.3, 0, 0])
            self.play(*appear(q), run_time=1.0)

    # ------------------------------------------------------------ c9.build.4
    def clip4(self):
        with self.say("c9.build.4") as c:
            g = grid()
            sweep_clear(self, *during(appear(g.rows, g.heads, shift=None, lag=0.3), 0.5, 1),
                        run_time=1.6)  # early: the grid's sides, The Kid's genre and actor rows
            cells = [s for row in g.cells for s in row]
            self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in cells], lag_ratio=0.08),
                      run_time=min(2.6, c.until("three times ten")))
            c.wait_until("three times ten")
            eq = T("3 × 10 = 30", 48, GOLD).move_to([0.5, -1.95, 0])
            self.play(*appear(eq), run_time=1.0)
            self.grid, self.eq = g, eq

            c.wait_until("again")
            jc = _join_card()
            jc.scale(min(1, 1.8 / jc.height)).move_to([-4.9, -2.6, 0])
            jc.shift(UP * max(0, -3.5 - jc.get_bottom()[1]))
            self.play(*appear(jc, shift=None), run_time=0.8)
            self.play(*flash(list(jc.card.vals), time_width=1.5), run_time=1.3)
            self.jc = jc

            c.wait_until("flow")
            fl = flow_movie().move_to([3.6, -3.0, 0])
            self.play(*appear(fl, shift=None), run_time=0.9)
            c.wait_until("vanished")
            reds = [cell[0].animate.set_stroke(RED, 3) for cell in fl.cells] + \
                   [cell[1].animate.set_color(RED) for cell in fl.cells]
            self.play(*during(reds, 0, 0.5), *during([FadeOut(fl)], 0.5, 1), run_time=1.4)
            c.wait_until("two thousand")
            cnt = VGroup(T("2,934 rows", 40, GOLD), T("vs", 30, DIM), T("2,935 movies", 40))
            cnt.arrange(RIGHT, buff=0.3).move_to([3.4, -3.0, 0])
            for m in cnt[1:]:
                m.align_to(cnt[0], DOWN)
            self.play(*appear(cnt, shift=None), run_time=1.0)
            self.cnt = cnt
            c.wait_until("one short")
            self.play(FlashAround(cnt[0], time_width=1.5, run_time=min(1.0, c.until())))

    # ------------------------------------------------------------ c9.build.5
    def clip5(self):
        g = self.grid
        with self.say("c9.build.5") as c:
            # fix: the grid splits into the two lists
            corner = g.cells[0][0].copy()
            self.add(corner)
            moves = []
            for r in range(3):
                moves.append(g.cells[r][0].animate.shift(G_SHIFT))
                moves.append(g.rows[r].animate.shift(G_SHIFT))
            moves.append(corner.animate.shift(A_SHIFT))
            for cc in range(1, 10):
                moves.append(g.cells[0][cc].animate.shift(A_SHIFT))
            for cc in range(10):
                moves.append(g.heads[cc].animate.shift(A_SHIFT))
            inner = [g.cells[r][cc] for r in (1, 2) for cc in range(1, 10)]
            ref = recap_r7()
            self.play(*during([FadeOut(m) for m in inner] + disappear(self.eq, self.jc, self.cnt), 0, 0.4),
                      *during(moves, 0.25, 0.8), *during(appear(ref.n3, ref.n10, lag=0.3), 0.75, 1),
                      run_time=2.2)  # early: the two counts, 3 and 10

            # scalar: the solution, each subquery boxed, collapsing to one value
            c.wait_until("scalar")
            code = Code(SOL_SRC, 21)
            code.move_to([-6.6 + code.width / 2, 3.55 - code.height / 2, 0])
            sweep_clear(self, *during(appear(code, shift=None), 0.5, 1), run_time=min(1.4, c.until("subquery")))
            c.wait_until("subquery")
            gsub = [code.find("(SELECT list(g.name)", line=4), code.line(5), code.line(6),
                    code.find("WHERE hg.movie_id = m.movie_id)", line=7)]
            asub = [code.find("(SELECT list(json_object('person_id', p.person_id,", line=8)] + \
                   [code.line(i) for i in range(9, 13)] + [code.find("AND hp.position = 'actor')", line=13)]
            boxes = []
            for sub in (gsub, asub):
                b = SurroundingRectangle(VGroup(*sub), buff=0.08).set_stroke(YELLOW, 2.5)
                b.set_fill(YELLOW, 0.1).set_z_index(-1)
                boxes.append(b)
            self.play(*[FadeIn(b) for b in boxes], run_time=0.8)
            c.wait_until("single value")
            chips = [chip(LIST_VAL), chip("[{…}, {…}, …]")]
            comma = code.find(",", line=7)
            comma_home = comma.get_center()
            shrink = []
            for sub, b, ch in zip((gsub, asub), boxes, chips):
                head = sub[0]
                ch.move_to([head.get_left()[0] + ch.width / 2, head.get_y(), 0])
                p = ch.get_center()
                for part in sub:
                    for gl in part:
                        gl.save_state()
                        shrink.append(gl.animate.scale(0.12, about_point=p).set_opacity(0))
            comma_to = comma.copy().next_to(chips[0], RIGHT, buff=0.06).align_to(comma, DOWN)
            comma_to.set_y(chips[0].get_bottom()[1] + 0.12 + comma.height / 2)
            self.play(*during(shrink, 0, 0.5),
                      *during([ReplacementTransform(b, ch.box) for b, ch in zip(boxes, chips)], 0.1, 0.7),
                      *during([FadeIn(ch.value) for ch in chips], 0.55, 1),
                      *during([comma.animate.move_to(comma_to)], 0.5, 1),
                      run_time=1.8)

            # corr: back to the subqueries, m.movie_id YELLOW, the outer loop small
            c.wait_until("corr")
            glyphs = [gl for sub in (gsub, asub) for part in sub for gl in part]
            self.play(*during([FadeOut(ch) for ch in chips], 0, 0.4),
                      *during([Restore(gl) for gl in glyphs] + [comma.animate.move_to(comma_home)], 0.35, 1),
                      run_time=1.4)
            mids = [code.find("m.movie_id", line=7), code.find("m.movie_id", line=12)]
            c.wait_until("outer movie")
            self.play(*[a for m in mids for a in recolor(m, YELLOW)], *flash(mids, time_width=1.5),
                      run_time=1.2)
            left, curs = movies_inset()
            cur = curs[0]
            self.play(*appear(left, shift=None), FadeIn(cur), run_time=1.0)  # early: the movies list, read whole
            c.wait_until("for every movie")
            self.play(*flash(mids, time_width=1.5), run_time=0.9)
            for i in (1, 2):
                self.play(Transform(cur, curs[i]), *flash(mids, time_width=1.5), run_time=0.7)
            settle(self, code)

            # result
            c.wait_until("result")
            card = kid_doc()
            sweep_clear(self, time_span(FadeIn(card.frame), 0.6, 1.4), time_span(FadeIn(card.code), 0.7, 1.5),
                        run_time=1.5)
            n3 = T("3", 40, GOLD).next_to(card.code.line(6), RIGHT, buff=0.35)
            n10 = T("10", 40, GOLD).next_to(card.code.line(15), RIGHT, buff=0.35)
            self.play(*appear(n3, n10, shift=None, lag=0.4), run_time=1.0)
            c.wait_until("every movie", nth=1)
            rows = T("2,935 rows", 52, GOLD).move_to([RX, 0, 0])
            self.play(*appear(rows), run_time=min(1.0, c.until()))  # early: the document count, on "every movie"
            self.card, self.n3, self.n10, self.rows = card, n3, n10, rows

    # ------------------------------------------------------------ c9.build.6
    def clip6(self):
        with self.say("c9.build.6") as c:
            rows = self.rows
            s1 = Code("FROM has_position AS hp", 24)
            dots = MathTex(r"\vdots", color=DIM).set_height(0.32)
            s2 = Code("WHERE hp.movie_id = m.movie_id\n  AND hp.position = 'actor'", 24)
            snip = VGroup(s1, dots, s2).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            dots.shift(RIGHT * 0.3)
            snip.move_to([RX, 1.35, 0])
            self.play(rows.animate.scale(0.7).move_to([RX, 3.25, 0]),
                      *during(appear(snip, shift=None), 0.4, 1), run_time=1.5)
            pos = s2.find("hp.position = 'actor'", line=1)
            c.wait_until("has position")
            self.play(*recolor(pos, YELLOW), FlashAround(pos, time_width=1.5), run_time=1.3)

            c.wait_until("kaiva")
            kaiva = A2.movie_card("Kaiva", 2023, size=30).move_to([RX, -0.6, 0])
            ten = T("has_position: 10 actors", 30, GREEN).move_to([RX, -1.6, 0])
            zero = T("plays_role: 0 rows", 30, DIM).move_to([RX, -2.25, 0])
            self.play(*appear(kaiva, shift=None), run_time=0.9)
            c.wait_until(own_word=ten, cue="ten actors")
            self.play(*appear(ten, zero, lag=0.5), run_time=1.3)  # early: the 0 rows answers "no rows in plays role"

            c.wait_until("roles")
            head = VGroup(T("actors over", 30, DIM), Mono("plays_role", 28, BLUE, weight=BOLD))
            head.arrange(RIGHT, buff=0.2).move_to([RX, 2.2, 0])
            lst = Mono("\n".join(ROLES_LINES), 22, line_spacing=0.9)
            lst.next_to(head, DOWN, buff=0.35).set_x(RX)
            self.play(*during(disappear(snip, kaiva, ten, zero), 0, 0.45),
                      *during(appear(head, lst, shift=None, lag=0.2), 0.45, 1), run_time=1.6)
            c.wait_until("albert")
            aa = select(lst, "Albert Austin")
            hb = select(lst, "Henry Bergman")
            self.play(*[a for o in aa for a in recolor(o, RED)],
                      *[a for o in hb for a in recolor(o, LIGHT_RED)], run_time=1.0)
            note = T("Car Thief · Man in Shelter", 30, RED).next_to(lst, DOWN, buff=0.4).set_x(RX)
            c.wait_until(own_word=note, cue="two parts")
            self.play(*appear(note), run_time=0.9)
            c.wait_until("twice")
            self.play(*flash(list(aa), color=RED, time_width=1.5), run_time=1.2)
            self.side = [rows, head, lst, note]
        self.wait(2.0)
        self.play(*disappear(*self.side, self.n3, self.n10), run_time=1.0)
        self.wait(1.0)
