"""Chapter 4, scene 3: the ripple counter circuit, and why the chain counts. Clips c4.ripple.1 – c4.ripple.4.

ripple_circuit() is ch3_s7_recap's ripple_chain() without its LEDs (make_ff(..., bubble=True)
copied from there), each Q running right to a junction, up to a GREEN Q_k label and down into the
next clock input. Geometry (unscaled, built at ORIGIN, then .scale(k, about_point=ORIGIN) and
shifted by `center`): box centres x = -4.3, 0, 4.3, y = 0; boxes 1.5 x 2.6 (FG stroke 4); pins
0.6 above / below centre; T wires BLUE 0.85 long with a BLUE MathTex '1' (44) left of each;
junctions at x + 2.0; Q_k stubs up to y = 1.75, labels MathTex Q_k 44 GREEN just above; feeds down
to y = -2.3, across, up into the next bubble (GREEN, stroke 5); first clock wire YELLOW. CLK label
(T 36 YELLOW) is built separately (.clk_l, not in the group). Default k = 0.85, center (0, 0.85):
the circuit then spans x ≈ -5.3 … 5.6, y ≈ -1.1 … 2.85.
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


# ---- ch3_s7_recap's make_ff (ins=..., bubble=...) ----------------------------------------------
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


# ---- the ripple counter (ch3_s7_recap's ripple_chain without LEDs) ------------------------------
CH_X = (-4.3, 0.0, 4.3)
STUB_Y = 1.75
FEED_Y = -BOX_H / 2 - EN_WIRE


def ripple_circuit(k=0.85, center=_p(0, 0.85)):
    """Three falling-edge T flip-flops, T tied to a BLUE 1, Q_k clocking the next.
    Parts: .ffs .ones .feeds (Q_k -> next clock, k = 0, 1) .stubs .dots .q_labels; .clk_l (not in
    the group: add it yourself). .glow_path(k) -> a fresh path from Q_k's pin into the next clock."""
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

    def glow_path(i):
        f, n = ffs[i], ffs[i + 1]
        pts = [f.q_w.get_start(), stubs[i].get_points()[3], *[feeds[i].get_points()[j] for j in (3, 7)],
               n.clk_w.get_end()]
        return VMobject().set_points_as_corners(pts).set_stroke(GREEN, 10)
    g.glow_path = glow_path
    return g


# ---- s5's T table (ch3_s7_recap's grid_table / t_table) ---------------------------------------
TAB_XS = [0, 0.75, 1.9, 2.8, ("L", 3.75)]
TAB_SEPS = [1.32, 3.4]
TAB_PITCH = 0.66
QB = r"$\overline{Q}"
T_COL = 0.375
TK = 1.35
MK = 1.15


def grid_table(rows, xs, size=44, pitch=0.66, seps=(), colors=None, tk=1.0):
    out = []
    for i, row in enumerate(rows):
        cells = []
        for j, s in enumerate(row):
            col = (colors[i] if colors and colors[i] else FG)
            if s.startswith("$"):
                m = MathTex(s[1:], font_size=size * MK, color=col)
            else:
                m = T(s, size=size * 0.82 * tk, color=col)
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


def t_table():
    tab = grid_table([["$T", "$Q'", r"$\overline{Q}\,'", "comment"],
                      ["$0", "$Q", QB, "hold"],
                      ["$1", QB, "$Q", "toggle"]],
                     [T_COL] + TAB_XS[2:], size=44, pitch=TAB_PITCH, seps=TAB_SEPS, tk=TK)
    r = tab.rows
    r[0][0].set_color(BLUE)
    for i in (0, 1, 2):
        for m in r[i][1:3]:
            m.set_color(GREEN)
    r[2][3].set_color(YELLOW)
    return tab


# ---- small edge glyphs (ch2_s6's tiny traces: a step with a filled triangle on the edge) ------
def edge_glyph(kind, center, w=2.4, h=0.6, color=YELLOW, tri=0.13):
    cx, cy = center[0], center[1]
    lo, hi = cy - h / 2, cy + h / 2
    a, b = (hi, lo) if kind == "fall" else (lo, hi)
    line = poly([(cx - w / 2, a), (cx, a), (cx, b), (cx + w / 2, b)], color, 4)
    t = Triangle().scale(tri).set_stroke(width=0).set_fill(color, 1)
    if kind == "fall":
        t.rotate(PI)
    t.move_to(_p(cx, cy))
    return VGroup(line, t)


def dim_symbol(g):
    for m in [g.box, g.tri, g.clk_w, g.q_w, g.qb_w, *g.in_w]:
        m.set_stroke(DIM)
    for l in g.labels:
        l.set_color(DIM)
    return g


