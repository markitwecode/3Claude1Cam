"""Chapter 3, scene 2: the shape of cosh, read off the two dashed halves. Clips c3.cosh.1 – c3.cosh.4.

Shared with ch3_s3 and the recap (import with load_scene("ch3_s2_cosh")):
- FIG_CENTER: where this scene's axes sit (graph_axes() of ch1_s2, moved there).
- half_exp_curve(ax, dashed=True): GOLD (1/2)e^x, clipped at y = 5; dashed by default.
- half_emx_curve(ax, dashed=True): PURPLE (1/2)e^{-x}, its mirror image.
- half_label(ax, which): MathTex label of a half curve ("exp" or "emx"), by its top end.
- zero_dot(ax): YELLOW dot at (0, 1).
- cosh_figure(): VGroup(ax, cosh, cosh label, both dashed halves, their labels, the dot);
  attributes .ax .cosh .lab_cosh .hexp .hemx .lab_hexp .lab_hemx .dot.
- handover_shot(): this scene's last frame (= cosh_figure()).
"""
# style: 2
# handover: next
import math
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

S2 = load_scene("ch1_s2_define")
graph_axes, exp_curve, emx_curve, cosh_curve = S2.graph_axes, S2.exp_curve, S2.emx_curve, S2.cosh_curve
curve_label, x_marks, ctex, _plot = S2.curve_label, S2.x_marks, S2.ctex, S2._plot
X_LO, X_HI, Y_LO, Y_HI, COSH_LIM = S2.X_LO, S2.X_HI, S2.Y_LO, S2.Y_HI, S2.COSH_LIM

FIG_CENTER = np.array([1.0, -0.55, 0])
FIG_Y_LEN = 6.6                          # a little shorter than ch1's 7, to leave the top for formulas
L10 = math.log(10)                       # (1/2)e^x reaches y = 5
COL_X = -5.05                            # centre of the property column, left of the axes


def _half_exp(x):
    return 0.5 * math.exp(x)


def _half_emx(x):
    return 0.5 * math.exp(-x)


def _dash(curve):
    return DashedVMobject(curve, num_dashes=34, dashed_ratio=0.6)


def half_exp_curve(ax, dashed=True, width=5):
    c = _plot(ax, _half_exp, X_LO, L10, GOLD, width)
    return _dash(c) if dashed else c


def half_emx_curve(ax, dashed=True, width=5):
    c = _plot(ax, _half_emx, -L10, X_HI, PURPLE, width)
    return _dash(c) if dashed else c


def half_label(ax, which, size=38):
    if which == "exp":
        m = MathTex(r"\tfrac{1}{2}e^{x}", font_size=size, color=GOLD)
        m.next_to(ax.c2p(math.log(9.2), 4.6), LEFT, buff=0.3)
    else:
        m = MathTex(r"\tfrac{1}{2}e^{-x}", font_size=size, color=PURPLE)
        m.next_to(ax.c2p(-math.log(9.2), 4.6), RIGHT, buff=0.3)
    return set_backstroke(m)


def zero_dot(ax):
    return Dot(ax.c2p(0, 1), radius=0.11, color=YELLOW).set_z_index(3)


def fig_axes():
    return graph_axes(y_length=FIG_Y_LEN).move_to(FIG_CENTER)


def cosh_figure():
    ax = fig_axes()
    ch = cosh_curve(ax)
    lab = curve_label(ax, "cosh")
    hexp, hemx = half_exp_curve(ax), half_emx_curve(ax)
    lhexp, lhemx = half_label(ax, "exp"), half_label(ax, "emx")
    dot = zero_dot(ax)
    g = VGroup(ax, hexp, hemx, ch, lab, lhexp, lhemx, dot)
    g.ax, g.cosh, g.lab_cosh, g.hexp, g.hemx, g.lab_hexp, g.lab_hemx, g.dot = (
        ax, ch, lab, hexp, hemx, lhexp, lhemx, dot)
    return g


def handover_shot():
    return cosh_figure()


def bar_pair(ax, x, w=0.24):
    """PURPLE bar 0..(1/2)e^{-x}, GOLD bar stacked on it up to cosh x."""
    y0, y1, y2 = ax.c2p(x, 0)[1], ax.c2p(x, _half_emx(x))[1], ax.c2p(x, math.cosh(x))[1]
    cx = ax.c2p(x, 0)[0]
    p = Rectangle(width=w, height=y1 - y0).move_to([cx, (y0 + y1) / 2, 0])
    g = Rectangle(width=w, height=y2 - y1).move_to([cx, (y1 + y2) / 2, 0])
    p.set_stroke(width=0).set_fill(PURPLE, 0.8)
    g.set_stroke(width=0).set_fill(GOLD, 0.8)
    return p, g


def branch(ax, lo, hi, color=YELLOW, width=8):
    return _plot(ax, math.cosh, lo, hi, color, width)


