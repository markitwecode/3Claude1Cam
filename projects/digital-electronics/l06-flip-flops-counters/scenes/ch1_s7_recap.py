"""Chapter 1, scene 7: the catch (the latch responds the whole time EN = 1), the recap tiles, and
next time's flip-flop. Clips c1.recap.1 – c1.recap.3."""
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



# =============================================================================================
# Chapter 1 gate drawings (owned here; s3–s7 copy this block verbatim).
#   Wires: neutral WIRE (FG) = value not shown; ON (GREEN, bright) = 1; OFF (DIM) = 0.
#   light(w, v) -> animation that lights a wire (or wire group) to logic value v.
#   Gates are VGroups with .body .bubble (or None) .num (or None), .inp(i) and .out() points
#   (they follow scaling/moving). Built at unit size; 1.2 tall.
# =============================================================================================
WIRE, ON, OFF = FG, GREEN, DIM
WIRE_W = 4
GATE_COLOR = BLUE


def _p(x, y):
    return np.array([x, y, 0.0])


def wire(*pts, color=WIRE):
    """Polyline wire through (x, y) points."""
    w = VMobject().set_points_as_corners([_p(*p) if len(p) == 2 else np.array(p) for p in pts])
    return w.set_stroke(color, WIRE_W)


def junction(x, y, color=WIRE):
    return Dot(_p(x, y), radius=0.07, color=color)


def wire_color(v):
    return ON if v else OFF


def light(w, v=None, color=None):
    """Animation: wire (or VGroup of wires and junction dots) to value v (1 bright, 0 dim),
    or to `color` (e.g. WIRE for neutral)."""
    return w.animate.set_color(color if color is not None else wire_color(v))


