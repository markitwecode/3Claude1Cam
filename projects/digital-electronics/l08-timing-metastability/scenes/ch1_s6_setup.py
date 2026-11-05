"""Chapter 1, scene 6: the set-up constraint and the lecture's budget bar. Clips c1.setup.1 – c1.setup.5.

Opens on ch1_s5's final timing diagram (its `# ===` kit copied verbatim, rebuilt by s5_diagram()).
The counter block (second ruler pair) is ch1_s1_hook's, copied verbatim; here it is shrunk to COUNTER_SC.
The third ruler pair is THE lecture's budget bar, owned here (ch1_s7, ch1_s8, ch3, ch4, ch7 copy it).
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


# ============================================================================
# Data-sheet timing-diagram kit (shared spec: ch1_s2/s3, ch2–ch7 copy it)
# ============================================================================
WAVE_W = 4          # stroke of every trace
ROW_H = 0.8         # high-to-low height of a row
SLOPE = 0.35        # horizontal run of a sloped edge
GUIDE_W = 1.5       # thin grey guides
DIM_W = 3           # dimension arrows


def clock_wave(x0, x1, y, edges, h=ROW_H, slope=SLOPE, color=YELLOW, start_low=True):
    """One polyline clock trace from x0 to x1 centred on y; `edges` = x centres of every edge
    (alternating rise/fall from the start level). slope=0 gives the square L6 style."""
    lo, hi = y - h / 2, y + h / 2
    level = lo if start_low else hi
    pts = [np.array([x0, level, 0])]
    for xc in edges:
        other = hi if level == lo else lo
        pts.append(np.array([xc - slope / 2, level, 0]))
        pts.append(np.array([xc + slope / 2, other, 0]))
        level = other
    pts.append(np.array([x1, level, 0]))
    wave = VMobject().set_points_as_corners(pts)
    wave.set_stroke(color, WAVE_W)
    return wave


def bus(x0, x1, y, crossings, h=ROW_H, color=BLUE):
    """A data row: two parallel lines (high and low) from x0 to x1 that swap through an X on each
    interval (a, b) in `crossings` (left to right; touching intervals make a hatched run).
    Returns a VGroup ordered left to right, with `.runs` (pairs of lines) and `.xs` (each X)."""
    lo, hi = y - h / 2, y + h / 2
    g = VGroup()
    g.runs, g.xs = [], []
    cur = x0
    for a, b in list(crossings) + [(x1, x1)]:
        if a - cur > 1e-3:
            run = VGroup(Line([cur, hi, 0], [a, hi, 0]), Line([cur, lo, 0], [a, lo, 0]))
            run.set_stroke(color, WAVE_W)
            g.add(run)
            g.runs.append(run)
        if b - a > 1e-3:
            x = VGroup(Line([a, hi, 0], [b, lo, 0]), Line([a, lo, 0], [b, hi, 0]))
            x.set_stroke(color, WAVE_W)
            g.add(x)
            g.xs.append(x)
        cur = b
    return g


def hatch(a, b, n):
    """n touching crossover intervals filling [a, b]: the settling run."""
    w = (b - a) / n
    return [(a + i * w, a + (i + 1) * w) for i in range(n)]


def guide(x, y_top, y_bot):
    """Thin grey vertical guide."""
    return Line([x, y_top, 0], [x, y_bot, 0]).set_stroke(DIM, GUIDE_W)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=44):
    """Dimension arrow: thin double-headed line from xa to xb at y, small tips, with a
    same-colour MathTex label above (UP) or below (DOWN). Returns VGroup(arrow, label)."""
    arr = DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.15)
    return VGroup(arr, lab)


def sweep_in(group, x0, x1):
    """Draw every line of `group` left to right, as if a pen swept from x0 to x1."""
    leaves = group.family_members_with_points()
    origs = [m.copy() for m in leaves]

    def upd(_, a):
        X = x0 + a * (x1 - x0)
        for leaf, orig in zip(leaves, origs):
            lx0, lx1 = orig.get_left()[0], orig.get_right()[0]
            if lx1 - lx0 < 1e-6:
                frac = 1.0 if X >= lx0 else 0.0
            else:
                frac = min(1.0, max(0.0, (X - lx0) / (lx1 - lx0)))
            if a >= 1:
                frac = 1.0
            leaf.pointwise_become_partial(orig, 0, frac)

    return UpdateFromAlphaFunc(group, upd)
# ============================================================================


# ---- ch1_s1_hook's counter block (verbatim) ----
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



# ---- this lecture's placement of the counter (ch1_s4 / ch1_s6 copy it) ----------------------
SC = 0.86                                  # whole circuit scale
BOTTOM_Y = -3.4                            # circuit bottom (clock source) on screen
READ_X, READ_Y = -3.3, 2.85                # readout row centre
TRAIL_X0, TRAIL_DX, TRAIL_N = 0.2, 0.8, 8  # trail slots: x = TRAIL_X0 + k * TRAIL_DX, at READ_Y
TAG_SIZE = 30


def hook_counter():
    """Returns (S, chains, src, M): L6's counter with LEDs and 1 Hz source, scaled SC and placed;
    M(p) maps an L6 screen point to this placement. Parts are separate mobjects: show them with
    counter_parts(S, chains, src)."""
    S = sync_counter()
    chains = [led_chain(i, on=True) for i in range(3)]
    src, _hz = clock_source()
    W = VGroup(S, *chains, *[ch.ohm for ch in chains], src)
    c0 = W.get_center()
    W.scale(SC)
    W.shift(np.array([0.0, BOTTOM_Y - W.get_bottom()[1], 0.0]) - np.array([W.get_center()[0], 0, 0]))
    c1 = W.get_center()
    # small labels back to their L6 on-screen size (>= 28), each about its own centre
    for m in [*[x for f in S.ffs for x in (f.d_l, f.q_l, f.qb_l)], *S.names]:
        m.scale(1 / SC)
    S.block_l.scale(1 / SC).next_to(S.block, UP, buff=0.13)
    for ch in chains:
        r = ch.ohm.get_right()
        ch.ohm.scale(1 / SC).move_to(r, aligned_edge=RIGHT)

    def M(p):
        return c1 + (np.array(p, dtype=float) - c0) * SC
    return S, chains, src, M


def counter_parts(S, chains, src):
    return [*S.all, *[m for ch in chains for m in (ch.res, ch.link, ch.led, ch.ohm)], src]


def freq_tag(text, S):
    return T(text, TAG_SIZE, YELLOW).next_to(S.clk_l, RIGHT, buff=0.3)


def readout(n, dec_color=GOLD):
    lab = MathTex(r"Q_2\,Q_1\,Q_0", font_size=40, color=GREEN)
    eq1 = MathTex("=", font_size=40)
    bits = Mono(f"{n:03b}", 44, GREEN)
    eq2 = MathTex("=", font_size=40)
    dec = T(str(n), 48, dec_color)
    VGroup(lab, eq1, bits, eq2, dec).arrange(RIGHT, buff=0.25).move_to(_p(READ_X, READ_Y))
    return lab, eq1, bits, eq2, dec


def trail_digit(v, color, k):
    return T(str(v), 42, color).move_to(_p(TRAIL_X0 + k * TRAIL_DX, READ_Y))


def _bits(n):
    return [(n >> i) & 1 for i in range(3)]      # [Q0, Q1, Q2]
# =============================================================================================


# ============================================================================
# THE lecture's budget bar (owned by ch1_s6; ch1_s7, ch1_s8, ch3, ch4, ch7 copy this block)
# ============================================================================
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
# ============================================================================


# ---- ch1_s5's final diagram, same numbers ----
YC, YQ, YD = 2.1, 0.4, -1.3
X0, X1 = -4.6, 6.3
E1, FALL, E2 = -2.8, 0.7, 4.2
XQ = -1.6
LAB_X = -5.9
XS = 3.5          # D1 has settled: the end of its last X
ARR_Y = -2.4      # bottom row of dimension arrows

# the bar in the diagram's proportions (t_pc 1.2, t_pd 5.1, t_su 0.7; T_c 7.0)
SEGS = [("t_{pc}", PINK, XQ - E1), ("t_{pd}", PURPLE, XS - XQ), ("t_{su}", GOLD, E2 - XS)]
TC_LEN = E2 - E1
SHORT_LEN = 5.5   # clip 5's too-short period: t_pd's tail and all of t_su hang past it
BAR_X0 = -3.3
COUNTER_SC = 0.6
EQ_X, EQ_Y1, EQ_Y2 = 4.3, 0.05, -0.8    # clip 5: where the shrunk results wait at the right


def s5_diagram():
    clk = clock_wave(X0, X1, YC, [E1, FALL, E2], color=YELLOW)
    clk_lab = T("CLK", 40, YELLOW).move_to([LAB_X, YC, 0])
    g1, g2 = guide(E1, 3.25, -2.6), guide(E2, 3.25, -2.6)
    tc = dim_arrow(E1, E2, 3.05, YELLOW, "T_c")
    q0 = bus(X0, X1, YQ, [(XQ - 0.2, XQ + 0.2)], color=GREEN)
    q0_lab = MathTex("Q_0", font_size=48, color=GREEN).move_to([LAB_X, YQ, 0])
    gq = guide(XQ, YQ + 0.6, -2.6)
    tpc = dim_arrow(E1, XQ, ARR_Y, PINK, "t_{pc}", label_dir=DOWN)
    d1 = bus(X0, X1, YD, hatch(FALL, 2.7, 4) + [(3.1, 3.5)], color=BLUE)
    d1_lab = MathTex("D_1", font_size=48, color=BLUE).move_to([LAB_X, YD, 0])
    return clk_lab, clk, g1, g2, tc, q0_lab, q0, gq, tpc, d1_lab, d1


def x_mark(a, b, y, color, h=ROW_H, width=WAVE_W):
    lo, hi = y - h / 2, y + h / 2
    return VGroup(Line([a, hi, 0], [b, lo, 0]), Line([a, lo, 0], [b, hi, 0])).set_stroke(color, width)


class Setup(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c1.setup.1
    def clip1(self):
        with self.say("c1.setup.1") as c:
            parts = s5_diagram()
            (self.clk_lab, self.clk, g1, g2, self.tc, q0_lab, q0, gq,
             self.tpc, d1_lab, self.d1) = parts
            d1 = self.d1
            self.play(*[FadeIn(m) for m in parts], run_time=1.0)  # early: s5's diagram returns whole
            self.D = VGroup(*parts)
            settle(self, self.D)
            # the question: every crossing of D1 in turn
            self.play(*[time_span(FlashAround(x, color=BLUE, buff=0.06), 0.25 * i, 0.25 * i + 0.9)
                        for i, x in enumerate(d1.xs)],
                      run_time=min(0.25 * (len(d1.xs) - 1) + 0.9, c.until("the last one")))

            # {latest}: the last one brightens; a guide drops from it; t_su to the next edge
            c.wait_until("the last one")
            last = d1.xs[-1]
            self.gs = guide(XS, YD + 0.4, -2.6)
            self.play(last.animate.set_stroke(YELLOW, 6), FlashAround(last, color=YELLOW, buff=0.08),
                      run_time=1.0)
            self.play(Create(self.gs), run_time=0.9)
            c.wait_until("set-up time")
            self.tsu = dim_arrow(XS, E2, ARR_Y, GOLD, "t_{su}", label_dir=DOWN)
            self.play(GrowFromCenter(self.tsu[0]), *appear(self.tsu[1]), run_time=1.4)

            # {earlier}: GREEN ticks over the earlier crossings
            c.wait_until("earlier")
            self.ticks = [check_mark(GREEN).scale(0.6).move_to([x.get_center()[0], YD + 0.72, 0])
                          for x in d1.xs[:-1]]
            self.play(*appear(*self.ticks, shift=0.15 * DOWN, lag=0.25), run_time=1.5)

            # {late}: a ghost X inside the t_su span, RED, crossed out
            c.wait_until("later")
            self.ghost = x_mark(XS + 0.15, E2 - 0.15, YD, RED).set_stroke(opacity=0.6)
            self.cross = cross_mark(RED).move_to([(XS + E2) / 2, YD + 0.75, 0])
            self.play(FadeIn(self.ghost), run_time=1.0)
            self.play(*appear(self.cross, shift=None), run_time=0.8)

    # ------------------------------------------------------------------ c1.setup.2
    def clip2(self):
        with self.say("c1.setup.2") as c:
            # {sum}: t_pd fills in from Q0's guide to D1's last X
            self.tpd = dim_arrow(XQ, XS, ARR_Y, PURPLE, "t_{pd}", label_dir=DOWN)
            self.play(*during(disappear(*self.ticks, self.ghost, self.cross), 0, 0.4),
                      *during([GrowFromCenter(self.tpd[0]), *appear(self.tpd[1])], 0.3, 1.0),
                      run_time=2.0)
            settle(self, self.D, add=[self.gs, self.tsu, self.tpd])

            # {tpc} {tpd} {tsu}: flashed in turn
            for arr, col, cue, nxt in ((self.tpc, PINK, "tpc", "tpd"), (self.tpd, PURPLE, "tpd", "tsu"),
                                       (self.tsu, GOLD, "tsu", "in the worst case")):
                c.wait_until(cue)
                self.play(FlashAround(arr, color=col, time_width=1.5, buff=0.1),
                          run_time=min(1.2, c.until(nxt)))

            # together they fill one period
            c.wait_until("in the worst case")
            row = Line([E1, ARR_Y, 0], [E2, ARR_Y, 0]).set_stroke(YELLOW, 7)
            top = Line([E1, 3.05, 0], [E2, 3.05, 0]).set_stroke(YELLOW, 7)
            self.play(VShowPassingFlash(top, time_width=0.6), VShowPassingFlash(row, time_width=0.6),
                      run_time=2.0)

            # {bar}: the diagram moves up; the three arrows lift out into the bar
            c.wait_until("bar")
            self.D.generate_target()
            self.D.target.scale(0.65).move_to([0.2, 0, 0]).to_edge(UP, buff=0.5)
            self.play(MoveToTarget(self.D), run_time=1.2)
            bar = budget_bar(SEGS, TC_LEN, x0=BAR_X0, y=-1.72)
            self.bar = bar
            arrows = (self.tpc, self.tpd, self.tsu)
            self.play(*[TransformFromCopy(a[0], s) for a, s in zip(arrows, bar.segs)], run_time=1.6)
            # the T_c arrow flashes; the outline grows in place from the bar's left end
            self.play(time_span(FlashAround(self.tc[0], color=YELLOW, time_width=1.5, buff=0.1), 0, 1.0),
                      time_span(GrowFromEdge(bar.outline, LEFT), 0.4, 1.4),
                      *during(appear(bar.tc, *bar.syms, shift=None, lag=0.1), 0.45, 1.0),
                      run_time=1.4)
            settle(self, bar)

            # {ineq}
            c.wait_until("ineq")
            ineq = MathTex("T_c", r"\ge", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", font_size=52)
            for i, col in ((0, YELLOW), (2, PINK), (4, PURPLE), (6, GOLD)):
                ineq[i].set_color(col)
            ineq.move_to([-1.3, -3.0, 0])
            self.ineq = ineq
            self.play(*appear(ineq, shift=None), run_time=1.2)

    # ------------------------------------------------------------------ c1.setup.3
    def clip3(self):
        bar = self.bar
        with self.say("c1.setup.3") as c:
            # {worst}: "max" under t_pc and t_pd
            m1 = T("max", 30, PINK).next_to(bar.segs[0], DOWN, buff=0.2)
            m2 = T("max", 30, PURPLE).next_to(bar.segs[1], DOWN, buff=0.2)
            c.wait_until("slowest")
            self.play(*appear(m1), run_time=1.0)
            c.wait_until("slowest", nth=1)
            self.play(*appear(m2), run_time=1.0)

            # {limit}: GREEN outline round the inequality
            c.wait_until("limit")
            box = SurroundingRectangle(self.ineq, color=GREEN, buff=0.2).set_stroke(GREEN, 3)
            lab = T("minimum clock period", 32, GREEN).next_to(box, RIGHT, buff=0.3)
            self.play(GrowFromCenter(box), run_time=1.0)
            c.wait_until(own_word=lab)
            self.play(*appear(lab), run_time=1.0)

            # {short}: part 2 gets the shortest delays
            c.wait_until("short")
            p2 = T("part 2: the shortest delays", 28, DIM, slant=ITALIC)
            p2.next_to(m2, RIGHT, buff=0.9).align_to(m2, DOWN)
            self.play(*appear(p2), run_time=1.0)

    # ------------------------------------------------------------------ c1.setup.4
    def clip4(self):
        bar, ineq = self.bar, self.ineq
        with self.say("c1.setup.4") as c:
            # {example}: the diagram clears; the bar and the rule move up
            dy = 2.3 - bar.outline.get_center()[1]
            c.wait_until("real numbers")
            sweep_clear(self, bar.animate.shift(dy * UP), ineq.animate.move_to([0.2, -0.75, 0]),
                        keep=[bar, ineq], run_time=min(1.8, c.until("these flip-flops")))

            ff = T("flip-flops: from the data sheet", 30, DIM).move_to([0.2, 0.35, 0])
            n02 = T("0.2 ns", 34, GOLD).next_to(bar.segs[0], DOWN, buff=0.2)
            n47 = T("4.7 ns", 34, GOLD).next_to(bar.segs[1], DOWN, buff=0.2)
            n01 = T("0.1 ns", 34, GOLD).next_to(bar.segs[2], DOWN, buff=0.2)
            l02 = Line(n02.get_bottom() + 0.1 * DOWN, ff.get_top() + [-2.4, 0.1, 0]).set_stroke(DIM, 2)
            l01 = Line(n01.get_bottom() + 0.1 * DOWN, ff.get_top() + [2.5, 0.1, 0]).set_stroke(DIM, 2)
            logic = T("logic", 30, DIM).next_to(n47, DOWN, buff=0.2)

            c.wait_until(own_word=ff, cue="these flip-flops")
            self.play(*appear(ff), run_time=1.0)
            c.wait_until("zero point two")
            self.play(*appear(n02), Create(l02), run_time=1.2)
            c.wait_until("zero point one")
            self.play(*appear(n01), Create(l01), run_time=1.2)

            # {logic}
            c.wait_until("logic")
            self.play(*appear(logic), run_time=0.9)
            c.wait_until("four point seven")
            self.play(*appear(n47), run_time=1.0)

            # {add}
            c.wait_until("add")
            add = MathTex("T_c", r"\ge", "0.2", "+", "4.7", "+", "0.1", "=", r"5.0\ \text{ns}", font_size=52)
            add[0].set_color(YELLOW)
            for i in (2, 4, 6, 8):
                add[i].set_color(GOLD)
            add.move_to([0.2, -0.75, 0])
            self.play(*edit(ineq, add), run_time=2.0)

            # {freq}
            c.wait_until("freq")
            fq = MathTex("f_c", r"\le", r"\frac{1}{5.0\ \text{ns}}", "=", r"200\ \text{MHz}", font_size=52)
            fq[0].set_color(YELLOW)
            fq[4].set_color(GOLD)
            fq.move_to([0.2, -2.4, 0])
            tick = check_mark(GREEN).next_to(fq, RIGHT, buff=0.4)
            self.play(*appear(fq, shift=None), run_time=1.2)
            self.play(*appear(tick, shift=None), run_time=0.7)
            self.add_eq, self.fq, self.tick = add, fq, tick

    # ------------------------------------------------------------------ c1.setup.5
    def clip5(self):
        bar = self.bar
        with self.say("c1.setup.5") as c:
            # {hook}: the counter returns small, with its RED trail
            S, chains, src, M = hook_counter()
            for f in S.ffs:                       # shrunk to an icon: its labels would be unreadable
                f.remove(f.d_l, f.q_l, f.qb_l)
            words = {id(m) for m in [*S.names, S.clk_l, *S.q_labels, *S.xor_labels, S.block_l,
                                     *S.block_labels, *[ch.ohm for ch in chains]]}
            cparts = [m for m in counter_parts(S, chains, src) if id(m) not in words]
            cg = VGroup(*cparts)
            cg.scale(COUNTER_SC).move_to([-3.0, 0, 0])
            cg.shift((-3.45 - cg.get_bottom()[1]) * UP)
            ty = cg.get_center()[1]
            ff2_lab = T("FF2", 28, FG).next_to(S.ffs[2].box, UP, buff=0.12)
            cparts.append(ff2_lab)
            trail = [T(str(v), 42, col).move_to([1.4 + 0.8 * k, ty, 0])
                     for k, (v, col) in enumerate(((3, GOLD), (0, RED), (5, RED), (2, RED), (7, RED)))]
            for m in (self.add_eq, self.fq, self.tick):
                m.generate_target().scale(0.6)
            self.add_eq.target.move_to([EQ_X, EQ_Y1, 0])
            pair = VGroup(self.fq.target, self.tick.target)
            self.tick.target.next_to(self.fq.target, RIGHT, buff=0.25)
            pair.move_to([EQ_X, EQ_Y2, 0])
            sweep_clear(self, *[time_span(FadeIn(m), 0.6, 1.6) for m in cparts],
                        *[time_span(FadeIn(d), 0.9 + 0.1 * k, 1.6) for k, d in enumerate(trail)],
                        # the 5.0 ns and 200 MHz results stay up, smaller, at the right
                        *during([MoveToTarget(m) for m in (self.add_eq, self.fq, self.tick)], 0.3, 1.0),
                        keep=[bar, self.add_eq, self.fq, self.tick], run_time=1.6)

            # {tooshort}: a shorter period; the segments no longer fit
            c.wait_until("tooshort")
            short = budget_bar(SEGS, SHORT_LEN, x0=BAR_X0, y=1.0, syms=False)
            self.play(*[TransformFromCopy(a, b) for a, b in zip(bar.segs, short.segs)], run_time=1.4)
            # thin YELLOW ticks at each bar's right end: the old period's end, the new one's
            x_old, x_new = bar.outline.get_right()[0], short.outline.get_right()[0]
            y_b, y_s = bar.outline.get_center()[1], short.outline.get_center()[1]
            tick_old = DashedLine([x_old, y_b + 0.4, 0], [x_old, y_s - 0.4, 0], dash_length=0.08
                                  ).set_stroke(YELLOW, 2).set_z_index(2)
            tick_new = Line([x_new, y_s + 0.4, 0], [x_new, y_s - 0.4, 0]
                            ).set_stroke(YELLOW, 3).set_z_index(2)
            self.play(GrowFromEdge(short.outline, LEFT), *appear(short.tc, shift=None),
                      FadeIn(tick_old), time_span(FadeIn(tick_new), 0.6, 1.1),
                      run_time=min(1.1, c.until("stale")))
            # everything past the shorter period's end (t_pd's tail and all of t_su) turns RED
            over_w = short.segs[-1].get_right()[0] - x_new
            over = Rectangle(width=over_w, height=BAR_H).set_stroke(width=0).set_fill(RED, BAR_FILL)
            over.move_to([x_new + over_w / 2, y_s, 0]).set_z_index(0.5)
            self.play(FadeIn(over),
                      FlashAround(over, color=RED, time_width=1.5, buff=0.08),
                      run_time=min(1.0, c.until("stale")))

            # {stale}: D2 still flickering as the edge arrives; FF2 flashes RED
            c.wait_until("stale")
            self.play(*disappear(self.add_eq, self.fq, self.tick), run_time=0.8)
            bo = S.block_out

            def flick(m, a):
                m.set_stroke(BLUE if a >= 1 or int(a * 10) % 2 else RED)

            bus_p, _ = S.clk_paths()
            bus_p[0].set_stroke(width=6)
            self.play(UpdateFromAlphaFunc(bo, flick),
                      *during([VShowPassingFlash(bus_p[0], time_width=0.8)], 0.55, 1.0), run_time=2.2)
            ff2 = S.ffs[2]
            self.play(FlashAround(ff2.box, color=RED, time_width=1.5, buff=0.08),
                      ff2.box.animate.set_stroke(RED), FlashAround(trail[-1], color=RED, buff=0.1),
                      run_time=1.3)
