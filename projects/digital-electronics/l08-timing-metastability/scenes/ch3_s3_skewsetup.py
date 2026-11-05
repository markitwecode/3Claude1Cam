"""Chapter 3, scene 3: skew and set-up (p. 108). Clips c3.setup.1 – c3.setup.4.

Shared helpers (between the rulers below; s2, s4, s5 copy them):
  split_path()      ch1_s4's path_diagram() with its CLK bus replaced by a clock source at the right
                    (.src, YELLOW circle r 0.3 at (6.25, -1.8)) and two YELLOW branches:
                    .clk_br1 short, source -> (4.4, -1.8) -> FF1's triangle, opacity 0.55;
                    .clk_br0 long, source -> down to y -2.55 -> left to x -4.4 -> FF0's triangle.
                    Labels .clk0_l "CLK0" (T 34 YELLOW, under the long run) and .clk1_l "CLK1"
                    (T 34 YELLOW at 0.7, above the short run). .clk_paths() -> fresh width-10 copies.
  skew_traces()     p. 108's four traces in ch1_s5's data-sheet style (geometry in the TRACE block).
  budget_bar()      ch1_s6's bar, verbatim.
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
# THE lecture's budget bar, copied verbatim from ch1_s6_setup.py
# =============================================================================================
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
# =============================================================================================


def grow_outline(outline, start=0.2):
    """The outline fades in at `start` of its width and widens from its left edge (no zero-width stub)."""
    left, w = outline.get_left(), outline.width
    ref = outline.copy()

    def upd(m, a):
        m.become(ref.copy().stretch_to_fit_width(w * (start + (1 - start) * a)).move_to(left, aligned_edge=LEFT))
        m.set_stroke(opacity=min(1.0, a / 0.35))
    return UpdateFromAlphaFunc(outline, upd)


def source_dip(src):
    """The source label hides while a flying copy leaves it, then returns (no doubled glyph)."""
    def upd(m, a):
        m.set_opacity(1.0 if a <= 0.0 else (0.0 if a < 0.6 else min(1.0, (a - 0.6) / 0.35)))
    return UpdateFromAlphaFunc(src, upd)


# ---- this scene's layout --------------------------------------------------------------------
STRIP_SC = 0.27
STRIP_C = _p(-2.6, 2.88)            # the path's strip (shapes only), top: x -4.3 … -0.9, y 2.3 … 3.45
DIAG_SC, DY0 = 0.85, -0.6           # the diagram is drawn at 0.85 of skew_traces(), 0.6 down
DY4 = 1.25                          # clip 4: it moves up to make room for the bar
BAR_Y = -3.1
BAR_Y_END, BAR_CX_END = -1.3, 0.3   # clip 4 {rule}: the bar moves to the centre
INEQ_Y = 1.5


def M(mob):
    """Full-size skew_traces() coordinates -> this scene's diagram."""
    return mob.scale(DIAG_SC, about_point=ORIGIN).shift(DY0 * UP)


def mx(x):
    return DIAG_SC * x