class Gate(VGroup):
    def __init__(self, body, ins, out, bubble=None, num=None, num_at=(-0.1, 0.0), color=GATE_COLOR):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body, self.bubble = body, bubble
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body)
        if bubble is not None:
            bubble.set_stroke(color, 4).set_fill(BG, 1)
            self.add(bubble)
        self.num = None
        if num is not None:
            self.num = T(str(num), size=28, color=DIM).move_to(_p(*num_at))
            self.add(self.num)
        self.add(*self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()


def nor_gate(num=None, color=GATE_COLOR):
    """Distinctive-shape NOR (OR body + output bubble), 1.6 wide x 1.2 tall, centred at ORIGIN.
    inp(0) top input (y +0.3), inp(1) bottom (y -0.3), out() right of the bubble (0.9, 0)."""
    x0 = -0.7
    b = VMobject()
    b.start_new_path(_p(x0, 0.6))
    b.add_cubic_bezier_curve_to(_p(0.0, 0.6), _p(0.45, 0.35), _p(0.7, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.45, -0.35), _p(0.0, -0.6), _p(x0, -0.6))
    b.add_cubic_bezier_curve_to(_p(x0 + 0.25, -0.2), _p(x0 + 0.25, 0.2), _p(x0, 0.6))
    bubble = Circle(radius=0.1).move_to(_p(0.8, 0))
    return Gate(b, [(-0.56, 0.3), (-0.56, -0.3)], (0.9, 0.0), bubble=bubble, num=num, color=color)


def and_gate(num=None, color=GATE_COLOR):
    """AND (flat back, round front), 1.3 wide x 1.2 tall, centred near ORIGIN.
    inp(0) top (-0.7, 0.3), inp(1) bottom (-0.7, -0.3), out() (0.6, 0)."""
    k = 0.5523 * 0.6
    b = VMobject()
    b.start_new_path(_p(-0.7, 0.6))
    b.add_line_to(_p(0.0, 0.6))
    b.add_cubic_bezier_curve_to(_p(k, 0.6), _p(0.6, k), _p(0.6, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.6, -k), _p(k, -0.6), _p(0.0, -0.6))
    b.add_line_to(_p(-0.7, -0.6))
    b.add_line_to(_p(-0.7, 0.6))
    return Gate(b, [(-0.7, 0.3), (-0.7, -0.3)], (0.6, 0.0), num=num, num_at=(-0.15, 0.0), color=color)


def not_gate(color=GATE_COLOR):
    """Inverter: triangle + output bubble, pointing right. inp(0) (-0.4, 0), out() (0.46, 0)."""
    tri = Polygon(_p(-0.4, 0.35), _p(-0.4, -0.35), _p(0.3, 0.0))
    bubble = Circle(radius=0.08).move_to(_p(0.38, 0))
    return Gate(tri, [(-0.4, 0.0)], (0.46, 0.0), bubble=bubble, color=color)


class RSLatch(VGroup):
    """Slide p. 79 NOR RS latch. Parts:
    .g1 (top NOR, "1"), .g2 (bottom NOR, "2"), .gates
    .r .s            input wires (R into g1's top input, S into g2's bottom input)
    .q  = VGroup(.q_out, .fq, .q_dot)    Q node: g1 output line + feedback into g2's top input
    .qb = VGroup(.qb_out, .fqb, .qb_dot) Q-bar node: g2 output line + feedback into g1's bottom input
    .wires = {"r", "s", "q", "qb"} (light(latch.wires[k], v))
    .lab_r .lab_s (BLUE), .lab_q .lab_qb (GREEN), .labels
    Unscaled it is 5.4 wide x 3.6 tall, centred at ORIGIN (wire ends at x = +-2.2)."""

    def __init__(self, labels=True):
        super().__init__()
        g1, g2 = nor_gate(1).shift(1.2 * UP), nor_gate(2).shift(1.2 * DOWN)
        self.g1, self.g2, self.gates = g1, g2, VGroup(g1, g2)
        a1, b1, a2, b2 = g1.inp(0), g1.inp(1), g2.inp(0), g2.inp(1)
        o1, o2 = g1.out(), g2.out()
        xl, xr, xt, xf = -2.2, 2.2, 1.4, -1.2
        self.r = wire((xl, a1[1]), tuple(a1[:2]))
        self.s = wire((xl, b2[1]), tuple(b2[:2]))
        self.q_out = wire(tuple(o1[:2]), (xr, o1[1]))
        self.qb_out = wire(tuple(o2[:2]), (xr, o2[1]))
        self.fq = wire((xt, o1[1]), (xt, 0.5), (xf, -0.5), (xf, a2[1]), tuple(a2[:2]))
        self.fqb = wire((xt, o2[1]), (xt, -0.5), (xf, 0.5), (xf, b1[1]), tuple(b1[:2]))
        self.q_dot, self.qb_dot = junction(xt, o1[1]), junction(xt, o2[1])
        self.q = VGroup(self.q_out, self.fq, self.q_dot)
        self.qb = VGroup(self.qb_out, self.fqb, self.qb_dot)
        self.wires = {"r": self.r, "s": self.s, "q": self.q, "qb": self.qb}
        self.add(self.r, self.s, self.q, self.qb, g1, g2)
        self.lab_r = MathTex("R", font_size=48, color=BLUE).next_to(self.r.get_start(), LEFT, buff=0.15)
        self.lab_s = MathTex("S", font_size=48, color=BLUE).next_to(self.s.get_start(), LEFT, buff=0.15)
        self.lab_q = MathTex("Q", font_size=48, color=GREEN).next_to(self.q_out.get_end(), RIGHT, buff=0.15)
        self.lab_qb = MathTex(r"\overline{Q}", font_size=48, color=GREEN).next_to(
            self.qb_out.get_end(), RIGHT, buff=0.15)
        self.labels = VGroup(self.lab_r, self.lab_s, self.lab_q, self.lab_qb)
        if labels:
            self.add(*self.labels)

    def end(self, key):
        """Outer end point of a terminal wire: 'r', 's' (left ends), 'q', 'qb' (right ends)."""
        return {"r": self.r.get_start(), "s": self.s.get_start(),
                "q": self.q_out.get_end(), "qb": self.qb_out.get_end()}[key]


def rs_latch(labels=True):
    """The chapter's RS latch at unit scale, centred at ORIGIN (see RSLatch)."""
    return RSLatch(labels=labels)


# hero placement used in s2 (and where s3 opens): rs_latch().scale(LATCH_SCALE).move_to(LATCH_POS)
LATCH_SCALE = 1.15
LATCH_POS = _p(-3.4, 0.15)


class DLatch(VGroup):
    """Slide p. 86 D latch: D (bottom left) straight into the S-side AND, through an inverter into
    the R-side AND; EN enters between the ANDs and branches to both; the ANDs feed rs_latch().
    Parts: .latch (RSLatch, its R/S labels dropped), .and_r (top), .and_s (bottom), .inv,
    .d (VGroup: D wire to the S-AND + junction + riser to the inverter), .dn (inverter out -> R-AND),
    .en (VGroup: EN wire, junction, branches), .lab_d .lab_en (BLUE), .wires {"d","dn","en","r","s","q","qb"}.
    Default: 9.3 wide x 4.2 tall at scale 1, centred at ORIGIN."""

    def __init__(self):
        super().__init__()
        L = RSLatch(labels=True)
        L.remove(L.lab_r, L.lab_s)
        self.latch = L
        rs, ss = L.r.get_start(), L.s.get_start()
        ar = and_gate()
        ar.shift(rs - ar.out())
        as_ = and_gate()
        as_.shift(ss - as_.out())
        self.and_r, self.and_s = ar, as_
        xd, xj, xe, xin = -6.2, -5.4, -4.1, ar.inp(0)[0]
        yt, yb = ar.inp(0)[1], as_.inp(1)[1]
        inv = not_gate().move_to(_p(-4.6, yt))
        self.inv = inv
        d_main = wire((xd, yb), (xin, yb))
        d_rise = wire((xj, yb), (xj, yt), tuple(inv.inp(0)[:2]))
        self.d = VGroup(d_main, d_rise, junction(xj, yb))
        self.dn = wire(tuple(inv.out()[:2]), (xin, yt))
        en_main = wire((xd, 0.0), (xe, 0.0))
        en_br = wire((xin, ar.inp(1)[1]), (xe, ar.inp(1)[1]), (xe, as_.inp(0)[1]), (xin, as_.inp(0)[1]))
        self.en = VGroup(en_main, en_br, junction(xe, 0.0))
        self.lab_d = MathTex("D", font_size=48, color=BLUE).next_to(_p(xd, yb), LEFT, buff=0.15)
        self.lab_en = MathTex(r"\mathrm{EN}", font_size=44, color=BLUE).next_to(_p(xd, 0), LEFT, buff=0.15)
        self.wires = {"d": self.d, "dn": self.dn, "en": self.en, **L.wires}
        self.add(self.d, self.dn, self.en, ar, as_, inv, L, self.lab_d, self.lab_en)
        self.move_to(ORIGIN)


def d_latch():
    """The chapter's D latch at unit scale, centred at ORIGIN (see DLatch)."""
    return DLatch()



# =============================================================================================
# Scene-only helpers (grid_table copied from ch1_s2_rslatch.py)
# =============================================================================================
def grid_table(rows, xs, size=44, pitch=0.66, seps=(), colors=None):
    """rows: list of lists of strings ('$...' -> MathTex, else T). Column centres xs (or ('L', x)
    for left-aligned). Returns VGroup(header, *rows, lines) with .rows (incl. header), .lines."""
    out = []
    for i, row in enumerate(rows):
        cells = []
        for j, s in enumerate(row):
            col = (colors[i] if colors and colors[i] else FG)
            if s.startswith("$"):
                m = MathTex(s[1:], font_size=size, color=col)
            else:
                m = T(s, size=size * 0.82, color=col)
            x = xs[j]
            if isinstance(x, tuple):
                m.move_to(_p(x[1], -i * pitch), aligned_edge=LEFT)
                m.set_y(-i * pitch)
            else:
                m.move_to(_p(x, -i * pitch))
            cells.append(m)
        out.append(VGroup(*cells))
    top, bot = 0.4, -(len(rows) - 1) * pitch - 0.38
    lines = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 2) for x in seps])
    lines.add(Line(_p(out[0].get_left()[0] - 0.3, -pitch / 2),
                   _p(out[0].get_right()[0] + 0.3, -pitch / 2)).set_stroke(DIM, 2))
    g = VGroup(*out, lines)
    g.rows, g.lines = out, lines
    return g


