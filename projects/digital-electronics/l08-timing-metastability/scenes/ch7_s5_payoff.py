"""Chapter 7, scene 5: nearly double: the pipelined circuit's latency and throughput, why not exactly
double, a balanced split, and a third stage. Clips c7.payoff.1 – c7.payoff.5.

Circuit: ch7_s2's block (copied below) at s2's size and place, with s4's register at A and two stage
panels; tokens in ch6's task colours. Bars: ch1_s6's budget_bar at 0.85 units per ns, left edge x -4.6.
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


def poly(pts, color, width=5):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# =============================================================================================
# L6's make_ff (D flip-flop), copied from ch1_s4_path.py
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


def make_ff(center=ORIGIN, bubble=False, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    bub = None
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.1))
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.2)).set_stroke(YELLOW, 5)
    else:
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    if bub is not None:
        g.add(bub)
    g.box, g.tri, g.bub = box, tri, bub
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g
# =============================================================================================


# =============================================================================================
# THE ch7 circuit (p. 117), owned by ch7_s2; ch7_s1, s3, s4, s5 and the recap copy this block.
# Built in design units, then scaled to full width. C.xy(x, y) maps a design point to the screen
# (it follows C as long as C is moved as one group: C.o / C.u are two VectorizedPoints inside it).
# =============================================================================================
K = 0.55                    # flip-flop scale (box 0.825 x 1.43 in design units)
PIN_SIZE = 30               # D / Q / Q-bar letters inside a flip-flop (design size)
FW = BOX_W * K / 2          # half box width
FH = BOX_H * K / 2          # half box height
STUB = WIRE * K             # pin stub length
FF_DY = PIN_Y * K           # the D/Q pin row sits this far above the box centre
YM, YU, YL, YB = 0.75, 1.95, -0.45, -2.0      # main pin row, CB1 row, CB2 row, CLK bus
CB_W, CB_H, CB3_H = 1.1, 1.0, 1.2
IN_OFF = 0.25               # CB3's two inputs at YM +- IN_OFF
X_IN = -5.0                                   # input register (box centre)
X_F = X_IN + FW + STUB + 0.3                  # the fork
X_C12 = X_F + 0.3 + CB_W / 2                  # CB1 / CB2
X_U5 = X_C12 + CB_W / 2 + 0.25 + FW           # s5: register on CB1's output wire
X_L5 = X_U5 + 2 * FW + 0.15                   # s5: register on CB2's output wire (staggered)
X_J = X_L5 + FW + 0.25                        # the two wires drop / rise into CB3 here
X_3 = X_J + 0.3 + CB_W / 2                    # CB3
X_A = X_3 + CB_W / 2 + 0.3 + FW               # point A (s4's register)
X_4 = X_A + FW + 0.3 + CB_W / 2               # CB4
X_OUT = X_4 + CB_W / 2 + 0.25 + STUB + FW     # output register
DELAYS = (3.2, 2.5, 3, 5.5)                   # ns, CB1..CB4
TPD_SIZE = 38
CIRC_W, CIRC_Y = 13.3, 0.4                    # full-width span and centre height on screen
WIRE_OP, WIRE_W = 0.7, 4
WIRE_NS = 0.25                                # pulse travel time per design unit of wire


def _wire(pts):
    return poly(pts, FG, WIRE_W).set_stroke(opacity=WIRE_OP)


def tpd_tex(v, size=TPD_SIZE):
    return MathTex(r"t_{pd} = " + str(v) + r"\text{ ns}", font_size=size, color=PURPLE)


def ch7_ff(x, ypin, stubs=True):
    """make_ff at scale K with its D pin at (x, ypin), design units; its clock wire removed (the
    branch is a separate part). stubs=False: no pin stubs (it sits on an existing wire; the box is
    filled BG so the wire is hidden under it)."""
    f = make_ff()
    f.remove(f.clk_w)
    if not stubs:
        f.remove(f.d_w, f.q_w, f.qb_w)
    f.box.set_fill(BG, 1)
    f.scale(K, about_point=ORIGIN)
    for lab in (f.d_l, f.q_l, f.qb_l):
        lab.scale(PIN_SIZE / (36 * K))
    f.shift(_p(x, ypin - FF_DY))
    return f


def _branch(x, ypin):
    return Line(_p(x, YB), _p(x, ypin - FF_DY - FH)).set_stroke(YELLOW, 5)


def circuit():
    """Parts (each a separate mobject; C.parts lists them in drawing order):
    .ff_in .ff_out (ch7_ff; .box .tri .d_l .q_l .qb_l .d_w .q_w .qb_w)  .in_l .out_l ("Input"/"Output")
    .w_q (Q stub -> fork) .fork (dot) .w_up .w_dn (fork -> CB1 / CB2) .w_1 .w_2 (CB1 / CB2 -> CB3)
    .w_34 (CB3 -> CB4, where A is) .w_out (CB4 -> FF_out)  .cb [CB1..CB4] Rectangles  .names [T]
    .tpd [MathTex t_pd = ... ns]  .clk_bus .clk_dot .clk_l .br_in .br_out (bus -> each triangle)
    .tri_in .tri_out (the clock triangles)  .a_mark (VGroup: .stalk .ring .letter)
    .a_tag (DIM "the slide's point A", NOT in parts: s1 shows it)
    .r1 / .r2 (route-only parts: in-wire, block, out-wire)  .shared (Q stub, CB3, CB4 and their wires)
    C.s() current scale, C.xy(x, y) design -> screen point."""
    C = VGroup()
    C.ff_in = ch7_ff(X_IN, YM)
    C.ff_out = ch7_ff(X_OUT, YM)
    C.tri_in, C.tri_out = C.ff_in.tri, C.ff_out.tri
    C.in_l = T("Input", 32).next_to(_p(X_IN - FW - STUB, YM), LEFT, buff=0.12)
    C.out_l = T("Output", 32).next_to(_p(X_OUT + FW + STUB, YM), RIGHT, buff=0.12)
    C.cb, C.names = [], []
    for i, (x, y, h) in enumerate(((X_C12, YU, CB_H), (X_C12, YL, CB_H), (X_3, YM, CB3_H), (X_4, YM, CB_H))):
        b = Rectangle(width=CB_W, height=h).set_stroke(BLUE, 4).set_fill(opacity=0).move_to(_p(x, y))
        C.cb.append(b)
        C.names.append(T(f"CB{i + 1}", 32, BLUE).move_to(_p(x, y + h / 2 - 0.2)))
    C.tpd = [tpd_tex(d) for d in DELAYS]
    C.tpd[0].next_to(C.cb[0], UP, buff=0.2)
    C.tpd[1].next_to(C.cb[1], DOWN, buff=0.2)
    C.tpd[2].next_to(C.cb[2], UP, buff=0.2)
    if C.tpd[2].get_left()[0] < X_J + 0.15:
        C.tpd[2].shift(RIGHT * (X_J + 0.15 - C.tpd[2].get_left()[0]))
    C.tpd[3].next_to(C.cb[3], UP, buff=0.2)
    if C.tpd[3].get_left()[0] < C.tpd[2].get_right()[0] + 0.3:
        C.tpd[3].shift(RIGHT * (C.tpd[2].get_right()[0] + 0.3 - C.tpd[3].get_left()[0]))
    l12, r12 = X_C12 - CB_W / 2, X_C12 + CB_W / 2
    C.w_q = _wire([(X_IN + FW + STUB, YM), (X_F, YM)])
    C.fork = Dot(_p(X_F, YM), radius=0.07, color=FG)
    C.w_up = _wire([(X_F, YM), (X_F, YU), (l12, YU)])
    C.w_dn = _wire([(X_F, YM), (X_F, YL), (l12, YL)])
    C.w_1 = _wire([(r12, YU), (X_J, YU), (X_J, YM + IN_OFF), (X_3 - CB_W / 2, YM + IN_OFF)])
    C.w_2 = _wire([(r12, YL), (X_J, YL), (X_J, YM - IN_OFF), (X_3 - CB_W / 2, YM - IN_OFF)])
    C.w_34 = _wire([(X_3 + CB_W / 2, YM), (X_4 - CB_W / 2, YM)])
    C.w_out = _wire([(X_4 + CB_W / 2, YM), (X_OUT - FW - STUB, YM)])
    C.clk_bus = Line(_p(X_IN - FW - STUB, YB), _p(X_OUT, YB)).set_stroke(YELLOW, 5)
    C.clk_dot = Dot(_p(X_IN, YB), radius=0.08, color=YELLOW)
    C.clk_l = T("CLK", 32, YELLOW).next_to(_p(X_IN - FW - STUB, YB), LEFT, buff=0.12)
    C.br_in, C.br_out = _branch(X_IN, YM), _branch(X_OUT, YM)
    ring = Circle(radius=0.22).set_stroke(FG, 3).move_to(_p(X_A, YM - 0.84))
    letter = T("A", 30).move_to(ring)
    stalk = Arrow(_p(X_A, YM - 0.6), _p(X_A, YM - 0.06), buff=0, stroke_width=3, tip_length=0.14,
                  max_tip_length_to_length_ratio=0.4, color=FG)
    C.a_mark = VGroup(stalk, ring, letter)
    C.a_mark.stalk, C.a_mark.ring, C.a_mark.letter = stalk, ring, letter
    C.a_tag = T("the slide's point A", 30, DIM).next_to(ring, DOWN, buff=0.15)
    C.r1 = [C.w_up, C.cb[0], C.w_1]
    C.r2 = [C.w_dn, C.cb[1], C.w_2]
    C.shared = [C.w_q, C.cb[2], C.w_34, C.cb[3], C.w_out]
    C.parts = [C.w_q, C.w_up, C.w_dn, C.w_1, C.w_2, C.w_34, C.w_out, C.fork,
               C.clk_bus, C.clk_dot, C.br_in, C.br_out, C.clk_l,
               C.ff_in, C.ff_out, C.in_l, C.out_l, *C.cb, *C.names, *C.tpd, C.a_mark]
    C.o, C.u = VectorizedPoint(ORIGIN), VectorizedPoint(_p(1, 1))
    C.add(*C.parts, C.a_tag, C.o, C.u)
    s = CIRC_W / VGroup(*C.parts).width
    C.scale(s, about_point=ORIGIN)
    C.shift(_p(0, CIRC_Y) - VGroup(*C.parts).get_center())
    C.s = lambda: C.u.get_x() - C.o.get_x()
    C.xy = lambda x, y: C.o.get_center() + C.s() * _p(x, y)
    return C


def _fit(C, mob):
    """Place a mobject built in design units onto the circuit's current position and scale."""
    return mob.scale(C.s(), about_point=ORIGIN).shift(C.o.get_center())


