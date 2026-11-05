"""Chapter 6, scene 5: Exercise 21, the co-star query in SQL. Clips c6.sql.1 – c6.sql.5.

Layout: side by side can't hold the 43-character Cypher and the 56-character SQL at a readable
size, so (as in ch2 s6) they are stacked: the drawing p1 -> m <- p2 top-left, ch3 s5's query
top-right, the SQL built line by line underneath.

Exports: recap_tile() (for s7): pattern pieces with arrows into their SQL lines
(h1, h2 YELLOW, p1, p2 PINK, GROUP BY YELLOW), centred at ORIGIN, ~11 x 3.6.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S57 = load_scene("ch5_s7_exercises")
S35 = load_scene("ch3_s5_aggregate")
S61 = load_scene("ch6_s1_intro")
S64 = load_scene("ch6_s4_wachowski")

CY_S, SQ_S = 27, 27
CYL = S35.Q3.split("\n")
SQL = ["SELECT   p1.name AS name1, p2.name AS name2,",
       "         count(*) AS movies",
       "FROM     has_position AS h1",
       "JOIN     has_position AS h2 ON h2.movie_id = h1.movie_id",
       "JOIN     people AS p1 ON p1.person_id = h1.person_id",
       "JOIN     people AS p2 ON p2.person_id = h2.person_id",
       "WHERE    h1.position = 'actor'",
       "  AND    h2.position = 'actor'",
       "  AND    h1.person_id < h2.person_id",
       "GROUP BY p1.name, p2.name",
       "ORDER BY movies DESC, name1, name2",
       "LIMIT    5;"]
R2 = "FROM     plays_role AS r1"
R3 = "JOIN     plays_role AS r2 ON r2.movie_id = r1.movie_id"

TOP5 = S35.TOP5
STONE = [("Matt Stone", "Trey Parker", "51"), ("Trey Parker", "April Stewart", "36"),
         ("Matt Stone", "April Stewart", "33"), ("Chris Evans", "Scarlett Johansson", "24"),
         ("Robert Downey Jr.", "Scarlett Johansson", "23")]
SELF = [("Samuel L. Jackson", "Samuel L. Jackson", "39"), ("Tom Hanks", "Tom Hanks", "39"),
        ("Brad Pitt", "Brad Pitt", "38")]
MATT = ["Kenny McCormick", "Kyle Broflovski", "Saddam Hussein"]
TREY = ["Eric Cartman", "Satan", "Stan Marsh"]
GROUP_IDS = "GROUP BY p1.person_id, p2.person_id, p1.name, p2.name"
CY_IDS = ("RETURN p1.person_id, p2.person_id,\n"
          "       p1.name AS name1, p2.name AS name2,\n"
          "       count(*) AS movies")


# ---------------------------------------------------------------- pieces
def paint_sql(ln, s):
    """ch2 s6's colour-matching: edges YELLOW, people PINK, the shared movie BLUE."""
    marks = [("has_position AS h1", YELLOW), ("has_position AS h2", YELLOW),
             ("plays_role AS r1", RED), ("plays_role AS r2", RED),
             ("h2.movie_id = h1.movie_id", BLUE), ("r2.movie_id = r1.movie_id", BLUE),
             ("people AS p1", PINK), ("people AS p2", PINK),
             ("p1.person_id = h1.person_id", PINK), ("p2.person_id = h2.person_id", PINK),
             ("h1.position = 'actor'", YELLOW), ("h2.position = 'actor'", YELLOW)]
    for sub, col in marks:
        if sub in s:
            ln.find(sub).set_color(col)
    if s.startswith("GROUP BY p1.name"):
        for g in ln.find(s):
            g.set_fill(YELLOW, opacity=1)
    S35.paint(ln)
    return ln


def sql_line(s, size=SQ_S):
    return paint_sql(Code(s, size=size, lang="sql"), s)


