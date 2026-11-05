"""Chapter 2, scene 4: the sliding counter as a circuit: one AND gate, two plain wires; two rounds
of clock edges with the GOLD 1s sliding a -> b -> c; the output waveform; the scoreboard gains
the sliding row. Clips c2.circ.1 – c2.circ.3.

Helpers owned here (s6, s7, s8 copy them verbatim, with s1's make_ff/and_gate/bar_label parts):
- sliding_circuit(): three D flip-flops a b c left to right (s1's make_ff, size 42), YELLOW CLK
  bus from a 1 Hz source at the left, an AND gate (pointing down, inputs labelled b-bar c-bar like
  s1's binary_circuit) whose BLUE riser feeds D_a, GREEN plain wires Q_a -> D_b and Q_b -> D_c, an
  LED on each Q (L6 led), "output" GREEN by Q_b's LED. Native about 13.2 x 7.25.
  .ffs .names .gate .stubs .in_l .gate_parts .riser .wires .led_stubs .jdots .leds .out_l .clk
  .dots .src .clk_l .hz .spots (bit spots above each box) .in_spot .dval_spot .gate_center;
  .clk_paths() -> fresh thick YELLOW copies of the bus and clock pins for a pulse.
- place_small(circ): a small placement for s7/s8 (width 6.4, left -6.7, top 2.05; unused here).
- board() / sliding_cells(sb): s1's scoreboard (binary row) at native size, centred, top -1.3,
  under the circuit as it stands in clips 1-2 (scale 0.72, top 3.6), and the sliding row
  "sliding | 3 | 1 | none" (sb_cell, row slot 1). s7 adds the ring in slot 2 (re-place it first:
  three rows need 2.6 of height).

Layout: clips 1-2 circuit scale 0.72, top 3.6 (bottom -1.62); the {order} card and then the
waveform (CLK y -2.3, output y -3.0, height 0.45) below it. Clip 3: the circuit shrinks to scale
0.62, top 3.7 (bottom about -0.8), board() below it (top -1.3).
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


# ---- L6 ch6_s6_circuit's make_ff (D flip-flop), copied via s1 ------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def bar_label(ch, size=36, color=GREEN):
    """A letter with an overbar (NOT), e.g. a-bar."""
    q = T(ch, size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(max(q.width * 1.1, 0.2))
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, bubble=False, d_text="D", size=36):
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
    d_l = T(d_text, size, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", size, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar(size).move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    if bub is not None:
        g.add(bub)
    g.box, g.tri, g.bub = box, tri, bub
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


# ---- L6 ch6_s6_circuit's gate and LED, copied ----------------------------------------------------
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
    return Gate(_and_body(), [(-0.7, 0.3), (-0.7, -0.3)], (0.6, 0.0), color=color)


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


# ---- s2's cell bit and waveforms, copied -----------------------------------------------------------
def cell_bit(b, size=44):
    """What a cell holds: a GOLD travelling 1, or a DIM 0 (z 2, above the cell fill)."""
    return Mono("1", size, color=GOLD) if b else Mono("0", size, color=DIM)


def clk_wave(n, p, h=0.6, color=YELLOW, width=4):
    """CLK: n periods of length p, rising at x = k p (high first half), small ▲ on each rise.
    Built with its left end at x = 0 and its middle at y = 0: place it with .shift()."""
    lo, hi = -h / 2, h / 2
    pts = []
    for k in range(n):
        x = k * p
        pts += [[x, lo, 0], [x, hi, 0], [x + p / 2, hi, 0], [x + p / 2, lo, 0]]
    pts.append([n * p, lo, 0])
    wave = VMobject().set_points_as_corners(pts).set_stroke(color, width)
    tri = 0.1 * min(1.0, h / 0.6)
    ups = VGroup(*[Triangle().scale(tri).set_stroke(width=0).set_fill(color, 1).move_to([k * p, 0, 0])
                   for k in range(n)])
    g = VGroup(wave, ups)
    g.wave = wave
    return g


# ---- s1's scoreboard, copied verbatim ------------------------------------------------------------
SB_SIZE = 28
SB_HEAD = ["assignment", "flip-\nflops", "next-state\ngates", "output\nlogic"]
SB_COL_X = (-2.65, -1.0, 0.6, 2.3)     # column centres (col 0 is left-aligned at its left edge)
SB_COL0_LEFT = -3.55
SB_HEAD_Y = 0.95
SB_RULE_Y = 0.45
SB_ROW_Y0, SB_ROW_PITCH = 0.0, 0.6


def scoreboard(rows, n_rows=3):
    """rows: list of (name, flip-flops, gates, output) strings. Room for n_rows rows."""
    head = VGroup()
    for i, (h, x) in enumerate(zip(SB_HEAD, SB_COL_X)):
        t = T(h, SB_SIZE, DIM, line_spacing=0.8)
        if i == 0:
            t.move_to(_p(0, SB_HEAD_Y)).align_to(_p(SB_COL0_LEFT, 0), LEFT)
        else:
            t.move_to(_p(x, SB_HEAD_Y))
        head.add(t)
    rule = Line(_p(SB_COL0_LEFT, SB_RULE_Y), _p(SB_COL_X[3] + 0.6, SB_RULE_Y)).set_stroke(DIM, 2)
    anchors = []
    for r in range(n_rows):
        y = SB_ROW_Y0 - r * SB_ROW_PITCH
        anchors.append([VectorizedPoint(_p(SB_COL0_LEFT, y))] + [VectorizedPoint(_p(x, y)) for x in SB_COL_X[1:]])
    sb = VGroup(head, rule, *[a for row in anchors for a in row])
    sb.head, sb.rule, sb.anchors, sb.rows = head, rule, anchors, []
    sb.unit = rule.get_length()   # native rule length: lets sb_cell scale text with the board
    for r, row in enumerate(rows):
        sb.rows.append(VGroup(*[sb_cell(sb, r, c, s) for c, s in enumerate(row)]))
        sb.add(sb.rows[-1])
    return sb


def sb_cell(sb, r, col, text, color=None):
    """A cell's text for row slot r, column col, sized and placed for the board as it is now."""
    if color is None:
        color = FG if (col == 0 or not text.strip().isdigit()) else GOLD
    t = T(text, SB_SIZE, color).scale(sb.rule.get_length() / sb.unit)
    a = sb.anchors[r][col].get_center()
    if col == 0:
        t.move_to(a, aligned_edge=LEFT)
    else:
        t.move_to(a)
    return t


