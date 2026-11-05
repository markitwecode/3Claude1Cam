"""Chapter 5, scene 5: trial and error finds T_c >= 3.04 ns. Clips c5.trial.1 – c5.trial.4.

Shots: opens on s4's substituted equation alone (size 50 at MT_CENTER, fades in) -> equation compact across the top; table T_c | MTBF with GOLD target;
rows 2.0 / 2.5 / 3.0 ns (RED crosses), 3.04 ns (GREEN tick) -> GOLD answer box on the right,
DIM exact boundary -> GOLD "x15" arrows; tau ruler along the bottom, "x e ~ 2.7" per step,
brace "1 ns = 5 tau -> e^5 ~ 148" turns GREEN -> table + ruler shrink left and dim, answer box
goes to s6's spot (upper left, s6's answer_box()), sanity check on the right.
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


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# mtbf_example(): copied from ch5_s4_example.py (its last shot)
# =============================================================================================
MT_SIZE = 50
MT_CENTER = np.array([1.6, 0.0, 0.0])


def mtbf_example(size=MT_SIZE, center=MT_CENTER):
    x, y = r"500\times10^{-12}", r"(200\times10^{-12})}"
    num_tex = [r"T_c", r"\,e^{(", r"T_c", r"-", x, r")/", y]
    num = MathTex(*num_tex, font_size=size)
    num[0].set_color(YELLOW)
    num[2].set_color(YELLOW)
    num[4].set_color(GOLD)
    den = MathTex(r"(0.2)\,", r"150\times10^{-12}", font_size=size)
    L = MathTex(r"31.5\times10^{6}", font_size=size).set_color(GOLD)
    eq = MathTex("=", font_size=size)
    w = max(num.width, den.width) + 0.3
    bar = Line(LEFT * w / 2, RIGHT * w / 2).set_stroke(FG, 3.5)
    num.next_to(bar, UP, buff=0.16)
    den.next_to(bar, DOWN, buff=0.18)
    eq.next_to(bar, LEFT, buff=0.3)
    eq.set_y(bar.get_y())
    L.next_to(eq, LEFT, buff=0.3)
    L.shift((bar.get_y() - L[0][0].get_y()) * UP)
    F = VGroup(L, eq, num, bar, den)
    F.move_to(center)
    return F


def tc_ring(glyph, pad=0.2, width=4):
    """s4's YELLOW ring round one T_c (pad 0.12, width 3 for the one in the exponent)."""
    return Ellipse(width=glyph.width + pad, height=glyph.height + 0.8 * pad).move_to(glyph).set_stroke(YELLOW, width)


def card_row(sym, val, color=FG, size=46):
    full = MathTex(sym, "=", val, font_size=size)
    a = MathTex(sym + "=", font_size=size, color=color).move_to(VGroup(full[0], full[1]))
    b = MathTex(val, font_size=size, color=color).move_to(full[2])
    return VGroup(a, b)


def s4_values():
    """s4's dimmed compact value column, upper left (tau, t_su, T_0, N), and its dimmed year line."""
    rows = [card_row(r"\tau", r"200\,\mathrm{ps}"), card_row(r"t_{su}", r"500\,\mathrm{ps}", GOLD),
            card_row(r"T_0", r"150\,\mathrm{ps}"), card_row(r"N", r"0.2")]
    for i, r in enumerate(rows):
        r.scale(0.8)
        r.shift([-5.6, 2.6 - 0.75 * i, 0] - r[0][0][-1].get_center())
        r.set_opacity(DIMMED)
    about = MathTex(r"1\ \text{year}", r"\approx", r"31.5\times10^{6}", r"\ \mathrm{s}", font_size=50)
    about[2].set_color(GOLD)
    about.move_to([MT_CENTER[0] + 0.5, 3.1, 0]).set_opacity(DIMMED)
    return rows, about


