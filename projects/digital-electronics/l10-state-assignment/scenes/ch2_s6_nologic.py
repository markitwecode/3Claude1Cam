"""Chapter 2, scene 6: the ring needs no next-state logic: D_a = e, D_b = a, ...; unrolled into five
flip-flops on one clock with no gates; 27 unused states. Clips c2.wire.1 – c2.wire.3.

Shared visual owned here:
- ring_circuit(): the five-flip-flop ring (shift_reg_state_ass) in its final frame position, centred
  (0, -0.2), 12.93 wide x 4.02 tall (x -6.46..6.46, y -2.21..1.81). ch3 s1 opens on it; s7/s8 show it
  small (scale it). .ffs[i] (make_ff, a..e), .names[i], .feedback (Q_e -> D_a along the top),
  .clk, .out_arrow/.out_l ("output" on Q_b: a down arrow tapped off the Q_b -> D_c wire at
  x -0.74, y 0.19 -> -1.35, label T 40 GREEN below it centred (-1.12, -1.59), clear of the feedback wire).
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


# ---- s5's ring circle and table (ch2_s5_ring.py, copied verbatim) --------------------------------
RING = "abcde"
RING_STATES = ["00011", "00110", "01100", "11000", "10001"]   # e d c b a, one per clock state
RING_R = 1.75          # circle radius (cell centres)
RING_CELL = 0.85       # square cell side
CIRCLE_C = np.array([-3.6, 0.2, 0.0])
TABLE_C = np.array([3.4, 0.1, 0.0])


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


def ring_table(center=TABLE_C, rows=5):
    """The ring's transition table (p. 137), styled as s3's slide_table(): titles "Current state" /
    "Next state" (T 30 FG) over the blocks, header e d c b a | e′ d′ c′ b′ a′ (GREEN T 36), `rows`
    rows of Mono 36 digits (1s GOLD, 0s FG), DIM stroke-2 rules.

    .titles (VGroup of 2), .head_l / .head_r (VGroups of 5 GREEN letters), .hline, .vline,
    .cur[k][j] / .nxt[k][j] the digit of row k, column j (j = 0 is e, 4 is a). .row_y(k) row k's y."""
    c = np.array(center, dtype=float)
    lx = [c[0] - 3.1 + 0.6 * j for j in range(5)]
    rx = [c[0] + 0.7 + 0.6 * j for j in range(5)]
    hy = c[1] + 1.75
    ry = [c[1] + 0.7 - 0.7 * k for k in range(5)]
    titles = VGroup(T("Current state", 30).move_to([lx[2], hy + 0.65, 0]),
                    T("Next state", 30).move_to([rx[2] + 0.04, hy + 0.65, 0]))
    head_l = VGroup(*[T(RING[4 - j], 36, color=GREEN).move_to([lx[j], hy, 0]) for j in range(5)])
    head_r = VGroup(*[T(RING[4 - j] + "′", 36, color=GREEN).move_to([rx[j] + 0.08, hy, 0])
                      for j in range(5)])
    for m in [*head_l, *head_r]:
        m.align_to(head_l[0], DOWN) if m is not head_l[0] else None
    hline = Line([lx[0] - 0.4, hy - 0.42, 0], [rx[4] + 0.45, hy - 0.42, 0]).set_stroke(DIM, 2)
    vline = Line([c[0], hy + 0.35, 0], [c[0], ry[rows - 1] - 0.4, 0]).set_stroke(DIM, 2)

    def digit(d, x, y):
        return Mono(d, 36, color=GOLD if d == "1" else FG).move_to([x, y, 0])
    cur, nxt = [], []
    for k in range(rows):
        s, t = RING_STATES[k], RING_STATES[(k + 1) % 5]
        cur.append([digit(s[j], lx[j], ry[k]) for j in range(5)])
        nxt.append([digit(t[j], rx[j], ry[k]) for j in range(5)])
    g = VGroup(titles, head_l, head_r, hline, vline, *[d for r in cur + nxt for d in r])
    g.titles, g.head_l, g.head_r, g.hline, g.vline, g.cur, g.nxt = titles, head_l, head_r, hline, vline, cur, nxt
    g.row_y = lambda k: ry[k]
    return g


# ---- L6 ch6_s6_circuit's make_ff (D flip-flop), as copied in ch2_s1_hook.py ----------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
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


