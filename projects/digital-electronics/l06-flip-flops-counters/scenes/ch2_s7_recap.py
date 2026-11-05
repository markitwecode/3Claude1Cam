"""Chapter 2, scene 7: recap in five panels, then next time (J-K, T, asynchronous inputs). Clips c2.recap.1 – c2.recap.2."""
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


# ---- common latch geometry (s1's make_latch) ------------------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0

# ---- recap grid: 3 tiles on top, 2 below -----------------------------------------------------
TOP_X = (-4.55, 0.0, 4.55)
BOT_X = (-2.4, 2.4)
VIS_Y = (2.3, -1.05)
CAP_Y = (1.15, -2.25)          # caption tops
TILE_W, TILE_H = (4.1, 2.0), (4.1, 2.1)


def vis_at(i):
    return _p(TOP_X[i], VIS_Y[0]) if i < 3 else _p(BOT_X[i - 3], VIS_Y[1])


def fit(m, i):
    w, h = TILE_W if i < 3 else TILE_H
    s = min(w / m.width, h / m.height)
    m.scale(s, about_point=m.get_center())
    m.move_to(vis_at(i))
    return s


def caption(text, i, **kw):
    y = CAP_Y[0] if i < 3 else CAP_Y[1]
    t = T(text, 28, line_spacing=0.8, **kw)
    return t.move_to(_p(vis_at(i)[0], y), aligned_edge=UP).set_x(vis_at(i)[0])


# ---- {r1}: s1's two CLK traces ---------------------------------------------------------------
S1_X0, S1_X1 = -2.0, 6.0
CLK_H = 0.8
S1_TOP, S1_BOT = 1.4, -1.5
RISES = [k * 0.25 + 0.0625 for k in range(4)]
FALLS = [k * 0.25 + 0.1875 for k in range(4)]


def sx(u):
    return S1_X0 + u * (S1_X1 - S1_X0)


def s1_wave(y0, h=CLK_H):
    level, pts = 0, [[S1_X0, y0, 0]]
    for u in sorted(RISES + FALLS):
        pts += [[sx(u), y0 + level * h, 0], [sx(u), y0 + (1 - level) * h, 0]]
        level = 1 - level
    pts.append([S1_X1, y0 + level * h, 0])
    return VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 4)


def panel_window():
    top = s1_wave(S1_TOP)
    bot = s1_wave(S1_BOT).set_stroke(YELLOW, 2, opacity=0.55)
    bands = [Rectangle(width=sx(f) - sx(r), height=CLK_H).set_stroke(width=0)
             .set_fill(YELLOW, 0.18).set_z_index(-1)
             .move_to([(sx(r) + sx(f)) / 2, S1_TOP + CLK_H / 2, 0]) for r, f in zip(RISES, FALLS)]
    arrows = [Arrow([sx(r), S1_BOT - 0.05, 0], [sx(r), S1_BOT + CLK_H + 0.35, 0], buff=0,
                    stroke_width=6, tip_length=0.22, max_tip_length_to_length_ratio=0.3,
                    color=YELLOW) for r in RISES]
    dots = [Dot([sx(r), S1_BOT, 0], radius=0.1, color=YELLOW) for r in RISES]
    g = VGroup(*bands, top, bot, *arrows, *dots)
    g.bands, g.arrows, g.dots, g.top = bands, arrows, dots, top
    fit(g, 0)
    return g


