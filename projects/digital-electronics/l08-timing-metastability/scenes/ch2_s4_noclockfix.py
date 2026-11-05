"""Chapter 2, scene 4: why the clock can't save you, and the real fix. Clips c2.noclock.1 – c2.noclock.4.

Copied (not imported): s3's two-box end shot (make_ff / build_chain / pair transform), s1's window
style, s2's hold_diagram (here with a `lab` label boost) and ch1_s4's path_diagram.

Last shot (opens s5): routes_path(): path_diagram() scaled PS = 0.66 about ORIGIN, shifted PY UP,
every text label then scaled LB = 1.3 in place; the CL box replaced by routes(P): BLUE long route
(upper rail, three BLUE gate boxes 0.46 x 0.4) now GREEN; YELLOW short route (lower rail, one gate)
with two plain FG buffer triangles; junction dots at x = +-XJ on the pin row. The path's CLK label
sits right of the CLK bus's right end (next_to(bus end, RIGHT, 0.2)). The diagram:
hold_diagram(0.4, k=DK, shift=(DX, DY), lab=LAB) with the GOLD band, GREEN ticks on D1's row
in the band and between the t_su guide and the second edge.
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
# s3's two-box end shot (copied from ch2_s3_shiftreg.py)
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def make_ff3():
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    g = VGroup(d_w, q_w, box, tri, d_l, q_l)
    g.box, g.tri, g.d_w, g.q_w, g.d_l, g.q_l, g.clk_w = box, tri, d_w, q_w, d_l, q_l, clk_w
    return g


S3_K = 0.6
S3_FF_X = (-3.6, -0.2)
S3_FF_Y = 1.15
S3_HX = (BOX_W / 2 + WIRE) * S3_K
PAIR_S = 1.4
PAIR_A = _p((S3_FF_X[0] + S3_FF_X[1]) / 2, S3_FF_Y)
PAIR_B = _p(0, 1.05)
RULE_Y = -1.95
REL_Y = -3.0
COLS = {"t_{pc}": PINK, "t_{pd}": PURPLE, "t_{hold}": GOLD}


def pair_shot():
    """s3's last frame: FF0 + FF1, the bare Q_0 wire, the CLK bus (all pieces separate)."""
    ffs = []
    for x in S3_FF_X:
        f = make_ff3()
        f.scale(S3_K, about_point=ORIGIN).shift(_p(x, S3_FF_Y))
        f.clk_w.scale(S3_K, about_point=ORIGIN).shift(_p(x, S3_FF_Y))
        for lb in (f.d_l, f.q_l):
            lb.scale(1.3, about_point=lb.get_center())
        ffs.append(f)
    qy = S3_FF_Y + PIN_Y * S3_K
    link = Line(_p(S3_FF_X[0] + S3_HX, qy), _p(S3_FF_X[1] - S3_HX, qy)).set_stroke(GREEN, 5)
    names = [T(f"FF{i}", 32).next_to(f.box, UP, buff=0.15) for i, f in enumerate(ffs)]
    by = S3_FF_Y - (BOX_H / 2 + EN_WIRE) * S3_K
    bus = Line(_p(S3_FF_X[0] - 1.2, by), _p(S3_FF_X[1], by)).set_stroke(YELLOW, 5)
    jdot = Dot(_p(S3_FF_X[0], by), radius=0.07, color=YELLOW)
    clk_l = T("CLK", 32, YELLOW).next_to(bus.get_start(), LEFT, buff=0.15)
    parts = [ffs[0], ffs[1], names[0], names[1], link, ffs[0].clk_w, ffs[1].clk_w, bus, jdot, clk_l]
    for m in parts:
        m.scale(PAIR_S, about_point=PAIR_A).shift(PAIR_B - PAIR_A)
    pin_y = (qy - PAIR_A[1]) * PAIR_S + PAIR_B[1]
    q0 = MathTex("Q_0", font_size=40, color=GREEN).scale(1.15).move_to(_p(-1.3, pin_y + 0.42))
    parts.append(q0)
    return parts


# =============================================================================================
# s2's data-sheet diagram (copied from ch2_s2_hold.py; `lab` boosts the label sizes)
# =============================================================================================
WAVE_W = 4
ROW_H = 0.8
SLOPE = 0.35
GUIDE_W = 1.5
DIM_W = 3


