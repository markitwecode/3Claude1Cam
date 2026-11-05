"""Chapter 3, scene 7: recap in six panels, then the teaser for Part 4 (metastability).
Clips c3.recap.1 – c3.recap.2.

Panels (ch1_s8 / ch2_s6 styling: no frames, a T 30 line under each, earlier panels dimmed by a BG veil):
3 x 2 grid, columns x = -4.55, 0, 4.55 (r6 at 4.45); centres y 2.3 / -1.05; lines from y 0.95 / -2.2 down.
 r1 ch3_s1's clock_board() (no lettering) with one pulse spreading and the ticks on the time axis,
 r2 ch3_s2's split path (lettering off, 0.65) over its small CLK0 / CLK1 traces and the TEAL t_skew,
 r3 ch3_s3's four-segment budget bar (drawn 3.6 wide, no symbols) under its inequality (MathTex 34),
 r4 ch1_s7's 1 ns bar (unit 3.6): the skew slides in, the PURPLE logic shrinks 0.7 -> 0.6 ns, a ghost of 0.7 stays,
 r5 ch3_s5's hold view cut to CLK1's edge: GOLD band + t_hold, TEAL/PINK/PURPLE chain under a brace, GREEN tick,
 r6 ch3_s6's skew_fences(+0.1) -> skew_fences(-0.1) (L 3.2), "easier"/"harder" under the fences, swapping.
Teaser: a push button wired to a flip-flop's D (BLUE), the clock ticking; ch1_s3's WindowDiagram
(k 0.5, origin (3.3, 0.7)) with a RED dashed change of D inside the GOLD window and a RED "???" on Q.
End card: "Part 4 · Metastability and the synchroniser" T 40 FG at (0, -2.85).
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
# r1: ch3_s1_hook.py's clock_board()
# =============================================================================================
BD_W, BD_H, BD_C = 12.4, 5.0, (0.0, 0.9)
FFB_W, FFB_H = 0.6, 0.8
COLS_X = (-3.8, -1.6, 0.6, 2.8, 5.0)
ROWS_Y = (2.5, 1.0, -0.5)
SPINE_X = -5.0
SRC_C = (-5.7, 0.25)
AXIS_Y = -2.7
AXIS_X0, AXIS_X1 = -5.6, 1.2
TICK_X0, TICK_X1 = -5.25, 0.6
BOARD_SLOTS = [(0, 0), (1, 0), (2, 0),
               (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
               (0, 2), (2, 2), (3, 2), (4, 2)]


def small_ff(center):
    r = Rectangle(width=FFB_W, height=FFB_H).set_stroke(FG, 3).set_fill(BG, 1)
    hb = FFB_H / 2
    tri = Polygon(_p(-0.11, -hb), _p(0.11, -hb), _p(0, -hb + 0.17)).set_stroke(FG, 2.5).set_fill(BG, 1)
    g = VGroup(r, tri).move_to(_p(*center))
    g.rect, g.tri = r, tri
    return g


def clock_board():
    B = VGroup()
    B.rect = RoundedRectangle(corner_radius=0.3, width=BD_W, height=BD_H).move_to(_p(*BD_C))
    B.rect.set_stroke(DIM, 2).set_fill("#181B22", 1)
    B.src = VGroup(
        RoundedRectangle(corner_radius=0.1, width=0.6, height=0.6).set_stroke(YELLOW, 3).set_fill(BG, 1),
        VMobject().set_points_as_corners([_p(-0.2, -0.1), _p(-0.08, -0.1), _p(-0.08, 0.1), _p(0.08, 0.1),
                                          _p(0.08, -0.1), _p(0.2, -0.1)]).set_stroke(YELLOW, 3),
    ).move_to(_p(*SRC_C))
    s0 = B.src.get_right()
    B.boxes, B.branches, B.lengths = [], [], []
    for ci, ri in BOARD_SLOTS:
        x, y = COLS_X[ci], ROWS_Y[ri]
        b = small_ff((x, y))
        ch = y - FFB_H / 2 - 0.35
        pts = [s0, _p(SPINE_X, s0[1]), _p(SPINE_X, ch), _p(x, ch), _p(x, y - FFB_H / 2)]
        br = VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 4)
        B.boxes.append(b)
        B.branches.append(br)
        B.lengths.append(sum(np.linalg.norm(pts[k + 1] - pts[k]) for k in range(len(pts) - 1)))
    B.tree = VGroup(*B.branches)
    B.add(B.rect, B.tree, *B.boxes, B.src)
    L_max = max(B.lengths)
    B.axis = Arrow(_p(AXIS_X0, AXIS_Y), _p(AXIS_X1, AXIS_Y), buff=0, stroke_width=3,
                   max_tip_length_to_length_ratio=0.04).set_color(DIM)

    def tick(i, color=YELLOW):
        x = TICK_X0 + (TICK_X1 - TICK_X0) * B.lengths[i] / L_max
        return Line(_p(x, AXIS_Y - 0.25), _p(x, AXIS_Y + 0.25)).set_stroke(color, 5)
    B.tick = tick
    B.tick0 = Line(_p(TICK_X0, AXIS_Y - 0.25), _p(TICK_X0, AXIS_Y + 0.25)).set_stroke(DIM, 4)
    return B


# =============================================================================================
# r2: make_ff / path_diagram / split_path from ch3_s3_skewsetup.py; small traces from ch3_s2_skew.py
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
P_FF_X = (-4.4, 4.4)
P_FF_Y = 0.5
P_PIN = P_FF_Y + PIN_Y
P_BUS = P_FF_Y - BOX_H / 2 - EN_WIRE
P_BUS_X0 = -5.6
P_CL_W, P_CL_H = 3.4, 1.6
SRC_X, SRC_R = 6.25, 0.3
LONG_Y = -2.55
TRI_Y = P_FF_Y - BOX_H / 2 - 0.02
CLK1_OP = 0.55


def make_ff(center=ORIGIN):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    g = VGroup(d_w, q_w, qb_w, box, tri)
    g.box, g.tri = box, tri
    g.shift(center)
    return g


def split_path_shapes():
    """split_path() without any lettering: FF0, FF1, CL, wires, the source and both clock branches."""
    P = VGroup()
    P.ff0, P.ff1 = [make_ff(_p(x, P_FF_Y)) for x in P_FF_X]
    x_q0 = P_FF_X[0] + BOX_W / 2 + WIRE
    x_d1 = P_FF_X[1] - BOX_W / 2 - WIRE
    P.cl = Rectangle(width=P_CL_W, height=P_CL_H).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(0, P_PIN))
    P.q0_w = Line(_p(x_q0, P_PIN), _p(-P_CL_W / 2, P_PIN)).set_stroke(GREEN, 5)
    P.d1_w = Line(_p(P_CL_W / 2, P_PIN), _p(x_d1, P_PIN)).set_stroke(BLUE, 5)
    ring = Circle(radius=SRC_R).set_stroke(YELLOW, 4).set_fill(BG, 1)
    sq = VMobject().set_points_as_corners([_p(-0.17, -0.08), _p(-0.08, -0.08), _p(-0.08, 0.08),
                                           _p(0.04, 0.08), _p(0.04, -0.08), _p(0.17, -0.08)])
    sq.set_stroke(YELLOW, 3)
    P.src = VGroup(ring, sq).move_to(_p(SRC_X, P_BUS))
    x0, x1 = P_FF_X
    P.clk_br1 = VMobject().set_points_as_corners([_p(SRC_X - SRC_R, P_BUS), _p(x1, P_BUS), _p(x1, TRI_Y)])
    P.clk_br1.set_stroke(YELLOW, 5, opacity=CLK1_OP)
    P.clk_br0 = VMobject().set_points_as_corners([_p(SRC_X, P_BUS - SRC_R), _p(SRC_X, LONG_Y),
                                                  _p(x0, LONG_Y), _p(x0, TRI_Y)])
    P.clk_br0.set_stroke(YELLOW, 5)
    P.add(P.clk_br0, P.clk_br1, P.ff0, P.ff1, P.cl, P.q0_w, P.d1_w, P.src)
    return P


WAVE_W = 4
ROW_H = 0.8
SLOPE = 0.35
GUIDE_W = 1.5
DIM_W = 3


def clock_wave(x0, x1, y, edges, h=ROW_H, slope=SLOPE, color=YELLOW, start_low=True, width=WAVE_W):
    lo, hi = y - h / 2, y + h / 2
    level = lo if start_low else hi
    pts = [np.array([x0, level, 0])]
    for xc in edges:
        other = hi if level == lo else lo
        pts.append(np.array([xc - slope / 2, level, 0]))
        pts.append(np.array([xc + slope / 2, other, 0]))
        level = other
    pts.append(np.array([x1, level, 0]))
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)


def guide(x, y_top, y_bot, color=DIM, width=GUIDE_W):
    return Line([x, y_top, 0], [x, y_bot, 0]).set_stroke(color, width)


def harrow(xa, xb, y, color):
    return DoubleArrow(_p(xa, y), _p(xb, y), buff=0, stroke_width=DIM_W, tip_length=0.14,
                       max_tip_length_to_length_ratio=0.4, color=color)


# ch3_s2's small-trace geometry
S2_PS, S2_PS_C = 0.65, _p(0, 1.8)
S2_TW = (-4.6, 2.4)
S2_TY0, S2_TY1, S2_TYSK = -0.7, -1.85, -2.55
S2_CE = [-2.6, -0.6, 1.4]
S2_SK = 0.7


# =============================================================================================
# r3 / r4 / r6: THE lecture's budget bar (ch1_s6), ch1_s7's padlock, ch3_s6's skew_fences()
# =============================================================================================
BAR_H = 0.5
BAR_FILL = 0.85
BAR_OUT_W = 3


def budget_bar(segs, total, x0=-3.3, y=0.0, tc_tex="T_c", h=BAR_H, tc_size=44):
    g = VGroup()
    g.segs = []
    x = x0
    for col, w in segs:
        r = Rectangle(width=w, height=h).set_stroke(width=0).set_fill(col, BAR_FILL)
        r.move_to([x + w / 2, y, 0])
        g.segs.append(r)
        x += w
    g.outline = Rectangle(width=total, height=h).set_stroke(YELLOW, BAR_OUT_W).set_fill(opacity=0)
    g.outline.move_to([x0 + total / 2, y, 0]).set_z_index(1)
    g.tc = MathTex(tc_tex, font_size=tc_size, color=YELLOW).next_to(g.outline, LEFT, buff=0.25)
    g.add(*g.segs, g.outline, g.tc)
    return g


def padlock(scale=1.0):
    body = RoundedRectangle(corner_radius=0.04, width=0.26, height=0.2)
    body.set_fill(BG, 1).set_stroke(width=0)
    shackle = Arc(radius=0.085, start_angle=0, angle=PI).set_stroke(BG, 3.5)
    shackle.move_to(body.get_top() + 0.075 * UP)
    lock = VGroup(shackle, body)
    lock.scale(scale)
    return lock


def tc_arrow(xa, xb, y):
    return DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.4, color=YELLOW)


def skew_fences(skew, x0, y, L, hold=0.3, su=0.1, lo=0.4, hi=0.8):
    """ch3_s6's skew_fences() without "D1 may change" and the TEAL skew arrows."""
    H = VGroup()
    H.bar = budget_bar([(GOLD, su * L)], L, x0=x0, y=y)
    seg = H.bar.segs[0].shift((1 - su - skew) * L * RIGHT)
    H.su = seg
    H.arrow = tc_arrow(x0, x0 + L, y - BAR_H / 2 - 0.3)
    H.edges = VGroup(*[Arrow([x, y + 0.3, 0], [x, y + 0.95, 0], buff=0, stroke_width=4, tip_length=0.2,
                             max_tip_length_to_length_ratio=0.4, color=YELLOW) for x in (x0, x0 + L)])
    xf, xd = x0 + (hold - skew) * L, x0 + (1 - su - skew) * L
    H.fence = Line([xf, y - 0.45, 0], [xf, y + 0.45, 0]).set_stroke(GOLD, 7).set_z_index(2)
    H.deadline = Line([xd, y - 0.45, 0], [xd, y + 0.45, 0]).set_stroke(GOLD, 4).set_z_index(2)
    H.fence_l = MathTex("t_{hold}", font_size=36, color=GOLD).next_to(H.fence, UP, buff=0.1)
    H.su_l = MathTex("t_{su}", font_size=34, color=GOLD)
    dx = 0.08 if skew > 0 else (0.16 if skew < 0 else -0.08)
    H.su_l.move_to([seg.get_x() + dx, 0, 0]).align_to(H.fence_l, DOWN)
    if skew < 0:
        H.fence_l.align_to(_p(xf - 0.1, 0), RIGHT)
    a, b = x0 + lo * L, x0 + hi * L
    box = Rectangle(width=b - a, height=BAR_H).set_stroke(BLUE, 3).set_fill(BLUE, 0.22)
    box.move_to([(a + b) / 2, y, 0])
    hl = VGroup(*[Line([x, y - BAR_H / 2, 0], [x + BAR_H, y + BAR_H / 2, 0]).set_stroke(BLUE, 2)
                  for x in np.arange(a + 0.08, b - BAR_H, 0.3)])
    H.stretch = VGroup(box, hl)
    H.xf, H.xd = xf, xd
    H.skseg = None
    H.add(H.bar, H.arrow, H.edges, H.stretch, H.fence, H.deadline, H.fence_l, H.su_l)
    if skew > 0:
        H.skseg = Rectangle(width=skew * L, height=BAR_H).set_stroke(width=0).set_fill(TEAL, BAR_FILL)
        H.skseg.move_to([x0 + (1 - skew / 2) * L, y, 0])
        H.add(H.skseg)
    return H


