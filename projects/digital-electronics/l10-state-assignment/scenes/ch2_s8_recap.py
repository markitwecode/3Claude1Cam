"""Chapter 2, scene 8: recap in six panels on a 3 x 2 grid, then the ring switched on: nothing happens.
Clips c2.recap.1 – c2.recap.2.

Layout: "Recap" T 40 at (0, 3.4) (L8 ch5_s7_recap's heading); six faint DIM slot frames 4.2 x 3.1 at
x = -4.5, 0, 4.5, tops y 2.95 / -0.3. Each panel's picture fits 3.9 x 2.05 at (x, top - 1.18), its
line (T 28) hangs from top - 2.3. Earlier panels dim under a BG veil (as L8's recaps).
 r1 s2's SlideRow (bits 001 -> 011 -> 110), r2 s2's bit_wave a b c (two rounds, outlined GREEN),
 r3 s3's slide_table with col_box(0, 2) GREEN + col_box(1, 1) BLUE and D_b = a,
 r4 s4's sliding_circuit with the AND lit YELLOW, r5 s5's ring_circle (GOLD pair stepping round),
 r6 s7's board3 + sb_arrows.
{next}: s6's ring_circuit() at its own geometry (centre (0, -0.2)); below it "output" T 30 GREEN and
the flat GREEN trace at y -3.3 (x -5.0 .. 6.0) under CLK pulses; RED "?" T 64 at (0.5, -2.75).
End card: "Part 3 · Starting in a used state" T 40 at (0, 3.2); the clock keeps ticking ~8 s; fade.
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


# ---- s4's circuit parts (ch2_s4_slidecircuit.py, copied verbatim; s6/s7 share them) ----------
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

# ---- r1/r2: s2's SlideRow and bit_wave (ch2_s2_sliding.py, copied verbatim) -------------------
SLIDE_PITCH = 2.4    # cell centre to cell centre
SLIDE_SIDE = 1.5     # cell square side
CODES = ["000", "001", "011", "110", "100"]


class SlideRow(VGroup):
    """Three flip-flop cells c b a (a on the right), BLUE squares with GREEN names above,
    DIM arrows showing the shift direction (in at a, a->b->c, out past c).
    .cells .names .links (in, a->b, b->c, out) .items (the bits held, c b a) .bits.
    step(new) -> anims: every bit slides one cell left, c's falls off, `new` enters a;
    cells holding a 1 light faintly GOLD."""

    def __init__(self, center, **kw):
        super().__init__(**kw)
        self.cells = [Square(SLIDE_SIDE, color=BLUE, stroke_width=4).set_fill(BG, 1)
                      .move_to(center + (i - 1) * SLIDE_PITCH * RIGHT) for i in range(3)]
        self.names = [T(n, 40, color=GREEN).next_to(self.cells[i], UP, buff=0.22)
                      for i, n in enumerate("cba")]
        kw_a = dict(buff=0, color=DIM, stroke_width=3, tip_length=0.16,
                    max_tip_length_to_length_ratio=0.4)
        a_r = self.cells[2].get_right()
        c_l = self.cells[0].get_left()
        self.links = [Arrow(a_r + 0.68 * RIGHT, a_r + 0.08 * RIGHT, **kw_a)]
        for i in (1, 0):
            self.links.append(Arrow(self.cells[i + 1].get_left() + 0.08 * LEFT,
                                    self.cells[i].get_right() + 0.08 * RIGHT, **kw_a))
        self.links.append(Arrow(c_l + 0.08 * LEFT, c_l + 0.68 * LEFT, **kw_a))
        self.items, self.bits = [], [0, 0, 0]
        self.add(*self.cells, *self.names, *self.links)

    def zeros(self):
        self.items = [cell_bit(0).move_to(c).set_z_index(2) for c in self.cells]
        return self.items

    def step(self, new):
        old = self.items
        g = cell_bit(new).move_to(self.cells[2]).set_z_index(2)
        anims = [FadeOut(old[0], shift=SLIDE_PITCH * LEFT),
                 old[1].animate.shift(SLIDE_PITCH * LEFT),
                 old[2].animate.shift(SLIDE_PITCH * LEFT),
                 FadeIn(g, shift=SLIDE_PITCH * LEFT)]
        self.items = [old[1], old[2], g]
        self.bits = self.bits[1:] + [new]
        for cell, b in zip(self.cells, self.bits):
            anims.append(cell.animate.set_fill(GOLD if b else BG, 0.22 if b else 1))
        return anims



def bit_wave(bits, p, h=0.6, color=GREEN, width=4):
    """A signal holding bits[k] for period k (changes on the rising edges at x = k p).
    Left end at x = 0, middle at y = 0, like clk_wave."""
    lv = lambda b: h / 2 if b else -h / 2  # noqa: E731
    pts = [[0, lv(bits[0]), 0]]
    for k in range(1, len(bits)):
        if bits[k] != bits[k - 1]:
            pts += [[k * p, lv(bits[k - 1]), 0], [k * p, lv(bits[k]), 0]]
    pts.append([len(bits) * p, lv(bits[-1]), 0])
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)



# ---- r3: s3's slide_table / col_box (ch2_s3_slidelogic.py, copied verbatim) -------------------
SL_CODES = ["000", "001", "011", "110", "100"]
SL_GX = (-4.9, -1.9)          # current / next block centres (current = s2's widened code column)
SL_GAP = 0.85                 # digit pitch inside a block (c, b, a at -GAP, 0, +GAP)
SL_TITLE_Y, SL_HEAD_Y, SL_PITCH = 2.45, 1.75, 0.7
SL_SEP_X, SL_RULE_Y = -3.4, 1.4


def slide_table(dx=0.0):
    """The sliding assignment's state transition table (p. 135). The current block is exactly s2's
    code_column(-4.9, 1.75, gap=0.85): GREEN T 36 header letters, Mono 36 digits (1s GOLD, 0s FG),
    rows at y = 1.05 - 0.7 r. Next block centred at x = -1.9, headers c′ b′ a′. Titles
    "Current state" / "Next state" T 30 FG at y 2.45; DIM stroke-2 rules (vertical at -3.4, under the
    headers at y 1.4). The table spans about x -6.2 .. -0.6, y 2.7 .. -2.0 (shifted by dx).
    .titles[g] .heads[g] (VGroup of 3) .lines .cur[r] / .nxt[r] (VGroup of 3 digits, c first)
    .groups = [cur, nxt]; .col(g, j) -> VGroup(header j, its 5 digits); .block(g) -> heads+rows."""
    titles = VGroup(*[T(s, 30).move_to(_p(gx, SL_TITLE_Y)) for s, gx in zip(("Current state", "Next state"), SL_GX)])
    heads = VGroup(*[VGroup(*[T(n + pr, 36, color=GREEN).move_to(_p(gx + (j - 1) * SL_GAP, SL_HEAD_Y))
                              for j, n in enumerate("cba")])
                     for pr, gx in zip(("", "′"), SL_GX)])
    lines = VGroup(Line(_p(SL_SEP_X, 2.8), _p(SL_SEP_X, -2.05)).set_stroke(DIM, 2),
                   Line(_p(-6.15, SL_RULE_Y), _p(-0.65, SL_RULE_Y)).set_stroke(DIM, 2))

    def row(code, gx, r):
        y = SL_HEAD_Y - SL_PITCH * (r + 1)
        return VGroup(*[Mono(d, 36, color=GOLD if d == "1" else FG).move_to(_p(gx + (j - 1) * SL_GAP, y))
                        for j, d in enumerate(code)])
    cur = VGroup(*[row(code, SL_GX[0], r) for r, code in enumerate(SL_CODES)])
    nxt = VGroup(*[row(SL_CODES[(r + 1) % 5], SL_GX[1], r) for r in range(5)])
    g = VGroup(titles, heads, lines, cur, nxt)
    g.shift(dx * RIGHT)
    g.titles, g.heads, g.lines, g.cur, g.nxt = titles, heads, lines, cur, nxt
    g.groups = [cur, nxt]
    g.col = lambda gi, j: VGroup(heads[gi][j], *[r[j] for r in g.groups[gi]])
    return g


def col_box(tab, gi, j, color):
    return SurroundingRectangle(tab.col(gi, j), color=color, buff=0.14, stroke_width=4)



# ---- r5: s5's ring_circle (ch2_s5_ring.py, copied verbatim; its cell_bit replaces s2's) ---------
RING = "abcde"
RING_STATES = ["00011", "00110", "01100", "11000", "10001"]   # e d c b a, one per clock state
RING_R = 1.75          # circle radius (cell centres)
RING_CELL = 0.85       # square cell side
CIRCLE_C = np.array([-3.6, 0.2, 0.0])
TABLE_C = np.array([3.4, 0.45, 0.0])


def _dirn(i, n=5):
    a = PI / 2 - TAU * i / n
    return np.array([np.cos(a), np.sin(a), 0.0])


def bit_color(b):
    return GOLD if int(b) else DIM


def ring_cell_style(box, bit):
    """s2's cell look (ch2_s2_sliding.py SlideRow): BLUE border; a cell holding a 1 lights faintly
    GOLD, otherwise BG fill. bit None = empty cell."""
    box.set_stroke(BLUE, 4)
    return box.set_fill(GOLD, 0.22) if bit is not None and int(bit) else box.set_fill(BG, 1)


def cell_bit(b, size=44):
    """What a cell holds (s2's cell_bit): a GOLD travelling 1, or a DIM 0."""
    return Mono("1", size, color=GOLD) if int(b) else Mono("0", size, color=DIM)


def ring_circle(center=CIRCLE_C, R=RING_R, bits=None):
    """Five square flip-flop cells a..e clockwise from 12 o'clock round a circle.

    .boxes[i] (RoundedRectangle), .labels[i] (GREEN italic letter, just outside its cell),
    .arrows[0..3] a->b->c->d->e (FG), .close e->a (YELLOW), .digits[i] (T 40, only if `bits` is a
    string in a..e order), .pos(i) cell centre, .center, .R. bits=None leaves the cells empty."""
    center = np.array(center, dtype=float)
    pos = [center + R * _dirn(i) for i in range(5)]
    boxes, labels, digits, arrows = [], [], [], []
    for i in range(5):
        b = RoundedRectangle(corner_radius=0.12, width=RING_CELL, height=RING_CELL).move_to(pos[i])
        ring_cell_style(b, None if bits is None else bits[i])
        boxes.append(b)
        labels.append(T(RING[i], 38, color=GREEN).move_to(center + (R + 0.75) * _dirn(i)))
        if bits is not None:
            digits.append(cell_bit(bits[i], 40).move_to(pos[i]))
    for i in range(5):
        p, q = pos[i], pos[(i + 1) % 5]
        u = (q - p) / np.linalg.norm(q - p)
        arrows.append(Arrow(p + 0.56 * u, q - 0.56 * u, buff=0, color=YELLOW if i == 4 else FG,
                            stroke_width=4 if i == 4 else 3, tip_length=0.2,
                            max_tip_length_to_length_ratio=0.4))
    g = VGroup(*arrows, *boxes, *labels, *digits)
    g.boxes, g.labels, g.digits, g.arrows, g.close = boxes, labels, digits, arrows[:4], arrows[4]
    g.pos = lambda i: pos[i]
    g.center, g.R = center, R
    return g



# ---- {next}: s6's ring_circuit (ch2_s6_nologic.py, copied verbatim) -----------------------------
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
    top = min(a.get_end()[1] for a in arrows) - 0.1 * k
    return [T(w, 30, GOLD).move_to(a.get_end()).align_to(_p(0, top), UP) for w, a in zip(words, arrows)]


# ---- the two chips ------------------------------------------------------------------------------------
CHIP_W, CHIP_H = 6.0, 4.4
L_C, R_C = _p(-3.6, -0.1), _p(3.6, -0.1)


# =============================================================================================
# recap grid
# =============================================================================================
COL_X = (-4.5, 0.0, 4.5)
SLOT_TOP = (2.95, -0.3)
SLOT_W, SLOT_H = 4.2, 3.1
VIS_W, VIS_H = 3.9, 2.05
CAP = 28
VEIL = 0.45


def slot(i):
    """(x, top) of slot i: 0-2 top row, 3-5 bottom row."""
    return COL_X[i % 3], SLOT_TOP[i // 3]


def slot_frame(i):
    x, top = slot(i)
    return (RoundedRectangle(corner_radius=0.15, width=SLOT_W, height=SLOT_H)
            .set_stroke(DIM, 2, opacity=0.45).move_to(_p(x, top - SLOT_H / 2)))


def vis_center(i):
    x, top = slot(i)
    return _p(x, top - 1.18)


def fit(m, ctr, w=VIS_W, h=VIS_H):
    s = min(w / m.width, h / m.height)
    m.scale(s).move_to(ctr)
    return s


def caption(i, lines, **kw):
    x, top = slot(i)
    g = VGroup(*[T(s, CAP, **kw) for s in lines]).arrange(DOWN, buff=0.1)
    return g.move_to(_p(x, 0)).align_to(_p(0, top - 2.3), UP)


def veil(*mobs):
    g = VGroup(*mobs)
    return (Rectangle(width=g.width + 0.3, height=g.height + 0.3).set_stroke(width=0)
            .set_fill(BG, VEIL).move_to(g).set_z_index(20))


class PanelRow(SlideRow):
    """s2's SlideRow, shrunk: step() slides by the row's own (scaled) pitch, bits at BIT size."""
    BIT = 30

    def zeros(self):
        self.items = [cell_bit(0, self.BIT).move_to(c).set_z_index(2) for c in self.cells]
        return self.items

    def step(self, new):
        pitch = self.cells[1].get_x() - self.cells[0].get_x()
        old = self.items
        g = cell_bit(new, self.BIT).move_to(self.cells[2]).set_z_index(2)
        anims = [FadeOut(old[0], shift=pitch * LEFT),
                 old[1].animate.shift(pitch * LEFT),
                 old[2].animate.shift(pitch * LEFT),
                 FadeIn(g, shift=pitch * LEFT)]
        self.items = [old[1], old[2], g]
        self.bits = self.bits[1:] + [new]
        for cell, b in zip(self.cells, self.bits):
            anims.append(cell.animate.set_fill(GOLD if b else BG, 0.22 if b else 1))
        return anims


TRACE_Y = -3.3
TRACE_X = (-5.0, 6.0)


class Recap(NarratedScene):
    def construct(self):
        self.panels = []
        self.clip1()
        self.clip2()
        self.end_card()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def dim_previous(self):
        out = []
        for t in self.panels:
            if not getattr(t, "veiled", False):
                t.veiled = True
                out.append(FadeIn(veil(t)))
        return out

    # -- c2.recap.1: r1 sliding cells, r2 waveforms, r3 table, r4 circuit --------------------------
    def clip1(self):
        with self.say("c2.recap.1") as c:
            head = T("Recap", 40).move_to(_p(0, 3.4))
            frames = [slot_frame(i) for i in range(6)]
            self.play(*appear(head, shift=None), *[FadeIn(f) for f in frames],
                      run_time=min(1.2, c.until("r1")))  # early: the scene's heading

            # r1: two GOLD 1s slide through c b a
            c.wait_until("r1")
            row = PanelRow(ORIGIN)
            fit(row, vis_center(0) + 0.1 * DOWN)
            for n in row.names:
                n.scale(1.4)
            bits = row.zeros()
            cap1 = caption(0, ["two 1s slide through", "three flip-flops"], t2c={"1s": GOLD})
            self.play(FadeIn(row), *[FadeIn(b) for b in bits], run_time=0.8)
            for new in (1, 1):
                self.play(*row.step(new), run_time=0.8)
                self.wait(0.3)
            self.play(*row.step(0), *appear(cap1, shift=None), run_time=min(1.0, c.until("r2", floor=0.5)))
            self.panels.append(VGroup(row, *row.items, cap1))

            # r2: the same waveform in three phases, all outlined
            c.wait_until("r2")
            p, x0 = 0.33, COL_X[1] - 1.45
            vc = vis_center(1)
            ys = {"a": vc[1] + 0.62, "b": vc[1], "c": vc[1] - 0.62}
            seq = {"a": [0, 1, 1, 0, 0], "b": [0, 0, 1, 1, 0], "c": [0, 0, 0, 1, 1]}
            labs = [T(n, 32, color=GREEN).next_to(_p(x0, ys[n]), LEFT, buff=0.22) for n in "abc"]
            waves = [bit_wave(seq[n] * 2, p, h=0.4).shift(_p(x0, ys[n])) for n in "abc"]
            self.play(*self.dim_previous(), *appear(*labs, shift=None, lag=0.15),
                      *[time_span(Create(w, rate_func=linear), 0.3 * i, 0.3 * i + 1.4) for i, w in enumerate(waves)],
                      run_time=2.0)
            c.wait_until("any of them")
            outlines = [SurroundingRectangle(w, color=GREEN, buff=0.08, stroke_width=3) for w in waves]
            cap2 = caption(1, ["same waveform,", "any phase"])
            self.play(*[time_span(GrowFromCenter(o), 0.2 * i, 0.2 * i + 0.9) for i, o in enumerate(outlines)],
                      run_time=1.3)
            self.play(*appear(cap2, shift=None), run_time=min(1.0, c.until("r3", floor=0.5)))
            self.panels.append(VGroup(*labs, *waves, *outlines, cap2))

            # r3: s3's table, current a and next b' boxed, D_b = a
            c.wait_until("r3")
            tab = slide_table()
            fit(tab, vis_center(2) + 0.75 * LEFT, h=VIS_H)
            eq = MathTex("D_b", "=", "a", font_size=44)
            eq[0].set_color(BLUE)
            eq[2].set_color(GREEN)
            eq.move_to(_p(COL_X[2] + 1.35, vis_center(2)[1]))
            cap3 = caption(2, ["matching columns", "are wires"])
            self.play(*self.dim_previous(), FadeIn(tab), run_time=1.0)  # early: the panel's table, shown whole
            c.wait_until("matches")
            gbox, bbox = col_box(tab, 0, 2, GREEN), col_box(tab, 1, 1, BLUE)
            self.play(FadeIn(gbox), time_span(FadeIn(bbox), 0.3, 1.0), run_time=1.0)
            c.wait_until("just a wire")
            self.play(*appear(eq, shift=None), *appear(cap3, shift=None),
                      run_time=min(1.0, c.until("r4", floor=0.5)))
            self.panels.append(VGroup(tab, gbox, bbox, eq, cap3))

            # r4: s4's circuit, its one AND gate lit
            c.wait_until("r4")
            circ = sliding_circuit()
            fit(circ, vis_center(3))
            cap4 = caption(3, ["one AND gate"])
            self.play(*self.dim_previous(), FadeIn(circ), run_time=0.9)  # early: the panel's circuit, shown whole
            c.wait_until("just one")
            g = circ.gate
            self.play(*[m.animate.set_stroke(YELLOW) for m in g.strokes()], *flash([g]),
                      *appear(cap4, shift=None), run_time=min(1.0, c.until(floor=0.5)))
            self.panels.append(VGroup(circ, cap4))

    # -- c2.recap.2: r5 ring, r6 scoreboard, {next} the ring switched on ------------------------------
    def clip2(self):
        with self.say("c2.recap.2") as c:
            # r5: the ring of five, the GOLD pair stepping round
            ring = ring_circle(ORIGIN, RING_R, bits="11000")
            fit(ring, vis_center(4))
            ctr = np.mean([b.get_center() for b in ring.boxes], axis=0)
            R = np.linalg.norm(ring.boxes[0].get_center() - ctr)
            tokens = list(ring.digits)
            bits = [1, 1, 0, 0, 0]

            def step():
                anims = []
                for i, tok in enumerate(tokens):
                    th0 = PI / 2 - TAU * i / 5

                    def upd(m, a, th0=th0):
                        th = th0 - a * TAU / 5
                        m.move_to(ctr + R * np.array([np.cos(th), np.sin(th), 0]))
                    anims.append(UpdateFromAlphaFunc(tok, upd))
                new_bits = [bits[(i - 1) % 5] for i in range(5)]
                for i in range(5):
                    tgt = ring.boxes[i].copy()
                    ring_cell_style(tgt, new_bits[i])
                    anims.append(Transform(ring.boxes[i], tgt))
                bits[:] = new_bits
                tokens[:] = [tokens[(i - 1) % 5] for i in range(5)]
                return anims

            cap5 = caption(4, ["a ring of five:", "no gates"])
            self.play(*self.dim_previous(), FadeIn(ring), run_time=1.0)  # early: the panel's ring, shown whole
            c.wait_until("copies")
            self.play(*step(), run_time=1.0)
            self.wait(0.4)
            self.play(*step(), run_time=1.0)
            c.wait_until("no gates")
            self.play(*appear(cap5, shift=None), *flash([ring.close], color=YELLOW),
                      run_time=min(1.0, c.until("r6", floor=0.5)))
            self.panels.append(VGroup(ring, cap5))

            # r6: s7's scoreboard with its GOLD arrows
            c.wait_until("r6")
            sb = board3()
            arrows = sb_arrows(sb)
            labs = sb_arrow_labels(sb, arrows)
            fit(VGroup(sb, *arrows, *labs), vis_center(5))
            cap6 = caption(5, ["more flip-flops,", "less logic"])
            self.play(*self.dim_previous(), FadeIn(sb), *appear(cap6, shift=None),  # early: the panel's board and line, shown whole
                      run_time=1.0)
            c.wait_until("flip-flops")
            self.play(*[GrowArrow(a) for a in arrows], *appear(*labs, lag=0.3, shift=None), run_time=1.2)
            self.panels.append(VGroup(sb, *arrows, *labs, cap6))

            # {next}: the panels clear; the ring circuit returns, switched on
            c.wait_until("next")
            rc = self.rc = ring_circuit()
            self.play(*during([FadeOut(m) for m in self.mobjects], 0.0, 0.45),
                      *during([FadeIn(rc)], 0.5, 1.0), run_time=1.5)
            out_l = T("output", 30, GREEN)
            out_l.move_to(_p(TRACE_X[0] - 0.25, TRACE_Y), aligned_edge=RIGHT)
            trace = Line(_p(TRACE_X[0], TRACE_Y), _p(TRACE_X[1], TRACE_Y)).set_stroke(GREEN, 4)
            self.play(*appear(out_l, shift=None), run_time=0.6)
            rt = max(1.5, c.until("nothing happens") + 0.6)
            self.play(Create(trace, rate_func=linear), *self.ticks(rt), run_time=rt)
            q = self.q = T("?", 64, RED).move_to(_p(0.5, -2.75))
            self.play(*appear(q, shift=None), run_time=0.8)

            # {why}: the "?" pulses
            c.wait_until("why")
            self.play(FlashAround(q, color=RED, time_width=1.5), q.animate(rate_func=there_and_back).scale(1.25),
                      *self.ticks(1.2), run_time=min(1.2, c.until(floor=0.6)))

    def ticks(self, rt, period=1.2):
        """CLK pulses along the bus and every clock pin, one per `period` s, within rt s."""
        rc = self.rc
        paths = [rc.clk] + [f.clk_w for f in rc.ffs]
        out = []
        t = 0.0
        while t + 0.8 <= rt + 1e-6:
            out += [time_span(VShowPassingFlash(m.copy().set_stroke(YELLOW, 8), time_width=0.6), t, t + 0.8)
                    for m in paths]
            t += period
        return out

    def end_card(self):
        part3 = T("Part 3 · Starting in a used state", 40).move_to(_p(0, 3.2))
        self.play(*appear(part3), *self.ticks(1.2), run_time=1.2)
        for _ in range(6):
            self.play(*self.ticks(1.2), run_time=1.2)
