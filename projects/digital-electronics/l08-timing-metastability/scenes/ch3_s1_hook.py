"""Chapter 3, scene 1: hook: both rules assume one instant; a real clock tree spreads the edge out.
Clips c3.hook.1 – c3.hook.2.

Shots: title card -> ch1_s4's path_diagram() (scale 0.8, centre (0, -0.9), one CLK line) under
ch2_s4's two inequalities (size 40, stacked, >= aligned,
GOLD tags T 30 on the left as in ch2_s6's tile) -> the path shrinks into the board's top-right
corner -> clock_board(): a dozen small FFs fed by a YELLOW comb tree, one edge spreads, ticks
collect on an axis under the board -> "?" and the inequalities return, small, with "?".
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
# make_ff + path_diagram, copied from ch2_s6_recap.py (ch1_s4_path.py geometry, one CLK line)
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    g.box, g.tri = box, tri
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


P_FF_Y = 0.5
P_PIN = P_FF_Y + PIN_Y
P_BUS = P_FF_Y - BOX_H / 2 - EN_WIRE
P_BUS_X0 = -5.6
P_CL_H = 1.6


def path_diagram(ff_x=(-4.4, 4.4), cl_w=3.4):
    P = VGroup()
    ffs = []
    for x in ff_x:
        f = make_ff(_p(x, P_FF_Y))
        f.remove(f.clk_w)
        ffs.append(f)
    P.ff0, P.ff1 = ffs
    P.names = [T(f"FF{i}", 36, FG).next_to(f.box, UP, buff=0.2) for i, f in enumerate(ffs)]
    x_q0 = ff_x[0] + BOX_W / 2 + WIRE
    x_d1 = ff_x[1] - BOX_W / 2 - WIRE
    P.cl = Rectangle(width=cl_w, height=P_CL_H).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(0, P_PIN))
    P.cl_l = VGroup(T("Combinational", 32, BLUE), T("Logic (CL)", 32, BLUE)).arrange(DOWN, buff=0.12).move_to(P.cl)
    P.q0_w = Line(_p(x_q0, P_PIN), _p(-cl_w / 2, P_PIN)).set_stroke(GREEN, 5)
    P.d1_w = Line(_p(cl_w / 2, P_PIN), _p(x_d1, P_PIN)).set_stroke(BLUE, 5)
    P.q0_l = MathTex("Q_0", font_size=40, color=GREEN).next_to(_p(x_q0, P_PIN), UP, buff=0.15)
    P.d1_l = MathTex("D_1", font_size=40, color=BLUE).next_to(_p(x_d1, P_PIN), UP, buff=0.15)
    P.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(P.ff0.d_w, LEFT, buff=0.12)
    P.q1_l = MathTex("Q_1", font_size=40, color=GREEN).next_to(P.ff1.q_w, RIGHT, buff=0.12)
    P.clk_bus = Line(_p(P_BUS_X0, P_BUS), _p(ff_x[1], P_BUS)).set_stroke(YELLOW, 5)
    P.clk_dot = Dot(_p(ff_x[0], P_BUS), radius=0.08, color=YELLOW)
    P.clk_l = T("CLK", 34, YELLOW).next_to(_p(P_BUS_X0, P_BUS), LEFT, buff=0.15)
    P.clk_br0, P.clk_br1 = ffs[0].clk_w, ffs[1].clk_w
    P.all = [P.ff0, P.ff1, *P.names, P.cl, P.cl_l, P.q0_w, P.q0_l, P.d1_w, P.d1_l, P.d0_l, P.q1_l,
             P.clk_bus, P.clk_dot, P.clk_l, P.clk_br0, P.clk_br1]
    P.add(*P.all)

    def clk_paths(width=10):
        s = P.clk_bus.get_start()
        out = []
        for br in (P.clk_br0, P.clk_br1):
            a, b = br.get_start(), br.get_end()
            out.append(VMobject().set_points_as_corners([s, a, b]).set_stroke(YELLOW, width))
        return out
    P.clk_paths = clk_paths
    return P


# =============================================================================================
# The two inequalities, ch2_s4_noclockfix.py styling (t_pc PINK, t_pd PURPLE, t_su/t_hold GOLD)
# =============================================================================================
def inequalities(size=40):
    l1 = MathTex("T_c", r"\geq", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", font_size=size)
    l2 = MathTex("(", "t_{pc}", "+", "t_{pd}", ")", r"_{\min}", r"\geq", "t_{hold}", font_size=size)
    for m, cols in ((l1, {2: PINK, 4: PURPLE, 6: GOLD}), (l2, {1: PINK, 3: PURPLE, 7: GOLD})):
        for i, col in cols.items():
            m[i].set_color(col)
    return l1, l2


# =============================================================================================
# clock_board(): a board of 12 small flip-flops fed by a YELLOW comb-shaped clock tree
#   B.rect             dark rounded rectangle, 12.4 x 5.0, centre (0, 0.9) (x -6.2..6.2, y -1.6..3.4)
#   B.src, B.src_l     clock source (rounded square with a square wave) at (-5.7, 0.25), "CLK" below
#   B.boxes[i]         small FF: VGroup(rect, tri), 0.6 x 0.8; .rect .tri; B.pos[i] its centre
#   B.branches[i]      YELLOW polyline source -> spine x=-5.0 -> row channel -> up into box i's triangle
#   B.lengths[i]       its length; B.order = indices nearest -> farthest; B.SHORT / B.LONG
#   B.tree             VGroup of all branches (overlapping on shared segments, same colour)
#   B.axis             time axis under the board (Arrow at y AXIS_Y, x -5.6 -> 1.2) + "t"; B.axis_t
#   B.tick(i)          a YELLOW tick on the axis for box i (x proportional to its route length)
#   B.tick0            DIM tick at t = 0 (the edge leaving the source)
#   B.tick_x(L)        axis x for route length L
# The board group B holds rect, src, src_l, tree, boxes (not the axis or ticks).
# =============================================================================================
BD_W, BD_H, BD_C = 12.4, 5.0, (0.0, 0.9)
FFB_W, FFB_H = 0.6, 0.8
COLS_X = (-3.8, -1.6, 0.6, 2.8, 5.0)
ROWS_Y = (2.5, 1.0, -0.5)
SPINE_X = -5.0
SRC_C = (-5.7, 0.25)
AXIS_Y = -2.7
AXIS_X0, AXIS_X1 = -5.6, 1.2
TICK_X0, TICK_X1 = -5.25, 0.6
# (col, row) slots used; the top-right corner is left free (s1 parks the shrunken path there)
BOARD_SLOTS = [(0, 0), (1, 0), (2, 0),
               (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
               (0, 2), (2, 2), (3, 2), (4, 2)]


def small_ff(center):
    r = Rectangle(width=FFB_W, height=FFB_H).set_stroke(FG, 3).set_fill(BG, 1)
    hb = FFB_H / 2
    tri = Polygon(_p(-0.11, -hb), _p(0.11, -hb), _p(0, -hb + 0.17)).set_stroke(FG, 2.5).set_fill(BG, 1)
    g = VGroup(r, tri).move_to(_p(*center))
    g.rect, g.tri = r, tri
    return g


def clock_board():
    B = VGroup()
    B.rect = RoundedRectangle(corner_radius=0.3, width=BD_W, height=BD_H).move_to(_p(*BD_C))
    B.rect.set_stroke(DIM, 2).set_fill("#181B22", 1)
    B.src = VGroup(
        RoundedRectangle(corner_radius=0.1, width=0.6, height=0.6).set_stroke(YELLOW, 3).set_fill(BG, 1),
        VMobject().set_points_as_corners([_p(-0.2, -0.1), _p(-0.08, -0.1), _p(-0.08, 0.1), _p(0.08, 0.1),
                                          _p(0.08, -0.1), _p(0.2, -0.1)]).set_stroke(YELLOW, 3),
    ).move_to(_p(*SRC_C))
    B.src_l = T("CLK", 30, YELLOW).next_to(B.src, DOWN, buff=0.15)
    s0 = B.src.get_right()
    B.boxes, B.pos, B.branches, B.lengths = [], [], [], []
    for ci, ri in BOARD_SLOTS:
        x, y = COLS_X[ci], ROWS_Y[ri]
        b = small_ff((x, y))
        ch = y - FFB_H / 2 - 0.35
        pts = [s0, _p(SPINE_X, s0[1]), _p(SPINE_X, ch), _p(x, ch), _p(x, y - FFB_H / 2)]
        br = VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 4)
        B.boxes.append(b)
        B.pos.append(_p(x, y))
        B.branches.append(br)
        B.lengths.append(sum(np.linalg.norm(pts[k + 1] - pts[k]) for k in range(len(pts) - 1)))
    B.order = sorted(range(len(B.boxes)), key=lambda i: B.lengths[i])
    B.SHORT, B.LONG = B.order[0], B.order[-1]
    B.tree = VGroup(*B.branches)
    B.add(B.rect, B.tree, *B.boxes, B.src, B.src_l)

    L_max = max(B.lengths)
    B.axis = Arrow(_p(AXIS_X0, AXIS_Y), _p(AXIS_X1, AXIS_Y), buff=0, stroke_width=3,
                   max_tip_length_to_length_ratio=0.04).set_color(DIM)
    B.axis_t = MathTex("t", font_size=40, color=DIM).next_to(B.axis, RIGHT, buff=0.15)

    def tick_x(L):
        return TICK_X0 + (TICK_X1 - TICK_X0) * L / L_max

    def tick(i, color=YELLOW):
        return Line(_p(tick_x(B.lengths[i]), AXIS_Y - 0.2), _p(tick_x(B.lengths[i]), AXIS_Y + 0.2)).set_stroke(color, 5)
    B.tick_x, B.tick = tick_x, tick
    B.tick0 = Line(_p(TICK_X0, AXIS_Y - 0.2), _p(TICK_X0, AXIS_Y + 0.2)).set_stroke(DIM, 4)
    return B


# =============================================================================================


class ClockSkewHook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(1.0)   # hold the question
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- c3.hook.1: title, the path and its two rules ---------------------------------------------
    def clip1(self):
        card = title_card("Part 3 · Clock skew")
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        P = path_diagram().scale(0.8).move_to([0, -0.9, 0])
        P.cl_l.scale(1.1)
        l1, l2 = inequalities(40)
        # ch2_s4 layout (stacked, the two >= aligned, tags left of each line), at ch2_s6's tile size
        l1.move_to(_p(0, 0.45))
        l2.move_to(_p(0, -0.45))
        l2.shift((l1[1].get_x() - l2[6].get_x()) * RIGHT)
        left = min(l1.get_left()[0], l2.get_left()[0])
        tag1, tag2 = T("set-up", 30, GOLD), T("hold", 30, GOLD)
        tag1.move_to(_p(left - 0.3, l1[1].get_y()), aligned_edge=RIGHT)
        tag2.move_to(_p(left - 0.3, l2[6].get_y()), aligned_edge=RIGHT)
        VGroup(tag1, l1, tag2, l2).move_to([0, 2.45, 0])
        self.P, self.ineq = P, (tag1, l1, tag2, l2)
        with self.say("c3.hook.1") as c:
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course, card.part, lag=0.35), run_time=1.3)  # early: title card read whole
            c.wait_until("path")
            sweep_clear(self, *during([FadeIn(P)], 0.5, 1.0), run_time=1.6)
            self.play(*appear(tag1, l1, tag2, l2, shift=None, lag=0.3), run_time=1.4)  # early: the two rules shown whole
            # {early}: set-up brightens, hold steps back
            c.wait_until("early")
            self.play(*set_alpha([tag2, l2], 0.3), FlashAround(l1, color=YELLOW, time_width=1.5), run_time=1.5)
            # {steady}: hold brightens, set-up steps back
            c.wait_until("steady")
            self.play(*set_alpha([tag2, l2], 1), *set_alpha([tag1, l1], 0.3),
                      FlashAround(l2, color=YELLOW, time_width=1.5), run_time=1.5)

    # -- c3.hook.2: one instant? the clock tree spreads the edge ----------------------------------
    def clip2(self):
        P = self.P
        tag1, l1, tag2, l2 = self.ineq
        same = T("same instant", 32, YELLOW).next_to(P.clk_bus, DOWN, buff=0.3)
        B = clock_board()
        q = T("?", 60, YELLOW).move_to([(TICK_X0 + TICK_X1) / 2, -2.0, 0])
        r1, r2 = inequalities(34)
        q1, q2 = T("?", 40, YELLOW), T("?", 40, YELLOW)
        rg1 = VGroup(r1, q1).arrange(RIGHT, buff=0.2)
        rg2 = VGroup(r2, q2).arrange(RIGHT, buff=0.2)
        VGroup(rg1, rg2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.05, -2.65, 0])
        with self.say("c3.hook.2") as c:
            # {same}: both rules back; one pulse along CLK reaches both triangles at once
            self.play(*set_alpha([tag1, l1], 1), run_time=0.8)
            c.wait_until("reaches")
            self.play(*[VShowPassingFlash(p, time_width=0.6, rate_func=linear) for p in P.clk_paths()],
                      run_time=1.2)
            c.wait_until(own_word=same)
            self.play(*flash([P.ff0.tri, P.ff1.tri]), *appear(same), run_time=1.0)

            # {board}: zoom out: the path shrinks into a corner of a big board
            c.wait_until("board")
            labels = [*P.names, P.cl_l, P.q0_l, P.d1_l, P.d0_l, P.q1_l, P.clk_l,
                      P.ff0.d_l, P.ff0.q_l, P.ff0.qb_l, P.ff1.d_l, P.ff1.q_l, P.ff1.qb_l]
            self.play(*disappear(tag1, l1, tag2, l2, same, *labels), run_time=0.8)
            for m in labels:
                for parent in (P, P.ff0, P.ff1):
                    parent.remove(m)
            self.play(FadeIn(B.rect), P.animate.scale(0.31).move_to([4.3, 2.72, 0]), run_time=1.6)
            self.bring_to_front(P)
            self.play(FadeIn(B.src), *[FadeIn(b) for b in B.boxes], *set_alpha([P], 0.45),
                      *[Create(br) for br in B.branches], run_time=2.0)
            self.play(*appear(B.src_l), run_time=0.8)

            # {edge}: the source fires; the time axis appears with its t = 0 tick
            c.wait_until("edge")
            self.play(FlashAround(B.src, color=YELLOW, time_width=1.5), *appear(B.axis, B.axis_t, B.tick0, shift=None),
                      run_time=1.4)
            # one pulse down every branch at the same speed: nearest arrives on {near}, farthest on {far}
            L = B.lengths
            t_near, t_far = c.at("near") + 0.3, c.at("far") + 0.6
            v = (L[B.LONG] - L[B.SHORT]) / (t_far - t_near)
            t0 = max(self.time, t_near - L[B.SHORT] / v)
            if t0 > self.time:
                self.wait(t0 - self.time)
            anims = []
            for i, br in enumerate(B.branches):
                arr = L[i] / v
                tw = min(0.5, 1.4 / L[i])
                pulse = br.copy().set_stroke(YELLOW, 10)
                anims.append(time_span(VShowPassingFlash(pulse, time_width=tw, rate_func=linear),
                                       0.0, arr * (1 + tw)))
                anims.append(time_span(FlashAround(B.boxes[i].rect, color=YELLOW, buff=0.06), arr, arr + 0.6))
                anims.append(time_span(B.boxes[i].rect.animate.set_stroke(YELLOW), arr, arr + 0.3))
                anims.append(time_span(FadeIn(B.tick(i)), arr, arr + 0.3))
            end = max(L[i] / v * (1 + min(0.5, 1.4 / L[i])) for i in range(len(L)))
            end = max(end, L[B.LONG] / v + 0.6)
            self.play(*anims, run_time=end)

            # {question}: a "?" over the spread; the two rules return, each with its own "?"
            c.wait_until("question")
            self.play(*appear(q), run_time=1.0)
            self.play(*appear(rg1, rg2, lag=0.4), run_time=1.4)  # early: the two rules return together with the question
