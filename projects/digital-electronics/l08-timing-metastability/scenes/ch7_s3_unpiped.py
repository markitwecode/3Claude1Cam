"""Chapter 7, scene 3: without pipelining, T_c = 12 ns; latency 12 ns, throughput 83.3 MHz. Clips c7.unpiped.1 – c7.unpiped.3.

Circuit block copied from ch7_s2_circuit.py; budget bar block from ch1_s6 (via ch7_s2).
Chapter bar scale (s4, s5 share it): NS = 0.85 units per ns, left edge BAR_X0 = -4.6, centre y BAR_Y = -0.75,
height BAR_H 0.5; 12 ns ends at x 5.6. Ends on GOLD T 30 "12 ns" over "83.3 MHz", left x -6.6, top y 3.5.
Circuit shrink matches ch7_s4_cut (SHRINK 0.66, top 3.55, centre x 0.6, over s4's panel box); pin letters,
t_pd, Input/Output/CLK and A fade as it shrinks, CB names grow to T 28 just outside their blocks.
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


def _fade_family(mob, f):
    for sm in mob.family_members_with_points():
        sm.set_fill(opacity=sm.get_fill_opacity() * f, family=False)
        sm.set_stroke(opacity=sm.get_stroke_opacity() * f, family=False)


def _ride(m, P, v, a, b, m0, m1, fade_out=None, final=None, fade_in=None):
    """m rides the circuit's shrink (scale SHRINK about P, shift v, smooth over [m0, m1] of the play)
    while it runs over [a, b] of the play; fades out over fade_out; with `final`, jumps there and
    fades in over fade_in. Fractions are of the whole play."""
    start = m.copy()

    def upd(mob, t):
        g = a + (b - a) * t
        if final is not None and g >= fade_in[0]:
            mob.become(final)
            _fade_family(mob, smooth(min(1.0, (g - fade_in[0]) / (fade_in[1] - fade_in[0]))))
            return
        e = smooth(min(1.0, max(0.0, (g - m0) / (m1 - m0))))
        mob.become(start.copy().scale(1 + (SHRINK - 1) * e, about_point=P).shift(v * e))
        _fade_family(mob, 1 - min(1.0, max(0.0, (g - fade_out[0]) / (fade_out[1] - fade_out[0]))))

    return UpdateFromAlphaFunc(m, upd, rate_func=linear)


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


LIT = "#CDA9DE"
CRIT_W = 8
OFF = 0.3

# chapter-7 bar scale (s4 and s5 keep exactly this)
NS = 0.85
BAR_X0 = -4.6
BAR_Y = -0.75
SHRINK, SHRUNK_TOP, SHRUNK_X = 0.66, 3.55, 0.6    # ch7_s4_cut's shrunk circuit
ARR_Y = -1.22
TCL_X, TCL_Y = 2.0, -1.58         # "T_c = 12 ns" under the arrow; latency's "12 ns" sits under it
LAT_Y, THR_Y, MIL_Y = -2.25, -2.78, -3.24
CORNER_X, CORNER_TOP = -6.6, 3.5


def split_line(text, key, size=36, color=GOLD):
    """A T line built as two separate mobjects: (rest, key part), placed exactly as one T would set them."""
    full = T(text, size, color)
    i = text.index(key)
    head = T(text[:i].rstrip(), size, color)
    num = T(key, size, color)
    head.move_to(select(full, text[:i].rstrip())[0])
    num.move_to(select(full, key)[0])
    return full, head, num


class Unpiped(NarratedScene):
    def construct(self):
        C = circuit()
        C.remove(C.a_tag)
        self.C = C
        # s2's c7.circuit.4 look: route 1 critical, CB2 dimmed
        for w in (C.w_q, C.w_up, C.w_1, C.w_34, C.w_out):
            w.set_stroke(width=CRIT_W, opacity=1)
        for i in (0, 2, 3):
            C.cb[i].set_stroke(BLUE, CRIT_W)
        for w in (C.w_dn, C.w_2, C.cb[1]):
            w.set_stroke(opacity=OFF)
        C.names[1].set_opacity(OFF)
        C.tpd[1].set_opacity(OFF)
        self.play(*[FadeIn(m) for m in C.parts], run_time=0.8)  # early: s2's circuit returns (continuity)
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ helpers
    def edge(self, start=True, end=True):
        C = self.C
        out = []
        if start:
            out.append(FlashAround(C.tri_in, color=YELLOW, buff=0.06, time_width=1.5))
        if end:
            out.append(FlashAround(C.tri_out, color=YELLOW, buff=0.06, time_width=1.5))
        return out

    def token(self, color, run_time, k, extra=()):
        """A token leaves FF_in on an edge, runs the critical path, is captured on the next edge and
        lands as result dot k beside "Output"."""
        C = self.C
        keys, _ = route_keys(C, 1)
        d = pulse(color).move_to(keys[0][1])
        self.play(*self.edge(end=False), FadeIn(d, scale=0.5), *extra, run_time=0.7)
        self.play(run_pulse(d, keys, 0, keys[-1][0]), run_time=run_time)
        res = Dot(radius=0.11, color=color).next_to(C.ff_out.q_w, RIGHT, buff=0.25 + 0.34 * k)
        self.play(*self.edge(start=False), FadeOut(d, scale=0.5),
                  time_span(FadeIn(res, scale=0.5), 0.35, 0.8), run_time=0.8)
        self.results.append(res)

    # ------------------------------------------------------------------ c7.unpiped.1
    def clip1(self):
        C = self.C
        x = BAR_X0
        segs = [("t_{pc}", PINK, 0.2 * NS)] + [("t_{pd}", PURPLE, d * NS) for d in (3.2, 3, 5.5)] + \
            [("t_{su}", GOLD, 0.1 * NS)]
        bar = budget_bar(segs, 12 * NS, x0=BAR_X0, y=BAR_Y, syms=False)
        self.bar = bar
        with self.say("c7.unpiped.1") as c:
            # {bar}: the circuit shrinks to the top third; one clock period appears below it
            # (as ch7_s4_cut's c7.cut.3: pin letters, t_pd, Input/Output/CLK and A fade; CB names stay at 28)
            gone = [C.in_l, C.out_l, C.clk_l, *C.tpd, C.a_mark]
            pins = [lab for ff in (C.ff_in, C.ff_out) for lab in (ff.d_l, ff.q_l, ff.qb_l)]
            movers = [m for m in C.parts if m not in gone]
            xa = C.xy(X_A, YM)[0]   # s4's panel box, so the shrink lands exactly where s4's does
            ghost = [stage_panel(C, C.ff_in.box.get_left()[0] - 0.2, xa - 0.04, 1).rect,
                     stage_panel(C, xa + 0.04, C.ff_out.box.get_right()[0] + 0.2, 2).rect]
            box = VGroup(*[m.copy() for m in movers], *ghost)
            P = box.get_center()
            new_top = P[1] + SHRINK * (box.get_top()[1] - P[1])
            v = _p(SHRUNK_X - P[0], SHRUNK_TOP - new_top)
            grow = 28 / (32 * C.s() * SHRINK)
            # pin letters leave their flip-flops so they can ride (and fade) on their own
            for ff in (C.ff_in, C.ff_out):
                for lab in (ff.d_l, ff.q_l, ff.qb_l):
                    ff.remove(lab)
                    self.add(lab)
            M0, M1 = 0.15, 0.7      # the shrink's span of the play
            anims = []
            for m in movers:
                if m in C.names:
                    i = C.names.index(m)
                    blk, d = C.cb[i], (DOWN if i == 1 else UP)
                    off = (SHRINK * blk.height + SHRINK * grow * m.height) / 2 + 0.1
                    final = m.copy().scale(SHRINK * grow).move_to(P + SHRINK * (blk.get_center() - P) + v + d * off)
                    # crossfade: rides inside its block while fading out, fades in outside as the shrink ends
                    anims += during(_ride(m, P, v, M0, 0.85, M0, M1, fade_out=(M0, 0.42), final=final,
                                          fade_in=(0.65, 0.85)), M0, 0.85)
                else:
                    anims += during(m.animate.scale(SHRINK, about_point=P).shift(v), M0, M1)
            riders = gone + pins
            self.play(*during([_ride(m, P, v, 0, M1, M0, M1, fade_out=(0.05, 0.5)) for m in riders], 0, M1),
                      *anims,
                      *during([FadeIn(bar.outline)], 0.6, 1.0),
                      *during(appear(bar.tc, shift=None), 0.7, 1.0),
                      run_time=min(2.4, c.until("rule") - 0.1))
            for m in riders:
                self.remove(*m.get_family())
            for m in gone:
                C.remove(m)
            for m in (C.o, C.u):
                m.scale(SHRINK, about_point=P).shift(v)

            # {rule}
            rule = MathTex("T_c", r"\ge", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", font_size=48)
            for i, col in ((0, YELLOW), (2, PINK), (4, PURPLE), (6, GOLD)):
                rule[i].set_color(col)
            rule.move_to([0.5, -0.1, 0])
            self.rule = rule
            c.wait_until("rule")
            self.play(*appear(rule, shift=None), run_time=1.2)
            # one box slides from term to term, each on its own words
            hb = None
            for cue, i, col in (("clock-to-output", 2, PINK), ("logic's", 4, PURPLE), ("set-up", 6, GOLD)):
                c.wait_until(cue)
                nb = token_box(rule[i], rule, color=col)
                fl = FlashAround(rule[i], color=col, time_width=1.5, buff=0.12)
                if hb is None:
                    self.play(FadeIn(nb), fl, run_time=1.0)
                    hb = nb
                else:
                    self.play(Transform(hb, nb), fl, run_time=1.0)
            c.wait_until("pink")
            self.play(FadeOut(hb), run_time=0.5)

            # the total, built term by term under the bar
            total = MathTex("T_c", "=", "0.2", "+", "3.2", "+", "3", "+", "5.5", "+", "0.1", "=",
                            r"12\text{ ns}", font_size=44)
            for i, col in ((0, YELLOW), (2, PINK), (4, PURPLE), (6, PURPLE), (8, PURPLE), (10, GOLD),
                           (12, YELLOW)):
                total[i].set_color(col)
            total.move_to([0.5, LAT_Y, 0])
            self.total = total

            # {pink}: from the input register
            c.wait_until("pink")
            self.play(TransformFromCopy(C.ff_in.box, bar.segs[0]),
                      *during(appear(total[0], total[1], total[2], shift=None), 0.5, 1.0), run_time=1.5)

            # {purple}: CB1, CB3, CB4
            self.names, self.divs = [], []
            steps = (("three point two", 0, 1, 0), ("three", 1, 2, 2), ("five point five", 0, 3, 3))
            for k, (cue, nth, j, cb) in enumerate(steps):
                c.wait_until(cue, nth=nth)
                room = c.until(steps[k + 1][0], nth=steps[k + 1][1]) if k < 2 else c.until("gold")
                seg = bar.segs[j]
                nm = T(f"CB{cb + 1}", 30, FG).move_to(seg)
                self.names.append(nm)
                extra = []
                if j > 1:
                    dv = Line(seg.get_corner(UL), seg.get_corner(DL)).set_stroke(BG, 3).set_z_index(0.5)
                    self.divs.append(dv)
                    extra = during([FadeIn(dv)], 0.75, 1.0)
                self.play(TransformFromCopy(C.cb[cb], seg), *extra,
                          *during(appear(nm, shift=None), 0.5, 1.0),
                          *during(appear(total[2 * j + 1], total[2 * j + 2], shift=None), 0.3, 0.8),
                          run_time=min(1.2, max(0.6, room - 0.05)))

            # {gold}: from the output register
            c.wait_until("gold")
            self.play(TransformFromCopy(C.ff_out.box, bar.segs[4]),
                      *during(appear(total[9], total[10], shift=None), 0.5, 1.0), run_time=1.4)

            # {total}: = 12 ns; the YELLOW T_c arrow spans the bar
            c.wait_until("total")
            arr = DoubleArrow([BAR_X0, ARR_Y, 0], [BAR_X0 + 12 * NS, ARR_Y, 0], buff=0, color=YELLOW,
                              stroke_width=3, tip_length=0.2, max_tip_length_to_length_ratio=0.1)
            tcl = MathTex(r"T_c = 12\text{ ns}", font_size=40, color=YELLOW).move_to([TCL_X, TCL_Y, 0])
            self.arr, self.tcl = arr, tcl
            self.play(*appear(total[11], total[12], shift=None), GrowFromCenter(arr),
                      *during(appear(tcl, shift=None), 0.4, 1.0), run_time=min(1.5, c.until() - 0.05))
            settle(self, total)

    # ------------------------------------------------------------------ c7.unpiped.2
    def clip2(self):
        C, bar = self.C, self.bar
        end_x = BAR_X0 + 12 * NS
        gold = bar.segs[4]
        with self.say("c7.unpiped.2") as c:
            # {faster}: the period marker nudges left; set-up pokes past and turns RED; back to 12 ns
            mk = Line([end_x, BAR_Y - 0.45, 0], [end_x, BAR_Y + 0.45, 0]).set_stroke(YELLOW, 6).set_z_index(3)
            self.play(FadeIn(mk), run_time=0.5)
            self.play(mk.animate.shift(0.5 * LEFT), run_time=1.3)
            self.play(restyle(gold, fill=RED),
                      FlashAround(gold, color=RED, time_width=1.5, buff=0.12), run_time=1.2)
            # the RED overshoot holds through "...too late for its set-up time"
            c.wait_until("latency")
            tick = check_mark(GREEN).scale(0.7).move_to([end_x, BAR_Y + 0.85, 0])
            self.play(mk.animate.shift(0.5 * RIGHT), restyle(gold, fill=GOLD),
                      *during(appear(tick, shift=None), 0.5, 1.0), run_time=1.0)

            # {latency}: a BLUE token, edge to edge
            self.results = []
            self.token(BLUE, 2.6, 0)

            # the latency line takes the total's place
            full, lat_a, lat_n = split_line("latency = 1 cycle = 12 ns", "12 ns")
            full_x = TCL_X - (lat_n.get_x() - full.get_x())
            for m in (lat_a, lat_n):
                m.shift([full_x - full.get_x(), LAT_Y - full.get_y(), 0])
            self.lat_a, self.lat_n = lat_a, lat_n
            c.wait_until("so the latency")
            grp = VGroup(lat_a, lat_n)
            self.play(*swap(self.total, grp), *disappear(mk, tick), run_time=min(1.4, c.until() - 0.05))
            self.remove(grp)
            self.add(lat_a, lat_n)

    # ------------------------------------------------------------------ c7.unpiped.3
    def clip3(self):
        C = self.C
        with self.say("c7.unpiped.3") as c:
            # {throughput}: GREEN, then TEAL, one period apart
            self.token(GREEN, 1.6, 1)

            full, thr_a, thr_n = split_line("throughput = 1/12 ns ≈ 83.3 MHz", "83.3 MHz")
            for m in (thr_a, thr_n):
                m.shift([self.lat_a.get_left()[0] - full.get_left()[0], THR_Y - full.get_y(), 0])
            self.thr_a, self.thr_n = thr_a, thr_n
            c.wait_until(own_word=thr_a)
            self.play(*appear(thr_a, thr_n, shift=None, lag=0.3), run_time=1.2)
            self.token(TEAL, 1.2, 2)

            # {million}
            mil = T("≈ 83 million results per second", 28, DIM)
            mil.move_to([0, MIL_Y, 0]).align_to(thr_a, LEFT)
            c.wait_until("million")
            self.play(*appear(mil, shift=0.1 * UP), run_time=1.0)

            # {same}: latency and the clock period, the same 12 ns
            c.wait_until("same")
            eq = MathTex("=", font_size=34, color=YELLOW).rotate(PI / 2)
            eq.move_to([TCL_X, (self.tcl.get_bottom()[1] + self.lat_n.get_top()[1]) / 2, 0])
            self.play(FlashAround(self.lat_n, color=YELLOW, time_width=1.5, buff=0.1),
                      FlashAround(self.tcl, color=YELLOW, time_width=1.5, buff=0.1),
                      time_span(FadeIn(eq), 0.6, 1.4), run_time=1.8)

            # {keep}: the two numbers go to the top-left corner
            c.wait_until("keep")
            sweep_clear(self, keep=[self.lat_n, self.thr_n], run_time=1.2)
            sc = 30 / 36
            t1 = self.lat_n.copy().scale(sc)
            t1.move_to([CORNER_X + t1.width / 2, CORNER_TOP - t1.height / 2, 0])
            t2 = self.thr_n.copy().scale(sc)
            t2.next_to(t1, DOWN, buff=0.18).align_to(t1, LEFT)
            self.play(self.lat_n.animate.scale(sc).move_to(t1), self.thr_n.animate.scale(sc).move_to(t2),
                      run_time=1.6)
