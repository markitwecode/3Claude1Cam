"""Chapter 1, scene 7: a query where a value goes (scalar subquery). Clips c1.scalar.1 – c1.scalar.4.

Exported for callbacks (ch1 s8 recap, ch2 s1 "a value"), static, built at ORIGIN:
- SUBQUERY: the string "(SELECT AVG(rating) FROM ratings)".
- subquery_code(size=30) -> Code of SUBQUERY (sql highlighting), as it sits after `>` here.
- avg_chip(size=30) -> VGroup(box, value): the GOLD rounded chip "7.17" the subquery collapses into
  (`.box` RoundedRectangle, `.value` Mono "7.17"); at size 30 it is ~1.0 x 0.5.
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
from lib.style import *  # noqa: E402,F403

SUBQUERY = "(SELECT AVG(rating) FROM ratings)"

ATTEMPT = """SELECT title, rating
FROM   movies JOIN ratings USING (movie_id)
WHERE year = 1976
  AND rating > AVG(rating);"""

SCALAR = """SELECT title, rating
FROM   movies JOIN ratings USING (movie_id)
WHERE year = 1976
  AND rating > (SELECT AVG(rating) FROM ratings);"""

CODE_SIZE = 30


def subquery_code(size=CODE_SIZE):
    """The parenthesised scalar subquery as Code, at ORIGIN."""
    return Code(SUBQUERY, size=size)


def avg_chip(size=CODE_SIZE):
    """The GOLD chip "7.17" the scalar subquery collapses into, at ORIGIN."""
    value = Mono("7.17", size=size, color=GOLD)
    box = RoundedRectangle(corner_radius=0.12, width=value.width + 0.32, height=value.height + 0.3)
    box.set_stroke(GOLD, 2.5).set_fill(GOLD, 0.15)
    box.move_to(value)
    chip = VGroup(box, value)
    chip.box, chip.value = box, value
    return chip


# number line for clip 4
LINE_Y = 1.2


def rx(r):
    return -6.0 + (r - 5.5) * 3.2


class Scalar(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(4.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        with self.say("c1.scalar.1") as c:
            q = T("Which 1976 movies are rated\nabove the overall average?", 44, YELLOW)
            q.move_to(UP * 0.3)
            self.play(*appear(q), run_time=1.0)
            c.wait_until("obvious")

            code = Code(ATTEMPT, size=CODE_SIZE).move_to(UP * 1.2)
            self.code1 = code
            self.play(*during([q.animate.scale(0.7).move_to(UP * 3.2)], 0, 0.6),
                      *during(appear(code), 0.45, 1), run_time=min(2.0, c.until("error")))
            c.wait_until("error")

            e1 = Mono("Binder Error: WHERE clause cannot contain aggregates!", 28, RED)
            e2 = Mono("LINE 4:   AND rating > AVG(rating);", 28, RED)
            errs = VGroup(e1, e2).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
            errs.move_to(DOWN * 1.35)
            caret = Mono("^", 28, RED)
            caret.next_to(e2, DOWN, buff=0.08)
            caret.set_x(select(e2, "AVG")[0][0].get_x())
            err = VGroup(errs, caret)
            self.play(*appear(e1, e2, caret, lag=0.3), run_time=1.3)
            self.play(FlashAround(code.find("AVG(rating)", line=3), color=RED, run_time=1.5, time_width=1.5))
            c.wait_until("the where clause judges")

            # the WHERE gate and what it can see
            view = DashedVMobject(Rectangle(width=6.9, height=3.1), num_dashes=60).set_stroke(DIM, 2)
            view.move_to([-2.85, -1.05, 0])
            cond = Mono("WHERE rating > AVG(rating)", 28)
            select(cond, "WHERE")[0].set_color(BLUE)
            avg_g = select(cond, "AVG(rating)")[0].set_color(YELLOW)
            cond.move_to([-2.85, 0.05, 0])
            gx = -2.85
            posts = VGroup(Line([gx, -0.45, 0], [gx, -1.0, 0]), Line([gx, -1.8, 0], [gx, -2.35, 0]))
            posts.set_stroke(BLUE, 8)
            self.play(*during(disappear(q, err), 0, 0.35),
                      *during([code.animate.move_to(UP * 2.4)], 0.3, 0.65),
                      *during(appear(view, posts, cond, shift=None, lag=0.2), 0.6, 1),
                      run_time=1.6)  # early: the gate's condition, read from the code above

            row_t = Mono("Rocky 1976 8.1", 28)
            row_b = RoundedRectangle(corner_radius=0.1, width=row_t.width + 0.3, height=0.6)
            row_b.set_stroke(BLUE, 2).set_fill(BG, 1)
            row = VGroup(row_b, row_t).move_to([-4.45, -1.4, 0])
            self.play(*appear(row, shift=None), run_time=0.8)
            self.play(row.animate.move_to([-1.3, -1.4, 0]), run_time=min(1.6, c.until("an average needs")))
            c.wait_until("an average needs")

            head = Mono("rating", 28, DIM)
            vals = [Mono(v, 28, GOLD) for v in ["6.0", "7.4", "8.1", "8.1", "8.2"]]
            dots = Mono("⋮", 28, GOLD)
            col = VGroup(head, *vals, dots).arrange(DOWN, buff=0.16).move_to([3.7, -1.0, 0])
            col_box = SurroundingRectangle(col, color=BLUE, buff=0.2, corner_radius=0.1).set_stroke(width=2)
            self.play(*appear(col_box, col, shift=None, lag=0.2), run_time=1.0)
            start = avg_g.get_right() + RIGHT * 0.1
            end = col_box.get_left() + UP * 0.2
            arrow = Arrow(start, end, buff=0.05, color=YELLOW, stroke_width=4)
            t = (0.6 - start[0]) / (end[0] - start[0])
            cross = cross_mark().move_to(start + t * (end - start))
            self.play(GrowArrow(arrow), time_span(FadeIn(cross, scale=0.6), 0.6, 1.2), run_time=1.2)
            self.diagram = VGroup(view, posts, cond, row, col_box, col, arrow, cross)

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        code = self.code1
        with self.say("c1.scalar.2") as c:
            code2 = Code(SCALAR, size=CODE_SIZE).move_to(UP * 2.4)
            self.play(*edit(code, code2), run_time=1.8)
            self.play(*disappear(*self.diagram), run_time=min(1.0, c.until("shape")))
            self.code2 = code2
            c.wait_until("shape")

            sub = code2.find(SUBQUERY, line=3)
            self.sub = sub
            box = token_box(sub, code2.line(3))
            self.box = box
            hdr = Mono("avg(rating)", 28, DIM)
            val = Mono("7.17", 40, GOLD)
            hr = Rectangle(width=3.0, height=0.6).set_stroke(BLUE, 2)
            cr = Rectangle(width=3.0, height=0.85).set_stroke(BLUE, 2)
            cr.next_to(hr, DOWN, buff=0)
            hdr.move_to(hr)
            val.move_to(cr)
            table = VGroup(hr, cr, hdr, val).move_to([0, -0.9, 0])
            self.play(FadeIn(box), run_time=0.8)
            self.play(*appear(VGroup(hr, cr), hdr, val, shift=None, lag=0.25), run_time=1.2)
            c.wait_until("one row")
            self.play(FlashAround(cr, run_time=1.5, time_width=1.5))
            c.wait_until("value")

            lhs = Mono("rating >", 36)
            slot = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=1.6, height=0.8),
                                  num_dashes=24).set_stroke(DIM, 2)
            slot.move_to([0, -3.0, 0])
            lhs.next_to(slot, LEFT, buff=0.3)
            self.play(*appear(lhs, slot, shift=None, lag=0.2), run_time=1.0)
            val2 = val.copy().move_to(slot)
            self.play(*fly(val, val2), run_time=1.6)
            c.wait_until("name")

            brace = span_brace(sub.get_corner(DL), sub.get_corner(DR), color=YELLOW, buff=0.12)
            label = T("scalar subquery", 36, YELLOW).next_to(brace, DOWN, buff=0.12)
            self.play(GrowFromCenter(brace), run_time=0.8)
            self.play(*appear(label), run_time=0.9)
            self.table_bits = VGroup(table, lhs, slot, val2)
            self.brace, self.label = brace, label

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        code2, sub, box = self.code2, self.sub, self.box
        with self.say("c1.scalar.3") as c:
            self.play(*disappear(*self.table_bits), run_time=0.8)
            self.play(FlashAround(sub, run_time=1.2, time_width=1.5))
            rat = code2.find("ratings", line=3)
            self.play(Transform(box, token_box(rat, code2.line(3))), run_time=0.8)
            c.wait_until("runonce")

            badge_t = T("1×", 36, YELLOW)
            badge_b = RoundedRectangle(corner_radius=0.15, width=badge_t.width + 0.4,
                                       height=badge_t.height + 0.3).set_stroke(YELLOW, 2.5)
            badge = VGroup(badge_b, badge_t.move_to(badge_b))
            p = [sub.get_left()[0] + avg_chip().width / 2, self.label.get_y(), 0]
            badge.move_to(p)
            self.play(*appear(badge), run_time=1.0)
            c.wait_until("collapse")

            chip = avg_chip()
            chip.move_to(sub)
            chip.set_x(sub.get_left()[0] + chip.width / 2)
            semi = code2.find(";", line=3)
            p = chip.get_center()
            shrink = [g.animate.scale(0.12, about_point=p).set_opacity(0) for g in sub]
            semi_to = semi.copy().next_to(chip, RIGHT, buff=0.06).align_to(semi, DOWN)
            self.play(*during([FadeOut(box)], 0, 0.3), *during(disappear(self.brace, self.label), 0, 0.4),
                      *during(shrink, 0, 0.5),
                      *during([GrowFromCenter(chip)], 0.45, 1),
                      *during([semi.animate.move_to(semi_to)], 0.5, 1),
                      run_time=2.0)
            self.chip = chip
            c.wait_until("all")

            cnt = T("2,935 ratings", 30, DIM).next_to(badge, DOWN, buff=0.25)
            self.play(*appear(cnt), run_time=1.0)
            c.wait_until("outward")

            ghost = Mono("(SELECT … )", 30, DIM).move_to([-3.6, -2.4, 0])
            ell = select(ghost, "…")[0]
            reach = CurvedArrow(ell.get_top() + UP * 0.1, [-4.9, 1.15, 0], angle=-PI / 5,
                                color=DIM, stroke_width=3)
            tag = T("part 3", 28, DIM).next_to(ghost, RIGHT, buff=0.5)
            self.play(*appear(ghost, shift=None), run_time=0.9)
            self.play(Create(reach), run_time=1.3)
            c.wait_until("we'll meet it")
            self.play(*appear(tag), run_time=0.9)

    # ------------------------------------------------------------------ clip 4
    def clip4(self):
        chip = self.chip
        with self.say("c1.scalar.4") as c:
            c.wait_until("five")
            axis = Line([rx(5.5), LINE_Y, 0], [rx(8.5), LINE_Y, 0]).set_stroke(FG, 3)
            ticks = VGroup(*[Line([rx(v), LINE_Y - 0.1, 0], [rx(v), LINE_Y + 0.1, 0]).set_stroke(FG, 3)
                             for v in (6, 7, 8)])
            tlabels = VGroup(*[Mono(str(v), 28, DIM).move_to([rx(v), LINE_Y - 0.4, 0]) for v in (6, 7, 8)])
            thr = Line([rx(7.17), LINE_Y - 0.6, 0], [rx(7.17), LINE_Y + 0.6, 0]).set_stroke(GOLD, 4)
            chip_to = [rx(7.17), LINE_Y - 0.95, 0]
            rest = [m for m in self.mobjects if m is not chip]
            self.play(*during(disappear(*rest), 0, 0.45),
                      *during([chip.animate.move_to(chip_to)], 0.4, 1), run_time=1.4)
            self.play(*appear(axis, ticks, tlabels, thr, shift=None, lag=0.15), run_time=1.0)

            # name, rating, label side, row (1 above, 2 above, -1 below), dot lift
            spec = [("King Kong", 6.0, 1, 0.0), ("Carrie", 7.4, 1, 0.0), ("Network", 8.1, -1, 0.0),
                    ("Rocky", 8.1, 2, 0.28), ("Taxi Driver", 8.2, 1, 0.0)]
            row_y = {1: 2.0, 2: 2.7, -1: 0.3}
            self.pts = {}
            for name, r, row, lift in spec:
                d = Dot([rx(r), LINE_Y + lift, 0], radius=0.11, color=FG)
                ly = row_y[row]
                lab = T(f"{name} {r}", 30)
                lab.move_to([0, ly, 0]).align_to([rx(r) + 0.1, 0, 0], LEFT)
                tip = ly - 0.2 if row > 0 else ly + 0.2
                lead = Line(d.get_center(), [rx(r), tip, 0]).set_stroke(DIM, 2)
                self.pts[name] = (d, lead, lab)
            order = ["King Kong", "Carrie", "Network", "Rocky", "Taxi Driver"]
            items = []
            for n in order:
                d, lead, lab = self.pts[n]
                items += [d, lead, lab]
            self.play(*appear(*[VGroup(*self.pts[n]) for n in order], shift=None, lag=0.3),  # early: the five shown whole, then walked
                      run_time=min(1.8, c.until("clear")))
            c.wait_until("clear")

            winners = ["Carrie", "Network", "Rocky", "Taxi Driver"]
            anims = []
            for n in winners:
                d, lead, lab = self.pts[n]
                anims += recolor([d, lab], GREEN)
            self.play(*anims, run_time=1.2)
            c.wait_until("carrie")
            self.play(FlashAround(self.pts["Carrie"][2], color=GREEN, run_time=1.2, time_width=1.5))
            c.wait_until("network and rocky")
            self.play(FlashAround(self.pts["Network"][2], color=GREEN, run_time=1.2, time_width=1.5),
                      FlashAround(self.pts["Rocky"][2], color=GREEN, run_time=1.2, time_width=1.5))
            c.wait_until("and taxi driver")
            self.play(FlashAround(self.pts["Taxi Driver"][2], color=GREEN, run_time=1.2, time_width=1.5))
            c.wait_until("kong")

            kd, kl, klab = self.pts["King Kong"]
            self.play(*recolor([kd, klab], RED), run_time=0.7)

            th = Mono("title", 30, DIM)
            rh = Mono("rating", 30, DIM)
            rows = [("Carrie", "7.4"), ("Network", "8.1"), ("Rocky", "8.1"), ("Taxi Driver", "8.2")]
            lx, rxr, y0, pitch = -2.4, 2.0, -0.55, 0.55
            th.move_to([0, y0, 0]).align_to([lx, 0, 0], LEFT)
            rh.move_to([0, y0, 0]).align_to([rxr, 0, 0], RIGHT)
            rule = Line([lx - 0.2, y0 - 0.32, 0], [rxr + 0.2, y0 - 0.32, 0]).set_stroke(DIM, 2)
            cells = []
            for i, (t, r) in enumerate(rows):
                y = y0 - 0.15 - pitch * (i + 1)
                tt = Mono(t, 30).move_to([0, y, 0]).align_to([lx, 0, 0], LEFT)
                rr = Mono(r, 30, GOLD).move_to([0, y, 0]).align_to([rxr, 0, 0], RIGHT)
                cells.append(VGroup(tt, rr))
            self.play(*set_alpha([kd, kl, klab], 0.3),
                      *appear(VGroup(th, rh, rule), *cells, shift=None, lag=0.3),
                      run_time=max(0.8, min(2.0, c.until())))
