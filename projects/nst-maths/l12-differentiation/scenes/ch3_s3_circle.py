"""Chapter 3, scene 3: Example 40, both slopes of a circle. Clips c3.circle.1 – c3.circle.5.

Exports `circle_figure(...)` (Example 40's circle) for ch3 s6 and the recap.
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

UNIT = 0.8                                  # screen units per axis unit (equal on both axes)
FIG_CENTRE = np.array([-3.4, -0.4, 0.0])    # screen point of the circle's centre (1, 0)
XP = 2.8                                    # the example abscissa; points (2.8, ±2.4)
TAN_LEN = 2.6                               # tangent segment length, in axis units
COL_X = 3.5                                 # centre of the right-hand working column


def tangent_seg(ax, x0, y0, color=GREEN, length=TAN_LEN):
    """Tangent segment to the circle at (x0, y0), centred there (vertical where y0 = 0)."""
    d = np.array([y0, -(x0 - 1.0)])
    d = d / np.linalg.norm(d) * length / 2
    return Line(ax.c2p(x0 - d[0], y0 - d[1]), ax.c2p(x0 + d[0], y0 + d[1])).set_stroke(color, 4)


def circle_figure(centre_dot=True, ticks=True, dashed=False, points=False, tangents=False,
                  verticals=False):
    """Example 40's circle at a fixed place (centre (1, 0) at screen (-3.4, -0.4), 0.8 per unit):
    equal-unit axes x -3..5, y -3.5..3.5 (DIM, x ticks only), BLUE circle radius 3.
    Optional: centre dot, tick labels -2 and 4, dashed vertical at x = 2.8, YELLOW points
    (2.8, ±2.4), their GREEN tangent lines, the RED vertical tangents at x = -2 and 4.
    Parts: .axes .xlab .ylab .circle .centre .ticks (VGroup "-2", "4") .dashed .p_top .p_bot
    .t_top .t_bot .v_left .v_right (None when off)."""
    ax = Axes(x_range=[-3, 5, 1], y_range=[-3.5, 3.5, 1], x_length=8 * UNIT, y_length=7 * UNIT,
              axis_config={"color": DIM, "stroke_width": 2, "tip_width": 0.18, "tip_height": 0.18},
              y_axis_config={"include_ticks": False})
    ax.shift(FIG_CENTRE - ax.c2p(1, 0))
    xlab = MathTex("x", font_size=34, color=FG).next_to(ax.x_axis.get_right(), DOWN, buff=0.15)
    ylab = MathTex("y", font_size=34, color=FG).next_to(ax.y_axis.get_top(), RIGHT, buff=0.15)
    circle = Circle(radius=3 * UNIT).set_stroke(BLUE, 5).move_to(ax.c2p(1, 0))
    fig = VGroup(ax, xlab, ylab, circle)
    fig.axes, fig.xlab, fig.ylab, fig.circle = ax, xlab, ylab, circle
    parts = {}
    parts["centre"] = Dot(ax.c2p(1, 0), radius=0.07, color=FG) if centre_dot else None
    if ticks:
        tm = MathTex("-2", font_size=30, color=FG).next_to(ax.c2p(-2, 0), DL, buff=0.08)
        tp = MathTex("4", font_size=30, color=FG).next_to(ax.c2p(4, 0), DR, buff=0.08)
        parts["ticks"] = VGroup(tm, tp)
    else:
        parts["ticks"] = None
    parts["dashed"] = (DashedLine(ax.c2p(XP, -3.3), ax.c2p(XP, 3.3), dash_length=0.12)
                       .set_stroke(FG, 2.5) if dashed else None)
    yp = 2.4
    parts["p_top"] = Dot(ax.c2p(XP, yp), radius=0.09, color=YELLOW) if points else None
    parts["p_bot"] = Dot(ax.c2p(XP, -yp), radius=0.09, color=YELLOW) if points else None
    parts["t_top"] = tangent_seg(ax, XP, yp) if tangents else None
    parts["t_bot"] = tangent_seg(ax, XP, -yp) if tangents else None
    parts["v_left"] = tangent_seg(ax, -2, 0, RED) if verticals else None
    parts["v_right"] = tangent_seg(ax, 4, 0, RED) if verticals else None
    for k in ("dashed", "t_top", "t_bot", "v_left", "v_right", "centre", "ticks", "p_top", "p_bot"):
        if parts[k] is not None:
            fig.add(parts[k])
        setattr(fig, k, parts[k])
    return fig


def right_angle_mark(ax, x0, y0, s=0.24):
    p = ax.c2p(x0, y0)
    u = ax.c2p(1, 0) - p
    u = u / np.linalg.norm(u)
    v = np.array([-u[1], u[0], 0.0])
    return VMobject().set_points_as_corners([p + s * u, p + s * u + s * v, p + s * v]).set_stroke(FG, 2.5)


def lowest(glyphs):
    return min(glyphs, key=lambda g: g.get_center()[1])


def mt(*parts, size=40, color=FG):
    return MathTex(*parts, font_size=size, color=color)


class Circle40(NarratedScene):
    def construct(self):
        fig = circle_figure(dashed=True, points=True, tangents=True, verticals=True)
        ax = fig.axes
        self.fig = fig
        self.part1(fig, ax)
        self.part2()
        self.part3(fig, ax)
        self.part4(fig, ax)
        self.part5(fig, ax)

    # ---------------------------------------------------------------- c3.circle.1
    def part1(self, fig, ax):
        head = T("Example 40", 44, YELLOW)
        orig = mt("y^2", "=", "9 - (x - 1)^2")
        VGroup(head, orig).arrange(RIGHT, buff=0.5).to_corner(UL, buff=0.5)
        orig.align_to(head, DOWN).shift(0.04 * DOWN)
        task = T("Find the gradient.", 32).next_to(orig, DOWN, buff=0.3, aligned_edge=LEFT)
        self.head, self.orig, self.task = head, orig, task
        r1 = mt("(x - 1)^2 + y^2 = 9").move_to([COL_X, 2.9, 0])
        self.r1 = r1
        cen_lab = mt("(1, 0)", size=30).next_to(fig.centre, DL, buff=0.12)
        ang = -40 * DEGREES
        c0 = ax.c2p(1, 0)
        rad = Line(c0, c0 + 3 * UNIT * np.array([np.cos(ang), np.sin(ang), 0])).set_stroke(FG, 3)
        r_lab = mt("3", size=34).move_to(rad.get_center() + 0.3 * np.array([-0.643, -0.766, 0]))
        self.cen_lab, self.rad, self.r_lab = cen_lab, rad, r_lab

        with self.say("c3.circle.1") as c:
            self.play(*appear(head, orig, lag=0.4), run_time=1.2)  # early: heading and the notes' equation
            self.play(FadeIn(fig.axes, fig.xlab, fig.ylab), Create(fig.circle), run_time=1.8)
            c.wait_until("move")
            self.play(FlashAround(orig, run_time=1.2, time_width=1.5), *during(appear(r1), 0.4, 1.0),
                      run_time=min(1.8, 0.6 * c.until("centre")))
            c.wait_until("centre")
            self.play(*appear(fig.centre, cen_lab), run_time=1.0)
            c.wait_until("radius")
            self.play(Create(rad), run_time=1.0)
            self.play(*appear(r_lab), run_time=0.8)
            c.wait_until("span")
            self.play(*appear(*fig.ticks, lag=0.5), run_time=1.4)
            c.wait_until(own_word=task)
            self.play(*appear(task), run_time=1.0)

    # ---------------------------------------------------------------- c3.circle.2
    def part2(self):
        r2 = mt(r"\dfrac{d}{dx}", r"\left(y^2\right)", "=", r"\dfrac{d}{dx}",
                r"\left(9 - (x - 1)^2\right)").move_to([COL_X, 1.6, 0])
        r3l = mt("2y", r"\,\dfrac{dy}{dx}")
        r3r = mt("=", "-2(x - 1)")
        VGroup(r3l, r3r).arrange(RIGHT, buff=0.2).move_to([COL_X, 0.15, 0])
        tag = T("chain rule: y depends on x", 30, YELLOW).next_to(r3l, DOWN, buff=0.3)
        tag.set_x(COL_X)
        r4 = mt(r"\dfrac{dy}{dx}", "=", r"-\dfrac{x - 1}{y}").move_to([COL_X, -1.9, 0])
        r4[0].set_color(GREEN)
        self.r2, self.r3l, self.r3r, self.tag, self.r4 = r2, r3l, r3r, tag, r4

        with self.say("c3.circle.2") as c:
            self.play(FlashAround(self.orig, run_time=1.2, time_width=1.5), *during(appear(r2), 0.4, 1.0),
                      run_time=min(1.8, 0.6 * c.until("left")))
            c.wait_until("left")
            self.play(FlashAround(r2[1], run_time=1.2, time_width=1.5), *during(appear(r3l), 0.4, 1.0),
                      run_time=1.6)
            c.wait_until("chain rule")
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("right")
            self.play(FlashAround(r2[4], run_time=1.2, time_width=1.5), *during(appear(r3r), 0.4, 1.0),
                      run_time=1.6)
            c.wait_until("divide")
            self.play(FlashAround(r3l[0], run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("result")
            self.play(*appear(r4), run_time=min(1.4, c.until(floor=1.0)))

    # ---------------------------------------------------------------- c3.circle.3
    def part3(self, fig, ax):
        r4 = self.r4
        slope_lab = mt(r"\dfrac{y}{x - 1}", size=36)
        p = ax.c2p(XP, 2.4)
        mid = (ax.c2p(1, 0) + p) / 2
        slope_lab.move_to(mid + 0.75 * np.array([-0.8, 0.6, 0]))
        rmark = right_angle_mark(ax, XP, 2.4)
        prod = mt(r"\dfrac{y}{x - 1}\cdot\left(-\dfrac{x - 1}{y}\right) = -1").move_to([COL_X, 1.1, 0])
        self.slope_lab, self.rmark, self.prod = slope_lab, rmark, prod

        with self.say("c3.circle.3") as c:
            self.play(*during(disappear(self.r1, self.r2, self.r3l, self.r3r, self.tag), 0, 0.45),
                      *during([r4.animate.move_to([COL_X, 2.6, 0])], 0.4, 1.0),
                      *during(appear(fig.p_top, shift=None), 0.5, 1.0), run_time=1.8)
            c.wait_until("radius")
            self.play(Rotate(self.rad, angle=np.arctan2(2.4, 1.8) + 40 * DEGREES, about_point=ax.c2p(1, 0)),
                      *swap(self.r_lab, slope_lab), run_time=1.8)
            c.wait_until("perp")
            self.play(GrowFromCenter(fig.t_top), Create(rmark), run_time=1.5)
            self.play(*appear(prod), run_time=1.2)

    # ---------------------------------------------------------------- c3.circle.4
    def part4(self, fig, ax):
        r4 = self.r4
        yg = lowest(r4[2])
        sub = mt(r"y = \pm\sqrt{9 - (x - 1)^2}", color=YELLOW).move_to([COL_X, 1.1, 0])
        l1 = mt(r"\dfrac{dy}{dx}", "=", r"-\dfrac{x - 1}{\pm\sqrt{9 - (x - 1)^2}}", size=38)
        l1[0].set_color(GREEN)
        den = [g for g in l1[2] if g.get_center()[1] < l1[2].get_center()[1]]
        min(den, key=lambda g: g.get_center()[0]).set_color(YELLOW)
        l1.move_to([COL_X, -0.35, 0])
        l2 = mt("=", r"\mp", r"\dfrac{x - 1}{\sqrt{9 - (x - 1)^2}}", size=38)
        l2[1].set_color(YELLOW)
        l2.next_to(l1, DOWN, buff=0.35)
        l2.shift((l1[1].get_x() - l2[0].get_x()) * RIGHT)
        self.sub, self.l1, self.l2 = sub, l1, l2

        def readout(yv, sv, pt, up):
            yl = mt("y =", yv, size=34)
            yl[1].set_color(GOLD)
            sl = mt(r"\tfrac{dy}{dx}", "=", sv, size=34)
            sl[0].set_color(GREEN)
            sl[2].set_color(GOLD)
            g = VGroup(yl, sl).arrange(DOWN, aligned_edge=RIGHT, buff=0.15)
            g.next_to(pt, LEFT, buff=0.3)
            g.shift((g.height / 2 + 0.2) * (DOWN if up else UP))
            return yl, sl

        ytop, stop = readout("2.4", r"-\tfrac34", fig.p_top, True)
        ybot, sbot = readout("-2.4", r"+\tfrac34", fig.p_bot, False)
        self.reads = [ytop, stop, ybot, sbot]

        with self.say("c3.circle.4") as c:
            self.play(FlashAround(yg, run_time=1.5, time_width=1.5), *recolor([yg], YELLOW), run_time=1.5)
            c.wait_until("sub")
            self.play(*swap(self.prod, sub), run_time=1.4)
            c.wait_until("two")
            self.play(*disappear(self.rad, self.slope_lab, self.rmark, self.cen_lab),
                      Create(fig.dashed), run_time=1.2)
            self.play(*appear(fig.p_bot, shift=None), run_time=0.8)
            c.wait_until("lines")
            self.play(GrowFromCenter(fig.t_bot), run_time=1.4)
            c.wait_until("sign")
            self.play(FlashAround(sub, run_time=1.2, time_width=1.5), *during(appear(l1), 0.4, 1.0),
                      run_time=1.8)
            self.play(*appear(l2), run_time=1.2)
            c.wait_until("num")
            self.play(*appear(ytop, ybot, lag=0.5), run_time=1.4)
            c.wait_until("minus three quarters")
            self.play(*appear(stop), run_time=1.0)
            c.wait_until("plus three quarters")
            self.play(*appear(sbot), run_time=1.0)

    # ---------------------------------------------------------------- c3.circle.5
    def part5(self, fig, ax):
        xt = ValueTracker(XP)

        def yv():
            return float(np.sqrt(max(9 - (xt.get_value() - 1) ** 2, 0.0)))

        def slope():
            return min((xt.get_value() - 1) / max(yv(), 1e-3), 99.99)

        m_dash = always_redraw(lambda: DashedLine(ax.c2p(xt.get_value(), -3.3), ax.c2p(xt.get_value(), 3.3),
                                                  dash_length=0.12).set_stroke(FG, 2.5))
        m_tt = always_redraw(lambda: tangent_seg(ax, xt.get_value(), yv()))
        m_tb = always_redraw(lambda: tangent_seg(ax, xt.get_value(), -yv()))
        m_pt = always_redraw(lambda: Dot(ax.c2p(xt.get_value(), yv()), radius=0.09, color=YELLOW))
        m_pb = always_redraw(lambda: Dot(ax.c2p(xt.get_value(), -yv()), radius=0.09, color=YELLOW))
        moving = [m_dash, m_tt, m_tb, m_pt, m_pb]

        abs_lab = mt(r"\left|\dfrac{dy}{dx}\right| =", size=40)
        num = DecimalNumber(0.75, num_decimal_places=2, font_size=40, color=GOLD)
        abs_lab.move_to([COL_X - 0.7, 0.0, 0])
        num.next_to(abs_lab, RIGHT, buff=0.2)
        num.add_updater(lambda m: m.set_value(slope()).next_to(abs_lab, RIGHT, buff=0.2))
        inf = MathTex(r"\infty", font_size=48, color=RED).next_to(abs_lab, RIGHT, buff=0.2)

        box = load_scene("ch1_s6_differentiable").diff_box().scale(0.8).move_to([2.75, 1.95, 0])
        box.border.set_fill(BG, 1)
        finite = select(box.b, "finite")[0]
        strict = mt("-2 < x < 4", size=44).move_to([COL_X, 0.0, 0])
        ul = underline(strict, RED)
        lab_r = set_backstroke(mt("2y = 0", size=34, color=RED).next_to(fig.v_right, UP, buff=0.15))
        lab_l = set_backstroke(mt("2y = 0", size=34, color=RED).next_to(fig.v_left, UP, buff=0.15))
        card_t = mt(r"\dfrac{dg}{dy} \neq 0", size=38)
        card = VGroup(RoundedRectangle(corner_radius=0.15, width=card_t.width + 0.6,
                                       height=card_t.height + 0.4).set_stroke(DIM, 2), card_t)
        card.move_to([COL_X, -2.15, 0])
        arr = Arrow(lab_r.get_right() + 0.05 * RIGHT, card.get_left() + 0.05 * LEFT, buff=0.1,
                    stroke_width=4, color=RED)
        originals = [fig.dashed, fig.t_top, fig.t_bot, fig.p_top, fig.p_bot]

        with self.say("c3.circle.5") as c:
            self.play(*during(disappear(self.r4, self.sub), 0, 0.4),
                      *during([self.l1.animate.shift(2.95 * UP), self.l2.animate.shift(2.95 * UP)], 0.35, 0.75),
                      *during(appear(abs_lab, num, shift=None), 0.8, 1.0), run_time=1.6)
            self.add(*moving)
            self.play(xt.animate.set_value(4.0), *set_alpha(originals, DIMMED),
                      *during(disappear(*self.reads), 0, 0.2),
                      run_time=max(1.5, c.until("vertical") - 0.3), rate_func=smooth)
            num.clear_updaters()
            for m in moving:
                m.clear_updaters()
            c.wait_until("vertical")
            self.play(FadeOut(*moving), FadeIn(fig.v_right), GrowFromCenter(fig.v_left), run_time=1.2)
            c.wait_until("infinite")
            self.play(*swap(num, inf), run_time=1.2)
            c.wait_until("finite")
            self.play(*during(disappear(self.head, self.orig, self.task, self.l1, self.l2, abs_lab, inf), 0, 0.45),
                      *during(appear(box, shift=None), 0.5, 1.0), run_time=1.4)
            c.wait_until("be finite")
            self.play(*recolor(finite, YELLOW), FlashUnder(finite, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("strict")
            self.play(*during(disappear(box), 0, 0.45),
                      *during(appear(self.l1, self.l2, strict, shift=None), 0.5, 1.0),
                      run_time=1.4)
            self.play(Create(ul), run_time=0.8)
            c.wait_until("cond")
            self.play(*appear(lab_r, lab_l, lag=0.4), run_time=1.2)
            self.play(*appear(card), run_time=1.2)
            self.play(GrowArrow(arr), run_time=1.0)

        # end on the circle with its two GREEN and two RED tangent lines, then fade to empty
        self.play(*disappear(self.l1, self.l2, strict, ul,
                             lab_r, lab_l, card, arr, fig.dashed, fig.centre),
                  *set_alpha([fig.t_top, fig.t_bot, fig.p_top, fig.p_bot], 1), run_time=1.2)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
