"""Chapter 2, scene 5: longest and shortest delays; contamination delay. Clips c2.range.1 – c2.range.4.

Copied (not imported) from ch2_s4_noclockfix.py: hold_diagram + path_diagram/routes_path/routes (s4's
end shot, with s4's fix pass: FG buffers, CLK label at the right end of its line); from ch2_s1_hook.py
(ch1_s6's owner copy): budget_bar + tc_arrow.

Shared with s6's recap tile 5 / ch3: hold_budget(x0=BAR_X0, y=BAR_Y, L=TC_LEN, hold=0.3, su=0.1,
lo=0.4, hi=0.8): the 7.0 x 0.5 period bar (x -3.3 .. 3.7, y 1.4), YELLOW outline, T_c label left,
label-free YELLOW T_c arrow 0.35 under it, YELLOW up-arrows (clock edges) above both ends, GOLD hold
fence (vertical, stroke 7) at hold*L with "t_hold" above, GOLD t_su segment (last su*L) whose left edge
is the GOLD set-up deadline line, BLUE hatched "D1 may change" stretch from lo*L to hi*L.
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
# s3's two-box end shot (copied from ch2_s3_shiftreg.py)
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0

# =============================================================================================
# s2's data-sheet diagram (copied from ch2_s2_hold.py; `lab` boosts the label sizes)
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


YC, YQ, YD = 2.1, 0.4, -1.3
X0, X1 = -4.6, 6.3
E1, FALL, E2 = -2.8, 0.7, 4.2
PERIOD = E2 - E1
XQ = -1.6
HATCH_END = 2.7
XSU = 3.5
LAB_X = -5.9
Y_A = -2.4
HOLD_END = 0.3

# this scene's placement of the diagram
DK = 0.6
DX, DY = 0.0, -1.71
LAB = 1.3


def ux(u):
    return E1 + u * PERIOD


def M(x, y):
    return np.array([DK * x + DX, DK * y + DY, 0])


def _place(*ms):
    for m in ms:
        m.scale(DK, about_point=ORIGIN).shift([DX, DY, 0])
    return ms


def hold_diagram(hatch0=0.4, k=DK, shift=(DX, DY), lab=LAB):
    xh = ux(hatch0)
    clk_l = clock_wave(X0, HATCH_END, YC, [E1, FALL], color=YELLOW)
    clk_r = clock_wave(HATCH_END, X1, YC, [E2], color=YELLOW)
    clk_lab = T("CLK", 40 * lab, YELLOW).move_to([LAB_X, YC, 0])
    g1, g2 = guide(E1, 3.25, -2.6), guide(E2, 3.25, -2.6)
    tc = dim_arrow(E1, E2, 3.05, YELLOW, "T_c", size=44 * lab)
    q0 = bus(X0, HATCH_END, YQ, [(XQ - 0.2, XQ + 0.2)], color=GREEN)
    q0_r = bus(HATCH_END, X1, YQ, [], color=GREEN)
    q0_lab = MathTex("Q_0", font_size=48 * lab, color=GREEN).move_to([LAB_X, YQ, 0])
    gq = guide(XQ, YQ + 0.6, -2.6)
    tpc = dim_arrow(E1, XQ, Y_A, PINK, "t_{pc}", label_dir=DOWN, size=44 * lab)
    d1 = bus(X0, HATCH_END, YD, hatch(xh, HATCH_END, 4), color=BLUE)
    d1_r = bus(HATCH_END, X1, YD, [(3.1, XSU)], color=BLUE)
    d1_lab = MathTex("D_1", font_size=48 * lab, color=BLUE).move_to([LAB_X, YD, 0])
    gsu = guide(XSU, YD + 0.4, -2.6)
    tpd = dim_arrow(XQ, XSU, Y_A, PURPLE, "t_{pd}", label_dir=DOWN, size=44 * lab)
    tsu = dim_arrow(XSU, E2, Y_A, GOLD, "t_{su}", label_dir=DOWN, size=44 * lab)

    dg = VGroup(g1, g2, gq, gsu, clk_l, clk_r, q0, q0_r, d1, d1_r,
                clk_lab, q0_lab, d1_lab, tc, tpc, tpd, tsu)
    band = Rectangle(width=ux(HOLD_END) - E1, height=ROW_H + 0.16)
    band.set_stroke(GOLD, 2).set_fill(GOLD, 0.22).move_to([(E1 + ux(HOLD_END)) / 2, YD, 0])
    band.set_z_index(-1)
    for m in (dg, band):
        m.scale(k, about_point=ORIGIN).shift([shift[0], shift[1], 0])
    for name, m in dict(g1=g1, g2=g2, gq=gq, gsu=gsu, clk=clk_l, clk_r=clk_r, q0=q0, q0_r=q0_r,
                        d1=d1, d1_r=d1_r, clk_lab=clk_lab, q0_lab=q0_lab, d1_lab=d1_lab,
                        tc=tc, tpc=tpc, tpd=tpd, tsu=tsu).items():
        setattr(dg, name, m)
    dg.band = band
    return dg



# =============================================================================================
# ch1's path (copied from ch1_s4_path.py)
# =============================================================================================
def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, bubble=False, d_text="D"):
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
    g.box, g.tri, g.bub = box, tri, None
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


P_FF_X = (-4.2, 4.2)
P_FF_Y = 0.5
P_PIN = P_FF_Y + PIN_Y
P_BUS = P_FF_Y - BOX_H / 2 - EN_WIRE
P_BUS_X0 = -5.6
P_CL_W, P_CL_H = 3.0, 1.6


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


PS, PY, LB = 0.66, 1.9, 1.3
XJ = 1.25                 # route junctions (frame x = -XJ, +XJ)
RAIL = 0.55               # rails above / below the pin row


def routes_path():
    """path_diagram() across the top of the frame, labels boosted to stay readable."""
    P = path_diagram()
    P.scale(PS, about_point=ORIGIN).shift(PY * UP)
    for m in [*P.names, P.q0_l, P.d1_l, P.d0_l, P.q1_l, P.clk_l, P.cl_l,
              P.ff0.d_l, P.ff0.q_l, P.ff0.qb_l, P.ff1.d_l, P.ff1.q_l, P.ff1.qb_l]:
        m.scale(LB)
    P.pin = P.q0_w.get_start()[1]
    return P


def routes(pin):
    R = VGroup()
    up, lo = pin + RAIL, pin - RAIL
    R.long = VMobject().set_points_as_corners([_p(-XJ, pin), _p(-XJ, up), _p(XJ, up), _p(XJ, pin)])
    R.short = VMobject().set_points_as_corners([_p(-XJ, pin), _p(-XJ, lo), _p(XJ, lo), _p(XJ, pin)])
    for w in (R.long, R.short):
        w.set_stroke(BLUE, 4)

    def gate(x, y):
        return Rectangle(width=0.42, height=0.4).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(_p(x, y)).set_z_index(1)
    R.gates_long = [gate(x, up) for x in (-0.68, 0.0, 0.68)]
    R.gate_short = gate(-0.68, lo)
    R.dots = [Dot(_p(x, pin), radius=0.07, color=BLUE) for x in (-XJ, XJ)]
    R.bufs = []
    for x in (0.02, 0.66):
        b = Polygon(_p(x - 0.2, lo - 0.21), _p(x - 0.2, lo + 0.21), _p(x + 0.22, lo))
        R.bufs.append(b.set_stroke(GOLD, 3).set_fill(BG, 1).set_z_index(1))
    R.lo = lo
    R.add(R.long, R.short, *R.gates_long, R.gate_short, *R.dots)
    return R


# =============================================================================================
# s1's window (fill 0.25 style, split at the edge), drawn large for FF1's D input
# =============================================================================================
WX, WY, WW, WH = 1.7, -1.4, 5.2, 0.95


def s4_end_shot():
    """s4's last frame: the path with its two routes (S) and the good hold diagram (D)."""
    P = routes_path()
    P.clk_l.next_to(P.clk_bus.get_end(), RIGHT, buff=0.15)      # s4 fix pass: CLK at the line's right end
    P.remove(P.cl, P.cl_l)
    P.q0_w.put_start_and_end_on(P.q0_w.get_start(), _p(-XJ, P.pin))
    P.d1_w.put_start_and_end_on(_p(XJ, P.pin), P.d1_w.get_end())
    R = routes(P.pin)
    R.long.set_stroke(GREEN, 6)
    for g in R.gates_long:
        g.set_stroke(GREEN)
    R.short.set_stroke(YELLOW, 6)
    R.gate_short.set_stroke(YELLOW)
    for b in R.bufs:
        b.set_stroke(FG)                                          # s4 fix pass: plain FG buffers
    R.add(*R.bufs)
    S = VGroup(P, R)
    S.P, S.R = P, R
    dg = hold_diagram(0.4)
    t1 = check_mark(GREEN).move_to(dg.band)
    t2 = check_mark(GREEN).move_to(M((XSU + E2) / 2, YD))
    D = VGroup(dg.band, dg, t1, t2)
    return S, D


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


