"""Chapter 2, scene 7: recap in four panels, then a look ahead to the graphs and inverses.
Clips c2.recap.1 – c2.recap.2.

Panels (2 x 2), each a miniature of the scene that taught it, built on its mark while the
earlier ones dim: r1 s2's cancelling e^{2x} / e^{-2x}, boxed (93), circle and hyperbola;
r2 s3's i sinh A . i sinh B -> i^2 = -1 -> YELLOW +; r3 s3's result line and s5's row 5 child
with the tanh^2 unfold; r4 s6's boxed tanh(A+B) with the GREEN tick. On {next} the panels sweep
away for ch1 s2's axes with cosh / sinh / tanh, the dashed GOLD (1/2)e^x guide, then the
mirror line y = x, a YELLOW "?" and "log". End card held ~8 s, then fade.
"""
# style: 2
import math
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

S2 = load_scene("ch2_s2_pythag")
S3 = load_scene("ch2_s3_addition")
S5 = load_scene("ch2_s5_rule")
G = load_scene("ch1_s2_define")
SINH_C = G.SINH_C

PW = 6.5                                # panel frame width; top row shorter than the bottom
CENTRES = [np.array([-3.4, 2.1, 0]), np.array([3.4, 2.1, 0]),
           np.array([-3.4, -1.6, 0]), np.array([3.4, -1.6, 0])]
HEIGHTS = [3.0, 3.0, 4.1, 4.1]
CAP = 28
FADED = 0.4


def frame_at(k):
    return RoundedRectangle(corner_radius=0.15, width=PW, height=HEIGHTS[k]).set_stroke(DIM, 2).move_to(CENTRES[k])


TITLE_ROOM = 0.62                       # band at the top of each panel for its title


def caption_at(text, k):
    """The panel's title: one plain style for all four, in the band at the panel's top."""
    return T(text, CAP, DIM, slant=ITALIC).move_to(CENTRES[k] + UP * (HEIGHTS[k] / 2 - 0.34))


def fit(g, k, w=5.8, room=0.3):
    h = HEIGHTS[k] - TITLE_ROOM - room
    if g.width > w:
        g.scale_to_fit_width(w)
    if g.height > h:
        g.scale_to_fit_height(h)
    g.move_to(CENTRES[k] + DOWN * (TITLE_ROOM - 0.12) / 2)
    return g


def mini_plot(curves, r=0.62, asym=False):
    """A small square plot: faint axes, the curve(s), dashed asymptotes y = +-x if asked."""
    axes = VGroup(Line(LEFT * r, RIGHT * r), Line(DOWN * r, UP * r)).set_stroke(DIM, 1.5, opacity=0.6)
    parts = [axes]
    if asym:
        for sgn in (1, -1):
            parts.append(DashedLine(r * 0.95 * np.array([-1, -sgn, 0]), r * 0.95 * np.array([1, sgn, 0]),
                                    dash_length=0.06).set_stroke(DIM, 1.5))
    return VGroup(*parts, *curves)


