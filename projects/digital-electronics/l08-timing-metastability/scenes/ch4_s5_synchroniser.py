"""Chapter 4, scene 5: one more flip-flop: the two-stage synchroniser. Clips c4.sync.1 – c4.sync.4.

Shots: s4's decay curve (decay_graph(), full size) shrinks to the upper-left corner; RED problem
line, "-> minimise its probability:", YELLOW "a synchroniser (cascaded flip-flops)" -> board
clears; sync_circuit() across the top half (s1's push-button on D0 BLUE, FF0, TEAL D1 wire, FF1,
GREEN Q, one YELLOW CLK bus below); ch2 s3's shift-register ghost below it shrinks to two stages
lined up under FF0/FF1, tag on top -> sync_timing() under the circuit (data-sheet style): CLK,
D1, Q; a fingertip presses the button; at the first edge D1 converges to a RED midline (circuit
wire RED), T_c, D1 resolves to TEAL before the next edge -> t_res / t_su / t_pc on one baseline,
GREEN tick by FF1, Q crosses, the slide's line at the bottom -> "old value" / "new value" tags with
ticks; FF0 outline RED "takes the risk", FF1 GREEN "sees a settled input". s6 keeps both helpers.
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
# decay_graph(): the metastability decay curve (s4 copies it at full size)
# =============================================================================================
def decay_graph(width=8.0, height=4.2):
    """FG axes, x "t" with ticks tau..5tau, y "P(t_res > t)", RED curve falling from T_0/T_c.
    Built centred on ORIGIN. Parts: .ax .curve .labels"""
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
    g.labels = VGroup(tlabels, ylab0, xl, yl)
    g.move_to(ORIGIN)
    return g
# =============================================================================================


# =============================================================================================
# push_button() + make_ff(): copied from ch4_s1_hook.py (Q-bar dropped here: the synchroniser
# uses Q only, as the slide does)
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
PUSH = 0.18


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


def push_button(center=ORIGIN):
    stem = Line(_p(-0.3, 0), _p(-0.58, 0)).set_stroke(FG, 5)
    cap = RoundedRectangle(corner_radius=0.06, width=0.16, height=0.62).set_stroke(FG, 4).set_fill(DIM, 1)
    cap.move_to(_p(-0.66, 0))
    body = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.84).set_stroke(FG, 4).set_fill(BG, 1)
    g = VGroup(stem, cap, body)
    g.stem, g.cap, g.body = stem, cap, body
    g.shift(center)
    g.out = lambda: body.get_right()
    return g


def fingertip():
    f = RoundedRectangle(corner_radius=0.21, width=1.4, height=0.44).set_stroke(FG, 3).set_fill(BG, 1)
    f.move_to(_p(-0.7, 0))
    nail = RoundedRectangle(corner_radius=0.07, width=0.34, height=0.17).set_stroke(FG, 2)
    nail.move_to(_p(-0.27, 0.07))
    return VGroup(f, nail)
# =============================================================================================


# =============================================================================================
# sync_circuit(): the two-flip-flop synchroniser (slide p. 112), top half. s6 / recap copy it.
# =============================================================================================
SK = 0.62                    # flip-flop scale
SFF_X = (-1.7, 2.1)          # FF0, FF1 centres
SFF_Y = 2.244                # box centre (top 3.05)
SBTN_X = -4.3                # button housing centre
SHX = (BOX_W / 2 + WIRE) * SK


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
# =============================================================================================


# =============================================================================================
# sync_timing(): slide p. 112's timing diagram in ch1_s5's data-sheet style. s6 / recap copy it.
# =============================================================================================
WAVE_W = 4
ROW_H = 0.5
SLOPE = 0.35
GUIDE_W = 1.5
DIM_W = 3
TX0, TX1 = -4.7, 4.2             # traces end at 4.2: the old/new tags get the lane to their right
E1, E2 = -2.4, 2.6               # the two rising edges (one period apart)
CLK_EDGES = [E1, 0.1, E2]
XS = 1.6                         # D1 resolved (the split)
QX = (3.3, 3.6)                  # Q's crossover, t_pc after E2
TROW = {"CLK": 0.0, "D1": -0.95, "Q": -1.95}
DIM_Y = -2.5
TC_Y = 0.4                       # T_c sits on the CLK trace, 0.42 clear of the circuit's bus
LAB_X = -5.45


def clock_wave(x0, x1, y, edges, h=ROW_H, slope=SLOPE, color=YELLOW):
    lo, hi = y - h / 2, y + h / 2
    level = lo
    pts = [_p(x0, level)]
    for xc in edges:
        other = hi if level == lo else lo
        pts += [_p(xc - slope / 2, level), _p(xc + slope / 2, other)]
        level = other
    pts.append(_p(x1, level))
    return VMobject().set_points_as_corners(pts).set_stroke(color, WAVE_W)


def pair(xa, xb, y, color, h=ROW_H):
    return VGroup(Line(_p(xa, y + h / 2), _p(xb, y + h / 2)),
                  Line(_p(xa, y - h / 2), _p(xb, y - h / 2))).set_stroke(color, WAVE_W)


def guide(x, y_top, y_bot):
    return Line(_p(x, y_top), _p(x, y_bot)).set_stroke(DIM, GUIDE_W)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=40):
    arr = DoubleArrow(_p(xa, y), _p(xb, y), buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.12)
    g = VGroup(arr, lab)
    g.arr, g.lab = arr, lab
    return g


def sync_timing():
    D = VGroup()
    yc, yd, yq = TROW["CLK"], TROW["D1"], TROW["Q"]
    h2 = ROW_H / 2
    D.clk = clock_wave(TX0, TX1, yc, CLK_EDGES)
    D.labs = [T("CLK", 32, YELLOW).move_to(_p(LAB_X, yc)),
              MathTex("D_1", font_size=40, color=TEAL).move_to(_p(LAB_X, yd)),
              MathTex("Q", font_size=40, color=GREEN).move_to(_p(LAB_X, yq))]
    # D1: 0 or 1 -> converges (RED) at E1 -> RED midline -> diverges -> resolved TEAL pair
    D.d1_pre = pair(TX0, E1, yd, TEAL)
    c1 = E1 + 0.3
    D.d1_conv = VGroup(Line(_p(E1, yd + h2), _p(c1, yd)), Line(_p(E1, yd - h2), _p(c1, yd))).set_stroke(RED, WAVE_W)
    D.mid_x = -0.4
    D.d1_red1 = Line(_p(c1, yd), _p(D.mid_x, yd)).set_stroke(RED, WAVE_W)
    D.d1_red2 = Line(_p(D.mid_x, yd), _p(XS - 0.3, yd)).set_stroke(RED, WAVE_W)
    D.d1_div = VGroup(Line(_p(XS - 0.3, yd), _p(XS, yd + h2)), Line(_p(XS - 0.3, yd), _p(XS, yd - h2))).set_stroke(TEAL, WAVE_W)
    D.d1_post = pair(XS, TX1, yd, TEAL)
    # Q: old value, then a clean X t_pc after E2
    D.q_pre = pair(TX0, QX[0], yq, GREEN)
    D.q_x = VGroup(Line(_p(QX[0], yq + h2), _p(QX[1], yq - h2)),
                   Line(_p(QX[0], yq - h2), _p(QX[1], yq + h2))).set_stroke(GREEN, WAVE_W)
    D.q_post = pair(QX[1], TX1, yq, GREEN)
    # the rising edges (for flashes)
    D.edge1 = Line(_p(E1 - SLOPE / 2, yc - h2), _p(E1 + SLOPE / 2, yc + h2))
    D.edge2 = Line(_p(E2 - SLOPE / 2, yc - h2), _p(E2 + SLOPE / 2, yc + h2))
    # dimensions
    D.tc = dim_arrow(E1, E2, TC_Y, YELLOW, "T_c")
    D.tc.lab.move_to(_p(E2 + 0.42, TC_Y + 0.22))       # above-right of the arrow, clear of the high CLK level
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


# ---- ch2_s3_shiftreg.py build_chain() (and its make_ff), copied: the ghost ----------------------
K = 0.6
FF_X = (-3.6, -0.2, 3.2)
HX = (BOX_W / 2 + WIRE) * K


def _sr_ff():
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    g = VGroup(d_w, q_w, box, tri, d_l, q_l)
    g.box, g.clk_w, g.d_l, g.q_l, g.d_w = box, clk_w, d_l, q_l, d_w
    return g


def build_chain(fy):
    C = VGroup()
    C.ffs = []
    for x in FF_X:
        f = _sr_ff()
        f.scale(K, about_point=ORIGIN).shift(_p(x, fy))
        f.clk_w.scale(K, about_point=ORIGIN).shift(_p(x, fy))
        for lb in (f.d_l, f.q_l):
            lb.scale(1.3, about_point=lb.get_center())
        C.ffs.append(f)
    qy = fy + PIN_Y * K
    C.links = [Line(_p(FF_X[i] + HX, qy), _p(FF_X[i + 1] - HX, qy)).set_stroke(GREEN, 5) for i in range(2)]
    C.tail = Line(_p(FF_X[2] + HX, qy), _p(FF_X[2] + HX + 0.45, qy)).set_stroke(GREEN, 5)
    rx = [(FF_X[0] + FF_X[1]) / 2, (FF_X[1] + FF_X[2]) / 2, FF_X[2] + HX + 0.45]
    top = fy + BOX_H / 2 * K + 0.22
    C.risers = [Line(_p(x, qy), _p(x, top)).set_stroke(GREEN, 5) for x in rx]
    C.dots = [Dot(_p(x, qy), radius=0.07, color=GREEN) for x in rx[:2]]
    C.qls = [MathTex(f"Q_{i}", font_size=40, color=GREEN).next_to(_p(x, top), UP, buff=0.1)
             for i, x in enumerate(rx)]
    C.names = [T(f"FF{i}", 32).next_to(f.box, UP, buff=0.15) for i, f in enumerate(C.ffs)]
    C.din = MathTex("D_{in}", font_size=40, color=BLUE).next_to(C.ffs[0].d_w.get_start(), LEFT, buff=0.12)
    by = fy - (BOX_H / 2 + EN_WIRE) * K
    C.by = by
    C.bus = Line(_p(FF_X[0] - 1.2, by), _p(FF_X[2], by)).set_stroke(YELLOW, 5)
    C.jdots = [Dot(_p(x, by), radius=0.07, color=YELLOW) for x in FF_X[:2]]
    C.clk_ws = [f.clk_w for f in C.ffs]
    C.clk_l = T("CLK", 32, YELLOW).next_to(C.bus.get_start(), LEFT, buff=0.15)
    return C


GHOST_Y = -1.6
GHOST_OP = 0.45


def grow_dim(arr):
    """ch1_s5's grow_dim: a DoubleArrow grown from its centre at true tip size."""
    start, end = arr.get_start(), arr.get_end()
    mid, half = (start + end) / 2, (end - start) / 2
    final = arr.copy()

    def upd(m, a):
        if a >= 1:
            m.become(final)
            return
        if a * np.linalg.norm(end - start) < 0.4:
            m.become(final).set_opacity(0)
            return
        m.become(DoubleArrow(mid - a * half, mid + a * half, buff=0, stroke_width=DIM_W,
                             tip_length=0.16, max_tip_length_to_length_ratio=0.4,
                             color=final.get_color()))

    return UpdateFromAlphaFunc(arr, upd, rate_func=smooth)