# ---- {r2}: s2's feedback latch and one buzzing window (copied from ch2_s2_window) --------------
def feedback_latch(center=ORIGIN, s=0.8):
    c = np.array(center)
    FB_EN = 0.6

    def P(x, y):
        return c + s * _p(x, y)

    hw, hh = s * BOX_W / 2, s * BOX_H / 2
    g = VGroup()
    g.box = Rectangle(width=2 * hw, height=2 * hh).set_stroke(FG, 4).set_fill(BG, 1).move_to(c)
    g.sq = Square(0.2).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(g.box.get_bottom())
    xr_q = BOX_W / 2 + WIRE + 0.85
    g.d_w = Line(P(-BOX_W / 2 - WIRE, PIN_Y), P(-BOX_W / 2, PIN_Y)).set_stroke(BLUE, 5)
    g.q_w = Line(P(BOX_W / 2, PIN_Y), P(xr_q, PIN_Y)).set_stroke(GREEN, 5)
    g.qb_w = Line(P(BOX_W / 2, -PIN_Y), P(BOX_W / 2 + WIRE, -PIN_Y)).set_stroke(GREEN, 5)
    g.en_w = Line(P(0, -BOX_H / 2 - FB_EN), P(0, -BOX_H / 2) + 0.1 * DOWN).set_stroke(BLUE, 5)
    g.d_l = T("D", 36, BLUE).move_to(P(-BOX_W / 2, PIN_Y) + 0.3 * RIGHT)
    g.q_l = T("Q", 36, GREEN).move_to(P(BOX_W / 2, PIN_Y) + 0.3 * LEFT)
    g.qb_l = MathTex(r"\overline{Q}", font_size=40, color=GREEN).move_to(P(BOX_W / 2, -PIN_Y) + 0.3 * LEFT)
    g.en_l = T("EN", 30, BLUE).move_to(g.box.get_bottom() + 0.42 * UP)
    xr, top, xl, r = BOX_W / 2 + WIRE + 0.4, BOX_H / 2 + 0.45, -(BOX_W / 2 + WIRE + 0.4), 0.17
    arc = [_p(xr + r * np.cos(a), PIN_Y + r * np.sin(a)) for a in np.linspace(-PI / 2, PI / 2, 13)]
    pts = ([_p(BOX_W / 2 + WIRE, -PIN_Y), _p(xr, -PIN_Y), _p(xr, PIN_Y - r)] + arc[1:-1]
           + [_p(xr, PIN_Y + r), _p(xr, top), _p(xl, top), _p(xl, PIN_Y), _p(-BOX_W / 2 - WIRE, PIN_Y)])
    g.loop = VMobject().set_points_as_corners([c + s * q for q in pts]).set_stroke(GREEN, 5)
    g.clk_w = g.en_w.copy().set_stroke(YELLOW, 6).set_z_index(1)
    g.clk_l = T("CLK", 32, YELLOW).next_to(g.en_w.get_start(), LEFT, buff=0.18).shift(0.12 * UP)
    g.add(g.loop, g.d_w, g.q_w, g.qb_w, g.en_w, g.clk_w, g.box, g.sq, g.d_l, g.q_l, g.qb_l, g.clk_l)
    g.labels = [(g.d_l, 36, 28), (g.q_l, 36, 28), (g.qb_l, 40, 32), (g.clk_l, 32, 28)]   # EN dropped: too small here
    return g


def red_buzz(x_r, x_f, y_lo, h, offset, step, n, start_high, color=RED, width=4):
    lv = start_high
    pts = [(x_r, y_lo + h * lv)]
    for k in range(n):
        x = x_r + offset + k * step
        pts += [(x, y_lo + h * lv)]
        lv = 1 - lv
        pts += [(x, y_lo + h * lv)]
    pts.append((x_f, y_lo + h * lv))
    return poly(pts, color, width)


def buzz_window(w=2.4, h=0.6, gap=0.5, n=9):
    m = 0.35 * w
    x0, xr, xf, x1 = -w / 2 - m, -w / 2, w / 2, w / 2 + m
    yc = gap / 2
    g = VGroup()
    g.clk = poly([(x0, yc), (xr, yc), (xr, yc + h), (xf, yc + h), (xf, yc), (x1, yc)], YELLOW)
    g.band = Rectangle(width=w, height=2 * h + gap + 0.3).set_stroke(width=0).set_fill(YELLOW, 0.12)
    g.band.set_z_index(-1)
    g.buzz = red_buzz(xr, xf, -yc - h, h, 0.1 * w, 0.8 * w / (n - 1), n, 0)
    g.add(g.band, g.clk, g.buzz)
    return g


def panel_buzz():
    L = feedback_latch(ORIGIN, 0.8)
    bw = buzz_window(w=1.4, h=0.6, gap=0.5, n=8)
    bw.next_to(L, RIGHT, buff=0.35).align_to(L.box, DOWN).shift(0.1 * UP)
    g = VGroup(L, bw)
    g.L, g.bw = L, bw
    s = fit(g, 1)
    for lab, size, want in L.labels:
        bump(lab, want / (size * s))
    L.clk_l.next_to(L.en_w.get_start(), LEFT, buff=0.1).shift(0.1 * UP)
    return g


