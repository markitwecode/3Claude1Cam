"""Chapter 4, scene 7: recap in six tiles, then the teaser for Part 5 (MTBF). Clips c4.recap.1 – c4.recap.3.

Tiles (ch2_s6_recap styling: no frames, T 30 lines under each, earlier tiles dimmed by a BG veil),
two rows of three at x = -4.6, 0, 4.6 (centres y 2.35 / -1.3, lines from y 0.95 / -2.6 down):
 t1 s1's button_ff() over a CLK / D strip with GOLD windows; the press lands inside one, which turns RED.
 t2 s2's Q trace drifting to the RED halfway level, "???", beside volt_axis()'s GREEN / RED bands.
 t3 s3's hill() with the RED ball on the summit, arrows down both sides.
 t4 s5's decay_graph() with s4's GOLD "÷ e" arcs; line = s4's model_formula().
 t5 s5's sync_circuit() over sync_timing() (text stripped), FG t_res arrow.
 t6 s6's res_bar() over the boxed pfail_formula(); line = s6's fail_condition().
{next}: tiles clear; sync_circuit() alone (full size, shifted (0.72, -0.7)); BLUE ticks with GOLD
P_fail tags run along D0 into FF0, faster and faster, two turn RED (FF0 flashes RED).
{years}: GOLD "P_fail -> years" + a small calendar at y -1.3. End card "Part 5 · Mean time between
failures" T 48 FG at (0, -2.85), held 8 s.
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
# make_ff_s1 + push_button + fingertip + button_ff, copied from ch4_s1_hook.py
# (s1's make_ff, with Q-bar and the CLK wire in the group; renamed: s5's make_ff is below)
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
PUSH = 0.18


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff_s1(center=ORIGIN, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    g.box, g.tri = box, tri
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


def push_button(center=ORIGIN):
    stem = Line(_p(-0.3, 0), _p(-0.58, 0)).set_stroke(FG, 5)
    cap = RoundedRectangle(corner_radius=0.06, width=0.16, height=0.62).set_stroke(FG, 4).set_fill(DIM, 1)
    cap.move_to(_p(-0.66, 0))
    body = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.84).set_stroke(FG, 4).set_fill(BG, 1)
    g = VGroup(stem, cap, body)            # body last: it hides the stem when pushed in
    g.stem, g.cap, g.body = stem, cap, body
    g.plunger = VGroup(stem, cap)
    g.shift(center)
    g.out = lambda: body.get_right()
    return g


def fingertip():
    f = RoundedRectangle(corner_radius=0.21, width=1.4, height=0.44).set_stroke(FG, 3).set_fill(BG, 1)
    f.move_to(_p(-0.7, 0))
    nail = RoundedRectangle(corner_radius=0.07, width=0.34, height=0.17).set_stroke(FG, 2)
    nail.move_to(_p(-0.27, 0.07))
    g = VGroup(f, nail)
    g.nail = nail
    return g


HERO_FF = _p(0.6, 0.95)
HERO_K = 0.85
BTN_X = -4.0


def button_ff(ff_center=HERO_FF, k=HERO_K, btn_x=BTN_X):
    ff = make_ff_s1().scale(k).move_to(ff_center)
    y = ff.d_w.get_center()[1]
    btn = push_button(_p(btn_x, y))
    wire = Line(btn.out(), ff.d_w.get_left()).set_stroke(BLUE, 5)
    clk_l = T("CLK", 30, YELLOW).next_to(ff.clk_w.get_bottom(), LEFT, buff=0.15).shift(0.12 * UP)
    g = VGroup(wire, ff, btn, clk_l)
    g.ff, g.btn, g.wire, g.clk_l = ff, btn, wire, clk_l
    g.finger = fingertip().shift(btn.cap.get_left())
    return g
# =============================================================================================


# =============================================================================================
# Data-sheet kit (ch1_s5 / ch4_s2): clock_wave, guide, dim_arrow, grow_dim
# =============================================================================================
WAVE_W = 4
SLOPE = 0.35
GUIDE_W = 1.5
DIM_W = 3


def clock_wave(x0, x1, y, edges, h=0.5, slope=SLOPE, color=YELLOW, start_low=True):
    lo, hi = y - h / 2, y + h / 2
    level = lo if start_low else hi
    pts = [_p(x0, level)]
    for xc in edges:
        other = hi if level == lo else lo
        pts += [_p(xc - slope / 2, level), _p(xc + slope / 2, other)]
        level = other
    pts.append(_p(x1, level))
    return VMobject().set_points_as_corners(pts).set_stroke(color, WAVE_W)


def guide(x, y_top, y_bot):
    return Line(_p(x, y_top), _p(x, y_bot)).set_stroke(DIM, GUIDE_W)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=40):
    arr = DoubleArrow(_p(xa, y), _p(xb, y), buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.12)
    g = VGroup(arr, lab)
    g.arr, g.lab = arr, lab
    return g


def grow_dim(arr, tip=0.16):
    """ch1_s5's grow_dim: a DoubleArrow grown from its centre at true tip size."""
    start, end = arr.get_start(), arr.get_end()
    mid, half = (start + end) / 2, (end - start) / 2
    final = arr.copy()

    def upd(m, a):
        if a >= 1:
            m.become(final)
            return
        if a * np.linalg.norm(end - start) < 0.3:
            m.become(final).set_opacity(0)
            return
        m.become(DoubleArrow(mid - a * half, mid + a * half, buff=0, stroke_width=final.get_stroke_width(),
                             tip_length=tip, max_tip_length_to_length_ratio=0.4,
                             color=final.get_color()))

    return UpdateFromAlphaFunc(arr, upd, rate_func=smooth)
