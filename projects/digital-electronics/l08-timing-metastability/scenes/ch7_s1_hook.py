"""Chapter 7, scene 1: hook: title card, ch6's pipelined path (small), p. 117's circuit, two questions.
Clips c7.hook.1 – c7.hook.2.

{last}: ch6 s6's pipelined path (pipe_diagram, scaled 0.6) with one long budget bar under it that
becomes the two shorter stage bars. {circuit}: ch7_s2's circuit() at its own size/position, drawn
left to right; C.a_tag shown on "from the slides" and faded on {extra} (with C.a_mark, which the
ghost register covers). {fast}: YELLOW T_c = ? above. {extra}: dashed ghost of a_register(C), YELLOW
"?" right of its branch. {almost}: GOLD "× 2 ?" beside it. Ends with everything faded.
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
from lib.titles import title_card  # noqa: E402


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


# =============================================================================================
# THE pipelined path (ch6 s6; ch7's hook reopens it). Built at scale K6 of ch1's path:
#   registers (make_ff, box BG-filled) at x -5 / 0 / 5, y FY (0.3 in c6.reg.1–3, 1.8 in c6.reg.4);
#   box 1.125 x 1.95; pin row FY + 0.45; each register has 2 DIM ghost boxes behind it (+0.1, +0.2);
#   "register" labels T 30 FG at y FY + 1.5; logic blocks BLUE stroke 4, BG fill, height 1.3 on
#   the pin row: stage 1 x -3.8..-1.2, stage 2 x 1.2..3.8 (unpipelined: one block -3.8..3.8);
#   their labels T 30 BLUE on the label row; Q_0 GREEN / D_1 BLUE MathTex 36 over the wires;
#   CLK bus YELLOW y FY - 1.725 from x -5.6 to 5, junction dots at -5 and 0, "CLK" T 32 left.
# =============================================================================================
K6 = 0.75
RX = (-5.0, 0.0, 5.0)
FY0 = 0.3
HX = (BOX_W / 2 + WIRE) * K6          # 1.2: box centre to a pin wire's end
BLK_H = 1.3
LAB_DY = 1.5
BUS_DY = -(BOX_H / 2 + EN_WIRE) * K6  # -1.725
BUS_X0 = -5.6


def make_reg(x, fy):
    f = make_ff()
    f.scale(K6, about_point=ORIGIN)
    for lb in (f.d_l, f.q_l, f.qb_l):
        lb.scale(1.2, about_point=lb.get_center())
    f.shift(_p(x, fy))
    f.box.set_fill(BG, 1)
    br = f.clk_w
    f.remove(br)
    gh = []
    for k in (2, 1):
        r = Rectangle(width=BOX_W * K6, height=BOX_H * K6).set_stroke(DIM, 3).set_fill(BG, 1)
        r.move_to(f.box.get_center() + 0.1 * k * (UP + RIGHT)).set_z_index(-1 - k)
        gh.append(r)
    return f, br, gh


def pipe_diagram(fy=FY0):
    """Parts: .ffs [FF0, mid, FF1] (make_ff, no clock wire) .brs (clock branches) .ghs (pairs of
    ghost boxes) .reg_ls ("register") .wide .wide_l (one block, "combinational logic") .b1 .b2
    .b1_l .b2_l (stage blocks) .q0_l .d1_l .bus .dots [at FF0, at mid] .clk_l .outline (DIM dashed,
    the lifted-out mid register) .bridge (DIM wire across the gap). .pin .fy .lane_map.
    .clk_paths(regs) -> fresh YELLOW paths bus start -> each register's triangle, current positions."""
    D = VGroup()
    D.fy, D.pin = fy, fy + PIN_Y * K6
    D.ffs, D.brs, D.ghs = [], [], []
    for x in RX:
        f, br, gh = make_reg(x, fy)
        D.ffs.append(f)
        D.brs.append(br)
        D.ghs.append(gh)
    lab_y = fy + LAB_DY
    D.reg_ls = [T("register", 30, FG).move_to(_p(x, lab_y)) for x in RX]
    a, b = RX[0] + HX, RX[2] - HX              # -3.8, 3.8
    m0, m1 = RX[1] - HX, RX[1] + HX            # -1.2, 1.2

    def block(x0, x1):
        return Rectangle(width=x1 - x0, height=BLK_H).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(
            _p((x0 + x1) / 2, D.pin))
    D.wide = block(a, b)
    D.wide_l = T("combinational logic", 30, BLUE).move_to(_p(0, lab_y))
    D.b1, D.b2 = block(a, m0), block(m1, b)
    D.b1_l = T("stage 1 logic", 30, BLUE).move_to(_p((a + m0) / 2, lab_y))
    D.b2_l = T("stage 2 logic", 30, BLUE).move_to(_p((m1 + b) / 2, lab_y))
    D.q0_l = set_backstroke(MathTex("Q_0", font_size=36, color=GREEN).next_to(_p(a - 0.3, D.pin), UP, buff=0.12))
    D.d1_l = MathTex("D_1", font_size=36, color=BLUE).next_to(_p(b + 0.3, D.pin), UP, buff=0.12)
    by = fy + BUS_DY
    D.bus = Line(_p(BUS_X0, by), _p(RX[2], by)).set_stroke(YELLOW, 5)
    D.dots = [Dot(_p(x, by), radius=0.08, color=YELLOW) for x in RX[:2]]
    D.clk_l = T("CLK", 32, YELLOW).next_to(_p(BUS_X0, by), LEFT, buff=0.15)
    D.outline = DashedVMobject(Rectangle(width=BOX_W * K6, height=BOX_H * K6), num_dashes=28).set_stroke(DIM, 3)
    D.outline.move_to(_p(RX[1], fy))
    D.bridge = Line(_p(m0, D.pin), _p(m1, D.pin)).set_stroke(DIM, 5)
    # lane geometry: distance along the logic -> x (block 1, a short hop across the gap, block 2)
    D.W, D.H = (m0 - a) - 0.2, 0.5
    D.lane_map = [(0.0, D.W, a + 0.1), (D.W + D.H, 2 * D.W + D.H, m1 + 0.1)]
    D.gap = (m0, m1)

    def clk_paths(idx=(0, 1, 2), width=10):
        s = D.bus.get_start()
        out = []
        for i in idx:
            br = D.brs[i]
            p0, p1 = br.get_start(), br.get_end()
            out.append(VMobject().set_points_as_corners([s, p0, p1]).set_stroke(YELLOW, width))
        return out
    D.clk_paths = clk_paths
    return D