def inserted_ff(C, x, ypin):
    """A register dropped onto an existing wire at design (x, ypin): VGroup(ff, branch, dot) with
    .ff (stubless ch7_ff, box filled BG) .branch (YELLOW, bus -> its triangle) .dot (bus junction)."""
    ff = ch7_ff(x, ypin, stubs=False)
    br = _branch(x, ypin)
    dot = Dot(_p(x, YB), radius=0.08, color=YELLOW)
    g = VGroup(br, dot, ff)
    g.ff, g.branch, g.dot = ff, br, dot
    return _fit(C, g)


def a_register(C):
    """s4: the D flip-flop at A, on the CB3 -> CB4 wire, with its CLK branch."""
    return inserted_ff(C, X_A, YM)


def s5_registers(C):
    """s5: [register on CB1's output wire, register on CB2's output wire] (staggered so the upper
    one's CLK branch passes left of the lower one; it crosses CB2's wire, no junction)."""
    return [inserted_ff(C, X_U5, YU), inserted_ff(C, X_L5, YL)]


def stage_panel(C, x0, x1, k, pad=0.15):
    """A soft background panel over screen x0..x1, from just under the CLK bus to just over the
    circuit's top label; "stage k" (T 30 DIM) inside at its bottom. VGroup(rect, label), .rect .label;
    z -5 (behind everything)."""
    y0 = C.clk_bus.get_y() - 0.62
    y1 = max(t.get_top()[1] for t in C.tpd) + pad
    rect = RoundedRectangle(corner_radius=0.18, width=x1 - x0, height=y1 - y0)
    rect.set_stroke(width=0).set_fill(FG, 0.07).move_to(_p((x0 + x1) / 2, (y0 + y1) / 2)).set_z_index(-5)
    lab = T(f"stage {k}", 30, DIM).move_to(_p((x0 + x1) / 2, y0 + 0.24))
    g = VGroup(rect, lab)
    g.rect, g.label = rect, lab
    return g


