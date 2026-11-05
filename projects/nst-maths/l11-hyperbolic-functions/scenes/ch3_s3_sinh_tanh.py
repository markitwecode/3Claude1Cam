"""Chapter 3, scene 3: sinh from the two dashed halves, tanh and its band, all three together.
Clips c3.odd.1 – c3.odd.5.

Opens on ch3_s2_cosh.handover_shot() (no fade-in); ends on ch3_s4_arsinh.fig25d_shot() (handover).
Shared: handover_shot() (= Figure 25(d)), tanh_fig() (Figure 25(c): axes, dashes, tanh curve).
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

C1 = load_scene("ch1_s2_define")
S2 = load_scene("ch3_s2_cosh")
S4 = load_scene("ch3_s4_arsinh")
G3 = load_scene("ch7_s4_g3")

SINH_C, TANH_C = C1.SINH_C, S4.TANH_C
_plot = C1._plot
COL_X = S2.COL_X
SINH_SYM = math.asinh(3)                 # symmetric sinh piece, for the half-turn
PSZ = 38                                 # property column size

# Figure 25(c) panel
TX_LEN, TY_LEN = 8.4, 4.4
T_CENTER = np.array([-1.6, -1.0, 0])
NOTE_X = 4.75


def handover_shot():
    return S4.fig25d_shot()


def colored(src, size, cmap):
    """MathTex in FG with glyph ranges recoloured: cmap = {(a, b): colour}."""
    m = MathTex(src, font_size=size, color=FG)
    for (a, b), col in cmap.items():
        for g in m[0][a:b]:
            g.set_color(col)
    return m


def glyphs(m, *idx):
    return [m[0][i] for i in idx]


def tanh_axes():
    ax = Axes(x_range=[-3, 3, 1], y_range=[-1.2, 1.2, 1], x_length=TX_LEN, y_length=TY_LEN, tips=False,
              axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": True, "tick_size": 0.06})
    ax.move_to(T_CENTER)
    return ax


def tanh_fig():
    ax = tanh_axes()
    vp = G3.dline(ax, (-3, 1), (3, 1), GOLD)
    vm = G3.dline(ax, (-3, -1), (3, -1), PURPLE)
    th = G3.fcurve(ax, math.tanh, -3, 3, TANH_C, 6)
    g = VGroup(ax, vp, vm, th)
    g.ax, g.vp, g.vm, g.tanh = ax, vp, vm, th
    return g


class SinhTanh(NarratedScene):
    def construct(self):
        fig = S2.handover_shot()
        self.add(*fig.submobjects)
        self.fig = fig
        self.clip_sinh()
        self.clip_hug()
        self.clip_tanh()
        self.clip_limits()
        self.clip_all()

    # ------------------------------------------------------------ c3.odd.1
    def clip_sinh(self):
        f = self.fig
        ax = f.ax
        o = ax.c2p(0, 0)
        with self.say("c3.odd.1") as c:
            formula = colored(r"\sinh x = \tfrac12 e^{x} - \tfrac12 e^{-x}", 46,
                              {(0, 5): SINH_C, (6, 11): GOLD, (12, 18): PURPLE})
            formula.move_to([S2.FIG_CENTER[0], 3.2, 0])
            self.play(*set_alpha([f.cosh, f.lab_cosh], 0.3), *appear(formula), run_time=1.2)

            c.wait_until("minus sign")
            nemx = S2._dash(_plot(ax, lambda x: -0.5 * math.exp(-x), -math.log(6), C1.X_HI, PURPLE, 5))
            nlab = set_backstroke(MathTex(r"-\tfrac12 e^{-x}", font_size=38, color=PURPLE))
            nlab.move_to(ax.c2p(1.75, -0.85))
            self.play(Transform(f.hemx, nemx), *swap(f.lab_hemx, nlab),
                      run_time=min(1.8, c.until("zero", floor=1.0)))
            self.nlab = nlab

            c.wait_until("zero")
            sh = C1.sinh_curve(ax)
            lab_sh = C1.curve_label(ax, "sinh")
            self.play(Create(sh), f.dot.animate.move_to(o), run_time=1.5)
            self.play(*appear(lab_sh), run_time=0.8)
            self.sh, self.lab_sh = sh, lab_sh

            c.wait_until("so shine of zero")
            p1 = MathTex(r"\sinh 0 = \dfrac{1 - 1}{2} = 0", font_size=PSZ, color=FG)
            for g in p1[0][0:4]:
                g.set_color(SINH_C)
            p1.move_to([COL_X, 2.2, 0])
            self.play(*appear(p1), run_time=1.0)
            self.p1 = p1

            c.wait_until("swap")
            labs = [f.lab_hexp, nlab, lab_sh]
            self.play(*[Rotate(m, PI, axis=UP, about_point=o) for m in (f.hexp, f.hemx, sh)],
                      *set_alpha(labs, DIMMED), run_time=2.0)

            c.wait_until("antisym")
            self.play(*[Rotate(m, -PI, axis=UP, about_point=o) for m in (f.hexp, f.hemx, sh)],
                      *set_alpha(labs, 1), run_time=1.5)
            p2 = MathTex(r"\sinh(-x) = -\sinh x", font_size=PSZ, color=FG)
            for g in glyphs(p2, 0, 1, 2, 3, 10, 11, 12, 13):
                g.set_color(SINH_C)
            p2.move_to([COL_X, 0.9, 0])
            self.play(*appear(p2), run_time=1.0)
            self.p2 = p2

            c.wait_until("Spin")
            ghost = _plot(ax, math.sinh, -SINH_SYM, SINH_SYM, YELLOW, 9).set_stroke(opacity=0.7)
            self.play(FadeIn(ghost), run_time=0.5)
            self.play(Rotate(ghost, PI, axis=OUT, about_point=o), run_time=2.2)
            self.play(FadeOut(ghost), run_time=min(0.8, c.until(floor=0.4)))

    # ------------------------------------------------------------ c3.odd.2
    def clip_hug(self):
        f = self.fig
        ax = f.ax
        o = ax.c2p(0, 0)
        sh = self.sh
        with self.say("c3.odd.2") as c:
            glow_r = _plot(ax, S2._half_exp, 1.0, S2.L10, GOLD, 18).set_stroke(opacity=0.3)
            self.play(*set_alpha([f.hemx, self.nlab], 0.3), Create(glow_r), run_time=1.5)
            c.wait_until("hugs")
            self.play(VShowPassingFlash(_plot(ax, math.sinh, 1.0, C1.SINH_HI, YELLOW, 9), time_width=0.6),
                      run_time=1.6)

            c.wait_until("left")
            glow_l = _plot(ax, lambda x: -0.5 * math.exp(-x), -math.log(6), -1.0, PURPLE, 18)
            glow_l.set_stroke(opacity=0.3).reverse_points()
            self.play(FadeOut(glow_r), *set_alpha([f.hemx, self.nlab], 1),
                      *set_alpha([f.hexp, f.lab_hexp], 0.3), run_time=1.0)
            self.play(Create(glow_l), run_time=1.4)

            c.wait_until("flip")
            self.play(VShowPassingFlash(_plot(ax, math.sinh, C1.SINH_LO, -1.0, YELLOW, 9).reverse_points(),
                                        time_width=0.6), run_time=1.6)

            c.wait_until("Out there")
            ghost = _plot(ax, math.cosh, -math.acosh(3), 0, TEAL, 6).set_stroke(opacity=0.7)
            self.play(FadeIn(ghost), run_time=0.6)
            self.play(Rotate(ghost, PI, axis=RIGHT, about_point=o), run_time=2.0)

            c.wait_until("gap")
            xs = [-1.5, -0.5, 0.5, 1.5]
            segs = [Line(ax.c2p(x, math.sinh(x)), ax.c2p(x, math.cosh(x))).set_stroke(PURPLE, 6) for x in xs]
            self.play(*during([FadeOut(glow_l), FadeOut(ghost)], 0, 0.5),
                      *set_alpha([f.cosh, f.lab_cosh], 1),
                      *set_alpha([f.hexp, f.hemx, f.lab_hexp, self.nlab], 0.3), run_time=1.0)
            self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.25), run_time=1.4)
            gap = set_backstroke(colored(r"\cosh x - \sinh x = e^{-x} > 0", 40,
                                         {(0, 5): TEAL, (6, 11): SINH_C, (12, 15): PURPLE}))
            gap.move_to(ax.c2p(1.25, -2.45))
            self.play(*appear(gap), run_time=1.0)

    # ------------------------------------------------------------ c3.odd.3
    def clip_tanh(self):
        with self.say("c3.odd.3") as c:
            tf = tanh_fig()
            self.tf = tf
            ax = tf.ax
            F = colored(r"\tanh x = \dfrac{\sinh x}{\cosh x} = \dfrac{e^{x} - e^{-x}}{e^{x} + e^{-x}}", 50,
                        {(0, 5): TANH_C, (6, 11): SINH_C, (12, 17): TEAL,
                         (18, 20): GOLD, (21, 24): PURPLE, (25, 27): GOLD, (28, 31): PURPLE})
            F.move_to([T_CENTER[0], 2.75, 0])
            self.F = F
            c.wait_until("divided")
            sweep_clear(self, FadeIn(ax), *appear(F), run_time=1.6)

            c.wait_until("top")
            top = VGroup(*F[0][18:24])
            bot = VGroup(*F[0][25:31])

            def box(g):
                return SurroundingRectangle(g, buff=0.1).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).set_z_index(-1)

            b = box(top)
            self.play(FadeIn(b), run_time=0.8)
            c.wait_until("bottom")
            self.play(Transform(b, box(bot)), run_time=1.0)

            c.wait_until("zero")
            dot = Dot(ax.c2p(0, 0), radius=0.11, color=YELLOW).set_z_index(3)
            self.play(FadeOut(b), Create(tf.tanh), GrowFromCenter(dot), run_time=2.0)
            self.tdot = dot

            c.wait_until("odd")
            odd = MathTex(r"\tanh(-x) = -\tanh x", font_size=PSZ, color=FG)
            for g in glyphs(odd, 0, 1, 2, 3, 10, 11, 12, 13):
                g.set_color(TANH_C)
            odd.move_to([NOTE_X, 2.75, 0])
            self.play(*appear(odd), run_time=1.0)
            self.odd = odd
            c.wait_until("an odd function")
            ghost = tf.tanh.copy().set_stroke(YELLOW, 9, opacity=0.7)
            self.play(FadeIn(ghost), run_time=0.4)
            self.play(Rotate(ghost, PI, axis=OUT, about_point=ax.c2p(0, 0)),
                      run_time=min(2.0, max(1.0, c.remaining - 0.6)))
            self.play(FadeOut(ghost), run_time=0.4)

    # ------------------------------------------------------------ c3.odd.4
    def clip_limits(self):
        tf, F = self.tf, self.F
        ax = tf.ax
        emx = glyphs(F, 21, 22, 23, 28, 29, 30)
        ex = glyphs(F, 18, 19, 25, 26)
        with self.say("c3.odd.4") as c:
            self.play(*set_alpha(emx, DIMMED), run_time=1.0)
            c.wait_until("one")
            one = colored(r"\dfrac{e^{x}}{e^{x}} = 1", 44, {(0, 2): GOLD, (3, 5): GOLD})
            one.move_to([NOTE_X, ax.c2p(0, 1)[1] + 0.15, 0])
            self.play(Create(tf.vp), *appear(one), run_time=1.5)

            c.wait_until("negx")
            self.play(*set_alpha(emx, 1), *set_alpha(ex, DIMMED), run_time=1.0)
            c.wait_until("you get minus one")
            mone = colored(r"\dfrac{-e^{-x}}{e^{-x}} = -1", 44, {(1, 4): PURPLE, (5, 8): PURPLE})
            mone.move_to([NOTE_X, ax.c2p(0, -1)[1] - 0.15, 0])
            self.play(Create(tf.vm), *appear(mone), run_time=1.5)

            c.wait_until("band")
            shade = Rectangle(width=TX_LEN, height=ax.c2p(0, 1)[1] - ax.c2p(0, -1)[1])
            shade.move_to(ax.c2p(0, 0)).set_stroke(width=0).set_fill(TANH_C, 0.13).set_z_index(-2)
            self.play(*set_alpha(ex, 1), FadeIn(shade), run_time=1.2)
            c.wait_until("always smaller")
            band = MathTex(r"-1 < \tanh x < 1", font_size=42, color=FG)
            for g in band[0][3:8]:
                g.set_color(TANH_C)
            band.move_to([NOTE_X, ax.c2p(0, 0)[1], 0])
            self.play(*appear(band), run_time=1.0)

    # ------------------------------------------------------------ c3.odd.5
    def clip_all(self):
        d = S4.fig25d_shot()
        lab = d.labels
        with self.say("c3.odd.5") as c:
            c.wait_until("all three")
            sweep_clear(self, FadeIn(d.ax), Create(d.cosh), Create(d.sinh), Create(d.tanh),
                        *appear(lab["cosh"], lab["sinh"], lab["tanh"], lag=0.2), run_time=2.0)  # early: the picture shown whole

            pairs = {k: [getattr(d, k), lab[k]] for k in ("cosh", "sinh", "tanh")}

            def spot(k, prev):
                return (set_alpha(pairs[k], 1)
                        + set_alpha(sum((pairs[j] for j in prev), []), DIMMED))

            c.wait_until("cosh")
            self.play(*spot("cosh", ["sinh", "tanh"]), run_time=1.0)
            self.play(VShowPassingFlash(d.cosh.copy().set_stroke(YELLOW, 10), time_width=0.6), run_time=1.2)
            c.wait_until("sinh")
            self.play(*spot("sinh", ["cosh"]), run_time=1.0)
            self.play(VShowPassingFlash(d.sinh.copy().set_stroke(YELLOW, 10), time_width=0.6), run_time=1.5)
            c.wait_until("tanh")
            self.play(*spot("tanh", ["sinh"]), run_time=1.0)
            self.play(VShowPassingFlash(d.tanh.copy().set_stroke(YELLOW, 10), time_width=0.6), run_time=1.5)

            c.wait_until("slope")
            self.play(*set_alpha(pairs["cosh"] + pairs["sinh"], 1), Create(d.yline), run_time=1.5)
            ax = d.ax
            self.play(VShowPassingFlash(_plot(ax, math.sinh, -0.7, 0.7, YELLOW, 10), time_width=0.8),
                      VShowPassingFlash(_plot(ax, math.tanh, -0.7, 0.7, YELLOW, 10), time_width=0.8),
                      run_time=1.5)
        # handover: settle on exactly fig25d_shot() and hold; ch3_s4 opens on it
        self.remove(*self.mobjects)
        self.add(*handover_shot().submobjects)
        self.wait(1.0)
