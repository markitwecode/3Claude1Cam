"""Chapter 6, scene 7: why it counts: the carry pattern. Clips c6.carry.1 – c6.carry.3.

Helpers copied: make_ff / ripple_circuit / count_column geometry (ch4_s3_ripple.py), xor_formula
(ch3_s5_t.py), sync_counter (ch6_s6_circuit.py).
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


def poly(pts, color, width=4):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# ---- ch4_s3_ripple's make_ff / ripple_circuit ---------------------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), q_len=WIRE, bubble=False):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + q_len, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    top_clk = -hb - (0.22 if bubble else 0.02)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, top_clk)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, 36, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    parts = [*in_w, q_w, qb_w, clk_w, box, tri]
    bub = None
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.11))
        parts.append(bub)
    g = VGroup(*parts, *in_l, q_l, qb_l)
    g.box, g.tri, g.bub, g.clk_w, g.q_w, g.qb_w, g.in_w = box, tri, bub, clk_w, q_w, qb_w, in_w
    g.labels = [*in_l, q_l, qb_l]
    g.shift(center)
    return g


CH_X = (-4.3, 0.0, 4.3)
STUB_Y = 1.75
FEED_Y = -BOX_H / 2 - EN_WIRE


def ripple_circuit(k=0.85, center=_p(0, 0.85)):
    ffs = [make_ff(_p(x, 0), ins=(("T", PIN_Y),), bubble=True) for x in CH_X]
    ones = [MathTex("1", font_size=44, color=BLUE).next_to(f.in_w[0].get_start(), LEFT, buff=0.12)
            for f in ffs]
    feeds, stubs, dots, q_labels = [], [], [], []
    for i, x in enumerate(CH_X):
        jx = x + BOX_W / 2 + WIRE + 0.4
        stubs.append(poly([(x + BOX_W / 2 + WIRE, PIN_Y), (jx, PIN_Y), (jx, STUB_Y)], GREEN, 5))
        q_labels.append(MathTex(f"Q_{i}", font_size=44, color=GREEN).next_to(_p(jx, STUB_Y), UP, buff=0.1))
        if i < 2:
            ffs[i + 1].clk_w.set_stroke(GREEN)
            feeds.append(poly([(jx, PIN_Y), (jx, FEED_Y), (CH_X[i + 1], FEED_Y)], GREEN, 5))
            dots.append(Dot(_p(jx, PIN_Y), radius=0.09, color=GREEN))
    clk_l = T("CLK", 36, YELLOW).next_to(ffs[0].clk_w.get_start(), DOWN, buff=0.12)
    g = VGroup(*ffs, *ones, *stubs, *feeds, *dots, *q_labels)
    for m in (g, clk_l):
        m.scale(k, about_point=ORIGIN).shift(center)
    g.ffs, g.ones, g.feeds, g.stubs, g.dots, g.q_labels, g.clk_l = ffs, ones, feeds, stubs, dots, q_labels, clk_l

    def glow_path(i):
        f, n = ffs[i], ffs[i + 1]
        pts = [f.q_w.get_start(), stubs[i].get_points()[3], *[feeds[i].get_points()[j] for j in (3, 7)],
               n.clk_w.get_end()]
        return VMobject().set_points_as_corners(pts).set_stroke(GREEN, 8)
    g.glow_path = glow_path
    return g


# ---- ch3_s5_t's xor_formula ---------------------------------------------------------------------
def xor_formula(size=84):
    """Q' = T xor Q (Q', Q GREEN; T BLUE). Parts [0] Q' [1] = [2] T [3] xor [4] Q."""
    f = MathTex("Q'", "=", "T", r"\oplus", "Q", font_size=size)
    f[0].set_color(GREEN)
    f[2].set_color(BLUE)
    f[4].set_color(GREEN)
    return f


# ---- ch4_s3_ripple's counting column (rows 000..111) ------------------------------------------
ROW_X = -4.6
DEC_X = -6.35
HEAD_Y = 3.3
ROW_Y0, ROW_P = 2.55, 0.66


def row_y(r):
    return ROW_Y0 - r * ROW_P