# =============================================================================================


# =============================================================================================
# undefined_diagram() constants + volt_axis(), copied from ch4_s2_undefined.py (the tile uses
# the Q row and the axis; q0 starts at UQ_X0 instead of UX0, to fit the tile)
# =============================================================================================
ROW_H2 = 0.8
UX1 = 3.0
UXE = -0.6
UY_Q = -1.6
UQ_MID = UY_Q
UXQ = UXE + 0.2
UXQ_FLAT = UXE + 1.4
UQ_X0 = -2.6


def q_row():
    lo_q = UY_Q - ROW_H2 / 2
    q0 = Line(_p(UQ_X0, lo_q), _p(UXQ, lo_q)).set_stroke(GREEN, WAVE_W)
    xs = np.linspace(UXQ, UXQ_FLAT, 24)
    s = (xs - UXQ) / (UXQ_FLAT - UXQ)
    ys = lo_q + (UQ_MID - lo_q) * (s * s * (3 - 2 * s))
    q_bad = VMobject().set_points_as_corners([_p(x, y) for x, y in zip(xs, ys)] + [_p(UX1, UQ_MID)])
    q_bad.set_stroke(RED, WAVE_W)
    return q0, q_bad


VA_X = 4.3
VA_LO, VA_HI = UQ_MID - 1.8, UQ_MID + 1.8
VA_BAND = 0.8


def volt_axis():
    g = VGroup()
    line = Line(_p(VA_X, VA_LO), _p(VA_X, VA_HI)).set_stroke(FG, 3)
    ticks = VGroup(*[Line(_p(VA_X - 0.12, y), _p(VA_X + 0.12, y)).set_stroke(FG, 3) for y in (VA_LO, VA_HI)])
    axis = VGroup(line, ticks)
    lo_l = T("0 V", 30).next_to(_p(VA_X - 0.12, VA_LO), LEFT, buff=0.15)
    hi_l = MathTex(r"V_{DD}", font_size=40).next_to(_p(VA_X, VA_HI), UP, buff=0.15)
    bx, bw = VA_X + 0.35, 0.5

    def band(y0, y1, color, op):
        return Rectangle(width=bw, height=y1 - y0).set_stroke(color, 2).set_fill(color, op).move_to(
            _p(bx, (y0 + y1) / 2))

    ok0 = band(VA_LO, VA_LO + VA_BAND, GREEN, 0.45)
    ok1 = band(VA_HI - VA_BAND, VA_HI, GREEN, 0.45)
    bad = band(VA_LO + VA_BAND, VA_HI - VA_BAND, RED, 0.4)
    ok0_l = T("valid 0", 30, GREEN).next_to(ok0, RIGHT, buff=0.2)
    ok1_l = T("valid 1", 30, GREEN).next_to(ok1, RIGHT, buff=0.2)
    bad_l = T("invalid", 30, RED).next_to(bad, RIGHT, buff=0.2)
    level = DashedLine(_p(UX1 + 0.1, UQ_MID), _p(bx - bw / 2 - 0.05, UQ_MID), dash_length=0.12)
    level.set_stroke(RED, 3)
    g.add(axis, lo_l, hi_l, ok0, ok1, bad, ok0_l, ok1_l, bad_l, level)
    g.axis, g.lo_l, g.hi_l, g.ok0, g.ok1, g.bad = axis, lo_l, hi_l, ok0, ok1, bad
    g.ok0_l, g.ok1_l, g.bad_l, g.level = ok0_l, ok1_l, bad_l, level
    return g
# =============================================================================================


# =============================================================================================
# hill() + ball() + place(), copied from ch4_s3_ball.py
# =============================================================================================
U_END = 1.42


def _f(u):
    return (u * u - 1.0) ** 2


class Hill(VGroup):
    def __init__(self, xs=3.0, ys=2.5, labels=True, color=BLUE, width=6):
        super().__init__()
        self.curve = ParametricFunction(lambda u: _p(u * xs, _f(u) * ys), t_range=(-U_END, U_END, 0.01))
        self.curve.set_stroke(color, width)
        self._o, self._ux, self._uy = VectorizedPoint(ORIGIN), VectorizedPoint(_p(xs, 0)), VectorizedPoint(_p(0, ys))
        self.add(self.curve, self._o, self._ux, self._uy)
        self.lab0 = VGroup(T("0", size=56, color=GREEN), T("stable", size=36)).arrange(DOWN, buff=0.1)
        self.lab1 = VGroup(T("1", size=56, color=GREEN), T("stable", size=36)).arrange(DOWN, buff=0.1)
        self.lab0.next_to(self.point(-1), DOWN, buff=0.3)
        self.lab1.next_to(self.point(1), DOWN, buff=0.3)
        self.lab_meta = T("metastable", size=44, color=RED).next_to(self.point(0), UP, buff=0.85)
        self.labels = VGroup(self.lab0, self.lab1, self.lab_meta)
        if labels:
            self.add(*self.labels)

    def point(self, u):
        o = self._o.get_center()
        return o + u * (self._ux.get_center() - o) + _f(u) * (self._uy.get_center() - o)

    def ball_point(self, u, r):
        t = self.point(u + 1e-3) - self.point(u - 1e-3)
        n = np.array([-t[1], t[0], 0.0])
        return self.point(u) + r * n / np.linalg.norm(n)


