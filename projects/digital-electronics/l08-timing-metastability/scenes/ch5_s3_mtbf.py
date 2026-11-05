"""Chapter 5, scene 3: from failures per second to seconds per failure, MTBF. Clips c5.mtbf.1 – c5.mtbf.4.

Shots: s2's end shot (P_fail/s = N P_fail at 84, "failures per second", YELLOW loop arrow) ->
the label's nouns swap round "per": "seconds per failure"; YELLOW "mean time between failures
(MTBF)" above -> MTBF = 1/(P_fail/s), a time axis with a RED cross every 100 s, "0.01 failures per
second <-> MTBF = 100 s" -> s2's formula small at the top; its N P_fail flies into the denominator;
ch4's P_fail line below, its right side flies in -> T_0/T_c turns over, the minus glows RED and goes,
the exponential climbs into the numerator -> result centred: MTBF = 1/(P_fail/s) = T_c e^((T_c -
t_su)/tau) / (N T_0) (right part = s4's mtbf_formula() tex and colours, at size 60) -> brace + t_res,
ch4's small bar -> formula up, axes T_c / MTBF, GOLD exponential, YELLOW dot; DIM half-height copy.
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


# ---- ch5_s2_rate.py tex(), copied: N and P_fail GOLD ----
GOLDS = ("N", r"P_{\text{fail}}")


def tex(s, size=40, color=FG):
    import re
    pieces = [x for x in re.split(r"(N|P_\{\\text\{fail\}\})", s) if x]
    m = MathTex(*pieces, font_size=size, color=color)
    for part in m.submobjects:
        if getattr(part, "tex_string", "") in GOLDS:
            part.set_color(GOLD)
    return m


# ---- glyph helpers ----
def glyphs(m):
    out = []
    for part in m.submobjects:
        out.extend(part.submobjects)
    return out


def at_glyph(piece, full, i, j=0):
    """Shift `piece` so its glyph j sits exactly on glyph i of `full` (same font size)."""
    piece.shift(glyphs(full)[i].get_center() - glyphs(piece)[j].get_center())
    return piece


def paint(m, idx, color):
    g = glyphs(m)
    for i in idx:
        g[i].set_color(color)
    return m


SIZE = 72
EXP_NEG = r"e^{-(T_c - t_{su})/\tau}"         # e - ( T c - t s u ) / tau
RHS3 = r"\frac{T_0}{T_c}\," + EXP_NEG          # T 0 bar T c | e ...


def m_pfs(size=SIZE):
    return paint(MathTex(r"P_{\text{fail}}/\text{s}", font_size=size), range(5), GOLD)


def m_exp_neg(size=SIZE):
    return paint(paint(MathTex(EXP_NEG, font_size=size), (3, 4), YELLOW), (6, 7, 8), GOLD)


def m_rhs3(size=SIZE):
    m = MathTex(RHS3, font_size=size)
    return paint(paint(m, (3, 4, 8, 9), YELLOW), (11, 12, 13), GOLD)


# ---- s4's mtbf_formula() numerator / denominator (ch5_s4_example.py mtbf_state, same tex) ----
NUM_TEX = [r"T_c", r"\,e^{(", r"T_c", r"-", r"t_{su}", r")/", r"\tau}"]


def mtbf_num(size=SIZE):
    num = MathTex(*NUM_TEX, font_size=size)
    num[0].set_color(YELLOW)
    num[2].set_color(YELLOW)
    num[4].set_color(GOLD)
    return num


def mtbf_den(size=SIZE):
    return MathTex(r"N\,", r"T_0", font_size=size)


def frac_layout(L, eq, num, den, center):
    """mtbf_state's layout: bar = wider of num/den + 0.3; returns the bar Line."""
    w = max(num.width, den.width) + 0.3
    bar = Line(LEFT * w / 2, RIGHT * w / 2).set_stroke(FG, 3.5)
    num.next_to(bar, UP, buff=0.16)
    den.next_to(bar, DOWN, buff=0.18)
    eq.next_to(bar, LEFT, buff=0.3)
    eq.set_y(bar.get_y())
    L.next_to(eq, LEFT, buff=0.3)
    L.shift((bar.get_y() - L[0][0].get_y()) * UP)
    VGroup(L, eq, num, bar, den).move_to(center)
    return bar


