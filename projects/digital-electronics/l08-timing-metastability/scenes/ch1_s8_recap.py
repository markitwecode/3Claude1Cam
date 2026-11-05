"""Chapter 1, scene 8: recap in six panels, then the teaser for Part 2 (hold time).
Clips c1.recap.1 – c1.recap.3.

Panels (3 x 2 grid, columns x = -4.65, 0, 4.65): r1 clock + T_c + f_c = 1/T_c, r2 the CLK/D/Q window,
r3 the path, r4 data-sheet conventions, r5 the budget bar + T_c >= ..., r6 the 1 ns bar + t_pd <= ...
End card: s4's path (scale 0.8, centred (0, 1.1)), FF1's window RED, YELLOW "?" at (0, -1.55),
"Part 2 · Hold time" T 48 at (0, -2.85).
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
# r1: copied from ch1_s2_clock.py (ClockWave, dim_arrow -> s2_dim_arrow, clock_with_period)
# =============================================================================================
class ClockWave(VGroup):
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
        return self.wave.get_left()[0] + self._rise[i] * self.wave.width / self._width


def s2_dim_arrow(x0, x1, y, color=YELLOW, guide_bottom=None, label=None, gap=0.2):
    line = DoubleArrow([x0, y, 0], [x1, y, 0], buff=0, stroke_width=3, tip_length=0.14,
                       max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=20,
                       color=color)
    lo = y - 0.6 if guide_bottom is None else guide_bottom
    guides = VGroup(*[Line([x, lo, 0], [x, y + 0.18, 0]).set_stroke(DIM, 2) for x in (x0, x1)])
    g = VGroup(guides, line)
    g.line, g.guides, g.label = line, guides, None
    if label is not None:
        label.set_color(color).next_to(line, UP, buff=gap)
        g.add(label)
        g.label = label
    return g


C2_W, C2_H, C2_Y, C2_ARROW_Y = 10.0, 1.0, 1.9, 2.8


def clock_with_period(periods=5, i=1, label=True):
    wave = ClockWave(width=C2_W, height=C2_H, periods=periods).move_to([0, C2_Y, 0])
    lbl = MathTex("T_c", font_size=48) if label else None
    arrow = s2_dim_arrow(wave.rising_x(i), wave.rising_x(i + 1), C2_ARROW_Y,
                         guide_bottom=C2_Y - C2_H / 2, label=lbl, gap=0.12)
    g = VGroup(wave, arrow)
    g.wave, g.arrow = wave, arrow
    return g


# =============================================================================================
# r2: copied from ch1_s3_ffnumbers.py (dim_arrow -> s3_dim_arrow, WindowDiagram)
# =============================================================================================
def s3_dim_arrow(a, b, color, base_a=None, base_b=None, width=3, tip=0.14):
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
        self.lab_clk, self.lab_d, self.lab_q = [
            MathTex(t, font_size=44 * fs, color=c).move_to(P(0, y)).align_to(P(self.X0 - 0.3, 0), RIGHT)
            for t, c, y in zip([r"\mathrm{CLK}", "D", "Q"], [YELLOW, BLUE, GREEN], self.row_y)]
        self.guide = Line(P(0, H + A + 0.3), P(0, -H - A - 0.2)).set_stroke(DIM, 1.5).set_z_index(-2)
        self.up = (Triangle().scale(0.12 * max(k, 0.8)).set_stroke(width=0).set_fill(YELLOW, 1)
                   .move_to(P(0, H)))
        self.clk = self.path(0, [(self.X0, 1), (-2.3, 1), (-2.3, 0), (0, 0), (0, 1), (2.3, 1),
                                 (2.3, 0), (self.X1, 0)], YELLOW, sw)
        self.d = self.path(1, [(self.X0, 0), (-self.T_SU, 0), (-self.T_SU, 1), (self.T_HOLD, 1),
                               (self.T_HOLD, 0), (self.X1, 0)], BLUE, sw)
        self.q = self.path(2, [(self.X0, 0), (self.T_PC, 0), (self.T_PC, 1), (self.X1, 1)], GREEN, sw)
        ya, yp = A + 0.55, -H - A - 0.45
        self.su = s3_dim_arrow(P(-self.T_SU, ya), P(0, ya), GOLD, P(0, A)[1], P(0, A)[1])
        self.hold = s3_dim_arrow(P(0, ya), P(self.T_HOLD, ya), GOLD, P(0, A)[1], P(0, A)[1])
        self.pc = s3_dim_arrow(P(0, yp), P(self.T_PC, yp), PINK, P(0, -H - A)[1], P(0, -H - A)[1])
        mt = 44 * fs
        self.sym_su = MathTex(r"t_{\mathrm{su}}", font_size=mt, color=GOLD).next_to(self.su.arrow, LEFT, buff=0.15)
        self.sym_hold = MathTex(r"t_{\mathrm{hold}}", font_size=mt, color=GOLD).next_to(self.hold.arrow, RIGHT, buff=0.15)
        self.sym_pc = MathTex(r"t_{\mathrm{pc}}", font_size=mt, color=PINK).next_to(self.pc.arrow, RIGHT, buff=0.15)
        self.band = (Rectangle(width=k * (self.T_SU + self.T_HOLD), height=k * (2 * A + 0.3))
                     .set_stroke(width=0).set_fill(GOLD, 0.25).set_z_index(-3)
                     .move_to(P((self.T_HOLD - self.T_SU) / 2, 0)))

    def P(self, x, y):
        return self.o + self.k * np.array([x, y, 0.0])

    def path(self, row, pts, color, width):
        y0 = self.row_y[row]
        return (VMobject().set_points_as_corners([self.P(x, y0 + (self.AMP if b else -self.AMP)) for x, b in pts])
                .set_stroke(color, width))


# =============================================================================================
# r3 / end card: copied from ch1_s4_path.py (make_ff, qbar, path_diagram)
# =============================================================================================
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
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    g.box, g.tri = box, tri
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


P_FF_X = (-4.4, 4.4)
P_FF_Y = 0.5
P_PIN = P_FF_Y + PIN_Y
P_BUS = P_FF_Y - BOX_H / 2 - EN_WIRE
P_BUS_X0 = -5.6
P_CL_W, P_CL_H = 3.4, 1.6


def path_diagram():
    P = VGroup()
    ffs = []
    for x in P_FF_X:
        f = make_ff(_p(x, P_FF_Y))
        f.remove(f.clk_w)
        ffs.append(f)
    P.ff0, P.ff1 = ffs
    P.names = [T(f"FF{i}", 36, FG).next_to(f.box, UP, buff=0.2) for i, f in enumerate(ffs)]
    x_q0 = P_FF_X[0] + BOX_W / 2 + WIRE
    x_d1 = P_FF_X[1] - BOX_W / 2 - WIRE
    P.cl = Rectangle(width=P_CL_W, height=P_CL_H).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(0, P_PIN))
    P.cl_l = VGroup(T("Combinational", 32, BLUE), T("Logic (CL)", 32, BLUE)).arrange(DOWN, buff=0.12).move_to(P.cl)
    P.q0_w = Line(_p(x_q0, P_PIN), _p(-P_CL_W / 2, P_PIN)).set_stroke(GREEN, 5)
    P.d1_w = Line(_p(P_CL_W / 2, P_PIN), _p(x_d1, P_PIN)).set_stroke(BLUE, 5)
    P.q0_l = MathTex("Q_0", font_size=40, color=GREEN).next_to(_p(x_q0, P_PIN), UP, buff=0.15)
    P.d1_l = MathTex("D_1", font_size=40, color=BLUE).next_to(_p(x_d1, P_PIN), UP, buff=0.15)
    P.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(P.ff0.d_w, LEFT, buff=0.12)
    P.q1_l = MathTex("Q_1", font_size=40, color=GREEN).next_to(P.ff1.q_w, RIGHT, buff=0.12)
    P.clk_bus = Line(_p(P_BUS_X0, P_BUS), _p(P_FF_X[1], P_BUS)).set_stroke(YELLOW, 5)
    P.clk_dot = Dot(_p(P_FF_X[0], P_BUS), radius=0.08, color=YELLOW)
    P.clk_l = T("CLK", 34, YELLOW).next_to(_p(P_BUS_X0, P_BUS), LEFT, buff=0.15)
    P.clk_br0, P.clk_br1 = ffs[0].clk_w, ffs[1].clk_w
    P.all = [P.ff0, P.ff1, *P.names, P.cl, P.cl_l, P.q0_w, P.q0_l, P.d1_w, P.d1_l, P.d0_l, P.q1_l,
             P.clk_bus, P.clk_dot, P.clk_l, P.clk_br0, P.clk_br1]
    P.add(*P.all)

    def clk_paths(width=10):
        s = P.clk_bus.get_start()
        out = []
        for br in (P.clk_br0, P.clk_br1):
            a, b = br.get_start(), br.get_end()
            out.append(VMobject().set_points_as_corners([s, a, b]).set_stroke(YELLOW, width))
        return out
    P.clk_paths = clk_paths
    return P


# =============================================================================================
# r4: copied from ch1_s5_datasheet.py (clock_wave -> ds_clock_wave, bus, hatch)
# =============================================================================================
WAVE_W = 4
ROW_H = 0.8
SLOPE = 0.35


def ds_clock_wave(x0, x1, y, edges, h=ROW_H, slope=SLOPE, color=YELLOW, start_low=True):
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
    w = (b - a) / n
    return [(a + i * w, a + (i + 1) * w) for i in range(n)]


# =============================================================================================
# r5: copied from ch1_s6_setup.py (budget_bar -> bar6, the lecture's canonical bar)
# =============================================================================================
BAR_H = 0.5
BAR_FILL = 0.85
BAR_OUT_W = 3


def bar6(segs, total, x0=-3.3, y=0.0, tc_tex="T_c", syms=True, nums=None,
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


# =============================================================================================
# r6: copied from ch1_s7_marketing.py (padlock, budget_bar -> bar7, colored_tex); numbers may be None
# =============================================================================================
SEG_OP = 0.85
SEG_COLORS = (PINK, PURPLE, GOLD)
SEG_TEX = ("t_{pc}", "t_{pd}", "t_{su}")


def padlock(scale=1.0):
    body = RoundedRectangle(corner_radius=0.04, width=0.26, height=0.2)
    body.set_fill(BG, 1).set_stroke(width=0)
    shackle = Arc(radius=0.085, start_angle=0, angle=PI).set_stroke(BG, 3.5)
    shackle.move_to(body.get_top() + 0.075 * UP)
    lock = VGroup(shackle, body)
    lock.scale(scale)
    return lock


def bar7(pc, pd, su, tc, unit=1.0, x0=-3.3, y=0.8, tc_tex="T_c", syms=True, nums=None,
         locks=False, lock_scale=1.0, sym_size=40, num_size=34):
    """ch1_s7's pcs_bar: bar6 (= budget_bar) with the three standard segments and optional
    padlocks on t_pc and t_su (.locks, z 2). Here each padlock is shrunk to fit inside its segment."""
    segs = [(t, col, w * unit) for t, col, w in zip(SEG_TEX, SEG_COLORS, (pc, pd, su))]
    g = bar6(segs, tc * unit, x0, y, tc_tex, syms=syms, nums=nums,
             sym_size=sym_size, num_size=num_size)
    g.locks = []
    if locks:
        for r in (g.segs[0], g.segs[2]):
            lk = padlock(lock_scale)
            if lk.width > 0.75 * r.width:
                lk.scale(0.75 * r.width / lk.width)
            g.locks.append(lk.move_to(r).set_z_index(2))
        g.add(*g.locks)
    return g


def colored_tex(parts, colors, size=60):
    m = MathTex(*parts, font_size=size)
    for i, col in colors.items():
        m[i].set_color(col)
    return m
# =============================================================================================


# ---- recap grid ----------------------------------------------------------------------------
COL_X = (-4.55, 0.0, 4.55)
TOP_Y, BOT_Y = 2.25, -1.05          # visual centres
TOP_CAP, BOT_CAP = 0.95, -2.2       # caption top edges
PANEL_W = 4.2
CAP = 30


def fit(mob, w, h, center):
    mob.scale(min(w / mob.width, h / mob.height)).move_to(center)
    return mob


def caption(lines, x, top):
    g = VGroup(*lines).arrange(DOWN, buff=0.16)
    if g.width > PANEL_W + 0.2:
        g.scale_to_fit_width(PANEL_W + 0.2)
    g.move_to([x, 0, 0]).align_to([0, top, 0], UP)
    return g


def mt(parts, colors, size=CAP):
    """One caption line in MathTex; prose parts as \\text{...}."""
    return colored_tex(parts, colors, size)


class Recap(NarratedScene):
    def construct(self):
        self.panels = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- c1.recap.1: r1 clock, r2 window, r3 path -------------------------------------------------
    def clip1(self):
        with self.say("c1.recap.1") as c:
            # r1: clock wave + T_c; f_c = 1/T_c
            cw = clock_with_period(periods=4, i=1)
            fit(cw, PANEL_W, 1.3, [COL_X[0], TOP_Y + 0.45, 0])
            lab = cw.arrow.label
            lab.scale(1.75).next_to(cw.arrow.line, UP, buff=0.08)
            formula = MathTex("f_c", "=", r"\frac{1}{T_c}", font_size=44)
            formula[0].set_color(YELLOW)
            formula.move_to([COL_X[0], TOP_Y - 0.62, 0])
            cap1 = caption([T("frequency = 1 / period", CAP)], COL_X[0], TOP_CAP)
            c.wait_until("r1")
            self.play(Create(cw.wave.wave), FadeIn(cw.wave.ups), run_time=1.5, rate_func=linear)
            c.wait_until("time between")
            self.play(*appear(cw.arrow), run_time=1.0)
            c.wait_until("frequency")
            self.play(*appear(formula), run_time=1.0)
            self.play(*appear(cap1, shift=None), run_time=1.0)
            self.panels.append(VGroup(cw, formula, cap1))

            # r2: CLK / D / Q, the GOLD window, PINK t_pc
            w = WindowDiagram(origin=ORIGIN, k=0.6, fs=0.85)
            labs = [w.lab_clk, w.lab_d, w.lab_q, w.sym_su, w.sym_hold, w.sym_pc]
            shapes = [w.guide, w.up, w.clk, w.d, w.q, w.su, w.hold, w.pc, w.band]
            wd = VGroup(*shapes, *labs)
            fit(wd, PANEL_W, 2.35, [COL_X[1], TOP_Y, 0])
            for m in (w.lab_clk, w.lab_d, w.lab_q):
                m.scale(1.25, about_edge=RIGHT)
            w.sym_su.scale(1.25, about_edge=RIGHT)
            w.sym_hold.scale(1.25, about_edge=LEFT)
            w.sym_pc.scale(1.25, about_edge=LEFT)
            cap2 = caption([
                mt([r"\text{keep D still:}"], {0: GOLD}),
                mt([r"t_{\mathrm{su}}", r"\text{ before, }", r"t_{\mathrm{hold}}", r"\text{ after;}"],
                   {0: GOLD, 2: GOLD}),
                mt([r"\text{Q after }", r"t_{\mathrm{pc}}"], {1: PINK}),
            ], COL_X[1], TOP_CAP)
            c.wait_until("r2")
            self.play(*appear(VGroup(w.lab_clk, w.lab_d, w.lab_q, w.guide, w.up, w.clk, w.d, w.q),
                              shift=None), run_time=1.2)
            c.wait_until("set-up time")
            self.play(FadeIn(w.band), FadeIn(w.su), FadeIn(w.hold), run_time=1.0)
            self.play(*appear(w.sym_su, w.sym_hold, lag=0.3), run_time=1.0)
            c.wait_until("output")
            self.play(FadeIn(w.pc), *appear(w.sym_pc), run_time=1.0)
            self.play(*appear(cap2, shift=None), run_time=1.0)  # early: the line sums up what was just said
            self.panels.append(VGroup(wd, cap2))

            # r3: the path, small
            P = path_diagram()
            for f in (P.ff0, P.ff1):
                f.remove(f.d_l, f.q_l, f.qb_l)
            P.remove(P.cl_l, P.q0_l, P.d1_l, P.d0_l, P.q1_l, P.clk_l, *P.names)
            fit(P, 3.4, 2.0, [COL_X[2] + 0.5, TOP_Y - 0.1, 0])
            names = VGroup(*[T(f"FF{i}", CAP).next_to(f.box, UP, buff=0.12) for i, f in enumerate((P.ff0, P.ff1))])
            cl = T("CL", CAP, BLUE).move_to(P.cl)
            clk = T("CLK", 28, YELLOW).next_to(P.clk_bus, LEFT, buff=0.1)
            cap3 = caption([T("FF0 launches, FF1 receives", 28)], COL_X[2] - 0.1, TOP_CAP)
            c.wait_until("r3")
            self.play(FadeIn(P), *appear(names, cl, clk, shift=None), run_time=1.2)
            c.wait_until("one flip-flop")
            self.play(*flash([P.ff0.box], color=GREEN), run_time=0.8)
            c.wait_until("next")
            self.play(*flash([P.ff1.box], color=BLUE), *appear(cap3), run_time=min(1.0, c.until(floor=0.5)))
            self.panels.append(VGroup(P, names, cl, clk, cap3))

    # -- c1.recap.2: r4 data sheet, r5 budget, r6 1 ns + grow --------------------------------------
    def clip2(self):
        with self.say("c1.recap.2", gap=1.5) as c:
            # r4: data-sheet conventions
            x = COL_X[0]
            ck = ds_clock_wave(x - 2.0, x + 2.0, BOT_Y + 0.5, [x - 1.1, x + 0.3, x + 1.6], h=0.6, slope=0.3)
            bs = bus(x - 2.0, x + 2.0, BOT_Y - 0.55, [(x - 0.85, x - 0.5)] + hatch(x + 0.35, x + 1.55, 3), h=0.6)
            cap4 = caption([T("data-sheet style", CAP)], x, BOT_CAP)
            c.wait_until("r4")
            self.play(Create(ck), FadeIn(bs), run_time=1.5)
            self.play(*appear(cap4), run_time=1.0)
            c.wait_until("sloped")
            self.play(FlashAround(VGroup(*ck.get_subcurve(0.18, 0.32).get_family()), color=YELLOW,
                                  time_width=1.5), run_time=1.0)
            c.wait_until("both values")
            self.play(FlashAround(bs.runs[0], color=BLUE, time_width=1.5), run_time=1.0)
            c.wait_until("crossings")
            self.play(FlashAround(bs.xs[0], color=BLUE, time_width=1.5),
                      FlashAround(VGroup(*bs.xs[1:]), color=BLUE, time_width=1.5), run_time=1.0)
            self.panels.append(VGroup(ck, bs, cap4))

            # r5: the budget bar, T_c >= t_pc + t_pd + t_su
            k = 3.3 / 7.0
            segs = [("t_{pc}", PINK, 1.2 * k), ("t_{pd}", PURPLE, 5.1 * k), ("t_{su}", GOLD, 0.7 * k)]
            b5 = bar6(segs, 7.0 * k, x0=COL_X[1] - 3.3 / 2 + 0.38, y=BOT_Y - 0.1, sym_size=34)
            ineq5 = colored_tex(["T_c", r"\ge", "t_{pc}", "+", "t_{pd}", "+", "t_{su}"],
                                {0: YELLOW, 2: PINK, 4: PURPLE, 6: GOLD}, 40)
            ineq5.move_to([COL_X[1], 0, 0]).align_to([0, BOT_CAP, 0], UP)
            c.wait_until("r5")
            self.play(FadeIn(b5.outline), *appear(b5.tc, shift=None), run_time=1.0)
            c.wait_until("clock-to-cue")
            self.play(FadeIn(b5.segs[0]), *appear(b5.syms[0]), run_time=0.8)
            c.wait_until("logic's delay")
            self.play(FadeIn(b5.segs[1]), *appear(b5.syms[1]), run_time=0.8)
            c.wait_until("set-up time")
            self.play(FadeIn(b5.segs[2]), *appear(b5.syms[2]), run_time=0.8)
            self.play(*appear(ineq5), run_time=min(1.0, c.until("r6", floor=0.5)))
            self.panels.append(VGroup(b5, ineq5))

            # r6: the 1 ns bar, padlocked ends, t_pd <= T_c - (t_pc + t_su)
            U = 2.2
            left = COL_X[2] - 2.0 + 1.55
            b6 = bar7(0.2, 0.7, 0.1, 1.0, unit=U, x0=left, y=BOT_Y - 0.1, tc_tex=r"T_c = 1\,\text{ns}",
                      syms=False, nums=[None, "0.7 ns", None], locks=True, lock_scale=0.85)
            b6.tc.scale(36 / 44, about_edge=RIGHT)   # panel size; the canonical bar's T_c label is 44
            ineq6 = colored_tex(["t_{pd}", r"\le", "T_c", "-", "(", "t_{pc}", "+", "t_{su}", ")"],
                                {0: PURPLE, 2: YELLOW, 5: PINK, 7: GOLD}, 40)
            ineq6.move_to([COL_X[2], 0, 0]).align_to([0, BOT_CAP, 0], UP)
            c.wait_until("r6")
            self.play(*[FadeIn(m) for m in (*b6.segs, b6.outline, *b6.locks)],
                      *appear(b6.tc, *b6.nums, shift=None), run_time=1.2)
            c.wait_until("logic gets")
            self.play(FlashAround(b6.segs[1], color=PURPLE, time_width=1.5), *appear(ineq6), run_time=1.2)

            # {grow}: the bar stretches to hold a longer PURPLE segment
            c.wait_until("can't fit")
            left2 = COL_X[2] - 2.0 + 0.55
            g6 = bar7(0.2, 1.2, 0.1, 1.5, unit=U, x0=left2, y=BOT_Y - 0.1, tc_tex=r"T_c\!\uparrow",
                      syms=False, locks=True, lock_scale=0.85)
            g6.tc.scale(36 / 44, about_edge=RIGHT)
            grows = MathTex(r"\text{or }", "T_c", r"\text{ grows}", font_size=34)
            grows[1].set_color(YELLOW)
            grows.next_to(ineq6, DOWN, buff=0.22)
            self.play(*during(disappear(*b6.nums), 0, 0.4),
                      *swap(b6.tc, g6.tc),
                      *[Transform(a, b) for a, b in zip(b6.segs, g6.segs)],
                      Transform(b6.outline, g6.outline),
                      *[a.animate.move_to(b) for a, b in zip(b6.locks, g6.locks)],
                      run_time=min(2.0, c.until("has to grow", floor=1.0)))
            c.wait_until("has to grow")
            self.play(*appear(grows), run_time=min(1.0, c.until(floor=0.5)))
            self.panels.append(VGroup(*b6.segs, b6.outline, *b6.locks, g6.tc, ineq6, grows))

    # -- c1.recap.3: next time, the race into FF1's window ----------------------------------------
    def clip3(self):
        P = path_diagram().scale(0.8).move_to([0, 1.1, 0])
        P.cl_l.scale(1.15)
        x0 = P.ff0.q_w.get_start()
        cl = P.cl
        ydip = cl.get_center()[1] - 0.47
        end = P.ff1.d_w.get_center()
        route = VMobject().set_points_as_corners([
            x0, cl.get_left(), [cl.get_left()[0] + 0.35, ydip, 0], [cl.get_right()[0] - 0.35, ydip, 0],
            cl.get_right(), end])
        band = (Rectangle(width=P.ff1.d_w.width, height=0.36).set_stroke(width=0)
                .set_fill(GOLD, 0.35).set_z_index(-3).move_to(P.ff1.d_w).shift(0.08 * RIGHT))
        dot = Dot(x0, radius=0.13, color=BLUE).set_z_index(5)
        # D_1 above-left of the window, clear of the wire the dot rides in on
        P.d1_l.next_to(band, UP, buff=0.0).align_to(band, DOWN).shift(0.26 * UP)
        P.d1_l.set_x(band.get_left()[0] - 0.12 - P.d1_l.width / 2)
        q = T("?", 110, YELLOW).move_to([0, -1.55, 0])
        part2 = T("Part 2 · Hold time", 48).move_to([0, -2.85, 0])
        with self.say("c1.recap.3") as c:
            # {next}: the panels shrink away, the path returns
            self.play(*during([FadeOut(p, scale=0.5) for p in self.panels], 0, 0.5),
                      *during([FadeIn(P)], 0.5, 1), run_time=1.6)
            # one rising edge: FF1's window opens; a new value leaves FF0
            c.wait_until("new data")
            self.play(*[VShowPassingFlash(p, time_width=0.6) for p in P.clk_paths()],
                      FadeIn(band), FadeIn(dot, scale=0.5), run_time=1.0)
            self.play(MoveAlongPath(dot, route), run_time=max(1.0, c.until("race")), rate_func=smooth)
            # {race}: it lands inside the window
            def pulse(m, a):
                m.set_fill(interpolate_color(ManimColor(GOLD), ManimColor(RED), min(1, 2 * a)),
                           0.35 + 0.5 * np.sin(PI * a) + 0.15 * a)
            self.play(UpdateFromAlphaFunc(band, pulse), run_time=1.2)
            self.play(*appear(q), run_time=1.0)  # early: the teaser's end card
            self.play(*appear(part2), run_time=1.0)  # early: the teaser's end card
        self.wait(8.0)   # end card; the music carries it
