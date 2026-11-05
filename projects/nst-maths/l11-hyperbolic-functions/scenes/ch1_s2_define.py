"""Chapter 1, scene 2: real exponentials: cosh and sinh defined, drawn, and e^x = cosh x + sinh x. Clips c1.def.1 – c1.def.5.

Series graph style, defined here (import with load_scene("ch1_s2_define")):
- graph_axes(x_length=9, y_length=7, ticks=True): DIM axes, x in [-2.5, 2.5], y in [-3, 5], no tips.
- exp_curve(ax) GOLD e^x, emx_curve(ax) PURPLE e^{-x}, cosh_curve(ax, lo, hi) TEAL,
  sinh_curve(ax, lo, hi) SINH_C (a lighter teal); every curve is clipped to the y range.
- curve_label(ax, which): MathTex label placed by its curve ("exp", "emx", "cosh", "sinh").
- x_marks(ax, x=1.0): VGroup(line, gold, purple, mid) at x: DIM vertical line, the dots on e^x and
  e^{-x} and the TEAL midpoint (cosh x); .line .gold .purple .mid.
- exp_graph(): the finished graph of this scene (axes, four curves, labels), at GRAPH_CENTER;
  attributes .ax .exp .emx .cosh .sinh .labels (dict).
"""
# style: 2
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


# ---------------------------------------------------------------- series graph style
SINH_C = "#A8EBD9"                      # lighter teal: sinh, distinct from cosh's TEAL
X_LO, X_HI = -2.5, 2.5
Y_LO, Y_HI = -3.0, 5.0
L5 = math.log(5)
COSH_LIM = math.acosh(5)                # cosh reaches y = 5
SINH_LO, SINH_HI = math.asinh(-3), math.asinh(5)
GRAPH_CENTER = np.array([1.0, -0.1, 0])


def graph_axes(x_length=9.0, y_length=7.0, ticks=True):
    return Axes(x_range=[X_LO, X_HI, 1], y_range=[Y_LO, Y_HI, 1], x_length=x_length, y_length=y_length,
                tips=False, axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": ticks,
                                         "tick_size": 0.06})


def _plot(ax, f, lo, hi, color, width):
    if hi - lo < 1e-3:
        hi = lo + 1e-3
    return ax.plot(f, x_range=[lo, hi, 0.02], color=color, stroke_width=width)


def exp_curve(ax, width=5):
    return _plot(ax, math.exp, X_LO, L5, GOLD, width)


def emx_curve(ax, width=5):
    return _plot(ax, lambda x: math.exp(-x), -L5, X_HI, PURPLE, width)


def cosh_curve(ax, lo=-COSH_LIM, hi=COSH_LIM, width=6):
    return _plot(ax, math.cosh, max(lo, -COSH_LIM), min(hi, COSH_LIM), TEAL, width)


def sinh_curve(ax, lo=SINH_LO, hi=SINH_HI, width=6):
    return _plot(ax, math.sinh, max(lo, SINH_LO), min(hi, SINH_HI), SINH_C, width)


def curve_label(ax, which, size=40):
    if which == "exp":
        m = MathTex("e^{x}", font_size=size, color=GOLD)
        m.next_to(ax.c2p(math.log(4.6), 4.6), LEFT, buff=0.25)
    elif which == "emx":
        m = MathTex("e^{-x}", font_size=size, color=PURPLE)
        m.next_to(ax.c2p(-1.2, math.exp(1.2)), LEFT, buff=0.3)
    elif which == "cosh":
        m = MathTex(r"\cosh x", font_size=size, color=TEAL)
        m.next_to(ax.c2p(math.acosh(4.2), 4.2), RIGHT, buff=0.3)
    else:
        m = MathTex(r"\sinh x", font_size=size, color=SINH_C)
        m.next_to(ax.c2p(math.asinh(2.6), 2.6), RIGHT, buff=0.3)
    return set_backstroke(m)


