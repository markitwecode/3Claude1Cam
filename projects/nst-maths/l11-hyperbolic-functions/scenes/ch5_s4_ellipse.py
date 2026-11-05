"""Chapter 5, scene 4: a stretched circle, the ellipse (x/a)^2 + (y/b)^2 = 1. Clips c5.ellipse.1 – c5.ellipse.4.

Colour by role: circle/ellipse BLUE, semi-major GOLD, semi-minor GREEN, centre YELLOW.
`wide_ellipse()` (module level) is reused by the recap ch5_s8_recap (r3).
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

R = 1.5            # circle radius
A_W, B_W = 2.4, 1.5  # the wide ellipse
A_T, B_T = 1.3, 2.0  # the tall ellipse
AX_C = np.array([-3.5, -0.1, 0])
COL_X = 3.1        # right-hand column of equations


def _arm(start, end, color):
    return Arrow(start, end, buff=0, color=color, stroke_width=6, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=10)


def ellipse_picture(a, b, label_size=36):
    """The notes' picture: BLUE ellipse centred at ORIGIN, YELLOW centre, arms out to a (along x) and
    b (along y), a brace under the x-arm's span and one beside the y-arm's span. The larger of a, b
    is the semi-major axis (GOLD), the smaller the semi-minor axis (GREEN): colour by role.
    Parts: .ell .dot .arm_x .arm_y .brace_x .lab_x .brace_y .lab_y"""
    major_x = a >= b
    cx, cy = (GOLD, GREEN) if major_x else (GREEN, GOLD)
    nx, ny = ("major", "minor") if major_x else ("minor", "major")
    ell = Ellipse(width=2 * a, height=2 * b, color=BLUE, stroke_width=5)
    dot = Dot(ORIGIN, radius=0.08, color=YELLOW)
    arm_x = _arm(ORIGIN, a * RIGHT, cx)
    arm_y = _arm(ORIGIN, b * UP, cy)
    brace_x = Brace(Line(-b * UP, a * RIGHT - b * UP), DOWN, buff=0.2).set_color(cx)
    lab_x = T(f"Semi-{nx} axis", label_size, color=cx).next_to(brace_x, DOWN, buff=0.12)
    brace_y = Brace(Line(a * RIGHT, a * RIGHT + b * UP), RIGHT, buff=0.2).set_color(cy)
    lab_y = T(f"Semi-{ny}\naxis", label_size, color=cy, line_spacing=0.8)
    lab_y.next_to(brace_y, RIGHT, buff=0.15)
    g = VGroup(ell, arm_x, arm_y, dot, brace_x, lab_x, brace_y, lab_y)
    g.ell, g.dot, g.arm_x, g.arm_y = ell, dot, arm_x, arm_y
    g.brace_x, g.lab_x, g.brace_y, g.lab_y = brace_x, lab_x, brace_y, lab_y
    return g


def wide_ellipse(label_size=36):
    """The wide ellipse (a > b) with its GOLD semi-major / GREEN semi-minor braces, centre at ORIGIN."""
    return ellipse_picture(A_W, B_W, label_size)


def make_axes():
    ax = Axes(x_range=[-3, 3, 1], y_range=[-2.4, 2.4, 1], x_length=6, y_length=4.8, tips=False,
              axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": False})
    ax.shift(AX_C - ax.c2p(0, 0))
    xl = MathTex("x", font_size=36, color=DIM).next_to(ax.x_axis, RIGHT, buff=0.15)
    yl = MathTex("y", font_size=36, color=DIM).next_to(ax.y_axis, UP, buff=0.12)
    return ax, xl, yl


def _tick(point, horizontal, color):
    d = RIGHT if horizontal else UP
    return Line(point - 0.16 * d, point + 0.16 * d, color=color, stroke_width=5)


class EllipseScene(NarratedScene):
    def construct(self):
        ax, xl, yl = make_axes()
        O = ax.c2p(0, 0)
        pic = wide_ellipse().shift(O)
        circle = Circle(radius=R, color=BLUE, stroke_width=5).move_to(O)

        # ---------------- clip 1: the circle, divided by r^2 ----------------
        row1 = MathTex(r"x^2 + y^2 = r^2", font_size=56).move_to([COL_X, 2.5, 0])
        chain = MathTex(r"\frac{x^2}{r^2}+\frac{y^2}{r^2}=", r"\left(\frac{x}{", "r", r"}\right)^2+\left(\frac{y}{",
                        "r", r"}\right)^2=1", font_size=46).move_to([COL_X, 0.9, 0])
        row2 = MathTex(r"\frac{x^2}{r^2}+\frac{y^2}{r^2}=1", font_size=46)
        row2.move_to(chain.get_center()).align_to(chain, LEFT)

        with self.say("c5.ellipse.1") as c:
            self.play(*appear(ax, xl, yl, shift=None, lag=0.15), run_time=1.0)
            self.play(Create(circle), *appear(pic.dot, row1, shift=None), run_time=1.6)
            c.wait_until("divide")
            self.play(*appear(row2), run_time=1.0)
            c.wait_until("over")
            self.play(*edit(row2, chain), run_time=min(1.8, c.until("same") - 0.2))
            c.wait_until("same")
            boxes = [SurroundingRectangle(chain[i], color=YELLOW, buff=0.07, stroke_width=2)
                     .set_fill(YELLOW, 0.2) for i in (2, 4)]
            self.play(*[FadeIn(b) for b in boxes], *recolor([chain[2], chain[4]], YELLOW), run_time=1.0)
            self.play(*flash(boxes), run_time=1.5)

        # ---------------- clip 2: different scales -> the ellipse ----------------
        row3r = MathTex(r"\left(\frac{x}{", "r", r"}\right)^2+\left(\frac{y}{", "r", r"}\right)^2=1",
                        font_size=56).move_to([COL_X, -0.9, 0])
        row3 = MathTex(r"\left(\frac{x}{", "a", r"}\right)^2+\left(\frac{y}{", "b", r"}\right)^2=1",
                       font_size=56).move_to(row3r)
        row3[1].set_color(GOLD)
        row3[3].set_color(GREEN)
        TOP = np.array([COL_X - 0.6, 2.4, 0])
        tag = MathTex("(100)", font_size=40, color=DIM)
        tag_lab = T("equation of an ellipse", 36, color=FG)
        xrow = MathTex("x = 0", r"\;\Rightarrow\;", r"y = \pm", "b", font_size=50).move_to([COL_X, -0.1, 0])
        xrow[3].set_color(GREEN)
        yrow = MathTex("y = 0", r"\;\Rightarrow\;", r"x = \pm", "a", font_size=50).move_to([COL_X, -1.4, 0])
        yrow[3].set_color(GOLD)

        with self.say("c5.ellipse.2") as c:
            src = VGroup(*chain[1:])
            self.play(*fly(src, row3r), *[FadeOut(b) for b in boxes],
                      *recolor([chain[2], chain[4]], FG), run_time=1.6)
            c.wait_until("ab")
            self.play(*edit(row3r, row3), ReplacementTransform(circle, pic.ell), run_time=2.0)
            c.wait_until("eq")
            self.play(*during(disappear(row1, chain), 0, 0.45),
                      *during([row3.animate.move_to(TOP)], 0.35, 1), run_time=1.6)
            tag.next_to(row3, RIGHT, buff=0.45)
            tag_lab.next_to(row3, DOWN, buff=0.35)
            self.play(*flash([row3]), run_time=1.5)
            c.wait_until("tag")
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("basic equation")
            self.play(*appear(tag_lab), run_time=1.0)
            c.wait_until("x0")
            tb = [_tick(ax.c2p(0, s * B_W), True, GREEN) for s in (1, -1)]
            tbl = [MathTex("b", font_size=36, color=GREEN).next_to(tb[0], UL, buff=0.08),
                   MathTex("-b", font_size=36, color=GREEN).next_to(tb[1], DL, buff=0.08)]
            self.play(*appear(xrow), *[GrowFromCenter(t) for t in tb], *appear(*tbl, shift=None),
                      run_time=1.4)
            c.wait_until("y0")
            ta = [_tick(ax.c2p(s * A_W, 0), False, GOLD) for s in (1, -1)]
            tal = [MathTex("a", font_size=36, color=GOLD).next_to(ta[0], DR, buff=0.08),
                   MathTex("-a", font_size=36, color=GOLD).next_to(ta[1], DL, buff=0.08)]
            self.play(*appear(yrow), *[GrowFromCenter(t) for t in ta], *appear(*tal, shift=None),
                      run_time=1.4)

        # ---------------- clip 3: semi-major, semi-minor; wide and tall ----------------
        pos = MathTex("a", r",\ ", "b", r" > 0", font_size=50).move_to([COL_X, -2.7, 0])
        pos[0].set_color(GOLD)
        pos[2].set_color(GREEN)
        tall = ellipse_picture(A_T, B_T)

        with self.say("c5.ellipse.3") as c:
            self.play(GrowArrow(pic.arm_x), run_time=1.2)
            c.wait_until("as far as b")
            self.play(GrowArrow(pic.arm_y), run_time=1.2)
            c.wait_until("pos")
            self.play(*appear(pos), run_time=1.0)
            c.wait_until("major")
            d = np.array([0, 0.2, 0]) - pic.get_center()
            for m in (pic.brace_x, pic.lab_x, pic.brace_y, pic.lab_y):
                m.shift(d)
            shown = (pic.ell, pic.dot, pic.arm_x, pic.arm_y)
            sweep_clear(self, *[m.animate.shift(d) for m in shown], pos.animate.move_to([0, -2.9, 0]),
                        keep=list(shown) + [pos], run_time=1.4)
            self.play(GrowFromCenter(pic.brace_x), *appear(pic.lab_x), run_time=1.0)
            c.wait_until("minor")
            self.play(GrowFromCenter(pic.brace_y), *appear(pic.lab_y), run_time=1.0)
            c.wait_until("wide")
            settle(self, pic)
            cap_w = MathTex("a > b", font_size=40).move_to([-3.3, -2.6, 0])
            self.play(pic.animate.scale(0.8).move_to([-3.3, 0.4, 0]), *during(disappear(pos), 0, 0.5), run_time=1.5)
            self.play(*appear(cap_w), run_time=1.0)
            c.wait_until("tall")
            tall.scale(0.8).move_to([3.5, 0.4, 0])
            cap_t = MathTex("b > a", font_size=40).move_to([3.5, -2.6, 0])
            self.play(*appear(tall.ell, tall.dot, tall.arm_x, tall.arm_y, shift=None, lag=0.1),
                      *appear(tall.brace_x, tall.lab_x, tall.brace_y, tall.lab_y, cap_t, lag=0.1),
                      run_time=1.3)

        # ---------------- clip 4: shifted centre, tilted ellipses, general form ----------------
        shifted = MathTex(r"\left(\frac{x-", "x_0", "}{", "a", r"}\right)^2+\left(\frac{y-", "y_0", "}{", "b",
                          r"}\right)^2=1", font_size=44).move_to([COL_X + 0.3, 2.4, 0])
        for i, col in ((1, YELLOW), (3, GOLD), (5, YELLOW), (7, GREEN)):
            shifted[i].set_color(col)
        ctr = ax.c2p(0.8, 0.6)
        ctr_lab = MathTex("(x_0,\\, y_0)", font_size=34, color=YELLOW)
        ib_tag = T("NST IB", 30, color=DIM)
        ib_eq = MathTex(r"\mathbf{x}^{\mathsf{T}} A\, \mathbf{x} = s", font_size=48, color=PURPLE)
        ib = VGroup(ib_tag, ib_eq).arrange(DOWN, buff=0.25).move_to([COL_X + 0.3, 0.3, 0])
        gen_lab = T("More general form", 32, color=DIM)
        gen = MathTex("Ax^2+", "Bxy", "+Cy^2+Dx+Ey+F=0", font_size=44)
        VGroup(gen_lab, gen).arrange(RIGHT, buff=0.45).move_to([0, -3.2, 0])
        gen2 = MathTex("Ax^2+Cy^2+Dx+Ey+F=0", font_size=44).move_to(gen).align_to(gen, LEFT)
        tilt = 25 * DEGREES

        with self.say("c5.ellipse.4") as c:
            c.wait_until("subtract")   # the wide/tall pair holds into this line
            d = ctr - pic.ell.get_center()
            parts = (pic.ell, pic.dot, pic.arm_x, pic.arm_y, pic.brace_x, pic.brace_y)
            self.play(*during(disappear(tall, cap_w, cap_t, pic.lab_x, pic.lab_y), 0, 0.45),
                      *during([m.animate.shift(d) for m in parts], 0.2, 0.8),
                      *during(appear(ax, xl, yl, shift=None), 0.5, 1), run_time=1.5)
            settle(self, pic, drop=[pic.lab_x, pic.lab_y])
            ctr_lab.next_to(ctr, DL, buff=0.1)
            la = MathTex("a", font_size=40, color=GOLD).next_to(pic.brace_x, DOWN, buff=0.1)
            lb = MathTex("b", font_size=40, color=GREEN).next_to(pic.brace_y, RIGHT, buff=0.12)
            self.play(*appear(shifted), *appear(la, lb, ctr_lab, shift=None, lag=0.15),
                      run_time=min(1.2, c.until("aligned", floor=0.6)))
            c.wait_until("aligned")
            guides = [ax.x_axis.copy(), ax.y_axis.copy(),
                      Line(pic.arm_x.get_start(), pic.arm_x.get_end()),
                      Line(pic.arm_y.get_start(), pic.arm_y.get_end())]
            self.play(*[VShowPassingFlash(g.set_stroke(YELLOW, 6), time_width=0.6) for g in guides],
                      run_time=1.6)
            c.wait_until("ib")
            self.play(*disappear(pic.brace_x, pic.brace_y, la, lb), run_time=0.7)
            settle(self, pic, drop=[pic.brace_x, pic.brace_y])
            self.play(*[Rotate(m, tilt, about_point=ctr) for m in (pic.ell, pic.arm_x, pic.arm_y)],
                      run_time=1.6)
            self.play(*appear(ib_tag, ib_eq, lag=0.3), run_time=1.2)
            c.wait_until("general")
            self.play(*appear(gen_lab, gen, lag=0.3), run_time=1.2)
            c.wait_until("xy")
            self.play(*recolor(gen[1], YELLOW), run_time=0.8)
            self.play(*flash([gen[1]]), run_time=1.5)
            c.wait_until("noxy")
            self.play(*[Rotate(m, -tilt, about_point=ctr) for m in (pic.ell, pic.arm_x, pic.arm_y)],
                      *edit(gen, gen2), run_time=1.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