def clock_wave(x0, x1, y, edges, h=ROW_H, slope=SLOPE, color=YELLOW, start_low=True):
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


def guide(x, y_top, y_bot):
    return Line([x, y_top, 0], [x, y_bot, 0]).set_stroke(DIM, GUIDE_W)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=44):
    arr = DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.15)
    return VGroup(arr, lab)


YC, YQ, YD = 2.1, 0.4, -1.3
X0, X1 = -4.6, 6.3
E1, FALL, E2 = -2.8, 0.7, 4.2
PERIOD = E2 - E1
XQ = -1.6
HATCH_END = 2.7
XSU = 3.5
LAB_X = -5.9
Y_A = -2.4
HOLD_END = 0.3

# this scene's placement of the diagram
DK = 0.6
DX, DY = 0.0, -1.71
LAB = 1.3
OFF = 0.2                 # c2.noclock.3 only: the diagram sits OFF higher (keeps t_pd / t_su labels in margin)


def ux(u):
    return E1 + u * PERIOD


def M(x, y, off=0.0):
    return np.array([DK * x + DX, DK * y + DY + off, 0])


def _place(*ms, off=0.0):
    for m in ms:
        m.scale(DK, about_point=ORIGIN).shift([DX, DY + off, 0])
    return ms


def d1_at(h, off=0.0):
    """D1's bus with its hatched stretch starting at fraction h of the period, placed."""
    b = bus(X0, HATCH_END, YD, hatch(ux(h), HATCH_END, 4), color=BLUE)
    _place(b, off=off)
    return b


def hold_diagram(hatch0=0.4, k=DK, shift=(DX, DY), lab=LAB):
    xh = ux(hatch0)
    clk_l = clock_wave(X0, HATCH_END, YC, [E1, FALL], color=YELLOW)
    clk_r = clock_wave(HATCH_END, X1, YC, [E2], color=YELLOW)
    clk_lab = T("CLK", 40 * lab, YELLOW).move_to([LAB_X, YC, 0])
    g1, g2 = guide(E1, 3.25, -2.6), guide(E2, 3.25, -2.6)
    tc = dim_arrow(E1, E2, 3.05, YELLOW, "T_c", size=44 * lab)
    q0 = bus(X0, HATCH_END, YQ, [(XQ - 0.2, XQ + 0.2)], color=GREEN)
    q0_r = bus(HATCH_END, X1, YQ, [], color=GREEN)
    q0_lab = MathTex("Q_0", font_size=48 * lab, color=GREEN).move_to([LAB_X, YQ, 0])
    gq = guide(XQ, YQ + 0.6, -2.6)
    tpc = dim_arrow(E1, XQ, Y_A, PINK, "t_{pc}", label_dir=DOWN, size=44 * lab)
    d1 = bus(X0, HATCH_END, YD, hatch(xh, HATCH_END, 4), color=BLUE)
    d1_r = bus(HATCH_END, X1, YD, [(3.1, XSU)], color=BLUE)
    d1_lab = MathTex("D_1", font_size=48 * lab, color=BLUE).move_to([LAB_X, YD, 0])
    gsu = guide(XSU, YD + 0.4, -2.6)
    tpd = dim_arrow(XQ, XSU, Y_A, PURPLE, "t_{pd}", label_dir=DOWN, size=44 * lab)
    tsu = dim_arrow(XSU, E2, Y_A, GOLD, "t_{su}", label_dir=DOWN, size=44 * lab)

    dg = VGroup(g1, g2, gq, gsu, clk_l, clk_r, q0, q0_r, d1, d1_r,
                clk_lab, q0_lab, d1_lab, tc, tpc, tpd, tsu)
    band = Rectangle(width=ux(HOLD_END) - E1, height=ROW_H + 0.16)
    band.set_stroke(GOLD, 2).set_fill(GOLD, 0.22).move_to([(E1 + ux(HOLD_END)) / 2, YD, 0])
    band.set_z_index(-1)
    for m in (dg, band):
        m.scale(k, about_point=ORIGIN).shift([shift[0], shift[1], 0])
    for name, m in dict(g1=g1, g2=g2, gq=gq, gsu=gsu, clk=clk_l, clk_r=clk_r, q0=q0, q0_r=q0_r,
                        d1=d1, d1_r=d1_r, clk_lab=clk_lab, q0_lab=q0_lab, d1_lab=d1_lab,
                        tc=tc, tpc=tpc, tpd=tpd, tsu=tsu).items():
        setattr(dg, name, m)
    dg.band = band
    return dg