def result_layout(L, eq1, one, mden, eq2, num, den, center):
    w2 = max(num.width, den.width) + 0.3
    bar2 = Line(LEFT * w2 / 2, RIGHT * w2 / 2).set_stroke(FG, 3.5)
    num.next_to(bar2, UP, buff=0.16)
    den.next_to(bar2, DOWN, buff=0.18)
    eq2.next_to(bar2, LEFT, buff=0.3).set_y(bar2.get_y())
    w1 = max(one.width, mden.width) + 0.3
    bar1 = Line(LEFT * w1 / 2, RIGHT * w1 / 2).set_stroke(FG, 3.5)
    bar1.next_to(eq2, LEFT, buff=0.3).set_y(bar2.get_y())
    one.next_to(bar1, UP, buff=0.16)
    mden.next_to(bar1, DOWN, buff=0.18)
    eq1.next_to(bar1, LEFT, buff=0.3).set_y(bar2.get_y())
    L.next_to(eq1, LEFT, buff=0.3)
    L.shift((bar2.get_y() - L[0][0].get_y()) * UP)
    VGroup(L, eq1, one, bar1, mden, eq2, num, bar2, den).move_to(center)
    return bar1, bar2


def put_bar(bar, new):
    return bar.animate.put_start_and_end_on(new.get_start(), new.get_end())


# ---- ch4_s6_fail.py res_bar() look (budget_bar: t_res FG + t_su GOLD, YELLOW outline), small,
# with ch4's YELLOW T_c dimension arrow over both ----
BAR_H, BAR_FILL, BAR_OUT_W, DIM_W = 0.5, 0.85, 3, 3


def small_res_bar(total=3.2, su=0.6):
    g = VGroup()
    r1 = Rectangle(width=total - su, height=BAR_H).set_stroke(width=0).set_fill(FG, BAR_FILL)
    r2 = Rectangle(width=su, height=BAR_H).set_stroke(width=0).set_fill(GOLD, BAR_FILL)
    r1.move_to(_p((total - su) / 2, 0))
    r2.move_to(_p(total - su / 2, 0))
    out = Rectangle(width=total, height=BAR_H).set_stroke(YELLOW, BAR_OUT_W).set_fill(opacity=0)
    out.move_to(_p(total / 2, 0)).set_z_index(1)
    s1 = MathTex("t_{res}", font_size=36, color=FG).next_to(r1, UP, buff=0.15)
    s2 = MathTex("t_{su}", font_size=36, color=GOLD).next_to(r2, UP, buff=0.15)
    s2.align_to(s1, DOWN)
    y = -(BAR_H / 2 + 0.3)
    arr = DoubleArrow(_p(0, y), _p(total, y), buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=YELLOW)
    tc = MathTex("T_c", font_size=40, color=YELLOW).next_to(arr, DOWN, buff=0.12)
    g.add(r1, r2, out, s1, s2, arr, tc)
    return g


def f_curve(x):
    return 0.02 * np.exp(0.62 * x)


