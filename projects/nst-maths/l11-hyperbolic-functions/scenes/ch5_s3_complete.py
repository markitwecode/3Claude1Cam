"""Chapter 5, scene 3: completing the square on (99); the r^2 sign cases; E2's circle. Clips c5.complete.1 – c5.complete.5.

Opens on ch5_s2_circle.handover_shot(): (99) at the top stays, the dim picture and "?" clear.
Module-level builders reused by the recap ch5_s8_recap (r1/r2):
  e2_equation(size)          (x - 1)^2 + y^2 = 1
  e2_figure(origin, u)       axes, BLUE circle, GOLD radius 1, YELLOW centre (1, 0)
  case_icons()               (small BLUE circle, YELLOW point, RED empty-set + "no points")
  case_rows()                the r^2 > 0 / = 0 / < 0 case card rows
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

HALF_A = r"\tfrac{1}{2}a"
HALF_B = r"\tfrac{1}{2}b"

# square picture (clip 1)
S, H = 2.4, 0.9
BL = np.array([-3.6, -1.55, 0.0])

# E2 figure (clips 4-5)
U = 1.3
ORG = np.array([1.9, -0.4, 0.0])
LX = -6.3                          # left edge of the working


def M(parts, size=44, colors=None, color=FG):
    m = MathTex(*parts, font_size=size, color=color)
    for i, col in (colors or {}).items():
        m[i].set_color(col)
    return m


def left_at(m, y):
    m.move_to([0, y, 0]).align_to([LX, 0, 0], LEFT)
    return m


# ---------------- builders reused by the recap ----------------
def e2_equation(size=48):
    """(x - 1)^2 + y^2 = 1"""
    return M(["(x", "-", "1", ")^2", "+", "y^2", "=", "1"], size)


def e2_figure(origin=ORG, u=U):
    """VGroup(axes, xlab, ylab, circle, radius, rlab, cdot, clab): the E2 circle."""
    ax = Axes(x_range=[-1, 3.2, 1], y_range=[-1.75, 1.75, 1], x_length=4.2 * u, y_length=3.5 * u,
              axis_config={"color": DIM, "include_ticks": False, "stroke_width": 2})
    ax.shift(origin - ax.c2p(0, 0))
    xl = MathTex("x", font_size=36, color=DIM).next_to(ax.x_axis.get_right(), DOWN, buff=0.15)
    yl = MathTex("y", font_size=36, color=DIM).next_to(ax.y_axis.get_top(), LEFT, buff=0.15)
    cen = ax.c2p(1, 0)
    circ = Circle(radius=u, color=BLUE, stroke_width=5).move_to(cen)
    ang = PI / 3
    tip = cen + u * np.array([np.cos(ang), np.sin(ang), 0])
    rad = Line(cen, tip, color=GOLD, stroke_width=5).set_z_index(2)
    rlab = set_backstroke(MathTex("1", font_size=40, color=GOLD))
    rlab.move_to((cen + tip) / 2 + 0.28 * np.array([-np.sin(ang), np.cos(ang), 0]))
    cdot = Dot(cen, radius=0.09, color=YELLOW).set_z_index(3)
    clab = set_backstroke(MathTex("(1,\\, 0)", font_size=38, color=YELLOW)).next_to(cen, DOWN, buff=0.22)
    return VGroup(ax, xl, yl, circ, rad, rlab, cdot, clab)


def case_icons():
    """(circle, point, empty): the r^2 > 0, = 0, < 0 pictures."""
    circ = Circle(radius=0.42, color=BLUE, stroke_width=5)
    pt = Dot(radius=0.1, color=YELLOW)
    empty = VGroup(MathTex(r"\varnothing", font_size=56, color=RED), T("no points", 32, RED))
    empty.arrange(RIGHT, buff=0.3)
    return circ, pt, empty


def case_rows():
    """Three rows VGroup(math, icon), left-aligned, pitch 1.25."""
    icons = case_icons()
    rows = VGroup()
    for rel, icon in zip([">", "=", "<"], icons):
        m = MathTex("r^2", rel, "0", font_size=44)
        icon = icon.copy()
        icon.next_to(m, RIGHT, buff=0.7)
        icon.align_to(m.get_right() + 0.7 * RIGHT, LEFT)
        rows.add(VGroup(m, icon))
    rows.arrange(DOWN, buff=0.55, aligned_edge=LEFT)
    for r in rows:   # icons in one column
        r[1].set_x(rows.get_left()[0] + 2.0 + r[1].width / 2)
    return rows


def shrink_away(m):
    return UpdateFromAlphaFunc(m, lambda mob, a: mob.become(_shrunk(mob.saved, a)))


def _shrunk(src, a):
    s = src.copy().scale(max(1 - a, 0.01))
    s.set_stroke(opacity=1 - a)
    return s


class CompleteSquare(NarratedScene):
    def construct(self):
        shot = load_scene("ch5_s2_circle").handover_shot()
        self.add(shot)
        ax0, circ0, q0, eq99, tag99 = shot.submobjects
        self.remove(shot)
        self.add(ax0, circ0, q0, eq99, tag99)

        # ---------------- clip 1: the square picture -----------------
        with self.say("c5.complete.1") as c:
            self.play(*disappear(ax0, circ0, q0), run_time=1.0)
            c.wait_until("pic")

            sq = Square(S, color=BLUE, stroke_width=4).set_fill(BLUE, 0.35)
            sq.move_to(BL + np.array([S / 2, S / 2, 0]))
            sx1 = MathTex("x", font_size=40).next_to(sq, DOWN, buff=0.15)
            sx2 = MathTex("x", font_size=40).next_to(sq, LEFT, buff=0.15)
            self.play(*appear(sq, sx1, sx2, lag=0.2), run_time=1.2)
            c.wait_until("two strips")
            st_r = Rectangle(height=S, width=H, color=BLUE, stroke_width=4).set_fill(BLUE, 0.15)
            st_r.next_to(sq, RIGHT, buff=0)
            st_t = Rectangle(height=H, width=S, color=BLUE, stroke_width=4).set_fill(BLUE, 0.15)
            st_t.next_to(sq, UP, buff=0)
            ha1 = MathTex(HALF_A, font_size=36).next_to(st_r, DOWN, buff=0.15)
            ha2 = MathTex(HALF_A, font_size=36).next_to(st_t, LEFT, buff=0.15)
            self.play(*appear(st_r, st_t, lag=0.3), run_time=1.2)
            c.wait_until("half the number a")
            self.play(*appear(ha1, ha2, lag=0.3), run_time=1.0)
            c.wait_until("corner")

            corner = Square(H, color=YELLOW, stroke_width=4).set_fill(YELLOW, 0)
            corner.move_to(st_r.get_top() + np.array([0, H / 2, 0]))
            dcorner = DashedVMobject(corner.copy(), num_dashes=16)
            self.play(FadeIn(dcorner), run_time=1.0)
            self.play(FlashAround(dcorner, run_time=1.5, time_width=1.5, buff=0.08))
            c.wait_until("area")
            clab = MathTex(r"(\tfrac{1}{2}a)^2", font_size=40, color=YELLOW)
            clab.next_to(corner, RIGHT, buff=0.3)
            self.play(*appear(clab, shift=0.2 * LEFT), run_time=1.0)
            c.wait_until("add")

            corner.set_fill(YELLOW, 0)
            self.add(corner)
            self.remove(dcorner)
            self.play(corner.animate.set_fill(YELLOW, 0.55), run_time=1.0)
            c.wait_until("take it away")
            away = corner.copy()
            dest = np.array([2.9, -0.35, 0])
            minus = MathTex("-", font_size=60, color=YELLOW).next_to(dest, LEFT, buff=0.65)
            self.play(away.animate.move_to(dest), run_time=1.4)
            self.play(*appear(minus, shift=None), run_time=0.8)
            c.wait_until("result")

            res = M(["x^2", "+", "a", "x", "=", "(x", "+", HALF_A, ")^2", "-", r"(\tfrac{1}{2}a)^2"],
                    52, colors={10: YELLOW})
            res.move_to([0, -2.95, 0])
            self.play(*appear(res), run_time=1.5)
            c.wait_until()

        pic = [sq, sx1, sx2, st_r, st_t, ha1, ha2, corner, clab, away, minus]

        # ---------------- clip 2: both pairs, close up, r^2, centre -----------------
        with self.say("c5.complete.2") as c:
            both = M(["x^2", "+", "a", "x", "+", r"(\tfrac{1}{2}a)^2", r"-", r"(\tfrac{1}{2}a)^2",
                      "+", "y^2", "+", "b", "y", "+", r"(\tfrac{1}{2}b)^2", "-", r"(\tfrac{1}{2}b)^2",
                      "+", "c", "=", "0"], 40, colors={i: YELLOW for i in (5, 6, 7, 14, 15, 16)})
            if both.width > 12.8:
                both.scale_to_fit_width(12.8)
            both.move_to([0, 1.5, 0])
            sweep_clear(self, keep=[eq99, tag99, res])
            self.play(*set_alpha([res], 0.4), run_time=0.6)
            derive(self, eq99, both, run_time=2.0)
            c.wait_until("close")

            closed = M(["(x", "+", HALF_A, ")^2", "+", "(y", "+", HALF_B, ")^2", "=",
                        r"(\tfrac{1}{2}a)^2 + (\tfrac{1}{2}b)^2 - c"], 48)
            closed.move_to([-0.6, 0.0, 0])
            self.play(*set_alpha([both], 0.5), *appear(closed), run_time=min(1.6, c.until("rhs")))
            c.wait_until("rhs")
            box = SurroundingRectangle(closed[10], color=YELLOW, buff=0.15, stroke_width=3)
            self.play(closed[10].animate.set_color(GOLD), FadeIn(box), run_time=1.2)
            c.wait_until("rsq")
            rsq = MathTex("=", "r^2", font_size=48, color=GOLD).next_to(box, RIGHT, buff=0.25)
            self.play(*appear(rsq, shift=0.2 * LEFT), run_time=1.0)
            c.wait_until("centre")

            centre = M([r"\text{centre}\ ", "(", "-", HALF_A, r",\,", "-", HALF_B, ")"], 48, color=YELLOW)
            centre.move_to([0, -1.5, 0])
            self.play(*appear(centre), *disappear(res), run_time=1.2)
            c.wait_until("signs flipped")
            self.play(*flash([centre[2], centre[5], closed[1], closed[6]], run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until()

        # ---------------- clip 3: the sign of the right-hand side -----------------
        with self.say("c5.complete.3") as c:
            self.play(*disappear(both, centre), run_time=0.8)
            self.play(*[m.animate.shift(1.4 * UP) for m in (closed, box, rsq)], run_time=1.2)
            rows = case_rows()
            card = SurroundingRectangle(rows, color=DIM, buff=0.35, corner_radius=0.15, stroke_width=2)
            VGroup(rows, card).next_to(box, DOWN, buff=0.4)
            if card.get_right()[0] > 6.5:
                VGroup(rows, card).shift((6.5 - card.get_right()[0]) * RIGHT)
            c.wait_until("sign")
            self.play(FadeIn(card), FlashAround(box, run_time=1.5, time_width=1.5), run_time=1.5)
            for cue, r in zip(["pos", "zero", "neg"], rows):
                c.wait_until(cue)
                self.play(*appear(r[0], r[1], lag=0.4, shift=None), run_time=1.2)
            c.wait_until()

        # ---------------- clip 4: E2 -----------------
        with self.say("c5.complete.4") as c:
            src = T("Examples Sheet I, E2", 30, DIM).to_corner(UL, buff=0.5)
            sweep_clear(self, time_span(FadeIn(src), 0.6, 1.2), keep=[])  # early: source label of the example
            c.wait_until("ex squared")
            l1 = left_at(M(["x^2", "-", "2", "x", "+", "y^2", "=", "0"], 48), 2.0)
            self.play(*appear(l1), run_time=1.2)
            c.wait_until("half")
            ann = MathTex(r"\tfrac{1}{2}(-2) = -1", font_size=40, color=GOLD).next_to(l1, RIGHT, buff=0.9)
            self.play(*appear(ann), run_time=1.0)
            c.wait_until("add its square")
            l2 = left_at(M(["x^2", "-", "2", "x", "+", "1", "-", "1", "+", "y^2", "=", "0"], 48,
                           colors={4: YELLOW, 5: YELLOW, 6: YELLOW, 7: YELLOW}), 0.1)
            derive(self, l1, l2, run_time=2.0)
            c.wait_until("done")
            l3 = left_at(e2_equation(48), -1.15)
            # term-safe: x^2 - 2x + 1 closes up into (x - 1)^2; no glyph-matching rewrite
            self.play(*appear(l3), run_time=1.2)
            sq_src = VGroup(*[m.copy() for m in l2[0:6]])
            sq_dst = VGroup(*[m.copy() for m in l3[0:4]])
            self.play(FlashAround(sq_src, run_time=1.5, time_width=1.5, buff=0.1),
                      FlashAround(sq_dst, run_time=1.5, time_width=1.5, buff=0.1), run_time=1.5)
            c.wait_until("read")

            fig = e2_figure()
            ax, xl, yl, circ, rad, rlab, cdot, clab = fig
            self.play(*appear(ax, xl, yl, shift=None), run_time=0.8)
            self.play(Create(circ), *appear(cdot, clab), run_time=1.4)
            self.play(Create(rad), *appear(rlab), run_time=min(1.0, c.until("origin")))
            c.wait_until("origin")
            odot = Dot(ax.c2p(0, 0), radius=0.08, color=FG).set_z_index(3)
            self.play(FadeIn(odot), FlashAround(odot, run_time=1.4, time_width=1.5, buff=0.12),
                      run_time=min(1.4, c.until(floor=0.6)))
            c.wait_until()

        # ---------------- clip 5: slide the constant -----------------
        with self.say("c5.complete.5") as c:
            l1c = left_at(M(["x^2", "-", "2", "x", "+", "y^2", "+", "c", "=", "0"], 48, colors={7: GOLD}), 2.0)
            self.play(*during(disappear(l2, ann), 0, 0.4),
                      *during([l3.animate.move_to([l3.get_x(), 0.7, 0])], 0.35, 1.0),
                      *edit(l1, l1c), run_time=1.5)
            l3c = left_at(M(["(x", "-", "1", ")^2", "+", "y^2", "=", "1", "-", "c"], 48, colors={9: GOLD}), 0.7)
            self.play(*edit(l3, l3c), run_time=min(1.3, c.until("plus1")))
            c.wait_until("plus1")

            r1 = left_at(M([r"c = 1:\quad", "(x", "-", "1", ")^2", "+", "y^2", "=", "0"], 44,
                           colors={0: GOLD, 8: YELLOW}), -0.7)
            self.play(*appear(r1), run_time=1.3)
            c.wait_until("point")
            circ.saved = circ.copy()
            self.play(*disappear(rad, rlab, odot), shrink_away(circ), run_time=1.5)
            self.remove(circ)
            self.play(FlashAround(cdot, run_time=1.2, time_width=1.5, buff=0.1))
            c.wait_until("plus2")

            r2 = left_at(M([r"c = 2:\quad", "(x", "-", "1", ")^2", "+", "y^2", "=", "-1"], 44,
                           colors={0: GOLD, 8: RED}), -2.0)
            self.play(*appear(r2), run_time=1.3)
            c.wait_until("none")
            nop = set_backstroke(T("no points", 36, RED)).move_to(cdot.get_center() + 0.5 * UP + 0.3 * RIGHT)
            self.play(*swap(VGroup(cdot, clab), nop), run_time=1.4)
            c.wait_until()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
