"""Chapter 3, scene 6: the skew the other way round; the shift-register race; the middle flip-flop.
Clips c3.other.1 – c3.other.3.

Copied (not imported): make_ff / path_diagram / split_path, clock_wave / dim_arrow / guide,
budget_bar / tc_arrow and skew_fences() from ch3_s5_skewhold.py; the small traces' look from
ch3_s2_skew.py; the shift register (make_ff without Q-bar, K = 0.6, FF_X, GOLD digit) from
ch2_s3_shiftreg.py, with its clock now coming from a source at the left.

Shared with the recap: skew_fences(skew, x0, y, L) takes a negative skew too (CLK1 *late*): the hold
fence at (hold - skew) = 0.4, the deadline at the bar's right end, the GOLD t_su segment poking out
past it (up to CLK1's late edge), the TEAL t_skew arrows pointing right; no TEAL bar segment. For
skew < 0 the t_hold label sits left of its fence and "D1 may change" is left-aligned in the stretch.
s5's end shot is skew_fences(0.1) at the default place; here it is re-laid at x0 -5.6, y -0.6, L 6.
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
# make_ff + path_diagram + split_path, copied from ch3_s5_skewhold.py
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


def src_icon(center, r=SRC_R):
    """split_path()'s clock source: a YELLOW ring with a square-wave glyph."""
    ring = Circle(radius=SRC_R).set_stroke(YELLOW, 4).set_fill(BG, 1)
    sq = VMobject().set_points_as_corners([_p(-0.17, -0.08), _p(-0.08, -0.08), _p(-0.08, 0.08),
                                           _p(0.04, 0.08), _p(0.04, -0.08), _p(0.17, -0.08)])
    sq.set_stroke(YELLOW, 3)
    g = VGroup(ring, sq)
    if r != SRC_R:
        g.scale(r / SRC_R)
    return g.move_to(center)


def branch_pts(reverse=False):
    """Corner lists (full size) of the two clock branches: source at the right (CLK1 short) or,
    reversed, at the left (CLK0 short, CLK1 the long one round the bottom)."""
    x0, x1 = P_FF_X
    if not reverse:
        b1 = [_p(SRC_X - SRC_R, P_BUS), _p(x1, P_BUS), _p(x1, TRI_Y)]
        b0 = [_p(SRC_X, P_BUS - SRC_R), _p(SRC_X, LONG_Y), _p(x0, LONG_Y), _p(x0, TRI_Y)]
    else:
        b0 = [_p(-SRC_X + SRC_R, P_BUS), _p(x0, P_BUS), _p(x0, TRI_Y)]
        b1 = [_p(-SRC_X, P_BUS - SRC_R), _p(-SRC_X, LONG_Y), _p(x1, LONG_Y), _p(x1, TRI_Y)]
    return b0, b1


def split_path():
    """ch1_s4's path with the clock split (p. 107): a source at the right, a short branch to FF1
    (.clk_br1, dimmer) and a long one round to FF0 (.clk_br0)."""
    P = path_diagram()
    P.remove(P.clk_bus, P.clk_dot, P.clk_l, P.clk_br0, P.clk_br1)
    P.src = src_icon(_p(SRC_X, P_BUS))
    b0, b1 = branch_pts()
    P.clk_br1 = VMobject().set_points_as_corners(b1).set_stroke(YELLOW, 5, opacity=CLK1_OP)
    P.clk_br0 = VMobject().set_points_as_corners(b0).set_stroke(YELLOW, 5)
    P.all = [P.ff0, P.ff1, *P.names, P.cl, P.cl_l, P.q0_w, P.q0_l, P.d1_w, P.d1_l, P.d0_l, P.q1_l,
             P.clk_br0, P.clk_br1, P.src]
    P.add(P.clk_br0, P.clk_br1, P.src)
    return P
# =============================================================================================


# =============================================================================================
# Data-sheet timing-diagram kit, copied from ch1_s5_datasheet.py (via ch3_s5)
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


def grow_out(arr):
    """A dimension arrow growing out of arr.pa to arr.pb (ch3_s5)."""
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
# =============================================================================================