class Mtbf(NarratedScene):
    def construct(self):
        # ------------------------------------------------ s2's last shot (same build, same place)
        formula = tex(r"P_{\text{fail}}/\text{s} = N\,P_{\text{fail}}", 84).move_to(_p(0, 0.5))
        rate_full = T("failures per second", 44).next_to(formula, DOWN, buff=0.7)
        rg = rate_full.submobjects
        w_fail = T("failures", 44)
        w_per = T("per", 44)
        w_sec = T("second", 44)
        for w, a, b in ((w_fail, 0, 8), (w_per, 8, 11), (w_sec, 11, 17)):
            w.move_to(VGroup(*rg[a:b]).get_center())
        a0 = rate_full.get_right() + _p(0.45, -0.05)
        a1 = rate_full.get_left() + _p(-0.45, -0.05)
        loop = CurvedArrow(a0, a1, angle=-PI * 0.55, color=YELLOW).set_stroke(width=5)
        self.play(FadeIn(formula), FadeIn(w_fail), FadeIn(w_per), FadeIn(w_sec), FadeIn(loop),
                  run_time=0.6)

        # ---------------------------------------------------------------- c5.mtbf.1
        with self.say("c5.mtbf.1") as c:
            tgt_full = T("seconds per failure", 44).move_to(rate_full)
            tg = tgt_full.submobjects
            n_secs = T("seconds", 44).move_to(VGroup(*tg[0:7]).get_center())
            n_per = T("per", 44).move_to(VGroup(*tg[7:10]).get_center())
            n_fail = T("failure", 44).move_to(VGroup(*tg[10:17]).get_center())
            self.play(*during([FadeOut(loop), formula.animate.shift(0.7 * UP)], 0, 0.4),
                      *during([w_fail.animate(path_arc=-2.0).align_to(n_fail, LEFT),
                               w_sec.animate(path_arc=-2.0).align_to(n_secs, LEFT),
                               w_per.animate.move_to(n_per)], 0.3, 1),
                      run_time=min(2.0, c.until("we measure")))
            c.wait_until("we measure")
            self.remove(w_per)
            self.add(n_per)
            self.play(*edit(w_fail, n_fail), *edit(w_sec, n_secs), run_time=min(1.2, c.until("name")))
            label = VGroup(n_secs, n_per, n_fail)

            name = T("mean time between failures (MTBF)", 46, YELLOW).move_to(_p(0, 2.85))
            c.wait_until("measured")
            self.play(*during(disappear(formula), 0, 0.4),
                      *during([m.animate.shift((2.1 - label.get_y()) * UP) for m in label], 0.3, 1),
                      run_time=1.4)
            c.wait_until(own_word=name)
            self.play(*appear(name), run_time=1.2)

            # MTBF = 1 / (P_fail/s)
            L = MathTex(r"\mathrm{MTBF}", font_size=SIZE)
            eq = MathTex("=", font_size=SIZE)
            one = MathTex("1", font_size=SIZE)
            den1 = m_pfs()
            bar = frac_layout(L, eq, one, den1, _p(0, -0.15))
            c.wait_until("reciprocal")
            self.play(*appear(L, eq, one, bar, den1, lag=0.12, shift=None), run_time=1.4)
            c.wait_until("probability of failure")
            self.play(FlashAround(den1, run_time=1.5, time_width=1.5), run_time=1.5)

            # the example: a failure every 100 s
            AX_Y, X0, X1 = -2.25, -5.5, 5.5
            ax = Line(_p(X0 - 0.3, AX_Y), _p(X1 + 0.3, AX_Y)).set_stroke(DIM, 3)

            def axx(s):
                return X0 + (X1 - X0) * s / 500

            ticks = VGroup(*[Line(_p(axx(s), AX_Y - 0.1), _p(axx(s), AX_Y + 0.1)).set_stroke(DIM, 3)
                             for s in range(0, 501, 100)])
            tlabs = [T(f"{s} s", 28, DIM).next_to(_p(axx(s), AX_Y - 0.1), DOWN, buff=0.12)
                     for s in range(0, 501, 100)]
            crosses = [cross_mark(RED).scale(0.8).move_to(_p(axx(s), AX_Y + 0.42)) for s in range(100, 501, 100)]
            c.wait_until("For example")
            self.play(Create(ax), *appear(ticks, *tlabs, lag=0.05, shift=None), run_time=1.0)
            c.wait_until("once")
            self.play(*appear(*crosses, lag=0.35, shift=0.2 * DOWN), run_time=min(2.0, c.until("on average")))
            stmt = MathTex(r"0.01", r"\ \text{failures per second}\ \ \leftrightarrow\ \ \mathrm{MTBF} = ",
                           r"100\ \text{s}", font_size=40)
            stmt[0].set_color(GOLD)
            stmt[2].set_color(GOLD)
            stmt.move_to(_p(0, -3.4))
            c.wait_until("on average")
            self.play(*appear(stmt, shift=None), run_time=1.0)

        # ---------------------------------------------------------------- c5.mtbf.2
        with self.say("c5.mtbf.2") as c:
            top = tex(r"P_{\text{fail}}/\text{s} = N\,P_{\text{fail}}", 54).move_to(_p(0, 3.15))
            top_l = paint(MathTex(r"P_{\text{fail}}/\text{s}", font_size=54), range(5), GOLD)
            top_eq = MathTex("=", font_size=54)
            top_r = paint(MathTex(r"N\,P_{\text{fail}}", font_size=54), range(6), GOLD)
            at_glyph(top_l, top, 0)
            at_glyph(top_eq, top, 7)
            at_glyph(top_r, top, 8)
            CEN = _p(0, 0.2)
            for m in (L, eq, one):
                m.generate_target()
            den2 = paint(MathTex(r"N\,P_{\text{fail}}", font_size=SIZE), range(1, 6), GOLD)
            bar2 = frac_layout(L.target, eq.target, one.target, den2, CEN)
            den1.generate_target()
            den1.target.next_to(bar2, DOWN, buff=0.18)
            sweep_clear(self, *appear(top_l, top_eq, top_r, shift=None),
                        *[MoveToTarget(m) for m in (L, eq, one, den1)], put_bar(bar, bar2),
                        keep=[L, eq, one, bar, den1], run_time=min(1.8, c.until("number of")))

            top_r2 = top_r.copy()
            c.wait_until("N times")
            self.play(*during(disappear(den1), 0, 0.4),
                      *during([top_r.animate(path_arc=-PI).become(den2)], 0.3, 1),
                      *during([FadeIn(top_r2)], 0.75, 1),
                      run_time=min(1.8, c.until("pfail")))
            self.remove(top_r)
            self.add(den2)
            dN = at_glyph(MathTex("N", font_size=SIZE), den2, 0)
            dPf = paint(at_glyph(MathTex(r"P_{\text{fail}}", font_size=SIZE), den2, 1), range(5), GOLD)
            self.remove(den2)
            self.add(dN, dPf)

            # ch4's P_fail, below
            pf_l = paint(MathTex(r"P_{\text{fail}} =", font_size=56), range(5), GOLD)
            pf_r = m_rhs3(56)
            pf_r.next_to(pf_l, RIGHT, buff=0.25)
            pf_r.shift((glyphs(pf_l)[5].get_y() - glyphs(pf_r)[2].get_y()) * UP)
            VGroup(pf_l, pf_r).move_to(_p(0, -2.5))
            c.wait_until("pfail")
            self.play(FlashAround(dPf, run_time=1.2, time_width=1.5), *appear(pf_l, pf_r, lag=0.3, shift=None),
                      run_time=1.4)

            full3 = MathTex(r"N\," + RHS3, font_size=SIZE)
            rhs3 = m_rhs3()
            dN.generate_target()
            at_glyph(rhs3, full3, 1)
            at_glyph(dN.target, full3, 0)
            for m in (L, eq, one):
                m.generate_target()
            bar3 = frac_layout(L.target, eq.target, one.target, VGroup(dN.target, rhs3), CEN)
            c.wait_until("times an exponential")
            self.play(*during(disappear(dPf), 0, 0.5),
                      *during([MoveToTarget(m) for m in (L, eq, one, dN)] + [put_bar(bar, bar3)], 0.3, 1),
                      run_time=1.0)
            self.play(pf_r.animate.become(rhs3), *during(disappear(pf_l), 0.55, 1), run_time=1.6)
            self.remove(pf_r)
            self.add(rhs3)
            # explode rhs3 into its pieces (no visible change)
            dT0 = at_glyph(MathTex("T_0", font_size=SIZE), rhs3, 0)
            dfbar = glyphs(rhs3)[2].copy()
            dTc = at_glyph(MathTex("T_c", font_size=SIZE, color=YELLOW), rhs3, 3)
            dexp = at_glyph(m_exp_neg(), rhs3, 5)
            self.remove(rhs3)
            self.add(dT0, dfbar, dTc, dexp)

            c.wait_until("two things")
            self.play(FlashAround(VGroup(dT0, dfbar, dTc), run_time=1.2, time_width=1.5), run_time=1.2)

            # T_0/T_c turns over within {over}: spread, swap round each other, go to their places
            c.wait_until("over")
            k = min(1.0, max(0.6, (c.until("sign") - 0.3) / 3.1))
            self.play(*disappear(one, dfbar), dN.animate.shift(0.45 * LEFT), dexp.animate.shift(0.45 * RIGHT),
                      run_time=0.8 * k)
            p0, p1 = dT0.get_center(), dTc.get_center()
            self.play(dT0.animate(path_arc=PI).move_to(p1), dTc.animate(path_arc=PI).move_to(p0), run_time=1.0 * k)
            full4 = MathTex(r"N\,T_0\," + EXP_NEG, font_size=SIZE)
            for m in (L, eq, dTc, dN, dT0, dexp):
                m.generate_target()
            at_glyph(dN.target, full4, 0)
            at_glyph(dT0.target, full4, 1)
            at_glyph(dexp.target, full4, 3)
            bar4 = frac_layout(L.target, eq.target, dTc.target,
                               VGroup(dN.target, dT0.target, dexp.target), CEN)
            self.play(*[MoveToTarget(m) for m in (L, eq, dTc, dN, dT0, dexp)], put_bar(bar, bar4),
                      run_time=1.3 * k)

            # the minus sign goes; the exponential climbs beside T_c
            c.wait_until("minus sign")
            minus = glyphs(dexp)[1]
            self.play(*recolor([minus], RED), FlashAround(minus, color=RED, run_time=1.2, time_width=1.5),
                      run_time=1.2)
            num5 = mtbf_num()
            den5 = mtbf_den()
            for m in (L, eq, dTc, dN, dT0):
                m.generate_target()
            bar5 = frac_layout(L.target, eq.target, num5, den5, CEN)
            dTc.target.move_to(num5[0])
            dN.target.move_to(den5[0])
            dT0.target.move_to(den5[1])
            fexp = paint(paint(MathTex(r"e^{(T_c - t_{su})/\tau}", font_size=SIZE), (2, 3), YELLOW),
                         (5, 6, 7), GOLD)
            fexp_tmp = fexp.copy()
            at_glyph(fexp_tmp, dexp, 0)
            at_glyph(fexp, num5, 2)          # glyph 2 of "T_c e^..." is the e (T, c, e)
            c.wait_until("disappears")
            self.play(*edit(dexp, fexp_tmp), run_time=1.0)
            c.wait_until("so the decaying")
            # T_c steps left to its final x, then the exponential arcs (bulging right) straight
            # into its final place beside it; afterwards "=" and the denominator shift right
            # together, the denominator ahead of the "=".
            self.play(*during([MoveToTarget(dTc)], 0, 0.4),
                      *during([fexp_tmp.animate(path_arc=PI / 2).move_to(fexp)], 0.15, 0.6),
                      *during([MoveToTarget(m) for m in (L, eq, dN, dT0)] + [put_bar(bar, bar5)], 0.5, 1),
                      run_time=min(2.4, c.until("growing one")))
            self.remove(fexp_tmp)
            self.remove(dTc, fexp, dN, dT0)
            self.add(num5, den5)

        # ---------------------------------------------------------------- c5.mtbf.3
        with self.say("c5.mtbf.3") as c:
            eq1 = MathTex("=", font_size=SIZE)
            one_m = MathTex("1", font_size=SIZE)
            mden = m_pfs()
            for m in (L, eq, num5, den5):
                m.generate_target()
            mbar, rbar = result_layout(L.target, eq1, one_m, mden, eq.target, num5.target, den5.target, _p(0, -0.7))
            VGroup(L.target, eq1, one_m, mbar, mden, eq.target, num5.target, rbar, den5.target).scale(0.9)
            self.play(*during(disappear(top_l, top_eq, top_r2), 0, 0.4),
                      *during([MoveToTarget(m) for m in (L, eq, num5, den5)] + [put_bar(bar, rbar)], 0.2, 0.7),
                      *during(appear(eq1, one_m, mbar, mden, lag=0.1, shift=None), 0.6, 1),
                      run_time=min(1.8, c.until("On top")))

            c.wait_until("On top")
            self.play(FlashAround(num5, run_time=1.8, time_width=1.5), run_time=1.8)

            ins = VGroup(num5[2], num5[3], num5[4])
            brace = Brace(ins, UP, buff=0.12, color=DIM)
            tres = MathTex("t_{res}", font_size=46, color=FG).next_to(brace, UP, buff=0.12)
            c.wait_until("minus the")
            self.play(GrowFromCenter(brace), run_time=1.0)
            c.wait_until("resolution time")
            self.play(*appear(tres), run_time=1.0)
            rb = small_res_bar()
            rb.move_to(_p(-3.6, 2.35))
            c.wait_until("from last time")
            self.play(*appear(*rb[:3], shift=None), *appear(*rb[3:], lag=0.2), run_time=1.3)

            c.wait_until("Underneath")
            self.play(FlashAround(den5, run_time=1.6, time_width=1.5), run_time=1.6)

        # ---------------------------------------------------------------- c5.mtbf.4
        with self.say("c5.mtbf.4") as c:
            fparts = [L, eq1, one_m, mbar, mden, eq, num5, bar, den5]
            fg = VGroup(*[m.copy() for m in fparts])
            S = 0.72
            fg.scale(S).move_to(_p(0, 2.85))
            moves = [m.animate.become(t) for m, t in zip(fparts, fg)]
            axes = Axes(x_range=[0, 10, 10], y_range=[0, 10, 10], x_length=8.4, y_length=4.2,
                        axis_config={"color": DIM, "include_ticks": False, "stroke_width": 3},
                        tips=True).move_to(_p(-0.2, -1.15))
            xl = MathTex("T_c", font_size=44, color=YELLOW).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
            yl = MathTex(r"\mathrm{MTBF}", font_size=40).next_to(axes.y_axis.get_end(), LEFT, buff=0.2)
            self.play(*during(disappear(brace, tres, *rb), 0, 0.4),
                      *during(moves, 0.2, 0.75),
                      *during(appear(axes, xl, yl, shift=None), 0.65, 1),
                      run_time=min(2.2, c.until("Make it")))

            curve = axes.plot(f_curve, x_range=[0, 9.6], color=GOLD).set_stroke(width=5)
            x = ValueTracker(2.0)
            adot = always_redraw(lambda: Dot(axes.c2p(x.get_value(), 0), radius=0.1, color=YELLOW))
            cdot = always_redraw(lambda: Dot(axes.c2p(x.get_value(), f_curve(x.get_value())),
                                             radius=0.1, color=YELLOW))
            vl = always_redraw(lambda: DashedLine(axes.c2p(x.get_value(), 0),
                                                  axes.c2p(x.get_value(), f_curve(x.get_value())),
                                                  dash_length=0.08).set_stroke(YELLOW, 2.5))
            c.wait_until("Make it")
            self.play(Create(curve, rate_func=linear), run_time=min(3.0, c.until("grows exponentially")))
            self.add(vl, adot, cdot)
            self.play(x.animate.set_value(7.5), rate_func=rate_functions.ease_in_quad,
                      run_time=min(3.0, c.until("The input")))

            half = axes.plot(lambda t: 0.5 * f_curve(t), x_range=[0, 9.6], color=DIM).set_stroke(DIM, 4)
            c.wait_until("only divides")
            self.play(TransformFromCopy(curve, half), run_time=1.6)
            hl = T("N doubled: MTBF halved", 32, DIM).move_to(axes.c2p(4.2, 5.6))
            c.wait_until("twice as often")
            self.play(*appear(hl), run_time=1.0)  # early: names the DIM curve already drawn

            c.wait_until("slightly longer")
            y0 = f_curve(7.5)
            ghost = DashedLine(axes.c2p(0, y0), axes.c2p(7.5, y0), dash_length=0.1).set_stroke(DIM, 2.5)
            self.play(Create(ghost), run_time=0.8)
            self.play(x.animate.set_value(9.2), run_time=min(2.0, c.until(floor=1.0)))

        vl.clear_updaters()
        adot.clear_updaters()
        cdot.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
