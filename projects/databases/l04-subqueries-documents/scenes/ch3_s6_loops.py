"""Chapter 3, scene 6: two loops, one difference (semijoin and antijoin as nested loops). Clips c3.loops.1 – c3.loops.4.

Shared pieces (later scenes: `from lib.paths import load_scene; m = load_scene("ch3_s6_loops")`):
- `semi_code(size=26)` -> Code (python) of slide 67's semijoin loop as it ends here: the `append(person)`
  line and the `break  # at most one row per person` line YELLOW.
- `anti_code(size=26)` -> Code (python) of slide 67's antijoin loop: every `matched` and the `break` YELLOW.
Both are static, at ORIGIN.
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

JOIN_SRC = """results = []
for person in people:
    for credit in composer_credits:
        if credit["person_id"] == person["person_id"]:
            results.append((person, credit))"""
SEMI5_SRC = """results = []
for person in people:
    for credit in composer_credits:
        if credit["person_id"] == person["person_id"]:
            results.append(person)"""
SEMI_SRC = SEMI5_SRC + "\n            break         # at most one row per person"
ANTI_SRC = """results = []
for movie in movies:
    matched = False
    for role in plays_role:
        if role["movie_id"] == movie["movie_id"]:
            matched = True
            break
    if not matched:        # no match, so output it
        results.append(movie)"""

CODE_SIZE = 24
CODE_X, CODE_TOP = -4.65, 3.6


def _code(src, size=CODE_SIZE):
    return Code(src, size=size, lang="python")


def semi_code(size=CODE_SIZE):
    code = _code(SEMI_SRC, size)
    code.line(4).set_color(YELLOW)
    code.line(5).set_color(YELLOW)
    return code


def anti_code(size=CODE_SIZE):
    code = _code(ANTI_SRC, size)
    for k in range(3):
        code.find("matched", nth=k).set_color(YELLOW)
    code.find("break").set_color(YELLOW)
    return code


def _place_code(code):
    code.align_to([CODE_X, 0, 0], LEFT)
    code.align_to([0, CODE_TOP, 0], UP)
    return code


# ---------------------------------------------------------------- the loop picture (s2's, built larger)
ZID = "nm0001877"
PEOPLE_ROWS = [("A.R. Rahman",), None, ("Hans Zimmer",), None]
CC_ROWS = [None, ("nm0006246", "tt0169102"), (ZID, "tt0095953"), (ZID, "tt0103074"), (ZID, "tt0104694"), None]
Z_IDX = [2, 3, 4]
MOVIE_ROWS = [("The Kid",), None, ("Flow",)]
PR_ROWS = [None, ("tt0012349", "A Tramp"), ("tt0012349", "The Child")]

LSIZE, RSIZE = 30, 26
LEFT_X, CARD_X0, RES_X, RES_W = -6.45, -3.0, 4.55, 3.9


def _vdots(h=0.3):
    return MathTex(r"\vdots", color=DIM).set_height(h)


def _loop(left_title, left_rows, right_title, right_cols, right_rows, card_top, pitch=0.44, lpitch=0.6):
    """s2's loop picture: a left column (outer rows) and a BLUE card (the scanned table)."""
    loop = VGroup()
    # left column
    lt = Mono(left_title, LSIZE, weight=BOLD)
    hdr = 0.55
    lt.move_to([0, card_top - hdr / 2, 0]).align_to([LEFT_X, 0, 0], LEFT)
    width_all = max(Mono(r[0], LSIZE).width for r in left_rows if r)
    rows = []
    for i, r in enumerate(left_rows):
        y = card_top - hdr - 0.4 - i * lpitch
        if r is None:
            g = VGroup(_vdots(0.34).move_to([LEFT_X + 0.3, y, 0]))
        else:
            g = VGroup(Mono(r[0], LSIZE).move_to([0, y, 0]).align_to([LEFT_X, 0, 0], LEFT))
        rows.append(g)
    left = VGroup(lt, *rows)
    left.title, left.rows, left.width_all = lt, rows, width_all
    # card
    cw = [max([Mono(c, RSIZE).width] + [Mono(r[j], RSIZE).width for r in right_rows if r])
          for j, c in enumerate(right_cols)]
    pad, gap = 0.22, 0.36
    w = 2 * pad + sum(cw) + gap * (len(cw) - 1)
    heads_h = 0.46
    h = hdr + heads_h + pitch * len(right_rows) + 0.12
    x0 = CARD_X0
    cx = x0 + w / 2
    box = Rectangle(width=w, height=h).set_stroke(BLUE, 3).set_fill(BG, 0)
    box.move_to([cx, card_top - h / 2, 0])
    divider = Line([x0, card_top - hdr, 0], [x0 + w, card_top - hdr, 0]).set_stroke(BLUE, 2)
    title = Mono(right_title, LSIZE, weight=BOLD).move_to([cx, card_top - hdr / 2, 0])
    cxs = [x0 + pad]
    for ww in cw[:-1]:
        cxs.append(cxs[-1] + ww + gap)
    hy = card_top - hdr - heads_h / 2
    heads = VGroup(*[Mono(c, RSIZE, color=DIM).move_to([0, hy, 0]).align_to([cxs[j], 0, 0], LEFT)
                     for j, c in enumerate(right_cols)])
    y0 = card_top - hdr - heads_h - pitch / 2
    crow = []
    for i, r in enumerate(right_rows):
        y = y0 - i * pitch
        if r is None:
            g = VGroup(*[_vdots(0.28).move_to([cxs[j] + 0.3, y, 0]) for j in range(len(right_cols))])
        else:
            cells = []
            for j, s_ in enumerate(r):
                col = DIM if j == 1 else FG
                t = Mono(s_, RSIZE, color=col).move_to([0, y, 0]).align_to([cxs[j], 0, 0], LEFT)
                t._base_color = col
                cells.append(t)
            g = VGroup(*cells)
        crow.append(g)
    card = VGroup(box, divider, title, heads, *crow)
    card.box, card.title, card.rows, card.pitch = box, title, crow, pitch
    card.y_first, card.y_last = y0, y0 - (len(right_rows) - 1) * pitch
    loop.add(left, card)
    loop.left, loop.card = left, card

    def cursor_at(i):
        r = Rectangle(width=width_all + 0.4, height=0.54)
        r.set_stroke(YELLOW, 2.5).set_fill(YELLOW, 0.12).set_z_index(-1)
        r.move_to([LEFT_X + width_all / 2, rows[i].get_center()[1], 0])
        return r

    loop.cursor_at = cursor_at
    return loop