def sql_lines(size=SQ_S, top=2.2):
    """The twelve SQL lines as separate Codes, laid out exactly as the whole block (centred in x)."""
    full = Code("\n".join(SQL), size=size, line_spacing=0.72, lang="sql")
    full.move_to(ORIGIN).align_to([0, top, 0], UP)
    out = []
    for i, s in enumerate(SQL):
        ln = sql_line(s, size).move_to(full.line(i).get_center())
        out.append(ln)
    return out


def cypher_block(size=CY_S, src=S35.Q3):
    cy = S35.paint(Code(src, size=size))
    for sub, col in (("(p1:Person)", PINK), ("(p2:Person)", PINK), ("(m:Movie)", BLUE),
                     ("-[:ACTED_IN]->", YELLOW), ("<-[:ACTED_IN]-", YELLOW)):
        if sub in src:
            cy.find(sub).set_color(col)
    return cy


def band(i, j, top=3.28, left=None):
    """Cypher lines i..j-1 (verbatim, indentation kept) in the top band."""
    b = cypher_block(CY_S, "\n".join(CYL[i:j]))
    b.move_to(ORIGIN).align_to([0, top, 0], UP)
    if left is not None:
        b.align_to([left, 0, 0], LEFT)
    return b


def vtx(text, color, at, r=0.42, size=30):
    circ = Circle(radius=r, color=color, stroke_width=4).set_fill(color, 0.12).move_to(at)
    lab = T(text, size=size, slant=ITALIC).move_to(circ)
    v = VGroup(circ, lab)
    v.circ, v.lab = circ, lab
    return v


def yarrow(a, b, color=YELLOW, width=4):
    return Arrow(a.circ.get_center(), b.circ.get_center(), buff=a.circ.radius + 0.06, stroke_width=width,
                 color=color, max_tip_length_to_length_ratio=0.2)


def drawing(y=2.15, x0=-5.95, pitch=2.1, r=0.42, size=30):
    p1 = vtx("p1", PINK, [x0, y, 0], r, size)
    m = vtx("m", BLUE, [x0 + pitch, y, 0], r, size)
    p2 = vtx("p2", PINK, [x0 + 2 * pitch, y, 0], r, size)
    e1, e2 = yarrow(p1, m), yarrow(p2, m)
    g = VGroup(e1, e2, p1, m, p2)
    g.p1, g.m, g.p2, g.e1, g.e2 = p1, m, p2, e1, e2
    return g


ALL_ROWS = TOP5 + STONE + SELF


def col_layout(size, gap):
    hdr = ["name1", "name2", "movies"]
    widths = [max([Mono(hdr[j], size=size).width] + [Mono(r[j], size=size).width for r in ALL_ROWS])
              for j in range(3)]
    xs, acc = [], 0.0
    for w in widths:
        xs.append(acc)
        acc += w + gap
    return widths, xs, acc - gap


def result_table(left, top, n, size=27, pitch=0.5, gap=0.45):
    """cypher-shell look (ch3 s5): DIM header, rule, column lines; fixed columns for every row set.
    Returns (head, place) where place(rows, color=None) builds the row block."""
    widths, xs, total = col_layout(size, gap)
    xs = [left + x for x in xs]
    hdr = VGroup()
    for j, h in enumerate(["name1", "name2", "movies"]):
        t = Mono(h, size=size, color=DIM)
        cx = xs[j] + widths[j] / 2 if j == 2 else xs[j] + t.width / 2
        hdr.add(t.move_to([cx, top, 0]))
    rule = Line([left - 0.15, top - 0.32, 0], [left + total + 0.15, top - 0.3, 0], color=DIM, stroke_width=2)
    bottom = top - 0.72 - pitch * (n - 1) - 0.27
    seps = [Line([xs[j] - gap / 2, top + 0.22, 0], [xs[j] - gap / 2, bottom, 0], color=DIM, stroke_width=2)
            for j in (1, 2)]
    head = VGroup(hdr, rule, *seps)

    def place(rows, color=None):
        block = VGroup()
        for i, r in enumerate(rows):
            y = top - 0.72 - pitch * i
            row = VGroup()
            for j, v in enumerate(r):
                col = color or (GOLD if j == 2 else FG)
                t = Mono(v, size=size, color=col)
                cx = xs[j] + widths[j] / 2 if j == 2 else xs[j] + t.width / 2
                row.add(t.move_to([cx, y, 0]))
            block.add(row)
        return block
    head.right = left + total
    return head, place


