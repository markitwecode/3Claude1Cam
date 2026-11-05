"""Chapter 3, scene 5: skew and hold (p. 109), then both fences slide. Clips c3.hold.1 – c3.hold.4.

Copied (not imported): make_ff/path_diagram/split_path, the timing-diagram kit and skew_traces() from
ch3_s3_skewsetup.py (skew_traces gains .d1_x0, D1's first crossover); budget_bar + tc_arrow from
ch2_s5_contamination.py.

Shared with s6 / the recap: skew_fences(skew=0.0, ...) (between the rulers below) is ch2_s5's
hold_budget() with both fences moved earlier by `skew` (a fraction of the period): hold fence at
(hold - skew), deadline at (1 - su - skew), the GOLD t_su segment just right of the deadline, a TEAL
t_skew segment filling the last `skew` of the bar, and two TEAL t_skew arrows (old -> new place)
under the T_c arrow.
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
# make_ff + path_diagram, copied from ch1_s4_path.py; split_path() is ch3's split-clock version
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


P_FF_X = (-4.4, 4.4)
P_FF_Y = 0.5
P_PIN = P_FF_Y + PIN_Y                       # 1.1
P_BUS = P_FF_Y - BOX_H / 2 - EN_WIRE         # -1.8
P_BUS_X0 = -5.6
P_CL_W, P_CL_H = 3.4, 1.6


def path_diagram():
    P = VGroup()
    ffs = []
    for x in P_FF_X:
        f = make_ff(_p(x, P_FF_Y))
        f.remove(f.clk_w)
        ffs.append(f)
    P.ff0, P.ff1 = ffs
    P.names = [T(f"FF{i}", 36, FG).next_to(f.box, UP, buff=0.2) for i, f in enumerate(ffs)]
    x_q0 = P_FF_X[0] + BOX_W / 2 + WIRE
    x_d1 = P_FF_X[1] - BOX_W / 2 - WIRE
    P.cl = Rectangle(width=P_CL_W, height=P_CL_H).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(0, P_PIN))
    P.cl_l = VGroup(T("Combinational", 32, BLUE), T("Logic (CL)", 32, BLUE)).arrange(DOWN, buff=0.12).move_to(P.cl)
    P.q0_w = Line(_p(x_q0, P_PIN), _p(-P_CL_W / 2, P_PIN)).set_stroke(GREEN, 5)
    P.d1_w = Line(_p(P_CL_W / 2, P_PIN), _p(x_d1, P_PIN)).set_stroke(BLUE, 5)
    P.q0_l = MathTex("Q_0", font_size=40, color=GREEN).next_to(_p(x_q0, P_PIN), UP, buff=0.15)
    P.d1_l = MathTex("D_1", font_size=40, color=BLUE).next_to(_p(x_d1, P_PIN), UP, buff=0.15)
    P.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(P.ff0.d_w, LEFT, buff=0.12)
    P.q1_l = MathTex("Q_1", font_size=40, color=GREEN).next_to(P.ff1.q_w, RIGHT, buff=0.12)
    P.clk_bus = Line(_p(P_BUS_X0, P_BUS), _p(P_FF_X[1], P_BUS)).set_stroke(YELLOW, 5)
    P.clk_dot = Dot(_p(P_FF_X[0], P_BUS), radius=0.08, color=YELLOW)
    P.clk_l = T("CLK", 34, YELLOW).next_to(_p(P_BUS_X0, P_BUS), LEFT, buff=0.15)
    P.clk_br0, P.clk_br1 = ffs[0].clk_w, ffs[1].clk_w
    P.all = [P.ff0, P.ff1, *P.names, P.cl, P.cl_l, P.q0_w, P.q0_l, P.d1_w, P.d1_l, P.d0_l, P.q1_l,
             P.clk_bus, P.clk_dot, P.clk_l, P.clk_br0, P.clk_br1]
    P.add(*P.all)
    return P


SRC_X, SRC_R = 6.25, 0.3          # the clock source, on the old bus row (y -1.8)
LONG_Y = -2.55                    # the long branch's bottom run
TRI_Y = P_FF_Y - BOX_H / 2 - 0.02  # where a branch meets its triangle (-0.82)
CLK1_OP = 0.55                    # CLK1 is drawn a little dimmer for the rest of the chapter


def split_path():
    """ch1_s4's path with the clock split (p. 107): a source at the right, a short branch to FF1
    (.clk_br1, dimmer) and a long one round to FF0 (.clk_br0). Parts: as path_diagram() minus
    .clk_bus .clk_dot .clk_l, plus .src .clk_br0 .clk_br1 .clk0_l .clk1_l; .all lists them.
    Spans x -6.6 … 6.55, y -3.05 … 2.25 at full size."""
    P = path_diagram()
    P.remove(P.clk_bus, P.clk_dot, P.clk_l, P.clk_br0, P.clk_br1)
    ring = Circle(radius=SRC_R).set_stroke(YELLOW, 4).set_fill(BG, 1)
    sq = VMobject().set_points_as_corners([_p(-0.17, -0.08), _p(-0.08, -0.08), _p(-0.08, 0.08),
                                           _p(0.04, 0.08), _p(0.04, -0.08), _p(0.17, -0.08)])
    sq.set_stroke(YELLOW, 3)
    P.src = VGroup(ring, sq).move_to(_p(SRC_X, P_BUS))
    x0, x1 = P_FF_X
    P.clk_br1 = VMobject().set_points_as_corners([_p(SRC_X - SRC_R, P_BUS), _p(x1, P_BUS), _p(x1, TRI_Y)])
    P.clk_br1.set_stroke(YELLOW, 5, opacity=CLK1_OP)
    P.clk_br0 = VMobject().set_points_as_corners([_p(SRC_X, P_BUS - SRC_R), _p(SRC_X, LONG_Y),
                                                  _p(x0, LONG_Y), _p(x0, TRI_Y)])
    P.clk_br0.set_stroke(YELLOW, 5)
    P.clk0_l = T("CLK0", 34, YELLOW).next_to(_p(-1.6, LONG_Y), DOWN, buff=0.15)
    P.clk1_l = T("CLK1", 34, YELLOW).next_to(_p((x1 + SRC_X - SRC_R) / 2 + 0.05, P_BUS), UP, buff=0.15)
    P.clk1_l.set_opacity(0.7)
    P.all = [P.ff0, P.ff1, *P.names, P.cl, P.cl_l, P.q0_w, P.q0_l, P.d1_w, P.d1_l, P.d0_l, P.q1_l,
             P.clk_br0, P.clk_br1, P.src, P.clk0_l, P.clk1_l]
    P.add(P.clk_br0, P.clk_br1, P.src, P.clk0_l, P.clk1_l)

    def clk_paths(width=10):
        return [br.copy().set_stroke(YELLOW, width, opacity=1) for br in (P.clk_br0, P.clk_br1)]
    P.clk_paths = clk_paths
    return P
# =============================================================================================


# =============================================================================================
# Data-sheet timing-diagram kit, copied from ch1_s5_datasheet.py (+ its grow_dim)
# =============================================================================================
WAVE_W = 4
ROW_H = 0.8
SLOPE = 0.35
GUIDE_W = 1.5
DIM_W = 3


def clock_wave(x0, x1, y, edges, h=ROW_H, slope=SLOPE, color=YELLOW, start_low=True):
    lo, hi = y - h / 2, y + h / 2
    level = lo if start_low else hi
    pts = [np.array([x0, level, 0])]
    for xc in edges:
        other = hi if level == lo else lo
        pts.append(np.array([xc - slope / 2, level, 0]))
        pts.append(np.array([xc + slope / 2, other, 0]))
        level = other
    pts.append(np.array([x1, level, 0]))
    wave = VMobject().set_points_as_corners(pts)
    wave.set_stroke(color, WAVE_W)
    return wave


def bus(x0, x1, y, crossings, h=ROW_H, color=BLUE):
    lo, hi = y - h / 2, y + h / 2
    g = VGroup()
    g.runs, g.xs = [], []
    cur = x0
    for a, b in list(crossings) + [(x1, x1)]:
        if a - cur > 1e-3:
            run = VGroup(Line([cur, hi, 0], [a, hi, 0]), Line([cur, lo, 0], [a, lo, 0]))
            run.set_stroke(color, WAVE_W)
            g.add(run)
            g.runs.append(run)
        if b - a > 1e-3:
            x = VGroup(Line([a, hi, 0], [b, lo, 0]), Line([a, lo, 0], [b, hi, 0]))
            x.set_stroke(color, WAVE_W)
            g.add(x)
            g.xs.append(x)
        cur = b
    return g


def hatch(a, b, n):
    w = (b - a) / n
    return [(a + i * w, a + (i + 1) * w) for i in range(n)]


def guide(x, y_top, y_bot):
    return Line([x, y_top, 0], [x, y_bot, 0]).set_stroke(DIM, GUIDE_W)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=44):
    arr = DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.15)
    return VGroup(arr, lab)


def sweep_in(group, x0, x1):
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

    return UpdateFromAlphaFunc(group, upd)


def grow_dim(arr):
    start, end = arr.get_start(), arr.get_end()
    mid, half = (start + end) / 2, (end - start) / 2
    final = arr.copy()
    min_len = 0.4

    def upd(m, a):
        if a >= 1:
            m.become(final)
            return
        L = a * np.linalg.norm(end - start)
        if L < min_len:
            m.become(final).set_opacity(0)
            return
        m.become(DoubleArrow(mid - a * half, mid + a * half, buff=0, stroke_width=DIM_W,
                             tip_length=0.16, max_tip_length_to_length_ratio=0.4,
                             color=final.get_color()))

    return UpdateFromAlphaFunc(arr, upd, rate_func=smooth)
# =============================================================================================


# =============================================================================================
# p. 108's four traces (CLK1 ahead of CLK0 by t_skew), worst case: D1 settles exactly t_su
# before CLK1's edge. Built at full size; s5 redraws it for p. 109.
# =============================================================================================
TR_X0, TR_X1 = -5.0, 6.6            # trace extent
TR_LAB_X = -6.0                     # row labels' centres
Y_C0, Y_Q0, Y_D1, Y_C1 = 2.0, 0.85, -0.3, -2.05
Y_TC = 2.75                         # T_c arrow (label above)
Y_ARR = -1.35                       # t_pc / t_pd / t_su arrow row (labels above)
Y_SK = -2.75                        # t_skew arrows (labels below)
G_TOP, G_BOT = 2.95, -2.9           # full-height guides at CLK0's rising edges
T_PC, T_PD, T_SU, T_SK = 1.2, 4.2, 0.8, 1.0
E1 = -1.4                           # CLK0's first rising edge
TC = T_PC + T_PD + T_SU + T_SK      # 7.2: the four pieces exactly fill the period
E2 = E1 + TC                        # 5.8
FALL = E1 + TC / 2                  # 2.2
XQ = E1 + T_PC                      # -0.2  Q0's crossover centre
XS = XQ + T_PD                      # 4.0   D1 settled (end of its last X)
K1, K2 = E1 - T_SK, E2 - T_SK       # -2.4, 4.8  CLK1's rising edges
D1_X = hatch(XQ + 0.5, XS - 0.6, 4) + [(XS - 0.4, XS)]   # hatched run, then the last crossover


def edge_line(xc, y, color=YELLOW, width=WAVE_W, opacity=1.0):
    """A rising edge of a clock row, as its own line (to brighten / dim one edge)."""
    return Line(_p(xc - SLOPE / 2, y - ROW_H / 2), _p(xc + SLOPE / 2, y + ROW_H / 2)).set_stroke(
        color, width, opacity=opacity)


def skew_traces(arr_size=40):
    """Returns an object with the diagram's parts (none added to anything):
      .labs [CLK0, Q0, D1, CLK1]   T 40 / MathTex 48 at x TR_LAB_X
      .clk0 .clk1                  clock_wave rows (CLK1 opacity CLK1_OP, edges shifted by -T_SK)
      .q0                          GREEN bus, one X at XQ;   .d1a .d1b  BLUE bus split before the last X
      .g_e1 .g_e2                  full-height guides at E1, E2;  .g_k1 .g_k2 short guides under CLK1
      .g_q .g_s                    guides at XQ and XS down to the arrow row
      .tc                          YELLOW T_c dim_arrow (E1..E2, y Y_TC, label up, 44)
      .sk1 .sk2                    TEAL t_skew arrows (K..E, y Y_SK, labels down)
      .tpc .tpd .tsu               PINK / PURPLE / GOLD arrows on the row Y_ARR, labels up"""
    D = type("Traces", (), {})()
    D.labs = [T("CLK0", 40, YELLOW).move_to(_p(TR_LAB_X, Y_C0)),
              MathTex("Q_0", font_size=48, color=GREEN).move_to(_p(TR_LAB_X, Y_Q0)),
              MathTex("D_1", font_size=48, color=BLUE).move_to(_p(TR_LAB_X, Y_D1)),
              T("CLK1", 40, YELLOW).move_to(_p(TR_LAB_X, Y_C1)).set_opacity(0.7)]
    D.clk0 = clock_wave(TR_X0, TR_X1, Y_C0, [E1, FALL, E2])
    D.clk1 = clock_wave(TR_X0, TR_X1, Y_C1, [K1, FALL - T_SK, K2]).set_stroke(opacity=CLK1_OP)
    D.q0 = bus(TR_X0, TR_X1, Y_Q0, [(XQ - 0.2, XQ + 0.2)], color=GREEN)
    d1 = bus(TR_X0, TR_X1, Y_D1, D1_X, color=BLUE)
    D.d1a = VGroup(*[m for m in d1 if m.get_left()[0] < XS - 0.45])
    D.d1b = VGroup(*[m for m in d1 if m.get_left()[0] >= XS - 0.45])
    D.last_x = d1.xs[-1]
    D.d1_x0 = d1.xs[0]
    D.g_e1, D.g_e2 = guide(E1, G_TOP, G_BOT), guide(E2, G_TOP, G_BOT)
    lo1 = Y_C1 - ROW_H / 2
    D.g_k1, D.g_k2 = guide(K1, lo1, G_BOT), guide(K2, lo1, G_BOT)
    D.g_q = guide(XQ, Y_Q0, Y_ARR - 0.15)
    D.g_s = guide(XS, Y_D1, Y_ARR - 0.15)
    D.tc = dim_arrow(E1, E2, Y_TC, YELLOW, "T_c")
    D.sk1 = dim_arrow(K1, E1, Y_SK, TEAL, "t_{skew}", label_dir=DOWN, size=arr_size)
    D.sk2 = dim_arrow(K2, E2, Y_SK, TEAL, "t_{skew}", label_dir=DOWN, size=arr_size)
    D.tpc = dim_arrow(E1, XQ, Y_ARR, PINK, "t_{pc}", size=arr_size)
    D.tpd = dim_arrow(XQ, XS, Y_ARR, PURPLE, "t_{pd}", size=arr_size)
    D.tsu = dim_arrow(XS, K2, Y_ARR, GOLD, "t_{su}", size=arr_size)
    return D
# =============================================================================================




# =============================================================================================
# THE lecture's budget bar (copied from ch2_s1_hook.py, which copied ch1_s6_setup.py verbatim)
# =============================================================================================
BAR_H = 0.5
BAR_FILL = 0.85
BAR_OUT_W = 3


def budget_bar(segs, total, x0=-3.3, y=0.0, tc_tex="T_c", syms=True, nums=None,
               sym_size=40, num_size=34):
    """One clock period as a budget (ch1_s6's helper, unchanged)."""
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


def tc_arrow(xa, xb, y):
    """ch1_s6's YELLOW T_c dimension arrow, label-free: the bar's T_c names it."""
    return DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.4, color=YELLOW)

