"""Chapter 2, scene 7: flip-flops or wires? The ring trades two flip-flops for no logic; on a chip
that can be the cheaper design; the scoreboard gains its ring row. Clips c2.trade.1 – c2.trade.3.

Helpers copied verbatim: s4's (ch2_s4_slidecircuit.py) make_ff/gate/led parts, s1's scoreboard /
sb_cell, sliding_circuit, place_small, board, sliding_cells; s6's ring_circuit; s1's quote_card.

Shared visual owned here (s8's recap and ch3-ch6 reuse it):
- board3(): the three-row scoreboard (binary / sliding / ring "ring | 5 | 0 | none"), centred, scale
  SB3_SCALE. ring_cells(sb) adds the ring row to a board; sb_arrows(sb) -> the two GOLD arrows
  (beside the flip-flop and gate columns, both pointing down the rows); sb_arrow_labels(sb, arrows)
  -> "more" / "fewer" under their tips; row_box(sb, r) -> the row highlight.
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


# ---- s6's ring circuit (ch2_s6_nologic.py), copied verbatim ----------------------------------------
RING = "abcde"
RC_X = (-6.4, -3.2, 0.0, 3.2, 6.4)    # flip-flops a..e, native; Q of one meets D of the next
RC_TOP = 2.7                           # feedback wire height, native
RC_CLK_Y = -BOX_H / 2 - EN_WIRE        # -2.3
RC_SCALE = 0.77
RC_CENTER = _p(0.0, -0.2)


def ring_circuit():
    """Five D flip-flops a..e on one CLK, Q_a->D_b ... Q_d->D_e, Q_e back along the top to D_a,
    "output" on Q_b. No gates. Final frame position: centre (0, -0.2), 12.93 x 4.02."""
    ffs = [make_ff(_p(x, 0), size=42) for x in RC_X]
    names = [T(n, 48, GREEN).move_to(_p(x - 0.5, -1.8)) for n, x in zip(RING, RC_X)]
    q_end = RC_X[4] + BOX_W / 2 + WIRE          # 8.0
    d_start = RC_X[0] - BOX_W / 2 - WIRE        # -8.0
    feedback = poly([(q_end, PIN_Y), (q_end, RC_TOP), (d_start - 0.3, RC_TOP), (d_start - 0.3, PIN_Y),
                     (d_start, PIN_Y)], GREEN)
    clk = Line(_p(RC_X[0] - 1.0, RC_CLK_Y), _p(RC_X[4], RC_CLK_Y)).set_stroke(YELLOW, 5)
    clk_l = T("CLK", 44, YELLOW).next_to(clk, LEFT, buff=0.15)
    dots = [Dot(_p(x, RC_CLK_Y), radius=0.08, color=YELLOW) for x in RC_X[:4]]
    # "output": a tap on the Q_b -> D_c wire, pointing down between b and c, label under the boxes
    tap = _p(RC_X[1] + BOX_W / 2 + WIRE + 0.25, PIN_Y)      # x -1.35, clear of b's Q-bar stub (-1.6)
    out_arrow = Arrow(tap, _p(tap[0], -1.4), buff=0, color=GREEN, stroke_width=4,
                      tip_length=0.2, max_tip_length_to_length_ratio=0.3)
    out_dot = Dot(tap, radius=0.08, color=GREEN)
    out_l = T("output", 40, GREEN).move_to(_p(-1.85, -1.72))
    circ = VGroup(clk, *dots, feedback, *ffs, *names, out_arrow, out_dot, out_l, clk_l)
    circ.ffs, circ.names, circ.feedback, circ.clk, circ.clk_l = ffs, names, feedback, clk, clk_l
    circ.dots, circ.out_arrow, circ.out_dot, circ.out_l = dots, out_arrow, out_dot, out_l
    circ.scale(RC_SCALE).move_to(RC_CENTER)
    return circ


# ---- s1's quote card, copied ---------------------------------------------------------------------
def quote_card(text, size=30):
    t = T(text, size, FG, slant=ITALIC, line_spacing=0.9)
    box = RoundedRectangle(corner_radius=0.15, width=t.width + 0.6, height=t.height + 0.5)
    box.set_stroke(DIM, 2).set_fill(BG, 1)
    return VGroup(box, t.move_to(box))



# ---- the three-row scoreboard (shared: s8, ch3-ch6) -------------------------------------------------
SB3_SCALE = 1.35
SB3_CENTER = _p(0.0, 1.0)
RING_ROW = ("ring", "5", "0", "none")


def ring_cells(sb):
    return [sb_cell(sb, 2, col, s) for col, s in enumerate(RING_ROW)]


def board3(with_ring=True):
    """s1's scoreboard with binary and sliding rows (and the ring row), scaled and centred."""
    sb = scoreboard([("binary", "3", "3", "none"), ("sliding", "3", "1", "none")])
    sb.scale(SB3_SCALE).move_to(SB3_CENTER)
    if with_ring:
        row = VGroup(*ring_cells(sb))
        sb.rows.append(row)
        sb.add(row)
    return sb