# ---- {r3}: s3's master-slave circuit (copied from ch2_s3_masterslave) ---------------------------
WIRE_W = 5
MX, SX, CY = -2.6, 2.6, 0.2
MS_PIN = CY + PIN_Y
MS_CLK_Y = -3.1                  # s3: -2.3; lowered so the CLK-bar / CLK labels fit at tile size
MS_EN_Y = CY - BOX_H / 2 - 0.1
X_IN, X_OUT = -5.3, 5.3
INV1_X, INV2_X = -4.3, 0.0
MS_S = 0.31
MS_K = 2.26                      # labels: 40 -> ~28 at tile size


def wire(*pts, color=FG, width=WIRE_W):
    return VMobject().set_points_as_corners([_p(*p) for p in pts]).set_stroke(color, width)


def latch_box(center=ORIGIN):
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4).set_fill(BG, 1)
    sq = Square(0.2).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(box.get_bottom())
    g = VGroup(box, sq)
    g.box, g.square = box, sq
    g.shift(center)
    return g


def inverter(x, y, color=BLUE):
    tri = Polygon(_p(x - 0.4, y + 0.35), _p(x - 0.4, y - 0.35), _p(x + 0.3, y))
    tri.set_stroke(color, 4).set_fill(BG, 1)
    bubble = Circle(radius=0.08).set_stroke(color, 4).set_fill(BG, 1).move_to(_p(x + 0.38, y))
    return VGroup(tri, bubble)


def door_icon(is_open, height=0.8, color=None):
    h, w = height, 0.65 * height
    col = color or (GREEN if is_open else RED)
    frame = Rectangle(width=w, height=h).set_stroke(color or (GREEN if is_open else FG), 3).set_fill(BG, 1)
    g = VGroup(frame)
    if is_open:
        swing = 0.42 * w
        panel = Polygon(_p(-w / 2, h / 2), _p(-w / 2, -h / 2), _p(-w / 2 - swing, -h / 2 - 0.1 * h),
                        _p(-w / 2 - swing, h / 2 + 0.1 * h))
        panel.set_stroke(col, 2).set_fill(col, 0.85)
        g.add(panel)
    else:
        panel = Rectangle(width=w - 0.12 * h, height=h - 0.12 * h).set_stroke(width=0).set_fill(col, 0.9)
        knob = Dot(_p(w / 2 - 0.2 * w, 0), radius=0.045 * h / 0.8, color=BG)
        g.add(panel, knob)
    return g