def s4_tags():
    nc = T("This equation has no closed form solution", 34, color=RED)
    tag = T("trial and error", 34, color=GREEN)
    tbox = RoundedRectangle(corner_radius=0.15, width=tag.width + 0.5, height=tag.height + 0.4)
    tbox.set_stroke(GREEN, 2.5)
    VGroup(nc, VGroup(tbox, tag)).arrange(RIGHT, buff=0.55).move_to([0, -2.95, 0])
    tag.move_to(tbox)
    return nc, tbox, tag


# =============================================================================================
# answer_box(): s6's (ch5_s6_cascade.py) small answer box, upper left
# =============================================================================================
def answer_box():
    tex = MathTex(r"T_c \geq 3.04\text{ ns}", font_size=40, color=FG)
    box = SurroundingRectangle(tex, color=GOLD, buff=0.18, corner_radius=0.08).set_stroke(GOLD, 3)
    g = VGroup(box, tex)
    g.box, g.tex = box, tex
    g.to_corner(UL, buff=0.5)
    return g


# =============================================================================================
# the table
# =============================================================================================
TC_X = -5.3        # T_c column centre
MTBF_L = -4.1      # MTBF column left edge
MARK_X = 0.9       # crosses / tick
ROW_Y = [1.0, 0.38, -0.24, -0.86]
ROW_SIZE = 42


def row(tc, mtbf, i):
    a = MathTex(tc + r"\text{ ns}", font_size=ROW_SIZE, color=YELLOW).move_to([TC_X, ROW_Y[i], 0])
    b = MathTex(mtbf, font_size=ROW_SIZE, color=GOLD)
    b.move_to([MTBF_L, ROW_Y[i], 0], aligned_edge=LEFT)
    b.set_y(ROW_Y[i])
    return a, b


# =============================================================================================
# the ruler: T_c from 2.0 to 3.0 ns in steps of tau = 200 ps
# =============================================================================================
R_X0, R_STEP, R_Y = -5.4, 2.0, -1.8


def ruler():
    axis = Line(_p(R_X0 - 0.3, R_Y), _p(R_X0 + 5 * R_STEP + 0.4, R_Y)).set_stroke(DIM, 3)
    ticks = VGroup(*[Line(_p(R_X0 + k * R_STEP, R_Y - 0.12), _p(R_X0 + k * R_STEP, R_Y + 0.12))
                     .set_stroke(FG, 3) for k in range(6)])
    nums = VGroup(*[MathTex(f"{2 + 0.2 * k:.1f}", font_size=32, color=YELLOW)
                    .move_to(_p(R_X0 + k * R_STEP, R_Y - 0.42)) for k in (0, 5)])
    unit = T("ns", 28, color=DIM).next_to(nums[-1], RIGHT, buff=0.15)
    name = MathTex(r"T_c", font_size=40, color=YELLOW).next_to(axis, RIGHT, buff=0.2)
    steps = [MathTex(r"\times e \approx 2.7", font_size=34, color=GOLD)
             .move_to(_p(R_X0 + (k + 0.5) * R_STEP, R_Y + 0.42)) for k in range(5)]
    tau = MathTex(r"\tau = 200\text{ ps}", font_size=34, color=DIM)
    tau.move_to(_p(R_X0 + 2.5 * R_STEP, R_Y - 0.42))
    return axis, ticks, nums, unit, name, steps, tau