# =============================================================================================
# THE lecture's budget bar + the fence picture at any skew (ch3_s5's skew_fences, extended)
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


def tc_arrow(xa, xb, y):
    return DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.4, color=YELLOW)


FB_L = 7.0          # one CLK0 period
FB_X0 = -3.5        # bar x -3.5 .. 3.5
FB_Y = -0.8         # bar centre row


def skew_fences(skew=0.0, x0=FB_X0, y=FB_Y, L=FB_L, hold=0.3, su=0.1, lo=0.4, hi=0.8, sk_size=32,
                may_size=30):
    """One CLK0 period with both fences, measured from CLK0's edge, when CLK1 is `skew` (fraction of
    the period) ahead; skew < 0: CLK1 is -skew late. Parts as ch3_s5: .bar (.outline .tc) .su (GOLD
    t_su segment) .arrow (T_c) .edges .fence (hold, at hold-skew) .fence_l .deadline (at 1-su-skew)
    .su_l .stretch (.box .hatch, lo..hi) .may_l; skew > 0: .skseg (TEAL, the last `skew` of the bar);
    skew != 0: .sk_arrows (TEAL DoubleArrows, old -> new fence place; .pa old end, .pb new end) with
    .sk_labels. xs: .xf .xd .xa .xb."""
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
    dx = 0.08 if skew > 0 else (0.16 if skew < 0 else -0.08)
    H.su_l.move_to([seg.get_x() + dx, 0, 0]).align_to(H.fence_l, DOWN)
    a, b = x0 + lo * L, x0 + hi * L
    box = Rectangle(width=b - a, height=BAR_H).set_stroke(BLUE, 3).set_fill(BLUE, 0.22)
    box.move_to([(a + b) / 2, y, 0])
    hl = VGroup(*[Line([x, y - BAR_H / 2, 0], [x + BAR_H, y + BAR_H / 2, 0]).set_stroke(BLUE, 2)
                  for x in np.arange(a + 0.08, b - BAR_H, 0.3)])
    H.stretch = VGroup(box, hl)
    H.stretch.box, H.stretch.hatch = box, hl
    H.may_l = T("D1 may change", may_size, BLUE).move_to([(a + b) / 2, 0, 0]).align_to(H.fence_l, DOWN)
    H.may_l.shift(0.04 * UP)
    if skew < 0:    # the hold fence is at the stretch: its label steps to the left of it
        H.fence_l.align_to(_p(xf - 0.1, 0), RIGHT)
        H.may_l.align_to(_p(a + 0.12, 0), LEFT)
    elif H.may_l.get_right()[0] > H.su_l.get_left()[0] - 0.12:   # a short bar: keep it clear of t_su
        H.may_l.align_to(_p(H.su_l.get_left()[0] - 0.12, 0), RIGHT)
    H.xf, H.xd, H.xa, H.xb = xf, xd, a, b
    H.add(H.bar, H.arrow, H.edges, H.fence, H.deadline, H.fence_l, H.su_l, H.stretch, H.may_l)
    H.skseg, H.sk_arrows, H.sk_labels = None, [], []
    if skew > 0:
        H.skseg = Rectangle(width=skew * L, height=BAR_H).set_stroke(width=0).set_fill(TEAL, BAR_FILL)
        H.skseg.move_to([x0 + (1 - skew / 2) * L, y, 0])
        H.add(H.skseg)
    if skew != 0:
        ys = y - BAR_H / 2 - 0.8
        for xo, xn in ((x0 + hold * L, xf), (x0 + (1 - su) * L, xd)):
            arr = DoubleArrow([xn, ys, 0], [xo, ys, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                              max_tip_length_to_length_ratio=0.4, color=TEAL)
            arr.pa, arr.pb = _p(xo, ys), _p(xn, ys)
            H.sk_arrows.append(arr)
            H.sk_labels.append(MathTex("t_{skew}", font_size=sk_size, color=TEAL).next_to(arr, DOWN, buff=0.12))
        H.add(*H.sk_arrows, *H.sk_labels)
    return H
# =============================================================================================


# =============================================================================================
# ch2_s3's shift register (make_ff without Q-bar, K = 0.6), clock now from a source at the left
# =============================================================================================
K = 0.6
FF_X = (-3.6, -0.2, 3.2)
HX = (BOX_W / 2 + WIRE) * K          # box centre to the end of a pin wire (0.96)


def sr_ff():
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    g = VGroup(d_w, q_w, box, tri, d_l, q_l)
    g.box, g.tri, g.d_w, g.q_w, g.d_l, g.q_l, g.clk_w = box, tri, d_w, q_w, d_l, q_l, clk_w
    return g


def build_chain(fy, ff_x=FF_X, taps=True, src_dx=1.6):
    """ch2_s3's build_chain; the bus starts at a clock source src_dx left of FF0 (no CLK label)."""
    C = VGroup()
    C.ffs = []
    for x in ff_x:
        f = sr_ff()
        f.scale(K, about_point=ORIGIN).shift(_p(x, fy))
        f.clk_w.scale(K, about_point=ORIGIN).shift(_p(x, fy))
        for lb in (f.d_l, f.q_l):
            lb.scale(1.3, about_point=lb.get_center())
        C.ffs.append(f)
    qy = fy + PIN_Y * K
    C.qy = qy
    C.links = [Line(_p(ff_x[i] + HX, qy), _p(ff_x[i + 1] - HX, qy)).set_stroke(GREEN, 5) for i in range(2)]
    C.names = [T(f"FF{i}", 32).next_to(f.box, UP, buff=0.15) for i, f in enumerate(C.ffs)]
    by = fy - (BOX_H / 2 + EN_WIRE) * K
    C.by = by
    r = 0.24
    C.src = src_icon(_p(ff_x[0] - src_dx, by), r=r)
    C.bus = Line(_p(ff_x[0] - src_dx + r, by), _p(ff_x[2], by)).set_stroke(YELLOW, 5)
    C.jdots = [Dot(_p(x, by), radius=0.07, color=YELLOW) for x in ff_x[:2]]
    C.clk_ws = [f.clk_w for f in C.ffs]
    C.all = [*C.ffs, *C.names, *C.links, C.src, C.bus, *C.jdots, *C.clk_ws]
    if taps:
        C.tail = Line(_p(ff_x[2] + HX, qy), _p(ff_x[2] + HX + 0.45, qy)).set_stroke(GREEN, 5)
        rx = [(ff_x[0] + ff_x[1]) / 2, (ff_x[1] + ff_x[2]) / 2, ff_x[2] + HX + 0.45]
        top = fy + BOX_H / 2 * K + 0.22
        C.risers = [Line(_p(x, qy), _p(x, top)).set_stroke(GREEN, 5) for x in rx]
        C.dots = [Dot(_p(x, qy), radius=0.07, color=GREEN) for x in rx[:2]]
        C.qls = [MathTex(f"Q_{i}", font_size=40, color=GREEN).next_to(_p(x, top), UP, buff=0.1)
                 for i, x in enumerate(rx)]
        C.din = MathTex("D_{in}", font_size=40, color=BLUE).next_to(C.ffs[0].d_w.get_start(), LEFT, buff=0.12)
        C.all += [C.tail, *C.risers, *C.dots, *C.qls, C.din]
    return C


def digit_pos(ff):
    b = ff.box
    return b.get_center() + DOWN * 0.19 * b.height


def digit(s, ff, color=GOLD, size=40):
    return T(s, size, color).move_to(digit_pos(ff))
# =============================================================================================


# ---- clip 1 layout ---------------------------------------------------------------------------
FL, FX0, FY = 5.6, -5.7, -0.8        # the fence picture, re-laid left of s5's place
HOLD_C, SETUP_C = _p(-3.5, 2.35), _p(3.5, 2.35)   # s5's two rules, unchanged
RS = 36
HOLD_PARTS = ["t_{skew}", "+", "(", "t_{pc}", "+", "t_{pd}", ")", r"_{\min}", r"\geq", "t_{hold}"]
HOLD_COLS = {0: TEAL, 3: PINK, 5: PURPLE, 7: YELLOW, 9: GOLD}
HOLD2_PARTS = ["(", "t_{pc}", "+", "t_{pd}", ")", r"_{\min}", r"\geq", "t_{hold}", "+", "t_{skew}"]
SU_PARTS = ["T_c", r"\geq", "(", "t_{pc}", "+", "t_{pd}", ")", r"_{\max}", "+", "t_{su}", "+", "t_{skew}"]
SU_COLS = {0: YELLOW, 3: PINK, 5: PURPLE, 9: GOLD, 11: TEAL}

PSC = 0.36                            # the small path (split_path, lettering off)
PS_C = _p(4.0, 0.42)
TL_X = 2.1                            # small traces: labels, extent, rows, edges
TW_X0, TW_X1 = 2.9, 6.6
TY0, TY1, TY_SK = -1.0, -1.8, -2.35
TH, TSL = 0.5, 0.25
CE = [3.8, 4.95, 6.1]
SK = 0.45


def rule_terms(parts, cols, center, size=RS):
    full = MathTex(*parts, font_size=size).move_to(center)
    return [MathTex(s, font_size=size, color=cols.get(i, FG)).move_to(full[i]) for i, s in enumerate(parts)]


def place_small(m):
    return m.scale(PSC, about_point=ORIGIN).shift(PS_C - PSC * _p(0, -0.375))


def small_path():
    P = split_path()
    for f in (P.ff0, P.ff1):
        f.remove(f.d_l, f.q_l, f.qb_l)
    P.remove(*P.names, P.cl_l, P.q0_l, P.d1_l, P.d0_l, P.q1_l)
    place_small(P)
    return P


def clk1_wave(k):
    return clock_wave(TW_X0, TW_X1, TY1, [e + k for e in CE if e + k < TW_X1 - TSL], h=TH,
                      slope=TSL).set_stroke(opacity=CLK1_OP)


def small_traces(k):
    D = type("Small", (), {})()
    D.lab0 = T("CLK0", 30, YELLOW).move_to(_p(TL_X, TY0))
    D.lab1 = T("CLK1", 30, YELLOW).move_to(_p(TL_X, TY1)).set_opacity(0.7)
    D.clk0 = clock_wave(TW_X0, TW_X1, TY0, CE, h=TH, slope=TSL)
    D.clk1 = clk1_wave(k)
    D.g_e = guide(CE[0], TY0 + TH / 2, TY_SK - 0.15)
    D.g_k = guide(CE[0] + k, TY1 - TH / 2, TY_SK - 0.15)
    D.sk = dim_arrow(min(CE[0], CE[0] + k), max(CE[0], CE[0] + k), TY_SK, TEAL, "t_{skew}",
                     label_dir=DOWN, size=32)
    D.parts = [D.lab0, D.lab1, D.clk0, D.clk1, D.g_e, D.g_k, D.sk]
    return D


# ---- clip 2 layout ---------------------------------------------------------------------------
SR_Y = 1.4                            # the shift register's flip-flop row
R_LX = -5.7                           # its two traces: labels, extent, rows
R_X0, R_X1 = -5.0, 1.4
R_Y0, R_Y1, R_YS, R_YP = -1.2, -2.0, -2.65, -3.2
R_E, R_SK, R_PC = -3.2, 1.5, 0.9
ROW2_Y = -1.3                         # {two}: the RED tag and the ghost
ROW3_Y = -2.75                        # {nofix}: the rule and the slower clock

# ---- clip 3 layout ---------------------------------------------------------------------------
FF_X3 = (-4.2, 0.0, 4.2)
ROW_Y3 = 0.8


class OtherWay(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- c3.other.1: s5's fences; the skew turned round; both fences slide later ---------------
    def clip1(self):
        H, Hn = skew_fences(0.1, FX0, FY, FL, may_size=28), skew_fences(-0.1, FX0, FY, FL, may_size=28)
        hold = rule_terms(HOLD_PARTS, HOLD_COLS, HOLD_C)
        setup = rule_terms(SU_PARTS, SU_COLS, SETUP_C)
        easy = T("easier", 30, GREEN).next_to(VGroup(*[m.copy() for m in hold]), DOWN, buff=0.3)
        hard = T("harder", 30, RED).next_to(VGroup(*[m.copy() for m in setup]), DOWN, buff=0.3)
        P = small_path()
        D = small_traces(-SK)
        with self.say("c3.other.1") as c:
            # {flip}: s5's end shot, re-laid; the small path and its traces beside it
            self.play(*[FadeIn(m) for m in H.submobjects], *[FadeIn(m) for m in (*hold, *setup, easy, hard)], FadeIn(P), *[FadeIn(m) for m in D.parts], run_time=1.0)  # early: s5's end shot and s2's small path return whole
            c.wait_until("lags")
            b0, b1 = branch_pts(reverse=True)
            nb0 = place_small(VMobject().set_points_as_corners(b0)).set_stroke(YELLOW, 5)
            nb1 = place_small(VMobject().set_points_as_corners(b1)).set_stroke(YELLOW, 5, opacity=CLK1_OP)
            s_to = place_small(src_icon(_p(-SRC_X, P_BUS))).get_center()
            new = small_traces(SK)
            self.play(MoveAlongPath(P.src, ArcBetweenPoints(P.src.get_center(), s_to, angle=-PI / 3)),
                      Transform(P.clk_br0, nb0), Transform(P.clk_br1, nb1),
                      Transform(D.clk1, new.clk1), Transform(D.g_k, new.g_k),
                      Transform(D.sk[0], new.sk[0]), D.sk[1].animate.move_to(new.sk[1]),
                      run_time=min(2.0, c.until("slide", floor=1.2)))
            # {slide}: both fences 0.2 of the period later
            c.wait_until("slide")
            moves = [(H.fence, Hn.fence), (H.fence_l, Hn.fence_l), (H.deadline, Hn.deadline),
                     (H.su, Hn.su), (H.su_l, Hn.su_l), (H.may_l, Hn.may_l)]
            self.play(*during(disappear(*H.sk_arrows, *H.sk_labels), 0, 0.35),
                      *during([H.skseg.animate.stretch(0.02, 0, about_edge=RIGHT).set_opacity(0)], 0, 0.5),
                      *during([a.animate.move_to(b) for a, b in moves], 0.15, 0.85),
                      *during([grow_out(a) for a in Hn.sk_arrows], 0.45, 1.0), run_time=2.0)
            self.remove(H.skseg)
            self.play(*appear(*Hn.sk_labels, shift=None, lag=0.2), run_time=0.7)
            # {setup}: the deadline has left the stretch; the set-up rule's skew turns to minus
            c.wait_until("setup")
            gap = Rectangle(width=Hn.xd - Hn.xb, height=BAR_H).move_to(_p((Hn.xd + Hn.xb) / 2, FY))
            easy2 = T("easier", 30, GREEN).move_to(hard)
            self.play(FlashAround(gap, color=GREEN, time_width=1.5, buff=0.05), *swap(hard, easy2), run_time=1.3)
            c.wait_until("minus")
            minus = MathTex("-", font_size=RS).move_to(setup[10])
            self.play(*swap(setup[10], minus), FlashAround(setup[11], color=TEAL, time_width=1.5), run_time=1.3)
            # {hold}: the hold fence now touches the stretch; the rule takes + t_skew on the right
            c.wait_until("hold")
            touch = Rectangle(width=0.5, height=BAR_H + 0.3).move_to(_p(Hn.xf, FY))
            hard2 = T("harder", 30, RED).move_to(easy)
            self.play(FlashAround(touch, color=RED, time_width=1.5), *swap(easy, hard2), run_time=1.3)
            c.wait_until("at least")
            full2 = MathTex(*HOLD2_PARTS, font_size=RS).move_to(HOLD_C)
            order = [9, 8] + list(range(8))          # old index -> new index
            plus2 = MathTex("+", font_size=RS).move_to(full2[8])
            self.play(hold[0].animate(path_arc=-0.35 * PI).move_to(full2[order[0]]),   # a low arc over the others
                      *during(disappear(hold[1]), 0, 0.3), *during(appear(plus2, shift=None), 0.75, 1.0),
                      *during([hold[i].animate.move_to(full2[order[i]]) for i in range(2, 10)], 0.2, 0.9),
                      run_time=min(1.8, c.until("plus the skew", floor=1.2)))
            c.wait_until("plus the skew")
            self.play(FlashAround(hold[0], color=TEAL, time_width=1.5), run_time=min(1.2, c.until(floor=0.6)))

    # -- c3.other.2: the shift register races ---------------------------------------------------
    def clip2(self):
        C = build_chain(SR_Y)
        self.C = C
        lab0 = T("CLK0", 30, YELLOW).next_to(C.jdots[0], RIGHT, buff=0.1).next_to(C.bus, DOWN, buff=0.14, coor_mask=[0, 1, 0])   # under the bus, same clearance
        lab1 = T("CLK1", 30, YELLOW).next_to(C.jdots[1], RIGHT, buff=0.1).next_to(C.bus, DOWN, buff=0.14, coor_mask=[0, 1, 0])   # under the bus, same clearance
        with self.say("c3.other.2") as c:
            # {shift}: clear to ch2's shift register, clock from the left
            self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.45), *during([FadeIn(m) for m in C.all], 0.5, 1.0), run_time=1.8)  # early: ch2's shift register returns whole
            c.wait_until("no logic")
            self.play(*flash(C.links, color=GREEN), run_time=1.2)
            c.wait_until("slow the data")
            s = C.bus.get_start()
            p0 = VMobject().set_points_as_corners([s, C.clk_ws[0].get_start(), C.clk_ws[0].get_end()])
            p1 = VMobject().set_points_as_corners([s, C.clk_ws[1].get_start(), C.clk_ws[1].get_end()])
            self.play(*[VShowPassingFlash(p.copy().set_stroke(YELLOW, 10), time_width=0.5, rate_func=linear)
                        for p in (p0, p1)], *appear(lab0, lab1, shift=None, lag=0.3), run_time=1.4)  # early: the branch names
            # {late}: t_hold = 0; the two traces; t_skew against (t_pc)_min
            th0 = MathTex(r"t_{hold} = 0", font_size=40, color=GOLD).move_to(_p(4.3, -1.6))
            c.wait_until(own_word=th0)
            self.play(*appear(th0), run_time=1.0)
            rl0 = T("CLK0", 30, YELLOW).move_to(_p(R_LX, R_Y0))
            rl1 = T("CLK1", 30, YELLOW).move_to(_p(R_LX, R_Y1))
            w0 = clock_wave(R_X0, R_X1, R_Y0, [R_E], h=TH, slope=TSL)
            w1 = clock_wave(R_X0, R_X1, R_Y1, [R_E + R_SK], h=TH, slope=TSL)
            g0 = guide(R_E, R_Y0 + TH / 2, R_YP - 0.15)
            g1 = guide(R_E + R_SK, R_Y1 - TH / 2, R_YS - 0.15)
            c.wait_until("flip-flop one's")
            self.play(*appear(rl0, rl1, shift=None, lag=0.2), sweep_in(w0, R_X0, R_X1), sweep_in(w1, R_X0, R_X1),
                      run_time=1.4, rate_func=linear)  # early: the two rows drawn together
            sk = dim_arrow(R_E, R_E + R_SK, R_YS, TEAL, "t_{skew}", label_dir=RIGHT, size=36)
            c.wait_until("late by")
            self.play(FadeIn(g0), FadeIn(g1), grow_dim(sk[0]), *during(appear(sk[1], shift=None), 0.4, 1.0),
                      run_time=1.3)
            pc = dim_arrow(R_E, R_E + R_PC, R_YP, PINK, r"(t_{pc})_{\min}", label_dir=RIGHT, size=36)
            pc.pa, pc.pb = _p(R_E, R_YP), _p(R_E + R_PC, R_YP)
            pc[0].pa, pc[0].pb = pc.pa, pc.pb
            c.wait_until("shortest")
            self.play(grow_out(pc[0]), *during(appear(pc[1], shift=None), 0.4, 1.0), run_time=1.4)
            # {race}: D_in = 1, all three hold 0
            c.wait_until("race")
            din1 = MathTex(r"D_{in} = 1", font_size=40, color=BLUE)
            din1.align_to(C.din, RIGHT).set_y(C.din.get_y())
            zeros = [digit("0", f) for f in C.ffs]
            self.play(*edit(C.din, din1), *appear(*zeros, shift=None, lag=0.15), run_time=1.3)
            C.din = din1
            # the edge reaches FF0: it takes the 1
            c.wait_until("takes in")
            ones = [digit("1", f) for f in C.ffs[:2]]
            v = 1.6
            t0 = p0.get_arc_length() / v
            self.play(VShowPassingFlash(p0.copy().set_stroke(YELLOW, 10), time_width=0.4, rate_func=linear),
                      time_span(FlashAround(C.ffs[0].tri, color=YELLOW, buff=0.08), t0 * 0.9, t0 * 0.9 + 0.7),
                      *[time_span(a, t0 * 0.9, t0 * 0.9 + 0.9) for a in swap(zeros[0], ones[0])],
                      run_time=t0 * 0.9 + 0.9)
            # it passes straight on: a 1 runs along the wire while the edge is still on its way to FF1
            c.wait_until("passes it")
            run1 = T("1", 40, GOLD).move_to(_p(FF_X[0] + HX + 0.25, C.qy + 0.3))
            end1 = _p(FF_X[1] - HX - 0.25, C.qy + 0.3)
            rest = VMobject().set_points_as_corners([C.clk_ws[0].get_start(), C.clk_ws[1].get_start(),
                                                     C.clk_ws[1].get_end()]).set_stroke(YELLOW, 10)
            self.play(*during(appear(run1, shift=None), 0, 0.15), FlashAround(C.qls[0], color=GREEN, time_width=1.5),
                      *during([run1.animate.move_to(end1)], 0.12, 0.55),
                      VShowPassingFlash(rest, time_width=0.35, rate_func=linear),
                      run_time=max(2.0, min(3.5, c.until("catches", floor=2.0))))
            # the late edge catches it at FF1 too
            c.wait_until("catches")
            self.play(FlashAround(C.ffs[1].tri, color=YELLOW, buff=0.08), *during(disappear(run1), 0, 0.4),
                      *swap(zeros[1], ones[1]), run_time=1.3)
            # {two}: the 1 in two places; the correct state as a ghost
            c.wait_until("two")
            gone = [rl0, rl1, w0, w1, g0, g1, sk, pc, th0]
            tag = T("two places in one edge", 36, RED).move_to(_p(-1.9, ROW2_Y))
            self.play(*during(disappear(*gone), 0, 0.45), *during(appear(tag), 0.45, 1.0),
                      *during(flash(ones, color=RED, time_width=1.5), 0.45, 1.0), run_time=1.8)
            ghost = VGroup(*[f.box.copy() for f in C.ffs], *[ln.copy() for ln in C.links])
            ghost.scale(0.55).move_to(_p(4.0, ROW2_Y))
            ghost.set_stroke(GREEN, 3, opacity=0.5)
            gd = [T(s, 30, GREEN).set_opacity(0.6).move_to(b.get_center()) for s, b in zip("100", ghost[:3])]
            ok = check_mark(GREEN).scale(0.7).next_to(ghost, UP, buff=0.15)
            self.play(*appear(ghost, *gd, shift=None, lag=0.1), GrowFromCenter(ok), run_time=1.2)  # early: the right answer, shown under the pause
            # {nofix}: the hold rule, no T_c in it; a slower clock struck out
            c.wait_until("hold violation")
            rule = MathTex(*HOLD2_PARTS, font_size=44).move_to(_p(-1.9, ROW3_Y))
            for i, col in {1: PINK, 3: PURPLE, 7: GOLD, 9: TEAL}.items():
                rule[i].set_color(col)
            self.play(*appear(rule, shift=None), FlashAround(tag, color=RED, time_width=1.5), run_time=1.3)
            fast = clock_wave(2.6, 5.4, ROW3_Y, [2.95, 3.45, 3.95, 4.45, 4.95], h=0.5, slope=0.2)
            slow = clock_wave(2.6, 5.4, ROW3_Y, [3.1, 4.4], h=0.5, slope=0.2)
            c.wait_until("as we saw")
            self.play(*during([Create(fast)], 0, 0.4), *during([Transform(fast, slow)], 0.5, 1.0), run_time=1.6)
            strike = Line(_p(2.5, ROW3_Y - 0.45), _p(5.5, ROW3_Y + 0.45)).set_stroke(RED, 7)
            c.wait_until("no slower clock")
            self.play(GrowFromEdge(strike, LEFT), run_time=min(0.9, c.until(floor=0.5)))

    # -- c3.other.3: a middle flip-flop sees the skew both ways ---------------------------------
    def clip3(self):
        R = build_chain(ROW_Y3, ff_x=FF_X3, taps=False, src_dx=1.8)
        with self.say("c3.other.3") as c:
            # {advice}: clear to a three-flip-flop row
            c.wait_until("which way")
            self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.45), *during([FadeIn(m) for m in R.all], 0.5, 1.0), run_time=1.8)  # early: the row returns whole
            # {both}: which way? FF1's branch singled out
            q = T("?", 52, YELLOW).next_to(R.clk_ws[1], RIGHT, buff=0.2)
            c.wait_until("both")
            self.play(*appear(q, shift=None), *set_alpha([R.clk_ws[0], R.clk_ws[2]], 0.4),
                      FlashAround(R.clk_ws[1], color=YELLOW, time_width=1.5), run_time=1.2)  # early: the question mark
            # {middle}: data in, data out
            ay = R.qy + 0.32
            a_in = Arrow(_p(FF_X3[0] + HX + 0.3, ay), _p(FF_X3[1] - HX - 0.3, ay), buff=0, stroke_width=5,
                         color=FG, tip_length=0.22)
            a_out = Arrow(_p(FF_X3[1] + HX + 0.3, ay), _p(FF_X3[2] - HX - 0.3, ay), buff=0, stroke_width=5,
                          color=FG, tip_length=0.22)
            c.wait_until("take data in")
            self.play(GrowArrow(a_in), run_time=1.2)
            c.wait_until("pass it on")
            self.play(GrowArrow(a_out), run_time=1.2)
            # {inpath}: FF1 late; hold harder on the way in
            late = T("late", 34, TEAL).next_to(R.clk_ws[1], RIGHT, buff=0.2)
            c.wait_until("inpath")
            self.play(*swap(q, late), run_time=1.2)
            h_l = T("hold harder", 32, RED).next_to(a_in, UP, buff=0.15)
            c.wait_until("hold gets harder")
            self.play(a_in.animate.set_color(RED), FlashAround(a_in, color=RED, time_width=1.5),
                      *appear(h_l), run_time=1.3)
            # {outpath}: set-up harder on the way out
            s_l = T("set-up harder", 32, RED).next_to(a_out, UP, buff=0.15)
            c.wait_until("outpath")
            self.play(a_out.animate.set_color(RED), FlashAround(a_out, color=RED, time_width=1.5),
                      *appear(s_l), run_time=1.3)
            c.wait_until("its own data")
            # a stretch of FF1's own output wire brightens and runs along it (same stroke width, no taper)
            wire = R.links[1]
            self.play(VShowPassingFlash(wire.copy().set_stroke(ManimColor(GREEN).interpolate(ManimColor(WHITE), 0.6), wire.get_stroke_width()),
                                        time_width=0.3, taper_width=0.0, rate_func=linear),
                      run_time=1.2)
            # {check}
            cap = T("check skew both ways: it affects both rules", 36).move_to(_p(0, -2.1))
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.0)
