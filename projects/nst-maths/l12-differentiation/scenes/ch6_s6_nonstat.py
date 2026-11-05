"""Chapter 6, scene 6: inflections that aren't stationary; the three graphs; the x^4 + x trap. Clips c6.nonstat.1 – c6.nonstat.4.

Exports (static, named parts):
three_graphs() -> VGroup   the notes' three graphs in a row, as clip 3 ends
    .heading   T "point of inflection" over the row
    .left .middle .right   panels (y = x^3 + x, y = x^3, y = x^3 - 3x), each with
        .axes .curve (BLUE) .name (MathTex, BLUE, above) .dot (YELLOW, origin) .tan (GREEN tangent)
        .info (VGroup of MathTex: y'(0) = ..., y''(0) = 0[, y'''(0) = 6 \\neq 0]) .word (T rising /
        stationary / falling) .down .up (T "concave down" RED / "concave up" GREEN, on the curve)
    .panels (VGroup left, middle, right) .same (MathTex y'' = 6x, under all three)
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

_s1 = load_scene("ch6_s1_hook")
_s2 = load_scene("ch6_s2_vocab")
_s4 = load_scene("ch6_s4_higher")
AXIS_CFG = _s4.AXIS_CFG


def _yp(x):
    """y' of the notes' curve: (x + 2)(x + 1/2)(x - 3/2)^2."""
    return (x + 2) * (x + 0.5) * (x - 1.5) ** 2


def _tilted_tangent(fig, x, half=0.8):
    p = fig.at_x(x)
    d = fig.axes.c2p(x + 1, _s1.curve_y(x) + _yp(x)) - p
    d = d / np.linalg.norm(d)
    return Line(p - half * d, p + half * d, color=GREEN, stroke_width=5).set_z_index(1)


# ---------------------------------------------------------------- the three graphs
ROW_Y = 0.75
PANEL_XS = (-4.6, 0.0, 4.6)
INFO_YS = (-1.05, -1.6, -2.15)
WORD_Y = -2.75
SPECS = [
    # f, plot range, slope at 0, name, info lines, word, concavity label positions (down, up) offsets
    (lambda x: x ** 3 + x, (-1.15, 1.15), 1, r"y = x^3 + x",
     [r"y'(0) = 1 \neq 0", r"y''(0) = 0"], "rising", ((-0.95, 0.72), (0.95, -0.72))),
    (lambda x: x ** 3, (-1.38, 1.38), 0, r"y = x^3",
     [r"y'(0) = 0", r"y''(0) = 0", r"y'''(0) = 6 \neq 0"], "stationary", ((-0.95, 0.72), (0.95, -0.72))),
    (lambda x: x ** 3 - 3 * x, (-1.0, 1.0), -3, r"y = x^3 - 3x",
     [r"y'(0) = -3 \neq 0", r"y''(0) = 0"], "falling", ((-0.95, -0.72), (0.95, 0.72))),
]


def _graph_panel(i):
    f, xr, slope, name, info, word, (dn, up) = SPECS[i]
    cx = PANEL_XS[i]
    p = VGroup()
    ax = Axes(x_range=[-1.4, 1.4, 1], y_range=[-2.7, 2.7, 1], x_length=3.4, y_length=2.7,
              tips=True, axis_config=AXIS_CFG)
    ax.shift(np.array([cx, ROW_Y, 0]) - ax.c2p(0, 0))
    p.axes = ax
    p.curve = ax.plot(f, x_range=[xr[0], xr[1], 0.01], color=BLUE, stroke_width=4)
    p.name = MathTex(name, font_size=40, color=BLUE).move_to([cx, ROW_Y + 1.82, 0])
    o = ax.c2p(0, 0)
    p.dot = Dot(o, radius=0.09, color=YELLOW).set_z_index(2)
    d = ax.c2p(1, slope) - o
    d = d / np.linalg.norm(d)
    p.tan = Line(o - 0.95 * d, o + 0.95 * d, color=GREEN, stroke_width=4).set_z_index(1)
    p.info = VGroup(*[MathTex(s, font_size=34, color=FG).move_to([cx, y, 0]) for s, y in zip(info, INFO_YS)])
    p.word = T(word, 34, YELLOW).move_to([cx, WORD_Y, 0])
    p.down = T("concave\ndown", 28, RED, line_spacing=0.75).move_to(o + np.array([dn[0], dn[1], 0]))
    p.up = T("concave\nup", 28, GREEN, line_spacing=0.75).move_to(o + np.array([up[0], up[1], 0]))
    p.add(ax, p.curve, p.name, p.tan, p.dot, p.info, p.word, p.down, p.up)
    return p


def three_graphs():
    g = VGroup()
    g.heading = T("point of inflection", 40).move_to([0, 3.35, 0])
    g.left, g.middle, g.right = (_graph_panel(i) for i in range(3))
    g.panels = VGroup(g.left, g.middle, g.right)
    g.same = MathTex(r"y'' = 6x", font_size=42, color=FG).move_to([0, -3.3, 0])
    g.add(g.heading, g.panels, g.same)
    return g


# ---------------------------------------------------------------- the trap
def _quartic_panel():
    p = VGroup()
    ax = Axes(x_range=[-1.6, 1.3, 1], y_range=[-0.8, 3.8, 1], x_length=6.0, y_length=5.6,
              tips=True, axis_config=AXIS_CFG)
    ax.move_to([-3.2, -0.35, 0])
    p.axes = ax
    p.curve = ax.plot(lambda x: x ** 4 + x, x_range=[-1.5, 1.2, 0.01], color=BLUE, stroke_width=5)
    p.name = MathTex(r"y = x^4 + x", font_size=48, color=BLUE).move_to([-3.2, 3.2, 0])
    o = ax.c2p(0, 0)
    p.dot = Dot(o, radius=0.11, color=YELLOW).set_z_index(2)
    d = ax.c2p(1, 1) - o
    d = d / np.linalg.norm(d)
    p.tan = Line(o - 1.3 * d, o + 1.3 * d, color=GREEN, stroke_width=5).set_z_index(1)
    p.up_l = T("concave up", 30, GREEN).move_to(ax.c2p(-0.62, 2.1))
    p.up_r = T("concave up", 30, GREEN).move_to(ax.c2p(0.55, 2.9))
    return p


class NonStatScene(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------- clip 1
        lf = _s2.labelled_figure()
        fig = lf.fig
        top = VGroup(fig, lf.labels)
        strip = lf.strip
        with self.say("c6.nonstat.1") as c:
            self.play(FadeIn(top), FadeIn(strip), run_time=min(1.5, c.until("plain")))  # early: the notes' labelled figure, inherited whole
            c.wait_until("plain")
            b1, b2 = fig.bend1, fig.bend2
            self.play(*flash([b1, b2], run_time=1.5, time_width=1.5),
                      b1.animate(rate_func=there_and_back).scale(1.8),
                      b2.animate(rate_func=there_and_back).scale(1.8), run_time=1.5)
            c.wait_until("tilt")
            tilts = [_tilted_tangent(fig, _s1.BEND1_X), _tilted_tangent(fig, _s1.BEND2_X)]
            flats = [_s2._flat_tangent(d) for d in (fig.peak, fig.valley, fig.flat)]
            self.play(*[GrowFromCenter(m) for m in flats], run_time=1.0)
            self.play(*[GrowFromCenter(m) for m in tilts], run_time=1.5)
            settle(self, top, add=flats + tilts)
            c.wait_until("defn")
            d1, d2 = strip.dashes[0], strip.dashes[1]
            zero1 = MathTex(r"y'' = 0", font_size=36, color=YELLOW).move_to([d1.get_x() - 0.85, -2.0, 0])
            zero2 = MathTex(r"y'' = 0", font_size=36, color=YELLOW).move_to([d2.get_x() + 0.85, -2.0, 0])
            beams = [Line(d.get_start(), d.get_end()).set_stroke(YELLOW, 6) for d in (d1, d2)]
            self.play(*[VShowPassingFlash(bm, time_width=0.6) for bm in beams],
                      *recolor([d1, d2], YELLOW), *appear(zero1, zero2, lag=0.2), run_time=1.5)

        # ---------------------------------------------------------- clip 2
        defs = VGroup(
            MathTex(r"y'' = 0 \text{ and changes sign,}", font_size=41),
            MathTex(r"\dfrac{dy}{dx} > 0:\ \text{rising point of inflection}", font_size=41),
            MathTex(r"\dfrac{dy}{dx} < 0:\ \text{falling point of inflection}", font_size=41),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_corner(DL, buff=0.55)
        with self.say("c6.nonstat.2") as c:
            c.wait_until("positive")
            self.play(*during(disappear(strip, zero1, zero2), 0, 0.45),
                      *during([top.animate.scale(0.85).to_edge(UP, buff=0.35)], 0.25, 1), run_time=1.5)
            self.play(*appear(defs[0], defs[1], lag=0.4), run_time=min(1.4, c.until("falling")))
            c.wait_until("falling")
            self.play(*appear(defs[2]), run_time=1.0)
            c.wait_until("figure")
            fall = T("falling", 30, YELLOW).move_to(fig.bend1.get_center() + np.array([-0.95, -0.5, 0]))
            rise = T("rising", 30, YELLOW).move_to(fig.bend2.get_center() + np.array([0.9, -0.45, 0]))
            c.wait_until(own_word=fall)
            self.play(*appear(fall), run_time=1.0)
            c.wait_until(own_word=rise)
            self.play(*appear(rise), run_time=1.0)
            c.wait_until("stationary")
            rtext = lf.rising[0]
            self.play(FlashAround(rtext, run_time=1.8, time_width=1.5), *recolor([rtext], YELLOW), run_time=1.8)
            c.wait_until("cubic")
            cube = _s4.build_panel("cube", (0.55, -4.75, -2.3))
            crise = T("rising", 32, YELLOW).next_to(cube.axes, LEFT, buff=0.3)
            self.play(FadeIn(cube), *appear(crise), run_time=1.2)  # early: "rising" closes this line

        # ---------------------------------------------------------- clip 3
        g = three_graphs()
        P = g.panels
        with self.say("c6.nonstat.3") as c:
            c.wait_until("three graphs")
            base = [m for p in P for m in (p.axes, p.curve, p.name, p.dot)]
            sweep_clear(self, *[FadeIn(m) for m in base], FadeIn(g.heading),  # early: the notes' board heading
                        run_time=2.0)
            c.wait_until("left")
            L = g.left
            self.play(GrowFromCenter(L.tan), *appear(*L.info, lag=0.4), run_time=1.6)
            c.wait_until(own_word=L.word)
            self.play(*appear(L.word), run_time=1.0)
            c.wait_until("middle")
            M = g.middle
            self.play(GrowFromCenter(M.tan), *appear(M.info[0]), run_time=1.4)
            c.wait_until("second derivative zero")
            self.play(*appear(M.info[1]), run_time=0.9)
            c.wait_until("third derivative six")
            self.play(*appear(M.info[2]), run_time=0.9)
            c.wait_until(own_word=M.word)
            self.play(*appear(M.word), run_time=1.0)
            c.wait_until("right")
            R = g.right
            self.play(GrowFromCenter(R.tan), *appear(*R.info, lag=0.4), run_time=1.6)
            c.wait_until(own_word=R.word)
            self.play(*appear(R.word), run_time=1.0)
            c.wait_until("six times ex")
            self.play(*appear(g.same), run_time=1.0)
            c.wait_until("concave down")
            self.play(*appear(*[p.down for p in P], lag=0.2), run_time=1.2)
            c.wait_until("concave up")
            self.play(*appear(*[p.up for p in P], lag=0.2), run_time=min(1.2, c.until()))

        # ---------------------------------------------------------- clip 4
        q = _quartic_panel()
        cx = 3.7
        q1 = MathTex(r"y'(0) = 1", font_size=42).move_to([cx, 2.4, 0])
        q2 = MathTex(r"y''(0) = 0", font_size=42).move_to([cx, 1.65, 0])
        looks = T("rising point of inflection?", 32, t2c={"?": YELLOW}).move_to([cx, 0.8, 0])
        strike = Line(looks.get_left() + 0.1 * LEFT, looks.get_right() + 0.1 * RIGHT, color=RED, stroke_width=5)
        noinf = T("no inflection", 34, RED).move_to([cx, 0.2, 0])
        never = MathTex(r"y'' = 12x^2 \geq 0", font_size=44).move_to([cx, -0.75, 0])
        rule = VGroup(T("point of inflection:", 36),
                      VGroup(MathTex(r"y''", font_size=44), T("changes sign", 36)).arrange(RIGHT, buff=0.2)
                      ).arrange(DOWN, buff=0.25).move_to([cx, -2.45, 0])
        rbox = SurroundingRectangle(rule, color=YELLOW, buff=0.3, stroke_width=4)
        with self.say("c6.nonstat.4") as c:
            c.wait_until("zero second derivative")
            sweep_clear(self, FadeIn(q.axes), FadeIn(q.curve), run_time=2.0)
            c.wait_until("quart")
            self.play(*appear(q.name), run_time=1.0)
            c.wait_until("slope is one")
            self.play(FadeIn(q.dot), GrowFromCenter(q.tan), *appear(q1), run_time=1.5)
            c.wait_until("second derivative is zero")
            self.play(*appear(q2), run_time=1.0)
            c.wait_until("looks")
            self.play(*appear(looks), run_time=1.0)
            c.wait_until("never")
            self.play(*appear(never), run_time=1.2)
            c.wait_until("cup")
            self.play(*appear(q.up_l, q.up_r, lag=0.4), run_time=1.5)
            c.wait_until("no inflection")
            self.play(Create(strike), run_time=0.8)
            self.play(*appear(noinf), run_time=1.0)
            c.wait_until("change")
            self.play(FadeIn(rbox), *appear(rule), run_time=1.5)
        self.wait(1.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