def _verts(w):
    return list(w.get_start_anchors()) + [w.get_end()]


def route_keys(C, r):
    """Keyframes [(t_ns, point)] for a pulse on route r (1: via CB1, 2: via CB2) from FF_in's Q to
    FF_out's D: blocks take their t_pd, wires WIRE_NS per design unit. Also returns the times it
    reaches its block (CB1/CB2) and CB3: keys, (t_block, t_cb3)."""
    s = C.s()
    pts, ns = [], []

    def go(seq, delay=None):
        for a, b in zip(seq, seq[1:]):
            pts.append((a, b))
            ns.append(delay if delay is not None else np.linalg.norm(b - a) / s * WIRE_NS)

    blk = C.cb[r - 1]
    w_in, w_mid = (C.w_up, C.w_1) if r == 1 else (C.w_dn, C.w_2)
    go([C.ff_in.q_w.get_start(), C.ff_in.q_w.get_end(), C.fork.get_center()])
    go(_verts(w_in))
    i_blk = len(pts)
    go([blk.get_left(), blk.get_right()], DELAYS[r - 1])
    go(_verts(w_mid))
    i_cb3 = len(pts)
    cb3 = C.cb[2]
    a, k, b = _verts(w_mid)[-1], _p(cb3.get_left()[0] + 0.2 * s, cb3.get_y()), cb3.get_right()
    la, lb = np.linalg.norm(k - a), np.linalg.norm(b - k)
    pts += [(a, k), (k, b)]
    ns += [DELAYS[2] * la / (la + lb), DELAYS[2] * lb / (la + lb)]
    go(_verts(C.w_34))
    go([C.cb[3].get_left(), C.cb[3].get_right()], DELAYS[3])
    go(_verts(C.w_out) + [C.ff_out.d_w.get_end()])
    keys, t = [(0.0, pts[0][0])], 0.0
    for (a, b), d in zip(pts, ns):
        t += d
        keys.append((t, b))
    return keys, (keys[i_blk][0], keys[i_cb3][0])