# ---- the ring circuit (shared: ch3 s1 opens on it, s7/s8 show it small) -------------------------
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


# ---- this scene's pieces ------------------------------------------------------------------------
TAB_POS = _p(-3.1, -0.05)
EQ_X = 1.75
CIRC_POS = _p(4.85, -0.05)
EQ_Y = [1.5, 0.65, -0.2, -1.05, -1.9]     # D_a .. D_e


def equation(i):
    """D_<ring[i]> = <ring[i-1]>: D BLUE, letters GREEN."""
    m = MathTex("D", "_" + RING[i], "=", RING[i - 1], font_size=56)
    m[0].set_color(BLUE)
    m[1].set_color(GREEN)
    m[3].set_color(GREEN)
    return m.move_to(_p(EQ_X, EQ_Y[i]))


def col_box(glyphs, color):
    return SurroundingRectangle(VGroup(*[g.copy() for g in glyphs]), color=color, buff=0.12,
                                corner_radius=0.08).set_stroke(color, 3)


def code_grid():
    codes = [format(n, "05b") for n in range(32)]
    used = set(RING_STATES)
    items = []
    for n, s in enumerate(codes):
        r, cidx = divmod(n, 8)
        items.append(Mono(s, 32).move_to(_p(-5.25 + 1.5 * cidx, 1.2 - 0.85 * r)))
    grid = VGroup(*items)
    grid.items = items
    grid.used = [m for m, s in zip(items, codes) if s in used]
    grid.unused = [m for m, s in zip(items, codes) if s not in used]
    return grid


def x_over(m, pad=0.08):
    l, r = m.get_left()[0] - pad, m.get_right()[0] + pad
    b, t = m.get_bottom()[1] - pad, m.get_top()[1] + pad
    return VGroup(Line(_p(l, b), _p(r, t)), Line(_p(l, t), _p(r, b))).set_stroke(FG, 3, opacity=0.7)


