"""Chapter 4, scene 5: where ripple goes wrong (7 -> 6 -> 4 -> 0, and the clock-speed limit). Clips c4.prob.1 – c4.prob.4.

Opens on s4's last frame (the bare ripple diagram, block below copied verbatim from ch4_s4_timing),
then zooms into the eighth falling edge. The zoom lives in module-level helpers so ch6 s6 can replay it:
ZoomStair() (labels, CLK, YELLOW guide + ▼, Q0..Q2), squeeze_clk() / slow_q0() -> fast_q0(), zoom_brackets() (3 GOLD delay brackets),
zoom_cursor(j), zoom_reading(j), trail_arrows(), readout_box(j). zmap/zinv map diagram
coordinates to/from the zoom. Ends on an empty frame.
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


# =============================================================================================
# The zoom at the eighth falling edge (7 -> 0). ch6 s6 replays it: keep these helpers self-contained.
# =============================================================================================
Z_WIN = (4.85, RD_X1)                    # diagram x-window shown by the zoom
Z_SCR = (-4.6, 6.3)                      # where that window lands on screen
Z_SX = (Z_SCR[1] - Z_SCR[0]) / (Z_WIN[1] - Z_WIN[0])   # 7.52
Z_SY = 0.82
Z_Y0 = 3.2                               # CLK row on screen (diagram row 2.9)


def zmap(p):
    return np.array([Z_SCR[0] + Z_SX * (p[0] - Z_WIN[0]), Z_Y0 + Z_SY * (p[1] - RD_ROW_Y[0]), p[2]])


def zinv(p):
    return np.array([Z_WIN[0] + (p[0] - Z_SCR[0]) / Z_SX, RD_ROW_Y[0] + (p[1] - Z_Y0) / Z_SY, p[2]])


Z_E = zmap(_p(RD_FALL[7], 0))[0]         # the 7 -> 0 edge on screen (-2.37)
Z_D = Z_SX * RD_D                        # one flip-flop delay on screen (1.50)
Z_ROW = [Z_Y0 + Z_SY * (y - RD_ROW_Y[0]) for y in RD_ROW_Y]   # 3.2, 2.05, 0.90, -0.24
Z_AMP = Z_SY * RD_AMP
Z_FALLS = [Z_E + (r + 1) * Z_D for r in range(3)]            # Q0, Q1, Q2 fall
Z_BRK_Y = [Z_ROW[r + 1] - Z_AMP - 0.2 for r in range(3)]     # delay bracket under each Q row
Z_TRAIL_Y = -1.6                        # the trail 7 -> 6 -> 4 -> 0
Z_FAST = Z_E + 2.5 * Z_D                 # the squeezed clock's next falling edge


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
    """The zoom: .labels (CLK, Q0..Q2, as the diagram's), .clk, .guide (YELLOW, at Z_E), .down (▼),
    .q[0..2] (one polyline each, falling at Z_FALLS[r])."""

    def __init__(self, **kw):
        super().__init__(**kw)
        texs = [r"\mathrm{CLK}", "Q_0", "Q_1", "Q_2"]
        cols = [YELLOW, GREEN, GREEN, GREEN]
        self.labels = VGroup(*[
            MathTex(t, font_size=40, color=c).move_to(_p(0, y)).align_to(_p(Z_SCR[0] - 0.35, 0), RIGHT)
            for t, c, y in zip(texs, cols, Z_ROW)])
        self.clk = clk_with_period(Z_P_SLOW)
        self.guide = zoom_guide(Z_E)
        self.down = zoom_down(Z_E)
        self.q = [_zfall(r + 1, x) for r, x in enumerate(Z_FALLS)]
        self.add(self.guide, self.labels, self.clk, *self.q, self.down)


Z_P_SLOW = 18.0                          # a period long enough that no other CLK edge is in the window
Z_P_FAST = 2.5 * Z_D                     # the squeezed clock: 2.5 delays


def clk_with_period(period):
    """CLK in the zoom with the given period, falling edge fixed at Z_E; edges clipped to the window.
    Always built from verticals and horizontals, so a squeeze can rebuild it frame by frame."""
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


def fast_clk():
    return clk_with_period(Z_P_FAST)


def squeeze_clk(clk, run_time=2.5):
    """The clock's period shrinks from Z_P_SLOW to Z_P_FAST; the trace is rebuilt every frame (no morph)."""
    def upd(m, alpha):
        m.become(clk_with_period(Z_P_SLOW * (Z_P_FAST / Z_P_SLOW) ** alpha))
    return UpdateFromAlphaFunc(clk, upd, run_time=run_time)


def _q0_pts(lift):
    """Q0 with the same corners before and after the squeeze: the level after the rise point is `lift`."""
    a, b = Z_FALLS[0], Z_FAST + Z_D
    return [(Z_SCR[0], 1), (a, 1), (a, 0), (b, 0), (b, lift), (Z_SCR[1], lift)]


def slow_q0():
    return _zpoly(1, _q0_pts(0), GREEN)


def fast_q0():
    """Q0 under the fast clock: falls at Z_E + d, rises again d after the next edge (same corners as slow_q0)."""
    return _zpoly(1, _q0_pts(1), GREEN)


def delay_bracket(x0, x1, y, color=GOLD):
    h = 0.14
    return VMobject().set_points_as_corners(
        [_p(x0, y + h), _p(x0, y), _p(x1, y), _p(x1, y + h)]).set_stroke(color, 4)


def zoom_brackets():
    """One GOLD bracket per delay: edge -> Q0 fall on Q0's row, Q0 -> Q1 on Q1's, Q1 -> Q2 on Q2's."""
    xs = [Z_E, *Z_FALLS]
    return [delay_bracket(xs[r] + 0.04, xs[r + 1] - 0.04, Z_BRK_Y[r]) for r in range(3)]


READS = [("111", 7, GREEN), ("110", 6, RED), ("100", 4, RED), ("000", 0, GREEN)]


def zoom_cursor(j):
    a, b = Z_E + j * Z_D, Z_E + (j + 1) * Z_D
    top, bot = _zy(0, 1) + 0.18, _zy(3, 0) - 0.45
    return (Rectangle(width=b - a - 0.08, height=top - bot).move_to(_p((a + b) / 2, (top + bot) / 2))
            .set_stroke(YELLOW, 2, opacity=0.7).set_fill(YELLOW, 0.08).set_z_index(-3))


TRAIL_PITCH = 2.85


def zoom_reading(j):
    """Reading j of the trail 7 -> 6 -> 4 -> 0, in place at Z_TRAIL_Y."""
    bits, v, col = READS[j]
    return T(f"{bits} = {v}", 36, col).move_to(_p((j - 1.5) * TRAIL_PITCH, Z_TRAIL_Y))


def trail_arrows():
    xs = [(j - 1.5) * TRAIL_PITCH for j in range(4)]
    half = 0.5 * T("111 = 7", 36).width
    return [Arrow(_p(xs[j] + half + 0.28, Z_TRAIL_Y), _p(xs[j + 1] - half - 0.28, Z_TRAIL_Y), buff=0,
                  stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.4).set_color(DIM)
            for j in range(3)]


def readout_box(j):
    """The readout highlight on trail entry j (slides along with the cursor)."""
    r = zoom_reading(j)
    return (Rectangle(width=r.width + 0.7, height=0.75).move_to(r).set_stroke(YELLOW, 2)
            .set_fill(YELLOW, 0.1).set_z_index(-1))
# =============================================================================================


def window_rect():
    lo, hi = _p(Z_WIN[0], _rd_y(3, 0) - 0.25), _p(Z_WIN[1], _rd_y(0, 1) + 0.25)
    return (Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1]).move_to((lo + hi) / 2)
            .set_stroke(YELLOW, 3))


