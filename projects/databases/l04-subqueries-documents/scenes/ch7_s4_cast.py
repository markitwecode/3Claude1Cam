"""Chapter 7, scene 4: compare numbers as numbers. Clips c7.cast.1 – c7.cast.5.

Exports (for ch7_s5 and ch7_s8, via `load_scene("ch7_s4_cast")`):
  star_wars_query(size=28, cast_gold=False)  slide 86's query as Code (sql), verbatim.
      .arrows   [glyphs of `->>` in `(movie->>'title')`, `->>` in `(movie->>'year')`]
      .spans    [glyphs of `(movie->>'title')`, of `(movie->>'year')`]  (parens included)
      .parens   [(open, close), (open, close)]  the two pairs of parentheses (glyph VGroups)
      .cast     glyphs of `::INTEGER`
  dict_grid()  static: '99' over '321' as character cells, first column lit (YELLOW box),
               the other columns dimmed; .grid (cells), .col_box, .cells[r][c] = VGroup(box, ch)
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

J = load_scene("ch4_s2_json")

# ══ the Star Wars query (slide 86) ═════════════════════════════════════════════

SW_SRC = ("SELECT movie->>'title' AS title, movie->>'year' AS year\n"
          "FROM   movies\n"
          "WHERE (movie->>'title') LIKE 'Star Wars%'\n"
          "  AND (movie->>'year')::INTEGER >= 2000\n"
          "ORDER BY year;")
SW_SRC_NOCAST = SW_SRC.replace("(movie->>'year')::INTEGER", "(movie->>'year')")

SW_ROWS = [("Star Wars: Episode II - Attack of the Clones", "2002"),
           ("Star Wars: Episode III - Revenge of the Sith", "2005"),
           ("Star Wars: Episode VII - The Force Awakens", "2015"),
           ("Star Wars: Episode VIII - The Last Jedi", "2017"),
           ("Star Wars: Episode IX - The Rise of Skywalker", "2019")]

MINMAX_SRC = ("SELECT MIN(movie->>'minutes') AS shortest,\n"
              "       MAX(movie->>'minutes') AS longest\n"
              "FROM   movies;")
MINMAX_CAST_SRC = ("SELECT MIN((movie->>'minutes')::INTEGER) AS shortest,\n"
                   "       MAX((movie->>'minutes')::INTEGER) AS longest\n"
                   "FROM   movies;")
STRINGS_SRC = ("SELECT '999' > '2000' AS as_strings,\n"
               "       999 > 2000     AS as_numbers;")
BINDER = ["Binder Error: Cannot compare values of type VARCHAR",
          "and type INTEGER_LITERAL - an explicit cast is required"]


def star_wars_query(size=28, cast_gold=False):
    q = Code(SW_SRC, size=size)
    q.arrows = [q.find("->>", line=2), q.find("->>", line=3)]
    q.spans = [q.find("(movie->>'title')", line=2), q.find("(movie->>'year')", line=3)]
    q.parens = [(q.find("(", line=2), q.find(")", line=2)),
                (q.find("(", line=3), q.find(")", line=3))]
    q.cast = q.find("::INTEGER", line=3)
    if cast_gold:
        q.cast.set_color(GOLD)
    return q


def sw_table(size=28, pitch=0.5):
    h_t, h_y = Mono("title", size), Mono("year", size)
    titles = [Mono(t, size, color=BLUE) for t, _ in SW_ROWS]
    years = [Mono(y, size, color=BLUE) for _, y in SW_ROWS]
    x_year = max(t.width for t in titles) + 0.7
    for i, (t, y) in enumerate(zip(titles, years)):
        yy = -(i + 1) * pitch - 0.12
        t.move_to([t.width / 2, yy, 0])
        y.move_to([x_year + y.width / 2, yy, 0])
    h_t.move_to([h_t.width / 2, 0, 0])
    h_y.move_to([x_year + h_y.width / 2, 0, 0])
    right = years[0].get_right()[0]
    rule = Line([-0.1, -0.3, 0], [right + 0.1, -0.3, 0]).set_stroke(DIM, 2)
    rows = [VGroup(t, y) for t, y in zip(titles, years)]
    g = VGroup(h_t, h_y, rule, *rows)
    g.header, g.rule, g.rows, g.years, g.h_year = VGroup(h_t, h_y), rule, rows, years, h_y
    g.pitch = pitch
    return g


def year_grid(table):
    """DIM character grid over the year column: a frame and 3 lines between the digits."""
    g = table.years[0]
    p = (g[3].get_center()[0] - g[0].get_center()[0]) / 3
    x0 = g[0].get_center()[0] - p / 2
    top = table.years[0].get_y() + table.pitch / 2
    bot = table.years[-1].get_y() - table.pitch / 2
    frame = Rectangle(width=4 * p, height=top - bot).move_to([x0 + 2 * p, (top + bot) / 2, 0])
    lines = [Line([x0 + k * p, top, 0], [x0 + k * p, bot, 0]) for k in (1, 2, 3)]
    out = VGroup(frame, *lines).set_stroke(DIM, 2)
    return out


def sw_layout():
    q = star_wars_query(28, cast_gold=True).to_edge(UP, buff=0.45)
    t = sw_table()
    t.move_to(ORIGIN).align_to(q, LEFT).shift(0.1 * RIGHT)
    t.shift((q.get_bottom()[1] - 0.75 - t.header.get_top()[1]) * UP)
    return q, t


# ══ character grids ════════════════════════════════════════════════════════════

def char_grid(strings, cell=1.0, size=56, color=BLUE):
    rows, cells = VGroup(), []
    for r, s in enumerate(strings):
        row = []
        for k, ch in enumerate(s):
            box = Square(cell).set_stroke(DIM, 2).set_fill(BG, 0)
            box.move_to([k * cell, -r * cell, 0])
            m = Mono(ch, size, color=color).move_to(box)
            row.append(VGroup(box, m))
        cells.append(row)
        rows.add(VGroup(*row))
    rows.move_to(ORIGIN)
    rows.cells, rows.cell = cells, cell
    return rows


def col_box(grid, k=0, color=YELLOW):
    col = [row[k] for row in grid.cells if len(row) > k]
    r = SurroundingRectangle(VGroup(*col), buff=0.08, color=color)
    r.set_stroke(color, 3).set_fill(color, 0.18).set_z_index(-1)
    return r


def rest_cells(grid, k=0):
    return [c for row in grid.cells for c in row[k + 1:]]


def dict_grid():
    grid = char_grid(["99", "321"])
    box = col_box(grid, 0)
    for c in rest_cells(grid, 0):
        c.set_opacity(0.35)
    g = VGroup(box, grid)
    g.grid, g.col_box, g.cells = grid, box, grid.cells
    return g


def value_pair(heads, size_h=30, size_v=44, gap=1.2):
    """Two header labels side by side; returns (h0, h1) and the value anchor points."""
    h0, h1 = Mono(heads[0], size_h), Mono(heads[1], size_h)
    h1.next_to(h0, RIGHT, buff=gap)
    return h0, h1


class ChSevenCast(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── 1: the query, projection / selection, the five films ────────────────────
    def clip1(self):
        q = star_wars_query(28).move_to(0.5 * UP)
        self.q = q
        with self.say("c7.cast.1") as c:
            self.play(*appear(q, shift=None), run_time=1.2)  # early: the query is shown whole, then walked
            self.play(*flash([q.find("->>", nth=i) for i in range(4)]), run_time=1.5)
            tp = T("projection π", 30, color=DIM).next_to(q, UP, buff=0.3).align_to(q, LEFT)
            ts = T("selection σ", 30, color=DIM).next_to(q.line(2), RIGHT, buff=0.5)
            c.wait_until(own_word=tp)
            self.play(*appear(tp), run_time=1.0)
            c.wait_until(own_word=ts)
            self.play(*appear(ts), run_time=1.0)
            c.wait_until("query")
            self.play(*flash([q.find("'Star Wars%'"), q.find("2000")]),
                      run_time=min(1.8, c.until("like")))
            c.wait_until("like")
            box = token_box(q.line(2), q.line(2))
            self.play(FadeIn(box), run_time=1.0)
            c.wait_until("year")
            self.play(Transform(box, token_box(q.line(3), q.line(3))),
                      *recolor(q.cast, GOLD), run_time=1.5)
            c.wait_until("result")
            self.play(*during([FadeOut(box), *disappear(tp, ts)], 0, 0.4),
                      *during([q.animate.to_edge(UP, buff=0.45)], 0.4, 1.0), run_time=1.4)
            _, t = sw_layout()
            self.play(FadeIn(t.header), FadeIn(t.rule),
                      *appear(*t.rows, lag=0.2), run_time=1.6)
            self.t = t

    # ── 2: ->> gives a string; dictionary order; MIN/MAX without a cast ──────────
    def clip2(self):
        q, t = self.q, self.t
        with self.say("c7.cast.2") as c:
            self.play(FlashAround(q.cast, color=GOLD, time_width=1.5),
                      run_time=min(1.4, c.until("string")))
            c.wait_until("string")
            tree = J.json_tree({"title": "The Kid", "year": 1921, "minutes": 68},
                               size=32, row_gap=0.9)
            tree.move_to([-3.6, 0.3, 0])
            sweep_clear(self, time_span(FadeIn(tree), 0.6, 1.2))
            leaf = tree.node("minutes")
            c.wait_until("holds a number")
            self.play(FlashAround(leaf, color=GOLD, time_width=1.5), run_time=1.5)
            y = leaf.get_y()
            arr = Arrow([leaf.get_right()[0] + 0.15, y, 0], [2.2, y, 0], buff=0,
                        stroke_width=4, color=FG)
            lab = Mono("->>'minutes'", 32).next_to(arr, DOWN, buff=0.35)
            res = Mono("'68'", 56, color=BLUE).next_to(arr, RIGHT, buff=0.3)
            r1 = Mono("68", 56, color=BLUE)
            r1.move_to(res).shift((res[1].get_center() + res[2].get_center()) / 2 - res.get_center())
            vtag = T("varchar", 30, color=DIM).next_to(res, DOWN, buff=0.3)
            c.wait_until("The Kid's")
            self.play(GrowArrow(arr), *appear(lab), run_time=1.0)
            self.play(*fly(leaf, r1, arc=0.0), run_time=1.4)
            c.wait_until("the text")
            self.play(*edit(r1, res), *during(appear(vtag), 0.5, 1.0), run_time=1.2)
            c.wait_until("dict")
            grid = char_grid(["99", "321"])
            grid.move_to([-3.6, -0.3, 0])
            sweep_clear(self, keep=[res, vtag])
            self.play(*appear(*grid, lag=0.5), run_time=1.4)
            c.wait_until("max")
            mq = Code(MINMAX_SRC, size=30).to_edge(UP, buff=0.6)
            self.play(*during(disappear(res, vtag), 0, 0.4),
                      *during([grid.animate.move_to([-3.6, -1.3, 0])], 0.2, 0.8),
                      *during(appear(mq, shift=None), 0.4, 1.0), run_time=1.6)
            h_s, h_l = value_pair(("shortest", "longest"))
            VGroup(h_s, h_l).move_to([3.0, -0.6, 0])
            v_l = Mono("99", 48, color=RED).next_to(h_l, DOWN, buff=0.45)
            v_s = Mono("100", 48, color=RED).next_to(h_s, DOWN, buff=0.45)
            v_s.match_y(v_l)
            c.wait_until("the answer is")
            self.play(*appear(h_l, v_l, lag=0.3), run_time=1.2)
            c.wait_until("min")
            self.play(*appear(h_s, v_s, lag=0.3), run_time=1.2)
        self.grid, self.mq, self.h_s, self.h_l, self.v_s, self.v_l = grid, mq, h_s, h_l, v_s, v_l

    # ── 3: first character decides; the cast fixes it; ORDER BY year ────────────
    def clip3(self):
        grid, mq = self.grid, self.mq
        with self.say("c7.cast.3") as c:
            cb = col_box(grid, 0)
            self.play(FadeIn(cb), *set_alpha(rest_cells(grid, 0), 0.35), run_time=1.5)
            c.wait_until("nine beats three")
            self.play(FlashAround(grid.cells[0][0][1], color=YELLOW, time_width=1.5),
                      FlashAround(self.v_l, color=RED, time_width=1.5), run_time=1.5)
            c.wait_until("real")
            cq = Code(MINMAX_CAST_SRC, size=30).move_to(mq).align_to(mq, UP)
            self.play(*edit(mq, cq), *set_alpha([grid, cb], DIMMED), run_time=1.5)
            n_s = Mono("22", 48, color=GOLD).move_to(self.v_s)
            n_l = Mono("321", 48, color=GOLD).move_to(self.v_l)
            k_s = check_mark().next_to(n_s, RIGHT, buff=0.25)
            k_l = check_mark().next_to(n_l, RIGHT, buff=0.25)
            note = T("321 minutes: Gangs of Wasseypur", 28, color=DIM)
            note.next_to(VGroup(self.h_s, self.h_l, n_s, n_l), DOWN, buff=0.5)
            c.wait_until("the shortest is")
            self.play(*swap(self.v_s, n_s), *swap(self.v_l, n_l),
                      *during([FadeIn(k_s), FadeIn(k_l)], 0.5, 1.0), run_time=1.2)
            self.play(*appear(note), run_time=1.0)
            c.wait_until("order")
            q2, t2 = sw_layout()
            sweep_clear(self, time_span(FadeIn(q2), 0.6, 1.2), time_span(FadeIn(t2), 0.6, 1.2))
            vtag = T("varchar", 28, color=DIM).next_to(t2.h_year, UP, buff=0.15)
            self.play(*flash([q2.find("ORDER BY year")]), *appear(vtag), run_time=1.5)
            yg = year_grid(t2)
            cap = T("sorted as text: safe only because every year has 4 digits", 30, color=FG)
            cap.next_to(t2, DOWN, buff=0.45).match_x(t2)
            c.wait_until("It only works")
            self.play(FadeIn(yg), *appear(cap), run_time=1.4)
        self.q2, self.t2, self.vtag, self.yg, self.cap = q2, t2, vtag, yg, cap

    # ── 4: forget the cast -> binder error; '999' > '2000' ──────────────────────
    def clip4(self):
        q2 = self.q2
        with self.say("c7.cast.4") as c:
            q3 = Code(SW_SRC_NOCAST, size=28).align_to(q2, LEFT).align_to(q2, UP)
            self.play(*edit(q2, q3), run_time=min(1.6, c.until("binder")))
            box = token_box(q3.line(3), q3.line(3))
            self.play(FadeIn(box), run_time=1.0)
            err = VGroup(*[Mono(s, 28, color=RED) for s in BINDER])
            err.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([0, -1.0, 0])
            c.wait_until("binder")
            self.play(*during(disappear(self.t2, self.vtag, self.yg), 0, 0.45),
                      *during(set_alpha([self.cap], 0.4), 0, 0.45),
                      *during(appear(err), 0.5, 1.0), run_time=1.5)
            c.wait_until("friendly")
            self.play(FlashAround(err, color=GREEN, time_width=1.5), run_time=1.5)
            c.wait_until("strings")
            sq = Code(STRINGS_SRC, size=36).move_to(2.2 * UP)
            sweep_clear(self, time_span(FadeIn(sq), 0.6, 1.2))
            g2 = char_grid(["999", "2000"], cell=0.9, size=48).move_to([-3.4, -1.2, 0])
            self.play(*appear(*g2, lag=0.5), run_time=1.4)
            cb2 = col_box(g2, 0)
            h_a, h_b = value_pair(("as_strings", "as_numbers"), gap=0.9)
            VGroup(h_a, h_b).move_to([3.0, -0.6, 0])
            v_a = Mono("true", 44, color=RED).next_to(h_a, DOWN, buff=0.45)
            v_b = Mono("false", 44, color=GREEN).next_to(h_b, DOWN, buff=0.45)
            v_a.match_y(v_b)
            c.wait_until("The string nine")
            self.play(*appear(h_a, v_a, h_b, v_b, lag=0.25), run_time=1.5)
            c.wait_until("greater than")
            self.play(FadeIn(cb2), *set_alpha(rest_cells(g2, 0), 0.35), run_time=1.0)

    # ── 5: two spellings ────────────────────────────────────────────────────────
    def clip5(self):
        with self.say("c7.cast.5") as c:
            left = Code("CAST(x AS INTEGER)", size=44)
            eq = T("=", 56)
            right = Code("x::INTEGER", size=44)
            row = VGroup(left, eq, right).arrange(RIGHT, buff=0.7).move_to(0.4 * UP)
            sweep_clear(self)
            self.play(*appear(left, eq, right, lag=0.3), run_time=1.4)
            t_std = T("standard SQL", 32, color=DIM).next_to(left, DOWN, buff=0.6)
            t_dk = T("DuckDB shorthand", 32, color=DIM).next_to(right, DOWN, buff=0.6)
            t_dk.match_y(t_std)
            c.wait_until(own_word=t_std)
            self.play(*appear(t_std), run_time=1.0)
            c.wait_until("short")
            self.play(*appear(t_dk), run_time=1.0)  # early: the tag names the spelling as the voice introduces it ({short})
