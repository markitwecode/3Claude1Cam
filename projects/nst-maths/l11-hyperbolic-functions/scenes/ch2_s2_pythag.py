"""Chapter 2, scene 2: cosh^2 - sinh^2 = 1, derived from the definitions. Clips c2.pythag.1 - c2.pythag.4.

Layout: (84) | (85) on top; derivation rows A, B, C below on one "=" column; (93) boxed at the
bottom. Clip 4 clears the working, puts (93) beside the circle identity, then the
circle / hyperbola pair below them.

Shared groups (reused later): result_group() -> VGroup(R93, box): (93) all TEAL, font 52, YELLOW
box buff 0.25.  circle_pair() is built in construct (BLUE circle, TEAL hyperbola, DIM dashed asymptotes).
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
from lib.style import *  # noqa: E402,F403

SINH_C = "#A8EBD9"          # ch1 s2's lighter teal for sinh
ROW = 40                    # derivation font size


def bracket_colour(part, minus_color=FG):
    """part = MathTex piece '\\left(e^{x} ± e^{-x}\\right)[^2]': ( e x ± e - x ) [2]."""
    part[1:3].set_color(GOLD)
    part[4:7].set_color(PURPLE)
    part[3].set_color(minus_color)
    return part


def defs():
    d84 = MathTex(r"\cosh x", "=", r"\frac{1}{2}", r"\left(e^{x} + e^{-x}\right)", font_size=44)
    d85 = MathTex(r"\sinh x", "=", r"\frac{1}{2}", r"\left(e^{x} - e^{-x}\right)", font_size=44)
    d84[0][0:4].set_color(TEAL)
    d85[0][0:4].set_color(SINH_C)
    bracket_colour(d84[3])
    bracket_colour(d85[3])
    return d84, d85


TOP84, TOP85 = np.array([-3.4, 3.15, 0]), np.array([3.4, 3.15, 0])


def carry(src, dst, t_in=0.55, t_out=0.8, dst_in=0.84, hfirst=False):
    """A faint copy of src leaves it, travels to dst and hands over to dst (src stays)."""
    cp = src.copy()
    a0, a1 = cp.get_center(), dst.get_center()

    def upd(m, a):
        if hfirst:      # across first, then down: keeps clear of the row it lands in
            d = a1 - a0
            m.move_to(a0 + np.array([d[0] * smooth(min(1, 1.6 * a)), d[1] * smooth(max(0, 1.6 * a - 0.6)), 0]))
        else:
            m.move_to(a0 + (a1 - a0) * smooth(a))
        op = np.clip((a - t_in) / 0.2, 0, 1) * (1 - np.clip((a - t_out) / 0.1, 0, 1))
        m.set_opacity(op)

    cp.set_opacity(0)
    return [UpdateFromAlphaFunc(cp, upd, remover=True), *during([FadeIn(dst)], dst_in, 1.0)]


def result_group():
    r = MathTex(r"\cosh^2 x", "-", r"\sinh^2 x", r"\equiv", "1", font_size=52, color=TEAL)
    box = SurroundingRectangle(r, color=YELLOW, buff=0.25)
    return VGroup(r, box)


class Pythag(NarratedScene):
    def construct(self):
        d84, d85 = defs()
        d84.scale(52 / 44).move_to([0, 1.0, 0])      # alone first, centred and big
        d85.scale(52 / 44)
        d85.shift([d84[1].get_x() - d85[1].get_x(), -0.8 - d85.get_y(), 0])

        A = MathTex(r"\cosh^2 x - \sinh^2 x", "=", r"\frac{1}{4}", r"\left(e^{x} + e^{-x}\right)^{2}",
                    "-", r"\frac{1}{4}", r"\left(e^{x} - e^{-x}\right)^{2}", font_size=ROW)
        A[0][0:4].set_color(TEAL)
        A[0][7:11].set_color(SINH_C)
        bracket_colour(A[3])
        bracket_colour(A[6])
        B = MathTex("=", r"\frac{1}{4}", r"\Big[", "(", "e^{2x}", "+", "2", "+", "e^{-2x}", ")", "-",
                    "(", "e^{2x}", "-", "2", "+", "e^{-2x}", ")", r"\Big]", font_size=ROW)
        for i in (4, 12):
            B[i].set_color(GOLD)
        for i in (8, 16):
            B[i].set_color(PURPLE)
        C = MathTex("=", r"\frac{1}{4}", r"\cdot", "4", "=", "1", font_size=ROW)
        A.move_to([0, 1.65, 0])
        B.shift([A[1].get_x() - B[0].get_x(), 0.35 - B.get_y(), 0])
        C.shift([A[1].get_x() - C[0].get_x(), -0.9 - C.get_y(), 0])
        block = VGroup(A, B, C)
        dx = -block.get_center()[0]
        block.shift(dx * RIGHT)

        X = MathTex("2", r"\cdot", "e^{x}", r"\cdot", "e^{-x}", "=", "2", r"\cdot", "e^{0}", "=", "2",
                    font_size=ROW)
        X[2].set_color(GOLD)
        X[4].set_color(PURPLE)
        X[10].set_color(GOLD)
        X.move_to([0, -0.9, 0])

        res = result_group()
        R, box = res
        res.move_to([0, -2.2, 0])
        ident = T("identity: true for every x", size=30, color=FG, t2s={"x": ITALIC})
        ident.next_to(box, DOWN, buff=0.22)

        # ---------------------------------------------------------------- clip 1
        with self.say("c2.pythag.1") as c:
            self.play(*appear(d84), run_time=1.0)
            c.wait_until("cosh")
            self.play(FlashAround(d84[3][1:3], color=GOLD, time_width=1.5),
                      FlashAround(d84[3][4:7], color=PURPLE, time_width=1.5),
                      run_time=min(2.0, 0.6 * c.until("sinh")))
            c.wait_until("sinh")
            self.play(*appear(d85), run_time=1.0)
            self.play(FlashAround(d85[3][3], time_width=1.5), *recolor([d85[3][3]], YELLOW),
                      run_time=1.5)
            c.wait_until("square")
            self.play(*during([d84.animate.scale(44 / 52).move_to(TOP84),
                               d85.animate.scale(44 / 52).move_to(TOP85)], 0, 0.6),
                      *during(appear(A[0], A[1]), 0.55, 1.0), run_time=1.8)
            self.play(*carry(d84[3], A[3]), *carry(d85[3], A[6]), *appear(A[4], shift=None),
                      run_time=1.6)
            c.wait_until("quarter")
            h1 = MathTex(r"\frac{1}{2}", font_size=ROW).move_to(A[2])
            h2 = MathTex(r"\frac{1}{2}", font_size=ROW).move_to(A[5])
            self.play(*flash([d84[2], d85[2]]), *appear(h1, h2, shift=None, lag=0), run_time=0.9)
            self.play(*swap(h1, A[2]), *swap(h2, A[5]), run_time=1.1)
        settle(self, A)

        # ---------------------------------------------------------------- clip 2
        with self.say("c2.pythag.2") as c:
            self.play(*appear(B[0], B[1], B[2], B[3], B[9], B[10], B[11], B[17], B[18], lag=0.08),
                      run_time=min(1.2, c.until("ends")))
            c.wait_until("ends")
            self.play(*carry(A[3][1:3], B[4]), run_time=1.6)
            c.wait_until("and e to the minus ex")
            self.play(*carry(A[3][4:7], B[8]), run_time=1.6)
            c.wait_until("middle")
            self.play(*appear(X[0], X[1], X[2], X[3], X[4], lag=0.1), run_time=1.2)
            c.wait_until("their exponents cancel")
            self.play(*appear(X[5], X[6], X[7], X[8], lag=0.1), run_time=1.0)
            c.wait_until("product is one")
            self.play(*appear(X[9], X[10], lag=0.15), run_time=1.0)
            c.wait_until("just two")
            self.play(*carry(X[10], B[6]), *appear(B[5], B[7], shift=None), run_time=1.5)
            c.wait_until("second")
            self.play(*appear(B[12], B[13], B[14], B[15], B[16], lag=0.12), run_time=1.0)
            self.play(FlashAround(VGroup(B[13], B[14]), time_width=1.5), run_time=1.5)
        settle(self, B)

        # ---------------------------------------------------------------- clip 3
        with self.say("c2.pythag.3") as c:
            self.play(*disappear(X), FlashAround(B[10], time_width=1.5),
                      run_time=min(1.2, c.until("cancel")))
            c.wait_until("cancel")

            def strike(g):
                return Line(g.get_corner(DL) + 0.06 * DL, g.get_corner(UR) + 0.06 * UR,
                            color=RED, stroke_width=4)

            s1, s2 = strike(B[4]), strike(B[12])
            self.play(Create(s1), Create(s2), *set_alpha([B[4], B[12]], 0.4), run_time=1.2)
            c.wait_until("and so do")
            s3, s4 = strike(B[8]), strike(B[16])
            self.play(Create(s3), Create(s4), *set_alpha([B[8], B[16]], 0.4), run_time=1.2)
            c.wait_until("four")
            self.play(*recolor([B[13]], YELLOW), *flash([B[6], VGroup(B[10], B[13], B[14])]),
                      run_time=1.5)
            c.wait_until("that makes four")
            self.play(*appear(C[0], C[1], C[2], shift=None), *carry(B[6], C[3], 0.4, 0.6, 0.7),
                      *carry(VGroup(B[13], B[14]), C[3], 0.4, 0.6, 0.7)[:1], run_time=1.6)
            c.wait_until("a quarter of four")
            self.play(*appear(C[4], C[5], lag=0.2), run_time=1.0)
            settle(self, C)
            c.wait_until("result")
            self.play(*appear(R), run_time=1.2)
            self.play(GrowFromCenter(box), run_time=0.8)
            c.wait_until("identity")
            self.play(FlashAround(R[3], time_width=1.5), run_time=1.5)
            c.wait_until(own_word=ident)
            self.play(*appear(ident), run_time=1.0)

        # ---------------------------------------------------------------- clip 4
        circ_id = MathTex(r"\cos^2 x", "+", r"\sin^2 x", r"\equiv", "1", font_size=52, color=BLUE)
        y_cmp = 0.4
        circ_id.move_to([-3.4, y_cmp, 0])
        res_pos = np.array([3.4, y_cmp, 0])
        note = T("comp. sin²θ + cos²θ = 1", size=30, color=DIM, slant=ITALIC)
        note.rotate(4 * DEGREES)

        with self.say("c2.pythag.4") as c:
            sweep_clear(self, VGroup(res, ident).animate.move_to(res_pos + 0.4 * DOWN), *appear(circ_id), keep=[res, ident],
                        run_time=min(2.2, c.until("plus")))
            note.next_to(ident, DOWN, buff=0.35)
            c.wait_until("plus")
            self.play(FlashAround(circ_id[1], time_width=1.5), *recolor([circ_id[1]], YELLOW), run_time=1.5)
            c.wait_until("minus")
            self.play(FlashAround(R[1], time_width=1.5), *recolor([R[1]], YELLOW), run_time=1.5)
            self.play(*appear(note), run_time=1.0)  # early: the lecturer's margin note, quoted not read

            # ---- the picture
            c.wait_until("curve")
            top = 2.95
            cc = np.array([-3.3, -0.9, 0])
            hc = np.array([3.4, -0.9, 0])
            rad = 1.3
            axes_c = VGroup(Line(cc + 1.8 * LEFT, cc + 1.8 * RIGHT), Line(cc + 1.7 * DOWN, cc + 1.7 * UP))
            axes_h = VGroup(Line(hc + 2.6 * LEFT, hc + 2.6 * RIGHT), Line(hc + 2.1 * DOWN, hc + 2.1 * UP))
            for ax in (axes_c, axes_h):
                ax.set_stroke(DIM, 2, opacity=0.5)
            circle = Circle(radius=rad, color=BLUE, stroke_width=4).move_to(cc)
            c_eq = set_backstroke(MathTex("x^2 + y^2 = 1", font_size=34, color=BLUE)).move_to(cc + 0.45 * DOWN)
            self.play(circ_id.animate.scale(0.8).move_to([-3.4, top, 0]),
                      res.animate.scale(0.8).move_to([3.4, top, 0]),
                      run_time=1.5)
            self.play(FadeIn(axes_c), Create(circle), *disappear(note, ident), run_time=1.5)

            c.wait_until("the point with coordinates cosine")
            th = ValueTracker(0.0)

            def cpos():
                a = th.get_value()
                return cc + rad * np.array([np.cos(a), np.sin(a), 0])

            cdot = Dot(cpos(), radius=0.09, color=YELLOW)
            cdot.add_updater(lambda m: m.move_to(cpos()))
            clab = set_backstroke(MathTex(r"(\cos\theta, \sin\theta)", font_size=34, color=YELLOW))

            def place_clab(m):
                a = th.get_value()
                m.next_to(cpos(), np.array([np.cos(a), np.sin(a), 0]), buff=0.18)

            place_clab(clab)
            clab.add_updater(place_clab)
            self.play(FadeIn(cdot), *appear(clab, shift=None), *appear(c_eq), run_time=1.0)
            self.play(th.animate.set_value(TAU), rate_func=linear,
                      run_time=max(1.0, min(6.0, c.until("hyper") - 0.3)))

            c.wait_until("hyper")
            # each branch grows out of its vertex, up and down at once (no stray ends drawn first)
            halves = [ParametricFunction(lambda t, sx=sx, sy=sy: hc + np.array([sx * np.cosh(t), sy * np.sinh(t), 0]),
                                         t_range=[0, 1.3], color=TEAL, stroke_width=4)
                      for sx in (1, -1) for sy in (1, -1)]
            asym = VGroup(DashedLine(hc + 2.1 * (DL), hc + 2.1 * (UR), dash_length=0.12),
                          DashedLine(hc + 2.1 * (UL), hc + 2.1 * (DR), dash_length=0.12))
            asym.set_stroke(DIM, 2, opacity=0.6)
            h_eq = set_backstroke(MathTex("x^2 - y^2 = 1", font_size=34, color=TEAL)).move_to(hc + 2.45 * UP)
            self.play(FadeIn(axes_h), FadeIn(asym), *set_alpha([cdot, clab], 0.35), run_time=0.8)
            self.play(*[Create(hb) for hb in halves], run_time=1.2)
            tt = ValueTracker(0.0)

            def hpos():
                t = tt.get_value()
                return hc + np.array([np.cosh(t), np.sinh(t), 0])

            hdot = Dot(hpos(), radius=0.09, color=YELLOW)
            hdot.add_updater(lambda m: m.move_to(hpos()))
            hlab = set_backstroke(MathTex(r"(\cosh\theta, \sinh\theta)", font_size=34, color=YELLOW))
            hlab.add_updater(lambda m: m.next_to(hpos(), LEFT, buff=0.2))
            hlab.next_to(hpos(), LEFT, buff=0.2)
            self.play(FadeIn(hdot), *appear(hlab, shift=None), *appear(h_eq), run_time=1.0)
            self.play(tt.animate.set_value(1.2), run_time=1.5)
            self.play(tt.animate.set_value(-1.2), run_time=min(2.5, max(1.0, c.until("name") - 0.2)))

            c.wait_until("name")
            hname = T("hyperbola", size=36, color=TEAL)
            tag_t = T("part 6", size=30, color=DIM)
            tag = VGroup(SurroundingRectangle(tag_t, color=DIM, buff=0.12, corner_radius=0.08,
                                              stroke_width=2), tag_t)
            tag.next_to(hname, RIGHT, buff=0.35)
            VGroup(hname, tag).move_to([hc[0], -3.15, 0])
            c.wait_until(own_word=hname)
            self.play(*appear(hname), run_time=1.0)
            self.play(*appear(tag), run_time=1.0)  # early: the chapter tag sits by its name; 'part six' comes in the next breath

        for m in (cdot, clab, hdot, hlab):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
