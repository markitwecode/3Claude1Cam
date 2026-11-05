"""Chapter 3, scene 2: differentiate both sides of g(y) = h(x). Clips c3.implicit.1 – c3.implicit.4.

Equations are MathTex built from parts; a line becomes the next line by moving the parts both share
(same tex, same size, so they land exactly) and fading the rest out/in (regroup), never a morph.
The condition line `\\dfrac{dg}{dy} \\neq 0` is MathTex(r"\\dfrac{dg}{dy}", r"\\neq 0"), size 52, FG with
the `\\neq 0` YELLOW (scene 3 recalls it).
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

SZ = 60          # hero equations
DDX = r"\dfrac{d}{dx}"
DYDX = r"\dfrac{dy}{dx}"
DGDY = r"\dfrac{dg}{dy}"
DHDX = r"\dfrac{dh}{dx}"
GL, GR = r"g\big(", r"\big)"


def mt(parts, size=SZ, colors=None):
    m = MathTex(*parts, font_size=size, color=FG)
    for i, col in (colors or {}).items():
        m[i].set_color(col)
    return m


def frac_parts(m):
    """(top glyphs left to right, bar, bottom glyphs left to right) of a one-fraction part."""
    g = list(m.submobjects)
    bar = max(g, key=lambda s: s.width / max(s.height, 1e-3))
    cy = bar.get_center()[1]
    top = sorted([s for s in g if s is not bar and s.get_center()[1] > cy], key=lambda s: s.get_x())
    bot = sorted([s for s in g if s is not bar and s.get_center()[1] < cy], key=lambda s: s.get_x())
    return top, bar, bot


def regroup(old, new, pairs, out_extra=(), in_extra=()):
    """old line -> new line: parts in pairs {old_i: new_j} (same tex) slide; the rest leave / arrive."""
    anims = [old[i].animate.move_to(new[j]).set_color(new[j].get_color()) for i, j in pairs.items()]
    leave = [FadeOut(old[i], shift=0.2 * UP) for i in range(len(old)) if i not in pairs]
    leave += [FadeOut(m, shift=0.2 * UP) for m in out_extra]
    got = set(pairs.values())
    arrive = [FadeIn(new[j], shift=0.2 * UP) for j in range(len(new)) if j not in got]
    arrive += [FadeIn(m, shift=0.2 * UP) for m in in_extra]
    res = []
    if leave:
        res += during(leave, 0, 0.4)
    if anims:
        res += during(anims, 0.1, 0.6)
    if arrive:
        res += during(arrive, 0.6, 1)
    return res


def g_of(y):
    return y ** 3 - 3 * y


class Implicit(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def finish(self, old, new):
        """After a regroup play: drop every piece of old, put new on screen whole."""
        self.remove(*old.get_family())
        self.add(new)

    # ------------------------------------------------------------------ g(y) = h(x)
    def clip1(self):
        expl = mt(["y = f(x)"], 44).to_corner(UL, buff=0.6)
        g0 = mt([GL, "y", GR, "=", "h(x)"], 72).move_to(1.6 * UP)
        tag = T("(108)", 30, DIM).next_to(g0, RIGHT, buff=0.9)
        b1 = Brace(g0[0:3], DOWN, buff=0.15, color=DIM)
        b2 = Brace(g0[4], DOWN, buff=0.15, color=DIM)
        l1 = VGroup(T("a function of", 30), MathTex("y", font_size=38)).arrange(RIGHT, buff=0.12)
        l2 = VGroup(T("a function of", 30), MathTex("x", font_size=38)).arrange(RIGHT, buff=0.12)
        l1.next_to(b1, DOWN, buff=0.15).shift(0.4 * LEFT)
        l2.next_to(b2, DOWN, buff=0.15).shift(0.4 * RIGHT)
        arrow = Arrow(0.15 * DOWN, 1.05 * DOWN, buff=0, color=FG, stroke_width=4)
        inv = mt([r"y = g^{-1}\big(h(x)\big)"], 56).move_to(1.75 * DOWN)
        nope = T("not always possible", 36, RED).next_to(inv, DOWN, buff=0.45)
        self.g0, self.c1 = g0, VGroup(expl, tag, b1, b2, l1, l2, arrow, inv, nope)

        with self.say("c3.implicit.1") as c:
            self.play(*appear(expl), run_time=1.0)
            c.wait_until("implicit")
            self.play(*set_alpha([expl], 0.35), *appear(g0), run_time=1.3)
            self.play(*appear(tag, shift=None), run_time=0.8)
            c.wait_until("function of why")
            self.play(GrowFromCenter(b1), *appear(l1), run_time=1.0)
            c.wait_until("function of ex")
            self.play(GrowFromCenter(b2), *appear(l2), run_time=1.0)
            c.wait_until("invert")
            self.play(GrowArrow(arrow), *during(appear(inv), 0.3, 1), run_time=1.6)
            c.wait_until("but")
            self.play(*set_alpha([inv, arrow], 0.35), *appear(nope), run_time=1.0)

    # ------------------------------------------------------------------ differentiate both sides
    def clip2(self):
        g0 = self.g0
        g1 = mt([DDX, GL, "y", GR, "=", DDX, "h(x)"]).move_to(1.0 * UP)
        g2 = mt([DDX, GL, "y(x)", GR, "=", DDX, "h(x)"], colors={2: YELLOW}).move_to(1.0 * UP)
        g3 = mt([DDX, GL, "y(x)", GR, "=", DHDX], colors={2: YELLOW}).move_to(1.0 * UP)
        rowa = g3.copy().move_to(2.0 * UP)
        bl = mt([DDX, GL, "y(x)", GR], colors={2: YELLOW})
        br = mt(["=", DGDY, r"\,\dfrac{dy}{dx}"], colors={2: GREEN})
        row_b = VGroup(bl, br).arrange(RIGHT, buff=0.22)
        row_b.move_to(0.5 * DOWN).align_to(rowa, LEFT)   # left side sits under row A's left side
        self.rowa, self.bl, self.br = g3, bl, br

        with self.say("c3.implicit.2") as c:
            self.play(*regroup(g0, g1, {0: 1, 1: 2, 2: 3, 3: 4, 4: 6}, out_extra=list(self.c1)),
                      run_time=1.6)
            self.finish(g0, g1)
            c.wait_until("remember")
            self.play(*regroup(g1, g2, {0: 0, 1: 1, 3: 3, 4: 4, 5: 5, 6: 6}), run_time=1.6)
            self.finish(g1, g2)
            c.wait_until("right")
            self.play(*regroup(g2, g3, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}), run_time=1.6)
            self.finish(g2, g3)
            c.wait_until("left")
            self.play(FlashAround(VGroup(*g3[0:4]).copy(), time_width=1.5, run_time=1.8))
            c.wait_until("chain rule")
            ghost = VGroup(*[m.copy() for m in g3[0:4]])
            self.add(ghost)
            self.play(g3.animate.move_to(rowa), ghost.animate.move_to(bl), run_time=1.6)
            self.remove(ghost)
            self.add(bl)
            c.wait_until("chain")
            self.play(*appear(br[0], br[1], lag=0.3), run_time=1.2)
            c.wait_until("times the derivative")
            self.play(*appear(br[2]), run_time=1.0)

    # ------------------------------------------------------------------ rearrange: (109), (110)
    def clip3(self):
        rowa, bl, br = self.rowa, self.bl, self.br
        e109 = mt([DGDY, r"\,\dfrac{dy}{dx}", "=", DHDX], colors={1: GREEN}).move_to(2.45 * UP)
        t109 = T("(109)", 30, DIM).next_to(e109, RIGHT, buff=0.7)
        e110 = mt([DYDX, "=", DHDX, r"\bigg/", DGDY], 64, colors={0: GREEN}).move_to(0.15 * DOWN)
        box = SurroundingRectangle(e110, color=YELLOW, buff=0.3, stroke_width=4)
        t110 = T("(110)", 30, DIM).next_to(box, RIGHT, buff=0.4)
        cond = mt([DGDY, r"\neq 0"], 52, colors={1: YELLOW}).next_to(box, DOWN, buff=0.45)

        ax = Axes(x_range=[0, 2.4, 1], y_range=[-2.5, 3.2, 1], x_length=4.2, y_length=4.6, tips=True,
                  axis_config={"color": DIM, "include_ticks": False, "stroke_width": 3})
        ax.move_to([3.9, 0.0, 0])
        xl = MathTex("y", font_size=36, color=DIM).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
        yl = MathTex("g", font_size=36, color=BLUE).next_to(ax.y_axis.get_end(), RIGHT, buff=0.15)
        curve = ax.plot(g_of, x_range=[0.15, 2.1], color=BLUE, stroke_width=5)
        gl = Line(ax.c2p(0, 2), ax.c2p(2.4, 2), color=GREEN, stroke_width=3)
        gd = Dot(ax.c2p(2, 2), radius=0.1, color=GREEN)
        rl = Line(ax.c2p(0, -1.7), ax.c2p(2.4, -1.7), color=RED, stroke_width=3)
        rd = [Dot(ax.c2p(r, -1.7), radius=0.1, color=RED) for r in (0.6645, 1.3014)]

        with self.say("c3.implicit.3", gap=1.4) as c:
            # settle as (109): row B's right side and row A's dh/dx slide into one line
            moves = [br[1].animate.move_to(e109[0]), br[2].animate.move_to(e109[1]),
                     rowa[5].animate.move_to(e109[3])]
            leave = [FadeOut(m, shift=0.2 * UP) for m in [*rowa[0:5], *bl, br[0]]]
            self.play(*during(leave, 0, 0.4), *during(moves, 0.25, 0.85),
                      *during([FadeIn(e109[2], shift=0.2 * UP)], 0.7, 1), run_time=1.8)
            self.remove(*rowa.get_family(), *bl.get_family(), *br.get_family())
            self.add(e109)
            self.play(*appear(t109, shift=None), run_time=0.8)

            c.wait_until("eq110")
            self.play(*self.copy_to(e109[1], e110[0]), *during(appear(e110[1], shift=None), 0.6, 1),
                      run_time=1.5)
            c.wait_until("derivative of the right-hand side")
            self.play(*self.copy_to(e109[3], e110[2]), run_time=1.3)
            c.wait_until("divided by")
            self.play(*self.copy_to(e109[0], e110[4]), *during(appear(e110[3], shift=None), 0.6, 1),
                      run_time=1.3)
            settle(self, e110)
            c.wait_until("That's equation")
            self.play(FadeIn(box), *appear(t110, shift=None), run_time=1.0)
            c.wait_until("cond")
            self.play(*appear(cond), FlashAround(e110[4], time_width=1.5, run_time=2.0), run_time=2.0)

            c.wait_until("inverse")
            left = 3.3 * LEFT
            col = [e109, t109, e110, box, t110, cond]
            self.play(*[m.animate.shift(left) for m in col],
                      *during([FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(curve)], 0.4, 1), run_time=1.6)
            self.play(Create(gl), FadeIn(gd, scale=0.5), run_time=0.9)
            self.play(Create(rl), *[FadeIn(d, scale=0.5) for d in rd], run_time=0.9)
            c.wait_until("consistent")
            self.play(FlashAround(gd, color=GREEN, time_width=1.5), FlashAround(cond[1], time_width=1.5),
                      gd.animate.scale(1.4), run_time=1.4)

    def copy_to(self, src, dst):
        """A copy of src slides onto dst (same glyphs); dst takes over when it lands."""
        ghost = src.copy()
        self.add(ghost)
        return [ghost.animate.move_to(dst).set_color(dst.get_color()),
                during([FadeIn(dst)], 0.95, 1)[0], during([FadeOut(ghost)], 0.95, 1)[0]]

    # ------------------------------------------------------------------ example: y = ln ax
    def clip4(self):
        l1 = mt([r"y = \ln ax"], 54)
        l2 = mt([r"\Rightarrow", "e^{y}", "= ax"], 54, colors={1: GOLD})
        l3 = mt([r"\Rightarrow", DDX, "e^{y}", "=", "e^{y}", DYDX, "=", r"\dfrac{d}{dx}(ax)", "=", "a"], 54,
                colors={2: GOLD, 4: GOLD, 5: GREEN})
        l4 = mt([r"\Rightarrow", DYDX, "=", r"\dfrac{a}{e^{y}}", "=", r"\dfrac{a}{ax}", "=", r"\dfrac{1}{x}"],
                54, colors={1: GREEN})
        for s in frac_parts(l4[3])[2]:
            s.set_color(GOLD)
        chain = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        l1.shift((l2[1].get_left()[0] - l1.get_left()[0]) * RIGHT)
        chain.move_to(0.2 * DOWN)
        head = T("Example", 40, DIM).to_corner(UL, buff=0.6)
        alab = T("a: a constant", 30, DIM, t2s={"a:": ITALIC}).next_to(l1, RIGHT, buff=0.8)
        (na,), _, (da, _x) = frac_parts(l4[5])
        strikes = [Line(m.get_corner(DL) + 0.06 * (DL), m.get_corner(UR) + 0.06 * UR, color=YELLOW,
                        stroke_width=5) for m in (na, da)]
        box = SurroundingRectangle(VGroup(*l4[1:]), color=YELLOW, buff=0.22, stroke_width=4)
        promise = T("part two's promise", 30, YELLOW).next_to(box, RIGHT, buff=0.35)

        with self.say("c3.implicit.4") as c:
            sweep_clear(self, time_span(FadeIn(head), 0.6, 1.2))
            c.wait_until("lnx")
            self.play(*appear(l1), run_time=1.0)
            c.wait_until("constant")
            self.play(*appear(alab, shift=None), run_time=0.9)
            c.wait_until("exp")
            self.play(*appear(*l2, lag=0.2), run_time=1.3)
            c.wait_until("lhs")
            self.play(*appear(l3[0], l3[1], l3[2], lag=0.2), run_time=1.2)
            c.wait_until("chain rule gives")
            self.play(*appear(l3[3], l3[4], l3[5], lag=0.3), run_time=1.4)
            c.wait_until("rhs")
            self.play(*appear(l3[6], l3[7], l3[8], l3[9], lag=0.3), run_time=1.6)
            c.wait_until("result")
            self.play(*appear(l4[0], l4[1], l4[2], l4[3], lag=0.3), run_time=1.6)
            c.wait_until("that is")
            self.play(*appear(l4[4], l4[5], lag=0.3), run_time=1.2)
            c.wait_until("cancel")
            self.play(*[Create(s) for s in strikes], run_time=1.0)
            c.wait_until("one over")
            self.play(*appear(l4[6], l4[7], lag=0.3), run_time=1.1)
            self.play(FadeIn(box), *appear(promise, shift=None), run_time=1.0)
        self.wait(2.6)