def panel_ms():
    g = VGroup()
    g.master, g.slave = latch_box(_p(MX, CY)), latch_box(_p(SX, CY))
    for lb in (g.master, g.slave):
        lb.set_z_index(1)
    g.lab_master = T("Master", 40).move_to(_p(MX, 1.95))
    g.lab_slave = T("Slave", 40).move_to(_p(SX, 1.95))
    g.d_wire = wire((X_IN, MS_PIN), (MX - BOX_W / 2, MS_PIN), color=BLUE)
    g.lab_d = T("D", 40, BLUE)
    g.qint_wire = wire((MX + BOX_W / 2, MS_PIN), (SX - BOX_W / 2, MS_PIN), color=TEAL)
    g.lab_qint = MathTex(r"Q_{\mathrm{int}}", font_size=44, color=TEAL)
    g.q_wire = wire((SX + BOX_W / 2, MS_PIN), (X_OUT, MS_PIN), color=GREEN)
    g.lab_q = T("Q", 40, GREEN)
    g.clk_wire = wire((X_IN, MS_CLK_Y), (INV1_X - 0.4, MS_CLK_Y), color=YELLOW, width=6)
    g.inv1 = inverter(INV1_X, MS_CLK_Y).set_z_index(1)
    g.clkb_wire = wire((INV1_X + 0.46, MS_CLK_Y), (MX, MS_CLK_Y), (MX, MS_EN_Y), color=YELLOW, width=6)
    g.node = Dot(_p(MX, MS_CLK_Y), radius=0.09, color=YELLOW)
    g.mid_wire = wire((MX, MS_CLK_Y), (INV2_X - 0.4, MS_CLK_Y), color=YELLOW, width=6)
    g.inv2 = inverter(INV2_X, MS_CLK_Y).set_z_index(1)
    g.clk2_wire = wire((INV2_X + 0.46, MS_CLK_Y), (SX, MS_CLK_Y), (SX, MS_EN_Y), color=YELLOW, width=6)
    g.lab_clkb = MathTex(r"\overline{\mathrm{CLK}}", font_size=40, color=YELLOW)
    g.lab_clk2 = MathTex(r"\mathrm{CLK}", font_size=40, color=YELLOW)
    g.add(g.d_wire, g.qint_wire, g.q_wire, g.clk_wire, g.clkb_wire, g.mid_wire, g.clk2_wire, g.node,
          g.master, g.slave, g.inv1, g.inv2)
    g.scale(MS_S, about_point=ORIGIN)
    labs = (g.lab_master, g.lab_slave, g.lab_d, g.lab_q, g.lab_qint, g.lab_clkb, g.lab_clk2)
    for lab in labs:
        lab.scale(MS_S * MS_K)
    g.lab_d.next_to(g.d_wire.get_start(), LEFT, buff=0.1)
    g.lab_q.next_to(g.q_wire.get_end(), RIGHT, buff=0.1)
    g.lab_qint.next_to(g.qint_wire, DOWN, buff=0.1)
    g.lab_master.next_to(g.master.box, UP, buff=0.1)
    g.lab_slave.next_to(g.slave.box, UP, buff=0.1)
    for lab, lb in ((g.lab_clkb, g.master), (g.lab_clk2, g.slave)):
        y = (lb.box.get_bottom()[1] + g.clk_wire.get_y()) / 2
        lab.move_to(_p(lb.box.get_x() - 0.12 - lab.width / 2, y))
    g.add(*labs)
    g.move_to(vis_at(2))
    return g


def ms_door(lb, is_open):
    return door_icon(is_open, 0.42).move_to(lb.box.get_center()).set_z_index(3)


# ---- {r4}: s4-s5's diagram cut down to CLK, D, Q ------------------------------------------------
class MiniTiming(VGroup):
    AMP = 0.2

    def __init__(self, x0=-1.45, x1=2.05, pitch=0.8):
        super().__init__()
        P = (x1 - x0) / 5.1
        self.x0, self.x1, self.P = x0, x1, P
        self.fall = [x0 + 0.4 * P + k * P for k in range(5)]
        self.rise = [f + 0.5 * P for f in self.fall]
        self.row_y = [pitch, 0.0, -pitch]
        self.labels = VGroup(*[MathTex(t, font_size=34, color=col).move_to(_p(0, y))
                               .align_to(_p(x0 - 0.2, 0), RIGHT)
                               for t, col, y in zip([r"\mathrm{CLK}", "D", "Q"], [YELLOW, BLUE, GREEN],
                                                    self.row_y)])
        g_top, g_bot = self.row_y[0] + self.AMP + 0.12, self.row_y[2] - self.AMP - 0.12
        self.guides = VGroup(*[Line(_p(x, g_top), _p(x, g_bot)).set_stroke(FG, 2.5).set_z_index(-2)
                               for x in self.rise[:4]])
        pts = [(x0, 1)]
        for f, r in zip(self.fall, self.rise):
            pts += [(f, 1), (f, 0), (r, 0), (r, 1)]
        pts.append((x1, 1))
        self.clk = self.path(0, pts, YELLOW)
        xr, xf = self.rise[0] + 0.25 * P, self.rise[2] + 0.2 * P
        self.d = self.path(1, [(x0, 0), (xr, 0), (xr, 1), (xf, 1), (xf, 0), (x1, 0)], BLUE)
        r = self.rise
        self.q = self.path(2, [(x0, 1), (r[0], 1), (r[0], 0), (r[1], 0), (r[1], 1), (r[3], 1), (r[3], 0),
                               (x1, 0)], GREEN)
        self.qvals = [set_backstroke(MathTex(str(b), font_size=30, color=GREEN)
                                     .move_to(_p(r[k] + 0.17, self.row_y[2])), width=8)
                      for k, b in enumerate([0, 1, 1, 0])]
        self.add(self.guides, self.labels, self.clk, self.d, self.q, *self.qvals)

    def y(self, row, bit):
        return self.row_y[row] + (self.AMP if bit else -self.AMP)

    def path(self, row, pts, color, width=4):
        return VMobject().set_points_as_corners([_p(x, self.y(row, b)) for x, b in pts]).set_stroke(color, width)


