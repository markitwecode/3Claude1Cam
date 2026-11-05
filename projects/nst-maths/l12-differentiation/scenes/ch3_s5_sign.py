"""Chapter 3, scene 5: the sign of cos y, and Example 41's answer. Clips c3.sign.1 – c3.sign.5."""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

TOP_Y = 3.1          # the top row: the line to finish (left), the identity (right)
TOP_SIZE = 40
GX, GY = -2.2, -0.4  # the sine graph's centre
PX = 4.6             # right panel centre


def mt(*parts, size=40, color=FG):
    return MathTex(*parts, font_size=size, color=color)


def triangle():
    """Ex 41's right triangle: right angle bottom right, sides 1 (bottom) and x (right), hypotenuse
    sqrt(1 + x^2), angle y at the left corner (YELLOW arc and y). VGroup at ORIGIN, about 4.6 x 3.1;
    parts .tri .right_angle .one .x .hyp .arc .y."""
    w, h = 3.2, 2.2
    A, B, C = np.array([-w / 2, -h / 2, 0]), np.array([w / 2, -h / 2, 0]), np.array([w / 2, h / 2, 0])
    tri = Polygon(A, B, C).set_stroke(BLUE, 4).set_fill(BLUE, 0.08)
    s = 0.28
    right_angle = VMobject().set_points_as_corners([B + s * LEFT, B + s * LEFT + s * UP, B + s * UP])
    right_angle.set_stroke(FG, 2.5)
    one = mt("1", size=40).next_to(Line(A, B), DOWN, buff=0.2)
    x = mt("x", size=40).next_to(Line(B, C), RIGHT, buff=0.2)
    hyp = mt(r"\sqrt{1 + x^2}", size=40)
    normal = np.array([-h, w, 0]) / np.hypot(w, h)
    hyp.move_to((A + C) / 2 + normal * 0.62)
    ang = np.arctan2(h, w)
    arc = Arc(radius=0.75, start_angle=0, angle=ang, arc_center=A).set_stroke(YELLOW, 4)
    y = mt("y", size=40, color=YELLOW).move_to(A + 1.1 * np.array([np.cos(ang / 2), np.sin(ang / 2), 0]))
    g = VGroup(tri, right_angle, one, x, hyp, arc, y)
    g.move_to(ORIGIN)
    g.tri, g.right_angle, g.one, g.x, g.hyp, g.arc, g.y = tri, right_angle, one, x, hyp, arc, y
    return g


def answer_box(size=48):
    """Ex 41's boxed answer dy/dx = 1/(1 + x^2), dy/dx GREEN, YELLOW box (stroke 3, buff 0.3),
    VGroup at ORIGIN; parts .rect .formula (3 parts: dy/dx, =, 1/(1 + x^2))."""
    formula = mt(r"\dfrac{dy}{dx}", "=", r"\dfrac{1}{1 + x^2}", size=size)
    formula[0].set_color(GREEN)
    rect = SurroundingRectangle(formula, color=YELLOW, buff=0.3).set_stroke(YELLOW, 3)
    g = VGroup(rect, formula)
    g.move_to(ORIGIN)
    g.rect, g.formula = rect, formula
    return g


def wavy_under(mob, color=YELLOW, buff=0.14, amp=0.05, waves=None):
    w = mob.width
    n = waves or max(3, int(round(w / 0.22)))
    curve = ParametricFunction(lambda t: np.array([t, amp * np.sin(2 * PI * n * t / w), 0]),
                               t_range=[0, w]).set_stroke(color, 3)
    curve.move_to(mob.get_bottom() + (buff + amp) * DOWN)
    return curve


def split_pm(part):
    """Rebuild the single +- glyph of a MathTex part as a + over a - (each its own glyph, sized to
    the original's box), so the two signs can be coloured and struck separately. Returns (plus, minus)."""
    g = part[0]
    col = g.get_fill_color()
    plus = MathTex("+")[0][0]
    minus = MathTex("-")[0][0]
    for m in (plus, minus):
        m.set_fill(col, 1).set_stroke(width=0)
        m.stretch_to_fit_width(g.width)
    plus.stretch_to_fit_height(g.height * 0.78).move_to(g, aligned_edge=UP)
    minus.move_to(g, aligned_edge=DOWN)
    part.remove(g)
    part.add(plus, minus)
    return plus, minus