def pos_at(keys, t):
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, p0), (t1, p1) in zip(keys, keys[1:]):
        if t <= t1:
            return p0 + (p1 - p0) * ((t - t0) / (t1 - t0) if t1 > t0 else 1)
    return keys[-1][1]


def route_path(C, r, color=YELLOW, width=10):
    """A fresh path along route r (Q -> D), for VShowPassingFlash."""
    keys, _ = route_keys(C, r)
    return VMobject().set_points_as_corners([p for _, p in keys]).set_stroke(color, width)


def pulse(color=YELLOW):
    g = VGroup(Dot(radius=0.13, color=color).set_opacity(0.35), Dot(radius=0.075, color=color))
    return g.set_z_index(6)


def run_pulse(dot, keys, t0, t1, stop=None):
    """Move a pulse along keys from t0 to t1 ns (linear in time), holding at `stop` if given."""
    cap = keys[-1][0] if stop is None else stop
    return UpdateFromAlphaFunc(dot, lambda m, a: m.move_to(pos_at(keys, min(t0 + (t1 - t0) * a, cap))),
                               rate_func=linear)
# =============================================================================================


# =============================================================================================
# THE lecture's budget bar (owned by ch1_s6; copied verbatim)
# =============================================================================================
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
# =============================================================================================



# =============================================================================================
# ch7 bars (s3 / s4 / s5 / recap): budget_bar at 0.85 units per ns, left edge x -4.6
# =============================================================================================
UNIT = 0.85            # units per ns
BX0 = -4.6             # bars' left edge
TASK_COLORS = [BLUE, GREEN, TEAL, FG]


def ns_x(ns):
    return BX0 + ns * UNIT


def stage_bar(segs, y, total=None, outline=YELLOW):
    """segs = [(colour, ns, name or None)]. A budget_bar without its T_c label: .segs .outline,
    .names (T 28 inside the named segments), .divs (thin BG dividers between adjacent PURPLE
    segments). total (ns) = the outline's length (default: the sum)."""
    tot = sum(s[1] for s in segs) if total is None else total
    b = budget_bar([("x", col, ns * UNIT) for col, ns, _ in segs], tot * UNIT, x0=BX0, y=y, syms=False)
    b.remove(b.tc)
    if outline != YELLOW:
        b.outline.set_stroke(outline, 2)
    b.names, b.divs = [], []
    for (col, ns, name), r in zip(segs, b.segs):
        if name:
            b.names.append(T(name, 28).move_to(r))
    for (ca, _, _), (cb, _, _), r in zip(segs, segs[1:], b.segs):
        if ca == PURPLE and cb == PURPLE:
            b.divs.append(Line(r.get_corner(UR), r.get_corner(DR)).set_stroke(BG, 3).set_z_index(0.5))
    b.add(*b.divs, *b.names)
    return b


def side_label(name, total, y):
    """Left of a bar: name (T 30) over its total (GOLD T 30), right edge 0.3 left of the bars."""
    a = T(name, 30)
    t = T(total, 30, GOLD)
    VGroup(a, t).arrange(DOWN, buff=0.1).next_to(_p(BX0, y), LEFT, buff=0.3)
    return a, t


def idle_box(y, ns_from=5.8, ns=0.7):
    """s4's idle box: dashed DIM outline of ns after stage 2's bar, DIM "idle" right of it."""
    r = Rectangle(width=ns * UNIT, height=BAR_H).move_to(_p(ns_x(ns_from) + ns * UNIT / 2, y))
    box = DashedVMobject(r.set_stroke(DIM, 2), num_dashes=14)
    lab = T("idle", 28, DIM).next_to(box, RIGHT, buff=0.15)
    return box, lab
# =============================================================================================

ROW12, ROW_S1, ROW_S2 = 1.0, -0.3, -1.5      # clip 3/4 bar rows
CAP_Y, SUM_Y = -2.65, -3.4
ROWS3 = (1.9, 0.9, -0.1)                     # clip 5 bar rows
EQ_X = 0.9                                   # clip 5 equations' left edge


