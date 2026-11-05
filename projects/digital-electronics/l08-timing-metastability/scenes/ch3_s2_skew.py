"""Chapter 3, scene 2: what skew is. Clips c3.skew.1 – c3.skew.3.

Shots: ch3_s1's clock_board() (rect centre (0, 0.9), source at left), dimmed except branches
B.SHORT and B.LONG -> a ruler under the long branch's bottom run, a pulse, GOLD "≈ 15 cm per ns"
-> s1's time axis: two arrival ticks -> the board becomes a square chip with an H-tree whose 16
ends light at slightly different moments -> a TEAL brace over the ticks, "clock skew"
-> clear: ch3_s3's split_path() at centre, built up (source at right, CLK0 long, CLK1 short and
dimmer) -> a pulse reaches FF1 first; the path shrinks to the top, two small data-sheet traces
below (CLK1 earlier), TEAL t_skew dim arrow -> a ghost source swings left, CLK1 slides later, back
-> tag "first: CLK1 ahead (slides pp. 107–109)" -> traces go, split_path() back to full size at
centre (as s3 opens on it) in one move while the traces fade, held 1 s, faded.
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
# clock_board(), copied from ch3_s1_hook.py
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
# Data-sheet kit, copied from ch3_s3_skewsetup.py (ch1_s5_datasheet.py + grow_dim)
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
    """Draw each leaf up to a vertical front moving from x0 to x1 (by x, not by curve count, so a
    wave whose edges sit further left shows them earlier)."""
    leaves = group.family_members_with_points()
    origs = [m.copy() for m in leaves]

    def upto(orig, X):
        pts = orig.points
        n = len(pts) // 4
        xs = [pts[4 * i][0] for i in range(n)] + [pts[-1][0]]
        if X <= xs[0]:
            return 0.0
        if X >= xs[-1]:
            return 1.0
        for i in range(n):
            if xs[i] <= X < xs[i + 1] or i == n - 1:
                w = xs[i + 1] - xs[i]
                t = 1.0 if w < 1e-6 else min(1.0, max(0.0, (X - xs[i]) / w))
                return (i + t) / n
        return 1.0

    def upd(_, a):
        X = x0 + a * (x1 - x0)
        for leaf, orig in zip(leaves, origs):
            lx0 = orig.get_left()[0]
            frac = 1.0 if a >= 1 else upto(orig, X)
            leaf.pointwise_become_partial(orig, 0, frac)
            leaf.set_stroke(opacity=orig.get_stroke_opacity() if X - lx0 > 0.15 or frac >= 1 else 0)

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
# This scene's own pieces
# =============================================================================================
RULER_Y = -1.95                     # ruler under the long branch's bottom run (y -1.25)
CH_C, CH_S = _p(0, 1.1), 4.4        # the chip: square, centre, side
H1, H2 = 1.1, 0.55                  # H-tree arm lengths (level 1, level 2)
PS = 0.65                           # the split path's scale while the traces are up
PS_C = _p(0, 1.8)                   # ... and its centre
TW_X0, TW_X1 = -4.6, 2.4            # small traces' extent
TY0, TY1, TY_SK = -0.7, -1.85, -2.55  # CLK0 row, CLK1 row, t_skew arrow row
TL_X = -5.6                         # row labels
CE = [-2.6, -0.6, 1.4]              # CLK0's edges (rise, fall, rise)
SK = 0.7                            # the skew


def ruler(x0=-5.0, x1=5.0, y=RULER_Y):
    g = VGroup(Line(_p(x0, y), _p(x1, y)).set_stroke(DIM, 2))
    n = int(round((x1 - x0) / 0.5))
    for k in range(n + 1):
        x = x0 + k * 0.5
        h = 0.2 if k % 5 == 0 else 0.1
        g.add(Line(_p(x, y), _p(x, y - h)).set_stroke(DIM, 2))
    return g


# An uneven clock tree: the clock enters at the bottom-left; some ends sit right by the entry,
# others far along the wire.  name: (parent, (x, y)) in absolute coordinates; leaves start with L.
TREE = {
    "R": (None, (-1.5, -1.1)),
    "A": ("R", (-1.5, -0.3)), "L1": ("A", (-1.95, -0.3)),
    "B": ("A", (-1.5, 0.9)), "L2": ("B", (-1.95, 0.9)),
    "I": ("B", (-0.3, 0.9)), "L10": ("I", (-0.3, 1.7)),
    "C": ("B", (-1.5, 2.5)), "L3": ("C", (-1.95, 2.5)),
    "D": ("C", (0.3, 2.5)), "L4": ("D", (0.3, 2.95)), "L11": ("D", (0.3, 1.9)),
    "E": ("D", (1.8, 2.5)), "L5": ("E", (1.8, 2.95)), "L6": ("E", (1.8, 1.6)),
    "F": ("A", (0.0, -0.3)), "L7": ("F", (0.0, 0.3)),
    "G": ("F", (1.8, -0.3)), "L8": ("G", (1.8, -0.75)),
    "H": ("G", (1.8, 0.6)), "L9": ("H", (0.6, 0.6)),
}


def chip():
    """Square chip with pins and an uneven clock tree from a bottom-left entry (TREE)."""
    c = CH_C
    g = VGroup()
    g.body = Square(side_length=CH_S).move_to(c).set_stroke(DIM, 2).set_fill("#181B22", 1)
    pins = VGroup()
    hs = CH_S / 2
    for k in range(9):
        o = -hs + 0.4 + k * (CH_S - 0.8) / 8
        for a, b in ((_p(o, hs), _p(o, hs + 0.16)), (_p(o, -hs), _p(o, -hs - 0.16)),
                     (_p(hs, o), _p(hs + 0.16, o)), (_p(-hs, o), _p(-hs - 0.16, o))):
            pins.add(Line(c + a, c + b).set_stroke(DIM, 3))
    g.pins = pins

    def pt(n):
        return _p(*TREE[n][1])

    def chain(n):
        out = []
        while n is not None:
            out.append(pt(n))
            n = TREE[n][0]
        return out[::-1]

    segs = VGroup(*[Line(pt(par), pt(n)) for n, (par, _) in TREE.items() if par is not None])
    segs.set_stroke(YELLOW, 3)
    g.tree = segs
    g.paths, g.leaves, g.lengths = [], [], []
    for n in TREE:
        if n.startswith("L"):
            pts = chain(n)
            g.paths.append(VMobject().set_points_as_corners(pts))
            g.lengths.append(sum(np.linalg.norm(pts[k + 1] - pts[k]) for k in range(len(pts) - 1)))
            g.leaves.append(Square(side_length=0.24).move_to(pt(n)).set_stroke(FG, 2).set_fill(BG, 1))
    g.add(g.pins, g.body, g.tree, *g.leaves)
    return g


def small_traces(k_shift=-SK):
    """CLK0 and CLK1 (edges shifted by k_shift), ch1_s5 style, plus the t_skew guides and arrow."""
    D = type("Small", (), {})()
    D.lab0 = T("CLK0", 34, YELLOW).move_to(_p(TL_X, TY0))
    D.lab1 = T("CLK1", 34, YELLOW).move_to(_p(TL_X, TY1)).set_opacity(0.7)
    D.clk0 = clock_wave(TW_X0, TW_X1, TY0, CE)
    D.clk1 = clk1_wave(k_shift)
    D.g_e = guide(CE[0], TY0 + ROW_H / 2, TY_SK - 0.15)
    D.g_k = k_guide(k_shift)
    D.sk = dim_arrow(CE[0] + k_shift, CE[0], TY_SK, TEAL, "t_{skew}", label_dir=DOWN, size=40)
    return D


def clk1_wave(k_shift):
    return clock_wave(TW_X0, TW_X1, TY1, [e + k_shift for e in CE]).set_stroke(opacity=CLK1_OP)


def k_guide(k_shift):
    return guide(CE[0] + k_shift, TY1 - ROW_H / 2, TY_SK - 0.15)


def pulse(scene, paths, v, tws=None, extra=(), at=None):
    """One pulse down each path at speed v; `at[i](arrival)` -> extra anims for path i."""
    anims = list(extra)
    end = 0.0
    for i, p in enumerate(paths):
        L = p.get_arc_length()
        arr = L / v
        tw = min(0.5, 1.4 / L) if tws is None else tws
        anims.append(time_span(VShowPassingFlash(p, time_width=tw, rate_func=linear), 0.0, arr * (1 + tw)))
        end = max(end, arr * (1 + tw))
        if at is not None:
            for a, t1 in at(i, arr):
                anims.append(a)
                end = max(end, t1)
    scene.play(*anims, run_time=end)


class ClockSkewWhat(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.ending()

    # -- c3.skew.1: wires have delay; skew on a board and on a chip -------------------------------
    def clip1(self):
        B = clock_board()
        S_, L_ = B.SHORT, B.LONG
        keep = (S_, L_)
        for i in range(len(B.boxes)):
            if i not in keep:
                B.branches[i].set_stroke(opacity=DIMMED)
                B.boxes[i].rect.set_stroke(opacity=DIMMED)
                B.boxes[i].tri.set_stroke(opacity=DIMMED)
        # bright branches drawn over the dimmed ones on shared segments
        B.tree.submobjects = [b for i, b in enumerate(B.branches) if i not in keep] + \
                             [B.branches[S_], B.branches[L_]]
        self.B = B
        R = ruler()
        speed = T("≈ 15 cm per ns", 38, GOLD).move_to(_p(4.25, 2.75))
        ticks = [B.tick(S_), B.tick(L_)]
        with self.say("c3.skew.1", gap=1.0) as c:
            # {wire}
            self.play(FadeIn(B), run_time=1.2)
            c.wait_until("delay")
            self.play(*flash([B.boxes[S_].rect, B.boxes[L_].rect]), run_time=1.2)
            # {cm}: a ruler along the long branch, a pulse along it, the speed
            c.wait_until("cm")
            self.play(*appear(R, shift=None), run_time=1.0)
            c.wait_until("travels")
            self.play(VShowPassingFlash(B.branches[L_].copy().set_stroke(YELLOW, 10, opacity=1),
                                        time_width=0.25, rate_func=linear), run_time=2.4)
            c.wait_until("fifteen")
            self.play(*appear(speed), run_time=1.0)
            # {lengths}: the time axis, then both pulses leave together
            c.wait_until("lengths")
            self.play(*appear(B.axis, B.axis_t, B.tick0, shift=None), run_time=1.0)
            self.wait(0.3)
            Ls = (B.lengths[S_], B.lengths[L_])
            v = Ls[1] / 3.0

            def at(i, arr):
                box = B.boxes[keep[i]].rect
                return [(time_span(FlashAround(box, color=YELLOW, buff=0.06), arr, arr + 0.6), arr + 0.6),
                        (time_span(box.animate.set_stroke(YELLOW), arr, arr + 0.3), arr + 0.3),
                        (time_span(FadeIn(ticks[i]), arr, arr + 0.3), arr + 0.3)]
            pulse(self, [B.branches[k].copy().set_stroke(YELLOW, 10, opacity=1) for k in keep], v, at=at)
            # {chip}: the board becomes a chip; its clock tree's ends light up one after another
            C = chip()
            self.C = C
            c.wait_until("chip")
            others = [B.tree, *B.boxes, B.src, B.src_l, R, speed]
            self.play(*during([FadeOut(m) for m in others], 0, 0.45),
                      *during([ReplacementTransform(B.rect, C.body)], 0.25, 0.85),
                      *during([FadeIn(C.pins), Create(C.tree), *[FadeIn(lf) for lf in C.leaves]], 0.6, 1.0),
                      run_time=2.0)
            c.wait_until("spread")
            # one speed for every wire: the ends light in order of wire length
            total = max(2.0, min(3.4, c.until("name") - 0.15))
            vv = max(C.lengths) / (total - 0.3)
            anims, end = [], 0.0
            for p, lf, Lp in zip(C.paths, C.leaves, C.lengths):
                arr = Lp / vv
                tw = min(0.5, 0.9 / Lp)
                anims.append(time_span(VShowPassingFlash(p.copy().set_stroke(YELLOW, 8), time_width=tw,
                                                         rate_func=linear), 0, arr * (1 + tw)))
                anims.append(time_span(lf.animate.set_fill(YELLOW, 1).set_stroke(YELLOW), arr, arr + 0.25))
                end = max(end, arr * (1 + tw), arr + 0.25)
            self.play(*anims, run_time=end)
            # {name}: a TEAL brace over the spread of ticks, "clock skew"
            c.wait_until("name")
            x0, x1 = ticks[0].get_center()[0], ticks[1].get_center()[0]
            top = ticks[0].get_top()[1]
            brace = span_brace(_p(x0, top), _p(x1, top), direction=UP, color=TEAL, buff=0.12, inset=0.0)
            name = T("clock skew", 40, TEAL).next_to(brace, UP, buff=0.12)
            self.play(GrowFromCenter(brace), *flash(ticks), run_time=1.2)
            c.wait_until("called")
            self.play(*appear(name), run_time=1.0)
        self.ticks, self.brace, self.name = ticks, brace, name

    # -- c3.skew.2: the path redrawn with two clock wires -----------------------------------------
    def clip2(self):
        P = split_path()
        P.clk_br1.set_stroke(opacity=1)
        P.clk1_l.set_opacity(1)
        self.P = P
        base = [m for m in P.all if m not in (P.clk_br0, P.clk_br1, P.src, P.clk0_l, P.clk1_l)]
        with self.say("c3.skew.2") as c:
            # {redraw}
            # "clock skew" stays as a small heading, top left, while the board clears
            head = self.name.copy().scale(0.8)
            head.to_corner(UL, buff=0.5)
            self.play(*during([self.name.animate.scale(0.8).move_to(head)], 0.35, 0.9),
                      *during([FadeOut(m) for m in self.mobjects if m is not self.name], 0.0, 0.45),
                      *during([FadeIn(m) for m in base], 0.5, 1.0), run_time=1.8)
            # {source}: the source at the right, the two branches
            c.wait_until("source")
            self.play(FadeIn(P.src, scale=0.6), Create(P.clk_br1), Create(P.clk_br0), run_time=1.8)
            c.wait_until("shorter")
            self.play(VShowPassingFlash(P.clk_paths()[1], time_width=0.5, rate_func=linear),
                      FlashAround(P.ff1.tri, color=YELLOW, buff=0.08), run_time=1.2)
            # {clk0}
            c.wait_until("clk0")
            self.play(*appear(P.clk0_l), VShowPassingFlash(P.clk_paths()[0], time_width=0.3, rate_func=linear),
                      run_time=1.4)
            # {clk1}: labelled, and drawn a little dimmer from here on
            c.wait_until("clk1")
            self.play(*appear(P.clk1_l), run_time=1.0)
            self.play(restyle(P.clk_br1, op=CLK1_OP), restyle(P.clk1_l, op=0.7), run_time=0.8)
            # {ahead}: one pulse leaves the source on both branches; FF1's triangle is reached first
            c.wait_until("ahead")
            paths = P.clk_paths()
            v = paths[0].get_arc_length() / 1.8

            def at(i, arr):
                tri = (P.ff0.tri, P.ff1.tri)[i]
                return [(time_span(FlashAround(tri, color=YELLOW, buff=0.08), arr, arr + 0.7), arr + 0.7)]
            pulse(self, paths, v, tws=0.25, at=at)
            # the path rises and shrinks; the two traces sweep in under it
            c.wait_until("its edges")
            # the lettering steps out (the traces carry the names), the shapes rise and shrink
            texts = [*P.names, P.cl_l, P.q0_l, P.d1_l, P.d0_l, P.q1_l, P.clk0_l, P.clk1_l]
            ff_texts = [(f, t) for f in (P.ff0, P.ff1) for t in (f.d_l, f.q_l, f.qb_l)]
            letters = texts + [t for _, t in ff_texts]
            self.letters = [t.copy() for t in letters]
            for f, t in ff_texts:
                f.remove(t)
            P.remove(*texts)
            settle(self, P)
            P.save_state()
            self.play(*during(disappear(*letters), 0, 0.4),
                      *during([P.animate.scale(PS).move_to(PS_C)], 0.3, 1.0), run_time=1.1)
            D = small_traces()
            self.D = D
            self.play(*appear(D.lab0, D.lab1, shift=None, lag=0.2),
                      sweep_in(D.clk0, TW_X0, TW_X1), sweep_in(D.clk1, TW_X0, TW_X1),
                      run_time=1.1, rate_func=linear)  # early: the two rows drawn together
            c.wait_until("amount")
            # the t_skew arrow arrives; the "clock skew" heading has done its job
            self.play(FadeIn(D.g_e), FadeIn(D.g_k), grow_dim(D.sk[0]),
                      *during(appear(D.sk[1], shift=None), 0.4, 1.0),
                      *during(disappear(self.name), 0.3, 1.0), run_time=min(1.2, c.until(floor=0.5)))

    # -- c3.skew.3: it could be the other way round ----------------------------------------------
    def clip3(self):
        P, D = self.P, self.D
        ghost = P.src.copy().set_stroke(opacity=0.4)
        cx = P.get_center()[0]
        g_to = _p(2 * cx - P.src.get_center()[0], P.src.get_center()[1])
        new1 = clk1_wave(SK)
        new_k = k_guide(SK)
        new_sk = dim_arrow(CE[0], CE[0] + SK, TY_SK, TEAL, "t_{skew}", label_dir=DOWN, size=40)
        tag = VGroup(T("first: CLK1 ahead", 30, FG), T("(slides pp. 107–109)", 30, DIM)).arrange(DOWN, buff=0.15)
        tag.move_to(_p(4.75, (TY0 + TY1) / 2))
        with self.say("c3.skew.3") as c:
            # {other}: "That's the case on the lecture's slides": hold, then the swap of order
            c.wait_until("other way round")
            self.play(FadeIn(ghost), run_time=0.5)
            self.play(MoveAlongPath(ghost, ArcBetweenPoints(ghost.get_center(), g_to, angle=-PI / 3)),
                      Transform(D.clk1, new1), Transform(D.g_k, new_k),
                      Transform(D.sk[0], new_sk[0]), D.sk[1].animate.move_to(new_sk[1]),
                      run_time=2.0)
            # {later}: back to CLK1 ahead; the tag
            c.wait_until("later")
            old = small_traces()
            self.play(FadeOut(ghost), Transform(D.clk1, old.clk1), Transform(D.g_k, old.g_k),
                      Transform(D.sk[0], old.sk[0]), D.sk[1].animate.move_to(old.sk[1]), run_time=1.2)
            c.wait_until(own_word=tag[0])
            self.play(*appear(tag[0], tag[1], lag=0.3), run_time=1.0)  # early: the source note belongs to the line
        self.tag = tag

    # -- end on split_path() alone, full size at centre (ch3_s3 opens on it) -----------------------
    def ending(self):
        P, D = self.P, self.D
        self.wait(0.6)
        # traces and tag fade out while the path grows back to full size, its lettering fading in
        c0 = P.saved_state.get_center()
        small = []
        for t in self.letters:
            s = t.copy().scale(PS, about_point=c0).shift(PS_C - c0)
            s.set_opacity(0)
            small.append(s)
        self.add(*small)
        self.play(*during(disappear(self.tag, D.lab0, D.lab1, D.clk0, D.clk1, D.g_e, D.g_k, D.sk), 0, 0.5),
                  *during([Restore(P), *[Transform(s, t) for s, t in zip(small, self.letters)]], 0.15, 1.0),
                  run_time=1.6)
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