def panel_timing():
    td = MiniTiming()
    td.move_to(vis_at(3))
    return td


# ---- {r5}: s6's latch and flip-flop symbols ----------------------------------------------------
def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_latch(center=ORIGIN):
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    sq = Square(0.2).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(box.get_bottom())
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    en_w = Line([0, -BOX_H / 2 - EN_WIRE, 0], [0, -BOX_H / 2 - 0.1, 0]).set_stroke(BLUE, 5)
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    en_l = T("EN", 30, BLUE).move_to([0, -BOX_H / 2 + 0.42, 0])
    g = VGroup(d_w, q_w, en_w, box, sq, d_l, q_l, en_l)
    g.box, g.sq, g.labels = box, sq, [d_l, q_l, en_l]
    g.shift(center)
    return g


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), clr=False):
    """s6's make_ff box, pins and triangle; `ins` = (label, y) BLUE inputs on the left."""
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, 36, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(*in_w, q_w, qb_w, clk_w, box, tri, *in_l, q_l, qb_l)
    g.box, g.tri, g.clk_w = box, tri, clk_w
    g.labels = [*in_l, q_l, qb_l]
    g.shift(center)
    return g


def panel_symbols():
    lt = make_latch(_p(-1.75, 0))
    ff = make_ff(_p(1.75, 0))
    g = VGroup(lt, ff)
    g.lt, g.ff = lt, ff
    s = fit(g, 4)
    for lab in lt.labels + ff.labels:
        bump(lab, 28 / (36 * s) if lab is not lt.labels[2] else 28 / (30 * s))
    # the markers the narration points at, 2x so they read at tile size
    lt.sq.scale(2.0, about_point=lt.sq.get_center())
    ff.tri.scale(2.0, about_point=ff.tri.get_bottom())
    ff.clk_w.put_start_and_end_on(ff.clk_w.get_start(), ff.tri.get_bottom() + 0.01 * UP)
    lt.labels[2].next_to(lt.sq, UP, buff=0.06)
    return g


# ---- {next}: the J-K and T boxes, CLR and its timing --------------------------------------------
JK_C, TF_C = _p(-4.7, 0.2), _p(-1.1, 0.2)      # with the timing and "?": bbox x -6.3 .. 6.3
CLR_DX = 0.55                 # CLR pin 0.55 right of the clock pin
TM_X0, TM_X1 = 2.15, 5.45
PAIR_DX = 2.9                 # the boxes start centred, slide left on {async}
CLK_ROW, CLR_ROW, AMP2 = 0.45, -1.15, 0.25