# ---- this scene's shared pieces --------------------------------------------------------------------
S_FF_X = (-4.4, 0.0, 4.4)            # flip-flops a, b, c
GATE_OUT_Y = 1.7                     # the AND points down; its output sits here
S_GATE_X = S_FF_X[0] - 2.0           # -6.4
CLK_Y = -BOX_H / 2 - EN_WIRE         # -2.3
S_LED_Y = 1.4
S_BIT_Y = 2.2
SMALL_W, SMALL_LEFT, SMALL_TOP = 6.4, -6.7, 2.05
SB_TOP = -1.3
CIRC3_SCALE, CIRC3_TOP = 0.62, 3.7   # clip 3: the circuit above the board


def sliding_circuit():
    """D_a = b-bar . c-bar, D_b = a, D_c = b; output from b. Native, about 13.2 x 7.25."""
    ffs = [make_ff(_p(x, 0), size=42) for x in S_FF_X]
    names = [T(n, 48, GREEN).move_to(_p(x - 0.5, -1.8)) for n, x in zip("abc", S_FF_X)]
    gate = and_gate().rotate(-PI / 2)
    gate.shift(_p(S_GATE_X, GATE_OUT_Y) - gate.out())
    stubs = [Line(gate.inp(i), gate.inp(i) + 0.4 * UP).set_stroke(GREEN, 4) for i in range(2)]
    # rotated -90 deg: inp(0) is on the right, inp(1) on the left
    in_l = [bar_label("b", 46), bar_label("c", 46)]
    in_l[0].move_to(gate.inp(1) + 0.7 * UP, aligned_edge=DOWN).shift(0.08 * LEFT)
    in_l[1].move_to(gate.inp(0) + 0.7 * UP, aligned_edge=DOWN).shift(0.08 * RIGHT)
    d_a = S_FF_X[0] - BOX_W / 2 - WIRE
    riser = poly([(S_GATE_X, GATE_OUT_Y), (S_GATE_X, PIN_Y), (d_a, PIN_Y)], BLUE)
    q_end = [x + BOX_W / 2 + WIRE for x in S_FF_X]
    wires = [Line(_p(q_end[i], PIN_Y), _p(S_FF_X[i + 1] - BOX_W / 2 - WIRE, PIN_Y)).set_stroke(GREEN, 5)
             for i in (0, 1)]
    led_stubs = [Line(_p(x, PIN_Y), _p(x, S_LED_Y - LED_R)).set_stroke(FG, 4) for x in q_end]
    jdots = [Dot(_p(x, PIN_Y), radius=0.08, color=GREEN) for x in q_end[:2]]
    leds = [led(False).move_to(_p(x, S_LED_Y)) for x in q_end]
    out_l = T("output", 42, GREEN).next_to(leds[1], RIGHT, buff=0.2)
    # clock: 1 Hz source at the left end of the bus
    src_c = _p(S_GATE_X - 0.2, CLK_Y)
    circle = Circle(radius=0.28).set_stroke(FG, 3).set_fill(BG, 1).move_to(src_c)
    w = 0.13
    sq = poly([(-2 * w, -w), (-w, -w), (-w, w), (w, w), (w, -w), (2 * w, -w)], YELLOW, 3).move_to(circle)
    src = VGroup(circle, sq)
    clk = Line(src_c + 0.28 * RIGHT, _p(S_FF_X[2], CLK_Y)).set_stroke(YELLOW, 5)
    dots = [Dot(_p(x, CLK_Y), radius=0.08, color=YELLOW) for x in S_FF_X[:2]]
    clk_l = T("CLK", 42, YELLOW).next_to(circle, RIGHT, buff=0.15).shift(0.42 * DOWN)
    hz = T("1 Hz", 42, GOLD).next_to(circle, LEFT, buff=0.15)
    spots = [VectorizedPoint(_p(x, S_BIT_Y)) for x in S_FF_X]
    in_spot = VectorizedPoint(_p(S_FF_X[0] - 1.3, S_BIT_Y))
    dval_spot = VectorizedPoint(_p(S_GATE_X - 0.38, 1.15))
    gate_center = VectorizedPoint(_p(S_GATE_X, GATE_OUT_Y + 0.75))
    gate_parts = VGroup(gate, *stubs, *in_l)
    circ = VGroup(clk, *dots, src, riser, *wires, *led_stubs, *jdots, *ffs, *names, gate_parts,
                  *leds, out_l, clk_l, hz, *spots, in_spot, dval_spot, gate_center)
    circ.ffs, circ.names, circ.gate, circ.stubs, circ.in_l = ffs, names, gate, stubs, in_l
    circ.gate_parts, circ.riser, circ.wires, circ.led_stubs, circ.jdots = gate_parts, riser, wires, led_stubs, jdots
    circ.leds, circ.out_l, circ.clk, circ.dots, circ.src = leds, out_l, clk, dots, src
    circ.clk_l, circ.hz, circ.spots, circ.in_spot = clk_l, hz, spots, in_spot
    circ.dval_spot, circ.gate_center = dval_spot, gate_center

    def clk_paths():
        k = circ.ffs[0].box.width / BOX_W
        return [m.copy().set_stroke(YELLOW, 10 * max(k, 0.5)) for m in [clk] + [f.clk_w for f in ffs]]
    circ.clk_paths = clk_paths
    return circ