def term_eq(a, b, c_, total, size=36):
    eq = MathTex(a, "+", b, "+", c_, "= " + total + r"\text{ ns}", font_size=size)
    for i, col in ((0, PINK), (2, PURPLE), (4, GOLD)):
        eq[i].set_color(col)
    return eq


class PipelinePayoff(NarratedScene):
    def construct(self):
        self.build_circuit()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- circuit, register, panels, token routes ------------------------------------------------
    def build_circuit(self):
        C = self.C = circuit()
        self.circ_parts = [m for m in C.parts if m is not C.a_mark]
        self.regA = a_register(C)
        xin, xa, xo = C.ff_in.box.get_x(), self.regA.ff.box.get_x(), C.ff_out.box.get_x()
        self.panels2 = [stage_panel(C, xin, xa - 0.03, 1), stage_panel(C, xa + 0.03, xo, 2)]
        self.tris = [C.tri_in, self.regA.ff.tri, C.tri_out]
        k, _ = route_keys(C, 1)
        self.k = k
        y = C.xy(0, YM)[1]
        self.tD = self.t_at_x(self.regA.ff.box.get_left()[0], y)
        self.tQ = self.t_at_x(self.regA.ff.box.get_right()[0], y)

    def t_at_x(self, x, y):
        for (t0, p0), (t1, p1) in zip(self.k, self.k[1:]):
            if abs(p0[1] - y) < 1e-3 and abs(p1[1] - y) < 1e-3 and p0[0] <= x <= p1[0] and p1[0] > p0[0] \
                    and p0[0] > self.C.cb[2].get_right()[0] - 1e-3:
                return t0 + (t1 - t0) * (x - p0[0]) / (p1[0] - p0[0])
        raise ValueError("x not on the CB3 -> CB4 wire")

    def edge(self):
        return [time_span(FlashAround(t, color=YELLOW, buff=0.06, time_width=1.5), 0, 0.9) for t in self.tris]

    def token(self, col):
        d = pulse(col).move_to(pos_at(self.k, 0))
        self.add(d)
        return d

    def stage1(self, d):
        return time_span(run_pulse(d, self.k, 0, self.tD), 0.2, 2.0)

    def stage2(self, d):
        return time_span(run_pulse(d, self.k, self.tQ, self.k[-1][0]), 0.2, 2.0)

    def exit(self, d, col):
        a, b = self.C.ff_out.q_w.get_start(), self.C.ff_out.q_w.get_end()

        def f(m, t):
            m.move_to(a + (b - a) * min(1, t / 0.7))
            o = 1 - max(0, (t - 0.6) / 0.4)
            m[0].set_opacity(0.35 * o)
            m[1].set_opacity(o)
        return [time_span(UpdateFromAlphaFunc(d, f, rate_func=linear), 0.2, 1.4),
                time_span(FlashAround(self.C.out_l, color=col, time_width=1.5), 0.8, 2.0)]

    # ------------------------------------------------------------------ c7.payoff.1
    def clip1(self):
        C = self.C
        with self.say("c7.payoff.1") as c:
            self.play(*[FadeIn(m) for m in self.circ_parts], FadeIn(self.regA),  # early: s4's pipelined circuit returns (continuity)
                      *[FadeIn(p) for p in self.panels2], run_time=0.8)

            # {blue}: on an edge, BLUE leaves the input register and waits at the new one
            c.wait_until("blue")
            blue = self.token(BLUE)
            self.play(*self.edge(), self.stage1(blue), run_time=2.0)

            y_txt = self.panels2[0].rect.get_bottom()[1] - 0.42
            lat = T("latency = 2 × 6.5 = 13 ns", 32, GOLD).move_to(_p(0, y_txt)).to_edge(LEFT, buff=0.6)
            thr = T("throughput = 1/6.5 ns ≈ 153.85 MHz", 32, GOLD).move_to(_p(0, y_txt)).to_edge(RIGHT, buff=0.6)
            c.wait_until(own_word=lat)
            self.play(*appear(lat), run_time=1.0)

            # {green}: next edge: BLUE into stage 2, GREEN into stage 1 behind it
            c.wait_until("green")
            green = self.token(GREEN)
            self.play(*self.edge(), self.stage2(blue), self.stage1(green), run_time=2.0)

            # {throughput}: BLUE leaves, GREEN on, TEAL in
            c.wait_until("throughput")
            teal = self.token(TEAL)
            self.play(*self.edge(), *self.exit(blue, BLUE), self.stage2(green), self.stage1(teal), run_time=2.0)
            self.remove(blue)

            c.wait_until("That's a throughput")
            white = self.token(FG)
            self.play(*self.edge(), *self.exit(green, GREEN), self.stage2(teal), self.stage1(white),
                      *during(appear(thr), 0.25, 0.8), run_time=2.0)
            self.remove(green)
            self.lat, self.thr = lat, thr

    # ------------------------------------------------------------------ c7.payoff.2
    def clip2(self):
        LX, X1, X2 = -6.2, -0.4, 3.0
        RY = (1.55, 0.65, -0.25)
        hdr = [T("no pipeline", 36).move_to(_p(X1, 2.5)), T("two stages", 36).move_to(_p(X2, 2.5))]
        rule = Line(_p(LX, 2.08), _p(4.6, 2.08)).set_stroke(DIM, 2)
        rows = [T(s, 36).move_to(_p(0, y)).align_to(_p(LX, 0), LEFT)
                for s, y in zip(("clock period", "latency", "throughput"), RY)]
        vals = [[T(a, 40, GOLD).move_to(_p(X1, y)), T(b, 40, GOLD).move_to(_p(X2, y))]
                for (a, b), y in zip((("12 ns", "6.5 ns"), ("12 ns", "13 ns"), ("83.3 MHz", "153.85 MHz")), RY)]
        table = [*hdr, rule, *rows, *[v for r in vals for v in r]]
        quote = T("“It can be seen that the 2-stage pipeline has almost\n"
                  "doubled the throughput (clock frequency), with only\n"
                  "a small increase in latency.”", 32, line_spacing=0.9).move_to(_p(0, -1.95))
        plus = T("+ 1 ns", 30, DIM).next_to(vals[1][1], RIGHT, buff=0.3)
        times = T("× 1.85", 40, GREEN).next_to(vals[2][1], RIGHT, buff=0.3)
        with self.say("c7.payoff.2") as c:
            # {compare}: the circuit shrinks away; the table comes in
            old = Group(*self.mobjects)
            self.play(*during(FadeOut(old, scale=0.35), 0, 0.5), *during(appear(*table, shift=None, lag=0.05), 0.45, 1.0), run_time=1.8)  # early: the table is shown whole, then walked
            self.remove(*old.submobjects)
            c.wait_until("twelve nanoseconds")
            self.play(FlashAround(vals[1][0], color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("to thirteen")
            self.play(FlashAround(vals[1][1], color=GOLD, time_width=1.5), run_time=1.2)

            c.wait_until("As last time")
            self.play(*appear(quote, shift=None), run_time=1.0)  # early: the slide's line, read by the viewer
            c.wait_until("grows a little")
            self.play(*appear(plus), run_time=1.0)

            # {times}
            c.wait_until("times")
            self.play(*appear(times), FlashAround(vals[2][1], color=GREEN, time_width=1.5), run_time=1.4)
            c.wait_until("Almost double")
            self.play(FlashUnder(select(quote, "doubled the throughput")[0], color=GREEN, time_width=1.5),
                      run_time=1.4)
        self.table = [*table, plus, times, quote]

    # ------------------------------------------------------------------ c7.payoff.3
    def clip3(self):
        b12 = stage_bar([(PINK, 0.2, None), (PURPLE, 3.2, "CB1"), (PURPLE, 3, "CB3"), (PURPLE, 5.5, "CB4"),
                         (GOLD, 0.1, None)], ROW12)
        b1 = stage_bar([(PINK, 0.2, None), (PURPLE, 3.2, "CB1"), (PURPLE, 3, "CB3"), (GOLD, 0.1, None)], ROW_S1)
        b2 = stage_bar([(PINK, 0.2, None), (PURPLE, 5.5, "CB4"), (GOLD, 0.1, None)], ROW_S2)
        l12 = side_label("one stage", "12 ns", ROW12)
        l1 = side_label("stage 1", "6.5 ns", ROW_S1)
        l2 = side_label("stage 2", "5.8 ns", ROW_S2)
        idle, idle_l = idle_box(ROW_S2)
        self.b1, self.b2, self.l1, self.l2, self.idle = b1, b2, l1, l2, (idle, idle_l)
        note = T("“Note the throughput is not exactly doubled since the\n"
                 "pipeline stages are not equal and a penalty is also\n"
                 "incurred owing to the additional D-type FF.”", 30, line_spacing=0.9)
        note.to_edge(UP, buff=0.45)
        xh = ns_x(6)
        half = DashedLine(_p(xh, ROW12 + 0.45), _p(xh, ROW_S2 - 0.4), dash_length=0.12).set_stroke(YELLOW, 3)
        half_l = T("half of 12 ns", 30, YELLOW).next_to(half, UP, buff=0.12)
        self.half = (half, half_l)
        cap1 = T("stage 2 idles 0.7 ns every cycle", 34).move_to(_p(0, CAP_Y))
        cap2 = T("+ 0.3 ns: the extra register", 34).move_to(_p(0, CAP_Y))
        pink_l = T("0.2", 28, PINK).next_to(b2.segs[0], UP, buff=0.1)
        gold_l = T("0.1", 28, GOLD).next_to(b1.segs[-1], UP, buff=0.1)
        self.tags = (pink_l, gold_l)
        sm = MathTex(r"6.5 + 5.8 = 12.3 = 12 + 0.3", font_size=44, color=GOLD).move_to(_p(0, SUM_Y))
        with self.say("c7.payoff.3") as c:
            # {why}: the table shrinks; the 12 ns bar and the two stage bars return
            old = Group(*self.table)
            bars = [b12, *l12, b1, *l1, b2, *l2, idle, idle_l]
            self.play(*during(FadeOut(old, scale=0.5), 0, 0.45), *during(appear(*bars, shift=None, lag=0.06), 0.45, 1.0), run_time=1.6)  # early: s3's and s4's bars return whole
            self.remove(*old.submobjects)
            self.play(*appear(note, shift=None), run_time=1.0)  # early: the slide's line, read by the viewer

            # {half}
            c.wait_until("half")
            self.play(GrowFromEdge(half, UP), run_time=1.2)
            c.wait_until(own_word=half_l)
            self.play(*appear(half_l), run_time=1.0)

            # {unequal}: idle box
            c.wait_until("unequal")
            self.play(FlashAround(VGroup(*b1.segs), color=FG, time_width=1.5),
                      FlashAround(VGroup(*b2.segs), color=FG, time_width=1.5), run_time=1.4)
            c.wait_until("Stage two finishes")
            self.play(*appear(cap1), run_time=1.0)
            c.wait_until("idle")
            self.play(FlashAround(idle, color=YELLOW, time_width=1.5), idle_l.animate.set_color(YELLOW), run_time=1.5)

            # {overhead}: the new register's two segments
            c.wait_until("overhead")
            self.play(idle_l.animate.set_color(DIM), FlashAround(b2.segs[0], color=PINK, time_width=1.5),
                      *appear(pink_l), run_time=1.4)
            c.wait_until("time", nth=1)
            self.play(FlashAround(b1.segs[-1], color=GOLD, time_width=1.5), *appear(gold_l), run_time=1.4)
            c.wait_until("Together")
            self.play(*swap(cap1, cap2), run_time=1.2)  # early: the caption names the register just described

            # {sum}
            c.wait_until("sum")
            self.play(*appear(sm), run_time=1.2)
        self.cap, self.sum = cap2, sm
        self.b12, self.l12, self.note = b12, l12, note

    # ------------------------------------------------------------------ c7.payoff.4
    def clip4(self):
        b1, b2 = self.b1, self.b2
        h = 5.85 / 2
        t1 = stage_bar([(PINK, 0.2, None), (PURPLE, h, None), (PURPLE, h, None), (GOLD, 0.1, None)], ROW_S1)
        t2 = stage_bar([(PINK, 0.2, None), (PURPLE, 5.85, None), (GOLD, 0.1, None)], ROW_S2)
        n1 = T("6.15 ns", 30, GOLD).move_to(self.l1[1])
        n2 = T("6.15 ns", 30, GOLD).move_to(self.l2[1])
        eq = term_eq("0.2", "5.85", "0.1", "6.15", size=44).move_to(_p(0, SUM_Y))
        res = T("6.15 ns, 162.6 MHz", 36, GOLD).move_to(_p(0, (ROW_S1 + ROW_S2) / 2))
        res.align_to(_p(1.4, 0), LEFT)
        fast = T("≈ × 1.95", 40, GREEN).next_to(res, DOWN, buff=0.35).align_to(res, LEFT)
        cap = T("cut where the stages come out equal", 34).move_to(_p(0, CAP_Y))
        with self.say("c7.payoff.4") as c:
            # {balanced}: the two bars morph into equal bars, both still past the dashed 6 ns line
            morph = [Transform(a, b_) for a, b_ in zip(b1.segs, t1.segs)] + \
                [Transform(a, b_) for a, b_ in zip(b2.segs, t2.segs)] + \
                [Transform(b1.outline, t1.outline), Transform(b2.outline, t2.outline)]
            gone = [*b1.names, *b2.names, *b1.divs, *self.idle, *self.tags]
            self.play(*during(disappear(*gone), 0, 0.4), *during(morph, 0.25, 1.0), run_time=2.2)
            c.wait_until("six point one five")
            self.play(*swap(self.sum, eq), *swap(self.l1[1], n1), *swap(self.l2[1], n2), run_time=1.4)

            # {balance}
            c.wait_until("balance")
            self.play(*appear(res), *swap(self.cap, cap), run_time=1.2)  # early: the caption states the next sentence
            c.wait_until("one point nine five")
            self.play(*appear(fast), run_time=1.0)
        self.n12 = (n1, n2)

    # ------------------------------------------------------------------ c7.payoff.5
    def clip5(self):
        C = self.C
        r5 = s5_registers(C)
        xin, xa, xo = C.ff_in.box.get_x(), self.regA.ff.box.get_x(), C.ff_out.box.get_x()
        xm = (r5[0].ff.box.get_x() + r5[1].ff.box.get_x()) / 2
        panels3 = [stage_panel(C, xin, xm - 0.03, 1), stage_panel(C, xm + 0.03, xa - 0.03, 2),
                   stage_panel(C, xa + 0.03, xo, 3)]
        specs = (((PINK, 0.2, None), (PURPLE, 3.2, "CB1"), (GOLD, 0.1, None)),
                 ((PINK, 0.2, None), (PURPLE, 3, "CB3"), (GOLD, 0.1, None)),
                 ((PINK, 0.2, None), (PURPLE, 5.5, "CB4"), (GOLD, 0.1, None)))
        bars = [stage_bar(list(s), y, outline=DIM) for s, y in zip(specs, ROWS3)]
        labs = [T(f"stage {i + 1}", 30).next_to(_p(BX0, y), LEFT, buff=0.3) for i, y in enumerate(ROWS3)]
        eqs = [term_eq("0.2", a, "0.1", t).move_to(_p(0, y)).align_to(_p(EQ_X, 0), LEFT)
               for (a, t), y in zip((("3.2", "3.5"), ("3", "3.3"), ("5.5", "5.8")), ROWS3)]
        xm5 = ns_x(5.8)
        marker = Line(_p(xm5, ROWS3[0] + 0.45), _p(xm5, ROWS3[2] - 0.45)).set_stroke(YELLOW, 4)
        pace = T("CB4 sets the pace", 36, YELLOW).move_to(_p(-2.3, -1.25))
        res = T("5.8 ns, 172.4 MHz", 40, GOLD).move_to(_p(2.8, -1.25))
        lat = T("latency = 3 × 5.8 = 17.4 ns", 40, GOLD, t2c={"17.4": RED}).move_to(_p(0, -2.2))
        lesson = T("each new stage: + 0.3 ns, + 1 cycle of latency", 36).move_to(_p(0, -3.1))
        with self.say("c7.payoff.5") as c:
            # {three}: back to the circuit; each bar row (bar + its side labels) leaves as one object
            rows = [[self.b12, *self.l12], [self.b1, self.l1[0], self.n12[0]], [self.b2, self.l2[0], self.n12[1]]]
            for b in (self.b1, self.b2):        # their names/dividers left in c7.payoff.4: drop them for good
                b.remove(*b.names, *b.divs)
            for parts in rows:
                self.remove(*parts)
                self.add(VGroup(*parts))
            sweep_clear(self, *[FadeIn(m) for m in self.circ_parts], FadeIn(self.regA), run_time=1.6)
            c.wait_until("Put registers")
            self.play(*appear(*r5, shift=None, lag=0.3), run_time=1.2)
            self.play(*[FadeIn(p) for p in panels3], run_time=0.9)  # early: the three stages, named a moment later

            # three bars at the same scale, each on its number
            c.wait_until("of three point five")
            sweep_clear(self, *appear(bars[0], labs[0], eqs[0], shift=None, lag=0.1), run_time=1.3)
            c.wait_until("three point three")
            self.play(*appear(bars[1], labs[1], eqs[1], shift=None, lag=0.1), run_time=1.0)
            c.wait_until("and five point eight")
            self.play(*appear(bars[2], labs[2], eqs[2], shift=None, lag=0.1), run_time=1.0)

            # {pace}: the period marker lands at 5.8 ns; CB4's bar outlined YELLOW
            c.wait_until("pace")
            self.play(FadeIn(marker, shift=0.3 * DOWN), restyle(bars[2].outline, outline=YELLOW, width=5),
                      run_time=1.3)
            c.wait_until(own_word=pace)
            self.play(*appear(pace), run_time=1.0)
            c.wait_until("five point eight nanoseconds")
            self.play(*appear(res), run_time=1.0)

            # {longer}
            c.wait_until(own_word=lat)
            self.play(*appear(lat), run_time=1.0)
            c.wait_until("seventeen point four")
            self.play(FlashAround(select(lat, "17.4")[0], color=RED, time_width=1.5), run_time=1.2)

            # {lesson}
            c.wait_until("lesson")
            self.play(*appear(lesson), run_time=1.0)  # early: the lesson line sums up both sentences
        self.wait(0.8)
