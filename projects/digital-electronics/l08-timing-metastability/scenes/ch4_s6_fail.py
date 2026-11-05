"""Chapter 4, scene 6: when the synchroniser fails. Clips c4.fail.1 – c4.fail.4.

Shots: s5's sync_circuit() + sync_timing() fade back and compact (x0.85, up 0.9); YELLOW "?" by Q;
t_res flashes, the t_su stretch flashes GOLD; the second edge slides right (T_c 5 -> 6 s5 units),
carrying t_su, t_res stretches; "slower" by T_c -> a second run: D1 stays RED past FF1's deadline,
t_su turns RED, Q goes RED halfway, FF1 outline RED, "???", caption -> circuit leaves, diagram
rises; ch1's budget bar ghost under it (t_pc/t_pd/t_su), t_pc + t_pd give way to t_res: res_bar();
the caption swaps for "fails if t_res > T_c - t_su" -> diagram leaves, bar + condition rise; s4's
model, T_c - t_su flies into the exponent: pfail_formula() boxed; caption; "longer T_c" with a thin
arrow to T0/T_c and a thick one to the exponential. The recap copies res_bar() / pfail_formula().
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
# sync_timing(): slide p. 112's timing diagram in ch1_s5's data-sheet style. s6 / recap copy it.
# =============================================================================================
WAVE_W = 4
ROW_H = 0.5
SLOPE = 0.35
GUIDE_W = 1.5
DIM_W = 3
TX0, TX1 = -4.7, 4.2             # traces end at 4.2: the old/new tags get the lane to their right
E1, E2 = -2.4, 2.6               # the two rising edges (one period apart)
CLK_EDGES = [E1, 0.1, E2]
XS = 1.6                         # D1 resolved (the split)
QX = (3.3, 3.6)                  # Q's crossover, t_pc after E2
TROW = {"CLK": 0.0, "D1": -0.95, "Q": -1.95}
DIM_Y = -2.5
TC_Y = 0.4                       # T_c sits on the CLK trace, 0.42 clear of the circuit's bus
LAB_X = -5.45


def clock_wave(x0, x1, y, edges, h=ROW_H, slope=SLOPE, color=YELLOW):
    lo, hi = y - h / 2, y + h / 2
    level = lo
    pts = [_p(x0, level)]
    for xc in edges:
        other = hi if level == lo else lo
        pts += [_p(xc - slope / 2, level), _p(xc + slope / 2, other)]
        level = other
    pts.append(_p(x1, level))
    return VMobject().set_points_as_corners(pts).set_stroke(color, WAVE_W)


def pair(xa, xb, y, color, h=ROW_H):
    return VGroup(Line(_p(xa, y + h / 2), _p(xb, y + h / 2)),
                  Line(_p(xa, y - h / 2), _p(xb, y - h / 2))).set_stroke(color, WAVE_W)


def guide(x, y_top, y_bot):
    return Line(_p(x, y_top), _p(x, y_bot)).set_stroke(DIM, GUIDE_W)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=40):
    arr = DoubleArrow(_p(xa, y), _p(xb, y), buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.12)
    g = VGroup(arr, lab)
    g.arr, g.lab = arr, lab
    return g


def sync_timing():
    D = VGroup()
    yc, yd, yq = TROW["CLK"], TROW["D1"], TROW["Q"]
    h2 = ROW_H / 2
    D.clk = clock_wave(TX0, TX1, yc, CLK_EDGES)
    D.labs = [T("CLK", 32, YELLOW).move_to(_p(LAB_X, yc)),
              MathTex("D_1", font_size=40, color=TEAL).move_to(_p(LAB_X, yd)),
              MathTex("Q", font_size=40, color=GREEN).move_to(_p(LAB_X, yq))]
    # D1: 0 or 1 -> converges (RED) at E1 -> RED midline -> diverges -> resolved TEAL pair
    D.d1_pre = pair(TX0, E1, yd, TEAL)
    c1 = E1 + 0.3
    D.d1_conv = VGroup(Line(_p(E1, yd + h2), _p(c1, yd)), Line(_p(E1, yd - h2), _p(c1, yd))).set_stroke(RED, WAVE_W)
    D.mid_x = -0.4
    D.d1_red1 = Line(_p(c1, yd), _p(D.mid_x, yd)).set_stroke(RED, WAVE_W)
    D.d1_red2 = Line(_p(D.mid_x, yd), _p(XS - 0.3, yd)).set_stroke(RED, WAVE_W)
    D.d1_div = VGroup(Line(_p(XS - 0.3, yd), _p(XS, yd + h2)), Line(_p(XS - 0.3, yd), _p(XS, yd - h2))).set_stroke(TEAL, WAVE_W)
    D.d1_post = pair(XS, TX1, yd, TEAL)
    # Q: old value, then a clean X t_pc after E2
    D.q_pre = pair(TX0, QX[0], yq, GREEN)
    D.q_x = VGroup(Line(_p(QX[0], yq + h2), _p(QX[1], yq - h2)),
                   Line(_p(QX[0], yq - h2), _p(QX[1], yq + h2))).set_stroke(GREEN, WAVE_W)
    D.q_post = pair(QX[1], TX1, yq, GREEN)
    # the rising edges (for flashes)
    D.edge1 = Line(_p(E1 - SLOPE / 2, yc - h2), _p(E1 + SLOPE / 2, yc + h2))
    D.edge2 = Line(_p(E2 - SLOPE / 2, yc - h2), _p(E2 + SLOPE / 2, yc + h2))
    # dimensions
    D.tc = dim_arrow(E1, E2, TC_Y, YELLOW, "T_c")
    D.tc.lab.move_to(_p(E2 + 0.42, TC_Y + 0.22))       # above-right of the arrow, clear of the high CLK level
    D.tcx = VGroup(guide(E1, yc + h2 + 0.05, TC_Y + 0.14), guide(E2, yc + h2 + 0.05, TC_Y + 0.14))
    top, bot = yc + h2 + 0.05, DIM_Y - 0.12
    D.g1, D.gs, D.g2 = guide(E1, top, bot), guide(XS, yd, bot), guide(E2, top, bot)
    D.gq = guide(QX[0], yq, bot)
    D.tres = dim_arrow(E1, XS, DIM_Y, FG, "t_{res}", label_dir=DOWN)
    D.tsu = dim_arrow(XS, E2, DIM_Y, GOLD, "t_{su}", label_dir=DOWN)
    D.tpc = dim_arrow(E2, QX[0], DIM_Y, PINK, "t_{pc}", label_dir=DOWN)
    D.all = [D.clk, *D.labs, D.d1_pre, D.d1_conv, D.d1_red1, D.d1_red2, D.d1_div, D.d1_post,
             D.q_pre, D.q_x, D.q_post, D.tc, D.tcx, D.g1, D.gs, D.g2, D.gq, D.tres, D.tsu, D.tpc]
    D.add(*D.all)
    return D
# =============================================================================================


# ---- ch4_s5_synchroniser.py grow_dim / sweep_in / pulse, copied ----
def grow_dim(arr):
    """ch1_s5's grow_dim: a DoubleArrow grown from its centre at true tip size."""
    start, end = arr.get_start(), arr.get_end()
    mid, half = (start + end) / 2, (end - start) / 2
    final = arr.copy()

    def upd(m, a):
        if a >= 1:
            m.become(final)
            return
        if a * np.linalg.norm(end - start) < 0.4:
            m.become(final).set_opacity(0)
            return
        m.become(DoubleArrow(mid - a * half, mid + a * half, buff=0, stroke_width=DIM_W,
                             tip_length=0.16, max_tip_length_to_length_ratio=0.4,
                             color=final.get_color()))

    return UpdateFromAlphaFunc(arr, upd, rate_func=smooth)