def async_timing():
    P = 1.5
    rises = [TM_X0 + 0.4, TM_X0 + 0.4 + P]
    pts = [(TM_X0, CLK_ROW - AMP2)]
    for r in rises:
        pts += [(r, CLK_ROW - AMP2), (r, CLK_ROW + AMP2), (r + P / 2, CLK_ROW + AMP2),
                (r + P / 2, CLK_ROW - AMP2)]
    pts.append((TM_X1, CLK_ROW - AMP2))
    clk = poly(pts, YELLOW)
    arrows = [Arrow(_p(r, CLK_ROW - AMP2 - 0.1), _p(r, CLK_ROW + AMP2 + 0.35), buff=0, stroke_width=6,
                    tip_length=0.2, max_tip_length_to_length_ratio=0.3, color=YELLOW) for r in rises]
    a, b = rises[0] + 0.55 * P - 0.25, rises[0] + 0.55 * P + 0.25
    clr = poly([(TM_X0, CLR_ROW - AMP2), (a, CLR_ROW - AMP2), (a, CLR_ROW + AMP2), (b, CLR_ROW + AMP2),
                (b, CLR_ROW - AMP2), (TM_X1, CLR_ROW - AMP2)], RED)
    pulse = poly([(a, CLR_ROW - AMP2), (a, CLR_ROW + AMP2), (b, CLR_ROW + AMP2), (b, CLR_ROW - AMP2)], RED, 9)
    lab_clk = T("CLK", 30, YELLOW).move_to(_p(0, CLK_ROW)).align_to(_p(TM_X0 - 0.2, 0), RIGHT)
    lab_clr = T("CLR", 30, RED).move_to(_p(0, CLR_ROW)).align_to(_p(TM_X0 - 0.2, 0), RIGHT)
    return VGroup(lab_clk, clk), arrows, VGroup(lab_clr, clr), pulse


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c2.recap.1
    def clip1(self):
        with self.say("c2.recap.1", gap=2.0) as c:
            # {r1}: a window, or an instant
            p1 = panel_window()
            cap1 = caption("a window,\nor an instant", 0)
            c.wait_until("r1")
            self.play(*appear(p1, shift=None), *during(appear(cap1), 0.4, 1.0), run_time=1.5)  # early: recap tile, seen whole
            c.wait_until("whole window")
            self.play(*[b.animate.set_fill(YELLOW, 0.4) for b in p1.bands],
                      *[VShowPassingFlash(p1.top.copy().set_stroke(YELLOW, 8), time_width=0.6)],
                      run_time=1.2)
            self.play(*[b.animate.set_fill(YELLOW, 0.18) for b in p1.bands], run_time=0.6)
            c.wait_until("edge")
            self.play(*flash(p1.arrows, time_width=1.5, buff=0.06), run_time=min(1.3, c.until("r2")))

            # {r2}: fed back, a latch oscillates
            p2 = panel_buzz()
            cap2 = caption("fed back,\na latch oscillates", 1)
            c.wait_until("r2")
            self.play(*appear(p2, shift=None), *during(appear(cap2), 0.4, 1.0), run_time=1.5)  # early: recap tile, seen whole
            c.wait_until("oscillates")
            self.play(VShowPassingFlash(p2.L.loop.copy().set_stroke(GREEN, 9), time_width=0.5),
                      VShowPassingFlash(p2.bw.buzz.copy().set_stroke(RED, 8), time_width=0.5),
                      run_time=1.5)
            c.wait_until("window is open")
            self.play(p2.bw.band.animate.set_fill(YELLOW, 0.3), run_time=0.8)
            self.play(p2.bw.band.animate.set_fill(YELLOW, 0.12), run_time=min(0.8, c.until("r3")))

            # {r3}: two latches, never open together
            p3 = panel_ms()
            d_m, d_s = ms_door(p3.master, True), ms_door(p3.slave, False)
            cap3 = caption("two latches,\nnever open together", 2)
            c.wait_until("r3")
            self.play(*appear(p3, shift=None), *during(appear(cap3), 0.4, 1.0), run_time=1.5)  # early: recap tile, seen whole
            self.play(FadeIn(d_m, scale=0.7), FadeIn(d_s, scale=0.7), run_time=0.8)
            c.wait_until("opposite phases")
            d_m2, d_s2 = ms_door(p3.master, False), ms_door(p3.slave, True)
            self.play(*during([FadeOut(d_m, scale=0.7), FadeOut(d_s, scale=0.7)], 0, 0.45),
                      *during([FadeIn(d_m2, scale=0.7), FadeIn(d_s2, scale=0.7)], 0.5, 1.0),
                      run_time=1.2)
            c.wait_until("never transparent")
            self.play(*flash([p3.lab_clkb, p3.lab_clk2], time_width=1.5, buff=0.06),
                      run_time=min(1.5, c.until("r4")))

            # {r4}: Q takes D at each rising edge
            p4 = panel_timing()
            cap4 = caption("Q takes D at\neach rising edge", 3,
                           t2c={"Q": GREEN, "D": BLUE, "rising edge": YELLOW})
            c.wait_until("r4")
            self.play(*appear(p4, shift=None), *during(appear(cap4), 0.4, 1.0), run_time=1.5)  # early: recap tile, seen whole
            c.wait_until("rising edge")
            self.play(*[time_span(VShowPassingFlash(g.copy().set_stroke(YELLOW, 6), time_width=1.0),
                                  0.25 * k, 0.25 * k + 0.8) for k, g in enumerate(p4.guides)],
                      run_time=1.55)
            c.wait_until("holds it")
            r = p4.rise
            self.play(*[VShowPassingFlash(Line(_p(r[k], p4.y(2, b)), _p(r[k + 1], p4.y(2, b)))
                                          .set_stroke(GREEN, 10), time_width=1.0, taper_width=0.1)
                        for k, b in enumerate([0, 1, 1])],
                      run_time=min(1.5, c.until("r5")))

            # {r5}: square: latch, triangle: flip-flop
            p5 = panel_symbols()
            cap5 = caption("square: latch,\ntriangle: flip-flop", 4)
            c.wait_until("r5")
            self.play(*appear(p5, shift=None), *during(appear(cap5), 0.4, 1.0), run_time=1.5)  # early: recap tile, seen whole
            c.wait_until("square")
            self.play(p5.lt.sq.animate.set_stroke(YELLOW), FlashAround(p5.lt.sq, buff=0.08, time_width=1.5),
                      run_time=1.5)
            c.wait_until("triangle")
            self.play(p5.ff.tri.animate.set_stroke(YELLOW), FlashAround(p5.ff.tri, buff=0.08, time_width=1.5),
                      run_time=min(1.5, c.until(floor=0.8)))
            c.wait_until()

    # ------------------------------------------------------------------ c2.recap.2
    def clip2(self):
        with self.say("c2.recap.2") as c:
            # {next}: the panels shrink away; J-K and T boxes
            old = list(self.mobjects)
            title = T("Next: J-K and T flip-flops", 48, t2c={"Next:": YELLOW}).move_to(_p(0, 3.2))
            jk = make_ff(JK_C + PAIR_DX * RIGHT, ins=(("J", PIN_Y), ("K", -PIN_Y)))
            tf = make_ff(TF_C + PAIR_DX * RIGHT, ins=(("T", PIN_Y),))
            lag = 0.6 / max(1, len(old) - 1)          # the whole sweep ends at 1.3 s
            self.play(*[time_span(FadeOut(m, scale=0.5), lag * k, lag * k + 0.7)
                        for k, m in enumerate(old)],
                      run_time=1.3)
            self.play(FadeIn(title, shift=0.2 * DOWN), run_time=0.8)
            self.play(*appear(jk, tf, shift=None, lag=0.3), run_time=min(1.5, c.until("async")))  # early: the pair is named together
            c.wait_until("async")

            # {async}: a RED CLR pin under the T box, a RED pulse between two clock arrows
            hb = BOX_H / 2
            clr_w = Line(TF_C + _p(CLR_DX, -hb - EN_WIRE), TF_C + _p(CLR_DX, -hb)).set_stroke(RED, 5)
            clr_l = T("CLR", 30, RED).next_to(clr_w.get_start(), DOWN, buff=0.15)
            self.play(jk.animate.shift(PAIR_DX * LEFT), tf.animate.shift(PAIR_DX * LEFT), run_time=0.9)
            self.play(GrowFromEdge(clr_w, UP), *during(appear(clr_l), 0.3, 1.0), run_time=1.0)
            clk_row, arrows, clr_row, pulse = async_timing()
            self.play(*appear(clk_row, clr_row, shift=None, lag=0.3),
                      *[during([GrowArrow(a)], 0.5, 1.0)[0] for a in arrows],
                      run_time=1.3)
            self.play(VShowPassingFlash(pulse, time_width=1.0, taper_width=0.1),
                      run_time=min(1.3, c.until("why")))
            c.wait_until("why")

            # {why}: a YELLOW "?" beside it
            q = T("?", 72, YELLOW).move_to(_p(TM_X1 + 0.6, (CLK_ROW + CLR_ROW) / 2))
            self.play(*appear(q), run_time=1.0)
            c.wait_until()
        # end card, carried by the music
        self.wait(8.0)