def _move_cursor(loop, i):
    return [Transform(loop.cursor, loop.cursor_at(i))]


def _sweep(loop, run_time=1.5):
    card = loop.card
    bar = Rectangle(width=card.box.width - 0.12, height=card.pitch)
    bar.set_stroke(width=0).set_fill(YELLOW, 0.22).set_z_index(-1)
    x, y0, y1 = card.box.get_center()[0], card.y_first, card.y_last
    bar.move_to([x, y0, 0])

    def upd(m, a):
        m.move_to([x, y0 + (y1 - y0) * a, 0])
        m.set_fill(YELLOW, max(0, 0.22 * min(1, a / 0.08, (1 - a) / 0.08)))

    return [UpdateFromAlphaFunc(bar, upd, run_time=run_time, rate_func=linear, remover=True)]


def _light(loop, idxs, color=YELLOW):
    return [cell.animate.set_color(color if color else getattr(cell, "_base_color", FG))
            for i in idxs for cell in loop.card.rows[i]]


def _results(bottom, w=RES_W, h=1.7):
    box = Rectangle(width=w, height=h).set_stroke(GREEN, 2.5)
    box.move_to([RES_X, bottom + h / 2, 0])
    title = Mono("results", LSIZE, weight=BOLD).move_to([RES_X, bottom + h - 0.28, 0])
    div = Line([RES_X - w / 2, bottom + h - 0.55, 0], [RES_X + w / 2, bottom + h - 0.55, 0]).set_stroke(GREEN, 2)
    g = VGroup(box, title, div)
    g.slot = np.array([RES_X, bottom + (h - 0.55) / 2, 0])
    return g


