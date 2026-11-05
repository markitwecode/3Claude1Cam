"""Chapter 4, scene 4: the 3-bit ripple counter's timing diagram, delays drawn. Clips c4.timing.1 – c4.timing.4.

Timing style of ch2_s4_master (MathTex row labels, DIM guides) and ch3_s4_toggle (traces, ▼/▲ edge
marks). The diagram lives in the module-level helper `ripple_diagram()`: s5 and s6 copy it verbatim.
Ends on the bare diagram (labels, CLK, ▼ marks, guides, Q0..Q2, cause arrows), held, no fade-out:
s5 opens on exactly that frame.
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


# =============================================================================================
# Shared with ch4_s5 / ch4_s6 (copy verbatim): ripple_diagram()
# =============================================================================================
RD_X0, RD_X1 = -5.1, 6.3                 # waves run x0 -> x1
RD_P = (RD_X1 - RD_X0) / 8.9             # clock period (1.281)
RD_FALL = [RD_X0 + RD_P + k * RD_P for k in range(8)]   # falling edges (guides), k = 0..7
RD_D = 0.2                               # propagation delay, drawn as a gap
RD_ROW_Y = [2.9, 1.5, 0.1, -1.3]         # CLK, Q0, Q1, Q2
RD_AMP = 0.3                             # levels at row_y ± AMP
RD_STUB = RD_X0 + 0.55                   # end of the reset stub on the Q rows


def _rd_y(row, bit):
    return RD_ROW_Y[row] + (RD_AMP if bit else -RD_AMP)


def _rd_poly(row, pts, color, width=4):
    return (VMobject().set_points_as_corners([_p(x, _rd_y(row, b)) for x, b in pts])
            .set_stroke(color, width))


def _rd_pieces(row, edges, color=GREEN):
    """Q trace cut into pieces: [0] reset stub, [1] flat to the first change, [k+2] starts with change k."""
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
    """Small YELLOW arrow: a fall on row_from (at x_from) triggers the change on row_to (at x_to)."""
    a, b = _p(x_from, _rd_y(row_from, 0) - 0.06), _p(x_to, _rd_y(row_to, 1) + 0.06)
    return Arrow(a, b, buff=0, stroke_width=3, tip_length=0.16,
                 max_tip_length_to_length_ratio=0.35).set_color(YELLOW)


class RippleDiagram(VGroup):
    """3-bit ripple counter timing diagram (slide p. 94), delays drawn.
    Rows CLK (YELLOW), Q0, Q1, Q2 (GREEN) at RD_ROW_Y; labels right-aligned at x0 - 0.35.
    CLK starts low, rises half a period before each falling edge RD_FALL[k] (k = 0..7), ends low.
    Q0 changes at fall[k] + d; Q1 at fall[1,3,5,7] + 2d; Q2 at fall[3,7] + 3d (d = RD_D).
    Parts: .labels (MathTex, final colours) .clk .downs (YELLOW ▼ on CLK at each fall) .guides (DIM)
    .q[r] (pieces, see _rd_pieces) .causes1 (Q0 -> Q1, 4) .causes2 (Q1 -> Q2, 2)."""

    def __init__(self, **kw):
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
        self.add(self.guides, self.labels, self.clk, self.downs, *self.q[0], *self.q[1], *self.q[2],
                 *self.causes1, *self.causes2)


def ripple_diagram():
    return RippleDiagram()
# =============================================================================================


def edge_line(x, row, color=YELLOW, width=10):
    return Line(_p(x, _rd_y(row, 0)), _p(x, _rd_y(row, 1))).set_stroke(color, width)


def edge_flashes(xs, row, color=YELLOW):
    return [VShowPassingFlash(edge_line(x, row, color), time_width=1.0) for x in xs]


BITS_Y, COUNT_Y = -2.3, -3.0
COUNTS = [0, 1, 2, 3, 4, 5, 6, 7, 0]
BOUNDS = [RD_X0, *RD_FALL, RD_X1]


def stretch(j):
    return BOUNDS[j], BOUNDS[j + 1]


def cursor_box(j):
    a, b = stretch(j)
    top, bot = _rd_y(1, 1) + 0.22, COUNT_Y - 0.36
    return (Rectangle(width=b - a - 0.1, height=top - bot).move_to(_p((a + b) / 2, (top + bot) / 2))
            .set_stroke(YELLOW, 2, opacity=0.7).set_fill(YELLOW, 0.08).set_z_index(-3))


class Timing(NarratedScene):
    def construct(self):
        self.td = ripple_diagram()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        # end on the bare diagram, held: s5 opens on exactly this frame (no fade-out)
        self.wait(1.0)

    # ------------------------------------------------------------------------------------------
    def clip1(self):
        td = self.td
        with self.say("c4.timing.1") as c:
            for lab in td.labels:
                lab.set_color(DIM)
            self.play(*appear(*td.labels, lag=0.2, shift=0.2 * RIGHT),  # early: the diagram's empty frame, rows filled one by one
                      run_time=min(1.6, c.until("reset")))
            c.wait_until("reset")
            self.pulses = [_rd_poly(r, [(RD_X0 + 0.14, 0), (RD_X0 + 0.14, 1), (RD_X0 + 0.38, 1),
                                        (RD_X0 + 0.38, 0)], RED, 4) for r in (1, 2, 3)]
            self.clr = T("CLR", 28, RED).move_to(_p(RD_X0 + 0.26, (_rd_y(0, 0) + _rd_y(1, 1)) / 2))
            self.play(*[Create(td.q[r][0]) for r in range(3)],
                      *[lab.animate.set_color(GREEN) for lab in td.labels[1:]],
                      run_time=1.0)
            self.play(*[Create(p) for p in self.pulses], *appear(self.clr, shift=0.15 * DOWN),
                      run_time=1.2)
            c.wait_until("clk")
            self.play(Create(td.clk), td.labels[0].animate.set_color(YELLOW),
                      rate_func=linear, run_time=min(2.4, c.until("arrows") - 0.1))
            c.wait_until("arrows")
            self.play(*[time_span(FadeIn(u, shift=0.12 * DOWN), 0.15 * i, 0.15 * i + 0.5)
                        for i, u in enumerate(td.downs)],
                      *[time_span(GrowFromEdge(g, UP), 0.15 * i + 0.2, 0.15 * i + 0.9)
                        for i, g in enumerate(td.guides)],
                      run_time=2.0)

    # ------------------------------------------------------------------------------------------
    def clip2(self):
        td = self.td
        q0 = td.q[0]
        with self.say("c4.timing.2") as c:
            self.play(*disappear(*self.pulses, self.clr), Create(q0[1]), rate_func=linear,
                      run_time=min(1.4, c.until("up to one")))
            c.wait_until("up to one")
            self.play(Succession(*[Create(p, rate_func=linear, run_time=0.75) for p in q0[2:6]],
                                 *[Create(p, rate_func=linear, run_time=0.18) for p in q0[6:]]),
                      run_time=min(3.7, c.until("delay") - 0.1))

            # ---- zoom on the first edge
            c.wait_until("delay")
            Z, pt, to = 3.0, _p(RD_FALL[0] + RD_D / 2, 2.1), _p(0, 0.3)
            on = [m for m in self.mobjects if isinstance(m, VMobject)]
            self.play(*[m.animate.scale(Z, about_point=pt).shift(to - pt) for m in on],
                      run_time=min(2.0, c.until("that gap")))
            zx = lambda x: (x - pt[0]) * Z + to[0]   # noqa: E731
            zy = lambda y: (y - pt[1]) * Z + to[1]   # noqa: E731
            c.wait_until("that gap")
            hi = zy(_rd_y(1, 1))
            xa, xb, yb = zx(RD_FALL[0]), zx(RD_FALL[0] + RD_D), hi + 0.3
            self.brace = VGroup(Line(_p(xa, yb), _p(xb, yb)),
                                Line(_p(xa, yb - 0.18), _p(xa, yb + 0.18)),
                                Line(_p(xb, yb - 0.18), _p(xb, yb + 0.18))).set_stroke(GOLD, 5)
            self.play(GrowFromCenter(self.brace),
                      run_time=1.4)
            c.wait_until("prop")
            self.prop = set_backstroke(T("propagation delay", 40, GOLD), width=8)
            self.prop.next_to(self.brace, UP, buff=0.25)
            self.play(*appear(self.prop, shift=0.15 * DOWN), run_time=1.0)
            c.wait_until("in this part")
            self.play(*disappear(self.prop, self.brace), run_time=0.8)
            self.play(*[m.animate.shift(pt - to).scale(1 / Z, about_point=pt) for m in on], run_time=min(1.6, c.until() - 0.05))

    # ------------------------------------------------------------------------------------------
    def clip3(self):
        td = self.td
        q1, q2 = td.q[1], td.q[2]
        with self.say("c4.timing.3") as c:
            self.play(Create(q1[1]), FlashUnder(td.labels[2], time_width=1.5), rate_func=linear,
                      run_time=1.2)
            c.wait_until("falling edges")
            self.play(*edge_flashes(td.e0[1::2], 1), run_time=1.6)
            c.wait_until("q1first")
            a = td.causes1[0]
            self.play(*during([GrowArrow(a)], 0, 0.5), *during([Create(q1[2], rate_func=linear)], 0.45, 1),
                      run_time=1.8)
            c.wait_until("q1rest")
            self.play(*edge_flashes(td.e0[3::2], 1), run_time=1.5)
            c.wait_until("down up and down")
            anims = []
            for i, (a, p) in enumerate(zip(td.causes1[1:], q1[3:])):
                anims += during([GrowArrow(a)], i / 3, i / 3 + 0.15)
                anims += during([Create(p, rate_func=linear)], i / 3 + 0.13, (i + 1) / 3)
            self.play(*anims, run_time=min(2.4, c.until("q2") - 0.1))

            c.wait_until("q2")
            self.play(Create(q2[1]), FlashUnder(td.labels[3], time_width=1.5), rate_func=linear,
                      run_time=1.2)
            self.play(*edge_flashes(td.e1[1::2], 2), run_time=1.4)
            c.wait_until("first falls")
            self.play(*during([GrowArrow(td.causes2[0])], 0, 0.5),
                      *during([Create(q2[2], rate_func=linear)], 0.45, 1), run_time=1.8)
            c.wait_until("q2fall")
            self.play(*during([GrowArrow(td.causes2[1])], 0, 0.5),
                      *during([Create(q2[3], rate_func=linear)], 0.45, 1),
                      run_time=min(1.5, c.until("stair") - 0.05))

            # ---- the staircase at edges 4 and 8
            c.wait_until("stair")
            self.glow = []
            for k in (3, 7):
                for r in range(3):
                    self.glow.append(edge_line(RD_FALL[k] + (r + 1) * RD_D, r + 1, GOLD, 8))
            self.play(*[time_span(FadeIn(g), 0.25 * (i % 3), 0.25 * (i % 3) + 0.6)
                        for i, g in enumerate(self.glow)], run_time=1.4)
            self.play(*[FlashAround(VGroup(*self.glow[3 * j:3 * j + 3]).copy(), color=GOLD, time_width=1.5,
                                    buff=0.15) for j in range(2)], run_time=1.6)

    # ------------------------------------------------------------------------------------------
    def clip4(self):
        td = self.td
        with self.say("c4.timing.4") as c:
            self.head = MathTex("Q_2Q_1Q_0", font_size=34, color=GREEN)
            self.head.move_to(_p(0, BITS_Y)).align_to(_p(RD_X0 - 0.25, 0), RIGHT)
            self.play(*appear(self.head, shift=0.15 * DOWN), FlashUnder(td.labels[3], time_width=1.5),
                      run_time=1.4)
            self.bits, self.counts = [], []
            for j, v in enumerate(COUNTS):
                a, b = stretch(j)
                x = (a + b) / 2
                s = format(v, "03b")
                self.bits.append(T(" ".join(s), 32, GREEN).move_to(_p(x, BITS_Y)))
                self.counts.append(T(str(v), 46, GOLD).move_to(_p(x, COUNT_Y)))
            self.cursor = cursor_box(0)

            def step(j, rt, first=False):
                mv = FadeIn(self.cursor) if first else Transform(self.cursor, cursor_box(j))
                self.play(*during([mv], 0, 0.7),
                          *during(appear(self.bits[j], self.counts[j], lag=0.2), 0.15, 1), run_time=rt)

            for j, cue in enumerate(["r0", "r1", "r2", "r3", "r4"]):
                c.wait_until(cue)
                step(j, 1.0 if j == 0 else 0.6, first=(j == 0))
            c.wait_until("rest")
            step(5, 0.6)
            c.wait_until("six")
            step(6, 0.6)
            c.wait_until("seven")
            step(7, min(0.6, c.until("wrap")))
            c.wait_until("wrap")
            step(8, 0.8)
            c.wait_until("it counts")
            self.play(FlashAround(VGroup(*self.counts[:8]).copy(), color=GOLD, time_width=1.5, buff=0.15),
                      run_time=2.0)
        self.play(FadeOut(self.cursor, self.head, *self.bits, *self.counts, *self.glow), run_time=1.0)