class Trial(NarratedScene):
    def construct(self):
        # s4's substituted equation alone, at s4's position and size
        F = mtbf_example()
        self.play(FadeIn(F), run_time=0.6)
        self.wait(0.4)

        # ---------------------------------------------------------------- c5.trial.1
        with self.say("c5.trial.1") as c:
            self.play(*during([F.animate.scale(0.68).move_to([0, 3.05, 0])], 0.2, 1.0), run_time=1.6)
            h_tc = MathTex(r"T_c", font_size=46).move_to([TC_X, 2.2, 0])
            h_mt = MathTex(r"\mathrm{MTBF}", font_size=46)
            h_mt.move_to([MTBF_L, 2.2, 0], aligned_edge=LEFT)
            h_mt.set_y(2.2)
            rule = Line(_p(-6.3, 1.88), _p(1.4, 1.88)).set_stroke(DIM, 2)
            vbar = Line(_p(-4.45, 2.5), _p(-4.45, -1.2)).set_stroke(DIM, 2)
            c.wait_until("mean time")
            self.play(*appear(h_tc, h_mt, shift=None), GrowFromCenter(rule), FadeIn(vbar), run_time=1.0)
            target = T("target: 1 year ≈ 365 days", 32, color=GOLD)
            target.move_to([MTBF_L, 1.58, 0], aligned_edge=LEFT)
            c.wait_until("with a year")
            self.play(*appear(target), run_time=1.0)

            rows = [row("2.0", r"1.4\text{ days}", 0), row("2.5", r"21\text{ days}", 1),
                    row("3.0", r"311\text{ days}", 2),
                    row("3.04", r"384\text{ days} \approx 1.05\text{ years}", 3)]
            marks = [cross_mark().move_to([MARK_X, ROW_Y[i], 0]) for i in range(3)]
            tick = check_mark().move_to([MARK_X, ROW_Y[3], 0])

            c.wait_until("two")
            self.play(*appear(rows[0][0]), run_time=1.0)
            c.wait_until("that gives")
            self.play(*appear(rows[0][1]), run_time=1.0)
            c.wait_until("far too short")
            self.play(Create(marks[0]), run_time=0.8)

            c.wait_until("twofive")
            self.play(*appear(rows[1][0]), run_time=0.9)
            c.wait_until("gives about", nth=1)
            self.play(*appear(rows[1][1]), run_time=0.9)
            c.wait_until("still short")
            self.play(Create(marks[1]), run_time=0.7)

            c.wait_until("three")
            self.play(*appear(rows[2][0]), run_time=0.9)
            c.wait_until("gives about", nth=2)
            self.play(*appear(rows[2][1]), run_time=0.9)
            short = T("just short", 30, color=RED).next_to(marks[2], RIGHT, buff=0.3)
            c.wait_until(own_word=short)
            self.play(Create(marks[2]), *appear(short), run_time=0.9)

        # ---------------------------------------------------------------- c5.trial.2
        with self.say("c5.trial.2") as c:
            self.play(*appear(rows[3][0]), run_time=1.0)
            c.wait_until("gives about")
            self.play(*appear(rows[3][1]), run_time=1.2)
            c.wait_until("just over")
            self.play(Create(tick), run_time=0.8)

            a1 = MathTex(r"T_c \geq 3.04\text{ ns}", font_size=44, color=FG)
            a2 = MathTex(r"f_c \leq 329\text{ MHz}", font_size=44, color=FG)
            VGroup(a1, a2).arrange(DOWN, buff=0.35).move_to([4.9, 1.0, 0])
            abox = SurroundingRectangle(VGroup(a1, a2), color=GOLD, buff=0.3, corner_radius=0.1)
            abox.set_stroke(GOLD, 3)
            c.wait_until("slide")
            self.play(FadeIn(abox), *appear(a1, shift=None), run_time=1.2)
            c.wait_until("frequency")
            self.play(*appear(a2), run_time=1.0)
            exact = T("exact boundary:\n3.03 ns", 30, color=DIM).next_to(abox, DOWN, buff=0.3)
            c.wait_until("exact")
            self.play(*appear(exact), run_time=1.0)

        # ---------------------------------------------------------------- c5.trial.3
        with self.say("c5.trial.3") as c:
            gx = -1.6
            arrows, gl = [], []
            for i in range(2):
                s = _p(gx, ROW_Y[i] + 0.02)
                e = _p(gx, ROW_Y[i + 1] - 0.02)
                arr = CurvedArrow(s, e, angle=-PI / 1.6, color=GOLD, tip_length=0.18)
                arr.set_stroke(GOLD, 3).set_fill(opacity=0)
                arr.tip.set_fill(GOLD, 1)
                arrows.append(arr)
                gl.append(T("×15", 30, color=GOLD).next_to(arr, RIGHT, buff=0.12))
            self.play(Create(arrows[0]), *appear(gl[0]), run_time=1.0)
            self.play(Create(arrows[1]), *appear(gl[1]), run_time=0.8)

            axis, ticks, nums, unit, name, steps, tau = ruler()
            c.wait_until("pertau")
            self.play(Create(axis), *appear(ticks, nums, unit, name, shift=None, lag=0.15),
                      run_time=1.5)
            c.wait_until("each extra tau")
            # the first step's tau label replaces the 2.0 / 2.2 gap
            self.play(*appear(steps[0], tau), run_time=1.4)
            c.wait_until("multiplies")
            self.play(*appear(*steps[1:], lag=0.3), run_time=2.0)

            c.wait_until("perns")
            brace = span_brace(_p(R_X0, R_Y - 0.65), _p(R_X0 + 5 * R_STEP, R_Y - 0.65), DOWN, color=DIM,
                               buff=0.05)
            blab = MathTex(r"1\text{ ns} = 5\tau \;\rightarrow\; e^{5} \approx 148", font_size=38, color=GOLD)
            blab.next_to(brace, DOWN, buff=0.12)
            self.play(GrowFromCenter(brace), *appear(blab), run_time=1.5)
            c.wait_until("cheap")
            self.play(brace.animate.set_color(GREEN), FlashAround(blab, color=GREEN, time_width=1.5),
                      run_time=1.8)

        # ---------------------------------------------------------------- c5.trial.4
        with self.say("c5.trial.4") as c:
            A = answer_box()
            left = VGroup(h_tc, h_mt, rule, vbar, *[m for r in rows for m in r], *marks, tick)
            left.generate_target()
            left.target.scale(0.75).to_edge(LEFT, buff=0.5).set_y(0.0)
            left.target.set_opacity(0.4)
            self.play(*during(disappear(F, a2, abox, exact, target, short, *arrows, *gl, axis, ticks, nums,
                                        unit, name, *steps, tau, brace, blab), 0, 0.45),
                      *during([a1.animate.scale(40 / 44).move_to(A.tex), MoveToTarget(left)], 0.2, 0.85),
                      *during([FadeIn(A.box)], 0.75, 1.0), run_time=min(2.0, c.until("pfail")))

            CX = 2.6
            l1a = MathTex(r"P_{\mathrm{fail}}\text{ at }3.04\text{ ns}", r"\approx", r"1.5\times10^{-7}",
                          font_size=46)
            l1a[2].set_color(GOLD)
            l1b = MathTex(r"\approx 1\text{ in }6.6\text{ million}", font_size=46, color=GOLD)
            l2a = MathTex(r"0.2\text{ per second}", r"\times", r"31.5\times10^{6}\text{ s}", font_size=46)
            l2b = MathTex(r"\approx 6.3\text{ million changes per year}", font_size=46, color=GOLD)
            l3 = MathTex(r"\rightarrow\ \text{just under 1 failure per year}", font_size=44)
            g1 = VGroup(l1a, l1b).arrange(DOWN, buff=0.22)
            g2 = VGroup(l2a, l2b).arrange(DOWN, buff=0.22)
            VGroup(g1, g2, l3).arrange(DOWN, buff=0.7).move_to([CX, 0.0, 0])
            ok = check_mark().next_to(l3, RIGHT, buff=0.25)

            c.wait_until("pfail")
            self.play(*appear(l1a), run_time=1.2)
            c.wait_until("one in six")
            self.play(*appear(l1b), run_time=1.0)
            c.wait_until("changes")
            self.play(*appear(l2a), run_time=1.2)
            c.wait_until("six point three")
            self.play(*appear(l2b), run_time=1.0)
            c.wait_until("once")
            self.play(*appear(l3), run_time=1.2)
            c.wait_until("exactly")
            self.play(Create(ok), run_time=0.8)

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