TC_LEN = 7.0
BAR_X0 = -3.3
BAR_Y = 1.4


def hold_budget(x0=BAR_X0, y=BAR_Y, L=TC_LEN, hold=0.3, su=0.1, lo=0.4, hi=0.8):
    """One clock period with both fences: hold fence (left), set-up deadline (right), and the
    BLUE hatched stretch where D1 may change. Parts: .bar (.outline .tc .segs[0] = t_su) .arrow
    .edges .fence .fence_l .deadline .su_l .stretch (.box .hatch) .may_l."""
    H = VGroup()
    H.bar = budget_bar([("t_{su}", GOLD, su * L)], L, x0=x0, y=y, syms=False)
    seg = H.bar.segs[0].shift((1 - su) * L * RIGHT)
    H.su = seg
    H.arrow = tc_arrow(x0, x0 + L, y - BAR_H / 2 - 0.35)
    H.edges = VGroup(*[Arrow([x, y + 0.3, 0], [x, y + 1.0, 0], buff=0, stroke_width=4, tip_length=0.2,
                             max_tip_length_to_length_ratio=0.4, color=YELLOW) for x in (x0, x0 + L)])
    xf, xd = x0 + hold * L, x0 + (1 - su) * L
    H.fence = Line([xf, y - 0.45, 0], [xf, y + 0.45, 0]).set_stroke(GOLD, 7).set_z_index(2)
    H.deadline = Line([xd, y - 0.45, 0], [xd, y + 0.45, 0]).set_stroke(GOLD, 4).set_z_index(2)
    H.fence_l = MathTex("t_{hold}", font_size=40, color=GOLD).next_to(H.fence, UP, buff=0.1)
    H.su_l = MathTex("t_{su}", font_size=36, color=GOLD)
    H.su_l.move_to([seg.get_x() - 0.08, 0, 0]).align_to(H.fence_l, DOWN)
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
    return H