def row_box(sb, r, color=YELLOW):
    a = sb.anchors[r]
    w = sb.rule.get_length() + 0.3
    box = Rectangle(width=w, height=0.62 * sb.rule.get_length() / sb.unit).set_stroke(color, 2)
    box.set_fill(color, 0.15).set_z_index(-1)
    return box.move_to(_p(sb.rule.get_center()[0], a[0].get_center()[1]))


def sb_arrows(sb):
    """GOLD arrows beside the flip-flop column (3, 3, 5) and the gate column (3, 1, 0), both pointing
    down the rows in reading order (binary -> sliding -> ring); label them with sb_arrow_labels."""
    k = sb.rule.get_length() / sb.unit
    top = sb.anchors[0][1].get_center()[1] + 0.22 * k
    bot = sb.anchors[2][1].get_center()[1] - 0.22 * k
    out = []
    for col, up in ((1, False), (2, False)):
        x = sb.anchors[0][col].get_center()[0] + 0.42 * k
        a, b = (_p(x, bot), _p(x, top)) if up else (_p(x, top), _p(x, bot))
        out.append(Arrow(a, b, buff=0, color=GOLD, stroke_width=5, tip_length=0.22,
                         max_tip_length_to_length_ratio=0.3))
    return out


def sb_arrow_labels(sb, arrows, words=("more", "fewer")):
    """GOLD labels under the two arrow tips: flip-flops "more", gates "fewer"."""
    k = sb.rule.get_length() / sb.unit
    base = min(a.get_end()[1] for a in arrows) - 0.36 * k     # shared baseline (neither word has a descender)
    return [T(w, 30, GOLD).move_to(a.get_end()).align_to(_p(0, base), DOWN) for w, a in zip(words, arrows)]


# ---- the two chips ------------------------------------------------------------------------------------
CHIP_W, CHIP_H = 6.0, 4.4
L_C, R_C = _p(-3.6, -0.1), _p(3.6, -0.1)
FB_W, FB_H = 0.8, 1.0
FF_Y = 1.0
WIRE_W = 3


def ff_block(p):
    box = Rectangle(width=FB_W, height=FB_H).set_stroke(FG, 3).set_fill(BG, 1).move_to(p)
    lab = T("FF", 40, FG).move_to(p)
    g = VGroup(box, lab)
    g.box = box
    return g


def chip_outline(center, name):
    r = RoundedRectangle(corner_radius=0.3, width=CHIP_W, height=CHIP_H).set_stroke(DIM, 4).move_to(center)
    lab = T("chip", 44, DIM).next_to(r, UP, buff=0.12).align_to(r, LEFT).shift(0.2 * RIGHT)
    nm = T(name, 44, FG).next_to(r, DOWN, buff=0.15)
    return r, lab, nm


def binary_chip():
    r, lab, nm = chip_outline(L_C, "binary")
    cx = L_C[0]
    fx = [cx - 1.8, cx, cx + 1.8]
    gx = [cx - 1.5, cx, cx + 1.5]
    ffs = [ff_block(_p(x, FF_Y)) for x in fx]
    gy = -1.25
    gates = []
    for x in gx:
        g = and_gate().scale(0.6).rotate(-PI / 2)
        g.move_to(_p(x, gy))
        gates.append(g)
    pins = [_p(x + d, FF_Y - FB_H / 2) for x in fx for d in (-0.2, 0.2)]
    ins = [g.inp(i) for g in gates for i in (1, 0)]
    order = [3, 0, 5, 1, 4, 2]
    levels = [0.3, -0.5, 0.1, -0.3, -0.1, -0.7]
    wires = []
    for i, j in enumerate(order):
        p, q = pins[i], ins[j]
        y = levels[i]
        wires.append(VMobject().set_points_as_corners([p, _p(p[0], y), _p(q[0], y), q]).set_stroke(FG, WIRE_W))
    for k, (g, f) in enumerate(zip(gates, ffs)):
        o = g.out()
        yb = -1.82 - 0.1 * k
        xl = cx - 2.75 + 0.1 * k
        yt = 1.78 + 0.12 * k
        xf = fx[k] - FB_W / 2
        pts = [o, _p(o[0], yb), _p(xl, yb), _p(xl, yt), _p(xf - 0.2, yt), _p(xf - 0.2, FF_Y + 0.25),
               _p(xf, FF_Y + 0.25)]
        wires.append(VMobject().set_points_as_corners(pts).set_stroke(FG, WIRE_W))
    cost = Rectangle(width=CHIP_W - 0.5, height=1.3).set_stroke(width=0).set_fill(GOLD, 0.2)
    cost.move_to(_p(cx, -0.2)).set_z_index(-1)
    grp = VGroup(r, lab, nm, *wires, *[g for g in gates], *ffs)
    grp.outline, grp.lab, grp.nm, grp.ffs, grp.gates, grp.wires, grp.cost = r, lab, nm, ffs, gates, wires, cost
    return grp