# =============================================================================================


# =============================================================================================
# The fence picture at any skew (ch2_s5's hold_budget, both fences moved earlier by `skew`)
# =============================================================================================
FB_L = 7.0          # one CLK0 period
FB_X0 = -3.5        # bar x -3.5 .. 3.5
FB_Y = -0.8         # bar centre row


def skew_fences(skew=0.0, x0=FB_X0, y=FB_Y, L=FB_L, hold=0.3, su=0.1, lo=0.4, hi=0.8, sk_size=32):
    """One CLK0 period with both fences, measured from CLK0's edge, when CLK1 is `skew` (fraction of
    the period) ahead. Parts as ch2_s5's hold_budget: .bar (.outline .tc) .su (GOLD t_su segment)
    .arrow (T_c, 0.35 under the bar) .edges .fence (hold, at hold-skew) .fence_l .deadline (at
    1-su-skew) .su_l .stretch (.box .hatch, lo..hi) .may_l; plus, when skew > 0, .skseg (TEAL, the
    last `skew` of the bar) and .sk_arrows (two TEAL t_skew DoubleArrows, old -> new fence place,
    0.45 under the T_c arrow) with .sk_labels (MathTex sk_size, below them). xs: .xf .xd .xa .xb."""
    H = VGroup()
    H.bar = budget_bar([("t_{su}", GOLD, su * L)], L, x0=x0, y=y, syms=False)
    seg = H.bar.segs[0].shift((1 - su - skew) * L * RIGHT)
    H.su = seg
    H.arrow = tc_arrow(x0, x0 + L, y - BAR_H / 2 - 0.35)
    H.edges = VGroup(*[Arrow([x, y + 0.3, 0], [x, y + 1.0, 0], buff=0, stroke_width=4, tip_length=0.2,
                             max_tip_length_to_length_ratio=0.4, color=YELLOW) for x in (x0, x0 + L)])
    xf, xd = x0 + (hold - skew) * L, x0 + (1 - su - skew) * L
    H.fence = Line([xf, y - 0.45, 0], [xf, y + 0.45, 0]).set_stroke(GOLD, 7).set_z_index(2)
    H.deadline = Line([xd, y - 0.45, 0], [xd, y + 0.45, 0]).set_stroke(GOLD, 4).set_z_index(2)
    H.fence_l = MathTex("t_{hold}", font_size=40, color=GOLD).next_to(H.fence, UP, buff=0.1)
    H.su_l = MathTex("t_{su}", font_size=36, color=GOLD)
    H.su_l.move_to([seg.get_x() + (0.08 if skew > 0 else -0.08), 0, 0]).align_to(H.fence_l, DOWN)
    a, b = x0 + lo * L, x0 + hi * L
    box = Rectangle(width=b - a, height=BAR_H).set_stroke(BLUE, 3).set_fill(BLUE, 0.22)
    box.move_to([(a + b) / 2, y, 0])
    hl = VGroup(*[Line([x, y - BAR_H / 2, 0], [x + BAR_H, y + BAR_H / 2, 0]).set_stroke(BLUE, 2)
                  for x in np.arange(a + 0.08, b - BAR_H, 0.3)])
    H.stretch = VGroup(box, hl)
    H.stretch.box, H.stretch.hatch = box, hl
    H.may_l = T("D1 may change", 30, BLUE).move_to([(a + b) / 2, 0, 0]).align_to(H.fence_l, DOWN)
    H.may_l.shift(0.04 * UP)
    H.xf, H.xd, H.xa, H.xb = xf, xd, a, b
    H.add(H.bar, H.arrow, H.edges, H.fence, H.deadline, H.fence_l, H.su_l, H.stretch, H.may_l)
    H.skseg, H.sk_arrows, H.sk_labels = None, [], []
    if skew > 0:
        H.skseg = Rectangle(width=skew * L, height=BAR_H).set_stroke(width=0).set_fill(TEAL, BAR_FILL)
        H.skseg.move_to([x0 + (1 - skew / 2) * L, y, 0])
        ys = y - BAR_H / 2 - 0.8
        for xo, xn in ((x0 + hold * L, xf), (x0 + (1 - su) * L, xd)):
            arr = DoubleArrow([xn, ys, 0], [xo, ys, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                              max_tip_length_to_length_ratio=0.4, color=TEAL)
            H.sk_arrows.append(arr)
            H.sk_labels.append(MathTex("t_{skew}", font_size=sk_size, color=TEAL).next_to(arr, DOWN, buff=0.12))
        H.add(H.skseg, *H.sk_arrows, *H.sk_labels)
    return H
# =============================================================================================


# ---- this scene's layout --------------------------------------------------------------------
STRIP_SC = 0.27
STRIP_C = _p(-2.6, 2.88)            # s3's strip (shapes only)
DIAG_SC, DY0 = 0.85, -0.6           # s3's placement of skew_traces()
S_UP = 0.5                          # {first}: the diagram moves up to make room underneath
T_HOLD = 2.0                        # hold window, full-size trace units (< t_skew + t_pc + 0.5)
DIM_X = 0.92                        # the right half (dimmed) starts here
INEQ_C = _p(3.72, 1.0)              # clip 3: the hold rule in the cleared right half
HOLD_C, SETUP_C = _p(-3.5, 2.35), _p(3.5, 2.35)   # clip 4: the two rules, small
RULE_SIZE, SMALL = 40, 36


def M(mob):
    return mob.scale(DIAG_SC, about_point=ORIGIN).shift(DY0 * UP)


def sx(x):
    return DIAG_SC * x


mx = sx


def sy(y):
    """Full-size trace y -> scene y after the {first} shift."""
    return DIAG_SC * y + DY0 + S_UP


X_K1, X_E1, X_Q, X_D = sx(K1), sx(E1), sx(XQ), sx(XQ + 0.5)   # CLK1 edge, CLK0 edge, Q0 change, D1's first change
X_HE = sx(K1 + T_HOLD)                                        # hold window's end
HALF = ROW_H * DIAG_SC / 2
Y_D1S, Y_C1S = sy(Y_D1), sy(Y_C1)
Y_HOLD = -1.28                       # t_hold arrow (between D1 and CLK1)
Y_MARK = -0.93                       # ticks / crosses under D1
Y_CHAIN = -2.55                      # t_skew / t_pc / t_pd (under CLK1's high level, labels up)


def harrow(xa, xb, y, color):
    arr = DoubleArrow(_p(xa, y), _p(xb, y), buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    arr.pa, arr.pb = _p(xa, y), _p(xb, y)
    return arr


def grow_out(arr):
    """A dimension arrow growing out of its left end (pa) to its right end (pb)."""
    a0, b0 = arr.pa, arr.pb
    final = arr.copy()
    col = final.get_color()
    full = np.linalg.norm(b0 - a0)
    min_len = min(0.3, 0.6 * full)

    def upd(m, t):
        if t >= 1:
            m.become(final)
            return
        if t * full < min_len:
            m.become(final).set_opacity(0)
            return
        m.become(DoubleArrow(a0, a0 + t * (b0 - a0), buff=0, stroke_width=DIM_W, tip_length=0.16,
                             max_tip_length_to_length_ratio=0.4, color=col))

    return UpdateFromAlphaFunc(arr, upd, rate_func=smooth)


def vguide(x, y0, y1, color=DIM, width=GUIDE_W):
    return Line(_p(x, y0), _p(x, y1)).set_stroke(color, width)


def ghost_x(x, w=0.3):
    hi, lo = Y_D1S + HALF, Y_D1S - HALF
    return VGroup(Line(_p(x - w / 2, hi), _p(x + w / 2, lo)),
                  Line(_p(x - w / 2, lo), _p(x + w / 2, hi))).set_stroke(FG, WAVE_W, opacity=0.6)


def make_strip():
    """s3's top strip, built in place: split_path() without its lettering, at STRIP_SC, CLK0 / CLK1 at 30."""
    P = split_path()
    for f in (P.ff0, P.ff1):
        f.remove(f.d_l, f.q_l, f.qb_l)
    P.remove(*P.names, P.cl_l, P.q0_l, P.d1_l, P.d0_l, P.q1_l)
    P.scale(STRIP_SC)
    shapes = VGroup(*[m.copy() for m in (P.ff0, P.ff1, P.cl, P.q0_w, P.d1_w, P.clk_br0, P.clk_br1, P.src)])
    P.shift(STRIP_C - shapes.get_center())
    P.clk0_l.scale(30 / (34 * STRIP_SC)).next_to(P.clk_br0, LEFT, buff=0.15).align_to(P.clk_br0, DOWN)
    P.clk1_l.scale(30 / (34 * STRIP_SC)).next_to(P.src, RIGHT, buff=0.15)
    return P


class SkewHold(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- c3.hold.1: the traces again; CLK1's first edge captures; the hold window --------------
    def clip1(self):
        P = make_strip()
        D = skew_traces()
        rows = [D.clk0, D.q0, D.d1a, D.d1b, D.clk1]
        for m in [*D.labs, *rows]:
            M(m)
        self.P, self.D = P, D
        self.trace = [*D.labs, *rows]
        self.overlay = Rectangle(width=7.1 - DIM_X, height=6.0).set_stroke(width=0).set_fill(BG, 0.75)
        self.overlay.move_to(_p((DIM_X + 7.1) / 2, 2.2 - 3.0)).set_z_index(5)
        with self.say("c3.hold.1") as c:
            # {back}
            self.play(FadeIn(P), *appear(*D.labs, lag=0.2), run_time=1.2)  # early: the four rows return whole
            self.play(*[sweep_in(r, mx(TR_X0), mx(TR_X1)) for r in rows], run_time=1.8, rate_func=linear)
            # {first}: up a little; the right half dims
            c.wait_until("first")
            self.play(*[m.animate.shift(S_UP * UP) for m in self.trace],
                      *during([FadeIn(self.overlay)], 0.3, 1.0), run_time=1.6)
            # {capture}: CLK1's first edge, FF1
            c.wait_until("capture")
            self.k1 = M(edge_line(K1, Y_C1, width=7)).shift(S_UP * UP)
            self.g_k1 = vguide(X_K1, Y_D1S + HALF + 0.1, Y_CHAIN - 0.35, YELLOW, 2.5)
            self.play(FadeIn(self.k1), FadeIn(self.g_k1), restyle(P.ff1.box, outline=YELLOW, width=6),
                      FlashAround(P.ff1.box, color=YELLOW, time_width=1.5), run_time=1.4)
            c.wait_until("old dee one")
            self.play(FlashAround(D.labs[2], color=BLUE, time_width=1.5), run_time=1.2)
            # {window}: the GOLD band, the tag, the t_hold arrow
            c.wait_until("window")
            band = Rectangle(width=X_HE - X_K1, height=2 * HALF + 0.16).set_stroke(width=0).set_fill(GOLD, 0.25)
            band.move_to(_p((X_K1 + X_HE) / 2, Y_D1S)).set_z_index(-1)
            self.band = band
            self.play(GrowFromEdge(band, LEFT), run_time=1.0)
            th = harrow(X_K1, X_HE, Y_HOLD, GOLD)
            th_l = MathTex("t_{hold}", font_size=36, color=GOLD).next_to(th.pa, LEFT, buff=0.2).set_z_index(6)
            tag = T("old D1 steady", 28, GOLD).next_to(th_l, LEFT, buff=0.35)   # clear of D1's bus lines
            self.tag = tag
            c.wait_until(own_word=tag)
            self.play(*appear(tag, shift=None), run_time=0.9)
            self.th, self.th_l = th, th_l
            c.wait_until("hold time")
            self.play(grow_out(th), *during(appear(th_l, shift=None), 0.3, 1.0),
                      run_time=min(1.4, c.until(floor=0.8)))

    # -- c3.hold.2: launch a skew later; Q0; D1's earliest change; the count --------------------
    def clip2(self):
        D, P = self.D, self.P
        sk = harrow(X_K1, X_E1, Y_CHAIN, TEAL)
        tpc = harrow(X_E1, X_Q, Y_CHAIN, PINK)
        tpd = harrow(X_Q, X_D, Y_CHAIN, PURPLE)
        labs = [MathTex(s, font_size=34, color=col).next_to(a, UP, buff=0.12).set_z_index(6)
                for s, col, a in (("t_{skew}", TEAL, sk), ("t_{pc}", PINK, tpc), ("t_{pd}", PURPLE, tpd))]
        labs[0].shift(0.08 * RIGHT)      # clear of CLK1's rising edge
        self.chain, self.chain_l = [sk, tpc, tpd], labs
        with self.say("c3.hold.2") as c:
            # {launch}
            self.play(grow_out(sk), *during(appear(labs[0], shift=None), 0.4, 1.0), run_time=1.4)
            c.wait_until("clock zero's")
            e1 = M(edge_line(E1, Y_C0, width=7)).shift(S_UP * UP)
            g_e1 = vguide(X_E1, sy(Y_C0), Y_CHAIN)
            self.e1 = e1
            self.play(FadeIn(e1), FadeIn(g_e1), FlashAround(e1, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("launch")
            self.play(*flash([P.ff0.box]), VShowPassingFlash(P.clk_paths(6)[0], time_width=0.5), run_time=1.2)
            # {q0}
            c.wait_until("q0")
            g_q = vguide(X_Q, sy(Y_Q0), Y_CHAIN)
            self.play(FadeIn(g_q), grow_out(tpc), FlashAround(D.q0.xs[0], color=GREEN, time_width=1.5),
                      *during(appear(labs[1], shift=None), 0.4, 1.0), run_time=1.5)
            # {d1}: the earliest change; "min" on both delays
            c.wait_until("d1")
            g_d = vguide(X_D, Y_D1S, Y_CHAIN - 0.35)
            self.play(FadeIn(g_d), grow_out(tpd), FlashAround(D.d1_x0, color=BLUE, time_width=1.5),
                      *during(appear(labs[2], shift=None), 0.4, 1.0), run_time=1.5)
            m1 = T("min", 28, PINK).next_to(tpc, DOWN, buff=0.12)
            m2 = T("min", 28, PURPLE).next_to(tpd, RIGHT, buff=0.12)   # t_pd is short: its tag sits beside it
            m2.set_z_index(6)                                          # above the dimming veil
            self.mins = [m1, m2]
            self.play(*appear(m1, m2, lag=0.3), run_time=0.8)  # early: "min" is what "starts to change" means
            # {count}: one bracket over the three, against t_hold
            c.wait_until("count")
            br = span_brace(_p(X_K1, Y_CHAIN - 0.62), _p(X_D, Y_CHAIN - 0.62), DOWN, color=FG, inset=0.0, buff=0.0)
            self.brace = br
            self.play(GrowFromCenter(br), run_time=1.2)
            for cue, a, col in (("skew", sk, TEAL), ("clock-to-cue delay", tpc, PINK)):
                c.wait_until(cue, nth=1)
                self.play(FlashAround(a, color=col, time_width=1.5, buff=0.08), run_time=min(0.8, c.until("logic's delay", nth=1, floor=0.5)))
            c.wait_until("logic's delay", nth=1)
            self.play(FlashAround(tpd, color=PURPLE, time_width=1.5, buff=0.08),
                      run_time=min(0.8, c.until(floor=0.3)))

    # -- c3.hold.3: good / bad ghosts; the rule; min; skew helps; the quote ----------------------
    def clip3(self):
        D = self.D
        parts = ["t_{skew}", "+", "(", "t_{pc}", "+", "t_{pd}", ")", r"_{\min}", r"\geq", "t_{hold}"]
        cols = {0: TEAL, 3: PINK, 5: PURPLE, 9: GOLD}
        full = MathTex(*parts, font_size=RULE_SIZE).move_to(INEQ_C)
        terms = [MathTex(s, font_size=RULE_SIZE, color=cols.get(i, FG)).move_to(full[i]).set_z_index(6)
                 for i, s in enumerate(parts)]
        self.terms = terms
        with self.say("c3.hold.3") as c:
            # {good}
            g1 = ghost_x(0.0)
            tick = check_mark(GREEN).scale(0.8).move_to(_p(0.0, Y_MARK))
            self.play(FadeIn(g1), FlashAround(self.th, color=GOLD, time_width=1.5, buff=0.08),
                      FlashAround(Rectangle(width=self.brace.width, height=self.brace.height).move_to(self.brace), color=FG, time_width=1.5), run_time=1.2)
            self.play(GrowFromCenter(tick), run_time=0.8)
            # {bad}
            c.wait_until("bad")
            g2 = ghost_x((X_K1 + X_E1) / 2 + 0.05)
            cross = cross_mark(RED).scale(0.8).move_to(_p(g2.get_x(), Y_MARK))
            self.play(FadeIn(g2), run_time=0.8)
            self.play(GrowFromCenter(cross), FlashAround(self.band, color=RED, time_width=1.5), run_time=1.3)
            # {rule}: the ghosts go, the right half clears, the arrows' names fly into the rule
            c.wait_until("rule")
            self.play(*disappear(g1, g2, tick, cross), self.overlay.animate.set_fill(BG, 1), run_time=1.0)
            sk_l, tpc_l, tpd_l = self.chain_l
            self.play(*during(fly(sk_l, terms[0]), 0, 0.7), run_time=1.3)
            c.wait_until("clock-to-cue")
            self.play(*during(fly(tpc_l, terms[3]), 0, 0.7), *during([FadeIn(terms[1]), FadeIn(terms[2])], 0.75, 1.0),
                      run_time=1.3)
            c.wait_until("logic")
            # the "+" marks t_pd's slot first; the label then flies straight into it
            self.play(*during([FadeIn(terms[4])], 0, 0.3), *during(fly(tpd_l, terms[5]), 0, 0.65),
                      *during([FadeIn(terms[6]), FadeIn(terms[7])], 0.75, 1.0), run_time=1.3)
            c.wait_until("at least")
            self.play(*during(fly(self.th_l, terms[9], arc=-0.35), 0, 0.75), *during([FadeIn(terms[8])], 0.8, 1.0), run_time=1.4)
            # {min}
            c.wait_until("min")
            self.play(FlashAround(terms[7], color=YELLOW, time_width=1.5), *recolor([terms[7]], YELLOW),
                      *flash(self.mins, color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("earliest")
            self.play(FlashAround(D.d1_x0, color=BLUE, time_width=1.5), run_time=1.2)
            # {helps}
            c.wait_until("helps")
            tk = check_mark(GREEN).move_to(terms[0].get_center() + 0.75 * DOWN).set_z_index(6)
            self.play(FlashAround(terms[0], color=TEAL, time_width=1.5), *during([GrowFromCenter(tk)], 0.4, 1.0),
                      run_time=1.3)
            # {quote}
            c.wait_until("quote")
            q = VGroup(T("“in effect, the availability", 30, FG, slant=ITALIC),
                       T("of hold time is increased”", 30, FG, slant=ITALIC)).arrange(DOWN, buff=0.15)
            q.move_to(_p(INEQ_C[0], INEQ_C[1] - 2.0)).set_z_index(6)
            self.tk, self.quote = tk, q
            self.play(*appear(q, lag=0.2), run_time=0.8)  # early: p. 109's words, read in the narration's paraphrase

    # -- c3.hold.4: both fences, then the skew slides them --------------------------------------
    def clip4(self):
        terms = self.terms
        H0, H1 = skew_fences(0.0), skew_fences(0.1)
        k = SMALL / RULE_SIZE
        tgt = VGroup(*[t.copy() for t in terms]).scale(k).move_to(HOLD_C)
        su_parts = ["T_c", r"\geq", "(", "t_{pc}", "+", "t_{pd}", ")", r"_{\max}", "+", "t_{su}", "+", "t_{skew}"]
        su_cols = {0: YELLOW, 3: PINK, 5: PURPLE, 9: GOLD, 11: TEAL}
        setup = MathTex(*su_parts, font_size=SMALL).move_to(SETUP_C)
        for i, col in su_cols.items():
            setup[i].set_color(col)
        others = [m for m in self.mobjects if m not in terms and m is not self.overlay]
        with self.say("c3.hold.4") as c:
            # {fences}: clear to the bar (once the quote has been read); the hold rule shrinks to the top left
            c.wait_until("picture")
            self.play(*during([FadeOut(m) for m in others], 0, 0.5), *during([FadeOut(self.overlay)], 0.45, 0.6),
                      *during([t.animate.scale(k).move_to(g) for t, g in zip(terms, tgt)], 0.35, 1.0), run_time=1.6)
            self.play(GrowFromEdge(H0.bar.outline, LEFT),
                      *during(appear(H0.arrow, H0.bar.tc, *H0.edges, shift=None, lag=0.1), 0.3, 1.0),
                      *during(appear(setup, shift=None), 0.5, 1.0), run_time=min(1.4, c.until("anywhere", floor=0.8)))  # early: one period, and both rules
            # the stretch, the hold fence, the deadline
            c.wait_until("anywhere")
            # the stretch widens sideways from its centre at full height (GrowFromCenter began as a dot)
            self.play(grow_wide(H0.stretch.box, None), *during([FadeIn(H0.stretch.hatch)], 0.4, 1.0),
                      *during(appear(H0.may_l), 0.4, 1.0), run_time=1.3)
            settle(self, H0.stretch)
            c.wait_until("hold fence")
            self.play(FadeIn(H0.fence), *appear(H0.fence_l), FlashAround(H0.fence, color=GOLD), run_time=1.1)
            c.wait_until("deadline")
            self.play(grow_wide(H0.su, LEFT), FadeIn(H0.deadline), *appear(H0.su_l),
                      run_time=min(1.1, c.until("slide", floor=0.8)))
            # {slide}
            c.wait_until("slide")
            # dim GOLD ghosts stay at the old places (0.3, 0.9) as both fences slide
            ghosts = [DashedLine(m.get_start() + 0.2 * DOWN, m.get_end() + 0.2 * UP, dash_length=0.09)
                      .set_stroke(GOLD, 5, opacity=0.6).set_z_index(3) for m in (H0.fence, H0.deadline)]
            self.add(*ghosts)
            self.play(*[m.animate.move_to(n) for m, n in ((H0.fence, H1.fence), (H0.fence_l, H1.fence_l),
                                                         (H0.deadline, H1.deadline), (H0.su, H1.su),
                                                         (H0.su_l, H1.su_l))],
                      grow_wide(H1.skseg, RIGHT), *[grow_out_rev(a) for a in H1.sk_arrows], run_time=2.0)
            self.play(*appear(*H1.sk_labels, shift=None, lag=0.2), run_time=0.9)
            # {hurt}
            c.wait_until("hurt")
            lost = Rectangle(width=ghosts[1].get_x() - H1.xd, height=BAR_H + 0.14).set_stroke(RED, 3)
            lost.set_fill(RED, 0.18).set_z_index(1).move_to(_p((ghosts[1].get_x() + H1.xd) / 2, FB_Y))
            self.play(GrowFromCenter(lost), FlashAround(H0.deadline, color=RED, time_width=1.5, buff=0.12),
                      FlashAround(ghosts[1], color=RED, time_width=1.5, buff=0.08), run_time=1.3)
            hard = T("harder", 30, RED).next_to(setup, DOWN, buff=0.3)
            c.wait_until(own_word=hard)
            self.play(*appear(hard), run_time=0.9)
            # {help}
            c.wait_until("help")
            gap = Rectangle(width=H1.xa - H1.xf, height=BAR_H + 0.14).set_stroke(GREEN, 3)
            gap.set_fill(GREEN, 0.22).set_z_index(1).move_to(_p((H1.xa + H1.xf) / 2, FB_Y))
            self.play(GrowFromCenter(gap), FlashAround(ghosts[0], color=GREEN, time_width=1.5, buff=0.08),
                      run_time=1.3)
            easy = T("easier", 30, GREEN).next_to(tgt, DOWN, buff=0.3)
            c.wait_until(own_word=easy)
            self.play(*appear(easy), run_time=min(0.9, c.until(floor=0.6)))
        self.wait(0.6)
        # the ghosts and highlights go; the end shot (copied by s6 / the recap) is unchanged
        self.play(*disappear(*ghosts, lost, gap), run_time=0.8)
        self.wait(1.8)


def grow_wide(rect, edge):
    """A bar segment growing out of one edge, full height throughout (GrowFromEdge starts it as a dot)."""
    rect.save_state()
    if edge is None:
        rect.stretch(0.01, 0)
    else:
        rect.stretch(0.01, 0, about_edge=edge)
    return Restore(rect)


def grow_out_rev(arr):
    """A TEAL skew arrow growing from the fence's old place (its right end) to the new one."""
    arr.pa, arr.pb = arr.get_right(), arr.get_left()
    return grow_out(arr)