def hill(xs=3.0, ys=2.5, labels=True, color=BLUE, width=6):
    return Hill(xs, ys, labels, color, width)


def ball(color=RED, r=0.3):
    b = Circle(radius=r).set_stroke(width=0).set_fill(color, 1)
    b.r = r
    return b


def place(b, h, u):
    return b.move_to(h.ball_point(u, b.r))
# =============================================================================================


# =============================================================================================
# decay_graph(), copied from ch4_s5_synchroniser.py; model_formula(), copied from ch4_s4_model.py
# =============================================================================================
def decay_graph(width=8.0, height=4.2):
    ax = Axes(x_range=[0, 5.6, 1], y_range=[0, 1.1, 1], x_length=width, y_length=height, tips=False,
              axis_config={"color": FG, "stroke_width": 3, "include_ticks": False})
    ticks = VGroup()
    tlabels = VGroup()
    for i in range(1, 6):
        pt = ax.c2p(i, 0)
        ticks.add(Line(pt + 0.1 * DOWN, pt + 0.1 * UP).set_stroke(FG, 3))
        tlabels.add(MathTex(r"\tau" if i == 1 else rf"{i}\tau", font_size=40, color=FG)
                    .next_to(pt, DOWN, buff=0.2))
    y0 = 0.9
    ytick = Line(ax.c2p(0, y0) + 0.1 * LEFT, ax.c2p(0, y0) + 0.1 * RIGHT).set_stroke(FG, 3)
    ylab0 = MathTex(r"T_0/T_c", font_size=40, color=RED).next_to(ax.c2p(0, y0), LEFT, buff=0.2)
    xl = MathTex("t", font_size=44, color=FG).next_to(ax.c2p(5.6, 0), RIGHT, buff=0.2)
    yl = MathTex(r"P(t_{res} > t)", font_size=44, color=FG).next_to(ax.c2p(0, 1.1), UP, buff=0.2)
    curve = ax.plot(lambda t: y0 * np.exp(-t), x_range=[0, 5.5]).set_stroke(RED, 5)
    g = VGroup(ax, ticks, ytick, curve, tlabels, ylab0, xl, yl)
    g.ax, g.curve = ax, curve
    g.ticks, g.ytick, g.tlabels, g.ylab0, g.xl, g.yl = ticks, ytick, tlabels, ylab0, xl, yl
    g.labels = VGroup(tlabels, ylab0, xl, yl)
    g.move_to(ORIGIN)
    return g


MODEL_TEX = r"P(t_{res} > t) = \frac{T_0}{T_c}\, e^{-t/\tau}"


def model_formula(size=72):
    f = MathTex(MODEL_TEX, font_size=size, color=FG)
    g = f[0]
    if len(g) != 20:
        raise ValueError(f"model_formula: expected 20 glyphs, got {len(g)}")
    gl = list(g)
    fr = sorted(gl[10:15], key=lambda m: -m.get_center()[1])
    bot = fr[3:5]
    for m in bot:
        m.set_color(YELLOW)
    f.move_to(ORIGIN)
    return f
# =============================================================================================


