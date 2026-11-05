"""Chapter 7, scene 4: H4, route ii (differentiate as it stands) and why the routes agree.
Clips c7.h4two.1 – c7.h4two.5.

Opens on s3's handover_shot() (route i's boxed answer upper left, the small H4 card upper right).
Clip 1: "route ii" label; y + e^y sin y = 1/x becomes d/dx(...) = d/dx(1/x), tag y = y(x); YELLOW y'
marks over every function of y; the derivative row builds term by term. Clip 2: the y' terms
collect, y'(1 + e^y(sin y + cos y)) = -1/x^2; route i's GREEN box lands on the bracket; route ii's
boxed answer. Clip 3: both answers side by side (GREEN bottoms aligned); their tops (BLUE)^2 ?= 1/x^2;
the original equation drops in and squares; ? becomes =, GREEN tick on the card. Clip 4: the slip
(struck RED y's), the wrong answer, the y = 1/2 test (-0.514 GREEN vs -3.90 RED), RED cross on the
card. Clip 5: GREEN bottoms flash; the curve x = 1/(y + e^y sin y) with its tip (0.1015, 2.419), a
RED vertical tangent, ch3 s6's cube root small beside it. Ends empty.

Exports (for the recap ch7_s6):
    answer_ii_group(size=48) -> VGroup(box, formula, label "route ii"); .formula has .frac .den_tex
        (GREEN box's tex) .den_box (the GREEN boxed group).
    answers_pair() -> VGroup(ans1, ans2): route i (s3's answer_group) and route ii side by side at
        the centre, same scale, GREEN bottoms on one height; .ans1 .ans2.
    squared_eq(size=44) -> (BLUE box)^2 = 1/x^2; parts .lhs .eq .rhs.
    ey_good(size=48) -> MathTex e^y y' (e^y GOLD, y' YELLOW).
    ey_struck(size=48) -> VGroup(tex, strike): e^y y' with the y' RED and struck; .tex .strike.
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

S3 = "ch7_s3_h4_one"
ROW_A = np.array([0.0, -0.35, 0])
ROW_B = np.array([0.0, -2.35, 0])
ROW_C = np.array([0.0, -0.1, 0])
X_I, X_II, Y_PAIR = -3.45, 3.45, 1.0


def s3():
    return load_scene(S3)


# ------------------------------------------------------------------ exported pieces

def answer_ii_formula(size=48):
    """dy/dx = -1 / (x^2 GREEN)."""
    m = s3()
    num = MathTex("1", font_size=size)
    dbox = m.boxed(m.dp_tex(size), GREEN)
    den = VGroup(MathTex("x^2", font_size=size), dbox).arrange(RIGHT, buff=0.12)
    den[0].align_to(dbox.tex, DOWN)
    fr = m.frac(num, den)
    f = m.line([MathTex(r"\frac{dy}{dx}", font_size=size), MathTex("=", font_size=size),
                MathTex("-", font_size=size), fr], fr, buff=0.2)
    f.frac, f.den_box, f.den_tex = fr, dbox, dbox.tex
    return f


def answer_ii_group(size=48):
    f = answer_ii_formula(size)
    box = SurroundingRectangle(f, color=YELLOW, buff=0.28, stroke_width=3)
    lab = T("route ii", 30, YELLOW)
    lab.next_to(box, DOWN, buff=0.15).align_to(box, LEFT)
    g = VGroup(box, f, lab)
    g.box, g.formula, g.label = box, f, lab
    return g


def _place(ans, scale, x, label_buff=0.15):
    bf = VGroup(ans.box, ans.formula)
    bf.scale(scale).move_to([x, Y_PAIR, 0])
    ans.label.next_to(ans.box, DOWN, buff=label_buff).align_to(ans.box, LEFT)
    return ans


def pair_scale():
    a = s3().answer_group()
    return 5.6 / VGroup(a.box, a.formula).width


def answers_pair():
    m = s3()
    k = pair_scale()
    a1 = _place(m.answer_group(), k, X_I)
    a2 = _place(answer_ii_group(), k, X_II)
    dy = a1.formula.frac.den.rect.get_y() - a2.formula.den_box.rect.get_y()
    a2.shift(dy * UP)
    g = VGroup(a1, a2)
    g.ans1, g.ans2 = a1, a2
    return g


def squared_eq(size=44):
    m = s3()
    lhs = m.squared(m.boxed(m.lhs_tex(size), BLUE), size)
    eq = MathTex("=", font_size=size)
    rhs = MathTex(r"\frac{1}{x^2}", font_size=size)
    g = VGroup(lhs, eq, rhs).arrange(RIGHT, buff=0.25)
    g.lhs, g.eq, g.rhs = lhs, eq, rhs
    return g


def ey_good(size=48):
    t = MathTex("e^y", "y'", font_size=size)
    t[0].set_color(GOLD)
    t[1].set_color(YELLOW)
    return t


def ey_struck(size=48):
    t = MathTex("e^y", "y'", font_size=size)
    t[0].set_color(GOLD)
    t[1].set_color(RED)
    st = strike(t[1])
    g = VGroup(t, st)
    g.tex, g.strike = t, st
    return g


def strike(m):
    return Line(m.get_corner(DL) + 0.06 * (LEFT + DOWN), m.get_corner(UR) + 0.06 * (RIGHT + UP),
                color=RED, stroke_width=5)


# ------------------------------------------------------------------ scene pieces

def eq0_tex(size=52):
    t = MathTex("y", "+", "e^y", r"\sin y", "=", r"\frac{1}{x}", font_size=size)
    t[2].set_color(GOLD)
    return t


def row_a_tex(size=52):
    t = MathTex(r"\frac{d}{dx}", r"\Big(", "y", "+", "e^y", r"\sin y", r"\Big)", "=",
                r"\frac{d}{dx}", r"\frac{1}{x}", font_size=size)
    t[4].set_color(GOLD)
    return t


def row_b_tex(size=48):
    t = MathTex("y'", "+", "e^y", "y'", r"\sin y", "+", "e^y", r"\cos y", r"\, y'", "=", "-",
                r"\frac{1}{x^2}", font_size=size)
    for i in (0, 3, 8):
        t[i].set_color(YELLOW)
    for i in (2, 6):
        t[i].set_color(GOLD)
    return t


def row_c_tex(size=52):
    t = MathTex("y'", r"\Big(", "1", "+", "e^y", r"(\sin y + \cos y)", r"\Big)", "=", "-",
                r"\frac{1}{x^2}", font_size=size)
    t[0].set_color(YELLOW)
    t[4].set_color(GOLD)
    return t


def wrong_tex(size=46):
    t = MathTex("y'", "=", "-", r"\frac{1}{x^2}", "-", "e^y", r"(\sin y + \cos y)", font_size=size)
    t.set_color(RED)
    return t


def f_lhs(y):
    return y + np.exp(y) * np.sin(y)


def bisect(fn, a, b, n=60):
    fa = fn(a)
    for _ in range(n):
        m = 0.5 * (a + b)
        if (fn(m) > 0) == (fa > 0):
            a, fa = m, fn(m)
        else:
            b = m
    return 0.5 * (a + b)


def cube_root_pic():
    """ch3 s6's cube root, small: BLUE y = x^(1/3), RED vertical tangent at the origin."""
    u = 0.95
    ax = Axes(x_range=[-1.7, 1.7, 10], y_range=[-1.7, 1.7, 10], x_length=3.4 * u, y_length=3.4 * u,
              tips=True, axis_config={"color": DIM, "include_ticks": False, "stroke_width": 3})
    curve = ParametricFunction(lambda t: ax.c2p(t ** 3, t), t_range=[-1.17, 1.17], color=BLUE,
                               stroke_width=5)
    tan = Line(ax.c2p(0, -1.45), ax.c2p(0, 1.45), color=RED, stroke_width=6)
    xl = MathTex("x", font_size=32).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
    yl = MathTex("y", font_size=32).next_to(ax.y_axis.get_end(), UP, buff=0.08)
    lab = MathTex("y = x^{1/3}", font_size=36, color=BLUE).next_to(ax.c2p(-0.25, 1.35), LEFT, buff=0.1)
    g = VGroup(ax, xl, yl, curve, tan, lab)
    g.axes, g.curve, g.tan, g.lab = ax, curve, tan, lab
    return g