class SkewSetup(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- c3.setup.1: the four rows, CLK0, CLK1 ------------------------------------------------
    def clip1(self):
        P = split_path()
        self.P = P
        self.play(FadeIn(P), run_time=0.8)
        self.wait(0.4)
        D = skew_traces()
        self.D = D
        for m in [*D.labs, D.clk0, D.clk1, D.q0, D.d1a, D.d1b, D.g_e1, D.g_e2, D.g_k1, D.g_k2, D.g_q,
                  D.g_s, D.tc, D.sk1, D.sk2, D.tpc, D.tpd, D.tsu]:
            M(m)
        # the strip: shapes only (the small lettering fades out), CLK0 / CLK1 labels kept at 30
        texts = [*P.names, P.cl_l, P.q0_l, P.d1_l, P.d0_l, P.q1_l]
        ff_texts = [(f, t) for f in (P.ff0, P.ff1) for t in (f.d_l, f.q_l, f.qb_l)]
        P.generate_target()
        tgt = P.target
        ix = P.submobjects.index
        for t in texts:
            tgt[ix(t)].set_opacity(0)
        for f, t in ff_texts:
            tgt[ix(f)][f.submobjects.index(t)].set_opacity(0)
        tgt.scale(STRIP_SC)
        shapes = VGroup(*[tgt[ix(m)] for m in (P.ff0, P.ff1, P.cl, P.q0_w, P.d1_w, P.clk_br0, P.clk_br1, P.src)])
        tgt.shift(STRIP_C - shapes.get_center())
        tl0, tl1 = tgt[ix(P.clk0_l)], tgt[ix(P.clk1_l)]
        tl0.scale(30 / (34 * STRIP_SC)).next_to(tgt[ix(P.clk_br0)], LEFT, buff=0.15)
        tl0.align_to(tgt[ix(P.clk_br0)], DOWN)
        tl1.scale(30 / (34 * STRIP_SC)).next_to(tgt[ix(P.src)], RIGHT, buff=0.15)
        with self.say("c3.setup.1") as c:
            # {traces}
            self.play(MoveToTarget(P), run_time=1.4)
            for f, t in ff_texts:
                f.remove(t)
            P.remove(*texts)
            self.play(*appear(*D.labs, lag=0.3), run_time=1.4)  # early: the four rows shown whole, then walked
            # {clk0}
            c.wait_until("clk0")
            self.play(sweep_in(D.clk0, mx(TR_X0), mx(TR_X1)), run_time=1.8, rate_func=linear)
            self.play(FadeIn(D.g_e1), FadeIn(D.g_e2), grow_dim(D.tc[0]),
                      *during(appear(D.tc[1], shift=None), 0.4, 1.0), run_time=1.4)
            # {clk1}: a copy of CLK0 drops to the bottom row, then slides earlier
            c.wait_until("clk1")
            cp = D.clk0.copy()
            self.play(cp.animate.move_to(D.clk1, coor_mask=UP), run_time=1.2)
            c.wait_until("shifted earlier")
            self.play(Transform(cp, D.clk1),
                      *during([FadeIn(D.g_k1), FadeIn(D.g_k2), grow_dim(D.sk1[0]), grow_dim(D.sk2[0])], 0.45, 0.9),
                      *during(appear(D.sk1[1], D.sk2[1], shift=None, lag=0.1), 0.6, 1.0),
                      run_time=min(2.0, c.until(floor=1.2)))
            self.remove(cp)
            self.add(D.clk1)

    # -- c3.setup.2: launch, Q0, D1 settles ---------------------------------------------------
    def clip2(self):
        D, P = self.D, self.P
        with self.say("c3.setup.2") as c:
            # {launch}
            e1 = M(edge_line(E1, Y_C0, width=7))
            self.play(FadeIn(e1), FlashAround(e1, color=YELLOW, time_width=1.5),
                      VShowPassingFlash(P.clk_paths(6)[0], time_width=0.5), run_time=1.5)
            c.wait_until("launches it")
            self.play(*flash([P.ff0.box]), run_time=1.2)
            self.e1 = e1
            # {q0}
            c.wait_until("q0")
            self.play(sweep_in(D.q0, mx(TR_X0), mx(TR_X1)), run_time=1.8, rate_func=linear)
            self.play(FadeIn(D.g_q), grow_dim(D.tpc[0]), *during(appear(D.tpc[1], shift=None), 0.4, 1.0),
                      run_time=1.4)
            # {d1}: the hatched settling run
            c.wait_until("d1")
            self.play(sweep_in(D.d1a, mx(TR_X0), mx(XS - 0.4)), run_time=2.4, rate_func=linear)
            # {settle}: the last crossover, and t_pd
            c.wait_until("settle")
            self.play(sweep_in(D.d1b, mx(XS - 0.4), mx(TR_X1)), run_time=0.9, rate_func=linear)
            self.play(FadeIn(D.g_s), grow_dim(D.tpd[0]), *during(appear(D.tpd[1], shift=None), 0.4, 1.0),
                      run_time=min(1.4, c.until(floor=0.8)))

    # -- c3.setup.3: which edge? CLK1's, early by the skew --------------------------------------
    def clip3(self):
        D, P = self.D, self.P
        q = M(T("?", 60, YELLOW).move_to(_p(XS - 0.2, Y_ARR + 0.35)))
        with self.say("c3.setup.3") as c:
            # {deadline}
            self.play(*appear(q), FlashAround(D.last_x, color=YELLOW, time_width=1.5), run_time=1.2)  # early: the question mark
            # {capture}: CLK1's second edge and its guide light, CLK0's second edge dims
            c.wait_until("capture")
            k2 = M(edge_line(K2, Y_C1, width=7))
            g_k2 = M(Line(_p(K2, Y_ARR + 0.2), _p(K2, G_BOT)).set_stroke(YELLOW, 2.5))
            e2_cover = M(edge_line(E2, Y_C0, color=BG, width=9))
            e2_dim = M(edge_line(E2, Y_C0, opacity=0.3))
            self.play(FadeIn(k2), FadeIn(g_k2), restyle(P.ff1.box, outline=YELLOW, width=6),
                      FlashAround(P.ff1.box, color=YELLOW, time_width=1.5), run_time=1.4)
            self.play(FadeIn(e2_cover), FadeIn(e2_dim), run_time=1.0)
            self.k2, self.g_k2, self.e2_cover, self.e2_dim = k2, g_k2, e2_cover, e2_dim
            c.wait_until("set-up time")
            self.play(grow_dim(D.tsu[0]), *swap(q, D.tsu[1]), run_time=1.4)
            # {early}: the gap between CLK1's edge and CLK0's
            c.wait_until("early")
            self.play(restyle(D.sk2[0], width=5), FlashAround(D.sk2, color=TEAL, time_width=1.5),
                      run_time=1.4)
            self.play(*set_alpha([D.sk1], 0.45), run_time=0.8)
            # {lost}: ch1's deadline (t_su before CLK0's edge) slides left by the skew
            c.wait_until("lost")
            ghost = VGroup(
                DoubleArrow(_p(E2 - T_SU, Y_ARR), _p(E2, Y_ARR), buff=0, stroke_width=DIM_W, tip_length=0.16,
                            max_tip_length_to_length_ratio=0.4, color=GOLD),
                Line(_p(E2 - T_SU, Y_ARR - 0.3), _p(E2 - T_SU, Y_ARR + 0.3)).set_stroke(GOLD, 4))
            M(ghost).set_opacity(0.5)
            self.play(FadeIn(ghost), run_time=0.8)
            self.play(ghost.animate.shift(mx(T_SK) * LEFT), run_time=1.6)
            gap = Rectangle(width=T_SK, height=0.5).set_stroke(width=0).set_fill(TEAL, 0.3)
            M(gap.move_to(_p(K2 + T_SK / 2, Y_ARR)))
            self.play(FadeOut(ghost), FadeIn(gap), FlashAround(gap, color=TEAL, time_width=1.5),
                      FlashAround(D.last_x, color=GOLD, time_width=1.5), run_time=min(1.4, c.until(floor=0.8)))
            self.gap_rect = gap

    # -- c3.setup.4: the four-piece budget and the rule ----------------------------------------
    def clip4(self):
        D, P = self.D, self.P
        diagram = [*D.labs, D.clk0, D.clk1, D.q0, D.d1a, D.d1b, D.g_e1, D.g_e2, D.g_k1, D.g_k2, D.g_q,
                   D.g_s, D.tc, D.sk1, D.sk2, D.tpc, D.tpd, D.tsu, self.e1, self.k2, self.g_k2,
                   self.e2_cover, self.e2_dim]
        bar = budget_bar([("t_{pc}", PINK, mx(T_PC)), ("t_{pd}", PURPLE, mx(T_PD)),
                          ("t_{su}", GOLD, mx(T_SU)), ("t_{skew}", TEAL, mx(T_SK))],
                         mx(TC), x0=mx(E1), y=BAR_Y, sym_size=40)
        bar.syms[2].shift(0.06 * LEFT)
        bar.syms[3].shift(0.06 * RIGHT)
        with self.say("c3.setup.4") as c:
            # {bar}: the strip and the gap go; the diagram moves up; the outline grows under T_c
            self.play(*during([FadeOut(P), FadeOut(self.gap_rect)], 0, 0.5),
                      *during([m.animate.shift(DY4 * UP) for m in diagram], 0.3, 1.0), run_time=1.6)
            self.play(time_span(FlashAround(D.tc[0], color=YELLOW, time_width=1.5, buff=0.1), 0, 1.0),
                      time_span(grow_outline(bar.outline), 0.3, 1.3),
                      *during(appear(bar.tc, shift=None), 0.5, 1.0), run_time=1.3)
            # {segs}: each arrow drops into its segment
            arrows = (D.tpc, D.tpd, D.tsu)
            cues = ("segs", "logic's delay", "set-up time")
            for k, (a, cue) in enumerate(zip(arrows, cues)):
                c.wait_until(cue)
                self.play(ReplacementTransform(a[0].copy(), bar.segs[k]),
                          *during(appear(bar.syms[k], shift=None), 0.5, 1.0), run_time=1.2)
            # {fourth}: the skew
            c.wait_until("fourth")
            self.play(FlashAround(D.sk2, color=TEAL, time_width=1.5), run_time=1.0)
            self.play(ReplacementTransform(D.sk2[0].copy(), bar.segs[3]),
                      *during(appear(bar.syms[3], shift=None), 0.5, 1.0), run_time=1.4)
            # {rule}: the diagram clears; the bar moves to the centre; its symbols fly into the rule
            c.wait_until("rule")
            parts = [*bar.segs, bar.outline, *bar.syms, bar.tc]
            end_shift = _p(BAR_CX_END - bar.outline.get_x(), BAR_Y_END - BAR_Y)
            sweep_clear(self, *[m.animate.shift(end_shift) for m in parts], keep=parts, run_time=1.6)
            settle(self, bar)
            full = MathTex("T_c", r"\geq", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", "+", "t_{skew}",
                           font_size=52)
            full.move_to(_p(BAR_CX_END - 0.3, INEQ_Y))
            cols = {0: YELLOW, 2: PINK, 4: PURPLE, 6: GOLD, 8: TEAL}
            terms = [MathTex(s, font_size=52, color=cols.get(i, FG)).move_to(full[i])
                     for i, s in enumerate(["T_c", r"\geq", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", "+",
                                            "t_{skew}"])]
            self.ineq = VGroup(*terms)
            c.wait_until("at least")
            self.play(*fly(bar.tc, terms[0]), *during(appear(terms[1], shift=None), 0.5, 1.0), run_time=1.2)
            steps = [("clock-to-cue delay", 0, [], 2), ("logic's delay", 1, [3], 4),
                     ("set-up time", 2, [5], 6), ("skew", 3, [7], 8)]
            for cue, k, plus, idx in steps:
                c.wait_until(cue, nth=1)
                self.play(*fly(bar.syms[k], terms[idx], arc=(-0.5 if k == 2 else None)),
                          *during([FadeIn(terms[j]) for j in plus], 0.5, 1.0),
                          *([source_dip(bar.syms[k])] if k == 2 else []), run_time=1.0)
            # {worst}: the longest delays
            c.wait_until("worst")
            m1 = T("max", 30, PINK).next_to(bar.segs[0], DOWN, buff=0.2)
            m2 = T("max", 30, PURPLE).next_to(bar.segs[1], DOWN, buff=0.2)
            m2.align_to(m1, DOWN)
            self.play(*appear(m1, m2, lag=0.3), run_time=1.2)  # early: "max" is what "longest" means
