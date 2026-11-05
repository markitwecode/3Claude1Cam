"""Chapter 6, scene 3: the second-derivative test. Clips c6.second.1 – c6.second.4.

Exports (static, named parts):
cubic_graph(dots=False) -> VGroup   y = x^3 - 3x on its axes (ch1 Figure 29 style)
    .axes   Axes (DIM, no ticks, tips), x -2.3..2.3, y -3.2..3.2, 6.0 x 6.08, origin at GRAPH_O
    .xlab .ylab   "x", "y" at the axis tips
    .curve  BLUE plot, x -2.1..2.1
    .name   MathTex "y = x^3 - 3x", top left of the axes
    .max_dot .min_dot   YELLOW dots at (-1, 2), (1, -2) (in the group only with dots=True)
    Helpers: cubic_pt(axes, x), cubic_tangent(axes, x, length) (GREEN).
umbrellas() -> VGroup
    .pool .bowl .bowl_rain .bowl_tex .bowl_lab   left: upside-down BLUE umbrella, FG pool (0.3),
        rain streaks falling in, "y'' > 0", "minimum"
    .cap .cap_rain .cap_tex .cap_lab              right: usual-way-up umbrella, rain above and
        running off its edges, "y'' < 0", "maximum"
    .left .right   VGroups of each side's parts; .bowl_pivot .cap_pivot  rim centres (arrays)
    .bowl / .cap are VGroup(canopy, shaft, tip, hook) with .canopy .shaft .tip .hook.
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

GRAPH_O = np.array([-2.3, -0.5, 0.0])
TAN_LEN = 2.2


def _f(x):
    return x ** 3 - 3 * x


def _fp(x):
    return 3 * x ** 2 - 3


def cubic_pt(axes, x):
    return axes.c2p(x, _f(x))


def cubic_tangent(axes, x, length=TAN_LEN):
    p = cubic_pt(axes, x)
    d = axes.c2p(x + 1, _f(x) + _fp(x)) - p
    d = d / np.linalg.norm(d)
    return Line(p - 0.5 * length * d, p + 0.5 * length * d, color=GREEN, stroke_width=4)


def cubic_graph(dots=False):
    g = VGroup()
    axes = Axes(x_range=[-2.3, 2.3, 10], y_range=[-3.2, 3.2, 10], x_length=6.0, y_length=6.08,
                tips=True, axis_config={"color": DIM, "include_ticks": False, "stroke_width": 3})
    axes.shift(GRAPH_O - axes.c2p(0, 0))
    g.axes = axes
    g.xlab = MathTex("x", font_size=40).next_to(axes.x_axis.get_end(), RIGHT, buff=0.15)
    g.ylab = MathTex("y", font_size=40).next_to(axes.y_axis.get_end(), UP, buff=0.12)
    g.curve = axes.plot(_f, x_range=[-2.1, 2.1], color=BLUE, stroke_width=5)
    g.name = MathTex("y = x^3 - 3x", font_size=44)
    g.name.move_to(axes.get_corner(UL) + np.array([-1.3, 0.86, 0]), aligned_edge=LEFT)
    g.max_dot = Dot(cubic_pt(axes, -1), radius=0.09, color=YELLOW)
    g.min_dot = Dot(cubic_pt(axes, 1), radius=0.09, color=YELLOW)
    g.add(axes, g.xlab, g.ylab, g.curve, g.name)
    if dots:
        g.add(g.max_dot, g.min_dot)
    return g


# ---------------------------------------------------------------- umbrellas
U_R = 1.6


def _umbrella(c):
    """Upright umbrella with its rim centre at c: VGroup(canopy, shaft, tip, hook)."""
    c = np.array(c, dtype=float)
    arc = Arc(radius=U_R, start_angle=0, angle=PI, arc_center=c)
    canopy = VMobject()
    canopy.append_points(arc.points)
    n = 4
    xs = np.linspace(-U_R, U_R, n + 1)
    for a, b in zip(xs[:-1], xs[1:]):
        sc = ArcBetweenPoints(c + np.array([a, 0, 0]), c + np.array([b, 0, 0]), angle=-PI / 2.2)
        canopy.append_points(sc.points)
    canopy.set_stroke(BLUE, 5).set_fill(BLUE, 0.15)
    shaft = Line(c + U_R * UP, c + 1.4 * DOWN, color=BLUE, stroke_width=5)
    tip = Line(c + U_R * UP, c + (U_R + 0.22) * UP, color=BLUE, stroke_width=5)
    hook = Arc(radius=0.3, start_angle=0, angle=-PI, arc_center=c + np.array([-0.3, -1.4, 0]))
    hook.set_stroke(BLUE, 5)
    u = VGroup(canopy, shaft, tip, hook)
    u.canopy, u.shaft, u.tip, u.hook = canopy, shaft, tip, hook
    return u


def _streaks(c, tops, length=0.4):
    c = np.array(c, dtype=float)
    return VGroup(*[Line(c + np.array([x, y, 0]), c + np.array([x, y - length, 0]),
                         color=FG, stroke_width=3, stroke_opacity=0.6) for x, y in tops])


def _pool(c, level=-0.7):
    c = np.array(c, dtype=float)
    a0 = np.arcsin(-level / U_R)
    angs = np.linspace(PI + a0, 2 * PI - a0, 40)
    pts = [c + U_R * 0.97 * np.array([np.cos(t), np.sin(t), 0]) for t in angs]
    return Polygon(*pts, stroke_width=0).set_fill(FG, 0.3)


def umbrellas():
    g = VGroup()
    cl, cr = np.array([-3.4, 0.7, 0.0]), np.array([3.4, 0.7, 0.0])
    g.bowl_pivot, g.cap_pivot = cl, cr
    g.bowl = _umbrella(cl).rotate(PI, about_point=cl)
    g.pool = _pool(cl)
    g.bowl_rain = _streaks(cl, [(-1.2, 2.6), (-0.65, 2.2), (-1.05, 1.6), (0.9, 2.55), (1.25, 1.85),
                                (0.8, 1.15), (-0.5, 1.0), (-0.85, 0.15), (0.6, 0.0)])
    g.bowl_tex = MathTex("y'' > 0", font_size=48, color=GREEN).move_to([cl[0], -1.85, 0])
    g.bowl_lab = T("minimum", 40, YELLOW).move_to([cl[0], -2.65, 0])
    g.cap = _umbrella(cr)
    g.cap_rain = VGroup(*_streaks(cr, [(-1.3, 2.7), (-0.7, 2.4), (0.45, 2.65), (1.0, 2.3), (1.5, 2.75)]),
                        *_streaks(cr, [(-1.85, -0.1), (-1.85, -0.75), (1.85, -0.2), (1.85, -0.85)]))
    g.cap_tex = MathTex("y'' < 0", font_size=48, color=GREEN).move_to([cr[0], -1.85, 0])
    g.cap_lab = T("maximum", 40, YELLOW).move_to([cr[0], -2.65, 0])
    g.left = VGroup(g.pool, g.bowl, g.bowl_rain, g.bowl_tex, g.bowl_lab)
    g.right = VGroup(g.cap, g.cap_rain, g.cap_tex, g.cap_lab)
    g.add(g.pool, g.bowl, g.bowl_rain, g.bowl_tex, g.bowl_lab, g.cap, g.cap_rain, g.cap_tex, g.cap_lab)
    return g


# ---------------------------------------------------------------- scene helpers
def _slope_text(x):
    s = _fp(x)
    if abs(s) < 0.05:
        v = "0"
    else:
        v = f"{s:+.1f}"
    return MathTex(f"y' = {v}", font_size=38, color=GREEN)


def readout_min(axes, x):
    p = cubic_pt(axes, x)
    return _slope_text(x).move_to([p[0] + 0.6, -3.15, 0])


def readout_max(axes, x):
    p = cubic_pt(axes, x)
    return _slope_text(x).move_to([p[0] - 1.2, 2.7, 0])


class SecondDerivativeTest(NarratedScene):
    def construct(self):
        g = cubic_graph()
        ax = g.axes
        self.g = g

        # ---------------- c6.second.1: the curve, its derivative, two stationary points, which is which?
        with self.say("c6.second.1") as c:
            self.play(FadeIn(ax), FadeIn(g.xlab), FadeIn(g.ylab), run_time=1.0)
            self.play(Create(g.curve), *appear(g.name), run_time=2.2)
            c.wait_until("deriv")
            deriv = MathTex("y'", "=", "3x^2 - 3", "=", "3", "(x - 1)", "(x + 1)", font_size=42)
            deriv[0].set_color(GREEN)
            deriv.move_to([3.85, 2.9, 0])
            self.deriv = deriv
            self.play(*appear(deriv), run_time=1.2)
            c.wait_until("zero")
            self.play(*flash([deriv[5], deriv[6]]), run_time=1.5)
            c.wait_until("dots")
            self.play(GrowFromCenter(g.max_dot), GrowFromCenter(g.min_dot), run_time=1.0)
            self.play(*flash([g.max_dot, g.min_dot]), run_time=1.2)
            c.wait_until("ask")
            self.q_max = T("?", 48, YELLOW).move_to(g.max_dot.get_center() + 0.62 * UP)
            self.q_min = T("?", 48, YELLOW).move_to(g.min_dot.get_center() + 0.62 * UP)
            self.play(*appear(self.q_max, self.q_min, lag=0.3), run_time=1.2)

        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------- c6.second.2: the tangent rolls through the minimum
    def clip2(self):
        g, ax = self.g, self.g.axes
        with self.say("c6.second.2") as c:
            xt = ValueTracker(0.2)
            tan = cubic_tangent(ax, 0.2)
            rd = readout_min(ax, 0.2)
            self.play(FadeIn(tan), *appear(rd), run_time=1.0)
            tan.add_updater(lambda m: m.become(cubic_tangent(ax, xt.get_value())))
            rd.add_updater(lambda m: m.become(readout_min(ax, xt.get_value())))
            self.play(xt.animate.set_value(0.4), run_time=min(2.0, c.until("neg")), rate_func=smooth)
            c.wait_until("neg")
            self.play(FlashAround(rd, color=GREEN, run_time=1.5, time_width=1.5))
            c.wait_until("zero")
            self.play(xt.animate.set_value(1.0), run_time=min(2.0, 0.8 * c.until("pos")))
            self.play(FlashAround(g.min_dot, color=YELLOW, run_time=1.0))
            c.wait_until("pos")
            self.play(xt.animate.set_value(1.6), run_time=min(2.0, 0.8 * c.until("incr")))
            c.wait_until("incr")
            lab = T("slope:", 36, GREEN)
            signs = MathTex("-", r"\;\to\;", "0", r"\;\to\;", "+", font_size=44, color=GREEN)
            row = VGroup(lab, signs).arrange(RIGHT, buff=0.3).move_to([3.5, 0.45, 0])
            up = Arrow(row.get_right() + 0.35 * RIGHT + 0.5 * DOWN, row.get_right() + 0.35 * RIGHT + 0.5 * UP,
                       color=GREEN, stroke_width=6, buff=0)
            self.play(*appear(row), run_time=1.0)
            c.wait_until("increases")
            self.play(GrowArrow(up), run_time=1.0)
            c.wait_until("positive there")
            ypp = MathTex("y'' > 0", font_size=48, color=GREEN).move_to([3.85, -0.6, 0])
            self.play(*appear(ypp), run_time=1.0)
        self.tan, self.rd, self.row, self.up, self.ypp, self.xt = tan, rd, row, up, ypp, xt

    # ---------------- c6.second.3: the test, and applying it
    def clip3(self):
        g, ax = self.g, self.g.axes
        with self.say("c6.second.3") as c:
            self.tan.clear_updaters()
            self.rd.clear_updaters()
            self.play(*during(disappear(self.row, self.up, self.tan, self.rd), 0, 0.45),
                      *during([self.deriv.animate.move_to([3.85, 0.4, 0])], 0.4, 1.0), run_time=1.6)
            c.wait_until("rule")
            l1 = MathTex(r"\dfrac{d^2y}{dx^2} > 0", r"\;\Rightarrow\;", r"\text{local minimum}", font_size=40)
            l2 = MathTex(r"\dfrac{d^2y}{dx^2} < 0", r"\;\Rightarrow\;", r"\text{local maximum}", font_size=40)
            l1[2].set_color(YELLOW)
            l2[2].set_color(YELLOW)
            VGroup(l1, l2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.85, 2.25, 0])
            card = RoundedRectangle(corner_radius=0.15, width=VGroup(l1, l2).width + 0.6,
                                    height=VGroup(l1, l2).height + 0.5, color=DIM, stroke_width=3)
            card.move_to(VGroup(l1, l2))
            self.play(FadeIn(card), *appear(l1), run_time=1.3)  # early: the rule card is read out over the sentence
            c.wait_until("falls in")
            seg = ax.plot(_f, x_range=[0.2, 1.75], color=YELLOW, stroke_width=8)
            self.play(VShowPassingFlash(seg, time_width=0.5), run_time=2.0)
            c.wait_until("a local minimum")
            self.play(FlashAround(l1[2], run_time=1.5, time_width=1.5),
                      FlashAround(g.min_dot, run_time=1.5, time_width=1.5))

            # the maximum
            c.wait_until("max")
            xt = ValueTracker(-1.6)
            tan = cubic_tangent(ax, -1.6)
            rd = readout_max(ax, -1.6)
            self.play(FadeIn(tan), *appear(rd), run_time=0.9)
            tan.add_updater(lambda m: m.become(cubic_tangent(ax, xt.get_value())))
            rd.add_updater(lambda m: m.become(readout_max(ax, xt.get_value())))
            self.play(xt.animate.set_value(-1.0), run_time=min(1.6, c.until("decreases")))
            c.wait_until("decreases")
            self.play(xt.animate.set_value(-0.4), run_time=min(1.6, c.until("local maximum")))
            down = Arrow([-5.3, 1.9, 0], [-5.3, 0.8, 0], color=GREEN, stroke_width=6, buff=0)
            self.play(GrowArrow(down), run_time=0.8)
            c.wait_until("local maximum")
            self.play(*appear(l2), run_time=1.0)

            # apply it
            c.wait_until("check")
            tan.clear_updaters()
            rd.clear_updaters()
            ypp6 = MathTex("y''", "=", "6x", font_size=48, color=GREEN).move_to(self.ypp)
            self.play(*during(disappear(tan, rd, down), 0, 0.45), *edit(self.ypp, ypp6), run_time=1.5)
            c.wait_until("six at")
            fmin = MathTex("y''(1) = 6 > 0", font_size=40, color=GREEN)
            fmin.move_to(g.min_dot.get_center() + 1.0 * RIGHT, aligned_edge=LEFT)
            lmin = T("minimum", 36, YELLOW).next_to(fmin, DOWN, buff=0.25, aligned_edge=LEFT)
            self.play(*swap(self.q_min, fmin), run_time=1.2)
            c.wait_until(own_word=lmin)
            self.play(*appear(lmin), run_time=1.0)
            c.wait_until("minus")
            fmax = MathTex("y''(-1) = -6 < 0", font_size=40, color=GREEN)
            fmax.move_to([-6.6, 2.4, 0], aligned_edge=LEFT)
            lmax = T("maximum", 36, YELLOW).next_to(fmax, DOWN, buff=0.25, aligned_edge=LEFT)
            self.play(*swap(self.q_max, fmax), run_time=1.2)
            c.wait_until(own_word=lmax)
            self.play(*appear(lmax), run_time=1.0)

    # ---------------- c6.second.4: the umbrella memory aid
    def clip4(self):
        with self.say("c6.second.4", gap=2.7) as c:
            c.wait_until("lecturer")
            u = umbrellas()
            u.bowl.rotate(PI, about_point=u.bowl_pivot)        # starts the usual way up
            sweep_clear(self, time_span(FadeIn(u.bowl), 1.0, 2.0), time_span(FadeIn(u.cap), 1.2, 2.2),
                        run_time=2.2)
            c.wait_until("bowl")
            self.play(Rotate(u.bowl, PI, about_point=u.bowl_pivot), run_time=1.6)
            c.wait_until("collects the rain")
            self.play(LaggedStart(*[FadeIn(s, shift=0.5 * DOWN) for s in u.bowl_rain], lag_ratio=0.12),
                      run_time=1.6)
            self.play(GrowFromEdge(u.pool, DOWN), run_time=1.2)
            c.wait_until("positive second derivative")
            self.play(*appear(u.bowl_tex), run_time=1.0)
            c.wait_until(own_word=u.bowl_lab)
            self.play(*appear(u.bowl_lab), run_time=1.0)
            c.wait_until("cap")
            self.play(FlashAround(u.cap.canopy, color=BLUE, run_time=1.2, time_width=1.5))
            c.wait_until("no rain underneath")
            self.play(LaggedStart(*[FadeIn(s, shift=0.5 * DOWN) for s in u.cap_rain], lag_ratio=0.12),
                      run_time=1.8)
            c.wait_until("negative second derivative")
            self.play(*appear(u.cap_tex), run_time=1.0)
            c.wait_until(own_word=u.cap_lab)
            self.play(*appear(u.cap_lab), run_time=1.0)
