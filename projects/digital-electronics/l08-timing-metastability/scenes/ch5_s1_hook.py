"""Chapter 5, scene 1: hook: a one-in-ten-million failure, once a second vs a million times a second. Clips c5.hook.1 – c5.hook.3.

Shots: title card -> ch4 s5's sync_circuit() centred high, ch4 s6's boxed pfail_formula() (P_fail GOLD)
beside res_bar() below it -> a BLUE pulse on D0, D1 wobbles RED, FF1's edge, RED "???" flickers at Q
-> on {years} the circuit shrinks to the chapter's small spot (scale 0.6, to_corner(UL, buff=0.5)),
the formula to the upper right, a 2-year time axis with month ticks across the middle; GOLD
"P_fail = 1 in 10,000,000" under the formula -> fine BLUE comb, 6 RED crosses every 116 days, row
"1 change per second -> a failure every 10^7 s ~ 116 days" -> the comb fills solid, the axis becomes
0..60 s, the crosses slide to every 10 s, row "10^6 changes per second -> a failure every 10 s" ->
YELLOW underlines under the rates -> all dims, two YELLOW questions in the band above the axis.
Copied as they stand: make_ff()/sync_circuit() (ch4_s5), budget_bar()/res_bar()/pfail_formula() (ch4_s6).
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
from lib.titles import title_card  # noqa: E402


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================


# =============================================================================================
# push_button() + make_ff(): copied from ch4_s1_hook.py (Q-bar dropped here: the synchroniser
# uses Q only, as the slide does)
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
PUSH = 0.18


def make_ff(center=ORIGIN, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    g = VGroup(d_w, q_w, box, tri, d_l, q_l)
    g.box, g.tri = box, tri
    g.d_l, g.q_l, g.d_w, g.q_w, g.clk_w = d_l, q_l, d_w, q_w, clk_w
    g.shift(center)
    clk_w.shift(center)
    return g


def push_button(center=ORIGIN):
    stem = Line(_p(-0.3, 0), _p(-0.58, 0)).set_stroke(FG, 5)
    cap = RoundedRectangle(corner_radius=0.06, width=0.16, height=0.62).set_stroke(FG, 4).set_fill(DIM, 1)
    cap.move_to(_p(-0.66, 0))
    body = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.84).set_stroke(FG, 4).set_fill(BG, 1)
    g = VGroup(stem, cap, body)
    g.stem, g.cap, g.body = stem, cap, body
    g.shift(center)
    g.out = lambda: body.get_right()
    return g


def fingertip():
    f = RoundedRectangle(corner_radius=0.21, width=1.4, height=0.44).set_stroke(FG, 3).set_fill(BG, 1)
    f.move_to(_p(-0.7, 0))
    nail = RoundedRectangle(corner_radius=0.07, width=0.34, height=0.17).set_stroke(FG, 2)
    nail.move_to(_p(-0.27, 0.07))
    return VGroup(f, nail)
# =============================================================================================


# =============================================================================================
# sync_circuit(): the two-flip-flop synchroniser (slide p. 112), top half. s6 / recap copy it.
# =============================================================================================
SK = 0.62                    # flip-flop scale
SFF_X = (-1.7, 2.1)          # FF0, FF1 centres
SFF_Y = 2.244                # box centre (top 3.05)
SBTN_X = -4.3                # button housing centre
SHX = (BOX_W / 2 + WIRE) * SK


def sync_circuit():
    C = VGroup()
    ffs = []
    for x in SFF_X:
        f = make_ff()
        f.scale(SK, about_point=ORIGIN).shift(_p(x, SFF_Y))
        f.clk_w.scale(SK, about_point=ORIGIN).shift(_p(x, SFF_Y))
        for lb in (f.d_l, f.q_l):
            lb.scale(1.45, about_point=lb.get_center())
        ffs.append(f)
    C.ff0, C.ff1 = ffs
    py = SFF_Y + PIN_Y * SK
    C.py = py
    C.ff0.q_w.set_stroke(TEAL)
    C.ff0.q_l.set_color(TEAL)
    C.ff1.d_w.set_stroke(TEAL)
    C.ff1.d_l.set_color(TEAL)
    C.names = [T(f"FF{i}", 30, FG).move_to(f.box.get_center() + 0.3 * DOWN) for i, f in enumerate(ffs)]
    C.btn = push_button(_p(SBTN_X, py))
    C.d0_w = Line(C.btn.out(), C.ff0.d_w.get_start()).set_stroke(BLUE, 5)
    C.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(
        (C.btn.out() + C.ff0.d_w.get_start()) / 2, UP, buff=0.14)
    C.link = Line(C.ff0.q_w.get_end(), C.ff1.d_w.get_start()).set_stroke(TEAL, 5)
    C.d1_l = MathTex("D_1", font_size=40, color=TEAL).next_to(C.link, UP, buff=0.12)
    C.q_l = MathTex("Q", font_size=40, color=GREEN).next_to(C.ff1.q_w.get_end(), RIGHT, buff=0.15)
    by = SFF_Y - (BOX_H / 2 + EN_WIRE) * SK
    C.by = by
    C.bus = Line(_p(-3.2, by), _p(SFF_X[1], by)).set_stroke(YELLOW, 5)
    C.jdot = Dot(_p(SFF_X[0], by), radius=0.08, color=YELLOW)
    C.clk_ws = [f.clk_w for f in ffs]
    C.clk_l = T("CLK", 30, YELLOW).next_to(C.bus.get_start(), LEFT, buff=0.15)
    C.finger = fingertip().shift(C.btn.cap.get_left())
    C.d1_wires = [C.ff0.q_w, C.link, C.ff1.d_w]
    C.all = [C.ff0, C.ff1, *C.names, C.btn, C.d0_w, C.d0_l, C.link, C.d1_l, C.q_l,
             C.bus, C.jdot, *C.clk_ws, C.clk_l]
    C.add(*C.all)
    return C
# =============================================================================================


# =============================================================================================


# ============================================================================
# THE lecture's budget bar (owned by ch1_s6; ch1_s7, ch1_s8, ch3, ch4, ch7 copy this block)
# ============================================================================
BAR_H = 0.5          # segment / outline height
BAR_FILL = 0.85      # segment fill opacity (no stroke)
BAR_OUT_W = 3        # YELLOW outline stroke


def budget_bar(segs, total, x0=-3.3, y=0.0, tc_tex="T_c", syms=True, nums=None,
               sym_size=40, num_size=34):
    """One clock period as a budget. `segs` = [(tex, colour, length), ...] laid flush left to right
    from x0 (they may run past the outline: a broken budget). `total` = the outline's length (one T_c).
    Returns VGroup(*segs, outline, *syms, tc, *nums) with
      .segs    Rectangles BAR_H tall, filled in their colour at BAR_FILL, no stroke (z 0)
      .outline YELLOW Rectangle, stroke BAR_OUT_W, no fill, x0 .. x0 + total (z 1, over the segments)
      .syms    MathTex(tex, sym_size) in the segment's colour, 0.15 above each segment ([] if not syms)
      .tc      MathTex(tc_tex, 44) YELLOW, 0.25 left of the outline
      .nums    GOLD T(text, num_size) 0.2 under each segment whose `nums` entry is not None"""
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
# ============================================================================

# =============================================================================================
# res_bar(): the synchroniser's budget, t_res + t_su = T_c (s6's bar; the recap copies it)
# pfail_formula(): s4's model, and P_fail boxed (slide p. 113; the recap copies it)
# needs budget_bar() (ch1_s6 block above)
# =============================================================================================
RB_X0, RB_TOT, RB_SU, RB_Y = -2.04, 5.1, 0.85, -1.35   # under s6's diagram: E1 .. second edge
PF_SIZE = 64


def res_bar(x0=RB_X0, y=RB_Y, total=RB_TOT, su=RB_SU):
    """t_res (FG) then t_su (GOLD), one T_c long."""
    return budget_bar([("t_{res}", FG, total - su), ("t_{su}", GOLD, su)], total, x0=x0, y=y)


def model_formula(size=PF_SIZE):
    """s4's model P(t_res > t) = T0/T_c e^{-t/tau}; T_c YELLOW. .t = the exponent's t."""
    m = MathTex(r"P(t_{res} > t) = \frac{T_0}{T_c}\, e^{-t/\tau}", font_size=size)
    for i in (13, 14):
        m[0][i].set_color(YELLOW)
    m.t = m[0][17]
    return m


def color_tc_tsu(m):
    """Colour a MathTex 'T_c - t_{su}': T_c YELLOW, t_su GOLD."""
    for i in (0, 1):
        m[0][i].set_color(YELLOW)
    for i in (3, 4, 5):
        m[0][i].set_color(GOLD)
    return m


def pfail_formula(size=PF_SIZE):
    """P_fail = T0/T_c e^{-(T_c - t_su)/tau}, boxed YELLOW. VGroup(main, ins, box):
    .main the formula with an empty slot in the exponent, .ins the 'T_c - t_su' in that slot
    (s6 flies it in), .box, .frac / .expo (VGroups for flashes and arrows, not on screen)."""
    main = MathTex(r"P_{fail} = \frac{T_0}{T_c}\, e^{-(\phantom{T_c - t_{su}})/\tau}", font_size=size)
    g = main[0]
    for i in (9, 10):
        g[i].set_color(YELLOW)
    ins = color_tc_tsu(MathTex(r"T_c - t_{su}", font_size=size))
    lp, rp = g[13], g[14]
    ins.scale_to_fit_width(rp.get_left()[0] - lp.get_right()[0] - 0.1)
    ins.move_to([(lp.get_right()[0] + rp.get_left()[0]) / 2, ins.get_y(), 0])
    ins.shift((lp.get_y() - ins[0][2].get_y()) * UP)
    box = SurroundingRectangle(VGroup(main, ins), buff=0.3).set_stroke(YELLOW, 3)
    F = VGroup(main, ins, box)
    F.main, F.ins, F.box = main, ins, box
    F.frac = VGroup(*g[6:11])
    F.expo = VGroup(*g[11:17], ins)
    return F



# =============================================================================================
# this scene's own layout
# =============================================================================================
SMALL = 0.6                      # the chapter's small synchroniser: scale 0.6 (labels >= 18), to_corner(UL, buff=0.5)
AX_Y = -0.35                     # the time axis
AX_X0, AX_X1 = -6.0, 6.0
AX_W = AX_X1 - AX_X0
COMB_H = 0.42
ROW1_Y, ROW2_Y = -1.95, -3.0    # the two rate -> failure rows
ROW_X = -6.0                     # rows left-aligned here
Q1_Y, Q2_Y = 1.35, 0.6           # the questions, in the band above the axis
DAYS = 730.0


def ax_x(frac):
    return AX_X0 + frac * AX_W


def time_axis():
    A = VGroup()
    A.line = Line(_p(AX_X0, AX_Y), _p(AX_X1, AX_Y)).set_stroke(FG, 3)
    A.end_ticks = VGroup(*[Line(_p(x, AX_Y - 0.16), _p(x, AX_Y + 0.16)).set_stroke(FG, 3)
                           for x in (AX_X0, AX_X1)])
    A.months = VGroup(*[Line(_p(ax_x(k / 24), AX_Y - 0.1), _p(ax_x(k / 24), AX_Y)).set_stroke(DIM, 2)
                        for k in range(1, 24)])
    A.zero = T("0", 32).next_to(_p(AX_X0, AX_Y - 0.16), DOWN, buff=0.15)
    A.end = T("2 years", 32).next_to(_p(AX_X1, AX_Y - 0.16), DOWN, buff=0.15)
    A.add(A.line, A.end_ticks, A.months, A.zero, A.end)
    return A


def ten_s_ticks():
    return VGroup(*[Line(_p(ax_x(k / 6), AX_Y - 0.13), _p(ax_x(k / 6), AX_Y)).set_stroke(DIM, 2)
                    for k in range(1, 6)])


def comb(n=220):
    return VGroup(*[Line(_p(ax_x((i + 0.5) / n), AX_Y), _p(ax_x((i + 0.5) / n), AX_Y + COMB_H))
                    .set_stroke(BLUE, 1.6) for i in range(n)])


def solid_comb():
    return Rectangle(width=AX_W, height=COMB_H).set_stroke(width=0).set_fill(BLUE, 0.85).move_to(
        _p(0, AX_Y + COMB_H / 2))


def cross_at(x):
    return cross_mark(RED).move_to(_p(x, AX_Y + COMB_H / 2)).set_z_index(2)


def rate_row(num, word, y):
    """VGroup(num, word): BLUE rate text; .word is what gets underlined."""
    n = MathTex(num, font_size=44, color=BLUE)
    w = T(word, 34, BLUE)
    g = VGroup(n, w).arrange(RIGHT, buff=0.18)
    w.shift((n[0][0].get_bottom()[1] - w[0].get_bottom()[1]) * UP)   # baselines: '1'/'10' with the 'c'
    g.move_to(_p(0, y)).align_to(_p(ROW_X, 0, ), LEFT)
    g.num, g.word = n, w
    return g


class Hook(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------------- clip 1
        with self.say("c5.hook.1", gap=0.6) as c:
            card = title_card("Part 5 · Mean time between failures")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course, card.part, lag=0.35), run_time=1.3)  # early: title card read whole

            # {synch}: the synchroniser, centred high
            C = sync_circuit()
            C.shift((0 - C.get_x()) * RIGHT + 0.1 * DOWN)
            F = pfail_formula()
            for i in range(5):
                F.main[0][i].set_color(GOLD)
            F.scale_to_fit_width(5.6).move_to(_p(-3.2, -1.45))
            B = res_bar()
            B.scale(0.78).move_to(_p(3.4, -1.35))
            c.wait_until("synch")
            sweep_clear(self, time_span(FadeIn(C), 0.6, 1.4), run_time=1.4)
            c.wait_until("found")
            self.play(*appear(F, B, lag=0.4, shift=None), run_time=min(1.4, c.until("the chance")))  # early: ch4's last shot, read as one

            # {gamble}: a change on D0, D1 caught mid-way, still wobbling at FF1's edge
            c.wait_until("gamble")
            d0 = C.d0_w.copy().set_stroke(BLUE, 10)
            self.play(VShowPassingFlash(d0, time_width=0.6, run_time=0.8),
                      *during([w.animate.set_stroke(RED) for w in C.d1_wires] + [C.d1_l.animate.set_color(RED)],
                              0.55, 1), run_time=0.9)
            x0, x1 = C.ff0.q_w.get_start()[0], C.ff1.d_w.get_end()[0]
            py = C.py
            phase = ValueTracker(0)
            wob = always_redraw(lambda: FunctionGraph(
                lambda x: py - 0.02 + 0.06 * np.sin(9 * (x - x0) + phase.get_value()) * np.sin(PI * (x - x0) / (x1 - x0)),
                x_range=[x0, x1]).set_stroke(RED, 4))
            self.add(wob)
            bus = C.bus.copy().set_stroke(YELLOW, 10)
            qq = T("???", 40, RED).next_to(C.q_l, RIGHT, buff=0.2)
            qq.set_opacity(0)
            self.add(qq)

            def flick(m, a):
                m.set_opacity(0 if a < 0.45 else 0.55 + 0.45 * np.cos(14 * (a - 0.45)) ** 2)

            self.play(phase.animate.set_value(30), VShowPassingFlash(bus, time_width=0.5),
                      UpdateFromAlphaFunc(qq, flick), run_time=min(1.9, c.until()), rate_func=linear)
            qq.set_opacity(1)

        # ---------------------------------------------------------------- clip 2
        with self.say("c5.hook.2") as c:
            # {years}: shrink to the shared small spot; a two-year axis
            wob.clear_updaters()
            self.remove(phase)
            self.play(*disappear(qq, wob, B),
                      *[w.animate.set_stroke(TEAL) for w in C.d1_wires], C.d1_l.animate.set_color(TEAL),
                      run_time=0.8)
            ftarget = F.copy().scale_to_fit_width(4.2).move_to(_p(4.3, 3.15))
            A = time_axis()
            self.play(C.animate.scale(SMALL).to_corner(UL, buff=0.5),
                      F.animate.become(ftarget),
                      *during(appear(A, shift=None), 0.55, 1), run_time=min(2.0, c.until("tenmillion")))

            # {tenmillion}
            tag = VGroup(MathTex(r"P_{fail}", font_size=44, color=GOLD),
                         T("= 1 in 10,000,000", 36, GOLD)).arrange(RIGHT, buff=0.15)
            tag[1].shift((tag[0][0][0].get_bottom()[1] - tag[1].get_bottom()[1]) * UP)
            tag.next_to(ftarget, DOWN, buff=0.25)
            c.wait_until("tenmillion")
            self.play(*appear(tag), FlashAround(tag, color=GOLD, run_time=1.4, time_width=1.5), run_time=1.4)  # early: the tag is the sentence

            # {slow}: one change a second, a failure every 116 days
            c.wait_until("slow")
            K = comb()
            r1 = rate_row("1", "change per second", ROW1_Y)
            self.play(LaggedStart(*[FadeIn(l) for l in K], lag_ratio=0.02),
                      *during(appear(r1), 0.3, 1), run_time=min(2.0, c.until("failure about")))  # early: row read with its sentence
            day_x = [ax_x(116 * k / DAYS) for k in range(1, 7)]
            X = [cross_at(x) for x in day_x]
            c.wait_until("failure about")
            self.play(*appear(*X, lag=0.3, shift=None), run_time=min(1.6, c.until("ten million seconds")))
            r2 = rate_row("10^6", "changes per second", ROW2_Y)
            arr_x = max(r1.get_right()[0], r2.get_right()[0]) + 0.35
            arr1 = MathTex(r"\rightarrow", font_size=44, color=FG).next_to(_p(arr_x, r1.get_y()), RIGHT, buff=0)
            res1 = MathTex(r"\text{a failure every } 10^{7}\text{ s} \approx 116 \text{ days}",
                           font_size=44, color=RED).next_to(arr1, RIGHT, buff=0.35)
            c.wait_until("ten million seconds")
            self.play(*appear(arr1, res1, lag=0.3), run_time=1.3)  # early: result built on its words

            # {fast}: a million changes a second, a failure every 10 s
            c.wait_until("fast")
            S = solid_comb()
            self.play(*during([FadeIn(S)], 0, 0.7), *during(disappear(*K), 0.3, 1),
                      *during(appear(r2), 0.3, 1), run_time=min(1.6, c.until("failure every")))  # early: row read with its sentence
            end2 = T("60 s", 32).move_to(A.end)
            ticks2 = ten_s_ticks()
            c.wait_until("failure every")
            self.play(*swap(A.end, end2), *during(disappear(A.months), 0, 0.5), *during(appear(ticks2, shift=None), 0.5, 1),
                      *[x.animate.move_to(_p(ax_x(k / 6), x.get_y())) for k, x in enumerate(X, 1)],
                      run_time=min(1.6, c.until("depends")))
            arr2 = MathTex(r"\rightarrow", font_size=44, color=FG).next_to(r2, RIGHT, buff=0.35)
            res2 = MathTex(r"\text{a failure every } 10\text{ s}", font_size=44, color=RED)
            res2.next_to(arr2, RIGHT, buff=0.35).align_to(res1, LEFT)
            arr2.align_to(arr1, LEFT)
            self.play(*appear(arr2, res2, lag=0.3), run_time=min(1.2, c.until("depends")))  # early: result on its words

            # {depends}
            c.wait_until("depends")
            u1 = underline(r1.word, YELLOW)
            u2 = underline(r2.word, YELLOW)
            self.play(GrowFromCenter(u1), GrowFromCenter(u2), run_time=1.2)

        # ---------------------------------------------------------------- clip 3
        with self.say("c5.hook.3") as c:
            q1 = T("How long, on average, between failures?", 44, YELLOW).move_to(_p(0, Q1_Y))
            q2 = T("What clock period makes that at least a year?", 44, YELLOW).move_to(_p(0, Q2_Y))
            board = [m for m in self.mobjects if isinstance(m, VMobject)]
            self.play(*set_alpha(board, DIMMED), *during(appear(q1), 0.4, 1), run_time=1.4)  # early: the question is the sentence
            c.wait_until("year")
            self.play(*appear(q2), run_time=1.2)  # early: second question, read with its sentence

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
