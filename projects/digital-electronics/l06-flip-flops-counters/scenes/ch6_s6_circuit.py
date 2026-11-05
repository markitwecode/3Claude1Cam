"""Chapter 6, scene 6: the synchronous 3-bit counter built (slide p. 100), opened, clocked, run on LEDs,
and compared with ch4's ripple 7 -> 0. Clips c6.circuit.1 – c6.circuit.5.

sync_counter() is the shared picture (s7's inset and s8's recap copy it): three D flip-flops
(ch5_s2's make_ff, scaled K = 0.78; FF0 left) centred x = -5.1, -0.3, 4.75 at y = -0.5; one YELLOW CLK
line from a drop at x = -5.8 (bottom end y = -2.75, "CLK" right of it) along y = -2.29 into every
clock pin (junction dots at FF0 and FF1); GREEN Q risers from each Q pin up to y = 1.45, Q_i labels
(MathTex 40) left of their tops; D0 = BLUE loop from FF0's Q-bar under the box (y = -1.9) to D0;
D1 = XOR (OR shape + back arc) fed by net labels Q0, Q1; D2 = BLUE "combinational logic" block
(1.2 x 2.4) with net-label inputs Q0, Q0', Q1, Q1', Q2, Q2'. Built directly in screen units; spans
x -6.35 … 6.0, y -2.9 … 1.95 (with the block label). led_chain(i) adds the 270 ohm resistor (vertical
zigzag, y 1.45 … 2.05) and the LED (r 0.24 at y 2.45) on top of riser i.
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


# ---- ch5_s2_sync's make_ff (D flip-flop) ------------------------------------------------------
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


# ---- ch1_s2_rslatch's gate drawings (OR / XOR from the NOR shape, no bubble) --------------------
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
    return poly(pts, FG, 4)


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
    S.ffs = [make_ff().scale(K, about_point=ORIGIN).shift(_p(x, FF_Y)) for x in FF_X]
    S.names = [T(f"FF{i}", 28, DIM).move_to(_p(x, FF_Y + BOX_H / 2 * K + 0.25)) for i, x in enumerate(FF_X)]
    S.bus = poly([(DROP_X, DROP_Y), (DROP_X, BUS_Y), (FF_X[2], BUS_Y)], YELLOW)
    S.jdots = [Dot(_p(x, BUS_Y), radius=0.08, color=YELLOW) for x in FF_X[:2]]
    S.clk_l = T("CLK", 34, YELLOW).next_to(_p(DROP_X, DROP_Y - 0.1), RIGHT, buff=0.48)
    S.risers = [Line(_p(x + HX, QY), _p(x + HX, RISE_TOP)).set_stroke(GREEN, 5) for x in FF_X]
    S.q_labels = [MathTex(f"Q_{i}", font_size=40, color=GREEN).next_to(_p(x + HX, 1.05), LEFT, buff=0.15)
                  for i, x in enumerate(FF_X)]
    x0 = FF_X[0]
    S.loop = poly([(x0 + HX, QBY), (x0 + HX, LOOP_Y), (x0 - HX, LOOP_Y), (x0 - HX, QY)], BLUE)
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


def clock_source():
    """The 1 Hz source at the bottom of the CLK drop: circle with a square wave, "1 Hz" (GOLD) under CLK."""
    c = Circle(radius=0.28).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(DROP_X, DROP_Y - 0.28))
    w = 0.13
    wave = poly([(-2 * w, -w), (-w, -w), (-w, w), (w, w), (w, -w), (2 * w, -w)], YELLOW, 3).move_to(c)
    hz = T("1 Hz", 30, GOLD)
    return VGroup(c, wave), hz


# =============================================================================================
# ch4_s5_problems' ripple zoom at the 7 -> 0 edge (copied; replayed here half-size, side by side)
# =============================================================================================
RD_X0, RD_X1 = -5.1, 6.3
RD_P = (RD_X1 - RD_X0) / 8.9
RD_FALL = [RD_X0 + RD_P + k * RD_P for k in range(8)]
RD_D = 0.2
RD_ROW_Y = [2.9, 1.5, 0.1, -1.3]
RD_AMP = 0.3
Z_WIN = (4.85, RD_X1)
Z_SCR = (-4.6, 6.3)
Z_SX = (Z_SCR[1] - Z_SCR[0]) / (Z_WIN[1] - Z_WIN[0])
Z_SY = 0.82
Z_Y0 = 3.2


def zmap(p):
    return np.array([Z_SCR[0] + Z_SX * (p[0] - Z_WIN[0]), Z_Y0 + Z_SY * (p[1] - RD_ROW_Y[0]), p[2]])


Z_E = zmap(_p(RD_FALL[7], 0))[0]
Z_D = Z_SX * RD_D
Z_ROW = [Z_Y0 + Z_SY * (y - RD_ROW_Y[0]) for y in RD_ROW_Y]
Z_AMP = Z_SY * RD_AMP
Z_FALLS = [Z_E + (r + 1) * Z_D for r in range(3)]
Z_P_SLOW = 18.0


def _zy(row, bit):
    return Z_ROW[row] + (Z_AMP if bit else -Z_AMP)


def _zpoly(row, pts, color, width=4):
    return VMobject().set_points_as_corners([_p(x, _zy(row, b)) for x, b in pts]).set_stroke(color, width)


def _zfall(row, x):
    return _zpoly(row, [(Z_SCR[0], 1), (x, 1), (x, 0), (Z_SCR[1], 0)], GREEN)


def zoom_guide(x, color=YELLOW, width=3):
    top, bot = _zy(0, 1) + 0.1, _zy(3, 0) - 0.1
    return Line(_p(x, top), _p(x, bot)).set_stroke(color, width).set_z_index(-2)


def zoom_down(x):
    return (Triangle().rotate(PI).scale(0.16).set_stroke(width=0).set_fill(YELLOW, 1)
            .move_to(_p(x, Z_ROW[0])).set_z_index(1))


def clk_with_period(period):
    h = period / 2
    rise0 = Z_E - h

    def level(x):
        return 1 if (x - rise0) % period < h else 0

    events = []
    for k in range(-3, 12):
        for x in (rise0 + k * period, Z_E + k * period):
            if Z_SCR[0] < x < Z_SCR[1]:
                events.append(x)
    events.sort()
    b = level(Z_SCR[0] + 1e-6)
    pts = [(Z_SCR[0], b)]
    for x in events:
        pts += [(x, b), (x, 1 - b)]
        b = 1 - b
    pts.append((Z_SCR[1], b))
    return _zpoly(0, pts, YELLOW)


class ZoomStair(VGroup):
    """The zoom (labels omitted here: rebuilt at full size beside the half-size traces)."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.clk = clk_with_period(Z_P_SLOW)
        self.guide = zoom_guide(Z_E)
        self.q = [_zfall(r + 1, x) for r, x in enumerate(Z_FALLS)]
        self.add(self.guide, self.clk, *self.q)