def x_marks(ax, x=1.0):
    line = Line(ax.c2p(x, Y_LO), ax.c2p(x, Y_HI)).set_stroke(DIM, 3)
    gold = Dot(ax.c2p(x, math.exp(x)), radius=0.09, color=GOLD)
    purple = Dot(ax.c2p(x, math.exp(-x)), radius=0.09, color=PURPLE)
    mid = Dot(ax.c2p(x, math.cosh(x)), radius=0.11, color=TEAL)
    g = VGroup(line, gold, purple, mid)
    g.line, g.gold, g.purple, g.mid = line, gold, purple, mid
    return g


def exp_graph():
    ax = graph_axes().move_to(GRAPH_CENTER)
    ex, emx, ch, sh = exp_curve(ax), emx_curve(ax), cosh_curve(ax), sinh_curve(ax)
    labels = {k: curve_label(ax, k) for k in ("exp", "emx", "cosh", "sinh")}
    g = VGroup(ax, ex, emx, ch, sh, *labels.values())
    g.ax, g.exp, g.emx, g.cosh, g.sinh, g.labels = ax, ex, emx, ch, sh, labels
    return g


# ---------------------------------------------------------------- coloured maths
_COL = {"B": BLUE, "T": TEAL, "S": SINH_C, "P": PINK, "G": GOLD, "U": PURPLE, "F": FG, "Y": YELLOW,
        "D": DIM, "N": GREEN}


def ctex(src, pattern, size=52):
    """MathTex coloured glyph by glyph, one pattern letter per glyph (spaces ignored)."""
    m = MathTex(src, font_size=size)
    pat = pattern.replace(" ", "")
    assert len(m[0]) == len(pat), (src, len(m[0]), len(pat))
    for g, ch in zip(m[0], pat):
        g.set_color(_COL[ch])
    return m


def at_glyph(m, idx, x, y):
    m.shift(np.array([x, y, 0]) - m[0][idx].get_center())
    return m


def grp(m, a, b):
    return VGroup(*m[0][a:b])


SRC_COSH = (r"\cosh x = \frac{1}{2}\left(e^{x} + e^{-x}\right)", "TTTTF F FFF F GG F UUU F")
SRC_SINH_I = (r"\sinh x = \frac{1}{2i}\left(e^{x} - e^{-x}\right)", "SSSSF F FFFP F GG F UUU F")
SRC_SINH = (r"\sinh x = \frac{1}{2}\left(e^{x} - e^{-x}\right)", "SSSSF F FFF F GG F UUU F")
SRC_SUM = (r"\cosh x + \sinh x = \tfrac{1}{2}e^{x} + \tfrac{1}{2}e^{-x} + \tfrac{1}{2}e^{x} - \tfrac{1}{2}e^{-x}",
           "TTTTF F SSSSF F FFFGG F FFFUUU F FFFGG F FFFUUU")
SRC_SUM2 = (r"\cosh x + \sinh x = e^{x}", "TTTTF F SSSSF F GG")
SRC_RESULT = (r"e^{x} = \cosh x + \sinh x", "GG F TTTTF F SSSSF")
SRC_COUSIN = (r"e^{ix} = \cos x + i \sin x", "BPB F BBBB F P BBBB")

X_COSH, X_SINH = -3.4, 3.4         # centres of the two definition columns
Y_DEF = -0.9
SZ = 50


def bracket(bottom, top, color, off=0.22, arm=0.14):
    """A ] bracket just right of the vertical span bottom..top (a shape, so it can morph)."""
    r = off * RIGHT
    a = arm * RIGHT
    m = VMobject().set_points_as_corners([bottom + r, bottom + r + a, top + r + a, top + r])
    return m.set_stroke(color, 4)


def eq_number(text, line):
    n = T(text, size=28, color=DIM)
    n.next_to(line, DOWN, buff=0.35)
    return n


def place_def(m, x):
    m.move_to([x, Y_DEF, 0])
    return m