# =============================================================================================
# teaser: ch1_s3_ffnumbers.py's WindowDiagram (with its dim_arrow)
# =============================================================================================
def dim_arrow(a, b, color, base_a=None, base_b=None, width=3, tip=0.14):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    arrow = DoubleArrow(a, b, buff=0, stroke_width=width, tip_length=tip,
                        max_tip_length_to_length_ratio=0.4).set_color(color)
    guides = VGroup()
    for p, base in ((a, base_a), (b, base_b)):
        if base is None:
            continue
        over = 0.15 if base < p[1] else -0.15
        guides.add(Line(_p(p[0], base), _p(p[0], p[1] + over)).set_stroke(DIM, 1.5))
    g = VGroup(guides, arrow)
    g.arrow, g.guides = arrow, guides
    return g


class WindowDiagram:
    T_SU, T_HOLD, T_PC = 1.3, 1.0, 1.7
    X0, X1, PITCH, AMP = -4.6, 4.6, 2.0, 0.3

    def __init__(self, origin=ORIGIN, k=1.0, fs=1.0):
        self.o, self.k, self.fs = np.array(origin, dtype=float), k, fs
        P, A, H = self.P, self.AMP, self.PITCH
        self.row_y = [H, 0.0, -H]
        sw = 4 * max(k, 0.8)
        self.sw = sw
        self.lab_clk, self.lab_d, self.lab_q = [
            MathTex(t, font_size=44 * fs, color=c).move_to(P(0, y)).align_to(P(self.X0 - 0.3, 0), RIGHT)
            for t, c, y in zip([r"\mathrm{CLK}", "D", "Q"], [YELLOW, BLUE, GREEN], self.row_y)]
        self.guide = Line(P(0, H + A + 0.3), P(0, -H - A - 0.2)).set_stroke(DIM, 1.5).set_z_index(-2)
        self.up = (Triangle().scale(0.12 * max(k, 0.8)).set_stroke(width=0).set_fill(YELLOW, 1)
                   .move_to(P(0, H)))
        self.clk = self.path(0, [(self.X0, 1), (-2.3, 1), (-2.3, 0), (0, 0), (0, 1), (2.3, 1),
                                 (2.3, 0), (self.X1, 0)], YELLOW, sw)
        ya = A + 0.55
        self.su = dim_arrow(P(-self.T_SU, ya), P(0, ya), GOLD, P(0, A)[1], P(0, A)[1])
        self.hold = dim_arrow(P(0, ya), P(self.T_HOLD, ya), GOLD, P(0, A)[1], P(0, A)[1])
        mt = 44 * fs
        self.sym_su = MathTex(r"t_{\mathrm{su}}", font_size=mt, color=GOLD).next_to(self.su.arrow, LEFT, buff=0.15)
        self.sym_hold = MathTex(r"t_{\mathrm{hold}}", font_size=mt, color=GOLD).next_to(self.hold.arrow, RIGHT, buff=0.15)
        self.band = (Rectangle(width=k * (self.T_SU + self.T_HOLD), height=k * (2 * A + 0.3))
                     .set_stroke(width=0).set_fill(GOLD, 0.25).set_z_index(-3)
                     .move_to(P((self.T_HOLD - self.T_SU) / 2, 0)))
        self.one_q = T("1", max(28, 36 * fs), GREEN).move_to(P(2.9, -H))

    def P(self, x, y):
        return self.o + self.k * np.array([x, y, 0.0])

    def path(self, row, pts, color, width):
        y0 = self.row_y[row]
        return (VMobject().set_points_as_corners([self.P(x, y0 + (self.AMP if b else -self.AMP)) for x, b in pts])
                .set_stroke(color, width))

    def d_change(self, x, color=RED):
        return DashedLine(self.P(x, self.AMP), self.P(x, -self.AMP), dash_length=0.1).set_stroke(color, 5)

    def q_unknown(self):
        return T("???", max(30, 38 * self.fs), RED).move_to(self.one_q)