# ------------------------------------------------------------------ scene

class H4RouteTwo(NarratedScene):
    def construct(self):
        self.m = s3()
        shot = self.m.handover_shot()
        self.ans1, self.card = shot.answer, shot.card
        self.add(self.ans1, self.card)   # as two top-level objects, so each can be kept or moved alone
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c7.h4two.1
    def clip1(self):
        route = T("route ii: differentiate as it stands", 32, t2c={"route ii:": TEAL}).move_to([0, 1.05, 0])
        eq0 = eq0_tex().move_to(ROW_A)
        A = row_a_tex().move_to(ROW_A)
        tag = MathTex("y = y(x)", font_size=34, color=TEAL).next_to(A[2], DOWN, buff=0.35)
        top = A[1].get_top()[1] + 0.32
        marks = [MathTex("y'", font_size=34, color=YELLOW).move_to([A[i].get_x(), top, 0])
                 for i in (2, 4, 5)]
        B = row_b_tex().move_to(ROW_B)
        b1, b2, b3 = VGroup(B[0]), VGroup(*B[1:9]), VGroup(*B[9:])
        with self.say("c7.h4two.1") as c:
            self.play(*appear(route, eq0, lag=0.3), run_time=1.0)  # early: route title and the equation
            c.wait_until("Differentiate")
            self.play(*edit(eq0, A), run_time=1.6)
            c.wait_until("depends")
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("chain")
            self.play(*appear(*marks, lag=0.35), run_time=1.8)
            c.wait_until("terms")
            self.play(FlashAround(VGroup(A[2], marks[0]), time_width=1.5),
                      *during(appear(b1, shift=0.2 * DOWN), 0.3, 1.0), run_time=1.5)
            c.wait_until("E to the why times")
            self.play(FlashAround(VGroup(A[4], A[5]), color=GOLD, time_width=1.5), run_time=1.2)
            self.play(*appear(b2, shift=0.2 * DOWN), run_time=1.6)
            c.wait_until("rhs")
            self.play(FlashAround(VGroup(A[8], A[9]), time_width=1.5),
                      *during(appear(b3, shift=0.2 * DOWN), 0.3, 1.0), run_time=1.6)
        self.remove(*b1.get_family(), *b2.get_family(), *b3.get_family())
        self.add(B)
        self.route, self.A, self.tag, self.marks, self.B = route, A, tag, marks, B

    # ------------------------------------------------------------------ c7.h4two.2
    def clip2(self):
        B = self.B
        C = row_c_tex().move_to(ROW_C)
        bracket = VGroup(*C[2:6])
        grect = SurroundingRectangle(bracket, color=GREEN, buff=0.1, stroke_width=3)
        same = T("same as route i", 30, GREEN).next_to(grect, DOWN, buff=0.22)
        k = pair_scale()
        a2 = answer_ii_group()
        VGroup(a2.box, a2.formula).scale(k).move_to([0, -1.95, 0])
        a2.label.next_to(a2.box, DOWN, buff=0.15).align_to(a2.box, LEFT)
        den1 = self.ans1.formula.frac.den
        with self.say("c7.h4two.2") as c:
            self.play(*flash([B[0], B[3], B[8]], time_width=1.5), run_time=1.2)
            self.play(*during(disappear(self.A, self.tag, *self.marks), 0, 0.4),
                      *during(edit(B, C), 0.3, 1.0), run_time=min(2.4, c.until("same") - 0.1))
            c.wait_until("same")
            self.play(TransformFromCopy(den1.rect, grect), FlashAround(den1, color=GREEN, time_width=1.5),
                      run_time=1.8)
            c.wait_until("route", nth=0)
            self.play(*appear(same), run_time=1.0)
            c.wait_until("answer2")
            self.play(*during(disappear(self.route), 0, 0.4),
                      *during(appear(a2.formula, shift=None), 0.2, 0.8),
                      *during([GrowFromCenter(a2.box)], 0.5, 1.0), run_time=1.6)
            self.play(*appear(a2.label), run_time=0.9)  # early: the result's name
        self.C, self.grect, self.same, self.ans2 = C, grect, same, a2

    # ------------------------------------------------------------------ c7.h4two.3
    def clip3(self):
        a1, a2 = self.ans1, self.ans2
        pair = answers_pair()
        p1, p2 = pair.ans1, pair.ans2
        m = self.m
        E1 = m.squared(m.boxed(m.lhs_tex(44), BLUE), 44)
        E2 = MathTex(r"\overset{?}{=}", font_size=48, color=YELLOW)
        E3 = MathTex(r"\frac{1}{x^2}", font_size=48)
        E1.move_to([X_I, -1.15, 0])
        E3.move_to([X_II, -1.15, 0])
        E2.move_to([0, -1.15, 0])
        E2b = MathTex("=", font_size=48, color=GREEN).move_to(E2)
        F = VGroup(m.boxed(m.lhs_tex(44), BLUE), MathTex("=", font_size=44),
                   MathTex(r"\frac{1}{x}", font_size=44)).arrange(RIGHT, buff=0.25).move_to([0, -2.85, 0])
        F2 = squared_eq(44).move_to(F)
        tick = check_mark(GREEN).next_to(self.card.frame, DOWN, buff=0.15).align_to(self.card.agree, RIGHT)
        with self.say("c7.h4two.3") as c:
            sweep_clear(self, *during([Transform(a1, p1), Transform(a2, p2)], 0.3, 1.0),
                        keep=[a1, a2, self.card], run_time=min(2.2, c.until("look") - 0.1))
            c.wait_until("look")
            num1 = a1.formula.frac.num
            self.play(FlashAround(num1, color=BLUE, time_width=1.5),
                      *during(appear(E1), 0.3, 1.0), run_time=1.5)
            c.wait_until("one over ex squared")
            self.play(FlashAround(a2.formula.frac, time_width=1.5),
                      *during(appear(E3), 0.3, 1.0), run_time=1.5)
            c.wait_until("Are they really")
            self.play(*appear(E2), run_time=1.0)
            c.wait_until("orig")
            self.play(*appear(F, shift=0.4 * DOWN), run_time=1.2)
            self.play(FlashAround(F[0], color=BLUE, time_width=1.5),
                      FlashAround(a1.formula.frac.num.inner, color=BLUE, time_width=1.5), run_time=1.5)
            c.wait_until("square")
            self.play(*swap(F, F2), run_time=1.4)
            self.play(*swap(E2, E2b), FlashAround(VGroup(E1, E3), color=GREEN, time_width=1.5),
                      run_time=1.4)
            c.wait_until("So the answers agree")
            self.play(*appear(tick, shift=None), *recolor(self.card.agree[0], GREEN), run_time=1.2)
        settle(self, self.card)
        self.E = [E1, E2b, E3, F2]
        self.tick = tick

    # ------------------------------------------------------------------ c7.h4two.4
    def clip4(self):
        a1, a2 = self.ans1, self.ans2
        Sx = row_b_tex(44).move_to([0, -1.2, 0])
        strikes = [strike(Sx[3]), strike(Sx[8])]
        W = wrong_tex().move_to([-0.9, -2.7, 0])
        xc = cross_mark(RED).move_to(self.tick)
        test = MathTex(r"y = \tfrac12", r"\quad\Rightarrow\quad", r"x \approx 0.775", font_size=44)
        test.move_to([0, -1.2, 0])
        good = [MathTex(r"\approx -0.514", font_size=40, color=GREEN)
                .next_to(a.box, DOWN, buff=0.15).align_to(a.box, RIGHT) for a in (a1, a2)]
        bad = MathTex(r"\approx -3.90", font_size=44, color=RED).next_to(W, RIGHT, buff=0.4)
        with self.say("c7.h4two.4") as c:
            sweep_clear(self, *appear(Sx, shift=None), keep=[a1, a2, self.card, self.tick],
                        run_time=1.4)
            c.wait_until("dropping")
            self.play(*[GrowFromEdge(s, DL) for s in strikes],
                      *recolor([Sx[3], Sx[8]], RED), run_time=1.5)
            c.wait_until("test")
            self.play(*appear(W), run_time=1.3)
            self.play(*swap(self.tick, xc), *recolor(self.card.agree[0], RED), run_time=1.2)
            settle(self, self.card)
            c.wait_until("At why equals")
            self.play(*during(disappear(Sx, *strikes), 0, 0.45),
                      *during(appear(test), 0.5, 1.0), run_time=1.4)
            c.wait_until("correct slope")
            self.play(*appear(*good, lag=0.2), run_time=1.2)
            c.wait_until("wrong one")
            self.play(*appear(bad), run_time=1.0)
        self.xc = xc

    # ------------------------------------------------------------------ c7.h4two.5
    def clip5(self):
        a1, a2 = self.ans1, self.ans2
        # the curve x = 1 / (y + e^y sin y), 0 < y < 3.267, stretched in x
        O = np.array([-5.6, -3.3, 0])
        ux, uy = 4.0, 1.72
        ax = Axes(x_range=[0, 1.22, 10], y_range=[0, 3.65, 10], x_length=1.22 * ux, y_length=3.65 * uy,
                  tips=True, axis_config={"color": DIM, "include_ticks": False, "stroke_width": 3})
        ax.shift(O - ax.c2p(0, 0))
        xl = MathTex("x", font_size=36).next_to(ax.x_axis.get_end(), RIGHT, buff=0.12)
        yl = MathTex("y", font_size=36).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        xmax = 1.2
        y_lo = bisect(lambda y: f_lhs(y) - 1 / xmax, 0.05, 1.0)
        y_hi = bisect(lambda y: f_lhs(y) - 1 / xmax, 2.6, 3.26)
        curve = ParametricFunction(lambda t: ax.c2p(1 / f_lhs(t), t), t_range=[y_lo, y_hi, 0.01],
                                   color=BLUE, stroke_width=5)
        y_tip, x_tip = 2.41917, 0.101535
        tip = ax.c2p(x_tip, y_tip)
        dot = Dot(tip, radius=0.1, color=YELLOW)
        y0 = 3.26650
        dash = DashedLine(ax.c2p(0, y0), ax.c2p(1.2, y0), color=DIM, dash_length=0.12, stroke_width=3)
        ylab = MathTex("2.42", font_size=30, color=GOLD).next_to(ax.c2p(0, y_tip), LEFT, buff=0.12)
        dlab = MathTex("3.27", font_size=30, color=DIM).next_to(ax.c2p(0, y0), LEFT, buff=0.12)
        vline = Line(tip + 1.0 * DOWN, tip + 1.0 * UP, color=RED, stroke_width=6)
        vtag = MathTex(r"\frac{dx}{dy} = 0:\ \text{no finite } \frac{dy}{dx}", font_size=34, color=RED)
        vtag.next_to(tip, RIGHT, buff=0.45)
        cap = VGroup(self.m.boxed(self.m.dp_tex(40), GREEN), MathTex("= 0", font_size=40))
        cap.arrange(RIGHT, buff=0.2).move_to([3.4, 2.75, 0])
        cube = cube_root_pic()
        cube.move_to([3.8, -1.3, 0])
        with self.say("c7.h4two.5", gap=1.6) as c:
            sweep_clear(self, keep=[a1, a2, self.card, self.xc], run_time=1.2)
            c.wait_until("divide")
            self.play(FlashAround(a1.formula.frac.den, color=GREEN, time_width=1.5),
                      FlashAround(a2.formula.den_box, color=GREEN, time_width=1.5), run_time=1.6)
            c.wait_until("curve")
            sweep_clear(self, FadeIn(ax), *appear(xl, yl, cap, shift=None, lag=0.1), run_time=1.4)
            self.play(Create(curve), FadeIn(dash), *appear(dlab, shift=None), run_time=2.0)
            c.wait_until("two point four")
            self.play(FadeIn(dot, scale=0.5), *appear(ylab, shift=None), run_time=1.0)
            c.wait_until("vertical")
            self.play(GrowFromCenter(vline), run_time=1.2)
            self.play(*appear(vtag, shift=None), run_time=1.0)  # early: the tag sums up this sentence
            c.wait_until("reciprocal rule")
            self.play(*appear(cube, shift=None), run_time=1.2)  # early: the cube root is named in this clause
            self.play(FlashAround(cube.tan, color=RED, time_width=1.5), run_time=min(1.4, c.until(floor=0.5)))
