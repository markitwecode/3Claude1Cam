"""Chapter 5, scene 7: area of an ellipse is pi*a*b; its circumference is not pi(a + b). Clips c5.area.1 – c5.area.3."""
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
from lib.style import *  # noqa: E402,F403

EX_UNIT = 1.25                      # scene units per unit of Example 36's ellipse
EX_CENTRE = np.array([-3.0, -0.4, 0])


def ex36_ellipse(unit=EX_UNIT, centre=EX_CENTRE, label_size=40):
    """Example 36's tall ellipse: centre (-1, 3) YELLOW, semi-minor sqrt2 along x GREEN,
    semi-major 2 along y GOLD, BLUE filled curve."""
    a, b = np.sqrt(2) * unit, 2 * unit
    ell = Ellipse(width=2 * a, height=2 * b, color=BLUE, stroke_width=5)
    ell.set_fill(BLUE, opacity=0.22).move_to(centre)
    minor = Line(centre, centre + a * RIGHT, color=GREEN, stroke_width=5)
    major = Line(centre, centre + b * UP, color=GOLD, stroke_width=5)
    dot = Dot(centre, radius=0.09, color=YELLOW)
    c_lab = MathTex(r"(-1,\,3)", font_size=label_size, color=YELLOW).next_to(dot, DL, buff=0.1)
    a_lab = MathTex(r"\sqrt{2}", font_size=label_size, color=GREEN).next_to(minor, UP, buff=0.12)
    b_lab = MathTex(r"2", font_size=label_size, color=GOLD).next_to(major, LEFT, buff=0.15)
    return VGroup(ell, minor, major, dot, c_lab, a_lab, b_lab)


def ex36_formula(size=48):
    return MathTex(r"A = \pi \cdot \sqrt{2} \cdot 2 = 2\sqrt{2}\,\pi \approx 8.9", font_size=size)


def ex36_area():
    """The filled ellipse with A = pi a b (reused by ch5_s8_recap)."""
    shape = ex36_ellipse()
    formula = ex36_formula().move_to([2.9, 0.3, 0])
    return VGroup(shape, formula)


C1 = np.array([-2.5, -0.6, 0])      # centre of the stretched circle
R0 = 1.4
SA, SB = 1.6, 1.9                   # on-screen stretch factors standing for a, b
LAB = np.array([3.7, 0.3, 0])


def grid_circle():
    circ = Circle(radius=R0, color=BLUE, stroke_width=5).set_fill(BLUE, opacity=0.18).move_to(C1)
    s, pitch = 0.26, 0.32
    sq = VGroup()
    n = int(R0 / pitch) + 1
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = (i + 0.5) * pitch, (j + 0.5) * pitch
            far = np.hypot(abs(x) + s / 2, abs(y) + s / 2)
            if far < R0 - 0.04:
                sq.add(Square(side_length=s, stroke_color=BLUE, stroke_width=1.5)
                       .set_fill(BLUE, opacity=0.3).move_to(C1 + np.array([x, y, 0])))
    return circ, sq


def flat_arc_lengths(a, b, n=2001):
    th = np.linspace(0, 2 * PI, n)
    pts = np.stack([a * np.cos(th), b * np.sin(th)], axis=1)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    return th, np.concatenate([[0], np.cumsum(seg)])