def latch_symbol():
    """Slide p. 86 D-latch symbol: a tall BLUE box, D in on the left, Q out on the right, EN in
    from below through a small square on the box's bottom edge. Parts: .box .d_wire .lab_d
    .q_wire .lab_q .en_wire .square .lab_en; groups .d_part .q_part .en_part.
    6.2 wide x 4.2 tall at scale 1, box centred at ORIGIN (box 2.6 x 3.4)."""
    g = VGroup()
    box = Rectangle(width=2.6, height=3.4).set_stroke(GATE_COLOR, 4).set_fill(BG, 1)
    d_wire = wire((-3.1, 0.8), (-1.3, 0.8))
    q_wire = wire((1.3, 0.8), (3.1, 0.8))
    en_wire = wire((0, -2.5), (0, -1.7))
    square = Square(side_length=0.34).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -1.7))
    lab_d = MathTex("D", font_size=52, color=BLUE).move_to(_p(-0.85, 0.8))
    lab_q = MathTex("Q", font_size=52, color=GREEN).move_to(_p(0.85, 0.8))
    lab_en = MathTex(r"\mathrm{EN}", font_size=40, color=BLUE).move_to(_p(0, -0.95))
    g.box, g.d_wire, g.q_wire, g.en_wire, g.square = box, d_wire, q_wire, en_wire, square
    g.lab_d, g.lab_q, g.lab_en = lab_d, lab_q, lab_en
    g.d_part, g.q_part = VGroup(d_wire, lab_d), VGroup(q_wire, lab_q)
    g.en_part = VGroup(en_wire, square, lab_en)
    g.add(box, g.d_part, g.q_part, g.en_part)
    return g