def sweep_in(group, x0, x1):
    """ch1_s5's sweep_in: draw every line of `group` left to right, as a pen from x0 to x1."""
    leaves = group.family_members_with_points()
    origs = [m.copy() for m in leaves]

    def upd(_, a):
        X = x0 + a * (x1 - x0)
        for leaf, orig in zip(leaves, origs):
            lx0, lx1 = orig.get_left()[0], orig.get_right()[0]
            if lx1 - lx0 < 1e-6:
                frac = 1.0 if X >= lx0 else 0.0
            else:
                frac = min(1.0, max(0.0, (X - lx0) / (lx1 - lx0)))
            if a >= 1:
                frac = 1.0
            leaf.pointwise_become_partial(orig, 0, frac)
            leaf.set_stroke(opacity=orig.get_stroke_opacity() if frac * (lx1 - lx0) > 0.15 or frac >= 1
                            else 0)

    return UpdateFromAlphaFunc(group, upd, rate_func=linear)


def pulse(line, color=YELLOW, width=9):
    """A bright bump running along a wire (a copy, removed at the end)."""
    return VShowPassingFlash(line.copy().set_stroke(color, width), time_width=0.5)


class Synchroniser(NarratedScene):
    def construct(self):
        C = sync_circuit()
        D = sync_timing()

        # ---------------------------------------------------------------- clip 1
        with self.say("c4.sync.1") as c:
            G = decay_graph().shift(0.2 * DOWN)
            self.play(FadeIn(G), run_time=0.8)
            prob = T("Metastability gives rise to severe system problems", 36, RED).move_to(_p(0, 0.25))
            G.generate_target()
            G.target.scale(0.45).to_corner(UL, buff=0.45)
            G.target.labels.set_opacity(0)      # the thumbnail keeps only the axes and the curve
            self.play(*during(MoveToTarget(G), 0, 0.6), *during(appear(prob), 0.5, 1),
                      run_time=min(2.2, c.until("so we have")))
            mini = VGroup(MathTex(r"\rightarrow", font_size=44, color=FG),
                          T("minimise its probability:", 36)).arrange(RIGHT, buff=0.2).move_to(_p(0, -0.7))
            c.wait_until("unlikely")
            self.play(*appear(mini), run_time=1.0)
            syn = T("a synchroniser (cascaded flip-flops)", 36, YELLOW).move_to(_p(0, -1.5))
            c.wait_until(own_word=syn)
            self.play(*appear(syn), run_time=1.0)

            c.wait_until("circuit")
            sweep_clear(self, *appear(C.btn, C.d0_w, C.ff0, C.names[0], shift=None, lag=0.15),
                        syn.animate.move_to(_p(0.3, 0.4)), keep=[syn], run_time=1.8)
            c.wait_until("one more")
            self.play(*appear(C.ff1, C.names[1], shift=None, lag=0.2), run_time=1.2)

            c.wait_until("The input")
            self.play(*appear(C.d0_l), pulse(C.d0_w), run_time=1.2)
            c.wait_until("whose output")
            self.play(Create(C.link), run_time=1.0)
            c.wait_until("dee one")
            self.play(*appear(C.d1_l), run_time=0.9)
            c.wait_until("goes straight")
            self.play(pulse(C.ff0.q_w), pulse(C.link), pulse(C.ff1.d_w), run_time=1.2)
            c.wait_until("Its output")
            self.play(*appear(C.q_l), pulse(C.ff1.q_w), run_time=1.0)

            c.wait_until("shiftreg")
            self.play(Create(C.bus), *[Create(w) for w in C.clk_ws], FadeIn(C.jdot),
                      *during(appear(C.clk_l), 0.4, 1), run_time=1.5)
            self.play(pulse(C.bus), run_time=1.0)

            # the ghost: ch2 s3's three-stage chain, under the circuit
            S = build_chain(GHOST_Y)
            ghost = [*S.ffs, *S.names, *S.links, S.tail, *S.risers, *S.dots, *S.qls, S.din,
                     S.bus, *S.jdots, *S.clk_ws, S.clk_l]
            for m in ghost:
                for sub in m.family_members_with_points():
                    sub.set_stroke(opacity=GHOST_OP)
                    if sub.get_fill_opacity() > 0:
                        sub.set_fill(opacity=GHOST_OP)
            c.wait_until("shift register")
            self.play(*[FadeIn(m) for m in ghost], run_time=1.0)
            drop = [S.ffs[2], S.names[2], S.clk_ws[2], S.tail, S.risers[2], S.qls[2]]
            keep = [m for m in ghost if all(m is not d for d in drop) and m is not S.bus]
            s = (SFF_X[1] - SFF_X[0]) / (FF_X[1] - FF_X[0])
            piv = _p(FF_X[0], GHOST_Y)
            moves = []
            for m in keep:
                m.generate_target()
                m.target.scale(s, about_point=piv).shift((SFF_X[0] - FF_X[0]) * RIGHT)
                moves.append(MoveToTarget(m))
            nb_y = GHOST_Y + s * (S.by - GHOST_Y)
            new_bus = Line(_p(s * (-1.2) + SFF_X[0], nb_y), _p(SFF_X[1], nb_y)).set_stroke(YELLOW, 5, opacity=GHOST_OP)
            tag = T("a two-stage shift register", 32, FG).move_to(_p(0.2, 3.36))
            c.wait_until("with just")
            self.play(*during(disappear(*drop), 0, 0.4), *during(moves, 0.25, 0.85),
                      *during([ReplacementTransform(S.bus, new_bus)], 0.25, 0.85),
                      *during(appear(tag), 0.6, 1), run_time=min(1.8, c.until(floor=0.8)))
            ghost_left = keep + [new_bus]

        # ---------------------------------------------------------------- clip 2
        with self.say("c4.sync.2") as c:
            traces = VGroup(D.clk, D.d1_pre, D.q_pre)
            self.play(*during(disappear(*ghost_left, syn), 0, 0.35),
                      *during([sweep_in(traces, TX0, TX1)], 0.35, 1),
                      *during(appear(*D.labs, shift=None, lag=0.15), 0.4, 0.9),  # early: row labels of the diagram
                      run_time=min(2.0, c.until("meta")))
            c.wait_until("Suppose")
            self.play(FadeIn(C.finger, shift=0.3 * RIGHT), run_time=0.7)
            c.wait_until("bad moment")
            self.play(C.finger.animate.shift(PUSH * RIGHT), C.btn.stem.animate.shift(PUSH * RIGHT),
                      C.btn.cap.animate.shift(PUSH * RIGHT), pulse(C.d0_w), run_time=0.9)
            c.wait_until("At this edge")
            self.play(FlashAround(D.edge1, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("zero goes")
            self.play(*during(disappear(tag), 0, 0.5), sweep_in(VGroup(D.d1_conv, D.d1_red1), E1, D.mid_x),
                      *recolor(C.d1_wires, RED), C.d1_l.animate.set_color(RED), run_time=1.8)
            c.wait_until("sits halfway")
            self.play(FlashAround(D.d1_red1, run_time=1.2, time_width=1.5, color=RED), run_time=1.2)

            c.wait_until("next edge")
            self.play(FlashAround(D.edge2, run_time=1.2, time_width=1.5), FadeIn(D.tcx), grow_dim(D.tc.arr),
                      *during(appear(D.tc.lab, shift=None), 0.5, 1), run_time=1.5)
            c.wait_until("so dee one")
            self.play(sweep_in(VGroup(D.d1_red2, D.d1_div, D.d1_post), D.mid_x, TX1),
                      *during(recolor(C.d1_wires, TEAL), 0.35, 0.7),
                      *during([C.d1_l.animate.set_color(TEAL)], 0.35, 0.7),
                      run_time=min(3.0, c.until(floor=1.5)))

        # ---------------------------------------------------------------- clip 3
        with self.say("c4.sync.3") as c:
            self.play(FadeIn(D.g1), FadeIn(D.gs), *during([grow_dim(D.tres.arr)], 0.3, 1),
                      *during(appear(D.tres.lab, shift=None), 0.6, 1), run_time=1.6)
            c.wait_until("time before")
            self.play(FadeIn(D.g2), *during([grow_dim(D.tsu.arr)], 0.3, 1),
                      *during(appear(D.tsu.lab, shift=None), 0.6, 1), run_time=1.5)

            tick = check_mark(GREEN).move_to(C.ff1.box.get_right() + _p(0.42, -0.45))
            c.wait_until("settled by then")
            self.play(FlashAround(Line(_p(XS, TROW["D1"] + 0.25), _p(E2, TROW["D1"] - 0.25)),
                                  run_time=1.2, time_width=1.5, color=TEAL), run_time=1.2)
            c.wait_until("valid input")
            self.play(pulse(C.link), pulse(C.ff1.d_w), *during(appear(tick, shift=None), 0.4, 1),
                      run_time=1.2)

            c.wait_until("valid output")
            self.play(sweep_in(VGroup(D.q_x, D.q_post), QX[0] - 0.01, TX1), pulse(C.ff1.q_w),
                      FlashAround(C.q_l, run_time=1.5, time_width=1.5, color=GREEN), run_time=1.5)
            c.wait_until("delay after")
            self.play(FadeIn(D.gq), *during([grow_dim(D.tpc.arr)], 0.2, 1),
                      *during(appear(D.tpc.lab, shift=None), 0.5, 1), run_time=1.3)

            likely = VGroup(MathTex("D_1", font_size=34, color=TEAL),
                            T("will resolve to a valid level with high probability if", 28),
                            MathTex("T_c", font_size=34, color=YELLOW),
                            T("is long enough", 28)).arrange(RIGHT, buff=0.13).move_to(_p(0, -3.38))
            for m in (likely[1], likely[3]):
                m.align_to(likely[0], DOWN)
            c.wait_until("likely")
            self.play(*appear(likely, shift=None), run_time=1.0)

        # ---------------------------------------------------------------- clip 4
        with self.say("c4.sync.4") as c:
            yd = TROW["D1"]
            self.play(FlashAround(VGroup(D.d1_div, Line(_p(XS, yd + 0.25), _p(XS + 0.8, yd - 0.25))),
                                  run_time=1.4, time_width=1.5, color=TEAL), run_time=1.4)
            old = T("old value", 28, FG)
            new = T("new value", 28, FG)
            old.move_to(_p(TX1 + 0.25 + old.width / 2, yd - ROW_H / 2))     # right of where the D1 rails end
            new.move_to(_p(TX1 + 0.25 + new.width / 2, yd + ROW_H / 2))
            t_old = check_mark(GREEN).scale(0.75).next_to(old, RIGHT, buff=0.18)
            t_new = check_mark(GREEN).scale(0.75).next_to(new, RIGHT, buff=0.18)
            c.wait_until("old value")
            self.play(*appear(old, t_old, lag=0.3), run_time=1.1)
            c.wait_until("new one")
            self.play(*appear(new, t_new, lag=0.3), run_time=1.1)
            c.wait_until("one period later")
            self.play(pulse(Line(_p(E1, TC_Y), _p(E2, TC_Y))), run_time=1.4)

            risk = T("takes the risk", 30, RED).move_to(_p(SFF_X[0], 3.36))
            sees = T("sees a settled input", 30, GREEN).move_to(_p(SFF_X[1], 3.36))
            c.wait_until(own_word=risk)
            self.play(restyle(C.ff0.box, outline=RED), *appear(risk), run_time=1.2)
            c.wait_until(own_word=sees)
            self.play(restyle(C.ff1.box, outline=GREEN), *appear(sees), run_time=1.2)

        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
