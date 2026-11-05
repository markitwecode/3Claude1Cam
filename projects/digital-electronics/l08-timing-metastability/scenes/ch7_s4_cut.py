"""Chapter 7, scene 4: one register at A cuts the logic into two stages; the slowest stage decides.
Clips c7.cut.1 – c7.cut.5.

Opens on ch7_s2's circuit (its `# ===` blocks copied verbatim) at full size, with s3's GOLD corner
numbers. In clip 3 the circuit (with its stage panels) shrinks to the top (SHRINK, top SHRUNK_TOP,
centre x SHRUNK_X) and the two budget bars build underneath at NS units per ns from BAR_X0.
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

CRIT_W = 8                 # critical-path stroke width (ch7_s2)
OFF = 0.3                  # off-critical-path opacity (ch7_s2)

# ---- this scene's layout (s5 and the recap copy it) ------------------------------------------
SHRINK, SHRUNK_TOP, SHRUNK_X = 0.66, 3.55, 0.6    # circuit + panels after clip 3's shrink
NS = 0.85                  # bar units per ns (chapter scale, s3 / s5)
BAR_X0 = -4.6              # bars' left edge
BAR1_Y, BAR2_Y = -1.05, -2.2
ARROW_Y = -0.35            # the T_c arrow over the bars
EQ_X = 1.8                 # left edge of each bar's sum
BOTTOM_Y = -3.35           # question / "the slowest stage decides"


def corner_numbers():
    """s3's corner: GOLD T 30 "12 ns" over "83.3 MHz", left x -6.6, top y 3.5."""
    g = VGroup(T("12 ns", 30, GOLD), T("83.3 MHz", 30, GOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    return g.align_to(_p(-6.6, 0), LEFT).align_to(_p(0, 3.5), UP)


def bar_segs(lengths_ns, colors, y):
    """budget_bar's segments only (no outline / T_c: the shared period marker plays that part)."""
    b = budget_bar([("", col, n * NS) for n, col in zip(lengths_ns, colors)], 1.0, x0=BAR_X0, y=y, syms=False)
    return b.segs


def bar_sum(terms, colors, total, y):
    eq = MathTex("T_c =", *[x for t in terms for x in ("+", t)][1:], "=", total + r"\text{ ns}", font_size=32)
    k = 1
    for col in colors:
        eq[k].set_color(col)
        k += 2
    eq[-1].set_color(GOLD)
    return eq.align_to(_p(EQ_X, 0), LEFT).set_y(y)


def t_at_x(keys, x, y):
    """Time (ns) at which a pulse on keys crosses screen x on the horizontal run at height y."""
    for (t0, p0), (t1, p1) in zip(keys, keys[1:]):
        if abs(p0[1] - y) < 1e-3 and abs(p1[1] - y) < 1e-3 and p0[0] <= x <= p1[0] and p1[0] > p0[0]:
            return t0 + (t1 - t0) * (x - p0[0]) / (p1[0] - p0[0])
    raise ValueError("x not on route")


def ns_x(ns):
    return BAR_X0 + ns * NS


def period_marker(ns):
    x = ns_x(ns)
    line = Line(_p(x, BAR1_Y + 0.45), _p(x, BAR2_Y - 0.45)).set_stroke(YELLOW, 4)
    return line


def tc_arrow(ns):
    return DoubleArrow(_p(BAR_X0, ARROW_Y), _p(ns_x(ns), ARROW_Y), buff=0, stroke_width=3, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.4, color=YELLOW)


class OneRegister(NarratedScene):
    def construct(self):
        self.C = circuit()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def edge(self, rt=1.2):
        """A rising edge on all three clock triangles at once (plus a flash along the bus)."""
        C, R = self.C, self.R
        bus = C.clk_bus.copy().set_stroke(YELLOW, 10)
        return [VShowPassingFlash(bus, time_width=0.8, run_time=rt * 0.6)] + \
            [time_span(FlashAround(t, color=YELLOW, buff=0.08, time_width=1.5), 0.3 * rt, rt)
             for t in (C.tri_in, R.ff.tri, C.tri_out)]

    # ------------------------------------------------------------------ c7.cut.1
    def clip1(self):
        C = self.C
        R = self.R = a_register(C)
        self.corner = corner = corner_numbers()
        with self.say("c7.cut.1") as c:
            self.play(*[FadeIn(m) for m in C.parts], FadeIn(corner), run_time=0.8)  # early: s2's circuit and s3's corner return (continuity)

            # {insert}: the register drops onto the CB3 -> CB4 wire; the A marker fades as it lands
            c.wait_until("one more register")
            self.play(*during([FadeOut(C.a_mark)], 0, 0.45),
                      *during([FadeIn(R.ff, shift=0.4 * DOWN)], 0.35, 1.0), run_time=1.6)
            C.remove(C.a_mark)
            c.wait_until("single")
            self.play(FlashAround(R.ff.box, color=YELLOW, time_width=1.5), run_time=1.4)

            # {wire}: CLK grows a branch up to its triangle; an edge on all three at once
            c.wait_until("wire")
            self.play(FadeIn(R.dot, scale=0.5), GrowFromPoint(R.branch, R.branch.get_start()), run_time=1.2)
            c.wait_until("same moment")
            self.play(*self.edge(1.4), run_time=1.4)

            # {stages}: two soft panels, abutting at the new register's centre
            xa = R.ff.box.get_x()
            self.p1 = stage_panel(C, C.ff_in.box.get_left()[0] - 0.2, xa - 0.04, 1)
            self.p2 = stage_panel(C, xa + 0.04, C.ff_out.box.get_right()[0] + 0.2, 2)
            c.wait_until("stages")
            self.play(FadeIn(self.p1.rect), FadeIn(self.p2.rect), *appear(  # early: the panels' names come with "two stages"
                      self.p1.label, self.p2.label, lag=0.3),
                      run_time=1.4)

            # register, logic, register (walked on stage 1)
            c.wait_until("a register")
            self.play(FlashAround(C.ff_in.box, color=FG, time_width=1.5), run_time=min(1.0, c.until("then logic")))
            c.wait_until("then logic")
            self.play(*[FlashAround(C.cb[i], color=BLUE, time_width=1.5) for i in range(3)],
                      run_time=min(1.0, c.until("then a register")))
            c.wait_until("then a register")
            self.play(FlashAround(R.ff.box, color=FG, time_width=1.5), run_time=min(1.0, c.until()))

    # ------------------------------------------------------------------ c7.cut.2
    def clip2(self):
        C, R = self.C, self.R
        keys, _ = route_keys(C, 1)
        ym = C.ff_in.q_w.get_y()
        d_pt = _p(R.ff.box.get_left()[0], ym)
        q_pt = _p(R.ff.box.get_right()[0], ym)
        t_d = t_at_x(keys, d_pt[0], ym)
        with self.say("c7.cut.2") as c:
            # {hold}: task 1's BLUE dot runs CB1, CB3 and waits at the new register's D
            blue = pulse(BLUE).move_to(keys[0][1])
            self.add(blue)
            self.play(*self.edge(1.0), run_pulse(blue, keys, 0, t_d, stop=t_d),
                      run_time=max(1.5, c.until("catches") - 0.2))
            c.wait_until("catches")
            blue_q = pulse(BLUE).move_to(q_pt)
            green = pulse(GREEN).move_to(keys[0][1])
            self.play(*self.edge(1.2), *during([FadeOut(blue)], 0.2, 0.5),
                      *during([FadeIn(blue_q), FadeIn(green)], 0.5, 1.0), run_time=1.2)
            c.wait_until("holds it steady")
            work = VMobject().set_points_as_corners(
                [q_pt, C.cb[3].get_left(), C.cb[3].get_right(), C.ff_out.d_w.get_end()]).set_stroke(BLUE, 10)
            self.play(VShowPassingFlash(work, time_width=0.6), run_time=min(3.0, c.until("meanwhile") - 0.2))

            # {meanwhile}: the GREEN value, launched on that same edge, works its way through stage 1
            c.wait_until("meanwhile")
            self.play(run_pulse(green, keys, 0, t_d, stop=t_d), run_time=min(3.0, c.until("never catch") - 0.2))
            c.wait_until("never catch")
            self.play(FlashAround(R.ff.box, color=YELLOW, time_width=1.5), run_time=1.5)
            self.dots = (blue_q, green)

    # ------------------------------------------------------------------ c7.cut.3
    def clip3(self):
        C, R = self.C, self.R
        with self.say("c7.cut.3") as c:
            # the circuit (with its panels) moves up and shrinks to make room for the bars
            # (too small once shrunk: pin letters, t_pd labels, Input/Output/CLK fade; CB names stay at 28)
            gone = [C.in_l, C.out_l, C.clk_l, *C.tpd]
            pins = [lab for ff in (C.ff_in, C.ff_out, R.ff) for lab in (ff.d_l, ff.q_l, ff.qb_l)]
            movers = [m for m in C.parts if m is not C.a_mark and m not in gone]
            movers += [R, self.p1.rect, self.p2.rect]
            box = VGroup(*movers)
            P = box.get_center()
            new_top = P[1] + SHRINK * (box.get_top()[1] - P[1])
            v = _p(SHRUNK_X - P[0], SHRUNK_TOP - new_top)
            grow = 28 / (32 * C.s() * SHRINK)
            anims = []
            for m in movers:
                if m in C.names:      # names (kept at 28) sit just outside their block, where t_pd was
                    i = C.names.index(m)
                    blk, d = C.cb[i], (DOWN if i == 1 else UP)
                    off = (SHRINK * blk.height + SHRINK * grow * m.height) / 2 + 0.1
                    a = m.animate.scale(SHRINK * grow).move_to(P + SHRINK * (blk.get_center() - P) + v + d * off)
                else:
                    a = m.animate.scale(SHRINK, about_point=P).shift(v)
                anims.append(a)
            # the faded labels ride with the circuit as it shrinks, fading on the way
            anims += [m.animate.scale(SHRINK, about_point=P).shift(v).set_opacity(0) for m in gone]
            self.play(*disappear(*self.dots, self.p1.label, self.p2.label),
                      *[restyle(lab, op=0) for lab in pins],
                      *during(anims, 0.25, 1.0), run_time=1.8)
            self.remove(*gone)
            for ff in (C.ff_in, C.ff_out, R.ff):
                for lab in (ff.d_l, ff.q_l, ff.qb_l):
                    ff.remove(lab)
                    self.remove(lab)
            for m in (C.o, C.u):
                m.scale(SHRINK, about_point=P).shift(v)
            for m in (self.p1, self.p2):
                m.remove(m.label)

            # {s1path}: CB1 and CB3 critical, CB2 dimmed
            c.wait_until("block one")
            self.play(*[restyle(w, op=1, width=CRIT_W) for w in (C.w_q, C.w_up, C.w_1)],
                      *[restyle(C.cb[i], outline=BLUE, width=CRIT_W) for i in (0, 2)],
                      *set_alpha([C.w_dn, C.w_2, C.cb[1], C.names[1]], OFF), run_time=1.5)

            # {s1bar}: stage 1's bar, each segment from its source
            ns1 = (0.2, 3.2, 5.8 - 3.4, 6.2 - 5.8, 0.1)       # CB3's 3 ns split at the 5.8 ns mark (clip 5)
            self.bar1 = segs = bar_segs(ns1, (PINK, PURPLE, PURPLE, PURPLE, GOLD), BAR1_Y)
            self.eq1 = eq = bar_sum(["0.2", "3.2", "3", "0.1"], (PINK, PURPLE, PURPLE, GOLD), "6.5", BAR1_Y)
            self.lab1 = lab = T("stage 1", 30, DIM).next_to(_p(BAR_X0, BAR1_Y), LEFT, buff=0.3)
            nm1 = T("CB1", 28, FG).move_to(segs[1])
            nm3 = T("CB3", 28, FG).move_to(VGroup(segs[2], segs[3]))
            dv13 = Line(segs[2].get_corner(UL), segs[2].get_corner(DL)).set_stroke(BG, 3).set_z_index(0.5)
            c.wait_until("zero point two")
            self.play(*appear(lab, shift=None), ReplacementTransform(C.ff_in.box.copy(), segs[0]),
                      *appear(eq[0], eq[1], lag=0.2), run_time=1.2)
            c.wait_until("three point two")
            self.play(ReplacementTransform(C.cb[0].copy(), segs[1]), *during(appear(nm1, shift=None), 0.6, 1.0),
                      *appear(eq[2], eq[3], lag=0.2), run_time=1.2)
            c.wait_until("plus three", nth=1)
            self.play(ReplacementTransform(C.cb[2].copy(), segs[2]), ReplacementTransform(C.cb[2].copy(), segs[3]),
                      time_span(FadeIn(dv13), 0.9, 1.2), *during(appear(nm3, shift=None), 0.6, 1.0),
                      *appear(eq[4], eq[5], lag=0.2), run_time=1.2)
            c.wait_until("zero point one")
            # the new register rings GOLD on "zero point one", and its GOLD copy drops into the bar
            src = R.ff.box.copy().set_stroke(GOLD, CRIT_W).set_fill(GOLD, 0.5)
            rf_stroke = (R.ff.box.get_stroke_color(), R.ff.box.get_stroke_width())
            self.play(*during([R.ff.box.animate.set_stroke(GOLD, CRIT_W), FadeIn(src)], 0, 0.2),
                      *during([ReplacementTransform(src, segs[4])], 0.4, 1.0),
                      *during(appear(eq[6], eq[7], lag=0.2), 0.5, 1.0), run_time=1.8)
            c.wait_until("six point five")
            self.play(*appear(eq[8], eq[9], lag=0.2),
                      R.ff.box.animate.set_stroke(rf_stroke[0], rf_stroke[1]), run_time=1.0)
            settle(self, eq)

            # {cb2}: CB2's route flickers; DIM 2.5 < 3.2 beside it
            c.wait_until("cb2")
            self.cmp = cmp = MathTex("2.5 < 3.2", font_size=36, color=DIM)
            cmp.align_to(_p(-6.6, 0), LEFT).set_y(C.cb[1].get_y())
            self.play(VShowPassingFlash(route_path(C, 2, color=FG, width=8), time_width=0.5),
                      *appear(cmp, shift=None), run_time=1.6)

    # ------------------------------------------------------------------ c7.cut.4
    def clip4(self):
        C, R = self.C, self.R
        with self.say("c7.cut.4") as c:
            # {s2path}: CB4 brightens
            self.lab2 = lab = T("stage 2", 30, DIM).next_to(_p(BAR_X0, BAR2_Y), LEFT, buff=0.3)
            self.play(*[restyle(w, op=1, width=CRIT_W) for w in (C.w_34, C.w_out)],
                      restyle(C.cb[3], outline=BLUE, width=CRIT_W), *appear(lab, shift=None),
                      *disappear(self.cmp), run_time=1.4)

            # {s2bar}
            self.bar2 = segs = bar_segs((0.2, 5.5, 0.1), (PINK, PURPLE, GOLD), BAR2_Y)
            self.eq2 = eq = bar_sum(["0.2", "5.5", "0.1"], (PINK, PURPLE, GOLD), "5.8", BAR2_Y)
            c.wait_until("zero point two")
            self.play(ReplacementTransform(R.ff.box.copy(), segs[0]), *appear(eq[0], eq[1], lag=0.2), run_time=1.2)
            c.wait_until("five point five")
            nm4 = T("CB4", 28, FG).move_to(segs[1])
            self.play(ReplacementTransform(C.cb[3].copy(), segs[1]), *during(appear(nm4, shift=None), 0.6, 1.0),
                      *appear(eq[2], eq[3], lag=0.2), run_time=1.2)
            c.wait_until("zero point one")
            self.play(ReplacementTransform(C.ff_out.box.copy(), segs[2]), *appear(eq[4], eq[5], lag=0.2),
                      run_time=1.2)
            c.wait_until("five point eight")
            self.play(*appear(eq[6], eq[7], lag=0.2), run_time=1.0)
            settle(self, eq)

            # {question}
            c.wait_until("question")
            self.q = q = MathTex(r"T_c = 6.5\text{ or }5.8\ ?", font_size=44, color=YELLOW).move_to(_p(0.6, BOTTOM_Y))
            self.play(*appear(q), run_time=1.0)

    # ------------------------------------------------------------------ c7.cut.5
    def ride_swap(self, old, new, shift, n=3):
        """The label rides with the marker; its number swaps whole (old fades out, then new fades
        in, same spot), the unit glyphs stay. `n` = number glyphs at the start of each label."""
        new.shift(-shift)             # built at its end spot: start beside the old label
        start = new.get_center()
        ghosts = [g.copy() for g in old[:n]]
        g0 = [g.get_center() for g in ghosts]
        for g in new[:n]:
            g.set_opacity(0)
        self.remove(old)
        self.add(new, *ghosts)
        self._ghosts = ghosts

        def upd(m, a):
            m.move_to(start + a * shift)
            for g in m[:n]:
                g.set_opacity(max(0.0, 2 * a - 1))
            for g, c0 in zip(ghosts, g0):
                g.move_to(c0 + a * shift).set_opacity(max(0.0, 1 - 2 * a))
        return UpdateFromAlphaFunc(new, upd)

    def clip5(self):
        b1, b2 = self.bar1, self.bar2
        with self.say("c7.cut.5") as c:
            # {try}: one more shared edge; one period marker over both bars
            self.play(*self.edge(1.4), run_time=1.4)
            mk, arr = period_marker(5.8), tc_arrow(5.8)
            tc = MathTex("T_c", font_size=44, color=YELLOW).next_to(arr, LEFT, buff=0.2)
            c.wait_until("one period")
            self.play(GrowFromCenter(mk), GrowFromCenter(arr), *appear(tc, shift=None), run_time=1.4)

            # {short}: 5.8 ns
            c.wait_until("short")
            v58 = T("5.8 ns", 30, GOLD).next_to(_p(ns_x(5.8), ARROW_Y), RIGHT, buff=0.15)
            self.play(*appear(v58), run_time=1.0)
            c.wait_until("just fits")
            tick2 = check_mark().scale(0.8).move_to(_p(ns_x(5.8) + 0.4, BAR2_Y))
            self.play(*appear(tick2, shift=None), FlashAround(b2[-1], color=GREEN, buff=0.12, time_width=1.5),
                      run_time=1.2)

            # {red}: stage 1 overshoots by 0.7 ns: set-up violated
            c.wait_until("red")
            viol = T("set-up violated", 30, RED).next_to(_p(ns_x(5.8) + 0.15, (BAR1_Y + BAR2_Y) / 2), RIGHT, buff=0)
            self.play(*recolor([b1[3], b1[4]], RED), run_time=1.2)
            self.play(*appear(viol), run_time=1.0)  # early: names the overshoot as it turns red
            c.wait_until("breaks the rule")
            self.play(FlashAround(VGroup(b1[3], b1[4]), color=RED, buff=0.1, time_width=1.5), run_time=1.4)

            # {slide}: the period stretches to 6.5; stage 1 fits, stage 2 idles 0.7 ns
            c.wait_until("slide")
            v65 = T("6.5 ns", 30, GOLD).next_to(_p(ns_x(6.5), ARROW_Y), RIGHT, buff=0.15)
            shift = RIGHT * (ns_x(6.5) - ns_x(5.8))
            self.play(*during(disappear(viol) + [b1[3].animate.set_color(PURPLE), b1[4].animate.set_color(GOLD)],
                              0, 0.4),
                      *during([mk.animate.shift(shift), Transform(arr, tc_arrow(6.5)), tick2.animate.shift(shift)],
                              0.2, 0.9),
                      *during([self.ride_swap(v58, v65, shift)], 0.2, 0.9), run_time=2.0)
            self.remove(*self._ghosts)
            tick1 = check_mark().scale(0.8).move_to(_p(ns_x(6.5) + 0.4, BAR1_Y))
            self.play(*appear(tick1, shift=None), run_time=1.0)
            idle = DashedVMobject(Rectangle(width=0.7 * NS, height=BAR_H), num_dashes=12).set_stroke(DIM, 3)
            idle.move_to(_p(ns_x(5.8 + 0.35), BAR2_Y))
            idle_l = T("idle", 30, DIM).next_to(idle, DOWN, buff=0.15)
            c.wait_until("more time")
            self.play(FadeIn(idle), *appear(idle_l), run_time=1.2)

            # {slowest}
            c.wait_until("slowest")
            ans = VGroup(T("the slowest stage decides", 40, YELLOW),
                         MathTex(r"T_c = 6.5\text{ ns}", font_size=44, color=GOLD)).arrange(RIGHT, buff=0.6)
            ans.move_to(_p(0.3, BOTTOM_Y))
            self.play(*swap(self.q, ans), run_time=1.4)
        self.wait(4.8)