def _partial_sweep(loop, row_i):
    """A YELLOW bar runs down the card and stops on row row_i (it stays; fade it yourself)."""
    card = loop.card
    bar = Rectangle(width=card.box.width - 0.12, height=card.pitch)
    bar.set_stroke(width=0).set_fill(YELLOW, 0.22).set_z_index(-1)
    x = card.box.get_center()[0]
    y0, y1 = card.y_first, card.rows[row_i].get_center()[1]
    bar.move_to([x, y0, 0])

    def upd(m, a):
        m.move_to([x, y0 + (y1 - y0) * a, 0])
        m.set_fill(YELLOW, 0.22 * min(1, a / 0.08 if a < 0.08 else 1))

    return bar, UpdateFromAlphaFunc(bar, upd, rate_func=linear)


def _counter(tracker, pos, size=44, color=GOLD):
    m = Mono("0", size, color=color).move_to(pos)
    m.add_updater(lambda mob: mob.become(
        Mono(f"{int(round(tracker.get_value())):,}", size, color=color).move_to(pos)))
    return m


def _line_box(code, i):
    return token_box(code.line(i), code.line(i))


# ---------------------------------------------------------------- clip 4 pieces
def _pill(text, color, x, y, w, size=30, t2c=None):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=0.62).set_stroke(color, 2.5)
    r.move_to([x, y, 0])
    t = T(text, size, color, t2c=t2c or {}).move_to(r)
    return VGroup(r, t)