class CoshShape(NarratedScene):
    def construct(self):
        fig = cosh_figure()
        ax, ch, lab_ch = fig.ax, fig.cosh, fig.lab_cosh
        hexp, hemx, lhexp, lhemx, dot = fig.hexp, fig.hemx, fig.lab_hexp, fig.lab_hemx, fig.dot

        # ------------------------------------------------ c3.cosh.1: the picture, split in halves
        with self.say("c3.cosh.1") as c:
            ex, emx = exp_curve(ax), emx_curve(ax)
            lab_ex, lab_emx = curve_label(ax, "exp"), curve_label(ax, "emx")
            self.play(FadeIn(ax), FadeIn(ex), FadeIn(emx), FadeIn(ch),
                      FadeIn(lab_ex), FadeIn(lab_emx), FadeIn(lab_ch), run_time=1.5)  # early: the picture shown whole
            c.wait_until("gold")
            self.play(VShowPassingFlash(ex.copy().set_stroke(YELLOW, 9), time_width=0.5),
                      FlashAround(lab_ex, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("purple")
            self.play(VShowPassingFlash(emx.copy().set_stroke(YELLOW, 9), time_width=0.5),
                      FlashAround(lab_emx, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("avg")
            marks = x_marks(ax, 1.0)
            self.play(Create(marks.line), GrowFromCenter(marks.gold), GrowFromCenter(marks.purple), run_time=1.2)
            self.play(GrowFromCenter(marks.mid), run_time=1.0)

            c.wait_until("halves")
            self.play(FadeOut(marks), run_time=0.8)
            sexp = half_exp_curve(ax, dashed=False)
            semx = half_emx_curve(ax, dashed=False)
            c.wait_until("half of E to the ex")
            self.play(ReplacementTransform(ex.copy(), sexp), *set_alpha([ex, lab_ex], 0.35),
                      run_time=min(1.8, c.until("half of E to the minus ex")))
            c.wait_until("half of E to the minus ex")
            self.play(ReplacementTransform(emx.copy(), semx), *set_alpha([emx, lab_emx], 0.35),
                      run_time=min(1.8, c.until("dashed")))
            c.wait_until("dashed")
            self.play(*during([FadeOut(ex), FadeOut(emx), FadeOut(lab_ex), FadeOut(lab_emx)], 0, 0.5),
                      FadeOut(sexp), FadeIn(hexp), FadeOut(semx), FadeIn(hemx), run_time=1.0)
            self.play(*appear(lhexp, lhemx, lag=0.3), run_time=0.8)

            c.wait_until("sum")
            formula = ctex(r"\cosh x = \tfrac{1}{2}e^{x} + \tfrac{1}{2}e^{-x}",
                           "TTTTT F GGGGG F UUUUUU", size=46)
            formula.move_to([FIG_CENTER[0], 3.2, 0])
            xs = [-1.5, 0.0, 1.0, 1.8]
            bars = [bar_pair(ax, x) for x in xs]
            pbars = [b[0] for b in bars]
            gbars = [b[1] for b in bars]
            self.play(*during(appear(formula), 0, 0.45),
                      *during([GrowFromEdge(b, DOWN) for b in pbars], 0.25, 0.65),
                      *during([GrowFromEdge(b, DOWN) for b in gbars], 0.6, 1.0),
                      run_time=max(1.6, c.until(floor=1.6)))

        # ------------------------------------------------ c3.cosh.2: cosh 0 = 1; even
        with self.say("c3.cosh.2") as c:
            self.play(GrowFromCenter(dot), FlashAround(VGroup(pbars[1], gbars[1]), run_time=1.2, time_width=1.5),
                      run_time=1.2)
            p1 = ctex(r"\cosh 0 = \dfrac{1 + 1}{2} = 1", "TTTTT F GFU F F F Y", size=40)
            p1.move_to([COL_X, 2.2, 0])
            c.wait_until("Both exponentials")
            self.play(*appear(p1), run_time=1.2)

            c.wait_until("mirror")
            mline = DashedLine(ax.c2p(0, Y_LO), ax.c2p(0, Y_HI), dash_length=0.12).set_stroke(FG, 3, opacity=0.45)
            self.play(*[FadeOut(b) for b in pbars + gbars], GrowFromCenter(mline),
                      *set_alpha([lhexp, lhemx], DIMMED), run_time=1.2)
            c.wait_until("The two dashed curves")
            o = ax.c2p(0, 0)
            self.play(Rotate(hexp, PI, axis=UP, about_point=o), Rotate(hemx, PI, axis=UP, about_point=o),
                      run_time=2.0)
            c.wait_until("and their sum")
            self.play(Rotate(hexp, -PI, axis=UP, about_point=o), Rotate(hemx, -PI, axis=UP, about_point=o),
                      run_time=1.6)
            self.play(*set_alpha([lhexp, lhemx], 1), run_time=0.6)

            c.wait_until("even")
            p2 = ctex(r"\cosh(-x) = \cosh x", "TTTTTTTT F TTTTT", size=40)
            p2.move_to([COL_X, 0.9, 0])
            self.play(*appear(p2), run_time=1.2)
            c.wait_until("The graph is its own")
            self.play(VShowPassingFlash(mline.copy().set_stroke(YELLOW, 5, opacity=1), time_width=0.6),
                      VShowPassingFlash(branch(ax, 0, COSH_LIM), time_width=0.6),
                      VShowPassingFlash(branch(ax, -COSH_LIM, 0).reverse_points(), time_width=0.6),
                      run_time=1.8)

        # ------------------------------------------------ c3.cosh.3: far right, far left
        with self.say("c3.cosh.3") as c:
            stand = x_marks(ax, 2.0).line
            self.play(FadeOut(mline), FadeOut(lhexp), Create(stand), run_time=1.2)
            gd = Dot(ax.c2p(2, _half_exp(2)), radius=0.1, color=GOLD).set_z_index(3)
            pd = Dot(ax.c2p(2, _half_emx(2)), radius=0.1, color=PURPLE).set_z_index(3)
            rg = set_backstroke(MathTex(r"\tfrac{1}{2}e^{2} \approx 3.69", font_size=38, color=GOLD))
            rg.next_to(gd, LEFT, buff=0.25).shift(0.35 * UP)
            rp = set_backstroke(MathTex(r"\tfrac{1}{2}e^{-2} \approx 0.068", font_size=38, color=PURPLE))
            rp.next_to(pd, DL, buff=0.2)
            c.wait_until("half of E to the ex")
            self.play(GrowFromCenter(gd), *appear(rg), run_time=1.2)
            c.wait_until("half of E to the minus ex")
            self.play(GrowFromCenter(pd), *appear(rp), run_time=1.2)

            c.wait_until("hug")
            glow_r = _plot(ax, _half_exp, 1.0, L10, GOLD, 18).set_stroke(opacity=0.3)
            self.play(Create(glow_r),
                      VShowPassingFlash(branch(ax, 1.0, COSH_LIM), time_width=0.6), run_time=1.8)

            c.wait_until("the roles swap")
            self.play(*during(disappear(stand, gd, pd, rg, rp), 0, 0.55), *during(appear(lhexp), 0.5, 1.0),
                      run_time=1.4)
            c.wait_until("hugleft")
            glow_l = _plot(ax, _half_emx, -L10, -1.0, PURPLE, 18).set_stroke(opacity=0.3).reverse_points()
            self.play(Create(glow_l),
                      VShowPassingFlash(branch(ax, -COSH_LIM, -1.0).reverse_points(), time_width=0.6),
                      run_time=min(1.8, c.until(floor=1.2)))

        # ------------------------------------------------ c3.cosh.4: cosh x >= 1, and why
        with self.say("c3.cosh.4") as c:
            floor = DashedLine(ax.c2p(X_LO, 1), ax.c2p(X_HI, 1), dash_length=0.14).set_stroke(YELLOW, 3)
            self.play(FadeOut(glow_r), FadeOut(glow_l), GrowFromPoint(floor, ax.c2p(0, 1)), run_time=1.4)
            p6 = ctex(r"\cosh x \ge 1", "TTTTT Y Y", size=40)
            p6.move_to([COL_X, -0.3, 0])
            c.wait_until("at least one")
            self.play(*appear(p6), run_time=1.0)

            c.wait_until("why")
            l1 = ctex(r"e^{-x} = \dfrac{1}{e^{x}}", "UUU F F F GG", size=40)
            l2 = ctex(r"a + \dfrac{1}{a} \ge 2 \quad (a > 0)", "FFFFF YY FFFFF", size=40)
            l3 = MathTex(r"2 + \tfrac{1}{2} = 2\tfrac{1}{2}", font_size=38, color=FG)
            right = VGroup(l2, l3).arrange(DOWN, buff=0.35)
            body = VGroup(l1, right).arrange(RIGHT, buff=0.9)
            l3.align_to(l2, LEFT)
            card = RoundedRectangle(corner_radius=0.15, width=body.width + 0.8, height=body.height + 0.6)
            card.set_stroke(DIM, 2).set_fill(BG, 1)
            VGroup(card, body).move_to([FIG_CENTER[0], -2.65, 0])
            card.set_z_index(4)
            for m in (l1, l2, l3):
                m.set_z_index(5)
            self.play(FadeIn(card), run_time=0.8)
            c.wait_until("E to the minus ex is one over")
            self.play(*appear(l1), run_time=1.2)
            c.wait_until("recip")
            self.play(*appear(l2), run_time=1.2)
            c.wait_until("Two plus a half")
            self.play(*appear(l3), run_time=1.2)

            c.wait_until("U")
            self.play(FlashAround(p6, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("and it equals one only")
            self.play(Flash(dot, color=YELLOW, line_length=0.25, flash_radius=0.3, run_time=1.0),
                      run_time=1.0)
            c.wait_until("Cosh is a U")
            self.play(*disappear(card, l1, l2, l3, formula, p1, p2, p6, floor), run_time=1.2)
            self.play(VShowPassingFlash(branch(ax, 0, COSH_LIM), time_width=0.6),
                      VShowPassingFlash(branch(ax, -COSH_LIM, 0).reverse_points(), time_width=0.6),
                      run_time=min(1.8, c.until(floor=1.0)))
        self.wait(1.0)          # handover: hold Figure 25(a); ch3_s3 opens on handover_shot()