def place_small(circ):
    return circ.scale_to_fit_width(SMALL_W).align_to(_p(SMALL_LEFT, 0), LEFT).align_to(_p(0, SMALL_TOP), UP)


def board():
    """s1's board with the binary row, at native size under the clip-2 circuit (top -1.3)."""
    sb = scoreboard([("binary", "3", "3", "none")])
    sb.move_to(_p(0, 0)).align_to(_p(0, SB_TOP), UP)
    return sb


def sliding_cells(sb):
    return [sb_cell(sb, 1, col, s) for col, s in enumerate(("sliding", "3", "1", "none"))]


# ---- the {order} reminder card -------------------------------------------------------------------
CARD_Y = -2.6
MINI_SIDE, MINI_PITCH = 0.62, 0.82


def mini_row(cx, names, bits):
    cells, labs, vals = [], [], []
    for i, (n, b) in enumerate(zip(names, bits)):
        p = _p(cx + (i - 1) * MINI_PITCH, CARD_Y)
        sq = Square(MINI_SIDE, color=BLUE, stroke_width=3).set_fill(GOLD if b else BG, 0.22 if b else 1).move_to(p)
        cells.append(sq)
        labs.append(T(n, 30, GREEN).next_to(sq, UP, buff=0.1))
        vals.append(cell_bit(b, 32).move_to(p).set_z_index(2))
    g = VGroup(*cells, *labs, *vals)
    g.cells, g.labs, g.vals = cells, labs, vals
    return g