class NoLogic(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(0.15)

    # -- c2.wire.1: reading D_a .. D_e off the table ---------------------------------------------
    def clip1(self):
        with self.say("c2.wire.1") as c:
            tab = ring_table()
            tab.scale(0.95).move_to(TAB_POS)
            ring = ring_circle()
            ring.scale(0.75).move_to(CIRC_POS)
            self.tab, self.ring = tab, ring
            self.play(*appear(tab, ring, shift=None, lag=0.3), run_time=1.4)  # early: the table is shown whole, then read column by column
            dq = MathTex("D", r"=\ ?", font_size=60)
            dq[0].set_color(BLUE)
            dq.move_to(_p(EQ_X, 2.6))
            self.play(*appear(dq), run_time=1.0)
            self.dq = dq
            c.wait_until("da")

            # a' and e columns
            def pair(nj, cj):
                nb = col_box([tab.head_r[nj]] + [tab.nxt[k][nj] for k in range(5)], BLUE)
                cb = col_box([tab.head_l[cj]] + [tab.cur[k][cj] for k in range(5)], GREEN)
                return nb, cb

            nb, cb = pair(4, 0)
            self.play(FadeIn(nb), run_time=1.0)
            self.play(FadeIn(cb), run_time=1.0)
            eqs = [equation(i) for i in range(5)]
            self.eqs = eqs
            c.wait_until("So flip-flop A takes")
            self.play(*appear(eqs[0]), run_time=1.2)
            c.wait_until("db")

            order = [(1, 3, 4, None), (2, 2, 3, "see takes"), (3, 1, 2, "dee from see"), (4, 0, 1, "and flip-flop ee")]
            for n, (i, nj, cj, cue) in enumerate(order):
                if cue is not None:
                    c.wait_until(cue)
                nb2, cb2 = pair(nj, cj)
                rt = 1.5 if n == 0 else 0.8
                # fade out at the old columns, fade in at the new ones (no slide across others)
                self.play(*during([FadeOut(nb), FadeOut(cb)], 0, 0.45),
                          *during([FadeIn(nb2), FadeIn(cb2)], 0.5, 1), run_time=rt)
                nb, cb = nb2, cb2
                if n == 0:
                    c.wait_until("dee bee equals A")
                self.play(*appear(eqs[i]), run_time=0.9 if n == 0 else 0.6)
        self.col_boxes = (nb, cb)

    # -- c2.wire.2: it's the ring's wiring; unrolled, no gates -------------------------------------
    def clip2(self):
        tab, ring, eqs, dq = self.tab, self.ring, self.eqs, self.dq
        with self.say("c2.wire.2") as c:
            self.play(*set_alpha([tab], DIMMED), *disappear(dq, *self.col_boxes), run_time=0.8)
            # each equation lights with its arrow; e -> a last
            for i in [1, 2, 3, 4, 0]:
                arrow = ring.close if i == 0 else ring.arrows[i - 1]
                self.play(FlashAround(eqs[i], run_time=0.65, time_width=1.5),
                          VShowPassingFlash(arrow.copy().set_stroke(YELLOW, 8), time_width=0.6, run_time=0.65),
                          run_time=0.65)
            cap = T("each input is the output of the flip-flop before it", 36)
            cap.move_to(_p(0, -3.15))
            c.wait_until("Each flip-flop's input")
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("unroll")

            circ = ring_circuit()
            self.circ = circ
            # the circle fades out whole, then the five flip-flop boxes fade in (no cell morph/travel)
            leaving = [tab, *eqs, *ring.arrows, ring.close, *ring.labels, *ring.boxes]
            self.play(*during([FadeOut(m) for m in leaving], 0, 0.45),
                      *during([FadeIn(ff.box) for ff in circ.ffs], 0.5, 1),
                      *during([FadeIn(n) for n in circ.names], 0.7, 1),
                      run_time=2.0)
            rest_ff = VGroup(*[m for ff in circ.ffs for m in ff if m is not ff.box])
            clock = VGroup(circ.clk, *circ.dots, circ.clk_l)
            self.play(*appear(rest_ff, clock, shift=None, lag=0.4), run_time=1.6)
            c.wait_until("with one long wire")
            outp = VGroup(circ.out_arrow, circ.out_dot, circ.out_l)
            self.play(Create(circ.feedback), run_time=1.3)
            self.play(VShowPassingFlash(circ.feedback.copy().set_stroke(YELLOW, 9), time_width=0.4),
                      *appear(outp, shift=None), *during(disappear(cap), 0.3, 1), run_time=1.2)
            # put the circuit back on screen as one object
            self.remove(*[ff.box for ff in circ.ffs], *circ.names, rest_ff, clock, circ.feedback, outp)
            self.add(circ)
            c.wait_until("nogates")
            ng = T("no gates", 52, color=GOLD).move_to(_p(0, 2.75))
            self.play(*appear(ng), run_time=1.0)
            self.ng = ng
            c.wait_until()

    # -- c2.wire.3: 32 codes, 5 used, 27 don't cares ---------------------------------------------
    def clip3(self):
        with self.say("c2.wire.3") as c:
            grid = code_grid()
            c.wait_until("thirty-two")
            sweep_clear(self, time_span(FadeIn(grid), 0.6, 1.4), run_time=1.4)
            c.wait_until("we use only five")
            self.play(*[m.animate.set_color(GREEN) for m in grid.used],
                      *[m.animate.set_color(DIM) for m in grid.unused], run_time=1.5)
            c.wait_until("lots")
            quote = T("“Unused states. Lots!”", 44, slant=ITALIC).move_to(_p(0, 2.75))
            self.play(*appear(quote), run_time=1.0)
            c.wait_until("Twenty-seven")
            n27 = T("27", 72, color=GOLD).move_to(_p(0, -2.85))
            self.play(*appear(n27), run_time=1.0)
            c.wait_until("fine")
            xs = [x_over(m) for m in grid.unused]
            self.play(LaggedStart(*[FadeIn(x) for x in xs], lag_ratio=0.08), run_time=2.0)
            c.wait_until("remember")
            faint = interpolate_color(ManimColor(DIM), ManimColor(RED), 0.6)
            self.play(*[m.animate(rate_func=there_and_back).set_color(faint) for m in grid.unused],
                      *[x.animate(rate_func=there_and_back).set_stroke(faint) for x in xs], run_time=1.4)
            c.wait_until("They come back")
            self.play(FadeOut(VGroup(grid, *xs), scale=0.2), FadeOut(quote), FadeOut(n27),
                      run_time=min(1.4, c.until(floor=0.5)))