def mid_parts(D):
    return [D.ffs[1], *D.ghs[1], D.brs[1], D.dots[1], D.reg_ls[1]]


def pipelined_parts(D):
    """The closing circuit (ch7's hook): everything of the pipelined path that stays on screen."""
    out = []
    for i in range(3):
        out += [D.ffs[i], *D.ghs[i], D.brs[i], D.reg_ls[i]]
    return out + [D.b1, D.b2, D.b1_l, D.b2_l, D.q0_l, D.d1_l, D.bus, *D.dots, D.clk_l]
# =============================================================================================


# =============================================================================================
# The two stage budgets (ch1_s6 budget_bar, copied verbatim) and their closing layout.
#   unit lengths: t_pc 0.7 PINK, t_pd 2.2 (stage 1) / 3.1 (stage 2) PURPLE, t_su 0.6 GOLD.
#   Side by side (c6.reg.4 {rule}): bar 1 x0 -4.4, bar 2 x0 0.9, y -0.9; formula MathTex 40 at y -2.0.
#   Stacked (closing): both x0 -4.4; bar 1 y -0.9, bar 2 y -2.2; "stage 1/2" T 30 FG left;
#   YELLOW brace under bar 2 spanning -4.4..0.0 with T_c (44); dashed YELLOW guide at x 0.0
#   (y -2.5..-0.5); bar 1's outline stretched to 4.4; tag "the slowest / stage decides"
#   T 36 YELLOW centred (3.3, -1.55).
# =============================================================================================
BAR_H = 0.5          # segment / outline height
BAR_FILL = 0.85      # segment fill opacity (no stroke)
BAR_OUT_W = 3        # YELLOW outline stroke


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


T_PC, T_SU = 0.7, 0.6
T_PD = (2.2, 3.1)
BAR_X0 = (-4.4, 0.9)
BAR_Y = -0.9
STACK_Y2 = -2.2
LONG = T_PC + T_PD[1] + T_SU          # 4.4