# =============================================================================================
# Delay bars (clips 1 – 3)
# =============================================================================================
PU_Y, PK_Y = 0.0, -1.8           # t_pd row (top, nearer the path), t_pc row
XMIN, XMAX = -0.4, 3.6           # the two columns after {bars}
BAR_T = 0.36


def dbar(tex, color, a, b, y):
    g = VGroup()
    g.rect = Rectangle(width=b - a, height=BAR_T).set_stroke(width=0).set_fill(color, 0.6).move_to([(a + b) / 2, y, 0])
    g.ta = Line([a, y - 0.32, 0], [a, y + 0.32, 0]).set_stroke(color, 6)
    g.tb = Line([b, y - 0.32, 0], [b, y + 0.32, 0]).set_stroke(color, 6)
    g.la = MathTex(f"({tex})" + r"_{\min}", font_size=48, color=color).next_to(g.ta, LEFT, buff=0.45)
    g.lb = MathTex(f"({tex})" + r"_{\max}", font_size=48, color=color).next_to(g.tb, RIGHT, buff=0.45)
    g.add(g.rect, g.ta, g.tb, g.la, g.lb)
    return g


def column(x):
    r = Rectangle(width=0.55, height=PU_Y - PK_Y + 1.0).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.1)
    return r.move_to([x, (PU_Y + PK_Y) / 2, 0]).set_z_index(-1)


def stack(L, x0, y, pc, pd, h=0.36):
    a = Rectangle(width=pc * L, height=h).set_stroke(width=0).set_fill(PINK, 0.85).move_to([x0 + pc * L / 2, y, 0])
    b = Rectangle(width=(pd - pc) * L, height=h).set_stroke(width=0).set_fill(PURPLE, 0.85)
    b.move_to([x0 + (pc + pd) * L / 2, y, 0])
    return VGroup(a, b)


