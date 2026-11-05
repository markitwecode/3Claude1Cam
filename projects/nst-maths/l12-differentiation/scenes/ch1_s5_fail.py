"""Chapter 1, scene 5: a corner and a jump (|x| and the Heaviside step). Clips c1.fail.1 – c1.fail.4.

Exported helpers (s6 and the recap import them; both are built with the axes' origin at ORIGIN,
unit 1.6, and are moved/scaled as a whole: `g = v_graph().scale(0.45).move_to(...)`):

- `v_graph()` -> VGroup(ax, curve, corner)
    .ax      Axes, x in [-2.4, 2.4], y in [-0.6, 2.4], DIM, no numbers
    .curve   BLUE y = |x| on x in [-2, 2] (a polyline through (-2,2), (0,0), (2,2)), stroke 5
    .corner  RED Dot (r 0.09) at the origin
- `step_graph()` -> VGroup(ax, left, right, jump, hole, dot)
    .ax      Axes, x in [-2.2, 2.2], y in [-0.6, 1.8], DIM, no numbers
    .left    BLUE line y = 0 for x in [-2, 0], stroke 5
    .right   BLUE line y = 1 for x in [0, 2], stroke 5
    .jump    dashed RED vertical (0, 0)-(0, 1)
    .hole    open circle at (0, 0): BLUE ring, BG fill (r 0.09)
    .dot     filled BLUE dot at (0, 1) (r 0.09)
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

UNIT = 1.6
AXIS_CFG = {"color": DIM, "stroke_width": 2, "tip_width": 0.2, "tip_height": 0.2}


def _axes(xr, yr):
    ax = Axes(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1],
              x_length=(xr[1] - xr[0]) * UNIT, y_length=(yr[1] - yr[0]) * UNIT,
              axis_config=AXIS_CFG)
    ax.shift(-ax.c2p(0, 0))
    return ax


def v_graph():
    ax = _axes((-2.4, 2.4), (-0.6, 2.4))
    curve = VMobject().set_points_as_corners([ax.c2p(-2, 2), ax.c2p(0, 0), ax.c2p(2, 2)])
    curve.set_stroke(BLUE, 5)
    corner = Dot(ax.c2p(0, 0), radius=0.09, color=RED).set_z_index(3)
    g = VGroup(ax, curve, corner)
    g.ax, g.curve, g.corner = ax, curve, corner
    return g


def step_graph():
    ax = _axes((-2.2, 2.2), (-0.6, 1.8))
    left = Line(ax.c2p(-2, 0), ax.c2p(0, 0)).set_stroke(BLUE, 5)
    right = Line(ax.c2p(0, 1), ax.c2p(2, 1)).set_stroke(BLUE, 5)
    jump = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1), dash_length=0.1).set_stroke(RED, 4)
    hole = Circle(radius=0.09).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(ax.c2p(0, 0)).set_z_index(3)
    dot = Dot(ax.c2p(0, 1), radius=0.09, color=BLUE).set_z_index(3)
    g = VGroup(ax, left, right, jump, hole, dot)
    g.ax, g.left, g.right, g.jump, g.hole, g.dot = ax, left, right, jump, hole, dot
    return g


def axis_labels(ax):
    xl = MathTex("x", font_size=36, color=DIM).next_to(ax.x_axis.get_right(), DOWN, buff=0.15)
    yl = MathTex("y", font_size=36, color=DIM).next_to(ax.y_axis.get_top(), LEFT, buff=0.15)
    return xl, yl


class Fail(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- |x|
    def clip1(self):
        v = v_graph()
        v.shift(1.4 * DOWN)
        self.v = v
        ax = v.ax
        v.remove(v.corner)
        xl, yl = axis_labels(ax)
        self.vxl, self.vyl = xl, yl
        label = MathTex("y = |x|", font_size=48, color=BLUE).move_to(ax.c2p(1.25, 2.25))
        self.vlabel = label
        with self.say("c1.fail.1") as c:
            self.play(Create(ax), run_time=1.5)
            self.play(*appear(xl, yl, shift=None), run_time=0.8)
            c.wait_until("modx")
            self.play(Create(v.curve), run_time=1.6)
            c.wait_until("why equals")
            self.play(*appear(label), run_time=1.0)
            settle(self, v)

            c.wait_until("left")
            tl = Line(ax.c2p(-1.7, 1.7), ax.c2p(-0.5, 0.5)).set_stroke(GREEN, 9)
            ll = T("slope −1", 32, GREEN).move_to(ax.c2p(-1.45, 0.55))
            self.play(Create(tl), run_time=1.2)
            c.wait_until(own_word=ll)
            self.play(*appear(ll), run_time=1.0)

            c.wait_until("right")
            tr = Line(ax.c2p(0.5, 0.5), ax.c2p(1.7, 1.7)).set_stroke(GREEN, 9)
            lr = T("slope +1", 32, GREEN).move_to(ax.c2p(1.45, 0.55))
            self.play(Create(tr), run_time=1.2)
            c.wait_until(own_word=lr)
            self.play(*appear(lr), run_time=1.0)
            self.tangents = [tl, ll, tr, lr]

            c.wait_until("continuous")
            pen = Dot(ax.c2p(-2, 2), radius=0.11, color=YELLOW).set_z_index(4)
            self.play(FadeIn(pen, scale=0.5), run_time=0.5)
            self.play(MoveAlongPath(pen, v.curve.copy()), rate_func=linear,
                      run_time=min(3.2, c.until() - 0.9))
            self.play(FadeOut(pen), run_time=0.6)

    # ---------------------------------------------------------------- corner, chords
    def clip2(self):
        v, ax = self.v, self.v.ax
        o = ax.c2p(0, 0)
        others = [self.vxl, self.vyl, self.vlabel]
        with self.say("c1.fail.2") as c:
            self.play(*during(disappear(*self.tangents), 0, 0.4),
                      *during([v.animate.scale(1.2, about_point=o)]
                              + [m.animate.scale(1.2, about_point=o) for m in others], 0.2, 1),
                      run_time=1.6)
            corner = self.v_corner = Dot(o, radius=0.09 * 1.2, color=RED).set_z_index(3)
            self.play(GrowFromCenter(corner), FlashAround(corner, color=RED, run_time=1.2,
                                                          time_width=1.5), run_time=1.2)
            settle(self, v, add=[corner])
            v.corner = corner

            c.wait_until("candidates")
            L = 2.8
            line = Line(o + L * LEFT, o + L * RIGHT).set_stroke(FG, 4).set_z_index(2)
            q = T("?", 64, YELLOW).move_to(o + 1.5 * UP)
            self.play(GrowFromCenter(line), run_time=1.2)
            self.play(*appear(q), run_time=0.8)
            c.wait_until("lots of lines")
            self.play(Rotate(line, angle=35 * DEGREES, about_point=o), run_time=1.3)
            self.play(Rotate(line, angle=-70 * DEGREES, about_point=o), run_time=2.0)
            self.play(Rotate(line, angle=35 * DEGREES, about_point=o), run_time=1.0)

            c.wait_until("rightchord")
            self.play(*disappear(line, q), run_time=0.8)
            rch = self.chords(ax, [0.6, 1.2, 1.8])
            rl = T("slope +1", 34, TEAL).move_to(ax.c2p(1.45, 0.5))
            self.play(*[Create(m) for m in rch[0]], *[FadeIn(d, scale=0.5) for d in rch[1]],
                      *during(appear(rl), 0.5, 1), run_time=1.8)

            c.wait_until("leftchord")
            lch = self.chords(ax, [-0.6, -1.2, -1.8])
            ll = T("slope −1", 34, TEAL).move_to(ax.c2p(-1.45, 0.5))
            self.play(*[Create(m) for m in lch[0]], *[FadeIn(d, scale=0.5) for d in lch[1]],
                      *during(appear(ll), 0.5, 1), run_time=1.8)

            # {fails}: the V moves left, the formula arrives on the right
            c.wait_until("fails")
            # chords and their labels ride along with the V (labels keep their size) and stay up
            # until the V shrinks into its thumbnail at the start of c1.fail.3
            shapes = rch[0] + rch[1] + lch[0] + lch[1]
            s = 0.7
            d = np.array([-3.35, -1.0, 0]) - o
            moves = [m.animate.scale(s, about_point=o).shift(d) for m in [v] + others + shapes]
            moves += [m.animate.move_to((m.get_center() - o) * s + o + d) for m in [rl, ll]]
            self.play(*moves, run_time=1.6)
            self.chord_stuff = shapes + [rl, ll]
            formula = MathTex(r"\frac{d|x|}{dx} = \begin{cases} -1 & \text{if } x < 0, \\"
                              r" +1 & \text{if } x > 0, \end{cases}", font_size=46)
            formula.move_to([3.5, 0.9, 0])
            self.play(*appear(formula), run_time=1.0)
            c.wait_until("does not exist")
            bad = T("but d|x|/dx does not exist\nat x = 0.", 34, RED).next_to(formula, DOWN, buff=0.6)
            self.play(*appear(bad), run_time=1.0)
            c.wait_until("everywhere else")
            self.play(FlashAround(formula, run_time=1.8, time_width=1.5))
            self.formula, self.bad = formula, bad

    def chords(self, ax, xs):
        o = ax.c2p(0, 0)
        lines = [Line(o, ax.c2p(x, abs(x))).set_stroke(TEAL, 7).set_z_index(1) for x in xs]
        dots = [Dot(ax.c2p(x, abs(x)), radius=0.08, color=TEAL).set_z_index(2) for x in xs]
        return lines, dots

    # ---------------------------------------------------------------- Heaviside
    def clip3(self):
        v = self.v
        sg = step_graph()
        sg.shift(np.array([2.5, -1.2, 0]))
        self.sg = sg
        ax = sg.ax
        xl, yl = axis_labels(ax)
        with self.say("c1.fail.3") as c:
            # the V shrinks into a thumbnail, top-left
            vt = v.copy()
            vt.scale(3.4 / v.width).move_to([-4.8, 2.45, 0])
            lab_t = MathTex("y = |x|", font_size=32, color=BLUE).next_to(vt, DOWN, buff=0.15)
            self.play(*during(disappear(self.bad, self.vxl, self.vyl, *self.chord_stuff), 0, 0.45),
                      *during([Transform(v, vt), Transform(self.vlabel, lab_t)], 0.2, 1),
                      run_time=1.5)
            hdef = MathTex(r"H(x) = \begin{cases} 0 & x < 0, \\ 1 & x > 0, \end{cases}", font_size=44)
            hdef.move_to([-4.3, -1.0, 0])
            num = T("(104)", 28, DIM).next_to(hdef, RIGHT, buff=0.3)
            self.hdef = VGroup(hdef, num)
            self.play(*appear(hdef, num, lag=0.3), run_time=1.2)

            c.wait_until("zero")
            self.play(*during(disappear(self.formula), 0, 0.4),
                      *during([Create(ax)] + appear(xl, yl, shift=None), 0.3, 1), run_time=1.2)
            self.play(Create(sg.left), run_time=0.8)
            c.wait_until("one")
            self.play(Create(sg.right), run_time=1.0)

            c.wait_until("conv")
            q = MathTex(r"x = 0\ ?", font_size=40, color=YELLOW).move_to(ax.c2p(-0.75, 0.55))
            tag = T("definitions vary", 30, DIM).move_to(ax.c2p(-1.2, 1.1))
            self.play(*appear(q), run_time=1.0)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)

            c.wait_until("filled dot")
            self.play(*during(disappear(q, tag), 0, 0.4),
                      *during([GrowFromCenter(sg.dot), FlashAround(sg.dot, time_width=1.5)], 0.3, 1),
                      run_time=1.6)
            c.wait_until("open circle")
            self.play(GrowFromCenter(sg.hole), run_time=1.0)
            c.wait_until("exactly one value")
            self.play(FlashAround(sg.dot, run_time=1.5, time_width=1.5))

    # ---------------------------------------------------------------- dH/dx, the chord across the jump
    def clip4(self):
        sg, ax = self.sg, self.sg.ax
        with self.say("c1.fail.4") as c:
            f1 = T("slope 0", 32, GREEN).move_to(ax.c2p(-1.2, -0.33))
            f2 = T("slope 0", 32, GREEN).move_to(ax.c2p(1.2, 1.33))
            self.play(*appear(f1, f2, lag=0.3), run_time=1.2)  # early: narration says "flat ... derivative is zero"

            c.wait_until("undefined")
            ddef = MathTex(r"\frac{dH}{dx} = \begin{cases} 0 & x \neq 0 \\ ",
                           r"\text{undefined}", r" & \text{at } x = 0 \end{cases}", font_size=40)
            ddef[1].set_color(RED)
            ddef.move_to([-4.0, -1.0, 0])
            self.play(*swap(self.hdef, ddef), Create(sg.jump), run_time=1.4)

            c.wait_until("cross")
            dx = ValueTracker(1.0)
            chord = always_redraw(lambda: Line(ax.c2p(-dx.get_value(), 0), ax.c2p(0, 1))
                                  .set_stroke(TEAL, 5).set_z_index(2))
            foot = always_redraw(lambda: Dot(ax.c2p(-dx.get_value(), 0), radius=0.08, color=TEAL)
                                 .set_z_index(3))
            self.play(*during(disappear(f1, f2), 0, 0.4),
                      *during([Create(chord), FadeIn(foot)], 0.35, 1), run_time=1.6)
            br = span_brace(ax.c2p(-1, 0), ax.c2p(0, 0), DOWN, color=TEAL)
            dxl = MathTex(r"\delta x", font_size=40, color=TEAL).next_to(br, DOWN, buff=0.1)
            one = MathTex("1", font_size=40, color=TEAL).move_to(ax.c2p(0.22, 0.5))
            self.play(GrowFromCenter(br), *appear(dxl, one, lag=0.4), run_time=1.3)

            c.wait_until("slopeh")
            self.play(FlashAround(one, run_time=1.2, time_width=1.5))
            c.wait_until("run of delta")
            self.play(FlashAround(dxl, run_time=1.2, time_width=1.5))
            c.wait_until("so its slope")
            rd = MathTex(r"\text{slope} = \frac{1}{\delta x}", font_size=46).move_to([4.95, 3.05, 0])
            self.play(*appear(rd), run_time=1.0)

            c.wait_until("grow")
            r1 = MathTex(r"\delta x = 0.1:\ \text{slope } 10", font_size=36, color=GOLD)
            r1.move_to([4.95, 2.25, 0])
            self.play(*during(disappear(br, dxl), 0, 0.3),
                      *during([dx.animate.set_value(0.1)], 0.15, 0.8),
                      *during(appear(r1), 0.35, 0.75), run_time=2.4)

            c.wait_until("with a hundredth")
            r2 = MathTex(r"\delta x = 0.01:\ \text{slope } 100", font_size=36, color=GOLD)
            r2.next_to(r1, DOWN, buff=0.3)
            self.play(*during([dx.animate.set_value(0.01)], 0, 0.7),
                      *during(appear(r2), 0.3, 0.8), *set_alpha([r1], 0.5), run_time=1.6)

            c.wait_until("grows without bound")
            self.play(*recolor(r2, RED), FlashAround(r2, color=RED, time_width=1.5), run_time=1.8)
            chord.clear_updaters()
            foot.clear_updaters()