def right_parts(e2, off=0.0):
    """The pieces that move with the second rising edge (at unscaled x = e2), placed."""
    d = e2 - E2
    x1, xsu = X1 + d, XSU + d
    parts = dict(
        clk_r=clock_wave(HATCH_END, x1, YC, [e2], color=YELLOW),
        q0_r=bus(HATCH_END, x1, YQ, [], color=GREEN),
        d1_r=bus(HATCH_END, x1, YD, [(3.1, XSU)], color=BLUE),
        g2=guide(e2, 3.25, -2.6),
        gsu=guide(xsu, YD + 0.4, -2.6),
        tc=dim_arrow(E1, e2, 3.05, YELLOW, "T_c", size=44 * LAB),
        tsu=dim_arrow(xsu, e2, Y_A, GOLD, "t_{su}", label_dir=DOWN, size=44 * LAB),
    )
    _place(*parts.values(), off=off)
    return parts


def slack_rect(e2, off=OFF):
    """GREEN gap on D1's row: from D1's last change (XSU) to the moved deadline."""
    w = max(e2 - E2, 0.02)
    r = Rectangle(width=DK * w, height=DK * (ROW_H + 0.16)).set_stroke(GREEN, 2).set_fill(GREEN, 0.3)
    r.move_to(M(XSU + w / 2, YD, off)).set_z_index(-1)
    return r


# =============================================================================================
# ch1's path (copied from ch1_s4_path.py)
# =============================================================================================
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
    g.box, g.tri, g.bub = box, tri, None
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


P_FF_X = (-4.2, 4.2)
P_FF_Y = 0.5
P_PIN = P_FF_Y + PIN_Y
P_BUS = P_FF_Y - BOX_H / 2 - EN_WIRE
P_BUS_X0 = -5.6
P_CL_W, P_CL_H = 3.0, 1.6


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
    return P


PS, PY, LB = 0.66, 1.9, 1.3
XJ = 1.25                 # route junctions (frame x = -XJ, +XJ)
RAIL = 0.55               # rails above / below the pin row


def routes_path():
    """path_diagram() across the top of the frame, labels boosted to stay readable."""
    P = path_diagram()
    P.scale(PS, about_point=ORIGIN).shift(PY * UP)
    for m in [*P.names, P.q0_l, P.d1_l, P.d0_l, P.q1_l, P.clk_l, P.cl_l,
              P.ff0.d_l, P.ff0.q_l, P.ff0.qb_l, P.ff1.d_l, P.ff1.q_l, P.ff1.qb_l]:
        m.scale(LB)
    P.clk_l.next_to(P.clk_bus.get_end(), RIGHT, buff=0.2)      # as ch2_s3: clear of the diagram's CLK row
    P.pin = P.q0_w.get_start()[1]
    return P


def routes(pin):
    R = VGroup()
    up, lo = pin + RAIL, pin - RAIL
    R.long = VMobject().set_points_as_corners([_p(-XJ, pin), _p(-XJ, up), _p(XJ, up), _p(XJ, pin)])
    R.short = VMobject().set_points_as_corners([_p(-XJ, pin), _p(-XJ, lo), _p(XJ, lo), _p(XJ, pin)])
    for w in (R.long, R.short):
        w.set_stroke(BLUE, 4)

    def gate(x, y):
        return Rectangle(width=0.42, height=0.4).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(_p(x, y)).set_z_index(1)
    R.gates_long = [gate(x, up) for x in (-0.68, 0.0, 0.68)]
    R.gate_short = gate(-0.68, lo)
    R.dots = [Dot(_p(x, pin), radius=0.07, color=BLUE) for x in (-XJ, XJ)]
    R.bufs = []
    for x in (0.02, 0.66):
        b = Polygon(_p(x - 0.2, lo - 0.21), _p(x - 0.2, lo + 0.21), _p(x + 0.22, lo))
        R.bufs.append(b.set_stroke(FG, 3).set_fill(BG, 1).set_z_index(1))
    R.lo = lo
    R.add(R.long, R.short, *R.gates_long, R.gate_short, *R.dots)
    return R