def count_column(values=range(8)):
    head = [MathTex(f"Q_{b}", font_size=44, color=GREEN) for b in (2, 1, 0)]
    rows, decs = [], []
    for r, v in enumerate(values):
        rows.append(Mono(" ".join(format(v, "03b")), size=44, color=GREEN).move_to(_p(ROW_X, row_y(r))))
        decs.append(T(str(v), 38, GOLD).move_to(_p(DEC_X, row_y(r))))
    for h, i in zip(head, [0, 1, 2]):
        h.move_to(_p(rows[0][i].get_x(), HEAD_Y))
    return head, rows, decs


# ---- s6's synchronous counter (ch6_s6_circuit.py) -----------------------------------------------
def poly5(pts, color, width=5):
    return poly(pts, color, width)


def make_dff(center=ORIGIN, bubble=False, d_text="D"):
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




GATE_COLOR = BLUE


class Gate(VGroup):
    def __init__(self, body, ins, out, extra=None, color=GATE_COLOR):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body = body
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body)
        self.extra = extra
        if extra is not None:
            extra.set_stroke(color, 4).set_fill(opacity=0)
            self.add(extra)
        self.add(*self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()

    def strokes(self):
        return [m for m in (self.body, self.extra) if m is not None]


def _or_body():
    x0 = -0.7
    b = VMobject()
    b.start_new_path(_p(x0, 0.6))
    b.add_cubic_bezier_curve_to(_p(0.0, 0.6), _p(0.45, 0.35), _p(0.7, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.45, -0.35), _p(0.0, -0.6), _p(x0, -0.6))
    b.add_cubic_bezier_curve_to(_p(x0 + 0.25, -0.2), _p(x0 + 0.25, 0.2), _p(x0, 0.6))
    return b


def or_gate(color=GATE_COLOR):
    """OR: the NOR body without its bubble, 1.4 x 1.2. inp(0) (-0.56, 0.3), inp(1) (-0.56, -0.3), out() (0.7, 0)."""
    return Gate(_or_body(), [(-0.56, 0.3), (-0.56, -0.3)], (0.7, 0.0), color=color)


def xor_gate(color=GATE_COLOR):
    """XOR: OR plus a back arc 0.15 behind it. inp(i) on the back arc (-0.71, +-0.3), out() (0.7, 0)."""
    arc = VMobject()
    arc.start_new_path(_p(-0.85, 0.6))
    arc.add_cubic_bezier_curve_to(_p(-0.6, 0.2), _p(-0.6, -0.2), _p(-0.85, -0.6))
    return Gate(_or_body(), [(-0.71, 0.3), (-0.71, -0.3)], (0.7, 0.0), extra=arc, color=color)


def _and_body():
    k = 0.5523 * 0.6
    b = VMobject()
    b.start_new_path(_p(-0.7, 0.6))
    b.add_line_to(_p(0.0, 0.6))
    b.add_cubic_bezier_curve_to(_p(k, 0.6), _p(0.6, k), _p(0.6, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.6, -k), _p(k, -0.6), _p(0.0, -0.6))
    b.add_line_to(_p(-0.7, -0.6))
    b.add_line_to(_p(-0.7, 0.6))
    return b


def and_gate(color=GATE_COLOR):
    """AND, 1.3 x 1.2. inp(0) (-0.7, 0.3), inp(1) (-0.7, -0.3), out() (0.6, 0)."""
    return Gate(_and_body(), [(-0.7, 0.3), (-0.7, -0.3)], (0.6, 0.0), color=color)


def and3_gate(color=GATE_COLOR):
    """Three-input AND: inputs (-0.7, 0.35), (-0.7, 0), (-0.7, -0.35)."""
    return Gate(_and_body(), [(-0.7, 0.35), (-0.7, 0.0), (-0.7, -0.35)], (0.6, 0.0), color=color)


# ---- ch2_s6_symbols' LED (off reads as off: hollow DIM ring) -----------------------------------
LED_R = 0.24


def led(on):
    c = Circle(radius=LED_R)
    if on:
        c.set_stroke(GREEN, 3).set_fill(GREEN, 0.9)
    else:
        c.set_stroke(DIM, 3).set_fill(BG, 0)
    c.on = on
    return c


def set_led(l, on):
    l.on = on
    if on:
        return l.animate.set_stroke(GREEN, 3).set_fill(GREEN, 0.9)
    return l.animate.set_stroke(DIM, 3).set_fill(BG, 0)


# =============================================================================================
# THE synchronous counter (slide p. 100). s7 / s8 copy this block for their insets.
# =============================================================================================
K = 0.78                                   # flip-flop scale
FF_X = (-5.1, -0.3, 4.75)
FF_Y = -0.5
HX = (BOX_W / 2 + WIRE) * K                # box centre to the end of a pin wire (1.248)
QY = FF_Y + PIN_Y * K                      # Q and D pin row (-0.03)
QBY = FF_Y - PIN_Y * K                     # Q-bar pin row (-0.97)
BUS_Y = FF_Y - (BOX_H / 2 + EN_WIRE) * K   # the CLK line (-2.29)
LOOP_Y = -1.9                              # FF0's Q-bar -> D0 loop, under the box
DROP_X, DROP_Y = -5.8, -2.75               # CLK comes in here
RISE_TOP = 1.45
LED_Y = 2.45
LOW = 0.25                                 # a wire at 0 keeps its colour at this opacity


def zigzag(x, y0, y1, n=6, amp=0.13):
    lead = 0.1
    pts = [(x, y0), (x, y0 + lead)]
    h = (y1 - y0 - 2 * lead) / n
    for j in range(n):
        pts.append((x + (amp if j % 2 == 0 else -amp), y0 + lead + (j + 0.5) * h))
    pts += [(x, y1 - lead), (x, y1)]
    return poly5(pts, FG, 4)


def led_chain(i, on=False):
    """Resistor + LED on top of riser i: VGroup(res, link, led) with .res .link .led .ohm (label, not in group)."""
    x = FF_X[i] + HX
    res = zigzag(x, RISE_TOP, 2.05)
    link = Line(_p(x, 2.05), _p(x, LED_Y - LED_R)).set_stroke(FG, 4)
    lamp = led(on).move_to(_p(x, LED_Y))
    ohm = T("270 Ω", 28, FG).next_to(_p(x - 0.13, 1.75), LEFT, buff=0.12)
    g = VGroup(res, link, lamp)
    g.res, g.link, g.led, g.ohm = res, link, lamp, ohm
    return g


def sync_counter():
    """Parts (each a separate mobject; .all lists them): .ffs .names .bus (polyline from the drop) .jdots
    .clk_l .risers .q_labels .loop (D0) .xor .xor_stubs .xor_labels .block .block_l .block_out
    .block_stubs .block_labels; .q_spot(i) / .d_spot(i): where a value digit sits above Q_i's / D_i's
    pin wire; .clk_paths(): fresh YELLOW paths (bus, then the clock pins) for a pulse."""
    S = VGroup()
    S.ffs = [make_dff().scale(K, about_point=ORIGIN).shift(_p(x, FF_Y)) for x in FF_X]
    S.names = [T(f"FF{i}", 28, DIM).move_to(_p(x, FF_Y + BOX_H / 2 * K + 0.25)) for i, x in enumerate(FF_X)]
    S.bus = poly5([(DROP_X, DROP_Y), (DROP_X, BUS_Y), (FF_X[2], BUS_Y)], YELLOW)
    S.jdots = [Dot(_p(x, BUS_Y), radius=0.08, color=YELLOW) for x in FF_X[:2]]
    S.clk_l = T("CLK", 34, YELLOW).next_to(_p(DROP_X, DROP_Y), RIGHT, buff=0.3)
    S.risers = [Line(_p(x + HX, QY), _p(x + HX, RISE_TOP)).set_stroke(GREEN, 5) for x in FF_X]
    S.q_labels = [MathTex(f"Q_{i}", font_size=40, color=GREEN).next_to(_p(x + HX, 1.05), LEFT, buff=0.15)
                  for i, x in enumerate(FF_X)]
    x0 = FF_X[0]
    S.loop = poly5([(x0 + HX, QBY), (x0 + HX, LOOP_Y), (x0 - HX, LOOP_Y), (x0 - HX, QY)], BLUE)
    # D1: XOR right against D1's pin wire
    xg = xor_gate().scale(K)
    xg.shift(_p(FF_X[1] - HX, QY) - xg.out())
    S.xor = xg
    S.xor_stubs, S.xor_labels = [], []
    for j in range(2):
        a = xg.inp(j)
        st = Line(a + 0.35 * LEFT, a).set_stroke(GREEN, 4)
        S.xor_stubs.append(st)
        S.xor_labels.append(MathTex(f"Q_{j}", font_size=36, color=GREEN).next_to(st, LEFT, buff=0.08))
    # D2: the combinational-logic block
    x2 = FF_X[2]
    bx1 = x2 - HX - 0.3
    S.block = Rectangle(width=1.2, height=2.4).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(bx1 - 0.6, QY))
    S.block_out = Line(_p(bx1, QY), _p(x2 - HX, QY)).set_stroke(BLUE, 5)
    S.block_l = VGroup(T("combinational", 28, BLUE), T("logic", 28, BLUE)).arrange(DOWN, buff=0.08)
    S.block_l.next_to(S.block, UP, buff=0.15)
    texs = ["Q_0", r"\overline{Q_0}", "Q_1", r"\overline{Q_1}", "Q_2", r"\overline{Q_2}"]
    S.block_stubs, S.block_labels = [], []
    for j, t in enumerate(texs):
        y = QY + 1.0 - 0.4 * j
        st = Line(_p(bx1 - 1.2 - 0.25, y), _p(bx1 - 1.2, y)).set_stroke(GREEN, 4)
        S.block_stubs.append(st)
        S.block_labels.append(MathTex(t, font_size=32, color=GREEN).next_to(st, LEFT, buff=0.08))
    S.all = [*S.ffs, *S.names, S.bus, *S.jdots, S.clk_l, *S.risers, *S.q_labels, S.loop, xg,
             *S.xor_stubs, *S.xor_labels, S.block, S.block_out, S.block_l, *S.block_stubs, *S.block_labels]
    S.add(*S.all)
    S.q_spot = lambda i: _p(FF_X[i] + 0.92, QY + 0.3)
    S.d_spot = lambda i: _p(FF_X[i] - 0.92, QY + 0.3)

    def clk_paths():
        return ([S.bus.copy().set_stroke(YELLOW, 10)],
                [f.clk_w.copy().set_stroke(YELLOW, 10) for f in S.ffs])
    S.clk_paths = clk_paths
    return S