def ring_chip():
    r, lab, nm = chip_outline(R_C, "ring")
    cx = R_C[0]
    fx = [cx + (i - 2) * 1.1 for i in range(5)]
    ffs = [ff_block(_p(x, FF_Y)) for x in fx]
    wires = [Line(_p(fx[i] + FB_W / 2, FF_Y), _p(fx[i + 1] - FB_W / 2, FF_Y)).set_stroke(FG, WIRE_W)
             for i in range(4)]
    e, a = fx[4] + FB_W / 2, fx[0] - FB_W / 2
    wires.append(VMobject().set_points_as_corners(
        [_p(e, FF_Y), _p(e + 0.2, FF_Y), _p(e + 0.2, 1.8), _p(a - 0.2, 1.8), _p(a - 0.2, FF_Y), _p(a, FF_Y)]
    ).set_stroke(FG, WIRE_W))
    spare = RoundedRectangle(corner_radius=0.2, width=CHIP_W - 0.6, height=2.0).set_stroke(GREEN, 2)
    spare.set_fill(GREEN, 0.2).move_to(_p(cx, -1.15))
    spare_l = T("room to spare", 42, GREEN).move_to(spare)
    grp = VGroup(r, lab, nm, *wires, *ffs)
    grp.outline, grp.lab, grp.nm, grp.ffs, grp.wires, grp.spare, grp.spare_l = r, lab, nm, ffs, wires, spare, spare_l
    return grp