# =============================================================================================
# make_ff + sync_circuit() + sync_timing(), copied from ch4_s6_fail.py (= s5's)
# =============================================================================================
def make_ff(center=ORIGIN, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    g = VGroup(d_w, q_w, box, tri, d_l, q_l)
    g.box, g.tri = box, tri
    g.d_l, g.q_l, g.d_w, g.q_w, g.clk_w = d_l, q_l, d_w, q_w, clk_w
    g.shift(center)
    clk_w.shift(center)
    return g


SK = 0.62
SFF_X = (-1.7, 2.1)
SFF_Y = 2.244
SBTN_X = -4.3


def sync_circuit():
    C = VGroup()
    ffs = []
    for x in SFF_X:
        f = make_ff()
        f.scale(SK, about_point=ORIGIN).shift(_p(x, SFF_Y))
        f.clk_w.scale(SK, about_point=ORIGIN).shift(_p(x, SFF_Y))
        for lb in (f.d_l, f.q_l):
            lb.scale(1.45, about_point=lb.get_center())
        ffs.append(f)
    C.ff0, C.ff1 = ffs
    py = SFF_Y + PIN_Y * SK
    C.py = py
    C.ff0.q_w.set_stroke(TEAL)
    C.ff0.q_l.set_color(TEAL)
    C.ff1.d_w.set_stroke(TEAL)
    C.ff1.d_l.set_color(TEAL)
    C.names = [T(f"FF{i}", 30, FG).move_to(f.box.get_center() + 0.3 * DOWN) for i, f in enumerate(ffs)]
    C.btn = push_button(_p(SBTN_X, py))
    C.d0_w = Line(C.btn.out(), C.ff0.d_w.get_start()).set_stroke(BLUE, 5)
    C.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(
        (C.btn.out() + C.ff0.d_w.get_start()) / 2, UP, buff=0.14)
    C.link = Line(C.ff0.q_w.get_end(), C.ff1.d_w.get_start()).set_stroke(TEAL, 5)
    C.d1_l = MathTex("D_1", font_size=40, color=TEAL).next_to(C.link, UP, buff=0.12)
    C.q_l = MathTex("Q", font_size=40, color=GREEN).next_to(C.ff1.q_w.get_end(), RIGHT, buff=0.15)
    by = SFF_Y - (BOX_H / 2 + EN_WIRE) * SK
    C.by = by
    C.bus = Line(_p(-3.2, by), _p(SFF_X[1], by)).set_stroke(YELLOW, 5)
    C.jdot = Dot(_p(SFF_X[0], by), radius=0.08, color=YELLOW)
    C.clk_ws = [f.clk_w for f in ffs]
    C.clk_l = T("CLK", 30, YELLOW).next_to(C.bus.get_start(), LEFT, buff=0.15)
    C.finger = fingertip().shift(C.btn.cap.get_left())
    C.d1_wires = [C.ff0.q_w, C.link, C.ff1.d_w]
    C.all = [C.ff0, C.ff1, *C.names, C.btn, C.d0_w, C.d0_l, C.link, C.d1_l, C.q_l,
             C.bus, C.jdot, *C.clk_ws, C.clk_l]
    C.add(*C.all)
    return C


ROW_H = 0.5
TX0, TX1 = -4.7, 4.2
E1, E2 = -2.4, 2.6
CLK_EDGES = [E1, 0.1, E2]
XS = 1.6
QX = (3.3, 3.6)
TROW = {"CLK": 0.0, "D1": -0.95, "Q": -1.95}
DIM_Y = -2.5
TC_Y = 0.4
LAB_X = -5.45


def pair(xa, xb, y, color, h=ROW_H):
    return VGroup(Line(_p(xa, y + h / 2), _p(xb, y + h / 2)),
                  Line(_p(xa, y - h / 2), _p(xb, y - h / 2))).set_stroke(color, WAVE_W)


def sync_timing():
    D = VGroup()
    yc, yd, yq = TROW["CLK"], TROW["D1"], TROW["Q"]
    h2 = ROW_H / 2
    D.clk = clock_wave(TX0, TX1, yc, CLK_EDGES, h=ROW_H)
    D.labs = [T("CLK", 32, YELLOW).move_to(_p(LAB_X, yc)),
              MathTex("D_1", font_size=40, color=TEAL).move_to(_p(LAB_X, yd)),
              MathTex("Q", font_size=40, color=GREEN).move_to(_p(LAB_X, yq))]
    D.d1_pre = pair(TX0, E1, yd, TEAL)
    c1 = E1 + 0.3
    D.d1_conv = VGroup(Line(_p(E1, yd + h2), _p(c1, yd)), Line(_p(E1, yd - h2), _p(c1, yd))).set_stroke(RED, WAVE_W)
    D.mid_x = -0.4
    D.d1_red1 = Line(_p(c1, yd), _p(D.mid_x, yd)).set_stroke(RED, WAVE_W)
    D.d1_red2 = Line(_p(D.mid_x, yd), _p(XS - 0.3, yd)).set_stroke(RED, WAVE_W)
    D.d1_div = VGroup(Line(_p(XS - 0.3, yd), _p(XS, yd + h2)), Line(_p(XS - 0.3, yd), _p(XS, yd - h2))).set_stroke(TEAL, WAVE_W)
    D.d1_post = pair(XS, TX1, yd, TEAL)
    D.q_pre = pair(TX0, QX[0], yq, GREEN)
    D.q_x = VGroup(Line(_p(QX[0], yq + h2), _p(QX[1], yq - h2)),
                   Line(_p(QX[0], yq - h2), _p(QX[1], yq + h2))).set_stroke(GREEN, WAVE_W)
    D.q_post = pair(QX[1], TX1, yq, GREEN)
    D.tc = dim_arrow(E1, E2, TC_Y, YELLOW, "T_c")
    D.tc.lab.move_to(_p(E2 + 0.42, TC_Y + 0.22))
    D.tcx = VGroup(guide(E1, yc + h2 + 0.05, TC_Y + 0.14), guide(E2, yc + h2 + 0.05, TC_Y + 0.14))
    top, bot = yc + h2 + 0.05, DIM_Y - 0.12
    D.g1, D.gs, D.g2 = guide(E1, top, bot), guide(XS, yd, bot), guide(E2, top, bot)
    D.gq = guide(QX[0], yq, bot)
    D.tres = dim_arrow(E1, XS, DIM_Y, FG, "t_{res}", label_dir=DOWN)
    D.tsu = dim_arrow(XS, E2, DIM_Y, GOLD, "t_{su}", label_dir=DOWN)
    D.tpc = dim_arrow(E2, QX[0], DIM_Y, PINK, "t_{pc}", label_dir=DOWN)
    D.all = [D.clk, *D.labs, D.d1_pre, D.d1_conv, D.d1_red1, D.d1_red2, D.d1_div, D.d1_post,
             D.q_pre, D.q_x, D.q_post, D.tc, D.tcx, D.g1, D.gs, D.g2, D.gq, D.tres, D.tsu, D.tpc]
    D.add(*D.all)
    return D
# =============================================================================================


# =============================================================================================
# budget_bar (ch1_s6) + res_bar / pfail_formula / fail_condition, copied from ch4_s6_fail.py
# =============================================================================================
BAR_H = 0.5
BAR_FILL = 0.85
BAR_OUT_W = 3


def budget_bar(segs, total, x0=-3.3, y=0.0, tc_tex="T_c", syms=True, nums=None,
               sym_size=40, num_size=34):
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


RB_X0, RB_TOT, RB_SU, RB_Y = -2.04, 5.1, 0.85, -1.35
PF_SIZE = 64


def res_bar(x0=RB_X0, y=RB_Y, total=RB_TOT, su=RB_SU):
    return budget_bar([("t_{res}", FG, total - su), ("t_{su}", GOLD, su)], total, x0=x0, y=y)


def color_tc_tsu(m):
    for i in (0, 1):
        m[0][i].set_color(YELLOW)
    for i in (3, 4, 5):
        m[0][i].set_color(GOLD)
    return m


def pfail_formula(size=PF_SIZE):
    main = MathTex(r"P_{fail} = \frac{T_0}{T_c}\, e^{-(\phantom{T_c - t_{su}})/\tau}", font_size=size)
    g = main[0]
    for i in (9, 10):
        g[i].set_color(YELLOW)
    ins = color_tc_tsu(MathTex(r"T_c - t_{su}", font_size=size))
    lp, rp = g[13], g[14]
    ins.scale_to_fit_width(rp.get_left()[0] - lp.get_right()[0] - 0.1)
    ins.move_to([(lp.get_right()[0] + rp.get_left()[0]) / 2, ins.get_y(), 0])
    ins.shift((lp.get_y() - ins[0][2].get_y()) * UP)
    box = SurroundingRectangle(VGroup(main, ins), buff=0.3).set_stroke(YELLOW, 3)
    F = VGroup(main, ins, box)
    F.main, F.ins, F.box = main, ins, box
    return F


def fail_condition(word="fails if"):
    w = T(word, 40)
    a = MathTex(r"t_{res} >", font_size=50)
    a[0][4].set_color(RED)
    b = color_tc_tsu(MathTex(r"T_c - t_{su}", font_size=50))
    a.next_to(w, RIGHT, buff=0.3)
    b.next_to(a, RIGHT, buff=0.22)
    b.shift((a[0][4].get_y() - b[0][2].get_y()) * UP)
    w.align_to(a[0][0], DOWN)
    g = VGroup(w, a, b)
    g.w, g.a, g.b = w, a, b
    return g
# =============================================================================================


# ---- recap grid (ch2_s6_recap styling) -------------------------------------------------------
TILE_X = (-4.6, 0.0, 4.6)
TOP_Y, BOT_Y = 2.35, -1.3
TOP_CAP, BOT_CAP = 0.95, -2.6
TILE_W, TILE_H = 4.0, 2.4
CAP = 30
VEIL = 0.45


def caption(lines, x, top):
    g = VGroup(*lines).arrange(DOWN, buff=0.14)
    g.move_to([x, 0, 0]).align_to([0, top, 0], UP)
    return g


def veil(*mobs):
    g = VGroup(*mobs)
    return (Rectangle(width=g.width + 0.3, height=g.height + 0.3).set_stroke(width=0)
            .set_fill(BG, VEIL).move_to(g).set_z_index(20))


def fit(g, ctr, w=TILE_W, h=TILE_H):
    s = min(w / g.width, h / g.height, 1.0)
    g.scale(s).move_to(ctr)
    return s


def calendar(color=FG):
    """A small wall calendar: frame, GOLD header band, two rings, a 4 x 3 grid of day dots."""
    w, h = 1.0, 1.0
    frame = RoundedRectangle(corner_radius=0.08, width=w, height=h).set_stroke(color, 3)
    head = Rectangle(width=w, height=0.24).set_stroke(width=0).set_fill(GOLD, 0.8)
    head.move_to(frame.get_top() + 0.12 * DOWN)
    rings = VGroup(*[Line(_p(x, h / 2 + 0.1), _p(x, h / 2 - 0.08)).set_stroke(color, 4) for x in (-0.25, 0.25)])
    dots = VGroup(*[Dot(_p(-0.3 + 0.2 * i, 0.12 - 0.18 * j), radius=0.035, color=color)
                    for j in range(3) for i in range(4)])
    return VGroup(head, frame, rings, dots)


class Recap4(NarratedScene):
    def construct(self):
        self.tiles = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)   # end card; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def dim_previous(self):
        out = []
        for t in self.tiles:
            if not getattr(t, "veiled", False):
                t.veiled = True
                out.append(FadeIn(veil(t)))
        return out

    # -- c4.recap.1: t1 button + window, t2 Q undefined, t3 the hill ------------------------------
    def clip1(self):
        with self.say("c4.recap.1") as c:
            c.wait_until("r1")
            # t1: s1's button wired to D, over a CLK / D strip with GOLD windows
            bf = button_ff()
            bf.ff.remove(bf.ff.d_l, bf.ff.q_l, bf.ff.qb_l)
            bf.remove(bf.clk_l)
            y_c, y_d, row = -1.6, -2.6, 0.7
            ex = HERO_FF[0]                     # a rising edge right under the flip-flop
            clk = clock_wave(-4.6, 2.0, y_c, [ex - 3.6, ex - 2.4, ex - 1.2, ex, ex + 1.2], h=row,
                             start_low=False)
            wins = VGroup(*[Rectangle(width=1.0, height=row + 0.25).set_stroke(width=0).set_fill(GOLD, 0.25)
                            .move_to(_p(e - 0.1, y_d)) for e in (ex - 2.4, ex)])
            gds = VGroup(*[guide(e, y_c + row / 2 + 0.1, y_d - row / 2 - 0.15) for e in (ex - 2.4, ex)])
            lo, hi = y_d - row / 2, y_d + row / 2
            xr = ex - 0.25
            d_low = Line(_p(-4.6, lo), _p(xr - 0.08, lo)).set_stroke(BLUE, WAVE_W)
            d_rise = VMobject().set_points_as_corners([_p(xr - 0.08, lo), _p(xr + 0.08, hi), _p(2.0, hi)])
            d_rise.set_stroke(BLUE, WAVE_W)
            shapes = VGroup(bf, gds, wins, clk, d_low, d_rise)
            s1 = fit(shapes, _p(TILE_X[0], TOP_Y))
            d_t = T("D", 28, BLUE).move_to(bf.ff.box.get_left() + 0.17 * RIGHT).set_y(bf.ff.d_w.get_y())
            q_t = T("Q", 28, GREEN).move_to(bf.ff.box.get_right() + 0.17 * LEFT).set_y(bf.ff.q_w.get_y())
            win = wins[1]
            self.remove(d_rise)
            self.play(FadeIn(VGroup(bf, gds, wins, clk, d_low)), *appear(d_t, q_t, shift=None),
                      run_time=1.2)  # early: the tile's pin labels
            c.wait_until("change inside")
            self.play(bf.btn.plunger.animate.shift(PUSH * HERO_K * s1 * RIGHT), Create(d_rise),
                      run_time=1.0)
            self.play(win.animate.set_fill(RED, 0.45), FlashAround(win, color=RED, time_width=1.5),
                      run_time=1.2)
            cap1 = caption([T("Outside inputs ignore", CAP), T("the window", CAP, t2c={"window": GOLD})],
                           TILE_X[0], TOP_CAP)
            self.play(*appear(cap1, shift=None), run_time=1.0)  # early: the tile's summary line
            self.tiles.append(VGroup(shapes, d_t, q_t, cap1))

            # t2: s2's Q row drifting to the RED halfway level, beside the voltage axis
            c.wait_until("r2")
            q0, q_bad = q_row()
            V = volt_axis()
            bands = VGroup(V.axis, V.ok0, V.ok1, V.bad)
            shapes2 = VGroup(q0, q_bad, bands, V.level)
            fit(shapes2, _p(TILE_X[1], TOP_Y))
            q_t2 = T("Q", 30, GREEN).next_to(q0, LEFT, buff=0.15)
            z_t = T("0", 30, GREEN).next_to(V.ok0, RIGHT, buff=0.15)
            o_t = T("1", 30, GREEN).next_to(V.ok1, RIGHT, buff=0.15)
            qm = T("???", 30, RED).next_to(q_bad.get_end(), UP, buff=0.2).shift(0.75 * LEFT)
            self.play(*self.dim_previous(), FadeIn(bands), Create(q0),
                      *appear(q_t2, z_t, o_t, shift=None), run_time=1.3)  # early: the axis labels with the axis
            c.wait_until("undefined")
            self.play(Create(q_bad), run_time=1.5)
            self.play(*appear(qm), run_time=0.9)
            c.wait_until("neither")
            self.play(Create(V.level), FlashAround(V.bad, color=RED, time_width=1.5), run_time=1.3)
            cap2 = caption([T("Q undefined:", CAP, t2c={"Q": GREEN, "undefined:": RED}),
                            T("neither 0 nor 1", CAP)], TILE_X[1], TOP_CAP)
            c.wait_until("valid one")
            self.play(*appear(cap2, shift=None), run_time=min(1.0, c.until("r3", floor=0.5)))  # early: the tile's summary line
            self.tiles.append(VGroup(shapes2, q_t2, z_t, o_t, qm, cap2))

            # t3: s3's hill, ball on the summit, arrows down both sides
            c.wait_until("r3")
            H = hill(labels=False)
            b = ball()
            place(b, H, 0.0)
            g3 = VGroup(H, b)
            fit(g3, _p(TILE_X[2], TOP_Y + 0.1), h=2.0)
            arrows = []
            for sgn in (-1, 1):
                a0 = H.point(sgn * 0.3) + 0.3 * UP + sgn * 0.05 * RIGHT
                a1 = H.point(sgn * 0.82) + 0.32 * UP + sgn * 0.15 * RIGHT
                arrows.append(Arrow(a0, a1, buff=0, stroke_width=4, color=RED, tip_length=0.18,
                                    max_tip_length_to_length_ratio=0.3))
            self.play(*self.dim_previous(), FadeIn(H), FadeIn(b, scale=0.6), run_time=1.2)
            c.wait_until("rolls off")
            self.play(*[GrowArrow(a) for a in arrows], run_time=1.2)
            c.wait_until("longer it takes")
            cap3 = caption([T("Metastable: resolves,", CAP, t2c={"Metastable:": RED}),
                            T("in its own time", CAP)], TILE_X[2], TOP_CAP)
            self.play(*appear(cap3, shift=None), run_time=1.0)  # early: the tile's summary line
            self.tiles.append(VGroup(g3, *arrows, cap3))

    # -- c4.recap.2: t4 decay, t5 synchroniser, t6 P_fail -----------------------------------------
    def clip2(self):
        with self.say("c4.recap.2") as c:
            # t4: the decay curve with a GOLD "÷ e" arc at every tau
            G = decay_graph(width=3.6, height=1.5)
            G.remove(G.ylab0, G.yl)
            for lb in G.tlabels:
                lb.scale(0.75)
            G.xl.scale(0.7)
            ax = G.ax

            def P(t):
                return ax.c2p(t, 0.9 * np.exp(-t))

            arcs, divs = [], []
            for i in range(1, 6):
                a = CurvedArrow(P(i - 1) + 0.12 * UP + 0.06 * RIGHT, P(i) + 0.14 * UP,
                                angle=-0.9 if i == 1 else -0.7, color=GOLD, stroke_width=3, tip_length=0.12)
                d = MathTex(r"\div e", font_size=28, color=GOLD).next_to(a.point_from_proportion(0.5),
                                                                         UR if i == 1 else UP, buff=0.06)
                arcs.append(a)
                divs.append(d)
            g4 = VGroup(G, *arcs, *divs)
            ctr4 = _p(TILE_X[0], BOT_Y)
            g4.shift(ctr4 - g4.get_center())
            self.play(*self.dim_previous(), FadeIn(VGroup(G.ax, G.ticks, G.ytick)),
                      *appear(*G.tlabels, G.xl, shift=None, lag=0.1), run_time=1.2)  # early: axis labels with the axes
            self.play(Create(G.curve), run_time=min(1.5, c.until("divided")))
            c.wait_until("divided")
            self.play(LaggedStart(*[AnimationGroup(Create(a), FadeIn(d)) for a, d in zip(arcs, divs)],
                                  lag_ratio=0.45), run_time=min(2.4, c.until("r5", floor=1.0)))  # early: one per step
            mf = model_formula(36)
            cap4 = caption([mf], TILE_X[0], BOT_CAP)
            self.play(*appear(cap4, shift=None), run_time=min(1.0, c.until("r5", floor=0.5)))
            self.tiles.append(VGroup(g4, cap4))

            # t5: s5's synchroniser over its timing diagram, text stripped, the FG t_res arrow
            c.wait_until("r5")
            C = sync_circuit()
            D = sync_timing()
            for f in (C.ff0, C.ff1):
                f.remove(f.d_l, f.q_l)
            circ = VGroup(C.ff0, C.ff1, C.btn, C.d0_w, C.link, C.bus, C.jdot, *C.clk_ws)
            traces = VGroup(D.g1, D.gs, D.g2, D.clk, D.d1_pre, D.d1_conv, D.d1_red1, D.d1_red2, D.d1_div,
                            D.d1_post, D.q_pre, D.q_x, D.q_post)
            tres = D.tres.arr
            g5 = VGroup(circ, traces, tres)
            s5 = fit(g5, _p(TILE_X[1], BOT_Y + 0.02), h=1.8)
            tres_l = MathTex("t_{res}", font_size=32, color=FG).next_to(tres, DOWN, buff=0.08)
            self.remove(tres)
            self.play(*self.dim_previous(), FadeIn(circ), FadeIn(traces), run_time=1.3)
            c.wait_until("one more flip-flop")
            self.play(FlashAround(C.ff1.box, color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("most of a period")
            self.play(grow_dim(tres, tip=0.16 * s5), *appear(tres_l), run_time=1.2)
            c.wait_until("settle")
            cap5 = caption([T("One more flip-flop:", CAP, t2c={"flip-flop:": YELLOW}),
                            T("a period to settle", CAP)], TILE_X[1], BOT_CAP)
            self.play(*appear(cap5, shift=None), run_time=min(1.0, c.until("r6", floor=0.5)))  # early: the tile's summary line
            self.tiles.append(VGroup(g5, tres_l, cap5))

            # t6: s6's bar (t_res + t_su = T_c) over the boxed P_fail formula
            c.wait_until("r6")
            bar = res_bar(x0=0.0, y=0.0, total=3.8, su=0.8)
            F = pfail_formula(size=56)
            F.next_to(bar, DOWN, buff=0.4)
            F.shift((bar.outline.get_x() - F.get_x()) * RIGHT)
            g6 = VGroup(bar, F)
            fit(g6, _p(TILE_X[2], BOT_Y), w=4.3, h=2.5)
            self.play(*self.dim_previous(), FadeIn(VGroup(*bar.segs, bar.outline)),
                      *appear(*bar.syms, bar.tc, shift=None, lag=0.15), FadeIn(F.box),
                      *appear(F.main, F.ins, shift=None), run_time=1.3)  # early: the tile's bar and formula shown whole
            c.wait_until("clock period")
            cap6 = fail_condition("Fails if")
            cap6.scale(0.72)
            cap6.move_to([TILE_X[2], 0, 0]).align_to([0, BOT_CAP, 0], UP)
            self.play(*appear(cap6, shift=None), FlashAround(bar.segs[1], color=GOLD, time_width=1.5),
                      run_time=1.2)  # early: the condition the sentence states
            c.wait_until("turns that into")
            self.play(FlashAround(F.box, color=YELLOW, time_width=1.5), run_time=min(1.2, c.until(floor=0.6)))
            self.tiles.append(VGroup(g6, cap6))

    # -- c4.recap.3: next time, MTBF --------------------------------------------------------------
    def clip3(self):
        C = sync_circuit()
        C.shift(_p(0.72, -0.7))
        years = MathTex(r"P_{fail}", r"\rightarrow", r"\text{years}", font_size=56, color=GOLD)
        cal = calendar().next_to(years, RIGHT, buff=0.45)
        yrs = VGroup(years, cal).move_to(_p(0, -1.3))
        part5 = T("Part 5 · Mean time between failures", 48).move_to([0, -2.85, 0])
        with self.say("c4.recap.3") as c:
            # {next}: the tiles dim, then clear for the synchroniser alone
            self.play(*self.dim_previous(), run_time=1.0)
            c.wait_until("actually fail")
            self.play(*during([FadeOut(m) for m in self.mobjects], 0.0, 0.45),
                      *during([FadeIn(C)], 0.5, 1.0), run_time=min(1.6, c.until("tiny chance", floor=1.0)))
            # a stream of input changes into D0, faster and faster
            c.wait_until("tiny chance")
            R = max(3.0, min(5.2, 0.85 * c.until("years")))
            xa = C.btn.out()[0] + 0.12
            xb = C.ff0.box.get_left()[0] - 0.1
            L = xb - xa
            wy = C.d0_w.get_y()
            sched = []
            t, d = 0.0, 0.95
            while True:
                T_i = max(0.36, min(1.15, 1.15 * d))
                if t + T_i > R - 0.05:
                    break
                sched.append((t, T_i))
                t += d
                d = max(0.3, d * 0.82)
            red_idx = {3, len(sched) - 3}
            ticks, flashes = [], []
            tr = ValueTracker(0.0)
            for i, (t0, Ti) in enumerate(sched):
                bar_ = Line(_p(0, wy - 0.3), _p(0, wy + 0.08)).set_stroke(BLUE, 6)
                tag = MathTex(r"P_{fail}", font_size=28, color=GOLD).next_to(bar_, DOWN, buff=0.1)
                tk = VGroup(bar_, tag).set_z_index(5)
                tk.t0, tk.Ti, tk.red = t0, Ti, i in red_idx

                def upd(m, t0=t0, Ti=Ti, red=tk.red, park=-30.0 - 3 * i):
                    p = (tr.get_value() - t0) / Ti
                    if p <= 0 or p >= 1:
                        m.set_opacity(0)
                        m.move_to(_p(park, m.get_y()))
                        return
                    m.shift((xa + p * L - m[0].get_x()) * RIGHT)
                    # the tag stays left of FF0 and is gone before the next tick starts (one tag at a time)
                    m[1].set_x(min(m[0].get_x(), xb - 0.05 - m[1].width / 2))
                    op = min(1.0, p / 0.15, (1 - p) / 0.15)
                    top = max(0.0, min(1.0, (p - 0.05) / 0.12, (0.72 - p) / 0.12))
                    hot = red and p > 0.55
                    m[0].set_stroke(RED if hot else BLUE, opacity=op)
                    m[1].set_fill(RED if hot else GOLD, opacity=top)
                tk.add_updater(upd)
                tk.set_opacity(0)
                ticks.append(tk)
                if tk.red:
                    ta = t0 + 0.6 * Ti
                    flashes.append(time_span(FlashAround(C.ff0.box, color=RED, time_width=1.5),
                                             ta, min(R, ta + 0.7)))
            self.add(*ticks)
            self.play(tr.animate.set_value(R), *flashes, run_time=R, rate_func=linear)
            for tk in ticks:
                tk.clear_updaters()
            self.remove(*ticks)
            # {years}
            c.wait_until("years")
            self.play(*appear(years), FadeIn(cal, shift=0.25 * DOWN), run_time=1.2)
        self.play(*appear(part5), run_time=1.0)  # early: the end card