READS = [("111", 7, GREEN), ("110", 6, RED), ("100", 4, RED), ("000", 0, GREEN)]


def zoom_cursor(j):
    a, b = Z_E + j * Z_D, Z_E + (j + 1) * Z_D
    top, bot = _zy(0, 1) + 0.18, _zy(3, 0) - 0.3
    return (Rectangle(width=b - a - 0.08, height=top - bot).move_to(_p((a + b) / 2, (top + bot) / 2))
            .set_stroke(YELLOW, 2, opacity=0.7).set_fill(YELLOW, 0.08).set_z_index(-3))


# ---- the split screen: each half shows the zoom at half width -----------------------------------
HALF_X0 = {"L": -5.75, "R": 1.15}          # where Z_SCR[0] lands
HALF_W = 5.25
H_SX = HALF_W / (Z_SCR[1] - Z_SCR[0])
H_ROW0, H_PITCH = 2.15, 1.05
H_SY = H_PITCH / (Z_ROW[0] - Z_ROW[1])


def half_map(side):
    def f(p):
        return np.array([HALF_X0[side] + H_SX * (p[0] - Z_SCR[0]), H_ROW0 + H_SY * (p[1] - Z_ROW[0]), p[2]])
    return f


def half_labels(side):
    texs = [r"\mathrm{CLK}", "Q_0", "Q_1", "Q_2"]
    cols = [YELLOW, GREEN, GREEN, GREEN]
    return [MathTex(t, font_size=34, color=c).move_to(_p(0, H_ROW0 - r * H_PITCH))
            .align_to(_p(HALF_X0[side] - 0.15, 0), RIGHT) for r, (t, c) in enumerate(zip(texs, cols))]


