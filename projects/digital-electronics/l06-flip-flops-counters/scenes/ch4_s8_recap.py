"""Chapter 4, scene 8: recap in six tiles, then next time (the synchronous counter). Clips c4.recap.1 – c4.recap.3.

Grid, captions and bump() as ch3_s7_recap (vis_at / fit / caption). Tiles reuse, scaled down and
with thinned strokes (ch2's end_strokes idea: bubbles stay hollow): s2's state_ring + edge_tick,
s3's ripple_circuit, s4's ripple_diagram with the counts, s5's ZoomStair + zoom_brackets (the trail
redrawn compact as 7 -> 6 -> 4 -> 0: the in-place readings do not fit a tile), s6's diagram with GOLD
f..f/8, s7's bcd_chain (inner pin letters dropped at this size) + mini_timeline.
End card: s3's three flip-flops, feeds removed, clock pins on one YELLOW CLK line; the three Q
values change together (011 -> 100); BLUE '?' boxes replace the T = 1 inputs; "Part 5 · ...".
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


def bump(m, k):
    """Grow a label back by k about its own centre after its tile was shrunk."""
    return m.scale(k, about_point=m.get_center())


def thin(g, k):
    """Strokes do not scale with the tile: thin them by k so small parts keep their shape."""
    for m in g.family_members_with_points():
        w = m.get_stroke_width()
        if w > 0:
            m.set_stroke(width=max(1.0, w * k))
    return g


def hollow_bubbles(ffs):
    for f in ffs:
        if getattr(f, "bub", None) is not None:
            f.bub.set_stroke(width=1.5)
            f.bub.scale(1.5, about_point=f.bub.get_top())


# ---- recap grid (ch3_s7_recap): 3 tiles on top, 3 below ------------------------------------------
TILE_X = (-4.55, 0.0, 4.55)
VIS_Y = (2.25, -1.05)          # no "Recap" header here: the rows take its room (text >= 26 in the tiles)
CAP_Y = (0.85, -2.25)          # caption tops
TILE_W, TILE_H = 4.1, (2.4, 2.0)
HEAD_Y = 3.3


def vis_at(i):
    return _p(TILE_X[i % 3], VIS_Y[i // 3])


def fit(m, i):
    s = min(TILE_W / m.width, TILE_H[i // 3] / m.height)
    m.scale(s, about_point=m.get_center())
    m.move_to(vis_at(i))
    return s


def fit_wh(m, w, h):
    s = min(w / m.width, h / m.height)
    m.scale(s, about_point=m.get_center())
    return s


def caption(text, i, **kw):
    t = T(text, 28, line_spacing=0.8, **kw)
    return t.move_to(_p(vis_at(i)[0], CAP_Y[i // 3]), aligned_edge=UP).set_x(vis_at(i)[0])


# ---- s2: state_ring / edge_tick ------------------------------------------------------------------
RING_R = 2.3
NODE_R = 0.5


def edge_tick(color=YELLOW, w=0.4, h=0.28, width=4):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [[-w / 2, -h / 2, 0], [0, -h / 2, 0], [0, h / 2, 0], [w / 2, h / 2, 0]])


def state_ring(n_bits=3, radius=RING_R):
    n = 2 ** n_bits
    hub = Dot(ORIGIN, radius=0.01).set_opacity(0)

    def dirn(i):
        a = PI / 2 - TAU * i / n
        return np.array([np.cos(a), np.sin(a), 0.0])

    nodes, circles, bits, decimals, arrows = [], [], [], [], []
    for i in range(n):
        p = radius * dirn(i)
        circ = Circle(radius=NODE_R, color=BLUE, stroke_width=4).set_fill(BG, 1).move_to(p)
        b = Mono(format(i, f"0{n_bits}b"), size=28, color=GREEN).move_to(p)
        circles.append(circ)
        bits.append(b)
        nodes.append(VGroup(circ, b))
        decimals.append(T(str(i), 34, color=GOLD).move_to(p - 0.85 * dirn(i)))
    for i in range(n):
        p, q = radius * dirn(i), radius * dirn((i + 1) % n)
        u = (q - p) / np.linalg.norm(q - p)
        arrows.append(Arrow(p + (NODE_R + 0.04) * u, q - (NODE_R + 0.04) * u, buff=0, color=FG,
                            stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.4))
    ring = VGroup(VGroup(*arrows), VGroup(*nodes), VGroup(*decimals), hub)
    ring.nodes, ring.circles, ring.bits, ring.decimals, ring.arrows, ring.hub = (
        nodes, circles, bits, decimals, arrows, hub)
    ring.out_point = lambda i, d=0.68: ring.hub.get_center() + (radius + d) * dirn(i) * (
        ring.circles[0].width / (2 * NODE_R))
    return ring


# ---- flip-flop symbol (s3's make_ff with .bub, s7's lab / .qb_l) ---------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
CLR_DX = 0.55


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), q_len=WIRE, bubble=False, lab=36):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + q_len, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    top_clk = -hb - (0.22 if bubble else 0.02)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, top_clk)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, lab, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", lab, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar(lab).move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    parts = [*in_w, q_w, qb_w, clk_w, box, tri]
    bub = None
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.11))
        parts.append(bub)
    g = VGroup(*parts, *in_l, q_l, qb_l)
    g.box, g.tri, g.bub, g.clk_w, g.q_w, g.qb_w, g.in_w = box, tri, bub, clk_w, q_w, qb_w, in_w
    g.qb_l = qb_l
    g.labels = [*in_l, q_l, qb_l]
    g.shift(center)
    return g


def spread_q(f):
    c, h = f.box.get_center(), f.box.height
    f.labels[-2].move_to(c + _p(f.labels[-2].get_x() - c[0], 0.27 * h))
    f.labels[-1].move_to(c + _p(f.labels[-1].get_x() - c[0], -0.25 * h))


# ---- s3: ripple_circuit ----------------------------------------------------------------------------
CH_X = (-4.3, 0.0, 4.3)
STUB_Y = 1.75
FEED_Y = -BOX_H / 2 - EN_WIRE


def ripple_circuit(k=0.85, center=_p(0, 0.85)):
    hb = BOX_H / 2
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

    def glow_path(i, width=10):
        f, n = ffs[i], ffs[i + 1]
        pts = [f.q_w.get_start(), stubs[i].get_points()[3], *[feeds[i].get_points()[j] for j in (3, 7)],
               n.clk_w.get_end()]
        return VMobject().set_points_as_corners(pts).set_stroke(GREEN, width)
    g.glow_path = glow_path
    return g


# ---- s4: ripple_diagram ------------------------------------------------------------------------------
RD_X0, RD_X1 = -5.1, 6.3
RD_P = (RD_X1 - RD_X0) / 8.9
RD_FALL = [RD_X0 + RD_P + k * RD_P for k in range(8)]
RD_D = 0.2
RD_ROW_Y = [2.9, 1.5, 0.1, -1.3]
RD_AMP = 0.3
RD_STUB = RD_X0 + 0.55


def _rd_y(row, bit):
    return RD_ROW_Y[row] + (RD_AMP if bit else -RD_AMP)


def _rd_poly(row, pts, color, width=4):
    return (VMobject().set_points_as_corners([_p(x, _rd_y(row, b)) for x, b in pts])
            .set_stroke(color, width))


def _rd_pieces(row, edges, color=GREEN):
    xs = [RD_STUB, *edges, RD_X1]
    out, b = [_rd_poly(row, [(RD_X0, 0), (RD_STUB, 0)], color)], 0
    for k in range(len(xs) - 1):
        if k == 0:
            pts = [(xs[0], b), (xs[1], b)]
        else:
            pts = [(xs[k], b), (xs[k], 1 - b), (xs[k + 1], 1 - b)]
            b = 1 - b
        out.append(_rd_poly(row, pts, color))
    return out


def _rd_cause(x_from, row_from, x_to, row_to):
    a, b = _p(x_from, _rd_y(row_from, 0) - 0.06), _p(x_to, _rd_y(row_to, 1) + 0.06)
    return Arrow(a, b, buff=0, stroke_width=3, tip_length=0.16,
                 max_tip_length_to_length_ratio=0.35).set_color(YELLOW)


class RippleDiagram(VGroup):
    def __init__(self, causes=True, **kw):
        super().__init__(**kw)
        d = RD_D
        texs = [r"\mathrm{CLK}", "Q_0", "Q_1", "Q_2"]
        cols = [YELLOW, GREEN, GREEN, GREEN]
        self.labels = VGroup(*[
            MathTex(t, font_size=40, color=c).move_to(_p(0, y)).align_to(_p(RD_X0 - 0.35, 0), RIGHT)
            for t, c, y in zip(texs, cols, RD_ROW_Y)])
        pts = [(RD_X0, 0)]
        for f in RD_FALL:
            pts += [(f - RD_P / 2, 0), (f - RD_P / 2, 1), (f, 1), (f, 0)]
        pts.append((RD_X1, 0))
        self.clk = _rd_poly(0, pts, YELLOW)
        self.downs = VGroup(*[Triangle().rotate(PI).scale(0.1).set_stroke(width=0).set_fill(YELLOW, 1)
                              .move_to(_p(f, RD_ROW_Y[0])) for f in RD_FALL])
        g_top, g_bot = _rd_y(0, 1) + 0.12, _rd_y(3, 0) - 0.12
        self.guides = VGroup(*[Line(_p(f, g_top), _p(f, g_bot)).set_stroke(DIM, 1.5).set_z_index(-2)
                               for f in RD_FALL])
        self.e0 = [f + d for f in RD_FALL]
        self.e1 = [RD_FALL[k] + 2 * d for k in (1, 3, 5, 7)]
        self.e2 = [RD_FALL[k] + 3 * d for k in (3, 7)]
        self.q = [_rd_pieces(1, self.e0), _rd_pieces(2, self.e1), _rd_pieces(3, self.e2)]
        self.causes1 = [_rd_cause(RD_FALL[k] + d, 1, RD_FALL[k] + 2 * d, 2) for k in (1, 3, 5, 7)]
        self.causes2 = [_rd_cause(RD_FALL[k] + 2 * d, 2, RD_FALL[k] + 3 * d, 3) for k in (3, 7)]
        self.add(self.guides, self.labels, self.clk, self.downs, *self.q[0], *self.q[1], *self.q[2])
        if causes:
            self.add(*self.causes1, *self.causes2)


COUNTS = [0, 1, 2, 3, 4, 5, 6, 7, 0]
BOUNDS = [RD_X0, *RD_FALL, RD_X1]


# ---- s5: the zoom at the 7 -> 0 edge -------------------------------------------------------------
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
Z_BRK_Y = [Z_ROW[r + 1] - Z_AMP - 0.2 for r in range(3)]


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


class ZoomStair(VGroup):
    def __init__(self, **kw):
        super().__init__(**kw)
        texs = [r"\mathrm{CLK}", "Q_0", "Q_1", "Q_2"]
        cols = [YELLOW, GREEN, GREEN, GREEN]
        self.labels = VGroup(*[
            MathTex(t, font_size=40, color=c).move_to(_p(0, y)).align_to(_p(Z_SCR[0] - 0.35, 0), RIGHT)
            for t, c, y in zip(texs, cols, Z_ROW)])
        self.clk = _zpoly(0, [(Z_SCR[0], 1), (Z_E, 1), (Z_E, 0), (Z_SCR[1], 0)], YELLOW)
        self.guide = zoom_guide(Z_E)
        self.down = zoom_down(Z_E)
        self.q = [_zfall(r + 1, x) for r, x in enumerate(Z_FALLS)]
        self.add(self.guide, self.labels, self.clk, *self.q, self.down)


def delay_bracket(x0, x1, y, color=GOLD):
    h = 0.14
    return VMobject().set_points_as_corners(
        [_p(x0, y + h), _p(x0, y), _p(x1, y), _p(x1, y + h)]).set_stroke(color, 4)


def zoom_brackets():
    xs = [Z_E, *Z_FALLS]
    return [delay_bracket(xs[r] + 0.04, xs[r + 1] - 0.04, Z_BRK_Y[r]) for r in range(3)]


# ---- s7: bcd_chain / mini_timeline ---------------------------------------------------------------
class Gate(VGroup):
    def __init__(self, body, ins, out, color=BLUE):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body = body
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body, *self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()


def and_gate(color=BLUE):
    k = 0.5523 * 0.6
    b = VMobject()
    b.start_new_path(_p(-0.7, 0.6))
    b.add_line_to(_p(0.0, 0.6))
    b.add_cubic_bezier_curve_to(_p(k, 0.6), _p(0.6, k), _p(0.6, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.6, -k), _p(k, -0.6), _p(0.0, -0.6))
    b.add_line_to(_p(-0.7, -0.6))
    b.add_line_to(_p(-0.7, 0.6))
    return Gate(b, [(-0.7, 0.3), (-0.7, -0.3)], (0.6, 0.0), color=color)


FF_X = (-6.45, -2.15, 2.15, 6.45)
JX = BOX_W / 2 + WIRE + 0.4
B_STUB_Y = 1.9
CLR_Y = -2.9
GATE_C = (9.75, 2.4)
RET_X = 10.75
B_K = 0.6
B_C = _p(0, -1.62)
B_LAB = 48


def bcd_chain():
    hb = BOX_H / 2
    ffs = [make_ff(_p(x, 0), ins=(("T", PIN_Y),), bubble=True, lab=B_LAB) for x in FF_X]
    for f in ffs:
        f.qb_w.set_stroke(DIM)
        f.qb_l.set_color(DIM)
    ones = [MathTex("1", font_size=56, color=BLUE).next_to(f.in_w[0].get_start(), LEFT, buff=0.12)
            for f in ffs]
    dots, qlabs, wires = [], [], []
    for k, x in enumerate(FF_X):
        jx = x + JX
        wires.append(poly([(x + BOX_W / 2 + WIRE, PIN_Y), (jx, PIN_Y), (jx, B_STUB_Y)], GREEN, 5))
        qlabs.append(MathTex(f"Q_{k}", font_size=B_LAB + 4, color=GREEN).move_to(_p(jx - 0.62, 1.35)))
        if k < 3:
            ffs[k + 1].clk_w.set_stroke(GREEN)
            wires.append(poly([(jx, PIN_Y), (jx, -hb - EN_WIRE), (FF_X[k + 1], -hb - EN_WIRE)], GREEN, 5))
            dots.append(Dot(_p(jx, PIN_Y), radius=0.09, color=GREEN))
    clk_l = T("CLK", B_LAB, YELLOW).next_to(ffs[0].clk_w.get_start(), LEFT, buff=0.15)
    pins = [Line(_p(x + CLR_DX, -hb), _p(x + CLR_DX, CLR_Y)).set_stroke(RED, 5) for x in FF_X]
    bus = Line(_p(FF_X[0] + CLR_DX, CLR_Y), _p(FF_X[3] + CLR_DX, CLR_Y)).set_stroke(RED, 5)
    clr_l = T("CLR", B_LAB, RED).next_to(bus.get_start(), LEFT, buff=0.15)
    gate = and_gate().move_to(_p(*GATE_C))
    i0, i1, o = gate.inp(0), gate.inp(1), gate.out()
    taps = {1: poly([(FF_X[1] + JX, B_STUB_Y), (FF_X[1] + JX, i0[1]), (i0[0], i0[1])], GREEN, 5),
            3: poly([(FF_X[3] + JX, B_STUB_Y), (FF_X[3] + JX, i1[1]), (i1[0], i1[1])], GREEN, 5)}
    gate_out = poly([(o[0], o[1]), (RET_X, o[1]), (RET_X, CLR_Y), (FF_X[3] + CLR_DX, CLR_Y)], RED, 5)
    base = VGroup(*ffs, *ones, *wires, *dots, clk_l)
    clr = VGroup(*pins, bus, clr_l)
    g = VGroup(base, VGroup(*qlabs), clr, gate, taps[1], taps[3], gate_out)
    g.scale(B_K, about_point=ORIGIN).move_to(B_C)
    g.ffs, g.ones, g.qlabs, g.bus, g.clk_l, g.clr_l = ffs, ones, qlabs, bus, clk_l, clr_l
    g.gate, g.gate_out = gate, gate_out
    return g


TL_W, TL_H, SLIVER = 1.5, 0.55, 0.13


def mini_timeline(reset_at=10, w=TL_W, h=TL_H):
    seq = [8, 9, 10, 0]
    col = GOLD
    g, cells, nums = VGroup(), {}, {}
    x = 0.0
    for v in seq:
        if v == reset_at:
            r = Rectangle(width=SLIVER, height=h).set_stroke(RED, 2).set_fill(RED, 1)
            r.move_to(_p(x + SLIVER / 2, 0))
            n = T(str(v), 30, RED).next_to(r, DOWN, buff=0.12)
            x += SLIVER
        else:
            r = Rectangle(width=w, height=h).set_stroke(col, 3).set_fill(col, 0.12)
            r.move_to(_p(x + w / 2, 0))
            n = T(str(v), 34, col).move_to(r)
            x += w
        cells[v], nums[v] = r, n
        g.add(r, n)
    g.cells, g.nums = cells, nums
    return g


# ---- the six panels --------------------------------------------------------------------------------
RING_A, RING_B = 1.55, 0.95          # the tile's ring: an ellipse (the tile is wide, not tall)
PILL_W, PILL_H = 0.86, 0.5            # nodes as pills: "000" at 26 does not fit a circle that fits here


def ring_pos(i, a=RING_A, b=RING_B):
    t = TAU * i / 8
    return _p(a * np.sin(t), b * np.cos(t))


def pill():
    return RoundedRectangle(corner_radius=0.22, width=PILL_W, height=PILL_H).set_stroke(BLUE, 2.5)


def panel_ring():
    """s2's state ring redrawn at tile size: BLUE nodes with GREEN bits, GOLD decimals inside,
    FG arrows clockwise from 000 at the top, the YELLOW edge tick at the hub."""
    nodes, bits, decs, arrows = [], [], [], []
    for i in range(8):
        n = pill().set_fill(BG, 1).move_to(ring_pos(i))
        nodes.append(n)
        bits.append(Mono(format(i, "03b"), 27, GREEN).move_to(n))
        decs.append(T(str(i), 27, GOLD).move_to(ring_pos(i, 0.74, 0.42)))
    for i in range(8):
        p, q = ring_pos(i), ring_pos((i + 1) % 8)
        u = (q - p) / np.linalg.norm(q - p)
        out = min(PILL_W / 2 / max(abs(u[0]), 1e-6), PILL_H / 2 / max(abs(u[1]), 1e-6)) + 0.04
        arrows.append(Arrow(p + out * u, q - out * u, buff=0, color=FG, stroke_width=2,
                            tip_length=0.12, max_tip_length_to_length_ratio=0.5))
    tick = edge_tick(w=0.25, h=0.17, width=3)
    hub = Dot(ORIGIN, radius=0.01).set_opacity(0)
    g = VGroup(*arrows, *nodes, *bits, *decs, tick, hub)
    g.shift(vis_at(0))
    dot = pill().set_stroke(YELLOW, 4).move_to(nodes[0])
    g.nodes, g.hub, g.dot = nodes, hub, dot
    return g


def r1_caption(i):
    l1 = T("counter: n flip-flops,", 28, t2s={" n ": ITALIC})
    two = MathTex("2^n", font_size=34)
    l2 = VGroup(two, T("states", 28)).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    two.shift(0.02 * DOWN)
    g = VGroup(l1, l2).arrange(DOWN, buff=0.12)
    return g.move_to(_p(vis_at(i)[0], CAP_Y[0]), aligned_edge=UP).set_x(vis_at(i)[0])


def panel_ripple():
    rc = ripple_circuit(k=1.0, center=ORIGIN)
    g = VGroup(rc, rc.clk_l)
    s = fit(g, 1)
    thin(g, 0.55)
    hollow_bubbles(rc.ffs)
    for f in rc.ffs:
        f.remove(f.qb_l)
        for lab in f.labels[:-1]:
            bump(lab, 26.6 / (36 * s))
        t_l, q_l = f.labels[0], f.labels[1]
        t_l.set_x(f.box.get_left()[0] + 0.025 + t_l.width / 2)
        q_l.set_x(f.box.get_right()[0] - 0.015 - q_l.width / 2)
    for o, f in zip(rc.ones, rc.ffs):
        bump(o, 26.6 / (44 * s)).next_to(f.in_w[0].get_start(), LEFT, buff=0.05)
    for q, st in zip(rc.q_labels, rc.stubs):
        bump(q, 28 / (44 * s)).next_to(st.get_end(), UP, buff=0.05)
    bump(rc.clk_l, 26.6 / (36 * s)).next_to(rc.ffs[0].clk_w.get_start(), DOWN, buff=0.05)
    g.move_to(vis_at(1))
    g.rc = rc
    return g


def panel_timing():
    rd = RippleDiagram()
    cy = -2.3
    counts = [T(str(v), 46, GOLD).move_to(_p((BOUNDS[j] + BOUNDS[j + 1]) / 2, cy))
              for j, v in enumerate(COUNTS)]
    g = VGroup(rd, *counts)
    s = fit(g, 2)
    thin(rd, 0.6)
    x_lab = rd.clk.get_left()[0] - 0.08
    for lab in rd.labels:
        bump(lab, 26.6 / (40 * s)).align_to(_p(x_lab, 0), RIGHT)
    for n in counts:
        bump(n, 26.6 / (46 * s))
    g.move_to(vis_at(2))
    g.rd, g.counts = rd, counts
    return g


def panel_zoom():
    z = ZoomStair()
    brk = zoom_brackets()
    body = VGroup(z, *brk)
    s = fit_wh(body, 4.0, 1.35)
    thin(body, 0.6)
    x_lab = z.clk.get_left()[0] - 0.08
    for lab in z.labels:
        bump(lab, 26.6 / (40 * s)).align_to(_p(x_lab, 0), RIGHT)
    trail = MathTex("7", r"\to", "6", r"\to", "4", r"\to", "0", font_size=40)
    for k, col in zip(range(7), [GREEN, DIM, RED, DIM, RED, DIM, GREEN]):
        trail[k].set_color(col)
    trail.next_to(body, DOWN, buff=0.18).set_x(z.clk.get_center()[0])
    g = VGroup(body, trail)
    g.move_to(vis_at(3))
    g.z, g.brk, g.trail = z, brk, trail
    return g


def panel_divider():
    rd = RippleDiagram(causes=False)
    flabs = [MathTex(t, font_size=44, color=GOLD).next_to(_p(RD_X1, RD_ROW_Y[r]), RIGHT, buff=0.3)
             for r, t in enumerate(["f", "f/2", "f/4", "f/8"])]
    g = VGroup(rd, *flabs)
    s = fit_wh(g, 3.7, 1.9)
    thin(rd, 0.6)
    x_lab = rd.clk.get_left()[0] - 0.08
    for lab in rd.labels:
        bump(lab, 26.6 / (40 * s)).align_to(_p(x_lab, 0), RIGHT)
    x_r = rd.clk.get_right()[0]
    for f, lab in zip(flabs, rd.labels):
        bump(f, 30 / (44 * s))
        f.move_to(_p(0, lab.get_y())).align_to(_p(x_r + 0.12, 0), LEFT)
    g.move_to(vis_at(4))
    g.rd, g.flabs = rd, flabs
    return g


def panel_bcd():
    ch = bcd_chain()
    for f in ch.ffs:
        f.remove(*f.labels)
    base = ch.submobjects[0]
    base.remove(*ch.ones, ch.clk_l)
    ch.remove(ch.submobjects[1])           # the Q_k labels: too crowded at tile size
    s = fit_wh(ch, 3.6, 1.3)
    thin(ch, 0.5)
    hollow_bubbles(ch.ffs)
    k = s * B_K
    bump(ch.clr_l, 26.6 / (B_LAB * k)).next_to(ch.bus.get_start(), LEFT, buff=0.06)
    tl = mini_timeline()
    tl.scale(0.48)
    for v, n in tl.nums.items():
        bump(n, 26.6 / ((30 if v == 10 else 34) * 0.48))
    tl.nums[10].next_to(tl.cells[10], DOWN, buff=0.05)
    g = VGroup(ch, tl).arrange(DOWN, buff=0.18)
    g.move_to(vis_at(5))
    g.ch, g.tl = ch, tl
    return g


# ---- the end card: s3's flip-flops on one clock --------------------------------------------------
class Recap(NarratedScene):
    def construct(self):
        self.tiles = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def show_tile(self, panel, cap, rt=1.5):
        prev = self.tiles[-1] if self.tiles else []
        anims = [*set_alpha(prev, 0.5), *appear(panel, shift=None), *during(appear(cap), 0.4, 1.0)]
        self.play(*anims, run_time=rt)  # early: recap tile, seen whole
        self.tiles.append([panel, cap])

    # ------------------------------------------------------------------ c4.recap.1
    def clip1(self):
        with self.say("c4.recap.1") as c:
            # {r1}: the state ring; the dot steps once round
            p1 = panel_ring()
            cap1 = r1_caption(0)
            c.wait_until("r1")
            self.show_tile(p1, cap1)
            hub = p1.hub.get_center()

            def steps(t, n=8):
                # each step: move in the first 40%, then hold on the node for the rest
                k = min(int(t * n), n - 1)
                return (k + smooth(min(1.0, (t * n - k) / 0.4))) / n
            self.play(FadeIn(p1.dot), run_time=0.5)
            self.play(UpdateFromAlphaFunc(p1.dot, lambda m, a: m.move_to(hub + ring_pos(8 * steps(a))),
                                          rate_func=linear),
                      run_time=max(3.6, c.until("two to the N") - 0.1))
            p1.add(p1.dot)
            c.wait_until("two to the N")
            self.play(LaggedStart(*[VShowPassingFlash(ci.copy().set_stroke(YELLOW, 4), time_width=0.6)
                                    for ci in p1.nodes], lag_ratio=0.12), run_time=1.6)

            # {r2}: the ripple circuit; Q0 and Q1 glow into the next clocks
            p2 = panel_ripple()
            cap2 = caption("each stage clocked\nby the one before", 1)
            c.wait_until("r2")
            self.show_tile(p2, cap2)
            c.wait_until("output of the one before")
            self.play(LaggedStart(*[VShowPassingFlash(p2.rc.glow_path(i, 6), time_width=0.6)
                                    for i in (0, 1)], lag_ratio=0.5), run_time=1.6)

            # {r3}: the timing diagram with its counts
            p3 = panel_timing()
            cap3 = caption("it counts,\none delay per stage", 2, t2c={"counts,": GOLD})
            c.wait_until("r3")
            self.show_tile(p3, cap3)
            c.wait_until("one delay later")
            self.play(FlashAround(VGroup(*p3.counts).copy(), color=GOLD, time_width=1.5, buff=0.08),
                      run_time=min(1.4, c.until(floor=0.3) - 0.05))

    # ------------------------------------------------------------------ c4.recap.2
    def clip2(self):
        with self.say("c4.recap.2") as c:
            # {r4}: the 7 -> 0 zoom and its false counts
            p4 = panel_zoom()
            cap4 = caption("delays add up:\nfalse counts, speed limit", 3, t2c={"false counts": RED})
            self.show_tile(p4, cap4)
            c.wait_until("false values")
            self.play(*flash([p4.trail[2], p4.trail[4]], color=RED, time_width=1.5, buff=0.06), run_time=1.2)
            c.wait_until("clock speed")
            self.play(*[VShowPassingFlash(b.copy().set_stroke(GOLD, 6), time_width=1.0) for b in p4.brk],
                      run_time=1.2)

            # {r5}: f, f/2, f/4, f/8
            p5 = panel_divider()
            cap5 = caption("each output halves the\nfrequency: dividers", 4,
                           t2c={"halves": GOLD, "dividers": YELLOW})
            c.wait_until("r5")
            self.show_tile(p5, cap5)
            c.wait_until("dividers")
            self.play(LaggedStart(*flash(p5.flabs, color=GOLD, time_width=1.5, buff=0.06), lag_ratio=0.3),
                      run_time=1.4)

            # {r6}: the BCD chain, AND on the CLR line, its 8, 9, sliver, 0
            p6 = panel_bcd()
            cap6 = caption("AND gate + clear:\ncount 0 to 9", 5, t2c={"clear": RED})
            c.wait_until("r6")
            self.show_tile(p6, cap6)
            c.wait_until("clear inputs")
            self.play(FlashAround(p6.ch.gate, color=BLUE, time_width=1.5, buff=0.05),
                      VShowPassingFlash(p6.ch.gate_out.copy().set_stroke(RED, 5), time_width=0.8),
                      run_time=1.2)
            c.wait_until("counts from")
            self.play(FlashAround(p6.tl.copy(), color=GOLD, time_width=1.5, buff=0.06),
                      run_time=min(1.3, c.until(floor=0.6)))

    # ------------------------------------------------------------------ c4.recap.3
    def clip3(self):
        with self.say("c4.recap.3") as c:
            # {next}: the grid clears; s3's three flip-flops come back
            c.wait_until("synchronous")
            self.play(FadeOut(*self.mobjects), run_time=1.0)
            title = T("Next: the synchronous counter", 48, t2c={"Next:": YELLOW}).move_to(_p(0, 3.35))
            self.play(*appear(title), run_time=0.9)  # early: the next topic's title, said in this sentence
            rc = ripple_circuit()
            vals = [Mono(v, 40, GREEN).next_to(q, RIGHT, buff=0.18) for v, q in zip("110", rc.q_labels)]
            self.play(*appear(rc, rc.clk_l, *vals, shift=None, lag=0.15),  # early: the circuit and its pin names, shown whole
                      run_time=min(1.4, c.until("One clock") - 0.1))

            # One clock goes to every flip-flop: feeds out, one YELLOW CLK line in
            c.wait_until("One clock")
            starts = [f.clk_w.get_start() for f in rc.ffs]
            bus = Line(starts[0], starts[2]).set_stroke(YELLOW, 5)
            jdot = Dot(starts[1], radius=0.09, color=YELLOW)
            self.play(FadeOut(*rc.feeds, *rc.dots), run_time=0.8)
            for m in (*rc.feeds, *rc.dots):
                rc.remove(m)
            self.play(Create(bus), FadeIn(jdot),
                      *[f.clk_w.animate.set_stroke(YELLOW) for f in rc.ffs[1:]], run_time=1.2)

            # so they all change together: one edge, three new values
            new = [Mono(v, 40, GREEN).move_to(o) for v, o in zip("001", vals)]
            c.wait_until("change together")
            self.play(VShowPassingFlash(bus.copy().set_stroke(YELLOW, 10), time_width=0.6),
                      *[a for o, n in zip(vals, new) for a in during(swap(o, n), 0.35, 1.0)],
                      run_time=1.6)

            # {logic}: the price, a BLUE '?' box in front of each input
            boxes = []
            for o, f in zip(rc.ones, rc.ffs):
                b = Rectangle(width=0.55, height=0.6).set_stroke(BLUE, 4).set_fill(BG, 1)
                b.next_to(f.in_w[0].get_start(), LEFT, buff=0)
                boxes.append(VGroup(b, T("?", 36, BLUE).move_to(b)))
            part = T("Part 5 · Designing a synchronous counter", 40).move_to(_p(0, -2.75))
            c.wait_until("logic")
            self.play(*disappear(*rc.ones), run_time=0.6)
            for o in rc.ones:
                rc.remove(o)
            self.play(*[GrowFromCenter(bx) for bx in boxes], run_time=0.8)
            self.play(*appear(part), run_time=1.0)  # early: end-card line, not read aloud
        # end card, carried by the music
        self.wait(7.6)
