"""Chapter 3, scene 4: less time for the logic. Clips c3.less.1 – c3.less.3.

Opens on ch3_s3's end shot (the rule at (0, 1.5), the four-piece bar at (0.3, -1.3)); the worked
numbers and the 1 ns bar are ch1_s7's (budget_bar / pcs_bar / one_ns_bar copied verbatim).
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


# ============================================================================
# THE lecture's budget bar (owned by ch1_s6; copied verbatim from ch1_s7)
# ============================================================================
BAR_H = 0.5
BAR_FILL = 0.85
BAR_OUT_W = 3


def budget_bar(segs, total, x0=-3.3, y=0.0, tc_tex="T_c", syms=True, nums=None,
               sym_size=40, num_size=34):
    g = VGroup()
    g.segs, g.syms, g.nums = [], [], []
    x = x0
    for tex, col, w in segs:
        r = Rectangle(width=w, height=BAR_H).set_stroke(width=0).set_fill(col, BAR_FILL)
        r.move_to([x + w / 2, y, 0])
        g.segs.append(r)
        x += w
    g.outline = Rectangle(width=total, height=BAR_H).set_stroke(YELLOW, BAR_OUT_W).set_fill(opacity=0)
    g.outline.move_to([x0 + total / 2, y, 0]).set_z_index(1)
    if syms:
        for (tex, col, _), r in zip(segs, g.segs):
            g.syms.append(MathTex(tex, font_size=sym_size, color=col).next_to(r, UP, buff=0.15))
    g.tc = MathTex(tc_tex, font_size=44, color=YELLOW).next_to(g.outline, LEFT, buff=0.25)
    for txt, r in zip(nums or [], g.segs):
        if txt is not None:
            g.nums.append(T(txt, num_size, GOLD).next_to(r, DOWN, buff=0.2))
    g.add(*g.segs, g.outline, *g.syms, g.tc, *g.nums)
    return g


SEG_COLORS = (PINK, PURPLE, GOLD)
SEG_TEX = ("t_{pc}", "t_{pd}", "t_{su}")


def padlock(scale=1.0):
    body = RoundedRectangle(corner_radius=0.04, width=0.26, height=0.2)
    body.set_fill(BG, 1).set_stroke(width=0)
    shackle = Arc(radius=0.085, start_angle=0, angle=PI).set_stroke(BG, 3.5)
    shackle.move_to(body.get_top() + 0.075 * UP)
    lock = VGroup(shackle, body)
    lock.scale(scale)
    return lock


def pcs_bar(pc, pd, su, tc, unit=1.0, x0=-3.3, y=0.8, tc_tex="T_c", syms=True, nums=None,
            locks=False, lock_scale=1.0, sym_size=40, num_size=34):
    segs = [(t, col, w * unit) for t, col, w in zip(SEG_TEX, SEG_COLORS, (pc, pd, su))]
    g = budget_bar(segs, tc * unit, x0, y, tc_tex, syms=syms, nums=nums,
                   sym_size=sym_size, num_size=num_size)
    g.locks = []
    if locks:
        for r in (g.segs[0], g.segs[2]):
            g.locks.append(padlock(lock_scale).move_to(r).set_z_index(2))
        g.add(*g.locks)
    return g


def one_ns_bar(unit=7.5, left=-3.3, y=0.8, numbers=True):
    big = unit >= 4
    nums = None
    if numbers:
        nums = ["0.2", "0.7 ns", "0.1"] if big else [None, "0.7 ns", None]
    return pcs_bar(0.2, 0.7, 0.1, 1.0, unit=unit, x0=left, y=y, tc_tex=r"T_c = 1\,\text{ns}",
                   syms=big, nums=nums, locks=True, lock_scale=1.3 if big else 0.85,
                   sym_size=48 if big else 40, num_size=40 if big else 34)
# ============================================================================


def colored_tex(parts, colors, size=52):
    m = MathTex(*parts, font_size=size)
    for i, col in colors.items():
        m[i].set_color(col)
    return m


# ---- layout ----------------------------------------------------------------
INEQ_Y = 1.5
S3_X0, S3_Y = 0.3 - 6.12 / 2, -1.3          # ch3_s3's end bar
S3_W = (1.02, 3.57, 0.68, 0.85)
FORM_Y = 3.2                                 # clip 2: the rearranged rule moves up
BY = -1.0                                    # clip 2: the 1 ns bar
UNIT, LEFT_X = 7.5, -3.3                     # 7.5 units per ns, as ch1_s7
SK = 0.1 * UNIT                              # 0.1 ns
UP3 = 3.5                                    # clip 3: bar 1 moves up by this
BY2 = 0.0                                    # clip 3: the second bar


def given(parts, colors):
    return colored_tex(parts, colors, size=44)


class LessLogic(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- c3.less.1: rearrange; the skew eats the logic's budget ---------------------------------
    def clip1(self):
        ineq = colored_tex(["T_c", r"\geq", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", "+", "t_{skew}"],
                           {0: YELLOW, 2: PINK, 4: PURPLE, 6: GOLD, 8: TEAL}).move_to(_p(0, INEQ_Y))
        segs = [("t_{pc}", PINK, S3_W[0]), ("t_{pd}", PURPLE, S3_W[1]),
                ("t_{su}", GOLD, S3_W[2]), ("t_{skew}", TEAL, S3_W[3])]
        bar = budget_bar(segs, sum(S3_W), x0=S3_X0, y=S3_Y, sym_size=40)
        bar.syms[2].shift(0.06 * LEFT)
        bar.syms[3].shift(0.06 * RIGHT)
        m1 = T("max", 30, PINK).next_to(bar.segs[0], DOWN, buff=0.2)
        m2 = T("max", 30, PURPLE).next_to(bar.segs[1], DOWN, buff=0.2)
        m2.align_to(m1, DOWN)
        self.bar, self.ineq, self.maxes = bar, ineq, (m1, m2)
        pieces = [ineq, *bar.segs, bar.outline, *bar.syms, bar.tc, m1, m2]

        with self.say("c3.less.1") as c:
            self.play(*[FadeIn(m) for m in pieces], run_time=1.0)  # early: s3's end shot returns
            # {rearrange}: the designer's part, the logic, glows
            c.wait_until("logic")
            others = [ineq[i] for i in range(9) if i != 4]
            self.play(FlashAround(ineq[4], color=PURPLE, time_width=1.5, buff=0.12),
                      FlashAround(bar.segs[1], color=PURPLE, time_width=1.5),
                      *set_alpha(others, 0.5), run_time=1.8)
            # {solve}: t_pd to the left, the rest across
            c.wait_until("solve")
            self.play(*set_alpha(others, 1), run_time=0.6)
            rearr = colored_tex(["t_{pd}", r"\leq", "T_c", "-", "(", "t_{pc}", "+", "t_{su}", "+",
                                 "t_{skew}", ")"],
                                {0: PURPLE, 2: YELLOW, 5: PINK, 7: GOLD, 9: TEAL}).move_to(_p(0, INEQ_Y))
            # keyed rearrangement: old piece -> new piece; t_pd arcs over the row to the left,
            # >= and the spare + leave first, the new <=, -, ( and ) arrive last
            keep = {0: 2, 2: 5, 3: 6, 6: 7, 7: 8, 8: 9}
            leave = during([FadeOut(ineq[1]), FadeOut(ineq[5])], 0, 0.3)
            slide = during([Transform(ineq[i], rearr[j]) for i, j in keep.items()], 0.15, 0.75)
            a, b = ineq[4].get_center(), rearr[0].get_center()
            lift = 0.85 * UP
            path = VMobject().set_points_smoothly([a, a + 0.75 * lift, a + lift + 0.6 * LEFT,
                                                   b + lift + 0.6 * RIGHT, b + 0.75 * lift, b])
            hop = during([MoveAlongPath(ineq[4], path)], 0.12, 0.8)
            arrive = during([FadeIn(rearr[k]) for k in (1, 3, 4, 10)], 0.72, 1)
            self.play(*leave, *slide, *hop, *arrive, run_time=2.2)
            self.remove(*ineq.get_family())
            self.add(rearr)
            self.rearr = rearr
            # {eats}: no skew first (TEAL collapses, the logic gets it all), then the skew pushes
            # back in from the right end and the logic shrinks by as much
            c.wait_until("eats")
            s = bar.segs
            sk_w = S3_W[3]
            rt = min(1.5, max(1.0, (c.until() - 0.4) / 2))
            self.play(s[3].animate.stretch_to_fit_width(0.01, about_edge=RIGHT),
                      s[1].animate.stretch_to_fit_width(S3_W[1] + sk_w, about_edge=LEFT),
                      s[2].animate.shift(sk_w * RIGHT),
                      bar.syms[1].animate.shift(sk_w / 2 * RIGHT),
                      bar.syms[2].animate.shift(sk_w * RIGHT),
                      *during([bar.syms[3].animate.set_fill(opacity=0).shift(sk_w / 2 * RIGHT)], 0, 0.25),
                      m2.animate.shift(sk_w / 2 * RIGHT),
                      run_time=rt)
            self.wait(min(0.6, max(0.3, c.until() - 2 * rt)))
            self.play(s[3].animate.stretch_to_fit_width(sk_w, about_edge=RIGHT),
                      s[1].animate.stretch_to_fit_width(S3_W[1], about_edge=LEFT),
                      s[2].animate.shift(sk_w * LEFT),
                      bar.syms[1].animate.shift(sk_w / 2 * LEFT),
                      bar.syms[2].animate.shift(sk_w * LEFT),
                      *during([bar.syms[3].animate.set_fill(opacity=1).shift(sk_w / 2 * LEFT)], 0.65, 1),
                      m2.animate.shift(sk_w / 2 * LEFT),
                      run_time=rt)

    # -- c3.less.2: the worked example, 1 ns, then 0.1 ns of skew -------------------------------
    def clip2(self):
        bar, rearr = self.bar, self.rearr
        m1, m2 = self.maxes
        g_pc = given(["t_{pc}", "=", r"0.2\,\text{ns}"], {0: PINK, 2: GOLD})
        g_su = given(["t_{su}", "=", r"0.1\,\text{ns}"], {0: GOLD, 2: GOLD})
        g_pc.move_to(_p(0, 1.9)).to_edge(LEFT, buff=0.9)
        g_su.move_to(_p(0, 1.15)).align_to(g_pc, LEFT)
        g_f = given(["f_c", "=", r"1\,\text{GHz}", r"\;\rightarrow\;", "T_c", "=", r"1\,\text{ns}"],
                    {0: YELLOW, 2: GOLD, 4: YELLOW, 6: GOLD})
        g_f.move_to(_p(0, 1.9)).align_to(_p(0.5, 0), LEFT)
        g_sk = given(["t_{skew}", "=", r"0.1\,\text{ns}"], {0: TEAL, 2: GOLD})
        g_sk.move_to(_p(0, 1.15)).align_to(g_f, LEFT)
        wire = T("≈ 1.5 cm of extra board wire", 30, DIM).next_to(g_sk, DOWN, buff=0.22)
        wire.align_to(g_sk, LEFT)
        self.givens = [g_pc, g_su, g_f, g_sk, wire]

        with self.say("c3.less.2") as c:
            # {example}: the rule moves up; the "max" tags go
            self.play(*during(disappear(m1, m2), 0, 0.5),
                      rearr.animate.scale(0.92).move_to(_p(0, FORM_Y)), run_time=1.4)
            c.wait_until("clock-to-cue delay")
            self.play(*appear(g_pc), run_time=1.0)
            c.wait_until("set-up time")
            self.play(*appear(g_su), run_time=1.0)
            # {ghz}
            c.wait_until("ghz")
            self.play(*appear(g_f), run_time=1.2)
            # the bar is redrawn 1 ns wide (ch1_s7's), without the skew
            c.wait_until("one nanosecond")
            b1 = one_ns_bar(unit=UNIT, left=LEFT_X, y=BY, numbers=True)
            n02, n07, n01 = b1.nums
            moves = [Transform(bar.segs[i], b1.segs[i]) for i in range(3)]
            moves += [Transform(bar.syms[i], b1.syms[i]) for i in range(3)]
            moves += [Transform(bar.outline, b1.outline)]
            self.play(*moves,
                      *during([FadeOut(bar.segs[3]), FadeOut(bar.syms[3])], 0, 0.4),
                      *during(swap(bar.tc, b1.tc), 0.4, 1),
                      *during([FadeIn(lk) for lk in b1.locks] + appear(n02, n01, shift=None), 0.6, 1),
                      run_time=2.0)
            segs = list(bar.segs[:3])
            syms = list(bar.syms[:3])
            outline, tc, locks = bar.outline, b1.tc, b1.locks
            c.wait_until("zero point seven")
            self.play(*appear(n07), FlashAround(segs[1], color=PURPLE, time_width=1.5), run_time=1.5)
            # {skew}
            c.wait_until("skew")
            self.play(*appear(g_sk), run_time=1.2)
            c.wait_until("on a board")
            self.play(*appear(wire), run_time=1.0)
            # {left}: the skew slides in at the right end; the logic shrinks to 0.6 ns
            c.wait_until("left")
            teal = Rectangle(width=SK, height=BAR_H).set_stroke(width=0).set_fill(TEAL, BAR_FILL)
            teal.move_to(_p(LEFT_X + UNIT - SK / 2, BY))
            t_sym = MathTex("t_{skew}", font_size=48, color=TEAL).next_to(teal, UP, buff=0.15)
            t_sym.align_to(syms[0], DOWN)
            t_num = T("0.1", 40, GOLD).next_to(teal, DOWN, buff=0.2).align_to(n01, DOWN)
            lab_shift = 0.35            # the GOLD labels step aside for the TEAL ones
            pd_left = segs[1].get_left()[0]
            new_pd_w = 0.6 * UNIT
            # the sliver it lost flashes, and its tag drops in, as PURPLE finishes shrinking
            sliver = Rectangle(width=SK, height=BAR_H).move_to(_p(pd_left + new_pd_w + SK / 2, BY))
            seventh = T("1/7 of the logic’s time", 30, PURPLE)
            seventh.move_to(_p(sliver.get_x(), BY - 1.5))
            self.play(FadeIn(teal, shift=1.4 * LEFT), FadeIn(t_sym, shift=1.4 * LEFT),
                      *during([FlashAround(sliver, color=PURPLE, stroke_width=6, time_width=1.5,
                                           buff=0.08)] + appear(seventh), 0.3, 0.8),
                      FadeIn(t_num, shift=1.4 * LEFT),
                      segs[1].animate.stretch_to_fit_width(new_pd_w, about_edge=LEFT),
                      segs[2].animate.shift(SK * LEFT), locks[1].animate.shift(SK * LEFT),
                      syms[2].animate.shift((SK + lab_shift) * LEFT),
                      n01.animate.shift((SK + lab_shift) * LEFT),
                      syms[1].animate.shift(SK / 2 * LEFT),
                      n07.animate.shift(SK / 2 * LEFT),
                      run_time=1.8)
            c.wait_until("zero point six")
            n06 = T("0.6 ns", 40, GOLD).move_to(n07)
            self.play(*swap(n07, n06), run_time=1.0)

        self.b1 = dict(segs=[*segs, teal], syms=[*syms, t_sym], nums=[n02, n06, n01, t_num],
                       outline=outline, tc=tc, locks=list(locks))
        self.seventh = seventh

    # -- c3.less.3: keep 0.7 ns and the clock period grows -------------------------------------
    def clip3(self):
        b = self.b1
        seventh = self.seventh
        bar1 = [*b["segs"], *b["syms"], *b["nums"], b["outline"], b["tc"], *b["locks"]]

        segs2 = [("t_{pc}", PINK, 0.2 * UNIT), ("t_{pd}", PURPLE, 0.7 * UNIT),
                 ("t_{su}", GOLD, SK), ("t_{skew}", TEAL, SK)]
        b2 = budget_bar(segs2, 1.1 * UNIT, x0=LEFT_X, y=BY2, syms=False,
                        nums=["0.2", "0.7 ns", "0.1", "0.1"], num_size=40)
        b2.nums[2].shift(0.2 * LEFT)
        b2.nums[3].shift(0.2 * RIGHT)
        locks2 = [padlock(1.3).move_to(b2.segs[i]).set_z_index(2) for i in (0, 2)]
        x1 = LEFT_X + UNIT
        mark = DashedLine(_p(x1, b["nums"][3].get_bottom()[1] + UP3 - 0.08), _p(x1, BY2 - 0.95), dash_length=0.1)
        mark.set_stroke(YELLOW, 2)
        mark_lab = T("1 ns", 30, YELLOW).next_to(mark, DOWN, buff=0.12)
        need = colored_tex(["T_c", r"\geq", r"1.1\,\text{ns}"], {0: YELLOW, 2: GOLD})
        need.move_to(_p(0.3, -1.6))
        old_f = MathTex(r"1\,\text{GHz}", font_size=48, color=DIM)
        new_f = colored_tex(["f_c", r"\leq", r"909\,\text{MHz}"], {0: YELLOW, 2: GOLD}, size=52)
        VGroup(old_f, new_f).arrange(RIGHT, buff=1.0).move_to(_p(0.3, -2.75))
        strike = Line(old_f.get_left() + 0.12 * LEFT, old_f.get_right() + 0.12 * RIGHT).set_stroke(RED, 5)

        with self.say("c3.less.3") as c:
            # {other}: the givens clear; bar 1 (and its 1/7 tag) moves up
            sweep_clear(self, *[m.animate.shift(UP3 * UP) for m in [*bar1, seventh]],
                        keep=[*bar1, seventh], run_time=2.2)
            # {keep}: the tag goes first, then a second bar with the logic kept at 0.7 ns
            c.wait_until("keep")
            self.play(*during(disappear(seventh), 0, 0.3),
                      *during([ReplacementTransform(s.copy(), s2) for s, s2 in zip(b["segs"], b2.segs)]
                              + [ReplacementTransform(lk.copy(), lk2) for lk, lk2 in zip(b["locks"], locks2)],
                              0.33, 1),
                      run_time=2.4)
            c.wait_until("nanoseconds")
            self.play(*appear(*b2.nums, lag=0.15), run_time=1.2)
            # {grow}: the 1 ns mark comes down; the period grows to 1.1 ns
            c.wait_until("grow")
            self.play(GrowFromEdge(mark, UP), run_time=0.9)
            c.wait_until("at least")
            self.play(GrowFromEdge(b2.outline, LEFT), *appear(mark_lab, shift=None),
                      run_time=min(1.2, c.until("one point one")))
            c.wait_until("one point one")
            self.play(*appear(need), run_time=1.0)
            # {mhz}
            c.wait_until("mhz")
            self.play(*appear(old_f, shift=None), run_time=0.8)
            self.play(Create(strike), *appear(new_f), run_time=1.2)
            # {cost}
            c.wait_until("cost")
            self.play(FlashAround(b2.segs[3], color=TEAL, stroke_width=6, time_width=1.5),
                      FlashUnder(new_f[2], color=GOLD, time_width=1.5), run_time=2.0)