# =============================================================================================
# recap layout (ch1_s8 / ch2_s6)
# =============================================================================================
COL_X = (-4.55, 0.0, 4.55)
TOP_Y, BOT_Y = 2.3, -1.4
TOP_CAP, BOT_CAP = 0.85, -2.6
PANEL_W = 4.2
CAP = 30
VEIL = 0.45


def fit(mob, w, h, center):
    mob.scale(min(w / mob.width, h / mob.height)).move_to(center)
    return mob


def caption(lines, x, top):
    g = VGroup(*lines).arrange(DOWN, buff=0.14)
    if g.width > PANEL_W + 0.2:
        g.scale_to_fit_width(PANEL_W + 0.2)
    g.move_to([x, 0, 0]).align_to([0, top, 0], UP)
    return g


def colored_tex(parts, colors, size=34):
    m = MathTex(*parts, font_size=size)
    for i, col in colors.items():
        m[i].set_color(col)
    return m


def veil(mob):
    return (Rectangle(width=mob.width + 0.3, height=mob.height + 0.3).set_stroke(width=0)
            .set_fill(BG, VEIL).move_to(mob).set_z_index(20))


class Recap3(NarratedScene):
    def construct(self):
        self.panels = []
        self.clip1()
        self.clip2()
        self.wait(8.0)   # end card; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def dim_previous(self):
        out = []
        for p in self.panels:
            if not getattr(p, "veiled", False):
                p.veiled = True
                out.append(FadeIn(veil(p)))
        return out

    # -- c3.recap.1: the six panels ----------------------------------------------------------------
    def clip1(self):
        with self.say("c3.recap.1", gap=1.6) as c:
            self.r1(c)
            self.r2(c)
            self.r3(c)
            self.r4(c)
            self.r5(c)
            self.r6(c)

    def r1(self, c):
        B = clock_board()
        ticks = [B.tick(i) for i in range(len(B.boxes))]
        grp = VGroup(B, B.axis, B.tick0, *ticks)
        fit(grp, PANEL_W, 2.2, _p(COL_X[0], TOP_Y))
        t_lab = MathTex("t", font_size=34, color=DIM).next_to(B.axis, RIGHT, buff=0.12)
        cap = caption([T("edges arrive", CAP), T("at different times", CAP)], COL_X[0], TOP_CAP)
        c.wait_until("r1")
        self.play(FadeIn(B), FadeIn(B.axis), FadeIn(B.tick0), *appear(t_lab, shift=None), run_time=1.2)
        # one edge leaves the source and spreads down every branch at the same speed
        c.wait_until("travel")
        L = B.lengths
        v = max(L) / 2.6
        anims = []
        end = 0.0
        for i, br in enumerate(B.branches):
            arr = L[i] / v
            tw = 0.3
            pulse = br.copy().set_stroke(YELLOW, 7)
            anims.append(time_span(VShowPassingFlash(pulse, time_width=tw, rate_func=linear), 0.0, arr * (1 + tw)))
            anims.append(time_span(B.boxes[i].rect.animate.set_stroke(YELLOW), arr, arr + 0.3))
            anims.append(time_span(FadeIn(ticks[i]), arr, arr + 0.3))
            end = max(end, arr * (1 + tw), arr + 0.3)
        self.play(FlashAround(B.src, color=YELLOW, buff=0.05), *anims, run_time=end)
        c.wait_until("different moments")
        self.play(*appear(*cap, shift=None, lag=0.3), run_time=1.0)  # early: the panel's summary line
        self.panels.append(VGroup(grp, t_lab, cap))

    def r2(self, c):
        P = split_path_shapes()
        P.scale(S2_PS).move_to(S2_PS_C)
        x0, x1 = S2_TW
        clk0 = clock_wave(x0, x1, S2_TY0, S2_CE)
        clk1 = clock_wave(x0, x1, S2_TY1, [e - S2_SK for e in S2_CE]).set_stroke(opacity=CLK1_OP)
        g_e = guide(S2_CE[0], S2_TY0 + ROW_H / 2, S2_TYSK - 0.15)
        g_k = guide(S2_CE[0] - S2_SK, S2_TY1 - ROW_H / 2, S2_TYSK - 0.15)
        sk = harrow(S2_CE[0] - S2_SK, S2_CE[0], S2_TYSK, TEAL)
        grp = VGroup(P, clk0, clk1, g_e, g_k, sk)
        fit(grp, 3.4, 2.0, _p(COL_X[1] + 0.35, TOP_Y + 0.15))
        lab0 = T("CLK0", 28, YELLOW).next_to(clk0, LEFT, buff=0.12)
        lab1 = T("CLK1", 28, YELLOW).set_opacity(0.7).next_to(clk1, LEFT, buff=0.12)
        sk_l = MathTex("t_{skew}", font_size=32, color=TEAL).next_to(sk, DOWN, buff=0.08)
        cap = caption([T("clock skew", CAP, t2c={"skew": TEAL})], COL_X[1], TOP_CAP)
        c.wait_until("r2")
        self.play(*self.dim_previous(), FadeIn(P), FadeIn(clk0), FadeIn(clk1),
                  *appear(lab0, lab1, shift=None, lag=0.2), run_time=1.3)  # early: the panel's rows return whole
        c.wait_until("clock skew")
        self.play(FadeIn(g_e), FadeIn(g_k), GrowFromCenter(sk), *appear(sk_l, shift=None),
                  *appear(cap, shift=None), run_time=1.2)  # early: the line names the arrow
        c.wait_until("splits")
        paths = [br.copy().set_stroke(YELLOW, 6, opacity=1) for br in (P.clk_br0, P.clk_br1)]
        self.play(*[VShowPassingFlash(p, time_width=0.5, rate_func=linear) for p in paths], run_time=1.2)
        c.wait_until("clock zero")
        self.play(FlashAround(lab0, color=YELLOW, time_width=1.5), run_time=0.9)
        c.wait_until("clock one")
        self.play(FlashAround(lab1, color=YELLOW, time_width=1.5), run_time=min(0.9, c.until("r3", floor=0.5)))
        self.panels.append(VGroup(grp, lab0, lab1, sk_l, cap))

    def r3(self, c):
        cx = COL_X[2]
        W = 3.6
        ws = [W * w / 6.12 for w in (1.02, 3.57, 0.68, 0.85)]
        x0 = cx - W / 2 + 0.3
        bar = budget_bar(list(zip((PINK, PURPLE, GOLD, TEAL), ws)), W, x0=x0, y=1.8, h=0.42, tc_size=36)
        parts = ["T_c", r"\geq", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", "+", "t_{skew}"]
        cols = {0: YELLOW, 2: PINK, 4: PURPLE, 6: GOLD, 8: TEAL}
        full = MathTex(*parts, font_size=34).move_to(_p(cx, 2.85))
        terms = [MathTex(s, font_size=34, color=cols.get(i, FG)).move_to(full[i]) for i, s in enumerate(parts)]
        cap = caption([T("skew joins the budget", CAP, t2c={"skew": TEAL})], cx, TOP_CAP)
        c.wait_until("r3")
        self.play(*self.dim_previous(), *appear(*terms[:7], shift=None, lag=0.05),
                  FadeIn(bar.outline), *appear(bar.tc, shift=None), run_time=1.3)  # early: the rule shown whole first
        self.play(*[time_span(GrowFromEdge(s, LEFT), 0.25 * k, 0.25 * k + 0.6) for k, s in enumerate(bar.segs[:3])],
                  run_time=1.1)
        c.wait_until("fourth piece")
        self.play(GrowFromEdge(bar.segs[3], LEFT), *appear(terms[7], terms[8], shift=None, lag=0.2),
                  FlashAround(bar.segs[3], color=TEAL, time_width=1.5, buff=0.06), run_time=1.3)
        c.wait_until("budget")
        self.play(*appear(cap, shift=None), run_time=min(1.0, c.until("r4", floor=0.5)))
        self.panels.append(VGroup(bar, *terms, cap))

    def r4(self, c):
        cx, cy = COL_X[0], BOT_Y
        U = 3.6
        x0 = cx - U / 2
        by = cy - 0.15
        bar = budget_bar([(PINK, 0.2 * U), (PURPLE, 0.7 * U), (GOLD, 0.1 * U)], U, x0=x0, y=by, h=0.45)
        bar.remove(bar.tc)
        tc = MathTex(r"T_c = 1\,\text{ns}", font_size=36, color=YELLOW).move_to(_p(cx, by + 0.7))
        locks = [padlock(0.85).move_to(bar.segs[i]).set_z_index(2) for i in (0, 2)]
        n07 = T("0.7 ns", 30, GOLD).next_to(bar.segs[1], DOWN, buff=0.18)
        ghost = DashedVMobject(Rectangle(width=0.7 * U, height=0.69).move_to(bar.segs[1]), num_dashes=40)
        ghost.set_stroke(PURPLE, 2, opacity=0.55)
        rule = colored_tex(["t_{pd}", r"\leq", "T_c", "-", "(", "t_{pc}", "+", "t_{su}", "+", "t_{skew}", ")"],
                           {0: PURPLE, 2: YELLOW, 5: PINK, 7: GOLD, 9: TEAL}, 34)
        cap = caption([rule], cx, BOT_CAP)
        c.wait_until("r4")
        self.play(*self.dim_previous(), FadeIn(VGroup(*bar.segs, bar.outline)), *[FadeIn(lk) for lk in locks],
                  *appear(tc, n07, shift=None, lag=0.2), run_time=1.3)  # early: the 1 ns bar returns with its numbers
        self.play(*appear(cap, shift=None), run_time=1.0)  # early: the rule the sentence states
        c.wait_until("zero point seven")
        self.play(FlashAround(bar.segs[1], color=PURPLE, time_width=1.5), FadeIn(ghost), run_time=1.2)
        c.wait_until("shrink")
        sk = 0.1 * U
        teal = Rectangle(width=sk, height=0.45).set_stroke(width=0).set_fill(TEAL, BAR_FILL)
        teal.move_to(_p(x0 + U - sk / 2, by))
        self.play(FadeIn(teal, shift=0.8 * LEFT),
                  bar.segs[1].animate.stretch_to_fit_width(0.6 * U, about_edge=LEFT),
                  bar.segs[2].animate.shift(sk * LEFT), locks[1].animate.shift(sk * LEFT),
                  n07.animate.shift(sk / 2 * LEFT), run_time=1.5)
        c.wait_until("zero point six")
        n06 = T("0.6 ns", 30, GOLD).move_to(n07)
        self.play(*swap(n07, n06), run_time=min(1.0, c.until("r5", floor=0.5)))
        self.panels.append(VGroup(bar, teal, tc, *locks, n06, ghost, cap))

    def r5(self, c):
        cx, cy = COL_X[1], BOT_Y
        s = 0.75
        K1, E1, XQ, XD, HE = (s * x for x in (-2.4, -1.4, -0.2, 0.3, -0.4))
        bx0, bx1 = -2.3, 0.9
        yd, yc, ych = 0.7, 0.0, -0.55
        hh = 0.22
        d_runs = VGroup(Line(_p(bx0, yd + hh), _p(XD, yd + hh)), Line(_p(bx0, yd - hh), _p(XD, yd - hh)),
                        Line(_p(XD, yd + hh), _p(XD + 0.24, yd - hh)), Line(_p(XD, yd - hh), _p(XD + 0.24, yd + hh)),
                        Line(_p(XD + 0.24, yd + hh), _p(bx1, yd + hh)), Line(_p(XD + 0.24, yd - hh), _p(bx1, yd - hh)))
        d_runs.set_stroke(BLUE, WAVE_W)
        d_l = MathTex("D_1", font_size=34, color=BLUE).next_to(_p(bx0, yd), LEFT, buff=0.15)
        clk1 = clock_wave(bx0, bx1, yc, [K1], h=2 * hh, slope=0.2).set_stroke(opacity=CLK1_OP)
        c_l = T("CLK1", 28, YELLOW).set_opacity(0.7).next_to(_p(bx0, yc), LEFT, buff=0.15)
        band = Rectangle(width=HE - K1, height=2 * hh + 0.16).set_stroke(width=0).set_fill(GOLD, 0.25)
        band.move_to(_p((K1 + HE) / 2, yd)).set_z_index(-1)
        th = harrow(K1, HE, yd + 0.45, GOLD)
        th_l = MathTex("t_{hold}", font_size=32, color=GOLD).next_to(th, RIGHT, buff=0.12)
        g_k = guide(K1, yd + hh + 0.1, ych - 0.1, YELLOW, 2.5)
        g_d = guide(XD, yd - hh, ych - 0.1)
        chain = [harrow(K1, E1, ych, TEAL), harrow(E1, XQ, ych, PINK), harrow(XQ, XD, ych, PURPLE)]
        br = span_brace(_p(K1, ych - 0.12), _p(XD, ych - 0.12), DOWN, color=FG, inset=0.0, buff=0.0)
        tick = check_mark(GREEN).scale(0.75).move_to(_p(XD + 0.55, ych - 0.05))
        grp = VGroup(band, d_runs, d_l, clk1, c_l, th, th_l, g_k, g_d, *chain, br, tick)
        grp.shift(_p(cx - grp.get_center()[0], BOT_CAP + 0.25 - grp.get_bottom()[1]))
        cap = caption([T("skew helps hold", CAP, t2c={"skew": TEAL})], cx, BOT_CAP)
        c.wait_until("r5")
        self.play(*self.dim_previous(), FadeIn(d_runs), FadeIn(clk1), FadeIn(g_k), FadeIn(band), FadeIn(th),
                  *appear(d_l, c_l, th_l, shift=None, lag=0.15), run_time=1.1)  # early: the hold view returns whole
        self.play(*[GrowFromCenter(a) for a in chain], FadeIn(g_d), GrowFromCenter(br), run_time=1.0)
        c.wait_until("more room")
        self.play(GrowFromCenter(tick), FlashAround(band, color=GREEN, time_width=1.5),
                  *appear(cap, shift=None), run_time=min(1.1, c.until("r6", floor=0.5)))  # early: the panel's line
        self.panels.append(VGroup(grp, cap))

    def r6(self, c):
        cx, cy = 4.45, BOT_Y
        L = 3.2
        x0 = cx - 2.11 + 0.7
        y = cy + 0.4
        H, Hn = skew_fences(0.1, x0, y, L), skew_fences(-0.1, x0, y, L)
        ty = y - 0.88          # rule name; its verdict sits under it
        right = x0 + L

        def tag_x(x, w=1.0):
            return min(x, right + 0.3 - w / 2)
        hold_w = T("hold", 28, FG).move_to(_p(tag_x(H.xf), ty))
        su_w = T("set-up", 28, FG).move_to(_p(tag_x(H.xd), ty))
        easy = T("easier", 28, GREEN).next_to(hold_w, DOWN, buff=0.1)
        hard = T("harder", 28, RED).next_to(su_w, DOWN, buff=0.1)
        cap = caption([T("turn it round:", CAP), T("the trade reverses", CAP)], cx, BOT_CAP)
        c.wait_until("r6")
        self.play(*self.dim_previous(), *[FadeIn(m) for m in H.submobjects], *appear(hold_w, easy, su_w, hard, shift=None, lag=0.15), run_time=1.0)  # early: s5's fence picture returns whole, rule names with it
        c.wait_until("round")
        moves = [(H.fence, Hn.fence), (H.fence_l, Hn.fence_l), (H.deadline, Hn.deadline),
                 (H.su, Hn.su), (H.su_l, Hn.su_l)]
        dh = tag_x(Hn.xf) - hold_w.get_x()
        ds = tag_x(Hn.xd) - su_w.get_x()
        self.play(*during([H.skseg.animate.stretch(0.02, 0, about_edge=RIGHT).set_opacity(0)], 0, 0.5),
                  *[a.animate.move_to(b) for a, b in moves],
                  *[m.animate.shift(dh * RIGHT) for m in (hold_w, easy)],
                  *[m.animate.shift(ds * RIGHT) for m in (su_w, hard)],
                  *during(appear(*cap, shift=None, lag=0.3), 0.3, 1.0), run_time=1.4)  # early: the panel's line
        self.remove(H.skseg)
        H.remove(H.skseg)
        c.wait_until("trade reverses")
        hard2 = T("harder", 28, RED).next_to(hold_w, DOWN, buff=0.1)
        easy2 = T("easier", 28, GREEN).next_to(su_w, DOWN, buff=0.1)
        self.play(*swap(easy, hard2), *swap(hard, easy2), run_time=1.0)
        self.panels.append(VGroup(H, hold_w, su_w, hard2, easy2, cap))

    # -- c3.recap.2: next time, an input that obeys no clock --------------------------------------
    def clip2(self):
        # the button and the flip-flop (left)
        pin_y = 1.4
        fx = -2.6
        box = Rectangle(width=1.3, height=2.0).set_stroke(FG, 4).move_to(_p(fx, pin_y - 0.5))
        tri = Polygon(_p(fx - 0.16, box.get_bottom()[1]), _p(fx + 0.16, box.get_bottom()[1]),
                      _p(fx, box.get_bottom()[1] + 0.24)).set_stroke(FG, 3).set_fill(BG, 1)
        d_lab = T("D", 32, BLUE).move_to(_p(box.get_left()[0] + 0.28, pin_y))
        q_lab = T("Q", 32, GREEN).move_to(_p(box.get_right()[0] - 0.28, pin_y))
        q_w = Line(_p(box.get_right()[0], pin_y), _p(box.get_right()[0] + 0.7, pin_y)).set_stroke(GREEN, 5)
        bx = -5.5
        base = RoundedRectangle(corner_radius=0.08, width=0.95, height=0.32).set_stroke(FG, 3).set_fill(BG, 1)
        base.move_to(_p(bx, pin_y - 0.16))
        cap_ = RoundedRectangle(corner_radius=0.1, width=0.55, height=0.26).set_stroke(FG, 3).set_fill(DIM, 1)
        cap_.next_to(base, UP, buff=0)
        stem = Line(cap_.get_bottom(), base.get_top()).set_stroke(FG, 3)
        btn_l = T("button", 28, DIM).next_to(base, DOWN, buff=0.2)
        d_w = VMobject().set_points_as_corners([_p(base.get_right()[0], pin_y - 0.16), _p(-4.3, pin_y - 0.16),
                                                _p(-4.3, pin_y), _p(box.get_left()[0], pin_y)]).set_stroke(BLUE, 5)
        cy_ = box.get_bottom()[1] - 0.8
        clk_w = VMobject().set_points_as_corners([_p(-5.7, cy_), _p(fx, cy_), _p(fx, box.get_bottom()[1])])
        clk_w.set_stroke(YELLOW, 5)
        clk_l = T("CLK", 30, YELLOW).next_to(_p(-5.7, cy_), LEFT, buff=0.15)
        circuit = [box, tri, q_w, base, stem, cap_, d_w, clk_w]
        # the window diagram (right)
        W = WindowDiagram(origin=_p(3.15, 0.55), k=0.62, fs=0.8)
        x_bad = 0.45
        d_lo = W.path(1, [(W.X0, 0), (x_bad, 0)], BLUE, W.sw)
        d_hi = W.path(1, [(x_bad, 1), (W.X1, 1)], BLUE, W.sw)
        q_new = W.path(2, [(W.X0, 0), (W.T_PC, 0)], GREEN, W.sw)
        bad = W.d_change(x_bad)
        unk = W.q_unknown()
        part4 = T("Part 4 · Metastability and the synchroniser", 40).move_to(_p(0, -2.85))

        with self.say("c3.recap.2") as c:
            # {next}: the panels shrink away; the button and the flip-flop arrive
            self.play(*during([FadeOut(m, scale=0.5) for m in self.mobjects], 0, 0.5),
                      *during([FadeIn(m) for m in circuit], 0.5, 1.0),
                      *during(appear(d_lab, q_lab, clk_l, btn_l, shift=None), 0.55, 1.0), run_time=1.6)  # early: the teaser circuit arrives whole
            # the clock ticks past, steady
            n = 0
            while c.until("button press") > 1.3 and n < 3:
                self.play(VShowPassingFlash(clk_w.copy().set_stroke(YELLOW, 10), time_width=0.4, rate_func=linear),
                          FlashAround(tri, color=YELLOW, buff=0.05), run_time=1.0)
                n += 1
            c.wait_until("button press")
            dot = Dot(d_w.get_start(), radius=0.11, color=BLUE).set_z_index(5)
            self.play(cap_.animate(rate_func=there_and_back).shift(0.1 * DOWN), FadeIn(dot, scale=0.5), run_time=0.7)
            self.play(MoveAlongPath(dot, d_w), run_time=1.3)
            # "which obey no clock at all": the clock ticks on, out of step with the press
            c.wait_until("no clock")
            self.play(VShowPassingFlash(clk_w.copy().set_stroke(YELLOW, 10), time_width=0.4, rate_func=linear),
                      FlashAround(tri, color=YELLOW, buff=0.05), FadeOut(dot), run_time=1.0)
            # {broken}: the window; the press lands inside it; Q unknown
            c.wait_until("broken")
            self.play(*[FadeIn(m) for m in (W.guide, W.up, W.clk, W.band)],
                      *appear(W.lab_clk, W.lab_d, W.lab_q, shift=None, lag=0.1), run_time=1.0)  # early: the diagram's rows
            self.play(FadeIn(W.su), FadeIn(W.hold), *appear(W.sym_su, W.sym_hold, shift=None, lag=0.2),
                      Create(d_lo), Create(q_new), run_time=1.2)  # early: the window's two names
            c.wait_until("changes inside")
            self.play(Create(bad), FadeIn(d_hi), FlashAround(W.band, color=RED, time_width=1.5), run_time=1.2)
            c.wait_until("window")
            self.play(*appear(unk), run_time=min(1.0, c.until(floor=0.5)))
        self.play(*appear(part4), run_time=1.0)  # early: the end card
