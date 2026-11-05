"""Chapter 2, scene 3: a subquery that returns a column, inside NOT IN. Clips c2.notin.1 – c2.notin.4.

Exports (static, built where they sit on screen):
- or_line() -> Code `year = 1927 OR year = 1931` (sql, size 30 scaled to 28), parked bottom-left
  (left edge x = -6.6, centre y = -3.5). s6 brings it back.
- notin_query() -> Code of slide 64's query (size 34, wrapped after `NOT IN`), centred at (0, 1.0).
- column_into_in() -> VGroup(.head, .column, .close, .check): `year IN (` + the 6-cell column +
  `)` (parens stretched to the column's height) + GREEN check, centred near (0, -1.75).
  `.label` ("is it a member?", T 32 GREEN) is built beside it but is NOT part of the group.
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

S2 = load_scene("ch2_s2_absent")
S1 = load_scene("ch2_s1_hook")
SCH = load_scene("ch1_s2_schema")
cell = S2.cell

EX_SRC = """SELECT title, year FROM movies
WHERE year IN (1927, 1931);"""
OR_SRC = "year = 1927 OR year = 1931"
NOTIN_SRC = """SELECT movie_id, title FROM movies
WHERE movie_id NOT IN
  (SELECT movie_id FROM plays_role);"""
IN_SRC = "year IN (1927, 1931)"

OR_BIG_POS = np.array([2.9, -1.05, 0])
IN_POS = np.array([-0.4, -1.75, 0])
COL_POS = np.array([1.2, 1.0, 0])
PAREN_H = 2.7
CARD_S = 28 / 24          # schema cards: column names at size 28


# ---------------------------------------------------------------- exports
def or_line():
    """The parked OR line, bottom-left (s6 brings it back)."""
    code = Code(OR_SRC, 30, lang="sql").scale(28 / 30)
    code.move_to([0, -3.5, 0]).align_to([-6.6, 0, 0], LEFT)
    return code


def notin_query():
    return Code(NOTIN_SRC, 34, lang="sql").move_to([0, 1.0, 0])


def _in_code():
    return Code(IN_SRC, 48, lang="sql").move_to(IN_POS)


def column_into_in():
    code = _in_code()
    head = code.find("year IN (")
    opn = code.find("(")
    close = code.find(")")
    col = S1.shape_icon("column")
    col.move_to([0, IN_POS[1], 0]).next_to(head, RIGHT, buff=0.35)
    col.set_y(IN_POS[1])
    close.next_to(col, RIGHT, buff=0.35)
    for p in (opn, close):
        p.stretch_to_fit_height(PAREN_H)
        p.set_y(IN_POS[1])
    check = check_mark(GREEN).next_to(close, RIGHT, buff=0.55)
    label = T("is it a member?", 32, GREEN).next_to(check, RIGHT, buff=0.3)
    g = VGroup(head, col, close, check)
    g.head, g.open, g.column, g.close, g.check, g.label = head, opn, col, close, check, label
    return g


# ---------------------------------------------------------------- scene-local helpers
def example_result():
    """title | year: Metropolis 1927, City Lights 1931, M 1931 (left half)."""
    cols = [(-4.3, 2.8), (-2.2, 1.4)]
    heads = [Mono("title", 28, DIM).move_to([cols[0][0], -0.15, 0]),
             Mono("year", 28, DIM).move_to([cols[1][0], -0.15, 0])]
    rows = []
    for y, (t, yr) in zip([-0.75, -1.35, -1.95], [("Metropolis", 1927), ("City Lights", 1931), ("M", 1931)]):
        rows.append(VGroup(cell(T(t, 28), cols[0][1], center=[cols[0][0], y, 0]),
                           cell(T(str(yr), 28, GOLD), cols[1][1], center=[cols[1][0], y, 0])))
    return VGroup(*heads), rows


def notin_result():
    """movie_id | title: Flow, Kaiva (s2's GREEN result look), lower left."""
    RC = [(-4.2, 2.7), (-2.0, 1.7)]
    heads = [Mono("movie_id", 28, DIM).move_to([RC[0][0], -0.6, 0]),
             Mono("title", 28, DIM).move_to([RC[1][0], -0.6, 0])]
    rows = []
    for y, (mid, tt) in zip([-1.2, -1.8], [("tt4772188", "Flow"), ("tt27719898", "Kaiva")]):
        r = VGroup(cell(Mono(mid, 28), RC[0][1], color=GREEN, center=[RC[0][0], y, 0]),
                   cell(T(tt, 28), RC[1][1], color=GREEN, center=[RC[1][0], y, 0]))
        for m in r:
            m.rect.set_stroke(GREEN, 3)
        rows.append(r)
    return VGroup(*heads), rows


class NotInScene(NarratedScene):
    def construct(self):
        cap, flow, kaiva = S2.handover_shot()
        self.add(cap, flow, kaiva)
        self.cap, self.flow, self.kaiva = cap, flow, kaiva
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(3.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ clip 1: IN and its OR
    def clip1(self):
        with self.say("c2.notin.1") as c:
            big_in = Mono("IN", 96, BLUE).move_to([0, 0.3, 0])
            self.play(*appear(big_in), run_time=1.0)

            c.wait_until("example")
            q = Code(EX_SRC, 36, lang="sql").move_to([0, 1.25, 0])
            q_in = q.find("IN")
            others = [g for g in q.text if all(g is not h for h in q_in)]
            self.play(big_in.animate.scale(q_in.height / big_in.height).move_to(q_in.get_center()),
                      run_time=1.4)
            self.remove(big_in)
            for g in others:
                g.set_opacity(0)
            self.add(q)
            self.play(*[g.animate.set_opacity(1) for g in others], run_time=1.0)
            self.q = q

            c.wait_until("finds three movies")
            heads, rows = example_result()
            self.play(*appear(heads, shift=None), run_time=0.8)
            self.play(*appear(*rows, lag=0.35), run_time=1.6)
            self.ex_heads, self.ex_rows = heads, rows

            c.wait_until("or")
            cond = q.find("year IN (1927, 1931)")
            orl = Code(OR_SRC, 30, lang="sql").move_to(OR_BIG_POS)
            mid = Code(IN_SRC, 30, lang="sql").move_to(OR_BIG_POS)
            self.play(*fly(cond, mid), run_time=1.4)
            c.wait_until("year equals")
            self.play(*edit(mid, orl), run_time=1.6)
            self.orl = orl
            c.wait_until("or year")
            self.play(FlashUnder(orl.find("OR"), color=BLUE, time_width=1.5), run_time=1.2)

    # ------------------------------------------------------------ clip 2: three shapes
    def clip2(self):
        cap, flow, kaiva, orl = self.cap, self.flow, self.kaiva, self.orl
        with self.say("c2.notin.2") as c:
            park = or_line()
            sweep_clear(self, orl.animate.scale(28 / 30).move_to(park.get_center()),
                        keep=[cap, flow, kaiva, orl], run_time=1.4)

            pair = S1.corner_icons()
            self.play(*appear(pair, shift=None), run_time=0.9)  # early: part one's two shapes, recalled whole
            c.wait_until("a whole table")
            oc = S1.open_card()
            target = VGroup(VGroup(oc.grid, oc.labels[0]), VGroup(oc.cell, oc.labels[1]))
            self.play(Transform(pair, target), run_time=1.8)  # early: same icons, moving to the centre

            c.wait_until("column")
            column = S1.shape_icon("column").move_to(oc.column)
            seed = VGroup(*[row[0].copy() for row in pair[0][0]])
            self.play(ReplacementTransform(seed, column), run_time=1.8)
            col_lab = T("a column", 36).move_to(oc.labels[2])
            c.wait_until(own_word=col_lab)
            self.play(*appear(col_lab), run_time=1.0)

            c.wait_until("compare")
            rating = Code("rating >", 48, lang="sql")
            rating.move_to(COL_POS).align_to([0.6, 0, 0], RIGHT)
            self.play(*during(disappear(pair), 0, 0.45),
                      *during([column.animate.move_to(COL_POS),
                               col_lab.animate.move_to(COL_POS + 1.85 * DOWN)], 0.4, 1),
                      run_time=1.6)
            self.play(*appear(rating, shift=None), run_time=1.0)

            c.wait_until("Which of these")
            x = cross_mark().move_to(COL_POS + 0.95 * RIGHT)
            wv = T("which value?", 34, RED).next_to(x, RIGHT, buff=0.3)
            self.play(*appear(x, wv, lag=0.3), *flash([column], color=RED), run_time=1.3)

            c.wait_until("set")
            fin = column_into_in()
            code = _in_code()
            self.play(*set_alpha([rating, x, wv], DIMMED), *disappear(col_lab), *appear(code, shift=None),
                      run_time=1.2)
            lst = code.find("1927, 1931")
            opn, close = code.find("("), code.find(")")
            new_open, new_close = fin.open.copy(), fin.close.copy()
            self.play(*during([g.animate.set_opacity(0) for g in lst], 0, 0.3),
                      *during([MoveAlongPath(column, VMobject().set_points_as_corners(
                          [column.get_center(), [column.get_x(), fin.column.get_y(), 0],
                           fin.column.get_center()]))], 0.3, 0.75),
                      *during([opn.animate.set_opacity(0), close.animate.set_opacity(0)], 0.6, 0.8),
                      *during([FadeIn(new_open), FadeIn(new_close)], 0.7, 1),
                      run_time=1.9)
            # put the static export on screen in place of the animated pieces
            self.remove(*code.get_family(), column, new_open, new_close)
            self.add(fin.head, fin.column, fin.close)
            self.add(rating, x, wv)
            c.wait_until("whether")
            self.play(*appear(fin.check, fin.label, lag=0.3, shift=None), run_time=0.8)  # early: the line ends on "member"
        self.fin = fin

    # ------------------------------------------------------------ clip 3: NOT IN with a subquery
    def clip3(self):
        cap, flow, kaiva, orl = self.cap, self.flow, self.kaiva, self.orl
        with self.say("c2.notin.3") as c:
            q = notin_query()
            self.q = q
            fin = self.fin
            ins = [fin.head, fin.column, fin.close, fin.check, fin.label]
            sweep_clear(self, *appear(q, shift=None), keep=[cap, flow, kaiva, orl, *ins], run_time=1.6)
            self.play(FlashUnder(cap, color=YELLOW, time_width=1.5), run_time=1.3)

            c.wait_until("reads")
            ul = underline(q.find("NOT IN"), YELLOW)
            self.ul = ul
            self.play(GrowFromCenter(ul), run_time=1.0)

            c.wait_until("inner")
            sub = q.find("(SELECT movie_id FROM plays_role)")
            column = S1.shape_icon("column").move_to([4.8, -2.0, 0])
            box = SurroundingRectangle(sub, color=YELLOW, buff=0.08)
            self.sub_box = box
            self.play(*disappear(*ins), run_time=0.8)
            self.play(GrowFromCenter(box), run_time=0.8)
            ghost = box.copy()
            frame = Rectangle(width=column.width, height=column.height).set_stroke(YELLOW, 3)
            frame.move_to(column)
            self.play(Transform(ghost, frame), run_time=1.2)
            self.play(FadeIn(column), FadeOut(ghost), run_time=0.6)
            rows_lab = T("30,303 rows", 36, GOLD)
            rows_lab.move_to([0, -1.6, 0]).align_to([4.2, 0, 0], RIGHT)
            dist_lab = T("2,933 different movies", 30, DIM)
            dist_lab.move_to([0, -2.3, 0]).align_to([4.2, 0, 0], RIGHT)
            self.column, self.rows_lab, self.dist_lab = column, rows_lab, dist_lab
            c.wait_until("thirty thousand")
            self.play(*appear(rows_lab), run_time=1.0)
            c.wait_until("lots of repeats")
            self.play(*appear(dist_lab), run_time=1.0)

            c.wait_until("answer")
            heads, rows = notin_result()
            self.res_heads, self.res_rows = heads, rows
            self.play(*appear(heads, shift=None), run_time=0.7)
            self.play(*appear(*rows, lag=0.4), *flash([flow, kaiva], time_width=1.5), run_time=1.6)

            c.wait_until("english")
            self.play(FlashUnder(cap, color=YELLOW, time_width=1.5), run_time=1.3)

    # ------------------------------------------------------------ clip 4: Kaiva's ten actors
    def clip4(self):
        cap, kaiva, q = self.cap, self.kaiva, self.q
        with self.say("c2.notin.4") as c:
            self.play(*disappear(self.column, self.rows_lab, self.dist_lab, self.sub_box),
                      FlashAround(kaiva, time_width=1.5), FlashAround(self.res_rows[1], time_width=1.5),
                      run_time=1.4)

            m = SCH.schema_map()
            hp = m.cards["has_position"].copy().scale(CARD_S)
            hp.move_to([1.25, 0, 0]).align_to([0, -0.55, 0], UP)
            pr = m.cards["plays_role"].copy().scale(CARD_S)
            pr.move_to([4.9, 0, 0]).align_to([0, -0.55, 0], UP)
            ten = VGroup(T("10", 44, GOLD), T("actors", 30, DIM)).arrange(RIGHT, buff=0.2)
            ten.move_to([hp.get_x(), -3.4, 0])
            zero = VGroup(T("0", 44, GOLD), T("roles", 30, DIM)).arrange(RIGHT, buff=0.2)
            zero.move_to([pr.get_x(), -3.4, 0])
            for g in (ten, zero):
                g[1].align_to(g[0], DOWN)

            c.wait_until("has position")
            self.play(*appear(hp, shift=None), run_time=1.0)
            c.wait_until("ten actors")
            self.play(*appear(ten), run_time=1.0)

            c.wait_until("roles")
            self.play(*appear(pr, shift=None), run_time=1.0)
            self.play(*appear(zero), run_time=0.9)

            c.wait_until("plays role is the only")
            word = q.find("plays_role")
            arrow = Arrow(word.get_bottom() + 0.05 * DOWN, pr.get_top() + 0.05 * UP + 0.3 * LEFT,
                          buff=0.05, stroke_width=4, color=YELLOW,
                          max_tip_length_to_length_ratio=0.35)
            self.play(GrowArrow(arrow), *recolor(word, YELLOW),
                      SCH.card_alpha(hp, DIMMED), *set_alpha([ten], DIMMED), run_time=1.5)

            c.wait_until("exact")
            ans = T("it answered exactly what it was asked", 38, YELLOW).move_to([-0.7, 3.4, 0])
            self.play(*swap(cap, ans), run_time=1.3)
            self.wait(0.6)
            self.play(*disappear(hp, pr, ten, zero, arrow), *recolor(word, FG), run_time=1.0)