# ---- the counting column -----------------------------------------------------------------------
ROW_X = -4.6                     # centre of each row "q2 q1 q0" (Mono 44, one space between bits)
BIT_P = 2 * 0.0083 * 44          # Mono pitch of "0 0 0": 0.73 between bits
COL_X = (ROW_X - BIT_P, ROW_X, ROW_X + BIT_P)       # Q2, Q1, Q0
DEC_X = -2.75
HEAD_Y = 3.3
ROW_Y0, ROW_P = 2.55, 0.66
VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 0]


def row_y(r):
    return ROW_Y0 - r * ROW_P


def count_column():
    head = [MathTex(f"Q_{b}", font_size=44, color=GREEN) for b in (2, 1, 0)]
    rows, decs = [], []
    for r, v in enumerate(VALUES):
        rows.append(Mono(" ".join(format(v, "03b")), size=44, color=GREEN).move_to(_p(ROW_X, row_y(r))))
        decs.append(T(str(v), 38, GOLD).move_to(_p(DEC_X, row_y(r))))
    for h, row in zip(head, [0, 1, 2]):
        h.move_to(_p(rows[0][row].get_x(), HEAD_Y))
    return head, rows, decs


def step_arrow(rows, r, from_bit, to_bit):
    """Between rows r and r+1: from glyph from_bit to glyph to_bit (0 = Q2 ... 2 = Q0)."""
    y = (row_y(r) + row_y(r + 1)) / 2
    x0, x1 = rows[r][from_bit].get_x(), rows[r][to_bit].get_x()
    return Arrow(_p(x0 - 0.1, y), _p(x1 + 0.1, y), buff=0,
                 stroke_width=5, max_tip_length_to_length_ratio=0.45, color=YELLOW)


# ---- s2's state ring (copied from ch4_s2_counters.py) -------------------------------------------
RING_C = _p(4.15, -1.4)
RING_K = 0.75                    # ring scale here; its bits and decimals keep their s2 sizes
RING_R = 2.3        # ring radius (node centres)
NODE_R = 0.5        # node circle radius


def state_ring(n_bits=3, radius=RING_R):
    """The chapter's running counter: 2^n nodes clockwise from the top (000 at 12 o'clock).

    Built centred on ORIGIN. Node i: BLUE circle (r 0.5, stroke 4) holding its bits (Mono 28, GREEN);
    its GOLD decimal (T 34) sits 0.85 inward. arrows[i] goes i -> i+1 (FG, stroke 3); arrows[-1] is the
    wrap 111 -> 000. ring.hub is an invisible dot at the centre (moves with the ring);
    ring.out_point(i, d) is the point d beyond node i's centre, radially outward.
    """
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