def sum_label(kind):
    m = MathTex("(", "t_{pc}", "+", "t_{pd}", ")_{\\" + kind + "}", font_size=44)
    m[1].set_color(PINK)
    m[3].set_color(PURPLE)
    return m


def arrow_tag(left, right, color):
    return VGroup(T(left, 36, color), MathTex(r"\rightarrow", font_size=44, color=color),
                  T(right, 36, color)).arrange(RIGHT, buff=0.2)


class Contamination(NarratedScene):
    def construct(self):
        S, D = s4_end_shot()
        self.play(FadeIn(S), FadeIn(D), run_time=0.8)
        self.wait(0.2)
        self.clip1(S, D)
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c2.range.1 ----------------------------------------------------------------------------
    def clip1(self, S, D):
        S.generate_target()
        S.target.scale(0.9).to_corner(UL, buff=0.35)
        pk = dbar("t_{pc}", PINK, -0.2, 1.4, PK_Y)
        pu = dbar("t_{pd}", PURPLE, 0.4, 2.8, PU_Y)
        singles = []
        for g, tex, col in ((pk, "t_{pc}", PINK), (pu, "t_{pd}", PURPLE)):
            m = g.rect.get_x()
            g.ta_home, g.tb_home = g.ta.get_center(), g.tb.get_center()
            g.ta.move_to([m, g.ta.get_y(), 0])
            g.tb.move_to([m, g.tb.get_y(), 0])
            singles.append(MathTex(tex, font_size=52, color=col).next_to(g.ta, LEFT, buff=0.2))
        with self.say("c2.range.1") as c:
            self.play(*during(disappear(D), 0, 0.45), *during([MoveToTarget(S)], 0.25, 1.0), run_time=2.0)
            self.play(*appear(pk.ta, pk.tb, singles[0], pu.ta, pu.tb, singles[1], shift=None, lag=0.15),  # early: the two delays, as numbers
                      run_time=min(1.2, c.until("in fact")))
            c.wait_until("is a range")
            anims = []
            for g in (pk, pu):
                anims += during([g.ta.animate.move_to(g.ta_home), g.tb.animate.move_to(g.tb_home),
                                 GrowFromCenter(g.rect)], 0.3, 0.85)
                anims += during(appear(g.la, g.lb, shift=None), 0.7, 1.0)
            self.play(*during(disappear(*singles), 0, 0.3), *anims, run_time=2.0)
            settle(self, pk)
            settle(self, pu)

            c.wait_until("why")
            self.play(*[FlashAround(g.rect, color=YELLOW, time_width=1.5) for g in (pk, pu)], run_time=1.6)

            R = S.R
            c.wait_until("short route")
            j_s = DashedLine(R.gate_short.get_bottom(), pu.ta.get_top(), dash_length=0.12).set_stroke(YELLOW, 3)
            self.play(VShowPassingFlash(R.short.copy().set_stroke(YELLOW, 10), time_width=0.5),
                      *during([Create(j_s)], 0.3, 1.0), FlashAround(pu.ta, color=YELLOW), run_time=1.5)
            c.wait_until("long route")
            j_l = DashedLine(R.gates_long[2].get_bottom(), pu.tb.get_top(), dash_length=0.12).set_stroke(GREEN, 3)
            self.play(VShowPassingFlash(R.long.copy().set_stroke(GREEN, 10), time_width=0.5),
                      *during([Create(j_l)], 0.3, 1.0), FlashAround(pu.tb, color=GREEN), run_time=1.5)

            c.wait_until("bars")
            moves = [FadeOut(j_s), FadeOut(j_l)]
            for g, y in ((pk, PK_Y), (pu, PU_Y)):
                new = dbar("t_{pc}" if g is pk else "t_{pd}", g.ta.get_color(), XMIN, XMAX, y)
                moves += [Transform(g.rect, new.rect), g.ta.animate.move_to(new.ta), g.tb.animate.move_to(new.tb),
                          g.la.animate.move_to(new.la), g.lb.animate.move_to(new.lb)]
            self.play(*moves, run_time=2.0)
            self.S, self.pk, self.pu = S, pk, pu

    # ---- c2.range.2 ----------------------------------------------------------------------------
    def clip2(self):
        pk, pu = self.pk, self.pu
        with self.say("c2.range.2") as c:
            su_tag = T("set-up: latest settle", 36, GOLD).move_to([XMAX, PU_Y + 1.0, 0])
            self.play(*appear(su_tag), run_time=1.0)
            c.wait_until("longest delays")
            cmax = column(XMAX)
            self.play(FadeIn(cmax), FlashAround(pu.tb, color=YELLOW), FlashAround(pk.tb, color=YELLOW),
                      run_time=1.5)

            c.wait_until("shortest")
            h_tag = T("hold: earliest change", 36, GOLD).move_to([XMIN, PK_Y - 1.0, 0])
            self.play(*appear(h_tag), run_time=1.0)  # early: "hold" opens the sentence it tags
            cmin = column(XMIN)
            self.play(FadeIn(cmin), FlashAround(pu.ta, color=YELLOW), FlashAround(pk.ta, color=YELLOW),
                      run_time=1.5)

            c.wait_until("opposite ends")
            self.play(*flash([cmin, cmax], color=YELLOW, time_width=1.5), run_time=min(1.6, c.until(floor=0.8)))
            self.cols = [cmin, cmax, su_tag, h_tag]

    # ---- c2.range.3 ----------------------------------------------------------------------------
    def clip3(self):
        pk, pu = self.pk, self.pu
        dx = 1.5 * LEFT
        card_t = T("Harris & Harris", 34, FG)
        card_b = RoundedRectangle(corner_radius=0.12, width=card_t.width + 0.7, height=card_t.height + 0.6)
        card_b.set_stroke(DIM, 2).set_fill(BG, 1)
        card = VGroup(card_b, card_t.move_to(card_b)).move_to([-4.2, 2.7, 0])
        with self.say("c2.range.3") as c:
            sweep_clear(self, *during([pk.animate.shift(dx), pu.animate.shift(dx)], 0.35, 0.9),
                        *during(appear(card), 0.55, 1.0), keep=[pk, pu], run_time=1.8)

            c.wait_until("cq")
            cq = VGroup(MathTex(r"(t_{pc})_{\min}:", font_size=48, color=PINK),
                        T("clock-to-Q contamination delay", 32, FG)).arrange(RIGHT, buff=0.25)
            cq.next_to(pk.la, DOWN, buff=0.45, aligned_edge=LEFT)
            self.play(FlashAround(pk.ta, color=PINK), *appear(cq), run_time=1.5)  # early: the definition the sentence reads

            c.wait_until("comb")
            comb = VGroup(MathTex(r"(t_{pd})_{\min}:", font_size=48, color=PURPLE),
                          T("combinational contamination delay", 32, FG)).arrange(RIGHT, buff=0.25)
            comb.next_to(pu.la, DOWN, buff=0.45, aligned_edge=LEFT)
            self.play(FlashAround(pu.ta, color=PURPLE), *appear(comb), run_time=1.5)  # early: the definition the sentence reads

            # {meaning}: a D1 trace; from the earliest change a RED smudge spreads into the hatching
            c.wait_until("meaning")
            ty, x0, xc, xh, x1 = 2.55, 0.3, 2.0, 4.6, 6.1
            tr = bus(x0, x1, ty, hatch(xc, xh, 4) + [(xh, xh)], h=0.6, color=BLUE)
            d1 = MathTex("D_1", font_size=44, color=BLUE).next_to(_p(x0, ty), LEFT, buff=0.2)
            self.play(*appear(d1, tr, shift=None, lag=0.2), run_time=1.2)
            c.wait_until("earliest")
            smudge = Rectangle(width=xh - xc, height=0.75).set_stroke(width=0).set_fill(RED, 0.4)
            smudge.move_to([(xc + xh) / 2, ty, 0]).set_z_index(-1)
            tag = T("contaminated", 32, RED).next_to(smudge, DOWN, buff=0.15)
            self.play(GrowFromEdge(smudge, LEFT), *[x.animate.set_stroke(RED) for x in tr.xs],
                      *during(appear(tag), 0.6, 1.0), rate_func=linear, run_time=2.0)

    # ---- c2.range.4 ----------------------------------------------------------------------------
    def clip4(self):
        H = hold_budget()
        L, x0 = TC_LEN, BAR_X0
        mn = stack(L, x0, 0.1, 0.15, 0.4)
        mx = stack(L, x0, -0.6, 0.25, 0.8)
        mn_l = sum_label("min").next_to(_p(x0, mn.get_y()), LEFT, buff=0.3)
        mx_l = sum_label("max").next_to(_p(x0, mx.get_y()), LEFT, buff=0.3)
        bot = H.bar.outline.get_bottom()[1]
        ga = DashedLine([H.xa, mn.get_top()[1], 0], [H.xa, bot, 0], dash_length=0.1).set_stroke(DIM, 2)
        gb = DashedLine([H.xb, mx.get_top()[1], 0], [H.xb, bot, 0], dash_length=0.1).set_stroke(DIM, 2)
        with self.say("c2.range.4") as c:
            # fix pass: the bar grows only after the board is clear (a held start state showed a stray dot),
            # and the T_c arrow and the fences fade in whole (a scaled-down Arrow keeps full-size tips).
            sweep_clear(self, run_time=1.0)
            self.play(GrowFromEdge(H.bar.outline, LEFT),
                      *during(appear(H.arrow, H.bar.tc, *H.edges, shift=None, lag=0.1), 0.3, 1.0), run_time=1.2)  # early: one clock period
            self.play(GrowFromEdge(H.su, LEFT), FadeIn(H.fence), FadeIn(H.deadline),
                      *appear(H.fence_l, H.su_l, lag=0.2), run_time=min(1.2, c.until("spread")))  # early: the budget's two fences shown whole

            c.wait_until("spread")
            self.play(*during([GrowFromEdge(mn[0], LEFT)], 0, 0.25), *during([GrowFromEdge(mn[1], LEFT)], 0.2, 0.45),
                      *during(appear(mn_l, shift=None), 0.35, 0.55),
                      *during([GrowFromEdge(mx[0], LEFT)], 0.45, 0.7), *during([GrowFromEdge(mx[1], LEFT)], 0.65, 0.9),
                      *during(appear(mx_l, shift=None), 0.8, 1.0), run_time=2.2)
            c.wait_until("latest")
            self.play(Create(ga), Create(gb), *during([GrowFromCenter(H.stretch)], 0.3, 1.0),
                      *during(appear(H.may_l), 0.5, 1.0), run_time=min(1.4, c.until("fence")))

            c.wait_until("fence")
            tk1 = check_mark(GREEN).scale(0.7).move_to([(H.xf + H.xa) / 2, BAR_Y, 0]).set_z_index(3)
            self.play(FlashAround(H.fence, color=GOLD), FlashAround(H.stretch.box.copy().stretch(0.05, 0, about_edge=LEFT), color=BLUE),
                      *during([GrowFromCenter(tk1)], 0.5, 1.0), run_time=1.5)
            c.wait_until("deadline")
            tk2 = check_mark(GREEN).scale(0.7).move_to([(H.xb + H.xd) / 2, BAR_Y, 0]).set_z_index(3)
            self.play(FlashAround(H.deadline, color=GOLD), FlashAround(H.stretch.box.copy().stretch(0.05, 0, about_edge=RIGHT), color=BLUE),
                      *during([GrowFromCenter(tk2)], 0.5, 1.0), run_time=1.5)

            c.wait_until("max")
            t_max = arrow_tag("max delays", "clock rate", YELLOW).move_to([0.2, -1.75, 0])
            self.play(FlashAround(mx, color=YELLOW, time_width=1.5), FlashAround(H.arrow, color=YELLOW, time_width=1.5),
                      *during(appear(t_max), 0.3, 1.0), run_time=1.6)
            c.wait_until("min")
            t_min = arrow_tag("contamination delays", "hold", GOLD).move_to([0.2, -2.65, 0])
            self.play(FlashAround(mn, color=GOLD, time_width=1.5), FlashAround(H.fence, color=GOLD, time_width=1.5),
                      *during(appear(t_min), 0.3, 1.0), run_time=min(1.6, c.until(floor=0.8)))