# =============================================================================================
# s1's window (split at the edge), floated over FF1's D input as s1 places it on the path
# =============================================================================================
WW, WH = 3.0, 0.5


def window(wx, wy):
    W = VGroup()
    W.left = (Rectangle(width=WW / 2, height=WH).set_stroke(width=0).set_fill(GOLD, 0.1)
              .move_to(_p(wx - WW / 4, wy)))
    W.right = (Rectangle(width=WW / 2, height=WH).set_stroke(width=0).set_fill(GOLD, 0.5)
               .move_to(_p(wx + WW / 4, wy)))
    W.edge = Line(_p(wx, wy - WH / 2 - 0.12), _p(wx, wy + WH / 2 + 0.12)).set_stroke(YELLOW, 4)
    W.l_lab = T("set-up", 36, GOLD).set_opacity(0.4).move_to(_p(wx - WW / 4, wy + 0.6))
    W.r_lab = T("hold", 36, GOLD).move_to(_p(wx + WW / 4, wy + 0.6))
    W.r_lab.align_to(W.l_lab, DOWN)
    return W


class NoClockFix(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ---- c2.noclock.1: hold time zero ----------------------------------------------------------------
    def clip1(self):
        pair = pair_shot()
        rule = MathTex(r"(t_{pc})_{\min} \geq t_{hold}", font_size=56,
                       tex_to_color_map=COLS).move_to(_p(0, RULE_Y))
        rel = VGroup(T("a reliable flip-flop:", 36),
                     MathTex(r"t_{hold}", font_size=44, color=GOLD),
                     T("shorter than its own", 36),
                     MathTex(r"(t_{pc})_{\min}", font_size=44, tex_to_color_map={"t_{pc}": PINK}))
        rel.arrange(RIGHT, buff=0.2).move_to(_p(0, REL_Y))
        # one centred column: window over FF1's D input, the pair, the rule, the tag
        PK, PC = 0.65, _p(0, 0.3)
        ctr = VGroup(*pair).get_center()
        for m in pair:
            m.generate_target()
            m.target.scale(PK, about_point=ctr).shift(PC - ctr)
        for lb in (pair[2].target, pair[3].target, pair[9].target):   # FF0 / FF1 / CLK stay >= 30
            lb.scale(1.1)
        for f in pair[:2]:
            for lb in (f.target[4], f.target[5]):                      # D / Q stay >= 30
                lb.scale(1.18)
        rk = 48 / 56
        rule.generate_target()
        rule.target.scale(rk).move_to(_p(0, -1.7))
        d_in = pair[1].target[0]                                       # FF1's D wire
        wx = d_in.get_center()[0]
        W = window(wx, pair[3].target.get_top()[1] + 0.55)
        lead = DashedLine(_p(wx, W.edge.get_bottom()[1] - 0.05), _p(wx, d_in.get_y() + 0.08),
                          dash_length=0.08).set_stroke(DIM, 2)
        with self.say("c2.noclock.1") as c:
            self.play(*appear(*pair, rule, rel, shift=None, lag=0.0), run_time=0.8)  # early: s3's last shot returns
            c.wait_until("though not all")
            self.play(*during(disappear(rel), 0, 0.4),  # early: FF1's window, drawn whole, then walked
                      *[MoveToTarget(m) for m in pair], MoveToTarget(rule),
                      *during(appear(lead, W.left, W.right, W.edge, W.l_lab, W.r_lab,
                                     shift=None, lag=0.1), 0.5, 1.0),
                      run_time=2.0)
            # {zero}: t_hold -> 0
            rule0 = MathTex(r"(t_{pc})_{\min} \geq 0", font_size=56,
                            tex_to_color_map={"t_{pc}": PINK, "0": GOLD})
            rule0.scale(rk).move_to(rule, aligned_edge=LEFT)
            c.wait_until("of zero")
            self.play(*edit(rule, rule0), run_time=min(1.4, c.until("free")))
            # {free}: the hold half collapses onto the edge
            c.wait_until("free")
            thin = W.right.copy().stretch(0.02, 0, about_edge=LEFT)
            free = T("free to change", 36, GREEN).move_to(W.r_lab, aligned_edge=LEFT).align_to(W.r_lab, DOWN)
            free.shift((wx + 0.2 - free.get_left()[0]) * RIGHT)
            self.play(*during([Transform(W.right, thin)], 0, 0.6), *during(disappear(W.r_lab), 0, 0.4),
                      *during(appear(free), 0.55, 1.0), run_time=2.2)
            # {always}: tick + tag
            tag = VGroup(MathTex(r"t_{pc} > 0", font_size=48, tex_to_color_map={"t_{pc}": PINK}),
                         T(", always", 40, GREEN))
            tag.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
            tag.next_to(rule0, DOWN, buff=0.55)
            c.wait_until("always")
            self.play(*appear(tag), run_time=1.0)
            tick = check_mark(GREEN).scale(1.2).next_to(rule0, RIGHT, buff=0.35)
            c.wait_until("greater")
            self.play(GrowFromCenter(tick), FlashAround(rule0, color=GREEN), run_time=1.2)

    # ---- c2.noclock.2: the two constraints ----------------------------------------------------------
    def clip2(self):
        l1 = MathTex("T_c", r"\geq", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", font_size=56)
        l2 = MathTex("(", "t_{pc}", "+", "t_{pd}", ")", r"_{\min}", r"\geq", "t_{hold}", font_size=56)
        for m, cols in ((l1, {2: PINK, 4: PURPLE, 6: GOLD}), (l2, {1: PINK, 3: PURPLE, 7: GOLD})):
            for i, col in cols.items():
                m[i].set_color(col)
        l1.move_to(_p(0.6, 0.7))
        l2.move_to(_p(0.6, -0.55))
        l2.shift((l1[1].get_x() - l2[6].get_x()) * RIGHT)
        left = min(l1.get_left()[0], l2.get_left()[0])
        lab1 = T("set-up", 36, GOLD)
        lab2 = T("hold", 36, GOLD)
        for lab, ln in ((lab1, l1), (lab2, l2)):
            lab.move_to(_p(left - 0.4, ln[1].get_y() if ln is l1 else ln[6].get_y()), aligned_edge=RIGHT)
        self.ineq = [lab1, l1, lab2, l2]
        with self.say("c2.noclock.2") as c:
            sweep_clear(self, *appear(lab1, l1, lab2, l2, shift=None, lag=0.3), run_time=1.8)  # early: the two constraints, side by side
            c.wait_until("setup")
            self.play(*recolor(l1[0], YELLOW), FlashAround(l1[0], color=YELLOW, time_width=1.5), run_time=1.5)
            # {hold}: a highlight sweeps the hold line and finds no T_c
            c.wait_until("hold")
            h = l2.height + 0.3
            box = Rectangle(width=0.42, height=h).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.2)
            box.move_to(l2, aligned_edge=LEFT).shift(0.15 * LEFT).set_z_index(-1)
            full = Rectangle(width=l2.width + 0.3, height=h).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.2)
            full.move_to(l2).set_z_index(-1)
            self.play(FadeIn(box), run_time=0.4)
            self.play(Transform(box, full), run_time=1.8, rate_func=linear)   # one sweep, left edge fixed
            no = VGroup(T("no", 36, YELLOW), MathTex("T_c", font_size=48, color=YELLOW))
            no.arrange(RIGHT, buff=0.15, aligned_edge=DOWN).next_to(l2, RIGHT, buff=0.7)
            self.play(FadeOut(box), *appear(no), run_time=1.0)
            self.no = no
            c.wait_until("every term")
            self.play(*flash([l2[1], l2[3], l2[7]], color=YELLOW), run_time=1.4)

    # ---- c2.noclock.3: slowing the clock does nothing for hold ---------------------------------------
    def clip3(self):
        lab1, l1, lab2, l2 = self.ineq
        no = self.no
        top = [lab1, l1, lab2, l2, no]
        grp = VGroup(*top)
        s = 44 / 56
        tgt = grp.copy().scale(s)
        tgt.move_to(_p(0, 3.55 - tgt.height / 2))
        ctr, d = grp.get_center(), tgt.get_center() - grp.get_center()
        dg = hold_diagram(0.2, shift=(DX, DY + OFF))
        self.dg = dg
        ov = Rectangle(width=DK * (ux(HOLD_END) - ux(0.2)), height=DK * (ROW_H + 0.16))
        ov.set_stroke(RED, 3).set_fill(RED, 0.45).move_to(M((ux(0.2) + ux(HOLD_END)) / 2, YD, OFF))
        self.ov = ov
        with self.say("c2.noclock.3") as c:
            self.play(*[m.animate.scale(s, about_point=ctr).shift(d) for m in top],
                      *during([FadeIn(dg), FadeIn(dg.band)], 0.55, 1.0), run_time=2.0)
            c.wait_until("violation")
            self.play(FadeIn(ov), FlashAround(ov, color=RED, time_width=1.5), run_time=1.2)

            # {later}: the second edge slides right; set-up gets room
            c.wait_until("later")
            gap = slack_rect(1.0)
            self.slack = gap
            self.slide(E2 + 1.0, during([GrowFromEdge(gap, LEFT)], 0.3, 1.0), run_time=2.0)
            c.wait_until("more room")
            self.play(FlashAround(gap, color=GREEN, time_width=1.5), run_time=1.2)

            # {stuck}: the first edge, the band and the overlap stay put
            c.wait_until("stuck")
            self.play(FlashAround(dg.band, color=RED, time_width=1.5), FlashAround(ov, color=RED, time_width=1.5),
                      VShowPassingFlash(dg.g1.copy().set_stroke(RED, 5), time_width=0.6), run_time=1.6)
            pin_l = Line(M(E1, 3.45, OFF), M(E1, -2.6, OFF)).set_stroke(YELLOW, 2.5)
            pin_d = Dot(M(E1, 3.45, OFF), radius=0.08, color=YELLOW)
            meas = T("measured from this edge", 32, YELLOW).next_to(pin_d, UP, buff=0.2)
            c.wait_until("pinned")
            self.play(Create(pin_l), FadeIn(pin_d), run_time=1.0)
            self.play(*appear(meas), run_time=1.0)
            self.pin = [pin_l, pin_d, meas]

            # {any}: further right, twice; the overlap never moves
            c.wait_until("any")
            fails = VGroup(T("fails at any", 32, RED), MathTex("T_c", font_size=44, color=RED))
            fails.arrange(RIGHT, buff=0.15, aligned_edge=DOWN).move_to(_p(3.2, meas.get_y()))
            self.play(*appear(fails), run_time=1.0)  # early: the tag lands with the sentence
            self.fails = fails
            self.slide(E2 + 2.0, [Transform(gap, slack_rect(2.0)), FlashAround(ov, color=RED)], run_time=1.3)
            self.slide(E2 + 2.8, [Transform(gap, slack_rect(2.8)), FlashAround(ov, color=RED)],
                       run_time=min(1.3, c.until(floor=0.6)))

    def slide(self, e2, extra=(), run_time=1.5):
        dg = self.dg
        new = right_parts(e2, OFF)
        self.play(*[Transform(getattr(dg, k), v) for k, v in new.items()], *extra, run_time=run_time)

    # ---- c2.noclock.4: the real fix -----------------------------------------------------------------
    def clip4(self):
        dg, ov, gap = self.dg, self.ov, self.slack
        cap = VGroup(*[T(s, 28, FG, slant=ITALIC, disable_ligatures=True) for s in (
            "Note that hold time violations cannot be overcome",
            "by adjusting the clock period. Consequently, they can be",
            "hard to fix and have to be taken seriously")]).arrange(DOWN, buff=0.12)
        cap.move_to(_p(0, 1.3))
        P = routes_path()
        R = routes(P.pin)
        with self.say("c2.noclock.4") as c:
            # the T_c arrow and label sit under the caption: hidden while it is up (restored at {fix})
            self.play(*during(disappear(*self.pin, self.fails) + [restyle(dg.tc, 0)], 0, 0.45),
                      *during(appear(cap, shift=None), 0.5, 1.0), run_time=1.6)
            c.wait_until("taken seriously")
            ts = select(cap[2], "taken seriously")[0]
            self.play(*recolor(ts, YELLOW), FlashAround(ts, color=YELLOW, time_width=1.5, buff=0.06), run_time=1.4)

            # {fix}: clear the words, the edge comes back, the path returns across the top
            c.wait_until("fix")
            new = right_parts(E2)
            still = [getattr(dg, k) for k in ("g1", "gq", "clk", "q0", "d1", "clk_lab", "q0_lab", "d1_lab",
                                              "tpc", "tpd")] + [dg.band, ov]
            self.play(*during(disappear(*self.ineq, self.no, cap), 0, 0.4),  # early: ch1's path returns whole
                      *during([Transform(getattr(dg, k), v) for k, v in new.items()] + [FadeOut(gap)]
                              + [m.animate.shift(OFF * DOWN) for m in still], 0.2, 0.75),
                      *during(appear(*P.all, shift=None, lag=0.02), 0.5, 1.0),  # early: ch1's path returns whole
                      run_time=2.2)
            settle(self, P)

            # {routes}: the CL box opens into two routes
            c.wait_until("routes")
            q0_t = Line(P.q0_w.get_start(), _p(-XJ, P.pin)).set_stroke(GREEN, 5)
            d1_t = Line(_p(XJ, P.pin), P.d1_w.get_end()).set_stroke(BLUE, 5)
            self.play(*during(disappear(P.cl_l), 0, 0.3),
                      *during([FadeOut(P.cl), Transform(P.q0_w, q0_t), Transform(P.d1_w, d1_t)], 0.15, 0.6),
                      *during([Create(R.long), Create(R.short)], 0.4, 1.0),
                      *during(appear(*R.gates_long, R.gate_short, *R.dots, shift=None, lag=0.1), 0.55, 1.0),
                      run_time=2.0)
            P.remove(P.cl, P.cl_l)
            c.wait_until("shortest")
            self.play(R.short.animate.set_stroke(YELLOW, 6), R.gate_short.animate.set_stroke(YELLOW),
                      VShowPassingFlash(R.short.copy().set_stroke(YELLOW, 10), time_width=0.5), run_time=1.4)
            fast = T("fastest way through", 30, YELLOW).move_to(_p(0, R.lo - 0.5))
            self.play(*appear(fast), run_time=1.0)

            # {buffers}: two buffers slide into the short route
            c.wait_until("buffers")
            self.play(VShowPassingFlash(R.short.copy().set_stroke(YELLOW, 10), time_width=0.5), run_time=1.2)
            c.wait_until("usually with buffers")
            self.play(*appear(*R.bufs, shift=0.35 * DOWN, lag=0.3), run_time=1.5)
            c.wait_until("a little later")
            self.play(*flash(R.bufs, color=YELLOW), run_time=1.2)

            # {moved}: D1's first change slides out of the hold window
            c.wait_until("moved")
            tick1 = check_mark(GREEN).move_to(dg.band)

            def hatch_slide(m, a):          # hatch start 0.2 -> 0.4; band and hatch end stay put
                m.become(d1_at(0.2 + 0.2 * a))

            def overlap(m, a):              # RED = hatch start .. band end, gone once out of the band
                h = 0.2 + 0.2 * a
                w = max(ux(HOLD_END) - ux(h), 0.002)
                op = min(1.0, w / (ux(HOLD_END) - ux(0.2)))
                r = Rectangle(width=DK * w, height=DK * (ROW_H + 0.16)).set_stroke(RED, 3, opacity=op)
                r.set_fill(RED, 0.45 * op).move_to(M(ux(HOLD_END) - w / 2, YD))
                m.become(r)
            self.play(UpdateFromAlphaFunc(dg.d1, hatch_slide), UpdateFromAlphaFunc(ov, overlap),
                      *during([FadeIn(tick1, scale=0.6)], 0.7, 1.0), run_time=2.2)
            self.remove(ov)

            # {slowest}: the long route is untouched; set-up still met
            c.wait_until("slowest")
            self.play(R.long.animate.set_stroke(GREEN, 6), *[g.animate.set_stroke(GREEN) for g in R.gates_long],
                      VShowPassingFlash(R.long.copy().set_stroke(GREEN, 10), time_width=0.5), run_time=1.3)
            tick2 = check_mark(GREEN).move_to(M((XSU + E2) / 2, YD))
            self.play(FlashAround(dg.d1_r.xs[0], color=GREEN), GrowFromCenter(tick2),
                      run_time=min(1.2, c.until(floor=0.6)))