# ---- clock (copied from ch1_s3_clock.py; originates in ch1_s1_hook.py) ----
class ClockWave(VGroup):
    """YELLOW clock square wave: starts low for half a period, then `periods` cycles (high half,
    low half). Flat levels, sharp vertical edges, small ▲ on every rising edge (▼ on falling
    edges if down_arrows). .wave (the line), .ups, .downs; .period; .rising_x(i)/.falling_x(i)
    give the current absolute x of edge i. Default 9.9 × 0.7, period 1.8, centred at ORIGIN."""

    def __init__(self, width=9.9, height=0.7, periods=5, color=YELLOW, up_arrows=True,
                 down_arrows=False, stroke_width=4, **kw):
        super().__init__(**kw)
        p = width / (periods + 0.5)
        x0, lo, hi = -width / 2, -height / 2, height / 2
        pts, self._rise, self._fall = [[x0, lo, 0]], [], []
        x = x0 + p / 2
        for _ in range(periods):
            pts += [[x, lo, 0], [x, hi, 0]]
            self._rise.append(x - x0)
            x += p / 2
            pts += [[x, hi, 0], [x, lo, 0]]
            self._fall.append(x - x0)
            x += p / 2
        pts.append([x0 + width, lo, 0])
        self.wave = VMobject().set_points_as_corners(pts).set_stroke(color, stroke_width)
        self.period, self._width = p, width
        tri = 0.11 * min(1.0, height / 0.7)
        self.ups = VGroup(*[Triangle().scale(tri).set_stroke(width=0).set_fill(color, 1)
                            .move_to([x0 + r, 0, 0]) for r in (self._rise if up_arrows else [])])
        self.downs = VGroup(*[Triangle().rotate(PI).scale(tri).set_stroke(width=0).set_fill(color, 1)
                              .move_to([x0 + f, 0, 0]) for f in (self._fall if down_arrows else [])])
        self.add(self.wave, self.ups, self.downs)

    def rising_x(self, i):
        return self.wave.get_left()[0] + self._rise[i] * self.wave.width / self._span()  # scale-safe

    def falling_x(self, i):
        return self.wave.get_left()[0] + self._fall[i] * self.wave.width / self._span()

    def _span(self):
        return self._width


def clock_wave(width=9.9, height=0.7, periods=5, color=YELLOW, up_arrows=True, down_arrows=False):
    return ClockWave(width, height, periods, color, up_arrows, down_arrows)


# ---- timing trace (copied from ch1_s4_andgate.py) ----
TRACE_H = 0.6


def trace(x0, w, toggles, yc, color, h=TRACE_H):
    """Timing trace in the clock_wave stroke style: starts low, toggles at the given fractions."""
    lo, hi = yc - h / 2, yc + h / 2
    lvl, pts = lo, [[x0, lo, 0]]
    for f in toggles:
        x = x0 + f * w
        pts += [[x, lvl, 0]]
        lvl = hi if lvl == lo else lo
        pts += [[x, lvl, 0]]
    pts.append([x0 + w, lvl, 0])
    return VMobject().set_points_as_corners(pts).set_stroke(color, 4)