def sweep_in(group, x0, x1):
    """ch1_s5's sweep_in: draw every line of `group` left to right, as a pen from x0 to x1."""
    leaves = group.family_members_with_points()
    origs = [m.copy() for m in leaves]

    def upd(_, a):
        X = x0 + a * (x1 - x0)
        for leaf, orig in zip(leaves, origs):
            lx0, lx1 = orig.get_left()[0], orig.get_right()[0]
            if lx1 - lx0 < 1e-6:
                frac = 1.0 if X >= lx0 else 0.0
            else:
                frac = min(1.0, max(0.0, (X - lx0) / (lx1 - lx0)))
            if a >= 1:
                frac = 1.0
            leaf.pointwise_become_partial(orig, 0, frac)
            leaf.set_stroke(opacity=orig.get_stroke_opacity() if frac * (lx1 - lx0) > 0.15 or frac >= 1
                            else 0)

    return UpdateFromAlphaFunc(group, upd, rate_func=linear)


def pulse(line, color=YELLOW, width=9):
    """A bright bump running along a wire (a copy, removed at the end)."""
    return VShowPassingFlash(line.copy().set_stroke(color, width), time_width=0.5)


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
# s6's own layout: s5's circuit + diagram compacted (scale K about ORIGIN, then DY up)
# =============================================================================================
K = 0.85
DY = 0.9
DX = 1.0                         # how far the second edge moves (s5 units): T_c 5.0 -> 6.0
E2N = E2 + DX
TXE = 5.8                        # s6 runs the traces further right (s5 stops at 4.2 for its tags)
XL = 4.2                         # the failing run: D1 resolves only after the second edge
UP2 = 1.9                        # clip 3: the diagram rises to the top once the circuit leaves