TRAIL_Y = -2.05


def trail_entry(bits, v, col, x):
    b = Mono(bits, 30, col).move_to(_p(x, TRAIL_Y))
    d = T(str(v), 42, col).move_to(_p(x, TRAIL_Y - 0.6))
    return b, d


def trail_arrow(x0, x1, color=DIM):
    y = TRAIL_Y - 0.3
    return Arrow(_p(x0 + 0.42, y), _p(x1 - 0.42, y), buff=0, stroke_width=3, tip_length=0.18,
                 max_tip_length_to_length_ratio=0.4).set_color(color)


def digit(v, color, at):
    d = Mono(str(v), 34, color).move_to(at)
    d.set_opacity(1 if v else 0.45)
    return d


def _bits(n):
    return [(n >> i) & 1 for i in range(3)]      # [Q0, Q1, Q2]


class CounterCircuit(NarratedScene):
    def construct(self):
        self.S = sync_counter()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clock_pulse(self, extra=(), run_time=1.6):
        bus_p, clk_p = self.S.clk_paths()
        self.play(*during([VShowPassingFlash(p, time_width=0.6) for p in bus_p], 0, 0.55),
                  *during([VShowPassingFlash(p, time_width=0.8) for p in clk_p], 0.5, 0.8),
                  *extra, run_time=run_time)

    # ------------------------------------------------------------------ c6.circuit.1
    def clip1(self):
        S = self.S
        with self.say("c6.circuit.1") as c:
            # {ffs}: three D flip-flops
            c.wait_until("ffs")
            self.play(*appear(*S.ffs, lag=0.3, shift=None), run_time=1.3)
            self.play(*[Create(r) for r in S.risers], *during(appear(*S.q_labels, *S.names, lag=0.1), 0.3, 1),  # early: pin names, not spoken
                      run_time=min(1.2, c.until("clk")))
            # {clk}: one clock line, branching up into every clock pin
            c.wait_until("clk")
            self.play(Create(S.bus), run_time=1.5)
            self.play(*[FadeIn(d, scale=0.5) for d in S.jdots], *appear(S.clk_l, shift=None),
                      *[FlashAround(f.tri, color=YELLOW, time_width=1.5, buff=0.08) for f in S.ffs],
                      run_time=1.3)
            # {d0}: FF0's Q-bar wired round to D0
            c.wait_until("d0")
            self.play(VShowPassingFlash(S.ffs[0].qb_w.copy().set_stroke(YELLOW, 10), time_width=0.8), run_time=1.0)
            self.play(Create(S.loop), run_time=1.6)
            # {d1}: XOR fed by Q0 and Q1
            c.wait_until("d1")
            self.play(FadeIn(S.xor), run_time=1.0)
            c.wait_until("cue zero")
            self.play(*[Create(s) for s in S.xor_stubs], *appear(*S.xor_labels, lag=0.4), run_time=1.3)
            self.play(VShowPassingFlash(S.ffs[1].d_w.copy().set_stroke(YELLOW, 10), time_width=0.8),
                      run_time=min(1.0, c.until("d2")))
            # {d2}: the combinational-logic block, fed by every output and its complement
            c.wait_until("d2")
            self.play(FadeIn(S.block), Create(S.block_out), run_time=1.2)
            c.wait_until(own_word=S.block_l[0])
            self.play(*appear(S.block_l), run_time=1.0)
            c.wait_until("fed by", nth=1)
            self.play(*[Create(s) for s in S.block_stubs], *appear(*S.block_labels, shift=None, lag=0.15),
                      run_time=1.8)

    # ------------------------------------------------------------------ c6.circuit.2
    def clip2(self):
        S = self.S
        with self.say("c6.circuit.2") as c:
            # {open}: the block opens into a panel; the rest of the circuit steps back
            self.block_home = S.block.copy()
            others = [m for m in S.all if m is not S.block]
            panel = RoundedRectangle(corner_radius=0.3, width=12.6, height=6.5).set_stroke(BLUE, 4)
            panel.set_fill(BG, 1).move_to(_p(0, -0.1))
            self.panel = panel
            self.play(*during([FadeOut(*others)], 0, 0.45),
                      *during([ReplacementTransform(S.block, panel)], 0.3, 1.0), run_time=1.6)
            expr = MathTex(r"D_2 =", r"Q_2", r".(", r"\overline{Q_0} + \overline{Q_1}", r")", r"+",
                           r"Q_0.Q_1.\overline{Q_2}", font_size=44)
            expr[0].set_color(BLUE)
            expr.move_to(_p(0, 2.45))
            self.expr = expr
            self.play(*appear(expr, shift=None), run_time=min(1.0, c.until("or")))

            # the gate network (screen units, full size)
            g_or1 = or_gate().move_to(_p(-2.4, 1.0))
            g_and = and_gate().move_to(_p(0.3, 0.55))
            g_and3 = and3_gate().move_to(_p(0.3, -1.4))
            g_or2 = or_gate().move_to(_p(2.9, -0.4))
            XL = -4.45

            def lab(t, y):
                return MathTex(t, font_size=40, color=GREEN).next_to(_p(XL, y), LEFT, buff=0.1)

            def chip(t, g, d):
                return T(t, 28, DIM).next_to(g, d, buff=0.12)
            # {or}
            # labels 0.7 apart (Q1-bar's overbar clear of Q0's subscript), jogging into the 0.6-pitch pins
            or_ys = (1.55, 0.85)
            or_in = [lab(r"\overline{Q_0}", or_ys[0]), lab(r"\overline{Q_1}", or_ys[1])]
            or_w = [poly([(XL, y), (-3.4, y), (-3.4, g_or1.inp(j)[1]), g_or1.inp(j)[:2]], GREEN, 4)
                    for j, y in enumerate(or_ys)]
            or_chip = chip("74HC32", g_or1, UP)
            c.wait_until("or")
            box = token_box(expr[3], expr)
            self.play(FadeIn(g_or1), *[Create(w) for w in or_w], *during(appear(*or_in, shift=None, lag=0.3), 0.2, 1),
                      *during([FadeIn(box)], 0.4, 1.0), run_time=1.5)
            self.play(*appear(or_chip, shift=None), *[s.animate.set_stroke(YELLOW) for s in g_or1.strokes()],
                      run_time=1.0)
            # {and}
            and_in = [lab("Q_2", 0.25)]
            and_w = [poly([g_or1.out()[:2], (-1.05, 1.0), (-1.05, 0.85), g_and.inp(0)[:2]], FG, 4),
                     Line(_p(XL, 0.25), g_and.inp(1)).set_stroke(GREEN, 4)]
            and_chip = chip("74HC08", g_and, UP)
            c.wait_until("and")
            self.play(*[s.animate.set_stroke(BLUE) for s in g_or1.strokes()], FadeIn(g_and),
                      *[Create(w) for w in and_w], *during(appear(*and_in), 0.3, 1),
                      Transform(box, token_box(VGroup(*expr[1:5]), expr)), run_time=1.5)
            self.play(*appear(and_chip, shift=None), *[s.animate.set_stroke(YELLOW) for s in g_and.strokes()],
                      run_time=1.0)
            # {three}
            # labels 0.55 apart (Q2-bar's overbar clear of Q1), wires jog into the gate's 0.35-pitch pins
            a3_ys = (-0.85, -1.4, -1.95)
            a3_in = [lab("Q_0", a3_ys[0]), lab("Q_1", a3_ys[1]), lab(r"\overline{Q_2}", a3_ys[2])]
            a3_w = [poly([(XL, y), (-1.0, y), (-1.0, g_and3.inp(j)[1]), g_and3.inp(j)[:2]], GREEN, 4)
                    for j, y in enumerate(a3_ys)]
            a3_chip = chip("74HC11", g_and3, DOWN)
            c.wait_until("three")
            self.play(*[s.animate.set_stroke(BLUE) for s in g_and.strokes()], FadeIn(g_and3),
                      *[Create(w) for w in a3_w], *during(appear(*a3_in, shift=None, lag=0.25), 0.2, 1),
                      Transform(box, token_box(expr[6], expr)), run_time=1.6)
            self.play(*appear(a3_chip, shift=None), *[s.animate.set_stroke(YELLOW) for s in g_and3.strokes()],
                      run_time=1.0)
            # {join}
            j_w = [poly([g_and.out()[:2], (1.6, 0.55), (1.6, -0.1), g_or2.inp(0)[:2]], FG, 4),
                   poly([g_and3.out()[:2], (1.6, -1.4), (1.6, -0.7), g_or2.inp(1)[:2]], FG, 4)]
            out_w = Line(g_or2.out(), _p(4.5, -0.4)).set_stroke(BLUE, 5)
            d2 = MathTex("D_2", font_size=44, color=BLUE).next_to(out_w, RIGHT, buff=0.12)
            or2_chip = chip("74HC32", g_or2, UP)
            c.wait_until("join")
            self.play(*[s.animate.set_stroke(BLUE) for s in g_and3.strokes()], FadeIn(g_or2),
                      *[Create(w) for w in j_w], Transform(box, token_box(VGroup(*expr[1:]), expr)),
                      run_time=1.5)
            self.play(Create(out_w), *during(appear(d2, shift=None), 0.5, 1), *appear(or2_chip, shift=None),
                      *[s.animate.set_stroke(YELLOW) for s in g_or2.strokes()], run_time=1.2)
            # {sim}: the lecturer's Yenka circuit
            c.wait_until("sim")
            tag = T("Yenka circuit “sync_ctr”", 30, DIM).move_to(_p(3.6, -2.55))
            self.play(*[s.animate.set_stroke(BLUE) for s in g_or2.strokes()], FadeOut(box),
                      *during(appear(tag, shift=None), 0.2, 1), run_time=1.2)  # early: names the simulator file
            self.inner = [expr, g_or1, g_and, g_and3, g_or2, *or_in, *or_w, or_chip, *and_in, *and_w, and_chip,
                          *a3_in, *a3_w, a3_chip, *j_w, out_w, d2, or2_chip, tag]

    # ------------------------------------------------------------------ c6.circuit.3
    def clip3(self):
        S = self.S
        with self.say("c6.circuit.3") as c:
            # {sync}: the panel closes back into the block; the clock triangles glow
            others = [m for m in S.all if m is not S.block]
            self.play(*during([FadeOut(*self.inner)], 0, 0.4),
                      *during([ReplacementTransform(self.panel, self.block_home)], 0.3, 0.8),
                      *during([FadeIn(*others)], 0.6, 1.0), run_time=1.4)
            S.all[S.all.index(S.block)] = self.block_home
            S.block = self.block_home
            self.play(*[f.tri.animate.set_stroke(YELLOW, 5) for f in S.ffs], run_time=min(0.9, c.until("together")))
            # {together}: one pulse, all three flash at once
            c.wait_until("connected")
            self.clock_pulse(run_time=1.6)
            c.wait_until("same time")
            self.play(*[FlashAround(f.box, color=YELLOW, time_width=1.5, buff=0.1) for f in S.ffs], run_time=1.2)
            # {settle}: state 011; the gates work out D = 100; the next edge loads it
            c.wait_until("settle")
            q = _bits(3)
            self.qd = [digit(v, GREEN, S.q_spot(i)) for i, v in enumerate(q)]
            self.play(*appear(*self.qd, shift=None, lag=0.1), S.risers[2].animate.set_stroke(opacity=LOW),
                      run_time=1.0)
            d = [1 - q[0], q[0] ^ q[1], (q[2] & (1 - q[0] | 1 - q[1])) | (q[0] & q[1] & (1 - q[2]))]
            self.dd = [digit(v, BLUE, S.d_spot(i)) for i, v in enumerate(d)]
            c.wait_until("work out")
            paths = [S.loop, S.ffs[1].d_w, S.block_out]
            self.play(*[VShowPassingFlash(p.copy().set_stroke(YELLOW, 10), time_width=0.7) for p in paths],
                      *during([S.loop.animate.set_stroke(opacity=LOW), S.ffs[0].d_w.animate.set_stroke(opacity=LOW),
                               S.ffs[1].d_w.animate.set_stroke(opacity=LOW)], 0.3, 0.8),
                      *during(appear(*self.dd, shift=None, lag=0.1), 0.4, 1.0), run_time=1.5)
            c.wait_until("loads")
            # the edge: all three Q's change in the same instant (one swap each, same window)
            nq = d
            newq = [digit(v, GREEN, S.q_spot(i)) for i, v in enumerate(nq)]
            sw = []
            for a, b in zip(self.qd, newq):
                sw += swap(a, b, shift=0.12 * UP)
            self.clock_pulse(extra=[*during(sw, 0.6, 1.0),
                                    *during([S.risers[0].animate.set_stroke(opacity=LOW),
                                             S.risers[1].animate.set_stroke(opacity=LOW),
                                             S.risers[2].animate.set_stroke(opacity=1)], 0.75, 0.9)],
                             run_time=min(1.6, c.until("key")))
            self.qd = newq
            # {key}: and the gates settle again: D = 101 (D0 = not Q0 = 1, D1 = 0, D2 = 1)
            c.wait_until("key")
            nd_v = [1 - nq[0], nq[0] ^ nq[1], (nq[2] & (1 - nq[0] | 1 - nq[1])) | (nq[0] & nq[1] & (1 - nq[2]))]
            newd = [digit(v, BLUE, S.d_spot(i)) for i, v in enumerate(nd_v)]
            sw = []
            for a, b in zip(self.dd, newd):
                sw += swap(a, b, shift=0.12 * UP)
            self.play(*[FlashAround(f.tri, color=YELLOW, time_width=1.5, buff=0.08) for f in S.ffs],
                      VShowPassingFlash(S.loop.copy().set_stroke(YELLOW, 10), time_width=0.7),
                      *during([S.loop.animate.set_stroke(opacity=1), S.ffs[0].d_w.animate.set_stroke(opacity=1)],
                              0.3, 0.7),
                      *during(sw, 0.3, 0.9), run_time=1.5)
            self.dd = newd

    # ------------------------------------------------------------------ c6.circuit.4
    def clip4(self):
        S = self.S
        with self.say("c6.circuit.4") as c:
            # {run}: a 1 Hz source and a light on each output; reset to 000
            src, hz = clock_source()
            hz.next_to(S.clk_l, DOWN, buff=0.18).align_to(S.clk_l, LEFT)
            self.play(*disappear(*self.qd, *self.dd),
                      *[m.animate.set_stroke(opacity=1) for m in (S.loop, S.ffs[0].d_w, S.ffs[1].d_w)],
                      *[f.tri.animate.set_stroke(FG, 3) for f in S.ffs],
                      S.risers[2].animate.set_stroke(opacity=LOW), run_time=1.0)
            self.play(FadeIn(src), *during(appear(hz, shift=None), 0.3, 1), run_time=min(1.2, c.until("light")))
            c.wait_until("light")
            self.chains = [led_chain(i) for i in range(3)]
            self.play(*[Create(ch.res) for ch in self.chains], *[Create(ch.link) for ch in self.chains],
                      *during([FadeIn(ch.led) for ch in self.chains], 0.5, 1.0),
                      *during(appear(*[ch.ohm for ch in self.chains], shift=None, lag=0.15), 0.4, 1.0),
                      run_time=min(1.6, c.until("order")))
            # {order}: LSB on the left light, MSB on the right
            lsb = T("LSB", 30, YELLOW).next_to(self.chains[0].led, LEFT, buff=0.2)
            msb = T("MSB", 30, YELLOW).next_to(self.chains[2].led, LEFT, buff=0.2)
            c.wait_until("least")
            self.play(*appear(lsb), FlashAround(self.chains[0].led, color=YELLOW, time_width=1.5, buff=0.12),
                      run_time=1.2)  # early: LSB is spoken as "least significant bit"
            self.play(*appear(msb), run_time=1.0)  # early: MSB, its opposite end
            # the readout
            self.r_lab = MathTex(r"Q_2\,Q_1\,Q_0", font_size=40, color=GREEN)
            self.r_eq1 = MathTex("=", font_size=40)
            self.r_bits = Mono("000", 44, GREEN)
            self.r_eq2 = MathTex("=", font_size=40)
            self.r_dec = T("0", 48, GOLD)
            row = VGroup(self.r_lab, self.r_eq1, self.r_bits, self.r_eq2, self.r_dec).arrange(RIGHT, buff=0.25)
            row.move_to(_p(0.3, 3.35))
            self.play(*appear(self.r_lab, self.r_eq1, self.r_bits, self.r_eq2, self.r_dec, shift=None, lag=0.1),
                      run_time=min(1.2, c.until("count")))
            # {count}: zero … seven, then back to zero
            c.wait_until("count")
            self.play(*flash([self.r_dec], color=GOLD, time_width=1.5, buff=0.12), run_time=0.6)
            words = [("one", 1), ("two", 0), ("three", 0), ("four", 0), ("five", 0), ("six", 0), ("seven", 0)]
            for n, (w, nth) in enumerate(words, start=1):
                c.wait_until(w, nth=nth)
                self.step_to(n, run_time=0.3)
            c.wait_until("wrap")
            self.step_to(0, run_time=0.9)
            self.play(*flash([self.r_bits, self.r_dec], color=GREEN, time_width=1.5, buff=0.12), run_time=1.0)
            # {lab}: zoom on one resistor and its LED
            c.wait_until("lab")
            ch = self.chains[0]
            keep = [ch.res, ch.link, ch.led]
            gone = [m for m in self.mobjects if m not in keep]
            pivot = VGroup(*keep).get_center()
            for m in keep:
                m.generate_target()
                m.target.scale(2.2, about_point=pivot).shift(_p(0, 0.1) - pivot)
            self.play(*during(disappear(*gone), 0, 0.45), *during([MoveToTarget(m) for m in keep], 0.35, 1.0),
                      run_time=1.6)
            big_ohm = T("270 Ω", 40, FG).next_to(ch.res, LEFT, buff=0.35)
            big_led = T("LED", 40, GREEN).next_to(ch.led, RIGHT, buff=0.35)
            self.play(*appear(big_ohm, shift=None), set_led(ch.led, True), *during(appear(big_led, shift=None), 0.3, 1),
                      run_time=min(1.2, c.until("resistor") - 0.1))  # early: the resistor's value, named just after
            c.wait_until("resistor")
            self.play(FlashAround(VGroup(ch.res, big_ohm), color=YELLOW, time_width=1.5, buff=0.15), run_time=1.5)
            c.wait_until("burning")
            path = poly([(0, ch.res.get_bottom()[1]), (0, ch.led.get_top()[1])], YELLOW, 8)
            self.play(VShowPassingFlash(path, time_width=0.6), run_time=min(1.2, c.until(floor=0.5)))

    def step_to(self, n, run_time):
        """A real counter changes instantly: bits, decimal, LEDs and output wires all switch in one
        frame on the word (no cross-fade); a clock pulse then runs along the line during the hold."""
        S = self.S
        b = _bits(n)
        nb = Mono(f"{n:03b}", 44, GREEN).move_to(self.r_bits)
        nd = T(str(n), 48, GOLD).move_to(self.r_dec)
        self.remove(self.r_bits, self.r_dec)
        self.add(nb, nd)
        for ch, v in zip(self.chains, b):
            ch.led.on = bool(v)
            if v:
                ch.led.set_stroke(GREEN, 3).set_fill(GREEN, 0.9)
            else:
                ch.led.set_stroke(DIM, 3).set_fill(BG, 0)
        for r, v in zip(S.risers, b):
            r.set_stroke(opacity=1 if v else LOW)
        self.r_bits, self.r_dec = nb, nd
        bus_p, _ = S.clk_paths()
        self.play(VShowPassingFlash(bus_p[0], time_width=0.8), run_time=run_time)

    # ------------------------------------------------------------------ c6.circuit.5
    def clip5(self):
        with self.say("c6.circuit.5") as c:
            # {compare}: split screen
            div = Line(_p(0.15, 3.6), _p(0.15, -3.4)).set_stroke(DIM, 2)
            sweep_clear(self, time_span(GrowFromCenter(div), 0.6, 1.2), run_time=1.2)
            # {ripple}: left, ch4's ripple zoom at the 7 -> 0 edge
            fL = half_map("L")
            z = ZoomStair()
            for m in z.submobjects:
                m.apply_function(fL)
            down = zoom_down(Z_E).move_to(fL(_p(Z_E, Z_ROW[0])))
            labsL = half_labels("L")
            titleL = T("ripple counter", 40, RED).move_to(_p(-3.2, 3.35))
            c.wait_until(own_word=titleL)
            self.play(*appear(titleL, shift=None), *[FadeIn(m) for m in (z.clk, *z.q)],
                      *during(appear(*labsL, shift=None, lag=0.1), 0.2, 1), run_time=1.3)
            self.play(Create(z.guide), GrowFromCenter(down), run_time=min(0.8, c.until("stagger")))
            # {stagger}: 7 -> 6 -> 4 -> 0, the cursor walking the staircase
            xs = [-5.4, -3.85, -2.3, -0.75]
            entries = [trail_entry(bits, v, col, x) for (bits, v, col), x in zip(READS, xs)]
            arrows = [trail_arrow(xs[j], xs[j + 1]) for j in range(3)]
            cur = zoom_cursor(0).apply_function(fL)
            c.wait_until("stagger")
            self.play(FadeIn(cur), *during(appear(*entries[0], shift=None), 0.3, 1), run_time=0.8)
            for j, (w, nth) in enumerate((("six", 0), ("four", 0), ("zero", 1)), start=1):
                c.wait_until(w, nth=nth)
                self.play(Transform(cur, zoom_cursor(j).apply_function(fL)), GrowArrow(arrows[j - 1]),
                          *during(appear(*entries[j], shift=None), 0.3, 1), run_time=min(0.7, c.until("same")))
            self.play(FadeOut(cur), *flash([VGroup(*entries[1]), VGroup(*entries[2])], color=RED, time_width=1.5, buff=0.12),
                      run_time=min(1.2, c.until("same")))
            # {same}: right, our three Q traces fall on one edge
            fR = half_map("R")
            xf = Z_E + 0.5 * Z_D
            clkR = _zpoly(0, [(Z_SCR[0], 0), (Z_E, 0), (Z_E, 1), (Z_SCR[1], 1)], YELLOW).apply_function(fR)
            qR = [_zfall(r + 1, xf).apply_function(fR) for r in range(3)]
            guideR = Line(_p(xf, _zy(1, 1) + 0.15), _p(xf, _zy(3, 0) - 0.15)).apply_function(fR)
            guideR.set_stroke(YELLOW, 4)
            labsR = half_labels("R")
            titleR = T("synchronous counter", 40, GREEN).move_to(_p(3.75, 3.35))
            c.wait_until("same")
            self.play(*appear(titleR, shift=None), FadeIn(clkR), *[FadeIn(q) for q in qR],
                      *during(appear(*labsR, shift=None, lag=0.1), 0.2, 1), run_time=1.3)  # early: names the side
            self.play(GrowFromCenter(guideR), run_time=1.0)
            self.play(VShowPassingFlash(guideR.copy().set_stroke(YELLOW, 10), time_width=0.8), run_time=1.0)
            # {clean}: 7 -> 0, nothing in between
            xr = [2.55, 4.95]
            eR = [trail_entry("111", 7, GREEN, xr[0]), trail_entry("000", 0, GREEN, xr[1])]
            aR = trail_arrow(xr[0], xr[1], GREEN)
            c.wait_until("clean")
            self.play(*appear(*eR[0], shift=None), run_time=0.8)
            c.wait_until("zero", nth=2)
            self.play(GrowArrow(aR), *during(appear(*eR[1], shift=None), 0.3, 1), run_time=min(1.0, c.until(floor=0.5)))
            c.wait_until()
            self.wait(0.6)