class Loops(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ the join loop
    def clip1(self):
        with self.say("c3.loops.1") as c:
            loop = _loop("people", PEOPLE_ROWS, "composer_credits", ("person_id", "movie_id"), CC_ROWS,
                         card_top=0.45)
            res = _results(loop.card.box.get_bottom()[1])
            self.loop, self.res = loop, res
            self.play(*appear(loop.left, loop.card, res, lag=0.3), run_time=1.6)  # early: the loop's shape shown whole first
            c.wait_until("nested loop join")
            code = _place_code(_code(JOIN_SRC))
            self.code = code
            self.play(*appear(code, shift=None), run_time=1.2)
            c.wait_until("outer")
            cur = loop.cursor_at(2)
            loop.cursor = cur
            box = _line_box(code, 1)
            self.box = box
            self.play(FadeIn(box), FadeIn(cur), run_time=1.0)
            c.wait_until("inner")
            self.play(Transform(box, _line_box(code, 2)), *_sweep(loop, 1.6), run_time=1.6)
            c.wait_until("match")
            self.play(Transform(box, _line_box(code, 3)), *_light(loop, Z_IDX), run_time=1.2)
            c.wait_until("append")
            tr = ValueTracker(0)
            num = _counter(tr, res.slot + LEFT * 0.45)
            lab = T("rows", 28, DIM).next_to(res.slot + RIGHT * 0.1, RIGHT, buff=0.0)
            lab.align_to(num, DOWN)
            self.play(Transform(box, _line_box(code, 4)), *appear(num, lab, shift=None), run_time=1.2)
            self.play(tr.animate.set_value(1), run_time=0.6)
            c.wait_until("zimmer")
            rt = max(1.0, min(2.7, c.until() - 0.1))
            self.play(Succession(*[_sweep(loop, rt / 3)[0] for _ in range(3)]),
                      tr.animate(rate_func=linear).set_value(72), run_time=rt)
            num.clear_updaters()
            self.count = VGroup(num, lab)

    # ------------------------------------------------------------ the semijoin
    def clip2(self):
        loop, code, box = self.loop, self.code, self.box
        with self.say("c3.loops.2") as c:
            semi5 = _place_code(_code(SEMI5_SRC))
            self.play(*during([FadeOut(box)], 0, 0.4), *during(disappear(self.count), 0, 0.4),
                      *during(_light(loop, Z_IDX, None), 0, 0.5),
                      *during(edit(code, semi5), 0.3, 1), run_time=1.8)
            c.wait_until("person")
            self.play(*recolor(semi5.line(4), YELLOW), FlashAround(semi5.line(4), run_time=1.2),
                      run_time=1.2)
            c.wait_until("break")
            semi = _place_code(_code(SEMI_SRC))
            semi.line(4).set_color(YELLOW)
            semi.find("break").set_color(YELLOW)
            self.play(*edit(semi5, semi), run_time=1.5)
            c.wait_until("first")
            bar, sw = _partial_sweep(loop, Z_IDX[0])
            self.play(sw, run_time=1.4)
            self.play(*_light(loop, [Z_IDX[0]]), run_time=0.8)
            c.wait_until("once")
            row = Mono("Hans Zimmer", 30, GREEN).move_to(self.res.slot)
            self.play(*recolor(loop.left.rows[2], GREEN), *appear(row), run_time=1.2)
            c.wait_until("skip")
            rest = [cell for i in Z_IDX[1:] + [5] for cell in loop.card.rows[i]]
            self.play(*set_alpha(rest, 0.3), run_time=1.2)
            c.wait_until("most")
            com = semi.find("# at most one row per person")
            self.play(*recolor(com, YELLOW), FlashUnder(com, run_time=1.5), run_time=1.5)
            self.semi, self.bar, self.row = semi, bar, row

    # ------------------------------------------------------------ the antijoin
    def clip3(self):
        old = self.loop
        with self.say("c3.loops.3") as c:
            anti = _place_code(anti_code())
            gone = [old.left, old.card, old.cursor, self.res, self.row, self.bar]
            self.play(*during(disappear(*gone), 0, 0.4), *during(edit(self.semi, anti), 0.3, 1), run_time=2.0)
            loop = _loop("movies", MOVIE_ROWS, "plays_role", ("movie_id", "role"), PR_ROWS,
                         card_top=-0.95, pitch=0.4, lpitch=0.5)
            res = _results(loop.card.box.get_bottom()[1], h=1.4)
            self.play(*appear(loop.left, loop.card, res, lag=0.3), run_time=1.2)  # early: the new loop's shape shown whole first
            self.loop, self.res, self.code = loop, res, anti
            c.wait_until("flag")
            cur = loop.cursor_at(0)
            loop.cursor = cur
            box = _line_box(anti, 2)
            self.box = box
            self.play(FadeIn(cur), FadeIn(box), run_time=1.0)
            self.play(FlashAround(anti.find("matched", nth=0), run_time=1.2), run_time=1.2)
            c.wait_until("scan")
            bar, sw = _partial_sweep(loop, 1)
            self.play(Transform(box, _line_box(anti, 3)), sw, run_time=1.5)
            self.play(*_light(loop, [1]), run_time=0.6)
            c.wait_until("it sets matched to true")
            self.play(Transform(box, _line_box(anti, 5)), run_time=0.8)
            c.wait_until("breaks")
            self.play(Transform(box, _line_box(anti, 6)), run_time=0.8)
            c.wait_until("kid")
            self.play(Transform(box, _line_box(anti, 7)), FadeOut(bar), *_light(loop, [1], None),
                      *recolor(loop.left.rows[0], DIM), run_time=1.2)
            c.wait_until("flow")
            self.play(*_move_cursor(loop, 2), Transform(box, _line_box(anti, 3)), run_time=1.0)
            tr = ValueTracker(0)
            top = res.get_top()[1]
            num = _counter(tr, [RES_X, top + 0.85, 0], size=40)
            lab = T("rows checked", 28, DIM).move_to([RES_X, top + 0.32, 0])
            self.play(*appear(num, lab, shift=None), run_time=0.5)
            rt = max(1.5, min(2.6, c.until("out") - 0.2))
            self.play(*_sweep(loop, rt), tr.animate(rate_func=linear).set_value(30303), run_time=rt)
            num.clear_updaters()
            c.wait_until("out")
            flow = Mono("Flow", 30, GREEN).move_to(res.slot)
            self.play(Transform(box, _line_box(anti, 8)), *recolor(loop.left.rows[2], GREEN),
                      *appear(flow), run_time=min(1.2, c.until(floor=0.8)))
            self.extra = [num, lab, flow, box]

    # ------------------------------------------------------------ inverses, and every row once
    def clip4(self):
        loop, anti = self.loop, self.code
        with self.say("c3.loops.4") as c:
            DS = 28
            semi_d = _code("results.append(person)\nbreak", DS).set_color(YELLOW)
            anti_d = _code("if not matched:\n    results.append(movie)", DS)
            anti_d.find("matched").set_color(YELLOW)
            semi_d.move_to([-3.6, 1.95, 0])
            anti_d.move_to([3.6, 1.95, 0])
            l_semi = T("EXISTS · semijoin", 32, GREEN).move_to([-3.6, 2.95, 0])
            l_anti = T("NOT EXISTS · antijoin", 32, GREEN).move_to([3.6, 2.95, 0])
            gone = [loop.left, loop.card, loop.cursor, self.res, *self.extra, anti]
            self.play(*during(disappear(*gone), 0, 0.4),
                      *during(appear(semi_d, anti_d, shift=None, lag=0.2), 0.5, 1), run_time=1.8)
            ax = (l_semi.get_right()[0] + l_anti.get_left()[0]) / 2
            arr = DoubleArrow([ax - 0.75, 2.95, 0], [ax + 0.75, 2.95, 0], buff=0, stroke_width=4,
                              tip_length=0.2, color=YELLOW)
            inv = T("inverses", 30, YELLOW).next_to(arr, UP, buff=0.12)
            self.play(*appear(l_semi, l_anti, lag=0.3), GrowFromCenter(arr), *appear(inv), run_time=1.2)  # early: names of the two loops, said in this sentence

            # people
            c.wait_until("split")
            ppl = _pill("people  23,179", BLUE, 0, 0.3, 6.0, t2c={"23,179": GOLD})
            self.play(*appear(ppl, shift=None), run_time=1.0)  # early: the people column, before the sentence that splits it
            c.wait_until("people are composers")
            pl = _pill("1,086 composers", GREEN, -3.4, 0.3, 4.6)
            pr = _pill("22,093 others", DIM, 3.4, 0.3, 4.6)
            self.play(*during(disappear(ppl), 0, 0.4), *during(appear(pl, shift=0.3 * LEFT), 0.4, 1),
                      *during(appear(pr, shift=0.3 * RIGHT), 0.4, 1), run_time=1.6)
            c.wait_until("everyone else")
            eq1 = T("1,086 + 22,093 = 23,179", 32, GOLD).move_to([0, -0.45, 0])
            self.play(*appear(eq1), run_time=1.0)

            # movies
            c.wait_until("movies")
            mv = _pill("movies  2,935", BLUE, 0, -1.65, 6.0, t2c={"2,935": GOLD})
            self.play(*appear(mv, shift=None), run_time=1.0)
            c.wait_until("and two")
            ml = _pill("2,933 with actors", DIM, -3.4, -1.65, 4.6)
            mr = _pill("2: Flow, Kaiva", GREEN, 3.4, -1.65, 4.6)
            self.play(*during(disappear(mv), 0, 0.4), *during(appear(ml, shift=0.3 * LEFT), 0.4, 1),
                      *during(appear(mr, shift=0.3 * RIGHT), 0.4, 1), run_time=1.6)
            c.wait_until("have none")
            eq2 = T("2,933 + 2 = 2,935", 32, GOLD).move_to([0, -2.4, 0])
            self.play(*appear(eq2), run_time=1.0)
            c.wait_until()