def stage_bar(i, x0=None, y=BAR_Y):
    segs = [("t_{pc}", PINK, T_PC), ("t_{pd}", PURPLE, T_PD[i]), ("t_{su}", GOLD, T_SU)]
    return budget_bar(segs, T_PC + T_PD[i] + T_SU, x0=BAR_X0[i] if x0 is None else x0, y=y,
                      sym_size=36)


def stage_rule(bar):
    f = MathTex("T_c", r"\ge", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", font_size=40)
    for k, col in zip((0, 1, 2, 3, 4, 5, 6), (YELLOW, FG, PINK, FG, PURPLE, FG, GOLD)):
        f[k].set_color(col)
    return f.move_to(_p(bar.outline.get_x(), -2.0))


def t_brace(x1, y=STACK_Y2):
    br = span_brace(_p(BAR_X0[0], y - BAR_H / 2), _p(x1, y - BAR_H / 2), DOWN, YELLOW, buff=0.12)
    return br


def t_guide(x):
    return DashedLine(_p(x, STACK_Y2 - 0.3), _p(x, BAR_Y + 0.4), dash_length=0.1).set_stroke(YELLOW, 2)


def closing_tag():
    return VGroup(T("the slowest", 36, YELLOW), T("stage decides", 36, YELLOW)).arrange(
        DOWN, buff=0.14).move_to(_p(3.3, -1.55))
# =============================================================================================


LAST_S = 0.6            # {last}: the ch6 picture at 0.6 of its size
LAST_UP = 0.6           # ... shifted up this much after scaling
LONG_SEGS = [("t_{pc}", PINK, T_PC), ("t_{pd}", PURPLE, T_PD[0] + T_PD[1] + 0.5), ("t_{su}", GOLD, T_SU)]


def small(m):
    return m.scale(LAST_S, about_point=ORIGIN).shift(LAST_UP * UP)


def is_text(m):
    return any(isinstance(x, (Text, MathTex)) for x in m.get_family())


def ghost_register(C):
    """A dashed copy of a_register(C): dashed box, faint pin letters, dashed YELLOW branch."""
    r = a_register(C)
    box = DashedVMobject(r.ff.box.copy().set_fill(opacity=0), num_dashes=30).set_stroke(FG, 3, opacity=0.8)
    labs = VGroup(r.ff.d_l, r.ff.q_l, r.ff.qb_l).copy().set_opacity(0.5)
    tri = r.ff.tri.copy().set_fill(opacity=0).set_stroke(FG, 2, opacity=0.6)
    br = DashedVMobject(r.branch.copy(), num_dashes=12).set_stroke(YELLOW, 4, opacity=0.6)
    g = VGroup(br, box, tri, labs)
    g.box, g.branch = box, br
    return g


class Hook(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------------- clip 1
        with self.say("c7.hook.1") as c:
            card = title_card("Part 7 · Pipelining a circuit")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course, card.part, lag=0.35), run_time=1.3)  # early: title card read whole

            # {last}: ch6's pipelined path, small, with one long period under it
            D = pipe_diagram()
            pic = VGroup(*pipelined_parts(D))
            small(pic)
            long_bar = small(budget_bar(LONG_SEGS, sum(w for _, _, w in LONG_SEGS), x0=-3.3, y=-3.0,
                                        sym_size=36))
            bars = [small(stage_bar(0, y=-3.0)), small(stage_bar(1, y=-3.0))]
            c.wait_until("last")
            ins = (time_span(FadeIn(pic), 0.5, 1.1), time_span(FadeIn(long_bar), 0.6, 1.1))
            sweep_clear(self, *ins, run_time=1.1)  # early: ch6's closing picture, recalled whole
            c.wait_until("can run")
            self.play(*during(disappear(long_bar), 0, 0.45),
                      *during(appear(*bars, shift=None, lag=0.15), 0.5, 1), run_time=1.4)

            # {circuit}: p. 117's circuit draws itself left to right as ch6's picture clears
            C = circuit()
            self.C = C
            c.wait_until("circuit")
            rt = max(3.0, c.until("the one from the slides") - 0.1)
            x0 = min(m.get_left()[0] for m in C.parts)
            x1 = max(m.get_right()[0] for m in C.parts)
            t0, span = 0.22 * rt, 0.78 * rt
            anims = [time_span(FadeOut(m), 0, 0.22 * rt) for m in (pic, *bars)]
            sched = {}
            for m in C.parts:
                a = t0 + (m.get_left()[0] - x0) / (x1 - x0) * 0.72 * span
                b = min(rt, a + max(0.28 * span, m.width / (x1 - x0) * 0.72 * span))
                sched[id(m)] = (a, b)
            # a block's name, t_pd label and outgoing wire wait until the block itself is drawn
            deps = [(C.cb[0], [C.w_1]), (C.cb[1], [C.w_2]), (C.cb[2], [C.w_34]), (C.cb[3], [C.w_out])]
            deps = [(cb, [C.names[i], C.tpd[i], *ws]) for i, (cb, ws) in enumerate(deps)]
            for cb, ms in deps:
                cb_b = sched[id(cb)][1]
                for m in ms:
                    a, b = sched[id(m)]
                    a = max(a, cb_b)
                    sched[id(m)] = (a, max(b, min(rt, a + 0.25 * span)))
            # the "A" marker waits for CB3's outgoing wire, where it points
            a, b = sched[id(C.a_mark)]
            a = max(a, sched[id(C.w_34)][1])
            sched[id(C.a_mark)] = (a, max(b, min(rt, a + 0.25 * span)))
            for m in C.parts:
                a, b = sched[id(m)]
                an = FadeIn(m) if (is_text(m) or isinstance(m, Dot)) else Create(m)
                anims.append(time_span(an, a, b))
            self.play(*anims, run_time=rt)  # early: the circuit drawn whole, then walked
            c.wait_until("the one from the slides")
            self.play(*appear(C.a_tag), run_time=1.0)  # early: the tag names the slides, never read aloud

            # A register at the input, four blocks of logic, and a register at the output
            # one YELLOW highlight per phrase, each landing on its own words
            def hl(m):
                return SurroundingRectangle(m, color=YELLOW, buff=0.16, stroke_width=5)
            h_in = hl(C.ff_in.box)
            c.wait_until("A register at the input")
            self.play(GrowFromCenter(h_in), run_time=min(0.6, 0.5 * c.until("four blocks")))
            c.wait_until("four blocks")
            h_cb = [hl(b) for b in C.cb]
            rt = min(1.0, 0.8 * c.until("and a register"))
            self.play(*during([FadeOut(h_in)], 0, 0.4),
                      *during([GrowFromCenter(h) for h in h_cb], 0.2, 1), run_time=rt)
            c.wait_until("and a register")
            h_out = hl(C.ff_out.box)
            c.wait_until("at the output")
            rt = min(0.8, 0.5 * c.until(None))
            self.play(*during([FadeOut(h) for h in h_cb], 0, 0.5),
                      *during([GrowFromCenter(h_out)], 0.3, 1), run_time=rt)
            self.h_out = h_out

        # ---------------------------------------------------------------- clip 2
        with self.say("c7.hook.2") as c:
            q_tc = MathTex("T_c", "=", "?", font_size=56, color=YELLOW).move_to(_p(0, 3.4))
            self.play(FadeOut(self.h_out), run_time=min(0.6, c.until("How fast")))
            c.wait_until("How fast")
            self.play(*appear(q_tc), run_time=1.2)

            # {extra}: one more register in the middle: a dashed ghost at A
            gh = ghost_register(C)
            qm = MathTex("?", font_size=60, color=YELLOW)
            qm.move_to(C.xy(X_A + 0.5, -0.85))
            c.wait_until("extra")
            self.play(*disappear(C.a_tag, C.a_mark), run_time=0.8)
            self.play(FadeIn(gh, shift=0.3 * DOWN), run_time=1.4)
            self.play(*appear(qm), run_time=0.9)

            # {almost}: × 2 ?
            x2 = MathTex(r"\times", "2", "?", font_size=48, color=GOLD)
            x2.next_to(qm, DOWN, buff=0.22, aligned_edge=LEFT)   # its own line, apart from the ghost's "?"
            c.wait_until("almost")
            self.play(*appear(x2), run_time=1.0)
            c.wait_until("not quite")
            rt = max(0.5, min(1.2, c.until(None) - 0.25))   # the ring clears before the clip ends
            self.play(FlashAround(x2, run_time=rt, time_width=1.5, color=GOLD), run_time=rt)
            c.wait_until()

        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