# ---- wire hop (copied from ch1_s5_dlatch.py) ----
HOP_R = 0.16   # wire-hop radius where D's riser crosses EN


def add_hop(D, r=HOP_R):
    """Redraw D's riser (D.d[1]) with a semicircular hop, bulging LEFT, where it crosses the EN
    wire (centre = riser x, EN y; from (x, y_en - r) to (x, y_en + r)), so it doesn't read as joined."""
    riser = D.d[1]
    p0, p_top, p_inv = riser.get_start(), _p(riser.get_start()[0], D.dn.get_end()[1]), D.inv.inp(0)
    x, y = p0[0], D.en[0].get_start()[1]
    arc = [_p(x + r * np.cos(a), y + r * np.sin(a)) for a in np.linspace(-PI / 2, -3 * PI / 2, 17)]
    riser.set_points_as_corners([p0, *arc, p_top, p_inv])
    return D


# ---- s6's timing diagram, as it ends s6 (copied from ch1_s6_transparent.py) ----------------
EN_SEQ = [0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
D_SEQ = [1, 0, 0, 1, 1, 0, 0, 0, 1, 1]
Q_SEQ = [1, 1, 0, 1, 1, 0, 0, 0, 0, 0]
X0, STEP_W, TR_H = -4.4, 1.0, 0.6
ROW_Y = {"en": 1.15, "d": 0.0, "q": -1.15}      # s6's final rows (after its WAVE_UP shift)
TR_COL = {"en": BLUE, "d": BLUE, "q": GREEN}
SEQ = {"en": EN_SEQ, "d": D_SEQ, "q": Q_SEQ}


def trace_seg(key, k):
    vals, y = SEQ[key], ROW_Y[key]
    lv = lambda b: y + (TR_H / 2 if b else -TR_H / 2)  # noqa: E731
    x = X0 + k * STEP_W
    pts = []
    if k > 0 and vals[k] != vals[k - 1]:
        pts.append([x, lv(vals[k - 1]), 0])
    pts += [[x, lv(vals[k]), 0], [x + STEP_W, lv(vals[k]), 0]]
    return VMobject().set_points_as_corners(pts).set_stroke(TR_COL[key], 4)


def waveform():
    """s6's last shot: ({key: [10 segments]}, labels VGroup, band)."""
    segs = {k: [trace_seg(k, i) for i in range(10)] for k in SEQ}
    labs = VGroup(*[MathTex(s, font_size=44, color=TR_COL[k]).move_to(_p(X0 - 0.75, ROW_Y[k]))
                    for k, s in (("en", r"\mathrm{EN}"), ("d", "D"), ("q", "Q"))])
    band = Rectangle(width=5 * STEP_W, height=3.4).set_stroke(width=0).set_fill(YELLOW, 0.13)
    band.move_to(_p(X0 + 4.5 * STEP_W, 0)).set_z_index(-1)
    # s6's faint dashed low-level baselines
    bases = VGroup(*[DashedLine(_p(X0, ROW_Y[k] - TR_H / 2), _p(X0 + 10 * STEP_W, ROW_Y[k] - TR_H / 2),
                                dash_length=0.08).set_stroke(DIM, 2, opacity=0.6).set_z_index(-1)
                     for k in ("en", "d", "q")])
    return segs, labs, band, bases


# ---- this scene ------------------------------------------------------------------------------
LIFT = 0.45                             # clip 1: the waveform rises to make room for CLK
CLK_Y = -2.0
FLURRY = [0.06, 0.12, 0.19, 0.25, 0.32, 0.38, 0.45, 0.52, 0.58, 0.65, 0.72, 0.79, 0.86, 0.93]


def flurry(key):
    """D (or Q) across the band (steps 2..6) wiggling fast; Q follows D (it drops at EN's rise)."""
    y = ROW_Y[key] + LIFT
    lo, hi = y - TR_H / 2, y + TR_H / 2
    xa, w = X0 + 2 * STEP_W, 5 * STEP_W
    pts = [[xa, hi, 0]] if key == "q" else []
    lvl = lo
    pts.append([xa, lo, 0])
    for f in FLURRY:
        x = xa + f * w
        pts.append([x, lvl, 0])
        lvl = hi if lvl == lo else lo
        pts.append([x, lvl, 0])
    pts.append([xa + w, lvl, 0])
    return VMobject().set_points_as_corners(pts).set_stroke(TR_COL[key], 4)


# recap grid: 3 tiles on top, 2 + "next" below
COL_X = (-4.6, 0.0, 4.6)
VIS_Y = (2.55, -0.95)
CAP_Y = (1.42, -2.22)          # caption tops
TILE_W, TILE_H = 4.0, 2.1


def vis_at(i):
    r, col = divmod(i, 3)
    return _p(COL_X[col], VIS_Y[r])


def cap_at(i):
    r, col = divmod(i, 3)
    return _p(COL_X[col], CAP_Y[r])


def fit(m, i, w=TILE_W, h=TILE_H):
    m.scale(min(w / m.width, h / m.height))
    return m.move_to(vis_at(i))


def caption(text, i, **kw):
    t = T(text, size=28, color=FG, line_spacing=0.8, **kw)
    return t.move_to(cap_at(i), aligned_edge=UP).set_x(cap_at(i)[0])


def bump(m, size=26, edge=None, pad=0.0):
    """After a tile is shrunk, grow a terminal label back to a readable size, anchored on the
    edge that touches its wire (RIGHT for labels left of a wire, LEFT for labels right of one)."""
    k = size / m.font_size
    if k > 1:
        m.scale(k, about_point=m.get_critical_point(edge) if edge is not None else m.get_center())
    if edge is not None and pad:
        m.shift(-pad * edge)      # restore a clear gap to the wire (the tile scale shrank it)
    return m


def drop_nums(latch):
    for g in (latch.g1, latch.g2):
        if g.num is not None:
            g.remove(g.num)


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(7.5)   # end card under the music
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- c1.recap.1: the catch -----------------------------------------------------------------
    def clip1(self):
        segs, labs, band, bases = waveform()
        allm = [*[s for k in SEQ for s in segs[k]], labs, band, bases]
        self.add(*allm)          # s6's last shot, already on screen
        with self.say("c1.recap.1") as c:
            self.play(*[m.animate.shift(LIFT * UP) for m in allm], run_time=min(1.2, c.until("window")))
            c.wait_until("window")
            lab = T("still responding", size=38, color=RED).next_to(band, UP, buff=0.3)
            old = [segs[k][i] for k in ("d", "q") for i in range(2, 7)]
            fd, fq = flurry("d"), flurry("q")
            rt = min(3.0, max(1.5, c.until(own_word=lab) - 0.1))
            self.play(*during([FadeOut(m) for m in old], 0, 0.2),
                      *during([Create(fd, rate_func=linear), Create(fq, rate_func=linear)], 0.15, 1.0),
                      run_time=rt)
            c.wait_until(own_word=lab)
            self.play(band.animate.set_fill(RED, 0.13), *appear(lab), run_time=1.2)

            c.wait_until("want")
            clk = clock_wave(10.0, 0.6, 4, up_arrows=False).move_to(_p(X0 + 5, CLK_Y))
            clab = MathTex(r"\mathrm{CLK}", font_size=44, color=YELLOW).move_to(_p(X0 - 0.75, CLK_Y))
            self.play(Create(clk.wave, rate_func=linear), *appear(clab, shift=None),  # early: the clock row the line leads to
                      run_time=min(1.6, c.until("one instant")))
            xe = clk.rising_x(1)
            tri = Triangle().scale(0.11 * 1.8).set_stroke(width=0).set_fill(YELLOW, 1).move_to(_p(xe, CLK_Y))
            dash = DashedLine(_p(xe, CLK_Y + 0.3), _p(xe, band.get_top()[1]), dash_length=0.1)
            dash.set_stroke(YELLOW, 3)
            one = T("one instant", size=34, color=YELLOW).move_to(_p(xe, CLK_Y - 0.75))
            c.wait_until("one instant")
            self.play(FadeIn(tri, scale=0.4), Create(dash), *appear(one), run_time=1.5)
            c.wait_until("rising edge")
            self.play(FlashAround(tri, color=YELLOW, time_width=1.5, buff=0.12),
                      VShowPassingFlash(dash.copy().set_stroke(YELLOW, 6), time_width=0.5),
                      run_time=min(1.5, c.until(floor=0.5)))

    # -- c1.recap.2: the recap tiles -----------------------------------------------------------
    def clip2(self):
        with self.say("c1.recap.2") as c:
            sweep_clear(self, run_time=1.2)

            # r1: the NOR latch beside its table
            L = rs_latch()
            drop_nums(L)
            rows = [["$S", "$R", "$Q'", r"$\overline{Q}'"],
                    ["$0", "$0", "$Q", r"$\overline{Q}"],
                    ["$0", "$1", "$0", "$1"],
                    ["$1", "$0", "$1", "$0"],
                    ["$1", "$1", "$0", "$0"]]
            tab = grid_table(rows, [0, 0.75, 1.9, 2.8], size=44, pitch=0.66,
                             seps=[1.32], colors=[None, None, None, None, RED])
            t1 = fit(VGroup(L, tab).arrange(RIGHT, buff=0.6), 0, w=4.0, h=2.2).shift(0.15 * RIGHT)
            for m, e in ((L.lab_r, RIGHT), (L.lab_s, RIGHT), (L.lab_q, LEFT), (L.lab_qb, LEFT)):
                bump(m, 28, e, pad=0.08)
            cap1 = caption("RS latch: remembers\na bit, asynchronously", 0)
            c.wait_until("r1")
            self.play(*appear(t1, shift=None), *during(appear(cap1), 0.4, 1.0),  # early: recap tile, seen whole
                      run_time=1.5)
            c.wait_until("illegal")
            self.play(FlashAround(tab.rows[4], color=RED, time_width=1.5, buff=0.06),
                      run_time=min(1.5, c.until("r2")))

            # r2: the clock with edge markers
            clk = clock_wave(4.0, 1.2, 3, up_arrows=True, down_arrows=True).move_to(vis_at(1))
            for tri in [*clk.ups, *clk.downs]:
                tri.scale(1.6)
            cap2 = caption("Clock: edges mark\nwhen to change", 1)
            c.wait_until("r2")
            self.play(Create(clk.wave, rate_func=linear), *during(appear(cap2), 0.4, 1.0), run_time=1.6)
            c.wait_until("rising")
            self.play(*appear(*clk.ups, shift=0.2 * UP, lag=0.15),
                      *during(appear(*clk.downs, shift=0.2 * DOWN, lag=0.15), 0.35, 1.0), run_time=1.6)
            settle(self, clk)

            # r3: the AND gate as a valve, a = 0 blocking, a = 1 passing
            g = and_gate().scale(2.0)
            g.body.set_stroke(opacity=0.3)
            ctr = g.body.get_center() + 0.05 * RIGHT
            ring = Circle(radius=0.48).move_to(ctr).set_stroke(YELLOW, 4).set_fill(BG, 1)
            flap = Line(ctr + 0.42 * LEFT, ctr + 0.42 * RIGHT).set_stroke(BLUE, 8)
            hub = Dot(ctr, radius=0.09, color=BLUE)
            handle = MathTex("a", font_size=44, color=BLUE).next_to(ring, UP, buff=0.12)
            valve = VGroup(g, ring, flap, hub, handle).move_to(_p(-2.7, -0.1))
            WIG = [0.12, 0.3, 0.42, 0.52, 0.66, 0.88]
            w = 2.6
            b0, y0 = trace(0, w, WIG, 0.6, BLUE), trace(0, w, [], -0.6, GREEN)
            b1, y1 = trace(w, w, WIG, 0.6, BLUE), trace(w, w, WIG, -0.6, GREEN)
            tb = MathTex("b", font_size=44, color=BLUE).move_to(_p(-0.6, 0.6))
            ty = MathTex("y", font_size=44, color=GREEN).move_to(_p(-0.6, -0.6))
            h0 = T("a = 0", size=30, color=DIM).move_to(_p(w / 2, 1.4))
            h1 = T("a = 1", size=30, color=DIM).move_to(_p(1.5 * w, 1.4))
            div = DashedLine(_p(w, -1.05), _p(w, 1.05), dash_length=0.08).set_stroke(DIM, 2)
            t3 = fit(VGroup(valve, tb, ty, h0, h1, div, b0, y0, b1, y1), 2, w=4.2)
            bump(handle, 30, DOWN)
            bump(tb, 30, RIGHT)
            bump(ty, 30, RIGHT)
            bump(h0, 28)
            bump(h1, 28)
            cap3 = caption("AND: 0 blocks, 1 passes", 2)
            c.wait_until("r3")
            self.play(*appear(t3, shift=None), run_time=1.2)  # early: recap tile, seen whole
            c.wait_until("a zero blocks")
            self.play(*appear(cap3), FlashAround(VGroup(b0.copy(), y0.copy()), color=RED, time_width=1.5),
                      run_time=1.4)
            c.wait_until("passes")
            self.play(FlashAround(VGroup(b1.copy(), y1.copy()), color=GREEN, time_width=1.5),
                      run_time=min(1.4, c.until("r4")))

            # r4: the D latch, R and S never both 1
            D = add_hop(d_latch())
            drop_nums(D.latch)
            fit(D, 3, w=4.2, h=1.5).shift(0.5 * UP)
            for m, e in ((D.lab_d, RIGHT), (D.lab_en, RIGHT), (D.latch.lab_q, LEFT), (D.latch.lab_qb, LEFT)):
                bump(m, 28, e, pad=0.08)
            never = T("R and S never both 1", size=28, color=GREEN).next_to(D, DOWN, buff=0.16)
            cap4 = caption("D latch: illegal\nstate impossible", 3)
            c.wait_until("r4")
            self.play(*appear(D, shift=None), *during(appear(cap4), 0.4, 1.0), run_time=1.5)
            c.wait_until("never")
            self.play(*appear(never), run_time=min(1.0, c.until("r5")))

            # r5: the waveform with its band
            segs, labs, band, bases = waveform()
            wv = VGroup(*[s for k in SEQ for s in segs[k]], labs, bases)
            whole = VGroup(wv, band)
            fit(whole, 4, w=4.2)
            for m in labs:
                bump(m, 28, RIGHT)
            cap5 = caption("Transparent while EN = 1:\nlevel-triggered", 4)
            c.wait_until("r5")
            self.play(*appear(wv, shift=None), FadeIn(band), *during(appear(cap5), 0.4, 1.0), run_time=1.5)
            c.wait_until("while enable is one")
            self.play(FlashAround(band, color=YELLOW, time_width=1.5, buff=0.03),
                      run_time=min(1.6, c.until(floor=0.5)))
            self.tiles = [t1, cap1, clk, cap2, t3, cap3, D, never, cap4, wv, cap5]
            self.band5 = band

    # -- c1.recap.3: next time -----------------------------------------------------------------
    def clip3(self):
        s1, s2 = latch_symbol(), latch_symbol()
        s2.shift(6.2 * RIGHT)
        pair = VGroup(s1, s2).scale(0.28).move_to(vis_at(5) + 0.45 * UP)
        for sym in (s1, s2):
            for m in (sym.lab_d, sym.lab_q, sym.lab_en):
                bump(m, 28)
        gap = 0.25
        s1.shift(gap * LEFT)
        s2.shift(gap * RIGHT)
        clk = clock_wave(3.0, 0.45, 2, up_arrows=False)
        clk.move_to(_p(vis_at(5)[0], pair.get_bottom()[1] - 0.3 - 0.225))
        tri = Triangle().scale(0.11 * 1.6).set_stroke(width=0).set_fill(YELLOW, 1)
        tri.move_to(_p(clk.rising_x(1), clk.get_y()))
        nxt = caption("Next: the master-slave\nD flip-flop", 5, t2c={"Next:": YELLOW})
        with self.say("c1.recap.3") as c:
            self.play(*set_alpha(self.tiles, 0.35), self.band5.animate.set_fill(opacity=0.06),
                      *during(appear(nxt), 0.3, 1.0), run_time=1.2)
            c.wait_until("two of these")
            self.play(*appear(s1, s2, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("back to back")
            self.play(s1.animate.shift(gap * RIGHT), s2.animate.shift(gap * LEFT), run_time=1.4)
            c.wait_until("changes only")
            self.play(Create(clk.wave, rate_func=linear), run_time=1.2)
            c.wait_until("rising edge")
            self.play(FadeIn(tri, scale=0.4, shift=0.15 * UP), run_time=min(1.0, c.until(floor=0.5)))
        self.play(FlashAround(tri, color=YELLOW, time_width=1.5, buff=0.1), run_time=1.5)