class Define(NarratedScene):
    def construct(self):
        hook = load_scene("ch1_s1_hook")

        # ------------------------------------------------ c1.def.1: last time's pair, and the question
        with self.say("c1.def.1") as c:
            pair = hook.cos_sin_pair()
            self.play(*appear(pair, shift=None), run_time=1.0)
            c.wait_until("Cosine of ex")
            self.play(FlashAround(pair.cos, color=BLUE, run_time=1.6, time_width=1.5))
            c.wait_until("Sine of ex")
            self.play(FlashAround(pair.sin, color=BLUE, run_time=1.6, time_width=1.5))
            c.wait_until("ask")
            self.play(pair.cos.animate.scale(0.75).move_to([-3.4, 2.8, 0]),
                      pair.sin.animate.scale(0.75).move_to([3.4, 2.8, 0]),
                      run_time=min(1.6, c.until("What happens")))  # pair settles in the top row
            rings = VGroup(*[Circle(radius=0.17).set_stroke(YELLOW, 3).move_to(line[k])
                             for line in (pair.cos, pair.sin) for k in (5, 9)])
            self.play(*[GrowFromCenter(r) for r in rings], run_time=0.8)
            question = T("What if the exponent is real?", size=44, color=YELLOW).move_to([0, 0.95, 0])
            c.wait_until(own_word=question, cue="What happens")
            self.play(*appear(question), run_time=1.0)

        # ------------------------------------------------ c1.def.2: cosh and sinh
        with self.say("c1.def.2") as c:
            big = hook.cos_sin_pair(size=SZ)
            cos_a, sin_a = big.cos, big.sin
            cos_a.move_to([X_COSH, Y_DEF, 0])
            sin_a.move_to([X_SINH, Y_DEF, 0])
            self.play(*disappear(question, rings), run_time=0.8)
            self.play(*fly(pair.cos, cos_a), run_time=min(1.6, c.until("E to the ex, plus")), rate_func=linear)
            cosh = place_def(ctex(*SRC_COSH, size=SZ), X_COSH)
            n84 = eq_number("(84)", cosh)
            c.wait_until("E to the ex, plus")
            self.play(*edit(cos_a, cosh), run_time=2.0)
            c.wait_until("hyperbolic cosine")
            self.play(*appear(n84, shift=None), FlashAround(grp(cosh, 0, 4), color=TEAL, time_width=1.5),
                      run_time=1.4)

            c.wait_until("sinh")
            self.play(*fly(pair.sin, sin_a), run_time=1.6, rate_func=linear)
            sinh_i = place_def(ctex(*SRC_SINH_I, size=SZ), X_SINH)
            self.play(*edit(sin_a, sinh_i), run_time=min(2.0, c.until("denom")))
            c.wait_until("denom")
            self.play(FlashAround(grp(sinh_i, 8, 10), color=YELLOW, run_time=1.6, time_width=1.5))
            sinh = place_def(ctex(*SRC_SINH, size=SZ), X_SINH)
            n85 = eq_number("(85)", sinh)
            c.wait_until("It's just two")
            self.play(*edit(sinh_i, sinh), run_time=1.6)
            self.play(*appear(n85, shift=None), run_time=0.8)
            c.wait_until("real")
            tag = T("real in, real out", size=40, color=GREEN).move_to([0, -3.1, 0])
            self.play(*appear(tag), run_time=1.0)

        # ------------------------------------------------ c1.def.3: the two exponentials, and x = 1
        with self.say("c1.def.3") as c:
            ax = graph_axes().move_to(GRAPH_CENTER)
            corner = VGroup(cosh.copy(), sinh.copy()).scale(0.68).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            corner.to_corner(UL, buff=0.5)
            for m, t in zip((cosh, sinh), corner):
                m.target = t
            self.play(*during(disappear(pair, n84, n85, tag), 0, 0.35),
                      *during([MoveToTarget(cosh)], 0.25, 0.7),
                      *during([MoveToTarget(sinh)], 0.55, 1.0), run_time=2.2)
            self.play(Create(ax), run_time=1.4)
            c.wait_until("gold")
            ex = exp_curve(ax)
            lab_ex = curve_label(ax, "exp")
            self.play(Create(ex), run_time=1.8, rate_func=linear)
            self.play(*appear(lab_ex), run_time=0.8)
            c.wait_until("purple")
            emx = emx_curve(ax)
            lab_emx = curve_label(ax, "emx")
            self.play(Create(emx), run_time=1.8, rate_func=linear)
            self.play(*appear(lab_emx), run_time=0.8)

            c.wait_until("stand")
            xt = ValueTracker(1.0)
            marks = x_marks(ax, 1.0)
            self.play(Create(marks.line), run_time=1.2)
            v_gold = MathTex("2.72", font_size=36, color=GOLD)
            v_gold.next_to(marks.gold, LEFT, buff=0.2)
            v_purple = MathTex("0.37", font_size=36, color=PURPLE)
            v_purple.next_to(marks.purple, UR, buff=0.1)
            set_backstroke(v_gold)
            set_backstroke(v_purple)
            c.wait_until("Here E to the ex")
            self.play(GrowFromCenter(marks.gold), *appear(v_gold), run_time=1.2)
            c.wait_until("zero point three seven")
            self.play(GrowFromCenter(marks.purple), *appear(v_purple), run_time=1.2)
            c.wait_until("mid")
            seg = DashedLine(marks.gold.get_center(), marks.purple.get_center(), dash_length=0.08)
            seg.set_stroke(FG, 2)
            v_mid = set_backstroke(MathTex(r"\cosh 1 \approx 1.54", font_size=40, color=TEAL))
            v_mid.next_to(marks.mid, RIGHT, buff=0.3)
            self.play(Create(seg), run_time=0.8)
            self.play(GrowFromCenter(marks.mid), *appear(v_mid), run_time=1.2)

        # ------------------------------------------------ c1.def.4: sweep: cosh, then sinh
        with self.say("c1.def.4") as c:
            def follow(dot, f):
                def upd(m):
                    x = xt.get_value()
                    y = f(x)
                    m.move_to(ax.c2p(x, min(max(y, Y_LO), Y_HI)))
                    m.set_opacity(1.0 if Y_LO <= y <= Y_HI else 0.0)
                return upd

            def tracer(make):
                lo = [xt.get_value()]
                hi = [xt.get_value()]
                curve = make(ax, lo[0], hi[0])

                def upd(m):
                    x = xt.get_value()
                    lo[0], hi[0] = min(lo[0], x), max(hi[0], x)
                    m.become(make(ax, lo[0], hi[0]))
                curve.add_updater(upd)
                return curve

            line_upd = lambda m: m.put_start_and_end_on(ax.c2p(xt.get_value(), Y_LO),  # noqa: E731
                                                        ax.c2p(xt.get_value(), Y_HI))
            ch_curve = tracer(cosh_curve)
            ch_curve.set_z_index(-1)
            self.add(ch_curve)
            marks.line.add_updater(line_upd)
            marks.gold.add_updater(follow(marks.gold, math.exp))
            marks.purple.add_updater(follow(marks.purple, lambda x: math.exp(-x)))
            marks.mid.add_updater(follow(marks.mid, math.cosh))

            def path_cosh(a):                       # 1 -> -lim, then -lim -> +lim
                lim = COSH_LIM
                if a < 0.35:
                    return 1 + (-lim - 1) * smooth(a / 0.35)
                return -lim + 2 * lim * smooth((a - 0.35) / 0.65)
            self.play(UpdateFromAlphaFunc(xt, lambda m, a: m.set_value(path_cosh(a))),
                      *during(disappear(v_gold, v_purple, v_mid, seg), 0.0, 0.12),
                      run_time=min(5.5, c.until("gap") - 0.9), rate_func=linear)
            ch_curve.clear_updaters()
            lab_ch = curve_label(ax, "cosh")
            self.play(*appear(lab_ch), run_time=0.8)

            c.wait_until("gap")
            self.play(xt.animate.set_value(1.0), run_time=1.4)
            gap_line = Line(marks.purple.get_center(), marks.gold.get_center())
            brace = bracket(marks.purple.get_center(), marks.gold.get_center(), FG)
            self.play(GrowFromCenter(brace), run_time=1.2)
            half_line = Line(ax.c2p(1, 0), ax.c2p(1, math.sinh(1)))
            brace2 = bracket(half_line.get_start(), half_line.get_end(), SINH_C)
            self.play(Transform(brace, brace2), run_time=1.6)
            sdot = Dot(ax.c2p(1, math.sinh(1)), radius=0.11, color=SINH_C)
            v_sinh = set_backstroke(MathTex(r"\sinh 1 \approx 1.18", font_size=40, color=SINH_C))
            v_sinh.next_to(brace, RIGHT, buff=0.2).align_to(sdot, DOWN).shift(0.05 * DOWN)
            self.play(GrowFromCenter(sdot), *appear(v_sinh), run_time=1.2)

            c.wait_until("zero")
            sh_curve = tracer(sinh_curve)
            sh_curve.set_z_index(-1)
            self.add(sh_curve)
            sdot.add_updater(follow(sdot, math.sinh))
            self.play(*during(disappear(brace, v_sinh), 0, 0.3),
                      xt.animate.set_value(0.0), run_time=2.2)
            self.play(FlashAround(marks.gold, color=YELLOW, run_time=1.2, time_width=1.5),
                      FlashAround(sdot, color=YELLOW, run_time=1.2, time_width=1.5))
            c.wait_until("To the left")
            self.play(xt.animate.set_value(SINH_LO), run_time=2.6)
            c.wait_until("So cosh is the average")
            moving = [marks.line, marks.gold, marks.purple, marks.mid, sdot]
            self.play(xt.animate.set_value(SINH_HI), *during(disappear(*moving), 0.7, 1.0),
                      run_time=2.6)
            for m in moving + [sh_curve]:
                m.clear_updaters()
            self.remove(*moving)
            lab_sh = curve_label(ax, "sinh")
            self.play(*appear(lab_sh), run_time=0.8)

        # ------------------------------------------------ c1.def.5: e^x = cosh x + sinh x
        with self.say("c1.def.5") as c:
            graph = [ax, ex, emx, ch_curve, sh_curve, lab_ex, lab_emx, lab_ch, lab_sh]
            self.play(*set_alpha(graph, 0.18), run_time=1.0)
            eq = ctex(*SRC_SUM, size=52).move_to([0, 0.2, 0])
            eq_bg = BackgroundRectangle(eq, fill_opacity=0.9, buff=0.25)
            self.add(eq_bg)
            c.wait_until("Add cosh and shine")
            self.play(FadeIn(eq_bg), *appear(eq, shift=None), run_time=1.2)
            c.wait_until("cancel")
            strikes = [Line(grp(eq, a, b).get_corner(DL), grp(eq, a, b).get_corner(UR)).set_stroke(RED, 5)
                       for a, b in ((18, 24), (31, 37))]
            self.play(*[Create(s) for s in strikes], run_time=1.2)
            self.play(*recolor(list(grp(eq, 18, 24)) + list(grp(eq, 31, 37)), RED), run_time=0.6)
            eq2 = ctex(*SRC_SUM2, size=56).move_to([0, 0.2, 0])
            c.wait_until("the two E to the ex terms")
            self.play(*during(disappear(*strikes), 0, 0.4), *edit(eq, eq2), run_time=2.0)

            c.wait_until("result")
            result = ctex(*SRC_RESULT, size=56).move_to([0, 0.2, 0])
            box = SurroundingRectangle(result, color=YELLOW, buff=0.25)
            self.play(*swap(eq2, result), run_time=1.4)
            self.play(GrowFromCenter(box), run_time=0.8)
            c.wait_until("cousin")
            rbox = VGroup(result, box)
            self.remove(result, box)
            self.add(rbox)
            cousin = ctex(*SRC_COUSIN, size=56).move_to([3.4, 0.2, 0])
            self.play(rbox.animate.move_to([-3.3, 0.2, 0]),
                      eq_bg.animate.stretch_to_fit_width(13.4).move_to([0, 0.2, 0]), run_time=1.4)
            self.play(*appear(cousin, shift=None), run_time=1.2)
            c.wait_until("same pattern")
            self.play(*flash([cousin[0][1], cousin[0][9]], color=PINK, run_time=1.4, time_width=1.5))

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