def dashed_route(points, color=YELLOW):
    pts = [np.array([x, y, 0.0]) for x, y in points]
    path = VMobject().set_points_as_corners(pts)
    d = DashedVMobject(path, num_dashes=46, dashed_ratio=0.55).set_stroke(color, 3)
    tip = Triangle().set_fill(color, 1).set_stroke(width=0).scale(0.1)
    tip.move_to(pts[-1] + 0.05 * DOWN)
    return d, tip


def sp_grid():
    """South Park: Bigger, Longer & Uncut as s4's edge grid; the count is placed by the scene."""
    g = S64.edge_grid(MATT, TREY, "Matt Stone", "Trey Parker")
    g.remove(g.count)
    labs = VGroup(*[T(t, size=30).move_to(old) for t, old in zip(TREY, g.col_labels)])
    g.remove(g.col_labels)
    g.col_labels = labs
    g.add(labs)
    g.col_title.next_to(g.col_labels, UP, buff=0.18)
    g.shift([-g.get_x(), 1.7 - g.block.get_top()[1], 0])
    return g


def recap_tile():
    """Static: each pattern piece with an arrow into the SQL line it becomes."""
    srcs = [("-[:ACTED_IN]->", YELLOW), ("<-[:ACTED_IN]-", YELLOW), ("(p1:Person)", PINK),
            ("(p2:Person)", PINK), ("implicit", YELLOW)]
    lines = ["FROM     has_position AS h1", "JOIN     has_position AS h2 ON …",
             "JOIN     people AS p1 ON …", "JOIN     people AS p2 ON …", "GROUP BY p1.name, p2.name"]
    rows = VGroup()
    for (s, col), ln in zip(srcs, lines):
        if s == "implicit":
            a = T("(implicit)", size=30, color=YELLOW, slant=ITALIC)
        else:
            a = Mono(s, size=28, color=col)
        b = Code(ln, size=28, lang="sql")
        paint_sql(b, ln)
        if "…" in ln:
            b.find("…").set_color(DIM)
        rows.add(VGroup(a, b))
    xa, xb = -5.4, -1.4
    for i, r in enumerate(rows):
        y = 1.6 - 0.8 * i
        r[0].move_to([0, y, 0]).align_to([xa + 3.0, 0, 0], RIGHT)
        r[1].move_to([0, y, 0]).align_to([xb, 0, 0], LEFT)
    arrows = VGroup(*[Arrow(r[0].get_right(), r[1].get_left(), buff=0.15, stroke_width=4,
                            color=src[1], max_tip_length_to_length_ratio=0.25)
                      for r, src in zip(rows, srcs)])
    arrows[-1] = DashedVMobject(arrows[-1], num_dashes=8)
    g = VGroup(rows, arrows)
    g.move_to(ORIGIN)
    return g