class Ripple(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c4.ripple.1
    def clip1(self):
        circ = self.circ = ripple_circuit()
        with self.say("c4.ripple.1") as c:
            # {circuit}: three boxes, left to right
            self.play(*appear(*circ.ffs, shift=None, lag=0.4), run_time=min(2.0, c.until("tflip")))
            # {tflip}: chained: each Q into the next clock input, outputs on top
            c.wait_until("tflip")
            self.play(*[Create(w) for w in [*circ.stubs, *circ.feeds]], *appear(*circ.dots, shift=None),
                      run_time=1.5)
            self.play(*appear(*circ.q_labels, lag=0.3), run_time=1.0)  # early: output names, read later
            # {one}: every T tied to 1
            c.wait_until("one")
            self.play(*appear(*circ.ones, shift=0.2 * RIGHT, lag=0.4), run_time=1.5)
            # only wires
            c.wait_until("only wires")
            paths = [circ.glow_path(0), circ.glow_path(1)] + \
                    [f.in_w[0].copy().set_stroke(BLUE, 10) for f in circ.ffs]
            self.play(*[VShowPassingFlash(p, time_width=0.5) for p in paths], run_time=1.5)

            # {toggle}: the T table inset, toggle row lit
            tab = self.tab = t_table().scale(0.98)
            tab.move_to(_p(1.2, -2.5))
            c.wait_until("toggle")
            self.play(*appear(tab, shift=None), run_time=1.0)  # early: the table shown whole, then its toggle row lit
            c.wait_until("toggle mode")
            self.play(*set_alpha([tab.rows[1]], 0.35),
                      FlashAround(tab.rows[2], time_width=1.5, buff=0.08), run_time=1.5)
            # every clock edge flips its output
            c.wait_until("every active")
            self.play(*flash(circ.q_labels, color=GREEN, time_width=1.5, buff=0.08), run_time=1.5)

    # ------------------------------------------------------------------ c4.ripple.2
    def clip2(self):
        circ = self.circ
        f0 = circ.ffs[0]
        self.P = f0.box.get_bottom()
        self.Pz = _p(-3.6, -0.9)
        self.Z = 1.5 / 0.85
        rest = [*circ.ffs[1:], *circ.ones[1:], *circ.stubs, *circ.feeds, *circ.dots, *circ.q_labels]
        self.rest = rest
        with self.say("c4.ripple.2") as c:
            # {bubble}: zoom on the first clock input
            zoom = [m.animate.scale(self.Z, about_point=self.P).shift(self.Pz - self.P) for m in (f0, circ.ones[0])]
            self.play(*during(disappear(self.tab, *rest), 0, 0.45), *during(zoom, 0.25, 1.0), run_time=2.0)

            # {triangle}: edge-triggered
            c.wait_until("triangle")
            self.play(f0.tri.animate.set_stroke(YELLOW), FlashAround(f0.tri, time_width=1.5, buff=0.1),
                      run_time=1.5)
            # {circle}: complemented
            c.wait_until("circle")
            self.play(f0.bub.animate.set_stroke(YELLOW), FlashAround(f0.bub, time_width=1.5, buff=0.08),
                      run_time=1.5)

            # {falling}: toggles on the falling edge
            fall = self.fall = edge_glyph("fall", _p(2.9, 2.1), w=2.8, h=0.7, tri=0.16)
            fall_l = self.fall_l = T("toggles on the falling edge", 36, YELLOW).move_to(_p(2.9, 1.15))
            c.wait_until("falling")
            self.play(*appear(fall, shift=None), run_time=1.0)
            c.wait_until(own_word=fall_l)
            self.play(*appear(fall_l), run_time=1.0)

            # so far: rising edge (ch3's plain-triangle T symbol, DIM)
            old = make_ff(ins=(("T", PIN_Y),))
            dim_symbol(old).scale(0.8)
            old.shift(_p(0.75, -1.0) - old.box.get_center())
            rise = edge_glyph("rise", _p(3.95, -1.1), w=2.4, h=0.6, color=DIM, tri=0.14)
            rise_l = T("so far: rising edge", 34, DIM).move_to(_p(3.95, -2.05))
            self.side = [fall, fall_l, old, rise, rise_l]
            c.wait_until("so far")
            self.play(*appear(old, rise, shift=None, lag=0.3), *during(appear(rise_l), 0.4, 1.0), run_time=1.5)
            c.wait_until("first to act")
            self.play(*flash([fall], color=YELLOW, time_width=1.5, buff=0.12), run_time=1.5)

    # ------------------------------------------------------------------ c4.ripple.3
    def clip3(self):
        circ = self.circ
        f0 = circ.ffs[0]
        with self.say("c4.ripple.3") as c:
            # {clock}: zoom back out; CLK into the first flip-flop only
            back = f0.copy().scale(1 / self.Z, about_point=self.Pz).shift(self.P - self.Pz)
            back.tri.set_stroke(FG)
            back.bub.set_stroke(FG)
            unzoom = [Transform(f0, back),
                      circ.ones[0].animate.scale(1 / self.Z, about_point=self.Pz).shift(self.P - self.Pz)]
            self.play(*during(disappear(*self.side), 0, 0.45), *during(unzoom, 0.2, 0.8),
                      *during(appear(*self.rest, shift=None, lag=0), 0.55, 1.0), run_time=1.8)
            self.play(*appear(circ.clk_l, shift=0.25 * UP),
                      VShowPassingFlash(f0.clk_w.copy().reverse_points().set_stroke(YELLOW, 12), time_width=0.6),
                      run_time=1.0)

            # {chain}: Q0 drives the second clock input
            c.wait_until("chain")
            self.play(VShowPassingFlash(circ.glow_path(0), time_width=0.6),
                      FlashAround(circ.ffs[1].tri, color=GREEN, time_width=1.5, buff=0.1), run_time=1.5)
            # {next}: Q1 drives the third
            c.wait_until("next")
            self.play(VShowPassingFlash(circ.glow_path(1), time_width=0.6),
                      FlashAround(circ.ffs[2].tri, color=GREEN, time_width=1.5, buff=0.1), run_time=1.5)

            # {notsync}: not the same clock
            warn = self.warn = T("not clocked using the same clock:\nnot a synchronous design", 34, RED,
                                 line_spacing=0.8)
            warn.move_to(_p(0.9, -2.75))
            c.wait_until("notsync")
            self.play(*flash([f.tri for f in circ.ffs], color=RED, time_width=1.5, buff=0.12),
                      *appear(warn), run_time=1.2)  # early: the slide's words, said over the next sentence

    # ------------------------------------------------------------------ c4.ripple.4
    def clip4(self):
        circ = self.circ
        head, rows, decs = count_column()
        with self.say("c4.ripple.4") as c:
            # {why}: the circuit shrinks to the top left; the count ring comes in
            settle(self, circ, add=[circ.clk_l])
            k = 0.5 / 0.85
            target = circ.copy().scale(k)
            target.clk_l.scale(1.6)
            for q in [*target.q_labels, *target.ones]:
                q.scale(1.3)
            for f in target.ffs:
                for l in f.labels:
                    l.scale(1.6)
                f.bub.set_stroke(width=2)
            target.move_to(_p(6.55 - target.width / 2, 3.5 - target.height / 2))
            ring = state_ring().scale(RING_K).move_to(RING_C)
            for m in [*ring.bits, *ring.decimals]:
                m.scale(1 / RING_K)
            ring_parts = [*ring.arrows, *ring.circles, *ring.bits, *ring.decimals]
            self.play(*during(disappear(self.warn), 0, 0.4),
                      *during([Transform(circ, target)], 0.2, 0.85), run_time=1.6)
            self.play(*appear(*ring_parts, shift=None, lag=0), run_time=1.0)

            # {column}: copies of the ring's states unroll into a column, 0 to 7 and back to 0
            c.wait_until("column")
            # (copies flying out of the ring crossed its middle, over its decimals: instead each row
            # fades in at its place while its ring node flashes, so nothing moves through the ring)
            unroll = []
            for r, v in enumerate(VALUES):
                unroll += during(appear(rows[r], shift=None), 0.08 * r, 0.08 * r + 0.36)
                if r < 8:   # the node's own outline pulses YELLOW and back (no square flash box)
                    unroll += during([ring.circles[v].animate(rate_func=there_and_back).set_stroke(YELLOW, 7)],
                                     0.08 * r, 0.08 * r + 0.36)
            self.play(*unroll, *during(appear(*head, shift=None, lag=0.1), 0.0, 0.3),
                      run_time=min(2.4, c.until("lsb") - 0.9))
            self.play(*appear(*decs, shift=None, lag=0.05), *set_alpha(ring_parts, 0.4), run_time=0.8)

            # {lsb}: Q0 flips every step
            c.wait_until("lsb")
            q0 = [rw[2] for rw in rows]
            self.play(*[time_span(m.animate.set_color(YELLOW), 0.18 * i, 0.18 * i + 0.4) for i, m in enumerate(q0)],
                      FlashUnder(head[2], time_width=1.5, buff=0.08), run_time=1.85)

            # {carry}: watch Q1 ... it flips when Q0 falls 1 -> 0
            c.wait_until("carry")
            self.play(*[m.animate.set_color(GREEN) for m in q0], head[1].animate.set_color(YELLOW),
                      FlashUnder(head[1], time_width=1.5, buff=0.08), run_time=1.2)
            arrows = [step_arrow(rows, r, 2, 1) for r in (1, 3, 5, 7)]
            c.wait_until("falls from one")
            self.play(*[GrowArrow(a) for a in arrows], *[time_span(rows[r + 1][1].animate.set_color(YELLOW),
                                                                   0.3 * i + 0.3, 0.3 * i + 0.8)
                                                         for i, r in enumerate((1, 3, 5, 7))],
                      run_time=2.0)
            c.wait_until("carry when")
            self.play(*flash(arrows, time_width=1.5, buff=0.06), run_time=1.3)

            # {edge}: a 1 -> 0 of Q0 is a falling edge on the second clock input
            box = SurroundingRectangle(VGroup(rows[1][2].copy(), rows[2][2].copy()), color=YELLOW, buff=0.1)
            box.set_stroke(YELLOW, 3)
            f0, f1 = circ.ffs[0], circ.ffs[1]
            # against the second flip-flop's clock input: between the Q0 feed's riser and f1's clock wire
            ex = f1.clk_w.get_x() - 0.55
            ey = f1.clk_w.get_center()[1]
            edge = edge_glyph("fall", _p(ex, ey), w=0.8, h=0.3, tri=0.09)
            c.wait_until("edge")
            self.play(FadeIn(box), run_time=0.6)
            self.play(*fly(box, edge), VShowPassingFlash(circ.glow_path(0).set_stroke(GREEN, 8), time_width=0.6),
                      run_time=1.5)
            self.play(FadeOut(box), run_time=0.5)

            # {same}: Q1's falls flip Q2
            arrows2 = [step_arrow(rows, r, 1, 0) for r in (3, 7)]
            c.wait_until("same")
            self.play(*[GrowArrow(a) for a in arrows2], head[0].animate.set_color(YELLOW),
                      *[rows[r + 1][0].animate.set_color(YELLOW) for r in (3, 7)], run_time=1.5)