def fit(m):
    return m.scale(K, about_point=ORIGIN).shift(DY * UP)


def fx(x):
    return K * x


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


def fail_condition():
    """'fails if t_res > T_c - t_su' (t_res FG, '>' RED, T_c YELLOW, t_su GOLD). .b = 'T_c - t_su'."""
    w = T("fails if", 40)
    a = MathTex(r"t_{res} >", font_size=50)
    a[0][4].set_color(RED)
    b = color_tc_tsu(MathTex(r"T_c - t_{su}", font_size=50))
    a.next_to(w, RIGHT, buff=0.3)
    b.next_to(a, RIGHT, buff=0.22)
    b.shift((a[0][4].get_y() - b[0][2].get_y()) * UP)
    w.align_to(a[0][0], DOWN)
    g = VGroup(w, a, b)
    g.w, g.a, g.b = w, a, b
    return g
# =============================================================================================


class SynchroniserFails(NarratedScene):
    def construct(self):
        C = sync_circuit()
        D = sync_timing()
        circ = list(C.all)
        diag = [D.clk, *D.labs, D.d1_pre, D.d1_conv, D.d1_red1, D.d1_red2, D.d1_div, D.d1_post,
                D.q_pre, D.q_x, D.q_post, D.tcx[0], D.tcx[1], D.g1, D.gs, D.g2, D.gq,
                D.tc.arr, D.tc.lab, D.tres.arr, D.tres.lab, D.tsu.arr, D.tsu.lab, D.tpc.arr, D.tpc.lab]
        yd, yq = TROW["D1"], TROW["Q"]
        h2 = ROW_H / 2

        # ---------------------------------------------------------------- clip 1
        with self.say("c4.fail.1") as c:
            self.play(*[FadeIn(m) for m in circ + diag], run_time=0.8)
            qpos = K * C.q_l.get_center() + DY * UP
            qmark = T("?", 44, YELLOW).move_to(qpos + (K * C.q_l.width / 2 + 0.3) * RIGHT)
            small = [*C.names, C.clk_l, D.labs[0]]      # keep these >= 28 after compacting
            self.play(*during([m.animate.scale(K, about_point=ORIGIN).shift(DY * UP).scale(1.13 if any(m is x for x in small) else 1)
                               for m in circ + diag], 0, 0.65),
                      *during(appear(qmark), 0.65, 1), run_time=min(2.2, c.until("wait")))

            c.wait_until("wait")
            self.play(FlashAround(D.tres, color=FG, run_time=1.4, time_width=1.5),
                      D.tres.arr.animate.set_stroke(width=5), run_time=1.4)
            c.wait_until("must still")
            stretch = Line(_p(XS, yd + h2), _p(E2, yd - h2))
            fit(stretch)
            self.play(FlashAround(VGroup(D.tsu, stretch), color=GOLD, run_time=1.5, time_width=1.5),
                      D.tres.arr.animate.set_stroke(width=DIM_W), run_time=1.5)   # t_res's beat is over
            c.wait_until("next edge")
            self.play(FlashAround(fit(D.edge2.copy()), run_time=1.2, time_width=1.5), run_time=1.2)

            # {later}: the second edge slides right, carrying t_su; t_res stretches
            c.wait_until("later")
            d = fx(DX) * RIGHT
            clk_n = fit(clock_wave(TX0, TXE, TROW["CLK"], [E1, (E1 + E2N) / 2, E2N]))
            tc_n = fit(dim_arrow(E1, E2N, TC_Y, YELLOW, "T_c")).arr
            tres_n = fit(dim_arrow(E1, XS + DX, DIM_Y, FG, "t_{res}", label_dir=DOWN)).arr
            tres_n.set_stroke(width=D.tres.arr.get_stroke_width())
            qpre_n = fit(pair(TX0, QX[0] + DX, yq, GREEN))
            qpost_n = fit(pair(QX[1] + DX, TXE, yq, GREEN))
            d1post_n = fit(pair(XS, TXE, yd, TEAL))
            self.play(Transform(D.clk, clk_n), Transform(D.tc.arr, tc_n), Transform(D.tres.arr, tres_n),
                      Transform(D.q_pre, qpre_n), Transform(D.q_post, qpost_n), Transform(D.d1_post, d1post_n),
                      D.tc.lab.animate.shift(d), D.tres.lab.animate.shift(d / 2),
                      *[m.animate.shift(d) for m in (D.g2, D.tcx[1], D.gs, D.tsu.arr, D.tsu.lab, D.q_x, D.gq,
                                                     D.tpc.arr, D.tpc.lab)],
                      run_time=min(2.2, c.until("slower")))
            slower = T("slower", 36, YELLOW).next_to(D.tc.lab, RIGHT, buff=0.35)
            slower.align_to(D.tc.lab, DOWN)
            c.wait_until("more slowly")
            self.play(*appear(slower), run_time=1.0)

        # ---------------------------------------------------------------- clip 2
        with self.say("c4.fail.2") as c:
            gone = [D.d1_red2, D.d1_div, D.d1_post, D.q_x, D.q_post, D.gq, D.tpc.arr, D.tpc.lab]
            self.play(*disappear(*gone, qmark), *recolor(C.d1_wires, RED),
                      C.d1_l.animate.set_color(RED), run_time=1.2)
            for m in gone:
                diag.remove(m)
            c.wait_until("cue")
            self.play(FlashAround(C.q_l, color=GREEN, run_time=1.4, time_width=1.5), run_time=1.4)

            # {late}: D1 stays RED past FF1's deadline
            c.wait_until("late")
            red_ext = Line(_p(D.mid_x, yd), _p(XL - 0.3, yd)).set_stroke(RED, WAVE_W)
            div_l = VGroup(Line(_p(XL - 0.3, yd), _p(XL, yd + h2)),
                           Line(_p(XL - 0.3, yd), _p(XL, yd - h2))).set_stroke(TEAL, WAVE_W)
            post_l = pair(XL, TXE, yd, TEAL)
            late = [fit(red_ext), fit(div_l), fit(post_l)]
            self.add(*late)
            self.play(sweep_in(VGroup(*late), fx(D.mid_x), fx(TXE)), *during(disappear(slower), 0, 0.3),
                      run_time=min(3.2, c.until("deadline")))
            diag += late
            c.wait_until("deadline")
            self.play(D.tsu.arr.animate.set_color(RED),
                      FlashAround(D.gs, color=RED, run_time=1.3, time_width=1.5), run_time=1.3)

            # {broken}: Q goes RED halfway, FF1's outline RED
            c.wait_until("broken")
            q0 = QX[0] + DX
            q_conv = VGroup(Line(_p(q0, yq + h2), _p(q0 + 0.3, yq)),
                            Line(_p(q0, yq - h2), _p(q0 + 0.3, yq))).set_stroke(RED, WAVE_W)
            q_mid = Line(_p(q0 + 0.3, yq), _p(TXE, yq)).set_stroke(RED, WAVE_W)
            qbad = [fit(q_conv), fit(q_mid)]
            self.add(*qbad)
            self.play(sweep_in(VGroup(*qbad), fx(q0) - 0.01, fx(TXE)), restyle(C.ff1.box, outline=RED),
                      C.ff1.q_w.animate.set_stroke(RED), C.q_l.animate.set_color(RED), run_time=1.6)
            diag += qbad
            qq = T("???", 36, RED).next_to(qbad[1], RIGHT, buff=0.3)
            cap = T("synchroniser fails: Q metastable", 36, t2c={"Q metastable": RED}).move_to(_p(0, -2.65))
            c.wait_until("undefined")
            self.play(*appear(qq, cap, lag=0.35), run_time=min(1.3, c.until(floor=0.8)))
            diag.append(qq)

        # ---------------------------------------------------------------- clip 3
        with self.say("c4.fail.3") as c:
            gsegs = [("t_{pc}", PINK, RB_TOT * 1.2 / 7), ("t_{pd}", PURPLE, RB_TOT * 5.1 / 7),
                     ("t_{su}", GOLD, RB_TOT * 0.7 / 7)]
            ghost = budget_bar(gsegs, RB_TOT, x0=RB_X0, y=RB_Y)
            for s in ghost.segs:
                s.set_fill(opacity=0.4)
            for s in ghost.syms:
                s.set_opacity(0.55)
            gparts = [*ghost.segs, ghost.outline, ghost.tc, *ghost.syms]
            self.play(*during(disappear(*circ), 0, 0.4),
                      *during([m.animate.shift(UP2 * UP) for m in diag], 0.3, 0.8),
                      *during([FadeIn(m) for m in gparts], 0.7, 1), run_time=min(2.2, c.until("slot")))

            FB = res_bar()
            c.wait_until("the resolution time")
            self.play(*during(disappear(ghost.segs[0], ghost.segs[1], ghost.syms[0], ghost.syms[1]), 0, 0.4),
                      *during([GrowFromEdge(FB.segs[0], LEFT), ReplacementTransform(ghost.segs[2], FB.segs[1]),
                               ReplacementTransform(ghost.syms[2], FB.syms[1])], 0.3, 0.85),
                      *during(appear(FB.syms[0], shift=None), 0.75, 1), run_time=2.0)
            self.remove(ghost.outline, ghost.tc, FB.segs[0], FB.segs[1], FB.syms[0], FB.syms[1])
            self.add(FB)

            c.wait_until("sits where")
            self.play(FlashAround(FB.segs[0], color=FG, run_time=1.5, time_width=1.5),
                      FlashAround(D.tres, color=FG, run_time=1.5, time_width=1.5), run_time=1.5)

            cond = fail_condition().move_to(_p(RB_X0 + RB_TOT / 2, -2.6))
            c.wait_until(own_word=cond.w)
            self.play(*swap(cap, cond), run_time=1.3)

        # ---------------------------------------------------------------- clip 4
        with self.say("c4.fail.4") as c:
            F = pfail_formula().move_to(_p(0.3, -0.4))
            O = model_formula().move_to(F.main)
            self.play(*during(disappear(*diag), 0, 0.35),
                      *during([FB.animate.shift(3.9 * UP), cond.animate.shift(3.95 * UP)], 0.35, 0.8),
                      *during(appear(O, shift=None), 0.82, 1), run_time=min(2.1, c.until("For the time")))

            c.wait_until("For the time")
            self.play(FlashAround(O.t, run_time=1.3, time_width=1.5),
                      FlashAround(cond.b, run_time=1.3, time_width=1.5), run_time=1.3)
            c.wait_until("clock period")
            self.play(*during(edit(O, F.main), 0, 0.55), *during(fly(cond.b, F.ins), 0.5, 1),
                      run_time=min(2.6, c.until("pfail")))

            pcap = T("probability of failure for a single input change", 32).next_to(F.box, DOWN, buff=0.4)
            c.wait_until("pfail")
            self.play(FadeIn(F.box, scale=1.08), run_time=1.0)   # frames the whole formula from the start
            c.wait_until(own_word=pcap)
            self.play(*appear(pcap), run_time=1.0)

            c.wait_until("It's")
            self.play(FlashAround(F.frac, run_time=1.4, time_width=1.5), run_time=1.4)
            c.wait_until("times the exponential")
            self.play(FlashAround(F.expo, run_time=1.6, time_width=1.5), run_time=1.6)

            # {twice}
            tag = VGroup(T("longer", 34), MathTex("T_c", font_size=44, color=YELLOW)).arrange(RIGHT, buff=0.15)
            tag[1].align_to(tag[0], DOWN)
            tag.move_to(_p(0.3, -3.25))
            yb = F.box.get_bottom()[1] - 0.08
            thin = Arrow(tag.get_top() + 0.35 * LEFT, [F.frac.get_x(), yb, 0], buff=0.1,
                         stroke_width=3, tip_length=0.2, color=FG)
            thick = Arrow(tag.get_top() + 0.35 * RIGHT, [F.expo.get_x(), yb, 0], buff=0.1,
                          stroke_width=10, max_stroke_width_to_length_ratio=20, tip_length=0.34, color=FG)
            fewer = T("fewer bad times", 32).next_to(thin.get_center(), LEFT, buff=0.35)
            more = T("more time to settle:", 32).next_to(thick.get_center(), RIGHT, buff=0.45)
            big = T("the big effect", 32, GREEN).next_to(more, DOWN, buff=0.15, aligned_edge=LEFT)
            c.wait_until(own_word=tag[0])
            self.play(*during(disappear(pcap), 0, 0.45), *during(appear(tag), 0.5, 1), run_time=1.2)
            c.wait_until("Bad times")
            self.play(GrowArrow(thin), *during(appear(fewer), 0.4, 1), run_time=1.3)
            c.wait_until("more time")
            self.play(GrowArrow(thick), *during(appear(more), 0.4, 1), run_time=1.4)
            c.wait_until(own_word=big)
            self.play(*appear(big), FlashAround(F.expo, color=GREEN, run_time=1.5, time_width=1.5),
                      run_time=1.5)

        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