# ---------------------------------------------------------------- scene
class CoStarsInSql(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c6.sql.1
    def clip1(self):
        cards = S57.exercise_cards().scale(1.2).move_to(ORIGIN)
        panel = S57.exercise_panel("21")
        card = cards[3]
        bars = S61.pause_icon().next_to(panel.title, RIGHT, buff=0.45)
        self.panel, self.bars = panel, bars
        with self.say("c6.sql.1") as c:
            self.play(*appear(*cards, shift=None, lag=0.05), run_time=0.4)  # early: the card row, as in s2–s4
            self.play(*during([ReplacementTransform(card.box.copy(), panel.frame)], 0, 0.7),
                      *during(disappear(*cards), 0, 0.5),
                      *during(appear(panel.title), 0.5, 1), run_time=1.2)
            c.wait_until(own_word=panel.question[0])
            self.play(*appear(panel.qgrp, shift=0.15 * DOWN), run_time=1.0)  # early: the card's question is shown whole
            c.wait_until("stop")
            self.play(*appear(bars, shift=None), run_time=0.6)

    # ------------------------------------------------------------ c6.sql.2
    def clip2(self):
        panel = self.panel
        hero = cypher_block(28).move_to([0, -0.45, 0])
        dr = drawing(y=2.45, x0=-2.4, pitch=2.4, r=0.45)
        b_match, b_where, b_ret, b_order = band(0, 2), band(2, 3), band(3, 5), band(5, 7)
        L = sql_lines()
        self.L = L
        tag_target = panel.title.copy().scale(0.6).to_corner(UL, buff=0.5)
        self.tag = panel.title

        # one has_position row, and the edge it becomes
        hp = VGroup(*[Mono(s, size=28, color=DIM) for s in ("person_id", "movie_id", "position")])
        vals = VGroup(Mono("nm0000122", size=30), Mono("tt0012349", size=30),
                      Mono("'actor'", size=30, color=YELLOW))
        for k, (h, v) in enumerate(zip(hp, vals)):
            x = -3.3 + 3.3 * k
            h.move_to([x, 0.75, 0])
            v.move_to([x, 0.15, 0])
        box = RoundedRectangle(corner_radius=0.12, width=11.4, height=2.0).set_stroke(BLUE, 3) \
            .set_fill(BLUE, 0.06).move_to([0, 0.75, 0])
        title = T("has_position", size=32, color=BLUE).next_to(box.get_corner(UL), DR, buff=0.18)
        hp.shift(0.15 * DOWN)
        pv = vtx("", PINK, [-3.3, -1.75, 0], r=0.42)
        mv = vtx("", BLUE, [0.0, -1.75, 0], r=0.42)
        pid = Mono("nm0000122", size=28).next_to(pv.circ, DOWN, buff=0.15)
        mid_ = Mono("tt0012349", size=28).next_to(mv.circ, DOWN, buff=0.15)
        earr = yarrow(pv, mv, width=5)
        elab = Mono(":ACTED_IN", size=28, color=YELLOW).next_to(earr, UP, buff=0.12)

        with self.say("c6.sql.2", gap=1.5) as c:
            self.play(*during(disappear(panel.frame, panel.qgrp, self.bars), 0, 0.45),
                      *during([panel.title.animate.become(tag_target)], 0.15, 0.7),
                      *during(appear(dr, hero, shift=None, lag=0.2), 0.5, 1),  # early: the query this exercise translates
                      run_time=1.8)
            c.wait_until("in part one")
            self.play(*during(disappear(dr), 0, 0.4), *during(edit(hero, b_match), 0.3, 1), run_time=1.5)
            self.play(*appear(box, title, hp, vals, shift=None, lag=0.15), run_time=1.0)  # early: one row, shown whole
            c.wait_until("came from")
            self.play(GrowFromCenter(pv.circ), GrowFromCenter(mv.circ),
                      *during(fly(vals[0], pid), 0.1, 1), *during(fly(vals[1], mid_), 0.2, 1),
                      run_time=1.6)
            c.wait_until("whose position")
            self.play(GrowArrow(earr), FlashAround(vals[2], run_time=1.5, time_width=1.5),
                      *during(appear(elab), 0.4, 1), run_time=1.5)

            c.wait_until("two")
            self.play(*disappear(box, title, hp, vals, pv.circ, mv.circ, pid, mid_, earr, elab), run_time=0.8)
            self.play(FlashAround(b_match.find("-[:ACTED_IN]->"), run_time=1.4, time_width=1.5),
                      *appear(L[2], shift=None), run_time=1.4)
            c.wait_until("joined on")
            self.play(FlashAround(b_match.find("<-[:ACTED_IN]-"), run_time=1.5, time_width=1.5),
                      FlashAround(b_match.find("(m:Movie)"), color=BLUE, run_time=1.5, time_width=1.5),
                      *appear(L[3], shift=None), run_time=1.5)

            c.wait_until("people")
            self.play(*flash([b_match.find("(p1:Person)"), b_match.find("(p2:Person)")], color=PINK,
                             run_time=1.6, time_width=1.5),
                      *appear(L[4], L[5], shift=None, lag=0.4), run_time=1.6)

            c.wait_until("filter")
            self.play(*flash([b_match.find(":ACTED_IN", nth=0), b_match.find(":ACTED_IN", nth=1)],
                             run_time=1.4, time_width=1.5),
                      *appear(L[6], L[7], shift=None, lag=0.3), run_time=1.4)

            c.wait_until("less")
            self.play(*swap(b_match, b_where), run_time=1.2)
            self.play(FlashAround(b_where, color=FG, run_time=1.2, time_width=1.5),
                      *appear(L[8], shift=None), run_time=1.2)
            c.wait_until("carries over")
            self.play(*swap(b_where, b_ret), run_time=1.0)
            self.play(*appear(L[0], L[1], shift=None, lag=0.3), run_time=1.2)

            c.wait_until("group")
            self.play(*flash([b_ret.find("p1.name AS name1"), b_ret.find("p2.name AS name2")],
                             run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("without being told")
            lbl = T("implicit in Cypher", size=28, color=YELLOW, slant=ITALIC)
            lbl.next_to(L[9], RIGHT, buff=0.45)
            xg = L[0].get_left()[0] - 0.4
            yr = b_ret.line(0).get_y()
            route, tip = dashed_route([(L[9].get_left()[0] - 0.1, L[9].get_y()), (xg, L[9].get_y()),
                                       (xg, yr), (b_ret.get_left()[0] - 0.25, yr)])
            tip.rotate(-PI / 2).move_to([b_ret.get_left()[0] - 0.2, yr, 0])
            self.play(*appear(L[9], shift=None), *during([Create(route)], 0.3, 0.9),
                      *during([FadeIn(tip)], 0.85, 1),
                      *during(appear(lbl, shift=None), 0.3, 0.8),  # early: names what the dashed arrow shows
                      run_time=1.8)
            c.wait_until("in sequel")
            self.play(FlashAround(L[9], run_time=1.4, time_width=1.5),
                      *during(disappear(lbl, route, tip), 0, 0.4), *during(swap(b_ret, b_order), 0, 0.6),
                      *during(appear(L[10], L[11], shift=None, lag=0.3), 0.5, 1), run_time=1.6)

    # ------------------------------------------------------------ c6.sql.3
    def clip3(self):
        tag = self.tag
        c_head, c_place = result_table(-4.6, 2.9, 5)
        d_head, d_place = result_table(-4.6, -0.45, 5)
        c_body, d_body = c_place(TOP5), d_place(TOP5)
        c_lab = T("Cypher", size=32).move_to([-5.95, 2.9, 0])
        d_lab = T("DuckDB", size=32).move_to([-5.95, -0.45, 0])
        ticks = [check_mark(GREEN).scale(0.7).move_to([d_head.right + 0.45, r.get_y(), 0]) for r in d_body]
        x2 = sql_line(SQL[2]).move_to([0, 2.9, 0]).align_to([-6.28, 0, 0], LEFT)
        x3 = sql_line(SQL[3]).move_to([0, 2.4, 0]).align_to([-6.28, 0, 0], LEFT)
        y2 = sql_line(R2).move_to(x2).align_to(x2, LEFT)
        y3 = sql_line(R3).move_to(x3).align_to(x3, LEFT)
        s_body = d_place(STONE)

        with self.say("c6.sql.3") as c:
            sweep_clear(self, *appear(c_lab, c_head, c_body, d_lab, d_head, d_body, shift=None, lag=0.08),  # early: the two replies arrive whole
                        keep=[tag], run_time=1.8)
            self.play(*appear(*ticks, shift=None, lag=0.35), run_time=1.6)
            c.wait_until("roles")
            self.play(*during(disappear(c_lab, c_head, c_body, *ticks), 0, 0.45),
                      *during(appear(x2, x3, shift=None, lag=0.2), 0.5, 1), run_time=1.4)  # early: the lines the trap changes
            c.wait_until("join plays role")
            self.play(*edit(x2, y2), *edit(x3, y3), run_time=1.6)
            c.wait_until("stone")
            self.play(*swap(d_body, s_body), run_time=1.4)
            c.wait_until("they share only")
            self.play(FlashAround(s_body[0], color=GOLD, run_time=1.6, time_width=1.5), run_time=1.6)

            # the 3 x 3 grid (s4's edge grid)
            sp = T("South Park: Bigger, Longer & Uncut", size=36, color=BLUE).move_to([0, 3.2, 0])
            g = sp_grid()
            nine = g.count.copy().move_to([-3.2, -1.35, 0])
            eq = T("5 × 9 + 1 × 6 = 51", size=44, color=GOLD).move_to([2.6, -1.35, 0])
            sub = T("five films with 3 × 3 roles, one with 2 × 3", size=28, color=DIM).move_to([2.6, -1.95, 0])
            cap1 = T("plays_role: one row per character", size=32, t2c={"plays_role": RED})
            cap2 = T("has_position: one row per credit", size=32, t2c={"has_position": YELLOW})
            caps = VGroup(cap1, cap2).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([0, -2.95, 0])
            parts = [g.block, g.row_labels, g.col_labels, g.row_title, g.col_title]
            glyphs = [gl for row in g.glyphs for gl in row]
            c.wait_until("nine")
            sweep_clear(self, *appear(sp, *parts, shift=None, lag=0.1),  # early: the film and its two casts
                        keep=[tag], run_time=1.6)
            self.play(*appear(*glyphs, shift=None, lag=0.12), run_time=1.5)
            self.play(*appear(nine), run_time=1.0)
            c.wait_until("the same multiplying")
            self.play(*appear(eq, sub, lag=0.4), run_time=1.4)
            c.wait_until("plays role has")
            self.play(*appear(cap1, cap2, lag=0.5), run_time=1.5)

    # ------------------------------------------------------------ c6.sql.4
    def clip4(self):
        tag = self.tag
        w = [sql_line(SQL[i]) for i in (6, 7, 8)]
        for k, ln in enumerate(w):
            ln.move_to([0, 2.9 - 0.48 * k, 0]).align_to([-5.3, 0, 0], LEFT)
        strike = Line(w[2].get_left() + 0.12 * LEFT, w[2].get_right() + 0.12 * RIGHT, color=RED, stroke_width=5)
        head, place = result_table(-4.85, 0.9, 3)
        body = place(SELF, color=RED)

        dr = drawing(y=0.6, x0=1.6, pitch=2.2, r=0.5, size=34)
        e_lab = T("two different edges", size=32, color=GREEN).move_to([3.8, -0.7, 0])
        row = VGroup(Mono("nm0000168", size=28), Mono("tt0110912", size=28),
                     Mono("'actor'", size=28, color=YELLOW)).arrange(RIGHT, buff=0.35)
        rbox = RoundedRectangle(corner_radius=0.12, width=row.width + 0.5, height=0.8).set_stroke(BLUE, 3) \
            .set_fill(BLUE, 0.06)
        rcard = VGroup(rbox, row).move_to([-3.05, -0.2, 0])
        rt = T("has_position", size=30, color=BLUE).next_to(rbox, DOWN, buff=0.2).align_to(rbox, LEFT)
        loop = CurvedArrow(rbox.get_top() + 1.5 * RIGHT + 0.05 * UP, rbox.get_top() + 1.5 * LEFT + 0.05 * UP,
                           angle=0.75 * PI, color=RED, stroke_width=4)
        same = T("h1 = h2", size=34, color=RED, slant=ITALIC).next_to(loop, UP, buff=0.15)

        with self.say("c6.sql.4") as c:
            sweep_clear(self, *appear(*w, shift=None, lag=0.15),  # early: the WHERE block, shown whole
                        keep=[tag], run_time=1.6)
            c.wait_until("drop the")
            self.play(Create(strike), *set_alpha([w[2]], 0.4), run_time=1.0)
            c.wait_until("then the top pair")
            self.play(*appear(head, body, shift=None, lag=0.3), run_time=1.4)  # early: the reply, shown whole
            c.wait_until("paired with himself")
            self.play(FlashAround(body[0], color=RED, run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("reuse")
            sweep_clear(self, *appear(dr, shift=None), keep=[tag], run_time=1.6)
            c.wait_until("different edges")
            self.play(*flash([dr.e1, dr.e2], run_time=1.4, time_width=1.5), *appear(e_lab), run_time=1.4)
            c.wait_until("a join has")
            self.play(*appear(rcard, rt, shift=None, lag=0.2), run_time=1.0)  # early: the row the join reuses
            c.wait_until("pairs with itself")
            self.play(Create(loop), *during(appear(same), 0.5, 1), run_time=1.4)  # early: names the loop

    # ------------------------------------------------------------ c6.sql.5
    def clip5(self):
        tag = self.tag
        R = 0.78

        def person(lines, at):
            circ = Circle(radius=R, color=PINK, stroke_width=4).set_fill(PINK, 0.12).move_to(at)
            lab = VGroup(*[T(s, size=28) for s in lines]).arrange(DOWN, buff=0.06).move_to(circ)
            return circ, lab
        tud = person(["Alan", "Tudyk"], [-4.7, 1.6, 0])
        cw = [person(["Chris", "Williams"], [4.7, y, 0]) for y in (2.75, 0.45)]
        dodge = Circle(radius=0.28, color=BLUE, stroke_width=4).set_fill(BLUE, 0.12).move_to([0, 2.75, 0])
        froz = Circle(radius=0.28, color=BLUE, stroke_width=4).set_fill(BLUE, 0.12).move_to([0, 0.45, 0])
        d_t = T("Dodgeball: A True Underdog Story (2004)", size=28, color=BLUE).next_to(dodge, UP, buff=0.12)
        f_t = T("Frozen (2013)", size=28, color=BLUE).next_to(froz, DOWN, buff=0.12)

        def arr(a, b):
            a, b = np.array(a), np.array(b)
            u = (b - a) / np.linalg.norm(b - a)
            return Arrow(a + u * (R + 0.04), b - u * 0.32, buff=0, stroke_width=3, color=FG,
                         max_tip_length_to_length_ratio=0.12)
        a_td = arr(tud[0].get_center(), dodge.get_center())
        a_tf = arr(tud[0].get_center(), froz.get_center())
        a_cd = arr(cw[0][0].get_center(), dodge.get_center())
        a_cf = arr(cw[1][0].get_center(), froz.get_center())
        midp = np.array([4.7, 1.6, 0])
        a_cd2, a_cf2 = arr(midp, dodge.get_center()), arr(midp, froz.get_center())
        a_cd3, a_cf3 = a_cd.copy(), a_cf.copy()

        merged = Mono("Alan Tudyk │ Chris Williams │ 2", size=30, color=RED).move_to([0, -0.85, 0])
        split = VGroup(*[Mono("Alan Tudyk │ Chris Williams │ 1", size=30, t2c={"1": GOLD})
                         for _ in range(2)]).arrange(DOWN, buff=0.16).move_to([0, -0.95, 0])
        g_sql = Code(GROUP_IDS, size=27, lang="sql").move_to([0, -1.85, 0])
        g_sql.text.set_color(YELLOW)
        g_cy = S35.paint(Code(CY_IDS, size=27, line_spacing=0.85))
        g_cy.next_to(g_sql, DOWN, buff=0.15).align_to(g_sql, LEFT)
        g_cy.find("p1.person_id, p2.person_id").set_color(YELLOW)

        with self.say("c6.sql.5") as c:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=1.0)
            c.wait_until("tudyk")
            self.play(GrowFromCenter(tud[0]), *appear(tud[1], shift=None), run_time=1.0)
            c.wait_until("dodgeball")
            self.play(GrowArrow(a_td), GrowFromCenter(dodge), GrowFromCenter(cw[0][0]), GrowArrow(a_cd),
                      *during(appear(d_t, cw[0][1], shift=None, lag=0.3), 0.3, 1), run_time=1.5)  # early: names drawn with their circles
            c.wait_until("frozen")
            self.play(GrowArrow(a_tf), GrowFromCenter(froz), GrowFromCenter(cw[1][0]), GrowArrow(a_cf),
                      *during(appear(f_t, cw[1][1], shift=None, lag=0.3), 0.3, 1), run_time=1.4)  # early: names drawn with their circles

            c.wait_until("merged")
            (c1, l1), (c2, l2) = cw
            for m in (c1, c2, l1, l2):
                m.save_state()
            self.play(*during([c1.animate.move_to(midp), c2.animate.move_to(midp),
                               l1.animate.move_to(midp).set_opacity(0), l2.animate.move_to(midp),
                               Transform(a_cd, a_cd2), Transform(a_cf, a_cf2)], 0, 0.6),
                      *during(appear(merged), 0.6, 1), run_time=2.0)
            c.wait_until("ids")
            self.play(*appear(g_sql, g_cy, shift=None, lag=0.4), run_time=1.4)  # early: the grouping, in both languages
            c.wait_until("split again")
            self.play(*during([Restore(c1), Restore(c2), Restore(l1), Restore(l2),
                               Transform(a_cd, a_cd3), Transform(a_cf, a_cf3)], 0, 0.6),
                      *during(swap(merged, split), 0.3, 1), run_time=1.8)

            # compare: the pattern side of each query
            bm = band(0, 2, top=2.95, left=-6.28)
            Lc = sql_lines()
            dy = 1.85 - Lc[2].get_top()[1]
            for ln in Lc:
                ln.shift(dy * UP)
            show = Lc[2:10]
            c.wait_until("compare")
            sweep_clear(self, *appear(bm, *show, shift=None, lag=0.05), keep=[tag], run_time=1.8)  # early: both queries, whole
            br = Brace(bm, RIGHT, buff=0.2, color=GOLD)
            one = T("1 pattern line", size=30, color=GOLD).next_to(br, RIGHT, buff=0.2)
            c.wait_until("in cypher the pattern")
            self.play(GrowFromCenter(br), *appear(one, shift=None), run_time=1.2)
            labels = ["4 table references", "3 join conditions", "2 position filters", "GROUP BY written out"]
            spots = [(-6.2, -2.45), (0.6, -2.45), (-6.2, -3.05), (0.6, -3.05)]
            flashes = [
                [Lc[2].find("has_position AS h1"), Lc[3].find("has_position AS h2"),
                 Lc[4].find("people AS p1"), Lc[5].find("people AS p2")],
                [Lc[3].find("h2.movie_id = h1.movie_id"), Lc[4].find("p1.person_id = h1.person_id"),
                 Lc[5].find("p2.person_id = h2.person_id")],
                [Lc[6].find("h1.position = 'actor'"), Lc[7].find("h2.position = 'actor'")],
                [Lc[9]]]
            cues = ["four tables", "three conditions", "two filters", "group by you write"]
            for txt, (x, y), fl, cue in zip(labels, spots, flashes, cues):
                t = T(txt, size=32, color=GOLD).move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
                c.wait_until(cue)
                self.play(*flash(fl, color=GOLD, run_time=1.1, time_width=1.5),
                          *appear(t, shift=None), run_time=1.1)
            c.wait_until()
        self.wait(2.0)