class Tradeoff(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c2.trade.1
    def clip1(self):
        with self.say("c2.trade.1") as c:
            cap = T("See needs 2 more FFs, but no logic and simple wiring", 36, t2c={"2 more FFs": GOLD})
            cap.move_to(_p(0, 2.95))
            ring = ring_circuit().scale_to_fit_width(12.0).move_to(_p(0, 0.45))
            self.play(*appear(cap), FadeIn(ring), run_time=min(1.5, c.until("two more")))  # early: the slide's line, read next
            c.wait_until("two more")
            self.play(FlashUnder(select(cap, "2 more FFs")[0], color=GOLD, run_time=1.5, time_width=1.5),
                      *[FlashAround(ring.ffs[i].box, color=GOLD, run_time=1.5, time_width=1.5) for i in (3, 4)])
            c.wait_until("fun")
            card = quote_card("“just a couple of bits of fun”", 36).move_to(_p(0, -2.95))
            self.play(*appear(card), run_time=1.0)

            c.wait_until("power")
            slide = place_small(sliding_circuit()).scale_to_fit_width(6.5).move_to(_p(-3.45, 0.3))
            k = 6.5 / ring.width
            ring.generate_target()
            ring.target.scale(k)
            ring.target.shift(_p(3.45, 0) - _p(ring.target.get_center()[0], 0))
            dy = slide.ffs[0].box.get_center()[1] - ring.target.ffs[0].box.get_center()[1]
            ring.target.shift(dy * UP)
            self.play(*during([FadeOut(cap)], 0, 0.45),
                      *during([MoveToTarget(ring)], 0.2, 0.8),
                      *during([FadeIn(slide)], 0.5, 1.0), run_time=min(2.0, c.until("no combinational")))
            g1 = T("one gate", 36, GOLD).move_to(_p(-3.45, -1.95))
            g0 = T("no gates", 36, GOLD).move_to(_p(3.45, -1.95))
            k_s = slide.ffs[0].box.width / BOX_W
            self.play(*[VShowPassingFlash(m.copy().set_stroke(BLUE, 12 * k_s), time_width=0.6)  # early: one gate, then none
                        for m in (slide.riser, slide.ffs[0].d_w)],
                      FlashAround(slide.gate_parts, color=BLUE, run_time=1.5, time_width=1.5),
                      *appear(g1), run_time=1.5)
            self.play(*appear(g0), run_time=1.0)  # early: one gate, then none
            c.wait_until("no combinational")
            k_r = ring.ffs[0].box.width / BOX_W
            self.play(*[VShowPassingFlash(f.d_w.copy().set_stroke(BLUE, 14 * k_r), time_width=0.8)
                        for f in ring.ffs],
                      *[f.d_w.animate.set_stroke(BLUE, 9 * k_r) for f in ring.ffs],
                      FlashAround(g0, color=GOLD, run_time=1.5, time_width=1.5),
                      run_time=min(1.5, c.until() - 0.1))
            self.board_now = [slide, ring, g1, g0]

    # ------------------------------------------------------------------ c2.trade.2
    def clip2(self):
        with self.say("c2.trade.2") as c:
            lc, rc = binary_chip(), ring_chip()
            sweep_clear(self, time_span(FadeIn(lc), 0.6, 1.6), time_span(FadeIn(rc), 0.8, 1.8),  # early: the chips, named as they appear
                        run_time=min(1.8, c.until("modern")))
            c.wait_until("only a little")
            blocks = [f.box for f in lc.ffs + rc.ffs]
            self.play(*flash(blocks, color=GREEN, run_time=1.5, time_width=1.5),
                      *[b.animate.set_fill(GREEN, 0.25) for b in blocks], run_time=1.5)
            c.wait_until("wiring")
            self.play(*[w.animate.set_stroke(GOLD, 4) for w in lc.wires], FadeIn(lc.cost),
                      *[b.animate.set_fill(BG, 1) for b in blocks], run_time=1.5)
            c.wait_until("more flip-flops")
            self.play(FadeIn(rc.spare), *appear(rc.spare_l, shift=None), run_time=1.5)  # early: the spare area, said as "more"

            c.wait_until("part1")
            chips = VGroup(lc, lc.cost, rc, rc.spare, rc.spare_l)
            b1 = T("• FF implementation may take less chip area than you\n"
                   "   may think given their gate level representation", 30, line_spacing=0.9)
            b2 = T("• Wiring complexity can be as big an issue as gate complexity", 30)
            VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(_p(0, -2.4))
            chips.generate_target()
            chips.target.scale(0.7).move_to(_p(0, 1.4))
            self.play(MoveToTarget(chips), run_time=1.3)
            self.play(*appear(b1), run_time=1.0)  # early: the slide's points, read as a pair
            c.wait_until("area and wiring")
            self.play(*appear(b2), run_time=min(1.0, c.until()))
            self.bullets = [b1, b2]

    # ------------------------------------------------------------------ c2.trade.3
    def clip3(self):
        with self.say("c2.trade.3") as c:
            sb = board3(with_ring=False)
            sweep_clear(self, time_span(FadeIn(sb), 0.6, 1.2),  # early: the scoreboard returns
                        *[time_span(b.animate.shift(0.4 * DOWN), 0.3, 1.2) for b in self.bullets],
                        keep=self.bullets, run_time=1.2)
            row = ring_cells(sb)
            self.play(*appear(*row, lag=0.15), run_time=min(1.0, c.until("binary")))  # early: the ring row joins the board
            settle(self, sb, add=[VGroup(*row)])
            sb.rows.append(VGroup(*row))

            c.wait_until("binary")
            box = row_box(sb, 0)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("sliding")
            self.play(Transform(box, row_box(sb, 1)), run_time=1.0)
            c.wait_until("ring")
            arrows = sb_arrows(sb)
            self.play(Transform(box, row_box(sb, 2)), run_time=1.0)
            labs = sb_arrow_labels(sb, arrows)
            self.play(*[GrowArrow(a) for a in arrows], *appear(*labs, lag=0.3),  # early: more / fewer, what the row says
                      run_time=min(1.5, c.until("none of them")))
            c.wait_until("none of them")
            outs = [sb.rows[r][3] for r in range(3)]
            self.play(FadeOut(box), *recolor(outs, GREEN), *flash(outs, color=GREEN, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("depends")
            dep = T("Depends what we are trying to optimise", 40, slant=ITALIC)
            dep.move_to(_p(0, -2.85))
            self.play(*swap(VGroup(*self.bullets), dep), run_time=1.2)
        self.wait(4.0)