class Area(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ area
    def clip1(self):
        with self.say("c5.area.1") as c:
            head = self.head = T("Area", 48).to_corner(UL, buff=0.6)
            self.play(*appear(head), run_time=1.0)  # early: section title
            c.wait_until("circle")

            circ, sq = grid_circle()
            rad = Line(C1, C1 + R0 * RIGHT, color=FG, stroke_width=3)
            r_lab = MathTex("1", font_size=36).next_to(rad, UP, buff=0.1)
            self.play(FadeIn(circ), LaggedStart(*[FadeIn(q) for q in sq], lag_ratio=0.01),
                      run_time=min(1.4, 0.5 * c.until("has area")))
            lab = MathTex(r"A = \pi r^2", font_size=56).move_to(LAB)
            self.play(Create(rad), *appear(r_lab, lab, lag=0.3), run_time=min(1.2, c.until("has area")))
            c.wait_until("has area")
            lab2 = MathTex(r"A = \pi r^2 = \pi", font_size=56).move_to(LAB)
            self.play(*edit(lab, lab2), run_time=min(1.5, c.until("sx")))
            c.wait_until("sx")

            # stretch along x by a
            right = C1 + (R0 + 0.12) * RIGHT
            arr_a = Arrow(right, right + 0.9 * RIGHT, buff=0, color=GOLD, stroke_width=5)
            ta = MathTex(r"\times a", font_size=40, color=GOLD).next_to(arr_a, UP, buff=0.1)
            self.play(GrowArrow(arr_a), *appear(ta), run_time=1.0)
            dx = (SA - 1) * R0 * RIGHT
            self.play(*disappear(rad, r_lab), circ.animate.stretch(SA, 0, about_point=C1),
                      *[q.animate.stretch(SA, 0, about_point=C1) for q in sq],
                      arr_a.animate.shift(dx), ta.animate.shift(dx), run_time=2.0)
            lab3 = MathTex(r"A = \pi a", font_size=56).move_to(LAB)
            c.wait_until("by that factor")
            self.play(*edit(lab2, lab3), run_time=1.5)
            c.wait_until("sy")

            # stretch along y by b
            top = C1 + (R0 + 0.12) * UP
            arr_b = Arrow(top, top + 0.8 * UP, buff=0, color=GREEN, stroke_width=5)
            tb = MathTex(r"\times b", font_size=40, color=GREEN).next_to(arr_b, RIGHT, buff=0.12)
            self.play(GrowArrow(arr_b), *appear(tb), run_time=0.7)
            dy = (SB - 1) * R0 * UP
            self.play(circ.animate.stretch(SB, 1, about_point=C1),
                      *[q.animate.stretch(SB, 1, about_point=C1) for q in sq],
                      arr_b.animate.shift(dy), tb.animate.shift(dy), run_time=2.5)
            lab4 = MathTex(r"A = \pi a b", font_size=56).move_to(LAB)
            c.wait_until("by that factor", nth=1)
            self.play(*edit(lab3, lab4), run_time=1.5)
            c.wait_until("formula")

            box = SurroundingRectangle(lab4, color=YELLOW, buff=0.25)
            tag = MathTex(r"(101)", font_size=36, color=DIM).next_to(box, RIGHT, buff=0.25)
            note = T("area of an ellipse", 32, color=YELLOW).next_to(box, DOWN, buff=0.3)
            self.play(FadeIn(box), *flash([lab4]), run_time=min(1.5, c.until("that's equation")))
            self.play(*appear(note), run_time=1.0)
            c.wait_until("that's equation")
            self.play(*appear(tag), run_time=1.0)
            self.c1 = [circ, sq, arr_a, ta, arr_b, tb, lab4, box, tag, note]

    # ------------------------------------------------------------ Example 36
    def clip2(self):
        with self.say("c5.area.2") as c:
            ex = ex36_area()
            shape, formula = ex
            formula.move_to([2.9, -0.7, 0])
            circ, sq, arr_a, ta, arr_b, tb, lab4, box, tag, note = self.c1
            block = VGroup(lab4, box, tag, note)
            self.play(*disappear(circ, sq, arr_a, ta, arr_b, tb),
                      block.animate.move_to([3.4, 2.3, 0]), run_time=1.0)
            ex_lab = T("Example 36", 34, color=DIM).move_to([-3.0, 2.75, 0])
            self.play(FadeIn(shape), *appear(ex_lab, formula), run_time=1.4)
            self.play(*flash([formula[0][-3:]], color=GOLD), run_time=1.5)
            c.wait_until("circ")

            # make room: ellipse to the left, area result up to the corner, dimmed
            head2 = T("Circumference", 48).to_corner(UL, buff=0.6)
            self.play(*swap(self.head, head2), *disappear(block, ex_lab),  # early: section title
                      shape.animate.scale(0.72).move_to([-3.3, 0.5, 0]),
                      *during([formula.animate.scale(0.6).set_opacity(0.45).to_corner(UR, buff=0.6)], 0.45, 1),
                      run_time=1.5)
            self.head = head2
            small = Circle(radius=1.1, color=BLUE, stroke_width=5).move_to([3.0, 0.5, 0])
            self.play(Create(small), run_time=1.2)
            c.wait_until("two pi r")

            g_c = MathTex(r"\Gamma = 2\pi r", font_size=48).move_to([3.0, -1.9, 0])
            self.play(*appear(g_c), run_time=1.0)
            c.wait_until("you might guess")
            g_e = MathTex(r"\Gamma = \pi(a + b)", font_size=48, color=YELLOW).move_to([-3.3, -1.9, 0])
            self.play(*appear(g_e), run_time=1.0)
            c.wait_until("not")

            strike = Line(g_e.get_left() + 0.15 * LEFT, g_e.get_right() + 0.15 * RIGHT,
                          color=RED, stroke_width=6)
            note = T("the circumference of an ellipse is not Γ = π(a + b)", 32,
                     t2c={" not ": RED}, t2w={" not ": BOLD}).move_to([0, -3.25, 0])
            self.play(Create(strike), g_e.animate.set_color(RED), *appear(note), run_time=1.0)

    # ------------------------------------------------------- the flat ellipse
    def clip3(self):
        with self.say("c5.area.3") as c:
            U, CEN = 3.0, np.array([0, 0.9, 0])
            bt = ValueTracker(0.6)

            def ell():
                b = bt.get_value()
                return Ellipse(width=2 * U, height=2 * b * U, color=BLUE, stroke_width=5) \
                    .set_fill(BLUE, opacity=0.18).move_to(CEN)

            def minor():
                return Line(CEN, CEN + bt.get_value() * U * UP, color=GREEN, stroke_width=5)

            def b_lab():
                return MathTex(r"b", font_size=40, color=GREEN) \
                    .next_to(CEN + bt.get_value() * U * UP, UP, buff=0.15)

            e = always_redraw(ell)
            mn = always_redraw(minor)
            mj = Line(CEN, CEN + U * RIGHT, color=GOLD, stroke_width=5)
            a_lab = MathTex(r"a = 1", font_size=40, color=GOLD).next_to(CEN + U * RIGHT, RIGHT, buff=0.25)
            bl = always_redraw(b_lab)

            c.wait_until("almost flat")
            sweep_clear(self, time_span(FadeIn(e), 0.6, 1.4), time_span(FadeIn(mj), 0.6, 1.4),
                        time_span(FadeIn(mn), 0.6, 1.4), keep=[], run_time=1.4)
            c.wait_until("semi-major")
            self.play(*appear(a_lab), *flash([mj], color=GOLD), run_time=1.2)
            c.wait_until("semi-minor")
            self.play(*appear(bl), run_time=0.8)
            self.play(bt.animate.set_value(0.035), run_time=max(1.0, min(3.0, c.until("around") - 0.2)))
            c.wait_until("around")

            # a dot runs round; a counter climbs with the distance travelled
            b = bt.get_value()
            th, L = flat_arc_lengths(1.0, b)
            tt = ValueTracker(0)
            dot = always_redraw(lambda: Dot(CEN + U * np.array([np.cos(tt.get_value()),
                                                                b * np.sin(tt.get_value()), 0]),
                                            radius=0.11, color=GOLD))
            gl = MathTex(r"\text{round} \approx", font_size=44, color=GOLD)
            num = DecimalNumber(0, num_decimal_places=1, font_size=44, color=GOLD)
            num.add_updater(lambda m: m.set_value(float(np.interp(tt.get_value(), th, L))))
            row = VGroup(gl, num).arrange(RIGHT, buff=0.2).move_to([-3.0, -1.4, 0])
            num.next_to(gl, RIGHT, buff=0.2)
            self.play(FadeIn(dot), *appear(gl, num), run_time=0.8)
            self.play(tt.animate.set_value(2 * PI), run_time=max(2.0, min(5.0, c.until("guessval") - 0.3)),
                      rate_func=linear)
            num.clear_updaters()
            num.set_value(float(L[-1]))
            c.wait_until("guessval")

            guess = MathTex(r"\pi(1 + 0) \approx 3.14", font_size=44, color=RED).move_to([3.0, -1.4, 0])
            self.play(*appear(guess), run_time=1.0)
            note = T("it needs ‘elliptic integrals’", 32).move_to([0, -2.9, 0])
            c.wait_until("true circumference")
            self.play(*appear(note), run_time=1.0)
            self.mobs3 = [row]