def card_arrow(x0, x1, color):
    return Arrow(_p(x0, CARD_Y), _p(x1, CARD_Y), buff=0, color=color, stroke_width=4,
                 tip_length=0.18, max_tip_length_to_length_ratio=0.4)


# ---- the run -----------------------------------------------------------------------------------------
W_X0, W_P, W_H = -4.2, 0.95, 0.45
W_CLK_Y, W_OUT_Y = -2.3, -3.0


def d_a(state):
    return int(state[1] == 0 and state[2] == 0)


def out_piece(k, bits):
    lv = lambda b: W_OUT_Y + (W_H / 2 if b else -W_H / 2)  # noqa: E731
    x = W_X0 + k * W_P
    pts = []
    if k > 0 and bits[k] != bits[k - 1]:
        pts.append((x, lv(bits[k - 1])))
    pts += [(x, lv(bits[k])), (x + W_P, lv(bits[k]))]
    return poly(pts, GREEN, 4)


class SlideCircuit(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c2.circ.1
    def clip1(self):
        with self.say("c2.circ.1") as c:
            circ = self.circ = sliding_circuit()
            circ.scale(0.72).move_to(_p(0, 0)).align_to(_p(0, 3.6), UP)
            ffs = circ.ffs
            self.play(*appear(*ffs, *circ.names, lag=0.15, shift=None),
                      FadeIn(circ.clk), FadeIn(circ.src), *[FadeIn(d) for d in circ.dots],
                      *appear(circ.clk_l, circ.hz, shift=None), run_time=1.6)  # early: the circuit shown whole, then walked
            self.play(*appear(circ.gate_parts, circ.riser, *circ.wires, *circ.jdots, lag=0.12, shift=None),
                      *appear(*circ.led_stubs, *circ.leds, circ.out_l, lag=0.1, shift=None),
                      run_time=1.6)  # early: the circuit shown whole, then walked
            self.add(circ)

            # {order}: s2's table row, mirrored into the circuit's a b c
            c.wait_until("order")
            table = self.table = mini_row(3.2, "cba", (0, 0, 1))
            t_arrow = self.t_arrow = card_arrow(1.94, 1.34, DIM)
            t_cap = self.t_cap = T("table: a on the right", 30, FG).move_to(_p(3.2, -3.4))
            self.play(*appear(table, t_arrow, t_cap, lag=0.2, shift=None), run_time=1.1)  # early: s2's row, recalled
            crow = self.crow = mini_row(-3.2, "abc", (1, 0, 0))
            c_cap = self.c_cap = T("circuit: a on the left", 30, FG).move_to(_p(-3.2, -3.4))
            c.wait_until("circuit puts")
            self.play(*appear(*crow.cells, *crow.labs, *crow.vals, lag=0.08, shift=None),
                      run_time=min(1.4, 0.8 * c.until("on the left")))
            c.wait_until("on the left")
            self.play(*appear(c_cap), FlashAround(circ.names[0], color=GREEN, time_width=1.5), run_time=1.0)
            c_arrow = self.c_arrow = card_arrow(-1.94, -1.34, GOLD)
            c.wait_until("slide to the right")
            self.play(GrowArrow(c_arrow), *flash(crow.vals[0:1], color=GOLD), run_time=1.2)

            # {gate}
            c.wait_until("gate")
            g = circ.gate
            self.play(*[m.animate.set_stroke(YELLOW) for m in g.strokes()], *flash([g]), run_time=1.0)
            c.wait_until("takes the")
            self.play(*flash([ffs[1].qb_l, ffs[2].qb_l], color=GREEN),
                      *flash(circ.in_l, color=GREEN), run_time=1.3)
            c.wait_until("feeds")
            self.play(VShowPassingFlash(circ.riser.copy().set_stroke(YELLOW, 9), time_width=0.6),
                      FlashAround(ffs[0].d_l, color=BLUE), run_time=1.2)

            # {wires}
            c.wait_until("wires")
            self.play(*[m.animate.set_stroke(BLUE) for m in g.strokes()],
                      circ.wires[0].animate.set_stroke(YELLOW),
                      VShowPassingFlash(circ.wires[0].copy().set_stroke(YELLOW, 10), time_width=0.6),
                      run_time=1.4)
            c.wait_until("output of bee")
            self.play(circ.wires[1].animate.set_stroke(YELLOW),
                      VShowPassingFlash(circ.wires[1].copy().set_stroke(YELLOW, 10), time_width=0.6),
                      run_time=1.4)

    # ------------------------------------------------------------------ c2.circ.2
    def clip2(self):
        circ = self.circ
        ffs = circ.ffs
        with self.say("c2.circ.2") as c:
            k = ffs[0].box.width / BOX_W
            size = 50 * k
            spots = [s.get_center() for s in circ.spots]
            bits = [cell_bit(0, size).move_to(p).set_z_index(2) for p in spots]
            card = [self.table, self.crow, self.t_arrow, self.c_arrow, self.t_cap, self.c_cap]
            self.play(*during(disappear(*card), 0, 0.45),
                      *[w.animate.set_stroke(GREEN) for w in circ.wires],
                      *during(appear(*bits, lag=0.15, shift=None), 0.45, 1), run_time=1.6)

            # D_a = 1 at 000; the wave starts
            dval = cell_bit(1, 40 * k).move_to(circ.dval_spot).set_color(GOLD)
            w_clk_l = T("CLK", 30, YELLOW).next_to(_p(W_X0, W_CLK_Y), LEFT, buff=0.3)
            w_out_l = T("output", 30, GREEN).next_to(_p(W_X0, W_OUT_Y), LEFT, buff=0.3)
            seq = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 1), (0, 0, 1)]
            out_bits = [s[1] for s in seq] * 2
            clk_pieces = [clk_wave(1, W_P, W_H).shift(_p(W_X0 + j * W_P, W_CLK_Y)) for j in range(10)]
            out_pieces = [out_piece(j, out_bits) for j in range(10)]
            c.wait_until("first state")
            self.play(circ.riser.animate.set_stroke(GOLD), ffs[0].d_w.animate.set_stroke(GOLD),
                      *appear(dval, shift=None), run_time=1.0)
            self.play(*appear(w_clk_l, w_out_l, shift=None, lag=0.2),  # early: the plot's axes, filled in on the edges
                      Create(clk_pieces[0].wave, rate_func=linear), FadeIn(clk_pieces[0][1]),
                      Create(out_pieces[0], rate_func=linear), run_time=min(1.2, c.until("tick")))

            # {tick}: ten edges, two rounds
            c.wait_until("tick")
            per = (c.until() - 0.3) / 10
            t_out, t_wave = c.at("out"), c.at("wave")
            done = set()
            state = seq[0]
            for j in range(1, 11):
                new = (d_a(state), state[0], state[1])
                g = cell_bit(new[0], size).move_to(spots[0]).set_z_index(2)
                anims = [VShowPassingFlash(p, time_width=0.8) for p in circ.clk_paths()]
                anims += [time_span(FadeOut(bits[2]), 0, 0.25),   # leaves in place: never a 2nd digit over c's LED
                          bits[1].animate.move_to(spots[2]), bits[0].animate.move_to(spots[1]),
                          FadeIn(g, shift=spots[0] - circ.in_spot.get_center())]
                bits = [g, bits[0], bits[1]]
                for i in range(3):
                    if new[i] != state[i]:
                        anims.append(ffs[i].box.animate.set_fill(GOLD if new[i] else BG, 0.22 if new[i] else 0))
                        anims.append(set_led(circ.leds[i], bool(new[i])))
                if d_a(new) != d_a(state):
                    col = GOLD if d_a(new) else BLUE
                    nd = cell_bit(d_a(new), 40 * k).move_to(circ.dval_spot)
                    if d_a(new):
                        nd.set_color(GOLD)
                    anims += [circ.riser.animate.set_stroke(col), ffs[0].d_w.animate.set_stroke(col),
                              *swap(dval, nd)]
                    dval = nd
                if j < 10:
                    cp = clk_pieces[j]
                    anims += [Create(cp.wave, rate_func=linear), FadeIn(cp[1]),
                              Create(out_pieces[j], rate_func=linear)]
                else:
                    x = W_X0 + 10 * W_P
                    tail_c = poly([(x, W_CLK_Y - W_H / 2), (x, W_CLK_Y + W_H / 2),
                                   (x + 0.3, W_CLK_Y + W_H / 2)], YELLOW, 4)
                    tail_o = poly([(x, W_OUT_Y - W_H / 2), (x + 0.3, W_OUT_Y - W_H / 2)], GREEN, 4)
                    anims += [Create(tail_c, rate_func=linear), Create(tail_o, rate_func=linear)]
                now = self.time
                if "out" not in done and t_out < now + per:
                    done.add("out")
                    anims += [FlashAround(circ.out_l, color=GREEN, time_width=1.5),
                              FlashAround(w_out_l, color=GREEN, time_width=1.5)]
                if "wave" not in done and t_wave < now + per:
                    done.add("wave")
                    hi = Line(_p(W_X0 + 2 * W_P, W_OUT_Y + W_H / 2), _p(W_X0 + 4 * W_P, W_OUT_Y + W_H / 2))
                    anims += [FlashAround(hi, color=GREEN, time_width=1.5, buff=0.14)]
                self.play(*anims, run_time=0.62 * per)
                state = new
                if j < 10:
                    self.wait(0.38 * per)
            self.bits, self.dval = bits, dval
            self.waves = [w_clk_l, w_out_l, *clk_pieces, *out_pieces, tail_c, tail_o]

    # ------------------------------------------------------------------ c2.circ.3
    def clip3(self):
        circ = self.circ
        with self.say("c2.circ.3") as c:
            sb = board()
            # the circuit shrinks a little (labels stay >= 26) and rises, so the board has clear room below
            circ.generate_target()
            circ.target[circ.submobjects.index(circ.riser)].set_stroke(BLUE)
            circ.target[circ.submobjects.index(circ.ffs[0])].d_w.set_stroke(BLUE)
            circ.target.scale(CIRC3_SCALE / 0.72).move_to(_p(0, 0)).align_to(_p(0, CIRC3_TOP), UP)
            sweep_clear(self, time_span(MoveToTarget(circ), 0.3, 1.2), time_span(FadeIn(sb), 0.9, 1.8), keep=[circ], run_time=1.8)  # early: the scoreboard returns
            row = sliding_cells(sb)
            self.play(*appear(row[0]), run_time=1.0)
            c.wait_until("same three")
            self.play(*appear(row[1]), FlashAround(sb.rows[0][1], color=GOLD), run_time=1.0)
            c.wait_until("one gate")
            self.play(*appear(row[2]), FlashAround(sb.rows[0][2], color=GOLD, time_width=1.5),
                      FlashAround(row[2], color=GOLD, time_width=1.5), run_time=1.3)
            self.play(*appear(row[3]), run_time=min(0.9, c.until("less")))  # early: output logic, not spoken

            c.wait_until("less")
            self.play(*[w.animate.set_stroke(YELLOW) for w in circ.wires],
                      *[VShowPassingFlash(w.copy().set_stroke(YELLOW, 8), time_width=0.6) for w in circ.wires],
                      run_time=1.5)
            c.wait_until("plain wires")
            self.play(*[VShowPassingFlash(w.copy().set_stroke(YELLOW, 8), time_width=0.6) for w in circ.wires],
                      run_time=1.2)

            c.wait_until("further")
            q = T("?", 64, YELLOW).move_to(circ.gate_center)
            set_backstroke(q, width=8)
            self.play(*set_alpha([circ.gate_parts], DIMMED), *appear(q, shift=None), run_time=1.2)