# ---- this scene ---------------------------------------------------------------------------------
EQ_SIZE = 64
OPL_X = -2.2                     # the ladder's ⊕ column
LAD_Y = (2.6, 0.85, -0.9)
RULE_Y = -3.05


def ladder_line(k, rhs, y, size=EQ_SIZE):
    """D_k = Q_k ⊕ rhs: D FG, Q GREEN, rhs BLUE; the ⊕ at (OPL_X, y). Parts [0] D [1] = [2] Q [3] ⊕ [4] rhs."""
    m = MathTex(f"D_{k}", "=", f"Q_{k}", r"\oplus", rhs, font_size=size)
    m[2].set_color(GREEN)
    m[4].set_color(BLUE)
    m.shift(_p(OPL_X, y) - m[3].get_center())
    return m


class Carry(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c6.carry.1
    def clip1(self):
        with self.say("c6.carry.1") as c:
            # {why}: s5's second line, fresh
            # s5's second line and its colouring (ch6_s5_groups.py E2 / line2)
            eq = MathTex("D_2", "=", "Q_2", ".", "(", r"\overline{Q_0}", "+", r"\overline{Q_1}", ")", "+",
                         r"Q_0.Q_1.\overline{Q_2}", font_size=EQ_SIZE)
            eq[2].set_color(YELLOW)
            eq[5].set_color(PURPLE)
            eq[7].set_color(TEAL)
            eq[10].set_color(PINK)
            eq.move_to(_p(0, 1.3))
            self.play(*appear(eq, shift=None), run_time=1.2)
            # "dee two": a short colour pulse on D2 itself (BLUE, so it isn't read as the YELLOW Q2)
            c.wait_until("dee two")
            d2 = eq[0]

            d2_rest = d2.copy()

            def pulse(m, a):
                b = there_and_back(a)
                m.become(d2_rest.copy().scale(1 + 0.18 * b))
                m.set_color(interpolate_color(ManimColor(FG), ManimColor(BLUE), b))
            self.play(UpdateFromAlphaFunc(d2, pulse), run_time=1.8)
            demo = VGroup(eq[5], eq[6], eq[7])

            # {demorgan}: the two complements become one
            c.wait_until("demorgan")
            eq2 = MathTex("D_2", "=", "Q_2", ".", "(", r"\overline{Q_0.Q_1}", ")", "+",
                          r"Q_0.Q_1.\overline{Q_2}", font_size=EQ_SIZE)
            eq2[2].set_color(YELLOW)
            eq2[8].set_color(PINK)
            eq2.move_to(eq)
            tag = T("De Morgan", 34, YELLOW).next_to(eq2[5], DOWN, buff=0.3)
            self.play(*appear(tag), FlashAround(demo, time_width=1.5, buff=0.1), run_time=1.2)
            c.wait_until("complement")
            self.play(*edit(eq, eq2), run_time=1.6)

            # {swap}: copy / flip table
            c.wait_until("swap")
            xs = (-3.3, -0.95, 0.0, 3.9)

            def row(bit, res, word, col, y):
                cond = MathTex(rf"Q_1.Q_0 = {bit}", font_size=56).move_to(_p(xs[0], y))
                arr = MathTex(r"\Rightarrow", font_size=56, color=DIM).move_to(_p(xs[1], y))
                r = MathTex(r"D_2 = ", res, font_size=56)
                r[1].set_color(YELLOW)
                r.move_to(_p(xs[2], y), aligned_edge=LEFT).set_y(y)
                w = T(word, 42, col).move_to(_p(xs[3], y))
                return VGroup(cond, arr, r, w)

            r0 = row(0, "Q_2", "copy", TEAL, -0.75)
            r1 = row(1, r"\overline{Q_2}", "flip", YELLOW, -2.0)
            self.play(*set_alpha([eq2[8]], 0.4), FlashAround(eq2[5], time_width=1.5, buff=0.1),
                      run_time=1.2)
            c.wait_until("copies")
            self.play(*appear(r0, lag=0.3), run_time=1.5)
            c.wait_until("flips")
            self.play(*appear(r1, lag=0.3), run_time=1.5)

            # {xor}: the line collapses
            c.wait_until("xor")
            eq3 = MathTex("D_2", "=", "Q_2", r"\oplus", "Q_1.Q_0", font_size=EQ_SIZE)
            eq3[2].set_color(YELLOW)
            eq3.move_to(eq2)
            # clean handover (no glyph matching): the bracket, the bar and the PINK term fade where they
            # are, "D_2 = Q_2" slides to its new place, then "⊕ Q_1.Q_0" fades in
            self.play(*during([FadeOut(eq2[i]) for i in range(3, 9)] + disappear(tag), 0, 0.4),
                      *during([eq2[i].animate.move_to(eq3[i]) for i in range(3)], 0.35, 0.75),
                      *during(appear(eq3[3], eq3[4], shift=None, lag=0.15), 0.7, 1), run_time=1.8)
            self.remove(*eq2.get_family())
            self.add(eq3)
            c.wait_until("dee two equals")
            self.play(FlashAround(eq3, time_width=1.5, buff=0.15), run_time=1.5)
        self.eq3, self.table = eq3, VGroup(r0, r1)

    # ------------------------------------------------------------------ c6.carry.2
    def clip2(self):
        eq3 = self.eq3
        with self.say("c6.carry.2") as c:
            # {ladder}: the D2 line drops to the bottom rung
            l2 = ladder_line(2, "Q_1.Q_0", LAD_Y[2])
            l2[4].set_color(FG)
            l2[2].set_color(GREEN)
            self.play(*disappear(*self.table), run_time=0.8)
            self.play(*edit(eq3, l2), run_time=1.2)
            l0 = ladder_line(0, "1", LAD_Y[0])
            l1 = ladder_line(1, "Q_0", LAD_Y[1])
            c.wait_until("l0")
            self.play(*appear(l0), run_time=1.2)
            c.wait_until("l1")
            self.play(*appear(l1), run_time=1.2)
            c.wait_until("l2")
            self.play(*recolor([l2[4]], BLUE), FlashAround(l2, time_width=1.5, buff=0.12), run_time=1.5)

            # {tee}: part three's rule, and the T each line feeds
            c.wait_until("tee")
            f = xor_formula(size=76).move_to(_p(4.3, LAD_Y[1]))
            self.play(*appear(f, shift=None), run_time=1.2)  # early: the T rule is read in this sentence
            braces, tl = [], []
            for k, (l, rhs) in enumerate(zip((l0, l1, l2), ("1", "Q_0", "Q_1.Q_0"))):
                b = Brace(l[4], DOWN, buff=0.1, color=BLUE)
                t = MathTex(f"T_{k} = {rhs}", font_size=46, color=BLUE).next_to(b, DOWN, buff=0.08)
                braces.append(b)
                tl.append(t)
            c.wait_until("tee ex-or")
            self.play(*[GrowFromCenter(b) for b in braces],
                      *appear(*tl, lag=0.3), FlashAround(f[2], time_width=1.5), run_time=1.8)  # early: T labels named by the rule

            # {rule}
            rule = T("a bit toggles when all the bits below it are 1", 38, YELLOW).move_to(_p(0, RULE_Y))
            c.wait_until("rule")
            self.play(*appear(rule), run_time=1.2)
        self.rule = rule

    # ------------------------------------------------------------------ c6.carry.3
    def clip3(self):
        rule = self.rule
        with self.say("c6.carry.3", gap=2.0) as c:
            # {binary}: the counting column, flipped bits YELLOW
            head, rows, decs = count_column()
            sweep_clear(self, rule.animate.scale(0.9).move_to(_p(0, -3.45)),
                        *appear(*head, *rows, *decs, shift=None, lag=0.03), keep=[rule], run_time=1.6)
            flips = []
            for r in range(1, 8):
                a, b = format(r - 1, "03b"), format(r, "03b")
                flips += [rows[r][i] for i in range(3) if a[i] != b[i]]
            self.play(*recolor(flips, YELLOW), run_time=1.2)

            # {carry}: zoom on 011 -> 100
            c.wait_until("carry")
            big3 = Mono("0 1 1", size=88, color=GREEN).move_to(_p(2.4, 1.5))
            big4 = Mono("1 0 0", size=88, color=GREEN).move_to(_p(2.4, -1.0))
            d3 = T("3", 64, GOLD).move_to(_p(5.2, 1.5))
            d4 = T("4", 64, GOLD).move_to(_p(5.2, -1.0))
            zbox = SurroundingRectangle(VGroup(rows[3], rows[4], decs[3]), color=YELLOW, buff=0.12,
                                        stroke_width=3)
            self.play(FadeIn(zbox), *appear(big3, d3, big4, d4, shift=0.3 * RIGHT, lag=0.2),
                      run_time=min(1.6, c.until("two low")))
            c.wait_until("two low")
            self.play(*recolor([big3[1], big3[2]], YELLOW), *flash([big3[1], big3[2]]), run_time=1.5)
            c.wait_until("all three")
            ay = 0.25
            arrow = Arrow(_p(big3[2].get_x() + 0.35, ay), _p(big3[0].get_x() - 0.35, ay), buff=0,
                          color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.12)
            carry = T("carry", 40, YELLOW).next_to(arrow, LEFT, buff=0.3)
            self.play(GrowArrow(arrow), *recolor(list(big4), YELLOW),
                      *during(appear(carry, shift=0.2 * LEFT), 0.55, 1), run_time=1.8)  # early: names the arrow as it lands; said a beat later

            # {ripple}: ch4's ripple counter, one stage at a time
            c.wait_until("counter")
            rc = ripple_circuit(k=0.72, center=_p(-0.2, 0.2))
            for m in [*rc.q_labels, *rc.ones, rc.clk_l, *[l for f in rc.ffs for l in f.labels]]:
                m.scale(1.15)
            rc.clk_l.next_to(rc.ffs[0].clk_w.get_start(), DOWN, buff=0.08)
            rlab = T("part 4: ripple", 34, DIM).to_corner(UL, buff=0.6)
            bits = [Mono(b, size=36, color=GREEN).next_to(q, RIGHT, buff=0.12) for q, b in
                    zip(rc.q_labels, "110")]
            sweep_clear(self, *appear(rc, rc.clk_l, rlab, *bits, shift=None, lag=0), run_time=1.0)
            new = [Mono(b, size=36, color=YELLOW).move_to(o) for o, b in zip(bits, "001")]
            steps = []
            for i in range(3):
                steps.append(AnimationGroup(*swap(bits[i], new[i]), FlashAround(rc.ffs[i].box, buff=0.06)))
                if i < 2:
                    steps.append(VShowPassingFlash(rc.glow_path(i), time_width=0.6))
            self.play(Succession(*steps), run_time=max(1.8, min(3.0, c.until("here") - 1.0)))

            # {here}: our circuit, every flip on one edge
            c.wait_until("here")
            self.here(c, new)

            # {four}: a fourth bit
            c.wait_until("four")
            lys = (2.5, 1.1, -0.3, -1.7)
            ls = [ladder_line(k, rhs, y, size=68) for k, (rhs, y) in
                  enumerate(zip(("1", "Q_0", "Q_1.Q_0"), lys))]
            l3 = ladder_line(3, "Q_2.Q_1.Q_0", lys[3], size=68)
            dx = -VGroup(*ls, l3).get_center()[0]          # the full 4-line ladder centred on screen
            for l in (*ls, l3):
                l.shift(dx * RIGHT)
            # the circuit and every value digit leave together, then the ladder returns
            self.play(*during([FadeOut(m) for m in list(self.mobjects)], 0, 0.45),
                      *during(appear(*ls, shift=None, lag=0.1), 0.5, 1), run_time=1.6)
            c.wait_until("d3")
            self.play(*appear(l3, shift=0.6 * DOWN), run_time=1.6)
            c.wait_until("ex-or cue two")
            self.play(FlashAround(l3[4], time_width=1.5, buff=0.1), run_time=1.5)

    def here(self, c, ripple_bits):
        """s6's circuit: the gates settle every D first, then one edge moves all three Q's."""
        k, ctr = 0.86, _p(0.05, 0.35)
        S = sync_counter()
        S.scale(k, about_point=ORIGIN).shift(ctr)
        for m in [*S.names, S.clk_l, *S.q_labels, *S.xor_labels, *S.block_labels,
                  *[l for f in S.ffs for l in (f.d_l, f.q_l, f.qb_l)]]:
            m.scale(1.15)
        S.block_l.scale(1.15).next_to(S.block, UP, buff=0.12)

        def spot(p):
            return p * k + ctr

        lab = T("ours: synchronous", 34, DIM).to_corner(UL, buff=0.6)
        qd = [Mono(b, size=36, color=GREEN).move_to(spot(S.q_spot(i))) for i, b in enumerate("110")]
        # the ripple inset (and its Q labels / digits) is gone before ours arrives: no doubled Q2
        self.play(*during([FadeOut(m) for m in list(self.mobjects)], 0, 0.45),
                  *during(appear(S, lab, *qd, shift=None, lag=0), 0.5, 1), run_time=1.4)

        # the gates work out every flip, before the edge
        c.wait_until("gates")
        dd = [Mono(b, size=36, color=YELLOW).move_to(spot(S.d_spot(i))) for i, b in enumerate("001")]
        self.play(VShowPassingFlash(S.loop.copy().set_stroke(YELLOW, 9), time_width=0.6),
                  FlashAround(S.xor, time_width=1.5, buff=0.08), FlashAround(S.block, time_width=1.5, buff=0.08),
                  *during(appear(*dd, shift=0.15 * RIGHT, lag=0.15), 0.4, 1), run_time=1.8)

        # one edge: every flip-flop moves at once
        c.wait_until("every flip-flop")
        bus_p, clk_p = S.clk_paths()
        new = [Mono(b, size=36, color=YELLOW).move_to(o) for o, b in zip(qd, "001")]
        self.play(Succession(VShowPassingFlash(bus_p[0], time_width=0.6, run_time=0.8),
                             AnimationGroup(*[VShowPassingFlash(p, time_width=0.8) for p in clk_p],
                                            *[FlashAround(f.box, buff=0.06) for f in S.ffs], run_time=0.8)),
                  *during([a for o, n in zip(qd, new) for a in swap(o, n)], 0.5, 1), run_time=1.6)
