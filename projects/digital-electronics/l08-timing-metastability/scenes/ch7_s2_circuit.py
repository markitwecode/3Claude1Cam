"""Chapter 7, scene 2: the circuit (p. 117) and its critical path. Clips c7.circuit.1 – c7.circuit.5.

This file owns p. 117's circuit for all of ch7: copy the block between the `# ===` rulers.
circuit() is built in design units and scaled to full width (C.s(), about 0.93), centred at (0, CIRC_Y).
Input -> FF_in (L6 make_ff at K = 0.55) -> Q forks -> CB1 (upper) / CB2 (lower) -> CB3 -> (A) -> CB4
-> FF_out -> Output. CLK (YELLOW) along the bottom, branching up into both clock triangles.
Blocks BLUE outlines (no fill), names BLUE inside, t_pd labels PURPLE; wires FG at 0.7 opacity.
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

LIT = "#CDA9DE"            # a t_pd label "brightened" (light PURPLE)
CRIT_W = 8                 # critical-path stroke width
OFF = 0.3                  # off-critical-path opacity


def sum_tex(a, b, c_, total):
    return MathTex(a, "+", b, "+", c_, "=", total + r"\text{ ns}", font_size=44, color=GOLD)


class CircuitCritical(NarratedScene):
    def construct(self):
        self.C = circuit()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- block lighting ------------------------------------------------------------------------
    def light(self, i, on=True):
        C = self.C
        return [restyle(C.cb[i], outline=YELLOW if on else BLUE, width=6 if on else 4)]

    def label(self, i, on=True):
        return [self.C.tpd[i].animate.set_color(LIT if on else PURPLE)]

    # ------------------------------------------------------------------ c7.circuit.1
    def clip1(self):
        C = self.C
        with self.say("c7.circuit.1") as c:
            self.play(*[FadeIn(m) for m in C.parts], run_time=0.8)  # early: s1's circuit returns (continuity)
            clk = VMobject().set_points_as_corners(
                [C.clk_bus.get_start(), C.br_in.get_start(), C.br_in.get_end()]).set_stroke(YELLOW, 10)
            qw = C.ff_in.q_w.copy().set_stroke(YELLOW, 10)
            self.play(VShowPassingFlash(clk, time_width=0.6, run_time=1.0),
                      time_span(FlashAround(C.tri_in, color=YELLOW, buff=0.08, time_width=1.5), 0.6, 1.5),
                      time_span(FlashAround(C.ff_in.q_l, color=YELLOW, buff=0.08, time_width=1.5), 1.3, 2.4),
                      run_time=2.4)
            self.play(time_span(VShowPassingFlash(qw, time_width=0.8), 0, 0.8), run_time=0.8)

            # {fork}: a pulse leaves Q and splits at the fork
            c.wait_until("fork")
            k1, (b1, _) = route_keys(C, 1)
            k2, (b2, _) = route_keys(C, 2)
            d1, d2 = pulse(), pulse()
            d1.move_to(k1[0][1])
            d2.move_to(k2[0][1])
            self.add(d1, d2)
            self.play(run_pulse(d1, k1, 0, b1), run_pulse(d2, k2, 0, b2), run_time=min(2.0, c.until("cb1") - 0.9))
            self.play(FadeOut(d1, d2), run_time=0.6)

            # {cb1} .. {cb4}: each block lights as it is named, its t_pd label brightening on its number
            steps = (("cb1", "three point two"), ("cb2", "two point five"),
                     ("cb3", "three nanoseconds"), ("cb4", "five point five"))
            for i, (mark, num) in enumerate(steps):
                c.wait_until(mark)
                prev = self.light(i - 1, False) + self.label(i - 1, False) if i else []
                self.play(*self.light(i), *prev, run_time=0.9)
                c.wait_until(num)
                self.play(*self.label(i), run_time=0.8)

    # ------------------------------------------------------------------ c7.circuit.2
    def clip2(self):
        C = self.C
        with self.say("c7.circuit.2") as c:
            # {spec}: the registers flash; p. 118's first line slides in under the circuit
            self.play(*self.light(3, False), *self.label(3, False),
                      FlashAround(C.ff_in.box, color=FG, time_width=1.5),
                      FlashAround(C.ff_out.box, color=FG, time_width=1.5), run_time=1.4)
            l1 = MathTex(r"\text{Assume that for each D-type FF,}", font_size=36)
            l2 = MathTex(r"\text{max }", r"t_{pc}", r"= 0.2\text{ ns and min }", r"t_{su}", r"= 0.1\text{ ns.}",
                         font_size=36)
            l2[1].set_color(PINK)
            l2[3].set_color(GOLD)
            spec = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            spec.to_edge(LEFT, buff=0.6).align_to(_p(0, C.clk_bus.get_y() - 0.45), UP)
            self.spec = spec
            c.wait_until("the slide")
            self.play(*appear(l1, l2, lag=0.5), run_time=1.6)
            c.wait_until("at most")
            self.play(FlashUnder(l2[1], color=PINK, time_width=1.5), run_time=1.4)
            c.wait_until("zero point one")
            self.play(FlashUnder(l2[3], color=GOLD, time_width=1.5), run_time=1.4)

            # {same}: a small DIM inset of ch1 s6's budget bar, tagged "part 1"
            c.wait_until("same")
            bar = budget_bar([("t_{pc}", PINK, 0.55), ("t_{pd}", PURPLE, 2.3), ("t_{su}", GOLD, 0.4)], 3.25,
                             x0=2.7, y=spec.get_center()[1] + 0.05, sym_size=32)
            eq = MathTex("0.2", "+", "4.7", "+", "0.1", r"= 5.0\text{ ns}", font_size=34)
            for i, col in ((0, PINK), (2, PURPLE), (4, GOLD)):
                eq[i].set_color(col)
            eq.next_to(bar.outline, DOWN, buff=0.22)
            tag = T("part 1", 30, DIM).next_to(bar.tc, LEFT, buff=0.35)
            inset = VGroup(bar, eq, tag)
            inset.set_opacity(0.6)
            bar.outline.set_stroke(opacity=0.6).set_fill(opacity=0)
            self.inset = inset
            self.play(*appear(VGroup(bar, eq), shift=None), *appear(tag), run_time=1.2)

    # ------------------------------------------------------------------ c7.circuit.3
    def clip3(self):
        C = self.C
        with self.say("c7.circuit.3") as c:
            # {routes}: two pulses leave the fork together, each at the speed its delays set
            k1, (_, t13) = route_keys(C, 1)
            k2, (_, t23) = route_keys(C, 2)
            d1, d2 = pulse(), pulse()
            d1.move_to(k1[0][1])
            d2.move_to(k2[0][1])
            self.add(d1, d2)
            self.play(run_pulse(d1, k1, 0, k1[-1][0]), run_pulse(d2, k2, 0, k1[-1][0]),
                      run_time=max(1.5, c.until("sum1") - 0.8))
            self.play(FadeOut(d1, d2), run_time=0.5)

            # {sum1}: a running sum over route 1, term by term with the blocks
            s1 = sum_tex("3.2", "3", "5.5", "11.7").move_to(_p(-1.4, 3.35))
            self.sum1 = s1
            c.wait_until("three point two")
            self.play(*appear(s1[0]), *self.light(0), run_time=0.9)
            c.wait_until("plus three")
            self.play(*appear(s1[1], s1[2], lag=0.15), *self.light(0, False), *self.light(2), run_time=0.9)
            c.wait_until("plus five point five")
            self.play(*appear(s1[3], s1[4], lag=0.15), *self.light(2, False), *self.light(3), run_time=0.9)
            c.wait_until("eleven point seven")
            self.play(*appear(s1[5], s1[6], lag=0.15), *self.light(3, False), run_time=1.0)
            settle(self, s1)

            # {sum2}: under route 2
            self.play(*disappear(self.spec, self.inset), run_time=0.8)
            c.wait_until("sum2")
            s2 = sum_tex("2.5", "3", "5.5", "11.0").move_to(_p(-2.0, C.clk_bus.get_y() - 0.75))
            self.sum2 = s2
            self.play(VShowPassingFlash(route_path(C, 2), time_width=0.5), *appear(s2, shift=None),
                      run_time=1.4)

            # {wait}: replay up to CB3's two inputs; CB2's pulse waits there, CB3 lights on CB1's
            c.wait_until("wait")
            d1, d2 = pulse(), pulse()
            d1.move_to(k1[0][1])
            d2.move_to(k2[0][1])
            self.add(d1, d2)
            self.play(run_pulse(d1, k1, 0, t23, stop=t13), run_pulse(d2, k2, 0, t23, stop=t23),
                      run_time=min(t23 / 1.0, max(1.5, c.until("no help") - 0.3)))
            v_lo = C.w_2.get_end()
            v_hi = C.w_1.get_end()
            xj = _verts(C.w_1)[1][0]
            st2 = T("2.5 ns", 30, GOLD).next_to(_p(xj, (v_lo[1] + C.w_2.get_start()[1]) / 2), LEFT, buff=0.15)
            st1 = T("3.2 ns", 30, GOLD).next_to(_p(xj, (v_hi[1] + C.w_1.get_start()[1]) / 2), LEFT, buff=0.15)
            self.stamps = (st1, st2)
            c.wait_until("no help")
            self.play(*appear(st2), restyle(d2, fill=DIM), run_time=1.0)
            c.wait_until("has to wait")
            self.play(run_pulse(d1, k1, t23, t13), run_time=0.9 * (t13 - t23) / 0.7)
            self.play(*appear(st1), *self.light(2), run_time=1.0)
            self.dots = (d1, d2)

    # ------------------------------------------------------------------ c7.circuit.4
    def clip4(self):
        C = self.C
        crit_r1 = [C.w_q, C.w_up, C.w_1, C.w_34, C.w_out]
        with self.say("c7.circuit.4") as c:
            # {critical}: route 1 brightened and thickened
            self.play(*[restyle(w, op=1, width=CRIT_W) for w in crit_r1],
                      *[restyle(C.cb[i], outline=BLUE, width=CRIT_W) for i in (0, 2, 3)], run_time=1.5)
            crit = T("critical path", 40, YELLOW).move_to(_p(3.6, 3.35))
            self.crit = crit
            c.wait_until(own_word=crit)
            self.play(*appear(crit), run_time=1.0)
            c.wait_until("here")
            self.play(*disappear(*self.dots, *self.stamps), run_time=0.8)
            self.play(VShowPassingFlash(route_path(C, 1, width=12), time_width=0.5), run_time=2.0)

            # {dim}: CB2 and its wires dim
            c.wait_until("dim")
            self.play(*set_alpha([C.w_dn, C.w_2, C.cb[1], C.names[1], C.tpd[1]], OFF), run_time=1.2)

            # {why}: a tiny DIM ch1 reminder in the corner
            c.wait_until("why")
            why = VGroup(T("part 1", 28, DIM), T("worst case = longest delays", 30, DIM))
            why.arrange(DOWN, aligned_edge=RIGHT, buff=0.15).to_corner(DR, buff=0.5)
            self.why = why
            self.play(*appear(*why, lag=0.3), run_time=1.2)

    # ------------------------------------------------------------------ c7.circuit.5
    def clip5(self):
        C = self.C
        s = C.s()

        def lab(v, like, op=1.0):
            return tpd_tex(v, TPD_SIZE * s).move_to(like).set_opacity(op)

        def sm(a, total, like):
            return sum_tex(a, "3", "5.5", total).move_to(like)

        def tnum(m, v):      # the number's glyphs in a t_pd label ("t", "p", "d", "=" come first)
            return list(m[0][4:4 + len(v)])

        def snum(m, a, total):   # the changing term and the total in a sum
            return list(m[0]) + list(m[6][:len(total)])

        def renum(old, new, old_g, new_g, op=1.0):
            """Only the numbers change, in place: `new` takes `old`'s place with its new numbers
            hidden; standalone copies of the old numbers fade out, then the new ones fade in."""
            ghosts = [g.copy() for g in old_g]
            for g in new_g:
                g.set_opacity(0)
            self.remove(old)
            self.add(new, *ghosts)

            def show(m, a):
                for g in new_g:
                    g.set_opacity(a * op)
            return during([FadeOut(g) for g in ghosts], 0, 0.5) + \
                during([UpdateFromAlphaFunc(new, show)], 0.45, 1.0)

        with self.say("c7.circuit.5") as c:
            # {faster}: CB2 2.5 -> 2.0, its sum 11.0 -> 10.5; the critical 11.7 stays put; tick back
            t2a, s2a = lab("2.0", C.tpd[1], OFF), sm("2.0", "10.5", self.sum2)
            self.play(*renum(C.tpd[1], t2a, tnum(C.tpd[1], "2.5"), tnum(t2a, "2.0"), OFF),
                      *renum(self.sum2, s2a, snum(self.sum2, "2.5", "11.0"), snum(s2a, "2.0", "10.5")),
                      time_span(FlashAround(self.sum1[6], color=YELLOW, time_width=1.5), 0.6, 1.5),
                      run_time=1.5)
            t2b, s2b = lab("2.5", t2a, OFF), sm("2.5", "11.0", s2a)
            self.play(*renum(t2a, t2b, tnum(t2a, "2.0"), tnum(t2b, "2.5"), OFF),
                      *renum(s2a, s2b, snum(s2a, "2.0", "10.5"), snum(s2b, "2.5", "11.0")), run_time=min(0.9, max(0.5, c.until("cb1fast") - 0.4)))
            C.tpd[1], self.sum2 = t2b, s2b

            # {cb1fast}: CB1 3.2 -> 2.9, the critical sum 11.7 -> 11.4
            c.wait_until("cb1fast")
            t1a, s1a = lab("2.9", C.tpd[0]), sm("2.9", "11.4", self.sum1)
            self.play(*renum(C.tpd[0], t1a, tnum(C.tpd[0], "3.2"), tnum(t1a, "2.9")),
                      *renum(self.sum1, s1a, snum(self.sum1, "3.2", "11.7"), snum(s1a, "2.9", "11.4")), run_time=1.3)

            # {until}: CB1 slides on down past 2.5; route 2 brightens, route 1 dims
            c.wait_until("until")
            t1b, s1b = lab("2.3", t1a), sm("2.3", "10.8", s1a)
            r2_on = [restyle(w, op=1, width=CRIT_W) for w in (C.w_dn, C.w_2)] + \
                [restyle(C.cb[1], op=1, width=CRIT_W), restyle(C.names[1], op=1), restyle(t2b, op=1)]
            r1_off = [restyle(w, op=OFF, width=WIRE_W) for w in (C.w_up, C.w_1)] + \
                [restyle(C.cb[0], op=OFF, width=4), restyle(C.names[0], op=OFF)]
            self.play(*during(renum(t1a, t1b, tnum(t1a, "2.9"), tnum(t1b, "2.3"))
                             + renum(s1a, s1b, snum(s1a, "2.9", "11.4"), snum(s1b, "2.3", "10.8")), 0, 0.55),
                      *during(r2_on + r1_off, 0.45, 1.0), run_time=2.6)
            c.wait_until("moves")
            self.play(VShowPassingFlash(route_path(C, 2, width=12), time_width=0.5),
                      FlashAround(self.crit, color=YELLOW, time_width=1.5), run_time=1.6)

        # restore: route 1 critical again
        t1c, s1c = lab("3.2", t1b), sm("3.2", "11.7", s1b)
        r1_on = [restyle(w, op=1, width=CRIT_W) for w in (C.w_up, C.w_1)] + \
            [restyle(C.cb[0], op=1, width=CRIT_W), restyle(C.names[0], op=1)]
        r2_off = [restyle(w, op=OFF, width=WIRE_W) for w in (C.w_dn, C.w_2)] + \
            [restyle(C.cb[1], op=OFF, width=4), restyle(C.names[1], op=OFF), restyle(t2b, op=OFF)]
        self.play(*during(renum(t1b, t1c, tnum(t1b, "2.3"), tnum(t1c, "3.2"))
                             + renum(s1b, s1c, snum(s1b, "2.3", "10.8"), snum(s1c, "3.2", "11.7")), 0, 0.6), *during(r1_on + r2_off, 0.4, 1.0),
                  run_time=2.0)
        self.wait(2.5)