QUOTE_Y = -2.85


def quote(text):
    return T(text, 28, FG, line_spacing=1.0).move_to(_p(0, QUOTE_Y))


class Problems(NarratedScene):
    def construct(self):
        td = ripple_diagram()
        # s4's last frame, already on screen: add the diagram's parts as top-level pieces (same order)
        self.add(*td.submobjects)
        self.td = td
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------------------------------
    def zoom_in(self, rt):
        td = self.td
        z = ZoomStair()
        self.z = z
        win = window_rect()
        self.play(FadeIn(win), FlashAround(td.guides[7].copy(), color=YELLOW, time_width=1.5),
                  run_time=0.8)
        # the diagram zooms (and fades) while the zoom's own pieces grow from their pre-images
        old = [td.guides, td.clk, td.downs, *td.q[0], *td.q[1], *td.q[2], *td.causes1, *td.causes2]
        anims = []
        for m in old:
            m.generate_target()
            m.target.apply_function(zmap).set_opacity(0)
            anims.append(MoveToTarget(m))
        win.generate_target()
        win.target.apply_function(zmap).set_stroke(opacity=0)
        anims.append(MoveToTarget(win))
        for m in [z.clk, *z.q, z.guide]:
            m.generate_target()
            m.apply_function(zinv)
            anims.append(MoveToTarget(m))
        z.guide.set_stroke(DIM, 1.5)
        for lab, dst in zip(td.labels, z.labels):
            anims.append(lab.animate.move_to(dst))
        self.add(z.guide, z.clk, *z.q)
        self.play(*anims, run_time=rt)
        self.remove(win, *old, *td.labels)
        self.add(z.labels)
        self.play(GrowFromCenter(z.down), run_time=0.5)

    def clip1(self):
        with self.say("c4.prob.1") as c:
            self.zoom_in(rt=min(2.2, c.until("still") - 1.6))
            z = self.z
            # ---- the cursor walks the staircase; one reading per stretch
            self.brk = zoom_brackets()
            self.reads = [zoom_reading(j) for j in range(4)]
            self.cursor = zoom_cursor(0)
            self.box = readout_box(0)
            self.arrows = trail_arrows()
            c.wait_until("still")
            self.play(FadeIn(self.cursor), *during([FadeIn(self.box)], 0.2, 0.7),
                      *during(appear(self.reads[0]), 0.4, 1), run_time=1.6)
            for j, cue in ((1, "six"), (2, "four"), (3, "zero")):
                c.wait_until(cue)
                edge = Line(_p(Z_FALLS[j - 1], _zy(j, 0)), _p(Z_FALLS[j - 1], _zy(j, 1))).set_stroke(YELLOW, 10)
                # cursor column and trail box move together, on the word
                self.play(Transform(self.cursor, zoom_cursor(j)), Transform(self.box, readout_box(j)),
                          GrowFromCenter(self.brk[j - 1]), run_time=0.8)
                self.play(VShowPassingFlash(edge, time_width=1.0), *during([GrowArrow(self.arrows[j - 1])], 0, 0.5),
                          *during(appear(self.reads[j]), 0.3, 1), run_time=0.8)
            # ---- the trail 7 -> 6 -> 4 -> 0 stays
            c.wait_until("passed")
            self.play(FadeOut(self.cursor), FadeOut(self.box), run_time=1.0)
            self.play(*flash([self.reads[1], self.reads[2]], color=RED, time_width=1.5), run_time=1.8)

    # ------------------------------------------------------------------------------------------
    def clip2(self):
        with self.say("c4.prob.2") as c:
            self.q1 = quote("See outputs do not change at the same time, i.e., synchronously.\n"
                            "So hard to know when count output is actually valid.")
            self.play(*appear(self.q1), run_time=1.2)
            c.wait_until("different times")
            edges = [Line(_p(x, _zy(r + 1, 0)), _p(x, _zy(r + 1, 1))).set_stroke(YELLOW, 10)
                     for r, x in enumerate(Z_FALLS)]
            self.play(*[time_span(VShowPassingFlash(e, time_width=1.0), 0.5 * i, 0.5 * i + 0.9)
                        for i, e in enumerate(edges)], run_time=1.9)
            c.wait_until("valid")
            self.qmarks = [T("?", 48, RED, weight=BOLD).next_to(self.reads[j], UP, buff=0.18) for j in (1, 2)]
            self.play(*appear(*self.qmarks, lag=0.3), run_time=1.2)
            c.wait_until("read the outputs")
            self.play(*flash([self.reads[1], self.reads[2]], color=RED, time_width=1.5), run_time=1.8)

    # ------------------------------------------------------------------------------------------
    def clip3(self):
        z = self.z
        with self.say("c4.prob.3", gap=1.6) as c:
            self.play(*disappear(self.q1, *self.reads, *self.arrows, *self.qmarks), run_time=0.9)
            # the three delays slide down onto one line, end to end
            self.play(*[b.animate.set_y(Z_BRK_Y[2]) for b in self.brk[:2]], run_time=1.5)
            self.total = (MathTex(r"3\ \text{stages} \;\rightarrow\; 3\ \text{delays}", font_size=44, color=GOLD)
                          .move_to(_p((Z_E + Z_FALLS[2]) / 2, -1.25)))
            c.wait_until("three")
            self.play(*appear(self.total), run_time=1.0)
            c.wait_until("general")
            self.ntotal = (MathTex(r"n\ \text{stages} \;\rightarrow\; n\ \text{delays}", font_size=44, color=GOLD)
                           .move_to(self.total))
            self.play(*swap(self.total, self.ntotal), run_time=1.2)
            # ---- squeeze the clock
            c.wait_until("fast")
            self.play(squeeze_clk(z.clk, run_time=2.5))
            c.wait_until("early")
            self.g2 = zoom_guide(Z_FAST)
            self.d2 = zoom_down(Z_FAST)
            self.play(GrowFromEdge(self.g2, UP), GrowFromCenter(self.d2), run_time=1.2)
            # same corner structure: only the level after the rise point lifts (verticals stay vertical)
            z.q[0].become(slow_q0())
            self.play(Transform(z.q[0], fast_q0()), run_time=1.0)
            c.wait_until("wrong")
            self.bad = T("100 = 4", 34, RED).move_to(_p(Z_FAST, -1.9))
            self.not0 = T("not 0", 34, RED, weight=BOLD).next_to(self.bad, RIGHT, buff=0.4)
            self.play(*appear(self.bad), run_time=1.0)
            self.play(*appear(self.not0), run_time=0.8)
            c.wait_until("limit")
            self.q2 = quote("Propagation delay builds up from stage to stage,\n"
                            "limiting maximum clock speed before miscounting occurs.").set_y(-2.85)
            self.play(*appear(self.q2), run_time=1.2)

    # ------------------------------------------------------------------------------------------
    def clip4(self):
        with self.say("c4.prob.4") as c:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
            title = T("The ripple counter", 52).move_to(_p(0, 2.5))
            self.play(*appear(title), run_time=0.8)
            div = Line(_p(0, 1.3), _p(0, -2.3)).set_stroke(DIM, 2)
            good_h = T("very simple", 48, GREEN).move_to(_p(-3.5, 0.7))
            good_b = T("just string\nflip-flops together", 38, FG, line_spacing=1.1).next_to(good_h, DOWN, buff=0.45)
            bad_h = T("not synchronous", 48, RED).move_to(_p(3.5, 0.7))
            bad_b = T("outputs change\nat different times", 38, FG, line_spacing=1.1).next_to(bad_h, DOWN, buff=0.45)
            c.wait_until("simple")
            self.play(FadeIn(div), *appear(good_h, good_b, lag=0.4), run_time=1.4)
            c.wait_until("rules")
            self.play(*appear(bad_h, bad_b, lag=0.2), run_time=1.0)
        self.wait(1.6)
