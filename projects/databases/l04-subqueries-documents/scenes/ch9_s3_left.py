"""Chapter 9, scene 3: Exercise 13, pair three (LEFT JOIN: ON vs WHERE). Clips c9.left.1 – c9.left.4.

Opens from empty on s2's growing database (r = (1, 10); s = (10, 99), (10, 5)) at s2's place, with
pair_code(3) beside it. (3, 30) goes into r's slot 3 (index 2; s4 later fills slot 2 with (2, NULL)).
Clip 2 builds the ON version's joined table under the first query; clip 3 moves to a full-width
ON | WHERE layout (the db leaves), builds the WHERE version's table, filters it, compares results and
shows a tiny counterexample; clip 4 states the rule, lines up pair 2's inner join, then the Annie Hall
callback. Ends empty.

EXPORTS (static, no updaters; `load_scene("ch9_s3_left").<name>()`):
- padded_row(): the joined row `3 | 30 | NULL | NULL` (Mono 28, NULLs PINK, a DIM bar between the r
  part and the s part), centred at ORIGIN, 3.43 wide; `.cells[0..3]`, `.bar`.
- recap_r3(): the padded row kept under ON (GREEN x, a ✓), dropped under WHERE (`= 99` + PINK `NULL`
  pill, the row at 0.4 with a RED strike), BLUE "ON" / "WHERE" headers above; ~12.4 wide, 1.3 tall,
  centred at ORIGIN; `.on` `.where` (each VGroup(head, row, ...)).
- jrow(vals, x0, y): a joined-table row whose x-column is centred at x0 (columns at +0, 0.7, 1.73, 2.85).
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

S2 = load_scene("ch9_s2_pairs")
R8 = load_scene("ch3_s8_recap")
SCH = S2.SCH

JDX = (0.0, 0.7, 1.73, 2.85)     # column centres of a joined row, from the x column
BAR_DX = 1.17
EQ_DX, PILL_DX = 3.5, 4.63         # "= 99" and the verdict pill (left edges)
HY = 0.55                          # joined-table header y
RY = (0.05, -0.45, -0.95)          # joined-table rows
X1A = -0.88                        # table 1 beside the db (under query a)
X1B = -6.43                        # table 1 in the ON half
X2 = 0.42                          # table 2 in the WHERE half
B_LEFT, A_LEFT, Q2_TOP = 0.3, -6.55, 2.85
RES_TOP = -1.45
R1_X, R2_X = X1B + 1.6, X2 + 1.6
NE_X = (R1_X + R2_X) / 2


def jrow(vals, x0, y, size=28):
    cells = VGroup(*[S2.value_text(v, size).move_to([x0 + dx, y, 0]) for dx, v in zip(JDX, vals)])
    bar = Line([x0 + BAR_DX, y - 0.22, 0], [x0 + BAR_DX, y + 0.22, 0]).set_stroke(DIM, 1.5)
    g = VGroup(cells, bar)
    g.cells, g.bar = cells, bar
    return g


def jhead(x0, y):
    cols = VGroup(*[SCH._placed(c, 28, DIM, NORMAL, y, cx=x0 + dx)[0] for dx, c in zip(JDX, "xyyz")])
    bar = Line([x0 + BAR_DX, y - 0.2, 0], [x0 + BAR_DX, y + 0.2, 0]).set_stroke(DIM, 1.5)
    rule = Line([x0 - 0.3, y - 0.26, 0], [x0 + 3.55, y - 0.26, 0]).set_stroke(DIM, 1.5)
    return VGroup(cols, bar, rule)


def test_marks(x0, y, word, color):
    eq = Mono("= 99", 28, color)
    eq.move_to([x0 + EQ_DX, y, 0], aligned_edge=LEFT)
    p = S2.paint(S2.pill(word, color), color)
    p.move_to([x0 + PILL_DX, y, 0], aligned_edge=LEFT)
    return eq, p


def mini_table(name, rows=()):
    w, h = 1.4, 1.25
    box = Rectangle(width=w, height=h).set_stroke(BLUE, 2.5)
    title = Mono(name, 28, weight=BOLD).move_to(box.get_top() + 0.27 * DOWN)
    rule = Line(box.get_corner(UL) + 0.55 * DOWN, box.get_corner(UR) + 0.55 * DOWN).set_stroke(BLUE, 2)
    g = VGroup(box, rule, title)
    for vals in rows:
        y = box.get_top()[1] - 0.9
        g.add(*[Mono(str(v), 28).move_to([box.get_x() + dx, y, 0]) for dx, v in zip((-0.35, 0.3), vals)])
    return g


def inset():
    r = mini_table("r", [(3, 30)])
    s = mini_table("s")
    VGroup(r, s).arrange(RIGHT, buff=0.35)
    on = VGroup(Mono("ON", 28, BLUE), T("1 row", 30, GOLD)).arrange(RIGHT, buff=0.25)
    wh = VGroup(Mono("WHERE", 28, BLUE), T("0 rows", 30, GOLD)).arrange(RIGHT, buff=0.25)
    txt = VGroup(on, wh).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    body = VGroup(VGroup(r, s), txt).arrange(RIGHT, buff=0.6)
    box = RoundedRectangle(corner_radius=0.18, width=body.width + 0.6, height=body.height + 0.4).set_stroke(DIM, 2)
    box.move_to(body)
    g = VGroup(box, r, s, on, wh).move_to([0, -2.45, 0])
    g.box, g.r, g.s, g.on, g.wh = box, r, s, on, wh
    return g


def ann_rows(size=28):
    rows = VGroup()
    for k, (title, comp) in enumerate(R8.RESULT_1977):
        t = Mono(title, size)
        c = Mono(comp if comp else "null", size, color=FG if comp else PINK)
        t.move_to([0, -k * 0.55, 0], aligned_edge=LEFT)
        c.move_to([t.get_left()[0] + 8.4, -k * 0.55, 0], aligned_edge=LEFT)
        rows.add(VGroup(t, c))
    return rows


ANN_A = "LEFT JOIN has_position AS hp\n  ON … AND hp.position = 'composer'\nWHERE …"
ANN_B = "LEFT JOIN has_position AS hp\n  ON …\nWHERE … AND hp.position = 'composer'"


# ---------------------------------------------------------------- exports
def padded_row():
    g = jrow((3, 30, None, None), 0, 0)
    g.shift(-g.get_center())
    return g


def recap_r3():
    on_row = jrow((3, 30, None, None), -5.6, 0)
    on_row.cells[0].set_color(GREEN)
    ok = check_mark().next_to(on_row, RIGHT, buff=0.4)
    on_h = Mono("ON", 30, BLUE).move_to([on_row.get_x(), 0.75, 0])
    wh_row = jrow((3, 30, None, None), 0.6, 0)
    eq, p = test_marks(0.6, 0, "NULL", PINK)
    wh_h = Mono("WHERE", 30, BLUE).move_to([VGroup(wh_row, p).get_x(), 0.75, 0])
    wh_row.set_opacity(0.4)
    cut = S2.strike(wh_row)
    on = VGroup(on_h, on_row, ok)
    wh = VGroup(wh_h, wh_row, eq, p, cut)
    g = VGroup(on, wh)
    g.shift(-g.get_center())
    g.on, g.where = on, wh
    return g


class Ch9S3Left(NarratedScene):
    def construct(self):
        self.ask()
        self.grow()
        self.where()
        self.rule()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c9.left.1
    def ask(self):
        with self.say("c9.left.1") as c:
            d = S2.db([(1, 10)], [(10, 99), (10, 5)])
            st = S2.strip(3)
            self.d, self.st = d, st
            self.play(*appear(d.r, d.s, st, lag=0.25, shift=None), run_time=min(1.2, c.until("pair3")))  # early: the tables' tags and the pair strip, read whole
            c.wait_until("pair3")
            q = S2.pair_code(3)
            self.q = q
            self.play(*appear(q.a, q.b, lag=0.3, shift=None), run_time=min(1.4, c.until("left join")))
            c.wait_until("left join")
            lj = [q.a.find("LEFT JOIN"), q.b.find("LEFT JOIN")]
            self.play(*recolor(lj[0], YELLOW), *recolor(lj[1], YELLOW),
                      *flash(lj, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("ask")
            mid = (q.a.get_bottom()[1] + q.b.get_top()[1]) / 2
            qm = T("?", 60, YELLOW).move_to([4.6, mid, 0])
            self.play(*appear(qm), run_time=0.9)
            c.wait_until("yes")
            ne = MathTex(r"\neq", font_size=72, color=RED).move_to(qm)
            self.ne = ne
            self.play(*swap(qm, ne), run_time=min(1.0, c.until()))

    # ------------------------------------------------------------ c9.left.2
    def grow(self):
        d, q = self.d, self.q
        with self.say("c9.left.2") as c:
            ins = S2.insert_code("INSERT INTO r VALUES\n  (3, 30);")
            self.play(*appear(ins, shift=None), run_time=0.8)
            row = d.r.make_row(2, (3, 30))
            self.play(*flash([ins.find("3"), ins.find("30")]),
                      *during(appear(row, shift=0.4 * DOWN), 0.3, 1), run_time=1.3)
            settle(self, d.r, add=[row])
            d.r.rows[2] = row
            self.play(FlashAround(row, color=YELLOW, run_time=1.0, time_width=1.5), run_time=1.0)
            # the search in s finds nothing
            c.wait_until("No row of the second")
            p0 = d.r.cell(2, 1).get_right() + 0.15 * RIGHT
            p1 = np.array([d.s.col_x(0) - 0.3, d.s.slot_y(2), 0])
            dash = DashedLine(p0, p1, dash_length=0.12).set_stroke(YELLOW, 3)
            self.play(Create(dash), run_time=1.2)
            xm = cross_mark().scale(0.75).move_to(p1 + 0.3 * RIGHT)
            c.wait_until("equal to thirty")
            self.play(*appear(xm, shift=None), run_time=0.8)
            # {on}: the first query's joined table
            c.wait_until("on")
            head1 = jhead(X1A, HY)
            self.head1 = head1
            self.play(*during(disappear(ins, q.b, self.ne), 0, 0.45),
                      *during(appear(head1, shift=None), 0.5, 1), run_time=1.4)
            c.wait_until("part of the matching")
            on_g = [q.a.find("ON r.y = s.y"), q.a.find("AND s.z = 99")]
            self.play(*recolor(on_g[1], YELLOW), FlashUnder(on_g[0], run_time=1.3, time_width=1.5),
                      FlashUnder(on_g[1], run_time=1.3, time_width=1.5), run_time=1.3)
            # {match}: 1 meets the 99 row
            c.wait_until("match")
            ml = Line(d.r.cell(0, 1).get_right() + 0.1 * RIGHT,
                      d.s.cell(0, 0).get_left() + 0.1 * LEFT).set_stroke(GREEN, 4)
            self.ml = ml
            self.play(Create(ml), *recolor(d.s.rows[0], GREEN), *recolor(d.r.rows[0], GREEN),
                      *set_alpha([d.s.rows[1]], DIMMED), run_time=1.2)
            j0 = jrow((1, 10, 10, 99), X1A, RY[0])
            self.play(*appear(j0, shift=None), run_time=min(1.0, c.until("pad")))
            # {pad}: 3 finds none, kept anyway
            c.wait_until("pad")
            j1 = jrow((3, 30, None, None), X1A, RY[1])
            self.play(*during(disappear(dash, xm), 0, 0.5), FlashAround(row, color=YELLOW, run_time=1.2),
                      *during(appear(j1.cells[0], j1.cells[1], j1.bar, shift=None), 0.3, 1), run_time=1.2)
            c.wait_until("padded with nulls")
            nulls = [j1.cells[2], j1.cells[3]]
            self.play(*appear(*nulls, lag=0.2, shift=None),
                      *during(flash(nulls, color=PINK), 0.4, 1), run_time=1.3)
            settle(self, j1)
            self.j0, self.j1 = j0, j1
            # {res1}
            c.wait_until("res1")
            r1 = S2.place_top(S2.result_card([1, 3]), 3.6, 0.75)
            r1.vals.set_color(GREEN)
            self.r1 = r1
            self.play(*appear(r1, shift=None), *recolor(j0.cells[0], GREEN), *recolor(j1.cells[0], GREEN),
                      run_time=min(1.4, c.until()))

    # ------------------------------------------------------------ c9.left.3
    def where(self):
        d, q = self.d, self.q
        with self.say("c9.left.3") as c:
            a = q.a
            ul = a.get_corner(UL)
            dx = (X1B - X1A) * RIGHT
            r1 = self.r1
            r1_to = np.array([R1_X - r1.box.get_x(), RES_TOP - r1.box.get_top()[1], 0])
            self.play(*disappear(d.r, d.s, self.ml), run_time=0.7)
            self.play(*during([a.animate.scale(30 / 34, about_point=ul).shift(np.array([A_LEFT, Q2_TOP, 0]) - ul),
                               self.head1.animate.shift(dx), self.j0.animate.shift(dx),
                               self.j1.animate.shift(dx)], 0.3, 1),
                      *during([r1.animate.shift(r1_to)], 0.55, 1), run_time=1.4)
            b2 = Code(S2.PAIR_SRC[3][1], size=30)
            b2.shift(np.array([B_LEFT, Q2_TOP, 0]) - b2.get_corner(UL))
            b2.find("LEFT JOIN").set_color(YELLOW)
            head2 = jhead(X2, HY)
            self.b2 = b2
            self.play(*appear(b2, head2, lag=0.3, shift=None), run_time=1.0)
            c.wait_until("matches on why alone")
            self.play(FlashUnder(b2.find("ON r.y = s.y"), run_time=1.2, time_width=1.5), run_time=1.2)
            # the joined table on y alone
            c.wait_until("One matches both rows")
            t0 = jrow((1, 10, 10, 99), X2, RY[0])
            t1 = jrow((1, 10, 10, 5), X2, RY[1])
            t2 = jrow((3, 30, None, None), X2, RY[2])
            self.play(*fly(self.j0, t0, arc=0.0), *during(appear(t1, shift=None), 0.5, 1), run_time=1.5)
            c.wait_until("three is padded")
            self.play(*fly(self.j1, t2), run_time=1.3)
            # {filter}: WHERE tests every row
            c.wait_until("filter")
            wh = b2.find("WHERE s.z = 99")
            bar = Rectangle(width=6.75, height=0.5).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12)
            bar.set_z_index(-1).move_to([X2 - 0.35 + 6.75 / 2, RY[0], 0])
            self.play(*recolor(wh, YELLOW), FlashUnder(wh, run_time=1.2, time_width=1.5), FadeIn(bar),
                      run_time=1.2)
            rows = [t0, t1, t2]
            verdicts = [("TRUE", GREEN), ("FALSE", RED), ("NULL", PINK)]
            marks = []
            for k, cue in enumerate(("every row", "Five fails", "null equals")):
                c.wait_until(cue)
                eq, p = test_marks(X2, RY[k], *verdicts[k])
                marks.append((eq, p))
                col = verdicts[k][1]
                anims = [*recolor(rows[k].cells[3], col), *during(appear(eq, p, lag=0.3, shift=None), 0.3, 1)]
                if k:
                    anims.append(during([bar.animate.move_to([bar.get_x(), RY[k], 0])], 0, 0.45)[0])
                self.play(*anims, run_time=1.2)
            # {drop}: the RED and PINK rows fall away
            c.wait_until("drop")
            gone = [t1, t2, *marks[1], *marks[2]]
            self.play(*[FadeOut(m, shift=0.6 * DOWN) for m in gone], FadeOut(bar), run_time=0.9)
            # {res2}
            c.wait_until("res2")
            r2 = S2.place_top(S2.result_card([], slots=1), R2_X, RES_TOP)
            one = S2.value_text(1).set_color(GREEN).move_to(r2.slot_pos(0))
            self.play(*during(appear(r2, shift=None), 0, 0.5), *recolor(t0.cells[0], GREEN),
                      *during(fly(t0.cells[0], one), 0.3, 1), run_time=1.4)
            settle(self, r2, add=[one])
            c.wait_until("just one")
            ne2 = MathTex(r"\neq", font_size=72, color=RED).move_to([NE_X, r2.slot_pos(0)[1], 0])
            self.play(*appear(ne2, shift=None), run_time=0.9)
            self.r2, self.ne2 = r2, ne2
            # {tiny}: one row in r, s empty
            c.wait_until("tiny")
            ins = inset()
            self.play(*disappear(self.head1, self.j0, self.j1, head2, t0, *marks[0]), run_time=0.8)
            up = (0.75 - RES_TOP) * UP
            self.play(*during([self.r1.animate.shift(up), r2.animate.shift(up), ne2.animate.shift(up)], 0, 0.5),
                      *during(appear(ins.box, ins.r, ins.s, lag=0.2, shift=None), 0.5, 1), run_time=1.5)
            c.wait_until("empty")
            self.play(*appear(ins.on, ins.wh, lag=0.4, shift=None), run_time=min(1.2, c.until()))
            settle(self, ins)
            self.ins = ins

    # ------------------------------------------------------------ c9.left.4
    def rule(self):
        a, b2 = self.q.a, self.b2
        with self.say("c9.left.4") as c:
            cap_on = T("ON: which rows of s match", 30, t2c={"ON:": BLUE})
            cap_on.move_to([0, 0, 0]).align_to([A_LEFT, 0, 0], LEFT).align_to(a.get_bottom() + 0.45 * DOWN, UP)
            self.play(*disappear(self.r1, self.r2, self.ne2), run_time=0.8)
            self.play(*appear(cap_on), run_time=1.0)
            cap_on2 = T("every row of r survives", 30, GREEN).next_to(cap_on, DOWN, buff=0.25, aligned_edge=LEFT)
            c.wait_until(own_word=cap_on2)
            self.play(*appear(cap_on2), run_time=1.0)
            cap_wh = T("WHERE: runs after the padding,\ncan drop rows", 30, t2c={"WHERE:": BLUE})
            cap_wh.align_to([B_LEFT, 0, 0], LEFT).align_to(cap_on, UP)
            c.wait_until(own_word=cap_wh)
            self.play(*during(disappear(self.ins), 0, 0.5), *during(appear(cap_wh), 0.3, 1), run_time=1.3)
            # {inner}: WHERE turns it back into pair 2's inner join
            c.wait_until("inner")
            wh = b2.find("WHERE s.z = 99")
            self.play(*disappear(a, cap_on, cap_on2), FlashUnder(wh, run_time=1.2, time_width=1.5), run_time=1.2)
            inner = Code(S2.PAIR_SRC[2][1], size=30).set_color(DIM)
            inner.shift(np.array([A_LEFT, Q2_TOP, 0]) - inner.get_corner(UL))
            eq = MathTex("=", font_size=72, color=GREEN).move_to([(inner.get_right()[0] + B_LEFT) / 2, b2.get_y(), 0])
            self.play(*appear(inner, shift=0.8 * RIGHT), run_time=1.3)
            c.wait_until("turns")
            self.play(*appear(eq, shift=None), run_time=0.9)
            lab = T("pair 2", 30, DIM).align_to([A_LEFT, 0, 0], LEFT).align_to(cap_on, UP)
            c.wait_until(own_word=lab)
            self.play(*appear(lab), run_time=min(0.9, c.until("annie")))
            # {annie}: the composer test moved into WHERE
            c.wait_until("annie")
            ann = Code(ANN_A, size=30).move_to([0, 1.45, 0])
            rows = ann_rows().move_to([0, -1.05, 0])
            sweep_clear(self, *during(appear(ann, *rows, lag=0.25, shift=None), 0.5, 1), keep=[self.st], run_time=1.6)
            c.wait_until("into where")
            ann2 = Code(ANN_B, size=30)
            ann2.shift(ann.get_corner(UL) - ann2.get_corner(UL))
            src = ann.find("AND hp.position = 'composer'", line=1)
            dst = ann2.find("AND hp.position = 'composer'", line=2)
            self.play(*[g.animate.move_to(t.get_center()) for g, t in zip(src, dst)], run_time=1.4)
            self.remove(*ann.get_family())
            self.add(ann2)
            c.wait_until("no composer")
            annie = rows[0]
            cut = Line(annie.get_left() + 0.15 * LEFT, annie.get_right() + 0.15 * RIGHT).set_stroke(RED, 5)
            self.play(Create(cut), *recolor(annie, RED), run_time=1.0)
            two = T("2 rows", 32, GOLD).next_to(rows, DOWN, buff=0.35).align_to(rows, RIGHT)
            c.wait_until("drops out")
            self.play(*appear(two), run_time=min(0.9, c.until()))
        self.wait(2.0)