class Sign(NarratedScene):
    def construct(self):
        self.need()
        self.range()
        self.strict()
        self.substitute()
        self.check()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- clip 1
    def need(self):
        shot = load_scene("ch3_s4_tripos").handover_shot()
        self.add(shot)
        self.remove(shot)
        box, L = shot.box, shot.line
        self.add(box, L)
        self.L = L
        with self.say("c3.sign.1") as c:
            L.generate_target()
            L.target.scale(TOP_SIZE / 56).to_edge(LEFT, buff=0.5).set_y(TOP_Y)
            self.play(*during(disappear(box), 0, 0.45), *during([MoveToTarget(L)], 0.4, 1), run_time=1.6)
            self.wavy = wavy_under(L[0])
            c.wait_until("cosine")
            self.play(Create(self.wavy), run_time=1.0)
            note = T("Need cos y in terms of x.", 32, slant=ITALIC)
            note.next_to(L, RIGHT, buff=0.8).set_y(TOP_Y)
            self.note = note
            c.wait_until(own_word=note)
            self.play(*appear(note), run_time=1.0)

            P = mt(r"\cos^2 y + \sin^2 y = 1", size=48).move_to([0, 1.0, 0])
            I = mt(r"\cos y", "=", r"\pm", r"\sqrt{1 - \sin^2 y}", size=56).move_to([0, -0.6, 0])
            I[2].set_color(YELLOW)
            self.plus, self.minus = split_pm(I[2])
            self.P, self.I = P, I
            c.wait_until("identity")
            self.play(*appear(P), run_time=1.2)
            c.wait_until("so cosine of why")
            self.play(*appear(I), run_time=1.5)

            q = mt("?", size=56, color=YELLOW).next_to(I[2], UP, buff=0.35)
            self.q = q
            c.wait_until("which")
            self.play(*appear(q), FlashAround(I[2], run_time=1.2, time_width=1.5), run_time=1.2)

            tag = T("most students slipped here", 30, RED).move_to([I[2].get_x() + 0.6, -2.4, 0])
            arrow = Arrow(tag.get_top() + 0.6 * LEFT, I[2].get_bottom(), buff=0.12, color=RED,
                          stroke_width=4, max_tip_length_to_length_ratio=0.3)
            self.tag = VGroup(tag, arrow)
            c.wait_until("where")
            self.play(*appear(tag), GrowArrow(arrow), run_time=1.0)

    # ---------------------------------------------------------------- clip 2
    def range(self):
        I = self.I
        with self.say("c3.sign.2") as c:
            I.generate_target()
            I.target.scale(TOP_SIZE / 56).to_edge(RIGHT, buff=0.5).set_y(TOP_Y)
            self.play(*during(disappear(self.note, self.P, self.q, self.tag), 0, 0.45),
                      *during([MoveToTarget(I)], 0.4, 1), run_time=1.6)

            ax = Axes(x_range=[-PI, PI, PI / 2], y_range=[-1.25, 1.25, 1], x_length=7.6, y_length=3.0,
                      tips=False, axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False})
            ax.move_to([GX, GY, 0])
            ylab = mt("y", size=36, color=DIM).next_to(ax.x_axis.get_right(), RIGHT, buff=0.15)
            sine = ax.plot(np.sin, x_range=[-PI, PI]).set_stroke(BLUE, 4)
            slab = mt(r"\sin y", size=36, color=BLUE).move_to(ax.c2p(-2.4, 0.95))
            self.ax, self.sine = ax, sine
            self.play(FadeIn(ax), FadeIn(ylab), run_time=0.8)
            self.play(Create(sine), *appear(slab), run_time=1.5)
            self.graph = [ax, ylab, sine, slab]

            hline = Line(ax.c2p(-PI, 0.5), ax.c2p(PI, 0.5)).set_stroke(YELLOW, 3)
            d1 = Dot(ax.c2p(PI / 6, 0.5), radius=0.1, color=RED)
            d2 = Dot(ax.c2p(5 * PI / 6, 0.5), radius=0.1, color=RED)
            c.wait_until("wiggle")
            self.play(Create(hline), run_time=1.2)
            c.wait_until("undone")
            self.play(FadeIn(d1, scale=0.5), FadeIn(d2, scale=0.5), run_time=0.8)

            piece = ax.plot(np.sin, x_range=[-PI / 2, PI / 2]).set_stroke(BLUE, 7)
            ticks = VGroup(*[mt(t, size=32, color=DIM).next_to(ax.c2p(v, 0), DOWN, buff=0.2)
                             for t, v in [(r"-\tfrac{\pi}{2}", -PI / 2), (r"\tfrac{\pi}{2}", PI / 2)]])
            ticks[0].shift(0.3 * RIGHT)
            ticks[1].shift(0.15 * RIGHT)
            self.piece = piece
            c.wait_until("piece")
            self.play(restyle(sine, 0.25), Create(piece), FadeOut(d2), run_time=1.6)
            c.wait_until("minus pi")
            self.play(*appear(ticks, lag=0.3), run_time=1.0)
            board = mt(r"\sin^{-1} \text{ takes values in } \left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right]",
                       size=40).move_to([GX, -3.0, 0])
            c.wait_until("gives angles")
            self.play(*appear(board), run_time=1.0)

            cosg = ax.plot(np.cos, x_range=[-PI / 2, PI / 2])
            area = ax.get_area(cosg, x_range=[-PI / 2, PI / 2], color=GREEN, opacity=0.2)
            cosd = DashedVMobject(cosg.copy().set_stroke(FG, 3), num_dashes=30)
            cnote = mt(r"\text{so } \cos y \ge 0", size=40).move_to([PX, 0.9, 0])
            c.wait_until("cos")
            self.play(Create(cosd), FadeIn(area), run_time=1.2)
            self.play(*appear(cnote), run_time=0.9)
            self.graph += [hline, d1, piece, ticks, board, cosd, area, cnote]

    # ---------------------------------------------------------------- clip 3
    def strict(self):
        ax, I = self.ax, self.I
        with self.say("c3.sign.3") as c:
            ineq = mt(r"\left|\dfrac{x}{\sqrt{1 + x^2}}\right| < 1", size=40).move_to([PX, -0.4, 0])
            since = mt(r"\text{since } \sqrt{1 + x^2} > |x|", size=34).move_to([PX, -1.6, 0])
            self.play(*appear(ineq), run_time=1.2)
            c.wait_until("because")
            self.play(*appear(since), run_time=1.0)

            ends = VGroup(*[Circle(radius=0.11).set_stroke(RED, 3).set_fill(BG, 1).move_to(ax.c2p(v, s))
                            for v, s in [(-PI / 2, -1), (PI / 2, 1)]])
            c.wait_until("inside")
            self.play(*[FadeIn(e, scale=0.5) for e in ends], run_time=1.0)
            pos = mt(r"\cos y > 0", size=44, color=GREEN).move_to([PX, -2.7, 0])
            c.wait_until("positive")
            self.play(*appear(pos), run_time=1.0)
            self.graph += [ineq, since, ends, pos]

            div = mt(r"\div \cos y", size=34, color=YELLOW)
            gap_l, gap_r = self.L.get_right()[0], I.get_left()[0]
            div.move_to([(gap_l + gap_r) / 2 + 0.4, TOP_Y, 0])
            darrow = Arrow(div.get_left(), [gap_l, TOP_Y, 0], buff=0.15, color=YELLOW, stroke_width=4,
                           max_tip_length_to_length_ratio=0.3)
            self.div = VGroup(div, darrow)
            c.wait_until("divide")
            self.play(*appear(div, shift=None), GrowArrow(darrow), run_time=1.2)

            c.wait_until("plus")
            if self.minus is not None:
                self.play(*recolor(self.plus, GREEN), FlashAround(self.plus, run_time=0.8), run_time=0.8)
                c.wait_until("reject")
                self.play(self.minus.animate.shift(0.3 * DOWN).set_color(RED), run_time=0.6)
                m = self.minus.get_center()
                strike = Line(m + np.array([-0.15, -0.09, 0]), m + np.array([0.15, 0.09, 0])).set_stroke(RED, 4)
                self.play(Create(strike), run_time=0.6)
            else:
                strike = Cross(I[2], stroke_color=RED, stroke_width=3, scale_factor=0.6)
                self.play(*recolor(I[2], GREEN), run_time=0.8)
                c.wait_until("reject")
                self.play(Create(strike), run_time=0.8)
            self.strike = strike

    # ---------------------------------------------------------------- clip 4
    def substitute(self):
        L, I = self.L, self.I
        with self.say("c3.sign.4") as c:
            R = mt(r"\sin y", "=", r"\dfrac{x}{\sqrt{1 + x^2}}", size=36)
            R.next_to(I, DOWN, buff=0.35).align_to(I, RIGHT)
            sweep_clear(self, time_span(FadeIn(R, shift=0.2 * DOWN), 0.7, 1.4), keep=[L, I, self.strike],
                        run_time=1.4)
            self.play(FlashAround(I[3], run_time=1.5, time_width=1.5))

            S = mt(r"\cos y", "=", "+", r"\sqrt{1 - \dfrac{", "x^2", r"}{1 + x^2}}", "=",
                   r"\sqrt{\dfrac{1}{1 + x^2}}", size=44)
            S[2].set_color(GREEN)
            S.move_to([0, 0.2, 0])
            c.wait_until("cosine of why is")
            self.play(*appear(*S[0:6], lag=0.1, shift=None), run_time=1.6)
            c.wait_until("common")
            self.play(*recolor(S[4], YELLOW), *recolor(R[2][0], YELLOW),
                      FlashAround(S[4], run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("cancels")
            self.play(*appear(S[6], S[7], lag=0.2, shift=None), run_time=1.2)
            settle(self, S)

            Q = mt("=", r"\dfrac{1}{\sqrt{1 + x^2}}", size=44)
            Q[1].set_color(GREEN)
            Q.move_to([0, -1.35, 0])
            Q.shift((S[6].get_x() - Q[0].get_x()) * RIGHT)
            c.wait_until("simplify")
            self.play(*appear(Q), run_time=1.2)

            D = mt(r"\dfrac{dy}{dx}", "=", r"\dfrac{(1 + x^2)^{", "1/2", r"}}{(1 + x^2)^{", "3/2", "}}",
                   size=44)
            D[0].set_color(GREEN)
            D[3].set_color(GOLD)
            D[5].set_color(GOLD)
            D.move_to([0, -2.85, 0])
            c.wait_until("divide2")
            self.play(FlashAround(L, run_time=1.2, time_width=1.5), *appear(D), run_time=1.5)

            ab = answer_box()
            ab.move_to(D)
            self.ab = ab
            c.wait_until("answer")
            self.play(*edit(D, ab.formula), run_time=1.5)
            self.play(FadeIn(ab.rect), run_time=0.8)
            settle(self, ab)

    # ---------------------------------------------------------------- clip 5
    def check(self):
        ab = self.ab
        with self.say("c3.sign.5") as c:
            ab.generate_target()
            ab.target.move_to([-3.6, 2.0, 0])
            ghost = mt(r"-\dfrac{1}{1 + x^2}", size=48, color=RED).set_opacity(0.6)
            ghost.move_to([-0.4, 2.0, 0])
            sweep_clear(self, MoveToTarget(ab), time_span(FadeIn(ghost), 1.0, 1.4), keep=[ab], run_time=1.4)

            pax = Axes(x_range=[-5, 5, 1], y_range=[-2, 2, 1], x_length=4.4, y_length=2.6, tips=False,
                       axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False})
            pax.move_to([4.2, 1.7, 0])
            pxl = mt("x", size=30, color=DIM).next_to(pax.x_axis.get_right(), RIGHT, buff=0.12)
            pyl = mt("y", size=30, color=DIM).next_to(pax.y_axis.get_top(), RIGHT, buff=0.12)
            curve = pax.plot(np.arctan, x_range=[-5, 5]).set_stroke(BLUE, 4)
            tang = Line(pax.c2p(-1.4, -1.4), pax.c2p(1.4, 1.4)).set_stroke(GREEN, 4)
            gstrike = Line(ghost.get_corner(DL), ghost.get_corner(UR)).set_stroke(RED, 5)
            c.wait_until("check")
            self.play(FadeIn(pax), FadeIn(pxl), FadeIn(pyl), Create(curve), run_time=1.5)
            self.play(Create(tang), Create(gstrike), ghost.animate.set_opacity(0.35), run_time=1.0)
            plot = VGroup(pax, pxl, pyl, curve, tang)

            note = mt(r"\textit{(in fact } y = \tan^{-1} x\textit{)}", size=36).move_to([-3.6, 0.45, 0])
            c.wait_until("note")
            self.play(*appear(note), run_time=1.0)

            tri = triangle().move_to([-3.6, -2.1, 0])
            c.wait_until("draw")
            self.play(*set_alpha([plot, ghost, gstrike], 0.4), Create(tri.tri), run_time=1.5)
            self.play(Create(tri.right_angle), *appear(tri.one, tri.x, lag=0.3), run_time=1.2)
            c.wait_until("hypotenuse")
            self.play(*appear(tri.hyp), Create(tri.arc), *appear(tri.y), run_time=1.2)

            sin_row = mt(r"\sin y", "=", r"\dfrac{x}{\sqrt{1 + x^2}}", size=40)
            sin_row.move_to([0.4, -1.3, 0], aligned_edge=LEFT)
            c.wait_until("sin")
            self.play(*appear(sin_row), *flash([tri.x, tri.hyp]), run_time=1.5)

            tan_row = mt(r"\tan y", "=", r"\dfrac{x}{1}", "=", "x", size=40)
            tan_row.move_to([0.4, -2.8, 0], aligned_edge=LEFT)
            final = mt(r"\Rightarrow\; y = \tan^{-1} x", size=40, color=YELLOW).next_to(tan_row, RIGHT, buff=0.5)
            c.wait_until("tan")
            self.play(*appear(tan_row), *flash([tri.x, tri.one]), run_time=1.5)
            c.wait_until("which is")
            self.play(*appear(final), run_time=1.0)
        self.wait(1.5)