def strike(m):
    return Line(m.get_corner(DL) + 0.04 * DL, m.get_corner(UR) + 0.04 * UR,
                stroke_width=3, color=FG)


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(7.6)                       # end card: the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    # ------------------------------------------------------------ the four panels
    def clip1(self):
        with self.say("c2.recap.1") as c:
            # ---- r1: cosh^2 - sinh^2 = 1
            c.wait_until("r1")
            k = 0
            fr1 = frame_at(k)
            canc = MathTex("(", "e^{2x}", "+", "2", "+", "e^{-2x}", ")", "-",
                           "(", "e^{2x}", "-", "2", "+", "e^{-2x}", ")", font_size=40)
            for i in (1, 9):
                canc[i].set_color(GOLD)
            for i in (5, 13):
                canc[i].set_color(PURPLE)
            res = S2.result_group().scale(0.7)
            circ = Circle(radius=0.36, color=BLUE, stroke_width=4)
            hyp = VGroup(*[ParametricFunction(lambda t, s=s: 0.3 * np.array([s * np.cosh(t), np.sinh(t), 0]),
                                              t_range=[-1.25, 1.25], color=TEAL, stroke_width=4)
                           for s in (1, -1)])
            plot_c = mini_plot([circ])
            plot_h = mini_plot([hyp], asym=True)
            pics = VGroup(plot_c, plot_h).arrange(RIGHT, buff=0.3)
            low = VGroup(res, pics).arrange(RIGHT, buff=0.4)
            body1 = fit(VGroup(canc, low).arrange(DOWN, buff=0.25), k, w=6.0, room=0.15)
            cap1 = caption_at("expanding the definitions", k)
            self.play(FadeIn(fr1), *appear(cap1), *appear(canc), run_time=min(1.2, c.until("gives")))
            c.wait_until("gives")
            strikes = [strike(canc[i]) for i in (1, 9, 5, 13)]
            self.play(*[Create(s) for s in strikes], run_time=1.0)
            c.wait_until("cosh squared")
            self.play(*appear(res), run_time=1.2)
            c.wait_until("the circle identity")
            self.play(FadeIn(plot_c[0]), FadeIn(plot_h[0]), FadeIn(plot_h[1]), FadeIn(plot_h[2]),
                      Create(circ), Create(hyp[0]), Create(hyp[1]), run_time=1.3)
            panel1 = VGroup(fr1, canc, *strikes, res, plot_c, plot_h, cap1)
            settle(self, panel1)

            # ---- r2: through the complex door
            c.wait_until("r2")
            k = 1
            fr2 = frame_at(k)
            top = MathTex("-", r"\,i", r"\sinh A", r"\cdot", "i", r"\sinh B", font_size=44)
            for i in (1, 4):
                top[i].set_color(PINK)
            for i in (2, 5):
                top[i].set_color(TEAL)
            bot = MathTex("+", r"\,\sinh A", r"\,\sinh B", font_size=44, color=TEAL)
            bot[0].set_color(YELLOW)
            note = MathTex("i^2", "=", "-1", font_size=40)
            note[0].set_color(PINK)
            col = VGroup(top, bot).arrange(DOWN, buff=0.9)
            bot.align_to(top, LEFT)
            body2 = fit(VGroup(col, note).arrange(RIGHT, buff=0.8), k)
            cap2 = caption_at("through the complex door", k)
            self.play(*set_alpha([panel1], FADED), FadeIn(fr2), *appear(top, cap2, lag=0.3),
                      run_time=min(1.3, c.until("eye times eye")))
            c.wait_until("eye times eye")
            self.play(*flash([top[1], top[4]], color=PINK), run_time=1.0)
            c.wait_until("minus one")
            self.play(*appear(note), run_time=0.9)
            c.wait_until("flips")
            down = Arrow(top.get_bottom(), bot.get_top(), buff=0.12, stroke_width=3, color=DIM)
            down.set_x(bot[0].get_x() + 0.6)
            self.play(GrowArrow(down), *during(appear(bot), 0.35, 1.0), run_time=min(1.5, c.until("r3")))
            panel2 = VGroup(fr2, top, down, bot, note, cap2)
            settle(self, panel2)

            # ---- r3: the rule
            c.wait_until("r3")
            k = 2
            fr3 = frame_at(k)
            # s3's result line, wrapped after the first product to fit the panel
            rowa = G.ctex(r"\cosh(A + B) \equiv \cosh A \cosh B", "TTTTFFFFF F TTTTF TTTTF", size=50)
            rowb = G.ctex(r"+ \sinh A \sinh B", "Y TTTTF TTTTF", size=50)
            rowb.next_to(rowa, DOWN, buff=0.3).align_to(rowa[0][10], LEFT)
            row1 = VGroup(rowa, rowb)
            row5c = S5.row5(size=50)[2]
            row5c.next_to(row1, DOWN, buff=0.6)
            br = Brace(row5c[2], DOWN, buff=0.15, color=DIM)
            frc = S5.frac_of(S5.mtex(r"\sinh^2 z", size=46, color=TEAL),
                             S5.mtex(r"\cosh^2 z", size=46, color=TEAL), TEAL)
            frc.next_to(br, DOWN, buff=0.2)
            body3 = fit(VGroup(row1, row5c, br, frc), k, room=0.35)
            cap3 = caption_at("flip on sinh × sinh, hidden ones too", k)
            plus1 = rowb[0][0]
            self.play(*set_alpha([panel2], FADED), FadeIn(fr3), *appear(rowa, rowb, lag=0.3),
                      run_time=min(1.3, c.until("rename")))
            c.wait_until("rename")
            self.play(*appear(row5c), run_time=1.0)
            c.wait_until("flip")
            self.play(*flash([plus1, row5c[1]]), *appear(cap3), run_time=1.2)
            c.wait_until("hidden")
            self.play(GrowFromCenter(br), *during(appear(frc), 0.3, 1.0),
                      run_time=min(1.5, c.until("r4")))
            panel3 = VGroup(fr3, row1, row5c, br, frc, cap3)
            settle(self, panel3)

            # ---- r4: tanh(A + B)
            c.wait_until("r4")
            k = 3
            fr4 = frame_at(k)
            tf = S5.tan_formula(h=True, plus=True, size=60)
            tbox = SurroundingRectangle(tf, color=YELLOW, buff=0.25, stroke_width=3)
            tick = check_mark(GREEN).scale(1.3)
            tick.next_to(tbox, RIGHT, buff=0.35)
            body4 = fit(VGroup(tf, tbox, tick), k, w=5.9, room=0.35)
            cap4 = caption_at("a plus underneath", k)
            plus4 = tf[1][2][1]
            self.play(*set_alpha([panel3], FADED), FadeIn(fr4), *appear(tf),
                      run_time=min(1.3, c.until("plus underneath")))
            c.wait_until("plus underneath")
            self.play(FadeIn(tbox), FlashAround(plus4, time_width=1.5), *appear(cap4), run_time=1.2)
            c.wait_until("where the tangent")
            self.play(*appear(tick, shift=None), run_time=0.8)
            panel4 = VGroup(fr4, tf, tbox, tick, cap4)
            settle(self, panel4)
            self.play(*set_alpha([panel1, panel2, panel3], 1),
                      run_time=max(0.3, min(1.0, c.until() - 0.1)))
        self.panels = [panel1, panel2, panel3, panel4]

    # ------------------------------------------------------------ next time
    def clip2(self):
        u = 0.8
        ax = G.graph_axes(x_length=5 * u, y_length=8 * u)
        ax.move_to([-0.4, -0.35, 0])
        guide = DashedVMobject(G._plot(ax, lambda x: 0.5 * math.exp(x), G.X_LO, math.log(10), GOLD, 3),
                               num_dashes=40)
        coshc = G.cosh_curve(ax, width=5)
        sinhc = G.sinh_curve(ax, width=5)
        tanhc = G._plot(ax, math.tanh, G.X_LO, G.X_HI, TEAL, 4)
        lc = MathTex(r"\cosh", font_size=34, color=TEAL).next_to(ax.c2p(-2.1, math.cosh(-2.1)), LEFT, buff=0.15)
        ls = MathTex(r"\sinh", font_size=34, color=SINH_C).next_to(ax.c2p(-1.75, math.sinh(-1.75)), LEFT, buff=0.15)
        lt = MathTex(r"\tanh", font_size=34, color=TEAL).next_to(ax.c2p(2.5, 1.0), RIGHT, buff=0.15)
        for m in (lc, ls, lt):
            set_backstroke(m)
        title = T("Next time", 44, DIM).to_corner(UL, buff=0.6)
        mirror = DashedLine(ax.c2p(-2.5, -2.5), ax.c2p(2.5, 2.5), dash_length=0.12).set_stroke(FG, 2.5)
        q = T("?", 64, YELLOW).next_to(ax.c2p(2.5, 2.5), RIGHT, buff=0.35)
        logw = T("log", 48, YELLOW).next_to(q, RIGHT, buff=0.35)
        with self.say("c2.recap.2") as c:
            c.wait_until("draw")
            sweep_clear(self, FadeIn(ax), FadeIn(guide), *appear(title), run_time=1.4)
            c.wait_until("cosh")
            self.play(Create(coshc), *appear(lc), run_time=min(1.0, c.until("shine")))
            c.wait_until("shine")
            self.play(Create(sinhc), *appear(ls), run_time=min(1.0, c.until("tanch")))
            c.wait_until("tanch")
            self.play(Create(tanhc), *appear(lt), run_time=min(1.0, c.until("undo")))
            c.wait_until("undo")
            self.play(Create(mirror), *during(appear(q), 0.4, 1.0), run_time=1.5)
            c.wait_until("logs")
            self.play(*appear(logw), run_time=1.0)
